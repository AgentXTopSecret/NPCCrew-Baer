# Lauf baer-pfoten: Pruefer Optik (Kevins Augen), 09.11.2026

**Statisch/offline gerendert und angesehen, nicht gespielt.** Geprueft: neues GLB `_arbeit/baer_pfote/mod/42/media/models_X/Skinned/NCBear.glb`
(MD5 a6099029...) mit neuer Body-Textur (4ae60e6c..., Stand v13) gegen den Test-Mod-Stand NCBearTest (GLB 2a4837f6..., Body c2d6c8cc...).
Nichts in Test-Mod, NPC Crew, baer_fell oder an den Bauer-Dateien geaendert (MD5 vorher = nachher, 20:57), nichts committet. Eigene
Dateien nur unter `_arbeit/baer_pfote/pruef/optik/`. Alle Bilder unten habe ich selbst angesehen (Read). Kevins Vorlagen nur angesehen
und lokal neben die Renders gelegt (Blaetter), nichts davon in Mod oder Textur.

## 0. Kurz (Ergebnis zuerst)

1. **Keine Saeule mehr, in keiner Pose.** Alle vier Pfoten lesen sich in Stehen, Gehen (Fussaufsatz), Rennen, Sitzen, Aufrichten,
   Liegen, Hieb und Biss als Pfote/Fuss, im Ton-Bild UND mit Textur (Tabelle 2). Sitzen: lange Sohle mit Zehen statt runder Kappe;
   Liegen: lange Sohlen statt abgesaegter runder Scheiben; von hinten: Fuss mit Ferse statt Stumpf. Die Textur verdeckt nichts.
2. **Kein Blocker.** **2 major:**
   - **M1 Wulst/"Pluderhose" an Ellbogen und Knie:** der dicke Rumpf endet ueber dem neuen duennen Unterarm/Unterschenkel mit einem
     ueberhaengenden Saum; im Ton wie ein Hosenbein, mit Textur als dunkle Ringlinie. Ist in Spielgroesse sichtbar.
   - **M2 Hintersohle nicht wie Kevins Foto:** die gemalte Platte ist ein Schild mit spitzem Ende und hoert ueber der Ferse auf; die
     Ferse ist Fell. Die Zehen sind lang wie Finger, die Zehenballen klein. Sohle glatt und gleichmaessig grau, kein Reifenprofil mehr.
3. **6 minor** (Abschnitt 4): Pranke von unten kastig mit Querstreifen, heller Handwurzelballen wie ein Kiesel, kleiner Schlitz in der
   Kniekehle im Sitzen, Sohlenrand im Ton zackig, weniger Straehnen am Unterbein, Aufrichten-Pranke von vorn wie bisher "Maul mit
   Zaehnen" (Clip-Sache).
4. Nicht schlechter als baer-fell: Kopf gleich (Pixelvergleich: Abweichungen nur am Bildrand Hals/Bein, x < 162 von 500), Rumpf,
   helle Unterseite, Straehnen am Rumpf und Ei-Form sehen gleich aus. Das Netz hat keine offenen Kanten (alt 0, neu 0).

**Regel-Hinweis (GPU):** Kevins weitergeleiteter Satz lautet *"loesch die regel die hab ich nie gemacht!"*. Der Auftrag liest ihn als
"rendern auch bei laufendem Spiel erlaubt". Der Satz laesst sich auch anders lesen. Ich habe keine Regel geaendert, das ist nicht
mein Schritt. Mein Wrapper `pruef/optik/werkzeug/gpu_render_pruef.sh` prueft vorsichtshalber trotzdem auf das Spiel und haette
gewartet. ProjectZomboid lief bei **keinem** meiner vier Render-Laeufe (20:47-20:49 und 20:54-20:55, Protokoll
`pruef/optik/log/gpu_protokoll.txt`). Damit stimmen meine Renders mit beiden Lesarten ueberein. Projekt-`CLAUDE.md` Abschnitt 5
enthaelt die Regel "nie rendern, waehrend er spielt" weiterhin. **Welche Regel Kevin loeschen will, muss der Workflow mit ihm klaeren.**

