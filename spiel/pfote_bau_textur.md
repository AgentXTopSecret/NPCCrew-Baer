# Lauf baer-pfoten: Bauer Textur (09.11.2026)

Blender 5.2.3, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.** GPU nur RTX 4090 mit OptiX +
OptiX-Entrauscher (`werkzeug/render_optik.py` prueft das per assert), jeder Render ueber `werkzeug/gpu_render.sh` (Sperre `gpu.lock`,
fremdes Blender abwarten). Erster Anlauf bis ~20:22 (Abschnitte 0-4, Bau bis v11); ab ~19:53 lief ProjectZomboid, nach der alten Regel
deshalb keine Kontroll-Renders. **Zweiter Anlauf ab 20:23** nach Kevins Regelaenderung (09.11. ~20:25, "loesch die regel die hab ich nie
gemacht!": rendern auch bei laufendem Spiel; `gpu_render.sh` ohne Spiel-Pruefung, MD5 20f03821...): Kontroll-Renders 20:25-20:38, dabei
einen echten Fehler im Bild gefunden und nachgebessert (v12/v13, Abschnitt 3). Um 20:23 lief ProjectZomboid64.exe, um 20:39 nicht mehr.
Hinweis: Ich hatte Kevins Satz zuerst falsch gelesen und 20:23-20:25 die Spiel-Pruefung in `gpu_render.sh`/`warte_render.sh` kurz
wiederhergestellt; noch vor dem ersten Render zurueckgesetzt (`gpu_render.sh` wieder MD5 20f03821..., byte-gleich zur Fassung des Laufs).
Nichts in Test-Mod, NPC Crew oder `baer_fell` geschrieben, nichts committet; Originale `*_anim.py`/`*_fell.py` unveraendert (MD5
`textur/log/md5_originale_vorher.txt` = `md5_originale_nachher.txt`). Kevins Vorlagen nur angesehen und lokal in die Kontrollblaetter
gelegt, nichts davon in Textur oder Mod.

## 0. Kurz

1. **Neue Textur fuer die neuen Pfoten** (`baer/spiel/baer_textur_pfote.py`, Kopie von `baer_textur_fell.py`): neue Ansichten des neuen
   Hochmodells (26 Koerper + 9 Back-Pose, 2048, 96 Samples OptiX, 19:09-19:16), gebacken nach dem Weg von baer-fell (Ausgleich
   Blickrichtung, Farbabgleich, Back-Pose, Glaetten, 3D-Buesche, Deckel, keine Rost-Pfoten, Kopf/Krallen alt).
2. **Sohlen neu gemalt** auf den neuen Sohlen-Inseln nach dem Ballenplan des Netzes (`netz/sohle_layout.json`): hinten lange
   Sohlenplatte mit runder Ferse und fuenf Zehenballen im Bogen, vorn querliegender Handballen und fuenf Zehenballen; Leder hell-grau,
   leicht warm, gewoelbt (Mitte heller), schmale dunkle Furche, dazwischen und am Rand Fell (Straehnen, Fellkranz). Ueber eine 3D-Maske
   dazu der **Handwurzelballen** vorn (angehoben, ausserhalb der Insel) und der **Fersen-Hochzug** hinten. **Zehenrillen dunkler**.
3. **Fussruecken mit Fell**, Pfoten so dunkel wie baer-fell (Helligkeit je Hoehenband angeglichen), kleinere Haarbuesche an der Pfote.
4. **Farbe = baer-fell**: der Zwischenstand des Netz-Bauers ist auf dem Ruecken 15 % dunkler (Luma 77 statt 90); Bezug fuer Farbabgleich
   und Hals-Naht ist deshalb die fertige baer-fell-Textur (NCBearTest-Stand), per 3D-Naechster auf die neue UV uebertragen.
5. **Zweiter Anlauf, Nachbesserung v12/v13:** die Kontroll-Renders zeigten um jede Sohle einen **hellen Ring/Doppelstrich** (im Sitzen
   nah an der Ferse wie eine Schnittkante, von unten als heller Umriss). Ursache gemessen: gebackenes Fell 1-3 cm ueber dem Boden Luma
   79 gegen 49-64 darueber, Inselrand Luma 108-114, UV-Polster um die Insel hell. Behoben: Fell unter 5 cm hoechstens 1,15 x Fell
   4-8 cm desselben Beins, Inselrand-Mischung ebenso gedeckelt, Polster neu aus der gemalten Insel gefuellt. Jetzt endet die Sohle in
   Fell (Bilder `bilder/textur_6_nah.png`, `textur_10_abgesaegt.png`). Endstand = v13 = `pfote`.
6. **Feste Regeln gemessen** (Abschnitt 4): GLB byte-gleich zum Netz-Bauer, Deer byte-gleich, Kopf-Texel bit-gleich, Krallen beim
   Abtasten bit-gleich, Maul-Flecken bit-gleich, Body 1024 / WorldItems 2048 RGB wie bisher; Unterseite, Farbe, Straehnen am Rumpf wie
   vorher. Ergebnis liegt in `mod/42/media/textures/` (vorher dort der Platzhalter des Netz-Bauers, gesichert in `textur/vorher/textures/`).

## 1. Was gebaut ist

`baer/spiel/baer_textur_pfote.py` (Kopie, Original `baer_textur_fell.py` unveraendert; MD5 der Kopie jetzt 6f0f389e..., erster Anlauf
e202673c...):
- Hilfen/Hochmodell aus `baer_export_pfote.py` (-> `baer_quelle_pfote.py`), Netz `netz/lowpoly_pfote.blend`, Ausgaben `textur/`,
  Ordner wie bisher per `BAER_TX_DIR`, `BAER_FELL_NETZ`, `BAER_TX_ANS`, neu `BAER_TX_ZWISCHEN` (Bezug).
- **Haarrichtung an der Pfote** wie das Pfotenhaar des Hochmodells (`baer_quelle_pfote.py:2018-2022`, Richtung wie `wachse` :702-725:
  unter Spiel-z 0,10 nach vorn/unten), damit der Ausgleich der Blickrichtung an der Pfote stimmt.
- **Sohlen** (`sohlen_malen`, `leder_farbe`, `ballen_q3`, `handwurzel_q`, `fell_2d`): Ballenplan aus `netz/sohle_layout.json`
  (Vieleck + Ellipsen, `ballen_q` des Netz-Bauers, Rand-Skala 0,012 gleich); auf der Insel ohne Hoehen-Strafe (das Netz ist dort grob,
  2 cm Raster - sonst gezackte Ballenkanten, v2); ausserhalb der Insel 3D-Fortsetzung: Ballen nur unten (Normale nach unten, Hoehe
  0,5-1,0 cm, Zehenballen bis 1,6 cm), hinten Fersen-Hochzug hinter x -0,535 bis 0,6-1,1 cm Hoehe, vorn Handwurzelballen als Kappe der
  Kugel aus `spez/pfoten_plan.json` (Mitte 0,265 / +-0,258 / 0,0475, r 0,029; Punkte nahe der Kugel, Normale von der Mitte weg,
  untere/hintere Haelfte). Fell auf der Insel: kurze Straehnen vom Ballen weg, am Inselrand weich in die gebackene Farbe.
- **Zehenrillen**: Verdeckung im Kleinen (Reichweite 3 cm Spielmass, 48 Strahlen) an den 2.647 Pfotenpunkten unter 9 cm, bis 45 % dunkler.
- **Kleine Buesche an der Pfote** (unter 14 cm: 1,2 cm lang statt ~3,4 cm).
- **Pfoten-Helligkeit je Hoehe** an baer-fell (`PF_ABGLEICH`, Ziel = Median-Luma der baer-fell-Textur je Band, unten 62 statt 72),
  **Uebergang Knie/Ellbogen** (Spiel-z 0,27-0,50) oertlich an baer-fell, **waagerechte Baender am neuen Wulst** (dicker Rumpf ueber
  duennem Bein) je Bein und 45-Grad-Sektor eingeebnet, dort kaum nachgeschaerft.
- **Neu im zweiten Anlauf (v12/v13):**
  - `RAND_K = 1,15` (`baer_textur_pfote.py:465`), **Sohlenrand-Deckel** (:1329-1346, v12): geglaettete Log-Luma (6 Runden ueber das Netz)
    von Rumpf und Sohlen-Insel unter 5 cm hoechstens Median-Fell 4-8 cm des Beins x 1,15; nur abdunkeln, Straehnen bleiben
    (Log: 220.582 Texel, Faktor p5/p50 0,53/0,67).
  - **Inselrand** in `sohlen_malen` (:845-850, v13): die Mischung "am Inselrand weich in die gebackene Farbe" nimmt die gebackene Farbe
    nur bis Pfotenfell x 1,15 hell (Farbton und dunklere Straehnen bleiben).
  - **UV-Polster** (:1405-1410, v13): Texel ohne Netz bis 10 Texel um die Sohlen-Inseln neu aus den gemalten Insel-Texeln gefuellt
    (38.619 Texel); vorher stammte das Polster aus dem Fuellen VOR dem Sohlenmalen (hell) und wirkte ueber das 2x2-Mittel der 1024er.
    Kopf-/Krallen-Texel werden danach wie bisher aus dem alten Stand gesetzt, bleiben also bit-gleich.
- Werkzeuge `_arbeit/baer_pfote/textur/werkzeug/`: `lauf_textur.sh` (Kette backen/glb/deer), `fell_uebertrag.py` (Bezug),
  `ansichten_beide.sh`, `auftrag_textur.py`, `blatt_textur.py`, `uebersicht.py`, `textur_pruef.py` (feste Regeln), `mess_textur.py` und
  `mess_bild.py` (Kopien, nur Pfade), `warte_render.sh` (erster Anlauf, beendet, nicht mehr benutzt), `block_pfoten_malen.py`
  (Bau-Schritt); neu `zellen_blatt.py` (Blatt "abgesaegtes Bein?"), `pfote_luma.py` (Pfoten-Luma je Hoehe, Rost).

## 2. Ansichten (GPU)

`textur/ansichten_auftrag.json` (26: k_h*, k_o*, k_top, k_u*, k_bot, u_s*) und `textur/ansichten_pose_auftrag.json` (9, Back-Pose),
Fell-Variante wie baer-fell (Beine weniger Melanin, Haar rauer, Zehenhaar +0,12 heller). Helligkeit je Ansicht wie baer-fell
(Verhaeltnis 0,94-1,18, hinten/unten etwas heller wegen der duenneren Hinterbeine; `textur/ansichten/helligkeit_pfote.json`).
Log `textur/log/ansichten.log`, `ansichten_pose.log`, `ansichten_beide.txt` (19:09:44-19:16:28, RC 0/0). Im zweiten Anlauf geprueft:
gueltig (Netz seitdem unveraendert, GLB des Netz-Bauers a6099029... von 18:43), nicht neu gerendert.

## 3. Runden (alle selbst angesehen)

| Version | Aenderung | Befund im Bild |
|---|---|---|
| v1 | Kopie + neue Ansichten + Sohlen nach Plan | Ruecken Luma 77 statt 90: Farbabgleich am (dunkleren) Zwischenstand |
| v2 | Bezug = baer-fell-Textur uebertragen (`zw_fell_2048.png`) | Farbe wie baer-fell; Sohle eine flache graue Platte mit gezackten Kanten, Zehenballen vom Fellkranz verdeckt (`textur/bilder/v2_sohle_uv.png`, `textur_v2_6_nah.png`) |
| v3/v4 | keine Hoehen-Strafe auf der Insel, Woelbung, Risse 0,14 -> 0,06, Fell als Straehnen statt Wellen | Zehenballen und Platte klar; v3 hatte sichtbare Wellenlinien (Querfalten mit Welle) -> v4 ohne (`textur/bilder/v3_sohle_uv.png`, `v4_sohle_uv.png`) |
| v5 | Ferse ab x -0,535 (kein Flaschenhals), Inselrand in die gebackene Farbe | Sitzen wie Kevins Foto; Pfotenfell hell-beige ("Socken", Luma 71-101 gegen baer-fell 50-72) |
| v6 | Pfoten-Helligkeit je Hoehe an baer-fell | Pfoten braun wie der Koerper; feine dunkle Querlinie oben am Vorderbein |
| v7-v10 | Uebergang 27-50 cm an baer-fell, Band-Einebnung, weniger Nachschaerfen | Linie schwaecher (Profil vorn 49 -> 53 gegen 60 daneben), ganz weg ist sie nicht (Abschnitt 7) |
| v11 | Fersen-Hochzug nur bis 0,6-1,1 cm (vorher 1,1-1,7) | gezackte Grenze an der Ferse im Liegen weg. **Zweiter Anlauf, volle Kontroll-Renders (`textur/render/v11`, 95 Bilder):** heller Ring um jede Sohle - im Sitzen nah an der Ferse ein heller Doppelstrich mit Kerbe (wie eine Schnittkante), von unten ein heller Umriss um Sohle und Pranke (`textur/render/v11/sitzen_HL_vorn_nah_tex.png`, `gehen_HL_nah_tex.png`, `ruhe_HL_unten_tex.png`). Gemessen (Ruhepose, Rumpf ohne Sohle): 0-1 cm Luma 102, 1-3 cm 79, 3-5 cm 62; Inselrand (0-3 Texel) 108-114 |
| v12 | Sohlenrand-Deckel auf dem gebackenen Fell (RAND_K 1,15) | 1-3 cm 79 -> 61; Ring im Bild nur wenig schwaecher (`textur/render/v12`): der Strich sitzt am Inselrand (Mischung in die helle gebackene Farbe, noch 82-94) und im hellen UV-Polster |
| **v13 = Endstand** | Inselrand-Mischung gedeckelt, UV-Polster neu gefuellt | Inselrand 63-72 (vorher 108-114); im Sitzen endet die Sohle in braunem Fell, kein Strich, keine Kerbe; von unten kein heller Umriss; Liegen/Spielgroesse/8 Azimute ohne Rueckschritt (`textur/render/v13`, `textur/bilder/textur_v13_*.png`) |

Der Bake ist deterministisch: `NCBear_v13_2048.png` = `NCBear_pfote_2048.png` (94212c2e...), Body 1024 je 4ae60e6c..., ~100 s CPU.

## 4. Feste Regeln (gemessen; `textur/mess/textur_pruef_pfote.json`, `mess_textur_pfote.txt`, `mess_bild_pfote.txt`, `log/kampf_pfote.log`, `log/tier_pfote.log`)

| Regel | Ergebnis |
|---|---|
| GLB mit der neuen Textur | `textur/glb_pfote/.../NCBear.glb` **a6099029...** = `mod/.../NCBear.glb` des Netz-Bauers (byte-gleich, das GLB enthaelt keine Bilder; KAMPF_OK) |
| Deer | `textur/tier_pfote/.../NCBearDeer.glb` **9246fa53...** = `mod/.../NCBearDeer.glb` (byte-gleich, Original `baer_tier_anim.py`; TIER_OK) |
| Kopf-Texel | 858.273 von 858.273 (2048) und 212.944 von 212.944 Pixel (1024) bit-gleich zu NCBearTest (033d3705 / c2d6c8cc) |
| Krallen | an 2.496 Krallen-Ecken und allen Abtastpunkten in den Krallen-Dreiecken bilinear bit-gleich (2048 und 1024, max. Abweichung 0,0); 5 von 264 Krallen-Texeln (2048) liegen ausserhalb jedes Abtastfelds und sind anders (Rumpf-Insel-Rand, ohne Wirkung; wie v11) |
| Maul-Flecken | 1024er Flecken samt 4 px Saum bit-gleich zu NCBearTest; "Flecken Gaumen/Zunge/Zahn frei" (Log) |
| PNG | Body RGB 1024x1024 (4ae60e6c...), WorldItems RGB 2048x2048 (94212c2e...), wie NCBearTest |
| Unterseite im Spiel-Licht (`mess_textur.py`, relativ Ruecken) | Achsel 0,52, Leiste 0,53, Innenbein vorn 0,45 / hinten 0,48, Bauch 0,55, Hinterteil 0,59, Brust 0,51, Kehle 0,69 (Soll >= 0,40; gleich v11; baer-fell 0,55/0,55/0,43/0,43/0,54/0,63/0,55/0,70) |
| Farbe | Ruecken Luma 90 (baer-fell 91), Kopf/Hals-Naht Farbsprung Mittel 8,3 / 90 % 17,7 (baer-fell 7,9 / 16,6) |
| Rost-Pfoten | gesaettigte Fellpixel (s > 0,62, v > 0,30) unter 22 cm: 0,02 % (`pfote_luma.py`; baer-fell 0,00 %, Zwischenstand 0,88 %); in Spielgroesse-Bildern 0,00-0,02 % |
| Sohle | Ballen-Kuppe Luma 119-121, Furche 41 (sRGB); Sohle im Spiel 0,73 vorn / 0,84 hinten der Rueckenhelligkeit (v11 0,78/0,86; baer-fell 0,56) |

Pfoten-Luma je Hoehe (Median, Rumpf ohne Sohle; Baender 0-4-8-12-20-30-40-55 cm):
baer-fell 72 / 59 / 50 / 60 / 61 / 64 / 74 - Zwischenstand Netz-Bauer 78 / 79 / 76 / 67 / 66 / 74 / 69 - v11 73 / 57 / 52 / 59 / 58 / 64 / 72 -
**neu (v13) 61 / 57 / 52 / 59 / 58 / 64 / 72** (Ziel 0-4 cm 62; der hoehere baer-fell-Wert kam vom hellen Fellkranz der Saeule).
Feiner: 1-3 cm 79 -> 61, 3-5 cm 62 -> 60; 0-1 cm 101 sind die Ledertexel der Ballenkanten/Fersen-Hochzug.

**Straehnen** (`textur/werkzeug/mess_bild.py`, gleiche Kameras wie die baer-fell-Nachbesserung, Spielgroesse, Licht B; alt = baer-fell,
neu = Endstand; `textur/mess/mess_bild_pfote.txt`): Kontrast Ruecken 0,070 / 0,070, Flanke 0,079 / 0,080, Hinterteil 0,079 / 0,075,
Vorderbein 0,080 / 0,078, Hinterbein 0,067 / 0,053; Kohaerenz Ruecken 0,660 / 0,658, Flanke 0,595 / 0,598; Aufrichten Schenkel
Kohaerenz 0,669 / 0,455. Leisten-Band/Brust 1,35 / 1,22 (baer-fell 1,45 / 1,34, also nicht heller). Rumpf wie baer-fell; an den Beinen
weniger Straehnen-Kontrast (gleich in v11, also nicht von v12/v13; Abschnitt 7).

## 5. Kontrollbilder (Spiel-Licht B, `werkzeug/render_optik.py`, offline)

Renders des Endstands: `textur/render/v13/` (95 Bilder, Body 4ae60e6c... = Endstand) und `textur/render/pruef_final/` (70 Bilder,
Kameras der baer-fell-Pruefung). Alt = NCBearTest-Stand (baer-fell), Ton = ohne Textur (Netz-Bauer, Netz unveraendert).
- `bilder/textur_0_uebersicht.png` - Kevins Vorlagen | Sitzen von vorn, Hinterfuss im Sitzen nah, Aufrichten, Stehen vorn, Pranke von unten (alt | Ton | Textur)
- `bilder/textur_1_stehen_gehen.png` - Stehen, Gehen je Pfote nah und Spielwinkel (alt | Ton | Textur)
- `bilder/textur_2_sitzen_aufrichten.png` - Sitzen, Aufrichten je Pfote (alt | Ton | Textur)
- `bilder/textur_3_liegen.png` - Liegen je Pfote
- `bilder/textur_4_zusatz.png` - Rennen seitlich/hinten, Gehen-Schwung, Sitzen von vorn, SitDown, Swipe, Aufrichten von hinten
- `bilder/textur_5_ruhe.png` - Ruhepose je Pfote: Seite, vorn, unten, schraeg
- `bilder/textur_6_nah.png` - Hinterfuss im Sitzen von vorn (wie Kevins Hauptvorlage), Ferse im Aufrichten, Pranke von unten, Liegen (Ton | Textur)
- `bilder/textur_7_sitzen_8_azimute.png` - Sitzen in 8 Spielwinkeln (el 30)
- `bilder/textur_8_spielgroesse.png` - so klein wie im Spiel (alt | neu)
- `bilder/textur_9_sohlen_uv.png` - die Sohlen in der Textur, alt | neu
- `bilder/textur_10_abgesaegt.png` - dieselben Kameras wie die baer-fell-Bilder hinter Kevins Beschwerde, baer-fell | neu (Abschnitt 6)
- Zwischenstaende: v11 als Einzelbilder `textur/render/v11/` und `pruef_v11/`, Blaetter `textur/bilder/textur_v12_*.png`,
  `textur/bilder/textur_v13_*.png` (= Endstand-Blaetter).

Selbst angesehen (Read auf die PNG): Blaetter 0, 1, 2, 3, 4, 6, 7, 8, 9, 10 und Einzelbilder (Sitzen nah HL/HR, Gehen von unten,
Aufrichten Ferse/Pranke unten, Liegen, Ruhe unten) in v11, v12 und v13.

## 6. "Abgesaegtes Bein?" (eigene Sicht, Textur-Bilder neben Ton)

`bilder/textur_10_abgesaegt.png` (gleiche Kamera wie Kevins Beschwerde-Bilder `baer_fell/pruef/optik/blaetter/b6_sit_fuss.png`,
`c4_pfoten.png`, `x_B_rear_pranken.png`):
- **B_sit_fuss_nah / sit_fuss_nah (Sitzen, Hinterfuss):** baer-fell runde Saeule mit dunkler Kappe, Sohle nur gemalt, Zehen als
  Klumpen oben. Neu: der Unterschenkel geht in einen langen Fuss ueber, Sohle als lange helle Platte, Zehen mit Krallen oben, Ferse
  unten rund mit Fellrand. Im Ton (`sit_fuss_nah_ton`) ebenso: Saeule -> Fuss. Liest sich als Baerenfuss.
- **pfote_hinten_nah (Stehen):** baer-fell Saeule mit Zehenwulst; neu Ferse hinten, Fussruecken mit Fell, Zehen vorn.
- **pfote_vorn_nah / rear_pranken_nah:** neu schmaleres Handgelenk, Pranke mit Zehen und langen Krallen; von vorn oben gut. Von unten
  (`textur_6_nah.png`, aufrichten_VL_unten) wirkt die Pranke kastig - das ist die Form (Ton genauso), die Textur verdeckt es nicht.
- **sohle_HL_spiel / idle_sohlen / idle_unten:** baer-fell dunkle runde Scheibe; neu lange Hintersohle mit Zehenreihe, vorn
  Handballen mit Zehen; heller Rand-Umriss seit v13 weg.
- **Aufrichten** (`textur_2`, `textur_6`): steht auf ganzen Hinterfuessen, Ferse und Zehen sichtbar. **Gehen/Rennen/Liegen:** Pfoten
  lesbar, keine helle Kappe mehr.
Mein Urteil (statisch, nicht gespielt): im Ton- und im Texturbild vier Pfoten statt Saeulen; die Textur verdeckt keine falsche Form,
die verbliebenen Formschwaechen (Pranke unten kastig) sieht man im Ton wie mit Textur.

## 7. Offen / Schwaechen

- **Pranke von unten kastig** (Form, Netz-Bauer Abschnitt 1/3); vorn von unten zusaetzlich ein dunkler Fellstreifen quer zwischen
  Handwurzelballen und Handballen (`textur/render/v13/gehen_VL_nah_tex.png`) - so gemalt (Fell zwischen den Ballen), wirkt aber wie eine
  Querlinie. Nur von unten sichtbar.
- **Hintersohle sehr gleichmaessig** hell (eine Platte ohne Zeichnung), Zehenballen kleiner als auf Kevins Foto und dunkel umrandet.
- **Straehnen an den Beinen** schwaecher als baer-fell (Hinterbein-Kontrast 0,053 statt 0,067, Schenkel-Kohaerenz 0,46 statt 0,67);
  schon in v11. Moeglich, dass die festen Messfenster aus baer-fell bei den duenneren Beinen Hintergrund/Rumpf treffen - ungeprueft.
- Feine dunkle Querlinie oben am Vorderbein (Wulst) schwaecher als in v6, nicht ganz weg (Abschnitt 3).
- Pfotenfell unten jetzt dunkler als baer-fell (0-4 cm 61 statt 72; gewollt, Ziel 62) - im Spiel auf dunklem Boden ungeprueft.
- 5 von 264 Krallen-Texeln (2048) anders, ausserhalb jedes Abtastfelds (wie v11, ohne Wirkung).
- **Sitzen:** Hinterfuss schwebt 0,8 cm (Netz-Bauer, nur mit Clip-Aenderung C2) - Textur kann das nicht beheben.
- Nur offline mit Spiel-Licht B gerendert, **nicht gespielt**; Mipmaps/Texturgroessen-Option (Vorgabe deckelt auf 256) im Spiel ungeprueft.
- Die Test-Mod NCBearTest ist unveraendert; uebernehmen nur auf Kevins Wort (Integrator).

## 8. Neu bauen (aus `_arbeit/baer_pfote/`)
```
bash textur/werkzeug/ansichten_beide.sh                       # GPU ~7 min (gpu_render.sh je Auftrag)
"C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe" -b --factory-startup --python textur/werkzeug/fell_uebertrag.py -- \
   <abs>/textur/mess/texel_pfote.npz <abs>/../baer_fell/fix/textur/mess/texel_fix.npz <NCBearTest WorldItems/NCBear.png> \
   <abs>/netz/zwischen_pfote/42/media/textures/WorldItems/NCBear.png <abs>/textur/zw_fell_2048.png   # Bezug (texel-npz aus einem Bake)
bash textur/werkzeug/lauf_textur.sh pfote backen glb deer      # ~1,7 + 0,2 + 0,1 min CPU
python textur/werkzeug/textur_pruef.py textur/NCBear_pfote_2048.png textur/glb_pfote/42/media/textures/Body/NCBear.png textur/mess/texel_pfote.npz
python textur/werkzeug/mess_textur.py "neu=textur/NCBear_pfote_2048.png|textur/mess/texel_pfote.npz"
python textur/werkzeug/pfote_luma.py textur/NCBear_pfote_2048.png textur/mess/texel_pfote.npz
python textur/werkzeug/auftrag_textur.py NAME <Body-1024>; bash werkzeug/gpu_render.sh <abs>/werkzeug/render_optik.py <abs>/textur/render/NAME/auftrag.json LOG
python textur/werkzeug/blatt_textur.py NAME final; python textur/werkzeug/uebersicht.py NAME textur/NCBear_pfote_2048.png
# Pruef-Kameras: textur/render/pruef_final/auftrag.json (= pruef_v11 mit Endstand-Body), dann
python textur/werkzeug/zellen_blatt.py pruef_final; python textur/werkzeug/mess_bild.py textur/render/pruef_final
cp textur/glb_pfote/42/media/textures/Body/NCBear.png mod/42/media/textures/Body/NCBear.png
cp textur/NCBear_pfote_2048.png mod/42/media/textures/WorldItems/NCBear.png
```

## 9. Dateien

Alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/`:
- Skript: `baer/spiel/baer_textur_pfote.py` (MD5 6f0f389e...)
- Ergebnis-Mod: `_arbeit/baer_pfote/mod/42/media/textures/Body/NCBear.png` (1024, 4ae60e6c...), `.../textures/WorldItems/NCBear.png`
  (2048, 94212c2e...); daneben unveraendert vom Netz-Bauer `models_X/Skinned/NCBear.glb` (a6099029...), `NCBearDeer.glb` (9246fa53...),
  `models_X/WorldItems/NCBear.fbx` (ab35c415...). Platzhalter vorher: `_arbeit/baer_pfote/textur/vorher/textures/`.
- Textur-Arbeit: `_arbeit/baer_pfote/textur/` (`NCBear_pfote_2048.png`, `NCBear_v1..v13_2048.png`, `glb_pfote/`, `glb_quelle_pfote/`,
  `tier_pfote/`, `glb_v*/`, `ansichten/`, `ansichten_pose/`, `zw_fell_2048.png`, `NCBear_kopf_variante.png`)
- Messungen: `_arbeit/baer_pfote/textur/mess/` (`textur_pruef_pfote.json`, `textur_pruef_v11..v13.json`, `mess_textur_pfote.txt`,
  `mess_bild_pfote.txt`, `mess_bild_v11.txt`, `texel_pfote.npz`, `backen_pfote.json`, `kampf_bericht_pfote.json`)
- Logs: `_arbeit/baer_pfote/textur/log/` (`backen_pfote.log`, `kampf_pfote.log`, `tier_pfote.log`, `render_v11/v12/v13.log`,
  `render_pruef_v11.log`, `render_pruef_final.log`, `md5_originale_vorher.txt`, `md5_originale_nachher.txt`)
- Renders: `_arbeit/baer_pfote/textur/render/` (`v13/` und `pruef_final/` = Endstand, `v11/`, `v12/`, `pruef_v11/` zum Vergleich)
- Kontrollbilder: `_arbeit/baer_pfote/bilder/textur_0_uebersicht.png` ... `textur_10_abgesaegt.png`; Zwischenstaende
  `_arbeit/baer_pfote/textur/bilder/`
- Werkzeuge: `_arbeit/baer_pfote/textur/werkzeug/` (neu: `zellen_blatt.py`, `pfote_luma.py`)
