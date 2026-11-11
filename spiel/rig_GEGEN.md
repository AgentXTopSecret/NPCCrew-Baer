# GEGEN -- Lauf baer-rig-junges, Rolle GEGENPRUEFER (11.11.2026, ~13:50-14:40)

**Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und nichts am Endergebnis geaendert. Geschrieben nur unter `rig/gegen/`
(eigene Werkzeuge, eigene Harness-Dumps, Renders, Pruefblaetter), `rig/bilder/KEVIN_junges_spielfertig.png` und diese Datei. Kein git,
kein Download, nichts in Test-Mods, NPC Crew, Spiel oder `_arbeit/baer_zaehmen/mod/`. GPU nur ueber `_arbeit/baer_gen/werkzeug/gpu_lauf.sh`
(3 Laeufe, Sperre danach frei). Zahlen bei Groesse 1,0 (im Spiel x 0,35), Rahmen tier (x vorn, y links, z oben, Boden z 0).

Geprueft: `rig/out/42/media/models_X/Skinned/NCBearCub.glb` **ee7a0cce2efb188e307b8f51a090b868** und
`rig/out/42/media/textures/Body/NCBearCub.png` **92a829fab0a23521cc00bcebeb42c9d0** (= `rig/out/md5.txt`, selbst nachgerechnet).
Vergleich: Platzhalter NCBearTest `NCBearCub.glb` 6c3f0a96 / `.png` 2ee25f24, Erwachsener `NCBear.glb` 08ec7806 (nur gelesen, Kopien in `gegen/dump/`).

## 0. Urteil kurz
- **(a) ersetzt_platzhalter: JA -- das neue Junge ist klar besser.** Es sieht aus wie Kevins Foto (kompakt, runder Kopf, grosse runde
  Ohren, hohe Beine), sitzt wie die Sitzvorlage, liegt tot flach auf der Seite, geht 3x so schnell ohne Rutschen. Der Platzhalter wirkt wie
  ein langer, flacher erwachsener Baer, seine Vorderpfoten schweben im Gang, die Hinterpfoten rutschen 15-50 cm (im Spiel) je Schritt.
- **(b) bereit_fuer_test_mod: JA.** Der Harness laedt die Datei (26 Knochen, 15 Clips), alle festen Regeln halten (selbst gemessen,
  Tabelle 2), keine Risse (0 offene Kanten, Naht-Punkte bleiben in allen 874 Bildern beisammen), nichts schwebt, Stuetzpfoten <= 1,38 cm.
- **Offen bleibt (kein Blocker, Kevins Wort):** (1) M3 Wachsen: ueber Groesse 0,35 rutschen die Pfoten im Gang (bei 0,75 bis ~21 cm je
  Schritt im Spiel) -- im Modell nicht loesbar, Code-Frage `cubMaxSize`; der Platzhalter rutscht bei JEDER Groesse gleich viel oder mehr.
  (2) Fressen: Schnauze ~18 cm (im Spiel) ueber dem Boden. (3) Kopf vorn gesenkt, Gesicht aus Kevins Kamera klein unten.

## 1. Wie geprueft (unabhaengig von Bauer und Pruefern)
- **Eigene Harness-Laeufe:** `Dump.java` (unveraendert) auf `neu.glb` (Kopie von `rig/out`, MD5 gleich), Platzhalter und Erwachsenen ->
  `gegen/dump/*.txt`; alle drei "OK ... Knochen 26 Clips [15 Namen]". Mein Dump von `rig/out` ist byte-gleich mit `fix/clips/dump_final.txt`
  (MD5 61580dd0).
- **Eigener Leser und eigene Haut** (`gegen/werkzeug/g_lib.py`, nur numpy): v' = Summe w * M * OFF * v. Konvention am Dump geprueft:
  Idle Bild 0 gegen Rohpunkte Median 0,85 cm (Ruhe ~ Idle), Boden bei z 0. Bereichs-Etiketten (Krallen, Pfoten, Kopf) aus `skelett/netz_rig.npz`
  ueber Punkt-Lagen zugeordnet (11.811/11.811, Abweichung < 0,1 mm), gegen Gewichtsmasken gegengeprueft.
- **Eigene Messungen:** `g_fakten.py` (Datei-Regeln, Knochen, Clips, Kanten, Naehte, Textur, GLB-Aufbau), `g_mess.py` (Boden je Pfote und
  Bild, Liegen, Fressen, Dehnung wie `baer_gewichte_rig.dehnung` nachgebaut, Uebergaenge, Tempo, Gleiten der Haftpunkte in Welt bei 0,35 /
  0,5 / 0,75), `g_durch.py` + `g_wirt.py` (**neues Verfahren:** Durchdringung des ganzen Netzes mit sich selbst ueber die Windungszahl, jeder
  Punkt jedes Bildes aller 15 Clips, dazu "Gast steckt in Wirt" je Koerperteil) -- fuer neu, Platzhalter und Erwachsenen.
