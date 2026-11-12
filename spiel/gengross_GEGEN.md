# GEGEN -- Lauf baer-gen-gross, Rolle GEGENPRUEFER (11.11.2026, ~22:10-23:00)

**Statisch geprueft, nicht gespielt.** An der Abgabe nichts geaendert. Geschrieben nur `R/gegen/` (Dumps, Skripte, Renders, Blaetter),
`R/bilder/KEVIN_gross_vergleich.png` und diese Datei (R = `_arbeit/baer_gen_gross`). Kein git, kein Download. GPU nur ueber `R/gpu.lock`
und erst, wenn kein fremdes Blender lief (`gegen/g_gpu.sh`; einmal auf das Blender eines anderen Laufs gewartet).
Abgabe vor und nach der Pruefung: `out/md5.txt` 6 x OK (NCBearGen.glb 87811753, NCBearGen.png bd6a335e, NCBearGenFoto.png da159718,
Bench cb184551 / 97b144d7 / db296ad8). Originale `rig/md5_vorher.txt` 28 x OK (NCBearTest NCBear.glb 08ec7806 unveraendert).

## 0. Urteil kurz
- **Keine feste Regel gebrochen** (alles selbst gemessen, Tabelle 2). Skelett, inverseBind und alle 15 Clips byte-gleich mit dem 2c; das
  Spiel (Dump.java) liest das GLB; Dehnung, Boden, Naehte, Netz, Gewichte, Texturen in den Grenzen. B1 ist wirklich behoben (Kopf/Maul max 2,58).
- **Testhilfe laedt sauber** (statisch): Pruefer gruen, Attrappe Lua 5.1 "ALL OK", NCBearFight greift die Arten nicht (Beleg 3).
- **Laeuft wie ein Baer: ja.** Gleiche Clips; Gehen/Rennen Bild fuer Bild deckungsgleich mit dem 2c (eigene Renders aus dem Spiel-Skinning).
- **Schoener als der 2c: nein, ehrlich nicht.** Gleich gut bei Stehen 3/4, Gehen und offenem Maul; schlechter beim **Aufrichten aus Kevins
  Kamera** (schwarze Unterarme + schwarzes Wellenband quer ueber die Brust, auch in Spielgroesse deutlich, G-01), beim Fressen von oben
  (spitze Schnauze, O-01 bestaetigt), beim Sitzen (wirkt wie ein Teddy mit runden Ohren) und in Spielgroesse (liest sich als grauer Baer).
- **bereit_fuer_test_mod: ja** -- als Vergleichs-Modell. Bedingung fuer den Integrator: NUR den Patch `fix1/M2_uebernahme.patch` einspielen,
  NICHT die Vollkopie `fix1/m2/baer_uebernahme.py` (veraltet, wuerde die F1-Aenderungen zurueckdrehen, G-06).

## 1. Weg (unabhaengig vom Bauer und den Pruefern)
- Importer-Harness `Dump.java` selbst auf `out/.../NCBearGen.glb` und NCBearTest `NCBear.glb` laufen lassen (`gegen/dump_gen.txt`, `dump_2c.txt`).
- Eigener Leser + eigenes Linear Blend Skinning (`gegen/g_dump.py`); Konvention an der Idle-Pose bestimmt (Kanten-Verhaeltnis median 1,00,
  p99 1,07; die andere Konvention 1,25). Eigener GLB-Vergleich (`g_glb.py`).
- **Renders ohne Blenders glTF-Animation:** Punkte UND Normalen je Pose aus dem Dump genau wie im Spiel gerechnet (`g_posen.py`), in Blender
  als Netz mit eigenen Normalen gebaut, Cycles OPTIX (`g_render.py`). UV-Lage an Gesicht/Pfoten des 2c bestaetigt. 2c und neu je Pose mit
  derselben Kamera. 190 + 90 Bilder (`gegen/r_a`, `gegen/r_b`), alle Blaetter unter `gegen/blaetter/` selbst angesehen.

