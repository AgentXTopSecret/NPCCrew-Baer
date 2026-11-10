# Lauf baer-2c: Bau Sitzen (10.11.2026, Neustart 05:14-05:50)

Blender 5.2.3, JDK 25, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
- Nichts in die Test-Mod NCBearTest geschrieben (GLB dort weiter 5066fa67), nichts nach NPC Crew, nichts committet.
- Originale `*_pfote.py` unveraendert (MD5 9ae68692 / 402f9f5b / 14fceba9 / 380f259f / a14a4e1b). Von den `*_2c.py` habe ich nur
  `baer_kampf_2c.py` geaendert (quelle/export/gewichte/textur_2c: MD5 72230dae / a44ad5c3 / 8bdd899a / fbd67ac7 wie Bau Koerper).
- Fremde `_arbeit/baer_*`-Ordner nur gelesen. Renders nur RTX 4090/OptiX (+ Entrauscher) ueber `werkzeug/gpu_render.sh` (Sperre `gpu.lock`).
- Alle Bilder unten habe ich angesehen. Blaetter mit Vorlage oder Spielbild liegen nur lokal unter `_arbeit/baer_2c`.
- Sitz-Ausnahme der Kopf-Hals-Grenze (SPEZ 5.4, K2) ist benutzt: Kopf gegen Hals nicken bis 57,5 (Grenze 60), nur in den drei Sitz-Clips.
  Das ist die offene Entscheidung der Spez (Orchestrator/Kevin); ohne sie gilt K1 (nicht gebaut, siehe 6.2).

## 0. Kurz

| Ziel | neu (Endstand n2, Sit Bild 0/30/60/90) | heute (NCBearTest) | Soll | ok |
|---|---|---|---|---|
| Fussabstand (Mitten Hinterfuss-Haut) | **71,0 cm** | 118,1 | 62-72 | ja |
| Sprunggelenke y | 67,0 cm | 113,3 | 66-72 | ja |
| Luecke Hinterfuss / Vorderpfote, Pfote / Pfote | 3,7 / 1,5 cm | 21,8 / 11,4 | >= 2 / >= 1 | ja |
| Ferse auf dem Boden (tiefste Fersenhaut) | +0,15 cm | +0,14 / +0,48 | 0-0,5 | ja |
| Vorderpfoten flach (tiefste Haut), Ballen x / \|y\| | 0,00 cm, 0,40 / 0,12 | x 0,40 \|y\| 0,18 | 0,34-0,40 / 0,11-0,13 | ja |
| Ellbogen innen ("gerade nach unten") | 161,5-162,9 | 152,6-155,6 | 150-172 | ja |
| Kopf-Oberkante | 1,306-1,314 m | 1,191-1,205 | 1,20-1,32 | ja |
| Hinterfuss sichtbar L/B (Spielkamera) | 1,36 | 2,14 | 1,1-1,4 | ja |
| Spielkamera: Koerper hinter dem Kopf | +6,5 / +6,7 / +5,2 / +6,7 cm | +24,0 / +21,8 / +21,4 / +21,8 | <= +2 (K1-Ersatz <= +8) | **nein** (K1-Ersatz ja) |
| Spielkamera: Kante 3 cm neben dem Kopf | -6,2/-13,7; -2,7/-14,9; -3,3/-17,9; -2,7/-14,9 | +12,2/+4,5 ... +14,1/-1,8 | <= -10 (K1 <= -4) | **nein** (eine Seite beim Umschauen) |
| Spielkamera: Kopf / Silhouette | 0,49-0,52 | 0,33-0,35 | >= 0,45 | ja |
| Von vorn: Kante neben dem Kopf | -33,0/-34,5; -26,3/-34,4; -25,5/-37,9 | -16,2/-23,1 ... -15,9/-26,3 | <= -28 (K1 <= -22) | Bild 0 ja, beim Umschauen eine Seite -25,5 |
| Von vorn: Koerper hinter dem Kopf | -11,2 .. -11,5 | -4,6 .. -6,3 | <= -8 | ja |
| Von vorn: Kopf / Brustband | 0,57-0,59 | 0,48-0,51 | >= 0,55 | ja |
| Clips: Dauer/Proben/Zeiten | SitDown 1,6 s/49, Sit 4,0 s/121, StandUp 1,3 s/40, Zeiten bit-gleich | gleich | gleich | ja |
| Sit-Schleife | erstes = letztes Bild bit-gleich; SitDown-Ende = Sit-Anfang = StandUp-Anfang (0,0) | | | ja |
| 12 andere Clips, Knochen, Offset, Bind, Netz | bit-gleich zu Bau Koerper (Dump-Vergleich) | | bit-gleich | ja |
| Gelenkgrenzen (Klemmen) | 0 in allen drei Clips, `aus_grenze` leer | StandUp: Knie am Anschlag 6-11 Bilder | 0 | ja |
| Boden | Sit/SitDown/StandUp tiefster Punkt -0,00 cm | -0,00 | >= -0,05 / -0,06 | ja |
| Durchdringung Hinterfuss/Unterarm, Pfote/Pfote | 0 Punkte in jedem Bild aller drei Clips | | 0 | ja |
| Dehnung Sitz-Clips 99,5 % / max | 2,31-2,32 / 3,56-3,68 (Nacken hinter dem Kopf) | 1,89-2,02 / 2,86-3,11 | <= 2,6 / <= 4,0 | ja |
| Achsel/Brust in den Sitz-Clips | 3,09 / 2,82 | 1,56-1,62 / 1,73-1,82 | <= 3,5 | ja |
| Max ueber alle Clips | 99,5 % 2,49, max 3,68 (Sit), Achsel/Brust 3,51 (SwipeR, Bau Koerper) | | 2,6 / 4,0 / 3,5 | wie Bau Koerper (Achsel 3,51 bleibt offen) |

