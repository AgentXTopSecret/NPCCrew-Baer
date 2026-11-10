# Lauf baer-baby (10.11.2026): Netz des Baer-Jungen (Entwurf). Blender 5.2.3 nur fuer die Dreiecksvernetzung (mathutils
# delaunay_2d_cdt), alles andere numpy (baer_form_baby.py). Neu gebaut, kein Original geaendert.
# Koerper = heutiges Spielnetz (NCBearTest 5066fa67, Dump) mit Junges-Proportionen, ohne Kopf und Hals (Gewicht Head+Jaw+Neck >= 0,5).
# Kopf = neue Teile aus der impliziten Form (SPEZ 4.1/4.2):
#   U  Oberkopf-Schale mit Hals-Lappen (deckt den Koerper-Rand), Augenmulden, Nase, Maul-Schnitt (Gaumen)  -> Head (+ Hals weich)
#   J  Unterkiefer-Schale (Kinn, Unterlippe, Zunge oben; steckt geschlossen im Oberkopf)                    -> Jaw
#   O  zwei Ohren (Rotationskoerper: Mulde vorn, dicker Rand)                                              -> Head
#   A  zwei Augaepfel (Kappe in der Mulde)                                                                 -> Head
# Jedes Kopfteil ist sternfoermig um seinen Mittelpunkt (geprueft) und wird aus Karten trianguliert; die Karten sind zugleich die UV.
# Aufruf: blender --background --factory-startup --python baer_netz_baby.py -- AUSGABE.npz [PARAM.json]
# Statisch/offline, nicht gespielt.
import json
import math
import sys
import time

import numpy as np
from mathutils.geometry import delaunay_2d_cdt

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_baby as bf  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:]
AUS = ARGS[0]
P = dict(bf.KOPF_P)
if len(ARGS) > 1:
    P.update(json.load(open(ARGS[1])))
t0 = time.time()


def log(*a):
    print("NETZ", round(time.time() - t0, 1), *a, flush=True)


E, J = bf.junges_standard()
K = bf.koerper_netz(E, J)
W_M = bf.W_ZU_L * bf.L_SOLL
W_D = W_M * bf.M2U
k2w, w2k = bf.kopf_welt(J, W_D)
log("Koerper", len(K["P"]), "Punkte", len(K["F"]), "Dreiecke; Randschleife", len(K["rand_loop"]), "Punkte")


def cdt(pts2, kanten=()):
    pts2 = np.asarray(pts2, float)
    r = delaunay_2d_cdt([(float(a), float(b)) for a, b in pts2], [tuple(map(int, e)) for e in kanten], [], 0, 1e-12)
    orig = r[3]
    m = np.array([o[0] if len(o) else -1 for o in orig])
    assert (m >= 0).all(), "CDT hat neue Punkte erzeugt"
    F = np.array([[m[i] for i in f] for f in r[2] if len(f) == 3])
    assert len(set(m.tolist())) == len(m) == len(pts2), (len(set(m.tolist())), len(m), len(pts2))
    return F


def ausrichten(F, X, c):
    """Ganze Karte (einheitlicher Umlauf aus CDT bzw. Gitter) nach aussen drehen: Mehrheit der Dreiecke zeigt von c weg.
    (Kein Einzel-Umdrehen: in Mulden zeigt die Aussennormale zur Mitte, das waere dort falsch.)"""
    n = np.cross(X[F[:, 1]] - X[F[:, 0]], X[F[:, 2]] - X[F[:, 0]])
    m = X[F].mean(1) - c
    a = np.linalg.norm(n, axis=1)
    if ((n * m).sum(1) * 0 + np.sign((n * m).sum(1)) * a).sum() < 0:
        return F[:, ::-1].copy()
    return F.copy()


# ------------------------------------------------------------------ Dichte (Kantenlaenge in W) ----------------------------------
DF = P.get("dichte_faktor", 1.0)


def l_oben(Pt):
    return DF * l_oben0(Pt)


def l_oben0(Pt):
    x, y, z = Pt[:, 0], Pt[:, 1], Pt[:, 2]
    l = np.full(len(Pt), P.get("dichte_basis", 0.066))
    l = np.where(x > -0.15, P.get("dichte_gesicht", 0.038), l)
    for s in (1.0, -1.0):
        d = np.linalg.norm(Pt - np.array((0.0, s * P["au_y"], 0.0)), axis=1)
        l = np.minimum(l, P.get("dichte_auge", 0.0068) + np.maximum(d - 0.045, 0) * P.get("steig_auge", 0.45))
        do = np.linalg.norm(Pt - np.array(P["ohr_c"]) * (1, s, 1), axis=1)
        l = np.minimum(l, 0.034 + np.maximum(do - 0.15, 0) * 0.3)
    dn = np.linalg.norm((Pt - np.array(P["na_c"])) / (1.0, 1.0, 1.3), axis=1)
    l = np.minimum(l, P.get("dichte_nase", 0.012) + np.maximum(dn - 0.10, 0) * P.get("steig_nase", 0.35))
    dl = np.min(np.linalg.norm(Pt[:, None, :] - LIPPE[None], axis=2), axis=1)       # Abstand zur Lippenkante (nicht zum Gaumen)
    l = np.minimum(l, P.get("dichte_maul", 0.012) + np.maximum(dl - 0.012, 0) * P.get("steig_maul", 0.45))
    if "ma_breite" in P:   # fix1 (M4): Kiefer-Rillen unter dem Kinn (|y| = ma_breite) sauber aufloesen
        yl = np.interp(x, *P["ma_breite"])
        rille = (np.abs(np.abs(y) - yl) < 0.03) & (x > P["ma_xh"] - 0.03) & (z < np.interp(x, *P["ma_linie"]) + 0.01)
        l = np.where(rille, np.minimum(l, P.get("dichte_rille", 0.018)), l)
    if VERDECKT is not None:   # fix1: Kopfschale im Hals-Schlauch (verdeckt) grob
        rc, rn, rr = VERDECKT
        dq = Pt - rc
        h_ = dq @ rn
        rad = np.linalg.norm(dq - np.outer(h_, rn), axis=1)
        l = np.where((h_ > 0.015) & (rad < 0.85 * rr), np.maximum(l, P.get("dichte_verdeckt", 0.11)), l)
    if P.get("wz_amp", 0) > 0:   # fix1: Wangen-Zacken brauchen ~ Periode/4
        wz = (np.abs(y) > 0.33) & (x > P["wz_x"][0] - 0.03) & (x < P["wz_x"][2] + 0.03) & (z < P["wz_z"][0] + 0.03) & (z > P["wz_z"][1] - 0.03)
        l = np.where(wz, np.minimum(l, P.get("dichte_wange", 0.032)), l)
    return l


def lippe_kante():
    xs = np.linspace(P["ma_xh"], 0.20, 12)
    hb = np.interp(xs, *P["sn_breite"]) * 0.95
    seite = [np.stack((xs, s * hb, np.interp(xs, *P["ma_linie"])), 1) for s in (1.0, -1.0)]
    ys = np.linspace(-0.15, 0.15, 9)
    vorn = np.stack((np.full(9, 0.215), ys, np.full(9, np.interp(0.215, *P["ma_linie"]))), 1)
    return np.concatenate(seite + [vorn])


LIPPE = lippe_kante()
VERDECKT = None


def l_kiefer(Pt):
    m = np.interp(Pt[:, 0], *P["ma_linie"])
    lippe = (Pt[:, 2] > m - 0.03) & (Pt[:, 2] < m + 0.004) & (Pt[:, 0] > P["ma_xh"] - 0.03)
    return DF * np.where(lippe, 0.016, np.where(Pt[:, 0] > P["ma_xh"] - 0.03, 0.032, P.get("dichte_kiefer_hinten", 0.07)))


