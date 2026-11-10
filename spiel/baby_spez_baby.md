# SPEZ_BABY -- Lauf baer-baby: Entwurf des Baer-Jungen (Spezifikation)

Stand 10.11.2026 nachts. Alles **statisch/offline** gemessen und gerendert, **nicht gespielt**. Nichts in NCBearTest, NPC Crew oder
Lauf 2c geschrieben; nichts committet. Grundlage Erwachsener: NCBearTest `NCBear.glb` MD5 `5066fa6774f32b52df558e9878c48610`, gelesen ueber
den Dump des Spiel-Importers `_arbeit/baer_pfote/fix1/bau4/dump_final.txt(.pkl)` (Kette `fix1/log/kette13.txt:13-14` belegt dieselbe MD5).
Vorlage `baer/begleiter/kevin_babygesicht_vorlage.webp` (525 x 903 px) nur angesehen und vermessen; **kein Pixel, keine Kontur, keine
Farbflaeche** daraus wird in Modell oder Textur verwendet. Blaetter mit der Vorlage (`vergleich_ton_foto.png`, `referenz/r_*.png`) bleiben
hier und werden nie weitergegeben. Die Skizze `skizze_baby.png` ist nur aus Zahlen gezeichnet (keine Vorlagen-Pixel).

Einheit **W** = Kopfbreite ueber das Wangenfell in Augenhoehe, ohne Ohren. Alle Kopfmasse sind Vielfache von W.

---

## 0. Kurzfassung (alles, was der Bauer braucht)

1. **Was am Foto anders ist als heute:** nicht die Breiten (Augenabstand 0,30 W, Nase 0,17 W, Schnauze 0,33 W sind beim Erwachsenen schon
   fast gleich), sondern **Hoehe und Tiefe**: gewoelbte Stirn (Krone **+0,34 W** ueber dem Auge statt +0,20), Ohren **hoch und weit vorn**
   (Mitte 0,26 W ueber / 0,32 W hinter dem Auge statt 0,08 / 0,51), **kurze Schnauze** (Nasenspitze 0,27 W vor dem Auge statt 0,39),
   **flacher Unterkiefer** (Kinn 0,34 W unter dem Auge statt 0,46), **runde Augen** (Oeffnung 0,056 x 0,043 W statt Schlitz 0,061 x 0,020).
2. **Foto-Kamera:** das Foto schaut ~**30 Grad ueber der Kopfachse** auf das Gesicht (Herleitung 1.4). In dieser Kamera muss der Ton-Kopf
   die Fotomasse treffen: Umriss oben +0,46, Ohr oben +0,50, Ohrmitte +0,38, Nasenmitte -0,25, Kinn -0,36 (in W zur Augenlinie), W/H 1,20.
3. **Weg ins Spiel (empfohlen): eigenes GLB `NCBearCub.glb`** mit denselben 26 Knochennamen, eigenen (kuerzeren) Knochen, eigenem Kopfnetz
   und eigener Textur, eigener Tierart `bearcub` (Stufe -> `bear`), `animset = "buck"`, die **15 Clips per Skript kopiert**: Drehungen
   bit-gleich, nur die Lage-Schluessel neu. Knochen-Skalierung im selben GLB geht **nicht** (3.3: die Engine setzt jede Knochenlage aus dem
   Clip und ignoriert Skalier-Schluessel). Das ist auch Vanillas Weg (Kitz, Kalb, Ferkel, Lamm, Kueken: eigenes Netz je Jungtier, 3.1).
4. **Koerper:** L (Nase bis Rumpfende) = 1,90 m bei Groesse 1,0 (= 66,5 cm bei 0,35); W = 0,34 L; Kopflaenge 0,90 W; Ruecken 0,54 L; Bauch
   0,11 L ueber Boden; Rumpf rund (Breite/Hoehe 1,0, Breite 0,42 L); Kopf oben auf dem Koerper, **kein Kragen** (Stufe im Umriss <= 0,01 L).
5. **Technik:** 26 Knochen wie der Erwachsene (Namen, Eltern, Reihenfolge), <= 20.000 Dreiecke (Vorschlag Kopf 3.000-4.500), <= 4 Einfluesse,
   Summe 1, ein Netz/Material, Body-Textur 1024 x 1024 RGB (Kopf >= 30 % der UV-Flaeche). Nase-Glanz und Augen-Glanzpunkt **gemalt** (der
   Tier-Shader kennt keinen Glanz).
6. **Farben (Zielwerte sRGB, belichtete Seite):** Fell Gesicht (80,63,57) mit Spitzen (126,108,101)..(163,136,124), Grund (41,23,18); Wange
   (88,60,42); Augenring (53,40,36); ueber dem Auge (73,54,46); Schnauze (155,131,118)/(158,125,103), Lichter (190,160,140); Nase (23,19,20)
   mit Oberkante (98,95,100); Iris (30,25,25); Ohr-Mulde (19,9,6), Ohrrand (146,113,93), Haarbueschel innen (99,72,58); Krallen (126,122,129).

---

## 1. Foto vermessen

### 1.1 Wie

- Ausschnitte mit Pixelraster (nur Ablesen): `referenz/r_gesamt.png`, `r_augen.png`, `r_schnauze.png`, `r_links.png`, `r_ohr_l.png`,
  `r_ohr_r.png` (Werkzeug `werkzeug/raster.py`). Umriss je Zeile aus Helligkeit/Farbe (Hintergrund grau, Baer braun, Gauss 2 px).
- Schaerfe je Hoehe (mittlerer |Laplace|): Stirn y 410-455 am schaerfsten (34-39), Ohren 9-11, der Buckel ueber dem Kopf y 245-290 nur 3-3,4
  -> **der Buckel ist der Ruecken hinter dem Kopf**, nicht die Schaedeldecke. Krone daher bei y ~295 (+-10).
- Licht von links: rechte Gesichtshaelfte im Schatten (Schnauze rechts L 82 statt 132). Farbwerte deshalb von der belichteten Seite.
- Farben: `werkzeug/farben.py` -> `referenz/farben.json` (Median, 10/90-Perzentil, hellste/dunkelste 10 % je Zone).

### 1.2 Masse (Foto-Pixel, W = 490 px)