## 1. Wie gerendert

- Eigene Dumps mit dem Importer des Spiels (`_arbeit/baer_spiel/harness/Dump.java`): `pruef/optik/dump/dump_neu.txt` (aus dem Mod-GLB;
  byte-gleich zu `dump_final.txt` des Netz-Bauers) und `dump_alt.txt` (aus NCBearTest).
- Werkzeug `pruef/optik/werkzeug/render_optik.py` = Kopie von `werkzeug/render_optik.py` (Haeutung wie der Importer). Gerendert nur
  auf der RTX 4090 mit OptiX und OptiX-Entrauscher (assert im Skript, Log `BILD Geraete ['NVIDIA GeForce RTX 4090']`).
- Wrapper `gpu_render_pruef.sh` = Kopie von `gpu_render.sh`: Sperre `gpu.lock` und Warten auf fremdes Blender. Dazu kommt die
  Spiel-Pruefung (siehe 0). Um 20:54 lief ein fremdes `explosion_sim.py` (andere Sitzung). Es war beendet, bevor mein Lauf startete.
- **Ton** = graues Material ohne Textur. **Textur** = Licht B (`spielB`, an Kevins Spielbildern kalibriert, baer_fell
  pruef_optik.md 1).
- Kameras alt/neu gleich (`pruef/optik/auftrag_*.json`, `auftrag2_*.json`, erzeugt von `werkzeug/auftrag.py` / `auftrag2.py`):
  - **Spielwinkel nah:** el 30, az zur Pfote gedreht.
  - **Flach von aussen:** el 0-10, Profil Ferse/Zehen.
  - **Spielgroesse:** `pxu 560` = Kevins 4K-Zoom, el 30; halb `pxu 280`.
  - **Beschwerde-Kameras:** die vier Kameras der Bilder hinter Kevins Beschwerde (`b6_sit_fuss`, `x_B_rear_pranken`,
    `pfote_vorn_nah`, `pfote_hinten_nah`).
  - **Weitere:** Sohlen von unten, Kopf, Unterseite, Hinterteil.
- **Posen** (Fussaufsatz aus dem Dump bestimmt, `pruef/optik/werkzeug/ziele.py`, `log/ziele_neu.json`):

  | Pose | Clip, Bild |
  |---|---|
  | Stehen | Idle01 Bild 0 |
  | Gehen (Fussaufsatz je Pfote) | Walk VL Bild 2, VR 16, HL 26, HR 12 |
  | Rennen | Run VL Bild 7, VR 9, HL 0, HR 1 |
  | Sitzen | NCBear_Sit Bild 60 (2,0 s) |
  | Aufrichten | NCBear_Rear Bild 39 (1,3 s) |
  | Liegen | DeerStag_Dead |
  | Hieb | SwipeR/SwipeL Bild 18 (0,6 s) |
  | Biss | NCBear_Bite Bild 16 (0,533 s) |

  Dazu je Pfote das tiefste Bild in Gehen/Rennen (Zehen im Boden?) und die Ferse im Sitzen von der Seite.
- 223 + 223 Einzelbilder in `pruef/optik/render/neu/` und `render/alt/`. Blaetter (alt Ton | alt Textur | NEU Ton | NEU Textur) in
  `pruef/optik/blaetter/`, Ausschnitte in `pruef/optik/zoom/`.

## 2. Pfote oder Saeule? (je Pose und Pfote, Ton und Textur)

Alle Pfade relativ zu `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/pruef/optik/`.

