# Lauf baer-fell: Gegenpruefer (09.11.2026)

**Statisch/offline geprueft und gerendert, nicht gespielt.** Alle Messungen mit eigenen Werkzeugen an eigenen Dumps des
Spiel-Importers (`_arbeit/baer_spiel/harness/Dump.java`), nicht mit den Zahlen der Nachbesserung. Renders 14:10-14:13 nur auf der
RTX 4090 (OptiX + OptiX-Entrauscher) ueber `werkzeug/gpu_render.sh`; vor jedem Lauf `tasklist`: Spiel lief nicht; Sperre `gpu.lock`
danach frei. Nichts in die Test-Mod, nach NPC Crew oder in Dateien der Bauer/der Nachbesserung geschrieben, nichts committet. Die
Dateien des abgebrochenen Anlaufs in `pruef/` (dump_*.txt, glb_pruef_out.txt, dump/, ref/) nicht benutzt und nicht angefasst.
Eigene Dateien: `pruef/gegen/` (Werkzeuge `werkzeug/`, Ausgaben `log/`, Dumps `dump/`, Bilder `render/`, `blatt/`), dazu dieser
Bericht und `bilder/kevin_vorher_nachher.png`.

## 0. Ergebnis

**Bereit fuer die Test-Mod: ja** (nur alle fuenf Dateien zusammen). Kein Blocker, kein offenes major. Alle festen Regeln halten,
die vier major des Pruefers Optik und das major des Pruefers Technik sind behoben (selbst nachgemessen, Zahlen stimmen mit dem
Bericht der Nachbesserung ueberein). Kevins drei Pflichtpunkte sind im Spielwinkel sichtbar erreicht. Was bleibt, ist Geschmack
(Kevins Blick) und ein paar Kleinigkeiten ohne Wirkung im Spiel (Abschnitt 4).

| Datei (unter `_arbeit/baer_fell/mod/`) | MD5 |
|---|---|
| `42/media/models_X/Skinned/NCBear.glb` | `2a4837f6e8f41d97e07c76b2353b5520` |
| `42/media/models_X/Skinned/NCBearDeer.glb` | `f34cb9dcd5fc5c6f97e9d45255f998b2` |
| `42/media/models_X/WorldItems/NCBear.fbx` | `7e3300fe728a24172792623abf1a2f5c` |
| `42/media/textures/Body/NCBear.png` | `c2d6c8cc2e5858eff6b3d679fc4d5343` |
| `42/media/textures/WorldItems/NCBear.png` | `033d3705b0e1f4ed09c6d6f518a285e5` |

Byte-gleich zu `fix/mod/42/media/` (gleiche MD5). Genau diese fuenf Dateien, keine Lua, kein Skript, kein Test-/Cheat-Inhalt.

## 1. Feste Regeln (eigene Pruefung)

