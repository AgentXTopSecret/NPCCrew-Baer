# Lauf baer-fell: Bauer Netz (Sohlen, Unterseite, Gewichte, Form)

Stand 08.11.2026 spaet, Blender 5.2.3, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
Gerendert nur Kontrollbilder auf der RTX 4090 (OptiX + OptiX-Entrauscher, `werkzeug/gpu_render.sh`: Spiel lief nicht, Sperre
`gpu.lock` danach frei). Nichts in die Test-Mod oder nach NPC Crew geschrieben. Uebergabe an den Textur-Bauer: `netz/uebergabe.md`.

## 0. Kurz

1. **Gegenprobe der Kopien bestanden**: `baer_export_fell.py` (mit `BAER_FELL_AUS=1`) + `backen` + `baer_kampf_fell.py` ergeben
   Netz/UV gleich `lowpoly_anim.blend`, Textur MD5 `eb717769...` und **GLB MD5 `4cfe4f29...` byte-gleich** zu NCBearTest.
2. **Sohlen mit Ballen** in Netz und UV: je Pfote eine neue Sohle (377-463 Dreiecke) mit 5 Zehenballen im Bogen, querliegendem
   Sohlenballen, vorn Handwurzelballen, hinten langem Fersenballen; Ballen bei z = 0, Furchen 8 mm hoeher. Je Sohle **eine eigene
   UV-Insel, eben projiziert**, 2-fache Dichte (~30 Texel/cm2 bei 1024), Lage exakt in `netz/sohle_layout.json`.
3. **Dehnung stark gesenkt** durch optimierte Hautgewichte (neues Werkzeug `baer_gewichte_fell.py`): 99,5 % je Clip hoechstens
   **2,48** (vorher bis 4,13), Hoechstwert **3,37** (vorher bis 14,21), Achsel/Brust hoechstens **3,04** (vorher 8,21/4,50),
   Liegen sigma2 < 0,3: **194** (vorher 408). Alle Zielwerte der Forschung fuer das Netz erreicht bis auf Achsel+Ellbogen-Falten (154, Ziel 120).
4. **Clips 15/15 bit-gleich**, Knochen, Offset- und Bind-Matrizen gleich, Kopf und Krallen wie baer-anim, Liegehoehe aus `liege_alt.json`.
   **18.870 Dreiecke im GLB** (Grenze 19.600).
5. Form: Gesaessfalte hinten, Schultern voller, Flanken unten schlanker - im Ton-Bild nur schwach zu sehen. **Zotteln als Geometrie
   probiert und verworfen** (sehen aus wie Noppen, Hubbel und Knicke steigen; Abschnitt 4).

## 1. Gegenprobe der Kopien (byte-gleich)

| Schritt | Ergebnis |
|---|---|
| `baer_kampf_fell.py` mit Netz/Textur aus NCBearTest, `NCB_FELL_GEWICHTE=formel` (damals noch Vorgabe) | `NCBear.glb` `4cfe4f29a21b3e5063a0dec46b8dfb5e`, `Body/NCBear.png` `a800c084...` = NCBearTest |
| `baer_export_fell.py netz` mit `BAER_FELL_AUS=1` | Punkte, Dreiecke, UV je Ecke, Gegend **gleich** `_arbeit/baer_anim/modell/lowpoly_anim.blend` (exakt) |
| ... `backen` | `WorldItems/NCBear.png` `eb717769...` = Bestand |
| ... `baer_kampf_fell.py` auf diesem Ergebnis | `NCBear.glb` `4cfe4f29...` = NCBearTest |

## 2. Was gebaut ist

