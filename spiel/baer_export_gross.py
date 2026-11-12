# Lauf baer-gross (11.11.2026), Bau Clips: Kopie von baer_export_2c.py (Original unveraendert, MD5 13b06a84). Kopie-Schritt: nur Pfade/Namen
# auf _arbeit/baer_gross bzw. *_gross.py umgestellt (NETZ-Vorgabe -> _arbeit/baer_gross/netz/, MOD_FELL -> _arbeit/baer_gross/mod/42/media/, QUELLE baer_quelle_gross.py). Statisch/offline, nicht gespielt.
# Lauf baer-gross, Bau Netz+Gewichte (11.11.2026, SPEZ_GROSS.md 3.5): nur zwei Formschritte in form_2c, Rest unveraendert:
#   N1 Buckel (G1): C2C_BUCKEL Kamm 0,013 -> 0,043 m, Flanken 0,045 -> 0,055 (Stand bau_n5, Fortsetzung), Kamm-Fenster wie 2c;
#   N2 Taille (R2): neuer Schritt (h) - Aussenflanke |y| ab 0,22, Ruhe x -0,28..+0,08 (voll -0,22..+0,02), z 0,45-0,95, halbe Breite bis
#      C2C_TAILLE (BAER_2C_TAILLE, 0 = aus). Kopf/Krallen/Pfoten bleiben fest wie 2c (C2C_KOPF_FEST, z < 0,115).
# Fortsetzung Bau Netz (11.11. abends): (h2) obere Flanke vor der Huefte (BAER_2C_FLANKE, Ziel 0,380 bei x -0,28; Rear "Bauch" ohne Taille)
#   und Buckel-Flanken laufen erst bei x 0,32-0,44 aus (BAER_2C_BUCKEL_AUS_FL; Kragen neben dem Kopf im Sitzen). Kamm/Nacken unveraendert.
# Lauf baer-2c (10.11.2026, Bau Koerper): Kopie von baer_export_pfote.py (Original unveraendert). Ausgaben nach _arbeit/baer_2c/.
# Aenderungen mit "2c" kommentiert (SPEZ_2C.md 2, 4): form_2c (Beine ohne Glocke, Rumpf schmaler, Nacken flacher), Hinterfuss/Sohle
# kurz und rund, Hinterkrallen -0,070 in x. Statisch gebaut, nicht gespielt.
# Lauf baer-pfoten (09.11.2026): Kopie von baer_export_fell.py (Original bleibt). Kevin: "das soll natuerlich nur eine richtige
# baerenpfote sein" (SPEZ_PFOTEN.md). Neu gegen baer-fell:
#   - Hochmodell baer_quelle_pfote.py: je Pfote EIN Feld (Bein + Fuss + Zehen), Teile 'pfote_*' statt 'zehen_*' in der Huelle.
#   - Huellendicke an Pfote und Unterschenkel aus dem SOLL des Spielnetzes (pfoten_abstand(.., 'soll')): die Huelle waechst nur bis zur
#     Soll-Flaeche (Zehen 0,4 cm, Fuss 0,7 cm, Gelenk 1 cm, z 0,20 2 cm ..., ab z 0,36 wie baer-fell 7,1 cm); in der Pfote nicht
#     nachgeglaettet (das Feld ist schon glatt), Taubin an der Pfote nur 10 %.
#   - Krallen vorn K1 (je Kralle starr in y zur Mittelkralle, Teilung 4,6 -> 4,1 cm), hinten bit-gleich; Kopf bit-gleich wie baer-fell.
#   - Sohlen: Ballenplan aus _arbeit/baer_pfote/spez/pfoten_plan.json (Sohlenplatte hinten / Handballen vorn als Vieleck, fuenf
#     Zehenballen), RASTER 20 mm, BALLEN_HUB 12 mm.
#   - Stufe 'ansichten' (Fell-Ansichten des neuen Hochmodells, aus baer_export.py:160), Ausgabe BAER_PFOTE_ANS; fuer den Rumpf ueber
#     z 0,40 kann die Huelle weiter aus den alten Ansichten kommen (BAER_PFOTE_ANS_ALT), damit sich dort nichts aendert.
#   - BAER_PFOTE_NUR_HUELLE=1: Stufe netz endet nach der Huelle (dichtes Netz als npz, fuer die Form-Runden).
# Ausgaben unter _arbeit/baer_pfote/ (netz/, mod/42/media/). Statisch gebaut und offline gemessen, nicht gespielt.
# Vorgaenger (baer-fell): Kopie von baer_export_anim.py fuer den Lauf baer-fell (Bauer Netz, 08.11.2026; Original bleibt). Neu gegen baer-anim:
#   - Sohlen mit Ballen: die flache Sohlenscheibe jeder Pfote wird durch eine Sohle mit Ballen ersetzt (sohlen_bauen): fuenf
#     Zehenballen im Bogen hinter den Krallen, ein querliegender Sohlenballen, vorn ein Handwurzelballen, hinten ein langer
#     Fersenballen. Ballen liegen bei z = 0 auf, die Furchen sind BALLEN_HUB nach oben eingezogen (Auflage wie bisher).
#   - Jede Sohle ist eine eigene UV-Insel mit SOHLE_DICHTE-facher Texeldichte; Lage der Ballen in Spielmetern und UV steht in
#     netz/sohle_layout.json (fuer den Textur-Bauer). Flaechen-Attribut 'sohle' (0 keine, 1 VL, 2 VR, 3 HL, 4 HR);
#     Regionen als Karte: _arbeit/baer_fell/netz/karten.py (nach den Gewichten).
#   - Form (FORM_*): Gesaessfalte hinten (gegen "von hinten ein Klumpen"), Schultern voller und Flanken unten schlanker
#     (gegen "Rumpf von vorn ein Ei"); nur am dichten Rumpf vor dem Verringern, Kopf und Krallen bleiben.
#   - Stufe 'fbx': Spielnetz ohne Textur als models_X/WorldItems/NCBear.fbx nach MOD_FELL (Eingang fuer baer_kampf_fell.py).
#   - Ausgaben unter _arbeit/baer_fell/netz/ (lowpoly_<NAME>.blend, netz_<NAME>.npz); NAME aus BAER_FELL_NAME (Vorgabe 'fell').
#     BAER_FELL_AUS=1 schaltet alles Neue ab (Gegenprobe: dann entsteht genau das Netz von baer-anim).
#   - Optional (Vorgabe aus) BAER_ZOTTELN: spitze Zotteln an Umrisslinien - probiert und verworfen (bau_netz.md 4).
#   - 'backen' ist unveraendert bis auf die Pfade (gehoert dem Textur-Bauer; hier nur fuer einen Zwischenstand mit den alten Ansichten).
# Lauf baer-anim (Vorgaenger):
# Kopie von baer_export.py fuer den Lauf baer-anim (Original bleibt): runderes Spielnetz, Kopf und Krallen unveraendert.
# Ursachen der Ecken und Hubbel (anim_modell.md): grobe Rumpfhaut (Voxel 5,2 cm), Fellhuelle in 1-cm-Stufen geschaelt und
# kaum geglaettet, Zotteln mit 3,6-6,6 cm Ausschlag, danach auf 11.100 Rumpfdreiecke verringert.
# Neu: Rumpfhaut 'baer_koerper_rund' (baer_quelle_anim.py), Schaelen in 2,5-mm-Stufen an weichgezeichneten Umrissen, Fell
# 1 cm voller, keine Zotteln, volumentreu geglaettet, Falten (Achsel, Leiste) aufgefuellt, mehr Rumpfdreiecke. Kopf und Krallen
# kommen Punkt fuer Punkt samt UV und Texeln aus dem alten Spielnetz; die Naht ist ein Streifen am alten Kopfrand.
# Eingang (nur lesen): die Ansichten des Hochmodells mit Fell aus baer_export.py 'ansichten' (ANS) und das alte Spielnetz
# (ALT_FBX, ALT_PNG = NCBearTest-Stand vom 08.11.). Die Ansichten werden hier NICHT neu gerendert.
# Aufruf: blender --background --factory-startup --python baer_export_fell.py -- STUFE [Rumpfdreiecke]
#   diagnose   die Fellhuelle Schritt fuer Schritt (alt/neu) als diagnose.blend, mit Hubbel-Mass
#   netz       neue Huelle (Form), Naht an den alten Kopf, verringern, Sohlen, Rumpf-UV -> NETZ/lowpoly_<NAME>.blend
#   fbx        NETZ/lowpoly_<NAME>.blend -> MOD_FELL/models_X/WorldItems/NCBear.fbx (ohne Textur)
#   backen     Ansichten auf den neuen Rumpf, Kopf/Krallen-Texel aus der alten Textur -> FBX + 2048er Textur nach MOD (Zwischenstand)
#   kopfprobe  altes und neues FBX (BAER_FELL_FBX, Vorgabe MOD_FELL): Kopf- und Krallenpunkte bit-gleich, UV gleich
# Statisch geprueft und offline gemessen, nicht gespielt.
import json
import math
import os
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