| Regel | Werkzeug / Ausgabe | Ergebnis |
|---|---|---|
| 15 Clips bit-gleich | `werkzeug/regeln.py` (Textbloecke des Dumps je Clip) -> `log/regeln_out.txt`; `werkzeug/glb_datei.py` (Animations-Puffer der Datei byte-weise) -> `log/glb_datei_out.txt` | 15/15 textgleich im Dump, 15/15 x 78 Kanaele byte-gleich in der Datei |
| Knochen, Namen, Eltern, Offset, Bind | Kopfteil des Dumps (81 Zeilen) textgleich; Datei: 28 Knoten TRS/Kinder gleich, inverseBind byte-gleich, joints gleich | ja |
| <= 20.000 Dreiecke nach dem Importer | Dump: **18.930** (alt 18.040) | ja |
| <= 4 Einfluesse, ein Netz/Material | Dump und Datei: max 4, Summe 1,000000, keine negativen; Datei 1 Netz, 1 Primitiv, 0 Materialien, 0 Bilder | ja |
| Kopf bleibt so | `regeln.py` gegen `mess/lowpoly.npz` (gegend 1/2): Kopf 1.333 Punkte, 1.332 Lage+UV+Gewichte/Index bit-gleich, 1 Punkt am Halsrand weicht in x um **1 Float-Stelle (4e-9 Einheiten)** ab, sonst alle 16 Werte gleich; 21 Nahtpunkte nur andere Normale. Alle 1.227 Punkte, die voll am Kopf/Kiefer haengen: alle 16 Werte bit-gleich | ja (besser als im Fix-Bericht: dort "1,6 cm", siehe 4.) |
| Krallen unveraendert | 455/455 alle 16 Werte bit-gleich | ja |
| Kopf/Krallen in Bewegung | `werkzeug/dehnung.py`: 1.787 Paare gehaeutet ueber alle 15 Clips/alle Bilder: **0,0000 mm** | ja |
| Liegehoehe Death/Dead | tiefster Punkt Dead alt/neu 0,0001 m, Death 1,8 cm unter Null wie alt (Clips bit-gleich zu baer-anim) | ja |
| tiefster Punkt je Clip nicht tiefer | 15/15 gleich oder hoeher (SwipeL -8,2 -> -3,6 mm, Rear -1,8 -> -1,2 mm) | ja |
| Kopf-Texel der Vorgabe bit-gleich | `werkzeug/textur.py` (eigener Rasterer, Pixelmitten): Body 1024 Kopf-Inseln 212.593 Texel **0 verschieden**, WorldItems 2048 850.454 Texel 0 (+1 px: 0); bilinear an allen 1.335 Kopf-Ecken max 0,2 Stufen | ja (Hinweis 4.1) |
| Krallenfarbe | bilinear an 455 Krallen-Ecken: Body und 2048 je 0 verschieden | ja (T-m3 behoben) |
| Maul-Flecken frei | Body: drei Flecken samt 4 px Saum 0 verschieden, 0 Rumpf-/Kopf-Insel-Texel darin | ja |
| Dateien/Typen | PNG 8 Bit RGB, Farbtyp 2, ohne Interlace, gleiche Chunks wie alt, Groessen 1024/2048 wie alt; Pfade gleich | ja |
| Deer (Rueckfall "bearstag") | `werkzeug/deer.py`: 40 Knochen, Offset/Bind textgleich zum alten Deer, 18.516 Dreiecke, <= 4 Einfluesse; UV passt zum neuen Netz (10.865/10.909, Rest Rundung), das alte Deer nur 1.790 | ja: **nur mit den anderen vier zusammen** |
| WorldItems-FBX | `Probe.java` (Importer): laedt, 1 Netz, 10.909 Punkte, UV aus dem neuen Layout; keine Nutzer-/Scratchpad-Pfade mehr (alt: zwei) | ja |
| Originale `*_anim.py` | `git diff HEAD -- spiel/` im Repo `baer/`: leer | unveraendert |
| Skripte | alle vier `baer_*_fell.py` parsen; Zeilenenden LF wie die Originale (der Pruefer Technik schrieb "CRLF" - stimmt nicht, war aber nie anders) | ja |

## 2. Kevins Pflichtpunkte

| Punkt | Beleg | Urteil |
|---|---|---|
| 1. Sohlen mit Ballen | `render/neu/sit_gross.png`, `sit_fuss_nah.png` (Spielwinkel, Licht B), `sohle_HL_pur.png`, `sohle_VL_pur.png` (reine Textur von unten), `rear_unten.png`; Blatt `blatt/z3_sit_fuss_nah.png` (alt / geliefert / neu). Alle vier Sohlen: fuenf Zehenballen im Bogen, querliegender Sohlenballen, hinten langer Fersenballen, vorn Handwurzelballen; Haut grau, kein schwarzes Loch mehr; Sohlen-Punkte 964, alle mit Gewicht 1,0 an Hand/Fuss (`log/gewichte_out.txt`) | **erreicht**. Form im Ton weiter ein rundes Roehrenende (Ballen-Relief 8 mm), die Textur traegt die Sohle |
| 2. Unterseite | `render/neu/rear_spiel.png`, `rear_gross.png`, `rear_brust_nah.png`, `rear_unten.png`, `kehle_unten.png`; Blatt `blatt/z3_rear_spiel.png`. Brust/Bauch nicht mehr dunkel verschmiert (Luma Kasten Brust/Bauch im Spielbild alt 39 -> neu 53, `log/kontrast_out.txt`), keine Hautlappen an Achsel/Handgelenk, kein heller Streifen innen an den Hinterbeinen, kein goldenes "V" (die Lieferung hatte es), Vorderpranken grau-braun statt dunkler Klumpen | **erreicht** in der Farbe; Pranken-**Form** (Schaufel) unveraendert -> Kevin |
| 3. Dehnung Achsel/Brust | `werkzeug/dehnung.py` (eigene SVD je Dreieck, Regionen der Forschung) -> `log/dehnung_out.txt` | **erreicht**: siehe 3. |