# ------------------------------------------------------------------ Schale aus drei/zwei Karten ---------------------------------
def schale(feld, c, ax, l_fn, A1, A2, N1, N2, r_max, name, kante=None):
    """Sternfoermige Schale: Gesicht (alpha <= A1, flaechentreu), Band (A1..A2, beta x alpha), Rueckseite (alpha >= A2).
    A2 = None -> nur zwei Karten (vorn bis A1, hinten ab A1). Rueckgabe: X (W), F, karte, uvk (Karten-Koordinaten)."""
    c = np.asarray(c, float)
    ax = np.asarray(ax, float) / np.linalg.norm(ax)
    a, e1, e2 = bf.basis(ax)

    def ray(d):
        return bf.ray_cast(feld, c, d, r_max, n_grob=int(r_max / 0.004) + 2, n_bis=26)

    def h_flaech(axx):
        def h(xy):
            d = bf.richtung_aus_flaech(xy, axx)
            r = bf.ray_cast(feld, c, d, r_max, n_grob=int(r_max / 0.008) + 2, n_bis=12)
            return l_fn(c + d * r[:, None]) / r
        return h

    def ring_pkt(al, N):
        be = np.arange(N) * 2 * math.pi / N
        return np.cos(al) * a + np.outer(np.cos(be), np.sin(al) * e1) + np.outer(np.sin(be), np.sin(al) * e2), be

    teile = []
    # vorn
    rho1 = 2 * math.sin(A1 / 2)
    d1, be1 = ring_pkt(A1, N1)
    rand1 = bf.flaech_aus_richtung(d1, ax)
    s_rand = 2 * math.pi * rho1 / N1
    inn = bf.quadbaum((-rho1, -rho1), (rho1, rho1), h_flaech(ax), rho1 / 4, tiefe=9,
                      innen=lambda q: np.linalg.norm(q, axis=1) < rho1 - 0.6 * s_rand)
    kanten_vorn = []
    if kante is not None:     # Zwangskanten (Lippenkante, fix1: Augenringe): Punkte exakt auf der Kante, Nachbarpunkte zu nah entfernen
        if not isinstance(kante, list):
            kante = [(kante, False)]
        kqs = [bf.flaech_aus_richtung(kd, ax) for kd, _ in kante]
        alle = np.concatenate(kqs, 0)
        hk = h_flaech(ax)(alle)
        dd_ = np.linalg.norm(inn[:, None, :] - alle[None], axis=2)
        dmin = dd_.min(1)
        j = dd_.argmin(1)
        inn = inn[dmin > 0.45 * hk[j]]
        o = len(rand1) + len(inn)
        for kq, (_, zu) in zip(kqs, kante):
            kanten_vorn += [(o + i, o + i + 1) for i in range(len(kq) - 1)]
            if zu:
                kanten_vorn.append((o + len(kq) - 1, o))
            o += len(kq)
        inn = np.concatenate([inn] + kqs, 0)
    xy = np.concatenate((rand1, inn), 0)
    teile.append(("vorn", xy, bf.richtung_aus_flaech(xy, ax), len(rand1)))
    if A2 is not None:
        sk = math.sin((A1 + A2) / 2)
        d2, be2 = ring_pkt(A2, N2)
        # Band: Raender alpha = A1 (be1), alpha = A2 (be2), Naht beta = 0 / 2pi
        ns = max(3, int(round((A2 - A1) * sk / (2 * math.pi * sk / N1))))
        als = np.linspace(A1, A2, ns + 2)[1:-1]
        pts = [np.stack((be1 * sk, np.full(N1, A1)), 1), np.array([[2 * math.pi * sk, A1]]),
               np.stack((be2 * sk, np.full(N2, A2)), 1), np.array([[2 * math.pi * sk, A2]]),
               np.stack((np.zeros(ns), als), 1), np.stack((np.full(ns, 2 * math.pi * sk), als), 1)]
        rand = np.concatenate(pts, 0)

        def h_band(ba):
            d = bf.richtung_aus_band(ba, ax, sk)
            r = bf.ray_cast(feld, c, d, r_max, n_grob=int(r_max / 0.008) + 2, n_bis=12)
            return l_fn(c + d * r[:, None]) / r
        mar = 0.5 * 2 * math.pi * sk / max(N1, N2)
        inn = bf.quadbaum((0, A1), (2 * math.pi * sk, A2), h_band, (A2 - A1) / 3, tiefe=8,
                          innen=lambda q: (q[:, 0] > mar) & (q[:, 0] < 2 * math.pi * sk - mar) & (q[:, 1] > A1 + mar) & (q[:, 1] < A2 - mar))
        ba = np.concatenate((rand, inn), 0)
        teile.append(("band", ba, bf.richtung_aus_band(ba, ax, sk), len(rand)))
        Ah, dh = A2, d2
    else:
        Ah, dh = A1, d1
    # hinten (Projektion um -ax)
    rho2 = 2 * math.sin((math.pi - Ah) / 2)
    rand3 = bf.flaech_aus_richtung(dh, -ax)
    s3 = 2 * math.pi * rho2 / len(dh)
    inn = bf.quadbaum((-rho2, -rho2), (rho2, rho2), h_flaech(-ax), rho2 / 4, tiefe=9,
                      innen=lambda q: np.linalg.norm(q, axis=1) < rho2 - 0.6 * s3)
    xy = np.concatenate((rand3, inn), 0)
    teile.append(("hinten", xy, bf.richtung_aus_flaech(xy, -ax), len(rand3)))
    Xs, Fs, karte, uvk = [], [], [], []
    off = 0
    for nm, q, d, nrand in teile:
        r = ray(d)
        X = c + d * r[:, None]
        F = cdt(q, kanten_vorn if nm == "vorn" else ())
        F = ausrichten(F, X, c)
        Xs.append(X)
        Fs.append(F + off)
        karte += [nm] * len(X)
        uvk.append(q)
        off += len(X)
        log(name, nm, len(X), "Punkte", len(F), "Dreiecke", "Zwangskanten", len(kanten_vorn) if nm == "vorn" else 0)
    return np.concatenate(Xs), np.concatenate(Fs), np.array(karte), uvk


def feld_U(Q):
    return bf.kopf_feld(Q, P)


def feld_J(Q):
    return bf.kiefer_feld(Q, P)


P = bf.augen_setzen(P)
log("Augen Oberflaeche", np.round(P["au_flaeche"], 4).tolist(), "Augapfel-Mitten", np.round(P["au_ball"], 4).tolist())
C_U = np.array(P.get("c_U", (-0.25, 0.0, -0.08)))
AX_U = np.array(P.get("ax_U", (1.0, 0.0, -0.2)))
C_J = np.array(P.get("c_J", (0.07, 0.0, -0.29)))
AX_J = np.array(P.get("ax_J", (0.6, 0.0, -0.8)))
# Sternform pruefen
rng = np.random.default_rng(1)
dd = rng.normal(size=(4000, 3))
dd /= np.linalg.norm(dd, axis=1)[:, None]
sw = bf.stern_pruef(feld_U, C_U, dd, 1.3, n=520)
log("Stern U: Strahlen mit != 1 Wechsel", int((sw != 1).sum()), "von", len(sw))
for d_ in dd[sw != 1][:12]:
    ts_ = np.linspace(0, 1.3, 520)
    v_ = feld_U(C_U[None, :] + np.outer(ts_, d_)) >= 0
    w_ = np.where(np.diff(v_.astype(int)) != 0)[0]
    log("  U-Strahl", np.round(d_, 2), "Wechsel bei", [np.round(C_U + d_ * ts_[i], 3).tolist() for i in w_])
