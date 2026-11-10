# Lauf baer-2c: Bau Textur + 5 Mod-Dateien (10.11.2026, 07:11-08:15)

Blender 5.2.3, JDK 25, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
- Nichts in die Test-Mod NCBearTest geschrieben (GLB dort weiter 5066fa67), nichts nach NPC Crew, nichts committet, nichts hochgeladen.
- Originale `*_pfote.py` unveraendert (MD5 9ae68692 / 402f9f5b / 14fceba9 / 380f259f / a14a4e1b, `textur/log/md5_skripte_vorher.txt` =
  `md5_skripte_nachher.txt`). Von den `*_2c.py` habe ich **nur `baer/spiel/baer_textur_2c.py`** geaendert (fbd67ac7 -> **19060fa4**, Kopie
  `textur/log/baer_textur_2c_stand_19060fa4.py`); export/kampf/maul/quelle/gewichte_2c unveraendert (85eb1f11 / b1575c19 / be09fe8e / 72230dae / 8bdd899a).
- Fremde `_arbeit/baer_*`-Ordner nur gelesen. Renders nur RTX 4090/OptiX + OptiX-Entrauscher ueber `werkzeug/gpu_render.sh` (Sperre
  `gpu.lock`, nicht auf das Spiel geprueft; Sperre am Ende frei). Kevins Vorlagen/Spielbild nur angesehen und lokal in Blaetter gelegt.
- Alle unten genannten Blaetter habe ich angesehen (Read).

## 0. Kurz

| Punkt | Ergebnis (Endstand) | Soll | ok |
|---|---|---|---|
| 5 Mod-Dateien in `mod/42/media/` | genau 5, Pfade wie NCBearTest, MD5 Abschnitt 6 | 5 | ja |
| GLB byte-gleich zum Gebiss-Bauer | **0ce2661e** = `glb_2c` (das GLB enthaelt keine Bilder) | byte-gleich | ja |
| Deer | **7a9f8778** = `glb_2c/tier` (Original `baer_tier_anim.py`, TIER_OK) | | ja |
| PNG | Body RGB 1024x1024, WorldItems RGB 2048x2048 (wie NCBearTest) | gleich | ja |
| Kopf-Texel 2048 / 1024 (ohne Flecken+4 px) | **0 von 858.273 / 0 von 212.944** verschieden zu NCBearTest; 1024 auch 0 zum Gebiss-Bauer | bit-gleich | ja |
| Maul-Flecken 1024 | 22.338 Pixel, **0** verschieden zum Gebiss-Bauer (`glb_2c` Body) | | ja |
| Hintersohle Median sRGB | HL **67/48/39**, HR **68/50/40** (NCBearTest 128/118/104 grau) | 62/42/30 +-12, R-B >= 20 | ja (R-B 28) |
| Sohle: Kuppe (Ballenmitte) ueber Median / Furche | HL **+10,7** / HR **+8,3**; Furche Luma **25** | +10..+15 / <= 45 | HL ja, HR knapp nein |
| Sohle grau (Saettigung < 0,25) | 0 % der Ledertexel | keine Grautoene | ja |
| Krallen hinten (bilinear an allen Ecken, 2048 und 1024) | einfarbig **63/50/40** (alt 150/131/105) | Wurzel <= 70/55/45, Spitze <= 150/135/115 | ja |
| Krallen vorn | 108/93/76 (alt 187/165/136); kein Kanal heller als vorher (max +0,0) | hoechstens dunkler | ja |
| Kopf-Passung Texel (`mess_texel_naht.py`, 1024) 0-4/4-8/8-12/12-20/20-35/35-60 cm | **1,00 / 0,95 / 0,95 / 1,01 / 0,94** / 0,70 (NCBearTest 1,01 / 0,96 / 0,91 / 0,90 / 0,76 / 0,66) | 0-12 >= 0,95; 20-35 >= 0,85 | ja |
| Kopf-Passung Bild Spielkamera Sit 0/30/60/90: Ring 0-4 cm / Kopf innen | **0,83 / 0,81 / 0,81 / 0,82** (alt 0,79 / 0,78 / 0,76 / 0,78) | >= 0,92 | **nein** (7.1) |
| dto. Ring 4-12 cm | **0,86 / 0,83 / 0,81 / 0,83** (alt 0,82 / 0,79 / 0,74 / 0,78) | >= 0,85 | nur Bild 0 |
| dto. Feinkontrast Ring/Kopf | 1,22 / 1,20 / 1,20 / 1,22 (alt 1,20 / 1,23 / 1,22 / 1,26) | <= 1,20 | knapp (Bild 0/90 +0,02) |
| Unterseite im Spiel-Licht (relativ Ruecken, `mess_textur`) | Kehle 0,79, Achsel 0,52, Leiste 0,54, Innenbein v/h 0,43/0,47, Brust 0,69, Bauch 0,52, Hinterteil 0,57 | >= 0,40 | ja |
| Straehnen Ruecken (`mess_bild`, Spielgroesse Licht B) | Kontrast **0,070**, Kohaerenz **0,656** (alt 0,069 / 0,659) | >= 0,063 / >= 0,60 | ja |
| Farbsprung Kopf/Hals (1-cm-Wuerfel) | Mittel 8,4, 90 % 18,5 (alt 8,5 / 18,4) | | wie alt |
| Pfoten-Luma je Hoehe 0-4-8-12-20-30-40-55 cm | 60/56/53/59/56/65/79 (alt 62/56/52/59/59/63/73); Rost < 22 cm 0,03 % | | wie alt |

