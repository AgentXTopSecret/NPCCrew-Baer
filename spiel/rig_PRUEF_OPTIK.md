# PRUEF_OPTIK -- Lauf baer-rig-junges, Rolle PRUEFER OPTIK (11.11.2026, ~11:50-12:40)

**Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und nichts am Modell geaendert. Geschrieben nur unter
`rig/pruef_optik/` und diese Datei. Kein git, kein Download, nichts in Test-Mods, NPC Crew, Spiel oder `_arbeit/baer_zaehmen/mod/`.
GPU nur ueber `_arbeit/baer_gen/werkzeug/gpu_lauf.sh` (Sperre `gpu.lock`, 3 Laeufe, je unter 3 min, Sperre wieder frei).

Gepruefter Stand: `rig/out/42/media/models_X/Skinned/NCBearCub.glb` MD5 **d89856ef508a0100dbb4e384f0ab4640** und
`rig/out/42/media/textures/Body/NCBearCub.png` MD5 **8ce68838b0df138b7bf667b98d687800** (= `rig/out/md5.txt`, selbst nachgerechnet).
Vergleich: alter Platzhalter NCBearTest `NCBearCub.glb` 6c3f0a96... / `NCBearCub.png` 2ee25f24... (nur gelesen, Kopie in `pruef_optik/dump/`).

## 0. Urteil kurz
**Das neue Junge ist besser als der Platzhalter -- Ersetzen: ja**, mit zwei grossen Restpunkten, die Kevin sehen wird:
1. **Fressen (Eat)** sieht nicht nach Fressen aus: Kopf vor die Brust geklappt, Schnauze 15 cm (im Spiel) ueber dem Boden; aus Kevins
   Kamera ein Ei ohne Gesicht. Der Clip laeuft beim Fuettern des Jungen (`BanditsNPCBearFeedAction.lua:60`). Der Platzhalter frisst am Boden.
2. **Kevins Hauptkamera (az 0 / el 30)**: das Gesicht sitzt klein unten am Umriss, die Ohren liegen als zwei dunkle runde Scheiben
   **innerhalb** des Kopf-/Rueckenumrisses ("drittes Auge", schon in GEGEN_OPTIK C-01 Rest 1) -- auch 1:1 sichtbar.

Klar besser als der Platzhalter: Form wie das Foto (kompakt, rund, grosse runde Ohren, kurze Schnauze; der Platzhalter wirkt wie ein
langer flacher erwachsener Baer), Gesicht nah (freundliches Teddygesicht statt Grinse-Zahnstrich), **Sitzen fast wie Kevins Vorlage**,
alle Pfoten stehen auf dem Boden (Platzhalter: Vorderpfoten schweben in Idle 4 cm, sinken im Gang bis -3 cm), **Gehen ohne Gleiten bei
0,35 und 3x so schnell**, keine Risse in irgendeinem Clip in Spielgroesse, ruhigere Textur ohne Mipmaps.

## 1. Wie geprueft (unabhaengig vom Bauer)
- **Eigener Harness-Lauf:** `Dump.java` (unveraendert) auf das fertige GLB und auf den Platzhalter -> `pruef_optik/dump/neu.txt`, `alt.txt`
  ("OK ... Knochen 26 Clips [15 Namen]" fuer beide). Eigener Leser `werkzeug/lese_dump.py` (nicht `dumpread.py`).
- **Eigene Haeutung wie die Engine:** v' = Summe w * M * OFF * v aus den Importer-Matrizen (Konvention geprueft: Idle 0 gegen Ruhe 0,0036 E
  Abweichung, die drei anderen Varianten 0,011-0,012; inverse OFF-Beckenlage = Idle-Becken; `log/konvention.txt`). Normalen = gehaeutete
  Dump-Normalen, Netz/UV genau aus dem Dump. UV-Richtung am Platzhalter geeicht (der ist gespielt): `render/test/uvtest.png`.
- **Eigener Renderer** `werkzeug/render_pruef.py` (Cycles OPTIX, orthografisch, Boden), Kamera az 0 = von vorn, az 90 = von links.
  Spielgroesse = 577 px/E bei 0,35 = 109,9 px je Meter (bei 1,0 gebaut). 1.058 Bilder (`render/r`, `render/r2`, `render/flach`).
- **Eigene Messungen:** Boden je Pfote und Bild, Kopf tiefster Punkt, Gleiten der aufliegenden Sohlpunkte in Welt (`werkzeug/posen.py`,
  `gleiten2.py`), umgeklappte Dreiecke (`falten.py`), Korn ohne Mipmaps (`render_flach.py`).
