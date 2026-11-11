# NACHBESSERUNG -- Lauf baer-rig-junges, Rolle NACHBESSERUNG (11.11.2026)

**Statisch geprueft, nicht gespielt.** Geschrieben nur unter `rig/fix/`, `rig/out/` (Endergebnis), diese Datei, ein Hinweisblock oben in
`rig/CLIPS.md` und `baer/spiel/baer_clips_rig.py` (Sitz-Vorgaben). Nichts in Test-Mods, NPC Crew, Spiel oder `_arbeit/baer_zaehmen/mod/`;
kein git, kein Download. Alle 191 Dateien aus `rig/clips/md5_nachher.txt` (NCBearTest, zaehmen/mod, Original-Skripte, Eingaenge) sind
nachgezaehlt byte-gleich. Zahlen bei Groesse 1,0 (Spiel x 0,35), Rahmen tier (x vorn, y links, z oben), Haut aus dem Importer-Dump.

## 0. Ergebnis kurz
- **Sicherung:** Stand vor der Nachbesserung in `rig/out_vor_fix/` (GLB d89856ef..., PNG 8ce68838..., byte-gleich nachgezaehlt).
- **Neu:** `rig/out/42/media/models_X/Skinned/NCBearCub.glb` **ee7a0cce2efb188e307b8f51a090b868** (1.235.528 Byte),
  `rig/out/42/media/textures/Body/NCBearCub.png` **92a829fab0a23521cc00bcebeb42c9d0**, `rig/out/md5.txt`.
- **Harness laedt es** (Dump.java auf genau diese Datei): 26 Knochen, 15 Clips, 11.811 Punkte, 19.418 Dreiecke; FK Importer gegen GLB-Kette
  5,2e-7 E; Dump von `rig/out` = Dump von `rig/fix/out` (MD5 61580dd0).
- **Behoben:** Tod/Liegen (das Junge liegt jetzt auf der Flanke), Sitz-Durchdringung (Strahl-Test 0 in allen drei Sitz-Clips, Werkzeug
  des Pruefers), Fressen (Kopf vorgestreckt, Gesicht aus Kevins Kamera sichtbar), Ohren (keine dunklen "Augen-Scheiben" mehr).
- **Offen fuer Kevin:** Wachsen gegen Gangbild (geht im Modell nicht zu loesen), Schnauze erreicht beim Fressen den Boden nicht
  (eigener Fress-Clip?), Kopfhaltung beim Stehen/Gehen, kleine Restpunkte (Liste 5).

