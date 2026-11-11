# Probelauf Bild-zu-3D (TRELLIS.2 ueber ComfyUI) -- 10.11.2026, ~20:46-21:15

Kurz: **Der Weg laeuft** (lokal, ohne weitere Downloads, 3-5 min je Bild, Aufloesung der Vorlage 1536 passt in 24 GB).
Beide Rohmodelle sehen von allen Seiten nach einem Baeren aus. Sie sind aber **NICHT "richtig schoen von allen Seiten"**:
Fell ist als stachelige Geometrie gebaut (Igel-/Zapfen-Oberflaeche), Pfoten sind kahl, E hat einen weissen Fleck auf dem Kopf und
einen falschen Lappen am Hinterteil. Das Spiel lief waehrend des ganzen Laufs NICHT (tasklist vor jedem Lauf geprueft).

## 1. Was installiert wurde
| Was | Pfad | Groesse |
|---|---|---|
| ComfyUI v0.44.0 portable (entpackt, 62.623 Dateien) | `C:\Users\Kevin\Tools\ComfyUI\ComfyUI_windows_portable\` | 12,76 GB gesamt mit Modellen (4,51 GB Paket) |
| Hauptmodell | `...\ComfyUI\models\diffusion_models\trellis_2_int8_convrot.safetensors` | 5.253.048.192 B |
| Form-VAE | `...\ComfyUI\models\vae\trellis_2_shape_vae_bf16.safetensors` | 1.095.844.024 B |
| Textur-VAE | `...\ComfyUI\models\vae\trellis_2_texture_vae_bf16.safetensors` | 948.461.364 B |
| Bild-Encoder | `...\ComfyUI\models\clip_vision\dino_v3_vit_l.safetensors` | 1.212.559.776 B |
| Hintergrund-Entferner | `...\ComfyUI\models\background_removal\birefnet.safetensors` | 444.473.596 B |
Das `.7z` liegt weiter in `C:\Users\Kevin\Tools\ComfyUI\_download\`. Python 3.13.14, PyTorch 2.14.1+cu130 (im Paket).
Keine Custom Nodes, kein pip, kein Nachladen; das Server-Log zeigt keinen Download-Versuch.

## 2. Werkzeuge (neu)
- `baer\tools\gen_trellis.py` -- Startskript (nur Standardbibliothek): Bild nach `ComfyUI\input`, `/prompt`, wartet auf `/history`,
  misst VRAM-Spitze (nvidia-smi alle 2 s, ganze Karte), kopiert GLB + Eingangsbild + Maske + Basisfarbe + `<name>_lauf.json`.
  Schalter: `--aufloesung` (1024..2048), `--seed` (Versatz auf alle vier Seeds), `--ohne-entferner` (Maske = PNG-Alpha), `--textur`, `--flaechen`.
- `baer\tools\trellis2_ablauf_api.json` -- Ablauf im API-Format, erzeugt von `_arbeit\baer_gen\werkzeug\baue_ablauf.py`.
  Aus der Vorlage `3d_pixal3d_trellis2_image_to_model.json` (templates 0.11.101); Pixal3D-Lader, MoGe und Pixal3DConditioning entfernt,
  Schalter fest auf TRELLIS.2. Abweichungen von der Vorlage (begruendet im Skript): `pad_factor` 1.0 statt 1.1 (Tooltip von
  Trellis2Conditioning: "pad_factor=1.0 for TRELLIS.2"); `SaveGLB` statt `MeshToFile3D`+`Save3DAdvanced` (gleiche GLB-Funktion
  `mesh_item_to_glb_bytes`, braucht keinen Browser); ohne-Entferner-Zweig mit `InvertMask` (LoadImage liefert 1-Alpha -- der
  Vorlagen-Zweig wuerde die Maske umgedreht benutzen); dazu SaveImage fuer Eingangsbild, Maske, Basisfarbe.
- `_arbeit\baer_gen\werkzeug\rundum.py` (Blender: messen + 8x2 Ansichten, OPTIX, 64 Samples, OPTIX-Entrauscher, orthografisch,
  Hoehenwinkel 30 Grad), `blatt.py` (PIL: Blatt).

## 3. Wiederholen
```
cd C:\Users\Kevin\Tools\ComfyUI\ComfyUI_windows_portable
python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --listen 127.0.0.1 --port 8188 --disable-auto-launch
   (im Hintergrund lassen; diesmal per PowerShell Start-Process, Ausgabe nach _arbeit\baer_gen\log\comfy_*.log)