| Datei | Aenderung (Originale unveraendert) |
|---|---|
| `baer/spiel/baer_export_fell.py` | Kopie von `baer_export_anim.py`. Neu: `form_fell` (Form am dichten Rumpf vor dem Verringern), `sohlen_bauen` (Sohlen, `mathutils.geometry.delaunay_2d_cdt` mit dem alten Sohlenrand als Zwangskante), `uv_rumpf` mit Sohlen-Inseln (eben projiziert, `SOHLE_DICHTE` 2,0), `sohle_layout` (json), Stufe `fbx`, optional `zotteln_fell` (Vorgabe aus). Ausgaben nach `_arbeit/baer_fell/netz/` (`lowpoly_<NAME>.blend`, `netz_<NAME>.npz`). `backen` nur Pfade (und Attribut `sohle` vor dem FBX entfernt), Rechnung unveraendert. |
| `baer/spiel/baer_kampf_fell.py` | Kopie von `baer_kampf_anim.py`. Clips/Formeln Zeile fuer Zeile gleich. Neu: Vorgabe-Quelle `_arbeit/baer_fell/mod/42/media/`; Gewichte aus `NCB_FELL_GEWICHTE` (Vorgabe `netz/gewichte_fell.npz`, `formel` = alte Formel, Punkte/Dreiecke werden geprueft); `NCB_FELL_NUR_GEWICHTE` schreibt Netz + Formel-Gewichte als npz und endet. |
| `baer/spiel/baer_gewichte_fell.py` | **neu**: optimiert die Hautgewichte gegen die Dehnung aller 15 Clips (Abschnitt 3.4). |
| `baer/spiel/baer_quelle_fell.py` | **nicht angelegt**: das Netz braucht nur die Form des Hochmodells (`baer_quelle_anim.py`, nur gelesen); die Fellfarbe (W3) ist Sache des Textur-Bauers. |

**Sohlen** (`sohlen_bauen`): Sohlenflaeche je Pfote = Rumpfdreiecke mit Mitte unter 12 mm und Normale nach unten (nz < -0,6), groesste
Gruppe, Loecher geschlossen, Rand genau eine Schleife (geprueft). Ihr Rand bleibt Punkt fuer Punkt (Uebergang in den Fellkranz), das Innere
wird neu trianguliert: Ballen als Ellipsen aus der Lage der fuenf Krallen (Zehenballen 6,0 cm/5,2 cm hinter der Kralle, Sohlenballen
querliegend 17,6/16 cm breit, Handwurzelballen 4,4 x 5,2 cm, Fersenballen 20 cm lang, zur Ferse 30 % schmaler, Querfurche davor),
Ringe je Ballen, Furchen-Raster 15 mm. Hoehe: Ballen bei z = 0 (Auflage wie die alte Scheibe), Furchen `BALLEN_HUB` 8 mm hoeher,
zum Rand weich auf die Randhoehe. Geschlossen und gleich ausgerichtet (geprueft); 973 Sohlenpunkte haengen zu 100 % an Hand/Fuss.

**Form** (`form_fell`, Spielmass): Gesaessfalte an der Mittellinie hinten bis 25,8 mm tief (Breite ~4 cm, Schritt bis Schwanzansatz),
Schultern seitlich bis +24 mm, Flanken/Huefte unten seitlich bis -17 mm; Feld ueber das Netz geglaettet. Kopf, Hals, Pfoten unberuehrt.

## 3. Messungen alt gegen neu

### 3.1 Netz (`netz/pruef_netz.py` = baer-anim-Werkzeug, Quellpfad angepasst; FBX)

| | Bestand (baer-anim) | baer-fell |
|---|---|---|
| Dreiecke FBX (Rumpf / Kopf / Krallen) | 17.626 (14.499 / 2.295 / 832) | **18.456** (15.329, davon Sohlen 1.672 / 2.295 / 832) |
| Dreiecke GLB nach Importer (mit Maul) | 18.040 | **18.870** (Ziel <= 19.600) |
| Punkte FBX / GLB | 8.855 / 10.814 | 9.270 / 11.186 |
| Kanten mit != 2 Flaechen, Umklapper | 0, 1 | 0, 1 |
| Rumpf-Knick Mittel / 90 % / ueber 20 Grad / ueber 35 Grad | 6,5 / 14,4 / 5,7 % / 0,82 % | 7,4 / 15,7 / 6,9 % / 2,06 % (Ballenkanten, Falte) |
| Hubbel (Rest nach Quadrik in 8 cm) Mittel / 90 % / max | 1,5 / 4,0 / 17,1 mm | 1,6 / 4,4 / 22,1 mm (Sohlen und Gesaessfalte sind absichtlich) |
| Masse x / y / z | -0,803..1,157 / +-0,487 / 0..1,159 | -0,801..1,157 / -0,478..0,483 / 0..1,159 |
| UV-Flaeche Rumpf (samt Sohlen) | 0,473 | 0,470 (Sohlen 4-fache Texel je cm2) |

