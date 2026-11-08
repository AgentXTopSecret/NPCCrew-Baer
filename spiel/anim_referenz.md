# Baer: Bewegungs-Referenz fuer die neuen Clips (Lauf baer-anim)

Stand 08.11.2026. **Nur gelesen, recherchiert und offline gemessen, nichts gebaut, nichts gespielt.** Grundlage: Kevins Urteil
nach dem Test (ENTSCHEIDUNGEN.md, Abschnitte "Befehle, Sitzen, Fressen" und "Kampf-Animationen, Kevins Test"), seine Vorlage
`../begleiter/kevin_sitzvorlage.png` (nur angesehen), Websuche (keine Downloads; Quellen in Abschnitt 11), und eine Messung
der heutigen Clips aus `baer_kampf.py`.

Kurz: Der "komische Knick" ist gemessen und hat einen Namen. **Die Pranke ist gegen den Unterarm verdreht** (Hieb bis 139 Grad,
Doppelschlag bis 168 Grad, erlaubt sind rund 35) und **der Ellbogen ist zusammengefaltet** (Hieb 36, Doppelschlag 27,
Aufrichten 48 Grad Innenwinkel; Gang und Lauf kommen nie unter 77). Ursache im Skript: Die Pfotendrehung `rot_*` ist eine
**Weltdrehung**, auch wenn die Pfote in der Luft ist, und die Ausholpunkte liegen zu nah an der Schulter. Beim Hieb bewegen
sich Becken und Hinterbeine kaum (Becken dreht hoechstens 6 Grad, Hinterpfoten 0 m).

---

## 1. Messgroessen und Vorzeichen (alle Zahlen in diesem Bericht)

Werkzeug: `_arbeit/baer_anim/ref/gelenke_messen.py`. Es fuehrt `baer_kampf.py` bis zum Abschnitt "Netz" aus (reine
Posenmathematik) und misst jedes Bild. Aufruf:
`blender --background --factory-startup --python gelenke_messen.py -- AUSGABE.txt [QUELLE.py]`.
Gegenprobe gegen das gespielte `NCBear.glb` (MD5 `2e9a6d17...`, glTF-Import von Blender, Szene auf 30 Bilder/s):
Drehwinkel Schluesselbein->Oberarm, Oberarm->Unterarm, Unterarm->Pfote in 14 Bildern gleich bis auf 0,1 Grad
(`glb_gegenprobe.py`, `glb_gegenprobe.txt`). Die Messung beschreibt also genau das, was Kevin gesehen hat.

Skelett (26 Knochen, Namen aus `baer_tier.py`:56-75 und `baer_kampf.py`:145), Tier-Rahmen in Meter: x vorn, y links, z oben.

| Knochen | Eltern | Gelenk in Ruhe (x, y, z) | Bemerkung |
|---|---|---|---|
| `Bip01_Pelvis` | `Bip01` | (-0,37, 0, 0,72) | Becken |
| `Bip01_Spine` | Pelvis | (-0,06, 0, 0,75) | Lende |
| `Bip01_Spine1` | Spine | (0,24, 0, 0,80) | Brust |
| `Bip01_Neck` | Spine1 | (0,50, 0, 0,80) | Hals |
| `Bip01_Head` / `Bip01_Jaw` | Neck / Head | (0,70, 0, 0,72) | **Kopf bleibt in Form**; Kiefer 0-40 Grad |
| `Bip01_Tail` | Pelvis | (-0,70, 0, 0,70) | |
| `Bip01_L_Clavicle` (R gespiegelt) | Spine1 | (0,30, 0,10, 0,92) | Schulterblatt, **traegt keine Gewichte**, verschiebt nur die Schulter |
| `_UpperArm` / `_Forearm` / `_Hand` | Clavicle / UpperArm / Forearm | Schulter (0,29, 0,225, 0,72), Ellbogen (0,23, 0,24, 0,41), Handgelenk (0,32, 0,23, 0,10), Ballen (0,48, 0,22, 0,045) | Oberarm 0,316 m, Unterarm 0,323 m, Pfote 0,169 m |
| `_Thigh` / `_Calf` / `_Foot` / `_Toe0` | Pelvis / Thigh / Calf / Foot | Huefte (-0,46, 0,25, 0,69), Knie (-0,35, 0,262, 0,41), Ferse (-0,48, 0,247, 0,10), Ballen (-0,25, 0,24, 0,045) | 0,301 / 0,336 / 0,237 m; Toe0 folgt dem Fuss |

Messgroessen je Bein (VL, VR vorn, HL, HR hinten):

| Name | Bedeutung | Vorzeichen |
|---|---|---|
| **vor** | Oberarm gegen Schulterblatt bzw. Oberschenkel gegen Becken, Schwenk in der Laengsebene | + nach vorn |
| **abd** | dieselbe Achse seitlich | + nach aussen |
| **Dreh** | Drehung des Oberarms/Oberschenkels um die eigene Achse | + Ellbogen/Knie dreht nach aussen. Ruhe der IK: vorn -9, hinten -6 |
| **innen** | Innenwinkel Ellbogen bzw. Knie | 180 = gestreckt. Ruhe: Ellbogen 152,5, Knie 135,6 |
| **dors** | Pfote gegen die Verlaengerung des Unterarms in der Gelenkebene | + Zehen nach oben/vorn (dorsal), - Pfote nach hinten-unten (palmar). Ruhe vorn +54,6, hinten -99,3 |
| **aus** | Pfote aus der Gelenkebene (seitlicher Knick im Handgelenk) | |
| **sup** | Pfote um die Unterarmachse gedreht | + Sohle nach innen (Supination), - Sohle nach aussen |

