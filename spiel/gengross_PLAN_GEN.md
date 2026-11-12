# PLAN_GEN -- Lauf baer-gen-gross: neuer grosser Baer E auf das 2c-Skelett (11.11.2026, Rolle PLAN)

**Nur Plan. Nichts am Modell gebaut, nichts gespielt, nichts in Test-Mods/NPC Crew/Spiel/`_arbeit/baer_zaehmen`/`_arbeit/baer_gross` geschrieben,
kein git, kein Download, keine GPU benutzt.** Gelesen: E_FEIN, GEGEN_OPTIK, STUFE2/PROBELAUF (ueberflogen), der ganze Rig-Lauf des Jungen
(`_arbeit/baer_gen/rig/RIG_PLAN.md`, `FORM.md`, `SKELETT.md`, `GEGEN.md`), SPEZ_2C (Abschnitte 0-3, 7, 8), `baer_maul_2c.py` (Schnitt),
`baer_gewichte_2c.py` (Kopf), `baer_export_junges.py` (Kopf), NCBearTest `NCBearDefs.lua`, `NCBearFight.lua` (Riegel, Sperre, Akt),
`NCBearBench.lua`, `NCBearBenchVergleich*.{lua,txt}`, `BanditsNPCBearCrew.lua`, `baer/tools/baer_uebernahme.py` (Einordnung),
ENTSCHEIDUNGEN.md (Ende), STAND.md (Kopf). Bilder selbst angesehen: Foto E, `spiel/gen_KEVIN_gross.png`, `spiel/2c_vorher_nachher.png`,
und alle eigenen Blaetter unter `plan/bilder/`.
**Selbst gemessen** (nur CPU, numpy + PIL, eigener Rasterer; Werkzeuge `plan/mess/`): 2c-Skelett und 2c-Netz aus einem EIGENEN Dump.java-Lauf
(`plan/dump/erw_2c.txt`, MD5 2875ca08 = gleich dem Dump in `_arbeit/baer_junges/eingang/`), E aus `E_schoen.glb`. Statisch geprueft, nicht gespielt.

Rahmen ueberall: **tier** = x vorn, y links, z oben, Boden z = 0, **Meter bei Groesse 1,0** (Modell 0,544 Einheiten je Meter). "roh" = Einheit
von `E_schoen.glb` (L ~ 0,96); glTF -> tier roh: x = glTF z, y = glTF x - y_mitte (-0,0131), z = glTF y + 0,34443. Blender-roh (form_info,
form2/textur2-Parameter): tier roh = (-by, bx, bz + 0,34443).

---------------------------------------------------------------------------------------------------------------------------------------

## 0. Kurz: Entscheidungen und Kernzahlen

| # | Entscheidung | Zahl |
|---|---|---|
| 1 | **Skelett und alle 15 Clips des 2c-Baeren byte-gleich**; das Netz von E wird an die 2c-RUHE angepasst (Lehre "Giraffe": keine eigenen Gang-Clips, keine eigenen Knochenlagen). Kein Becken-Hub moeglich -> **Bodenkontakt kommt nur aus der Form** (Pfoten, Sitzflaeche, Schnauze). | 26 Knochen, 15 Clips, Gewichte nur an den 21 Knochen, die auch 2c benutzt |
| 2 | **Massstab** s aus Rumpfhoehe/Bauch/Beinansatz/Buckel (alles passt zusammen) | **s = 1,70 m je roh** (Fit 1,66-1,74), Versatz **dx = +0,033 m** (Fit 0,02-0,06, Sitz-Kontakt) |
| 3 | **Rumpf quer verbreitern** (E ist bei s 1,70 schmaler als 2c; Beine muessen auf y +-0,225/+-0,25, Liegen/Sitzen brauchen die 2c-Breite) | q(x): Schulter **1,20**, Taille 1,03, Huefte **1,15** (Fit 1,05-1,25); Gesamtbreite <= 0,82 m |
| 4 | **Kopf starr in die 2c-Kopflage** (Kopf-Aussenform bleibt, nur gerade + umgesetzt): Gier -49,1 Grad weg, Rollen weg, Nicken +10 Grad, Augenmitte -> (1,000 / 0 / 0,727) | Hals traegt den Kopf ~0,10 m weiter vor, ~0,13 m tiefer; Schnauze landet dann bei x 1,166 (2c 1,157), Unterkante 0,55 (2c 0,53-0,55) |
| 5 | **Beine in die 2c-Ruhe** (glatte Umstellung wie das Junge, `bein_trafo`) | vorn Handgelenk **+0,21 m vor, +-0,11..0,13 m aussen**, Unterarm 0 -> 16,2 Grad; hinten Knie **+0,10 vor, +-0,07..0,09 aussen**, Unterschenkel -> 22,8 Grad |
| 6 | **Pfoten neu auf den 2c-Fussabdruck** (E-Stil: 5 Zehenballen, dunkle Sohle) | vorn 28,5 x 20 cm, hinten 29 x 19,6 cm (Ferse x -0,556, Zehen -0,264), Sohle z 0 +-0,3 cm |
| 7 | **Maul/Kiefer wie 2c**: Schnitt an der 2c-Lippenlinie (E-Kopf liegt im 2c-Kopfrahmen), Innenraum, Zaehne, Zunge, Gaumen, Wangenhaut aus `baer_maul_2c.py` (Kopie) | 874 Dreiecke (Untergrenze 700), Innenteile quer x k_b ~0,8 (E-Schnauze schmaler) |
| 8 | **Haushalt** | Koerper <= 18.950 (ohne Krallen-Geometrie) bzw. <= 18.100 (mit), Lippenschnitt ~150, Maul 874, Krallen 832 (optional) -> **<= 19.850**, hart 20.000 |
| 9 | **Gewichte** wie der 2c-/Junges-Lauf: Formel in Gelenk-Koordinaten (2c-Gelenke) + Raumglaettung + Optimierer gegen ALLE 15 2c-Clips (Matrizen aus `plan/dump/erw_2c.txt`) | p99,5 <= 2,6, max <= 4,0, Achsel/Brust <= 3,5 |
| 10 | **Export = Puffer-Tausch im 2c-GLB** (`NCBear.glb` 08ec7806): Knoten, Skin (inverseBind), 15 Animationen BYTE-GLEICH kopiert, nur das Netz neu | Dump-Bloecke BONES/OFFSET/BIND/alle CLIP textgleich mit 2c |
| 11 | **Beide Farben** aus EINER Form/UV (braun = `E_tex_final`, Fototon = `E_tex_fototon`; Netz/UV per np.array_equal gleich) | 2 x 1024 x 1024 RGB |
| 12 | **Vergleichs-Spawn** Arten `ncbeargen`/`ncbeargenfoto` = Kopie von "bear" mit eigenem Modell; NCBearFight greift nur `getAnimalType() == "bear"` (NCBearFight.lua:1787) -> nie Kampfbaer | `NCBear_GenLive()`, dazu `NCBear_GenAct(name)`, `NCBear_GenStay(on)`, `NCBear_GenClean()` |

**Ergebnis der groben Zielskizze** (`plan/bilder/plan_ziel_grob.png`, selbst angesehen): E mit s 1,70, dx 0,033, q 1,20/1,15 und dem Kopf in der
2c-Kopflage deckt den 2c-Umriss von der Seite, von vorn und von oben fast genau (Laenge ~1,93 m statt 1,96, Buckel 1,14 m wie 2c); es fehlen nur
noch die umgestellten Beine. Der Weg ist also machbar, ohne E zu verbiegen: E behaelt Kopf, Buckel, runden Hintern, Fell, Pfoten-Stil.

---------------------------------------------------------------------------------------------------------------------------------------

## 1. Bestand und Lehren

### 1.1 E heute (`_arbeit/baer_gen/aus/`)
| Datei | MD5 | Inhalt |
|---|---|---|
| `E_schoen.glb` | 0044f3e5 | Spielnetz Fotopose, 19.200 Dreiecke (GLB), 11.655 Punkte, 9.602 verschweisst, **geschlossen** (0 offene/0 nicht-mannigfaltige Kanten), 1 Netz/1 Material/1 UV, Textur eingebettet |
| `E_schoen_fototon.glb` | 0dbe612f | **gleiche Lagen/Dreiecke/UV** (np.array_equal geprueft), nur andere Textur |
| `E_schoen_textur.png` / `E_schoen_fototon_textur.png` | 06e6bdeb / 4f902c5a | 1024 x 1024 RGB; UV-Belegung 64,2 % (`plan/bilder/plan_uv_frei_E_schoen.png`) |
| Kette | | Rohmodell `aus/varianten/E_c2_form.glb` (73 MB, TRELLIS) -> `nachbesserung/form2.py` + `E_form_v9.json` (Abstandsfeld, Ohren/Pfoten/Stummel/Glaetten) -> `nachbesserung/textur2.py` + `E_tex_final.json` (braun: `farbton_drehen` 18 Grad / Saettigung 1,25) bzw. `E_tex_fototon.json` |
Offene Optik-Punkte aus GEGEN_OPTIK (E): **E-03 helle Gesichtsmaske + Mittelscheitel (major)**, E-05 Pluesch/flau (major, nur gross), E-06 Pfoten
von der Seite Platten, E-07 Kopf 49-57 Grad gedreht, E-09 Maehnenreste hinter den Ohren, E-11 kein heller Brustlatz (beim Aufrichten sichtbar).

### 1.2 Der 2c-Baer (Ziel; eigener Dump von `NCBearTest/.../NCBear.glb` 08ec7806)
- **Gelenke in Ruhe** (tier-m, aus inv(OFFSET), gleich `_arbeit/baer_junges/koerper/skelett.json ruhe_m_erw`): Bip01 (0/0/0,72), Pelvis (-0,37/0/0,72),
  Huefte (-0,46/+-0,25/0,69), Knie (-0,35/+-0,262/0,41), Sprunggelenk (-0,48/+-0,247/0,10), Ballen/Toe0 (-0,25/+-0,24/0,045), Spine (-0,06/0/0,75),
  Spine1 (0,24/0/0,80), Clavicle (0,30/+-0,10/0,92), Schulter (0,29/+-0,225/0,72), Ellbogen (0,23/+-0,24/0,41), Handgelenk (0,32/+-0,23/0,10),
  Neck (0,50/0/0,80), Head (0,70/0/0,72), **Jaw (0,8044/0/0,6454)**, Tail (-0,70/0/0,70).