## 1. Je Mangel: was gemacht, neue Zahlen
### PRUEF_TECHNIK
| ID | vorher | gemacht | nachher |
|---|---|---|---|
| **M1 major** Death-Ende/Dead: Rumpf 14,7-18,9 cm hoch auf der linken Pranke | Rumpf 17,1, Kopf 15,1 cm | Dead: Kopf zum Boden (Hals/Kopf je 9,37 Grad), Beine am Schulter-/Hueftgelenk um die waagerechte Achse quer zum Bein gehoben (VL 24,8 / HL 21,6 / VR 4,5 / HR 8,0 Grad), dann Hub; Death mit Rampen (links im Kippen Bild 16-34, rechts Bild 33-44, Kopf ssf(0,55;0,92)), Hub-Sprung im Sturz 1,5 cm/Bild (`fix/werkzeug/tot_loesen.py`, `tot_death.py`, `abw_bauen_fix.py`) | **Dead: Rumpf 0,31, Kopf 0,30, Netz ohne Krallen 0,30, Krallen 0,10 cm** (Pruefer-Werkzeug `fix/pt/pt_vergleich.json`); Death ab Bild 44 Rumpf 0,24-0,75 cm, Bild 47-57 hebt sich der Rumpf bis 2,58 cm (das tut der Erwachsene dort auch: +2,0 cm "letzter Atemzug"), ab Bild 58 0,3-0,9; Death-Ende = Dead (Haut 0,000 cm). Blatt `fix/bilder/N1_tod.png`, `N1b_tod_ton.png` |
| **M2 major** Sitz-Trio: Unterschenkel im Unterarm | Sit 6-16 Punkte je Bein bis 3,3 cm, SitDown/StandUp 20/3-7 Bilder | Sitzpose neu geloest (`baer_clips_rig.py` RIG-Vorgabe, Variante s6): Kniepol nach aussen (hpole y 0,15 -> 0,30; das Knie geht an die Drehgrenze des Oberschenkels), Sprunggelenk \|y\| 0,345 -> 0,37, Hinterfuss-Gieren 20 -> 8, Pranken \|y\| 0,098 -> 0,095, Zwischenplatz y 0,095 -> 0,09 | **Strahl-Test (`pt_durch2.py` des Pruefers, am neuen Dump): 0 Punkte in SitDown, Sit, StandUp** (alle Bilder; Sit jedes 4.). Eigener Test (`fix/werkzeug/durch.py`, Endgewichte): 0. Grobe 30-%-Kapsel (`sitz_pruef.py`): SitDown 1 Punkt in 2 Bildern, Sit/StandUp 0 (vorher 10-14) |
| **M3 major** Gang nur bei 0,35 ohne Gleiten (Wachsen B1d bis 0,75) | -- | **nicht im Modell loesbar** (Rechnung des Pruefers bestaetigt: Pfote in Welt = 1,5 x Groesse x Modell, Wurzel = 1,6 x Weg, beide x Abspieltempo -> Verhaeltnis Groesse/0,35). CLIPS.md 8.1.1 berichtigt | Frage an Kevin (5.1). Walk/Run byte-gleich mit vorher |
| M4 minor Death im Kippen Stuetzpfoten > 1,5 | 22 Stuetzbilder > 1,5, max 12,54 cm | mit M1: rechte Stuetzbeine im Kippen <= 3 Grad (VR 7 Bilder max 2,33, HR 13 Bilder max 2,67) | **0 Stuetzbilder > 1,5**, 21 > 1,0, max **1,38 cm** (Bild 9 und 25; `fix/pt/pt_mess.json`) |
| M5 minor Eat: Schnauze nicht am Boden, Grenze unklar | Kopf vor die Brust, tiefste Kopfhaut 42,3 cm, Augen-Nase -89..-68 | Hals -25,5 / Kopf -9,5 Grad (Kopf vorgestreckt statt vor die Brust; je Knochen <= 25,5, zusammen 35,0 = RIG_PLAN 5.2 "hoechstens 35") | tiefste Kopfhaut **51,8..57,6 cm** (im Spiel ~18 cm; also 9 cm hoeher als vorher), Augen-Nase **-73..-33**, 0 Kopfpunkte < 1,5 cm an Brust/Arm (vorher 1 in der eigenen Probe, 3-6 laut CLIPS.md), Dehnung Eat max 2,17 (vorher 2,91). Boden weiter unerreichbar -> Frage 5.2 |
| M6 minor Krallen an der Netzgrenze | Dead Krallen -0,5 | mit M1 | **Dead Krallen +0,10 cm** (>= -0,3 erfuellt). Swipe/Slam/Bite/Maul/Eat unveraendert -0,50..-0,43 (stehende Clips, Grenze ">= -0,5" gilt). Death im Kippen Krallen -0,33 (Erwachsener dort -0,03; vorher -0,50) |
| M7 minor CLIPS.md ungenau | 3 Stellen | Hinweisblock "NACHBESSERUNG" oben in `rig/CLIPS.md` berichtigt (1) Death liegt, (2) Dead aufliegend, (3) Abspieltempo hilft nicht | -- |

