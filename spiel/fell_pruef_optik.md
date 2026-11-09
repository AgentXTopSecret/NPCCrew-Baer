# Lauf baer-fell: Pruefer OPTIK (Gegenstand: neues GLB + neue Body-Textur gegen den Stand in NCBearTest)

Stand 09.11.2026, PZ 42.21, Blender 5.2.3. **Statisch/offline geprueft und gerendert, nicht gespielt.** Alle Renders RTX 4090,
OptiX + OptiX-Entrauscher, ueber `werkzeug/gpu_render.sh` (vor jedem Lauf `tasklist`: Spiel lief nie; Sperre `gpu.lock` nach jedem
Lauf frei). Nichts in die Test-Mod oder nach NPC Crew geschrieben, nichts committet, keine Datei der Bauer geaendert.
Eigene Dateien nur in `_arbeit/baer_fell/pruef/optik/` (Pfade unten relativ dazu).

Geprueft: `_arbeit/baer_fell/mod/42/media/models_X/Skinned/NCBear.glb` (MD5 `c8250ace...`) + `textures/Body/NCBear.png`
(1024, MD5 `79a9aca4...`) gegen `Zomboid/mods/NCBearTest/42/media` (GLB `4cfe4f29...`, Body `a800c084...`). Beide GLB selbst mit dem
Importer des Spiels gelesen (`_arbeit/baer_spiel/harness/Dump.java`): `dump/dump_alt.txt` (= `bestand/dump.txt`, MD5 `9267335...`),
`dump/dump_neu.txt` (MD5 `eafc2bae...`). Die Dateien eines abgebrochenen Laufs in `pruef/` (dump_*.txt, ref/, dump/) nicht benutzt.

## 0. Kurz

1. **Sohlen: ja, im Spielwinkel jetzt als Pfote mit Ballen lesbar, kein schwarzes Loch mehr.** Sitzen, Spielgroesse: Sohle/Ruecken
   0,22 -> 0,51 (Licht A) bzw. 0,33 -> 0,81 (Licht B, naeher am Spiel); Ballen sichtbar auch mit 256er Textur. Form (Ton) bleibt ein
   rundes Roehrenende - die Textur traegt die Sohle.
2. **Unterseite: deutlich besser** - Brust/Bauch nicht mehr dunkel verschmiert (Rear, Brust Luma 18 -> 27, Bauch 9 -> 26 bei Licht A),
   die hellen Hautlappen an Handgelenken/Achseln (alt Rear, Hieb, Tot) sind weg, Innenstreifen unten an den Hinterbeinen weg.
3. **ABER (major): der helle Streifen innen an den Hinterbeinen beim Aufrichten von vorn ist NICHT weg, er ist heller geworden.** Es ist
   die Region "Leiste": Textur-Luma dort 151 statt 83 (Ruecken 97). Im Spiel-Licht B leuchtet sie als goldenes "V" (Luma 122-125,
   Stirn 83; alt 92-104). Das ist genau der Streifen aus Kevins Bild.
4. Form: "Ei" von vorn und Pranken-Form praktisch unveraendert (Breite oben/unten 0,924 -> 0,941). Hinterteil heller, Form gleich.
5. Bewegung **ruhiger**: Knick-Kanten (Flaechenwinkel +25 Grad gegen Ruhe) in jedem Clip weniger, Gehen -41 %, Hieb -45/-47 %, Tot -32 %.
   Neu: kleine Delle vorn am rechten Hinterknie bei Hieb R/Slam (Hand-Gewicht auf Kniepunkten).
6. Kopf unveraendert (Texel 0 Unterschied, Geometrie bis auf Nahtrand gleich), Maul-Flecken frei, Hals-Naht wie vorher.
7. Straehnen im Spielbild nicht staerker als vorher; an Beinen/Hinterteil eher Flecken ("Frottee") als Straehnen. Pfoten neu rostorange.
8. 1024 statt 2048 ist optisch richtig (Flimmer-Nachbau: 2048 verdoppelt das Flimmern, +30 % Detail).

