# Lauf baer-fell: Pruefer Technik

Stand 09.11.2026, PZ 42.21, Blender 5.2.3, JDK 25. **Statisch/offline geprueft, nicht gespielt.** Keine GPU benutzt (kein Render),
nichts in die Test-Mod, nach NPC Crew oder in Dateien der Bauer geschrieben, nichts committet. Eigene Dateien nur in
`_arbeit/baer_fell/pruef/technik/`. Die Dateien des abgebrochenen Anlaufs in `pruef/` (dump_*.txt, glb_pruef_out.txt, dump/, ref/)
habe ich weder verwertet noch geloescht; alle Dumps hier sind neu erzeugt.

Geprueft: `_arbeit/baer_fell/mod/42/media/` (neu) gegen `Zomboid/mods/NCBearTest/42/media/` (alt, nur gelesen).

## 0. Ergebnis kurz

- **Kein Blocker.** Alle festen Regeln halten, mit eigenem Beleg: 15/15 Clips bit-gleich (auch in der Datei), Knochen/Namen/Eltern,
  Offset- und Bind-Matrizen bit-gleich, 18.870 Dreiecke nach dem Importer, <= 4 Einfluesse, Summe 1, ein Netz, Kopf- und Krallenpunkte
  bit-gleich, Liegehoehe gleich, Texturen gleicher PNG-Typ und gleiche Groesse, Kopf-Texel bit-gleich, Maul-Flecken frei und
  unveraendert, Pfade gleich, nur die 5 Dateien.
- **Nachbau ohne GPU byte-gleich:** GLB `c8250ace`, Body-Textur `79a9aca4`, WorldItems-Textur `9395c7fe`, Kopf-Variante `7c466a70`,
  NCBearDeer.glb `c5cc07bb` (das FBX nur wegen Zeitstempel und Pfad nicht, seine Geometrie ist gleich).
- **Dehnung selbst gemessen:** alle Dehnungsziele der Forschung erreicht (99,5 % hoechstens 2,48, Hoechstwert 3,37, Achsel/Brust in
  Rear/Sitzen/Hieb/Slam hoechstens 3,04). Pflichtpunkt 3 erfuellt.
- **Jar-Beleg "Tiere: keine Mipmaps" stimmt.** "2048 flimmert" ist eine Folgerung daraus, im Spiel nicht gesehen.
- **1 x major:** Falten Achsel+Ellbogen im Liegen 154 statt Ziel <= 120 (Kevins Punkt 6). **8 x minor** (Abschnitt 8).

## 1. Wie geprueft (eigene Werkzeuge, nicht die Zahlen der Bauer)

| Was | Werkzeug (in `pruef/technik/`) | Ausgabe |
|---|---|---|
| GLB mit dem Importer des Spiels lesen (alt, neu, beide Deer) | `baer_spiel/harness/Dump.java` (gleiche 7 Nachbearbeitungs-Schritte wie `FileTask_LoadMesh.loadGLTF`, per javap geprueft) | `dump/alt.txt`, `dump/neu.txt`, `dump/deer_*.txt` |
| GLB-Datei direkt (JSON, Puffer): Netze, Material, Bilder, Skin, Animationen byte-weise | `glb_json.py` | `glb_json_out.txt` |
| Clips, Matrizen, Netz, Gewichte, Tiefpunkte, Dehnung (SVD je Dreieck, alle Bilder), Umklapper | `analyse.py` | `analyse_out.txt` |
| Kopf/Krallen ueber die Ecken der ALTEN Lowpoly (gegend 1/2), Lage+UV+Gewichte+Normale, Kopf in Bewegung | `kopf.py` | `kopf_out.txt` |
| Dehnung je Region (Regeln der Forschung `werkzeug/regionen.py`, an meinen Dumps) | `region_tabelle.py` | `reg_alt/`, `reg_neu/`, `region_tabelle_out.txt` |
| Falten liegend/sitzend | `netz/falten_fell.py` an meinen Dumps | `falten_out.txt` |
| Texturen: PNG-Kopf, Kopf-/Krallen-Texel, Maul-Flecken, UV-Ueberlappung, Saum, Straehnen, Sohle, Kopf-Variante | `textur_pruef.py`, `uv_pruef.py` | `textur_out.txt`, `uv_out.txt`, `straehnen_out.txt`, `sohle_out.txt`, `kopfvariante_out.txt` |
| Jar | javap auf eigene Auszuege `jar/` | `javap_*.txt` |
| Nachbau | `repro/lauf.sh` (Abschnitt 6) | `repro/lauf_out.txt`, `repro/tier.log` |