SPA = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_anim/modell/"      # Eingang baer-anim (nur lesen): alt/NCBear.fbx, alt/NCBear_2048.png
NETZ = os.environ.get("BAER_PFOTE_NETZ", os.environ.get("BAER_FELL_NETZ", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gross/netz/"))   # Arbeitsordner (Nachbesserung 09.11.: per Umgebung umlenkbar, sonst ueberschreibt ein Nachbau die gelieferten Dateien)
SP = NETZ
HIER = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/"
NAME = os.environ.get("BAER_FELL_NAME", "2c")
FELL = os.environ.get("BAER_FELL_AUS", "") != "1"
MOD = os.environ.get("BAER_FELL_MOD", NETZ + "zwischen_" + NAME + "/42/media/")   # backen (Zwischenstand) schreibt hierher
MOD_FELL = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gross/mod/42/media/"
QUELLE = HIER + "baer_quelle_gross.py"
MARKE = "# ------------------------------------------------------------------ Boden und Licht wie ein Tag im Spiel"
ANS = os.environ.get("BAER_PFOTE_ANS", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/ansichten/")
ANS_ALT = os.environ.get("BAER_PFOTE_ANS_ALT", "")   # alte Ansichten fuer den Rumpf (z > 0,40), leer = alles aus ANS
PLAN = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/spez/pfoten_plan.json"
NUR_HUELLE = os.environ.get("BAER_PFOTE_NUR_HUELLE", "") == "1"
PF_UEB = tuple(float(t) for t in os.environ.get("BAER_PFOTE_UEB", "0.28,0.35").split(","))   # Uebergang Pfoten-/Rumpfhuelle (Spiel-z)
PF_BAND = tuple(float(t) for t in os.environ.get("BAER_PFOTE_BAND", "0.24,0.28,0.33,0.37").split(","))   # Knie-Band: dort nachglaetten
PF_BAND_RUNDEN = int(os.environ.get("BAER_PFOTE_BAND_RUNDEN", "30"))
PF_HINTEN_HEUTE = ([0.24, 0.26, 0.30, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50],
                   [-0.612, -0.612, -0.610, -0.607, -0.605, -0.603, -0.603, -0.605, -0.611, -0.621, -0.640, -0.660])   # Hinterkante heute (Spiel)
PF_RAND_RING_RUNDEN = int(os.environ.get("BAER_PFOTE_RAND_RING", "0"))
PF_RAND_RUNDEN = int(os.environ.get("BAER_PFOTE_RAND", "0"))   # Sohlenrand-Schleife glaetten (0 = aus)
PF_Z_DEZ = 0.12            # Spiel-z: darunter zaehlt ein Punkt beim Verringern zur Pfote
PF_ZIEL = int(os.environ.get("BAER_PFOTE_ZIEL", "3950"))   # 2c: 4300 -> 3950 (kuerzere Hinterfuesse, SPEZ_2C 7.1)
_PF_ZIEL_ALT = 4300              # Dreiecke aller vier Pfoten unter PF_Z_DEZ (vor den Sohlen)
PF_RUMPF_REST = int(os.environ.get("BAER_PFOTE_RUMPF", "10520"))      # Dreiecke des Rumpfs ohne Pfoten und Kopf; fix1 2c: 10600 -> 10520 (breitere Hintersohlen +90, Ziel <= 19.850)
PF_VOXEL = tuple(float(t) for t in os.environ.get("BAER_PFOTE_VOXEL", "0.0085,0.0095").split(","))   # Voxel der zwei Remesh-Stufen (Hochmodell-m)
# Nachbesserung 1 (fix1, 09.11.2026 abends; _arbeit/baer_pfote/fix1_bericht.md): am dichten Netz nach form_fell (Spielmeter)
#   (a) Kegel statt Kragen: je Bein zwischen FIX1_KEGEL (Spiel-z) radial von der neuen Wade/dem Unterarm (z_lo) glatt
#       (smoothstep, keine Stufe, kein Ueberhang) bis zum baer-fell-Querschnitt (z_hi) - Pruefer Optik M1 "Pluderhose";
#   (b) Rumpf ab FIX1_KLEMM auf die baer-fell-Flaeche (fix1/alt_huelle.npz aus dem NCBearTest-GLB 2a4837f6) - Pruefer Technik M2;
#   (c) Fersen-Hinterkante (Ruhe-z 5-19 cm) FIX1_FERSE_DX nach hinten bis zur baer-fell-Linie - Pruefer Technik M1 (Sitzen schwebt);
#   (d) Ferse unten breiter (Sohle oval statt Schild) - Pruefer Optik M2. BAER_PFOTE_FIX1=0 schaltet alles ab.
FIX1 = os.environ.get("BAER_PFOTE_FIX1", "1") == "1"
FIX1_ALT = os.environ.get("BAER_PFOTE_FIX1_ALT", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/fix1/alt_huelle.npz")
FIX1_KEGEL = tuple(float(t) for t in os.environ.get("BAER_PFOTE_KEGEL", "0.18,0.342").split(","))
FIX1_KLEMM = tuple(float(t) for t in os.environ.get("BAER_PFOTE_KLEMM", "0.325,0.34").split(","))
# 2c: (c)/(d) aus - die neue kurze Ferse (baer_quelle_2c.py PF_TEILE H) wuerde sonst auf die alte baer-fell-Linie (x -0,63) gezogen
FIX1_FERSE_DX = float(os.environ.get("BAER_PFOTE_FERSE_DX", "0.0"))
FIX1_FERSE_BREIT = float(os.environ.get("BAER_PFOTE_FERSE_BREIT", "0.0"))
FIX1_ENTWIRR = int(os.environ.get("BAER_PFOTE_ENTWIRR", "8"))


def _fix1_niere(cx, cy, ax, ay, bieg, n=32):
    t = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    s_ = np.sin(t)
    return [[round(float(cx + ax * math.cos(a) + bieg * (1.0 - b * b)), 5), round(float(cy + ay * b), 5)] for a, b in zip(t, s_)]


# fix1: Ballenplan (ersetzt die Eintraege aus spez/pfoten_plan.json; Pruefer Optik M2/minor 1, Technik M3). Hinten: Sohlenplatte oval,
# vorn naeher an die (kuerzeren) Zehen, die Ferse rund geschlossen; das Ende hinter x -0,56 gilt fuer die Textur in 'abgerollten'
# Koordinaten (x - z, baer_textur_pfote.py ballen_q3), so laeuft das Leder rund um die Fersenkante bis ~3,5 cm hoch. Zehenballen
# groesser und naeher an der Platte. Vorn: Handballen als querliegende Niere (Ellipse, Vorderkante gewoelbt) statt Vieleck mit Ecken;
# Handwurzelballen wie im Hochmodell (baer_quelle_pfote.py PF_TEILE V ballen).
FIX1_PLAN = {
    "H": dict(platte_xy=[[-0.293, 0.163], [-0.279, 0.192], [-0.261, 0.226], [-0.258, 0.245], [-0.266, 0.268], [-0.281, 0.298],
                         [-0.295, 0.326], [-0.33, 0.331], [-0.37, 0.329], [-0.42, 0.318], [-0.48, 0.304], [-0.53, 0.292], [-0.57, 0.284],
                         [-0.605, 0.278], [-0.635, 0.272], [-0.655, 0.262], [-0.667, 0.243], [-0.655, 0.224], [-0.635, 0.214],
                         [-0.605, 0.208], [-0.57, 0.202], [-0.53, 0.194], [-0.48, 0.181], [-0.42, 0.168], [-0.37, 0.159], [-0.33, 0.158]],
              zehenballen_x_y_skala=[[-0.266, 0.166, 0.90], [-0.239, 0.204, 1.0], [-0.229, 0.240, 1.0], [-0.238, 0.277, 1.0],
                                     [-0.265, 0.315, 0.97]],
              zehenballen_r_cm=[1.80, 2.15]),
    "V": dict(handballen_xy=_fix1_niere(0.384, 0.213, 0.050, 0.086, 0.010),
              zehenballen_r_cm=[2.0, 2.4],
              handwurzelballen_x_y_r=[0.262, 0.238, 0.033], handwurzelballen_z_unten_cm=[1.5, 1.7]),
}
ALT_FBX = SPA + "alt/NCBear.fbx"
ALT_PNG = SPA + "alt/NCBear_2048.png"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["netz"]
STUFE = ARGS[0]
# Abbildung Hochmodell -> Spielmeter genau wie im alten Spielnetz (lowpoly.blend nachgerechnet: x0 = Flaechenschwerpunkt,
# zmin = tiefster Punkt; FBX dagegen 5,5e-8): sonst saesse der Rumpf gegen Kopf und Knochen verschoben
X0_ALT, ZMIN_ALT = -0.081113065901304876, 0.001335123204626143
# Stellschrauben des runden Netzes
NORMAL_RUNDEN = 24      # Schaelrichtung glaetten (alt 8)
FELL_PLUS = 0.010       # Fellgrenze im Rumpf weiter (m Hochmodell), an den Beinen die Haelfte
ALPHA_SIGMA = 1.5       # Umrisse der Ansichten weichzeichnen (Pixel der 1024er Maske, rund 5 mm)
SCHAEL_STUFEN = 65      # 2,5-mm-Stufen bis 16 cm (alt 16 Stufen = 1 cm)
D_RUNDEN = 30           # Felldicke ueber die Haut glaetten (alt 4)
TAUBIN_RUNDEN = 25      # volumentreu glaetten (Rumpf; Gesicht 0, Zehen 25 %)
FALTEN_RUNDEN = 30      # nach innen gewoelbte Stellen nach aussen heben
NAHT_BAND = 0.08        # so weit (m) wird der Rumpf am Kopfrand auf die alte Flaeche gezogen
NAHT_LUECKE = 0.012     # Rumpfdreiecke naeher an der Kopfnaht fallen weg, der Streifen schliesst
NAHT_GLATT = 0.10       # Band um die Kopfnaht, in dem der Rumpf an den festen Kopfrand geglaettet wird
NAHT_RUNDEN = 30
KOPF_NAHT = 0.06        # so weit (m Hochmodell, 4,5 cm Spielmass) in den Kopf hinein darf der Rand mitgeglaettet werden
SCHWANZ_RUNDEN = 25     # Stummelschwanz abstumpfen
RUMPF_ZIEL = 14500      # Dreiecke im Rumpf (alt 11.101); Kopf 2.295 und Krallen 832 bleiben
# Gaumen, Zunge, Zahn in baer_kampf.py (FLECK_*, Bildpixel der 1024er Textur von oben): keine Rumpf-Insel darf hinein
# Lauf baer-2c Bau Gebiss: die Flecken stehen jetzt in baer_maul_2c.py (FLECKEN, SPEZ_2C.md 3.4, gegen die UV-Karte von Bau Koerper
# geprueft: frei mit 3 px Saum, keine Insel wandert). Geprueft wird mit SPERR_FLECKEN (:3006 und baer_textur_2c.py:1497); das Packen
# der Rumpf-Inseln sperrt weiter die alten Rechtecke (SPERR_PACKEN), damit die Stufe netz dasselbe UV wie Bau Koerper liefert.
SPERR_FLECKEN = ((276, 4, 92, 102), (372, 4, 82, 102), (458, 4, 45, 102))
SPERR_PACKEN = ((280, 16, 80, 80), (376, 16, 80, 80), (472, 16, 24, 24))
# fix1 2c: die alten Sperrflaechen (+8 px Rand) deckten die neuen Flecken nicht ganz (Zahn-Fleck bis y 106): mit dem breiteren Hinterfuss
# legte der Packer eine Insel in den Zahn-Fleck (2048: x 984-1005, y 191-211, 335 Texel; Abbruch baer_textur_2c.py:1803). Jetzt decken die
# Sperrflaechen samt Rand genau SPERR_FLECKEN.
SPERR_PACKEN = tuple((x0 + 8, y0 + 8, w_ - 16, h_ - 16) for x0, y0, w_, h_ in SPERR_FLECKEN)
# Packversuche fuer die Rumpf-Inseln um die festen Kopf-/Krallen-Inseln: (Rand, Form, Drehung)
WACHSEN = (1.03, 1.06, 1.09, 1.12, 1.15)   # danach je Insel so viel groesser versuchen
PACK_VERSUCHE = ((0.0032, "CONCAVE", "ANY", "CLOSEST_UDIM"), (0.0024, "CONCAVE", "ANY", "CLOSEST_UDIM"),
                 (0.0032, "CONCAVE", "ANY", "ORIGINAL_AABB"), (0.0030, "CONCAVE", "ANY", "ORIGINAL_AABB"), (0.0028, "CONCAVE", "ANY", "ORIGINAL_AABB"),
                 (0.0026, "CONCAVE", "ANY", "ORIGINAL_AABB"), (0.0024, "CONCAVE", "ANY", "ORIGINAL_AABB"), (0.0022, "CONCAVE", "ANY", "ORIGINAL_AABB"),
                 (0.0020, "CONCAVE", "ANY", "ORIGINAL_AABB"))
# Lauf baer-fell (alle Masse Spielmeter)
SOHLE_DICHTE = 2.0      # Texeldichte der Sohlen-Inseln gegen den Rumpf (Rumpf 1,0, Pfote 1,35)
FORM_FALTE = float(os.environ.get("BAER_FORM_FALTE", "0.040"))       # Gesaessfalte hinten: Tiefe an der Mittellinie (Nachbesserung 09.11.: 0,026 -> 0,040)
FORM_SCHULTER = float(os.environ.get("BAER_FORM_SCHULTER", "0.040"))  # Schultern seitlich voller (Nachbesserung 09.11.: 0,024 -> 0,040, "Ei" im Aufrichten)
FORM_FLANKE = float(os.environ.get("BAER_FORM_FLANKE", "0.032"))     # Flanken/Huefte unten schlanker (Nachbesserung 09.11.: 0,017 -> 0,032)
ZOTTEL_AMP = float(os.environ.get("BAER_ZOTTELN", "0.0"))   # spitze Zotteln an den Umrisslinien: Ausschlag (m), 0 = aus
ZOTTEL_ABSTAND = 0.042  # Abstand der Spitzen (m)      # Flanken und Huefte unten seitlich schlanker
T0 = time.time()


def log(*a):
    print("EXPORT %.1fs" % (time.time() - T0), *a, flush=True)


def quelle(modus):
    """Fuehrt das Hochmodell-Skript bis vor Boden und Licht aus: Ruhehaltung, alle Teile, kein Gang."""
    src = open(QUELLE, encoding="utf-8").read()
    assert src.count(MARKE) == 1
    alt = sys.argv
    sys.argv = [alt[0], "--", modus]
    Q = {"__name__": "baer_quelle", "__file__": QUELLE}
    exec(compile(src.split(MARKE)[0], QUELLE, "exec"), Q)
    sys.argv = alt
    return Q


# ------------------------------------------------------------------ Bild lesen
def lade_exr(pfad):
    img = bpy.data.images.load(pfad)
    img.colorspace_settings.name = "Non-Color"
    w, h = img.size
    a = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    bpy.data.images.remove(img)
    return a.reshape(h, w, 4)


class Ansicht:
    """Rechnet Weltpunkte in Pixel einer gerenderten Ansicht. Zeile 0 ist unten, wie in Blender."""

    def __init__(self, v):
        self.v = v
        self.name = v["name"]
        self.res = v["res"]
        self.ortho = v["ortho"]
        c = np.array(v["c"])
        d = np.array(v["d"])
        self.c, self.d = c, d
        co = Vector(v["c"]) + Vector(v["d"]) * 12.0
        q = (-Vector(v["d"])).to_track_quat("-Z", "Y")
        M = q.to_matrix()
        self.x = np.array(M.col[0])
        self.y = np.array(M.col[1])
        self.z = np.array(M.col[2])
        self.co = np.array(co)
        self.s = self.res / self.ortho

    def pix(self, P):
        R = P - self.co
        u = (R @ self.x) * self.s + self.res * 0.5
        v = (R @ self.y) * self.s + self.res * 0.5
        tiefe = -(R @ self.z)
        return u, v, tiefe


def bilinear(img, u, v):
    """Bilinear in Pixelzentren; ausserhalb -> klemmt, Rueckgabe zusaetzlich Maske."""
    h, w = img.shape[:2]
    x = u - 0.5
    y = v - 0.5
    inn = (x >= 0) & (y >= 0) & (x < w - 1) & (y < h - 1)
    x0 = np.clip(np.floor(x).astype(np.int64), 0, w - 2)
    y0 = np.clip(np.floor(y).astype(np.int64), 0, h - 2)
    fx = np.clip(x - x0, 0.0, 1.0)
    fy = np.clip(y - y0, 0.0, 1.0)
    if img.ndim == 3:
        fx = fx[:, None]
        fy = fy[:, None]
    a = img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx
    b = img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy, inn


# ------------------------------------------------------------------ Hilfen am Netz (numpy)
def netz_arrays(me):
    n = len(me.vertices)
    V = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", V)
    V = V.reshape(n, 3)
    me.calc_loop_triangles()
    m = len(me.loop_triangles)
    T = np.empty(m * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("vertices", T)
    return V, T.reshape(m, 3)


def v_normalen(V, T):
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    N = np.zeros_like(V)
    for i in range(3):
        for ax in range(3):
            N[:, ax] += np.bincount(T[:, i], weights=n[:, ax], minlength=len(V))
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)


def kanten(T):
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    E.sort(axis=1)
    return np.unique(E, axis=0)


def glatt_feld(F, E, n_v, runden, faktor=0.5):
    """Mittelung ueber die Kanten fuer ein Skalar- oder Vektorfeld."""
    F = F.copy()
    for _ in range(runden):
        cnt = np.bincount(E[:, 0], minlength=n_v) + np.bincount(E[:, 1], minlength=n_v)
        if F.ndim == 1:
            S = np.bincount(E[:, 0], weights=F[E[:, 1]], minlength=n_v) + np.bincount(E[:, 1], weights=F[E[:, 0]], minlength=n_v)
            F = F + (S / np.maximum(cnt, 1) - F) * faktor
        else:
            for ax in range(F.shape[1]):
                S = np.bincount(E[:, 0], weights=F[E[:, 1], ax], minlength=n_v) + np.bincount(E[:, 1], weights=F[E[:, 0], ax], minlength=n_v)
                F[:, ax] += (S / np.maximum(cnt, 1) - F[:, ax]) * faktor
    return F


# ------------------------------------------------------------------ Stufe netz: Fellhuelle
def neues_netz(name, V, F):
    me = bpy.data.meshes.new(name)
    me.from_pydata(np.asarray(V, dtype=float).tolist(), [], np.asarray(F).tolist() if hasattr(F, "tolist") else F)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def welt_netz(ob):
    me = ob.data
    n = len(me.vertices)
    V = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", V)
    V = V.reshape(n, 3)
    M = np.array(ob.matrix_world)
    V = V @ M[:3, :3].T + M[:3, 3]
    F = [tuple(p.vertices) for p in me.polygons]
    return V, F


def alpha_laden(views, schritt=2, ordner=None):
    A = []
    for v in views:
        rgba = lade_exr((ordner or ANS) + v["name"] + ".exr")
        a = rgba[..., 3]
        h = a.shape[0] // schritt * schritt
        a = a[:h, :h].reshape(h // schritt, schritt, h // schritt, schritt).mean(axis=(1, 3))
        A.append(a.astype(np.float32))
    return A


def huelle_schaelen(V, N, dlim, views, alpha, schritt=2, dmax=0.15, stufen=16, schwelle=0.5):
    """Geht von der Haut nach aussen, solange der Punkt in JEDER Ansicht im Fell liegt und unter der Grenze bleibt."""
    D = np.linspace(0.0, dmax, stufen)
    d = np.zeros(len(V))
    lebt = np.ones(len(V), dtype=bool)
    objs = [Ansicht(v) for v in views]
    for k in range(1, stufen):
        idx = np.nonzero(lebt)[0]
        if not len(idx):
            break
        P = V[idx] + N[idx] * D[k]
        ok = D[k] <= dlim[idx]
        for av, a in zip(objs, alpha):
            u, v, _ = av.pix(P)
            r = a.shape[0]
            iu = np.floor(u / schritt).astype(np.int64)
            iv = np.floor(v / schritt).astype(np.int64)
            inn = (iu >= 0) & (iv >= 0) & (iu < r) & (iv < r)
            drin = np.zeros(len(idx), dtype=bool)
            drin[inn] = a[iv[inn], iu[inn]] >= schwelle
            if av.name.startswith("h_"):
                # Kopfansichten sehen nur den Kopf: ausserhalb des Bildes sagen sie nichts
                ok &= drin | ~inn
            else:
                ok &= drin
        lebt[idx] = ok
        d[idx[ok]] = D[k]
    return d


def _zotteln(s, q, y, ph0):
    r = np.zeros(len(s))
    for fs, fq, fy, ph, gew in ((6.3, 25.0, 21.0, 0.3, 1.0), (10.7, 39.0, 33.0, 2.1, 0.72), (3.9, 14.5, 13.0, 4.4, 0.85)):
        wn = np.sin(q * fq + 1.9 * np.sin(s * fs * 0.6 + ph + ph0)) * np.sin(y * fy + 1.5 * np.sin(s * fs * 0.8 + ph * 2.0) + ph + ph0)
        r = np.maximum(r, np.maximum(wn, 0.0) ** 1.4 * gew)
    return np.clip(r, 0.0, 1.0)


def buschel_rauschen(P, bein):
    """Spitze, in Strichrichtung gestreckte Zotteln, 0..1. Rumpf: nach hinten und unten. Bein: nach unten, sonst entstehen Ringe."""
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    rumpf = _zotteln(x * 0.86 + z * 0.51, -x * 0.51 + z * 0.86, y, 0.0)
    r_bein = _zotteln(z * 0.55, x * 0.8, y * 0.8, 1.3)
    return rumpf * (1.0 - bein) + r_bein * bein


# ------------------------------------------------------------------ Stufe backen: Ansichten auf die Abwicklung
HELL = float(os.environ.get("BAER_HELL", "1.95"))    # Das Spiel rechnet Textur x (0.4 Umgebung + Licht), also duenkler als gebacken
GAMMA = float(os.environ.get("BAER_GAMMA", "0.92"))
TEX = 2048
GROESSE = 0.75   # Hochmodell -> Meter (fest wie das alte Spielnetz)


def raster_uv(UVt, T, Vt, Nt, res):
    pos = np.zeros((res, res, 3), dtype=np.float32)
    nrm = np.zeros((res, res, 3), dtype=np.float32)
    tri = np.full((res, res), -1, dtype=np.int32)
    UVp = UVt * res
    for i in range(len(T)):
        a, b, c = UVp[i]
        den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(den) < 1e-9:
            continue
        x0 = max(int(math.floor(min(a[0], b[0], c[0]) - 1.0)), 0)
        x1 = min(int(math.ceil(max(a[0], b[0], c[0]) + 1.0)), res - 1)
        y0 = max(int(math.floor(min(a[1], b[1], c[1]) - 1.0)), 0)
        y1 = min(int(math.ceil(max(a[1], b[1], c[1]) + 1.0)), res - 1)
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        w0 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / den
        w1 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / den
        w2 = 1.0 - w0 - w1
        ad = abs(den)
        t0 = -0.75 * math.hypot(*(c - b)) / ad
        t1 = -0.75 * math.hypot(*(a - c)) / ad
        t2 = -0.75 * math.hypot(*(b - a)) / ad
        rand = (w0 >= t0) & (w1 >= t1) & (w2 >= t2)
        if not rand.any():
            continue
        drin = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        sub = tri[y0:y1 + 1, x0:x1 + 1]
        nimm = drin | (rand & (sub < 0))
        g0 = np.clip(w0, 0, 1)
        g1 = np.clip(w1, 0, 1)
        g2 = np.clip(w2, 0, 1)
        s = g0 + g1 + g2
        g0, g1, g2 = g0 / s, g1 / s, g2 / s
        tv = T[i]
        for ax in range(3):
            pos[y0:y1 + 1, x0:x1 + 1, ax][nimm] = (g0 * Vt[tv[0], ax] + g1 * Vt[tv[1], ax] + g2 * Vt[tv[2], ax])[nimm]
            nrm[y0:y1 + 1, x0:x1 + 1, ax][nimm] = (g0 * Nt[tv[0], ax] + g1 * Nt[tv[1], ax] + g2 * Nt[tv[2], ax])[nimm]
        sub[nimm] = i
    return pos, nrm, tri


def zbuffer(av, V, T, res):
    u, v, d = av.pix(V)
    k = res / av.res
    u = u * k
    v = v * k
    Z = np.full((res, res), np.inf, dtype=np.float32)
    # Rueckseiten weglassen: im geschlossenen Netz ist immer eine Vorderseite naeher
    du1, dv1 = u[T[:, 1]] - u[T[:, 0]], v[T[:, 1]] - v[T[:, 0]]
    du2, dv2 = u[T[:, 2]] - u[T[:, 0]], v[T[:, 2]] - v[T[:, 0]]
    vorn = (du1 * dv2 - dv1 * du2) > 0
    for t in T[vorn]:
        ax, bx, cx = u[t[0]], u[t[1]], u[t[2]]
        ay, by, cy = v[t[0]], v[t[1]], v[t[2]]
        x0 = max(int(math.floor(min(ax, bx, cx))), 0)
        x1 = min(int(math.ceil(max(ax, bx, cx))), res - 1)
        y0 = max(int(math.floor(min(ay, by, cy))), 0)
        y1 = min(int(math.ceil(max(ay, by, cy))), res - 1)
        if x1 < x0 or y1 < y0:
            continue
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        w0 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        w1 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
        w2 = 1.0 - w0 - w1
        ins = (w0 >= -0.02) & (w1 >= -0.02) & (w2 >= -0.02)
        if not ins.any():
            continue
        dd = w0 * d[t[0]] + w1 * d[t[1]] + w2 * d[t[2]]
        sub = Z[y0:y1 + 1, x0:x1 + 1]
        sub[ins] = np.minimum(sub[ins], dd[ins])
    return Z


def minfilter(Z):
    out = Z.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            out = np.minimum(out, np.roll(np.roll(Z, dy, 0), dx, 1))
    return out


def srgb(x):
    x = np.clip(x, 0.0, None)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1.0 / 2.4) - 0.055)


def fuellen(col, frei, maske, runden):
    """Fuellt freie Texel von gefuellten Nachbarn, nur innerhalb der Maske."""
    H, W = frei.shape
    for it in range(runden):
        fy, fx = np.nonzero(frei & maske)
        if not len(fy):
            return it
        summe = np.zeros((len(fy), 3), dtype=np.float32)
        cnt = np.zeros(len(fy), dtype=np.float32)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            ny, nx = fy + dy, fx + dx
            ok = (ny >= 0) & (nx >= 0) & (ny < H) & (nx < W)
            idx = np.nonzero(ok)[0]
            ist = ~frei[ny[idx], nx[idx]]
            idx = idx[ist]
            summe[idx] += col[ny[idx], nx[idx]]
            cnt[idx] += 1
        neu = cnt > 0
        col[fy[neu], fx[neu]] = summe[neu] / cnt[neu][:, None]
        frei[fy[neu], fx[neu]] = False
        if not neu.any():
            return it
    return runden


def gesicht_nacharbeit(Q, S, P, kralle):
    """Macht Auge, Nase und Mundlinie im Bild lesbar und gleicht die Gegenden an. S ist sRGB je Texel in der Maske."""
    sst = Q["sst"]
    L = Q["w2l"](P)
    a, b, c = L[:, 0], L[:, 1], L[:, 2]
    B = np.abs(b)
    hb = Q["huelle_basis"](a, b, c)
    kopf = hb < 0.03
    # Gegenden: Kopf etwas dunkler, sonst Maske auf dunklem Koerper; Schnauze noch etwas; Unterbeine heller, sonst schwarz im Spiel
    kopfm = 1.0 - sst(0.0, 0.14, hb)
    R = Q["regionen"](a, b, c)
    S = S * (1.0 - 0.10 * kopfm[:, None])
    S = S * (1.0 - 0.13 * (R["schf"] * kopfm)[:, None])
    S = S * (1.0 + 0.30 * ((1.0 - sst(0.08, 0.50, P[:, 2])) * (1.0 - kopfm))[:, None])
    S = S * (1.0 + 0.42 * ((1.0 - sst(0.04, 0.30, P[:, 2])) * (1.0 - kopfm))[:, None])
    # Fell hinter den Ohren war dunkler als Kopf und Hals: ein Ring wie eine Kapuze
    ring = sst(0.15, -0.05, a) * (1.0 - sst(0.015, 0.11, hb))
    S = S * (1.0 + (0.20 * ring)[:, None] * np.array((1.12, 1.0, 0.82)))
    # Ohr innen dunkel: sonst eine helle Scheibe
    S = S * (1.0 - 0.45 * (R["innen"] * kopfm)[:, None])
    # Unterkiefer: von vorn sonst eine helle Schmollippe
    S = S * (1.0 - 0.24 * (R["unter"] * kopfm)[:, None])
    # Pfoten: Zehen und Ballen dunkel, sonst wirken sie nackt und rosa
    ze = Q["zehen_abstand"](P)
    pf = (1.0 - sst(0.005, 0.040, ze)) * (1.0 - kralle)
    lum = S @ np.array((0.3, 0.55, 0.15))
    dunkel = (lum * 0.62)[:, None] * np.array((1.0, 0.78, 0.60))
    S = S * (1.0 - pf[:, None]) + dunkel * pf[:, None]
    # Krallen: Horn, kein Blau aus dem Himmel
    lum = S @ np.array((0.3, 0.55, 0.15))
    horn = (lum * 0.86)[:, None] * np.array((1.0, 0.87, 0.70))
    S = S * (1.0 - kralle[:, None]) + horn * kralle[:, None]
    # Nase: tiefes Anthrazit statt Spiegelung des hellen Himmels
    fn = Q["feld_nase"](a, b, c)
    nase = (1.0 - sst(0.0005, 0.0070, fn)) * kopf
    S = S * (1.0 - nase[:, None]) + (S * 0.40 * np.array((1.0, 0.97, 0.97)) + 0.018) * nase[:, None]
    x_ = a - Q["NASE_C"][0]
    z_ = c - Q["NASE_C"][2]
    nl = Q["nasenloch"](x_, B, z_)
    loch = (1.0 - sst(-0.004, 0.0035, nl)) * nase
    S = S * (1.0 - 0.75 * loch[:, None])
    # Auge: tief und dunkel, mit Lidrand, kein Glanzpunkt
    AUGE, AU, AV, AW = Q["AUGE"], Q["AU"], Q["AV"], Q["AW"]
    x, y, z = Q["_acht"](a, B, c, AUGE, AU, AV, AW)
    sp = Q["spalt2d"](y, z)
    vorn = sst(-0.022, -0.005, x) * kopf
    schlitz = (1.0 - sst(-0.0005, 0.0026, sp)) * vorn
    lidrand = (1.0 - sst(0.0014, 0.0078, sp)) * vorn
    schatten = (1.0 - sst(0.006, 0.030, np.sqrt(y * y + z * z))) * vorn
    S = S * (1.0 - 0.16 * schatten[:, None])
    S = S * (1.0 - 0.50 * lidrand[:, None])
    S = S * (1.0 - schlitz[:, None]) + np.array((0.030, 0.019, 0.014)) * schlitz[:, None]
    # Mundlinie: nur eine dunkle Rille, keine gemalte Lippe
    dv = Q["lippe"](a, B) - c
    vorne = sst(Q["ECKE"] - 0.006, Q["ECKE"] + 0.034, a) * kopf
    linie = (1.0 - sst(0.0006, 0.0040, np.abs(dv))) * vorne
    saum = (1.0 - sst(0.001, 0.0085, np.abs(dv + 0.0030))) * vorne
    S = S * (1.0 - 0.18 * saum[:, None])
    S = S * (1.0 - 0.50 * linie[:, None])
    fur = Q["cap"](a, B, c, (0.497, 0.0, 0.010), (0.486, 0.0, -0.046), 0.0)
    rille = (1.0 - sst(0.0015, 0.0050, fur)) * kopf
    S = S * (1.0 - 0.30 * rille[:, None])
    return S


def unscharf(col, k, runden=2):
    """Kleine Unschaerfemaske im Texturraum: die Fellstriche sollen nach dem Mischen wieder Biss haben."""
    b = col.copy()
    for _ in range(runden):
        b = (np.roll(b, 2, 0) + np.roll(b, -2, 0) + np.roll(b, 2, 1) + np.roll(b, -2, 1) + b * 2.0) / 6.0
    if np.ndim(k) == 2:
        k = k[..., None]
    return np.clip(col + (col - b) * k, 0.0, 1.0)




def h2f(P):
    return (np.asarray(P, dtype=np.float64) - np.array((X0_ALT, 0.0, ZMIN_ALT))) * GROESSE


def f2h(P):
    return np.asarray(P, dtype=np.float64) / GROESSE + np.array((X0_ALT, 0.0, ZMIN_ALT))


# ------------------------------------------------------------------ _anim: altes Spielnetz lesen (Kopf und Krallen bleiben)
def alt_netz():
    """Altes Spielnetz (FBX, Meter) mit UV. Gegend je Flaeche: 1 Kopf (UV-Inseln wie baer_export Gegend 1, nach Mehrheit),
    2 Kralle (kleine Schalen), 0 Rumpf."""
    from bpy_extras import bmesh_utils
    bpy.ops.import_scene.fbx(filepath=ALT_FBX, use_custom_normals=False, use_image_search=False)
    ob = [o for o in bpy.context.selected_objects if o.type == "MESH"][0]
    me = ob.data
    n = len(me.vertices)
    V = np.empty(n * 3, dtype=np.float32)
    me.vertices.foreach_get("co", V)
    V = V.reshape(n, 3)
    F = np.array([tuple(p.vertices) for p in me.polygons], dtype=np.int64)
    assert F.shape[1] == 3
    uv = np.empty(len(me.loops) * 2, dtype=np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    LI = np.array([tuple(p.loop_indices) for p in me.polygons], dtype=np.int64)
    UVF = uv[LI]
    par = np.arange(n)

    def wz(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    for t in F:
        a = wz(t[0])
        par[wz(t[1])] = a
        par[wz(t[2])] = a
    r = np.array([wz(i) for i in range(n)])
    u, c = np.unique(r, return_counts=True)
    kralle_f = (r != u[c.argmax()])[F[:, 0]]
    return ob, me, V, F, UVF, kralle_f


def kopf_inseln(Q, me, V, F):
    from bpy_extras import bmesh_utils
    H = f2h(V.astype(np.float64))
    cen = H[F].mean(1)
    L = Q["w2l"](cen)
    hb = Q["huelle_basis"](L[:, 0], L[:, 1], L[:, 2])
    roh = (hb < 0.075) & (L[:, 0] > -0.10)
    bm = bmesh.new()
    bm.from_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    kopf = np.zeros(len(F), dtype=bool)
    for ins in bmesh_utils.bmesh_linked_uv_islands(bm, uvl):
        idx = np.array([f.index for f in ins])
        if roh[idx].mean() > 0.5:
            kopf[idx] = True
    bm.free()
    return kopf


def rand_schleifen(F):
    """Randkanten eines Flaechenstuecks (gerichtet wie in den Flaechen) zu geschlossenen Schleifen."""
    E = np.concatenate((F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]), 0)
    s = set(map(tuple, E.tolist()))
    rand = [e for e in s if (e[1], e[0]) not in s]
    nach = {}
    for a, b in rand:
        assert a not in nach, "Rand verzweigt"
        nach[a] = b
    schleifen = []
    frei = set(nach)
    while frei:
        a0 = frei.pop()
        sl = [a0]
        b = nach[a0]
        while b != a0:
            sl.append(b)
            frei.discard(b)
            b = nach[b]
        schleifen.append(sl)
    return schleifen


def taubin(V, E, n, runden, w, lam=0.5, mu=-0.53):
    """Volumentreues Glaetten, je Punkt gewichtet (w 0 = fest)."""
    cnt = np.bincount(E[:, 0], minlength=n) + np.bincount(E[:, 1], minlength=n)
    W = V.copy()
    for _ in range(runden):
        for f in (lam, mu):
            S = np.zeros_like(W)
            for ax in range(3):
                S[:, ax] = np.bincount(E[:, 0], weights=W[E[:, 1], ax], minlength=n) + np.bincount(E[:, 1], weights=W[E[:, 0], ax], minlength=n)
            W = W + (S / np.maximum(cnt, 1)[:, None] - W) * (f * w)[:, None]
    return W


def falten_fuellen(V, T, E, n, runden, w, schritt=0.5):
    """Hebt nur nach innen gewoelbte Stellen (Achsel, Leiste, Bauchrand) ein Stueck nach aussen: der Umriss wird weicher,
    gewoelbte Flaechen schrumpfen nicht."""
    cnt = np.bincount(E[:, 0], minlength=n) + np.bincount(E[:, 1], minlength=n)
    W = V.copy()
    for _ in range(runden):
        N = v_normalen(W, T)
        S = np.zeros_like(W)
        for ax in range(3):
            S[:, ax] = np.bincount(E[:, 0], weights=W[E[:, 1], ax], minlength=n) + np.bincount(E[:, 1], weights=W[E[:, 0], ax], minlength=n)
        lap = S / np.maximum(cnt, 1)[:, None] - W
        aus = np.maximum((lap * N).sum(1), 0.0)
        W = W + N * (aus * schritt * w)[:, None]
    return W


def alpha_weich(A, sigma):
    """Gauss je Ansicht (getrennt in x und y), gegen einzelne Haarspitzen im Umriss."""
    r = int(math.ceil(sigma * 3))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    out = []
    for a in A:
        b = np.apply_along_axis(lambda z: np.convolve(z, k, mode="same"), 0, a)
        b = np.apply_along_axis(lambda z: np.convolve(z, k, mode="same"), 1, b)
        out.append(b.astype(np.float32))
    return out


def zip_streifen(LH, LD, P):
    """Verbindet zwei geschlossene Randschleifen mit einem Dreiecksstreifen entlang der Bogenlaenge.
    LH laeuft wie die Kanten seiner Flaechen (Kopf), LD wie die Kanten seiner Flaechen (Rumpf). Der Streifen muss jede
    Randkante in Gegenrichtung enthalten: LH wird rueckwaerts, LD (umgedreht) vorwaerts durchlaufen."""
    LD = LD[::-1]

    def dreh(L):
        Q_ = P[L]
        c = Q_.mean(0)
        return np.cross(Q_ - c, np.roll(Q_, -1, 0) - c).sum(0)

    assert np.dot(dreh(LH), dreh(LD)) > 0, "Kopfrand und Rumpfrand laufen gegeneinander"

    def param(L):
        Q_ = P[L]
        s = np.concatenate(([0.0], np.cumsum(np.linalg.norm(np.roll(Q_, -1, 0) - Q_, axis=1))))
        return s[:-1] / s[-1]

    d = np.linalg.norm(P[LD] - P[LH[0]], axis=1)
    j0 = int(np.argmin(d))
    LD = LD[j0:] + LD[:j0]
    sa = np.append(param(LH), 1.0)
    sb = np.append(param(LD), 1.0)
    na, nb = len(LH), len(LD)
    i = j = 0
    tri = []
    while i < na or j < nb:
        a0, a1 = LH[i % na], LH[(i + 1) % na]
        b0, b1 = LD[j % nb], LD[(j + 1) % nb]
        if j >= nb or (i < na and sa[i + 1] <= sb[j + 1]):
            tri.append((a1, a0, b0))
            i += 1
        else:
            tri.append((b0, b1, a0))
            j += 1
    return tri


def huelle_bauen(Q, koerper, normal_runden, fell_plus, sigma, stufen, d_runden, zotteln):
    """Schritte 1-5 von baer_export.stufe_netz: Haut (Kopfhuelle, Rumpfhaut 'koerper', Nase, Zehen) zu einem Voxelnetz, dann
    nach aussen schaelen. Gibt die Fellhuelle W auf dem Netz der Haut zurueck (vor der zweiten Voxelrunde) und das Objekt 'roh'."""
    sst = Q["sst"]
    KV, KQ = Q["netz_aus_feld"](Q["huelle_basis"], (-0.42, -0.27, -0.28), (0.535, 0.27, 0.235), 0.0040, grob=4)
    KV = Q["glaette"](KV, KQ, 0.35, 2)
    VS, FS = [], []
    off = 0

    def dazu(V_, F_):
        nonlocal off
        VS.append(np.asarray(V_))
        FS.extend([tuple(int(i) + off for i in f) for f in F_])
        off += len(V_)

    dazu(Q["l2w"](KV), np.asarray(KQ).tolist())
    teile = [bpy.data.objects[koerper], bpy.data.objects["nase"]] + [o for o in bpy.data.objects if o.name.startswith("pfote_")]
    for ob in teile:
        V_, F_ = welt_netz(ob)
        dazu(V_, F_)
    roh = neues_netz("roh", np.concatenate(VS, 0), FS)
    rm = roh.modifiers.new("r", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = PF_VOXEL[0]   # Lauf baer-pfoten: wie baer-fell 8,5 mm (feiner aenderte den Kopf-Nahtrand)
    rm.adaptivity = 0.0
    bpy.context.view_layer.objects.active = roh
    roh.select_set(True)
    bpy.ops.object.modifier_apply(modifier=rm.name)
    V, T = netz_arrays(roh.data)
    E = kanten(T)
    N = v_normalen(V, T)
    N = glatt_feld(N, E, len(V), normal_runden, 0.6)
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
    L3 = Q["w2l"](V)
    a, b, c = L3[:, 0], L3[:, 1], L3[:, 2]
    hb = Q["huelle_basis"](a, b, c)
    L_, m_, r_, R_ = Q["haar_werte"](a, b, c)
    koerper_bein = 1.0 - sst(0.20, 0.50, V[:, 2])
    dlim_k = 0.112 - 0.022 * koerper_bein + fell_plus * (1.0 - 0.5 * koerper_bein)
    # Lauf baer-pfoten: zwei Schaelungen. (a) wie baer-fell (alte Grenze dlim_alt, alte Ansichten ANS_ALT oder ANS, 30 Runden
    # geglaettet) fuer alles ueber Spiel-z 0,37; (b) an Pfote und Unterschenkel/Unterarm waechst die Huelle nur bis zum Soll des
    # Spielnetzes (pfoten_abstand 'soll'), wo die Pfotengrenze greift genau bis dorthin, kaum geglaettet (Zehenrillen bleiben offen).
    # Uebergang z 0,29-0,37 (Spiel); so bleibt der Rumpf ueber dem Knie wie baer-fell und der Wechsel der Felldicke ist weich.
    zs_ = (V[:, 2] - ZMIN_ALT) * GROESSE
    dsoll = Q["pfoten_abstand"](V, "soll")
    m_pf = 1.0 - sst(0.04 / GROESSE, 0.10 / GROESSE, dsoll)
    d_pf = np.maximum(-dsoll, 0.0015 / GROESSE)
    ze = dsoll   # (nur fuer die abgeschalteten Zotteln)
    log("PFOTE Huelle: Punkte im Pfotenbereich %d, Haut ausserhalb des Solls (unter z 0,30) %d (max %.1f mm Spielmass)" % (
        int((m_pf > 0.5).sum()), int(((m_pf > 0.5) & (dsoll > 0.001) & (zs_ < 0.30)).sum()),
        float(np.max(np.where((m_pf > 0.5) & (zs_ < 0.30), dsoll, 0.0))) * GROESSE * 1000))
    kopf_g = 1.0 - sst(0.006, 0.17, hb)
    dlim_k = np.minimum(dlim_k, 0.112 + fell_plus - 0.082 * sst(0.96, 1.08, -V[:, 0]))
    dlim_h = L_ * Q["KOPF_SK"] * 0.60 + 0.0015
    dlim_alt = dlim_k + (dlim_h - dlim_k) * kopf_g
    dlim = dlim_alt * (1.0 - m_pf) + np.minimum(dlim_alt, d_pf) * m_pf
    dmax_ = 0.15 if stufen == 16 else 0.16
    views = json.load(open(ANS + "kameras.json"))
    alpha = alpha_laden(views)
    if sigma > 0:
        alpha = alpha_weich(alpha, sigma)
    d_neu = huelle_schaelen(V, N, dlim, views, alpha, dmax=dmax_, stufen=stufen)
    if ANS_ALT:
        del alpha
        views = json.load(open(ANS_ALT + "kameras.json"))
        alpha = alpha_laden(views, ordner=ANS_ALT)
        if sigma > 0:
            alpha = alpha_weich(alpha, sigma)
        log("PFOTE Huelle: Rumpf aus den alten Ansichten", ANS_ALT)
    d_alt = huelle_schaelen(V, N, dlim_alt, views, alpha, dmax=dmax_, stufen=stufen)
    del alpha
    stufen_d = len(np.unique(np.round(d_alt, 6)))
    log("Haut %s: %d Punkte; Schaelen d Mittel %.4f max %.4f, verschiedene Werte %d" % (koerper, len(V), d_alt.mean(), d_alt.max(), stufen_d))
    d_alt = glatt_feld(d_alt, E, len(V), d_runden, 0.5)
    schritt_ = dmax_ / (stufen - 1)
    an_grenze = (m_pf > 0.0) & (d_neu >= dlim - 1.01 * schritt_)
    d_neu = np.where(an_grenze, dlim, d_neu)
    d_neu = glatt_feld(d_neu, E, len(V), 3, 0.5)
    # Uebergang nach der Hoehe, an der der Punkt mit der alten Huelle LANDEN wuerde (Unterseite des Knies haengt sonst herab)
    z_aussen = zs_ + N[:, 2] * d_alt * GROESSE
    w_pf = glatt_feld(m_pf * (1.0 - sst(PF_UEB[0], PF_UEB[1], z_aussen)), E, len(V), 6, 0.5)
    d = d_alt * (1.0 - w_pf) + d_neu * w_pf
    # Knie: die Felldicke wechselt hier von der Pfote (2-4 cm) zum Rumpf (7 cm); im Band nachglaetten, damit keine Stufe (Stulpe) bleibt
    band = glatt_feld(sst(PF_BAND[0], PF_BAND[1], z_aussen) * (1.0 - sst(PF_BAND[2], PF_BAND[3], z_aussen)) * m_pf, E, len(V), 6, 0.5)
    d = d * (1.0 - band) + glatt_feld(d, E, len(V), PF_BAND_RUNDEN, 0.5) * band
    # Hinterkante Oberschenkel/Hock (Spiel-z 0,26-0,48) nicht hinter die heutige (GLB 2a4837f6, Schnitte): die Haut steht dort durch die
    # neue dritte Beinkugel bis 1,2 cm weiter hinten; mit der alten Huelle saesse das Hinterteil im Sitzen 2,3 cm im Boden
    xs_ = (V[:, 0] - X0_ALT) * GROESSE
    nx_ = N[:, 0]
    z_a2 = zs_ + N[:, 2] * d * GROESSE
    x_a2 = xs_ + nx_ * d * GROESSE
    x_lim = np.interp(z_a2, *PF_HINTEN_HEUTE) + 0.004   # 4 mm Rand: mit den Endgewichten sass die Kniekehle im Sitzen sonst 0,3 cm im Boden
    zone = (xs_ < -0.40) & (np.abs(V[:, 1]) * GROESSE > 0.08) & (z_a2 > 0.24) & (z_a2 < 0.50) & (nx_ < -0.15)
    zu_weit = zone & (x_a2 < x_lim)
    d_k = np.where(zu_weit, np.maximum((x_lim - xs_) / np.minimum(nx_, -0.15) / GROESSE, 0.0015), d)
    d_k = np.minimum(d, d_k)
    d = np.minimum(d, glatt_feld(d_k, E, len(V), 4, 0.5) + 0.0005)
    log("PFOTE Huelle: Hinterkante auf heute begrenzt, Punkte %d" % int(zu_weit.sum()))
    log("PFOTE Huelle: an der Pfotengrenze %d Punkte, Anteil Pfoten-Huelle > 0,5: %d Punkte" % (int(an_grenze.sum()), int((w_pf > 0.5).sum())))
    if zotteln:
        # wie baer_export Schritt 5
        bein = 1.0 - sst(0.42, 0.62, V[:, 2])
        zott = buschel_rauschen(V, bein)
        gesicht = 1.0 - sst(0.0, 0.11, hb)
        pfote = 1.0 - sst(0.015, 0.09, ze)
        grob = 0.5 + 0.5 * np.sin(V[:, 0] * 3.1 + 1.0) * np.sin(V[:, 1] * 4.3 + 0.4) * np.sin(V[:, 2] * 3.7 + 2.0)
        amp = (0.036 + 0.030 * grob) * (1.0 - gesicht) * (1.0 - pfote) * (1.0 - 0.25 * bein)
        d = d - amp * 0.42 + amp * zott
        log("Zotteln: Ausschlag je Punkt max %.4f, Mittel %.4f (m)" % ((amp * np.maximum(zott, 0.42)).max(), (amp * np.abs(zott - 0.42)).mean()))
    d = np.maximum(d, 0.0015)
    W = V + N * d[:, None]
    W[:, 2] = np.maximum(W[:, 2], ZMIN_ALT)  # Sohle auf dem Boden des alten Netzes (Spiel z = 0)
    return roh, W, T


# ------------------------------------------------------------------ Lauf baer-fell: Form am dichten Rumpf (vor dem Verringern)
def _sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def form_fell(W, T, E, n):
    """Verschiebt den dichten Rumpf (Hochmodell-Masse) entlang der Normalen, Masken in Spielmetern:
    Gesaessfalte (Mittellinie hinten, vom Schwanzansatz bis zum Schritt, nach innen), Schultern seitlich voller,
    Flanken/Huefte unten seitlich schlanker. Gesicht, Hals und Pfoten bleiben (Masken dort 0). Die Verschiebung wird als
    Feld ueber das Netz geglaettet, damit keine Kante entsteht."""
    Fm = h2f(W)
    x, y, z = Fm[:, 0], Fm[:, 1], Fm[:, 2]
    N = v_normalen(W, T)
    nx, ny = N[:, 0], N[:, 1]
    # Gesaessfalte: Mittellinie, nur hinten (Normale nach hinten), zwischen Schritt und Schwanzansatz
    falte = (FORM_FALTE * np.exp(-(y / 0.040) ** 2) * _sst(-0.52, -0.64, x) * _sst(0.25, -0.35, nx)
             * _sst(0.30, 0.40, z) * (1.0 - _sst(0.58, 0.68, z)))
    # Schultern: seitlich ueber den Vorderbeinen bis unter den Widerrist
    # Nachbesserung 09.11.: Masken nach der Messung fix/werkzeug/ei.py (breiteste Punkte im Aufrichten: oben Ruhe-z 0,40-0,83,
    # unten Ruhe-z 0,39-0,77) - Schulter ab z 0,38 statt 0,44, Flanke bis z 0,80 statt 0,70
    schulter = (FORM_SCHULTER * _sst(0.0, 0.12, x) * (1.0 - _sst(0.40, 0.54, x)) * _sst(0.38, 0.55, z)
                * (1.0 - _sst(0.86, 0.98, z)) * _sst(0.25, 0.65, np.abs(ny)))
    # Flanken und Huefte unten: seitlich hinter den Vorderbeinen bis ueber die Hinterbeine
    flanke = (FORM_FLANKE * _sst(0.02, -0.10, x) * _sst(-0.72, -0.60, x) * _sst(0.30, 0.40, z) * (1.0 - _sst(0.66, 0.80, z))
              * _sst(0.25, 0.65, np.abs(ny)))
    d = (schulter - flanke - falte) / GROESSE
    d = glatt_feld(d, E, n, 8, 0.5)
    W2 = W + N * d[:, None]
    log("FORM: Gesaessfalte bis %.1f mm, Schultern bis %.1f mm, Flanken bis %.1f mm (Spielmass); verschobene Punkte %d" % (
        falte.max() * 1000, schulter.max() * 1000, flanke.max() * 1000, int((np.abs(d) > 1e-4).sum())))
    return W2


def _spitzen(u, v):
    """Reihe spitzer Zotteln: je Zelle (Breite 1 in u) eine Spitze, Lage und Hoehe je Zelle leicht verschieden (fest, ohne Zufall
    zur Laufzeit). v verschiebt die Phase (versetzte Reihen). Ergebnis 0..1, schmale Spitzen mit breiten Taelern."""
    zelle = np.floor(u + 0.5 * np.floor(v))
    h1 = np.mod(np.sin(zelle * 12.9898 + np.floor(v) * 78.233) * 43758.5453, 1.0)
    h2 = np.mod(np.sin(zelle * 39.3468 + np.floor(v) * 11.135) * 24634.6345, 1.0)
    f = np.mod(u + 0.5 * np.floor(v), 1.0) - (0.5 + 0.25 * (h1 - 0.5))
    tri = np.clip(1.0 - np.abs(f) * 2.4, 0.0, 1.0) ** 2.2
    quer = np.clip(1.0 - np.abs(np.mod(v, 1.0) - 0.5) * 2.0, 0.0, 1.0) ** 1.2
    return tri * quer * (0.65 + 0.35 * h2)


def zotteln_fell(W, T):
    """Kurze spitze Zotteln (Kevins Punkt 1) nur an Umrisslinien, ohne langwelligen Anteil: Rueckenlinie mit Nacken, Bauchfranse,
    Hinterkante der Vorderbeine, Hinterteil. Spitzen ZOTTEL_ABSTAND auseinander, Ausschlag bis ZOTTEL_AMP entlang der Normalen."""
    Fm = h2f(W)
    x, y, z = Fm[:, 0], Fm[:, 1], Fm[:, 2]
    N = v_normalen(W, T)
    nx, nz = N[:, 0], N[:, 2]
    a = ZOTTEL_ABSTAND
    # Rueckenlinie und Nacken: nach oben zeigend, schmales Band an der Mittellinie (Nacken breiter)
    breite = 0.06 + 0.06 * _sst(0.25, 0.50, x)
    ruecken = _sst(0.55, 0.85, nz) * (1.0 - _sst(breite * 0.6, breite, np.abs(y))) * _sst(-0.72, -0.62, x) * (1.0 - _sst(0.52, 0.62, x))
    m_r = ruecken * _spitzen(-x / a, y / (a * 1.3))
    # Bauchfranse: nach unten zeigend zwischen den Beinen, haengende Spitzen
    bauch = _sst(0.55, 0.85, -nz) * _sst(-0.45, -0.35, x) * (1.0 - _sst(0.12, 0.22, x)) * (1.0 - _sst(0.16, 0.24, np.abs(y))) * _sst(0.26, 0.32, z)
    m_b = bauch * _spitzen(x / a, y / a)
    # Hinterkante der Vorderbeine (nach hinten zeigend, zwischen Ellbogen und Handgelenk)
    bein_v = _sst(0.45, 0.80, -nx) * _sst(0.08, 0.16, x) * (1.0 - _sst(0.40, 0.48, x)) * _sst(0.14, 0.20, z) * (1.0 - _sst(0.42, 0.50, z)) * _sst(0.10, 0.16, np.abs(y))
    m_v = bein_v * _spitzen(z / a, y / a)
    # Hinterteil: nach hinten zeigend, oberhalb des Schritts
    hinten = _sst(0.50, 0.80, -nx) * (1.0 - _sst(-0.66, -0.56, x)) * _sst(0.36, 0.44, z) * (1.0 - _sst(0.70, 0.78, z))
    m_h = hinten * _spitzen(z / a, y / a)
    d = ZOTTEL_AMP * np.maximum.reduce([m_r, m_b, m_v, m_h]) / GROESSE
    log("ZOTTELN: Ausschlag bis %.1f mm (Spielmass), Punkte mit Zotteln %d (Ruecken %d, Bauch %d, Vorderbein %d, Hinterteil %d)" % (
        d.max() * GROESSE * 1000, int((d > 1e-4).sum()), int((m_r > 0.05).sum()), int((m_b > 0.05).sum()), int((m_v > 0.05).sum()), int((m_h > 0.05).sum())))
    return W + N * d[:, None]


# ------------------------------------------------------------------ Lauf baer-fell: Sohlen mit Ballen
C2C_FUSS = os.environ.get("BAER_2C_FUSS", "1") == "1"   # 2c: neuer Ballenplan hinten
C2C_KRALLE_DX = float(os.environ.get("BAER_2C_KRALLE_DX", "-0.070"))   # 2c: Hinterkrallen in x (SPEZ_2C.md 4)
K1_FAKTOR = 4.1 / 4.6 - 1.0   # Lauf baer-pfoten: Krallen vorn, dy = (y_kralle - y_mitte) * K1_FAKTOR (SPEZ_PFOTEN.md 0 Nr. 4)
BALLEN_HUB = 0.0100        # Furchen so weit (m) ueber den Ballen (Lauf baer-pfoten: 8 -> 10 mm; 12 mm gab 1,55 cm Relief, Soll 1,0-1,4)
SOHLE_Z = 0.012            # Sohlenflaeche: Dreiecksmitte tiefer als das ...
SOHLE_NZ = -0.60           # ... und Normale so weit nach unten
RASTER = 0.0200            # Abstand der Furchen-Punkte (m) (Lauf baer-pfoten: 15 -> 20 mm, Dreiecks-Budget SPEZ 2.5)
VIELECK_SKALA = 0.012      # Ballen als Vieleck: q = 1 + Randabstand / VIELECK_SKALA (q < 1 im Ballen, Kante weich wie bei den Ellipsen)
RAND_FREI = 0.008          # innen so weit vom Rand keine neuen Punkte (gegen Splitter)


def _komponenten(F, n):
    par = np.arange(n)

    def wz(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    for t in F:
        a = wz(t[0])
        par[wz(t[1])] = a
        par[wz(t[2])] = a
    return np.array([wz(int(t[0])) for t in F])


def _rand(F):
    E = np.concatenate((F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]), 0)
    s = set(map(tuple, E.tolist()))
    rand = [e for e in s if (e[1], e[0]) not in s]
    nach = {}
    for a, b in rand:
        if a in nach:
            return None
        nach[a] = b
    schleifen = []
    frei = set(nach)
    while frei:
        a0 = frei.pop()
        sl = [a0]
        b = nach[a0]
        while b != a0:
            sl.append(b)
            frei.discard(b)
            b = nach[b]
        schleifen.append(sl)
    return schleifen


def _chaikin(P, runden=3):
    P = np.asarray(P, dtype=float)
    for _ in range(runden):
        Q_ = np.roll(P, -1, 0)
        P = np.stack((0.75 * P + 0.25 * Q_, 0.25 * P + 0.75 * Q_), 1).reshape(-1, 2)
    return P


def _poly_sd(P, poly):
    """Vorzeichenbehafteter Abstand (m) von Punkten P (n, 2) zum geschlossenen Vieleck poly (m, 2): innen negativ."""
    P = np.asarray(P, dtype=float)
    A_ = np.asarray(poly, dtype=float)
    B_ = np.roll(A_, -1, 0)
    d = np.full(len(P), 9.0)
    inn = np.zeros(len(P), dtype=bool)
    for a_, b_ in zip(A_, B_):
        ab = b_ - a_
        t = np.clip(((P - a_) @ ab) / max(ab @ ab, 1e-12), 0, 1)
        d = np.minimum(d, np.linalg.norm(P - (a_ + t[:, None] * ab), axis=1))
        kreuz = ((a_[1] > P[:, 1]) != (b_[1] > P[:, 1])) & (P[:, 0] < (b_[0] - a_[0]) * (P[:, 1] - a_[1]) / (b_[1] - a_[1] + 1e-300) + a_[0])
        inn ^= kreuz
    return np.where(inn, -d, d)


def _2c_platte(cx=-0.446, cy=0.242, ax=0.106, ay_vorn=0.080, ay_ferse=0.066, bieg=0.0, ex=3.4, n=48):
    # fix1 2c: ay 0,078/0,062 -> 0,080/0,066 (der Fuss ist 2 cm breiter, der Fellkranz bleibt 1,5-2 cm breit)
    """2c: Sohlenballen hinten als Super-Oval (Exponent ex), vorn breiter (14,1 cm bei x -0,40) als an der Ferse (13,0 bei x -0,50);
    Vorderkante x -0,340 (Furche ~1,3 cm zu den Zehenballen). Hinten bis x -0,552 (Ferse -0,555): die Textur rollt das Leder dort um die Fersenkante."""
    t = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    c_, s_ = np.cos(t), np.sin(t)
    cs = np.sign(c_) * np.abs(c_) ** (2.0 / ex)
    ss = np.sign(s_) * np.abs(s_) ** (2.0 / ex)
    ay = ay_ferse + (ay_vorn - ay_ferse) * (1.0 + c_) * 0.5
    return [[round(float(cx + ax * a_ + bieg * c * c), 5), round(float(cy + y_ * b_), 5)] for a_, c, b_, y_ in zip(cs, c_, ss, ay)]


# 2c (SPEZ_2C.md 4, Kevins Vorlage): fuenf grosse runde Zehenballen (Durchmesser 3,6 cm) dicht im Bogen, Mitte 3,0 cm hinter der
# (um -0,070 verschobenen) Krallenwurzel, aeussere 2,8-3,0 cm weiter hinten; ein grosser Sohlenballen x -0,553..-0,337 (vorn 14,6 cm,
# Ferse 12 cm), Furche ~1,2 cm zu den Zehenballen. Ersetzt fuer hinten FIX1_PLAN["H"].
C2C_PLAN_H = dict(platte_xy=_2c_platte(ex=2.4),   # fix1 2c (Pruefbericht M2): Netz-Platte Super-Oval 2,4 wie die Textur (2,3), nicht 3,4
                  zehenballen_x_y_skala=[[-0.331, 0.169, 0.92], [-0.311, 0.205, 1.0], [-0.303, 0.240, 1.0], [-0.310, 0.276, 1.0],
                                         [-0.330, 0.311, 0.97]],
                  zehenballen_r_cm=[1.80, 1.80])


def ballen_plan(pfote, krallen):
    """Lauf baer-pfoten: Ballen aus spez/pfoten_plan.json (Spielmeter; rechte Pfoten y gespiegelt): fuenf Zehenballen als Ellipsen
    (Name, cx, cy, ax, ay, 0) und die Sohlenplatte (hinten) bzw. der Handballen (vorn) als Vieleck (Name, cx, cy, 0, 0, 0, Vieleck).
    Der Handwurzelballen liegt angehoben (nicht im flachen Abdruck): Geometrie aus dem Hochmodell, Farbe Sache der Textur.
    krallen wird nur noch geprueft (5 je Pfote)."""
    assert len(krallen) == 5
    PL = json.load(open(PLAN))[pfote[0] + "L"]
    if FIX1:
        PL = dict(PL)
        PL.update(FIX1_PLAN[pfote[0]])
    if pfote[0] == "H" and C2C_FUSS:
        PL = dict(PL)
        PL.update(C2C_PLAN_H)
    sy = 1.0 if pfote[1] == "L" else -1.0
    ry, rx = [r / 100.0 for r in PL["zehenballen_r_cm"]]
    plan = []
    for i, (cx, cy, sk) in enumerate(PL["zehenballen_x_y_skala"]):
        plan.append(("zehe%d" % (i + 1), cx, sy * cy, rx * sk, ry * sk, 0.0))
    poly = np.array(PL.get("platte_xy") or PL["handballen_xy"], dtype=float)
    poly = _chaikin(poly, 3)
    poly[:, 1] *= sy
    if sy < 0:
        poly = poly[::-1]
    m = poly.mean(0)
    plan.append(("platte" if pfote[0] == "H" else "handballen", float(m[0]), float(m[1]), 0.0, 0.0, 0.0, poly))
    return plan


def ballen_plan_fell(pfote, krallen):
    """(baer-fell, nicht mehr benutzt) Ballen als Ellipsen in Spielmetern: (Name, Mitte x, Mitte y, Halbachse x, Halbachse y, Biegung).
    krallen: (5, 3) Krallenmitten der Pfote, nach y sortiert. Biegung: Mitte der Ellipse um so viel (m) nach vorn gewoelbt."""
    K = np.asarray(krallen, dtype=float)
    yc = K[2, 1]
    s = 1.0 if K[:, 1].mean() > 0 else -1.0
    plan = []
    vorn = pfote[0] == "V"
    for i, k in enumerate(K):
        # Zehenballen hinter der Kralle, zur Mitte hin etwas zusammen
        dx = 0.060 if vorn else 0.052
        plan.append(("zehe%d" % (i + 1), k[0] - dx, yc + (k[1] - yc) * 0.93, 0.0215 if vorn else 0.019, 0.0185 if vorn else 0.0165, 0.0))
    xz = min(p[1] for p in plan)
    if vorn:
        # Sohlenballen (Mittelhand): breit, querliegend, nach vorn gewoelbt; Handwurzelballen klein, hinten aussen
        plan.append(("sohle", xz - 0.066, yc, 0.032, 0.088, 0.012))
        plan.append(("handwurzel", xz - 0.150, yc + s * 0.030, 0.022, 0.026, 0.0))
    else:
        # Mittelfussballen querliegend, dahinter langer Fersenballen (zur Ferse schmaler)
        plan.append(("sohle", xz - 0.060, yc, 0.030, 0.080, 0.010))
        plan.append(("ferse", xz - 0.218, yc + s * 0.004, 0.100, 0.056, 0.0))
    return plan


def ballen_q(plan, X, Y):
    """Je Punkt kleinster normierter Ellipsenradius ueber alle Ballen (< 1 im Ballen) und welcher Ballen."""
    q = np.full(len(X), 9.0)
    wer = np.full(len(X), -1)
    for i, b_ in enumerate(plan):
        if len(b_) > 6:
            qi = 1.0 + _poly_sd(np.c_[X, Y], b_[6]) / VIELECK_SKALA
            neu = qi < q
            q = np.where(neu, qi, q)
            wer = np.where(neu, i, wer)
            continue
        (_n, cx, cy, ax, ay, bieg) = b_
        dy = (Y - cy) / ay
        dx = (X - cx - bieg * (1.0 - np.clip(dy, -1, 1) ** 2)) / ax
        if _n == "ferse":
            # zur Ferse (hinten) schmaler: Halbachse y nimmt nach hinten bis auf 70 % ab
            t = np.clip(-(X - cx) / ax, 0, 1)
            dy = (Y - cy) / (ay * (1.0 - 0.30 * t))
            dx = (X - cx) / ax
        qi = np.sqrt(dx * dx + dy * dy)
        neu = qi < q
        q = np.where(neu, qi, q)
        wer = np.where(neu, i, wer)
    return q, wer


def hoehe(plan, X, Y):
    """Ballen bei z = 0 mit runder Kante, Furchen BALLEN_HUB hoeher."""
    q, _ = ballen_q(plan, X, Y)
    return BALLEN_HUB * _sst(0.62, 1.22, q)


def sohlen_bauen(V, T, gegend):
    """V (n,3), T (m,3), gegend (m,) 0 Rumpf, 1 Kopf, 2 Kralle. Gibt V2, T2, gegend2, sohle_id je Dreieck (0 keine, 1..4),
    Plan je Pfote zurueck. Neue Punkte werden hinten angehaengt; alte Punkte der Scheibe bleiben unbenutzt (Aufrufer raeumt auf)."""
    from mathutils.geometry import delaunay_2d_cdt
    from mathutils import Vector
    V = np.asarray(V, dtype=np.float64)
    T = np.asarray(T, dtype=np.int64)
    n = len(V)
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
    c = V[T].mean(1)
    # Krallen je Pfote
    kr_f = T[gegend == 2]
    kr_r = _komponenten(kr_f, n)
    krallen = {}
    for r in np.unique(kr_r):
        vs = np.unique(kr_f[kr_r == r])
        m = V[vs].mean(0)
        key = ("V" if m[0] > -0.1 else "H") + ("L" if m[1] > 0 else "R")
        krallen.setdefault(key, []).append(m)
    kand = (gegend == 0) & (c[:, 2] < SOHLE_Z) & (fn[:, 2] < SOHLE_NZ)
    weg = np.zeros(len(T), dtype=bool)
    neue_V, neue_T, neue_id, plaene = [], [], [], {}
    n_neu = n
    for pid, key in enumerate(("VL", "VR", "HL", "HR"), start=1):
        K = np.array(sorted(krallen[key], key=lambda p: p[1]))
        assert len(K) == 5, (key, len(K))
        sx = 1 if key[0] == "V" else -1
        sy = 1 if key[1] == "L" else -1
        m = kand & (np.sign(c[:, 0] + 0.1) == sx) & (np.sign(c[:, 1]) == sy)
        idx = np.nonzero(m)[0]
        r = _komponenten(T[idx], n)
        u, cnt = np.unique(r, return_counts=True)
        idx = idx[r == u[cnt.argmax()]]
        # Loecher schliessen: Rumpfdreiecke, deren Punkte alle schon in der Sohle liegen
        for _ in range(3):
            schl = _rand(T[idx])
            if schl is not None and len(schl) == 1:
                break
            vs = set(np.unique(T[idx]).tolist())
            dazu = np.nonzero((gegend == 0) & np.array([all(int(v) in vs for v in t) for t in T]) & ~np.isin(np.arange(len(T)), idx))[0]
            idx = np.union1d(idx, dazu)
        # Lauf baer-pfoten: Rand aufraeumen (Fliegen = Punkte mit zwei Randwegen, Ohren = Dreiecke mit zwei Randkanten), groesstes
        # Stueck behalten, Loecher schliessen - bis der Rand genau eine Schleife ist
        for _r in range(30):
            schl = _rand(T[idx])
            if schl is not None and len(schl) == 1:
                break
            Ti = T[idx]
            Ed = np.concatenate((Ti[:, [0, 1]], Ti[:, [1, 2]], Ti[:, [2, 0]]), 0)
            k_ = Ed[:, 0] * 10**7 + Ed[:, 1]
            rv = Ed[:, 1] * 10**7 + Ed[:, 0]
            re_ = ~np.isin(rv, k_)
            aus_ = np.bincount(Ed[re_, 0], minlength=n)
            rk = re_.reshape(3, -1).sum(0)
            schlecht = (aus_[Ti] > 1).any(1) & (rk >= 1) | (rk >= 2)
            if schl is None and schlecht.any():
                idx = idx[~schlecht]
            rr_ = _komponenten(T[idx], n)
            u_, c_ = np.unique(rr_, return_counts=True)
            idx = idx[rr_ == u_[c_.argmax()]]
            if schl is not None:
                vs = set(np.unique(T[idx]).tolist())
                dazu = np.nonzero((gegend == 0) & np.array([all(int(v) in vs for v in t) for t in T]) & ~np.isin(np.arange(len(T)), idx))[0]
                # kleine Loecher mit einem Punkt in der Mitte (Huegel ueber 1,2 cm): den Punkt mit hineinnehmen
                for sl_ in sorted(schl, key=len)[:-1]:
                    if len(sl_) > 16:
                        continue
                    hv = set(int(v) for v in sl_)
                    nicht = ~np.isin(np.arange(len(T)), idx) & (gegend == 0)
                    nah_ = np.nonzero(nicht & (np.isin(T, list(hv)).sum(1) >= 2))[0]
                    spitzen = set(int(v) for t in T[nah_] for v in t) - hv
                    alle_ = hv | spitzen
                    dazu = np.union1d(dazu, np.nonzero(nicht & np.array([all(int(v) in alle_ for v in t) for t in T]))[0])
                idx = np.union1d(idx, dazu)
        schl = _rand(T[idx])
        if _r > 0:
            log("SOHLE %s: Rand aufgeraeumt in %d Runden, Dreiecke %d" % (key, _r, len(idx)))
        assert schl is not None and len(schl) == 1, ("Sohlenrand nicht eine Schleife", key, None if schl is None else [len(s) for s in schl])
        LR = np.array(schl[0])
        plan = ballen_plan(key, K)
        plaene[key] = dict(plan=plan, krallen=K.tolist())
        # Punkte: Rand (bleibt), Ballen-Ringe, Furchen-Raster
        R2 = V[LR, :2]
        innen_pts = []
        for b_ in plan:
            if len(b_) > 6:
                # Vieleck-Ballen: zwei Ringe innen am Rand, innen ein lockeres Raster
                poly = b_[6]
                lo_p, hi_p = poly.min(0), poly.max(0)
                for ein in (0.004, 0.016):
                    ring = []
                    for a_, c_ in zip(poly, np.roll(poly, -1, 0)):
                        ring.append(a_)
                    ring = np.array(ring)
                    # gleichmaessig ueber den Umfang, dann nach innen schieben (Normale aus dem Nachbarn)
                    lang = np.concatenate(([0.0], np.cumsum(np.linalg.norm(np.diff(np.vstack((ring, ring[:1])), axis=0), axis=1))))
                    nn = max(8, int(lang[-1] / (RASTER * 0.6)))
                    tt = np.linspace(0, lang[-1], nn, endpoint=False)
                    ringx = np.interp(tt, lang, np.append(ring[:, 0], ring[0, 0]))
                    ringy = np.interp(tt, lang, np.append(ring[:, 1], ring[0, 1]))
                    R_ = np.c_[ringx, ringy]
                    tg = np.roll(R_, -1, 0) - np.roll(R_, 1, 0)
                    nr = np.c_[tg[:, 1], -tg[:, 0]]
                    nr /= np.maximum(np.linalg.norm(nr, axis=1, keepdims=True), 1e-12)
                    R2_ = R_ + nr * ein
                    if (_poly_sd(R2_, poly) > 0).mean() > 0.5:
                        R2_ = R_ - nr * ein
                    innen_pts.extend([tuple(p) for p in R2_])
                gxp, gyp = np.meshgrid(np.arange(lo_p[0], hi_p[0], RASTER * 1.1), np.arange(lo_p[1], hi_p[1], RASTER * 1.1 * 0.866))
                gxp = gxp + (np.arange(gxp.shape[0])[:, None] % 2) * RASTER * 0.55
                Gp = np.stack((gxp.ravel(), gyp.ravel()), 1)
                Gp = Gp[_poly_sd(Gp, poly) < -0.028]
                innen_pts.extend([tuple(p) for p in Gp])
                continue
            (_n, cx, cy, ax, ay, bieg) = b_
            gross = ax * ay > 0.0012
            for f_, k_ in ((0.0, 1), (0.5, 7 if gross else 5), (0.97, 14 if gross else 9)):
                for j in range(k_):
                    a = 2 * math.pi * j / k_ + (0.3 if f_ == 0.5 else 0.0)
                    dy = f_ * math.sin(a)
                    ex = cx + bieg * (1 - dy * dy) + f_ * ax * math.cos(a)
                    ey = cy + f_ * ay * math.sin(a)
                    if _n == "ferse":
                        t = min(max(-(ex - cx) / ax, 0.0), 1.0)
                        ey = cy + f_ * ay * (1 - 0.30 * t) * math.sin(a)
                    innen_pts.append((ex, ey))
        lo, hi = R2.min(0), R2.max(0)
        gx, gy = np.meshgrid(np.arange(lo[0], hi[0], RASTER), np.arange(lo[1], hi[1], RASTER * 0.866))
        gx = gx + (np.arange(gx.shape[0])[:, None] % 2) * RASTER * 0.5
        G = np.stack((gx.ravel(), gy.ravel()), 1)
        q, _ = ballen_q(plan, G[:, 0], G[:, 1])
        G = G[q > 1.30]
        P_in = np.concatenate((np.array(innen_pts), G), 0)
        # nur Punkte im Rand-Polygon und weit genug vom Rand

        def im_poly(P, poly):
            x_, y_ = P[:, 0], P[:, 1]
            inn = np.zeros(len(P), dtype=bool)
            j = len(poly) - 1
            for i in range(len(poly)):
                xi, yi = poly[i]
                xj, yj = poly[j]
                kreuz = ((yi > y_) != (yj > y_)) & (x_ < (xj - xi) * (y_ - yi) / (yj - yi + 1e-300) + xi)
                inn ^= kreuz
                j = i
            return inn

        def abst_poly(P, poly):
            A_ = poly
            B_ = np.roll(poly, -1, 0)
            d = np.full(len(P), 9.0)
            for a_, b_ in zip(A_, B_):
                ab = b_ - a_
                t = np.clip(((P - a_) @ ab) / max(ab @ ab, 1e-12), 0, 1)
                d = np.minimum(d, np.linalg.norm(P - (a_ + t[:, None] * ab), axis=1))
            return d

        ok = im_poly(P_in, R2) & (abst_poly(P_in, R2) > RAND_FREI)
        P_in = P_in[ok]
        # doppelte/zu nahe Punkte weg
        behalt = []
        for p in P_in:
            if all(np.hypot(*(p - b)) > 0.0045 for b in behalt):
                behalt.append(p)
        P_in = np.array(behalt)
        alle2 = np.concatenate((R2, P_in), 0)
        nr = len(LR)
        kanten = [(i, (i + 1) % nr) for i in range(nr)]
        vo, eo, fo, ov, oe, of = delaunay_2d_cdt([Vector((float(a), float(b))) for a, b in alle2], kanten, [list(range(nr))], 1, 1e-7, True)
        # Zuordnung Ausgabe -> Eingabe (keine neuen Punkte erlaubt)
        karte = []
        for k_, o_ in enumerate(ov):
            assert len(o_) >= 1, ("CDT hat einen Punkt erfunden", key)
            karte.append(min(o_))
        karte = np.array(karte)
        assert len(set(karte.tolist())) == len(karte), ("CDT hat Punkte verschmolzen", key)
        tri = []
        for f in fo:
            assert len(f) == 3
            tri.append([int(karte[i]) for i in f])
        tri = np.array(tri)
        # Ausrichtung: Normale nach unten (im Grundriss im Uhrzeigersinn)
        a2 = alle2[tri]
        flaeche = (a2[:, 1, 0] - a2[:, 0, 0]) * (a2[:, 2, 1] - a2[:, 0, 1]) - (a2[:, 2, 0] - a2[:, 0, 0]) * (a2[:, 1, 1] - a2[:, 0, 1])
        tri[flaeche > 0] = tri[flaeche > 0][:, ::-1]
        # Hoehe: Ballen-Profil, zum Rand hin auf die Randhoehe
        zr = V[LR, 2]
        d_r = abst_poly(P_in, R2)
        # Randhoehe am naechsten Randpunkt
        j_n = np.argmin(((P_in[:, None, :] - R2[None, :, :]) ** 2).sum(-1), 1)
        z_in = hoehe(plan, P_in[:, 0], P_in[:, 1])
        if FIX1 and key[0] == "H":
            # fix1: die (jetzt bis hinten reichende) Sohlenplatte hinter x -0,546 sanft anheben (Ferse rollt ab, 12 % Steigung): mit
            # flachem Ende ging Walk HR an der Ferse 1,3 mm tiefer in den Boden als heute (Bild 13, Ruhe x -0,565)
            z_in = z_in + 0.12 * np.maximum(-0.546 - P_in[:, 0], 0.0) * _sst(-0.546, -0.556, P_in[:, 0])
        rand_w = 1.0 - _sst(0.0, 0.025, d_r - RAND_FREI)
        z_in = z_in * (1 - rand_w) + np.maximum(zr[j_n], z_in) * rand_w
        P3 = np.c_[P_in, z_in]
        glob = np.concatenate((LR, n_neu + np.arange(len(P_in))))
        neue_V.append(P3)
        neue_T.append(glob[tri])
        neue_id.append(np.full(len(tri), pid))
        n_neu += len(P_in)
        weg[idx] = True
        plaene[key].update(rand=LR.tolist(), punkte_neu=len(P_in), dreiecke_alt=int(len(idx)), dreiecke_neu=int(len(tri)),
                           flaeche_m2=float(np.abs(flaeche).sum() / 2), z_rand_max=float(zr.max()))
        log("SOHLE %s: alte Scheibe %d Dreiecke, Rand %d Punkte (z bis %.1f mm), neu %d Punkte, %d Dreiecke, Grundflaeche %.4f m2" % (
            key, len(idx), nr, zr.max() * 1000, len(P_in), len(tri), np.abs(flaeche).sum() / 2))
    V2 = np.concatenate([V] + neue_V, 0)
    T2 = np.concatenate([T[~weg]] + neue_T, 0)
    g2 = np.concatenate([gegend[~weg]] + [np.zeros(len(t), dtype=gegend.dtype) for t in neue_T])
    sid = np.concatenate([np.zeros(int((~weg).sum()), dtype=np.int32)] + [i.astype(np.int32) for i in neue_id])
    # geschlossen und gleich ausgerichtet?
    Ed = np.concatenate((T2[:, [0, 1]], T2[:, [1, 2]], T2[:, [2, 0]]), 0)
    key_ = Ed[:, 0] * 10**7 + Ed[:, 1]
    rev = Ed[:, 1] * 10**7 + Ed[:, 0]
    uk, uc = np.unique(key_, return_counts=True)
    offen = int((~np.isin(rev, key_)).sum())
    log("SOHLEN: Dreiecke %d -> %d, doppelte gerichtete Kanten %d, offene Kanten %d" % (len(T), len(T2), int((uc > 1).sum()), offen))
    assert (uc > 1).sum() == 0 and offen == 0
    return V2, T2, g2, sid, plaene


def sohlenrand_runden(V, T, gegend, sohle, plaene, runden=6, faktor=0.5, schritt_max=0.004):
    """Lauf baer-pfoten: der Sohlenrand (Schleife aus sohlen_bauen) folgt den Dreieckskanten des verringerten Netzes und ist zackig,
    die Kante zur Seitenwand scharf. (1) Die Randschleife wird entlang der Schleife geglaettet (jeder Punkt hoechstens 4 mm, die neuen
    Sohlenpunkte liegen >= 8 mm innen: die eben projizierte Sohlen-UV klappt nicht um); (2) der erste Ring der Seitenwand wird mit festem
    Rand geglaettet (Laplace): die Kante wird runder. Sohlen-Innenpunkte, Kopf und Krallen bleiben; nie unter den Boden."""
    V = np.asarray(V, dtype=np.float64).copy()
    n = len(V)
    fest = np.zeros(n, dtype=bool)
    fest[np.unique(T[gegend != 0])] = True
    sohl_v = np.zeros(n, dtype=bool)
    sohl_v[np.unique(T[sohle > 0])] = True
    bew_r = []
    for key in plaene:
        L = np.array(plaene[key]["rand"], dtype=np.int64)
        P0 = V[L].copy()
        P = P0.copy()
        for _ in range(runden):
            M = 0.5 * (np.roll(P, 1, 0) + np.roll(P, -1, 0))
            P = P + (M - P) * faktor
            d = P - P0
            ln = np.linalg.norm(d, axis=1, keepdims=True)
            P = P0 + d * np.minimum(1.0, schritt_max / np.maximum(ln, 1e-12))
        P[:, 2] = np.maximum(P[:, 2], 0.0)
        V[L] = P
        bew_r.append(np.linalg.norm(P - P0, axis=1))
    rand = set()
    for key in plaene:
        rand |= set(int(i) for i in plaene[key]["rand"])
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    nb = [[] for _ in range(n)]
    for a_, b_ in E:
        nb[a_].append(b_)
        nb[b_].append(a_)
    ring = set()
    for r in rand:
        for j in nb[r]:
            if not sohl_v[j] and not fest[j] and j not in rand:
                ring.add(j)
    ring = np.array(sorted(ring), dtype=np.int64)
    vor = V[ring].copy()
    for _ in range(PF_RAND_RING_RUNDEN):   # Runde 8: der Wandring klappte beim Glaetten um (Knick bis 104 Grad) -> Vorgabe 0 Runden
        M = np.array([V[list(set(nb[i]))].mean(0) for i in ring])
        V[ring] += (M - V[ring]) * faktor
        V[ring, 2] = np.maximum(V[ring, 2], 0.0)
    bew = np.linalg.norm(V[ring] - vor, axis=1) if len(ring) else np.zeros(1)
    bew_r = np.concatenate(bew_r)
    log("SOHLENRAND: Schleifen geglaettet (%d Punkte, Mittel %.1f mm, max %.1f mm), Wandring %d Punkte (Mittel %.1f mm, max %.1f mm)" % (
        len(bew_r), bew_r.mean() * 1000, bew_r.max() * 1000, len(ring), bew.mean() * 1000, bew.max() * 1000))
    return V


def sohle_layout(ob, sohle, plaene):
    """Schreibt NETZ/sohle_layout.json: je Pfote die Ballen (Spielmeter) und die Abbildung Grundriss (x, y) -> UV der Sohlen-Insel
    (affin, kleinste Quadrate ueber die Inselpunkte, Rest in Texeln der 2048er Textur)."""
    me = ob.data
    nl = len(me.loops)
    uv = np.empty(nl * 2, dtype=np.float64)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    lv = np.empty(nl, dtype=np.int64)
    me.loops.foreach_get("vertex_index", lv)
    V_, _T = netz_arrays(me)
    pi = np.empty(nl, dtype=np.int64)
    for p in me.polygons:
        pi[p.loop_start:p.loop_start + p.loop_total] = p.index
    aus = {"einheit": "Spielmeter, Tier-Rahmen (x vorn, y links, z oben); UV wie im FBX/GLB vor der V-Spiegelung (Blender-UV, v nach oben)",
           "ballen_hub_m": BALLEN_HUB, "sohle_dichte": SOHLE_DICHTE,
           "hinweis": "Ballen liegen bei z = 0 auf, Furchen BALLEN_HUB hoeher; Ellipse: ((x - cx - biegung*(1-dy^2))/ax)^2 + dy^2 <= 1 mit dy = (y - cy)/ay; Vieleck (Sohlenplatte hinten, Handballen vorn, Lauf baer-pfoten): q = 1 + Randabstand/vieleck_skala, innen negativ; Hoehe BALLEN_HUB * smoothstep(0.62, 1.22, q). Handwurzelballen (vorn) liegt angehoben ausserhalb des Abdrucks: Lage in spez/pfoten_plan.json",
           "pfoten": {}}
    for pid, key in enumerate(("VL", "VR", "HL", "HR"), start=1):
        if key not in plaene:
            continue
        m = sohle[pi] == pid
        X = np.c_[V_[lv[m], 0], V_[lv[m], 1], np.ones(int(m.sum()))]
        A, *_ = np.linalg.lstsq(X, uv[m], rcond=None)
        rest = np.abs(X @ A - uv[m]).max() * 2048
        lo, hi = uv[m].min(0), uv[m].max(0)
        aus["pfoten"][key] = dict(
            ballen=[(dict(name=b[0], cx=round(b[1], 5), cy=round(b[2], 5), ax=round(b[3], 5), ay=round(b[4], 5), biegung=round(b[5], 5)) if len(b) == 6
                     else dict(name=b[0], cx=round(b[1], 5), cy=round(b[2], 5), vieleck=[[round(float(t), 5) for t in pt] for pt in b[6]],
                               vieleck_skala=VIELECK_SKALA)) for b in plaene[key]["plan"]],
            krallen=[[round(float(t), 4) for t in k] for k in plaene[key]["krallen"]],
            uv_aus_xy=[[round(float(t), 7) for t in r] for r in A.T.tolist()],
            uv_aus_xy_rest_texel_2048=round(float(rest), 2),
            uv_rahmen=[[round(float(t), 5) for t in lo], [round(float(t), 5) for t in hi]],
            dreiecke=plaene[key]["dreiecke_neu"], grundflaeche_m2=round(plaene[key]["flaeche_m2"], 5),
            texel_je_cm2_1024=round(float(abs(np.linalg.det(A[:2, :2])) * 1024 * 1024 / 1e4), 2))
        log("SOHLE %s UV: Abbildung Rest %.2f Texel (2048), Rahmen %s..%s, Texel/cm2 (1024) %.1f" % (
            key, rest, lo.round(3), hi.round(3), aus["pfoten"][key]["texel_je_cm2_1024"]))
    json.dump(aus, open(NETZ + ("sohle_layout.json" if NAME == "pfote" else "sohle_layout_%s.json" % NAME), "w"), indent=1)


def stufe_diagnose():
    """Bilder-Belege: dieselbe Huelle Schritt fuer Schritt, alt gegen neu. Speichert diagnose.blend mit vier Huellen."""
    Q = quelle("form")
    ergebnis = []
    for name, koerper, nr, fp, sg, st, dr, zo in (
        ("A_alt_ohne_zotteln", "baer_koerper", 8, 0.0, 0.0, 16, 4, False),
        ("B_alt_mit_zotteln", "baer_koerper", 8, 0.0, 0.0, 16, 4, True),
        ("C_rundhaut_alt_geschaelt", "baer_koerper_rund", 8, 0.0, 0.0, 16, 4, False),
        ("D_neu_ohne_glaetten", "baer_koerper_rund", NORMAL_RUNDEN, FELL_PLUS, ALPHA_SIGMA, SCHAEL_STUFEN, D_RUNDEN, False),
    ):
        roh, W, T = huelle_bauen(Q, koerper, nr, fp, sg, st, dr, zo)
        bpy.data.objects.remove(roh, do_unlink=True)
        ergebnis.append((name, W, T))
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    from mathutils.kdtree import KDTree
    for name, W, T in ergebnis:
        o = neues_netz(name, h2f(W), T.tolist())
        o.data.shade_smooth()
        # Hubbel: Rest nach Ausgleich durch eine Quadrik (Hoehenfeld im Normalenrahmen) ueber 8 cm Spielmass, an 3000 Rumpfpunkten
        N = v_normalen(W, T)
        Lw = Q["w2l"](W)
        hbw = Q["huelle_basis"](Lw[:, 0], Lw[:, 1], Lw[:, 2])
        kand = np.nonzero((hbw > 0.20) & (W[:, 2] > 0.35))[0]
        wahl = kand[np.random.default_rng(5).choice(len(kand), 3000, replace=False)]
        kd = KDTree(len(W))
        for i, p in enumerate(W):
            kd.insert(p, i)
        kd.balance()
        res = []
        for i in wahl:
            nb = np.array([j for (_, j, _) in kd.find_range(W[i], 0.08 / GROESSE)])
            nb = nb[(N[nb] @ N[i]) > 0.3]
            P_ = W[nb] - W[i]
            t1 = np.cross(N[i], (1, 0, 0) if abs(N[i][0]) < 0.9 else (0, 1, 0))
            t1 /= np.linalg.norm(t1)
            t2 = np.cross(N[i], t1)
            x_, y_, z_ = P_ @ t1, P_ @ t2, P_ @ N[i]
            M_ = np.stack((x_ * x_, x_ * y_, y_ * y_, x_, y_, np.ones_like(x_)), 1)
            c_, *_ = np.linalg.lstsq(M_, z_, rcond=None)
            res.append(abs(c_[5]) * GROESSE)
        res = np.array(res)
        log("DIAG %s: Hubbel (Rest nach Quadrik in 8 cm, Rumpf, Spielmass) Mittel %.1f mm, 90%% %.1f mm, 99%% %.1f mm" % (
            name, res.mean() * 1000, np.percentile(res, 90) * 1000, np.percentile(res, 99) * 1000))
    bpy.ops.wm.save_as_mainfile(filepath=NETZ + "diagnose.blend")
    log("DIAGNOSE_OK")


# ------------------------------------------------------------------ Nachbesserung 1 (fix1): Kegel statt Kragen, Rumpf = baer-fell, Ferse
FIX1_BEINE = {"VL": ((0.0, 0.75), 1.0), "VR": ((0.0, 0.75), -1.0), "HL": ((-0.95, -0.10), 1.0), "HR": ((-0.95, -0.10), -1.0)}


def _fix1_kontur(S, T, h):
    """Schnittpunkte der Kanten mit der Ebene z = h (Spielmeter)."""
    z = S[T][:, :, 2]
    out = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        za, zb = z[:, a], z[:, b]
        m = (za - h) * (zb - h) < 0
        t = (h - za[m]) / (zb[m] - za[m])
        pa, pb = S[T[m, a]], S[T[m, b]]
        out.append(pa + t[:, None] * (pb - pa))
    return np.concatenate(out, 0)


def _fix1_bein(P, xr, s):
    return (P[:, 0] > xr[0]) & (P[:, 0] < xr[1]) & (P[:, 1] * s > 0.0)


def _fix1_radien(K, c, nb=180):
    """Aeusserer Radius je Winkelfach um c (periodisch gefuellt, leicht geglaettet)."""
    th = np.arctan2(K[:, 1] - c[1], K[:, 0] - c[0])
    r = np.hypot(K[:, 0] - c[0], K[:, 1] - c[1])
    b = np.floor((th + math.pi) / (2 * math.pi) * nb).astype(int) % nb
    R = np.full(nb, -1.0)
    np.maximum.at(R, b, r)
    ok = R > 0
    i_ = np.arange(nb)
    R = np.interp(i_, i_[ok], R[ok], period=nb)
    for _ in range(2):
        R = (np.roll(R, 1) + 2.0 * R + np.roll(R, -1)) / 4.0
    return R


def _fix1_r(R, th):
    nb = len(R)
    u = (th + math.pi) / (2 * math.pi) * nb - 0.5
    i0 = np.floor(u).astype(int)
    f = u - i0
    return R[i0 % nb] * (1.0 - f) + R[(i0 + 1) % nb] * f


def fix1_form(W, T, E, n, hbw):
    """Nachbesserung 1 am dichten Netz (Hochmodell-Meter rein/raus, gerechnet in Spielmetern), siehe FIX1 oben."""
    from mathutils.bvhtree import BVHTree
    from mathutils import Vector as _V
    sst = _sst
    S = h2f(W)
    A = np.load(FIX1_ALT)
    SA, TA, TAall = A["V"], A["T"], A["T_alle"]
    z_lo, z_hi = FIX1_KEGEL
    # (a) Kegel: je Bein der Querschnitt bei z_lo (neu) und z_hi (baer-fell); dazwischen radial um eine schraege Achse glatt
    # (smoothstep: unten und oben senkrecht anschliessend, dazwischen ohne Stufe und ohne Ueberhang)
    K_lo_alle = _fix1_kontur(S, T, z_lo)
    K_hi_alle = _fix1_kontur(SA, TAall, min(z_hi, 0.342))   # ueber ~0,345 waechst das Bein in den Bauch (Querschnitt nicht mehr getrennt)
    S0 = S.copy()
    for nm, (xr, s) in FIX1_BEINE.items():
        K_lo = K_lo_alle[_fix1_bein(K_lo_alle, xr, s)]
        K_hi = K_hi_alle[_fix1_bein(K_hi_alle, xr, s)]
        c_lo = 0.5 * (K_lo[:, :2].min(0) + K_lo[:, :2].max(0))
        c_hi = 0.5 * (K_hi[:, :2].min(0) + K_hi[:, :2].max(0))
        R_lo, R_hi = _fix1_radien(K_lo, c_lo), _fix1_radien(K_hi, c_hi)
        bein = _fix1_bein(S0, xr, s)
        m = bein & (S0[:, 2] > z_lo) & (S0[:, 2] < z_hi)
        # Hoehe neu als harmonisches Feld (Rand: z_lo unten, z_hi oben): der alte Saum ist eine nach innen umgeschlagene Falte (zu einer
        # Hoehe gehoeren dort zwei Lagen); mit der eigenen Hoehe fielen beide Lagen auf denselben Radius (Knick). u ist auf dem Netz
        # monoton und klappt die Falte auf.
        reg = bein & (S0[:, 2] > z_lo - 0.03) & (S0[:, 2] < z_hi + 0.03)
        gi = np.nonzero(reg)[0]
        lok = np.full(len(S0), -1)
        lok[gi] = np.arange(len(gi))
        e_ = E[reg[E[:, 0]] & reg[E[:, 1]]]
        a_, b_ = lok[e_[:, 0]], lok[e_[:, 1]]
        cnt = np.bincount(a_, minlength=len(gi)) + np.bincount(b_, minlength=len(gi))
        u_ = S0[gi, 2].copy()
        frei = m[gi] & (cnt > 0)
        for _it in range(1500):
            acc = np.bincount(a_, weights=u_[b_], minlength=len(gi)) + np.bincount(b_, weights=u_[a_], minlength=len(gi))
            u_ = np.where(frei, 0.4 * u_ + 0.6 * acc / np.maximum(cnt, 1), u_)
        uz = S0[:, 2].copy()
        uz[gi] = u_
        t = (uz[m] - z_lo) / (z_hi - z_lo)
        # Profil smoothstep: unten senkrecht aus dem schlanken Gelenk (bis z 0,20 fast unveraendert, sonst wird der Fuss wieder vom Bein
        # geschluckt - Abnahme 'Rist', 'Zehen-Ueberstand', 'Bein z15 - Fuss z3' brachen mit einem frueheren Anlauf ein), oben senkrecht
        # in den baer-fell-Querschnitt; dazwischen monoton, ohne Ueberhang
        f = t * t * (3.0 - 2.0 * t)
        c = c_lo[None, :] + (c_hi - c_lo)[None, :] * f[:, None]   # Achse mit demselben Profil (sonst Kniekehle hinter baer-fell)
        d = S0[m, :2] - c
        r = np.maximum(np.linalg.norm(d, axis=1), 1e-6)
        th = np.arctan2(d[:, 1], d[:, 0])
        r_soll = _fix1_r(R_lo, th) * (1.0 - f) + _fix1_r(R_hi, th) * f
        neu = c + d / r[:, None] * r_soll[:, None]
        w = sst(z_lo, z_lo + 0.012, uz[m])
        S[m, :2] = S0[m, :2] * (1.0 - w[:, None]) + neu * w[:, None]
        S[m, 2] = uz[m]
        bew = np.linalg.norm(S[m, :2] - S0[m, :2], axis=1)
        log("FIX1 Kegel %s: Punkte %d, z %.3f-%.3f, Mitte unten (%.3f %.3f) oben (%.3f %.3f), Radius unten %.3f-%.3f oben %.3f-%.3f, "
            "bewegt Mittel %.1f max %.1f cm" % (nm, int(m.sum()), z_lo, z_hi, c_lo[0], c_lo[1], c_hi[0], c_hi[1], R_lo.min(), R_lo.max(),
                                              R_hi.min(), R_hi.max(), bew.mean() * 100, bew.max() * 100))
    # (b) Rumpf ab FIX1_KLEMM auf die baer-fell-Flaeche (naechster Punkt), am Kopf nicht
    bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in SA], [tuple(map(int, t)) for t in TA])
    # nicht in Kopfnaehe (hbw < 0,20-0,30 Hochmodell-m): dort zieht die Naht den Rumpf ohnehin an den alten Kopf, und der Nahtrand des
    # Kopfes (Taubin mit festem Kopf) soll genau wie in baer-fell bleiben (baer_gewichte_pfote.py prueft die Kopfpunkte auf 1e-6 m)
    wk = sst(FIX1_KLEMM[0], FIX1_KLEMM[1], S[:, 2]) * sst(0.20, 0.30, hbw)
    idx = np.nonzero(wk > 0.0)[0]

    def klemmen(S, runde):
        naechst = np.empty((len(idx), 3))
        for k, i in enumerate(idx):
            naechst[k] = bvh.find_nearest(_V(S[i]))[0]
        dd = np.linalg.norm(naechst - S[idx], axis=1)
        # weiter als 3,5-6 cm von der alten Flaeche (Maul-/Kopfbereich, dort ist die alte Flaeche ausgespart): nicht ziehen
        # nur wo es abweicht (ab 2 mm, voll ab 6 mm): naeher liegende Punkte bleiben, sonst zieht der naechste Punkt in Kehlen
        # (Bein/Bauch) die dichten Punkte auf die Kanten des groben alten Netzes zusammen (umgeklappte Dreiecke)
        wk_i = wk[idx] * (1.0 - sst(0.035, 0.060, dd)) * sst(0.002, 0.006, dd)
        S[idx] += wk_i[:, None] * (naechst - S[idx])
        k_ = int(np.argmax(dd))
        log("FIX1 Rumpf auf baer-fell (%s): Punkte %d (voll %d), Abstand vorher p50 %.2f p95 %.2f max %.2f cm bei (%.3f %.3f %.3f); "
            "ueber 3,5 cm %d Punkte (nicht oder nur teils gezogen)" % (
            runde, len(idx), int((wk_i > 0.999).sum()), np.percentile(dd, 50) * 100, np.percentile(dd, 95) * 100, dd.max() * 100,
            S[idx[k_], 0], S[idx[k_], 1], S[idx[k_], 2], int((dd > 0.035).sum())))
        return S

    S = klemmen(S, "1")
    # (e) Naht oben (Kegel/baer-fell, z 0,29-0,38) und unten (Gelenk, z 0,12-0,20) volumentreu glaetten: dort klappten Dreiecke um
    # (Kegel gegen gezogene Flaeche) bzw. knickte der Anlauf; danach ab FIX1_KLEMM erneut genau auf baer-fell
    beine = np.zeros(len(S), dtype=bool)
    for nm, (xr, s) in FIX1_BEINE.items():
        beine |= _fix1_bein(S, xr, s)
    zz_ = S[:, 2]
    w_n = (sst(0.28, 0.31, zz_) * (1.0 - sst(0.36, 0.385, zz_)) + sst(0.115, 0.13, zz_) * (1.0 - sst(0.18, 0.205, zz_))) * beine
    w_n *= (np.abs(S[:, 1]) > 0.02)
    S = taubin(S, E, len(S), 20, w_n)
    S = klemmen(S, "2")
    # (f) Entwirren: an der Naht Kegel/baer-fell (Beine, z 0,31-0,40) klappten nach dem Ziehen einzelne dichte Dreiecke um; daraus wurden
    # nach dem Verringern Splitter (Pruefer Technik m4: Dehnung bis 46 ohne Kantenfilter). Wenige Runden reines Laplace nur dort
    # (Abweichung von baer-fell danach wenige mm, unter der Grenze 1,5 cm)
    w_e = sst(0.305, 0.32, S[:, 2]) * (1.0 - sst(0.385, 0.40, S[:, 2])) * beine * (np.abs(S[:, 1]) > 0.02)
    S = taubin(S, E, len(S), FIX1_ENTWIRR, w_e, lam=0.5, mu=0.0)
    # (c) Fersen-Hinterkante (Ruhe-z 5-19 cm) bis zur baer-fell-Linie; (d) Ferse unten breiter
    NS = v_normalen(S, T)
    for s in (1.0, -1.0):
        yc = 0.242 * s
        zz = np.arange(0.04, 0.215, 0.01)
        sh = np.zeros(len(zz))
        x_neu = np.zeros(len(zz))
        for k, h in enumerate(zz):
            Kn = _fix1_kontur(S, T, h)
            Ka = _fix1_kontur(SA, TAall, h)
            Kn = Kn[(Kn[:, 0] < -0.40) & (np.abs(Kn[:, 1] - yc) < 0.05)]
            Ka = Ka[(Ka[:, 0] < -0.40) & (np.abs(Ka[:, 1] - yc) < 0.05)]
            x_neu[k] = Kn[:, 0].min()
            sh[k] = min(0.0, Ka[:, 0].min() - Kn[:, 0].min())
        sh = np.maximum(sh, -FIX1_FERSE_DX * 1.5) * (1.0 - sst(0.17, 0.205, zz)) * sst(0.045, 0.07, zz)
        m = (S[:, 0] < -0.45) & (S[:, 1] * s > 0.08) & (S[:, 2] < 0.215)
        xb = np.interp(S[m, 2], zz, x_neu)
        dx = np.interp(S[m, 2], zz, sh) * (1.0 - sst(0.0, 0.045, S[m, 0] - xb)) * sst(-0.20, -0.60, NS[m, 0])
        fb = FIX1_FERSE_BREIT * sst(-0.50, -0.625, S[m, 0]) * (1.0 - sst(0.06, 0.13, S[m, 2]))
        S[m, 0] += dx
        S[m, 1] = yc + (S[m, 1] - yc) * (1.0 + fb)
        log("FIX1 Ferse %s: Verschiebung je z (cm) %s; Breite unten hinten x%.2f; Punkte verschoben %d (max %.2f cm)" % (
            "L" if s > 0 else "R", " ".join("%.0f:%.2f" % (h * 100, v * 100) for h, v in zip(zz, sh)), 1.0 + FIX1_FERSE_BREIT,
            int((np.abs(dx) > 1e-4).sum()), np.abs(dx).max() * 100))
    return f2h(S)


# ==== 2C FORM BEGIN ====
# Lauf baer-2c, Bau Koerper (10.11.2026, SPEZ_2C.md 2 / spez/soll_2c.json A_beine): Form am dichten Netz NACH fix1_form, in Spielmetern
# (Tier-Rahmen x vorn, y links, z oben, Ruhe). Ersetzt fuer Beine, Rumpfseiten und Nacken die fix1-Regel "ueber z 0,36 wie baer-fell".
#   (a) Beine in x: Vorder-/Hinterkante je Hoehe auf die Soll-Tabelle (stueckweise linear zwischen den Kanten wie die Attrappe der
#       Forschung, werkzeug/beine/attrappe.py); Kanten bis z 0,35 am Netz gemessen (freie Beinschleife), darueber gedachte Kanten.
#       Ueber z 0,36-0,44 nur noch an den Beinseiten (Brust-/Bauchmitte bleibt). Hinterkante Schenkel z 0,40-0,45 stetig zum Hintern.
#   (b) Beine innen: Innenkante je Hoehe auf das Soll (bis z 0,30-0,38, zur Mittellinie auf 0).
#   (c) seitlich EIN Feld: |y| > 0,20 wird gestaucht, Faktor je Hoehe aus der Bein-Tabelle (aussen y, z <= 0,40) und je x-Scheibe aus der
#       Rumpf-Soll-Halbbreite (z >= 0,48), dazwischen gemischt -> keine Kastenwand, keine Glocke, Rundung bleibt.
#   (d) Brust zwischen den Vorderbeinen auf ~0,36 heben (weiches Maximum, nur nach unten zeigende Flaeche).
#   (e) Nacken: Ruecken bei x 0,40-0,60 3-4,5 cm tiefer (Buckel x 0,10-0,30 bleibt), oben voll, 30 cm tiefer nichts.
#   (f) Fellbehang als Umriss-Kante: hinter dem Ellbogen 4,5 cm (z 0,36-0,54), Bauchkante 3 cm (x -0,24..0,07).
#   Danach das Verschiebungsfeld ueber das Netz glaetten (fest: Pfoten unter z 0,115, Kopf ab x 0,70 und alles bis 9 cm um die alte
#   Kopfnaht, weich bis 17,5 cm - so bleiben alle Kopfpunkte bit-gleich), Achsel-/Leisten-/Knoechelband glaetten, entwirren.
# BAER_2C_FORM=0 schaltet alles ab.
C2C_FORM = os.environ.get("BAER_2C_FORM", "1") == "1"
C2C_YREF = 0.20
_2C_ZT = np.array([0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80])
_2C_N = len(_2C_ZT)
_2C_BEIN = {
    # Soll aus soll_2c.json A_beine (z 0,12-0,40); darueber nach forschung_beine.md 4.1 und SPEZ 2.1 (aussen <= 0,392-0,400)
    "V": dict(fx=(-0.10, 0.02, 0.52, 0.64), fz=(0.115, 0.14),
              # Runde f6/f13: z 0,20 Hinterkante 0,184 statt 0,190 (Schritt 0,20->0,25 sonst 3,1-3,3 cm > 3,0, SPEZ 2.3; Toleranz 1,5)
              xr_s=[0.230, 0.224, 0.211, 0.184, 0.160, 0.135, 0.115, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100],
              xf_s=[0.418, 0.412, 0.406, 0.405, 0.404, 0.405, 0.408, 0.415, 0.435, 0.465, 0.490, 0.510, 0.510, 0.510, 0.510, 0.510],
              xr_o=[0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100, 0.100],   # gedachte Kanten heute ab z 0,40
              xf_o=[0.500, 0.490, 0.505, 0.510, 0.510, 0.510, 0.510, 0.510, 0.510],
              # Runde f8/f12: Innenkante z 0,30 0,090, z 0,35 0,104 (Glaettung + Achsel-Laplace verschieben ~1 cm; so Schritt vorn 0,30->0,35
              # 2,9 statt 3,9 cm; gemessen 0,111 / 0,093, Soll 0,100 / 0,082 +-1,5)
              yi_s=[0.127, 0.128, 0.128, 0.120, 0.112, 0.090, 0.104, 0.062, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030],
              yi_o=[0.030] * 9,
              yo_s=[0.310, 0.312, 0.318, 0.330, 0.344, 0.358, 0.372, 0.386, 0.392, 0.398, 0.400, 0.400, 0.400, 0.400, 0.400, 0.400],
              yo_o=[0.447, 0.458, 0.465, 0.466, 0.467, 0.467, 0.466, 0.461, 0.461]),
    "H": dict(fx=(-0.84, -0.72, -0.20, -0.06), fz=(0.115, 0.14),
              # Hinterkante: bis z 0,16 macht das Fussfeld (baer_quelle_2c.py), z 0,40-0,45 stetig nach hinten (Spielraum ohne die
              # Sitz-Clips >= 10 cm, log/spielraum_12.txt), ab z 0,50 wie heute (gemessen)
              # Runde f5: Hacke ueber der neuen Ferse ohne Kerbe (heute -0,56 -> -0,60 in 8 cm wirkte als Ring): -0,590 bei z 0,20 (Soll -0,600,
              # Toleranz 1,0 cm), dann wie Soll
              # Runde f6: Schritte <= 3,5 cm je 5 cm (Soll-Tabelle selbst 3,1/3,4): Vorderkante z 0,20-0,35 0,2-0,5 cm vor dem Soll
              xr_s=[None, None, None, -0.594, -0.604, -0.608, -0.611, -0.617, -0.645, None, None, None, None, None, None, None],
              xf_s=[-0.348, -0.370, -0.388, -0.380, -0.362, -0.338, -0.315, -0.288, -0.235, -0.185, -0.160, -0.160, -0.160, -0.160, -0.160, -0.160],
              xr_o=None,
              xf_o=[-0.160, -0.160, -0.160, -0.160, -0.160, -0.160, -0.160, -0.160, -0.160],
              yi_s=[0.151, 0.155, 0.159, 0.146, 0.135, 0.120, 0.100, 0.070, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030],
              yi_o=[0.050, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030, 0.030],
              yo_s=[0.332, 0.335, 0.340, 0.348, 0.361, 0.375, 0.388, 0.398, 0.400, 0.400, 0.405, 0.405, 0.405, 0.405, 0.405, 0.405],
              yo_o=[0.450, 0.452, 0.455, 0.456, 0.457, 0.458, 0.458, 0.458, 0.458]),
}
# Rumpf: Soll-Halbbreite je x (soll_2c.json rumpf_halbe_breite_ruhe, etwas unter dem oberen Rand); Hals x 0,50 0,255-0,29
_2C_RUMPF_X = np.array([-0.80, -0.70, -0.60, -0.50, -0.40, -0.30, -0.20, -0.10, 0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.58, 0.66])
_2C_RUMPF_S = np.array([0.300, 0.345, 0.372, 0.398, 0.398, 0.388, 0.354, 0.340, 0.350, 0.374, 0.388, 0.394, 0.374, 0.300, 0.0, 0.0])   # f7: Hals 0,300 (Kopfnaht fest, sonst Ring)
_2C_NACKEN_X = [0.30, 0.40, 0.50, 0.60, 0.66, 0.72]
_2C_NACKEN_DZ = [0.0, 0.030, 0.045, 0.040, 0.015, 0.0]
_2C_BRUST = dict(x=(0.08, 0.16, 0.48, 0.56), y=(0.07, 0.12), z_ziel=0.36)


def _2c_sst(a, b, x):
    t = np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _2c_schnitt(S, T, h):
    z = S[T][:, :, 2]
    out = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        za, zb = z[:, a], z[:, b]
        m = (za - h) * (zb - h) < 0
        t = (h - za[m]) / (zb[m] - za[m])
        pa, pb = S[T[m, a]], S[T[m, b]]
        out.append(pa + t[:, None] * (pb - pa))
    return np.concatenate(out, 0)


def _2c_fenster(x, f):
    return _2c_sst(f[0], f[1], x) * (1.0 - _2c_sst(f[2], f[3], x))


def _2c_stueck(t, e0, e1, aus0, aus1):
    d = e0 + np.clip(t, 0.0, 1.0) * (e1 - e0)
    d = np.where(t < 0.0, e0 * np.clip(1.0 + t / aus0, 0.0, 1.0), d)
    return np.where(t > 1.0, e1 * np.clip(1.0 - (t - 1.0) / aus1, 0.0, 1.0), d)


_2C_ZF = np.round(np.arange(0.10, 0.8201, 0.005), 4)   # feines Hoehenraster (5 mm), Kanten und Soll darauf geglaettet


def _2c_gauss_z(v, sigma_m):
    """Glaetten entlang des feinen z-Rasters (Gauss, Rand fortgesetzt)."""
    r = int(np.ceil(3 * sigma_m / 0.005))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) * 0.005 / sigma_m) ** 2)
    k /= k.sum()
    return np.convolve(np.r_[np.full(r, v[0]), v, np.full(r, v[-1])], k, "valid")


