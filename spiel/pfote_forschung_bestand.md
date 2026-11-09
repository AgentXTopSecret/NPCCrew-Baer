# Lauf baer-pfote, Forschung BESTAND: warum unsere Pfoten wie ein abgesaegtes Bein aussehen (09.11.2026)

Statisch/offline gemessen und gerendert, nicht gespielt. Grundlage: heutiges GLB der Test-Mod
(`NCBearTest/42/media/models_X/Skinned/NCBear.glb`, MD5 2a4837f6e8f41d97e07c76b2353b5520), ueber den Spiel-Importer gelesen
(`Dump.java`; `bestand/dump_pruef.txt` frisch erzeugt und byte-gleich zu `bestand/dump_heute.txt`). Masse in Spielmetern, Tier-Rahmen
x vorn, y links, z oben. Nichts in Test-Mod, NPC Crew oder baer_fell geschrieben; Originalskripte nicht geaendert.

## 0. Kurz

**Kevin hat recht, und die Ursache ist die Bau-Kette, nicht die Textur.** Das Spielnetz ist keine modellierte Haut, sondern eine
**Fellhuelle**: die Hochmodell-Haut wird bis zu 7,1 cm nach aussen geschaelt (an Bein und Pfote gleich dick) und dann **am Boden flach
abgeklemmt**. Dadurch wird das Bein eine 34-36 cm dicke Saeule bis zum Boden; ihr flacher Boden-Schnitt IST die Sohle (41 x 23 cm hinten,
28 x 21 cm vorn) und ist schmaler als das Bein darueber. Die Zehen sind im Hochmodell eigene kleine Objekte, die beim Schaelen nur
~0,9 cm Huelle bekommen - sie versinken in der Saeule und schauen nur 4-7 cm vorn heraus. Im Sitzen dreht der Fuss die flache Kappe nach
vorn: das ist Kevins "Saeule mit Kappe, Zehen oben drauf". Die Sohlen-Textur (baer-fell) ist auf diese Kappe gemalt.

**Machbar ohne Clip-Aenderung** fuer Stehen, Sitzen (Sohle zeigt nach vorn, 5 Grad ueber waagerecht), Aufrichten (Hinterfuss die ganze
Zeit flach) und Liegen - aber nur, wenn (a) die Pfote im Hochmodell ein eigener Fuss aus einem Feld wird UND (b) die Fellhuelle an der Pfote
duenn wird (Bein verjuengt sich) UND (c) die Hautgewichte am Sprung-/Handgelenk statt nach Hoehe verteilt werden. Grenze der Clips:
im Gehen/Rennen stecken die Pfoten schon heute 1,5-3,0 cm im Boden (Fuss starr, `Toe0` dreht nie); der neue Fuss darf also nicht laenger
werden als heute (Ferse/Zehen/Krallen innerhalb der heutigen Huelle), sonst tiefer als heute.

## 1. Wo die Saeule mit Kappe entsteht (Code, Belege)

### 1.1 Hochmodell `baer/spiel/baer_quelle_anim.py`
- **Beine** sind Metaball-Ketten im Rumpf (`:897-905`): Vorderbein `chain(..., 0.30/0.235)`, `(..., 0.25/0.205)`, dazu eine "Pranken"-Kette
  `(0.37,0.31,0.10)->(0.47,0.285,0.075)` r 0,20->0,17 (`:901`); Hinterbein entsprechend, Fuss-Kette `(-0.75,0.33,0.10)->(-0.47,0.32,0.075)`
  r 0,195->0,17 (`:905`). Danach Voxel 5,2 cm, glaetten (`:916-926`), zwei Stufen Catmull-Clark -> `baer_koerper_rund` (`:934-947`), das liest
  das Spielnetz. Ergebnis (Haut ohne Fell, `bestand/quelle_messen.log`): Bein rund 20 cm dick bis 5 cm ueber dem Boden; hinten unten eine
  schmale "Wurst" 31 x 16 cm, vorn 21 x 17 cm; unten rund, bis 0,9-1,2 cm unter den Boden.