Hinweis zu `analyse_out.txt`: die Zeile "Haut mit der Bind-Pose ... 1,40" ist ein Fehlversuch meinerseits (die `bindPose` des Dumps
laesst sich so nicht verketten) und sagt nichts ueber das Modell. Die Haut-Rechnung (`tier_pruef_lib.skin`) habe ich anders bestaetigt:
Idle-Bild 0 hat fast dieselbe Huelle wie die Ruhe (bis 12 mm), tiefster Punkt Idle 0,0000 m, Dead 0,0001 m (= Liegehoehe aus `liege_alt.json`).
Die Kopfmaske in `analyse.py` (UV-Raster) zaehlt zu wenig; massgeblich fuer Kopf/Krallen ist `kopf_out.txt`.

## 2. Feste Regeln (alle erfuellt)

| Regel | Beleg | Ergebnis |
|---|---|---|
| 15 Clips bit-gleich | `analyse_out.txt` 1 (Dauer, Abtastzeiten, Schluessel, Modellmatrizen `==`), `glb_pruef_out.txt`, `glb_json_out.txt` ("Animationen in der Datei byte-gleich ... abweichende Puffer 0") | ja, 15/15, auch die Puffer in der Datei |
| Knochen, Namen, Eltern, Offset, Bind | `analyse_out.txt`: 26/26, Offset/Bind `==` (max 0); Datei: 28 Knoten TRS gleich, inverseBind byte-gleich | ja |
| <= 20.000 Dreiecke nach dem Importer | Dump: **18.870** (alt 18.040), Datei 18.870 | ja (Budget 19.600) |
| <= 4 Einfluesse, Summe 1 | Datei WEIGHTS_0 und Dump: max 4, Summe 1,000000..1,000000, keine negativen; Knochen mit Gewicht 19 = alt | ja |
| ein Netz / ein Material | Datei: 1 Netz, 1 Primitiv, **kein** Material (wie alt), keine Bilder | ja |
| Kopf bleibt so | `kopf_out.txt`: Kopf 1.333/1.333 Dump-Punkte Lage+UV bit-gleich, 1.316 auch Normale (17 liegen direkt auf der Naht, Normale dort bis 1,7 Grad gedreht); Gewichte s. Befund m2 | ja |
| Krallen unveraendert | 455/455 Dump-Punkte in allen 16 Werten bit-gleich | ja |
| Liegehoehe Death/Dead | `analyse_out.txt` LIEGE: tiefster Punkt alt 0,0001 / neu 0,0001 m in beiden; Clips bit-gleich | ja |
| tiefster Punkt je Clip nicht tiefer | `analyse_out.txt` TIEF: 15/15 gleich oder hoeher (SwipeL +3,9 mm, Rear +0,6 mm) | ja |
| Sohlen haengen am Hand/Fuss (kein neues Gleiten) | 1.250 Sohlen-Dump-Punkte: Gewicht Hand/Fuss = 1,0000 | ja |
| Pfade und Namen | 5 Dateien unter denselben relativen Pfaden; Skripte `nc_bear_tier.txt`, `nc_bear.txt` unveraendert passend | ja |
| Texturformat | `textur_out.txt`: Body 1024x1024, WorldItems 2048x2048, beide 8 Bit RGB (Farbtyp 2), ohne Interlace, gleiche Bloecke wie alt | ja |
| Kopf-Texel der Vorgabe bit-gleich | 2048: Kopf-Inseln +3 px 878.054 Texel, 0 verschieden; Body 1024: Kopf-Inseln +1 px 217.189 Texel, 0 verschieden (+2 px: 10, +3 px: 142 = Nachbar-Rumpf) | ja |
| Maul-Flecken frei | drei Flecken samt 4 px Saum: Pixel alt == neu, 0 Texel unter Rumpf-/Kopf-UV | ja |
| Dateiliste | `mod/42/media`: genau NCBear.glb, NCBearDeer.glb, WorldItems/NCBear.fbx, Body/NCBear.png, WorldItems/NCBear.png; keine Lua, kein Skript, kein Test-/Cheat-Inhalt | ja |
| Originale `*_anim.py` | `git diff` im Repo `baer/`: unveraendert gegen HEAD | ja |
| Zeilenenden | `baer_*_fell.py` alle Zeilen CRLF wie die Originale, alle vier parsen | ja |
| nichts kopiert | Bau-Skripte lesen keine Kevin-Bilder/Netz-Daten (grep), Sohle prozedural aus `sohle_layout.json` | ja |
| Geometrie sauber | keine entarteten Dreiecke, keine UV-Ueberlappung zwischen Inseln (`uv_out.txt`, 65 Inseln, je Sohle genau 1). Ruhe-Umklapper 3 (2 im Maul), 164 Flaechen an Kanten mit != 2 Flaechen - **alle** im festen Kopf/Maul und genau wie alt | ja |