def _2c_kanten_heute(S, T, bein):
    """Kanten auf dem feinen Raster am Eingangsnetz (beide Seiten, gespiegelt): bis z 0,35 gemessen, darueber die gedachten Kanten
    (_o, Tabelle ab z 0,40); die Hinterkante hinten wird immer gemessen (Hintern). Danach entlang z geglaettet (sigma 1,2 cm)."""
    B = _2C_BEIN[bein]
    xa, xb = (0.0, 0.62) if bein == "V" else (-0.84, -0.08)
    k = {n: np.zeros(len(_2C_ZF)) for n in ("xr", "xf", "yi", "yo")}
    for i, h in enumerate(_2C_ZF):
        K = _2c_schnitt(S, T, max(h, 0.12))
        K = K[(K[:, 0] > xa) & (K[:, 0] < xb) & (np.abs(K[:, 1]) > 0.02)]
        Ka = np.abs(K[:, 1])
        mess = {"xr": K[:, 0].min(), "xf": K[:, 0].max(), "yi": Ka.min(), "yo": Ka.max()}
        for n in k:
            o = B[n + "_o"]
            if h <= 0.351 or o is None:
                k[n][i] = mess[n]
            else:
                k[n][i] = np.interp(h, _2C_ZT[7:], o)
    return {n: _2c_gauss_z(v, 0.012) for n, v in k.items()}


