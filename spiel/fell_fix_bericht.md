# Lauf baer-fell: Nachbesserung (09.11.2026)

**Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.** Renders nur RTX 4090, OptiX + OptiX-Entrauscher, ueber
`werkzeug/gpu_render.sh` (Werkzeug des Pruefers Optik `pruef/optik/werkzeug/render_optik.py`, gleiche Auftraege). Um 13:37 lief
ProjectZomboid (ohne NCBearTest): kein Render, nur CPU-Arbeit; ab 13:41 lief das Spiel nicht mehr, dann gerendert, Sperre `gpu.lock`
danach frei. Nichts in die Test-Mod oder nach NPC Crew geschrieben, nichts committet. Die Dateien des abgebrochenen Anlaufs in `pruef/`
nicht angefasst. Alte Mod-Dateien und Kopf-Variante vorher gesichert: `fix/vorher/` (MD5 unten), Skripte vorher: `fix/skripte_vorher/`.

## 0. Ergebnis kurz

- **Alle 4 major des Pruefers Optik und das major des Pruefers Technik behoben**, dazu 12 minor; 3 minor abgelehnt/offen mit Grund
  (Zotteln = Kevins Wort, Pranken-Form, Messgrundlage). Netz, Gewichte und beide Texturen sind neu gebaut.
- Feste Regeln (eigene Messung): **15/15 Clips bit-gleich**, Knochen/Namen/Eltern, Offset- und Bind-Matrizen bit-gleich, **18.930
  Dreiecke** nach dem Importer, <= 4 Einfluesse, Summe 1, ein Netz ohne Material, Liegehoehe 0,0001 m wie vorher, **Kopf-Texel
  bit-gleich** (2048 +2 px, 1024 +1 px: 0 verschieden), Maul-Flecken unveraendert und frei, PNG-Typ/Groesse gleich, Pfade gleich, nur die
  5 Dateien. Kopf/Krallen: Lage, UV, **jetzt auch Gewichte** bit-gleich (gehaeutet 0,00 mm Abweichung ueber alle Clips; vorher 2,38 mm);
  ein Kopfpunkt am Nahtrand (1,8 cm vom Rumpf) liegt 1,6 cm anders - erlaubt ("hoechstens Nahtrand wie baer-anim").
- Dehnung besser als die Lieferung: 99,5 % je Clip hoechstens **2,45** (Lieferung 2,48, Ziel 2,6), Hoechstwert **3,16** (3,37; Ziel 4,0),
  Achsel/Brust **3,02** (3,04; Ziel 3,5), Liegen sigma2 < 0,3 **121** (194; Ziel 200), Falten Achsel+Ellbogen liegend **58 + 30 = 88**
  (154; Ziel 120).

## 1. Befunde einzeln