| Pose | VL | VR | HL | HR | Bilder |
|---|---|---|---|---|---|
| Stehen | Pfote | Pfote | Pfote | Pfote | `blaetter/p_stehen_spiel.png`, `p_stehen_flach.png`, `k_beschwerde_kameras.png` (Zeile 3/4), `zoom/stehen_a135_beine_2x2.png` |
| Gehen (Aufsatz) | Pfote | Pfote | Pfote | Pfote | `blaetter/p_gehen_spiel.png`, `p_gehen_flach.png`, `x_boden.png` |
| Rennen | Pfote | Pfote | Pfote | Pfote | `blaetter/p_rennen_spiel.png`, `p_rennen_flach.png`, `x_boden2.png` |
| Sitzen | Pfote | Pfote | Pfote | Pfote | `blaetter/p_sitzen_spiel.png`, `p_sitzen_flach.png`, `k_beschwerde_kameras.png` (Zeile 1), `v_vorlage.png` |
| Aufrichten | Pfote (kastig) | Pfote (kastig) | Pfote | Pfote | `blaetter/p_aufrichten_spiel.png`, `p_aufrichten_flach.png`, `x_rear_pranken.png`, `x_rear_pranken2.png` |
| Liegen | Pfote | Pfote | Pfote | Pfote | `blaetter/p_liegen_spiel.png`, `p_liegen_flach.png` |
| Hieb | Pfote | Pfote | Pfote | Pfote | `blaetter/p_hieb_spiel.png`, `p_hieb_flach.png` |
| Biss | Pfote | Pfote | Pfote | Pfote | `blaetter/p_biss_spiel.png`, `p_biss_flach.png` |
| Spielgroesse (alle) | Pfote | Pfote | Pfote | Pfote | `blaetter/g_spielgroesse_1..4.png`, `h_halb.png` |

Zum Vergleich alt: In denselben Blaettern ist die alte Pfote in Stehen/Gehen/Rennen hinten und in Sitzen/Liegen eine Saeule mit
runder, flacher Stirn: `p_sitzen_spiel.png` alt Ton, `p_liegen_flach.png` alt Ton, `zoom/stehen_a135_beine_2x2.png` oben.
Kevins Beschwerde stimmt fuer den alten Stand.

**Eigene Schnitte im Stehen** (`log/schnitte_stehen.txt`, Spiel-cm, Laenge vorn-hinten):

| Pfote | Laenge am Boden (z 3) | Bein (z 15) | Bein (z 20) | |
|---|---|---|---|---|
| HL alt | 43,1 | 37,2 | 36,6 | = Saeule |
| HL neu | 44,3 | 22,2 | 20,4 | Fuss 2,2 x so lang wie das Bein dick |
| VL alt | 34,7 | 27,5 | 28,6 | |
| VL neu | 31,0 | 18,6 | 19,6 | Faktor 1,6 |

- Zehen hinten ragen vor das Schienbein: z 3 vorn 18,3 gegen z 15 vorn 39,4, also 21 cm.
- Ferse hinten 62,6 gegen Bein 60,5, also 2 cm.
- Das deckt sich mit `bau_netz.md` 3.2.

## 3. Kevins Fragen

