# Lauf baer-fell: Bauer Textur (Unterseite, Sohlen, Hinterteil, Kopf-Variante)

Stand 09.11.2026 frueh, Blender 5.2.3, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
GPU nur RTX 4090 mit OptiX + OptiX-Entrauscher, jeder Render ueber `werkzeug/gpu_render.sh` (prueft `tasklist` auf ProjectZomboid,
Sperre `gpu.lock`); das Spiel lief bei keiner Pruefung, die Sperre ist frei. Nichts in die Test-Mod oder nach NPC Crew geschrieben,
nichts committet (macht der Integrator). Kopf und Krallen: Texel bit-gleich zur alten 2048er.

## 0. Kurz

1. **Eigentliche Ursache des dunklen Hinterteils und der dunklen Unterseite gefunden:** Fell sieht von der Haarspitzen-Seite her
   viel dunkler aus (man schaut zwischen die Buesche in das verschattete Unterfell). Probe 512 (`textur/probe/p1`): die Flanke
   in `k_h135` hat 0,27x, `k_h180` 0,21x der Helligkeit von `k_h045` - auch mit rein diffusem Haar (0,41x / 0,20x), also Geometrie
   des Fells, nicht die Haar-BSDF. Das Backen nimmt fuer nach hinten/unten zeigende Flaechen genau diese Ansichten -> "Klumpen".
2. **Neue Ansichten** (26 Koerper + 9 Back-Pose, 2048, ~7 min GPU) mit nur fuer den Bake geaendertem Fell (Beine weniger Melanin,
   Haar rauer: gleichmaessiger aus allen Richtungen), dazu im Backen ein **gemessener Ausgleich der Blickrichtung zum Haar**
   (Modell aus 3,8 Mio. Proben, log-Streuung 0,474 -> 0,413) und ein **Farbabgleich an das alte Fell** (Ruecken oben): die
   Grundfarbe bleibt Kevins Baer.
3. **Back-Pose** (Oberschenkel 28 Grad, Oberarme 22 Grad nach aussen gedreht; Spielnetz mit den Hautgewichten des Hochmodells gleich
   posiert): Innenbeine/Achsel/Leiste/Bauch werden jetzt zu 96-100 % unter < 37 Grad gesehen (Innenbein hinten vorher 86 %).
4. **Sohlen** prozedural aus `netz/sohle_layout.json`: graue Lederhaut, 5 Zehenballen, Sohlenballen, Handwurzel- bzw. Fersenballen,
   schmale dunkle Furchen, Sohlenhaut dunkelgrau, Fellkranz am Rand. Ballen-Luma 95-96, Furchen 44 (Ziel 85-100 / <= 50).
5. **Im Spiel-Licht** (Nachbau Forschung A) ist die Unterseite jetzt 0,41-0,63 statt 0,18-0,36 der Rueckenhelligkeit, die Sohle
   0,48 statt 0,09; der helle Streifen innen an den Hinterbeinen ist weg (0,4 % statt 13,7 %).
6. **Kopf-Variante B** (Augen offener und dunkel mit Lidrand, Gesicht ~13 % dunkler) als eigene Datei, nicht eingebunden.
7. **Texturgroesse:** Body bleibt 1024 (Forschung B: keine Mipmaps, 2048 flimmert); 2048 nur als Vergleichsdatei.

## 1. Ursache (Probe, `textur/probe/`, Werte: mittlere lineare Helligkeit je Ansicht)

| Variante (512, 64 Samples) | k_h045 | k_h090 | k_h135 | k_h180 | k_bot | k_u150 | h135/h045 | h180/h045 |
|---|---|---|---|---|---|---|---|---|
| alt (wie baer-anim) | - | 0,0236 | 0,0105 | 0,0085 | 0,0212 | 0,0077 | - | - |
| a: Beine Melanin 0,13 -> 0,04, Haut Beine 0,62 -> 0,2 | 0,0412 | 0,0242 | 0,0110 | 0,0090 | 0,0224 | 0,0082 | 0,27 | 0,22 |
| c: wie a, Haar rein diffus | 0,0143 | 0,0113 | 0,0059 | 0,0029 | 0,0100 | 0,0038 | 0,41 | 0,20 |
| **b2 (gebaut):** a + Haar rau 0,6 / radial 1,0, Melanin +0,02, Zehenhaar -0,12 | 0,0537 | 0,0338 | 0,0218 | 0,0202 | 0,0285 | 0,0162 | 0,41 | 0,38 |

