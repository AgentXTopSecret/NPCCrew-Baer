# RIG_PLAN -- Lauf baer-rig-junges: Generator-Junges C spielfertig (11.11.2026, Rolle PLAN)

**Nur Plan. Nichts am Modell gebaut, nichts gespielt.** Gelesen: SPEZ_JUNGES (B.5, D ganz), SPEZ/bau/fix_baby, GEGEN_OPTIK,
C_ERZEUGEN, C_FEIN, NACHBESSERUNG_OPTIK, forschung_b1b (Befund 0.3), 2c-Kette (`baer_kampf_2c.py` Gang/Weg, `baer_gewichte_2c.py`),
angefangene `baer_*_junges.py`, Harness `Dump.java`, Vanilla-Animset `buck`, Jar-Dekompilat (`_arbeit/baer_spiel/dec`).
Selbst gemessen (nur CPU, numpy, keine GPU): `rig/plan/mess/` -- `mess_gen.py`, `schnitte_gen.py` (exakte Schnittkurven),
`ton_raster.py` (Ton-Ansichten mit Massgitter, `ton_roh/*.png`, selbst angesehen), `tempo.py` (Tempo-Tabelle),
Ergebnis `gen_landmarken_foto.json`. Statisch geprueft, nicht gespielt.

Rahmen ueberall: **tier** = x vorn, y links, z oben, Boden z = 0, Meter bei Groesse 1,0 (Spiel skaliert auf 0,35); Modelleinheit
E = 0,544 je Meter. "roh" = Einheit von `C_schoen.glb` (L ~ 1); glTF -> tier: x = glTF z, y = glTF x, z = glTF y - 0,45998.

---------------------------------------------------------------------------------------------------------------------------

## 0. Kurz: Entscheidungen und Kernzahlen

| # | Entscheidung | Zahl |
|---|---|---|
| 1 | **Form bleibt die des Generators.** Zwei Formstufen: **F1** in der Foto-Pose mit der bewaehrten Kette (`nachbesserung/form2.py` + `textur2.py`, nur neue Parameter: Ohren, Sohlen, Stirn-Kratzer); **F2** Umstellen in die Ruhelage auf dem fertigen Spielnetz (nur Punkte verschieben, UV und Textur bleiben). | F1 ~4 min je Runde, F2 Sekunden |
| 2 | **Massstab** ueber Kevins Schulterhoehe 40 cm bei 0,35 | s = **1,31 m je roh** (0,7126 E je roh); Widerrist 0,875 roh = 1,146 m |
| 3 | **Skelett:** 26 Knochen, Namen/Eltern/Reihenfolge und **Ruhe-Drehungen byte-gleich mit dem Erwachsenen**; neu nur die Lagen (Lehre M6) | Beine 1,000 (vorn = hinten), Rumpf isotrop R (Fit, Start 0,82, erlaubt 0,78-0,90), Spur quer frei, Hals-/Kopflage frei, Fuss (Toe0) am Netz, Kiefer ohne Gewichte |
| 4 | **Gewichte:** Formel in Gelenk-Koordinaten + Raumglaettung + Optimierer gegen die Clips (Kopie `baer_gewichte_2c.py`); Kopf mit Ohren starr am Kopf, Pfoten starr | <= 4 Einfluesse, Summe 1 +-1e-4 |
| 5 | **Clips:** 10 byte-gleich mit Becken-Regel + Hub (Idle, Death, Dead, Rear, SwipeL/R, Slam, Bite, Maul, Eat); **neu aus dem Gang-Generator mit den Gelenken des Jungen:** Walk (Trab), Run (Galopp), SitDown/Sit/StandUp; Kopf-Abweichungen Eat/Death/Dead | 15 Namen, Dauern, Abtastzeiten byte-gleich |
| 6 | **Gehen schneller ohne Fussgleiten:** Walk = **Trab, 3 Zyklen in 0,9 s**, S 0,64 m / duty 0,38 | **1,60 Kacheln/s** (Weg 0,9019 E), heute 0,52 |
| 7 | **Rennen entsprechend:** Run = **Galopp, 2 Zyklen in 0,5333 s**, S 0,61 m / duty 0,25 | **2,61 Kacheln/s** (Weg 0,8711 E), heute 2,47 (gleitet) |
| 8 | **Export:** Puffer-Tausch im Gerippe des gespielten `NCBear.glb` (08ec7806) wie `baer_export_junges.py`; Pruefung mit Dump.java | Ziel `rig/out/42/media/...` |

Grund fuer 6 (Kern): Bei Groesse 0,35 ist das Junge in Spielmetern so klein, dass ein **Schritt** hoechstens ~0,9 Kacheln/s
schafft (Froude-Zahl 0,5 bei Hueftehoehe 0,24 m); 1,6-2,3 Kacheln/s laeuft ein Tier dieser Groesse im **Trab** (Froude 1,6). Der
Erwachsenen-Walk gibt ohne Gleiten nur 0,24 Kacheln/s her (SPEZ D.6), mit 3 Zyklen 0,71 -- das reicht nicht. Abschnitt 5.3.

---------------------------------------------------------------------------------------------------------------------------

## 1. Messung des Generator-Jungen (Foto-Pose; `rig/plan/mess/gen_landmarken_foto.json`)

`C_schoen.glb` (04:24): 11.931 GLB-Punkte (9.837 verschweisst), 19.670 Dreiecke, 1 Netz/1 Material/1 UV, UV-Belegung 60,6 %
(`mess/uv_belegung.png`), Textur 1024 RGB.

| Mass | roh | Meter bei 1,0 (s 1,31) | bei 0,35 | SPEZ_JUNGES zum Vergleich |
|---|---|---|---|---|
| Widerrist H (Ruecken ueber der Vorderbein-Achse, x 0,12) | 0,875 | 1,146 | 40,1 cm | 1,143 |
| Kruppe (x -0,20) / Senke (x -0,075) | 0,829 / 0,810 | 1,086 / 1,061 | | 1,143 / 1,150 (kein Buckel) |
| Ohren oben | 0,969 | 1,269 | 44,4 cm | 1,03 m Kopf mit Ohren |
| Bauch tiefster Punkt (x -0,1) | 0,31 | 0,406 | | 0,400 |
| Brust zwischen den Vorderbeinen / Bug (x 0,10 / 0,20) | 0,35 / 0,42 | 0,46 / 0,55 | | 0,425 / 0,52 |
| Rumpfende (Stummel) x / Brust vorn (z 0,45) x | -0,523 / 0,301 | -0,685 / 0,394 | | -0,74 / 0,40 |
| Laenge L Nase -> Heck, Kopf gerade (Schaetzung) | ~1,06 | ~1,39 | ~48,6 cm | 1,85 (64,8 cm) |
| L / H | 1,21 | | | 1,62 |
| Rumpfbreite (Halbbreite) | 0,21-0,24 | 0,28-0,31 | | 0,32 |
| Spur halb vorn / hinten (Mitte Bein) | 0,095 / 0,1125 | 0,124 / 0,147 | | 0,196 / 0,210 |
| kleinster Abstand der Beine | 0,025 | 0,033 | | |
| Pfote vorn Laenge x Breite / hinten | 0,152x0,120 / 0,185x0,119 | 0,20x0,157 / 0,242x0,156 | | Pranke 0,228 breit / Hinterfuss 0,29 lang |
| Augenabstand / Ohren y / Ohren hinter den Augen | 0,104 / +-0,087 / 0,12-0,13 | 0,136 / +-0,114 / 0,16 | | |

