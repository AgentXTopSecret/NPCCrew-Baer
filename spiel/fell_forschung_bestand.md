# Lauf baer-fell, Forschung A: Bestand messen, Ziele festlegen

Stand 08.11.2026 abends, PZ 42.21, Blender 5.2.3. **Statisch und offline gemessen/gerendert, nicht gespielt.**
Ausgang = Stand im Spiel: `Zomboid/mods/NCBearTest/42/media` (nur gelesen), GLB MD5 `4cfe4f29a21b3e5063a0dec46b8dfb5e`,
`Body/NCBear.png` MD5 `a800c084...` (1024), `WorldItems/NCBear.png` MD5 `eb717769...` (2048). Kopien in `bestand/`.
Das GLB wurde mit dem Importer des Spiels gelesen (`_arbeit/baer_spiel/harness/Dump.java`), `bestand/dump.txt` ist byte-gleich
zu `_arbeit/baer_anim/anim/dumpfin.txt`. Alle Renders: RTX 4090, OptiX + OptiX-Entrauscher, vor jedem Render `tasklist`
(Spiel lief nie) und Sperre `_arbeit/baer_fell/gpu.lock` (`werkzeug/gpu_render.sh`). Nichts in die Test-Mod oder nach NPC Crew geschrieben.

## 0. Kurz

1. Kevins Bilder lassen sich nachstellen (Bl. `bilder/bestand_rear.png`, `bestand_sitzen.png`): Aufrichten von vorn = Kamera
   az 0/30 Grad, Sitzen = az 300/30 Grad (rechte Seite, leicht von vorn). Die schwarzen Loecher sind die **Hinterfuss-Sohlen als
   flache, runde Scheibe am Ende einer Beinroehre**, Textur fast schwarz (Luma-Median 15-22 von 255).
2. **Die Annahme "verdeckt beim Backen" stimmt am Spielnetz nicht.** 95-100 % der Texel von Achsel, Brust, Bauch, Innenbein,
   Kehle, Sohle wurden unter weniger als 37 Grad gesehen (Innenbein hinten 86 %). Die Unterseite ist dunkel, weil schon die
   Back-Ansichten dort dunkel sind (8-31 % der Rueckenhelligkeit, Sohle 4-6 %) - und das kommt aus der **Fellfarbe des Hochmodells**, nicht vom
   Licht der Ansichten (Licht-Probe: Verhaeltnis unten/oben 0,42 / 0,43 / 0,43 bei drei Lichtern). Im Spiel bekommt die Unterseite
   dazu nur Umgebungslicht 0,4 statt bis 0,775. Ergebnis im Spiel: Unterseite 0,19-0,35, Sohle 0,11-0,16 der Rueckenhelligkeit.
3. "Verschmiert": die Ansichten widersprechen sich an der Unterseite 1,2- bis 2,0-mal so stark wie am Ruecken (Mischung aus vielen
   Ansichten), dazu Dehnung beim Aufrichten/Hieb. Der helle Streifen innen an den Hinterbeinen kommt aus den waagerechten
   Schraeg-Ansichten `k_h045`/`k_h315`, die durch die Luecke unter dem Bauch schauen (14,7 % der Innenbein-hinten-Texel).
4. Dehnung je Dreieck (groesste Hauptdehnung, ohne festen Kopf): 99,5 % bei 2,95-4,13 in Rear/Hieb/Slam/Sit, Hoechstwerte
   5,4-14,2. Achsel bis 8,2 (Hieb R), Brust bis 4,5 (Hieb L), ein Schritt-Dreieck zwischen den Hinterbeinen bis 14,2.
5. Dreiecke: 18.040 im GLB, Budget 20.000, Reserve 1.960.
6. Wichtiger Nebenfund: Modell-Texturen werden nach der Spieler-Option "Max. Texturgroesse" gedeckelt, **Vorgabe 256**. Kevin
   hat 2048 eingestellt; die meisten Spieler sehen den Baeren mit 256. Alles muss deshalb auch bei 256 tragen.

## 1. Kevins Spielbilder nachgestellt

Werkzeug `werkzeug/render_bestand.py` (Erweiterung von `_arbeit/baer_anim/anim/render_anim.py`): haeutet das GLB genau wie der
Importer (Punkte, Gewichte, Offsets, Clip-Matrizen aus dem Dump), Kamera orthografisch, az = Grad um den Baeren (0 = von vorn,
+90 = seine linke Seite), el = Grad ueber dem Boden (Spiel 30). Shader "spiel" wie bisher (`render_glb.py`, `render_modell.py`):
Textur x min(1, 0,4 + 0,375 x Lambert), Licht (0,2,5); "ton" = graue Form mit Sonne. Die Richtung von Kevins Bildern wurde aus
acht Richtungen bestimmt (`mess/richtung_blatt.png`).

