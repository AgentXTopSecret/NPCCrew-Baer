# Baer, Lauf baer-anim: Fixer

Stand 08.11.2026, PZ 42.21, Bandits 42.21, Blender 5.2.3. Grundlage: `anim_review_optik.md` (13 Funde) und
`anim_review_technik.md` (9 Funde). Gebaut unter `_arbeit/baer_anim/mod/42` (nach `NCBearTest` kopiert erst der Abschluss),
nichts unter NPC Crew `42`/`common`, keine fremde Mod angefasst, nichts heruntergeladen. Renders nur auf der RTX 4090 (OptiX und
OptiX-Entrauscher), vor jedem Render `tasklist` geprueft: das Spiel lief nie. **Statisch geprueft und offline gemessen, nicht
gespielt.**

## Kurz

- **Alle ernsten Funde behoben oder mit Beleg eingegrenzt.** Hieb: Pranke nie mehr im eigenen Kiefer (0 statt 212 Punkte,
  kleinster Abstand 14,7 cm statt 0,3 cm). Doppelschlag: Pranken vor der Brust unter dem Kopf statt neben den Ohren (Arm im Kopf
  0 statt 43). Sitzen: Hinterbeine wirklich vorn, keine Beine mehr ineinander (2-3 statt 406-420 Punkte), Sohle rollt nicht mehr
  (Sitzen 1 Grad statt 61, Hinsetzen/Aufstehen Sprung je Bild <= 20 statt 47). Hinterbeine laden und schieben in Hieb,
  Doppelschlag und Biss (Knie bis 143/150/147 statt nie ueber 134).
- **Knockback (Technik 1/2):** seitlich getroffene Zombies werden nicht mehr gedreht und nicht mehr als Flug gezaehlt; sie fallen
  auf der Stelle ("side"). Geflogen wird nur bei FRONT, und geprueft werden jetzt beide Bahnen.
- **Offen bleibt (mit Beleg):** die Hautdehnung an Achsel/Brustunterseite beim Hieb und Doppelschlag (deutlich weniger, aber ueber
  3-fach) braucht das Netz (Lauf baer-fell); das Sitzen erreicht Kevins Vorlage nur mit gespreizten Hinterbeinen, weil das runde
  Netz sehr dicke Glieder hat -> **Kevins Wahl (a) oder (b)**, Bild `anim_sitzen_vergleich.png`.

## Dateien

| Datei | Was |
|---|---|
| `NPCCrew-Nebenprojekte/baer/spiel/baer_kampf_anim.py` | Bauweg (Original `baer_kampf.py` bleibt). Neu: Spuren Hieb, Doppelschlag, Biss, Bodenbiss, Sitzpose S, Hinsetzen, Aufstehen; feste Pruefung "Sohle rollt"; Vorschau-Pose (b) nur mit `NCB_VORSCHAU_SITZ_B` |
| `_arbeit/baer_anim/mod/42/media/models_X/Skinned/NCBear.glb` | **neu**, MD5 `4cfe4f29a21b3e5063a0dec46b8dfb5e`, 1.155.424 Byte, zweimal gebaut byte-gleich (`anim/bauf16`, `anim/baufin`) |
| `_arbeit/baer_anim/mod/42/media/textures/Body/NCBear.png` | unveraendert (MD5 `a800c084...`, der Bau schreibt dieselbe Datei) |
| `_arbeit/baer_anim/mod/42/media/lua/shared/NCBearFight.lua` | Knockback ohne Drehen, zweite Bahn, "von hinten" aus zwei Massen, lautes Schnauben 18 s, Hinsetzen spielt zu Ende, Weiten, Marke TESTSCHNITTSTELLE |
| `_arbeit/baer_anim/mod/42/media/lua/client/NCBearBench.lua` | `NCBear_KnockInfo` zeigt "bear at his side" statt "turned" |
| `_arbeit/baer_anim/attrappe/test_anim.lua`, `mutate.py` | Koerperwinkel getrennt von forwardDirection; 300 Pruefungen 0 Fehler, 23 von 23 Mutationen fallen auf |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_kampf_vorschau.mp4` | neu gerendert (Hieb L/R, Biss stehend, Biss liegend, Doppelschlag, Aufrichten; links Spielwinkel, rechts Seite) |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_sitzen_vorschau.mp4` | neu gerendert (Hinsetzen, Sitzen, Aufstehen, Fressen) |
| `NPCCrew-Nebenprojekte/baer/spiel/anim_sitzen_vergleich.png` | oben gebaut (a), unten Vorschau (b), je schraeg/vorn/Seite neben `kevin_sitzvorlage.png` (nur angesehen) |
| `_arbeit/baer_anim/fix/` | Werkzeuge: `schnell.py` (Posen ohne Netz in 1 s), `ueber.py`, `m/mess.py` (Windungszahl, Rollen, Knie, Dehnung, alte Clips), `m/radius.py`, Sicherungen `*.reviewed.*` |