- **Zehen = eigene Objekte, angesetzt:** `PFOTEN` (`:1482-1485`, Mitte xc/yc, Groesse g 1,0 vorn / 0,82 hinten), `zehen_lage` (`:1488-1498`,
  fuenf Zehen im Bogen), `zehen_feld_fn` (`:1501-1516`: Ellipsoid-Sohle 0,145g x 0,132g x 0,066g, fuenf Kapseln, Zehenballen, Sohlenballen,
  Boden-Schnitt), `pfote_bauen` (`:1519-1559`) baut daraus ein eigenes Netz `zehen_<Knochen>` und haengt es STARR an den Knochen
  (`on_bone`, `:1531`, `:1265-1274`); kein gemeinsames Feld mit dem Bein. Masse in Spielmetern: Zehen-Objekt hinten x -0,384..-0,195,
  17,4 cm breit, 8 cm hoch; vorn x 0,292..0,523, 21,3 cm breit, 9,8 cm hoch (`bestand/quelle_messen.log`).
- **Krallen** (`krallenpfad` `:828-838`, `rohr` `:791-825`) als Roehren vor den Zehen, ebenfalls starr am Knochen (`:1557-1558`).
- **Fell an den Pfoten:** Beinfell kuerzer zum Boden (`l_bein` 0,26..1, `:1610`), kein Beinfell auf den Zehen (`:1601-1602`), Zehen eigenes
  kurzes Haar 1,1-6,3 cm nach vorn-unten (`:1720-1741`). Wirkt auf Texturansichten; die Form der Spielpfote bestimmt es nicht (1.2).
- **Knochen im Hochmodell** (`:1186-1192`): `fuss` (-0,72/0,13)->(-0,42/0,06), `pranke` (0,35/0,13)->(0,56/0,06) (Hochmodell-Masse);
  sie bewegen nur das Hochmodell, das Spielskelett kommt aus `baer_kampf_fell.py` (1.4).

### 1.2 Weg ins Spielnetz `baer/spiel/baer_export_fell.py`
1. `huelle_bauen` (`:658-725`): Rumpfhaut + Nase + alle `zehen_*` als lose Teile zusammen, EIN Voxel-Remesh 8,5 mm (`:674-685`) - die Zehen
   werden nur "zusammengeschmolzen", keine weiche Verbindung.
2. **Schaelen** (`huelle_schaelen` `:242-269`): jeder Punkt wandert entlang der Normalen nach aussen, solange er in allen Fell-Ansichten
   (`_arbeit/baer_spiel/ansichten/`, 07.11.) im Fell liegt und unter `dlim` bleibt. **`dlim` an den Beinen = 0,112-0,022+0,005 = 0,095 m
   Hochmodell = 7,1 cm Spielmass** (`:695-696`), gleich fuer Unterschenkel, Ferse und Fussruecken; nur nahe an den Zehen-Objekten
   `0,012 + 1,05 x Zehenabstand` (`:697-698`) -> Zehen ~0,9 cm. Gemessen (Schnittkurven, `bestand/schnitt_mass.txt`): Hochmodell-Haut in
   20 cm Hoehe 20,6 x 19,6 cm (vorn) / 21,1 x 19,9 cm (hinten), Spielnetz 34,2 x 34,3 / 36,4 x 34,7 cm = **+6,7..7,6 cm je Seite**, also
   genau die `dlim`-Grenze (in 10 cm +4,4..6,4 cm).
3. **Bodenklemme**: `W[:, 2] = max(W[:, 2], ZMIN_ALT)` (`:724`), nochmals nach Glaetten/Form (`:1172`, `:1178`) und in Spielmetern
   (`:1385`). Alles, was die Huelle unter den Boden schiebt, wird flach - **das ist die Kappe**; ihr Umriss ist der Bein-Querschnitt am Boden.
4. Zweites Remesh 9,5 mm, Taubin, Falten (`:1146-1171`; Zehen nur 25 % geglaettet `:1159`), Verringern auf `RUMPF_ZIEL` 14.500 (`:74`,
   `:1333-1338`); Kopf (alte Punkte, UV, Texel) und Krallen (alte Schalen, `:1392-1398`) unveraendert aus dem alten FBX.