- Skin-Joints 26 (alle Knochen), **Gewichte nur an 21**: KEINE an Dummy01, Bip01, Translation_Data, L/R_Clavicle, L/R_Toe0 (Dump: OFFSET dort 0;
  die Pfote haengt starr am Foot). E bekommt genau dieselbe Menge -> OFFSET-Block im Dump textgleich.
- Netz: 19.806 Dreiecke, 11.911 Punkte, 1 Netz "NCBear.001", 1 Primitiv, **0 Material-/Bild-Eintraege** (Textur kommt aus der Rasse), Indizes u16;
  42 Teile (Koerper + 41 Kleinteile = 20 Krallen + Zaehne/Zunge), 112 offene + 41 nicht-mannigfaltige Kanten (alle an Kleinteilen/Maul).
- Masse: Laenge 1,957 (x -0,800..1,157), Breite 0,798 (halb 0,399 bei x -0,43, Taille 0,337 bei x -0,1), Buckel 1,146 bei x 0,21, Ruecken ueber der
  Huefte 1,05, Bauch 0,351-0,36, Beine laufen bei z ~0,38-0,40 in den Rumpf. Kopf: Augen (1,000/+-0,065/0,727), Abstand 0,130; Nasenspitze
  (1,154/0/0,638); Mundwinkel (0,975/+-0,053/0,612); Lippe vorn (1,093/0/0,583); **Auge-Nase-Linie -30,3 Grad** (Idle 0: -33,5; Walk -36; Sit 60: -9).
- Pfoten (Haut ohne Krallen, z < 4 cm): vorn x 0,239..0,524 (28,5 cm), y 0,114..0,313 (20 cm); hinten x -0,556..-0,264 (29,2 cm), y 0,144..0,340
  (19,6 cm). Krallen vorn bis x 0,561, hinten bis -0,244 (Spitzen z 0,5-1 cm).
- Gelenk im Bein-Schnitt (Fuer das Fotogerippe von E, 2.2): Handgelenk bei z 0,10 auf 48 % (hinten->vorn) / 57 % (innen->aussen) des Schnitts,
  Sprunggelenk 38 % / 53 %; Ellbogen auf 39 % des Unterarm-Schnitts bei z 0,35, **Knie auf 86 % (vorn!)** des Schenkel-Schnitts bei z 0,35.

### 1.3 Bodenkontakt des 2c-Baeren je Clip (Grundlinie; `plan/mess/kontakt_2c_teile.json`, tiefster Punkt in cm)
| Clip | Vorderpfote | Hinterfuss | Becken/Schenkel | Rumpf/Schulter | Kopf/Hals | Kleinteile (Krallen) |
|---|---|---|---|---|---|---|
| Idle01 | 0,0 | 0,0 | 31,0 | 32,2 | 46,2 | 0,5 |
| Walk | 0,0 | **-1,16** | 26,4 | 30,6 | 43,0 | **-2,40** |
| Run | -0,15 | 0,0 | 23,5 | 24,0 | 42,2 | **-2,98** |
| Death / Dead | 0,0 / 3,0 | -0,14 / 2,8 | **10,4** | **10,5** | 12,6 | 0,0 / 1,1 |
| Rear | 0,0 | -0,06 | 29,9 | 28,3 | 39,4 | 0,5 |
| SwipeL/R, Slam, Bite | -0,33..0 | 0,0 | 28-30 | 21-27 | 5,4 (Slam) .. 33 | 0,5 |
| Maul / **Eat** | 0,0 | 0,0 | 30,6 | 22,7 / 25,8 | **0,74 / -0,04** | 0,5 |
| SitDown / **Sit** / StandUp | 0,0 | 0,0 | **0,15 / 0,15 / 0,11** | 24-26 | 47-82 | 0,5 |
Lesart: aufliegen tun nur Pfoten, **die Sitzflaeche (Sit-Trio)** und **die Schnauze (Eat, Maul)**. Die Ruhe-Lage dieser Kontaktpunkte
(`kontakt_zonen_2c.json`): Sitzflaeche x -0,62..-0,58 / y -0,29..+0,28 / z 0,32..0,42 (Unterseite des Hinterns hinter und unter der Huefte);
Schnauze x 1,087..1,157 / z 0,53..0,66. **Tot liegt auch der 2c-Rumpf 10,4 cm ueber dem Boden** (Clip-Sache, nicht Netz; siehe Fragen).

