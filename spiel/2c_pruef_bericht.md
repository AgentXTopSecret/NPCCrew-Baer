# Lauf baer-2c: Pruefbericht Optik + Technik (10.11.2026, 08:12-09:10)

Gepruefter Stand: `_arbeit/baer_2c/mod/42/media/` (5 Dateien, MD5 unten), Vergleich gegen NCBearTest (Stand baer-pfoten, GLB 5066fa67).
**Statisch/offline gemessen und gerendert, nicht gespielt.** Nichts am Bau geaendert. Eigene Dateien nur unter `_arbeit/baer_2c/pruef/`.
Nichts in NCBearTest oder NPC Crew geschrieben, nichts committet. Renders nur RTX 4090/OptiX + OptiX-Entrauscher ueber eine Kopie von
`werkzeug/gpu_render.sh` (Sperre `gpu.lock`, nicht auf das Spiel geprueft). Alle unten genannten Bilder habe ich angesehen (Read).
Blaetter mit `NURLOKAL` im Namen sowie `pruef/render/ref_spielbild_ausschnitt.png` enthalten Kevins Spielbild bzw. Vorlagen: nur lokal.

## 0. Ergebnis kurz

| Kevins Punkt | Urteil (Ton UND Textur) | Beleg |
|---|---|---|
| "Hose im Stiefel" / Baumstaemme (C5, Ziel A) | **behoben**: Pfote -> Unterarm/Unterschenkel -> Ellbogen/Knie -> Rumpf ist eine Linie, kein Sack ueber dem Bein; Beine schlanker, leicht verjuengt (noch glatte Saeulen, wenig Muskelrelief) | `pruef/blaetter/p5_stehen_spielkamera.png`, `pruef/render/z_stehen_beine.png`, `p13_beine_nah.png`, `p6_gehen_vorn_hinten.png` |
| Sitzen wie die Vorlage (C2) | **weitgehend**: Hinterbeine eng (69 cm), Ferse liegt auf (0,15 cm), Vorderbeine gerade dazwischen, Pranken flach, Hinsetzen/Aufstehen fluessig. Kopf blickt aber sichtbar nach oben (von vorn/seitlich), Oberkoerper geneigt (Skelett-Grenze) | `p1_sitzen_spielkamera.png` (NURLOKAL), `p3_sitzen_seite_vorn.png`, `p7`, `p15`, `p16` |
| Kopf passt zum Koerper (C3) | **nur teilweise**: Kragen hinter dem Kopf +21..24 -> +5..7 cm (Soll <= +2), Buckel woelbt sich in der Spielkamera weiter ueber und neben den Kopf; Kopf heller/glatter, Kante unter dem Kinn, Ring-Falte am Hals im Ton | `p2_kopf_sitzen.png`, `pruef/render/z_kopf_neu.png`, `z_hals.png`, `pruef/log/kragen.txt` |
| Hinterfuss wie Baerenfuss (C1) | **mit Textur ja** (kurz, dunkelbraune Ledersohle, Zehenballen, dunkle Krallen); **im Ton** noch eine laengliche Platte mit geraden Seiten; von vorn L/B 1,50-1,60 | `p4_hinterfuss.png` (NURLOKAL), `pruef/log/fuss_lb.txt` |
| Gebiss/Zunge (Ziel B) | **innen ja**: 4 lange gebogene Eckzaehne, 6+6 Schneidezaehne, Backenleisten, dunkler Rachen, flache Zunge tief im Unterkiefer; Maul zu sauber. Oeffnung bleibt Kasten, Lefzen aussen braun (feste Kopf-Regel) | `p8_maul_bruellen.png`, `p9_maul_vorlage_NURLOKAL.png`, `p10_maul_halb_zu.png` |
| Feste Regeln | Clips, Skelett, Kopf, Dreiecke, Einfluesse, Boden, Dateien: **ja**. **Gerissen:** Falten liegend 254 > 136 und Achsel/Brust 3,510 > 3,5 | Abschnitt 2 |