Schnitt-Ansichten (Kamera-Clip an der Mittelebene) probiert (`probe/p2`) und verworfen: der Schnitt liegt im dichten Fell zwischen den
Beinen, das Bild ist dort schwarz. Statt dessen die Back-Pose (`probe/p3`, Blatt `probe/p3.png`).

## 2. Was gebaut ist

`baer/spiel/baer_textur_fell.py` (neu; liest `baer_quelle_anim.py` und die Hilfsfunktionen von `baer_export_fell.py` nur ein,
aendert keine fremde Datei):
- **Stufe ansichten** (GPU, Auftrag als JSON): Hochmodell "spiel", Fell nur fuer den Bake geaendert (`fell_variante`: Knoten des
  Materials `haar` und `fell`, Zehenhaar eigene Kopie `haar_zeh`, damit Kopf/Hals unveraendert bleiben), Kameras wie
  `baer_export.py:91-107` + `u_s000..270` (64 Grad von unten); mit `"pose": true` die Back-Pose (`back_pose_setzen`) und
  `p_s*`, `p_u*`, `p_bot`. Ausgabe `textur/ansichten/` (26) und `textur/ansichten_pose/` (9). Die alten Kopfansichten `h_*`
  werden nur noch fuer Kopf-Texel gelesen (die ersetzt ohnehin die alte Textur).
- **Stufe backen:** Projektion wie `stufe_backen_anim` (gleiche Kameras, Tiefenpuffer, Toleranzen, Alpha), dazu
  1. Ausgleich Blickrichtung/Haar: Haarrichtung je Texel aus den Partikelwerten (`baer_quelle_anim.py:1692-1694`), Modell
     log(Helligkeit) = Texel + b(a, a^2, Blick z, cos, a*Bein, z*Bein), a = Blick . Haar; jede Probe auf a = 0,5 umgerechnet
     (Ruecken von oben), Begrenzung x0,33..x3; Gewicht cos^10 (vorher 7) x exp(-3 (a-0,55)) (Haar von der Seite bevorzugt).
  2. Farbabgleich je Kanal an das alte Fell (Ruecken/Flanke ueber 0,75 m, 472.046 Texel; Faktor linear 0,44/0,41/0,41).
  3. W5 Bauchluecke: an Innenbeinen waagerechte Ansichten nur mit Toleranz 0,010 und Gewicht 0,15.
  4. Back-Pose-Ansichten auf das gleich posierte Spielnetz (naechster Hautpunkt -> Knochengewichte, lineares Skinning; Punkte im
     Mittel 18,6 cm bewegt), nur fuer Unterseiten-Texel, Gewicht x2 (56,7 % des Gewichts dort).
  5. Nacharbeit: Unterseite x(1 + 0,45 unten), Unterbeine x(1 + 0,20 tief) (statt x1,30/x1,42 und "Pfoten dunkel" von baer-anim),
     Regionen ueber das Netz geglaettet (keine Kanten an Inselgrenzen); Haarbuesche (drei gedrehte Lagen, ~2-3 cm breit, ~7 cm lang,
     Spitze heller, +-15 %, an Unterseite/Hinterteil staerker); Faltenschatten aus der Verdeckung des Spielnetzes (bis -38 % in tiefen
     Falten, offene Flaeche 0); Gesprenkel gedaempft, wo nur Ansichten gegen die Haarspitzen sehen.
  6. Hals-Naht: Farbe bis 15 cm vom Kopf grob an das alte Fell, die letzten 2,5-5 cm weich ins alte Fell (Zwischenstand des
     Netz-Bauers = alte Ansichten auf neuem Netz). Farbsprung an der Naht 8,2 sRGB-Stufen (vorher 8,1).
  7. Sohlen (`sohlen_malen`), Kopf/Krallen alte Texel (6 px Rand), Maul-Flecken frei (geprueft), Kopf-Variante.
- **Gegenprobe:** `BAER_TX_NUR_NEU=1` (alte Ansichten, alte Nacharbeit) ergibt die Textur des Netz-Bauers (`netz/zwischen_fell`)
  bis auf +-1 sRGB in 0,004 % der Pixel (Summenreihenfolge) - die Projektion ist dieselbe.
- **Netz nicht angefasst:** `baer_kampf_fell.py` mit der neuen Textur baut ein **byte-gleiches GLB** (`c8250ace...` = `mod/.../NCBear.glb`
  des Netz-Bauers; das GLB enthaelt keine Bilder).

