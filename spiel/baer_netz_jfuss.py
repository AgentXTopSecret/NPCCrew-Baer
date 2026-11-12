# Lauf baer-junges-fuss (11.11.2026), Bauer FORM: Netz des Baer-Jungen mit Beinen/Fuessen vom 2c-Baeren. Kopie von baer_netz_baby.py
# (MD5 ba385ab7, unveraendert gelassen); Funktionen hals_loft, gewichte_loft, in_rect, ATLAS wortgleich uebernommen, Rest neu:
#   Koerper = 2c-Spielnetz (Importer-Dump von quelle/2c/NCBear.glb 08ec7806) ohne Kopf/Hals (Head+Jaw+Neck >= 0,5), mit koerper_ruhe
#             (Faktoren S von heute, Skelett BIT-GLEICH fix1.npz) in die Ruhe des Jungen, dann
#             Rumpf-Ausgleich (Rumpf-Querschnitte wie heute, Beine wie 2c, baer_form_jfuss.rumpf_ausgleich),
#             Ring-Angleich (Koerperrand auf den heutigen geglaetteten Rand, baer_form_jfuss.ring_angleich),
#             optional Vorderpranken kleiner (pranke_vorn_f).
#   Kopf   = Teile U (Oberkopf mit Augen und heutigem Halsloch), J (Kiefer), Ol, Or (Ohren) FEST aus fix1.npz (Punkte, UV, Gewichte,
#             Dreiecke, kopfX, karte bit-gleich; nicht neu vernetzt, nicht neu geschweisst).
#   Hals H = neu: hals_loft (Parameter aus fix1.npz 'param') vom neuen Koerperrand, Naht-Streifen an die FESTEN 40 Lochrand-Punkte von U.
# Kein Blender noetig (nur numpy). Liest nur _arbeit/baer_junges_fuss/quelle und plan/dump (feste Kopien).
# Aufruf: python baer_netz_jfuss.py AUSGABE.npz [PARAM.json]
# Statisch/offline, nicht gespielt.
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_jfuss as bf  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
AUS = ARGS[0]
FP = dict(rumpf={}, bauch=True, bauch_y=(0.10, 0.17), ring_abfall=0.12, ring_sig=0.03, pranke_vorn_f=1.0)
# fix1 (Pruefer Technik T3): Schluessel "splitter_mm" in der Parameter-Datei (z. B. 2.0) = Splitter-Dreiecke darunter per Kantentausch
# entfernen; fehlt er, rechnet das Skript byte-gleich wie vor fix1 (a67e08fe).
if len(ARGS) > 1:
    FP.update(json.load(open(ARGS[1])))
t0 = time.time()


def log(*a):
    print("NETZ", round(time.time() - t0, 1), *a, flush=True)


# ------------------------------------------------------------------ heute (fest) ------------------------------------------------
HT = bf.lade_heute()
P = json.loads(str(HT["param"]))                      # Kopf-/Hals-Parameter genau wie fix1 (inkl. au_flaeche/au_ball)
ATLAS_HEUTE = json.loads(str(HT["atlas"]))
C_U = np.array(P.get("c_U", (-0.25, 0.0, -0.08)))
E, J, SK_INFO = bf.junges_jfuss()
# Skelett exakt wie heute (fix1.npz), damit k2w/w2k und koerper_ruhe bit-gleich rechnen (Abweichung vorher 4e-16)
J.BW = HT["BW"].copy()
J.t_loc = HT["t_loc"].copy()
J.inv_BW = np.array([np.linalg.inv(m) for m in J.BW])
W_D = float(HT["W_D"])
assert abs(W_D - bf.W_ZU_L * bf.L_SOLL * bf.M2U) < 1e-12
k2w, w2k = bf.kopf_welt(J, W_D)
log("Skelett gleich heute", SK_INFO)

# ------------------------------------------------------------------ Koerper: 2c im Jungen ---------------------------------------
K = bf.koerper_netz_jfuss(E, J)
log("Koerper 2c im Jungen", len(K["P"]), "Punkte", len(K["F"]), "Dreiecke; Randschleife", len(K["rand_loop"]), "Punkte, Schleifen",
    K["n_schleifen"], "Zacken-Dreiecke am Rand entfernt", bf.OHREN_INFO)