| Blatt | Inhalt |
|---|---|
| `bilder/bestand_rear.png` | Kevins Bild neben Nachbau (30 Grad, vorn tief, vorn-unten, schraeg), Form (Ton), Vorderpranken nah, Helligkeit der Back-Ansichten, Dehnung |
| `bilder/bestand_sitzen.png` | Kevins Bild neben Nachbau az 300, von vorn, vorn tief, Hinterfuss nah (Textur und Ton), alle Sohlen von unten, Dehnung |
| `bilder/bestand_liegen.png` | Tot (DeerStag_Dead) Bauch- und Rueckenseite, von hinten, von oben, Form; Ruhe von hinten |
| `bilder/bestand_regionen_helligkeit.png` | Regionen am Koerper (Ruhe vorn-unten, Seite, unten, hinten-unten, Rear, Sit), darunter Helligkeit der Ansichten und im Spiel |
| `bilder/bestand_dehnung.png` | Dehnung je Dreieck (Hoechstwert ueber den Clip) in Run, Rear, Sit, Slam, StandUp, Hieb L |
| `bilder/backqualitaet.png` | sechs Karten ueber der UV (Abschnitt 2) |

Was die Bilder zeigen (mit den Messungen unten):
- **Aufrichten:** Brust/Bauch dunkelbraun, Vorderpranken flache Schaufeln mit Knick am Handgelenk (Ton: Hautlappen oben),
  Hinterbeine Saeulen mit hellem Streifen innen, Fuesse kleine Klumpen. Rumpf von vorn breiter unten als oben: Breite ohne Arme
  0,95-0,97 m in 0,4-0,8 m Hoehe, 0,85-0,86 m in Schulterhoehe 1,3-1,5 m (Verhaeltnis 0,88) - das ist Kevins "Ei".
- **Sitzen:** die Hinterfuss-Sohle ist das runde Ende einer Roehre (Ton-Nahbild), Durchmesser rund 25 cm, Textur fast schwarz.
  Von unten (Ruhe) sind alle vier Sohlen runde Scheiben ohne Ballen; nur die Zehen-Hoecker vorn haben Form.
- **Liegen:** Bauchseite dunkel mit hellen Streifen innen an den Beinen; Form: Falten an Ellbogen und Achsel (Ton). Gemessen in
  DeerStag_Dead: 1.269 Rumpfdreiecke auf unter 50 % gestaucht, 408 unter 30 % (Achsel 165, Ellbogen 75), `werkzeug/falten.py`.
- **Von hinten:** Hinterteil einheitlich dunkel (Textur 0,26, Struktur 0,60 des Rueckens) - Kevins "Klumpen".

## 2. Back-Qualitaet ueber der UV (`bilder/backqualitaet.png`, Zahlen `mess/backqualitaet.json`)

`werkzeug/backqualitaet.py` rechnet die Projektion von `baer_export_anim.py` `stufe_backen_anim` (Zeilen 1472-1530) nach: dieselben
37 Ansichten (`_arbeit/baer_spiel/ansichten/kameras.json`, Kameras aus `baer_export.py:91-107`), derselbe Tiefenpuffer am Spielnetz,
Toleranz 0,030/0,014, Gewicht cos^7, cos >= 0,2, Alpha > 0,45, Kopfmaske. **Gegenprobe: "gesehen 0,9995 der Texel" wie im
Back-Protokoll** (`_arbeit/baer_anim/modell/log/backen.log`). Je Texel (1024): bester Winkel, mittlerer Winkel, knapp verdeckt,
Helligkeit der Ansichten (vor HELL 1,95), Uneinigkeit der Ansichten (gewichtete Streuung/Mittel).

Regionen (`werkzeug/regionen.py`, am Lowpoly mit den Gewichten aus dem GLB; Bild `bestand_regionen_helligkeit.png` oben):
Sohle = Hand/Fuss-Gewicht > 0,45, unter 6 cm, Normale nach unten; Kehle = Hals/Kopf-Gewicht, Normale nach unten, vor x 0,42;
Achsel = bis 22 cm vom Oberarm, Rueck-/Innen-/Unterseite; Leiste = bis 26 cm vom Oberschenkel, Vorder-/Innen-/Unterseite
(schliesst die Schenkel-Vorderseite ein); Innenbein = Beingewicht > 0,5, Normale zur Mitte; Brust; Bauch; Hinterteil;
Referenz Ruecken/Flanke. Die Regeln sind Naeherungen; die Bilder zeigen, dass sie an der richtigen Stelle sitzen.

