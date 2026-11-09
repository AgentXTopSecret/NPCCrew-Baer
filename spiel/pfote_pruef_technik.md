# Lauf baer-pfoten: Pruefer Technik

Stand 09.11.2026 ~21:30, PZ 42.21, Blender 5.2.3 (nur Hintergrund, kein Render), JDK 25. **Statisch/offline geprueft, nicht gespielt.**
Keine GPU benutzt: alle Bilder dieses Berichts sind mit einem eigenen numpy-Rasterer auf der CPU aus den Importer-Dumps gezeichnet
(`pruef/technik/raster.py`), nicht mit Cycles. Nichts in die Test-Mod, nach NPC Crew, nach `baer_fell` oder in Dateien der Bauer
geschrieben, nichts committet. Eigene Dateien nur in `_arbeit/baer_pfote/pruef/technik/` (plus dieser Bericht).

Geprueft: `_arbeit/baer_pfote/mod/42/media/` (neu: GLB a6099029, Deer 9246fa53, FBX ab35c415, Body 4ae60e6c, WorldItems 94212c2e)
gegen `Zomboid/mods/NCBearTest/42/media/` (alt = baer-fell: GLB 2a4837f6, Deer f34cb9dc, Body c2d6c8cc, WorldItems 033d3705; nur gelesen).

Hinweis zu Kevins Satz "loesch die regel die hab ich nie gemacht!" (vom Workflow mitgeschickt): Ich habe keine Regel geaendert oder
geloescht. Fuer diese Pruefung spielte die GPU-Regel keine Rolle, weil ich gar nicht auf der GPU gerendert habe. Welche Regel Kevin meint
(die Projekt-CLAUDE.md sagt in Abschnitt 5 "Nicht bauen oder rendern, waehrend Kevin mit der betroffenen Mod spielt"; der Auftrag nennt
eine geaenderte GPU-Regel mit Kevins Namen), ist aus dem Satz allein nicht eindeutig; das Loeschen ist Sache der Hauptsitzung mit Kevin.

## 0. Ergebnis kurz

- **Saeule oder Pfote?** In meinen eigenen Ton-Bildern (CPU, gleiche Clips, alt | neu) ist **jede der vier Pfoten in jeder Pose eine
  Pfote**: Bein verjuengt, Fuss ragt heraus, fuenf Zehen mit Krallen, hinten Ferse und lange Sohle; die alte Saeule mit runder Kappe ist in
  keiner Zelle mehr da (Tabelle Abschnitt 1). Mit Textur (Bilder der Bauer, angesehen) ebenso. Schwaechen: Pranke von unten ein Kasten,
  Hintersohle eine flache Platte mit scharfem Rand, Hinterfuss im Rennen-Schwung schmal und spitz.
- **Feste Regeln, die halten (eigener Beleg):** 15/15 Clips samt Skelett textgleich im Importer (46.433 Zeilen) und byte-gleich in der
  Datei, Knochen/Namen/Eltern/Offset/Bind gleich, 19.388 Dreiecke, <= 4 Einfluesse, Summe 1, 1 Netz/1 Primitiv/0 Material, keine offenen
  Kanten, keine neuen Umklapper, Kopf (1.331/1.333 Punkte bit-gleich, 2 um 5e-5 mm; gehaeutet 0,000 mm Abweichung in allen Bildern),
  Krallen hinten 228/228 bit-gleich, vorn Form/UV/Gewichte bit-gleich und nur starr in y verschoben (K1), Dehnung 99,5 % <= 2,49 / max
  3,22 / Achsel-Brust 3,08, Knoechel/Handgelenk <= 2,70, Texturen (Typ, Groesse, Kopf-Texel, Krallen-Abtastung, Maul-Flecken), Deer,
  nur 5 Dateien, keine Test-/Cheat-Dateien, Originalskripte unveraendert. **Nachbau ohne GPU (nur in meinen Ordner): GLB, Deer, Body
  und WorldItems byte-gleich**, FBX bis auf den Zeitstempel (Abschnitt 6).
- **1 x blocker:** Falten im Liegen deutlich schlechter als baer-fell (SPEZ-Grenze 120, gemessen 186; baer-fell 88) - die feste Regel
  "Falten duerfen nicht verloren gehen" ist damit verletzt, die Bauer haben es nicht gemessen (B1).
