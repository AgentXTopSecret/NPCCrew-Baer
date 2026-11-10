# Lauf baer-2c: Gegenpruefung Stand fix1 (10.11.2026, 10:25-11:40)

Geprueft: `_arbeit/baer_2c/mod/42/media/` (genau 5 Dateien, MD5 unten) gegen NCBearTest (Stand baer-pfoten, GLB 5066fa67).
**Statisch/offline gemessen und gerendert, nicht gespielt.** Nichts am Bau geaendert; eigene Dateien nur unter `_arbeit/baer_2c/pruef/gegen/`
und das Blatt `_arbeit/baer_2c/bilder/kevin_vorher_nachher.png`. Nichts in NCBearTest oder NPC Crew geschrieben, nichts committet.
Renders nur RTX 4090/OptiX + Entrauscher ueber eine Kopie von `werkzeug/gpu_render.sh` (Sperre `gpu.lock`, am Ende frei; nicht auf das Spiel
geprueft). Alle unten genannten Bilder habe ich angesehen. Blaetter mit `NURLOKAL` enthalten Spielbild/Vorlagen: nur lokal.
Originale `*_pfote.py` unveraendert (9ae68692/402f9f5b/14fceba9/380f259f/a14a4e1b).

## 0. Urteil

**ready = false.** Keine feste Regel ist gebrochen, und der Stand ist in jedem Bild deutlich besser als NCBearTest (Beine ohne Glocke,
Sitzen eng, Hinterfuss kurz/dunkel, Gebiss). Die Abnahme-Bedingung "sitzt wie die Vorlage, Kopf oben OHNE Kragen" ist aber nur
teilweise erfuellt: hinter dem Kopf steht der Buckel in Kevins Spielkamera noch +2,6..+4,2 cm ueber der Kopf-Oberkante (Spez <= +2),
eine Kopfseite -9,3..-10,1 (Spez <= -10), der Ring um den Kopf ist 12 % dunkler als der Kopf (Spez >= 0,92), und der Kopf blickt im
Sitzen sichtbar nach oben (Vorlage geradeaus). Das sind genau die Punkte, die Kevin mit "kopf passt nicht zum koerper" meinte; der Rest
haengt an seinen Entscheidungen (Buckel tiefer gegen seinen Schulterbuckel-Wunsch, Kopfblick gegen Kragen, Kopf-Texel/Kopf x1,12 nur als
Vorschlag). Empfehlung: Kevin diesen Stand zeigen (Blatt + Test unten), aber nicht als "fertig" melden.

| Kevins Punkt | Ton | Textur | Beleg |
|---|---|---|---|
| Hose im Stiefel / Glocke (C5) | weg, Uebergang stetig | weg | `pruef/gegen/blaetter/g2_stehen.png`, `g11_beine_nah.png`, `g3_gehen_rennen.png` |
| Beine Rohr/Baumstamm (Ziel A) | vorn verjuengt, hinten glatte Saeulen (von hinten fast gleich dick) | wie Ton | `render/z_hinten_4.png`, `render/z_seite_2.png` |
| Beine eng im Sitzen (C2/C4) | ja: Fuss-Mitten 71,2 cm (alt 118,1) | ja | `log/mess.txt` Abschn. 4, `blaetter/g1_sitzen_spielkamera_NURLOKAL.png` |
| Menschenfuss (C1) | nein mehr, aber im Ton ein runder Klotz mit kleinen Zehen | kurzes dunkles Oval mit Zehenballen | `blaetter/g6_hinterfuss_NURLOKAL.png`, `log/fuss_lb.txt` |
| Kopf in der Kapuze (C3) | ringsum weg, Buckel hinter dem Kopf bleibt; Kopf blickt hoch | Kopf heller als der Ring | `blaetter/g8_kopf_sitzen.png`, `log/kragen.txt`, `log/naht_bild.txt` |
| Zaehne/Zunge wie Vorlage (Ziel B) | 4 lange Eckzaehne, 6+6 Schneidezaehne, flache Zunge; Oeffnung Kasten, Mundwinkel-Zipfel | dunkler Rachen, Zahnfleisch rosa; Lefzen braun | `blaetter/g5_maul_NURLOKAL.png`, `render/z_maul_nah.png` |