swj = bf.stern_pruef(feld_J, C_J, dd, 0.6, n=300)
log("Stern J: Strahlen mit != 1 Wechsel", int((swj != 1).sum()), "von", len(swj))
for d_ in dd[swj != 1][:6]:
    ts_ = np.linspace(0, 0.6, 300)
    v_ = feld_J(C_J[None, :] + np.outer(ts_, d_)) >= 0
    w_ = np.where(np.diff(v_.astype(int)) != 0)[0]
    log("  J-Strahl", np.round(d_, 2), "Wechsel bei", [np.round(C_J + d_ * ts_[i], 3).tolist() for i in w_])

def lippen_kante(n_seite=14, n_vorn=13):
    """Lippenkante = Schnitt der Ebene z = m(x) mit der ungeschnittenen Oberkopf-Flaeche, fuer x > x_h (Mundwinkel bis vorn)."""
    f0 = lambda Q: bf.kopf_feld(Q, P, mit_maul=False)  # noqa: E731
    xc = -0.05
    pts = []
    phis = np.r_[np.linspace(1.0, 0.0, n_seite, endpoint=False), np.linspace(0.0, -1.0, n_seite)]
    # Winkel so waehlen, dass die Seiten bis zum Mundwinkel x_h reichen: Suche je Winkel radial in der Ebene
    for ph in np.linspace(1.25, -1.25, 2 * n_seite + n_vorn):
        d2 = np.array((math.cos(ph), math.sin(ph), 0.0))
        rs = np.linspace(0.0, 0.4, 801)
        Q = np.array((xc, 0.0, 0.0)) + np.outer(rs, d2)
        Q[:, 2] = np.interp(Q[:, 0], *P["ma_linie"])
        v = f0(Q)
        i = np.where(v < 0)[0].max()
        p = Q[i]
        if p[0] < P["ma_xh"] + 0.004:
            continue
        if "ma_breite" in P and abs(p[1]) > np.interp(p[0], *P["ma_breite"]) - 0.004:   # fix1: Schnitt seitlich begrenzt
            continue
        pts.append(p)
    K3 = np.array(pts)
    d = K3 - C_U
    return d / np.linalg.norm(d, axis=1)[:, None], K3


LIPPE_D, LIPPE_3D = lippen_kante()
log("Lippenkante", len(LIPPE_3D), "Punkte, x", np.round(LIPPE_3D[:, 0].min(), 3), "..", np.round(LIPPE_3D[:, 0].max(), 3))


def augen_ringe(n_seg=24, rhos=(0.70, 1.0, 1.38)):
    """fix1 (Befund M3): runde Augenraender -- je Auge geschlossene Zwangskanten auf Ellipsen rho = konst. (rho 1 = Rand der Oeffnung,
    0,70 = auf dem Augapfel, 1,38 = aussen am weichen Rand). n_seg >= 16 Segmente (vorher Sechs-/Achteck aus der freien Vernetzung)."""
    out = []
    for i, s in enumerate((1.0, -1.0)):
        _, an = bf.auge_lage(P, s)
        fl = np.array(P["au_flaeche"][i])
        up = np.array((0.0, 0.0, 1.0))
        t_ = np.cross(up, an)
        t_ /= np.linalg.norm(t_)
        u_ = np.cross(an, t_)
        ph = np.arange(n_seg) * 2 * math.pi / n_seg
        for rho in rhos:
            tief = P["au_ball_tief"] if rho < 1 else 0.0
            Q = fl[None] + rho * (np.outer(np.cos(ph) * P["au_b"], t_) + np.outer(np.sin(ph) * P["au_h"], u_)) - an * tief
            d = Q - C_U
            out.append((d / np.linalg.norm(d, axis=1)[:, None], True))
    return out




# ------------------------------------------------------------------ Ohren --------------------------------------------------------
def ohr(s, n_psi=14):
    R = P["ohr_d"] / 2
    th = P["ohr_dicke"] / 2
    mt = P["ohr_mulde_t"]
    # Profil (r, h) von der Muldenmitte vorn ueber den Rand zur Mitte hinten
    mr = P.get("ohr_mulde_r", 0.6) * R          # Muldenrand
    prof = np.array([(0.0, th - mt), (0.45 * mr, th - mt + 0.002), (0.80 * mr, th - mt + 0.009), (mr, th - 0.006),
                     (mr + 0.35 * (R - mr), th), (mr + 0.75 * (R - mr), th - 0.012),
                     (R, -0.002), (R - 0.25 * (R - mr), -th + 0.010), (mr, -th), (0.45 * mr, -th - 0.002),
                     (0.0, -th - 0.003)])
    n = np.array(P["ohr_n"], float) * (1, s, 1)
    n /= np.linalg.norm(n)
    up = np.array((0.0, 0.0, 1.0))
    t1 = np.cross(n, up)
    t1 /= np.linalg.norm(t1)
    t2 = np.cross(n, t1)                     # zeigt nach unten-ish
    c = np.array(P["ohr_c"]) * (1, s, 1)
    psi = np.arange(n_psi) * 2 * math.pi / n_psi
    X, uv, kar = [], [], []
    idx = {}
    for i, (r, h) in enumerate(prof):
        if r == 0.0:
            idx[(i, 0)] = len(X)
            X.append(c + n * h)
            uv.append((0.0, 0.0))
            kar.append("ohr_vorn" if h > 0 else "ohr_hinten")
            continue
        for j, ps in enumerate(psi):
            idx[(i, j)] = len(X)
            X.append(c + n * h + r * (math.cos(ps) * t1 + math.sin(ps) * t2))
            # Karte: vorn bis zum Aussenrand (i <= 6), hinten danach; Rand doppelt (beide Karten)
            uv.append((r * math.cos(ps), r * math.sin(ps)))
            kar.append("ohr_vorn" if i <= 6 else "ohr_hinten")
    X = np.array(X)
    uv = np.array(uv)
    kar = np.array(kar)
    # Aussenrand (i = 6) fuer die hintere Karte doppeln
    rand_neu = {}
    for j in range(n_psi):
        k = idx[(6, j)]
        rand_neu[j] = len(X)
        X = np.vstack((X, X[k]))
        uv = np.vstack((uv, uv[k]))
        kar = np.append(kar, "ohr_hinten")
    F = []
    for i in range(len(prof) - 1):
        for j in range(n_psi):
            j2 = (j + 1) % n_psi
            if prof[i][0] == 0.0:
                F.append((idx[(i, 0)], idx[(i + 1, j)], idx[(i + 1, j2)]))
            elif prof[i + 1][0] == 0.0:
                a_ = rand_neu[j] if i == 6 else idx[(i, j)]
                b_ = rand_neu[j2] if i == 6 else idx[(i, j2)]
                F.append((a_, idx[(i + 1, 0)], b_))
            else:
                a_ = rand_neu[j] if i == 6 else idx[(i, j)]
                b_ = rand_neu[j2] if i == 6 else idx[(i, j2)]
                F.append((a_, idx[(i + 1, j)], idx[(i + 1, j2)]))
                F.append((a_, idx[(i + 1, j2)], b_))
    F = np.array(F)
    F = ausrichten(F, X, c)
    return X, F, kar, uv