- **3 x major:** Sitz-Ferse schwebt 0,8 cm und ist **ohne** Clip-Aenderung behebbar (Probe), anders als berichtet (M1); Rumpf weicht an
  42 Punkten mehr als 1,5 cm von baer-fell ab, auch an der Gesaessfalte (M2); Pranke von unten ein Kasten (M3).
- **minor:** Abschnitt 8.

## 1. Saeule oder Pfote (je Pfote und Pose, eigene Ton-Bilder, angesehen)

Eigener Rasterer (CPU, z-Puffer, Lambert, grauer Boden z = 0), Netz = Importer-Dump, gehaeutet mit den unveraenderten Clips; je Ansicht
eine Zeile alt und eine Zeile neu, Spalten VL/VR/HL/HR, Ausschnitt um die Pfote (Radius 34 cm, darum oben ein gezackter Schnittrand - das ist der Bildausschnitt, nicht das Netz).
Alle Pfade unter `_arbeit/baer_pfote/pruef/technik/bilder/`.

| Pose (Clip, Bild) | VL | VR | HL | HR | Bild | Bemerkung (neu) |
|---|---|---|---|---|---|---|
| Stehen (Idle01, 0) | Pfote | Pfote | Pfote | Pfote | `ton_stehen.png`, Sohlen `ton_sohle.png` | alt: dicke Saeule, Zehen kaum vor dem Bein. Neu: Bein in 20 cm Hoehe halb so tief (34-36 -> 18-20 cm), Fuss/Pranke ragt vor, Ferse hinten |
| Gehen Stand (Walk, 5) | Pfote | Pfote | Pfote | Pfote | `ton_gehen_stand.png` | Fuss flach am Boden, Zehen vorn |
| Gehen Schwung (Walk, 20) | Pfote | Pfote | Pfote | Pfote | `ton_gehen_schwung.png` | Hinterfuss mit gehobener Ferse, Zehen unten |
| Rennen (Run, 9) | Pfote | Pfote | Pfote | Pfote | `ton_rennen.png` | HL/HR im Schwung nach hinten: schmal, spitz zulaufend (Zehen an der Spitze) - liest sich als Fuss, wirkt aber duenn |
| Sitzen (Sit, 60) | Pfote | Pfote | Pfote | Pfote | `ton_sitzen.png`, `ton_sitzen_nah.png` | alt HL/HR: runde Saeule mit flacher Kappe, Zehenklumpen oben (Kevins Beschwerde, im CPU-Bild nachgestellt). Neu: lange Sohle, fuenf Zehen oben; Ferse schwebt 0,8 cm (M1) |
| Aufrichten (Rear, 45) | Pfote | Pfote | Pfote | Pfote | `ton_aufrichten.png` | Hinterfuesse stehen mit Ferse und Zehen ganz auf; Pranken von unten kastig (M3) |
| Liegen (Dead, 1) | Pfote | Pfote | Pfote | Pfote | `ton_liegen_ganz.png`, `ton_liegen.png` | Hintersohle von unten eine flache Platte mit Zehenreihe |

Mit Textur (Renders der Bauer, nur angesehen): `_arbeit/baer_pfote/bilder/textur_2_sitzen_aufrichten.png`, `textur_10_abgesaegt.png` -
in allen gezeigten Zellen Pfote, die Textur verdeckt keine Saeule; Sohle hell wie auf Kevins Foto, Hintersohle eine gleichmaessige Platte.
Eigene einfache Formmasse in Ruhe (`form_out.txt`): Fusslaenge z 0-3 / Beintiefe z 20 alt 0,92-0,98 -> neu 1,47-1,81; Bein z 15 jetzt
0,6-1,6 cm schmaler als der Fuss (alt 9-10 cm breiter); Ferse hinter der Kehle hinten 2,4 cm (alt 1,0-1,7).

## 2. Feste Regeln (eigene Werkzeuge, Belege in `pruef/technik/`)