| Frage | Antwort | Bilder |
|---|---|---|
| Pfote oder Saeule? | **Pfote, ueberall** (Tabelle 2). | `blaetter/a0_uebersicht.png` |
| Ferse, Sohle, Zehenreihe, Krallen an der richtigen Stelle? | **Ja:** Ferse hinten, Zehenreihe vorn, Krallen an den Zehenspitzen. **Hinten im Sitzen:** Ferse unten, Sohle zur Kamera, Zehen oben wie in Kevins Vorlage. **Aber:** Die gemalte Platte endet spitz ueber der Ferse (M2). Die Zehen sind lang und einzeln wie Finger. Die Krallen wirken von vorn wie Kappen auf den Zehenspitzen (Krallenwurzel an der Oberflaeche, `bau_netz.md` 3.2). | `render/neu/k_sit_fuss_nah_ton.png`, `zoom/k_sit_fuss_nah_tex_zehen.png`, `blaetter/x_boden2.png` (Zeile 3/4) |
| Uebergang Bein -> Fuss natuerlich (kein Absatz, kein Kragen, kein Loch)? | **Gelenk -> Fuss: ja,** weich, kein Loch (0 offene Kanten, `log/loch_kopf.txt`). **Hoeher, an Ellbogen und Knie: nein.** Dort sitzt ein neuer Wulst mit Saum (M1). | `blaetter/x_knie.png`, `zoom/ganz_stehen_beine_2x2.png`, `zoom/aufrichten_a0_beine_2x2.png` |
| Sohle wie im Foto (grosse helle Lederballen) oder Reifenprofil? | **Kein Reifenprofil mehr.** **Hinten:** eine grosse, glatte, sehr gleichmaessig hellgraue Platte (wirkt wie eine Einlegesohle), Zehenballen klein und dunkel umrandet. **Vorn:** ovaler Handballen gut, Zehenballen klein. Der helle Ring um die Sohle ist weg; die Sohle endet in braunem Fell. | `blaetter/v_vorlage.png`, `u_sohlen_unten.png`, `zoom/unten_HL_kontrast_vorlage.png` |
| Fell am Fussruecken? | **Ja,** braunes Fell bis zu den Zehen, dunkler als der Rumpf (dunkle "Socken", wie beim echten Grizzly). Weniger Straehnen als am Rumpf (minor 5). | `render/neu/k_pfote_hinten_nah_tex.png`, `k_pfote_vorn_nah_tex.png` |
| Nichts schlechter als baer-fell (Unterseite, Straehnen, Ei, Kopf)? | **Kopf** gleich (`blaetter/r_rest.png` Zeile 1; Pixelvergleich `log/loch_kopf.txt`: 16.587 Pixel > 8 abweichend, alle bei x < 162 = Hals/Bein, keiner am Kopf). **Unterseite, Rumpf, Ei-Form** sehen gleich aus. **Unterbeine** weniger Straehne (minor 5). | `blaetter/r_rest.png`, `g_spielgroesse_1..4.png` |

## 4. Befunde

### Blocker
Keiner. Keine Saeule und kein abgesaegtes Bein in irgendeiner Pose. Die festen Regeln habe ich optisch nicht verletzt gefunden:

- Kopf gleich.
- Kein Clip sichtbar tiefer im Boden: `blaetter/x_boden.png` und `x_boden2.png` zeigen Zehen/Krallen am tiefsten Bild wie alt.
- Liegen auf gleicher Hoehe.

### M1 (major) Wulst/Saum an Ellbogen und Knie ("Pluderhose")

**Was man sieht:**
- Im Ton endet der dicke Oberarm/Oberschenkel mit einem runden, ueberhaengenden Saum ueber dem neuen duennen Unterarm/Unterschenkel.
  Von vorn im Aufrichten sieht das wie eine Pluderhose aus (`zoom/aufrichten_a0_beine_2x2.png` unten links).
- Mit Textur steht an der Saumkante eine dunkle Ringlinie wie ein Buendchen (`render/neu/x_knie_VL_tex.png`,
  `render/neu/rennen_VL_spiel_tex.png` oben). Im Rennen und beim Hieb wirkt der Unterarm "eingesteckt"
  (`blaetter/p_rennen_spiel.png` VR, `p_hieb_spiel.png` VR).
- In Spielgroesse sichtbar (`zoom/ganz_stehen_beine_2x2.png`, aus `render/neu/ganz_stehen_a300_ton|tex.png`).
- Alt gab es diesen Saum nicht: das Bein war bis unten dick.
- Kevin fragt ausdruecklich nach "kein Kragen". Der Uebergang Gelenk -> Fuss ist gut, der Kragen sitzt eine Etage hoeher.

**Gemessen:**
- Nach unten gewandte Flaeche (Normale z < -0,3) je Bein in 20-40 cm Hoehe, Stehen, Spiel-cm² (`log/wulst_unterseite.txt`):

  | Pfote | alt | neu |
  |---|---|---|
  | VL | 84 | 1.077 |
  | VR | 84 | 1.061 |
  | HL | 799 | 1.496 |
  | HR | 795 | 1.425 |

