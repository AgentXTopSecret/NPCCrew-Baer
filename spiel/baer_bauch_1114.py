# -*- coding: utf-8 -*-
# Lauf baer-gen-rear-bauch (14.11.2026), Bauer B: Bauch-/Brust-/Innenschenkel-Fell am Klassisch-Baeren, NUR Textur (textures/Body/NCBear.png).
# Kevin 13.11. ~22:45 (woertlich): "beim bauch vom std baeren will ich nur das das fell besser aussieht beim ROAR der rest soll so bleiben okay
# die textur da sieht nur matschig aus nicht wie richtiges fell beim bauch da".
#
# Was es tut (Nachbearbeitung der heutigen 1024er, nichts neu gebacken; Netz/UV/Gewichte/Clips werden nur GELESEN):
#   1. Klassisch-GLB lesen und pruefen (Punktzahl, Indexzahl, UV-Pruefsumme wie Test-Mod dc50d350), Textur 1024x1024 RGB; sonst Abbruch
#      BAUCHFELL_FEHLER (Code 2), nichts geschrieben.
#   2. Maske je Netz-Punkt wie PLAN 3.1 (_arbeit/baer_modell_1114/werkzeug/bauch_maske.py, gleiche Formeln): Bauch / Brust / Innenschenkel,
#      Kopf/Kiefer/Pfoten/Schwanz gesperrt. Zusaetzlich: Inseln mit Head/Jaw/Hand/Foot/Toe/Tail-Anteil > 0,4 ganz gesperrt (bit-gleich,
#      PLAN B1; dazu gehoert die Kehle, PLAN F2) und an Naehten zu solchen Inseln weich auf 0 (4 cm, 3D-Abstand) -> keine Kante.
#   3. Je Texel (Rasterung in UV): 3D-Lage, Normale, Maske, Insel; Rand-Polster (Gutter) bis 8 Texel: Lage/Normale aus dem Dreieck des naechsten
#      Insel-Texels fortgesetzt (die 256er-Verkleinerung mischt das Polster mit ein).
#   4. Wuchsrichtung h in der Flaeche: F = (-0,6, 0, -1) in die Flaeche gelegt (Brust abwaerts, Bauch nach hinten, Innenschenkel ab/hinten).
#      Gemessen: die Strichrichtung des Nachbarfells am Maskenrand liegt im Median 13-19 Grad daneben -> kein eigener Uebergang noetig.
#   5. Fell: Feinanteil des Rueckenfells DERSELBEN Textur (Vorbild-Quadrat in Insel 9, oberer Ruecken) in 3D "getupft": je 3D-Zelle (6 cm)
#      ein Tupf mit Zufalls-Versatz ins Vorbild, Lage im Vorbild aus Wuchsrichtung (laengs) und Querrichtung des Texels, varianztreu gemischt;
#      2x2 Unterabtastung, 11 Proben laengs des Strichs (kurz +-0,25 cm fuer die Straehnen, 40 % lang +-2 cm "gekaemmt", traegt auch bei 256),
#      leicht nachgeschaerft. Alles aus 3D-Lage/Normale gerechnet -> stetig ueber jede UV-Naht. Kein Fremdmaterial: Vorbild = Kevins Baeren-Textur.
#   6. Farbe: Grobanteil der heutigen Textur (Gauss sigma 7 Texel = 2,25 cm, in 3D ueber ein Voxelgitter je Normalen-Richtung -> stetig ueber
#      UV-Naehte) bleibt -> Farbton/Helligkeit wie heute; der Feinanteil (Matsch/Zickzack) wird durch das Fell ersetzt; am Maskenrand
#      varianztreu gemischt (kein matter Saum); Maske 0 -> bit-gleich.
#   7. Selbstpruefung (geaendert nur Maskenbereich + Polster daneben, gesperrte Inseln bit-gleich), PNG wie heute (RGB 8 bit 1024, dieselben
#      Zusatz-Bloecke sRGB/gAMA/cHRM/eXIf/oFFs/pHYs byte-gleich), erst .tmp, dann umbenennen. Ende "BAUCHFELL_OK MD5 <md5>". Fester Samen.
#
# Aufruf: python baer/spiel/baer_bauch_1114.py <NCBear.glb> <NCBear.png> <AUS.png> [--bericht B.json] [--felder F.npz] [--trotzdem]
#   Wieder-Aufsetzen: ist der Bauchbereich schon das neue Fell -> BAUCHFELL_SCHON, Eingang unveraendert nach AUS; weder alt noch neu -> Abbruch.
#   (EIN = geltende Klassisch-Dateien, heute Test-Mod NCBearTest/42/media/models_X/Skinned/NCBear.glb + textures/Body/NCBear.png)
# Statisch gerechnet, nicht gespielt. Reines Python/numpy + PIL. Schreibt nur AUS (und die optionalen Bericht-/Felder-Dateien).
# Schreibschutz: AUS darf kein Eingang sein und nicht unter .../Zomboid/mods/... oder .../steamapps/... liegen.
import hashlib
import io
import json
import os
import struct
import sys
import time

import numpy as np
from PIL import Image

M2U = 0.544                    # glTF-Einheiten je Meter (baer_kern_liegen.py)
R = 1024
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8, 5120: np.int8, 5122: np.int16}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
# Eingangs-Netz wie Test-Mod NCBear.glb dc50d350 (baer-gross fix1 + Liegen). Aendert ein spaeterer Lauf Netz oder UV, muss die Maske
# neu gerechnet werden -> Abbruch statt still falscher Maske (Clips duerfen sich aendern, sie werden nicht gelesen).
NETZ_PUNKTE = 11914
NETZ_INDIZES = 59430
UV_MD5 = "5e392a662c1de68fbd6a05127933cab6"      # MD5 der TEXCOORD_0-Bytes
# Fingerabdruck (MD5 der RGB-Bytes aller Texel mit Maske > 0, Standard-Einstellungen): alte Textur 5a841f0c / Ergebnis dieses Laufs 3493a5e6
BAUCH_ALT_MD5 = "ce05d3788c5c42efc9410b4eb2f8fd09"
BAUCH_NEU_MD5 = "a233e1beb5b2eb7718ecef843c3bad19"
SPERR = ("Bip01_Head", "Bip01_Jaw", "Bip01_L_Hand", "Bip01_R_Hand", "Bip01_L_Foot", "Bip01_R_Foot", "Bip01_L_Toe0", "Bip01_R_Toe0",
         "Bip01_Tail")

