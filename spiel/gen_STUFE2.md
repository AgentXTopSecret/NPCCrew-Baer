# Stufe 2 Bild-zu-3D (TRELLIS.2, ComfyUI) -- Varianten + Spielnetz-Vorschau -- 10.11.2026, ~21:30-22:50

Kurz: 18 neue Versuche (je Bild 9), gewaehlt **A_s2** und **E_c2_form**. Daraus je ein Spielnetz (< 20.000 Dreiecke, 1 Teil,
0 Loecher, 1024er-Textur). Die Stacheln sind im Spielnetz weg, die Farbe ist im Render auf das Foto geeicht. **Urteil: in
Spielgroesse lesbar als Braunbaer (E) bzw. Baerenjunges (A), aber NICHT "von allen Seiten schoen"** -- Einzelheiten unten.
Statisch geprueft, nicht im Spiel. Spiel lief nicht, kein Download, ComfyUI am Ende beendet (PID 28892).

## 1. Blaetter und Ergebnisse
| Was | Pfad (unter `_arbeit/baer_gen/`) |
|---|---|
| Vergleich Varianten | `bilder/A_varianten.png`, `bilder/E_varianten.png` (Zeile je Versuch: 4x Textur, 4x Ton; 0/90/180/270 Grad) |
| Spielnetz-Blaetter | `bilder/A_spielnetz.png`, `bilder/E_spielnetz.png` |
| Spielnetze | `aus/A_spielnetz.glb`, `aus/E_spielnetz.glb` (Textur eingebettet) + `aus/*_spielnetz_textur.png` (1024 RGB), `*_textur_roh.png` (nur gebacken, ohne Nacharbeit), `*_messung.json`, `*_arbeit.blend` |
| alle Varianten-GLB | `aus/varianten/*.glb` (+ `_lauf.json`, `_basecolor_*.png`) |
| Einzelbilder | `bilder/varianten_einzel/`, `bilder/einzel_A_spielnetz/`, `bilder/einzel_E_spielnetz/` (auch `regionen_*.png`, `foto_ansicht_*.png`, `maske_*.png`) |
| Logs | `log/var_out2.log` (Erzeugung), `log/vier_*.log`, `log/spielnetz_A.log`, `log/spielnetz_E.log` |

## 2. Welcher Seed steuert was (Knoten im Ablauf `baer/tools/trellis2_ablauf_api.json`)
| Knoten | Stufe | steuert (am Bild belegt) |
|---|---|---|
| `3` | Struktur (32er-Belegung) | grobe Masse: wo Kopf, Beine, Lappen sitzen |
| `18` | Form 512 | Oberflaeche/Umriss-Details; **bei E entscheidet er ueber den weissen Scheitelfleck** (E_c2_form: nur Seed 18 anders -> Fleck weg) |
| `23` | Hochrechnen | Feindetail (Straehnen, Krallen) |
| `12` | Textur | Farbton. **E_c3_textur (nur Seed 12 anders): weisser Fleck bleibt** -> der Fleck haengt an der Form, nicht am Textur-Seed. A_c3: gleiche Form, Farbe gruenstichiger. Lauf in 2 s, weil ComfyUI den Rest aus dem Zwischenspeicher nahm. |

