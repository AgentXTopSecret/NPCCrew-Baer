# SKELETT -- Lauf baer-rig-junges, Rolle SKELETT+GEWICHTE (11.11.2026)

**Statisch geprueft, nicht gespielt.** Kein Clip neu gebaut (das macht CLIPS+EXPORT), nichts in Test-Mods, NPC Crew, Spiel oder
`_arbeit/baer_zaehmen/mod/` geschrieben; kein git, kein Download. Originale per MD5 vorher/nachher gleich (`rig/skelett/md5_vorher.txt`,
`md5_nachher.txt`: baer_gewichte_2c.py, baer_export_junges.py, baer_*_junges.py, baer_kampf_2c.py, baer_form_rig.py, eingang/NCBear.glb +
erw_2c.txt.pkl, FORM-Abgabe C_rig_basis.*, NCBearTest NCBearCub.glb/.png/NCBear.glb, sp_skelett.py).

## 0. Ergebnis kurz
- **Skelett fertig** (`rig/skelett/skelett_rig.json`): 26 Knochen, Namen/Eltern/Reihenfolge/Knoten-Drehungen byte-gleich mit NCBear.glb
  08ec7806; Beine exakt 1,000; Rumpf isotrop **R 0,900** (gemessen 0,913, Plan-Grenze 0,90); Spur Q_H 0,644 / Q_V 0,554; Fuss-Faktor 0,361
  (Toe0 am Ballen); Hals C7 -> Atlas 15,3 cm, **delta +10,5 Grad** (Ziel <= 15); Netz-Versatz x -0,0825 m. Eigene Achsmessung: Beinachsen
  des Netzes 1,3-3,3 Grad gegen die Knochenrichtung (< 4: kein Nachdrehen). Alle Gelenke im Netz, >= 4,4 cm unter der Haut.
- **Gewichte fertig** (`rig/skelett/gewichte_rig.npz`, `regionen_rig.npz`): Formel in Gelenk-Koordinaten + harmonischer Hals + Raumglaettung
  + Optimierer (Kopie baer_gewichte_2c.py, 4 Laeufe). <= 4 Einfluesse, Summe 1 (+-1e-7), Kopf mit Ohren starr (Head 1,0, 1.995 Punkte),
  Pfoten starr (>= 0,99 unter dem Gelenk), Krallen 1,0, Stummel Tail 1,0, Kiefer ohne Gewicht.
- **Dehnung, Vorab-GLB (15 Clips des Erwachsenen mit Becken-Regel, ohne Hub), alle Bilder, Importer-Dump:** p99,5 **1,14-2,23** (Grenze 2,6),
  max **1,40-3,52** (Grenze 4,0), Achsel/Brust max **2,81** (Grenze 3,5) -- in JEDEM Clip im Rahmen. Erster Formel-Stand: p99,5 bis 3,9, max 8,1.
- **Probe-Posen** (Kopf +-30 nicken, +-35 gieren, Vorder-/Hinterbein +-35, Rear hoch, Run 4/13, Sit 0, Walk, Eat, Idle) gerendert und selbst
  angesehen: keine Risse, keine Beulen, Ohren und Stummel folgen starr. Rest (Abschnitt 6): Falte hinter der Wange bei reinem Kopf-Gieren 35
  Grad und kleine Nackenfalte bei Kopf-Heben 30 Grad -- beides ausserhalb dessen, was die Clips verlangen (Erwachsener: Kopf gegen Hals
  hoechstens ~9 Grad gieren, ~6 Grad heben).
- **Vorab-GLB** `rig/skelett/vorab/NCBearCub_vorab.glb` + Harness-Dump `dump_vorab.txt(.pkl)`: Importer laedt, 19.418 Dreiecke, 11.811
  GLB-Punkte, Matrizen Importer gegen eigene FK <= 2,6e-5 E in allen Bildern aller Clips, Gewichte Importer = eigene W (1,3e-7), 390/390
  Dreh- und Skalier-Ausgaenge, 1.170/1.170 Zeit-Accessoren byte-gleich.
- `C_rig.blend` (Armatur + Netz + Gewichte + 15 Clips + Textur eingepackt), Blaetter `rig/bilder/skelett_proben.png`,
  `skelett_proben_nah.png`, `skelett_gewichte.png`, `skelett_ruhe.png` (alle selbst angesehen).

---------------------------------------------------------------------------------------------------------------------------

## 1. Skelett (RIG_PLAN 3.1; Skript `baer/spiel/baer_skelett_rig.py bauen`)

### 1.1 Eigene Achsmessung der Beine (exakte waagerechte Schnitte, Schwerpunkt je Schnitt alle 1 cm)
| Bein | Schnitte (z) | freie Hauptachse gegen Knochenrichtung des Erwachsenen | Rest der Linie (Knochenrichtung) max / Mittel |
|---|---|---|---|
| VL / VR | 23 (0,12-0,34 m) | 3,3 Grad (frei 18,5 Grad vor, Knochen 16,2) | 0,98 / 0,37 cm |
| HL / HR | 21 (0,12-0,32 m; darueber verschmelzen die Hinterbeine) | 1,3 / 1,4 Grad (frei 23,6 Grad zurueck, Knochen 22,8) | 1,24 / 0,68 cm |
Alle Achsen < 4 Grad: kein Nachdrehen der Beine (RIG_PLAN 3.1 letzte Zeile). Die FORM-Beine stehen also wirklich in Knochenrichtung.
Aus den Linien: Hand-/Sprunggelenk auf z der Kette (0,097 / 0,100 m), Ellbogen/Knie (0,407 / 0,410), Schulter/Huefte ueber die
Oberarm-/Oberschenkel-Vektoren des Erwachsenen (Laenge und Richtung 1,000).

