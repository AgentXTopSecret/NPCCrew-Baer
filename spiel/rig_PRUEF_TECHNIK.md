# PRUEF_TECHNIK -- Lauf baer-rig-junges, Rolle PRUEFER TECHNIK (11.11.2026, ~12:10)

**Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und nichts am Endergebnis geaendert. Geschrieben nur in
`rig/pruef_technik/` (eigene Skripte, eigene Harness-Dumps, JSON/Logs) und diese Datei. Kein git, kein Download, kein Render, keine
GPU; NCBearTest, NPC Crew, `_arbeit/baer_zaehmen/mod/` und das Spiel nur gelesen. Alle Zahlen bei Groesse 1,0 (Spiel: x 0,35),
Rahmen tier (x vorn, y links, z oben, Boden z 0), Haut aus dem Importer-Dump (Dump.java), wo nicht anders gesagt.

Geprueft: `rig/out/42/media/models_X/Skinned/NCBearCub.glb` (MD5 d89856ef508a0100dbb4e384f0ab4640, 1.235.544 Byte) und
`rig/out/42/media/textures/Body/NCBearCub.png` (MD5 8ce68838b0df138b7bf667b98d687800) -- beide MD5 stimmen mit `rig/out/md5.txt`.
Vergleich: gespielter Erwachsener `NCBearTest/.../NCBear.glb` (08ec7806) und heutiger Platzhalter `NCBearTest/.../NCBearCub.glb` (6c3f0a96).

## 0. Urteil kurz
**Technisch spielfertig: alle festen Datei-Regeln selbst nachgemessen und erfuellt; der Harness laedt es (26 Knochen, 15 Clips).**
Gehen 1,603 / Rennen 2,613 Kacheln/s bestaetigt, in der Stuetze gleitet bei 0,35 nichts (0,00-0,12 cm). Dehnung, Naehte, Topologie,
Uebergaenge sauber. **Drei Befunde, die vor dem Ersetzen entschieden werden sollten (major, kein Blocker):**
1. **Death-Ende/Dead: das tote Junge liegt nicht, es steht auf der linken Vorderpfote** -- Rumpf 14,7-18,9 cm ueber dem Boden
   (bei 0,35 ~6 cm), Kopf 15-26 cm; nur Pfote VL (Krallen -0,5) und HL (1,8) beruehren den Boden. Platzhalter: Rumpf 2,1-3,9 cm.
   Der Baubericht sagt "Koerper liegt dabei auf" / "Dead aufliegend +0,45" -- das ist die Pfote, nicht die Flanke.
2. **Sitz-Trio: Unterschenkel und Unterarm durchdringen sich** (Strahl-Test: 6-16 Punkte je Bein, bis 3,3 cm tief, in ALLEN
   Sit-Bildern, SitDown ab ~Bild 29, StandUp Anfang); Erwachsener mit derselben Rechnung 0. SPEZ D.4 / RIG_PLAN C4 sagen "hart 0".
3. **Wachsen (B1d) gegen Gang:** NCBearTest zeigt das Junge heute von 0,35 bis 0,75 (`cubMaxSize`). Der neue Trab passt NUR bei
   0,35; bei 0,5 gleiten die Stuetzpfoten ~11-16 cm (Modell) = ~6-8 cm im Spiel je Schritt, bei 0,75 ~20-28 cm = ~15-21 cm.
   (Platzhalter bei 0,35 heute: 42-86 cm Modell -- also auch dann noch besser als heute.) Ein Abspieltempo je Groesse hilft NICHT.

---------------------------------------------------------------------------------------------------------------------------

## 1. Feste Regeln -- selbst gemessen
Werkzeuge (alle eigen, nur numpy/struct/json): `pruef_technik/pt_glb.py` (GLB direkt), `pt_lib.py` (Dump-Leser, Haut),
`pt_mess.py` (Boden, Dehnung, Naehte, Topologie, Tempo, Gleiten, Uebergaenge, Masse), `pt_gleiten.py` (Gleiten je Bild),
`pt_vergleich.py` (Erwachsener/Platzhalter mit derselben Rechnung, Death/Dead/Eat je Bild), `pt_durch.py` + `pt_durch2.py`
(Bein-Durchdringung; Oberflaechen-Test und Strahl-Paritaet). Ergebnisse `pt_*.json` / `pt_*.log`.