Kein Blocker gefunden. 4 major, 8 minor (Abschnitt 3).

## 1. Wie gerendert

- Werkzeug `werkzeug/render_optik.py` = Kopie von `_arbeit/baer_fell/werkzeug/render_bestand.py` (Haeutung wie Importer aus dem Dump),
  ergaenzt um: `amb/lmax` (Licht A heller), `pxu` (Spielgroesse in Pixel je Modelleinheit), Textur je Bild, `spp/pfilter`, und
  **Shader `spielB`**.
- **Licht A** = Forschung A (`forschung_bestand.md` 1): Textur x min(1; 0,4 + 0,375 x Lambert), Licht (0,2,5). Wie verlangt.
- **Licht B** = Forschung B (`forschung_engine.md` 4.1): Ambient 0,45 + zwei Fuell-Lichter 0,425 aus 19,5 Grad Hoehe von der
  Kameraseite und gegenueber, je Kanal auf 1 gedeckelt.
  **Kalibrierung an Kevins Bildern** (`werkzeug/kal_kevin.py`, alter Baer ausgerichtet auf Kevins Ausschnitt, Korrelation der
  Helligkeit je Pixel): Aufrichten A 0,825 / **B 0,913**, Sitzen A 0,536 / **B 0,749**. Licht B trifft das Spiel deutlich besser
  (Bild `blaetter/d1_B_rear_sit_kevin.png`); die Helligkeit im Spiel liegt dabei etwa beim 0,75-0,9-fachen von B. Darum stehen
  unten beide Lichter; die Texturmessungen der Bauer ("im Spiel hell") sind mit Licht A gerechnet.
- Spielgroesse: aus Kevins Aufrichten-Bild (Bildschirm 3840 breit, Bild 2000 breit) 563 Pixel je Modelleinheit bei 4K -> `pxu 560`;
  Kevins Ausschnitte 2-fach vergroessert (`ref/kevin_*_crop2.png`) haben dieselbe Groesse. Kamera Spielwinkel el 30 Grad, Aufrichten
  az 0, Sitzen az 300 (wie Forschung A). "halb" = doppelt so weit herausgezoomt.
- Posen: Rear 1,3 s (Bild 39), Sit 0 s und 2,0 s, DeerStag_Dead, Walk 0/0,233/0,467/0,7 s, SwipeL/R 0,433 s (Ausholen) und 0,6 s
  (Schlag; aus dem Dump als Bild groesster Reichweite bestimmt), Slam 0,9 s, Bite 0,533 s, Eat 0,7 s.
- Pfotenfoto `baer/begleiter/kevin_pfotenvorlage.png` und Kevins Spielbilder nur angesehen und daneben gestellt (`ref/`).

Alle Bilder habe ich angesehen (Read). Einzelbilder: `render/alt/`, `render/neu/`, `render/alias/`; Auftraege `auftrag*.json`.

## 2. Antworten auf die Fragen (mit Bildern)

