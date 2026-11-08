# Baer: runderes Spielnetz (Lauf baer-anim, Modellbauer)

Stand 08.11.2026, Blender 5.2.3, PZ 42.21. **Offline gemessen und gerendert, nicht gespielt.** Gerendert nur auf der RTX 4090
(OPTIX), vor jedem Render `tasklist` geprueft (einmal lief das Spiel: in der Zeit nur gerechnet, nicht gerendert).

Kevin: *"das gesicht also der kopf vom baeren passt so nur der rest ist so eckig"*. Ergebnis: Rumpf, Beine und Pranken sind
rund, der Kopf ist derselbe, alle zehn Clips bewegen sich bit-gleich. Bilder: `anim_modell_vergleich.png` (alt gegen neu),
`anim_modell_ursache.png` (woher die Ecken kamen).

## 1. Ursache (mit Bild-Belegen in `anim_modell_ursache.png`)

Das Spielnetz entsteht in `baer_export.py` Stufe `netz` aus einer "Fellhuelle": Haut nach aussen schieben, bis sie die
Fell-Umrisse von 38 Ansichten verlaesst. Vier Stellen im Bauweg machen daraus Ecken und Hubbel:

| # | Stelle | Befund | Wirkung |
|---|---|---|---|
| 1 | `baer_quelle.py` Rumpfhaut: Metabaelle, dann Voxel **5,2 cm** + 8x glaetten | 3.988 Punkte, Kante im Mittel 4,5 cm, Knick 7,8 Grad (90 %: 17 Grad) | Im Hochmodell verdeckt das Fell sie; die Huelle schiebt entlang der Normalen 9-11 cm nach aussen und vergroessert jeden Knick zu Graten |
| 2 | `huelle_schaelen` mit 16 Stufen bis 15 cm | Fellabstand nur in **1-cm-Stufen** (12 verschiedene Werte), danach 4x geglaettet | Terrassen, am deutlichsten als Querbaender an den Beinen (Bild A) |
| 3 | "Zotteln" (`buschel_rauschen`) | Ausschlag bis **6,5 cm**, Wellen 16-43 cm lang | Das sind Kevins "Hubbel": Rest nach Quadrik-Ausgleich in 8 cm steigt von 1,0 auf **4,1 mm** (Bild B) |
| 4 | Verringern auf 13.400 Dreiecke, Kopf aufgeblasen | Rumpf bekommt 11.101 Dreiecke, die Quadrik haelt die Hubbel als scharfe Kanten | 27 % der Rumpfkanten knicken ueber 20 Grad (Bild C, Draht) |

Normalen waren **nicht** die Ursache: Netz und GLB sind glatt schattiert (`shade_smooth`, Export mit Normalen).

## 2. Was gebaut ist

| Datei | Aenderung gegen das Original (das Original bleibt) |
|---|---|
| `baer_quelle_anim.py` | Zusaetzlich `baer_koerper_rund` = dieselbe Rumpfhaut mit 2 Stufen Catmull-Clark (unsichtbar im Render). Abstand zur alten Haut im Mittel -0,7 mm, hoechstens 4,7 mm; Knick 1,8 statt 7,8 Grad. Fell, Rig, Kopf, Pfoten des Hochmodells unveraendert. |
| `baer_export_anim.py` | Stufen `diagnose`, `netz`, `backen`, `kopfprobe`. Liest die vorhandenen Ansichten (`_arbeit/baer_spiel/ansichten`, nur lesen, nicht neu gerendert) und das alte Spielnetz (Kopie vom NCBearTest-Stand 08.11. unter `_arbeit/baer_anim/modell/alt/`). |
| `baer_kampf_anim.py` | Kopie von `baer_kampf.py`; Quelle waehlbar (Argument 2, Vorgabe das neue Netz), Liegehoehe der Sterbe-Clips aus Datei (Argument 3). Sonst Zeile fuer Zeile gleich. |
| `baer_tier_anim.py` | dieselben zwei Aenderungen; nur fuer `NCBearDeer.glb` (Rueckfall) benutzt. |

Neuer Weg in `netz`: runde Haut, schaelen in 2,5-mm-Stufen an weichgezeichneten Umrissen (Gauss 1,5 Pixel), Schaelrichtung
24x statt 8x geglaettet, Felldicke 30x statt 4x geglaettet, Fellgrenze am Rumpf 1 cm weiter, **keine Zotteln**, zweite
Voxelrunde 9,5 mm, volumentreu glaetten (Taubin 25x; Gesicht 0, Zehen 25 %), Falten **nur am Rumpf** auffuellen (Achsel,
Leiste, Bauchrand; ab Knie-/Ellbogenhoehe aufwaerts), Stummelschwanz abstumpfen. Dann wird der **alte Kopf** angesetzt:
Rumpf nahe am Kopf auf die alte Flaeche gezogen, alles im Kopfbereich weg, Naht als Dreiecksstreifen an den alten Kopfrand,
Band von 10 cm um die Naht geglaettet (Kopf als fester Rand), verringert mit festgehaltenem Kopf, alte Krallen dazu.