assert len(K["rand_loop"]) % 2 == 0, "hals_loft braucht eine gerade Zahl Randpunkte"
kh = HT["teil"] == 0
ih_ = -np.ones(len(kh), int)
ih_[kh] = np.arange(kh.sum())
F_heute = ih_[HT["F"][(HT["teil"][HT["F"]] == 0).all(1)]]
T_heute = bf.tier(HT["P"][kh])
T0 = bf.tier(K["P"])
par = dict(bf.RUMPF_PAR)
par.update(FP["rumpf"])
FELD = bf.rumpf_feld(T_heute, F_heute, T0, K["F"], par)
T1, AUSGL_INFO = bf.rumpf_ausgleich(T0, FELD, par)
log("Rumpf-Ausgleich", AUSGL_INFO)

# Bauch: Brust/Bauch zwischen den Beinen auf die heutige Hoehe (nur Rumpf-Gewicht, mittig |y| < bauch_y)
RUMPF_KN = ["Bip01", "Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Tail", "Bip01_L_Clavicle", "Bip01_R_Clavicle"]
w_rumpf = np.zeros(len(K["P"]))
for nm in RUMPF_KN:
    w_rumpf += np.where(K["Bi"] == E.idx[nm], K["Wt"], 0.0).sum(1)
BAUCH_INFO = {}
if FP["bauch"]:
    xs = FELD["xs"]
    zc = par["zc"]
    gut = np.isfinite(FELD["Bh"]) & np.isfinite(FELD["B2"]) & (FELD["B2"] < zc - 0.1) & (FELD["Bh"] < zc - 0.1)
    dB = bf._glatt1(np.where(gut, FELD["B2"] - FELD["Bh"], np.nan), par["sig_x"], par["dx"])
    dB = np.where(np.isfinite(dB), dB, 0.0)
    B2g = bf._glatt1(np.where(gut, FELD["B2"], np.nan), par["sig_x"], par["dx"])
    jn = np.where(np.isfinite(B2g))[0]
    B2g = B2g[jn[np.abs(np.arange(len(xs))[:, None] - jn[None]).argmin(1)]]
    x, y, z = T1[:, 0], T1[:, 1], T1[:, 2]
    v = np.clip((zc - z) / np.maximum(zc - np.interp(x, xs, B2g), 0.05), 0.0, 1.0)
    m = w_rumpf * (1.0 - bf.sst(FP["bauch_y"][0], FP["bauch_y"][1], np.abs(y))) * (z < zc)
    dz = -np.interp(x, xs, dB) * v * v * m
    T1 = T1 + np.stack((0 * dz, 0 * dz, dz), 1)
    BAUCH_INFO = dict(dz_min_cm=float(dz.min() * 100), dz_max_cm=float(dz.max() * 100), punkte=int((np.abs(dz) > 1e-4).sum()))
    log("Bauch", BAUCH_INFO)

# Vorderpranken (optional kleiner, Hoehe bleibt)
PRANKE_INFO = {}
if FP["pranke_vorn_f"] != 1.0:
    for s in ("L", "R"):
        w_h = np.where(K["Bi"] == E.idx["Bip01_%s_Hand" % s], K["Wt"], 0.0).sum(1)
        m = w_h > 0.5
        mitte = np.r_[T1[m, :2].mean(0), 0.0]
        T1 = bf.pranke_vorn(T1, bf.sst(0.3, 0.95, w_h) * (T1[:, 2] < 0.20), mitte, FP["pranke_vorn_f"])
        PRANKE_INFO[s] = dict(punkte=int(m.sum()), mitte=np.round(mitte, 3).tolist())
    log("Vorderpranken x", FP["pranke_vorn_f"], PRANKE_INFO)