## 3. Netz-Ziele der Forschung (selbst gemessen)

Dehnung = groesste Hauptdehnung je Dreieck ueber alle Bilder, ohne Kopf/Krallen/Maul (eigene SVD `analyse_out.txt`; Regionen nach
`werkzeug/regionen.py` an meinen Dumps `region_tabelle_out.txt`; beide stimmen mit der Tabelle in `bau_netz.md` 3.4 auf +-0,02 ueberein).

| Ziel (forschung_bestand.md 6) | alt | **neu** | erreicht |
|---|---|---|---|
| 99,5 % <= 2,6 je Clip | bis 4,13 (SwipeL) | **2,48** (SwipeR) | ja |
| max <= 4,0 je Clip | bis 14,21 | **3,37** (Sit, Ruecken/Flanke am Hals) | ja |
| Achsel/Brust max <= 3,5 in Rear, Sit*, Swipe*, Slam | Achsel 8,21 / Brust 4,50 | **3,04** (Brust SwipeR), Achsel 2,89 | ja (Wunsch 3,0 knapp verfehlt) |
| Kevins Werte "Hieb bis 6,9, Aufrichten 4,8" | Achsel SwipeL 6,06, SwipeR 8,21, Slam 6,35, Rear 3,29 | 2,67 / 2,89 / 2,37 / 2,44 | deutlich gesenkt |
| Kanten max <= 4,0 (Rumpf) | 4,20-5,87 | Rumpf max 3,17 (`glb_pruef_out.txt`); alle Kanten mit Maulwinkel Rear 4,12 (Kopf fest) | ja |
| Idle 99,5 % <= 1,3; Walk/Run nicht schlechter | 1,29; 3,03/3,52 | 1,20; 1,95/2,31 | ja |
| Dead sigma2 < 0,3 <= 200 | 408 | **194** | ja (knapp) |
| Achsel+Ellbogen sigma2 < 0,5 liegend <= 120 | 165+75 = 240 | **97+57 = 154** | **nein** (Befund M1) |
| Schulter/Huefte Rear 1,3 s >= 0,95 | 0,866 (Armgewicht < 0,05) / 0,924 (< 0,3) | **0,923 / 0,941** | **nein** (Befund m1) |
| Sohle: je Pfote 1 Insel, Ballen 4-10 mm | - | 4 Inseln; Sohlenpunkte z 0..24 mm, Median 8 mm | ja |
| Umklapper in Bewegung (Flaeche gegen geschweisste Punktnormale, nur neue) | z. B. Run 388, Death 471, Slam 176 | 315, 299, 130; mehr nur Rear 126->133, Dead 82->84 | nicht schlechter (Hinweis) |

## 4. Textur

- Groesse, Typ, Pfade, Kopf-Texel, Maul-Flecken: Abschnitt 2 (alles ja).
- Saum: Texel 1-2 px ausserhalb der Inseln mit Luma < 20: alt 22,0 %, neu 0,26 % (`uv_out.txt`) - keine dunklen Naehte mehr aus dem Saum.
- Sohle in der Spiel-Textur (Body 1024): Luma p5 42 / p50 65 / p95 105 - Ballen und Furchen ueberleben die 1024 (2048: 42/65/106).
- Straehnen in der 1024er (`straehnen_out.txt`, Bandpass in den Regionen der Forschung): Ruecken/Flanke 1,2-3,1 cm Std 6,59 -> 7,10 sRGB
  (+8 %), 3,1-9,3 cm 6,28 -> 5,89; Unterseite mehr Struktur absolut (Bauch 5,73 -> 6,44, Hinterteil 4,13 -> 6,69). Befund m4.
- Kopf-Variante `textur/NCBear_kopf_variante_body1024.png`: gleicher PNG-Typ, Unterschiede nur in Kopf-Inseln + 4 px, 0 Texel in Rumpf-
  oder Krallen-Inseln, Maul-Flecken gleich - als reiner Tausch von `textures/Body/NCBear.png` brauchbar (Kevins Wahl).
