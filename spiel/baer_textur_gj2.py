# Lauf baer-gen-junges-v2 (12.11.2026), Bauer GESICHT: Kopf-Textur des Generator-Jungen (PLAN.md 5.2). Neu.
# Start = Textur des Bauers BEINE (beine/NCBearBenchCubGen_beine.png, 1024 RGB). Geaendert wird NUR der Kopf (Schnauze, Augen, Nase,
# Ohren, Stirn/Wangen leicht dunkler); Rumpf, Beine, Pfoten, Sohlen, Krallen und die Pfoten-Naht bleiben Texel fuer Texel gleich.
# Jede Aenderung ist eine glatte Funktion der 3D-Lage (Ruhe vor der Kopf-Umformung P0 fuer "wo am Kopf", nach der Umformung P1 fuer
# runde Augen) -> ueber UV-Naehte hinweg stetig (keine Farbspruenge an Naehten). Fell-Zeichnung bleibt: neue Farbe x (L / L_weich)
# der alten Textur; die durch die Schnauzen-Streckung (x1,4) groeber gewordene Zeichnung bekommt ein feines, deterministisches Korn dazu.
# Danach werden die geaenderten Inseln 8 px in den freien Rand ausgedehnt (Mittel der Nachbarn, wie BEINE), damit Mipmaps sauber bleiben.
# Nachbesserung 12.11. (PRUEF_OPTIK M1/M8): helle Schnauze etwas breiter (sch_quer0/1) und als "Nasenruecken" schmal zwischen die Augen
# hinauf (br_*: |y| < 1,6..4,0 cm, Anteil 0,75, bis 5,5..8,5 cm ueber die Augenhoehe, nur nach vorn gerichtete Flaechen) -- wie Foto C/Babygesicht und
# das Standard-Junge; Iris dunkler (30/20/15 statt 42/28/20) und Pupille groesser (0,52 statt 0,45 des Radius): nah keine "Glasaugen".
# Dazu (PRUEF_OPTIK M5) "Pfoten-Ton": die Std-Pfoten (ohne Krallen und Sohle) waren unten grau/blaustichig (r/L 1,10, b/L 0,96 gegen das
# Fell 1,19 / 0,82) -> unter z 0,08 m der Farbton zu 75 % auf das Fell-Verhaeltnis gezogen (Helligkeit bleibt), bis z 0,125 weich aus.
# Das ist die einzige Aenderung ausserhalb von Kopf/Hals (eigener Zaehler im Info).
# Aufruf: python baer_textur_gj2.py NETZ_GESICHT.npz START.png AUS.png INFO.json [k=v,...]
# Statisch/offline, deterministisch, nicht gespielt.
import json
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_kopf_gj2 as K  # noqa: E402

PAR = dict(
    # Schnauze (warmes Hellbraun, Ziel-RGB vor der Fell-Zeichnung) und Rand (Meter, P0)
    sch_r=150.0, sch_g=124.0, sch_b=100.0, sch_vorn0=-0.012, sch_vorn1=0.030, sch_oben0=-0.030, sch_oben1=0.010,
    sch_quer0=0.048, sch_quer1=0.094, sch_korn=0.05,
    # Nasenruecken (Nachbesserung 12.11.): Anteil der Schnauzenfarbe, Halbbreite voll/aus, Hoehe ueber den Augen voll/aus (P0, Meter)
    br_staerke=0.75, br_halb0=0.016, br_halb1=0.040, br_oben0=0.055, br_oben1=0.085, br_unten=-0.035,
    # Lippenlinie (fein, dunkel) und Kinn
    lippe_dunkel=0.45, lippe_breite=0.0035,
    # Stirn/Wangen/Kopf leicht dunkler (Faktor), Uebergang ueber das Kopf-Gewicht (Hals)
    kopf_faktor=0.90,
    # Augen: Radius-Faktor gegen das alte Auge, Farben
    auge_faktor=1.25, auge_glanz=1, pupille=0.52, iris_r=30.0, iris_g=20.0, iris_b=15.0,
    # Nase
    nase_faktor=0.70,
    # Ohren: Kern dunkel (Anteil des Radius), Rand hell (L-Aufschlag gegen die Stirn)
    ohr_kern=0.42, ohr_kern_L=40.0, ohr_rand_plus=16.0, ohr_korn=0.14,
    # Pfoten-Ton (Nachbesserung 12.11.): Anteil, Hoehe voll/aus (Ruhe z, m)
    pf_staerke=0.75, pf_z0=0.08, pf_z1=0.125,
)