**Pose (Foto):** Kopf um **45,3 Grad nach links** gegiert (Augenmitte -> Schnauze), Augenachse 3,1 Grad gerollt, Augen-Nase-Linie
-41,2 Grad (Kopf leicht gesenkt, wie im Foto). **Mittelebene y = -0,050 roh** (Stummel -0,052, Ruecken-Grat -0,03..-0,075, Mitte
der Vorderbeine -0,055). **Rumpf in C-Bogen:** Rumpfmitte hinten y -0,03, Mitte -0,08, vorn -0,07 (~5 cm roh, ~7 Grad); Hinterbeine
um ~3,7 cm nach links versetzt (HL +0,15, HR -0,075 von der Mittelebene). **Vorderbeine:** VR senkrecht bei x 0,16; VL schraeg (Pfote
x 0,106, Oberkante x 0,0: Schritt-Pose, Schulterblatt zurueck). **Hinterbeine:** Unterschenkel fast senkrecht bei x -0,24..-0,25.
Ohren (Ton-Bilder `ton_roh/seite_l.png`, `seite_r.png`, `hinten.png`): zwei Knubbel auf schmalem Ansatz ("Pilz", GEGEN_OPTIK C-01).

**Was das heisst:** Das Generator-Junge ist **kompakter** als SPEZ_JUNGES (L/H 1,2 statt 1,62), der Kopf ist **kleiner und sitzt
hoch und nah auf den Schultern** (Hals kurz, Kopf hochgetragen wie im Foto), die Beine stehen **enger** (+-0,12-0,15 m statt
+-0,20), die Hinterpfoten sind kuerzer (0,24 m statt 0,29). Rumpfhoehe, Bauch, Breite und Beinlaenge passen zu SPEZ B.5.
Die Standhaltung im Spiel kommt aus Idle01 (Drehungen des Erwachsenen), nicht aus der Foto-Pose.

---------------------------------------------------------------------------------------------------------------------------

## 2. FORM (Rolle FORM; Ordner `rig/form/`, Skript `baer/spiel/baer_form_rig.py`)

### 2.0 Eingang (zuerst kopieren, nur Kopien lesen; MD5 in `rig/form/eingang/md5.txt`)
`aus/C_schoen.glb`, `aus/C_schoen_textur.png`, `aus/C_schoen_messung.json`, `nachbesserung/C_form_v17.json`,
`nachbesserung/C_tex_final.json`, `nachbesserung/E_form_v9.json` (nur Vorlage Sohlen), `nachbesserung/form/C_v17/form_info.json`.
`form2.py`/`textur2.py` werden **aufgerufen, nie geaendert**; braucht eine Stufe eine neue Option: Kopie nach
`rig/form/werkzeug/form2_rig.py` bzw. `textur2_rig.py`. Alle Parameter-`aus`/`renderordner` zeigen nach `rig/form/f1/`.

### 2.1 F1 -- Fotopose, bewaehrte Kette (Parameter `rig/form/C_form_rig.json`, `rig/form/C_tex_rig.json`)
Warum in der Fotopose: textur2 backt aus dem Rohmodell in der Fotopose und eicht die Farbe in der Fotoansicht; nur hier lassen sich
die Ohren 1:1 neben das Foto legen (Ansicht az 43 / el 8 nach GEGEN_OPTIK 2).
1. **Ohren (C-01, C-08)** -- Ausgang `C_form_v17.json "ohren"` (r_breit 0,05, r_hoch 0,047, dicke 0,034, k 0,014, kipp_grad 30,
   heraus 0,006). Ziel: von ALLEN Seiten runde, dicke Baerenohren **ohne Hals**:
   - Basis breiter: Vereinigung weicher (k 0,014 -> 0,03-0,04) und/oder ein flacher Sockel-Ellipsoid unter dem Ohr, Ohr tiefer
     setzen (heraus 0,006 -> 0 bis -0,01). Pruefmass: im Ton von 90/135/180/225/270 Grad ist das Ohrprofil an der Basis >= 85 %
     der groessten Ohrbreite, keine Taille > 0,5 cm roh.
   - Etwas groesser wie im Foto: +12..+18 % (r_breit ~0,058, r_hoch ~0,055, dicke >= 0,04); im Foto ist die Ohrbreite ~0,32 der
     Kopfbreite -- neben dem Foto in az 43 / el 8 pruefen.
   - Neigung nach hinten 30 -> 15-20 Grad, damit sie bei geradem Kopf von vorn ueber den Kopfumriss ragen.
   - Textur: Muschel dunkel, Saum fransig hell, keine strahligen "Holzmaserung"-Striche innen (ohr_fell_staerke runter), Rueckseite
     mit Fell und nicht heller als die Stirn.
2. **Stirn-Kratzer (C-02 Rest):** heller Strich auf der Stirn am rechten Ohr: mit einer Fuell-Kugel (wie `heck_fuellen`) aus dem
   Umring fuellen und mit gerichteten Fellstrichen belegen.
3. **Sohlenkanten rund (C-04, C-05 Rest):** die E-06-Werte aus `E_form_v9.json "pfoten"` uebernehmen (sohle_breite 0,88, sohle_h 0,03,
   k_bein 0,02, boden_k 0,012, `glaetten_je_bein` Knoechel/Sohle). Pruefmass: von der Seite (el -10) keine Platte, Unterkante
   rund (Radius >= 1,2 cm roh); von unten-vorn keine "Kamm"-Krallenreihe (Krallenstriche kuerzer).
4. **Laufen:** `form2.py` (CPU ~50 s) und `textur2.py` mit `sh werkzeug/gpu_lauf.sh <log> <blender ...>` (GPU-Sperre, ~2-2,5 min).
   Dreiecks-Ziel <= 19.900 (Importer zaehlt; Grenze 20.000). Ergebnis `rig/form/f1/C_f1.glb` + `C_f1_textur.png` + Messung.
   Mehrere Runden erlaubt (F1 -> F2 -> Vorschau -> F1), weil die 0-Grad-Ohrenprobe erst mit geradem Kopf geht.

### 2.2 F2 -- Umstellen in die Ruhelage (`baer_form_rig.py`, numpy; auf `C_f1.glb`, UV und Textur bleiben)
Ausgang: tier-Meter (Massstab s 1,31, Mittelebene y -0,050 roh -> y 0, Boden 0, x-Ursprung vorlaeufig Mitte zwischen Vorder- und
Hinterpfoten; SKELETT verschiebt x und darf s um <= +-3 % aendern). Verfahren: ein **Hilfs-Gerippe der Foto-Pose** (Punkte
aus Schnittkurven wie `mess/schnitte_gen.py`, Landmarken wie `mess/mess_gen.py`) und eine **Ziel-Ruhe**; jede Region bekommt eine
starre Bewegung, Uebergaenge mit glatten Gewichten (smoothstep entlang der Achse), Drehungen werden ueber den Winkel gemischt (kein
lineares Matrizen-Mischen = keine Schrumpfung), danach Laplace-Entspannen nur in den Uebergangsbaendern bei festem Rand.
Keine Topologie-Aenderung, kein neues UV.
1. **Kopf gerade (C-06):** zwei Drehpunkte auf der Hals-Mittellinie: Halsbasis C7 (Schaetzung roh (0,16 / -0,05 / 0,69)) und Atlas
   (Kopfrahmen x_k -0,17, z_k -0,03; Kopfrahmen = Augenmitte, x_k Blick waagerecht). Hals-Abschnitt um den Biegewinkel der
   Hals-Mittellinie (~-19 Grad) um C7, Rest der Gier (~-26 Grad) um den Atlas; Kopf vor der Atlas-Ebene -0,03 starr, Rumpf hinter C7
   +0,03 starr, dazwischen glatt. **Rollen 3,1 Grad zurueck, Nicken bleibt** (Augen-Nase-Linie -41 +-3 Grad, so steht er im Foto).
   Ergebnis: Blick entlang +x, Kopf-Mittelebene = y 0 (+-0,5 cm), Augen gleich hoch (+-0,3 cm).
   **Naht unsichtbar:** im Ton von 8 Seiten und nah keine Stufe/Falte am Hals (Umriss-Stufe <= 0,5 cm wie SPEZ C.4), Textur ohne
   verzerrte Fellstriche: Verzerrung je Dreieck (sigma1/sigma2 der Umstell-Abbildung) p99 <= 1,35 im Halsband; sonst dort mit
   gerichteten Fellstrichen nachfuellen (Fuell-Logik wie `textur2.py`).