Befunde: **2 blocker** (beide feste Zahl-Regeln, vom Bauer selbst als "nein" gemeldet), **2 major** (Kopf-Passung, Hinterfuss-Form im Ton),
11 minor. Endgueltig urteilt Kevin im Spiel.

## 1. Was ich gemacht habe (Werkzeuge `pruef/werkzeug/`, Ausgaben `pruef/log/`, `pruef/mess/p1/`)
- Importer: `Dump.java` (Harness `_arbeit/baer_spiel/harness`, unveraendert) auf alt/neu GLB und alt/neu Deer -> `pruef/dump/*.txt`.
  Mein Dump neu ist MD5-gleich zu `glb_2c/dump_2c.txt` (c2b8d6de), alt zu `pruef_koerper/dump/heute.txt` (ab53dabd).
- Eigene Rechnungen: `p_clips.py` (Skelett/Clips/Netz), `p_kopf.py` + `p_texel.py` (Kopf-Maske, Kopf-Texel 1024/2048), `p_sitz.py`
  (Boden je Clip, Anschluesse, Sitzen), `p_fuss_lb.py` (sichtbares L/B), `p_kragen.py` (Kragen), `p_blick.py` (Schnauzenwinkel),
  `p_gelenk.py` (Gelenkwinkel), `p_zaehne.py` (Zahn-Starrheit, Maul zu, Windungszahl), `p_flaeche.py` (Vorderpfote alt -> neue Flaeche),
  Datei-Ebene GLB (JSON, Anim-Puffer byteweise) inline, Deer-Abgleich inline, FBX mit `Probe.java`.
- Kopie der Bauer-Pruefsuite `messen_pruef.sh` (= `werkzeug/pruef/messen_2c.sh`, nur Ausgabeorte auf `pruef/mess/`) auf MEINEN Dumps:
  kopf, tiefst, Regionen/Dehnung, Falten, Ei, Beine, mess2c (`pruef/log/messen_p1.txt`).
- 155 Bilder je Stand (alt/neu, Ton UND Textur Licht B, Engine-Normalen): `pruef/log/auftrag_*.json` -> `pruef/render/alt|neu/`;
  16 Blaetter `pruef/blaetter/p1..p16`. Spielkamera nachgestellt (az 0 el 30, Sit 60): das alte Modell deckt Kevins Spielbild (`p1`).
- Selbstkorrektur: meine erste Projektion fuer "sichtbares L/B" hatte den Bild-oben-Vektor falsch (gab 1,63); korrigiert (gibt fuer alt
  2,12-2,14 = SPEZ "heute") -> neu **1,34-1,36** in der Spielkamera, wie der Bauer.

## 2. Technik

