# Lauf baer-2c: Nachbesserung fix1 (10.11.2026, 08:32-10:20)

Grundlage: `pruef_bericht.md` (2 blocker, 2 major, 8 minor). Blender 5.2.3, JDK 25, PZ 42.21.
**Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.** Endgueltig urteilt Kevin im Spiel.
- Stand vorher gesichert: `fix1/vorher/` (5 Mod-Dateien, alle `*_2c.py` + `lauf_2c.sh`, `glb_koerper/netz`, Dump; MD5 `fix1/vorher/md5.txt`).
- Nichts in NCBearTest (GLB dort weiter 5066fa67) oder NPC Crew geschrieben, nichts committet, nichts hochgeladen.
- Originale `*_pfote.py` unveraendert (9ae68692 / 402f9f5b / 14fceba9 / 380f259f / a14a4e1b). Fremde `_arbeit/baer_*` nur gelesen.
- Renders nur RTX 4090/OptiX + Entrauscher ueber `werkzeug/gpu_render.sh` (Sperre `gpu.lock`, am Ende frei; nicht auf das Spiel geprueft).
- Alle unten genannten Bilder habe ich angesehen. Blaetter mit `NURLOKAL` im Namen enthalten Kevins Spielbild/Vorlagen: nur lokal.

## 0. Ergebnis kurz

| Befund | Urteil | Beleg (vorher -> fix1) |
|---|---|---|
| **B1** Falten liegend Achsel+Ellbogen <= 136 | **behoben** | DeerStag_Dead sigma2<0,5: Achsel 142 -> **80**, Ellbogen 112 -> **47**, Summe 254 -> **127** (Ziel 120 knapp verfehlt); sigma2<0,3: 102 -> 74 (<= 200); Knie 157 -> 82; alle gestauchten 688 -> 498 (`fix1/mess/end2/falten_neu.txt`, `falten_detail_out.txt`) |
| **B2** Achsel/Brust <= 3,5 | **behoben** | SwipeR Achsel 3,51 -> **3,08**; ueber alle Clips 99,5 % 2,49 -> 2,33, Hoechstwert 3,68 -> 3,25 (`fix1/mess/end2/region_tabelle_out.txt`) |
| **M1** Kopf-Passung (Kragen) | **teilweise** | Spielkamera hinter dem Kopf Sit 0/30/60/90 +6,5/+6,7/+5,2/+6,7 -> **+3,9/+4,2/+2,6/+4,2 cm** (Soll <= +2); abgewandte Seite -5,7/-3,5/-3,3/-3,5 -> **-10,1/-8,6/-9,7/-8,6** (Soll <= -10); von vorn hinter -11,2..-11,5 -> -10,9..-11,2 (ok) (`fix1/mess/end2/log/kragen.txt`). Vorschlag des Pruefers (Nacken x 0,45-0,65) mit Beleg abgelehnt, siehe 1.3 |
| **M2** Hinterfuss im Ton laengliche Platte | **teilweise** | Umriss jetzt Ei statt Kapsel (Breiten-Schnitt x -0,50/-0,45/-0,40/-0,36/-0,33: 15,7/16,1/16,9/17,1/17,7 -> **16,6/18,5/19,3/19,4/18,6 cm**, `fix1/werkzeug/fuss_schnitt.py`); Netz-Platte Super-Oval 2,4 wie die Textur. Sichtbares L/B Spielkamera 1,34/1,36 -> 1,31/1,37 (ok), von vorn 1,50/1,51 -> **1,47/1,52** (Pruefer-Ziel <= 1,45 nur links; Spez 1,2-1,5 rechts +0,02). Zehen bleiben klein (Krallen/Zehen fest) |
| m1 Kopf blickt im Sitzen nach oben | offen (unveraendert, Zielkonflikt mit M1) | Schnauze Sit -10,5..-11,4 Grad wie vorher (`pruef/werkzeug/p_blick.py`) |
| m2 Knitter (Ton) | teilweise | Falten im Sitzen 587 -> 346, Rueckenfalte s2 min 0,24 -> 0,34; die kleinen schwarzen Knitter an Knie/Schenkel (Walk 20, SitDown 30, StandUp 7) sind im Ton noch da (`fix1/bilder/fix1_5b_knitter_zoom.png`) |
| m3 Vorderpfoten-Verringerung | abgelehnt (Rauschen, Beleg) | alte Punkte zur neuen Flaeche p95 0,94 mm, max 8,07 mm, 46 Punkte > 2 mm an der Sohle (vorher 1,1 / 8,1 / 47) - Verringern ist bei geaendertem Netz nicht bit-gleich wiederholbar, Form gleich |
| m4 Vorderkrallen hell | **behoben** | Mittel 2048 107/92/74 -> **88/74/61** (Wurzel max 92/79/65), nur dunkler (`fix1/textur/mess/textur_pruef_f1.json`) |
| m5 Brust-Stufe/Kehle (Textur) | offen | nicht angefasst |
| m6 Sitz-Ausnahme Kopf gegen Hals | offen (Entscheidung Kevin/Orchestrator) | jetzt ~57 Grad (Grenze 60) |
| m7 Beine im Ton glatte Saeulen | offen | Glocke formal ok: VL max +3,0, HL max +3,4 je 5 cm |
| m8 Nacken x 0,60 0,936 | abgelehnt (Beleg) | traegt nicht zum Kragen bei (1.3); unveraendert 0,936 |

