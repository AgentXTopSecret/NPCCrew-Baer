# -*- coding: utf-8 -*-
# Lauf baer-liegen (13.11.2026), Rolle BAUER JUNGE: "Junges liegt tot" -- Clips DeerStag_Death / DeerStag_Dead fuer
#   junges  NCBearCub.glb      (Baeren-Junges, Skelett jfuss)
#   gen     NCBearCubGen.glb   (Generator-Junges, eigenes Skelett) + byte-gleicher Zwilling NCBearBenchCubGen.glb
# NEU (kein Original geaendert). Reines Python/numpy, kein Blender. Importiert den gemeinsamen Kern baer_kern_liegen.py (wird NICHT
# geaendert) und -- nur fuer Mess-Funktionen der Abnahme -- baer_spuren_gross_liegen.py (beide im selben Ordner) und ersetzt in einem
# vorhandenen GLB NUR die Kanaele von Death/Dead; alles andere bleibt byte-gleich (Kern: schreibe + pruefe_nur_liegen). Die Ziel-Tabellen
# (POSE.md T1, Abschnitt 8 = Abweichungen JUNGE, Abschnitt 9 = Nachbesserung 1) stehen HIER als Python-dict, damit der Befehl ohne
# _arbeit/ laeuft. Die Tabelle wird bei jedem Bau am Netz des Eingangs-GLB neu aufgeloest (Boden-Regeln).
#
# EIN Befehl je Koerper (wiederholbar, auch auf einem spaeteren GLB mit gleichen Knochen; zweimal gebaut = dieselbe Datei):
#   python baer_spuren_junges_liegen.py junges EIN/NCBearCub.glb    AUS/NCBearCub.glb    [--bericht B.json]
#   python baer_spuren_junges_liegen.py gen    EIN/NCBearCubGen.glb AUS/NCBearCubGen.glb [--zwilling AUS/NCBearBenchCubGen.glb] [--bericht B.json]
#   python baer_spuren_junges_liegen.py alle   EIN_ORDNER AUS_ORDNER [--md5 md5_junge.txt] [--bericht-ordner ORDNER]
#        (liest EIN_ORDNER/NCBearCub.glb + NCBearCubGen.glb, schreibt die drei Dateien nach AUS_ORDNER)
#   python baer_spuren_junges_liegen.py pruefe ALT.glb NEU.glb      (Beweis "nur Death/Dead", Kern)
# Schalter: --ohne-abnahme (nur bauen, nicht abbrechen), --schnell (Sturz nur jedes 3. Bild pruefen),
#           --versuch TABELLE.json (nur zum Ausprobieren: Tabelle aus einer Datei; kein Abgabe-Stand)
# Der Befehl bricht mit Fehlercode 2 ab (Datei wird dann NICHT geschrieben), wenn die Abnahme-Ziele aus POSE.md 5 verletzt sind
# (A1-A5, A7-A10 und N1 "Beine eilen dem Rumpf nicht voraus"; Schwellen unten in SCHWELLEN / A).
# SCHREIBSCHUTZ (Nachbesserung 1, Mangel T1): der Befehl schreibt nie auf seinen Eingang (auch nicht bei anderer Gross-/Kleinschreibung)
# und nie in einen Mod- oder Spielordner (.../Zomboid/mods/..., .../steamapps/...) -- weder GLB noch Zwilling, Bericht oder md5-Datei.
# Statisch gerechnet, nicht gespielt. Schreibt nur die genannten Ausgabe-Dateien.
import copy
import hashlib
import json
import math
import os
import shutil
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baer_kern_liegen as K  # noqa: E402
import baer_spuren_gross_liegen as G  # noqa: E402   nur Mess-Funktionen (_paar_schnell, gelenke, gelenk_fehler); liegt im selben Ordner

GENERATOR = "baer_spuren_junges_liegen.py (Lauf baer-liegen, Bauer JUNGE, Nachbesserung 1)"
KEYS = ("VL", "VR", "HL", "HR")

# ------------------------------------------------------------------ Ziel-Tabellen (relative Sprache, POSE.md Abschnitt 2)
_RUMPF = dict(boden_rumpf=-0.010, q_pel=[2, 0, 84], q_sp=[-1, 0, 84], q_ch=[-4, 3, 83], q_ne=[-4, 20, 80], q_he=[0, 16, 78],
              q_ta=[-12, 0, 80], klav=dict(L=-8, R=6), kiefer=0, kopf_boden=-0.003)
