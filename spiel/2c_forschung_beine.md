# Forschung Beine (Lauf baer-2c, 10.11.2026)

Nur Forschung: nichts am Modell, an der Test-Mod oder an den Original-Skripten geaendert, nichts committet.
**Statisch/offline gemessen und gerendert, nicht gespielt.** Alle Masse in Spielmetern bei Groesse 1,0 (Tier-Rahmen: x nach vorn,
y nach links, z nach oben; Schulterhoehe heute 1,158 m). Fotos aus dem Netz wurden nur angesehen und ausgemessen, nichts gespeichert.

## 0. Kurzfassung

- **Wo der Baumstamm sitzt:** z 0,10-0,20 ist das Bein eine Roehre (Vorderbein 18,8 -> 19,8 cm von der Seite, Hinterbein 23,4 -> 21,7;
  Aenderung -0,2 bis +1,9 cm je 5 cm Hoehe). Das Handgelenk ist mit 18,8 cm rund 1,4- bis 1,8-mal so dick wie beim echten Baeren
  (10,7-13,7 cm bei gleicher Schulterhoehe) -- das bleibt, weil die Pfoten fertig sind.
- **Wo die Glocke sitzt:** z 0,20-0,35 springt die Breite um +7,2 bis +9,6 cm je 5 cm (Vorderbein 19,8 -> 39,1 cm, Hinterbein
  21,7 -> 42,7 cm in 15 cm Hoehe). Echt sind es +1,5 bis +4,6 cm je 5 cm, gleichmaessig. Die Glocke ist vor allem ein Wulst nach VORN
  (Vorderbein-Vorderkante 0,404 -> 0,501; Hinterbein: Fleisch 14-17 cm vor dem Kniegelenk) und von vorn/hinten eine senkrechte
  Rumpfwand, die 13 cm je Seite in 15 cm Hoehe ueber das Bein kragt ("Hose im Stiefel").
- **Ursache im Bau:** baer-pfoten durfte nur unter z 0,36 formen (`SPEZ_PFOTEN.md:49`), `fix1_form` zieht den Rumpf darueber auf die
  baer-fell-Flaeche zurueck und legt nur einen Kegel z 0,18-0,342 dazwischen (`baer_export_pfote.py:86-92`, `:1482-1554`); die
  Metaball-Ketten der Beine sind gerade Saeulen neben den Knochen (`baer_quelle_pfote.py:1130`, `:1138`).
- **Vorschlag (Abschnitt 4.1):** gleichmaessige Verjuengung Ellbogen -> Handgelenk bzw. Knie -> Hock, Wulst vorn weg, Aussenwand
  schraeg statt senkrecht. Vorderbein von der Seite 19,5 / 21,5 / 24,4 / 27,0 / 29,3 / 31,5 cm bei z 0,15 / 0,20 / 0,25 / 0,30 /
  0,35 / 0,40 (Verhaeltnis oben : Handgelenk 1,6-1,7; echt 1,5-2,0). Als Attrappe gerendert: `forschung/beine/blatt_spiel.png`.
- **Geht ohne Clip-Aenderung:** die ganze Formaenderung an Vorderbein, Hinterbein-Vorderseite und Aussenwand; Fellbehang am Ellbogen
  (Bodenspielraum mind. 5,4 cm) und am Bauch (mind. 15,2 cm). **Geht nicht ohne Clips:** Oberschenkel-Hinterkante nach hinten
  (Spielraum nur 1,2 cm, Sitzen begrenzt; `baer_export_pfote.py:808-819`), Hinterfuesse weiter unter den Koerper, schmalerer Stand.
- **Zotteln:** Netz-Zotteln waren 1,4 cm tief im 4,2-cm-Raster -> Noppen (`_arbeit/baer_fell/bau_netz.md:121-126`). Vorschlag: wenige
  grosse Behang-Kanten als Teil der Huelle (4-6 cm am Ellbogen) plus Straehnen und Schattenband in der Textur; Alpha-Ausschneiden
  kann der Tier-Shader technisch (`animalEffect.frag:33-36`), praktisch nein (dunkle Raender, im Spiel ungeprueft).
- **Haushalt:** heute 19.426 von 20.000 Dreiecken (Reserve 574). Die Formaenderung kostet 0 (feste Dezimier-Ziele). Behang-Kanten
  etwa +200 bis +300, aus dem glatten Ruecken zu holen, damit die Reserve dem Maul (Zaehne, Zunge) bleibt.
- **Risiken an Grenzen:** Dehnung steht bei 2,59 von 2,6; mit der schlankeren Achsel stieg mein Vergleichsmass in den Prankenhieben
  um +0,2 (gleiche Gewichte). Falten im Liegen Achsel+Ellbogen 136 > 120 schon heute. Ei-Mass faellt 1,032 -> 0,999 (Grenze 0,95).

## 1. VORLAGE: echter Braunbaer

### 1.1 Quellen (nur angesehen)