2. **Rumpf gerade:** seitliche Scherung dy(x) so, dass die Rumpfmitte (z 0,45-0,75 roh) fuer jedes x auf y 0 liegt (C-Bogen weg).
3. **Beine in die Ruhe des Skeletts:** Richtungen = Erwachsener in Ruhe (aus `_arbeit/baer_junges/koerper/skelett.json`
   `ruhe_m_erw`): Oberarm 11,0 Grad nach hinten, **Unterarm 16,2 Grad nach vorn**, Oberschenkel 21,4 Grad nach vorn,
   **Unterschenkel 22,8 Grad nach hinten**, Fuss 13,4 Grad unter der Waagerechten; Sohlen flach auf z 0. Sichtbar sind nur
   Unterarm und Unterschenkel: um Ellbogen bzw. Knie drehen (Ellbogen ~z 0,40 m, Knie ~z 0,41 m auf der Beinachse), VL zusaetzlich
   mit dem Schulterblatt nach vorn zu VR. Spur symmetrisch: +-b_V, +-b_H aus dem Mittel links/rechts, **Luecke zwischen linkem und
   rechtem Bein >= 4 cm bei 1,0** in jeder Hoehe (heute 3,3 cm vorn: Vorderbeine je ~0,5 cm nach aussen).
4. **Symmetrie-Probe** nach 1-3: Halbbreiten links/rechts je Schnitt (x alle 5 cm, z 0,3-0,8 m) und Beinprofile; wo |Unterschied| >
   1,5 cm: dort Form zur Mitte aus Punkt und gespiegeltem Gegenpunkt mischen (nur Form, Fotoseite links ist Vorbild; Kopf nicht
   anfassen, der ist seit C_FEIN gespiegelt).
5. **Ohren-Probe bei geradem Kopf** (C-01 Rest 1): von vorn (az 0, el 0 und el 30) ragen **beide** Ohren ueber den Kopfumriss
   (>= 0,10 Kopfbreite), kein dunkler Ohrfleck ganz innerhalb des Kopfumrisses; in Spielgroesse (577 px/E bei 0,35) Ohr je >= 15 px
   breit und >= 4 px ueber dem Umriss. Sonst zurueck nach F1.

### 2.3 Abgabe FORM (alles `rig/form/`)
| Datei | Inhalt |
|---|---|
| `C_rig_basis.npz` (**massgeblich**) | `V` verschweisste Punkte tier-Meter, `T` Dreiecke, `glb_punkt` (GLB-Punkt -> verschweisster Punkt), `UV` je GLB-Punkt (glTF-Konvention, v von oben), `V_foto` (Lage in der Foto-Pose), Masken je Punkt: `kopf`, `ohr_l`, `ohr_r`, `hals`, `pfote_VL/VR/HL/HR`, `kralle`, `sohle`, `stummel`, `skala_m_je_roh`, `y_mitte_roh` |
| `C_rig_basis.glb` + `C_rig_basis.png` | nur zum Ansehen (glTF: +z vorn, +y oben, Meter), Textur 1024 RGB |
| `landmarken_rig.json` | Ruhe, tier-Meter: Augen, Nasenspitze, Ohrspitzen/-basen, Krone, Hinterkopf, Atlas- und C7-Schaetzung, Kopfbreite W, Widerrist, Kruppe, Bauch, Bug, Rumpfende, Stummel; je Bein Achsenpunkte (Schnitt-Mitten z 0,05-0,35 m), Ellbogen/Knie wie gedreht, Pfoten-Mitte, Ferse, Ballen, Zehenspitze, Sohlenrand |
| `FORM.md`, `rig/bilder/form.png` | Bericht (Zahlen je Punkt 2.1/2.2, Messungen, Urteil) und Blatt: Foto + az 43/8 vorher/nachher, 8 Seiten gross (Textur, Ton), 8 Seiten Spielgroesse, Kopf nah 0/45/90/180/270, Ohren nah, Pfoten von der Seite el -10 |

---------------------------------------------------------------------------------------------------------------------------

## 3. SKELETT (Rolle SKELETT+GEWICHTE; Ordner `rig/skelett/`, Skript `baer/spiel/baer_skelett_rig.py`)

### 3.1 Regeln (Lehre M6 / FB 4.4 und was sich aendert)
- Knochen-Liste, Eltern, Reihenfolge, Knoten-`rotation` aller 26 Knochen = `NCBear.glb` 08ec7806, **byte-gleich**. Die Clips
  liefern absolute lokale Drehungen; nur so ergeben die Erwachsenen-Drehungen dieselbe Haltung. Neu sind nur Lagen (`translation`).
- **Beine exakt 1,000:** Calf-Lage (Oberschenkel 0,16378 E), Foot-Lage (Unterschenkel 0,18305 E), Forearm-Lage (Oberarm 0,1720 E),
  Hand-Lage (Unterarm 0,1757 E) = Erwachsener, Richtung und Laenge. Vorn = hinten (sonst Bodenfehler in jedem Clip).
- **Rumpf isotrop R:** Spine, Spine1-Lage, Thigh (x/z-Anteile), Clavicle, UpperArm (x/z-Anteile), Tail-Grundlage = Erwachsener x R.
  R wird gefittet: Hueftgelenk und Schultergelenk aus den Beinachsen des geraden Netzes (Knie + Oberschenkel-Vektor, Ellbogen +
  Oberarm-Vektor), R = Abstand Huefte-Schulter / 0,750. Start 0,82; erlaubt 0,78-0,90; ausserhalb 0,80-0,88 begruenden und
  `_arbeit/baer_junges/werkzeug/sp_skelett.py` (Kopie) mit dem R neu rechnen und den Rest-Bodenfehler melden.
- **Spur quer frei:** die y-Anteile von Thigh und Clavicle/UpperArm so, dass Huefte und Schulter ueber der (symmetrischen) Beinmitte
  von FORM liegen (erwartet +-0,147 / +-0,124 m statt +-0,2125 / +-0,191; Faktor Q_H ~0,69, Q_V ~0,65). Wirkt in den byte-gleichen
  Clips nur als feste Querverschiebung der Pfoten (gemessen nachweisen, D.3).
- **Fuss (Toe0-Lage) am Netz:** Sprunggelenk -> Ballen des kuerzeren Generator-Fusses (~0,18 m statt 0,237; Faktor ~0,78). Die neuen
  Gang-/Sitzclips rechnen mit diesem Ballen; in den byte-gleichen Clips stehen die Fuesse flach (Ballen-Abweichung je Grad Fuss-Nicken
  ~0,1 cm) -- gemessen in C1 (Abschnitt 6.3), sonst Fuss-Korrektur <= 5 Grad (D.5-Zeile, melden).