5. `sohlen_bauen` (`:897-1049`): nimmt die flache Scheibe (Dreiecksmitte < 1,2 cm UND Normale z < -0,6, `:917`), trianguliert sie IN DER
   EBENE neu (`delaunay_2d_cdt` `:1001`) und hebt die Furchen um 8 mm (`BALLEN_HUB` `:802`, `hoehe` `:891-894`). Ballen-Plan aus der
   Krallenlage (`ballen_plan` `:848-869`). Die Kappe bleibt eine Kappe, nur mit 8 mm Relief; Textur prozedural darauf (`sohle_layout`).

### 1.3 Masse heute (GLB, Ruhe; Schnitte `bestand/schnitt_mass.txt`, Abdruck/Gelenke `bestand/pfote_mass.txt`, deckt sich mit `bestand/messen_glb.txt`)
| | Sohlenabdruck (z < 1 cm) L x B | Bein in 10 cm L x B | in 20 cm L x B | in 30 cm | Zehen vor der Beinfront | Sohle L / Bein L (20 cm) |
|---|---|---|---|---|---|---|
| VL | 28,5 x 20,9 cm | 30,7 x 29,0 | 34,2 x 34,3 | 38,1 x 38,3 | 4,4 cm | 0,83 |
| HL | 41,0 x 22,9 cm | 38,8 x 31,1 | 36,4 x 34,7 | 41,1 x 39,1 | 6,5 cm | 1,13 |
(VR/HR gleich +-1 cm.) Kennzeichen der "abgesaegten" Form: (1) das Bein ist ueber der Sohle **breiter als die Sohle** (in 10 cm hinten
31,1 gegen 22,9 cm, vorn 29,0 gegen 20,9 cm) - der Rand ueberhaengt die Kappe; (2) Hinterkante senkrecht bis zum Boden (HL x -0,605 am
Boden, -0,634/-0,635 in 10/15 cm: die Ferse steht NICHT heraus); (3) Vorderkante ab 10 cm senkrecht (HL -0,246..-0,263), darunter nur
ein 6,5 cm Zehenwulst; (4) Fusslaenge kaum groesser als die Beindicke (1,13 hinten, 0,83 vorn). In Kevins Vorlage ragt die Sohlenplatte deutlich
aus dem Bein, ist etwa 1,8-mal so lang wie breit (am Foto geschaetzt, ungenau) - das Verhaeltnis L/B unserer Hintersohle (41/23 = 1,8)
stimmt sogar, nur sitzt sie als Stirnflaeche unter einer gleich dicken Saeule.