cd C:\Users\Kevin\NPCCrew-Nebenprojekte
python -I baer\tools\gen_trellis.py --bild _arbeit\baer_gen\eingang\A_zuschnitt.png --name A_roh --aus _arbeit\baer_gen\aus
python -I baer\tools\gen_trellis.py --bild _arbeit\baer_gen\eingang\E_zuschnitt.png --name E_roh --aus _arbeit\baer_gen\aus
blender.exe --background --factory-startup --python _arbeit\baer_gen\werkzeug\rundum.py -- <glb> <einzelordner> 600 64
python -I _arbeit\baer_gen\werkzeug\blatt.py <foto> <einzelordner> <blatt.png> "<titel>"
```
Danach den Server-Prozess beenden (diesmal PID 20868, beendet 21:1x). Neue Ausgaben zaehlen hoch (`..._00002_`), das Skript kopiert immer
die des Laufs. Gleiche Seeds + gleiche Einstellungen sollten gleiches Ergebnis geben (ungeprueft).

## 4. Laeufe
Beide: Aufloesung 1536 (Vorlage, nicht verkleinert noetig), Seeds 56 / 42 / 42 / 43 (Struktur / Form / Hochrechnen / Textur),
Schritte 12 / 20 / 12 / 12, CFG 7.5/7.5/7.5/1, Remesh 768 solid, auf 700.000 Flaechen, UV-Atlas 4096, BiRefNet AN.
| | A Junges | E grosser Baer |
|---|---|---|
| Dauer | 303 s (inkl. erstes Laden aller Modelle) | 174 s |
| VRAM-Spitze (ganze Karte, nvidia-smi) | 21.448 MiB | 18.590 MiB |
| vorher belegt (Windows/andere) | ~2.800-3.100 MiB | ~2.900 MiB |
| Maske | sauber: Ast NICHT dabei, alle 4 Pfoten ganz, leichter gruener Saum am Fell | sauber, alle Pfoten ganz |
| Dreiecke | 699.947 | 699.988 |
| Ecken (Datei / verschweisst) | 647.226 / 347.944 | 569.911 / 349.821 |
| getrennte Teile | 1 | 1 |
| wasserdicht | fast: 2 Randkanten, 26 nicht-mannigfaltige Kanten | fast: 0 Randkanten, 3 nicht-mannigfaltige Kanten |
| Ausdehnung (Blender x/y/z, auf Laenge 1 genormt) | 0,77 / 0,99 / 0,80 | 0,46 / 1,00 / 0,69 |
| Texturen | Basisfarbe 4096, Metall/Rauheit 4096, Normal 2048 (+AO) ; 1 Material | gleich |
| Beine getrennt | ja (Querschnitt unten 3-5 Flecken, Bilder: freie Beine, keine Haut dazwischen) | ja (3 Flecken; zwei Beine liegen in der Draufsicht dicht beieinander; Bilder: vier freie Beine) |
| Boden / Ast im Netz | nein / nein | nein / nein |
| GLB-Datei | 82,9 MB | 74,1 MB |
Der Hintergrund-Entferner hat nichts falsch gemacht -> keine eigene Freistellung noetig, keine zweite Variante gebaut.
Mittlere Farbe Basisfarbe vs. freigestelltes Foto (RGB): A 127/111/94 vs 100/88/72 (**Textur ~25 % zu hell**), E 99/86/85 vs 102/89/89 (passt).
Die Blatt-Bilder sind zusaetzlich etwas heller als die Textur (Sonne 3,5 + Himmel 0,45).

## 5. Ergebnisse
- GLB: `_arbeit\baer_gen\aus\A_roh.glb`, `E_roh.glb` (+ `*_eingang_*.png`, `*_maske_*.png`, `*_basecolor_*.png`, `*_lauf.json`)
- Blaetter: `_arbeit\baer_gen\bilder\A_rundum.png`, `E_rundum.png` (2400x1418), Einzelbilder `bilder\einzel_A|E\`, Messung `einzel_*\messung.json`
- Logs: `_arbeit\baer_gen\log\`

## 6. Ehrliches Urteil (Bilder selbst angesehen)
**A Junges -- Umriss gut, Oberflaeche und Farbe schlecht.** Von allen 8 Seiten klar ein junger Baer in der Pose des Fotos
(vorn rechts angehobene Pfote, Gewicht nach vorn). Rundlicher Koerper, Rueckenlinie und Hinterteil glaubhaft, auch die nicht sichtbare
linke Seite und der Ruecken sind plausibel geraten.
- Kopf: Form ok, Schnauze ok; Gesicht aber blass-cremefarben, die dunkle Augenpartie des Fotos fehlt weitgehend.
- Ohren: beide da, rund, richtig gross. Hinterkopf/Nacken: dichter Stachel-"Kragen".
- Fell: **das groesste Problem** -- das ganze Fell ist als tausende kleine Stacheln/Schuppen in die Geometrie geformt (im Tonbild
  deutlich: wie ein Tannenzapfen/Igel). Nicht weich, nicht flauschig. Fuer 20.000 Dreiecke im Spiel faellt das zwar weg, aber die Textur
  ist auf diese Stacheln gebacken.
- Pfoten: kahl, hautfarben-rosa, fast menschliche "Fuesse" mit Krallen -- falsch (im Foto dunkel und behaart, Sohlen nur unten).
- Bauch: von unten kaum zu sehen, wirkt geschlossen; keine Auffaelligkeit. Farbe insgesamt zu hell/grau-beige statt braun.
**E grosser Baer -- Seitenansicht stark, Kopf und Hinterteil falsch.** Die Seite des Fotos (90 Grad) trifft Koerper, Buckel, Beine und
nasses Fell gut, Farbe passt.
- Kopf: Schnauze und Gesicht von vorn brauchbar; **auf Stirn/Scheitel ein grellweisser Stachelfleck** (geraten, im Foto nicht da) --
  von jeder Seite sichtbar und der auffaelligste Fehler. Ohren: vorhanden, aber an der abgewandten Seite unpassend (rund-wulstig, eines
  steht seitlich weg).
- Hinterteil: **ein grosser falscher Lappen/Wulst** haengt hinten wie ein dicker Schwanz (in 135-225 Grad deutlich). Falsch.
- Pfoten: flache, dunkle "Flossen" mit angedeuteten Zehen; vorn ok, hinten paddelartig; eine Hinterpfote ballig.
- Rueckenlinie: gut (Schulterbuckel da). Bauch: ok. Abgewandte Seite: Koerper ok, Kopf/Ohren schlechter.
**Gesamt:** Als Ausgangspunkt fuer Form und Masse besser als jedes Skript-Modell bisher (Silhouette, Proportion, Pose stimmen), als
fertige Optik "von allen Seiten schoen" klar NEIN. Vor einem Einsatz waeren noetig: Fell-Stacheln glaetten (Remesh/Glaetten, oder neu
backen nach dem Verkleinern), Pfoten nacharbeiten, bei E Kopf-Fleck und Hinterteil-Lappen entfernen, Farbe A abdunkeln.

## 7. Was nicht ging / offen
- Nichts ist abgestuerzt; kein Speicherproblem bei 1536.
- Nicht probiert: andere Seeds (die Fehler bei E -- weisser Fleck, Lappen -- sind vielleicht Zufall; je Versuch nur ~3 min),
  Aufloesung 1024/2048, volles bf16-Hauptmodell (wuerde einen weiteren Download brauchen), `smooth_iters`/`band` im Remesh hoeher
  gegen die Stacheln.
- Vorderseite des glTF: Blender-Winkel 0 zeigt das Tier schraeg von vorn-links; die Laengsachse liegt auf Blender-Y. Fuer den Spiel-Export
  muss die Ausrichtung noch festgelegt werden.
- Querschnitt-Zaehlung der Beine ist grob (Rasterung); die Bilder sind der eigentliche Beleg.