- **Hals und Kopf frei am Netz:** Neck-Lage (Spine1-Gelenk -> C7) und Head-Lage (C7 -> Atlas) als freie Vektoren. Atlas: im Kopf
  0,14 W vor dem Hinterkopf-Fell, auf Augenhoehe -0..-0,05 W (W = Kopfbreite); C7 in der Mittelebene am Uebergang Widerrist/Hals,
  30-45 % der Halstiefe unter der Oberlinie. Unter diesen Bedingungen den Winkel delta zwischen C7->Atlas und der Erwachsenen-
  Richtung Neck->Head (22 Grad unter der Waagerechten) **klein halten** (Ziel <= 15 Grad, Kopf hoch getragen wie im Foto). delta
  bestimmt die Kopf-Abweichung, die Eat/Death/Dead brauchen (5.2).
- **Kiefer:** das Generator-Netz hat kein Maul (Mundlinie nur gemalt). `Bip01_Jaw` liegt am Kiefergelenk (unter/hinter dem Auge),
  **0 Gewichte** -- das Maul bleibt in allen Clips zu, nichts reisst. (Ein Maul ware eine eigene Formstufe, Frage an Kevin.)
- **Schwanz:** Tail-Gelenk an der Stummelwurzel (Stummel bei roh (-0,523 / -0,052 / 0,487)); nur der Stummel haengt daran.
- Wurzel: Bip01 (0 / 0 / 0,39168 E), Dummy01, Translation_Data in Ruhe = Erwachsener. Becken-Ruhe nach der Becken-Regel
  (SPEZ D.2): Hueftmitte = Hueftmitte Erwachsener + (DX, 0, 0), **DX = 0,375 x (1 - R)** m (R 0,85 -> 0,05625 wie SPEZ). Netz in x
  so verschieben, dass seine Hueften auf den Hueften des Skeletts liegen.
- Gelenke muessen im Netz liegen: jedes Gelenk >= 2 cm unter der Haut (Ellbogen, Knie, Hand-/Sprunggelenk >= 1,5 cm). Weicht eine
  Beinachse des Netzes > 4 Grad von der Knochenrichtung ab, die Funktion aus `baer_form_rig.py` (F2.3) nachdrehen und melden.

### 3.2 Abgabe SKELETT (zusaetzlich zu den Gewichten, 4.4)
- `skelett_rig.json` im **Format von** `_arbeit/baer_junges/koerper/skelett.json` (`faktoren`, `namen`, `eltern`, `lage_E`,
  `lage_E_erw`, `ruhe_m`, `ruhe_m_erw`) plus `skala_m_je_roh`, `R`, `Q_H`, `Q_V`, `dx_m`, `delta_hals_grad`, `fuss_faktor`,
  `netz_versatz_x_m`. Damit lesen `baer_kampf_junges.py`-Kopien (`NCB_JUNGES_SKELETT`) und der Export dieselben Zahlen.
- `sp_rig.txt`: Kopie von `sp_skelett.py` mit Lage-Vektoren statt Faktoren, Becken-Regel ueber alle 15 Clips des Erwachsenen:
  Bodenfehler der Vorder-/Hinterpfoten je Stuetzbild vor dem Hub, Abstand Hinterfuss <-> Unterarm, Abstand linkes <-> rechtes Bein.

---------------------------------------------------------------------------------------------------------------------------

## 4. GEWICHTE (Rolle SKELETT+GEWICHTE; Skript `baer/spiel/baer_gewichte_rig.py`)

### 4.1 Verfahren
1. **Formel** (wie `gewichte_eigen` in `baer_kampf_2c.py`, aber in Gelenk-Koordinaten statt fester Hoehen): je Bein Lauf-Parameter
   entlang Hueft->Knie->Sprung->Ballen bzw. Schulter->Ellbogen->Hand, smoothstep ueber die Gelenke (Breite: Huefte/Schulter 0,10 m,
   Knie/Ellbogen 0,07, Sprung/Hand 0,05); Rumpf Pelvis/Spine/Spine1 entlang der Wirbelsaeule (Breite 0,12); Tail nur Stummel;
   **Kopf mit Ohren starr = Head 1,0** vor der Ebene Atlas - 0,03 m; Hals Spine1 -> Neck -> Head entlang C7->Atlas ueber >= 8 cm;
   **Pfoten starr** (Formel-Anteil Hand bzw. Foot/Toe0 >= 0,95 unter der Sprung-/Handgelenkhoehe, Krallen 1,0).
   Seitenregel: linke Beinknochen nie rechts der Mitte und umgekehrt; Vorderbeinknochen nie am Hinterbein, nie hinter x 0 (und
   umgekehrt); Hals/Kopf nie am Bein (wie `fremd` in `baer_gewichte_2c.py`).
2. **Raumglaettung** (`raum_glatt`, sigma 0,03 m; aus `baer_form_junges.py`) ausser starre Zonen; <= 4 groesste, Summe 1.
3. **Optimierer:** Kopie von `baer_gewichte_2c.py` (projizierter Gradientenabstieg gegen sigma1, Stauchung, Falten, Glaette,
   Naehe zur Formel); entfernen: Kopf-/Krallen-Uebernahme aus alten Netzen (`KOPF_ALT`, `alt_von`, `k1_dy`, `k2c_dx`); frei sind
   nur Rumpf, Hals, Achsel, Leiste und Bein-Uebergaenge. Clips: zuerst der **Vorab-Dump** (4.3), endgueltig der Dump der fertigen
   15 Clips (Rolle CLIPS ruft dasselbe Skript noch einmal, 5.6). ~20 min CPU -> im Hintergrund starten.
- **Blender-Automatik (Knochen-Waerme) nicht als Hauptweg:** bei 3-4 cm Luecke zwischen den Beinen blutet sie in das Nachbarbein und
  in den Bauch; hoechstens als Vergleich.

### 4.2 Heikle Zonen (je Zone eine Probe-Pose, 4.3)
| Zone | Gefahr | Regel |
|---|---|---|
| Hals | kurzer, dicker Hals, Kopf hoch: Kopf nicken/gieren (Sit-Umschauen 13 -> 27,5 Grad) knittert Kehle/Nacken | Uebergang ueber die ganze Halslaenge, Spine1 nie im Kopf; Naht aus F2 nicht verschaerfen |
| Achsel/Brust | dicker Rumpf liegt um den Oberarm; Trab/Galopp schwingen +-0,3 m | Oberarm-Anteil an der Brustwand nur oberhalb des Ellbogens; Grenze Dehnung <= 3,5 |
| Leiste | Oberschenkel steckt im Bauch | Bauchmitte (|y| < 0,08) nur Rumpf; Leistenfalte weich |
| Bauch tief (0,41 m) | Ellbogen/Knie stossen in den Bauch | Bauch nie an Unterarm/Unterschenkel |
| Schwanz | Stummel klein | nur Tail, Ring 2 cm Mischung mit Pelvis |
| Ohren | duerfen nicht schwabbeln | Head 1,0, kein Neck |
| Pfoten | Generator-Pfoten sind Ellipsoid-Koerper | starr; Sohle bleibt eben |

### 4.3 Probe und Vorab-GLB
- **Vorab-GLB** `rig/skelett/vorab/NCBearCub_vorab.glb` mit `baer_export_rig.py`-Vorstufe (Kopie `baer_export_junges.py`, 6.1):
  12 byte-gleiche Clips mit Becken-Regel (ohne Hub) + die 3 Sitz-Clips des Erwachsenen umgerechnet (nur Vorab) -> Dump.java ->
  `dump_vorab.txt(.pkl)`. Daran optimieren und messen.