- **Eigener Renderer** `g_render.py` (Cycles OPTIX, orthografisch), rund 780 Bilder: alle 15 Clips x 4 Phasen aus Kevins Kamera (az 0 / el 30)
  gross + Ton + Spielgroesse 1:1 (110 px/m = 577 px/E bei 0,35) und aus az 45; Ruhe 8 Seiten; Liegen, Sitzen, Fressen aus 6 Seiten; Gang
  alle Bilder; Sterben/Hinsetzen/Aufstehen/Fressen als Streifen; Platzhalter dasselbe. **Alle Blaetter selbst angesehen** (Abschnitt 6).

## 2. Feste Regeln -- selbst gemessen am heutigen `rig/out`
| Regel | Grenze | gemessen | |
|---|---|---|---|
| Harness laedt | OK | OK, 26 Knochen, 15 Clips, 11.811 Punkte | ok |
| Dreiecke | <= 20.000 | **19.418** | ok |
| Netz / Material | 1 / 1 | GLB: 1 Mesh, 1 Primitiv, 0 Material-, 0 Bild-Eintraege (wie Erwachsener), Indizes u16 | ok |
| Knochen | 26, Namen wie Erwachsener | 26, Namen, Eltern, Reihenfolge, Skin-Joints, Knoten-Drehungen gleich (nur Mesh-Knoten heisst NCBearCub) | ok |
| Einfluesse | <= 4, Summe 1 | 4, Summe 0,99999986-1,00000017, kein NaN | ok |
| Clips | 15 Namen, Dauer, Abtastzeiten wie Erwachsener | alle 15 gleich (Dauer-Text und alle Zeiten byte-gleich im Dump, Zeit-Accessoren gleich); Skalier-Schluessel 1 +- 2,6e-5 (wie Erwachsener); Lage-Schluessel konstant ausser Pelvis/Translation_Data | ok |
| Textur | 1024 x 1024 RGB | 1024 x 1024, Modus RGB, kein Alpha; gegen `out_vor_fix` nur 4.905 Texel (Ohrmuschel) geaendert | ok |
| Namen | NCBearCub.glb/.png, NCBearCub_Body, animationsMesh NCBearCub | Dateinamen gleich; Skript `nc_bear_cub.txt` verweist auf genau diese | ok |
| Massstab | 0,544 E/m, gebaut bei 1,0 | Idle 0 bei 1,0: Laenge 1,42 m, Hoehe 1,24 m (mit Ohren), Breite 0,61 m; tiefster Punkt -0,2 cm | ok |
| Dehnung | p99,5 <= 2,6; max <= 4,0; Achsel/Brust <= 3,5 | **2,30 / 3,79 (SitDown, Leiste) / 3,23 (Rear)** -- alle 15 Clips eigene Rechnung, gleich mit NACHBESSERUNG +-0,01 | ok |
| Boden Stuetzpfoten | <= 1,5 cm, alle Clips | 13 Clips mit Erwachsenen-Stuetzbildern: max **1,38** (Death VL), 0 Bilder > 1,5, 23 > 1,0; Walk/Run (neuer Gang): Pfoten in der Stuetze -0,03..+0,9 | ok |
| Netz im Boden | >= -0,5 cm | min **-0,5005** (Krallen SwipeR; Hub klemmt dort, 0,05 mm drueber = im Spiel 0,0002 cm), Dead +0,10 | ok (an der Grenze) |
| Liegen (aufliegende Haut) | 0..+1,2, nie < -0,3 | Dead: Rumpf **0,31**, Kopf **0,30**, Krallen 0,10 cm; Death-Ende = Dead | ok |
| Risse | keine an Hals/Achsel/Leiste | 0 offene / 0 nicht-mannigfaltige / 0 entartete Kanten, 1 Zusammenhangsteil; 2.100 Naht-Paare (UV-Naehte) in allen 874 Bildern 0,000 cm auseinander. Im Ton nur Faltenstriche (m4), keine offenen Stellen | ok |
| Uebergaenge | | Idle/Walk/Run/Eat/Sit erstes = letztes 0,000 cm; SitDown-Ende = Sit 0 = StandUp 0 und Death-Ende = Dead 0,000 cm; Idle 0 -> SitDown 0 4,4 cm (Erwachsener 6,5) | ok |
| Tempo | Walk 1,60 / Run 2,61 | **1,603 / 2,613** Kacheln/s (Weg x MotionScale 1,6 / Dauer; Beleg `AnimationPlayer.java:1235`, `Defaults.xml:3`; Bild 1,5 x Groesse `IsoAnimal.java:2602`) | ok |