### PRUEF_OPTIK
| ID | gemacht | nachher (selbst angesehen) |
|---|---|---|
| **M1 major** Eat: Ei ohne Gesicht | wie Technik M5 | aus Kevins Kamera: Stirn, Ohren und Schnauzenspitze sichtbar, Kopf vor den Schultern; im Kauen (Bild 48/72) ganzes Gesicht (`fix/bilder/N3_eat.png`). Fressen am Boden geht weiter nicht (Frage 5.2) |
| **M2 major** Ohren als dunkle Scheiben aus az 0/el 30 | Textur: nur die Ohrmuschel (Ohr-Dreiecke mit Normale nach vorn, `fix/werkzeug/ohr_maske.py`) heller und kontrastaermer, Fellstruktur bleibt (`fix/werkzeug/tex_ohr.py k=0,55`; Muschel-Helligkeit p10/50/90 52/80/104 -> 74/84/104). Form unveraendert | die "drittes Augenpaar"-Scheiben sind weg, die Ohren lesen als weiche Ohrbecher, das Gesicht bleibt der Blickfang; aus az 45/90 weiter runde Ohren mit hellerem Inneren (`N4_ohren.png`, Probe 3 Staerken `fix/bilder/probe_ohr*.png`). Gesicht sitzt aus el 30 weiter klein unten (Kopfhaltung, Frage 5.3) |
| **M3 major** Gleiten ab Groesse 0,5 | wie Technik M3 | Frage 5.1 |
| m1 Aufsetz-Rutscher Walk/Run | **nicht gemacht** (Gang unveraendert, byte-gleich) | Walk VL 9,9 / HR 6,9 / VR 2,1 cm im Aufsetzbild (im Spiel 0,7-3,5 cm) -- im Spiel ansehen |
| m2 Maul Kopf an der Brust | nicht gemacht (das Junge spielt Maul heute vermutlich nicht; nur die Feed-Aktion setzt eine Aktion, ungeprueft) | unveraendert |
| m3 "Ei auf Stelzen" von hinten | nicht gemacht (Form, Kevins Wort) | unveraendert |
| m4 Kleinigkeiten im Ton nah | nicht gemacht (Form) | unveraendert; Leisten-Strich SitDown: Dehnung dort jetzt max 3,79 |
| m5 Kopf/Rumpf starr im Gang | nicht gemacht | unveraendert |
| m6 Pfoten/Sohlen | nicht gemacht | unveraendert; im Sitzen zeigen die Zehen jetzt 34 statt 18 Grad nach aussen (Folge von M2), die Sohlen stehen weiter nach vorn |
| m7 Fellfarbe | nicht gemacht (Kevins Wahl) | unveraendert |

## 2. Feste Regeln am Endergebnis (selbst gemessen)
| Regel | Grenze | Ergebnis |
|---|---|---|
| Dreiecke / Netz / Material | <= 20.000 / 1 / 1 | 19.418 / 1 Netz, 1 Primitiv / 0 Material-Eintraege wie Erwachsener |
| Knochen, Einfluesse | 26 Namen wie Erwachsener; <= 4, Summe 1 | gleich (`fix/pt/pt_glb.json`); 4, 0,9999999-1,0000002 |
| Clips | 15 Namen, Dauer, Abtastzeiten wie Erwachsener | gleich; Zeit-Kanaele byte-gleich; Dreh-Kanaele 234/390 byte-gleich (vorher 242; neu abweichend: Death/Dead L/R_UpperArm, L/R_Thigh) |
| Textur | 1024 x 1024 RGB 8 Bit | ja (Farbtyp 2, kein Alpha) |
| Namen / Massstab | NCBearCub.glb/.png, Mesh NCBearCub; 0,544 E/m | unveraendert (Netz, Skelett, Gewichte unveraendert) |
| Dehnung p99,5 / max / Achsel-Brust | 2,6 / 4,0 / 3,5 | **2,30 / 3,79 (SitDown Leiste) / 3,23**; je Clip: Idle 1,14/1,30, Walk 1,69/2,82, Run 1,72/2,68, Death 1,75/2,76, Dead 1,95/2,76, Rear 2,30/3,23, SwipeL 1,87/3,50, SwipeR 1,96/3,27, Slam 1,90/2,71, Bite 1,54/2,71, Maul 1,80/2,83, Eat 1,39/2,17, SitDown 2,08/3,79, Sit 2,17/3,47, StandUp 1,92/3,77 |
| Boden Stuetzpfoten | <= 1,5 cm, alle Clips | **alle 15 Clips -0,50..+1,38**, 0 Stuetzbilder > 1,5 (Death 21 > 1,0; SwipeR/Maul je 1 > 1,0 wie vorher) |
| Netz | >= -0,5 | min -0,50 (Krallen stehender Clips), Dead +0,10 |
| Risse | keine | Netz, UV-Naehte und Gewichte unveraendert (geschlossen); im Ton aller Blaetter keine Risse |
| Tempo | Walk 1,60 / Run 2,61 | 1,603 / 2,613 Kacheln/s (unveraendert) |
| Uebergaenge | | Walk/Run/Idle/Eat/Sit erstes = letztes 0,0; SitDown-Ende = Sit 0 = StandUp-Anfang 0,0; Death-Ende = Dead 0,0 |
| Sitzen (D.4/RIG 5.4) | | Sitzflaeche 0,08, Ferse 0,10, Pranken 0,00 cm; Ellbogen 168,0; Unterarm 7,3/-0,9 Grad; Hinterfuss-Mitten **0,743 m**; Pranken-Luecke **1,0 cm** (Grenze 1-4); Innenkante 8,8 cm; Knie 140,1; Blick -34,9..-34,0; Kopf gg. Hals 22,3 |