## 3. Versuche (Aufloesung 1536, Schritte 12/20/12/12, CFG 7.5/7.5/7.5/1 wenn nicht anders)
| Versuch | Seeds 3/18/23/12 | Dauer s | Befund am Bild |
|---|---|---|---|
| A_roh (Probelauf) | 56/42/42/43 | 303 | Igel-Stacheln, blass, rosa Pfoten |
| A_c1_struktur | 1001/42/42/43 | 305 | Stacheln, etwas dunkler, Form gut |
| A_c2_form | 56/1002/42/43 | 280 | Stacheln, blass, Pfoten hell |
| A_c3_textur | 56/42/42/1004 | 2 | wie roh, gruenstichig |
| **A_s2** | 2001/2002/2003/2004 | 309 | **dunkelstes Braun, Beine/Pfoten braun statt rosa, Kopf hell wie im Foto, 4 freie Beine, Ohren von allen Seiten** |
| A_s3 | 3001/.../3004 | 346 | rosa-braun, Kopf stark gesenkt |
| A_s4 | 4001/.../4004 | 305 | **weisse Flecken** auf Kopf und Ruecken -> raus |
| A_s5 | 5001/.../5004 | 276 | sehr blass rosa |
| A_k1_auf1024 | 56/42/42/43, Aufl. 1024 | 188 | Stacheln GLEICH stark, Farbe gelblich |
| A_k2_auf1024_cfg4 | wie k1 + CFG Form/Hochr. 4.0 | 214 | Stacheln gleich, heller |
| E_roh (Probelauf) | 56/42/42/43 | 174 | weisser Scheitelfleck, Lappen hinten |
| E_c1_struktur | 1001/42/42/43 | 201 | Fleck kleiner/heller, grau-beige |
| **E_c2_form** | 56/1002/42/43 | 226 | **kein Fleck, Farbe wie Foto (braun-mauve), Ohren beidseitig, Lappen hinten nur klein** |
| E_c3_textur | 56/42/42/1004 | 234 | Fleck bleibt |
| E_s2 | 2001/.../2004 | 211 | kein Fleck, aber Hinterteil zweigeteilt (Lappen) |
| E_s3 | 3001/.../3004 | 271 | weisser Fleck vorn am Kopf |
| E_s4 | 4001/.../4004 | 160 | heller Lappen hinten |
| E_s5 | 5001/.../5004 | 175 | weisser Fleck |
| E_k1_auf1024 | 56/42/42/43, 1024 | 287 | kein Fleck, grobe Straehnen, gelblich |
| E_k2_auf1024_cfg4 | 1024 + CFG 4.0 | 207 | kleiner heller Fleck |
VRAM-Spitze (ganze Karte) bis **23.464 MiB von 24.564** (A_s5) -- knapp, aber kein Absturz.

**Einstellungen gegen Stacheln** (`/object_info`: Trellis2UpsampleStage `target_resolution` 1024..2048; KSampler `cfg`, `steps`;
RescaleCFG `multiplier`; RemeshMesh `smooth_iters` max 20, `band`): gewaehlt 1024 statt 1536 (weniger Voxel fuer Feindetail) und
Fuehrung 4.0 statt 7.5 (weniger "Uebertreibung" der Bildmerkmale). **Ergebnis: beides hilft NICHT** -- die Stacheln sind auch bei
1024/CFG 4 gleich (Ton-Spalten der Blaetter). Das Modell deutet Fell grundsaetzlich als Geometrie; der Weg dagegen ist die
Nacharbeit in Blender (Abschnitt 4).

**Wahl A = A_s2:** einzig Variante mit braunen (nicht rosa) Beinen/Pfoten und Farbe nahe am Foto; keine Fremdflecken; vier
getrennte Beine (Querschnitt 3/5/4 Flecken, die angehobene Pfote erklaert die 3 unten); Ohren auf 180/270 sichtbar.
**Wahl E = E_c2_form:** einziger Versuch ohne weissen Fleck UND mit Fotofarbe; Hinterteil-Lappen viel kleiner als roh (hellbraune
Zunge statt dickem Wulst); E_k1 waere zweite Wahl (ohne Fleck, aber gelblich).

## 4. Aufbereitung zum Spielnetz (`werkzeug/spielnetz.py`, Parameter `werkzeug/param_A.json`, `param_E.json`)
1. GLB laden, verschweissen ("Hoch", 700k Dreiecke), Metall aus.
2. Kopie: Voxel-Remesh 0,005 x Laenge, nur groesstes Teil (A: 710 Kruemel weg, E: aehnlich).
3. Glaetten: Taubin 60 Durchgaenge + Laplace 60 Durchgaenge, danach Aufblasen entlang der Normalen um die mittlere Schrumpfung
   (A 0,67, E 0,86 Promille der Laenge). Kopf (Kugel um Schnauze/Kopfmitte, automatisch: vorderster Punkt in 30-80 % Hoehe) und
   Pfoten (unterste 10 %) nur mit 35 % Staerke. (Erst nur Taubin bis 600 Durchgaenge -- liess die Locken stehen; erst Laplace+Aufblasen half.)
4. Vereinfachen getrennt: Kopf+Pfoten und Rumpf je eigene Edit-Mode-Decimate, Kopf/Pfoten 2,5x Dreiecke je Flaeche
   (der Decimate-Modifier mit Eckgruppe sperrt die Gruppe ganz -- getestet, unbrauchbar).
5. Smart-UV (60 Grad, Rand 0,006), Backen 2048 vom Hoch-Netz: Diffus-Farbe, AO (Abstand 4 % Laenge), Position; dann numpy:
   Farbe weichzeichnen (Stachelmuster: A 80 %/Radius 4, E 60 %/3), AO maessig (20 %, kein Richtungslicht, Relief aus),
   E: Heck-Lappen-Farbe aus Umgebung (21.988 Texel), Farbangleich (s. 5), Rand fuellen, auf 1024 mitteln.