- **Probe-Posen** rendern (Ton + Textur, az 45 el 30 und Seite): Kopf -30/+30 Grad nicken, +-35 gieren; Vorderbein +-35 vor/zurueck,
  Hinterbein +-35; Rear hoechstes Bild; Run Bild 4/13 (Erwachsener, Vorab); Sit Bild 0 (Vorab). Keine Risse, keine Beulen, Ohren
  und Stummel folgen starr.
- `C_rig.blend` (Armatur + Netz + Gewichte zum Ansehen), Blender nur ueber `gpu_lauf.sh`, wenn gerendert wird.

### 4.4 Abgabe GEWICHTE
`rig/skelett/gewichte_rig.npz` (`W` verschweisste Punkte x 26, `namen`; `formel_W`; Masken), `regionen_rig.npz` (achsel, brust,
leiste, hals, kopf, ohr, pfote, kralle, stummel je Dreieck -- fuer die Dehnungs-Tabelle), `vorab/`, Probe-Blatt
`rig/bilder/skelett_proben.png`, Bericht `rig/SKELETT.md` (Gelenk-Tabelle Generator gegen SPEZ, R/Q/delta, Dehnung je Vorab-Clip).

---------------------------------------------------------------------------------------------------------------------------

## 5. CLIPS (Rolle CLIPS+EXPORT; Ordner `rig/clips/`, Skripte `baer/spiel/baer_clips_rig.py`, `baer_export_rig.py`)

### 5.1 Grundsatz (SPEZ D.1 unveraendert)
15 Clips, Namen, Dauern, Abtastzeiten (Zeit-Accessoren) **byte-gleich** mit `NCBear.glb` 08ec7806: Idle01 3,2 s/97, Walk 0,9/28,
Run 0,5333/17, Death 2,5667/78, Dead 0,0333/2, Rear 3,0/91, SwipeL/R 1,5/46, Slam 2,4/73, Bite 1,3/40, Maul 1,6/49, Eat 3,2/97,
SitDown 1,6/49, Sit 4,0/121, StandUp 1,3/40. Jeder Knochen hat in jedem Bild Lage, Drehung, Skalierung (1,0). Lagen konstant =
`lage_E` des Jungen ausser Bip01_Pelvis (je Bild) und Translation_Data (Weg).

### 5.2 Herkunft je Clip
| Clip | Drehungen | Becken | Weg | Abweichung (D.5, je Knochen/Bild mit Messwert in CLIPS.md) |
|---|---|---|---|---|
| Idle01, Rear, SwipeL, SwipeR, Slam, Bite, Maul | Erwachsener byte-gleich | Becken-Regel D.2 (DX = 0,375(1-R)) + Hub dz(Bild) an der Haut | 0 | Neck/Head <= 10 Grad nur bei Durchdringung; UpperArm/Forearm/Hand <= 3 Grad nur bei Stuetzpfote > 1,0 cm nach Hub |
| Eat | byte-gleich ausser Neck/Head | wie oben | 0 | **Neck+Head nicken bis delta + 15 Grad (hoechstens 35)**, falls die Schnauze sonst den Boden nicht erreicht zusaetzlich Vorderbeine (Ellbogen beugen) <= 10 Grad; Ziel tiefste Kopfhaut 0..+1,5 cm in den Bildern, in denen der Erwachsene < 1 cm hat. Reicht es nicht: Kopf so tief wie moeglich, melden (Frage Kevin) |
| Death, Dead | byte-gleich ausser Neck/Head ab Aufprall | Regel + Hub (liegt auf der eigenen, dickeren Flanke) | 0 | Kopf seitlich/nicken <= delta + 15 Grad; aufliegende Haut 0,0..+1,2 cm, nie < -0,3 |
| **Walk** | **neu: Trab** aus dem Gang-Generator, Gelenke des Jungen | aus dem Generator | 0,9019 E | ganzer Clip neu (Kevins Freigabe "Gehen schneller", 5.3) |
| **Run** | **neu: Galopp** aus dem Gang-Generator | aus dem Generator | 0,8711 E | ganzer Clip neu (5.3) |
| SitDown, Sit, StandUp | neu, S_J (D.4) mit den Gelenken des Jungen | aus dem Generator, z am Netz geloest | 0 | ganzer Clip neu (D.4) |

Kiefer: Drehungen wie der Erwachsene (ohne Gewichte unsichtbar).

### 5.3 Gehen schneller: wie das Spiel das Tempo nimmt und was ohne Gleiten geht
**Beleg (Vanilla/Jar, statisch gelesen):** Die Pfad-Bewegung ist die Laenge der Clip-Bewegung je Bild
(`_arbeit/baer_spiel/dec/PathFindBehavior2.java:938-943`, `moveToPoint :1029-1052`); die Bewegung ist `Translation_Data` x
`AdvancedAnimator.motionScale` (`AnimationPlayer.java:1235-1236`), MotionScale 1,6 (`media/AnimSets/Defaults.xml:3`); die
Tiergroesse kommt dort nicht vor, sie skaliert nur das Bild (1,5 x Groesse, `IsoAnimal.java:2606`). Die Buck-Knoten haben kein
`m_SpeedScale` (`AnimSets/buck/walk/defaultWalk.xml`, `run.xml`, `pathfind/defaultPathfind.xml`, `runPathfind.xml`) -> Abspieltempo
1,0, Dauer fest. Also: **Kacheln/s = Weg(E) x 1,6 / Dauer**, und ohne Gleiten muss gelten
**Weg je Zyklus = S/duty x 0,544 / (1,6/1,5) x 0,35** (S = Stuetzweg der Pfote in m bei 1,0, `weg_gang` `baer_kampf_2c.py:2500-2502`).
Gegenprobe: Platzhalter Walk 0,294 E -> 0,52, Run 0,822 -> 2,47 Kacheln/s (= forschung_b1b Befund 0.3).

**Hebel bei fester Dauer:** mehr Zyklen je Clip (N) und laengerer Stuetzweg. Tabelle `rig/plan/mess/tempo.py`:
| Variante | Kacheln/s | Urteil |
|---|---|---|
| Erwachsenen-Walk x 0,35, 1 Zyklus (SPEZ D.6) | 0,24 | zu langsam |
| C: Erwachsenen-Walk, 3 Zyklen (Bild 3i mod 27, byte-gleiche Schluessel) | 0,71 | Trippeln, reicht nicht |
| B: Erwachsenen-Run als Huepfgalopp, 2 Zyklen in 0,9 s | 1,32 | Galopp in Zeitlupe (2,2 Hz), Rueckfall |
| **A: Trab neu, 3 Zyklen (3,33 Hz), S 0,64 / duty 0,38** | **1,60** | **Ziel** |
| A schnell: Trab, 4 Zyklen (4,44 Hz), S 0,60 / duty 0,40 | 1,90 | Variante fuer Kevin (sehr flinke Schritte) |
| Run B: Erwachsenen-Run, 2 Zyklen (Bild 2i mod 16) | 2,22 | Rueckfall Run; langsamer als ein gehender Spieler (2,27) |
| **Run A: Galopp neu, 2 Zyklen (3,75 Hz), S 0,61 / duty 0,25** | **2,61** | **Ziel**: schneller als ein gehender Spieler |

