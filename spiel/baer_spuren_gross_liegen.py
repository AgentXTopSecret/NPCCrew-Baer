# -*- coding: utf-8 -*-
# Lauf baer-liegen (13.11.2026), Rolle BAUER GROSS: "Baer liegt tot" fuer die zwei GROSSEN Koerper -- 2c (NCBear.glb) und
# Generator-Baer (NCBearGen.glb). NEU (kein Original geaendert). Reines Python/numpy, kein Blender.
# Ersetzt in einem vorhandenen GLB NUR die Clips DeerStag_Death (Sturz) und DeerStag_Dead (liegt tot); Netz, UV, Gewichte, Knochen,
# Texturen und alle anderen Clips bleiben byte-gleich (Selbstpruefung des Kerns, bricht sonst ab).
#
#   EIN BEFEHL JE KOERPER (wiederholbar, auch auf einem spaeteren GLB, z. B. nach der Maul-Nachbesserung):
#     python baer_spuren_gross_liegen.py 2c  EIN/NCBear.glb    AUS/NCBear.glb    [BERICHT.json]
#     python baer_spuren_gross_liegen.py gen EIN/NCBearGen.glb AUS/NCBearGen.glb [BERICHT.json]
#   Schalter: --ohne-abnahme (baut auch bei verletzter Abnahme, Fehlercode 0), --tabelle POSE.json (andere relative Tabelle, Versuche),
#             --schnell (Sturz-Abnahme nur jedes 3. Bild)
#   Ende: Zeile "LIEGEN_GROSS_OK <koerper> MD5 <md5>" und Fehlercode 0, oder "LIEGEN_GROSS_FEHLER ..." und Fehlercode 2.
#
# Aufbau: gemeinsamer Kern baer_kern_liegen.py (Rig, Loeser, aufloesen, boden_je_bild, schreibe, pruefe_nur_liegen) wird IMPORTIERT und
# nicht geaendert. Eigen sind hier: die zwei relativen Ziel-Tabellen (POSE.md T1, Abschnitt 7 GROSS), die Zeitform der Becken-Lage im
# Sturz (sturz_gross: das Becken sinkt erst, wenn die Beine nachgeben) und die Abnahme A1-A5, A7-A10 (POSE.md 5).
# Voraussetzung am Eingang: gleiche Knochen-Namen/-Eltern/-Ruhe wie heute, Clips DeerStag_Death (78 Bilder) und DeerStag_Dead vorhanden
# (die heutigen ODER schon die neuen -- zweimal gebaut = gleiche Clips).
# Statisch/offline gerechnet, nicht gespielt. Schreibt nur AUS.glb und BERICHT.json.
import hashlib
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baer_kern_liegen as K  # noqa: E402

# ------------------------------------------------------------------ Relative Ziel-Tabellen (Sprache POSE.md Abschnitt 2)
# Seitenlage rechts, Rumpf und Wange am Boden. Untere Beine (VR, HR) flach nach vorn/hinten gestreckt und das obere Hinterbein (HL)
# wie im PLAN (POSE.md T1). Abweichung GROSS (POSE.md Abschnitt 7): das obere Vorderbein (VL) haengt mit leicht erhobenem Ellbogen
# (pole z 0,5) 28 Grad gesenkt vor der Brust, die Pfote 45 Grad gebeugt (statt 16 Grad gesenkt, Ellbogen flach, Pfote 80: weniger steif,
# kein Schlitz am Handgelenk); Generator-Baer: unteres Hinterbein vor -30 (statt -34: kein Rumpfpunkt mehr in der Bein-Oeffnung).
_RUMPF = dict(boden_rumpf=-0.01, q_pel=[2, 0, 84], q_sp=[-1, 0, 84], q_ch=[-4, 3, 83], q_ne=[-4, 20, 80], q_he=[0, 16, 78], q_ta=[-12, 0, 80],
              klav=dict(L=-8, R=6), kiefer=0, kopf_boden=-0.003, pel_xy=[-0.37, -0.24])
