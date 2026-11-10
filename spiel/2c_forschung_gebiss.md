# NC Bear 2c -- Forschung Gebiss + Zunge (10.11.2026)

Nur Forschung: nichts am Modell gebaut, nichts in die Test-Mod oder nach NPC Crew geschrieben, nichts committet.
**Statisch/offline gemessen und gerendert, nicht gespielt.** Alle Zahlen bei Groesse 1,0.
Gemessen am fertigen GLB aus baer-pfoten (`_arbeit/baer_pfote/mod/42/media/models_X/Skinned/NCBear.glb`, MD5 5066fa67...,
gleich der Datei in NCBearTest; Dump `forschung/gebiss/dump/heute.txt`, MD5 ab53dabdf89345d0f0aad9f2b6cd6b85).

## 0. Kurzfassung

- Heute: Maul-Inneres = 330 Dreiecke (Gaumen 141, Zunge 141, vier Eckzaehne 48). Die Eckzaehne sind gerade Kegel, 3,0 / 2,8 cm
  lang, 2,7 cm hinter der Lippe versteckt, alle Zahn-Dreiecke auf EINEM Texel. Keine Schneidezaehne, keine Backenzaehne, kein
  Zahnfleisch. Zunge und Gaumen sind zwei flache Faecher-Blaetter (je 17,2 x 20,7 cm, 3,9 px/cm). Lippen fellbraun bis zur Kante.
- Das Maul geht weit genug auf (Rear 38 Grad = 21,1 cm Spalt vorn; Fotos: geschaetzt 12-16 cm). Der Clip ist nicht das Problem,
  die Form ist es: eckige Kasten-Oeffnung, Mini-Zaehne, Zungen-Rechteck.
- Ein gutes Gebiss passt ohne Clip-Aenderung: starr an Head (oben) und Jaw (unten). Probe am geschlossenen Maul: obere Eckzaehne mit
  4,6 cm Krone bleiben unsichtbar bei a 0,440-0,450 / |b| 4,4-5,0 cm (mind. 2,1 cm innen von der Seitenlippe, 10 Grad nach innen
  geneigt); untere bei a 0,462 / |b| 3,4-4,0 cm bis 4,8 cm Krone. Direkt hinter der Lippenkante stechen sie durch.
- Dreiecke: frei 574 + wiederverwendbar 330 = 904. Vorschlag 874 (Sparfassung 700). Achtung: das Budget teilt sich mit den Beinen.
- Textur: groesstes freies Rechteck 196 x 108 px bei (269, 0) -- die Flecken koennen wachsen, ohne eine Insel zu verschieben.
- Kette: nur Kopie von `baer_kampf_pfote.py` (Stufe `glb`) + `deer` + Pruefer; `netz` und `gewichte` muessen nicht neu laufen.
- Nicht ohne Clip-/Knochen-Aenderung: echtes Hochziehen der Lefzen. Offen: Kasten-Mundwinkel und der "Zipfel" (gespannte
  Wangenhaut, Dehnung x3,9) -- das sind Aussenhaut-Gewichte, die Spezifikation muss sagen, ob sie zur Maske gehoeren.

## 1. VORLAGE

### 1.1 Kevins Vorlage (nur angesehen)

`baer/begleiter/kevin_bruellen_vorlage.webp` (Bildschirmfoto einer Bildersuche, Stockfotos). Ansehkopie nur unter
`_arbeit/baer_2c/referenz/kevin_bruellen_vorlage.png` (2000 x 1088) und acht vergroesserte Ausschnitte
`_arbeit/baer_2c/referenz/vorlage_ausschnitte.png`. Nichts davon in Modell, Textur oder Mod.

Was man auf den Fotos sieht (Beobachtung, keine Messung):
- **Obere Eckzaehne** an den vorderen Ecken des Oberkiefers, lang, spitz, leicht nach hinten und aussen gebogen, elfenbein
  bis gelblich, an der Basis dunkler.
- **Schneidezaehne:** sechs kleine in einer Reihe zwischen den Eckzaehnen, oben wie unten; die aeusseren groesser.
- **Untere Eckzaehne** stehen enger und VOR den oberen (greifen bei geschlossenem Maul in die Luecke davor).
- **Backenzaehne:** niedrige, hoeckrige Reihe hinter einer Luecke; nur angedeutet sichtbar.
- **Lefzen:** schwarz, nass glaenzend, rahmen die ganze Oeffnung; Oberlippe hochgezogen, Unterlippe haengt, innen rosa.
- **Zahnfleisch/Gaumen:** rosa bis mauve-grau, Rachen dunkel.
- **Zunge:** rosa-mauve, breit, flach, liegt tief zwischen den unteren Zahnreihen, runde Spitze kurz hinter den unteren
  Schneidezaehnen, Raender leicht hoch. Kein Klumpen, keine Rolle.
- **Oeffnung:** hohes Oval/U, Mundwinkel weit hinten mit einer Hautfalte (Wangenhaut) -- kein Kasten.

Schaetzung aus den Fotos (Pixelverhaeltnisse an kleinen Vorschaubildern, +-25 %): sichtbare obere Eckzahn-Krone ~ 0,5 x Abstand
der oberen Eckzahn-Spitzen; Bruell-Oeffnung (obere zu unteren Schneidezaehnen) ~ 1,7-2,3 x Eckzahn-Abstand.

### 1.2 Quellen (nur gelesen, nichts gespeichert oder kopiert)