| Frage | Antwort | Bilder |
|---|---|---|
| Sohlen im Spielwinkel als Ballen erkennbar? | **Ja.** Sitzen Spielgroesse: Sohlen-Luma 14 -> 33 (A), 23 -> 55 (B); Ruecken 63-68; Kevins Spiel (alt) 15/62. Ballen hellste 20 % 41/71, Furchen dunkelste 20 % 21/40 -> Muster sichtbar; bei 512 und 256 noch lesbar. Von unten (Ruhe) alle vier Sohlen mit 5 Zehenballen, Sohlenballen, Handwurzel- bzw. Fersenballen. | `blaetter/a0_uebersicht.png` Zeile 2-3, `b5_sit_spiel.png`, `b6_sit_fuss.png`, `d4_B_nah.png`, `c5_sohlen_pur.png`, `c6_sohlen_spiel.png`, `b11_unten_sohlen.png`, `e4_textur_1024_512_256.png` |
| Unterseite ausgearbeitet, nicht mehr dunkel verschmiert? | **Ueberwiegend ja.** Rear Spielgroesse (A): Brust 18 -> 27, Bauch 9 -> 26, Pranke 16 -> 36 (Stirn 73 = gleich). Von unten Bauch mit laengs laufenden Straehnen statt Flecken (Kohaerenz Bauch 0,55 -> 0,68, `werkzeug/struktur.py`). Hautlappen/Risse an Achsel und Handgelenk weg (alt deutlich in Rear, SwipeL von unten, Tot). **Ausnahme Leiste** (major 1). | `b1_rear_spiel.png`, `b2b_rear_unten_aufgehellt.png`, `x_B_rear_pranken.png`, `x_swipel1_unten_nah.png`, `b9_dead_spiel_ton.png`, `x_B_dead_spiel_s120_zoom.png` |
| Hinterteil kein Klumpen mehr? | **Teils.** Farbe heller (hinten Luma 47 -> 59, Licht B), nicht mehr einheitlich dunkel; Form im Ton gleich (Gesaessfalte kaum zu sehen). Fell dort jetzt gesprenkelt (major 4). | `b10_hinten.png`, `c8_fell.png`, `d2_B_spielwinkel.png` unten |
| Straehnen sichtbar oder kuenstlich? | Ruecken/Flanke im Spielbild wie vorher (Kontrast 0,047 -> 0,050 / 0,049 -> 0,057, Kohaerenz 0,61 -> 0,61). Nicht regelmaessig/gekachelt. Beine/Hinterteil: weniger Straehne, mehr Sprenkel (Kohaerenz Hinterbein 0,48 -> 0,43, hinten 0,57 -> 0,53). Gesamtes Detail im Spielbild +10 % (`werkzeug/alias_mass.py`: 2,98 -> 3,28). | `c8_fell.png`, `x_B_idle_hinten_spiel_zoom.png`, `e3_flimmern_1024_2048.png` |
| Neue Hubbel, Naehte, Dreckflecken, Farbspruenge? | Keine neuen Hubbel im Ton sichtbar (Ausnahme Knie-Delle minor 2). Naehte: Rumpf-Naht-Sprung Median 6,8 -> 10,2 sRGB, aber die Fellstruktur selbst ist auch kontrastreicher (Innenkanten 6,6 -> 9,3) - in den Bildern keine Nahtlinie gefunden. Neu: rostorange Pfoten (minor 1), zwei kleine scharfkantige helle Flecken (minor 4). | `c11_naehte.png`, `e1_orange_karte.png`, `x_flecken_rear.png` |
| Hals-Naht? | **Unveraendert.** Naht-Kanten Hals: Median 10,8 -> 11,2, max 22,5 -> 23,9, keine ueber 25. Im Bild dieselbe Kragenlinie wie vorher (von unten der Kopf-Ring, hinter dem Ohr eine Linie) - war schon da, nicht schlechter. | `c9_naht.png`, `b12_kopf_hals.png` |
| Kopf unveraendert? | **Ja.** Body-Textur: 156.275 Kopf-Texel (Dreiecke mit Kopf/Kiefer >= 0,9, 2 px eingerueckt) **0 Unterschied**; Maul-Flecken (280,16,80,80), (376,16,80,80), (472,16,24,24) **0 Unterschied** (`werkzeug/kopf_texel.py`). Geometrie: 1.509 von 1.534 Kopfpunkten gleiche Lage+UV, 25 am Halsrand; gehaeutet max 0,77e-3 Einheiten (1,4 mm) Abweichung. Im Bild nicht zu unterscheiden. | `b12_kopf_hals.png` |
| Bewegung ruhiger, nirgends eingedellt/zerrissen? | **Ruhiger, ja.** Rumpfkanten mit Flaechenwinkel +25 Grad gegen Ruhe, Mittel je Clip alt -> neu: Walk 420 -> 246, Run 966 -> 810, SwipeL 222 -> 120, SwipeR 215 -> 113, Slam 319 -> 231, Rear 531 -> 406, Sit 751 -> 644, Dead 1.189 -> 810, Bite 170 -> 143 (`werkzeug/knicke.py`). Ton-Bilder Gehen: Knickfalten an Hinterbein/Ellbogen weg; Hieb R: Achsel-Riss weg. Neu eine kleine Delle am rechten Hinterknie (minor 2). Nichts zerrissen. | `b14_walk_ton.png`, `x_swiper0_ton_nah.png`, `b16_swipel.png`, `b17_swiper.png`, `c1_knie_ton.png`, `c3_slam_folge.png` |

