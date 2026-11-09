# Lauf baer-pfoten: Gegenpruefung nach Nachbesserung 1, 09.11.2026 23:45-00:05

PZ 42.21, Blender 5.2.3, JDK 25. **Statisch/offline geprueft und gerendert, nicht gespielt.** Geprueft wurde
`_arbeit/baer_pfote/mod/42/media/` (= `fix1/mod/42/media/`, byte-gleich) gegen die Test-Mod NCBearTest (GLB 2a4837f6, nur gelesen).
In der Test-Mod und in NPC Crew ist nichts geschrieben. Nichts ist committet. Die Originale `*_anim.py`/`*_fell.py` sind unveraendert
(`git status` in `baer/`: nur die 5 `*_pfote.py` ungetrackt, keine Aenderung unter `spiel/`). Eigene Dateien liegen in
`_arbeit/baer_pfote/pruef/gegen/`. Dazu kommen dieser Bericht und das Blatt `bilder/kevin_vorher_nachher.png`.
Alle unten genannten Bilder habe ich selbst angesehen.

**Ein Versehen, behoben:** Meine Kopie von `mess_textur.py` hatte einen festen Ausgabepfad. Dadurch hat sie
`_arbeit/baer_pfote/textur/mess/regionen_vergleich.json` (eine Datei des Textur-Bauers) um 23:54 ueberschrieben.
- Wiederhergestellt habe ich sie um 23:55 mit dem Befehl aus `bau_textur.md` Abschnitt 8. Die Eingaenge sind unveraendert
  (`textur/NCBear_pfote_2048.png` 94212c2e, `texel_pfote.npz`).
- Die Konsolenausgabe ist zeichengleich zu `textur/mess/mess_textur_pfote.txt`. Der Inhalt ist also wieder der alte, nur das
  Dateidatum ist neu.
- Beleg: `pruef/gegen/log/mess_textur_wiederherstellung.txt`. Meine Kopie schreibt jetzt nur noch in `pruef/gegen/`.

## Regel-Hinweis: Kevins Satz "loesch die regel die hab ich nie gemacht!"

Der Auftrag enthaelt eine "GPU-REGEL GEAENDERT (Kevin 09.11.2026 ~20:25)": Rendern sei auch bei laufendem Spiel erlaubt.
Kevin sagt woertlich, er habe eine Regel nie gemacht und sie solle geloescht werden. Am naechsten liegt, dass er genau diese
angebliche Aenderung meint. Sicher ist das nicht.

