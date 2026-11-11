# Naehte: was der Baer (B1a: Junges finden und zaehmen; B1b: Folgen, Namensschild, Umbenennen, Futter hinhalten, Waisen) in NPC Crew und Vanilla beruehrt

Stand 11.11.2026 (B1b, Lauf baer-b1b), NPC Crew v3.14.68 (Zeilen wandern, es zaehlt die Fundstelle). **Statisch geprueft, nicht gespielt.**
B1b bringt **keine neue Naht in eine NPC-Crew-Datei**: nur 2 neue eigene Lua-Dateien (`server/BanditsNPCBearFollow.lua`,
`client/ISUI/BanditsNPCBearNameBox.lua`), 20 neue Texte je Sprache, 1 neue Sandbox-Option. Geaendert/neu: Zeilen 4, 5, 6, 7, 11, 13, 14, 15, 16, 17.
Gegenstueck zu `turret/NAEHTE.md`. Gelesen und geprueft von `baer/tools/baer_uebernahme.py`.

**Regel (Werkstatt-CLAUDE.md 0, Plan `_arbeit/baer_zaehmen/PLAN_ZAEHMEN.md` 12.2):** Alles, was NPC Crew beruehrt, steht zur
Laufzeit in `shared/BanditsNPCBearCrew.lua`, in `Events.OnGameBoot`, hinter einem Existenz-Riegel, genau einmal (`installed`).
**Keine NPC-Crew-Lua-Datei wird geaendert; es gibt keine einzige Naht-Zeile.** Das Uebernahme-Skript aendert in NPC Crew nur zwei Arten
von Dateien, beide nur durch Hinzufuegen: die sieben `Translate/<L>/UI.json` und `Sandbox.json` (sortiert zusammengefuehrt,
Round-Trip) und `42/media/sandbox-options.txt` (Optionen angehaengt). `IG_UI.json` hat NPC Crew nicht: sie wird in sieben Sprachen neu
angelegt. Mit und ohne NPC Crew und Bandits laeuft alles (Attrappe `_arbeit/baer_zaehmen/attrappe/gesamt/run.lua`, Abschnitte 1 und 14).

**Warum OnGameBoot:** NPC Crew setzt seine Tabellen auf Dateiebene. Nach der Uebernahme laden `BanditsNPCBear*.lua` alphabetisch VOR
`BanditsNPCLivestock*.lua` (Lua laedt je Ordner alphabetisch); ein Eintrag auf Dateiebene ginge verloren, weil
`Lv.NOT_TENDED = { ... }` (NC `shared/BanditsNPCLivestock.lua:5152`) die Tabelle neu anlegt. In der Test-Mod gilt dasselbe ueber die
Mod-Reihenfolge.

---

## Tabelle

