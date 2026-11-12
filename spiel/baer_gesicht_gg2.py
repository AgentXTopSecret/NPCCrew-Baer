# Lauf baer-gen-gross-v2 (12.11.2026), Rolle BAUER GESICHT (PLAN.md 4 + 5): Schnauze/Nase des grossen Generator-Baeren breiter und kraeftiger,
# Gesichts-Ebene (Ton, Nasenkuppe, Nasenloecher, Augen, Lippenlinie) als Vertrag fuer FELL, Vorschau-Texturen nur zum Ansehen.
# Kevin (12.11.2026): "ja mach den eignen model lauf wo du den verbesserst besonders sein gesicht (nase) die ist voll schmall und so".
# Statisch/offline, nicht gespielt. Schreibt nur unter _arbeit/baer_gen_gross/v2/gesicht/ (und nichts in Test-Mods, NPC Crew, Spiel).
# Rahmen: tier-Meter (x vorn, y links, z oben, Boden 0). Gearbeitet wird am verschweissten V (10.119), nicht an Dump-Punkten.
# Aufruf: python baer_gesicht_gg2.py <befehl> [k=v ...]
#   form     Breiten-Feld eichen + stumpfe Kuppe -> form/E_gg2_basis.npz(+.json), gewichte/E_gg2_gewichte.npz
#   pruef    Pruefungen an der neuen Form (nur kopf_starr bewegt, Zwillinge, Symmetrie, Augen, Spitze, Kehle, Kevins Kamera, Boden,
#            Maul-Probe, Dehnung 15 Clips) -> mess/pruef_form.json
#   karten   Lage-Karte fuer das neue V (L, N, T, KR) -> karten/_karten_gg2.npz
#   ebene    Gesichts-Ebene (Vertrag 5.3) -> ebene/gesicht_ebene.npz + gesicht_ebene_vorschau.png
#   vorschau Vorschau-Texturen (fix1-Struktur x neuer Ton) -> tex_vorschau/NCBearGen.png, NCBearGenFoto.png
import json
import os
import sys

import numpy as np

R = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross/"
V2 = R + "v2/"
GS = V2 + "gesicht/"
EIN = GS + "eingang/"
# NACHBESSERUNG (12.11.2026, v2/NACHBESSERUNG.md, Mangel m1): Vorgabe ist der nachgebesserte Stand -- Form mit raeumlich geglaetteter
# Verschiebung an Lippenlinie/Mundwinkel/Wange, Ausgaben unter v2/nachbesserung/gesicht/. "nb=0" auf der Befehlszeile = Stand des
# BAUER GESICHT (raum_sigma 0, Ausgaben unter v2/gesicht/ -- dort NICHT neu schreiben, FELL prueft MD5).
NB = "nb=0" not in sys.argv
GA = V2 + "nachbesserung/gesicht/" if NB else GS             # Ausgabe-Ordner (form, gewichte, karten, ebene, mess, tex_vorschau)
sys.path.insert(0, R + "fix1/werkzeug")
M2U = 0.544

# ------------------------------------------------------------------------------------------------ Kopf-Rahmen (PLAN 2.1)
E = np.array([0.967, 0.0, 0.740])                         # Augenmitte (gemalte Augen, R/form/landmarken_gen.json)
SPITZE = np.array([1.150, 0.0, 0.636])
A = SPITZE - E
LS = float(np.linalg.norm(A))                             # 0,211
A = A / LS
U = np.array([0.0, 0.0, 1.0]) - A[2] * A
U /= np.linalg.norm(U)
AUGEN = [np.array([0.967, 0.0757, 0.740]), np.array([0.967, -0.0757, 0.740])]
TT = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95])
SOLL = np.array([0.133, 0.124, 0.112, 0.100, 0.092, 0.087, 0.084, 0.082, 0.080, 0.079, 0.077, 0.070])
TOL = np.array([0.003, 0.006, 0.006, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.005])


