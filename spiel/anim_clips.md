# Baer: neue Kampf- und Ruheclips (Lauf baer-anim, Animator)

Stand 08.11.2026, PZ 42.21, Blender 5.2.3. **Statisch geprueft und offline gemessen, nicht gespielt.** Gemessen mit dem Importer
des Spiels (`tier_werkzeug/Probe.java`, `Dump.java` in `_arbeit/baer_spiel/harness`), dazu im Bau selbst und unabhaengig mit
`_arbeit/baer_anim/ref/gelenke_messen.py` (Kopie fuer die neue Clipliste: `anim/gelenke_messen_anim.py`). Gerendert nur auf der
RTX 4090 (OptiX, auch Entrauscher), vor jedem Render `tasklist` geprueft (das Spiel lief in diesem Lauf nie).

## 1. Ergebnis

- **Alle fuenf Kampfclips neu** (Hieb L/R, Doppelschlag, Aufrichten, Biss am Boden) und **fuenf neue**: Biss gegen Stehende,
  Hinsetzen, Sitzen (Schleife), Aufstehen, Fressen (Schleife). Dauern und Treffermomente genau wie `anim_spez.md` 7, also so, wie
  `NCBearFight.lua` (`F.ACTS`) und die Knoten-XML sie heute schon tragen: **Lua und XML muessen dafuer nicht geaendert werden.**
- **Gelenkgrenzen sind feste Regel im Skript** (`GRENZEN`, `GRENZEN_RUMPF`, `GRENZE_KLAV`, `GRENZE_KIEFER`, Werte aus
  `anim_referenz.md` 2). Jede Taste jedes neuen Clips wird nach dem Loesen dagegen geklemmt. Unabhaengige Gegenmessung mit
  `gelenke_messen.py`: **alle 13 gemessenen Clips "ok", 0 Befunde** (Grenzen und Spruenge je Bild).
- **Der Knick ist weg:** Pfote in der Luft dreht relativ zum Unterarm (nicht mehr als Weltdrehung), die Arme laufen in der Luft im
  Gelenkraum (Bogen statt gerader Weltlinie). Pfote seitlich (sup) heute -20..+28 statt -139/-168, Ellbogen nie unter 84,6 Grad
  innen (vorher 26,6/36,4).
- **Idle, Walk, Run, Death, Dead bit-gleich** (Abtastzeiten, Modellmatrizen, Schluessel: Abweichung 0,00e+00).
- **Fussgleiten** jeder aufgesetzten Pfote unter 0,01 Kacheln (hoechstens 0,0096), **nichts im Boden** (tiefster Hautpunkt der neuen
  Clips hoechstens 2,1 mm drunter, Pfote beim Abstuetzen).
- **Haut-Dehnung: Ziel 3-fach je Dreieck NICHT ueberall erreicht.** Erreicht bei Biss am Boden (2,67), Fressen (2,25); Sitzen,
  Hinsetzen, Aufstehen 3,84; Biss 4,47; Aufrichten 4,99; Doppelschlag 5,44; Hieb 5,93/6,05 (vorher 6,8-7,3). Der 99,5-%-Wert liegt
  ueberall bei hoechstens 3,27. Gruende und Versuche in Abschnitt 6.
- **Sitzen:** Kevins Vorlage ist mit diesem Skelett nur teilweise erreichbar (Abschnitt 7): Pfoten flach am Boden **oder** aufrechter
  Oberkoerper, beides zusammen geht geometrisch nicht. Gebaut ist "Pfoten flach am Boden, Ruecken rund, Kopf hoch".

## 2. Dateien