Im Bild (Ton und Textur): Sitzen aus Kevins Spielkamera -- Kopf oben auf dem Koerper, Hals/Schultern in Kopffarbe, Hinterfuesse kurz mit
dunkelbrauner Ledersohle, Fellkranz und Zehenballen statt grauer Badelatschen, Vorderbeine gerade dazwischen, Krallen dunkel
(`bilder/textur_1_sitzen_spielkamera.png`). Stehen/Gehen aus der Spielkamera: Fell laeuft von der Pfote ueber Unterarm/Unterschenkel in den
Rumpf ohne Farbkante, keine "Hose im Stiefel" in der Textur (`textur_4`). Gebiss mit Endstand-Textur wie beim Gebiss-Bauer (`textur_5`).

## 1. Was geaendert ist (`baer/spiel/baer_textur_2c.py`, Schalter `BAER_TX_2C=0` = alte Rechnung bis auf die Pfade)

- **Projektion am Netz VOR form_2c** (`feld_zurueck` :1008, Aufruf :1087-1095, Texel :1178-1186, Back-Pose :1206, Ansichten :1236,
  Ausgleich :1285 ff.): Das Hochmodell der Ansichten ist am Rumpf nicht verschmaelert (Bau Koerper 7.4). Je Spielnetz-Punkt die
  Verschiebung S0 - S der 8 naechsten Punkte der dichten Huelle (`netz/form2c_feld_2c.npz`) zurueck: p50 0,01 / p95 8,5 / max 13,8 cm,
  Abstand zur Huelle p50 2,4 / p95 7,2 mm. Projektion, Sichtbarkeit, Back-Pose und Ausgleich der Blickrichtung rechnen an dieser Lage;
  Buesche, Haarrichtung der Buesche, Masken, Hoehen und Verdeckung am NEUEN Netz -> die Straehnen folgen der neuen Form.
- **Bezug** (Farbabgleich, Naht, Uebergang 27-50 cm): NCBearTest-Textur (603ee699) per naechstem 3D-Punkt an der Lage vor form_2c auf die
  neue UV (`werkzeug/textur/fell_uebertrag_2c.py`, alte Texel-Lagen `baer_pfote/fix1/bau4/textur/mess/texel_pfote.npz`): Abstand p50
  0,75 / p95 1,44 mm -> `textur/zw_2c_2048.png`. Farbabgleich linear 0,440/0,416/0,423 (fix1: 0,468/0,439/0,442), Ruecken-Luma 94 (alt 90).