def sst(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def pchip(xk, yk, x):
    """monotone kubische Hermite-Interpolation (Fritsch-Carlson), aussen konstant (kein scipy auf diesem PC)."""
    xk, yk = np.asarray(xk, float), np.asarray(yk, float)
    h = np.diff(xk)
    dl = np.diff(yk) / h
    m = np.zeros_like(yk)
    for k in range(1, len(xk) - 1):
        if dl[k - 1] * dl[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / dl[k - 1] + w2 / dl[k])
    m[0], m[-1] = dl[0], dl[-1]
    x = np.clip(np.asarray(x, float), xk[0], xk[-1])
    i = np.clip(np.searchsorted(xk, x) - 1, 0, len(h) - 1)
    s = (x - xk[i]) / h[i]
    h00, h10, h01, h11 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s, -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
    return h00 * yk[i] + h10 * h[i] * m[i] + h01 * yk[i + 1] + h11 * h[i] * m[i + 1]


def rahmen(P):
    d = (P - E) @ A
    return d / LS, (P - E) @ U


def lade_ein():
    B = dict(np.load(EIN + "E_gen_basis_fix1.npz"))
    G = dict(np.load(EIN + "gewichte_fix1.npz"))
    assert np.array_equal(B["V"], G["V"])
    return B, G


def kopfmaske(G):
    nm = [str(n) for n in G["namen"]]
    return (G["W"][:, nm.index("Bip01_Head")] + G["W"][:, nm.index("Bip01_Jaw")]) > 0.5


def profil(V, kopf, tts=TT):
    """wie v2/plan/kk_mess.py: halb / oben_halb / hoehe je t (Querschnitt |d - tL| < 6 mm)"""
    t, h = rahmen(V)
    d = t * LS
    out = []
    for tt in tts:
        m = kopf & (np.abs(d - tt * LS) < 0.006)
        if m.sum() < 6:
            out.append((np.nan, np.nan, np.nan))
            continue
        top, bot = h[m].max(), h[m].min()
        ob = m & (np.abs(h - (top - 0.02)) < 0.007)
        out.append((float(np.abs(V[m, 1]).max()), float(np.abs(V[ob, 1]).max()) if ob.any() else np.nan, float(top - bot)))
    return np.array(out)


def hoehen_profil(V, kopf):
    """oben(t)/unten(t) des heutigen Querschnitts, glatt (fuer hn)."""
    t, h = rahmen(V)
    tg = np.linspace(-0.1, 1.05, 24)
    ob, un = [], []
    for tt in tg:
        m = kopf & (np.abs(t - tt) < 0.035)
        ob.append(h[m].max() if m.sum() > 5 else np.nan)
        un.append(h[m].min() if m.sum() > 5 else np.nan)
    ob, un = np.array(ob), np.array(un)
    ok = ~np.isnan(ob)
    ob, un = np.interp(tg, tg[ok], ob[ok]), np.interp(tg, tg[ok], un[ok])
    k = np.array([0.25, 0.5, 0.25])
    for _ in range(2):
        ob = np.r_[ob[0], np.convolve(ob, k, "valid"), ob[-1]]
        un = np.r_[un[0], np.convolve(un, k, "valid"), un[-1]]
    return tg, ob, un


def feld(V, starr, fk, hp, P):
    """Breiten-Feld (PLAN 4.2) + stumpfe Kuppe (4.3). Funktion NUR der Ruhe-Lage -> Zwillinge bleiben deckungsgleich."""
    t, h = rahmen(V)
    tg, ob, un = hp
    top, bot = np.interp(t, tg, ob), np.interp(t, tg, un)
    hn = np.clip((h - bot) / np.maximum(top - bot, 1e-3), 0, 1)
    tk = np.r_[TT, 1.0]
    f = np.where(t <= 0, 1.0, pchip(tk, fk, t))
    m = P["m0"] + P["m1"] * sst(0.45, 0.95, hn)
    w = sst(-0.02, 0.10, t) * starr
    w = w * (1 - sst(0.10, 0.16, -h - 0.12 - 0.20 * (0.3 - np.clip(t, 0, 0.3))))
    for au in AUGEN:
        w = w * sst(P["aug0"], P["aug1"], np.linalg.norm(V - au, axis=1))
    fy = 1 + (f - 1) * m * w
    V2_ = V.copy()
    V2_[:, 1] *= fy
    # stumpfe Kuppe: nur nach oben (u), nie nach vorn (+a)
    V2_ += (P["kuppe"] * sst(P["kt0"], P["kt1"], t) * sst(P["kh0"], P["kh1"], hn) * starr)[:, None] * U
    return V2_, dict(t=t, hn=hn, w=w, fy=fy)


P0 = dict(m0=0.75, m1=1.00, aug0=0.015, aug1=0.060, kuppe=0.014, kt0=0.78, kt1=0.98, kh0=0.30, kh1=0.85, runden=6, glatt=12, lam=0.5,
          soll95=0.066, f_ende=1.15, frei_t=0.03, soll10=0.119, soll20=0.107, soll30=0.096,
          soll40=0.090, raum_sigma=0.0, raum_lip0=0.020, raum_lip1=0.035)
if NB:
    P0["raum_sigma"] = 0.006                                            # NACHBESSERUNG m1 (nb=0: 0 = Stand BAUER GESICHT)
    P0["soll30"] = 0.0965                                               # sonst t 0,3 genau am Rand des Bands (0,0960 gegen 0,100 -+ 0,004)


def zwillings_gruppen(V):
    _, inv, cnt = np.unique(np.round(V, 7), axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    return [np.nonzero(inv == g)[0] for g in np.nonzero(cnt > 1)[0]]


def glaetten(V, Vf, T, frei, gruppen, schritte, lam):
    """Laplace-Glaetten NUR der Verschiebung D = Vf - V (uniforme Gewichte, Rand = nicht freie Punkte fest),
    Zwillinge bekommen nach jedem Schritt dieselbe Verschiebung (Mittel)."""
    D = Vf - V
    e = np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]])
    e = np.unique(np.sort(e, 1), axis=0)
    deg = np.zeros(len(V))
    np.add.at(deg, e[:, 0], 1)
    np.add.at(deg, e[:, 1], 1)
    for _ in range(int(schritte)):
        S = np.zeros_like(D)
        np.add.at(S, e[:, 0], D[e[:, 1]])
        np.add.at(S, e[:, 1], D[e[:, 0]])
        M = S / np.maximum(deg, 1)[:, None]
        D = np.where(frei[:, None], D + lam * (M - D), D)
        for g in gruppen:
            D[g] = D[g].mean(0)
    return V + D


