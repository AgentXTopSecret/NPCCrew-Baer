# Baer, Lauf baer-anim: Gegenpruefung nach dem Fixer

Stand 08.11.2026, PZ 42.21, Bandits 42.21. Geprueft: `anim_fix.md` und der ganze Stand `_arbeit/baer_anim/mod/42`
(GLB MD5 `4cfe4f29...`) gegen `NCBearTest/42` (GLB `2e9a6d17...`), dazu `ENTSCHEIDUNGEN.md`, `anim_review_optik.md`,
`anim_review_technik.md`, `anim_spez.md`. **Nur gelesen, gerechnet und Probe-Laeufe, nichts am Stand geaendert, nichts gerendert,
nichts gespielt.** Eigene Werkzeuge, unabhaengig von denen des Fixers: `_arbeit/baer_anim/gegen/` (`glbr.py` GLB-Leser,
`fk.py` Vorwaertskinematik und Haeutung in numpy, `t1`-`t16` Messungen). Masse in Modellmetern (GLB-Einheit / 0,544, also
Meter bei Baerengroesse 1,0). Das Spiel lief bei keinem Probe-Lauf.

## Kurz

**0 toedlich, 2 ernst, 8 klein.** Die Technik steht: Ziele unveraendert, Knockback-Logik richtig gegen das Jar, Clipnamen und
Treffermomente passen, alte Clips und Kopf bit-gleich, kein Gelenk knickt gegen seine Richtung. Die zwei ernsten Funde betreffen
das, was Kevin sieht und hoert: das Schnauben im Alltag ist vermutlich kaum hoerbar, und das Aufrichten (Kevins Kritikpunkt) ist
unveraendert und im Fixer-Bericht nicht als offen genannt.

## Funde

### ernst

1. **Schnauben im Alltag kaum hoerbar (`nc_bear_sounds.txt` `NCBear_HuffSoft`, `NCBearDefs.lua` huffsoft).**
   Kevin: Schnauben *"ja soll er"*. `ENTSCHEIDUNGEN.md` (Nachtrag 02:40) nennt schon das heutige Schnauben *"sehr leise; Huff-Schnitt
   ist der wackeligste"*. Gebaut ist eine noch leisere Fassung derselben Datei.
   Beleg, gemessen an den WAV-Dateien: `NCBear_Huff.wav` ist 0,21 s lang, Spitze -7,8 dBFS, RMS -24,8 dB. Growl1-3 und Roar
   liegen bei RMS -14 bis -14,7 dB, die Huff-Datei ist also rund 10 dB leiser. Dazu kommen beim Alltags-Schnauben `volume = 0.6`
   (rund -4,4 dB) und `distanceMax = 20` statt 30. Im Spiel ist das ungeprueft.
   **Reparatur:** `NCBear_HuffSoft` mit `volume = 1.0` (oder die Zeile streichen); leiser macht ihn dann nur `distanceMax 20`.
   Dazu `media/sound/NCBear_Huff.wav` um rund +7 dB normalisieren (Spitze auf -1 dBFS), mit Python `wave` aus der vorhandenen Datei
   und ohne Download. Davon haben beide Huff-Toene etwas. Kevin beim Test ausdruecklich `NCBear_Huff()` hoeren lassen.

2. **Aufrichten (NCBear_Rear) unveraendert, und der Rest aus Optik-Fund 6 fehlt im Fixer-Bericht.**
   Kevin hat das Aufrichten ausdruecklich *"nicht so huebsch"* genannt. Der Rear-Clip ist seit der Optik-Pruefung bit-gleich
   (eigener Vergleich `NCBear.reviewed.glb` gegen das Ergebnis: Rear identisch, Eat identisch, alle anderen neuen Clips geaendert).
   Optik-Fund 6 (ernst) nannte beim Aufrichten den harten "Kragen" ueber den Oberarmen (`pruef/s3_rear.png`, `s5_rear.png`).
   `anim_fix.md` Optik 6 fuehrt aber nur Hieb, Doppelschlag und Biss auf, und unter "Offen" steht Rear auch nicht.
   Eigene Messung (`gegen/t13.py`, Kanten ueber 3-fach je Bild): **Rear 100 (bei 1,17 s), Hieb 92, Doppelschlag 80, Biss 22,
   Sitzen 21, Gang 9.** Rear ist damit der staerkste Clip, an Wade und Hinterbein, Becken und Pranke.
   **Reparatur:** Rear in `anim_fix.md` unter "Offen" und in Kevins Nachricht aufnehmen (Netz, Lauf baer-fell), nicht verschweigen.
   Wenn noch eine Runde laeuft: die Oberarme beim Aufrichten weniger an die Brust ziehen, wie beim Doppelschlag-Fix, und dann die
   Dehnung neu zaehlen.

