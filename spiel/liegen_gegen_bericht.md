# GEGEN_1.md -- Lauf baer-liegen, Rolle GEGENPRUEFER, Runde 1 (13.11.2026, 20:36-21:00)

**Statisch geprueft: selbst gerechnet, selbst gerendert, selbst angesehen -- NICHT gespielt.** Geschrieben nur in `_arbeit/baer_liegen/gegen1b/`
(eigene Werkzeuge, Dumps, Messungen, Renders, Blaetter), dieser Bericht und `bilder/KEVIN_liegen.png`. Test-Mod nur gelesen (7 GLB-MD5 vor und nach
meiner Arbeit gleich: 08bfdbfd / 6c3f0a96 / 989939f2 x2 / d9931d32 / a80413f4 / f58ea4c9), `out/` nicht veraendert, kein git, kein Download.
Pfade relativ zu `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_liegen/`; G = `gegen1b/`. Laengen in ECHTEN cm bei Groesse 1,0
(1 Einheit = 1,8/0,98 m, wie die Berichte); im Spiel x 1,35 (grosse Baeren) bzw. x 0,35 (Junge).
Hinweis: Neben mir lag ein Ordner `gegen_1/` (angelegt 20:14, letzte Datei 20:49, kein Bericht) -- offenbar ein zweiter Gegenpruefer-Lauf. Ich habe ihn
weder gelesen noch benutzt und in einem eigenen Ordner gearbeitet.

## 0. Urteil

**Bestanden, schoen genug fuer Kevin, bereit fuer den Einbau in die Test-Mod. Kein Blocker, kein major offen.**
* Kevins Mangel ist bei allen vier Koerpern behoben: in Dead UND in allen 78 Sturz-Bildern schneidet kein Bein (Unterbein + Pfote) ein anderes Bein
  (eigene Dreieck-gegen-Dreieck-Pruefung; ALT: 43 Sturz-Bilder mit bis zu 562 Schnitt-Paaren). Der Koerper liegt auf, nichts steckt tiefer als 1,5 cm
  im Boden, der Sturz endet punktgleich in Dead.
* Aus Kevins Kamera (az 50 und az 90) ist jede Pfote frei und einzeln zu sehen; mit Textur dieselbe Form wie im TON (die Textur verdeckt nichts).
* Die zwei major der Pruefer sind wirklich behoben (O1 Junges-Sturz: Vorlauf 23,9 -> 0,9 Grad; T1 Schreibschutz vorhanden). O2 ist so weit behoben, wie
  "nur Clips" reicht; der Rest ist Kevins Entscheidung (K1, K2), nicht ein Bau-Fehler.
* Neu kaputt: nichts gefunden. Bekannte kleine Restpunkte (Abschnitt 5) sind alle nicht schlimmer als heute oder als Frage an Kevin gemeldet.

## 1. Was ich selbst gemacht habe (keinem Bericht geglaubt)

| Pruefung | Werkzeug (eigen, in G/werkzeug/) | Ergebnis |
|---|---|---|
| Importer des Spiels auf alle 10 GLB (5 ALT Test-Mod, 5 NEU out/) | `dumpe.sh` (Dump.java) | G/dump/ |
| glb_pruef.py je Paar | `_arbeit/baer_2c/werkzeug/pruef/glb_pruef.py` | G/mess/glb_pruef_*.txt |
| eigener Byte-Vergleich der GLB (JSON + BIN, jeder Accessor) | `g1b_bytes.py` | G/mess/bytes_*.txt |
| Durchdringung je Glied-Paar, Boden, Auflage, Pfotenabstand, Sicht aus Kevins Kamera, Dead + alle 78 Sturz-Bilder, ALT und NEU | `g1b_schnitt.py` (eigene Haut aus dem Dump, Blender-BVH Dreieck/Dreieck, Strahl je Punkt zur Kamera) + `g1b_tabelle.py` | G/mess/schnitt_*.json, TABELLE.txt, bein_koerper_je_bild.txt |
| Vorlauf der oberen Beine im Sturz (Befund O1) | `g1b_vorlauf.py` (Vorzeichen geprueft an Runde 0: -23,9 Grad = Befund des Pruefers) | G/mess/vorlauf.txt |
| Schweben beim Rennen | `g1b_rennen.py` | G/mess/rennen_*.txt |
| Wiederholbarkeit: alle drei Befehle aus WIEDERHOLEN.md vom Stand der Test-Mod in MEINEN Ordner | Skripte der Bauer, nur aufgerufen | G/wieder/ |
| Renders ALT/NEU mit derselben Kamera, Normalen wie die Engine, Licht wie das Spiel (animalEffect) | EIGENER Renderer `g1b_render.py` (nicht kopiert), RTX 4090 OptiX, Sperre gpu.lock (je < 2 min gehalten) | 336 Einzelbilder G/render/<Koerper>/ |
| Pruefblaetter (je Koerper Dead TON, Dead Textur, Spielgroesse, Sturz) und Kevins Blatt | `g1b_blatt.py`, `g1b_kevin.py` | G/blatt/, bilder/KEVIN_liegen.png |