Feste Regeln (alle ja): 12 Clips bit-gleich (Datei-Ebene), Skelett/Bind gleich, 19.806 Dreiecke, <= 4 Einfluesse, Summe 1, Kopf 1.333/1.333
bit-gleich (Lage+UV+Gewichte), Kopf-Texel 2048/1024 bit-gleich (amtliche Pruefung), Krallen vorn bit-gleich / hinten alt -0,070, Boden wie
vorher, Liegehoehe 1,12 cm, Dehnung, Falten, Ei 0,993, Zaehne bei Maul zu 0 aussen. Einzelheiten Abschnitt 3.

## 1. Was ich gemacht habe

### 1.1 B1/B2 und m2: Hautgewichte gegen die NEUEN Sitz-Clips (`baer/spiel/baer_gewichte_2c.py`)
Ursache: Die Optimierung las die Clip-Matrizen aus einem festen alten Dump (`_arbeit/baer_fell/bestand/dump.txt`, alte Sitz-Clips) und
tastete jeden 5. Bild ab - die Achsel-Spitze in SwipeR lag in Bild 13 und 18, also zwischen den Proben (eigene Auswertung von
`pruef/mess/p1/reg_neu/dehnung.npz`: SwipeR Achsel 3,51 in Bild 13).
Aenderungen (Kopfzeilen :2-5, alle neuen Schalter mit Vorgabe = altes Verhalten):
- `NCB_GEW_DUMP` (:86): Vorgabe jetzt `fix1/clips/dump_fix1_clips.pkl` = Clips des fix1-GLB (neue Sitz-Clips; 12 andere bit-gleich, geprueft).
- `swipe=1` (:233 ff.): SwipeL/SwipeR Bilder 6-23 einzeln.
- `liege=k`: Falten-Strafe in den 7 Liegebildern (Dead, Death ab 75 %) k-fach (:233, Energie `hz`).
- `band_z0/band_z1` (:222): Uebergangsband der Falten-Zone.
- `achsel_w/achsel_s` (:215 ff.): Zusatzstrafe auf sigma1 > achsel_s in Achsel+Brust (1.291 Dreiecke).
- Gradientenprobe (`pruef=1`) zeigt dieselbe Abweichung wie ohne die neuen Terme (Rauschen der bestehenden Rechnung).

Runden (je ~20 min CPU, 4 parallel; Logs `fix1/gew/r1|r2/*/gewichte.log`, Bewertung `fix1/gew/r*/eval_*.txt`):