- **Hintersohle** (`leder_farbe` :854, `ballen_q3` :796-800, `sohlen_malen` :934-940; Parameter :705-735): dunkelbraun-ledern H_FARBE
  1,30/0,94/0,76 x Luma, Kuppe 0,250, Rand x0,50, Woelbung Platte t^1,4 (Glanz nur in der Mitte), Zehenballen t^0,7 (pralle Kuppe),
  Furche 0,100; Sohlenballen in der Textur runder als das Netz (Super-Oval 2,3 statt 3,4 -> Ecken werden Fellkranz); Zehenballen x1/0,80
  groesser gemalt; Fellkranz auf der Insel 4-8,5 Texel (2048) voll + Straehnen 7-16 Texel, auch ueber dem Leder (nicht hinter x -0,53,
  dort laeuft das Leder um die Ferse); Leder an der Fersenkante hoechstens 2,2 cm hoch. Vorderpfoten unveraendert.
- **Krallen dunkler** (:1737-1798): je Krallen-Schale Wurzel/Spitze nach Abstand zum Rumpf, ins 2x2-Lesefeld (2048 und 1024) gemittelt,
  je Kanal nur dunkler (min mit alt). Hinten einfarbig 60-66/47-52/38-42 (eine Kralle liegt in der UV auf 1-2 Texeln: ein Verlauf
  Wurzel->Spitze mittelt sich weg, v5 gab einfarbig 97/83/69 > Wurzel-Grenze), vorn 72/59/48 -> 150/134/113 (gemittelt 108/93/76).
- **Kopf-Passung C3** (:1616-1641): nach der Naht-Mischung Hals/Nacken/Kehle/Schultern/Buckel nur anheben (geglaettetes Log-Feld, Straehnen
  bleiben) auf HALS_F x Kopfmittel (Kopf-Texel des Bezugs, Luma 113, RGB 141/106/76) je 3D-Abstand zum Kopf (1,00 an der Naht ->
  1,03 bei 5-12 cm -> 0,97 bei 30 cm -> 0,82 bei 50 cm -> 0 bei 62 cm), Rampe ab 0,5-5 cm von der Naht, nur ueber Spiel-z 0,30-0,62 (Beine
  bleiben dunkler), Farbton 55 % zum Kopf bis 30-45 cm. Nahe am Kopf (bis 20-32 cm) Buesche 60 % schwaecher und halb so viel nachgeschaerft.
- **Fellbehang SPEZ 2.5** (:1396-1420, :1432-1452): Masken wie form_2c (f) (Ellbogen z 0,34-0,56 hinter dem Unterarm, Bauchkante x -0,26..0,09):
  Haarrichtung abwaerts in der Flaeche, laengere Buesche (sig_l 6,5 cm Hochmodell), Hub x1,55; Schattenband darunter -16 % (30.575 /
  10.105 Texel > 0,5). Im Bild nur schwach sichtbar.
- **Brust-Glaettung** (:1591-1604): waagerechte Helligkeitsstufe quer ueber die Brust (im Sitzen von vorn, auch im NCBearTest-Stand, im
  Ton keine Kante): mittlere Stufen (Feld 3 gegen 30 Runden) zu 85 % eingeebnet. Ausserdem fuer 2c der alte Wulst-Schaerfe-Schalter aus
  (:1664) und die Bein-Uebergaenge 27-50 cm nur noch an den Beinen (|y| > 5-11 cm) mit weicher Oberkante 0,42-0,58 (:1524, :1540).
- **Messdaten**: `mess/texel_<NAME>.npz` jetzt mit P0, dk (Abstand zum Kopf) und den Hintersohlen-Texeln (q, Leder, Fell);
  `BAER_TX_NUR_TEXEL=1` schreibt nur die Texel-Lagen (Bezug).