# Ring-Angleich an den heutigen (geglaetteten) Koerperrand
R_heute, _, n_sch = bf.rand_schleife(T_heute, F_heute)
assert n_sch == 1 and len(R_heute) == 64, (n_sch, len(R_heute))
R_neu = T1[K["rand_loop"]]
d_vor = bf.abstand_schleifen(R_neu, R_heute) * 100
T2, d_rand, _ = bf.ring_angleich(T1, R_neu, R_heute, FP["ring_abfall"], FP["ring_sig"])
# Verschiebung (Ausgleich + Bauch + Ring) nahe am Rand glaetten (Laplace auf der Verschiebung, Rand fest): der Ring-Angleich zieht die
# gezackte 2c-Randschleife auf die glatte heutige Schleife; ohne Glaetten klappten am Kehlrand rechts 3 Dreiecke um (Probe v1).
rand_m = np.zeros(len(T0), bool)
wid0 = bf.schweiss_ids(T0, 6)
rand_m[np.isin(wid0, wid0[K["rand_loop"]])] = True
d_r = np.linalg.norm(T0[:, None, :] - T0[K["rand_loop"]][None], axis=2).min(1)
zone = d_r < FP.get("glatt_zone", 0.15)
um_vor = int(bf.umgekippt(T0, T2, K["F"]).sum())
T2 = bf.glaetten_verschiebung(T0, T2, K["F"], rand_m, zone, FP.get("glatt_runden", 40), 0.5)
T2, FALTEN_INFO = bf.falten_reparieren(T0, T2, K["F"], rand_m)
GLATT_INFO = dict(zone_punkte=int(zone.sum()), umgekippt_vorher=um_vor, umgekippt_nachher=int(bf.umgekippt(T0, T2, K["F"]).sum()),
                  falten=FALTEN_INFO)
log("Verschiebung geglaettet", GLATT_INFO)
d_nach = bf.abstand_schleifen(T2[K["rand_loop"]], R_heute) * 100
d_um = bf.abstand_schleifen(R_heute, T2[K["rand_loop"]]) * 100
RING_INFO = dict(vorher_median_cm=float(np.median(d_vor)), vorher_max_cm=float(d_vor.max()),
                 nachher_median_cm=float(np.median(d_nach)), nachher_max_cm=float(d_nach.max()),
                 heute_zu_neu_median_cm=float(np.median(d_um)), heute_zu_neu_max_cm=float(d_um.max()),
                 verschiebung_max_cm=float(np.linalg.norm(d_rand, axis=1).max() * 100))
log("Ring-Angleich", RING_INFO)
K["P"] = bf.dump(T2)
K["rand_loop_P"] = K["P"][K["rand_loop"]]
# Richtung "aus dem Koerper hinaus" je Randpunkt neu (wie koerper_netz)
wid_k = bf.schweiss_ids(K["P"], 6)
adj = {}
for f in K["F"]:
    for a_, b_ in ((0, 1), (1, 2), (2, 0)):
        adj.setdefault(wid_k[f[a_]], set()).add(wid_k[f[b_]])
        adj.setdefault(wid_k[f[b_]], set()).add(wid_k[f[a_]])
pos_w = np.zeros((wid_k.max() + 1, 3))
pos_w[wid_k] = K["P"]
rs = set(wid_k[K["rand_loop"]].tolist())
tang = []
for i_ in K["rand_loop"]:
    w_ = wid_k[i_]
    inn = [q for q in adj[w_] if q not in rs] or list(adj[w_])
    v_ = pos_w[w_] - pos_w[inn].mean(0)
    tang.append(v_ / np.linalg.norm(v_))
K["rand_tang"] = np.array(tang)


# ------------------------------------------------------------------ Hals (Loft vom Koerper-Rand in den Kopf) ---------------------
# wortgleich aus baer_netz_baby.py (fix1), globale Namen K, P, w2k, C_U, RING_DICHT
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
    assert P.get("hals_schweissen", False), "jfuss: nur der verschweisste Hals (fix1) ist vorgesehen"
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
HALS_SPALTE = None
HALS_INFO = {}
XH, FH, uvH, vH = hals_loft()
log("Hals-Loft", len(XH), "Punkte", len(FH), "Dreiecke", "Kehle", {k: v for k, v in HALS_INFO.items() if k not in ("ring_c", "ring_n")})