- **Selbst angesehen:** jedes Blatt unten, dazu Einzelbilder (Gang, Nacken). Rahmen tier (x vorn, y links, z oben), cm bei Groesse 1,0,
  "im Spiel" = x 0,35.

## 2. Blaetter (alle `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/pruef_optik/blaetter/`)
| Blatt | Inhalt |
|---|---|
| `P0_urteil.png` | auf einen Blick: Foto, neu 43/8, neu/alt Kevins Kamera (3x), Spielgroesse 1:1 neu/alt 4 Seiten, Sitzen neben Vorlage, Eat, Walk |
| `P1_ruhe_8seiten.png` | Ruhe (Idle01 Bild 0) 8 Seiten el 30: Spielgroesse, gross Textur, gross Ton -- neu und alt; Foto, Foto-Ansicht 43/8 |
| `P2_clips_kevin_1..3.png` | alle 15 Clips je 4 Phasen (0/25/50/75 %) aus Kevins Kamera az 0/el 30: neu gross, neu 1:1, alt 1:1 |
| `P3_clips_seite45_1..3.png` | alle 15 Clips je 4 Phasen: Ton von der Seite az 90/el 8 mit Boden, Textur az 45/el 30, alt Ton |
| `P4_gang_walk.png`, `P4_gang_run.png` | Walk 27 / Run 16 Bilder: Seite az 90/el 6 und az 45/el 30, neu und alt |
| `P5_sitzen.png` | Kevins Sitzvorlage neben Sit 0 / 60 von vorn (az 0/el 3), Ton, -30/+30/Kevin/Seite/hinten; alt Sit 0 |
| `P6_kopf.png`, `P6b_kopf_ganz.png` | Kopf nah (0/10, 0/30, 35-45, 90, 135, 180, 225/270, von oben) Textur und Ton, neu und alt |
| `P7_pfoten_heck.png` | Pfoten vorn/hinten/Seite, Hinterteil 4 Ansichten, Textur und Ton, neu und alt |
| `P8_r6_dehnung.png` | Eat tiefster Kopf, Death 38, Dead, Rear hoechster Kopf (neu/alt); je Clip das Bild mit der staerksten Kantendehnung (Ton) |
| `P9_kevin_3x.png` | Kevins Kamera 3x Spielgroesse: Ruhe, Walk 13, Eat 21, Sit 0 (az 0 und 45), neu und alt |
| `P10_kehle.png`, `P11_achsel.png`, `P12_leiste.png`, `P13_sitz_liegen.png` | Nahaufnahmen der heiklen Zonen (Ton + Textur) |
| `P14_ohne_mipmaps.png`, `P15_spiel_pixel.png` | Textur 1 Abtastung je Pixel (wie ohne Mipmaps) gegen 64; Spielgroesse pixelgetreu 3x |