def _2c_soll_fein(werte, heute):
    """Soll-Tabelle (_2C_ZT, None = wie heute) auf das feine Raster, glatt (sigma 1,5 cm)."""
    v = np.array([np.nan if w is None else w for w in werte], dtype=float)
    f = np.interp(_2C_ZF, _2C_ZT[~np.isnan(v)], v[~np.isnan(v)])
    if np.isnan(v).any():
        # None-Stellen: heute (gemessen) - zwischen den Knoten linear auf den Unterschied 0 auslaufen
        d = np.where(np.isnan(v), 0.0, v - np.interp(_2C_ZT, _2C_ZF, heute))
        f = heute + np.interp(_2C_ZF, _2C_ZT, d)
    return _2c_gauss_z(f, 0.015)


def _2c_naht_abstand(P, L):
    """Abstand zur geschlossenen Kopfnaht (Polylinie L, Spielmeter)."""
    A_, B_ = L, np.roll(L, -1, 0)
    d = np.full(len(P), 9.0)
    for a_, b_ in zip(A_, B_):
        ab = b_ - a_
        t_ = np.clip(((P - a_) @ ab) / max(float(ab @ ab), 1e-12), 0.0, 1.0)
        d = np.minimum(d, np.linalg.norm(P - (a_ + t_[:, None] * ab), axis=1))
    return d


