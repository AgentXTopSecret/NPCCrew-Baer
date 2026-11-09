# Lauf baer-pfoten: Nachbesserung 1 (fix1), 09.11.2026 21:20-23:50

Blender 5.2.3, PZ 42.21, JDK 25. **Statisch/offline gebaut, gemessen und angesehen, nicht gespielt.** Nichts in die Test-Mod
NCBearTest (GLB dort weiter 2a4837f6) oder nach NPC Crew geschrieben, nichts committet. Originale `*_anim.py`/`*_fell.py` unveraendert
(MD5 wie `log/md5_originale.txt`). Alter Stand gesichert: `fix1/vorher/42/media/` (5 Mod-Dateien) + `fix1/vorher/*.py` + Netz-npz.

**GPU / Kevins Satz "loesch die regel die hab ich nie gemacht!":** Der Satz hat zwei Lesarten (welche Regel?). Ich habe vorsichtig
gehandelt (passt zu beiden Lesarten und zur Projekt-CLAUDE.md Abschnitt 5 "nie rendern, waehrend er spielt"): solange ProjectZomboid lief
(bis ~23:40), **kein** GPU-Render; alle Kontrollbilder bis dahin mit einem eigenen CPU-Rasterer (Ton UND Textur). Erst als das Spiel
beendet war (23:43, `fix1/log/gpu_protokoll.txt`), ein Render-Lauf auf der RTX 4090/OptiX ueber `fix1/werkzeug/gpu_render_fix1.sh`
(Sperre gpu.lock, fremdes Blender abwarten, Spiel-Pruefung). `werkzeug/gpu_render.sh` des Laufs habe ich NICHT geaendert (kurz
zurueckgesetzt und sofort wiederhergestellt, MD5 wieder 20f03821). Welche Regel Kevin meint, muss die Hauptsitzung mit ihm klaeren.

## 0. Ergebnis kurz
1. **Kragen weg:** Der umgeschlagene Saum ("Pluderhose") an Ellbogen/Knie ist ersetzt durch einen glatten Kegel (Spiel-z 0,18-0,34), ohne
   Umschlag, ohne Stufe; die dunkle Ringlinie der Textur ist weg (Band-Glaettung bis 0,11 hinunter). Der Kegel ist steil (Bein 20 cm
   unten, baer-fell-Saeule 39 cm oben, dazwischen nur 16 cm Hoehe) - Kevins Urteil noetig (Abschnitt 2, M1-Optik).
2. **Hintersohle wie Kevins Foto:** ovale Platte bis an die Ferse, unten rund geschlossen (Leder laeuft um die Fersenkante, kein Schild
   mehr), Ferse breiter, Zehen kuerzer/dicker, Zehenballen groesser, Leder mit Flecken.
3. **Sitzen:** Ferse liegt wieder auf (HL 0,14 / HR 0,26 cm, baer-fell 0,16/0,14; vorher 0,74/0,86) - ohne Clip-Aenderung.
4. **Rumpf = baer-fell** ueber z 0,36 (Gesaessfalte und Knie-Abweichung weg), Pranke von unten runder, Handwurzelballen 1,5-1,6 cm.
5. **Falten (Blocker):** Achsel+Ellbogen 186 -> **136** Dreiecke (SPEZ <= 120, baer-fell 88); gestauchte **Flaeche** aber wie baer-fell
   (Ellbogen 25,0 % / bf 24,4 %, Achsel 10,9 % / bf 10,9 %), Knie 114 -> 14 (= bf), alle gestauchten 816 -> 704 (bf 772). Teilweise behoben.
6. Feste Regeln gehalten: 15/15 Clips bit-gleich, Knochen/Offset/Bind gleich, **19.426 Dreiecke**, <= 4 Einfluesse, Summe 1, Kopf
   bit-gleich (Punkte 1331/1333 + 2 um 5e-5 mm wie bisher, Texel 0 verschieden), Krallen hinten bit-gleich, vorn = alt + K1, Boden 0
   Verstoesse (auch ohne Toleranz besser als vorher), Dehnung 99,5 % 2,59 / max 3,40 / Achsel-Brust 3,26.

