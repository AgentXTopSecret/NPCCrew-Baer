# Lauf baer-baby: Bau Entwurf Baer-Junges (10.11.2026 nachts)

> **Stand: ueberholt durch die Nachbesserung `fix_baby.md` (fix1).** Der Text unten beschreibt den Bau VOR fix1 (Sicherung
> `fix1/vorher/`); Berichtigungen fix1 sind im Text markiert.

Blender 5.2.3, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert (RTX 4090, OptiX + Entrauscher), NICHT gespielt.**
Nichts in NCBearTest (GLB weiter MD5 5066fa67), NPC Crew, `_arbeit/baer_2c` oder `baer/spiel/*_2c.py` geschrieben; nichts committet.
Originale `baer/spiel/*_pfote.py` unveraendert (MD5 `log/md5_originale_vorher.txt` = `log/md5_originale_nachher.txt`). Die Vorlage
(`kevin_babygesicht_vorlage.webp`) liest nur `werkzeug/blatt_foto_baby.py` (Blatt nach `intern_vorlage/`); kein Pixel davon in Netz/Textur.
Verbindlich war `SPEZ_BABY.md`; Masse in W = Kopfbreite (0,646 m bei Groesse 1,0), L = Nasenspitze bis Rumpfende.

## 0. Kurz

1. **Gebaut:** `entwurf/NCBearCub.glb` (MD5 129cfc23db342d66c3a0030181725335) + `entwurf/NCBearCub.png` (1024 x 1024 RGB, MD5
   07abcf75dc10e012539f2028a07e011a). 19.938 Dreiecke (Koerper 15.860 = Erwachsenen-Netz, Kopf/Hals 4.078 neu), 26 Knochen wie der
   Erwachsene, 15 Clips umgerechnet. Der Importer des Spiels (Dump.java) laedt die Datei; alle Technik-Pruefungen gruen (3.7).
2. **Kopf und Gesicht neu als Form im Netz** (nicht nur skaliert): gewoelbte Stirn mit Absatz, kurze Schnauze, Nasenpolster, runde Augen
   als Oeffnung mit Augapfel 0,01 W tiefer, flacher Unterkiefer als eigene Schale (Maul oeffnet ohne Loch, dunkles Inneres + Zunge), runde
   dicke Ohren mit Mulde. **Alle Kopfmasse der SPEZ 4.1 in Toleranz** (Foto-Kamera und 3D, 3.1/3.2). Ton-Bild neben dem Foto angesehen
   (`intern_vorlage/vergleich_R6_foto.png`, `..._R1_foto.png`): die roten Fotolinien (Krone, Ohr, Auge, Nase, Kinn) treffen.
3. **Koerper:** Junges-Proportionen ueber Knochenlaengen (Beine 0,74, Rumpf quer 0,86 / hoch 0,94, Hals 0,45); L 1,857 m (65 cm bei 0,35),
   alle Werte SPEZ 4.4 in Toleranz. **Kein Kragen:** Hals = eigener Loft, der genau am Koerperrand ansetzt (Stufe im Umriss 0,0011 L).
4. **Textur:** Koerper = Fell des Erwachsenen (Farbe auf Soll gezogen), Kopf/Hals/Ohren prozedural aus den SPEZ-Zahlen; 15 von 16 Zonen
   im Soll (Ausnahme "ueber dem Auge", 3.9). Nasen-Glanz und Augen-Glanzpunkt gemalt.
5. **Bilder fuer Kevin** (`bilder/`, ohne Vorlage): R1 vorn liegend wie das Foto (neben der Soll-Skizze), R2 3/4, R3 Seite, R4 Sitzen,
   R5 Spielkamera 577/289 px je Einheit neben Spielfigur und Erwachsenem x 0,35, R5b Wechsel bei 0,75, R6 Kopf nah, Clip-Pruefung.