TABELLEN = {
    # Junges (NCBearCub.glb). Start war POSE.md T1 Spalte "Junges"; Bauer JUNGE (POSE.md Abschnitt 8): VL Pfote beuge 70 -> 25 (bei 70
    # faltet sich das Handgelenk: 27 Kanten unter halber Laenge, im TON-Bild als Schlitz zu sehen; bei 25 keine).
    # NACHBESSERUNG 1 (Mangel O2 "liegt wie ein umgekipptes Stofftier", POSE.md Abschnitt 9): die vier Beine stehen nicht mehr gerade
    # und parallel zur Bauchseite, sondern liegen wie bei den grossen Baeren gefaechert -- untere Beine weit nach vorn / hinten
    # (VR vor 24 -> 40, HR -32 -> -42; Dehnung 1,73 / 4,45 bei Schwelle 1,87 / 7,5), das obere Vorderbein nach vorn mit erhobenem
    # Ellbogen (vor 0 -> 25, senk 8 -> 12, pole z 0,5: Unterarm 19 statt 8 Grad geneigt, Pfote 7 cm tiefer), das obere Hinterbein nach
    # hinten mit erhobenem Knie (vor -4 -> -18, senk 14 -> 24, pole z 0,3: Unterschenkel 26 statt 13 Grad geneigt, Pfote 6-7 cm tiefer).
    # Grenzen (Gitter in _arbeit/baer_liegen/nach1/scan/): VL senk > 12 gibt mehr als 6 Naht-Punkte in der Achsel (A3), HL senk > 24
    # drueckt in den Bauch bzw. abd < -15, pole z hoeher reisst den Twist (vorn 20, hinten 15 Grad).
    "junges": dict(_RUMPF, pel_xy=[-0.3748, -0.24], bein=dict(
        VR=dict(s=0.97, vor=40, boden=0.0, pfote=dict(beuge=20)),
        HR=dict(s=0.925, vor=-42, boden=0.0, pfote=dict(beuge=10)),
        VL=dict(s=0.95, vor=25, senk=12, pole=[-1, 0, 0.5], pfote=dict(beuge=25)),
        HL=dict(s=0.925, vor=-18, senk=24, pole=[1, 0, 0.3], pfote=dict(beuge=7)))),
    # Generator-Junges (NCBearCubGen.glb). Start war POSE.md T1 Spalte "Generator-Junges" (Dehnung max 4,59, offen A7); Bauer JUNGE:
    # die Staffelung der Vorderpfoten kleiner und die der Hinterpfoten auf beide Beine verteilt (VR 40 -> 30, HR -30 -> -20): Dehnung
    # max 3,18 (heute 3,24). VL Pfote beuge 70 -> 25 (bei 70 liegt ein Faltenring um das Handgelenk).
    # NACHBESSERUNG 1 (Mangel O2, POSE.md Abschnitt 9): die oberen Beine haengen mit erhobenem Ellbogen / Knie statt waagerecht zu
    # stehen und zeigen auseinander -- VL senk 4 -> 10, pole z 0,5 (Unterarm 19 statt 3 Grad geneigt, Pfote 8 cm tiefer);
    # HL vor +8 -> -8, senk 4 -> 12, pole z 0,3 (Unterschenkel 18 statt 3 Grad geneigt, Pfote 5 cm tiefer). Die unteren Beine bleiben
    # (VR 30, HR -20): jede weitere Staffelung reisst die Dehnung (VR 36: 3,69, HR -28: 4,31 bei Schwelle 3,3).
    # Grenzen: VL senk > 10 bringt die obere Vorderpfote naeher als 10 cm an die untere (A2), HL senk 16 laesst die Hinterpfoten im
    # Sturz mit 1 cm aneinander vorbeigehen, HL vor +8 mit senk > 12 verdeckt von vorn die untere Hinterpfote (A6 > 0,20).
    "gen": dict(_RUMPF, pel_xy=[-0.3416, -0.2374], bein=dict(
        VR=dict(s=0.94, vor=30, boden=0.0, pfote=dict(beuge=20)),
        HR=dict(s=0.87, vor=-20, boden=0.0, pfote=dict(beuge=10)),
        VL=dict(s=0.94, vor=4, senk=10, pole=[-1, 0, 0.5], pfote=dict(beuge=25)),
        HL=dict(s=0.87, vor=-8, senk=12, pole=[1, 0, 0.3], pfote=dict(beuge=6)))),
}
MD5_PFAD = "42/media/models_X/Skinned/"                 # Pfad-Vorsatz in der md5-Datei (wie out/md5.txt)
DATEI = {"junges": "NCBearCub.glb", "gen": "NCBearCubGen.glb"}
ZWILLING = {"gen": "NCBearBenchCubGen.glb"}

# ------------------------------------------------------------------ Abnahme-Schwellen (POSE.md 5; Groesse 1,0)
SCHWELLEN = {
    "junges": dict(auflage_cm2=200.0, dehnung99=1.87, dehnung_max=7.5),
    "gen": dict(auflage_cm2=400.0, dehnung99=1.80, dehnung_max=3.3),
}
A = dict(pfoten_abstand_cm=10.0, rumpf_punkte=6, rumpf_tiefe_cm=1.5, boden=(-1.5, 0.0), kopf=(-1.0, 0.5), bein_unten=(-0.5, 0.5),
         sturz_boden=(-1.5, 0.6), drehsprung_grad=12.0, vorlauf_grad=8.0, kopf_mm=0.01, kiefer_grad=0.05)