| Mass | Pixel (Foto) | in W | Bemerkung |
|---|---|---|---|
| Kopfbreite W (Wangenfell, y 500) | x 18..508 = 490 | 1 | +-15 px; tiefer gehen Wangen in die Vorderbeine ueber |
| Breite an der Ohrbasis (Kerbe, y 390) | x 34..477 = 443 | 0,90 | |
| Krone (Umriss oben, zw. den Ohren) | y 295 | +0,457 ueber Auge | geschaetzt +-10 px (Schaerfe 1.1) |
| Kinn (unter dem Mund, verdeckt) | y ~705 | -0,37 | geschaetzt +-15 px |
| Kopfhoehe H (Krone-Kinn) | 410 | W/H = **1,195** (+-0,06) | "breiter als lang" |
| Augenlinie | y 519 | 0 | Mitten (185,5/519,5) und (334/518,5) |
| Augenabstand (Mitte-Mitte) | 148,5 | **0,303** | |
| Augenoeffnung | 28 x 21 (links 29 x 21, rechts 26 x 21) | **0,056 x 0,043** | h/b 0,75 = rund, Glanzpunkt oben |
| Auge unter Krone / H | 224 / 410 | 0,546 | |
| Ohr links | x 25..135, y 277..395, Mitte (80/336) | D 0,23-0,24 | |
| Ohr rechts | x 360..488, y 272..398, Mitte (424/335) | D 0,26 | Kopf leicht gedreht |
| Ohr-Durchmesser (Mittel) | ~120 (+-8) | **0,245** | runde Scheibe, Mulde sichtbar (zeigt nach vorn) |
| Ohrmitten-Abstand | 344 | **0,70** | |
| Ohren aussen | x 25..488 = 463 | **0,945** | Ohren fast so breit wie W |
| Ohrmitte ueber Augenlinie | 183 | **+0,373** | |
| Ohr oben ueber Augenlinie / ueber Krone | 245 / 21 | +0,50 / +0,043 | |
| Nase Breite x Hoehe | x 220..300, y 611..672 | **0,163 x 0,124** | Hoehe = Vorderflaeche + sichtbare Oberkante |
| Nasenmitte unter Augenlinie | 122 | **-0,249** | |
| Schnauze hell, Breite an der Nase (y 600-620) | ~160 (x 180..340) | **0,33** | geometrische Breite verdeckt; helle Zone |
| Schnauze hell, Breite y 560 / y 540 | 115 / 80 | 0,235 / 0,16 | verjuengt sich nach oben |
| Oberkante der hellen Zone (Stirnabsatz) | y ~530 (L 82 -> 155 in 20 px) | -0,02 | scharfer Helligkeitssprung = Absatz |
| sichtbarer Nasenruecken (Absatz bis Nase oben) | 81 | 0,165 | gibt mit der Nase die Kamera (1.4) |

### 1.3 Farbtoene (Zielwerte, sRGB 0-255, belichtete Seite; Quelle `referenz/farben.json`)

| Zone | Median | hellste 10 % | dunkelste 10 % |
|---|---|---|---|
| Schnauze oben (ueber der Nase) | (155,131,118) | (189,163,148) | (114,94,87) |
| Schnauze seitlich an der Nase | (158,125,103) | (193,156,131) | (124,94,75) |
| Nasenruecken zwischen den Augen | (150,123,112) | (193,165,153) | (96,74,66) |
| Stirn / Gesicht (dunkler) | (80,63,57) | (126,108,101) | (41,23,18) |
| Stirn oben | (104,82,72) | (163,136,124) | (61,41,32) |
| Wange (belichtet) | (88,60,42) | (149,109,86) | (37,16,6) |
| Augenring (Ring r 0,033-0,057 W) | (53,40,36) | (99,80,73) | (19,11,7) |
| ueber dem Auge ("Hauch heller") | (73,54,46) | (125,103,93) | (21,12,8) |
| Auge (Iris/Pupille) | (30,25,25) | (55,51,54) | -- ; Glanzpunkt weiss-blaeulich ~(225,230,240) |
| Nase | (23,19,20) | (74,72,80) | (5,1,1) |
| Nase Oberkante (Glanz) | (98,95,100) | (137,129,127) | -- |
| Ohr: Rand (Gegenlicht) | (146,113,93) | (225,203,187) | (66,42,28) |
| Ohr: Mulde innen | (19,9,6) | (58,40,31) | -- |
| Ohr: Haarbueschel unten innen | (64,40,26) | (99,72,58) | (14,7,4) |
| Prankenfell | (79,58,50) | (134,112,103) | (33,18,14) |
| Krallen (hell) | -- | (126,122,129) | (10,4,1) |

**Widerspruch, offen benannt:** ENTSCHEIDUNGEN.md sagt "Ohren innen etwas heller". Gemessen ist die Mulde selbst sehr dunkel (Schatten);
heller sind die **Haare am inneren Rand** und unten in der Mulde. Soll (4.3): dunkle Mulde, helle Haarbueschel am Innenrand.
**Fell gesprenkelt:** Grund (41..80, 23..63, 18..57), Spitzen (126..163, 108..136, 101..124), Anteil heller Spitzen ~10-15 %.

### 1.4 Kamera des Fotos und Stirnabsatz (Schaetzung, mit Herleitung)

- Aus einem Frontfoto lassen sich Laengen entlang der Blickrichtung (Schnauzenlaenge, Stirnwinkel) **nicht direkt** messen.
- Bildhoehe eines Punktes bei Kamera p Grad ueber der Kopfachse: v = z cos p - x sin p (x vorn, z oben, Ursprung Augenmitte).
- Drei unabhaengige Fotowerte passen zusammen nur bei **p = 30 Grad (+-10)**:
  - sichtbarer Nasenruecken 0,165 W;
  - Nasenmitte -0,249 W;
  - Nasenhoehe 0,124 W (Vorderflaeche plus Oberkante sichtbar).
- Probe mit dem Soll-Kopf (4.1): Absatz v = -0,037, Nase oben v = -0,197 (Foto -0,02 / -0,19), Nasenmitte -0,254 (Foto -0,249),
  Umriss oben 0,47 (0,457), Ohr oben 0,49 (0,50), Kinn -0,354 (~-0,37), W/H 1,21 (1,195).
- Plausibel: Kinn liegt auf dem Boden, Kopf nach unten geneigt, Kamera knapp darueber.
- **Stirnabsatz:** nicht als Winkel messbar. Belege im Foto:
  - harter Helligkeitssprung an der Oberkante der Schnauze (L 82 -> 155 in 0,04 W);
  - die Stirn nimmt in der 30-Grad-Ansicht 0,46 W ueber dem Auge ein.
- Daraus Soll:
  - Nasenruecken faellt 22 Grad (+-8) zur Kopfachse;
  - Stirn steigt am Absatz >= 60 Grad;
  - Krone 0,34 W ueber dem Auge.
- **Ungeprueft:** keine echten Seitenfotos angesehen (Internet nicht benutzt). Die Seite pruefen Kevins Augen am Bild R3.

### 1.5 Skizze

`skizze_baby.png`: links vorn in der Foto-Kamera mit allen Massen, rechts die Seite. Grau gestrichelt der Erwachsene heute (Profil
aus dem GLB, gleiche W). Gezeichnet nur aus `werkzeug/ziel_kopf.json` (Werkzeug `werkzeug/skizze.py`). Angesehen: die Proportionen lesen
sich als Junges; die Seitenansicht ist eine Formskizze, kein Fellbild.

---

## 2. Heute: Erwachsener und das Junge aus baer-fell mit denselben Zahlen

Werkzeug `werkzeug/mess_kopf.py` -> `mess/kopf_mass.json`:

- Kopfpunkte = Gewicht Head+Jaw >= 0,5 (1.532 Punkte, 2.465 Dreiecke).
- Kopf-Rahmen HA/HB/HC und Spielnetz = (Hochmodell - (x0,0,zmin)) x 0,75, aus `baer/spiel/baer_quelle_pfote.py:31-63` und
  `baer_kampf_pfote.py:108-121`.
- Auge/Ohr/Nase aus den Quell-Konstanten `baer_quelle_pfote.py:163-215, 339-340`, im GLB gegengeprueft: naechster Netzpunkt Augenhoehle
  0,0075, Ohr 0,018, Nasenspitze 0,020 Kopfeinheiten.