6. **Nicht erreicht (ehrlich):** Hautdehnung im Koerper in den Clips deutlich schlechter als beim Erwachsenen (p99,5 bis 4,41 statt
   <= Erwachsener + 10 %), Ursache Achsel/Leiste der Knochen-Skalierung (3.8, 6). Weg (`Translation_Data`): *Berichtigung fix1* -- NICHT unveraendert,
   sondern Erwachsener x 0,777 (diag(S_eltern), `baer_export_baby.py`; Walk 0,294 statt 0,378 E, Run 0,822 statt 1,058 E); jetzt
   Schalter `WEG_FAKTOR` (Kevins Wort, B1). Kopffell wirkt "wollig" und etwas kuehler/dunkler als das Koerperfell. Nicht gespielt.

## 1. Was gebaut ist

| Datei | Inhalt |
|---|---|
| `baer/spiel/baer_form_baby.py` (neu) | numpy-Kern. `Erwachsener` (:96, Ruhe aus den GLB-Knoten, FK gegen inv(Offset) geprueft), `Junges` (:161, Knochenlaengen = diag(S_eltern) x Lage, Drehungen bit-gleich, `koerper_ruhe` = Netz in die Ruhe des Jungen), Faktoren `FAKTOR`/`TL, FH` (:42-58), Halsansatz +5 cm `VERSATZ_TIER` (:59), `L_ZIEL` 1,84 (:33). Kopf-Rahmen am Kopfknochen `GELENK_KOPF_W` (:237, Gelenk bei (-0,45/-0,24) W), `kopf_rahmen_lokal` (:241). Kopf-Form als implizites Feld: `schaedel` (:285), `schnauze` (:298), `nase` (:323), `kopf_feld` (:341: Schaedel + Wangen + Unterkopf + Schnauze + Kinn + Nase, Augenloch + Augapfel, Maul-Schnitt), `kiefer_feld` (:377), `augen_loch`/`augen_setzen` (:724/:736), Parameter `KOPF_P` (:432). `ray_cast`/`stern_pruef` (:451/:476), Koerper ohne Kopf+Hals + Randschleife `koerper_netz` (:489), Karten/Quadtree (:662-:722). Nicht mehr benutzt (Vorstufen, bleiben zur Nachvollziehbarkeit): `hals_feld`, `hals_aus_rand`, `mulde`, `augapfel_mitten`, `falten_glaetten` (6). |
| `baer/spiel/baer_netz_baby.py` (neu, Blender nur fuer `delaunay_2d_cdt`) | Kopfteile als sternfoermige Schalen: Strahlen von einem Mittelpunkt, Karten (vorn flaechentreu, Band, hinten) = UV, Dichte je Merkmal `l_oben0` (:73, Augen/Nase/Lippenkante fein), Lippenkante als Zwangskanten `lippen_kante` (:229). `schale` (:108). U = Oberkopf, J = Unterkiefer (:254/:255), Ohren als Rotationskoerper `ohr` (:259), Hals-Loft `hals_loft` (:361: Zeile 0 liegt exakt auf der Koerper-Randschleife, Tangente setzt die Koerperflaeche fort, inneres Ende mit Deckel im Kopf), Gewichte Hals `gewichte_loft` (:543: v=0 Randgewichte, v=1 Head), UV-Atlas `ATLAS` (:451). Pruefung Volumen > 0 je Teil. `auge()` (:324, eigene Augaepfel) und `gewichte_hals` (:520) sind Vorstufen, ungenutzt. |
| `baer/spiel/baer_textur_baby.py` (neu) | `ZIEL` (:24 = SPEZ 4.3), Rauschen/Fell (:35-:66), Rasterung im UV (:74), `main` (:117): Koerper-Rechteck aus der Erwachsenen-Textur (Kanal-Faktor auf (79,58,50)), Kopfzonen, Fell-Straehnen entlang des Haarstrichs (von der Nase weg), Verdeckung aus der Form (nicht auf gemalte Teile), Polster. |
| `baer/spiel/baer_export_baby.py` (neu) | GLB ohne Blender aus dem Gerippe der Erwachsenen-GLB: Knoten-Lagen neu, inverse Bind neu, Netz-Puffer neu, Clips: Zeit/Dreh/Skalier-Schluessel byte-gleich, Lage-Schluessel konstant = Junges, Becken/Bip01/Translation_Data = Erwachsener x diag(S_eltern), **Bodenausgleich je Bild** im Becken (`BODEN` :22). |
| `_arbeit/baer_baby/werkzeug/` (neu) | `koerper_mass.py` (loest TL/FH), `kopf_schnitt.py` (Feld-Probe), `schnitt_netz.py`, `mess_baby.py` (Abnahme SPEZ 4.7 Punkt 1/3/4 + `landmarken.json`), `pruef_glb.py` (Punkt 5/6 ueber den Dump), `clip_pruef.py` (Dehnung, Boden), `render_vorbereiten.py` + `render_baby.py` (Ton/Textur/Spiel-Licht, Posen aus dem Importer-Dump), `posen.json` (Standbild "liegen_kinn"), `blatt.py`, `blaetter_final.py`, `blatt_foto_baby.py` (intern). Kopien: `baby_vergleich.py`, `zusammen.py`, `mensch.py/.npz`, `dumpread.py`, `glb_datei.py`, `glb_pruef.py`, `messen.py`, `dehnung_lib.py`. |