| Region | Dreiecke | m2 | Texel/cm2 (1024) | Winkel gut | Ansicht hell | Textur hell | **im Spiel hell** | Uneinigkeit | Struktur |
|---|---|---|---|---|---|---|---|---|---|
| Sohle vorn (2) | 579 | 0,13 | 14,2 | 100 % | 0,04 | 0,16 | **0,11** | 1,51 | 0,47 |
| Sohle hinten (2) | 454 | 0,15 | 14,2 | 100 % | 0,06 | 0,23 | **0,16** | 2,01 | 0,58 |
| Kehle | 320 | 0,06 | 10,9 | 100 % | 1,00 | 1,03 | 0,70 | 0,49 | 0,97 |
| Achsel | 817 | 0,31 | 9,4 | 99 % | 0,19 | 0,36 | **0,27** | 1,28 | 0,82 |
| Leiste/Schenkel vorn | 1.476 | 0,52 | 9,2 | 97 % | 0,31 | 0,52 | 0,35 | 1,18 | 0,77 |
| Innenbein vorn | 626 | 0,19 | 9,3 | 95 % | 0,12 | 0,31 | **0,22** | 1,28 | 0,95 |
| Innenbein hinten | 630 | 0,21 | 10,0 | 86 % | 0,08 | 0,24 | **0,19** | 1,49 | 1,04 |
| Brust | 356 | 0,10 | 10,2 | 95 % | 0,75 | 0,86 | 0,58 | 0,64 | 1,13 |
| Bauch | 88 | 0,11 | 6,0 | 100 % | 0,14 | 0,28 | **0,19** | 1,40 | 0,87 |
| Hinterteil | 1.372 | 0,58 | 8,4 | 100 % | 0,12 | 0,26 | **0,23** | 1,66 | 0,60 |
| Ruecken/Flanke (=1) | 3.507 | 1,74 | 8,7 | 100 % | 1 | 1 | 1 | 1 | 1 |
| Kopf (fest) | 2.362 | 0,53 | **40,0** | 100 % | 1,76 | 1,21 | 0,87 | 0,44 | 1,08 |

"im Spiel hell" = Textur x Spiel-Licht in Ruhehaltung, relativ zum Ruecken. Absolut (sRGB-Mittel): Ruecken (122,86,57),
Bauch (49,29,18), Hinterteil (48,27,16), Sohle vorn (39,28,21). "Struktur" = mittlere Abweichung von einer 7x7-Unschaerfe.

Ursachen mit Fundstelle:
- **Fellfarbe des Hochmodells:** Melanin +0,13 an den Beinen, -0,12 am Ruecken, helle Spitzen (`baer_quelle_anim.py:1637`,
  `:1641`, `:1648`), Grundfarbe "Beine und Bauch dunkler" (`:1004-1006`). Sohlen/Ballen der Zehen-Netze fast schwarz
  (0,014/0,011/0,010 linear, `:1529`), beim Backen noch einmal abgedunkelt (`baer_export_anim.py:410-413`); die Aufhellung der
  Unterbeine x1,30/x1,42 (`:399-400`) gleicht das nicht aus.
- **Licht der Ansichten ist nicht die Ursache** (`werkzeug/licht_probe.py`, `render/licht/licht_probe.json`): Hochmodell mit Fell,
  Helligkeit k_bot/k_top 0,42 (wie gebacken), 0,43 (gleichmaessige Welt), 0,43 (Kopflicht aus Kamerarichtung); k_u090/top
  0,41/0,42/0,37. Neu rendern mit anderem Licht allein hilft also kaum.
- **Spiel-Licht:** `animalEffect.frag` (Vanilla, `media/shaders`) rechnet Textur x min(1, Umgebung + Lampen x Lambert). Nach unten
  zeigende Flaechen bekommen nur die Umgebung; im Nachbau 0,4 gegen bis 0,775 oben (Faktor 1,9).
- **Uneinigkeit:** an der Unterseite mischen sich viele schraege Ansichten (bestes Bild fuer Achsel: `k_h135`/`k_h225`/`k_u150`/`k_u210`),
  das Fell ist 9 cm dick (Huelle zur Haut: Median 8,8-9,0 cm in Achsel/Brust/Bauch, Sohle 1,5-3,2 cm) - Parallaxe zwischen den
  Ansichten verwischt die Straehnen.
- **Back-Pose (Abschaetzung, nur Geometrie, `mess/posen.npz`):** Spreizpose (Beine 40/35 Grad nach aussen), Aufrichten 1,3 s,
  Sitzen, Tot am Spielnetz mit denselben 22 Koerperkameras: der Winkel wird kaum besser (mittlerer bester cos Ruhe 0,949,
  Spreizpose 0,952; Ruhe+Spreiz+Rear zusammen 100 % "gut" in jeder Region statt 86-100 %). Der Gewinn einer Back-Pose waere also nicht der Winkel,
  sondern freie Sicht ohne Durchblick durch die Bauchluecke und weniger Mischung - das ist nur mit echten Renders messbar.