| Pruefung | Messung | Soll | ok |
|---|---|---|---|
| 5 Dateien, Pfade | genau 5; GLB 0ce2661e76fcc8781d9fb3192eb16721, Deer 7a9f8778d3e22876ec1d6ca12d5b156a, FBX b440d69346a5d67bfed8c5b23788f00b, Body 9e9147b56b3792f57c65830034048b62, WorldItems dc8ad63d1279cd2caf6395bbf6d5e83e | wie Bericht | ja |
| GLB-Aufbau | 1 Netz, 1 Primitiv, 0 Materialien, 0 Bilder, 1 Skin, 15 Animationen mit denselben Namen; keine Extras, keine Test-/Cheat-Namen | | ja |
| Skelett | Dump-Teil BONES/OFFSET/BIND textgleich (81 Zeilen); Datei: Knoten-TRS/Kinder und inverseBind byte-gleich | bit-gleich | ja |
| 12 Clips | Dump-Bloecke textgleich; Datei: Sampler-Eingang/-Ausgang byte-gleich (`pruef/log/clips.txt`) | bit-gleich | ja |
| SitDown/Sit/StandUp | Dauer 1,6/4,0/1,3 s, Proben 49/121/40, Zeiten gleich, L-Zeilen gleich; Sit Bild 0 = 120 (0,0); SitDown-Ende = Sit 0 = StandUp 0 (0,0); SitDown 0 / StandUp-Ende gegen Idle 0 je 0,1308 wie heute | gleich | ja |
| Dreiecke / Einfluesse | 19.806 (heute 19.426); max 4, Summe 0,9999999-1,0000002, 0 negative | <= 20.000 (Ziel 19.850) | ja |
| Offene Kanten | 112, alle am Fussring der Zaehne (absichtlich, im Fleisch); nicht-mannigfaltig 41 = heute | | ja |
| Kopf (Maske) | eigene Pruefung: alle Kopfpunkte ausser Mund: Lage/UV/Gewichte gleich, 9 Normalen am Nahtrand anders (wie in allen Laeufen); Suite: 1.333/1.333 | bit-gleich | ja |
| Kopf-Texel | 2048: 0 von 836.172 verschieden; 1024: 2 Randtexel (max 9) in meiner Maske mit Umriss = 2x2-Mittel an der Inselkante | bit-gleich | ja |
| Mundinneres | 732 Punkte, nur Head/Jaw; Zaehne 244 Punkte alle Gewicht 1,0 an Head bzw. Jaw; 20 Teile (2+2 Eckzaehne, 6+6 Schneidezaehne, 4 Leisten) | starr | ja |
| Maul zu | 640 Bilder aller Clips mit Kiefer < 6 Grad (25 Stufen): 0 Zahnpunkte ausserhalb der Aussenhaut (Windungszahl), kleinster Abstand Zahn-Haut 2,5 mm (inkl. Zahnfuesse) (`pruef/log/zaehne.txt`) | 0 / >= 2 mm | ja |
| Krallen | vorn 227 bit-gleich, hinten 228 = alt + (-0,070) | | ja |
| Boden je Clip | kein Clip tiefer als heute; Death -1,42 -> -0,18; Rear -0,11 -> -0,06; Sitz-Clips -0,00 | >= heute - 0,05 | ja |
| Liegehoehe | Dead 0,40 -> 1,12 cm | [0,35; 1,40] | ja (schwebt 0,7 cm hoeher) |
| Dehnung | 99,5 % max 2,49; max 3,68 (Sit, Nacken hinter dem Kopf); **Achsel/Brust 3,510 (SwipeR)** | 2,6 / 4,0 / **3,5** | **nein (B2)** |
| Falten liegend (Dead) | **Achsel+Ellbogen 142+112 = 254** (heute 87+49 = 136); Knie 14 -> 157; sigma2<0,3 102 | **<= 136**, < 0,3 <= 200 | **nein (B1)** |
| Ei (Rear 1,3 s) | 0,993 (heute 1,032) | >= 0,95 | ja |
| Beine Glocke (Ruhe) | vorn Schritte max 3,01 (+0,01), hinten 3,38; max/Mittel 1,18-1,33 | 3,0 / 3,5 / 1,6 | ja (vorn formal +0,01) |
| Rumpf | gesamt 0,794 m; alle 12 Halbbreiten im Band | <= 0,82 | ja |
| Nacken Ruecken-z x 0,40/0,50/0,60 | 1,048 / 0,974 / **0,936** | 1,05-1,07 / 0,96-0,99 / 0,90-0,92 | x 0,60 +1,6 cm |
| Hinterfuss Ruhe | Haut -0,557..-0,264 = 29,3 cm; Breite x -0,50 15,1-15,6 / x -0,33 17,1-17,6 | 29 +-1 / 15-17 / 17-18 | ja |
| Sitzen (Sit 0/30/60/90) | Fussabstand 69,1 cm, Ferse 0,15 cm, Pranken 0,00 cm, Pfoten-Luecke 1,5 cm, Kopf oben 1,306-1,314 | 62-72 / 0-0,5 / flach / >= 1 / 1,20-1,32 | ja |
| Hinterfuss sichtbar L/B | Spielkamera **1,34-1,36**; von vorn el 0 **1,50-1,60** (nur Leder 1,75) | 1,1-1,4 / 1,2-1,5 | Spielkamera ja, vorn knapp nein |
| Gelenkwinkel (Knochenlagen) | Sitz-Clips Knie 55,8-147,7, Sprunggelenk 56,2-103,6, Ellbogen 115,4-162,9: alle innerhalb dessen, was die 12 alten Clips schon zeigen (Run Knie 55,6, Death Sprung 50,5) | | ja (Grenzen-Klemmen selbst nicht nachgerechnet) |
| Deer | laedt, 40 Knochen, Skelett-Text gleich zu heute; 18.576 Dreiecke, <= 4, Summe 1; jede Ecke = Ecke des neuen GLB in Lage UND UV (max 1,5e-7) | | ja |
| FBX WorldItems | laedt (Probe.java), 1 Netz, 11.208 Ecken (= Deer), keine Knochen, Breite y -0,395..0,399 | | ja |
| PNG | Body 1024 RGB, WorldItems 2048 RGB (wie heute) | | ja |
| Originale | `*_pfote.py` MD5 9ae68692/402f9f5b/14fceba9/380f259f/a14a4e1b, im Git unveraendert | unveraendert | ja |