- Nicht selbst gemessen (Sache des Optik-/Textur-Blicks): Uneinigkeit 1,18-2,32 (Ziel 1,1), Struktur Bauch/Hinterteil/Kehle 0,81-0,86.

## 5. Jar-Beleg "Tiere: keine Mipmaps, 2048 flimmert" (forschung_engine.md 1.3)

Selbst aus `projectzomboid.jar` gezogen und mit javap gelesen (`javap_*.txt`):
- `ModelInstanceTextureCreator.init(AnimalVisual, ModelInstance)` Offset 134: `Texture.getSharedTexture(String)`; diese setzt nur Flag 4
  bei Kompression (`Texture.getSharedTexture(String)` Offset 0-18) -> kein Flag 128, also **kein Groessendeckel** fuer die Tier-Textur.
- `ModelManager.getTextureFlags` Offset 15-18: `getOptionModelTextureMipmaps` -> `ifeq 21` springt auf die naechste Anweisung (leerer Zweig).
- `TextureCombiner.combine` Offset 815-821: derselbe leere Zweig. `createMipMaps` (einziger Aufruf von `glGenerateMipmap` dort) ist nur
  definiert: im ganzen Jar verweist keine andere Klasse darauf, in `TextureCombiner` selbst kein Aufruf.
- `TextureCombiner.createTexture`: `glTexImage2D` nur Stufe 0, `GL_TEXTURE_MAG_FILTER` und `GL_TEXTURE_MIN_FILTER` = 9729 (GL_LINEAR).
  Das Modell bekommt diese Kopie (`ModelInstanceTextureCreator.render` Offset 71-165: `createFullCharacterTexture`, `applyCharacterTexture`).
- **Ergebnis:** "keine Mipmaps" stimmt. "Flimmert" ist die Folge (Verkleinern ohne Mipmaps mit GL_LINEAR mischt nur 2x2 Texel) und bei
  der geschaetzten Zoomstufe (~1,2 Texel je Bildpunkt bei 1024) plausibel, aber **ungeprueft im Spiel**. Kevins Wunsch (2) "hoeher
  aufgeloest" ist damit begruendet nicht umgesetzt; ein A/B im Spiel waere der einzige echte Beleg.
- Nebenbei bestaetigt (Alpha-Haarkarten, Kevins Punkt 8): `combine` Offset 422-442 `glBlendFuncSeparate(blendSrc, blendDest, blendSrcA,
  blendDestA)`, Vorgaben in `TextureCombinerCommand` 770/771/.../771 - die Vormultiplikation, auf der das "nein" der Forschung beruht.
- Die GLB-Nachbearbeitung in `FileTask_LoadMesh.loadGLTF` sind genau die 7 Schritte, die `Dump.java` nutzt.

## 6. Nachbau ohne GPU (`pruef/technik/repro/lauf.sh`, 14,5 min)

Die dokumentierten Befehle schreiben fest in die Arbeitsordner der Bauer (`baer_export_fell.py:43` NETZ, `baer_textur_fell.py:27`
TX); ein woertlicher Nachbau haette deren Ergebnisse ueberschrieben. Darum liefen `baer_export_fell.py` und `baer_textur_fell.py` als
Kopie, in der **nur** diese Ausgabepfade (und der Verweis der Textur-Kopie auf die Export-Kopie) umgebogen sind (`diff` im Skript);
`baer_kampf_fell.py`, `baer_gewichte_fell.py`, `baer_tier_anim.py`, `lowpoly_npz.py`, `karten.py` liefen unveraendert. Eingang der
Textur: die vorhandenen GPU-Ansichten `textur/ansichten*` (nur gelesen).

| Stufe | Ergebnis gegen den Bauer |
|---|---|
| netz | `netz_fell.npz` und `sohle_layout.json` byte-gleich |
| fbx | MD5 anders (`440a1621` statt `d90796cd`): Zeitstempel und eingebetteter .blend-Pfad; Geometrie gleich (alles daraus Gebaute byte-gleich) |
| kopfprobe | gleiche Ausgabe (Krallen 456/456, Kopf 1.033/1.182, 149 am Nahtrand <= 4,5 cm gegen den Stand **vor** baer-anim) |
| Formel-Gewichte | `gew_fell2_formel.npz` byte-gleich |
| Gewichte (10 min CPU) | `gewichte_fell.npz` byte-gleich |
| GLB | **`c8250ace` byte-gleich**; Body 1024 aus der gelieferten 2048 `79a9aca4` byte-gleich |
| backen Zwischenstand, lowpoly_npz, karten | `zwischen_fell` PNG, `lp_fell.npz`, `karten_2048.npz` byte-/inhaltsgleich |
| Textur backen | **`NCBear_fell_2048.png` `9395c7fe` byte-gleich**, Kopf-Variante `7c466a70` byte-gleich |
| Body 1024 aus der nachgebauten 2048 | `79a9aca4` byte-gleich, GLB wieder `c8250ace` |
| NCBearDeer.glb (`baer_tier_anim.py`) | **`c5cc07bb` byte-gleich** |