### 1.4 Knochen und Gewichte (`baer/spiel/baer_kampf_fell.py`)
- Spielknochen (`:88-102`): Sprunggelenk `FERSE` (-0,48/0,247/**0,10**) -> Ballen `BALLEN_H` (-0,25/0,24/0,045) -> `ZEHE` (-0,19/0,03);
  Handgelenk `HAND` (0,32/0,23/**0,10**) -> `BALLEN_V` (0,48/0,22/0,045). Gegen die Sohle: hinten 13,2 cm Sohle hinter dem Gelenk, 29,0 cm
  davor; vorn 10,7 / 20,5 cm (`pfote_mass.txt`). Lage passt zu einem echten Fuss (Gelenk 10 cm hoch, Ferse dahinter, Fuss nach vorn).
- **Gewichte nach Hoehe statt nach Gelenk:** `w_fu = 1 - sst(0,055, 0,175, z)` (`:1734`): unter 5,5 cm 100 % Hand/Foot, bis 17,5 cm
  Uebergang zu Unterarm/Unterschenkel, egal ob ein Punkt vor dem Gelenk (Fussruecken) oder dahinter (Ferse) liegt. Krallen starr an
  Hand/Foot (`:1741-1746`). `Toe0` ist im Baeren-GLB gewichtslos; die Optimierung (`baer_gewichte_fell.py:96`, `z_pfote=0,06`) laesst alle
  Punkte unter 6 cm auf der Formel. Fuer einen echten Fuss muss die Formel am Gelenk trennen (siehe 4).

## 2. Clips (heutiges GLB, jedes Bild; `bestand/pfote_mass.txt`, `bestand/spielraum2.txt`, Gegenrechnung zu `bestand/messen_glb.txt`)
Fussrichtung hinten aus den Gelenkpunkten Foot -> Toe0 (beide aus den Clip-Matrizen), vorn Hand-Matrix auf HAND->BALLEN_V; Sohle = Normale.
| Clip | Vorderpfote: Fuss zum Boden / Sohle | Hinterfuss: Fuss zum Boden / Sohle | Sohle sichtbar? |
|---|---|---|---|
| Idle (Stehen) | -18,9 / -90 | -13,4 / -90 | nein (steht) |
| Walk | -72,6..-12,4 / bis -36 | -53,3..-6,4 / bis -50 | kurz von hinten unten |
| Run | -86,6..-12,9 / bis -19 | -71,3..-6,4 / bis -32 | kurz von hinten |
| **Sit** (Bild 60) | -18,9 / -90 (flach am Boden) | **+81,4 / +5,0, Richtung +-34 Grad** | **ja, Hintersohlen nach vorn-aussen** |
| SitDown/StandUp | flach | -13,9..+81,4 / -90..+5 | im Uebergang |
| **Rear** | -32,7..-0,9 / -90..-71 (in der Luft, Sohle nach unten) | -13,4 / **-90 die ganze Zeit** | Hinterfuss steht ganz auf |
| Dead (Liegen) | -49/-36 / -15/-29 (seitlich) | -35/-26 / -17/-32 (seitlich, zur Bauchseite) | ja, von der Bauchseite |
| Slam / SwipeL/R | -25,9..+10,4 / bis -61 (Slam), -32 (Swipe) | flach | Pranke kurz beim Swipe |
`Toe0` dreht in keinem Clip und keinem Bild gegen `Foot` (Abweichung <= 3e-7, `spielraum2.txt`): die Zehen koennen nicht abrollen.

## 3. Bilder (GPU-Regeln eingehalten: Spiel lief nicht, eigene Sperre `gpu.lock`, kein fremdes blender.exe, RTX 4090 OptiX + Entrauscher)
- `bilder/bestand_pfoten.png`: Kevins Hauptvorlage (nur Vergleich) + je Pose (Stehen, Gehen, Sitzen, Aufrichten, Liegen) Gesamtbild im
  Spielwinkel (Textur), Seitenbild Ton, alle vier Pfoten nah in Ton und Textur.
- `bilder/bestand_pfoten_spiel.png`: alle vier Pfoten im Spielwinkel (el 30, Diagonale), Ton und Textur.
- `bilder/bestand_hoch_gegen_spiel.png`: Hochmodell-Haut gegen Spielnetz in Ruhe, gleiche Kamera (Hinter-/Vorderbein von links, von
  vorn, von unten).
Angesehen: Stehen = Saeulen mit Krallensaum, Ferse unsichtbar; Gehen = angehobene Sohle ist eine flache dunkle Scheibe; Sitzen = grosse
ovale flache Kappe, die Zehen als schmaler Klumpen oben drauf (schmaler als die Kappe - umgekehrt zum echten Fuss); Aufrichten = vordere
Pranke von unten eine Platte mit Krallensaum, hinten Saeulen; Liegen = Saeule mit schraeg abgeschnittenem Ende. Im Hochmodell (ohne Fell)
hat der Hinterfuss noch Ferse und Fussruecken - die Huelle fuellt beides zu. Mit Textur sieht man dieselben Formen (Sohle gemalt auf der Kappe).
Einzelbilder: `bestand/render/` (90), `bestand/render_hoch/` (12).

## 4. Machbarkeit

**Neuer Aufbau (Vorschlag fuer den Bau):**
1. `baer_quelle_pfote.py`: Fuss-Ketten der Metaballs (`:901`, `:905`) weg, Unterschenkel/Unterarm zum Gelenk hin duenner; je Pfote EIN
   Abstandsfeld (wie `zehen_feld_fn`, aber vollstaendig): Gelenk-Kapsel ab ~15 cm Hoehe, Ferse (hinten rund), flache Sohlenplatte,
   querliegender Ballen, fuenf Zehen im Bogen (aussen weiter gespreizt als die Ferse breit), vorn zusaetzlich Handwurzelballen; weich (smin)
   in die Beinkapsel uebergehend. Das Feld ersetzt `zehen_*` als Teil fuer die Huelle; Krallen an die neuen Zehen versetzen (Form gleich).
2. `baer_export_pfote.py`: `dlim` aus einem Pfotenabstand: auf dem Fuss ~1-1,5 cm (kurzes Fell), am Unterschenkel von ~2-3 cm am Gelenk auf
   die heutigen 7 cm am Knie steigend (statt ueberall 7,1 cm). Die Bodenklemme bleibt (Auflage z = 0), schneidet dann aber nur ~1 cm
   der eigenen flachen Sohle ab. Taubin/Falten an der Pfote schwach (Zehenspalten bleiben), beim Verringern Pfoten weniger stark
   reduzieren (Gruppe wie `frei`). `sohlen_bauen` kann bleiben (findet die Sohle weiter ueber z < 1,2 cm und Normale nach unten).
3. Gewichte (`baer_kampf_pfote.py` Formel + `baer_gewichte_pfote.py`): Foot/Hand = alles unter der Gelenkebene vor und hinter dem Gelenk
   (Ferse, Fussruecken, Zehen), Calf/Forearm darueber, schmales Band am Gelenk; `z_pfote` -> Gelenkmaske. Kopfprobe muss versetzte Krallen
   erlauben (heute "456/456 bit-gleich", `fix/log/lauf1.txt`).

**Wo die Clips nicht reichen** (starre Punkte am Fussknochen durch alle Bilder, `bestand/spielraum2.txt`; heute = tiefste Pfotenhaut/Kralle):
| Punkt (Ruhe) | Walk | Run | Sit | SitDown/StandUp | heute Walk/Run |
|---|---|---|---|---|---|
| Ferse Sohle x -0,58 / -0,62 / -0,64, z 0 | -2,0 / -2,5 / -2,8 | 0 | 6,5 / 2,5 / 0,5 | 0 / 0 / -1,7,-1,2 | Haut hinten -1,7 / -1,5 |
| Ferse gerundet x -0,62 / -0,64, z 0,06 | +3,4 / +3,2 | +6 | 2,0 / 0,0 | 1,4 / -0,6 | |
| Zehe hinten x -0,20 / -0,18, z 0 | -1,7 / -2,5 | -1,9 / -3,0 | 44 / 46 | 0 | Krallen hinten -2,1 / -2,6 |
| Vorderpfote Handwurzel x 0,18 / 0,24, z 0 | -1,7 / -1,0 | -0,7 / 0 | 0 | 0 | Haut vorn -0,7 / -0,8 |
| Vorderzehe x 0,52 / 0,56, z 0 | -1,2 / -2,8 | -1,4 / -3,4 | 0 | 0 | Krallen vorn -2,4 / -3,0 |
Folgerung: Ferse flach nicht weiter als x -0,58, gerundet bis ~-0,63 (in 3-6 cm Hoehe); dann bleibt im Sitzen ~1-2 cm Luft unter der
Ferse (Vorlage: Ferse liegt auf) - ohne Clip nicht ganz zu schliessen, x -0,64 waere in SitDown/StandUp 0,6-1,7 cm im Boden. Zehen am
Boden nicht weiter vorn als heute (Haut hinten bis x -0,19, vorn 0,52) und nach vorn hochgerundet (ein Bodenpunkt bei -0,20 / 0,52 liegt
schon 0,4-0,5 cm tiefer als die heutige Haut); Krallen nicht weiter nach vorn (heute vorn x 0,561, hinten -0,174). Handwurzelballen
vorn muss hinten angehoben sein (~1,5 cm), sonst tiefer als heute. **Vorschlaege fuer die Clip-Runde:** `Toe0` im Gehen/Rennen abrollen
lassen (Zehen stecken heute 1,5-3 cm im Boden), im Sitzen Unterschenkel ~2 cm tiefer (Ferse auf den Boden).

**Was danach neu laufen muss und wie lange** (Zeiten aus `baer_fell/fix/log/lauf1-3.txt`, Logzeiten, `baer_spiel/ansichten.log`):
Fell-Ansichten des Hochmodells fuer die Huelle (GPU ~6 min; Stufe `ansichten` gibt es nur in `baer_export.py:160`, muss in die
Kopie, weil die alten Ansichten den neuen Fuss nicht kennen) -> `netz` ~2,5 min -> `fbx`+`kopfprobe` ~10 s -> `formel` ~35 s -> `gewichte`
12-15 min CPU -> `messen`/Dehnung ~1 min -> `glb`+Dump+`glb_pruef` ~1 min -> `karten` ~1 min -> Textur-Ansichten GPU ~5+2 min -> `backen`
~70 s (Sohlen-Textur neu nach `sohle_layout`) -> `body`+GLB ~40 s -> `deer` (NCBearDeer.glb) ~1 min -> Pruefbilder ~30 s je 90 Bilder.
**Ganze Kette ~35-40 min Maschinenzeit** (GPU ~13 min); Form-Runden nur mit Formel-Gewichten und Ton-Bildern ~5 min je Runde. Die
eigentliche Arbeit ist das Pfotenfeld selbst (mehrere Form-Runden).

**Dreiecke:** heute 18.930 = Rumpf 14.499 + Sohlen netto +890 (1.668 statt 778 Scheiben-Dreiecke) + Kopf 2.295 + Krallen 832 + Maul 414
(`baer_fell/fix/netz/log/netz.log`, `fell_forschung_bestand.md:135`); je Pfote 943-992 Hautdreiecke mit Hand/Foot-Gewicht > 0,5, davon
Sohle 374-461; Kantenlaenge Pfote im Mittel 18 mm, Rumpf 27 mm. Spielraum bis 20.000: 1.070. Vorschlag ~1.100-1.200 je Pfote (Zehen-
spalten), bezahlt durch Sohlen-Raster 15 -> 20 mm (`RASTER` `:805`, ~-600 gesamt), `RUMPF_ZIEL` 14.500 -> 14.000 (-500) und die duennere
Beinwand (weniger Umfang). Ziel ~19.500-19.900. Geschaetzt, nicht gebaut.

## 5. Dateien (alle unter `_arbeit/baer_pfote/`)
`bestand/pfote_mass.py|.txt` (Abdruck, Gelenke, Fusswinkel, Ziele; Breiten dort aus Punkten im 1-cm-Band, zu duenn besetzt - fuer Breiten gilt
`bestand/schnitt_mass.py|.txt`), `bestand/spielraum2.py|.txt` (Spielraum, Toe0), `bestand/auftrag_bestand.py|.json`,
`bestand/blatt_bestand.py`, `bestand/hoch_gegen_spiel.py`, `bestand/blatt_hoch.py`, `bestand/dump_pruef.txt`; Werkzeug-Kopien
`werkzeug/render_optik.py` (nur dumpread-Pfad), `werkzeug/dumpread.py`, `werkzeug/gpu_render.sh` (eigene Sperre + Pruefung auf fremdes
Blender). Vom abgebrochenen Anlauf nach Pruefung weiterverwendet: `dump_heute.txt` (byte-gleich zu frischem Dump), `quelle_messen.*`
(Knochen passen zur Abbildung `:59`), `messen_glb.*` Schnitte und Clip-Winkel (decken sich mit meiner Messung), `spielraum.*` (Werte
nachgerechnet, z. B. Ferse -0,58: Walk -2,0, Sit 6,5). Nicht verwendet: das "Seitenumriss"-Profil in `messen_glb.txt` (unplausibel,
z. B. 0,8 cm Hoehe mitten in der Beinsaeule).

## 6. Offen / ungeprueft
- Ob ein geaendertes Metaball-Bein das Voxelgitter des ganzen Rumpfs verschiebt (dann aendert sich die Huelle ueberall leicht) - ungeprueft.
- Vorlagen-Verhaeltnisse (Sohle ~1,8 x so lang wie breit) nur am Foto geschaetzt; kein Netz-Recherche-Auftrag in diesem Schritt.
- Dehnung am duenneren Gelenk (Walk: Knick Unterschenkel/Fuss 69-110 Grad, Run 55-105; Handgelenk 6-56) erst nach dem Bau messbar.