Rumpf: Gieren/Nicken/Rollen wie `euler()` in `baer_kampf.py` (Gieren + Nase links, Nicken + Nase runter, Rollen + linke
Seite hoch). **Die Spuren `r_pel/r_sp/r_ch/r_ne/r_he` sind Weltdrehungen**; die Grenzen in Abschnitt 2 gelten fuer die
Differenz Kind gegen Eltern. Die Zieltabellen unten nennen fuer den Rumpf Weltwerte ("welt") und fuer die Beine die
Messgroessen dieser Tabelle.

Hilfszahl fuer `("S", d)`-Ziele: Abstand Schulter-Handgelenk je Ellbogen-Innenwinkel: 55 -> 0,30 m, 80 -> 0,41, 100 -> 0,49,
120 -> 0,55, 150 -> 0,62, 160 -> 0,63, 170 -> 0,64 m.

## 2. Gelenkgrenzen (feste Regel fuer den Animator, im Messskript als `GRENZEN`)

Hergeleitet aus drei Dingen, je Zeile genannt: (G) was der abgenommene Gang/Lauf/Idle heute schon tut (gemessen, alle drei
liegen innerhalb), (H) Hund als Raubtier-Vergleich (Goniometrie, Quelle 4; **kein Baer**), (B) Baer-Befunde (Quellen 1-3, 5).
Baerspezifische Gradzahlen fuer Ellbogen und Handgelenk gibt es in dem, was ich gefunden habe, nicht; die Grenzen sind deshalb
**Arbeitswerte mit Sicherheitsabstand**, nicht gemessene Baeren-Grenzen.

| Gelenk (Knochen) | Grenze | Begruendung |
|---|---|---|
| Schulter vor (UpperArm gegen Clavicle) | -70 .. +60 | H: Schulter Beugung 51 / Streckung 160 Grad, Stehen rund 110-120 -> rund -60/+45; mehr nur mit dem Schulterblatt. G: Lauf -42..+11 |
| Schulter abd | -20 .. +45 | B: Baeren schlagen und umklammern seitlich; G: -7..+3 |
| Oberarm-Drehung | -35 .. +20 | G: -14..-6; jenseits zeigt der Ellbogen zur Brust bzw. nach vorn |
| Schulterblatt (`klav_` nick / roll) | -25 .. +20 / -15 .. +15 | G: Gang +-12, Lauf +-14 |
| **Ellbogen innen** (Forearm) | **55 .. 173**, im Kampf moeglichst 90..165 | H: Beugung 49-51; dicke Unterarm-/Bizepsmasse und die Haut (Dehnung bis 7-fach bei 36 Grad, `kampf_anim.md`) -> 55. G: 77..172. **Knickt nur in eine Richtung** (Ellbogen zeigt nach hinten; Gegenrichtung = Dreh ausserhalb der Grenze) |
| **Handgelenk dors** (Hand) | **-115 .. +75** | H: Karpus Beugung 32, Streckung 204 (= 24 ueber gerade). B: Sohlengaenger, beim flachen Aufsetzen mit senkrechtem Unterarm rund +70. G: -52..+59 |
| Handgelenk aus der Ebene | -15 .. +15 | H: Karpus fast reines Scharnier; G: -10..+10 |
| **Handgelenk sup** | **-20 .. +35** | B: Grizzly setzt die Vorderpfote mit der Aussenkante zuerst auf (rund 34 Grad) und dreht sie im Schwung nach innen (Quelle 1); adulte Braunbaeren drehen den Unterarm weniger als Kragenbaeren (Quelle 5). G: -10..-5 |
| Huefte vor (Thigh gegen Pelvis) | -60 .. +80 | G: Lauf bis +75; H: Huefte 58..180 |
| Huefte abd / Dreh | -15 .. +35 / -25 .. +15 | Sitzen braucht +20..+30 Spreizung |
| Knie innen (Calf) | 55 .. 174 | H: Knie 58..173; G: 56..173. Knie zeigt nach vorn |
| Sprunggelenk dors (Foot) | -125 .. -45 | G: -111..-55; H: Tarsus 40..188 |
| Lende (Spine gegen Pelvis) gier/nick/roll | +-12 / +-20 / +-12 | G: Lauf nick +-6 |
| Brust (Spine1 gegen Spine) | +-15 / +-15 / +-15 | G: Lauf nick +-7 |
| Hals (Neck gegen Spine1) | +-35 / -45..+50 / +-15 | G: Gang +3..+9 |
| Kopf (Head gegen Neck) | +-30 / +-35 / +-25 | Schuetteln braucht Rollen |
| Kiefer | 0 .. 40 | heutiges Maximum 38; Dingo-Schaedelmodell: kraeftigster Biss bei 25-35 Grad (Quelle 12) |

Dazu zwei Bewegungsregeln (im Skript als "springt"): **Pfotendrehung und Oberarmdrehung hoechstens 20 Grad je Bild**
(Gang/Lauf: unter 20), Pfotenbeugung hoechstens 35 Grad je Bild (Lauf: 34). Pruefung der abgenommenen Clips: Idle, Walk, Run
**0 Befunde**; Maul 0 Befunde.

## 3. Was in den heutigen Clips falsch ist (gemessen, `_arbeit/baer_anim/ref/gelenke_heute.txt`)

