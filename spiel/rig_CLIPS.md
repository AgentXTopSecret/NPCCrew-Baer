# CLIPS -- Lauf baer-rig-junges, Rolle CLIPS+EXPORT (11.11.2026)

**Statisch geprueft, nicht gespielt.** Nichts in Test-Mods, NPC Crew, Spiel oder `_arbeit/baer_zaehmen/mod/` geschrieben; kein git, kein
Download. Alle Zahlen bei Groesse 1,0 (das Spiel skaliert auf 0,35), Rahmen tier (x vorn, y links, z oben, Boden z 0), aus dem
**Importer-Dump des fertigen GLB** (`rig/clips/dump_final.txt(.pkl)`), wo nicht anders gesagt.

> **NACHBESSERUNG 11.11.2026 -- dieser Bericht beschreibt den Stand VOR der Nachbesserung** (jetzt in `rig/out_vor_fix/`, GLB d89856ef).
> Neuer Stand: `rig/out/` GLB ee7a0cce / PNG 92a829fa, Bericht `rig/NACHBESSERUNG.md` (Death/Dead liegen, Sitz ohne Durchdringung,
> Eat Kopf vorgestreckt, Ohrmuschel heller). Berichtigungen dieses Berichts (PRUEF_TECHNIK M7):
> 1. Abschnitt 0/5 C1 "Death ... der Koerper liegt dabei auf" stimmte nicht: im alten Stand lag nur die linke Pranke auf, der Rumpf hing
>    14,7-18,9 cm hoch (Messung PRUEF_TECHNIK M1).
> 2. Abschnitt 2/C2 "Dead aufliegend +0,45" waren Hautpunkte der linken Pranke, nicht die Flanke (Rumpf 17,1 cm).
> 3. Abschnitt 8.1.1 "Abhilfe waere ein Abspieltempo je Groesse" hilft nicht: Pfote (1,5 x Groesse x Modell) und Wurzel (1,6 x Weg)
>    skalieren beide mit dem Abspieltempo, das Verhaeltnis bleibt Groesse/0,35. Nur Gang-Clips je Groessenstufe oder Groesse 0,35.
> 4. Abschnitt 5 C4 "Sitz 10-14 Punkte, weiches Anliegen": mit dem Strahl-Test des Pruefers waren es echte Durchdringungen bis 3,3 cm;
>    die 30-%-Kapsel ist zu grob, und `sitz_loesen.py` rechnete mit `rl.Netz()` = Vorab-Gewichte der Rolle SKELETT, nicht mit `gewichte_end.npz`.

## 0. Ergebnis kurz
- **Endergebnis:** `rig/out/42/media/models_X/Skinned/NCBearCub.glb` (MD5 **d89856ef508a0100dbb4e384f0ab4640**, 1.235.544 Byte) und
  `rig/out/42/media/textures/Body/NCBearCub.png` (MD5 **8ce68838b0df138b7bf667b98d687800** = FORM-Abgabe `C_rig_basis.png`), `rig/out/md5.txt`.
- **Harness (Dump.java) laedt es:** 26 Knochen, 15 Clips, 11.811 Punkte, 19.418 Dreiecke, <= 4 Einfluesse, Summe 0,9999999-1,0000002.
  Matrizen des Importers gegen eigene Kette aus den GLB-Schluesseln <= **4,5e-7 E** (alle Bilder aller Clips), inverse Bind gegen Ruhe 3,4e-8 E.
- **Gehen schneller (Kevins Freigabe):** Walk = Trab, **1,603 Kacheln/s** (heute 0,52; Spieler gehend 2,27); Run = Galopp, **2,613 Kacheln/s**
  (heute 2,47 mit Gleiten). Gleiten der Stuetzpfoten **0,0 cm** (Pfoten-Spur waagerecht, Blatt `clips_gang.png`), Pfoten in der Stuetze
  -0,03..+0,73 cm, 0 ueberstreckte Bilder, 0 Durchdringung Bein/Bein. **Gilt fuer Groesse 0,35** -- siehe Risiko 8.1 (Wachsen B1d).
- **Sitzen S_J** neu am Netz geloest: sitzt aufrecht wie Kevins Vorlage (Pranken flach 0,0 cm, Sitzflaeche 0,1, Ferse 0,1 cm, Ellbogen
  167-169 Grad, Hinterfuss-Mitten 0,738 m, Blick Augen-Nase -34,9..-34,0 Grad). Blatt `clips_sitzen.png` (selbst angesehen).
- **Alle festen Regeln eingehalten**, Dehnung je Clip p99,5 <= **2,30** (Grenze 2,6), max <= **3,50** (4,0), Achsel/Brust <= **3,23** (3,5).
  Boden: alle Stuetzpfoten in allen Clips -0,5..+1,24 cm (Grenze 1,5) -- **Ausnahme Death im Kippen** (Abschnitt 5, C1).