| Regel | Beleg | Ergebnis |
|---|---|---|
| Importer liest beide GLB | `Dump.java` (Harness `_arbeit/baer_spiel/harness`), `dump/alt.txt`, `dump/neu.txt`, `dump/deer_*.txt`; meine Dumps sind MD5-gleich zu `bestand/dump_heute.txt` und `dump_final.txt` der Bauer | ja |
| 15 Clips bit-gleich, Knochen/Namen/Eltern, Offset, Bind | Dump-Teil vor `ELEMENTS` (Knochen, Eltern, OFFSET, BIND, alle 15 Clips mit Zeiten, lokalen Schluesseln, Modellmatrizen) alt == neu **textgleich**, 46.433 Zeilen, MD5 8b33202e (`dump/alt_skelett_clips.txt`); Datei: `glb_json_out.txt` "Animationen in der Datei byte-gleich ... abweichende Puffer 0", Knoten-TRS und inverseBind byte-gleich | ja |
| <= 20.000 Dreiecke | Dump 19.388 (alt 18.930), Datei 19.388 | ja |
| <= 4 Einfluesse, Summe 1 | Dump: Summe 0,9999999..1,0000002, max 4, 0 negative; Datei WEIGHTS_0 1,000000; Knochen mit Gewicht 19 = alt (`netz_pruef_out.txt` 1) | ja |
| 1 Netz / 1 Material | 1 Netz, 1 Primitiv, 0 Material, keine Bilder (`glb_json_out.txt`) | ja |
| Topologie | geschweisst: 0 offene Kanten; 41 Kanten mit > 2 Flaechen und 82 doppelte gerichtete Kanten, **alle** im festen Kopf/Maul/Krallen und genau wie alt; Umklapper in Ruhe ausserhalb Kopf/Maul/Krallen 0 (alt 1); keine entarteten Dreiecke (`netz_pruef_out.txt` 2) | ja |
| Kopf bleibt so | ueber die **alten** Etiketten (`baer_fell/fix/netz/lp_fell.npz`): 1.333 Kopfpunkte, 1.331 Lage+UV+Gewichte bit-gleich, 2 um 5,5e-5 mm verschoben (Float-Rauschen, Gewichte gleich), 1.314 auch Normale (17 am Nahtrand); gehaeutet ueber alle 15 Clips/alle Bilder Abweichung **0,000 mm** (1.559 Paare inkl. Krallen hinten); Maul 312/316 alle 16 Werte gleich, die 4 uebrigen sind Naht-Doppelpunkte am Hals/an der Pranke, nicht im Maul (`maul_krallen_out.txt`) | ja |
| Krallen | hinten 228/228 alle 16 Werte bit-gleich; vorn 227/227 UV und Gewichte bit-gleich, je Kralle starr nur in y verschoben (-10/-5/0/+5/+10 mm, Abweichung vom starren Versatz 0,0000 mm, x/z 0,00 mm), Normalen <= 0,01 Grad (`detail_out.txt` (b)); nur an Hand/Foot gewichtet | ja (Lage an die Zehen erlaubt) |
| Liegehoehe Death/Dead | Clips gleich; Rumpf (Ruhe-z > 0,36) tiefster Punkt Dead alt 1,77 / neu 1,90 cm, Netz gesamt 0,01 -> 0,40 cm (Kralle) (`detail_out.txt` (d)) | ja (Hinweis m2) |
| kein Clip tiefer im Boden | je Clip gesamt, je Pfote (Haut) und Krallen, alle Bilder (`netz_pruef_out.txt` 5): gesamt 0 Verstoesse ausser Maul -0,029 -> -0,034 cm; je Pfote nur Walk HR -1,414 -> -1,452 cm. Beides innerhalb der SPEZ-Toleranz 0,05 cm | ja mit Toleranz (m1) |
| Pfoten in Walk/Run/Rear: nicht im Boden, nicht schwebend | je Bild Ferse/Zehen (`detail_out.txt` (f)): Walk HL Bilder 0-10 Ferse 0 / Zehen 0 cm, HR Bilder 14-24 0/0, Run HL Bilder 0-2/16 0/0, VL Run 7-10 Zehen 0, Ferse 1 cm (angehobener Handwurzelballen). Tiefste Pfotenhaut je Clip (`netz_pruef_out.txt` 5): Walk VL -0,68 -> -0,06, VR -0,58 -> -0,12, HL -1,72 -> -1,72 (Fersenaufsatz Bild 26, alt gleich), HR -1,41 -> -1,45; Run VL -0,77 -> -0,14, HL -1,53 -> -0,75, HR -1,26 -> -0,75 cm; Krallen bis -2,40 (Walk) / -2,98 (Run) wie alt; Rear: Hinterfuesse ganz auf (Ferse 0, Zehen 0,4 cm). Nicht schwebend, nicht tiefer als alt (bis auf m1) | ja |
| Dehnung je Clip (Regeln der Forschung) | Kopie von `baer_fell/werkzeug/regionen.py` an meinen Dumps (`reg_alt/`, `reg_neu/`, `region_tabelle_out.txt`): 99,5 % max **2,49** (SwipeL; Soll 2,6), Hoechstwert **3,22** (SwipeR; 4,0), Achsel/Brust **3,08** (3,5) | ja (Hinweis m5) |
| Dehnung Knoechel/Handgelenk | eigene SVD (`dehnung_eigen.py`, `knoechel_out.txt`): Band Ruhe-z 5-22 cm, gefiltert wie die Forschung: max 2,70 (SwipeR), alt 2,66; Region Pfote/Gelenk (SPEZ) 99,5 % 2,54, max 3,08 | ja (Hinweis m4: Splitter) |
| Fremde Knochen an den Pfoten | keine Gewichte anderer Beine; Wirbelsaeule/Becken an Pfotenpunkten 11-14 cm hoch max 0,056 (alt 0,11), **neu: Bip01_Tail an 8 Punkten der HR-Pfote** (z 11-14 cm, max 0,011) (`detail_out.txt` (c)) | im Kern ja (m3) |
| Texturen | `textur_out.txt`: Body 1024x1024, WorldItems 2048x2048, beide RGB 8 Bit, gleiche PNG-Bloecke wie alt; Kopf-Texel (Inseln + 1 px) 0 verschieden in 2048 und 1024, Kopf-Inseln-Masken alt == neu; Krallen: alle 455 Krallen-Ecken bilinear abgetastet in beiden Texturen bit-gleich; Maul-Flecken (+4 px) bit-gleich, keine Rumpf/Kopf-UV darin; Body 1024 = 2x2-Mittel der 2048 an 98,4 % der Texel (Rest = Kopf/Flecken aus dem alten Stand) | ja |
| UV | Ueberlappung 17 Texel in 9 Dreieckspaaren, **alle in der festen Schnauze und genau wie alt** (`uv_ueber_out.txt`); keine an den Pfoten | ja |
| NCBearDeer.glb | laedt (40 Knochen, 0 Clips), Skelett-Teil des Dumps textgleich zum alten Deer, Knoten/inverseBind byte-gleich; 18.974 Dreiecke, Summe 1, <= 4; jede Ecke liegt auf einer Ecke von `lp_pfote` (Lage <= 0,0001 mm, UV <= 6e-8) - passt zum neuen Netz und zur neuen Textur (`deer_out.txt`) | ja |
| Dateien/Pfade | `mod/42/media`: genau `models_X/Skinned/NCBear.glb`, `NCBearDeer.glb`, `models_X/WorldItems/NCBear.fbx`, `textures/Body/NCBear.png`, `textures/WorldItems/NCBear.png`; keine Lua, kein Skript, kein Test-/Cheat-Inhalt; FBX ohne Nutzerpfad (nur "NCBear.blend") | ja |
| Originalskripte | `git diff` im Repo `baer/`: keine Aenderung an verfolgten Dateien unter `spiel/`; MD5 der `*_anim.py`, `*_fell.py`, `baer_tier_anim.py` = `log/md5_originale.txt` / `textur/log/md5_originale_vorher.txt`; die fuenf `*_pfote.py` sind neu (ungetrackt), CRLF wie die Originale, alle parsen | ja |
| Test-Mod/NPC Crew | NCBearTest-GLB weiter 2a4837f6 (09.11. 14:19), Texturen c2d6c8cc/033d3705 | unberuehrt |

