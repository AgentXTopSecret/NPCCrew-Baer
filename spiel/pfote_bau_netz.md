# Lauf baer-pfoten: Bauer Netz + Hochmodell (09.11.2026)

Blender 5.2.3, PZ 42.21. **Statisch/offline gebaut, gemessen und (Ton) gerendert, nicht gespielt.** Renders nur RTX 4090 (OptiX +
Entrauscher) ueber `werkzeug/gpu_render.sh` (Sperre `gpu.lock`, Spiel- und Fremd-Blender-Pruefung). Nichts in die Test-Mod oder nach
NPC Crew geschrieben, nichts committet, Originale `*_anim.py`/`*_fell.py` unveraendert (MD5 `log/md5_originale.txt`), baer_fell nur gelesen.
Uebergabe an den Textur-Bauer: `netz/uebergabe.md`.

## 0. Kurz

1. **Vier echte Pfoten statt Saeule mit Kappe.** Das Bein verjuengt sich zum Gelenk (hinten 20,5 cm in 20 cm Hoehe, heute 34,7; vorn
   20,3, heute 34,3), darunter ein eigener Fuss aus EINEM Feld mit dem Bein: hinten Ferse (ragt 2,3 cm hinter die Kehle), Rist, lange
   Sohlenplatte, fuenf einzelne Zehen (ragen 20,4 cm vor das Schienbein, heute 6,7), vorn breite Pranke mit Zehen (12,0 cm vor dem Unterarm,
   heute 4,1), angehobener Handwurzelballen. Im Ton-Bild ist jede Pfote als Fuss mit Zehen lesbar (Runden r6-r8f, Abschnitt 4).
2. **Feste Regeln gehalten (gemessen):** 15/15 Clips bit-gleich (Abtastzeiten, Schluessel, Modellmatrizen; Animationspuffer der Datei
   byte-gleich), Knochen/Namen/Eltern, Offset- und Bind-Matrizen gleich; **19.388 Dreiecke** (<= 20.000), <= 4 Einfluesse, Summe 1;
   **kein Clip tiefer im Boden als heute** (0 Verstoesse, je Clip/Pfote/Kralle); Kopf: 1.033 von 1.182 Kopfpunkten bit-gleich, 149
   Nahtrand-Punkte wie baer-fell (kopfprobe), im Dump 1.532/1.533 Kopfpunkte gleiche Lage; Krallen hinten 228/228 bit-gleich, vorn
   228/228 = alt + K1 (Abweichung 1,3e-8 m); Dehnung 99,5 % <= 2,49, max 3,22, Achsel 3,08 / Brust 2,94; fremde Gewichte 0.
3. **Nicht erreicht (ehrlich):** Sohlenrand-Knick (Soll <= 20/35/55 Grad, gemessen 36-38 / 61-64 / 84-92 an der Sohleninsel; nach der
   Mess-Art von `spez/heute_kontur.py` 24-27 / 46-50 / 59-66, heute 20-21 / 47-50 / 68-85); Rumpf ueber z 0,36 max 2,10 cm (Soll 1,5;
   p95 0,16 erfuellt; 4 Punkte an der Innenseite der Hinter-Kniekehle); Ballen-Relief 1,44-1,57 cm (Soll 1,0-1,4); Krallenwurzeln
   liegen an der Hautoberflaeche (-0,3..+0,15 cm, Soll 0,2-0,8 innen); Zehen-Rillen oben teils < 1,2 cm; Handwurzelballen unten 1,4 cm
   (Soll 1,5-2,0), Vorsprung 0,55 cm (Soll 0,8); Rist vorn 6,1 cm (Soll 6,5-8,5). Einzelheiten 3.2.
4. **Bilder:** Ton-Runden r1-r8f und Endstand als Blaetter `bilder/netz_<Runde>_1..5_ton.png` (Kevins Vorlage | alt | neu). Der
   Endstand wurde um 19:05 gerendert (18:44-19:04 lief ProjectZomboid, so lange nicht gerendert). Mit Zwischentextur:
   `bilder/netz_final_*_tex.png` - die Zwischentextur (Rechnung `backen` von baer-anim, neue Fell-Ansichten) ist **fleckig und ohne
   gemalte Sohle**, sie ist nur Platzhalter; die echte Textur macht der Textur-Bauer.

## 1. Was gebaut ist