Ei von vorn (Rear 1,3 s, Breite ohne Armpunkte 1,3-1,5 m zu 0,4-0,8 m, selbst gerechnet): alt 0,924 -> **1,033** (Armgewicht < 0,05:
0,866 -> 1,009), Ziel 0,95. Breitenprofil: Schultern 0,85 -> 0,95 m, Huefte 0,97 -> 0,92 m. Im Ton (`render/*/rear_ton.png`) sichtbar
breiter oben.

## 3. Netz-Ziele (eigene Messung, gleiche Gueltigkeitsregel wie `werkzeug/regionen.py`, ohne Kopf/Krallen/Maul)

| Clip | 99,5 % alt -> neu | max alt -> neu | Achsel / Brust neu |
|---|---|---|---|
| Idle | 1,30 -> 1,18 | 1,66 -> 1,28 | 1,20 / 1,13 |
| Walk / Run | 3,03 / 3,52 -> 1,87 / 2,21 | 5,71 / 10,85 -> 2,07 / 2,49 | <= 2,18 / 1,97 |
| Death / Dead | 3,16 / 3,03 -> 2,02 / 2,00 | 14,0 -> 2,34 / 2,32 | <= 1,86 / 1,77 |
| Rear | 3,60 -> 2,08 | 14,00 -> 2,56 | 2,17 / 1,76 |
| SwipeL / SwipeR | 4,13 / 4,10 -> 2,35 / 2,45 | 9,99 / 8,21 -> 3,02 / 3,12 | 2,76 / 3,02; 2,83 / 3,00 |
| Slam / Bite / Maul | 3,90 / 2,77 / 2,15 -> 2,08 / 1,73 / 1,53 | 6,90 / 5,50 / 5,38 -> 2,55 / 2,39 / 2,21 | <= 2,55 / 1,90 |
| SitDown / Sit / StandUp | 3,07 / 2,95 / 3,16 -> 1,94 / 1,84 / 2,01 | 13,9-14,2 -> 2,91 / 3,16 / 2,91 | <= 1,66 / 1,76 |
| Eat | 1,80 -> 1,52 | 3,35 -> 1,72 | 1,53 / 1,53 |

- Ziele: 99,5 % <= 2,6 (neu hoechstens **2,45**), max <= 4,0 (neu **3,16**), Achsel/Brust in Rear/Sit*/Swipe*/Slam <= 3,5 (neu **3,02**).
  Kevins Werte "Hieb bis 6,9, Aufrichten 4,8": Achsel Hieb jetzt <= 2,83, Aufrichten 2,17.
- Falten liegend (DeerStag_Dead, sigma2 < 0,5): Achsel 165 -> **58**, Ellbogen 75 -> **30** (Summe 88, Ziel <= 120), Knie 0 -> 14;
  sigma2 < 0,3 gesamt 408 -> **121** (Ziel <= 200). Sitzen: Achsel 161 -> 71, Ellbogen 19 -> 23. T-M1 behoben.
- Ausgeschlossene Splitter-Dreiecke (kurze Kante < 7,4 mm, `werkzeug/klein.py`): mit Dehnung > 4 alt 17, neu 15, zusammen ~10 cm2 -
  wie vorher, kein neuer Riss.
- Fremde Gewichte (`werkzeug/gewichte.py`): hinter x -0,05 m kein Unterarm/Hand-Gewicht (alt 2), vorn kein Unterschenkel/Fuss, ein
  Beinpunkt mit Hals/Kopf 0,016. O-m2 behoben.

## 4. Befunde des Gegenpruefers

Blocker: keine. Major: keine.

**Minor / Hinweise**
1. **3 Texel im 1-px-Rand der Kopf-Inseln (Body 1024) geaendert** (x 258/257/749, y 245/246/808; je Kanal hoechstens 14 Stufen). Sie liegen
   im Saum ausserhalb jeder Insel, in der Lieferung waren sie noch gleich. Die eigentlichen Kopf-Texel sind bit-gleich, an den Kopf-Ecken
   bilinear max 0,2 Stufen. Unsichtbar; der Fix-Bericht ("+1 px: 0") zaehlt mit einer anderen Randregel.
2. **Fix-Bericht ungenau beim Kopf-Nahtpunkt:** Der eine "verschobene" Kopfpunkt (alt 9406, neu 8840) liegt nicht 1,6 cm, sondern
   **4e-9 Einheiten** (eine Float-Stelle) anders, alle anderen Werte gleich. Die 1,8/1,6 cm sind der Abstand zum Rumpf aus `kopf.py`.
   Zugunsten der Regel.