**Warum nicht die Pfoten-Kette (`*_pfote.py`) kopiert:** Die kopiert ein Hochmodell (Metaballs, Surface Nets, Huelle, Backen aus
Ansichten). Das Junge braucht nach SPEZ 4.5 nur den heutigen Koerper mit Junges-Proportionen + einen neuen Kopf; die neuen Skripte
heissen trotzdem `*_baby.py` und liegen in `baer/spiel`. Der Kopf entsteht ohne Verringern: die Karten-Vernetzung bestimmt die
Dreieckszahl direkt (kein Faltenwurf, Augen/Nase/Mund auf keiner Naht).

## 2. Runden (Form, Ton-Bild jeweils angesehen)

| Runde | Aenderung | Befund im Ton-Bild |
|---|---|---|
| f1-f6 (Feld-Probe `form/*.png`) | Schaedel/Schnauze/Kinn/Wangen nach `ziel_kopf.json` | Profil oben trifft (Abw. <= 0,016 W); Wangen-Ellipsoid zeichnete erst einen Kreis ums Gesicht -> weicher verbunden |
| n1-n3 (`render/t4`) | erstes Netz, Hals-Lappen im Kopffeld | Teddy-Gesicht ja, aber **Kragen/Platte** hinter dem Kopf (Lappen ragte seitlich vor die Schulter, `form/schnitt_n4.png`) |
| n5-n9 (`t5`, `t6`, `t9`) | Hals als Loft genau auf dem Koerperrand, geglaettete Zeilen | Kragen weg; Rillen/Baender am Hals verschwunden; Dreiecke auf <= 20.000 gebracht (Lippen-Dichte nur an der Kante) |
| n10-n12 (`t10`-`t12`) | Augen als Zylinder-Oeffnung + Augapfel 0,01 W tiefer, Nasenpolster steht vor, Lippenkante als Zwangskante | Augen lesbar rund, Nase sichtbar, Mundlinie sauber statt Zickzack |
| n13 / final (`t13`, `render/final`) | Schaedel runder (Ohren freier), Wangen unten voller; Hals-Ende tiefer im Kopf + Deckel | In Gehen/Sitzen/Rennen **kein schwarzer Spalt** mehr am Nacken (vorher sichtbar, `render/h2/_b.png`), `render/h3/_b.png` |

## 3. Messwerte gegen SPEZ (Netz `netz/final.npz`, `mess/mess_final.json`)

