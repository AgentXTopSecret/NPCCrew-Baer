# Lauf baer-rig-junges (11.11.2026), Rolle SKELETT+GEWICHTE: Hautgewichte des Generator-Jungen C (RIG_PLAN.md Abschnitt 4).
# Teil "opt" ist eine Kopie von baer_gewichte_2c.py (Original unveraendert, Zeilenenden CRLF wie dort); entfernt: Kopf-/Krallen-
# Uebernahme aus alten Netzen (KOPF_ALT, alt_von, k1_dy, k2c_dx); Zonen/Schwellen/Regionen in GELENK-Koordinaten des Jungen statt
# fester Erwachsenen-Hoehen; frei sind nur Rumpf, Hals, Achsel, Leiste und Bein-Uebergaenge (Kopf mit Ohren starr = Head 1,0, Pfoten
# starr, Krallen 1,0, Stummel). Teil "formel" ist neu (Formel in Gelenk-Koordinaten + Raumglaettung), Teil "dehnung" misst.
#
# Aufrufe (Pfade absolut; NETZ = rig/skelett/netz_rig.npz, SK = rig/skelett/skelett_rig.json):
#   python baer_gewichte_rig.py formel NETZ SK AUS_FORMEL.npz          -> W (Formel), namen, Masken, gegend, regionen (je Dreieck)
#   python baer_gewichte_rig.py opt FORMEL.npz DUMP.pkl AUS.npz [k=v,...]  (Optimierer; ~20 min CPU, im Hintergrund starten)
#   python baer_gewichte_rig.py dehnung GEWICHTE.npz DUMP.pkl [AUS.json]   (Dehnung je Clip: p99,5 / max sigma1, Achsel/Brust, Falten)
#   python baer_gewichte_rig.py abgabe OPT.npz AUS_ORDNER                  -> gewichte_rig.npz, regionen_rig.npz
# Die Rolle CLIPS ruft "opt" mit dem Dump der fertigen 15 Clips noch einmal auf (RIG_PLAN 5.6), sonst unveraendert.
# Rahmen: tier-Meter (x vorn, y links, z oben) im SKELETTRAHMEN; Dump-Raum = (y, z, -x) * 0,544.
# Statisch/offline gerechnet, nicht gespielt. Schreibt nur unter _arbeit/baer_gen/rig/.
import json
import os
import pickle
import sys
import time

import numpy as np

T0 = time.time()
M2U = 0.544
CLIPS = ["DeerStag_Idle01", "DeerStag_Walk", "DeerStag_Run", "DeerStag_Death", "DeerStag_Dead", "NCBear_Rear", "NCBear_SwipeL",
         "NCBear_SwipeR", "NCBear_Slam", "NCBear_Bite", "NCBear_Maul", "NCBear_Eat", "NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp"]
REG_NAMEN = ["sonst", "achsel", "brust", "leiste", "hals", "kopf", "ohr", "pfote", "kralle", "stummel", "bauch"]
TORSO = ["Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head", "Bip01_Tail"]


def log(*a):
    print("GEW %.1fs" % (time.time() - T0), *a, flush=True)


def sst(a, b, x):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def raum_glatt(X, werte, sigma, block=400, Xq=None):
    """Raeumliches Gauss-Mittel von werte (n x k) ueber die Punkte X (aus baer_form_junges.py); Xq: Anfragepunkte (Vorgabe X)."""
    Xq = X if Xq is None else Xq
    out = np.zeros((len(Xq), werte.shape[1]), dtype=float)
    x2 = (X ** 2).sum(1)
    for a in range(0, len(Xq), block):
        Q = Xq[a:a + block]
        d2 = (Q ** 2).sum(1)[:, None] - 2.0 * Q @ X.T + x2[None, :]
        g = np.exp(-np.maximum(d2, 0.0) / (2.0 * sigma * sigma))
        out[a:a + block] = (g @ werte) / g.sum(1)[:, None]
    return out


def ketten_projektion(P, J):
    """Projektion der Punkte P auf die Polylinie J (k x 3): Lauf-Parameter s (Meter ab J[0]) und Abstand r."""
    best_r = np.full(len(P), np.inf)
    best_s = np.zeros(len(P))
    s0 = 0.0
    for a, b in zip(J[:-1], J[1:]):
        ab = b - a
        L = float(np.linalg.norm(ab))
        t = np.clip(((P - a) @ ab) / (L * L), 0.0, 1.0)
        r = np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
        m = r < best_r
        best_r[m] = r[m]
        best_s[m] = s0 + t[m] * L
        s0 += L
    return best_s, best_r


def achse_bei_z(J, z):
    """Lage (x, |y|) der Beinachse (Polylinie J von oben nach unten) auf Hoehe z; oberhalb/unterhalb senkrecht verlaengert."""
    zs, xs, ys = J[::-1, 2], J[::-1, 0], np.abs(J[::-1, 1])
    return np.interp(z, zs, xs), np.interp(z, zs, ys)