### klein

3. **Sitzen (a) ist nicht Kevins Vorlage. Das ist richtig als Wahl vorgelegt, aber Kevin sollte es so hoeren.** Eigene Messung
   (`t8.py`): Rumpf 56 Grad aus der Senkrechten (Vorlage etwa 15-20), Schulter 0,72 m hoch, Pranke 0,10 m, Hinterfuesse
   +-0,57 m seitlich und 0,15 m vor Bip01, Zehen 0,39 m hoch (Sohle steht vorn, wie im Bild). Hinterbein und Vorderbein beruehren sich
   (kleinster Abstand 0,4-1,1 cm). Die Begruendung des Fixers haelt (Arm reicht 0,72 m, aufrecht braeuchte die Schulter rund 0,95 m).
   Im Spielwinkel wirkt (a) wie ein geduckter Klumpen (`anim_sitzen_vergleich.png` oben, `fix/bilder/video_sitz_auszug.png`).
   (b) trifft den Umriss besser. Ein noch nicht versuchter Hebel waere das Schluesselbein: die Schulter im Sitzen absenken, das
   Schulterblatt rutscht am Rumpf hinunter. Damit kaemen vielleicht 40-45 Grad heraus (ungeprueft, Haut an der Schulter pruefen).
   Nur, wenn Kevin (a) waehlt und es ihm zu geduckt ist.

4. **Knockback fliegt nur bei FRONT.** Das ist richtig gegen das Jar gebaut (`IsoGameCharacter.testDotSide` 0-8 gibt
   `Side.name()` zurueck, `testDotSideEnum` 78-91: FRONT ab Skalarprodukt > 0,7), aber Kevin muss es wissen: seitlich und von hinten
   Getroffene fallen auf der Stelle. Fuer "von hinten" gibt es in der XML einen eigenen Flug: `actiongroups/zombie/idle/
   to_staggerback-knockeddown-fromBehind.xml` verlangt `playerAttackPosition == BACK`, der Knoten spielt
   `Zombie_PushedFwdOver_FromBehind` (`AnimSets/zombie/staggerback-knockeddown-fromBehind/fromBehindAndFall.xml`). Der Aufruf
   `setPlayerAttackPosition(String)` ist belegt (Bandits `ZAPush.lua:42`). Den Wert "BACK" setzt aber keine Lua-Zeile, und wie weit
   der Clip fliegt, ist ungemessen. Deshalb nur nach Messung und mit Kevins Wort, nicht jetzt.

5. **Doppelschlag schlaegt Nebenziele in die Luft.** Die Pranken landen im Treffer (1,30 s) 0,55 m vor Bip01 (Gelenk, `t11.py`;
   der Fixer misst 0,58 Kacheln Pfotenmitte). Getroffen wird bis 1,5 Kacheln im Kegel +-80 Grad. Der Zuschlag ist 0,9, beim Hieb
   0,55. Ein Nebenziel 1,3-1,5 Kacheln vor ihm faellt also, waehrend die Pranken eine knappe Kachel davor auf den Boden schlagen.
   **Vorschlag:** `slamReach` 1,2 und im Spiel ansehen (`NCBear_Tune("slamReach", 1.2)`).