P_STD = dict(
    seed=1114,
    F="-0.6,0,-1",            # Wuchsrichtung (tier: x vorn, y links, z oben), PLAN 3.2
    sperr_naht_cm=4.0,        # weicher Abfall der Maske zu gesperrten Inseln
    polster=8,                # Rand-Polster in Texeln (PLAN 3.3)
    lf_sigma=7.0,             # Grobanteil (Texel): darunter bleibt die heutige Textur, darueber kommt das Fell
    tz_cm=6.0,                # Tupf-Zelle
    tsig=0.3,                 # Tupf-Fenster sigma (Anteil der Zelle)
    tskala=1.2,               # Vorbild-Massstab (1 = gleiche cm wie am Ruecken; 1,2 = Straehnen etwas feiner)
    unter=2,                  # Unterabtastung je Texel (2x2)
    lk=11, ll_cm=0.25,        # Proben laengs des Strichs (Raster bis +-max(ll, ll2)), kurzes Gauss-Fenster +-ll (Straehnen)
    ll2_cm=2.0, mix2=0.4,     # langes Fenster +-ll2 (gekaemmte Buendel, tragen auch bei 256) und sein Anteil
    scharf=0.6,               # Nachschaerfen (4-Nachbarn, nur innerhalb des Maskenbereichs samt Polster)
    gain=1.4,                 # Staerke des Fells (Fs Bauch = Ruecken 0,158)
    lf3d=1,                   # Grobfarbe in 3D (stetig ueber UV-Naehte) statt je Insel in UV
    lf_laeng_cm=0.0,          # Grobfarbe zusaetzlich laengs des Strichs mitteln (+-cm)
)


def fehler(msg):
    print("BAUCHFELL_FEHLER", msg)
    sys.exit(2)


# ------------------------------------------------------------------ GLB lesen (wie baer_kern_liegen.py, eigenstaendig)
def lade_glb(pfad):
    b = open(pfad, "rb").read()
    if b[:4] != b"glTF":
        fehler("kein GLB: %s" % pfad)
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    return J, b[o + 8:o + 8 + bl]


def acc_arr(J, B, i):
    a = J["accessors"][i]
    v = J["bufferViews"][a["bufferView"]]
    k = NC[a["type"]]
    dt = np.dtype(CT[a["componentType"]])
    s = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    st = v.get("byteStride", k * dt.itemsize)
    if st == k * dt.itemsize:
        raw = B[s:s + a["count"] * k * dt.itemsize]
    else:
        raw = b"".join(B[s + j * st: s + j * st + k * dt.itemsize] for j in range(a["count"]))
    return np.frombuffer(raw, dtype=dt).reshape(a["count"], k)


def g2t(P):
    P = np.asarray(P, float)
    return P[..., [2, 0, 1]] / M2U


def q_mat(q):
    x, y, z, w = (float(v) for v in q)
    n = (x * x + y * y + z * z + w * w) ** 0.5
    x, y, z, w = x / n, y / n, z / n, w / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


class Netz:
    """Klassisch-Netz in Ruhe, Rahmen tier (Meter): P, N, UV, Dreiecke, Gewichtsmatrix je Knoten-Name."""

    def __init__(self, pfad):
        J, B = lade_glb(pfad)
        self.J = J
        pr = J["meshes"][0]["primitives"][0]
        at = pr["attributes"]
        self.uv_raw = acc_arr(J, B, at["TEXCOORD_0"])
        self.UV = self.uv_raw.astype(float)
        self.P = g2t(acc_arr(J, B, at["POSITION"]))
        N = g2t(acc_arr(J, B, at["NORMAL"]))
        self.N = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
        self.F = acc_arr(J, B, pr["indices"]).astype(np.int64).reshape(-1, 3)
        nodes = J["nodes"]
        self.name = [n.get("name", "?") for n in nodes]
        self.ix = {n: i for i, n in enumerate(self.name)}
        par = [-1] * len(nodes)
        for i, n in enumerate(nodes):
            for c in n.get("children", []):
                par[c] = i
        W = [None] * len(nodes)

        def welt(i):
            if W[i] is None:
                L = np.eye(4)
                L[:3, :3] = q_mat(nodes[i].get("rotation", (0, 0, 0, 1))) * np.array(nodes[i].get("scale", (1, 1, 1)))[None, :]
                L[:3, 3] = nodes[i].get("translation", (0, 0, 0))
                W[i] = L if par[i] < 0 else welt(par[i]) @ L
            return W[i]
        self.W0 = [welt(i) for i in range(len(nodes))]
        joints = list(J["skins"][0]["joints"])
        JN = acc_arr(J, B, at["JOINTS_0"]).astype(int)
        WT = acc_arr(J, B, at["WEIGHTS_0"]).astype(float)
        G = np.zeros((len(self.P), len(nodes)))
        jn = np.array(joints)
        for k in range(4):
            np.add.at(G, (np.arange(len(self.P)), jn[JN[:, k]]), WT[:, k])
        self.G = G
        self.n_idx = int(J["accessors"][pr["indices"]]["count"])

    def w(self, *nm):
        return self.G[:, [self.ix[x] for x in nm]].sum(1)

    def gelenk(self, n):
        return g2t(self.W0[self.ix[n]][:3, 3])


def ramp(x, a, b):
    return np.clip((x - a) / (b - a), 0, 1)