# ------------------------------------------------------------------ Kopf fest aus fix1.npz ---------------------------------------
TN = list(HT["teil_namen"])
KOPF_TEILE = ("U", "J", "Ol", "Or")
KOPF = {}
for nm in KOPF_TEILE:
    t = TN.index(nm)
    idx = np.where(HT["teil"] == t)[0]
    loc = -np.ones(len(HT["teil"]), int)
    loc[idx] = np.arange(len(idx))
    Ft = HT["F"][HT["teil"][HT["F"][:, 0]] == t]
    assert (HT["teil"][Ft] == t).all()
    KOPF[nm] = dict(idx=idx, F=loc[Ft], P=HT["P"][idx], X=HT["kopfX"][idx], UV=HT["UV"][idx], Wt=HT["Wt"][idx], Bi=HT["Bi"][idx],
                    karte=HT["karte"][idx], hals_b=HT["hals_b"][idx])
# Probe: k2w(kopfX) reproduziert die festen Punkte bit-gleich (gleiches Skelett, gleiche Rechnung)
d_k2w = max(float(np.abs(k2w(KOPF[nm]["X"]) - KOPF[nm]["P"]).max()) for nm in KOPF_TEILE)
log("Kopf fest: Teile", {nm: (len(KOPF[nm]["idx"]), len(KOPF[nm]["F"])) for nm in KOPF_TEILE}, "k2w-Probe max", d_k2w)


def naht_an_festes_loch():
    """Wie baer_netz_baby.schweissen(), aber das Loch in U ist FEST (fix1): Lochrand = Randschleife der festen U-Dreiecke (geschweisst
    nach Lage im Kopf-Rahmen, 1e-9), Reissverschluss-Streifen zwischen der letzten neuen Loft-Zeile und Kopien der festen Lochrand-Punkte
    (gleiche Lage wie U -> gemeinsame Normale beim Export), Hals-UV v = 1, Gewicht Head wie U."""
    global XH, FH, uvH, vH, HALS_SPALTE
    XU, FU = KOPF["U"]["X"], KOPF["U"]["F"]
    Ed, wd = RING_DICHT["E"], RING_DICHT["w"]
    rc, rn = np.array(HALS_INFO["ring_c"]), np.array(HALS_INFO["ring_n"])
    key = np.round(XU, 9)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    vertreter = {}
    for i in range(len(XU)):
        vertreter.setdefault(wid[i], i)
    Ew = np.sort(np.stack((wid[FU[:, [0, 1]]], wid[FU[:, [1, 2]]], wid[FU[:, [2, 0]]]), 1).reshape(-1, 2), axis=1)
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
    iB = np.array([vertreter[w_] for w_ in loop])           # Index in U (fest)
    B = XU[iB]
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
        B, iB, thB = B[::-1], iB[::-1], thB[::-1]
    k0 = int(np.argmin(np.abs(np.angle(np.exp(1j * (thB - thA[0]))))))
    B, iB, thB = np.roll(B, -k0, 0), np.roll(iB, -k0), np.roll(thB, -k0)
    dB = np.unwrap(richt * (thB - thA[0]))
    dB = dB - 2 * math.pi * np.round(dB[0] / (2 * math.pi))
    assert np.all(np.diff(dB) > -0.3), "Lochrand nicht monoton um die Halsachse"
    assert np.all(np.diff(dA) > 0), "neue Loft-Endzeile nicht monoton um die Halsachse"
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
    jb = np.linalg.norm(B[:, None] - Ed[None], axis=2).argmin(1)
    sB = ((B - Ed[jb]) * wd[jb]).sum(1)
    return np.r_[iB, iB[:1]], dict(lochrand_punkte=len(B), streifen=len(Fz),
                                    s_rand=[round(float(sB.min()), 4), round(float(sB.max()), 4)])


I_LOCH, NAHT_INFO = naht_an_festes_loch()
log("Naht an festes Loch", NAHT_INFO)

