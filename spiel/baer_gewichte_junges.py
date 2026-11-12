# Lauf baer-junges (10.11.2026), Bau Koerper: Kopie von baer_gewichte_2c.py (Original unveraendert), erzeugt von
# _arbeit/baer_junges/werkzeug/patch/mache_gewichte_junges.py. Hautgewichte des Baeren-Jungen NCBearCub gegen die Clips des JUNGEN
# (Dump des GLB mit den endgueltigen Sitz-Clips, NCB_GEW_DUMP). Eingang: npz mit V (Ruhe des Jungen), V_erw (Urbild = Erwachsener 2c,
# gleiche Punkt-Nummern), T, W (Start = gewichte_2c.npz), namen, kralle. Zonen, Schwellen und Regionen werden am Urbild ausgewertet.
# Aufruf: python baer_gewichte_junges.py START.npz LP_JUNGES.npz AUS.npz [schluessel=wert,...]
# Lauf baer-2c (10.11.2026): Kopie von baer_gewichte_pfote.py (Original unveraendert); Aenderungen mit "2c" kommentiert.
# Nachbesserung fix1 baer-2c (10.11.2026, Pruefbericht B1/B2/m2): (1) Clip-Matrizen aus dem 2c-GLB (neue Sitz-Clips) statt des alten
#   Bestands-Dumps (NCB_GEW_DUMP, Vorgabe _arbeit/baer_2c/fix1/clips/dump_fix1_clips.pkl = Clips des fix1-GLB); (2) swipe=1: SwipeL/SwipeR Bilder 6-23 einzeln
#   (Achsel-Spitze lag in Bild 13/18 zwischen den 5er-Schritten); (3) liege=k: Falten-Strafe in den Liegebildern (Dead, Death ab 75 %)
#   k-fach; (4) band_z0/band_z1: Uebergangsband der Falten-Zone (Vorgabe 0,18-0,40 wie fix1 baer-pfoten).
# Lauf baer-pfoten (09.11.2026): Kopie von baer_gewichte_fell.py (Original bleibt). Neu: (1) Punkte, deren Formel-Gewicht an Fuss/Hand
# >= 0,95 ist (Pfote unter dem Gelenk, Fussruecken vor dem Gelenk), bleiben auf der Formel (SPEZ_PFOTEN.md 2.2: die Pfote bewegt sich
# starr mit dem Fuss-/Handknochen); (2) vordere Krallen liegen um K1 verschoben (netz_<NAME>.npz 'k1_dy'): fuer die Zuordnung zu den
# alten Kopf-/Krallengewichten wird die Verschiebung zurueckgerechnet. Sonst wie baer-fell.
# Vorgaenger: Lauf baer-fell, Bauer Netz (08.11.2026): Hautgewichte des Baeren gegen die Dehnung optimieren (nur numpy, keine GPU, kein Blender).
# Ausgang: das Spielnetz mit den Gewichten der Formel aus baer_kampf_fell.py (npz mit NCB_FELL_NUR_GEWICHTE) und die Knochenmatrizen
# aller 15 Clips aus dem Dump des GLB (Importer des Spiels, Dump.java). Die Clips sind bit-gleich zum Bestand, also gelten dieselben
# Matrizen. Gesucht sind die Gewichte der freien Punkte (Rumpf ausser Pfoten unter z_pfote, Kopf und Kehle vor x_hals), die ueber
# jedes 'schritt'-te Bild aller Clips die groesste Hauptdehnung sigma1 je Dreieck klein halten (quadratisch + 'hoch' x vierte Potenz,
# grosse Dehnung also staerker bestraft), Stauchung sigma2 < 1 mit 'druck' bestrafen, glatt ueber die Kanten ('glatt') und nahe an der
# Formel ('nah'); kein freier Punkt unter den Boden ('boden'). Je Punkt nur Rumpfknochen (+ Kopf) und die Beinknochen der eigenen Seite. Nebenbedingungen: Gewichte >= 0,
# Summe 1, hoechstens 4 Einfluesse (die 4 staerksten bleiben, danach nachoptimiert). Verfahren: projizierter Gradientenabstieg mit
# Schrittweitensuche (die Energie faellt in jeder Runde), je Punkt vorkonditioniert ('vor').
# Aufruf: python baer_gewichte_fell.py GEWICHTE_FORMEL.npz GEGEND.npz AUS.npz [schluessel=wert,...]
#   GEGEND.npz: 'gegend' je Dreieck (0 Rumpf, 1 Kopf, 2 Kralle), Reihenfolge wie im FBX (netz_<NAME>.npz der Stufe netz)
#   AUS.npz -> baer_kampf_fell.py liest sie (NCB_FELL_GEWICHTE, Vorgabe _arbeit/baer_fell/netz/gewichte_fell.npz)
# Messung danach: _arbeit/baer_fell/netz/messen.py (alle Bilder, wie werkzeug/regionen.py). Statisch/offline gerechnet, nicht gespielt.
# Nachbesserung 09.11.2026 (fix_bericht.md): (1) keine 'fremden' Knochen mehr: Vorderbein-Knochen nur vor x 0 und nicht am Hinterbein,
#   Hinterbein-Knochen nur hinter x 0 und nicht am Vorderbein (Formel-Anteil des anderen Beins < 0,05), Hals/Kopf nicht am Bein und nicht
#   hinter x 0,10 (Pruefer Optik minor 2: Delle am Hinterknie aus Hand-Gewicht); Anteile der Formel bleiben erlaubt; (2) Falten
#   Achsel/Ellbogen: zusaetzliche
#   Strafe 'falte' x (falte_s - sigma2)^2 fuer Dreiecke der Region Achsel und um das Ellbogengelenk (r_ell, Tier-m) (Pruefer Technik M1);
#   (3) Kopf- und Krallenpunkte bekommen exakt die Gewichte von baer-anim (NCB_FELL_KOPF_ALT, npz der Formel am alten FBX, Zuordnung
#   ueber die Lage); (4) Quetsch-Strafe 'quetsch' x (quetsch_s - sigma2)^2 fuer alle Dreiecke (Liegen: sigma2 < 0,3 hoechstens 200).
import os
import pickle
import sys
import time