6. Export GLB (nur Basisfarbe, rau 0,9), Messung, Ansichten (Cycles OPTIX, Standard-Transformation, orthografisch, 30 Grad).
Wiederholen (Spiel darf laufen; GPU-Sperre macht `gpu_lauf.sh`):
```
cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen
sh werkzeug/gpu_lauf.sh log/spielnetz_A.log /c/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe --background --factory-startup --python werkzeug/spielnetz.py -- werkzeug/param_A.json
python werkzeug/spielblatt.py aus/A_roh_eingang_00001_.png bilder/einzel_A_spielnetz aus/A_spielnetz_messung.json bilder/A_spielnetz.png "Titel"
```
(E genauso mit `param_E.json`, `E_roh_eingang_00001_.png`.) Varianten: ComfyUI starten (PROBELAUF.md), dann
`python_embeded\python.exe -I werkzeug/gen_var.py werkzeug/versuche_A.json` (ueberspringt vorhandene GLB; Pause-Datei
`gpu.lock.pause` laesst Blender zwischen zwei Versuchen an die Karte), Ansichten `werkzeug/vier.py`, Blatt `werkzeug/varblatt.py`.

## 5. Messwerte
| | A_spielnetz | E_spielnetz |
|---|---|---|
| Dreiecke / Ecken | 19.124 / 9.540 | 19.562 / 9.781 |
| Teile / Randkanten (Loecher) / nicht-mannigfaltig | 1 / 0 / 0 | 1 / 0 / 0 |
| Ausdehnung x/y/z (roh) | 0,649/0,957/0,726 (0,675/0,978/0,739) | 0,442/0,983/0,680 (0,453/0,995/0,690) |
| Kantenlaenge Promille L: Kopf/Pfoten/Ruecken/Flanke/Beine | 10,6/12,5/19,1/16,9/16,5 | 10,3/10,4/17,1/15,8/16,1 |
| Beine-Querschnitt (Flecken 3-8/8-15/15-25 %) | 3/5/4 (eine Pfote angehoben) | 3/4/4 (zwei Beine dicht, Bilder: vier frei) |
| Umriss roh->Spiel IoU 0/90/180/270 | 0,937/0,947/0,941/0,945 | 0,964/0,960/0,963/0,960 |
| mittl. Umriss-Abweichung | 3,8-4,5 Promille der Hoehe (~2 px bei 800 px) | 2,8-4,0 Promille |
| Textur | 1024x1024 RGB, 1 Material | gleich |
Die Umriss-Verluste (Flaeche 94 % bzw. 96 %) sind die abgeschnittenen Stachelspitzen am Rand -- gewollt.
Bei der ersten Fassung (nur Taubin) war IoU 0,97-0,98, die Oberflaeche aber noch lockig.

**Farbe / Helligkeit:** (a) Licht geeicht: beleuchteter Render / flache Textur (Emission) gleich hell -- Verhaeltnis vor Eichung
im Test 0,84 (Probelauf-Problem nachgewiesen), jetzt 0,996 (A) / 1,004 (E), Nachweis je Ansicht in `*_messung.json`
(`farbnachweis_render_vs_textur`, z. B. A 90 Grad Render 110/98/83 vs Textur 112/100/83; E 90 Grad 116/102/102 vs 118/102/102).
(b) Fotoabgleich IM RENDER: Ansicht wie das Foto (A 60 Grad, E 90 Grad, Hoehe 10 Grad), flache Textur, Mittel der sichtbaren
Fellpixel = Mittel des freigestellten Fotos (Maske 7 px eingezogen, sRGB-Mittel): A Foto 102/90/74, Render vorher 111/98/80 ->
nachher 102/90/74; **E Foto 109/94/95, Render vorher 148/129/128 -> nachher 109/94/95** (E war im sichtbaren Teil 35 % zu hell;
das Texel-Mittel taeuschte, weil Bauch/Innenseiten dunkel sind). (c) Regionen relativ zum Foto (Kopf/Schnauze/Beine/Pfoten,
Werte im Blatt): z. B. A Beine Textur roh 91/72/51 -> 84/69/52 (Foto 84/70/55), A Pfoten 82/69/54 -> 83/71/58.
Grenze: das Foto ist stark von hinten beleuchtet (gleiches Fell 50-170 sRGB), Ruecken/Flanke deshalb nur gemessen, nicht angeglichen.