# ------------------------------------------------------------------ UV-Atlas (wortgleich, fix1-Stand mit hals_schweissen) --------
ATLAS = dict(koerper=(0.0, 0.0, 0.62, 0.62), vorn=(0.62, 0.0, 1.0, 0.38), hinten=(0.62, 0.38, 1.0, 0.62), band=(0.0, 0.62, 1.0, 0.78),
             hals=(0.0, 0.78, 1.0, 0.86), j_vorn=(0.0, 0.86, 0.14, 1.0), j_hinten=(0.14, 0.86, 0.28, 1.0),
             ohr_l_vorn=(0.28, 0.86, 0.42, 1.0), ohr_l_hinten=(0.42, 0.86, 0.56, 1.0), ohr_r_vorn=(0.56, 0.86, 0.70, 1.0),
             ohr_r_hinten=(0.70, 0.86, 0.84, 1.0))
if P.get("hals_schweissen", False):
    ATLAS.update(hals=(0.0, 0.78, 1.0, 0.885), j_vorn=(0.0, 0.885, 0.115, 1.0), j_hinten=(0.115, 0.885, 0.23, 1.0),
                 ohr_l_vorn=(0.23, 0.885, 0.345, 1.0), ohr_l_hinten=(0.345, 0.885, 0.46, 1.0), ohr_r_vorn=(0.46, 0.885, 0.575, 1.0),
                 ohr_r_hinten=(0.575, 0.885, 0.69, 1.0))
assert {k: list(v) for k, v in ATLAS.items()} == ATLAS_HEUTE, "Atlas weicht von fix1 ab"
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


# ------------------------------------------------------------------ Gewichte Hals (wortgleich) --------------------------------------
ih, ij = E.idx["Bip01_Head"], E.idx["Bip01_Jaw"]


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


# ------------------------------------------------------------------ Zusammenbau (Reihenfolge wie fix1: koerper U J H Ol Or) -------
PH = k2w(XH)
n_r0 = len(K["rand_loop"])
PH[:n_r0] = K["rand_loop_P"]                 # Zeile 0 = Koerperrand exakt (gleiche Lage -> verschweisst)
PH[n_r0] = K["rand_loop_P"][0]
nB = len(I_LOCH)
PH[-nB:] = KOPF["U"]["P"][I_LOCH]            # Naht-Streifen = Kopien der festen Lochrand-Punkte (bit-gleich)
XH[-nB:] = KOPF["U"]["X"][I_LOCH]
WtH, BiH, hbH = gewichte_loft(vH)
UVH = in_rect(uvH, np.zeros(2), np.ones(2), ATLAS["hals"], gleich=False)
teile = [("koerper", K["P"], K["F"], in_rect(K["UV"], np.zeros(2), np.ones(2), ATLAS["koerper"], gleich=False), K["Wt"], K["Bi"],
          np.full((len(K["P"]), 3), np.nan), np.array(["koerper"] * len(K["P"])), np.zeros(len(K["P"]))),
         ("U",) + tuple(KOPF["U"][k] for k in ("P", "F", "UV", "Wt", "Bi", "X", "karte", "hals_b")),
         ("J",) + tuple(KOPF["J"][k] for k in ("P", "F", "UV", "Wt", "Bi", "X", "karte", "hals_b")),
         ("H", PH, FH, UVH, WtH, BiH, XH, np.array(["hals"] * len(XH)), hbH),
         ("Ol",) + tuple(KOPF["Ol"][k] for k in ("P", "F", "UV", "Wt", "Bi", "X", "karte", "hals_b")),
         ("Or",) + tuple(KOPF["Or"][k] for k in ("P", "F", "UV", "Wt", "Bi", "X", "karte", "hals_b"))]
off = 0
L = {k: [] for k in ("P", "F", "UV", "Wt", "Bi", "X", "karte", "hb", "teil", "kopf_fest", "quelle")}
for t, (nm, Pp, Ff, UVp, Wp, Bp, Xp, kp, hb) in enumerate(teile):
    n = len(Pp)
    L["P"].append(Pp)
    L["F"].append(Ff + off)
    L["UV"].append(UVp)
    L["Wt"].append(Wp)
    L["Bi"].append(Bp)
    L["X"].append(Xp)
    L["karte"].append(kp)
    L["hb"].append(hb)
    L["teil"].append(np.full(n, t))
    L["kopf_fest"].append(KOPF[nm]["idx"] if nm in KOPF else -np.ones(n, int))
    L["quelle"].append(K["alt"] if nm == "koerper" else -np.ones(n, int))
    off += n