def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ Maske je Punkt (PLAN 3.1 = werkzeug/bauch_maske.py)
def maske_punkte(nz):
    P, N = nz.P, nz.N
    w_rumpf = nz.w("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1")
    w_brust = nz.w("Bip01_Spine1", "Bip01_L_Clavicle", "Bip01_R_Clavicle", "Bip01_Neck")
    w_bein = nz.w("Bip01_L_Thigh", "Bip01_R_Thigh", "Bip01_L_Calf", "Bip01_R_Calf")
    w_sperr = nz.w(*SPERR)
    z_huefte = nz.gelenk("Bip01_L_Thigh")[2]
    z_schulter = nz.gelenk("Bip01_L_UpperArm")[2]
    bauch = ramp(w_rumpf, 0.3, 0.7) * ramp(-N[:, 2], 0.25, 0.55)
    brust = ramp(w_brust, 0.3, 0.7) * ramp(-N[:, 2], 0.10, 0.40) * ramp(N[:, 0], -0.2, 0.2) * ramp(z_schulter - P[:, 2], -0.02, 0.06)
    innen = ramp(w_bein + 0.5 * nz.w("Bip01_Pelvis"), 0.4, 0.8) * ramp(-np.sign(P[:, 1]) * N[:, 1], 0.25, 0.55) * ramp(z_huefte + 0.05 - P[:, 2], 0.0, 0.08)
    m = np.maximum(np.maximum(bauch, brust), innen) * (1 - ramp(w_sperr, 0.15, 0.4))
    return m, w_sperr, dict(bauch=bauch, brust=brust, innen=innen)


def inseln(nz):
    """UV-Inseln: Dreiecke ueber gemeinsame Punkt-Indizes verbunden (wie werkzeug/uv_inseln.py). -> Insel je Punkt (0..n-1, nach Groesse)."""
    n = len(nz.P)
    par = np.arange(n)

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for t in nz.F:
        r0 = find(t[0])
        for k in (1, 2):
            rk = find(t[k])
            if rk != r0:
                par[rk] = r0
    root = np.array([find(i) for i in range(n)])
    u, inv, cnt = np.unique(root, return_inverse=True, return_counts=True)
    ordn = np.argsort(-cnt, kind="stable")
    rang = np.empty_like(ordn)
    rang[ordn] = np.arange(len(ordn))
    return rang[inv.ravel()]


# ------------------------------------------------------------------ Rasterung in UV
def rastern(nz):
    """Je Texel (Mitte innerhalb eines Dreiecks): Dreieck-Index (-1 = Polster) und Baryzentrik. Bildzeile = v * 1024 (wie bauch_maske.py;
    die Textur liegt so, glTF-UV oben links)."""
    uvp = nz.UV * R
    TRI = -np.ones((R, R), np.int64)
    BAR = np.zeros((R, R, 3))
    for ti, t in enumerate(nz.F):
        a, b, c = uvp[t]
        x0, x1 = int(max(0, np.floor(min(a[0], b[0], c[0]) - 0.5))), int(min(R - 1, np.ceil(max(a[0], b[0], c[0]))))
        y0, y1 = int(max(0, np.floor(min(a[1], b[1], c[1]) - 0.5))), int(min(R - 1, np.ceil(max(a[1], b[1], c[1]))))
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if x1 < x0 or y1 < y0 or abs(d) < 1e-12:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
        l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-9) & (l2 >= -1e-9) & (l3 >= -1e-9)
        if not ins.any():
            continue
        sl = (slice(y0, y1 + 1), slice(x0, x1 + 1))
        TRI[sl] = np.where(ins, ti, TRI[sl])
        BAR[sl] = np.where(ins[..., None], np.stack((l1, l2, l3), -1), BAR[sl])
    return TRI, BAR


def baryz(nz, ti, xs, ys):
    """Baryzentrik der Punkte (xs, ys) (Texel-Mitten) bezueglich Dreieck ti (auch ausserhalb -> fortgesetzt)."""
    uvp = nz.UV * R
    t = nz.F[ti]
    a, b, c = uvp[t[:, 0]], uvp[t[:, 1]], uvp[t[:, 2]]
    d = (b[:, 1] - c[:, 1]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 1] - c[:, 1])
    d = np.where(np.abs(d) < 1e-12, 1e-12, d)
    l1 = ((b[:, 1] - c[:, 1]) * (xs - c[:, 0]) + (c[:, 0] - b[:, 0]) * (ys - c[:, 1])) / d
    l2 = ((c[:, 1] - a[:, 1]) * (xs - c[:, 0]) + (a[:, 0] - c[:, 0]) * (ys - c[:, 1])) / d
    return np.stack((l1, l2, 1 - l1 - l2), -1)


def polster(TRI, weite):
    """Naechster Insel-Texel je Polster-Texel (Ring fuer Ring, 8 Nachbarn, bis 'weite' Texel): Index (y, x) oder -1."""
    NY = np.where(TRI >= 0, np.arange(R)[:, None], -1).astype(np.int64)
    NX = np.where(TRI >= 0, np.arange(R)[None, :], -1).astype(np.int64)
    RING = np.where(TRI >= 0, 0, -1)
    for r in range(1, weite + 1):
        neu_y, neu_x = NY.copy(), NX.copy()
        best = np.full((R, R), 1e9)
        frei = NY < 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                sy = np.roll(NY, (dy, dx), (0, 1))
                sx = np.roll(NX, (dy, dx), (0, 1))
                yy, xx = np.arange(R)[:, None], np.arange(R)[None, :]
                dist = (sy - yy) ** 2 + (sx - xx) ** 2
                ok = frei & (sy >= 0) & (dist <= 2 * (r + 1) ** 2)       # kein Umlauf ueber den Bildrand
                bes = ok & (dist < best)
                best = np.where(bes, dist, best)
                neu_y = np.where(bes, sy, neu_y)
                neu_x = np.where(bes, sx, neu_x)
        RING = np.where((NY < 0) & (neu_y >= 0), r, RING)
        NY, NX = neu_y, neu_x
    return NY, NX, RING