| Variante | Achsel+Ellbogen (Dead) | Achsel/Brust max | 99,5 % / max |
|---|---|---|---|
| vorher (k5 B, alte Clips) | 142+112 = 254 | 3,51 | 2,49 / 3,68 |
| r1a nur neue Clips + swipe | 121+64 = 185 | 3,05 | 2,31 / 3,27 |
| r1c liege 8, falte_s 0,70 | 98+60 = 158 | 3,40 | 2,32 / 3,40 |
| r2a liege 16, achsel_w 200 | 92+51 = 143 | 3,44 | 2,31 / 3,44 |
| **r2b liege 30, falte_s 0,72, achsel_w 300 (s 3,1)** | **80+47 = 127** | **3,08** | **2,33 / 3,25** |
| r2c falte 150, liege 12 | 81+51 = 132 | 3,34 | 2,34 / 3,34 |

Gewaehlt **r2b** = neue Vorgabe `GEWPAR` in `werkzeug/lauf_2c.sh:26`
(`falte=100,falte_s=0.72,hoch=12,swipe=1,liege=30,band_z0=0.20,band_z1=0.45,achsel_w=300,achsel_s=3.1`; 8 Threads).
Hinweis Wiederholbarkeit: Die gelieferten Gewichte sind mit `dump_fix1_clips.pkl` gerechnet (SitDown mit Zwischenplatz der Vorderpfote
x 0,44); danach wurde nur noch `V_ZW` auf 0,43 gesetzt (1.4). Wer die Gewichte neu rechnet, bekommt sie mit dieser Datei byte-gleich.

### 1.2 M2 Hinterfuss (`baer_quelle_2c.py:962-973`, `baer_export_2c.py:999-1014`)
- Halbe Breite des Fussfeldes `w`: Ferse runder und breiter, Mitte bis 0,101 (vorher 0,086-0,091 fast gleich = Kapsel), Laenge gleich.
- Netz-Sohlenplatte Super-Oval 2,4 statt 3,4 (`C2C_PLAN_H`), Platte 16,0 / 13,2 cm breit (ay 0,080/0,066): der Fellkranz ist jetzt Form
  (Rand 1,5-2 cm um das Leder), nicht nur Textur. Die Textur (`H_PLATTE_EX` 2,3) und das Netz passen so zusammen.
- Verworfen (Runde f2): Ferse 7 mm kuerzer. Dann muss das Sprunggelenk im Sitzen tiefer, der Unterschenkel liegt im Boden und die
  Beckenloesung laeuft weg (`fix1/probe/pc.out`: Becken z 0,548, Pfoten 14 cm in der Luft). Laenge bleibt 29,4 cm.
- Haushalt: breitere Sohlen +90 Dreiecke -> `PF_RUMPF_REST` 10.600 -> 10.520 (`baer_export_2c.py:82`); Ergebnis 19.806 wie vorher.
- Folge: Der Packer legte eine Rumpf-Insel in den Zahn-Fleck (2048 x 984-1005, y 191-211, 335 Texel; Abbruch `baer_textur_2c.py:1803`).
  Die alten Sperrflaechen (`SPERR_PACKEN`) deckten die neuen Flecken nicht ganz; jetzt decken sie genau `SPERR_FLECKEN`
  (`baer_export_2c.py:151-154`). Netz-Lage, Dreiecke und Formel-Gewichte dabei bit-gleich (geprueft f4 gegen f5), nur das UV anders.

### 1.3 M1 Kragen: Ortung, Buckel, Sitzhaltung
**Ortung** (`fix1/werkzeug/kragen_ort.py`, `kragen_seite.py`, Log `fix1/log/kragen_ort.txt`): Alle Koerperpunkte, die in der Spielkamera
ueber die Kopf-Oberkante ragen, liegen in Ruhe bei **x 0,13-0,30, z 1,14-1,16, Gewicht Spine1 = 1,0** - das ist der Buckel. Auch die Kante
neben dem Kopf ist Buckel-Flanke (x 0,22-0,25, |y| 0,20, z 1,03-1,07). Der Nacken x 0,45-0,65 und der Kopfnaht-Schutz tragen nichts bei.
Darum habe ich den Pruefer-Vorschlag "Nacken x 0,45-0,65 senken, Kopfnaht-Schutz 9 -> 5 cm" **nicht** umgesetzt (er haette nur die Kopf-
Bit-Gleichheit gefaehrdet) und m8 (Nacken x 0,60 = 0,936) bleibt.
Die Kamerarichtung "oben im Bild" zeigt fuer Spine1-Punkte im Sitzen fast genau auf Ruhe-z (0,12 / 0 / 0,99): jeder cm Buckel tiefer
ist ~1 cm weniger Kragen.