## 2. Technik -- nur Death/Dead geaendert

* **glb_pruef.py (Importer des Spiels), alle fuenf:** 26 Knochen, gleiche Namen/Eltern; Offset und Bind 0.00e+00; 13 Clips (Idle01, Run, Walk, Bite, Eat,
  Maul, Rear, Sit, SitDown, Slam, StandUp, SwipeL, SwipeR) "Abweichung Modellmatrix 0.00e+00, Schluessel 0.00e+00"; Death 78/78 Abtastungen, Dauer
  2.5667 / 2.5667; Dead 2/2, Dauer 0.0333 / 0.0333; Punkte, Dreiecke, Gewichtssumme 1,0, hoechstens 4 Einfluesse gleich.
* **Eigener Byte-Vergleich, alle fuenf `NUR_DEATH_DEAD_OK`:** Knoten, Szene, Skin (Joints, inverse Bind-Bytes), alle Netz-Accessoren (POSITION, NORMAL,
  TEXCOORD_0, JOINTS_0, WEIGHTS_0, Indizes), Material-JSON gleich; 15 Clips gleiche Namen und Reihenfolge; 13 Clips jeder Sampler byte-gleich (Zeiten,
  Werte, Interpolation). Death/Dead: gleiche Kanal-Ziele, gleiche Zeit-Bytes, gleiche Interpolation; Werte geaendert in 19 Kanaelen (2c, Generator-Baer,
  Junges: Becken-Lage + 18 Drehungen) bzw. 20 (Generator-Junges, zusaetzlich R_Toe0). **Kiefer und alle Skalierungen unveraendert** (Gesicht starr).
  Letztes Death-Bild = Dead Bild 0 = Dead Bild 1 (float32 bit-gleich je Kanal), Death-Bilder 0-15 bit-gleich zu ALT, erstes geaendertes Bild 16,
  Quaternion-Laenge auf 1,2e-07, alle Werte endlich. Einziger sonstiger Unterschied: `asset.generator` (Text).
* **Zwilling:** `cmp out/.../NCBearCubGen.glb NCBearBenchCubGen.glb` byte-gleich (MD5 dae9dbed...). **md5.txt:** ASCII, LF, `md5sum -c` 5 x OK;
  `out/` = genau 5 GLB + md5.txt.
* **Wiederholbar:** GROSS 2c, GROSS gen und Junge `alle` (WIEDERHOLEN.md) vom Stand der Test-Mod in G/wieder/ -> Code 0, alle fuenf MD5 = out/
  (dc50d350 / 867b558b / 8a1b1e27 / dae9dbed x2), Abnahme der Skripte bestanden (Junges Vorlauf VL 0,9 / HL 0,1 Grad; Gen-Junges 5,4 / 6,7).
  Schreibschutz im Junge-Skript gelesen (`schreibschutz()`, normcase + samefile, "/zomboid/mods/" und "/steamapps/" abgelehnt, vor jedem Bau) -- T1 behoben.