TABELLEN = {
    "2c": dict(_RUMPF, bein=dict(
        VR=dict(s=0.93, vor=48, boden=0.0, pfote=dict(beuge=22)),
        HR=dict(s=0.93, vor=-42, boden=0.0, pfote=dict(beuge=24)),
        VL=dict(s=0.90, vor=12, senk=28, pole=[-1, 0, 0.5], pfote=dict(beuge=45)),
        HL=dict(s=0.90, vor=-8, senk=14, pfote=dict(beuge=17)))),
    "gen": dict(_RUMPF, bein=dict(
        VR=dict(s=0.93, vor=48, boden=0.0, pfote=dict(beuge=22)),
        HR=dict(s=0.93, vor=-30, boden=0.0, pfote=dict(beuge=21)),
        VL=dict(s=0.90, vor=12, senk=28, pole=[-1, 0, 0.5], pfote=dict(beuge=45)),
        HL=dict(s=0.90, vor=-6, senk=14, pfote=dict(beuge=17)))),
}
# Schwellen der Abnahme (POSE.md 5): Auflage cm2, Dehnung 99,5 % / max (heute + 0,10 / heute)
SCHWELLEN = {"2c": dict(auflage=700.0, dehn99=1.74, dehnmax=7.5), "gen": dict(auflage=400.0, dehn99=1.67, dehnmax=7.6)}
# Gelenkgrenzen wie baer_kampf_gross.py GRENZEN (:580) und POSE.md 2: prot, abd, tw (Twist des Oberarms/Oberschenkels), inner
GRENZEN = {"V": dict(prot=(-70, 60), abd=(-20, 45), tw=(-35, 20), inner=(55, 173)),
           "H": dict(prot=(-60, 80), abd=(-15, 35), tw=(-25, 15), inner=(55, 174))}
GRENZEN_RUMPF = dict(sp_pel=((-12, 12), (-20, 20), (-12, 12)), ch_sp=((-15, 15), (-15, 15), (-15, 15)),
                     ne_ch=((-35, 35), (-45, 50), (-15, 15)), he_ne=((-30, 30), (-35, 35), (-25, 25)))
# Sturz: tiefster Hautpunkt je Bild (m). NACHBESSERUNG 1 (Mangel T5): unten -0,011 statt -0,012 (Kern) -- die grossen Baeren stehen im
# Spiel mit Groesse 1,35; -1,2 cm waren dort -1,62 cm (Kevins Grenze "nichts tiefer als 1,5 cm im Boden"), -1,1 cm sind -1,49 cm.
BOD_UNTEN, BOD_OBEN = -0.011, 0.005
PEL_AB = 0.30                                # Becken-Lage folgt ssf(PEL_AB, 1, k): sinkt erst, wenn die Beine nachgeben


# ------------------------------------------------------------------ Sturz: Zeitform wie der Kern, Becken-Lage spaeter
def sturz_gewichte_gross(n):
    """Gewichte je Bild wie K.sturz_gewichte (Zeitform von pose_death, baer_kampf_gross.py:512) + 'pel' fuer die Becken-LAGE.
    Der Kern blendet die Becken-Lage mit k; dann sinkt das Becken schon, waehrend die Beine noch stehen, und die Boden-Regel muss es
    bis 7,3 cm zurueckheben. Mit pel = ssf(0,30, 1, k) bleibt die Korrektur unter 4 cm (gleicher Endverlauf, weniger Eingriff)."""
    G = K.sturz_gewichte(n)
    for g in G:
        g["pel"] = K.ssf(PEL_AB, 1.0, g["k"])
    G[-1]["pel"] = 1.0
    return G