## 2. Feste Regeln (selbst gemessen, Spalte "Bauer" = NACHBESSERUNG.md)
| Regel | Grenze | gemessen (Gegenpruefer) | Bauer | ok |
|---|---|---|---|---|
| Dreiecke | <= 20.000 | 19.958 (ELEMENTS 59.874 / 3), Punkte 12.746, Indizes u16 | 19.958 | ja |
| Netz / Material | 1 / 1 | 1 Mesh, 1 Primitive, kein Material/Bild (wie 2c) | gleich | ja |
| Knochen | 26, Name/Eltern/Ruhe/inverseBind = 2c | Dump BONES+OFFSET+BIND+15 CLIP-Bloecke textgleich (MD5 beider Kopfteile 2cd5bebc, 46.433 Zeilen); GLB: Knoten gleich bis auf Netz-Namen, Skin-JSON gleich, inverseBind-Bytes gleich, 733/733 Nicht-Netz-Accessoren byte-gleich | gleich | ja |
| Clips | 15 byte-gleich | 15 Namen gleich, 2.340 Sampler-Accessoren 0 anders | gleich | ja |
| Einfluesse | <= 4, Summe 1 | max 4 (5.460/3.363/2.695/1.228 Punkte mit 1/2/3/4), Summe 1 +-4,5e-8, kein NaN/negativ; 19 benutzte Knochen = 2c | gleich | ja |
| Texturen | 1024 x 1024 RGB je Farbe | beide 1024 x 1024, 8 Bit RGB, kein Alpha | gleich | ja |
| Massstab | 0,544 / Groesse 1,0 | Ruhe 1,92 x 0,78 x 1,14 m (2c 1,96 x 0,79 x 1,15) | gleich | ja |
| Dehnung p99,5 je Clip | <= 2,6 | max 1,91 (Rear) | 1,91 | ja |
| Dehnung max | <= 4,0 | max 3,18 (SwipeL Bild 13, Brust x 0,29); Kopf/Maul max 2,58 (Rear), Bite 2,20, Maul 2,18, Slam 1,87; kein Dreieck > 3,5 | 3,18 / 2,58 | ja |
| Achsel/Brust | <= 3,5 | eigene Zone max 3,18 (SwipeL), sonst <= 2,95 | 3,18 | ja |
| Boden alle Clips | >= -1,5 cm | tiefster Punkt -1,36 (Run Bild 11), Walk -1,26, Death -1,15, Sit -0,97, Dead -0,44, Stehen 0,00 | gleich | ja |
| Risse Hals/Achsel/Leiste | keine | Koerperhaut nach Lage verschweisst 0 offene Kanten; 2.505 Naht-Paare in allen 874 Bildern 0,0000 cm | 0,000 | ja |
| Kopf-Aussenform | bleibt | in out/ unveraendert (Probe "Schnauze breiter" nur in fix1/proben) | | ja |
| Testhilfe-Namen | NCBearBench* | 3 Dateien NCBearBench*, Art-Namen ncbeargen/ncbeargenfoto | | ja |

Weitere eigene Zahlen: Lippen-Zwillinge 59 Gruppen; bei Kiefer 0 Grad 0,00 cm (Idle/Walk/Run/Dead/SitDown/StandUp), Mundwinkel oeffnen
hoechstens 4,1 cm (2c 12,0). Sitzflaeche +0,29 cm (2c +0,15), Liegen Rumpf 10,47 cm (2c 10,70). Rueckenlinie Ruhe x +0,2 / 0 / -0,3 / -0,5:
1,141 / 1,093 / 1,080 / 1,044 (2c 1,145 / 1,087 / 1,054 / 1,034) -> Buckel ist der hoechste Punkt (O-03 bestaetigt). Schnauzen-Halbbreite
x 1,10 / 1,05 / 1,00: 0,049 / 0,057 / 0,064 m (2c 0,075 / 0,078 / 0,095) -> O-01 bestaetigt. Symmetrie 0,392 / 0,392.

## 3. Testhilfe (statisch)
- `luacheck.py` 2/2 ok, `scopecheck.py` 0, `localcount.py` hoechstens 10 aktiv / 37 insgesamt, `luacheck_pz.py` nur W113 `NCBearFight`
  (Test-Mod-Globale, mit nil-Riegel gelesen, `NCBearBenchGen.lua:298`). ASCII, LF, keine BOM.