## 2. Runden (Bilder angesehen)

| Runde | Was | Befund |
|---|---|---|
| v1 | 2c-Kette erstmals, Sohle 62/42/30, Hals-Ziel 0,97 | Kopf oben, Sohle terrakotta-rot im Licht B, Hals hell mit harter Kante quer ueber die Brust (`textur/blatt_v1_a.png`, `zoom_v1_sit.png`); Bild-Ring 0,78 |
| v2 | Sohle dunkler/weniger rot, Platte runder, Zehenballen groesser; Hals-Ziel 1,03 ab 0,5 cm, z-Maske 0,28-0,50 | Sohle dunkelbraun, Bild-Ring 0,81, Feinkontrast 1,20; Brust-Linie bleibt (`blatt_v2_a/b/c.png`) |
| v3/v3p/v4 | z-Maske 0,30-0,62; Probe ohne Back-Pose; Bein-Uebergaenge nur an den Beinen, Wulst-Schaerfe aus | Linie unveraendert -> nicht Back-Pose, nicht Bein-Stufen (`blatt_v3p_brust.png`, `blatt_v4_brust.png`, Debug Regionen/z `blatt_dbg.png`) |
| v5 | Brust-Glaettung | Linie deutlich weicher, nicht ganz weg (`blatt_v5_brust.png`) |
| v6-v8 | Krallen hinten einfarbig dunkel; Sohlen-Kuppe staerker | Krallen-Soll erfuellt; Kuppe +6 -> +8 -> +13/+9 |
| **Ende (2c)** | Kuppe 0,250, Zehenballen t^0,7 | Werte Tabelle 0; zweimal byte-gleich gebaut (v5 = 2c 22c8b07a vor den Sohlen-/Krallen-Runden) |

## 3. Kontrollbilder (`bilder/`, Licht B, Engine-Normalen; alt = NCBearTest, neu = Endstand; Ton = ohne Textur)
- `textur_1_sitzen_spielkamera.png` -- **NUR LOKAL**: Kevins Spielbild | alt | neu Textur | neu Ton | Vorlage; neu Bild 0/30/90, Spielgroesse.
- `textur_2_sitzen_vorn.png` -- Sitzen von vorn und im Vorlagen-Blick (az -30 el 8): alt | neu | Ton.
- `textur_3_hinterfuss.png` -- **NUR LOKAL**: Hinterfuss im Sitzen nah (el 10 / el 0) neben den Vorlagen-Fuessen; Sohle von unten, nah, Seite, hinten.
- `textur_4_stehen_spielkamera.png` -- Stehen seitlich az +90/-90 el 30 (wie Kevins Bild), az 50/130, Gehen 2/20, Rennen 5: alt | neu | Ton.
- `textur_5_gebiss.png` -- **NUR LOKAL**: Bruell-Vorlage (2 Ausschnitte) | alt | neu (Rear 48 vorn/Foto/schraeg/Seite/oben/unten, Maul 13, Kauen, zu), Spielgroesse.
- `textur_6_posen.png` -- Aufrichten, Liegen, Stehen vorn/hinten, Spielgroesse alt | neu.
- `textur_7_kopf_passung.png` -- Kopf-Koerper-Uebergang (Ausschnitt) alt | neu | Zonen | Ton; vorn und Vorlagen-Blick.
- `textur_8_sohlen_uv.png` -- Sohlen-Inseln in der 2048er: alt HL | neu HL | neu VL (unveraendert).
- `textur_vorschau_sitzen.mp4` (208 Bilder, 30 fps, Spielkamera, Textur: Hinsetzen -> Sitz-Schleife -> Aufstehen), `textur_vorschau_bilder.png`.
- Einzelbilder `textur/render/final/` (49), `alt/` (49), `gebiss_final/` (24), `pruef_alt|pruef_neu/` (21, Kameras der Straehnen-Messung), `video/`.