**Prankenhieb `NCBear_SwipeL` (R gespiegelt), 1,10 s**

| Befund | Wert | Grenze | Wann |
|---|---|---|---|
| Pfote verdreht (sup) | **-139** (vorher +27: 166 Grad Drehung in 0,3 s), 11 Bilder ausserhalb | -20..+35 | 0,47-0,70 s, am staerksten 0,57 |
| Pfotendrehung je Bild | 49 Grad | 20 | 0,43 s |
| Pfote seitlich abgeknickt (aus) | +33 / -25, 12 Bilder | +-15 | 0,47 / 0,63 |
| Ellbogen zusammengefaltet | **36,4** innen (Haut 7-fach gedehnt) | >= 55 | 0,23 s |
| Oberarm nach innen gedreht | -56 (Ellbogen zur Brust) | >= -35 | 0,30 s |
| Arm seitlich hoch | abd 52,5 | 45 | 0,40 |
| Rest des Koerpers | Becken gier -6..+3, nick +-2, roll +-2, Versatz <= 5 cm; Hinterpfoten 0,000 m Weg, Knie 122..134; Brust gier -18..+8, roll -2..+14 | - | "bewegt den restlichen Koerper null" ist bestaetigt: nur Brust und Kopf |
| Stuetzbein VR | Ellbogen sinkt auf 121 | - | 0,43; wirkt wie Einknicken statt Stuetzen |

Ursache im Skript: `rot_VL` (Weltdrehung) mit Rollen 45..70 und Gieren -55 waehrend der Unterarm hochgeschwungen ist
(`baer_kampf.py` `sp_hieb_l`), Ausholpunkt `("S", (0.26, 0.30, 0.14))` nur 0,42 m von der Schulter, Pol `(-0.6, 0.3, -0.7)`.

**Doppelschlag `NCBear_Slam`, 2,20 s**

| Befund | Wert | Grenze | Wann |
|---|---|---|---|
| Ellbogen zusammengefaltet | **26,6** innen, 14 Bilder unter 55 | >= 55 | 0,67 s (Hochphase) |
| Pfote palmar ueberbeugt | dors -141 | >= -115 | 0,83 |
| Pfote auf dem Kopf | sup **-168**, Sprung 142 Grad in einem Bild | -20..+35 / 20 je Bild | 0,70 / 0,90 |
| Pfote seitlich abgeknickt | aus +-46 | +-15 | 0,83 |

Ursache: `rot_V*` = (0, 10, 0) Weltdrehung in der Luft, waehrend der Rumpf 42 Grad hochgekippt ist; Ziel `("S", (0.30, 0, 0.10))`
nur 0,32 m von der Schulter (= Ellbogen rund 60 oder weniger).

**Aufrichten `NCBear_Rear`, 3,00 s** (Dauer bleibt, nur schoener)

| Befund | Wert | Grenze/Ziel | Wann |
|---|---|---|---|
| Vorderbeine an die Brust gezogen ("Maennchen") | Ellbogen **48-61** ueber 1,5 s | echte Baeren lassen sie haengen: 95-115 | 0,7-2,2 s |
| Pfoten nach innen-oben gedreht | sup bis **66** | <= 35 | 1,0-2,0 |
| Schulter ueberstreckt | vor -94 (Schulterblatt nur -14) | >= -70 | 0,67 |
| Hohlkreuz | Becken welt -52, Brust -80: Lende+Brust 28 Grad nach hinten | Becken mehr drehen, Lende <= 15 | 1,0 |
| tief gehockt | Knie 102-105 | 120-135 | oben |
| Kopf | welt nick bis -46, schuettelt +-6 | gut | |

**Biss `NCBear_Maul`, 1,60 s**: keine Grenzverletzung. Schwach: Brust rollt beim Schuetteln nur +-4 (der Kopf schuettelt
allein), die Vorderbeine knicken auf 96-107 ein statt dass Hals und Kopf tiefer gehen (Hals nutzt nur +15 von +50), keine
Pfote haelt das Opfer.

## 4. Was echte Braunbaeren tun (Zusammenfassung der Quellen)

- **Waffe Nr. 1 ist die Vorderpranke, Nr. 2 der Biss.** Beute wird mit einem oder mehreren Prankenschlaegen auf Nase,
  Kehle oder Ruecken getroffen, groessere Tiere per Biss in Ruecken und Nacken getoetet (Quelle 6); Beute wird
  niedergedrueckt und gleich gefressen, im Kampf zielen Baeren mit den Pranken auf Brust und Schultern und beissen in
  Kopf und Hals (Quelle 7, 10). Der Schlag kommt aus der **Schulter**: sie liefert im Gang die meiste Leistung, das
  Handgelenk faengt Energie ab (Quelle 2); der Buckel ist Muskel (Quelle 7).
- **Das Vorderbein ist eine Saeule mit nach innen gezogenem Ellbogen** (rund 20 Grad aus der Senkrechten), die Pfote
  setzt mit der Aussenkante auf und ist nach innen gedreht (Quelle 1). Daraus: Stuetzbein bleibt fast gestreckt; Pfote
  im Schlag leicht supiniert (Ballen nach innen), nie umgekehrt.
- **Niederdruecken mit beiden Pranken**: Eisbaeren richten sich auf, springen und landen mit den Vorderpranken auf dem
  Schneebau (Quelle 8) - das Vorbild fuer den Doppelschlag; danach wird zugebissen.