| Regel | Grenze | gemessen (Endergebnis) | ok |
|---|---|---|---|
| Dreiecke | <= 20.000 | **19.418** (GLB-Indizes 58.254/3 und Importer 58.254/3) | ja |
| Netz / Material | 1 / 1 | 1 Mesh "NCBearCub", 1 Primitiv (mode 4), Knoten "NCBearCub"; **0 Material-, 0 Bild-, 0 Textur-Eintraege** wie Erwachsener und Platzhalter (Textur kommt aus der Rasse) | ja |
| Punkte / Indizes | < 65.536, u16 | 11.811 GLB-Punkte, Index-Typ 5123 (u16), JOINTS_0 u8, max Index 11.810 | ja |
| Knochen | 26, Namen wie Erwachsener | 26; Namen, Reihenfolge, Joint-Knoten, Eltern **identisch**; Knoten-Drehungen 0 Abweichungen; Knoten-Skalen wie Erwachsener | ja |
| Einfluesse | <= 4, Summe 1 | max 4; Summe GLB 0,99999996-1,00000004, Importer 0,9999999-1,0000002; 0 negativ; 0 NaN | ja |
| Clips | 15 Namen, Dauer, Abtastzeiten wie Erwachsener | 15 Namen in gleicher Reihenfolge; **alle 1.170 Zeit-Kanaele byte-gleich**; Dauern im Dump gleich (3,2/0,9/0,53333336/2,5666666/0,033333335/3,0/1,5/1,5/2,4/1,3/1,6/3,2/1,6/4,0/1,3); Bilder 97/28/17/78/2/91/46/46/73/40/49/97/49/121/40; Interpolation wie Erwachsener | ja |
| Skalier-Schluessel | 1,0 | **390/390 byte-gleich** mit dem Erwachsenen (Tail traegt dort wie beim Erwachsenen 1,000026) | ja |
| Lage-Schluessel | konstant ausser Pelvis/Translation_Data | Abweichung 0,0 in allen 15 Clips; Lagen = `skelett_rig.json` lage_E (z dort mit umgekehrtem Vorzeichen, Dump-Raum) | ja |
| Dreh-Kanaele | byte-gleich ausser D.5 / neue Clips | **242/390** byte-gleich; abweichend: Walk/Run/SitDown/Sit/StandUp je 23 (neu), Death/Dead Neck+Head je 12,75 Grad, Eat Neck+Head je 15,0, SwipeL/R je 6 Arm-Knochen <= 3,0, Maul 6 <= 2,94, Bite 6 <= 1,55, Slam 3 <= 0,67 -- deckt sich mit CLIPS.md T4 | ja (Eat s. M5) |
| Textur | 1024 x 1024 RGB 8 Bit, kein Alpha | IHDR 1024 x 1024, Bittiefe 8, Farbtyp 2, kein tRNS (nur IHDR/IDAT/IEND); = FORM-Abgabe `C_rig_basis.png`; UV-Menge = FORM-GLB (nicht gespiegelt) | ja |
| Namen | NCBearCub.glb / .png, model NCBearCub_Body, animationsMesh NCBearCub | Pfade `42/media/models_X/Skinned/NCBearCub.glb`, `42/media/textures/Body/NCBearCub.png`; Mesh-Name NCBearCub wie Platzhalter; passt zu `nc_bear_cub.txt` (mesh/meshFile `Skinned/NCBearCub.glb`) und `BanditsNPCBearDefs.lua` (bodyModel NCBearCub_Body, texture NCBearCub, animset buck) | ja |
| Massstab | 0,544 E/m wie Erwachsener, gebaut bei 1,0 | FORM-GLB (m) / End-GLB (E) = 0,544 exakt; Beinknochen 0,30107/0,33649/0,31611/0,32296 m = Erwachsener; Bip01-Hoehe 0,720 m = Erwachsener; Idle 0: Laenge 1,42 m, Ohren 1,24 m, Widerrist ~1,19 m (bei 0,35 ~42 cm) | ja |
| Dehnung p99,5 | <= 2,6 | ueber alle Dreieck-Bilder je Clip max **2,298** (Rear); schlimmstes Einzelbild 2,43 (Rear) | ja |
| Dehnung max | <= 4,0 | **3,503** (SwipeL, Bauch); Erwachsener mit derselben Rechnung 6,61 (Rear) | ja |
| Achsel/Brust | <= 3,5 | **3,233** (Rear, Achsel); sonst <= 3,05 | ja |
| Boden je Stuetzpfote | <= 1,5 cm (Ziel 1,0) | 14 Clips: **-0,50..+1,24 cm**, 0 Stuetzbilder > 1,5 (> 1,0: SwipeR 1x 1,03, Maul 1x 1,24). **Death: 22 Stuetzbilder > 1,5, bis 12,5 cm** (M1/M4). Dead: keine Stuetzpfote beim Erwachsenen | nein (Death) |
| ganzes Netz | >= -0,5 cm | min -0,50 (Krallen/Pfoten in Death, Dead, Swipe, Slam, Bite, Maul; Hub klemmt dort genau an der Grenze) | ja (Grenze) |
| Risse Hals/Achsel/Leiste | keine | **geschlossenes Netz**: 0 offene, 0 nicht-mannigfaltige Kanten, 0 entartete/doppelte Dreiecke, 0 gegen die Normalen gewendet (Erwachsener 3); 1.862 UV-Naht-Gruppen mit **identischen Gewichten** -> Spalt 0,0000 cm in allen 874 Bildern | ja |
| Harness | laedt | `OK ... Knochen 26 Clips [15]`; mein Dump ist **byte-gleich** mit `rig/clips/dump_final.txt` (MD5 7cdf1404) | ja |
| Tempo bei 0,35 | Walk 1,60 (>= 1,40) / Run 2,61 (>= 2,40) | aus den GLB-Schluesseln: Weg 0,901572 / 0,871111 E, linear (Abw. 3e-8), Richtung +z (vorwaerts) -> **1,603 / 2,613 Kacheln/s** (Platzhalter 0,523 / 2,465; Erwachsener 0,673 / 3,173). Formel Weg x 1,6 / Dauer: `Defaults.xml:3` MotionScale 1,6, `dec/AnimationPlayer.java:1235-1236`; Bild x 1,5 x Groesse `dec/IsoAnimal.java:2606` | ja |
| Gleiten (Stuetze) bei 0,35 | <= 1,5 cm | Stuetzbilder der Generator-Phase: Kontaktpunkte bewegen sich in der Welt **0,00-0,12 cm** je Bild (Walk und Run, alle 4 Pfoten) | ja |