* Lua/XML: unveraendert; `grep -rIl DeerStag_Dea` ueber die Test-Mod (ohne .glb) findet nichts -- kein Skript haengt an Death/Dead. Namen und Dauer gleich, also
  laufen Vanilla falldown -> onground -> Leichnam wie heute. **SP und MP:** geaendert sind nur zwei Clips in fuenf Modell-Dateien -- kein eigener SP-/MP-Zweig;
  beides ungespielt. Nach dem Einbau Spiel neu starten.

## 3. Geometrie -- eigene Messung (ALT -> NEU)

### 3.1 Dead (liegt tot)

| Mass | Gross Klassisch (NCBear) | Gross Braun (NCBearGen) | Junges Klassisch (NCBearCub) | Junges Braun (NCBearCubGen + Zwilling) |
|---|---|---|---|---|
| Bein/Bein-Schnitte (Dreieck-Paare) | VL-VR 160 + HL-HR 250 -> **0** | VL-VR 175 + HL-HR 247 -> **0** | VL-VR 144 + HL-HR 166 -> **0** | VL-VR 45 -> **0** |
| Bein/Rumpf-Kopf-Schnitte | VL 105 (11,3 cm), HL 115, VR 1 -> **VL 6 Paare, 1,5 cm (Achsel-Naht)** | VL 145, HL 141, VR 1 -> **0** | VL 175, HL 179, VR 30 -> **VL 11 Paare, 1,4 cm (Achsel-Naht)** | VL 9, HR 3 -> **0** |
| Bein/fremder Oberarm/Oberschenkel | 0 -> 0 | VL-OberarmVR 22 -> **0** | 0 -> 0 | 0 -> 0 |
| kleinster Pfotenabstand | 2,4 -> **16,4 cm** | 0,3 -> **15,0 cm** | 1,0 -> **18,6 cm** | 0,3 -> **12,3 cm** |
| tiefster Punkt / Rumpf / Kopf | +1,1 / +10,7 / +12,5 -> **-0,90 / -0,77 / -0,29** | -0,4 / +10,5 / +13,0 -> **-0,88 / -0,50 / -0,29** | +2,6 / +4,3 / +4,9 -> **-0,99 / +0,29 / -0,29** | 0,0 / +3,9 / 0,0 -> **-0,81 / +0,33 / -0,29** |
| im Spiel tiefster Punkt | **-1,22 cm** | **-1,19 cm** | **-0,35 cm** | **-0,28 cm** |
| untere Beine VR / HR (Boden) | +1,1 / +2,8 -> **-0,18 / -0,26** | -0,4 / +1,3 -> **-0,15 / -0,15** | +2,7 / +2,6 -> **0,0 / 0,0** | +5,1 / +6,1 -> **0,0 / -0,13** |
| Auflage (Dreiecke ganz unter 1,84 cm) | 0 -> **1736 cm2** | 5 -> **900 cm2** | 0 -> **629 cm2** | 54 -> **877 cm2** |
| obere Pfoten VL / HL tiefster Punkt (in der Luft) | 15,8 / 35,7 cm (Spiel 21 / 48) | 14,9 / 35,4 (Spiel 20 / 48) | 35,3 / 33,1 (Spiel 12 / 12) | 25,2 / 33,7 (Spiel 9 / 12) |
| Kevins Kamera az 50 / az 90: kleinste Pfote frei | 0,49 / 0,16 -> **1,00 / 1,00** | 0,58 / 0,27 -> **1,00 / 0,99** | 0,43 / 0,20 -> **1,00 / 1,00** | 0,92 / 0,89 -> **1,00 / 0,93** |
| Pfote hinter anderer Pfote, schlimmste Stelle | az 270 0,46 | az 270 0,65 | az 270 0,37 | az 0 0,27 |
| ... NEU | **az 0 HR 0,40** (von vorn, Hinterpfote hinter der oberen) | az 0 HR 0,23 | **0,00** | az 0 HR 0,12 |
| az 180 untere Vorderpfote frei (NEU) | 0,04 | 0,07 | 0,36 | 0,52 |