## 3. Dehnung je Dreieck (`mess/dehnung.json`, `mess/dehnung_ohne_kopf.json`, Karte `bilder/bestand_dehnung.png`)

Mass: groesste Hauptdehnung sigma1 der Abbildung Ruhe -> Pose je Dreieck (wie stark die Textur in der schlimmsten Richtung gezogen
wird), Hoechstwert ueber alle Bilder des Clips; ohne Kopf/Krallen/Maul, ohne Kanten < 7,4 mm (wie `streck.py`) und ohne Splitter
(Hoehe < 2 mm); 14.206 von 18.040 Dreiecken zaehlen. Zum Vergleich mit `anim_clips.md` die alte Kantendehnung (Kanten max).

| Clip | 99,5 % | max (Ort) | > 3 | > 2 | Achsel | Brust | Bauch | Leiste | Innenbein v | Innenbein h | Kehle | Kanten max (alle Kanten wie `streck.py`) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Walk | 3,03 | 5,71 (Innenbein h) | 77 | 670 | 3,95 | 2,66 | 1,52 | 2,68 | 4,49 | 5,71 | 1,61 | 3,79 |
| Run | 3,52 | 10,85 (Innenbein h) | 192 | 1.091 | 4,58 | 3,23 | 1,77 | 4,69 | 5,33 | 10,85 | 1,75 | 4,37 |
| Death/Dead | 3,16 | 14,03 (Innenbein h) | 91 | 881 | 3,78 | 3,36 | 1,27 | 4,38 | 6,41 | 14,03 | 1,82 | 4,12 |
| **Rear** | 3,60 | 14,00 (Innenbein h) | 233 | 1.181 | 3,29 | 1,88 | 3,32 | 5,17 | 5,14 | 14,00 | 1,99 | 4,99 |
| **SwipeL** | 4,13 | 9,99 (Innenbein v) | 233 | 740 | 6,06 | 4,50 | 2,15 | 1,58 | 9,99 | 3,03 | 1,63 | 5,41 |
| **SwipeR** | 4,10 | 8,21 (Achsel) | 256 | 729 | 8,21 | 4,01 | 2,44 | 1,57 | 4,93 | 2,20 | 1,77 | 5,87 |
| **Slam** | 3,90 | 6,90 (Innenbein v) | 244 | 893 | 6,35 | 3,06 | 1,98 | 2,22 | 6,90 | 5,05 | 1,42 | 4,20 |
| Bite | 2,77 | 5,50 | 50 | 261 | 1,96 | 2,42 | 1,29 | 2,38 | 4,31 | 5,50 | 2,19 | 3,80 |
| **Sit** / SitDown / StandUp | 2,95 / 3,07 / 3,16 | 13,94-14,21 (Innenbein h) | 65-109 | 619-960 | 2,65-3,45 | 3,12-3,18 | 2,26-2,28 | 5,00-5,16 | 2,12-2,31 | 13,94-14,21 | 3,14-3,45 | 4,54-5,16 |
| Eat | 1,80 | 3,35 | 1 | 23 | 1,57 | 2,33 | 1,25 | 1,20 | 3,35 | 1,41 | 2,39 | 3,00 |
| Idle | 1,29 | 1,66 | 0 | 0 | | | | | | | | 1,33 |

- Der Wert 14 ist **ein** Dreieck im Schritt zwischen den Hinterbeinen (Ruhe x -0,40, y 0,08, z 0,23 m; Kanten 13-38 mm), wo die
  Gewichte von linkem und rechtem Oberschenkel aufeinandertreffen; es kippt in jedem Clip mit gebeugten Hinterbeinen, auch in den
  Vanilla-Clips. Zweiter Schwerpunkt: Achsel/Rippenbogen und Unterseite Oberarm bei Hieb und Slam (Karte), dritter: Innenseite der
  Hinterbeine beim Aufrichten und Sitzen (gelb-orange, 2-4-fach).
- Gewichte heute: Oberarm (75) und Oberschenkel (65) tragen fast nichts; die Wurzel der Beine haengt an Becken/Brust und Unterarm/
  Unterschenkel (`werkzeug/info.py`). Der Uebergang Rumpf->Bein ist dadurch kurz.

## 4. Dreiecke, UV, Texel

- GLB nach Importer: **18.040** = Rumpf 14.499 + Kopf 2.295 + Krallen 832 + Maul/Zaehne 414 (`baer_kampf_anim.py`). Budget 20.000.
- UV (1024): Rumpf 47 %, Kopf 20 % der Flaeche. Kopf hat **40 Texel/cm2**, Rumpf 8-10, Sohle 14. Sohlen liegen heute schon
  weitgehend auf eigenen Inseln (Tafel 2 in `backqualitaet.png`).