- **Aufrichten**: meist zum Schauen/Riechen, auch Drohung vor Kaempfen (Quellen 9, 13); Rangeln im Stehen gibt es,
  **ist aber nicht gewollt** (Kevin).
- **Sitzen**: aufrecht auf dem Hinterteil, Hinterbeine nach vorn, Vorderpfoten zwischen den Beinen bzw. im Schoss;
  beim Fressen kleiner Dinge oft so (Quellen 13, 14). Kevins Vorlage ist die Hauptpose.
- **Fressen am Kadaver**: zuerst Bauch und Brust auf, dann die Muskeln (Quelle 6); die Koerperhaltung beschreibt keine
  Quelle -> Pose unten ist ein Entwurf (Pfote haelt fest, Kopf reisst).
- **Keine Studie gefunden**, die einen Baeren-Prankenhieb, Biss oder das Aufrichten kinematisch misst. Die Phasen unten
  sind aus den Beschreibungen, der Mechanik (Schwerpunkt ueber dem Stuetzdreieck) und den Grenzen abgeleitet.

## 5. Prankenhieb (SwipeL; SwipeR = gespiegelt), 1,10 s, Treffer 0,46 s (bleibt, `hitPc` 0,42)

Prinzip: Gewicht auf Gegenvorderbein und Hinterbeine, Schulter hebt (Buckel), Arm holt aussen-oben aus, der **Rumpf dreht
den Schlag** (Brust 35 Grad gieren statt heute 26, Becken folgt mit 40 %), Arm fast gestreckt im Treffer, Pranke hakt nach
innen-unten durch und setzt **mit Gewicht** vorn auf (Schritt), zurueck. Kopf zielt, weicht im Treffer weg.

| Phase | t (s) | Anteil | Rumpf welt (gier / nick / roll) und Becken-Versatz | Schlagarm VL | Gegenarm VR | Hinterbeine | Kopf, Kiefer |
|---|---|---|---|---|---|---|---|
| A Laden | 0-0,16 | 0-15 % | Becken +3/-2/+3, x -0,05 y -0,05 z -0,02; Lende +6/-4/+6; Brust +10/-8/+12 | Pfote hebt 6 cm; vor 0, abd +5, Dreh -9, innen 135, dors +20, sup +5 | traegt: innen 150-158, Pfote fest | Knie 128, Pfoten fest | Kopf welt gier 0 (zielt), nick +6; Kiefer 6 |
| B Ausholen | 0,16-0,34 | 15-31 % | Becken +5/-4/+4, x -0,07 y -0,06 z -0,03; Lende +9/-6/+8; Brust +12/-10/+14; `klav_L` nick -18 roll +12 | Pfote aussen-oben (Ballen rund 0,15 vor, 0,25 aussen, 0,05-0,15 ueber der Schulter); vor +25..+35, abd +30..+40, Dreh 0..+10, **innen 95-105**, dors -30..-45 (Pfote haengt, Krallen vorn-unten), sup +15..+25, aus <= 10 | innen >= 145 | Knie 122 (geladen) | gier 0, nick +8; Kiefer 16-20, Kopf zieht 3 cm zurueck |
| C Schlag | 0,34-0,46 | 31-42 % | Becken -4/+2/-2, x +0,02 y -0,02; Lende -10/+4/-4; Brust -20/+8/-8; `klav_L` nick 0 roll -5 | zum Ziel (Ballen wie heute rund (1,00, 0,05, 0,55)); vor +45..+55, abd +5..+10, Dreh -10..-20, **innen 145-160 (fast gestreckt)**, dors -10..+5 (Krallen voraus), sup +20..+30, **keine Umkehr der Drehung** | innen >= 145 | Knie 140 (Schub), Pfoten fest | gier -15 (weg vom Schlag), nick +12; Kiefer 22 |
| D Durchzug, Aufsetzen | 0,46-0,66 | 42-60 % | Becken -6/+3/-3, x +0,07; Lende -14/+6/-5; Brust -24/+12/-8 | hakt nach innen-unten, setzt bei 0,62-0,66 auf: rund +0,30 m vor und 0,08 m innen vom Ruheplatz; innen 150-160, dors +45..+55 (flach), sup 0..+10 | innen >= 140 | Knie 145 | gier -10, nick +10; Kiefer 18 |
| E Zurueck | 0,66-1,10 | 60-100 % | alles bis 0,95 in die Grundhaltung | Schritt zurueck: Pfote hebt 8-10 cm, innen 120-130, dors 0..+20, aufsetzen 0,90-0,95 am Ruheplatz | | Knie 134 | Kiefer 0 bis 1,0 |

Pruefwerte im Treffer: Pranke 0,8-0,85 Kacheln vor der Mitte (wie heute, `kampf_anim.md`), damit `NCBearFight.lua` (Hieb 1,4)
nicht geaendert werden muss.

## 6. Biss: liegendes Ziel (Maul, 1,60 s, Treffer 0,544 s) und stehendes Ziel (neu)

**Gegen ein liegendes Ziel (`NCBear_Maul`, Dauer und Treffer bleiben, `hitPc` 0,34)**: Kopf und Hals gehen tief (nicht die
Vorderbeine), eine Pranke drueckt das Opfer nieder, Biss, zwei Schuettler, bei denen die Schultern mitrollen.