Lesart: "Schnitt-Paare" zaehlt Dreiecke, die sich wirklich kreuzen; die Tiefe ist der Abstand der kreuzenden Ecken zur Ebene des geschnittenen Dreiecks.
Die zwei Achsel-Stellen liegen an der Naht Unterarm/Rumpf des oberen Vorderbeins (innerhalb A3, schon von Bauer und Pruefer genannt); ALT steckte das
ganze Bein 11 cm tief. Mein "Rumpf" ist ohne Oberarme -- bei den Jungen liegen Schulter und Huefte auf, der Rumpf selbst 0,3 cm darueber.
Sicht: eigene Rechnung (Anteil der zur Kamera zeigenden Pfotenpunkte ohne Hindernis), nicht die der Bauer; az 50 / 90 erfuellt A6 klar.

### 3.2 Death (Sturz, alle 78 Bilder)

| Mass | Gross Klassisch | Gross Braun | Junges Klassisch | Junges Braun |
|---|---|---|---|---|
| Bilder mit Bein/Bein-Schnitt (max Paare) | 43 (562) -> **0** | 43 (579) -> **0** | 43 (452) -> **0** | 43 (259) -> **0** |
| Bein/Rumpf tiefste Stelle | 11,4 cm -> **3,4 cm** | 5,6 -> **2,9** | 5,4 -> **2,0** | 2,9 -> **3,0** |
| Bein/fremder Oberarm-Oberschenkel | 0 -> 0 | 40 Bilder (max 24) -> **0** | 0 -> 0 | 0 -> 0 |
| Boden je Bild (im Spiel) | -0,15..+1,12 -> **-1,10..+0,50 (-1,49..+0,67)** | -1,16..+0,13 -> **-1,10..+0,50 (-1,49..+0,67)** | -0,20..+2,63 -> **-1,19..0,00 (-0,42..0)** | -0,28..+0,64 -> **-1,19..0,00 (-0,42..0)** |
| Rumpf liegt (unter 1 cm und bleibt) ab | nie -> **Bild 41** | nie -> **Bild 42** | nie -> **Bild 58** | nie -> **Bild 42** |
| groesster Punktweg / Ruck je Bild | 6,6 / 1,3 -> 11,5 / 2,6 cm | 6,7 / 1,4 -> 11,2 / 2,3 | 5,8 / 2,0 -> 8,9 / 2,0 | 7,2 / 5,0 -> 8,1 / **3,1** |
| letztes Death-Bild gegen Dead (Haut) | **0,00 cm** | **0,00** | **0,00** | **0,00** |
| Vorlauf obere Beine VL / HL (negativ = Bein vor dem Rumpf) | -0,9 / 0,0 | -0,9 / 0,0 | Runde 0: -23,9 / -17,0 -> **-0,9 / 0,0** | ALT -10,3 / -15,6 -> **-5,9 / -7,2** |

Mehr Punktweg als heute ist gewollt: heute faellt der Baer gar nicht (er bleibt halb stehend auf gefalteten Beinen). Junges "Rumpf ab Bild 58": der
Junges-Rumpf federt nach dem Aufschlag (Zeitform von heute), Schulter/Huefte liegen frueher.

## 4. Bilder -- selbst angesehen (eigener Renderer, ALT und NEU je Blick mit derselben Kamera)

Blaetter `G/blatt/<Koerper>_dead_ton.png`, `_dead_tex.png` (Kevins Kamera az 0/50/90/180/270, flach Bauchseite, flach von vorn, von oben),
`_spiel.png` (Spielgroesse neben 1,8-m-Figur, Textur + TON), `_sturz.png` (12 Bilder TON az 50, 5 Bilder Textur az 90, Death-Ende in der Dead-Kamera).
* **Grosse Baeren:** liegen als Baer auf der Seite: unteres Vorderbein nach vorn, unteres Hinterbein nach hinten am Boden, oberes Vorderbein haengt,
  Kopf mit der Wange am Boden, Rumpf ohne Spalt auf dem Boden (ALT: Schatten-Spalt unter dem ganzen Koerper, Beine gestapelt, Risse in der Achsel).
  Oberes Hinterbein steht flach von vorn/hinten waagerecht in der Luft (K1). Sturz: knickt ein (Bild 33-36), faellt (36-42), liegt ab ~46 -- ohne Sprung.