## 3. Messung alt / neu (gleiches neues Netz; `textur/werkzeug/mess_textur.py`, Definitionen wie `werkzeug/auswertung.py`; alles relativ zu Ruecken/Flanke)

| Region | Textur hell | **im Spiel hell** | Uneinigkeit absolut | Uneinigkeit rel. | Struktur | Winkel gut |
|---|---|---|---|---|---|---|
| Sohle vorn | 0,14 -> 0,70 | **0,09 -> 0,48** | 0,79 -> 0,34 | 1,31 -> 1,49 | 0,37 -> 0,67 | 100 % |
| Sohle hinten | 0,14 -> 0,71 | **0,09 -> 0,48** | 0,98 -> 0,34 | 1,62 -> 1,50 | 0,38 -> 0,57 | 100 % |
| Kehle | 1,04 -> 1,01 | 0,70 -> 0,69 | 0,29 -> 0,27 | 0,48 -> 1,18 | 0,98 -> 0,86 | 100 % |
| Achsel | 0,33 -> 0,79 | **0,23 -> 0,56** | 0,78 -> 0,40 | 1,29 -> 1,74 | 0,80 -> 0,94 | 100 % |
| Leiste | 0,53 -> 0,80 | **0,36 -> 0,56** | 0,64 -> 0,41 | 1,06 -> 1,78 | 0,81 -> 0,93 | 100 % |
| Innenbein vorn | 0,32 -> 0,62 | **0,22 -> 0,43** | 0,75 -> 0,37 | 1,23 -> 1,62 | 0,98 -> 0,97 | 100 % |
| Innenbein hinten | 0,23 -> 0,58 | **0,18 -> 0,41** | 0,94 -> 0,45 | 1,55 -> 1,98 | 1,03 -> 0,90 | 86 -> 96 % |
| Brust | 0,86 -> 0,81 | 0,58 -> 0,55 | 0,39 -> 0,29 | 0,64 -> 1,29 | 1,16 -> 1,01 | 100 % |
| Bauch | 0,29 -> 0,78 | **0,20 -> 0,53** | 0,71 -> 0,53 | 1,16 -> 2,32 | 0,96 -> 0,81 | 100 % |
| Hinterteil | 0,26 -> 0,73 | **0,23 -> 0,63** | 0,98 -> 0,35 | 1,61 -> 1,55 | 0,60 -> 0,85 | 100 % |
| Ruecken/Flanke (=1) | 1 | 1 | 0,61 -> 0,23 | 1 | 1 | 100 % |
| Kopf (fest) | 1,22 -> 1,22 | 0,87 -> 0,88 | Texel bit-gleich alt | | | |

Ruecken-Luma der Body-Textur 92 -> 92 (Farbe gehalten). "Winkel gut" alt = Forschung A (86 % Innenbein hinten, sonst 95-100 %).

| Ziel (Forschung A 6) | Ergebnis | erreicht |
|---|---|---|
| Im Spiel hell Achsel/Bauch/Innenbein/Leiste/Hinterteil >= 0,40 | 0,41-0,63 | ja (Innenbein hinten knapp: 0,41) |
| Brust/Kehle >= 0,55 | 0,55 / 0,69 | ja (Brust knapp) |
| Sohle >= 0,35, Ballen-Luma 85-100, Furchen <= 50, Kontrast >= 35 | 0,48; 95-96; 44; 51 | ja |
| Heller Streifen Innenbein hinten <= 3 % | 0,4 % (vorher 13,7 %; 95-%-Wert/Median der Luma 6,62 -> 1,61) | ja |
| Winkel gut >= 95 % je Region | 96-100 % | ja (durch die Back-Pose) |
| Uneinigkeit <= 1,1 (relativ zum eigenen Ruecken) | 1,18-2,32 | **nein**: absolut halbiert (Ruecken 0,61 -> 0,23, Unterseite 0,64-0,98 -> 0,27-0,53, alle unter dem alten Ruecken), aber der Ruecken wurde noch sauberer, das Verhaeltnis steigt |
| Struktur >= 0,9 Unterseite, Sohle >= 1,0 | Achsel 0,94, Leiste 0,93, Innenbein 0,97/0,90, Brust 1,01; Bauch 0,81, Hinterteil 0,85, Kehle 0,86; Sohle 0,57-0,67 | **teils**: Bauch/Hinterteil/Kehle darunter (Hinterteil vorher 0,60); Sohle ist absichtlich glattes Leder |
| Pruefbild 256/512/2048 | `bilder/textur_groessen.png` | ja |
| Kopf-Texel der Vorgabe = alt | 858.273 Kopf- und 251 Krallen-Texel bit-gleich zur alten 2048er | ja |