| Nr | Aussage | URL |
|---|---|---|
| Q1 | Zahnformel I 3/3, C 1/1, P 4/4, M 2/3 = 42; erwachsenes Maennchen 2,0 m lang, Schulter 1,0 m | https://www.depts.ttu.edu/nsrl/mammals-of-texas-online-edition/Accounts_Extinct_Carnivora/Ursus_arctos.php |
| Q2 | Schaedel Alaska erwachsen: Condylobasallaenge 360 mm, Jochbogenbreite 230 mm; Formel 3.1.2-4.2 / 3.1.2-4.3 | https://www.skullsite.co.uk/Brbear/brbear.htm |
| Q3 | Schaedel russ. Maennchen 31,5-45,5 cm lang, Jochbogen 17,5-27,7 cm; Schneide- und Eckzaehne gross, untere Eckzaehne stark gebogen; erste drei obere Backenzaehne verkuemmert; Drohgesicht: Maul offen, Oberlippe gekraeuselt, Unterlippe haengt | https://en.wikipedia.org/wiki/Brown_bear |
| Q4 | "Distance between the canines is from 6 to 8 cm."; Kopf-Rumpf 1-2,8 m, Schulter 90-150 cm | https://animaldiversity.org/accounts/Ursus_arctos/ |
| Q5 | Keine Reisszaehne, lange Eckzaehne, erste drei Praemolaren klein oder fehlend, breite flache Molaren; erster unterer Molar > 20,4 mm lang, > 10,5 mm breit | https://ielc.libguides.com/sdzg/factsheets/brownbear/characteristics |
| Q6 | 42 Zaehne; je Kiefer 6 Schneidezaehne, 2 Eckzaehne; oben 8 P + 4 M, unten 8 P + 6 M; beim Drohen ziehen Schnauzenmuskeln die Oberlippe hoch | https://a-z-animals.com/blog/grizzly-bear-teeth/ |
| Q7 | Flache Mahl-Molaren und -Praemolaren | https://www.fws.gov/story/drilling-down-bear-dentition |
| Q8 | Zunge: fuenf Papillen-Arten, vier Baerenarten aehnlich (Pastor et al. 2011, nur Zusammenfassung) | https://zendy.io/title/10.1002/jemt.20975 |
| Q9 | Abguss "grizzly canine 11,5 cm" = ganze Laenge MIT Wurzel (Haendlerangabe, keine Kronenhoehe) | https://www.skullsunlimited.com/products/replica-grizzly-bear-tooth-mo-35 |

Nicht gefunden (bleibt Schaetzung): Kronenhoehe des Braunbaer-Eckzahns, Masse der Zunge, Zahl der Gaumenleisten beim Baeren.
Nur als Suchtreffer-Schnipsel gesehen, nicht geoeffnet: Hoehlenbaer (nicht Braunbaer) obere Eckzahn-Breite Maennchen
17,3-20,5 mm; Hund 6-10 quere Gaumenleisten; Zungenstudie asiatischer Baeren "keine Mittelfurche, kein Zungenwulst".

### 1.3 Masstabelle: Natur -> unser Kopf

Massstab: unser Kopf ist 51,4 cm lang (Schnauzenachse, echt gemessen), ein grosses Maennchen hat mit Weichteilen ~44 cm
(Schaedel 36-45 cm, Q2/Q3; Weichteil-Zuschlag geschaetzt) -> Faktor 1,17. Gegenprobe: unser Eckzahn-Abstand oben 9,0 cm gegen
8 cm (Q4) -> 1,12. **Gerechnet mit f = 1,15 (Spanne 1,1-1,2) -- der Faktor selbst ist eine Schaetzung.**

| Mass | Natur (grosses Maennchen) | Quelle | bei uns (x 1,15) | heute im Modell |
|---|---|---|---|---|
| Zahnformel | I 3/3, C 1/1, P 4/4, M 2/3 = 42 | Q1, Q6 | je Seite 3 Schneide-, 1 Eckzahn; Backenzaehne angedeutet | 4 Eckzaehne, sonst nichts |
| Abstand obere Eckzaehne | 6-8 cm | Q4 | 6,9-9,2 cm | 8,8 cm (Mitten), 9,1 cm (Spitzen) |
| Abstand untere Eckzaehne | enger als oben, ~5-6,5 cm | SCHAETZUNG (Fotos) | 5,8-7,5 cm | 7,7-8,1 cm |
| Obere Eckzahn-Krone sichtbar | 3-4 cm | SCHAETZUNG (Fotos x Q4) | 3,5-4,6 cm | 3,0 cm ganz, davon 1,5-2 cm sichtbar |
| Untere Eckzahn-Krone | 3-3,5 cm, stark gebogen | SCHAETZUNG; Biegung Q3 | 3,5-4,0 cm | 2,8 cm, gerade |
| Eckzahn-Basis (laengs x quer) | ~2,0 x 1,5 cm | SCHAETZUNG (Hoehlenbaer 1,7-2,1 cm quer als Obergrenze) | 2,3 x 1,7 cm | Kreis r 0,75 / 0,70 cm |
| Eckzahn-Kruemmung | oben leicht (~30-35 Grad Bogen), unten stark (~45 Grad) | SCHAETZUNG; Q3 | gleich | 0 Grad |
| Schneidezaehne oben, je Zahn | ~0,8-1,1 cm breit, 1,0-1,4 cm hoch, I3 am groessten | SCHAETZUNG (Fotos) | 0,9-1,3 breit, 1,1-1,6 hoch | fehlen |
| Schneidezaehne unten, je Zahn | ~0,7-0,9 cm breit, 0,8-1,0 hoch | SCHAETZUNG (Fotos) | 0,8-1,0 breit, 0,9-1,1 hoch | fehlen |
| Luecke hinter dem Eckzahn | ~2-3,5 cm (P1-P3 klein oder fehlend) | Q3, Q5; Laenge SCHAETZUNG | 2,5-4 cm | -- |
| Unterer M1 | > 2,04 cm lang, > 1,05 cm breit | Q5 | 2,4-2,6 x 1,2-1,3 cm | fehlt |
| Backenzahnreihe oben (P4, M1, M2) | ~1,6 / 2,3 / 3,5 cm | SCHAETZUNG (aus Q5 hochgerechnet) | 1,8 / 2,6 / 4,0 cm (Reihe ~8,6 cm) | fehlt |
| Backenzahnreihe unten (p4, m1-m3) | ~1,3 / 2,3 / 2,4 / 1,9 cm | Q5 fuer m1, Rest SCHAETZUNG | 1,5 / 2,6 / 2,8 / 2,2 cm (Reihe ~9,1 cm) | fehlt |
| Kronenhoehe Backenzaehne | ~0,9-1,0 cm, flach | Q5, Q7; Hoehe SCHAETZUNG | 1,0-1,2 cm | fehlt |
| Bruell-Oeffnung vorn | 12-16 cm | SCHAETZUNG (Fotos x Q4) | 14-18 cm | 21,1 cm bei 38 Grad (Rear) |
| Zunge | breit, flach; ~6-7 cm breit, 1-1,3 cm dick | SCHAETZUNG (Fotos); Q8 nur Oberflaeche | 7-8 cm breit hinten, 5-6 cm an der Spitze, 1,2-1,5 cm dick, Spitze 1,5-2 cm hinter den unteren Schneidezaehnen | Blatt 20,7 cm breit, 0 cm dick |
| Gaumenleisten | Baer nicht gefunden (Hund 6-10) | SCHAETZUNG | 7-8, nur gemalt | 7 gemalte Rippen |
| Lefzen | schwarz, nass, Oberlippe hochgezogen | Q3, Q6, Fotos | schwarzer Saum 1,2-1,5 cm | fellbraun, Kante RGB (110, 84, 58) |