Umgesetzt:
1. **Buckel** (`baer_export_2c.py:1865-1880`, Schritt (g) in `form_2c`, `C2C_BUCKEL` :1959): Kamm 1,3 cm tiefer (Spez-Toleranz 1,5),
   Flanken (|y| ab 0,08-0,20) bis 4,5 cm tiefer -> Buckel schmaler, Kamm bleibt; voll x 0,02-0,28, aus bei -0,10 / 0,38.
   Ruecken-z x 0,10/0,20/0,30: 1,139/1,159/1,140 -> **1,126/1,145/1,126** (Spez 1,139/1,159/1,142 +-1,5: x 0,30 liegt 1 mm unter dem
   Band, wenn man 1,142 nimmt; gegen die mess2c-Referenz 1,140 im Band). x 0,40 1,048 -> 1,056 (jetzt im Band 1,05-1,07).
2. **Sitzhaltung** (`baer_kampf_2c.py:1306-1311`): Brust -37 -> -40 (Spez-Soll 5.2), Hals -78 -> -77,5, Schulterblatt 16 -> 18; Lende
   -27, Kopf -20 (Welt), Becken und Sprunggelenk unveraendert. Probe ueber 13 Varianten (`fix1/probe/pa.py`-`pe.py`, Logs `.out`):
   Brust -40 bringt ~1,5 cm Kragen, Lende -29 erzeugte eine Klemmung in StandUp (Bild 9), Schulterblatt 20 klemmt, Hals -78 gab eine
   Kopf-Oberkante von 1,322-1,327.
3. Kopf-Oberkante jetzt **1,316-1,323 m** (Spez 1,20-1,32: Bild 60 +3 mm darueber).

Weiter kommt man nur mit einem tieferen Buckel (ausserhalb der Spez) - **Vorschlag fuer Kevin**, nur gerechnet
(`fix1/log/kragen_vorschlag_buckel.txt`): Kamm weitere 1,5 cm tiefer -> hinter +1,1..+2,7 cm; 3,0 cm tiefer -> -0,4..+1,2 cm (alle <= +2).
Die Seiten bleiben dabei -8,6..-10,1. Der Buckel ist aber Kevins Wunsch ("Schulterbuckel"), deshalb nicht gebaut.

### 1.4 Folgen in den Sitz-Clips (`baer_kampf_2c.py:1473`)
Mit Brust -40 und dem breiteren Fuss stach in SitDown Bild 29-30 ein Punkt der linken Hinterzehe in den Unterarm (`fix1/probe/pg.out`).
Zwischenplatz der Vorderpfoten `V_ZW` x 0,44 -> 0,43: 0 Punkte (`fix1/probe/pi.py`, Endstand `fix1/probe/pg_end2.out`).

### 1.5 m4 Krallen (`baer_textur_2c.py:726`)
`KRALLE_V` 72/59/48 -> 150/134/113 jetzt 66/54/44 -> 112/98/82 (Regel "vorn hoechstens dunkler").

### 1.6 Kette
Netz f1 -> f2 (kurze Ferse, verworfen) -> f3 (Zwischenstand, unbenutzt) -> f4 -> **f5** (nur Sperrflaechen/UV neu). Gewichte r2b, GLB +
Deer (`fix1/bau_f5`), Textur-Kette als Kopie `fix1/werkzeug/textur/lauf_textur_f1.sh` (Ausgabe `fix1/textur/`, Ansichten neu gerendert, weil
sich das Hochmodell am Fuss geaendert hat). GLB aus der Textur-Kette = GLB aus `fix1/bau_f5` (08ec7806, byte-gleich).