def sturz_gross(rig, alt, t_end, q_end, G):
    """Wie K.sturz (Drehungen im Gelenkraum auf die neue Endpose geblendet), nur die Becken-Lage mit G[f]['pel']."""
    t, q = K.sturz(rig, alt, t_end, q_end, G)
    ip = rig.ix["Bip01_Pelvis"]
    d = np.asarray(t_end[ip]) - alt["t"][-1, ip]
    if float(np.abs(d).max()) < 1e-7:            # Eingang traegt die Endpose schon (zweiter Bau): Becken-Spur bleibt bit-gleich
        return alt["t"].copy(), q
    for f in range(len(alt["T"])):
        t[f, ip] = alt["t"][f, ip] + G[f]["pel"] * d
    t[-1, ip] = t_end[ip]
    return t, q


def spuren_gross(rig, t_end, q_end):
    """Death = heutige Spur auf die Endpose geblendet (sturz_gross) und am Boden gehalten (K.boden_je_bild), Dead = letztes Death-Bild."""
    death, dead = rig.clip("DeerStag_Death"), rig.clip("DeerStag_Dead")
    G = sturz_gewichte_gross(len(death["T"]))
    t2, q2 = sturz_gross(rig, death, t_end, q_end, G)
    t3, z0, z1, c = K.boden_je_bild(rig, t2, q2, death["s"], BOD_UNTEN, BOD_OBEN)
    if float(np.abs(t3 - t2).max()) >= 1e-6:     # Korrektur unter 1 Mikrometer (zweiter Bau: Rundung): Spur bleibt bit-gleich
        t2 = t3
    td, qd = dead["t"].copy(), dead["q"].copy()
    ip = rig.ix["Bip01_Pelvis"]
    for i, name in enumerate(rig.name):
        if name.startswith("Bip01_"):
            qd[:, i] = q2[-1, i]
    td[:, ip] = t2[-1, ip]
    info = dict(sturz_tief_vor_cm=z0, sturz_tief_cm=z1, becken_korrektur_cm=c, gewichte=G)
    return {"DeerStag_Death": dict(t=t2, q=q2), "DeerStag_Dead": dict(t=td, q=qd)}, info, death


# ------------------------------------------------------------------ Messen
def _tw(L, pose, key):
    """Twist des oberen Knochens gegen den Elternknochen wie schulter_mass()/twist_swing() in baer_kampf_gross.py:675 (Grad)."""
    L_ = L.LEG[key]
    hip0, K0, A0 = L.Jp[L_["oben"]], L.Jp[L_["unten"]], L.Jp[L_["fuss"]]
    d_up0 = (K0 - hip0) / np.linalg.norm(K0 - hip0)
    l = (A0 - hip0) / np.linalg.norm(A0 - hip0)
    e0 = K0 - (hip0 + l * float((K0 - hip0) @ l))
    e0 /= np.linalg.norm(e0)
    lat = np.array([0.0, float(L_["s"]), 0.0])
    sgn = 1.0 if float(np.cross(d_up0, e0) @ lat) > 0 else -1.0
    q = K.mat_q(pose[L.eltern[L_["oben"]]][0].T @ pose[L_["oben"]][0])
    ang = 2.0 * math.atan2(float(q[:3] @ d_up0), float(q[3]))
    ang = (ang + math.pi) % (2 * math.pi) - math.pi
    return round(math.degrees(ang) * sgn, 1)


def gelenke(L, pose):
    r = {}
    for key in L.LEG:
        w = K.bein_winkel(L, pose, key)
        w["tw"] = _tw(L, pose, key)
        r[key] = w
    r.update(K.rumpf_winkel(pose))
    return r


def gelenk_fehler(g):
    f = []
    for key in ("VL", "VR", "HL", "HR"):
        for nm, (lo, hi) in GRENZEN[key[0]].items():
            if not lo - 0.05 <= g[key][nm] <= hi + 0.05:
                f.append("A8 %s %s %.1f ausserhalb %s..%s" % (key, nm, g[key][nm], lo, hi))
    for nm, gr in GRENZEN_RUMPF.items():
        for v, (lo, hi), ax in zip(g[nm], gr, ("yaw", "pitch", "roll")):
            if not lo - 0.05 <= v <= hi + 0.05:
                f.append("A8 %s %s %.1f ausserhalb %s..%s" % (nm, ax, v, lo, hi))
    return f