# ------------------------------------------------------------------ Felder je Texel
def felder(nz, opt, log=print):
    t0 = time.time()
    m_p, w_sperr, reg = maske_punkte(nz)
    isl_p = inseln(nz)
    n_isl = isl_p.max() + 1
    cnt = np.bincount(isl_p, minlength=n_isl)
    anteil = np.bincount(isl_p, weights=w_sperr, minlength=n_isl) / np.maximum(cnt, 1)
    gesperrt = anteil > 0.4
    # Naht zu gesperrten Inseln: Punkte gesperrter Inseln, deren Lage auch ein Punkt einer freien Insel hat
    key = np.round(nz.P * 1e5).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.ravel()
    frei_lage = np.zeros(inv.max() + 1, bool)
    frei_lage[inv[~gesperrt[isl_p]]] = True
    naht = gesperrt[isl_p] & frei_lage[inv]
    m_roh = m_p.copy()
    m_p = np.where(gesperrt[isl_p], 0.0, m_p)
    r_naht = float(opt["sperr_naht_cm"]) / 100.0
    if naht.any():
        PN = nz.P[naht]
        sel = np.where(m_p > 0)[0]
        d = np.full(len(sel), 1e9)
        for s0 in range(0, len(sel), 2000):
            ss = sel[s0:s0 + 2000]
            d[s0:s0 + 2000] = np.sqrt(((nz.P[ss][:, None, :] - PN[None]) ** 2).sum(-1)).min(1)
        m_p[sel] *= sst(0.0, r_naht, d)
    log("Maske Punkte: >0.5 %d (roh %d), Inseln %d, gesperrt %d (Anteil Kopf/Kiefer/Pfote/Schwanz > 0,4), Naht-Punkte %d" % (
        (m_p > 0.5).sum(), (m_roh > 0.5).sum(), n_isl, gesperrt.sum(), naht.sum()))
    TRI, BAR = rastern(nz)
    insel = TRI >= 0
    NY, NX, RING = polster(TRI, int(opt["polster"]))
    pol = (~insel) & (NY >= 0)
    # Dreieck je Texel: Insel-Texel eigenes, Polster-Texel das des naechsten Insel-Texels (Baryzentrik fortgesetzt)
    T_eff = np.where(insel, TRI, -1)
    T_eff[pol] = TRI[NY[pol], NX[pol]]
    B_eff = BAR.copy()
    yy, xx = np.nonzero(pol)
    B_eff[pol] = baryz(nz, T_eff[pol], xx + 0.5, yy + 0.5)
    gilt = T_eff >= 0
    tri = nz.F[T_eff[gilt]]
    L = B_eff[gilt]

    def ip(arr):
        return np.einsum("nk,nk...->n...", L, arr[tri])
    TP = np.zeros((R, R, 3)); TN = np.zeros((R, R, 3)); TM = np.zeros((R, R)); TS = np.zeros((R, R))
    TP[gilt] = ip(nz.P)
    nn = ip(nz.N)
    TN[gilt] = nn / np.maximum(np.linalg.norm(nn, axis=1, keepdims=True), 1e-9)
    TM[gilt] = np.clip(ip(m_p), 0, 1)
    TS[gilt] = ip(w_sperr)
    # Polster: Maske des naechsten Insel-Texels (nicht fortgesetzt), Insel-Nummer ebenso
    TI = -np.ones((R, R), np.int64)
    TI[insel] = isl_p[nz.F[TRI[insel], 0]]
    TI[pol] = TI[NY[pol], NX[pol]]
    # Polster: Maske = kleinerer Wert aus naechstem Insel-Texel und fortgesetzter Baryzentrik (so bleibt ein Rand-Texel, den eine
    # tolerantere Rasterung schon zur Insel zaehlt, bei Maske 0 unveraendert)
    TM[pol] = np.minimum(TM[NY[pol], NX[pol]], TM[pol])
    # Jacobi UV->3D je Dreieck (Unterabtastung im Texel, Vorbild-Massstab)
    uvp = nz.UV * R
    a, b, c = uvp[nz.F[:, 0]], uvp[nz.F[:, 1]], uvp[nz.F[:, 2]]
    PA, PB, PC = nz.P[nz.F[:, 0]], nz.P[nz.F[:, 1]], nz.P[nz.F[:, 2]]
    Duv = np.stack((b - a, c - a), -1)                       # 2x2 (Spalten)
    DP = np.stack((PB - PA, PC - PA), -1)                    # 3x2
    det = Duv[:, 0, 0] * Duv[:, 1, 1] - Duv[:, 0, 1] * Duv[:, 1, 0]
    det = np.where(np.abs(det) < 1e-12, 1e-12, det)
    inv2 = np.stack((np.stack((Duv[:, 1, 1], -Duv[:, 0, 1]), -1), np.stack((-Duv[:, 1, 0], Duv[:, 0, 0]), -1)), 1) / det[:, None, None]
    JAC = np.einsum("tij,tjk->tik", DP, inv2)                # 3x2: dP/du (Spalte 0, Bildspalte x), dP/dv (Spalte 1, Bildzeile y)
    log("Felder %.1fs: Insel-Texel %d, Polster-Texel %d, Maske>0 %d, Maske>0,5 %d" % (time.time() - t0, insel.sum(), pol.sum(),
        (TM > 0).sum(), (TM > 0.5).sum()))
    return dict(TRI=TRI, T_eff=T_eff, insel=insel, pol=pol, RING=RING, NY=NY, NX=NX, TP=TP, TN=TN, TM=TM, TS=TS, TI=TI,
                gesperrt=gesperrt, anteil=anteil, JAC=JAC, m_p=m_p, isl_p=isl_p)


# ------------------------------------------------------------------ Wuchsrichtung
def wuchsrichtung(N, F):
    """F in die Flaeche gelegt; wo die Normale fast parallel zu F steht (Flaeche schaut nach hinten-unten), weich auf 'nach hinten'
    (wie haar_tangente in baer_textur_gross.py)."""
    h = F[None] - (N @ F)[:, None] * N
    lh = np.linalg.norm(h, axis=1)
    hinten = np.array((-1.0, 0.0, 0.0))
    dh = hinten[None] - (N @ hinten)[:, None] * N
    b = sst(0.15, 0.45, lh / np.linalg.norm(F))
    h = b[:, None] * h / np.maximum(lh, 1e-9)[:, None] + (1 - b)[:, None] * dh / np.maximum(np.linalg.norm(dh, axis=1, keepdims=True), 1e-9)
    return h / np.maximum(np.linalg.norm(h, axis=1, keepdims=True), 1e-9)