- Aussenkante VL (`log/profil_aussen.txt`): von z 2 bis 16 flach bei 31 cm, dann 36,1 (z 28) -> 43,2 (z 34), also 7 cm nach aussen
  auf 6 cm Hoehe.

**Vorschlag:**
- Netz: den Uebergang Rumpfhuelle -> Pfotenhuelle (`baer_export_pfote.py`, Uebergang nach Landehoehe z 0,28-0,35 und Knie-Band)
  ueber 15-20 cm statt ~7 cm auslaufen lassen, also den Unterarm/Unterschenkel oben dicker anschliessen (Kegel statt Stufe).
- Textur: die dunkle Ringlinie an der Saumkante einebnen (`bau_textur.md` Abschnitt 7 kennt sie als "feine dunkle Querlinie").

### M2 (major) Hintersohle: spitzes Schild statt ovaler Platte mit runder Ferse, Fingerzehen

**Was man sieht:**
- Textur: Die gemalte Hintersohle laeuft zur Ferse in eine Spitze aus (Schild/Pfeilspitze) und endet einige cm ueber dem
  tiefsten Punkt der Ferse; die Ferse selbst ist Fell (`render/neu/x_sit_HL_ferse_tex.png`, `sitzen_HL_flach_tex.png`,
  `blaetter/u_sohlen_unten.png` HL/HR, `zoom/unten_HL_kontrast_vorlage.png`).
- Kevins Vorlage (`kevin_baerenfuss_vorlage.png`, Auftrag): ovale Platte, Ferse unten rund, grosse Zehenballen dicht im Bogen.
- Bei uns sind die Zehenballen klein, dunkel umrandet und durch einen dunklen Streifen von der Platte getrennt
  (`zoom/k_sit_fuss_nah_tex_zehen.png`). Die Platte ist glatt und einfarbig hellgrau (wie eine Einlegesohle).
- Form (Ton): Die fuenf Hinterzehen sind lang, zylindrisch und tief getrennt, eher wie Finger als wie kurze Baerenzehen
  (`render/neu/k_sit_fuss_nah_ton.png`, `sitzen_HL_flach_ton.png`).
- Im Sitzen ist das Kevins wichtigste Ansicht (Blatt `blaetter/v_vorlage.png` Zeile 2 neben seiner Vorlage).

**Vorschlag:**
- Textur (`baer_textur_pfote.py` `sohlen_malen`, Plan `netz/sohle_layout.json`): Plattenumriss zur Ferse rund schliessen, bis an
  den tiefsten Punkt der Ferse ziehen und den Fersen-Hochzug einbeziehen. Zehenballen groesser und naeher an die Platte, Fellstreifen
  dazwischen schmaler. Etwas Leder-Unruhe in die Platte.
- Netz (`baer_quelle_pfote.py` `pf_zehen_ell`): Zehen kuerzer und dicker, Rillen oben flacher.

### Minor
1. **Vorderpranke von unten kastig:**
   - Umriss ein Rechteck mit runden Ecken, laenger als breit. Ein dunkler Querstreifen liegt zwischen Handballen und
     Handwurzelballen, der Handwurzelballen sitzt seitlich (`render/neu/unten_VL_tex.png`, `unten_VL_ton.png`,
     `x_rear_VL_untenvorn_tex.png`).
   - Nur von unten zu sehen (Aufrichten von unten, Liegen). Im Spielwinkel von oben unauffaellig. Bauer kennt es (`bau_netz.md` 4).
2. **Heller Handwurzelballen von der Seite/hinten wie ein angeklebter Kiesel**, im Stehen/Gehen hinter dem Vorderhandgelenk
   (`render/neu/gehen_VR_flach_tex.png`, `x_walk_VR5_tex.png`, `zoom/stehen_a135_beine_2x2.png` unten rechts). Etwas dunkler oder
   kleiner malen.