| Datei | Inhalt |
|---|---|
| `NPCCrew-Nebenprojekte/baer/spiel/baer_kampf_anim.py` | Bauweg (Kopie, Original `baer_kampf.py` bleibt). Neu: Grenzen, Messung, Klemmen, Spuren aller zehn Clips, Bericht je Clip |
| `_arbeit/baer_anim/mod/42/media/models_X/Skinned/NCBear.glb` | **neu**, MD5 `f06d9ec12990509c852ad578a0b31608`, 1.155.960 Byte; zweimal gebaut byte-gleich |
| `_arbeit/baer_anim/mod/42/media/textures/Body/NCBear.png` | unveraendert (MD5 `a800c084...`, der Bau schreibt dieselbe Datei) |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_kampf_vorschau.mp4` | Hieb L, Hieb R, Biss stehend, Biss liegend, Doppelschlag, Aufrichten; links Spielwinkel, rechts Seite |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_sitzen_vorschau.mp4` | Hinsetzen, Sitzen, Aufstehen, Fressen (zweimal) |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_sitzen_vergleich.png` | Sitzen schraeg von vorn, von vorn, von der Seite, neben `kevin_sitzvorlage.png` (nur angesehen, nichts uebernommen) |
| `_arbeit/baer_anim/anim/` | Werkzeuge: `bau.sh`, `pruef_anim.py` (Dump-Pruefung), `render_anim.py`, `blatt.py`, `video.py`, `kodieren.py`, `pose_probe.py`, `gewicht_probe.py`, Berichte `bericht*.json` |

Neu bauen: `blender --background --factory-startup --python baer_kampf_anim.py -- ZIEL "" _arbeit/baer_anim/modell/liege_alt.json [BERICHT.json]`
(leeres Argument 2 = rundes Netz des Modellbauers; ohne die Liege-Datei weichen Death/Dead ab, siehe `anim_modell.md` 6).

## 3. Clips (GLB, vom Importer gelesen)

| Clip | Dauer | Bilder | Schleife | Treffer (s / m_TimePc) | was trifft, wo (Kacheln vor Bip01, seitlich, Hoehe m) | Ablauf |
|---|---|---|---|---|---|---|
| NCBear_SwipeL | 1,50 | 46 | nein | 0,60 / 0,40 | Pranke links: 0,945 vor, 0,03 innen, 0,52 m | Laden 0-0,20 (Gewicht rechts-hinten), Ausholen 0,20-0,44 (Schulter hebt, Pranke aussen auf Schulterhoehe, Ellbogen 95), Schlag 0,44-0,60 (Rumpf dreht den Schlag, Brust gieren +12 -> -14, Arm 140 Grad fast gestreckt, Krallen voraus), Durchzug und Aufsetzen mit Gewicht 0,60-0,80 (0,30 vor dem Platz), Schritt zurueck 1,08-1,30 |
| NCBear_SwipeR | 1,50 | 46 | nein | 0,60 / 0,40 | gespiegelt | gespiegelt aus SwipeL |
| NCBear_Bite | 1,30 | 40 | nein | 0,52 / 0,40 | Schnauze: 0,948 vor, Mitte, 0,935 m (Hals/Brust eines Zombies) | duckt 0-0,17, Vorstoss mit halbem Aufrichten und langem Hals 0,17-0,48, Vorderpfoten loesen sich und landen 0,07 weiter vorn (0,62), Zubeissen 0,48-0,56, zweimal Schuetteln 0,58-0,95 (Brust rollt mit), je ein Schritt zurueck |
| NCBear_Maul | 1,60 | 49 | nein | 0,544 / 0,34 | Schnauze: 0,681 vor, 0,07 m | Kopf und Hals gehen tief (nicht die Vorderbeine), linke Pranke tritt vor und drueckt nieder, Biss, zweimal Schuetteln mit rollenden Schultern, Schritt zurueck |
| NCBear_Slam | 2,40 | 73 | nein | 1,30 / 0,54 | beide Pranken am Boden: 0,579 vor, je 0,171 seitlich | halb aufrichten 0,22-0,90 (Becken -22, Brust -42, Pranken vorn-oben, Ellbogen 85-125), Niederschlag 0,90-1,27 (Arme strecken sich, Pfoten erst kurz vor dem Aufsetzen flach), Aufprall und Nachfedern, links 1,55-1,75 und rechts 1,75-1,95 zurueck |
| NCBear_Rear | 3,00 | 91 | nein | - (Bruellen ab 0,81 s / 0,27) | - | hoch 0,25-0,85 (Becken -48, Lende fast gerade, Brust -78..-80), oben mit Bruellen (Maul 37-38 Grad 0,95-1,85), Vorderpranken haengen locker vor der Brust (Ellbogen 102-108), Kopf hoch (welt -44), Hinterbeine stabil (Knie 124-163), leichtes Schwanken; herunter 2,05-2,72, Aufsetzen am Ruheplatz |
| NCBear_SitDown | 1,60 | 49 | nein | - | - | Knie beugen, Gewicht nach hinten; Hinterpfoten je ein halber Schritt nach vorn (0,25-0,47 / 0,42-0,64), Becken sinkt und dreht, Vorderpfoten ruecken zwischen die Hinterbeine (0,70-1,00), Hinterbeine strecken sich nach vorn, Sohle nach vorn-oben (0,90-1,22); Ende = Sitzpose S |
| NCBear_Sit | 4,00 | 121 | ja (erstes = letztes Bild = S) | - | - | Atmen (Brust 2 Grad, zwei Zuege), Kopf schaut langsam um (gieren 10 -> 28 -> 10), kurzes Maulzucken, Pfoten fest |
| NCBear_StandUp | 1,30 | 40 | nein | - | - | Hinterbeine halb unter den Koerper (0-0,30), Oberkoerper nach vorn, Hinterteil hebt, Vorderpfoten auf den Ruheplatz (0,30-0,58), Hinterpfoten ganz zurueck (0,55-0,92), Grundhaltung |
| NCBear_Eat | 3,20 | 97 | ja (= Fresspose E) | - | - | Kopf am Boden vor den Pfoten, Zubeissen 0,50-0,72, Reissen hoch-zurueck 0,72-1,20 (linke Pranke drueckt), Kauen mit halb gehobenem Kopf 1,20-2,70 (Kiefer 4-14 Grad, 2,5 Hz), zurueck |

Alle neuen Clips: Translation_Data ueber den ganzen Clip 0, Bip01 still (Weg 0), alle 26 Knochen mit Schluesseln, Kampfclips
beginnen und enden in der Grundhaltung (Mittel von DeerStag_Idle01). Die Ton-Momente der Knoten passen zur Bewegung: Wusch
0,42 s = Beginn des Schlags, Aufschlag-Ton 1,27 s = Aufsetzen der Pranken, Knurren 0,10 s, Bruellen 0,81 s = Maul geht auf.

**Fuer die Lua-Seite (Reichweiten, Formeln aus `anim_spez.md` 7; nicht von mir geaendert):** swipeReach = 0,945 + 0,55 = rund 1,5
(heute 1,4), slamReach = 0,579 + 0,9 = rund 1,5 (bleibt), biteReach = 0,948 + 0,45 = rund 1,4 (heute vorlaeufig 1,3), maulReach =
0,681 + 0,42 = rund 1,1 (heute 1,2). Ohne Nachziehen trifft der Hieb bei 1,4 Kacheln, sichtbar reicht die Pranke 0,95.

## 4. Wie gebaut (im Skript `baer_kampf_anim.py`, Abschnitt "Kampf- und Ruheclips")

- **Spuren je Bein:** `ball_` (Ballen in Welt oder `("S", d)` relativ zur Schulter/Huefte), `welt_` (1 = Pfote flach in Welt, fuer den
  Boden; 0 = relativ zum Unterarm mit `rel_` = (dors, aus, sup) in den Messgroessen), `ik_` (1 = IK zum Ballen; 0 = Vorwaertskette
  aus `fk_` = (prot, abd, Drehung, Ellbogen innen), dazwischen je Gelenk gemischt), `pole_` (Pol im Rahmen der Brust bzw. des Beckens).
- **Klemmen** (`bein_kampf`): Abstand Schulter-Handgelenk in den Ellbogengrenzen; liegt die Oberarmdrehung ausserhalb, wird der
  Ellbogen um die Achse Schulter-Handgelenk geschwenkt (Handgelenk bleibt); danach Schulter (prot, abd, Drehung), Ellbogen (reines
  Scharnier) und Pfote (dors, aus, sup per Newton) auf die Grenze. Rumpf: Lende, Brust, Hals, Kopf gegen den Elternknochen;
  Schulterblatt; Kiefer 0-40. Wie oft geklemmt wurde, steht je Clip im Bericht (`klemm`).
- **Ganzer Koerper:** jede Phase mit Pfotenbewegung hat Becken- (Versatz und Drehung), Lenden-, Brust-, Hals-, Kopf- und
  Schulterblattwerte; Hinterpfoten stehen, die Knie arbeiten (Hieb 117-134, Aufrichten 124-163).
- **Schritte:** die Pfote bleibt waehrend eines Schritts flach in Welt (sonst tauchen beim Abheben die Zehen in den Boden).

## 5. Messwerte (Bericht `_arbeit/baer_anim/anim/bericht19.json`, Dump `dump19.txt` = `dump18.txt`)

Gelenke, ganzer Clip (Vorderbein des Schlags bzw. beide; Grenzen in Klammern):

| Clip | Ellbogen innen (55..173) | Pfote dors (-115..75) | Pfote sup (-20..35) | Oberarm prot (-70..60) | groesster Sprung je Bild sup/Drehung/dors (20/20/35) | geklemmt |
|---|---|---|---|---|---|---|
| SwipeL | 95,0..172,8 | -34,9..61,0 | -15,5..28,0 | -15,3..40,0 | 11,1 / 2,7 / 25,4 | VL Abstand 7 Bilder (Abheben), VR Pfote 9 (Stuetzpfote dreht im Koerper) |
| Slam | 84,6..167,2 | -45,0..53,2 | -9,3..10,0 | -25,0..25,9 | 5,7 / 2,0 / 17,5 | V Abstand 11 je Seite (Landeanflug) |
| Bite | 112,6..172,8 | -20,0..68,3 | -13,6..5,0 | -19,6..19,9 | 9,6 / 1,1 / 33,5 | V Abstand 6/4 |
| Maul | 91,8..149,6 | 17,8..53,2 | -20,0..-2,9 | -35,1..1,4 | 5,8 / 1,8 / 11,9 | VL Pfote 5 |
| Rear | 102,0..167,1 | -46,0..53,2 | -9,2..12,0 | -56,0..-1,6 | 4,5 / 0,4 / 14,2 | V Abstand 14 (Abheben/Aufsetzen), HR Huefte 10 |
| SitDown / Sit / StandUp | 129,5..172,8 / 158,7..162,8 / 108,1..158,7 | 41..75 / 67..69 / 41..67 | -9..0 | -45..-1 | <= 14,5 | Sitzen 0; Hinsetzen/Aufstehen Knie am Anschlag 55 (Abstand 6-11 Bilder) |
| Eat | 106,5..109,4 | 32..40 | -14..-9 | -35..-20 | <= 0,6 | 0 |

Hinterbeine in allen Clips innerhalb der Grenzen (Knie 55..163, Fuss dors -122..-69, Drehung -14..+10). Rumpf gegen Eltern: Lende
nick -19..+14, Brust -13..+14, Hals -43..+31, Kopf gieren/rollen hoechstens 17/22 (Grenzen 20/15/50/30/25).

Haut und Boden (Importer des Spiels, `pruef_anim.py`; Kacheln = E x 1,5):

| Clip | tiefster Hautpunkt (E) | Gleiten aufgesetzter Sohlen (Kacheln, max) | Dehnung max (Ort) | 99,5 % | Kanten > 3 |
|---|---|---|---|---|---|
| SwipeL / SwipeR | -0,0021 / -0,0018 (Stuetzpfote) | 0,0082 | 5,93 / 6,05 (Rippen hinter der Achsel, Brustunterseite) | 2,88 / 2,96 | 113 / 126 |
| Slam | 0,0000 | 0,0064 | 5,44 (Rippen hinter der Achsel, oben) | 3,27 | 199 |
| Bite | 0,0000 | 0,0007 | 4,47 (Rippen hinter der Achsel) | 2,72 | 72 |
| Maul | -0,0021 | 0,0053 | 2,67 | 1,58 | 0 |
| Rear | -0,0010 | 0,0094 | 4,99 (Innenseite Unterschenkel/Leiste) | 2,80 | 81 |
| SitDown / Sit / StandUp | -0,0007 / 0,0000 / 0,0000 | 0,0056 / - / 0,0096 | 3,84 (Unterschenkel) | 2,12-2,15 | 3-6 |
| Eat | -0,0002 (Kiefer am Futter) | 0 | 2,25 | 1,47 | 0 |
| alt: Idle / Walk / Run / Death / Dead | unveraendert | unveraendert | 1,33 / 3,79 / 4,37 / 4,12 / 4,11 (vorher 1,36 / 3,79 / 4,37 / 4,12 / 4,11) | | |

## 6. Gewichte und Dehnung

- **Geaendert (wirkt nur auf die Haut, nicht auf die Bewegung):** (1) Die Brust unter dem Hals (vor und zwischen den Vorderbeinen,
  unter z 0,42-0,62 m) gehoert der Brust statt dem Hals (`rumpf_anteile`); vorher zog ein gesenkter Hals sie mit (Sitzen 4,84 -> 3,84,
  Biss am Boden 3,62 -> 2,92). (2) Brustunterseite zwischen den Vorderbeinen 30 Runden mehr geglaettet (`BRISKET`; Hieb 6,8 -> 6,3).
  Alte Clips dabei nicht schlechter (Tabelle oben).
- **Versucht und verworfen** (`gewicht_probe.py`, alle Clips je Variante): Unterarm-Gewicht aus der Brustmitte nehmen (Riss wandert an
  die neue Grenze, Hieb 16-fach), engere Regel fuer die Beininnenseite (Gang 6-fach), ganze Bereiche Achsel/Leiste 6-80 Runden glaetten
  (Kante an der Maskengrenze, bis 9-fach), ganzes Netz 4-16 Runden (Hieb bleibt 6,3-6,7).
- **Warum 3-fach nicht geht:** die hoechsten Werte sitzen an kurzen Kanten am Rippenbogen hinter der Achsel und an der Brustunterseite,
  wo die Haut von Rumpf- auf Armgewicht wechselt. Hebt der Arm 0,4-0,5 m nach vorn, muesste dieser Wechsel ueber rund 20 cm Haut
  laufen; zwischen Bein und Brustmitte sind es 14 cm. Mit linearem Haeuten und diesem Netz bleibt nur weniger Armhub (Hieb und
  Doppelschlag sind schon etwas zurueckgenommen: prot 46 -> 40 bzw. 34 -> 24, Dehnung 6,3 -> 5,9 bzw. 6,0 -> 5,4) oder ein
  Korrekturknochen bzw. ein Netz mit Falte an der Achsel (Lauf baer-fell). Sichtbar ist es im Spielwinkel als kurz gedehnte Achsel
  beim Ausholen und im Treffer.

## 7. Sitzen und Kevins Vorlage (`anim_sitzen_vergleich.png`)

- Gebaut: Hinterteil am Boden (Becken -42, tiefster Hautpunkt 0), Ruecken rund (Lende +14, Brust +14 gegen den Elternknochen),
  **Vorderbeine gerade (Ellbogen 159-163) mit flachen Pranken zwischen den Hinterbeinen**, Hinterbeine vorn mit Ferse am Boden und
  Sohle nach vorn-oben, Kopf hoch (Hals -56) und zu seiner linken Seite (gieren 10, rollen 5), Schleife mit Atmen und Umschauen.
- **Unterschied zur Vorlage:** dort ist der Oberkoerper senkrecht. Gemessen an der Haut (`pose_probe.py`): sitzt das Hinterteil am
  Boden, liegt das Becken-Gelenk bei rund 0,38 m; damit die Vorderpfoten mit geradem Arm (0,64 m) flach auf den Boden reichen, darf die
  Schulter hoechstens rund 0,72 m hoch sein. Mit Brust -14 Grad ist sie 0,716 m; bei Brust -24 sind es 0,80 m, bei -40 rund 0,9 m,
  dann haengen die Pfoten 8-20 cm ueber dem Boden. Deshalb wirkt unser Baer gedrungener, Kopf und Ruecken bilden einen Buckel.
- **Kevins Wahl (Vorschlag):** (a) so lassen; (b) zweite Sitzpose "aufrecht", Pranken liegen dann im Schoss bzw. auf den Hinterpfoten
  statt am Boden (Quelle 14 in `anim_referenz.md`); (c) im Lauf baer-fell die Vorderbeine/Rumpfproportion des Netzes anpassen.

## 8. Unsicher, offen

1. **Nicht gespielt.** Blende zwischen den Knoten (0,10-0,30 s), Drehung des Zombies beim Treffer und ob die Treffer im Spiel sitzen,
   zeigt nur Kevins Test.
2. Haut-Dehnung ueber 3 an Achsel und Leiste (Abschnitt 6).
3. Sitzen weicht von der Vorlage ab (Abschnitt 7).
4. Stuetzpfote beim Hieb dreht auf dem Ballen 7 Grad mit dem Koerper und steht dabei 5 mm hoeher (sonst klemmt das Handgelenk bzw.
   taucht 9 mm in den Boden); Gleiten 0,008 Kacheln.
5. Fressen: die linke Pranke steht auf dem Futter nur 6 cm vor ihrem Ruheplatz (Blende rein/raus schiebt sie sonst sichtbar).
6. Reichweiten in `NCBearFight.lua` (Abschnitt 3) zieht die Lua-Seite nach; sonst stimmt der Treffer im Spiel nicht mit dem Bild.

Statisch geprueft und offline gemessen, nicht gespielt.