## 3. Befunde

### major 1 - Heller Streifen innen an den Hinterbeinen (Leiste) beim Aufrichten bleibt und ist heller
- Beleg: `blaetter/x_B_rear_beine.png` (Kevin | alt | neu, Licht B), `d1_B_rear_sit_kevin.png`, `b1_rear_spiel.png`, `d4_B_nah.png`
  (B_rear_gross), `d2_B_spielwinkel.png` (Rear s45, Sitzen s60: goldenes Band am Oberschenkel).
- Messung Rear Spielgroesse, Luma Band links/rechts: Kevin 95/96; Licht A alt 46/54 -> neu 61/65; **Licht B alt 92/104 -> neu 122/125**,
  Stirn 83 (B). Ort: Punkte 1899/1894/4061 (Ruhe x +-0,11-0,15, y 0,08, z 0,24 = Leiste/Schenkel vorn), Region "Leiste" in
  `netz/karten/karten_2048.npz`. Textur dort sRGB (184-203, 128-143, 79-89) = **Luma 151, 1,56 x Ruecken** (alt 83 = 0,86 x).
- Ursache (Schluss aus der Messung): die Aufhellung der Unterseite ist fuer die Ruhehaltung gerechnet (Flaeche nach unten, nur Ambient).
  Beim Aufrichten/Sitzen/Liegen dreht die Leiste zur Kamera und bekommt volles Licht -> leuchtet. Kevins "heller Streifen innen" ist
  im Bild genau dieses Band (der untere senkrechte Innenstreifen ist dagegen weg).
- Vorschlag: Leiste/Schenkel-Vorderseite in der Textur hoechstens auf ~1,0-1,1 x Ruecken-Luma, dort keine helleren Haarspitzen;
  Pruefung im Rear-Spielwinkel mit Licht B (Band <= Brust + 20 %).

### major 2 - "Ei" und Pranken-Form von vorn beim Aufrichten unveraendert
- Beleg: `b4_rear_ton.png`, `x_rear_ton_nah.png`, `x_B_rear_pranken.png`. Breite ohne Armpunkte (Armgewicht < 0,3) im Rear 1,3 s:
  oben (1,3-1,5 m) / unten (0,4-0,8 m) = 0,897/0,971 = **0,924 -> 0,905/0,962 = 0,941** (Ziel >= 0,95; gleicher Wert wie Bauer Netz).
  Umriss-Profil `rear_vorn_tief`: Schulter +8 %, Huefte -3 % - im Bild nicht als andere Form zu sehen.
- Pranken: Farbe besser (keine Lappen, heller), Form im Ton dieselbe Schaufel mit Knick am Handgelenk. Kevins Punkte "Rumpf von vorn
  ein Ei" und "Vorderpranken formlose Klumpen" sind optisch nur in der Farbe geloest.

### major 3 - Kevins Punkt (2) "staerkere Straehnen": im Spielbild nicht erreicht
- Beleg `werkzeug/struktur.py` (Licht B, Spielgroesse): Kontrast Ruecken 0,047 -> 0,050, Flanke 0,049 -> 0,057, Hinterteil 0,057 -> 0,059;
  Bilder `c8_fell.png` (Flanke nah alt/neu kaum verschieden). Body bleibt 1024 (richtig, siehe 4.); die Straehnen muessten breiter/
  kontrastreicher in der 1024er stehen, damit sie ankommen. Bauch ist die Ausnahme (laengs, Kohaerenz 0,68).