3. **Hinterteil/Hinterbeine in Spielgroesse noch etwas koernig und graustichig** (`blatt/z3_hinten_spiel.png`, alt / geliefert / neu):
   deutlich ruhiger als die Lieferung (Kohaerenz Hinterteil 0,48 -> 0,57, alt 0,47; Hinterbein 0,31 -> 0,36, alt 0,38), aber die alten
   langen Haarstriche hatte die Textur glatter. Geschmack, Kevins Blick.
4. **Sohle mittelgrau, im Sitzen deutlich sichtbare graue Flaeche**; um die Zehen ein heller, gezackter Fellkranz (`sohle_HL_pur.png`).
   Gewollt war "dunkelgraue Lederhaut" - im Spiel ist es laut Kalibrierung des Pruefers Optik etwas dunkler als Licht B. Geschmack.
5. **Vorderpranken grau-braun ("Handschuh")** statt rostorange/dunkel - besser als beide Vorstaende, Form unveraendert (Pranke traegt die festen Krallen).
6. Kleine Beule vorn am Oberschenkel bei Slam 0,9 s (`blatt/p_knie_slam_ton.png`), glatt, keine Delle mehr; im Texturbild nicht zu sehen.
7. WorldItems 2048: die drei Fleck-Rechtecke haben eine andere Fuellfarbe als alt - keine UV zeigt dorthin (FBX ohne Maul), ohne Wirkung.
8. FBX nicht byte-gleich nachbaubar (Objekt-IDs je Blender-Lauf), Geometrie gleich - bekannt, harmlos.

**Abgelehnt/offen mit Grund (geprueft, Begruendung haelt):** Zotteln (Geometrie gab Noppen, braucht Kevins Wort), Pranken-Form,
Gesaessfalte nur schwach (im Ton von hinten kaum zu sehen, `blatt/p_hinten_ton.png`), Ballen-Relief 8 mm, Normalen der Unterseite,
Band/Brust 1,45 statt 1,2 (das Band ist im Bild weg; die Brust liegt im Rear im Schatten, das Mass ist dort schief).

## 5. Optik-Befunde der Pruefer: Stand

| Befund | Gegenprobe | Stand |
|---|---|---|
| O-M1 goldenes "V" Leiste | `blatt/z3_rear_spiel.png` (alt / geliefert / neu, Licht B, Spielgroesse): in der Lieferung klar, neu weg, auch in `render/neu/rear_gross.png` und `rear_unten.png`. Die Luma-Zahlen der Nachbesserung (Band 92/87 -> 68/62) habe ich nicht mit ihrem Ausschnitt wiederholt, nur das Bild | behoben |
| O-M2 Ei | 1,033 selbst gerechnet; Ton breiter oben | behoben (Pranken-Form offen -> Kevin) |
| O-M3 Straehnen | Ruecken/Flanke im Sitzen, Spielgroesse: Feinkontrast alt 0,076 / geliefert 0,081 / **neu 0,107**, Kohaerenz 0,63 / 0,59 / **0,68** | behoben |
| O-M4 Sprenkel/Wirbel | Kohaerenz s. 4.3; kein Wirbel im Bild | behoben (Rest Geschmack) |
| T-M1 Falten liegend | 88 (Ziel 120) | behoben |
| O-m1 rostorange, O-m2 Knie-Delle, O-m3 Sohle, O-m4 Flecken, T-m2/3/5/6/7 | Bilder `blatt/p_*.png`, `log/*` | behoben |

Kopf-Variante `textur/NCBear_kopf_variante_body1024.png` (3582a42b) und `NCBear_kopf_variante.png` (c049a6b5) passen zum neuen Rumpf:
Unterschiede nur in Kopf-Inseln + 4 px, 0 in Rumpf-/Krallen-Inseln, Maul-Flecken gleich (`log/kopfvariante_out.txt`). Nicht Teil der
Mod, nur fuer Kevins spaetere Wahl.

## 6. Fuer den Integrator

- **Nur alle fuenf Dateien zusammen** nach `Zomboid/mods/NCBearTest/42/media/...` (gleiche relativen Pfade), vorher und nachher sichern,
  byte-gleich nachzaehlen. Das alte Deer passt nicht zur neuen UV.
- Danach muss Kevin das Spiel **neu starten**.
- Vergleichsblatt fuer Kevin: `_arbeit/baer_fell/bilder/kevin_vorher_nachher.png` (2268 x 1502).

Statisch/offline geprueft und gerendert, nicht gespielt.