- Junges baer-fell = dieselbe Knochen-Skalierung wie `_arbeit/baer_fell/baby/auftrag.json` auf die Ruhehaltung.
- Umrisse: `mess/umriss_*.png`.

| Mass (in W) | Foto | Erwachsener heute | Junges baer-fell | Soll Junges |
|---|---|---|---|---|
| **Foto-Kamera 30 Grad:** Umriss oben ueber Auge | 0,457 | 0,552 | 0,431 | 0,46 +-0,04 |
| Ohrmitte ueber Auge | 0,373 | 0,327 | 0,274 | 0,38 +-0,04 |
| Nasenmitte unter Auge | 0,249 | 0,271 | 0,236 | 0,25 +-0,03 |
| Kinn unter Auge | ~0,37 | 0,490 | 0,465 | 0,36 +-0,05 |
| W / H | 1,195 | 0,96 | 1,12 | 1,20 +-0,08 |
| **Breiten (jede Kamera):** Augenabstand | 0,303 | 0,299 | 0,308 | 0,30 +-0,02 |
| Augenoeffnung b x h | 0,056 x 0,043 | 0,061 x 0,020 | 0,063 x 0,021 | 0,056 x 0,043 (+-0,008 / +-0,006) |
| Nase b | 0,163 | 0,172 | 0,177 | 0,165 +-0,015 |
| Schnauze an der Nase | 0,33 | 0,337 | 0,339 | 0,33 +-0,03 |
| Ohr-Durchmesser | 0,245 | 0,272 | 0,280 | 0,245 +-0,025 |
| Ohrmitten-Abstand | 0,70 | 0,598 | 0,616 | 0,70 +-0,04 |
| Ohren aussen | 0,945 | 0,816 | 0,840 | 0,93 +-0,04 |
| **3D, Kopf-Rahmen:** Krone ueber Auge | -- | 0,200 | 0,207 | 0,34 +-0,04 |
| Krone hinter Auge | -- | 0,665 | 0,428 | 0,30 +-0,07 |
| Ohrmitte ueber / hinter Auge | -- | 0,081 / 0,513 | 0,084 / 0,402 | 0,26 / 0,32 (+-0,04 / +-0,05) |
| Nasenspitze vor Auge | -- | 0,395 | 0,309 | 0,27 +-0,03 |
| Nasenmitte unter Auge | -- | 0,108 | 0,112 | 0,155 +-0,03 |
| Kinn unter Auge | -- | 0,457 | 0,468 | 0,34 +-0,04 |
| Kopflaenge (Nase bis Hinterkopf in Ohrhoehe) | -- | 1,158 | 0,881 | 0,90 +-0,06 |
| Nasenruecken-Neigung | -- | -3,7 Grad | -5,2 Grad | -22 +-8 Grad |
| Stirn-Neigung um die Augenlinie | -- | -56 Grad (Stufe, danach flacher Schaedel) | -63 Grad | >= 60 Grad, dann Kuppel |

W absolut: Erwachsener 0,4345 m, baer-fell 0,611 m (Groesse 1,0).
Hinweis: W des Erwachsenen enthaelt Wangen-/Kragenfell, das am Kopf haengt; im Ton-Bild wirkt das Gesicht rund 10 % schmaler.

**Ton-Bild neben dem Foto:** `vergleich_ton_foto.png` (nur hier).

- Oben: Foto | Erwachsener | baer-fell-Junges in der Foto-Kamera, gleiche W, gleiche Augenlinie, rote Linien = Fotomasse.
- Unten: beide Seiten, dazu der Erwachsene genau entlang der Kopfachse.
- Gerendert auf der RTX 4090/OptiX, 16 Samples, 480 px. Werkzeug `werkzeug/ton_kopf.py` ueber `werkzeug/gpu_render.sh`;
  Einzelbilder `ton/*.png`.

Angesehen:

1. Beide Ton-Koepfe haben dasselbe **Erwachsenen-Gesicht**: lange, kastenfoermige Schnauze mit flacher Stirnseite, Augen nur
   Striche, kleine Ohren hinten auf einem flachen Schaedel.
2. Das baer-fell-Junge ist nur ein groesserer Erwachsenenkopf: kein eigenes Gesicht (bestaetigt Kevins Satz).
3. **Kragen:** von der Seite und von 3/4 steht beim baer-fell-Jungen der Rand der Rumpf-Fellhuelle als Manschette um Hals und Hinterkopf
   (`ton/jung_seite.png`, `ton/jung_dreiviertel.png`). Beim Erwachsenen ist er flacher, aber da (`ton/erw_vorn00.png`: Ring ums Gesicht).
4. In der Foto-Kamera liegt beim Erwachsenen der flache lange Schaedel hoch im Bild: Umriss 0,55 statt 0,46, Kinn 0,49 statt 0,37.
   Das Foto-Gesicht ist also nicht "hoeher", sondern **kuerzer und gewoelbter**.

---

## 3. Weg ins Spiel

### 3.1 Wie Vanilla B42 Jungtiere macht (statisch belegt)

| Tier | Jungtier-Art | eigenes Modell | eigene Clips (animationsMesh) | eigenes animset | Stufe -> | Datei:Zeile |
|---|---|---|---|---|---|---|
| Reh | `fawn` | `DeerFawn` | `Deer_Fawn` (Skinned/DeerFawn, Praefix `DeerFawn_`) | `fawn` | doe / buck nach 60 Tagen | DeerDefinitions.lua:7-11, 58-92; models_animals.txt:232-238; animations_meshes.txt:30-35 |
| Rind | `cowcalf` | `CowCalf_Body` | `Cow_Calf` | `cowcalf` | cow / bull nach 180 | CowDefinitions.lua:8-11, 121-138; models_animals.txt:134-146; animations_meshes.txt:74-79 |
| Schwein | `piglet` | `FarmPig_PigletBody` | `Pig_Piglet` | `piglet` | sow / boar nach 140 | PigDefinitions.lua:8-11, 91-106; models_animals.txt:162-172; animations_meshes.txt:88-93 |
| Schaf | `lamb` | `Sheep_Lamb` | `Sheep_Lamb` | `lamb` | ewe / ram | SheepDefinitions.lua:9, 146-151; models_animals.txt:368; animations_meshes.txt:115 |
| Huhn | `chick` | `Chicken_Chick` | `Chicken_Chick` | `chick` | hen / cockerel nach 126 | ChickenDefinitions.lua:8-10, 81-96; animations_meshes.txt:53-58 |
| Kaninchen | `rabkitten` | `RabKitten_Body` | `Rabbit_Kitten` | `rabkitten` | rabdoe / rabbuck | RabbitDefinitions.lua:8-10, 111-126; models_animals.txt:442 |
| **Maus** | `mousepups` | **dasselbe** `Mouse_Body` | `Mouse` | `mouse` | nur kleiner (0,4-0,7 statt 0,7-1,0) | MouseDefinitions.lua:87-99, 137-147 |

- **Regel:** jedes groessere Vanilla-Jungtier ist eine **eigene Tierart mit eigenem Netz und eigenem animationsMesh**.
- Nur die Maus waechst allein ueber die Groesse.
- Die Jungtier-Textur kommt aus `breed.textureBaby`, solange die Stufe ein `nextStage` hat (`IsoAnimal.initTexture`,
  `_arbeit/baer_spiel/dec/IsoAnimal.java:1525-1537`; z. B. DeerDefinitions.lua:43).