Im Ton aus Kevins Spielkamera: der Baer sitzt kompakt, Hinterbeine eng, Vorderbeine gerade zwischen den Hinterbeinen, Kopf oben auf
dem Koerper statt in einer Kapuze, kurze Hinterfuesse mit der Sohle nach vorn (`bilder/sitzen_spielkamera.png`). Der Kragen ist von
+21..+24 cm auf +5..+7 cm gesunken, das Spez-Ziel +2 cm erreiche ich nicht (Abwaegung in 3).

## 1. Neustart: Zwischenstaende uebernommen, Kette geprueft

- Der erste Sitzen-Bauer (04:01-04:35) hatte Pose SITZ_2C (K2), `sp_setzen_2c`, `sp_sitzen_2c`, `sp_aufstehen_2c`, die Sitz-Grenze
  `GRENZEN_RUMPF_SITZ` und Probe-Werkzeuge (`sitzen/werkzeug/pose_probe_2c.py`, `sitzmess.py`, `mess_sitzen.py`, `messen_sitzen.sh`,
  `kodieren.py`, `auftrag_probe.py`). Alles uebernommen; Pose und Schritte unten nachgebessert.
- Die Datei hatte er mit CRLF gespeichert (MD5 7a23aa83). Bau Koerper hatte LF hinterlassen (11c7f3c4). Ich habe 11c7f3c4 aus
  `baer_kampf_pfote.py` + Kopfzeilen + den zwei Pfad-Zeilen rekonstruiert (MD5 genau 11c7f3c4 in LF,
  `sitzen/rekon_11c7f3c4/kampf_lf.py`) und damit die GLB-Stufe gebaut: **GLB MD5 89678e8f = `glb_koerper`, Dump byte-gleich**
  (`sitzen/bau_rekon/`). Die Kette ist also deterministisch, und halbe Aenderungen gab es nur in den Sitz-Teilen.