6. **Die Marke TESTSCHNITTSTELLE steht nicht "an jeder Stelle".** Ohne Marke sind: die Leser von `F.forceNext` (`NCBearFight.lua`
   startFight :469-471, ChooseAct :532-537), der Zweig "play" in updateCalm (:1103, :1122, :1144-1152), `F.knockLog` (:166,
   :625-627) und die drei Konsolenbefehle `NCBear_Fight`, `NCBear_Tune` und `NCBear_FightInfo` (:1475-1543, schon vorher da). Nach
   der FESTEN REGEL (ENTSCHEIDUNGEN, Copy-Paste) gehoeren `NCBear_*`-Befehle in Bench-Dateien, sonst bricht das Uebernahme-Skript
   ab. Das ist Arbeit fuer B1. Bis dahin den Satz "an jeder Stelle (8 Stellen)" berichtigen.

7. **Testanleitung: der Debug-Spawn hat 1,0 Leben.** Der Horde-Spawner hat Leben 1,0 als Vorgabe (`ISSpawnHordeUI.lua:110-111`),
   der Hieb macht 1,0 und `damage` toetet bei `h <= 0`. Jeder Hieb toetet also wieder (*"die meisten sind sofort tot"*), und Fluege
   sieht er dann nur bei Todesstoessen. Das steht in `anim_spez.md` 1 und `anim_lua.md`:36, muss aber in Kevins kurze Anleitung:
   vor dem Spawnen den Schieber auf 2,0 stellen, oder `NCBear_ZHealth(2, 10)`.

8. **Trefferhoehe und ein falscher Kommentar.** Der Hieb trifft auf Kniehoehe eines Zombies: Pranke 0,42 m bei Groesse 1, rund
   0,57 m bei 1,35. Das ist Geschmack. Der Kommentar "Schnauze in Halshoehe" (`NCBearFight.lua:841`) stimmt nicht: der Kiefer
   steht im Treffer 0,90 m hoch, das ist Bauchhoehe. Kommentar anpassen.

9. **Aus- und Einstiege ohne Clip.** Ein Treffer im Sitzen (`calmEnd` "hurt") laesst die Pose um 62,7 cm springen, nur ueber den
   Blend von idle (Sitzen gegen Stehen, `t15.py`). Fressen beginnt 29 cm neben idle, ueberblendet in 0,30 s. Beides ist sichtbar,
   aber kurz. Fuer die Befehle in B2b vormerken.

10. **Kommentar-Zeilen um eins verschoben:** `ISInventoryTransferAction.lua:589/:592` heisst im Spiel :590/:593. Die Fundstellen
    selbst stimmen (gelesen).

## Geprueft und in Ordnung (selbst gemessen)

- **Alte Clips:** Idle01, Walk, Run, Death, Dead: alle 78 Kanaele je Clip bit-gleich (MD5 von Zeit und Wert, `t1.py`). Knoten,
  Gelenkliste und Inverse-Bind-Matrizen gleich. Probe.java (Engine-Lader, `gegen/probe_final.txt`) liest 15 Clips mit den Dauern
  aus `F.ACTS`. Keiner der neuen Clips hat Wurzelweg (deferred 0,0). Run bleibt bei 1,058 E, Walk bei 0,378 E.
- **Kopf:** alle 1.293 Punkte mit Kopf- oder Kiefergewicht > 0,99 gleich in Lage und UV, 2.048 Kopfdreiecke gleich. Die Kopfflaeche
  der neuen Body-Textur ist pixelgleich (150.180 Pixel, 0 Abweichung, `t3.py`). Der Rest der Textur ist neu gepackt.
  `NCBearDeer.glb` nutzt die neuen UVs (100 % in der neuen Menge), passt also zur neuen Textur. Kopierliste: genau die 17 Dateien
  aus `diff -rq`.
- **Gelenke (`t5.py`, `t6.py`, `t12.py`):** der Ellbogen knickt in keinem Clip ueber gestreckt hinaus (innen 85-173 Grad, Gang
  89-172) und bleibt in der Scharnierebene. Das Knie knickt nie um. Das Handgelenk liegt im Rahmen von Gang und Lauf, beim Hieb
  dreht die Pranke bis 27,5 Grad ein. Die Ellbogenrichtung zur Brust weicht hoechstens 20 Grad von der Ruhe ab (Gang 14), es gibt
  also keinen verdrehten Oberarm. Die Sohle aus der Beinebene bleibt beim Hinsetzen und Aufstehen bei hoechstens 18 Grad.