| Datei | Aenderung (Kopie, Original bleibt) |
|---|---|
| `baer/spiel/baer_quelle_pfote.py` | aus `baer_quelle_anim.py`. Neu im Feld-Teil (numpy, vor `Ende des Abstandsfelds`): `PfBein` (Loft ueber z), `PfFuss` (Loft ueber x: Kuppel ueber flacher Sohle, Ferse, Rist), `pf_zehen_ell` (fuenf laengliche, 9 Grad gekippte Zehen um die festen Krallenwurzeln), Krallenbett-Ellipsoide, Handwurzelballen, `pf_feld_s(vh, x, y, z, teil, soll)` (Spielmeter; `soll=True` = Soll des Spielnetzes mit Huelle), `pfote_feld_fn`. Metaballs: obere Kugeln der Unterschenkel-/Unterarmkette genau wie alt (vorn 3, hinten 2), die unteren neu duenner und nach hinten (`PF_KUGELN`), Fuss-/Pranken-Ketten (alt :901/:905) weg. `pfote_bauen` baut `pfote_<Knochen>` (Surface Nets, 2,0-2,6 mm), Krallen wie bisher, vorn K1. `pfoten_abstand(P, teil)`. Pfotenhaar (`haar_<Knochen>`), Beinfell nur wo die Koerperhaut nicht im Pfotenfeld steckt. `OUT` -> `_arbeit/baer_pfote/hoch/`. Kopf unveraendert. |
| `baer/spiel/baer_export_pfote.py` | aus `baer_export_fell.py`. Pfade nach `_arbeit/baer_pfote/` (`BAER_PFOTE_NETZ`, `BAER_PFOTE_ANS`, `BAER_PFOTE_ANS_ALT`, `MOD_FELL`). Huelle: zwei Schaelungen - Rumpf wie baer-fell (alte Grenze, alte Ansichten, 30 Runden glatt), Pfote/Unterschenkel bis genau zum Soll (`pfoten_abstand(..,'soll')`), Uebergang nach der Landehoehe z 0,28-0,35, Knie-Band nachgeglaettet, Hinterkante z 0,24-0,50 nicht hinter die heutige (+4 mm). Taubin an der Pfote 10 %. Verringern in zwei Gaengen (Rumpf ohne Pfoten 10.600, Pfoten unter z 0,12 zusammen 4.300). Sohlen: Ballenplan aus `spez/pfoten_plan.json` (Platte/Handballen als Vieleck, fuenf Zehenballen), `RASTER` 20 mm, `BALLEN_HUB` 10 mm, Rand-Aufraeumen (Fliegen/Ohren/kleine Loecher). K1 der vorderen Krallen + `k1_dy` in `netz_pfote.npz`. UV: Pfote vor/hinter dem Gelenk getrennt, Bein-Innenseite eigene Insel, selbstueberlappende Inseln werden geteilt. Neue Stufe `ansichten` (aus `baer_export.py:46-188`). `kopfprobe` prueft K1. `BAER_PFOTE_NUR_HUELLE=1` (Form-Runden). |
| `baer/spiel/baer_kampf_pfote.py` | aus `baer_kampf_fell.py`, Clips Zeile fuer Zeile gleich. Vorgabe-Quelle `_arbeit/baer_pfote/mod/42/media/`, `NCB_PFOTE_GEWICHTE`/`NCB_PFOTE_NUR_GEWICHTE`, Formel mit Fussruecken-Korrektur `max(w_fu, sst(0,04, 0,09, x - x_gelenk) * (1 - sst(0,10, 0,16, z)))`. |
| `baer/spiel/baer_gewichte_pfote.py` | aus `baer_gewichte_fell.py`: Pfote (Formel Fuss/Hand >= 0,95) bleibt Formel; K1 bei der Zuordnung der alten Krallengewichte zurueckgerechnet; Boden-Strafe fuer freie Punkte bis Ruhe-z 0,45 statt 0,25 (sonst Kniekehle im Sitzen 0,2-0,3 cm im Boden). |
| `werkzeug/lauf_pfote.sh` | Kette `netz fbx kopfprobe formel gewichte glb zwischen karten deer` (Deer mit dem unveraenderten `baer_tier_anim.py`), bricht ab, wenn eine Stufe kein OK meldet. |
| `werkzeug/` neu | `pfote_abnahme.py` (SPEZ 3.2), `pfote_tiefst.py` (Clip-Tiefe gegen `spez/heute_tiefst.json`), `rumpf_abstand.py` (Rumpf ueber z 0,36, Kopf), `dehnung_pfote.py` (Region Pfote/Gelenk), `feld_proto.py` (Feld ohne Blender, Umrisse), `zehen_profil.py`, `zehen_netz.py`, `auftrag_runde.py`, `blatt_runde.py`, `netzlib.py`, `dump_npz.py`; Kopien aus baer_fell (messen, glb_pruef, regeln, dehnung, fremd, glb_datei, karten, ...). |