| Nr | Bild / Text | Was man sieht |
|---|---|---|
| F1 | https://commons.wikimedia.org/wiki/File:Kamchatka_Brown_Bear_near_Dvuhyurtochnoe_on_2015-07-23.jpg | steht fast genau seitlich, Fell NASS (Beine wirken duenn) |
| F2 | https://commons.wikimedia.org/wiki/File:Eurasian_brown_bear_(Ursus_arctos_arctos)_female_1.jpg | 3/4 von vorn, trocken |
| F3 | https://commons.wikimedia.org/wiki/File:A_grizzly_walking_along_a_dry_creek_bed_(f9be3011-73cc-412a-8a0d-bf9306229860).jpg | geht, Seite, zotteliges trockenes Fell (1 px = 3,4 mm, Genauigkeit +-1,5 cm) |
| F4 | https://commons.wikimedia.org/wiki/File:A_grizzly_pauses_while_walking_along_a_creek_bed_in_Denali_(fc2334b8-e376-4034-b309-3dca64fc932a).jpg | 3/4 von hinten, derselbe Baer |
| F5 | https://commons.wikimedia.org/wiki/File:Brown_bear.jpg | grosses Maennchen, 3/4 von vorn, geht (nur grob) |
| T1 | https://www.nps.gov/articles/bear-identification.htm , https://www.umt.edu/grizzly-bear-recovery/grizzly-bears/identification.php | Buckel = Muskel ueber der Schulter, Ruecken faellt zum Hinterteil |
| T2 | `_arbeit/baer_pfote/forschung_referenz.md:66`, `:71`, `:135-160` (dort Shine u. a., https://sites.usc.edu/mcgowanlab/files/2023/02/JEB_Shine_GB_IDA_2017.pdf) | Ellbogen ~20 Grad nach innen, Pfote setzt auf der Aussenkante auf; Modell = grosses Maennchen |
| T3 | https://journals.viamedica.pl/folia_morphologica/article/download/FM.a2019.0125/49621 (Schienbein 267-269 mm), https://journals.sagepub.com/doi/10.1177/09596836251358723 (Oberarm 254-315 mm) | Knochenlaengen, schwache Belege |

Ehrlich: ein Foto genau von vorn oder genau von hinten im Stand habe ich nicht gefunden (nur 3/4-Sichten F2, F4, F5). Alle Zeilen
"von vorn/hinten" sind deshalb grob. Nicht brauchbar waren (angesehen): liegende/sitzende Baeren, Portraets, Baeren im Wasser, zu
kleine Baeren im Bild.

### 1.2 Proportionen (Verhaeltnis zur Schulterhoehe, umgerechnet auf 1,158 m)

| Mass | echt (Verhaeltnis) | echt bei Groesse 1,0 | heute im Modell | Quelle |
|---|---|---|---|---|
| Buckel ueber der Sattellinie | 5,7 % | 6,6 cm | Buckel 1,158, Ruecken bei x 0 1,100 = 5,8 cm; aber kein Sattel, der Ruecken faellt durch bis 1,033 | F1 |
| Hinterteil-Oberkante | 0,98 | 1,136 (Kamtschatka; Grizzly laut T1 tiefer) | 1,033 bei x -0,50 | F1, T1 |
| Bauch-Unterkante mit Behang | 33-34 % | 0,38-0,40 | 0,35-0,38 (Bauch), Brust 0,302 | F1, F3 |
| Achselfalte hinter dem Ellbogen | 39 % | 0,45 | Bein verschmilzt ab z 0,37-0,40; Ellbogengelenk fest bei 0,41 | F1 |
| Handgelenk, Breite von der Seite | 9-12 % | 10,7 (nass) - 13,7 cm (trocken) | **18,8 cm (16 %)**, fest (Pfote fertig) | F1, F3 |
| Unterarm oben : Handgelenk | 1,7 nass / 2,0 trocken / 1,5 | bei festem Handgelenk 18,8: 28-37 cm auf Ellbogenhoehe | 39,1 cm bei z 0,35 (2,08), aber als Sprung | F1, F3, F5 |
| Zunahme Vorderbein je 5 cm Hoehe | -- | +1,5 cm (nass), +2,3 bis +4,6 cm (trocken), gleichmaessig | -0,2 bis +1,9 (z 0,10-0,20), dann +7,2 bis +9,6 (z 0,20-0,30) | F1, F3 |
| Vorderbein von vorn : Brustbreite | je ~1/3, Spalt 0,5-0,7 Beinbreiten | -- | Bein 18-20 cm zu Brust 93 cm = 0,20; Spalt 25 cm = 1,3 Beinbreiten (z 0,20) | F2 |
| Brust zwischen den Beinen | haengt etwa bis Ellbogenhoehe | ~0,40 | 0,302 (11 cm unter dem Ellbogengelenk) | F2 |
| Hinterbein auf Hock-Hoehe, Seite | 11-16 % | 12,8 (nass) - 19 cm (trocken) | 21,7 cm (z 0,20), fest bis z 0,115 | F1, F3 |
| Hinterbein auf Kniehoehe : Hock | 2,35 nass / 1,6 trocken | 30-31 cm bei z 0,33-0,42 | 42,7 cm schon bei z 0,35 | F1, F3 |
| Zunahme Hinterbein je 5 cm Hoehe | -- | +2,1 bis +3 cm | +7,7 bis +9,6 (z 0,20-0,30) | F1, F3 |
| Hinterkante hinter der Ferse | -- | 4 / 8 / 11 / 18 / 26 / 36 cm bei z 0,20 / 0,27 / 0,345 / 0,40 / 0,48 / 0,77 | 0 cm bis z 0,45 (senkrecht bei x -0,60), dann 3 / 7 / 10 / 11,6 cm bei z 0,50 / 0,55 / 0,60 / 0,70 | F1 |
| Hautsegel Knie -> Bauch (Kniefalte) | sichtbar, hohl | -- | fehlt: stattdessen Fleisch 14-17 cm vor dem Kniegelenk | F3 |
| Rumpfbreite : Schulterhoehe | ~0,5-0,65 (grob, 3/4-Sicht) | ~0,58-0,75 m | **0,93 m (0,80)** | F4 |
| Hock-Breite : Rumpfbreite (hinten) | 0,28 | -- | 0,20-0,22 | F4 |
| Spalt zwischen den Hinterbeinen : Rumpfbreite | 0,12 | -- | 0,32 (29 cm bei z 0,20) | F4 |
| Aussenkontur Huefte -> Knoechel (hinten) | faellt stetig nach innen, keine Stufe | -- | senkrechte Wand z 0,35-0,75, dann Stufe | F4 |
| Rumpflaenge Hinterteil-Nase : Schulterhoehe | 1,84 | 2,13 m | 1,69 (1,96 m) | F3 |
| Oberschenkel : Unterschenkel (Knochen) | etwa 1,08 (schwach) | -- | 30,1 : 33,6 cm = 0,90 (Knochen fest) | T3 |
| Fell an den Beinen | dunkler als der Rumpf, Behang hinter dem Unterarm | -- | Textur-Sache | F3, F5 |

Lesart: Der echte Baer hat **keine** Stelle, an der das Bein ueber kurze Strecke wieder dick wird. Vorderbein: dicke, glatt
zulaufende Saeule, am breitesten am Ellbogenbehang (F2, F5). Hinterbein: breite Keule, die nach hinten ueber die Ferse haengt (F1).
Zwei Dinge am Modell sind groesser als die Glocke selbst und in diesem Lauf nicht frei: das dicke Handgelenk (Pfoten fertig) und
der sehr breite Rumpf (0,93 m; Ei-Form und Fell-Errungenschaften sollen bleiben).

### 1.3 Eigene Skizzen (selbst gezeichnet, PIL, Massstab 500 px je Meter wie die Ton-Bilder)

- `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung/beine/skizze_seite.png`
- `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung/beine/skizze_vorn.png`
- `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung/beine/skizze_hinten.png`

Grau = Umriss des heutigen Netzes (Ruhelage, aus dem Dump gerastert), hellrot = faellt im Vorschlag weg, rote Linie = Vorschlag,
schwarz = Knochen (fest), blau = Masse des echten Baeren aus F1-F4 (durchgezogen trocken, gestrichelt nass), orange = Fellbehang.
Angesehen: alle drei. Werkzeug `werkzeug/beine/skizze.py`.

## 2. BESTAND: wie die Beine heute gemacht sind

### 2.1 Bau (Datei:Zeile)

- **Hochmodell** `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_quelle_pfote.py`: Metaball-Ketten `:1119-1145`. Vorderbein
  `chain((0.30, s*0.29, 0.78), (0.33, s*0.32, 0.40), 0.30, 0.235, 3)` "lang und saeulig" (`:1130`): eine gerade Saeule bei y
  0,29-0,32 und x 0,30-0,33 -- 6-8 cm ausserhalb und bis 10 cm vor den Knochen; der Zickzack Schulter 0,29 -> Ellbogen 0,23 ->
  Handgelenk 0,32 kommt nicht vor. Hinterbein `chain((-0.72, s*0.33, 0.72), (-0.57, s*0.36, 0.42), 0.35, 0.26, 3)` "maechtige
  Keule" (`:1138`): liegt 22-26 cm hinter der Linie Huefte-Knie. Buckel `ball(0.33, 0, 1.03, 0.34)` (`:1123-1125`). Pfoten-Tabellen
  `PfBein` `:946-951`, `:963-968`, Kugeln `PF_KUGELN` `:1089-1092`, Schwelle 0,62 (`:1070`).
- **Fell-Huelle** `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_export_pfote.py`, `huelle_bauen` `:723-835`: Felldicke
  `dlim_k = 0.112 - 0.022 * koerper_bein + ...` (`:760-761`), Knieband `:805-807` ("die Felldicke wechselt hier von der Pfote
  (2-4 cm) zum Rumpf (7 cm)") -- genau dieser Wechsel 2-4 -> 7 cm in `PF_UEB = (0.28, 0.35)` (`:69`) ist die Glocke im Fell.
  Hinterkante Oberschenkel/Hock gedeckelt `:808-819` (Sitzen, siehe 4.2).
- **`form_fell`** `:844-869`: Schulter +4,0 cm (`FORM_SCHULTER`, `:151`, Maske z 0,38-0,98), Flanke -3,2 cm, Gesaessfalte 4,0 cm;
  das ist der Ei-Fix aus baer-fell (`_arbeit/baer_fell/fix_bericht.md:27`).
- **`fix1_form`** `:1473-1594`: Kegel je Bein z 0,18-0,342 (`FIX1_KEGEL`, `:86`; "ueber ~0,345 waechst das Bein in den Bauch"
  `:1485`; `f = t*t*(3-2t)` `:1516`), darueber wird der Rumpf auf die baer-fell-Flaeche gezogen (`:1530-1554`, `FIX1_ALT`).
  Folge der Regel `_arbeit/baer_pfote/SPEZ_PFOTEN.md:49` ("Oberhalb z 0,36 bleibt die Form wie heute ... p95 <= 0,5 cm").
- **Gewichte** `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_kampf_pfote.py`, `gewichte_eigen` `:1722`: Oberarm/Oberschenkel
  blenden erst z 0,32-0,50 ein (`:1733-1734`), Fuss bis z 0,175 (`:1735`). Im fertigen GLB: UpperArm hoechstens 0,50 (Schulter
  aussen z 0,45-0,60 nur 0,15-0,19, Spine1 0,62-0,76); Thigh hoechstens 0,73, nur 39 Punkte >= 0,5. Dominante Dreiecke: L/R UpperArm
  13/16, L/R Thigh 97/100 -- **Oberarm und Oberschenkel bewegen fast keine Haut**, das Bein "haengt" am Unterarm/Unterschenkel.

### 2.2 Knochen (fest; Ruhelage aus den Offset-Matrizen des Dumps, linke Seite)

| Gelenk | x | y | z | Knochen bis zum naechsten Gelenk |
|---|---|---|---|---|
| Schulter (UpperArm) | 0,290 | 0,225 | 0,720 | Oberarm 31,6 cm, -11 Grad |
| Ellbogen (Forearm) | 0,230 | 0,240 | 0,410 | Unterarm 32,3 cm, +16 Grad |
| Handgelenk (Hand) | 0,320 | 0,230 | 0,100 | -- |
| Huefte (Thigh) | -0,460 | 0,250 | 0,690 | Oberschenkel 30,1 cm, +21 Grad |
| Knie (Calf) | -0,350 | 0,262 | 0,410 | Unterschenkel 33,6 cm, -23 Grad |
| Hock (Foot) | -0,480 | 0,247 | 0,100 | Ballen (-0,250, 0,240, 0,045) |

(Hinterbein-Konstanten auch `baer_kampf_pfote.py:94`.) Netz: 11.853 Punkte, 19.426 Dreiecke, 26 Knochen; x -0,800..1,157,
y -0,463..0,467, z 0..1,159.

### 2.3 Querschnitte am heutigen GLB (Importer-Dump `forschung/beine/dump/heute.txt`)

Waagerechte Schnitte in Ruhe, Breite von der Seite (x) x von vorn (y), cm:

| z | Vorderbein | Hinterbein | Befund |
|---|---|---|---|
| 0,05 | 28,6 x 19,4 | 36,4 x 18,4 | Pfote |
| 0,10 | 18,8 x 18,3 | 28,6 x 18,1 | Gelenk |
| 0,15 | 18,7 x 18,5 | 23,4 x 18,1 | **Roehre** |
| 0,20 | 19,8 x 20,4 | 21,7 x 20,2 | **Roehre** |
| 0,25 | 27,0 x 27,9 | 29,4 x 27,2 | **Glocke** (+7,2 / +7,7 cm) |
| 0,30 | 35,7 x 36,8 | 39,0 x 35,6 | **Glocke** (+8,7 / +9,6 cm) |
| 0,35 | 39,1 x 40,6 | 42,7 x 38,7 | laeuft in den Rumpf |
| ab 0,40 | verschmolzen | verschmolzen | Kasten: Gesamtbreite 0,906 (z 0,35) -> 0,93 (z 0,50-0,70) |

Kanten in Ruhe (links): Vorderbein-Vorderkante x 0,404 (z 0,15-0,20) -> 0,441 -> 0,485 -> 0,501 (z 0,25 / 0,30 / 0,35);
Hinterkante 0,206 -> 0,171 -> 0,128 -> 0,110. Aussenkante y 0,328 (z 0,20) -> 0,370 -> 0,420 -> 0,440 -> 0,465 (z 0,50), Innenkante
0,124 -> 0,091 -> 0,052 -> 0,034 (Spalt zwischen den Vorderbeinen 25 cm -> 7 cm). Hinterbein: Hinterkante senkrecht x -0,609 bis
-0,601 von z 0,20 bis 0,40, erst ab z 0,50 nach hinten (-0,667, -0,705, -0,738, -0,750); Vorderkante -0,392 (z 0,20) -> -0,31 ->
-0,214 -> -0,175 (Kniegelenk bei x -0,35!). Aussen 0,348 -> 0,388 -> 0,435 -> 0,453; innen 0,146 -> 0,116 -> 0,079 -> 0,066.

Schnitte senkrecht zum Knochen (Station in cm ab dem oberen Gelenk, Seite / vorn):

| Lage | Unterarm | Unterschenkel |
|---|---|---|
| Stehen/Ruhe | 10: 37,3/40,0; 15: 33,5/34,1; 20: 26,1/24,1; 25: 19,4/19,2; 30: 18,2/18,1 | 10: 35,7/38,1; 15: 29,4/33,6; 20: 24,2/26,9; 25: 22,8/20,8 |
| Gang A (Walk Bild 2) | 5: 30,0/40,0; 10: 25,9/37,1; 15: 23,8/29,9; 20: 21,7/22,3; 25: 18,6/19,0; 30: 18,8/18,2 | 10: 39,0/38,1; 15: 31,2/33,2; 20: 25,6/26,2; 25: 24,4/20,5 |
| Gang B (Walk Bild 20) | 20: 47,9/37,1; 25: 22,3/19,5; 30: 18,4/18,2 | 30: 27,7/18,2 |

Auch im Gang: unten 10 cm lang gleich dick (18-19 cm), dann in 10 cm auf das Doppelte. In Gang B (Bein nach hinten) reicht die
Glocke bis Station 20 (47,9 cm). Oberarm und Oberschenkel ergeben in keinem Bild eine freie Schleife (stecken ganz im Rumpf).
Alle Zahlen: `forschung/beine/log/beine_mass.txt`.

Zonen-Bild (blau = Roehre 1.082 Dreiecke z 0,10-0,20, rot = Glocke 2.470 Dreiecke z 0,20-0,37, gelb = Kasten 1.728 Dreiecke
|y| > 0,36, z 0,37-0,82): `forschung/beine/render/heute_zonen_seite.png`, `heute_zonen_vorn.png`, `heute_zonen_hinten.png`,
`heute_zonen_spiel_vl.png`, `heute_zonen_spiel_hl.png`. Ton: `heute_ton_*.png`, Gang `gangA_ton_*.png`, `gangB_ton_*.png`.

### 2.4 Zonen an der Dehn- oder Faltgrenze heute

| Zone | Stand | Grenze | Beleg |
|---|---|---|---|
| Dehnung gesamt (99,5 % je Clip) | 2,59 | 2,6 | `_arbeit/baer_pfote/gegen_bericht.md:53`, `:97` ("nur 0,01 unter der Grenze") |
| Dehnung Achsel/Brust | 3,26 (SwipeL) | 3,5 | `gegen_bericht.md:53`, `_arbeit/baer_pfote/fix1_bericht.md:61` |
| Dehnung max | 3,40 | 4,0 | `gegen_bericht.md:53` |
| Falten im Liegen, Achsel + Ellbogen | 87 + 49 = 136 Dreiecke | 120 (baer-fell 88) | `gegen_bericht.md:56`, `:114`; `_arbeit/baer_pfote/pruef_technik.md:145-154` |
| Falten Knie | 14 | wie baer-fell | `fix1_bericht.md:23` |
| Splitter | max 26,65 (SitDown Bild 24, Hinterschenkel aussen) | -- | `gegen_bericht.md:161` |
| Falten-Strafe hoeher | `falte=120` ergab Dehnung 2,64 > 2,6 | -- | `gegen_bericht.md:63`, `fix1_bericht.md:39` |
| Kegel am Bein | "steil (Kevin urteilen lassen)" | -- | `fix1_bericht.md:89` |

Also: Achsel, Ellbogen und Hinterschenkel aussen -- genau die Zonen, die der Vorschlag anfasst -- haben heute keine Reserve.

## 3. ZOTTELN: Fellbehang ohne Noppen

Was scheiterte (baer-fell): `BAER_ZOTTELN=0.014`, spitze Zotteln 1,4 cm tief im Abstand 4,2 cm an Ruecken, Bauch, Vorderbein-
Hinterkante, Hinterteil. Nach dem Verringern Reihen kleiner Pyramiden; Rumpf-Knick > 20 Grad 21,3 % statt 6,9 %, Umklapper 13
(`_arbeit/baer_fell/bau_netz.md:121-126`, Bild `_arbeit/baer_fell/netz/bild_zotteln.png`). Grund: Zottel kleiner als die
Dreieckskante nach dem Verringern (~3-4 cm) -- das Netz kann sie nicht tragen.

| Weg | Was | Dreiecke | Urteil |
|---|---|---|---|
| A. Behang als Umriss der Huelle | Vor dem Verringern eine durchgehende Kante in die Huelle formen: Ellbogenbehang 4-6 cm tief, laeuft bis z 0,15 auf 0 aus; Bauchkante 3-4 cm; Kniefalte als hohles Hautsegel Knie -> Bauch; "Hose" an der Schenkel-Hinterkante hoechstens 1-2 cm (4.2). Eine Kante, viele cm lang -> ueberlebt das Verringern | etwa +200 bis +300 (Kantenschleifen), sonst 0 | **empfohlen** |
| B. Textur | Haengende Straehnen-Buendel 3-6 Texel (1-2 cm) quer ueber die Behang-Kante, darunter ein dunkles Schattenband, Beine insgesamt dunkler als der Rumpf (F3, F5). Texeldichte `baer/spiel/fell_forschung_engine.md:57-65` | 0 | **empfohlen**, zusammen mit A |
| C. Wenige grosse Lappen | Geschlossene Keile >= 6 cm tief, 10-18 cm lang, schief, nach hinten-unten; 2 je Ellbogen, 3 je Schenkel, ~5 am Bauch = 15-20 Lappen | 150-240 (8-12 je Lappen) | nur als Probe; braucht eigene UV-Inseln, Back-Quelle und Gewichte je Lappen; Faltenzone Ellbogen (136 > 120) |
| D. Alpha-Ausschneiden | Fellkarten mit Loechern | wenige | technisch ja, praktisch nein |

Zu D, statisch belegt: Vanilla `C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/shaders/animalEffect.frag:33-36`
(`vec4 texSample = texture2D(Texture, texCoords); if(texSample.w < 0.01) ... discard;`) und `:78`
(`vec4(col * vertColour, Alpha * texSample.w)`) -- von mir in diesem Lauf nachgelesen. Aus der frueheren Forschung
`baer/spiel/fell_forschung_engine.md:73-116`, von mir NICHT neu geprueft: Textur laeuft zweimal durch den TextureCombiner (am
Schirm rgb x a^3 -> dunkle Raender), Rueckseiten werden weggeschnitten (nur `cullFace = None` am Muendungsfeuer), keine Sortierung,
kein Vanilla-Tier mit Alpha (`:54`), Vanilla-Haare sind feste Netze. **Im Spiel ungeprueft**; nur auf Kevins Wort als Probe.

Bodenspielraum fuer Behang (4.2): Ellbogen mind. 5,4 cm, Unterarm-Hinterkante 8,4 cm, Bauch 15,2 cm, Brust 20,9 cm ->
A geht dort ohne Clip-Aenderung. Schenkel-Hinterkante mind. 1,2 cm -> "Hose" praktisch nur ueber Textur.

## 4. MACHBARKEIT + HAUSHALT

### 4.1 Vorschlag in Zahlen (linke Seite, Ruhelage; "heute -> Vorschlag")

Vorderbein:

| z | Vorderkante x | Hinterkante x | Breite Seite | Aussen y | Innen y | Breite vorn |
|---|---|---|---|---|---|---|
| 0,12 | 0,412 (bleibt) | 0,224 (bleibt) | 18,8 | 0,312 | 0,128 | 18,4 |
| 0,15 | 0,404 -> 0,406 | 0,217 -> 0,211 | 18,7 -> 19,5 | 0,316 -> 0,318 | 0,131 -> 0,128 | 18,5 -> 19,0 |
| 0,20 | 0,404 -> 0,405 | 0,206 -> 0,190 | 19,8 -> 21,5 | 0,328 -> 0,330 | 0,124 -> 0,120 | 20,4 -> 21,0 |
| 0,25 | 0,441 -> 0,404 | 0,171 -> 0,160 | 27,0 -> 24,4 | 0,370 -> 0,344 | 0,091 -> 0,112 | 27,9 -> 23,2 |
| 0,30 | 0,485 -> 0,405 | 0,128 -> 0,135 | 35,7 -> 27,0 | 0,420 -> 0,358 | 0,052 -> 0,100 | 36,8 -> 25,8 |
| 0,35 | 0,501 -> 0,408 | 0,110 -> 0,115 | 39,1 -> 29,3 | 0,440 -> 0,372 | 0,034 -> 0,082 | 40,6 -> 29,0 |
| 0,40 | 0,500 -> 0,415 | 0,100 | -> 31,5 | 0,447 -> 0,386 | -> 0,055 | -> 33 |
| 0,45-0,60 | 0,435 / 0,465 / 0,490 / heute | Behang | -- | 0,400 / 0,414 / 0,428 / 0,441 | -- | -- |

Hinterbein:

| z | Hinterkante x | Vorderkante x | Breite Seite | Aussen y | Innen y | Breite hinten |
|---|---|---|---|---|---|---|
| 0,20 | -0,609 (bleibt) | -0,392 -> -0,390 | 21,7 -> 21,9 | 0,348 | 0,146 | 20,2 |
| 0,25 | -0,605 (bleibt) | -0,311 -> -0,364 | 29,4 -> 24,1 | 0,388 -> 0,361 | 0,116 -> 0,135 | 27,2 -> 22,6 |
| 0,30 | -0,604 (bleibt) | -0,214 -> -0,340 | 39,0 -> 26,4 | 0,435 -> 0,375 | 0,079 -> 0,120 | 35,6 -> 25,5 |
| 0,35 | -0,602 (bleibt) | -0,175 -> -0,317 | 42,7 -> 28,5 | 0,453 -> 0,388 | 0,066 -> 0,100 | 38,7 -> 28,8 |
| 0,40 | -0,603 (bleibt) | -> -0,288, darueber Kniefalte | -> 31,5 | 0,450 -> 0,402 | -> 0,070 | -> 33 |
| 0,45-0,60 | bleibt (Sitzen) | -0,235 / -0,185 / heute | -- | 0,415 / 0,428 / 0,442 / 0,455 | -- | -- |

Zusaetzlich, nicht in der Attrappe: Brust zwischen den Vorderbeinen von 0,302 auf etwa 0,34-0,36 heben (echt etwa Ellbogenhoehe,
F2), Behang-Kanten aus Abschnitt 3, Schulter/Oberarm als sichtbare Muskelmasse ueber dem Ellbogen (schraeg nach hinten-oben zum
Buckel, der mit 5,8 cm ueber dem Ruecken schon passt).

**Attrappe** (nur zur Anschauung: Punkte des heutigen Netzes nach diesen Tabellen verschoben, gleiche Gewichte, kein Bau, nicht
fuer die Mod; `werkzeug/beine/attrappe.py`, Dump `forschung/beine/dump/attrappe.txt`, Protokoll `forschung/beine/log/attrappe.txt`):
3.433 von 9.719 Punkten verschoben, groesste Verschiebung 13,3 cm; erreichte Schnitte Vorderbein Seite 19,3 / 20,0 / 24,0 / 28,9 /
30,3 cm und Hinterbein 23,3 / 20,9 / 22,7 / 28,3 / 30,4 cm bei z 0,15 / 0,20 / 0,25 / 0,30 / 0,35; Gesamtbreite z 0,30 0,872 ->
0,770, z 0,50 0,927 -> 0,853. Oberflaeche 5,780 -> 5,537 m2. 7 umgeklappte Dreiecke (Schaden der Attrappe, kein Befund am Modell).

**Bilder heute neben Vorschlag und Skizze** (alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung/beine/`):

| Blatt | Inhalt | angesehen |
|---|---|---|
| `blatt_seite.png` | Ton heute / Ton Attrappe / Skizze, Seite | ja |
| `blatt_vorn.png` | Ton heute / Ton Attrappe / Skizze, vorn | ja |
| `blatt_hinten.png` | Ton heute / Ton Attrappe / Skizze, hinten | ja |
| `blatt_spiel.png` | Spielwinkel vorn links und hinten links, heute / Attrappe | ja |
| `blatt_gang.png` | Gang A und B von der Seite, heute / Attrappe | ja |
| `blatt_gang_spiel.png` | Gang A und B im Spielwinkel, heute / Attrappe | ja: Gang A Vorderbein ohne Wulst, aber Knitter hinter dem Ellbogen; Gang B Hinterbein schlanker, Knitter in der Kniekehle; der Rumpf bleibt in beiden sehr breit |

Was ich auf den Blaettern sehe: Von der Seite ist der Wulst vor Unterarm und Knie weg, die Beine laufen sichtbar zu. Im Spielwinkel
wirkt das Vorderbein wie ein Arm mit Ellbogen statt wie ein Pfosten unter einem Kasten; von hinten ist die "Hose im Stiefel"
deutlich kleiner, aber nicht weg (Hinterkante und Stand bleiben). **Ehrlich:** unten bleibt das Bein dick (Handgelenk 18,8 cm),
ein schlanker echter Baerenunterarm wird es ohne Eingriff an den Pfoten nicht. In Gang B knittert die Attrappe vor dem Knie und am
Ellbogen (alte Gewichte auf neuer Form) -- dort braucht der Bau die Kniefalte und neu gerechnete Gewichte.

### 4.2 Was geht ohne Clip-Aenderung (Spielraum-Rechnung, `forschung/beine/log/attrappe.txt`)

Mass: wie weit darf ein Punkt entlang seiner Normalen nach aussen, bis er in irgendeinem Bild eines der 15 Clips tiefer laege als
der heute tiefste Punkt dieses Clips (nur die Boden-Regel; Dehnung und Falten extra).

| Zone | min / 5 % / Median (cm) | begrenzender Clip | Folge |
|---|---|---|---|
| Schenkel hinten (x < -0,55, z 0,24-0,60) | 1,2 / 2,0 / 4,3 | NCBear_Sit, StandUp | Hinterkante nach hinten: **nein** (Vorschlag waere bis +5,4 cm) |
| Hock/Ferse hinten (z 0,12-0,24) | 0,0 / 0,5 / 4,4 | StandUp, SitDown | nichts anbauen |
| Ellbogen hinten (z 0,25-0,50) | 5,4 / 7,3 / 30,0 | DeerStag_Death, Dead | Behang 4-6 cm: ja |
| Unterarm hinten (z 0,12-0,25) | 8,4 / 9,8 / 13,8 | DeerStag_Death | ja |
| Bauch unten | 15,2 / 20,8 / 27,9 | Death, Slam | ja |
| Brust unten | 20,9 / 23,7 / 30,8 | Slam | ja |
| Aussenwand Schulter | 2,1 / 2,9 / 81,9 | DeerStag_Dead (liegt auf der Seite) | nur nach innen formen (Vorschlag tut das) |
| Aussenwand Schenkel | 4,7 / 5,6 / 20,7 | DeerStag_Dead | nur nach innen formen |

Bestaetigt die Notiz im Code (`baer_export_pfote.py:808-819`: "mit der alten Huelle saesse das Hinterteil im Sitzen 2,3 cm im
Boden", 4 mm Rand an der Kniekehle).

Pruefung der Attrappe gegen die festen Regeln:

| Regel | heute | Attrappe | Urteil |
|---|---|---|---|
| Kein Clip tiefer im Boden | je Clip siehe Protokoll (Run -2,98 cm, Walk -2,40, Death -1,42, Dead +0,40) | in allen 15 Clips gleich | haelt |
| Liegehoehe Death/Dead | Dead tiefster Punkt +0,40 cm | +0,40 cm | haelt |
| Ei-Mass (Rear 1,3 s, Formel aus `_arbeit/baer_fell/fix/werkzeug/ei.py`) | 1,032 | 0,999 | haelt (Grenze 0,95, `SPEZ_PFOTEN.md:247`), aber 0,033 weniger: die schraege Wand schneidet in `FORM_SCHULTER`; beim Bau nachmessen, notfalls Wand erst unter z 0,50 schraeg |
| Dehnung 99,5 % (mein Kantenmass, NICHT das des Pruefers; nur Vergleich) | SwipeR 2,48, SwipeL 2,52, Rear 2,63, StandUp 1,76, Sit 1,75 | 2,70 / 2,76 / 2,65 / 1,91 / 1,85 | **Warnung**: schlankere Achsel dehnt in den Hieben um +0,2 mehr; der Pruefer steht bei 2,59 von 2,6 |
| Pfoten unter dem Gelenk | -- | Punkte unter z 0,115 unverschoben | haelt |
| Kopf, Clips, Knochen | -- | unberuehrt (nur Rumpf/Bein-Punkte bis x 0,66, z 0,80) | haelt |

Ohne Clip-Aenderung machbar: (a) Wulst vorn an Vorder- und Hinterbein weg, (b) gleichmaessige Verjuengung nach 4.1, (c) Aussenwand
schraeg, (d) Kniefalte, (e) Behang am Ellbogen und Bauch als Umriss, (f) Beine dunkler und Straehnen in der Textur, (g) mehr
Gewicht auf Oberarm/Oberschenkel -- Gewichte sind kein Clip, aber jede Aenderung haengt an der Dehngrenze (2,59/2,6) und an den
Falten (136/120); nur als Versuch in der Form-Runde.

**Vorschlaege fuer die Clip-Runde** (in diesem Lauf nicht machbar):
1. Oberschenkel-Hinterkante 2-5 cm weiter hinten (echt 18-26 cm hinter der Ferse bei z 0,40-0,48; heute 0) -- braucht ein anderes
   Sitzen (Sit, SitDown, StandUp).
2. Hinterfuesse 10-15 cm weiter unter den Koerper (echt haengt das Hinterteil 36 cm hinter der Ferse, heute 11,6 cm).
3. Schmalerer Stand: Handgelenk-Mitten heute 46 cm auseinander, Spalt zwischen den Hinterbeinen 29 cm (echt etwa 0,12 Rumpfbreiten).
4. Oberschenkel laenger als der Unterschenkel (heute 30,1 zu 33,6 cm; echt eher umgekehrt, schwacher Beleg T3).
5. Ausserhalb der Beine, nur als Befund: Rumpf 0,93 m breit (echt grob 0,6-0,75 m), Hinterteil 10 cm tiefer als bei F1.

### 4.3 Welche Kettenschritte neu laufen muessen

Reihenfolge der baer-pfoten-Kette (Kopien der Skripte nach `_arbeit/baer_2c/werkzeug/`, Originale nicht aendern):

1. Hochmodell: Bein-Ketten `baer_quelle_pfote.py:1130`, `:1138` an die Knochen legen (Schulter -> Ellbogen -> Handgelenk bzw.
   Huefte -> Knie -> Hock statt gerader Saeule), `PfBein`-Tabellen oben anschliessen -> Fell-Ansichten (GPU).
2. `netz`: `huelle_bauen` (`PF_UEB`, `PF_BAND`, `dlim_k`: Felldicke gleitend ueber z 0,15-0,45 statt 0,28-0,35), `form_fell`
   (Masken Schulter/Flanke, neue Behang-Kanten), `fix1_form` (`FIX1_KEGEL`, `FIX1_KLEMM`, `alt_huelle.npz`: die Regel "ueber z 0,36
   wie baer-fell" muss fuer die Beinzonen fallen; Hinterkante `PF_HINTEN_HEUTE` `:72` bleibt), Verringern, Sohlen, UV.
3. `fbx` -> `kopfprobe` (Kopf-Aussenform bit-gleich pruefen) -> `formel`-Gewichte -> `gewichte` (Optimierung 12-15 min CPU) -> `glb`
   + Dump + Pruefer -> `zwischen`/`karten` -> Textur-Ansichten (GPU) -> Backen -> Body/GLB -> `deer`.

Ganze Kette etwa 35-40 min; Form-Runden mit Formel-Gewichten und Ton-Bildern etwa 5 min. Unveraendert bleiben: alle 15 Clips,
Knochen, Pfoten unter z 0,115, Krallen, Kopf-Aussenform.

### 4.4 Dreiecks-Haushalt (Grenze 20.000, heute 19.426, Reserve 574)

| Region | heute | Vorschlag | Bemerkung |
|---|---|---|---|
| Kopf + Kiefer | 2.543 | wie die Maul-Aufgabe es braucht | Aussenform fest |
| Hals | 969 | 969 | -- |
| Rumpf (Pelvis 3.855, Spine 1.171, Spine1 2.454) | 7.480 | etwa 7.200 | glatter Ruecken/Hinterteil -250 bis -300 |
| Schwanz | 142 | 142 | -- |
| Vorderbeine: Pfote z < 0,12 | 2.569 | 2.569 | fest |
| Vorderbeine: Gelenk 0,12-0,20 | 408 | 408 | Nahtkante |
| Vorderbeine: 0,20-0,36 (Glocke) | 1.061 | etwa 1.000 | kleinere Flaeche |
| Vorderbeine: 0,36-0,50 + Ellbogenbehang | 100 | etwa 260 | Kantenschleifen fuer den Behang |
| Hinterbeine: Pfote z < 0,12 | 2.978 | 2.978 | fest |
| Hinterbeine: Gelenk 0,12-0,20 | 437 | 437 | Nahtkante |
| Hinterbeine: 0,20-0,36 (Glocke) | 1.078 | etwa 1.000 | kleinere Flaeche |
| Hinterbeine: 0,36-0,75 + Kniefalte | 311 | etwa 460 | Kniefalte, Schenkel |
| **Summe** | **19.426** | **etwa 19.430** | Beine dreiecks-neutral |

(Summen nach dominantem Knochen bzw. Hoehenzone, `forschung/beine/log/beine_mass.txt`; Krallen 832 stecken in den Pfoten.)
Die Verteilung laeuft ueber die Zielzahlen der Dezimierung (`baer_export_pfote.py:77-78` `PF_ZIEL = 4300`, `PF_RUMPF_REST = 10600`,
`:139` `RUMPF_ZIEL = 14500`), nicht von Hand; eine reine Formaenderung kostet deshalb 0. Empfehlung: Beine neutral halten und die
Reserve von 574 dem Maul lassen; Lappen-Probe (Weg C, 150-240) nur, wenn danach noch Platz ist.

### 4.5 Offene Punkte / Unsicherheit

- Alle Foto-Masse +-1,5 cm und von Fell-Zustand abhaengig (nass F1, trocken F3); von vorn/hinten nur 3/4-Sichten.
- Die Attrappe zeigt nur die Form, nicht Gewichte, Textur oder Falten des echten Baus.
- Mein Dehnungs-Vergleich ist nicht das Mass des Pruefers; er zeigt nur die Richtung (Achsel wird knapper).
- Nichts davon ist im Spiel gesehen.

## 5. Dateien

- Bericht: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung_beine.md`
- Bilder: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/forschung/beine/` (`skizze_seite.png`, `skizze_vorn.png`,
  `skizze_hinten.png`, `blatt_seite.png`, `blatt_vorn.png`, `blatt_hinten.png`, `blatt_spiel.png`, `blatt_gang.png`,
  `blatt_gang_spiel.png`; Einzelbilder `render/heute_*.png`, `render/gangA_*.png`, `render/gangB_*.png`, `render/attrappe_*.png`)
- Messprotokolle: `.../forschung/beine/log/beine_mass.txt`, `.../forschung/beine/log/attrappe.txt`
- Dumps: `.../forschung/beine/dump/heute.txt` (heutiges GLB), `.../forschung/beine/dump/attrappe.txt` (nur Anschauung)
- Werkzeuge: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/werkzeug/beine/` (`beine_mass.py`, `attrappe.py`, `skizze.py`,
  `zonen_feld.py`, `dumpread.py`, `render_optik.py`, `gpu_render.sh`)