- **Ganzer Koerper:** Hieb Hueft-Gieren -9..+7, Schulter -25..+22, Hinterknie 111-143. Doppelschlag Knie 119-150, Brust bis
  1,09 m. Biss Knie 122-147, Becken 10 cm vor. Die Hinterpfoten gleiten nicht (0 cm). Der Wurzelknochen bleibt stehen (wie bisher).
- **Durchdringung Arm/Kopf (Ersatzmass, kleinster Punktabstand, `t7.py`):** Hieb 15,6 cm (Fixer 14,7), Doppelschlag 6 cm, Biss
  25 cm, Aufrichten 13 cm, Bodenbiss 1,5 cm, Fressen 1,8 cm.
- **Treffermomente (`t11.py`):** Hieb 0,60 s = groesste Weite der Pranke (0,93 m vor), Doppelschlag 1,30 s = Pranken am Boden,
  Biss 0,52 s = Kiefer am weitesten vorn. Die XML (`m_TimePc`) passt zu `hitPc`. Toene: AttackStomp 1,27 s,
  SledgehammerSwing/Hit, MacheteHit, ZombieBite und HeadSmash gibt es in Vanilla (`scripts/generated/sounds/...`).
- **Naehte:** alle Kampfclips beginnen und enden in idle (0,1 cm). SitDown-Ende = Sit = StandUp-Anfang (0,0 cm). StandUp endet in
  idle (0,1 cm).
- **Ziele:** `F.IsTarget`, `pickTarget`, `canStrike`, `targetOk` und `hitList` sind byte-gleich zum heutigen Stand. Knockback,
  Schieben und `NCBear_ZHealth` laufen nur auf Zielen nach der Regel. Kein Scheinangriff, kein Rangeln.
- **Knockback gegen das Jar:** `testDotSide` gibt einen String zurueck, der Vergleich mit "FRONT"/"BEHIND" geht. Gedreht wird
  nicht mehr. Beide Bahnen (Baer -> Zombie und `-getForwardDirection`) gehen durch dieselbe Vorpruefung. Alle neuen Aufrufe sind
  belegt und haben gleiche Argumenttypen (`DebugContextMenu.lua:668` knockDown, `ISHutchGrabAnimal.lua:31`, `ISFarmingMenu.lua:463`,
  `ISWorldObjectContextMenu.lua:688`, Bandits `ZAPush.lua:36/41/42`).
- **Haengen:** jeder Unterzustand hat einen Ausgang (act und Hinsetzen/Aufstehen: Ende oder Frist +1 s; Sitzen und Fressen: Zeit;
  Anrennen: stuckTime und fightMax; Suchen: noTarget; Rueckweg: 20 s). Ein Ziel waehrend des Hinsetzens wartet bis zum Clipende.
  Ein Fehler schaltet einmal laut ab (pcall mit Meldung, keine Tarnkappe).
- **Kosten:** Listendurchlaeufe nur im 0,5-s-Takt oder je Angriff, alles Wachsende gedeckelt (8/8/8/32/50).
- **Testhilfen:** die acht neuen Befehle stehen nur in `client/NCBearBench.lua`, es gibt kein neues Menue, und die Spawn-Dateien
  sind unveraendert.
- **Pruefer:** luacheck 0, scopecheck 0, localcount hoechstens 106 insgesamt, luacheck_pz nur W113 auf den eigenen Global
  `NCBearFight`. Die Attrappe habe ich selbst laufen lassen: 300 Pruefungen, 0 Fehler. Alles LF und ASCII ohne BOM
  (`NCBearAttackProbe.lua` CRLF wie live).
- **Mehrspieler:** bleibt aus (`onTick` hinter `isSP()`), die Befehle sagen "singleplayer only".

## Urteil

Ausliefern geht, mit zwei Pflichtpunkten vor Kevins Test: das Schnauben hoerbar machen (Fund 1) und Kevin sagen, dass das
Aufrichten nicht neu ist und der Kragen bleibt (Fund 2). Dazu gehoeren in die Kurzanleitung: das Leben der Zombies auf 2,0
stellen (Fund 7), nur von vorn Getroffene fliegen (Fund 4), und Sitzen (a) ist nicht das Bild, (b) gibt es als Vorschau (Fund 3).

Statisch geprueft und offline gemessen, nicht gespielt.