def form_2c(S, T, E, kopfnaht=None):
    """Spielmeter rein und raus. Gibt S neu und ein Protokoll-Woerterbuch zurueck. kopfnaht: Punkte der alten Kopfnaht (Spielmeter,
    geschlossene Schleife); bis C2C_KOPF_FEST davon bleibt alles bit-gleich (der Kopf-Nahtrand wird spaeter mit den Rumpfpunkten bis
    7,5 cm geglaettet - nur so bleiben die 1.333 Kopfpunkte wie heute)."""
    sst = _2c_sst
    S0 = S.copy()
    n = len(S)
    x, y, z = S0[:, 0], S0[:, 1], S0[:, 2]
    ay = np.abs(y)
    sg = np.where(y >= 0, 1.0, -1.0)
    prot = {}
    H = {b_: _2c_kanten_heute(S0, T, b_) for b_ in ("V", "H")}
    for b_ in ("V", "H"):
        prot["heute_" + b_] = {k_: np.round(np.interp(_2C_ZT, _2C_ZF, v_), 4).tolist() for k_, v_ in H[b_].items()}
    # (a) Beine in x
    DX = np.zeros(n)
    for bein in ("V", "H"):
        B = _2C_BEIN[bein]
        h = H[bein]
        xr_s, xf_s = _2c_soll_fein(B["xr_s"], h["xr"]), _2c_soll_fein(B["xf_s"], h["xf"])
        xr, xf = np.interp(z, _2C_ZF, h["xr"]), np.interp(z, _2C_ZF, h["xf"])
        er, ef = np.interp(z, _2C_ZF, xr_s) - xr, np.interp(z, _2C_ZF, xf_s) - xf
        t = (x - xr) / np.maximum(xf - xr, 0.02)
        w = _2c_fenster(x, B["fx"]) * sst(B["fz"][0], B["fz"][1], z) * (1.0 - sst(0.70, 0.82, z))
        # ueber z 0,36-0,44 nur an den Beinseiten, Brust-/Bauchmitte bleibt
        w *= 1.0 - sst(0.36, 0.44, z) * (1.0 - sst(0.06, 0.16, ay))
        DX += w * _2c_stueck(t, er, ef, 0.8, 0.8)
    S1 = S0.copy()
    S1[:, 0] += DX
    # (b) Beine innen
    DYi = np.zeros(n)
    for bein in ("V", "H"):
        B = _2C_BEIN[bein]
        h = H[bein]
        yi = np.interp(z, _2C_ZF, h["yi"])
        ei = np.interp(z, _2C_ZF, _2c_soll_fein(B["yi_s"], h["yi"])) - yi
        zfade = (0.32, 0.40) if bein == "V" else (0.36, 0.44)
        w = _2c_fenster(x, B["fx"]) * sst(B["fz"][0], B["fz"][1], z) * (1.0 - sst(zfade[0], zfade[1], z))
        tyi = (ay - yi) / np.maximum(C2C_YREF - yi, 0.02)
        d = np.where(tyi < 0.0, ei * np.clip(ay / np.maximum(yi, 1e-3), 0.0, 1.0), ei * (1.0 - np.clip(tyi, 0.0, 1.0)))
        DYi += w * d * (ay < C2C_YREF)
    # (c) seitlich: |y| > C2C_YREF stauchen; Faktor Bein je z (yo heute -> Soll), Rumpf je x (Halbbreite -> Soll) nur ueber den Beinen
    S1a = np.abs(S1[:, 1])
    f_bein = np.ones(n)
    w_bein = np.zeros(n)
    for bein in ("V", "H"):
        B = _2C_BEIN[bein]
        h = H[bein]
        yo = np.interp(z, _2C_ZF, h["yo"])
        yo_s = np.interp(z, _2C_ZF, _2c_soll_fein(B["yo_s"], h["yo"]))
        cl = np.clip((yo_s - C2C_YREF) / np.maximum(yo - C2C_YREF, 0.02), 0.2, 1.0)
        wb_ = _2c_fenster(x, B["fx"])
        f_bein = np.where(wb_ > w_bein, cl, f_bein)
        w_bein = np.maximum(w_bein, wb_)
    # Rumpf-Halbbreite je x-Band (ueber z 0,45), Faktor geglaettet
    xs = np.arange(-0.82, 0.70, 0.02)
    Bh = np.zeros(len(xs))
    for i, x0 in enumerate(xs):
        m = (np.abs(S1[:, 0] - x0) < 0.015) & (z > 0.45)
        Bh[i] = S1a[m].max() if m.any() else C2C_YREF
    soll = np.interp(xs, _2C_RUMPF_X, _2C_RUMPF_S)
    c_x = np.where(soll > 0.0, np.clip((soll - C2C_YREF) / np.maximum(Bh - C2C_YREF, 1e-3), 0.25, 1.0), 1.0)
    for _ in range(3):
        c_x = np.convolve(np.r_[c_x[0], c_x, c_x[-1]], [0.25, 0.5, 0.25], "valid")
    c_x = np.where(xs > 0.60, 1.0, c_x)
    prot["rumpf_x"] = np.round(xs, 2).tolist()
    prot["rumpf_heute"] = np.round(Bh, 3).tolist()
    prot["rumpf_faktor"] = np.round(c_x, 3).tolist()
    f_rumpf = np.interp(S1[:, 0], xs, c_x)
    f_rumpf = 1.0 - (1.0 - f_rumpf) * (1.0 - sst(0.50, 0.62, S1[:, 0]))
    # unter z 0,30 kein Rumpf-Faktor (dort ist nur Bein); Bein-Faktor bis z 0,38 voll, bis 0,50 ausblenden
    f_rumpf = 1.0 - (1.0 - f_rumpf) * sst(0.28, 0.42, z)
    wl = w_bein * (1.0 - sst(0.38, 0.50, z))
    f = wl * f_bein + (1.0 - wl) * f_rumpf
    aussen = S1a > C2C_YREF
    DYo = np.where(aussen, (C2C_YREF + (S1a - C2C_YREF) * f) - S1a, 0.0)
    S2 = S1.copy()
    S2[:, 1] += sg * (DYi + DYo)
    # (h) baer-gross Bau Netz (SPEZ_GROSS.md 3.5 N2, R2 "kein Rohr"): Taille fuellen. Nur die Aussenflanke (|y| ab 0,22) im Fenster Ruhe
    #     x -0,28..+0,08 (voll -0,22..+0,02), z 0,45-0,95: je x-Scheibe so weit nach aussen, dass die halbe Breite C2C_TAILLE erreicht wird
    #     (nur breiter, nie schmaler; Gesamtbreite bleibt an der Huefte x -0,46). Radial wie (c): Punkte nahe |y| 0,22 bewegen sich kaum,
    #     die breiteste Stelle voll; weich auslaufend in x und z. Bauch-Unterseite (z < 0,45) unberuehrt.
    if C2C_TAILLE > 0:
        S2a = np.abs(S2[:, 1])
        xs_t = np.arange(-0.30, 0.1001, 0.01)   # schmale Scheiben (+-6 mm), sonst misst der Rand der Scheibe die breitere Nachbarschaft mit
        Bt = np.zeros(len(xs_t))
        for i, x0 in enumerate(xs_t):
            m_ = (np.abs(x - x0) < 0.006) & (z > 0.45) & (z < 0.95)
            Bt[i] = S2a[m_].max() if m_.any() else C2C_TAILLE
        dt_ = np.clip(C2C_TAILLE - Bt, 0.0, 0.05)
        for _ in range(4):
            dt_ = np.convolve(np.r_[dt_[0], dt_, dt_[-1]], [0.25, 0.5, 0.25], "valid")
        d_x = np.interp(x, xs_t, dt_) * _2c_fenster(x, (-0.28, -0.22, 0.02, 0.08))
        b_x = np.interp(x, xs_t, Bt)
        wz_t = sst(0.45, 0.58, z) * (1.0 - sst(0.86, 0.96, z))
        DYt = np.where(S2a > 0.22, (S2a - 0.22) * (d_x / np.maximum(b_x - 0.22, 0.03)) * wz_t, 0.0)
        S2[:, 1] += sg * DYt
        prot["taille_x"] = np.round(xs_t, 2).tolist()
        prot["taille_heute"] = np.round(Bt, 4).tolist()
        prot["taille_plus_cm"] = np.round(dt_ * 100, 2).tolist()
        prot["taille_max_cm"] = round(float(DYt.max() * 100), 2)
    # (h2) baer-gross Bau Netz Fortsetzung (R2 Rear "Bauch", 11.11. abends): obere Aussenflanke vor der Huefte fuellen. Im Aufrichten liegt
    #      das Mass "Bauch" (Mitte Huefte-Ellbogen) auf Ruhe x -0,34..-0,22, z 0,70-0,85; dort hatte die Flanke eine Delle (|y| 0,33-0,35
    #      gegen Huefte 0,39 und Taille (h) 0,36) -> von vorn eine Taille ueber den Schenkeln. Je Zelle (x 1 cm, z 2 cm) die halbe Breite auf
    #      das Ziel C2C_FLANKE(x) heben (nur breiter, hoechstens 3,5 cm), ueber z 0,74 sinkt das Ziel (0,5 cm je cm: Querschnitt bleibt
    #      oval, kein Kasten); Punkte ab |y| 0,22, Faktor hoechstens 1. Draufsicht unveraendert (unten, z 0,45-0,60, ist die Scheibe
    #      dort schon breiter). 0 = aus.
    if C2C_FLANKE > 0:
        S2a = np.abs(S2[:, 1])
        xs_f = np.arange(-0.44, -0.0999, 0.01)
        zs_f = np.arange(0.50, 0.9601, 0.02)
        Bf = np.full((len(xs_f), len(zs_f)), np.nan)
        for i, x0 in enumerate(xs_f):
            mx_ = np.abs(x - x0) < 0.006
            for j, z0 in enumerate(zs_f):
                m_ = mx_ & (np.abs(z - z0) < 0.012) & (S2a > 0.15)
                if m_.any():
                    Bf[i, j] = S2a[m_].max()
        for j in range(len(zs_f)):   # Luecken je z-Zeile in x auffuellen
            ok_ = ~np.isnan(Bf[:, j])
            Bf[:, j] = np.interp(xs_f, xs_f[ok_], Bf[ok_, j]) if ok_.any() else 0.5
        T_f = np.interp(xs_f, [-0.40, -0.34, -0.28, -0.22, -0.16], [C2C_FLANKE + 0.020, C2C_FLANKE + 0.012, C2C_FLANKE, C2C_FLANKE - 0.006, C2C_FLANKE - 0.006])
        ziel_ = T_f[:, None] - 0.5 * np.maximum(zs_f[None, :] - 0.74, 0.0)
        df_ = np.clip(ziel_ - Bf, 0.0, 0.035)
        for _ in range(3):   # weich in x und z
            df_ = np.pad(df_, 1, mode="edge")
            df_ = 0.25 * df_[:-2, 1:-1] + 0.5 * df_[1:-1, 1:-1] + 0.25 * df_[2:, 1:-1]
            df_ = np.pad(df_, 1, mode="edge")
            df_ = 0.25 * df_[1:-1, :-2] + 0.5 * df_[1:-1, 1:-1] + 0.25 * df_[1:-1, 2:]
        fx_ = np.clip((x - xs_f[0]) / 0.01, 0, len(xs_f) - 1.0001)
        fz_ = np.clip((z - zs_f[0]) / 0.02, 0, len(zs_f) - 1.0001)
        i0, j0 = fx_.astype(int), fz_.astype(int)
        tx_, tz_ = fx_ - i0, fz_ - j0
        bil = lambda A: ((1 - tx_) * (1 - tz_) * A[i0, j0] + tx_ * (1 - tz_) * A[i0 + 1, j0] + (1 - tx_) * tz_ * A[i0, j0 + 1] + tx_ * tz_ * A[i0 + 1, j0 + 1])
        w_f = _2c_fenster(x, (-0.44, -0.38, -0.20, -0.12)) * sst(0.50, 0.58, z) * (1.0 - sst(0.86, 0.96, z))
        DYf = np.where(S2a > 0.22, np.clip((S2a - 0.22) / np.maximum(bil(Bf) - 0.22, 0.03), 0.0, 1.0) * bil(df_) * w_f, 0.0)
        S2[:, 1] += sg * DYf
        prot["flanke_max_cm"] = round(float(DYf.max() * 100), 2)
        prot["flanke_plus_cm_z0.72"] = np.round(df_[:, list(np.round(zs_f, 2)).index(0.72)] * 100, 2).tolist()
    # (d) Brust zwischen den Vorderbeinen heben: weiches Maximum (Punkte unter z_ziel + 4 cm laufen auf z_ziel zu, darueber nichts)
    Bp = _2C_BRUST
    N0 = v_normalen(S0, T)
    mb = _2c_fenster(x, Bp["x"]) * (1.0 - sst(Bp["y"][0], Bp["y"][1], ay)) * sst(0.0, -0.5, N0[:, 2])
    zz_ = Bp["z_ziel"] + 0.04
    z_neu = np.where(z < zz_, Bp["z_ziel"] + 0.04 * np.exp(np.minimum(z - zz_, 0.0) / 0.04), z)
    DZ = mb * (z_neu - z)
    sel_ = (mb > 0.9)
    prot["brust_z_heute_min"] = round(float(z[sel_].min()), 4) if sel_.any() else None
    # (e) Nacken flacher: oben voll, 30 cm unter dem Ruecken nichts
    xb_ = np.arange(0.20, 0.80, 0.02)
    ztop = np.array([z[(np.abs(x - x0) < 0.015) & (ay < 0.06)].max() if ((np.abs(x - x0) < 0.015) & (ay < 0.06)).any() else 0.9 for x0 in xb_])
    zt = np.interp(x, xb_, ztop)
    dn = np.interp(x, _2C_NACKEN_X, _2C_NACKEN_DZ)
    DZ -= dn * sst(zt - 0.30, zt - 0.02, z)
    # (g) fix1 2c (Pruefbericht M1; Ortung _arbeit/baer_2c/fix1/log/kragen_ort.txt): der Kragen hinter und neben dem Kopf im Sitzen ist
    #     der Buckel (Ruhe x 0,13-0,30, z 1,14-1,16, Spine1), nicht der Nacken x 0,45-0,65. Kamm um C2C_BUCKEL[0] tiefer (Spez-Toleranz
    #     des Buckels 1,5 cm), Flanken (|y| ab 0,08-0,20) um C2C_BUCKEL[1] tiefer: Buckel schmaler, Kamm bleibt. Voll x 0,02-0,28,
    #     aus bei x -0,10 und 0,38 (Nacken x 0,40 unberuehrt); 25 cm unter dem Kamm nichts.
    if C2C_BUCKEL[0] > 0 or C2C_BUCKEL[1] > 0:
        xg_ = np.arange(-0.30, 0.62, 0.02)
        zg_ = np.array([z[(np.abs(x - x0) < 0.015) & (ay < 0.06)].max() if ((np.abs(x - x0) < 0.015) & (ay < 0.06)).any() else 0.9
                        for x0 in xg_])
        zk_ = np.interp(x, xg_, zg_)
        wg_ = sst(-0.10, 0.02, x) * (1.0 - sst(C2C_BUCKEL_AUS[0], C2C_BUCKEL_AUS[1], x))   # baer-gross: Auslauf vorn per BAER_2C_BUCKEL_AUS (2c 0,28-0,38)
        # baer-gross Fortsetzung: die Flanken (|y| ab 0,08) duerfen weiter vorn auslaufen als der Kamm (BAER_2C_BUCKEL_AUS_FL; Kragen "neben dem
        # Kopf" im Sitzen = Schulterdach Ruhe x 0,33-0,36, |y| 0,20); der Kamm (Mittellinie, Nacken x 0,40) bleibt bei C2C_BUCKEL_AUS
        wgf_ = sst(-0.10, 0.02, x) * (1.0 - sst(C2C_BUCKEL_AUS_FL[0], C2C_BUCKEL_AUS_FL[1], x))
        dg_ = (C2C_BUCKEL[0] * sst(zk_ - 0.12, zk_ - 0.01, z) * wg_
               + C2C_BUCKEL[1] * sst(0.08, 0.20, ay) * sst(zk_ - 0.25, zk_ - 0.08, z) * wgf_)
        DZ -= dg_
        prot["buckel_max_cm"] = round(float(dg_.max() * 100), 2)
    S3 = S2.copy()
    S3[:, 2] += DZ
    # (f) Fellbehang als Umriss (SPEZ 2.5, Weg A der Forschung): Kante hinter dem Ellbogen (nach hinten-unten, ueber der freien
    # Beinschleife z 0,34-0,50, damit die Glocke-Regel im Band z 0,12-0,40 haelt) und Bauchkante seitlich (nach unten)
    if C2C_BEHANG[0] > 0 or C2C_BEHANG[1] > 0:
        Nn = v_normalen(S3, T)
        xs3, ys3, zs3 = S3[:, 0], np.abs(S3[:, 1]), S3[:, 2]
        hk = np.interp(zs3, _2C_ZF, _2c_soll_fein(_2C_BEIN["V"]["xr_s"], H["V"]["xr"]))
        ell = (C2C_BEHANG[0] * sst(0.36, 0.43, zs3) * (1.0 - sst(0.48, 0.54, zs3)) * np.exp(-((ys3 - 0.255) / 0.065) ** 2)
               * sst(-0.15, -0.55, Nn[:, 0]) * (1.0 - sst(0.03, 0.09, np.abs(xs3 - hk + 0.01))))
        # Runde f10: Bauchkante erst vor der Kniefalte (x ab -0,24), sonst verbreitert sie das Hinterbein bei z 0,35 um 1,2 cm
        bauch = (C2C_BEHANG[1] * _2c_fenster(xs3, (-0.24, -0.15, -0.01, 0.07)) * np.exp(-((ys3 - 0.255) / 0.06) ** 2)
                 * sst(-0.2, -0.6, Nn[:, 2]) * sst(0.30, 0.36, zs3) * (1.0 - sst(0.52, 0.58, zs3)))
        S3[:, 0] -= ell * 0.85
        S3[:, 2] -= ell * 0.5 + bauch
        prot["behang_ellbogen_max_cm"] = round(float(ell.max() * 100), 2)
        prot["behang_bauch_max_cm"] = round(float(bauch.max() * 100), 2)
    # Verschiebung glaetten (Pfoten und Kopf fest)
    D = S3 - S0
    fest = (z < 0.115) | (x > 0.70)
    w_kopf = np.ones(n)
    if kopfnaht is not None:
        dk = _2c_naht_abstand(S0, np.asarray(kopfnaht, dtype=float))
        fest |= dk < C2C_KOPF_FEST[0]
        w_kopf = _2c_sst(C2C_KOPF_FEST[0], C2C_KOPF_FEST[1], dk)
        D *= w_kopf[:, None]
        prot["kopf_fest_punkte"] = int((dk < C2C_KOPF_FEST[0]).sum())
    D[fest] = 0.0
    for _ in range(C2C_GLATT):
        D = glatt_feld(D, E, n, 1, 0.5)
        D[fest] = 0.0
    S4 = S0 + D
    # Naht Brust/Vorderbein-Innenseite und Kniefalte/Leiste: Lage volumentreu glaetten (dort treffen Innenkante, Brust und Stauchung
    # aufeinander; ohne das bleiben 2-3 cm hohe Spitzen am Achsel-/Leistenrand, Schnittbild form/bild/schnitt_x0.30.png)
    zn = S4[:, 2]
    wn = (_2c_fenster(S4[:, 0], (0.06, 0.12, 0.50, 0.58)) * (1.0 - sst(0.15, 0.20, np.abs(S4[:, 1])))
          * sst(0.27, 0.32, zn) * (1.0 - sst(0.46, 0.52, zn)))
    wn = np.maximum(wn, _2c_fenster(S4[:, 0], (-0.44, -0.36, -0.10, -0.02)) * (1.0 - sst(0.17, 0.22, np.abs(S4[:, 1])))
                    * sst(0.30, 0.35, zn) * (1.0 - sst(0.50, 0.56, zn)))
    wn[fest] = 0.0
    wn *= w_kopf
    S4 = taubin(S4, E, n, C2C_NAHT, wn)
    # Achselrand zwischen den Vorderbeinen (Innenwand trifft die gehobene Brust): reines Laplace (schrumpft die Spitze) im schmalen Band
    wa = (_2c_fenster(S4[:, 0], (0.06, 0.12, 0.50, 0.58)) * _2c_sst(0.02, 0.05, np.abs(S4[:, 1])) * (1.0 - _2c_sst(0.14, 0.18, np.abs(S4[:, 1])))
          * _2c_sst(0.31, 0.35, zn) * (1.0 - _2c_sst(0.43, 0.47, zn)))
    wa[fest] = 0.0
    wa *= w_kopf
    S4 = taubin(S4, E, n, C2C_ACHSEL, wa, lam=0.5, mu=0.0)
    # f16: Hacke/Knoechel-Band z 0,13-0,24 an allen vier Beinen weich (der fix1-Kegel setzt bei z 0,18 mit einem Knick an; von hinten
    # und im Spielwinkel sah das wie ein Ring ueber der Ferse aus, render/f15)
    zr = S4[:, 2]
    wr = sst(0.12, 0.15, zr) * (1.0 - sst(0.22, 0.26, zr)) * sst(0.08, 0.12, np.abs(S4[:, 1]))
    wr[fest] = 0.0
    wr *= w_kopf
    S4 = taubin(S4, E, n, C2C_RING, wr, lam=0.5, mu=0.0)
    # Entwirren: Dreiecke, deren Normale sich um mehr als 75 Grad dreht, samt Nachbarn volumentreu nachglaetten
    n0 = np.cross(S0[T[:, 1]] - S0[T[:, 0]], S0[T[:, 2]] - S0[T[:, 0]])
    for runde in range(3):
        n1 = np.cross(S4[T[:, 1]] - S4[T[:, 0]], S4[T[:, 2]] - S4[T[:, 0]])
        cw = (n0 * n1).sum(1) / np.maximum(np.linalg.norm(n0, axis=1) * np.linalg.norm(n1, axis=1), 1e-18)
        schlecht = cw < 0.26
        prot["umklapper_%d" % runde] = int(schlecht.sum())
        if not schlecht.any():
            break
        wv = np.zeros(n)
        wv[np.unique(T[schlecht])] = 1.0
        wv = np.clip(glatt_feld(wv, E, n, 4, 0.5) * 4.0, 0.0, 1.0)
        wv[fest] = 0.0
        wv *= w_kopf
        S4 = taubin(S4, E, n, 6, wv)
    bew = np.linalg.norm(S4 - S0, axis=1)
    prot["bewegt_max_cm"] = round(float(bew.max() * 100), 2)
    prot["bewegt_p95_cm"] = round(float(np.percentile(bew, 95) * 100), 2)
    prot["bewegt_n_2mm"] = int((bew > 0.002).sum())
    return S4, prot