Faltenschatten wirken nur an wenigen Stellen (0,08 % der Texel ueber halber Staerke): in der Ruhehaltung gibt es kaum tiefe Falten;
Falten, die erst in Posen entstehen (Liegen, Sitzen), sind nicht eingebacken (die Textur gilt fuer alle Posen).

## 4. Sohlen

Je Sohlen-Texel (`karten_2048.npz` `sohle_xyz`, `sohle_pfote`) der Ellipsenabstand q zum naechsten Ballen wie `ballen_q`
(`baer_export_fell.py:870`): Kuppe heller (q < 0,95), schmale Randlinie bei q = 1, Furche dunkel (q 0,9-1,55), weiter weg
Sohlenhaut dunkelgrau, unregelmaessige Lederrisse 6-12 mm, Querfalten auf Sohlen-/Fersenballen, Fellkranz gezackt 0,3-2 cm am
Inselrand. Farbe leicht warmes Grau. Nach Kevins Foto nachgezeichnet, nichts daraus kopiert. Krallen unveraendert (alte Texel).
Bild: `bilder/textur_sitzen.png` (Hinterfuss nah, alle Sohlen von unten), `textur/bilder/sohle_uv_nah_v7.png`.

## 5. Kopf-Variante (nur Vergleich, Vorgabe bleibt die alte Kopf-Textur)

`textur/NCBear_kopf_variante.png` (2048, wie WorldItems) und `textur/NCBear_kopf_variante_body1024.png` (1024 mit Maul-Flecken, aus
`baer_kampf_fell.py`): nur Kopf-Texel geaendert (466.105 inkl. 6-px-Rand), Rumpf und Krallen gleich der Vorgabe. Lidspalte 1,1-1,25x
groesser und dunkel (sRGB ~14/9/6), Lidrand -55 %, Augenhoehle -22 %, Gesicht nach vorn -13 %. Bild `bilder/textur_kopf_variante.png`.
Zum Ausprobieren muesste nur `textures/Body/NCBear.png` gegen die Variante getauscht werden (Kevins Wort).

## 6. Texturgroesse

`textures/Body/NCBear.png` bleibt **1024** (Forschung B: kein Deckel fuer Tiere, aber keine Mipmaps -> 2048 flimmert bei Kevins
Zoom). `textures/WorldItems/NCBear.png` bleibt die 2048er Backquelle wie bisher. Zum Vergleich `textur/bilder/body_fell_2048.png`
(2048 mit doppelt grossen Maul-Flecken; nicht eingebunden). Pruefbild: Ballen und Haarbuesche sind bei 512 noch lesbar, bei 256
nur noch als hellere Flecken (`bilder/textur_groessen.png`).

## 7. Bilder (offline, Spiel-Licht wie Forschung A nachgebaut: Textur x min(1, 0,4 + 0,375 Lambert), nicht gespielt)

| Blatt | Inhalt |
|---|---|
| `bilder/textur_rear.png` | Kevins Aufrichten-Bild neben alt/neu: Spielwinkel, vorn tief, von unten, Vorderpranken nah, schraeg |
| `bilder/textur_sitzen.png` | Kevins Sitzen-Bild und Pfotenvorlage (nur angezeigt) neben alt/neu: Spielwinkel, Hinterfuss nah, alle Sohlen von unten, von vorn |
| `bilder/textur_liegen.png` | Tot links/hinten/Bauchseite, Ruhe von hinten/unten/Spielwinkel |
| `bilder/textur_groessen.png` | 256 / 512 / 1024 / 2048 |
| `bilder/textur_kopf_variante.png` | Kopf A (Vorgabe) / B (Variante) |
| `bilder/textur_uv.png` | Body-Textur alt / neu ueber der UV |

Einzelbilder `textur/render/{alt2,neu,neu_256,neu_512,neu_2048,kopfA,kopfB}/`, Auftraege `textur/render_*.json`.

## 8. Offen / unsicher