| Phase | t (s) | Anteil | Rumpf welt | Vorderbeine | Hals/Kopf (gegen Eltern) | Kiefer |
|---|---|---|---|---|---|---|
| A Senken | 0-0,20 | 0-13 % | Becken nick +2, x +0,03; Brust nick +6 | beide fest, innen >= 130 | Hals +15, Kopf +10 | 4 -> 18 |
| B Vorstoss + Pranke | 0,20-0,46 | 13-29 % | Becken +4, x +0,08; Brust +12 | **VL tritt vor und drueckt** (Ballen +0,25 vor, 0,03 innen, bei 0,40 am Boden, innen 145-155, dors +50..+55); VR fest, innen >= 125 | Hals +30..+40, Kopf +20..+25 (Kopf welt 55-60 runter) | 34 bei 0,46 |
| C Zubeissen | 0,46-0,56 | 29-35 % | Ruck: Brust +14 | VL drueckt (fest) | Kopf +3 cm runter | 34 -> 3 (Treffer 0,544) |
| D Schuetteln 2x | 0,56-1,12 | 35-70 % | **Brust gier +-6, roll +-7**; Becken still | VL fest (haelt) | Hals gier +-12, Kopf gier +-18, roll +-14; 2 Zyklen, je 0,28 s (rund 3,6 Hz, geschaetzt) | 3 |
| E Hoch | 1,12-1,60 | 70-100 % | zurueck | VL Schritt zurueck bis 1,45 | zurueck | 0 |

**Gegen ein stehendes Ziel (neu, Vorschlag `NCBear_Bite`, 1,40 s, Treffer 0,48 s, `hitPc` 0,34)**: Ein Zombie ist bei
Baerengroesse 1,35 rund 1,33 Modellmeter hoch; die Brust des Ziels liegt bei 0,75-1,0 m Modellhoehe (Schnauze heute 0,62).
Darum Vorstoss mit halbem Aufrichten und langem Hals.

| Phase | t (s) | Anteil | Rumpf welt | Beine | Hals/Kopf | Kiefer |
|---|---|---|---|---|---|---|
| A Ansatz | 0-0,18 | 0-13 % | Becken x -0,05; Brust nick +4 (duckt) | Knie 125 (laden) | Hals +10, Kopf +5 | 0 -> 10 |
| B Vorstoss | 0,18-0,48 | 13-34 % | Becken nick -6, x +0,08; Lende -10; Brust nick -18..-22 (vorn hoch) | Hinterknie 125 -> 150 (Schub); beide Vorderpfoten loesen sich kurz (0,22-0,40) und setzen 0,15 m weiter vorn wieder auf, innen 130-150 in der Luft, dors -20..0 | Hals -15..-25 (nach vorn-oben gestreckt), Kopf -5..+5; Schnauze im Treffer 0,85-1,0 m hoch, 0,75-0,85 Kacheln vor der Mitte | 34 bei 0,40-0,46 |
| C Zubeissen + Ruck | 0,48-0,58 | 34-41 % | Brust +8 | Vorderpfoten fest | Kopf ruckt 8-12 cm nach unten-hinten (nick +15) | 34 -> 3 |
| D Schuetteln 2x | 0,58-0,95 | 41-68 % | Brust gier +-6, roll +-6, sinkt auf nick 0 | fest | Hals gier +-12, Kopf gier +-15, roll +-12 | 3 |
| E Zurueck | 0,95-1,40 | 68-100 % | Grundhaltung | Vorderpfoten Schritt zurueck an den Ruheplatz | zurueck | 0 ab 1,10 |

Abwechseln (Hieb L, Hieb R, Biss, Doppelschlag) ist Sache von `NCBearFight.lua`, nicht der Clips.

## 7. Doppelschlag / Niederdruecken (Slam), 2,20 s, Treffer 1,25 s (bleibt, `hitPc` 0,57)

Prinzip nach Quelle 8: halb aufrichten, Vorderbeine **locker vorn-oben** (nicht an die Brust), dann faellt das ganze Gewicht
nach vorn, die Hinterbeine schieben, die Vorderbeine strecken sich und landen **flach** mit fast geraden Ellbogen, federn.

| Phase | t (s) | Anteil | Rumpf welt (nick) | Vorderbeine (beide) | Hinterbeine | Kopf, Kiefer |
|---|---|---|---|---|---|---|
| A Ansatz | 0-0,20 | 0-9 % | Becken +2, Brust +4, Becken x -0,03 | fest | Knie 134 -> 120 | Kiefer 4 |
| B Aufrichten halb | 0,20-0,85 | 9-39 % | Becken -22, Lende -30, Brust -40; Becken x -0,09; `klav` nick -15 | vor +20..+40 (vorn-oben), abd +5..+10, Dreh -10..0, **innen 90-110**, dors -40..-60 (haengt), sup 0..+15 | Knie 105-115, Huefte vor -20, Pfoten fest | Hals +15..+25, Kopf welt -10..0 (sieht das Ziel); Kiefer 20-26 |
| C Niederschlag | 0,85-1,22 | 39-55 % | Becken +4, Lende +8, Brust +14; Becken x +0,07 | strecken: **innen 100 -> 150-160**, vor +40 -> +10, dors -50 -> +45..+55 (flach) **erst kurz vor dem Aufsetzen**, sup -> 0; Aufsetzen 1,22 (Ballen +0,26..+0,30 vor dem Ruheplatz, wie heute) | Knie 110 -> 145 (Schub) | Hals +8, Kopf +6 (Kopf welt +28, schaut runter); Kiefer 26 |
| D Aufprall | 1,22-1,40 | 55-64 % | Brust +17, federt | Ellbogen geben nach 155 -> 130, Pfoten fest | Knie 140 | Kiefer 14 -> 6; Treffer 1,25 |
| E Zurueck | 1,40-2,20 | 64-100 % | -> 0 bis 2,12 | links 1,42-1,62, rechts 1,62-1,82 Schritt zurueck (Hub 7 cm, dors +10..+20 in der Luft) | -> 134 | 0 |