## 2. Geaenderte Skripte (`baer/spiel/`, MD5 vorher -> nachher; `fix1/log/md5_skripte_nachher.txt`)
| Datei | MD5 | Zeilen |
|---|---|---|
| `baer_quelle_2c.py` | 72230dae -> efe9d3fb | :962-973 Fussbreite |
| `baer_export_2c.py` | 85eb1f11 -> 13b06a84 | :82 Haushalt, :151-154 Sperrflaechen, :999-1014 Platte, :1865-1880 + :1959 Buckel |
| `baer_gewichte_2c.py` | 8bdd899a -> f2d68d2a | :2-5, :43, :85-90, :215-218, :222, :230-243, Energie/Gradient |
| `baer_kampf_2c.py` | b1575c19 -> 3ec0fbd2 | :1306-1311 Sitzhaltung, :1473 V_ZW |
| `baer_textur_2c.py` | 19060fa4 -> 670fe492 | :726 Vorderkrallen |
| `baer_maul_2c.py` | be09fe8e (unveraendert) | |
| `_arbeit/baer_2c/werkzeug/lauf_2c.sh` | 9e7fbbaa -> 199e1fb5 | :26 GEWPAR r2b |
Zeilenenden je Datei wie vorher (export/quelle/gewichte CRLF, kampf/textur LF; Werkzeug `fix1/werkzeug/ersetze.py`).

## 3. Messungen Endstand (`fix1/mess/end2/`, Dump = GLB 08ec7806)
| Pruefung | vorher | fix1 | Soll | ok |
|---|---|---|---|---|
| Clips | 12 bit-gleich | 12 bit-gleich: Dump-Text (`log/clips.txt`) und Datei-Ebene (Sampler-Puffer, Knoten, inverseBind) | bit-gleich | ja |
| Sitz-Clips Dauer/Proben/Schleife | 1,6/4,0/1,3 s, 49/121/40 | gleich; Sit 0 = 120, SitDown-Ende = Sit 0 = StandUp 0 (0,0); Anfang/Ende gegen Idle 0,1308 wie heute (`log/sitz.txt`) | gleich | ja |
| Klemmungen / Durchdringung Sitz-Clips | 0 / 0 | 0 / 0 je Bild (`fix1/probe/pg_end2.out`, Bericht `bau_f5/log/bericht_final.json`) | 0 | ja |
| Dreiecke / Einfluesse / Summe | 19.806 | 19.806 / max 4 / 0,9999999-1,0000002 | <= 19.850 | ja |
| Kopf | 1.333 bit-gleich | 1.333/1.333 Lage+UV+Gewichte, 9 Normalen am Nahtrand (wie immer) | bit-gleich | ja |
| Kopf-Texel (amtlich `textur_pruef_2c.py`) | 0 / 0 | 2048: 0 von 858.272; 1024: 0 von 212.944; Flecken 0 verschieden zum Gebiss-Bauer | 0 | ja |
| Kopf-Texel (Pruefer-Raster `p_texel.py`) | 2048 0, 1024 2 (max 9) | 2048 1 (max 24), 1024 3 (max 29) - Randtexel der Raster-Maske, ausserhalb der amtlichen Maske | | Hinweis |
| Krallen | vorn 227 gleich, hinten -0,070 | gleich | | ja |
| Zaehne Maul zu | 0 aussen, 2,5 mm | 0 aussen, 2,5 mm (`log/zaehne.txt`) | 0 / >= 2 mm | ja |
| Boden je Clip | | wie vorher (Run -2,98, Walk -2,40, Death -0,14, Sitz -0,00); die 2 "Verstoesse" = Hinterkralle im Sitzen 24,9 cm UEBER dem Boden (wie vorher) | nicht tiefer | ja |
| Liegehoehe Dead | 1,12 cm | 1,12 cm | 0,35-1,40 | ja |
| Dehnung 99,5 % / max / Achsel-Brust | 2,49 / 3,68 / 3,51 | **2,33 / 3,25 / 3,08** | 2,6 / 4,0 / 3,5 | ja |
| Kehle / Ruecken-Flanke in Sit | 2,56 / 3,68 | 2,26 / 3,25 | | |
| Falten Dead Achsel+Ellbogen / <0,3 | 254 / 102 | **127 / 74** | 136 / 200 | ja |
| Falten Sit (Info) | 587 | 346 | | |
| Splitter max | 34,7 | 20,2 (SwipeR 13, Achselrand) | | |
| Ei (Rear 1,3 s) | 0,993 | 0,993 | >= 0,95 | ja |
| Glocke Ruhe | vorn 3,01 / hinten 3,38 | vorn max 3,0 / hinten max 3,4 | 3,0 / 3,5 | ja |
| Rumpf gesamt | 0,794 | 0,794 | <= 0,82 | ja |
| Hinterfuss Laenge / Breite x -0,50 | 29,3 / 15,7 | 29,4 / 16,6 (Schnitt) | 29 +-1 / 15-17 | ja |
| Breite x -0,33 | 17,7 | 18,6 (Fuss mit Fellkranz; Leder 16,0) | Platte 17-18 | Spez-Wert +0,6 (gewollt, M2) |
| Sitzen: Fussabstand / Ferse / Pfoten / Luecke | 69,1 / 0,15 / 0,00 / 1,5 | 70,0 / 0,09-0,10 / 0,00 / 1,5 | 62-72 / 0-0,5 / flach / >= 1 | ja |
| Unterseite (Spiel-Licht) | Kehle 0,79 ... Innenbein 0,43 | Kehle 0,78, Achsel 0,52, Leiste 0,53, Innenbein 0,43/0,46, Brust 0,69, Bauch 0,52, Hinterteil 0,56 (`log/mess_textur.txt`) | >= 0,40 | ja |
| Texel-Baender um den Kopf 0-4/4-8/8-12/12-20/20-35/35-60 | 1,00/0,95/0,95/1,01/0,94/0,70 | 0,99/0,95/0,95/1,02/0,93/0,70 (`end/log/texel_naht.txt`) | | wie vorher |
| Hintersohle Median | 67/48/39 | 66/48/39 (HL), 69/50/40 (HR), R-B 27/29 | 62/42/30 +-12 | ja |
| Straehnen (`mess_bild`) | 0,070 / 0,656 | nicht neu gemessen (Rumpf-Textur-Rechnung unveraendert, Unterseite/Baender gleich) | | ungeprueft |