## 2. Runden (Form, alte Ansichten bis r6, ab r7 neue Fell-Ansichten)
| Runde | Aenderung | Befund im Ton-Bild (angesehen) |
|---|---|---|
| r1 | Pfotenfeld + duennes Bein, Huelle bis zum Soll | Bein verjuengt, Fuss mit Ferse - aber Zehen nicht lesbar (flache Keil-Front), Stufe am Knie (`bilder/netz_r1_*`) |
| r2 | zwei Schaelungen, Knie-Band, Zehen als lange Wuerste | gleich: Rillen in Huelle/Voxeln zugelaufen (gemessen: Kerben 0,5-1,1 cm am Netz, 3-6 cm im Feld) |
| r3 | Zehen schmaler, Voxel 6,5/7,5 mm | Kerben 1,2-2,3 cm; Pranke von schraeg vorn mit Zehen; Sitzen: lange Sohle mit Zehen statt Kappe |
| r4-r5 | Verringern in zwei Gaengen (Pfoten 1.030-1.240 Dreiecke), Hinterkante auf heute begrenzt | Sitz-Clip ging 2,35 cm in den Boden (Hinterteil) -> behoben |
| r6 | Voxel zurueck auf 8,5/9,5 mm (Kopf-Nahtrand sonst nicht wie baer-fell), Zehen noch schmaler | **jede Pfote liest sich als Pfote** (`bilder/netz_r6_2_sitzen_aufrichten_ton.png`: Sitzen lange Sohle + 5 Zehen; Aufrichten: Hinterfuesse mit Ferse/Zehen) |
| r7 | neue Fell-Ansichten (`ansichten/`), Krallenbetten, breiterer Fuss | wie r6; Sohlenrand zackig, Pranke von unten kastig |
| r8/r9 | Knie-Uebergang tiefer (Breite in 36 cm wie heute), Sohlenrand-Glaettung probiert und verworfen (Knick schlechter) | `bilder/netz_r8f_*` |
| final | kleinere Krallenbetten, Gelenk 1 cm schmaler, Handwurzelballen hoeher, Boden-Strafe Gewichte | wie r6-r8f (`bilder/netz_final_*_ton.png`): Sitzen lange Sohle mit Zehen, Aufrichten Fuesse mit Ferse/Zehen, Pranke mit Zehen |

