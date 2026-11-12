# Baer schlaeft -- Plan (Lauf baer-schlaf, 09.11.2026)

Grundlage: die sechs Forschungsberichte `_arbeit/baer_schlaf/forschung_engine.md`, `forschung_referenz.md`, `forschung_zz.md`,
`forschung_npcschlaf.md`, `forschung_bett.md`, `forschung_ton.md` (alle sechs ganz gelesen, keiner fehlt). Pfade ab
`C:/Users/Kevin/NPCCrew-Nebenprojekte`, Test-Mod ab `Zomboid/mods/NCBearTest/42/media`, Vanilla ab `ProjectZomboid/media`.
Kurzverweise: "engine 2.4" = forschung_engine.md Abschnitt 2.4 usw. "(selbst nachgesehen)" = beim Schreiben dieses Plans geoeffnet.
**Nur Forschung: nichts gebaut, nichts heruntergeladen, nichts gerendert, keine Mod-Datei geaendert. Statisch geprueft, nicht gespielt.**
Gilt unter `ENTSCHEIDUNGEN.md` (geht vor); Kevins Wunsch woertlich dort :113, seine Punkte :114-119.

---

## 0. Kurz fuer Kevin

- **Geht:** Der Baer legt sich nachts hin (auf den Bauch, Kinn auf den Pfoten), atmet ruhig und steht morgens wieder auf. Ueber ihm steigen kleine z Z z auf.
- **Kampf geht vor:** Kommt ein Zombie, schreckt er hoch und kaempft (Passiv: steht auf und kommt zu dir; Jungtier versteckt sich).
  Im Mehrspieler reist das Liege-Bild ohne eigenes Paket mit -- aber erst, wenn das Baeren-Gehirn auf dem Server laeuft. Heute laeuft
  es nur im Einzelspieler, im Mehrspieler schlaeft er also noch nicht (offen, ungespielt; 2.5).
- **Geht:** ein Baerenbett (flaches Strohlager, gut 3 x 2 m). Du baust es selbst und stellst es hin, und der ausgewachsene Baer passt genau darauf.
- **Geht nicht:** Einen freien Schlafton gibt es im Netz nicht. Die einzige echte Aufnahme darf in keine Mod. Darum erst einmal ohne Ton; nachruesten bleibt moeglich.
- **Spaeter wie die NPCs:** nachts schlafen, wenn er bleibt oder frei herumlaeuft, und neben dir liegen, wenn du schlaefst.
- **Wann gebaut wird:** erst wenn das neue Fell fertig ist. Die Bewegungen kommen in die naechste Bewegungs-Runde, Schlafen + z Z z + Bett danach in einem Lauf nach der Gegenwehr.
- Nichts davon ist gespielt.
- **Du entscheidest:** die Fragen K1-K21 in Abschnitt 7. Mit "Ja, alle so" gilt ueberall der Vorschlag.

---

## 1. Schlaf-Animation

### 1.1 Haltung: "Sphinx"

Bauchlage, Ellbogen unter der Schulter, Unterarme flach nach vorn, Hinterbeine untergeschlagen, Kinn zwischen den Pranken -- und in
der Schlafpose der Kopf etwa 20 Grad zur Seite gesunken (Wange auf der linken Pranke). So ist es knuffig (Teddy wie
`kevin_sitzvorlage.png`) und aus der schraegen Spielkamera gut lesbar: Ruecken, Kopf vorn, beide Pranken, Platz fuer z Z z.