Mein Urteil (statisch, nicht gespielt): **"Menschenfuss?"** nein -- kurze, dunkelbraune, ovale Sohle mit Zehenballen und Fellkranz, im Ton
und mit Textur. **"Kopf in der Kapuze?"** weitgehend nein -- Kopf oben, Hals/Schulter in Kopffarbe; unter dem Kinn bleibt eine
sichtbare Grenze zwischen glattem Kopf- und gestraehntem Halsfell (7.1). **"Hose im Stiefel?"** in der Textur nein (keine Farbkante am
Ellbogen/Knie). **"Zaehne/Zunge wie die Vorlage?"** innen ja (wie Bau Gebiss), Lefzen aussen fellbraun (Vorschlag 5).

## 4. Messungen (Werkzeuge `werkzeug/textur/`, Ausgaben `textur/mess/`)
- Feste Regeln: `textur_pruef_2c.py` -> `textur_pruef_2c.json` (Tabelle 0).
- Kopf-Passung Texel: `spez/werkzeug/mess_texel_naht.py textur/dump_v1.txt.pkl <Body>` -> `texel_naht_final.txt`; Bild:
  `spez/werkzeug/mess_naht.py <zonen> <tex> 20 0.001838 65` -> `naht_bild_final.txt`, `naht_bild_final_sit{0,30,60,90}.txt`.
- Unterseite: `mess_textur_2c.py` -> `mess_textur_2c.txt`; Straehnen: `mess_bild_2c.py render/pruef_alt render/pruef_neu` -> `mess_bild_2c.txt`
  (Leisten-Band/Brust im Aufrichten 0,99/0,95, alt 1,63/1,46: die Brust ist heller geworden; Brust-Kontrast 0,054 statt 0,062);
  Pfoten: `pfote_luma.py` -> `pfote_luma_2c.txt` / `pfote_luma_alt.txt`.
- Back-Log `textur/log/backen_2c.log`, GLB-Log `kampf_2c.log`, Deer `tier_2c.log`, Renders `render_*.log`.

## 5. Vorschlaege (NUR VORSCHLAG, nicht in den 5 Mod-Dateien; `vorschlag/`)
1. **Kopf-Texel 9 % dunkler** ab 5 cm von der Naht (an der Naht unveraendert): `NCBear_kopftexel.png` (1024) / `NCBear_kopftexel_2048.png`,
   Blatt `blatt_kopftexel.png`. Bild-Ring 0,88 / 0,88 (Endstand 0,81 / 0,81), aber Feinkontrast 1,32 und Koerperring/Kopfrand 1,10 (Endstand
   1,02) -- der Kopfrand wird sichtbar dunkler als der Hals. Im Bild sehr dezent. Werkzeug `werkzeug/textur/vorschlag_kopftexel.py`.
2. **Schwarzer Lippensaum aussen (M3)** neu auf der Endstand-Textur: `NCBear_lippensaum_endstand.png` (1024, 2.467 Texel) und
   `NCBear_lippensaum_endstand_2048.png` (9.679 Texel), Blatt `blatt_lippensaum_endstand.png` (Werkzeug des Gebiss-Bauers). Die alten
   Dateien des Gebiss-Bauers (`NCBear_lippensaum.png` auf der Platzhalter-Textur) habe ich nicht angefasst.
3. `textur/NCBear_kopf_variante.png` (Augen, alter Vergleich aus baer-fell) entsteht wie bisher nebenbei, nicht angesehen, nicht Teil der Lieferung.