# ------------------------------------------------------------------ Farbe
def gauss2(img, s):
    """Trennbarer Gauss (Rand: Null), img (h, w) oder (h, w, k)."""
    r = int(3 * s)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / s) ** 2)
    k /= k.sum()
    out = np.asarray(img, float)
    for ax in (0, 1):
        out = np.apply_along_axis(lambda v: np.convolve(v, k, mode="same"), ax, out)
    return out


def grobanteil(old, f, sigma, inseln_ids):
    """Grobfarbe der alten Textur je Texel: normierter Gauss nur ueber Insel-Texel DERSELBEN Insel (Polster-Texel: Insel des naechsten
    Insel-Texels), damit keine Nachbarinsel hineinblutet."""
    LF = old.copy()
    r = int(3 * sigma) + 2
    for i in inseln_ids:
        ziel = f["TI"] == i
        ys, xs = np.nonzero(ziel)
        y0, y1, x0, x1 = max(0, ys.min() - r), min(R, ys.max() + r + 1), max(0, xs.min() - r), min(R, xs.max() + r + 1)
        sl = (slice(y0, y1), slice(x0, x1))
        w = (f["insel"][sl] & (f["TI"][sl] == i)).astype(float)
        num = gauss2(old[sl] * w[..., None], sigma)
        den = gauss2(w, sigma)
        z = ziel[sl]
        LF[sl][z] = num[z] / np.maximum(den[z], 1e-6)[:, None]
    return LF


def lum(c):
    return c @ np.array((0.299, 0.587, 0.114))


def grob3d(old, f, sel, sigma_m, h=None, laeng_m=0.0, log=print):
    """Grobfarbe der alten Textur in 3D (stetig ueber UV-Naehte): alle Insel-Texel werden mit ihrer 3D-Lage in ein Voxelgitter (Kante
    sigma/2) eingetragen, getrennt nach 6 Normalen-Richtungen (Gewicht max(0, n.e)^2, damit Arm-Innenseite und Brust oder die zwei
    Seiten einer Falte nicht ineinanderlaufen), je Richtung 3D-Gauss (sigma), und an den Ziel-Texeln (sel) mit deren Normalen-Gewichten
    gelesen. Mit h und laeng_m: zusaetzlich laengs der Wuchsrichtung gemittelt (7 Proben, Gauss +-laeng) -> Farbstreifen folgen dem Strich."""
    t0 = time.time()
    v = sigma_m / 2.0
    P_s, N_s = f["TP"][sel], f["TN"][sel]
    lo = P_s.min(0) - 4 * sigma_m
    hi = P_s.max(0) + 4 * sigma_m
    quelle = f["insel"] & np.all(f["TP"] >= lo, -1) & np.all(f["TP"] <= hi, -1)
    Pq, Nq, Cq = f["TP"][quelle], f["TN"][quelle], old[quelle]
    n = np.ceil((hi - lo) / v).astype(int) + 2
    E6 = np.array(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)), float)

    def ecken(P):
        g = (P - lo) / v
        i = np.clip(np.floor(g).astype(np.int64), 0, n - 2)
        t = np.clip(g - i, 0, 1)
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = (t[:, 0] if dx else 1 - t[:, 0]) * (t[:, 1] if dy else 1 - t[:, 1]) * (t[:, 2] if dz else 1 - t[:, 2])
                    yield np.ravel_multi_index((i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz), n), w
    r = int(np.ceil(3 * 2.0))
    kern = np.exp(-0.5 * (np.arange(-r, r + 1) / 2.0) ** 2)
    kern /= kern.sum()

    def blur(G):
        for ax in range(3):
            out = np.zeros_like(G)
            for k, kv in zip(range(-r, r + 1), kern):
                out += kv * np.roll(G, k, ax)
            G = out
        return G
    wq = np.maximum(Nq @ E6.T, 0) ** 2
    ws = np.maximum(N_s @ E6.T, 0) ** 2
    num = np.zeros((len(P_s), 3))
    den = np.zeros(len(P_s))
    if h is not None and laeng_m > 0:
        sl_ = np.linspace(-laeng_m, laeng_m, 7)
        wl_ = np.exp(-0.5 * (sl_ / (laeng_m / 1.5)) ** 2)
        wl_ /= wl_.sum()
    else:
        sl_, wl_ = np.zeros(1), np.ones(1)
    for b in range(6):
        if wq[:, b].max() <= 0 or ws[:, b].max() <= 0:
            continue
        G = np.zeros((4, n.prod()))
        for idx, w in ecken(Pq):
            ww = w * wq[:, b]
            for c in range(3):
                G[c] += np.bincount(idx, weights=ww * Cq[:, c], minlength=n.prod())
            G[3] += np.bincount(idx, weights=ww, minlength=n.prod())
        G = np.stack([blur(G[c].reshape(n)) for c in range(4)]).reshape(4, -1)
        for sv, wv in zip(sl_, wl_):
            for idx, w in ecken(P_s + sv * h if h is not None else P_s):
                ww = w * ws[:, b] * wv
                num += (ww[:, None] * G[:3, idx].T)
                den += ww * G[3, idx]
    LF = num / np.maximum(den, 1e-12)[:, None]
    log("Grobfarbe 3D %.1fs (Voxel %.2f cm, sigma %.2f cm, Quell-Texel %d, Gitter %s)" % (time.time() - t0, 100 * v, 100 * sigma_m, len(Pq),
                                                                                          n.tolist()))
    return LF


# ------------------------------------------------------------------ Fell-Vorbild: Rueckenfell derselben Textur, in 3D getupft
VORBILD = (552, 260, 130)      # Zeile, Spalte, Kante: Quadrat ganz in Insel 9 (oberer Ruecken/Flanke links, nie in der Maske)