## 1. Feste Regeln (eigene Rechnung, Werkzeuge `pruef/gegen/werkzeug/`, Logs `pruef/gegen/log/`)

| Regel | Messung | ok |
|---|---|---|
| 5 Dateien, Pfade, MD5 | genau 5; MD5 = Kurzfassung fix1 (Tabelle 5); PNG 1024/2048 RGB wie alt (`log/technik.txt`) | ja |
| GLB-Aufbau | 1 Netz, 1 Primitiv, 0 Materialien, 0 Bilder, 1 Skin, 15 Animationen, keine Extras (`g_technik.py`) | ja |
| Skelett | Knotennamen, TRS, Kinder, Skin-Joints gleich, inverseBind byte-gleich; Dump BONES/OFFSET/BIND textgleich | ja |
| 12 Clips bit-gleich | Datei-Ebene: alle 78 Kanaele je Clip byte-gleich (Sampler-Ein-/Ausgang); Dump-Bloecke textgleich | ja |
| Sitz-Clips Vertrag | SitDown/Sit/StandUp: Dauer 1,6/4,0/1,3, Proben 49/121/40, Zeitzeilen gleich; Sit erstes = letztes Bild, SitDown-Ende = Sit 0 = StandUp 0 (0,0) (`log/sitz2.txt`) | ja |
| Dreiecke / Einfluesse | 19.806 (<= 20.000); max 4, Summe 0,9999999..1,0000002, 0 negativ | ja |
| Kopf ausserhalb Maske | 1.333/1.333 amtliche Kopfpunkte Lage+Gewichte+UV gleich (`log/kopf2.txt`); eigene Maske Kopf/Kiefer >= 0,999: 1.005/1.005 alle 16 Werte gleich. 234 Punkte mit Teil-Kopfgewicht (x 0,45-0,73) anders = Hals/Rumpf, keiner amtlich Kopf | ja |
| Kopf-Texel | eigene UV-Maske (reine Kopf-Dreiecke): 2048 0 von 525.257 verschieden; 1024 1 Randtexel (max 9) von 132.016, 2 px eingerueckt 0 von 124.717 | ja |
| Krallen | vorn 227/227 alle 16 Werte gleich; hinten 228/228 Gewichte/UV gleich, Lage = alt + (-0,070 m) auf 0,0000 mm (`log/krallen.txt`) | ja |
| Boden je Clip | kein Clip tiefer als alt (Death -1,42 -> -0,14, Rear -0,11 -> -0,06, Rest gleich, Sitz-Clips 0,00) (`log/mess.txt` 1) | ja |
| Liegehoehe Dead/Death | 0,40 -> **1,12 cm** (Band Spez 0,35-1,40); liegt 7 mm hoeher als bisher | ja (Band) |
| Dehnung (Suite-Regel) | eigene SVD mit der Gueltigkeitsregel der Suite: 99,5 % max **2,33**, Hoechstwert **3,25**, Achsel/Brust **3,08** (`log/dehnung_suite_regel.txt`) - deckt sich mit fix1 | ja |
| Maul zu | alle **640** Bilder mit Kiefer < 6 Grad, alle 244 Zahnpunkte: **0** ausserhalb der Aussenhaut (`log/mess.txt` 5) | ja |
| Deer / FBX | Deer 40 Knochen, Skelett-Text gleich alt, jede Ecke = Ecke des GLB (max 1,1e-7); FBX laedt (Probe), 1 Netz, 11.093 Ecken, keine Knochen (`log/fbx_probe.txt`) | ja |
| Sitzen Ferse / Pranken | Ferse tiefste Haut 0,09/0,10 cm in jedem Bild, Vorderpranken 0,00, Luecke Vorderpfoten 1,5 cm | ja |
| Durchdringung Sitz-Clips | grobe Kapselprobe Hinterbein in Unterarm: 0 Punkte in allen Bildern | ja |

## 2. Befunde