## 3. Urteil je Clip (neu; Belege P2/P3/P4/P8/P10-P13; Boden = tiefste Pfotenhaut ohne Abzug der Krallen, cm bei 1,0)
| Clip | Boden / Schweben | Risse, Beulen, Falten | Gangbild / Wirkung | Urteil |
|---|---|---|---|---|
| Idle01 | alle 4 Pfoten -0,2..+0,2 (alt: vorn +4,0 schwebend) | keine | ruhig, Kopf leicht gesenkt wie im Foto | gut; Ohren/Gesicht von vorn s. M2 |
| Walk (Trab) | Stuetzpfoten 0,0; Netz bis 2,85 hoch = Flugphase (gewollt) | keine sichtbar; Ton nah: Leiste glatt | flinker Trab, weite Schritte, liest sich als laufendes Junges; Kopf und Rumpf ganz starr (m5) | gut; Aufsetz-Rutscher m1 |
| Run (Galopp) | Stuetzpfoten 0,0; Flugphase bis 3,75 | Ton nah Bild 5: scharfe Querfalte hinten unter dem Hintern (480 px/m, 1:1 unsichtbar) | Galopp mit gestrecktem/gesammeltem Bein, Rumpf und Kopf starr ("Schaukelpferd") | ok; m1, m5 |
| Death | -0,5..+0,35, kein Schweben | keine in Spielgroesse | kippt auf die Seite, Beine gestreckt | gut |
| Dead | liegt, Netz -0,5 (Krallen) | Beine liegen uebereinander (wie CLIPS.md) | liest sich als totes Tier | gut |
| Rear | Hinterpfoten -0,3..+0,3 | Ton nah: kleine dunkle Flecken an Unterarm/Schulter (umgeklappte Dreiecke, 1:1 unsichtbar) | steht auf, Arme vor der Brust, Gesicht sichtbar -- huebsch | gut (Kampf-Clip, beim Jungen heute nicht genutzt, ungeprueft) |
| SwipeL / SwipeR | Stuetzpfoten -0,5..+1,0 | Ton nah: dunkle Strichlein am Unterarm (wie Rear) | Arm schwingt seitlich, ok | ok |
| Slam | -0,5..0,0 | wie Rear | duckt vorn, ok | ok |
| Bite | -0,5..+0,5 | Ton nah: Kehlfalte quer unter dem Kinn | Kopf hebt, ok | ok |
| Maul | -0,5..+1,0 | Kopf an die Brust geklappt (Kehle, Ton 30/-20: dunkler Keil an Brust/Oberarm) | wirkt wie Ducken, nicht wie Zubeissen | m2 (beim Jungen heute nicht genutzt, ungeprueft) |
| **Eat** | Pfoten ok; **Kopf tiefster Punkt 42,3..54,5 cm** (alt 0,2 cm) | Kehle gestaucht, Schnauze liegt vor der Brust | **aus Kevins Kamera ein gesichtsloses Ei mit zwei Ohrscheiben**; kein Fressen am Boden | **M1** |
| SitDown | 0,0..+0,3 | Ton nah Bild 22: kurzer dunkler Riss-Strich an der Leiste (480 px/m; 1:1 unsichtbar) | setzt sich glatt hin | gut |
| Sit | Sitzflaeche 0,0, Pranken 0,0, Fersen 0,1 | Unterarm liegt am Unterschenkel an (kein sichtbarer Durchstoss, Ton von vorn sauber) | **fast wie Kevins Vorlage**: aufrecht, Kopf oben, Pranken zwischen den Hinterbeinen, Sohlen nach vorn | sehr gut; Sohlen m6 |
| StandUp | 0,0..+0,26 | Ton nah Bild 13: Laengsfalte vorn am Oberschenkel | steht glatt auf | gut |

## 4. Urteil je Koerperteil
| Teil | Befund | Beleg |
|---|---|---|
| Kopf/Gesicht | nah ein freundliches Teddygesicht (braune Iris, schwarze Nase, helle Schnauze); Kopf gerade; Kopfgroesse zum Rumpf wie im Foto (Kopf ~46 % der Schulterhoehe in der Foto-Ansicht 43/8). Aus el 30 von vorn klein und unten | P6b, P1, P9 |
| Ohren | von der Seite und schraeg runde dicke Teddyohren, von hinten **keine Pilze mehr** (C-01 Rest 2 behoben). **Von vorn aus el 30 zwei dunkle Scheiben im Umriss** (M2); von oben (el 70) wie eingerollte Schneckenhaeuser | P6b 0/30, 0/70; P9; P15 |
| Nacken | Ton 135/20 eine Kerbe hinter dem rechten Ohr, Ton 180/20 senkrechte Spiegelnaht (Lichtsprung) im Nacken; in der Textur kaum zu sehen | P6b, `render/vorschau_nacken.png` |
| Rumpf | rund, kompakt, Ruecken hell (sonnig) wie im Foto, Beine dunkel; von hinten (az 180) "Ei auf Stelzen" (m3) | P1, P7 |
| Pfoten | stehen alle; vorn runde Saeulen-Stumpen ohne Zehenform, Krallen nur kleine gemalte Striche; im Sitzen sind die Hinterfuss-Sohlen gleichmaessig schwarze Ovale (m6) | P7, P13 |
| Schwanz | Stummel, im Ton ein kleiner Knubbel, in der Textur unsichtbar -- passt zum Jungen | P7 |
| Fell/Farbe | grau-braun, wenig Kontrast, weich/filzig; Foto ist waermer mit goldenen Lichtern (GEGEN C-12, Kevins Wahl); Platzhalter waermer/roter | P0, P1 |
| Textur ohne Mipmaps | Abweichung 1 Abtastung gegen 64 im Mittel 5-6 Stufen (alt 5,5-7) bei 0,35, 2,5-3,2 (alt 2,9-3,7) bei 0,75 -> eher weniger Flimmern als heute (Laufzeit ungeprueft) | P14 |