### 3.1 Foto-Kamera 30 Grad (SPEZ 4.1, in W zur Augenlinie)
| Mass | gemessen | Soll | |
|---|---|---|---|
| Umriss oben | 0,477 | 0,46 +-0,04 | ok |
| Ohr oben | 0,508 | 0,50 +-0,04 | ok |
| Ohrmitte | 0,385 | 0,38 +-0,04 | ok |
| Nasenmitte | -0,256 | -0,25 +-0,03 | ok |
| Kinn | -0,363 | -0,36 +-0,05 | ok |
| W / H | 1,200 | 1,20 +-0,08 | ok |
| Auge unter Umriss / H | 0,568 | 0,56 +-0,04 | ok |
| Breite an der Ohrkerbe (v 0,263) | 0,907 | 0,90 +-0,04 | ok |
| Ohren aussen | 0,925 | 0,93 +-0,04 | ok |

### 3.2 Kopf 3D (Kopf-Rahmen, W)
| Mass | gemessen | Soll | |
|---|---|---|---|
| Krone (x, z) | (-0,311, 0,340) | (-0,30 +-0,07, 0,34 +-0,04) | ok |
| Nasenspitze vor dem Auge | 0,282 | 0,27 +-0,03 | ok |
| Hinterkopf (Ohrhoehe) | -0,629 | -0,63 +-0,06 | ok |
| Kopflaenge | 0,911 | 0,90 +-0,06 | ok |
| Kinn bei x 0,12 | -0,340 | -0,34 +-0,04 | ok |
| tiefster Punkt vor x -0,03 (Definition 4.1) | -0,380 bei x -0,03 | -0,34 +-0,04 | Grenze: das Soll-Profil selbst hat (0,0/-0,38) |
| Profil oben / unten max. Abweichung | 0,012 / 0,030 (unten nur x >= -0,45, dahinter Hals) | <= 0,03 | ok |
| Nasenruecken | -20,8 Grad | -22 +-8 | ok |
| Stirn ueber dem Absatz | 66,4 Grad | >= 60 | ok |

### 3.3 Teile (SPEZ 4.2)
Ohr D 0,245, Dicke 0,09, Mitten-Abstand 0,70, Mitte (-0,32/+-0,35/0,26), Normale (0,85,0,35,0,40) (= Soll). Augenabstand 0,307
(0,30 +-0,02), Oeffnung 0,056 x 0,043 (Soll), Augapfel 0,010 tiefer als der Rand (0,01-0,02). Nase 0,166 x 0,100 (0,165 x 0,105), steht
0,017 W vor der Schnauze. Schnauze am Absatz 0,156 (0,18 +-0,03 ok); Schnauzenbreite an der Nase: Netzbreite der Schnauze 0,30-0,33
(Parameter `sn_breite`), die helle Zone der Textur deckt 0,33; die Mess-Schicht in `mess_baby.py` (Punkte |z - Nase| < 0,01, x > 0,08)
liefert 0,224, weil dort die Schnauze schon in die Wange uebergeht (Messart, keine Formluecke). Mund geschlossen mit Gaumen/Zunge,
Mundwinkel (0,04/+-0,124/-0,244) (Soll (0,03/+-0,13/-0,24)); Kinn an der Unterseite bei x 0,12: z -0,342.

### 3.4 Koerper (Idle Bild 0, Boden)
| Mass | gemessen | Soll | |
|---|---|---|---|
| L | 1,857 m (65,0 cm bei 0,35) | 1,90 +-0,08 m | ok |
| W / L | 0,348 | 0,34 +-0,03 | ok |
| Ruecken / L | 0,527 (34,2 cm bei 0,35) | 0,54 +-0,04 | ok |
| Bauch / L | 0,103 | 0,11 +-0,03 | ok |
| Rumpf B/H | 1,02 | 1,00 +-0,08 | ok |
| Rumpf Breite / L | 0,433 | 0,42 +-0,04 | ok |
| Kopf oben minus Ruecken | +0,005 L | -0,03..+0,08 | ok |
| sichtbarer Hals | 0,008 L | <= 0,08 | ok |
| Pfoten | 0,94 x Erwachsenen-Pfote (= L-Verhaeltnis 1,84/1,957) | +-10 % | ok |

