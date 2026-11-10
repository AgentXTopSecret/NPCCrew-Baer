# Lauf baer-2c: Bau Koerper (10.11.2026, 01:48-04:15)

Blender 5.2.3, JDK 25, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
- Nichts in die Test-Mod NCBearTest geschrieben (GLB dort weiter 5066fa67), nichts nach NPC Crew, nichts committet.
- Originale `*_pfote.py` unveraendert (MD5 9ae68692 / 402f9f5b / 14fceba9 / 380f259f / a14a4e1b wie vor dem Lauf).
- Fremde `_arbeit/baer_*`-Ordner nur gelesen. Alle Bilder unten habe ich angesehen.
- Renders nur RTX 4090/OptiX (+ OptiX-Entrauscher) ueber `werkzeug/gpu_render.sh` (Sperre `gpu.lock`).
- **Versehen:** Ein frueher Render-Auftrag hatte einen relativen Ausgabepfad; Blender schrieb 14 Ton-PNGs nach `C:\render\f3\`
  (02:06, nur Ton-Bilder der dichten Huelle, keine Vorlage/kein Spielbild). Kopien liegen in `render/f3/`. Das Loeschen von
  `C:\render\` wurde vom Sicherheits-Check blockiert - **bitte von Hand loeschen**. Seitdem sind alle Ausgabepfade absolut.

## 0. Kurz

| Ziel | Ergebnis (Endstand k5, Variante B) | Soll | ok |
|---|---|---|---|
| Glocke / "Hose im Stiefel" (Ruhe, waagerecht, Zunahme je 5 cm) | vorn 1,8 / 3,0 / 3,0 / 2,1 (vorn-y max 3,1), hinten max 3,4 | vorn <= 3,0, hinten <= 3,5 | knapp (vorn 3,0-3,1) |
| dto. heute | vorn +7,2 / +8,7 cm, hinten +7,8 / +9,6 cm | | |
| Rumpf gesamt | **0,794 m** (heute 0,930) | <= 0,82 (ideal 0,78) | ja |
| Rumpf-Halbbreite x -0,60..0,50 | alle 12 Werte im Soll-Band (z. B. x 0,30: 0,392; heute 0,467) | Tabelle 2.4 | ja |
| Nacken Ruecken-z x 0,40 / 0,50 / 0,60 | 1,048 / 0,974 / 0,936 (heute 1,083 / 1,016 / 0,938) | 1,05-1,07 / 0,96-0,99 / 0,90-0,92 | x 0,60 nein (+1,6 cm, Kopfnaht-Schutz) |
| Hals-Halbbreite x 0,50 | 0,274 (heute 0,324) | 0,255-0,29 | ja |
| Buckel x 0,10 / 0,20 / 0,30 | 1,139 / 1,159 / 1,140 | 1,139 / 1,159 / 1,142 +-1,5 cm | ja |
| Hinterfuss Laenge (Haut, ohne Krallen) | **29,3 cm** (Ferse -0,557, Zehenstirn -0,264); heute 43,2 | 29 +-1 | ja |
| Hinterfuss Breite x -0,50 / x -0,33 | 15,1 / 17,6 cm | 15-17 / 17-18 | ja |
| Hinterkrallen | 228/228 = alt + (-0,070; y, z bit-gleich) | -0,070 +-0,1 mm | ja |
| Clips | 15/15 bit-gleich, Knochen/Eltern/Offset/Bind gleich | bit-gleich | ja |
| Kopf | 1.333/1.333 Lage+UV+Gewichte bit-gleich, gehaeutet in allen Bildern 0,00 mm | bit-gleich | ja |
| Dreiecke | **18.990** (heute 19.426) | <= 19.850 inkl. Maul (+544 -> ~19.534) | ja |
| Dehnung 99,5 % / max | 2,49 / 3,51 (heute 2,59 / 3,40) | <= 2,6 / <= 4,0 | ja |
| Dehnung Achsel/Brust | **3,51** (SwipeR) | <= 3,5 | **nein (0,01)** |
| Falten liegend Achsel+Ellbogen | **254** (heute 136) | <= 136, Ziel 120 | **nein** (Begruendung 3.4) |
| Ei (Rear 1,3 s) | 0,993 (heute 1,032) | >= 0,95 | ja |
| Boden, 12 Nicht-Sitz-Clips | 0 Verstoesse; Walk-Kralle hinten +0,73/+0,66 (heute -2,08/-2,23) | nicht tiefer | ja |
| Liegehoehe Dead | 1,12 cm (heute 0,40) | 0,35-1,40 | ja |

Im Ton aus der Spielkamera: Pfote -> Unterarm/Unterschenkel -> Ellbogen/Knie -> Schulter/Schenkel -> Rumpf ist eine Linie,
keine "Hose im Stiefel" mehr (`bilder/koerper_stehen_spielwinkel_ton.png`). Hinterfuss kurz, Ferse rund.

**Nicht gemacht (nicht mein Teil):** Sitz-Clips, Kragen-Messung in der neuen Sitzpose, Gebiss, Texturen (Sohle dunkel,
Hals-/Schulter-Texel). `gewichte_eigen` in `baer_kampf_2c.py` ist **unveraendert**: die Optimierung haelt die Dehnung, eine
Formel-Aenderung haette nur die Ausgangslage verschoben.

## 1. Was geaendert ist (Kopien in `baer/spiel/`, MD5 Endstand)

| Datei (MD5) | Aenderung |
|---|---|
| `baer_quelle_2c.py` (72230dae) | `OUT` -> `_arbeit/baer_2c/hoch/` (:26).<br>`PF_KRALLEN["H"]["x"]` alle -0,070 (:929-931).<br>`PF_ZEHE["H"]` kuerzer und runder: ax 0,0215-0,0238 statt 0,027-0,031, ay +1 mm (:943-945).<br>`PF_TEILE["H"]` (:950-973), Bein: Hinterkante unten -0,548..-0,566 bis z 0,12, dann zur Hacke -0,598 bei 0,20 (:957); unten schmaler, hw 0,066 bei z 0,03 (:959).<br>`PF_TEILE["H"]` Fuss: Ferse x0 -0,555, vorn x1 -0,302; w als Oval (Ferse 0,036 -> 0,091); zb Fersenrundung r ~4 cm; zt Fersen-Oberkante 0,085 (kein Rand ueber dem Bein); Rist faellt 0,160 -> 0,064; Querschnitt n 2,4 statt 2,8.<br>Hochmodell-Krallen hinten Sx -0,070/PF_G (:1809). |
| `baer_export_2c.py` (a44ad5c3) | Pfade -> `_arbeit/baer_2c/`, Name `2c`, Quelle `baer_quelle_2c.py` (:56-66).<br>`PF_ZIEL` 4.300 -> 3.950 (:80).<br>fix1 (c)/(d) Ferse aus: `FIX1_FERSE_DX`/`_BREIT` 0 (:95-96).<br>`C2C_FUSS`, `C2C_KRALLE_DX` (:917-918).<br>Neuer Ballenplan hinten `_2c_platte`/`C2C_PLAN_H` (:991-1012): Sohlenballen Super-Oval x -0,552..-0,340, 14,1 cm vorn / 13,0 an der Ferse; 5 Zehenballen 3,6 cm, Mitte 3,0 cm hinter der Krallenwurzel, im Bogen; benutzt in `ballen_plan` (:1023).<br>**`form_2c`** (Block :1627-1937, Aufruf :1983-2000, Abschnitt 2).<br>Hinterkrallen starr -0,070 + `k2c_dx` in `netz_2c.npz` (:2280-2287, :2351).<br>`kopfprobe` prueft hinten alt + (-0,070) (:3133); Diagnose-Zeile stuerzt nicht mehr ab, wenn keine Kralle bit-gleich ist (:3091).<br>Verschiebungsfeld `netz/form2c_feld_2c.npz` (:1998). |
| `baer_gewichte_2c.py` (8bdd899a) | Kopf-/Krallen-Zuordnung rechnet `k2c_dx` zurueck (:64-66).<br>Lauf mit `falte=100,falte_s=0.62,hoch=12` (Variante B, 3.3). |
| `baer_kampf_2c.py` (11c7f3c4) | Nur Pfade: Vorgabe-Quelle `_arbeit/baer_2c/mod/42/media/` (:53), Gewichte `.../netz/gewichte_2c.npz` (:1777). Clips und `gewichte_eigen` unveraendert (Bau Sitzen/Gebiss). |
| `baer_textur_2c.py` (fbd67ac7) | Nur Pfade: ARB `_arbeit/baer_2c/`, EXPORT `baer_export_2c.py`, Name `2c` (:44-50). Rest fuer den Textur-Bauer. |

## 2. `form_2c` (dichte Huelle nach fix1, Spielmeter; Quelle auch `form/form2c_block.py`)

- **(a) Beine in x** (:1775): Vorder-/Hinterkante je Hoehe auf die Soll-Tabelle.
  - Die heutigen Kanten werden bis z 0,35 alle 5 mm am Netz gemessen, darueber gelten die gedachten Kanten der Forschung.
  - Beides wird in z geglaettet (Gauss 1,2/1,5 cm). Bei rein linearer Tabelle zeigten sich Ringe auf dem Bein (Runde f3).
  - Ueber z 0,36-0,44 wirkt es nur an den Beinseiten, die Brust-/Bauchmitte bleibt.
  - Schenkel-Hinterkante z 0,40-0,45 stetig nach hinten: -0,618 / -0,637, dann -0,683 bei z 0,50. Heute war dort eine Stufe von
    -0,614 auf -0,683. Der Bodenspielraum ohne die drei Sitz-Clips ist dort >= 10,6 cm (`log/spielraum_12.txt`).
- **(b) Innenkante** (:1790): Innenkante der Beine auf das Soll, zur Mittellinie auf 0.
- **(c) EIN Seitenfeld** (:1802): |y| > 0,20 wird gestaucht.
  - Der Faktor kommt je Hoehe aus der Bein-Tabelle (aussen y) und je x-Scheibe aus der Rumpf-Soll-Halbbreite (ab z 0,28-0,42).
  - Dazwischen wird gemischt. So gibt es keine Kastenwand, und die Rundung bleibt.
- **(d) Brust** zwischen den Vorderbeinen auf ~0,36 (weiches Maximum, nur Unterseite) (:1839).
- **(e) Nacken** x 0,40-0,60 um 3-4,5 cm tiefer (:1848).
- **(f) Behang als Umriss-Kante** (:1856): hinter dem Ellbogen 4,5 cm (z 0,36-0,54, ueber der freien Beinschleife, damit die
  Glocke-Regel haelt), Bauchkante 3 cm (x -0,24..0,07, nicht an der Kniefalte).
- **Feldglaettung** (:1871): 25 Runden. Fest bleiben die Pfoten unter z 0,115, der Kopf ab x 0,70 und **alles bis 9 cm um die
  alte Kopfnaht** (weich bis 17,5 cm). Nur so bleibt der Kopf-Nahtrand (149 Punkte, spaeter mit dem Rumpf geglaettet) bit-gleich;
  ohne den Schutz waren 157 Kopfpunkte verschoben (Runde k1).
- **Naht-Glaettungen** (:1886, :1896, :1902):
  - Taubin an Achsel und Leiste.
  - Laplace am Achselrand gegen 1-2 cm hohe Spitzen (`form/bild/schnitt_x0.30.png`).
  - Knoechelband z 0,13-0,24 gegen einen Ring ueber der Ferse (`form/bild/f15_fuss.png` vor, `f16_fuss.png` nach dem Glaetten).
- Danach wird entwirrt.
- Kennzahlen: 95.295 von 155.4xx Punkten > 2 mm bewegt, max 13,8 cm, p95 9,1 cm.

## 3. Runden

| Runde | Was | Befund (Bild angesehen) |
|---|---|---|
| r0 | nur neuer Hinterfuss (Huelle) | 29,5 cm lang |
| f1-f3 | form_2c erste Fassungen, Brust heben | Profil-Tabellen getroffen; Hoerner am Achselrand, Ringe am Bein (`form/bild/f3_blatt*.png`) |
| f4-f7 | feines z-Raster, Rumpf-Faktor nur ueber den Beinen, Kopfnaht-Schutz, Hals 0,300 | Ringe weg, Halsband-Ring weg (`form/bild/f7_blatt.png`) |
| k1 | ganze Kette mit Formel-Gewichten | Spielkamera ohne Stiefel (`form/bild/k1_a..e.png`); Kopfrand noch verschoben |
| k2 / k3 | mit Gewichtsoptimierung | Kopf 1.333/1.333 bit-gleich; Achsel 3,56/3,57, Falten 220/235 |
| f8-f13 | Behang hoeher, Bauchkante vor die Kniefalte, Innenkante/Hacke nachgestellt | alle Schritte vorn <= 3,0-3,1, hinten <= 3,4 |
| k4 | Kette | 99,5 % 2,63 > 2,6 mit Standard-Gewichten |
| f14-f16 | Ferse von unten oval, von hinten rund, kein Ring | `form/bild/f14_fuss.png`, `f15_fuss.png`, `f16_fuss.png` |
| **k5** | Endstand; Gewichte A (hoch=10) und **B (hoch=12, falte=100)** | B gewaehlt: Achsel 3,51 statt 3,53, Achsel+Ellbogen 254 statt 264 |

Gewichts-Proben:
- k2 mit falte=100: 99,5 % 2,63, Achsel 3,66 - verworfen.
- k4 mit hoch=10: 2,47 / 3,50.
- k5 A: 2,49 / 3,53, Falten 668.
- k5 B: 2,49 / 3,51, Falten 688.

## 4. Messungen Endstand (`pruef_koerper/k5B/`, Dump `glb_koerper/dump_koerper.txt`)

### 4.1 Beine (Ruhe, waagerechte Schnitte, freie Schleife; `beine/beine_mass.txt`, `glocke_posen.txt`)

| z | 0,15 | 0,20 | 0,25 | 0,30 | 0,35 |
|---|---|---|---|---|---|
| VL Seite / Soll / heute | 19,5 / 19,5 / 18,7 | 21,3 / 21,5 / 19,8 | 24,3 / 24,4 / 27,0 | 27,3 / 27,0 / 35,7 | 29,4 / 29,3 / 39,1 |
| VL vorn / Soll / heute | 18,6 / 19,0 / 18,5 | 20,2 / 21,0 / 20,4 | 22,7 / 23,2 / 27,9 | 24,9 / 25,8 / 36,8 | 27,5 / 29,0 / 40,6 |
| HL Seite / Soll / heute | 19,3 / - / 23,4 | 20,8 / 21,0 / 21,7 | 24,1 / 24,1 / 29,4 | 27,5 / 26,7 / 39,0 | 30,5 / 29,3 / 42,7 |
| HL vorn / heute | 17,9 / 18,1 | 19,5 / 20,2 | 22,6 / 27,2 | 26,0 / 35,6 | 28,6 / 38,7 |

- **Zunahme je 5 cm (Ruhe):**
  - VL Seite +1,8 / +3,0 / +3,0 / +2,1; VR vorn bis +3,1 (Grenze 3,0).
  - HL bis +3,4 (Grenze 3,5).
  - Kein Schritt < -0,5; max/Mittel 1,18-1,33 (<= 1,6).
  - Heute +7,2 bis +9,6, max/Mittel bis 1,99.
- **Idle Bild 0** gleich (VL Seite max 3,05).
- **Senkrecht zum Knochen:**
  - Ruhe Unterarm max 3,0.
  - Unterschenkel bis 3,9 an der obersten freien Stelle unter dem Knie (heute 6,3-6,7).
  - Walk Bild 2 Unterschenkel 3,3, Unterarm 3,2.
  - Die oberste Stelle am Ellbogen schneidet bei Idle/Walk schon den Rumpf (+4,4 bis +16), wie heute.
  - Walk Bild 20: Unterarm +5,2 an der Ellbogen-Stelle (Bein weit hinten, Schnitt streift die Achsel).
- **Formal:** vorn 0,0-0,1 cm ueber 3,0 an einzelnen Schritten; im Bild keine Kante (`bilder/koerper_stehen_*`).
- **Schenkel-Hinterkante** z 0,40 / 0,45 / 0,50 / 0,60 / 0,70: -0,618 / -0,637 / -0,683 / -0,742 / -0,781.
  - Stetig, die Stufe -0,614 -> -0,683 ist weg.
  - Soll-Ziel z 0,50-0,70 (-0,66 / -0,71 / -0,75) ist 1-3 cm weiter hinten erreicht (Hintern wie heute).

### 4.2 Rumpf, Nacken, Hinterfuss (`mess2c_out.txt`)
- **Halbbreite x -0,60..0,50:** 0,368 / 0,396 / 0,396 / 0,382 / 0,337 / 0,337 / 0,344 / 0,369 / 0,386 / 0,392 / 0,369 / 0,274.
  Alle liegen im Soll-Band. Gesamt 0,794 m.
- **Ruecken-z:** siehe 0. x 0,60 0,936 statt 0,90-0,92. Das liegt 9-17 cm von der Kopfnaht und damit im Schutzband
  (Kopf bit-gleich hat Vorrang).
- **Hinterfuss:**
  - Ferse -0,557, vorn -0,264: 29,3 cm.
  - Breite x -0,50 15,1, x -0,33 17,6 cm.
  - Im alten Sitz-Clip sichtbares L/B aus der Spielkamera 1,48 (heute 2,14), von vorn 1,70 (heute 2,44). Das neue Sitzen macht
    Bau Sitzen.

### 4.3 Feste Regeln
- **Clips und Skelett** (`bau_k5/log/glb_pruef_B.txt`): 15/15 Abtastungen/Schluessel/Modellmatrix gleich; Knochen 26, Namen und
  Eltern gleich, Offset/Bind max 0,0.
- **Netz:** 11.516 Punkte, 18.990 Dreiecke, Summe 1,0000, max 4 Einfluesse.
- **Kopf** (`kopf_out.txt`): 1.333/1.333 Lage, UV und Gewichte bit-gleich, 9 Normalen am Nahtrand anders (wie in den frueheren
  Laeufen). Kopf+Krallen gehaeutet in allen Clips/Bildern 0,00 mm. Kopfprobe FBX: 1.033 bit-gleich + 149 Nahtrand wie heute
  (max 20,9 mm wie bau4).
- **Krallen:** vorn 227/227 bit-gleich, hinten 228 = alt + (-0,070).
- **Boden** (`tiefst_out.txt`, Grundlinie neu am heutigen GLB, `werkzeug/pruef/spez/heute_tiefst.json`): 12 Nicht-Sitz-Clips
  0 Verstoesse.
  - Run HL-Kralle +0,74 (heute -2,58).
  - Death -0,18 (heute -1,42).
  - Dead 1,12 (heute 0,40, Band bis 1,40 ok).
  - Die 5 "Verstoesse" betreffen nur die alten Sitz-Clips: Netz -0,08 cm in Sit/SitDown/StandUp und Krallen 32,75 statt 39,72 cm
    hoch (liegen hoeher als der Boden). Diese Clips ersetzt Bau Sitzen; laut Auftrag erlaubt.
- **Dehnung** (`region_tabelle_out.txt`): 99,5 % je Clip max 2,49, max 3,51.
  - Achsel/Brust 3,51 (SwipeR; SwipeL 3,12).
  - Run max 2,90 (Leiste; heute 3,40 Achsel).
- **Falten liegend** (`falten_detail_out.txt`):
  - Achsel 142 + Ellbogen 112 = 254 (heute 87 + 49 = 136).
  - Die Zonen haben jetzt doppelt so viele Dreiecke (Ellbogen 535 statt 267, Knie 745 statt 18), weil das Bein schlanker ist und
    die Zonen nach Geometrie gezogen werden.
  - Flaechenanteil gestaucht: Ellbogen 20,8 % (heute 25,0 %), Achsel 11,7 % (10,9 %).
  - Alle gestauchten zusammen 688 (heute 704); sigma2 < 0,3: 102 (<= 200).
- **Ei:** 0,993.
- **Splitter** ohne Kantenfilter: max 34,7 in SwipeL Bild 18 (Achselrand, Dreieck 1,6 mm hoch; heute 26,7). Gefiltert unsichtbar,
  im Spiel ungeprueft.

### 4.4 Kragen (C3) mit dem ALTEN Sitz-Clip (`pruef_koerper/sitz/mess_sitz_k5B.txt`, Werkzeug wie Spez)
- **Spielkamera Bild 60:** hinter dem Kopf +21,3 cm (heute +21,4), neben dem Kopf +14,0 / -4,9 (heute +14,1 / -1,8).
- **Von vorn:** -12,9 / -29,0 (heute -15,9 / -26,3).
- **Lesart:** Mit der alten Haltung aendert das schmalere Netz den Kragen kaum, er ist der Buckel hinter dem tief haengenden Kopf
  (Buckel bleibt laut Spez).
- **Ruhe von vorn:** Kopf/Koerper 0,55 (heute 0,47).
- Die Spez-Werte (<= +2 cm) haengen an der neuen Haltung K2 (Bau Sitzen). R7 der Spez bleibt offen: Nacken tiefer geht nur, wenn
  der Kopfnaht-Schutz kleiner wird, und das kostet die Kopf-Bit-Gleichheit.

## 5. Bilder (`bilder/`, Ton, alt = NCBearTest heute | neu = Endstand; mit Vorlage nur lokal)
- `koerper_stehen_seite_ton.png`, `koerper_stehen_vorn_ton.png`, `koerper_stehen_hinten_ton.png`
- `koerper_stehen_spielwinkel_ton.png`:
  - Spielkamera seitlich az +90/-90 el 30 wie Kevins Bild, dazu az 50/130.
  - Neu: durchgehender Uebergang, keine Glocke, kein Sack ueber dem Bein. Alt: kurze Stiefel unter weitem Sack.
- `koerper_gehen_ton.png` (Walk 2, Walk 20, Walk Spielwinkel, Run 5): Bein schlank und stetig. Im Walk 20/Run 5 eine kleine scharfe
  Knitterfalte vorn am gebeugten Hinterknie (Ton; alt dort ein weicher Wulst).
- `koerper_sitzen_alt_ton.png`: ALTER Sitz-Clip auf dem neuen Netz. Hinterbeine weit gespreizt, Fuesse schweben (7,3 cm). Wird
  ersetzt.
- `koerper_aufrichten_ton.png`: schlanker, Beine gerade, Ei 0,993.
- `koerper_liegen_ton.png`, `koerper_spielgroesse_ton.png` (Spielgroesse, Baer ~250 px): unauffaellig, Beine laufen in den Rumpf.
- `koerper_hinterfuss_ton.png` (Sohle von unten | **Vorlage, nur lokal**) und `koerper_hinterfuss_seite_ton.png` (Seite, nah,
  hinten, ganz von unten).
  - Neu kurz und breit, Ferse rund.
  - **Ehrlich:** Von unten ist es im Ton noch eher ein abgerundetes Rechteck als das Oval der Vorlage.
  - Die Zehenballen (10 mm Relief) sieht man im Ton kaum; die Vorlage zeigt sie dunkel und prall.
  - Von hinten ist die Ferse unten noch flach, mit leichtem Dichtewechsel bei z 0,12 (Grenze Pfoten-/Rumpf-Verringerung).
  - Sohle dunkel, Fellkranz und Ballen-Farbe macht die Textur.
- Arbeitsbilder: `form/bild/*` (Schnitte, dichte Huelle), `form/k2blatt/*`, Einzelbilder `render/pose_alt|pose_neu|f*/`.

## 6. Kette wiederholen (~25 min; Gewichte 15 min CPU)
```
cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c
R=$PWD/bau_k5 bash werkzeug/lauf_2c.sh netz fbx kopfprobe formel gewichte glb   # GEWPAR-Vorgabe jetzt falte=100,falte_s=0.62,hoch=12
R=$PWD/bau_k5 bash werkzeug/pruef/messen_2c.sh k5B dump_final.txt               # alle Messungen gegen heute
python werkzeug/auftrag_pose.py bau_k5/dump_final.txt render/pose_neu render/pose_neu_auftrag.json neu
bash werkzeug/gpu_render.sh werkzeug/render_optik.py render/pose_neu_auftrag.json log/render_pose_neu.log
bash werkzeug/blaetter_koerper.sh neu
```
- **Form-Runden ohne Blender:**
  - Vorform-Huelle: `R=... bash werkzeug/lauf_2c.sh huelle`. Sie schreibt `netz/form2c_feld_2c.npz` (S0 = vor form_2c).
  - Dann `python werkzeug/form_probe.py VOR.npz AUS.npz form/form2c_block.py form/kopfnaht_schleife.npy`.
  - Dann `python werkzeug/mess2c.py AUS.npz NAME` und `werkzeug/auftrag_npz.py` + `gpu_render.sh` (~10 s).
- Der Block in `form/form2c_block.py` ist identisch mit dem in `baer_export_2c.py` (diff ohne Zeilenenden).
- Hinweis: `bau_k5/netz/gewichte_2c.npz` ist Variante A. Der Endstand B liegt in `bau_k5/netz/gewichte_2c_B.npz` und
  `glb_koerper/netz/gewichte_2c.npz`.

## 7. Offen / fuer die naechsten Bauer
1. **Achsel 3,51 (> 3,5 um 0,01) und Falten 254 (> 136):**
   - Formal gerissen. Die gestauchte Flaeche je Zone ist am Ellbogen kleiner als heute, an der Achsel +0,8 Punkte.
   - Gegenmittel laut Spez R1: Schulter-Halbbreite 0,40 -> 0,42 (in `_2C_RUMPF_S` x 0,20-0,30), kostet Rumpfbreite.
   - Staerkere Falten-Strafe hebt die Dehnung (Proben 3.3). Kevins Urteil im Spiel noetig.
2. **Nacken x 0,60 +1,6 cm ueber Soll:** Kopfnaht-Schutz (9-17,5 cm). Weniger Schutz = Kopf-Nahtrand nicht mehr bit-gleich.
3. **Bau Sitzen:** neues Netz `glb_koerper/42/media/models_X/WorldItems/NCBear.fbx` + `glb_koerper/netz/gewichte_2c.npz`.
   - Hinterfuss Ferse x -0,557, Sprunggelenk wie gehabt.
   - Neue Sitzpose am Netz loesen (Spez R5).
   - Bodenregel: Schenkel-Hinterkante liegt z 0,40-0,45 bis 2,4 cm weiter hinten als heute.
4. **Textur-Bauer:**
   - UV ist neu (alle 5 Dateien zusammen).
   - Sohlen-Layout `glb_koerper/netz/sohle_layout_2c.json`, Ballenplan `C2C_PLAN_H` (`baer_export_2c.py:1005`). Die
     Fersen-Abroll-Schwelle x -0,545 in `baer_textur_2c.py` passt noch (Ferse jetzt -0,557).
   - **Das Hochmodell-Rumpf ist NICHT verschmaelert** (nur der Fuss): form_2c wirkt am Spielnetz. Fuer Fell-Ansichten/Backen
     liegt das Feld `glb_koerper/netz/form2c_feld_2c.npz` (S0 -> S, Spielmeter) bereit, falls die Projektion an Schulter/Knie
     (bis 14 cm) daneben greift.
   - Body-PNG in `glb_koerper/` ist nur Platzhalter (alte Textur, passt nicht zum neuen UV).
5. **Gebiss-Bauer:** Kopf und Kopfrahmen unveraendert. Dreiecke 18.990 + 544 = ~19.534.
6. Knitterfalte am gebeugten Hinterknie (Walk 20, Run 5, Ton) und Splitter max 34,7 am Achselrand: im Spiel pruefen.
7. Behang: Ellbogen 4,5 cm und Bauch 3 cm sind gebaut, im Ton nur leicht sichtbar. Textur-Straehnen darueber macht der
   Textur-Bauer.
8. **Nicht gespielt.**

## 8. Dateien
- **Endstand:** `glb_koerper/42/media/models_X/Skinned/NCBear.glb` (89678e8f0c4065555c232ccaa707ccb1),
  `.../WorldItems/NCBear.fbx` (b440d693...), `.../textures/Body/NCBear.png` (Platzhalter), `glb_koerper/dump_koerper.txt`.
- **Netz:** `glb_koerper/netz/` (`netz_2c.npz`, `gewichte_2c.npz` = B, `gew_2c_formel.npz`, `lowpoly_2c.blend`, `lp_2c.npz`,
  `sohle_layout_2c.json`, `form2c_feld_2c.npz`).
- **Bau-Ordner:** `bau_r0`, `bau_k1..k5`, `bau_k4feld`, `bau_k5feld`, `bau_f14`, `bau_f15`; Logs `log/kette_*.txt`.
- **Werkzeuge:**
  - `werkzeug/lauf_2c.sh`, `mess2c.py`, `form_probe.py`, `spielraum.py`, `auftrag_npz.py`, `auftrag_pose.py`, `blatt_npz.py`,
    `blaetter_koerper.sh`, `glb_variante.sh`.
  - `render_optik.py` (Kopie, + npz-Netze, Licht von unten fuer Sohlenansichten), `gpu_render.sh`.
  - `pruef/` (Kopien der Pruefer-Werkzeuge + `messen_2c.sh`, `glocke_posen.py`, `beine_mass_2c.py`, `mess_sitz_2c.py`).
  - `kette/` (Kopien `_arbeit/baer_pfote/werkzeug`).
- **Messungen:** `pruef_koerper/k5B/` (Endstand), `k1`-`k5`, `heute/`, `sitz/`; `log/spielraum_12.txt`.
- **Vorlage-Ausschnitte (nur lokal):** `referenz/vorlage_fuss_links.png`, `vorlage_fuss_rechts.png`.