## 5. Eigene Messungen (Zahlen)
**Boden** (`pruef_optik/neu_mess.json`, `alt_mess.json`): neu Netz-Minimum in allen Clips >= -0,50 cm (Krallen), kein Clip schwebt ausser den
Flugphasen Walk (bis 2,85) / Run (bis 3,75). Alt: Walk bis -2,86, Run bis -3,31 (steckt im Boden), Idle Vorderpfoten +4,0 (schwebt).

**Tempo aus dem eigenen Dump:** Walk |TD| 0,9016 E -> **1,603 Kacheln/s**, Run 0,8711 E -> **2,613** (alt 0,523 / 2,465); Formel
Weg x 1,6 / Dauer laut RIG_PLAN 5.3 (Jar-Beleg dort, von mir nicht nachgelesen).

**Gleiten der aufliegenden Sohlpunkte** (Welt = Pfote x 1,5 x s + Weg x 1,6; `log/gleiten2_*.log`, Spur fester Sohlpunkte oben):
| | s = 0,35 | s = 0,50 | s = 0,75 |
|---|---|---|---|
| neu Walk, Stuetzbilder | **0,00 cm** je Bild | 5,6 cm je Bild (im Spiel 2,8) | 10,0 cm je Bild (im Spiel 7,5) |
| neu Walk, Aufsetzbild | HR 6,9 / VL 9,9 / VR 2,0 cm (im Spiel 2,4 / 3,5 / 0,7) | | |
| neu Run, Aufsetz-/Stuetzbild | VL 8,6 / VR 3,6 cm (im Spiel 3,0 / 1,3); HL 0,0 | 0,9-9,2 cm | 7,7-16,3 cm |
| alt Walk | typisch 3,4-4,1 cm je Bild, bis 11 am Stuetzende (Hinterpfoten gleiten durchgehend) | typisch 1,6-2,3 | typisch 0,2-0,9 |
`CLIPS.md` meldet "Gleiten 0,0 cm" -- das gilt fuer den Abrollpunkt in der Stuetze; im **Aufsetzbild** rutscht die Sohle noch ein Bild
lang vor (m1). Ab Groesse 0,5 (B1d zeigt das Junge bis 0,75) laeuft das "Laufband" (M3, wie CLIPS.md 8.1.1).

**Umgeklappte Dreiecke** (Flaechennormale gegen gehaeutete Punktnormalen, grobe Naeherung; `render/falten_*.json`): neu max je Clip
15 (Idle) .. 706 (Death), alt 14 .. 769; neu in 10 von 15 Clips weniger als alt (mehr: Idle, Dead, Rear, Eat, Sit). Sichtbar nur nah als dunkle Strichlein (P11), 1:1 nicht.

**Kopf tiefster Punkt Eat:** neu 42,3 cm (im Spiel 14,8), alt 0,2 cm.