- Attrappe `bench/attrappe/test.lua` selbst laufen lassen (Lua 5.1, echte NCBearDefs.lua der Test-Mod): **ALL OK**.
- NCBearFight erkennt "seine" Baeren nur an `getAnimalType() == "bear"` (`shared/NCBearFight.lua:1787`, selbst gelesen); `F.NearestBear`
  (:1914), `F.Calm.Sit/Stand/Eat/Play` (:1925/:1947/:1964/:1985) gibt es. Der Baeren-Kern fragt nur `B.BodyKind` (`BanditsNPCBear.lua:36`,
  :497-501). -> ncbeargen/ncbeargenfoto sind nie Kampfbaer.
- Arten = flache Kopie von `bear` mit eigenem bodyModel/Stufe/genes/Rasse (gleiches Muster wie die gespielte `NCBearBenchVergleichDefs.lua`);
  eigenes animationsMesh mit denselben 15 Clip-Namen = gespieltes Muster `NCBearBenchCubAlt`. Nur Einzelspieler (`isSP()` in jedem Befehl).

## 4. Je Pose: schoener als der 2c? (ehrlich; Bilder `gegen/blaetter/` und `bilder/KEVIN_gross_vergleich.png`)
| Pose | Urteil | Beleg |
|---|---|---|
| Stehen, Kevins Kamera | **gleich** (Geschmack): lebendige Augen, natuerliches Fell; aber Schnauze schmal, Ohren als runde Scheiben | `z_kevin.png`, `z_kopf_kevin.png` |
| Stehen, Seite | **leicht schlechter**: Buckel jetzt da, Rumpf gut; Kopf kleiner mit hohen runden Ohren und langer schmaler Schnauze -> wirkt juenger/wie ein Schwarzbaer, 2c maechtiger | `z_seite_a.png`, `z_seite_b.png` |
| Gehen / Rennen | **gleich** (Bewegung identisch, Pfoten stehen) | `z_gehen.png` |
| Sitzen | **schlechter bis gleich**: Kopf frei, aber Teddy/Koala-Eindruck (runde Ohren oben), Kehlfalte im Ton; 2c liest sich mehr als Baer | `z_sitzen.png`, `z_sitz_zoom.png` |
| Aufrichten, Kevins Kamera | **schlechter**: schwarze Unterarme + schwarzes Wellenband quer ueber die obere Brust (G-01) | `z_rear_brust.png`, `z_aufrichten.png` |
| Maul offen nah (Rear/Bite) | **gleich gut**: Zaehne, Zunge, Mundwinkel sauber (B1 behoben) | `n1_maul.png` |
| Fressen aus Kevins Kamera | **schlechter**: von oben spitze Schnauze + Ohrscheiben (O-01) | `z_kopf_kevin.png`, `n6_kopf.png` |
| Spielgroesse 101 px/m | **schlechter**: 2c klar Braunbaer; neu grauer Baer, Aufrichten-Band deutlich, heller Punkt an der Brust sichtbar | `z_spiel101_x2.png` |

## 5. Maengel (keiner bricht eine feste Regel)
### G-01 major (Optik) -- Aufrichten: schwarze "Stola" (O-02 nur teilweise behoben)
- Aus Kevins Kamera (az 0, el 30) Rear 48: Unterarme schwarz, dazwischen ein schwarzes Wellenband quer ueber die obere Brust; in Spielgroesse
  deutlich. Der Ton zeigt dort nur Falten -> es ist die Textur. Der eigene Beleg des Bauers `fix1/bilder/fix1_2_vorderseite.png` zeigt es auch.
- Textur-Helligkeit je Region relativ zum Ruecken (`g_farbe.py`): neu Unterarm 0,46 / Achsel innen 0,69 / Oberarm 0,75 / Brust 0,83;
  2c 0,61 / 0,86 / 0,93 / 0,97. Brust/Bauch sind heller als vorher (Brust 0,55 -> 0,83), Arme und Achsel bleiben viel dunkler als beim 2c.