### 3.5 Kein Kragen (gerasterter Umriss, Kopfspalten ausgenommen)
Seite: Stufe max 0,0011 L, Buckel ueber der Geraden Widerrist-Kopf 0,0077 L. 3/4 (az 315): Stufe 0,0011 L (Buckel 0,046 L = normale
Schulterwoelbung, Bild `mess/mess_final_kragen_315.png`). Soll Stufe <= 0,01 L: **ok**.

### 3.6 Landmarken
`landmarken.json` (Kopie `mess/landmarken.json`): Augen, Absatz, Nasenmitte, Nasenspitze, Krone, Ohren, Kinn, Mundwinkel in Spiel-Metern
(Ruhe, Groesse 1,0) + Kopfachse; Abstand jeder Landmarke zur Netzflaeche <= 1,8 mm (Soll <= 5 mm). Hinweis: der Kopf-Rahmen-y zeigt in
der Welt nach rechts (Dump-Raum gespiegelt, `baer_form_baby.py:241`), fuer den symmetrischen Kopf ohne Belang.

### 3.7 Technik ueber den Importer (`log/pruef_glb_final.txt`, Dump `entwurf/dump_final.txt`)
| Pruefung | Ergebnis |
|---|---|
| Laden (Dump.java, JAssImp wie das Spiel) | OK, 26 Knochen, 15 Clips (`log/dump_final.log`) |
| Knochen Name/Eltern/Reihenfolge = Erwachsener | ja |
| Dreiecke | 19.938 (<= 20.000) |
| Einfluesse / Summe | max 4 / 0,99999985..1,00000018 |
| Netz/Material | 1 Netz, 1 Primitiv, kein Material (wie der Erwachsene) |
| NaN | nein |
| Clips: Namen/Dauern | gleich (Abw. 0,0) |
| Dreh-Schluessel | gleich dem Erwachsenen (Abw. 0,0); im GLB 1.560/1.560 Zeit-/Dreh-/Skalier-Puffer byte-gleich |
| Lage-Schluessel | konstant = Junges-Ruhe fuer alle Knochen ausser Becken (Hub x 0,777 + Bodenausgleich) und Translation_Data (*fix1: x 0,777, nicht unveraendert*) |
| Modellmatrizen Importer vs. eigene Rechnung | max 2,6e-5 |
| Offset = inv(Ruhe Junges) | max 4,7e-8 |
| Textur | 1024 x 1024 RGB |

### 3.8 Clips (`mess/clips_final.json`, `log/clips_final.txt`, beide ueber den Importer-Dump)
- **Boden:** je Bild tiefster Punkt Junges minus Erwachsener: alle 15 Clips |d| <= 0,28 cm (Soll <= 1,5) **ok** -- erst nach dem
  Bodenausgleich im Becken (vorher Sitzen -7,1 cm im Boden, Liegen/Tod -5,1, Rennen +-2,6).
- **Dehnung (sigma1, p99,5 je Clip), Junges-Koerper gegen Erwachsener:** Idle 1,35/1,21; Eat 2,28/1,62; Walk 2,91/1,87; Run 3,67/2,07;
  Sit 2,60/2,00; SwipeL 4,41/2,60 (alle Clips in der Datei). Soll <= Erwachsener + 10 %: **nicht erreicht**. Ursache gemessen: die
  Dreiecke mit sigma > 3 sitzen an Bauch/Achsel/Leiste (Rumpf-Gewichte nahe den Beinen, z ~0,22 m); die unterschiedliche Skalierung
  (Rumpf quer 0,86/hoch 0,94, Beine laengs 0,74) kippt in der Ruhe 34 Dreiecke um. Kopf/Hals: Kopfteile starr (sigma 1,00), Hals p99,5
  1,7-2,8.
- **Sichtbar** (`bilder/C_clips_pruefung.png`, Ton): Fressen (Kiefer 15 Grad) und Maul (34 Grad) oeffnen ohne Loch, Inneres dunkel,
  Zunge; Gehen/Rennen/Sitzen ohne Risse; am Nacken nur eine Falte (kein Spalt mehr).