### 1.4 Lehren aus dem Rig-Lauf des Jungen (rig/*.md) -- was hier anders gemacht wird
| Lehre | Folge hier |
|---|---|
| Eigener Trab/Galopp + lange Beine -> "laeuft wie eine Giraffe", Kevin: altes Junges "definitiv besser" | **keine eigenen Clips**, Walk/Run/Translation_Data byte-gleich = Tempo und Gang wie 2c |
| Kopf hoch wie im Foto -> Fressen 18 cm ueber dem Boden, Gesicht aus Kevins Kamera klein | **Kopf in die 2c-Kopflage** (Schnauze erreicht den Boden wie 2c) |
| F2 "nur Punkte des Spielnetzes verschieben" faltete Brust/Schulter; Saeulen-Tausch gab Stufen an Knie/Ellbogen | **Rohmodell glatt verformen** (`bein_trafo`, Winkel-Mischung) und form2/textur2 in Ruhe NEU laufen lassen (frisches Fell, keine verzerrten Striche) |
| Kopfmaske bis in den Nacken = Nacken starr | Kopf starr nur vor der Ebene Atlas - 0,03 m; Hals harmonisch (Kotangens-Laplace) |
| Pfoten-Uebergang 5 cm -> Handgelenk riss (sigma1 11,7) | Pfote = 1 - sst(Gelenk - 0,005; Gelenk + 0,085; z), 9 cm |
| Optimierer schob Hand ans Brustbein | Regel `traeger` (Knochen nur, wo die Formel ihn im Umkreis ~8 cm hat), Seitenregel, `fremd` |
| Assimp JOIN_IDENTICAL_VERTICES legt Ober-/Unterlippe zusammen | Unterlippen-UV +2e-4 versetzen (wie `baer_maul_2c.py`) |
| Kamera-Matrix erst nach `view_layer.update()` aktuell; Blender loeste relative Pfade gegen `C:\` auf | nur absolute Pfade, `update()` nach jeder Kameradrehung |
| alter Dump = altes Netz | jede Zahl aus dem Dump des fertigen GLB |

---------------------------------------------------------------------------------------------------------------------------------------

## 2. Messung E gegen 2c (`plan/mess/mess_e_2c.json`, `gelenke_e_2c.json`, `kopf_passung.json`, Blaetter `plan/bilder/`)

### 2.1 Grundmasse
| Mass | E roh | E bei s 1,70 | 2c (m) | Lesart |
|---|---|---|---|---|
| Buckel (Widerrist) | 0,670 (x 0,10) | **1,14** (x 0,20) | 1,146 (x 0,21) | deckt sich |
| Ruecken ueber der Huefte | 0,678 | 1,15 | 1,05 | E-Ruecken waagerecht, Heck 10 cm hoeher (bleibt: Generator-Form) |
| Bauch tiefster Punkt (Mitte) | 0,214 | **0,36** | 0,351-0,36 | deckt sich |
| Beine laufen in den Rumpf | ~0,225 | 0,38-0,39 | 0,38-0,40 | deckt sich -> Beinlaenge passt ohne Streckung |
| Laenge Heck -> Schnauze | 0,959 (Kopf gedreht) | 1,63 (gedreht) / **~1,93** (Kopf in 2c-Lage) | 1,957 | fast gleich |
| Breite | 0,403 | 0,69 | 0,80 | **E 14 % schmaler** -> q (Abschnitt 3.3) |
| Halbbreite Schulter (x 0,17) / Taille (x -0,1) / Huefte (x -0,43) / Heckende (x -0,63) | | 0,311 / 0,326 / 0,343 / 0,282 | 0,383 / 0,337 / 0,399 / 0,363 | Verhaeltnis 1,23 / 1,03 / 1,16 / 1,29 |
| Augenabstand | 0,0755 | **0,128** | 0,130 | **Kopfgroesse passt bei s 1,70 von selbst** |
| Auge -> Nase | 0,113 | 0,193 | 0,178 | E-Schnauze 1,5 cm laenger |
| Auge-Nase-Linie | -40,2 Grad (Fotopose, Kopf um 49,1 Grad nach links gegiert) | | -30,3 Grad | Kopf +10 Grad heben |
| Pfote vorn L x B (z < 4 cm) | | 0,22-0,24 x 0,15-0,16 | 0,285 x 0,20 | E-Vorderpfote kleiner |
| Pfote hinten L x B | | 0,31-0,32 x 0,17-0,18 | 0,292 x 0,196 | ~gleich |
| Dreiecke / Textur | 19.200 / 1024 RGB | | 19.806 / 1024 RGB | |
Warum s = 1,70 und nicht "Laenge 1,96 wie das Standmodell" (s 2,04): dann waere E 1,36 m hoch, Beine bis zum Bauch 0,44-0,50 m statt 0,39
(Ellbogen/Knie liegen fest bei 0,41) -- Beine muessten gestaucht und der Rumpf 10 cm gesenkt werden. Bei 1,70 passen Hoehe, Bauch, Beinansatz,
Buckel und Kopfgroesse gleichzeitig; nur die Breite und die Beinstellung muessen an das Skelett.

### 2.2 Beine (Achsen = Schnittmitten der Beine, Fotopose x 1,70 + dx 0,033; `gelenke_e_2c.json`, Blatt `plan_gelenke_e_2c.png`)
| Bein | E-Achse bei z 0,10 -> 2c Hand/Sprung | Weg | E-Achse bei z 0,41 -> 2c Ellbogen/Knie | Weg | Neigung E -> 2c |
|---|---|---|---|---|---|
| VL | (0,108 / 0,116) -> (0,32 / 0,23) | **+0,21 vor / +0,11 aussen** | (0,104 / 0,161) -> (0,23 / 0,24) | +0,13 / +0,08 | -1 -> -16 Grad (Pfote vor dem Ellbogen) |
| VR | (0,112 / -0,096) -> (0,32 / -0,23) | **+0,21 / 0,13 aussen** | (0,18 / -0,115) -> (0,23 / -0,24) | +0,05 / 0,125 | +12 (Schaetzung unsicher, Bein laeuft in die Brust) -> -16 |
| HL | (-0,483 / 0,193) -> (-0,48 / 0,247) | 0,00 / +0,05 | (-0,459 / 0,197) -> (-0,35 / 0,262) | **+0,11 / +0,065** | +4 -> +23 Grad |
| HR | (-0,40 / -0,189) -> (-0,48 / -0,247) | -0,08 / 0,06 | (-0,446 / -0,177) -> (-0,35 / -0,262) | **+0,10 / 0,085** | -8,5 -> +23 Grad |
Die Fotopose steht "gesammelt": Vorderbeine senkrecht und eng unter der Brust (Pfoten ~25 cm auseinander statt 46), Hinterbeine senkrecht unter
der Huefte. Die 2c-Ruhe ist ein gestreckter, breiter Stand (Unterarm 16 Grad vor, Unterschenkel 23 Grad zurueck) -- im Spiel stellt ohnehin
Idle01 die Beine. Die Wege sind gross (vorn bis 21 cm), aber das Junge hat 7,6 cm quer + 26 Grad Drehung sauber geschafft (FORM.md 2).

### 2.3 Kopf (Probe `kopf_passung.py`: E-Kopf STARR, Augenmitte auf die 2c-Augenmitte, Auge-Nase -30,3 Grad, gerade)
| x (m) | E oben / unten / halb | 2c oben / unten / halb |
|---|---|---|
| 0,85 | 0,909 / 0,516 / 0,209 | 0,854 / 0,531 / 0,191 |
| 0,95 | 0,854 / 0,542 / 0,158 | 0,830 / 0,538 / 0,133 |
| 1,00 | 0,798 / 0,551 / 0,080 | 0,810 / 0,550 / 0,096 |
| 1,05 | 0,719 / 0,546 / 0,058 | 0,702 / 0,529 / 0,081 |
| 1,10 | 0,682 / 0,549 / 0,055 | 0,685 / 0,543 / 0,075 |
| vorderste Spitze | x 1,166 | x 1,157 |
**Die E-Schnauze landet in Hoehe und Laenge auf +-1,5 cm auf der 2c-Schnauze** -> die Schnauze erreicht im Fressen den Boden wie 2c (Kontaktzone
x 1,09-1,16 / z 0,53-0,66), und die 2c-Lippenlinie, das 2c-Kiefergelenk und der 2c-Innenraum passen in den E-Kopf. Unterschied: **E-Schnauze
ist 20-30 % schmaler** (halb 4,4-5,8 cm statt 6,9-8,1) -> Innenraum quer skalieren (3.6). Hinterkopf/Wangen breiter (Ohren). Gegen die Fotopose
(nur gerade gedreht, Augenmitte bei (0,90/0/0,857)) muss der Kopf ~0,10 m vor und ~0,13 m tiefer: **der Hals wird ~0,16 m laenger** (3.3.4).

### 2.4 Sitz-/Liege-Probe (`sitz_probe.py`, E-Heck mit Gewichten des naechsten 2c-Punkts, Clips aus dem Dump; nur Schaetzung)
| dx | q | Sit 0/60, SitDown 48: tiefster Heckpunkt E (2c 0,0) | Dead: E-Heck (2c 9,8) |
|---|---|---|---|
| 0,033 | 1,00 / 1,10 / 1,20 | +0,9 / +1,3 / +1,2 cm | 16,2 / 13,0 / **9,8** cm |
| 0,09 | 1,00 / 1,10 / 1,20 | +3,9 / +3,9 / +4,0 cm (schwebt) | 16,9 / 13,6 / 10,4 |
-> dx klein halten (Heck weit hinten), Huefte q ~1,15-1,2. Die Sitzflaeche muss nach dem Umstellen mit der Attrappe neu gemessen werden (3.8).

### 2.5 Blaetter (alle selbst angesehen)
- `plan/bilder/plan_e_gegen_2c_s170.png`: 6 Ansichten (Seite, vorn, oben, Kevins Kamera 0/30, 45/30, hinten) je 2c-Ton + Skelett | E-Fotopose x 1,70 |
  uebereinander (blau 2c, rot E-Umriss), dazu Spielgroesse (~101 px/m).
- `plan/bilder/plan_gelenke_e_2c.png`: Seite/vorn/oben, E-Ton mit Beinachsen (rot), 2c-Gelenke beschriftet (blau), Wege E -> 2c (gelb).
- `plan/bilder/plan_ziel_grob.png`: GROBE Zielskizze (Kopf in 2c-Lage, Rumpf q, Beine noch nicht umgestellt) gegen 2c -- Umriss deckt sich.
- `plan/bilder/plan_uv_frei_E_schoen.png`: UV-Belegung von E heute mit den groessten freien Rechtecken.
Gesehen: E ist in der Fotopose ein kompakter, hoher Baer mit Kopf auf Rueckenhoehe; in die 2c-Kopflage gesetzt wirkt er wie ein breiterer,
rundkoepfiger 2c -- Buckel, runder Hintern und Ohren bleiben erkennbar. Die grobe Skizze zeigt am Hals eine Falte (lineare Mischung) -- genau das
muss der Bau mit Winkel-Mischung + Laplace-Band + form2-Glaettung vermeiden.

---------------------------------------------------------------------------------------------------------------------------------------

## 3. FORM: wie das Netz auf das 2c-Skelett kommt (Rolle BAU FORM + TEXTUR; Ordner `R/form/`, R = `_arbeit/baer_gen_gross`)

### 3.0 Grundsatz
Werkzeuge des Jungen kopieren (Originale nie aendern, MD5 vorher/nachher in `R/form/eingang/md5_original.txt`):
`baer/spiel/baer_form_rig.py` -> **`baer/spiel/baer_form_gengross.py`** (Teile `plan` | `abgabe`), `_arbeit/baer_gen/rig/form/werkzeug/{bein_trafo,
raw_ruhe2, form2_rig, textur2_rig, glb_lib, rblick, cfg_ruhe, blatt_form, montage, texel_flecken*, pixel_3d}.py` -> `R/form/werkzeug/*_gengross.py`
(gleiche Namen mit Endung `_gengross`). Aufruf von `nachbesserung/form2.py`/`textur2.py` nur ueber diese Kopien. Ablauf:
**Fit (3.1) -> Fotogerippe (3.2) -> Rohmodell in die 2c-Ruhe verformen (3.3) -> form2 (3.4) -> TON-Runde ansehen -> textur2 braun + Fototon
(3.5) -> Meter-Rahmen -> Maul (3.6) -> Krallen (3.7, optional) -> Kontakt-Vorprobe (3.8) -> Abgabe (3.9).** Mehrere Runden 3.3-3.4 erlaubt
(je ~1-4 min CPU); erst wenn das TON-Blatt neben dem 2c stimmt, textur2 starten (GPU, Sperre).

### 3.1 Rahmen und Fit
1. Rohmodell `aus/varianten/E_c2_form.glb` wie `form2.py` laden (Drehung `dreh_z` wie dort), in tier roh; Mittelebene y aus Rumpf z 0,45-0,75 roh
   (heute -0,0131 im E_schoen-Rahmen; mit Rumpf-Scherung dy(x) Grad 3 wie das Junge, falls E einen Bogen hat).
2. **s** (Start 1,70) als Kleinste-Quadrate ueber: Bauch-Mitte 0,355 m, Beinansatz 0,39 m, Buckel 1,146 m, Ellbogen-/Kniehoehe der Beinachsen
   0,41 m; erlaubt 1,66-1,74, ausserhalb begruenden. Die Augenmitte (Kopfgroesse) ist die Gegenprobe: Augenabstand 0,125-0,135 m.
3. **dx** (Start +0,033): Huefte von E (Fotogerippe 3.2) ueber die 2c-Huefte x -0,46; Grenze: Sitz-Vorprobe (3.8) <= +1,5 cm Abstand der Sitzflaeche.
4. **q(x)** Querfaktor fuer y, glatt (Stuetzwerte bei x -0,80/-0,60/-0,45/-0,10/0,15/0,35/0,55: q_h*0,97 / q_h / q_h / 1,03 / q_s / q_s / 1,0), nach
   unten in die Beine auslaufend (die Beine werden NICHT breiter, nur mitgeschoben, 3.3.3), nach vorn in den Hals auf 1,0 (Kopf bleibt 1,0).
   Start q_s = 1,20, q_h = 1,15. Kriterien: Gesamtbreite <= 0,82 m (2c-Regel C4); Schulter-/Hueftgelenk >= 6 cm unter der Haut; Oberarm/Schenkel
   von vorn innerhalb des Rumpfumrisses; Dead-Rumpf <= 2c + 2 cm (3.8); Ton von vorn/hinten neben `ref_hinten_grizzly.jpg` kein Fass, kein "Ei".

### 3.2 Fotogerippe von E (Gelenke der Fotopose, roh)
Gleiche 26 Namen. Lage je Gelenk so, dass es im E-Bein an DERSELBEN relativen Stelle liegt wie das 2c-Gelenk im 2c-Bein (1.2): Handgelenk/
Sprunggelenk auf z = 0,10/s im Schnitt bei 48/57 % bzw. 38/53 %; Ellbogen/Knie auf z = 0,41/s, Ellbogen 39 % (hinten->vorn) des Unterarm-Schnitts,
**Knie 86 % (vorn) des Schenkel-Schnitts** (Schnitte bei 0,35/s und darueber extrapoliert, wo das Bein in den Rumpf laeuft); Schulter = Ellbogen
+ (0,06 / -0,015 / 0,31)/s, Huefte = Knie + (-0,11 / -0,012 / 0,28)/s (2c-Richtungen). Kopf: Augenmitte/Kopfrahmen aus
`nachbesserung/form/E_v9/form_info.json kopf_rahmen_spiegel` (augen_mitte, vorn, seitlich, oben). Abgabe als `R/form/fotogerippe.json` + Blatt.

### 3.3 Rohmodell in die 2c-Ruhe verformen (`R/form/werkzeug/raw_ruhe_gengross.py`, Blender CPU, Kopie von raw_ruhe2.py + bein_trafo)
Reihenfolge (jede Stufe glatt, keine Topologie-Aenderung, verschweisste Punkte bleiben zusammen):
1. **Rumpf gerade** (Scherung dy(x)), **Massstab** s (in roh bleibt alles roh; die 2c-Ziele werden nach roh umgerechnet: Ziel_roh = (2c - (dx,0,0))/s).
2. **Quer q(x)** fuer den Rumpf (z > Beinansatz - 0,03/s); Beine werden als Block mit der Verbreiterung ihrer Ansatzstelle quer verschoben.
3. **Beine glatt** mit `bein_trafo_gengross.py`: je Bein J (Ellbogen/Knie Foto) -> Jz (2c), K (Hand/Sprung Foto) -> Kz (2c): Drehung um J mit
   Winkel-Mischung, Streckung entlang der Achse (erlaubt 0,92-1,10), Querverschiebung J -> Jz in einem BREITEN Band (Schulterblatt/Oberschenkel
   gleiten mit, Band >= 0,15 m, damit die Brust nicht faltet -- Lehre f2_t1), Pfote nur verschoben (nicht gekippt). Neu gegen das Junge: auch der
   Oberarm/Oberschenkel dreht (Ellbogen +0,05..0,13 vor, Knie +0,10 vor): Drehung um Schulter/Huefte mit Winkel-Mischung im Band.
   **Standbein-Wahl:** je Paar das sauberere Foto-Bein umstellen (Vorschlag VR, HR wie beim Jungen), das andere entsteht als Spiegelbild
   unterhalb `z_spiegel` (form2_rig e5 `koerper_spiegel`); Farbquelle: unten Spiegelbild, oben links Fotoseite (E-Fotoansicht az 90 = linke Seite).
   Ziel-Richtungen = 2c-Knochen: Oberarm 11,0 Grad zurueck, Unterarm 16,2 vor, Oberschenkel 21,4 vor, Unterschenkel 22,8 zurueck, Fuss 13,4 Grad.
   Luecke zwischen Bein und Bein (Netz) >= 4 cm bis zum Beinansatz; Hinterfuss/Unterarm frei.
4. **Kopf + Hals:** Kopf STARR (vor der Ebene Atlas-Kehle minus 3 cm, Ohren immer) mit der Trafo "Fotokopf -> 2c-Kopflage": Gier -49,1 Grad und
   Rollen zurueck (Kopfrahmen gerade, Mittelebene des Gesichts = y 0), Nicken so, dass die Auge-Nase-Linie **-30,3 +-2 Grad** hat, Lage so, dass
   (a) Augenmitte (1,000 / 0 / 0,727) +-2 cm, (b) Nasenspitze x 1,154 +-2 cm, z 0,638 +-1,5 cm, (c) Schnauzen-Unterkante x 1,05-1,13 gegen
   2c z 0,53-0,55 +-1,5 cm (Fress-Kontakt). Gewichtet a:b:c = 1:1:2; optional ein gleichmaessiger Kopf-Faktor h 0,95-1,05 (Aussenform bleibt).
   Rumpf fest hinter dem Buckel-Gipfel (x <= 0,20 m) und unter z 0,55 m; **dazwischen harmonische Gewichte** (Kotangens-Laplace auf dem Spielnetz,
   per 6 Nachbarn aufs Rohmodell, wie das Junge) und **Winkel-Mischung** (nie lineare Lage-Mischung -> die Falte der Grobskizze).
   Die ~0,16 m Halsverlaengerung auf das GANZE Band Buckelvorderkante -> Hinterkopf verteilen (Streckung <= 1,35 je Richtung); Kehle/Brust vorn
   ziehen mit nach vorn-unten. Messen: Halsdicke (oben-unten) in der Mitte >= 2c-Wert, keine Einschnuerung, Nackenlinie ohne Stufe.
5. Ausgabe `R/form/f2/raw_ruhe_form.glb` (Form-Quelle) und `raw_ruhe_tex.glb` (Farbquelle), `plan.json/plan.npz` (alle Trafos, damit textur2 und
   die Kontaktprobe dieselben Zahlen lesen).

### 3.4 form2 in der Ruhe (`form2_gengross.py` + `R/form/E_form_ruhe.json` aus `E_form_v9.json` umgerechnet)
- Umrechnen wie `baer_form_rig.py plan`: alles mit `kopfrahmen: true` (Ohren, Flicken, Regionen am Kopf) ueber den neuen Kopfrahmen; Rumpf-Regionen
  (`buckel_wulst`, `schulter`, `hals_wangen`, `heck_lappen`, `nacken_fuellen`) ueber die Verformung ihres Mittelpunkts, Radien x Streckung.
  `spiegel` (Kopfebene) = y 0; `stummel` am Heck nach der Verformung (Lage pruefen: Tail-Gelenk (-0,70/0/0,70) liegt dann im Hinterteil).
- **Pfoten neu am 2c-Fussabdruck** (`pfoten.liste` xy = 2c-Pfotenmitten in roh; `sohle_vorn`/`sohle_hinten`, `sohle_breite` so, dass vorn 28,5 x 20 cm,
  hinten Ferse x -0,556 bis Zehen -0,264 und 19,6 cm breit herauskommen, Sohle flach auf z 0, `z_schnitt` = Handgelenk-/Sprunghoehe - 2 cm);
  E-Stil bleibt: 5 Zehenballen, Knoechel rund, keine Platte von der Seite (E-06: Unterkante Radius >= 1,2 cm roh, `glaetten_je_bein` wie E_v9).
- Ohren unveraendert (E-02 ist erledigt); nach dem Geraderichten von vorn ueber dem Kopfumriss pruefen.
- **TON-Runde (Pflicht vor textur2):** `rblick_gengross.py` Ton aus Kevins Kamera (az 0 / el 30), az 45/30, Seite az 90 el 0 und el 30, vorn, hinten,
  oben -- jeweils NEBEN dem 2c-Ton (gleiche Kamera, gleicher Massstab) und mit 2c-Skelett eingeblendet; Gelenke >= 2 cm unter der Haut
  (Ellbogen/Knie/Hand/Sprung >= 1,5 cm); Beinachse gegen Knochenrichtung <= 4 Grad. Erst weiter, wenn die Bild-Fragen 10.4 Nr. 1-4 "ja" sind.

### 3.5 textur2 in der Ruhe, beide Farben (`textur2_gengross.py`, `R/form/E_tex_ruhe_braun.json`, `E_tex_ruhe_foto.json`)
- Aus `E_tex_final.json` bzw. `E_tex_fototon.json` umgerechnet (Regionen/Malerei mit Koordinaten ueber `plan.json`), Farbquelle `raw_ruhe_tex.glb`.
  **Gleiches Netz + gleiche UV** fuer beide: Lauf braun erzeugt Netz/UV; Lauf Fototon mit identischem Netz (gleiche `saat`/Parameter oder Netz
  aus dem braunen Lauf laden) -- Pruefung `np.array_equal` auf Lagen/Dreiecke/UV, sonst Fototon nur umfaerben.
- **Dreiecksziel:** Koerper nach dem Vereinfachen <= 18.950 GLB-Dreiecke ohne bzw. <= 18.100 mit Krallen-Geometrie (`ziel_dreiecke` heute 19.800 ->
  19.200; Startwert ~19.500 bzw. ~18.650, nachregeln). Kopf/Pfoten weiter dichter (dichte 2,5).
- **UV-Reserve** fuer die Flecken (3 px Saum, nach dem Packen mit der Logik von `plan/mess/uv_frei.py` suchen): Gaumen 94 x 104, Zunge 94 x 104,
  Zahn/Zahnfleisch/Lippe-Streifen 206 x 25 (Masse wie 2c; andere Seitenverhaeltnisse bei gleicher Flaeche erlaubt), Krallen-Streifen 64 x 16
  (nur mit Geometrie-Krallen). Passt es nicht: Inseln beim Packen x 0,95 und neu suchen. Flecken in BEIDEN Texturen gleich.
- **Optik-Punkte, die hier billig mitgehen:** E-03 Gesicht/Stirn auf Rumpfton (Helligkeit Kopf/Rumpf aus Kevins Kamera 0,95-1,05) und
  Mittelscheitel weg (Strich von der Nase nach hinten); **kein dunkler/heller Ring am Hals** (2c-G2-Lehre: Ring 0-4 cm / Kopf innen Helligkeit
  >= 0,92 und <= 1,08, Feinkontrast <= 1,20); E-09 Maehnenreste hinter den Ohren weich; E-11 Brust/Kehle 10-15 % heller (beim Aufrichten
  sichtbar, `ref_aufrecht_vorn.jpg` nur ansehen); E-05 Fellkontrast etwas hoeher, wenn die Spielgroesse ruhig bleibt (Helligkeits-Streuung >= 42).
- Belichtung eichen wie textur2 (Render/Textur 1,00 +-0,01); Farbmittel in der Fotoansicht wie heute (braun 23 Grad, Fototon 358 Grad).

### 3.6 Maul und Kiefer (`baer/spiel/baer_maul_gengross.py` = Kopie von `baer_maul_2c.py`; Aufruf aus `baer_form_gengross.py`)
Warum das geht: der E-Kopf liegt nach 3.3.4 im **2c-Kopfrahmen** (K_HO/K_HA/K_HB/K_HC, `fbx2l`, `k_lippe`, `K_ECKE` gelten in tier-Metern des
Spielnetzes -- E steht in genau diesem Rahmen). Also:
1. **Schnitt** an der 2c-Lippenflaeche f = c - k_lippe(a, |b|) - dc (Region `a > K_ECKE - 0,03` und x > 0,80 wie 2c). dc (Start 0) so waehlen, dass
   der Schnitt auf E eine einfache Linie von Mundwinkel zu Mundwinkel ist (die Pruefungen `assert` in maul_bauen bleiben) und vorn 5-6 cm unter
   der Nasenmitte, am Mundwinkel 10-12 cm unter dem Auge liegt (2c: Lippe vorn (1,093/0/0,583), Ecke (0,975/+-0,053/0,612)); Abweichung <= 1,5 cm,
   sonst begruenden. Die gemalte E-Maullinie (`malen.maul`) danach auf die Schnittlinie legen (Textur-Lippenkante dunkel).
2. **Innenraum wie 2c** (SPEZ_2C 3.1-3.4, 874 Dreiecke: Eckzaehne 168, Schneidezaehne 72, Backenzahn-Leisten 96, Gaumen + oberer Wall 150, Boden +
   unterer Wall 110, Zunge 110, innerer Lippenstreifen 120, Wangenhaut 32, Rachen 16; Sparfassung 700). Quer-Faktor **k_b** = Schnauzen-Halbbreite
   E / 2c an a 0,30 und 0,42 (gemessen ~0,75-0,85) fuer alle b-Lagen des Innenraums; Kronen x min(1; k_b + 0,1) (sichtbar bleiben: obere Eckzaehne
   in Spielgroesse >= 4 px hoch im Rear-Bild 48). Teile starr Head (oben) / Jaw (unten) mit Gewicht 1,0.
3. **Kiefer-Anteil** der Aussenhaut: `kiefer_anteil(a, f, seite)` aus 2c (Wange/Kinn weich zum Hals), Unterlippen-Zwillinge UV +2e-4.
4. **Flecken** (`flecken_malen` mit den 2c-Farben) in die reservierten Rechtecke beider Texturen.
5. **Probe in FORM** (vor der Abgabe, starres Oeffnen um das Jaw-Gelenk mit den vorlaeufigen Gewichten): Kiefer 0/5/24/34/38 Grad (= Sit, Eat,
   Bite, Rear) Ton + Textur nah und Spielgroesse neben 2c Rear Bild 48: Zaehne/Zunge sichtbar, keine Zahnspitze ausserhalb der Lippen bei
   Maul zu (Windungszahl, Luft >= 2 mm), kein Loch an den Mundwinkeln.
**Rueckfall** (nur wenn der Schnitt auf E nicht als einfache Linie geht): Lippenflaeche aus E-Landmarken als glatte Kurve neu definieren (gleiche
Schnittlogik); Maul zu = Rueckschritt gegen 2c, nur mit Beleg und als major melden.

### 3.7 Krallen (optional, Stufe nach dem Maul)
Wenn der Haushalt es erlaubt: die 20 Krallen des 2c (Kleinteile, 832 Dreiecke, Form) an die E-Zehenballen setzen (je Kralle starr: Wurzel an die
Zehenspitze, Richtung wie 2c), Gewicht 1,0 an Hand/Foot, UV auf den Krallen-Streifen (Verlauf Wurzel dunkel -> Spitze horngrau wie E-Malerei).
Spitzen so weit anheben, dass in KEINEM Clip ein Punkt tiefer als -1,5 cm liegt (2c-Krallen gehen in Walk -2,4, Run -3,0 cm -- hier verboten).
Sonst Sparfassung (20 x ~24 Dreiecke, 30 % kuerzer) oder bei gemalten Krallen bleiben (E heute; aus Kevins Kamera "gut", GEGEN_OPTIK E-06).

### 3.8 Kontakt-Vorprobe (Pflicht vor der Abgabe; `R/form/werkzeug/kontakt_probe_gengross.py`, CPU)
Attrappe: Ruhe-Netz in Metern, Gewichte = naechster 2c-Punkt gleicher Region (Seite, Bein, Kopf/Kiefer getrennt) bzw. `gewichte_2c.npz`, Clips aus
`plan/dump/erw_2c.txt`. Messen und mit 1.3 vergleichen: Stuetzpfoten je Bild (Grenze +-1,5 cm), Sitzflaeche Sit/SitDown-Ende/StandUp-Anfang
(0..+1,5 cm), Schnauze Eat/Maul in den Bildern mit 2c-Kopf < 1 cm (-0,5..+1,5), Dead/Death Rumpf (<= 2c + 2 cm), ganzes Netz >= -1,5 cm.
Faellt etwas durch: Form nachstellen (dx, Heck-Unterseite, Pfoten-Sohle, Kopf-Lage) -- **nicht** an die Clips gehen.

### 3.9 Abgabe FORM (`R/form/`)
| Datei | Inhalt |
|---|---|
| **`E_gen_basis.npz`** (massgeblich) | tier-Meter bei 1,0, 2c-Rahmen: `V` verschweisst, `T`, `T_glb`, `glb_punkt`, `UV` je GLB-Punkt (glTF, v von oben -- beim Export NICHT spiegeln), Masken je Punkt: `kopf` (starr), `ohr_l/_r`, `kiefer_aussen` (+ Anteil), `maul_innen_head`, `maul_innen_jaw`, `lippe_ober`/`lippe_unter` (Zwillinge), `kralle`, `pfote_VL/VR/HL/HR`, `sohle`, `stummel`, `hals_band`; `W_vorlaeufig` (n x 26, aus 3.8) |
| `E_gen_basis.glb` + `E_gen_braun.png` + `E_gen_foto.png` | zum Ansehen (ohne Skin), beide Texturen 1024 x 1024 RGB 8 Bit |
| `landmarken_gen.json` | Augen, Nase, Lippe vorn, Mundwinkel, Ohrspitzen, Hinterkopf, Kehle, Buckel, Kruppe, Bauch, Heckende, Stummel, Sitzflaeche; je Bein Achsenpunkte, Gelenktiefe unter der Haut, Pfote (Ferse/Ballen/Zehen/Sohlenrand); s, dx, q-Stuetzwerte, Kopf-Trafo, k_b, dc |
| `pruef_form.json` | alle Zahlen aus 3.1-3.8 und Abschnitt 6 (Teil K) |
| `fotogerippe.json`, `plan.json/.npz`, `E_form_ruhe.json`, `E_tex_ruhe_*.json`, `f2/` | Kette zum Wiederholen |
| `R/FORM.md`, `R/bilder/form_*.png` | Bericht + Blaetter (10.1) |

### 3.10 Generator-Schoenheit: was bleibt, was sich aendert
**Bleibt:** Kopf (Form, Ohren, Augen, Nase, gemalte Details), Schulterbuckel, runder Hintern mit Stummel, Fell-Malerei und Farbe (beide Toene), Pfoten-
Stil (Ballen, dunkle Sohle), die Rumpfform im Seitenriss. **Aendert sich (Pflicht durch das 2c-Skelett):** Kopf tiefer/weiter vorn wie beim 2c
(Hals ~16 cm laenger), Rumpf 15-20 % breiter (wie 2c), Beine im breiten 2c-Stand, Pfoten 2c-gross, Maul mit Innenraum.

---------------------------------------------------------------------------------------------------------------------------------------

## 4. GEWICHTE (Rolle BAU SKELETT + GEWICHTE + CLIPS; Skript `baer/spiel/baer_gewichte_gengross.py`, Ordner `R/rig/`)

Kopie von `baer/spiel/baer_gewichte_rig.py` (Teile `formel` / `opt` / `dehnung` / `abgabe`; ist selbst die bereinigte Kopie von `baer_gewichte_2c.py`
ohne KOPF_ALT/alt_von/k1_dy/k2c_dx). Aenderungen:
1. **Skelett = 2c** (`plan/mess/mess_e_2c.json 2c_m.gelenke` bzw. aus dem Dump): keine Faktoren R/Q, keine Becken-Regel.
2. **Formel** (Gelenk-Koordinaten): Beine entlang Huefte/Schulter -> Knie/Ellbogen -> Sprung/Hand (Uebergaenge Huefte/Schulter 0,10 m, Knie/Ellbogen
   0,07, Pfote 9 cm: `1 - sst(G - 0,005; G + 0,085; z)`), Schritt-/Brustbein-Regel an der Linie, wo linkes und rechtes Bein zusammenlaufen;
   Rumpf Pelvis -> Spine -> Spine1, Uebergaenge 0,20; **Kopf starr** (Maske `kopf`, Ohren dabei) = Head 1,0; Hals harmonisch (Head = sst(0,3;1;h),
   Rumpf = 1 - sst(0;0,7;h), Neck = Rest); **Kiefer** = Maske `kiefer_aussen` mit dem 2c-Anteil, Innenraum starr (Head/Jaw 1,0), Lippen-Zwillinge
   wie maul_bauen; Stummel/Heck: Tail wie die 2c-Formel (2c hat 184 Punkte mit Tail am ganzen Heck; Tail dreht in Dead/Death bis 154 Grad, in
   Swipe 17 Grad -> Optimierer entscheidet, Stummel nie > 0,6 Tail); Krallen starr an Hand/Foot. **Keine Gewichte an Clavicle, Toe0, Dummy01,
   Bip01, Translation_Data** (wie 2c).
3. **Raumglaettung** sigma 0,03 m je Koerperhaelfte ausser starren Zonen; Seitenregel (links nie rechts, Vorderbein nie hinter der Rumpfmitte
   x -0,085 und umgekehrt, Hals/Kopf nie am Bein), <= 4 Einfluesse, Summe 1.
4. **Optimierer** gegen die ENDGUELTIGEN Matrizen = die 15 2c-Clips aus `plan/dump/erw_2c.txt` (byte-gleiche Clips -> der Dump des fertigen GLB hat
   dieselben Matrizen; kein Vorab-GLB noetig): jedes 3. Bild + SwipeL/R Bilder 6-23 einzeln + Liegebilder (Dead, Death ab 75 %) mit Faltenstrafe
   + 16 Probe-Posen (Kopf +-30/+-35, Beine +-35). Frei: Rumpf, Hals, Achsel, Leiste, Bein-Uebergaenge; fest: Kopf, Kiefer-Innenraum, Lippen,
   Pfoten (Formel >= 0,95), Krallen. Regeln `traeger`, `fremd`, `ueber_w/ueber_s` (3,5), `achsel_w` 20 ueber 3,0, `boden` 0. ~20-30 min CPU ->
   im Hintergrund.
5. **Startvergleich** (billig, empfohlen): zweiter Start = Gewichte des naechsten 2c-Punkts (`_arbeit/baer_junges/eingang/gewichte_2c.npz` +
   `netz_2c.npz`, gleiche Region) -> beide optimieren, den besseren nehmen (schlechtester Clip p99,5 / max / Achsel).
6. **Fuer spaeter vorbereiten:** das Skript nimmt den Dump-Pfad als Parameter; kommt der neue Rear aus Lauf baer-gross, wird der Optimierer mit dem
   neuen Dump noch einmal gerechnet (nur Rear-Bilder zusaetzlich), Netz/Skelett bleiben.

## 5. CLIPS BYTE-GLEICH UND EXPORT (gleiche Rolle; `baer/spiel/baer_export_gengross.py`, Ziel `R/out/`)

- Kopie von `baer_export_junges.py` (nur numpy). **Container** = `plan/eingang/NCBear_2c.glb` (Kopie von NCBearTest, MD5 08ec7806 -- vor dem Lesen
  pruefen). Getauscht werden NUR: POSITION, NORMAL (glatt ueber verschweisste Lagen), TEXCOORD_0 (UV aus der npz, nicht spiegeln), JOINTS_0 (u8),
  WEIGHTS_0, Indizes u16, Mesh-Name `NCBearGen`. **Byte-gleich kopiert:** alle 28 Knoten (Namen, Eltern, rotation/translation/scale), Skin (joints +
  inverseBindMatrices-Accessor), alle 15 Animationen (Sampler input/output-Accessoren, Kanaele). Kein Material, kein Bild (wie 2c).
- Lage-Umrechnung tier -> GLB genau wie der 2c-Export (Probe: Dump-VERTS des neuen GLB -> tier == `E_gen_basis.npz V` +-1e-5 m).
- Clips: nichts neu, keine Ausnahme vorgesehen. **Ausnahme nur mit Beleg** (Bein passt nachweislich nicht): dann je Clip/Knochen/Bild Messwert,
  Grund und Kevins Frage in RIG.md -- erwartet: keine.
- Texturen: `R/form/E_gen_braun.png` -> `R/out/42/media/textures/Body/NCBearGen.png`, `E_gen_foto.png` -> `.../NCBearGenFoto.png`.
- Harness (vor jedem "fertig"):
  `"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump <abs>/R/out/42/media/models_X/Skinned/NCBearGen.glb <abs>/R/rig/dump_gen.txt skin`
  (JB = jdk25 bin, G = Spielordner, H = `_arbeit/baer_spiel/harness`; Lauf ~1 s). Dann **textgleich** vergleichen: Zeilen BONES..BIND und jeder
  CLIP-Block (Zeiten, L-Zeilen, Matrizen) gegen `plan/dump/erw_2c.txt` -- Unterschied nur in ELEMENTS/VERTS erlaubt.
- Video `R/bilder/rig_vorschau.mp4`: Kevins Kamera, Textur braun, 2c | neu nebeneinander: Idle (2 s) -> Walk (3 Schleifen) -> Run (3) -> SitDown ->
  Sit (2 s) -> StandUp -> Rear -> Eat; Bilder aus dem Dump gerendert, kodiert mit `_arbeit/baer_2c/werkzeug/textur/kodieren.py` (Blender-Sequenzer).

---------------------------------------------------------------------------------------------------------------------------------------

## 6. Pruefgroessen und Grenzen (gilt fuer RIG, Pruefer, Nachbesserung, Gegenpruefer)

Werkzeuge kopieren (nie aendern) nach `R/werkzeug/`: `_arbeit/baer_junges/werkzeug/` (clip_pruef, clip_schluessel, glb_datei, kanten, stuetz,
gleiten, dehnung_lib, haushalt), `_arbeit/baer_2c/pruef/gegen/werkzeug/` (g_technik, g_mess, g_dehn2, g_kragen, g_naht, g_sitz2, g_zahn2,
render_pruef), `_arbeit/baer_gen/rig/gegen/werkzeug/` (g_lib, g_durch, g_wirt, g_fakten, g_mess), `plan/mess/` (lib_plan, ton, kontakt_*).

| Nr | Messung | Grenze |
|---|---|---|
| T1 | 26 Knochen Name/Eltern/Reihenfolge, Knoten-Bytes, Skin-Joints, inverseBind-Bytes = NCBear.glb 08ec7806 | exakt |
| T2 | 15 Animationen: Accessor-Bytes gleich; Dump BONES/OFFSET/BIND/CLIP textgleich mit `plan/dump/erw_2c.txt` | exakt |
| T3 | Harness laedt; Dreiecke (ELEMENTS/3) <= 20.000 (Ziel <= 19.850); GLB-Punkte < 65.536; <= 4 Einfluesse; Summe 1 +-1e-4; kein NaN; Gewichte nur an den 21 2c-Knochen | hart |
| T4 | Koerperhaut 0 offene / 0 nicht-mannigfaltige / 0 entartete Kanten; offene Kanten nur an Kleinteilen (Zaehne, Zunge, Krallen) wie 2c; 0 in Ruhe umgekippte Dreiecke; UV-Naht-Paare in allen 874 Bildern 0,000 cm auseinander | hart |
| T5 | 2 Texturen 1024 x 1024 RGB 8 Bit, kein Alpha; Maul-/Krallen-Flecken in beiden gleich; `R/out/md5.txt` gegen Platte | exakt |
| T6 | NCBearTest, NPC Crew, `_arbeit/baer_zaehmen`, `_arbeit/baer_gross`, Originale `baer/spiel/*` (ausser neuen `*_gengross.py`) und `_arbeit/baer_gen/*` unveraendert (MD5 vorher/nachher) | exakt |
| C1 | Stuetzpfoten je Bild (Stuetzbilder wie 2c, `stuetz.py`), Haut ohne Krallen | -1,5..+1,5 cm (Ziel +-1,0) |
| C2 | ganzes Netz je Bild inkl. Krallen | >= -1,5 cm (2c selbst -2,4/-3,0 in Walk/Run: hier NICHT erlaubt) |
| C3 | aufliegende Haut: Sitzflaeche Sit/SitDown-Ende/StandUp-Anfang; Schnauze Eat/Maul (Bilder mit 2c-Kopf < 1 cm) | 0..+1,5 cm bzw. -0,5..+1,5 cm |
| C4 | Dead/Death tiefster Rumpfpunkt | >= -0,5 und <= 2c + 2,0 cm (2c 10,4) |
| C5 | Dehnung je Clip, ALLE Bilder (gueltig wie 2c: Kante >= 7,4 mm, Hoehe >= 2 mm): p99,5 sigma1; max; Achsel/Brust | <= 2,6; <= 4,0; <= 3,5 (berichtet: Hals, Wange bei offenem Maul, Leiste) |
| C6 | Durchdringung (Windungszahl `g_durch`/`g_wirt`): Bein in Bein, Hinterfuss/Unterarm, Zaehne bei Maul zu (Kiefer < 6 Grad: 0 Zahnpunkte aussen, Luft >= 2 mm), Zunge/Gaumen bei 3-14 Grad | <= 2c-Grundlinie (selbst gemessen) bzw. 0 |
| C7 | Kopf in Ruhe: Auge-Nase -30,3 +-2 Grad; Augenmitte +-2 cm; Augen gleich hoch +-0,3 cm; Mitte y +-0,5 cm; Nasenspitze x 1,154 +-0,02 | hart |
| C8 | Kragen (`g_kragen`, Sit 0/30/60/90 aus Kevins Kamera): Koerper hinter dem Kopf ueber Kopf-Oberkante | <= 2c-Wert + 2 cm |
| C9 | Gleiten der Stuetzpfoten je Phase (Walk/Run, Welt = lokal + Weg x 1,6) | <= 2c-Wert + 0,5 cm |
| K1 | Gelenke unter der Haut (Ruhe) | >= 2 cm (Ellbogen/Knie/Hand/Sprung >= 1,5) |
| K2 | Beinachse gegen Knochenrichtung; Sohle in Ruhe; Fussabdruck | <= 4 Grad; z 0 +-0,3 cm; vorn 28,5 +-3 x 20 +-2, hinten 29 +-1 x 19-21 cm |
| K3 | Breite gesamt; Symmetrie (Halbbreiten links/rechts) | <= 0,82 m; <= 1,5 cm |
| K4 | Haushalt je Teil (Koerper, Lippenschnitt, Maul innen, Krallen) | Summe <= 19.850 |
| K5 | Farbe: Kopf/Rumpf aus Kevins Kamera 0,95-1,05; Ring am Hals 0,92-1,08 / Kontrast <= 1,20; Belichtung 1,00 +-0,01 | |

---------------------------------------------------------------------------------------------------------------------------------------

## 7. Beide Farben
Ein GLB, zwei Texturen: **braun** (`E_tex_final`, 23 Grad, Standard der Testhilfe `ncbeargen`) und **Fototon** (`E_tex_fototon`, 358 Grad, Art
`ncbeargenfoto`). Gleiche UV, gleiche Flecken, gleiche Malerei ausser Farbton/Saettigung. Jedes Abnahme-Blatt zeigt braun; die Fototon-Variante je
einmal Ruhe 8 Seiten, Sitzen, Gehen, Spielgroesse (10.2 R8). Kevin waehlt (Fragen).

---------------------------------------------------------------------------------------------------------------------------------------

## 8. Dateien (R = `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross`)
```
R/out/42/media/models_X/Skinned/NCBearGen.glb          Netz + 2c-Skelett + 15 2c-Clips (byte-gleich), Mesh-Name NCBearGen
R/out/42/media/textures/Body/NCBearGen.png             braun, 1024 RGB
R/out/42/media/textures/Body/NCBearGenFoto.png         Fototon, 1024 RGB
R/out/42/media/scripts/NCBearBenchGen.txt              Modell-Eintraege (Testhilfe)
R/out/42/media/lua/shared/NCBearBenchGenDefs.lua       Arten ncbeargen / ncbeargenfoto (Testhilfe)
R/out/42/media/lua/client/NCBearBenchGen.lua           NCBear_GenLive() + Testbefehle (Testhilfe, nur Einzelspieler)
R/out/md5.txt                                          MD5 aller 6 Dateien
```
Kein Translate-Ordner (eine `Translate/EN/IG_UI.json` in `out/` wuerde beim Einbau die der Test-Mod ueberschreiben). Namen geprueft: "ncbeargen",
"NCBearGen", "NCBear_GenLive" kommen in NPC Crew `42/media/lua` und NCBearTest nicht vor (grep -i); `NCBearBenchVergleich.txt` hat Modelle
`NCBearBenchGenE_*` in module NCBear -- kein Konflikt mit `NCBearGen_Body` in module Base, Dateiname verschieden.
**Uebernahme-Naht:** `baer_uebernahme.py` haelt `NCBearBench*` immer zurueck; `NCBearGen.glb/.png` fallen unter `OLD_ASSET` (^NCBear) und werden
als Altlast zurueckgehalten (nicht kopiert, Trockenlauf meldet sie) -- richtig so, bis Kevin E waehlt; dann neuer Name im BanditsNPCBear-Stil beim
Modellwechsel (Lauf b1e nimmt "das jeweils aktuelle grosse Modell").

---------------------------------------------------------------------------------------------------------------------------------------

## 9. Vergleichs-Spawn (Rolle BAU BENCH; Bericht `R/BENCH.md`)

### 9.1 Modell-Skript `NCBearBenchGen.txt` (Form wie NCBearTest `scripts/nc_bear_tier.txt`, Kommentare nur im Block)
```
module Base
{
    animationsMesh NCBearGen { meshFile = Skinned/NCBearGen.glb, keepMeshAnimations = true, }
    model NCBearGen_Body { mesh = Skinned/NCBearGen.glb, shader = animalEffect, static = false, animationsMesh = NCBearGen, }
}
```
`module Base` ist Pflicht (bodyModel ohne Punkt, NCBearTest `nc_bear_cub.txt` Kommentar). Eigenes animationsMesh = in sich geschlossen.
Spaeter umschaltbar auf `animationsMesh = NCBear` (dann kommt ein neuer Rear aus NCBear.glb von selbst; belegt durch die gespielte Zeile
`NCBearStag_Body ... animationsMesh = Deer_Stag` in `nc_bear_tier.txt`) -- nur auf Kevins Wort, nicht in diesem Lauf.

### 9.2 Arten `NCBearBenchGenDefs.lua` (shared)
- `require "NCBearDefs"` ganz oben (Grund: `NCBearBenchGenDefs.lua` laedt alphabetisch VOR `NCBearDefs.lua`; Muster gespielt:
  `NCBearBenchVergleichDefs.lua:8 require "BanditsNPCBearDefs"`; Vanilla-Beleg fuer `require` sucht der Bauer).
- `src = AnimalDefinitions.animals["bear"]`; fehlt sie: eine Zeile ins Log, nichts anlegen. Flache Kopie aller Felder (`for k, v in pairs(src)`, wie
  NCBearBenchVergleichDefs.lua), dann: `bodyModel = "NCBearGen_Body"`; `stages = { [name] = { ageToGrow = 60 } }` (Eintrag gleich dem Artnamen,
  NCBearDefs.lua `stufen[name]`); `breeds = { brown = Kopie von src.breeds.brown mit texture = textureMale = "NCBearGen" bzw. "NCBearGenFoto" }`
  (textureBaby nicht noetig: male = true; sounds-Tabelle darf geteilt bleiben); `minSize = maxSize = 1.0`, `group = "bear"` UNVERAENDERT lassen
  (dann greift die NPC-Crew-Naht `BanditsNPCBearCrew.lua:34 NOT_TENDED["bear"]` -- kein Vieh fuer die Crew).
- `AnimalAvatarDefinition[name] = AnimalAvatarDefinition["bear"]` (sonst wirft das Tier-Info-Fenster, NCBearDefs.lua Kommentar ISAnimalUI.lua:622/:31);
  `AnimalPartsDefinitions.animals[name .. "brown"] = AnimalPartsDefinitions.animals["bearbrown"]` (Zerlegen, ButcheringUtil.lua:18).
- **NCBearFight-Riegel (Beleg):** NCBearFight registriert nur `o:getAnimalType() == "bear"` (`NCBearFight.lua:1787` in `scanBears`), alle Testbefehle
  NCBear_Sit/Eat/AnimTest gehen ueber `F.NearestBear` = nur registrierte Baeren (`NCBearBench.lua:58`). NCBearSize/NCBearSpawn/AttackProbe kennen nur
  bear/bearstag (`NCBearSize.lua:24`, `NCBearSpawn.lua:7`, `NCBearAttackProbe.lua:34`); der Jungen-Code nur `B.CUB` ("ncbearcub"). -> Die neuen Arten
  sind nie Kampfbaer, nie Junges. Gewollt: der Vergleich soll Form und Bewegung zeigen, nicht den Kampf.

### 9.3 Befehle `NCBearBenchGen.lua` (client, nur Einzelspieler: `not isServer() and not isClient()`)
| Befehl | Wirkung | Engine-Aufrufe (Fundstelle) |
|---|---|---|
| `NCBear_GenLive()` | 2c-Baer ("bear"), braun ("ncbeargen"), Fototon ("ncbeargenfoto") lebend in einer Reihe neben dem Spieler (Abstand 3 Kacheln), alle mit Blick SE (zur Kamera) | wie `NCBearBenchVergleich.lua` spawnAt: getAllAnimalsDefinitions/getBreeds (DebugContextMenu.lua:246-275), addAnimal + addToWorld (:1462-1471), getSpecificPlayer(0), getCurrentSquare, getCell():getGridSquare; `setDir(IsoDirections.SE)` (ButcheringUtil.lua:574, NCBearBench.lua:72) |
| `NCBear_GenAct(name)` | spielt einen Clip auf allen Gen-Baeren in 12 Kacheln: sit (= sitdown 1,6 s -> sit -> nach 20 s standup 1,3 s), eat, rear, bite, maul, swipeL, swipeR, slam; Dauer aus F.ACTS (NCBearFight.lua:47-58, nur gelesen) | `getBehavior():setBlockMovement(true/false)` (ISPetAnimal.lua:36/:49), `setVariable("NCBearAct", act)` (ISPetAnimal.lua:43), `clearVariable("NCBearAct")` (ISPetAnimal.lua:48), `stopAllMovementNow()` vor dem Loesen (ISAnimalContextMenu.lua:760, wie NCBearFight setBlock); Takt Events.OnTick (DebugContextMenu.lua:1491) mit getGameTime():getMultiplier() (NCBearFight.lua:1871) |
| `NCBear_GenStay(on)` | Gen-Baeren bleiben stehen (zum Ansehen) / laufen wieder | setBlockMovement wie oben; Sperre laeuft nach ~167 s ab (NCBearFight.lua:148, :468 Kommentar) -> alle 60 s false/true erneuern wie `refreshBlock` |
| `NCBear_GenClean()` | entfernt alle geladenen Gen-Baeren | Liste rueckwaerts (getObjectListForLua, instanceof IsoAnimal), `animal:remove()` (Vanilla ButcheringUtil.lua:609, DebugContextMenu.lua:616; gespielt NCBearSpawn.lua:72) |
Hinweis zu NCBearAct: in NCBearFight gilt "NCBearAct schreibt nur NCBearFight.lua" (anim_spez 6.5) -- das betrifft Baeren, die NCBearFight fuehrt;
die Gen-Arten fuehrt NCBearFight nie (9.2), also kein zweiter Schreiber am selben Tier. Im Bericht so begruenden. Grenzen ehrlich in die Hilfe-Zeilen:
Laerm (Rennen/Schuesse) laesst die Gen-Baeren weglaufen (Engine `respondToSound`, nur der 2c-Baer hat den Laerm-Riegel), Sperre max ~2-3 min.
**Spielstand-Warnung (in die Kopfzeile und den Kevin-Test):** eine gespeicherte Art, die es spaeter nicht mehr gibt, bricht das Laden
(BanditsNPCBearDefs.lua Kopf) -> vor dem Entfernen der Testhilfe `NCBear_GenClean()` und speichern.
Pruefer: `python C:/Users/Kevin/Zomboid/mods/NPCCrew/_docs/tools/luacheck.py`, `scopecheck.py`, `luacheck_pz.py`, `localcount.py`; Lua 5.1, LF, ASCII.

---------------------------------------------------------------------------------------------------------------------------------------

## 10. Abnahme-Bilder (alle aus dem Dump bzw. der Abgabe-npz; Ton UND Textur; gross UND Spielgroesse ~101 px/m bei Groesse 1,0; immer NEBEN dem 2c
in gleicher Kamera; Kevins Kamera = az 0 / el 30 (Baer schaut zur Kamera), Seite = az 90 el 0 und el 30; GPU nur mit `R/gpu.lock`; jedes Bild selbst
ansehen; Fotos nur lokal, nie in ein Blatt fuer Git)

### 10.1 FORM (`R/bilder/form_*.png`)
| Blatt | Inhalt |
|---|---|
| form_1_ton_ueber_2c | Ruhe Ton: Seite, vorn, oben, Kevins Kamera, 45/30, hinten -- E-neu | 2c | uebereinander mit 2c-Skelett (wie `plan_e_gegen_2c_s170.png`) |
| form_2_ruhe8 | Ruhe 8 Seiten (az 0..315, el 30) gross Ton + braun + Fototon, Zeile Spielgroesse, Zeile 2c |
| form_3_kopf | Kopf nah vorn / 3/4 / Seite / oben / hinten, Ton + Textur; Ohren von vorn ueber dem Umriss; Lippenlinie; Hals-Uebergang (Ring) |
| form_4_maul | Kiefer 0/5/24/34/38 Grad, Ton + Textur, nah und Spielgroesse, neben 2c Rear Bild 48 (gleiche Kamera) und `kevin_bruellen_vorlage.webp` (nur lokal) |
| form_5_pfoten | Pfoten Seite (el -10), unten, vorn, Kevins Kamera nah; neben 2c |
| form_6_kontakt | Attrappe: Sit 60 (Kevins Kamera + Seite), Eat tiefstes Bild, Dead, Walk 2/20 -- mit Zahlen 3.8 |
| form_7_foto | E-neu Fotoansicht (az 90 el 10) und Kevins Kamera neben `vorlage_E_gross.jpg` und E_schoen (Fotopose) -- "was ist geblieben" |

### 10.2 RIG (`R/bilder/rig_*.png`, Video `rig_vorschau.mp4`)
| Blatt | Inhalt |
|---|---|
| rig_1_clips_K | alle 15 Clips x 4 Phasen (0/25/50/75 %) aus Kevins Kamera: 2c | E braun, gross + Ton + Spielgroesse |
| rig_2_clips_seite | dasselbe von der Seite (az 90 el 30) |
| rig_3_gang | Walk und Run als Filmstreifen (8 Bilder, Seite el 10) beide Baeren, Pfotenspuren als Linien |
| rig_4_sitzen | Sit 0/30/60/90 aus Kevins Kamera neben `kevin_sitzen_gut_1111.webp` (nur lokal) und dem 2c; Kragen-Zahl |
| rig_5_bruellen | Rear 48 (1,60 s), Bite 13, Maul 13, Eat 15 nah: Zaehne, Zunge, Gaumen; Spielgroesse; neben 2c |
| rig_6_liegen | Death Mitte, Dead aus 6 Seiten |
| rig_7_kampf | SwipeL/R, Slam Schluesselbilder |
| rig_8_fototon | Fototon: Ruhe 8 Seiten, Sitzen, Gehen, Spielgroesse |
| rig_9_dehnung | schlechteste Bilder je Clip mit sigma1-Farbe (Ton) |

### 10.3 Gegenpruefer: `R/bilder/KEVIN_gross_vergleich.png` (2c | E braun | E Fototon; Stehen Kevins Kamera, Seite, Gehen, Sitzen, Aufrichten,
Spielgroesse) ohne fremde Fotos.

### 10.4 Bild-Fragen (Ja/Nein mit Bildpfad; ein Nein ist ein Befund)
1. Ton ohne Textur: von 8 Seiten ein Braunbaer (kein Tisch-Stand, kein Fass, kein langer Giraffenhals)?
2. Kopf gerade, Gesicht aus Kevins Kamera, Hals ohne Falte/Stufe/Einschnuerung, kein Ring?
3. Maul: zu unsichtbar (nur Lippenlinie), offen (Rear/Bite) Zaehne + Zunge wie 2c, keine Loecher an den Mundwinkeln?
4. Pfoten von der Seite rund, Fussabdruck wie 2c, Krallen (falls Geometrie) nie im Boden?
5. Gehen/Rennen: Pfoten stehen, nichts schwebt/steckt, Gang wie 2c?
6. Sitzen wie Kevins Sitz-Bild vom 2c, Hintern auf dem Boden, Kopf nicht in der "Kapuze"?
7. Keine Risse/Beulen an Achsel, Leiste, Hals, Wange in irgendeinem Clip?
8. Neben dem 2c: schoener? (ehrlich, je Pose)

---------------------------------------------------------------------------------------------------------------------------------------

## 11. Wer baut was (Reihenfolge FORM -> RIG -> BENCH; danach Pruefer Optik + Technik, Nachbesserung, Gegenpruefer)

| Rolle | Schreibt | Liest | Gibt ab |
|---|---|---|---|
| **BAU FORM + TEXTUR** | `R/form/`, `R/bilder/form_*`, `R/FORM.md`, `baer/spiel/baer_form_gengross.py`, `baer/spiel/baer_maul_gengross.py`, `R/form/werkzeug/*_gengross.py` | dieser Plan, `plan/mess/*.json`, `_arbeit/baer_gen/{aus,nachbesserung,rig/form}`, `plan/dump/erw_2c.txt` | `R/form/E_gen_basis.npz` (+glb, 2 png, landmarken, pruef_form.json) |
| **BAU SKELETT+GEWICHTE+CLIPS** | `R/rig/`, `R/out/42/media/{models_X,textures}`, `R/bilder/rig_*`, Video, `R/RIG.md`, `baer/spiel/baer_gewichte_gengross.py`, `baer_export_gengross.py`, `R/werkzeug/` | FORM-Abgabe, `plan/eingang/NCBear_2c.glb`, `plan/dump/erw_2c.txt` | `NCBearGen.glb`, `NCBearGen.png`, `NCBearGenFoto.png`, `R/rig/dump_gen.txt`, `gewichte_gen.npz`, Messungen |
| **BAU BENCH** | `R/out/42/media/{scripts,lua}`, `R/BENCH.md`, `R/out/md5.txt` | RIG, NCBearTest (nur lesen), Vanilla | 3 Testhilfe-Dateien + md5 |
Zeitbedarf (Schaetzung aus dem Jungen): FORM 3.3/3.4 je Runde 1-4 min CPU, textur2 ~2,5 min GPU je Farbe, Maul/Krallen/Kontaktprobe Minuten;
Gewichte 20-30 min CPU (Hintergrund); Renders je Blatt 1-3 min GPU. **Prioritaet FORM, falls die Zeit knapp wird:** (1) Form + Kopf + Beine im Ton
richtig, (2) braune Textur, (3) Maul, (4) Fototon, (5) Krallen-Geometrie.
**GPU:** eigene Kopie `R/werkzeug/gpu_lauf.sh` von `_arbeit/baer_gen/werkzeug/gpu_lauf.sh` mit `W=R` (Sperre `R/gpu.lock` per mkdir, wartet auf freie
Sperre UND auf kein fremdes blender.exe -- Lauf baer-gross rendert parallel; danach rmdir). CPU-Laeufe (form2, raw_ruhe, Optimierer) ohne Sperre.
Befehle ueber 2 Minuten im Hintergrund. Nur absolute Pfade an Blender.

---------------------------------------------------------------------------------------------------------------------------------------

## 12. Risiken (in dieser Reihenfolge pruefen)
| # | Risiko | Gegenmittel / Messung |
|---|---|---|
| R1 | Halsverlaengerung ~16 cm wirkt wie ein langer Hals ("Giraffe") oder faltet | Verschiebung ueber das ganze Band Buckel -> Hinterkopf verteilen, Kehle/Brust mitziehen, Winkel-Mischung + Laplace-Band; Seitenriss gegen 2c (Halsdicke >= 2c); Ton nah von 8 Seiten |
| R2 | Vorderbeine 11-13 cm nach aussen + 21 cm nach vorn: Brust/Schulter falten (Lehre f2_t1) | zuerst q verbreitern (Beine wandern relativ weniger), breites Band, Oberarm-Drehung um die Schulter; Schnitte der Brust auf Falten pruefen |
| R3 | Sitzflaeche schwebt (kein Hub!) | dx klein, Heck-Unterseite nach der Kontaktprobe formen (3.8) |
| R4 | Liegen schwebt mehr als 2c | q an Huefte/Schulter (Probe: q 1,2 = 2c-Wert) |
| R5 | Lippenschnitt auf E keine einfache Linie | dc, Region; Rueckfall eigene Lippenkurve (3.6) |
| R6 | Zaehne stehen aus der schmalen E-Schnauze | k_b, Windungszahl-Probe bei Maul zu |
| R7 | Dreiecke ueber 20.000 | Koerperziel nachregeln, Sparfassung Maul 700, Krallen gemalt |
| R8 | Dehnung an Achsel/Wange (2c-Rear lag schon nahe an der Grenze) | Optimierer mit Achsel-/Wangen-Gewicht, Wangenhaut wie 2c |
| R9 | Gesicht hell / Ring am Hals / Pluesch | Textur-Punkte 3.5 mit Zahlen K5 |
| R10 | Geometrie-Krallen im Boden (2c: -2,4/-3,0 cm) | Spitzen heben, sonst gemalt |
| R11 | Lauf baer-gross aendert parallel Rear/Gewichte des 2c | hier die HEUTIGEN Clips; Skelett gleich -> neuer Rear spaeter byte-gleich per Export-Skript (neuer Container) + Optimierer-Nachlauf mit neuem Dump |
| R12 | FORM-Rolle zu gross fuer einen Agenten | Prioritaeten Abschnitt 11; Zwischenstaende mit MD5 sichern, jeder Schritt einzeln wiederholbar |
| R13 | Ungeprueft (Laufzeit): Spielbild im Spiel, Flimmern, MP | "statisch geprueft, nicht gespielt"; Testhilfe nur Einzelspieler |

## 13. Fragen fuer Kevin (in den Bericht des Laufs, nicht waehrend des Laufs fragen)
1. **Kopfhaltung:** Der neue Baer traegt den Kopf jetzt tief wie der 2c-Baer (weil er dessen Skelett und Bewegungen bekommt); im Foto traegt er ihn hoeher.
   So lassen? (Hoeher ginge nur mit eigenen Hals-/Kopfbewegungen = die Bewegungen waeren nicht mehr gleich.)
2. **Breite:** Er ist jetzt so breit wie der 2c-Baer (Schultern ~20 % breiter als das Generator-Modell), sonst haetten die Beine keinen Platz. So lassen?
3. **Farbe:** braun oder Fototon? (beide gebaut)
4. **Kopf:** Generator-Kopf (gebaut) oder doch der 2c-Kopf?
5. **Krallen:** echte Krallen wie beim 2c-Baeren oder nur gemalt?
6. **Aufrichten/Bruellen:** Er hat heute noch das alte Aufrichten (das du beim 2c "scheisse" fandest); das neue aus dem anderen Lauf kann er spaeter 1:1 bekommen.
7. **Liegen:** Tot liegen beide Baeren ~10 cm ueber dem Boden (liegt an der Bewegung, nicht am Modell) -- spaeter fuer beide richten?
8. Wenn E gewinnt: soll er das grosse Modell fuer den Modellwechsel ab Tag 15 werden (Lauf b1e)?

## 14. Dateien dieses Plans (alle unter R)
- `PLAN_GEN.md` (diese Datei)
- `plan/eingang/` Kopien + `md5.txt` (E_schoen 0044f3e5, E_schoen_fototon 0dbe612f, Texturen 06e6bdeb/4f902c5a, NCBear_2c.glb 08ec7806, NCBear_2c.png 4cfdb177)
- `plan/dump/erw_2c.txt` (eigener Dump.java-Lauf, MD5 2875ca08) + `.p.pkl`
- `plan/mess/`: `lib_plan.py` (Dump-/GLB-Leser), `ton.py` (CPU-Rasterer), `mess_e_2c.py` -> `mess_e_2c.json` (Profile, Beinschnitte, 2c-Gelenke),
  `kontakt_2c.py`, `kontakt_2c_b.py` -> `kontakt_2c.json`, `kontakt_2c_teile.json`, `kontakt_zonen.py` -> `kontakt_zonen_2c.json`, `kopf_passung.py` ->
  `kopf_passung.json`, `sitz_probe.py`, `gelenke_blatt.py` -> `gelenke_e_2c.json`, `uv_frei.py`, `blatt_e_2c.py`, `ziel_grob.py` -> `ziel_grob.npz`
- `plan/bilder/`: `plan_e_gegen_2c_s170.png`, `plan_gelenke_e_2c.png`, `plan_ziel_grob.png`, `plan_uv_frei_E_schoen.png`