## 2. Weitere Messungen (Auszug)
- **Uebergaenge:** Walk/Run erstes = letztes Bild (ohne Weg) 0,0; Sit erstes = letztes 0,0; SitDown Ende = Sit 0 = StandUp 0 exakt;
  Idle/Eat geschlossen. SitDown 0 / StandUp Ende gegen Idle 0: 0,1308 E -- exakt derselbe Wert wie beim Erwachsenen.
- **Eat:** tiefste Kopfhaut 42,3-57 cm (Erwachsener -0,04..16 cm). Neck/Head je 15,0 Grad in ALLEN 97 Bildern (gegenlaeufig).
- **Gangbild:** Walk hat in 3 von 28 Bildern keine Pfote am Boden (fliegender Trab, Junges bis 2,85 cm hoch = ~1 cm im Spiel);
  Run 4 von 17 (Galopp). Run-Stuetze sehr kurz: VR 1 Bild je Zyklus, VL/HR 2, HL 2-3 (Pfote "tippt").
- **Aufsetzen:** im letzten Schwungbild vor der Stuetze liegt die Pfote schon 0,1-1,0 cm ueber dem Boden und faehrt bis zum
  naechsten Bild noch 2-10 cm (bei 1,0; bei 0,35 ~1-3,5 cm) vorwaerts (VL 9,9 / HR 6,9 / VR 2,1 / Run VL 8,6). Das ist Restschwung
  beim Landen zwischen zwei Schluesseln, kein Gleiten in der Stuetze; Hinweis, kein Befund.
- **Bein-Durchdringung Walk/Run:** Strahl-Test 0 Punkte (der grobe Oberflaechen-Test `pt_durch.py` meldet dort 50-74 Punkte, ist aber
  nach dem Strahl-Test falsch-positiv; er gilt nur als Vorfilter). Linke/rechte Vorderpranke im Sitzen: 0 (beruehren sich nur).