### 3.9 Textur (`log/textur_uv_final.txt`)
- UV: Kopf (U, J, Ohren) 61,0 % der genutzten UV-Flaeche (Soll >= 30 %); Gesicht vorn 313 x 381 Texel (>= 256 x 256); Augenoeffnung
  30 x 30 Texel (>= 14); Augen, Nase, Mund liegen ganz auf EINER Karte (keine Naht).
- Zonen-Median gegen SPEZ 4.3: Gesicht (95,71,61) [Grenze +15 R], Stirn oben (111,87,76), Wange (88,60,43), Augenring (57,44,39),
  Schnauze oben (147,124,112), seitlich (143,113,94), Nase (29,25,24), Iris (28,24,24) + Glanzpunkt, Ohr Mulde (28,15,10), Rand
  (143,111,92), Haare (124,95,77), Unterlid (151,150,155), Maul innen (45,26,26), Zunge (127,69,71), Koerper (70,53,50): alle in
  Toleranz **ausser "ueber dem Auge" (57,43,36) statt (73,54,46)** (913 Texel, -16).
- Helle Spitzen im Kopffell 8,5 % (Ziel 10-15 %).
- Die Textur malt keine fehlende Form: Stirnwoelbung, runde Augen, Nase, Mund sind im Ton-Bild vorhanden (R6 Ton | Textur).

## 4. Weg ins Spiel (vorbereitet, NICHT eingebaut)

Empfehlung wie SPEZ 3.5 (Weg A, Vanillas Jungtier-Weg, SPEZ 3.1/3.2 belegt): eigenes Netz `NCBearCub.glb` mit eigener Tierart `bearcub`
(Stufe -> `bear`), `animset = "buck"`. **Der Entwurf zeigt, dass die Clip-Kopie per Skript geht:** `baer_export_baby.py` erzeugt sie
schon (Drehungen byte-gleich, Lagen neu, Bodenausgleich je Bild); der Importer liest sie fehlerfrei und rechnet dieselben Matrizen.
Dateien fuer B1 (Pfade wie der Erwachsene):
- `42/media/models_X/Skinned/NCBearCub.glb` (= `entwurf/NCBearCub.glb`), `42/media/textures/Body/NCBearCub.png` (= `entwurf/NCBearCub.png`).
- Skript (module Base, wie `nc_bear_tier.txt:3-15`): `animationsMesh NCBearCub { meshFile = Skinned/NCBearCub.glb, keepMeshAnimations = true }`,
  `model NCBearCub_Body { mesh = Skinned/NCBearCub.glb, animationsMesh = NCBearCub, shader = animalEffect, ... }` -- Felder wie beim Erwachsenen.
- Definition (SPEZ 3.7): Art `bearcub` (bodyModel `NCBearCub_Body`, animset `buck`, Stufe -> `bear`, minSize 0,35 / maxSize 0,75),
  `textureBaby = "NCBearCub"` in der Rasse; Erwachsenen-minSize gegen den 1,3-Sprung (SPEZ 3.2).
- Namensprobe 10.11.: `bearcub|NCBearCub|BanditsNPCBearCub` in `NPCCrew/42/media/lua` 0 Treffer, in Vanilla `media/lua`+`media/scripts`
  0 Treffer. Spaeter in NPC Crew: `BanditsNPCBearCub.glb/.png` (SPEZ 3.6).
- **Offen fuer B1 (Kevins Wort):** Weg/`Translation_Data` (heute Erwachsenen-Weg, Junges gleitet bei 0,35; SPEZ 3.3 Punkt 4), Uebergabe
  von modData beim Stufenwechsel, `isBaby`-Nebenwirkungen, Halbstark mit Junges- oder Erwachsenen-Modell, MP.

## 5. Befehle zum Wiederholen (alle aus `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby`)