# ------------------------------------------------------------------ Augaepfel ----------------------------------------------------
def auge(s, n_ring=5, n_seg=12, al_max=62):
    ac, an = bf.auge_lage(P, s)
    # Oberflaeche ohne Mulde entlang der Blickrichtung suchen
    f0 = lambda Q: bf.kopf_feld(Q, P, mit_auge=False, mit_maul=False, mit_hals=False)  # noqa: E731
    st = ac - an * 0.1
    tt = bf.ray_cast(f0, st, an[None, :], 0.3)[0]
    flaeche = st + an * tt
    rb = P["au_ball_r"]
    mz = flaeche - an * (P["au_ball_tief"] + rb)
    a, e1, e2 = bf.basis(an)
    X, uv = [mz + an * rb], [(0.0, 0.0)]
    for i in range(1, n_ring + 1):
        al = math.radians(al_max) * i / n_ring
        for j in range(n_seg):
            be = 2 * math.pi * j / n_seg
            d = math.cos(al) * a + math.sin(al) * (math.cos(be) * e1 + math.sin(be) * e2)
            X.append(mz + d * rb)
            uv.append((math.sin(al) * math.cos(be), math.sin(al) * math.sin(be)))
    F = []
    for j in range(n_seg):
        F.append((0, 1 + j, 1 + (j + 1) % n_seg))
    for i in range(1, n_ring):
        for j in range(n_seg):
            a_, b_ = 1 + (i - 1) * n_seg + j, 1 + (i - 1) * n_seg + (j + 1) % n_seg
            c_, d_ = 1 + i * n_seg + j, 1 + i * n_seg + (j + 1) % n_seg
            F.append((a_, c_, d_))
            F.append((a_, d_, b_))
    X = np.array(X)
    F = ausrichten(np.array(F), X, mz)
    return X, F, np.array(["auge"] * len(X)), np.array(uv), dict(mitte=mz.tolist(), flaeche=flaeche.tolist(), n=an.tolist())


ohren = [ohr(1.0), ohr(-1.0)]
log("Ohren", [len(o[1]) for o in ohren])


# ------------------------------------------------------------------ Hals (Loft vom Koerper-Rand in den Kopf) ---------------------
def rand_glaetten():
    """fix1 (Befund 'Nacken: Falte mit dunklem Schlitz'): die Randschleife des Koerpers (Schnitt nach Gewicht) ist gezackt (Zacken
    groesser als der erste Hals-Streifen) -> der erste Streifen klappte um (Knick bis 175 Grad, fix1/naht.py). Hier wird die Schleife
    in der Ruhe geglaettet (Laplace entlang der Schleife, 'rand_glatt' Runden), der erste Nachbarring im Koerper geht halb mit.
    Nur die Ruhe-Lage der Randpunkte aendert sich (Gewichte bleiben)."""
    it = int(P.get("rand_glatt", 0))
    if it <= 0:
        return
    Pk_ = K["P"]
    key_ = np.round(Pk_, 6)
    _, wid_ = np.unique(key_, axis=0, return_inverse=True)
    wid_ = wid_.ravel()
    R0 = K["rand_loop_P"].copy()
    R1 = R0.copy()
    for _ in range(it):
        R1 = (np.roll(R1, 1, 0) + 2 * R1 + np.roll(R1, -1, 0)) / 4
    dR = R1 - R0
    rw = wid_[K["rand_loop"]]
    verschieb = np.zeros((wid_.max() + 1, 3))
    gesetzt = np.zeros(wid_.max() + 1, bool)
    verschieb[rw] = dR
    gesetzt[rw] = True
    # erster Nachbarring: halbe mittlere Verschiebung der benachbarten Randpunkte
    acc = np.zeros((wid_.max() + 1, 3))
    cnt = np.zeros(wid_.max() + 1)
    for f in K["F"]:
        w3 = wid_[f]
        for a_ in range(3):
            for b_ in range(3):
                if a_ != b_ and gesetzt[w3[a_]] and not gesetzt[w3[b_]]:
                    acc[w3[b_]] += verschieb[w3[a_]]
                    cnt[w3[b_]] += 1
    nb = (cnt > 0) & ~gesetzt
    verschieb[nb] = 0.5 * acc[nb] / cnt[nb][:, None]
    K["P"] = Pk_ + verschieb[wid_]
    K["rand_loop_P"] = R1
    global RAND_INFO
    RAND_INFO = dict(runden=it, max_verschiebung_m=float(np.linalg.norm(dR, axis=1).max() / bf.M2U),
                     mittel_m=float(np.linalg.norm(dR, axis=1).mean() / bf.M2U), nachbarn=int(nb.sum()))


RAND_INFO = {}
rand_glaetten()
log("Koerperrand geglaettet", RAND_INFO)