### 3.2 Kopf und Krallen (`kopfprobe`)
Krallen **456/456 bit-gleich**; Kopf **1.033/1.182 bit-gleich**, die 149 anderen nur am Nahtrand (<= 4,5 cm, wie baer-anim, naechster zum
Ohr 7,1 cm, Auge 27,5 cm); Flaechen Kopf+Krallen 3.127/3.127 gleich, **UV-Abweichung 0**. Kopf-Dehnung in allen Clips gleich dem Bestand
(Maulwinkel beim Oeffnen, z. B. Rear 6,45, wie vorher).

### 3.3 Clips und GLB (`Dump.java` + `glb_pruef.py`)
**15/15 Clips bit-gleich** (Abtastzeiten, Schluessel, Modellmatrizen Abweichung 0). Knochen 26, Namen/Eltern gleich, **Offset- und
Bind-Matrizen Abweichung 0** (dafuer werden Gewichte unter 0,01 gestrichen: sonst traegt GLB-Punkt 0 vier Einfluesse und der
Importer laesst die gewichtslosen Knochen Dummy01/Bip01/L_Toe0 mit Einheits-Offset stehen - ohne Wirkung auf die Haut, aber jetzt
gleich wie vorher). Einfluesse <= 4 (Verteilung 1/2/3/4: 3.679/2.237/1.339/2.015 Punkte), Summe 1,0000, 19 Knochen mit Gewicht wie
vorher. Liegehoehe aus `liege_alt.json`: tiefster Punkt im Tot-Bild 0,0001 m.

### 3.4 Gewichte und Dehnung (`netz/messen.py`, Mass wie `werkzeug/regionen.py`; ohne Kopf/Krallen; gegengeprueft mit regionen.py am Dump)

Weg: Formel-Gewichte wie baer-anim als Start; 6.053 freie Punkte (Rumpf ueber z 6 cm und hinter x 0,80, also auch Handgelenk, Ferse,
Hals); je Punkt nur Rumpfknochen (+ Kopf vorn, Schwanz hinten) und die Beinknochen der eigenen Seite (vorn/hinten nach x getrennt).
Energie ueber jedes 5. Bild aller 15 Clips: (sigma1-1)^2 + 6 (sigma1-1)^4 je Dreieck, Stauchung (1-sigma2)^2 x 4, Glaette ueber die
Kanten, Naehe zur Formel; dazu kein freier Punkt unter den Boden in **jedem** Bild. Projizierter Gradientenabstieg mit Schrittweitensuche,
je Punkt vorkonditioniert, 200 + 60 Runden (~11 min CPU). Abweichung von der Formel im Mittel 0,037 je Punkt.