## Optik (anim_review_optik.md)

1. **ernst, behoben -- Hieb: Pranke durch den Kiefer.** Treffpunkt jetzt vor der linken Schulter und tiefer (0,898 Kacheln vor,
   0,162 zur Schlagseite, 0,385 m hoch; vorher 0,945 / 0,03 innen / 0,52 m), der Kopf dreht im Schlag weiter weg (Welt -27 statt
   -16) und hebt sich, der Unterarm zieht danach UNTER dem Kinn durch. Gemessen (Windungszahl, `m/mess.py hieb`, Bild 10-27):
   Pfote im Kopf 0 (vorher bis 209, der Pruefer zaehlte 212), Kopf im Arm 0 (bis 277), kleinster Abstand 14,7 cm (0,3). SwipeR ist weiter das Spiegelbild.
2. **ernst, (b)/(c) behoben, (a) Kevins Wahl -- Sitzen.** Hinterbeine vorn (Ferse 0,49 vor der Hueftlinie, Fersengelenk 0,16 hoch,
   Knie 141), Sohle nach vorn (leicht nach aussen), Vorderpfoten +-0,18. Durchdringung (alle Glieder gegeneinander): 1-3 Punkte
   statt 406/420 (Hinterpfote im Vorderbein), Pfote in Pfote 0 statt 88-101. **Warum gespreizt:** das runde Netz hat sehr dicke
   Glieder -- um Unterarm und Unterschenkel liegt die Haut im Mittel 0,16-0,17 m vom Knochen (90 %: 0,20-0,21; `m/radius.py`).
   Zwei Glieder nebeneinander brauchen damit rund 0,36 m Achsabstand; zwischen den Vorderbeinen bleiben keine 0,36 m frei, also
   muessen die Hinterbeine aussen vorbei (Fersen +-0,57). Der Rumpf bleibt bei 56 Grad: aufrecht und Pfoten flach am Boden
   schliessen sich mit diesem Skelett aus (Animator 7, vom Pruefer nachgerechnet). **Neu dafuer: Vorschau (b)** -- Rumpf 10 Grad
   aus der Senkrechten, Pranken haengen vor dem Bauch (die Knie erreichen sie nicht, Oberarm zurueck ist auf -70 begrenzt),
   Hinterbeine schmaler (+-0,44), keine Durchdringung, tiefster Punkt +0,4 mm. Nur als Bild, nicht in der Mod. Preis von (a):
   die Haut in der Leiste ist gedehnt (max 4,54, 21 Kanten ueber 3; vorher 3,84) -- vorn zwischen den Beinen sichtbar.