def sst(a, b, x):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def lum(c):
    return c @ np.array([0.299, 0.587, 0.114])


def uv_raster(UV, T, n=1024):
    """Texel -> Dreieck (tid, -1 = frei) und Baryzentren b1/b2 (Texelmitte (i+0,5)/n; glTF v von oben wie die Textur-Zeilen)"""
    X = UV[:, 0] * n
    Y = UV[:, 1] * n
    tid = np.full((n, n), -1, np.int64)
    b1 = np.zeros((n, n))
    b2 = np.zeros((n, n))
    for t, (i, j, k) in enumerate(T):
        xa, ya, xb, yb, xc, yc = X[i], Y[i], X[j], Y[j], X[k], Y[k]
        mnx, mxx = int(max(0, math.floor(min(xa, xb, xc)))), int(min(n - 1, math.ceil(max(xa, xb, xc))))
        mny, mxy = int(max(0, math.floor(min(ya, yb, yc)))), int(min(n - 1, math.ceil(max(ya, yb, yc))))
        den = (yb - yc) * (xa - xc) + (xc - xb) * (ya - yc)
        if abs(den) < 1e-12 or mxx < mnx or mxy < mny:
            continue
        gx, gy = np.meshgrid(np.arange(mnx, mxx + 1) + 0.5, np.arange(mny, mxy + 1) + 0.5)
        l1 = ((yb - yc) * (gx - xc) + (xc - xb) * (gy - yc)) / den
        l2 = ((yc - ya) * (gx - xc) + (xa - xc) * (gy - yc)) / den
        l3 = 1 - l1 - l2
        ins = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        sub = tid[mny:mxy + 1, mnx:mxx + 1]
        frei = ins & (sub < 0)
        sub[frei] = t
        b1[mny:mxy + 1, mnx:mxx + 1][frei] = l1[frei]
        b2[mny:mxy + 1, mnx:mxx + 1][frei] = l2[frei]
    return tid, b1, b2


def merkmal(A, T, tid, b1, b2):
    m = tid >= 0
    tt = T[tid[m]]
    l1, l2 = b1[m][:, None], b2[m][:, None]
    A = A.reshape(len(A), -1).astype(float)
    return l1 * A[tt[:, 0]] + l2 * A[tt[:, 1]] + (1 - l1 - l2) * A[tt[:, 2]]


def weich(img, r):
    """Kastenfilter (2r+1) zweimal = weicher Tiefpass (nur numpy), Rand gespiegelt"""
    out = img.astype(float)
    for _ in range(2):
        for ax in (0, 1):
            p = np.pad(out, [(r, r) if a == ax else (0, 0) for a in range(out.ndim)], mode="reflect")
            c = np.cumsum(p, axis=ax)
            c = np.concatenate([np.zeros_like(np.take(c, [0], axis=ax)), c], axis=ax)
            n = out.shape[ax]
            out = (np.take(c, np.arange(2 * r + 1, n + 2 * r + 1), axis=ax) - np.take(c, np.arange(0, n), axis=ax)) / (2 * r + 1)
    return out


def korn(n, seed=7):
    """deterministisches feines Korn (Wert-Rauschen aus einer festen Hash-Folge), Mittel 0, Std 1"""
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    h = np.sin(i * 12.9898 + j * 78.233 + seed * 37.719) * 43758.5453
    h = h - np.floor(h)
    h = h + 0.5 * np.roll(h, 1, axis=1) + 0.5 * np.roll(h, -1, axis=1)     # kurze waagerechte Striche (Fell)
    h = (h - h.mean()) / h.std()
    return h


