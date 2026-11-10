# Bild-zu-3D-Generator fuer den Baeren -- Recherche 10.11.2026 (~20:30-21:00)

Auftrag Kevin (woertlich in `ENTSCHEIDUNGEN.md` ganz unten): Generatoren heraussuchen + Bilder eines schoenen Baeren, der ganz drauf ist.
Stand: **nur recherchiert, nichts heruntergeladen, nichts installiert, nichts ausprobiert.** Ob das Ergebnis bei einem Baeren wirklich besser
ist als das Skript-Modell, ist UNGEPRUEFT -- das zeigt erst ein Versuch.

## 1. Empfehlung: TRELLIS.2 (Microsoft) ueber ComfyUI
- **TRELLIS.2-4B**: Bild -> 3D-Netz mit Textur, 4 Mrd. Parameter, **MIT-Lizenz** (Modellkarte `huggingface.co/microsoft/TRELLIS.2-4B`: "License: mit").
  Offizieller Code nur unter Linux getestet, braucht laut README eine NVIDIA-Karte mit mindestens 24 GB (die 4090 hat genau 24 GB)
  (`github.com/microsoft/TRELLIS.2`, README "Prerequisites"). Eingabe: EIN Bild.
- **Weg unter Windows: ComfyUI.** TRELLIS.2 ist seit ComfyUI v0.34.0 (22.08.2026) fest eingebaut, kein Fremd-Zusatz noetig
  (`blog.comfy.org/p/trellis2-and-pixal3d-are-now-native`, Anleitung `docs.comfy.org/tutorials/3d/trellis2`). ComfyUI laesst sich ohne
  Fenster ueber eine lokale Schnittstelle steuern -- so wie Blender per Skript.
- Ablauf im Generator: Hintergrund entfernen (BiRefNet) -> Grobform -> Form verfeinern -> Textur -> Netz vereinfachen, UV, Textur backen.
  Ergebnis liegt unter `ComfyUI/output/3d/ComfyUI/`.