- **Offen / ehrlich:** (1) **Eat: die Schnauze erreicht den Boden nicht** (tiefste Kopfhaut 42 cm bei 1,0 = 15 cm im Spiel) -- mit keiner
  erlaubten Abweichung (D.5) moeglich, Frage an Kevin. (2) Death: im Kippen hebt die schmalere Spur die Stuetzpfoten bis 6,7 cm (der Koerper
  liegt dabei auf, Schweben des ganzen Tiers <= 0,77 cm). (3) Sitz-Trio: Innenseite Unterschenkel beruehrt den Unterarm (10-14 Punkte in der
  groben 30-%-Kapsel). (4) Wachsen (B1d, andere Sitzung) zeigt das Junge bis Groesse 0,75 -- dann gleiten die Pfoten (Risiko 8.1).

---------------------------------------------------------------------------------------------------------------------------

## 1. Neue Clips (Generator `baer/spiel/baer_clips_rig.py`, Kopie von `baer_kampf_junges.py` Zeilen 1-1702, geaenderte Stellen "RIG")
Skelett `rig/skelett/skelett_rig.json` (ruhe_m). Ausgabe Posen `rig/clips/clips_neu_posen.npz` -> `rig/werkzeug/wandle.py` ->
`rig/clips/clips_neu.npz` (lokale Drehungen Dump-Raum, Becken-Lage, Weg). Lage-Schluessel gegen lage_E max 2,6e-6 E; Walk/Run/Sit erstes =
letztes Bild bit-gleich (ohne Weg).

### 1.1 Walk = Trab (RIG_PLAN 5.3), 28 Bilder, 3 Zyklen a 9 Bilder (3,33 Hz)
| Groesse | Plan | gebaut | Grund |
|---|---|---|---|
| S (Stuetzweg H/V) / duty | 0,64 / 0,38 | **0,53 / 0,3148** | Plan-Werte (Suche `rig/clips/suche` v1): 6 Bilder ueberstreckt, Becken wippt 4,31 cm (> 4), Hinterfuss faehrt durch Unterarm/Pranke derselben Seite (185 Punkte; kurzer Rumpf L/H 1,2). Gleiches S/duty = gleiches Tempo ohne Gleiten ("fliegender Trab"). S 0,56 / 0,55 / 0,54: 3 Bilder ueberstreckt oder Durchdringung (v1-v4). |
| mitte H / V | 0,04 / -0,02 | 0,0 / 0,0 | Abstand Vorder-/Hinterpfote derselben Seite |
| ab H / V (Abrollen) | 30 / 28 | 22 / 22 | Abrollpunkt neu: Zehenansatz unten (vorn x 0,395 / z 0,006, hinten -0,330 / 0,007), nicht Toe0 (8 cm hoch: Sohlenspitze tauchte ein). Mit 30 Grad hob die Sohle hinter dem Abrollpunkt > 1,0 cm. |
| spitze H / V (Pfote im Schwung) | 45 / 60 | 35 / 40 | die runde Generator-Pfote sah im Schwung wie ein Haken aus (Diag-Render); Messung gleich (v6) |
| Vorderpfote hebt steil ab | -- | m0 V 0,3, hexp V 0,6 | sonst laeuft sie nach dem Abheben weiter nach hinten in die Bahn des Hinterfusses |
| kontakt, hub, aussen, senk, streck, Rumpf-Rollen/Nicken +-1,5, Schulterblatt +-14, Kopf ruhig | wie Plan | wie Plan | |
**Weg = 3 x 0,53 / 0,3148 x 0,544 / (1,6/1,5) x 0,35 = 0,90157 E -> 1,603 Kacheln/s** (Plan 0,90189 / 1,603). Becken z Spitze-Spitze 0,79 cm.

### 1.2 Run = Galopp, 17 Bilder, 2 Zyklen a 8 Bilder (3,75 Hz)
| Groesse | Plan | gebaut | Grund |
|---|---|---|---|
| S / duty | 0,61 / 0,25 | **0,56 / 0,2295** | Plan: 2 Bilder ueberstreckt, Becken 6,45 cm, Durchdringung 147 Punkte (v1/v3) |
| aussen / spur H / V | 0,012 / 0 / 0 | 0,04 / +0,01 / -0,005 | Hinterpfote im Schwung weiter aussen am Unterarm vorbei |
| ab, spitze, m0/hexp V | RUN | 22/20, 45/50, 0,3/0,6 | wie Trab |
**Weg = 2 x 0,56 / 0,2295 x 0,51 x 0,35 = 0,87111 E -> 2,613 Kacheln/s** (Plan 2,613). Becken 3,98 cm.