## 3. Messungen alt (GLB 2a4837f6) gegen neu (GLB a6099029, Dump.java)
### 3.1 Feste Regeln
| Regel | Ergebnis |
|---|---|
| Clips | 15/15 Abtastungen/Schluessel/Modellmatrix gleich (`log/glb_pruef_final.txt`), Animationspuffer byte-gleich (`glb_datei.py`) |
| Knochen, Offset, Bind | gleich (max 0,0) |
| Dreiecke | 19.388 nach dem Importer (heute 18.930; Ziel 19.300-19.700); je Pfote VL/VR/HL/HR 1.100 / 1.100 / 1.288 / 1.290 (heute 994 / 986 / 1.038 / 1.040) |
| Einfluesse/Summe | <= 4, 1,0000; 1 Netz, 1 Primitiv |
| Boden | 0 Verstoesse (`log/tiefst_final.txt`): z. B. Walk Haut VL -0,06 (heute -0,68), HR -1,45 (heute -1,41, Grenze -1,46), Run VL -0,17 (-0,77); Death Netz -1,53 (-1,81); Dead 0,40 (0,01); Sit Bild 60 tiefste Fusshaut 0,78/0,86 cm (heute 0,16/0,14 - Ferse schwebt, Clip-Runde C2) |
| Kopf | kopfprobe 1.033 bit-gleich + 149 Nahtrand wie baer-fell; Dump 1.532/1.533 Kopf+Kiefer-Punkte gleiche Lage, 1.504 auch UV/Gewichte; Kopf-/Krallengewichte = baer-anim (1.638 Punkte) |
| Krallen | hinten 228/228 bit-gleich, vorn 228/228 = alt + K1 (x/z bit-gleich, y 1,3e-8 m) |
| Dehnung (`messen.py`, `dehnung_pfote.py`) | 99,5 % je Clip max 2,49 (baer-fell 2,45, Soll 2,6), max 3,22 (3,16; 4,0), Achsel 3,08 (3,02; 3,5), Brust 2,94; **Pfote/Gelenk** 99,5 % max 2,54, max 3,08 (Soll 2,6 / 4,0); Liegen sigma2 < 0,3: 154 (Soll 200). Falten Achsel+Ellbogen sigma2 < 0,5 liegend: nicht eigens gemessen (Pruefer) |
| Fremde Gewichte (`fremd.py`) | 0 / 0 / 0 / 0 (heute 0 / 1 / 0 / 0) |
| Gewichte Pfote | unter 6 cm 98-99 % >= 0,95 (min 0,86-0,91); Fussruecken bis 10 cm min 0,74-0,84 (heute 0,59-0,62); Wade/Unterarm z 0,20-0,28 min 0,57-0,61 - **Soll >= 0,95 nicht erreicht** (heute auch nicht, 0,46-0,52; die Formel mischt dort Rumpf/Becken) |
| Rumpf ueber z 0,36 | p50 0,00, **p95 0,16 cm** (Soll 0,5), **max 2,10 cm** (Soll 1,5; 4 Punkte > 1,5 an der Innenseite der Hinter-Kniekehle bei z 0,37); ueber z 0,40 max 1,14 |
| Dateien | 5 Dateien mit gleichen Pfaden in `mod/42/media/` (MD5 Abschnitt 6); Deer 40 Knochen, Namen/Eltern/Offset/Bind gleich baer-fell, 18.974 Dreiecke |

### 3.2 Form (`werkzeug/pfote_abnahme.py`, `log/abnahme_final.txt`, heute `log/abnahme_heute.json`)
| Mass | VL heute -> neu | HL heute -> neu | Soll V / H |
|---|---|---|---|
| Bein z15 minus Fuss z3 (cm) | +9,1 -> -1,5 | +8,4 -> -0,6 (HR -0,5) | <= -1,5 / <= -0,5 |
| Fusslaenge / Beintiefe z20 | 1,08 -> 1,51 | 1,23 -> 2,12 | >= 1,4 / 2,0 |
| Sohle / Beintiefe z20 | 0,87 -> 1,15 | 1,13 -> 2,02 | >= 1,0 / 1,6 |
| Zehen-Ueberstand (cm) | 4,1 -> 12,0 | 6,7 -> 20,4 | >= 10 / 18 |
| Ferse hinter der Kehle (cm) | - | 1,5 -> 2,3 | - / >= 2,0 |
| Rist in der Fussmitte (cm) | Saeule -> 6,1 | Saeule -> 7,2 | 6,5-8,5 / 6,5-9,0 |
| Zehenstirn z 2,5: Vorspruenge / Einzuege (cm) | 5 / 0,2-0,4 -> 5 / 1,25-2,4 | 3 / 0,1-0,2 -> 5 / 0,6-2,3 (HR 0,8-2,4) | 5 / >= 0,8 |
| Hoehenprofil 1 cm hinter den Kuppen: Maxima / Rillen (cm) | 3 / 0,2-0,6 -> 5 / 0,3-2,3 | 4 / 0,1-0,3 -> 5 / 0,6-1,8 | 5 / >= 1,2 |
| Krallenwurzel in der Haut (cm, + = innen) | - | - | 0,2-0,8: neu -0,3..+0,15 (an der Oberflaeche) |
| Sohlenrand-Knick Mittel/p90/max (Mess-Art heute_kontur) | 20,1/46,8/68,0 -> 26,8/50,2/65,8 | 20,8/49,5/84,7 -> 23,6/45,6/58,7 | <= 20/35/55 |
| Ballen-Relief (cm) | 1,35 -> 1,44 | 1,06 -> 1,57 | 1,0-1,4 |
| Handwurzelballen unten / Vorsprung (cm) | - -> 1,4 / 0,55 | - | 1,5-2,0 / >= 0,8 |
| Schnitte (Tabellen SPEZ 1.2/1.3) | z 0,10-0,25: Kanten +-0,5, Breiten +-0,5 | z 0,10-0,25: Kanten +-0,4, Breiten +-0,5 | z 0,30-0,36 Knie: Vorderkante hinten 2,7 cm vor dem Soll (Uebergang) |
Umrisse gegen Tabelle/heute: `bilder/netz_final_umriss_links.png`, `..._rechts.png`.