```
python werkzeug/koerper_mass.py                                   # TL/FH (stehen in baer_form_baby.py:42)
"C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe" --background --factory-startup \
   --python C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_netz_baby.py -- C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/netz/final.npz netz/final.json
python C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_textur_baby.py netz/final.npz entwurf/NCBearCub.png tex/final_zonen.npz
python C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/baer_export_baby.py netz/final.npz entwurf/NCBearCub.glb
JB=C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin; G="C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"; H=C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness
"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/entwurf/NCBearCub.glb C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/entwurf/dump_final.txt skin
python werkzeug/pruef_glb.py entwurf/dump_final.txt netz/final.npz mess/pruef_glb_final.json
python werkzeug/clip_pruef.py entwurf/dump_final.txt.pkl netz/final.npz mess/clips_final.json
python werkzeug/mess_baby.py netz/final.npz mess/mess_final.json mess/landmarken.json
python werkzeug/render_vorbereiten.py render/final/ein.json
bash werkzeug/gpu_render.sh werkzeug/render_baby.py render/final/auftrag.json log/render_final.log   # Sperre gpu.lock, wartet auf fremdes Blender
python werkzeug/blaetter_final.py                                  # bilder/ + intern_vorlage/
```

## 6. Nicht erreicht, offen, ungeprueft

1. **Hautdehnung Koerper** in den Clips (3.8): nicht im Soll. `falten_glaetten` (`baer_form_baby.py:557`, glaettet nur umgekippte
   Dreiecke) probiert: umgekippte 34 -> 8, p99,5 teils besser, aber Hoechstwerte schlechter (bis 182) -> verworfen. Abhilfe fuer B1/2c:
   Bein-/Rumpf-Faktoren angleichen oder Gewichte an Achsel/Leiste neu (das macht Lauf 2c ohnehin am Koerper).
2. **"ueber dem Auge"** 16 zu dunkel (kleine Zone am Augenloch).
3. Der Koerper ist der heutige Stand mit Junges-Proportionen: Hinterfuss, "Hose in Stiefeln", Sitzhaltung, breiter Rumpf aus Lauf 2c
   sind NICHT drin. Die Pfoten sind Erwachsenen-Pfoten x 0,94 (wirken beim Jungen gross).
4. Kopffell: Straehnen in Haarstrich-Richtung, wirkt "wollig"; der Kopf wirkt neben dem Koerperfell (Erwachsenen-Textur) etwas dunkler
   und kuehler -- gemessen liegen beide im Soll. Ohren/Stirn ohne einzelne Haarbueschel.
5. Kopfform von der Seite ist aus dem Frontfoto geschaetzt (SPEZ 1.4); Kevins Blick auf R3/R6 entscheidet.
6. Weg (`Translation_Data`) x 0,777 (*Berichtigung fix1*, Schalter `WEG_FAKTOR`), Clip-Dauer unveraendert (B1, Kevins Wort). Bodenausgleich = tiefster Punkt wie beim Erwachsenen (nicht
   je Stuetzpfote einzeln).
7. Standbild-Pose R1 (`werkzeug/posen.json`) ist nur fuers Bild, kein Clip.
8. Nicht gespielt; nichts davon ist in der Test-Mod.

## 7. Dateien (`C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/`)
- `entwurf/NCBearCub.glb`, `entwurf/NCBearCub.png`, `entwurf/dump_final.txt(.pkl)`; `netz/final.npz` + `netz/final.json` (Parameter);
  `landmarken.json`; `mess/*.json`, `log/*`.
- Fuer Kevin: `bilder/R1_vorn_liegend_wie_foto.png`, `R2_dreiviertel_stehend.png`, `R3_seite.png`, `R4_sitzen.png`,
  `R5_spielkamera_577.png` (100 % ansehen), `R5_spielkamera_289.png`, `R5b_wechsel_bei_075.png`, `R6_kopf_nah.png`, `C_clips_pruefung.png`;
  Einzelbilder `render/final/`.
- **Nur intern (zeigen die Vorlage, nie weitergeben):** `intern_vorlage/vergleich_R1_foto.png`, `vergleich_R6_foto.png`,
  `form/foto_t*.png`, dazu die SPEZ-Blaetter `vergleich_ton_foto.png`, `referenz/`.
- Zwischenstaende: `netz/n*.npz`, `form/`, `render/t*`, `render/x13*`, `render/l1`, `render/h2|h3`, `tex/`.