## 3. Je Mangel der Pruefer: geschlossen?
### PRUEF_TECHNIK
| ID | Befund (kurz) | heute gemessen / gesehen | Urteil |
|---|---|---|---|
| M1 major | Tote stehen auf der Pranke, Rumpf 15-19 cm hoch | Dead: Rumpf 0,31, Kopf 0,30 cm; Death ab Bild 44 Rumpf 0,24-2,58 (Bild 47-57 "letzter Atemzug", Erwachsener ebenso). Bild: liegt flach auf der rechten Seite, Beine ausgestreckt, aus allen 6 Seiten | **geschlossen** |
| M2 major | Sitz-Trio: Unterschenkel im Unterarm | eigener Windungszahl-Test, alle Bilder SitDown/Sit/StandUp: **0 Punkte Unterschenkel/Fuss im Arm, 0 Unterarm/Pfote im Bein**. Was bleibt, sind Hautfalten innerhalb eines Teils (Achsel, Knie-Kehle beim Aufstehen), beim Erwachsenen mehr | **geschlossen** |
| M3 major | Gang rutscht bei Groesse > 0,35 | unveraendert: Walk je Stuetzphase bei 0,5 bis 15,5 cm Modell (~7,8 cm im Spiel), bei 0,75 bis 27,9 (~21 cm); Run 10,0 (~5,0) / 24,0 (~18 cm). Platzhalter dagegen (gleiche Rechnung): Walk 0,35/0,5/0,75 = 30 / 27 / 23 cm im Spiel, Run bis 50 cm. Rechnung "Abspieltempo hilft nicht" bestaetigt | **offen, nicht im Modell loesbar** (Frage 1) |
| M4 minor | Death im Kippen Stuetzpfoten > 1,5 | 0 Stuetzbilder > 1,5, max 1,38 (VL), 21 > 1,0 | **geschlossen** |
| M5 minor | Eat: Schnauze nicht am Boden | tiefste Kopfhaut 51,8 cm (im Spiel ~18 cm), Platzhalter 0,2, Erwachsener ~0. Neck -25,5 / Head -9,5 Grad gegen den Erwachsenen (Summe 35 = RIG_PLAN 5.2, ueber SPEZ D.5 "zusammen <= 15") | **bewusst offen** (Frage 2) |
| M6 minor | Krallen an der Netzgrenze | Dead Krallen +0,10 (>= -0,3 erfuellt); stehende Clips -0,50 wie vorher | **geschlossen** fuers Liegen |
| M7 minor | CLIPS.md widerspricht Messung | Hinweisblock oben in CLIPS.md berichtigt die drei Stellen; NACHBESSERUNG-Zahlen habe ich auf +-0,01 nachgemessen (Dehnung, Boden, Tempo, Liegen) | **geschlossen** |

### PRUEF_OPTIK
| ID | Befund (kurz) | heute gesehen | Urteil |
|---|---|---|---|
| M1 major | Eat: Ei ohne Gesicht, Kopf an der Brust | Kopf jetzt vorgestreckt und gesenkt, keine Kehl-Stauchung. Aus Kevins Kamera Bild 48/72 Gesicht ganz sichtbar; im tiefsten Bild (21/24) sieht man weiter v. a. Stirn, Ohren und Nasenspitze -- wirkt wie "Kopf runter zur Hand", nicht kaputt. Aus 45/90 klar ein Junges mit gesenktem Kopf | **weitgehend geschlossen**, Rest = Frage 2 |
| M2 major | Ohren als dunkle Scheiben ("drittes Augenpaar") aus az 0/el 30 | Muschel heller, liest sich gross und in Spielgroesse 1:1 (auch 2x pixelgetreu angesehen) als zwei Ohrbecher ueber dem Gesicht, nicht als Augen. Gesicht sitzt aus el 30 weiter klein unten (Kopfhaltung) | **geschlossen**; Rest Kopfhaltung = Frage 3 |
| M3 major | Gleiten beim Wachsen | wie Technik M3 | **offen** (Frage 1) |
| m1 | Aufsetz-Rutscher | Walk: VL 9,9 / HR 6,9 / VR 2,1 cm im Aufsetzbild (Pfote < 1 cm ueber dem Boden in zwei Folgebildern), danach 0,0-0,1; Run VL 8,6 / VR 3,6. Im Spiel x 0,35 = hoechstens 3,5 cm fuer 1/30 s. Erwachsener bei 1,0 bis 4,5 (Walk) / 13,5 (Run) je Phase | offen, minor |
| m2 | Maul: Kopf an der Brust | unveraendert (Bild 12/24 von vorn nur Oberkopf und Ohren). Kampf-Clip, vom Jungen heute kaum gespielt (ungeprueft) | offen, minor |
| m3 | von hinten "Ei auf Stelzen" | unveraendert (schmal, runder Hintern, duenne dunkle Beine) | offen, minor (Form) |
| m4 | Kleinigkeiten im Ton nah | unveraendert: Faltenstriche an Unterarm/Brust in Rear/Swipe/Sit (Ton), lokal umgeklappte Dreiecke je Bild hoechstens 205 (Run) / 342 (StandUp), Erwachsener 614 / 497. Mit Textur und 1:1 unsichtbar | offen, minor |
| m5 | Galopp starr | unveraendert | offen, minor |
| m6 | Pfoten/Sohlen | unveraendert; Sitz-Sohlen dunkle Ovale (Platzhalter: graue Sohlen) | offen, minor |
| m7 | Fellfarbe flau | unveraendert (Kevins Wahl C-12) | offen, minor |