Wichtig: unser echtes Maul ist nur 13,0 cm lang (Lippe vorn bis Mundwinkel). Eckzahn + Luecke + volle Backenzahnreihe
(~2,3 + 3 + 8,6 cm) passen NICHT hinein -- die Backenzaehne muessen gekuerzt "angedeutet" werden (Wunsch sagt das auch).

## 2. BESTAND

### 2.1 Kopfrahmen (zum Lesen aller Zahlen)

Kopf-lokal: a nach vorn, b seitlich, c nach oben (`baer/spiel/baer_kampf_pfote.py:107-141`, `fbx2l` 136, `l2fbx` 140).
1 Kopfeinheit = 87,75 cm fuer b und c. **Die a-Achse ist in der Schnauze gestaucht: fuer a > 0,32 ist eine a-Einheit nur
68,44 cm** (Uebergang 0,23-0,32). Lippenlinie `k_lippe(a, B)` (`baer_kampf_pfote.py:164`), Mundwinkel `K_ECKE = 0.275` (:121),
Kieferknochen von (0,075; 0; -0,060) nach (0,45; 0; -0,070) (:169). Achtung fuer Pruefer: `tier()` spiegelt (Determinante -1),
die Windungszahl innen ist -1 -> Innen-Test nur mit `abs(w) > 0.5`.

### 2.2 Wie das Maul heute gebaut ist

**Spielmodell** (das, was im GLB landet) -- `baer_kampf_pfote.py`:
- `maul_bauen` :1898-2134. Schneidet die Aussenhaut entlang der Lippenlinie im Bereich `a > K_ECKE - 0.03` auf, verdoppelt die
  Linienpunkte (oberer Zwilling folgt Head, unterer Jaw; UV des unteren um 2e-4 versetzt) und schliesst einen Beutel an.
- `blatt()` :2027 baut Gaumen und Zunge je als Faecher: Rand -> Ring bei 0,55 zur Mitte -> Mittelpunkt, gewoelbt um
  `GEWOELBE, MULDE = 0.012, 0.008` (:1877). Fuenf hintere Punkte quer ueber die Mundwinkel mit Kiefergewicht 0,5.
- Zaehne :2062-2083: vier 6-seitige Kegel. Oben Basis (0,430; +-0,050; -0,036), Spitze (0,428; +-0,052; -0,070), r 0,0085.
  Unten Basis (0,415; +-0,044; -0,052), Spitze (0,418; +-0,046; -0,020), r 0,0080. Alle Zahn-Dreiecke auf EINEM UV-Punkt (:2115).
- Flecken :1873-1875: `FLECK_GAUMEN = (280,16,80,80)`, `FLECK_ZUNGE = (376,16,80,80)`, `FLECK_ZAHN = (472,16,24,24)`;
  `fleck_uv` :1880 (2 px Innenrand), `kiefer_anteil` :1887, UV der Blaetter :2114, `netz_ersetzen` :2137.
- Farbe :2443-2487: die 1024er Body-Textur entsteht durch Halbieren der 2048er (:2444-2452), dann `fleck_malen` (:2455, 4 px
  Saum): `gaumen_farbe` :2466 (Dunkelrot 0,20/0,085/0,085 mit 7 Kosinus-Rippen), `zungen_farbe` :2473 (Rosa 0,62/0,30/0,31,
  Mittelrinne), Zahnfarbe (0,86; 0,81; 0,69) :2484-2486. Die Flecken gibt es nur in der 1024er Body-Textur.
- Reserviert sind die Flecken durch `SPERR_FLECKEN` (`baer_export_pfote.py:141`, benutzt :2326 und :2631) und als frei
  bestaetigt in `baer_textur_pfote.py:1495-1499`.
- Kieferwinkel: `GRENZE_KIEFER = (0.0, 40.0)` :577; Spuren je Clip :1092, :1133, :1170 (Rear), :1204, :1238 (Maul), :1285, :1370,
  :1419-1420 (Eat).

**Hochmodell** (nur fuer Schau-Render und Backen, landet nicht im GLB) -- `baer_quelle_pfote.py`: `feld_kopf` :290 (Hoehle und
Zahnfleisch :290-305), `feld_zunge` :378, `feld_kamm` :385, `rohr()` :797, Zaehne :1675-1716 (`fang_o` :1702, `fang_u` :1703,
3 Schneidezaehne und 5 Backenzaehne je Seite), Bruellen 32 Grad :2280-2284. **Das Hochmodell hat also schon ein Gebiss -- es
kommt im Spielmodell nur nicht an**, weil `maul_bauen` das Innere unabhaengig davon neu baut.

### 2.3 Zahlen (Dump des fertigen GLB)