C2C_GLATT = int(os.environ.get("BAER_2C_GLATT", "25"))
C2C_BEHANG = tuple(float(t) for t in os.environ.get("BAER_2C_BEHANG", "0.045,0.030").split(","))   # Ellbogen, Bauch (m)
C2C_KOPF_FEST = (0.090, 0.175)   # Spielmeter um die alte Kopfnaht: bis 9 cm fest, bis 17,5 cm weich
C2C_BUCKEL = tuple(float(t) for t in os.environ.get("BAER_2C_BUCKEL", "0.043,0.055").split(","))   # fix1 2c: Kamm, Flanken (m), (g); baer-gross N1: Kamm 0,013 -> 0,043, Flanken 0,045 -> 0,055 (Fortsetzung: Kragen neben dem Kopf im Sitzen)
C2C_BUCKEL_AUS = tuple(float(t) for t in os.environ.get("BAER_2C_BUCKEL_AUS", "0.28,0.38").split(","))   # baer-gross: vorderer Auslauf des Buckel-Fensters (m)
C2C_TAILLE = float(os.environ.get("BAER_2C_TAILLE", "0.366"))   # baer-gross N2: Ziel halbe Breite der Taille (m), Schritt (h); 0 = aus
C2C_FLANKE = float(os.environ.get("BAER_2C_FLANKE", "0.380"))   # baer-gross Fortsetzung (h2): Ziel halbe Breite obere Flanke bei Ruhe x -0,28 (m; Bau-Stand bau_n5: 0,380); 0 = aus
C2C_BUCKEL_AUS_FL = tuple(float(t) for t in os.environ.get("BAER_2C_BUCKEL_AUS_FL", "0.32,0.44").split(","))   # baer-gross Fortsetzung: Auslauf vorn der Buckel-Flanken (m)
C2C_NAHT = int(os.environ.get("BAER_2C_NAHT", "25"))
C2C_ACHSEL = int(os.environ.get("BAER_2C_ACHSEL", "30"))
C2C_RING = int(os.environ.get("BAER_2C_RING", "15"))
# ==== 2C FORM END ====


def stufe_netz_anim():
    Q = quelle("form")
    sst = Q["sst"]
    t_start = time.time()
    roh, W, T = huelle_bauen(Q, "baer_koerper_rund", NORMAL_RUNDEN, FELL_PLUS, ALPHA_SIGMA, SCHAEL_STUFEN, D_RUNDEN, False)
    roh.data.vertices.foreach_set("co", W.ravel())
    roh.data.update()
    rm2 = roh.modifiers.new("r2", "REMESH")
    rm2.mode = "VOXEL"
    rm2.voxel_size = PF_VOXEL[1]   # wie baer-fell 9,5 mm
    rm2.adaptivity = 0.0
    bpy.context.view_layer.objects.active = roh
    bpy.ops.object.modifier_apply(modifier=rm2.name)
    W, T = netz_arrays(roh.data)
    E = kanten(T)
    n = len(W)
    # Glaetten und Falten fuellen; Gesicht und Zehen bleiben (Gewicht 0 bzw. wenig)
    Lw = Q["w2l"](W)
    hbw = Q["huelle_basis"](Lw[:, 0], Lw[:, 1], Lw[:, 2])
    zew = Q["pfoten_abstand"](W, "fuss")
    w_glatt = sst(0.07, 0.20, hbw) * (0.10 + 0.90 * sst(0.03, 0.10, zew))
    W = taubin(W, E, n, TAUBIN_RUNDEN, w_glatt)
    # Falten nur am Rumpf fuellen (Achsel, Leiste, Bauchrand); Handgelenk und Ferse bleiben eingezogen, sonst dehnt sich die
    # Haut dort beim Abknicken im Gang staerker (gemessen mit Dump.java)
    W = falten_fuellen(W, T, E, n, FALTEN_RUNDEN, w_glatt * sst(0.30, 0.42, W[:, 2]))
    W = taubin(W, E, n, 6, w_glatt)
    # Stummelschwanz: als Spitze aus dem Fell (die Fellgrenze ist dort eng). Nur dort einfach glaetten, das stumpft ab.
    sa = np.array((-1.06, 0.0, Q["lz"](0.70)))
    sb = np.array((-1.15, 0.0, Q["lz"](0.68)))
    t_ = np.clip(((W - sa) @ (sb - sa)) / ((sb - sa) @ (sb - sa)), 0.0, 1.0)
    d_sw = np.linalg.norm(W - (sa + t_[:, None] * (sb - sa)), axis=1)
    w_sw = 1.0 - sst(0.07, 0.17, d_sw)
    W = taubin(W, E, n, SCHWANZ_RUNDEN, w_sw, lam=0.5, mu=0.0)
    W[:, 2] = np.maximum(W[:, 2], ZMIN_ALT)
    log("Huelle geglaettet", n, "Punkte", len(T), "Dreiecke", "%.1fs" % (time.time() - t_start))
    if FELL:
        W = form_fell(W, T, E, n)
        if ZOTTEL_AMP > 0:
            W = zotteln_fell(W, T)
        W[:, 2] = np.maximum(W[:, 2], ZMIN_ALT)
        if FIX1:
            W = fix1_form(W, T, E, n, hbw)
            W[:, 2] = np.maximum(W[:, 2], ZMIN_ALT)
        if C2C_FORM:
            # 2c: Beine ohne Glocke, Rumpf schmaler, Nacken flacher (form_2c, Spielmeter)
            # alte Kopfnaht (Spielmeter) aus dem alten Netz: dort bleibt die Huelle unveraendert (Kopf-Nahtrand bit-gleich)
            _vorher = set(bpy.data.objects)
            _ob_k, _me_k, _VA_k, _FA_k, _UVA_k, _kr_k = alt_netz()
            _LH_k = rand_schleifen(_FA_k[kopf_inseln(Q, _me_k, _VA_k, _FA_k)])
            assert len(_LH_k) == 1
            naht_2c = _VA_k[np.array(_LH_k[0])].astype(np.float64)
            for _o in list(bpy.data.objects):
                if _o not in _vorher:
                    bpy.data.objects.remove(_o, do_unlink=True)
            bpy.data.meshes.remove(_me_k)
            S0_2c = h2f(W)
            S_2c, prot_2c = form_2c(S0_2c, T, E, naht_2c)
            # Verschiebungsfeld fuer den Textur-Bauer (Hochmodell/Ansichten angleichen): dichte Huelle vorher/nachher, Spielmeter
            np.savez(NETZ + "form2c_feld_%s.npz" % NAME, S0=S0_2c.astype(np.float32), S=S_2c.astype(np.float32), T=T.astype(np.int32))
            for k_, v_ in prot_2c.items():
                log("F2C", k_, v_)
            W = f2h(S_2c)
            W[:, 2] = np.maximum(W[:, 2], ZMIN_ALT)
    if NUR_HUELLE:
        # Lauf baer-pfoten, Form-Runden: dichte Huelle in Spielmetern, ohne Kopfnaht/Verringern/Sohlen/UV
        np.savez(NETZ + "huelle_%s.npz" % NAME, V=h2f(W), T=T)
        log("NUR_HUELLE", NETZ + "huelle_%s.npz" % NAME, len(W), "Punkte", len(T), "Dreiecke")
        return

    # 6. Altes Netz: Kopf und Krallen. In Hochmodell-Massen (f2h), der Kopf wird spaeter genau in Spielmetern zurueckgegeben
    bpy.data.objects.remove(roh, do_unlink=True)
    ob_alt, me_alt, VA, FA, UVA, kralle_a = alt_netz()
    kopf_a = kopf_inseln(Q, me_alt, VA, FA)
    VAh = f2h(VA.astype(np.float64))
    kopf_v = np.unique(FA[kopf_a])
    LH_all = rand_schleifen(FA[kopf_a])
    log("Altes Netz", len(VA), "Punkte", len(FA), "Dreiecke; Kopf", int(kopf_a.sum()), "Krallen", int(kralle_a.sum()), "Kopfrand-Schleifen", [len(s) for s in LH_all])
    assert len(LH_all) == 1, "Kopfnaht ist nicht genau eine Schleife"
    LH = LH_all[0]
    # 7. Naht: Rumpf nahe am Kopf auf die alte Flaeche ziehen (8 cm Band), dann alles weg, was dem alten Kopf am naechsten liegt
    from mathutils.bvhtree import BVHTree
    from mathutils import Vector as _V
    haupt_a = ~kralle_a
    idx_h = np.nonzero(haupt_a)[0]
    bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in VAh], [tuple(map(int, t)) for t in FA[idx_h]])
    naechst = np.empty((n, 3))
    fidx = np.empty(n, dtype=np.int64)
    for i in range(n):
        loc, nrm, k, dist = bvh.find_nearest(_V(W[i]))
        naechst[i] = loc
        fidx[i] = idx_h[k]
    LHp = VAh[LH]
    dl = np.full(n, 9.0)
    for s in range(0, len(LHp), 1):
        dl = np.minimum(dl, np.linalg.norm(W - LHp[s], axis=1))
    band = (1.0 - sst(0.0, NAHT_BAND, dl))
    am_kopf = kopf_a[fidx]
    band = np.where(am_kopf, 1.0, band)
    W = W * (1.0 - band[:, None]) + naechst * band[:, None]
    # Flaechen weg, deren Mitte dem alten Kopf am naechsten liegt oder die naeher als NAHT_LUECKE an der Kopfnaht liegen
    cen = W[T].mean(1)
    weg = np.zeros(len(T), dtype=bool)
    for k in range(len(T)):
        loc, nrm, j, dist = bvh.find_nearest(_V(cen[k]))
        weg[k] = kopf_a[idx_h[j]]
    A_ = LHp
    B_ = np.roll(LHp, -1, 0)
    dseg = np.full(n, 9.0)
    for s_ in range(len(A_)):
        ab = B_[s_] - A_[s_]
        t_ = np.clip(((W - A_[s_]) @ ab) / max(ab @ ab, 1e-12), 0.0, 1.0)
        dseg = np.minimum(dseg, np.linalg.norm(W - (A_[s_] + t_[:, None] * ab), axis=1))
    weg |= (dseg[T] < NAHT_LUECKE).any(1)
    Tb = T[~weg]

    def groesstes(Tx):
        par = np.arange(n)

        def wz(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i

        for t in Tx:
            a_ = wz(t[0])
            par[wz(t[1])] = a_
            par[wz(t[2])] = a_
        rr = np.array([wz(int(t[0])) for t in Tx])
        uu, cc = np.unique(rr, return_counts=True)
        return Tx[rr == uu[cc.argmax()]]

    # Rand aufraeumen: keine Punkte mit zwei Randwegen (Fliege), keine Ohren (Flaeche mit zwei Randkanten)
    for runde in range(40):
        Tb = groesstes(Tb)
        Ed = np.concatenate((Tb[:, [0, 1]], Tb[:, [1, 2]], Tb[:, [2, 0]]), 0)
        key = Ed[:, 0] * 10**7 + Ed[:, 1]
        rev = Ed[:, 1] * 10**7 + Ed[:, 0]
        rand_e = ~np.isin(rev, key)
        aus = np.bincount(Ed[rand_e, 0], minlength=n)
        rk = rand_e.reshape(3, -1).sum(0)
        schlecht = (aus[Tb] > 1).any(1) | (rk >= 2)
        if not schlecht.any():
            break
        Tb = Tb[~schlecht]
    LD_all = rand_schleifen(Tb)
    log("Neuer Rumpf ohne Kopfbereich", len(Tb), "Dreiecke, Randschleifen", [len(s) for s in LD_all], "Aufraeumrunden", runde)
    LD = max(LD_all, key=len)
    assert len(LD_all) == 1, "Rumpfrand ist nicht genau eine Schleife"
    # 8. Zusammensetzen: neuer Rumpf (Punkte 0..n-1), alter Kopf (Punkte n..), Streifen dazwischen
    kmap = np.full(len(VA), -1, dtype=np.int64)
    kmap[kopf_v] = n + np.arange(len(kopf_v))
    P = np.concatenate((W, VAh[kopf_v]), 0)
    LHn = [int(kmap[i]) for i in LH]
    strip = zip_streifen(LHn, [int(i) for i in LD], P)
    Fk = kmap[FA[kopf_a]]
    S = np.array(strip, dtype=np.int64)
    Nn = v_normalen(P, np.concatenate((Tb, Fk), 0))
    ns = np.cross(P[S[:, 1]] - P[S[:, 0]], P[S[:, 2]] - P[S[:, 0]])
    flip = (ns * Nn[S].sum(1)).sum(1) < 0
    Fall = np.concatenate((Tb, S, Fk), 0)
    # Gerichtete Kanten: jede genau einmal (geschlossen und gleich ausgerichtet)
    Ed = np.concatenate((Fall[:, [0, 1]], Fall[:, [1, 2]], Fall[:, [2, 0]]), 0)
    key = Ed[:, 0] * 10**7 + Ed[:, 1]
    ukey, ucnt = np.unique(key, return_counts=True)
    rev = Ed[:, 1] * 10**7 + Ed[:, 0]
    offen = (~np.isin(rev, key)).sum()
    log("Zusammengesetzt: %d Dreiecke (Streifen %d, davon gegen die Nachbarnormale %d); doppelte gerichtete Kanten %d, offene Kanten %d" % (len(Fall), len(S), int(flip.sum()), int((ucnt > 1).sum()), int(offen)))
    assert (ucnt > 1).sum() == 0 and offen == 0
    # 9. Verringern; Kopf und Naht festhalten (Gruppe 'frei': Kopf 0, Rest 1)
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    # Lose Punkte (der weggeschnittene Kopfbereich des neuen Rumpfs) entfernen, Kopfpunkte bleiben am Ende
    benutzt = np.unique(Fall)
    assert (benutzt[-len(kopf_v):] == np.arange(n, n + len(kopf_v))).all()
    neu_i = np.full(len(P), -1, dtype=np.int64)
    neu_i[benutzt] = np.arange(len(benutzt))
    n_r = int((benutzt < n).sum())
    P = P[benutzt]
    Fall = neu_i[Fall]
    n = n_r
    # 8b. Naht weich: Rumpfpunkte bis NAHT_GLATT von der Kopfnaht volumentreu glaetten, der Kopf ist dabei fester Rand.
    # So laeuft der glatte Rumpf ohne Stufe an den alten Kopfrand heran, und der Streifen klappt nicht um.
    LHc = neu_i[np.array(LHn)]
    A_ = P[LHc]
    B_ = np.roll(A_, -1, 0)
    dk = np.full(len(P), 9.0)
    for s_ in range(len(A_)):
        ab = B_[s_] - A_[s_]
        t_ = np.clip(((P - A_[s_]) @ ab) / max(ab @ ab, 1e-12), 0.0, 1.0)
        dk = np.minimum(dk, np.linalg.norm(P - (A_[s_] + t_[:, None] * ab), axis=1))
    wn = np.zeros(len(P))
    wn[:n] = 1.0 - sst(0.0, NAHT_GLATT, dk[:n])
    # Der aeusserste Kopfrand (bis KOPF_NAHT an der Naht, das ist Nackenfell hinter Wange und Ohr) darf mitgehen: sonst bleibt
    # dort der Knick zwischen alter Kopfhuelle und Rumpf stehen. Alles weiter als KOPF_NAHT von der Naht bleibt bit-gleich.
    wn[n:] = 1.0 - sst(0.0, KOPF_NAHT, dk[n:])
    wn[n:][dk[n:] >= KOPF_NAHT] = 0.0
    # Um die Ohren bleibt alles, wie es ist (bis 7 cm Spielmass um die Ohrmitte fest, bis 9 cm weich)
    Lk = Q["w2l"](P[n:])
    d_ohr = np.sqrt((Lk[:, 0] - Q["OHR_C"][0]) ** 2 + (np.abs(Lk[:, 1]) - abs(Q["OHR_C"][1])) ** 2 + (Lk[:, 2] - Q["OHR_C"][2]) ** 2) * Q["KOPF_SK"] * GROESSE
    wn[n:] *= sst(0.07, 0.09, d_ohr)
    P_kopf_vorher = P[n:].copy()
    En = kanten(Fall)
    P = taubin(P, En, len(P), NAHT_RUNDEN, wn)
    bew = np.linalg.norm(P[n:] - P_kopf_vorher, axis=1)
    log("Kopfrand: %d von %d Kopfpunkten bewegt, max %.1f mm (Spielmass), alle innerhalb %.1f cm der Naht" % (
        int((bew > 0).sum()), len(bew), bew.max() * 1000 * GROESSE, float(dk[n:][bew > 0].max() if (bew > 0).any() else 0) * 100 * GROESSE))
    nf = np.cross(P[Fall[:, 1]] - P[Fall[:, 0]], P[Fall[:, 2]] - P[Fall[:, 0]])
    Nv = v_normalen(P, Fall)
    um = (nf * Nv[Fall].sum(1)).sum(1) < 0
    log("Naht geglaettet: %d Punkte im Band, Umklapper danach %d" % (int((wn > 0.01).sum()), int(um.sum())))
    ob = neues_netz("zus", P, Fall.tolist())
    vg = ob.vertex_groups.new(name="frei")
    vg.add(list(range(n)), 1.0, "REPLACE")
    vg.add(list(range(n, len(P))), 0.0, "REPLACE")
    # Merker je Punkt: alte Nummer + 1 fuer Kopfpunkte, 0 sonst (Kopfpunkte werden nicht verschmolzen, behalten also den Wert)
    kn = np.zeros(len(P), dtype=np.float32)
    kn[n:] = kopf_v.astype(np.float32) + 1.0
    ob.data.attributes.new("kopfnr", "FLOAT", "POINT").data.foreach_set("value", kn)
    n_kopf_f = int(kopf_a.sum())
    n_kr = int(kralle_a.sum())
    # Lauf baer-pfoten: in zwei Gaengen verringern. (A) Rumpf ohne Pfoten auf PF_RUMPF_REST, Pfoten und Kopf fest; (B) nur die Pfoten
    # (unter Spiel-z PF_Z_DEZ) auf PF_ZIEL: die Zehen behalten genug Dreiecke (Rillen), der Rest bleibt im Budget (SPEZ 2.5)
    z_pf_h = PF_Z_DEZ / GROESSE + ZMIN_ALT
    pf_v = np.zeros(len(P), dtype=bool)
    pf_v[:n] = P[:n, 2] < z_pf_h
    w_a = np.where(pf_v, 0.0, 1.0)
    w_a[n:] = 0.0
    for o_ in list(ob.vertex_groups):
        ob.vertex_groups.remove(o_)
    vg = ob.vertex_groups.new(name="frei")
    for wert in (0.0, 1.0):
        vg.add([int(i) for i in np.nonzero(w_a == wert)[0]], wert, "REPLACE")
    n_pf_f = int(pf_v[Fall].any(1).sum())
    dm = ob.modifiers.new("wenig", "DECIMATE")
    dm.decimate_type = "COLLAPSE"
    dm.use_collapse_triangulate = True
    dm.vertex_group = "frei"
    dm.vertex_group_factor = 1000.0
    dm.ratio = (PF_RUMPF_REST + n_kopf_f + n_pf_f) / len(Fall)
    dg = bpy.context.evaluated_depsgraph_get()
    me_a = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    Wa_, Ta_ = netz_arrays(me_a)
    kna = np.empty(len(Wa_), dtype=np.float32)
    me_a.attributes["kopfnr"].data.foreach_get("value", kna)
    ob_b = bpy.data.objects.new("zus_b", me_a)
    bpy.context.scene.collection.objects.link(ob_b)
    pfb = (Wa_[:, 2] < z_pf_h) & (kna < 0.5)
    for o_ in list(ob_b.vertex_groups):
        ob_b.vertex_groups.remove(o_)
    vgb = ob_b.vertex_groups.new(name="frei_b")   # die Gruppennamen haengen am Netz: 'frei' traegt noch Gang A
    vgb.add([int(i) for i in np.nonzero(pfb)[0]], 1.0, "REPLACE")
    vgb.add([int(i) for i in np.nonzero(~pfb)[0]], 0.0, "REPLACE")
    n_pf_a = int(pfb[Ta_].any(1).sum())
    dmb = ob_b.modifiers.new("wenig", "DECIMATE")
    dmb.decimate_type = "COLLAPSE"
    dmb.use_collapse_triangulate = True
    dmb.vertex_group = vgb.name
    dmb.vertex_group_factor = 1000.0
    dmb.ratio = (len(Ta_) - n_pf_a + PF_ZIEL) / len(Ta_)
    for o_ in list(bpy.context.view_layer.objects):
        o_.select_set(False)
    bpy.context.view_layer.objects.active = ob_b
    ob_b.select_set(True)
    bpy.ops.object.modifier_apply(modifier=dmb.name)
    me2 = ob_b.data
    W2, T2 = netz_arrays(me2)
    log("PFOTE Verringern: Gang A Rumpf %d -> %d Dreiecke (Pfoten %d fest), Gang B Pfoten %d -> Ziel %d, Netz jetzt %d" % (
        len(Fall) - n_pf_f, len(Ta_) - n_pf_a, n_pf_f, n_pf_a, PF_ZIEL, len(T2)))
    # Kopfpunkte wiederfinden: gleiche Lage
    # Das Netz speichert float32: verglichen wird mit den Kopfpunkten in derselben Genauigkeit
    P32 = P.astype(np.float32)
    kn2 = np.empty(len(W2), dtype=np.float32)
    me2.attributes["kopfnr"].data.foreach_get("value", kn2)
    alt_von = np.full(len(W2), -1, dtype=np.int64)
    W32 = W2.astype(np.float32)
    fest_alt = np.zeros(len(VA), dtype=bool)
    for i in np.nonzero(kn2 > 0.5)[0]:
        j = int(round(float(kn2[i]))) - 1
        if abs(float(kn2[i]) - (j + 1)) < 1e-3:
            alt_von[i] = j
            k_ = n + int(np.searchsorted(kopf_v, j))
            fest_alt[j] = bool((W32[i] == P_kopf_vorher[k_ - n].astype(np.float32)).all())
    assert len(set(alt_von[alt_von >= 0].tolist())) == int((alt_von >= 0).sum()), "Kopfpunkt doppelt"
    gef = set(alt_von[alt_von >= 0].tolist())
    fehl = [i for i in kopf_v if i not in gef]
    if fehl:
        from mathutils.kdtree import KDTree
        kd = KDTree(len(W2))
        for i, p in enumerate(W2):
            kd.insert(p, i)
        kd.balance()
        dd = [kd.find(VAh[i])[2] for i in fehl]
        log("Kopfpunkte nicht wiedergefunden %d, Abstand zum naechsten neuen Punkt max %.6f m" % (len(fehl), max(dd)))
    log("Nach Verringern %d Dreiecke, Kopfpunkte wiedergefunden %d von %d" % (len(T2), int((alt_von >= 0).sum()), len(kopf_v)))
    assert (alt_von >= 0).sum() == len(kopf_v)
    # Kopfflaechen unveraendert?
    kopf_alt_set = set(tuple(sorted(f)) for f in FA[kopf_a].tolist())
    T2a = alt_von[T2]
    ist_kopf = (T2a >= 0).all(1)
    gefunden = set(tuple(sorted(f)) for f in T2a[ist_kopf].tolist())
    log("Kopfflaechen gleich: %d von %d, neue Flaechen nur aus Kopfpunkten %d" % (len(kopf_alt_set & gefunden), len(kopf_alt_set), len(gefunden - kopf_alt_set)))
    assert kopf_alt_set <= gefunden
    ist_kopf = np.array([tuple(sorted(f)) in kopf_alt_set for f in T2a.tolist()]) & ist_kopf
    # 10. In Spielmeter. Kopfpunkte genau wie im alten FBX, der Rest ueber dieselbe Abbildung wie baer_export (x0, zmin alt)
    WF = h2f(W2)
    # Kopfpunkte, die nicht am Rand mitgingen: genau die alten Spielmeter
    ia = np.nonzero(alt_von >= 0)[0]
    ia = ia[fest_alt[alt_von[ia]]]
    WF[ia] = VA[alt_von[ia]].astype(np.float64)
    log("Kopfpunkte genau wie alt: %d, am Rand geglaettet: %d" % (len(ia), int((alt_von >= 0).sum()) - len(ia)))
    nicht_kopf = alt_von < 0
    WF[nicht_kopf, 2] = np.maximum(WF[nicht_kopf, 2], 0.0)
    # UV der Kopfflaechen: aus dem alten Netz (Ecke fuer Ecke ueber die alten Punktnummern)
    uvk = {}
    for fi in np.nonzero(kopf_a)[0]:
        for k in range(3):
            uvk[(int(fi), int(FA[fi, k]))] = UVA[fi, k]
    alt_flaeche = {tuple(sorted(f)): i for i, f in zip(np.nonzero(kopf_a)[0], FA[kopf_a].tolist())}
    # 11. Krallen: alte Schalen unveraendert dazu
    kr_v = np.unique(FA[kralle_a])
    kr_map = np.full(len(VA), -1, dtype=np.int64)
    kr_map[kr_v] = len(WF) + np.arange(len(kr_v))
    Vend = np.concatenate((WF, VA[kr_v].astype(np.float64)), 0)
    Tk = kr_map[FA[kralle_a]]
    # Lauf baer-pfoten, K1: jede vordere Kralle starr in y zur Mittelkralle ihrer Pfote (Teilung 4,6 -> 4,1 cm); hinten bit-gleich
    k1_dy = np.zeros(len(Vend))
    _kr_r = _komponenten(Tk, len(Vend))
    _mitten = {}
    for _r in np.unique(_kr_r):
        _vs = np.unique(Tk[_kr_r == _r])
        _m = Vend[_vs].mean(0)
        if _m[0] > -0.1:
            _mitten.setdefault("L" if _m[1] > 0 else "R", []).append((_r, _vs, _m))
    for _seite, _liste in _mitten.items():
        assert len(_liste) == 5, ("K1: nicht 5 Krallen vorn", _seite, len(_liste))
        _yc = float(np.mean([m_[1] for _r, _vs, m_ in _liste]))
        for _r, _vs, _m in _liste:
            k1_dy[_vs] = (_m[1] - _yc) * K1_FAKTOR
    Vend[:, 1] += k1_dy
    # 2c (SPEZ_2C.md 4): alle zehn Hinterkrallen starr um dx = -0,070 (Form, UV, Gewichte gleich); k2c_dx fuer gewichte/kopfprobe
    k2c_dx = np.zeros(len(Vend))
    for _r in np.unique(_kr_r):
        _vs = np.unique(Tk[_kr_r == _r])
        if Vend[_vs].mean(0)[0] < -0.1:
            k2c_dx[_vs] = C2C_KRALLE_DX
    Vend[:, 0] += k2c_dx
    log("K2C hinten: Krallen verschoben %d Punkte um dx %.3f m" % (int((k2c_dx != 0).sum()), C2C_KRALLE_DX))
    log("K1 vorn: Krallen verschoben %d Punkte, dy je Kralle (cm) %s" % (int((k1_dy != 0).sum()), sorted(set(np.round(k1_dy[k1_dy != 0] * 100, 2).tolist()))))
    Tend = np.concatenate((T2, Tk), 0)
    gegend = np.concatenate((np.where(ist_kopf, 1, 0), np.full(len(Tk), 2)))
    log("Spielnetz neu: %d Punkte, %d Dreiecke (Rumpf %d, Kopf %d, Krallen %d)" % (len(Vend), len(Tend), int((gegend == 0).sum()), int((gegend == 1).sum()), int((gegend == 2).sum())))
    sohle = np.zeros(len(Tend), dtype=np.int32)
    plaene = {}
    n_v_vor_sohle = len(Vend)
    if FELL:
        Vend, Tend, gegend, sohle, plaene = sohlen_bauen(Vend, Tend, gegend)
        if PF_RAND_RUNDEN > 0:
            # Runde 8/9 probiert: Schleife glaetten (4 mm) und Wandring glaetten machten den Randknick nicht kleiner (Mittel 32-39 -> 37-39,
            # max bis 104 Grad, pfote_abnahme.py) -> Vorgabe aus
            Vend = sohlenrand_runden(Vend, Tend, gegend, sohle, plaene, runden=PF_RAND_RUNDEN)
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    ob = neues_netz("NCBear", Vend, Tend.tolist())
    me = ob.data
    me.shade_smooth()
    me.uv_layers.new(name="UVMap")
    uvd = me.uv_layers.active.data
    # Kopf- und Krallen-UV setzen
    alt_uv_kr = {}
    for fi in np.nonzero(kralle_a)[0]:
        for k in range(3):
            alt_uv_kr[(int(kr_map[FA[fi, k]]),)] = None
    kr_flaeche = {tuple(kr_map[FA[fi]].tolist()): fi for fi in np.nonzero(kralle_a)[0]}
    for p in me.polygons:
        g = gegend[p.index]
        if g == 1:
            vv = [int(alt_von[v]) for v in p.vertices]
            fi = alt_flaeche[tuple(sorted(vv))]
            for li, v in zip(p.loop_indices, vv):
                uvd[li].uv = tuple(map(float, uvk[(int(fi), v)]))
        elif g == 2:
            fi = kr_flaeche[tuple(p.vertices)]
            for k, li in enumerate(p.loop_indices):
                uvd[li].uv = tuple(map(float, UVA[fi, k]))
    ga = me.attributes.new("gegend", "INT", "FACE")
    ga.data.foreach_set("value", gegend.astype(np.int32))
    alt_ganz = np.concatenate((alt_von, kr_v))   # je Punkt des neuen Netzes: Nummer im alten FBX oder -1
    alt_ganz = np.concatenate((alt_ganz, np.full(len(Vend) - n_v_vor_sohle, -1, dtype=alt_ganz.dtype)))
    k1_ganz = np.concatenate((k1_dy, np.zeros(len(Vend) - n_v_vor_sohle)))
    k2c_ganz = np.concatenate((k2c_dx, np.zeros(len(Vend) - n_v_vor_sohle)))
    # Punkte der alten Sohlenscheiben, die keine Flaeche mehr tragen, entfernen (Reihenfolge der uebrigen bleibt)
    benutzt = np.zeros(len(Vend), dtype=bool)
    benutzt[np.unique(Tend)] = True
    if not benutzt.all():
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[bm.verts[int(i)] for i in np.nonzero(~benutzt)[0]], context="VERTS")
        bm.to_mesh(me)
        bm.free()
        me.update()
        Vend = Vend[benutzt]
        alt_ganz = alt_ganz[benutzt]
        k1_ganz = k1_ganz[benutzt]
        k2c_ganz = k2c_ganz[benutzt]
        V_chk, _T_chk = netz_arrays(me)
        assert len(V_chk) == len(Vend) and np.abs(V_chk - Vend.astype(np.float32)).max() < 1e-6, "Punktreihenfolge nach dem Aufraeumen anders"
        log("Lose Punkte der alten Sohlen entfernt: %d, Netz jetzt %d Punkte, %d Dreiecke" % (int((~benutzt).sum()), len(Vend), len(me.polygons)))
    sa = me.attributes.new("sohle", "INT", "FACE")
    sa.data.foreach_set("value", sohle.astype(np.int32))
    np.savez(NETZ + "netz_%s.npz" % NAME, alt_von=alt_ganz, gegend=gegend, V=Vend, sohle=sohle, k1_dy=k1_ganz, k2c_dx=k2c_ganz)
    uv_rumpf(Q, ob, gegend, sohle if FELL else None)
    ob["n_haupt"] = int(len(WF))
    if FELL:
        sohle_layout(ob, sohle, plaene)
    bpy.ops.wm.save_as_mainfile(filepath=NETZ + "lowpoly_%s.blend" % NAME)
    log("NETZ_FELL_OK" if FELL else "NETZ_ANIM_OK", "%.1fs" % (time.time() - t_start))