## 6. Hartes Urteil (Blaetter selbst angesehen)
**A Baerenjunges -- in Spielgroesse als Baerenjunges erkennbar, schoen ist es nicht.**
- Kopf/Ohren: Form gut, Ohren rund und auf allen 8 Seiten da. Nacken/Hinterkopf: noch Locken-Wuelste (Kopf wurde absichtlich schwach geglaettet) -- auf 135-225 Grad sichtbar.
- Schnauze/Augen: Schnauze hell wie im Foto, aber das GANZE Gesicht ist cremefarben; die dunkle Augenpartie des Fotos fehlt, Augen sind nicht zu erkennen.
- Ruecken/Flanke: glatt, Form gut; Farbe fleckig zweigeteilt (grau-beiger Ruecken, orange-braunes Hinterteil/Beine); leichtes Krakelee-Muster aus der Rohtextur bleibt in Gross sichtbar, in Spielgroesse kaum.
- Bauch: unauffaellig. Beine: vier getrennt, Pose wie Foto (eine Pfote angehoben).
- Pfoten: jetzt braun statt rosa, aber Form = glatte Stummel mit angedeuteten, eher menschlichen Zehen; keine Krallen, keine Ballen. Ehrlich: schwach.
- Hinterteil: rund, ok.
**E grosser Baer -- bester Stand bisher; Seitenansicht ueberzeugt, Kopf und Hinterteil nicht.**
- Kopf: rund, Schnauze gut, Ohren beidseitig vorhanden; Gesicht glatt, ohne Augen-Detail; hinter dem Kopf ein Wulst (Rest der Nackenmaehne).
- Ruecken: Schulterbuckel da, glatt. Flanke/Bauch: gut. Beine: vier, dunkel, stimmig.
- Pfoten: dunkel, flach, angedeutete Zehen -- in Spielgroesse ok, gross eher "Flossen" hinten.
- Hinterteil: **der Lappen ist geometrisch noch da** (kleine Zunge/Beutel auf 135-225 Grad), nur farblich angeglichen. Falsch.
- Farbe: wie Foto (braun-mauve), wirkt im grauen Licht leicht rosa; Fell-Eindruck nur schwach (glatte Plueschtier-Oberflaeche).
**Beide:** "von allen Seiten schoen" -> NEIN. Es sind glatte, gut proportionierte Plueschtier-Formen mit Fotofarbe; Fell, Augen,
Krallen fehlen, A ist fleckig, E hat den Heck-Lappen.

## 7. Loesbar? Was offen ist
- **Nacharbeit (ohne Download, meine Empfehlung):** Heck-Lappen bei E und Nacken-Wulst bei beiden gezielt wegglaetten/abschneiden
  (Kugel-Masken mit Laplace, wie Pfoten); Augen + dunkle Augenpartie (A) und Nase per 3D-Position in die Textur malen; Pfoten:
  Ballen/Krallen nicht aus TRELLIS -- besser die Pfoten aus dem eigenen Skript-Modell (baer/spiel) aufsetzen oder Krallen malen;
  Fell-Eindruck: Straehnen-Muster gerichtet (laengs Koerper) in die Textur malen statt der Rohtextur-Kerben.
- **Anderes Foto:** hilft bei A gegen Gegenlicht/Blaesse (ein Junges in gleichmaessigem Licht, Seitenansicht). Stacheln bleiben (Modell-Eigenart).
- **Volles Hauptmodell trellis_2_bf16 (9,63 GB, braeuchte Kevins Ja):** koennte Form und Textur etwas sauberer machen (int8 ist
  quantisiert); die Fell-als-Geometrie-Deutung und Zufallsflecken sind aber Eigenarten des Verfahrens, nicht der Quantisierung --
  ich erwarte keinen Sprung, ungeprueft. VRAM: int8 brauchte schon bis 23,4 GB; bf16 koennte nicht passen (ungeprueft).
- Ausrichtung/Skalierung fuer das Spiel, Knochen, Bewegung: nicht Teil dieser Stufe.
- Werkzeug-Fehler offen: `draht_kopf.png` (eigene Kopf-Kamera) ist verschoben; das Blatt zeigt statt dessen einen Ausschnitt aus `draht.png`.
- `aus/test/` und `bilder/einzel_A_test/`, `bilder/A_test_blatt.png`, `bilder/A_varianten_zwischen.png`, `bilder/E_var_zw.png` sind Zwischenstaende (loeschbar).