### 1.3 Sitzen S_J (RIG_PLAN 5.4) -- `rig/werkzeug/sitz_loesen.py` (Becken z, Sprunggelenk z, Becken x, Pfote x am Netz geloest)
Parameter in `baer_clips_rig.py` (RIG-Vorgabe) und `rig/clips/sitz_final_par.json`: Becken (-0,2453 / 0,3945), r_pel -40, r_sp -35, r_ch -47,
**Hals -25 (Erwachsener -66,8: zog den Kopf 11 cm hinter die Schulter, weil C7 senkrecht ueber Spine1 steht)**, Kopf -7, Schulterblatt 19,5,
Vorderpfote (0,356 / 0,098 / 0,042), Sprunggelenk (0,235 / 0,345 / 0,1389), Fuss (20 / -91 / 5), Zwischenplatz Vorderpfoten (0,40 / 0,095),
Hinterbein weicht im Schritt 9 cm nach aussen aus (`ferse_dy`, neu). Messung Sit Bild 0 (Bild 30/60/90 gleich bis auf den Kopf):
| Teil | Soll (5.4 / D.4) | gemessen |
|---|---|---|
| Sitzflaeche / Ferse / Pranken (tiefste Haut) | 0,0..+0,3 / 0..0,5 / -0,05..+0,3 cm | **0,10 / 0,10 / 0,00 cm** |
| Hueftmitte | x -0,29 +-0,03 | (-0,290 / 0 / 0,322) |
| Achsen Becken->Lende / Lende->Brust | 40-47 / 44-52 | 45,5 / 44,5 |
| Brustachse (Erwachsenen-Richtung Spine1->Neck mit der Brustdrehung) | 52-62, min 48 | **47,0** (1 Grad unter dem Minimum: steiler hebt die Schulter ueber 0,733 m, dann ueberstreckt der Arm -- Variante r_ch -50: Ellbogen 172,8 > 172) |
| Schulter | z <= 0,737 | (0,181 / 0,103 / 0,733) |
| Ellbogen innen / Unterarm gegen Senkrechte | 160-172 / <= 8 | 167,2-169,0 / Seite 6,8, vorn -0,6 |
| Handgelenk x - Schulter x / \|y\| / z | 0..3 cm / 0,09-0,13 / 0,095-0,105 | 1,5 cm / 0,097 / 0,097 |
| Pranken-Luecke / Pranken flach | 1-4 cm | 1,6 cm / Sohle 0,0..1,19 (Rand) |
| Knie innen | 115-145 | 135,8 |
| Hinterfuss-Mitten / Innenkante neben Pranke / Handgelenk hinter Sprunggelenk | 0,55-0,76 m / >= 1,5 cm / 3-10 cm | **0,738 / 6,0 / 3,9** |
| Zehen hoch / aussen | 65-80 / 10-25 | 77,4 / 17,6 |
| Sohlen-Normale hoch | 10-25 | **1,0** (Generator-Pfote: Sohle parallel zu Foot->Toe0 minus 13,6 Grad; 10-25 hiesse Zehen 86-101 Grad = ueber senkrecht; Erwachsener 2c gleich -91) |
| Blick Augen-Nase (jedes Sit-Bild) | -40..-33 | **-34,9..-34,0** |
| Kopf gegen Hals | <= 68 | 20,2-22,3 |
| Atlas ueber/vor dem Schultergelenk | >= 0 | **-1,5 cm** (knapp dahinter; Kopf oben 1,279 m = 44,8 cm bei 0,35) |
| Schwanz am Boden | 0..+1,2 | Stummel 11,9 cm hoch (sitzt auf dem runden Hintern, im Bild unsichtbar) |
| Uebergaenge | SitDown 0 / StandUp Ende = Idle; Sit erstes = letztes | Sit 0 = Sit Ende = SitDown Ende = StandUp 0 bit-gleich; gegen Idle01 Bild 0: Gelenke 2,28 cm, Drehung 7,70 Grad (Erwachsener 2c gleich gemessen: 2,06 cm / 7,70) |
| Sprung je Bild (lokale Drehung) | wie 2c | SitDown 18,0 / StandUp 17,0 Grad (Erwachsener 2c 16,3 / 19,4) |
| Klemmen/Ueberstrecken (Log) | 0 | 0 in allen drei Clips |

---------------------------------------------------------------------------------------------------------------------------