| # | Befund | Entscheidung | Messwert Lieferung -> Nachbesserung (alt NCBearTest in Klammern) |
|---|---|---|---|
| O-M1 | Heller Streifen/goldenes "V" Leiste (Rear, Licht B) | **behoben** (Textur) | Rear Spielgroesse Licht B, Band L/R Luma 92/87 -> **68/62** (alt 73/69); Band/Brust 1,84/1,74 -> 1,45/1,34 (alt 1,85/1,74). Textur Leiste (5x5-Mittel / Ruecken) p95 1,53 -> **1,13**, p99 1,78 -> 1,24; Leiste im Spiel hell (Licht A, Ruhe) 0,56 -> 0,55 (Ziel >= 0,40 bleibt). Im Bild kein Band mehr (`fix/blick/f_rear_k.png`, `f_rear_gross.png`). Das Pruefer-Ziel "Band <= Brust + 20 %" ist mit meinem Ausschnitt nicht erreicht (Brust liegt im Rear unter den Armen im Schatten); das Band ist jetzt dunkler als im heutigen Spielstand. |
| O-M2 / T-m1 | "Ei" und Pranken von vorn | **Ei behoben** (Netz), **Pranken-Form offen** | Breite oben/unten Rear 1,3 s (Armgewicht < 0,3) 0,941 -> **1,033**; (< 0,05) 0,923 -> **1,009** (Ziel >= 0,95). Schultern 2,4 -> 4,0 cm voller (Maske ab Ruhe-z 0,38), Flanke/Huefte 1,7 -> 3,2 cm schlanker (bis z 0,80), `fix/werkzeug/ei.py`. Pranken: Farbe jetzt grau-braun statt Lappen/rostorange, **Form unveraendert** (Pranke traegt die festen Krallen; mehr Volumen hiesse Krallen/Netz der Pfote anfassen) -> Kevin. |
| O-M3 / T-m4 | Straehnen nicht staerker | **behoben** (Textur) | Spielgroesse Licht B (`fix/werkzeug/mess_bild.py`, Regionen wie `struktur.py`): Kontrast Ruecken 0,050 -> **0,070** (alt 0,047), Flanke 0,057 -> **0,079**, Hinterteil 0,059 -> 0,079; Kohaerenz Ruecken 0,61 -> 0,66, Flanke 0,52 -> 0,60. Buesche jetzt einzeln um zufaellige 3D-Punkte (~1,3 cm breit, ~8 cm lang Spielmass = 3-6 Texel der 1024er), Hub 0,15 -> 0,30. |
| O-M4 | Beine/Hinterteil gesprenkelt, Wirbel am Schwanzansatz | **behoben** (Textur) | Kohaerenz Hinterbein 0,43 -> **0,57** (alt 0,48), Hinterteil 0,50 -> 0,59, Hinten-Ansicht 0,53 -> 0,64. Ursache: helle Haarschlaufen aus Ansichten gegen die Haarspitzen (x3-Ausgleich) + Gitter-Buesche in projizierten Koordinaten (Ringe um den Wirbel der Haarrichtung). Jetzt: Gesprenkel vor der Nacharbeit inselweise geglaettet (`glaetten_insel`, ~2,5 Texel), stabile Haarrichtung (`haar_tangente`), 3D-Buesche (`buesche_3d`). Wirbel in `dead_hinten` weg. Bilder `fix/blick/t1_bein_zoom.png`, `t1_dead_k.png`. |
| T-M1 | Falten Achsel+Ellbogen liegend 154 (Ziel 120) | **behoben** (Gewichte) | DeerStag_Dead sigma2 < 0,5: Achsel 97 -> **58**, Ellbogen 57 -> **30** (Summe 88); Sitzen Achsel 116 -> **71**, Ellbogen 33 -> **23** (alt 19); Dead sigma2 < 0,3: 194 -> **121**. Neu: Knie liegend 0 -> 14 Dreiecke (sigma2 < 0,5), im Ton-Bild unauffaellig (`fix/blick/f_knie_k.png`). Falten-Strafe (Achsel-Region + 16 cm um den Ellbogen) und Quetsch-Strafe (alle Dreiecke unter sigma2 0,35) in `baer_gewichte_fell.py`. |
| O-m1 | Pfoten rostorange | **behoben** | Anteil gesaettigter Fellpixel (s > 0,62, v > 0,30): Idle 0,42 -> **0,02 %**, Sit 0,45 -> 0,02 %, Rear 0,70 -> 0,01 % (alt 0,12/0,09/0,03 %). Pfoten (unter ~22 cm) zu grau-braun, Saettigung des Fells hoechstens 0,56 (dunkle Texel ausgenommen). |
| O-m2 | Delle Hinterknie, fremde Gewichte | **behoben** | Hinterkoerper mit Hand/Unterarm > 0,005: 28 -> **0** (alt 12); Vorderbein mit Hals/Kopf: 239 -> **1** (max 0,016, aus der Formel); Hinterkoerper mit Hals/Kopf: 168 -> **0** (`fix/werkzeug/fremd.py`). Regel: Vorderbein-Knochen nur vor x 0, Hinterbein-Knochen nur dahinter, nie am anderen Bein; Hals/Kopf nicht an Beinen/Hinterteil. Delle/Stern in `knie_swiper_ton`, `slam_folge2_ton` weg. |
| O-m3 | Sohle: Ballen klein, Reifenprofil, Punktring | **behoben** | Ballen ~15 % groesser gemalt (q x 0,87), Sohlenhaut heller/glatter (Luma Sohlenhaut ~60 -> ~75, Risse 6-12 mm -> 1-2 cm und schwaecher), Ballen-Luma 96 -> 100, Furchen 44 -> 46 (Ziel <= 50), Fellkranz als Straehnen in Pfotenfarbe, Pfoten-Unterseite ums Sohlen-Rund voll geglaettet. Bilder `fix/blick/f_sohle_k.png`. Netz-Relief (8 mm) unveraendert. |
| O-m4 | Scharfkantige helle Flecken | **behoben** | Ursache: Back-Pose- und Innenbein-Gewichte schalteten hart je Dreieck (Region der Karte gilt je Dreieck). Jetzt weiche Felder ueber das Netz. In `naht_bein_hinten`, `bauch_seite_unten`, `B_rear_gross` keine Flecken mehr zu sehen (`fix/blick/f_naht_k.png`, `f_rear_gross.png`). |
| O-m5 | Gesaessfalte nicht sichtbar | **teils** (Netz) | Falte 2,6 -> 4,0 cm tief; im Ton von hinten schwach sichtbar, dazu schmalere Huefte (`fix/blick/f_ton_k.png`). Kevins Blick entscheidet. |
| O-m6 | Zotteln am Umriss | **abgelehnt bis Kevins Wort** | Geometrie-Zotteln gaben Noppen (`bau_netz.md` 4); die Textur kann den Umriss nicht aendern. |
| O-m7 | Falten hinter dem Ellbogen liegend | **behoben** mit T-M1 | Knick-Bild `dead_links_ton` ruhiger; Zahlen bei T-M1. |
| O-m8 | Licht A statt B | **angenommen** | Alle Helligkeitsurteile hier mit Licht B (Spielgroesse), Licht-A-Werte nur zum Vergleich. |
| T-m2 | Kopf-Gewichte nicht bit-gleich | **behoben** | Kopf 1.333 Dump-Punkte: Lage+UV+Gewichte/Index 1.332 gleich (Lieferung 1.161), 1 Nahtrand-Punkt verschoben (siehe 0.); Krallen 455/455 in allen 16 Werten; Kopf+Krallen gehaeutet 2,38 -> **0,00 mm**. Gewichte aus `netz/gew_bestand.npz` (Formel am alten FBX), Zuordnung ueber die Lage (alt_von zaehlt in einem anderen FBX). |
| T-m3 | Krallenfarbe an 46 Ecken | **behoben** | Bilinear an allen 456 Krallen-Ecken gegen NCBearTest: Body 46 -> **0** verschieden, WorldItems 23 -> **0** (Lesefeld 2x2 in 2048 und 1024 mit den Texeln von `bestand/NCBear_2048.png`; 65 Texel, 58 in Rumpf-Inseln). Krallen-UV unveraendert. |
| T-m5 | Nachbau ueberschreibt die Lieferung, Doku-Luecken | **behoben** | Ordner per Umgebung: `BAER_FELL_NETZ`, `BAER_TX_DIR`, `BAER_TX_ANS` (dazu bestehend `BAER_FELL_FBX`, `NCB_FELL_GEWICHTE`, neu `NCB_FELL_KOPF_ALT`); Kopf-Variante landet in `BAER_TX_DIR`. `bau_netz.md` 6 und `bau_textur.md` 9 ergaenzt (lowpoly_npz, karten, Deer). Ganze Kette ohne GPU: `fix/lauf_fix.sh`. |
| T-m6 | Maul-Maske in glb_pruef faengt Rumpfpunkte | **behoben** | `netz/glb_pruef.py`: nur die drei Flecken + 4 px; Lieferung 248 -> 222 Punkte (= alt 222). |
| T-m7 | FBX mit Nutzerpfad und Zeitstempel | **behoben (Pfad, Zeit), Rest offen** | `fbx_neutral` in `baer_export_fell.py`: Pfad -> "NCBear.blend" (gleich lang), Zeitstempel fest; "Kevin" 0-mal in der Datei. Byte-gleich nachbaubar ist das FBX trotzdem nicht: Blender vergibt die Objekt-IDs je Lauf neu (36 Byte); Geometrie gleich. |
| T-m8 | Nur alle fuenf Dateien zusammen | **an den Integrator** | Gilt weiter: neues Netz/UV. Neues Deer passt zur neuen UV (10.909/10.909 UV), das gelieferte nicht mehr (1.793/10.878). |