### 1.2 Entscheidungen
| Groesse | Wert | Begruendung |
|---|---|---|
| **R (Rumpf isotrop)** | **0,900** (gemessen 0,913) | Abstand Huefte-Schulter des Netzes / 0,750. 0,913 liegt ueber der Plan-Grenze 0,90 -> 0,90 genommen; der Rest (0,9 cm) verteilt sich auf beide Beinpaare: Knochen hinten 0,50 cm vor, vorn 0,50 cm hinter der Netzachse (Linienrest der Messung selbst bis 1,2 cm). Ausserhalb 0,80-0,88 -> `sp_rig.txt` neu gerechnet (Abschnitt 2): R naeher an 1 heisst KLEINERE Rest-Bodenfehler als SPEZ_JUNGES (0,85). |
| DX (Becken-Regel) | 0,0375 m = 0,375 (1 - R) | RIG_PLAN 3.1 |
| Netz-Versatz x | -0,0825 m | Mitte Huefte/Schulter des Netzes auf die des Skeletts; Skelettrahmen = Formrahmen + (-0,0825, 0, 0) |
| Q_H (Huefte quer) | 0,644 -> Huefte \|y\| 0,145 m (Erw. 0,25) | Huefte ueber der gemessenen Beinlinie (Knie \|y\| 0,157, Sprung 0,142 liegen dann genau auf der Messlinie) |
| Q_V (Schulter quer) | 0,554 -> Schulter \|y\| 0,112 m (Erw. 0,225); Schluesselbein-Ansatz quer mit demselben Faktor | ebenso (Ellbogen 0,127, Hand 0,117) |
| Fuss-Faktor (Toe0) | 0,361 -> Toe0 bei (-0,360 / +-0,139 / 0,080) | Richtung = Fussachse des Erwachsenen, Laenge bis ueber den Ballen des Netzes (FORM-Landmarke x -0,277 Formrahmen). **Der Plan-Wert ~0,78 passt nicht mehr:** FORM setzte das Sprunggelenk mitten ueber die Pfote (Ferse 11 cm dahinter), mit 0,78 laege Toe0 vor der Zehenspitze. Toe0 traegt keine Gewichte und dreht in keinem Clip des Erwachsenen (gemessen: Streuung 0,0 Grad in allen 15) -- wichtig nur fuer den Gang-Generator (Abrollpunkt). |
| C7 (Neck-Gelenk) | Formrahmen (0,290 / 0 / 0,965) | Halsansatz in der Mittelebene ueber dem Brustgelenk, 31 % der Tiefe unter der Oberlinie (1,188), Mitte der "Halsroehre" Kehlfalte 0,70 .. Nacken 1,20 |
| Atlas (Head-Gelenk) | Formrahmen (0,440 / 0 / 0,935) | unter der Ohr-Hinterkante (x 0,438), Augenhoehe 0,955 - 0,045 W (W 0,446); FORM-Schaetzung (0,441 / 0,922) bestaetigt |
| delta Hals | **+10,5 Grad** (C7->Atlas 11,3 Grad unter der Waagerechten, Erwachsener 21,8) | Ziel <= 15 erfuellt; Halslaenge 15,3 cm |
| Kiefer | Formrahmen (0,610 / 0 / 0,865), keine Gewichte | Maul bleibt in allen Clips zu (Plan) |
| Schwanz | Formrahmen (-0,585 / 0 / 0,748) | Stummelwurzel, 4,4 cm unter der Haut (Stummel-Maske Mitte -0,630 / 0,755) |
Lage-Vektoren aus den Weltlagen ueber die UNVERAENDERTEN Ruhe-Drehungen (np.linalg.solve; Probe FK -> Weltlage < 1e-9 E). Calf/Foot/
Forearm/Hand = Erwachsener auf 1e-9 (assert). Kiefer/Hals/Kopf/Schwanz/Toe0 frei.