## 3. Abweichungen von Plan/SPEZ (bewusst, mit Grund) -- bitte Lead/Kevin bestaetigen
1. **Death/Dead: Beine gedreht (UpperArm/Thigh bis 24,8 Grad).** SPEZ D.5 erlaubt dort nur Hals/Kopf/Hub. Ohne Beine lag das Junge 17 cm
   hoch auf der linken Pranke (Regel "aufliegende Haut 0..1,2" und "Boden <= 1,5 in allen Clips" verletzt). Der Pruefer hat genau das
   vorgeschlagen. Rechte Stuetzbeine im Kippen bis 3 Grad am Oberschenkel (D.5 nennt fuer IK nur Arm-Knochen).
2. **Death: Hub-Sprung 1,5 cm/Bild** im Sturz (SPEZ D.2: 0,3; Bauer hatte 1,2). Das Junge faellt mit dem Erwachsenen; so schwebt nichts.
3. **Eat: Kopf HOEHER statt tiefer.** RIG_PLAN 5.2 sagt "so tief wie moeglich, melden". Tiefer (38-42 cm) heisst Kopf an die Brust =
   gesichtsloses Ei (Optik M1). Gewaehlt: Gesicht sichtbar, 51,8 cm. Grenze gelesen als je Knochen <= 25,5, zusammen <= 35.
4. **Sitzen: Zehen 34 statt 10-25 Grad nach aussen, Sohlen-Normale 4 statt 10-25 Grad hoch.** Das Knie steht an der Drehgrenze, der Fuss
   wird an der Pfotengrenze geklemmt (Log "schwenk"/"pfote"); mehr Abstand Bein/Arm geht innerhalb der Gelenkgrenzen nicht anders.
   Pranken-Luecke 1,0 cm = untere Grenze.
5. **Ohr-Textur geaendert** (nur Farbe der Muschel, keine Form). Die von GEGEN_OPTIK gelobte "dunkle Muschel mit hellem Saum" aus az 45
   ist dadurch weicher.

## 4. Lehre (fuer spaetere Laeufe)
- `rl.Netz()` ohne Argument nimmt die **Vorab-Gewichte der Rolle SKELETT** (`skelett/gewichte_rig.npz`), nicht `clips/gewichte_end.npz`.
  Mit den Vorab-Gewichten zeigten alle Sitz-Varianten 0 Punkte, mit den Endgewichten 3 Punkte in SitDown/StandUp. Durchdringung und Boden
  immer mit den Endgewichten bzw. am Dump messen. (`sitz_loesen.py` des Bauers loest die Sitzhoehe ebenfalls mit den Vorab-Gewichten;
  am Dump liegt die Sitzflaeche bei 0,08 statt 0,15 cm -- innerhalb 0,0..0,3.)

## 5. Fragen fuer Kevin
1. **Wachsen gegen Gangbild:** Das Junge geht nur bei Groesse 0,35 ohne zu rutschen. Wenn es (B1d) bis 0,75 waechst, rutschen die Pfoten
   je Schritt bis ~15-21 cm (im Spiel). Ein anderes Abspieltempo hilft nicht. Moeglich: (a) bei 0,35 lassen bis zum grossen Modell,
   (b) Gang-Clips je Groessenstufe (Code-Lauf waehlt sie), (c) kleineres cubMaxSize.
2. **Fressen:** Das Junge streckt beim Fuettern den Kopf vor, die Schnauze bleibt ~18 cm (im Spiel) ueber dem Boden -- passt zum Fuettern
   aus der Hand? Oder ein eigener Fress-Clip (Vorderbeine einknicken, Schnauze am Boden)?