| Clip | 99,5 % alt / Formel neu Netz / **neu** | max alt / Formel / **neu** (Ort neu) | Achsel max alt / neu | Brust max alt / neu | tiefster Punkt alt / neu (m) | sigma2 < 0,3 alt / neu |
|---|---|---|---|---|---|---|
| Idle | 1,29 / 1,30 / **1,20** | 1,66 / 1,68 / **1,30** | 1,35 / 1,18 | 1,34 / 1,15 | 0 / 0 | 0 / 0 |
| Walk | 3,03 / 3,03 / **1,95** | 5,71 / 7,11 / **2,23** | 3,95 / 2,07 | 2,66 / 1,86 | -0,0240 / -0,0240 | 1.205 / 681 |
| Run | 3,52 / 3,58 / **2,31** | 10,85 / 9,65 / **2,67** | 4,58 / 2,06 | 3,23 / 1,95 | -0,0298 / -0,0298 | 1.900 / 1.747 |
| Death | 3,16 / 3,15 / **2,07** | 14,03 / 7,78 / **2,56** (Innenbein h.) | 3,78 / 1,83 | 3,36 / 2,06 | -0,0181 / -0,0181 | 1.574 / 1.012 |
| Dead | 3,03 / 3,07 / **2,05** | 14,00 / 7,62 / **2,56** | 3,75 / 1,64 | 3,36 / 1,72 | 0,0001 / 0,0001 | **408 / 194** |
| Rear | 3,60 / 3,66 / **2,16** | 14,00 / 6,09 / **3,21** (Innenbein h.) | 3,29 / 2,44 | 1,88 / 1,76 | -0,0018 / -0,0012 | 476 / 256 |
| SwipeL | 4,13 / 4,10 / **2,40** | 9,99 / 13,09 / **2,98** (Brust) | 6,06 / 2,75 | 4,50 / 2,98 | -0,0082 / -0,0042 | 372 / 195 |
| SwipeR | 4,10 / 4,00 / **2,48** | 8,21 / 8,43 / **3,18** (Bauch) | 8,21 / 2,89 | 4,01 / 3,04 | -0,0073 / -0,0070 | 368 / 162 |
| Slam | 3,90 / 3,85 / **2,13** | 6,90 / 9,84 / **2,51** | 6,35 / 2,37 | 3,06 / 1,90 | 0 / 0 | 631 / 364 |
| Bite | 2,77 / 2,76 / **1,82** | 5,50 / 4,33 / **2,53** | 1,96 / 2,12 | 2,42 / 1,54 | 0 / 0 | 449 / 249 |
| Maul | 2,15 / 2,19 / **1,57** | 5,38 / 5,57 / **2,32** | 2,46 / 1,59 | 2,16 / 1,55 | -0,0004 / -0,0003 | 440 / 155 |
| SitDown | 3,08 / 3,15 / **1,99** | 13,94 / 7,24 / **3,09** (Hals oben) | 3,28 / 1,86 | 3,12 / 1,93 | 0 / 0 | 1.284 / 916 |
| Sit | 2,95 / 3,05 / **1,90** | 13,94 / 5,78 / **3,37** (Hals oben) | 2,65 / 1,89 | 3,18 / 2,00 | 0 / 0 | 216 / 65 |
| StandUp | 3,16 / 3,22 / **2,08** | 14,21 / 7,51 / **3,09** (Hals oben) | 3,45 / 1,85 | 3,12 / 1,93 | 0 / 0 | 1.090 / 853 |
| Eat | 1,80 / 1,76 / **1,56** | 3,35 / 3,45 / **2,25** | 1,57 / 1,60 | 2,33 / 1,60 | 0 / 0 | 262 / 71 |

"Formel" = neues Netz mit den alten Formel-Gewichten (zeigt: die Senkung kommt aus den Gewichten). "tiefster Punkt" schliesst die
Krallen ein (Walk/Run/Death unveraendert). Kantendehnung des Rumpfs (`glb_pruef`, ohne Maul) je Clip max 1,34-3,17 (vorher 1,33-5,87);
ueber alle Kanten samt Maul bleibt Rear bei 4,12 (Maulwinkel, vorher 4,99). Falten liegend (`falten_fell.py`): sigma2 < 0,5 in
Achsel + Ellbogen 97 + 57 = 154 (vorher 165 + 75 = 240; Ziel 120 nicht erreicht), Sitzen 116 + 33 (vorher 161 + 19).