## 3. Was baer-fell erreicht hat (Rumpf, Ei, Falten)

- **Ei** (Kopie `werkzeug/ei.py` an meinen Dumps, `ei_out.txt`): Rear 1,3 s Verhaeltnis 1,033 -> 1,032 (Soll >= 0,95). Gehalten.
- **Rumpf** (eigener Punkt-Dreieck-Abstand, `rumpf.py`, `rumpf_out.txt`): ueber Ruhe-z 0,36 neu -> alte Flaeche p50 0,00 / p95 0,35 /
  max **2,71 cm**, 42 Punkte > 1,5 cm; umgekehrt max 2,65 cm. Ueber z 0,45 p95 0,06, max 2,19 cm. SPEZ 3.1: p95 <= 0,5 erfuellt, max <= 1,5
  **nicht** (M2).
- **Falten** (Kopie `werkzeug/falten_fell.py` an meinen Dumps, `falten_alt.txt`, `falten_neu.txt`, `falten_detail_out.txt`): B1.
- Unterseite/Straehnen: nicht selbst gemessen (Optik-/Textur-Blick); die Rumpf-Texel ausserhalb der Pfoten habe ich nicht verglichen.

## 4. Gewichte an Pfote und Gelenk (eigene Zaehlung, `netz_pruef_out.txt` 4)
Hand bzw. Fuss+Zeh unter 6 cm: >= 0,95 bei 97,5-98,9 % der Punkte, min 0,86-0,91 (alt 99,2-99,4 %, min 0,90-0,94); z 6-10 cm min
0,56-0,62 (alt 0,59-0,62). SPEZ-Ziele "Fussgewicht >= 0,95 unter 6 cm" und "Wade/Unterarm >= 0,95 ab z 0,20" damit nicht ganz erreicht -
wie von den Bauern selbst gemeldet, und alt auch nicht (m6).