- Vorschlag: Achsel-Innenseite und Unterarm-Innenseite (die Flaechen, die beim Aufrichten zur Kamera zeigen) auf ~0,75 aufhellen,
  Unterarm aussen dunkel lassen (Foto: dunkle Beine); danach Rear 48 aus Kevins Kamera neu ansehen. Oder Kevin entscheidet (Frage 3).
### G-02 minor -- heller Dreiecks-Fleck an Kehle/Brust
- Dreieck 10670 (Ruhe x 0,51, y -0,09, z 0,54; eigene UV-Insel bei Pixel 753-757 / 509-515): vorher dunkler Fleck (L 81 neben 141), nach fix1
  heller Fleck (176 neben 141), beide Texturen. Im Sitzen/Aufrichten nah klar sichtbar, in Spielgroesse ein heller Pixel. Beleg `z_sitz_zoom.png`,
  `z_fleck_tex.png`. Vorschlag: Insel auf den Ton der Nachbar-Texel setzen. Groesster Nahtsprung der Textur (95).
### G-03 minor -- Lippenschnitt bei geschlossenem Maul (O-07 Rest)
- Seite/3-4 nah: schwarze, gezackte Striche von der Nase bis unter das Auge (Ton und Textur). Kein Loch: Zwillinge 0,00 cm, Haut 0 offen ->
  Furche. In Spielgroesse eine dunkle Maullinie. Beleg `n6_kopf.png`, `n5_rest.png` (Sitzen Seite).
### G-04 minor -- Krallenwurzeln offen und teils ausserhalb der Haut
- 80 offene Kanten an den Krallen (4 je Kralle; die 2c-Krallen sind geschlossen). Windungszahl: in Ruhe liegen 39 von 80 Wurzelpunkten
  AUSSERHALB der Haut, 0,9-7,8 mm (Median 2,7 mm). Im Nahbild (Ton) keine Luecke zu sehen; im Spiel mit Rueckseiten-Abschnitt evtl. eine
  1-Pixel-Luecke an der Krallenbasis (ungeprueft). Vorderkrallen duenn und kurz, eine fast waagrecht (bekannt, Frage 4). Beleg `n3_pfoten.png`.
### G-05 minor -- Farbspruenge an UV-Naehten
- Mittel wie 2c (7,9), aber 21 Kanten mit Sprung > 60 (2c 8): Brust unten, linke Flanke unten (x -0,26, y 0,20, z 0,45), Bauch hinten.
  Nahbild Flanke: waagrechte Linie, dazu eine kleine dunkle Kerbe vor dem Hinterbein. Spielgroesse unsichtbar. Beleg `n2_flanke.png`, `g_naht_tex.json`.
### G-06 major (Einbau) -- veraltete Vollkopie des Uebernahme-Skripts
- `fix1/m2/baer_uebernahme.py` (dac52af6) ist auf altem Stand: die heutige `baer/tools/baer_uebernahme.py` (31974bf9) hat seither die
  F1-Aenderungen (Baeren-Fenster, Taste V, PlaceCub ...). Wer die Kopie einspielt, dreht F1 zurueck. **Nur den Patch einspielen:**
  `patch --dry-run` an einer Kopie: "Hunk #1 succeeded at 184 (offset 13 lines)". Dazu `baer/NAEHTE.md` (heute "genau 26 Fehlern",
  Zeile 84) auf 29 + die drei Pfade. Den Trockenlauf danach selbst laufen lassen (liest NPC Crew; hier nicht gelaufen).
### G-07 minor -- veraltete Pruefsumme im Kommentar
- `out/42/media/scripts/NCBearBenchGen.txt` Kommentar nennt "Netz NCBearGen.glb b36d947b" (heute 87811753). Nur Text.
### G-08 minor -- Durchdringung Sitzen (= m1, bestaetigt)
- Eigene Probe (Bein-Punkte 2 mm nach aussen, Windungszahl): Sit 60 / SitDown 48 / StandUp 0 je 35 (2c 6), Walk 7 22 (2c 6), Rear 48 93
  (2c 111). Flach (Ellbogen am Bauch), aus Kevins Kamera verdeckt. PLAN C6 formal verletzt, keine feste Regel der Aufgabe.