## 1. Was geaendert ist (alle Aenderungen mit "fix1" kommentiert, abschaltbar)
| Datei | Aenderung |
|---|---|
| `baer/spiel/baer_export_pfote.py` | `fix1_form` nach `form_fell` am dichten Netz (Spielmeter): (a) Kegel je Bein radial um eine schraege Achse, Hoehe als harmonisches Feld (klappt den alten Umschlag auf), Profil smoothstep z 0,18-0,342 bis zum baer-fell-Querschnitt; (b) Rumpf ab z 0,325-0,34 auf die baer-fell-Flaeche gezogen (`fix1/alt_huelle.npz` aus NCBearTest-GLB 2a4837f6; nur wo > 2-6 mm abweichend, nicht am Kopf); (e) Naehte geglaettet + erneut gezogen; (f) "Entwirren" 8 Runden Laplace an der Kegel-Oberkante (Umklapper 37 -> 0); (c) Fersen-Hinterkante z 0,08-0,20 bis zur baer-fell-Linie (bis 1,2 cm); (d) Ferse unten bis x1,3 breiter. Ballenplan `FIX1_PLAN` (hinten ovale Platte bis x -0,667, groessere Zehenballen; vorn Handballen als Niere). Sohle hinten hinter x -0,546 12 % angehoben (sonst Walk HR 1,3 mm tiefer). |
| `baer/spiel/baer_quelle_pfote.py` | Hinterzehen kuerzer (ax -16 %) und dicker (ay +12 %), Zehenstirn +2 mm (Krallenwurzeln), Krallenbett etwas groesser; Pranke hinten schmaler/weicher aufgesetzt (Umriss von unten oval); Handwurzelballen r 3,3 cm, tiefer, mehr zur Mitte. |
| `baer/spiel/baer_gewichte_pfote.py` | Falten-Zone + Knie + Beinband z 0,18-0,40 (falte_b 25), Lauf mit `falte=75,falte_s=0.62`; Rumpfknochen (Becken/Wirbel/Schwanz/Hals/Kopf) an Beinpunkten unter z 0,15 verboten; Fuss/Hand unter z 0,06 >= 0,95. |
| `baer/spiel/baer_textur_pfote.py` | Ferse "abgerollt" (x_u = x - z hinter x -0,545, Leder rund um die Fersenkante), 3D-Fortsetzung hinten bis z 5 cm; Leder-Flecken 3-6 cm (+-8 %), Furche schmaler, Fell zwischen den Ballen heller; Zehenballen hinten groesser (q x 0,86) und an den Zehen bis 2,4 cm hoch; Handwurzelballen nur unten und 28 % dunkler; Band-Glaettung ab z 0,11 (Kegel); unter 30 cm halb so viel Kontrast-Daempfung (Straehnen); Kopf-Texel immer alt (neue UV-Packung). |
| `baer_kampf_pfote.py` | unveraendert. |
| Werkzeuge `fix1/werkzeug/` | `kette.sh` (ganze Kette ohne GPU nach `fix1/bau*`), `ton.py`/`posen_blatt.py`/`nah_blatt.py` (CPU-Rasterer Ton+Textur), `alt_huelle.py`, `wulst2.py`, `profil.py`, `knick.py`, `tief_ort.py`, `patch_textur.py`, `gpu_render_fix1.sh`; Messungen `fix1/pruef/` (Kopien der Pruefer-Werkzeuge, `messen.sh`). |

Bau-Runden: `fix1/bau` (Kegel ab 0,14: Fuss vom Bein geschluckt, Abnahme brach ein -> verworfen), `bau2` (Fersen-Anhebung), `bau3`
(Kegel ab 0,18), **`bau4` = Endstand** (Entwirren, falte 75). Probe `falte=120` an bau3: Achsel+Ellbogen 134, aber 99,5 % 2,64 > 2,6 -> verworfen.

## 2. Befunde (je Befund: behoben / teils / abgelehnt, mit Messwert)
Messungen in `fix1/pruef/` am Importer-Dump `fix1/bau4/dump_final.txt` (Dump.java), alt = NCBearTest, vorher = Lieferung a6099029.