* **Junges Klassisch:** liegt auf der Seite, Beine nach vorn/hinten gefaechert, obere Beine haengen; aus az 50/90 klar als liegendes Junges lesbar.
  Flach von vorn stehen die oberen Beine noch etwas steif zur Seite (K1). Sturz: die linken Beine gehen MIT dem Rumpf (Bild 30/33 kein Wegstrecken mehr).
* **Junges Braun:** liegt auf der Seite (nicht mehr auf dem Ruecken, M6), Pfoten frei; die vier Beine stehen aber fast parallel quer ab -- von vorn und von
  oben wirkt es steifer als die anderen drei (K2). Aus az 50 / 90 liegt es gut.
* **Textur verdeckt nichts:** dieselbe Form in TON und Textur. Spielgroesse: grosse Baeren gut lesbar; Junge sehr klein (Blatt fuer Kevin mit Zoom 2x).
* Mein erster Durchlauf zeigte am Kopf des Jungen eine feine Linie -- das war mein Renderer (Normalen an UV-Naehten getrennt), nicht das Modell; alle
  Bilder sind danach mit Engine-Normalen (Dump-Normalen, mit den Knochen gedreht) neu gerendert.

**Blatt fuer Kevin:** `bilder/KEVIN_liegen.png` (2768 x 1737): je Koerper (Gross Klassisch, Gross Braun/Natur, Junges Klassisch, Junges Braun) ALT links,
NEU rechts: Spielgroesse neben 1,8-m-Figur (Junge mit Zoom 2x), nah aus az 50, az 90 (Bauchseite), az 180 -- mit Textur, Licht wie das Spiel; unten eine
Reihe TON (az 50, ALT | NEU je Koerper). Deutsche Beschriftung, "nicht im Spiel" steht drauf.

## 5. Pruefer-Befunde nachgeprueft, und was offen bleibt

| Befund | Stand nach Nachbesserung 1 | mein Beleg |
|---|---|---|
| O1 major Junges-Sturz, Beine vor dem Rumpf | **behoben** | Vorlauf VL -23,9 -> -0,9 Grad; Sturz-Blatt Bild 30/33 |
| O2 major Junge "umgekipptes Stofftier" | **teilweise** (Junges deutlich besser, Junges Braun maessig) -> K1/K2 | Blaetter NCBearCub/NCBearCubGen_dead_* |
| O3 grosse Baeren oberes Hinterbein waagerecht | belassen (K1) | flach vorn / Bauchseite |
| O4 Pfoten-Huepfer Junges Braun | **behoben** | Ruck 5,0 (heute) -> 3,1 cm |
| O5 unteres Hinterbein kurz durch den Bauch | **offen, minor** | Bild 33-37: HR/Rumpf 2c 87 Paare (ALT 20), Gen 21 (9), Junges 86 (25), Gen-Junges 48 (64); Tiefe 1,5..3 cm; Unterseite, ~0,15 s |
| O6 Hautfalten (Gewichte) | belassen (K6) | Nahbilder: kleine Kante am Ellbogen Gross Braun, keine Risse wie ALT |
| O7 nicht aus jeder Richtung alle Pfoten | belassen (K5) | az 180 untere Vorderpfote 0,04 / 0,07 (gross); az 0 beim 2c Hinterpfote zu 0,40 hinter der oberen |
| T1 major Schreibschutz Junge-Skript | **behoben** | Code gelesen; Wiederhol-Lauf ok |
| T2 out/ aufgeraeumt | **behoben** | 5 GLB + md5.txt |
| T3 / T4 HR-Gelenk im Kippen, Beckenweg 4 cm/Bild | belassen, festgehalten | nicht nachgemessen (Gelenk), Punktweg 11,5 cm/Bild gesehen, kein Sprung im Bild |
| T5 Boden im Spiel -1,62 cm | **behoben** | -1,10 cm = -1,49 im Spiel |
| T6 / T7 / T8 | **behoben** | Abnahme im Lauf gesehen; engster Bein-Abstand Gen-Junges 4,4 cm; Plan-Zeile |

**Offene Maengel (alle minor, kein Grund, Kevin das Blatt nicht zu zeigen):**
1. O5: Sturz Bild 33-37 -- unteres Hinterbein schneidet kurz den Bauch, bei 2c/Junges mit mehr Flaeche als heute (Zahlen oben). Ganz weg nur mit
   eigener Sturz-Bewegung.