3. **ernst, behoben -- Sohle klappt um.** Ursache gefunden und belegt: die alte Vorgabe `rel_H (-100, -6, 10)` lag im toten Winkel
   der Messgroessen. Steht der Fuss quer zum Unterschenkel, ist eine Drehung um die Fusslaengsachse fuer dors/seitab/sup fast
   unsichtbar; der Loeser rollte die Sohle 61,4 Grad, um 1,6 Grad seitab zu erfuellen (nachgerechnet: dieselbe Rechnung mit
   `(-100, -1,627, -5,974)` rollt 0,3 Grad). Jetzt steht der Hinterfuss im Sitzen IN WELT (Gieren 34 mit dem Bein, Nicken -95),
   im Schritt bis 40 % flach, dann dreht er. Gemessen (`m/mess.py roll`): Sitzen -1,2/+1,2 Grad (vorher 61,4); Hinsetzen
   -13,2..+13,2, Sprung je Bild hoechstens 16,1 (vorher 47,4); Aufstehen -12,7..+15,9, Sprung 18,8 (vorher 35,0). **Neue feste Pruefung im Bau** (`SOHLE_GRENZE`,
   `SOHLE_SPRUNG` = 20/20, eigene Messung aus Beinebene und Sohlennormale): jeder Clip, der sie reisst, steht im Bericht unter
   "ausserhalb Grenze" -- sie hat in diesem Lauf drei Fehlversuche gefangen.
4. **ernst, behoben -- Doppelschlag: Pranken neben dem Gesicht.** Hochphase mit Pranken vor der Brust UNTER dem Kopf (Ellbogen
   104-112, Pfoten rund 0,33 m unter der Nase), Kopf hoeher (Hals -28, Kopf -22). Gemessen: Arm im Kopf 0 (vorher 43), kleinster
   Abstand 6,3 cm; 8-9 Kopfpunkte zaehlt die Probe weiter "im Arm" (wie vorher am Anfang und Ende des Clips, Grundrauschen der
   Messung). Hinweis: "Oberarm vor +35..+40" (Vorschlag) hob die Pranken bei aufgerichteter Brust noch hoeher (gemessen, verworfen).
5. **ernst, behoben -- der Koerper arbeitet nicht.** Hieb: Hinterbeine laden beim Ausholen und schieben im Schlag (Knie HL 124-136,
   HR 111-143; vorher 117-134), Becken gieren -9..+7 bei Brust -19..+16 (rund 40 %). Doppelschlag: laden auf rund 120, im
   Niederschlag 150. Biss: 122 -> 147. Ruhewinkel 133,7.
6. **ernst, verbessert, Rest offen (Netz) -- Hautdehnung Achsel/Brustunterseite.** Kanten ueber 3-fach je Bild (alle Kanten, wie
   der Pruefer): Hieb 92 statt 116, Doppelschlag 80 statt 207, Biss 22 statt 88; ueber 4-fach im Clip: Hieb 27 statt 41,
   Doppelschlag 14 statt 49. Hoechstwert Hieb 5,61 (5,93), Doppelschlag 5,38 (5,44). Ort weiter Rippen hinter der Achsel und die
   Innenseite des Unterarms an der Brustmitte (Ruhelage 0,06 m neben der Mittellinie: so dick ist der Unterarm). Unter 3-fach
   kommt das nur mit dem Netz (Achselfalte, duennere Vorderbeine oder Korrekturknochen) -- Lauf baer-fell. Den "Zipfel am
   Ellbogen" sehe ich in den neuen Treffer-Bildern nicht mehr (`fix/bilder/blatt_f4_hieb.png`), bewiesen ist das nicht.
7. **klein, behoben -- Bodenbiss Bild 20.** Haltende Pranke 5 cm weiter aussen, Schuetteln zur linken Seite 17 statt 30 Grad.
   Pfote im Kopf 0 (vorher 73); 7-11 Kopfpunkte zaehlt die Probe in den Bildern 10-14 (Pranke tritt vor), 0-3 sonst.
8. **klein, behoben -- Biss: Arme hochgerissen.** Die Vorderpfoten bleiben per IK an einem flachen Bogen: hoechstens 15,6 cm
   (vorher 53), groesster Schritt 4,1 cm je Bild (vorher 35).
9. **klein, nicht geaendert -- Stuetzpfote dreht beim Hieb.** Der staerkere Rumpf dreht sie mit (Grenze des Handgelenks greift in
   12 Bildern). Im Spielwinkel nicht zu sehen; ein Festnageln liesse das Handgelenk knicken.