- **Texturdeckel:** `ModelManager.loadModelInternal` setzt fuer Nicht-Fahrzeug-Modelle `getTextureFlags()` = Flag 128
  (`_arbeit/baer_spiel/dec/ModelManager.java:1314-1349`, Jar-Lesart aus dem Lauf baer-spiel); Flag 128 deckelt nach der Option
  "Max. Texturgroesse", Vorgabe 1 = 256 (Belege `rucksack/forschung/REZEPT_ENGINE.md:572`). Kevins `Zomboid/options.ini:63`
  `maxTextureSize=4` (= 2048; diese eine Zeile gezielt gelesen, die Datei liegt ausserhalb der Suchorte dieses Auftrags).
  Vanilla-Tiere haben 256x256 (`media/textures/Body/Cow_*.png`, `DeerStag.png` u. a.). Folge: 2048 sieht nur, wer die Option
  hochstellt; bei 256 ist ein Rumpf-Texel rund 1,4 cm gross.
- **Alpha-Haarkarten (Kevins Punkt 8):** technisch moeglich - `animalEffect.frag:34-36` verwirft Texel mit Alpha < 0,01, gibt
  sonst Alpha x Texturalpha aus (`:78`); `Model.DrawChar` schaltet Alpha-Test (> 0,01) und Mischen ein und **Rueckseiten-Culling
  an** (`dec/Model.java:354-367`), abschaltbar nur fuer das ganze Modell per Modellskript `cullFace = None`
  (`dec/ModelScript.java:82-88`, Vanilla `scripts/generated/weapons/firearm/fx/muzzle_flash_models.txt:7`). Heute ist die Textur RGB
  ohne Alpha. Risiken: einseitige Karten verschwinden von hinten (Culling) oder ganze Figur ohne Culling; halbtransparente Raender
  ohne Sortierung; Mipmap/Deckel 256 duennt Haare aus. Ungeprueft im Spiel.

## 5. Wege (Vorschlag), Aufwand und Risiko