## 3. Optik (alt | neu, Ton UND Textur, nah UND Spielgroesse)
- **Sitzen Spielkamera** (`p1`, `p12_spielgroesse_NURLOKAL.png`): alt deckt Kevins Bild (Fellball, Kapuze, Badelatschen). Neu: kompakt, Beine eng,
  Vorderbeine gerade, Hinterfuesse kurze dunkle Ovale mit Zehenballen. Der Buckel woelbt sich aber weiter hinter und neben dem Kopf ueber
  die Kopf-Oberkante (+5..7 cm), das Gesicht ist heller/glatter als das Halsfell -> "Kopf in der Kapuze" deutlich schwaecher, nicht weg.
- **Von vorn / seitlich** (`p3`, `z_brust.png`, `z_hals.png`): Kopf blickt nach oben, man sieht unter das Kinn (Vorlage: geradeaus); waagerechte
  Helligkeitsstufe quer ueber die Brust, kleiner heller Fleck an der Kehle; im Ton eine Ring-Kante zwischen Kopfunterseite und Hals.
- **Hinsetzen/Aufstehen** (`p7` Ton, `p15` Textur): fluessig, nichts im Boden; StandUp Bild 7 schwarzer Knitterspalt am Knie (`z_su07b.png`).
- **Stehen Spielkamera seitlich** (`p5`, `z_stehen_beine.png`): keine Glocke, kein Sack, Uebergang stetig; Unterbeine bleiben dunkler (weicher
  Farbverlauf, keine Kante).
- **Gehen/Rennen** (`p6`): Walk 20 schwarze Knitterkante vorn am gebeugten Hinterknie, Walk 2 kleiner schwarzer Spalt hinter dem Vorderbein
  (`z_gehen_knie.png`); mit Textur kaum sichtbar (`z_gehen_knie2.png`).
- **Aufrichten/Bruellen, Hieb, Biss, Liegen** (`p11`, `p8`, `p10`): Gebiss deutlich naeher an der Vorlage; Liegen: Knitter an Schulter/Flanke wie
  heute, anders verteilt (`z_dead.png`).
- **Kopf aussen, Vorderpranken, Unterseite/Straehnen** (`p14`): Kopf aussen unveraendert; Straehnen und helle Unterseite im Bild erhalten
  (Messwerte `mess_textur`/`mess_bild` NICHT selbst wiederholt, Zahlen vom Textur-Bauer). Vorderpranken: Sohle unveraendert hellgrau,
  Krallen etwas dunkler, aber noch hell.

## 4. Befunde

### Blocker
**B1 Falten liegend: feste Regel gerissen.** `pruef/mess/p1/falten_neu.txt`, `falten_detail_out.txt`: DeerStag_Dead sigma2 < 0,5 Achsel 142 +
Ellbogen 112 = **254** (heute 136, SPEZ 8.1 hart <= 136, Ziel 120); Knie 14 -> 157 Dreiecke, gestauchte Knie-Flaeche 0,008 -> 0,0425 m2. Anteilig:
Ellbogen 25,0 -> 20,8 % (besser), Achsel 10,9 -> 11,7 % (schlechter); alle gestauchten 704 -> 688. Bild `pruef/render/z_dead.png`: die grosse
Achsel-Knitterzone von heute ist kleiner, dafuer Streifen-Falten an Flanke und Schenkel. Vorschlag: Gewichtsoptimierung mit Falten-Zone um das
Band Ellbogen/Knie z 0,20-0,45 erweitert (wie Fix B1 in baer-pfoten), dabei die neuen Sitz-Clips statt des alten Dumps einlesen
(`baer_gewichte_2c.py:80`), danach Falten + Dehnung neu; oder Kevin nimmt die anteilige Lesart ausdruecklich an.