- **Falten (s2 < 0,5):** Groessenordnung wie Erwachsener (z. B. Sit 70.067 gegen 56.322 Dreieck-Bilder, Rear 30.150 gegen 37.145);
  keine Grenze, nur Vergleich.
- **T6:** alle 191 Dateien aus `rig/clips/md5_nachher.txt` (NCBearTest, `_arbeit/baer_zaehmen/mod/`, Originalskripte, Eingaenge)
  jetzt noch byte-gleich (nachgezaehlt ~12:00).
- Translation_Data (0 Gewichte) hat eine andere inverse Bind-Matrix als beim Erwachsenen -- genau wie im gespielten Platzhalter;
  ohne Gewicht wirkungslos. Jaw hat 0 Gewichte (Maul bleibt zu); seine Drehschluessel in den 5 neuen Clips sind nicht die des
  Erwachsenen (RIG_PLAN 5.2) -- unsichtbar. Toe0-Lage 0,046 E (Erwachsener 0,129), 0 Gewichte.
- Vanilla `buck` ruft weitere Clips (IdleEating01, Sitting..., Alert...), die weder Erwachsener noch Junges haben -- unveraendert
  gegenueber dem gespielten Erwachsenen.

---------------------------------------------------------------------------------------------------------------------------

## 3. Befunde

### M1 (major) Death-Ende und Dead: das tote Junge steht auf einer Pfote statt zu liegen
- **Wo:** `DeerStag_Death` Bilder ~35-77, `DeerStag_Dead` (Pose der Leiche).
- **Beleg** (`pt_vergleich.log`, `pt_vergleich.json`, Haut je Knochengruppe, Bild Dead 0): tiefster Punkt je Teil -- L_Hand -0,5
  (105 Punkte < 3 cm), L_Foot 1,8, **Pelvis 17,7, R_Thigh 17,1, Spine 19,7, Spine1 21,1, R_UpperArm 21,0, Kopf 15,1**, R_Hand 13,1,
  R_Foot 13,2 cm. Nur 3 Nicht-Krallen-Punkte < 1 cm. Erwachsener: Rumpf 10,4, R_Hand 1,1; Platzhalter: Spine1 2,1, Pelvis 3,9,
  R_Foot 0,4. In Death 35-49 Rumpf 14,7-18,9 cm. Sichtbar in `rig/bilder/clips_r6.png` (Death 38 und Dead: Koerper in der Luft,
  Beine darunter). Bei 0,35 ~6 cm Luft unter der Leiche, bei 0,75 ~13 cm.
- **Regel:** RIG_PLAN 5.2/5.5 und SPEZ D.3 "aufliegende Haut 0,0..+1,2 cm, nie < -0,3" -- die Flanke liegt nie auf; die Krallen
  liegen bei -0,5.
- **Ursache (Messung):** schmale Spur (Q_V 0,55 / Q_H 0,64) mit den Drehungen des Erwachsenen: beim Kippen auf die rechte Seite
  rutschen die linken Beine unter den Koerper, der Hub haelt die tiefste Haut (die linke Pranke) bei 0 -> Rumpf haengt darueber.
- **Vorschlag:** D.5 fuer Death ab Aufprall und Dead erweitern (Entscheidung Lead): linkes Vorder- und Hinterbein im Liegen
  wegdrehen/strecken (UpperArm/Forearm/Thigh/Calf) bzw. zusaetzliches Rollen des Rumpfes, dann Hub, bis die rechte Flanke
  0..1,2 cm aufliegt; neu messen mit `pt_vergleich.py`. Danach Bild Death/Dead von 4 Seiten in Spielgroesse.

### M2 (major) Sitz-Trio: Unterschenkel stecken im Unterarm (harte Regel "0 Punkte")
- **Beleg** (`pt_durch2.py`, Strahl-Paritaet mit drei Strahlen quer zur Knochenachse, alle drei ungerade = innen; Tiefe = Abstand zur
  naechsten B-Haut): Sit Bild 0 und 60 -- HL in VL 9 Punkte bis 2,3 cm, VL in HL 6 bis 2,0, HR in VR 12 bis 1,9, **VR in HR 11 bis
  3,3 cm**, Hoehe 16-24 cm; in allen 31 gemessenen Sit-Bildern; SitDown 20 Bilder (ab ~29), StandUp 3-7 Bilder. **Erwachsener
  Sit/SitDown/StandUp: 0.** Bei 0,35 bis ~1,2 cm.