## 4. Bilder (`fix1/bilder/`, alle angesehen; vorher = Stand vor fix1, fix1 = Endstand)
- `fix1_1_sitzen_spielkamera_NURLOKAL.png`: Kevins Spielbild | Vorlage | vorher/fix1 Ton und Textur (az 0 el 30, Sit 60) + Sit 0.
  Gesehen: Die Kuppel hinter dem Kopf ist kleiner und schmaler, der Kopf sitzt etwas freier oben; ganz weg ist sie nicht (M1 teilweise).
  Hinterfuesse im Ton breiter und unten runder.
- `fix1_2_sitzen_ansichten.png`: vorn / az -30 / Seite / hinten, Ton und Textur. Seitlich etwas aufrechter, Buckel flacher.
- `fix1_3_hinterfuss_NURLOKAL.png`: Fuss im Sitzen el 10/30, Sohle von unten, Seite, Ton/Textur, neben den Vorlagen-Fuessen. Von unten Ei
  statt Kapsel, Leder-Oval mit Fellkranz in Form und Farbe; im Ton bleibt er laenger als die fast runde Vorlage, Zehen klein.
- `fix1_4_stehen_liegen_achsel.png`: Stehen Spielkamera seitlich (keine "Hose im Stiefel", wie vorher), Liegen, Achsel liegend, SwipeR 13.
- `fix1_5_knitter.png`, `fix1_5b_knitter_zoom.png`: Walk 20/2, StandUp 7, SitDown 30 - Knitter im Ton weiter sichtbar (m2 teilweise).
- `fix1_6_hinsetzen_aufstehen.png`: Hinsetzen/Aufstehen je 7 Bilder, Ton und Textur: fluessig, nichts im Boden.
- Arbeitsblaetter `f1_fuss_ton_NURLOKAL.png`, `f4_sitzen_ton_NURLOKAL.png`; Einzelbilder `fix1/render/v0|neu|seq|f1|f4/`.
- Ein Vorschau-Video habe ich nicht neu gerendert (Bildfolge `fix1_6` statt dessen).