UV: nur der Rumpf neu (Rumpf in vier Stuecke geteilt: links/rechts, vorn/hinten). Kopf- und Krallen-Inseln bleiben, wo sie
sind. Blender packt um die festen Inseln herum und liess dabei oben ein Fuenftel frei; deshalb packt danach ein eigenes
Raster-Packen (FFT, 4 Drehungen, mindestens 4 Pixel der 1024er Textur Abstand) alle Rumpf-Inseln in die ganze freie Flaeche.
Die drei Flecken fuer Gaumen, Zunge, Zahn (`baer_kampf.py` FLECK_*) bleiben frei (geprueft: 0 Inseltexel darin).

Textur: `backen` wie im Original (Ansichten auf den neuen Rumpf projiziert, gleiche Nacharbeit, 2048), danach Kopf- und
Krallen-Texel unveraendert aus der alten Textur. Im Spiel weiter 1024 (`Body/NCBear.png`, 2x2 gemittelt wie bisher).

## 3. Messungen alt gegen neu (`pruef_netz.py`, `volumen.py`, Spielmeter)

| | alt | neu |
|---|---|---|
| Dreiecke FBX (Rumpf / Kopf / Krallen) | 14.228 (11.101 / 2.295 / 832) | 17.626 (14.499 / 2.295 / 832) |
| Dreiecke GLB nach Importer (mit Maul) | 14.642 | **18.040** (Grenze 20.000) |
| Rumpf: Knick zwischen Nachbarflaechen, Mittel / 90 % | 15,7 / 32,7 Grad | **6,5 / 14,4 Grad** |
| Rumpf: Kanten ueber 20 Grad Knick | 27,4 % | **5,7 %** |
| Hubbel (Rest nach Quadrik in 8 cm), Mittel / 90 % / max | 4,4 / 9,4 / 34,8 mm | **1,5 / 4,0 / 17,1 mm** |
| umgeklappte Flaechen | 16 | 1 |
| Volumen | 0,717 m3 | **0,759 m3 (+6 %, mehr Fell)** |
| Oberflaeche | 6,14 m2 | 5,91 m2 (weniger Beulen) |
| Schattenriss Seite / oben / vorn | 1,335 / 1,227 / 0,860 m2 | 1,341 / 1,234 / 0,863 m2 (gleich gross) |
| Masse x, y, z | -0,798..1,157, +-0,50, 0..1,164 | -0,803..1,157, +-0,49, 0..1,159 |
| UV-Flaeche Rumpf | rund 0,38 der Textur | **0,47** (rund 15 % mehr Texel je cm) |
| ein Netz, ein Material, Kanten mit != 2 Flaechen | ja, ja, 0 | ja, ja, 0 |

## 4. Kopf: unveraendert bis auf den Nahtrand (`kopfprobe`, beide FBX zurueckgelesen)

- **Krallen: 456 von 456 Punkten bit-gleich.**
- **Kopf: 1.033 von 1.182 Punkten bit-gleich.** Die 149 anderen liegen alle **hoechstens 4,5 cm von der Kopfnaht** (Nackenfell
  hinter Wange und Ohr), verschoben im Mittel 4,9 mm, hoechstens 16,9 mm. Kein verschobener Punkt gehoert zu Ohr, Auge oder
  Schnauze (Masken aus `regionen`: 0), naechster zur Ohrmitte 7,1 cm (bis 7 cm um jede Ohrmitte ist gesperrt), zum Auge 27 cm.
  Grund: der alte Kopfrand trug selbst Zotteln und einen Knick; mit festem Rand blieb am Hals eine Kerbe stehen
  (Nahbild "Kopfnaht" im Vergleichsblatt). Anders ginge es nur mit sichtbarer Stufe.
- Alle 3.127 Kopf- und Krallenflaechen gleich verbunden, **UV-Abweichung 0**; Kopf- und Krallen-Texel aus der alten Textur.
- Maul aus `baer_kampf_anim.py` identisch gebaut: 41 Schnittkanten, 40 Punkte verdoppelt, Beutel 282, Zaehne 48 Punkte,
  289 Kieferpunkte (alt dieselben Zahlen).

## 5. Clips und Gewichte (Importer des Spiels: `Dump.java`, `Probe.java`)

- **Alle 10 Clips bit-gleich** (DeerStag_Idle01/Walk/Run/Death/Dead, NCBear_Rear/SwipeL/SwipeR/Slam/Maul): gleiche
  Abtastzeiten, Schluessel und Modellmatrizen Abweichung 0,00e+00 (`glb_pruef.py`). Knochen, Namen, Eltern gleich.