| # | Weg | Aufwand | Risiko | Wirkung |
|---|---|---|---|---|
| W1 | **Sohlen als eigene UV-Inseln** (je Pfote eine Insel, von unten projiziert, Zehen oben), **Ballen-Textur prozedural** nach dem Ballen-Plan des Hochmodells (`zehen_feld_fn`, `baer_quelle_anim.py:1501-1517`: querliegender Sohlenballen, fuenf Zehenballen im Bogen), hinten zusaetzlich langer Sohlen-/Fersenballen; dunkelgraue Lederhaut (Ballen sRGB ~85-100, Furchen ~35-45, leicht warm), feine Lederstruktur, Fellkranz am Rand, Krallen unveraendert | klein-mittel | gering (Naht Fell/Sohle) | Sohle im Spiel 0,11 -> >= 0,35, Ballen lesbar auch bei 256 |
| W2 | **Ballen-Geometrie**: Sohlenscheibe -> Sohle mit Kuppen; **Furchen nach oben einziehen statt Ballen nach unten**, damit die Auflage z = 0 bleibt (Liegehoehe, "nichts im Boden", Fussgleiten); Hand/Fuss-Gewicht 100 % | mittel (+100-150 Dreiecke je Pfote) | mittel (Sohlen-Kontakt in 15 Clips neu pruefen) | Form im Sitzen statt Roehrenende |
| W3 | **Fellfarbe nur fuer den Bake** (Kopie `baer_quelle_fell.py`): Melanin-Zuschlag Beine/Bauch +0,13 -> etwa +0,05, helle Spitzen auch unten, Ansichten neu rendern (37 Ansichten ~6 min GPU, `_arbeit/baer_spiel/ansichten.log`) | mittel | mittel (Uebergang zur alten Kopf-Textur am Hals abgleichen) | Ansicht hell Unterseite 0,08-0,31 -> >= 0,45 |
| W4 | **Ausgleich Spiel-Licht im Texturraum**: Regionsmasken (aus `regionen.py`) heben Unterseite/Hinterteil um den fehlenden Lichtanteil (bis x1,6), weiche Uebergaenge; **Straehnen**: Kontrast in 2-4 cm breiten Haarbuescheln laengs der Haarrichtung (traegt auch bei 256); **Faltenschatten** leicht (AO des Spielnetzes an Ellbogen, Achsel, Leiste, max -25 %) | klein | gering-mittel (wirkt gemalt, wenn zu stark) | im Spiel hell >= 0,40, Struktur >= 0,9 |
| W5 | **Bauchluecke sperren**: Innenbein-Texel nehmen keine waagerechten Schraeg-Ansichten (`k_h045/135/225/315`), deren Strahl unter dem Bauch durchgeht (Tiefen-Toleranz dort 0,010 statt 0,030) | klein | gering | heller Streifen 14,7 % -> <= 3 % |
| W6 | **Back-Pose-Ansichten** (Beine 35-40 Grad gespreizt, Vorderbeine vor), Hochmodell-Rig posieren, Spielnetz gleich posieren, nur fuer Achsel/Leiste/Innenbein/Bauch mischen | mittel-hoch | mittel (Haar folgt dem verformten Netz; Rueckprojektion) | Winkel kaum besser (Abschn. 2); weniger Uneinigkeit erwartet - **erst nach W3-W5, nur wenn Uneinigkeit > 1,1 bleibt** |
| W7 | **Dehnung**: Kantenschleifen um Achsel/Oberarm und im Schritt, Gewichtsverlauf Rumpf->Bein ueber 20-25 cm (geodaetisch statt Luftlinie), Oberarm/Oberschenkel echte Anteile; Achsel in Ruhe als weiche Falte statt aufgefuellt (`baer_export_anim.py` FALTEN_RUNDEN, `anim_modell.md` 5); Schritt-Mittellinie L/R glatt | mittel | mittel (Gang/Run/Sterben duerfen nicht schlechter werden; Messung je Variante 25 s mit `regionen.py`) | siehe Ziele |
| W8 | **Zotteln im Umriss**: kurze spitze Buesche nur an Umrisskanten (Rueckenlinie, Bauchfranse, Hinterkante Vorderbein, Nacken, Hinterteil), Wellenlaenge 3-6 cm, Ausschlag 0,8-2 cm, ohne langwelligen Anteil (Hubbel-Mass bleibt) | mittel (+600-900 Dreiecke) | mittel (Budget) | Umriss "fellig" ohne Beulen |
| W8b | Alpha-Haarkarten als **Probe-Variante** (eigene Datei, nicht Vorgabe), RGBA, `cullFace = None` | mittel | hoch (Abschn. 4) | nur auf Kevins Test |
| W9 | **Form hinten/vorn**: Gesaessfalte und Trennung der Schenkel, Stummelschwanz-Buesche (gegen "Klumpen"); Brust/Schulter-Fell voller, Unterbauch schlanker (gegen "Ei") | mittel | mittel (Sterbe-Liegehoehe kommt aus `liege_alt.json`, Umriss sonst) | Schulter/Huefte >= 0,95 |
| W10 | **Textur 2048** im Spiel (Kevins Punkt 2), gleiche Datei `Body/NCBear.png`; Kopf-Inseln bleiben, Kopf-Texel aus dem alten 2048er (`WorldItems/NCBear.png`) | klein | gering; Wirkung nur mit Option 2048 | Pruefbild auch in 256/512 |
| W11 | **Kopf-Variante B** (Augen tiefer/dunkler mit Lidrand, Gesicht 10-15 % dunkler) als **zweite Datei**, nicht eingebunden; Vorgabe bleibt alt | klein | keins | Kevin waehlt |

## 6. Ziele (messbar, je Lauf mit den Werkzeugen aus `werkzeug/` gegen den Bestand)

**Netz** (Dump des neuen GLB, `regionen.py`/`tabelle_dehnung.py`/`falten.py`):
- Dehnung je Dreieck (ohne Kopf/Krallen/Maul): **99,5 % <= 2,6** in jedem Clip (heute bis 4,13); **max <= 4,0** in jedem Clip
  (heute 5,4-14,2); **Achsel und Brust max <= 3,5** in Rear, Sit/SitDown/StandUp, SwipeL/R, Slam (heute bis 8,21/4,50); Wunsch 3,0.
  Kanten max <= 4,0 (heute 4,20-5,87). Idle 99,5 % <= 1,3, Walk/Run nicht schlechter als heute.
- Falten liegend (Dead): Dreiecke mit sigma2 < 0,3 <= 200 (heute 408), Achsel+Ellbogen sigma2 < 0,5 <= 120 (heute 240).
- Sohlen: je Pfote eine UV-Insel; 1 Sohlen- + 5 Zehenballen (+ Fersenballen hinten) als Kuppen 4-10 mm (Spielmeter) ueber den
  Furchen; tiefster Hautpunkt je Clip nicht tiefer als heute (`anim_clips.md` 5: bis -2,1 mm), Fussgleiten <= 0,01 Kacheln.