## 2. Feste Regeln und Netz-Ziele (eigene Messung am neuen GLB, `fix/technik/analyse_out.txt` = Pruefer-Werkzeug `analyse.py`)

| Clip | 99,5 % Lieferung -> neu | max -> neu | Achsel max | Brust max |
|---|---|---|---|---|
| Idle | 1,20 -> 1,18 | 1,30 -> 1,28 | 1,20 | 1,13 |
| Walk / Run | 1,95 / 2,31 -> 1,87 / 2,21 | 2,24 / 2,67 -> 2,07 / 2,49 | 2,07 / 2,18 | 1,86 / 1,97 |
| Death / Dead | 2,07 / 2,05 -> 2,02 / 2,00 | 2,56 -> 2,34 / 2,32 | 1,86 / 1,85 | 1,77 / 1,54 |
| Rear | 2,16 -> 2,08 | 3,21 -> 2,56 | 2,17 | 1,76 |
| SwipeL / SwipeR | 2,40 / 2,48 -> 2,35 / 2,45 | 2,98 / 3,18 -> 3,02 / 3,12 | 2,76 / 2,83 | 3,02 / 3,00 |
| Slam / Bite / Maul | 2,13 / 1,82 / 1,57 -> 2,08 / 1,73 / 1,53 | 2,51 / 2,53 / 2,32 -> 2,55 / 2,39 / 2,21 | 2,55 / 2,39 / 1,76 | 1,90 / 1,44 / 1,55 |
| SitDown / Sit / StandUp | 1,98 / 1,90 / 2,08 -> 1,94 / 1,84 / 2,01 | 3,09 / 3,37 / 3,09 -> 2,91 / 3,16 / 2,91 | <= 1,66 | <= 1,76 |
| Eat | 1,56 -> 1,52 | 2,25 -> 1,72 | 1,53 | 1,53 |