def raum_region(V, B, P):
    """NACHBESSERUNG m1: Blend-Gewicht (Ruhe-Lage VOR dem Feld) fuer das raeumliche Glaetten -- Lippenlinie hinter der Spitze (x < 1,05),
    Mundwinkel und Wange hinter dem Auge (Orte aus v2/pruef/technik/knick.json). Spitze/Nasenkuppe und Augen bleiben unberuehrt."""
    Pl = V[B["lippe_ober"]]
    d = np.sqrt(((V[:, None, :] - Pl[None, :, :]) ** 2).sum(-1)).min(1)
    r = (1 - sst(P["raum_lip0"], P["raum_lip1"], d)) * (1 - sst(1.03, 1.06, V[:, 0]))
    for s in (1, -1):
        r = np.maximum(r, 1 - sst(0.02, 0.04, np.linalg.norm(V - np.array([0.94, s * 0.085, 0.684]), axis=1)))
    return r


def raum_glatt(V, Vg, frei, starr, tp, gruppen, rg, sig):
    """NACHBESSERUNG m1: Verschiebung D = Vg - V im Gebiet rg raeumlich (Gauss sigma in der Ruhe-Lage) glaetten. Der Graph-Laplace allein
    laesst fast deckungsgleiche Punkte an der Lippenlinie (Splitter-Dreiecke) mit verschiedenem D -> Knicke bis 84 Grad. Aussenhaut mittelt nur
    Aussenhaut, Mundwand mittelt Aussenhaut + Wand (geht mit der Lippe mit); Zaehne/Zunge/Gaumen unveraendert; Zwillinge danach gemittelt."""
    D = Vg - V
    Dn = D.copy()
    aussen = tp == "aussen"
    wand = np.isin(tp, ["wand_o", "wand_u"])
    quelle = starr > 0.5
    for ziel_m, q_m in ((frei & aussen & (rg > 0), quelle & aussen), (frei & wand & (rg > 0), quelle & (aussen | wand))):
        zi, qi = np.nonzero(ziel_m)[0], np.nonzero(q_m)[0]
        for a in range(0, len(zi), 400):
            z = zi[a:a + 400]
            d2 = ((V[z][:, None, :] - V[qi][None, :, :]) ** 2).sum(-1)
            w = np.exp(-d2 / (2 * sig * sig)) * (d2 < (3 * sig) ** 2)
            Dn[z] = (w @ D[qi]) / w.sum(1)[:, None]
    Dn = D + rg[:, None] * (Dn - D)
    for g in gruppen:
        Dn[g] = Dn[g].mean(0)
    return V + Dn


def feld_glatt(V, T, starr, fk, hp, P, gruppen, B=None):
    Vf, info = feld(V, starr, fk, hp, P)
    t, h = rahmen(V)
    frei = (starr > 0.5) & (t > P["frei_t"])
    for au in AUGEN:
        frei &= np.linalg.norm(V - au, axis=1) > 0.012
    Vg = glaetten(V, Vf, T, frei, gruppen, P["glatt"], P["lam"])
    if P.get("raum_sigma", 0) > 0:                                      # NACHBESSERUNG m1
        Vg = raum_glatt(V, Vg, frei, starr, B["teil_punkt"].astype(str), gruppen, raum_region(V, B, P), P["raum_sigma"])
    return Vg, info