- **Regel:** SPEZ D.4 "Hart: 0 Punkte von Hinterfuss/Unterschenkel im Unterarm und umgekehrt", RIG_PLAN 6.3 C4. Der Baubericht nennt
  10-14 Punkte als "weiches Anliegen"; gemessen ist es eine Durchdringung bis 3,3 cm.
- **Vorschlag:** Hinterbein im Sitz etwas weiter nach aussen (`ferse_dy` / Hinterfuss-Mitten Richtung 0,76) oder Unterarme 1-2 Grad
  nach innen, bis der Strahl-Test 0 zeigt; sonst Kevin/Lead entscheiden lassen, ob Anliegen im Fell geduldet wird (im Ton von vorn
  vermutlich verdeckt -- ungeprueft).

### M3 (major, Risiko) Gangbild nur bei Groesse 0,35 ohne Gleiten -- NCBearTest zeigt das Junge bis 0,75
- **Beleg:** `NCBearTest/42/media/lua/shared/BanditsNPCBear.lua:103-105` (`growCurve` 0,35 -> 0,75 bei g 0,15; `cubMaxSize = 0.75`),
  `BanditsNPCBearStats.lua:222-227` (gezeigte Groesse = min(s, cubMaxSize)), `BanditsNPCBearDefs.lua:83-84` (minSize 0,35,
  **maxSize 1,35** -- nicht mehr 0,35/0,35 wie im Auftrag). Gleiten je Stuetzphase (`pt_mess.json` tempo_gleiten, Modell-cm):
  Walk 0,35: 0,0 | 0,5: 11-16 | 0,75: 20-28; Run 0,5: 6-10 | 0,75: 13-24. Im Spiel x Groesse: bei 0,75 ~15-21 cm je Schritt.
- **Physik:** Pfote in der Welt = 1,5 x Groesse x Modell, Wurzel = 1,6 x Weg (beides x Abspieltempo). Das Verhaeltnis ist
  Groesse/0,35 -- **ein Abspieltempo je Groesse (CLIPS.md 8.1.1) aendert daran nichts**, nur die Schrittfrequenz.
- **Vorschlag:** Kevin entscheiden lassen (Frage 1): a) Junges bis zum Modellwechsel bei 0,35 lassen, b) Gang-Clips je Groessenstufe
  (Weg proportional zur Groesse, Wahl per Animset-Variable -- Code-Lauf), c) `cubMaxSize` kleiner. Bis dahin: bei jeder gezeigten
  Groesse > 0,35 gleitet der Trab (immer noch weniger als der Platzhalter heute bei 0,35: 42-86 cm Modell).

### M4 (minor) Death im Kippen: Stuetzpfoten ueber 1,5 cm
- Bilder 23-29: VR/HR 1,55-2,39 cm, waehrend der Erwachsene auf ihnen steht (Netz sonst bei 0,0). Ab Bild 36 s. M1 (bis 12,5 cm).
  Meine Zaehlung (Stuetzbild = Erwachsenen-Pfote samt Krallen < 1,0 cm, wie `baer_junges/werkzeug/stuetz.py`): 44 > 1,0, 22 > 1,5,
  max 12,54 (VR) -- CLIPS.md nennt 39 / 17 / max 6,73 (andere Stuetzbild-Auswahl). Bei 0,35 im Kippen ~0,8 cm.

### M5 (minor) Eat erreicht den Boden nicht; Grenze unterschiedlich gelesen
- Tiefste Kopfhaut 42,3 cm (bei 0,35 ~15 cm). Neck -15 / Head +15 in allen Bildern: je Knochen <= 25,5 (RIG_PLAN 5.2 "bis delta+15")
  erfuellt, als Summe der Betraege 30 > 25,5 bzw. SPEZ D.5 "zusammen <= 15" nicht. Wirkt gegenlaeufig (Kopf vor die Brust).
- Gebraucht wird der Clip beim Fuettern aus der Hand (`BanditsNPCBearFeedAction.lua:58-60`, Figur in "AnimalLureLow") -- dort ist
  eine Schnauze ueber dem Boden evtl. sogar passender. Kevin (Frage 2).