def hals_loft():
    """Hals als Loft: Zeile v = 0 liegt genau auf der Randschleife des Koerpers (gleiche Lage, Tangente setzt die Koerperflaeche
    fort -> kein Kragen). fix1 (Befund M1 'Kopf aufgesteckt'): das Ende v = 1 liegt jetzt AUF der Kopfschale (eps darunter) und
    laeuft tangential in sie aus (Hohlkehle): je Spalte wird der Eintrittspunkt X* der alten Kurve in den Kopf gesucht, von dort
    'hals_kehle' W auf der Kopfflaeche weiter (Richtung = Halsachse in der Tangentialebene, weg vom Hals), Ende-Tangente = diese
    Flaechenrichtung. Damit gibt es keinen Knick (Kerbe) mehr zwischen Hals und Kopf; Kopf-Schale und Hals sind nur nicht
    verschweisst (Ende-Zeile 100 % Head, liegt eps unter der Kopfflaeche). Hermite-Kurven je Randpunkt."""
    R = w2k(K["rand_loop_P"])
    Tk = w2k(K["rand_loop_P"] + K["rand_tang"] * 1e-3) - R
    Tk /= np.linalg.norm(Tk, axis=1)[:, None]
    if P.get("hals_tangente_normal", False):
        # fix1: Start-Richtung exakt in der Tangentialebene des Koerpers (Punktnormale aus den Koerper-Dreiecken, geschweisst),
        # senkrecht zur Randschleife, aus dem Koerper hinaus -- vorher 'Rand minus Mittel der Nachbarn' (bis ~25 Grad daneben:
        # sichtbarer Knick Koerper/Hals, fix1/tmp/a5_nacken.png)
        Pk_, Fk_ = K["P"], K["F"]
        key_ = np.round(Pk_, 6)
        _, wid_ = np.unique(key_, axis=0, return_inverse=True)
        wid_ = wid_.ravel()
        fn_ = np.cross(Pk_[Fk_[:, 1]] - Pk_[Fk_[:, 0]], Pk_[Fk_[:, 2]] - Pk_[Fk_[:, 0]])
        acc_ = np.zeros((wid_.max() + 1, 3))
        for k_ in range(3):
            np.add.at(acc_, wid_[Fk_[:, k_]], fn_)
        nk = acc_[wid_[K["rand_loop"]]]
        nk = w2k(K["rand_loop_P"] + nk / np.linalg.norm(nk, axis=1)[:, None] * 1e-3) - R
        nk /= np.linalg.norm(nk, axis=1)[:, None]
        rt = np.roll(R, -1, 0) - np.roll(R, 1, 0)
        tn_ = np.cross(nk, rt)
        tn_ /= np.linalg.norm(tn_, axis=1)[:, None]
        tn_ = np.where(((tn_ * Tk).sum(1) < 0)[:, None], -tn_, tn_)
        Tk = tn_
    c = R.mean(0)
    a = np.array(P.get("hals_innen", (-0.30, 0.0, -0.20)))
    ax = (a - c) / np.linalg.norm(a - c)
    e1 = np.array((0.0, 1.0, 0.0))
    e1 = e1 - ax * (e1 @ ax)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    th = np.arctan2((R - c) @ e2, (R - c) @ e1)
    r1, r2 = P.get("hals_innen_r", (0.24, 0.20))
    I = a + np.outer(r1 * np.cos(th), e1) + np.outer(r2 * np.sin(th), e2)
    L = np.linalg.norm(I - R, axis=1)[:, None]
    n = len(R)

    def glatt(A, it=4):
        A = A.copy()
        for _ in range(it):
            A = (np.roll(A, 1, 0) + 2 * A + np.roll(A, -1, 0)) / 4
        return A
    Rg, Tg = glatt(R), glatt(Tk)
    Tg /= np.linalg.norm(Tg, axis=1)[:, None]
    t0g = Tg * L * P.get("hals_k0", 0.5)
    t1 = ax * L * P.get("hals_k1", 0.6)

    def herm(v, A, TA, B, TB):
        v = np.asarray(v, float)[:, None, None]
        h00, h10, h01, h11 = 2 * v ** 3 - 3 * v ** 2 + 1, v ** 3 - 2 * v ** 2 + v, -2 * v ** 3 + 3 * v ** 2, v ** 3 - v ** 2
        return h00 * A[None] + h10 * TA[None] + h01 * B[None] + h11 * TB[None]
    fK = lambda Q: bf.kopf_feld(Q, P, mit_maul=False)  # noqa: E731

    def grad(Q, h=1e-3):
        g = np.stack([(fK(Q + h * e) - fK(Q - h * e)) / (2 * h) for e in np.eye(3)], 1)
        return g / np.linalg.norm(g, axis=1)[:, None]
    info = {}
    if P.get("hals_kehle", 0) > 0:
        vf = np.linspace(0.0, 1.0, 401)
        Xs = herm(vf, Rg, t0g, I, t1)
        fv = fK(Xs.reshape(-1, 3)).reshape(len(vf), n)
        assert (fv[-1] < 0).all(), "altes Hals-Ende nicht im Kopf"
        ist = np.argmax(fv < 0, axis=0)
        Xst = Xs[ist, np.arange(n)]
        nS = grad(Xst)
        w = ax[None] - (nS @ ax)[:, None] * nS
        w /= np.linalg.norm(w, axis=1)[:, None]
        E0 = Xst + w * P["hals_kehle"]

        def auf_flaeche(Q):
            d = Q - C_U
            d /= np.linalg.norm(d, axis=1)[:, None]
            return C_U + d * bf.ray_cast(fK, C_U, d, 1.3)[:, None]
        S = auf_flaeche(E0)
        for _ in range(3):
            S = auf_flaeche(glatt(S, 3))
        nE = grad(S)
        wE = ax[None] - (nE @ ax)[:, None] * nE
        wE /= np.linalg.norm(wE, axis=1)[:, None]
        wE = glatt(wE, 2)
        wE -= (wE * nE).sum(1)[:, None] * nE
        wE /= np.linalg.norm(wE, axis=1)[:, None]
        Ende = S - nE * P.get("hals_eps", 0.004)
        L2 = np.linalg.norm(Ende - Rg, axis=1)[:, None]
        t0n = Tg * L2 * P.get("hals_k0", 0.5)
        t1n = wE * L2 * P.get("hals_k1e", 0.55)
        Xn = herm(vf, Rg, t0n, Ende, t1n)
        fn = fK(Xn.reshape(-1, 3)).reshape(len(vf), n)
        innen = (fn[(vf > 0.02) & (vf < 0.93)] < -0.003)
        info = dict(kehle_tief_min=float(fn[(vf > 0.02) & (vf < 0.93)].min()), punkte_innen=int(innen.sum()),
                    spalten_innen=int(innen.any(0).sum()), eintritt_v=[float(vf[ist].min()), float(vf[ist].max())])
        rc = Ende.mean(0)
        _, _, Vt = np.linalg.svd(Ende - rc)
        rn = Vt[2] if Vt[2] @ (c - rc) > 0 else -Vt[2]          # zeigt vom Kopf zum Koerper
        info.update(ring_c=rc.tolist(), ring_n=rn.tolist(), ring_r=float(np.linalg.norm(Ende - rc, axis=1).min()))
        RING_DICHT.update(E=Ende, w=wE)
        Iend, T1end, T0use, Luse = Ende, t1n, t0n, L2
    else:
        Iend, T1end, T0use, Luse = I, t1, t0g, L
    vs = np.array(P.get("hals_v", (0.0, 0.15, 0.35, 0.6, 1.0)))
    X, uv, vv, rows, spalte = [], [], [], [], []
    bog = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack((R, R[:1])), axis=0), axis=1))]
    bog /= bog[-1]
    for k, v in enumerate(vs):
        if k == 0:
            row, ub, sel = R, bog[:-1], np.arange(n)
        else:
            sel = np.arange(0, n, 2)          # ab Zeile 1 nur jede zweite Spalte
            row = herm([v], Rg, T0use, Iend, T1end)[0]
            if P.get("hals_kehle", 0) > 0:    # fix1: nahe am Koerperrand die ungeglaettete Randlage (sonst klappt der erste Streifen um)
                bl = np.clip(v / 0.35, 0, 1)
                bl = bl * bl * (3 - 2 * bl)
                row = row + (R - Rg) * (1 - bl)
            row = row[sel]
            ub = bog[sel]
        spalte += list(sel) + [0]
        rows.append((len(X), len(row)))
        X += list(np.vstack((row, row[:1])))
        uv += list(np.stack((np.r_[ub, 1.0], np.full(len(row) + 1, v)), 1))
        vv += [v] * (len(row) + 1)
    X = np.array(X)
    uv = np.array(uv)
    vv = np.array(vv)
    F = []
    o0, n0 = rows[0]
    o1, n1 = rows[1]
    for j in range(n1):
        a0, a1, a2 = o0 + 2 * j, o0 + 2 * j + 1, o0 + 2 * j + 2
        b0, b1 = o1 + j, o1 + j + 1
        F += [(a0, b0, a1), (a1, b0, b1), (a1, b1, a2)]
    for k in range(1, len(vs) - 1):
        oa, na = rows[k]
        ob, nb_ = rows[k + 1]
        for j in range(na):
            F += [(oa + j, ob + j, ob + j + 1), (oa + j, ob + j + 1, oa + j + 1)]
    ol, nl = rows[-1]
    RING_DICHT.update(zeile=(ol, nl))
    if not P.get("hals_schweissen", False):
        # Deckel am inneren Ende (liegt unter der Kopfflaeche; schliesst den Schlauch -> keine offenen Kanten)
        ci = len(X)
        X = np.vstack((X, a[None, :]))
        uv = np.vstack((uv, [[0.5, 1.0]]))
        vv = np.append(vv, 1.0)
        spalte.append(0)
        for j in range(nl):
            F.append((ol + j, ci, ol + j + 1))
    else:
        uv[:, 1] *= P.get("hals_uv_ende", 0.92)    # v 0,92..1 bleibt fuer den Naht-Streifen zur Kopfschale
    F = np.array(F)
    nrm = np.cross(X[F[:, 1]] - X[F[:, 0]], X[F[:, 2]] - X[F[:, 0]])
    m = X[F].mean(1)
    tt = np.clip(((m - c) @ ax) / np.linalg.norm(a - c), 0, 1)
    achse = c + np.outer(tt, a - c)
    if ((nrm * (m - achse)).sum(1) > 0).mean() < 0.5:
        F = F[:, ::-1]
    global HALS_SPALTE, HALS_INFO
    HALS_SPALTE = np.array(spalte)
    HALS_INFO = info
    return X, F, uv, vv