## 8. Aufrichten mit Bruellen (Rear), 3,00 s (Dauer bleibt; Bruellton ab 0,81 s, Maul offen 0,95-1,85 wie heute)

Prinzip: Gewicht nach hinten ueber die Hinterpfoten (Sohlen flach, Fersen am Boden), **das Becken dreht, die Lende bleibt
fast gerade**, Knie leicht gebeugt, Oberkoerper leicht nach vorn geneigt (nicht senkrecht), **Vorderbeine haengen** mit
gebeugtem Ellbogen vor dem Bauch, Pranken baumeln; Kopf hoch und vorn, leichtes Schwanken.

| Phase | t (s) | Anteil | Rumpf welt (nick) | Vorderbeine | Hinterbeine | Kopf, Kiefer |
|---|---|---|---|---|---|---|
| A Ansatz | 0-0,25 | 0-8 % | Becken +2, Brust +4; Becken x -0,04 | entlasten | Knie 134 -> 118 | Kopf hebt (Hals -10) |
| B Hochkommen | 0,25-0,85 | 8-28 % | Becken -55..-60, Lende -65..-70, Brust -72..-78; Becken x -0,10..-0,12 (Schwerpunkt ueber den Hinterpfoten) | Pfoten loesen sich bei 0,30; `klav` nick -20; vor -55..-65, abd +8..+12, Dreh -10..+5, **innen 95-115**, **dors -60..-90 (baumeln)**, sup 0..+15 | Knie 118 -> 125-135, Huefte vor -40..-50, Pfoten und Fersen fest | Hals +25..+35 (Kopf vorn), Kopf welt -30..-40 (hoch) |
| C Oben, Bruellen | 0,85-2,05 | 28-68 % | Schwanken roll +-3, gier +-4, Periode rund 1,2 s | pendeln mit: innen +-8, dors +-10 | fest | Kiefer 36-38 ab 0,95, Kopf gier +-6 im Bruellen |
| D Herunterkommen | 2,05-2,75 | 68-92 % | kippt vor: Brust -> 0 | strecken nach vorn-unten: innen 130-150, dors +20..+45 kurz vor dem Aufsetzen; Aufsetzen 2,70-2,75 rund 0,05-0,10 vor dem Ruheplatz | Knie -> 130 | Kiefer zu ab 2,15 |
| E Federn | 2,75-3,00 | 92-100 % | Grundhaltung | Ellbogen 150 -> 135 -> Ruhe | Ruhe | Ruhe |

Grenzen dabei: Lende+Brust gegen Becken zusammen <= 20 Grad nach hinten (heute 28); Schulter vor >= -70 (Rest ueber das
Schulterblatt und die Rumpfneigung).

## 9. Hinsetzen, Sitzen (Kevins Vorlage), Aufstehen, Fressen

Zeiten: Vanillas Reh hat `DeerStag_IdleToSitting` 2,67 s, `DeerStag_SittingIdle` 5,50 s, `DeerStag_SittingToStanding` 2,40 s,
`DeerStag_IdleEating01` 8,33 s (gemessen aus `media/anims_X/Deer/*.x`, 4800 Ticks/s; die Knoten `buck/idle/idle1.xml`,
`idleSit.xml`, `eating/eating.xml` spielen genau diese Namen). Vorschlag fuer den Baeren: **Hinsetzen 2,2 s, Sitzen-Schleife
5,5 s, Aufstehen 1,6 s** (Kampf hat Vorrang, also flott), **Fressen-Schleife 4,0 s**.

**Sitzpose (Ende von Hinsetzen, Mitte der Schleife)** nach `kevin_sitzvorlage.png`: aufrecht auf dem Hinterteil, Oberkoerper
senkrecht und rund, Vorderbeine gerade zwischen den Hinterbeinen, Pranken flach, Hinterbeine nach vorn und leicht gespreizt,
Sohlen nach vorn/oben, Kopf leicht seitlich.

| Teil | Ziel |
|---|---|
| Becken (`Bip01_Pelvis`) | welt nick -60..-65; tiefster Hautpunkt (Hinterteil/Schwanz) genau 0,000 (Haut messen, nicht schaetzen) |
| Lende / Brust | welt -72..-75 / -80..-85 (gegen Eltern -10..-12 / -8..-10): senkrecht, Bauch vorn |
| Hals / Kopf | Hals gegen Brust +45..+48, Kopf gegen Hals +22..+28 -> Kopf welt -5..-10 (geradeaus, leicht hoch); **Kopf gier +15..+20, rollen +5** (Vorlage: zu seiner linken Seite) |
| Schulterblatt | nick -20 |
| Vorderbeine | vor -55..-65, abd -5..0 (eng; Pfoten bei y +-0,12..0,15 statt +-0,22), Dreh -10..0, **innen 155-168**, dors +60..+72 (flach), sup 0..+10; Pfoten 0,30-0,40 m vor der Hueftlinie zwischen den Hinterbeinen. Reicht das Bein nicht (`bein()` meldet "ueber"), Brust auf -70..-75 neigen statt ueber 170 zu strecken |
| Hinterbeine | vor +5..+15 (Oberschenkel zeigt durch die Beckendrehung nach vorn), **abd +20..+30**, Dreh +5..+10 (Knie nach oben-aussen), Knie innen 130-155, Fuss dors -85..-110 (wie im Stehen), sup +10..+20 (Sohle leicht nach innen, Ballen sichtbar); Fersen 0,55-0,70 m vor und 0,30-0,35 m seitlich der Hueftlinie |
| Kiefer, Schwanz | zu; Schwanz am Boden |
| Sitzen-Schleife 5,5 s | Atmen Brust nick +-1,5 (zwei Zyklen), Kopf schaut langsam um (gier +5 .. +30 .. +5); Pfoten bewegen sich nicht (Gleiten 0) |