- `baer_kampf_2c.py` jetzt LF (MD5 Endstand cf5e18af, Kopie `glb_sitzen/log/baer_kampf_2c_stand.py`).
- Die Stufe `formel` (Formel-Gewichte, liest `baer_kampf_2c.py` bis vor die Clips) habe ich mit dem Endstand neu gerechnet:
  `gew_2c_formel.npz` in allen Feldern gleich zu `glb_koerper/netz/` (`sitzen/bau_n2/formel/`). Die Gewichtsoptimierung liest die
  Clip-Matrizen aus einem festen alten Dump (`baer_gewichte_2c.py:80`, `_arbeit/baer_fell/bestand/dump.txt`), nicht aus diesem Skript;
  netz/fbx/gewichte sind damit die von Bau Koerper (FBX b440d693, Gewichte B ab8a487d). Nicht neu gerechnet (15 min CPU, Ergebnis gleich).

## 2. Was in `baer_kampf_2c.py` geaendert ist (nur Sitz-Teile; Zeilen Endstand)

| Ort | Inhalt |
|---|---|
| :1-4 | Kopfzeilen (was Bau Sitzen geaendert hat) |
| :580-582, :991, :1692, :2522, :2532 | Sitz-Grenze `GRENZEN_RUMPF_SITZ` (Kopf gegen Hals nicken bis +60), aktiv nur fuer die drei Sitz-Clips (vom ersten Bauer, unveraendert) |
| :1288-1312 | `SITZ_2C` neu (Begruendung im Kommentar): Becken (-0,29; z 0,40572 geloest), Becken -35, Lende -27, Brust -37, Hals (4,2; -78; 2), Kopf (12; -20; 5), Schwanz -35, Schulterblatt nicken 16 / rollen -3, Vorderpfote (0,40; 0,12), gier 4, Sprunggelenk (0,18; 0,335; z 0,08111 geloest), Hinterfuss welt (20; -91; 5), Kniepol (0,67; 0,15; 0,74) |
| :1313 | `_pose_s2c` (erster Bauer) |
| :1483-1511 | **neu `FERSE_WEG`, `_ferse_weg`**: Hinterbein-Schritt in die Sitzlage und aus ihr ueber den Weg des Sprunggelenks (flach, Hub 2,5 cm, 3 cm aussen), Fuss dreht um die Ferse |
| :1514-1552 | `sp_setzen_2c`: Schritt 0,68-0,94 mit `_ferse_weg` (statt Ballen mit 6 cm Hub) |
| :1554-1569 | `sp_sitzen_2c` unveraendert bis auf den Kommentar (Atmen, Umschauen gier 12 -> 27 -> 12, Kiefer 5 Grad bei 2,9 s) |
| :1571-1606 | `sp_aufstehen_2c`: erster Hinterbein-Schritt mit `_ferse_weg` |
| :1638-1640 | Clip-Liste: die drei Sitz-Clips bauen aus `sp_*_2c` auf `POSE_S2C`; Dauer/Schluesselzeiten wie heute |

`NCBear_SitB` gibt es im GLB nicht; die Vorschau-Variante (`NCB_VORSCHAU_SITZ_B`) ist nicht angefasst und nicht geprueft.

## 3. Runden (Bilder angesehen; Probe = Haut ohne GLB, `sitzen/probe/p25..p36.log`)