| Was | Wert |
|---|---|
| Netz | 11.853 Dump-Punkte, 19.426 Dreiecke (Grenze 20.000 -> 574 frei), 26 Knochen, 15 Clips |
| Tier in Ruhe | 1,96 m lang, 1,16 m hoch, 0,93 m breit |
| Kopf (Head+Jaw > 0,5) | 1.532 Punkte, 2.465 Dreiecke; 51,4 cm lang (echt), 43,4 cm breit; a -0,124..0,515, c -0,241..0,189 |
| Gaumen | 95 Punkte, 141 Dreiecke, 270,6 cm2 |
| Zunge | 95 Punkte, 141 Dreiecke, 269,9 cm2 |
| Zaehne | 32 Punkte, 48 Dreiecke (4 x 12), 31,3 cm2 |
| Maul-Inneres gesamt | 330 Dreiecke |
| Beutel-Blaetter | a 0,249..0,492 = 17,2 cm lang x 20,7 cm breit; Gaumen c -0,047..-0,033, Zunge c -0,053..-0,040 |
| Schnittlinie | 31 Lagen, 64 obere + 64 untere Dump-Punkte, a 0,302..0,492, \|b\| bis 0,095 |
| Maul echt | 13,0 cm lang (Lippe vorn bis Mundwinkel), Lippenkontur halber Bogen 17,1 cm, vorn ~14 cm breit |
| Eckzahn oben | 2,99 cm lang, Basisradius 0,75 cm, bei a 0,430 / \|b\| 4,4 cm (2,7 cm innen von der Lippe) |
| Eckzahn unten | 2,82 cm lang, Basisradius 0,70 cm, bei a 0,415 / \|b\| 3,9 cm -- steht HINTER dem oberen (Natur: davor) |
| Maulpunkte | 288 Dump-Punkte, Knochen nur `Bip01_Head` (Index 18) und `Bip01_Jaw` (Index 19, Kind von Head) |
| Kiefergewicht | > 0: 625 Punkte, > 0,5: 363, = 1: 225; 1.102 Dreiecke beruehren einen Kieferpunkt |

Korrektur: `mess/messen_gebiss_out.txt` nennt fuer Beutel und Kopf entlang a "21,3 cm" und "56,0 cm" -- das ist mit dem
gleichmaessigen Faktor gerechnet und zu lang. Richtig (ueber `a_meter()`): 17,2 cm und 51,4 cm.

Lippenlinie (rechte Seite; halbe Breite in cm je a): 0,31: 8,3 | 0,35: 7,9 | 0,39: 7,6 | 0,43: 7,2 | 0,45: 7,1 | 0,47: 6,6 |
0,485: 4,4. Die Linie laeuft fast gerade nach vorn und knickt erst auf den letzten 2 cm ein -> Kasten.

Schnauzen-Querschnitte der Aussenhaut (cm; halbe Breite an der Lippe / Hoehe darueber / Tiefe darunter):
a 0,32: 8,4 / 11,5 / 6,6 | 0,36: 7,8 / 10,6 / 6,3 | 0,40: 7,8 / 9,5 / 6,1 | 0,44: 7,3 / 9,9 / 5,9 | 0,46: 7,3 / 9,8 / 5,6 |
0,48: 7,0 / 8,7 / 3,9. Das ist der Raum, in den Zaehne passen muessen.

### 2.4 Texeldichte (1024er Body-Textur)

| Flaeche | px/cm | Bemerkung |
|---|---|---|
| Gaumen | 3,91 | Fleck 80 x 80, Mittel RGB (48, 20, 20) |
| Zunge | 3,91 | Fleck 80 x 80, Mittel RGB (99, 46, 47) |
| Zaehne | 0 | ein einziger Texel, RGB (219, 207, 176) -- kein Verlauf, kein Zahnfleischrand moeglich |
| Kopfhaut | 6,33 | |
| Rumpf/Beine | 3,18 | |
| Oberlippen-Kante | -- | Mittel RGB (110, 84, 58), dunkelster Texel (59, 45, 32) -> fellbraun, nicht schwarz |

### 2.5 Wie weit das Maul je Clip aufgeht

Gemessen aus den Clip-Matrizen (`mess/maulbewegung.json`): Kieferwinkel, Spalt vorn (Lippe zu Lippe), Abstand der Eckzahn-Spitzen.

| Clip | groesster Winkel | Zeit (Bild) | Spalt vorn | Spitzenabstand | offen von-bis |
|---|---|---|---|---|---|
| NCBear_Rear | 38,0 Grad | 1,60 s (48) | 21,1 cm | 13,9 cm | 0,67-2,23 s; Plateau 35-38 Grad 0,95-1,85 s |
| NCBear_Bite | 34,0 | 0,433 s (13) | 18,9 | 12,0 | 0,03-1,03 s; 3 Grad Halten 0,6-0,95 s (1,7 cm) |
| NCBear_Maul | 33,7 | 0,433 s (13) | 18,8 | 11,9 | 0,07-1,20 s; 3 Grad Halten |
| NCBear_Slam | 26,0 | 1,133 s (34) | 14,6 | 8,2 | 0,07-1,67 s |
| NCBear_SwipeL / SwipeR | 22,0 | 0,60 s (18) | 12,4 | 6,3 | 0,07-1,20 s |
| NCBear_Eat | 24,0 | 0,50 s (15) | 13,5 | -- | NIE zu: kleinster Spalt 1,7 cm; 18 Grad an Anfang/Ende, Kauen 4 <-> 14 Grad bei 1,2-2,7 s |
| NCBear_Sit | 5,0 | 2,90 s | 2,8 | -- | 2,70-3,17 s |
| DeerStag_Idle01, Walk, Run, Death, Dead, NCBear_SitDown, NCBear_StandUp | 0 | -- | 0 | 4,47 | zu |

Zaehne gegen die Aussenhaut heute: zu -> 0 von 32 Zahnpunkten aussen, kleinste Tiefe 1,83 cm unter der Haut (untere Spitzen
3,4 cm). Maul 3 Grad: 0 aussen. Eat 4 Grad: 2 aussen. Rear 38 Grad: nur die vier Spitzen ragen heraus.

### 2.6 Was die heutige Kopfprobe abdeckt -- und die Maske

- `baer_export_pfote.py` `stufe_kopfprobe` :2673 (Kopf-Dreiecke 2.295 + Krallen 832 = 3.127 bit-gleich), `kopf_inseln()` :600.
  Diese Stufe laeuft VOR `maul_bauen` und sieht das Maul-Innere gar nicht.