**Hinsetzen 2,2 s**

| Phase | t (s) | Anteil | Ablauf |
|---|---|---|---|
| A | 0-0,40 | 0-18 % | Gewicht nach hinten, Hinterknie 134 -> 100, Becken senkt sich 0,15 m, Becken nick -15 |
| B | 0,40-1,30 | 18-59 % | Hinterteil zum Boden: Becken nick -15 -> -55, Kontakt bei rund 1,2 s; Hinterpfoten bleiben stehen, bis es aufsitzt |
| C | 1,30-1,80 | 59-82 % | Hinterbeine nach vorn (links 1,30-1,55, rechts 1,55-1,80, je Schritt mit Hub 5 cm); Oberkoerper richtet sich auf (Brust -40 -> -82); Vorderpfoten ruecken je einen Schritt zwischen die Hinterbeine (1,40-1,60 / 1,60-1,80) |
| D | 1,80-2,20 | 82-100 % | Setzen, leichtes Nachfedern, Kopf dreht zur Seite in die Sitzpose |

**Aufstehen 1,6 s**: 0-0,30 (0-19 %) Hinterpfoten je ein Schritt zurueck unter den Koerper, Oberkoerper nach vorn (Brust -82
-> -45); 0,30-0,90 (19-56 %) Vorderpfoten nach vorn auf den Ruheplatz, Becken hebt (nick -55 -> -10, Knie 100 -> 125);
0,90-1,60 (56-100 %) in die Grundhaltung (Ende = Mittel von `DeerStag_Idle01`, damit die Blende nicht springt).

**Fressen am Boden, Schleife 4,0 s** (stehend; eine Pranke haelt das Futter; liegend waere eine zweite Fassung, Kevins Wahl):

| Phase | t (s) | Anteil | Ablauf |
|---|---|---|---|
| A Kopf runter | 0-0,6 | 0-15 % | Hals gegen Brust +35..+45, Kopf welt 55-65 runter, Brust nick +8, Vorderellbogen 125-140; VL steht auf dem Futter (+0,15 vor, 0,05 innen, dors +55, sup +10) |
| B Zubeissen | 0,6-0,9 | 15-23 % | Kiefer 22 -> 3 bei 0,8 |
| C Reissen | 0,9-1,5 | 23-38 % | Kopf ruckt 10-15 cm hoch-zurueck, gier +-10, Brust nick -4; VL drueckt (Ellbogen 140 -> 155), Pfote bleibt fest |
| D Kauen | 1,5-3,4 | 38-85 % | Kopf halb hoch (welt +20..+30), Kiefer 4-14 Grad mit 2,5 Hz (5 Zyklen), Kopf gier +-5 |
| E Kopf runter | 3,4-4,0 | 85-100 % | zurueck zu A (nahtlos) |

## 10. Hinweise fuer den Animator (aus der Messung)

1. **In der Luft die Pfotendrehung relativ zum Unterarm vorgeben**, nicht als Weltdrehung. Heute ist `rot_*` immer Welt;
   sobald Unterarm oder Rumpf weit gedreht sind, muss das Handgelenk die ganze Differenz schlucken (Hieb -139, Slam -168).
   Am Boden (Stuetze) bleibt Welt richtig (flach aufsetzen). Weg: in Luftphasen das Handgelenk (`ank`) vorgeben und die
   Pfote aus Unterarm + dors/sup bauen, oder `rot_*` je Bild aus der Unterarmrichtung rechnen.
2. **Ausholpunkte mit Abstand**: Schulter-Handgelenk >= 0,41 m (Ellbogen >= 80), im Kampf 0,49-0,62 m (100-150).
3. **Pol des Ellbogens im Rumpfrahmen** (hinten-unten zum Koerper, z. B. Brustdrehung angewandt auf (-1, 0,15 s, -0,3)),
   damit die Oberarm-Drehung zwischen -35 und +20 bleibt; bei nach vorn gehobenem Arm zeigt der Ellbogen nach unten.
4. **Ganzer Koerper**: jede Phase mit Pfotenbewegung bekommt Becken- und Brustwerte (Tabellen oben); Stuetzbein bleibt
   >= 140 gestreckt; Hinterpfoten fest (Gleiten 0), Knie arbeiten (120-150).
5. **Pruefen**: `gelenke_messen.py -- aus.txt baer_kampf_anim.py` (braucht dort weiter den Abschnitt "Netz",
   `KAMPF_CLIPS` mit (Name, Spurfunktion, Dauer, Zeiten), `spuren_bauen`, `kampf_pose`); neue Nicht-Kampf-Clips (Sitzen,
   Fressen) in dieselbe Liste oder das Skript erweitern. Ziel: **0 Befunde** wie heute bei Idle/Walk/Run/Maul.
   Die alten Clips Idle/Walk/Run/Death/Dead werden davon nicht beruehrt (Abweichung 0 misst der Bau mit Probe.java).