def _windung32(Q, P, tt, block=96):
    """Windungszahl wie K.windung, in float32 gerechnet (2,4x schneller); grenznahe Werte (0,45..0,55) rechnet _innen() mit K.windung nach."""
    if len(tt) == 0 or len(Q) == 0:
        return np.zeros(len(Q))
    A, B, C = (P[tt[:, k]].astype(np.float32) for k in range(3))
    Q = Q.astype(np.float32)
    w = np.zeros(len(Q))
    Ax, Ay, Az = A.T
    Bx, By, Bz = B.T
    Cx, Cy, Cz = C.T
    for i in range(0, len(Q), block):
        q = Q[i:i + block]
        qx, qy, qz = q[:, 0:1], q[:, 1:2], q[:, 2:3]
        ax, ay, az = Ax - qx, Ay - qy, Az - qz
        bx, by, bz = Bx - qx, By - qy, Bz - qz
        cx, cy, cz = Cx - qx, Cy - qy, Cz - qz
        la = np.sqrt(ax * ax + ay * ay + az * az)
        lb = np.sqrt(bx * bx + by * by + bz * bz)
        lc = np.sqrt(cx * cx + cy * cy + cz * cz)
        det = ax * (by * cz - bz * cy) + ay * (bz * cx - bx * cz) + az * (bx * cy - by * cx)
        den = la * lb * lc + (ax * bx + ay * by + az * bz) * lc + (bx * cx + by * cy + bz * cz) * la + (cx * ax + cy * ay + cz * az) * lb
        w[i:i + block] = np.arctan2(det, den).sum(1, dtype=np.float64) / (2 * np.pi)
    return w


def _innen(P, q, fb):
    """Punkte q (Indizes) mit |Windungszahl| > 0,5 gegen die Dreiecke fb -- gleiche Aussage wie K.paar, nur schneller."""
    if not len(q) or not len(fb):
        return q[:0]
    w = np.abs(_windung32(P[q], P, fb))
    nah = (w > 0.45) & (w < 0.55)
    if nah.any():
        w[nah] = np.abs(K.windung(P[q[nah]], P, fb))
    return q[w > 0.5]


def _paar_schnell(P, F, ma, mb):
    """Wie K.paar (Punkte von a IN b und b IN a, Tiefe = Abstand des tiefsten Innenpunkts zum naechsten Punkt des anderen Teils), ohne
    den Haut-Abstand. Liefert (Punkte, Tiefe cm)."""
    ia, ib = np.nonzero(ma)[0], np.nonzero(mb)[0]
    fa, fb = F[ma[F].all(1)], F[mb[F].all(1)]
    lo, hi = P[ib].min(0) - 0.02, P[ib].max(0) + 0.02
    qa = ia[((P[ia] >= lo) & (P[ia] <= hi)).all(1)]
    lo, hi = P[ia].min(0) - 0.02, P[ia].max(0) + 0.02
    qb = ib[((P[ib] >= lo) & (P[ib] <= hi)).all(1)]
    n, tief = 0, 0.0
    for inn, andere in ((_innen(P, qa, fb), ib), (_innen(P, qb, fa), ia)):
        n += len(inn)
        if len(inn):
            tief = max(tief, float(np.linalg.norm(P[inn][:, None] - P[andere][None], axis=2).min(1).max()))
    return n, round(100 * tief, 2)


def _paare_bild(rig, T, P, mit_paaren=True):
    """Je Bild: Punkte in den 12 Pfoten-/Bein-Paaren (A1/A9) und groesste Tiefe Bein gegen Rumpf+Hals+Kopf (A9)."""
    F = rig.F
    keys = ("VL", "VR", "HL", "HR")
    n = 0
    if mit_paaren:
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                n += _paar_schnell(P, F, T["bein_" + a], T["bein_" + b])[0]      # bein_ = Unterbein + Pfote, enthaelt das Pfoten-Paar
    koerper = T["rumpf"] | T["hals"] | T["kopf"]
    tief = 0.0
    for a in keys:
        tief = max(tief, _paar_schnell(P, F, T["bein_" + a], koerper)[1])
    return n, tief