## 4. Eigene Befunde (neu)
| ID | Schwere | wo | Befund |
|---|---|---|---|
| G1 | minor | Death ab ~Bild 36, Dead | **Die Beine stecken im Liegen ineinander:** Unterarm L in Arm R bis 455 Punkte, Unterschenkel R in Bein L bis 385 (Windungszahl-Test). Der Erwachsene hat dasselbe (361 / 214, gleiche Drehungen), das Junge mehr wegen der schmalen Spur. Im Bild aus allen 6 Seiten liest es sich als uebereinanderliegende Beine, kein Loch, kein Flackern. |
| G2 | minor | Ruhe/Gang aus az 45 | Das nahe Ohr zeigt sich als runde Scheibe seitlich am Kopf (Muschel nach vorn-aussen), im Foto stehen die Ohren mehr oben. Kopf-Aussenform des Generators (feste Regel), daher nur Beobachtung. |
| G3 | Hinweis | Swipe/Bite/Maul/Slam | Netz-Minimum -0,5005 cm = an der Grenze -0,5 (Rundung des Hubs, 0,05 mm). Unsichtbar. |
| G4 | Hinweis | Ruhe, Brust-Mittellinie zwischen den Vorderbeinen | 4 Punkte einer Spiegelnaht ueberschneiden sich schon in der Ruhe (Falte, < 2 mm). Unsichtbar. |
| G5 | bestaetigen | Death/Dead, Eat | **Bewusste Abweichungen von SPEZ D.5** (NACHBESSERUNG 3): Death/Dead L_UpperArm 24,8 / L_Thigh 21,6 / R_Thigh 8,0 / R_UpperArm 4,5 / Neck, Head je 9,4 Grad; Eat Neck 25,5 / Head 9,5 Grad. Gemessen genau so (alle anderen Dreh-Kanaele wie berichtet). Begruendung traegt (sonst liegt das Junge nicht / Kopf an der Brust); Lead/Kevin bestaetigen. |

## 5. Alt gegen neu (gleiche Rechnung, gleicher Massstab)
| | ALT (Platzhalter heute) | NEU |
|---|---|---|
| Gestalt | lang und flach (1,86 m bei 1,0), kleine Ohren, helle Schnauze, "erwachsener Baer / Wombat" von der Seite | kompakt (1,42 m), grosser runder Kopf, grosse runde Ohren, hohe Beine -- wie das Foto |
| Aus Kevins Kamera (az 0) | Gesicht gross und gut lesbar, breiter Kasten | schmaler, Kopf gesenkt, Gesicht kleiner, Ohren klar |
| Gehen | 0,52 Kacheln/s; Vorderpfoten schweben (2-9 cm), Hinterpfoten sinken bis -2,9 cm und rutschen 15-30 cm (Spiel) je Schritt | 1,60 Kacheln/s (Trab); Stuetzpfoten stehen, nur Aufsetzbild <= 3,5 cm (Spiel) |
| Rennen | 2,47 Kacheln/s, Hinterpfoten rutschen bis 50 cm (Spiel) | 2,61 (Galopp), Aufsetzbild <= 3,0 cm |
| Sitzen | Froschmaul-Strich, graue Sohlen gespreizt | aufrecht wie Kevins Sitzvorlage, Vorderbeine gerade dazwischen |
| Fressen | Schnauze am Boden (0,2 cm) | Kopf gesenkt, ~18 cm (Spiel) ueber dem Boden |
| Liegt tot | Rumpf 2,3 / Kopf 4,9 cm | Rumpf 0,31 / Kopf 0,30 cm |
| Selbst-Durchdringung Ruhe (Punkte) | 415 (Kopf/Kiefer/Pfoten) | 22 (Brustfalte) |