## 11. Quellen (gelesen am 08.11.2026; nichts heruntergeladen)

1. https://sicb.org/?p=22207 - SICB-Kurzfassung zur Vorderbein-Kinematik gehender Grizzlys: Ellbogen in der Stuetze rund 20 Grad nach innen, Pfote setzt mit der Aussenkante (rund 34 Grad) auf, Vorderpfote rund 68 Grad nach innen gedreht, ungewoehnliche Handgelenkdrehung.
2. https://sicb.org/?p=15953 - SICB-Kurzfassung zur Gelenkbelastung: die Schulter leistet die meiste Arbeit, das Handgelenk nimmt Energie auf, der Ellbogen wenig.
3. https://pure.hartpury.ac.uk/en/publications/grizzly-bear-ursus-arctos-horribilis-locomotion-forelimb-joint-me/ - Shine et al. 2017, J Exp Biol 220:1322-1329, Vorderbein als Strebe in der Frontalebene (nur Eintrag/Zusammenfassung gelesen, Volltext-PDF war nicht lesbar).
4. https://pmc.ncbi.nlm.nih.gov/articles/PMC6923198/ - Goniometrie an Franzoesischen Bulldoggen (Front. Vet. Sci. 2019): Beuge- und Streckwinkel von Schulter, Ellbogen, Karpus, Huefte, Knie, Tarsus; Hund als Raubtier-Vergleich.
5. https://pubmed.ncbi.nlm.nih.gov/34162775/ - CT-Studie zur Unterarmdrehung bei Baeren: adulte Braun- und Eisbaeren drehen weniger als Kragenbaeren (nur Suchzusammenfassung, Seite verlangte Cookies).
6. https://www.kora.ch/en/species/bear/signs-in-the-field - KORA: Braunbaeren toeten mit Prankenschlaegen auf Nase, Kehle, Ruecken, groessere Tiere per Biss in Ruecken/Nacken, fressen zuerst Bauch und Brust.
7. https://en.wikipedia.org/wiki/Brown_bear - Beute wird niedergedrueckt und gleich gefressen, Prankenschlag kann Genick oder Ruecken brechen, Kampf mit Schlaegen auf Brust/Schulter und Bissen in Kopf/Hals, Buckel ganz aus Muskeln.
8. https://www.fws.gov/story/2022-01/polar-bear-year-summer - US Fish and Wildlife: Eisbaerin duckt sich, setzt sich auf die Hinterbacken, springt und landet mit den Vorderpranken auf dem Robbenbau.
9. https://www.livescience.com/animals/bears/watch-as-2-male-alaskan-grizzly-bears-fight-in-an-epic-battle - Grizzlykampf: erst Drohen auf vier Beinen, dann aufgerichtet ringend.
10. https://www.ksl.com/article/50615919 - Wildtierfuehrer: Baeren kaempfen von Angesicht zu Angesicht mit den Zaehnen und zielen auf Kopf und Hals.
11. https://conference.bearbiology.org/workshops/ps06-bear-jaws-and-claws-a-biomechanical-breakdown/ - IBA-Workshop: Eisbaer-Biss- und Krallenkraft, Maulweite begrenzt.
12. https://researchers.une.edu.au/en/publications/effects-of-gape-and-tooth-position-on-bite-force-and-skull-stress-5/ - Dingo-Schaedelmodell: Maulwinkel 5-65 Grad untersucht, guenstigster Biss bei 25-35 Grad (nur Suchzusammenfassung).
13. https://lenz.io/c/bears-sitting-on-chairs-behavior-2d8837e6 - Faktencheck mit Verweis auf WDFW: Baeren sitzen beim Fressen oder Beobachten auf den Hinterbacken (schwache Quelle).
14. https://www.animalsaroundtheglobe.com/?p=345184 - Sitzen mit nach vorn gestreckten Hinterbeinen und Vorderpfoten im Schoss (Blog, schwache Quelle).
15. https://pubs.usgs.gov/publication/70169366 - USGS: Grizzlys jagen Wapitikaelber durch Suchen und Hetzen; die Toetungsbewegung beschreibt die Kurzfassung nicht.
16. Vanilla, lokal: `media/anims_X/Deer/DeerStag_{IdleToSitting,SittingIdle,SittingToStanding,IdleEating01}.x` (Dauern) und `media/AnimSets/buck/{idle/idle1,idle/idleSit,eating/eating}.xml` (Knoten).

## 12. Unsicher

- Gelenkgrenzen fuer Ellbogen, Handgelenk und Schulter sind aus Hund + abgenommenem Gang abgeleitet, nicht am Baeren gemessen.
- Schuettel-Frequenz (rund 3,6 Hz), Kauen 2,5 Hz und alle Phasen-Anteile sind Entwurf aus den Beschreibungen, nicht gemessen.
- Ob die Sitzpose ohne Durchdringen des Bodens und ohne Hautriss erreichbar ist, entscheidet erst die Hautmessung beim Bau
  (Becken -60..-65 dreht stark, `kampf_spez.md` 5.5 nennt Bauch und Hueften als Rissstellen).
- Ein Kopfschuetteln ohne Gegenbewegung der Schultern sieht vermutlich steif aus; wie viel Brust-Rollen schoen ist, sieht man
  nur im Bild.

Statisch geprueft und offline gemessen, nicht gespielt.