_W = {}


def _w_start(pfad):
    rig = K.Rig(pfad)
    _W["rig"], _W["T"], _W["death"] = rig, K.teile(rig), rig.clip("DeerStag_Death")


def _w_bild(a):
    f, tn, qn = a
    rig, T, death = _W["rig"], _W["T"], _W["death"]
    npkt, tief_neu = _paare_bild(rig, T, rig.haut_tier(rig.welt(tn, qn, death["s"][f])))
    _, tief_alt = _paare_bild(rig, T, rig.haut_tier(rig.welt(death["t"][f], death["q"][f], death["s"][f])), mit_paaren=False)
    return f, npkt, tief_neu, tief_alt


def sturz_bilder_messen(pfad, tn, qn, bilder):
    """Sturz je Bild messen (neu und heute), ueber mehrere Prozesse verteilt (je Bild ~8 s Rechenzeit); ohne Pool der Reihe nach."""
    auf = [(int(f), tn[f], qn[f]) for f in bilder]
    try:
        import multiprocessing as mp
        with mp.Pool(max(1, min(12, (os.cpu_count() or 2) - 2, len(auf))), initializer=_w_start, initargs=(pfad,)) as pool:
            return sorted(pool.map(_w_bild, auf, chunksize=1))
    except Exception as e:                                           # z. B. kein Pool erlaubt: langsam, aber gleiches Ergebnis
        print("LIEGEN_GROSS Hinweis: Sturz-Messung ohne Pool (%s)" % e)
        _w_start(pfad)
        return [_w_bild(a) for a in auf]


def drehsprung(q):
    """Groesster Drehwinkel eines Knochens zwischen Nachbarbildern (Grad)."""
    d = np.abs(np.einsum("fni,fni->fn", q[1:], q[:-1])) / (np.linalg.norm(q[1:], axis=2) * np.linalg.norm(q[:-1], axis=2))
    return float(np.degrees(2.0 * np.arccos(np.clip(d, -1.0, 1.0))).max())