def hash01(ix, iy, iz, saat, k):
    """Gleichverteilte Zufallszahl 0..1 je ganzzahliger 3D-Zelle (fest, plattformgleich)."""
    h = (ix.astype(np.uint64) * np.uint64(73856093)) ^ (iy.astype(np.uint64) * np.uint64(19349663)) ^ \
        (iz.astype(np.uint64) * np.uint64(83492791)) ^ np.uint64((saat * 2654435761 + k * 40503) % (1 << 32))
    h &= np.uint64(0xFFFFFFFF)
    h ^= h >> np.uint64(15)
    h = (h * np.uint64(0x2C1B3C6D)) & np.uint64(0xFFFFFFFF)
    h ^= h >> np.uint64(12)
    h = (h * np.uint64(0x297A2D39)) & np.uint64(0xFFFFFFFF)
    h ^= h >> np.uint64(15)
    return h.astype(np.float64) / 4294967296.0


def vorbild(old, f, sigma):
    """Feinanteil des Rueckenfells: E = alt / Grob - 1 je Kanal (Grob = normierter Gauss in Insel 9), Strichrichtung (Struktur-Tensor,
    Vorzeichen: in 3D nach hinten/unten = Wuchsrichtung) und Texel je Meter laengs/quer."""
    y0, x0, s = VORBILD
    isl = f["TI"][y0 + s // 2, x0 + s // 2]
    LF = grobanteil(old, f, sigma, [isl])
    E = old[y0:y0 + s, x0:x0 + s] / np.maximum(LF[y0:y0 + s, x0:x0 + s], 1e-3) - 1.0
    L = lum(old[y0:y0 + s, x0:x0 + s])
    gy, gx = np.gradient(L)
    jxx, jyy, jxy = (gx * gx).mean(), (gy * gy).mean(), (gx * gy).mean()
    th = 0.5 * np.arctan2(2 * jxy, jxx - jyy)
    es = np.array((-np.sin(th), np.cos(th)))                       # Strich (x = Spalte, y = Zeile)
    Jall = f["JAC"][f["TRI"][y0:y0 + s, x0:x0 + s].ravel()]          # n x 3 x 2
    d3 = Jall.mean(0) @ es
    if d3 @ np.array((-0.82, 0.0, -0.57)) < 0:                      # Deckhaar am Rumpf (haarrichtung, baer_textur_gross.py:557)
        es = -es
    ep = np.array((-es[1], es[0]))
    px_m = 1.0 / np.linalg.norm(Jall, axis=1).mean(0)               # Texel je Meter (Spalte, Zeile)
    return E - E.mean((0, 1)), es, ep, px_m


def tupfen(P, N, h, E, es, ep, px_m, opt, log=print):
    """Rueckenfell in 3D getupft ("Texture Bombing"): je 3D-Zelle (Kante tz) ein Tupf-Mittelpunkt mit Zufallslage, Zufalls-Versatz ins
    Vorbild und Spiegelung quer zum Strich; je Punkt die 27 Nachbar-Tupfen, Gewicht Gauss(Abstand), Koordinate im Vorbild aus der
    EIGENEN Wuchsrichtung (laengs) und Querrichtung des Punkts -> stetig ueber UV-Naehte. Mischung varianztreu: S / sqrt(Summe w^2)."""
    t0 = time.time()
    cm = 0.01
    z = float(opt["tz_cm"]) * cm
    sig = float(opt["tsig"]) * z
    saat = int(opt["seed"])
    s = E.shape[0]
    px_m = px_m * float(opt.get("tskala", 1.0))
    rand = 3 * sig * max(px_m) * 1.15 + 2
    q = np.cross(N, h)
    q /= np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-9)
    out = np.zeros((len(P), 3))
    blk = 40000
    for b0 in range(0, len(P), blk):
        sl = slice(b0, b0 + blk)
        Pb, Hb, Qb = P[sl], h[sl], q[sl]
        g = np.floor(Pb / z).astype(np.int64)
        S = np.zeros((len(Pb), 3))
        W2 = np.zeros(len(Pb))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dzz in (-1, 0, 1):
                    ix, iy, iz = g[:, 0] + dx, g[:, 1] + dy, g[:, 2] + dzz
                    C = np.stack(((ix + hash01(ix, iy, iz, saat, 1)) * z, (iy + hash01(ix, iy, iz, saat, 2)) * z,
                                  (iz + hash01(ix, iy, iz, saat, 3)) * z), 1)
                    d = Pb - C
                    w = np.exp(-0.5 * (d * d).sum(1) / sig ** 2)
                    a = np.einsum("ij,ij->i", d, Qb)            # quer (m)
                    b = np.einsum("ij,ij->i", d, Hb)            # laengs (m)
                    sp = np.where(hash01(ix, iy, iz, saat, 5) < 0.5, -1.0, 1.0)     # Spiegelung quer zum Strich
                    bb = b
                    aa = a * sp
                    ox = rand + hash01(ix, iy, iz, saat, 6) * (s - 1 - 2 * rand)
                    oy = rand + hash01(ix, iy, iz, saat, 7) * (s - 1 - 2 * rand)
                    X = np.clip(ox + (bb * es[0] + aa * ep[0]) * px_m[0], 0, s - 1.001)
                    Y = np.clip(oy + (bb * es[1] + aa * ep[1]) * px_m[1], 0, s - 1.001)
                    x0 = np.floor(X).astype(int)
                    y0 = np.floor(Y).astype(int)
                    fx, fy = (X - x0)[:, None], (Y - y0)[:, None]
                    v = (E[y0, x0] * (1 - fx) * (1 - fy) + E[y0, x0 + 1] * fx * (1 - fy) + E[y0 + 1, x0] * (1 - fx) * fy +
                         E[y0 + 1, x0 + 1] * fx * fy)
                    S += w[:, None] * v
                    W2 += w * w
        out[sl] = S / np.sqrt(np.maximum(W2, 1e-12))[:, None]
    log("Tupfen %.1fs fuer %d Punkte" % (time.time() - t0, len(P)))
    return out