### Fuer "ready" fehlend (Abnahme-Bedingung Kopf ohne Kragen / sitzt wie Vorlage)
**G1 Kragen-Rest hinter dem Kopf.** Eigene Rechnung (`werkzeug/g_kragen.py`, `log/kragen.txt`, ohne 6 cm Nahtband `log/kragen_ohne_naht6cm.txt`),
Kevins Kamera az 0 el 30: Koerper hinter dem Kopf alt +21,4..+24,0 -> neu **+2,6..+4,2 cm** (Spez <= +2); 3 cm neben dem Kopf alt +12,4/+6,2
-> neu **-9,3..-10,1** / -15,2..-18,5 (Spez <= -10); Kopf/Silhouette 0,33 -> 0,49-0,52 (Spez >= 0,45, ok). Bild `render/z_sit60_spiel_4.png`:
der Kragen ringsum ist weg, der Kopf sitzt oben, aber der Buckel woelbt sich links hinter dem Kopf noch ueber die Ohren. Die Kamera habe ich
selbst gegen Kevins Spielbild geprueft (`blaetter/g0_kamera_NURLOKAL.png`, az 0 el 30 deckt).
**G2 Kopf "aufgeklebt" (Farbe).** Eigenes Bildmass (`werkzeug/g_naht.py`, `log/naht_bild.txt`, Licht B): Ring 0-4 cm / Kopf alt 0,81 -> neu
**0,88** (Spez >= 0,92), Ring 4-12 cm 0,78 -> 0,95 (ok), Feinstruktur 1,10-1,24 -> 0,96 (ok). Im Bild: dunkler Saum unter Kinn und Wange.
**G3 Kopf blickt im Sitzen nach oben.** Kopf gegen Hals in den Sitz-Clips bis **58,4 Grad**, in allen 12 anderen Clips hoechstens 24,5
(`log/sitz2.txt`) = die Sitz-Ausnahme K2 (Spez 0.4/5.4), die laut Spez noch Kevin/Orchestrator freigeben muss. Bilder `g7_sitzen_ansichten_NURLOKAL.png`
(von vorn sieht man unter das Kinn, seitlich zeigt die Schnauze nach oben; Vorlage blickt geradeaus).
Alle drei brauchen Kevins Wort (fix1 Abschnitt 6: Buckel 1,5-3 cm tiefer gerechnet, nicht gebaut; Kopf-Texel/Kopf x1,12 nur Vorschlag).

### Major
**G4 Hinterfuss im Ton noch ein Klotz.** Mit Textur ein kurzes, dunkles Oval mit Zehenballen und Fellkranz (`render/z_fuss_vergleich_NURLOKAL.png`);
im Ton eine abgerundete Platte mit fuenf kleinen Zehen, die Vorlage hat grosse runde Zehenballen. Eigene Masse (`log/fuss_lb.txt`):
sichtbar L/B ohne Krallen 1,34-1,38 in allen Ansichten (alt 2,03-2,13), mit Krallen Spielkamera 1,43/1,44, von vorn **1,54-1,62** (Spez 1,2-1,5).
Ruhe: Fuss mit Krallen 32,1 cm (alt 46,2), Breite 18,4-18,6 cm.
**G5 Zahnfuesse der unteren Schneidezaehne 0,35 mm unter der Kinnhaut.** Eigene Rechnung ueber JEDEN Zahnpunkt (`log/zahn_abstand.txt`,
`log/zahn_teil.txt`): 12 Punkte < 2 mm, 3 < 1 mm, min **0,35 mm** (drei 6-Punkt-Schneidezaehne vorn unten, Jaw, starr; in jeder Pose gleich).
Kein Durchstich (Windungszahl 0 aussen). Spez 3.2 verlangt Luft >= 2 mm. Der Pruefer meldete "2,5 mm inkl. Zahnfuesse" (`pruef/werkzeug/p_zaehne.py`
misst nur jeden 3. Zahnpunkt und je Winkelstufe ein Bild) und fix1 uebernahm 2,5 mm; der Gebiss-Bauer hatte es ehrlich gemeldet
(`bau_gebiss.md`:107, :185 "0,2-1 mm, im Spiel ansehen"). Im Render nicht sichtbar; im Spiel nah auf das geschlossene Maul schauen.

### Minor
- **G6 Gestreckte Splitter-Dreiecke in der Achsel (verdeckt).** Mit ALLEN nicht entarteten Dreiecken (auch denen, die die Suite-Regel
  "Kante > 7,4 mm, Hoehe > 1,1 mm" auslaesst): Flaeche mit sigma1 > 4 je Clip alt -> neu z. B. Dead 16 -> 84 cm2, SwipeR 1 -> 71, Slam 9 -> 85,
  Walk 8 -> 48, Sit 34 -> 74 (`log/dehnung_flaeche.txt`), Einzelwerte bis 37 (`log/dehnung_suite_regel.txt`). Fast alles liegt in der
  Achselfalte; in den Feld-Renders sind nur einzelne rote Splitter zu sehen (`blaetter/g4_dehnung_a.png`, `g4_dehnung_b.png`). Feste Regel
  (Suite-Definition) eingehalten; Hinweis fuer die naechste Gewichtsrunde.