| Runde | Was | Befund |
|---|---|---|
| p24 (Stand erster Bauer) | Brust -40, Lende -25, Hals -82, Kopf -24, Schulterblatt 12 | `sitzen/blatt/p24_uebersicht.png`, `p24_seite_kopf.png`, `p24_hinten_oben.png`: **Kopf schaut deutlich nach oben** (von vorn sieht man unter das Kinn, von der Seite Schnauze ~20 Grad hoch); **scharfe Querfalte zwischen den Schulterblaettern** (von hinten). Kragen hinter +2,9 |
| p26 | Ruhe und alter Sitz-Clip auf dem Koerper-Netz von hinten | `sitzen/blatt/p26.png`: keine Falte -> sie kommt aus der neuen Haltung |
| Ortung | Stauchung am Ruecken | 85 Dreiecke sigma2 < 0,55 (min 0,06) bei Ruhe-x 0,10-0,20 = Uebergang Lende/Brust: Brust gegen Lende -15 (Streckung an der Grenze) |
| p25 | Kopf flacher (Hals -74/-70, Kopf -14/-12), Ruecken gerader, Schulterblatt 6 | `sitzen/blatt/p25.png`: Kopf geradeaus kostet Kragen (+7,1/+8,4); geraderer Ruecken hebt die Schulter, die Pranken schweben 0,8-2,2 cm |
| p27 | Suche 36 Posen: Brust -40/-37/-34 x Brust gegen Lende -15/-10/-6 x Schulterblatt 12/16 x Pranke x 0,38/0,41 (13 s) | Falte faellt mit der Streckung (85 -> 44-49 -> 8-16 Dreiecke); Pranken flach nur bis Schulter z ~0,73; Achsel 3,50 -> 3,09 -> 2,77; Kragen hinter +2,9 / +4,4 / +6,9 |
| p28 | vier Kandidaten c1-c4 mit Kopf geradeaus | `sitzen/blatt/p28.png`, `p28_zoom.png`: c1 (Brust -37, Streckung -10, Schulterblatt 16, Hals -78, Kopf -20): Falte nur noch weich, Kopf sitzt oben, Kopf fast waagerecht. c2/c3: Falte fast weg, aber die Schultern steigen neben dem Kopf (Kapuze kommt zurueck). c4: scharfe Falte |
| p29 | c1 mit Hals -76/-78/-80 und Umschau-Bild | gewaehlt Hals -78 / Kopf -20 (Kopf gegen Hals 57,5) |
| p30, p31 | drei Clips am Netz | StandUp: 2 Punkte Fuss im Unterarm bei 0,23 s -> Schrittmitte 3 cm nach aussen: 0 |
| n1 | GLB + alle Messungen | `sitzen/bau_n1/`; Video-Bilder zeigen beim Hinsetzen Bild 22-26 und Aufstehen Bild 3-10 ein hochgehobenes Sprunggelenk (bis 0,27 m) und ein Knie bis 55-62 Grad gefaltet -> harte Knitter an Knie/Schenkel (`sitzen/blatt/vid_setzen_detail.png`) |
| p34 | `_ferse_weg` gegen alten Ballen-Weg | Hinsetzen: Knie min 62 -> 74/84, Sprunggelenk max 0,272 -> 0,159 m; Aufstehen: Knie 55 (am Anschlag, 11 Klemmungen) -> 56/68 ohne Klemmen, Sprunggelenk 0,213 -> 0,156; Durchdringung 0, Boden 0 |
| **n2** | Endstand | `sitzen/blatt/vid_n1_n2.png` (oben alt, unten neu): Fuss bleibt unten und rollt auf die Ferse, kein zusammenfallender Schenkel mehr |
| p36 | kleineres Umschauen (Kopf gier 10/12 statt 15) | Kante neben dem Kopf nur 0,3-1,7 cm besser -> Umschauen bleibt wie heute (Spez 10 -> 28 -> 10) |

**Abwaegung Kopf/Kragen (ehrlich):** Mit dem Kopf des ersten Bauers (nach oben) waere der Kragen hinter dem Kopf +2,9 statt +6,5 cm,
aber der Baer schaut von vorn und von der Seite in den Himmel, und die Rueckenfalte ist scharf. Kevins Vorlage blickt geradeaus.
Ich habe den geraden Blick und den glatten Ruecken genommen. Kopf -20 liegt in der Spez-Spanne (-25..-15), das Kragenziel <= +2 cm
der Spez wurde mit dem nach oben blickenden Kopf geschaetzt.

## 4. Messungen Endstand (n2; Dump `glb_sitzen/dump_sitzen.txt`)