10. **klein, behoben -- Hinterpfoten schweben im Sitzen.** Tiefster Punkt der Hinterpfoten 1,8 / 2,6 mm (vorher 6-9 mm), ganzer
    Baer 0,0 mm; Hinsetzen und Aufstehen 0,0 mm (Bau-Bericht; ein Zwischenstand mit fruehem Aufdrehen der Zehen lag 58 mm tief).
11. **klein, nicht meins -- alte Clips mit neuem Netz.** Bewegung weiter bit-gleich (Idle, Walk, Run, Death, Dead: alle Kanaele
    Abweichung 0, eigener Leser; Probe.java: Netz, Knochen und alte Clips gleich). Die staerkere Dehnung an der Pranke im Gang
    kommt vom Netz des Modellbauers, nicht von den Clips -- Kevin beim naechsten Test auf die Pranke im Gang schauen lassen.
12. **klein, Geschmack -- Ausholen sieht von vorn wie Winken aus.** Das Ausholen ist unveraendert; Kevin entscheidet im Spiel.
13. **klein, berichtigt:** `anim_clips.md` 1 nennt "tiefster Hautpunkt 2,1 mm drunter" -- das sind 0,0021 Modelleinheiten, also
    rund 3,9 mm. Neue Clips jetzt: Kampf wie vorher, Sitzen/Hinsetzen/Aufstehen 0,0 mm.

## Technik (anim_review_technik.md)

1. **ernst, behoben -- seitlich: kein Flug, aber "back" gezaehlt.** Kein `faceLocationF` mehr. `testDotSide` liest den
   KOERPERwinkel (Jar `getLookAngleRadians` 0-53), `faceLocationF` setzt nur `forwardDirection` (Jar 51-58), deshalb blieb die
   Lage LEFT/RIGHT. Jetzt: LEFT/RIGHT -> auf der Stelle, `why = "side"`, Zaehler `side`; geflogen wird nur bei FRONT, und
   `setPlayerAttackPosition` bekommt genau den Wert von `testDotSide` (Fundstelle Bandits ZAPush.lua:42, gleicher Typ).
   `back` zaehlt nur noch echte Fluege (oder das Schieben). Attrappe: Koerperwinkel `look` getrennt von `fwd`, `faceLocationF`
   aendert nur `fwd`, Flug nach -Koerper; neue Pruefungen "side: falls on the spot", "mid-turn", "look behind".
   **Folge fuer Kevin:** nur Zombies, die den Baeren ansehen, fliegen; alle anderen fallen wie bisher auf der Stelle (vorher
   genauso, nur verdreht und falsch gezaehlt). Der sofortige Winkelsetzer `setTargetAndCurrentDirection` hat null Lua-Fundstellen
   und bleibt tabu.
2. **ernst, behoben -- falsche Bahn geprueft.** Zusaetzlich zur Geraden Baer -> Zombie wird die Bahn nach seinem eigenen Hinten
   (`-getForwardDirection()`, Bandits ZAPush.lua:36) mit derselben Vorpruefung (`F.ClearBehind`) gelesen; faellt eine durch,
   faellt er auf der Stelle. Kein neuer Engine-Aufruf. Wasser und Ebenenkante: weiter durch `flyOk` je neuer Kachel.
3. **klein, behoben -- Weiten.** Aus den neuen Clips: Hieb 0,90 + 0,55 = 1,4 (bleibt), Biss 0,97 + 0,45 = 1,4 (vorher 1,3),
   Bodenbiss 0,68 + 0,42 = 1,1 (vorher 1,2), Doppelschlag 0,58 + 0,9 = 1,5 (bleibt). Kommentar neu. Attrappe nachgezogen.
4. **klein, behoben -- zwei Masse fuer "von hinten".** `fromBehind = behind or side == "BEHIND"` fuer `setHitFromBehind`,
   `knockDown` und das Veto.