(`werkzeug/regionen.py` an meinem Dump, ohne Kopf/Krallen; Tabelle `fix/werkzeug/dehn_tab.py`.) Netzguete (`netz/pruef_netz.py`):
Rumpf-Knick ueber 20 Grad 6,9 -> 7,4 %, Hubbel Mittel 1,6 -> 1,7 mm, Umklapper 1, Kanten != 2 Flaechen 0. UV: 65 Inseln ohne
Ueberlappung, je Sohle 1 Insel, dunkler Saum 0,26 -> 0,17 %. Deer: 40 Knochen, Namen/Eltern/Offset/Bind gleich der Lieferung, 18.516
Dreiecke, keine Clips. Textur je Region im Ruhe-Licht A (`mess_textur.py`): Unterseite 0,43-0,70 (Ziel >= 0,40) wie geliefert;
Struktur (3-Texel-Detail) der Unterseite **relativ** zum jetzt staerkeren Ruecken gesunken (z. B. Bauch 0,81 -> 0,52, Hinterteil
0,85 -> 0,52): gewollte Folge der Gesprenkel-Glaettung, im Spielbild ist die Richtung des Fells klarer (Kohaerenz oben).

## 3. Dateien

- Mod (Arbeitsordner, alle 5 zusammen): `_arbeit/baer_fell/mod/42/media/`
  - `models_X/Skinned/NCBear.glb` **2a4837f6e8f41d97e07c76b2353b5520** (vorher c8250ace...)
  - `models_X/Skinned/NCBearDeer.glb` **f34cb9dcd5fc5c6f97e9d45255f998b2** (vorher c5cc07bb...)
  - `models_X/WorldItems/NCBear.fbx` **7e3300fe728a24172792623abf1a2f5c** (vorher d90796cd...)
  - `textures/Body/NCBear.png` (1024) **c2d6c8cc2e5858eff6b3d679fc4d5343** (vorher 79a9aca4...)
  - `textures/WorldItems/NCBear.png` (2048) **033d3705b0e1f4ed09c6d6f518a285e5** (vorher 9395c7fe...)
  - byte-gleich zu `fix/mod/42/media/` nachgezaehlt. Kopf-Variante neu (passt zum neuen Rumpf): `textur/NCBear_kopf_variante.png`
    c049a6b5..., `textur/NCBear_kopf_variante_body1024.png` 3582a42b... (1024: Unterschiede nur Kopf-Inseln + 4 px).