### 1.3 Gelenk-Tabelle (tier-Meter bei 1,0, Skelettrahmen; linke Seite) -- Generator-Junges gegen SPEZ_JUNGES (R 0,85) und Erwachsener
| Knochen | Junges (dieser Lauf) | SPEZ_JUNGES B.5 | Erwachsener | unter der Haut (cm) |
|---|---|---|---|---|
| Bip01 | -0.000 / 0.000 / 0.720 | -0.000 / 0.000 / 0.720 | -0.000 / 0.000 / 0.720 | - |
| Pelvis | -0.342 / -0.000 / 0.717 | -0.327 / -0.000 / 0.716 | -0.370 / 0.000 / 0.720 | 29,0 |
| L_Thigh | -0.422 / 0.145 / 0.690 | -0.404 / 0.212 / 0.690 | -0.460 / 0.250 / 0.690 | 14,8 |
| L_Calf | -0.312 / 0.157 / 0.410 | -0.294 / 0.225 / 0.410 | -0.350 / 0.262 / 0.410 | 9,3 |
| L_Foot | -0.443 / 0.142 / 0.100 | -0.424 / 0.209 / 0.100 | -0.480 / 0.247 / 0.100 | 8,4 |
| L_Toe0 | -0.360 / 0.139 / 0.080 | -0.194 / 0.203 / 0.045 | -0.250 / 0.240 / 0.045 | 4,4 |
| Spine | -0.062 / -0.000 / 0.744 | -0.064 / -0.000 / 0.741 | -0.060 / 0.000 / 0.750 | 26,6 |
| Spine1 | 0.207 / -0.000 / 0.789 | 0.191 / -0.000 / 0.783 | 0.240 / 0.000 / 0.800 | 18,1 |
| L_Clavicle | 0.262 / 0.050 / 0.897 | 0.242 / 0.085 / 0.885 | 0.300 / 0.100 / 0.920 | 18,4 |
| L_UpperArm | 0.253 / 0.112 / 0.717 | 0.234 / 0.191 / 0.716 | 0.290 / 0.225 / 0.720 | 9,9 |
| L_Forearm | 0.193 / 0.127 / 0.407 | 0.174 / 0.206 / 0.406 | 0.230 / 0.240 / 0.410 | 8,3 |
| L_Hand | 0.282 / 0.117 / 0.097 | 0.264 / 0.196 / 0.096 | 0.320 / 0.230 / 0.100 | 8,3 |
| Neck | 0.207 / 0.000 / 0.965 | 0.412 / -0.000 / 0.783 | 0.500 / 0.000 / 0.800 | 18,1 |
| Head | 0.357 / 0.000 / 0.935 | 0.612 / -0.000 / 0.704 | 0.700 / 0.000 / 0.720 | 18,6 |
| Jaw | 0.527 / 0.000 / 0.865 | 0.738 / -0.000 / 0.614 | 0.804 / 0.000 / 0.645 | 5,9 |
| Tail | -0.668 / 0.000 / 0.748 | -0.608 / -0.000 / 0.699 | -0.700 / 0.000 / 0.700 | 4,4 |
Alle Gelenke liegen im Netz (Windungszahl 1,000), jedes >= 4,4 cm unter der Haut (Plan >= 2 bzw. 1,5 cm). Neu gegen SPEZ_JUNGES: Hals und
Kopf sitzen 20-25 cm weiter hinten und 18-23 cm hoeher (kurzer Hals, Kopf hoch getragen wie im Foto); C7 liegt senkrecht ueber dem
Brustgelenk (Spine1), der Hals laeuft fast waagerecht (Neck-Lage zeigt nach oben statt nach vorn -- mechanisch egal, die Clips liefern
Drehungen; Folge: neigt der Clip die Brust, schwingt der Kopf eher vor als ab -- fuer Eat wichtig, Abschnitt 8).

---------------------------------------------------------------------------------------------------------------------------

## 2. Becken-Regel ueber alle 15 Clips (`rig/skelett/sp_rig.txt`, Kopie von sp_skelett.py mit Lage-Vektoren)
Gelenk-Ebene vor dem Hub, cm bei 1,0. Stuetzbild = Pfote des Erwachsenen < 1 cm.
- **Hinten exakt** (Fehler 0,15-0,73 cm, nur wo das Becken rollt) -- wie geplant. Ausnahme Death-Ende/Dead: 10,4 cm, weil das Tier auf der
  Seite liegt und die Huefte 10,5 cm schmaler ist -> dort gilt die Haut (CLIPS, Hub).
- **Vorn (stuetzende Handgelenke):** Idle -0,48..-0,08 | Walk -0,95..+0,63 | Run -0,21..+0,95 | Rear -0,30..+0,04 | Swipe -0,98..+1,55 |
  Slam -0,30..+0,83 | Bite -1,32..+0,39 | Maul -0,77..+2,10 | Eat +0,46..+0,79 | **Sitz-Trio -3,70** (die Sitz-Clips des Erwachsenen,
  nur Vorab; CLIPS baut S_J neu). Gleiten vorn: Walk 2,50, Run 1,03, **Swipe 7,17** (!), sonst <= 1,7 cm.
- **Quer:** in Idle/Walk/Run/Rear/Slam/Bite/Maul/Eat eine feste Verschiebung der Pfoten um -10,5..-11,5 cm (schmalere Spur) -- wie geplant.
  **Nicht konstant** in Swipe (-12,0..-7,9: der Rumpf dreht, die schmaleren Schultern setzen die Stuetzpfote anders) und Death (bis +7,8,
  Liegen). -> CLIPS: Swipe-Stuetzpfote messen (Gleiten 7,2 cm bei 1,0 = 2,5 cm im Spiel).
- **Bein an Bein (Achsen):** Ruhe vorn 23,4 / hinten 28,4 cm. Death Bild 35/36: vorn 0,1 / hinten 0,7 cm (Erwachsener selbst 8,2 / 7,6,
  also schon in Beruehrung) -> die schmalere Spur laesst die Beine im Fallen ineinander laufen. Sit/SitDown/StandUp (umgerechnet): vorn
  1,3-1,4 cm (Erwachsener 23,8) -- Grund mehr fuer S_J (Handgelenk \|y\| 0,09-0,13, Plan 5.4). Hinterfuss <-> Unterarm Run min 10,6 cm
  (Erwachsener 8,5).