### major 4 - Beine und Hinterteil wirken gesprenkelt (Flecken statt Fell)
- Beleg: `x_B_idle_hinten_spiel_zoom.png`, `d2_B_spielwinkel.png` (idle_hinten), `b10_hinten.png` (`render/neu/idle_hinten.png`),
  `render/neu/dead_hinten.png`, `x_B_dead_spiel_s120_zoom.png`. Dunkle Sprenkel/Kringel ueber Hinterteil und Beine ("Frottee"),
  dazu ein Wirbel am Schwanzansatz (`render/neu/dead_hinten.png` um x 420-450, y 560-620). Kohaerenz Hinterbein 0,48 -> 0,43,
  hinten 0,57 -> 0,53; Kontrast Hinterbein 0,117 -> 0,073 (weniger Straehne, mehr Rauschen). Wirkt in Spielgroesse wie Schmutz,
  Geschmackssache - Kevins Blick entscheidet. Vorschlag: Sprenkel an Beinen/Hinterteil daempfen, Buesche laenger in Haarrichtung
  (`BAER_TX_STRAEHNE` laut `bau_textur.md` 8.3).

### minor 1 - Pfoten rostorange
- Beleg `x_pfote_vorn_zoom.png`, `c4_pfoten.png`, `x_B_idle_spiel_zoom.png`, `e1_orange_karte.png` (magenta = Saettigung > 0,62 und
  Helligkeit > 0,30): Anteil der Fellpixel alt 0,0-0,1 % -> neu 0,4-0,7 % (Idle, Sit, Rear), vor allem Zehen/Handgelenk und Kanten der
  Unterarme. Alt waren die Zehenkuppen grau-beige. Im Spielbild als roetliche Pfoten zu sehen (`b5_sit_spiel.png`).

### minor 2 - Delle am rechten Hinterknie bei Hieb R und Slam; fremde Hautgewichte
- Beleg `c1_knie_ton.png`, `render/neu/knie_swiper_ton.png` (schwarze Kerbe), `c3_slam_folge.png` (Stern-Knautsch 0,7-1,0 s);
  im Textur-Bild nur ein dunkler Punkt (`c2_knie_spiel.png`). Ort Punkte 1527/1528/1583/1584 (Ruhe x -0,10..-0,14, y 0,12, z 0,15).
- Ursache (Dump): diese Kniepunkte tragen Gewicht an `Bip01_R_Hand`/Unterarm (1527: 0,024; bis 0,031 an Punkt 3941 links). Neu
  haben 23 Hinterkoerperpunkte Hand/Unterarm-Gewicht > 0,005 (alt 1, max 0,005); 248 Vorderbeinpunkte tragen Hals/Kopf-Gewicht bis
  0,092, 133 Hinterkoerperpunkte bis 0,049 (`werkzeug/gewicht_fremd.py`). Ohne diese Anteile laege die Haut je Clip bis 2,0-3,6 cm
  anders (`werkzeug/leck_wirkung.py`, z. B. SwipeR 3,6 cm, Sit 3,6 cm). Fuer diese 15 Clips sichtbar nur die Knie-Delle; Risiko bei
  neuen/geaenderten Clips (der Netz-Pruefer sollte das bewerten).

### minor 3 - Sohle: Ballen kleiner als im Foto, Sohlenhaut dominiert; Form bleibt Scheibe
- `c5_sohlen_pur.png`, `b6_sit_fuss.png`: Zehenballen und querliegender Sohlenballen deutlich kleiner als in Kevins Foto, viel dunkle
  Sohlenhaut dazwischen; die Lederrisse wirken in Spielgroesse wie Noppen-/Reifenprofil; der Fellkranz als gepunkteter Ring. Im Ton
  (`sit_fuss_nah_ton`) ist die Sohle weiter ein rundes Roehrenende (Ballen 8 mm). Mit Licht A bleibt die Sohle das Dunkelste
  (Luma 33 bei Ruecken 64). Kein Blocker: als Pfote lesbar.