### 4.1 Pose S_neu gegen SPEZ 5.2 (Engine-Haeutung des Dumps, `sitzen/log/mess_sitzen_n2.txt`, Bericht `glb_sitzen/log/bericht.json`)
| Teil | neu | Soll | ok |
|---|---|---|---|
| Becken Ursprung x / z | -0,290 / 0,406 | -0,32..-0,26 / 0,33-0,42 | ja |
| Huefte z | 0,330 | 0,27-0,35 | ja |
| Becken / Lende / Brust (Welt) | -35 / -27 / -37 | -35 / -25 / -40 (+-5) | ja |
| Brust gegen Lende | -10 (Schleife -10..-8) | -15 | Abweichung, Grund Rueckenfalte (3) |
| Schulterblatt nicken / rollen | 16 / -3 | 15..20 | ja |
| Hals / Kopf (Welt) | -78 / -20 | -77 / -25..-15 | ja |
| Kopf gegen Hals nicken (Umschauen) | 57,5 (54,4-57,5); gier bis 20,5, rollen bis 22,8 | +50..+60; gier <= 30, rollen <= 25 | ja (Sitz-Ausnahme) |
| Schulter z | 0,723-0,725 | 0,69-0,74 | ja |
| Vorderpfoten | Ballen x 0,40, \|y\| 0,12, Haut 0,00 cm, Ellbogen 161,5-162,9 | wie Tabelle | ja |
| Sprunggelenk x / \|y\| / z | 0,180 / 0,335 / 0,081 | 0,16-0,24 / 0,33-0,36 / ~0,07-0,09 | ja |
| Knie innen / \|y\| Knie | 134,6 / 0,314 | 115-145 / 0,32-0,40 | Winkel ja, \|y\| 6 mm darunter |
| Hinterfuss Welt gier / nick / rollen | 20 / **-91** / 5 | 15..25 / -95..-110 / 0..10 | nick 4 Grad zu flach: steiler stoesst der Fuss gegen den Unterschenkel (dors -124,0, Grenze -125; Probe des ersten Bauers: Klemmen rollte die Sohle bis 50 Grad) |
| Kiefer | zu, 5 Grad bei 2,6-3,3 s | wie heute | ja |

### 4.2 Clips (Vertrag `NCBearFight.lua:54-56`, XML `AnimSets/buck/idle/NCBear_*.xml`, beide nur gelesen)
- Lua: sitdown 1,60 / sit 4,00 loop / standup 1,30 (`NCBearFight.lua:54-56`); XML: `m_Looped` false/true/false, Ereignis
  `SetVariable NCBearDone=true` in SitDown/StandUp (`NCBear_SitDown.xml:5,15,17`, `NCBear_Sit.xml:5`, `NCBear_StandUp.xml:5,15,17`).
  Das GLB traegt keine Ereignisse; nichts davon geaendert.
- Dump: Bilder 49/121/40, Zeiten bit-gleich zu heute (`sitzen/werkzeug2/netz_gleich.py`, `glb_sitzen/log/glb_pruef.txt`).
- Sit Bild 0 = Bild 120 bit-gleich; SitDown Bild 48 = Sit Bild 0 = StandUp Bild 0 (Abweichung 0,0); SitDown Bild 0 und StandUp
  Bild 39 weichen von Idle Bild 0 um 0,131 ab, genau wie heute (Grundhaltung `grund()`).
- Sprung je Bild (aus `bericht.json` + Dump): Pfote/Oberarm drehen (sup, tw) max 3,4 / 4,4 Grad, Pfotenbeugung max 10,5 Grad, Becken
  max 2,36 cm/Bild (Grenzen 20 / 20 / 35 / 3). Schleifennaht Sit: 0.

### 4.3 Feste Regeln
- **Netz und 12 Clips:** Dump-Punkte (11.516 x 16 Werte), Indizes (56.970), Knochen, Offset: bit-gleich zu `glb_koerper/dump_koerper.txt`;
  DeerStag_Idle01/Walk/Run/Death/Dead, NCBear_Rear/SwipeL/SwipeR/Slam/Bite/Maul/Eat: Matrizen und Zeiten bit-gleich.
  Gegen heute (`glb_pruef`): Knochen 26, Namen/Eltern gleich, Offset/Bind max 0,0; 12 Clips Abweichung 0.