def baue(netz, start, aus, info_aus, kv=""):
    P = dict(PAR)
    if kv:
        for k_v in kv.split(","):
            k, v = k_v.split("=")
            P[k] = float(v)
    N = np.load(netz)
    gp, T, UV = N["glb_punkt"], N["T_glb"], N["UV"]
    tex0 = np.asarray(Image.open(start).convert("RGB")).astype(float)
    n = tex0.shape[0]
    tid, b1, b2 = uv_raster(UV, T, n)
    bel = tid >= 0
    P0 = merkmal(N["V_vor_kopf"][gp], T, tid, b1, b2)
    P1 = merkmal(N["V"][gp], T, tid, b1, b2)
    wk = merkmal(N["w_kopf"][gp], T, tid, b1, b2)[:, 0]
    ohr = {o: merkmal(N[o][gp].astype(float), T, tid, b1, b2)[:, 0] for o in ("ohr_l", "ohr_r")}
    # weiche Ohr-Maske fuer die Farbe (Punkt-Maske 6 Runden ueber die Kanten gemittelt): kein harter Farbrand am Ohransatz
    Ek = K.kanten(N["T"])
    ohr_w = {}
    for o in ("ohr_l", "ohr_r"):
        mv = N[o].astype(float)
        for _ in range(6):
            acc = np.zeros_like(mv)
            cnt = np.zeros_like(mv)
            np.add.at(acc, Ek[:, 0], mv[Ek[:, 1]])
            np.add.at(acc, Ek[:, 1], mv[Ek[:, 0]])
            np.add.at(cnt, Ek[:, 0], 1)
            np.add.at(cnt, Ek[:, 1], 1)
            mv = 0.5 * mv + 0.5 * acc / cnt
        ohr_w[o] = merkmal(mv[gp], T, tid, b1, b2)[:, 0]
    Vn = K.normalen(N["V"], N["T"])
    N1 = merkmal(Vn[gp], T, tid, b1, b2)
    N1 /= np.linalg.norm(N1, axis=1, keepdims=True) + 1e-12
    lm = K.landmarken(N["V_vor_kopf"])
    L0 = {k: N["V_vor_kopf"][i] for k, i in lm.items()}
    L1 = {k: N["V"][i] for k, i in lm.items()}
    col = tex0[bel].copy()                       # Farben der belegten Texel (Reihenfolge = bel)
    Lc = lum(col)
    # Fell-Zeichnung: L / L_weich (weicher Tiefpass ueber die Insel, freie Texel mit Nachbarn gefuellt)
    Lt = lum(tex0)
    Lw = weich(np.where(bel, Lt, np.nan_to_num(np.where(bel, Lt, 0))), 6)
    Bw = weich(bel.astype(float), 6)
    Lw2 = weich(np.where(bel, Lt, 0.0), 6) / np.maximum(Bw, 1e-3)
    detail = np.clip(Lt / np.maximum(Lw2, 1.0), 0.55, 1.6)[bel]
    info = dict(par=P, texel_belegt=int(bel.sum()))
    x0, y0, z0 = P0[:, 0], P0[:, 1], P0[:, 2]
    am0 = 0.5 * (L0["auge_l"] + L0["auge_r"])
    kopf = wk > 0.5
    neu = col.copy()
    # ---- 1. Kopf leicht dunkler (Stirn, Wangen, Hinterkopf), ueber das Kopf-Gewicht in den Hals auslaufend
    fk = 1.0 - (1.0 - P["kopf_faktor"]) * sst(0.3, 0.95, wk)
    neu *= fk[:, None]
    # ---- 2. Schnauze hell (warm), weicher Rand; Kinn hell; feines Korn
    m_s = (sst(am0[0] + P["sch_vorn0"], am0[0] + P["sch_vorn1"], x0) * (1 - sst(am0[2] + P["sch_oben0"], am0[2] + P["sch_oben1"], z0))
           * (1 - sst(P["sch_quer0"], P["sch_quer1"], np.abs(y0))) * sst(0.6, 0.95, wk))
    ziel = np.array([P["sch_r"], P["sch_g"], P["sch_b"]])
    kn = korn(n)[bel]
    # Zeichnung in der Schnauze eng begrenzt (0,8..1,25): das alte dunkle Nasenpolster/alte Spruenge sollen nicht als Flecken durchschlagen
    d_s = np.clip(detail, 0.8, 1.25) * (1.0 + P["sch_korn"] * kn)
    sch_col = ziel[None, :] * d_s[:, None]
    neu = neu * (1 - m_s[:, None]) + sch_col * m_s[:, None]
    info["schnauze_texel"] = dict(voll=int((m_s > 0.95).sum()), rand=int(((m_s > 0.05) & (m_s <= 0.95)).sum()))
    # ---- 2b. Nasenruecken: helle Zone schmal zwischen die Augen hinauf (nur nach vorn gerichtete Flaechen des Kopfes), weicher Rand
    if P["br_staerke"] > 0:
        vorn_w = sst(0.15, 0.45, N1[:, 0])
        m_b = ((1 - sst(P["br_halb0"], P["br_halb1"], np.abs(y0))) * sst(am0[2] + P["br_unten"], am0[2] + P["br_unten"] + 0.02, z0)
               * (1 - sst(am0[2] + P["br_oben0"], am0[2] + P["br_oben1"], z0)) * vorn_w * sst(0.6, 0.95, wk)) * P["br_staerke"]
        m_b = np.maximum(m_b - m_s, 0.0)                       # nur, wo die Schnauze nicht schon hell ist
        neu = neu * (1 - m_b[:, None]) + sch_col * m_b[:, None]
        info["nasenruecken_texel"] = dict(ueber_halb=int((m_b > 0.3).sum()), rand=int(((m_b > 0.05) & (m_b <= 0.3)).sum()))
    # ---- 3. Nase: schwarz, Nasenloecher dunkler, kleiner Glanz oben
    nase0 = L0["nasenspitze"]
    # Nasenpolster als 3D-Ellipse um die Nasenspitze (P0), angepasst an das alte dunkle Polster (L < 50: quer +-2,9 cm, hoch +-2,2 cm,
    # bis 1,5 cm hinter die Spitze) -> beide Seiten einer UV-Naht bekommen dieselbe Farbe (vorher Texel-Schwelle L < 60: Spruenge)
    dn3 = P0 - nase0
    e_n = np.sqrt((dn3[:, 1] / 0.0295) ** 2 + (dn3[:, 2] / 0.0225) ** 2)
    mn_w = (1 - sst(0.90, 1.08, e_n)) * sst(-0.028, -0.016, dn3[:, 0]) * kopf
    nase_col = np.array([30.0, 27.0, 29.0])[None, :] * np.clip(detail, 0.8, 1.2)[:, None] * P["nase_faktor"] / 0.70
    for sy_ in (1.0, -1.0):        # Nasenloecher: vorn unten an der Nase
        loch = nase0 + np.array([-0.004, sy_ * 0.013, -0.010])
        dl = np.linalg.norm(P0 - loch, axis=1)
        nase_col *= (1 - 0.55 * (1 - sst(0.004, 0.008, dl)))[:, None]
    glanz = nase0 + np.array([-0.012, 0.0, 0.016])
    dg = np.linalg.norm(P0 - glanz, axis=1)
    nase_col += (38.0 * (1 - sst(0.003, 0.010, dg)))[:, None]
    neu = neu * (1 - mn_w[:, None]) + nase_col * mn_w[:, None]
    info["nase_texel"] = int((mn_w > 0.5).sum())
    # ---- 4. Lippenlinie (fein): Mittelrinne unter der Nase bis zum Maul, Maullinie seitlich nach hinten (P0, auf der Schnauze)
    kinn0 = L0["kinn"]
    z_maul = kinn0[2] + 0.35 * (nase0[2] - kinn0[2])
    unter_nase = (z0 < nase0[2] - 0.016) & (z0 > z_maul) & (x0 > nase0[0] - 0.05)
    l_mitte = (1 - sst(P["lippe_breite"] * 0.5, P["lippe_breite"] * 1.5, np.abs(y0))) * unter_nase
    # Maullinie: z = z_maul + 0,25 * |y| (Mundwinkel leicht hoch), von |y| 0 bis 0,04, nur vorn auf der Schnauze
    zl = z_maul + 0.25 * np.abs(y0)
    l_maul = (1 - sst(P["lippe_breite"] * 0.5, P["lippe_breite"] * 1.5, np.abs(z0 - zl))) * (1 - sst(0.032, 0.042, np.abs(y0))) \
        * (x0 > nase0[0] - 0.075)
    m_l = np.maximum(l_mitte, l_maul) * m_s * (1 - mn_w)
    neu *= (1 - P["lippe_dunkel"] * m_l)[:, None]
    info["lippe_texel"] = int((m_l > 0.5).sum())
    # ---- 5. Augen: neu malen (runde Scheibe in der Lage NACH der Umformung), Radius = alter Radius x auge_faktor
    info["augen"] = {}
    oben = np.array([math.sin(math.radians(8.0)) * -1.0, 0.0, math.cos(math.radians(8.0))])  # Kopf-oben nach dem Heben
    for s, nm in (("l", "auge_l"), ("r", "auge_r")):
        c1 = L1[nm]
        d1 = np.linalg.norm(P1 - c1, axis=1)
        nah = (d1 < 0.03) & kopf
        dunkel = nah & (Lc < 30)
        c = P1[dunkel].mean(0) if dunkel.sum() >= 3 else c1
        d1 = np.linalg.norm(P1 - c, axis=1)
        # altes Auge = Pupille (L < 30) + Iris (rotbraun: R-B > 30, L < 62) innerhalb 2,2 cm; Fell daneben hat R-B ~25
        iris = (d1 < 0.022) & kopf & (((Lc < 62) & ((col[:, 0] - col[:, 2]) > 30)) | (Lc < 30))
        r_alt = float(np.percentile(d1[iris], 95)) if iris.sum() > 5 else 0.014
        R = r_alt * P["auge_faktor"]
        r = d1 / R
        # Profil: Pupille schwarz, Iris sehr dunkelbraun, dunkler Limbus/Lidrand, weicher Uebergang ins (abgedunkelte) Fell
        pup = np.array([10.0, 8.0, 8.0])
        iri = np.array([P["iris_r"], P["iris_g"], P["iris_b"]])
        lim = np.array([16.0, 12.0, 11.0])
        a_c = np.where(r[:, None] < P["pupille"], pup, np.where(r[:, None] < 0.80, iri * (0.9 + 0.25 * (r[:, None] - P["pupille"])), lim))
        w_a = 1 - sst(0.97, 1.08, r)
        lid = (1 - sst(1.0, 1.45, r)) * (r >= 0.97)
        neu_a = neu * (1 - 0.45 * lid)[:, None]
        neu_a = neu_a * (1 - w_a[:, None]) + a_c * w_a[:, None]
        sel = nah | (r < 1.6)
        neu[sel] = neu_a[sel]
        # Glanzpunkt: 1-2 Texel oben-vorn in der Iris
        g = c + R * 0.42 * (0.80 * oben + 0.60 * np.array([math.cos(math.radians(8)), 0, math.sin(math.radians(8))]))
        dg = np.linalg.norm(P1 - g, axis=1)
        ig = np.argsort(dg)[:max(1, int(P["auge_glanz"]))] if P["auge_glanz"] > 0 else []
        for i in ig:
            neu[i] = (215.0, 210.0, 205.0)
        info["augen"][nm] = dict(mitte=[round(float(v), 4) for v in c], r_alt_cm=round(100 * r_alt, 2), r_neu_cm=round(100 * R, 2),
                                 texel=int((r < 1.0).sum()), glanz_texel=len(ig))
    # ---- 6. Ohren: Muschel (Vorderseite) mit dunklem Kern und hellem Rand, Rueckseite wie die Stirn
    stirn = kopf & (z0 > am0[2] + 0.03) & (x0 > 0.45) & (np.abs(y0) < 0.1) & (ohr["ohr_l"] < 0.5) & (ohr["ohr_r"] < 0.5)
    L_stirn = float(np.median(lum(neu[stirn])))
    info["stirn_L"] = round(L_stirn, 1)
    info["ohren"] = {}
    for o in ("ohr_l", "ohr_r"):
        om = ohr[o] > 0.5
        po = P1[om]
        # Oeffnungsachse = mittlere Normale der nach vorn/aussen zeigenden Haelfte, Mitte = Schwerpunkt der Ohrpunkte
        sg = 1.0 if o == "ohr_l" else -1.0
        nn = N1[om]
        vor = nn @ np.array([0.75, sg * 0.66, 0.0]) > 0.15
        ax_ = nn[vor].mean(0)
        ax_ /= np.linalg.norm(ax_)
        mitte = po.mean(0)
        rel = P1 - mitte
        quer = rel - (rel @ ax_)[:, None] * ax_[None, :]
        rq = np.linalg.norm(quer, axis=1)
        Rm = float(np.percentile(rq[om], 97))
        rn = rq / Rm
        vorn = sst(-0.30, 0.30, N1 @ ax_)          # weich ueber den Muschelrand (Vorder-/Rueckseite liegen auf eigenen UV-Inseln)
        # Kern: weich dunkel, Rand: heller als die Stirn (+ohr_rand_plus), Rueckseite: nicht heller als die Stirn
        kern_w = (1 - sst(P["ohr_kern"] - 0.15, P["ohr_kern"] + 0.12, rn)) * vorn * om
        oben_k = np.array([-math.sin(math.radians(8.0)), 0.0, math.cos(math.radians(8.0))])
        rand_w = sst(P["ohr_kern"] + 0.20, P["ohr_kern"] + 0.45, rn) * vorn * om * sst(-0.25, 0.30, (rel @ oben_k) / Rm)  # heller Rand nur oben
        hinten_w = (1 - vorn) * om
        Lo = lum(neu)
        f_k = np.clip(P["ohr_kern_L"] / np.maximum(Lo, 1), 0.2, 1.0)
        f_r = np.clip((L_stirn + P["ohr_rand_plus"]) / np.maximum(Lo, 1), 0.6, 1.8)
        f_h = np.clip(L_stirn / np.maximum(Lo, 1), 0.5, 1.0)
        fo = np.ones(len(neu))
        fo = fo * (1 - kern_w) + f_k * kern_w
        fo = fo * (1 - rand_w) + f_r * rand_w
        fo = fo * (1 - hinten_w) + np.minimum(fo, f_h) * hinten_w
        fo = fo * (1.0 + P["ohr_korn"] * kn)        # feines Fell-Korn (die Generator-Muschel ist glatt wie Plastik)
        # weicher Uebergang am Ohransatz: Ohr-Maske (Gewicht) als Mischung
        mo = np.clip(ohr_w[o], 0, 1)
        neu = neu * (1 - mo[:, None]) + (neu * fo[:, None]) * mo[:, None]
        info["ohren"][o] = dict(achse=[round(float(v), 3) for v in ax_], R_cm=round(100 * Rm, 2),
                                kern_anteil_ohr=round(float((kern_w[om] > 0.5).sum() / om.sum()), 3),
                                rand_L=round(float(np.median(lum(neu[om & (rand_w > 0.5)]))), 1) if (om & (rand_w > 0.5)).any() else None,
                                kern_L=round(float(np.median(lum(neu[om & (kern_w > 0.5)]))), 1) if (om & (kern_w > 0.5)).any() else None,
                                hinten_L=round(float(np.median(lum(neu[om & (hinten_w > 0.5)]))), 1))
    # ---- 7. Pfoten-Ton (Nachbesserung 12.11., M5): Std-Pfoten ohne Krallen/Sohle, Farbton zum Fell-Verhaeltnis des Beins darueber
    m_pf = np.zeros(len(neu))
    if P["pf_staerke"] > 0:
        teil = merkmal(N["teil"][gp].astype(float), T, tid, b1, b2)[:, 0]
        krs = merkmal((N["kralle"] | N["sohle"])[gp].astype(float), T, tid, b1, b2)[:, 0]
        std = (teil > 0.5) & (krs < 0.5)
        fell = (teil < 0.5) & (P0[:, 2] > 0.14) & (P0[:, 2] < 0.26) & (wk < 0.01)
        cf = col[fell].mean(0)
        verh = cf / lum(cf)
        m_pf = std * (1 - sst(P["pf_z0"], P["pf_z1"], P0[:, 2])) * P["pf_staerke"]
        Lp = lum(neu)
        neu = neu * (1 - m_pf[:, None]) + (Lp[:, None] * verh[None, :]) * m_pf[:, None]
        info["pfoten_ton"] = dict(texel=int((m_pf > 0.05).sum()), fell_verhaeltnis=[round(float(v), 3) for v in verh])
    # ---- nur Kopf/Hals (und die Pfoten-Tonung) geaendert? Rumpf/Beine sonst Texel fuer Texel gleich
    neu = np.clip(np.round(neu), 0, 255)
    aend = np.abs(neu - col).max(1) > 0
    info["geaendert_texel"] = int(aend.sum())
    info["geaendert_pfoten_ton"] = int((aend & (m_pf > 0)).sum())
    info["geaendert_ausserhalb_kopf_hals"] = int((aend & (wk < 0.01) & (m_pf <= 0)).sum())
    out = tex0.copy()
    out[bel] = neu
    # ---- freie Texel neben geaenderten Inseln: 8 Runden Mittel der belegten/gefuellten Nachbarn (nur dort, wo ein Nachbar geaendert ist)
    ch = np.zeros((n, n), bool)
    ch[bel] = aend
    gef = bel.copy()
    for _ in range(8):
        acc = np.zeros((n, n, 3))
        cnt = np.zeros((n, n))
        q = np.zeros((n, n), bool)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            src = np.roll(np.roll(gef & ch, dy, 0), dx, 1)
            acc += np.roll(np.roll(out * (gef & ch)[..., None], dy, 0), dx, 1)
            cnt += src
            q |= src
        neu_t = q & ~gef
        out[neu_t] = acc[neu_t] / cnt[neu_t][:, None]
        gef |= neu_t
        ch |= neu_t
    info["rand_gefuellt_texel"] = int((gef & ~bel).sum())
    out = np.clip(np.round(out), 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGB").save(aus, optimize=False)
    json.dump(info, open(info_aus, "w"), indent=1)
    print("TEXTUR", json.dumps(info)[:1500])
    return info


if __name__ == "__main__":
    baue(*sys.argv[1:5], kv=sys.argv[5] if len(sys.argv) > 5 else "")