- `bodyModelSkel` ist das Skelett-Modell der verwesten Leiche, nicht das Animationsskelett: `initTexture` nimmt `textureSkeleton` bei
  `shouldBeSkeleton`, dec:1526-1527. Die Angabe "eigenes Skelett Deer_FawnSkeleton" im baer-fell-Bericht ist damit zu korrigieren.

### 3.2 Wachsen (Jar 42.21 von heute, javap `_arbeit/baer_baby/jar/*.javap.txt`; Lesehilfe Vineflower `_arbeit/baer_spiel/dec/`)

- **Groesse in der Stufe:** taeglich `size += (maxSize - minSize) / ageToGrow * health` (`AnimalData.growUp`, dec:218-234). Start
  `initSize` (dec:1355-1358). `setSize` klemmt auf [min, max] (javap `AnimalData.setSize` Offset 2-9).
- **Stufenwechsel:** `AnimalData.checkStages` (dec:120-133). Bei `daysSurvived >= ageToGrow` laeuft `grow(nextStage | nextStageMale)`.
  `grow` (javap `AnimalData.grow`) baut ein **neues IsoAnimal** (Offset 58/92) und uebernimmt:
  - Alter, Spieler-/Baum-Leine, Hunger, Durst, `playerAcceptanceList`, Stress, Genom;
  - Name (`setCustomName` 268), Geschlecht, Fahrzeug, **AnimalID** (`setAnimalID` 304).
  
  Danach `delete` des alten Tiers und `addToWorld` (540/545); im MP `AnimalInstanceManager.add` (dec:1435).
- **Nicht uebernommen: modData.** In `grow` gibt es keinen `getModData`-Aufruf.
- -> **Naht fuer B1:** Besitzer, Zaehm-Balken, Inventar und Level des Baeren muessen beim Wechsel ueber die gleiche AnimalID
  weitergereicht werden.
- **Groessensprung:** ist das Junge beim Wechsel ueber 70 % seiner Spanne, setzt `grow` die neue Groesse auf `neu x (1 + delta - 0,7)`
  (javap Offset 340-392). Wohlgenaehrt (delta 1) heisst das **+30 %**.
  - Beispiel: Junges endet bei 0,75, der Erwachsene startet bei minSize 0,75 x 1,3 = 0,975.
  - Ausgleich in B1: Erwachsenen-`minSize` = Jungen-`maxSize` / 1,3 (z. B. 0,58) oder bewusst hinnehmen.
- **`isBaby()` = Stufe hat `nextStage`** (dec:1779-1781). Es loest Vanilla-Jungtier-Verhalten aus (Mutter suchen/saugen
  BaseAnimalBehavior dec:1049, 1209; Zwerg-Groesse AnimalData dec:1727, 1745). **In B1 pruefen**, was davon beim Baeren greift.
- **Bewegung kennt die Groesse nicht:** `IsoGameCharacter.doDeferredMovement` (dec:1572-1640) liest keine Groesse; vgl.
  `baer/spiel/tier_spez.md:187` ("Das Bild folgt, der Weg nicht").
  - Folge: ein Junges bei 0,35 mit Erwachsenen-Weg gleitet um Faktor ~1/0,35.
  - Der Weg steht nur in `Translation_Data` (tier_spez.md:26, :229).
  - Siehe 3.3, Punkt 4.

### 3.3 Clips bei kuerzeren Knochen (belegt)

**1. Die Engine setzt jede Knochenlage aus dem Clip.** Javap `AnimationPlayer.updateBoneAnimationTransform_Internal`:

- `Keyframe.setIdentity` (Offset 68), dann `getTrackTransform` (202) -> `AnimationTrack.get`.
- Danach wird `key.position`/`key.rotation` aus dem Clip genommen (434-503), am Ende `boneTransforms[i].set(position, rotation, scale)` (622).
- `key.scale` wird nur im Rest-Gewicht-Zweig mit dem alten Wert gemischt (585-597).
- -> **Skalier-Schluessel der Clips wirken nicht**; Knochenlaengen kommen aus den Lage-Schluesseln.
- *Berichtigung fix1 (Pruefer-Befund 'Beleg ungenau'):* `getTrackTransform` (202) liefert auch `scale`, und `boneTransforms.set(position,
  rotation, scale)` (622) setzt es. Genauer: Skalier-Schluessel WUERDEN wirken, sind in allen 15 Clips aber 1,0 (Punkt 2) -- die
  Knochenlaenge kommt deshalb aus den Lage-Schluesseln. Die Folgerung (eigenes GLB mit eigenen Lage-Schluesseln) bleibt.

**2. Die 15 Clips des Erwachsenen tragen Lage-Schluessel fuer alle 26 Knochen** (`werkzeug/clip_schluessel.py` auf dem Dump):

- **ueber alle Clips und Bilder konstant** (Spannweite 0,00000 Einheiten) = reine Knochenlaengen;
- Ausnahme `Bip01_Pelvis` (Spannweite 0,232: Rumpf hebt/senkt sich, SitDown/StandUp 0,181 hoch);
- Ausnahme `Translation_Data` (Weg: Walk 0,378 E je 0,9 s, Run 1,058 E je 0,533 s);
- Skalier-Schluessel alle 1,0.

Konstante Werte (Modelleinheiten, 0,544 je Meter):

| Knochen | Lage-Schluessel |
|---|---|
| Bip01 | z 0,3917 (Hueft-Hoehe 0,72 m) |
| Thigh | (+-0,136 / -0,050 / -0,012) |
| Calf | 0,1638 |
| Foot | 0,1831 |
| Toe0 | 0,1287 |
| Spine | 0,1694 |
| Spine1 | 0,1655 |
| Clavicle | (+-0,054 / 0,033 / -0,065) |
| UpperArm | 0,1284 |
| Forearm | 0,172 |
| Hand | 0,1757 |
| Neck | 0,1414 |
| Head | 0,1172 |
| Jaw | (0 / 0,0653 / -0,0248) |
| Tail | -0,1797 |

**3. Folgerung:**

- **(a) Knochen-Skalierung im selben GLB geht nicht:** die Clips ziehen jede Lage zurueck, Skalierung wird ignoriert.
- **(b) Ein eigenes GLB mit kuerzeren Knochen und unveraenderten Clips geht auch nicht:** die Gelenke saessen auf Erwachsenen-Abstand,
  das Netz wuerde gedehnt.
- **(c) Eigene Kopien der 15 Clips im Jungen-GLB sind noetig und leicht:**
  - je Knochen den konstanten Lage-Schluessel durch die Jungen-Lage ersetzen;
  - `Bip01`-Hoehe und die Pelvis-Bewegung mit dem Hueft-Faktor skalieren;
  - Drehungen bit-gleich lassen. Reine Skriptarbeit, keine Handanimation.
- Gleich gewirkt hat schon `baby_vergleich.py welt_junges` (Kind-Lage im Elternraum skaliert). Dort fehlte nur die Bip01-/Pelvis-Hoehe,
  die per "min z = 0" je Objekt ersetzt wurde.

**4. Boden und Weg (B1):**