RING_DICHT = {}
XH, FH, uvH, vH = hals_loft()
uvH_roh = uvH.copy()
log("Hals", len(XH), "Punkte", len(FH), "Dreiecke", "Kehle", HALS_INFO)
# fix1: Teile der Kopfschale im Hals-Schlauch (verdeckt) grob vernetzen -> Dreiecke fuer Hohlkehle, Augenringe, Wangen
if "ring_c" in HALS_INFO:
    VERDECKT = (np.array(HALS_INFO["ring_c"]), np.array(HALS_INFO["ring_n"]), HALS_INFO["ring_r"])
def kinn_kante(n=19, psi_max=80.0):
    """fix1: Rand des Maul-Schnitts unter dem Kinn (Ebene x = x_h, unter der Mundlinie) als Zwangskante -- schliesst die
    Lippenkante zu einer Schleife um den Unterkiefer (vorher frei vernetzt: gezackter Rand, von unten sichtbar, fix1/r_alt/k_unten)."""
    f0 = lambda Q: bf.kopf_feld(Q, P, mit_maul=False)  # noqa: E731
    x0 = P["ma_xh"]
    m0 = float(np.interp(x0, *P["ma_linie"]))
    pts = []
    for ps in np.radians(np.linspace(-psi_max, psi_max, n)):
        d2 = np.array((0.0, math.sin(ps), -math.cos(ps)))
        rs = np.linspace(0.0, 0.5, 1001)
        Q = np.array((x0, 0.0, m0)) + np.outer(rs, d2)
        v = f0(Q)
        pts.append(Q[np.where(v < 0)[0].max()])
    K3 = np.array(pts)
    d = K3 - C_U
    return d / np.linalg.norm(d, axis=1)[:, None], K3


if P.get("kinn_kante", True):
    KINN_D, KINN_3D = kinn_kante()
    MAUL_SCHLEIFE = [(np.concatenate((LIPPE_D, KINN_D[::-1] if KINN_3D[0, 1] > 0 else KINN_D)), True)]
    log("Kinn-Kante", len(KINN_3D), "Punkte, Lippe Ende y", np.round(LIPPE_3D[[0, -1], 1], 3).tolist(), "Kinn Ende y", np.round(KINN_3D[[0, -1], 1], 3).tolist())
else:
    MAUL_SCHLEIFE = [(LIPPE_D, False)]
KANTEN_U = MAUL_SCHLEIFE + (augen_ringe(P.get("augen_n", 20), tuple(P.get("augen_rho", (0.72, 1.0)))) if P.get("augen_ringe", True) else [])
XU, FU, kU, uvU = schale(feld_U, C_U, AX_U, l_oben, math.radians(P.get("A1_U", 55)), math.radians(P.get("A2_U", 112)), 72, 56, 1.3, "U", kante=KANTEN_U)
XJ, FJ, kJ, uvJ = schale(feld_J, C_J, AX_J, l_kiefer, math.radians(95), None, 44, 44, 0.6, "J")


def schweissen():
    """fix1 (Befund M1, Vorschlag 'verschweissen'): Kopfschale U und Hals-Loft H zu EINER Flaeche verbinden. Das Loft-Ende liegt
    auf der Kopfflaeche (hals_eps 0). In U werden die Dreiecke im Hals-Schlauch und bis 'hals_loch' W hinter dem Loft-Ende
    entfernt (Abstand s entlang der Kopfflaeche, weg vom Hals); den Lochrand verbindet ein Reissverschluss-Streifen mit der letzten
    Loft-Zeile. Die Streifen-Punkte auf dem Lochrand sind Kopien der U-Randpunkte (gleiche Lage -> gemeinsame Normale beim Export),
    Hals-UV v = 1, Gewicht Head wie U."""
    global FU, XH, FH, uvH, vH, HALS_SPALTE
    Ed, wd = RING_DICHT["E"], RING_DICHT["w"]
    rc, rn, rr = np.array(HALS_INFO["ring_c"]), np.array(HALS_INFO["ring_n"]), HALS_INFO["ring_r"]
    j = np.linalg.norm(XU[:, None, :] - Ed[None], axis=2).argmin(1)
    s_ = ((XU - Ed[j]) * wd[j]).sum(1)
    nah = np.linalg.norm(XU - rc, axis=1) < 1.7 * rr
    weg_v = (s_ < P.get("hals_loch", 0.03)) & nah
    weg_f = weg_v[FU].any(1)
    FU_neu = FU[~weg_f]
    key = np.round(XU, 9)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    vertreter = {}
    for i in range(len(XU)):
        vertreter.setdefault(wid[i], i)
    Ew = np.sort(np.stack((wid[FU_neu[:, [0, 1]]], wid[FU_neu[:, [1, 2]]], wid[FU_neu[:, [2, 0]]]), 1).reshape(-1, 2), axis=1)
    u_, c_ = np.unique(Ew, axis=0, return_counts=True)
    rand = u_[c_ == 1]
    nbr = {}
    for a_, b_ in rand:
        nbr.setdefault(a_, []).append(b_)
        nbr.setdefault(b_, []).append(a_)
    einfach = all(len(v) == 2 for v in nbr.values())
    schleifen, gesehen = [], set()
    for st in nbr:
        if st in gesehen:
            continue
        lp, prev, cur = [st], None, st
        gesehen.add(st)
        while True:
            nx = [q for q in nbr[cur] if q != prev and q not in gesehen]
            if not nx:
                break
            prev, cur = cur, nx[0]
            lp.append(cur)
            gesehen.add(cur)
        schleifen.append(lp)
    assert einfach and len(schleifen) == 1, ("Lochrand nicht eine einfache Schleife", einfach, [len(x) for x in schleifen])
    loop = schleifen[0]
    B = np.array([XU[vertreter[w_]] for w_ in loop])
    e1 = np.cross(rn, (1.0, 0.0, 0.0))
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(rn, e1)

    def th(Q):
        return np.arctan2((Q - rc) @ e2, (Q - rc) @ e1)
    ol, nl = RING_DICHT["zeile"]
    A = XH[ol:ol + nl]
    uA = uvH[ol:ol + nl, 0].copy()
    thA = np.unwrap(th(A))
    richt = np.sign(thA[-1] - thA[0])
    dA = richt * (thA - thA[0])
    thB = th(B)
    tb = np.unwrap(thB)
    if np.sign(tb[min(3, len(B) - 1)] - tb[0]) != richt:
        B = B[::-1]
        thB = thB[::-1]
    k0 = int(np.argmin(np.abs(np.angle(np.exp(1j * (thB - thA[0]))))))
    B = np.roll(B, -k0, 0)
    thB = np.roll(thB, -k0)
    dB = np.unwrap(richt * (thB - thA[0]))
    dB = dB - 2 * math.pi * np.round(dB[0] / (2 * math.pi))
    assert np.all(np.diff(dB) > -0.3), "Lochrand nicht monoton um die Halsachse"
    uB = np.interp(np.clip(dB, 0, 2 * math.pi), np.r_[dA, 2 * math.pi], np.r_[uA, 1.0])
    oB = len(XH)
    XB = np.vstack((B, B[:1]))
    uvB = np.stack((np.r_[uB, 1.0], np.ones(len(B) + 1)), 1)
    XH = np.vstack((XH, XB))
    uvH = np.vstack((uvH, uvB))
    vH = np.append(vH, np.ones(len(XB)))
    HALS_SPALTE = np.append(HALS_SPALTE, np.zeros(len(XB), int))
    ua = np.r_[uA, 1.0]
    ub = np.r_[uB, 1.0]
    ia = list(range(ol, ol + nl + 1))
    ib = list(range(oB, oB + len(B) + 1))
    i = jj = 0
    Fz = []
    while i < len(ia) - 1 or jj < len(ib) - 1:
        if jj >= len(ib) - 1 or (i < len(ia) - 1 and ua[i + 1] <= ub[jj + 1]):
            Fz.append((ia[i], ib[jj], ia[i + 1]))
            i += 1
        else:
            Fz.append((ia[i], ib[jj], ib[jj + 1]))
            jj += 1
    Fz = np.array(Fz)
    nrm = np.cross(XH[Fz[:, 1]] - XH[Fz[:, 0]], XH[Fz[:, 2]] - XH[Fz[:, 0]])
    nH = np.cross(XH[FH[:, 1]] - XH[FH[:, 0]], XH[FH[:, 2]] - XH[FH[:, 0]])
    letzte = np.isin(FH, np.arange(ol, ol + nl + 1)).any(1)
    if (nrm @ nH[letzte].sum(0)).sum() < 0:
        Fz = Fz[:, ::-1]
    FH = np.vstack((FH, Fz))
    FU = FU_neu
    jb = np.linalg.norm(B[:, None] - Ed[None], axis=2).argmin(1)
    sB = ((B - Ed[jb]) * wd[jb]).sum(1)
    return dict(U_dreiecke_weg=int(weg_f.sum()), lochrand_punkte=len(B), streifen=len(Fz),
                s_rand=[round(float(sB.min()), 4), round(float(sB.max()), 4)])