## 2. Die 10 byte-gleichen Clips: Becken-Regel, Hub, D.5 (`rig/werkzeug/abw_bauen.py` -> `rig/clips/hub.json`, `rig/clips/abw.npz`)
Drehungen des Erwachsenen byte-gleich, Becken-Regel DX 0,0375 (aus dem Export), dazu Hub dz je Bild an der Haut: Stuetzbild = Pfote des
Erwachsenen (2c-Dump, eigene Haut) < 1,0 cm; dz = Mitte von min/max der Stuetzpfoten des Jungen; Netz ohne Krallen >= -0,5 cm; geglaettet
(+-2 Bilder), Sprung je Bild <= 0,3 cm (Death 1,2 cm, Begruendung unten). Arm-IK nur wo eine Stuetzpfote nach dem Hub > 1,0 cm vom Boden.
| Clip | Hub cm | Sprung/Bild | D.5-Abweichung (Knochen: groesste Abweichung gegen den Erwachsenen) | Stuetzpfoten nach Hub cm |
|---|---|---|---|---|
| Idle01 | -0,02..+0,02 | 0,005 | -- | -0,20..+0,20 |
| Death | -8,19..+0,80 | **1,2** | Neck/Head je 12,75 Grad zum Boden (zusammen 25,5 = delta+15), Rampe ssf(0,55; 0,92; t) wie der Kopf des Erwachsenen sinkt | 0,00..+6,73 (Kippen, s. C1) |
| Dead | -2,08 | 0 | Neck/Head je 12,75 Grad | liegt (Netz +0,45, Kopf 15,1 cm hoch; Erwachsener 12,6) |
| Rear | -0,18..+0,05 | 0,08 | -- | -0,29..+0,60 |
| SwipeL | -0,24..+0,24 | 0,25 | IK R (Stuetzarm, 16 Bilder): UpperArm 3,0 / Forearm 3,0 / Hand 3,0; L: 2,22 / 0,89 / 1,99 | -0,50..+0,98 (vorher 2,09) |
| SwipeR | -0,25..+0,27 | 0,25 | IK L: 3,0 / 3,0 / 3,0; R: 1,61 / 0,39 / 1,80 | -0,50..+1,03 (vorher 2,12) |
| Slam | -0,47..+0,02 | 0,14 | IK L (5 Bilder): 0,33 / 0,67 / 0,34 | -0,50..+0,92 |
| Bite | -0,18..+0,52 | 0,28 | IK L: 0,50 / 0,83 / 0,89; R: 0,83 / 1,00 / 1,55 | -0,50..+0,86 |
| Maul | -0,47..+0,01 | 0,30 | IK L: 1,33 / 1,94 / 2,94; R: 2,44 / 2,17 / 0,68 | -0,50..+1,24 (vorher 2,37) |
| Eat | -0,47..-0,37 | 0,02 | **Neck -15 / Head +15 Grad** (alle Bilder, Schleife bleibt zu), Begruendung unten | -0,43..+0,70 |
- **Eat:** Raster `abw.py probe` / Kontakt-Probe: mit allen erlaubten Kombinationen (je Knochen <= 25,5) bleibt die tiefste Kopfhaut bei 38-47 cm
  (kurzer Hals, Kopf hoch; Erwachsener ~0 cm). Hals +25,5 / Kopf -15 senkte sie nur auf 38,3 cm, drueckte den Kopf aber in die Brust (55-74
  Kopfpunkte < 1,5 cm an Brust/Arm, Falte an der Kehle im Ton, Dehnung max 3,44). Gewaehlt: Kopf VOR die Brust (3-6 Punkte, Dehnung max 2,91,
  Schnauze zeigt 68-89 Grad nach unten), tiefste Kopfhaut 42,3 cm. Ellbogen beugen (<= 10 Grad) bringt rechnerisch < 2 cm -- nicht benutzt.
- **Death:** die schmalere Spur (Q_H 0,64 / Q_V 0,55) hebt das ganze Junge beim Kippen bis 8 cm vom Boden (Bilder 28-40). Das Becken des
  Erwachsenen faellt dort selbst 0,5-0,7 cm je Bild; mit Hub-Sprung 1,2 cm/Bild schwebt das Junge hoechstens 0,77 cm (0,3 cm erlaubt -> 2,7 cm).

---------------------------------------------------------------------------------------------------------------------------

## 3. Gewichte endgueltig (RIG_PLAN 5.6) -- `baer_gewichte_rig.py opt` (unveraendert, nur Dump-Pfad), Abgabe `rig/clips/gewichte_end.npz`
Zwischen-GLB `rig/clips/zw/NCBearCub_zw.glb` (neue Clips, ohne Hub) -> Dump `zw/dump_zw.txt.pkl` -> `opt gew_formel.npz dump_zw.txt.pkl
gew/gew_opt_end.npz schritt=3` (Zusatzbilder an), 1.629 s CPU: <= 4 Einfluesse, Summe 1, Abweichung von der Formel im Mittel 0,085.
**Dehnung (C3) am fertigen GLB, alle Bilder, Importer-Matrizen** (`rig/clips/dehnung_final.json`):
| Clip | p99,5 | max (Region, Bild) | Achsel/Brust | Falten s2<0,5 |
|---|---|---|---|---|
| Idle01 | 1,14 | 1,30 (Hals 9) | 1,19 | 0 |
| Walk | 1,69 | 2,82 (Leiste 3) | 2,71 | 2.005 |
| Run | 1,72 | 2,68 (Achsel 0) | 2,68 | 2.105 |
| Death | 1,86 | 3,05 (Hals 71) | 2,69 | 2.656 |
| Dead | 2,08 | 3,05 (Hals 0) | 1,73 | 1.252 |
| Rear | **2,30** | 3,23 (Achsel 35) | **3,23** | 815 |
| SwipeL | 1,87 | **3,50** (Bauch 13) | 2,87 | 420 |
| SwipeR | 1,96 | 3,27 (13) | 3,05 | 433 |
| Slam | 1,90 | 2,71 (Achsel 27) | 2,71 | 408 |
| Bite | 1,54 | 2,71 (Hals 23) | 2,42 | 704 |
| Maul | 1,80 | 2,83 (Hals 25) | 2,22 | 371 |
| Eat | 1,78 | 2,91 (Hals 21) | 2,05 | 192 |
| SitDown | 1,97 | 3,47 (Leiste 26) | 1,96 | 1.771 |
| Sit | 2,05 | 3,08 (Leiste 0) | 1,89 | 639 |
| StandUp | 1,85 | 3,40 (Leiste 6) | 1,89 | 1.651 |
Alle Grenzen gehalten (2,6 / 4,0 / 3,5). Falten-Zahlen in der Groessenordnung des Vorab-Stands (SKELETT.md 5: Walk 1.703, Run 3.235).