1. **Nicht gespielt.** Das Spiel-Licht ist ein Nachbau; Kevins echte Zoomstufe/Licht koennen anders wirken.
2. Uneinigkeit relativ zum eigenen Ruecken ueber 1,1 (absolut halbiert, s. 3); Struktur an Bauch/Hinterteil/Kehle 0,81-0,86.
3. Haarbuesche sind gemalt (3D-Muster entlang der Haarrichtung); wirken sie im Spiel zu regelmaessig: `BAER_TX_STRAEHNE` senken.
4. Die Back-Pose verformt das Hochmodell mit dessen eigenen Hautgewichten; an der Leiste kann Fell dabei gestaucht sein (in den
   Ansichten nicht auffaellig, `probe/p3.png`).
5. Normalen der Unterseite nicht gekippt (Vorschlag Forschung B, Sache des Netzes).
6. Kevins Wahl: Kopf A oder B; Alpha-Haarkarten nicht gebaut (Forschung B: schwarze Saeume).

## 9. Neu bauen (aus `_arbeit/baer_fell/textur/`)
```
bash ../werkzeug/gpu_render.sh C:/.../baer/spiel/baer_textur_fell.py C:/.../textur/ansichten_auftrag.json log/ansichten.log        # GPU ~5 min
bash ../werkzeug/gpu_render.sh C:/.../baer/spiel/baer_textur_fell.py C:/.../textur/ansichten_pose_auftrag.json log/ansichten_pose.log  # GPU ~2 min
BAER_TX_NAME=fell blender -b --factory-startup --python C:/.../baer/spiel/baer_textur_fell.py -- backen   # ~70 s CPU, deterministisch
bash werkzeug/lauf_glb_textur.sh fell C:/.../textur/NCBear_fell_2048.png    # Body 1024 + GLB (GLB = c8250ace)
python werkzeug/mess_textur.py "alt=...gegenprobe_2048.png|mess/texel_gegenprobe.npz" "neu=...fell_2048.png|mess/texel_fell.npz"
```

**Nachbesserung 09.11.2026 (`fix_bericht.md`):** `backen` schreibt nach `BAER_TX_DIR` (Vorgabe `textur/`), liest Netz/Karten aus
`BAER_FELL_NETZ` (Vorgabe `netz/`) und die Ansichten aus `BAER_TX_ANS` (Vorgabe `textur/`); die Ausgabe heisst `NCBear_<BAER_TX_NAME>_2048.png`,
die Kopf-Variante `NCBear_kopf_variante.png` landet im selben Ordner (vorher immer in `textur/`, Pruefer Technik m5). Neue Stellschrauben:
`BAER_TX_RUHIG` (Gesprenkel glaetten, 0,80), `BAER_TX_CAP_LEISTE` (0,95), `BAER_TX_CAP_UNTEN` (1,08), `BAER_TX_SAT_MAX` (0,56),
`BAER_TX_SOHLE_Q` (0,87); `BAER_TX_STRAEHNE` jetzt 0,30 (vorher 0,15). Ganze Kette: `_arbeit/baer_fell/fix/lauf_fix.sh`.

## 10. Dateien
- Skript: `baer/spiel/baer_textur_fell.py` (neu)
- Ergebnis (Arbeits-Mod): `_arbeit/baer_fell/mod/42/media/textures/Body/NCBear.png` (1024, MD5 `79a9aca4a87c429339201657aa9629b4`),
  `_arbeit/baer_fell/mod/42/media/textures/WorldItems/NCBear.png` (2048, MD5 `9395c7fe5efc9ac7da10c3f423a6a36c`); GLB/FBX dort vom Netz-Bauer
  (mit dieser Textur gebaut byte-gleich `c8250ace...`)
- Textur-Ordner `_arbeit/baer_fell/textur/`: `NCBear_fell_2048.png`, `NCBear_kopf_variante.png` (`7c466a70...`),
  `NCBear_kopf_variante_body1024.png` (`9b976171...`), `ansichten/`, `ansichten_pose/`, Auftraege, `mess/` (`regionen_vergleich.json`,
  `backen_fell.json`, `texel_*.npz`), `glb_fell/`, `glb_kopfB/`, `log/`, `probe/`, `render/`, Zwischenstaende `NCBear_v1..v7_2048.png`
- Werkzeuge `textur/werkzeug/`: `mess_textur.py`, `body1024.py`, `blatt.py`, `final_blaetter.py`, `exr_blatt.py`, `lauf_glb_textur.sh`,
  `patch_*.py` (Bau-Schritte am eigenen Skript)
- Blaetter `_arbeit/baer_fell/bilder/textur_*.png`

Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.