- **Boden:** bei ungleichen Faktoren (Beine 0,64, Rumpf 0,8) bleiben die Pfoten nicht von selbst am Boden, vor allem in Sit/Rear.
  Abhilfe: je Bild eine Pelvis-z-Korrektur, so dass die tiefste Stuetzpfote dieselbe Bodenhoehe hat wie beim Erwachsenen.
  Pruefwert: <= 1,5 cm bei Groesse 1,0.
- **Weg:** `Translation_Data` mal Hinterbein-Faktor, sonst gleiten die kurzen Beine. Weil der Weg die Groesse nicht kennt (3.2), gilt
  zusaetzlich: bei 0,35 ist jeder Weg ~2,9x zu lang fuer das Bild.
- Vorschlag fuer B1, Kevins Wort noetig:
  - Weg x Bein-Faktor x 0,5 (Mitte des Wachsens);
  - zum Ausgleich kuerzere Clip-Dauer: das Junge trippelt schneller, damit es dem Spieler folgen kann.
- **Ungeprueft:** ob `buck` Laufen/Rennen beim Folgen ueberhaupt drosselt.

**5. Gleiche Clip-Namen in zwei Netzen gehen:**

- Clips sucht die Engine je Netz: javap `AnimationPlayer.play(String,..)` Offset 98-105 = `skinningData.animationClips.get(name)`;
  ebenso tier_spez.md:16.
- `NCBearCub.glb` darf also wieder `DeerStag_Idle01`, `NCBear_Sit` usw. tragen.
- `animset = "buck"` bleibt (kein Angriffszustand, passt zu "Jungtier kaempft nie").
- Die `NCBear_*`-XMLs in `AnimSets/buck/idle/` gelten fuer beide.
- Die 15 Clips: DeerStag_Idle01 3,2 s; NCBear_Eat 3,2; NCBear_Maul 1,6; DeerStag_Dead 0,033; NCBear_Sit 4,0; DeerStag_Run 0,533;
  NCBear_Bite 1,3; NCBear_SwipeR 1,5; DeerStag_Death 2,567; NCBear_Rear 3,0; NCBear_Slam 2,4; NCBear_SwipeL 1,5; DeerStag_Walk 0,9;
  NCBear_SitDown 1,6; NCBear_StandUp 1,3.
- Kiefer oeffnet in Eat 15 Grad, Sit 5, Maul/Bite ~34, Rear 38. Das Junge braucht deshalb eine geschlossene Mundhoehle (4.2).

### 3.4 Unsere Definition heute (NCBearTest, nur gelesen)

- `42/media/lua/shared/NCBearDefs.lua:62-102`:
  - zwei Arten `bear` / `bearstag`, je eine Stufe gleich dem Tiernamen (`ageToGrow = 60`, kein `nextStage`);
  - `animset = "buck"`, `minSize = maxSize = 1.0`;
  - Rasse `brown` mit `texture = textureMale = "NCBear"` (:36-60).
- `42/media/scripts/nc_bear_tier.txt:3-15`: `animationsMesh NCBear { meshFile = Skinned/NCBear.glb, keepMeshAnimations = true }`,
  `model NCBear_Body` (module Base, `shader = animalEffect`).
- `NCBearSize.lua:8-34`: Groesse nur per Konsole (`setSizeForced`, gilt bis zum naechsten Tag).
- Es gibt heute **kein Wachsen und keine Stufen**. Das kommt in B1.

### 3.5 Empfehlung: eigenes GLB (begruendet)

| Weg | geht? | Aufwand | Ergebnis |
|---|---|---|---|
| A **Eigenes `NCBearCub.glb`**: gleiche 26 Knochennamen, eigene Knochenlaengen, eigenes Netz (Kopf nach 4.1), eigene Textur, 15 Clips per Skript (3.3) | ja, Vanillas Weg (3.1) | Netz + Textur (dieser Lauf als Entwurf), Clip-Skript + Definition in B1 | eigenes Gesicht, Junges-Proportionen, Clips nutzbar |
| B Knochen-Skalierung am Erwachsenen-GLB | **nein** (3.3 a) | -- | Clips ziehen alles zurueck |
| C Gleiche Knochenlaengen, nur anderes Netz (Kopf gross, Rumpf rund, Beine bleiben lang) | ja, Clips bit-gleich | am kleinsten | Beine zu lang (Kevin will kurze Beine); nur Rueckfall |
| D Wie Maus: Erwachsener bei 0,35 | ja (heute) | null | "Spielzeug-Erwachsener" (baer-fell-Bericht) |

**Empfehlung A.**

- Uebergang: **Jungtier-Modell von 0,35 bis 0,75**, ab Halbstark das Erwachsenen-Modell. Kevins Wort offen; ENTSCHEIDUNGEN.md:140 sagt
  "evtl. auch noch Halbstark".
- Beim Wechsel springt die Form sichtbar (Bild R5b zeigt den Moment).
- Rueckfall C, wenn das Clip-Skript in B1 scheitert.

### 3.6 Namen und Kollisionsprobe

| Was | Test-Mod | spaeter NPC Crew |
|---|---|---|
| Netz | `models_X/Skinned/NCBearCub.glb` | `BanditsNPCBearCub.glb` |
| animationsMesh / model (module Base) | `NCBearCub` / `NCBearCub_Body` | `BanditsNPCBearCub` / `BanditsNPCBearCub_Body` |
| Textur | `textures/Body/NCBearCub.png` (als `breed.textureBaby`) | `Body/BanditsNPCBearCub.png` |
| Tierart | `bearcub` (Stufe -> `bear`) | B1 entscheiden (siehe unten) |
| Avatar / Zerlegen | `AnimalAvatarDefinition["bearcub"]`, `AnimalPartsDefinitions.animals["bearcubbrown"]` | entsprechend |

Probe am 10.11.2026:

- `grep -rli "bearcub|NCBearCub|BanditsNPCBear|AnimalDefinitions.animals[\"bear"` in `NPCCrew/42/media/lua`: **0 Treffer**.
  "cub" allein: 0 Treffer.
- Vanilla `media/lua` + `media/scripts`: kein `bearcub`, kein Tier `bear`. Nur `IGUI_ItemCat_Bear` (Item-Kategorie, kein Konflikt).
- NCBearTest: kein `cub`/`baby` ausser einem Kommentar in `NCBearSize.lua:2`.
- **Hinweis B1:** `AnimalDefinitions.animals` ist eine globale Tabelle aller Mods. Ein anderer Baeren-Mod koennte `bear` ebenfalls
  belegen. Fuer NPC Crew einen Praefix erwaegen (betrifft auch den Erwachsenen).
- NPC Crew liest die Tabelle nur (z. B. `client/ISUI/BanditsNPCLivestockPanel.lua:4079`, in `pcall`, nach `group`). Mit `group = "bear"`
  in B1 gegen Livestock pruefen.

### 3.7 Was in B1 dazukommt (nicht dieser Lauf)

1. Clip-Skript: 15 Clips in `NCBearCub.glb`.
   - Lage-Schluessel neu, Drehungen bit-gleich;
   - Bip01/Pelvis mit Hueft-Faktor, Bodenkorrektur je Bild;
   - `Translation_Data` und Dauer nach Kevins Wort (3.3, Punkt 4).