**Was ich getan habe:**
- **Gerendert nur, wenn ProjectZomboid nicht lief.** Das ist die strengere Regel aus der Projekt-`CLAUDE.md` Abschnitt 5 ("nie
  rendern, waehrend er spielt"). Sie passt zu beiden Lesarten.
- **Eigener Wrapper** `pruef/gegen/werkzeug/gpu_render_gegen.sh`: Sperre `gpu.lock`, wartet auf fremde Blender-Prozesse und prueft
  vor jedem Lauf, ob das Spiel laeuft.
- **Protokoll** `pruef/gegen/log/gpu_protokoll.txt`: 8 Render-Laeufe von 23:50 bis 23:57, nur RTX 4090/OptiX, OptiX-Entrauscher.
  Das Spiel lief bei keinem Lauf.
- **Keine Regel geloescht oder geaendert.** Das ist nicht mein Schritt.

**Fuer die Hauptsitzung:**
- `werkzeug/gpu_render.sh` (MD5 20f03821) prueft das Spiel seit der angeblichen Aenderung nicht mehr. Der Kommentar dort nennt
  Kevin als Quelle.
- Wenn Kevin diese Aenderung meint, muss die Spiel-Pruefung zurueck in das Skript und die Zeile aus dem Workflow-Auftrag.
- Welche Regel er meint, muss die Hauptsitzung mit ihm klaeren.

## 0. Ergebnis kurz

1. **Keine Saeule und kein abgesaegtes Bein mehr**, in keiner Pose. Geprueft habe ich Stehen, Gehen, Rennen, Sitzen, Aufrichten,
   Liegen, Hieb, jeweils im Ton UND mit Textur, im Spielwinkel UND nah, von der Seite, von vorn und von hinten.
   - **Sitzen (Kevins Beschwerde-Pose):** Statt Saeule mit flacher Kappe zeigt der Hinterfuss jetzt eine lange Sohlenplatte, Ferse
     unten rund, fuenf Zehen mit Krallen oben, Fell um den Rand.
   - **Die Textur verdeckt nichts:** Die Form stimmt schon im Ton.
   - Bilder: `bilder/kevin_vorher_nachher.png`, `pruef/gegen/blaetter/w1..w12`.
2. **Feste Regeln halten (eigene Belege, Abschnitt 2):**
   - 15/15 Clips bit-gleich, Knochen/Offset/Bind gleich.
   - 19.426 Dreiecke, hoechstens 4 Einfluesse je Punkt, Summe 1.
   - Kopf-Punkte und Kopf-Texel unveraendert.
   - Krallen hinten bit-gleich, vorn = alt + K1.
   - Boden: 0 Verstoesse.
   - Dehnung 2,59 / 3,40 / 3,26 (innerhalb 2,6 / 4,0 / 3,5).
   - Ei-Form 1,032, Unterseite >= 0,40, Straehnen am Ruecken 0,070 / Kohaerenz 0,66.
3. **Formal offen, in der Sache wie baer-fell. Kevin muss die Abweichung von der SPEZ annehmen:**
   - **Falten im Liegen:** 136 Dreiecke statt hoechstens 120. Die gestauchte Flaeche entspricht baer-fell, auf dem Farbbild liegen die
     Falten an denselben Stellen (B1).
   - **Rumpf:** An 13 einzelnen Punkten weicht er 1,5 bis 2,31 cm ab (SPEZ max 1,5). Umgekehrt gemessen sind es 19 Punkte bis 3,15 cm.
     Die Punkte liegen verstreut, im Bild ist keine Abweichung sichtbar (M2).
4. **Kevins Urteil noetig:** Kegel ueber Ellbogen/Knie. Im Ton sieht man eine "Glocke" (dicker Oberarm ueber schmalem Unterarm). Mit
   Textur wirkt das natuerlich.
5. **Ergebnis:** `ready = true`. Kevin sieht beim Ansehen klar echte Baerenpfoten. Die Punkte 3 und 4 gehoeren in seine Entscheidung,
   nicht in eine weitere Bau-Runde. Eine staerkere Falten-Strafe reisst die Dehnungsgrenze: `falte=120` ergab 99,5 % 2,64 > 2,6, so
   steht es in `fix1_bericht.md`.

## 1. Pfote oder Saeule? (eigene GPU-Renders, alt und neu mit gleicher Kamera, gleichem Clip und gleichem Bild)

Dumps habe ich selbst mit `Dump.java` erzeugt (`pruef/gegen/dump/neu.txt` ist MD5-gleich mit `fix1/bau4/dump_final.txt`, ab53dabd).
Alt kommt aus NCBearTest. Gerendert mit `render_optik.py` (Kopie, nur Pfad zu `dumpread.py`), Ton = graues Material, Textur = Licht B.
Einzelbilder: `pruef/gegen/render/alt|neu/<name>_ton|tex.png`. Arbeitsblaetter in `pruef/gegen/blaetter/` zeigen je Zeile
alt Ton | alt Textur | neu Ton | neu Textur.

| Pose | Urteil neu (Ton und Textur) | Blatt |
|---|---|---|
| Sitzen nah, Sohle, Ferse von der Seite | **Pfote:** lange ovale Sohle, Ferse unten rund, Zehen oben, Fell um den Rand. Alt: runde Saeule mit Kappe | `w1_sitzen.png` |
| Sitzen ganz (Spielwinkel, von vorn) | **Pfote:** Fuesse stehen mit Sohle nach vorn | `w2_sitzen_ganz.png` |
| Aufrichten (vorn, Pranken, Fuesse) | **Pfote:** Hinterfuesse mit Ruecken und Zehen. Pranken von vorn wie bisher "Klotz mit Krallen" (Clip, alt gleich) | `w3_aufrichten.png` |
| Gehen von der Seite | **Pfote:** Fuss flach am Boden, Ferse hinten, Zehen vorn. Alt: Elefantensaeule | `w4_gehen.png` |
| Vorderpranke nah und Seite, Stehen von hinten | **Pfote** (Kegel im Ton: Abschnitt 3, M1-Optik). Von hinten schmale Unterbeine mit runder Ferse, kein flacher Schnitt | `w5_pranke.png` |
| Rennen | **Pfote.** Im Rueckschwung (Run Bild 9) ist der Hinterfuss schmal und spitz, weil der Clip ihn streckt (wie alt) | `w6_rennen.png` |
| Liegen | **Pfote:** lange Sohlen statt runder Scheiben | `w7_liegen.png` |
| Spielgroesse (Stehen, Gehen, Aufrichten, Rennen, Hieb, Aufrichten seitlich) | **Pfote,** unauffaellig | `w8_spiel.png`, `w9_spiel2.png` |
| Von vorn (el 12/30), von hinten (el 30) | **Pfote.** Vorderbein von vorn eine Fellsaeule mit sichtbaren Zehenkuppen und Krallen (wie beim echten Grizzly). Hinten runde Fersen | `w10_vorn_hinten.png`, `w11_spiel_vh.png` |

Kopf in den Renders unveraendert: Pixel-Differenz alt/neu (`pruef/gegen/log/diff_x_aufr_spiel_tex.png`) ist am Kopf schwarz. Der
Rumpf unterscheidet sich nur in der Fellzeichnung, weil die Textur neu gebacken wurde.

## 2. Feste Regeln (eigene Messungen, `pruef/gegen/log/`)

| Regel | Beleg | Ergebnis |
|---|---|---|
| Importer liest das GLB, Skelett und 15 Clips | Dump-Teil vor ELEMENTS (46.433 Zeilen) alt == neu, MD5 8b33202e. `g_regeln.py`: je Clip T und M `array_equal`, OFFSET, BIND, Namen und Eltern gleich (`g_regeln.txt`). Datei: `glb_json_out.txt` "Animationen byte-gleich, abweichende Puffer 0", Knoten-TRS und inverseBind byte-gleich | ja |
| <= 20.000 Dreiecke, <= 4 Einfluesse, Summe 1 | 19.426, max 4, Summe 0,9999999..1,0000002, 0 negativ, 19 Knochen. 1 Netz, 1 Primitiv, 0 Material | ja |
| Kopf bleibt so | `kopf_out.txt`: 1.333 Kopfpunkte, davon 1.331 Lage+UV+Gewichte bit-gleich und 2 um 5e-5 mm (Float-Rauschen wie baer-fell). Normalen am Nahtrand 14 verschieden. `textur_out.txt`: Kopf-Texel 2048 und 1024 0 verschieden (Rand 1 px: 1 in 1024) | ja |
| Krallen | hinten 228/228 alle Werte gleich. Vorn 227 starr verschoben, max 10 mm (= K1). Krallen-Abtastung 455/455 gleich | ja |
| Boden / Liegen | `tiefst_out.txt`: VERSTOESSE 0. Dead tiefster Punkt 0,40 cm (>= 0,01), Death -1,42 (>= -1,81) | ja (Liegen schwebt 4 mm, m2 bekannt) |
| Dehnung | `region_tabelle_out.txt`: 99,5 % max 2,59 (<= 2,6), max 3,40 (<= 4,0), Achsel/Brust 3,26 (<= 3,5) | ja, aber nur 0,01 unter der Grenze |
| Ei | `ei_out.txt` Rear 1,3 s 1,032 (bf 1,033) | ja |
| Unterseite | `mess_textur_out.txt` spiel_hell relativ Ruecken: Achsel 0,53, Leiste 0,54, Innenbein v/h 0,44/0,49, Bauch 0,54, Hinterteil 0,60, Brust 0,50, Kehle 0,69 (Soll >= 0,40; bf 0,55/0,55/0,43/0,43/0,54/0,63/0,55/0,70) | ja |
| Straehnen (Spielgroesse, Licht B) | Eigene Renders mit den Kameras von `textur/render/pruef_final`, Messung `mess_bild.py` (`mess_bild_out.txt`, Spalte "fix"): Ruecken Kontrast 0,070 (>= 0,063), Kohaerenz 0,659 (>= 0,60) | ja (Beine: minor g4) |
| Gewichte an den Pfoten | `netz_pruef_out.txt`: unter 6 cm 100 % >= 0,95 (min 0,950), fremde Knochen 0 an allen 4 Pfoten | ja |
| Topologie | 0 offene Kanten. Kanten mit mehr als 2 Flaechen: 41, alle im festen Teil wie alt | ja |
| Dateien | genau 5 Dateien unter `mod/42/media`, keine Lua/Skripte/Testmenues. FBX ohne Nutzerpfad, laedt in Blender: 19.012 Dreiecke, UV 0..1 (`fbx_out.txt`). Deer: 40 Knochen, 19.012 Dreiecke, Skelett/inverseBind wie alt | ja |

## 3. Befunde

### Blocker
Keiner offen. Der fruehere B1 ist jetzt "formal offen, in der Sache erledigt", siehe B1.

**B1 Falten liegend.** Meine Messung (`falten_neu.txt`, `falten_detail_out.txt`) bestaetigt die Zahlen der Nachbesserung.

| Zone (Dead, sigma2 < 0,5) | neu (fix1) | baer-fell | SPEZ |
|---|---|---|---|
| Achsel + Ellbogen | 87 + 49 = **136** | 88 | <= 120 |
| Knie | 14 | 14 | - |
| alle gestauchten | 704 | 772 | - |
| sigma2 < 0,3 | 91 | 121 | <= 200 |
| Flaechenanteil Ellbogen | 25,0 % | 24,4 % | - |
| Flaechenanteil Achsel | 10,9 % | 10,9 % | - |

- Absolut ist die gestauchte Flaeche am Ellbogen 0,0192 m2 gross (baer-fell 0,0165).
- Das eigene Farbbild (`pruef/gegen/blaetter/w12_falten.png`, rot = sigma2 < 0,5) zeigt die Falten an denselben Stellen wie bei
  baer-fell. Neu ist ein Band an der Vorderkante Ellbogen/Kegel. Dafuer sind es insgesamt weniger.
- **Urteil:** Die SPEZ-Zahl ist formal gerissen. In der Sache ist nichts verloren. Die Zaehlung steigt, weil die Gelenkzonen
  dichter vernetzt sind (267/858 statt 190/688 Dreiecke).
- Eine staerkere Strafe reisst die Dehnung (Nachbesserung: 2,64). Deshalb braucht es Kevins Wort statt einer neuen Runde.

### Major
**M1-Optik Kegel ueber Ellbogen/Knie (Kevins Urteil).**
- **Ton:** Der umgeschlagene Saum ist weg. Im Ton bleibt eine glatte, steile "Glocke": dicker Oberarm, darunter ein schmaler,
  gerader Unterarm (`render/neu/s5_pranke_nah_ton.png`, `s5b_pranke_seite_ton.png`).
- **Spielgroesse:** Im Ton ist der Kegel noch zu ahnen (`w8_spiel.png` NEU Ton).
- **Textur:** Mit Textur wirkt er wie dickes Schulterfell und faellt nicht auf (`s5_pranke_nah_tex.png`).
- **Kein abgesaegtes Bein:** Die Pfote selbst ist eine Pfote.
- **Zur Entscheidung:** Ob der Kegel so bleibt, ist reine Optik und Kevins Entscheidung.

**M2 Rumpf (formal, keine sichtbare Wirkung).** Messung `rumpf_out.txt`, Ort und Knochen `log/g_rumpf_ort.txt`.
- Ueber Ruhe-z 0,36 neu -> alt: p95 0,15 cm. 13 Punkte liegen ueber 1,5 cm, max 2,31 cm (SPEZ max 1,5).
- **Neu gegenueber dem Bericht der Nachbesserung:** Umgekehrt gemessen (alt -> neu) sind es 19 Punkte bis **3,15 cm**. Der Bericht
  nennt nur die eine Richtung.
- Die Punkte liegen einzeln verstreut: Becken-Flanke, Schulter (Spine1/UpperArm), Hals, Ruecken. Es sind keine Cluster mehr.
- In den Bildern sind Silhouette und Gesaessfalte von hinten wie bei baer-fell (`w5_pranke.png` Zeile 3, `w11`).
- **Urteil:** formal offen, Kevin nimmt an oder nicht.

### Minor
- **g1 Sitz-Ferse HR.**
  - Der Bericht nennt "HR 0,26 cm". Das ist der tiefste Punkt des ganzen Beins (`detail_out.txt` (e)).
  - Die tiefste Fusshaut liegt bei **0,48 cm** (`tiefst_out.txt`: HL 0,14 / HR 0,48, heute 0,16 / 0,14).
  - Das ist besser als vorher (0,86), schwebt aber noch knapp 5 mm. Im Bild nicht zu sehen (`s1c_sitzen_ferse`).
- **g2 Aufrichten, Hinterfuss von vorn mit Textur:** heller Fleck vorn am Knoechel, darunter ein dunkler Fuss mit scharfer
  Oberkante. Wirkt leicht wie ein "Stiefel" (`render/neu/s3c_aufr_fuesse_tex.png`). Im Ton ein Fuss mit Zehen.
- **g3 Gehen, Ton:** Die Hautfalte vorn am angehobenen Ellbogen ist schaerfer als alt und wirkt wie ein Lappen
  (`render/neu/s4_gehen_seite_ton.png` bei x 300-345, y 130-225; alt an gleicher Stelle eine weichere Falte). Mit Textur unsichtbar.
- **g4 Straehnen an den Beinen schwaecher als baer-fell** (`mess_bild_out.txt`):
  - Hinterbein-Kontrast 0,059 (baer-fell 0,067).
  - Schenkel-Kohaerenz im Aufrichten 0,451 (0,669).
  - Leisten-Band-Kohaerenz 0,62 / 0,66 (0,71 / 0,71).
  - Die SPEZ-Pflicht (Ruecken) ist erfuellt. Die Beine sind schon seit der Lieferung schwaecher (minor 5).
- **g5 Dehnung ohne Reserve:** 2,59 / 3,40 / 3,26 liegt innerhalb der harten Grenzen. Das SPEZ-Ziel "nicht schlechter als
  baer-fell + 0,10" (2,45 / 3,16 / 3,02) verfehlen alle drei Werte.
- **g6 Splitter:** ohne Kantenfilter 18 Dreiecke > 4. Max **26,65** (SitDown Bild 24, Hinterschenkel aussen, Hoehe 1,15 mm);
  baer-fell max 8,28 (`splitter_out.txt`). Gefiltert unsichtbar, kann aber einen kurzen Textur-Schmierer geben (ungeprueft im Spiel).
- **g7 Krallenwurzeln hinten** -0,04..0,29 cm (Soll 0,2-0,8). Eine Wurzel liegt ausserhalb der Haut (`abnahme_out.txt`). Im Bild
  sitzen die Krallen an.
- **g8 Formziele 3.2 teils verfehlt** (`abnahme_out.txt`): Zehenstirn-Einzuege, Rillen hinten, Sohlenrand-Knick Mittel 31 Grad,
  Ballen-Relief 1,49-1,56 (Soll 1,0-1,4). Optisch nicht stoerend.
- **g9 Aufrichten-Pranke von vorn "Klotz mit Krallen":** gleich wie alt, nur mit einer Clip-Aenderung zu loesen. Vorschlag der
  Nachbesserung: Handflaeche nach vorn.
- **g10 Kleiner Schlitz am Oberschenkel im Sitzen (Ton):** gleich wie alt, nicht neu (`w1_sitzen.png` Zeile 2, `w2`).
- **g11 Belegluecken im Blatt der Nachbesserung:** In `fix1/bilder/gpu_vergleich.png` sind die Ton-Zellen "ruhe_HL_unten" (milchig)
  und "spielgross_stehen" (leer) unbrauchbar. Meine Renders decken beides ab.
  - `fix1/bilder/final/nah_b.png` enthaelt Kevins Stockfoto (Wasserzeichen). Das ist nur lokal zulaessig: nie weitergeben, nie in
    Mod oder Textur. Mein Blatt fuer Kevin enthaelt es nicht.

## 4. Was Kevin bekommt

- Vergleichsblatt `bilder/kevin_vorher_nachher.png` (2382 x 3333, MD5 26538384), alt links, neu rechts, je Ton und Textur. Zeilen:
  1. Sitzen nah (Sohle)
  2. Sitzen im Spielwinkel
  3. Aufrichten von vorn
  4. Gehen von der Seite
  5. Vorderpranke nah
- Uebernahme nur alle 5 Dateien zusammen (neues UV), relativ zu `_arbeit/baer_pfote/mod/`:

| Datei | MD5 |
|---|---|
| `42/media/models_X/Skinned/NCBear.glb` | 5066fa6774f32b52df558e9878c48610 |
| `42/media/models_X/Skinned/NCBearDeer.glb` | 1f704054a4b8a8c787a0d284d1c75683 |
| `42/media/models_X/WorldItems/NCBear.fbx` | 0cab0ff6eaee7003932c24902bca4d10 |
| `42/media/textures/Body/NCBear.png` | 4ae148dfc4028c40ee86bc42e8880880 |
| `42/media/textures/WorldItems/NCBear.png` | 603ee6998ebf3bc268019cdd53e227e2 |

- Den Bezug `fix1/bau4/textur/zw_fell_2048.png` behalten, er wird fuer den Nachbau gebraucht. Vor dem Kopieren sichern. Kopiert
  wird nur auf Kevins Wort, nicht waehrend er spielt.
- Testbefehle aus NCBearTest (`NCBearSpawn.lua:103`, `NCBearBench.lua:76/114`, `NCBearFight.lua:47` ACTS):
  - `NCBear_SpawnLive()`
  - `NCBear_Sit(20)`
  - `NCBear_AnimTest("rear")`
  - Der Kampf ist standardmaessig an (`NCBearFight.lua:205`).

## 5. Werkzeuge und Dateien (`pruef/gegen/`)

- **Eigene Werkzeuge:**
  - `werkzeug/g_regeln.py`: Clips, Gewichte, Kopf ueber Gewichte.
  - `g_ziele.py`: Pfoten-Mittelpunkte je Pose.
  - `g_auftrag.py`: Kameras alt/neu.
  - `g_streifen.py`: Arbeitsblaetter.
  - `g_kevin_blatt.py`: Vergleichsblatt fuer Kevin.
  - `g_fbx.py`: FBX laden.
  - `gpu_render_gegen.sh`: Sperre, fremdes Blender, Spiel-Pruefung.
- **Kopien ohne Aenderung der Rechnung:** `netz_pruef.py`, `detail.py`, `rumpf.py`, `regionen_kopie.py`, `region_tabelle.py`,
  `falten_detail.py`, `splitter.py`, `kopf.py`, `glb_json.py`, `textur_pruef_pfote.py`, `mess_bild.py`, `mess_textur.py`,
  `render_optik.py` (nur Pfade). Lauf: `werkzeug/messen_g.sh`.
- **Ausgaben:**
  - `log/*.txt`
  - Renders `render/alt|neu|straehnen/` (50 + 50 + 12 + 12 + 6 + 70 Bilder)
  - Blaetter `blaetter/w1..w12`
  - Dumps `dump/`
  - Auftraege `auftrag*.json`