Natuerlichkeit (Alexander: Schrittlaenge = 2,3 Fr^0,3 Hueftehoehen): bei 1,6 Kacheln/s trabt ein Tier mit 0,24 m Hueftehoehe mit
~3,0 Hz -- 3 Zyklen in 0,9 s (3,33 Hz) passen; Galopp bei 2,6 Kacheln/s ~3,8 Hz -- 2 Zyklen in 0,5333 s (3,75 Hz) passen.

**Festgelegt:**
- **Walk (Trab):** Kopie von `pose_walk` als `pose_trab` mit `TRAB = dict(T=9 Bilder je Zyklus (Phase = 3*i/27), duty 0,38,
  kontakt HL 0,00 / VR 0,02 / HR 0,50 / VL 0,52 (diagonale Paare), S H 0,64 / V 0,64, mitte H 0,04 / V -0,02, hub H 0,10 / V 0,12,
  ab H 30 / V 28, spitze H 45 / V 60, aussen 0,02, senk 0,03, streck 0,97/0,985)`. Rumpf: Rollen +-1,5 Grad (Trab ist ruhig),
  Becken/Brust nicken +-1,5 Grad doppelt je Zyklus, Kopf ruhig (gegen die Schultern), Schulterblatt +-14 Grad, Schwanz klein.
  **Weg = 3 x 0,64/0,38 x 0,51 x 0,35 = 0,90189 E -> 1,603 Kacheln/s.**
- **Run (Galopp):** `pose_run` mit `RUN_J = RUN des Erwachsenen, aber T=8 (Phase = 2*i/16), S 0,61 / 0,61, duty 0,25`.
  **Weg = 2 x 0,61/0,25 x 0,51 x 0,35 = 0,87108 E -> 2,613 Kacheln/s.**
- Erstes = letztes Bild (ausser Weg), Weg linear (0 -> -Weg in lokal z, Vorzeichen wie die Datei des Erwachsenen), S/duty im Skript
  und im Weg aus EINER Konstante (`WEG_BEZUG` 0,35 x N x S/duty x M2U / K_WELT).
- **Grenzen:** Rumpf-Wippen (Becken z Spitze-Spitze) <= 4 cm bei 1,0; Log "ueberstreckt" = 0 Bilder; Gelenkgrenzen wie
  `baer_kampf_2c.py:571-586`; Gleiten je Stuetzphase <= 1,5 cm bei 1,0 (~0,5 cm im Spiel); linkes/rechtes Bein und Hinterfuss/Unterarm
  ohne Durchdringung (Netz). Geht S 0,64 nicht innerhalb dieser Grenzen: S schrittweise auf 0,56 senken (1,40 Kacheln/s) und melden;
  darunter Rueckfall B (1,32). Run: S auf 0,56 (2,40) senken, darunter Rueckfall B (2,22).
- **Fuer den Code-Lauf (nicht in diesem Lauf):** das Junge geht 1,60 und rennt 2,61 Kacheln/s; die Folgen-Schwellen in
  `BanditsNPCBearFollow.lua` danach richten (Spieler gehend 2,27).

### 5.4 Sitzen S_J (SPEZ D.4, angepasst an das Generator-Junge)
Weg wie SPEZ D.4: parametrische Sitz-Spuren von 2c in der Kopie `baer_clips_rig.py` (aus `baer_kampf_junges.py`, das bereits
`NCB_JUNGES_SKELETT`, `NCB_JUNGES_SITZ`, `NCB_JUNGES_AUS` kann; Teilstand -- Ausgaben selbst pruefen), Gelenke aus `skelett_rig.json`,
an denselben Zeiten abgetastet, Becken-z und Sprunggelenk-z am Netz geloest. Gilt aus D.4 weiter: Brust->Hals 52-62 Grad (min 48),
Ellbogen 160-172 Grad, Pranken flach, Hinterfuss-Sohle nach vorn/oben, Sitz-Ausnahmen `ch_sp` -22 / `he_ne` +68, Sit erstes = letztes
Bild bit-gleich, SitDown Bild 0 und StandUp letztes Bild = Idle-Haltung. **Neu (Generator):** Handgelenk |y| 0,09-0,13 und
Hinterfuss-Mitten 0,55-0,76 m (engere Spur; Vorderpranken zwischen den Hinterfuessen, Innenkante Hinterfuss >= 1,5 cm neben der
Pranke); Kopf-Zahlen aus D.4 ersetzt durch: Kopf oben auf dem Koerper, Atlas ueber oder vor dem Schultergelenk, **Blick geradeaus
bis leicht gehoben** (Augen-Nase-Linie -40..-33 Grad in jedem Sit-Bild; Ruhe/Foto -41 = leicht gesenkt), Kopf gegen Hals <= 68 Grad. Vergleich neben `baer/begleiter/kevin_sitzvorlage.png`.

### 5.5 Boden (SPEZ D.3)
Stuetzbilder wie beim Erwachsenen (`werkzeug/stuetz.py`); je Stuetzpfote tiefste Haut ohne Krallen **-1,5..+1,5 cm, Ziel +-1,0**;
ganzes Netz nie < -0,5 cm; aufliegende Haut (Sitzen, Liegen, Eat-Schnauze) 0,0..+1,2. Hub dz je Bild glatt (Sprung <= 0,3 cm je Bild),
erst nach den endgueltigen Gewichten loesen (SPEZ D.2: "erst Sitz-Drehungen, dann Gewichte, zuletzt Hub und Weg").

### 5.6 Reihenfolge CLIPS
1. `baer_clips_rig.py` (Blender, CPU): Trab, Galopp, Sitz-Trio mit `skelett_rig.json` -> `rig/clips/clips_neu.npz` (je Clip und Bild
   Welt-Drehung und -Lage je Knochen wie `NCB_JUNGES_AUS`), Log mit Klemm-/Ueberstreck-Zaehlern.
2. Export Zwischenstand (6.1) -> Dump -> **Gewichte endgueltig** mit `baer_gewichte_rig.py` (unveraendertes Skript der Rolle SKELETT,
   nur Dump-Pfad; ~20 min Hintergrund) -> Hub je Clip an der Haut -> D.5-Abweichungen (Eat/Death/Dead/IK) -> Endexport -> Dump.
3. Alle Pruefungen 6.3, Blaetter 6.4, `CLIPS.md`.

---------------------------------------------------------------------------------------------------------------------------

## 6. EXPORT UND PRUEFUNG

### 6.1 Export-Weg (`baer/spiel/baer_export_rig.py`, Kopie von `baer_export_junges.py`, nur numpy)
Gerippe = `_arbeit/baer_junges/eingang/NCBear.glb` (08ec7806, = gespielter Erwachsener); getauscht werden nur Puffer:
POSITION/NORMAL/TEXCOORD_0/JOINTS_0 (u8)/WEIGHTS_0, Indizes u16, inverse Bind = inv(Ruhe des Jungen), Knoten-`translation` = `lage_E`,
Animations-Ausgaenge (Lagen; Drehungen nur der neuen Clips und der D.5-Zeilen). Ein Netz, ein Primitiv, **kein Material, kein Bild**.
Aenderungen gegenueber der Vorlage:
- Netz aus `C_rig_basis.npz` + `gewichte_rig.npz` (Ecken je GLB-Punkt, verschweisste Lage fuer Normalen); **UV ist schon glTF
  (v von oben): NICHT noch einmal spiegeln** (die Vorlage spiegelt, weil ihre npz v von unten hat). Probe: Texturfarbe an der Nase
  im Render schwarz, am Auge dunkel.
