# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Teil "pfoten" von baer_beine_gj2.py (PLAN.md 4.3, Weg A = Graft). Neu.
# Die Pfoten des Standard-Jungen (GLB d9931d32 = 2c-Baerenfuss x0,9402, von Kevin abgenommen) werden an die kurzen Beine des
# Generator-Jungen gesetzt:
#   1. Gen-Bein unter z_g (neu) weg, Gen-Bein darueber zum Schnitt hin leicht verjuengt (Mitte des Querschnitts, x/y getrennt)
#   2. Std-Pfote unter z_s (ueber ihrer Sohle) ausgeschnitten, Sprung-/Handgelenk auf das neue Gelenk geschoben (keine Drehung,
#      keine Laengen-Skalierung), Sohle auf z 0; oberer Teil (Fellkranz) per Ring-Morph auf den Gen-Ring (je Winkel), unter
#      morph_h0 (Zehen, Krallen, Sohle) unveraendert
#   3. Dreiecks-Budget: Halbkanten-Kollaps (QEM) nur im Inneren der Std-Pfote (nicht an Krallen, UV-Naehten, Ring)
#   4. Naht-Band: Reissverschluss zwischen Gen-Ring (oben) und Std-Ring (unten), Bogenlaenge ab gleichem Winkel; eigene UV-Streifen
#   5. UV-Atlas: Gen-UV x 880/1024 zur Ecke (0,0); Std-Pfoten-Inseln (Bounding-Box, Regal-Packung) und Band-Streifen in den freien
#      Streifen u > 0,86 / v > 0,86; Textur: Gen verkleinert, Std-Inseln aus der Std-Textur (Ausschnitt skaliert), Band gemischt
# Ausgabe: NETZ_GJ2.npz (Felder wie netz_rig.npz + teil/teil_T/quelle), GEWICHTE_START.npz (W, namen), Textur, Atlas-JSON.
# Statisch/offline, nicht gespielt.
import heapq
import json
import math
import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_beine_gj2 as BG  # noqa: E402
import baer_export_gj2 as X  # noqa: E402

Q = BG.Q
T0 = time.time()
GR = 1024
UVS = 880.0 / 1024.0                 # Gen-Atlas zur Ecke (0,0): genau 880 Pixel
BEINE = {"VL": (1, 1), "VR": (1, -1), "HL": (-1, 1), "HR": (-1, -1)}
PAR = dict(
    z_g=dict(V=0.165, H=0.165),       # Gen-Schnitt (neu, z)
    z_s=dict(V=0.130, H=0.130),       # Std-Schnitt ueber der eigenen Sohle
    morph_h0=0.05,                    # darunter bleibt die Std-Pfote unveraendert (Zehen, Krallen, Sohle)
    verjung=dict(V=(0.92, 0.96), H=(0.80, 0.90)),    # Gen-Querschnitt am Schnitt x/y (1 = nicht); hinten staerker (Ton-Bild: Klotz)
    verjung_oben=dict(V=0.27, H=0.245),             # bis hier (z) laeuft die Verjuengung auf 1
    budget=19850,
    insel_rand_px=3, insel_abstand_px=4, uv_dichte_ziel=None,
    gen_ausdehnen_px=8,               # Gen-Textur vor dem Verkleinern ueber die Inselraender hinaus fuellen (kein Schwarz in den Naehten)
    rand_ausdehnen_px=4,              # zum Schluss: Texel bis 4 px neben jeder Insel = Mittel der Insel-Texel (Mip-Stufen, Hell-Faktor)
    kranz_angleich=(0.06, 0.01),      # Std-Fell 6..1 cm unter dem Ring je Kanal weich auf die Gen-Farbe am Ring ziehen (Naht ohne Stufe)
)
# Unterbein heller (Vorstufe): Ruecken = Texel mit z > 0,72 und x < 0,25 (ohne Kopf), Unterbein = z_g..0,30
PAR_HELL = dict(ruecken_z=0.72, ruecken_x=0.25, unten_z=0.30, ziel=0.66, max=1.45, aus=(0.28, 0.42))


def log(*a):
    print("PFOTEN", round(time.time() - T0, 1), *a, flush=True)


sst = BG.sst


# =================================================================================================================================
# Hilfen
# =================================================================================================================================
def schweissen(P, tol=1e-6):
    q = np.round(np.asarray(P) / tol).astype(np.int64)
    _, idx, inv = np.unique(q, axis=0, return_index=True, return_inverse=True)
    return inv.ravel(), idx


def rand_kanten(T):
    E = np.sort(np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]])), 1)
    u, c = np.unique(E, axis=0, return_counts=True)
    return u[c == 1], u[c > 2]


def schleifen(T):
    """Gerichtete Randkanten (Reihenfolge wie in den Dreiecken) -> geordnete Schleifen."""
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]))
    key = {}
    for a, b in E:
        key[(int(a), int(b))] = key.get((int(a), int(b)), 0) + 1
    nxt = {}
    for (a, b) in key:
        if (b, a) not in key:
            nxt[a] = b
    out = []
    seen = set()
    for s in list(nxt):
        if s in seen:
            continue
        L = [s]
        seen.add(s)
        c = nxt[s]
        while c != s:
            L.append(c)
            seen.add(c)
            c = nxt[c]
        out.append(np.array(L))
    return out


def lies_std():
    J, B = X.lade_json_glb(Q + "std/NCBearCub.glb")
    pr = J["meshes"][0]["primitives"][0]
    a = pr["attributes"]
    P = X.acc_np(J, B, a["POSITION"]).astype(float) * (1, 1, -1)
    Nn = X.acc_np(J, B, a["NORMAL"]).astype(float) * (1, 1, -1)
    UV = X.acc_np(J, B, a["TEXCOORD_0"]).astype(float)
    Ji = X.acc_np(J, B, a["JOINTS_0"]).astype(int)
    Wt = X.acc_np(J, B, a["WEIGHTS_0"]).astype(float)
    F = X.acc_np(J, B, pr["indices"]).reshape(-1, 3).astype(int)
    names = [J["nodes"][k]["name"] for k in J["skins"][0]["joints"]]
    W = np.zeros((len(P), len(names)))
    for k in range(4):
        np.add.at(W, (np.arange(len(P)), Ji[:, k]), Wt[:, k])
    T = BG.tier(P)
    NT = np.stack((-Nn[:, 2], Nn[:, 0], Nn[:, 1]), 1)
    # glTF-Dreiecke zeigen nach aussen (Export dreht, wenn das Volumen negativ waere) -> Wicklung tier pruefen
    return dict(P=T, N=NT, UV=UV, W=W, F=F, names=names)


def gelenke_std():
    sys.path.insert(0, "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
    import g_lib as g
    std = g.lies("C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/plan/dump/std.txt")
    return {n: g.tier(np.linalg.inv(std["off"][std["idx"][n]])[:3, 3]) for n in std["names"]}


def volumen(P, T):
    return float(np.einsum("ij,ij->i", P[T[:, 0]], np.cross(P[T[:, 1]], P[T[:, 2]])).sum() / 6.0)


def uv_flaeche(UV, F):
    u = UV
    return 0.5 * np.abs((u[F[:, 1], 0] - u[F[:, 0], 0]) * (u[F[:, 2], 1] - u[F[:, 0], 1])
                        - (u[F[:, 2], 0] - u[F[:, 0], 0]) * (u[F[:, 1], 1] - u[F[:, 0], 1]))


def flaeche3(P, F):
    return 0.5 * np.linalg.norm(np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]), axis=1)