if P.get("hals_schweissen", False):
    log("Schweissen Kopf/Hals", schweissen())

# ------------------------------------------------------------------ UV-Atlas -----------------------------------------------------
# glTF-UV: u nach rechts, v von oben. Rechtecke (u0, v0, u1, v1); Polster 4 px.
ATLAS = dict(koerper=(0.0, 0.0, 0.62, 0.62), vorn=(0.62, 0.0, 1.0, 0.38), hinten=(0.62, 0.38, 1.0, 0.62), band=(0.0, 0.62, 1.0, 0.78),
             hals=(0.0, 0.78, 1.0, 0.86), j_vorn=(0.0, 0.86, 0.14, 1.0), j_hinten=(0.14, 0.86, 0.28, 1.0),
             ohr_l_vorn=(0.28, 0.86, 0.42, 1.0), ohr_l_hinten=(0.42, 0.86, 0.56, 1.0), ohr_r_vorn=(0.56, 0.86, 0.70, 1.0),
             ohr_r_hinten=(0.70, 0.86, 0.84, 1.0))
if P.get("hals_schweissen", False):
    # fix1: verschweisster Hals braucht mehr Texel (Naht-Streifen zur Kopfschale): Hals-Streifen 0,78..0,885, untere Reihe enger
    ATLAS.update(hals=(0.0, 0.78, 1.0, 0.885), j_vorn=(0.0, 0.885, 0.115, 1.0), j_hinten=(0.115, 0.885, 0.23, 1.0),
                 ohr_l_vorn=(0.23, 0.885, 0.345, 1.0), ohr_l_hinten=(0.345, 0.885, 0.46, 1.0), ohr_r_vorn=(0.46, 0.885, 0.575, 1.0),
                 ohr_r_hinten=(0.575, 0.885, 0.69, 1.0))
POL = 4.0 / 1024


def in_rect(q, lo, hi, rect, gleich=True):
    u0, v0, u1, v1 = rect
    u0, v0, u1, v1 = u0 + POL, v0 + POL, u1 - POL, v1 - POL
    q = (q - lo) / (hi - lo)
    if gleich:   # Seitenverhaeltnis halten, mittig
        sx, sy = (u1 - u0), (v1 - v0)
        ar = (hi[0] - lo[0]) / (hi[1] - lo[1])
        if sx / sy > ar:
            w = sy * ar
            u0 += (sx - w) / 2
            sx = w
        else:
            h_ = sx / ar
            v0 += (sy - h_) / 2
            sy = h_
        return np.stack((u0 + q[:, 0] * sx, v0 + q[:, 1] * sy), 1)
    return np.stack((u0 + q[:, 0] * (u1 - u0), v0 + q[:, 1] * (v1 - v0)), 1)


teile = []   # (name, X_W, F, UV, gewicht-art)
# U
off = 0
UV_U = np.zeros((len(XU), 2))
for nm, q in zip(("vorn", "band", "hinten"), uvU):
    m = kU == nm
    lo, hi = q.min(0), q.max(0)
    if nm == "band":
        # v (Bild) = alpha: oben am Bild = alpha klein (Gesichtsrand)
        UV_U[m] = in_rect(q, lo, hi, ATLAS["band"], gleich=False)
    else:
        rr = np.abs(q).max()
        UV_U[m] = in_rect(q * (1, -1), np.array((-rr, -rr)), np.array((rr, rr)), ATLAS[nm])
teile.append(("U", XU, FU, UV_U, kU))
UV_J = np.zeros((len(XJ), 2))
for nm, q in zip(("vorn", "hinten"), uvJ):
    m = kJ == nm
    rr = np.abs(q).max()
    UV_J[m] = in_rect(q * (1, -1), np.array((-rr, -rr)), np.array((rr, rr)), ATLAS["j_" + nm])
teile.append(("J", XJ, FJ, UV_J, np.array(["j_" + k for k in kJ])))
teile.append(("H", XH, FH, in_rect(uvH, np.zeros(2), np.ones(2), ATLAS["hals"], gleich=False), np.array(["hals"] * len(XH))))
for s, (X, F, kar, uv), sl in ((1.0, ohren[0], "l"), (-1.0, ohren[1], "r")):
    UVo = np.zeros((len(X), 2))
    R = P["ohr_d"] / 2 * 1.02
    for nm in ("vorn", "hinten"):
        m = kar == "ohr_" + nm
        q = uv[m] * (1, -1) * (1 if nm == "vorn" else -1, 1)
        UVo[m] = in_rect(q, np.array((-R, -R)), np.array((R, R)), ATLAS["ohr_%s_%s" % (sl, nm)])
    teile.append(("O" + sl, X, F, UVo, np.array(["ohr_%s_%s" % (sl, k[4:]) for k in kar])))

# ------------------------------------------------------------------ Gewichte -----------------------------------------------------
ih, ij = E.idx["Bip01_Head"], E.idx["Bip01_Jaw"]
# Quelle fuer den Hals: entfernte Halspunkte (nicht Kopf) + Koerperpunkte nahe am Rand
wHJ_weg = np.zeros(len(K["weg_P"]))
for k in range(4):
    wHJ_weg += np.where(np.isin(K["weg_Bi"][:, k], (ih, ij)), K["weg_Wt"][:, k], 0.0)
qm = wHJ_weg < 0.5
Q_P = np.concatenate((K["weg_P"][qm], K["P"][K["wHJN"] > 0.05]))
Q_W = np.concatenate((K["weg_Wt"][qm], K["Wt"][K["wHJN"] > 0.05]))
Q_B = np.concatenate((K["weg_Bi"][qm], K["Bi"][K["wHJN"] > 0.05]))
Q_K = w2k(Q_P)


def gewichte_hals(X):
    d_kopf = bf.kopf_feld(X, P, mit_hals=False)
    b = np.clip((d_kopf - 0.0) / 0.16, 0.0, 1.0)
    b = b * b * (3 - 2 * b)
    Wt = np.zeros((len(X), 4))
    Bi = np.zeros((len(X), 4), int)
    for i in range(len(X)):
        if b[i] <= 1e-4:
            Wt[i, 0], Bi[i, 0] = 1.0, ih
            continue
        j = np.argmin(((Q_K - X[i]) ** 2).sum(1))
        acc = {}
        for k in range(4):
            if Q_W[j, k] > 0:
                acc[Q_B[j, k]] = acc.get(Q_B[j, k], 0.0) + b[i] * Q_W[j, k]
        acc[ih] = acc.get(ih, 0.0) + (1 - b[i])
        it = sorted(acc.items(), key=lambda t: -t[1])[:4]
        sw = sum(w for _, w in it)
        for k, (bb, w) in enumerate(it):
            Wt[i, k], Bi[i, k] = w / sw, bb
    return Wt, Bi, b