# ------------------------------------------------------------------ Sturz (Death): Zeitform je Bein
# Der Sturz selbst ist die Regel des Kerns (K.sturz: heutige Spur, im Gelenkraum auf die neue Endpose geblendet; Rumpf-Fortschritt k
# von pose_death in baer_kampf_gross.py -> gleiche Kipp-Zeit, gleicher Aufschlag, gleiche Dauer; danach K.boden_je_bild).
# ABWEICHUNG vom Kern (gemeldet in BAU_JUNGE.md): das Gewicht der Bein-Knochen laeuft JE BEIN (kVL, kVR, kHL, kHR) statt je
# Koerperseite (kL, kR); dafuer wird K.gruppe waehrend des Aufrufs von K.sturz durch gruppe_je_bein ersetzt (der Kern bleibt unberuehrt).
#   w = ssf(a, b, k):  Kern  rechts (0,18, 1,0), links (0,03, 1,0).
#   Eintrag (a, b)          Regel des Kerns:  q = q_heute(f) * slerp(1, q_heute(ende)^-1 * q_neu(ende), w)   (Unterschied der Endposen DAZU)
#   Eintrag (a, b, "ziel")  auf das Ziel geblendet:  q = slerp(q_heute(f), q_neu(ende), w)   (Nachbesserung 1: Eigenheiten der heutigen
#                           Spur -- Huepfer, Wegstrecken -- klingen mit 1 - w ab; bei w = 1 haengt das Bein starr am Rumpf)
# Wiederholbar: traegt der Eingang die Endpose schon (zweiter Lauf auf dem eigenen Ergebnis), bleibt die Spur stehen.
# Gemessen an allen 78 Bildern (_arbeit/baer_liegen/nach1/scan/, Werkzeuge nach1/werkzeug/sturz_scan.py, kombi_scan.py):
#   Junges  Bauer JUNGE hatte die linken (oberen) Beine bei halbem Kippen fertig (0, 0,5): sie standen schon waagerecht zur Seite, als
#           der Rumpf erst 24..43 Grad gekippt war (Mangel O1, Vorlauf 22,6 / 16,2 Grad). NACHBESSERUNG 1: VL (0, 0,9), HL (0, 0,8) --
#           die Beine folgen dem Rumpf (Vorlauf hoechstens 0,9 Grad), weiter 0 Punkte in allen Bein-Paaren. Unteres Hinterbein HR
#           (0,3, 1,0) statt (0, 0,8): es wandert erst nach hinten, wenn der Rumpf kippt (Mangel O5: bis 102 statt 159 Punkte im Bauch;
#           spaeter als 0,3 reisst den Drehsprung ueber 12 Grad). VR bleibt (0, 0,8).
#   Gen-J.  die heutige Spur (per IK umgerechnet) hat Eigenheiten: die linke Vorderpfote huepft zwischen Bild 36 und 37 (Mangel O4) und
#           schwingt in Bild 35/36 DURCH die rechte, das linke Hinterbein schlaegt in Bild 24-29 nach aussen. Linke Beine deshalb auf
#           das ZIEL geblendet -- VL (0, 0,7, "ziel"), HL (0, 0,35, "ziel"): 0 Punkte in allen 78 Bildern, Huepfer weg, Vorlauf
#           hoechstens 5,4 / 6,7 Grad. Rechte Beine wie Bauer JUNGE: VR (0, 0,5), HR (0, 0,8) (die rechten Beine NICHT auf das Ziel
#           blenden: sie laegen dann flach, waehrend der Rumpf noch steht, und die Boden-Regel muesste das Becken 15 cm heben).
FORM = {
    "junges": dict(VR=(0.0, 0.8), HR=(0.3, 1.0), VL=(0.0, 0.9), HL=(0.0, 0.8)),
    "gen": dict(VR=(0.0, 0.5), HR=(0.0, 0.8), VL=(0.0, 0.7, "ziel"), HL=(0.0, 0.35, "ziel")),
}
_KERN_GRUPPE = K.gruppe                                  # Original des Kerns (wird nur waehrend K.sturz ersetzt)
_BEIN_VON = {}
for _key, _sn, _a, _b, _c in K.BEINE:
    for _teil in (_a, _b, _c) + (("Toe0",) if _a == "Thigh" else ()):
        _BEIN_VON["Bip01_%s_%s" % (_sn, _teil)] = "k" + _key


def gruppe_je_bein(name):
    """wie K.gruppe, aber die Bein-Knochen je Bein getrennt (kVL, kVR, kHL, kHR) statt je Koerperseite (kL, kR)."""
    return _BEIN_VON.get(name) or _KERN_GRUPPE(name)


def sturz_gewichte(n, art):
    """Gewicht je Bild und Gruppe (k Rumpf, kopf, je Bein kVL/kVR/kHL/kHR): Zeitform des Kerns, die Bein-Kurven kommen aus FORM[art]."""
    Gw = K.sturz_gewichte(n)
    for g in Gw:
        for bein, form in FORM[art].items():
            g["k" + bein] = 1.0 if g is Gw[-1] else K.ssf(form[0], form[1], g["k"])
    return Gw


def sturz_junge(rig, alt, t_end, q_end, Gw, art=None):
    """Death neu = K.sturz mit Gewichten je Bein; Beine mit FORM-Eintrag (a, b, "ziel") werden auf das Ziel geblendet. Liefert (t, q)."""
    K.gruppe = gruppe_je_bein                            # Kern-Funktion nur fuer diesen Aufruf ersetzt
    try:
        t, q = K.sturz(rig, alt, t_end, q_end, Gw)
    finally:
        K.gruppe = _KERN_GRUPPE
    ziel = {"k" + bein for bein, form in FORM.get(art, {}).items() if len(form) > 2 and form[2] == "ziel"}
    n = len(alt["T"])
    for i, name in enumerate(rig.name):
        g = _BEIN_VON.get(name)
        if g not in ziel:
            continue
        if K.winkel(K.q_mat(alt["q"][-1, i]), K.q_mat(q_end[i])) < 1e-4:
            continue                                     # Eingang traegt die Endpose schon: Spur bleibt (wie im Kern)
        for f in range(n):
            w = Gw[f][g]
            if w <= 0.0:
                q[f, i] = alt["q"][f, i]                 # Gewicht 0: Schluessel genau wie heute
                continue
            qq = K.q_slerp(alt["q"][f, i], q_end[i], w)
            if f and float(qq @ q[f - 1, i]) < 0:
                qq = -qq
            q[f, i] = qq
        qe = np.asarray(q_end[i], float)
        q[-1, i] = qe if float(qe @ q[-2, i]) >= 0 else -qe
    return t, q