- `baer_gewichte_pfote.py` `KOPF_FEST` :50-75 und :410-421: Kopfpunkte bekommen ihre alten Gewichte unveraendert zurueck.
- Pruefer am fertigen GLB (`_arbeit/baer_pfote/werkzeug/`): `kopf.py` (1.333 Kopfpunkte, 1.331 bit-gleich; Maul 312 von 316
  Dump-Punkten gleich) und `textur_pruef_pfote.py` (Kopf-Texel 0 verschieden; Flecken + 4 px Saum bit-gleich).

**Vorschlag fuer die Maske "Aussenform bleibt, Maul innen darf sich aendern"** (drei Zonen, jede einzeln pruefbar):

| Zone | Was dazugehoert | Was sich aendern darf | Pruefung |
|---|---|---|---|
| M1 Innen | alles, was `maul_bauen` erzeugt: Punkte mit UV in den Maul-Flecken (heute 95 + 95 + 32) | alles (Punkte, Dreiecke, UV, Gewichte, Texel der Flecken) | nur Grenzen: Dreiecke, 4 Einfluesse, Summe 1, nur Head/Jaw, Durchstich-Probe |
| M2 Lippenkante | die 31 Lagen der Schnittlinie (64 obere + 64 untere Dump-Punkte) | Lage und UV bleiben bit-gleich; erlaubt: neue Nachbarn nach innen, Kiefergewicht des UNTEREN Zwillings | Lage/UV bit-gleich, Gewichte gelistet |
| M3 Lippenband aussen | Aussenhaut vor a = 0,245 mit \|c - k_lippe(a,\|b\|)\| < d | NUR Texel (schwarzer Lippensaum); Punkte, UV, Gewichte bit-gleich | Texel-Vergleich mit Maske |
| Rest Kopf | alles andere | nichts | `kopf.py`, `textur_pruef` wie heute, Maske abgezogen |

Groesse von M3 je Bandbreite d: 3,5 mm -> 98 Punkte / 151 Dreiecke | 7 mm -> 112 / 180 | 10,5 mm -> 124 / 198 | 14 mm -> 134 / 216 |
17,6 mm -> 144 / 231 | 26,3 mm -> 166 / 273. Empfehlung d = 7 mm. M3 ist freiwillig: ohne M3 bleiben ALLE Kopf-Texel bit-gleich
und das Schwarz kommt nur von einem inneren Lippenstreifen (Abschnitt 4.3).

## 3. BILDER heute

Alle unter `_arbeit/baer_2c/forschung/gebiss/`, jedes Bild als `_ton.png` (ohne Textur) UND `_tex.png`, alle angesehen.
Cycles OPTIX, Auftraege `render/auftrag_heute.json`, `auftrag_heute2.json`, `auftrag_heute3.json`, Logs `log/render_heute*.log`.

| Blatt | Inhalt |
|---|---|
| `vergleich_heute_vorlage.png` | Kevins Vorlage oben, darunter heute a1/a4/a2/a3 in Ton und Textur. Nur unter `_arbeit/baer_2c`, nie weitergeben |
| `heute_bruellen_nah.png` | Rear Bild 48 (38 Grad) nah: vorn, schraeg, Seite, Foto-Blick, oben, unten |
| `heute_zu_und_halb.png`, `render/halb_blatt.png` | Maul zu (Idle) nah; halb offen: Maul 3 Grad, Eat 14 Grad, Bite 34 Grad |
| `heute_spielgroesse.png`, `heute_spielgroesse_kopf.png` | Spielgroesse (pxu 560, Blick 30 Grad von oben) und Kopf-Ausschnitte |

Einzelbilder `render/heute/`: `a1_bruellen_vorn`, `a2_bruellen_schraeg`, `a3_bruellen_seite`, `a4_bruellen_foto`,
`a5_bruellen_oben`, `a6_bruellen_unten` (1200 x 1200); `b1_zu_seite`, `b2_zu_schraeg`, `b3_zu_vorn`, `b4_zu_unten` (900 x 900);
`c1_maul3grad_schraeg`, `c2_fressen14grad_schraeg`, `c3_biss34grad_schraeg`; `s1_aufr_spiel_vorn`, `s2_aufr_spiel_schraeg`,
`s3_aufr_spiel_60`, `s4_biss_spiel`, `s5_stehen_spiel`, `s6_fressen_spiel` (700 x 760).

**Was genau schlecht aussieht** (im Tonbild genauso wie mit Textur -- es ist die Form, nicht die Farbe):
1. **Zaehne:** vier winzige gerade Kegel, sichtbar 1,5-2 cm, 2,7 cm hinter der Lippe -> von vorn kaum zu sehen. Keine Kruemmung,
   keine Schneidezaehne, keine Backenzaehne, kein Zahnfleisch. Untere Eckzaehne hinter den oberen (falsch herum).
2. **Zunge:** flaches rosa Blatt ueber den ganzen Maulboden von Lippe zu Lippe, gerade Vorderkante, ein Knick ("Dach") aus der
   Faecher-Vernetzung. Kein Koerper, keine runde Spitze, keine hochgezogenen Raender.
3. **Gaumen:** flaches dunkelrotes Blatt mit schwachen Streifen, kein Gewoelbe, kein Zahnfleischwall.
4. **Lefzen:** fellbraun bis zur Kante, kein schwarzer Saum, nicht hochgezogen; Unterlippe ist eine duenne scharfe Kante.
5. **Oeffnung:** rechteckiger Kasten, ~14 cm breit x 21 cm hoch, Seiten gerade nach hinten, am Mundwinkel noch 7 cm hoch.
6. **Zipfel an beiden Mundwinkeln:** duenner ">"-foermiger Span in a1, a2, a4, kleine Spitze in a3 (Abschnitt 4.5).
7. **Maul zu:** sauber, nichts sticht durch; die Lippenlinie ist nur eine gemalte Rille.
8. **Spielgroesse:** Kopf ~80 x 80 px, Maul 153-250 rosa/rote Pixel, je Eckzahn 2-3 px, aus dem Spielblick nur das untere Paar.
   Was man liest, ist ein rotes Rechteck (die Zunge). Bei ~1,6 px/cm waere eine 4,6-cm-Krone ~7 px hoch und 3-4 px breit --
   in Spielgroesse zaehlt also Helligkeitskontrast (helle Zaehne vor dunklem Rachen, schwarze Lefzen), nicht Texturdetail.