def gewichte_loft(vv):
    """Hals: v = 0 Gewichte des Koerper-Randpunkts, v = 1 nur Head; dazwischen weich (smoothstep 0,1..0,8)."""
    n = len(K["rand_loop"])
    rw = K["Wt"][K["rand_loop"]]
    rb = K["Bi"][K["rand_loop"]]
    Wt = np.zeros((len(vv), 4))
    Bi = np.zeros((len(vv), 4), int)
    b = np.clip((vv - 0.1) / 0.7, 0, 1)
    b = b * b * (3 - 2 * b)
    for k in range(len(vv)):
        i = int(HALS_SPALTE[k])
        acc = {}
        for q in range(4):
            if rw[i, q] > 0:
                acc[rb[i, q]] = acc.get(rb[i, q], 0.0) + (1 - b[k]) * rw[i, q]
        acc[ih] = acc.get(ih, 0.0) + b[k]
        it = sorted(acc.items(), key=lambda t: -t[1])[:4]
        sw = sum(w for _, w in it)
        for q, (bb, w) in enumerate(it):
            Wt[k, q], Bi[k, q] = w / sw, bb
    return Wt, Bi, b


def gewichte_kiefer(X):
    """fix1 (Befund M4 'Kiefer 0,92 W breite Platte'): der Unterkiefer bewegt nur die Mitte -- Jaw-Anteil 1 fuer |y| <= kj_y[0],
    0 fuer |y| >= kj_y[1] (dort Head: Wangen/Unterkopf neben dem Kinn bleiben zu), dazwischen weich (smoothstep); nach hinten
    (verdeckter Teil im Kopf) ebenso auf Head (kj_x). Ergebnis: beim Fressen oeffnet nur ein Maul <= 2 kj_y[1] W breit."""
    def sst_(a, b, v):
        t = np.clip((v - a) / (b - a), 0, 1)
        return t * t * (3 - 2 * t)
    w = sst_(P["kj_y"][1], P["kj_y"][0], np.abs(X[:, 1])) * sst_(P["kj_x"][0], P["kj_x"][1], X[:, 0])
    Wt = np.zeros((len(X), 4))
    Bi = np.zeros((len(X), 4), int)
    Wt[:, 0], Bi[:, 0] = w, ij
    Wt[:, 1], Bi[:, 1] = 1.0 - w, ih
    # nur ein Knochen, wo der andere 0 ist (Reihenfolge: groesseres Gewicht zuerst)
    tausch = Wt[:, 1] > Wt[:, 0]
    Wt[tausch] = Wt[tausch][:, [1, 0, 2, 3]]
    Bi[tausch] = Bi[tausch][:, [1, 0, 2, 3]]
    Bi[Wt == 0] = 0
    global KIEFER_INFO
    KIEFER_INFO = dict(punkte=len(X), voll_jaw=int((w > 0.999).sum()), misch=int(((w > 0.001) & (w < 0.999)).sum()),
                       head=int((w <= 0.001).sum()), breite_jaw_W=float(2 * np.abs(X[w > 0.5, 1]).max()))
    return Wt, Bi


KIEFER_INFO = {}
# ------------------------------------------------------------------ Zusammenbau --------------------------------------------------
Pk = [K["P"]]
Fk = [K["F"]]
UVk = [in_rect(K["UV"], np.zeros(2), np.ones(2), ATLAS["koerper"], gleich=False)]
Wk = [K["Wt"]]
Bk = [K["Bi"]]
teil_id = [np.zeros(len(K["P"]), int)]
kopfX = [np.full((len(K["P"]), 3), np.nan)]
karte = [np.array(["koerper"] * len(K["P"]))]
hals_b = [np.zeros(len(K["P"]))]
off = len(K["P"])
for tid, (nm, X, F, UV, kar) in enumerate(teile, start=1):
    Pw = k2w(X)
    if nm == "H":
        Wt, Bi, hb = gewichte_loft(vH)
    elif nm == "J" and P.get("kj_y"):
        Wt, Bi = gewichte_kiefer(X)
        hb = np.zeros(len(X))
    else:
        Wt = np.zeros((len(X), 4))
        Bi = np.zeros((len(X), 4), int)
        Wt[:, 0] = 1.0
        Bi[:, 0] = ij if nm == "J" else ih
        hb = np.zeros(len(X))
    Pk.append(Pw)
    Fk.append(F + off)               # Kopf-Rahmen -> Dump ist eine Drehung (kopf_rahmen_lokal, det +1): Umlauf bleibt, aussen = positiv
    UVk.append(UV)
    Wk.append(Wt)
    Bk.append(Bi)
    teil_id.append(np.full(len(X), tid))
    kopfX.append(X)
    karte.append(kar)
    hals_b.append(hb)
    off += len(X)
PA = np.concatenate(Pk)
FA = np.concatenate(Fk)
TID = np.concatenate(teil_id)
# fix1: unbenutzte Punkte (nach dem Schweissen entfernte Kopf-Dreiecke) aus allen Punkt-Feldern entfernen
benutzt = np.zeros(len(PA), bool)
benutzt[FA.ravel()] = True
if not benutzt.all():
    neu_i = -np.ones(len(PA), int)
    neu_i[benutzt] = np.arange(benutzt.sum())
    log("unbenutzte Punkte entfernt", int((~benutzt).sum()))
    PA, FA, TID = PA[benutzt], neu_i[FA], TID[benutzt]
    Pk, UVk, Wk, Bk, kopfX, karte, hals_b = ([np.concatenate(L)[benutzt]] for L in (Pk, UVk, Wk, Bk, kopfX, karte, hals_b))
    teil_id = [TID]
for t in range(1, len(teile) + 1):
    Ft = FA[TID[FA[:, 0]] == t]
    if P.get("hals_schweissen", False) and teile[t - 1][0] in ("U", "H"):   # verschweisst: U+H zusammen geschlossen
        Ft = FA[np.isin(TID[FA[:, 0]], [k + 1 for k, tt in enumerate(teile) if tt[0] in ("U", "H")])]
    v = np.einsum("ij,ij->i", PA[Ft[:, 0]], np.cross(PA[Ft[:, 1]], PA[Ft[:, 2]])).sum() / 6
    log("Volumen Dump", teile[t - 1][0], round(float(v), 6), "(muss > 0)")
    assert v > 0
log("Kiefer-Gewichte", KIEFER_INFO)
log("GESAMT", len(PA), "Punkte", len(FA), "Dreiecke (Koerper", len(K["F"]), ", Kopf", len(FA) - len(K["F"]), ")")
np.savez(AUS, P=PA, F=FA, UV=np.concatenate(UVk), Wt=np.concatenate(Wk), Bi=np.concatenate(Bk), teil=np.concatenate(teil_id),
         kopfX=np.concatenate(kopfX), karte=np.concatenate(karte), hals_b=np.concatenate(hals_b),
         teil_namen=np.array(["koerper"] + [t[0] for t in teile]), BW=J.BW, t_loc=J.t_loc, S=J.S, W_D=W_D,
         param=json.dumps({k: (v if not isinstance(v, np.ndarray) else v.tolist()) for k, v in P.items()}),
         atlas=json.dumps(ATLAS), koerper_alt=K["alt"])
log("NETZ_OK", AUS)