## 6. Die 5 Mod-Dateien (`_arbeit/baer_2c/mod/42/media/`, `textur/log/md5_mod.txt`)
- `models_X/Skinned/NCBear.glb` **0ce2661e76fcc8781d9fb3192eb16721** (= Gebiss-Bauer `glb_2c`)
- `models_X/Skinned/NCBearDeer.glb` **7a9f8778d3e22876ec1d6ca12d5b156a** (= `glb_2c/tier`)
- `models_X/WorldItems/NCBear.fbx` **b440d69346a5d67bfed8c5b23788f00b** (= Bau Koerper / `glb_2c`)
- `textures/Body/NCBear.png` **9e9147b56b3792f57c65830034048b62** (1024, RGB; 2x2-Mittel der 2048er + Maul-Flecken aus `baer_kampf_2c.py`/`baer_maul_2c.py`)
- `textures/WorldItems/NCBear.png` **dc8ad63d1279cd2caf6395bbf6d5e83e** (2048, RGB)

## 7. Offen / ehrlich
1. **Kopf-Passung im Bild nicht im Soll:** Ring 0-4 cm/Kopf innen 0,81-0,83 (Soll 0,92), Ring 4-12 cm 0,81-0,86 (Soll 0,85, nur Bild 0).
   "Kopf innen" ist das helle Gesicht (Textur heller + zur Kamera beleuchtet). Der Koerperring ist schon so hell wie der Kopfrand
   (Koerper/Kopfrand 1,00-1,02); weiter anheben ergaebe einen hellen Kragen um den Kopf. Die Texel-Ziele aus SPEZ 6.2 sind erfuellt.
   Rest nur ueber Kopf-Texel (Vorschlag 5.1, Kevins Wort) oder Kopfgroesse/Haltung. Unter dem Kinn bleibt eine sichtbare Grenze
   glattes Kopffell / gestraehntes Halsfell (`textur/zoom_kehle.png`); dort auch ein winziger heller Fleck an der Kehle (Ursache ungeprueft).
2. **Brust-Stufe** (Sitzen von vorn, auch im NCBearTest-Stand) weicher, nicht ganz weg; Ursache nicht gefunden (nicht Back-Pose, nicht die
   Bein-Stufen; Ton ohne Kante). Die Brust ist im Aufrichten jetzt so hell wie das Leistenband (0,99 statt 1,63).
3. **Sohle HR Kuppe +8,3** (Soll +10..+15; HL +10,7). Die Sohlenplatte wirkt von unten weiter eher wie eine grosse glatte Platte; die
   Zehenballen sind kleiner und weniger glaenzend als in der Vorlage.
4. **Vorderpranken-Sohlen bleiben hellgrau** (Regel "Vorderpranken bleiben"); im Liegen sichtbar neben den jetzt dunklen Hinterfuessen.
   Dunkel waere ein kleiner Schalter (Kevins Wort).