def uv_raster_zaehl(tri, res):
    """Zaehlt je Pixelmitte, wie viele UV-Dreiecke sie decken (streng innen)."""
    c = np.zeros((res, res), dtype=np.int16)
    P_ = tri * res
    for a, b, c3 in P_:
        x0 = max(int(math.floor(min(a[0], b[0], c3[0]))), 0)
        x1 = min(int(math.ceil(max(a[0], b[0], c3[0]))), res - 1)
        y0 = max(int(math.floor(min(a[1], b[1], c3[1]))), 0)
        y1 = min(int(math.ceil(max(a[1], b[1], c3[1]))), res - 1)
        if x1 < x0 or y1 < y0:
            continue
        den = (b[1] - c3[1]) * (a[0] - c3[0]) + (c3[0] - b[0]) * (a[1] - c3[1])
        if abs(den) < 1e-14:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        w0 = ((b[1] - c3[1]) * (X - c3[0]) + (c3[0] - b[0]) * (Y - c3[1])) / den
        w1 = ((c3[1] - a[1]) * (X - c3[0]) + (a[0] - c3[0]) * (Y - c3[1])) / den
        w2 = 1.0 - w0 - w1
        drin = (w0 > 0) & (w1 > 0) & (w2 > 0)
        c[y0:y1 + 1, x0:x1 + 1] += drin.astype(np.int16)
    return c


def dehnen(m, r):
    """Binaere Maske um r Pixel erweitern (Kreisscheibe)."""
    if r <= 0:
        return m.copy()
    out = m.copy()
    H, W = m.shape
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy > r * r + 0.5 or (dx == 0 and dy == 0):
                continue
            ys0, ys1 = max(0, dy), H + min(0, dy)
            xs0, xs1 = max(0, dx), W + min(0, dx)
            out[ys0:ys1, xs0:xs1] |= m[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out


def raster_packen(U, inseln_tri, fest, R, luecke, s):
    """Legt die Inseln (Liste von Dreiecks-Eckenindizes in U) mit Massstab s einzeln in die freie Flaeche: groesste zuerst,
    je Insel vier Drehungen (90 Grad), Platz unten-links (Kreuzkorrelation per FFT). fest: belegte Pixel (schon um die Luecke
    erweitert). Gibt neue UV oder None zurueck, wenn eine Insel nicht passt."""
    belegt = fest.astype(np.float32).copy()
    U2 = U.copy()
    groesse = []
    for tri in inseln_tri:
        P = U[tri]
        groesse.append(0.5 * np.abs((P[:, 1, 0] - P[:, 0, 0]) * (P[:, 2, 1] - P[:, 0, 1]) - (P[:, 2, 0] - P[:, 0, 0]) * (P[:, 1, 1] - P[:, 0, 1])).sum())
    for i in np.argsort(groesse)[::-1]:
        tri = inseln_tri[i]
        li = np.unique(tri)
        P0 = U[li] * s
        bestes = None
        F_bel = np.fft.rfft2(belegt)
        for k in range(4):
            c_, s_ = [(1, 0), (0, 1), (-1, 0), (0, -1)][k]
            P = np.stack((P0[:, 0] * c_ - P0[:, 1] * s_, P0[:, 0] * s_ + P0[:, 1] * c_), 1)
            P = P - P.min(0)
            Ppx = P * R + luecke + 0.5
            mw = int(math.ceil(Ppx[:, 0].max() + luecke + 0.5)) + 1
            mh = int(math.ceil(Ppx[:, 1].max() + luecke + 0.5)) + 1
            if mw >= R or mh >= R:
                continue
            ort = {int(l): j for j, l in enumerate(li)}
            T_ = np.array([[ort[int(x)] for x in t] for t in tri])
            m = uv_raster_zaehl(Ppx[T_] / R, R)[:mh, :mw] > 0
            # Raender: Pixel, die das Dreieck nur streifen, auch belegen
            m = dehnen(m, luecke)
            M = np.zeros((R, R), dtype=np.float32)
            M[:mh, :mw] = m
            C = np.fft.irfft2(F_bel * np.conj(np.fft.rfft2(M)), s=(R, R))
            frei = C[:R - mh, :R - mw] < 0.5
            if not frei.any():
                continue
            yx = np.argwhere(frei)
            j = np.lexsort((yx[:, 1], yx[:, 0]))[0]
            oy, ox = int(yx[j, 0]), int(yx[j, 1])
            if bestes is None or (oy, ox) < (bestes[0], bestes[1]):
                bestes = (oy, ox, k, Ppx, mh, mw, m)
        if bestes is None:
            return None
        oy, ox, k, Ppx, mh, mw, m = bestes
        belegt[oy:oy + mh, ox:ox + mw] = np.maximum(belegt[oy:oy + mh, ox:ox + mw], m.astype(np.float32))
        U2[li] = (Ppx + np.array((ox, oy))) / R
    return U2


def uv_rumpf(Q, ob, gegend, sohle=None):
    """Nur der Rumpf wird neu abgewickelt (wie baer_export Schritt 8); Kopf- und Krallen-Inseln bleiben, wo sie sind (gepinnt),
    die drei Flecken fuer Gaumen, Zunge, Zahn (baer_kampf.py FLECK_*) bleiben frei."""
    me = ob.data
    V3, T3 = netz_arrays(me)
    rumpf = gegend == 0
    # Abwickeln auf einer geglaetteten Kopie (Rumpfpunkte)
    E3 = kanten(T3)
    Vg = glatt_feld(V3, E3, len(V3), 12, 0.6)
    fest = np.zeros(len(V3), dtype=bool)
    fest[np.unique(T3[~rumpf])] = True
    Vg[fest] = V3[fest]
    me.vertices.foreach_set("co", Vg.ravel())
    me.update()
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        f.select = bool(rumpf[f.index])
    bmesh.update_edit_mesh(me)
    bpy.ops.uv.smart_project(angle_limit=math.radians(72), island_margin=0.0, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    bpy.context.tool_settings.use_uv_select_sync = True
    bpy.ops.uv.seams_from_islands(mark_seams=True, mark_sharp=False)
    bm = bmesh.from_edit_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    # Gegend des Rumpfs: 0 Rumpf, 2 Pfote (unter 0,15 m Spielmass wie im Hochmodell 0,15/0,75)
    teil = {}
    for f in bm.faces:
        if not rumpf[f.index]:
            teil[f.index] = -1
        else:
            c3 = f.calc_center_median()
            if sohle is not None and sohle[f.index] > 0:
                teil[f.index] = 6          # Lauf baer-fell: jede Sohle eine eigene Insel
            elif c3.z < 0.15 * GROESSE:
                # Lauf baer-pfoten: Pfote in Fuss vorn (Zehen, Rist) und hinten (Ferse) teilen, sonst wird das Band um den Fuss ein Ring
                # und die Abwicklung klappt um (gemessen: Rumpf doppelt ~1000 Pixel)
                x_gel = 0.32 if c3.x > -0.1 else -0.48
                teil[f.index] = 2 if c3.x >= x_gel else 7
            else:
                # Rumpf in vier Stuecke teilen (links/rechts an der Mittellinie, vorn/hinten bei x = 0): kleinere Inseln passen
                # besser um die festen Kopf-Inseln, die Textur wird dichter (gemessen: eine grosse Rumpf-Insel liess ein Fuenftel frei)
                teil[f.index] = (0 if c3.y >= 0.0 else 3) + (0 if c3.x >= 0.0 else 1) * (4 if c3.y >= 0.0 else 2)
                # Lauf baer-pfoten: das schlanke Bein ist eine Roehre; die Innenseite (zum Bauch) wird eine eigene Insel, sonst ist
                # Schulter + Bein ein Ring und die Abwicklung klappt um (gemessen: Inseln an der Schulter, ~1000 doppelte Pixel)
                if c3.z < 0.34 and abs(c3.y) > 0.10 and abs(c3.y) < (0.23 if c3.x > -0.1 else 0.245):
                    teil[f.index] = 8
    for e in bm.edges:
        if len(e.link_faces) == 2 and teil[e.link_faces[0].index] != teil[e.link_faces[1].index]:
            e.seam = True
    gehoert = {}
    inseln = []
    for f0 in bm.faces:
        if f0.index in gehoert or teil[f0.index] < 0:
            continue
        i = len(inseln)
        gehoert[f0.index] = i
        stapel = [f0]
        menge = []
        while stapel:
            f = stapel.pop()
            menge.append(f)
            for e in f.edges:
                if e.seam:
                    continue
                for g in e.link_faces:
                    if g.index not in gehoert and teil[g.index] >= 0:
                        gehoert[g.index] = i
                        stapel.append(g)
        inseln.append(menge)
    eltern = list(range(len(inseln)))
    insel_teil = [teil[x[0].index] for x in inseln]

    def wurzel(i):
        while eltern[i] != i:
            eltern[i] = eltern[eltern[i]]
            i = eltern[i]
        return i

    groesse = [len(x) for x in inseln]
    naht = [e for e in bm.edges if e.seam and len(e.link_faces) == 2 and all(teil[g.index] >= 0 for g in e.link_faces)]
    MIN_FLAECHEN = 70
    for _runde in range(40):
        zaehl = {}
        for e in naht:
            if not e.seam:
                continue
            a_ = wurzel(gehoert[e.link_faces[0].index])
            b_ = wurzel(gehoert[e.link_faces[1].index])
            if a_ == b_:
                e.seam = False
                continue
            if insel_teil[a_] != insel_teil[b_]:
                continue
            zaehl.setdefault(a_, {}).setdefault(b_, []).append(e)
            zaehl.setdefault(b_, {}).setdefault(a_, []).append(e)
        kleine = sorted([w for w in zaehl if groesse[w] < MIN_FLAECHEN], key=lambda w: groesse[w])
        if not kleine:
            break
        for w in kleine:
            w = wurzel(w)
            if groesse[w] >= MIN_FLAECHEN or w not in zaehl:
                continue
            kand = [(len(es), j) for j, es in zaehl[w].items() if wurzel(j) != w]
            if not kand:
                continue
            kand.sort(reverse=True)
            j = wurzel(kand[0][1])
            if j == w:
                continue
            for e in zaehl[w][kand[0][1]]:
                e.seam = False
            eltern[w] = j
            groesse[j] += groesse[w]
    # Grenze Rumpf/Kopf und Rumpf/Kralle ist immer Naht
    for e in bm.edges:
        if len(e.link_faces) == 2 and (teil[e.link_faces[0].index] < 0) != (teil[e.link_faces[1].index] < 0):
            e.seam = True
    # Lauf baer-fell: jede Sohle genau eine Insel (innen keine Naht, am Sohlenrand immer Naht)
    if sohle is not None:
        for e in bm.edges:
            if len(e.link_faces) == 2:
                sa_, sb_ = sohle[e.link_faces[0].index], sohle[e.link_faces[1].index]
                if sa_ > 0 and sa_ == sb_:
                    e.seam = False
                elif sa_ != sb_:
                    e.seam = True
    bmesh.update_edit_mesh(me)
    bpy.ops.mesh.select_all(action="DESELECT")
    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces:
        f.select = bool(rumpf[f.index])
    bmesh.update_edit_mesh(me)
    bpy.ops.uv.unwrap(method="ANGLE_BASED", fill_holes=True, correct_aspect=True, margin=0.002)
    # Lauf baer-pfoten: Inseln, die sich selbst ueberlappen (Rasterprobe), an ihrer mittleren Hoehe teilen und neu abwickeln
    from bpy_extras import bmesh_utils as _bu0
    for _runde in range(5):
        bm = bmesh.from_edit_mesh(me)
        uvl = bm.loops.layers.uv.active
        bm.faces.ensure_lookup_table()
        schlecht = []
        for insel in _bu0.bmesh_linked_uv_islands(bm, uvl):
            if not all(rumpf[f.index] for f in insel) or (sohle is not None and any(sohle[f.index] > 0 for f in insel)):
                continue
            tri_ = []
            for f in insel:
                pts = [tuple(l[uvl].uv) for l in f.loops]
                for i in range(1, len(pts) - 1):
                    tri_.append((pts[0], pts[i], pts[i + 1]))
            tri_ = np.array(tri_)
            lo_ = tri_.reshape(-1, 2).min(0)
            sp_ = max(float((tri_.reshape(-1, 2).max(0) - lo_).max()), 1e-6)
            if int((uv_raster_zaehl((tri_ - lo_) / sp_ * 0.98 + 0.01, 512) > 1).sum()) > 2:
                schlecht.append(insel)
        if not schlecht:
            break
        for f in bm.faces:
            f.select = False
        for insel in schlecht:
            idx_ = set(f.index for f in insel)
            zz = {f.index: f.calc_center_median().z for f in insel}
            zm = float(np.median(list(zz.values())))
            for f in insel:
                f.select = True
                for e in f.edges:
                    if len(e.link_faces) == 2 and all(g.index in idx_ for g in e.link_faces):
                        if (zz[e.link_faces[0].index] < zm) != (zz[e.link_faces[1].index] < zm):
                            e.seam = True
            log("UV-Teilung Runde %d: Insel mit %d Flaechen an z %.3f geteilt" % (_runde, len(insel), zm))
        bmesh.update_edit_mesh(me)
        bpy.ops.uv.unwrap(method="ANGLE_BASED", fill_holes=True, correct_aspect=True, margin=0.002)
    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces:
        f.select = bool(rumpf[f.index])
    bmesh.update_edit_mesh(me)
    # Lauf baer-fell: Sohlen-Inseln eben von unten projiziert (u = x, v = -y in Spielmetern der ungeglaetteten Punkte). Danach
    # wird jede Insel nur noch gedreht, gleichmaessig skaliert und verschoben: UV = affine Abbildung des Grundrisses (sohle_layout.json)
    if sohle is not None:
        bm = bmesh.from_edit_mesh(me)
        uvl = bm.loops.layers.uv.active
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            if f.index < len(sohle) and sohle[f.index] > 0:
                for l in f.loops:
                    p3 = V3[l.vert.index]
                    l[uvl].uv = (float(p3[0]), float(-p3[1]))
        bmesh.update_edit_mesh(me)
    # Dichte je Teil (Rumpf 1,0, Pfote 1,35 wie baer_export), Kopf/Krallen unberuehrt
    from bpy_extras import bmesh_utils
    bm = bmesh.from_edit_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    alle_inseln = bmesh_utils.bmesh_linked_uv_islands(bm, uvl)
    n_r = 0
    for insel in alle_inseln:
        if not all(rumpf[f.index] for f in insel):
            continue
        n_r += 1
        A3 = sum(f.calc_area() for f in insel)
        Auv = 0.0
        cu = np.zeros(2)
        n_ = 0
        zt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for f in insel:
            pts = [l[uvl].uv.copy() for l in f.loops]
            for i in range(1, len(pts) - 1):
                e1 = pts[i] - pts[0]
                e2 = pts[i + 1] - pts[0]
                Auv += abs(e1.x * e2.y - e1.y * e2.x) * 0.5
            for p_ in pts:
                cu += np.array((p_.x, p_.y))
                n_ += 1
            zt[teil[f.index]] += 1
        cu /= max(n_, 1)
        dichte = 1.35 if zt[2] + zt[7] > zt[0] + zt[3] + zt[4] + zt[5] + zt[8] else 1.0
        if zt[6] > sum(zt[:6]) + zt[7] + zt[8]:
            dichte = SOHLE_DICHTE
        fak = dichte * math.sqrt(A3 / max(Auv, 1e-9)) * 0.05
        for f in insel:
            for l in f.loops:
                u_ = l[uvl].uv
                l[uvl].uv = (cu[0] + (u_.x - cu[0]) * fak, cu[1] + (u_.y - cu[1]) * fak)
    # Lauf baer-pfoten: Selbstueberlappung je Insel (Rasterprobe 1024 in Inselkoordinaten), damit ein Fehlschlag zeigt, wo
    for insel in alle_inseln:
        if not all(rumpf[f.index] for f in insel):
            continue
        tri_ = []
        for f in insel:
            pts = [tuple(l[uvl].uv) for l in f.loops]
            for i in range(1, len(pts) - 1):
                tri_.append((pts[0], pts[i], pts[i + 1]))
        tri_ = np.array(tri_)
        lo_ = tri_.reshape(-1, 2).min(0)
        sp_ = max(float((tri_.reshape(-1, 2).max(0) - lo_).max()), 1e-6)
        c_ = uv_raster_zaehl((tri_ - lo_) / sp_ * 0.98 + 0.01, 512)
        if int((c_ > 1).sum()) > 2:
            cm_ = np.mean([np.array(f.calc_center_median()) for f in insel], 0)
            log("UV-INSEL ueberlappt sich: %d Flaechen, Teil %s, Mitte %s, doppelte Pixel %d (512 je Inselrahmen)" % (
                len(insel), sorted(set(teil[f.index] for f in insel)), np.round(cm_, 3), int((c_ > 1).sum())))
    # Kopf- und Krallen-UV pinnen; Sperrflaechen fuer die drei Flecken als eigene gepinnte Vierecke
    for f in bm.faces:
        if not rumpf[f.index]:
            for l in f.loops:
                l[uvl].pin_uv = True
    n_alt = len(bm.faces)
    sperr = []
    for x0, y0, w_, h_ in SPERR_PACKEN:      # 2c Bau Gebiss: Packen wie Bau Koerper (UV unveraendert)
        vs = [bm.verts.new((9.0 + 0.01 * len(sperr), 0.01 * k, 0.0)) for k in range(4)]
        f = bm.faces.new(vs)
        u0, u1 = (x0 - 8) / 1024.0, (x0 + w_ + 8) / 1024.0
        v0, v1 = 1.0 - (y0 + h_ + 8) / 1024.0, 1.0 - (y0 - 8) / 1024.0
        for l, uvp in zip(f.loops, ((u0, v0), (u1, v0), (u1, v1), (u0, v1))):
            l[uvl].uv = uvp
            l[uvl].pin_uv = True
        sperr.append(f)
    # Ecke oben rechts: ein winziges festes Viereck. Der Packer nimmt als Rahmen nur, was die festen Inseln aufspannen; ohne
    # diese Ecke blieben oben und rechts breite Streifen leer
    vs = [bm.verts.new((9.5, 0.01 * k, 0.0)) for k in range(4)]
    f = bm.faces.new(vs)
    for l, uvp in zip(f.loops, ((0.997, 0.997), (0.999, 0.997), (0.999, 0.999), (0.997, 0.999))):
        l[uvl].uv = uvp
        l[uvl].pin_uv = True
    sperr.append(f)
    bmesh.update_edit_mesh(me)
    # Packen in mehreren Versuchen; genommen wird der mit der groessten Rumpf-Flaeche ohne Ueberlappung (Rasterprobe)
    bpy.ops.object.mode_set(mode="OBJECT")
    nl = len(me.loops)
    uv0 = np.empty(nl * 2, dtype=np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv0)
    pol_rumpf = np.zeros(len(me.polygons), dtype=bool)
    pol_rumpf[:len(rumpf)] = rumpf
    LIp = [list(p.loop_indices) for p in me.polygons]
    bester = None
    rl0 = np.concatenate([LIp[i] for i in np.nonzero(pol_rumpf)[0]])
    for margin, form, dreh, quelle_ in PACK_VERSUCHE:
        U0 = uv0.reshape(-1, 2).copy()
        if quelle_ == "ORIGINAL_AABB":
            # Rumpf-Inseln vorher ueber das ganze Quadrat ziehen: dann ist der Startrahmen 0..1 (sonst nimmt der Packer
            # nur den Rahmen, den die festen Inseln vorgeben, und laesst oben und rechts Streifen frei)
            lo_, hi_ = U0[rl0].min(0), U0[rl0].max(0)
            U0[rl0] = (U0[rl0] - lo_) / np.maximum(hi_ - lo_, 1e-9)
        me.uv_layers.active.data.foreach_set("uv", U0.ravel())
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.select_all(action="SELECT")
        bpy.ops.uv.pack_islands(rotate=True, rotate_method=dreh, scale=True, margin_method="SCALED", margin=margin, shape_method=form,
                                pin=True, pin_method="LOCKED", udim_source=quelle_)
        bpy.ops.object.mode_set(mode="OBJECT")
        uv1 = np.empty(nl * 2, dtype=np.float32)
        me.uv_layers.active.data.foreach_get("uv", uv1)
        U = uv1.reshape(-1, 2).astype(np.float64)
        tr_r, tr_f = [], []
        for pi, li in enumerate(LIp):
            for k in range(1, len(li) - 1):
                (tr_r if pol_rumpf[pi] else tr_f).append((U[li[0]], U[li[k]], U[li[k + 1]]))
        tr_r, tr_f = np.array(tr_r), np.array(tr_f)
        fl = 0.5 * np.abs((tr_r[:, 1, 0] - tr_r[:, 0, 0]) * (tr_r[:, 2, 1] - tr_r[:, 0, 1]) - (tr_r[:, 2, 0] - tr_r[:, 0, 0]) * (tr_r[:, 1, 1] - tr_r[:, 0, 1])).sum()
        c_r = uv_raster_zaehl(tr_r, 1024)
        c_f = uv_raster_zaehl(tr_f, 1024)
        ueb_fest = int(((c_r > 0) & (c_f > 0)).sum())
        ueb_selbst = int((c_r > 1).sum())
        drin = bool((U[np.concatenate([LIp[i] for i in np.nonzero(pol_rumpf)[0]])] >= 0).all() and (U[np.concatenate([LIp[i] for i in np.nonzero(pol_rumpf)[0]])] <= 1).all())
        log("UV-Versuch Rand %.4f %s %s %s: Rumpfflaeche %.4f, Pixel ueber Kopf/Krallen/Flecken %d, Rumpf doppelt %d, in 0..1 %s" % (margin, form, dreh, quelle_, fl, ueb_fest, ueb_selbst, drin))
        if ueb_fest == 0 and ueb_selbst <= 4 and drin and (bester is None or fl > bester[0]):
            bester = (fl, uv1.copy(), margin, form, dreh, quelle_)
    assert bester is not None, "kein UV-Versuch ohne Ueberlappung"
    # Wachsen: die Rumpf-Inseln je um ihre Mitte vergroessern und ohne Skalieren neu packen, solange alles passt
    from bpy_extras import bmesh_utils as _bu
    me.uv_layers.active.data.foreach_set("uv", bester[1])
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    insel_loops = []
    for ins in _bu.bmesh_linked_uv_islands(bm, uvl):
        if all(f.index < len(rumpf) and rumpf[f.index] for f in ins):
            insel_loops.append(np.array([l.index for f in ins for l in f.loops]))
    bpy.ops.object.mode_set(mode="OBJECT")
    for faktor in WACHSEN:
        U0 = bester[1].reshape(-1, 2).copy()
        for li in insel_loops:
            c_ = U0[li].mean(0)
            U0[li] = c_ + (U0[li] - c_) * faktor
        me.uv_layers.active.data.foreach_set("uv", U0.ravel())
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.select_all(action="SELECT")
        bpy.ops.uv.pack_islands(rotate=True, rotate_method=bester[4], scale=False, margin_method="SCALED", margin=bester[2], shape_method=bester[3],
                                pin=True, pin_method="LOCKED", udim_source="CLOSEST_UDIM")
        bpy.ops.object.mode_set(mode="OBJECT")
        uv1 = np.empty(nl * 2, dtype=np.float32)
        me.uv_layers.active.data.foreach_get("uv", uv1)
        U = uv1.reshape(-1, 2).astype(np.float64)
        tr_r, tr_f = [], []
        for pi, li in enumerate(LIp):
            for k in range(1, len(li) - 1):
                (tr_r if pol_rumpf[pi] else tr_f).append((U[li[0]], U[li[k]], U[li[k + 1]]))
        tr_r, tr_f = np.array(tr_r), np.array(tr_f)
        fl = 0.5 * np.abs((tr_r[:, 1, 0] - tr_r[:, 0, 0]) * (tr_r[:, 2, 1] - tr_r[:, 0, 1]) - (tr_r[:, 2, 0] - tr_r[:, 0, 0]) * (tr_r[:, 1, 1] - tr_r[:, 0, 1])).sum()
        c_r = uv_raster_zaehl(tr_r, 1024)
        c_f = uv_raster_zaehl(tr_f, 1024)
        ueb_fest = int(((c_r > 0) & (c_f > 0)).sum())
        ueb_selbst = int((c_r > 1).sum())
        rl = np.concatenate([LIp[i] for i in np.nonzero(pol_rumpf)[0]])
        drin = bool((U[rl] >= 0).all() and (U[rl] <= 1).all())
        ok_ = ueb_fest == 0 and ueb_selbst <= 4 and drin
        log("UV wachsen x%.3f: Rumpfflaeche %.4f, ueber fest %d, doppelt %d, in 0..1 %s -> %s" % (faktor, fl, ueb_fest, ueb_selbst, drin, "ja" if ok_ else "nein"))
        if ok_ and fl > bester[0]:
            bester = (fl, uv1.copy(), bester[2], bester[3], bester[4], bester[5])
        elif not ok_:
            break
    me.uv_layers.active.data.foreach_set("uv", bester[1])
    log("UV genommen: Rand %.4f %s %s %s, Rumpfflaeche %.4f" % (bester[2], bester[3], bester[4], bester[5], bester[0]))
    # Eigenes Raster-Packen in die ganze freie Flaeche (Blender laesst um die festen Inseln Streifen leer): Inseln groesser,
    # solange alle passen. Luecke 3 Pixel der 1024er Textur zu jeder anderen Insel und zu den Flecken.
    U_b = bester[1].reshape(-1, 2).astype(np.float64)
    tri_fest, inseln_tri = [], []
    loop_insel = {}
    for ii, li in enumerate(insel_loops):
        for l_ in li:
            loop_insel[int(l_)] = ii
    inseln_tri = [[] for _ in insel_loops]
    for pi, li in enumerate(LIp):
        for k in range(1, len(li) - 1):
            t3 = (li[0], li[k], li[k + 1])
            if pol_rumpf[pi]:
                inseln_tri[loop_insel[int(li[0])]].append(t3)
            else:
                tri_fest.append(t3)
    inseln_tri = [np.array(t, dtype=np.int64) for t in inseln_tri]
    RP, LU = 1024, 2   # je Seite 2 Pixel: zwischen zwei Inseln mindestens 4 Pixel der 1024er Textur
    fest = uv_raster_zaehl(U_b[np.array(tri_fest)], RP) > 0
    fest = dehnen(fest, LU)
    fest[:LU, :] = True
    fest[-LU:, :] = True
    fest[:, :LU] = True
    fest[:, -LU:] = True
    lo_s, hi_s = 0.8, 1.6
    bestes_U = None
    U_eins = raster_packen(U_b, inseln_tri, fest, RP, LU, lo_s)
    if U_eins is not None:
        bestes_U = (lo_s, U_eins)
        for _ in range(8):
            mitte = 0.5 * (lo_s + hi_s)
            U_t = raster_packen(U_b, inseln_tri, fest, RP, LU, mitte)
            if U_t is None:
                hi_s = mitte
            else:
                lo_s = mitte
                bestes_U = (mitte, U_t)
    if bestes_U is not None:
        U_n = bestes_U[1]
        tr_r = np.concatenate([U_n[t] for t in inseln_tri], 0)
        tr_f = U_n[np.array(tri_fest)]
        c_r = uv_raster_zaehl(tr_r, 2048)
        c_f = uv_raster_zaehl(tr_f, 2048)
        ueb_fest = int(((c_r > 0) & (c_f > 0)).sum())
        ueb_selbst = int((c_r > 1).sum())
        fl = 0.5 * np.abs((tr_r[:, 1, 0] - tr_r[:, 0, 0]) * (tr_r[:, 2, 1] - tr_r[:, 0, 1]) - (tr_r[:, 2, 0] - tr_r[:, 0, 0]) * (tr_r[:, 1, 1] - tr_r[:, 0, 1])).sum()
        drin = bool((tr_r >= 0).all() and (tr_r <= 1).all())
        log("UV Raster-Packen: Massstab x%.3f, Rumpfflaeche %.4f (Blender %.4f), Pixel ueber fest %d, doppelt %d, in 0..1 %s" % (
            bestes_U[0], fl, bester[0], ueb_fest, ueb_selbst, drin))
        if ueb_fest == 0 and ueb_selbst == 0 and drin and fl > bester[0]:
            bester = (fl, U_n.astype(np.float32).ravel(), bester[2], bester[3], bester[4], "RASTER")
            me.uv_layers.active.data.foreach_set("uv", bester[1])
    else:
        log("UV Raster-Packen: passt schon bei x%.2f nicht, Blender-Ergebnis bleibt" % lo_s)
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(me)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    # Sperrflaechen wieder weg (samt Punkten), Pins loesen
    weg_v = set()
    for f in list(bm.faces)[n_alt:]:
        weg_v.update(f.verts)
    bmesh.ops.delete(bm, geom=list(weg_v), context="VERTS")
    for f in bm.faces:
        for l in f.loops:
            l[uvl].pin_uv = False
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode="OBJECT")
    me.vertices.foreach_set("co", V3.ravel())
    me.update()
    uv = np.empty(len(me.loops) * 2, dtype=np.float64)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    log("UV Rumpf-Inseln %d; uv min %s max %s" % (n_r, uv.min(0).round(3), uv.max(0).round(3)))


def stufe_backen_anim():
    """Wie stufe_backen, aber: Netz liegt schon in Spielmetern (Kopf/Krallen genau wie das alte FBX); projiziert wird in
    Hochmodell-Massen (f2h). Kopf- und Krallen-Texel kommen danach unveraendert aus der alten Textur."""
    Q = quelle("form")
    bpy.ops.wm.open_mainfile(filepath=NETZ + "lowpoly_%s.blend" % NAME)
    ob = bpy.data.objects["NCBear"]
    me = ob.data
    VF, T = netz_arrays(me)
    V = f2h(VF)
    m = len(T)
    LT = np.empty(m * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("loops", LT)
    LT = LT.reshape(m, 3)
    PT = np.empty(m, dtype=np.int64)
    me.loop_triangles.foreach_get("polygon_index", PT)
    gegend_p = np.empty(len(me.polygons), dtype=np.int32)
    me.attributes["gegend"].data.foreach_get("value", gegend_p)
    gegend = gegend_p[PT]
    uv = np.empty(len(me.loops) * 2, dtype=np.float64)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    E = kanten(T)
    Vg = glatt_feld(V, E, len(V), 8, 0.6)
    N = v_normalen(Vg, T)
    t0 = time.time()
    pos, nrm, tri = raster_uv(uv[LT], T, V, N, TEX)
    maske = tri >= 0
    log("UV gerastert", "%.1fs" % (time.time() - t0), "Texel", int(maske.sum()), "Anteil %.3f" % maske.mean())
    P = pos[maske].astype(np.float64)
    Nn = nrm[maske].astype(np.float64)
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-9)
    n_t = len(P)
    sum_c = np.zeros((n_t, 3), dtype=np.float32)
    sum_w = np.zeros(n_t, dtype=np.float32)
    views = json.load(open(ANS + "kameras.json"))
    L_ = Q["w2l"](P)
    kopf_maske = 1.0 - Q["sst"](0.02, 0.20, Q["huelle_basis"](L_[:, 0], L_[:, 1], L_[:, 2]))
    for v in views:
        av = Ansicht(v)
        kopf = av.name.startswith("h_")
        Z = minfilter(zbuffer(av, V, T, 1024))
        rgba = lade_exr(ANS + v["name"] + ".exr")
        u, vv, dep = av.pix(P)
        k = 1024.0 / av.res
        iu = np.clip(np.floor(u * k).astype(np.int64), 0, 1023)
        iv = np.clip(np.floor(vv * k).astype(np.int64), 0, 1023)
        tol = 0.014 if kopf else 0.030
        sicht = dep <= Z[iv, iu] + tol
        cs = np.clip(Nn @ av.d, 0.0, 1.0)
        w = cs ** 7
        if kopf:
            w = w * kopf_maske
        w[cs < 0.2] = 0.0
        w[~sicht] = 0.0
        idx = np.nonzero(w > 1e-5)[0]
        if len(idx):
            col, inn = bilinear(rgba, u[idx], vv[idx])
            al = col[:, 3]
            g = w[idx] * inn * (al > 0.45) * al * al
            if kopf:
                g *= 7.0
            c = col[:, :3] / np.maximum(al, 1e-3)[:, None]
            sum_c[idx] += (c * g[:, None]).astype(np.float32)
            sum_w[idx] += g.astype(np.float32)
    gesehen = sum_w > 1e-5
    log("Projektion fertig, gesehen %.4f der Texel" % gesehen.mean())
    lin = np.zeros_like(sum_c)
    lin[gesehen] = sum_c[gesehen] / sum_w[gesehen][:, None]
    S = srgb(lin)
    S = np.power(np.clip(S, 0.0, 1.0), GAMMA) * HELL
    kralle = (gegend == 2)[tri[maske]].astype(np.float64)
    S = gesicht_nacharbeit(Q, S, P, kralle)
    S = np.clip(S, 0.0, 1.0)
    col = np.zeros((TEX, TEX, 3), dtype=np.float32)
    frei = np.ones((TEX, TEX), dtype=bool)
    my, mx = np.nonzero(maske)
    col[my[gesehen], mx[gesehen]] = S[gesehen].astype(np.float32)
    frei[my[gesehen], mx[gesehen]] = False
    r = fuellen(col, frei, maske, 400)
    rest = int((frei & maske).sum())
    log("Innen gefuellt", r, "Runden; Rest", rest)
    if rest:
        col[frei & maske] = S[gesehen].mean(0)
        frei[frei & maske] = False
    alle = np.ones_like(maske)
    fuellen(col, frei, alle, 14)
    col[frei] = S[gesehen].mean(0)
    L_2 = Q["w2l"](P)
    ring_k = Q["sst"](0.15, -0.05, L_2[:, 0]) * (1.0 - Q["sst"](0.015, 0.11, Q["huelle_basis"](L_2[:, 0], L_2[:, 1], L_2[:, 2])))
    kmap = np.full((TEX, TEX), 0.85, dtype=np.float32)
    kmap[my, mx] = (0.85 * (1.0 - 0.9 * ring_k)).astype(np.float32)
    col = unscharf(col, kmap)
    # Kopf und Krallen: Texel aus der alten Textur (gleiche UV), mit 6 px Rand, nie ueber eine Rumpf-Insel
    alt = bpy.data.images.load(ALT_PNG)
    alt.colorspace_settings.name = "Non-Color"
    assert tuple(alt.size) == (TEX, TEX)
    A = np.empty(TEX * TEX * 4, dtype=np.float32)
    alt.pixels.foreach_get(A)
    A = A.reshape(TEX, TEX, 4)[..., :3]
    behalte = maske & (gegend[np.maximum(tri, 0)] != 0)
    rumpf_m = maske & (gegend[np.maximum(tri, 0)] == 0)
    rand = behalte.copy()
    for _ in range(6):
        g = rand.copy()
        g[1:] |= rand[:-1]
        g[:-1] |= rand[1:]
        g[:, 1:] |= rand[:, :-1]
        g[:, :-1] |= rand[:, 1:]
        rand = g
    rumpf_d = rumpf_m.copy()
    for _ in range(2):
        g = rumpf_d.copy()
        g[1:] |= rumpf_d[:-1]
        g[:-1] |= rumpf_d[1:]
        g[:, 1:] |= rumpf_d[:, :-1]
        g[:, :-1] |= rumpf_d[:, 1:]
        rumpf_d = g
    setzen = rand & ~rumpf_d
    col[setzen] = A[setzen]
    ueber = int((behalte & rumpf_m).sum())
    log("Alte Texel fuer Kopf und Krallen: %d (Inselflaeche %d), Ueberlappung mit Rumpf-Inseln %d" % (int(setzen.sum()), int(behalte.sum()), ueber))
    # Flecken fuer Gaumen, Zunge, Zahn: keine Insel darf hinein (baer_kampf.py malt dort)
    for x0, y0, w_, h_ in SPERR_FLECKEN:
        ys = slice(TEX - 2 * (y0 + h_), TEX - 2 * y0)
        xs = slice(2 * x0, 2 * (x0 + w_))
        log("Fleck", (x0, y0, w_, h_), "Inseltexel darin", int(maske[ys, xs].sum()))
        assert int(maske[ys, xs].sum()) == 0
    log("Textur Mittel sRGB", (col[maske].mean(0) * 255).round(1))
    img = bpy.data.images.new("NCBear", TEX, TEX, alpha=False)
    rgba = np.ones((TEX, TEX, 4), dtype=np.float32)
    rgba[..., :3] = col
    img.pixels.foreach_set(rgba.ravel())
    os.makedirs(MOD + "textures/WorldItems", exist_ok=True)
    os.makedirs(MOD + "models_X/WorldItems", exist_ok=True)
    img.filepath_raw = MOD + "textures/WorldItems/NCBear.png"
    img.file_format = "PNG"
    img.save()
    log("Textur gespeichert")
    me.materials.clear()
    mat = bpy.data.materials.new("NCBear")
    mat.use_nodes = True
    br = mat.node_tree.nodes["Principled BSDF"]
    tn = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tn.image = img
    mat.node_tree.links.new(tn.outputs["Color"], br.inputs["Base Color"])
    br.inputs["Roughness"].default_value = 1.0
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True
    for _a in ("gegend", "sohle"):
        if _a in me.attributes:
            me.attributes.remove(me.attributes[_a])
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    log("MASSE Meter: Laenge %.3f Breite %.3f Hoehe %.3f; Dreiecke %d" % (VF[:, 0].max() - VF[:, 0].min(), VF[:, 1].max() - VF[:, 1].min(), VF[:, 2].max(), m))
    log("x von %.3f bis %.3f, z von %.4f" % (VF[:, 0].min(), VF[:, 0].max(), VF[:, 2].min()))
    bpy.ops.export_scene.fbx(filepath=MOD + "models_X/WorldItems/NCBear.fbx", use_selection=True, apply_unit_scale=True,
                             apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_anim=False,
                             mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False)
    bpy.ops.wm.save_as_mainfile(filepath=NETZ + "spielmodell_%s.blend" % NAME)
    log("BACKEN_ANIM_OK")


def stufe_kopfprobe():
    """Liest das alte und das neue FBX zurueck. Kopf und Krallen: welche Punkte bit-gleich sind, wie weit die anderen von der
    Kopfnaht liegen und wie weit sie sich bewegt haben; Flaechen und UV gleich."""
    from mathutils.kdtree import KDTree

    def lies(pfad):
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.ops.import_scene.fbx(filepath=pfad, use_custom_normals=False, use_image_search=False)
        ob = [o for o in bpy.context.selected_objects if o.type == "MESH"][0]
        me = ob.data
        V = np.empty(len(me.vertices) * 3, dtype=np.float32)
        me.vertices.foreach_get("co", V)
        F = [tuple(p.vertices) for p in me.polygons]
        uv = np.empty(len(me.loops) * 2, dtype=np.float32)
        me.uv_layers.active.data.foreach_get("uv", uv)
        LI = [tuple(p.loop_indices) for p in me.polygons]
        return V.reshape(-1, 3), F, uv.reshape(-1, 2), LI

    VA, FA, UA, LA = lies(ALT_FBX)
    VN, FN, UN, LN = lies(os.environ.get("BAER_FELL_FBX", MOD_FELL + "models_X/WorldItems/NCBear.fbx"))
    Q = quelle("form")
    ob_alt, me_alt, VA2, FA2, UVA2, kralle_a = alt_netz()
    kopf_a = kopf_inseln(Q, me_alt, VA2, FA2)
    LH = rand_schleifen(FA2[kopf_a])[0]
    neu = {tuple(p.tolist()): i for i, p in enumerate(VN)}
    kd = KDTree(len(VN))
    for i, p in enumerate(VN):
        kd.insert(p, i)
    kd.balance()
    for name, maske in (("Krallen", kralle_a), ("Kopf", kopf_a)):
        idx = np.unique(FA2[maske])
        gleich = np.array([tuple(VA[i].tolist()) in neu for i in idx])
        d_neu = np.array([kd.find(VA[i])[2] for i in idx])
        A_ = VA[LH].astype(np.float64)
        B_ = np.roll(A_, -1, 0)
        dn = np.full(len(idx), 9.0)
        P_ = VA[idx].astype(np.float64)
        for s_ in range(len(A_)):
            ab = B_[s_] - A_[s_]
            t_ = np.clip(((P_ - A_[s_]) @ ab) / max(ab @ ab, 1e-12), 0.0, 1.0)
            dn = np.minimum(dn, np.linalg.norm(P_ - (A_[s_] + t_[:, None] * ab), axis=1))
        log("KOPFPROBE %s: Punkte %d, bit-gleich %d, verschoben %d" % (name, len(idx), int(gleich.sum()), int((~gleich).sum())))
        if (~gleich).any():
            log("KOPFPROBE %s verschoben: Abstand zur Naht max %.1f cm (Spielmass); Verschiebung Mittel %.1f mm, max %.1f mm; naechster bit-gleicher Punkt %.1f cm von der Naht" % (
                name, dn[~gleich].max() * 100, d_neu[~gleich].mean() * 1000, d_neu[~gleich].max() * 1000, (dn[gleich].min() * 100 if gleich.any() else -1.0)))   # 2c: alle Krallen verschoben (vorn K1, hinten -0,070)
            # Abstand der verschobenen Punkte zu Ohr, Auge, Nase, Mundwinkel (Kopfrahmen des Hochmodells, Spielmeter)
            L_ = Q["w2l"](f2h(P_[~gleich]))
            a_, B_, c_ = L_[:, 0], np.abs(L_[:, 1]), L_[:, 2]
            sk = Q["KOPF_SK"] * GROESSE
            for wo, p in (("Ohr", Q["OHR_C"]), ("Auge", Q["AUGE"]), ("Nase", Q["NASE_C"])):
                dd = np.sqrt((a_ - p[0]) ** 2 + (B_ - abs(p[1])) ** 2 + (c_ - p[2]) ** 2) * sk
                log("KOPFPROBE %s verschoben: naechster Punkt zur Mitte %s %.1f cm" % (name, wo, dd.min() * 100))
            d_ohr = np.sqrt((a_ - Q["OHR_C"][0]) ** 2 + (B_ - abs(Q["OHR_C"][1])) ** 2 + (c_ - Q["OHR_C"][2]) ** 2) * sk
            nah_ohr = d_ohr < 0.07
            log("KOPFPROBE %s verschoben und naeher als 7 cm an der Ohrmitte: %d Punkte, Verschiebung max %.1f mm" % (
                name, int(nah_ohr.sum()), (d_neu[~gleich][nah_ohr].max() * 1000) if nah_ohr.any() else 0.0))
            R_ = Q["regionen"](L_[:, 0], L_[:, 1], L_[:, 2])
            log("KOPFPROBE %s verschoben: Anteil Ohr max %.3f, Auge max %.3f, Schnauze max %.3f (0 = nicht darin)" % (name, R_["ohr"].max(), R_["aug"].max(), R_["schn"].max()))
    fl = {}
    for f, li in zip(FN, LN):
        fl[tuple(sorted(f))] = {v: tuple(UN[l].tolist()) for v, l in zip(f, li)}
    # Flaechen ueber die Zuordnung aus der Netz-Stufe vergleichen (Punktreihenfolge im FBX wie im Netz, geprueft), UV Ecke fuer Ecke
    Z = np.load(NETZ + "netz_%s.npz" % NAME)
    assert len(Z["V"]) == len(VN) and np.abs(Z["V"].astype(np.float32) - VN).max() == 0.0
    zu = {int(a_): i for i, a_ in enumerate(Z["alt_von"]) if a_ >= 0}
    ok = 0
    uvabw = 0.0
    for fi in np.nonzero(kopf_a | kralle_a)[0]:
        f = FA[fi]
        key = tuple(sorted(zu[v] for v in f))
        if key in fl:
            ok += 1
            for v, l in zip(f, LA[fi]):
                uvabw = max(uvabw, float(np.abs(np.array(fl[key][zu[v]]) - UA[l]).max()))
    log("KOPFPROBE Flaechen Kopf+Krallen alt %d, gleich wiedergefunden %d; UV-Abweichung max %.3g" % (int((kopf_a | kralle_a).sum()), ok, uvabw))
    # Lauf baer-pfoten: Krallen einzeln. Hinten bit-gleich, vorn = alt + K1 (nur y, +-0,1 mm), Form gleich (Abstaende in der Kralle)
    kr_alt = np.unique(FA2[kralle_a])
    k1 = Z["k1_dy"] if "k1_dy" in Z.files else np.zeros(len(VN))
    neu_von_alt = {int(a_): i for i, a_ in enumerate(Z["alt_von"]) if a_ >= 0}
    hinten_gleich = vorn_ok = vorn_n = 0
    abw_max = 0.0
    for i in kr_alt:
        j = neu_von_alt.get(int(i))
        if j is None:
            continue
        if VA[i, 0] < -0.1:
            # 2c: hinten Lage = alt + (C2C_KRALLE_DX, 0, 0) +-0,1 mm, y/z bit-gleich
            _dx = float(VN[j][0]) - float(VA[i][0])
            hinten_gleich += int(abs(_dx - C2C_KRALLE_DX) < 1e-4 and VN[j][1] == VA[i][1] and VN[j][2] == VA[i][2])
        else:
            vorn_n += 1
            soll = VA[i].astype(np.float64) + np.array((0.0, k1[j], 0.0))
            abw = float(np.abs(VN[j].astype(np.float64) - soll).max())
            abw_max = max(abw_max, abw)
            vorn_ok += int(abw < 1e-4 and VN[j][0] == VA[i][0] and VN[j][2] == VA[i][2])
    n_hinten = int((VA[kr_alt, 0] < -0.1).sum())
    log("KOPFPROBE K1: Krallen hinten %d von %d = alt + (dx -0,070; y, z bit-gleich; +-0,1 mm); vorn %d von %d = alt + K1 (x, z bit-gleich, y +-0,1 mm; Abweichung max %.2e m)" % (
        hinten_gleich, n_hinten, vorn_ok, vorn_n, abw_max))
    log("KOPFPROBE_OK")


def stufe_fbx():
    """Lauf baer-fell: Spielnetz (Spielmeter, Kopf +X, Boden z = 0) ohne Textur als FBX nach MOD_FELL, mit denselben
    Einstellungen wie stufe_backen_anim. Eingang fuer baer_kampf_fell.py (Gewichte, Maul, Clips) und den Textur-Bauer."""
    bpy.ops.wm.open_mainfile(filepath=NETZ + "lowpoly_%s.blend" % NAME)
    ob = bpy.data.objects["NCBear"]
    me = ob.data
    for o in list(bpy.data.objects):
        if o is not ob:
            bpy.data.objects.remove(o, do_unlink=True)
    me.materials.clear()
    me.materials.append(bpy.data.materials.new("NCBear"))
    for p in me.polygons:
        p.use_smooth = True
    for _a in ("gegend", "sohle"):
        if _a in me.attributes:
            me.attributes.remove(me.attributes[_a])
    VF, T = netz_arrays(me)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    ziel = os.environ.get("BAER_FELL_FBX", MOD_FELL + "models_X/WorldItems/NCBear.fbx")
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=ziel, use_selection=True, apply_unit_scale=True,
                             apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_anim=False,
                             mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False)
    log("MASSE Meter: Laenge %.3f Breite %.3f Hoehe %.3f; Punkte %d, Dreiecke %d" % (VF[:, 0].max() - VF[:, 0].min(), VF[:, 1].max() - VF[:, 1].min(), VF[:, 2].max(), len(VF), len(T)))
    fbx_neutral(ziel)
    log("FBX", ziel, os.path.getsize(ziel), "Byte")
    log("FBX_OK")