- Hubbel (Quadrik-Rest in 8 cm) Mittel/90 %/max <= 1,5/4,0/17,1 mm (Wert `anim_modell.md` 3); Zotteln: im Seitenumriss >= 8 Spitzen
  je Meter Umrisskante an den Zottel-Stellen, Ausschlag 0,8-2 cm.
- Schulter/Brust-Breite zu Hueft-Breite im Rear 1,3 s >= 0,95 (heute 0,88).
- Fest: **<= 19.600 Dreiecke** im GLB (400 Reserve unter 20.000), <= 4 Einfluesse, Summe 1, ein Netz/Material; alle 15 Clips
  bit-gleich (`glb_pruef.py`); Krallen 456/456 und Kopfpunkte bit-gleich ausser Nahtrand <= 4,5 cm (`kopfprobe`); Liegehoehe aus
  `liege_alt.json`; Pfade unveraendert.

**Textur** (`backqualitaet.py` + `auswertung.py` am neuen Netz, Renders der drei Kevin-Ansichten):
- Winkel "gut" >= 95 % je Region (heute Innenbein hinten 86 %).
- **Im Spiel hell** (Textur x Spiel-Licht, rel. Ruecken): Achsel, Bauch, Innenbein, Leiste, Hinterteil **>= 0,40** (heute 0,19-0,35),
  Brust/Kehle >= 0,55 (heute 0,58/0,70 halten); Sohle >= 0,35 (heute 0,11/0,16) und Ballen-Luma 85-100 sRGB, Furchen <= 50
  (Kontrast >= 35 Stufen; heute Median 15-22 ohne Muster).
- Uneinigkeit der Ansichten <= 1,1 (heute 1,18-2,01); Struktur >= 0,9 an der Unterseite, Sohle >= 1,0 (heute 0,47-0,95).
- Heller Streifen: Innenbein-hinten-Texel mit Ansicht > 0,8 Ruecken <= 3 % (heute 14,7 %).
- Pruefbild in 256, 512, 2048 (Mip-Stufen): Ballen und Straehnen bei 256 noch zu erkennen.
- Kopf-Texel der Vorgabe-Textur = alt (Differenz 0 in den Kopf-Inseln); Variante B nur als eigene Datei.

## 7. Arbeitsplan fuer zwei Bauer (getrennte Dateien, Reihenfolge Netz -> Textur)

Gemeinsam nur lesen: `_arbeit/baer_fell/werkzeug/*` (jeder kopiert, was er anpasst, in seinen Ordner), `mess/regionen.npz`,
`mess/lowpoly.npz`, Bestand `bestand/`. GPU nur mit `werkzeug/gpu_render.sh` (prueft Spiel, Sperre `gpu.lock`).

**Bauer "Netz"** - Dateien: `baer/spiel/baer_export_fell.py` (Kopie von `baer_export_anim.py`: Stufen netz, uv, kopfprobe),
`baer/spiel/baer_kampf_fell.py` (Kopie von `baer_kampf_anim.py`: Gewichte, GLB-Bau, Clips unveraendert; Texturgroesse als Argument,
FLECK_* fuer 2048 mitskalieren), Ordner `_arbeit/baer_fell/netz/`.
1. Kopien anlegen, Gegenprobe: mit unveraenderten Werten byte-gleiches GLB/PNG zum Bestand (wie baer-anim `anim_modell.md` 5).
2. Schritt-Dreieck und Achsel/Brust: Gewichte (Oberarm/Oberschenkel-Anteile, geodaetischer Verlauf, Mittellinie) und 1-2
   Kantenschleifen; nach jeder Variante `regionen.py` + `tabelle_dehnung.py` (25 s). Ziel Abschnitt 6.
3. Sohlen: Scheibe -> Sohle mit Ballen (W2), Furchen nach oben, eigene UV-Insel je Pfote; Ausgabe `netz/sohle_layout.json`
   (Mittelpunkt, Halbachsen, Drehung jedes Ballens in Spielmetern **und** UV) fuer den Textur-Bauer.
4. Zotteln an Umrisskanten (W8), Form hinten/vorn (W9), Falten liegend (W7); Dreiecke zaehlen (<= 19.600).
5. UV: Rumpf-Inseln neu packen fuer 2048 (Kopf-/Krallen-Inseln und Gaumen/Zunge/Zahn-Flecken bleiben), Attribut `region` (Nummern
   wie `regionen.json`) ins Netz schreiben.
6. Uebergabe: `netz/lowpoly_fell.blend`, `netz/NCBear.fbx`, `sohle_layout.json`, Regionsmaske 2048 (PNG), Zwischen-GLB mit der
   alten Textur zur Formpruefung; Pruefungen: kopfprobe, glb_pruef (15 Clips), Einfluesse, Liegehoehe, tiefster Hautpunkt,
   Fussgleiten, Dehnung, Falten, Hubbel; Renders Rear/Sit/Dead im Spielwinkel (Ton und alte Textur).