## 6. Bilder (alle selbst angesehen)
| Datei | Inhalt |
|---|---|
| **`rig/bilder/KEVIN_junges_spielfertig.png`** (2760 x 3888) | oben Foto + NEU aus Kevins Kamera gross + schraeg; Kopf nah, Foto-Winkel; Ruhe 8 Seiten 1:1 und gross; Reihe je wichtiger Clip (Gehen, Rennen, Hinsetzen, Sitzen, Fressen, Sterben, Liegt tot, Aufrichten) aus az 0 und 45 + 1:1; Reihe ALT gegen NEU (Ruhe, Gehen, Sitzen, Fressen, Liegt tot) gross, 45 und 1:1 |
| `rig/gegen/bilder/G1_clips_K.png`, `G1_clips_45.png` | alle 15 Clips x 4 Phasen: gross Textur, Ton, 1:1 |
| `rig/gegen/bilder/G2_alt_neu_K.png` | ALT gegen NEU aus Kevins Kamera, 7 Clips x 4 Phasen, gross und 1:1 |
| `rig/gegen/bilder/G3_ruhe8.png` | Ruhe 8 Seiten neu (1:1, gross, Ton) und alt |
| `rig/gegen/bilder/G4_pruefansichten.png` | Liegt tot 6 Seiten (neu Textur/Ton, alt), Sitzen 6 Seiten, Fressen tiefstes Bild, hinten, unten, Foto-Winkel |
| `rig/gegen/bilder/G5_streifen.png` | Gang/Galopp alle Bilder von der Seite (Ton) + 1:1, Sterben/Hinsetzen/Aufstehen/Fressen als Streifen |

## 7. Fragen fuer Kevin
1. **Wachsen gegen Gang:** Das neue Junge geht nur bei Groesse 0,35 ohne Rutschen. NCBearTest zeigt es heute bis 0,75 (`cubMaxSize`);
   dann rutschen die Pfoten bis ~21 cm je Schritt (beim Platzhalter heute 15-50 cm bei jeder Groesse). Lassen, kleineres `cubMaxSize`, oder
   spaeter Gang-Clips je Groessenstufe?
2. **Fressen:** Das Junge senkt den Kopf zur Hand, die Schnauze bleibt ~18 cm ueber dem Boden. Passt das zum Fuettern aus der Hand, oder
   soll es einen eigenen Fress-Clip mit Schnauze am Boden geben?
3. **Kopfhaltung:** Aus deiner Kamera von vorn sitzt das Gesicht klein unten (Kopf gesenkt). Kopf etwas hoeher tragen (eigener Lauf)?
4. **Ohren:** Innen jetzt heller -- so lassen? (Aus 45 Grad wirken sie als runde Scheiben seitlich am Kopf.)
5. Sitz-Pfoten zeigen jetzt 34 statt 18 Grad nach aussen (damit Bein und Arm sich nicht durchdringen) -- ok?

## 8. Wiederholen (G = `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen`)
```
java -Djava.library.path="<Spiel>" -cp "<harness>;<Spiel>/projectzomboid.jar" Dump $G/dump/neu.glb $G/dump/neu.txt skin   (ebenso alt, erw)
python $G/werkzeug/g_fakten.py ; python $G/werkzeug/g_mess.py ; python $G/werkzeug/g_durch.py neu ; python $G/werkzeug/g_wirt.py neu
python $G/werkzeug/g_auftrag.py ; sh .../baer_gen/werkzeug/gpu_lauf.sh LOG blender -b --factory-startup --python $G/werkzeug/g_render.py -- $G/render/cfg.json
python $G/werkzeug/g_kevin_auftrag.py ; (Render cfg_kevin.json wie oben) ; python $G/werkzeug/g_blatt.py ; python $G/werkzeug/g_kevin_blatt.py
```
Ergebnisse: `gegen/g_fakten.json`, `g_mess.json`, `g_durch_{neu,alt,erw}.json`, `g_wirt_{neu,erw}.json`, Logs `gegen/log/`, Renders `gegen/render/r`, `render/k`.