## 4. "Abgesaegtes Bein?" (eigene Sicht, Ton; Runden r6-r8f und Endstand)
Stehen/Gehen/Rennen/Sitzen/Aufrichten/Liegen x VL/VR/HL/HR: in den Ton-Bildern von r6/r7/r8f und dem Endstand (`bilder/netz_final_*_ton.png`,
`netz_r6_*`, `netz_r8f_*`, `hoch/r7_nah.png`) ist keine Zelle mehr eine Saeule mit Kappe: Bein schmaler als der Fuss, Ferse und Zehen ragen heraus,
fuenf Zehen mit Krallen, im Sitzen lange Sohle mit Zehen oben (wie Kevins Vorlage), im Aufrichten stehen die Hinterfuesse ganz auf.
Schwaechen, die ich sehe: Sohlenrand im Gehen von hinten unten zackig/scharf, Pranke von unten (Aufrichten) kastig, Unterschenkel von
hinten duenn gegen das maechtige Hinterteil. Mit Textur nicht geprueft (Textur-Bauer). Endurteil: Pruefer Optik/Gegenpruefer und Kevin im Spiel.

## 5. Offen / Clip-Runde
1. Endstand-Bilder neu machen: `python werkzeug/auftrag_runde.py final dump_final.txt alle <Body-Textur>` + `bash werkzeug/gpu_render.sh
   werkzeug/render_optik.py render/final/auftrag.json log/render_final.log` + `python werkzeug/blatt_runde.py final alt_alle ton|tex`.
2. Sohlenrand-Knick, Krallenwurzel-Tiefe, Handwurzelballen, Rillen oben, Rist vorn, Rumpf-max am Knie: siehe 3.2; weitere Runden moeglich.
3. Sitzen: Hinterfuss 0,8 cm ueber dem Boden (heute 0,15) - nur mit Clip (SPEZ 4.2 C2). Gehen/Rennen: Zehen stecken weiter bis 2,4 cm
   im Boden (Krallen unveraendert) - C1.
4. Texturen in `mod/` sind die Zwischentextur (Rechnung `backen` mit den neuen Fell-Ansichten); die echte Textur macht der Textur-Bauer.
5. Nicht gespielt.

## 6. Dateien (`_arbeit/baer_pfote/`)
- `mod/42/media/models_X/Skinned/NCBear.glb` a6099029..., `models_X/Skinned/NCBearDeer.glb` 9246fa53..., `models_X/WorldItems/NCBear.fbx`
  ab35c415..., `textures/Body/NCBear.png` 5d4d0fab... (Zwischentextur 1024), `textures/WorldItems/NCBear.png` 7762b674... (Zwischentextur 2048)
- Netz: `netz/lowpoly_pfote.blend`, `netz_pfote.npz`, `gewichte_pfote.npz`, `gew_pfote_formel.npz`, `sohle_layout.json`, `karten/`,
  `lp_pfote.npz`, `zwischen_pfote/`, `uebergabe.md`, `log/`
- Fell-Ansichten des neuen Hochmodells: `ansichten/` (36 EXR + kameras.json)
- Dumps: `dump_final.txt` (Endstand), `dump_r*.txt`, `dump_deer.txt`; Messungen `log/abnahme_final.txt|json`, `log/tiefst_final.txt|json`,
  `log/rumpf_final.json`, `log/dehnung_final.txt|json`, `log/messen_final.txt`, `log/glb_pruef_final.txt`, `log/kette_final*.txt`
- Bilder: `bilder/netz_r1..r8f_*_ton.png` (Runden), `bilder/netz_final_umriss_*.png`, `bilder/netz_heute_umriss.png`; Einzelbilder `render/r*/`,
  alt mit Textur `render/alt_alle/`
- Werkzeuge `werkzeug/`, Hochmodell-Proben `hoch/` (probe_hoch.py, patch_*.py = Bau-Schritte an den Skripten)