2. Definition `bearcub`:
   - `bodyModel = "NCBearCub_Body"`, `animset = "buck"`, `group = "bear"`;
   - Stufen: `bearcub` ageToGrow 7, `nextStage`/`nextStageMale` = "bear"; `bear` ageToGrow 14, `minAge` 7;
   - `minSize` 0,35, `maxSize` 0,75; Erwachsener `minSize` 0,75 (oder 0,58 gegen den 1,3-Sprung, 3.2), `maxSize` 1,35;
   - `textureBaby = "NCBearCub"` in der Rasse.
   
   Die Gen-Liste ohne `maxSize`-Gen lassen (NCBearDefs.lua:14), sonst wuerfelt das Genom die Groesse.
3. Uebergabe beim Wechsel: modData (Besitzer, Zaehm-Balken, Inventar, Level) ueber die AnimalID auf das neue Tier, SP und MP (Server
   macht `grow`).
4. `isBaby`-Nebenwirkungen pruefen (3.2); Avatar-/Zerlege-Eintraege fuer `bearcub`.
5. Kevins Tests SP und MP. Uebernahme-Naehte (NAEHTE-Liste): `AnimalDefinitions` global, NPC-Crew-Livestock.

---

## 4. SOLL

### 4.1 Kopf und Gesicht -- Form im Netz (Ton muss das Junge zeigen)

**Kopf-Rahmen:** x vorn entlang der Kopfachse (wie HA des Erwachsenen, 15 Grad nach unten geneigt in Ruhe), y links, z oben.
Ursprung = Mitte zwischen den Augen, Einheit W. Alle Zahlen stehen maschinenlesbar in `werkzeug/ziel_kopf.json`.

| Punkt / Mass | Soll | Toleranz | Erwachsener heute |
|---|---|---|---|
| Augenmitten | (0, +-0,15, 0) | +-0,01 | +-0,15 |
| Absatz (tiefster Punkt Mitte zw. Nasenruecken und Stirn) | (0,04, 0, -0,02) | +-0,03 | (~0,04, 0, ~0,0) |
| Nase oben-vorn / Spitze / Mitte | (0,25,0,-0,095) / (0,27,0,-0,14) / (0,24,0,-0,155) | +-0,03 | Spitze 0,395 vor dem Auge |
| Nasenruecken-Neigung (Absatz -> Nase oben) | -22 Grad | +-8 | -3,7 |
| Stirn: Anstieg in den ersten 0,08 W ueber dem Absatz | >= 60 Grad | -- | Stufe, dann flach |
| Krone (hoechster Punkt der Mittellinie) | (-0,30, 0, 0,34) | x +-0,07, z +-0,04 | (-0,665, 0, 0,20) |
| Kuppel: Profil oben | (0,0/0,10) (-0,05/0,20) (-0,12/0,28) (-0,20/0,325) (-0,30/0,34) (-0,42/0,30) (-0,52/0,22) (-0,60/0,12) | +-0,03 | flach 0,19-0,20 von -0,79 bis -0,1 |
| Hinterkopf in Ohrhoehe | x -0,63 | +-0,06 | -0,76 |
| Kopflaenge (Nasenspitze bis Hinterkopf) | 0,90 | +-0,06 | 1,16 |
| Kinn (tiefster Punkt vor x -0,03) | (0,12, 0, -0,34) | +-0,04 | z -0,457 |
| Profil unten | (0,255/-0,20) (0,23/-0,215) (0,21/-0,24) (0,19/-0,27) (0,12/-0,34) (0,0/-0,38) (-0,20/-0,40) | +-0,03 | tiefer, laenger |
| Breiteste Stelle (Wangenfell) | y +-0,50 bei z -0,06, x -0,12 | W selbst | -- |
| Breite an der Ohrbasis | 0,90 | +-0,04 | -- |
| Schnauzenbreite an der Nase / am Absatz | 0,33 / 0,18 | +-0,03 | 0,337 / -- |

**Foto-Kamera (p = 30 Grad, orthografisch, Kopf-Umriss ohne Koerper) -- Abnahme gegen das Foto:**

| Mass | Soll | Foto |
|---|---|---|
| Umriss oben ueber Augenlinie | 0,46 +-0,04 | 0,457 |
| Ohr oben | 0,50 +-0,04 | 0,50 |
| Ohrmitte | 0,38 +-0,04 | 0,373 |
| Nasenmitte | -0,25 +-0,03 | -0,249 |
| Kinn | -0,36 +-0,05 | ~-0,37 |
| W/H | 1,20 +-0,08 | 1,195 |
| Auge unter Umriss oben / H | 0,56 +-0,04 | 0,546 |

### 4.2 Teile

- **Ohren:**
  - runde Scheibe, D 0,245 W (+-0,025), Dicke mit Fell 0,08 W (+-0,02), Rand rund und wulstig ("dick bepelzt");
  - Mitte (-0,32, +-0,35, 0,26); Mulde zeigt nach vorn-aussen-oben, Normale ~(0,85, 0,35, 0,40) (Erwachsener (0,74, 0,60, 0,30));
  - Mulde 0,6 D, 0,02-0,03 W tief; Ohren ragen in der Foto-Kamera 0,04 W ueber den Umriss.
  - Einfluss nur `Bip01_Head`.
- **Augen:**
  - Oeffnung rund-mandelfoermig 0,056 x 0,043 W (h/b 0,75 +-0,1), Blickachse 18 Grad nach aussen, 8 Grad nach oben
    (Erwachsener 29 / 15 Grad, Schlitz 0,061 x 0,020);
  - Augapfel sichtbar dunkel, sitzt 0,01-0,02 W tiefer als das umgebende Gesicht. Keine tiefe Hoehle, kein Brauenwulst.
  - Oberlid deckt hoechstens das obere Sechstel; Unterlid als feiner Rand 0,004-0,006 W, in der Textur hellgrau.
- **Schnauze:**
  - kurz und stumpf; Querschnitt an der Nase rund-oval, Breite 0,33 W, Hoehe (Nase oben bis Kinn) ~0,25 W;
  - verjuengt sich nach oben zum Absatz (0,18 W), Wangen gehen weich in die Schnauze ueber.
- **Nase:**
  - Polster 0,165 x 0,105 W (Vorderflaeche), oben gerade Kante, unten schmaler (0,12 W);
  - zwei Nasenloecher als Kommas 0,045 W neben der Mitte, 0,03 W unter der Nasenmitte;
  - Polster steht 0,01-0,015 W aus der Schnauze; Mittelfurche zur Oberlippe.
- **Mund:**
  - geschlossen, Linie von der Nasenfurche nach hinten bis zum Mundwinkel (0,03, +-0,13, -0,24);
  - **Mundhoehle mit dunklem Inneren und flacher Zunge**, damit Eat (15 Grad), Sit (5 Grad) und notfalls Maul (34 Grad) kein Loch
    zeigen. Kleine Milchzaehne optional (das Junge bruellt nicht).
- **Wangen:** leicht abstehend: Fellzacken 0,015-0,03 W am Umriss zwischen z +0,18 und -0,24 (wie die Zotteln aus baer-fell, aber kurz).
- **Kein Kragen:**
  - Kopf- und Halsfell gehen ohne Kante in den Rumpf ueber;
  - im Umriss von Seite und 3/4 keine Stufe > 0,01 L um Hals und Hinterkopf;
  - keine Rumpf-Fellhuelle, die ueber den Kopfansatz greift.