---------------------------------------------------------------------------------------------------------------------------

## 4. Export und Harness (RIG_PLAN 6.1/6.2)
`baer/spiel/baer_export_rig.py` (Vorstufe der Rolle SKELETT, erweitert, LF): `neu=CLIPS_NEU.npz` setzt in Walk/Run/SitDown/Sit/StandUp alle
Drehungen ausser Dummy01/Bip01/Translation_Data (die stehen in allen 15 Clips des Erwachsenen in Ruhe, gemessen) und das Becken; Walk/Run
Translation_Data = Weg des Generators (Richtung und linearer Verlauf vom Erwachsenen); Hub als WELT-Hoehe ueber die Bip01-Drehung (der alte
Sitz-Weg addierte lokal y = in Bip01 nach vorn); `abw=` hat Vorrang vor allem. UV nicht gespiegelt (schon glTF).
**Harness-Ausgabe** (`rig/clips/log/dump_final.log`): `OK .../rig/out/42/media/models_X/Skinned/NCBearCub.glb Knochen 26 Clips [DeerStag_Idle01,
NCBear_Eat, NCBear_Maul, DeerStag_Dead, NCBear_Sit, DeerStag_Run, NCBear_Bite, NCBear_SwipeR, DeerStag_Death, NCBear_Rear, NCBear_Slam,
NCBear_SwipeL, DeerStag_Walk, NCBear_SitDown, NCBear_StandUp]`; Pickle: 26 Knochen, 15 Clips, (11811, 16) Punkte, 19.418 Dreiecke.

---------------------------------------------------------------------------------------------------------------------------