| Ziel (Forschung A, Abschnitt 6) | Wert | erreicht |
|---|---|---|
| 99,5 % <= 2,6 je Clip | max 2,48 (SwipeR) | ja |
| max <= 4,0 je Clip | max 3,37 (Sit, Hals oben) | ja |
| Achsel und Brust max <= 3,5 in Rear/Sit/Hieb/Slam | max 3,04 | ja (Wunsch 3,0 fast) |
| Kanten max <= 4,0 | Rumpf 3,17; mit Maul 4,12 (Kopf bleibt) | Rumpf ja |
| Dead sigma2 < 0,3 <= 200 | 194 | ja |
| Achsel+Ellbogen sigma2 < 0,5 <= 120 | 154 | **nein** (240 -> 154) |
| Idle 99,5 % <= 1,3; Walk/Run nicht schlechter | 1,20; 1,95 / 2,31 | ja |
| Dreiecke <= 19.600 | 18.870 | ja |
| Schulter/Huefte im Rear 1,3 s >= 0,95 | mein Mass (Breite ohne Punkte mit Armgewicht >= 0,3): 0,924 -> 0,941; das Mass der Forschung (0,88) habe ich nicht nachgebaut | **offen** |
| Sohlen: je Pfote eine Insel, Ballen 4-10 mm, tiefster Punkt nicht tiefer | ja, 8 mm, tiefster Punkt unveraendert, Sohlen 100 % an Hand/Fuss (Fussgleiten = Bestand) | ja |

## 4. Zotteln (Kevins Punkt 1): probiert, verworfen

Variante `BAER_ZOTTELN=0.014` (spitze Zotteln, Abstand 4,2 cm, nur Rueckenlinie/Nacken, Bauchfranse, Hinterkante Vorderbein,
Hinterteil; `netz/lowpoly_zott.blend`, Bild `netz/bild_zotteln.png`). Ergebnis nach dem Verringern: Reihen kleiner Pyramiden ("Noppen")
statt Fell, Rumpf-Knick ueber 20 Grad 21,3 % (ohne 6,9 %), ueber 35 Grad 7,1 %, Umklapper 13, Hubbel Mittel 2,0 mm. Damit bringen sie
Hubbel zurueck -> **nicht uebernommen** (Vorgabe 0). Die Engine kann keine brauchbaren Haarkarten (Forschung B: a^3-Saeume), also bleibt
das Fell Sache der Textur (Straehnen). Schalter bleibt im Skript, falls Kevin es sehen will.

## 5. Bilder (offline, Spiel-Licht nachgebaut, nicht gespielt)
- `bilder/netz_vergleich.png`: Bestand links / neu rechts - Hinterfuss nah im Sitzen (Ton und Zwischentextur), Sohlen von unten,
  Sitzen im Spielwinkel, Aufrichten (Spielwinkel, von unten, Pranken nah, vorn tief), Tot (Seite, hinten), Ruhe von hinten.
  Einzelbilder `render/netz_fell/`, Auftraege `render/netz_fell/auftrag*.json`.
- `netz/bild_form_vergleich.png`, `netz/bild_sohle_fell.png`, `netz/bild_zotteln.png` (CPU-Zeichner `netz/zeichne.py`, keine GPU).
- Ehrlich: in den Ton-Bildern sind die 8-mm-Ballen und die Gesaessfalte **nur schwach** zu sehen; die Sohle wirkt im Sitzen weiter wie
  ein rundes Ende, nur leicht gewellt. Den sichtbaren Unterschied muss die Sohlen-Textur bringen (Plan liegt bereit).

## 6. Neu bauen (alles ohne GPU)
```
cd _arbeit/baer_fell/netz
BAER_FELL_NAME=fell bash lauf_netz.sh netz fbx kopfprobe          # ~4 min: Blend, mod/.../WorldItems/NCBear.fbx, Kopfprobe
NCB_FELL_NUR_GEWICHTE=$PWD/gew_fell2_formel.npz blender -b --factory-startup --python baer/spiel/baer_kampf_fell.py -- $PWD/glb_tmp ""
python baer/spiel/baer_gewichte_fell.py gew_fell2_formel.npz gegend_fell2.npz gewichte_fell.npz   # ~11 min; gegend aus netz_fell.npz
python messen.py gewichte_fell.npz gegend_fell2.npz mess_fell_final.json; python tabelle.py
BAER_FELL_NAME=fell bash lauf_netz.sh backen                      # nur Zwischenstand mit alten Ansichten
bash lauf_glb.sh final $PWD/zwischen_fell/42/media                # GLB, Dump, Clip-Vergleich
```