---------------------------------------------------------------------------------------------------------------------------

## 3. Netz: Splitter-Dreiecke entschaerft (Abweichung vom Plan, begruendet)
Optimierer-Lauf 2 hatte alle Clips im Rahmen bis auf EIN Dreieck an der rechten Flanke (Rear sigma1 5,4): ein Splitter mit 5 mm Hoehe auf
12,5 cm Laenge. Splitter messen in der duennen Richtung jede kleine Scherung als riesige Dehnung. `baer_skelett_rig.py` tauscht deshalb die
lange Kante von Splitter-Dreiecken (Hoehe/Laenge < 0,08, Kante > 2 cm), nur wo keine UV-Naht liegt, beide neuen Dreiecke besser sind und
die Normalen < 30 Grad abweichen: **59 Splitter vorher, 49 Kanten getauscht, 11 bleiben** (UV-Naehte). Punkte, UV, Textur unveraendert;
groesste Texel-Verschiebung durch die neue Diagonale 0,11 Texel. Netz danach 0 offene / 0 nicht-mannigfaltige / 0 entartete Kanten,
19.418 Dreiecke, 11.811 GLB-Punkte. FORM-Dreiecke stehen weiter in `netz_rig.npz` (`T_form`, `T_glb_form`).

---------------------------------------------------------------------------------------------------------------------------

## 4. Gewichte (RIG_PLAN 4; Skript `baer/spiel/baer_gewichte_rig.py`, Teile formel / opt / dehnung / abgabe)

### 4.1 Formel (Gelenk-Koordinaten, Skelettrahmen)
- **Beine:** Zugehoerigkeit wie die bewaehrte 2c-Formel (`bein_anteil` in baer_kampf_2c.py), aber um die Beinachse des JUNGEN (Polylinie
  Huefte/Schulter -> Knie/Ellbogen -> Sprung/Hand): waagerechter Abstand zur Achse (zum Bauch hin x 1,5 strenger, nach aussen x 0,75),
  Hoehen-Uebergang Hinterbein z 0,44-0,84 / Vorderbein 0,40-0,78, darunter (z < 0,28 hinten / 0,36 vorn) alles Bein. Knochen je Lauf-
  Parameter entlang der Kette: Knie/Ellbogen-Uebergang 7 cm (Plan); **Pfote = 1 - sst(Gelenk - 0,005; Gelenk + 0,085; z)** (unter dem Hand-/
  Sprunggelenk >= 0,99; Uebergang 9 cm statt Plan 5 cm -- mit 5 cm riss das Handgelenk im Walk auf sigma1 11,7).
- **Schritt-/Brustbein-Regel (neu; Grund: die Beine stehen nur 3-5 cm auseinander):** an der Linie, an der linkes und rechtes Bein
  zusammenlaufen (gemessen: Hinterbeine z 0,334, Vorderbeine z 0,388), nur Rumpf; der Bein-Anteil waechst ueber 12 cm Abstand (|y| bzw.
  Hoehe unter der Linie). Wird VOR und NACH der Glaettung angewandt (die Glaettung trug sonst 15 % Unterschenkel in die Mittellinie ->
  sigma1 30 im Run).
- **Rumpf:** Pelvis -> Spine -> Spine1 entlang x, Uebergaenge 0,20 breit um die Gelenke (Plan 0,12; mit 0,12 entstand im Rear eine scharfe
  Querfalte am Lendenuebergang).
- **Kopf/Hals:** Kopf starr = vor der Ebene Atlas - 0,03 m; Ebenen-Normale senkrecht auf die Linie Nacken (hinter der Ohr-Hinterkante) ->
  Kehlfalte (am Netz gemessen, Normale (0,999 / 0 / 0,045)), ueber der Kehlfalte, innerhalb der Kopfbreite; Ohren immer. Rumpf fest: hinter
  C7 - 0,08 m, 10 cm unter der Kehlfalte, an Beinen, aussen an den Schultern. **Dazwischen harmonisch** (Kotangens-Laplace auf dem Netz,
  CG ohne scipy, 583 freie Punkte): Head = sst(0,3; 1; h), Rumpf = 1 - sst(0; 0,7; h), Neck = Rest. Grund: die FORM-Maske `kopf` reicht oben
  bis x 0,26 (der ganze Nacken waere starr) -- als starrer Kopf ungeeignet.
- **Schwanz:** Stummel-Maske Tail 1,0, Ring 2 cm mit dem Becken.
- **Raumglaettung** sigma 0,03 m (raum_glatt aus baer_form_junges.py) je Koerperhaelfte, ausser starre Zonen; dann Seitenregel (linke
  Knochen nie rechts, Vorderbein nie hinter der Mitte Huefte/Schulter x -0,085 und umgekehrt, Hals/Kopf nie am Bein), <= 4, Summe 1.