- Sicherung vorher: `fix/vorher/42/...` (c8250ace, c5cc07bb, d90796cd, 79a9aca4, 9395c7fe) und die alte Kopf-Variante (7c466a70, 9b976171).
- Skripte (geaendert): `baer/spiel/baer_export_fell.py` (NETZ per Umgebung, Form, `fbx_neutral`), `baer_gewichte_fell.py`
  (Knochenregel, Falten-/Quetsch-Strafe, Kopf-Gewichte alt, 240+80 Runden), `baer_textur_fell.py` (Ordner, weiche Felder,
  Gesprenkel, 3D-Buesche, Deckel/Farbton, Sohle, Krallen-Lesefeld). `baer_kampf_fell.py` unveraendert. `netz/glb_pruef.py` (Maske).
- Bau-Ordner der Nachbesserung: `fix/netz/` (Blend, npz, Gewichte, Karten, Zwischenstand), `fix/textur/` (2048er, Kopf-Variante,
  mess), `fix/quelle/` (FBX), `fix/lauf_fix.sh` (Kette), `fix/log/`. Die Lieferung der Bauer in `netz/` und `textur/` ist unveraendert
  (ausser der Kopf-Variante; `textur/mess/regionen_vergleich.json` wurde von meiner Messung ueberschrieben und mit den Befehlen aus
  `bau_textur.md` 9 wiederhergestellt).
- Messungen/Bilder: `fix/technik/` (analyse, kopf, textur, uv), `fix/mess_final/`, `fix/render/fix/` (70 Bilder, gleiche Auftraege
  wie Pruefer Optik), Blaetter alt|Lieferung|neu `fix/blick/f_*.png`, Werkzeuge `fix/werkzeug/`.

## 4. Offen

1. **Nicht gespielt.** Kevin muss das Spiel neu starten, wenn die Dateien in der Test-Mod sind.
2. Pranken-Form (Volumen) unveraendert; Zotteln am Umriss nur mit Kevins Wort; Gesaessfalte nur schwach sichtbar.
3. Ballen-Relief im Netz 8 mm (die Textur traegt die Sohle). Normalen der Unterseite nicht gekippt.
4. Neue Knie-Falten liegend (14 Dreiecke sigma2 < 0,5), im Bild unauffaellig. Sitzen Ellbogen 23 (alt 19).
5. Die Gewichte sind gegen genau diese 15 Clips gerechnet (neue Clips -> `baer_gewichte_fell.py` neu).
6. Optik-Urteile (Fell staerker, Pfoten grau-braun, breitere Schultern) sind Geschmack: Kevins Blick entscheidet.