3. **Kleiner Schlitz in der Kniekehle im Sitzen** (neu, alt nicht). Im Ton ein offener Spalt mit heller Kante, mit Textur eine
   duenne dunkle Linie (`zoom/sit_kniekehle_2x2.png`, aus `render/neu/k_sit_fuss_nah_ton.png` um x 175-200, y 240-250). Vermutlich
   die Stelle "Rumpf max 2,10 cm an der Innenseite der Hinter-Kniekehle" aus `bau_netz.md` 3.1 (ungeprueft).
4. **Sohlenrand im Ton facettiert/zackig**, von der Seite und von hinten unten; mit Textur unsichtbar
   (`render/neu/stehen_HL_flach_ton.png`, `blaetter/p_stehen_flach.png`). Bauer kennt es.
5. **Unterbein-Fell glatter, weniger Straehne als baer-fell**, sichtbar nah an den Unterschenkeln (`blaetter/p_stehen_flach.png`
   NEU Textur). Der Bauer misst Hinterbein-Kontrast 0,053 statt 0,067 (`bau_textur.md` 4); selbst nicht nachgemessen.
6. **Aufrichten, Vorderpranke von vorn auf Augenhoehe:**
   - Man blickt auf das Pfotenende: ein dunkler Block mit Krallen in einem dunklen Fellring, wie ein "Maul mit Zaehnen"
     (`render/neu/aufrichten_VR_flach_tex.png`, `k_rear_pranken_nah_tex.png`).
   - Alt war es genauso (`render/alt/aufrichten_VR_flach_tex.png`, `render/alt/k_rear_pranken_nah_tex.png`), also kein Rueckschritt. Von der Seite und im Spielwinkel ist es eine Pfote
     (`blaetter/x_rear_pranken.png`).
   - Kevins Vorlage zeigt die erhobene Pranke mit der Handflaeche zur Kamera; das geht nur mit Drehung im Clip.
     **Vorschlag fuer die Clip-Runde**, nicht aendern.

## 5. Dateien (alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/pruef/optik/`)

| Was | Dateien |
|---|---|
| Uebersicht | `blaetter/a0_uebersicht.png` (alt Textur, alt Ton, neu Ton, neu Textur je Pose), `blaetter/a1_maengel.png` (M1, M2, minor) |
| Je Pose | `blaetter/p_<pose>_spiel.png`, `p_<pose>_flach.png` |
| Spielgroesse | `g_spielgroesse_1..4.png`, `h_halb.png` |
| Beschwerde-Kameras | `k_beschwerde_kameras.png` |
| Sohlen | `u_sohlen_unten.png` |
| Vorlagen | `v_vorlage.png` |
| Rest | `r_rest.png` |
| Zusatz | `x_rear_pranken.png`, `x_rear_pranken2.png`, `x_boden.png`, `x_boden2.png`, `x_knie.png` |
| Einzelbilder | `render/neu/`, `render/alt/` (je 223) |
| Ausschnitte | `zoom/` |
| Auftraege | `auftrag_alt.json`, `auftrag_neu.json`, `auftrag2_alt.json`, `auftrag2_neu.json` |
| Messungen | `log/schnitte_stehen.txt`, `log/profil_aussen.txt`, `log/wulst_unterseite.txt`, `log/loch_kopf.txt`, `log/ziele_neu.json`, `log/gpu_protokoll.txt`, `log/render*.log` |
| Werkzeuge | `werkzeug/` (`render_optik.py`, `dumpread.py` = Kopien; neu `auftrag.py`, `auftrag2.py`, `blatt.py`, `ziele.py`, `schnitte.py`, `profil.py`, `wulst.py`, `loch_kopf.py`, `gpu_render_pruef.sh`, `info.py`) |
| Dumps | `dump/dump_neu.txt`, `dump/dump_alt.txt` |