## 7. NCBearDeer.glb

- Wofuer: Rueckfall-Art "bearstag" (`NCBearDefs.lua` `AnimalDefinitions.animals["bearstag"]`, Modell `NCBearStag_Body` in
  `nc_bear_tier.txt`): dasselbe Netz auf den Knochen des Rehs, bewegt mit den Reh-Clips (`animationsMesh = Deer_Stag`). Beide Arten
  nutzen dieselbe `textures/Body/NCBear.png` (Rasse "brown", `texture = "NCBear"`).
- Laedt: Importer liest 40 Knochen, 0 Clips, 18.456 Dreiecke (Lowpoly ohne Maul, wie alt 17.626 = altes FBX), <= 4 Einfluesse, Summe 1.
  Knochennamen/Eltern/Offset/Bind gleich dem alten Deer, Knoten-TRS und inverseBind byte-gleich.
- Passt zum neuen Netz: jede Ecke liegt auf einer Ecke von `lp_fell` (Lage <= 0,0002 mm, UV <= 6e-8). Das **alte** Deer passt nicht
  zur neuen Textur (nur 1.790 von 10.506 UV-Punkten = Kopf/Krallen) -> die fuenf Dateien muessen **zusammen** in die Test-Mod.
- Gewichte: Formel aus `baer_tier_anim.py` (nicht die optimierten) - fuer den Rueckfall ohne eigene Clips in Ordnung.

## 8. Befunde

### Blocker
Keine.

### Major
**M1 Falten Achsel+Ellbogen im Liegen verfehlt (Kevins Punkt 6).** `falten_out.txt` (falten_fell.py an meinem Dump): DeerStag_Dead
sigma2 < 0,5: Achsel 97 + Ellbogen 57 = **154**, Ziel <= 120 (forschung_bestand.md 6); alt 240. Im Sitzen Ellbogen 19 -> **33**
(schlechter), Achsel 161 -> 116. Messziel um 28 % verfehlt, die Bauer nennen es selbst offen. Fix: gezielt Gewichte an Ellbogen/Achsel
fuer die Liegepose nachoptimieren (Energie `druck` dort hoeher) oder eine Kantenschleife; dann Gewichte/GLB neu, Nachbau-Kette wie 6.

### Minor
**m1 "Ei" im Aufrichten knapp verfehlt.** `ei_out.txt`: Rear 1,30 s Verhaeltnis Schulter (1,3-1,5 m) zu Rumpf (0,4-0,8 m) ohne Arme:
alt 0,866 -> **0,923** (Armgewicht < 0,05, naeher am Mass der Forschung 0,88) bzw. 0,924 -> 0,941 (Mass des Bauers); Ziel 0,95.
Verbessert, nicht erreicht.

**m2 Kopf-Gewichte nicht bit-gleich.** `kopf_out.txt`: 172 von 1.333 Kopf-Punkten (halsseitig, Tier-x 0,59-0,80 m, bis 20 cm vom Rumpf)
haben leicht andere Gewichte (halbe L1 Median 0,0017, max 0,024). Ruheform bit-gleich; gehaeutet weichen Kopf und Krallen ueber alle
Clips/Bilder hoechstens **2,38 mm** ab (NCBear_Sit Bild 60, 99 % <= 1,0 mm). Praktisch "Kopf bleibt so"; nur zur Kenntnis.

**m3 Krallenfarbe aendert sich an 46 von 456 Krallenecken.** Die Krallen-UV sind Punkte (Dreiecke < 0,02 Texel). 46 Ecken (1024) bzw.
31 (2048) liegen mit ihrem 2x2-Lesefeld in einer **Rumpf-Insel** (z. B. Body-Texel x 46-47, y 1011-1013: Rumpf-Insel in alt und neu,
schon seit baer-anim so). Da der Rumpf heller wurde, lesen diese Krallen bis zu **32 sRGB-Stufen** heller (alt 61-86 -> neu 97-125).
Geometrie der Krallen bit-gleich; die Behauptung "251 Krallen-Texel bit-gleich" stimmt nur fuer deren Maske. Fix: die betroffenen
Krallen-UV auf einen freien Fleck legen (Export, dann GLB neu) oder im Spiel ansehen und hinnehmen.