# ------------------------------------------------------------------ Fell rechnen
def fell(nz, old, f, opt, log=print):
    """Neue Textur (float 0..1) aus alter Textur und Feldern; nur Texel mit Maske > 0 (Insel + Polster) werden neu gerechnet."""
    sel = f["TM"] > 0
    P, N = f["TP"][sel], f["TN"][sel]
    J = f["JAC"][f["T_eff"][sel]]
    Fv = np.array([float(x) for x in str(opt["F"]).split(",")])
    h = wuchsrichtung(N, Fv)
    E, es, ep, pxm = vorbild(old, f, float(opt["lf_sigma"]))
    log("Vorbild: Quadrat Zeile %d Spalte %d Kante %d, Strich %s, Texel/cm %s, Feinanteil-Std %s" % (
        VORBILD[0], VORBILD[1], VORBILD[2], es.round(3).tolist(), (pxm / 100).round(2).tolist(), E.std((0, 1)).round(3).tolist()))
    uo = int(opt["unter"])
    offs = [((i + 0.5) / uo - 0.5, (j + 0.5) / uo - 0.5) for j in range(uo) for i in range(uo)]
    # Proben laengs des Strichs auf einem gemeinsamen Raster bis +-ll2; zwei Gauss-Gewichte: kurz (ll, Straehnen) und lang (ll2, gekaemmte
    # Buendel, die auch in der 256er-Verkleinerung eine Richtung zeigen); D = (1 - mix2) kurz + mix2 lang
    lk, ll, ll2, mix2 = int(opt["lk"]), float(opt["ll_cm"]) * 0.01, float(opt["ll2_cm"]) * 0.01, float(opt["mix2"])
    ss = np.linspace(-max(ll, ll2), max(ll, ll2), lk) if lk > 1 else np.zeros(1)
    w1 = np.exp(-0.5 * (ss / max(ll / 1.5, 1e-9)) ** 2)
    w2 = np.exp(-0.5 * (ss / max(ll2 / 1.5, 1e-9)) ** 2)
    ws = (1 - mix2) * w1 / w1.sum() + mix2 * w2 / w2.sum()
    t0 = time.time()
    D = np.zeros((len(P), 3))
    for of in offs:
        Pof = P + np.einsum("nij,j->ni", J, np.array(of))
        for sv, wv in zip(ss, ws):
            if wv > 1e-4:
                D += wv * tupfen(Pof + sv * h, N, h, E, es, ep, pxm, opt, log=lambda *a: None)
    D /= len(offs)
    sch = float(opt["scharf"])
    if sch > 0:
        DI = np.zeros((R, R, 3))
        DI[sel] = D
        acc = np.zeros_like(DI)
        for ax, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
            ok = np.roll(sel, sh, ax) & sel
            acc += np.where(ok[..., None], np.roll(DI, sh, ax), DI)
        D = (DI + sch * (DI - acc / 4))[sel]
    log("Fell %.1fs: %d Texel x %d Unterproben x %d laengs" % (time.time() - t0, len(P), len(offs), len(ss)))
    if str(opt["lf3d"]) == "1":
        tx = np.median(np.linalg.norm(f["JAC"][f["TRI"][f["insel"] & (f["TM"] > 0.5)]], axis=1))     # Meter je Texel im Maskenbereich
        LF = grob3d(old, f, sel, float(opt["lf_sigma"]) * tx, h=h, laeng_m=float(opt["lf_laeng_cm"]) * 0.01, log=log)
    else:
        LF = grobanteil(old, f, float(opt["lf_sigma"]), np.unique(f["TI"][sel]))[sel]
    m = f["TM"][sel][:, None]
    Dalt = old[sel] / np.maximum(LF, 1e-3) - 1.0
    Dm = ((1 - m) * Dalt + m * float(opt["gain"]) * D) / np.sqrt((1 - m) ** 2 + m ** 2)
    neu = old.copy()
    neu[sel] = np.clip(LF * (1.0 + Dm), 0.0, 1.0)
    return neu, sel


# ------------------------------------------------------------------ PNG wie heute
def png_chunks(b):
    out = []
    i = 8
    while i < len(b):
        n = struct.unpack(">I", b[i:i + 4])[0]
        out.append((b[i + 4:i + 8], b[i:i + 12 + n]))
        i += 12 + n
    return out


def png_wie(alt_bytes, rgb8):
    """PNG aus rgb8 (H, W, 3 uint8), mit den Zusatz-Bloecken der alten Datei (alles zwischen IHDR und dem ersten IDAT, byte-gleich)."""
    bio = io.BytesIO()
    Image.fromarray(rgb8, "RGB").save(bio, format="PNG", compress_level=6)
    neu = png_chunks(bio.getvalue())
    alt = png_chunks(alt_bytes)
    zus = []
    for t, raw in alt[1:]:
        if t == b"IDAT":
            break
        zus.append(raw)
    ihdr = [raw for t, raw in neu if t == b"IHDR"]
    rest = [raw for t, raw in neu if t in (b"IDAT", b"IEND")]
    if len(ihdr) != 1 or ihdr[0][8:8 + 13] != alt[0][1][8:8 + 13]:
        fehler("IHDR weicht ab (Groesse/Format)")
    return b"\x89PNG\r\n\x1a\n" + ihdr[0] + b"".join(zus) + b"".join(rest)


def schreibschutz(aus, eingaenge):
    a = os.path.normcase(os.path.realpath(aus)).replace("\\", "/")
    for e in eingaenge:
        if a == os.path.normcase(os.path.realpath(e)).replace("\\", "/"):
            fehler("AUS ist ein Eingang: %s" % aus)
    al = a.lower()
    if "/zomboid/mods/" in al or "/steamapps/" in al:
        fehler("AUS liegt in einer Mod oder im Spiel: %s" % aus)