def fbx_neutral(pfad):
    """Nachbesserung 09.11.2026 (Pruefer Technik m7): der FBX-Export schreibt den lokalen .blend-Pfad (Original|ApplicationNativeFile)
    und die Uhrzeit (CreationTimeStamp). Pfad durch 'NCBear.blend' (gleich lang, mit Leerzeichen aufgefuellt: Laengenfelder bleiben)
    ersetzen, Zeitstempel fest 2026-11-09 00:00:00.000. Geometrie und alle anderen Bytes bleiben."""
    import re
    import struct
    b = bytearray(open(pfad, "rb").read())
    n_pfad = 0
    for m in list(re.finditer(rb"[A-Za-z]:[\\/][^\x00]{1,400}?\.blend", bytes(b))):
        neu = b"NCBear.blend"
        laenge = m.end() - m.start()
        b[m.start():m.end()] = (neu + b" " * max(laenge - len(neu), 0))[:laenge]
        n_pfad += 1
    i0 = b.find(b"CreationTimeStamp")
    n_zeit = 0
    if i0 >= 0:
        for nm, wert in ((b"Year", 2026), (b"Month", 11), (b"Day", 9), (b"Hour", 0), (b"Minute", 0), (b"Second", 0), (b"Millisecond", 0)):
            k = b.find(bytes([len(nm)]) + nm + b"I", i0, i0 + 600)
            if k >= 0:
                j = k + 1 + len(nm) + 1
                b[j:j + 4] = struct.pack("<i", wert)
                n_zeit += 1
    open(pfad, "wb").write(bytes(b))
    log("FBX neutral: Pfade ersetzt %d, Zeitstempel-Felder %d" % (n_pfad, n_zeit))


# ------------------------------------------------------------------ Lauf baer-pfoten: Stufe ansichten (aus baer_export.py:46-188, Rechnung gleich)
def _gpu(scene, samples, denoise=True):
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    used = []
    for d in prefs.devices:
        d.use = d.type == "OPTIX"
        if d.use:
            used.append(d.name)
    log("Geraete", used)
    assert any("4090" in u for u in used), "keine RTX 4090 mit OptiX"
    scene.cycles.device = "GPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = denoise
    if denoise:
        scene.cycles.denoiser = "OPTIX"
        scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.max_bounces = 8
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"


def _neutrale_welt(scene, oben=1.05, unten=0.72):
    w = bpy.data.worlds.new("backlicht")
    w.use_nodes = True
    nt = w.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = -1.0
    mr.inputs["From Max"].default_value = 1.0
    mr.inputs["To Min"].default_value = unten
    mr.inputs["To Max"].default_value = oben
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    nt.links.new(sp.outputs[2], mr.inputs["Value"])
    nt.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    nt.links.new(mr.outputs[0], nt.nodes["Background"].inputs[1])
    scene.world = w
    return w


def _kamera_daten():
    C_B = np.array((0.14, 0.0, 0.80))
    views = []

    def add(name, c, az, el, ortho, res):
        a, e = math.radians(az), math.radians(el)
        d = np.array((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        views.append(dict(name=name, c=[float(x) for x in c], d=[float(x) for x in d], ortho=ortho, res=res))
    for az in range(0, 360, 45):
        add("k_h%03d" % az, C_B, az, 0, 3.5, 2048)
    for az in range(0, 360, 60):
        add("k_o%03d" % az, C_B, az, 42, 3.5, 2048)
    add("k_top", C_B, 0.0, 89.5, 3.5, 2048)
    for az in range(30, 390, 60):
        add("k_u%03d" % az, C_B, az, -38, 3.5, 2048)
    add("k_bot", C_B, 0.0, -89.5, 3.5, 2048)
    return views


def _kopf_kameras(Q):
    c = np.array(Q["l2w"]((0.20, 0.0, -0.02)))
    views = []

    def add(name, az, el):
        a, e = math.radians(az), math.radians(el)
        d = np.array((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        views.append(dict(name=name, c=[float(x) for x in c], d=[float(x) for x in d], ortho=0.92, res=1536))
    for az, el in ((0, 4), (30, 2), (-30, 2), (62, 2), (-62, 2), (95, 2), (-95, 2), (0, 42), (55, 38), (-55, 38), (118, 30), (-118, 30), (0, -32), (48, -30), (-48, -30)):
        add("h_a%+04d_e%+03d" % (az, el), az, el)
    return views


def _kamera_setzen(scene, v):
    cam = bpy.data.cameras.new(v["name"])
    cam.type = "ORTHO"
    cam.ortho_scale = v["ortho"]
    cam.clip_start = 0.1
    cam.clip_end = 40.0
    co = bpy.data.objects.new(v["name"], cam)
    scene.collection.objects.link(co)
    c, d = Vector(v["c"]), Vector(v["d"])
    co.location = c + d * 12.0
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
    scene.camera = co
    scene.render.resolution_x = v["res"]
    scene.render.resolution_y = v["res"]
    bpy.context.view_layer.update()
    return co


def stufe_ansichten():
    """Hochmodell (baer_quelle_pfote.py, volle Qualitaet mit Fell) aus allen Richtungen als EXR mit Alpha -> ANS (Fellgrenze der Huelle).
    Gleiche Kameras wie baer_export.py; nur RTX 4090 mit OptiX. Vorhandene Bilder werden uebersprungen."""
    nur = ARGS[1] if len(ARGS) > 1 else None
    os.makedirs(ANS, exist_ok=True)
    Q = quelle("spiel")
    log("Hochmodell steht")
    scene = bpy.context.scene
    _gpu(scene, 96, True)
    _neutrale_welt(scene)
    scene.render.film_transparent = True
    scene.render.use_persistent_data = True
    im = scene.render.image_settings
    im.file_format = "OPEN_EXR"
    im.color_mode = "RGBA"
    im.color_depth = "32"
    im.exr_codec = "ZIP"
    views = _kamera_daten() + _kopf_kameras(Q)
    json.dump(views, open(ANS + "kameras.json", "w"), indent=1)
    for v in views:
        if nur and not v["name"].startswith(nur):
            continue
        out = ANS + v["name"] + ".exr"
        if os.path.exists(out):
            continue
        _kamera_setzen(scene, v)
        scene.render.filepath = out
        t = time.time()
        bpy.ops.render.render(write_still=True)
        log("ANSICHT", v["name"], "%.1fs" % (time.time() - t))
    log("ANSICHTEN_OK")


if STUFE == "ansichten":
    stufe_ansichten()
elif STUFE == "diagnose":
    stufe_diagnose()
elif STUFE == "netz":
    stufe_netz_anim()
elif STUFE == "backen":
    stufe_backen_anim()
elif STUFE == "kopfprobe":
    stufe_kopfprobe()
elif STUFE == "fbx":
    stufe_fbx()
else:
    raise SystemExit("Stufe %r gibt es hier nicht; Ansichten und Vorschau stehen in baer_export.py" % STUFE)
