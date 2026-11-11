# Gegenpruefung Optik: C_schoen (Junges) und E_schoen (grosser Baer), 11.11.2026, ~04:45-05:30

Gepruefter Stand: `aus/C_schoen.glb` (04:24) und `aus/E_schoen.glb` (04:35), dazu `aus/E_schoen_fototon.glb`.
Die Dateien habe ich so geladen, wie sie geliefert wurden. Alles habe ich mit eigenen Skripten gerendert und gemessen
(`gegen/skripte/`), keinem Bericht geglaubt und jedes Blatt selbst angesehen. **Statisch geprueft, nicht im Spiel.**
Ablauf: Nur Blender 5.2.3 headless, 4 Laeufe je etwa 21 s, jeder unter `gpu.lock` (`werkzeug/gpu_lauf.sh`); die Sperre ist frei
und kein Blender laeuft mehr. ComfyUI war nicht noetig und wurde nicht gestartet. Das Spiel lief nicht. Kein Download, kein git.

## 1. Urteil kurz
- **E grosser Baer: zeigen, ja.** Kein Blocker mehr. Krater, Hoernchen, Zorro-Band, Fingerabdruck-Boegen und Noppe sind weg,
  im Bild wie im Ton. Von allen 8 Seiten ist es ein sauberer Braunbaer mit Schulterbuckel, dunklen Beinen und rundem Heck.
  Ehrliche Reste: Das Fell wirkt wie weicher Filz bzw. Pluesch und ist flauer als das nasse Fotofell. Das Gesicht ist von vorn
  cremefarben und deutlich heller als der Rumpf. Von der Seite (knapp unter Augenhoehe) sind die Pfoten noch Platten mit Sohlenkante.
  Der Kopf ist 57 Grad zur Seite gedreht (Fotopose).
- **C Junges: so noch NICHT als "schoen von allen Seiten" zeigen.** Der Blocker C-01 ist nur **teilweise** behoben:
  - Bei 45 und 90 Grad sind es jetzt richtige Teddy-Ohren.
  - Bei 0 Grad (auch 1:1 in Spielgroesse) sitzt das nahe Ohr aber weiter als dunkler runder Fleck **im** Kopfumriss
    ("drittes Auge", nur groesser als vorher).
  - Von hinten und von der Seite (180, 225, 270 Grad, schraeg hinten) sind die Ohren **Pilze**: eine runde Kappe auf einem
    schmalen Hals. Schon 1:1 sieht man zwei Knubbel auf dem Kopf.

  Genau so etwas hat Kevin als "komisches Ding auf dem Kopf" verworfen. Alles andere am Jungen ist gut: Gesicht, Fell, Heck,
  Schritt und Sohlen. Eine kurze Ohren-Runde reicht (Abschnitt 6).

## 2. Messung (eigene; `gegen/bilder_C|E/messung.json`, `glb_roh.json`, `farbe.json`)
| | C_schoen | E_schoen | Ziel |
|---|---|---|---|
| Dreiecke (GLB-Accessor roh / Blender verschweisst) | 19.670 / 19.670 | 19.200 / 19.200 | <= 20.000: ok |
| Netze / Primitive / Teile | 1 / 1 / 1 | 1 / 1 / 1 | ok |
| Randkanten (Loecher) / nicht-mannigfaltige Kanten / Ecken | 0 / 0 / 0 | 0 / 0 / 0 | ok |
| Euler / Henkel / Selbstdurchdringung / entartet / Volumen | 2 / 0 / 0 / 0 / +0,171 | 2 / 0 / 0 / 0 / +0,096 | ok (geschlossen, Normalen aussen) |
| Beine: exakte Schnittkurven der Ebene z (3, 5, 8, 10, 15, 20, 25, 30 % Hoehe) | 4 getrennte Kurven von 3 bis 25 %, kleinster Abstand 2,5 cm (bei 8 und 25 %); bei 30 % beginnt der Schritt | 4 Kurven von 3 bis 30 %, kleinster Abstand 2,3 cm (15 %) | vier Beine getrennt: ok |
| Kantenlaenge in Promille der Diagonale: Kopf / Pfoten / Rumpf | 10,2 / 8,3 / 13,0 | 9,1 / 7,8 / 13,0 | Kopf und Pfoten dichter: ok |
| Textur (PNG-Kopf roh aus dem GLB) | 1024x1024, 8 Bit, Farbtyp 2 = RGB, 1 Material, 1 UV; byte-gleich mit `aus/C_schoen_textur.png` | gleich (mit `E_schoen_textur.png`) | ok |
| Belichtung (Licht / flache Textur vor -> nach Eichung) | 1,0025 -> 1,000 | 1,013 -> 1,000 | ok |
| Spielgroesse | 153,8 px je Einheit; 90 Grad = 139 px hoch | 206,1 px je Einheit; 90 Grad = 140 px | ok |