## 4. MACHBARKEIT

### 4.1 Was ohne Clip-Aenderung geht

Alles, was starre Form ist: Zaehne oben an `Bip01_Head`, Zaehne unten und Zunge an `Bip01_Jaw`, Gaumen/Zahnfleisch oben Head,
Maulboden Jaw, Wangenhaut gemischt. Die 15 Clips, Knochen, Offsets und Bind-Matrizen bleiben bit-gleich; alle vorhandenen
Kieferspuren (2.5) wirken sofort. Das Maul oeffnet weit genug (21,1 cm gegen geschaetzt 14-18 cm bei uns).

Nicht ohne Clip-/Knochen-Aenderung: **echtes Hochziehen der Oberlippe und Haengen der Unterlippe.** Dafuer braeuchte es einen
Lippenknochen oder eigene Spuren -- beides verbietet die Regel "Knochen und Clips bit-gleich". **Vorschlag fuer die Clip-Runde,
hier nicht gebaut.** Ersatz ohne Clip: schwarzer innerer Lippenstreifen + Zahnfleischwall direkt hinter der Lippenkante; beim
Oeffnen wirkt das wie eine zurueckgezogene Lefze, bei geschlossenem Maul ist es unsichtbar.

### 4.2 Wo Zaehne bei geschlossenem Maul durchstechen

Probe `werkzeug/gebiss/probe_gebiss.py`, Ausgabe `mess/probe_gebiss_out.txt`: gedachte Zaehne im Kopfrahmen, Bind-Pose, Test
jedes Zahnpunkts gegen die Aussenhaut (19.096 Dreiecke) per Windungszahl. Kontrolle: die heutigen 32 Zahnpunkte -> 0 aussen,
1,83 cm Tiefe (stimmt mit 2.5). Werte rechts/links; + = cm unter der Haut, - = aussen.

**Obere Eckzaehne** (Head; Basis 0,6 cm ueber der Lippenlinie, Oval 2,3 x 1,7 cm, 10 Grad nach vorn, 35 Grad Bogen nach hinten;
Spalte = sichtbare Krone; "+10" = zusaetzlich 10 Grad nach innen geneigt):

| a | \|b\| cm | 3,6 cm | 4,6 cm | 4,6 cm +10 | 5,6 cm | 5,6 cm +10 |
|---|---|---|---|---|---|---|
| 0,440 | 4,4 | +0,86/+1,02 | +0,80/+0,82 | +1,01/+1,07 | +0,12/+0,07 | +0,40/+0,48 |
| 0,440 | 5,0 | +0,45/+0,56 | +0,37/+0,41 | +0,66/+0,75 | aussen -0,27 | +0,32/+0,39 |
| 0,440 | 5,5 | +0,16/+0,22 | +0,01/+0,03 | +0,30/+0,38 | aussen -0,60 | +0,15/+0,11 |
| 0,440 | 6,0 | aussen -0,2 | aussen -0,35 | grenzwertig +0,04/-0,06 | aussen -0,93 | aussen -0,2 |
| 0,450 | 4,4 | +0,44 | +0,32/+0,37 | +0,48/+0,58 | +0,02 | +0,29/+0,33 |
| 0,450 | 5,0 | +0,08/+0,18 | -0,10/+0,05 | +0,19/+0,26 | aussen -0,36 | +0,14/+0,19 |
| 0,450 | 5,5-6,0 | aussen | aussen -0,2..-1,0 | aussen -0,03..-0,5 | aussen | aussen |
| 0,460 | 4,4 | -0,09/-0,03 | aussen | aussen | aussen | aussen |
| 0,460 | >= 5,0 | aussen | aussen bis -1,34 (11-41 Punkte) | aussen | aussen | aussen |

-> **4,6 cm Krone geht bei a 0,440-0,450 und |b| 4,4-5,0 cm, am besten 10 Grad nach innen geneigt** (Luft 0,2-1,0 cm). Das ist
2,2-3,1 cm hinter der Vorderlippe und mind. 2,1 cm innen von der Seitenlippe. 5,6 cm nur mit Neigung und 0,3-0,5 cm Luft.
Der Eckzahn kann NICHT direkt hinter der Lippenkante sitzen (Fotos zeigen ihn dort -- bei uns verhindert es die feste Aussenform).

**Untere Eckzaehne** (Jaw; Basis 0,6 cm unter der Lippenlinie, Oval 2,1 x 1,6 cm, 15 Grad nach vorn, 8 Grad nach aussen,
45 Grad Bogen nach hinten). Das Ergebnis haengt nicht von der Laenge ab (3,2 / 4,0 / 4,8 cm gleich): der kritische Punkt ist der
Basisring am Kinn.

| a | \|b\| 3,4 | 4,0 | 4,6 | 5,2 |
|---|---|---|---|---|
| 0,462 | +0,29/+0,22 | +0,13/+0,14 | 1 Punkt aussen (-0,16/-0,02) | 2-3 aussen (-0,42/-0,23) |
| 0,470 | 2 aussen (-0,21) | 2 aussen (-0,28) | 4-7 aussen (-0,42) | aussen (-0,73) |
| 0,478 | 8-17 aussen (-0,63..-1,05) | aussen | aussen | aussen |

-> **a ~ 0,462 (1,6-1,7 cm hinter der Vorderlippe), |b| 3,4-4,0 cm, Krone bis 4,8 cm.** Damit steht der untere Eckzahn
0,8-1,5 cm VOR dem oberen und ~1 cm weiter innen -- anatomisch richtig, anders als heute. Luft nur 0,1-0,3 cm: knapp.

**Backenzaehne als Bloecke** (0 von 27 Punkten aussen in allen Faellen): oben (1,8 / 2,6 / 4,0 cm lang) mit 1,0 cm Abstand zur
Lippenlinie +0,40..+0,52; 1,6 cm: +0,98..+1,10. Unten (1,6 / 2,6 / 2,8 / 2,2 cm): 1,0 cm: +0,65..+0,75; 1,6 cm: +1,21..+1,33.
-> ab 1,0 cm Abstand unkritisch.