# =================================================================================================================================
# QEM-Halbkanten-Kollaps (nur Std-Pfote; GLB-Ebene mit Schweiss-Ids)
# =================================================================================================================================
def kollaps(P, F, wid, geschuetzt, ziel_weg):
    """P: GLB-Punkte (tier), F: GLB-Dreiecke, wid: Schweiss-Id je GLB-Punkt, geschuetzt: je Schweiss-Id (darf nicht wandern).
    Halbkante u -> v auf Schweiss-Ebene; u nur, wenn u genau EINEN GLB-Punkt hat (keine UV-Naht). Gibt neue F (GLB) zurueck."""
    F = F.copy()
    alive = np.ones(len(F), bool)
    nW = wid.max() + 1
    glb_von = [[] for _ in range(nW)]
    for gpt, w_ in enumerate(wid):
        glb_von[w_].append(gpt)
    pos = np.zeros((nW, 3))
    pos[wid] = P
    Fw = wid[F]
    tri_von = [set() for _ in range(nW)]
    for t, (a, b, c) in enumerate(Fw):
        tri_von[a].add(t)
        tri_von[b].add(t)
        tri_von[c].add(t)
    Qm = np.zeros((nW, 4, 4))

    def ebene(t):
        a, b, c = pos[Fw[t]]
        n = np.cross(b - a, c - a)
        ar = np.linalg.norm(n)
        if ar < 1e-14:
            return np.zeros((4, 4))
        n = n / ar
        p = np.r_[n, -n @ a]
        return np.outer(p, p) * ar * 0.5
    for t in range(len(F)):
        K = ebene(t)
        for w_ in Fw[t]:
            Qm[w_] += K
    frei = np.array([len(glb_von[w_]) == 1 and not geschuetzt[w_] for w_ in range(nW)])

    def nachbarn(w_):
        s = set()
        for t in tri_von[w_]:
            s.update(Fw[t].tolist())
        s.discard(w_)
        return s

    def kosten(u, v):
        h = np.r_[pos[v], 1.0]
        return float(h @ Qm[u] @ h) + 1e-4 * float(np.sum((pos[u] - pos[v]) ** 2))
    heap = []
    for u in range(nW):
        if frei[u]:
            for v in nachbarn(u):
                heapq.heappush(heap, (kosten(u, v), u, v))
    weg = 0
    tot = np.zeros(nW, bool)
    while heap and weg < ziel_weg:
        c, u, v = heapq.heappop(heap)
        if tot[u] or tot[v] or not frei[u]:
            continue
        if abs(c - kosten(u, v)) > 1e-12 * max(1.0, abs(c)):
            continue
        Nu, Nv = nachbarn(u), nachbarn(v)
        if v not in Nu:
            continue
        gem = [t for t in tri_von[u] if v in Fw[t]]
        if len(gem) != 2:
            continue
        opp = set()
        for t in gem:
            opp.update(Fw[t].tolist())
        opp -= {u, v}
        if (Nu & Nv) != opp:
            continue
        # Umklappen / Entarten pruefen
        ok = True
        for t in tri_von[u]:
            if t in gem:
                continue
            tri = Fw[t]
            a0 = pos[tri]
            n0 = np.cross(a0[1] - a0[0], a0[2] - a0[0])
            a1 = a0.copy()
            a1[list(tri).index(u)] = pos[v]
            n1 = np.cross(a1[1] - a1[0], a1[2] - a1[0])
            l1 = np.linalg.norm(n1)
            if l1 < 1e-10 or (n0 @ n1) / (np.linalg.norm(n0) * l1 + 1e-30) < 0.3:
                ok = False
                break
            # Seitenverhaeltnis nicht schlechter als 1:12
            ed = [np.linalg.norm(a1[i] - a1[(i + 1) % 3]) for i in range(3)]
            if l1 / max(ed) ** 2 < 1.0 / 12.0:
                ok = False
                break
        if not ok:
            continue
        gu = glb_von[u][0]
        # GLB-Punkt von v im selben UV-Teil: der in den gemeinsamen Dreiecken
        gv = None
        for t in gem:
            for gp in F[t]:
                if wid[gp] == v:
                    gv = gp
        for t in gem:
            alive[t] = False
            for w_ in Fw[t]:
                tri_von[w_].discard(t)
        for t in list(tri_von[u]):
            k = list(Fw[t]).index(u)
            Fw[t][k] = v
            F[t][k] = gv
            tri_von[v].add(t)
        tri_von[u] = set()
        tot[u] = True
        Qm[v] += Qm[u]
        weg += 2
        for w_ in nachbarn(v) | {v}:
            if frei[w_] and not tot[w_]:
                for z in nachbarn(w_):
                    heapq.heappush(heap, (kosten(w_, z), w_, z))
    return F[alive], weg


# =================================================================================================================================
# Ringe, Morph, Reissverschluss
# =================================================================================================================================
def ring_param(R, c):
    """Ring (k x 3, geordnet) -> gegen den Uhrzeigersinn (von oben) gedreht, Start beim Winkel 0 um c, Bogenlaenge 0..1."""
    xy = R[:, :2] - c[:2]
    fl = 0.5 * np.sum(xy[:, 0] * np.roll(xy[:, 1], -1) - np.roll(xy[:, 0], -1) * xy[:, 1])
    ordn = np.arange(len(R))
    if fl < 0:
        ordn = ordn[::-1]
    xy = xy[ordn]
    th = np.arctan2(xy[:, 1], xy[:, 0])
    s0 = int(np.argmin(np.abs(th)))
    ordn = np.roll(ordn, -s0)
    Rq = R[ordn]
    d = np.linalg.norm(np.diff(np.r_[Rq, Rq[:1]], axis=0), axis=1)
    s = np.r_[0.0, np.cumsum(d)[:-1]] / d.sum()
    return ordn, s


def radius_funktion(R, c, n=360):
    """Ring -> Punkt auf dem Ring je Winkel (n Winkel), linear zwischen den Ringpunkten (Strahl-Schnitt)."""
    th = np.linspace(-np.pi, np.pi, n, endpoint=False)
    out = np.zeros((n, 2))
    A = R[:, :2] - c[:2]
    B = np.roll(A, -1, 0)
    for i, t in enumerate(th):
        dv = np.array((math.cos(t), math.sin(t)))
        best = None
        for a, b in zip(A, B):
            e = b - a
            M = np.array([[dv[0], -e[0]], [dv[1], -e[1]]])
            det = np.linalg.det(M)
            if abs(det) < 1e-14:
                continue
            r, u = np.linalg.solve(M, a)
            if r > 0 and -1e-9 <= u <= 1 + 1e-9:
                if best is None or r > best:
                    best = r
        out[i] = dv * (best if best is not None else 0.0)
    return th, out


def reissverschluss(A, sA, B, sB):
    """Band zwischen Schleife A (oben) und B (unten), beide gleich gerichtet, Parameter 0..1. Ids als Listen; A[0]/B[0] am Ende
    nochmals (Schluss). Liefert Dreiecke (Ids) und je Dreieck die Lage (fuer UV: Parameter je Ecke, oben/unten)."""
    nA, nB = len(A), len(B)
    i = j = 0
    T = []
    while i < nA or j < nB:
        a0, b0 = A[i % nA], B[j % nB]
        ta = sA[i + 1] if i + 1 < nA else 1.0
        tb = sB[j + 1] if j + 1 < nB else 1.0
        if j >= nB or (i < nA and ta <= tb):
            a1 = A[(i + 1) % nA]
            T.append(((a0, 0, i), (b0, 1, j), (a1, 0, i + 1)))
            i += 1
        else:
            b1 = B[(j + 1) % nB]
            T.append(((a0, 0, i), (b0, 1, j), (b1, 1, j + 1)))
            j += 1
    return T


# =================================================================================================================================
# Raster in UV (fuer Textur-Masken und das Band)
# =================================================================================================================================
def raster_uv(UVpx, F, W=GR, H=GR):
    """Dreiecke in Pixel-UV -> (tid, b1, b2) je Pixel (letzter gewinnt)."""
    tid = np.full((H, W), -1, int)
    b1 = np.zeros((H, W))
    b2 = np.zeros((H, W))
    for t, (i, j, k) in enumerate(F):
        xa, ya = UVpx[i]
        xb, yb = UVpx[j]
        xc, yc = UVpx[k]
        mnx, mxx = int(max(0, math.floor(min(xa, xb, xc)))), int(min(W - 1, math.ceil(max(xa, xb, xc))))
        mny, mxy = int(max(0, math.floor(min(ya, yb, yc)))), int(min(H - 1, math.ceil(max(ya, yb, yc))))
        if mxx < mnx or mxy < mny:
            continue
        den = (yb - yc) * (xa - xc) + (xc - xb) * (ya - yc)
        if abs(den) < 1e-12:
            continue
        gx, gy = np.meshgrid(np.arange(mnx, mxx + 1) + 0.5, np.arange(mny, mxy + 1) + 0.5)
        l1 = ((yb - yc) * (gx - xc) + (xc - xb) * (gy - yc)) / den
        l2 = ((yc - ya) * (gx - xc) + (xa - xc) * (gy - yc)) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
        if not ins.any():
            continue
        sub = tid[mny:mxy + 1, mnx:mxx + 1]
        sub[ins] = t
        b1[mny:mxy + 1, mnx:mxx + 1][ins] = l1[ins]
        b2[mny:mxy + 1, mnx:mxx + 1][ins] = l2[ins]
    return tid, b1, b2


def ausdehnen(img, voll, n):
    """Leere Texel (voll False) n Schritte lang mit dem Mittel ihrer vollen 8 Nachbarn fuellen; Rueckgabe neue Kopie."""
    img = img.copy()
    voll = voll.copy()
    for _ in range(n):
        acc = np.zeros_like(img)
        cnt = np.zeros(voll.shape)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                acc += np.roll(np.roll(img * voll[..., None], dy, 0), dx, 1)
                cnt += np.roll(np.roll(voll, dy, 0), dx, 1)
        neu = ~voll & (cnt > 0)
        if not neu.any():
            break
        img[neu] = acc[neu] / cnt[neu][:, None]
        voll |= neu
    return img