5. **Fellkranz** am Sohlenrand grau-braun (Pfotenfell 73/60/48), im Sitzen nah etwas heller als die Sohle.
6. **Behang** (Straehnen/Schatten) im Bild nur schwach; Hinterbein-Uebergang im Gehen 20 mit hellem Fleck an der Kniekehle (Textur), klein.
7. Pfoten-Helligkeit je Hoehe stoesst an die Faktor-Grenzen (2 cm 0,70, 10 cm 0,71, 25 cm 1,25) wie in fix1.
8. Ruecken-Luma 94 statt 90 (der Buckel gehoert zur Bezugsregion und ist heller geworden); Unterseiten-Verhaeltnisse dadurch leicht kleiner, alle >= 0,43.
9. Clip-Runde (nur melden, wie Bau Gebiss/Sitzen): Lefzen hochziehen; Liegehoehe; Aufrichten neu.
10. `C:\render\` (Bau Koerper) liegt weiter da -- bitte von Hand loeschen.
11. **Nicht gespielt.** Nur offline mit Spiel-Licht B; Mipmaps und die Texturgroessen-Option (Vorgabe deckelt auf 256) im Spiel ungeprueft.

## 8. Wiederholen (`cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c`)
```
bash werkzeug/textur/ansichten_beide.sh                       # GPU: 26 + 9 Ansichten des Hochmodells (07:12-07:18), textur/ansichten*/
python werkzeug/kette/karten.py textur/netz/lp_2c.npz glb_koerper/netz/gewichte_2c.npz textur/netz/karten
bash werkzeug/textur/lauf_textur_2c.sh t0 texel bezug         # Texel-Lagen (P, P0) + Bezug textur/zw_2c_2048.png
bash werkzeug/textur/lauf_textur_2c.sh 2c backen glb deer     # ~1,5 + 0,2 + 0,1 min CPU; prueft GLB/Deer-MD5 gegen glb_2c
python werkzeug/textur/textur_pruef_2c.py textur/NCBear_2c_2048.png textur/glb_2c/42/media/textures/Body/NCBear.png textur/mess/texel_2c.npz
bash werkzeug/textur/runde.sh NAME [kurz|alle]               # Runde: backen + glb + Kontroll-Renders + Kopf-Naht-Messung
python werkzeug/textur/auftrag_tx.py neu|alt DUMP BODY AUS AUFTRAG.json [ZONEN.npz] [satz]; bash werkzeug/gpu_render.sh <abs>/werkzeug/textur/render_textur.py <abs>/AUFTRAG.json LOG
python werkzeug/textur/blaetter_textur.py                     # bilder/textur_1..7
```
Netz-Eingaenge (Kopien): `textur/netz/` (lowpoly_2c.blend, lp_2c.npz, sohle_layout.json = sohle_layout_2c.json, form2c_feld_2c.npz,
karten/). Werkzeuge `werkzeug/textur/` (Kopien aus `baer_pfote/textur/werkzeug` + neu: lauf_textur_2c.sh, runde.sh, fell_uebertrag_2c.py,
auftrag_tx.py, render_textur.py (= gebiss/werkzeug/render_gebiss.py), blatt_tx.py, blaetter_textur.py, dump_pkl.py, textur_pruef_2c.py,
mess_textur_2c.py, mess_bild_2c.py, vorschlag_kopftexel.py, kodieren.py).

## 9. Dateien (`_arbeit/baer_2c/`)
- **Ergebnis:** `mod/42/media/` (5 Dateien, Abschnitt 6).
- **Textur-Arbeit:** `textur/` (`NCBear_2c_2048.png`, `NCBear_v1..v8_2048.png`, `zw_2c_2048.png`, `glb_2c/`, `glb_quelle_2c/`, `tier_2c/`,
  `ansichten/`, `ansichten_pose/`, `dump_v1.txt` (+ .pkl, = GLB 0ce2661e), Arbeitsblaetter `blatt_v*.png`, `blatt_dbg.png`, `zoom_*.png`,
  `sohle_uv_v1_v2.png`, `vorlage_bruellen_ausschnitt.png` (nur lokal)).
- **Messungen:** `textur/mess/` (`textur_pruef_2c.json`, `texel_naht_final.txt`, `naht_bild_final*.txt`, `naht_bild_vorschlag_kopf.txt`,
  `mess_textur_2c.txt`, `mess_bild_2c.txt`, `pfote_luma_2c.txt`, `pfote_luma_alt.txt`, `texel_2c.npz`, `backen_2c.json`, `zonen_neu.npz`).
- **Logs:** `textur/log/` (`ansichten*.log`, `backen_*.log`, `kampf_*.log`, `tier_2c.log`, `render_*.log`, `md5_mod.txt`, `md5_skripte_*.txt`).
- **Bilder:** `bilder/textur_1..8_*.png`, `bilder/textur_vorschau_sitzen.mp4`, `bilder/textur_vorschau_bilder.png` (1, 3, 5 nur lokal).
- **Vorschlaege:** `vorschlag/NCBear_kopftexel.png`, `NCBear_kopftexel_2048.png`, `blatt_kopftexel.png`, `NCBear_lippensaum_endstand.png`,
  `NCBear_lippensaum_endstand_2048.png`, `blatt_lippensaum_endstand.png`.