### Downloads (alle sechs brauchen Kevins Ja; Quelle jeweils der offizielle Herausgeber)
| # | Datei | Quelle | Groesse |
|---|---|---|---|
| 1 | `ComfyUI_windows_portable_nvidia.7z` (v0.44.0 vom 04.11.2026; nur entpacken, kein Installer) | `github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0` | 1,91 GB |
| 2 | `trellis_2_int8_convrot.safetensors` (Hauptmodell) | `huggingface.co/Comfy-Org/TRELLIS.2` -> `diffusion_models/` | 4,89 GB |
| 3 | `trellis_2_shape_vae_bf16.safetensors` | ebenda -> `vae/` | 1,02 GB |
| 4 | `trellis_2_texture_vae_bf16.safetensors` | ebenda -> `vae/` | 0,88 GB |
| 5 | `dino_v3_vit_l.safetensors` (Bild-Encoder; laut Anleitung gleichwertig zu `dino_v3_L_naf_fp32`) | ebenda -> `clip_vision/` | 1,13 GB |
| 6 | `birefnet.safetensors` (Hintergrund entfernen) | `huggingface.co/Comfy-Org/BiRefNet` -> `background_removal/` | 0,41 GB |
Zusammen **10,24 GB**. Beide Hugging-Face-Ablagen: Lizenz MIT, nicht zugangsbeschraenkt (API abgefragt 10.11.). Frei auf C: 266 GB.
Zielordner-Vorschlag: `C:\Users\Kevin\Tools\ComfyUI\`. Spaeter moeglich: das volle Hauptmodell `trellis_2_bf16.safetensors` (9,63 GB) statt
der 8-Bit-Fassung, falls die Form zu grob ist.

### Was NICHT genommen wird und warum
- **Pixal3D** (Tencent ARC; steckt in derselben ComfyUI-Vorlage): Gewichte unter eigener "pixal3d-license", auf Hugging Face mit
  `extra_gated_eu_disallowed: true` -> in der EU nicht nutzbar. Die Vorlage verlangt beide Hauptmodelle; Claude baut deshalb einen Ablauf
  nur mit TRELLIS.2 (ungeprueft, bis es einmal gelaufen ist).
- **Hunyuan3D 2.0 / 2.1** (Tencent): Lizenztext schliesst EU, Vereinigtes Koenigreich und Suedkorea aus.
- **Fertig-Pakete von Einzelpersonen** ("TRELLIS.2 Windows Portable" u. ae.): keine offizielle Quelle -> nicht herunterladen, nicht starten.
- **Web-Dienste** (Meshy, Tripo, Rodin): Konto + Hochladen.

### Was danach Claudes Arbeit bleibt
Das erzeugte Netz ist dicht (hunderttausende Dreiecke), ohne Knochen und in der Pose des Fotos. Danach: auf hoechstens 20.000 Dreiecke,
Skelett (26 Knochen) in die Pose des Netzes legen und binden, Gewichte, 15 Clips, Textur 1024, feste Regeln nachmessen, aus Kevins
Spielkamera rendern und neben das Foto legen. Deshalb sind STEHENDE Bilder besser als gehende (weniger Verzug beim Binden).
Grenzen: die abgewandte Seite wird geraten; Fell ist nur Textur, keine Haare; waehrend das Spiel laeuft, wird der Grafikspeicher knapp.

## 2. Baerenbilder (Wikimedia Commons, 133 gesichtet, 8 in der Auswahl; Blatt `auswahl_baerenbilder.jpg`, nicht in Git)
| | Bild (Commons-Dateiname) | Masse, Groesse | Lizenz | Urteil |
|---|---|---|---|---|
| A | `Bear cub on the beach (53167951257).jpg` | 5294x3309, 11,5 MB | CC BY 2.0 (Kandukuru Nagarjun) | **Junges, steht, alle Pfoten auf Sand, schraeg von vorn -- bestes Bild fuer das Junge** |
| B | `A spring cub (f4738912-cafc-492e-a4bd-a385cc0f51f4).jpg` | 6000x4000, 0,9 MB | gemeinfrei (NPS, M. Lewandowski) | Junges genau von der Seite, geht; Pfoten teils im Gras |
| C | `Eurasian brown bear (Ursus arctos arctos) cub 14 months.jpg` | 4378x2919, 11,3 MB | CC BY-SA 4.0 | 14 Monate, von vorn, Pfoten zwischen Steinen |
| D | `Cute Grizzly Bear Cub (48847666381).jpg` | 4471x2980, 8,3 MB | CC BY 2.0 | klein im Bild, von oben, helle Halskrause |
| E | `909's 2 5 Year Old Cub (Fat) (53214356524).jpg` | 6000x4000, 13,1 MB | gemeinfrei (KatmaiNPS) | **steht ruhig, rund, ganz drauf -- bestes Bild fuer den grossen Baeren** |
| F | `909's 2 5 Year Old Cub (Skinny) (53214448140).jpg` | 5079x3371, 2,4 MB | gemeinfrei (KatmaiNPS) | sauber von der Seite auf Kies, geht, eher duenn |
| G | `Grizzly bear cub walking brown bear.jpg` | 2100x1400, 0,3 MB | gemeinfrei (USFWS, S. Hillebrand) | von der Seite, geht, alle Beine frei |
| H | `910's 2 5 year-old cub (NPS-T Carmack) 07042024 (54039061200).jpg` | 5184x3888, 9,4 MB | gemeinfrei (NPS) | hell, geht, Kopf unten |
Adresse je Bild: `https://commons.wikimedia.org/wiki/File:<Dateiname mit _ statt Leerzeichen>`. Nicht genommen: `128 Grazer's spring cub
(M Freels) ...` (schoenes Seitenbild, aber im Namen "not an NPS photo"). Kevin 10.11.: die Lizenz der Bilder ist ihm egal ("du klaust ja
nicht das bild ... sondern nur den baeren"); freie Bilder wurden trotzdem bevorzugt, weil es nichts kostet.
Noch nicht gesucht: ein richtig ausgewachsener, schwerer Baer (E und F sind zweieinhalb Jahre alt).

## 3. Entschieden (Kevin 10.11. ~20:28) und offen
- **Kevin: "Ja, alle sechs"** (Downloads) und **"nimm A fuers baby und E fuer den grossen und mach das bitte richtig schoen von allen seiten
  das es immer gut aussieht"**. Die sechs Dateien laden nach `C:/Users/Kevin/Tools/ComfyUI/_download/` (`laden.sh`), die Bilder A und E
  liegen als `vorlage_A_junges.jpg` / `vorlage_E_gross.jpg` hier im Ordner (nicht in Git), Zuschnitte in `../../_arbeit/baer_gen/eingang/`.
- Kevin fragte, ob der Baer diesmal sicher gut wird. Antwort: NEIN, nicht sicher -- erster Versuch; er sieht Rundum-Bilder, bevor etwas ins
  Spiel kommt.
- Der laufende Lauf baer-junges baut Koerper, Kopf und Textur per Skript auf Fable; kommt die Form aus dem Generator, sind Kopf und Textur
  ueberholt (Skelett-Masse und Clip-Umrechnung bleiben nutzbar). Verbrauch ~20:20: 5 h 25 %, Woche alle 33 %, **Woche Fable 64 %**.