### 4.3 Textur (Zonen, Toene, Platz)

| Zone | Ton (sRGB Median) | Toleranz | Hinweis |
|---|---|---|---|
| Gesicht / Stirn Grund | (80,63,57) | +-15 je Kanal | gesprenkelt: 10-15 % Spitzen (126..163, 108..136, 101..124) auf Grund (41..80, 23..63, 18..57) |
| Wangen | (88,60,42) | +-15 | waermer, roetlich |
| Augenring (r 0,033-0,057 W) | (53,40,36) | +-12 | dunkler als die Stirn um ~25 L |
| ueber dem Auge | (73,54,46) | +-12 | Hauch heller als der Ring |
| Schnauze oben / seitlich | (155,131,118) / (158,125,103) | +-15 | Lichter bis (190,160,140) |
| Verlauf Schnauze -> Gesicht | hell bis zum Absatz, dann in 0,04-0,06 W auf Gesichtston; Zunge der hellen Zone bis zwischen die Augen (0,10-0,16 W breit) | -- | Foto: L 155 -> 82 |
| Nase | (23,19,20) | +-10 | Oberkante gemalt (98,95,100)..(137,129,127), 0,015 W breit; kleiner Glanzfleck |
| Iris/Pupille | (30,25,25) | +-10 | gemalter Glanzpunkt (225,230,240), D 0,008-0,012 W, oben-vorn |
| Unterlid-Rand | hellgrau ~(150,150,155) | +-20 | fein |
| Ohr aussen | Koerperfell mit Spitzen | -- | |
| Ohr Rand | (146,113,93) | +-20 | |
| Ohr Mulde | (19,9,6)..(35,22,15) | +-12 | |
| Ohr Innenrand-Haare | (99,72,58)..(150,115,92) | +-20 | "innen heller" |
| Koerper / Beine | (79,58,50) Grund, Spitzen wie oben | +-15 | zu den Pranken dunkler |
| Krallen | elfenbein-grau (126,122,129) Spitze, dunkler Ansatz | +-20 | 5 je Pranke, im Verhaeltnis gross |

- Der Tier-Shader rechnet Textur x min(1; 0,45 + 0,425 (N.L1) + 0,425 (N.L2)) (`_arbeit/baer_fell/forschung_engine.md` 4.1, zitiert in
  `baby_vergleich.py:8`). **Kein Glanz** -> Nase und Augenglanz malen; Toene oben sind Albedo-Ziele.
- **Platz:**
  - Body-Textur **1024 x 1024 RGB** `NCBearCub.png`; Kopf (Gesicht+Ohren) >= 30 % der genutzten UV-Flaeche (Erwachsener 26 %);
  - Gesicht vorn (Ohrbasis bis Kinn) >= 256 x 256 Texel; Auge >= 14 Texel breit;
  - Augen, Nase, Mund **nicht auf einer UV-Naht**; Gesichtshaelften gespiegelt erlaubt (Glanzpunkt dann gespiegelt).
- **Regel:** Textur erst, wenn das Ton-Bild steht; eine Textur darf keine falsche Form verdecken (Ton und Textur immer nebeneinander).
- Erzeugen nur prozedural/gemalt aus diesen Zahlen. **Keine Vorlagen-Pixel**; kein Skript liest die Vorlage ausser den Mess-/Blatt-Skripten
  hier.

### 4.4 Koerper-Proportionen (Junges-GLB, Ruhe-/Idle-Bild 0, Groesse 1,0)

| Mass | Soll | Toleranz | Erwachsener | baer-fell-Junges |
|---|---|---|---|---|
| L Nasenspitze bis Rumpfende | 1,90 m (66,5 cm bei 0,35) | +-0,08 m | 1,957 m | 1,693 m |
| Kopfbreite W | 0,34 L | +-0,03 | 0,22 L | 0,36 L |
| Kopflaenge | 0,90 W (~0,31 L) | +-0,06 W | 0,26 L | 0,32 L |
| Ruecken oben (Widerrist) | 0,54 L (35,9 cm bei 0,35) | +-0,04 | 0,59 L | 0,56 L |
| Bauch ueber Boden | 0,11 L | +-0,03 | 0,15 L | 0,06 L (Ruhe) |
| Kopf oben (ohne Ohren) gegen Ruecken | -0,03 L bis +0,08 L | -- | -0,14 L | -0,105 L |
| Rumpf Breite / Hoehe | 1,00 | +-0,08 | 1,07 | 1,25 (zu breit) |
| Rumpf Breite | 0,42 L | +-0,04 | 0,475 L | 0,63 L |
| sichtbarer Hals (Hinterkopf bis Schulterlinie) | <= 0,08 L | -- | lang | -- |
| Pfoten / Krallen | Erwachsenen-Groesse bei gleichem L | +-10 % | -- | relativ gross |

- Startwerte der Knochenlaengen = Laengsfaktoren aus `baer_fell/baby/auftrag.json`:
  - Beine 0,64; Rumpf 0,80-0,84; Hals 0,50; Kopf neu;
  - quer **nicht** 1,16: der Rumpf wird direkt rund modelliert.
- `Bip01`-Hoehe neu, so dass die Pfoten in DeerStag_Idle01 Bild 0 auf dem Boden stehen. Danach alles gleichmaessig skalieren, bis L = 1,90 m.
- Kevins Tabelle (ENTSCHEIDUNGEN.md:8) sagt 70 cm / 40 cm Schulter. Mit kurzen Beinen wird die Schulter ~36 cm; das Bild R5 zeigt es.
- **Offen gesagt:**
  - Der Rumpf darunter ist der heutige Stand mit Junges-Proportionen.
  - Hinterfuss ("Menschenfuss"), "Hose in Stiefeln" und Sitzhaltung werden in Lauf 2c gebaut, nicht hier.
  - Den Kragen vermeidet das Junge selbst (4.2).

### 4.5 Technik

- **Knochen:**
  - genau die 26 des Erwachsenen, gleiche Namen, Eltern und Reihenfolge wie im Dump: Dummy01, Bip01, Bip01_Pelvis, L/R Thigh, Calf,
    Foot, Toe0, Spine, Spine1, L/R Clavicle, UpperArm, Forearm, Hand, Neck, Head, Jaw, Tail, Translation_Data;
  - Pflichtnamen siehe tier_spez.md:23-24.
- **<= 20.000 Dreiecke** (Erwachsener 19.426, davon Kopf 2.465). Vorschlag:
  - Kopf 3.000-4.500 (Ohren je ~350, Augen/Lider je ~250, Nase ~300, Mundhoehle ~300), Rumpf/Beine <= 14.000, Krallen wie heute.
- **<= 4 Einfluesse je Punkt, Summe 1 (+-1e-4)** (Erwachsener: max 4, Summe 1,0).
  - Kopf/Ohren/Nase nur Head; Unterkiefer, Kinn und Unterlippe Jaw; Hals weich Neck/Head.
- Ein Netz, ein Material, GLB wie der Erwachsene (baer_export-Weg, `keepMeshAnimations`). Textur 1024 RGB.
- Dieser Lauf baut nur den **Entwurf** (Netz, Textur, Renders), keine Mod-Dateien. Fuer Renders in Pose reicht die Knochen-Skalierung in
  numpy wie `baby_vergleich.py welt_junges` plus Bodenausgleich. Das GLB mit Clip-Kopien ist B1.