### M6 (minor) Krallen/Pfoten genau an der Netz-Grenze
- Netz min -0,50 cm in Death, Dead, SwipeL/R, Slam, Bite, Maul (Hub-Klemme). Grenze ">= -0,5" gehalten; fuer aufliegende Haut im
  Liegen (Dead) gilt "nie < -0,3" -> 0,2 cm darunter (Krallen der linken Pranke). Bei 0,35 0,07 cm.

### M7 (minor) Baubericht CLIPS.md an drei Stellen ungenau
- 0/5/C1: "Death ... der Koerper liegt dabei auf" -- gemessen liegt nur die Pranke VL auf (M1).
- 2/C2: "Dead aufliegend +0,45" -- das sind 3 Hautpunkte der linken Pranke, nicht die Flanke (Rumpf 17,1 cm).
- 8.1.1: "Abhilfe waere ein Abspieltempo je Groesse" -- hilft physikalisch nicht (M3).
- Sonst stimmen alle nachgemessenen Zahlen mit CLIPS.md ueberein (Dreiecke, Punkte, Tempo, Dehnung je Clip auf 0,01, T4, Boden der
  14 anderen Clips, Uebergaenge, Sit-Boden 0,0-0,14).

---------------------------------------------------------------------------------------------------------------------------

## 4. Fragen fuer Kevin
1. **Wachsen gegen Gangbild (M3):** Das neue Junge geht nur bei Groesse 0,35 ohne zu rutschen. Mit dem Wachsen aus B1d (zeigt das
   Junge bis 0,75) rutschen die Pfoten mit jedem Wachstumsschritt mehr. Soll das Junge bis zum grossen Modell bei 0,35 bleiben, oder
   sollen wir Gang-Clips je Groessenstufe bauen?
2. **Fressen (M5):** Beim Fuettern senkt das Junge den Kopf, die Schnauze bleibt ~15 cm ueber dem Boden. Passt das zum Fuettern aus
   der Hand, oder soll es einen eigenen Fress-Clip mit Kopf am Boden bekommen?
3. **Gehen 1,60 Kacheln/s:** Ein gehender Spieler macht ~2,27. Das Junge faellt beim Gehen also weiter zurueck und muss zwischendurch
   rennen (2,61) -- nur viel seltener als heute. Reicht das, oder lieber der flinkere Trab (1,9, Plan-Variante)?

## 5. Dateien
| Datei | Inhalt |
|---|---|
| `rig/PRUEF_TECHNIK.md` | dieser Bericht |
| `rig/pruef_technik/dump_neu.txt`, `dump_erw.txt`, `dump_alt.txt` (+ `.pt.pkl`) | eigene Harness-Dumps (neu = byte-gleich `clips/dump_final.txt`; erw = MD5 2875ca08 wie FB-Referenz) |
| `rig/pruef_technik/pt_glb.py` / `pt_glb.json` | GLB-Pruefung gegen Erwachsenen/Platzhalter, PNG-Kopf |
| `rig/pruef_technik/pt_lib.py`, `pt_mess.py` / `pt_mess.json`, `pt_mess.log` | Boden, Netz, Dehnung je Region, Naehte, Topologie, Tempo, Gleiten 0,35/0,5/0,75, Uebergaenge, Masse |
| `rig/pruef_technik/pt_gleiten.py` | Gleiten je Bild (Diagnose Aufsetzen) |
| `rig/pruef_technik/pt_vergleich.py` / `.json` / `.log` | Erwachsener und Platzhalter mit derselben Rechnung; Death/Dead/Eat je Bild |
| `rig/pruef_technik/pt_durch.py`, `pt_durch2.py` (+ `.json`, `.log`) | Bein-Durchdringung (Vorfilter / Strahl-Paritaet) |
| `rig/pruef_technik/punkt_zu_gewichte.npy`, `dreieck_zu_regionen.npy` | Zuordnung Dump <-> `gewichte_end.npz` / `regionen_rig.npz` (Abstand <= 1,1e-7 m, alle 19.418 Dreiecke eindeutig) |

Befehle (Wiederholung): Harness wie RIG_PLAN 6.2 mit Ausgabe nach `rig/pruef_technik/dump_neu.txt`; dann in `rig/pruef_technik/`:
`python pt_glb.py pt_glb.json`, `python pt_mess.py pt_mess.json`, `python pt_vergleich.py`, `python pt_durch2.py`, `python pt_gleiten.py 0.35`.