| # | Stelle | Fundstelle | Wie (Datei des Baeren) | ab |
|---|---|---|---|---|
| 1 | NPC Crews Tierpflege zaehlt jedes Tier einer Gruppe, die nicht in `Lv.NOT_TENDED` steht, als Vieh (zaehlen, Schlachtplan) | NC `shared/BanditsNPCLivestock.lua:5152` (Literal auf Dateiebene `{ rabbit, mouse, rat, raccoon, deer }`); Leser zur Laufzeit u. a. `server/BanditsNPCLivestockHerdServer.lua:515` -- `grep -rn NOT_TENDED 42/media/lua` am 10.11.: 24 Treffer in 9 Dateien, davon 14 Code-Zeilen in 8 Dateien (Rest Kommentare) | `shared/BanditsNPCBearCrew.lua`: in `OnGameBoot`, Riegel `BanditsNPC.Livestock` da und `type(NOT_TENDED) == "table"` (fehlt das Feld bei vorhandenem NPC Crew: `B.Err`, laut), dann `NOT_TENDED["ncbear"] = true` und `NOT_TENDED["bear"] = true` (alte Gruppe des Erwachsenen bis B5a) | B1a |
| 2 | NPC Crew setzt `fleeZombies = false` fuer jede nicht wilde Tierart | NC `shared/BanditsNPCAnimals.lua:50-89` | kein Aufsatz: `shared/BanditsNPCBearDefs.lua` setzt denselben Wert selbst (`fleeZombies = false`, `wild = false`) | B1a |
| 3 | Portrait und Vanillas "Animal info" lesen `AnimalAvatarDefinition[Art]` (ohne Eintrag wirft Vanilla) | NC `client/BanditsNPCPortrait.lua:324`, `:364`; Vanilla `client/ISUI/Animal/ISAnimalUI.lua:31` | `BanditsNPCBearDefs.lua`: `AnimalAvatarDefinition["ncbearcub"]` mit den Werten von `buck`, nur wenn es die Tabelle und `buck` gibt | B1a |
| 4 | Sandbox-Seite `BanditsNPC` ("NPC Crew") | NC `42/media/sandbox-options.txt` (42 Optionen am 10.11.), `Translate/<L>/Sandbox.json` (`Sandbox_BanditsNPC` = "NPC Crew") | Skript haengt die 20 `option BanditsNPC.Bear*`-Bloecke an (B1b: + `BearFollowMaxDistance`, integer 10..60, Vorgabe 40; Name in NPC Crew frei, Skript bricht sonst ab) (Abbruch bei vorhandenem Namen, nur C-Kommentare, `VERSION` nicht doppelt); `Sandbox_BanditsNPC` gleicher Wert = keine Kollision. Lesen: `B.Opt` nimmt NPC Crews `BanditsNPC.Opt(name, default)` (NC `shared/BanditsNPC.lua:6101`, Weltregel-Speicher geht vor), sonst `SandboxVars.BanditsNPC` | B1a, B1b |
| 5 | Texte `UI.json` (`UI_BN_Bear_*`, 94 je Sprache; B1b: +20 und `Note_Tamed` neu), `Sandbox.json` (46 je Sprache, 45 neu), `IG_UI.json` (3: `IGUI_AnimalType_ncbearcub`, `IGUI_Animal_Group_ncbear`, `IGUI_Breed_brown`) | NC `42/media/lua/shared/Translate/<L>/` (UI.json 3801, Sandbox.json 92 Schluessel am 11.11., beide sortiert, Round-Trip ok) | sortiert einfuegen; Namensraum je Datei; `UI_BN_Bear_` MIT Unterstrich (`UI_BN_Beard_None` ist NPC Crews); Vanilla kennt keinen der drei Tiernamen (Skript prueft gegen Vanilla-EN); B1b: kein `<`/`>` in einem UI-Text (Tooltips sind Rich-Text, Skript prueft) | B1a, B1b |
| 6 | Vanillas Tier-Menue | Vanilla `client/ISUI/Animal/ISAnimalContextMenu.lua:1235` (Ereignis `OnClickedAnimalForContext`), `:307-324` ("Kill" je nicht wildem Tier) | `client/BanditsNPCBearMenu.lua`: eigener Empfaenger am selben Ereignis; am Jungen (Art `ncbearcub`) Fuettern/Streicheln anhaengen und Vanillas "Kill" im Untermenue des Jungen entfernen (`removeOptionByName`, reines Lua `client/ISUI/ISContextMenu.lua:1016`) -- Menue-Hygiene, kein Schutz. **B1b:** am eigenen gezaehmten Jungen (nur Besitzer, nur mit Sicht-Eintrag) der Umschalter "Follow me"/"Stay here" und "Name the cub" -- echte Spielmechanik, Texte ueber Schluessel; das Eingabefenster ist Vanillas `ISTextBox` (`client/ISUI/ISTextBox.lua:280`, wie Vanillas Tier-Umbenennen `client/ISUI/Animal/ISAnimalUI.lua:459-485`), eigene Datei `client/ISUI/BanditsNPCBearNameBox.lua` | B1a, B1b |
| 7 | Vanillas Welt-Menue | Vanilla `client/ISUI/Hutch/ISHutchMenu.lua:115` (`OnFillWorldObjectContextMenu`) | `BanditsNPCBearMenu.lua`: "Baeren-Koeder auslegen" / "Koederplatz aufgeben" -- echte Spielmechanik (verbraucht Honig/Fisch), kein Testmenue. **B1b:** "Hold out food for the cub" (nur, wenn ein passendes Junges in 15 Kacheln steht): nimmt das Stueck nur in die Hand, `ISWorldObjectContextMenu.equip(p, Hand, Futter, true, false)` wie Vanilla `ISAnimalContextMenu.lua:93`; kein Gegenstand erzeugt oder verbraucht. Vanillas Locken (`ContextMenu_Lure`, `eatFromLured`) wird NICHT benutzt | B1a, B1b |
| 8 | Vanilla-Tabellen `AnimalDefinitions.animals`, `AnimalAvatarDefinition`, `AnimalPartsDefinitions.animals` | Vanilla `shared/Definitions/animal/DeerDefinitions.lua:1`, `:56`; `AnimalPartsDefinitions.lua:456`; `ButcheringUtil.lua:18` | nur NEUE Schluessel (`ncbearcub`, `ncbearcubbrown`), auf Dateiebene (Java liest `AnimalDefinitions` erst in `IsoWorld.init`); globale Zuweisung nur `AnimalDefinitions = AnimalDefinitions or {}` | B1a |
| 9 | Animset `buck` (Vanilla-Gruppe), Knoten `42/media/AnimSets/buck/idle/NCBear_Eat.xml` | Vanilla `media/AnimSets/buck/` (22 Knoten, 15 Clip-Namen); der Knoten hat genau eine Bedingung `NCBearAct` (STRING) | kopiert wird NUR `NCBear_Eat.xml` (Fress-Clip, `B.ACT = "eat"`); die 9 Knoten des Erwachsenen (Bite, Maul, Rear, Sit, SitDown, Slam, StandUp, SwipeL, SwipeR) bleiben bis B5a in der Test-Mod (Nachbesserung A10); der Clip liegt im GLB des Jungen (Skript prueft); 10 Vanilla-buck-Clips fehlen im GLB wie beim gespielten Erwachsenen (Warnung) | B1a |
| 10 | Modell und Textur in `module Base` | `42/media/scripts/nc_bear_cub.txt` (`animationsMesh NCBearCub`, `model NCBearCub_Body`, mesh `Skinned/NCBearCub.glb`), `textures/Body/NCBearCub.png` | Namen gegen Vanilla- und NC-Skripte geprueft (0 Treffer); `bodyModel` ohne Punkt sucht in `Base` (Werkstatt-CLAUDE.md 7 Zweihaender-Lehre); das endgueltige Modell aus `baer-junges` ersetzt den Platzhalter unter demselben Namen | B1a |
| 11 | Register `TrueCompanionsBears` (globale ModData) und Befehlsmodul `BanditsNPCBear` | eigener Name; NC nennt beides nicht (Skript: 9 Muster, 0 Code-Treffer) | nur beim Schreiber, nie uebertragen; Befehle Hello/BaitDrop (Client -> Server), Sync/Note (Server -> Client). **B1b:** + Mode `{ id, mode }` und Rename `{ id, name }` (Client -> Server; der Server prueft Besitz, Zustand, Fahrzeug, Abstand, Name; Drossel 500 ms je Spieler, Tabelle gedeckelt 64); Register-Felder `mode`/`name`, Sicht-Felder `mode`/`name` | B1a, B1b |
| 12 | Koeder gegen Foersterin/Pluenderer | NC Pluenderer (`SR.LootTypeRefused`, Turret-Naht #39) | **entfaellt**: der Koederplatz ist unsichtbar, kein Bodengegenstand (Plan 0.4) | - |
| 13 | NPC-Crew-Figuren | NC Bandits-Figuren (IsoZombie) | **entfaellt in B1a/B1b**: Zombies greifen Tiere nie an, Bandits zielt nie auf Tiere (Werkstatt-CLAUDE.md 8); das Junge greift niemanden an (Kampf ist B5a). B1b: Folgen kennt nur den Besitzer (Spieler aus `B.Players()`), nie eine NPC-Crew-Figur; Befehle an Crew-Figuren sind nicht in B1b | - |
| 14 | Namensschild (B1b); Taste V / Baeren-Fenster, Lebensbalken (spaeter) | NC `client/ISUI/BanditsNPCNameTags.lua` (NPC Crews Schilder; `grep -c "IsoAnimal\|getAnimalType\|isAnimal"` am 11.11.: 0 -- zeichnet keine Tiere) | **B1b: keine Naht.** Eigenes 1 x 1-Panel `client/ISUI/BanditsNPCBearHud.lua` (wie der B1a-Balken), nur Junge aus der eigenen Sicht, Anker `B.CFG.tagZ`. Taste V/Fenster **spaeter**: eine Taste waere ein `Events.OnKeyPressed` -- das Skript meldet das heute als Cheat-Fund (Regel `taste`); mit dem Fenster kommt dann eine einzelne, begruendete Ausnahme hierher | B1b, spaeter |
| 15 | Wachsen zum Erwachsenen (`nextStage`, Datenweitergabe) | - | **spaeter** (nach B1b); vorbereitet: die Wahrheit steht im Register (`kind`, `aid`, B1b auch `mode`/`name`), nicht nur am Tier | spaeter |
| 16 | Tiername in Vanilla ("Animal info", Untermenue-Titel), Vanillas Befehl `animal.rename` | Vanilla `client/ISUI/Animal/ISAnimalUI.lua:459-485` (Umbenennen ueber `setCustomName`); NPC Crew setzt keinen Tiernamen (`setCustomName` dort nur an Gegenstaenden, NC `shared/BanditsNPCLivestockButcher.lua:1760` `item:setCustomName(true)`) | **keine Naht, bekannte Grenze** (PLAN_B1B.md 0.3): der Name lebt nur im Register, kein `setCustomName`/`getCustomName`; Vanillas Tier-Info zeigt weiter "Bear cub", unser Schild den echten Namen | B1b |
| 17 | Waisen raeumen (N5) | eigene Art `ncbearcub` in Vanillas Objektliste (`getCell():getObjectListForLua()`, wie B1a) | `B.ScanAnimals` entfernt NUR ein `ncbearcub` ohne Spiegel und ohne passenden Eintrag, unbeobachtet (25 Kacheln, SP: nicht sichtbar), nach 30 s, ueber `B.RemoveCub` (im MP mit `removeAnimal(OnlineID)`); nie den Erwachsenen `bear`, nie NPC Crews Vieh oder andere Tiere (Art-Frage). Im MP am Server unbelegt wie B1a (A3) -- MP-Testpunkt | B1b |

## Die Zeilen

Keine. Der Baer setzt in B1a und B1b keine Zeile in eine NPC-Crew-Datei.

## Laufzeit-Aufsaetze (alle in `Events.OnGameBoot`)

| Datei | Was | Riegel | genau einmal |
|---|---|---|---|
| `shared/BanditsNPCBearCrew.lua` | `BanditsNPC.Livestock.NOT_TENDED["ncbear"/"bear"] = true` (Naht 1) | `BanditsNPC.Livestock ~= nil`, `type(NOT_TENDED) == "table"` | `installed` |

Alles andere haengt an Vanilla-Ereignissen (`OnClickedAnimalForContext`, `OnFillWorldObjectContextMenu`, `OnServerCommand`,
`OnClientCommand`, `OnGameStart`, `OnTick`, `EveryTenMinutes`, `OnInitGlobalModData`) und beruehrt NPC Crew nicht. Zur Laufzeit (nie
auf Dateiebene) gelesen werden: `BanditsNPC.Opt`, `BanditsNPC.Err`, `BanditsNPC.DIAG`, `BanditsNPC.Livestock` -- jeweils hinter
Existenz-Riegel (NC `shared/BanditsNPC.lua:6101`, `:187`, `:95`).

## Erlaubte Fundstellen des Trockenlaufs (bis B5a absichtlich rot)

Der Trockenlauf ohne `--vor-b5a` ist **absichtlich rot mit genau 24 Fehlern**: die alten, noch nicht umbenannten Teile der Test-Mod.
Kevin: Umbenennen der alten Dateien `NCBear*` und der Art `bear` zu Beginn von B5a. Sie werden NIE kopiert; das Skript fuehrt sie in
`ALT_EXPECTED`. Eine neue, nicht gelistete Altlast ist immer ein Fehler, auch mit `--vor-b5a`. `--echt` verbietet `--vor-b5a`: bis
B5a ist die echte Uebernahme deshalb gesperrt.

| # | Altlast | Grund / was B5a tut |
|---|---|---|
| 1 | `42/media/lua/shared/NCBearDefs.lua` | Art `bear` des Erwachsenen: umbenennen nach `BanditsNPCBear*`, Art/Gruppe entscheiden |
| 2 | `42/media/lua/shared/NCBearFight.lua` | Kampf des Erwachsenen (SP) |
| 3 | `42/media/lua/client/NCBearAttackProbe.lua` | Angriffs-Sonde: streichen oder nach `NCBearBench*` |
| 4 | `42/media/lua/client/NCBearSize.lua` | Groessen-Testhilfe: nach `NCBearBench*` oder streichen |
| 5 | `42/media/lua/client/NCBearSpawn.lua` | Spawn-Testhilfe des Erwachsenen: nach `NCBearBench*` |
| 6 | `42/media/lua/client/NCBearTest.lua` | Testbefehle `NCBear_Sit/Stand/Eat`: nach `NCBearBench*` |
| 7 | `42/media/models_X/Skinned/NCBear.glb` | Modell des Erwachsenen (geht mit der Art) |
| 8 | `42/media/models_X/Skinned/NCBearDeer.glb` | Test-Modell `bearstag`: streichen |
| 9 | `42/media/models_X/WorldItems/NCBear.fbx` | Test-Gegenstand: streichen |
| 10 | `42/media/textures/Body/NCBear.png` | Textur des Erwachsenen |
| 11 | `42/media/textures/Item_NCBear.png` | Icon des Test-Gegenstands: streichen |
| 12 | `42/media/textures/WorldItems/NCBear.png` | Textur des Test-Gegenstands: streichen |
| 13 | `42/media/scripts/nc_bear.txt` | `module NCBear`, Gegenstand `BearStatic` "Test Bear (model)", `DisplayCategory = Junk`: streichen |
| 14 | `42/media/scripts/nc_bear_tier.txt` | `NCBear_Body`, `NCBearStag_Body` des Erwachsenen |
| 15 | `42/media/scripts/nc_bear_sounds.txt` | Toene des Erwachsenen (mit dem Kampf) |
| 16-21 | `42/media/sound/NCBear_Growl1/2/3.wav`, `NCBear_Huff.wav`, `NCBear_Pain.wav`, `NCBear_Roar.wav` | Toene des Erwachsenen |
| 22 | EN `IG_UI.json` `IGUI_AnimalType_bear` ("Brown bear (test)") | Tiername der Test-Art |
| 23 | EN `IG_UI.json` `IGUI_AnimalType_bearstag` | streichen |
| 24 | EN `IG_UI.json` `IGUI_Animal_Group_bear` ("Bear (NC test)") | Gruppenname der Test-Gruppe |

**Nie kopiert (Testhilfe):** `client/NCBearBench.lua`, `client/NCBearBenchCub.lua` -- jede Datei mit Basisnamen `NCBearBench*`, gleich
welche Endung und welcher Ordner. Dazu `mod.info`, `42/mod.info`, `.git`, `.gitattributes`.

**Kopiert wird von den Animations-Knoten nur `NCBear_Eat.xml`** (alter Name, ohne Test-Inhalt; das Junge braucht ihn). Die 9 Knoten
des Erwachsenen ueberspringt das Skript bis B5a (Kampf-Knoten gehoeren nicht vor dem Kampf nach NPC Crew). Benennt B5a die Knoten um,
muss `B.ACT`/`NCBearAct` mitziehen.

## Cheat-Ausnahmen und erlaubte Treffer

| Datei | Regel | Code | Grund |
|---|---|---|---|
| `shared/BanditsNPCBearDefs.lua` | `befehl` (`NC<Name>_*`) | `bodyModel = "NCBearCub_Body"` | Name des model-Skripts, kein Befehl (Plan 12.1 Punkt 5) |
| alle | `global` | `BanditsNPC = BanditsNPC or {}` | Modultabelle wie NPC Crew |
| `shared/BanditsNPCBearDefs.lua` | `global` | `AnimalDefinitions = AnimalDefinitions or {}` | Vanillas Tabelle (DeerDefinitions.lua:1), nur diese Form |
| `shared/TimedActions/BanditsNPCBear{Feed,Pet,Bait}Action.lua` | `global` | `X = ISBaseTimedAction:derive("X")` | die Engine baut Netz-Aktionen ueber den globalen Klassennamen (Vanilla ISFeedAnimalFromHand.lua:3) |
| `client/BanditsNPCBearMenu.lua` | luacheck_pz W113 | die drei Aktionsklassen | luacheck_pz liest je Datei; die Klassen setzt die eigene Datei unter `shared/TimedActions/` |
| NC `shared/BanditsNPC.lua:1357` (11.11., v3.14.68) | Kollision (Kommentar) | `NCBear` im Changelog v3.14.58 | nur Kommentar: Warnung, keine Kollision |

**Tier-Regel (Plan 12.1 Punkt 7), vom Skript erzwungen:** `addAnimal(` und `:addToWorld(` nur in `B.CreateCub`
(`server/BanditsNPCBearWorld.lua`); `B.CreateCub(` nur aus `B.AppearFor`; `B.AppearFor(` nur aus `forestRolls` und `baitAppear`
(`server/BanditsNPCBearServer.lua`); `:remove()` am Tier und `removeAnimal(` (Server, Vanilla `ButcheringUtil.lua:612-614`) nur in
`B.RemoveCub`. Die Bench ruft `B.AppearFor` auch -- sie wird nie kopiert.

**B1b, vom Skript erzwungen:** Regel `force` -- `B.ScanAnimals(..., force)` (Waisen ohne die 30-s-Frist entfernen) gibt es nur in der
Werkbank (`NCBear_CubSweep`); im kopierten Code ist jeder Aufruf mit zweitem Argument ein Cheat-Fund. Die neuen Testbefehle
`NCBear_CubFollow/_CubName/_CubFollowTest/_CubOrphan/_CubSweep` und die Waise aus dem Nichts (`NCBear_CubOrphan` ruft `B.CreateCub`
ohne Eintrag) stehen nur in `client/NCBearBenchCub.lua` (Regeln `befehl`, Tier-Regel `CreateCub`). Gegenprobe 11.11. (verdorbene
Kopie: `B.ScanAnimals(players, true)` im Hirn-Takt, `<staying>` in EN/UI.json): 4 Fehler, wie erwartet.
Nachbesserung B1b A5 (11.11.): die Regel `force` ist keine Zeilen-Regex mehr, sondern `scan_force_hits` (zerlegt jede Erwaehnung von
`ScanAnimals` im Code-Teil der ganzen Datei): Fund ist jedes zweite Argument in jeder Form (auch `B.ScanAnimals(B.Players(), true)`,
`not false`, ueber mehrere Zeilen, `B:ScanAnimals(p)`) und `ScanAnimals` ohne Aufruf-Klammer (`local scan = B.ScanAnimals`,
`B["ScanAnimals"]`). Gegenprobe `_arbeit/baer_zaehmen/attrappe/uebernahme_force/probe_force.py`: 23 Faelle, 0 Fehler; kopierte
Dateien 0 Funde, Werkbank 2.

## Abhaengigkeiten, die beim Umbenennen (B5a) mitziehen muessen

- `B.ACT = "NCBearAct"` und die 10 Knoten `AnimSets/buck/idle/NCBear_*.xml` (Bedingung `NCBearAct`; nach NPC Crew geht bis dahin nur `NCBear_Eat.xml`).
- Naht 1 traegt die alte Gruppe `bear` mit; faellt die Art `bear` in B5a weg oder wird sie zu `ncbear`, die Zeile streichen.
- Die drei alten EN-Tiernamen stehen heute nur in der Test-Mod (EN `IG_UI.json`), nie in NPC Crew.