### 4.6 Renders fuer Kevin (Ton UND Textur, immer nebeneinander)

| Nr | Bild | Pose | Kamera |
|---|---|---|---|
| R1 | **vorn wie das Foto** | liegend, Kinn zwischen den Pranken (Standbild-Pose nur fuer das Bild erlaubt; Vorderbeine flach nach vorn, Hinterbeine untergeschlagen) | Foto-Kamera 30 Grad ueber der Kopfachse, Licht vorn-links-oben |
| R2 | 3/4 von vorn | stehend (DeerStag_Idle01 Bild 0) | az 315, 20 Grad hoch |
| R3 | Seite | stehend | az 90 und 270, 5 Grad |
| R4 | Sitzen | NCBear_Sit bei 2,0 s (Clip von heute, umgerechnet) | az 300, 20 Grad |
| R5 | **Spielkamera, Spielgroesse** | stehend und sitzend | orthografisch 30 Grad (Core.DoPushIsoStuff), Licht wie animalEffect, 577 px/Einheit (Kevins 4K-Zoom) und 289 |
| R5b | Wechsel-Moment | Junges bei 0,75 neben dem Erwachsenen bei 0,75 | wie R5 |
| R6 | Kopf nah | -- | Foto-Kamera und Seite, 1500 px/Einheit |

- R5: Spielfigur (MaleBody, `baby/mensch.py`), Erwachsener x 0,35, Junges bei 0,35; az 315 und 90.
- R1 zusaetzlich als **internes** Blatt neben dem Foto (nur unter `_arbeit/baer_baby`); fuer Kevin R1 neben `skizze_baby.png`.
- GPU: nur RTX 4090/OptiX + Entrauscher, Sperre `_arbeit/baer_baby/gpu.lock`, wartet auf fremdes blender.exe (`werkzeug/gpu_render.sh`).
  Zwischenstaende 480 px / 16 Samples.

### 4.7 Abnahme-Messungen (Pruefer)

Der Bauer legt `landmarken.json` ab: Augenmitten, Absatz, Nase (Mitte/Spitze), Krone, Ohrmitten, Kinn, Mundwinkel in Spiel-Metern bei
Groesse 1,0, dazu die Kopfachse.

1. **Form Kopf (Ton)**, mit `werkzeug/mess_kopf.py` umgestellt auf den Rahmen aus `landmarken.json`:
   - jede Landmarke <= 5 mm vom Netz;
   - alle Werte 4.1 (3D-Tabelle und Foto-Kamera-Tabelle) in Toleranz;
   - Ohr-D, Ohr-Abstand, Ohren aussen, Augenoeffnung, Nase, Schnauze (2.-Tabelle, Spalte Soll).
2. **Ton neben Foto:** Blatt wie `vergleich_ton_foto.png` mit dem Jungen; die roten Fotolinien treffen Umriss oben, Ohrmitte, Nase und
   Kinn in Toleranz. Ton-Bild **vor** jedem "fertig".
3. **Kein Kragen:** Umriss-Stufe um Hals/Hinterkopf <= 0,01 L in R2/R3 (Ton).
4. **Koerper:** alle Werte 4.4 im Idle-Bild 0 nach Bodenausgleich.
5. **Technik**, Dump ueber den Importer-Harness (`_arbeit/baer_spiel/harness/Dump.java`):
   - 26 Knochen Name/Eltern/Reihenfolge = Erwachsener;
   - Dreiecke <= 20.000; Einfluesse <= 4, Summe 1 +-1e-4; ein Netz/Material;
   - Textur 1024 x 1024 RGB; kein NaN.
6. **Clips** (nur falls im Entwurf schon gebaut, sonst B1):
   - 15 Namen und Dauern gleich (+-1e-4); Drehschluessel bit-gleich;
   - Lage-Schluessel konstant = Jungen-Lagen (ausser Pelvis/Translation_Data);
   - Bodenabstand der Stuetzpfoten je Bild <= 1,5 cm; Hautdehnung je Clip nicht schlechter als Erwachsener + 10 %
     (`baer_pfote/werkzeug/messen.py`-Weg).
7. **Textur:**
   - Median je UV-Zone in der Toleranz 4.3;
   - Auge/Nase/Mund ohne Naht;
   - Ton und Textur in R1/R6 nebeneinander: die Textur malt keine Form, die im Ton fehlt (z. B. keine gemalte Stirnwoelbung, keine
     gemalten runden Augen auf Schlitz-Lidern).
8. **Regeln:**
   - kein Schreiben in NCBearTest, NPC Crew, `_arbeit/baer_2c`, `baer/spiel/*_2c.py` oder Originale in `baer/spiel`;
   - neue Skripte nur `baer/spiel/*_baby.py`, Ausgaben nur `_arbeit/baer_baby`;
   - `kevin_babygesicht_vorlage` nur in Mess-/Blatt-Skripten (grep).

### 4.8 Grenzen, offen, ungeprueft

- Foto-Kamera p = 30 Grad ist eine Schaetzung (+-10); die Seitenform ist daraus abgeleitet, nicht gemessen. Kevins Blick auf R3 entscheidet.
- Kinn im Foto verdeckt (+-15 px). Krone aus der Schaerfe geschaetzt.
- Das Foto ist farblich bearbeitet oder vielleicht kuenstlich erzeugt: Herkunft unbekannt, die Toene sind Ziele, keine Biologie.
- Nicht gespielt: Wachsen, Typwechsel, `isBaby`, Gleiten und Groessensprung sind statisch gelesen, nicht im Spiel gesehen.
- Javap gegen das Jar vom 09.11. 16:07 (heute installiert). Die Vineflower-Zeilen (`dec/`) stammen vom Jar des 07.11.; die zitierten
  Stellen sind im heutigen Jar per javap gegengeprueft (grow, setSize, updateBoneAnimationTransform_Internal, play).

---

## 5. Dateien (alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/`)

- `SPEZ_BABY.md` (dieses Blatt), `skizze_baby.png` (Soll vorn/Seite, ohne Vorlage).
- `vergleich_ton_foto.png` (**mit Vorlage, nur hier**): Ton Erwachsener/baer-fell neben dem Foto.
- `referenz/` (**mit Vorlage, nur hier**): `r_*.png` Raster-Ausschnitte, `farben.json`.
- `mess/kopf_mass.json`, `mess/umriss_*.png`: Kopfmasse Erwachsener/baer-fell.
- `ton/*.png`, `ton/auftrag.json`, `ton/netze.npz`: Ton-Einzelbilder und Eingaben.
- `jar/*.javap.txt`, `jar/cls/`: javap-Auszuege (AnimalData, AnimationPlayer, AnimationsMesh, AnimationTrack, AnimalDefinitions).
- `werkzeug/`:
  - Messen: `raster.py`, `farben.py`, `kopf_mess.py`, `kopf_teile.py`, `mess_kopf.py`, `mess_koerper.py`, `clip_schluessel.py`;
  - Ton: `ton_vorbereiten.py`, `ton_kopf.py`, `gpu_render.sh` (Kopie, Sperre baer_baby), `blatt_ton_foto.py`;
  - Soll: `skizze.py`, `ziel_kopf.json` (Soll-Kopf maschinenlesbar).
- `log/ton_kopf.log`.