| # | Befund | Ergebnis | Beleg |
|---|---|---|---|
| B1 | Falten liegend (Blocker) | **teils**: Achsel+Ellbogen sigma2<0,5 186 -> 136 (SPEZ 120, bf 88); Knie 114 -> 14 (bf 14); alle 816 -> 704 (bf 772); sigma2<0,3 154 -> 91 (bf 121). Anteil gestauchte Flaeche Ellbogen 25,0 % (bf 24,4), Achsel 10,9 % (bf 10,9): je Flaeche wie baer-fell, die Zonen haben nur mehr Dreiecke (267/858 statt 190/688). Staerkere Strafe (120) drueckt auf 134, reisst aber 99,5 % <= 2,6 | `fix1/pruef/falten_neu.txt`, `falten_detail_out.txt`, `fix1/bau3/netz/log/gewichte_f2.log` |
| M1 Optik | Kragen/Saum | **behoben** (Umschlag + Ringlinie weg), Form Kegel: Ueberhang (Normale z < -0,7) VL 20-40 cm 749 -> 385 cm2, HL 937 -> 975 (Vorderkante Knie steil, glatt); Umklapper im dichten Netz 0 | `fix1/bilder/knie_ton.png`, `fix1/bilder/final/kurz_0.png`, `fix1/bilder/final/nah_b.png`, `wulst2.py` |
| M2 Optik | Hintersohle Schild | **behoben**: Platte oval bis an die Ferse, unten rund; Zehen kuerzer/dicker; Zehenballen groesser | `fix1/bilder/final/kurz_2.png` (Sitzen), `kurz_3.png` (Aufrichten unten), `nah_a.png` neben Kevins Vorlagen `nah_b.png` |
| M1 Technik | Sitz-Ferse schwebt | **behoben** ohne Clip: Sit Bild 60 HL 0,14 / HR 0,26 cm (bf 0,16/0,14; vorher 0,74/0,86) | `fix1/pruef/detail_out.txt` (e) |
| M2 Technik | Rumpf > 1,5 cm | **teils**: Gesaessfalte/Knie-Cluster weg; p95 0,35 -> 0,15 cm; > 1,5 cm 42 -> 13 Punkte, max 2,71 -> 2,31 cm, verstreute Einzelpunkte (Verringern; z. B. -0,128/0,142/1,026) | `fix1/pruef/rumpf_out.txt` |
| M3 Technik / minor 1 Optik | Pranke kastig | **behoben/teils**: Umriss von unten hinten rund, Handballen Niere; Handwurzelballen unten 1,56/1,48 cm (Soll 1,5-2,0), Vorsprung 1,04/0,74 (Soll 0,8, VR knapp); Rist vorn 6,0 (Soll 6,5, wie vorher) | `abnahme_out.txt`, `fix1/bilder/final/kurz_3.png` |
| minor 2 Optik | Handwurzelballen Kiesel | **behoben**: nur nach unten gewandte Kappe, 28 % dunkler | `nah_b.png` Stehen VL Seite |
| minor 3 Optik | Kniekehle-Schlitz Sitzen | **nicht gezielt behoben**; Rumpf dort jetzt = baer-fell + Kegel; im CPU-Bild Sitzen nah kein offener Spalt gesehen (ungeprueft im GPU-Bild) | `kurz_2.png` |
| minor 4 Optik | Sohlenrand facettiert | **abgelehnt** (mit Textur unsichtbar, laut Pruefer niedrige Prioritaet); Knick unveraendert ~26-31 Grad Mittel | `abnahme_out.txt` |
| minor 5 Optik | Unterbein-Straehnen | **teils** (weniger Daempfung unter 30 cm); nicht nachgemessen (mess_bild braucht GPU-Bilder der alten Kameras) | Textur-Bilder |
| minor 6 Optik | Aufrichten-Pranke von vorn | **abgelehnt** (Clips bit-gleich). **Vorschlag Clip-Runde:** im NCBear_Rear das Handgelenk drehen, Handflaeche nach vorn | - |
| m1 | Boden nur mit Toleranz | **behoben**: 0 Verstoesse; Walk HR -1,45 -> -1,38 (heute -1,41), HL -1,64 (-1,72); Maul VL -0,03 = heute | `tiefst_out.txt` |
| m2 | Liegen schwebt 4 mm | **abgelehnt**: Liegepose/Clips fest; tiefster Punkt 0,40 cm (Kralle, wie bf), Beine 0,58 cm; Regel "nicht tiefer" gehalten | `detail_out.txt` (d) |
| m3 | Schwanz/Wirbel an Pfoten | **behoben**: fremde Knochen 0 an allen Pfoten, Rumpfknochen unter 15 cm verboten | `netz_pruef_out.txt` 4 |
| m4 | Splitter | **teils**: Ferse-Splitter weg, Kegel-Oberkante entwirrt; ohne Kantenfilter noch 18 Dreiecke > 4, max 26,7 (SitDown, Hinterschenkel aussen z 0,41, Hoehe 1,2 mm) - schlechter als vorher 13,4, gefiltert unsichtbar; offen | `splitter_out.txt` |
| m5 | Achsel staerker gedehnt | teils: Run 2,71 -> 2,23 (bf 2,18), Rear 2,65 -> 2,29, Walk 2,34 -> 2,15; SwipeL 3,08 -> 3,26 (Grenze 3,5) | `region_tabelle_out.txt` |
| m6 | Pfotengewichte | **behoben**: Hand/Fuss unter 6 cm >= 0,95 bei 100 % (min 0,950) | `netz_pruef_out.txt` 4 |
| m7 | Krallenwurzeln | **teils**: Wurzeltiefe hinten 0,05..0,29 cm, vorn -0,06..0,25 (vorher -0,28..0,15; Soll 0,2-0,8); Anteil Krallenpunkte in der Haut 8-27 % | `abnahme_out.txt`, `krallen_wurzel_out.txt` |
| m8 | SPEZ-3.2-Formziele | gemessen: hinten alle Pfotenmasse ja (Fuss/Bein 2,03, Zehen-Ueberstand 19,7, Ferse 2,7, Rist 7,2); vorn Bein z15-Fuss z3 -1,3/-1,4 (Soll -1,5, vorher -1,5), Rist 6,0; Rillen/Zehenstirn hinten teils < Soll (gewollt flacher) | `abnahme_out.txt` |
| m9/m10 | nur 5 Dateien zusammen; Bezug | Integrator: alle 5 in einem Zug. Neuer Bezug `fix1/bau4/textur/zw_fell_2048.png` (aus Vor-Bake tx1 + fell_uebertrag) bei den Lieferungen behalten; Kette `fix1/werkzeug/kette.sh tx1 bezug tx2 txglb` | `fix1/log/kette12.txt` |