## 5. Gegenbefunde zu den Berichten der Bauer
1. "Sitzen: der Hinterfuss schwebt 0,8 cm, das geht nur mit einer Clip-Aenderung (C2)" - **stimmt so nicht** (M1).
2. "Rumpf-Hoechstwert 2,1 cm an 4 Punkten an der Hinter-Kniekehle" - bei mir 2,71 cm, 42 Punkte > 1,5 cm, auch an der Gesaessfalte (M2).
3. "Falten liegend: nicht eigens gemessen (Pruefer)" - gemessen: verfehlt (B1).
4. "0 Verstoesse Boden" gilt nur mit der Toleranz 0,05 cm der SPEZ; ohne Toleranz 2 Clips minimal tiefer (m1).
5. Alles andere (Clips, Kopf, Krallen, Dreiecke, Dehnung, Texturregeln, Deer, Dateien) habe ich mit eigenen Werkzeugen bestaetigt.

## 6. Nachbau ohne GPU (`pruef/technik/repro/lauf.sh`, 21:03-21:23, ~19 min CPU)

Befehle wie dokumentiert (`netz/uebergabe.md` 5: `lauf_pfote.sh netz fbx kopfprobe formel gewichte glb` + `zwischen karten deer`, mit
`ANS_ALT=_arbeit/baer_spiel/ansichten/`; `bau_textur.md` 8: `lauf_textur.sh pfote backen glb`), aber **alle Ausgaben nach `repro/`**
ueber die Umgebungsvariablen der Skripte (`BAER_PFOTE_NETZ`, `BAER_FELL_FBX`, `BAER_FELL_MOD`, `BAER_TX_DIR`, `BAER_FELL_NETZ`, Ziel-
Argumente) - kein Skript geaendert, keine Datei der Bauer beschrieben (Zeitstempel danach unveraendert). Eingaenge nur gelesen: die
GPU-Ansichten (`ansichten/`, `textur/ansichten*`), `textur/zw_fell_2048.png` (Bezug aus einem frueheren Bake), `spez/pfoten_plan.json`.

| Stufe | Ergebnis gegen die Lieferung |
|---|---|
| netz | `netz_pfote.npz` cd54a690 und `sohle_layout.json` b4983fa9 **byte-gleich** |
| fbx | MD5 anders (3b2dda1c statt ab35c415, 16 Byte laenger): Zeitstempel/Kopfdaten; Geometrie gleich (alles daraus Gebaute byte-gleich); kein Nutzerpfad mehr in der Datei |
| kopfprobe | gleiche Ausgabe (Kopf 3.127 Flaechen wiedergefunden, Krallen hinten 228 bit-gleich, vorn alt + K1, KOPFPROBE_OK) |
| formel / gewichte (13 min) | `gew_pfote_formel.npz` f30c3a84, `gewichte_pfote.npz` 69e2325a **byte-gleich** |
| glb | **NCBear.glb a6099029 byte-gleich** |
| karten | `lp_pfote.npz` b9ced180, `karten_2048.npz` 2dd4c8fb byte-gleich |
| deer (Original `baer_tier_anim.py`) | **NCBearDeer.glb 9246fa53 byte-gleich** |
| Textur backen (84 s) + glb | **WorldItems 2048 94212c2e** und **Body 1024 4ae60e6c byte-gleich**, GLB wieder a6099029 |

Damit sind alle fuenf Mod-Dateien aus den Skripten reproduzierbar (FBX bis auf Zeitstempel). Nicht nachgebaut: die GPU-Stufen
(Ansichten) und `zw_fell_2048.png` (entsteht mit `fell_uebertrag.py` aus einem frueheren Bake - in `bau_textur.md` 8 dokumentiert, aber
ein Henne-Ei-Eingang; minor m10).