### 4.2 Optimierer (Kopie baer_gewichte_2c.py; entfernt: KOPF_ALT / alt_von / k1_dy / k2c_dx)
Frei 5.832 Punkte (Rumpf, Hals, Achsel, Leiste, Bein-Uebergaenge), starr 3.879. Bilder: jedes 3. Bild aller 15 Vorab-Clips + Swipe 6-23 einzeln
+ **16 Zusatzbilder = die Probe-Posen** (Kopf +-30/+-35 nur Head und halb Neck/Head, Vorder-/Hinterbein je Seite +-35), damit die Gewichte
auch fuer Bewegungen taugen, die erst die neuen Clips bringen. Neu: `traeger` (ein Knochen nur, wo die Formel ihn im Umkreis ~8 cm hat --
Lauf 1 schob sonst Hand 0,06 ans Brustbein und Fuss 0,01 an die Flanke), `ueber_w/ueber_s` (Zusatzstrafe ueber sigma1 3,5 in allen Dreiecken),
Falten-Zone um Ruecken/Leiste/Hals erweitert, `achsel_w` 20 ueber 3,0, `boden` 0 (Vorab-Clips ohne Hub: ein Bodenabstand ist dort kein
Gewichtsfehler). Gradient gegen zentrale Differenzen in float64 geprueft (954,08 / 954,08; 284,95 / 285,01). Laufzeit 26 min CPU.

| Lauf | Aenderung | Ergebnis (schlechtester Clip) |
|---|---|---|
| Formel (erster Stand) | -- | p99,5 bis 3,92 (Rear), max bis 8,14 (Rear) |
| 1 | Optimierer, jedes 5. Bild | p99,5 <= 2,27, max 5,60 (Run), Achsel/Brust 4,26; fremde Knochen (Hand am Brustbein) |
| 2 | + traeger, Achsel 20, ueber 3,5, jedes 3. Bild | p99,5 <= 2,24, max 5,38 = EIN Splitter-Dreieck (Abschnitt 3) |
| 4 (Abgabe) | + Kantentausch, Hals-Uebergang breiter, Rumpf 0,20, Zusatzbilder | **p99,5 <= 2,23, max <= 3,52, Achsel/Brust <= 2,81** |
(Lauf 3 abgebrochen, durch 4 ersetzt.)

---------------------------------------------------------------------------------------------------------------------------

## 5. Dehnung je Vorab-Clip (`baer_gewichte_rig.py dehnung gewichte_rig.npz vorab/dump_vorab.txt.pkl`, ALLE Bilder, Importer-Matrizen)
Gueltig wie 2c (Kante >= 7,4 mm, Hoehe >= 2 mm). Falten = Dreiecke mit sigma2 < 0,5 in irgendeinem Bild.

| Clip | p99,5 sigma1 | max | Achsel/Brust max | Falten | Ort des Max | Lauf 1 p99,5 / max |
|---|---|---|---|---|---|---|
| Idle01 | 1,14 | 1,40 | 1,15 | 0 | Hals | 1,15 / 1,43 |
| Walk | 1,57 | 2,93 | 2,15 | 1.703 | Leiste | 1,59 / 3,50 |
| Run | 1,83 | 2,71 | 2,37 | 3.235 | Leiste | 1,88 / 5,59 |
| Death | 1,74 | 3,14 | 2,23 | 2.317 | Leiste | 1,76 / 3,13 |
| Dead | 1,82 | 3,10 | 1,67 | 943 | Leiste | 1,82 / 3,09 |
| Rear | 2,23 | 2,81 | 2,81 | 781 | Achsel | 2,27 / 5,02 |
| SwipeL | 1,85 | 3,52 | 2,78 | 406 | Bauch | 1,86 / 3,01 |
| SwipeR | 1,93 | 3,34 | 2,73 | 375 | sonst | 1,95 / 3,38 |
| Slam | 1,88 | 2,68 | 2,65 | 390 | sonst | 1,87 / 3,90 |
| Bite | 1,48 | 2,46 | 2,29 | 673 | Hals | 1,53 / 3,69 |
| Maul | 1,82 | 2,84 | 2,06 | 376 | Hals | 1,90 / 3,21 |
| Eat | 1,69 | 2,59 | 2,23 | 245 | sonst | 1,76 / 2,73 |
| SitDown | 1,82 | 2,95 | 2,05 | 1.848 | Leiste | 1,91 / 3,44 |
| Sit | 2,06 | 2,73 | 2,18 | 624 | Hals | 2,23 / 3,71 |
| StandUp | 1,73 | 2,91 | 2,05 | 2.011 | Leiste | 1,80 / 3,84 |

**Umgekippte Dreiecke** (Normale gegen die mitgedrehte Ruhe-Normale > 90 Grad = Ueberfaltung in Knickfalten, `werkzeug/kipp_dump.py`, max je
Clip, jedes 2. Bild) -- Junges / gespielter Erwachsener, gleiche Messung aus beiden Importer-Dumps: Idle 13 / 4, Walk 156 / 207, Run 708 / 590,
Death 665 / 547, Dead 532 / 293, Rear 270 / 293, Swipe 96 / 95, Slam 155 / 140, Bite 176 / 152, Maul 170 / 81, Eat 278 / 116, Sit 214 / 289,
StandUp 319 / 497. Gleiche Groessenordnung wie beim gespielten Erwachsenen (Knickfalten hinter Knie/Ellbogen, beim Liegen); Eat und Maul
hoeher (kurzer Hals, der Kopf geht in die Brust -- Abschnitt 8).
Torso-Anteil an den sichtbaren Beinen (|y| > 0,03): Hinterbein z 0,15-0,25 im Mittel 0,08, z 0,25-0,32 0,29 (Innenseite am Schritt, so
gewollt: Schritt-Regel; Aussenseite im Mittel 0,05); Vorderbein 0,04 / 0,17. Unter z 0,15 null.