- **G7 Knitter im Ton**: schwarze Kerben am Hinterknie (Walk 20, Run 5) und Halsring unter dem Kopf; mit Textur kaum (`render/z_knitter_walk20.png`).
- **G8 Vorderpfoten neu verringert**: 397 von 1.615 alten Punkten (z < 0,115) nicht mehr da, Abstand zur neuen Flaeche p50 0,27 / p95 4,75 /
  max 8,07 mm, 46 > 2 mm, alle an der Sohle (`log/vorderpfote.txt`). Regel "Pfoten bleiben" nur der Form nach; im Bild nicht zu sehen.
- **G9 Mund-Dreiecke 1.146** statt Soll 874 (Spez 8.2: 700-874); Gesamt 19.806 im Ziel (`bau_gebiss.md`:30).
- **G10 Maul-Oeffnung Kasten mit Zipfel am Mundwinkel, Lefzen braun** (`render/z_maul_nah.png`) - feste Kopf-Regel bzw. Clip-Runde.
- **G11 Liegend 7 mm hoeher** als bisher (1,12 statt 0,40 cm), im Spez-Band.
- **G12 Vorschau-Video**: `bilder/sitzen_vorschau.mp4` und `textur_vorschau_sitzen.mp4` sind vom Stand VOR fix1; fix1 hat keins neu gemacht.
  Ersatz von mir (nur lokal): `pruef/gegen/blaetter/g10_hinsetzen_sitzen_aufstehen.gif` (Kevins Kamera, alt|neu, Textur) und Kontaktbogen
  `g10_folge_kontakt.png`: Hinsetzen/Sitzen/Aufstehen fluessig, nichts im Boden, Fuesse bleiben eng.
- Nicht selbst gemessen (Zahlen von fix1, Dump byte-gleich zu meinem, MD5 2875ca08): Falten liegend 127, Ei 0,993, Unterseite, Straehnen.
  Im Bild sind helle Brust und Fellstraehnen erhalten (`blaetter/g7_sitzen_ansichten_NURLOKAL.png`, `g2_stehen.png`).

## 3. Bilder
- Fuer Kevin (ohne Vorlage/Spielbild/Stockfotos): `_arbeit/baer_2c/bilder/kevin_vorher_nachher.png` - links vorher (NCBearTest), rechts
  nachher, je Ton und Textur: Sitzen Spielkamera, Sitzen Spielgroesse, Sitzen von vorn, Hinterfuss nah, Bruellen nah, Bruellen Spielgroesse,
  Stehen seitlich (Spielkamera), Stehen hinten, Gehen.
- Arbeitsblaetter `pruef/gegen/blaetter/g0..g11` (NURLOKAL: g0, g1, g5, g6, g7), Einzelbilder `pruef/gegen/render/alt|neu|dehn_*|video_*`,
  Zooms `render/z_*.png`.

## 4. Kevins Test (nach dem Kopieren in NCBearTest, Spiel neu starten)
1. `NCBear_SpawnLive()`, dann `NCBear_Sit(20)` aus der normalen Spielkamera: Sitzt der Kopf oben auf dem Koerper oder noch in einer Kapuze?
   Stehen die Beine eng, sind die Hinterfuesse kurze dunkle Ovale (kein Badelatschen)? Blickt der Kopf zu sehr nach oben?
2. Hinsetzen und Aufstehen einmal ganz ansehen: fluessig, nichts im Boden?
3. Einmal um den stehenden Baeren laufen (seitlich, hinten): Hose im Stiefel weg?
4. Gehen und Rennen: Beine ohne Kerbe/Knick am Knie?
5. `NCBear_AnimTest("rear")`: Zaehne und Zunge beim Bruellen, dann nah an das geschlossene Maul: blitzt unten vorn ein Zahn durch die Lippe?
6. Gab es rote Fehler (ja/nein)?