PA = np.concatenate(L["P"])
FA = np.concatenate(L["F"])
TID = np.concatenate(L["teil"])


def splitter_tausch(P, F, UV, teil, h_mm, erlaubt_teile=(0, 3)):
    """fix1 (T3): Dreiecke mit Hoehe < h_mm (Tier-mm, Ruhe) im Koerper/Hals: laengste Kante tauschen, wenn der Nachbar ueber diese Kante
    (gleiche Punkt-Indizes, also nicht ueber eine UV-Naht) im selben Teil liegt, das schlechtere der zwei Dreiecke hoeher wird, die
    Flaechen-Normalen zur alten Lage passen (Knick < 30 Grad, Diagonalen-Mitten <= 1 mm auseinander), die UV-Dreiecke nicht umklappen und die neue Kante noch nicht existiert.
    Punkte, UV und Gewichte bleiben; nur zwei Zeilen von F aendern sich je Tausch (Reihenfolge der Dreiecke bleibt). Kopf nie (teil 1/2/4/5)."""
    F = F.copy()
    Pt = P / 0.544 * 1000.0

    def hoehe(f):
        a, b_, c = Pt[f[0]], Pt[f[1]], Pt[f[2]]
        e = max(np.linalg.norm(b_ - a), np.linalg.norm(c - b_), np.linalg.norm(a - c))
        return float(np.linalg.norm(np.cross(b_ - a, c - a)) / max(e, 1e-12))

    def nrm(f):
        v = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]])
        return v / max(np.linalg.norm(v), 1e-300)

    def uvfl(f):
        u, v = UV[f[1]] - UV[f[0]], UV[f[2]] - UV[f[0]]
        return float(u[0] * v[1] - u[1] * v[0])
    kanten = {}
    for i, f in enumerate(F):
        for a, b_ in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            kanten.setdefault((min(a, b_), max(a, b_)), set()).add(i)
    ok_t = np.isin(teil, erlaubt_teile)
    kand = [i for i in range(len(F)) if ok_t[F[i]].all() and hoehe(F[i]) < h_mm]
    kand.sort(key=lambda i: hoehe(F[i]))
    getauscht = []
    for i in kand:
        if hoehe(F[i]) >= h_mm:
            continue
        f = [int(v) for v in F[i]]
        ks = [(f[0], f[1], f[2]), (f[1], f[2], f[0]), (f[2], f[0], f[1])]
        x, y, z = max(ks, key=lambda k: np.linalg.norm(P[k[0]] - P[k[1]]))
        nb = kanten.get((min(x, y), max(x, y)), set()) - {i}
        if len(nb) != 1:
            continue
        j = nb.pop()
        if not ok_t[F[j]].all():
            continue
        w_ = [int(v) for v in F[j] if v not in (x, y)]
        if len(w_) != 1 or (min(z, w_[0]), max(z, w_[0])) in kanten:
            continue
        w_ = w_[0]
        n1_, n2_ = (z, x, w_), (z, w_, y)
        alt = min(hoehe(F[i]), hoehe(F[j]))
        neu = min(hoehe(n1_), hoehe(n2_))
        if neu <= alt + 0.3:
            continue
        na = nrm(F[i]) * hoehe(F[i]) + nrm(F[j]) * hoehe(F[j])
        if nrm(n1_) @ na <= 0 or nrm(n2_) @ na <= 0 or nrm(n1_) @ nrm(n2_) < math.cos(math.radians(30)):
            continue
        # Form bleibt: die zwei Diagonalen liegen fast in einer Flaeche (Abstand ihrer Mitten entlang der Normalen <= 1 mm bei Groesse 1,0)
        if abs(float((Pt[x] + Pt[y] - Pt[z] - Pt[w_]) @ (na / max(np.linalg.norm(na), 1e-300)))) / 2.0 > 1.0:
            continue
        s_alt = np.sign(uvfl(F[i]))
        if np.sign(uvfl(F[j])) != s_alt or np.sign(uvfl(n1_)) != s_alt or np.sign(uvfl(n2_)) != s_alt:
            continue
        if min(abs(uvfl(n1_)), abs(uvfl(n2_))) < 1e-9:
            continue
        for k_, ff in ((i, F[i]), (j, F[j])):
            for a, b_ in ((ff[0], ff[1]), (ff[1], ff[2]), (ff[2], ff[0])):
                kanten[(min(a, b_), max(a, b_))].discard(k_)
        F[i] = n1_
        F[j] = n2_
        for k_, ff in ((i, F[i]), (j, F[j])):
            for a, b_ in ((ff[0], ff[1]), (ff[1], ff[2]), (ff[2], ff[0])):
                kanten.setdefault((min(int(a), int(b_)), max(int(a), int(b_))), set()).add(k_)
        getauscht.append((i, j, round(alt, 2), round(neu, 2)))
    return F, getauscht