## 5. Messungen (RIG_PLAN 6.3)
| Nr | Messung | Grenze | Ergebnis |
|---|---|---|---|
| T1 | Knochen/Eltern/Reihenfolge, Knoten-Drehungen, Skin-Joints; Clips Namen/Dauer/Zeit-Accessoren; 1 Netz/1 Primitiv/kein Material/Bild; Skalier-Schluessel; Lagen = lage_E | exakt | alles gleich (`pruef_glb.json`): Knoten-Drehungen byte-gleich, Zeit-Accessoren **1.170/1.170**, Skalier **390/390**, Lagen-Abweichung 0, 1/1, kein Material/Bild, Dauern 3,2/0,9/0,5333/2,5667/0,0333/3,0/1,5/1,5/2,4/1,3/1,6/3,2/1,6/4,0/1,3, Bilder 97/28/17/78/2/91/46/46/73/40/49/97/49/121/40 |
| T2 | Importer laedt, Dreiecke, Punkte, Einfluesse, Summe, NaN, FK | hart | laedt; 19.418 (<= 20.000); 11.811 (< 65.536, u16); 4; 0,99999988-1,0000001; kein NaN; FK 4,5e-7 E |
| T3 | offene / nicht-mannigfaltige / entartete Kanten | 0 | 0 / 0 / 0 (Netz = FORM + Kantentausch SKELETT, unveraendert) |
| T4 | Dreh-Kanaele byte-gleich | nur laut Tabelle | **242/390** byte-gleich; abweichend: Walk/Run/SitDown/Sit/StandUp je 23 (neu), Death/Dead/Eat je Neck+Head, Swipe L/R, Maul, Bite je 6 Arm-Knochen, Slam 3 (= Abschnitt 2) |
| T5 | Textur 1024 RGB 8 Bit ohne Alpha; Pfade; MD5 | exakt | 1024 x 1024, RGB, 8 Bit, Farbtyp 2; `rig/out/md5.txt` |
| T6 | NCBearTest, zaehmen/mod, Originale, Eingaenge unveraendert | exakt | **Modelle, Texturen, Skripte, AnimSets der NCBearTest, `_arbeit/baer_zaehmen/mod/`, alle `baer/spiel/*.py` ausser `*_rig.py`, SKELETT-/FORM-Abgaben, `baer_junges/eingang/*` gleich** (`clips/md5_vorher.txt` / `md5_nachher.txt`, 189 Dateien). In NCBearTest aenderten sich um 10:55 Lua-, Translate-, sandbox- und mod.info-Dateien (+ BanditsNPCBearGrow.lua, Stats.lua neu) -- **nicht durch diesen Lauf** (er hat dort nur gelesen; vermutlich der Lauf B1d einer anderen Sitzung, ungeprueft). NPC Crew: nicht gelesen, nie beschrieben. |
| C1 | Boden je Stuetzpfote | -1,5..+1,5, Ziel +-1,0 | Idle -0,20..+0,20; Walk -0,03..+0,73; Run -0,03..+0,69; Rear -0,29..+0,60; SwipeL/R -0,50..+0,98/+1,03; Slam ..+0,92; Bite ..+0,86; **Maul ..+1,24**; Eat -0,43..+0,70; SitDown/StandUp ..+1,05/+0,99; Sit 0,0..+0,14; **Death 0,0..+6,73** (39 Stuetzbilder > 1,0, 17 > 1,5: im Kippen liegt das Junge mit dem Rumpf auf, die Pfoten des Erwachsenen stehen noch -- "wo andere Haut aufliegt, gilt die Haut des Jungen", D.3; Schweben des ganzen Tiers <= 0,77 cm) |
| C2 | Netz >= -0,5; Krallen nicht tiefer als Erwachsener; aufliegende Haut 0..+1,2 | | Netz ohne Krallen >= -0,50 in allen Clips; Krallen >= -0,50 (Death/Dead: Erwachsener -0,03/+1,12 -> 0,5 cm tiefer, im Liegen); Dead aufliegend +0,45; Sit Sitzflaeche 0,10 |
| C3 | Dehnung | 2,6 / 4,0 / 3,5 | Abschnitt 3: 2,30 / 3,50 / 3,23 |
| C4 | Durchdringung Bein/Bein (Kapseln wie g_sitz2 + Pfoten-Ellipsoide) | 0 | Walk/Run **0**; Sit 10-12, SitDown 13-14, StandUp 10-13 Punkte Innenseite Unterschenkel in der 30-%-Kapsel des Unterarms derselben Seite (weiches Anliegen der dicken Generator-Beine, im Ton von vorn nicht sichtbar; breiter = Hinterfuss-Mitten > 0,76 bzw. Pranken-Luecke < 1 cm, Varianten s5a-c/s6) |
| C5 | Sitz-Pose | 5.4 | Tabelle 1.3 |
| C6 | Augen-Nase Idle 0 = Ruhe +-5; Sit -40..-33; Kopf gegen Hals <= 68 / <= 35 | | Idle 0 **-45,2** (Ruhe -42,0); Sit -34,9..-34,0; Kopf gegen Hals max Sit 22,3, sonst Eat 28,0 / Bite 24,5 / Maul 23,0 |
| C7 | Tempo aus dem GLB, Gleiten | 1,60 (>=1,40) / 2,61 (>=2,40); <= 1,5 cm | Walk **1,603**, Run **2,613** Kacheln/s (Weg 0,90157 / 0,87111 E x 1,6 / Dauer); Gleiten je Stuetzphase 0,0 cm (Abrollpunkt in Welt) |
| C8 | Uebergaenge | | Walk/Run/Sit/Idle/Eat erstes = letztes 0,0; SitDown Ende = Sit 0 = StandUp Anfang 0,0 |
| C9 | Risse/Falten Hals/Achsel/Leiste (Ton) | keine > 1 cm2 | im Ton aller 15 Clips (az 90, Blatt `clips_45.png` rechte Spalte) keine Risse; kleine Kehlfalte im Eat (Kopf nach unten), Dead: Beine liegen uebereinander (Erwachsenen-Drehungen, schmale Spur) |
| K1 | Form gegen FORM-Abgabe | +-2 cm | Punkte = C_rig_basis + Versatz x -0,0825: Abweichung 0,0; UV gleich |

---------------------------------------------------------------------------------------------------------------------------

## 6. Blaetter (alle selbst angesehen; Renders Cycles OPTIX mit gpu.lock, aus dem Importer-Dump des fertigen GLB)
- `rig/bilder/clips.png` -- je Clip eine Zeile, 4 Phasen (0/25/50/75 %) aus Kevins Kamera az 0 / el 30 gross + Spielgroesse 1:1 (109,9 px/m).
- `rig/bilder/clips_45.png` -- dasselbe aus az 45 / el 30, rechts Ton von der Seite.
- `rig/bilder/clips_gang.png` -- Trab/Galopp alle Bilder von der Seite + Pfoten-Spuren in Welt (waagerechte dicke Strecken = steht).
- `rig/bilder/clips_sitzen.png` -- Kevins Sitzvorlage neben Sit 0/60 von vorn, Ton, az -30, Kevins Kamera.
- `rig/bilder/clips_ruhe.png` -- Foto | Ruhe az 43 / el 8 | Kevins Kamera; 8 Seiten (Textur, Ton, Spielgroesse); Kopf nah.
- `rig/bilder/clips_vergleich.png` -- alter Platzhalter (NCBearTest 6c3f0a96, eigener Dump `clips/platzhalter/`) gegen neu.
- `rig/bilder/clips_r6.png` -- Eat tiefstes Bild, Death 38, Dead, Rear hoechstes Bild.
**Bild-Fragen 6.5 (mein Urteil):** 1 Ton = Baerenjunges von 8 Seiten: ja (`clips_ruhe.png`). 2 Kopf gerade, Hals ohne Stufe: ja (FORM). 3 Ohren:
ja. 4 Pfoten rund: ja. 5 Trab/Galopp: Pfoten stehen, nichts schwebt/steckt, Gangbild flink -- ja (`clips_gang.png`; der Trab hat Flugphasen).
6 Sitzen wie Vorlage: **ja** (aufrecht, Beine vorn, Pranken dazwischen, Kopf oben, Blick geradeaus-seitlich). 7 Risse/Beulen: keine; kleine
Kehlfalte Eat, Beine im Liegen uebereinander. 8 Neben Platzhalter: das neue Junge ist kompakter, rundkoepfiger und dem Foto naeher; der
Platzhalter ist laenger (1,86 m gegen ~1,3 m bei 1,0) und frisst mit der Schnauze am Boden, das neue nicht (Eat-Frage). Urteil "besser" ist Sache
des Gegenpruefers.