**m4 "Staerkere Straehnen" (Kevins Punkt 2) in der Spiel-Textur kaum messbar.** `straehnen_out.txt`: Ruecken/Flanke Bandpass 1,2-3,1 cm
+8 %, 3,1-9,3 cm -6 %; relativ zur Helligkeit an der Unterseite sogar weniger (weil heller). Die Buesche kommen bei 1024 an, sind aber
nicht deutlich staerker als vorher. Urteil am Bild beim Optik-Pruefer; Stellschraube `BAER_TX_STRAEHNE`.

**m5 Nachbau nur mit umgebogenen Pfaden; Doku lueckenhaft.** `baer_export_fell.py:43` (NETZ fest) und `baer_textur_fell.py:27`/`:1009`
(TX fest, `NCBear_kopf_variante.png` wird bei jedem `backen` ueberschrieben): ein Nachbau nach `bau_netz.md` 6 / `bau_textur.md` 9
ueberschreibt die gelieferten Arbeitsdateien. In `bau_netz.md` 6 fehlen `lowpoly_npz.py` und `karten.py` (das Backen liest
`KARTEN = NETZ + "karten/karten_2048.npz"`, `baer_textur_fell.py:420`) und der Deer-Bau (`baer_tier_anim.py`, steht nur in
`netz/uebergabe.md` 3.5). Fix: Ausgabeordner per Umgebungsvariable, die drei Schritte in `bau_netz.md` 6 ergaenzen. Mit Kopien ist
alles byte-gleich (Abschnitt 6).

**m6 Mess-Maske "Maul" faengt Rumpfpunkte.** `netz/glb_pruef.py:38` (`innen = U 0,27..0,49, V < 0,10`) erfasst im neuen UV-Layout auch 26
Punkte innen am linken Vorderbein (UV-Pixel x 470-501, y 54-99, ausserhalb der Flecken). Diese 51 Dreiecke fehlen in Tiefpunkt/Dehnung
dieses Werkzeugs; nachgemessen max Dehnung 2,35 (SwipeL) - **kein Einfluss auf die Ergebnisse**. `werkzeug/regionen.py` (Maul ueber Abstand,
Zeile 121) ist nicht betroffen. Fix: Maske auf die drei Flecken-Rechtecke begrenzen.

**m7 FBX traegt Zeitstempel und lokalen Pfad.** `WorldItems/NCBear.fbx` enthaelt `C:\Users\Kevin\NPCCrew-Nebenprojekte\_arbeit\baer_fell\netz\lowpoly_fell.blend`
(alt sogar 6 Scratchpad-Pfade) - darum nicht byte-reproduzierbar und ein Nutzerpfad in einer Mod-Datei. Vorbestehend, harmlos fuer das Spiel.

**m8 Integrator-Hinweis: nur alle fuenf zusammen.** Neues UV: GLB, Deer-GLB, FBX, Body- und WorldItems-Textur gehoeren zusammen; ein
Teil-Kopieren (z. B. nur GLB oder nur Textur, oder das alte Deer behalten) gibt ein falsch texturiertes Tier (Abschnitt 7).

## 9. Nicht geprueft / offen
- **Nicht gespielt.** Ob Gewichte und Textur im Spiel so wirken, sieht nur Kevin. "2048 flimmert" nicht im Spiel gesehen.
- GPU-Stufen (Ansichten) nicht nachgebaut (Auftrag: ohne GPU); die Textur ist ab den vorhandenen Ansichten byte-gleich nachgebaut.
- Uneinigkeit/Struktur/"im Spiel hell" der Textur nicht selbst gemessen (Optik-/Textur-Blick). Normalen der Unterseite nicht gekippt
  (bekannt offen, kein Regelbruch).
- Kevins Pflichtpunkte 1/2 nur technisch geprueft (Sohlen-Inseln, Relief 8 mm, Ballen-Kontrast in der 1024 vorhanden; Unterseite heller);
  ob es schoen aussieht, ist Sache des Optik-Pruefers.

Statisch/offline geprueft, nicht gespielt.