**Farbe gegen Foto** (sRGB-Mittel der Fellpixel; Fotomaske um 7 px eingezogen; Render in der Fotoansicht, geeichtes Licht):

| | Foto | Render mit Licht | Render flach | Spielgroesse 90 Grad |
|---|---|---|---|---|
| C, Ansicht 43/8 Grad | 84/68/59, Farbton 23 Grad, Saettigung 0,30, Helligkeits-Streuung 42 | 79/66/58, 23 Grad, 0,27, Streuung 23 | 82/67/57, 23 Grad, 0,31 | 91/75/65, 24 Grad, 0,28 |
| E braun (Standard), Ansicht 90/10 Grad | 105/91/92, **357 Grad**, 0,13, Streuung 53 | 107/95/88, **23 Grad**, 0,18, Streuung 39 | 108/95/87, 22 Grad | 116/104/95, 23 Grad, 0,18 |
| E Fototon (Variante) | wie oben | 108/95/95, 358 Grad, 0,12 | -- | 117/103/103, 359 Grad, 0,12 |

- **C** liegt in Farbton und Saettigung auf dem Foto, ist etwa 5 % dunkler und hat nur den halben Kontrast (keine Sonnenlichter;
  das ist gewollt und ist Punkt C-12).
- **E braun** hat die Helligkeit des Fotos, ist aber bewusst um ca. 25 Grad zu Braun gedreht. Die Fototon-Variante trifft das Foto
  (rosa-grau). Helligkeitsbaender (oben/Mitte/unten, Kopf/Rumpf/Heck) stimmen bei E bis auf etwa 10 Stufen mit dem Foto ueberein.
  Der Render ist also nicht heller, er ist **flauer**: keine dunklen nassen Straehnen.
- **Hinweis zu C:** In meiner Kamera-Konvention passt die Fotoansicht bei Azimut **43 Grad**, Hoehe 8 Grad (Bild
  `gegen/C_foto_vergleich.png`, Kopf links zur Kamera, Rumpf nach rechts). Mit dem "8/8 Grad" aus C_FEIN sieht man das Junge fast
  frontal. Vermutlich zaehlt dort der Azimut anders. Die Werte oben gelten fuer 43 Grad.