def form(kv):
    P = dict(P0)
    P.update({k: float(v) for k, v in kv.items()})
    B, G = lade_ein()
    V = B["V"]
    starr = G["kopf_starr"].astype(float)
    kopf = kopfmaske(G)
    hp = hoehen_profil(V, kopf)
    ist = profil(V, kopf)
    soll = SOLL.copy()
    soll[-1] = P["soll95"]
    soll[1], soll[2], soll[3], soll[4] = P["soll10"], P["soll20"], P["soll30"], P["soll40"]
    fk = np.r_[np.clip(soll / ist[:, 0], 1, 3), 2.5]
    fk[0] = 1.0
    log = []
    gruppen = zwillings_gruppen(V)
    T = B["T"]
    for r in range(int(P["runden"])):
        Vn, info = feld_glatt(V, T, starr, fk, hp, P, gruppen, B)
        pr = profil(Vn, kopf)
        fehler = pr[:, 0] - soll
        log.append(dict(runde=r, fk=fk.round(3).tolist(), halb=pr[:, 0].round(4).tolist(), fehler_mm=(fehler * 1000).round(1).tolist()))
        print("Runde", r, "Fehler mm", (fehler * 1000).round(1).tolist(), flush=True)
        # Eichung: wirksamer Anteil des Feldes am breitesten Punkt -> Faktor nachfuehren (t 0 bleibt 1)
        fk[1:len(TT)] = 1 + (fk[1:len(TT)] - 1) * np.clip((soll[1:] - ist[1:, 0]) / np.maximum(pr[1:, 0] - ist[1:, 0], 1e-4), 0.5, 2.0)
        fk[-1] = fk[len(TT) - 1] * P["f_ende"]
        fk = np.clip(fk, 1.0, 3.0)
    Vn, info = feld_glatt(V, T, starr, fk, hp, P, gruppen, B)
    pr = profil(Vn, kopf)
    bew = np.linalg.norm(Vn - V, axis=1)
    assert ((bew > 1e-9) & (starr < 0.5)).sum() == 0, "Punkte ausserhalb kopf_starr bewegt"
    # Zwillinge (gleiche Ruhelage) muessen gleich bleiben
    k0 = np.round(V, 7)
    _, inv, cnt = np.unique(k0, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    zw_max = 0.0
    for g in np.nonzero(cnt > 1)[0]:
        ii = np.nonzero(inv == g)[0]
        zw_max = max(zw_max, float(np.abs(Vn[ii] - Vn[ii[0]]).max()))
    assert zw_max < 1e-12, zw_max
    Bn = dict(B)
    Bn["V"] = Vn
    os.makedirs(GA + "form", exist_ok=True)
    os.makedirs(GA + "gewichte", exist_ok=True)
    np.savez_compressed(GA + "form/E_gg2_basis.npz", **Bn)
    Gn = dict(G)
    Gn["V"] = Vn
    np.savez_compressed(GA + "gewichte/E_gg2_gewichte.npz", **Gn)
    ist_d = {"%.2f" % tt: dict(halb=round(float(a), 4), oben_halb=round(float(b), 4), hoehe=round(float(c), 4)) for tt, (a, b, c) in zip(TT, ist)}
    neu_d = {"%.2f" % tt: dict(halb=round(float(a), 4), oben_halb=round(float(b), 4), hoehe=round(float(c), 4)) for tt, (a, b, c) in zip(TT, pr)}
    js = dict(parameter=P, fk_t=np.r_[TT, 1.0].tolist(), fk=fk.round(4).tolist(), soll_halb=SOLL.tolist(), toleranz=TOL.tolist(),
              profil_vorher=ist_d, profil_nachher=neu_d, eichung=log, bewegt=int((bew > 1e-9).sum()), max_cm=round(float(bew.max() * 100), 2),
              zwillinge_max_m=zw_max, hoehen_profil=dict(t=hp[0].round(3).tolist(), oben=hp[1].round(4).tolist(), unten=hp[2].round(4).tolist()))
    json.dump(js, open(GA + "form/E_gg2_basis.npz.json", "w"), indent=1)
    print("bewegt", js["bewegt"], "max cm", js["max_cm"])
    for tt in TT:
        k = "%.2f" % tt
        print("t", k, "vorher", ist_d[k], "nachher", neu_d[k], "soll", SOLL[list(TT).index(tt)])


# ------------------------------------------------------------------------------------------------ Pruefungen (PLAN 3.1, 4.5, 4.6, 8 A5-A8, B)
CLIPS = ["DeerStag_Idle01", "DeerStag_Walk", "DeerStag_Run", "DeerStag_Death", "DeerStag_Dead", "NCBear_Rear", "NCBear_SwipeL",
         "NCBear_SwipeR", "NCBear_Slam", "NCBear_Bite", "NCBear_Maul", "NCBear_Eat", "NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp"]
JAW = np.array([0.8044, 0.0, 0.6454])                    # 2c-Jaw-Gelenk (R/plan/mess/mess_e_2c.json)


def kk_werte(V, W, kopf, sk):
    """Kevins Kamera az 0 / el 30 (Logik v2/plan/kk_mess.py): Schnauzenbreite / Kopfbreite in Hoehe der Kuppe +0/3/6/9 cm."""
    c30, s30 = np.cos(np.radians(30)), np.sin(np.radians(30))
    tip = V[kopf][np.argmax(V[kopf, 0])].copy()
    tip[1] = 0
    nase = kopf & (np.linalg.norm(V - tip, axis=1) < 0.03)
    out = {}
    for clip, f in (("DeerStag_Idle01", 0), ("NCBear_Eat", 32), ("DeerStag_Walk", 7)):
        P = sk.bild(V, W, clip, f)
        sx = P[:, 1]
        sy = -s30 * P[:, 0] + c30 * P[:, 2]
        ko = kopf & (V[:, 2] < 0.86)
        kb = sx[ko].max() - sx[ko].min()
        ny = np.median(sy[nase])
        dd = {"kopf_breite": round(float(kb), 3)}
        for nmr, dy in (("nase", 0.0), ("+3cm", 0.03), ("+6cm", 0.06), ("+9cm", 0.09)):
            mr = kopf & (np.abs(sy - (ny + dy)) < 0.005) & (V[:, 0] > E[0])
            if mr.any():
                b = sx[mr].max() - sx[mr].min()
                dd[nmr] = [round(float(b), 3), round(float(b / kb), 3)]
        out["%s_%d" % (clip, f)] = dd
    return out


def windung(P, Tm, Q):
    """Windungszahl der geschlossenen Flaeche (P, Tm) an den Punkten Q (Kopie aus R/form/werkzeug/gg_maul_probe.py)."""
    out = np.zeros(len(Q))
    A_ = P[Tm[:, 0]]
    B_ = P[Tm[:, 1]]
    C_ = P[Tm[:, 2]]
    for i, q in enumerate(Q):
        a, b, c = A_ - q, B_ - q, C_ - q
        la, lb, lc = np.linalg.norm(a, axis=1), np.linalg.norm(b, axis=1), np.linalg.norm(c, axis=1)
        det = np.einsum("ij,ij->i", a, np.cross(b, c))
        den = la * lb * lc + np.einsum("ij,ij->i", a, b) * lc + np.einsum("ij,ij->i", b, c) * la + np.einsum("ij,ij->i", c, a) * lb
        out[i] = np.arctan2(det, den).sum() * 2 / (4 * np.pi)
    return out


def maul_probe(B, V):
    jaw = B["kiefer_anteil"]
    T = B["T"]
    td = B["teil_dreieck"].astype(str)
    tp = B["teil_punkt"].astype(str)
    haut = td == "aussen"
    zahn = np.array([t.startswith("zahn") for t in tp])
    zunge = tp == "zunge"
    innen = ~np.isin(tp, ["aussen"]) & ~zahn & ~zunge & (tp != "kralle")

    def offen(a_grad):
        a = np.radians(a_grad)
        c, s = np.cos(a), np.sin(a)
        Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        return V + jaw[:, None] * ((V - JAW) @ Ry.T + JAW - V)

    er = {}
    for a in (0, 3, 5):
        P = offen(a)
        er["winkel_%d" % a] = dict(zahn_aussen=int((np.abs(windung(P, T[haut], P[zahn])) < 0.5).sum()),
                                   zunge_aussen=int((np.abs(windung(P, T[haut], P[zunge])) < 0.5).sum()))
    P = offen(0)
    er["innenwand_punkte"] = int(innen.sum())
    er["innenwand_aussen"] = int((np.abs(windung(P, T[haut], P[innen])) < 0.5).sum())
    hp = np.unique(T[haut].ravel())
    d = np.sqrt(((P[zahn][:, None, :] - P[hp][None, :, :]) ** 2).sum(-1)).min(1)
    er["zahn_luft_mm_min"] = round(float(d.min()) * 1000, 2)
    return er


def dehnung(V, T, W, sk, RT, RN, kopf_d):
    from fx_lib import dehn_vorb, sigma
    gt, RI = dehn_vorb(V, T)
    za = np.isin(RT, [RN.index("achsel"), RN.index("brust")])
    out = {}
    for c in CLIPS:
        s1all = []
        for f in range(sk.bildzahl(c)):
            s1, s2 = sigma(sk.bild(V, W, c, f), T, RI)
            s1all.append(s1)
        s1 = np.array(s1all)[:, gt]
        out[c] = dict(p995=round(float(np.percentile(s1, 99.5)), 3), max=round(float(s1.max()), 3),
                      achsel_brust_max=round(float(s1[:, za[gt]].max()), 3), kopf_maul_max=round(float(s1[:, kopf_d[gt]].max()), 3))
    return out


def pruef(kv):
    from fx_lib import lade_dump, Skin
    basis = kv.get("basis", GA + "form/E_gg2_basis.npz")
    aus = kv.get("aus", GA + "mess/pruef_form.json")
    schnell = kv.get("schnell", "0") == "1"
    B0, G0 = lade_ein()
    Bn = dict(np.load(basis))
    V0, Vn, T, W = B0["V"], Bn["V"], B0["T"], G0["W"]
    assert np.array_equal(T, Bn["T"])
    starr = G0["kopf_starr"]
    kopf = kopfmaske(G0)
    D = lade_dump(R + "rig/dump_2c.txt")
    sk = Skin(D, [str(n) for n in G0["namen"]])
    tp = B0["teil_punkt"].astype(str)
    aussen = tp == "aussen"
    o = {}
    bew = np.linalg.norm(Vn - V0, axis=1)
    o["bewegt"] = int((bew > 1e-9).sum())
    o["bewegt_ausserhalb_kopf_starr"] = int(((bew > 1e-9) & ~starr).sum())
    o["max_verschiebung_cm"] = round(float(bew.max() * 100), 2)
    k0 = np.round(V0, 7)
    _, inv, cnt = np.unique(k0, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    o["zwillinge_gruppen"] = int((cnt > 1).sum())
    o["zwillinge_max_abstand_m"] = float(max(np.abs(Vn[inv == g] - Vn[inv == g][0]).max() for g in np.nonzero(cnt > 1)[0]))
    # Spitze, Augen, Kehle
    o["spitze_x"] = [round(float(V0[kopf, 0].max()), 4), round(float(Vn[kopf, 0].max()), 4)]
    aug = np.zeros(len(V0), bool)
    for au in AUGEN:
        aug |= np.linalg.norm(V0 - au, axis=1) < 0.02
    o["augen_2cm_max_verschiebung_mm"] = round(float(bew[aug].max() * 1000), 2)
    t0, h0 = rahmen(V0)
    kehle = starr & (t0 < 0.3) & (h0 < -0.15)
    o["kehle_breite"] = [round(float(np.abs(V0[kehle, 1]).max()), 4), round(float(np.abs(Vn[kehle, 1]).max()), 4),
                         round(float(np.abs(Vn[kehle, 1]).max() / np.abs(V0[kehle, 1]).max()), 4)]
    o["profil"] = {"%.2f" % tt: dict(halb=round(float(a), 4), oben_halb=None if np.isnan(b) else round(float(b), 4),
                                     oben_anteil=None if np.isnan(b) else round(float(b / a), 2), hoehe=round(float(c), 4),
                                     soll=float(s), ok=bool(abs(a - s) <= tol))
                   for tt, (a, b, c), s, tol in zip(TT, profil(Vn, kopf), SOLL, TOL)}
    o["profil_heute"] = {"%.2f" % tt: dict(halb=round(float(a), 4), oben_halb=None if np.isnan(b) else round(float(b), 4), hoehe=round(float(c), 4))
                         for tt, (a, b, c) in zip(TT, profil(V0, kopf))}
    # Symmetrie (Kopf-Aussenhaut: Abstand zum Spiegelbild)
    for tag, V in (("heute", V0), ("neu", Vn)):
        Q = V[starr & aussen]
        M = Q * np.array([1, -1, 1])
        dd = np.sqrt(((M[:, None, :] - Q[None, :, :]) ** 2).sum(-1)).min(1)
        o["symmetrie_%s_cm" % tag] = [round(float(np.median(dd) * 100), 3), round(float(np.percentile(dd, 95) * 100), 3)]
    # Flaechenwinkel in der Zone (bewegte Dreiecke), p99
    zone = (bew[T] > 1e-9).any(1)
    kl = np.minimum.reduce([np.linalg.norm(V0[T[:, a]] - V0[T[:, b]], axis=1) for a, b in ((0, 1), (1, 2), (2, 0))])
    for tag, V, zz in (("heute", V0, zone), ("neu", Vn, zone), ("heute_ab7mm", V0, zone & (kl >= 0.0074)), ("neu_ab7mm", Vn, zone & (kl >= 0.0074))):
        fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
        fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
        kanten = {}
        for i in np.nonzero(zz & (B0["teil_dreieck"].astype(str) == "aussen"))[0]:
            for a, b in ((0, 1), (1, 2), (2, 0)):
                kanten.setdefault((min(T[i, a], T[i, b]), max(T[i, a], T[i, b])), []).append(i)
        ang = [np.degrees(np.arccos(np.clip(fn[v[0]] @ fn[v[1]], -1, 1))) for v in kanten.values() if len(v) == 2]
        o["flaechenwinkel_zone_%s_grad" % tag] = [round(float(np.percentile(ang, 99)), 2), round(float(np.max(ang)), 2)]
    o["kevin_kamera_heute"] = kk_werte(V0, W, kopf, sk)
    o["kevin_kamera_neu"] = kk_werte(Vn, W, kopf, sk)
    print(json.dumps({k: v for k, v in o.items() if k not in ("profil", "profil_heute")}, indent=0), flush=True)
    for k, v in o["profil"].items():
        print("t", k, v)
    if not schnell:
        # Boden: alle Clips, alle Bilder; Schnauze (Kopf-Aussenhaut) Eat/Maul
        bo = {}
        ks = kopf & aussen
        for tag, V in (("heute", V0), ("neu", Vn)):
            for c in CLIPS:
                zmin, zk = 9.0, 9.0
                for f in range(sk.bildzahl(c)):
                    P = sk.bild(V, W, c, f)
                    zmin = min(zmin, P[:, 2].min())
                    zk = min(zk, P[ks, 2].min())
                bo.setdefault(c, {})[tag] = dict(netz_min_cm=round(float(zmin * 100), 2), schnauze_min_cm=round(float(zk * 100), 2))
        o["boden"] = bo
        print("BODEN", json.dumps(bo), flush=True)
        o["maul_heute"] = maul_probe(B0, V0)
        o["maul_neu"] = maul_probe(B0, Vn)
        print("MAUL", o["maul_heute"], o["maul_neu"], flush=True)
        RT, RN = G0["regionen"], [str(s) for s in G0["regionen_namen"]]
        kd = kopf[T].all(1)
        o["dehnung_heute"] = dehnung(V0, T, W, sk, RT, RN, kd)
        o["dehnung_neu"] = dehnung(Vn, T, W, sk, RT, RN, kd)
        for c in CLIPS:
            print("DEHNUNG %-16s heute %s | neu %s" % (c, o["dehnung_heute"][c], o["dehnung_neu"][c]), flush=True)
    os.makedirs(os.path.dirname(aus), exist_ok=True)
    json.dump(o, open(aus, "w"), indent=1)
    print("ok", aus)


# ------------------------------------------------------------------------------------------------ schnelle Ton-Vorschau (numpy, keine GPU)
def raster_ton(P, T, W, H, kam, pxm, mitte, Tn=None):
    """z-Buffer-Rasterer, orthografisch, Ton grau (Kopie der Logik aus v2/plan/proto_feld.py). kam = (az, el) Grad.
    Normalen wie baer_export_gengross.normalen (ueber gleiche Lagen verschweisst, alle Dreiecke) oder nur aus Tn."""
    az, el = np.radians(kam[0]), np.radians(kam[1])
    fwd = -np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    rechts = np.array([-np.sin(az), np.cos(az), 0.0])
    oben = np.cross(rechts, fwd)
    Q = P - mitte
    sx = Q @ rechts * pxm + W / 2
    sy = -(Q @ oben) * pxm + H / 2
    sz = Q @ fwd
    Tq = T if Tn is None else Tn
    _, wid = np.unique(np.round(P, 7), axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[Tq[:, 1]] - P[Tq[:, 0]], P[Tq[:, 2]] - P[Tq[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[Tq[:, k]], fn)
    Nn = acc[wid]
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-12)
    img = np.full((H, W), 0.25)
    zb = np.full((H, W), np.inf)
    licht = -fwd * 0.6 + np.array([0, 0, 1.0]) * 0.8 + rechts * 0.35
    licht /= np.linalg.norm(licht)
    sel = (sx[T].max(1) >= 0) & (sx[T].min(1) < W) & (sy[T].max(1) >= 0) & (sy[T].min(1) < H)
    for a, b, c in T[sel]:
        xs = np.array([sx[a], sx[b], sx[c]]); ys = np.array([sy[a], sy[b], sy[c]]); zs = np.array([sz[a], sz[b], sz[c]])
        x0, x1 = int(max(0, np.floor(xs.min()))), int(min(W - 1, np.ceil(xs.max())))
        y0, y1 = int(max(0, np.floor(ys.min()))), int(min(H - 1, np.ceil(ys.max())))
        if x1 < x0 or y1 < y0:
            continue
        den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(den) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
        l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
        l2 = 1 - l0 - l1
        ins = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        if not ins.any():
            continue
        z = l0 * zs[0] + l1 * zs[1] + l2 * zs[2]
        n = l0[..., None] * Nn[a] + l1[..., None] * Nn[b] + l2[..., None] * Nn[c]
        n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-12)
        n = np.where(((n @ fwd) > 0)[..., None], -n, n)
        sh = 0.15 + 0.85 * np.clip(n @ licht, 0, 1)
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        upd = ins & (z < sub)
        sub[upd] = z[upd]
        img[y0:y1 + 1, x0:x1 + 1][upd] = sh[upd]
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def raster_tex(P, T, UV, tex, W, H, kam, pxm, mitte, Tn=None):
    """wie raster_ton, aber mit Textur (UV je Punkt, glTF-Richtung: Bildzeile = v * Hoehe), nearest; Licht 0,35 + 0,65 Lambert."""
    az, el = np.radians(kam[0]), np.radians(kam[1])
    fwd = -np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    rechts = np.array([-np.sin(az), np.cos(az), 0.0])
    oben = np.cross(rechts, fwd)
    Q = P - mitte
    sx = Q @ rechts * pxm + W / 2
    sy = -(Q @ oben) * pxm + H / 2
    sz = Q @ fwd
    Tq = T if Tn is None else Tn
    _, wid = np.unique(np.round(P, 7), axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[Tq[:, 1]] - P[Tq[:, 0]], P[Tq[:, 2]] - P[Tq[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[Tq[:, k]], fn)
    Nn = acc[wid]
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-12)
    th, tw = tex.shape[:2]
    img = np.zeros((H, W, 3)) + np.array([0.27, 0.29, 0.27])
    zb = np.full((H, W), np.inf)
    licht = -fwd * 0.6 + np.array([0, 0, 1.0]) * 0.8 + rechts * 0.35
    licht /= np.linalg.norm(licht)
    sel = (sx[T].max(1) >= 0) & (sx[T].min(1) < W) & (sy[T].max(1) >= 0) & (sy[T].min(1) < H)
    for a, b, c in T[sel]:
        xs = np.array([sx[a], sx[b], sx[c]]); ys = np.array([sy[a], sy[b], sy[c]]); zs = np.array([sz[a], sz[b], sz[c]])
        x0, x1 = int(max(0, np.floor(xs.min()))), int(min(W - 1, np.ceil(xs.max())))
        y0, y1 = int(max(0, np.floor(ys.min()))), int(min(H - 1, np.ceil(ys.max())))
        if x1 < x0 or y1 < y0:
            continue
        den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(den) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l0 = ((ys[1] - ys[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gy - ys[2])) / den
        l1 = ((ys[2] - ys[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gy - ys[2])) / den
        l2 = 1 - l0 - l1
        ins = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
        if not ins.any():
            continue
        z = l0 * zs[0] + l1 * zs[1] + l2 * zs[2]
        sub = zb[y0:y1 + 1, x0:x1 + 1]
        upd = ins & (z < sub)
        if not upd.any():
            continue
        sub[upd] = z[upd]
        n = l0[..., None] * Nn[a] + l1[..., None] * Nn[b] + l2[..., None] * Nn[c]
        n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-12)
        n = np.where(((n @ fwd) > 0)[..., None], -n, n)
        sh = 0.35 + 0.65 * np.clip(n @ licht, 0, 1)
        uu = l0 * UV[a, 0] + l1 * UV[b, 0] + l2 * UV[c, 0]
        vv = l0 * UV[a, 1] + l1 * UV[b, 1] + l2 * UV[c, 1]
        col = tex[np.clip((vv * th).astype(int), 0, th - 1), np.clip((uu * tw).astype(int), 0, tw - 1)]
        img[y0:y1 + 1, x0:x1 + 1][upd] = (col * sh[..., None])[upd]
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def ton(kv):
    """Ton-Blatt GEN heute | NEU | 2c aus Kevins Kamera und Kopf-Ansichten -> mess/ton_<tag>.png (nur zum Ansehen, keine GPU)."""
    from PIL import Image, ImageDraw
    from fx_lib import lade_dump, Skin
    sys.path.insert(0, R + "gegen")
    from g_dump import Haut
    tag = kv.get("tag", "neu")
    basis = kv.get("basis", GA + "form/E_gg2_basis.npz")
    D = lade_dump(R + "rig/dump_2c.txt")
    B0, G0 = lade_ein()
    Bn = np.load(basis)
    sk = Skin(D, [str(n) for n in G0["namen"]])
    h2 = Haut(R + "gegen/dump_2c.txt", 0)
    W0 = G0["W"]
    kopf0 = kopfmaske(G0)
    k2 = (h2.W[:, h2.names.index("Bip01_Head")] + h2.W[:, h2.names.index("Bip01_Jaw")]) > 0.5
    ANS = [("Kevin Idle01 0", "DeerStag_Idle01", 0, (0, 30), 700), ("Kevin Eat 32", "NCBear_Eat", 32, (0, 30), 700),
           ("Kevin Walk 7", "DeerStag_Walk", 7, (0, 30), 700), ("vorn el 0", None, 0, (0, 0), 700), ("schraeg 35/10", None, 0, (35, 10), 700),
           ("Seite 90/0", None, 0, (90, 0), 700), ("oben", None, 0, (0, 89), 700), ("Spiel Idle 100px/m x3", "DeerStag_Idle01", 0, (0, 30), 100)]
    if kv.get("nah") == "1":
        ANS = [("nah vorn 0/0", None, 0, (0, 0), 1400), ("nah 30/0", None, 0, (30, 0), 1400), ("nah 55/5", None, 0, (55, 5), 1400),
               ("nah Seite 90/0", None, 0, (90, 0), 1400), ("nah unten 40/-30", None, 0, (40, -30), 1400), ("nah oben 20/50", None, 0, (20, 50), 1400)]
    zeilen = []
    for name, clip, f, kam, pxm in ANS:
        reihe = []
        haut_T = B0["T"][B0["teil_dreieck"].astype(str) == "aussen"]
        spalten = [("GEN heute", B0["V"], B0["T"], W0, kopf0, None), ("NEU", Bn["V"], Bn["T"], W0, kopf0, None), ("2c", None, h2.T, None, k2, None)]
        if kv.get("tex"):
            spalten = [("GEN heute braun", B0["V"], None, W0, kopf0, R + "fix1/tex_final/NCBearGen.png"),
                       ("NEU braun", Bn["V"], None, W0, kopf0, kv["tex"] + "/NCBearGen.png"),
                       ("NEU foto", Bn["V"], None, W0, kopf0, kv["tex"] + "/NCBearGenFoto.png"),
                       ("2c", None, None, None, k2, "C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/textures/Body/NCBear.png")]
        if kv.get("hautnormalen") == "1":
            spalten.insert(2, ("NEU Hautnormalen", Bn["V"], Bn["T"], W0, kopf0, haut_T))
        for sp, V, T, W, km, Tn in spalten:
            if sp == "2c":
                P = h2.pose(clip, f) if clip else h2.ruhe()
            else:
                P = sk.bild(V, W, clip, f) if clip else V
            if pxm >= 1000:
                mitte = np.array([1.0, 0.0, 0.66])
                Wd, Hd = 420, 360
            elif pxm >= 500:
                mitte = P[km].mean(0) + (np.array([0.06, 0, -0.03]) if kam[1] < 80 else np.array([0.06, 0, 0]))
                Wd, Hd = 400, 360
            else:
                mitte = (P.max(0) + P.min(0)) / 2
                Wd, Hd = 170, 170
            if kv.get("tex"):
                from PIL import Image as _I
                tx = np.asarray(_I.open(Tn).convert("RGB")).astype(float) / 255
                if sp == "2c":
                    im = Image.fromarray(raster_tex(P, h2.T, h2.uv, tx, Wd, Hd, kam, pxm, mitte))
                else:
                    gp = B0["glb_punkt"]
                    im = Image.fromarray(raster_tex(P[gp], B0["T_glb"], B0["UV"], tx, Wd, Hd, kam, pxm, mitte))
            else:
                im = Image.fromarray(raster_ton(P, T, Wd, Hd, kam, pxm, mitte, Tn)).convert("RGB")
            if pxm < 500:
                im = im.resize((Wd * 2, Hd * 2), Image.NEAREST)
            ImageDraw.Draw(im).text((4, 4), "%s | %s" % (name, sp), fill=(255, 255, 0))
            reihe.append(im)
        zeilen.append(reihe)
    bw = max(sum(i.size[0] for i in z) for z in zeilen)
    bh = sum(max(i.size[1] for i in z) for z in zeilen)
    blatt = Image.new("RGB", (bw, bh), (30, 30, 30))
    y = 0
    for z in zeilen:
        x = 0
        for i in z:
            blatt.paste(i, (x, y))
            x += i.size[0]
        y += max(i.size[1] for i in z)
    os.makedirs(GA + "mess", exist_ok=True)
    blatt.save(GA + "mess/ton_%s.png" % tag)
    print("ok", GA + "mess/ton_%s.png" % tag)


if __name__ == "__main__":
    cmd = sys.argv[1]
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    {"form": form, "ton": ton, "pruef": pruef}[cmd](kv)