2. Achsel-Naht des oberen Vorderbeins in Dead: 2c 6 / Junges 11 Dreieck-Paare, 1,5 / 1,4 cm (innerhalb A3).
3. Junges Braun: vier Beine fast parallel quer, wirkt steif (K2; mehr Staffelung kostet Hautdehnung ueber heute).
4. Obere Beine erreichen den Boden nicht; grosse Baeren oberes Hinterbein waagerecht in der Luft (Spiel ~48 cm) (K1).
5. Sicht: von vorn (az 0) beim 2c Hinterpfote zu 40 % hinter der oberen Hinterpfote (eigenes Mass; das Mass der Bauer sagt 0,06 -- anderes Verfahren);
   von hinten (az 180) die untere Vorderpfote der grossen Baeren fast ganz verdeckt. Liegt an der Seitenlage (K5).
6. Sturz-Plumps: Vanilla-Ton bei 0,90 s, Rumpf liegt erst ab Bild 41/42 (1,37 s) (K3).

**Rennen (nur gemessen, Run byte-gleich):** Junges schwebt in Bild 6-9 bis +3,61 cm (Spiel +1,26 cm, Bild 7) und sinkt in Bild 11 -3,31 cm ein (Spiel
-1,16); Junges Braun +3,34 (Spiel +1,17) / 0; zum Vergleich Gross 2c +3,22 / -2,98 (Spiel +4,35 / -4,02). Deckt sich mit BAU_JUNGE.md (J3).

## 6. Fragen fuer Kevin

* **K1** Die oberen Beine liegen nicht am Boden, sie haengen frei (Spiel: gross ~21 / 48 cm, Junge ~12 cm). So lassen?
* **K2** Junges Braun liegt steifer (Beine quer, parallel). Darf die Haut an wenigen Stellen staerker gedehnt werden als heute, damit die Beine
  weiter gestaffelt liegen -- oder so lassen?
* **K6** Kleine Hautfalten am Ellbogen (Gewichte, in Spielgroesse nicht zu sehen): lassen oder spaeter ein Gewichte-Lauf?
* **K3** Der Plumps-Ton kommt ~0,4 s vor dem Aufschlag: so lassen?
* **K5** Von hinten/Rueckenseite sind nicht alle Pfoten zu sehen (wie beim echten Tier): ok?
* **J3** Junges im Rennen: kurze Flugphase 1,3 cm, kurz 1,2 cm im Boden -- spaeter angehen?

## 7. Kevins Test (nach dem Einbau; nicht gespielt)

Spiel neu starten (Modelle laden nur beim Start). Einzelspieler mit Debug. Befehle aus `NCBearBenchCub.lua` (nur Testhilfe):
`NCBear_CubHere()`, `NCBear_CubTame(100)`, `NCBear_CubKill()` -> Junges Klassisch faellt und liegt; danach `NCBear_CubClean()` (raeumt auf, Sperre weg),
fuer Junges Braun dasselbe mit `NCBear_CubLook("gen")` vor dem Kill; fuer den grossen Baeren vor dem Kill `NCBear_CubGrow(100)`, dann
`NCBear_CubLook("std")` bzw. `("gen")` / `("foto")`. Ansehen: Pfoten frei, liegt auf, kein Sprung am Ende des Sturzes.

## 8. Dateien

* Ergebnis (unveraendert geprueft): `out/42/media/models_X/Skinned/NCBear.glb` dc50d350be8179de576d2ec7251ce2ff, `NCBearGen.glb` 867b558b4b05d3878d365ebd80dcaf31,
  `NCBearCub.glb` 8a1b1e2792dfe06891bcf7d845a5587c, `NCBearCubGen.glb` = `NCBearBenchCubGen.glb` dae9dbed40ff4fa78ac74b38da466455, `out/md5.txt`.
* Neu von mir: `GEGEN_1.md` (dies), `bilder/KEVIN_liegen.png`, Ordner `gegen1b/` (werkzeug/, dump/, mess/, render/, blatt/, wieder/).