## 3. Jeder Mangel des Pruefers nachgeprueft (Beleg = Bild unter `gegen/`)
### C Junges
| ID | Schwere vorher | Status jetzt | Befund (eigene Renders) | Beleg |
|---|---|---|---|---|
| C-01 Ohren | blocker | **teilweise -> Rest major** | 45 und 90 Grad und Kevins Hauptansicht: Becher mit dunkler Muschel und hellem Saum, das ferne Ohr ragt ueber den Umriss. Vorher waren es flache Scheiben mit kleinem Loch. **Rest 1:** Bei 0 Grad liegt das nahe Ohr weiter ganz im Kopfumriss, als dunkler runder Fleck ueber dem Auge, auch 1:1. **Rest 2:** Von hinten bzw. seitlich (180/225/270, `kopf_hinten_b`) sind die Ohren Pilze mit duennem Hals und runder Kappe; im Ton eindeutig, 1:1 als zwei Knubbel. Ausserdem sind die Ohren kleiner als im Foto | `C_beleg_ohren.png`, `C_pruef_2_kopf.png`, `C_vorher_nachher.png` |
| C-02 Augen/Kopf | major | **behoben** | Braune Iris mit dunklem Rand, leicht dunklere Augenpartie, Kopf im Foto-Ton, Schnauze heller, Nase dunkel. Freundliches Teddygesicht. Kleiner Rest: ein heller **Kratzer** auf der Stirn am rechten Ohr (Textur, nah sichtbar) | `kopf_vorn_beide.png` (oben) |
| C-03 Flecken | major | **behoben** | Gerichtete Straehnen statt Blumenkohl. Nah eine leichte Maserung wie gebuerstetes Holz, in Spielgroesse ruhig | `C_pruef_1_uebersicht.png`, `C_pruef_4_spiel3x.png` |
| C-04 Pfoten/Krallen | major | **behoben (Rest minor)** | Pfoten dunkel, Krallen als lange helle Striche, aus der Spielkamera gut. Von unten-vorn wirkt die Krallenreihe wie ein Kamm oder Gebiss. Von der Seite (-10 Grad) sind die Pfoten flache Pantoffel-Platten | `C_pruef_3_pfoten_heck.png`, `C_zoom_pfoten3.png` |
| C-05 Knoechel | major | **fast behoben (Rest minor)** | In der Textur kein Sockenbund mehr. Im Ton aus der Spielkamera zeigt der rechte Vorderfuss noch eine leichte Stufe, am linken eine kleine Kerbe innen | `C_zoom_pfoten3.png` (unten rechts), `C_vorher_nachher.png` |
| C-06 Kopf-Pose | major | offen (Auftrag) | Kopf 43 Grad zur Seite. Bei 225 und 270 Grad sieht man kein Gesicht, nur Hinterkopf und Ohren | -- |
| C-07 Mosaik Heck | major | **behoben** | Kein Kachelmuster mehr, die Straehnen laufen nach unten | `C_pruef_3_pfoten_heck.png` (Heck) |
| C-08 Ohr-Textur | minor | teilweise | Saum und dunkle Muschel sind da. Innen laufen strahlenfoermige Streifen (Holzmaserung), die Rueckseite ist glatt und heller | `C_pruef_2_kopf.png` |
| C-09 Nacken | minor | teilweise | Weiche Mulde hinter dem Kopf, keine scharfe Kante mehr | `C_pruef_2_kopf.png` (Ton) |
| C-10 Schlitz Schritt | minor | **behoben** | Von unten eine weiche Rinne | `C_vorher_nachher.png` (Bauch unten Ton) |
| C-11 Sohlen | minor | **behoben** | Hauptballen und Zehenballen sind dunkel gemalt | `C_pruef_3_pfoten_heck.png` (Bauch unten) |
| C-12 Farbe | minor | offen (Kevin) | Siehe Abschnitt 2: Farbton und Saettigung wie im Foto, aber flau | -- |
| neu | minor | -- | Stummel im Ton von hinten-unten eine kleine Spitze (in der Textur unsichtbar). Von hinten (180) wirkt das Junge schmal und hoch wie ein Ei auf Beinen (Kopf verdeckt, Pose) | `C_pruef_3_pfoten_heck.png` |