## 6. Maengel (hart; Schwere fuer das Ersetzen des Platzhalters)
| ID | Schwere | Wo | Befund | Vorschlag |
|---|---|---|---|---|
| M1 | major | Eat (alle Bilder; Fuettern) | Kopf vor die Brust geklappt, Schnauze 42 cm (bei 1,0) ueber dem Boden; aus Kevins Kamera Ei ohne Gesicht (P2_3 Zeile Eat, P9 Eat_021, P10) | eigener Fress-Clip des Jungen (Vorderbeine einknicken bzw. hinlegen, Kopf am Boden) -- ausserhalb D.5, Kevins Wort (CLIPS.md 8.2.1); bis dahin Eat des Platzhalters nicht besser zu haben |
| M2 | major | Kevins Kamera az 0/el 30 in Idle/Walk/Run | Ohren als zwei dunkle Scheiben im Umriss ("drittes Auge"), Gesicht klein unten; 1:1 sichtbar (P15 az 0, P9) | Ohrmuschel heller/kontraermer malen und die Oeffnung etwas nach aussen-hinten drehen, oder Kopf in Idle/Walk ~10 Grad hoeher tragen (D.5-Ausnahme, Kevin) |
| M3 | major (Laufzeit, andere Sitzung) | Walk/Run bei Groesse > 0,35 | Stuetzpfote gleitet bei 0,5 2,8 cm, bei 0,75 7,5 cm je Bild im Spiel (Laufband) | Kevin entscheiden lassen: Junges bei 0,35 halten bis Clips je Groesse, oder Abspieltempo je Groesse (ungeprueft, ob die Engine das bei Tieren kann) |
| m1 | minor | Walk Aufsetzbild (HR 4->5, VL 4->5), Run (VL 3->4) | Sohle rutscht 1 Bild lang 2-10 cm (bei 1,0) vor; CLIPS.md "0,0 cm" misst nur den Abrollpunkt | Aufsetzen ein Bild frueher bremsen (Pfote im letzten Schwungbild schon mit Bodentempo) |
| m2 | minor | Maul (Bilder 12-36) | Kopf an die Brust geklappt, wirkt wie Ducken; dunkler Keil an Kehle/Oberarm im Ton | nur falls das Junge je Maul spielt; sonst so lassen |
| m3 | minor | Ruhe/Gang von hinten (az 180) | schmal und hoch, runder Hintern auf duennen dunklen Beinen ("Ei auf Stelzen"), wie GEGEN_OPTIK | Oberschenkel hinten etwas voller (Form), Kevins Wort |
| m4 | minor | Ton nah (>= 4x Spielgroesse) | Kerbe hinter dem rechten Ohr, Spiegelnaht im Nacken, dunkle Strichlein (umgeklappte Dreiecke) an Unterarmen in Swipe/Rear/Slam/Bite, Querfalte unter dem Hintern Run 5, Riss-Strich Leiste SitDown 22 | 1:1 unsichtbar; bei einer naechsten Formrunde Nackenkerbe glaetten |
| m5 | minor | Walk/Run | Kopf und Rumpf vollkommen starr (kein Nicken, keine Wirbelsaeule); Galopp wirkt wie Schaukelpferd | im Spiel ansehen (3,3/3,75 Hz); evtl. leichtes Kopfnicken |
| m6 | minor | Pfoten | Vorderpfoten Saeulen ohne Zehen, Krallen winzig gemalt; Hinterfuss-Sohlen im Sitzen gleichmaessig schwarze Ovale ohne Ballen | Sohlenballen in der Textur heller/gegliedert malen |
| m7 | minor | Fellfarbe | flau grau-braun, keine goldenen Lichter des Fotos (C-12) | Kevins Wahl |

## 7. Fragen fuer Kevin
1. **Fressen:** eigener Fress-Clip fuer das Junge (Vorderbeine einknicken oder hinlegen, Schnauze am Boden)? Heute sieht Fuettern beim
   neuen Jungen wie "Kopf an die Brust" aus.
2. **Von vorn aus deiner Kamera** sieht man beim neuen Jungen die Ohren als dunkle Scheiben auf dem Kopf. Ohren heller malen / etwas
   drehen, oder den Kopf beim Stehen und Gehen hoeher tragen?
3. **Wachsen:** Soll das Junge bei 0,35 bleiben, bis es Gang-Clips je Groesse gibt? Ab 0,5 rutschen die Pfoten sichtbar.
4. Farbe: so lassen (Foto-Ton, aber flau) oder waermer wie der alte Platzhalter?

## 8. Dateien (alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/pruef_optik/`)
- `dump/neu.txt`, `dump/alt.txt` (+ `.npz`) -- eigener Harness-Lauf; `dump/platzhalter_NCBearCub.*` -- Kopie des Platzhalters
- `werkzeug/lese_dump.py`, `lib_pruef.py`, `posen.py`, `gleiten2.py`, `falten.py`, `auftrag.py`, `auftrag2.py`, `render_pruef.py`,
  `render_flach.py`, `blaetter.py`, `blaetter2.py`
- `neu_mess.json`, `alt_mess.json`, `render/falten_*.json`, `render/wahl.json`, `log/*.log` (Konvention, Gleiten, Falten, Render)
- `render/r/`, `render/r2/`, `render/flach/` -- Einzelbilder; `blaetter/P0..P15*.png` -- Blaetter

Wiederholen (Bash, R = `.../rig/pruef_optik`):
```
java -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump <GLB> $R/dump/neu.txt skin
python $R/werkzeug/lese_dump.py $R/dump/neu.txt $R/dump/neu.npz ; python $R/werkzeug/posen.py $R/dump/neu.npz $R/neu
python $R/werkzeug/auftrag.py ; sh .../baer_gen/werkzeug/gpu_lauf.sh LOG blender -b --factory-startup --python $R/werkzeug/render_pruef.py -- $R/render/cfg.json
python $R/werkzeug/auftrag2.py ; (gpu_lauf wie oben mit cfg2.json; render_flach.py mit cfg_flach.json) ; python $R/werkzeug/blaetter2.py
python $R/werkzeug/gleiten2.py $R/dump/neu.npz 0.5 ; python $R/werkzeug/falten.py neu
```