- **Kopf** (`pruef_sitzen/n2/kopf_out.txt`): 1.333/1.333 Lage+UV+Gewichte bit-gleich; Krallen vorn 227 bit-gleich, hinten 228 = alt + (-0,070).
- **Dreiecke** 18.990, max 4 Einfluesse, Summe 1 (unveraendert, Netz von Bau Koerper). Body-PNG = Platzhalter von Bau Koerper (MD5 4ae148df).
- **Boden** (`pruef_sitzen/n2/tiefst_out.txt`): Sit/SitDown/StandUp Netz und jede Pfote -0,00 cm; die 12 anderen Clips wie Bau Koerper.
  Der Pruefer meldet 2 "Verstoesse": Hinterkralle im Sitzen 24,9 cm UEBER dem Boden statt 39,7 cm heute (Krallen zeigen nach oben,
  kuerzerer Fuss). Das ist kein Stecken im Boden, die Regel (nicht tiefer IM Boden) ist erfuellt.
- **Durchdringung** (Windungszahl, `sitzen/werkzeug/sitzmess.py`, jedes Bild): 0 in SitDown/Sit/StandUp (p30/p31/p34).
- **Dehnung** (`pruef_sitzen/n2/region_tabelle_out.txt`, ohne Kopf/Krallen):
  SitDown 2,32 / 3,56, Sit 2,32 / 3,68, StandUp 2,31 / 3,56 (99,5 % / max; Ort Ruecken/Flanke). Achsel 3,09, Brust 2,82, Leiste
  2,56-2,64, Kehle 2,53-2,56. Mit den alten Sitz-Clips auf dem Koerper-Netz waren es 1,95-2,15 / 2,79-2,88 (`pruef_koerper/k5B`):
  die aufrechte Haltung dehnt mehr, bleibt unter den Grenzen. **Max ueber alle Clips steigt dadurch von 3,51 auf 3,68** (Grenze 4,0).
  Ort des Hoechstwerts (p35): Haut Hals/Kopf hinter dem Kopf (Ruhe x 0,68, z 0,87, Gewichte Neck 0,51-0,61 / Head 0,39-0,49), kommt von
  Kopf gegen Hals +57,5; beim Umschauen 3,68.
- **Hals/Nacken und Bein-Uebergang** (Spez 8.1 "neu berichtet", `sitzen/werkzeug2/zonen_clips.py`, alle Bilder; alter Clip auf dem
  Koerper-Netz in Klammern): Hals/Nacken sigma1 max 3,67-3,84 (2,73-3,05), Kehle 2,77-2,91 (2,86), Knie sigma1 2,56-2,64 (2,11-2,88),
  Rueckenfalte sigma2 < 0,55 max 46 Dreiecke, min 0,24 (0). Bein-Uebergang z 0,12-0,50: mein Zonenfilter faengt einzelne Kleinst-
  Dreiecke an der Ellbogen-Behang-Kante (sigma1 bis 12; alt 6,7-9,0), der amtliche Regionen-Pruefer (oben) zeigt dort nichts ueber 3,7.
- **Falten liegend** (Dead): unveraendert 688 / Achsel+Ellbogen 254 (Clip bit-gleich; offen aus Bau Koerper).
  Falten im Sitzen (Info): 587 Dreiecke sigma2 < 0,5 (Ellbogen 202, Achsel 268, Knie 162); alter Clip auf dem Koerper-Netz 408.
- **Ei** 0,993, Beine/Rumpf/Hinterfuss (`mess2c`) wie Bau Koerper (Netz gleich).