import numpy as np

T0 = time.time()
G = np.load(sys.argv[1])
gg = np.load(sys.argv[2])["gegend"]
AUS = sys.argv[3]
P = dict(schritt=5, runden=240, lr=0.05, glatt=0.3, nah=0.02, z_pfote=0.06, x_hals=0.80, druck=4.0, hoch=6.0, nachrunden=80,
         z_oben=9.0, vor=1, klein=0.01, boden=1e9, falte=25.0, falte_s=0.6, r_ell=0.16, fremd=1, quetsch=15.0, quetsch_s=0.35, z_boden=0.45,
         fix1=1, falte_b=25.0, z_fremd=0.15, z_fuss=0.06, fuss_min=0.95, swipe=0.0, liege=1.0, band_z0=0.18, band_z1=0.40, achsel_w=0.0, achsel_s=3.0)
KOPF_ALT = os.environ.get("NCB_FELL_KOPF_ALT", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_fell/netz/gew_bestand.npz")
if len(sys.argv) > 4:
    for kv in sys.argv[4].split(","):
        k, v = kv.split("=")
        P[k] = float(v)
V, T, W0 = G["V"], G["T"], G["W"].astype(np.float64)
VZ = G["V_erw"]          # JUNGES: Urbild (Erwachsener 2c) fuer Zonen, Schwellen, Regionen
NAM = [str(n) for n in G["namen"]]
KR = G["kralle"]
n = len(V)
# Nachbesserung 09.11.: Kopf- und Krallenpunkte (alt_von >= 0 aus der Netz-Stufe) mit den Gewichten von baer-anim (Formel am alten FBX)
ALT_VON = np.load(sys.argv[2])["alt_von"] if "alt_von" in np.load(sys.argv[2]).files else None
KOPF_FEST = np.zeros(n, dtype=bool)
if ALT_VON is not None and os.path.exists(KOPF_ALT):
    GA = np.load(KOPF_ALT)
    nam_a = [str(x) for x in GA["namen"]]
    KOPF_FEST = ALT_VON >= 0
    # Zuordnung ueber die Lage (alt_von zaehlt im FBX von baer-anim, gew_bestand.npz im FBX von NCBearTest: andere Reihenfolge);
    # Kopf und Krallen liegen exakt wie im alten Netz (kopfprobe), also naechster Punkt mit Abstand < 1e-6
    _B = GA["V"].astype(np.float64)
    ia = np.empty(int(KOPF_FEST.sum()), dtype=np.int64)
    _VK = V.astype(np.float64).copy()
    if "k1_dy" in np.load(sys.argv[2]).files:
        # K1 zurueck: die alten Krallen lagen um k1_dy weiter aussen (float32 im FBX -> Vergleich auf 1e-6 m)
        _VK[:, 1] -= np.load(sys.argv[2])["k1_dy"]
    if "k2c_dx" in np.load(sys.argv[2]).files:
        # 2c: Hinterkrallen lagen um k2c_dx (-0,070) weiter vorn
        _VK[:, 0] -= np.load(sys.argv[2])["k2c_dx"]
    for _j, _p in enumerate(_VK[KOPF_FEST]):
        _d = ((_B - _p) ** 2).sum(1)
        ia[_j] = int(np.argmin(_d))
        assert _d[ia[_j]] < 1e-12, ("Kopf-/Krallenpunkt ohne Zwilling im alten Netz", _j, _d[ia[_j]])
    assert len(np.unique(ia)) == len(ia)
    Wa = np.zeros((len(ia), len(NAM)))
    for k_, nm_ in enumerate(nam_a):
        assert nm_ in NAM or GA["W"][ia, k_].max() == 0, nm_
        if nm_ in NAM:
            Wa[:, NAM.index(nm_)] = GA["W"][ia, k_]
    W0[KOPF_FEST] = Wa
    print("OPT Kopf/Krallen: %d Punkte mit den Gewichten von baer-anim, davon Lage gleich (< 1e-6) %d" % (
        int(KOPF_FEST.sum()), int((np.abs(GA["V"][ia] - V[KOPF_FEST]).max(1) == 0).sum())), flush=True)
DUMP = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_fell/bestand/dump.txt"   # Dump des Bestands-GLB 4cfe4f29 (Clips bit-gleich)
# fix1 2c: neue Sitz-Clips (SitDown/Sit/StandUp aus baer_kampf_2c.py); die 12 anderen Clips sind bit-gleich zum Bestand
DUMP = os.environ.get("NCB_GEW_DUMP", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges/glb_koerper/v1.txt.pkl")   # JUNGES: Dump des Jungen
print("OPT Clips aus", DUMP, flush=True)
if DUMP.endswith(".pkl"):
    D = pickle.load(open(DUMP, "rb"))
elif os.path.exists(DUMP + ".pkl"):
    D = pickle.load(open(DUMP + ".pkl", "rb"))
else:
    sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/tier_werkzeug")
    from dumpread import lese
    _d = lese(DUMP)
    D = dict(names=_d["names"], off=_d["off"], clips={k: dict(T=c["T"], M=c["M"]) for k, c in _d["clips"].items()})
IX = {nm: i for i, nm in enumerate(D["names"])}
OFF = np.asarray(D["off"])


def log(*a):
    print("OPT %.1fs" % (time.time() - T0), *a, flush=True)


# ---- Kanten (aus den Dreiecken), Ruhelaengen im Modellraum
P0 = np.stack((V[:, 1], V[:, 2], -V[:, 0]), 1) * 0.544
H0 = np.c_[P0, np.ones(n)]
E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
E.sort(1)
E = np.unique(E, axis=0)
L0 = np.linalg.norm(P0[E[:, 0]] - P0[E[:, 1]], axis=1)
gegV = np.zeros(n, dtype=np.int32)
for k in range(3):
    np.maximum.at(gegV, T[:, k], gg)
x, y, z = VZ[:, 0], VZ[:, 1], VZ[:, 2]          # JUNGES: Schwellen am Urbild
# ---- freie Punkte und Kandidaten-Knochen
rumpf = (gegV == 0) & ~KR
frei = rumpf & (z > P["z_pfote"]) & (x < P["x_hals"]) & (z < P["z_oben"])
# Lauf baer-pfoten: Pfote (Formel-Gewicht Fuss/Hand >= 0,95) bleibt auf der Formel
_w_pf = sum(W0[:, NAM.index("Bip01_%s_%s" % (s_, k_))] for s_ in "LR" for k_ in ("Hand", "Foot"))
frei &= _w_pf < 0.95
print("OPT Pfote fest (Formel Fuss/Hand >= 0,95, ueber z_pfote): %d Punkte" % int((rumpf & (z > P["z_pfote"]) & (_w_pf >= 0.95)).sum()), flush=True)
links = y >= 0
torso = ["Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Tail"] + (["Bip01_Head"] if P["x_hals"] > 0.6 else [])
bein = {s: ["Bip01_%s_%s" % (s, k) for k in ("UpperArm", "Forearm", "Hand", "Thigh", "Calf", "Foot")] for s in "LR"}
KAND = {s: [NAM.index(b) for b in torso + bein[s]] for s in "LR"}
nk = len(KAND["L"])
fi = np.nonzero(frei)[0]
kidx = np.where(links[fi, None], np.array(KAND["L"])[None, :], np.array(KAND["R"])[None, :])   # nf x nk (Spalten in W)
nf = len(fi)
# Erlaubt je Punkt: Kopf nur vorn (x > 0,45), Schwanz nur hinten (x < -0,55), Vorderbein nur vor x -0,25, Hinterbein nur hinter
# x 0,15 (sonst schiebt der Abstieg winzige, sinnlose Anteile weit entfernter Knochen hinein)
NAM_K = [NAM[i] for i in KAND["L"]]
erlaubt = np.ones((nf, nk), dtype=bool)
xf = x[fi]
for k_, nm_ in enumerate(NAM_K):
    if nm_ == "Bip01_Head":
        erlaubt[:, k_] = xf > 0.45
    elif nm_ == "Bip01_Tail":
        erlaubt[:, k_] = xf < -0.55
    elif any(t in nm_ for t in ("UpperArm", "Forearm", "Hand")):
        erlaubt[:, k_] = xf > -0.25
    elif any(t in nm_ for t in ("Thigh", "Calf", "Foot")):
        erlaubt[:, k_] = xf < 0.15
# Nachbesserung 09.11.: Beinknochen nur am eigenen Bein, Hals/Kopf nicht an Beinen und Hinterteil (Anteile der Formel, je Seite)
if P["fremd"] > 0:
    def _w0(*teile):
        return sum(np.where(links[fi], W0[fi, NAM.index("Bip01_L_" + t)], W0[fi, NAM.index("Bip01_R_" + t)]) for t in teile)
    wv0 = _w0("UpperArm", "Forearm", "Hand")
    wh0 = _w0("Thigh", "Calf", "Foot")
    for k_, nm_ in enumerate(NAM_K):
        if any(t in nm_ for t in ("UpperArm", "Forearm", "Hand")):
            erlaubt[:, k_] &= (xf > 0.0) & (wh0 < 0.05)
        elif any(t in nm_ for t in ("Thigh", "Calf", "Foot")):
            erlaubt[:, k_] &= (xf < 0.0) & (wv0 < 0.05)
        elif nm_ in ("Bip01_Neck", "Bip01_Head"):
            erlaubt[:, k_] &= (xf > 0.10) & (wv0 < 0.5) & (wh0 < 0.05)
    log("Nachbesserung: verbotene Knochen-Eintraege (fremd) %d" % int((~erlaubt).sum()))
if P.get("fix1", 1) > 0:
    # fix1 (Pruefer Technik m3): Schwanz, Wirbelsaeule, Becken (und Hals/Kopf) an den Beinen unter Ruhe-z z_fremd nicht
    _unten = (z[fi] < P["z_fremd"]) & (np.abs(y[fi]) > 0.05)
    for k_, nm_ in enumerate(NAM_K):
        if nm_ in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail", "Bip01_Neck", "Bip01_Head"):
            erlaubt[:, k_] &= ~_unten
    log("FIX1 Rumpfknochen unter z %.2f an den Beinen verboten: %d freie Punkte" % (P["z_fremd"], int(_unten.sum())))
# Startwerte: Formel, auf die Kandidaten beschraenkt
w = np.take_along_axis(W0[fi], kidx, 1)
w = np.where(erlaubt, np.maximum(w, 0), 0.0)
leer = w.sum(1) <= 1e-9
w[leer] = np.take_along_axis(W0[fi], kidx, 1)[leer]
erlaubt |= w > 0
w /= np.maximum(w.sum(1, keepdims=True), 1e-9)
w_start = w.copy()
log("Punkte %d, frei %d, Kandidaten je Punkt %d, Kanten %d" % (n, nf, nk, len(E)))
# Kanten mit mindestens einem freien Punkt
fpos = np.full(n, -1)
fpos[fi] = np.arange(nf)
ke = (fpos[E[:, 0]] >= 0) | (fpos[E[:, 1]] >= 0)
E2, L02 = E[ke], L0[ke]
ok = L02 > 0.002
E2, L02 = E2[ok], L02[ok]
log("Kanten mit freiem Punkt %d" % len(E2))
# Dreiecke mit freiem Punkt; gueltig wie messen.py (Kante >= 7,4 mm, Hoehe >= 2 mm)
kt = (fpos[T] >= 0).any(1)
T2 = T[kt]
e1 = P0[T2[:, 1]] - P0[T2[:, 0]]
e2 = P0[T2[:, 2]] - P0[T2[:, 0]]
l01, l02_ = np.linalg.norm(e1, axis=1), np.linalg.norm(e2, axis=1)
l12 = np.linalg.norm(P0[T2[:, 2]] - P0[T2[:, 1]], axis=1)
gt = np.minimum(np.minimum(l01, l02_), l12) > 0.004
gt &= np.linalg.norm(np.cross(e1, e2), axis=1) / np.maximum(np.maximum(l01, l02_), l12) > 0.002 * 0.544
T2, e1, e2, l01 = T2[gt], e1[gt], e2[gt], l01[gt]
uu = e1 / l01[:, None]
nn_ = np.cross(e1, e2)
nn_ /= np.linalg.norm(nn_, axis=1, keepdims=True)
vv = np.cross(nn_, uu)
Rm = np.stack((np.stack(((e1 * uu).sum(1), (e2 * uu).sum(1)), 1), np.stack(((e1 * vv).sum(1), (e2 * vv).sum(1)), 1)), 1)
RI = np.linalg.inv(Rm).astype(np.float64)                      # F = [e1 e2] RI
nt = len(T2)
# Nachbesserung 09.11.: Falten-Zone je Dreieck (Region Achsel nach regionen_rt.py mit den Formel-Gewichten, Ellbogen = Mitte naeher
# als r_ell am Forearm-Gelenk, Tier-m wie netz/falten_fell.py)
import importlib.util
_sp = importlib.util.spec_from_file_location("regionen_rt", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges/werkzeug/regionen_rt.py")
_rm = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_rm)
_RT, _RN = _rm.regionen(VZ, T, gg, W0, NAM)          # JUNGES: Regionen am Urbild
idx_t2 = np.nonzero(kt)[0][gt]
_mitte = V[T2].mean(1)
_ell = np.zeros(nt, dtype=bool)
for _s in "LR":
    _p = np.linalg.inv(np.asarray(D["off"])[IX["Bip01_%s_Forearm" % _s]])[:3, 3]
    _ell |= np.linalg.norm(_mitte - np.array((-_p[2], _p[0], _p[1])) / 0.544, axis=1) < P["r_ell"]
ZONE = ((_RT[idx_t2] == _RN.index("Achsel")) | _ell).astype(np.float64)
log("Falten-Zone: Dreiecke %d (Achsel %d, Ellbogen %d), Strafe %.1f unter sigma2 %.2f" % (int(ZONE.sum()), int((_RT[idx_t2] == _RN.index("Achsel")).sum()), int(_ell.sum()), P["falte"], P["falte_s"]))
# fix1 2c (Pruefbericht B2, Achsel/Brust <= 3,5): Zusatzstrafe achsel_w x (sigma1 - achsel_s)^2 fuer Achsel und Brust, in allen Bildern
ZA = ((_RT[idx_t2] == _RN.index("Achsel")) | (_RT[idx_t2] == _RN.index("Brust"))).astype(np.float64)
log("Achsel/Brust-Strafe: Dreiecke %d, Gewicht %.1f ueber sigma1 %.2f" % (int(ZA.sum()), P["achsel_w"], P["achsel_s"]))
# Nachbesserung 1 (fix1, Pruefer Technik B1: Falten im Liegen 88 -> 186, Knie 14 -> 114): Zone auch um das Kniegelenk (Calf, r_ell) und im
# Uebergangsband der Beine (Ruhe-z 0,18-0,40, |y| > 0,05: duenner Unterschenkel/Unterarm gegen dicken Rumpf), Strafe dort 'falte_b'
if P.get("fix1", 1) > 0:
    _knie = np.zeros(nt, dtype=bool)
    for _s in "LR":
        _p = np.linalg.inv(np.asarray(D["off"])[IX["Bip01_%s_Calf" % _s]])[:3, 3]
        _knie |= np.linalg.norm(_mitte - np.array((-_p[2], _p[0], _p[1])) / 0.544, axis=1) < P["r_ell"]
    _band = (_mitte[:, 2] > P["band_z0"]) & (_mitte[:, 2] < P["band_z1"]) & (np.abs(_mitte[:, 1]) > 0.05)
    _neu = (_knie | _band) & (ZONE < 0.5)
    ZONE = np.maximum(ZONE, _neu * P["falte_b"] / max(P["falte"], 1e-9))
    log("FIX1 Falten-Zone erweitert: Knie %d, Band z 0,18-0,40 %d, neu %d Dreiecke (Strafe %.1f); Zone jetzt %d" % (
        int(_knie.sum()), int(_band.sum()), int(_neu.sum()), P["falte_b"], int((ZONE > 0).sum())))
log("Dreiecke mit freiem Punkt (gueltig) %d" % nt)
# ---- Bilder: jedes P['schritt']-te Bild aller Clips
bilder = []
FW = []      # fix1 2c: Gewicht der Falten-Strafe je Bild (liege)
for c, C in D["clips"].items():
    nfr = len(C["T"])
    fr = list(range(0, nfr, int(P["schritt"]))) + [nfr - 1]
    if P["swipe"] > 0 and c in ("NCBear_SwipeL", "NCBear_SwipeR"):
        fr = sorted(set(fr) | set(range(6, min(24, nfr))))
    for f in fr:
        bilder.append(C["M"][f])
        FW.append(P["liege"] if (c == "DeerStag_Dead" or (c == "DeerStag_Death" and f >= 0.75 * (nfr - 1))) else 1.0)
nb = len(bilder)
FW = np.asarray(FW, dtype=np.float64)
log("Bilder je Clip: swipe %d, Liegebilder %d mit Falten-Gewicht %.1f" % (int(P["swipe"]), int((FW != 1.0).sum()), P["liege"]))
S = np.stack([np.einsum("bij,bjk->bik", M, OFF) for M in bilder], 0)[:, :, :3, :]     # nb x 26 x 3 x 4
# feste Punkte: Haut einmal je Bild
fest_v = np.unique(np.concatenate((E2[(fpos[E2] < 0)], T[(fpos[T] >= 0).any(1)][fpos[T[(fpos[T] >= 0).any(1)]] < 0])))
Wf = W0[fest_v]
bi = np.array([IX[nm] for nm in NAM])
Pfest = np.einsum("fbij,nj,nb->fni", S[:, bi], H0[fest_v], Wf, optimize=True).astype(np.float32)   # nb x nfest x 3
# freie Punkte: Q[f, v, k] = S_bone(k)(f) * h_v
Q = np.empty((nb, nf, nk, 3), dtype=np.float32)
for s in "LR":
    m = links[fi] if s == "L" else ~links[fi]
    bones = bi[KAND[s]]
    Q[:, m] = np.einsum("fkij,nj->fnki", S[:, bones], H0[fi[m]], optimize=True)
log("Bilder %d, Q %.0f MB" % (nb, Q.nbytes / 1e6))
# Boden: freie Punkte, die in Ruhe unter z 0,25 liegen, in JEDEM Bild aller Clips pruefen (nur ihre Hoehe)
bod = np.nonzero(z[fi] < P["z_boden"])[0]   # Lauf baer-pfoten: 0,25 -> 0,45 (Kniekehle/Hinterteil sassen im Sitzen 0,2-0,3 cm im Boden)
S_alle = np.concatenate([np.einsum("fbij,bjk->fbik", C["M"], OFF)[:, :, 1, :] for C in D["clips"].values()], 0)   # Bilder x 26 x 4 (Zeile y)
QB = np.empty((len(S_alle), len(bod), nk), dtype=np.float32)
for s_ in "LR":
    m_ = links[fi[bod]] if s_ == "L" else ~links[fi[bod]]
    QB[:, m_] = np.einsum("fkj,nj->fnk", S_alle[:, bi[KAND[s_]]], H0[fi[bod][m_]], optimize=True)
log("Boden: %d Punkte in %d Bildern" % (len(bod), len(S_alle)))
# Kantenenden: (ist frei, Index)
ea_f, eb_f = fpos[E2[:, 0]], fpos[E2[:, 1]]
fest_pos = np.full(n, -1)
fest_pos[fest_v] = np.arange(len(fest_v))
ea_x, eb_x = fest_pos[E2[:, 0]], fest_pos[E2[:, 1]]
tx = [fest_pos[T2[:, k]] for k in range(3)]
tf = [fpos[T2[:, k]] for k in range(3)]
fest_v2 = np.unique(T2[fpos[T2] < 0])
# Glaette-Kanten zwischen freien Punkten (gleiche Seite) und zu festen Nachbarn
Eff = E[(fpos[E[:, 0]] >= 0) & (fpos[E[:, 1]] >= 0)]
Eff = Eff[links[Eff[:, 0]] == links[Eff[:, 1]]]
ga, gb = fpos[Eff[:, 0]], fpos[Eff[:, 1]]


def projiziere(w, maske=None):
    """Zeilenweise auf das Simplex (w >= 0, Summe 1); maske: erlaubte Eintraege."""
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
    Pf = np.einsum("fnki,nk->fni", Q, w.astype(np.float32), optimize=True)       # nb x nf x 3
    A0, A1, A2 = (ecken(Pf, tf[k], tx[k]) for k in range(3))
    Em = np.stack((A1 - A0, A2 - A0), 3).astype(np.float64)                                         # nb x nt x 3 x 2
    F = np.einsum("ftij,tjk->ftik", Em, RI, optimize=True)
    C = np.einsum("ftji,ftjk->ftik", F, F, optimize=True)                         # 2x2
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
    e_deh = float((s * s + P["hoch"] * s ** 4).sum() + P["druck"] * (c * c).sum() + P["falte"] * (hz * hz).sum() + P["achsel_w"] * (ha * ha).sum()
                  + P["quetsch"] * (hq * hq).sum())
    # Boden: kein freier Punkt unter z = 0 (Modell-y, Massstab 0,544)
    zb = np.einsum("fnk,nk->fn", QB, w[bod].astype(np.float32), optimize=True).astype(np.float64)
    zneg = np.minimum(zb, 0.0)
    e_deh += P["boden"] * float((zneg * zneg).sum())
    e_gl = P["glatt"] * ((w[ga] - w[gb]) ** 2).sum() * nb / 100.0
    e_nah = P["nah"] * ((w - w_start) ** 2).sum() * nb / 100.0
    if not grad:
        return e_deh + e_gl + e_nah, s1
    # Eigenvektoren von C (2x2): v1 zu lam1
    a_, b_ = C[..., 0, 1], lam1 - C[..., 0, 0]
    v1 = np.stack((a_, b_), -1)
    kl = np.linalg.norm(v1, axis=-1) < 1e-9
    v1[kl] = (1.0, 0.0)
    v1 /= np.linalg.norm(v1, axis=-1, keepdims=True)
    v2 = np.stack((-v1[..., 1], v1[..., 0]), -1)
    f1 = (2 * s + 4 * P["hoch"] * s ** 3 + 2 * P["achsel_w"] * ha) / np.maximum(s1, 1e-6)
    f2 = (-2 * P["druck"] * c - 2 * P["falte"] * hz - 2 * P["quetsch"] * hq) / np.maximum(s2, 1e-6)
    Fv1 = np.einsum("ftik,ftk->fti", F, v1)
    Fv2 = np.einsum("ftik,ftk->fti", F, v2)
    dF = (f1[..., None, None] * Fv1[..., :, None] * v1[..., None, :] + f2[..., None, None] * Fv2[..., :, None] * v2[..., None, :]).astype(np.float32)
    dE = np.einsum("ftik,tjk->ftij", dF, RI, optimize=True)                       # nb x nt x 3 x 2 (nach e1, e2)
    gk = (-(dE[..., 0] + dE[..., 1]), dE[..., 0], dE[..., 1])
    gP = np.zeros((nb, nf, 3), dtype=np.float64)
    fo = (np.arange(nb) * nf)[:, None]
    for k in range(3):
        m_ = tf[k] >= 0
        ik = (fo + tf[k][m_][None]).ravel()
        for c_ in range(3):
            gP[:, :, c_] += np.bincount(ik, weights=gk[k][:, m_, c_].ravel(), minlength=nb * nf).reshape(nb, nf)
    g = np.einsum("fni,fnki->nk", gP.astype(np.float32), Q, optimize=True).astype(np.float64)
    g[bod] += np.einsum("fn,fnk->nk", (2.0 * P["boden"] * zneg).astype(np.float32), QB, optimize=True)
    gw = np.zeros_like(w)
    dg = 2 * P["glatt"] * (w[ga] - w[gb]) * nb / 100.0
    np.add.at(gw, ga, dg)
    np.add.at(gw, gb, -dg)
    g += gw + 2 * P["nah"] * (w - w_start) * nb / 100.0
    return e_deh + e_gl + e_nah, s1, g


def abstieg(w, runden, maske=None):
    """Projizierter Gradientenabstieg mit Schrittweitensuche: die Energie faellt in jeder Runde."""
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


def adam(w, runden, maske=None, lr=None):
    lr = P["lr"] if lr is None else lr
    m1 = np.zeros_like(w)
    m2 = np.zeros_like(w)
    for it in range(int(runden)):
        e, r, g = energie(w)
        m1 = 0.9 * m1 + 0.1 * g
        m2 = 0.999 * m2 + 0.001 * g * g
        mh = m1 / (1 - 0.9 ** (it + 1))
        vh = m2 / (1 - 0.999 ** (it + 1))
        w = projiziere(w - lr * mh / (np.sqrt(vh) + 1e-12), maske)
        if it % 50 == 0 or it == runden - 1:
            log("Runde %4d Energie %.4g, Kante r max %.2f, 99,5%% %.3f, min %.2f" % (it, e, r.max(), np.percentile(r, 99.5), r.min()))
    return w


e0, r0 = energie(w, grad=False)
if P.get("pruef", 0) > 0:
    rng = np.random.default_rng(1)
    e_, r_, g_ = energie(w)
    for _ in range(6):
        i, k = rng.integers(nf), rng.integers(nk)
        h = 1e-4
        w2 = w.copy(); w2[i, k] += h
        e2, _ = energie(w2, grad=False)
        log("Gradientenprobe", i, k, "analytisch %.5g numerisch %.5g" % (g_[i, k], (e2 - e_) / h))
    raise SystemExit
log("Start: Energie %.4g, sigma1 max %.2f 99,5%% %.3f" % (e0, r0.max(), np.percentile(r0, 99.5)))
w = abstieg(w, P["runden"], erlaubt)
# hoechstens 4 Einfluesse je Punkt: die staerksten 4 behalten, dann nur diese nachoptimieren
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
W[(W < P["klein"]) & ~KOPF_FEST[:, None]] = 0
o = np.argsort(-W, 1)
keep = np.zeros_like(W, dtype=bool)
np.put_along_axis(keep, o[:, :4], True, 1)
W[~keep] = 0
_nf = ~KOPF_FEST
W[_nf] /= W[_nf].sum(1, keepdims=True)
if P.get("fix1", 1) > 0:
    # fix1 (Pruefer Technik m3/m6): auch an den festen Pfotenpunkten (Formel) unter z_fremd keine Rumpfknochen; unter z_fuss
    # Fuss/Hand >= fuss_min (der Rest anteilig kleiner). Kopf/Krallen bleiben bit-gleich (KOPF_FEST).
    _rk = [NAM.index(nm_) for nm_ in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail", "Bip01_Neck", "Bip01_Head")]
    _bein = (np.abs(y) > 0.05) & ~KOPF_FEST & ~KR
    _m = _bein & (z < P["z_fremd"]) & (W[:, _rk].sum(1) > 0)
    _vor = W[:, _rk].sum(1).copy()
    W[np.ix_(_m, _rk)] = 0.0
    W[_m] /= W[_m].sum(1, keepdims=True)
    log("FIX1 Rumpfknochen an Beinpunkten unter z %.2f entfernt: %d Punkte (Anteil vorher max %.3f)" % (P["z_fremd"], int(_m.sum()), _vor[_m].max() if _m.any() else 0.0))
    _fh = np.zeros(n)
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
    log("FIX1 Fuss/Hand unter z %.2f auf >= %.2f gesetzt: %d Punkte (vorher min %.3f)" % (P["z_fuss"], P["fuss_min"], int(_m2.sum()), _fh[_bein & (z < P["z_fuss"]) & (_fh > 0.5)].min()))
if KOPF_FEST.any():
    assert (W[KOPF_FEST] == W0[KOPF_FEST]).all()
    log("Kopf/Krallen-Gewichte = baer-anim: %d Punkte bit-gleich" % int(KOPF_FEST.sum()))
assert (W > 0).sum(1).max() <= 4
np.savez(AUS, V=V, V_erw=VZ, T=T, W=W, namen=G["namen"], kralle=KR, frei=frei)
log("fertig: Einfluesse max %d, Summe %.6f..%.6f, Abweichung von der Formel im Mittel %.3f" % (
    (W > 0).sum(1).max(), W.sum(1).min(), W.sum(1).max(), np.abs(W - W0)[fi].sum(1).mean() / 2))