**Schneidezaehne als Bloecke** (Abstand = Vorderkante hinter der Vorderlippe):

| Zahn | 0,5 cm | 0,9 cm | 1,3 cm |
|---|---|---|---|
| oben I1 (b 0,65) | -0,07/-0,04 (aussen) | +0,26 | +0,64/+0,59 |
| oben I2 (b 1,95) | -0,28/-0,35 (aussen) | +0,09/-0,05 | +0,46/+0,32 |
| oben I3 (b 3,25) | -0,44/-0,50 (aussen) | -0,16/-0,13 (aussen) | +0,12/+0,24 |
| unten I1 (b 0,50) | +0,41 | +0,78 | +1,08 |
| unten I2 (b 1,45) | +0,21 | +0,51 | +0,81 |
| unten I3 (b 2,45) | +0,18 | +0,48 | +0,80 |

-> **obere Schneidezaehne mind. 1,3 cm hinter der Vorderlippe, untere ab 0,5 cm.**

Nicht geprueft (nur am geschlossenen Maul gemessen): bei kleinen Winkeln (Bite/Maul 3 Grad Halten, Sit 5 Grad, Eat 4-14 Grad)
taucht die obere Eckzahn-Krone noch in das Unterkiefer-Volumen und durchsticht ein flaches Bodenblatt (und der untere Eckzahn das
Gaumenblatt). Der Bau braucht dort Taschen/Rinnen seitlich der Zunge und eine eigene Durchstich-Probe je Clip mit >= 2 mm Luft.

### 4.3 Dreiecke: Vorschlag mit Zahlen

Verfuegbar: 574 frei + 330 heutiges Inneres = **904**.

| Teil | Bauweise | Vorschlag | Sparfassung |
|---|---|---|---|
| 4 Eckzaehne | 6-seitig, 4 Ringe + Spitze, gebogen, ohne Boden: 42 je Zahn | 168 | 120 (3 Ringe) |
| 12 Schneidezaehne | Zinnen-Leiste, 6 je Zahn | 72 | 48 |
| Backenzaehne | 4 Hoecker-Leisten (oben/unten, links/rechts), 24 je Leiste | 96 | 64 |
| Gaumen + oberer Zahnfleischwall | gewoelbtes Gitter statt Faecher | 150 | 120 |
| Maulboden + unterer Zahnfleischwall | mit Rinnen fuer die oberen Eckzaehne | 110 | 90 |
| Zunge | eigener Koerper, 7 x 5 Felder oben + Raender + Spitze | 110 | 90 |
| Innerer Lippenstreifen | schwarz -> rosa, 1,2-1,5 cm nach innen, 30 Abschnitte je Kiefer | 120 | 120 |
| Wangenhaut an den Mundwinkeln | 2 x 16 | 32 | 32 |
| Rachenwand | dunkel | 16 | 16 |
| **Summe** | | **874** | **700** |
| GLB danach | 19.426 - 330 + Summe | 19.970 (30 Reserve) | 19.796 (204 Reserve) |

**Achtung Budget-Konflikt:** dieselben 574 freien Dreiecke braucht auch ZIEL A (Beine realistischer). Die Spezifikation muss
teilen. Mit der Sparfassung bleiben 204 fuer die Beine; ein gutes Gebiss unter ~650 halte ich fuer nicht machbar, ohne dass
die Eckzaehne wieder kantig oder die Schneidezaehne weggelassen werden.

### 4.4 Textur

Gemessen `mess/texturplatz_out.txt`, Karte `mess/texturplatz.png`: die 1024er Body-Textur ist zu 81,2 % belegt (Inseln mit 3 px
Saum). Groesstes freies Rechteck **196 x 108 px bei x 269, y 0** -- es enthaelt die drei heutigen Flecken, die davon nur
80 x 80 + 80 x 80 + 24 x 24 nutzen. Zweites: 210 x 29 px bei x 465, y 0. Drittes: 100 x 31 px bei x 923, y 993.

Vorschlag: Gaumen ~92 x 100 und Zunge ~92 x 100 im ersten Rechteck (3,9 -> ~5 px/cm), Zahn-Streifen ~200 x 24 im zweiten
(Verlauf Zahnfleisch dunkel -> Zahnhals gelblich -> Spitze hell; Lippen-Schwarz -> Rosa als eigener Streifen). Keine Insel
muss dafuer wandern. `SPERR_FLECKEN` (`baer_export_pfote.py:141`) und die Pruefung `baer_textur_pfote.py:1495` muessen in den
Kopien dieselben Rechtecke nennen. Nutzen ehrlich: in Spielgroesse gering (Abschnitt 3, Punkt 8), fuer Nahbilder deutlich.

### 4.5 Kasten-Mundwinkel und der Zipfel

Gemessen `mess/mundwinkel_out.txt` (Rear Bild 48): Spalt zwischen oberem und unterem Lippenzwilling vorn 21,1 cm, bei a 0,396
16,9 cm, bei a 0,336 14,2-14,5 cm (Kiefergewicht hart 0 / 1), am Mundwinkel a 0,302 noch 7,0-7,5 cm (Gewicht 0,20-0,22 oben,
0,78-0,80 unten). Die Oeffnung ist also bis 2,4 cm vor den Winkel ein voller Kasten.

**Der Zipfel ist nicht der Beutel** (0 von 128 Beutelpunkten liegen in Idle, Rear, Bite, Eat, Slam mehr als 1 mm vor der
Kopfhaut). Er ist die gespannte Wangenhaut hinter dem Mundwinkel: kleine Dreiecke (0,3-0,7 cm2), deren Mittelreihe mit
Kiefergewicht 0,50 seitlich am weitesten aussen liegt, auf das Vierfache gezogen und von der Kante gesehen. Staerkste Dehnung:
laengste Kante 1,38 -> 5,40 cm (x3,9), 1,24 -> 4,73 cm (x3,8), Flaeche x4,0-4,6 (z. B. Dreiecke [10355, 9478, 9479],
[9483, 9474, 9477]) -- knapp unter der Dehnungsgrenze 4,0.