| Haltung | echt? (referenz 1, Quellen 8) | Urteil |
|---|---|---|
| **Sphinx** | ja: Bauch mit Schnauze am Boden (Murie, https://npshistory.com/series/science/14/chap4.htm), Pranke als Kissen (https://polarbearsinternational.org/news-media/articles/polar-bear-sleep-patterns) | **Haupthaltung**. Mit unseren Gelenkgrenzen gemessen erreichbar: Vorderbein ohne Klemmung (Schulter vor 30,2, Ellbogen 106,9), Hinterbein Huefte vor 77,8 (Grenze 80, `baer_kampf_fell.py:564`), Knie 65,1, aber Hinterfuss geklemmt (4 Klemmungen "pfote"/"schwenk", `_arbeit/baer_schlaf/referenz/umriss2.json`); Rumpf 0 Klemmungen, auch mit Kopf 25 Grad zur Seite (referenz 2, 6) |
| Seitenlage | ja, echter Tiefschlaf (Mattiello 2014, https://faunalytics.org/effect-of-the-change-of-social-environment-on-the-behavior-of-a-captive-brown-bear-ursus-arctos/) | **nein**: unsere Tot-Pose `DeerStag_Dead` liegt schon auf der Flanke (referenz 0.3), schlafend saehe er tot aus |
| Halb eingerollt | ja (Winterlager) | hoechstens spaeter (K2): die Probe hatte 22 Klemmungen an den Beinen (referenz 6) |
| Froschlage | ja | nein: geht nur mit gelockerten Gelenkgrenzen, Fuesse 31 cm im Boden (referenz 2) |
| Rueckenlage | ja | nein: "Beine in der Luft" liest sich ebenfalls wie tot |

Offen fuer den Animator: In der Probe stecken Ellbogenunterseite 5,2 cm und Hinterfuss 3,9 cm im Boden (referenz 6). Aufwachen nach echtem
Vorbild: erst mehrmals den Kopf heben und schauen, dann aufstehen (Murie, referenz 1). Ohr-Knochen gibt es nicht, also kein Ohrzucken
(referenz 3).

### 1.2 Clips (Namen fest, Dauer Vorschlag)

| Rolle | Clipname im GLB | Dauer | Bilder | Schleife | Anfang -> Ende | Inhalt (referenz 3) |
|---|---|---|---|---|---|---|
| Hinlegen | **`DeerStag_IdleToSitting`** | 2,4 s | 72 | nein | Grund -> L | Kopf senkt sich, Hinterteil sinkt (Hinterbeine zuerst, wie beim Hinsetzen), Vorderpfoten nacheinander vor, Ellbogen unter die Schulter, Brust auf, Kopf auf die Pranken, ein Seufzer |
| Schlafen | **`DeerStag_SittingIdle`** | 12,0 s | 360 | ja | L -> L | zwei Atemzuege (~10 je Minute): Becken +8..10 mm, Lende/Brust nicken -1..-1,5 Grad; Traumzucken ~7,5 s, Kiefer beim Ausatmen 2-3 Grad, Schwanz ~9,5 s; Pfoten fest |
| Aufwachen (ruhig) | **`DeerStag_SittingToStanding`** | 2,2 s | 66 | nein | L -> Grund | Kopf hebt sich, umschauen +-15 Grad, Vorderbeine strecken, Hinterteil hoch |
| Aufschrecken (K3) | eigener Knoten, Name in B5a (Vorschlag `Bear_WakeAlarm`, ohne `NC`-Vorsilbe, siehe 1.3 Punkt 3) | 1,1 s | 33 | nein | L -> Grund | Kopf ruckt hoch, dann Aufstehen im Schnellgang ("Kampf hat Vorrang") |
| nicht im ersten Bau (K4) | Wach liegen 6 s, Bett scharren 2 s | | | | | spaeter |

- **Pose L** = Sphinx mit Kopf ~20 Grad zur Seite, als neue Grundpose wie `POSE_S` (`spiel/baer_kampf_fell.py`, referenz 3/4). Ihre Hoehe
  steht als feste Zahl im Skript, nicht aus `liege_alt.json` (das gilt nur fuer Death/Dead; referenz 4 Punkt 5).
- Regeln wie alle Ruheclips: 30 Bilder/s, alle 26 Knochen mit Schluesseln, `Translation_Data` 0, Bip01 still (sonst wandert er beim Hinlegen;
  engine 2.4).
- **Warum Vanilla-Namen:** Der Ruheplatz der Engine spielt genau diese drei Namen. Selbst nachgesehen in `AnimSets/buck/idle/`:
  - `idle1.xml:6-9`: Uebergang nach `idleSit` mit `DeerStag_IdleToSitting`.
  - `idleSit.xml:4`: `DeerStag_SittingIdle`.
  - `idleSit.xml:6-10`: Bedingung `idleAction = sit`.
  - `idleSit.xml:11-26`: zurueck mit `DeerStag_SittingToStanding`.

  Die Engine sucht einen Clip nur im Modell des Tiers (`AnimationPlayer.play` Off. 97-111, engine 2.4). Die echten Rehe behalten also
  ihre eigenen Clips. Unser GLB hat heute schon `DeerStag_Idle01/_Walk/_Run/_Death/_Dead` unter Vanilla-Namen (engine 2.4).

### 1.3 Engine-Weg: Entscheidung Weg A (Ruheplatz der Engine, `idleAction = "sit"`)

**Widerspruch in den Berichten:**
- Referenz (3, 4 Punkt 4), z Z z (6) und NPC-Schlaf (4.1, 4.8) planen eigene Knoten mit unserer Variable `NCBearAct` (Weg B).
- Der Engine-Bericht (6.1) empfiehlt den Ruheplatz der Engine (Weg A).

**Selbst nachgesehen:**
- **Server -> Clients:** `NetworkPlayerAI.set` Off. 224-253 legt `getVariableString("idleAction")` ins Tierpaket (Flag 2).
  `NetworkPlayerAI.parse` Off. 709-737 setzt oder loescht `idleAction` an der Kopie des Clients
  (`_arbeit/baer_schlaf/engine/dump/zombie.characters.NetworkPlayerAI.txt:492-515, 1330-1350`).
- **`NCBearAct` reist nicht mit:** Das Tierpaket hat kein Feld dafuer (engine 5.2).
- **Die Engine loescht "sit" nicht:** `BaseAnimalBehavior.clearIdleAction` Off. 0-42 loescht nur Werte, die mit "idle" beginnen
  (`.../dump/zombie.characters.animals.behavior.BaseAnimalBehavior.txt:1717-1736`).
- **Abfrage:** `IsoAnimal.isAnimalSitting()` ist `"sit".equals(getVariableString("idleAction"))`
  (`.../dump/zombie.characters.animals.IsoAnimal.txt:6732-6739`).
- **Unser Baer:** `sitRandomly = false` (`lua/shared/NCBearDefs.lua:93`), die Engine setzt "sit" bei ihm also nie selbst.
- **Andere Lua-Stellen:** Vanilla setzt oder loescht `idleAction` nur in `ISPetAnimal.lua:43/48/55/62` (grep ueber `media/lua`).

**Darum Weg A:**
1. **Mehrspieler-Bild umsonst:** Der Server setzt den Wert, nach spaetestens ~1 s spielt jeder Client Hinlegen und Schlafen selbst.
   Auch wer spaeter dazukommt, bekommt den Wert mit dem naechsten Paket (engine 5.2/5.3).
2. **Keine neue AnimSet-XML** fuer das Schlafen.
3. **Namen bleiben fest:** Die Clipnamen sind Vanilla-Namen. Sie haengen nicht an der Umbenennung in B5a, und die Cheat-Pruefung des
   Uebernahme-Skripts trifft sie nicht. Deren Regel "befehl" `\bNC[A-Z][A-Za-z]*_[A-Za-z]\w*` (`turret/tools/turret_uebernahme.py:99`,
   prueft auch Strings) trifft dagegen schon heute `"NCBear_Sit"` in `F.ACTS` (`lua/shared/NCBearFight.lua:47-56`).
4. **z Z z und Schlafton ohne eigenes Paket:** Jeder Client fragt seine Kopie mit `isAnimalSitting()`.

**Preis:**
- Das Ende von Hinlegen und Aufstehen erkennt Lua nur ueber die Uhr; die Vanilla-Uebergaenge senden kein Ereignis (`idle1.xml`/`idleSit.xml`).
- Kein eigenes Ton-Ereignis im Schlafknoten: Die Vanilla-Datei `idleSit.xml` wird nicht ueberschrieben, sie gilt fuer alle Rehe.
  Der Ton laeuft deshalb ueber Client-Lua (3.4).
- "sit" schaltet in der Engine weitere Dinge ab: halber Hunger und Durst, kein Wandern, kein Trog von selbst (engine 1.4). Harmlos,
  weil unser Takt Hunger und Durst ohnehin selbst zaehlt (Unsterblich-Schalter, `PLAN.md:160-163`); trotzdem in B3 beachten.

**Ablauf** (neuer Unterzustand der Ruhe-Phase `calm` neben Sitzen und Fressen; heute `NCBearFight.lua:1492-1668` laut engine 3.1):
1. **Einschlafen:**
   - `NCBearAct` loeschen und die Bewegung sperren (`animal:getBehavior():setBlockMovement(true)`, `ISPetAnimal.lua:36`).
   - Mindestens 0,5 s in idle1 stehen lassen (Blend 0,40, `idle1.xml:5`).
   - Dann `animal:setVariable("idleAction", "sit")` (Form `ISPetAnimal.lua:43`). Ohne die Pause legt er sich ohne Hinlege-Clip hin
     (engine 4.2).
2. **Waehrend des Schlafs:** Sperre erneuern (refreshBlock wie heute), Gefahr weiter suchen, Alltags-Schnauben aus (`dailyHuff`,
   `NCBearFight.lua:1458-1488` laut ton 2.1).
3. **Ruhig aufwachen:** `animal:clearVariable("idleAction")` (`ISPetAnimal.lua:48`). Die Engine spielt das Aufstehen; nach 2,2 s plus
   Frist ist er frei.
4. **Aufschrecken (K3):**
   - Im selben Takt `idleAction` loeschen und `NCBearAct = "wakealarm"` setzen (eigener Knoten mit Prioritaet 10 wie `NCBear_Sit.xml`).
   - Der Clip beginnt in Pose L, das Ueberblenden aus der Schleife springt also nicht (Lesart, **ungeprueft**). Ende per `NCBearDone`,
     dann `startFight`.
   - Im MP sehen Mitspieler bis B8/B9 das ruhige Aufstehen (`NCBearAct` reist nicht); Kampf im MP ist bis B9 ohnehin aus.
   - Kein direkter Sprung Liegen -> Angriff (engine 4.2: Ruck).
5. **Treffer oder Laerm-Ausflug ("away"):** `idleAction` sofort loeschen. Sonst legt er sich nach der Engine-Flucht ohne Clip wieder hin
   (engine 4.1/4.3). Der Laerm-Code aus baer-laerm bleibt sonst unveraendert.
6. **Ruhe beenden:** Jede Stelle, die die Ruhe beendet, loescht `idleAction` nur, wenn der Wert noch "sit" ist (Muster NPC Crew
   `BanditsNPCLivestockAnimalOps.lua:1060`). Gefragt wird mit `animal:isAnimalSitting()` (Vanilla AM TIER belegt, s. Tabelle; im Jar
   genau `"sit".equals(getVariableString("idleAction"))`), nicht mit `getVariableString` (Gegenpruefung 9.2).
7. **Pflicht:** `sitRandomly = false` bleibt; als Kommentar in die Definition schreiben.

| Engine-Aufruf | Argumente | Fundstelle |
|---|---|---|
| `animal:setVariable("idleAction", "sit")` | String, String | `ISPetAnimal.lua:43` (selbst nachgesehen) |
| `animal:clearVariable("idleAction")` | String | `ISPetAnimal.lua:48/55/62` (selbst nachgesehen) |
| `animal:isAnimalSitting()` | - | `client/ISUI/Animal/ISAnimalContextMenu.lua:383` (selbst nachgesehen) |
| `animal:getVariableString("idleAction")` | String | Vanilla nur AM SPIELER (`ISWorldObjectContextMenu.lua:2624`); am Tier nur NPC Crew `BanditsNPCLivestockCoop.lua:917` und unsere Test-Mod `NCBearFight.lua:1349` (gespielt, mit `"NCBearHit"`). Fuer den Schlaf **nicht noetig**: `isAnimalSitting()` reicht (Gegenpruefung 9.2) |
| `animal:getBehavior():setBlockMovement(bool)` | bool | `ISPetAnimal.lua:36/49` |
| `getGameTime():getHour()` | - | `server/Traps/STrapGlobalObject.lua:535`, NPC Crew `shared/BanditsNPCRoutine.lua:244` (nicht `ISWeatherChannel.lua:89`: dort `_gametime:getHour()`) |
| `getGameTime():getWorldAgeHours()` (Schlafuhr 5.2) | - | `server/Farming/SFarmingSystem.lua:258` |
| nicht benutzen: `debugForceSit`, `VirtualAnimal:forceWakeUp` | | Debug bzw. anderes Objekt (engine 6.2) |

### 1.4 Bau-Lauf

**Wann:** in der Clip-Runde (STAND.md Punkt 3), nachdem baer-fell fertig ist. Dort fehlen noch Pruefer, Nachbesserung und Gegenpruefer
(`UEBERGABE.md:9-17`). Grund:
- Die Gewichte (`spiel/baer_gewichte_fell.py`) sind auf genau 15 Clips abgestimmt und muessen fuer jeden neuen Clip neu laufen (referenz 4).
- Ein Lauf fuer Aufrichten neu, Sitzen (b) und Schlafen heisst ein Gewichte-Lauf und ein GLB-Tausch.

| # | Agent | Aufgabe |
|---|---|---|
| 1 | Planer | Auftraege, Pose-L-Masse, Reihenfolge |
| 2 | Animator Kampf/Sitzen | Rear neu, Sitzen (b), Hinsetzen/Aufstehen nachziehen (in `baer_kampf_fell.py`) |
| 3 | Animator Schlaf | Pose L, Hinlegen, Schlafen, Aufwachen, Aufschrecken in einer **eigenen Datei** `spiel/baer_schlaf_clips.py`, die der Integrator mit einer Zeile einbindet (zwei Bauer nur mit getrennten Dateien) |
| 4 | Kritiker Kampf/Sitzen | Bild fuer Bild gegen die Referenz, Knicke, Durchdringung, Gleiten |
| 5 | Kritiker Schlaf | dasselbe fuer die Schlaf-Clips, Vorschau im Spielwinkel neben die Referenz |
| 6 | Messer | Gewichte neu fuer alle Clips, Dehnung, **Falten liegend** (heute 154 statt Ziel 120, referenz 4), Boden mit dem Importer des Spiels, `mess_umriss.py` -> Bettmass (4.1), Kopf-Oberkante und Kopf-Vorlage -> z Z z-Anker (2.2). **KOPF BLEIBT SO** (`ENTSCHEIDUNGEN.md:85`): der Gewichte-Lauf haelt Kopf- und Krallengewichte fest (`KOPF_FEST`, `spiel/baer_gewichte_fell.py:43-66`), Kopf-Ruheform/UV bit-gleich pruefen wie in baer-fell (`_arbeit/baer_fell/pruef_technik.md:51`); Kopf, Hals, Kiefer bewegen sich nur ueber Knochen |
| 7 | Lua/XML-Bauer | Dauern in `F.ACTS`, Aufschreck-Knoten, Bench-Befehle `NCBear_Sleep()`/`NCBear_Wake()` NUR in `NCBearBench.lua` (drehen zur Kamera wie AnimTest) |
| 8 | Gegenpruefer | unabhaengig, die alten 15 Clips bit-gleich (`glb_pruef.py`) |
| 9 | Integrator | Kopie in einem Zug, Sicherung vorher/nachher, Commit + Push |

- **Grenze:** 9 Agenten, unter der Grenze von 10.
- **Regeln aus baer-anim** (referenz 4): Gelenkgrenzen, Klemmungen im Bericht, Boden hoechstens ~2 mm, Fussgleiten unter 0,01 Kacheln,
  hoechstens zehn Runden.
- **Renders:** nur auf der 4090, auch bei laufendem Spiel (Kevin 09.11.: alte Regel geloescht), nie gleichzeitig mit einem anderen Render.
- **Baby-Modell:** Waehlt Kevin ein eigenes (`_arbeit/baer_fell/baby/`), braucht es dieselben drei Clips. Ob dafuer dasselbe Skelett und
  dieselben Clips reichen, ist **ungeprueft**.

---

## 2. z Z z ueber dem schlafenden Baeren

### 2.1 Aussehen (zz 4)
- **Drei Buchstaben "Z" gleichzeitig in der Luft:**
  - Jeder lebt 2,4 s, versetzt um 0,8 s, und steigt schraeg nach rechts auf (rund 58 px hoch, 12 px seitlich, leichtes Pendeln).
  - Groesse ueber das Leben eines Buchstaben: `0,55 + 0,45 * sin(pi * u)`, unten klein, in der Mitte gross, oben klein. So liest sich
    die Saeule wie "z Z z" (Rechenprobe `_arbeit/baer_schlaf/zz/zz_kurve_ausgabe.txt`).
  - Weich ein- und ausgeblendet.
- **Immer dieselbe Glyphe "Z":** Ein Wechsel z/Z mitten im Flug wuerde springen. "Z" gibt es in den Schriften aller sieben Sprachen,
  ein Textschluessel ist nicht noetig (zz Kurzbefund 8).
- **Farbe und Schatten wie die NPC-Crew-Namen:** fast weiss (0,96 0,96 0,90), schwarzer Schatten (`client/ISUI/BanditsNPCNameTags.lua:1022/1035/1058`).
  Kein Gruen (UIStyle :15-18). Nachtblau nur auf K6.
- **Schrift:** Hoehe nach `getFontHeight(UIFont.Medium)`, also mit Kevins Schriftgroessen-Option. Gezeichnet mit `drawTextZoomed`,
  verkleinert aus der naechstgroesseren Schrift (scharf, NameTags :209-210). Das Jungtier bekommt etwas kleinere Buchstaben (81 % bei 0,35).
- **Wann:** einblenden 0,5 s, nachdem die Schlaf-SCHLEIFE laeuft, also nicht schon beim Hinlegen. Beim Aufwachen (auch beim
  Aufschrecken) kommen keine neuen Buchstaben, alles blendet in 0,6 s aus.
- **In der Pause:** eigene Uhr, die nur ohne `isGamePaused()` laeuft (`client/Foraging/ISSearchManager.lua:1462`). Die Saeule steht still.

### 2.2 Wo (Anker, zz 3)
- **Hoehe:**
  - Formel: `dz = H_E * 1,5 * groesse / 2,44949` z-Ebenen (Jar `IsoAnimal.getAttachmentWorldPos` Off. 80-221, `Core.DoPushIsoStuff`
    Off. 370-422, zz 3.1).
  - Merkzahl: 1 m am Baeren bei Groesse 1,0 sind 64 px bei Zoom 1.
- **Waagerecht:** ueber dem KOPF, nicht ueber der Mitte. Formel: `x + vorn * KOPF_VOR_E * 1,5 * groesse`, beim Erwachsenen bis 0,9 Kacheln
  vor der Mitte. Die Richtung kommt aus `animal:getForwardDirection()` -- **nur Jar, braucht Kevins Wort (K21):** belegt ist der Aufruf
  nur am Zombie (Bandits `ZAPush.lua:37`) und am Spieler (Vanilla `ISBaseIcon.lua:216`, `FishingRod.lua:286`), an keinem Tier (grep
  Vanilla/Bandits/NPC Crew); IsoAnimal erbt ihn nur (`IsoAnimal extends IsoPlayer`, keine eigene Fassung im Dump). **Rueckfall ohne sein
  Wort:** Saeule ueber der Tiermitte (Vorlage 0) -- beim Erwachsenen steht sie dann rund 0,8 Kacheln hinter dem Kopf, ueber dem Buckel.
  Die Richtung wird im 500-ms-Sammler geholt, nicht je Bild.
- **Vorgabe bis zur Messung (berichtigt, 9.2):** Kopf-Oberkante **0,26 E**, Vorlage 0,45 E. Die Probe-Sphinx ist schon gemessen: der Kopf
  liegt 0,45-0,50 m hoch zwischen 0,70 und 0,85 m vor Bip01 bei 1,0 (referenz 6; nachgemessen in `referenz/umriss2_sphinx_haut.npy`,
  hoechster Hautpunkt je 5-cm-Streifen: 0,497 m bei x 0,70, 0,453 m bei x 0,80, 0,426 m bei x 0,85). Die fruehere Schaetzung 0,40 E
  (0,74 m) lag ueber dem Nacken und haette die Saeule beim Erwachsenen rund 20 px zu hoch gesetzt (64 statt ~41 px bei Zoom 1).
  Der Messer der Clip-Runde liefert die echten Zahlen aus Pose L (1.4, Agent 6); mit der Wange auf der Pranke liegt der Kopf eher noch tiefer.
- **Regler** gleich mitbauen (Lehre NPC Crew `CLAUDE.md:2448-2455`): Funktionen `BanditsNPC.Bear.Overlay.SetZzLift(px)` und
  `SetZzHead(hoch, vor)`. Die Konsolenbefehle dazu NUR in `NCBearBench.lua`.

### 2.3 Zeichen-Modul (gemeinsam mit Name und Balken)
- **Datei:** `42/media/lua/client/ISUI/BanditsNPCBearOverlay.lua`.
  - Klasse `BanditsNPCBearOverlay = ISPanel:derive(...)`, Modul `BanditsNPC.Bear.Overlay`.
  - Gleicher Pfad in Test-Mod und NPC Crew, Namen frei (eigene Probe 09.11.: 0 Treffer fuer `BanditsNPCBear`, `BanditsNPC.Bear`,
    `UI_BN_Bear_`, `BearOverlay`, `BearBed` in NPC Crew 42/common, Vanilla scripts/lua, Bandits 42.21/common, NCBearTest).
  - Das ersetzt den Vorschlag `BanditsNPCBearSleepFx.lua` (npcschlaf S13): eine Zeichenschicht fuer alles.
- **Bauform wie die NPC-Crew-Namensschilder** (gespielt):
  - 1x1-Panel in der Ecke, `backMost()`, nie vergroessert, nie unsichtbar, Maus-Funktionen geben `false`.
  - Angelegt in `OnGameStart`, geleert in `OnMainMenuEnter`.
  - Gezeichnet wird im `prerender`.
- **Sammler alle 500 ms** (Form NameTags :1165-1168):
  - Baeren, die da sind, auf gleicher Ebene, bis 45 Kacheln, im Blick (`square:isCanSee(0)`, `ISBaseIcon.lua:256`).
  - Deckel 8 Baeren, Zustandstabelle hoechstens 32 Eintraege.
  - Die Baeren kommen aus der Liste des Baeren-Kerns. Fehlt sie (MP-Client), hoechstens alle 5 s `getCell():getObjectListForLua()`
    mit `instanceof(o, "IsoAnimal")` und `getAnimalType()` (`DebugContextMenu.lua:616-620`, `ISAnimalUI.lua:65`).
- **Zeilen als Liste, von unten nach oben:** `bars` (spaeter Leben/Hunger/Durst/Laune), `name` (spaeter), darueber `zz` (jetzt). Neue
  Balken sind eine Zeile mehr, kein Umbau (zz 7).
- **Werte ueber eine Frage:** `BanditsNPC.Bear.OverlayInfo(animal)`. Den Schlaf liest das Overlay selbst aus `isAnimalSitting()` (2.5).
- **Einstellung JE SPIELER** (`ENTSCHEIDUNGEN.md:106`): `BanditsNPC.ClientCfg.Table("BearOverlay")` (Feld `zz`, spaeter `name`, `hp`, ...),
  Vorgabe an mit `== nil`, Speichern mit `Save()` (`client/BanditsNPCClientCfg.lua:139/145`), hinter einem Existenz-Riegel. Ohne NPC Crew
  gilt der Wert nur im Speicher. Geschaltet wird spaeter im Baeren-Fenster; Texte `UI_BN_Bear_Show*` kommen erst mit dem Menue.
- **Gehoert nie hinein:** Konsolenbefehle, Zwangsschlaf, Regler-Befehle. Die liegen in `NCBearBench.lua`.
- **Cheat-Pruefung beachten:** Die Regeln des Uebernahme-Skripts pruefen auch Strings und Bezeichner (`turret/tools/turret_uebernahme.py:99-104`):
  kein `NC<Name>_...`, kein "debug", "bench", "cheat", "test..." im Code. Darum auch den Diagnose-Schalter nicht "debug" nennen
  (z. B. `F.T.log` wie heute).

### 2.4 Kosten (zz 5)
- **Je sichtbarem schlafendem Baeren und Bild:** 3 Positionsabfragen, 2 Umrechnungen (`isoToScreenX/Y(0, ...)`), 6 Textaufrufe.
  Teure Fragen nur im 500-ms-Sammler.
- **Abgeschaltet:**
  - geteilter Bildschirm (`getNumActivePlayers() > 1`, `FishingHandler.lua:6`)
  - ausgeblendete UI
  - dedizierter Server: laedt `client/` nicht

### 2.5 Einzelspieler und Mehrspieler (Berichtigung gegen zz 6)
- **Wann z Z z erscheint:** genau dann, wenn auf DIESEM Rechner `animal:isAnimalSitting()` gilt und der Baer unsere Art ist. Der
  Bericht zz 6 nahm `NCBearAct` an und hielt deshalb "MP erst mit B8" fuer noetig. Mit Weg A (1.3) reist der Wert mit dem Tierpaket.
- **Einzelspieler:** Das Gehirn setzt den Wert, das Overlay liest ihn.
- **Mehrspieler:** Setzt das Gehirn auf dem Server den Wert, sieht jeder Client nach ~1 s Hinlegen, Schlaf und z Z z, ohne eigenes Paket.
- **MP offen:** Das Baeren-Gehirn laeuft heute nur im Einzelspieler (`NCBearFight.lua:4-5`, `:227-229`). Bis es unter `not isClient()`
  laeuft (`PLAN.md:236-240`), gibt es im MP keinen Schlaf.
- **Einschlaf-Moment auf dem Client:** Der Client kennt ihn nicht. Er startet seine Uhr, sobald er "sit" zum ersten Mal sieht, und
  wartet die Hinlege-Dauer ab (2,4 s + 0,5 s). Wer spaeter dazukommt, sieht die Saeule dann ~3 s verspaetet (harmlos).

---

## 3. Schlafton

### 3.1 Ergebnis
**Nichts wird ohne Kevins Ja je Datei heruntergeladen** (Name, Quelle, Groesse, Lizenz; Massstab `sound/roh/QUELLEN.txt`: gemeinfrei).

- **Gesucht:** Eine freie (gemeinfreie oder CC0) Aufnahme eines schlafenden, schnarchenden oder ruhig atmenden Baeren gibt es nach der
  Suche nicht. Durchsucht wurden:
  - soundbible, freesound (auch mit CC0-Filter), Wikimedia Commons
  - NPS/Yellowstone/NPGallery, FWS, Acoustic Atlas
  - Pixabay, earth.fm, Tierstimmenarchiv
  - nicht lesbar: Zapsplat (403), BBC (gesperrt) (ton 0/1)
- **Die einzige echte Aufnahme** (#8) steht unter einer Lizenz, die die Weitergabe in Mods ausschliesst (NC).
- **Freesound:** Herunterladen geht nur mit Konto (ton 1, FAQ). Das muesste Kevin selbst tun; wir legen kein Konto an.

### 3.2 Kandidaten (zum Ja je Datei; Angaben aus ton 1, nichts angehoert)

| # | Titel | URL | Dateiname | Groesse | Dauer | Lizenz | Lizenz erlaubt Mod? | als Schlafton geeignet? |
|---|---|---|---|---|---|---|---|---|
| 1 | bear_cub_feeding | https://npgallery.nps.gov/AssetDetail/e82a43bb-d16e-46d9-84d0-27794962bf16 | `bear_cub_feeding.wav` (auch MP3) | WAV 5,3 MB (MP3 489,6 KB) | 31 s | gemeinfrei (NPS) | ja | **nein** -- Schwarzbaer-Jungtier frisst; hoechstens Jungtier-Summen, ungehoert |
| 2 | Karhut heraeaevaet, kurlutus (Baeren wachen auf, Gurgeln) | https://freesound.org/people/YleArkisto/sounds/249443/ | Freesound-Datei 249443 (Name beim Laden, ungeprueft) | 86,9 MB WAV | 5:16 | CC BY 4.0 | ja, Namensnennung Pflicht, Konto noetig | **nein** -- Aufwachen/Gurgeln, Voegel, altes Band |
| 3 | Karhut syoevaet ja murisevat (fressen, knurren) | https://freesound.org/people/YleArkisto/sounds/249440/ | Freesound-Datei 249440 | 38,4 MB WAV | 2:20 | CC BY 4.0 | ja, Namensnennung Pflicht, Konto noetig | **nein** -- Fressen/Schnaufen, ab ~40 s Knurren, Voegel, Verkehr |
| 4 | huf grizzly bear / huf grizzly | https://freesound.org/people/Nivatius/sounds/519597/ und .../519598/ | Freesound 519597, 519598 (MP3) | 7,0 KB / 5,4 KB | 0,49 s / 0,36 s | CC0 | ja, Konto noetig | **nein** -- einzelne Schnauber (vermutlich aus #5) |
| 5 | Yellowstone sound library - Grizzly Bear vocalizations - 001 | https://commons.wikimedia.org/wiki/File:Yellowstone_sound_library_-_Grizzly_Bear_vocalizations_-_001.mp3 | `Yellowstone_sound_library_-_Grizzly_Bear_vocalizations_-_001.mp3` | 1.569.578 Byte | 65 s | gemeinfrei (NPS, Nennung erbeten) | ja | **nein** -- Warn-Schnauben eines Baeren in der Falle |
| 6 | Bear slurping from mud puddle | https://freesound.org/people/selsel/sounds/824784/ | Freesound 824784 (WAV) | 14,1 MB | 51 s | CC0 | ja, Konto noetig | **nein** -- trinkt |
| 7 | Grizzly bear sound effect | https://commons.wikimedia.org/wiki/File:Grizzly_bear_sound_effect.wav | `Grizzly_bear_sound_effect.wav` | 21.817.934 Byte | ~2:04 | CC0 nur behauptet | **unklar -> nein** (Gegenpruefung 9.3: "Own work" von Konto Zagzav12 ohne Benutzerseite, hochgeladen 04.11.2026, Datum "2012", keine Aufnahmeangaben; Herkunft nicht nachpruefbar) | **unbekannt** -- Inhalt nicht beschrieben |
| 8 | Grizzly Bear breathing | https://acousticatlas.org/item.php?id=2191 | MP3 der Seite | 254 KB | 1:05 | CC BY-NC 4.0 | **nein (NC)** | inhaltlich ja (ruhender Baer) -- **verboten** |
| - | Dreams of Bears (earth.fm) | https://earth.fm/recordings/dreams-of-bears | kein Download (nur Stream) | - | - | keine Lizenz | **nein** | inhaltlich ja -- **ungeeignet** |

### 3.3 Vanilla und Bandits
Kein Spielton passt (ton 2, gesucht in `media/scripts/**` und im Jar):
- **Vanilla:** `VoiceMaleSleep`/`VoiceFemaleSleep` sind menschliche Stimmen (`scripts/generated/sounds/player/sounds_player_voice_male.txt:303-311`).
  `FishBreath` gehoert zum Fisch (`sounds_ambience.txt:301-309`). Fuer kein Tier gibt es einen Schlaf- oder Atemton.
- **Bandits:** `ZSBreath_*` ist menschliches Keuchen (`zs_sounds.txt:531-541`). Es taugt nur als Vorbild fuer die Werte eines leisen
  Nahtons (1/4/0,6).
- **Rohaufnahmen:** In den drei vorhandenen Rohaufnahmen fand die Messung keine ruhige Atemstelle
  (`_arbeit/baer_schlaf/ton/ruhe_messung.py`, ton 3).

### 3.4 Rueckfall und vorbereiteter Weg
- **Vorgabe (K8): ohne Ton.**
- **Weg fuer spaeter** (dann eine Datei und eine Zeile):
  - Rassen-Schluessel `sleep = { name = ..., slot = "voice", priority = 1 }`. Niedrigste Stufe: Schmerz, Knurren und Huff gehen vor
    (Jar `IsoAnimal.playBreedSound` Off. 40-61, ton 4).
  - Tonskript-Eintrag mit `distanceMin = 1`, `distanceMax = 8`, `volume = 0.6`, ohne `loop`. `distanceMin` muss ausdruecklich drinstehen,
    sonst gilt 10 (Jar `GameSoundClip.<init>`).
  - Den Namen legt B5a zusammen mit den sechs vorhandenen `NCBear_*`-Toenen fest; die Cheat-Regel aus 1.3 trifft `NCBear_`.
- **Abspielen ueber Client-Lua im Overlay-Sammler** (2.3), weil Weg A keinen eigenen Schlafknoten hat:
  - Bedingung: Der Baer schlaeft (Schleife laeuft) und der Spieler ist hoechstens ~8 Kacheln entfernt auf gleicher Ebene.
  - Dann alle 8-15 s `animal:playBreedSound("sleep")` (`shared/TimedActions/Animals/ISHutchGrabAnimal.lua:31`, dort in `perform()`,
    also auf dem Client; am Tier in der Welt auch `ISPickupAnimal.lua:23`). Der Ton-Takt laeuft auch, wenn der Spieler das z Z z abschaltet.
  - Das laeuft auf jedem Rechner lokal, ohne Paket, also ohne Kick-Gefahr; Tierstimmen sind Sache des Clients (ton 2.2).
  - Ein Schalter im Code (Vorgabe aus) verhindert den Aufruf, solange es keine Datei gibt.
- **Nie** `idleSoundRadius`/`idleSoundVolume` fuer den Baeren setzen: Sonst wird jeder Stimmton zum Weltgeraeusch, lockt Zombies und
  laesst ihn fliehen (`AnimalSoundState.start` Off. 33-112, ton 2.2).
- **Hoertest ohne Download (nur auf K8-Wort):** den vorhandenen `NCBear_Huff.wav` als eigener, sehr leiser Eintrag (`distanceMin 1`,
  `distanceMax 6`, `volume 0.4`) alle 8-15 s. Ehrlich: Ein Atemstoss von 0,21 s ist kein Schnarchen.

---

## 4. Baerenbett

### 4.1 Groesse
1 Kachel = 1,225 m (1 Modelleinheit = 1,5 Kacheln, `Core.DoPushIsoStuff`; `spiel/bau_lebend.md:48`; bett 1.1).

| Was | Meter | Kacheln | Quelle |
|---|---|---|---|
| Erwachsener (1,35) Sphinx, Kopf gerade | 2,57 x 1,50 | 2,10 x 1,23 | referenz 6 (Haut gemessen, +-5 cm) |
| Erwachsener Sphinx, Kopf 25 Grad zur Seite (= Pose L) | 2,52 x 1,50 | 2,06 x 1,23 | referenz 6 |
| zum Vergleich: Seitenlage `DeerStag_Dead` / Stehen | 2,54 x 1,45 / 2,62 x 1,31 | 2,07 x 1,19 / 2,14 x 1,07 | bett 1.2 |
| **Bett aussen (Vorschlag, K11)** | **3,06 x 1,96** | **2,5 x 1,6** | dieser Plan |
| **Liegeflaeche innen** (Rahmen 10 cm je Seite) | **2,87 x 1,76** | **2,34 x 1,44** | dieser Plan |
| Belegung im Raster | | **2 x 3 Kacheln** (je 0,2-0,25 Luft) **nur, wenn die Bettmitte laengs auf einer Kachelmitte und quer auf einer Kachelkante liegt**; mittig auf einer Kachel 3 x 3, frei gedreht mehr (Gegenpruefung 9.4) | bett 1.3 |

**Widerspruch geklaert:**
- Bett 1.3 schlug 2,5 x 1,5 vor, gemessen an der Seitenlage `DeerStag_Dead` (1,19 Kacheln breit).
- Die Sphinx ist 4 cm breiter (1,23 Kacheln). Bei 1,5 Kacheln blieben je Seite nur 7 cm Luft, bei +-5 cm Messgenauigkeit und Atmen zu knapp.
- Referenz 5 verlangt innen mindestens 2,8 x 1,65 m.
- Mit 1,6 Kacheln Breite: 13 cm Luft je Seite und 17 cm an den Enden. Das passt "genau", und der Baer liegt nicht verloren darin (3 x 2 waere die Alternative in K11).

**Endmass:** aus dem echten Schlaf-Clip. Der Messer der Clip-Runde fuehrt `python -B _arbeit/baer_schlaf/bett/mess_umriss.py <neues GLB>`
ueber alle Bilder der Schleife aus -- und ebenso ueber Hinlegen, Aufwachen und Aufschrecken, denn die Pranken treten dabei vor und
zurueck, waehrend er schon auf dem Bett steht. Bettmass = Umriss x 1,35 + ~0,12 Kacheln Luft je Seite + Rahmen (bett 1.4).

Jungtier (0,35) und Halbstark (0,75) liegen mittig im selben Bett: ein Bett fuer alle Stufen.

### 4.2 Bau-Weg: (a) 3D-Bodengegenstand

| Weg | Urteil | Grund |
|---|---|---|
| **(a) Gegenstand mit Bodenmodell** (`WorldStaticModel`) | **ja** | im Projekt schon dreimal bewaehrt: Turret, Rucksack-Bodenmodell, Baeren-Statue der Test-Mod (bett 2a). Aufstellen, Drehen, Aufheben und Versetzen macht Vanillas "Place item on ground" (`ISInventoryPaneContextMenu.lua:4420-4436`, `ISExtendedPlacementUI.lua:429-454`), samt Sendung an alle (`ISDropWorldItemAction.lua:81-87`). Keine eigenen Kacheln, kein `tiledef`. Als Gegenstand traegt es nie das Bett-Flag der Engine, also legen sich weder NPCs noch Spieler hinein (Naht N4) |
| (b) eigene Kacheln (.tiles/.pack) | nein | 24 Iso-Bilder, `tiledef`-Nummer muss ueber alle Mods eindeutig sein (`ChooseGameInfo`, bett 2b), ein `bed`-Flag waere sogar schaedlich |
| (c) Eintrag im Bau-Menue (B42-Entity) | spaeter, auf Wort (K12) | Mischform c+a: Bau-Cursor mit Vanilla-Heuballen als Platzhalter, `OnCreate` legt das 3D-Bett aus (a) hin (Vorbild Futtertrog/NPC-Crew-Beacon, bett 2c). Mehr Code; der Cursor zeigt einen Heuballen |
| (d) Vanilla-Tierbett | gibt es nicht | nur Trog, Stall fuer Kleintiere, Heu (bett 2d) |

### 4.3 Gegenstand, Rezept, Namen
- **Gegenstand:** `NPCCrew.BearBed` (Modul `NPCCrew` wie `NPCCrew.CrewBackpack`).
  - Bodenmodell `NPCCrew_BearBed_Ground` in `module Base`, FBX `models_X/WorldItems/NPCCrew_BearBed_Ground.fbx`, Icon `Item_NPCCrew_BearBed`.
  - Gewicht 15, `DisplayCategory = Furniture`.
  - **Name fuer immer stabil.** Kollisionsprobe 0 Treffer (bett 3.1; eigene Probe 09.11., 2.3).
- **Rezept** (Vorschlag, K13; Form `MakeWoodenToolbox`, `recipes_carpentry.txt:296-317`; Zahlen bett 3.1):
  - Name `MakeNPCCrewBearBed`, Schreinerei, Holzarbeit 2, 300 Zeiteinheiten.
  - Hammer bleibt erhalten; dazu 8 Bretter, 12 Naegel, 30 Heu (`Base.HayTuft`), 2 Laken oder 1 grosses Leder.
  - Schreibweise fuer "1 grosses Leder ODER 2 Laken": `item 1 [Base.Leather_Crude_Large;2:Base.Sheet]` (Form Vanilla
    `recipes_tailoring_leatherAndHide.txt:1271`, `item 1 [Base.Leather_Crude_Large_Tan;2:Base.Leather_Crude_Medium_Tan]`). **Nicht** die Zeile aus
    bett 3.1 `item 2 [Base.Sheet;Base.Leather_Crude_Large]`: die verlangt 2 Stueck von einem der beiden, also auch 2 grosse Leder (9.4).
  - Ein Baerenfell-Item gibt es nicht (grep, bett 3.1).
- **Texte in sieben Sprachen:**
  - `Translate/<L>/ItemName.json` (Schluessel `NPCCrew.BearBed`), `Recipes.json`, `Tooltip.json` (`Tooltip_BN_Bear_Bed`), `UI.json` (`UI_BN_Bear_Bed*`).
  - NPC Crew hat heute nur `Sandbox.json`, `Tooltip.json`, `UI.json` (selbst nachgesehen, `shared/Translate/EN`). `ItemName.json` und
    `Recipes.json` werden sortiert zusammengefuehrt; wer zuerst kommt, legt an, nie doppelt (Naht wie Zweihaender/Rucksack, `../CLAUDE.md` 7).
- **Testhilfe** "Bett hinlegen" nur in `NCBearBench*.lua`.

### 4.4 Aussehen (K12) und Modell-Kette
- **Form:**
  - Flaches Strohlager in einem niedrigen Rahmen aus vier groben Balken, Ecken mit Seil gebunden. Rahmen an drei Seiten 10-12 cm hoch,
    das Kopfende flach (nur ein Heuwulst), damit Kinn, Pranken und die z Z z-Stelle frei bleiben (referenz 5).
  - Heu innen 3-4 cm hoch, am Rand aufgehaeuft, ein paar Halme ausserhalb.
  - Eine zusammengelegte rotbraune Decke am Kopfende als flaches Kissen.
  - Kein "BEAR"-Schild: Bei 256er Texturdeckel ist es nicht lesbar (bett 4).
- **Kette** (bett 4, Vorbild `rucksack/spiel_b/spiel_b.py`): Skript `baer/bett/bett_bau.py -- alles`, Blender 5.2.3 im Hintergrund.
  - Modell prozedural, 1.500-3.000 Dreiecke, Laengsachse Blender +X, Ursprung = Mitte der Liegeflaeche auf z = 0.
  - UV, Backen in 512 (OPTIX nur auf der 4090, nur wenn PZ nicht laeuft).
  - FBX mit `axis_forward="-Z"`, `axis_up="Y"`, `FBX_SCALE_ALL`; Skript-`scale = 0.544`.
  - Icon 32x32.
  - Pruefung offline mit `mess_umriss.py` und Draufsicht mit dem Baeren darauf (`_arbeit/baer_schlaf/bett/bild_draufsicht.py` erweitern).

### 4.5 Hoehe
**Flach.** Der Clip legt den Baeren auf den Boden (z = 0). Hoehe im Clip hiesse einen zweiten Satz Clips (am Boden und neben dem Besitzer
soll er auch schlafen). Eine Hoehe per `setZ` ist in Vanilla nur an einem Tier am Schlachthaken belegt (`ButcheringUtil.lua:577`); ob ein
freies Tier eine Bruchteil-Hoehe behaelt, ist **ungeprueft** (referenz 5, bett 1.4). Der Baer sinkt 3-4 cm "ins Stroh"; das sieht
natuerlich aus und verdeckt Bauchunterseite und Bodenberuehrung.

### 4.6 Wie der Baer es findet und sich hinlegt (SP)
1. **Suchen:** Nur wenn er schlafen will (selten, nie je Bild), im Umkreis 25 Kacheln um Zuhause oder Besitzer nach Bodengegenstaenden
   `NPCCrew.BearBed`. Form wie `client/NCBearTest.lua:44-60`: `getCell():getGridSquare`, `getWorldObjects`, `getItem():getFullType()`
   (Vanilla `ISWorldObjectContextMenu.lua:2973-2975`, bett 3.3).
2. **Gueltig nur, wenn:**
   - es am Boden liegt (`getWorldPosZ()` gleich der Ebene; der Spieler kann es im Platzier-Fenster anheben oder kippen),
   - die Flaeche frei ist (Rechteck nach `getWorldZRotation()` gedreht, Stichpunkte alle 0,25 Kacheln, Pruefung wie `flyOk`,
     `lua/shared/NCBearFight.lua:707-718`),
   - kein anderer Baer darauf liegt.
3. **Merken:** Lage und Drehung kommen ins Baeren-Gedaechtnis. Naechste Nacht zuerst dort nachsehen; der Baer merkt sich keine
   Gegenstands-Id, ein versetztes Bett bricht also nichts.
4. **Hingehen:** `pathToLocation` am Tier (Kevins Ausnahme mit Jar-Beleg, `ENTSCHEIDUNGEN.md:43`).
5. **Ausrichten:**
   - Der Liegepunkt liegt nicht in der Bettmitte: Die Mitte des Umrisses liegt 0,15 m x Groesse VOR dem Wurzelpunkt (bei 1,35:
     0,16 Kacheln, referenz 5). Darum steht der Wurzelpunkt so weit zum Fussende versetzt.
   - Blick zum flachen Kopfende.
   - Feinsetzen mit `animal:setX/setY(zahl)`: belegt AM TIER (`ButcheringUtil.lua:575-576`, selbst nachgesehen; dort ein Tier am Haken).
     Der Bett-Bericht sagte "am Tier nicht belegt"; das ist hiermit berichtigt. Ob die Engine die Kachel des Tiers nachzieht, wenn das
     Feinsetzen ueber eine Kachelkante geht, ist **ungeprueft** (dort setzt Vanilla danach gleich `setOnHook`); darum nur kleine Schritte
     und moeglichst hinlaufen.
   - Drehen mit `faceLocationF(x, y)`: Vanilla am Spieler (`shared/TimedActions/ISGetOnBedAction.lua:167`), Bandits am Zombie
     (`42.21/.../ZombieActions/ZAAim.lua:12`). IsoAnimal erbt von IsoPlayer und ueberschreibt die Methode nicht (Dump `IsoAnimal.txt`:
     keine eigene `faceLocationF`, `setDir`, `setX`, `setY`; selbst nachgesehen). Kevins Wort K19.
   - Rueckfall ohne sein Wort: `setDir(IsoDirections.X)` (`ButcheringUtil.lua:574`), nur 8 Richtungen. Ein frei gedrehtes Bett
     (Drehgriff ohne Raster, `ISExtendedPlacementUI.lua:429-439`) laesst ihn dann bis 22,5 Grad schief liegen; bei 2,5 m Laenge ragt er
     ueber den Rand.
6. **Hinlegen** wie 1.3. Ist kein Bett gueltig, schlaeft er am Boden (5.2).

### 4.7 Mehrspieler
- **Aufstellen und Aufheben:** Vanilla-Aktionen mit Sendung an alle (`ISDropWorldItemAction.lua:81-87`).
- **Gehirn auf dem Server:** Die Suche laeuft dort, wo das Gehirn laeuft (`not isClient()`). Ob der Server die Kacheln um ein Bett
  geladen hat, wenn der Besitzer in der Naehe ist, ist **ungeprueft** (Bandits liest Zellen auf dem Server, `server/BanditServerZombie.lua:15`).
- **Wem das Bett gehoert:** ein Register beim Server (globale ModData; Client bittet, Server prueft und schreibt; Vorbild NPC Crew
  `shared/BanditsNPCBeaconRegistry.lua:20-47`). Das gehoert zu B2a.
- **Bis dahin:** SP ja, MP offen.

---

## 5. Schlafen wie die NPCs

### 5.1 So schlafen die NPCs (npcschlaf 1)
- **Wann:** Nachtfenster 22-7 Uhr (`shared/BanditsNPCRoutine.lua:224-229`), Muedigkeit >= 30 und frei in der Basis (Bleiben/Relaxen,
  :239-248); Zusammenbruch ab 90 zu jeder Zeit (:241). Folgen und Wache sind Pflicht: das Nachtfenster greift dort nicht (`Routine.lua:236-243`,
  nur `NPCStay`/`NPCRelax`). Die Muedigkeit steigt aber **nur beim Folgen** (sowie Leichen entsorgen und Pluendern) nicht
  (`BanditsNPCNeeds.lua:478`, `following` = `NPCCompanion`/`NPCCorpse`/`NPCLoot`); **auf Wache steigt sie** und kann zum Zusammenbruch ab 90
  fuehren (berichtigt, 9.2).
- **Wo:** freies Bett der Basis, sonst der Boden.
- **Aufwachen:** Bedrohung binnen 7 Kacheln, Fensterende, ausgeschlafen (auch um 2-3 Uhr, `Programs.lua:4310-4319`), jeder Befehl,
  Bett weg.
- **Muedigkeit:** steigt 1,6 je Spielstunde; im Schlaf sinkt sie im Bett um 15, am Boden um 10,5 je Weltstunde (`Programs.lua:5044-5101`).
- **Kein z Z z** ueber schlafenden NPCs.
- **Im MP** rechnet bei den NPCs der Rechner des Besitzers.

### 5.2 Der Baer (Vorschlag; Grundsatz: Kampf hat Vorrang, Passiv bleibt, `ENTSCHEIDUNGEN.md:66/118`)
Gerechnet unter `not isClient()` (SP und Server, derselbe Code; Tiere rechnet der Server, `PLAN.md:216-240`). Bewusster Unterschied zu
den NPCs: Bei ihnen rechnet der Besitzer-Client. Der Zustand wird immer neu abgeleitet (Uhr, Muedigkeit, Befehl), nie als Marke allein
gespeichert (Lehre "STALE SLEEP FLAG", `client/BanditsNPCGuardian.lua:4056-4080`).

**Wann er schlaeft:**

| Lage | schlaeft? |
|---|---|
| Bleiben, Sitz, Frei herumlaufen (Basis) | nachts im Fenster und Muedigkeit >= 30 |
| Folgen, Komm her | nein (Pflicht, Muedigkeit steigt nicht) |
| **Besitzer schlaeft** und Baer in Folge-Abstand | ja, legt sich neben ihn (K17) |
| Muedigkeit >= 90 | ja, wo er steht |
| Jungtier 13-15 Uhr, Muedigkeit >= 30 | Mittagsschlaf (K15) |
| Gefahr in Suchweite / gerade gekaempft | nie einschlafen; 10 s Sperre nach jedem Abbruch (Muster `Routine.lua:743-759`) |
| Hunger oder Durst kritisch und Futter in Inventar/Trog | erst fressen, dann schlafen |

- **Bis die Befehle gebaut sind** (Schlaf-Grundstufe, Abschnitt 6) gilt eine Uebergangsregel: Er schlaeft nachts, wenn er in der Ruhe-Phase
  ist und kein Ziel hat.
- **Durchschlafen bis 7 Uhr** (K14), auch wenn die Muedigkeit vorher 0 erreicht. Den Baeren will man schlafen sehen; die NPCs stehen
  um 2-3 Uhr auf.

**Wo er schlaeft** (Reihenfolge):
1. **Neben dem schlafenden Besitzer:** freie, stehbare Kachel 1-2 neben ihm (`square:isFree(false)`, `ISWorldObjectContextMenu.lua:2199`),
   mit Platz in Laengsrichtung. Nie die Kachel des Besitzers, nie eine Kachel mit Bett-Flag (`ISWorldObjectContextMenu.lua:2642`).
2. **Eigenes Baerenbett** in derselben Basisflaeche (4.6): zuerst das eigene, sonst ein freies (K20).
3. **Boden, wo er steht**, nie auf Bett- oder Moebelkacheln. Erholung 70 % (Crew-Regel). Bei "Bleiben" ausserhalb der Basis an der
   Bleib-Stelle.

**Aufwachen:**

| Grund | danach |
|---|---|
| **Gefahr**: dieselbe Zielsuche wie im Kampf (`pickTarget`, Radius 10 Zombies / 12 Banditen, `NCBearFight.lua:86/:376`), geweckt wird 2 Kacheln weiter als gekaempft | Halbstark/Erwachsen: aufschrecken (1,1 s), kaempfen. **Passiv**: aufstehen, beim Befehl bleiben bzw. zum Besitzer (K16). **Jungtier**: zum Besitzer, verstecken. Danach 10 s ruhig, dann wieder hinlegen, wenn noch faellig |
| Treffer | sofort wach wie bei Gefahr |
| Morgen 7 Uhr | ruhig aufstehen, zurueck zum Befehl |
| ausgeschlafen ausserhalb des Fensters (Mittagsschlaf, Zusammenbruch) | aufstehen |
| jeder Befehl (Folgen, Komm her, Bleiben, Sitz, Frei, Q-Ruf) | aufstehen, Befehl (K18: kein eigener Weck-Knopf) |
| Besitzer wacht auf (Ort 1) | aufstehen, folgt wieder |
| Hunger oder Durst >= 90 | wach, frisst/trinkt aus Inventar/Trog, legt sich wieder hin (Abweichung von den NPCs: beim Baeren kosten sie Leben, `PLAN.md:150-151`) |
| Laerm (Engine-Flucht) | wie im Sitzen: `idleAction` sofort loeschen, nach 30 s Ruhe wieder hinlegen; mehr als 4 Stoerungen in 30 s: wach bleiben (`CALM_NOISE_MAX`, `NCBearFight.lua:197`) |
| Streicheln (Vanilla setzt "petting", `ISPetAnimal.lua:43`, und loescht danach ganz, `:48/:55/:62`) | steht sanft auf, laesst sich streicheln, legt sich nach 30 s wieder hin, wenn noch Nacht (K19) |
| jeder andere `idleAction`-Wert (z. B. "eat" beim Locken, Jar `IsoAnimal.eatFromLured` Off. 20-27, engine 3.5) | Regel: gilt `not animal:isAnimalSitting()`, ohne dass unser Code geweckt hat, ist der Schlaf vorbei; wie Streicheln behandeln |
| Downed, Tod, Unstuck-Knopf | Schlafzustand restlos weg, ohne Aufsteh-Clip |

**Muedigkeit und Beduerfnisse** (npcschlaf 4.5, Zahlen im Bau):

| Wert | Jungtier | Halbstark | Erwachsen |
|---|---|---|---|
| Anstieg je Spielstunde wach (nicht beim Folgen) | 2,6 | 2,0 | 1,6 |
| Abbau im Schlaf je Weltstunde: Bett / Boden | 15 / 10,5 | 15 / 10,5 | 15 / 10,5 |
| Schwelle Nacht / Zusammenbruch | 30 / 90 | 30 / 90 | 30 / 90 |

- Die Uhr zaehlt Weltstunden seit dem Einschlafen; das haelt auch bei Zeitraffer und Spielerschlaf. Ohne geladenen Baeren zaehlt nichts.
- Hunger und Durst steigen im Schlaf weiter (unser Takt).
- Laune: Eine durchgeschlafene Nacht im Baerenbett hebt sie, oft geweckt ohne Kampf senkt sie leicht ("gute Naechte der letzten 3 Tage").
- Nach dem Laden mitten in der Nacht wird der Zustand neu abgeleitet.

### 5.3 Mehrspieler
- **Bild:** Der Server entscheidet, das Bild reist ueber `idleAction` von selbst (1.3).
- **Schlaeft der Besitzer?** Auf dem Client belegt `player:isAsleep()` (`client/Context/ISMenuContextWorld.lua:41`). Ob der Server den
  Bettschlaf eines Spielers sieht, ist **ungeprueft** (npcschlaf 4.8). Rueckfall: Der Besitzer-Client meldet "schlaeft/wach" per
  `sendClientCommand`, der Server prueft nur den Besitz; eine falsche Meldung legt hoechstens den eigenen Baeren hin.
- **Kampf im MP** ist bis B9 aus: Gefahr weckt ihn, er zieht sich aber wie Passiv zurueck.
- **Logout des Besitzers:** Der Baer ruht (`PLAN.md:229-230`) und legt sich dafuer schlafen. Bei Gefahr wacht er trotzdem auf.

### 5.4 Naehte zu NPC Crew (Form `turret/NAEHTE.md`)
Keine NPC-Crew-Datei wird geaendert. Jeder Zugriff liest zur Laufzeit hinter einem Existenz-Riegel; jeder Aufsatz kommt in `OnGameBoot`.

| # | Was | NPC Crew (Fundstelle) | Wie | Ohne NPC Crew |
|---|---|---|---|---|
| N1 | Nachtfenster | `Routine.InSleepWindow`, `SleepStart/End` (`shared/BanditsNPCRoutine.lua:224-229`, shared) | lesen | eigene Vorgabe 22/7 |
| N2 | Basisflaeche | `BeaconRegistry.Sites` (`shared/BanditsNPCBeaconRegistry.lua:46`), `SiteRules.BaseZone/ZoneContains` (`shared/BanditsNPCSiteRules.lua:110/:549`), laeuft auf dem Server | genau in der Form von `ownZoneAt` (`shared/BanditsNPCNav.lua:255-277`); das Uebernahme-Skript prueft, ob es die Felder noch gibt und `BASE_KIND = "base"` (`SiteRules.lua:100`) gilt | vom Spieler gesetzter Bereich |
| N3 | NICHT benutzen | `BanditsNPC.Zones.Contains`, `Base.SiteNear`, `Base.Zone` (client/ bzw. falsch auf dem Server, npcschlaf S3) | - | - |
| N4 | Baerenbett ist kein NPC-/Spielerbett | `Base.P.sleepable` fragt `IsoFlagType.bed` (`shared/BanditsNPCBase.lua:201-204`) | durch Weg (a) erfuellt (Gegenstand, kein Bett-Flag); bei Weg c+a der Heuballen-Platzhalter mit `BedType = badBed` nur im Cursor -- pruefen | gleich |
| N5 | Baer nie im Menschenbett | `tileHasOther` ignoriert IsoAnimal (`Base.lua:1603-1619`) | Baer meidet Kacheln mit Bett-Flag | gleich |
| N6 | Tierpfleger der Crew | zaehlt `bear` als Vieh (`tier_spez.md` 5.4) und setzt `idleAction = "petting"` (`BanditsNPCLivestockAnimalOps.lua:1077`) -> weckt den schlafenden Baeren auf diesem Client, das naechste Paket legt ihn wieder hin (Flackern) | Ausnahme braucht eine NPC-Crew-Version und Kevins Wort (schon offen, `PLAN.md:144-146`) | entfaellt |
| N7 | Foersterin, Pluenderer, Farmer, MP-Nehm-Tuer am Bett-Gegenstand | `Forestry.PolicyIn/NoteIn`, `SiteRules.LootTypeRefused` (`BanditsNPCSiteRules.lua:926-929`), `F.Blocked`/`Fm.DigOk` | je ein Aufsatz wie Turret #39/#40 (`turret/NAEHTE.md:54`) | entfaellt |
| N8 | Spielerschlaf | Vanilla und NPC Crew zaehlen nur Zombies (Jar `IsoPlayer.updateLOS` Off. 648-650; `client/BanditsNPCSleep.lua`) | nichts noetig | gleich |
| N9 | Zeichnen | `BanditsNPC.ClientCfg` (Datei `NPCCrewClient.ini`, neuer Abschnitt `BearOverlay`), `BanditsNPC.UI.C` (Farben) | lesen | Speicher, eigene Farben |
| N10 | `OnSleepingTick` | NPC Crew nutzt es (`client/BanditsNPCPersistence.lua:10412-10419`) | eigener, zusaetzlicher Eintrag (Vanilla `ISSleepingUI.lua:92`) fuer die MP-Meldung "Besitzer schlaeft" | gleich |
| N11 | Texte | `UI_BN_Rt_fatigue_at` = "Sleeping" | eigene `UI_BN_Bear_Sleep_*`, `UI_BN_Bear_Bed*`, sieben Sprachen; immer mit Unterstrich greppen (`UI_BN_Bear` trifft `UI_BN_Beard_*`, ton 4) | Test-Mod-UI.json |
| N12 | Dateien | - | `shared/BanditsNPCBearSleep.lua` (Zustand, Regeln, Bett finden), `client/ISUI/BanditsNPCBearOverlay.lua` (z Z z, Schlafton-Takt, spaeter Name/Balken); Testhilfen NUR `NCBearBench*.lua` | gleich |
| N13 | Cheat-Pruefung | Regel "befehl" `\bNC[A-Z]...` (`turret_uebernahme.py:99`) | trifft heute `NCBear_*`-Clip- und Tonnamen in Lua-Strings -> in B5a umbenennen oder einzeln erlauben; die Schlaf-Clips haben Vanilla-Namen | - |
| N14 | Sandbox | - | erst keine Option (Vorschlag); falls gewuenscht `BanditsNPC.BearSleepAtNight` | - |

Bandits: nur als Muster (Uhrzeitfenster, "Treffer weckt", gesperrtes Aufstehen; `ZPCamper.lua:17-90`, `BanditUpdate.lua:2348-2353`).
`Bandit.SetSleeping` gilt fuer IsoZombie mit Bandits-Gehirn und ist fuer den Baeren nicht verwendbar (npcschlaf 2).

---

## 6. Einordnung in STAND.md (Vorschlag, K5) und Abhaengigkeiten

| STAND | Was | Schlaf-Anteil | braucht |
|---|---|---|---|
| 2 | baer-fell fertig machen (Pruefer, Nachbesserung, Gegenpruefer) | - | - |
| 3 | **Clip-Runde** | **S1 Schlaf-Clips** (1.4), Messungen fuer Bett und z Z z | neues Netz aus baer-fell, K1-K4; Gewichte neu |
| 4 | B5a Gegenwehr (zuerst Umbenennen) | Namensregel fuer Aufschreck-Clip und Toene (N13) | - |
| **4b neu** | **Lauf baer-schlaf-bau** | **S2** Schlaf-Grundstufe (Uebergangsregel 5.2, Aufwachen, Boden/Bett) + **z Z z** (2) + stummer Tonweg (3.4) + **S3 Baerenbett** (4) | S1 (Clips, Masse, Kopfhoehe), B5a (Namen, Treffer) |
| 5 | B1 + Baby + Zaehmen | Jungtier-Groesse fuer z Z z; Baby-Modell braucht ggf. eigene Schlaf-Clips | - |
| 6 | Befehle und Fenster | **S4a**: Schlaf an Bleiben/Sitz/Frei/Folgen, neben dem schlafenden Besitzer, Basisflaeche (N2), Bett in der Basis; z Z z-Schalter, Name und Balken ins selbe Overlay | Besitz/Register (B2a), Befehle (B2b) |
| 7 | Beduerfnisse | **S4b**: Muedigkeit je Stufe, Hunger/Durst wecken, Laune "gute Naechte", Mittagsschlaf | B3 |
| 10 | Mehrspieler | Bett-Register, Meldung "Besitzer schlaeft", Abnahme im MP mit Rolle `user` | B8 |

**Lauf baer-schlaf-bau** (9 Agenten):
1. Planer
2. Bauer Schlaf-Gehirn: `BanditsNPCBearSleep.lua`, Anbindung an die Ruhe-Phase, Bench-Befehle
3. Bauer Overlay: `BanditsNPCBearOverlay.lua`
4. Bauer Bett-Modell: `baer/bett/bett_bau.py`
5. Bauer Bett-Skript/Rezept/Texte (sieben Sprachen; einziger, der `Translate/` anfasst)
6. Pruefer Code: luacheck, scopecheck, localcount, luacheck_pz, Engine-Belege, Lua-5.1-Attrappe
7. Pruefer Masse/Optik: Bett gegen Umriss, Draufsicht, Spielwinkel
8. Gegenpruefer
9. Integrator

Nachbessern tun die Bauer selbst. Vor dem Lauf den Verbrauch pruefen und Kevin die Zahl nennen.

**Warum so:**
- Die Clips brauchen das neue Netz; ein zweiter Gewichte-Lauf kostet Zeit.
- Das Bettmass und der z Z z-Anker brauchen den echten Clip.
- Neue Lua-Dateien kommen erst nach der Umbenennung in B5a, dann gleich mit NPC-Crew-Namen (sonst waechst die Umbenennung).
- Kevins Reihenfolge Gegenwehr -> Baby bleibt bis auf den kleinen Lauf 4b erhalten. Will er das Baby zuerst, rueckt 4b hinter B1 (K5).

---

## 7. Fragen an Kevin

Vorschlag in Klammern; "Ja, alle so" nimmt alle Vorschlaege.
- K1 Schlafhaltung "Sphinx": Bauch, Kinn auf den Pranken, im Schlaf Kopf leicht zur Seite. (Ja; Seitenlage nicht, sieht aus wie tot.)
- K2 Erst nur diese eine Haltung, "eingerollt" hoechstens spaeter. (Ja.)
- K3 Bei Gefahr schnelles Aufschrecken (1,1 s) statt ruhigem Aufstehen (2,2 s). (Ja.)
- K4 Extra-Bewegungen "Bett zurechtscharren" und "wach liegen und umschauen". (Nein, spaeter.)
- K5 Reihenfolge: Schlaf-Bewegungen in die Clip-Runde, Schlafen + z Z z + Bett als ein Lauf nach der Gegenwehr, vor dem Baby. (Ja.)
- K6 z Z z wie die NPC-Namen: fast weiss, beim Zoomen gleich gross, hinter Waenden und hinter dir unsichtbar. (Ja; nicht Nachtblau.)
- K7 z Z z je Spieler im Baeren-Menue abschaltbar, Vorgabe an. (Ja.)
- K8 Erst einmal ohne Schlafton; der Weg fuer einen spaeteren Ton liegt bereit. (Ja; kein Hoertest mit dem Schnauber.)
- K9 Ausnahme fuer CC-BY-Aufnahmen oder selbst bei Yellowstone nach "Grizzly Bear breathing" fragen. (Beides nein.)
- K10 Kandidaten aus 3.2 laden. (Keine; alle sind kein schlafender Baer.)
- K11 Bett 2,5 x 1,6 Kacheln (3,1 x 2,0 m, passt genau, belegt 2 x 3 Kacheln, wenn passend hingestellt, sonst 3 x 3) statt 3 x 2. (2,5 x 1,6.)
- K12 Bett-Aussehen: flaches Strohlager im niedrigen Holzrahmen, Decke als Kissen, kein "BEAR"-Schild; Bau-Menue spaeter. (Ja.)
- K13 Rezept: Hammer, 8 Bretter, 12 Naegel, 30 Heu, 2 Laken oder 1 grosses Leder, Holzarbeit 2. (So.)
- K14 Er schlaeft nachts durch bis 7 Uhr (nicht wie die NPCs um 2-3 Uhr auf). (Ja.)
- K15 Erwachsene schlafen nur nachts, das Jungtier dazu Mittagsschlaf 13-15 Uhr. (Ja.)
- K16 Passiv und Gefahr im Schlaf: aufstehen und zu dir kommen. (Ja.)
- K17 Du schlaefst und er folgt dir: er legt sich neben dich. (Ja; nicht wach Wache halten.)
- K18 Kein eigener Befehl "Schlafen" und kein Weck-Knopf, jeder Befehl weckt. (Ja.)
- K19 Streicheln weckt ihn sanft, danach legt er sich wieder hin; zum genauen Ausrichten im Bett darf er eine Drehung benutzen, die das Spiel bei Spielern nutzt. (Ja.)
- K20 Mehrspieler: zuerst das eigene Baerenbett, sonst ein freies; z Z z fuer NPCs nicht jetzt. (Ja.)
- K21 (neu aus der Gegenpruefung) Damit das z Z z ueber dem KOPF steht, muss das Spiel fragen, wohin der Baer schaut. Die Frage dafuer
  ist im Spiel nur bei Spielern und Zombies benutzt, beim Tier nicht (gleiche Methode, geerbt). Darf sie beim Baeren benutzt werden?
  (Ja; sonst steht die Saeule ueber der Baerenmitte, beim Erwachsenen ueber dem Buckel statt ueber dem Kopf.)

---

## 8. Offene Risiken (alles ungeprueft, nichts gespielt)

1. **Sprung bei Laerm oder Treffer:** Die Engine-Flucht reisst ihn ohne Aufsteh-Clip aus dem Liegen. Lua kann das nicht verhindern,
   beim Sitzen ist es heute genauso (engine 4.3). Wie es aussieht: ungeprueft.
2. **Dauern:** Das Ende von Hinlegen und Aufstehen kennt Lua nur ueber die Uhr. Stimmen die Dauern nicht mit dem GLB, steht er zu frueh
   oder zu spaet auf (engine 7.2).
3. **Hinlegen ohne Clip,** wenn "sit" gesetzt wird, bevor er 0,5 s in idle1 stand (engine 4.2). Dasselbe beim Betreten des
   Idle-Zustands aus dem Gehen.
4. **Aufschrecken:** Das Ueberblenden aus der Vanilla-Schleife in den eigenen Knoten ohne Sprung ist eine Lesart, ungeprueft.
5. **Fehlender Clip laesst ihn stehend erstarren** (`AnimationPlayer.updateInternal` Off. 35-44, engine 3.3). Die Clips gehen nur
   zusammen mit dem neuen GLB in die Test-Mod.
6. **Liegepose:** Ellbogen und Hinterfuss stecken in der Probe noch im Boden. Die Falten an Achsel/Ellbogen liegen schon heute ueber
   dem Ziel (referenz 6, 4). Ob 1-1,5 cm Atem-Hub aus der Spielkamera zu sehen ist: ungeprueft.
7. **Fremde Mods:** Ein Mod, der `sitRandomly` des Baeren auf wahr setzt, legt ihn alle 3-7 Stunden zufaellig hin (engine 6.1).
8. **z Z z:**
   - Kopfhoehe und -vorlage sind geschaetzt, bis der Clip steht.
   - Ob die Vorwaertsrichtung zum Modellblick passt, ist ungeprueft; sonst steht die Saeule ueber dem Hinterteil. Die Abfrage selbst
     braucht Kevins Wort (K21); ohne es steht die Saeule ueber der Mitte.
   - Die Saeule liegt ueber der Welt: Baeume und Daecher verdecken sie nicht.
   - Dreht sich der Spieler weg, verschwindet sie. Im geteilten Bildschirm gibt es sie nicht.
9. **MP:**
   - Ob ein Client die Uebergaenge sauber spielt, wenn der Wert sprunghaft kommt: ungeprueft.
   - Ein Client streichelt (oder der Tierpfleger N6): kurzes Aufstehen und Hinlegen auf diesem Client. Ob `ISPetAnimal` im MP auch
     auf dem Server laeuft (dann saehen es alle, und unser Gehirn behandelt es als Streicheln), ist **ungeprueft**; `start()` hat
     einen eigenen `if not isClient()`-Zweig (`ISPetAnimal.lua:21-23`), was darauf hindeutet.
   - Ob der Server den Bettschlaf des Besitzers sieht: ungeprueft.
   - Das Baeren-Gehirn laeuft heute nur im SP.
   - Ob `playBreedSound` auf einem MP-Client hoerbar ist: ungeprueft.
10. **Laden mitten in der Nacht:** Vielleicht legt er sich nach jedem Laden sichtbar neu hin. Ob ein frueh gesetztes "sit" den
    Uebergang ueberspringt: ungeprueft.
11. **Bett:**
    - Verdecken an Waenden bei einem 2,5 Kacheln langen Bodenmodell: ungesehen.
    - Grenzen von "Place item on ground" bei grossen Modellen: ungeprueft.
    - Der Spieler kann das Bett anheben oder kippen.
    - Ob die Tier-KI eine Drehung per `faceLocationF` haelt: ungeprueft.
    - `setX/setY` ist nur an einem Tier am Haken belegt, nicht an einem frei laufenden.
12. **Platz am Boden:** Der erwachsene Baer ist am Boden 2,6 m lang und ragt neben Waenden und Moebeln hinein. Er braucht freie
    Nachbarkacheln in Laengsrichtung.
13. **Engine-Wandern** verschiebt den liegenden Baeren ohne Sperre; dieselbe Abwehr wie beim Sitzen ist noetig (npcschlaf 7.1).
14. **Datenform-Naht N2:** Aendert NPC Crew das Format der Basisflaeche, irrt sich der Baer.
15. **Baby-Modell:** Waehlt Kevin ein eigenes, braucht es eigene Schlaf-Clips, falls das Skelett abweicht.

Statisch geprueft, nicht gespielt.

---

## 9. Gegenpruefung (Datum 09.11.2026)

Unabhaengig, streng, nur gelesen: jede Fundstelle selbst geoeffnet, Jar-Dumps dieses Laufs gelesen, Lizenzseiten neu gelesen, Rechnungen
nachgerechnet. Nichts heruntergeladen (nur Webseiten gelesen, keine Audiodatei), nichts gebaut, keine Mod-Datei geaendert, keine GPU.
Geaendert wurde nur diese Datei. **Statisch geprueft, nicht gespielt.**

### 9.1 Geprueft und richtig (rund 100 Stellen)
- **AnimSet:** `AnimSets/buck/idle/idle1.xml:5-9`, `idleSit.xml:4/6-10/11-26`, `idle2.xml:18-21`; Test-Mod `NCBear_Sit.xml:8-13` (Prioritaet 10).
- **Vanilla-Lua am Tier:** `ISPetAnimal.lua:17/36/43/48/49/55/62` (einzige Vanilla-Stellen fuer `idleAction`, grep), `ISAnimalContextMenu.lua:383`
  (`isAnimalSitting`, einzige Stelle), `ButcheringUtil.lua:570` (`getData():getSize()`), `:574` (`setDir`), `:575-576` (`setX/setY`), `:577` (`setZ`),
  `ISHutchGrabAnimal.lua:31` (in `perform()`), `ISPickupAnimal.lua:23`, `DebugContextMenu.lua:616-620`, `ISAnimalUI.lua:65`.
- **Vanilla sonst:** `ISGetOnBedAction.lua:167` (`faceLocationF` am Spieler), `ISMenuContextWorld.lua:41`, `ISSleepingUI.lua:92`, `ISBaseIcon.lua:256`,
  `TensionUI.lua:11-12`, `ISUIElement.lua:1260`, `ISAddNonPvpZoneUI.lua:4`, `FishingManager.lua:41`, `FishingHandler.lua:6`, `ISSearchManager.lua:1462`
  und `:501-503`, `ISWorldObjectContextMenu.lua:2199/2624/2642/2973-2975`, `ISInventoryPaneContextMenu.lua:4420-4436`, `ISExtendedPlacementUI.lua:30-34,
  160, 429-454`, `ISDropWorldItemAction.lua:81-87`, `STrapGlobalObject.lua:535`, `recipes_carpentry.txt:296-317`, Gegenstaende `Plank`, `Nails`,
  `HayTuft`, `Sheet`, `Leather_Crude_Large`; Tonskripte `sounds_player_voice_male.txt:303`, `sounds_ambience.txt:301`.
- **Bandits:** `ZAAim.lua:12`, `ZAPush.lua:37`, `BanditServerZombie.lua:15`, `zs_sounds.txt:531-541`, `BanditUpdate.lua:2348-2353`, `ZPCamper.lua:17ff.`
- **NPC Crew (alles "NPC Crew macht X" am Code):** `BanditsNPCRoutine.lua:223-248/:743-759`, `BanditsNPCNeeds.lua:34/:386-387/:427-484`,
  `BanditsNPCPrograms.lua:4310-4319/:5044-5047/:5098-5101`, `BanditsNPCGuardian.lua:4056-4062`, `BanditsNPCBeaconRegistry.lua:21-52`,
  `BanditsNPCSiteRules.lua:100/:110/:549/:926-929`, `BanditsNPCNav.lua:255-277`, `BanditsNPCBase.lua:201-204/:1603-1619`,
  `BanditsNPCPersistence.lua:10413-10417`, `BanditsNPCLivestockAnimalOps.lua:1060/:1077/:1093-1114` (bestaetigt den Tierpaket-Weg fuer
  `idleAction` selbst), `BanditsNPCLivestockCoop.lua:917`, `NameTags.lua:209-210/:516/:1022/:1035/:1058/:1165-1168`, `UIStyle.lua:15-18`,
  `ClientCfg.lua:139/:145`, `UI.json:2929` (`UI_BN_Rt_fatigue_at`), `Translate/EN` nur Sandbox/Tooltip/UI, `NPCCrew/CLAUDE.md:2448-2455`. Kein z Z z.
- **Test-Mod:** `NCBearDefs.lua:48-57/:86/:88/:93/:96`, `NCBearFight.lua:4-5/:47-58/:86/:197/:227-229/:376/:428/:533/:707-718/:855/:1349/
  :1458-1498/:1536-1668/:1756/:1784-1787`, `NCBearTest.lua:44-60/:81`; `NCBear.glb`: 15 Clips (keiner der Liege-Clips), 26 Gelenke.
- **Jar (Dumps dieses Laufs):** `NetworkPlayerAI.set` Off. 224-253 / `parse` Off. 709-737, `BaseAnimalBehavior.clearIdleAction` Off. 0-42,
  `IsoAnimal.isAnimalSitting` Off. 0-13, `IsoAnimal.eatFromLured` Off. 20-27, `AnimationPlayer.play` Off. 97-152 (Clip nur im eigenen Modell),
  `Core.DoPushIsoStuff` Off. 380 (2,44949) und 413-422 (Massstab 1,5), `IsoAnimal.playBreedSound` Off. 40-61 (laeuft ein Ton hoeherer
  Prioritaet, kommt nichts), `GameSoundClip.<init>` (`distanceMin` 10), `IsoPlayer.updateLOS` Off. 279-337/648-650; `IsoAnimal extends IsoPlayer`
  ohne eigene `faceLocationF`, `setDir`, `setX`, `setY`, `setZ`, `getForwardDirection`.
- **Lizenzen (neu gelesen):** #1 NPGallery gemeinfrei, WAV 5,3 MB/31 s; #2/#3 Yle CC BY 4.0, 86,9 / 38,4 MB; #4 Nivatius CC0 (beide Seiten),
  aus NPS-Material; #5 Commons gemeinfrei (US-Bundeswerk), 1.569.578 Byte, 65 s; #6 selsel CC0, 14,1 MB; #8 Acoustic Atlas
  **CC BY-NC 4.0** (Jerrett, 1:05, 254 KB) -- richtig "verboten"; earth.fm ohne Lizenz, ohne Download; Freesound-FAQ: Laden nur mit Konto.
- **Kollisionsprobe neu:** `BanditsNPCBear`, `BanditsNPC.Bear`, `UI_BN_Bear_`, `BearOverlay`, `BearBed`, `BearSleep`, `Tooltip_BN_Bear` --
  0 Treffer in NPC Crew 42/common, Vanilla lua/scripts, Bandits 42.21/common, NCBearTest. `module NPCCrew` gibt es (`tc_handitems.txt:1`).
- **Bettrechnung:** 1 Kachel = 1 / (0,544 x 1,5) = 1,2255 m (Massstab 1,5 aus dem Jar, 0,544 E/m ist die Projekt-Festlegung MaleBody =
  1,8 m). Sphinx 1,905 x 1,112 m x 1,35 = 2,572 x 1,501 m = 2,10 x 1,23 Kacheln. Bett 2,5 x 1,6 Kacheln = 3,06 x 1,96 m, innen 2,34 x 1,44 =
  2,87 x 1,76 m (>= 2,8 x 1,65 aus referenz 5). Luft quer (1,764 - 1,501) / 2 = 13 cm, laengs mit Pose L (2,866 - 2,52) / 2 = 17 cm, mit Kopf
  gerade 15 cm. Bei 1,5 Kacheln Breite nur 7 cm. Alles stimmt.
- **Kevins Regeln:** Testbefehle nur in `NCBearBench*.lua`; Bett nur ueber Rezept; Namen nach NPC-Crew-Form; beide Laeufe 9 Agenten (<= 10);
  Kampf hat Vorrang (Aufschrecken, kein Sprung Liegen -> Angriff), Passiv und Jungtier beruecksichtigt; Bau erst nach baer-fell.

### 9.2 Falsch oder zu schoen -- korrigiert
1. **Abschnitt 0, Mehrspieler:** "sehen alle den schlafenden Baeren ohne Zusatzaufwand" verschwieg, dass das Gehirn heute nur im SP
   laeuft (`NCBearFight.lua:4-5`). Jetzt ehrlich: MP offen, ungespielt.
2. **`getForwardDirection()` am Tier** stand als belegt da ("IsoAnimal erbt"). Belegt ist sie nur am Zombie/Spieler (Bandits `ZAPush.lua:37`,
   Vanilla `ISBaseIcon.lua:216`, `FishingRod.lua:286`), an keinem Tier. Jetzt "nur Jar, Kevins Wort" (neue Frage **K21**) mit Rueckfall.
3. **z Z z-Hoehe:** Vorgabe 0,40 E war geschaetzt, obwohl die Probe-Sphinx schon gemessen war (Kopf 0,45-0,50 m = ~0,26 E). Die alte Zahl
   haette die Saeule beim Erwachsenen rund 20 px zu hoch gesetzt. Jetzt 0,26 E (2.2).
4. **`getVariableString("idleAction")` am Tier:** in Vanilla nur am Spieler belegt (`ISWorldObjectContextMenu.lua:2624`), am Tier nur in NPC Crew
   und der Test-Mod. Fuer den Schlaf ersetzt durch `isAnimalSitting()`, das Vanilla am Tier ruft (1.3 Punkt 6, Tabelle).
5. **`ISWeatherChannel.lua:89`** ist `_gametime:getHour()`, kein `getGameTime():getHour()`. Beleg ersetzt; `getWorldAgeHours` (Schlafuhr)
   mit Beleg `SFarmingSystem.lua:258` nachgetragen.
6. **Ton #7 (Commons "Grizzly bear sound effect")** stand bei "Lizenz erlaubt Mod?" auf "ja". Die Seite zeigt: "Own work" vom Konto Zagzav12
   ohne Benutzerseite, hochgeladen 04.11.2026, Datum "2012", keine Aufnahmeangaben. CC0 ist nur behauptet, Herkunft unklar -> "nein".
7. **Raster "2 x 3 Kacheln"** galt ohne Bedingung. Das stimmt nur bei passender Lage (bett 1.3), sonst 3 x 3 oder mehr. Berichtigt (4.1, K11).
8. **Rezept:** "Zahlen bett 3.1" haette die Zeile `item 2 [Base.Sheet;Base.Leather_Crude_Large]` uebernommen, die 2 grosse Leder verlangt.
   Richtige Vanilla-Form `item 1 [Base.Leather_Crude_Large;2:Base.Sheet]` nachgetragen (`recipes_tailoring_leatherAndHide.txt:1271`).
9. **NPC Crew, Wache:** "Folgen und Wache: dort steigt die Muedigkeit nicht" ist falsch fuer die Wache. `Needs.lua:478` nimmt nur
   `NPCCompanion`/`NPCCorpse`/`NPCLoot` aus; auf Wache steigt sie, nur das Nachtfenster greift nicht (`Routine.lua:243`). Berichtigt (5.1).
10. **Sphinx "erreichbar":** der Hinterfuss braucht 4 Klemmungen ("pfote"/"schwenk", `referenz/umriss2.json`). Nachgetragen (1.1).
11. **"KOPF BLEIBT SO"** (`ENTSCHEIDUNGEN.md:85`) fehlte, obwohl die Clip-Runde die Gewichte neu rechnet. Nachgetragen: Kopf-/Krallengewichte bleiben fest
    (`KOPF_FEST`, `spiel/baer_gewichte_fell.py:43-66`), Kopf-Pruefung wie in baer-fell (1.4, Agent 6).
12. **Bett-Endmass** wurde nur ueber die Schlafschleife gemessen. Hinlegen, Aufwachen und Aufschrecken kommen dazu, weil die Pranken dabei auf dem Bett treten (4.1).
13. **Wecken durch fremde `idleAction`-Werte** ("eat" beim Locken, Jar `eatFromLured` Off. 20-27) fehlte in der Weck-Tabelle. Nachgetragen (5.2).
14. Hinweis nachgetragen: Die Cheat-Pruefung trifft auch "debug"/"bench"/"test..." in Strings und Bezeichnern (2.3). Dazu zwei Risiken:
    ISPetAnimal laeuft vielleicht auch auf dem Server (8.9), und ob die Kachel bei `setX/setY` nachgezogen wird, ist offen (4.6).

Kleinkram, nicht geaendert: `F.ACTS` reicht bis `:58` (zitiert `:47-56`, Inhalt stimmt). Beim z Z z wandert ein Buchstabe am Ende seines Lebens
rund 20 px nach rechts (voll sichtbar bis ~12 px, verblassend bis ~18-20 px, `zz/zz_kurve_ausgabe.txt`), nicht nur "12 px".

### 9.3 Bleibt ungeprueft
- Alles zur Laufzeit: Uebergaenge Vanilla-Schleife -> eigener Aufschreck-Knoten, die 0,5-s-Pause vor "sit", Erstarren bei fehlendem Clip,
  Bild im MP-Client, Atem-Hub aus der Spielkamera, Verdecken des Bettmodells an Waenden, Grenzen von "Place item on ground" bei 2,5 Kacheln.
- Ob `faceLocationF`/`getForwardDirection` am Tier wirken bzw. zum Modellblick passen (K19/K21); ob `setX/setY` am freien Tier die Kachel nachzieht.
- MP: ob ISPetAnimal auf dem Server laeuft, ob der Server den Bettschlaf eines Spielers sieht, ob `playBreedSound` auf einem MP-Client
  hoerbar ist, ob der Server die Kacheln um ein Bett geladen hat. Die Takte 800/1000 ms (`javap -constants`) nicht neu gelesen.
- Ob Pose L den Kopf tiefer legt als die Probe (z Z z-Anker) und ob 13-17 cm Luft nach dem Beheben der Bodendurchdringung (Ellbogen 5,2 cm,
  Hinterfuss 3,9 cm) bleiben -- erst mit dem echten Clip messbar.
- Inhalt der Tonkandidaten (nichts angehoert, nichts geladen).

Statisch geprueft, nicht gespielt.

## Nachtrag 12.11.2026: Foto-Vorlagen und alle Baeren
Kevin hat 5 Fotos schlafender Braunbaeren ausgewaehlt gesehen (Liste in `ENTSCHEIDUNGEN.md` unten, Nr. 6 = Hauptvorlage). Die Schlaf-Pose gilt fuer Junges UND grossen Baeren (Kevin: "fuer unsere baeren ... baby und ganz gross"): Entwurf am grossen Baeren, Uebertrag auf das Junge wie beim Sitzen (baer_sitz_jfuss.py, IK). Pfoten liegen frei, nie ineinander (Kevin zur Tot-Pose 12.11.).
Dazu Kevins eigenes Bild `kevin_schlafen_vorlage_1112.png` (12.11. ~07:55, "das bild find ich auch noch gut dafuer"): eingerollt auf der Seite, Kopf am Boden, Beine angezogen, Pfoten frei -- Vorrang als Vorlage; als zweite Haltung "eingerollt" (Tiefschlaf) neben der Sphinx vorschlagen, klar unterscheidbar von der Tot-Pose.
Kevin 12.11. ~08:00 zum z Z z: "in einer farbe ;D die gut dafuer ist" -> Farbe aus Abschnitt 2 (fast weiss) ersetzen durch eine Schlaf-Farbe, Vorschlag sanftes Hellblau (~0,70 0,85 1,00) mit dunklem Schatten; im Plan als Bild neben Weiss zeigen, Kevin waehlt.