## 3. Feste Regeln (gemessen, bau4)
Clips 15/15 Abtastungen/Schluessel/Modellmatrix gleich, Knochen/Eltern/Offset/Bind gleich (`fix1/bau4/log/glb_pruef_final.txt`); Dreiecke
19.426; Summe 1,0000, max 4 Einfluesse, 19 Knochen; offene Kanten 0; Kopf 1331/1333 bit-gleich (+2 Float-Rauschen wie bisher), gehaeutet
0,000 mm; Kopf-Texel 2048/1024 0 verschieden (Rand 1 px in 1024: 1), Krallen-Abtastung 455/455 gleich, Maul-Flecken gleich
(`fix1/pruef/textur_out.txt`); Krallen hinten 228/228 bit-gleich, vorn alt + K1; Ei Rear 1,032 (bf 1,033); Dehnung 99,5 % 2,59 (<= 2,6),
max 3,40 (<= 4,0), Achsel/Brust 3,26 (<= 3,5); Boden 0 Verstoesse; Deer TIER_OK 18.974+ Dreiecke wie Netz.

## 4. Dateien
Mod-Ergebnis `_arbeit/baer_pfote/mod/42/media/` (= `fix1/mod/42/media/`, byte-gleich), MD5:
- `models_X/Skinned/NCBear.glb` 5066fa6774f32b52df558e9878c48610
- `models_X/Skinned/NCBearDeer.glb` 1f704054a4b8a8c787a0d284d1c75683
- `models_X/WorldItems/NCBear.fbx` 0cab0ff6eaee7003932c24902bca4d10
- `textures/Body/NCBear.png` 4ae148dfc4028c40ee86bc42e8880880
- `textures/WorldItems/NCBear.png` 603ee6998ebf3bc268019cdd53e227e2

Vorher (gesichert `fix1/vorher/42/media/`): a6099029 / 9246fa53 / ab35c415 / 4ae60e6c / 94212c2e. Skripte jetzt: export 9ae68692,
gewichte 402f9f5b, kampf 14fceba9 (unveraendert), quelle 380f259f, textur a14a4e1b.
Bilder (CPU, Ton+Textur, alt | vorher | neu): `fix1/bilder/final/p_<pose>.png` (stehen, gehen, gehen20, rennen, sitzen, aufrichten,
liegen, sohle), Auszug `fix1/bilder/final/kurz_0..4.png`, Nah + Kevins Vorlagen `fix1/bilder/final/nah_a.png`/`nah_b.png`, Knie
`fix1/bilder/knie_ton.png`. GPU (RTX 4090/OptiX, Spiel-Licht B, 23:43-23:44 nach Spielende, 143 Bilder, Log `fix1/log/render_fix1.log`): `render/fix1/`, Blatt `fix1/bilder/gpu_vergleich.png` (Zeile 2 'vorher' = `render/final` des Netz-Bauers mit dessen fleckiger Zwischentextur, nicht die gelieferte Textur). Angesehen: Bein ohne Saum, Sitzen Hintersohle oval bis zur Ferse, Spielgroesse unauffaellig.

## 5. Offen
Falten Achsel+Ellbogen 136 > 120 (Flaechenanteil wie bf); Kegel steil (Kevin urteilen lassen); Splitter max 26,7 ungefiltert; Rumpf 13
Einzelpunkte > 1,5 cm; Krallenwurzeln < 0,2 cm; vorn Bein z15 -1,3 statt -1,5; Fell-Ansichten (GPU) sind noch die des alten
Hochmodells (Zehen/Ferse/Pranke leicht anders, der Bake nimmt sie trotzdem); Aufrichten-Pranke von vorn = Clip-Runde. **Nicht gespielt.**