Das sind Punkte der Aussenhaut. Beheben laesst es sich nur ueber (a) Kiefergewichte der unteren Lippenzwillinge und der Reihe
hinter dem Winkel weicher staffeln (Ruhelage, UV, Texel bleiben bit-gleich; Maul zu aendert sich nicht) oder (b) eine innere
Wangenhaut, die Kasten-Ecke und Span verdeckt. (b) liegt klar in der Maske, (a) nur, wenn die Spezifikation Gewichte der Zone M2
freigibt -- und dann muss die Dehnungs-Pruefung neu laufen.

### 4.6 Was in der Kette neu laufen muss

Kette gelesen in `_arbeit/baer_pfote/werkzeug/lauf_pfote.sh`: Stufen `netz fbx kopfprobe formel gewichte glb zwischen karten deer`.

| Stufe | neu? | Grund |
|---|---|---|
| `netz`, `fbx`, `kopfprobe`, `formel` | nein | Aussennetz unveraendert; `maul_bauen` laeuft erst danach |
| `gewichte` (12-15 min CPU) | nein | nur wenn Variante (a) aus 4.5 gewaehlt wird |
| `glb` | **ja** | Kopie von `baer_kampf_pfote.py` mit neuem `maul_bauen` und Flecken-Malen; danach Dump und `glb_pruef.py` |
| `karten` | nur wenn die Flecken wachsen | Kopien von `baer_export_pfote.py` (`SPERR_FLECKEN`) und `baer_textur_pfote.py` -- nur Konstanten, Inseln bleiben |
| `deer` | **ja** | `NCBearDeer.glb` entsteht aus dem neuen `NCBear.glb` |

Danach die Pruefer: `kopf.py` und `textur_pruef_pfote.py` (als Kopie mit der Maske aus 2.6), Dreiecke <= 20.000, <= 4 Einfluesse,
Summe 1, ein Netz/Material, Clips bit-gleich gegen das baer-pfoten-GLB, Dehnung, Liegehoehe, neue Durchstich-Probe.
Die WorldItems-FBX entsteht vor `maul_bauen` (aus der Stufenfolge geschlossen, die Datei nicht eigens gezaehlt).

### 4.7 Offene Punkte

1. **Lefzen hochziehen** geht nicht ohne Knochen/Clip -> Vorschlag fuer die Clip-Runde; hier nur der statische Ersatz.
2. **Eckzahn sitzt 2,1-3,1 cm innen** statt direkt hinter der Lippe. Von vorn beim Bruellen gut sichtbar, von der Seite teils
   von der Lippe verdeckt. Ob das Kevin reicht, zeigt erst ein Tonbild neben der Vorlage.
3. **Kasten-Oeffnung und Zipfel:** Variante (a) Gewichte oder (b) Wangenhaut -- Entscheidung der Spezifikation (4.5).
4. **Dreieck-Budget** mit den Beinen teilen (4.3).
5. **Kleine Winkel** (3-14 Grad) nicht geprobt: Taschen im Maulboden noetig, sonst stechen Kronen durch Boden/Gaumen (4.2).
6. **Unterer Eckzahn** hat nur 0,1-0,3 cm Luft am Kinn; weiter vorn nur mit kleinerer oder hoeherer Basis.
7. **Eat schliesst nie** (min. 1,7 cm): Zaehne und Zunge sind beim Fressen dauernd zu sehen.
8. **Schwarzer Lippensaum aussen** (Zone M3) aendert Kopf-Texel -- nur mit ausdruecklicher Freigabe; sonst nur innen.
9. **Ohne Beleg, nur geschaetzt:** Eckzahn-Kronenhoehe, Zungenmasse, Gaumenleisten, Massstab 1,15 (Abschnitt 1.3).
10. **Hochmodell hat schon ein Gebiss** (`baer_quelle_pfote.py:1675-1716`): ob der Bau dessen Masse uebernimmt oder die aus
    4.2, ist offen -- die Hochmodell-Zaehne sind nicht gegen die Spielhaut geprobt.

## 5. Werkzeuge (eigene, nur unter `_arbeit/baer_2c/werkzeug/gebiss/`)

`dumpread.py`, `rahmen_gebiss.py` (Kopfrahmen, `a_meter`, Windungszahl; schreibt nichts), `messen_gebiss.py`, `probe_gebiss.py`,
`render_gebiss.py`, `auftrag_gebiss.py`, `blatt_gebiss.py`, `gpu_render.sh`. Die Originale in `baer/spiel` wurden nur gelesen.
Messdaten: `forschung/gebiss/mess/` (`heute.pkl`, `masken.npz`, `maulbewegung.json`, `kameras.json`, `messen_gebiss_out.txt`,
`probe_gebiss_out.txt`, `mundwinkel_out.txt`, `texturplatz_out.txt`, `texturplatz.png`).

## 6. Ehrlich

- Statisch/offline: gemessen am GLB-Dump, gerendert in Blender. Nichts davon ist gespielt.
- **Eine Datei wurde ungewollt gespeichert:** beim Lesen von
  `https://eprints.lib.hokudai.ac.jp/repo/huscap/all/11877/9(4)_p265-276.pdf` hat das Lese-Werkzeug die PDF (866,3 KB) von selbst
  abgelegt unter `C:\Users\Kevin\.claude\projects\C--Users-Kevin-NPCCrew-Nebenprojekte-baer\8f80868b-c5cd-4de5-ade1-25f74fc113d4\tool-results\webfetch-1794266595370-ikg69n.pdf`.
  Nicht geoeffnet, nicht benutzt, nicht ins Projekt kopiert, nicht geloescht (Kevins Entscheidung). Danach keine PDF-Adresse
  mehr abgerufen.
- Laengenfehler in `mess/messen_gebiss_out.txt` (Abschnitt 2.3) -- die Datei ist nicht korrigiert, dieser Bericht nennt die
  richtigen Werte.
- Die Probe in 4.2 prueft gedachte Zaehne nur am geschlossenen Maul gegen die Aussenhaut, nicht gegen Zunge, Gaumen oder
  einander, und nicht in Bewegung.