3. **Kopfhaltung:** Aus deiner Kamera sitzt das Gesicht beim Stehen/Gehen klein unten am Umriss. Kopf ~10 Grad hoeher tragen?
4. **Sitzen:** Die Hinterpfoten zeigen jetzt etwas mehr nach aussen (34 statt 18 Grad), damit Bein und Arm sich nicht mehr durchdringen. Ok?
5. **Ohren:** Innen jetzt heller (weniger "Augen" von vorn). Gefaellt dir das, oder lieber wieder dunkler?
6. Weiter offen aus den Pruefberichten: Aufsetz-Rutscher im Gang (m1), Galopp starr (m5), Sohlen ohne Ballen (m6), Fellfarbe (m7),
   Hinterteil von hinten (m3).

## 6. Dateien
| Datei | Inhalt |
|---|---|
| `rig/out/...NCBearCub.glb`, `...NCBearCub.png`, `rig/out/md5.txt` | **Endergebnis** |
| `rig/out_vor_fix/` | Stand vor der Nachbesserung |
| `baer/spiel/baer_clips_rig.py` | Sitz-Vorgabe neu (Kommentar "NACHBESSERUNG 11.11."), neuer Schalter `ferse_dy_auf` (Vorgabe = ferse_dy) |
| `rig/fix/werkzeug/abw_bauen_fix.py` | D.5 + Hub mit neuem Death/Dead/Eat (Kopie der Logik von `rig/werkzeug/abw_bauen.py`, Original unveraendert) |
| `rig/fix/werkzeug/tot_probe.py`, `tot_loesen.py`, `tot_death.py` | Liegepose und Sturz (Beine heben, Rampen, IK rechts) |
| `rig/fix/werkzeug/sitz_loesen_fix.py`, `sitz_var2.sh`, `sitz_vgl.py`, `sitz_dehn.py`, `durch.py`, `durch_ort.py` | Sitz-Varianten loesen, Strahl-Test (Endgewichte), Dehnung je Variante |
| `rig/fix/werkzeug/eat_probe.py`, `ohr_maske.py`, `tex_ohr.py` | Eat-Varianten, Ohr-Maske, Ohr-Textur |
| `rig/fix/werkzeug/ende_fix.sh`, `render_fix.py`, `blaetter_fix.py`, `probe1.py` | Endkette, Renders, Blaetter |
| `rig/fix/clips/` | `clips_neu(_posen).npz`, `abw/` (abw.npz, hub.json, abw_bericht.json), `dump_final.txt(.pkl)`, `pruef_*.json`, `dehnung_final.json`, `sitz_pruef_final.json`, `gang_pruef_final.json`, `sitz/` (Varianten a-s7) |
| `rig/fix/pt/` | Werkzeuge des Pruefers TECHNIK, auf den neuen Dump umgestellt: `pt_glb/pt_mess/pt_vergleich/pt_durch2` (.json/.log), `pt_durch2_ort.py` |
| `rig/fix/log/` | alle Logs |
| `rig/fix/bilder/N1_tod.png`, `N1b_tod_ton.png`, `N2_sitzen.png`, `N3_eat.png`, `N4_ohren.png` | vorher/nachher (selbst angesehen) |
| `rig/fix/bilder/probe_eat*.png`, `probe_ohr*.png`, `probe_tot1.png` | Proben (Eat 5 Varianten, Ohr-Textur 3 Staerken) |
| `rig/fix/bilder/blaetter/clips*.png` | Clip-Blaetter des Bauers neu aus dem Endergebnis (alle 15 Clips Kevins Kamera, 45 Grad, Gang, Sitzen, Ruhe, Vergleich Platzhalter, R6) |

Wiederholen (R = `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig`):
```
NCB_RIG_AUS=$R/fix/clips/clips_neu_posen.npz blender --background --factory-startup --python .../baer/spiel/baer_clips_rig.py -- x
python $R/werkzeug/wandle.py $R/fix/clips/clips_neu_posen.npz $R/fix/clips/clips_neu.npz
python $R/fix/werkzeug/abw_bauen_fix.py $R/clips/zw/dump_zw.txt.pkl $R/clips/gewichte_end.npz $R/fix/clips/abw
python $R/fix/werkzeug/tex_ohr.py $R/out_vor_fix/42/media/textures/Body/NCBearCub.png $R/fix/tex/NCBearCub.png k=0.55
sh $R/fix/werkzeug/ende_fix.sh            # Export, Harness, Pruefungen -> fix/out; danach nach rig/out kopieren + md5
cd $R/fix/pt && python pt_mess.py pt_mess.json && python pt_vergleich.py && python pt_durch2.py
```