5. **klein, behoben -- lautes Schnauben alle 6 s.** Jetzt hoechstens alle 18 s (`HUFF_LOUD_GAP`); Attrappe prueft den Abstand.
6. **klein, behoben -- Sprung aus halbem Hinsetzen.** Ein Ziel waehrend des Hinsetzens laesst den Clip zu Ende laufen (hoechstens
   1,6 s), danach direkt Aufstehen; `NCBear_Stand()` mitten im Hinsetzen ebenso (setzt die Sitzdauer auf 0). Kampf geht weiter
   vor, nur 1,6 s spaeter.
7. **klein, Frage an Kevin -- offene Tuer.** Gebaut ist "geschlossene Tuer sperrt den Flug, offene nicht". Kevins Wortlaut war
   "nie durch Wand, Tuer, Zaun". Die strenge Fassung waere `a:isDoorTo(b)` als Veto (belegt ISZoneDisplay.lua:403,
   ISObjectClickHandler.lua:135). Nicht geaendert, bis Kevin sagt, welche.
8. **klein, erledigt -- Kopierliste.** Der Abschluss kopiert alles, was `diff -rq mod/42 NCBearTest/42` meldet (unten), in einem
   Zug. GLB und Body-Textur gehoeren zusammen.
9. **klein, behoben -- Testschnittstelle in der Spieldatei.** Jede Stelle traegt die Marke `TESTSCHNITTSTELLE` (8 Stellen), dazu
   ein Absatz im Kopf von `NCBearFight.lua`: das Uebernahme-Skript nimmt sie heraus und legt `log` auf den Crew-Logging-Schalter.

## Pruefungen

- Lua: luacheck 0, scopecheck 0, localcount hoechstens 70 aktiv / 106 insgesamt, luacheck_pz nur W113 auf den eigenen Global
  `NCBearFight` (wie vorher). LF, ASCII, ohne BOM. Attrappe 300 Pruefungen, 0 Fehler; Mutationen 23/23 (neu: Seite fliegt doch,
  eigenes Hinten nicht geprueft, Blick hinten ignoriert, Schnauben 6 s, Sprung aus halbem Hinsetzen, Aufstehbefehl mitten im
  Hinsetzen, alte Weiten 1,2/1,3).
- GLB: Probe.java liest 15 Clips mit den Dauern aus `F.ACTS`; Netz, Knochen und die fuenf alten Clips gleich der gepruefen Fassung.
  Treffermomente und Tonmomente unveraendert (Hieb 0,60, Doppelschlag 1,30 mit Aufsetzen 1,27, Biss 0,52, Bodenbiss 0,544).
- Bau-Bericht: kein Clip ausserhalb einer Grenze (auch nicht der neuen Sohlengrenze), Boden: Kampfclips wie vorher, Sitzen 0,0 mm.

## Kevin entscheidet

1. **Sitzen (a) oder (b)** -- `anim_sitzen_vergleich.png`. (a) ist gebaut und im GLB; (b) ist nur ein Bild. Waehlt er (b), braucht
   es neue Hinsetz-/Aufsteh-Clips (eine Runde). Variante (c): duennere Glieder im Lauf baer-fell, dann ginge (a) schmaler.
2. **Offene Tuer** (Technik 7).
3. **Dehnung Achsel** -- im Spiel ansehen; die Abhilfe gehoert in den Lauf baer-fell.

## Abschluss: diese 17 Dateien kopieren (diff -rq, in einem Zug)

`AnimSets/buck/idle/NCBear_Bite.xml`, `_Eat.xml`, `_Sit.xml`, `_SitDown.xml`, `_StandUp.xml` (neu), `_Slam.xml`, `_SwipeL.xml`,
`_SwipeR.xml`; `lua/client/NCBearBench.lua` (neu); `lua/shared/NCBearDefs.lua`, `NCBearFight.lua`; `models_X/Skinned/NCBear.glb`,
`NCBearDeer.glb`; `models_X/WorldItems/NCBear.fbx`; `scripts/nc_bear_sounds.txt`; `textures/Body/NCBear.png`,
`textures/WorldItems/NCBear.png` (alle unter `42/media/`).

## Unsicher, offen

1. **Nicht gespielt.** Ob seitlich getroffene Zombies im Spiel wirklich auf der Stelle fallen und frontal getroffene 1,7 Kacheln
   fliegen, zeigt die Sondenzeile `knock: ... moved` nach Kevins Test.