- Die Liegehoehe der Sterbe-Clips rechnet `boden_liege()` aus der Haut. Sie wird jetzt einmal mit dem **alten** Netz gerechnet
  (`liege_alt.json`) und fuer das neue Netz geladen. Mit dem neuen Netz liegt im Tot-Bild nichts im Boden (tiefster Punkt
  0,0001 m, Becken 1,5 cm statt 0,6 cm ueber dem Boden).
- Gegenprobe der Kopien: `baer_kampf_anim.py` und `baer_tier_anim.py` mit dem **alten** Netz ergeben `NCBear.glb`,
  `Body/NCBear.png` und `NCBearDeer.glb` **byte-gleich** zu NCBearTest (MD5 2e9a6d17..., 58a4ea41..., c9841747...).
- Gewichte neu aus denselben Formeln: Summe 1,0000, hoechstens 4 Einfluesse, dieselben 19 Knochen mit Gewicht.
- Dehnung der Rumpfkanten (99,5 % / max), alt -> neu: Walk 1,69/3,72 -> 1,75/3,79; Run 2,12/4,18 -> 2,34/4,37; Idle
  1,16/1,40 -> 1,16/1,36; Death 2,13/4,59 -> 2,28/4,12; Rear 2,50/4,79 -> 2,83/4,76; Slam 2,91/6,17 -> 3,32/5,93; Hieb
  2,92/7,32 -> 3,35/6,87. Etwas mehr im 99,5-%-Wert: die gefuellten Achseln und Leisten sind mehr Haut ueber dem Gelenk.
  Groesste Dehnung bleibt am Handgelenk (wie alt). Fuer die neuen Kampfclips beachten.
- Unterschied ohne Wirkung: `Bip01_L_Toe0` (an keinem Punkt ein Gewicht, alt wie neu) liest der Importer jetzt mit echter
  Offset-Matrix statt Identitaet (`Probe`: bones 22 statt 21). Kein Punkt haengt daran, Clips gleich.

## 6. Zwischenstand fuer den Animator

Liegt in `_arbeit/baer_anim/mod/42/media/` (dort ersetzt, vorher MD5 geprueft: noch der Stand von NCBearTest) und
gleich in `_arbeit/baer_anim/modell/mod_neu/42/media/`:

| Datei | MD5 |
|---|---|
| `models_X/Skinned/NCBear.glb` (neues Netz, neue Gewichte, alle 10 Clips wie heute) | ddb95359... |
| `models_X/Skinned/NCBearDeer.glb` (Rueckfall) | fa2bcb38... |
| `textures/Body/NCBear.png` (1024, mit Maul-Flecken) | a800c084... |
| `models_X/WorldItems/NCBear.fbx` (Spielnetz ohne Knochen; Eingang fuer `baer_kampf_anim.py`) | (traegt Zeitstempel) |
| `textures/WorldItems/NCBear.png` (2048) | |

**Neue Clips bauen:** in `baer_kampf_anim.py` die Kampfclips aendern und aufrufen mit
`blender --background --factory-startup --python baer_kampf_anim.py -- ZIEL "" C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_anim/modell/liege_alt.json`
(leeres Argument 2 = neues Netz). **Ohne die Liege-Datei** rechnet es die Liegehoehe aus dem neuen Netz und Death/Dead
weichen ab. Pruefen: `_arbeit/baer_anim/modell/lauf_glb.sh` (baut, liest mit `Dump.java`, vergleicht mit dem alten GLB).
Das Netz neu bauen: `_arbeit/baer_anim/modell/lauf.sh netz backen kopfprobe pruef` (rund 4 Minuten, ohne GPU).

Item-Icon (`textures/Item_NCBear.png`) ist nicht neu gerendert.

## 7. Unsicher, offen

1. **Nicht gespielt.** Ob es im Spiel so rund wirkt, entscheidet Kevins Blick (Licht im Spiel wie `basicEffect` nachgebaut).
2. Am Hals bleibt ein weicher Wulst, wo der alte Kopfrand dicker ist als der neue Rumpf (keine Kerbe mehr). Ganz weg ginge er
   nur, wenn mehr vom Kopf mitdarf.
3. Der Rumpf ist glatter; Fellstraehnen zeigt nur noch die Textur. Spitze Zotteln im Umriss waeren der Lauf "baer-fell".
4. Stummelschwanz: ein kleiner runder Knubbel hinten, wie im Hochmodell.
5. Mehr UV-Naehte am Rumpf (Mittellinie, Mitte des Rueckens); im Bild von oben keine sichtbar.

Statisch geprueft und offline gemessen, nicht gespielt.