## 7. Wie geprueft (Werkzeuge in `pruef/technik/`, alle eigen oder Kopien der Forschungs-Werkzeuge, an meinen Dumps)
| Werkzeug | Was | Ausgabe |
|---|---|---|
| `Dump.java` (Harness, unveraendert) | Importer des Spiels: alt, neu, Deer alt/neu | `dump/*.txt` (+ `.pkl` ueber `lade.py`) |
| `glb_json.py` (Kopie Pruefer baer-fell) | Datei direkt: JSON, Puffer, Animationen byteweise | `glb_json_out.txt` |
| `netz_pruef.py` | Netz, Topologie, Kopf/Krallen ueber alte Etiketten, Pfoten-Gewichte, Boden je Clip/Pfote, Liegen (Abschnitt "6 Fussaufsatz" dort ist unbrauchbar: die Standphase nach Gelenkhoehe trifft beim Hinterfuss die Schwungphase; massgeblich ist die Liste je Bild in `detail_out.txt` (f)) | `netz_pruef_out.txt` |
| `detail.py` | Maul, Krallen vorn je Kralle, fremde Knochen, Liegen nach Teilen, Sitz-Ferse, Ferse/Zehen je Bild Walk/Run | `detail_out.txt` |
| `ferse.py`, `ferse_probe.py` | Sitz-Ferse: Hinterkante je Hoehe alt/neu; Probe "Ferse 0,6/0,7/0,9 cm zurueck" in allen Clips | `ferse_probe_out.txt` |
| `regionen_kopie.py`, `region_tabelle.py` | Regionen + Dehnung nach den Regeln der Forschung | `reg_*/`, `region_tabelle_out.txt` |
| `dehnung_eigen.py`, `splitter.py` | eigene SVD, mit/ohne Kantenfilter, Region Pfote/Gelenk, Knoechel; staerkste Dreiecke | `dehnung_eigen_out.txt`, `knoechel_out.txt`, `splitter_out.txt` |
| `falten_detail.py`, `falten_bild.py` (+ Kopie `werkzeug/falten_fell.py`, `ei.py`) | Falten im Liegen je Zone, Anteile, Lage | `falten_*.txt`, `falten_detail_out.txt`, `bilder/falten_liegen.png` |
| `rumpf.py` | Rumpf neu gegen baer-fell, Punkt-Dreieck-Abstand | `rumpf_out.txt` |
| `textur_pruef_pfote.py`, `uv_ueber.py` | PNG, Kopf-Texel, Krallen-Abtastung, Flecken, 1024/2048, UV-Ueberlappung | `textur_out.txt`, `uv_ueber_out.txt` |
| `krallen_wurzel2.py` | Anteil Krallenpunkte innerhalb der Haut (Strahl-Paritaet) | Konsole, Zahlen in m7 |
| `raster.py` | eigene Ton-Bilder (CPU) | `bilder/ton_*.png` |
| `repro/lauf.sh` | Nachbau ohne GPU, nur in `repro/` | `repro/lauf_out.txt`, `repro/*/log/` |

## 8. Befunde

### Blocker
**B1 Falten im Liegen: baer-fell-Erfolg verloren, SPEZ-Grenze gerissen.** `falten_alt.txt` / `falten_neu.txt` (`werkzeug/falten_fell.py` an
meinen Dumps, DeerStag_Dead): sigma2 < 0,5 Achsel + Ellbogen **alt 58 + 30 = 88 -> neu 111 + 75 = 186**; SPEZ 3.1 (hart): <= 120
(baer-fell 88); Knie 14 -> 114; sigma2 < 0,3: 121 -> 154 (Grenze 200 gehalten). Die Zaehlung haengt an den Zonen (Kugel 16 cm um das
Gelenk), die beim duenneren Bein mehr Oberflaeche enthalten (Ellbogen 190 -> 342, Knie 17 -> 225 Dreiecke); **auch anteilig** ist es
schlechter: Ellbogen 15,8 -> 21,9 % der Dreiecke (gestauchte Flaeche 0,0165 -> 0,0267 m2), Achsel 8,4 -> 12,6 % (0,0284 -> 0,0362 m2)
(`falten_detail_out.txt`). Die gestauchten Dreiecke sitzen jetzt gehaeuft im Band Ruhe-z 0,20-0,36 (Uebergang duennes Bein / dicker
Rumpf: 484 statt 274). Feste Regel "Falten duerfen nicht verloren gehen" verletzt; im Bericht der Bauer "nicht eigens gemessen".
Bild: `pruef/technik/bilder/falten_liegen.png` (rot = gestaucht; Falten am neuen Knie/Unterschenkel sichtbar). Fix: in
`baer_gewichte_pfote.py` die Falten-Zone (heute Achsel/Ellbogen, `OPT Falten-Zone: Dreiecke 907`) um das Uebergangsband Knie/Ellbogen
z 0,20-0,40 erweitern bzw. die Strafe dort erhoehen, Gewichte/GLB neu, dann `falten_fell.py` + `region_tabelle.py` erneut. Ob es im Spiel
auffaellt, ist ungeprueft (nur liegend).