### minor 4 - Kleine scharfkantige helle Flecken
- `x_flecken_rear.png`: heller Dreieck-Fleck innen am Unterarm (Rear, Punkte 6672/4384, Rear-Lage x 0,08 y 0,20 z 0,62) und helle
  Kante an der Bauchseite (Punkte 3973/3974); `c11_naehte.png` (naht_bein_hinten): helle gezackte "Flamme" innen am Oberschenkel.
  Jeweils 2-4 cm, Spielgroesse kaum sichtbar.

### minor 5 - Hinterteil-Form (Kevins Punkt 5) unveraendert
- `b10_hinten.png` (Ton): Gesaessfalte 25,8 mm im Bild nicht zu erkennen; Klumpen-Eindruck nur durch Farbe gemildert.

### minor 6 - Zotteln (Kevins Punkt 1) nicht umgesetzt
- Umriss in allen Bildern wie vorher (bewusst verworfen, `bau_netz.md` 4). Kevins Wort noetig.

### minor 7 - Liegen: Falten Ellbogen/Achsel
- `x_dead_links_ton_zoom.png`: hinter dem Ellbogen fleckige Schattierung (Flaechenknicke) im Ton, mit Textur unsichtbar
  (`x_dead_links_zoom.png`); Knick-Kanten Dead 1.189 -> 810. Kevins Punkt 6 messbar besser, optisch nur im Ton sichtbar.

### minor 8 - Messgrundlage "im Spiel hell" der Bauer
- Licht A trifft Kevins Bilder schlechter als Licht B (Abschnitt 1). Unter B sind nach oben/zur Kamera gedrehte, aufgehellte
  Unterseiten-Flaechen heller als unter A (Ursache von major 1). Zielwerte kuenftig auch mit Licht B pruefen.

## 4. Texturgroesse (Kevins Punkt 2, "hoeher aufgeloest")

Flimmer-Nachbau (`werkzeug/alias_mass.py`, `render/alias/`): 1 Abtastung je Pixel mit linearem Filter ohne Mipmaps (wie
`forschung_engine.md` 1.3) gegen Flaechenmittel 256 spp, Licht B, neues Netz. Fehler (sRGB-Stufen) / sichtbares Detail:
| Textur | Spielgroesse | halb so gross |
|---|---|---|
| alt 1024 | 0,81 / 2,98 | 1,65 / 3,51 |
| neu 1024 | 0,87 / 3,28 | 1,81 / 3,66 |
| neu 2048 (`textur/bilder/body_fell_2048.png`) | **1,92** / 4,28 | **3,42** / 4,10 |
2048 verdoppelt das Flimmern fuer +30 % (halb: +12 %) Detail; beim Herauszoomen ist das Flimmern fast so gross wie das Detail
(`e3_flimmern_1024_2048.png`). **1024 behalten ist optisch richtig.** Ob die Engine wirklich keine Mipmaps baut, habe ich nicht im Jar
geprueft (Beleg der Forschung B), nur die Folge nachgestellt.

## 5. Dateien (alle unter `_arbeit/baer_fell/pruef/optik/`)

- Blaetter `blaetter/`: Uebersicht `a0_uebersicht.png`; Licht A `b1`-`b19`; Nahbilder `c1`-`c11`; Licht B `d1`-`d5`; `e1_orange_karte.png`,
  `e2_body_textur_alt_neu.png`, `e3_flimmern_1024_2048.png`, `e4_textur_1024_512_256.png`; Ausschnitte `x_*.png`; Kalibrierung `kal_*.png`.
- Einzelbilder `render/alt/`, `render/neu/`, `render/alias/`; Kevin-Ausschnitte `ref/`; Dumps `dump/`; Logs `log/`.
- Werkzeuge `werkzeug/`: `render_optik.py`, `proj.py`, `pixel3d.py`, `blatt.py`, `auftrag*.py`, `kal_kevin.py`, `struktur.py`, `saett.py`,
  `naehte.py`, `knicke.py`, `kopf_texel.py`, `gewicht_fremd.py`, `leck_wirkung.py`, `alias_mass.py`; Blatt-Listen `blaetter*.json`.

Statisch/offline geprueft und gerendert, nicht gespielt. Kevin muss das Spiel neu starten, wenn die Dateien in die Test-Mod kommen.