def spuren_junge(rig, t_end, q_end, Gw, unten=-0.012, oben=0.005, art=None):
    """wie K.spuren, aber mit sturz_junge: Death am Boden gehalten (K.boden_je_bild), Dead = genau das letzte Death-Bild."""
    death, dead = rig.clip("DeerStag_Death"), rig.clip("DeerStag_Dead")
    t2, q2 = sturz_junge(rig, death, t_end, q_end, Gw, art)
    t2, z0, z1, c = K.boden_je_bild(rig, t2, q2, death["s"], unten, oben)
    info = dict(sturz_tief_vor_cm=z0, sturz_tief_cm=z1, becken_korrektur_cm=c)
    # Einrasten: Schluessel, die sich vom Eingang um weniger als 1e-7 unterscheiden (Lage: 0,2 Mikrometer; Drehung: Rundung von float32),
    # bleiben GENAU die des Eingangs. Dadurch liefert ein zweiter Lauf auf dem eigenen Ergebnis dieselbe Datei (gleiche MD5).
    nah = np.abs(t2 - death["t"]).max(axis=2) < 1e-7
    t2[nah] = death["t"][nah]
    vz = np.sign(np.einsum("fij,fij->fi", q2, death["q"]))[:, :, None]
    nah = np.abs(q2 * vz - death["q"]).max(axis=2) < 1e-7
    q2[nah] = death["q"][nah]
    td, qd = dead["t"].copy(), dead["q"].copy()
    ip = rig.ix["Bip01_Pelvis"]
    for i, name in enumerate(rig.name):
        if name.startswith("Bip01_"):
            qd[:, i] = q2[-1, i]
    td[:, ip] = t2[-1, ip]
    return {"DeerStag_Death": dict(t=t2, q=q2), "DeerStag_Dead": dict(t=td, q=qd)}, info


# ------------------------------------------------------------------ Messen
def _paare_bild(rig, T, P, mit_rumpf=True):
    F = rig.F
    paare = {}
    for i, a in enumerate(KEYS):
        for b in KEYS[i + 1:]:
            paare["pfote_%s-pfote_%s" % (a, b)] = K.paar(P, F, T["pfote_" + a], T["pfote_" + b])
            paare["bein_%s-bein_%s" % (a, b)] = K.paar(P, F, T["bein_" + a], T["bein_" + b])
    if mit_rumpf:
        koerper = T["rumpf"] | T["hals"] | T["kopf"]
        for a in KEYS:
            paare["bein_%s-rumpf" % a] = K.paar(P, F, T["bein_" + a], koerper)
            andere = np.zeros(len(P), bool)
            for b in KEYS:
                if b != a:
                    andere |= T["oben_" + b]
            paare["bein_%s-schenkel_andere" % a] = K.paar(P, F, T["bein_" + a], andere)
    return paare


def messe_endpose(rig, T, P):
    """Endpose (Dead): Boden, Auflage, Durchdringung je Paar, Pfotenabstand, Dehnung (wie werkzeug/mess_liegen.py, ohne Kamera)."""
    paare = _paare_bild(rig, T, P)
    d99, dmax = K.dehnung(rig, P, T)
    return dict(
        tief_cm=round(100 * float(P[:, 2].min()), 2),
        rumpf_tief_cm=round(100 * min(float(P[T[k], 2].min()) for k in K.RUMPF_TEILE), 2),
        kopf_tief_cm=round(100 * float(P[T["kopf"], 2].min()), 2),
        bein_tief_cm={k: round(100 * float(P[T["bein_" + k], 2].min()), 2) for k in KEYS},
        pfote_hoehe_cm={k: [round(100 * float(P[T["pfote_" + k], 2].min()), 1), round(100 * float(P[T["pfote_" + k], 2].max()), 1)] for k in KEYS},
        auflage_cm2=round(K.auflage(P, rig.F, 0.01), 0), auflage2_cm2=round(K.auflage(P, rig.F, 0.02), 0),
        pfote_mitte={k: [round(float(v), 3) for v in P[T["pfote_" + k]].mean(0)] for k in KEYS},
        paare=paare,
        pfote_bein_punkte=int(sum(v["a_in_b"] + v["b_in_a"] for k, v in paare.items() if "rumpf" not in k and "schenkel" not in k)),
        pfoten_abstand_min_cm=min(v["abstand_cm"] for k, v in paare.items() if k.startswith("pfote_")),
        dehnung=[round(d99, 2), round(dmax, 2)])


# --- Sturz je Bild (alle 78 Bilder; ueber mehrere Prozesse verteilt, ohne Pool der Reihe nach mit gleichem Ergebnis)
_W = {}


def _w_start(pfad):
    rig = K.Rig(pfad)
    _W["rig"], _W["T"], _W["death"] = rig, K.teile(rig), rig.clip("DeerStag_Death")


def _abstand_cm(P, ma, mb):
    ia, ib = np.nonzero(ma)[0], np.nonzero(mb)[0]
    d = 9.0
    for i in range(0, len(ia), 300):
        d = min(d, float(np.linalg.norm(P[ia[i:i + 300]][:, None] - P[ib][None], axis=2).min()))
    return round(100 * d, 2)