### G-09 minor -- Kehlfalte beim Sitzen, Ohren
- Sitzen Seite (Ton): scharfe Falte unter dem Kinn, deutlicher als beim 2c; im Fell kaum. Ohren gross, rund, oben -> Teddy-Eindruck beim
  Sitzen und von hinten (O-10 Rest; Kopf-Aussenform, also Kevins Wahl). Beleg `z_sitz_zoom.png`, `n5_rest.png`.

## 6. Bestaetigt (selbst gesehen)
- B1: Mundwinkel ohne Zipfel und ohne Riss bei Rear 48 / Bite 13 (`n1_maul.png`). O-03: Buckel hoechster Punkt (Seite und Messung).
- O-04: echte Krallen sichtbar, Boden nie tiefer als -1,36 cm. O-11: Leerraum gefuellt (Naht-Spruenge im Mittel wie 2c).
- Gehen/Rennen/Hiebe/Liegen ohne Risse; Kopf gerade und symmetrisch.

## 7. Fragen fuer Kevin
1. Kopf: so lassen, Schnauze vorn breiter (braucht deine Ausnahme von "Kopf-Aussenform bleibt"), oder den 2c-Kopf?
2. Farbe: braun, Fototon oder die waermere Probe?
3. Beim Aufrichten sind Arme und ein Band ueber der Brust schwarz (Blatt, Zeile "Aufrichten"). Aufhellen wie beim 2c?
4. Vorderkrallen: kurz lassen oder laenger (dann beim Abrollen etwas im Boden)?
5. Stoert dich beim Sitzen der Teddy-Eindruck (grosse runde Ohren oben)? Kleinere Ohren brauchen ebenfalls deine Ausnahme.

## 8. Kevins Test (nach dem Einbau durch den Integrator)
1. Spiel NEU starten (mit -debug), einen Wegwerf-Spielstand laden, ruhige offene Wiese.
2. Konsole: `NCBear_GenLive()` -> links 2c, Mitte braun, rechts Fototon, alle schauen zu dir.
3. ~5 s warten, dann `NCBear_GenAct("sit", 30)`, danach `"rear"`, `"eat"`, `"bite"`, `"swipeL"`, `"slam"` -- alle drei machen mit.
4. `NCBear_GenRun()` zweimal (hin und zurueck) = Rennen von der Seite; zwischendurch gehen sie von selbst.
5. Achten auf: Aufrichten (schwarzes Band?), Fressen (Kopf von oben), heller Punkt an der Kehle, Farbe im Spiel-Licht.
6. Zum Schluss `NCBear_GenClean()`, den 2c per Rechtsklick "Remove living bears nearby" entfernen, speichern.

## 9. Dateien
- Blatt fuer Kevin: `R/bilder/KEVIN_gross_vergleich.png` (MD5 f83708d5; 2c | neu braun | neu Fototon; Stehen Spielkamera, Seite, Gehen,
  Sitzen, Aufrichten, Spielgroesse 101 px/m 2x; ohne fremde Fotos).
- Blaetter: `R/gegen/blaetter/` (z_* Vergleiche, n1..n6 Nahaufnahmen, g1..g10 alle Ansichten 2c | braun | Fototon | Ton | 2c Ton).
- Messungen: `R/gegen/g_mess.json` (+ `.log`), `g_topo.json`, `g_zwilling.json`, `g_form.json`, `g_naht_tex.json`; Dumps `dump_gen.txt`, `dump_2c.txt`.
- Skripte: `R/gegen/g_dump.py`, `g_glb.py`, `g_mess.py`, `g_topo.py`, `g_zwilling.py`, `g_form.py`, `g_kralle.py`, `g_durch.py`, `g_farbe.py`,
  `g_naht_tex.py`, `g_flecken.py`, `g_pick.py`, `g_posen.py`, `g_render.py`, `g_auftrag.py`, `g_auftrag2.py`, `g_blatt.py`, `g_zeig.py`,
  `g_kevin_blatt.py`, `g_gpu.sh`; Patch-Probe `R/gegen/m2probe/`.
- Nach dem Kopieren muss Kevin das Spiel neu starten (Lua und Modelle laden nur beim Start).