- Skelett aus `skelett_rig.json` `lage_E` (statt Faktor x Erwachsener), Becken-Regel mit `dx_m`.
- Translation_Data: Walk/Run aus dem Generator-Weg (5.3); byte-gleiche Clips: Erwachsener x 0,35 (dort 0).
- Neue Clips aus `clips_neu.npz` (Welt -> lokal mit denselben Ruhe-Drehungen); Hub aus `hub.json`, D.5 aus `abw.npz`.
- Textur: `C_rig_basis.png` -> `rig/out/42/media/textures/Body/NCBearCub.png` (1024 x 1024, RGB 8 Bit, kein Alpha).
- Ziel GENAU `rig/out/42/media/models_X/Skinned/NCBearCub.glb`, `.../textures/Body/NCBearCub.png`, `rig/out/md5.txt`.
  Mesh-Name `NCBearCub`; `nc_bear_cub.txt` (model NCBearCub_Body, animationsMesh NCBearCub, `Skinned/NCBearCub.glb`) bleibt passend.

### 6.2 Harness (vor jedem "fertig")
```
JB=C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin; G="C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"
H=C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness
"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump <abs>/rig/out/42/media/models_X/Skinned/NCBearCub.glb <abs>/rig/clips/dump_final.txt skin
```
Danach `dumpread.py` -> `.pkl`; alle Clip-Posen fuer Renders und Messungen NUR aus diesem Dump (Lehre fix_baby: alter Dump = altes Netz).

### 6.3 Messungen (Werkzeuge kopieren nach `rig/werkzeug/`, Originale nie aendern, Pfade auf den neuen Dump)
Quellen: `_arbeit/baer_junges/werkzeug/` (clip_pruef, clip_schluessel, glb_datei, kanten, stuetz, gleiten, dehnung_lib, haushalt,
sitz_zahlen, sp_skelett, render_junges, gpu_render.sh), `_arbeit/baer_2c/pruef/gegen/werkzeug/` (g_technik, g_mess, g_dehn2, g_sitz2,
g_kragen, g_naht, render_pruef), `_arbeit/baer_baby/werkzeug/` (pruef_glb, mensch.py + mensch.npz, render_baby), `rig/plan/mess/`.
| Nr | Messung | Grenze |
|---|---|---|
| T1 | 26 Knochen Name/Eltern/Reihenfolge, Knoten-Drehungen byte-gleich; 15 Clips Namen/Dauer/Zeit-Accessoren byte-gleich; 1 Netz, 1 Primitiv, kein Material/Bild; Skalier-Schluessel 1,0; Lagen = `lage_E` ausser Pelvis/Translation_Data | exakt |
| T2 | Importer laedt (Dump.java), Dreiecke <= 20.000, GLB-Punkte < 65.536, <= 4 Einfluesse, Summe 1 +-1e-4, kein NaN, Matrizen Importer gegen eigene FK <= 1e-4 | hart |
| T3 | 0 offene, 0 nicht-mannigfaltige, 0 entartete Kanten/Dreiecke; 0 in der Ruhe umgekippte Dreiecke | hart |
| T4 | Drehschluessel byte-gleich in den 10 Clips aus 5.2, Abweichungen nur laut Tabelle (Zaehlung je Clip/Knochen gegen CLIPS.md) | hart |
| T5 | Textur 1024 x 1024 RGB 8 Bit, kein Alpha; beide Dateien am festen Pfad, MD5 in `md5.txt` | exakt |
| T6 | NCBearTest, NPC Crew, `_arbeit/baer_zaehmen/mod/`, Originalskripte `baer/spiel/*` (ausser neuen `*_rig.py`) unveraendert (MD5 vorher/nachher) | exakt |
| C1 | Boden je Stuetzpfote und Bild, alle 15 Clips | -1,5..+1,5 cm, Ziel +-1,0 |
| C2 | ganzes Netz tiefster Punkt je Bild; aufliegende Haut | >= -0,5 cm; 0..+1,2 |
| C3 | Dehnung je Clip (alle 15): p99,5 sigma1; max; Achsel/Brust | <= 2,6; <= 4,0; <= 3,5 |
| C4 | Durchdringung: links/rechts, Hinterfuss/Unterarm (Walk, Run, Sitz-Trio) | 0 Punkte im anderen Bein |
| C5 | Sitz-Pose 5.4 (Sit Bild 0/30/60/90) | Toleranzen dort |
| C6 | Kopf: Augen-Nase-Linie Idle Bild 0 = Ruhewert +-5; Sit -40..-33; Kopf gegen Hals <= 68 (Sit) / <= 35 sonst | hart |
| C7 | Tempo Walk / Run aus dem GLB (Weg x 1,6 / Dauer); Gleiten je Stuetzphase (Haut der Pfote, Welt = lokal x 1,5 x 0,35 + Weg x 1,6) | 1,60 (>= 1,40) / 2,61 (>= 2,40); <= 1,5 cm bei 1,0 |
| C8 | Uebergaenge: SitDown 0 / StandUp Ende = Idle; Sit erstes = letztes; Walk/Run erstes = letztes (ohne Weg); Sprung je Bild wie SPEZ_2C 5.4 | |
| C9 | Kein Riss/keine Falte > 1 cm2 an Hals, Achsel, Leiste in N5-Bildern (Ton) | hart |
| K1 | Form gegen F2-Abgabe: Masse Abschnitt 1 (H, Bauch, Breite, Spur) bei 1,0 +-2 cm | |

### 6.4 Renderliste
GPU nur mit `gpu.lock`; Kevins Spielkamera az 0 / el 30; Spielgroesse = 577 px/E bei 0,35 = ~140 px hoch (gleich der Gegenpruefer-
Konvention "90 Grad = 140 px"); jede Ansicht in Spielgroesse UND gross; Ton und Textur nebeneinander; jedes Bild selbst ansehen.

| Nr | Inhalt | Kamera |
|---|---|---|
| R1 | Ruhe/Idle 0, 8 Seiten | az 0..315 el 30, Spielgroesse + gross |
| R2 | **alle 15 Clips je 4 Phasen** (0/25/50/75 % der Dauer) mit Bodenebene | az 0 el 30 und az 45 el 30, Spielgroesse + gross |
| R3 | Walk und Run Filmstreifen 8 Bilder + Pfoten-Spuren als Linie (Gleiten) | az 90 el 10 |
| R4 | **Sitzen** Sit Bild 0 und 60 **von vorn neben `kevin_sitzvorlage.png`**; dazu az -30 el 8, az 0 el 30 | |
| R5 | Kopf nah: vorn, 3/4, Seite, hinten; Ohren 0/90/180/270 (Ruhe, Sit, Walk Mitte) | |
| R6 | Eat tiefstes Bild, Death Mitte, Dead, Rear hoechstes Bild | az 60 el 15 |
| R7 | Foto `baer/begleiter/vorlage_C_junges_steht.jpg` neben Ruhe az 43 el 8 und Kevins Spielkamera gross | |
| R8 | Platzhalter (NCBearTest NCBearCub.glb, nur lesen) gegen neu: Ruhe, Walk Mitte, Sitzen, Eat; Spielgroesse | az 0 und 45 el 30 |
Blaetter: `rig/bilder/form.png` (FORM), `rig/bilder/skelett_proben.png` (SKELETT), `rig/bilder/clips.png` (CLIPS: je Clip eine Zeile).