def cot_kanten(V, T):
    """Kotangens-Gewichte je Kante (i < j): w = 0,5 (cot a + cot b), nach unten begrenzt (positiv definit)."""
    I, J, Wt = [], [], []
    for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        u = V[T[:, b]] - V[T[:, a]]
        v = V[T[:, c]] - V[T[:, a]]
        cot = (u * v).sum(1) / np.maximum(np.linalg.norm(np.cross(u, v), axis=1), 1e-12)
        I.append(T[:, b]); J.append(T[:, c]); Wt.append(0.5 * cot)
    I, J, Wt = np.concatenate(I), np.concatenate(J), np.concatenate(Wt)
    lo, hi = np.minimum(I, J), np.maximum(I, J)
    key = lo.astype(np.int64) * len(V) + hi
    u_, inv = np.unique(key, return_inverse=True)
    w = np.bincount(inv, weights=Wt)
    w = np.maximum(w, 0.05 * np.median(w[w > 0]))
    return (u_ // len(V)).astype(np.int64), (u_ % len(V)).astype(np.int64), w


def harmonisch(V, T, fest, wert, iter_max=4000, tol=1e-10):
    """Loest Laplace(h) = 0 auf den freien Punkten (fest: Dirichlet-Werte 'wert'); CG ohne scipy."""
    I, J, w = cot_kanten(V, T)
    n = len(V)
    deg = np.bincount(I, weights=w, minlength=n) + np.bincount(J, weights=w, minlength=n)
    frei = ~fest
    h = np.where(fest, wert, 0.0)

    def Lmal(x):                       # (L x)_i = deg_i x_i - sum_j w_ij x_j
        y = deg * x
        y -= np.bincount(I, weights=w * x[J], minlength=n) + np.bincount(J, weights=w * x[I], minlength=n)
        return y
    b = -Lmal(np.where(fest, wert, 0.0))
    b[fest] = 0.0
    x = np.zeros(n)
    r = b.copy()
    p = r.copy()
    rr = r @ r
    for it in range(iter_max):
        Ap = Lmal(np.where(frei, p, 0.0))
        Ap[fest] = 0.0
        a = rr / max(p @ Ap, 1e-300)
        x += a * p
        r -= a * Ap
        rr2 = r @ r
        if rr2 < tol * max(b @ b, 1e-300):
            break
        p = r + (rr2 / rr) * p
        rr = rr2
    h[frei] = x[frei]
    log("HARMONISCH frei %d, Iterationen %d, Rest %.2e, Bereich %.3f..%.3f" % (int(frei.sum()), it + 1, rr2, h[frei].min(), h[frei].max()))
    return np.clip(h, 0.0, 1.0)


# =================================================================================================================================
# FORMEL
# =================================================================================================================================
def formel(netz, skj, aus):
    N = np.load(netz)
    sk = json.load(open(skj))
    V, T = N["V"].astype(np.float64), N["T"]
    vx = float(N["versatz_x"])
    namen = sk["namen"]
    pos = {k: np.array(v) for k, v in sk["ruhe_m"].items()}
    n = len(V)
    x, y, z = V[:, 0], V[:, 1], V[:, 2]
    ay = np.abs(y)
    W = {nm: np.zeros(n) for nm in namen}
    # ---- Beine: Kette, Zugehoerigkeit, Knochen je Lauf-Parameter
    x_mitte = 0.5 * (pos["Bip01_L_Thigh"][0] + pos["Bip01_L_UpperArm"][0])
    hand_dir = pos["Bip01_L_Hand"] - pos["Bip01_L_Forearm"]
    erw_hand = np.array(sk["ruhe_m_erw"]["Bip01_L_Hand"]) - np.array(sk["ruhe_m_erw"]["Bip01_L_Forearm"])
    # Vorderpfote: Handachse des Erwachsenen (Ruhe, y-Achse des Hand-Knochens) -> Richtung Handgelenk -> Zehen
    hand_y = np.array((0.944, -0.059, -0.325))
    m_bein = {}
    teil = {}
    # Schritt / Brustbein: Hoehe, bei der linkes und rechtes Bein in der Mittelebene zusammenlaufen (tiefster Mittelpunkt je Haelfte)
    mid0 = ay < 0.008
    z_kreuz = {"H": float(z[mid0 & (x < x_mitte)].min()), "V": float(z[mid0 & (x > x_mitte) & (x < pos["Bip01_L_UpperArm"][0] + 0.12)].min())}
    for s_, sy in (("L", 1.0), ("R", -1.0)):
        seite = (y >= 0) if s_ == "L" else (y < 0)
        for art in ("V", "H"):
            if art == "H":
                J = np.array([pos["Bip01_%s_%s" % (s_, k)] for k in ("Thigh", "Calf", "Foot", "Toe0")])
                kn = ("Bip01_%s_Thigh" % s_, "Bip01_%s_Calf" % s_, "Bip01_%s_Foot" % s_)
                zA, zB, r0, r1 = 0.44, 0.84, 0.13, 0.27
                vorne_streng = 1.5     # zum Bauch (vorn) strenger
                hinten = 0.9
                zu0, zu1 = 0.28, 0.40   # darunter alles Bein (Schritt bei z 0,34)
                halb = sst(x_mitte + 0.05, x_mitte - 0.05, x)
                zj = pos["Bip01_%s_Foot" % s_][2]
            else:
                ende = pos["Bip01_%s_Hand" % s_] + 0.10 * hand_y * np.array((1, sy, 1))
                J = np.array([pos["Bip01_%s_UpperArm" % s_], pos["Bip01_%s_Forearm" % s_], pos["Bip01_%s_Hand" % s_], ende])
                kn = ("Bip01_%s_UpperArm" % s_, "Bip01_%s_Forearm" % s_, "Bip01_%s_Hand" % s_)
                zA, zB, r0, r1 = 0.40, 0.78, 0.12, 0.25
                zu0, zu1 = 0.36, 0.46   # Vorderbeine bis z 0,42 getrennt
                halb = sst(x_mitte - 0.05, x_mitte + 0.05, x)
                zj = pos["Bip01_%s_Hand" % s_][2]
            ax_x, ax_y = achse_bei_z(J[:3], z)
            dxa = x - ax_x
            if art == "H":
                dxa = dxa * np.where(dxa > 0, vorne_streng, hinten)
            else:
                dxa = dxa * np.where(dxa < 0, 1.5, 1.0)
            dya = ay - ax_y
            dya = dya * np.where(dya < 0, 1.5, 0.75)
            r = np.sqrt(dxa ** 2 + dya ** 2)
            m_d = (1.0 - sst(zA, zB, z)) * (1.0 - sst(r0, r1, r))
            m_u = 1.0 - sst(zu0, zu1, z)
            # Schritt-/Brustbein-Regel: an der Linie, an der die Beine zusammenlaufen, nur Rumpf; Bein-Anteil waechst ueber 12 cm
            dc = np.sqrt(y ** 2 + np.maximum(z_kreuz[art] - z, 0.0) ** 2)
            kreuz = sst(0.0, 0.12, dc)
            m = (1.0 - (1.0 - m_d) * (1.0 - m_u)) * kreuz * halb * seite
            s, _ = ketten_projektion(V, J)
            L1 = float(np.linalg.norm(J[1] - J[0]))
            oben = 1.0 - sst(L1 - 0.035, L1 + 0.035, s)
            # Pfote: unter dem Hand-/Sprunggelenk >= 0,99, Uebergang bis 8,5 cm darueber (RIG_PLAN 4.1: >= 0,95 unter der Gelenkhoehe)
            pfote = 1.0 - sst(zj - 0.005, zj + 0.085, z)
            unten = (1.0 - oben) * (1.0 - pfote)
            oben = oben * (1.0 - pfote)
            m_bein[s_ + art] = m
            teil[s_ + art] = (kn, oben, unten, pfote)
    msum = sum(m_bein.values())
    sk_ = np.maximum(msum, 1.0)
    for k in m_bein:
        m_bein[k] = m_bein[k] / sk_
    msum = sum(m_bein.values())
    for k, (kn, o, u, p) in teil.items():
        W[kn[0]] += m_bein[k] * o
        W[kn[1]] += m_bein[k] * u
        W[kn[2]] += m_bein[k] * p
    rumpf = 1.0 - msum
    # ---- Rumpf entlang der Wirbelsaeule (Breite 0,12 um die Gelenke)
    xs, xs1 = pos["Bip01_Spine"][0], pos["Bip01_Spine1"][0]
    # Breite 0,20 (Plan 0,12): Lauf 1 zeigte im Rear (Ruecken ueberstreckt) eine scharfe Querfalte am Lendenuebergang
    p_sp = sst(xs - 0.10, xs + 0.10, x)
    p_ch = sst(xs1 - 0.10, xs1 + 0.10, x)
    # ---- Hals/Kopf: Ebene durch den Atlas, Normale = Senkrechte auf die Linie Nacken (hinter dem Ohr) -> Kehlfalte
    A, C7 = pos["Bip01_Head"], pos["Bip01_Neck"]
    ohr = N["ohr_l"] | N["ohr_r"]
    ohr_hinten = V[ohr, 0].min()
    mid = (ay < 0.012)
    oben_m = mid & (np.abs(x - ohr_hinten) < 0.012)
    nacken = np.array((ohr_hinten, 0.0, V[oben_m, 2].max()))
    # Kehlfalte: Punkt der vorderen Unterlinie (Mittelebene) zwischen Brust und Kinn mit dem kleinsten x + 0,5 (z - z0)
    km = mid & (x > A[0] - 0.08) & (x < A[0] + 0.20) & (z > 0.60) & (z < 0.82) & (z < A[2] - 0.10)
    # unterste Linie: je x-Streifen der tiefste Punkt, dann die konkavste Stelle (groesster Abstand unter der Sehne Brust -> Kinn)
    xb = np.arange(A[0] - 0.06, A[0] + 0.19, 0.01)
    unt = []
    for xx in xb:
        mm = km & (np.abs(x - xx) < 0.006)
        if mm.any():
            unt.append((xx, z[mm].min()))
    unt = np.array(unt)
    p0, p1 = unt[0], unt[-1]
    nrm = np.array((-(p1[1] - p0[1]), p1[0] - p0[0]))
    nrm /= np.linalg.norm(nrm)
    tief = (unt - p0) @ nrm
    kehle = unt[int(np.argmax(tief))]          # konkavste Stelle: am weitesten oben/hinten ueber der Sehne
    kehle = np.array((kehle[0], 0.0, kehle[1]))
    lin = kehle - nacken
    nk = np.array((-lin[2], 0.0, lin[0]))
    nk /= np.linalg.norm(nk)
    if nk[0] < 0:
        nk = -nk
    d = (V - A) @ nk
    d_c7 = float((C7 - A) @ nk)
    # Kopf starr: vor der Ebene Atlas - 0,03 m (Normale nk), ueber der Kehlfalte, innerhalb der Kopfbreite; Ohren immer
    kopf_starr = ((d >= -0.03) & ((z >= kehle[2] + 0.01) | (x >= kehle[0] + 0.10)) & ((ay <= 0.235) | (d >= 0.02))) | ohr
    # Rumpf fest (kein Hals/Kopf): hinter der C7-Ebene, unter der Kehlfalte (Brust), an den Beinen, aussen an den Schultern
    # Lauf 2: Uebergang nach hinten bis 8 cm hinter C7 (Lauf 1: Nackenfalte beim Kopfheben/-drehen auf nur 15 cm Uebergang)
    rumpf_fest = (d <= d_c7 - 0.08) | (z <= kehle[2] - 0.10) | (msum > 0.3) | ((ay > 0.26) & (d < -0.03))
    rumpf_fest &= ~kopf_starr
    # dazwischen harmonisch (Kotangens-Laplace auf dem Netz): glattester Uebergang Kopf -> Rumpf
    fest = kopf_starr | rumpf_fest
    h = harmonisch(V, T, fest, kopf_starr.astype(float))
    # Kopf = sst(0,3; 1; h) (flach an der starren Grenze), Rumpf = 1 - sst(0; 0,7; h), dazwischen Neck
    a_head = np.where(kopf_starr, 1.0, sst(0.3, 1.0, h))
    a_neck = np.where(kopf_starr, 0.0, np.maximum(0.0, sst(0.0, 0.7, h) - sst(0.3, 1.0, h)))
    rest = 1.0 - a_head - a_neck
    a_pel = rest * (1.0 - p_sp)
    a_spi = rest * p_sp * (1.0 - p_ch)
    a_ch = rest * p_sp * p_ch
    # ---- Schwanz: Stummel 1,0, Ring 2 cm mit dem Becken
    st = N["stummel"]
    dst = np.full(n, np.inf)
    for p in V[st]:
        dst = np.minimum(dst, np.linalg.norm(V - p, axis=1))
    a_tail = np.where(st, 1.0, 1.0 - sst(0.0, 0.02, dst))
    for k_, a_ in (("Bip01_Pelvis", a_pel), ("Bip01_Spine", a_spi), ("Bip01_Spine1", a_ch), ("Bip01_Neck", a_neck), ("Bip01_Head", a_head)):
        W[k_] += rumpf * a_ * (1.0 - a_tail)
    W["Bip01_Tail"] += rumpf * a_tail * 1.0
    W["Bip01_Pelvis"] += 0.0
    Wm = np.stack([W[nm] for nm in namen], 1)
    Wm /= Wm.sum(1, keepdims=True)
    # Kopf starr exakt (auch gegen die Bein-Anteile; Kopf liegt nie an einem Bein)
    ih = namen.index("Bip01_Head")
    Wm[kopf_starr] = 0.0
    Wm[kopf_starr, ih] = 1.0
    formel_W = Wm.copy()
    # ---- starre Zonen: Kopf, Pfoten (unter dem Gelenk, Pfoten-Masken), Krallen, Stummel
    kralle = N["kralle"]
    pfote_m = N["pfote_VL"] | N["pfote_VR"] | N["pfote_HL"] | N["pfote_HR"]
    i_pf = [namen.index("Bip01_%s_%s" % (s_, k)) for s_ in "LR" for k in ("Hand", "Foot")]
    pf_w = Wm[:, i_pf].sum(1)
    starr = kopf_starr | kralle | st | (pf_w >= 0.95)
    # ---- Raumglaettung (sigma 0,03 m) ausser starre Zonen, je Koerperhaelfte (keine Mischung linkes/rechtes Bein)
    SIG = 0.03
    Wg = Wm.copy()
    for hl in ((y >= -0.005), (y <= 0.005)):
        q = hl & ~starr
        Wg_h = raum_glatt(V[hl], Wm[hl], SIG, Xq=V[q])
        Wg[q] = Wg_h
    # Seitenregel nach dem Glaetten: linke Beinknochen nie rechts der Mitte und umgekehrt; Vorderbein nie hinter x_mitte, Hinterbein
    # nie davor; Hals/Kopf nie an Beinpunkten (Formel-Bein-Anteil > 0,5)
    for b, nm in enumerate(namen):
        if "_L_" in nm:
            Wg[y < 0, b] = 0.0
        if "_R_" in nm:
            Wg[y > 0, b] = 0.0
        if any(t in nm for t in ("UpperArm", "Forearm", "Hand", "Clavicle")):
            Wg[x < x_mitte, b] = 0.0
        if any(t in nm for t in ("Thigh", "Calf", "Foot", "Toe0")):
            Wg[x > x_mitte, b] = 0.0
        if nm in ("Bip01_Neck", "Bip01_Head"):
            Wg[msum > 0.5, b] = 0.0
        if nm == "Bip01_Tail":
            Wg[dst > 0.05, b] = 0.0
    Wg = np.maximum(Wg, 0.0)
    # Schritt-/Brustbein-Regel NACH dem Glaetten (das Glaetten traegt sonst Beingewicht in die Mittellinie): Bein x sst(0; 0,12; dc),
    # der Rest geht an den Rumpf (Becken/Lende/Brust wie entlang der Wirbelsaeule)
    hinten_m = x < x_mitte
    dc_post = np.sqrt(y ** 2 + np.maximum(np.where(hinten_m, z_kreuz["H"], z_kreuz["V"]) - z, 0.0) ** 2)
    kreuz_post = sst(0.0, 0.12, dc_post)
    bein_ix = [b for b, nm in enumerate(namen) if any(t in nm for t in ("Thigh", "Calf", "Foot", "UpperArm", "Forearm", "Hand"))]
    vorher = Wg[:, bein_ix].sum(1)
    Wg[:, bein_ix] *= kreuz_post[:, None]
    defizit = vorher - Wg[:, bein_ix].sum(1)
    for k_, a_ in (("Bip01_Pelvis", 1.0 - p_sp), ("Bip01_Spine", p_sp * (1.0 - p_ch)), ("Bip01_Spine1", p_sp * p_ch)):
        Wg[:, namen.index(k_)] += defizit * a_
    Wg[Wg < 1e-3] = 0.0
    leer = Wg.sum(1) <= 1e-9
    Wg[leer] = Wm[leer]
    log("FORMEL Punkte ohne Gewicht nach der Seitenregel (Formel zurueck): %d" % int(leer.sum()))
    o = np.argsort(-Wg, 1)
    keep = np.zeros_like(Wg, dtype=bool)
    np.put_along_axis(keep, o[:, :4], True, 1)
    Wg[~keep] = 0.0
    Wg /= Wg.sum(1, keepdims=True)
    # Krallen 1,0 an der Pfote (Hand vorn, Foot hinten)
    for s_ in "LR":
        for nm_, cond in (("Hand", x > x_mitte), ("Foot", x <= x_mitte)):
            m = kralle & ((y > 0) if s_ == "L" else (y <= 0)) & cond
            Wg[m] = 0.0
            Wg[m, namen.index("Bip01_%s_%s" % (s_, nm_))] = 1.0
    assert (Wg > 0).sum(1).max() <= 4 and np.abs(Wg.sum(1) - 1).max() < 1e-9
    # ---- Gegend je Dreieck (0 Rumpf, 1 Kopf, 2 Kralle) und Regionen je Dreieck
    gegend = np.zeros(len(T), dtype=np.int32)
    gegend[kopf_starr[T].all(1)] = 1
    gegend[kralle[T].all(1)] = 2
    reg_t = regionen(V, T, Wg, namen, pos, N, kopf_starr, x_mitte, np.where(kopf_starr, 0.0, h))
    info = dict(x_mitte=float(x_mitte), nacken=nacken.tolist(), kehle=kehle.tolist(), kopf_normale=nk.tolist(), d_c7=d_c7, z_kreuz=z_kreuz,
                hals_frei=int((~fest).sum()),
                kopf_starr=int(kopf_starr.sum()), starr=int(starr.sum()), versatz_x=vx,
                bein_punkte={k: int((v > 0.5).sum()) for k, v in m_bein.items()})
    np.savez(aus, V=V, T=T, W=Wg, formel_W=formel_W, namen=np.array(namen), kralle=kralle, kopf_starr=kopf_starr, starr=starr,
             pfote=pfote_m, ohr=ohr, stummel=st, gegend=gegend, regionen=reg_t, regionen_namen=np.array(REG_NAMEN),
             x_mitte=np.float64(x_mitte), kopf_normale=nk, d_kopf=d, info=json.dumps(info))
    log("FORMEL", json.dumps(info))
    log("FORMEL Einfluesse max %d, Summe %.6f..%.6f; Punkte je Hauptknochen:" % ((Wg > 0).sum(1).max(), Wg.sum(1).min(), Wg.sum(1).max()),
        {namen[k].replace("Bip01_", ""): int(c) for k, c in zip(*np.unique(Wg.argmax(1), return_counts=True))})
    log("FORMEL Regionen je Dreieck:", {REG_NAMEN[k]: int(c) for k, c in zip(*np.unique(reg_t, return_counts=True))})
    return aus


def regionen(V, T, W, namen, pos, N, kopf_starr, x_mitte, hals_w):
    """Region je Dreieck (fuer Falten-Zone und Dehnungs-Tabelle): achsel, brust, leiste, hals, kopf, ohr, pfote, kralle, stummel, bauch."""
    def ws(*nn):
        return sum(W[:, namen.index(n_)] for n_ in nn)
    wV = ws(*["Bip01_%s_%s" % (s, k) for s in "LR" for k in ("UpperArm", "Forearm", "Hand")])
    wH = ws(*["Bip01_%s_%s" % (s, k) for s in "LR" for k in ("Thigh", "Calf", "Foot")])
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    NL = np.zeros_like(V)
    for k in range(3):
        np.add.at(NL, T[:, k], fn)
    NL /= np.maximum(np.linalg.norm(NL, axis=1, keepdims=True), 1e-12)
    x, y, z = V[:, 0], V[:, 1], V[:, 2]
    nx, ny, nz = NL[:, 0], NL[:, 1], NL[:, 2]
    s_ = np.where(y >= 0, 1.0, -1.0)
    ny_in = -s_ * ny

    def seg_abst(P, a, b):
        ab = b - a
        t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
        return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
    g = lambda k, s: pos["Bip01_%s_%s" % (s, k)]
    dA = np.where(y >= 0, seg_abst(V, g("UpperArm", "L"), g("Forearm", "L")), seg_abst(V, g("UpperArm", "R"), g("Forearm", "R")))
    dT = np.where(y >= 0, seg_abst(V, g("Thigh", "L"), g("Calf", "L")), seg_abst(V, g("Thigh", "R"), g("Calf", "R")))
    xs = pos["Bip01_L_UpperArm"][0]
    R = np.zeros(len(V), dtype=np.int32)
    kopf_o = kopf_starr & ~(N["ohr_l"] | N["ohr_r"])
    regeln = [
        (1, (dA < 0.18) & (z < 0.70) & (z > 0.30) & (x > x_mitte) & ((nx < -0.15) | (ny_in > 0.15) | (nz < -0.35)) & ~kopf_starr),
        (3, (dT < 0.22) & (z < 0.66) & (z > 0.28) & (x < x_mitte) & ((nx > 0.15) | (ny_in > 0.15) | (nz < -0.35))),
        (2, (x > xs - 0.05) & (np.abs(y) < 0.12) & (z > 0.33) & (z < 0.78) & ((nx > 0.25) | (nz < -0.3)) & (wV < 0.4) & ~kopf_starr),
        (10, (nz < -0.45) & (x > pos["Bip01_L_Thigh"][0] + 0.10) & (x < xs - 0.05) & (np.abs(y) < 0.22) & (z > 0.30) & (wV < 0.3) & (wH < 0.3)),
        (4, (hals_w > 0.15) & ~kopf_starr),
        (5, kopf_o), (6, N["ohr_l"] | N["ohr_r"]),
        (7, N["pfote_VL"] | N["pfote_VR"] | N["pfote_HL"] | N["pfote_HR"]),
        (8, N["kralle"]), (9, N["stummel"]),
    ]
    for r, m in regeln:
        R[m] = r
    a_, b_, c_ = R[T[:, 0]], R[T[:, 1]], R[T[:, 2]]
    return np.where(b_ == c_, b_, a_).astype(np.int32)


# =================================================================================================================================
# DUMP laden (Pickle von dumpread.py oder Text)
# =================================================================================================================================
def lade_dump(pfad):
    if pfad.endswith(".pkl"):
        return pickle.load(open(pfad, "rb"))
    if os.path.exists(pfad + ".pkl"):
        return pickle.load(open(pfad + ".pkl", "rb"))
    sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges/werkzeug")
    from dumpread import lese
    _d = lese(pfad)
    return dict(names=_d["names"], off=_d["off"], clips={k: dict(T=c["T"], M=c["M"]) for k, c in _d["clips"].items()},
                verts=_d["verts"], el=_d["el"], idx=_d["idx"])


# =================================================================================================================================
# DEHNUNG je Clip (alle Bilder): sigma1 p99,5 / max, Achsel+Brust max, Falten (sigma2 < 0,5) je Region
# =================================================================================================================================
def dehnung(gew, dpfad, aus=None, regionen_aus=None):
    G = np.load(gew)
    D = lade_dump(dpfad)
    V, T, W = G["V"], G["T"], G["W"].astype(np.float64)
    NAM = [str(n) for n in G["namen"]]
    RT = G["regionen"]
    RN = [str(s) for s in G["regionen_namen"]]
    IX = {nm: i for i, nm in enumerate(D["names"])}
    OFF = np.asarray(D["off"])
    bi = np.array([IX[nm] for nm in NAM])
    P0 = np.stack((V[:, 1], V[:, 2], -V[:, 0]), 1) * M2U
    H0 = np.c_[P0, np.ones(len(V))]
    e1 = P0[T[:, 1]] - P0[T[:, 0]]
    e2 = P0[T[:, 2]] - P0[T[:, 0]]
    l01, l02 = np.linalg.norm(e1, axis=1), np.linalg.norm(e2, axis=1)
    l12 = np.linalg.norm(P0[T[:, 2]] - P0[T[:, 1]], axis=1)
    gt = np.minimum(np.minimum(l01, l02), l12) > 0.004
    gt &= np.linalg.norm(np.cross(e1, e2), axis=1) / np.maximum(np.maximum(l01, l02), l12) > 0.002 * M2U
    uu = e1 / l01[:, None]
    nn_ = np.cross(e1, e2)
    nn_ /= np.maximum(np.linalg.norm(nn_, axis=1, keepdims=True), 1e-12)
    vv = np.cross(nn_, uu)
    Rm = np.stack((np.stack(((e1 * uu).sum(1), (e2 * uu).sum(1)), 1), np.stack(((e1 * vv).sum(1), (e2 * vv).sum(1)), 1)), 1)
    RI = np.zeros_like(Rm)
    RI[gt] = np.linalg.inv(Rm[gt])
    nz = W > 0
    out = {}
    za = np.isin(RT, [RN.index("achsel"), RN.index("brust")])
    for c in CLIPS:
        C = D["clips"][c]
        s1all, s2all = [], []
        for M in C["M"]:
            S = np.einsum("bij,bjk->bik", M[bi], OFF[bi])[:, :3, :]
            P = np.einsum("bij,nj,nb->ni", S, H0, W, optimize=True)
            a1 = P[T[:, 1]] - P[T[:, 0]]
            a2 = P[T[:, 2]] - P[T[:, 0]]
            F = np.einsum("tij,tjk->tik", np.stack((a1, a2), 2), RI)
            sv = np.linalg.svd(F, compute_uv=False)
            s1all.append(sv[:, 0])
            s2all.append(sv[:, 1])
        s1 = np.array(s1all)[:, gt]
        s2 = np.array(s2all)[:, gt]
        rg = RT[gt]
        zone = za[gt]
        tot = s1.max(0)
        out[c] = dict(p995=round(float(np.percentile(s1, 99.5)), 3), max=round(float(s1.max()), 3),
                      achsel_brust_max=round(float(s1[:, zone].max()), 3) if zone.any() else 0.0,
                      falten_s2_unter_05=int((s2.min(0) < 0.5).sum()),
                      max_region=RN[int(rg[int(np.argmax(tot))])], max_bild=int(np.unravel_index(np.argmax(s1), s1.shape)[0]),
                      je_region_max={RN[r]: round(float(s1[:, rg == r].max()), 2) for r in np.unique(rg)})
        log("DEHNUNG %-16s p99,5 %.3f max %.3f (Region %s, Bild %d) Achsel/Brust %.3f Falten(s2<0,5) %d" % (
            c, out[c]["p995"], out[c]["max"], out[c]["max_region"], out[c]["max_bild"], out[c]["achsel_brust_max"], out[c]["falten_s2_unter_05"]))
    if aus:
        json.dump(out, open(aus, "w"), indent=1)
    return out


# =================================================================================================================================
# OPT -- Kopie von baer_gewichte_2c.py (Optimierer), angepasst an das Junge (Zonen in Gelenk-Koordinaten, keine Kopf-Uebernahme)
# =================================================================================================================================
def opt(formel_npz, dpfad, AUS, kv=""):
    G = np.load(formel_npz)
    gg = G["gegend"]
    P = dict(schritt=5, runden=240, lr=0.05, glatt=0.3, nah=0.02, z_pfote=0.06, druck=4.0, hoch=6.0, nachrunden=80,
             vor=1, klein=0.01, boden=0.0, falte=25.0, falte_s=0.6, r_ell=0.13, fremd=1, quetsch=15.0, quetsch_s=0.35, z_boden=0.45,
             fix1=1, falte_b=25.0, z_fremd=0.15, z_fuss=0.06, fuss_min=0.95, swipe=1.0, liege=1.0, band_z0=0.18, band_z1=0.44,
             achsel_w=20.0, achsel_s=3.0, ueber_w=10.0, ueber_s=3.5, traeger=0.08)
    # Junges: ueber_w/ueber_s: Zusatzstrafe ueber sigma1 3,5 in ALLEN Dreiecken (Grenze max 4,0); traeger: Knochen nur, wo die Formel ihn
    # im Umkreis von ~traeger Metern schon hat (sonst schiebt der Abstieg Hand/Fuss-Anteile in die Brust, Lauf 1: Hand 0,06 am Brustbein)
    # Junges: boden 0 (Vorgabe): die Vorab-Clips haben noch keinen Hub (RIG_PLAN 5.5); ein Bodenabstand ist dort kein Gewichtsfehler.
    # achsel_w 4 (2c fix1: Grenze Achsel/Brust 3,5), swipe 1 (Achsel-Spitze zwischen den 5er-Schritten), r_ell 0,13 (kleineres Bein)
    if kv:
        for k_v in kv.split(","):
            k, v = k_v.split("=")
            P[k] = float(v)
    V, T, W0 = G["V"], G["T"], G["W"].astype(np.float64)
    NAM = [str(n) for n in G["namen"]]
    KR = G["kralle"]
    STARR = G["starr"]
    n = len(V)
    x_mitte = float(G["x_mitte"])
    dkopf = G["d_kopf"]
    log("OPT Parameter", json.dumps(P))
    D = lade_dump(dpfad)
    log("OPT Clips aus", dpfad)
    IX = {nm: i for i, nm in enumerate(D["names"])}
    OFF = np.asarray(D["off"])
    # ---- Kanten (aus den Dreiecken), Ruhelaengen im Modellraum
    P0 = np.stack((V[:, 1], V[:, 2], -V[:, 0]), 1) * M2U
    H0 = np.c_[P0, np.ones(n)]
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    E.sort(1)
    E = np.unique(E, axis=0)
    L0 = np.linalg.norm(P0[E[:, 0]] - P0[E[:, 1]], axis=1)
    x, y, z = V[:, 0], V[:, 1], V[:, 2]
    # ---- freie Punkte und Kandidaten-Knochen (Junges: Kopf/Ohren, Pfoten, Krallen, Stummel starr)
    frei = ~STARR & (z > P["z_pfote"])
    _w_pf = sum(W0[:, NAM.index("Bip01_%s_%s" % (s_, k_))] for s_ in "LR" for k_ in ("Hand", "Foot"))
    frei &= _w_pf < 0.95
    log("OPT starr %d Punkte (Kopf %d), frei %d" % (int((~frei).sum()), int(G["kopf_starr"].sum()), int(frei.sum())))
    links = y >= 0
    torso = ["Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Tail", "Bip01_Head"]
    bein = {s: ["Bip01_%s_%s" % (s, k) for k in ("UpperArm", "Forearm", "Hand", "Thigh", "Calf", "Foot")] for s in "LR"}
    KAND = {s: [NAM.index(b) for b in torso + bein[s]] for s in "LR"}
    nk = len(KAND["L"])
    fi = np.nonzero(frei)[0]
    kidx = np.where(links[fi, None], np.array(KAND["L"])[None, :], np.array(KAND["R"])[None, :])
    nf = len(fi)
    NAM_K = [NAM[i] for i in KAND["L"]]
    erlaubt = np.ones((nf, nk), dtype=bool)
    xf = x[fi]
    # Junges: Kopf nur im Halsbereich (d_kopf >= -0,20: vor dem Halsansatz), Schwanz nur am Stummel-Ring (Formel > 0),
    # Vorderbein nur vor x_mitte, Hinterbein nur dahinter
    for k_, nm_ in enumerate(NAM_K):
        if nm_ == "Bip01_Head":
            erlaubt[:, k_] = dkopf[fi] > -0.20
        elif nm_ == "Bip01_Neck":
            erlaubt[:, k_] = dkopf[fi] > -0.26
        elif nm_ == "Bip01_Tail":
            erlaubt[:, k_] = W0[fi, NAM.index("Bip01_Tail")] > 0
        elif any(t in nm_ for t in ("UpperArm", "Forearm", "Hand")):
            erlaubt[:, k_] = xf > x_mitte
        elif any(t in nm_ for t in ("Thigh", "Calf", "Foot")):
            erlaubt[:, k_] = xf < x_mitte
    if P["traeger"] > 0:
        # Traeger je Knochen: Formel > 0, raeumlich geweitet (Gauss sigma = traeger/2, Schwelle 0,02) -- je Koerperhaelfte
        _ind = (W0 > 0).astype(np.float64)
        _tr = np.zeros_like(_ind)
        for _hl in ((y >= -0.005), (y <= 0.005)):
            _q = _hl & frei
            _tr[_q] = np.maximum(_tr[_q], raum_glatt(V[_hl], _ind[_hl], P["traeger"] / 2.0, Xq=V[_q]))
        _tr_k = np.take_along_axis(_tr[fi], kidx, 1) > 0.02
        vor_ = int(erlaubt.sum())
        erlaubt &= _tr_k
        log("OPT Traeger der Formel (geweitet %.2f m): erlaubte Eintraege %d -> %d" % (P["traeger"], vor_, int(erlaubt.sum())))
    if P["fremd"] > 0:
        def _w0(*teile):
            return sum(np.where(links[fi], W0[fi, NAM.index("Bip01_L_" + t)], W0[fi, NAM.index("Bip01_R_" + t)]) for t in teile)
        wv0 = _w0("UpperArm", "Forearm", "Hand")
        wh0 = _w0("Thigh", "Calf", "Foot")
        for k_, nm_ in enumerate(NAM_K):
            if any(t in nm_ for t in ("UpperArm", "Forearm", "Hand")):
                erlaubt[:, k_] &= (wh0 < 0.05)
            elif any(t in nm_ for t in ("Thigh", "Calf", "Foot")):
                erlaubt[:, k_] &= (wv0 < 0.05)
            elif nm_ in ("Bip01_Neck", "Bip01_Head"):
                erlaubt[:, k_] &= (wv0 < 0.5) & (wh0 < 0.05)
        log("OPT verbotene Knochen-Eintraege (fremd) %d" % int((~erlaubt).sum()))
    if P.get("fix1", 1) > 0:
        _unten = (z[fi] < P["z_fremd"]) & (np.abs(y[fi]) > 0.03)
        for k_, nm_ in enumerate(NAM_K):
            if nm_ in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail", "Bip01_Neck", "Bip01_Head"):
                erlaubt[:, k_] &= ~_unten
        log("OPT Rumpfknochen unter z %.2f an den Beinen verboten: %d freie Punkte" % (P["z_fremd"], int(_unten.sum())))
    w = np.take_along_axis(W0[fi], kidx, 1)
    w = np.where(erlaubt, np.maximum(w, 0), 0.0)
    leer = w.sum(1) <= 1e-9
    w[leer] = np.take_along_axis(W0[fi], kidx, 1)[leer]
    erlaubt |= w > 0
    w /= np.maximum(w.sum(1, keepdims=True), 1e-9)
    w_start = w.copy()
    log("OPT Punkte %d, frei %d, Kandidaten je Punkt %d, Kanten %d" % (n, nf, nk, len(E)))
    fpos = np.full(n, -1)
    fpos[fi] = np.arange(nf)
    ke = (fpos[E[:, 0]] >= 0) | (fpos[E[:, 1]] >= 0)
    E2, L02 = E[ke], L0[ke]
    ok = L02 > 0.002
    E2, L02 = E2[ok], L02[ok]
    kt = (fpos[T] >= 0).any(1)
    T2 = T[kt]
    e1 = P0[T2[:, 1]] - P0[T2[:, 0]]
    e2 = P0[T2[:, 2]] - P0[T2[:, 0]]
    l01, l02_ = np.linalg.norm(e1, axis=1), np.linalg.norm(e2, axis=1)
    l12 = np.linalg.norm(P0[T2[:, 2]] - P0[T2[:, 1]], axis=1)
    gt = np.minimum(np.minimum(l01, l02_), l12) > 0.004
    gt &= np.linalg.norm(np.cross(e1, e2), axis=1) / np.maximum(np.maximum(l01, l02_), l12) > 0.002 * M2U
    T2, e1, e2, l01 = T2[gt], e1[gt], e2[gt], l01[gt]
    uu = e1 / l01[:, None]
    nn_ = np.cross(e1, e2)
    nn_ /= np.linalg.norm(nn_, axis=1, keepdims=True)
    vv = np.cross(nn_, uu)
    Rm = np.stack((np.stack(((e1 * uu).sum(1), (e2 * uu).sum(1)), 1), np.stack(((e1 * vv).sum(1), (e2 * vv).sum(1)), 1)), 1)
    RI = np.linalg.inv(Rm).astype(np.float64)
    nt = len(T2)
    # Falten-Zone: Region Achsel, um Ellbogen/Knie (r_ell), Uebergangsband der Beine (band_z0..band_z1, |y| > 0,03)
    RT = G["regionen"]
    RN = [str(s) for s in G["regionen_namen"]]
    idx_t2 = np.nonzero(kt)[0][gt]
    _mitte = V[T2].mean(1)
    _ell = np.zeros(nt, dtype=bool)
    _knie = np.zeros(nt, dtype=bool)
    for _s in "LR":
        _p = np.linalg.inv(OFF[IX["Bip01_%s_Forearm" % _s]])[:3, 3]
        _ell |= np.linalg.norm(_mitte - np.array((-_p[2], _p[0], _p[1])) / M2U, axis=1) < P["r_ell"]
        _p = np.linalg.inv(OFF[IX["Bip01_%s_Calf" % _s]])[:3, 3]
        _knie |= np.linalg.norm(_mitte - np.array((-_p[2], _p[0], _p[1])) / M2U, axis=1) < P["r_ell"]
    ZONE = ((RT[idx_t2] == RN.index("achsel")) | _ell).astype(np.float64)
    _band = (_mitte[:, 2] > P["band_z0"]) & (_mitte[:, 2] < P["band_z1"]) & (np.abs(_mitte[:, 1]) > 0.03)
    _rue = (_mitte[:, 2] > 0.80) & (_mitte[:, 0] > x_mitte - 0.45) & (_mitte[:, 0] < x_mitte + 0.40)      # Ruecken (Rear: Ueberstreckung)
    _neu = (_knie | _band | _rue | (RT[idx_t2] == RN.index("leiste")) | (RT[idx_t2] == RN.index("hals"))) & (ZONE < 0.5)
    ZONE = np.maximum(ZONE, _neu * P["falte_b"] / max(P["falte"], 1e-9))
    ZA = ((RT[idx_t2] == RN.index("achsel")) | (RT[idx_t2] == RN.index("brust"))).astype(np.float64)
    log("OPT Falten-Zone %d Dreiecke (Achsel %d, Ellbogen %d, Knie/Band/Leiste/Hals neu %d); Achsel/Brust-Strafe %d Dreiecke (Gewicht %.1f ueber %.2f)" % (
        int((ZONE > 0).sum()), int((RT[idx_t2] == RN.index("achsel")).sum()), int(_ell.sum()), int(_neu.sum()), int(ZA.sum()), P["achsel_w"], P["achsel_s"]))
    log("OPT Dreiecke mit freiem Punkt (gueltig) %d" % nt)
    bilder = []
    FW = []
    for c, C in D["clips"].items():
        nfr = len(C["T"])
        fr = list(range(0, nfr, int(P["schritt"]))) + [nfr - 1]
        if P["swipe"] > 0 and c in ("NCBear_SwipeL", "NCBear_SwipeR"):
            fr = sorted(set(fr) | set(range(6, min(24, nfr))))
        for f in sorted(set(fr)):
            bilder.append(C["M"][f])
            FW.append(P["liege"] if (c == "DeerStag_Dead" or (c == "DeerStag_Death" and f >= 0.75 * (nfr - 1))) else 1.0)
    if P.get("zusatz", 1) > 0:
        # Probe-Posen als Zusatzbilder (RIG_PLAN 4.3): Kopf nicken +-30 / gieren +-35 (nur Head und je halb Neck/Head), Vorder- und
        # Hinterbein je Seite +-35 -- gebaut auf der Ruhe (inv(OFF) der gewichteten Knochen) mit denselben Drehachsen wie proben_posen.py.
        # Damit gelten die Gewichte auch fuer Bewegungen, die die Vorab-Clips nicht zeigen (neue Gang- und Sitz-Clips der Rolle CLIPS).
        _par = list(D["par"]) if "par" in D else None
        _BW = np.array([np.linalg.inv(o) for o in OFF])
        _Dm = np.array([[0, 1.0, 0], [0, 0, 1.0], [-1.0, 0, 0]])

        def _kinder(b):
            out = {b}
            neu_ = True
            while neu_:
                neu_ = False
                for k_, p_ in enumerate(_par):
                    if p_ in out and k_ not in out:
                        out.add(k_); neu_ = True
            return out

        def _rot(ax, g):
            a_ = np.asarray(ax, float) / np.linalg.norm(ax); t_ = np.radians(g)
            K = np.array([[0, -a_[2], a_[1]], [a_[2], 0, -a_[0]], [-a_[1], a_[0], 0]])
            return _Dm @ (np.eye(3) + np.sin(t_) * K + (1 - np.cos(t_)) * K @ K) @ _Dm.T

        def _pose(teile):
            M = _BW.copy()
            for kn, ax, g in teile:
                b = IX[kn]
                p_ = M[b][:3, 3].copy()
                G4 = np.eye(4); G4[:3, :3] = _rot(ax, g); G4[:3, 3] = p_ - G4[:3, :3] @ p_
                for k_ in _kinder(b):
                    M[k_] = G4 @ M[k_]
            return M
        Yq, Zq = (0, 1.0, 0), (0, 0, 1.0)
        zus = []
        for ax, g in ((Yq, 30), (Yq, -30), (Zq, 35), (Zq, -35)):
            zus.append(_pose([("Bip01_Head", ax, g)]))
            zus.append(_pose([("Bip01_Neck", ax, 0.5 * g), ("Bip01_Head", ax, 0.5 * g)]))
        for s_ in "LR":
            for g in (35, -35):
                zus.append(_pose([("Bip01_%s_UpperArm" % s_, Yq, g)]))
                zus.append(_pose([("Bip01_%s_Thigh" % s_, Yq, g)]))
        for M in zus:
            bilder.append(M)
            FW.append(1.0)
        log("OPT Zusatzbilder (Probe-Posen): %d" % len(zus))
    nb = len(bilder)
    FW = np.asarray(FW, dtype=np.float64)
    S = np.stack([np.einsum("bij,bjk->bik", M, OFF) for M in bilder], 0)[:, :, :3, :]
    fest_v = np.unique(np.concatenate((E2[(fpos[E2] < 0)], T[(fpos[T] >= 0).any(1)][fpos[T[(fpos[T] >= 0).any(1)]] < 0])))
    Wf = W0[fest_v]
    bi = np.array([IX[nm] for nm in NAM])
    Pfest = np.einsum("fbij,nj,nb->fni", S[:, bi], H0[fest_v], Wf, optimize=True).astype(np.float32)
    Q = np.empty((nb, nf, nk, 3), dtype=np.float32)
    for s in "LR":
        m = links[fi] if s == "L" else ~links[fi]
        bones = bi[KAND[s]]
        Q[:, m] = np.einsum("fkij,nj->fnki", S[:, bones], H0[fi[m]], optimize=True)
    log("OPT Bilder %d, Q %.0f MB" % (nb, Q.nbytes / 1e6))
    bod = np.nonzero(z[fi] < P["z_boden"])[0]
    if P["boden"] > 0:
        S_alle = np.concatenate([np.einsum("fbij,bjk->fbik", C["M"], OFF)[:, :, 1, :] for C in D["clips"].values()], 0)
        QB = np.empty((len(S_alle), len(bod), nk), dtype=np.float32)
        for s_ in "LR":
            m_ = links[fi[bod]] if s_ == "L" else ~links[fi[bod]]
            QB[:, m_] = np.einsum("fkj,nj->fnk", S_alle[:, bi[KAND[s_]]], H0[fi[bod][m_]], optimize=True)
    tx = [np.full(nt, -1) for _ in range(3)]
    fest_pos = np.full(n, -1)
    fest_pos[fest_v] = np.arange(len(fest_v))
    tx = [fest_pos[T2[:, k]] for k in range(3)]
    tf = [fpos[T2[:, k]] for k in range(3)]
    Eff = E[(fpos[E[:, 0]] >= 0) & (fpos[E[:, 1]] >= 0)]
    Eff = Eff[links[Eff[:, 0]] == links[Eff[:, 1]]]
    ga, gb = fpos[Eff[:, 0]], fpos[Eff[:, 1]]

    def projiziere(w, maske=None):
        if maske is not None:
            w = np.where(maske, w, -1e9)
        u = -np.sort(-w, 1)
        css = np.cumsum(u, 1) - 1
        ind = np.arange(1, w.shape[1] + 1)
        cond = u - css / ind > 0
        rho = cond.sum(1)
        theta = css[np.arange(len(w)), rho - 1] / rho
        out = np.maximum(w - theta[:, None], 0)
        if maske is not None:
            out = np.where(maske, out, 0)
        return out

    def ecken(Pf, ef, ex):
        return np.where(ef[None, :, None] >= 0, Pf[:, np.maximum(ef, 0)], Pfest[:, np.maximum(ex, 0)])

    def energie(w, grad=True):
        Pf = np.einsum("fnki,nk->fni", Q, w.astype(Q.dtype), optimize=True)
        A0, A1, A2 = (ecken(Pf, tf[k], tx[k]) for k in range(3))
        Em = np.stack((A1 - A0, A2 - A0), 3).astype(np.float64)
        F = np.einsum("ftij,tjk->ftik", Em, RI, optimize=True)
        C = np.einsum("ftji,ftjk->ftik", F, F, optimize=True)
        tr = C[..., 0, 0] + C[..., 1, 1]
        dt = C[..., 0, 0] * C[..., 1, 1] - C[..., 0, 1] ** 2
        disc = np.sqrt(np.maximum(tr * tr / 4 - dt, 1e-12))
        lam1, lam2 = tr / 2 + disc, np.maximum(tr / 2 - disc, 1e-12)
        s1, s2 = np.sqrt(lam1), np.sqrt(lam2)
        s = np.maximum(s1 - 1.0, 0.0)
        c = np.maximum(1.0 - s2, 0.0)
        hz = np.maximum(P["falte_s"] - s2, 0.0) * ZONE[None, :] * np.sqrt(FW)[:, None]
        hq = np.maximum(P["quetsch_s"] - s2, 0.0)
        ha = np.maximum(s1 - P["achsel_s"], 0.0) * ZA[None, :]
        hu = np.maximum(s1 - P["ueber_s"], 0.0)
        e_deh = float((s * s + P["hoch"] * s ** 4).sum() + P["druck"] * (c * c).sum() + P["falte"] * (hz * hz).sum() + P["achsel_w"] * (ha * ha).sum()
                      + P["quetsch"] * (hq * hq).sum() + P["ueber_w"] * (hu * hu).sum())
        if P["boden"] > 0:
            zb = np.einsum("fnk,nk->fn", QB, w[bod].astype(np.float32), optimize=True).astype(np.float64)
            zneg = np.minimum(zb, 0.0)
            e_deh += P["boden"] * float((zneg * zneg).sum())
        e_gl = P["glatt"] * ((w[ga] - w[gb]) ** 2).sum() * nb / 100.0
        e_nah = P["nah"] * ((w - w_start) ** 2).sum() * nb / 100.0
        if not grad:
            return e_deh + e_gl + e_nah, s1
        a_, b_ = C[..., 0, 1], lam1 - C[..., 0, 0]
        v1 = np.stack((a_, b_), -1)
        kl = np.linalg.norm(v1, axis=-1) < 1e-9
        v1[kl] = (1.0, 0.0)
        v1 /= np.linalg.norm(v1, axis=-1, keepdims=True)
        v2 = np.stack((-v1[..., 1], v1[..., 0]), -1)
        f1 = (2 * s + 4 * P["hoch"] * s ** 3 + 2 * P["achsel_w"] * ha + 2 * P["ueber_w"] * hu) / np.maximum(s1, 1e-6)
        f2 = (-2 * P["druck"] * c - 2 * P["falte"] * hz - 2 * P["quetsch"] * hq) / np.maximum(s2, 1e-6)
        Fv1 = np.einsum("ftik,ftk->fti", F, v1)
        Fv2 = np.einsum("ftik,ftk->fti", F, v2)
        dF = (f1[..., None, None] * Fv1[..., :, None] * v1[..., None, :] + f2[..., None, None] * Fv2[..., :, None] * v2[..., None, :]).astype(Q.dtype)
        dE = np.einsum("ftik,tjk->ftij", dF, RI, optimize=True)
        gk = (-(dE[..., 0] + dE[..., 1]), dE[..., 0], dE[..., 1])
        gP = np.zeros((nb, nf, 3), dtype=np.float64)
        fo = (np.arange(nb) * nf)[:, None]
        for k in range(3):
            m_ = tf[k] >= 0
            ik = (fo + tf[k][m_][None]).ravel()
            for c_ in range(3):
                gP[:, :, c_] += np.bincount(ik, weights=gk[k][:, m_, c_].ravel(), minlength=nb * nf).reshape(nb, nf)
        g = np.einsum("fni,fnki->nk", gP.astype(Q.dtype), Q, optimize=True).astype(np.float64)
        if P["boden"] > 0:
            g[bod] += np.einsum("fn,fnk->nk", (2.0 * P["boden"] * zneg).astype(np.float32), QB, optimize=True)
        gw = np.zeros_like(w)
        dg = 2 * P["glatt"] * (w[ga] - w[gb]) * nb / 100.0
        np.add.at(gw, ga, dg)
        np.add.at(gw, gb, -dg)
        g += gw + 2 * P["nah"] * (w - w_start) * nb / 100.0
        return e_deh + e_gl + e_nah, s1, g

    def abstieg(w, runden, maske=None):
        e, r, g = energie(w)
        vor = P.get("vor", 0) > 0
        rms = np.sqrt((g * g).mean(1)) if vor else None

        def richtung(g):
            if not vor:
                return g
            Dv = np.maximum(rms, rms.max() * 1e-3)
            return g / Dv[:, None]
        a = P["lr"] / max(np.abs(richtung(g)).max(), 1e-12)
        for it in range(int(runden)):
            dg = richtung(g)
            while True:
                w2 = projiziere(w - a * dg, maske)
                e2, r2 = energie(w2, grad=False)
                if e2 < e:
                    a *= 1.5
                    break
                a *= 0.3
                if a < 1e-14:
                    log("Schritt zu klein, Ende")
                    return w
            w = w2
            e, r, g = energie(w)
            if vor:
                rms = np.sqrt(0.8 * rms ** 2 + 0.2 * (g * g).mean(1))
            if it % 25 == 0 or it == runden - 1:
                log("Runde %4d Energie %.5g, sigma1 max %.2f, 99,5%% %.3f (Schritt %.3g)" % (it, e, r.max(), np.percentile(r, 99.5), a))
        return w

    if P.get("pruef", 0) > 0:          # Gradientenprobe in float64 (float32-Rauschen der Summe sonst groesser als der Gradient)
        Q = Q.astype(np.float64)
        Pfest = Pfest.astype(np.float64)
    e0, r0 = energie(w, grad=False)
    if P.get("pruef", 0) > 0:
        rng = np.random.default_rng(1)
        e_, r_, g_ = energie(w)
        for _ in range(6):
            i, k = rng.integers(nf), rng.integers(nk)
            h = P.get("pruef_h", 1e-4)
            w2 = w.copy()
            w2[i, k] += h
            e2, _ = energie(w2, grad=False)
            w3 = w.copy()
            w3[i, k] -= h
            e3, _ = energie(w3, grad=False)
            log("Gradientenprobe", i, k, "analytisch %.5g numerisch (zentral) %.5g" % (g_[i, k], (e2 - e3) / (2 * h)))
        raise SystemExit
    log("Start: Energie %.4g, sigma1 max %.2f 99,5%% %.3f" % (e0, r0.max(), np.percentile(r0, 99.5)))
    w = abstieg(w, P["runden"], erlaubt)
    o = np.argsort(-w, 1)
    maske = np.zeros_like(w, dtype=bool)
    np.put_along_axis(maske, o[:, :4], True, 1)
    maske &= w > P["klein"]
    maske[np.arange(nf), o[:, 0]] = True
    maske &= erlaubt
    w = projiziere(np.where(maske, w, 0), maske)
    w = abstieg(w, P["nachrunden"], maske)
    W = W0.copy()
    W[fi] = 0.0
    Wn = W[fi].copy()
    np.put_along_axis(Wn, kidx, w, 1)
    W[fi] = Wn
    W[(W < P["klein"]) & ~STARR[:, None]] = 0
    o = np.argsort(-W, 1)
    keep = np.zeros_like(W, dtype=bool)
    np.put_along_axis(keep, o[:, :4], True, 1)
    W[~keep] = 0
    W /= W.sum(1, keepdims=True)
    if P.get("fix1", 1) > 0:
        _rk = [NAM.index(nm_) for nm_ in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail", "Bip01_Neck", "Bip01_Head")]
        _bein = (np.abs(y) > 0.03) & ~G["kopf_starr"] & ~KR
        _m = _bein & (z < P["z_fremd"]) & (W[:, _rk].sum(1) > 0)
        W[np.ix_(_m, _rk)] = 0.0
        W[_m] /= W[_m].sum(1, keepdims=True)
        log("OPT Rumpfknochen an Beinpunkten unter z %.2f entfernt: %d Punkte" % (P["z_fremd"], int(_m.sum())))
        _fhk = [NAM.index("Bip01_%s_%s" % (s_, k_)) for s_ in "LR" for k_ in ("Hand", "Foot")]
        _fh = W[:, _fhk].sum(1)
        _m2 = _bein & (z < P["z_fuss"]) & (_fh > 0.5) & (_fh < P["fuss_min"])
        if _m2.any():
            _rest = 1.0 - _fh[_m2]
            _sk = (1.0 - P["fuss_min"]) / np.maximum(_rest, 1e-9)
            _maskfh = np.zeros(len(NAM), dtype=bool)
            _maskfh[_fhk] = True
            Wm = W[_m2]
            Wm[:, ~_maskfh] *= _sk[:, None]
            Wm[:, _maskfh] *= (P["fuss_min"] / np.maximum(_fh[_m2], 1e-9))[:, None]
            W[_m2] = Wm
        log("OPT Fuss/Hand unter z %.2f auf >= %.2f gesetzt: %d Punkte" % (P["z_fuss"], P["fuss_min"], int(_m2.sum())))
    assert (W[STARR] == W0[STARR]).all()
    assert (W > 0).sum(1).max() <= 4
    keep_ = {k: G[k] for k in G.files if k not in ("W",)}
    np.savez(AUS, W=W, frei=frei, opt_param=json.dumps(P), **keep_)
    log("OPT fertig: Einfluesse max %d, Summe %.6f..%.6f, Abweichung von der Formel im Mittel %.3f -> %s" % (
        (W > 0).sum(1).max(), W.sum(1).min(), W.sum(1).max(), np.abs(W - W0)[fi].sum(1).mean() / 2, AUS))


# =================================================================================================================================
# ABGABE: gewichte_rig.npz + regionen_rig.npz (RIG_PLAN 4.4)
# =================================================================================================================================
def abgabe(opt_npz, aus_dir):
    G = np.load(opt_npz)
    W = G["W"].astype(np.float64)
    assert (W > 0).sum(1).max() <= 4 and np.abs(W.sum(1) - 1).max() < 1e-6 and (W >= 0).all()
    np.savez(os.path.join(aus_dir, "gewichte_rig.npz"), W=W, namen=G["namen"], formel_W=G["formel_W"], V=G["V"], T=G["T"],
             kopf_starr=G["kopf_starr"], starr=G["starr"], pfote=G["pfote"], kralle=G["kralle"], ohr=G["ohr"], stummel=G["stummel"],
             frei=G["frei"] if "frei" in G.files else np.zeros(len(W), bool), opt_param=G["opt_param"] if "opt_param" in G.files else "",
             info=G["info"], regionen=G["regionen"], regionen_namen=G["regionen_namen"], x_mitte=G["x_mitte"], d_kopf=G["d_kopf"],
             gegend=G["gegend"])
    RT = G["regionen"]
    RN = [str(x) for x in G["regionen_namen"]]
    np.savez(os.path.join(aus_dir, "regionen_rig.npz"), regionen=RT, regionen_namen=G["regionen_namen"],
             **{r: (RT == RN.index(r)) for r in RN})
    log("ABGABE", os.path.join(aus_dir, "gewichte_rig.npz"), os.path.join(aus_dir, "regionen_rig.npz"),
        {r: int((RT == RN.index(r)).sum()) for r in RN})


if __name__ == "__main__":
    if sys.argv[1] == "formel":
        formel(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "opt":
        opt(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
    elif sys.argv[1] == "abgabe":
        abgabe(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "dehnung":
        dehnung(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