def _bild_messen(rig, T, P, mit_paaren=True):
    """Je Bild: Punkte in den 6 Bein-Paaren (bein_ = Unterbein + Pfote, enthaelt das Pfoten-Paar), kleinster Abstand zweier Beine,
    Tiefe Bein gegen Rumpf + Hals + Kopf je Bein (cm; gleiche Aussage wie K.paar, schneller: G._paar_schnell)."""
    F = rig.F
    out = dict(punkte=0, eng_cm=900.0, rumpf_cm={})
    if mit_paaren:
        for i, a in enumerate(KEYS):
            for b in KEYS[i + 1:]:
                out["punkte"] += G._paar_schnell(P, F, T["bein_" + a], T["bein_" + b])[0]
                out["eng_cm"] = min(out["eng_cm"], _abstand_cm(P, T["bein_" + a], T["bein_" + b]))
    koerper = T["rumpf"] | T["hals"] | T["kopf"]
    for a in KEYS:
        out["rumpf_cm"][a] = G._paar_schnell(P, F, T["bein_" + a], koerper)[1]
    return out


def _w_bild(a):
    f, tn, qn = a
    rig, T, death = _W["rig"], _W["T"], _W["death"]
    neu = _bild_messen(rig, T, rig.haut_tier(rig.welt(tn, qn, death["s"][f])))
    heute = _bild_messen(rig, T, rig.haut_tier(rig.welt(death["t"][f], death["q"][f], death["s"][f])), mit_paaren=False)
    return f, neu, heute


def sturz_bilder_messen(pfad, tn, qn, bilder):
    auf = [(int(f), tn[f], qn[f]) for f in bilder]
    try:
        import multiprocessing as mp
        with mp.Pool(max(1, min(16, (os.cpu_count() or 2) - 2, len(auf))), initializer=_w_start, initargs=(pfad,)) as pool:
            return sorted(pool.map(_w_bild, auf, chunksize=1), key=lambda x: x[0])
    except Exception as e:                                           # z. B. kein Pool erlaubt: langsam, aber gleiches Ergebnis
        print("LIEGEN Hinweis: Sturz-Messung ohne Pool (%s)" % e)
        _w_start(pfad)
        return [_w_bild(a) for a in auf]


def vorlauf(rig, L, t, q):
    """N1 (Nachbesserung 1, Mangel O1): Schwenk der OBEREN Beine (VL, HL: Schulter/Huefte -> Hand-/Sprunggelenk, in der Kipp-Ebene y-z)
    minus Rollen des Rumpfs (vorn Brust Spine1, hinten Becken), beide gegen Bild 0. Positiv = das Bein eilt dem Rumpf voraus
    ("streckt sich zur Seite, bevor der Koerper kippt"). Liefert {bein: Liste je Bild in Grad}."""
    n = t.shape[0]
    roh = {k: [] for k in ("VL", "HL")}
    for f in range(n):
        pose = L.lesen(t[f], q[f])
        roll = dict(V=K.euler_von(pose["Bip01_Spine1"][0])[2], H=K.euler_von(pose["Bip01_Pelvis"][0])[2])
        for key in roh:
            L_ = L.LEG[key]
            d = pose[L_["fuss"]][1] - pose[L_["oben"]][1]
            roh[key].append(math.degrees(math.atan2(d[1], -d[2])) - roll[key[0]])
    return {k: [round(v - w[0], 2) for v in w] for k, w in roh.items()}


def messe_sturz(rig, L, T, clip_alt, t, q, schritt=1):
    """Sturz: je Bild (jedes 'schritt'-te + letztes) Punkte in den Bein-Paaren, engster Bein-Abstand, Bein gegen Rumpf je Bein neu und
    heute; groesster Drehsprung zwischen Nachbarbildern und Vorlauf der oberen Beine (alle Bilder)."""
    n = t.shape[0]
    bilder = sorted(set(list(range(0, n, schritt)) + [n - 1]))
    res = sturz_bilder_messen(rig.pfad, t, q, bilder)
    out = dict(bilder=bilder, paar_punkte=[r[1]["punkte"] for r in res], eng_cm=[r[1]["eng_cm"] for r in res],
               rumpf_tiefe_cm=[max(r[1]["rumpf_cm"].values()) for r in res], rumpf_tiefe_heute_cm=[max(r[2]["rumpf_cm"].values()) for r in res],
               rumpf_je_bein_cm={k: [r[1]["rumpf_cm"][k] for r in res] for k in KEYS},
               rumpf_je_bein_heute_cm={k: [r[2]["rumpf_cm"][k] for r in res] for k in KEYS})
    d = np.abs(np.einsum("fni,fni->fn", q[1:], q[:-1])) / (np.linalg.norm(q[1:], axis=2) * np.linalg.norm(q[:-1], axis=2))
    out["drehsprung_grad"] = round(float(np.degrees(2.0 * np.arccos(np.clip(d, -1.0, 1.0))).max()), 2)
    out["vorlauf_grad"] = vorlauf(rig, L, t, q)
    return out


def tiefe_alle_bilder(rig, clip_alt, t, q):
    return [round(100 * float(rig.haut_tier(rig.welt(t[f], q[f], clip_alt["s"][f]))[:, 2].min()), 2) for f in range(t.shape[0])]