### Major
**M1 Sitz-Ferse schwebt 0,8 cm - und das ist ohne Clip-Aenderung behebbar.** `netz_pruef_out.txt` 5/6: NCBear_Sit tiefster Punkt HL
0,16 -> 0,74 cm, HR 0,10 -> 0,86 cm, ebenso Ende SitDown / Anfang StandUp. Der tiefste Sitz-Punkt ist die **Hinterkante der Ferse in
Ruhe-z 9-13 cm** (alt x -0,636 m, `detail_out.txt` (e)); diese Kante liegt neu **0,8 cm (z 9-12) bzw. 1,3 cm (z 12-15) weiter vorn**
als bei baer-fell (`ferse.py`). Probe (nur Rechnung an meinem Dump, Gewichte unveraendert): Hinterkante in z 7-16 cm um 0,6 cm nach hinten
-> Sit HL 0,15 / HR 0,27 cm (wie baer-fell), alle anderen Clips unveraendert, StandUp HR -0,03 cm (innerhalb der Toleranz 0,05)
(`ferse_probe_out.txt`). Die Aussage "nur mit Clip C2" (bau_netz.md 3.1/5.3, bau_textur.md 7) ist damit widerlegt; Sitzen ist die Pose
von Kevins Beschwerde. Fix: Grenzkurve/Soll der Ferse in `baer_quelle_pfote.py`/`pfoten_abstand` so, dass die Fersen-Hinterkante in Ruhe-z
7-16 cm bis zur baer-fell-Linie (x ~ -0,635) reicht; danach Boden-Pruefung aller Clips.

**M2 Rumpf weicht staerker von baer-fell ab als berichtet.** `rumpf_out.txt`: ueber Ruhe-z 0,36 max 2,71 cm, 42 Punkte > 1,5 cm (SPEZ:
max <= 1,5), u. a. an der **Gesaessfalte** (x -0,65, y -0,10, z 0,49-0,50) und aussen am rechten Knie (z 0,36-0,38); umgekehrt 16 alte
Punkte > 1,5 cm, einzelne bis z 1,0. Bericht der Bauer: "max 2,10 cm, 4 Punkte an der Innenseite der Hinter-Kniekehle". Das Profil hinten
weicht bei y -0,06 / z 0,50 um 1,7 cm ab. Die Gesaessfalte "von hinten wie baer-fell" (SPEZ 3.1) sollte der Optik-Pruefer im Ton
vergleichen. Fix: Rumpf-Schaelung oberhalb z 0,36 auf die alte Huelle klemmen (wie die Hinterkante z 0,24-0,50).

**M3 Pranke von unten ein Kasten.** `bilder/ton_sohle.png` (Zeile "unten neu", VL/VR) und `ton_aufrichten.png`: rechteckiger Handballen
mit fast rechten Ecken, von unten/vorn im Aufrichten ein Block mit Krallen; dazu Form-Ziele vorn verfehlt (Bericht der Bauer, Dump
MD5-gleich zu meinem: Handwurzelballen unten 1,4 statt 1,5-2,0 cm, Vorsprung 0,55 statt >= 0,8 cm, Rist vorn 6,1 statt 6,5-8,5 cm).
Liest sich noch als Pfote, aber genau der Blick, den Kevin bei einer erhobenen Pranke hat. Fix: Handballen als runde Querwulst
(Ellipse statt Vieleck) und Handwurzelballen hoeher/weiter vor.

### Minor
**m1 Boden ohne Toleranz minimal tiefer.** Walk HR-Haut -1,414 -> -1,452 cm (0,38 mm), Maul VL -0,029 -> -0,034 cm (0,05 mm);
Clip-Tiefstwert gesamt unveraendert (Krallen). Innerhalb der SPEZ-Toleranz 0,05 cm; der Bericht nennt die Toleranz nicht.