2. Hautdehnung (Optik 6) und Leistendehnung im Sitzen (Optik 2) -- Netz.
3. Kurze Beruehrungen bleiben: Hinsetzen Bild 33-38 (die Vorderpfoten ruecken ein und streifen die Wade, hoechstens rund 30
   Punkte, gezaehlt jeder dritte Punkt x 3), Aufstehen Bild 0-5 (rund 25, Pfote an Wade). Vorher: 83 und 58 Punkte in der Bewegung
   und 406-420 dauerhaft im Sitzen.
4. Die Messung "Kopf im Arm" beim Doppelschlag (8-9 Punkte) habe ich als Grundrauschen gelesen, weil sie vorher in den
   unbeteiligten Bildern ebenso stand; nachgewiesen ist das nicht.

Statisch geprueft und offline gemessen, nicht gespielt.

## Integrator (08.11., nach anim_review_gegen.md)

- **Gegen 1 (ernst) behoben:** `NCBear_HuffSoft` ohne `volume = 0.6` (nur noch `distanceMax 20`), `NCBear_Huff.wav` mit Python `wave`
  aus der vorhandenen Datei um +6,8 dB angehoben (Spitze -1,0 dBFS, RMS -18,1 dB, nichts abgeschnitten; Original in
  `_arbeit/baer_anim/integ/`). Gilt fuer beide Huff-Toene. Im Spiel ungeprueft.
- **Gegen 2 (ernst) offen, nicht gebaut:** **Aufrichten (NCBear_Rear) ist unveraendert** gegenueber dem Kampf-Stand, auch der harte
  "Kragen" ueber den Oberarmen (Dehnung 100 Kanten ueber 3-fach, staerkster Clip). Rear neu zu bauen haette GLB, Videos und Pruefung
  neu verlangt; gehoert in die naechste Runde (Oberarme weniger an die Brust, dann Netz im Lauf baer-fell).
- **Gegen 6 berichtigt:** die Marke TESTSCHNITTSTELLE steht NICHT an jeder Stelle; ohne Marke sind die Leser von `F.forceNext`, der
  Zweig "play" in updateCalm, `F.knockLog` und die Befehle `NCBear_Fight/_Tune/_FightInfo` (Umzug in Bench-Dateien: Arbeit fuer B1).
- **Gegen 8 und 10:** Kommentare berichtigt (Biss: Kiefer rund 0,9 m, Bauchhoehe; ISInventoryTransferAction :590/:593).
- **Gegen 3, 4, 5, 7, 9 nicht geaendert, in Kevins Anleitung bzw. hier vorgemerkt:** Sitzen (a) ist nicht das Bild; nur frontal
  Getroffene fliegen; `slamReach` 1,2 ausprobieren (`NCBear_Tune("slamReach", 1.2)`); Debug-Spawn hat Leben 1,0
  (`NCBear_ZHealth(2, 10)`); Sprung beim Treffer im Sitzen und beim Fressbeginn.
- Pruefer nach den Aenderungen: luacheck 0, scopecheck 0, localcount unveraendert, luacheck_pz nur W113 `NCBearFight`, Attrappe
  300/0. Videos gehoeren zum Stand: Kampfvideo aus `dumpf9` (alle Kampfclips, Netz, Bind gleich `dumpfin`), Sitzvideo und
  Vergleichsbild (a) aus `dumpf16` = `dumpfin`, `dumpfin` aus dem GLB `4cfe4f29`; Body-Textur seit 14:24 unveraendert.
- Kopiert nach `NCBearTest/42`: 34 Dateien, 6 neu, 13 ueberschrieben, `diff -rq` gleich; Sicherungen
  `backups/NCBearTest/NCBearTest_vor_anim_2026-11-08_175001.zip` und `..._mit_anim_2026-11-08_175026.zip`; beide `mod.info` neu
  beschrieben. Das Spiel lief beim Kopieren nicht.

Statisch geprueft und offline gemessen, nicht gespielt.