### 6.5 Bild-Fragen (Ja/Nein mit Bildpfad, ein Nein ist ein Befund)
1. Ton ohne Textur: Baerenjunges von allen 8 Seiten? 2. Kopf gerade, Gesicht von vorn, Hals ohne Naht/Stufe? 3. Ohren von allen Seiten
runde dicke Baerenohren, von vorn ueber dem Umriss, von hinten keine Pilze? 4. Pfoten von der Seite rund, keine Platte? 5. Trab und
Galopp: Pfoten stehen, nichts schwebt/steckt im Boden, Gangbild flink und rund? 6. Sitzen wie Kevins Vorlage (aufrecht, Beine nach
vorn, Pranken dazwischen, Kopf oben, Blick geradeaus)? 7. Keine Risse/Beulen an Achsel, Leiste, Hals in irgendeinem Clip? 8. Neben
dem Foto und neben dem Platzhalter: klar besser?

---------------------------------------------------------------------------------------------------------------------------

## 7. WER BAUT WAS -- Uebergaben (Reihenfolge FORM -> SKELETT+GEWICHTE -> CLIPS+EXPORT)

| Rolle | Ordner / Skripte | liest | gibt ab |
|---|---|---|---|
| **FORM** | `rig/form/`, `baer/spiel/baer_form_rig.py`; Parameter `rig/form/C_form_rig.json`, `C_tex_rig.json`; Aufruf `nachbesserung/form2.py`, `textur2.py` (unveraendert) | `aus/C_schoen*`, `nachbesserung/*.json`, Abschnitt 1, `rig/plan/mess/*` | `rig/form/C_rig_basis.npz` (massgeblich), `C_rig_basis.glb` + `.png`, `landmarken_rig.json`, `f1/` (F1-Stand), `rig/FORM.md`, `rig/bilder/form.png` |
| **SKELETT+GEWICHTE** | `rig/skelett/`, `baer/spiel/baer_skelett_rig.py`, `baer_gewichte_rig.py` (+ Vorstufe von `baer_export_rig.py` fuer den Vorab-GLB, Abstimmung: CLIPS uebernimmt und erweitert sie) | FORM-Abgabe, `_arbeit/baer_junges/eingang/NCBear.glb`, `erw_2c.txt.pkl`, `koerper/skelett.json` (Format, `ruhe_m_erw`) | `skelett_rig.json`, `sp_rig.txt`, `gewichte_rig.npz`, `regionen_rig.npz`, `vorab/NCBearCub_vorab.glb` + `dump_vorab.txt(.pkl)`, `C_rig.blend`, `rig/SKELETT.md`, `rig/bilder/skelett_proben.png` |
| **CLIPS+EXPORT** | `rig/clips/`, `rig/out/`, `rig/werkzeug/`, `baer/spiel/baer_clips_rig.py` (Kopie `baer_kampf_junges.py`), `baer_export_rig.py` (Kopie `baer_export_junges.py`) | FORM- und SKELETT-Abgaben | `rig/clips/clips_neu.npz`, `hub.json`, `abw.npz`, `gewichte_end.npz`, `dump_final.txt(.pkl)`, **`rig/out/42/media/models_X/Skinned/NCBearCub.glb`**, **`rig/out/42/media/textures/Body/NCBearCub.png`**, `rig/out/md5.txt`, `rig/CLIPS.md`, `rig/bilder/clips.png` |

Regeln fuer alle: Originale nie aendern (Kopien tragen `_rig`), Zeilenenden der Vorlage behalten, absolute Pfade an Blender, Befehle
> 2 min im Hintergrund, GPU nur mit `gpu.lock` (`_arbeit/baer_gen/werkzeug/gpu_lauf.sh`), kein Schreiben ausserhalb `rig/` und
`baer/spiel/baer_*_rig.py`, kein git, kein Download. Wer eine Grenze nicht erreicht: Messwert, Bild und Grund in den Bericht, weiter.

---------------------------------------------------------------------------------------------------------------------------

## 8. RISIKEN UND FRAGEN

### 8.1 Risiken (in dieser Reihenfolge pruefen)
1. **Hals nach dem Geraderichten** (45 Grad Gier in einen kurzen, dicken Hals): Fellstriche koennen sich verziehen; Gegenmittel
   Laplace-Band + Fellstriche nachfuellen (2.2.1). Bild nah von 8 Seiten.
2. **Eat mit kurzem Hals und hohem Kopf:** die Schnauze erreicht den Boden evtl. nur mit Ellbogen-Beugen; Grenze in 5.2.
3. **Trab mit grossem Stuetzweg:** Rumpf wippt, wenn die Beine fast gestreckt sind (Reichweite 0,62 m bei 0,59 m Hueft-Sprung-Hoehe);
   Gegenmittel `senk` 0,03 und Fersenheben; Rueckfall-Leiter 5.3.
4. **Enge Spur (3-4 cm Luecke):** Bein-Bein-Beruehrung bei Becken-Rollen; C4 misst, `aussen` im Trab hilft.
5. **R ausserhalb 0,80-0,88:** groessere Rest-Bodenfehler in den byte-gleichen Clips (vorn), Hub + <= 3 Grad IK, sonst melden.
6. Gewichts-Optimierer ist auf das Erwachsenen-Netz zugeschnitten (Kopf-/Krallen-Uebernahme) -- muss sauber entfernt werden.
7. Ungeprueft (Laufzeit): Flimmern ohne Mipmaps, ob ein sehr flinker Trab im Spiel ruhig wirkt, "walkingOnTheSpot"
   (`_arbeit/baer_zaehmen/dec_b1b/AnimalWalkState.java:60`, Klasse selbst nicht dekompiliert) bei langsamen Tieren (schnellerer Gang senkt das Risiko), alles MP.

### 8.2 Fragen fuer Kevin
1. **Laenge:** Das Generator-Junge ist kompakt: ~49 cm lang bei 40 cm Schulter (L/H 1,2); deine Zahl war "rund 70", SPEZ 65 cm.
   Geplant: so lassen (es ist dein Foto). Oder Rumpf strecken?
2. **Maul:** Das Generator-Junge hat kein offenes Maul; geplant: Maul bleibt in allen Clips zu (das Junge greift nicht an). Spaeter ein
   Maul zum Fressen?
3. **Gang:** Gehen wird ein flinker Trab mit 1,6 Kacheln/s (heute 0,52), Rennen ein Galopp mit 2,6. Noch flinker (Trab 1,9 mit sehr
   schnellen Schritten) waere ein Schalter. Die Folgen-Schwellen im Code muessen danach angepasst werden (nicht in diesem Lauf).
4. **Kopfhaltung:** Der Kopf wird hoch getragen wie im Foto (der Erwachsene traegt ihn tief). So lassen?
5. **Pfoten:** Die Hinterpfoten sind kuerzer als beim grossen Baeren (24 statt 29 cm bei 1,0) -- so lassen?
6. Lizenz Foto C CC BY-SA 4.0 (aus C_FEIN), ungeprueft, kein Rechtsrat.

## 9. Dateien dieses Plans
- `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/RIG_PLAN.md` (diese Datei)
- `rig/plan/mess/mess_gen.py`, `gen_mess.json` (Seitenriss, Beinbaender, Kopf), `schnitte_gen.py` + `schnitte_z.txt` (exakte
  Beinschnitte), `ton_raster.py` + `ton_roh/{seite_l,seite_r,vorn,hinten,oben}.png` (Massgitter, Achsen-Beschriftung = Bild-rechts-
  Achse), `tempo.py` (Tempo-Tabelle 5.3), `gen_landmarken_foto.json` (alle Zahlen aus Abschnitt 1), `uv_belegung.png`