## 5. Bilder (`bilder/`, Ton; Blaetter mit Vorlage/Spielbild nur lokal)
- `sitzen_spielkamera.png`: Kevins Spielbild | alt Textur | alt Ton | **neu Ton** (Sit 60) | Vorlage; darunter neu Sit 0/30/90 und
  az +-45 el 30. Neu: kompakt, Hinterbeine eng, Vorderbeine gerade dazwischen, Kopf oben, kein Fellkragen ringsum.
- `sitzen_vorn_vorlage_ton.png`: von vorn alt | neu | Vorlage; az -30 el 8 alt | neu Bild 60 | neu Bild 0; Seite, hinten el 15/30.
- `sitzen_hinterfuss_nah.png`: Hinterfuss im Sitzen (az 0 el 10) alt Ton | alt Textur | neu Ton | Vorlagen-Fuesse (nur lokal).
- `sitzen_spielgroesse_ton.png`: Spielbild nativ (Baer ~260 px) | alt | neu Bild 60 / Bild 0 in gleicher Groesse.
- `sitzen_vorschau.mp4` (208 Bilder, 30/s, 1280x640: links Spielkamera az 0 el 30, rechts Seite az 90 el 8): Hinsetzen -> eine
  Sitz-Schleife -> Aufstehen, Ton. Kontaktbogen `sitzen_vorschau_bilder.png`.
- Stehen aus der Spielkamera seitlich: unveraendert (Clips bit-gleich), Blatt von Bau Koerper `koerper_stehen_spielwinkel_ton.png`.
- **Mit Textur fuer neu: nicht moeglich.** Das UV ist neu (Bau Koerper), die Body-PNG ist ein Platzhalter; ein Probebild damit ist
  Flickwerk (`sitzen/render/n1/neu_sit60_spiel_tex_platzhalter.png`, nicht ins Blatt genommen). Textur-Bilder und Textur-Video macht
  der Textur-Bauer am Ende (gleiche Auftraege: `sitzen/log/auftrag_n1.json`, `auftrag_video_n2.json`, nur `textur`/`shader` aendern).
- Arbeitsbilder: `sitzen/blatt/` (p24, p25, p26, p28, p28_zoom, n1_zoom, vid_*), Einzelbilder `sitzen/render/`.

## 6. Offen / fuer die naechsten

1. **Kragen-Ziel nicht erreicht:** Spielkamera hinter dem Kopf +5,2..+6,7 cm (Soll <= +2, K1-Ersatz <= +8), Kante neben dem Kopf auf
   der vom Kopf abgewandten Seite beim Umschauen -2,7..-3,3 (Soll <= -10, K1 <= -4), von vorn -25,5..-26,3 (Soll <= -28). Rest kommt
   aus dem Buckel/Nacken des Netzes (Bau Koerper: Nacken x 0,60 +1,6 cm ueber Soll wegen Kopfnaht-Schutz) und dem geraden Kopf.
   Gegenmittel: Kopf staerker nach oben (Kragen +2,9, sieht von vorn nach Himmel aus), Kopf x1,10-1,15 als Vorschlag (SPEZ 6.3, nicht
   meine Aufgabe), Farbuebergang Hals/Nacken in der Textur (SPEZ 6.2.4).
2. **Entscheidung K2:** gebaut mit der Sitz-Ausnahme (Kopf gegen Hals 57,5). Wird sie abgelehnt: `GRENZEN_RUMPF_SITZ` auf +-35 zurueck,
   dann klemmt der Kopf auf +35 und der Hals muss flacher (K1) - neu messen, nicht gebaut.
3. **Hinterfuss nicken -91** statt -95..-110 und Knie \|y\| 0,314 statt >= 0,32 (siehe 4.1).
4. **Weiche Rueckenfalte** zwischen den Schulterblaettern (46 Dreiecke, min 0,24) und **Kniekehle** (sigma2 bis 0,02, auch mit dem alten
   Clip auf dem neuen Netz: 109 Dreiecke, min 0,08) und eine kleine Knitterkante aussen am Knie im Blick az -30 (`sitzen/blatt/n1_zoom.png`).
   Die Hautgewichte sind gegen die ALTEN Sitz-Clips optimiert (`baer_gewichte_2c.py:80` liest einen festen alten Dump). Vorschlag: die
   Gewichtsoptimierung einmal mit den neuen Sitz-Clips rechnen lassen - aendert aber alle Gewichte (Bau-Koerper-Messungen neu), daher
   nur nach Entscheidung.