---------------------------------------------------------------------------------------------------------------------------

## 7. Abweichungen vom Plan (alle begruendet)
| Plan | hier | Grund |
|---|---|---|
| Trab S 0,64 / duty 0,38 | 0,53 / 0,3148 (Tempo gleich 1,603) | Plan-Werte ueberstrecken, Becken 4,3 cm, Hinterfuss in Unterarm/Pranke (1.1) |
| Galopp S 0,61 / duty 0,25 | 0,56 / 0,2295 (Tempo gleich 2,613) | Ueberstrecken, Becken 6,5 cm, Durchdringung (1.2) |
| Abrollen um Toe0 | um den Zehenansatz unten | Toe0 liegt 8 cm hoch mitten in der Pfote (SKELETT Fuss-Faktor 0,361) |
| Eat: Hals/Kopf nach unten | Hals -15 / Kopf +15 (Kopf vor die Brust) | Boden mit D.5 unerreichbar; nach unten drueckte der Kopf in die Brust (2) |
| Hub-Sprung <= 0,3 cm/Bild | Death 1,2 cm/Bild | Kippen mit schmaler Spur (2) |
| Sitz: Brust 52-62 (min 48) | 47,0 | Armreichweite: Schulter <= 0,733 m (1.3) |
| Sitz: Sohlen-Normale 10-25 | 1,0 | Generator-Pfote (1.3) |
| Sitz: Atlas ueber/vor der Schulter | 1,5 cm dahinter | C7 senkrecht ueber Spine1 (1.3) |
| Werkzeuge kopieren | eigene Werkzeuge `rig/werkzeug/` (rl, gang_pruef, sitz_mess/-loesen/-pruef, wandle, hub, abw, abw_bauen, pruef_final, glb_fk, spuren, render_auftrag, clip_render (Kopie proben_render), blatt_clips, platzhalter_posen, montage, textur_pruef, ende.sh) | Messungen auf das Netz/Skelett des Generator-Jungen zugeschnitten; Originale nicht geaendert |

---------------------------------------------------------------------------------------------------------------------------

## 8. Risiken und Fragen fuer Kevin
### 8.1 Risiken
1. **Wachsen (B1d, andere Sitzung, NCBearTest 10:55):** `BanditsNPCBearDefs.lua` hat jetzt maxSize 1,35, `BanditsNPCBearStats.lua` zeigt das
   Junge bis `cubMaxSize` 0,75. Das Tempo bleibt 1,60 / 2,61 Kacheln/s (der Weg liest keine Groesse), aber die Pfoten laufen im Bild mit der
   Groesse: bei 0,5 laufen sie 43 %, bei 0,75 114 % schneller nach hinten als der Boden (Gleiten/"Laufband"). Ohne Gleiten passt der Clip nur
   bei 0,35. Abhilfe waere ein Abspieltempo je Groesse (ungeprueft, ob die Engine das fuer Tiere kann) oder Clips je Groessenstufe.
2. Ungeprueft (Laufzeit): wie der flinke Trab (3,3 Hz, Flugphasen) und der Galopp (1-2 Stuetzbilder je Pfote) im Spiel wirken; Flimmern ohne
   Mipmaps; "walkingOnTheSpot" (RIG_PLAN 8.1/7); alles MP.
3. Die Kampf-Clips (Rear/Swipe/Slam/Bite/Maul) sind fuer das Junge nur mitgebaut (gleiche 15 Namen); Maul-Stuetzpfote bis 1,24 cm.
### 8.2 Fragen
1. **Fressen:** Das Generator-Junge traegt den Kopf hoch auf einem kurzen Hals -- mit den erlaubten Abweichungen kommt die Schnauze nur auf
   ~42 cm (bei 1,0; ~15 cm im Spiel) ueber den Boden. Soll das Junge einen eigenen Fress-Clip bekommen (Vorderbeine einknicken/hinlegen, Kopf
   am Boden)? Das waere ein neuer Clip ausserhalb von D.5.
2. **Gehen:** Trab mit 1,60 Kacheln/s (vorher 0,52) und Galopp mit 2,61 -- passt das Tempo? Die Folgen-Schwellen in `BanditsNPCBearFollow.lua`
   muessen danach gerichtet werden (nicht dieser Lauf).