**B2 Achsel/Brust 3,510 > 3,5 (feste Regel).** `pruef/mess/p1/region_tabelle.json` NCBear_SwipeR Achsel 3,51027 (heute 2,91). Um 0,3 % ueber der
Grenze, im Bild nicht zu sehen. Vorschlag: im selben Gewichtslauf wie B1 die Achsel staerker gewichten, oder SPEZ R1 (Schulter-Halbbreite
x 0,20-0,30 0,40 -> 0,42); danach `region_tabelle.py` neu.

### Major
**M1 Kopf-Passung (C3) nur teilweise erreicht.** Eigene Rechnung `pruef/log/kragen.txt` (Spielkamera az 0 el 30): Koerper hinter dem Kopf
**+5,2..+6,7 cm** (Soll <= +2; heute +21..24), Kante neben dem Kopf auf der abgewandten Seite **-3,3..-5,7** (Soll <= -10); von vorn ok
(-11,5 / -24..-37). Bild: `pruef/render/z_kopf_neu.png` (Buckel als Kuppel ueber und neben dem Kopf, Gesicht heller und glatter, Kante am
Unterkiefer), `z_hals.png` (Ring-Kante Kopf/Hals im Ton). Textur-Ring 0,81-0,83 (Bauer, Soll 0,92). Vorschlag: (1) Nacken/Buckel hinter dem
Kopf in x 0,45-0,65 um weitere 3-5 cm senken, Kopfnaht-Schutz von 9 auf ~5 cm verkleinern (die 1.333 Kopfpunkte bleiben trotzdem fest, nur die
Rumpfseite der Naht bewegt sich; kopf.py danach); (2) Kevin zeigen: Vorschlaege Kopf x1,10-1,15 und Kopf-Texel 9 % dunkler
(`vorschlag/blatt_kopftexel.png`); (3) Halsring: Hals-Gewichte gegen die neuen Sitz-Clips optimieren (siehe B1).

**M2 Hinterfuss: rund nur in der Textur, im Ton eine laengliche Platte.** `pruef/log/fuss_lb.txt`: im Sitzen von vorn L/B **1,50-1,60** (Soll 1,2-1,5),
Lederflaeche allein 1,75; in der Spielkamera 1,34-1,36 (ok). Bild `pruef/blaetter/p4_hinterfuss.png` (neu-Ton: aufrechte Platte mit geraden Seiten,
kleine Zehen), Bauer-Blatt `bilder/textur_3_hinterfuss.png` (neu Ton von unten: Kapsel-Umriss). Die Textur malt das Leder runder als das Netz
(`bau_textur.md` 1: "Super-Oval 2,3 statt 3,4 -> Ecken werden Fellkranz") -- Kevins Regel "eine Textur darf eine falsche Form nie verdecken";
SPEZ 4 verlangt den runden Umriss vom Fellkranz als Form. Vorschlag: Fellkranz als Huellen-Wulst 1-1,5 cm um die Sohle (Seiten und Ferse),
Platte im Netz als Super-Oval 2,3-2,5 wie die Textur, Zehenballen 10-12 mm Relief und dichter am Rand; Ziel von vorn L/B <= 1,45.

### Minor
- **m1 Kopf blickt im Sitzen nach oben.** `pruef/werkzeug/p_blick.py`: Schnauzenlinie (Stirn hinten -> Nase) Sit -10,5..-11,4 Grad, Idle -34,8, Sit
  heute -4..-7,5 -> der Kopf ist ~24 Grad hoeher als im Stehen; von vorn sieht man unter das Kinn (`p3`, `z_brust.png`), seitlich zeigt die
  Schnauze nach oben (`z_hals.png`). Liegt in der SPEZ-Spanne (-25..-15), in der Spielkamera von vorn kaum stoerend. Vorschlag: Kopf nick -24..-26
  probieren und Kragen neu messen (Zielkonflikt mit M1 -> Kevin zeigen).