---------------------------------------------------------------------------------------------------------------------------

## 6. Probe-Posen (RIG_PLAN 4.3; `rig/bilder/skelett_proben.png`, `skelett_proben_nah.png`; selbst angesehen)
Gehaeutet wie die Engine (v' = Summe w M inv(Bind) v); eigene Posen auf der Ruhe, Clip-Bilder aus dem Importer-Dump des Vorab-GLB.

| Pose | sigma1 max | p99,5 | Bild |
|---|---|---|---|
| Kopf nicken ab 30 (nur Head) | 2,24 | 1,74 | Hals glatt, Kehle legt sich weich |
| Kopf heben 30 (nur Head) | 2,83 | 1,83 | **kleine Nackenfalte** hinter den Ohren (Ton: 2-3 dunkle Punkte) |
| Kopf gieren links / rechts 35 (nur Head) | 2,63 / 3,35 | 1,94 / 1,80 | **Falte hinter der Wange** auf der Innenseite der Drehung (Ton deutlich, mit Textur wie eine Hautfalte) |
| dieselben mit halb Neck / halb Head | 1,71-2,53 | 1,57-1,85 | Falten deutlich kleiner (sigma2 min 0,11-0,33 statt 0,01) |
| Vorderbein vor / zurueck 35 | 2,18 / 1,75 | 1,66 / 1,32 | Achsel glatt (aussen, innen, Textur) |
| Hinterbein vor / zurueck 35 | 2,85 / 3,04 | 1,67 / 1,81 | Leiste glatt; vorn kleine Leistenfalte beim Vorschwingen (natuerlich) |
| Rear hoechstes Bild (45) | 2,74 | 2,36 | steht aufrecht, Ruecken ohne Querfalte, Arme frei |
| Run 4 / 13 | 2,00 / 2,29 | 1,65 / 1,74 | sauber; Bild 13: die Beine des Erwachsenen-Galopps kreuzen beim kompakten Jungen (Clip-Frage, CLIPS baut den Galopp neu) |
| Sit 0 (Erwachsener umgerechnet, nur Vorab) | 2,72 | 2,02 | Falte Schulter -> Brust; Vorderpfoten 5,7 cm im Boden, Unterarme fast ineinander (Clip-Frage, S_J) |
| Walk 7 / 21 | 2,42 / 2,27 | 1,46 / 1,54 | sauber |
| Eat tiefstes Bild (21) | 2,59 | 2,10 | Kopf wird in die Brust gedrueckt (kurzer Hals + Eat des Erwachsenen) -- Clip-Frage (D.5 Eat) |
| Idle 0 | 1,38 | 1,15 | sauber |

Ohren: in jeder Pose starr am Kopf (Head 1,0), Form unveraendert. Stummel: folgt starr (Tail 1,0, Ring 2 cm). Pfoten: starr, Sohle eben.
Spielgroesse (az 0..315 / el 30, ~140 px): ruhig, keine Kanten. **Urteil:** fuer alle Bewegungen der 15 Clips sauber; die zwei Falten (Kopf
35 Grad nur ueber Head, Kopf heben 30 Grad) liegen ausserhalb der Clip-Bereiche (gemessen am Erwachsenen: Head gegen Neck gieren <= 8,7,
heben <= 5,9, senken <= 56,7 Grad (Sit); Neck gieren <= 10,8 Grad).

---------------------------------------------------------------------------------------------------------------------------

## 7. Vorab-GLB und Harness (RIG_PLAN 4.3; `baer/spiel/baer_export_rig.py`, Vorstufe fuer CLIPS)
`python baer_export_rig.py rig/skelett/netz_rig.npz rig/skelett/gewichte_rig.npz rig/skelett/vorab/NCBearCub_vorab.glb` -> Dump.java (skin) ->
`dump_pkl.py`. Gerippe NCBear.glb 08ec7806, Puffer getauscht, UV NICHT gespiegelt (schon glTF), Normalen ueber verschweisste Punkte.
Pruefung `werkzeug/glb_pruef.py` -> `vorab/pruef_vorab.json`:
- Knoten-Namen/Kinder/Drehungen/Skalierung und Skin-Joints = Erwachsener; Knoten-translation = lage_E (Abweichung 0).
- 1 Netz, 1 Primitiv, kein Material, kein Bild; 19.418 Dreiecke (<= 20.000), 11.811 GLB-Punkte, Indizes u16; <= 4 Einfluesse, Summe
  0,99999994-1,0000001; kein NaN; 0 offene / 0 nicht-mannigfaltige / 0 entartete Kanten.
- 15 Clips, Namen und Dauern = Erwachsener; Zeit-Accessoren 1.170/1.170, Dreh-Ausgaenge 390/390, Skalier-Ausgaenge 390/390 byte-gleich;
  Lagen konstant = lage_E ausser Pelvis (Becken-Regel) und Translation_Data (Walk/Run x 0,35).
- Importer (Dump.java): laedt, 26 Knochen (Namen = Skelett), 15 Clips, 11.811 Punkte, 19.418 Dreiecke; Matrizen Importer gegen eigene FK in
  allen Bildern aller Clips <= 2,6e-5 E (Grenze 1e-4); Gewichte Importer = eigene W (1,3e-7); Bind = eigene Ruhe fuer alle gewichteten
  Knochen (ungewichtete: Einheit, wie bekannt).

---------------------------------------------------------------------------------------------------------------------------

## 8. Uebergabe an CLIPS+EXPORT
1. **Netz = `rig/skelett/netz_rig.npz`** (NICHT C_rig_basis.npz): Skelettrahmen (Formrahmen x - 0,0825), Kantentausch, `T`/`T_glb`/
   `glb_punkt`/`UV` (glTF, nicht spiegeln), alle FORM-Masken. `gewichte_rig.npz` `W` gehoert genau zu diesen Punkten.
2. **Skelett = `rig/skelett/skelett_rig.json`** (Format wie koerper/skelett.json: `ruhe_m` im Skelettrahmen, `lage_E`, `dx_m` 0,0375, ...).
   Fuer Kopien von baer_kampf_junges.py: `NCB_JUNGES_SKELETT=.../rig/skelett/skelett_rig.json` (liest nur `ruhe_m`). Achtung dort:
   Knochen-SCHWAENZE werden mit Erwachsenen-Vektoren gebildet; beim Jungen zeigt die Neck-Lage nach oben (C7 senkrecht ueber Spine1), die
   Head-Lage weicht 10,5 Grad von der Neck-y-Achse ab -- fuer Drehungen egal, Lagen nur ueber `lage_E` rechnen.
3. **Export** = `baer/spiel/baer_export_rig.py` (Vorstufe, liest skelett_rig.json; Haken `sitz=`, `hub=`, `abw=` wie baer_export_junges.py).
   Fuer die neuen Walk/Run: Translation_Data aus dem Generator-Weg einbauen (heute: Erwachsener x WEG_BEZUG 0,35).
4. **Gewichte endgueltig** (RIG_PLAN 5.6) mit den fertigen Clips: `python baer_gewichte_rig.py formel netz_rig.npz skelett_rig.json F.npz`,
   dann `opt F.npz DUMP_FINAL.pkl OPT.npz schritt=3` (~26 min, im Hintergrund), dann `abgabe OPT.npz ORDNER` und `dehnung`.
   Die Zusatzbilder (Probe-Posen) bleiben dabei an (Vorgabe `zusatz=1`). Danach `werkzeug/abschluss.sh` als Vorlage fuer die Kette.
5. **Toe0** sitzt ueber dem Ballen (Fuss-Faktor 0,361, z 0,080): das Sprunggelenk steht mitten ueber der Pfote, Ferse 11 cm dahinter -- der
   Gang-Generator muss mit diesem Abrollpunkt rechnen (die Pfote ist starr am Foot; Toe0 hat kein Gewicht und dreht beim Erwachsenen nie).
6. **Beobachtungen fuer die Clips:** (a) Swipe: Stuetzpfote gleitet 7,2 cm gegen den Erwachsenen (schmalere Schultern, Rumpf dreht), quer
   nicht konstant -- C1/C7 messen, ggf. D.5-IK (<= 3 Grad). (b) Death/Dead: Beine laufen im Fallen ineinander (Achsen vorn 0,1 / hinten 0,7
   cm; Erwachsener 8,2 / 7,6) und liegen bis 10 cm hoeher (schmale Huefte, dicker Rumpf) -- Hub an der Haut. (c) Eat: der Kopf drueckt in die
   Brust (kurzer, hoher Hals); die Neck/Head-Abweichung D.5 (bis delta + 15 = 25,5 Grad) wird gebraucht. (d) Sitz: S_J mit Handgelenk
   |y| 0,09-0,13 passt zur Schulter |y| 0,112; der umgerechnete Erwachsenen-Sitz ist unbrauchbar (Pfoten 3,7 cm im Boden, Unterarme 1,4 cm
   Achsabstand). (e) Galopp: Hinterfuss <-> Unterarm im Erwachsenen-Run 10,6 cm Achsabstand, in Run 13 kreuzen die Beine sichtbar.
7. Werkzeuge (`rig/skelett/werkzeug/`): `proben_posen.py` (Posen + Dehnung + umgekippte Dreiecke), `proben_render.py` (Cycles, Ton/Textur,
   Boden ein/aus), `proben_cfg.py`, `proben_cfg_nah.py`, `proben_blatt.py`, `nah_blatt.py`, `glb_pruef.py`, `kipp_dump.py`, `dehn_ort.py`
   (wo liegen die groessten Dehnungen), `gew_bild.py`, `raster.py` (Software-Raster ohne GPU), `schnitt.py`, `skelett_bild.py`,
   `blend_bauen.py`, `abschluss.sh` (ganze Kette nach dem Optimierer).

---------------------------------------------------------------------------------------------------------------------------

## 9. Abweichungen vom Plan (alle begruendet)
| Plan | hier | Grund |
|---|---|---|
| R 0,78-0,90 (Start 0,82) | 0,900 (gemessen 0,913) | die FORM-Beine geben 0,913 vor; 0,90 = Plan-Grenze, Rest 0,5 cm je Beinpaar |
| Fuss-Faktor ~0,78 | 0,361 | Sprunggelenk steht nach FORM mitten ueber der Pfote; 0,78 laege vor der Zehenspitze |
| Rumpf-Uebergang 0,12 | 0,20 | Querfalte im Rear mit 0,12 |
| Sprung/Hand-Uebergang 0,05 | 0,09 (unter dem Gelenk >= 0,99) | Handgelenk sigma1 11,7 mit 0,05 |
| Huefte/Schulter-Uebergang 0,10 m entlang der Kette | Hoehen-Uebergang 0,44-0,84 / 0,40-0,78 und Abstand zur Achse (2c-Formel) | die Oberschenkel stecken ganz im Rumpf; die 2c-Form ist am gespielten Erwachsenen erprobt; der Optimierer verfeinert |
| FORM-Netz unveraendert | 49 Kanten getauscht | Splitter-Dreiecke (Abschnitt 3); Punkte/UV/Textur gleich, 0,11 Texel |
| Hals-Uebergang entlang der Halsachse | harmonisch zwischen starrem Kopf und Rumpf | kurzer, dicker Hals ohne "Roehre"; FORM-Kopfmaske ungeeignet (Nacken bis x 0,26) |
| Clips im Optimierer | + 16 Probe-Posen | Gewichte auch fuer die neuen Clips (Trab, Galopp, S_J) |

---------------------------------------------------------------------------------------------------------------------------

## 10. Fragen fuer Kevin
1. **Kopf drehen:** Dreht das Junge den Kopf weit (35 Grad) NUR im Genick, bildet sich hinter der Wange eine Hautfalte (im Fell wie eine
   Speckfalte). Die Clips des grossen Baeren drehen den Kopf gegen den Hals hoechstens ~9 Grad -- im Spiel also nicht zu sehen. Kommt spaeter
   ein Umschauen mit weiter Kopfdrehung, sollte der Hals mitdrehen (dann bleibt es glatt). In Ordnung so?
2. **Netz-Feinschliff:** 49 duenne "Splitter"-Dreiecke wurden umverbunden (unsichtbar, 0,11 Texel), damit die Dehnung nicht an einem
   Messfehler haengen bleibt. In Ordnung?
3. Aus RIG_PLAN 8.2 weiter offen (nicht diese Rolle): Laenge, Maul zu, Kopf hoch, kuerzere Hinterpfoten.

---------------------------------------------------------------------------------------------------------------------------

## 11. Dateien (alle unter `_arbeit/baer_gen/rig/`, Skripte unter `baer/spiel/`)
| Datei | Inhalt |
|---|---|
| `baer/spiel/baer_skelett_rig.py` (LF, neu) | `bauen [R=..]`: Achsmessung, Skelett, Gelenk-Probe, Kantentausch, sp_rig |
| `baer/spiel/baer_gewichte_rig.py` (CRLF wie Vorlage baer_gewichte_2c.py) | `formel`, `opt`, `dehnung`, `abgabe` |
| `baer/spiel/baer_export_rig.py` (LF wie Vorlage baer_export_junges.py) | Export-Vorstufe (CLIPS erweitert) |
| `skelett/skelett_rig.json` | Skelett (Format koerper/skelett.json + R, Q_H, Q_V, dx_m, delta_hals_grad, fuss_faktor, netz_versatz_x_m, Gelenke im Netz, sp_rig, splitter_tausch) |
| `skelett/netz_rig.npz` | Netz im Skelettrahmen (V, T, T_glb, glb_punkt, UV, Masken, V_foto, T_form/T_glb_form, kantentausch) |
| `skelett/gewichte_rig.npz` | W (9.711 x 26, Reihenfolge `namen` = Dump), formel_W, Masken, frei, regionen, opt_param |
| `skelett/regionen_rig.npz` | je Dreieck: achsel, brust, leiste, hals, kopf, ohr, pfote, kralle, stummel, bauch, sonst |
| `skelett/sp_rig.txt`, `mess_rig.json` | Becken-Regel ueber 15 Clips; Achsmessung |
| `skelett/vorab/NCBearCub_vorab.glb`, `dump_vorab.txt(.pkl)`, `pruef_vorab.json`, `dehnung_vorab.json` | Vorab-GLB, Harness, Pruefung, Dehnung |
| `skelett/C_rig.blend` | Armatur (26) + Netz + 26 Vertex-Gruppen + 15 Aktionen + Textur (eingepackt), glTF-Import des Vorab-GLB |
| `skelett/proben/posen_final.npz` (+ `_hals50`), `skelett/render/final`, `render/nah_final` | Probe-Posen und Renders |
| `bilder/skelett_proben.png`, `skelett_proben_nah.png`, `skelett_gewichte.png`, `skelett_ruhe.png` | Blaetter |
| `skelett/gew_formel.npz`, `gew_opt1/2/4.npz`, `log/opt*.log` | Zwischenstaende Optimierer |
| `skelett/md5_vorher.txt`, `md5_nachher.txt` | Originale unveraendert (alle 16 gleich) |