3. **Wachsen gegen Gangbild:** Soll das Junge bis 0,75 wachsen (dann gleiten die Pfoten, 8.1.1) oder bei 0,35 bleiben, bis es Clips je
   Groessenstufe gibt?
4. Sterben: das Junge liegt mit dem Kopf 15 cm (bei 1,0) ueber dem Boden (Erwachsener 12,6) und die Beine liegen uebereinander -- so lassen?
5. Aus RIG_PLAN 8.2 weiter offen: Laenge (kompakt, L/H 1,2), Maul zu, Kopf hoch getragen, kuerzere Hinterpfoten.

---------------------------------------------------------------------------------------------------------------------------

## 9. Befehle zum Wiederholen (Pfade absolut; R = C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig, SP = .../baer/spiel)
```
# 1. neue Clips (Blender, CPU, ~2 s) und Umrechnung
NCB_RIG_AUS=$R/clips/clips_neu_posen.npz blender --background --factory-startup --python $SP/baer_clips_rig.py -- x
python $R/werkzeug/wandle.py $R/clips/clips_neu_posen.npz $R/clips/clips_neu.npz
#    Pruefen: python $R/werkzeug/gang_pruef.py $R/clips/clips_neu_posen.npz ; python $R/werkzeug/sitz_pruef.py $R/clips/clips_neu_posen.npz
#    Gang-Varianten: python $R/werkzeug/gang_suche.py VARIANTEN.json ORDNER ; Sitz loesen: python $R/werkzeug/sitz_loesen.py NAME key=wert ...
# 2. Zwischen-GLB (ohne Hub) + Harness + Gewichte endgueltig (~27 min, Hintergrund)
python $SP/baer_export_rig.py $R/skelett/netz_rig.npz $R/skelett/gewichte_rig.npz $R/clips/zw/NCBearCub_zw.glb neu=$R/clips/clips_neu.npz
java -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump $R/clips/zw/NCBearCub_zw.glb $R/clips/zw/dump_zw.txt skin
python .../baer_junges/werkzeug/dump_pkl.py $R/clips/zw/dump_zw.txt
python $SP/baer_gewichte_rig.py opt $R/skelett/gew_formel.npz $R/clips/zw/dump_zw.txt.pkl $R/clips/gew/gew_opt_end.npz schritt=3
# 3. Endkette: Abgabe Gewichte, D.5 + Hub, Endexport, Textur, Harness, alle Pruefungen, MD5
sh $R/werkzeug/ende.sh
# 4. Renders und Blaetter (GPU-Sperre)
python $R/werkzeug/render_auftrag.py $R/clips/dump_final.txt.pkl $R/clips/gewichte_end.npz $R/out/42/media/textures/Body/NCBearCub.png $R/clips/render 24
python $R/werkzeug/spuren.py $R/clips/dump_final.txt.pkl $R/clips/clips_neu.npz $R/clips/render/spuren.png
sh .../_arbeit/baer_gen/werkzeug/gpu_lauf.sh LOG blender -b --factory-startup --python $R/werkzeug/clip_render.py -- $R/clips/render/cfg.json
python $R/werkzeug/blatt_clips.py $R/clips/render/r $R/clips/platzhalter/r $R/clips/gang_pruef_final.json $R/bilder
```

## 10. Dateien
| Datei | Inhalt |
|---|---|
| `baer/spiel/baer_clips_rig.py` (neu, LF) | Generator: Trab, Galopp, S_J (RIG-Vorgaben), Ausgabe Posen |
| `baer/spiel/baer_export_rig.py` (erweitert, LF) | Export mit `neu=`, Weg je Clip, Hub in Welt |
| `rig/clips/clips_neu_posen.npz`, `clips_neu.npz` | neue Clips (Posen / lokale Schluessel, Weg, Phasen) |
| `rig/clips/hub.json`, `abw.npz`, `abw/abw_bericht.json` | Hub je Bild, D.5-Kanaele, Bericht |
| `rig/clips/gewichte_end.npz` (= `gew/gewichte_rig.npz`), `gew/regionen_rig.npz`, `gew/gew_opt_end.npz`, `log/opt_end.log` | Endgewichte |
| `rig/clips/dump_final.txt(.pkl)`, `pruef_glb.json`, `pruef_final.json`, `dehnung_final.json`, `gang_pruef_final.json`, `sitz_pruef_final.json`, `log/*.log` | Harness und Messungen |
| `rig/clips/zw/` (Zwischen-GLB + Dump), `suche/` (Gang-Varianten), `sitz/` (Sitz-Loesungen), `platzhalter/` (Dump/Renders alt), `render/`, `diag/` | Arbeitsstaende |
| `rig/clips/md5_vorher.txt`, `md5_nachher.txt` | T6 |
| `rig/out/42/media/models_X/Skinned/NCBearCub.glb`, `rig/out/42/media/textures/Body/NCBearCub.png`, `rig/out/md5.txt` | **Endergebnis** |
| `rig/bilder/clips*.png` | Blaetter |