def bilinear(img, u, v):
    """img H x W x 3 float, u/v Pixel-Koordinaten (Mitte = +0,5)."""
    H, W = img.shape[:2]
    x = np.clip(u - 0.5, 0, W - 1.0001)
    y = np.clip(v - 0.5, 0, H - 1.0001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    return ((1 - fx) * (1 - fy) * img[y0, x0] + fx * (1 - fy) * img[y0, x0 + 1] + (1 - fx) * fy * img[y0 + 1, x0]
            + fx * fy * img[y0 + 1, x0 + 1])


def regal(boxen, frei, abstand):
    """Regal-Packung: boxen [(w, h)] (Pixel) in die freien Rechtecke frei [(x0, y0, x1, y1)]. Hoehe absteigend.
    Rueckgabe Liste (x, y) oder None."""
    ordn = sorted(range(len(boxen)), key=lambda i: -boxen[i][1])
    pos = [None] * len(boxen)
    for (x0, y0, x1, y1) in frei:
        pass
    # je freies Rechteck Regale von oben nach unten
    zustand = [dict(r=r, y=r[1], x=r[0], h=0) for r in frei]
    for i in ordn:
        w, h = boxen[i]
        ok = False
        for z in zustand:
            x0, y0, x1, y1 = z["r"]
            if w + abstand > x1 - x0:
                continue
            if z["x"] + w + abstand <= x1 and z["y"] + h + abstand <= y1:
                pos[i] = (z["x"] + abstand, z["y"] + abstand)
                z["x"] += w + abstand
                z["h"] = max(z["h"], h + abstand)
                ok = True
                break
            # neues Regal
            ny = z["y"] + z["h"]
            if ny + h + abstand <= y1:
                z["y"], z["x"], z["h"] = ny, x0, 0
                pos[i] = (z["x"] + abstand, z["y"] + abstand)
                z["x"] += w + abstand
                z["h"] = h + abstand
                ok = True
                break
        if not ok:
            return None
    return pos


# =================================================================================================================================
# Ebenen-Schnitt (12.11., Nachbesserung): Ringe GENAU auf z0 statt gezackter Randschleifen (Band 3,5 cm hoch statt -0,3..11 cm)
# =================================================================================================================================
def ebenen_schnitt(Pw, Tw, Tg, gp, UV, Ww, betroffen, z0, oben_bleibt, fang=0.003):
    """Schneidet die Dreiecke 'betroffen' an der Ebene z = z0. Punkte naeher als 'fang' an der Ebene werden auf sie gesetzt.
    oben_bleibt: True -> Teil ueber der Ebene bleibt (Gen), False -> Teil darunter (Std).
    Pw/Ww: Schweiss-Ebene (Lage, Gewichte), Tw/Tg: Dreiecke (Schweiss/GLB), gp: GLB -> Schweiss, UV: je GLB.
    Rueckgabe: neue Pw, Ww, gp, UV, Tw, Tg (nur behaltene Dreiecke) und Maske 'neu_auf_ebene' je Schweiss-Punkt."""
    Pw, Ww, gp, UV = Pw.copy(), Ww.copy(), gp.copy(), UV.copy()
    nah = np.abs(Pw[:, 2] - z0) < fang
    beteiligt = np.zeros(len(Pw), bool)
    beteiligt[Tw[betroffen].ravel()] = True
    Pw[nah & beteiligt, 2] = z0
    auf = beteiligt & (Pw[:, 2] == z0)
    bleibt = (Pw[:, 2] >= z0) if oben_bleibt else (Pw[:, 2] <= z0)
    neuP, neuW, neuGP, neuUV = [], [], [], []
    k_w, k_g = {}, {}

    def kante_w(a, b):
        key = (min(a, b), max(a, b))
        if key not in k_w:
            za, zb = Pw[a, 2], Pw[b, 2]
            t = (z0 - za) / (zb - za)
            p = Pw[a] + t * (Pw[b] - Pw[a])
            p[2] = z0
            k_w[key] = len(Pw) + len(neuP)
            neuP.append(p)
            neuW.append(Ww[a] + t * (Ww[b] - Ww[a]))
        return k_w[key]

    def kante_g(ga, gb):
        a, b = gp[ga], gp[gb]
        if auf[a]:
            return ga
        key = (min(ga, gb), max(ga, gb))
        if key not in k_g:
            za, zb = Pw[a, 2], Pw[b, 2]
            t = (z0 - za) / (zb - za)
            k_g[key] = len(gp) + len(neuGP)
            neuGP.append(kante_w(a, b))
            neuUV.append(UV[ga] + t * (UV[gb] - UV[ga]))
        return k_g[key]
    outW, outG = [], []
    for t in range(len(Tw)):
        tw, tg = Tw[t], Tg[t]
        if not betroffen[t]:
            outW.append(tw)
            outG.append(tg)
            continue
        b = bleibt[tw]
        nb = int(b.sum())
        if nb == 3:
            outW.append(tw)
            outG.append(tg)
            continue
        if nb == 0:
            continue
        # drehen: bei nb == 1 steht der bleibende Punkt vorn, bei nb == 2 der wegfallende hinten
        if nb == 1:
            r = int(np.argmax(b))
        else:
            r = (int(np.argmin(b)) + 1) % 3
        tw = np.roll(tw, -r)
        tg = np.roll(tg, -r)
        if nb == 1:
            g1 = kante_g(tg[0], tg[1]) if not auf[tw[0]] else tg[0]
            g2 = kante_g(tg[0], tg[2]) if not auf[tw[0]] else tg[0]
            if auf[tw[0]]:
                continue                                   # nur ein Punkt auf der Ebene: nichts uebrig
            tri = [(tg[0], g1, g2)]
        else:
            g12 = kante_g(tg[1], tg[2]) if not auf[tw[1]] else tg[1]
            g20 = kante_g(tg[0], tg[2]) if not auf[tw[0]] else tg[0]
            tri = []
            if g12 != tg[1]:
                tri.append((tg[0], tg[1], g12))
            if g20 != tg[0] and g20 != g12:
                tri.append((tg[0], g12, g20))
            elif g20 == tg[0] and g12 != tg[1]:
                pass
            if not tri:
                tri = [(tg[0], tg[1], g12)]
        for (a_, b_, c_) in tri:
            gw = []
            for gg in (a_, b_, c_):
                gw.append(gp[gg] if gg < len(gp) else neuGP[gg - len(gp)])
            if len(set(gw)) < 3:
                continue
            outW.append(np.array(gw))
            outG.append(np.array((a_, b_, c_)))
    if neuP:
        Pw = np.concatenate((Pw, np.array(neuP)))
        Ww = np.concatenate((Ww, np.array(neuW)))
    if neuGP:
        gp = np.concatenate((gp, np.array(neuGP, int)))
        UV = np.concatenate((UV, np.array(neuUV)))
    ring = np.zeros(len(Pw), bool)
    ring[len(Pw) - len(neuP):] = True
    ring[:len(auf)] |= auf
    return Pw, Ww, gp, UV, np.array(outW, int), np.array(outG, int), ring


# =================================================================================================================================
# Hauptteil
# =================================================================================================================================
def bein_knochen(k):
    s = k[1]
    if k[0] == "V":
        return ["Bip01_%s_%s" % (s, b) for b in ("UpperArm", "Forearm", "Hand")], "Bip01_%s_Hand" % s
    return ["Bip01_%s_%s" % (s, b) for b in ("Thigh", "Calf", "Foot", "Toe0")], "Bip01_%s_Foot" % s


def pfoten(skp, netz1, aus_netz, aus_gew, aus_png, aus_atlas=None, par_json=None):
    P_ = dict(PAR)
    if par_json:
        P_.update(json.load(open(par_json)))
    sk = json.load(open(skp))
    names = sk["namen"]
    JN = {n: np.array(v, float) for n, v in sk["ruhe_m"].items()}
    N = np.load(netz1)
    V = N["V"].astype(float).copy()
    T, Tg, gp, UVg = N["T"].copy(), N["T_glb"].copy(), N["glb_punkt"], N["UV"].astype(float)
    G = np.load(Q + "gen/gewichte_end.npz")
    W = G["W"].astype(float)
    assert [str(n) for n in G["namen"]] == names
    S = lies_std()
    assert S["names"] == names
    JS = gelenke_std()
    info = {}
    # Wicklung: beide geschlossenen Netze nach aussen (Volumen > 0)
    if volumen(V, T) < 0:
        T, Tg = T[:, ::-1].copy(), Tg[:, ::-1].copy()
    if volumen(S["P"], S["F"]) < 0:
        S["F"] = S["F"][:, ::-1].copy()
    # ------------------------------------------------------------------ 1. Gen: Verjuengung und Schnitt
    gen_ringe = {}
    for k, (sx, sy) in BEINE.items():
        art = k[0]
        zg, zt = P_["z_g"][art], P_["verjung_oben"][art]
        q = (np.sign(V[:, 0]) == sx) & (np.sign(V[:, 1]) == sy)

        def mitte(z0):
            m_ = q & (np.abs(V[:, 2] - z0) < 0.012)
            return V[m_, :2].mean(0)
        c0, c1 = mitte(zg), mitte(zt)
        m = q & (V[:, 2] < zt)
        z = V[m, 2]
        u = sst(zg, zt, z)
        c = c0[None, :] + ((np.clip(z, zg, zt) - zg) / (zt - zg))[:, None] * (c1 - c0)[None, :]
        fx, fy = P_["verjung"][art]
        s_x = 1.0 - (1.0 - fx) * (1.0 - u)
        s_y = 1.0 - (1.0 - fy) * (1.0 - u)
        V[m, 0] = c[:, 0] + s_x * (V[m, 0] - c[:, 0])
        V[m, 1] = c[:, 1] + s_y * (V[m, 1] - c[:, 1])
        # Ebenen-Schnitt bei z_g (Dreiecke dieses Beins unterhalb z_g + 6 cm)
        betr = q[T].all(1) & (V[T][:, :, 2].min(1) < zg + 0.06)
        V, W, gp, UVg, T, Tg, _r = ebenen_schnitt(V, T, Tg, gp, UVg, W, betr, zg, True)
    Tk, Tgk = T, Tg
    for L in schleifen(Tk):
        cc = V[L].mean(0)
        k = [kk for kk, (sx, sy) in BEINE.items() if np.sign(cc[0]) == sx and np.sign(cc[1]) == sy]
        assert len(k) == 1 and k[0] not in gen_ringe, ("Gen-Ring", cc, k)
        gen_ringe[k[0]] = L
    assert len(gen_ringe) == 4, len(gen_ringe)
    info["gen"] = dict(dreiecke_bleiben=int(len(Tk)), ring_punkte={k: int(len(v)) for k, v in gen_ringe.items()},
                       ring_z={k: [round(float(V[v, 2].min()), 4), round(float(V[v, 2].max()), 4)] for k, v in gen_ringe.items()})
    log("GEN", info["gen"])
    # ------------------------------------------------------------------ 2. Std-Pfoten ausschneiden (Ebenen-Schnitt) und verschieben
    P0 = S["P"]
    wid0, rep0 = schweissen(P0)
    Pw_s = P0[rep0].copy()
    Ww_s = S["W"][rep0].copy()
    for s_ in "LR":
        Ww_s[:, names.index("Bip01_%s_Foot" % s_)] += Ww_s[:, names.index("Bip01_%s_Toe0" % s_)]
        Ww_s[:, names.index("Bip01_%s_Toe0" % s_)] = 0.0
    gp_s, UV_s = wid0.copy(), S["UV"].copy()
    std_F = {}
    std_info = {}
    for k, (sx, sy) in BEINE.items():
        art = k[0]
        q = (np.sign(Pw_s[:, 0]) == sx) & (np.sign(Pw_s[:, 1]) == sy) & (Pw_s[:, 2] < 0.25)
        sohle = float(Pw_s[q, 2].min())
        sub = q[gp_s[S["F"]]].all(1)
        Fg_k = S["F"][sub]
        Fw_k = gp_s[Fg_k]
        Pw_s, Ww_s, gp_s, UV_s, Fw_k, Fg_k, _r = ebenen_schnitt(Pw_s, Fw_k, Fg_k, gp_s, UV_s, Ww_s, np.ones(len(Fw_k), bool),
                                                               sohle + P_["z_s"][art], False)
        std_F[k] = Fg_k
        std_info[k] = dict(sohle_std=round(sohle, 4), dreiecke=int(len(Fg_k)))
    # Verschieben (je Bein: Sprung-/Handgelenk auf das neue Gelenk, Sohle auf z 0)
    P_orig = Pw_s.copy()
    for k in BEINE:
        _kn, gel = bein_knochen(k)
        idx = np.unique(gp_s[std_F[k]])
        sohle = std_info[k]["sohle_std"]
        d = np.array((JN[gel][0] - JS[gel][0], JN[gel][1] - JS[gel][1], -sohle))
        Pw_s[idx] += d
        std_info[k]["versatz"] = np.round(d, 4).tolist()
    log("STD", std_info)
    # GLB-Ebene der Std-Teile wie vorher (S, Ps, wid_s, rep_s), Normalen der neuen Schnittpunkte 0
    nG0 = len(S["P"])
    N_s = np.zeros((len(gp_s), 3))
    N_s[:nG0] = S["N"]
    S = dict(P=P_orig[gp_s], UV=UV_s, W=Ww_s[gp_s], N=N_s, F=None, names=names)
    Ps = Pw_s[gp_s]
    wid_s = gp_s
    rep_s = np.zeros(len(Pw_s), int)
    rep_s[gp_s[::-1]] = np.arange(len(gp_s))[::-1]
    # Krallen (fast punktfoermige UV, wie baer_textur_jfuss.krallen_schalen), Ringe, Schutz
    F_alle = np.concatenate([std_F[k] for k in BEINE])
    r = uv_flaeche(S["UV"], F_alle) / np.maximum(flaeche3(S["P"], F_alle), 1e-12)
    kr_tri = r < 0.02 * np.median(r)
    kralle_w = np.zeros(wid_s.max() + 1, bool)
    kralle_w[wid_s[F_alle[kr_tri]].ravel()] = True
    std_ringe = {}
    for k in BEINE:
        Ls = schleifen(wid_s[std_F[k]])
        assert len(Ls) == 1, (k, len(Ls))
        std_ringe[k] = Ls[0]
    ring_w = np.zeros(wid_s.max() + 1, bool)
    for k in BEINE:
        ring_w[std_ringe[k]] = True
    # ------------------------------------------------------------------ 3. Dreiecks-Budget
    n_band = sum(len(gen_ringe[k]) + len(std_ringe[k]) for k in BEINE)
    n_gesamt = len(Tk) + len(F_alle) + n_band
    zuviel = n_gesamt - P_["budget"]
    info["budget"] = dict(gen=int(len(Tk)), std=int(len(F_alle)), band=int(n_band), summe_vorher=int(n_gesamt), budget=P_["budget"])
    if zuviel > 0:
        Pw = np.zeros((wid_s.max() + 1, 3))
        Pw[wid_s] = Ps
        schutz = kralle_w | ring_w
        # Ringnaehe (2 cm) ebenfalls schuetzen: dort soll der Morph glatt bleiben
        for k in BEINE:
            R = Pw[std_ringe[k]]
            dmin = np.min(np.linalg.norm(Pw[:, None, :] - R[None, ::2, :], axis=2), axis=1)
            schutz |= dmin < 0.02
        F_neu, weg = kollaps(Ps, F_alle, wid_s, schutz, zuviel + (zuviel % 2))
        log("KOLLAPS", "weg", weg, "Dreiecke", len(F_alle), "->", len(F_neu))
        F_alle = F_neu
        cc = Ps[F_alle].mean(1)
        for k, (sx, sy) in BEINE.items():
            std_F[k] = F_alle[(np.sign(cc[:, 0]) == sx) & (np.sign(cc[:, 1]) == sy)]
        info["budget"]["kollaps_weg"] = int(weg)
    # ------------------------------------------------------------------ 4. Ring-Morph (oberer Teil der Std-Pfote auf den Gen-Ring)
    morph_info = {}
    for k in BEINE:
        art = k[0]
        A = gen_ringe[k]
        B = std_ringe[k]                                   # Schweiss-Ids Std
        Bg = rep_s[B]                                      # ein GLB-Punkt je Ring-Id (Lage)
        cA = V[A].mean(0)
        cB = Ps[Bg].mean(0)
        thA, RA = radius_funktion(V[A], cA)
        thB, RB = radius_funktion(Ps[Bg], cB)
        D = (cA[:2] + RA) - (cB[:2] + RB)                  # je Winkel
        idx = np.unique(std_F[k])
        p = Ps[idx]
        w = sst(P_["morph_h0"], P_["z_s"][art], p[:, 2])
        th = np.arctan2(p[:, 1] - cB[1], p[:, 0] - cB[0])
        thp = np.r_[thA, thA[0] + 2 * np.pi]
        Dx = np.interp(th, thp, np.r_[D[:, 0], D[0, 0]])
        Dy = np.interp(th, thp, np.r_[D[:, 1], D[0, 1]])
        Ps[idx, 0] += w * Dx
        Ps[idx, 1] += w * Dy
        fakt = np.linalg.norm(RA, axis=1) / np.maximum(np.linalg.norm(RB, axis=1), 1e-9)
        morph_info[k] = dict(ring_faktor_min=round(float(fakt.min()), 3), ring_faktor_max=round(float(fakt.max()), 3),
                             mitte_versatz_cm=np.round((cA[:2] - cB[:2]) * 100, 2).tolist(),
                             gen_ring_xy_cm=[round(float(np.ptp(V[A, 0])) * 100, 1), round(float(np.ptp(V[A, 1])) * 100, 1)],
                             std_ring_xy_cm=[round(float(np.ptp(S["P"][Bg, 0])) * 100, 1), round(float(np.ptp(S["P"][Bg, 1])) * 100, 1)])
    info["morph"] = morph_info
    log("MORPH", morph_info)
    return locals()


def zusammenbau(L):
    """Teil 5-9: Band, Netz zusammensetzen, Gewichte, UV-Atlas, Textur, Masken. L = locals() von pfoten_form()."""
    V, Tk, Tgk, gp, UVg, W, S, Ps, wid_s, rep_s = (L[k] for k in ("V", "Tk", "Tgk", "gp", "UVg", "W", "S", "Ps", "wid_s", "rep_s"))
    std_F, gen_ringe, std_ringe, names, info, P_ = (L[k] for k in ("std_F", "gen_ringe", "std_ringe", "names", "info", "P_"))
    N = L["N"]
    F_alle = np.concatenate([std_F[k] for k in BEINE])
    # ------------------------------------------------------------------ Schweiss-Ebene: neue Ids
    g_alt = np.unique(Tk)
    g_neu = -np.ones(len(V), int)
    g_neu[g_alt] = np.arange(len(g_alt))
    s_alt = np.unique(wid_s[F_alle])
    s_neu = -np.ones(wid_s.max() + 1, int)
    s_neu[s_alt] = len(g_alt) + np.arange(len(s_alt))
    Pw = np.zeros((wid_s.max() + 1, 3))
    Pw[wid_s] = Ps
    VN = np.concatenate((V[g_alt], Pw[s_alt]))
    teil = np.r_[np.zeros(len(g_alt), int), np.ones(len(s_alt), int)]
    T_gen = g_neu[Tk]
    T_std = s_neu[wid_s[F_alle]]
    # ------------------------------------------------------------------ GLB-Ebene
    gg_alt = np.unique(Tgk)
    gg_neu = -np.ones(len(gp), int)
    gg_neu[gg_alt] = np.arange(len(gg_alt))
    sg_alt = np.unique(F_alle)
    sg_neu = -np.ones(len(S["P"]), int)
    sg_neu[sg_alt] = len(gg_alt) + np.arange(len(sg_alt))
    glb_punkt = np.r_[g_neu[gp[gg_alt]], s_neu[wid_s[sg_alt]]]
    assert (glb_punkt >= 0).all()
    Tg_gen = gg_neu[Tgk]
    Tg_std = sg_neu[F_alle]
    assert (glb_punkt[Tg_gen] == T_gen).all() and (glb_punkt[Tg_std] == T_std).all()
    # ------------------------------------------------------------------ 5. Band (Reissverschluss)
    band_T, band_Tg, band_glb = [], [], []           # band_glb: (Schweiss-Id, Bein, oben/unten, Parameter)
    band_info = {}
    for bi, k in enumerate(BEINE):
        A = g_neu[gen_ringe[k]]
        B = s_neu[std_ringe[k]]
        c = VN[A].mean(0)
        oA, sA = ring_param(VN[A], c)
        oB, sB = ring_param(VN[B], c)
        A, B = A[oA], B[oB]
        tri = reissverschluss(list(A), sA, list(B), sB)
        # Wicklung: Normale nach aussen (vom Ring-Mittelpunkt weg)
        nach_aussen = 0
        for (a, _, _), (b, _, _), (cc, _, _) in tri:
            p = VN[[a, b, cc]]
            n = np.cross(p[1] - p[0], p[2] - p[0])
            m = p.mean(0) - c
            m[2] = 0.0
            nach_aussen += 1 if n @ m > 0 else -1
        umdrehen = nach_aussen < 0
        sA_e, sB_e = np.r_[sA, 1.0], np.r_[sB, 1.0]
        n0 = len(band_glb)
        karte = {}
        for t in tri:
            ids, ec = [], []
            for (v, ob, i) in t:
                par = (sA_e if ob == 0 else sB_e)[i]
                key = (v, ob, i == (len(A) if ob == 0 else len(B)))
                if key not in karte:
                    karte[key] = len(band_glb)
                    band_glb.append((v, bi, ob, par))
                ids.append(v)
                ec.append(karte[key])
            if umdrehen:
                ids, ec = ids[::-1], ec[::-1]
            band_T.append(ids)
            band_Tg.append(ec)
        band_info[k] = dict(dreiecke=len(tri), gen_ring=int(len(A)), std_ring=int(len(B)), umgedreht=bool(umdrehen),
                            hoehe_cm=[round(float((VN[A, 2].min() - VN[B, 2].max()) * 100), 2), round(float((VN[A, 2].max() - VN[B, 2].min()) * 100), 2)],
                            glb_punkte=len(band_glb) - n0)
    info["band"] = band_info
    log("BAND", band_info)
    band_T = np.array(band_T, int)
    n_glb0 = len(glb_punkt)
    band_Tg = np.array(band_Tg, int) + n_glb0
    glb_punkt = np.r_[glb_punkt, np.array([b[0] for b in band_glb], int)]
    TN = np.concatenate((T_gen, T_std, band_T))
    TgN = np.concatenate((Tg_gen, Tg_std, band_Tg))
    teil_T = np.r_[np.zeros(len(T_gen), int), np.ones(len(T_std), int), np.full(len(band_T), 2)]
    assert (glb_punkt[TgN] == TN).all()
    # Naht glaetten (Nachbesserung nach dem Ton-Bild: Kante/"Manschette" an den Ringen): Laplace nur quer (x, y), z bleibt; frei sind
    # Gen-Punkte bis 3 cm ueber dem Gen-Ring und Std-Punkte bis 3 cm unter dem Std-Ring (samt Ringen), Rand fest
    zg_, zs_ = P_["z_g"]["H"], P_["z_s"]["H"]
    zone = ((teil == 0) & (VN[:, 2] < zg_ + 0.03)) | ((teil == 1) & (VN[:, 2] > zs_ - 0.03) & (VN[:, 2] < zs_ + 1e-6))
    Ek = np.unique(np.sort(np.concatenate((TN[:, [0, 1]], TN[:, [1, 2]], TN[:, [2, 0]])), 1), axis=0)
    deg = np.bincount(Ek[:, 0], minlength=len(VN)) + np.bincount(Ek[:, 1], minlength=len(VN))
    for _ in range(P_.get("naht_glatt", 12)):
        acc = np.zeros_like(VN)
        np.add.at(acc, Ek[:, 0], VN[Ek[:, 1]])
        np.add.at(acc, Ek[:, 1], VN[Ek[:, 0]])
        mit = acc / np.maximum(deg, 1)[:, None]
        VN[zone, :2] = 0.5 * VN[zone, :2] + 0.5 * mit[zone, :2]
    info["naht_glatt_punkte"] = int(zone.sum())
    # Pruefung: geschlossen, mannigfaltig
    r_, nm_ = rand_kanten(TN)
    info["netz"] = dict(punkte=int(len(VN)), glb_punkte=int(len(glb_punkt)), dreiecke=int(len(TN)), offen=int(len(r_)),
                        nicht_mannigfaltig=int(len(nm_)), volumen=round(volumen(VN, TN), 5))
    log("NETZ", info["netz"])
    # ------------------------------------------------------------------ 6. Gewichte (Schweiss-Ebene)
    WN = np.zeros((len(VN), len(names)))
    WN[:len(g_alt)] = W[g_alt]
    Ws = S["W"][rep_s[s_alt]].copy()
    for s in "LR":
        Ws[:, names.index("Bip01_%s_Foot" % s)] += Ws[:, names.index("Bip01_%s_Toe0" % s)]
        Ws[:, names.index("Bip01_%s_Toe0" % s)] = 0.0
    WN[len(g_alt):] = Ws
    # Gleichheit der Std-Gewichte an UV-Naehten (gleiche Lage -> gleiche Gewichte)
    dW = 0.0
    for gpt in sg_alt:
        dW = max(dW, float(np.abs(S["W"][gpt] - S["W"][rep_s[wid_s[gpt]]]).max()))
    info["gewichte"] = dict(std_naht_abweichung_max=dW, summe_abw=float(np.abs(WN.sum(1) - 1).max()))
    # ------------------------------------------------------------------ 7. UV-Atlas und Textur
    UVN = np.zeros((len(glb_punkt), 2))
    UVN[:len(gg_alt)] = UVg[gg_alt] * UVS
    tex_gen = np.asarray(Image.open(Q + "gen/NCBearCub.png").convert("RGB")).astype(float)
    # Nachbesserung 12.11. (Blatt nah): der schwarze Hintergrund der Gen-Textur blutete beim Verkleinern in die Inselraender -> dunkle
    # "Risse" an den UV-Naehten der Beine. Darum die Gen-Textur zuerst von ihren (verbliebenen) Dreiecken aus nach aussen fuellen.
    tidG0 = raster_uv(UVg * GR, Tgk)[0]
    tex_gen = ausdehnen(tex_gen, tidG0 >= 0, P_["gen_ausdehnen_px"])
    info["gen_ausgedehnt_texel"] = int(((tidG0 < 0) & (tex_gen.sum(2) > 0)).sum())
    tex_std = np.asarray(Image.open(Q + "std/NCBearCub.png").convert("RGB")).astype(float)
    img = np.zeros((GR, GR, 3))
    voll = np.zeros((GR, GR), bool)
    gen_kl = np.asarray(Image.fromarray(tex_gen.astype(np.uint8)).resize((880, 880), Image.LANCZOS)).astype(float)
    img[:880, :880] = gen_kl
    voll[:880, :880] = True
    # Std-Inseln
    par = np.arange(len(S["P"]))

    def wurzel(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for t in F_alle:
        a = wurzel(t[0])
        for v in t[1:]:
            b = wurzel(v)
            if a != b:
                par[b] = a
    tri_w = np.array([wurzel(t[0]) for t in F_alle])
    inseln = []
    for wv in np.unique(tri_w):
        vv = np.unique(F_alle[tri_w == wv])
        uvp = S["UV"][vv] * GR
        m = P_["insel_rand_px"]
        x0, y0 = int(math.floor(uvp[:, 0].min() - m)), int(math.floor(uvp[:, 1].min() - m))
        x1, y1 = int(math.ceil(uvp[:, 0].max() + m)), int(math.ceil(uvp[:, 1].max() + m))
        inseln.append(dict(v=vv, box=(x0, y0, x1, y1), wurzel=wv))
    A3 = flaeche3(Ps, F_alle).sum()
    Auv = uv_flaeche(S["UV"], F_alle).sum()
    A3g = flaeche3(V, Tk).sum()
    Auvg = uv_flaeche(UVg * UVS, Tgk).sum()
    s_ziel = math.sqrt((Auvg / A3g) / (Auv / A3)) if P_["uv_dichte_ziel"] is None else P_["uv_dichte_ziel"]
    band_h, band_w = 18, 214
    frei = [(882, 0, GR, GR), (0, 882, 880, GR - band_h - 4)]
    s = min(s_ziel, 1.6)
    pos = None
    while s > 0.4:
        boxen = [(int(math.ceil((b["box"][2] - b["box"][0]) * s)), int(math.ceil((b["box"][3] - b["box"][1]) * s))) for b in inseln]
        pos = regal(boxen, frei, P_["insel_abstand_px"])
        if pos is not None:
            break
        s *= 0.97
    assert pos is not None
    for b, (px, py) in zip(inseln, pos):
        x0, y0, x1, y1 = b["box"]
        w_, h_ = int(math.ceil((x1 - x0) * s)), int(math.ceil((y1 - y0) * s))
        xs = x0 + (np.arange(w_) + 0.5) / s
        ys = y0 + (np.arange(h_) + 0.5) / s
        gx, gy = np.meshgrid(xs, ys)
        img[py:py + h_, px:px + w_] = bilinear(tex_std, gx, gy)
        voll[py:py + h_, px:px + w_] = True
        for v in b["v"]:
            uvp = S["UV"][v] * GR
            UVN[sg_neu[v]] = ((px + (uvp[0] - x0) * s) / GR, (py + (uvp[1] - y0) * s) / GR)
        b["ziel"] = (px, py, w_, h_)
    info["atlas"] = dict(gen_skala=UVS, std_dichte_faktor_ziel=round(s_ziel, 3), std_skala=round(s, 3), inseln=len(inseln),
                         uv_dichte_gen=round(Auvg / A3g, 4), uv_dichte_std_neu=round(Auv * s * s / A3, 4))
    log("ATLAS", info["atlas"])
    # ---- (a) Unterbeine heller (PLAN 3.1 Vorstufe: Unterbein >= 0,65 x Ruecken; GESICHT macht es endgueltig): Faktor nach der
    #      3D-Hoehe je Texel (Gen-Dreiecke im Atlas gerastert), weich ab z 0,42 nach unten, gleiche Hoehe = gleicher Faktor (Naehte)
    nTg = len(Tg_gen)
    tid, b1, b2 = raster_uv(UVN * GR, TgN[:nTg])
    mm = tid >= 0
    tt = TgN[:nTg][tid[mm]]
    PzG = VN[glb_punkt][:, 2]
    zt = b1[mm] * PzG[tt[:, 0]] + b2[mm] * PzG[tt[:, 1]] + (1 - b1[mm] - b2[mm]) * PzG[tt[:, 2]]
    PxG = VN[glb_punkt][:, 0]
    xt = b1[mm] * PxG[tt[:, 0]] + b2[mm] * PxG[tt[:, 1]] + (1 - b1[mm] - b2[mm]) * PxG[tt[:, 2]]
    luma = lambda c_: c_ @ np.array([0.299, 0.587, 0.114])
    Lpx = luma(img[mm])
    hm = PAR_HELL
    ruecken = float(np.median(Lpx[(zt > hm["ruecken_z"]) & (xt < hm["ruecken_x"])]))
    unten = (zt < hm["unten_z"]) & (zt > P_["z_g"]["H"])
    L_unten = float(np.median(Lpx[unten]))
    k_hell = float(np.clip(hm["ziel"] * ruecken / max(L_unten, 1.0), 1.0, hm["max"]))
    fz = 1.0 + (k_hell - 1.0) * (1.0 - sst(hm["aus"][0], hm["aus"][1], zt))
    img[mm] = np.clip(img[mm] * fz[:, None], 0, 255)
    L2 = luma(img[mm])
    info["hell"] = dict(ruecken_L=round(ruecken, 1), unterbein_L_vorher=round(L_unten, 1), faktor=round(k_hell, 3),
                        unterbein_L_nachher=round(float(np.median(L2[unten])), 1),
                        verhaeltnis_vorher=round(L_unten / ruecken, 3), verhaeltnis_nachher=round(float(np.median(L2[unten])) / ruecken, 3))
    log("HELL", info["hell"])
    # ---- (b) Std-Fell (nicht Sohle/Ballen, nicht Krallen) je Bein auf die Gen-Beinfarbe am Ring ziehen (je Kanal, Mediane: Gen-Ring
    #      gegen Std-Fell 8..13 cm ueber der Sohle; vorn ist das Std-Fell dunkler als hinten)
    Nstd = np.cross(Ps[F_alle[:, 1]] - Ps[F_alle[:, 0]], Ps[F_alle[:, 2]] - Ps[F_alle[:, 0]])
    Nstd /= np.maximum(np.linalg.norm(Nstd, axis=1, keepdims=True), 1e-12)
    r_kr = uv_flaeche(S["UV"], F_alle) / np.maximum(flaeche3(S["P"], F_alle), 1e-12)
    kr_t = r_kr < 0.02 * np.median(r_kr)
    for b in inseln:
        tm = tri_w == b["wurzel"]
        nz = float(np.average(Nstd[tm, 2], weights=flaeche3(Ps, F_alle[tm]) + 1e-12))
        b["art"] = "kralle" if kr_t[tm].mean() > 0.5 else ("sohle" if nz < -0.45 else "fell")
        cc = Ps[b["v"]].mean(0)
        b["bein"] = [k for k, (sx, sy) in BEINE.items() if np.sign(cc[0]) == sx and np.sign(cc[1]) == sy][0]
    info["fellkranz"] = {}
    for k in BEINE:
        kand = np.nonzero(np.isin(glb_punkt[:len(gg_alt)], g_neu[gen_ringe[k]]))[0]
        c_gen = np.median(bilinear(img, UVN[kand, 0] * GR, UVN[kand, 1] * GR), 0)
        fp = []
        for b in inseln:
            if b["art"] == "fell" and b["bein"] == k:
                vv = b["v"]
                sel = vv[(Ps[vv, 2] > P_["z_s"][k[0]] - 0.035)]      # Fell nahe am Ring (Farbe an der Naht)
                if len(sel):
                    fp.append(bilinear(img, UVN[sg_neu[sel], 0] * GR, UVN[sg_neu[sel], 1] * GR))
        c_std = np.median(np.concatenate(fp), 0)
        ratio = np.clip(c_gen / np.maximum(c_std, 1.0), 0.7, 1.9)
        for b in inseln:
            if b["art"] == "fell" and b["bein"] == k:
                px, py, w_, h_ = b["ziel"]
                img[py:py + h_, px:px + w_] = np.clip(img[py:py + h_, px:px + w_] * ratio, 0, 255)
        info["fellkranz"][k] = dict(gen_ring=np.round(c_gen, 1).tolist(), std_fell=np.round(c_std, 1).tolist(), faktor=np.round(ratio, 3).tolist())
    info["fellkranz"]["inseln"] = {a: sum(1 for b in inseln if b["art"] == a) for a in ("fell", "sohle", "kralle")}
    log("FELLKRANZ", info["fellkranz"])
    # ---- (b2) heller Rand der Std-Pfote direkt unter dem Ring (Fellspitzen nach x1,6 heller, im Bild als Linie sichtbar): je Bein die
    #      Texel 0..2,5 cm unter dem Ring auf die Helligkeit 2,5..5 cm darunter ziehen (Faktor nach 3D-Hoehe, weich)
    ist = np.nonzero(teil_T == 1)[0]
    tidS, b1S, b2S = raster_uv(UVN * GR, TgN[ist])
    mS = tidS >= 0
    ttS = TgN[ist][tidS[mS]]
    PG3 = VN[glb_punkt]
    zS = b1S[mS] * PG3[ttS[:, 0], 2] + b2S[mS] * PG3[ttS[:, 1], 2] + (1 - b1S[mS] - b2S[mS]) * PG3[ttS[:, 2], 2]
    xS = b1S[mS] * PG3[ttS[:, 0], 0] + b2S[mS] * PG3[ttS[:, 1], 0] + (1 - b1S[mS] - b2S[mS]) * PG3[ttS[:, 2], 0]
    yS = b1S[mS] * PG3[ttS[:, 0], 1] + b2S[mS] * PG3[ttS[:, 1], 1] + (1 - b1S[mS] - b2S[mS]) * PG3[ttS[:, 2], 1]
    colS = img[mS]
    LS = colS @ np.array([0.299, 0.587, 0.114])
    rand_info = {}
    for k, (sx_, sy_) in BEINE.items():
        zs_ = P_["z_s"][k[0]]
        q = (np.sign(xS) == sx_) & (np.sign(yS) == sy_)
        rim = q & (zS > zs_ - 0.03)
        unt = q & (zS > zs_ - 0.06) & (zS <= zs_ - 0.03)
        if rim.sum() > 20 and unt.sum() > 20:
            # helle Fellspitzen-Texel kappen: Helligkeit hoechstens 1,08 x Median darunter, weich ab 3 cm unter dem Ring
            L_ref = float(np.median(LS[unt])) * 1.08
            w = sst(zs_ - 0.03, zs_ - 0.015, zS[q])
            Lq = LS[q]
            fak = np.where(Lq > L_ref, L_ref / np.maximum(Lq, 1.0), 1.0)
            fak = 1.0 - w * (1.0 - fak)
            colS[q] = colS[q] * fak[:, None]
            rand_info[k] = dict(rand_L_p90=round(float(np.percentile(LS[rim], 90)), 1), darunter_L=round(float(np.median(LS[unt])), 1),
                                gekappt=int((fak < 0.999).sum()))
    img[mS] = colS
    info["std_rand"] = rand_info
    log("STD-RAND", rand_info)
    # ---- (b3) Nachbesserung 12.11. (Blatt nah: unter dem Band ein dunkler, olivstichiger Streifen, Helligkeit Gen 74 -> Std 58..62):
    #      Std-Fell 6..1 cm unter dem Ring je Bein und Kanal weich auf die Gen-Farbe am Ring (Gen-Texel z_g..z_g+3 cm) ziehen; je 1-cm-
    #      Scheibe Median -> Ziel = w x Gen-Ring + (1 - w) x eigener Median, w = smoothstep(z_s - 6 cm, z_s - 1 cm); Faktor je Texel nach z
    #      linear zwischen den Scheiben (keine Stufen). Krallen/Sohle liegen tiefer (unberuehrt).
    yt = b1[mm] * VN[glb_punkt][tt[:, 0], 1] + b2[mm] * VN[glb_punkt][tt[:, 1], 1] + (1 - b1[mm] - b2[mm]) * VN[glb_punkt][tt[:, 2], 1]
    colG = img[mm]
    angl = {}
    k0, k1 = P_["kranz_angleich"]
    for k, (sx_, sy_) in BEINE.items():
        zg_k, zs_k = P_["z_g"][k[0]], P_["z_s"][k[0]]
        gq = (np.sign(xt) == sx_) & (np.sign(yt) == sy_) & (zt >= zg_k) & (zt < zg_k + 0.03)
        ref = np.median(colG[gq], 0)
        q = (np.sign(xS) == sx_) & (np.sign(yS) == sy_) & (zS > zs_k - k0 - 0.01)
        zc = np.arange(zs_k - k0 - 0.005, zs_k, 0.01)
        gain = np.ones((len(zc), 3))
        for i_, z_ in enumerate(zc):
            qq = q & (np.abs(zS - z_) <= 0.005)
            if qq.sum() < 20:
                continue
            med = np.median(colS[qq], 0)
            w = float(sst(zs_k - k0, zs_k - k1, z_))
            gain[i_] = (w * ref + (1 - w) * med) / np.maximum(med, 1.0)
        fq = np.stack([np.interp(zS[q], zc, gain[:, c_], left=1.0, right=gain[-1, c_]) for c_ in range(3)], 1)
        colS[q] = np.clip(colS[q] * fq, 0, 255)
        # Farbton nahe am Ring (5..1,5 cm darunter, bis 70 %) auf den Ton des Gen-Rings: eigene Helligkeit x Gen-Farbverhaeltnis
        # (das Std-Fell hat vorn oliv-gruenliche Spitzen, nah als Fleck unter dem Band sichtbar)
        hq = 0.7 * sst(zs_k - 0.05, zs_k - 0.015, zS[q])
        Lq = colS[q] @ np.array([0.299, 0.587, 0.114])
        ton = Lq[:, None] * (ref / max(float(ref @ np.array([0.299, 0.587, 0.114])), 1.0))[None, :]
        colS[q] = np.clip((1 - hq[:, None]) * colS[q] + hq[:, None] * ton, 0, 255)
        angl[k] = dict(gen_ring=np.round(ref, 1).tolist(), faktor_ring=np.round(gain[-1], 3).tolist(), faktor_6cm=np.round(gain[0], 3).tolist())
    img[mS] = colS
    info["kranz_angleich"] = angl
    log("KRANZ-ANGLEICH", angl)
    img_n = img.copy()
    # ---- (c) Band: Fell gespiegelt -- oben das Gen-Bein ueber dem Ring (an z_g gespiegelt), unten die Std-Pfote unter ihrem Ring
    #      (an z_s gespiegelt), in der Mitte ueberblendet. Strahl waagerecht vom Ring-Mittelpunkt im Winkel des Ringpunkts.
    by0 = GR - band_h - 2
    band_rects = {}
    for bi, k in enumerate(BEINE):
        band_rects[k] = (4 + bi * (band_w + 6), by0, band_w, band_h)

    def strahl(c3, th, zz, Ptri, UVtri):
        d = np.array((math.cos(th), math.sin(th), 0.0))
        o = np.array((c3[0], c3[1], zz))
        e1 = Ptri[:, 1] - Ptri[:, 0]
        e2 = Ptri[:, 2] - Ptri[:, 0]
        pv = np.cross(d[None, :], e2)
        det = (e1 * pv).sum(1)
        ok = np.abs(det) > 1e-12
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        tv = o[None, :] - Ptri[:, 0]
        u = (tv * pv).sum(1) * inv
        qv = np.cross(tv, e1)
        v = (qv @ d) * inv
        tt_ = (e2 * qv).sum(1) * inv
        hit = ok & (u >= -1e-6) & (v >= -1e-6) & (u + v <= 1 + 1e-6) & (tt_ > 0)
        if not hit.any():
            return None
        i = int(np.argmax(np.where(hit, tt_, -1)))
        return (1 - u[i] - v[i]) * UVtri[i, 0] + u[i] * UVtri[i, 1] + v[i] * UVtri[i, 2]
    PG = VN[glb_punkt]
    for k, (bx0, by0_, bw, bh) in band_rects.items():
        bi = list(BEINE).index(k)
        eintraege = [(i, b) for i, b in enumerate(band_glb) if b[1] == bi]
        for i, (v, _bi, ob, prm) in eintraege:
            UVN[n_glb0 + i] = ((bx0 + 2 + prm * (bw - 4)) / GR, (by0_ + 2 + ob * (bh - 4)) / GR)
        oben = sorted([(prm, v) for (i, (v, _b, ob, prm)) in eintraege if ob == 0])
        unten = sorted([(prm, v) for (i, (v, _b, ob, prm)) in eintraege if ob == 1])
        cA = VN[[v for _p, v in oben]].mean(0)
        thA = np.unwrap([math.atan2(VN[v, 1] - cA[1], VN[v, 0] - cA[0]) for _p, v in oben])
        thB = np.unwrap([math.atan2(VN[v, 1] - cA[1], VN[v, 0] - cA[0]) for _p, v in unten])
        pA = np.array([p for p, _ in oben] + [1.0])
        pB = np.array([p for p, _ in unten] + [1.0])
        thA = np.r_[thA, thA[0] + 2 * np.pi * np.sign(thA[-1] - thA[0] if len(thA) > 1 else 1)]
        thB = np.r_[thB, thB[0] + 2 * np.pi * np.sign(thB[-1] - thB[0] if len(thB) > 1 else 1)]
        zg, zs = P_["z_g"][k[0]], P_["z_s"][k[0]]
        hb = zg - zs
        sx_, sy_ = BEINE[k]
        cg = np.nonzero(teil_T == 0)[0]
        cent = PG[TgN[cg]].mean(1)
        selg = cg[(np.sign(cent[:, 0]) == sx_) & (np.sign(cent[:, 1]) == sy_) & (cent[:, 2] < zg + hb + 0.03)]
        cs = np.nonzero(teil_T == 1)[0]
        cent = PG[TgN[cs]].mean(1)
        sels = cs[(np.sign(cent[:, 0]) == sx_) & (np.sign(cent[:, 1]) == sy_) & (cent[:, 2] > zs - hb - 0.03)]
        PtG, UVtG = PG[TgN[selg]], UVN[TgN[selg]]
        PtS, UVtS = PG[TgN[sels]], UVN[TgN[sels]]
        for xx in range(bw):
            prm = np.clip((xx + 0.5 - 2) / (bw - 4), 0, 1)
            ta = float(np.interp(prm, pA, thA))
            tb = float(np.interp(prm, pB, thB))
            for yy in range(bh):
                t = np.clip((yy + 0.5 - 2) / (bh - 4), 0, 1)
                th = (1 - t) * ta + t * tb
                a = sst(0.55, 1.0, t)          # meist gespiegeltes Gen-Fell, erst unten in die Std-Farbe
                cols, ws = [], []
                if a < 1:
                    uv = strahl(cA, th, zg + max(t * hb, 0.003), PtG, UVtG)
                    if uv is not None:
                        cols.append(bilinear(img_n, np.array([uv[0] * GR]), np.array([uv[1] * GR]))[0])
                        ws.append(1 - a)
                if a > 0:
                    uv = strahl(cA, th, zs - 0.004 - 0.25 * max((1 - t) * hb, 0.0), PtS, UVtS)
                    if uv is not None:
                        cols.append(bilinear(img_n, np.array([uv[0] * GR]), np.array([uv[1] * GR]))[0])
                        ws.append(a)
                if cols:
                    img[by0_ + yy, bx0 + xx] = np.average(np.array(cols), axis=0, weights=np.array(ws) + 1e-9)
        # ungetroffene Texel (Strahl verfehlt): Spaltenmittel, sonst Nachbarzeile
        blk = img[by0_:by0_ + bh, bx0:bx0 + bw]
        leer = blk.sum(2) == 0
        if leer.any():
            for xx in range(bw):
                sp = blk[:, xx]
                ok_ = ~leer[:, xx]
                if ok_.any():
                    sp[~ok_] = np.array([np.interp(np.nonzero(~ok_)[0], np.nonzero(ok_)[0], sp[ok_, c_]) for c_ in range(3)]).T
        voll[by0_:by0_ + bh, bx0:bx0 + bw] = True
    # Std-UV fuer alle Std-GLB-Punkte gesetzt?
    assert np.isfinite(UVN).all()
    # Nachbesserung 12.11.: Texel bis rand_ausdehnen_px neben JEDER Insel (Gen, Std, Band) = Mittel der Insel-Texel -- die Hell-Faktoren
    # (a)/(b)/(b3) wirken nur in den Inseln, die Raender daneben blieben dunkler und zeigten sich als Naht-Linien (bilinear, Mip-Stufen)
    tidA = raster_uv(UVN * GR, TgN)[0]
    bedeckt = tidA >= 0
    img_r = ausdehnen(img, bedeckt, P_["rand_ausdehnen_px"])
    nah = ~bedeckt & (ausdehnen(bedeckt[..., None].astype(float), bedeckt, P_["rand_ausdehnen_px"])[..., 0] > 0)
    img[nah] = img_r[nah]
    voll |= nah
    info["rand_ausgedehnt_texel"] = int(nah.sum())
    # Ausdehnen (leere Pixel = Mittel der vollen Nachbarn), damit Mip-Stufen nicht schwarz bluten
    hinter = np.median(gen_kl.reshape(-1, 3), 0)
    for _ in range(6):
        acc = np.zeros_like(img)
        cnt = np.zeros((GR, GR))
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            sh = np.roll(np.roll(img * voll[..., None], dy, 0), dx, 1)
            vs = np.roll(np.roll(voll, dy, 0), dx, 1)
            acc += sh
            cnt += vs
        neu = ~voll & (cnt > 0)
        img[neu] = acc[neu] / cnt[neu][:, None]
        voll |= neu
    img[~voll] = hinter
    # ------------------------------------------------------------------ 8. Masken
    nV = len(VN)
    mk = {}
    for nm in ("kopf", "ohr_l", "ohr_r", "hals", "stummel"):
        a = np.zeros(nV, bool)
        src = np.r_[N[nm].astype(bool), np.zeros(max(0, len(V) - len(N[nm])), bool)]      # Schnittpunkte: nicht Kopf/Ohr/...
        a[:len(g_alt)] = src[g_alt]
        mk[nm] = a
    for k in BEINE:
        _kn, gel = bein_knochen(k)
        w_ = WN[:, names.index(gel)]
        if k[0] == "H":
            w_ = w_ + WN[:, names.index(gel.replace("Foot", "Toe0"))]
        mk["pfote_" + k] = (teil == 1) & (w_ >= 0.5)
    r = uv_flaeche(S["UV"], F_alle) / np.maximum(flaeche3(S["P"], F_alle), 1e-12)
    kr = np.zeros(nV, bool)
    kr[T_std[r < 0.02 * np.median(r)].ravel()] = True
    mk["kralle"] = kr
    NS = np.zeros((nV, 3))
    NS[len(g_alt):] = S["N"][rep_s[s_alt]]
    mk["sohle"] = (teil == 1) & (VN[:, 2] < 0.015) & (NS[:, 2] < -0.3) & ~kr
    # Quelle je Punkt
    quelle = np.r_[g_alt, -1 - s_alt]
    out = dict(V=VN, T=TN, T_glb=TgN, glb_punkt=glb_punkt, UV=UVN, teil=teil, teil_T=teil_T, quelle=quelle,
               **mk, info=np.array(json.dumps(info)))
    atlas = dict(gen_skala=UVS, gen_rechteck_px=[0, 0, 880, 880], frei_px=frei, std_skala=s,
                 std_inseln=[dict(quelle_px=b["box"], ziel_px=b["ziel"]) for b in inseln], band_px=band_rects)
    return out, WN, img, atlas


def pfoten_ganz(skp, netz1, aus_netz, aus_gew, aus_png, aus_atlas=None, par_json=None):
    L = pfoten(skp, netz1, aus_netz, aus_gew, aus_png, aus_atlas, par_json)
    out, WN, img, atlas = zusammenbau(L)
    np.savez(aus_netz, **out)
    np.savez(aus_gew, W=WN, namen=np.array(L["names"]))
    Image.fromarray(np.clip(np.round(img), 0, 255).astype(np.uint8), "RGB").save(aus_png)
    if aus_atlas:
        json.dump(atlas, open(aus_atlas, "w"), indent=1)
    log("->", aus_netz, aus_gew, aus_png, aus_atlas)
    return json.loads(str(out["info"]))