**Bauer "Textur"** - Dateien: `baer/spiel/baer_quelle_fell.py` (Kopie von `baer_quelle_anim.py`: Fellfarbe nur fuer den Bake, W3;
Fersenballen hinten im Hochmodell nur als Vorlage), `baer/spiel/baer_backen_fell.py` (neu: Stufen `ansichten_fell` [GPU],
`backen_fell`, `sohlen`, `kopf_b`), Ordner `_arbeit/baer_fell/textur/`.
0. (parallel zu Netz 1-4, braucht kein neues Netz) Ansichten mit geaenderter Fellfarbe in 512 an drei Kameras probieren
   (`licht_probe.py` als Vorlage), Zielwert Ansicht hell >= 0,45 der Oberseite; dann alle 37 Ansichten 2048 (~6 min GPU).
1. Nach Netz-Uebergabe: Backen auf `lowpoly_fell.blend` mit W5 (Bauchluecke), Mischung je Region, Straehnen (W4), Faltenschatten.
2. Sohlen-Textur prozedural aus `sohle_layout.json` (W1), nach Kevins Foto nachgezeichnet, nichts daraus kopiert.
3. Ausgleich Spiel-Licht (W4), Kopf-Texel unveraendert aus dem alten 2048er; Variante B als `textur/NCBear_kopfB_2048.png` (W11).
4. Uebergabe an Netz-Bauer: `WorldItems/NCBear.png` 2048 -> `baer_kampf_fell.py` baut GLB und `Body/NCBear.png` (2048 nach Kevins
   Punkt 2; 1024 als Rueckfall).
5. Pruefungen: `backqualitaet.py`/`auswertung.py` am neuen Netz (alle Zielwerte Abschnitt 6), Renders der drei Kevin-Ansichten
   neben `bilder/bestand_*.png`, Pruefbild 256/512/2048, Kopf-Differenz 0. Erst wenn W3-W5 die Uneinigkeit nicht unter 1,1 bringen:
   Back-Pose (W6).

Offen fuer Kevin: Alpha-Haarkarten nur als Probe (W8b)? Textur 2048 trotz Deckel 256 bei Vorgabe-Spielern? Kopf-Variante A/B.
Nicht Teil dieser Forschung: Galopp-Bild (7), Junges-Vergleich (9).

## 8. Werkzeuge und Daten (alle in `_arbeit/baer_fell/`)

| Datei | Zweck | Aufruf |
|---|---|---|
| `werkzeug/render_bestand.py` + `gpu_render.sh` | GLB wie das Spiel haeuten und rendern (Spiel-Licht, Ton, Farbfelder je Dreieck, Kamera az/el, Ausschnitt `ziel`/`ortho`) | `bash werkzeug/gpu_render.sh werkzeug/render_bestand.py AUFTRAG.json LOG` |
| `werkzeug/export_lowpoly.py` | Lowpoly aus `.blend` -> npz (Punkte, Dreiecke, UV, Gegend) | blender ... `-- BLEND AUS.npz` |
| `werkzeug/regionen.py` | Regionen, Flaeche/Texel je Region, Dehnung je Dreieck aller Clips (25 s) | `python werkzeug/regionen.py DUMP LOWPOLY.npz AUSORDNER` |
| `werkzeug/tabelle_dehnung.py`, `falten.py` | Dehnungstabelle ohne Kopf, Stauchung liegend | `python ...` (Pfade fest) |
| `werkzeug/posen.py` | Spreizpose + Clip-Posen am Lowpoly | `python werkzeug/posen.py DUMP regionen.npz AUS.npz` |
| `werkzeug/backqualitaet.py` | Back-Projektion nachgerechnet, je Texel Winkel/Helligkeit/Uneinigkeit, Posen-Abschaetzung (60 s, CPU) | blender ... `-- LOWPOLY.npz POSEN.npz AUS.npz` |
| `werkzeug/huelle_abstand.py` | Abstand Huelle -> Haut des Hochmodells | blender ... `-- LOWPOLY.npz AUS.npz` |
| `werkzeug/auswertung.py` | Tabellen je Region, `bilder/backqualitaet.png`, Farbfelder `mess/felder.npz` | `python werkzeug/auswertung.py` (Pfade fest auf `bestand/`) |
| `werkzeug/licht_probe.py` | Hochmodell mit Fell, 4 Ansichten x 3 Lichter | `bash werkzeug/gpu_render.sh werkzeug/licht_probe.py AUSORDNER LOG` |
| `mess/*.json`, `mess/*.npz` | alle Zahlen dieses Berichts | |

Statisch geprueft und offline gemessen/gerendert, nicht gespielt.