- **m2 Knitter mit schwarzen Spalten** (Ton; Textur verdeckt fast ganz): Walk 20 vorn am Hinterknie und Walk 2 hinter dem Vorderbein
  (`z_gehen_knie.png`), StandUp Bild 7 am Knie (`z_su07b.png`), Sitzen az -30 Knitterkante am Schenkel und kleine Kerbe an der Schulter
  (`z_sit_ton.png`). Vorschlag: mit dem Gewichtslauf aus B1 (neue Sitz-Clips) erledigen, sonst Laplace an Knie-/Achselrand.
- **m3 Vorderpfoten neu verringert.** 427 von 1.615 alten Punkten unter z 0,115 gibt es nicht mehr (1.811 statt 1.615), Abstand alter Punkte zur
  neuen Flaeche p95 1,1 mm, max 8,1 mm, 47 Punkte > 2 mm alle an der Sohle (`p_flaeche.py`). Regel "Pfoten bleiben (hoechstens Nahtrand)";
  im Bild nicht zu sehen. Vorschlag: Vorderpfoten-Verringerung einfrieren (PF_ZIEL nur hinten senken) oder als Rauschen annehmen.
- **m4 Vorderkrallen noch hell** (`p1`, `p12`): Kevin nannte die "weissen Krallen" der Vorderbeine; heute nur leicht dunkler (Mittel 108/93/76).
  Regel erlaubt dunkler: Vorschlag wie hinten (Wurzel <= 70/55/45).
- **m5 Brust-Stufe und Kehle** (`z_brust.png`): sichtbare waagerechte Kante quer ueber die Brust, heller Fleck an der Kehle (gibt es teils auch heute).
- **m6 Nacken x 0,60** 0,936 statt 0,90-0,92 (mess2c), gehoert zu M1.
- **m7 Sitz-Ausnahme Kopf gegen Hals 57,5 Grad** (SPEZ 5.4, Vorgabe K2) ist gebaut; Kevins/Orchestrators Entscheidung steht laut SPEZ 0.4 noch aus.
- **m8 Glocke vorn formal 3,01 > 3,0** an zwei Schritten (Ruhe), im Bild keine Kante.
- **m9 Beine** im Ton glatte, leicht verjuengte Saeulen ohne Muskelrelief; Fellbehang (4,5 cm) kaum sichtbar (`p13_beine_nah.png`). Kein Rueckfall,
  aber "kraeftiger Unterarm" und "Fell bricht die Kontur" nur angedeutet.
- **m10 Maul-Oeffnung Kasten, Lefzen braun, Oberkoerper geneigt (-37 Grad)**: feste Kopf-Regel bzw. Skelett; Clip-Runde/Vorschlag Lippensaum
  (`vorschlag/blatt_lippensaum_endstand.png`) Kevin zeigen.
- **m11 Liegend 0,7 cm hoeher** (1,12 statt 0,40 cm, im Band), `C:\render\` von Bau Koerper liegt noch da (von Hand loeschen).

## 5. Dateien (`_arbeit/baer_2c/pruef/`)
- Dumps `dump/` (alt, neu, deer_alt, deer_neu), Logs `log/` (clips, kopf, texel, sitz, fuss_lb, kragen, zaehne, gelenke, messen_p1, render_*),
  Suite-Ausgaben `mess/p1/`.
- Werkzeuge `werkzeug/` (eigene p_*.py, `auftrag_pruef.py`, `blatt.py`, Kopien `render_pruef.py`, `gpu_render.sh`, `dumpread.py`, `mess2c.py`,
  `messen_pruef.sh`).
- Bilder `render/alt|neu/` (je 155), Zooms `render/z_*.png`, Blaetter `blaetter/p1..p16` (NURLOKAL: p1, p4, p9, p12 und `render/ref_spielbild_ausschnitt.png`).