**Nachbesserung 09.11.2026 (Pruefer Technik m5, `fix_bericht.md`):** Die Kette oben schreibt fest nach `netz/` und ueberschreibt die
Lieferung. Seit der Nachbesserung lassen sich die Ordner umlenken: `BAER_FELL_NETZ` (Netz-Ordner fuer `baer_export_fell.py` und
`baer_textur_fell.py`), `BAER_FELL_FBX` (Ziel/Quelle des FBX), `BAER_TX_DIR` (Ausgabe des Textur-Backens samt Kopf-Variante),
`BAER_TX_ANS` (Ordner mit den GPU-Ansichten, Vorgabe `textur/`), `NCB_FELL_GEWICHTE` (Gewichte fuer `baer_kampf_fell.py`),
`NCB_FELL_KOPF_ALT` (Kopf-/Krallen-Gewichte von baer-anim, Vorgabe `netz/gew_bestand.npz`). Es fehlten drei Schritte:
`lowpoly_npz.py` (Blend -> `lp_fell.npz`) und `karten.py` (`lp_fell.npz` + Gewichte -> `karten/karten_2048.npz`, liest das Backen),
dazu der Rueckfall `NCBearDeer.glb` (`baer_tier_anim.py -- ZIEL QUELLE "" _arbeit/baer_spiel/tier_arbeit/deer_walk.txt`).
Die ganze Kette ohne GPU steht als ein Skript in `_arbeit/baer_fell/fix/lauf_fix.sh`
(`netz fbx kopfprobe formel gewichte glb zwischen karten backen body deer`, alles nach `fix/`).

## 7. Dateien
- Skripte: `baer/spiel/baer_export_fell.py`, `baer_kampf_fell.py`, `baer_gewichte_fell.py`
- Ergebnis: `_arbeit/baer_fell/mod/42/media/models_X/WorldItems/NCBear.fbx` (MD5 `d90796cd...`, traegt Zeitstempel),
  `models_X/Skinned/NCBear.glb` (`c8250ace...`, mit Zwischentextur-UV), `models_X/Skinned/NCBearDeer.glb` (`c5cc07bb...`, Rueckfall neu,
  40 Knochen, ohne Clips, geladen mit Dump.java)
- Netz/Uebergabe: `netz/lowpoly_fell.blend`, `netz_fell.npz`, `gewichte_fell.npz`, `sohle_layout.json`, `karten/` (Regionen + Sohlen-Koordinaten
  2048), `uebergabe.md`; Zwischenstand `netz/zwischen_fell/`, `netz/glb_final/` (samt `Body/NCBear.png` 1024 der Zwischentextur)
- Messung: `netz/mess_bestand.json`, `mess_fell2_formel.json`, `mess_fell_final.json(.npz)`, `mess_final/` (regionen.py am End-Dump),
  `dump_final.txt`, `log/`
- Werkzeuge: `netz/messen.py`, `opt_gewichte.py` (Versuchsstand), `regionen_rt.py`, `karten.py`, `lowpoly_npz.py`, `falten_fell.py`,
  `pruef_netz.py`, `glb_pruef.py`, `lauf_netz.sh`, `lauf_glb.sh`, `zeichne.py`, `bild_*.py`, `blatt_vergleich.py`, `tabelle.py`

## 8. Offen / unsicher
1. **Nicht gespielt.** Ob die Gewichte im Spiel ruhiger wirken, sieht nur Kevin; die Messung ist die Haut wie der Importer sie liest.
2. Die Gewichte sind gegen genau diese 15 Clips optimiert. Neue oder geaenderte Clips -> `baer_gewichte_fell.py` neu laufen lassen.
3. Ballen-Relief 8 mm ist klein; mehr (bis 10 mm laut Forschung) oder Ballen weiter vorstehend waere ein neuer Netz- und Gewichtslauf.
4. Achsel/Ellbogen-Falten liegend 154 statt Ziel 120; "Ei" im Aufrichten mit meinem Mass 0,941 (Ziel 0,95 nach anderem Mass).
5. Normalen der Unterseite kippen (Forschung B) nicht gemacht; GLB/Body-Textur der Zwischenstand haben die alte dunkle Unterseite.
6. Kevins Punkte 3/4 (Augen, Gesicht) und 7/9 nicht Teil des Netzes; Kopf unveraendert.