5. Dehnung max ueber alle Clips 3,51 -> 3,68 (Nacken hinter dem Kopf, Sitz); Achsel 3,51 (SwipeR) bleibt wie Bau Koerper offen.
6. Clip-Runde (nur melden): Aufrichten neu; Lefzen; Liegehoehe (unveraendert 1,12 cm).
7. `C:\render\` von Bau Koerper bitte weiter von Hand loeschen (nicht von mir).
8. **Nicht gespielt.** Kevins Test: `NCBear_Sit(20)` aus der Spielkamera, Hinsetzen/Aufstehen ansehen.

## 7. Wiederholen (~1 min ohne Video)
```
cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/sitzen
bash werkzeug2/glb_bau.sh $PWD/bau_X                          # GLB-Stufe mit baer_kampf_2c.py, Netz/Gewichte von Bau Koerper
python werkzeug2/netz_gleich.py ../glb_koerper/dump_koerper.txt bau_X/dump.txt
python werkzeug/mess_sitzen.py bau_X/dump.txt X                 # Sitz-Masse, Kopf-Passung -> log/mess_sitzen_X.txt
mkdir -p bau_X/netz && cp ../glb_koerper/netz/lp_2c.npz bau_X/netz/ && R=$PWD/bau_X bash werkzeug/messen_sitzen.sh X dump.txt
python werkzeug2/zonen_clips.py bau_X/dump.txt                  # Hals/Nacken, Knie, Ruecken je Clip
"$B" --background --factory-startup --python werkzeug/pose_probe_2c.py -- probe/p30.py   # Pose + Clips ohne GLB (Probe)
```
Video: `log/auftrag_video_n2.json` -> `bash ../werkzeug/gpu_render.sh ../werkzeug/render_optik.py ...` (2 min), Paare wie in
`render/video_n2_paar/`, dann `kodieren.py`.

## 8. Dateien (`_arbeit/baer_2c/`)
- **Endstand:** `glb_sitzen/42/media/models_X/Skinned/NCBear.glb` (MD5 1427f367156fd1ea707d706534c52086),
  `glb_sitzen/42/media/models_X/WorldItems/NCBear.fbx` (b440d693, = Bau Koerper), `glb_sitzen/42/media/textures/Body/NCBear.png`
  (Platzhalter 4ae148df), `glb_sitzen/dump_sitzen.txt`, `glb_sitzen/log/` (glb_pruef, bericht.json, kampf.log, mess_sitzen_n2, Skript-Stand).
- **Skript:** `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_kampf_2c.py` (MD5 cf5e18af, LF).
- **Bau-Ordner:** `sitzen/bau_rekon` (Gegenprobe 11c7f3c4), `sitzen/bau_n1`, `sitzen/bau_n2` (Endstand), `sitzen/bau_n3` (nach
  Kommentar-Aenderung, Dump = n2).
- **Messungen:** `pruef_sitzen/n1`, `pruef_sitzen/n2` (Endstand), `sitzen/log/mess_sitzen_*.txt`, `sitzen/probe/p25-p36.log`.
- **Werkzeuge:** `sitzen/werkzeug/` (vom ersten Bauer), `sitzen/werkzeug2/` (glb_bau.sh, netz_gleich.py, blatt.py, falten_zonen.py,
  knie_verlauf.py, zonen_clips.py).
- **Bilder:** `bilder/sitzen_*.png`, `bilder/sitzen_vorschau.mp4`; Referenz-Ausschnitt `referenz/spielbild_baer_ausschnitt_2.png` (nur lokal).