## 5. Die 5 Mod-Dateien (`_arbeit/baer_2c/mod/42/media/`, genau 5; `fix1/log/md5_mod.txt`)
- `models_X/Skinned/NCBear.glb` **08ec7806efd13181bcc6bfd99a11f3fa** (vorher 0ce2661e)
- `models_X/Skinned/NCBearDeer.glb` **91f0c60e2bbeba846779b8ef53133eaf** (vorher 7a9f8778)
- `models_X/WorldItems/NCBear.fbx` **da08d469de1e06d12d4c71461d3c026c** (vorher b440d693)
- `textures/Body/NCBear.png` **4cfdb177784758fc53eacd07a8319f45** (1024 RGB; vorher 9e9147b5)
- `textures/WorldItems/NCBear.png` **a640e4cd4c30cca8ed1c991d49f1cc55** (2048 RGB; vorher dc8ad63d)

## 6. Offen / fuer Kevin
1. **Kragen** +2,6..+4,2 cm (Soll +2), Seite -8,6..-10,1 (Soll -10): Rest ist der Buckel. Entscheidung: Buckel 1,5-3 cm tiefer
   (Zahlen 1.3) oder so lassen.
2. **Kopf blickt nach oben** (m1) und Sitz-Ausnahme Kopf gegen Hals ~57 Grad (m6): unveraendert, Zielkonflikt mit 1.
3. Kopf-Oberkante Bild 60 1,323 m (Spez 1,32, +3 mm).
4. Hinterfuss von vorn L/B rechts 1,52 (Spez bis 1,5); im Ton noch laenger als die Vorlage, Zehen klein.
5. Knitter im Ton (Walk 20 Knie, SitDown/StandUp Schenkel), Brust-Stufe (m5), glatte Bein-Saeulen (m7): nicht behoben.
6. Vorschlag-Dateien `vorschlag/NCBear_kopftexel*.png` und `*_lippensaum_endstand*.png` gehoeren zum Stand VOR fix1 (Rumpf-UV ist neu):
   Kopf-/Lippen-Texel darin gelten weiter, als ganze Textur passen sie nicht mehr - bei Bedarf mit `werkzeug/textur/vorschlag_kopftexel.py`
   auf die neue Textur neu rechnen.
7. Clip-Runde unveraendert offen (Lefzen, Aufrichten neu, Liegehoehe). `C:\render\` von Bau Koerper liegt weiter da (von Hand loeschen).
8. **Nicht gespielt.** Kevins Test: `NCBear_Sit(20)` aus der Spielkamera (Kopf/Buckel, Fuesse), Stehen/Gehen seitlich, Liegen.

## 7. Wiederholen (`cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c`)
```
R=$PWD/fix1/bau_f5 bash werkzeug/lauf_2c.sh netz fbx kopfprobe formel gewichte glb deer   # Gewichte ~20 min (GEWPAR r2b, Clips dump_fix1_clips.pkl)
cp fix1/bau_f5/netz/{lowpoly_2c.blend,lp_2c.npz,form2c_feld_2c.npz} fix1/textur/netz/; cp fix1/bau_f5/netz/sohle_layout_2c.json fix1/textur/netz/sohle_layout.json
python werkzeug/kette/karten.py fix1/textur/netz/lp_2c.npz fix1/bau_f5/netz/gewichte_2c.npz fix1/textur/netz/karten
bash fix1/werkzeug/textur/ansichten_beide.sh            # GPU, nur wenn sich das Hochmodell aendert
bash fix1/werkzeug/textur/lauf_textur_f1.sh t0 texel bezug; bash fix1/werkzeug/textur/lauf_textur_f1.sh 2c backen glb deer
R=$PWD/fix1/bau_f5 bash fix1/werkzeug/messen_f1.sh end2 dump_final.txt
```
Werkzeuge `fix1/werkzeug/` (kragen_ort/seite/probe/vorschlag, fuss_schnitt, fuss_lb, gew_varianten.sh, gew_eval.sh, pose_probe_f1.py,
auftrag_f1.py, blatt.py, ersetze.py, messen_f1.sh, textur/*); Proben `fix1/probe/`; Bau-Ordner `fix1/bau_f1..f5`, Gewichte `fix1/gew/`.