SPLITTER_INFO = {}
if FP.get("splitter_mm", 0) > 0:
    _UVA = np.concatenate(L["UV"])
    _kopf_vor = FA[np.isin(TID[FA[:, 0]], (1, 2, 4, 5))].copy()
    FA, _tausch = splitter_tausch(PA, FA, _UVA, TID, FP["splitter_mm"])
    assert np.array_equal(FA[np.isin(TID[FA[:, 0]], (1, 2, 4, 5))], _kopf_vor), "Kopf-Dreiecke geaendert"
    SPLITTER_INFO = dict(grenze_mm=FP["splitter_mm"], getauscht=len(_tausch), paare=_tausch)
    log("fix1 T3: Splitter unter %.1f mm getauscht: %d Kanten (Dreieck, Nachbar, Hoehe alt -> neu mm): %s" % (
        FP["splitter_mm"], len(_tausch), _tausch[:12]))
benutzt = np.zeros(len(PA), bool)
benutzt[FA.ravel()] = True
assert benutzt.all(), "unbenutzte Punkte"
# Volumen je geschlossenem Teil (U+H+Koerper verschweisst zusammen, J, Ol, Or einzeln)
for gr in (("koerper", "U", "H"), ("J",), ("Ol",), ("Or",)):
    ids = [k for k, tt in enumerate(teile) if tt[0] in gr]
    Ft = FA[np.isin(TID[FA[:, 0]], ids)]
    v = np.einsum("ij,ij->i", PA[Ft[:, 0]], np.cross(PA[Ft[:, 1]], PA[Ft[:, 2]])).sum() / 6
    log("Volumen Dump", "+".join(gr), round(float(v), 6), "(muss > 0)")
    assert v > 0
log("GESAMT", len(PA), "Punkte", len(FA), "Dreiecke", {tt[0]: len(tt[2]) for tt in teile})
assert len(FA) <= 20000, len(FA)
INFO = dict(skelett=SK_INFO, ohren=bf.OHREN_INFO, rumpf=AUSGL_INFO, bauch=BAUCH_INFO, pranke_vorn=PRANKE_INFO, ring=RING_INFO, glatt=GLATT_INFO,
            hals={k: v for k, v in HALS_INFO.items()}, naht=NAHT_INFO, parameter=FP, rumpf_par=par, **({"splitter": SPLITTER_INFO} if SPLITTER_INFO else {}),
            dreiecke=int(len(FA)), punkte=int(len(PA)))
np.savez(AUS, P=PA, F=FA, UV=np.concatenate(L["UV"]), Wt=np.concatenate(L["Wt"]), Bi=np.concatenate(L["Bi"]), teil=TID,
         kopfX=np.concatenate(L["X"]), karte=np.concatenate(L["karte"]), hals_b=np.concatenate(L["hb"]),
         teil_namen=np.array([t[0] for t in teile]), BW=HT["BW"], t_loc=HT["t_loc"], S=HT["S"], W_D=HT["W_D"],
         param=HT["param"], atlas=HT["atlas"], koerper_alt=np.concatenate(L["quelle"])[TID == 0],
         quelle_index=np.concatenate(L["quelle"]), kopf_fest=np.concatenate(L["kopf_fest"]),
         uv_quelle=np.where((TID == 0)[:, None], np.r_[K["UV"], np.zeros((len(PA) - len(K["P"]), 2))], np.nan),
         info=json.dumps(INFO, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
json.dump(INFO, open(AUS[:-4] + ".json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
log("NETZ_OK", AUS)