def abnahme_gross(koerper, rig, L, T, pose, t, q, neu, si, death, schritt=1):
    """Abnahme nach POSE.md 5: A1-A5, A7 (Endpose), A8 (Gelenke), A9 (Sturz), A10 (Kopf starr). Liefert (Messwerte, Fehlerliste)."""
    S = SCHWELLEN[koerper]
    P = rig.haut_tier(rig.welt(t, q))
    m = K.abnahme(rig, T, P)
    F = []
    # A1 / A2
    if m["pfote_bein_punkte"] != 0:
        F.append("A1 Pfoten-/Bein-Paare: %d Punkte ineinander" % m["pfote_bein_punkte"])
    if m["pfoten_abstand_min_cm"] < 10.0:
        F.append("A2 kleinster Pfotenabstand %.2f cm < 10" % m["pfoten_abstand_min_cm"])
    # A3 Bein gegen Rumpf je Paar <= 6 Punkte und <= 1,5 cm
    for k, v in m["paare"].items():
        if k.endswith("-rumpf") and (v["a_in_b"] + v["b_in_a"] > 6 or v["tiefe_cm"] > 1.5):
            F.append("A3 %s: %d Punkte, %.2f cm" % (k, v["a_in_b"] + v["b_in_a"], v["tiefe_cm"]))
    # A4 Boden
    if not -1.5 <= m["tief_cm"] <= 0.0 or not -1.5 <= m["rumpf_tief_cm"] <= 0.0:
        F.append("A4 tiefster Punkt %.2f / Rumpf %.2f cm nicht in -1,5..0" % (m["tief_cm"], m["rumpf_tief_cm"]))
    if not -1.0 <= m["kopf_tief_cm"] <= 0.5:
        F.append("A4 Kopf %.2f cm nicht in -1,0..0,5" % m["kopf_tief_cm"])
    for k in ("VR", "HR"):
        if not -0.5 <= m["bein_tief_cm"][k] <= 0.5:
            F.append("A4 unteres Bein %s %.2f cm nicht in -0,5..0,5" % (k, m["bein_tief_cm"][k]))
    # A5 Auflage
    if m["auflage_cm2"] < S["auflage"]:
        F.append("A5 Auflage %.0f cm2 < %.0f" % (m["auflage_cm2"], S["auflage"]))
    # A7 Dehnung
    if m["dehnung"][0] > S["dehn99"] + 0.005 or m["dehnung"][1] > S["dehnmax"] + 0.005:
        F.append("A7 Dehnung %s ueber %.2f / %.2f" % (m["dehnung"], S["dehn99"], S["dehnmax"]))
    # A8 Gelenke
    g = gelenke(L, pose)
    F += gelenk_fehler(g)
    m["gelenke"] = g
    # A10 Kopf starr: Kiefer in Ruhe, Kopf-Punkte (nur Kopf/Kiefer-Gewicht) gegeneinander unveraendert
    ij, ih = rig.ix["Bip01_Jaw"], rig.ix["Bip01_Head"]
    kiefer = K.winkel(K.q_mat(rig.q0[ij]), K.q_mat(q[ij]))
    Gw = rig.gewichte()
    starr = np.nonzero(Gw[:, ih] + Gw[:, ij] > 0.9999)[0]
    P0 = rig.haut_tier(rig.W0)
    pr = starr[:: max(1, len(starr) // 400)]
    d1 = np.linalg.norm(P[pr][:, None] - P[pr][None], axis=2)
    d0 = np.linalg.norm(P0[pr][:, None] - P0[pr][None], axis=2)
    kopf_mm = float(np.abs(d1 - d0).max() * 1000.0)
    m["kopf"] = dict(kiefer_grad=round(kiefer, 3), punkte_starr=int(len(starr)), abstand_fehler_mm=round(kopf_mm, 5))
    if kiefer > 0.05 or kopf_mm > 0.01:
        F.append("A10 Kopf: Kiefer %.3f Grad, Abstandsfehler %.5f mm" % (kiefer, kopf_mm))
    # A9 Sturz
    tn, qn = neu["DeerStag_Death"]["t"], neu["DeerStag_Death"]["q"]
    n = tn.shape[0]
    z = si["sturz_tief_cm"]
    if min(z) < -1.5 - 1e-6 or max(z) > 0.6 + 1e-6:
        F.append("A9 Sturz: tiefster Punkt je Bild %.2f..%.2f cm nicht in -1,5..0,6" % (min(z), max(z)))
    G = si["gewichte"]
    null = [f for f in range(n) if max(G[f].values()) <= 0.0]
    gleich = all(np.array_equal(tn[f].astype(np.float32), death["t"][f].astype(np.float32)) and
                 np.array_equal(qn[f].astype(np.float32), death["q"][f].astype(np.float32)) for f in null)
    if not gleich:
        F.append("A9 Sturz: Bilder mit Gewicht 0 (%d..%d) nicht bit-gleich zu heute" % (null[0], null[-1]))
    td, qd = neu["DeerStag_Dead"]["t"], neu["DeerStag_Dead"]["q"]
    if not (np.array_equal(tn[-1].astype(np.float32), td[0].astype(np.float32)) and np.array_equal(qn[-1].astype(np.float32), qd[0].astype(np.float32))
            and np.array_equal(td[0], td[-1]) and np.array_equal(qd[0], qd[-1])):
        F.append("A9 letztes Death-Bild ist nicht die Dead-Pose")
    ds = drehsprung(qn)
    if ds > 12.0:
        F.append("A9 Drehsprung %.2f Grad > 12" % ds)
    bilder = sorted(set(list(range(null[-1] + 1 if null else 0, n, schritt)) + [n - 1]))      # Bilder mit Gewicht 0 sind bit-gleich zu heute
    p_max, p_bild, tief_neu, tief_alt, schlecht = 0, -1, [], [], []
    for f, npkt, tn_, ta_ in sturz_bilder_messen(rig.pfad, tn, qn, bilder):
        if npkt > p_max:
            p_max, p_bild = npkt, f
        tief_neu.append(tn_)
        tief_alt.append(ta_)
        # Bein gegen Rumpf je Bild nicht tiefer als heute im selben Bild; die Naht-Toleranz von A3 (1,5 cm) gilt auch hier
        if tn_ > max(ta_, 1.5) + 0.05:
            schlecht.append((f, tn_, ta_))
    if p_max:
        F.append("A9 Sturz: Pfoten-/Bein-Paare bis %d Punkte ineinander (Bild %d)" % (p_max, p_bild))
    if schlecht:
        F.append("A9 Sturz: Bein gegen Rumpf tiefer als heute in %d Bildern, z. B. Bild %d: %.2f cm (heute %.2f)" % (
            len(schlecht), schlecht[0][0], schlecht[0][1], schlecht[0][2]))
    m["sturz"] = dict(tief_cm=[min(z), max(z)], becken_korrektur_cm=[min(si["becken_korrektur_cm"]), max(si["becken_korrektur_cm"])],
                      bilder_bitgleich=[null[0], null[-1]] if null else [], drehsprung_grad=round(ds, 2), bilder_geprueft=len(bilder),
                      paare_punkte_max=p_max, bein_rumpf_tief_neu_max_cm=max(tief_neu), bein_rumpf_tief_heute_max_cm=max(tief_alt),
                      bein_rumpf_tief_neu_cm=tief_neu, bein_rumpf_tief_heute_cm=tief_alt, bilder=bilder)
    return m, F


# ------------------------------------------------------------------ Ein Schritt je Koerper
def baue_gross(koerper, ein, aus, bericht=None, tabelle=None, abnahme=True, schritt=1, still=False):
    Z = tabelle if tabelle is not None else TABELLEN[koerper]
    e_abs, a_abs = (os.path.normcase(os.path.abspath(x)).replace("\\", "/") for x in (ein, aus))
    if e_abs == a_abs:
        print("LIEGEN_GROSS_FEHLER %s: EIN und AUS sind dieselbe Datei -- der Eingang wird nur gelesen" % koerper)
        return dict(fehler=["EIN = AUS"]), 2
    if "/zomboid/mods/" in a_abs or "/steamapps/" in a_abs:
        print("LIEGEN_GROSS_FEHLER %s: AUS liegt in einem Mod-/Spielordner -- dieses Skript schreibt nie dorthin (Einbau macht der Integrator)" % koerper)
        return dict(fehler=["AUS in Mod-/Spielordner"]), 2
    rig = K.Rig(ein)
    L = K.Loeser(rig)
    T = K.teile(rig)
    Za, info = K.aufloesen(rig, L, T, Z)
    stat = {}
    pose = L.welt_pose(Za, stat)
    t, q = L.lokal(pose)
    neu, si, death = spuren_gross(rig, t, q)
    m, F = abnahme_gross(koerper, rig, L, T, pose, t, q, neu, si, death, schritt)
    if stat.get("ueber"):
        F.append("Bein ueberstreckt (IK): %s" % stat["ueber"])
    if F and abnahme:
        print("LIEGEN_GROSS_FEHLER %s: Abnahme verletzt, nichts geschrieben" % koerper)
        for x in F:
            print("   ", x)
        return dict(fehler=F, mess=m), 2
    os.makedirs(os.path.dirname(os.path.abspath(aus)) or ".", exist_ok=True)
    r = K.schreibe(ein, aus, {k: dict(t=v["t"], q=v["q"]) for k, v in neu.items()},
                   generator="baer_spuren_gross_liegen.py %s (Lauf baer-liegen, Bauer GROSS)" % koerper, still=True)
    md5 = hashlib.md5(open(aus, "rb").read()).hexdigest()
    assert md5 == r["md5"]
    si_aus = {k: v for k, v in si.items() if k != "gewichte"}
    out = dict(koerper=koerper, ein=ein, ein_md5=hashlib.md5(open(ein, "rb").read()).hexdigest(), aus=aus, md5=md5, neu=r["neu"],
               andere_clips_bytegleich=[r["gleich"], r["alle"]], tabelle_rel=Z, ziele_abs=Za, stat=stat, mess=m, sturz_je_bild=si_aus,
               abnahme_fehler=F)
    out.update(info)
    if bericht:
        json.dump(out, open(bericht, "w"), indent=1)
    if not still:
        s = m["sturz"]
        print("LIEGEN_GROSS %s: tief %+.2f cm, Rumpf %+.2f, Kopf %+.2f, untere Beine %+.2f / %+.2f, Auflage %d cm2" % (
            koerper, m["tief_cm"], m["rumpf_tief_cm"], m["kopf_tief_cm"], m["bein_tief_cm"]["VR"], m["bein_tief_cm"]["HR"], m["auflage_cm2"]))
        print("LIEGEN_GROSS %s: Pfoten-/Bein-Paare %d Punkte, Bein-Rumpf %d Punkte, Pfotenabstand min %.2f cm, Dehnung %s" % (
            koerper, m["pfote_bein_punkte"], m["rumpf_punkte"], m["pfoten_abstand_min_cm"], m["dehnung"]))
        print("LIEGEN_GROSS %s: Sturz tief %.2f..%.2f cm, Becken-Korrektur %.2f..%.2f cm, Drehsprung %.2f Grad, Paare im Sturz max %d Punkte, "
              "Bein-Rumpf im Sturz max %.2f cm (heute %.2f); Bilder %d..%d bit-gleich" % (
                  koerper, s["tief_cm"][0], s["tief_cm"][1], s["becken_korrektur_cm"][0], s["becken_korrektur_cm"][1], s["drehsprung_grad"],
                  s["paare_punkte_max"], s["bein_rumpf_tief_neu_max_cm"], s["bein_rumpf_tief_heute_max_cm"],
                  s["bilder_bitgleich"][0], s["bilder_bitgleich"][1]))
        print("LIEGEN_GROSS %s: andere Clips byte-gleich %d/%d Sampler-Puffer, Netz/Skin/Knoten byte-gleich; neue Kanaele %s" % (
            koerper, r["gleich"], r["alle"], json.dumps(r["neu"])))
    if F:
        print("LIEGEN_GROSS_WARNUNG %s: Abnahme verletzt (--ohne-abnahme), trotzdem geschrieben:" % koerper)
        for x in F:
            print("   ", x)
    print("LIEGEN_GROSS_OK %s MD5 %s %s" % (koerper, md5, aus))
    return out, 0


def main(argv):
    pos = [a for a in argv if not a.startswith("--")]
    opt = [a for a in argv if a.startswith("--")]
    tab = None
    if "--tabelle" in argv:
        tp = argv[argv.index("--tabelle") + 1]
        pos.remove(tp)
        tab = json.load(open(tp))
    if len(pos) < 3 or pos[0] not in TABELLEN:
        print("Aufruf: python baer_spuren_gross_liegen.py 2c|gen EIN.glb AUS.glb [BERICHT.json] [--ohne-abnahme] [--schnell] [--tabelle POSE.json]")
        return 1
    _, code = baue_gross(pos[0], pos[1], pos[2], pos[3] if len(pos) > 3 else None, tabelle=tab, abnahme="--ohne-abnahme" not in opt,
                         schritt=3 if "--schnell" in opt else 1)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