# ------------------------------------------------------------------ Bau
def rechne(gerippe, art, Z=None):
    """Tabelle am Netz von 'gerippe' aufloesen und beide Clips rechnen. Liefert dict (rig, L, T, Za, pose, t, q, neu, sturz-info)."""
    Z = copy.deepcopy(TABELLEN[art] if Z is None else Z)
    rig = K.Rig(gerippe)
    L = K.Loeser(rig)
    T = K.teile(rig)
    Za, info = K.aufloesen(rig, L, T, Z)
    stat = {}
    pose = L.welt_pose(Za, stat)
    t, q = L.lokal(pose)
    n = len(rig.clip("DeerStag_Death")["T"])
    neu, si = spuren_junge(rig, t, q, sturz_gewichte(n, art), art=art)
    return dict(rig=rig, L=L, T=T, Z=Z, Za=Za, info=info, stat=stat, pose=pose, t=t, q=q, neu=neu, sturz=si)


def abnahme(art, r, schritt=1):
    """Prueft A1-A5, A7-A10 (POSE.md 5) und N1. Liefert (Liste der Verstoesse, Messwerte)."""
    rig, L, T, S = r["rig"], r["L"], r["T"], SCHWELLEN[art]
    P = rig.haut_tier(rig.welt(r["t"], r["q"]))
    m = messe_endpose(rig, T, P)
    f = []
    if m["pfote_bein_punkte"] != 0:
        f.append("A1 Pfoten-/Bein-Paare: %d Punkte ineinander" % m["pfote_bein_punkte"])
    if m["pfoten_abstand_min_cm"] < A["pfoten_abstand_cm"]:
        f.append("A2 Pfotenabstand %.2f cm < %.1f" % (m["pfoten_abstand_min_cm"], A["pfoten_abstand_cm"]))
    for k, v in m["paare"].items():
        if ("rumpf" in k or "schenkel" in k) and (v["a_in_b"] + v["b_in_a"] > A["rumpf_punkte"] or v["tiefe_cm"] > A["rumpf_tiefe_cm"]):
            f.append("A3 %s: %d Punkte, %.2f cm" % (k, v["a_in_b"] + v["b_in_a"], v["tiefe_cm"]))
    for nm, wert, (lo, hi) in (("gesamt", m["tief_cm"], A["boden"]), ("Rumpf", m["rumpf_tief_cm"], A["boden"]), ("Kopf", m["kopf_tief_cm"], A["kopf"]),
                               ("Bein VR", m["bein_tief_cm"]["VR"], A["bein_unten"]), ("Bein HR", m["bein_tief_cm"]["HR"], A["bein_unten"])):
        if not (lo - 0.005 <= wert <= hi + 0.005):
            f.append("A4 Boden %s %+.2f cm ausserhalb %s" % (nm, wert, (lo, hi)))
    if m["auflage_cm2"] < S["auflage_cm2"]:
        f.append("A5 Auflage %d cm2 < %d" % (m["auflage_cm2"], S["auflage_cm2"]))
    if m["dehnung"][0] > S["dehnung99"] + 0.005 or m["dehnung"][1] > S["dehnung_max"] + 0.005:
        f.append("A7 Dehnung %s ueber %.2f / %.2f" % (m["dehnung"], S["dehnung99"], S["dehnung_max"]))
    # A8 Gelenke der Endpose (Grenzen wie baer_kampf_gross.py:580 und POSE.md 2, samt Twist; Mess-Funktionen des GROSS-Skripts)
    g = G.gelenke(L, r["pose"])
    f += G.gelenk_fehler(g)
    m["gelenke"] = g
    if r["stat"].get("ueber"):
        f.append("A8 Bein ueberstreckt (IK): %s" % r["stat"]["ueber"])
    # A10 Kopf starr: Kiefer in Ruhe; Punkte, die ganz an Kopf/Kiefer haengen, gegeneinander unveraendert
    ij, ih = rig.ix["Bip01_Jaw"], rig.ix["Bip01_Head"]
    kiefer = K.winkel(K.q_mat(rig.q0[ij]), K.q_mat(r["q"][ij]))
    Gw = rig.gewichte()
    starr = np.nonzero(Gw[:, ih] + Gw[:, ij] > 0.9999)[0]
    P0 = rig.haut_tier(rig.W0)
    pr = starr[:: max(1, len(starr) // 400)]
    kopf_mm = float(np.abs(np.linalg.norm(P[pr][:, None] - P[pr][None], axis=2) - np.linalg.norm(P0[pr][:, None] - P0[pr][None], axis=2)).max() * 1000.0)
    m["kopf"] = dict(kiefer_grad=round(kiefer, 3), punkte_starr=int(len(starr)), abstand_fehler_mm=round(kopf_mm, 5))
    if kiefer > A["kiefer_grad"] or kopf_mm > A["kopf_mm"]:
        f.append("A10 Kopf: Kiefer %.3f Grad, Abstandsfehler %.5f mm" % (kiefer, kopf_mm))
    # A9 Sturz
    alt = rig.clip("DeerStag_Death")
    tn, qn = r["neu"]["DeerStag_Death"]["t"], r["neu"]["DeerStag_Death"]["q"]
    s = messe_sturz(rig, L, T, alt, tn, qn, schritt)
    s["tief_alle_cm"] = tiefe_alle_bilder(rig, alt, tn, qn)
    lo, hi = A["sturz_boden"]
    if min(s["tief_alle_cm"]) < lo - 0.005 or max(s["tief_alle_cm"]) > hi + 0.005:
        f.append("A9 Sturz-Boden %.2f..%.2f cm ausserhalb %s" % (min(s["tief_alle_cm"]), max(s["tief_alle_cm"]), (lo, hi)))
    if max(s["paar_punkte"]) != 0:
        f.append("A9 Sturz: Pfoten-/Bein-Paare ineinander in Bild %s" % [b for b, p in zip(s["bilder"], s["paar_punkte"]) if p])
    # Bein gegen Rumpf je Bild nicht tiefer als heute im selben Bild; die Naht-Toleranz von A3 (1,5 cm) gilt auch hier (wie GROSS)
    schlechter = [(b, a_, h) for b, a_, h in zip(s["bilder"], s["rumpf_tiefe_cm"], s["rumpf_tiefe_heute_cm"]) if a_ > max(h, A["rumpf_tiefe_cm"]) + 0.05]
    if schlechter:
        f.append("A9 Sturz: Bein gegen Rumpf tiefer als heute in %d Bildern, (Bild, neu, heute) %s" % (len(schlechter), schlechter[:6]))
    if s["drehsprung_grad"] > A["drehsprung_grad"]:
        f.append("A9 Drehsprung %.2f Grad > %.1f" % (s["drehsprung_grad"], A["drehsprung_grad"]))
    for bein, w in s["vorlauf_grad"].items():
        if max(w) > A["vorlauf_grad"]:
            f.append("N1 oberes Bein %s eilt dem Rumpf %.1f Grad voraus (Bild %d) > %.1f" % (bein, max(w), int(np.argmax(w)), A["vorlauf_grad"]))
    Gs = sturz_gewichte(len(alt["T"]), art)
    fest = [i for i, g_ in enumerate(Gs) if max(g_.values()) <= 0.0]
    s["bilder_bit_gleich"] = len(fest)
    for i in fest:
        if not (np.array_equal(tn[i].astype(np.float32), alt["t"][i].astype(np.float32)) and np.array_equal(qn[i].astype(np.float32), alt["q"][i].astype(np.float32))):
            f.append("A9 Bild %d (Gewicht 0) nicht bit-gleich zu heute" % i)
            break
    td, qd = r["neu"]["DeerStag_Dead"]["t"], r["neu"]["DeerStag_Dead"]["q"]
    if not (np.array_equal(td[0].astype(np.float32), tn[-1].astype(np.float32)) and np.array_equal(qd[0].astype(np.float32), qn[-1].astype(np.float32))
            and np.array_equal(td[0], td[-1]) and np.array_equal(qd[0], qd[-1])):
        f.append("A9 letztes Death-Bild != Dead")
    m["sturz"] = s
    return f, m


def md5(pfad):
    return hashlib.md5(open(pfad, "rb").read()).hexdigest()


def _norm(p):
    return os.path.normcase(os.path.abspath(p)).replace("\\", "/")


def schreibschutz(ein, *ziele):
    """T1: kein Ziel ist der Eingang (auch nicht bei anderer Gross-/Kleinschreibung oder als Verweis auf dieselbe Datei) und kein Ziel
    liegt in einem Mod- oder Spielordner. Liefert die Liste der Verstoesse."""
    f = []
    e = _norm(ein)
    for z in ziele:
        if not z:
            continue
        zn = _norm(z)
        gleich = zn == e
        if not gleich and os.path.exists(z) and os.path.exists(ein):
            try:
                gleich = os.path.samefile(z, ein)
            except OSError:
                gleich = False
        if gleich:
            f.append("EIN und AUS sind dieselbe Datei (%s) -- der Eingang wird nur gelesen" % z)
        if "/zomboid/mods/" in zn + "/" or "/steamapps/" in zn + "/":
            f.append("AUS liegt in einem Mod-/Spielordner (%s) -- dieses Skript schreibt nie dorthin (Einbau macht der Integrator)" % z)
    return f


def baue(art, ein, aus, bericht=None, zwilling=None, mit_abnahme=True, schritt=1, still=False, Z=None):
    """EIN Schritt: Death/Dead in 'ein' ersetzen -> 'aus' (+ byte-gleicher Zwilling). 'ein' wird nur gelesen. Bricht ab (Fehlercode 2,
    nichts geschrieben), wenn der Schreibschutz oder die Abnahme verletzt ist."""
    sperre = schreibschutz(ein, aus, zwilling, bericht)
    if sperre:
        for x in sperre:
            print("LIEGEN_JUNGE_FEHLER %s: %s" % (art, x))
        raise SystemExit(2)
    r = rechne(ein, art, Z)
    fehler, m = abnahme(art, r, schritt) if mit_abnahme else ([], {})
    if not still and m:
        s = m["sturz"]
        print("LIEGEN %s Endpose: tief %+.2f cm, Rumpf %+.2f, Kopf %+.2f, Beine unten VR %+.2f HR %+.2f, Auflage %d cm2, Pfote/Bein-Paare %d Punkte, "
              "Pfotenabstand min %.2f cm, Dehnung %s" % (art, m["tief_cm"], m["rumpf_tief_cm"], m["kopf_tief_cm"], m["bein_tief_cm"]["VR"],
                                                         m["bein_tief_cm"]["HR"], m["auflage_cm2"], m["pfote_bein_punkte"], m["pfoten_abstand_min_cm"], m["dehnung"]))
        print("LIEGEN %s Sturz (%d Bilder): Boden %.2f..%.2f cm, Paare max %d Punkte, engster Bein-Abstand %.2f cm, Bein-Rumpf tiefste %.2f cm (heute bis %.2f), "
              "Drehsprung %.2f Grad, Vorlauf obere Beine VL %.1f HL %.1f Grad, Bilder bit-gleich 0..%d"
              % (art, len(s["bilder"]), min(s["tief_alle_cm"]), max(s["tief_alle_cm"]), max(s["paar_punkte"]), min(s["eng_cm"]), max(s["rumpf_tiefe_cm"]),
                 max(s["rumpf_tiefe_heute_cm"]), s["drehsprung_grad"], max(s["vorlauf_grad"]["VL"]), max(s["vorlauf_grad"]["HL"]), s["bilder_bit_gleich"] - 1))
    if fehler:
        for x in fehler:
            print("LIEGEN ABNAHME VERLETZT:", x)
        raise SystemExit(2)
    os.makedirs(os.path.dirname(os.path.abspath(aus)), exist_ok=True)
    tmp = aus + ".tmp"
    w = K.schreibe(ein, tmp, r["neu"], generator=GENERATOR, still=True)
    os.replace(tmp, aus)
    if zwilling:
        shutil.copyfile(aus, zwilling)
        assert md5(zwilling) == w["md5"]
    out = dict(art=art, eingang=ein, eingang_md5=md5(ein), ausgang=aus, md5=w["md5"], zwilling=zwilling, neu=w["neu"], andere_clips_byte_gleich=[w["gleich"], w["alle"]],
               tabelle=r["Z"], form={k: list(v) for k, v in FORM[art].items()}, ziele_abs=r["Za"], stat=r["stat"], info=r["info"], mess=m,
               becken_korrektur_cm=r["sturz"].get("becken_korrektur_cm"),
               bein_winkel={k: K.bein_winkel(r["L"], r["pose"], k) for k in r["L"].LEG}, rumpf_winkel=K.rumpf_winkel(r["pose"]))
    if bericht:
        json.dump(out, open(bericht, "w"), indent=1)
    if not still:
        print("LIEGEN %s -> %s MD5 %s (andere Clips byte-gleich %d/%d Sampler-Puffer, Netz/Skin/Knoten byte-gleich)%s"
              % (art, aus, w["md5"], w["gleich"], w["alle"], (" + Zwilling " + zwilling) if zwilling else ""))
    return out


def _opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "pruefe":
        print("NUR_LIEGEN_OK", json.dumps(K.pruefe_nur_liegen(a[1], a[2])))
        return
    kw = dict(mit_abnahme="--ohne-abnahme" not in a, schritt=3 if "--schnell" in a else 1)
    if _opt(a, "--versuch"):
        # nur zum Ausprobieren im Arbeitsordner: Tabelle aus einer JSON-Datei statt aus TABELLEN (das Ergebnis ist dann KEIN Abgabe-Stand)
        kw["Z"] = json.load(open(_opt(a, "--versuch")))
        print("LIEGEN VERSUCH: Tabelle aus", _opt(a, "--versuch"))
    if len(a) >= 3 and a[0] in TABELLEN:
        baue(a[0], a[1], a[2], bericht=_opt(a, "--bericht"), zwilling=_opt(a, "--zwilling"), **kw)
    elif len(a) >= 3 and a[0] == "alle":
        ein, aus = a[1], a[2]
        bo = _opt(a, "--bericht-ordner")
        # Schreibschutz fuer ALLE Ziele, bevor irgendetwas gerechnet oder geschrieben wird
        sperre = []
        for art in ("junges", "gen"):
            sperre += schreibschutz(os.path.join(ein, DATEI[art]), os.path.join(aus, DATEI[art]),
                                    os.path.join(aus, ZWILLING[art]) if art in ZWILLING else None,
                                    os.path.join(bo, "bau_%s.json" % art) if bo else None, _opt(a, "--md5"))
            if art in ZWILLING:
                sperre += schreibschutz(os.path.join(ein, ZWILLING[art]), os.path.join(aus, DATEI[art]), os.path.join(aus, ZWILLING[art]))
        if sperre:
            for x in sorted(set(sperre)):
                print("LIEGEN_JUNGE_FEHLER alle: %s" % x)
            raise SystemExit(2)
        zeilen = []
        for art in ("junges", "gen"):
            zw = os.path.join(aus, ZWILLING[art]) if art in ZWILLING else None
            r = baue(art, os.path.join(ein, DATEI[art]), os.path.join(aus, DATEI[art]), zwilling=zw,
                     bericht=os.path.join(bo, "bau_%s.json" % art) if bo else None, **kw)
            zeilen.append("%s  %s%s" % (r["md5"], MD5_PFAD, DATEI[art]))
            if zw:
                zeilen.append("%s  %s%s" % (md5(zw), MD5_PFAD, ZWILLING[art]))
        if _opt(a, "--md5"):
            open(_opt(a, "--md5"), "w", newline="\n").write("\n".join(zeilen) + "\n")
        print("\n".join(zeilen))
    else:
        print(__doc__ or "")
        print("Aufruf: python baer_spuren_junges_liegen.py junges|gen EIN.glb AUS.glb [--zwilling Z.glb] [--bericht B.json] [--ohne-abnahme] [--schnell]")
        print("        python baer_spuren_junges_liegen.py alle EIN_ORDNER AUS_ORDNER [--md5 DATEI] [--bericht-ordner ORDNER]")
        print("        python baer_spuren_junges_liegen.py pruefe ALT.glb NEU.glb")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