### E grosser Baer
| ID | Schwere vorher | Status jetzt | Befund | Beleg |
|---|---|---|---|---|
| E-01 Krater | blocker | **behoben** | Beide Kopfseiten ohne dunklen Ring. Im Ton keine Delle und keine Kerbe | `E_zoom_seiten.png`, `E_vorher_nachher.png` |
| E-02 Ohren | major | **behoben (Rest minor)** | Dick und rund, keine Hoernchen. Von der Seite eher hoch-oval (Maus- bzw. Loeffelform); von vorn exakte Kreise mit dunkler Scheibe (Mickymaus) | `E_zoom_seiten.png`, `E_pruef_2_kopf.png` |
| E-03 Gesicht | major | **teilweise -> Rest major** | Zorro-Band weg, Augen jetzt sichtbar (braune Iris), Nasenspiegel und Maullinie da. **Neu bzw. Rest:** Stirn und Gesicht sind von vorn bzw. aus der Spielkamera **cremefarben-hell** und deutlich heller als der graubraune Rumpf (helle Maske). Die Straehnen laufen zu einem Mittelscheitel auf der Stirn zusammen. In Kevins Hauptansicht ist das das Auffaelligste | `kopf_vorn_beide.png` (unten), `bilder/KEVIN_gross.png` oben |
| E-04 Farbe | major | **behoben, Wahl bei Kevin** | Braun: 23 Grad bei Fotohelligkeit. Fototon: 358 Grad wie im Foto | Abschnitt 2 |
| E-05 Boegen | major | **behoben (Rest major: Pluesch)** | Keine Jahresringe mehr. Dafuer ist das Fell weich und verwaschen (Filz/Pluesch), der Kontrast ist 39 statt 53. Das Ziel "kein Pluesch-Eindruck" ist bei E nur in Spielgroesse erreicht, gross nicht | `E_pruef_1_uebersicht.png` |
| E-06 Pfoten/Knoechel | major | **teilweise (Rest minor)** | Keine rosa Punkte mehr, horngraue Krallen und Ballen sind da, aus der Spielkamera gut. Von der Seite (-10 Grad) bleibt eine flache Platte mit Sohlenkante, vorn zwei runde Zehenknoepfe | `E_zoom_heck_pfoten.png` (unten), `E_vorher_nachher.png` |
| E-07 Kopf-Pose | major | offen (Auftrag) | 57 Grad zur Seite | -- |
| E-08 Stummel/Spalte | major | **behoben** | Heck im Ton glatt und rund, keine Noppe, keine Furche. Rest minor: dunkle Tarnflecken mitten auf dem Hinterteil (Textur) | `E_vorher_nachher.png` (Heck Ton), `E_pruef_3_pfoten_heck.png` |
| E-09 Nacken | minor | teilweise | Weicher Uebergang. Hinter den Ohren (225/270) dunkle, fleckige Maehnenreste | `E_pruef_2_kopf.png` |
| E-10 Nase/Maul | minor | **behoben** | -- | `kopf_vorn_beide.png` |
| E-11 Brustlatz | minor | nicht gemacht | Die Brust ist von vorn-unten dunkel und fellig, ohne glatte Flaeche. Ein heller Latz wie in `ref_aufrecht_vorn` fehlt | Blatt, Reihe "Aufrichten" |
| neu (Optik) | minor | -- | Von hinten (180/30 Grad) haengen im Schritt zwei dunkle runde "Kugeln" (Hoden-Eindruck). **Nachgewiesen:** Das sind die eng stehenden Vorderbeine, die man durch die Luecke zwischen den Hinterbeinen sieht; mit weggeschnittener Vorderhaelfte verschwinden sie. Kein Netzfehler, das aendert sich mit der Bewegung | `E_probe_schritt.png` |