def main(argv):
    opt = dict(P_STD)
    bericht = felder_aus = None
    trotzdem = False
    i = 0
    rest = []
    while i < len(argv):
        if argv[i] == "--bericht":
            bericht = argv[i + 1]
            i += 2
        elif argv[i] == "--felder":
            felder_aus = argv[i + 1]
            i += 2
        elif argv[i] == "--trotzdem":
            trotzdem = True
            i += 1
        else:
            rest.append(argv[i])
            i += 1
    pos = [a for a in rest if "=" not in a]
    for a in rest:
        if "=" in a:
            k, v = a.split("=", 1)
            if k not in opt:
                fehler("unbekannte Einstellung %s" % k)
            opt[k] = v
    if len(pos) != 3:
        print(__doc__ if __doc__ else "Aufruf: python baer_bauch_1114.py NCBear.glb NCBear.png AUS.png [--bericht B.json] [--felder F.npz]")
        fehler("Aufruf: GLB TEXTUR AUS")
    glb, texp, aus = pos
    schreibschutz(aus, (glb, texp))
    for p in (bericht, felder_aus):
        if p:
            schreibschutz(p, (glb, texp))
    t0 = time.time()
    nz = Netz(glb)
    uvm = hashlib.md5(nz.uv_raw.tobytes()).hexdigest()
    if len(nz.P) != NETZ_PUNKTE or nz.n_idx != NETZ_INDIZES or uvm != UV_MD5:
        fehler("Netz/UV anders als dc50d350 (Punkte %d/%d, Indizes %d/%d, UV-MD5 %s/%s) -> Maske neu rechnen" % (
            len(nz.P), NETZ_PUNKTE, nz.n_idx, NETZ_INDIZES, uvm, UV_MD5))
    alt_bytes = open(texp, "rb").read()
    im = Image.open(io.BytesIO(alt_bytes))
    if im.size != (R, R) or im.mode != "RGB":
        fehler("Textur nicht 1024x1024 RGB: %s %s" % (im.size, im.mode))
    old8 = np.asarray(im.convert("RGB")).copy()
    old = old8.astype(np.float64) / 255.0
    print("Eingang: GLB %s (MD5 %s), Textur %s (MD5 %s)" % (glb, hashlib.md5(open(glb, "rb").read()).hexdigest(), texp,
                                                         hashlib.md5(alt_bytes).hexdigest()))
    f = felder(nz, opt)
    # Wieder-Aufsetzen (spaetere Modell-Laeufe): Fingerabdruck des Maskenbereichs. Schon neu -> unveraendert weitergeben; weder alt
    # noch neu -> Abbruch (sonst wuerde das Fell doppelt gerechnet oder ein fremder Stand ueberschrieben); --trotzdem rechnet dennoch.
    fp = hashlib.md5(np.ascontiguousarray(old8[f["TM"] > 0]).tobytes()).hexdigest()
    if fp == BAUCH_NEU_MD5:
        tmp = aus + ".tmp"
        with open(tmp, "wb") as fh:
            fh.write(alt_bytes)
        os.replace(tmp, aus)
        print("BAUCHFELL_SCHON: Bauchbereich ist schon das neue Fell (%s) -> Eingang unveraendert nach %s" % (fp, aus))
        print("BAUCHFELL_OK MD5 %s (%.1fs) -> %s" % (hashlib.md5(alt_bytes).hexdigest(), time.time() - t0, aus))
        return
    if fp != BAUCH_ALT_MD5 and not trotzdem:
        fehler("Bauchbereich der Eingangs-Textur ist weder der alte (%s) noch der neue (%s), sondern %s -> Eingang pruefen "
               "(--trotzdem rechnet dennoch)" % (BAUCH_ALT_MD5, BAUCH_NEU_MD5, fp))
    neu, sel = fell(nz, old, f, opt)
    neu8 = np.clip(neu * 255.0 + 0.5, 0, 255).astype(np.uint8)
    neu8[~sel] = old8[~sel]
    # Selbstpruefung
    geaendert = (neu8 != old8).any(-1)
    gesp_texel = f["insel"] & (f["TI"] >= 0) & f["gesperrt"][np.maximum(f["TI"], 0)]
    n_aus = int((geaendert & ~sel).sum())
    n_gesp = int((geaendert & gesp_texel).sum())
    if n_aus or n_gesp:
        fehler("geaendert ausserhalb Maske %d, in gesperrten Inseln %d" % (n_aus, n_gesp))
    daten = png_wie(alt_bytes, neu8)
    zur = np.asarray(Image.open(io.BytesIO(daten)).convert("RGB"))
    if not np.array_equal(zur, neu8):
        fehler("PNG-Rueckleseprobe weicht ab")
    tmp = aus + ".tmp"
    os.makedirs(os.path.dirname(os.path.abspath(aus)) or ".", exist_ok=True)
    with open(tmp, "wb") as fh:
        fh.write(daten)
    os.replace(tmp, aus)
    md5 = hashlib.md5(daten).hexdigest()
    gl = sorted(int(x) for x in np.where(f["gesperrt"])[0])
    info = dict(md5=md5, eingang_glb=glb, eingang_textur=texp, opt={k: str(v) for k, v in opt.items()},
                texel_geaendert=int(geaendert.sum()), texel_geaendert_insel=int((geaendert & f["insel"]).sum()),
                texel_geaendert_polster=int((geaendert & f["pol"]).sum()), texel_maske_gt0=int(sel.sum()),
                texel_insel_maske_gt05=int((f["insel"] & (f["TM"] > 0.5)).sum()), gesperrte_inseln=gl,
                sekunden=round(time.time() - t0, 1))
    print("geaendert %d Texel (Insel %d, Polster %d), ausserhalb 0, gesperrte Inseln (%d) bit-gleich" % (
        info["texel_geaendert"], info["texel_geaendert_insel"], info["texel_geaendert_polster"], len(gl)))
    if bericht:
        json.dump(info, open(bericht, "w"), indent=1)
    if felder_aus:
        np.savez_compressed(felder_aus, **{k: v for k, v in f.items()})
    print("BAUCHFELL_OK MD5 %s (%.1fs) -> %s" % (md5, time.time() - t0, aus))


if __name__ == "__main__":
    main(sys.argv[1:])