**m2 Liegend beruehrt nichts mehr den Boden.** Dead: tiefster Netzpunkt 0,40 cm (Kralle), Beine 0,77 cm, Rumpf 1,90 cm (alt: HR-Pfote
0,01 cm) - der liegende Baer schwebt ~4 mm. Clips/Liegepose unveraendert, Regel "Dead >= 0,01 cm" gehalten.

**m3 Schwanz- und Wirbelsaeulengewicht an den Pfoten.** HR: Bip01_Tail an 8 Punkten (z 11-14 cm, max 0,011) - neu; Spine/Spine1/Pelvis an
Pfotenpunkten 8-14 cm max 0,056 (alt bis 0,11, also weniger als vorher). `fremd.py` der Bauer zaehlt nur andere Beine. Wirkung klein.

**m4 Mehr Splitter an der Pfote, die die Dehnungsmessung auslaesst.** Der Kantenfilter der Forschung (Kanten > 7,35 mm, Hoehe > 2 mm)
laesst 565 von 7.521 Pfote/Gelenk-Dreiecken aus (alt 83 von 6.562). Ohne Filter: ein Splitter innen an der HL-Ferse (x -0,591, y 0,181,
z 0,095; Hoehe in Ruhe 0,56 mm) erreicht 13,4 (Run), 12,2 (StandUp), 9,2 (Walk), 3,2 schon im Idle (`splitter_out.txt`); baer-fell hatte
max 8,3. Sichtbar wohl nicht (winzig), aber ein Netz-Mangel an der Ferse.

**m5 Achsel staerker gedehnt als baer-fell** (innerhalb der Grenzen): Achsel max Run 2,18 -> 2,71, Rear 2,17 -> 2,65, SwipeL 2,76 -> 3,08,
Walk 2,07 -> 2,34 (`region_tabelle_out.txt`); Achsel-Region neu 444 statt 348 Punkte.

**m6 Pfoten-Gewichte unter den SPEZ-Zielen** (Abschnitt 4), bekannt und gemeldet; unter 6 cm etwas schlechter als alt (97,5 % statt
99,2 % >= 0,95, min 0,86 statt 0,90).

**m7 Krallenwurzeln weniger eingebettet.** Anteil Krallenpunkte innerhalb der Haut je Kralle alt 17-48 %, neu 0-30 %; ein Teilstueck der
VL-Kralle bei (0,52 / 0,17 / 0,05) liegt ganz ausserhalb (`krallen_wurzel2.py`). Deckt sich mit "Krallenwurzeln an der Oberflaeche".
In meinen Ton-Bildern sitzen die Krallen an; nah im Spiel ungeprueft.

**m8 Form-Ziele SPEZ 3.2 teils verfehlt** (Sohlenrand-Knick, Rillen, Ballen-Relief, Rist vorn) - von den Bauern gemeldet, nicht
unabhaengig nachgemessen (deren Werkzeug laeuft auf einem Dump, der MD5-gleich zu meinem ist).

**m9 Nur alle fuenf Dateien zusammen.** Neues UV: GLB, Deer, FBX, Body, WorldItems gehoeren zusammen (das alte Deer passt nicht zur neuen
Textur, das neue Deer passt nur zu `lp_pfote`).

**m10 Nachbau-Eingang `zw_fell_2048.png`.** Der Textur-Bake braucht den Bezug `textur/zw_fell_2048.png`, den `fell_uebertrag.py` aus der
texel-npz eines frueheren Bakes macht (`bau_textur.md` 8). Mit der gelieferten Datei ist alles byte-gleich; von Null an braucht es einen
Vor-Bake. Die Datei gehoert deshalb zu den Lieferungen (nicht loeschen). Das FBX ist nur bis auf den Zeitstempel reproduzierbar (harmlos).

## 9. Nicht geprueft / offen
- **Nicht gespielt.** Mipmaps/Texturgroessen-Option im Spiel, Wirkung der Falten liegend im Spiel, Krallenansatz nah: ungeprueft.
- Keine GPU-Renders (bewusst); die Ansichten-Stufen (GPU) nicht nachgebaut, sie sind Eingang des Nachbaus.
- Unterseite, Straehnen, Farbe der Textur nicht selbst gemessen (Optik-/Textur-Blick).
- FBX-Geometrie nur indirekt (ueber das nachgebaute GLB) geprueft.