## 4. Blaetter
| Blatt | Inhalt |
|---|---|
| **`bilder/KEVIN_junges.png`**, **`bilder/KEVIN_gross.png`** (2400 px breit) | Oben links das Foto, daneben gross die Ansicht aus Kevins Spielkamera (45 Grad, 30 Grad Hoehe). Darunter 8 Seiten in Spielgroesse 1:1 auf Grau und auf Gras (90 Grad = 140 px), 8 Seiten gross mit Textur, 8 Seiten als Ton und die Reihe "wie beim Aufrichten" (vorn-unten und Gesicht-unten auf Bauchhoehe -20 Grad, hinten 0 Grad, hinten-unten -20 Grad) neben `ref_aufrecht_vorn`, `ref_hinten_felsen` und `ref_hinten_grizzly`. Alles orthografisch, neutrales Licht, geeicht, nichts aufgehellt |
| `gegen/C_pruef_1..4_*.png`, `gegen/E_pruef_1..4_*.png` | 1: Uebersicht (Spielgroesse auf Grau, Gras und Erde). 2: Kopf aus der Spielkamera rundum (8 Seiten) und nah, je Textur und Ton. 3: Pfoten und Heck. 4: Spielgroesse 3x pixelgetreu |
| `gegen/*_vorher_nachher.png` | Gleiche Blickwinkel wie beim Optik-Pruefer, vorher (dessen Renders) und nachher (meine) |
| `gegen/C_beleg_ohren.png`, `E_zoom_seiten.png`, `E_zoom_heck_pfoten.png`, `E_probe_schritt.png`, `kopf_vorn_beide.png`, `C_zoom_pfoten3.png`, `foto_vergleich.png` (E: Foto, braun, Fototon), `C_foto_vergleich.png`, `texturen_beide.png` | Belege zu Abschnitt 3 |
| `gegen/bilder_C|E|Ef/` | Einzelbilder (transparent) + `messung.json`, `farbe.json`, `glb_roh.json`; `Ef` = Fototon-Variante |

Wiederholen (unter `_arbeit/baer_gen`):
```
B=/c/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe; W=$PWD
python gegen/skripte/glb_roh.py aus/C_schoen.glb gegen/bilder_C aus/C_schoen_textur.png
sh werkzeug/gpu_lauf.sh gegen/log/r.log $B --background --factory-startup --python $W/gegen/skripte/gegen_render.py -- $W/aus/C_schoen.glb $W/gegen/bilder_C $W/gegen/cfg_C.json
python gegen/skripte/gegen_blatt.py C ; python gegen/skripte/vorher_nachher.py C      (E genauso mit cfg_E.json)
```

## 5. Werkzeug-Lehre (fuer alle Render-Skripte)
Nach dem Setzen von `kam.rotation_euler` ist `kam.matrix_world` erst nach `bpy.context.view_layer.update()` aktuell. Mein erster
Lauf hat ohne das die Achsen der *vorigen* Kamera genommen: Bildmitte und Groesse waren falsch, Ansichten 135/180/225 waren
angeschnitten. Behoben und alles neu gerendert. `optik_pruefung/skripte/optik_render.py` hat denselben Aufbau (`proj_hoehe`). Seine
140 px bei 90 Grad stimmen zufaellig (die Kamera davor stand auch auf 90/30); die Bildgroesse der anderen Ansichten kann dort aber
leicht falsch sein. Die Mitte bestimme ich jetzt je Ansicht aus dem projizierten Netz (`bildmitte`).

## 6. Naechster Schritt (Empfehlung)
1. **Kurze Formrunde vor den Knochen, nicht schon Knochen und Clips.** Der Kopf muss fuer die Knochen ohnehin gerade gedreht
   werden (C-06/E-07). Dabei pruefen, dass die 0-Grad-Ansicht danach ein Gesicht zeigt.
   - C-Ohren: Basis breiter, kein Hals (keine Pilzform von hinten), etwas groesser wie im Foto. Bei geradem Kopf ragen beide
     Ohren von vorn ueber den Umriss; das loest Rest 1 von C-01 vermutlich von selbst, ungeprueft.
   - E-Gesicht: Stirn und Gesicht auf Rumpfton abdunkeln, den Mittelscheitel aufloesen.
   - Pfoten bei beiden: Sohlenkante bzw. Pantoffel-Platte von der Seite abrunden, Zehen weniger knopfig.
   - C: den Stirn-Kratzer entfernen.
2. Danach Kevin beide Blaetter zeigen. E kann er schon jetzt sehen (Farbwahl braun oder Fototon).
3. Dann Knochen, Gewichte und Clips. Beim Aufrichten auf Brust bzw. Bauch achten (bei E-11 eventuell einen hellen Latz).
4. Offen und nicht behebbar ohne Geometrie: E wirkt plueschig statt nass-straehnig. Ein zotteliger Umriss geht nur ueber Geometrie,
   Alpha fuer Tiere hat das Spiel nicht.
