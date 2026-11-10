# Lauf baer-zaehmen (B1a): PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 10.11.2026. **Statisch geprueft, nicht gespielt.** Geaendert: nur diese Datei. Probe und verdorbene Kopien liegen im Scratchpad
(`.../scratchpad/pa/`), nicht unter `_arbeit/`. Gelesen: PLAN_ZAEHMEN.md ganz, bau_uebernahme.md, bau_kern.md, schnittstelle_aenderungen.md,
alle 15 Lua-Dateien des Stagings ganz, sandbox-options.txt, nc_bear_cub.txt, NCBearDefs.lua/nc_bear_tier.txt der Test-Mod, NAEHTE.md,
Kopf des Uebernahme-Skripts. bau_oberflaeche.md nur ueber die Querverweise in bau_uebernahme.md (nicht ganz gelesen).

## Ergebnis kurz

- Eiserne Regel: 199 Fundstellen-Kommentare der 15 Dateien per Skript (`scratchpad/pa/belege.py`, `liste.txt`) gegen das heutige
  Vanilla/Bandits 42.22 nachgeschlagen: **alle 199 an der genannten Datei und Zeile vorhanden** (eine scheinbare Abweichung war ein
  Regex-Treffer, Zeile stimmt). Argumentzahl/-typen von Hand gegen die Fundzeilen verglichen: passen. Die Befunde betreffen die
  **Seite** (Client/Server): A1-A4.
- Trennung: kein Testbefehl, kein `isDebugEnabled`, kein `AddItem`, keine Taste, kein `_G` in den 14 echten Dateien. Bench nur ueber
  `NCBearMenu.extra` (alte Test-Mod, nur `isSingleplayer()`, NCBearTest.lua:113) und Konsole; der echte Code braucht die Bench nie.
- Namen: 0 Treffer der eigenen Namen im Code von NPC Crew (eigenes grep: `TrueCompanionsBears|BanditsNPCBear|UI_BN_Bear_|tcBear|ncbear|
  BanditsNPC.Bear|TC-BEAR|BanditsNPC_Bear` in `NPCCrew/42/media`), 0 in Vanilla lua/scripts. Staging 40 Dateien, MD5/Groesse wie
  `staging_dateien.txt`, 39 neu, 1 ueberschreibt (EN/IG_UI.json; die 4 alten Schluessel wortgleich).
- Texte: 7 Sprachen x UI 74 / Sandbox 44 / IG_UI 3 (EN 6) Schluessel, gleiche Platzhalter, Round-Trip, sortiert, ohne BOM, LF;
  CN-Zeichen alle in Vanilla-CN; 66 Schluessel aus dem Code alle in EN (die 8 `Dir_*` werden zusammengesetzt, BanditsNPCBearClient.lua:149);
  `%%` wie Vanilla (EN ContextMenu.json:502). Sandbox: 19 Optionen, jede mit Text + Tooltip (+5 enum-Texte), jede per `B.Opt` gelesen, Bereiche = `B.OPTS`.
- Tier-Definition: alle Felder des gespielten Erwachsenen vorhanden (plus `needMom`, `feedByHandAnim`, `textureBaby`); Rasse, animset
  `buck`, Gruppe `ncbear` mit Text, Stufe ohne `nextStage`, Skript-Form wie nc_bear_tier.txt:3-15; Knoten `NCBear_Eat.xml` (Bedingung
  `NCBearAct`=`eat`) und Spieler-Knoten `petlamb.xml` (Bedingung `animal`=`lamb`) existieren.

## Zahlen (selbst gelaufen)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (15 Dateien) | 15 file(s) checked, 0 failed |
| `scopecheck.py` | 15 file(s), 0 violation(s) |
| `luacheck_pz.py` | 11 W113: 3 Aktionsklassen (BanditsNPCBearMenu.lua:81/92/102), 8 in der Bench (NCBear_Cub*, NCBearMenu) -- erwartet |
| `localcount.py` | groesste Funktion aktiv 39 (Bench :308), echte Dateien 30 (Hud :178); insgesamt deklariert hoechstens 41 (Hud :178); 0 nahe/ueber der Grenze |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` (lua5.1) | **175 bestanden, 0 Fehler** (wie ergebnis.txt) |
| Trockenlauf `--staging` | NICHT OK, **24 Fehler, 3 Warnungen** = genau die Altlasten (ALT_EXPECTED); Ausgabe gleich `trockenlauf.txt` |
| Trockenlauf `--staging --vor-b5a` | OK, 0 Fehler, 27 Warnungen |
| `--probe` (in den Scratchpad) `--vor-b5a` | OK, 0 Fehler, 27 Warnungen; 49 Dateien geschrieben; 14 Lua luacheck/scopecheck ok, localcount <= 41, luacheck_pz 0 Treffer + 3 erlaubt |
| Cheat-Gegenprobe 1 (verdorbene Kopie: globale `NCBear_CubX`, `isDebugEnabled`, `AddItem`, `addAnimal` und `B.AppearFor` im Menue, `_G`, `Capability.AnimalCheats`, `OnKeyPressed`, Menuetext "Spawn cub here", `a:remove()` ausserhalb RemoveCub, fremde `Foo.json`, Bench-Kopie `shared/NCBearBenchZ.lua`) | 16 Fehler, alles gefunden; Bench-Kopie "NICHT kopiert" |
| Cheat-Gegenprobe 2 (Werkbank-Text "Cub: appear near me", `setGhostMode`, Griff nach `NCBearMenu.extra`) | 2 von 3 gefunden; `NCBearMenu.extra` NICHT (A6) |

## Befunde

**A1 (major) -- Tier entfernen auf dem dedizierten Server ohne Vanillas Server-Schritt.** `B.RemoveCub` (server/BanditsNPCBearWorld.lua:253-258)
ruft nur `animal:remove()`. Vanilla entfernt am Server anders: `removeAnimal(tonumber(args.id))` (server/ClientCommands.lua:841) bzw.
`animal:remove()` und DANACH im `isServer()`-Zweig `removeAnimal(animal:getOnlineID())` (shared/Definitions/animal/ButcheringUtil.lua:609-614).
`animal:remove()` allein ist der SP-Zweig des Debug-Menues (client/DebugUIs/DebugContextMenu.lua:231-235 -> :616). Der Kommentar
World.lua:251 "(shared, laeuft auch auf dem Server)" verschweigt :612-614. Folge im MP (ungeprueft): Verschwinden/Aufraeumen
laesst womoeglich ein Geistertier bei den Clients stehen. SP nicht betroffen. Vorschlag: im Server-Zweig wie ButcheringUtil.lua:612-614
zusaetzlich `removeAnimal(animal:getOnlineID())` (gleiche Typen, shared-Beleg).

**A2 (major) -- Bewegungssperre waehrend Fuettern/Streicheln im MP nur an der Client-Kopie.** Feed/Pet setzen `setBlockMovement(true)`
nur in `start()` (BanditsNPCBearFeedAction.lua:56, BanditsNPCBearPetAction.lua:63). Vanilla setzt die Sperre fuer den Server in
`serverStart()` und loest sie in `serverStop()`/`complete()` (shared/TimedActions/Animals/ISMilkAnimal.lua:212, :169, :196); der Server ruft
also nicht nur `complete()` (Plan 6.2.7 / FE 8.2 "Server ruft NUR complete()" ist damit zu eng). Beim Fuettern haelt der Hirn-Takt das
Junge mit Futter in der Hand ohnehin fest (Server :599-601, Rules :287/:307); beim Streicheln nicht -> das Junge kann am Server wegwandern,
`complete()` lehnt dann mit "zu weit" ab (kein Gegenstand betroffen). Vorschlag: `serverStart`/`serverStop` wie ISMilkAnimal, Sperre in
`complete()` loesen.

**A3 (major) -- Schreiber-Aufrufe im normalen Server-Ablauf mit nur Client-/SP-Beleg (eiserne Regel "gleiche Seite").**
- `getAllAnimalsDefinitions()` / `def:getBreeds()` (World.lua:209-215, bei JEDEM Erscheinen): Beleg nur client/DebugUIs/DebugContextMenu.lua:246-275;
  in server/ und shared/ 0 Treffer. Der Server-Weg steht in Vanilla: `AnimalDefinitions.getDef(args.type):getBreedByName(args.breed)`
  (server/ClientCommands.lua:808, auch shared ButcheringUtil.lua:79/85) -- damit liesse sich `findBreed` am Server belegen.
- `getCell():getObjectListForLua()` (World.lua:289, Suchlauf nach jedem Laden): Belege nur client (DebugContextMenu.lua:612, FenrisScenario.lua:505); server/shared 0.
- `animal:getAnimalID()` (Registry.lua:153/193, World.lua:270/310/331): Beleg nur client/ISUI/Animal/ISAnimalUI.lua:53; server/shared 0.
- `item:isRotten()` / `isBurnt()` (Food.lua:58, am Server in FeedComplete/BaitComplete/Hirn-Takt): Belege nur client (ISAnimalContextMenu.lua:37, ISInventoryPane.lua:990); server/shared 0.
Plan 6.3 Ende und bau_kern.md 2 nennen einen Teil davon ehrlich als MP-Testpunkt; nach der Regel sind es trotzdem Befunde. Vorschlag:
`findBreed` auf getDef/getBreedByName umstellen; fuer die anderen Kevins Wort je Methode oder einen Server-Beleg suchen (am Server
findet Vanilla Tiere ueber `getAnimal(id)`, ClientCommands.lua:817).

**A4 (minor) -- Fundstelle von der falschen Seite, obwohl eine passende da ist.** Server-Code nennt Client-Dateien: `getModData()` am Tier
(Registry.lua:181, ISInventoryPaneContextMenu.lua:4127; Server-Beleg ButcheringUtil.lua:596/602), `getOnlineID()` (Registry.lua:397, Server
:793; Beleg ButcheringUtil.lua:614), `getAnimalType()` (Beleg ButcheringUtil.lua:13), `isExistInTheWorld()` (shared ISAddAnimalInTrailer.lua:29).
Nur Kommentare umschreiben.

**A5 (minor) -- zwei Bench-Befehle umgehen die SP-Sperre.** `NCBear_CubLog` und `NCBear_CubSet` (client/NCBearBenchCub.lua:339-366) rufen
`ready()` nicht; auf einem MP-Client aendern sie `B.LogOn`/`B.CFG` des Clients (z. B. `feedTime` -> Client-Dauer weicht vom Server ab).
Datei wird nie kopiert; Vorschlag: `B.IsSP()` vorschalten.

**A6 (minor) -- Cheat-Pruefung erkennt den Griff nach dem alten Testmenue nicht.** Eine echte Datei mit `table.insert(NCBearMenu.extra, ...)`
lief in Gegenprobe 2 durch (Regel `befehl` verlangt `NC<Name>_`). Vorschlag: `\bNCBearMenu\b` und `NCBearBench` als Bezeichner in
CHEAT_RULES (baer_uebernahme.py:154-174).

**A7 (minor) -- Zahl der NOT_TENDED-Leser widerspruechlich.** NAEHTE.md:24 "heute 14 Code-Zeilen in 9 Dateien", BanditsNPCBearCrew.lua:10 und
Plan 12.2 "24 Treffer". Eine Zahl festschreiben (mit grep-Muster).

**A8 (minor) -- Junges ohne Stimme.** Der Erwachsene hat `pain`/`death` (NCBearDefs.lua:50-51, laut Kommentar :31-32 von Engine und
falldown.xml gerufen), das Junge nur `fallover` (BanditsNPCBearDefs.lua:53-55); Vanilla gibt dem Kitz eigene Toene (DeerDefinitions.lua
`fawn_sounds` ab :213). Gewollt (Plan 6.5), ob die Engine bei fehlendem Schluessel etwas meldet: ungeprueft.

**A9 (minor) -- "Werkbank" in Kommentaren der echten Dateien** (Registry.lua:338, BanditsNPCBear.lua:31), vom Skript als Warnung gemeldet; vor `--echt` streichen.

**A10 (minor) -- Uebernahme kopiert alle 10 Knoten des Erwachsenen** (Bite, Maul, Slam, Swipe ... -- Trockenlauf "13 Dateien") nach NPC Crew,
obwohl B1a nur `NCBear_Eat.xml` braucht (Plan 12.1 Punkt 10). Harmlos (jeder Knoten nur mit `NCBearAct`), zieht aber Kampf-Knoten vor B5a mit.

Kein Befund zu: Platzhaltern, Sandbox, Kollisionen, alten Dateien, Tier-Regel, JSON, CN, Trennung im echten Code, Round-Trip, Locals.

## Tabelle der geprueften Engine-Aufrufe (Kennung = Datei des Stagings: Bear=BanditsNPCBear.lua, Crew, Defs, Food, Reg=Registry,
Srv=Server, Wld=World, FA/PA/BA=Feed/Pet/BaitAction, Cl=Client, Mn=Menu, Hud, Bn=Bench)

| Pruef-Kennung | Fundstelle (Vanilla/Bandits 42.22) | gefundene Zeile | Urteil |
|---|---|---|---|
| Bear.forestZones | shared/Foraging/forageZones.lua:3 | `name = "DeepForest",` | Datei, Zeile, Argumente passen |
| Bear.forestDeep | shared/Foraging/forageZones.lua:27 | `name = "DeepForest",` | Zeile verschoben; Zeile 27 = Forest, korrekt (Regex traf DeepForest) |
| Bear.forestOrganic | shared/Foraging/forageZones.lua:140 | `name = "OrganicForest",` | Datei, Zeile, Argumente passen |
| Bear.isClient | shared/TimedActions/ISEatFoodAction.lua:136 | `if not isClient() and not isServer() then` | Datei, Zeile, Argumente passen |
| Bear.SandboxBandits | Bandits client/BanditUpdate.lua:495 | `if SandboxVars.Bandits.General_BleedOut then` | Datei, Zeile, Argumente passen |
| Bear.getTimestampMs | server/Foraging/forageServer.lua:456 | `local now = getTimestampMs();` | Datei, Zeile, Argumente passen |
| Bear.getTextOrNull | shared/TimedActions/ISReadABook.lua:220 | `local text = getTextOrNull(mediaID.info)` | Datei, Zeile, Argumente passen |
| Bear.getText2 | shared/Definitions/animal/ButcheringUtil.lua:394 | `item:setName(getText("IGUI_AnimalMeat", getText(partDef.baseName), getText(partDef.extraNa` | Datei, Zeile, Argumente passen |
| Bear.getText4 | client/Vehicles/ISUI/ISVehicleMenu.lua:403 | `local text = getText("ContextMenu_Vehicle_AttachVehicle", aName, bName, attachNameA, attac` | Datei, Zeile, Argumente passen |
| Bear.getUsername | shared/Traps/TrapSystem.lua:45 | `modData.player = player:getUsername()` | Datei, Zeile, Argumente passen |
| Bear.worldAge | server/Traps/STrapSystem.lua:77 | `luaObject.lastUpdate = getGameTime():getWorldAgeHours() / 24;` | Datei, Zeile, Argumente passen |
| Bear.getZonesAt | shared/Traps/TrapSystem.lua:12 | `local mapZones = getWorld():getMetaGrid():getZonesAt(square:getX(), square:getY(), square:` | Datei, Zeile, Argumente passen |
| Bear.zoneType | shared/Traps/TrapSystem.lua:16 | `tempZoneType = tempZone and tempZone:getType();` | Datei, Zeile, Argumente passen |
| Bear.getAnimalType | client/ISUI/Animal/ISAnimalUI.lua:65 | `self:drawText(getText("IGUI_AnimalType_" .. self.animal:getAnimalType()), self.xOffset + 1` | Datei, Zeile, Argumente passen |
| Bear.animalModData | client/ISUI/ISInventoryPaneContextMenu.lua:4127 | `animal:getModData()["skeleton"] = "true";` | Datei, Zeile, Argumente passen; Client-Datei; Server-Beleg ButcheringUtil.lua:596 (A4) |
| Bear.getOnlineID | client/ISUI/Animal/ISAnimalContextMenu.lua:432 | `"id", animal:getOnlineID())` | Datei, Zeile, Argumente passen; Client-Datei; Server-Beleg ButcheringUtil.lua:614 (A4) |
| Bear.sendClientCommand | client/DebugUIs/DebugContextMenu.lua:956 | `sendClientCommand(playerObj, 'bbq', 'setFuel', args)` | Datei, Zeile, Argumente passen |
| Bear.sendServerCommand | server/BuildingObjects/ISBuildUtil.lua:291 | `sendServerCommand(playerObj, 'ui', 'dirtyUI', { });` | Datei, Zeile, Argumente passen |
| Crew.OnGameBoot | client/Foraging/ISSearchManager.lua:1481 | `Events.OnGameBoot.Add(ISSearchManager.initBinds);` | Datei, Zeile, Argumente passen |
| Defs.Def1 | shared/Definitions/animal/DeerDefinitions.lua:1 | `AnimalDefinitions = AnimalDefinitions or {};` | Datei, Zeile, Argumente passen |
| Defs.Def56 | shared/Definitions/animal/DeerDefinitions.lua:56 | `AnimalDefinitions.animals = AnimalDefinitions.animals or {};` | Datei, Zeile, Argumente passen |
| Defs.icons | shared/Definitions/animal/DeerDefinitions.lua:44 | `AnimalDefinitions.breeds["deer"].breeds["whitetailed"].invIconMale = "Item_DeerMale_Dead";` | Datei, Zeile, Argumente passen |
| Defs.fallover | shared/Definitions/animal/DeerDefinitions.lua:185 | `fallover = { name = "AnimalFoleyBuckBodyfall" },` | Datei, Zeile, Argumente passen |
| Defs.fawnSize | shared/Definitions/animal/DeerDefinitions.lua:65 | `AnimalDefinitions.animals["fawn"].animalSize = 0.1;` | Datei, Zeile, Argumente passen |
| Defs.shadoww | shared/Definitions/animal/DeerDefinitions.lua:68 | `AnimalDefinitions.animals["fawn"].shadoww = 0.4;` | Datei, Zeile, Argumente passen |
| Defs.feedByHand | shared/Definitions/animal/DeerDefinitions.lua:92 | `AnimalDefinitions.animals["fawn"].feedByHandAnim = "AnimalLureLow";` | Datei, Zeile, Argumente passen |
| Defs.needMom | shared/Definitions/animal/ChickenDefinitions.lua:127 | `AnimalDefinitions.animals["chick"].needMom = false; -- every baby will follow their mom, i` | Datei, Zeile, Argumente passen |
| Defs.avatar | shared/Definitions/animal/AnimalAvatarDefinition.lua:231 | `AnimalAvatarDefinition["buck"] = {};` | Datei, Zeile, Argumente passen |
| Defs.ISAnimalUI31 | client/ISUI/Animal/ISAnimalUI.lua:31 | `self.avatarPanel:setZoom(self.avatarDefinition.zoom * self.animal:getData():getSize());` | Datei, Zeile, Argumente passen |
| Defs.parts | shared/Definitions/animal/AnimalPartsDefinitions.lua:456 | `local fawnwhitetailed = AnimalPartsDefinitions.animals["fawnwhitetailed"] or {};` | Datei, Zeile, Argumente passen |
| Defs.partsKey | shared/Definitions/animal/ButcheringUtil.lua:18 | `local def = AnimalPartsDefinitions.animals[fullName];` | Datei, Zeile, Argumente passen |
| Food.fishes | shared/Fishing/fishing_properties.lua:216 | `Fishing.fishes = Fishing.fishes or {};` | Datei, Zeile, Argumente passen |
| Food.itemType | shared/Fishing/fishing_properties.lua:94 | `o.itemType = itemType` | Datei, Zeile, Argumente passen |
| Food.ctx37 | client/ISUI/Animal/ISAnimalContextMenu.lua:37 | `if item:isAnimalFeed() or (instanceof(item, "Food") and (item:getFoodType() == "Fruits" or` | Datei, Zeile, Argumente passen; isRotten am Server nur Client-Beleg (A3) |
| Food.getFullType | client/ISUI/Animal/ISAnimalContextMenu.lua:55 | `local testType = foodInv:getFullType();` | Datei, Zeile, Argumente passen |
| Food.isBurnt | client/ISUI/ISInventoryPane.lua:990 | `elseif instanceof(item, "Food") and item:getHungChange() < 0 and not item:getScriptItem():` | Datei, Zeile, Argumente passen; isBurnt am Server nur Client-Beleg (A3) |
| Food.evalRecurse | client/ISUI/Animal/ISAnimalContextMenu.lua:33 | `local foods = playerObj:getInventory():getAllEvalRecurse(function(item)` | Datei, Zeile, Argumente passen |
| Food.displayName | shared/Definitions/animal/ButcheringUtil.lua:334 | `text = text .. item:getDisplayName();` | Datei, Zeile, Argumente passen |
| Reg.isClientRet | server/Traps/STrapSystem.lua:1 | `if isClient() then return end` | Datei, Zeile, Argumente passen |
| Reg.getOrCreate | server/Foraging/forageServer.lua:26 | `forageData = ModData.getOrCreate("forageData");` | Datei, Zeile, Argumente passen |
| Reg.OnInitGMD | server/Vehicles/ProfessionVehicles.lua:347 | `Events.OnInitGlobalModData.Add(OnInitGlobalModData)` | Datei, Zeile, Argumente passen |
| Reg.getAnimalID | client/ISUI/Animal/ISAnimalUI.lua:53 | `txt = " (" .. self.animal:getAnimalID() .. ")";` | Datei, Zeile, Argumente passen; Server, Beleg nur Client (A3) |
| Reg.isExist | client/ISUI/Animal/ISAnimalUI.lua:15 | `if not self.animal or (not self.animal:isExistInTheWorld() and not self.animal:getHutch() ` | Datei, Zeile, Argumente passen |
| Reg.isDead | server/Traps/STrapGlobalObject.lua:238 | `if animal:isDead() then` | Datei, Zeile, Argumente passen |
| Reg.getXYZ | shared/Definitions/animal/ButcheringUtil.lua:575 | `animal:setX(animal:getX() + AnimalAvatarDefinition[modData["AnimalType"]].animalPositionX)` | Datei, Zeile, Argumente passen |
| Srv.DistTo | shared/TimedActions/Animals/ISPetAnimal.lua:6 | `return self.character:getSquare():DistTo(self.animal:getSquare()) < 3;` | Datei, Zeile, Argumente passen |
| Srv.removeFromHands | shared/Camping/TimedActions/ISAddFuelAction.lua:66 | `self.character:removeFromHands(self.item)` | Datei, Zeile, Argumente passen |
| Srv.Remove | shared/Camping/TimedActions/ISAddFuelAction.lua:67 | `self.character:getInventory():Remove(self.item)` | Datei, Zeile, Argumente passen |
| Srv.sendRemove | shared/Camping/TimedActions/ISAddFuelAction.lua:68 | `sendRemoveItemFromContainer(self.character:getInventory(),self.item)` | Datei, Zeile, Argumente passen |
| Srv.contains | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6 | `return self.character:getInventory():contains(self.food);` | Datei, Zeile, Argumente passen |
| Srv.petAnimal | shared/TimedActions/Animals/ISPetAnimal.lua:70 | `self.animal:petAnimal(self.character);` | Datei, Zeile, Argumente passen |
| Srv.getGridSquare | server/Animal/ISPickDungCursor.lua:104 | `local square = getCell():getGridSquare(x, y, z)` | Datei, Zeile, Argumente passen |
| Srv.OnClientCommand | server/ClientCommands.lua:1357 | `Events.OnClientCommand.Add(ClientCommands.OnClientCommand)` | Datei, Zeile, Argumente passen |
| Srv.filter | server/Foraging/forageServer.lua:56 | `forageServer.OnClientCommand = function(_module, _command, _plObj, _packet, _clientID)` | Datei, Zeile, Argumente passen |
| Srv.ZombRand | shared/TimedActions/Animals/ISMilkAnimal.lua:25 | `if ZombRand(100) < chance then` | Datei, Zeile, Argumente passen |
| Srv.sqGetX | shared/Traps/TrapSystem.lua:12 | `local mapZones = getWorld():getMetaGrid():getZonesAt(square:getX(), square:getY(), square:` | Datei, Zeile, Argumente passen |
| Srv.primaryHand | server/BuildingObjects/ISEmptyGraves.lua:18 | `if self.character:getPrimaryHandItem() then` | Datei, Zeile, Argumente passen |
| Srv.isRunning | client/Foraging/ISBaseIcon.lua:702 | `return ((self.character:isRunning() or self.character:isSprinting()) and self.character:is` | Datei, Zeile, Argumente passen |
| Srv.isSprintingBd | Bandits shared/PlayerDamageModel.lua:81 | `if player:isRunning() or player:isSprinting() then` | Datei, Zeile, Argumente passen |
| Srv.EveryTen | server/Traps/STrapSystem.lua:134 | `Events.EveryTenMinutes.Add(STrapSystem.addSound);` | Datei, Zeile, Argumente passen |
| Srv.OnTick | server/Foraging/forageServer.lua:502 | `Events.OnTick.Add(forageServer.relevanceTick);` | Datei, Zeile, Argumente passen |
| Wld.onlinePlayers | server/Foraging/forageServer.lua:463 | `local players = getOnlinePlayers();` | Datei, Zeile, Argumente passen |
| Wld.numActive | client/Fishing/FishingHandler.lua:6 | `for i = 0, getNumActivePlayers()-1 do` | Datei, Zeile, Argumente passen |
| Wld.specific | server/BuildingObjects/ISBuildingObject.lua:183 | `local playerObj = getSpecificPlayer(self.player)` | Datei, Zeile, Argumente passen |
| Wld.pIsDead | server/Seasons/season.lua:127 | `if player and not player:isDead() then` | Datei, Zeile, Argumente passen |
| Wld.pGetX | Bandits server/BanditServerSpawner.lua:179 | `local dist = BanditUtils.DistTo(x, y, player:getX(), player:getY())` | Datei, Zeile, Argumente passen |
| Wld.night | shared/Foraging/forageSystem.lua:1945 | `local season = getClimateManager():getSeason();` | Datei, Zeile, Argumente passen |
| Wld.timeOfDay | shared/Foraging/forageSystem.lua:1944 | `function forageSystem.getTimeOfDay()` | Datei, Zeile, Argumente passen |
| Wld.water | client/ISUI/ISWorldObjectContextMenu.lua:688 | `return floor ~= nil and floor:hasProperty(IsoFlagType.water)` | Datei, Zeile, Argumente passen |
| Wld.getFloor | client/ISUI/ISWorldObjectContextMenu.lua:687 | `local floor = square:getFloor()` | Datei, Zeile, Argumente passen |
| Wld.isOutside | Bandits server/BanditServerSpawner.lua:152 | `sp.outside = square:isOutside()` | Datei, Zeile, Argumente passen |
| Wld.solidBd | Bandits server/BuildingObjects/ZSGuardposts.lua:12 | `return square:TreatAsSolidFloor() and square:isFree(false)` | Datei, Zeile, Argumente passen |
| Wld.solidV | server/BuildingObjects/ISWalkToCursor.lua:35 | `if testSquare and not testSquare:TreatAsSolidFloor() then` | Datei, Zeile, Argumente passen |
| Wld.HasTree | server/Foraging/forageServer.lua:276 | `if gatedZ[chunkKey] or occupied[sqKey] or square:HasTree() then` | Datei, Zeile, Argumente passen |
| Wld.isFreeBd | Bandits server/BanditServerSpawner.lua:231 | `elseif not square:isFree(false) then` | Datei, Zeile, Argumente passen |
| Wld.isFreeV | client/ISUI/ISWorldObjectContextMenu.lua:2219 | `if square and square:isFree(false) then` | Datei, Zeile, Argumente passen |
| Wld.vehicle | server/BuildingObjects/ISBuildUtil.lua:34 | `if square:isVehicleIntersecting() then return false end` | Datei, Zeile, Argumente passen |
| Wld.isCanSee | client/Foraging/ISBaseIcon.lua:256 | `local canSeeSquare = self.square:isCanSee(self.player);` | Datei, Zeile, Argumente passen |
| Wld.ringRand | Bandits server/BanditServerSpawner.lua:217 | `local theta = ZombRandFloat(0, 2 * math.pi)` | Datei, Zeile, Argumente passen |
| Wld.allDefs | client/DebugUIs/DebugContextMenu.lua:246 | `local defs = getAllAnimalsDefinitions();` | Datei, Zeile, Argumente passen; Schreiber nutzt es am Server, Beleg nur Client (A3) |
| Wld.getBreeds | client/DebugUIs/DebugContextMenu.lua:273 | `local breeds = def:getBreeds();` | Datei, Zeile, Argumente passen; wie allDefs (A3) |
| Wld.addAnimalSrv | server/ClientCommands.lua:809 | `local animal = addAnimal(getCell(), tonumber(args.x), tonumber(args.y), tonumber(args.z), ` | Datei, Zeile, Argumente passen |
| Wld.addToWorldSrv | server/ClientCommands.lua:810 | `animal:addToWorld()` | Datei, Zeile, Argumente passen |
| Wld.addAnimalDbg | client/DebugUIs/DebugContextMenu.lua:1460 | `local animal = addAnimal(getCell(),` | Datei, Zeile, Argumente passen |
| Wld.blockMove | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:28 | `self.animal:getBehavior():setBlockMovement(false);` | Datei, Zeile, Argumente passen |
| Wld.removeBU | shared/Definitions/animal/ButcheringUtil.lua:609 | `animal:remove();` | Datei, Zeile, Argumente passen; Server-Muster braucht removeAnimal (A1) |
| Wld.removeDbg | client/DebugUIs/DebugContextMenu.lua:616 | `animal:remove()` | Datei, Zeile, Argumente passen; SP-Zweig (A1) |
| Wld.objList | client/DebugUIs/DebugContextMenu.lua:612 | `local animals = getCell():getObjectListForLua()` | Datei, Zeile, Argumente passen; Server, Beleg nur Client (A3) |
| Wld.instanceAnimal | client/DebugUIs/DebugContextMenu.lua:615 | `if instanceof(animal, "IsoAnimal") then` | Datei, Zeile, Argumente passen; Client-Beleg; shared ISAddAnimalInTrailer.lua:29 vorhanden |
| Wld.blockCtx | client/ISUI/Animal/ISAnimalContextMenu.lua:89 | `animal:getBehavior():setBlockMovement(true);` | Datei, Zeile, Argumente passen |
| Wld.blockPet | shared/TimedActions/Animals/ISPetAnimal.lua:36 | `self.animal:getBehavior():setBlockMovement(true);` | Datei, Zeile, Argumente passen; start() = Client (A2) |
| Wld.fleeTo | shared/TimedActions/Animals/ISMilkAnimal.lua:38 | `self.animal:fleeTo(sq);` | Datei, Zeile, Argumente passen |
| FA.derive | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3 | `ISFeedAnimalFromHand = ISBaseTimedAction:derive("ISFeedAnimalFromHand");` | Datei, Zeile, Argumente passen |
| FA.new | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:66 | `function ISFeedAnimalFromHand:new(character, animal, food)` | Datei, Zeile, Argumente passen |
| FA.isValid | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6 | `return self.character:getInventory():contains(self.food);` | Datei, Zeile, Argumente passen |
| FA.start14 | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:14 | `if self.animal:isExistInTheWorld() then` | Datei, Zeile, Argumente passen |
| FA.start15 | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:15 | `self:setActionAnim(self.animal:getFeedByHandAnim())` | Datei, Zeile, Argumente passen |
| FA.start16 | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:16 | `self:setOverrideHandModels(self.food, nil)` | Datei, Zeile, Argumente passen |
| FA.start17 | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:17 | `self.character:faceThisObject(self.animal)` | Datei, Zeile, Argumente passen |
| FA.start19 | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:19 | `self.animal:getBehavior():setBlockMovement(true);` | Datei, Zeile, Argumente passen; nur Client-Kopie im MP (A2) |
| FA.sound | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:23 | `self.sound = self.character:playSound("GiveFoodAnimal")` | Datei, Zeile, Argumente passen |
| FA.forceStop | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:29 | `ISBaseTimedAction.forceStop(self);` | Datei, Zeile, Argumente passen |
| FA.stop | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:35 | `ISBaseTimedAction.stop(self);` | Datei, Zeile, Argumente passen |
| FA.perform | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:42 | `ISBaseTimedAction.perform(self);` | Datei, Zeile, Argumente passen |
| FA.duration | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:54 | `if self.character:isTimedActionInstant() then` | Datei, Zeile, Argumente passen |
| FA.soundStop | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:62 | `self.character:getEmitter():stopOrTriggerSound(self.sound);` | Datei, Zeile, Argumente passen |
| FA.isPlaying | shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:61 | `if self.sound and self.character:getEmitter():isPlaying(self.sound) then` | Datei, Zeile, Argumente passen |
| FA.petDist | shared/TimedActions/Animals/ISPetAnimal.lua:6 | `return self.character:getSquare():DistTo(self.animal:getSquare()) < 3;` | Datei, Zeile, Argumente passen |
| FA.waitToStart | shared/TimedActions/Animals/ISPetAnimal.lua:11 | `return self.character:shouldBeTurning()` | Datei, Zeile, Argumente passen |
| FA.update | shared/TimedActions/Animals/ISPetAnimal.lua:17 | `self.animal:faceThisObject(self.character);` | Datei, Zeile, Argumente passen |
| FA.setVarAnimal | shared/TimedActions/Animals/ISPetAnimal.lua:43 | `self.animal:setVariable("idleAction", "petting")` | Datei, Zeile, Argumente passen |
| FA.clearVar | shared/TimedActions/Animals/ISPetAnimal.lua:48 | `self.animal:clearVariable("idleAction");` | Datei, Zeile, Argumente passen |
| FA.isDeadHutch | client/ISUI/Hutch/ISHutchUI.lua:427 | `if animal:isDead() then` | Datei, Zeile, Argumente passen |
| PA.derive | shared/TimedActions/Animals/ISPetAnimal.lua:3 | `ISPetAnimal = ISBaseTimedAction:derive("ISPetAnimal");` | Datei, Zeile, Argumente passen |
| PA.new | shared/TimedActions/Animals/ISPetAnimal.lua:95 | `function ISPetAnimal:new(character, animal)` | Datei, Zeile, Argumente passen |
| PA.aiming | shared/TimedActions/Animals/ISPetAnimal.lua:15 | `self.character:setIsAiming(false);` | Datei, Zeile, Argumente passen |
| PA.override | shared/TimedActions/Animals/ISPetAnimal.lua:25 | `self:setOverrideHandModels(nil, nil)` | Datei, Zeile, Argumente passen |
| PA.sizeX | shared/TimedActions/Animals/ISPetAnimal.lua:26 | `self.character:setVariable("AnimalSizeX", 0.01);` | Datei, Zeile, Argumente passen |
| PA.sizeY | shared/TimedActions/Animals/ISPetAnimal.lua:32 | `self.character:setVariable("AnimalSizeY", current/range);` | Datei, Zeile, Argumente passen |
| PA.petanimal | shared/TimedActions/Animals/ISPetAnimal.lua:37 | `self.character:setVariable("petanimal", true)` | Datei, Zeile, Argumente passen |
| PA.animalVar | shared/TimedActions/Animals/ISPetAnimal.lua:39 | `self.character:setVariable("animal", self.animal:getAnimalType())` | Datei, Zeile, Argumente passen |
| PA.petfalse | shared/TimedActions/Animals/ISPetAnimal.lua:47 | `self.character:setVariable("petanimal", false)` | Datei, Zeile, Argumente passen |
| PA.unblock | shared/TimedActions/Animals/ISPetAnimal.lua:49 | `self.animal:getBehavior():setBlockMovement(false);` | Datei, Zeile, Argumente passen |
| PA.stop | shared/TimedActions/Animals/ISPetAnimal.lua:57 | `ISBaseTimedAction.stop(self);` | Datei, Zeile, Argumente passen |
| PA.perform | shared/TimedActions/Animals/ISPetAnimal.lua:66 | `ISBaseTimedAction.perform(self);` | Datei, Zeile, Argumente passen |
| PA.stopOnAim | shared/TimedActions/Animals/ISPetAnimal.lua:100 | `o.stopOnAim = false;` | Datei, Zeile, Argumente passen |
| PA.loot | shared/Camping/TimedActions/ISAddFuelAction.lua:41 | `self:setActionAnim("Loot")` | Datei, Zeile, Argumente passen |
| BA.derive | shared/Camping/TimedActions/ISAddFuelAction.lua:3 | `ISAddFuelAction = ISBaseTimedAction:derive("ISAddFuelAction");` | Datei, Zeile, Argumente passen |
| BA.new | shared/Camping/TimedActions/ISAddFuelAction.lua:84 | `function ISAddFuelAction:new(character, campfire, item, fuelAmt)` | Datei, Zeile, Argumente passen |
| BA.report | shared/Camping/TimedActions/ISAddFuelAction.lua:43 | `self.character:reportEvent("EventLootItem");` | Datei, Zeile, Argumente passen |
| BA.stop | shared/Camping/TimedActions/ISAddFuelAction.lua:50 | `ISBaseTimedAction.stop(self);` | Datei, Zeile, Argumente passen |
| BA.perform | shared/Camping/TimedActions/ISAddFuelAction.lua:59 | `ISBaseTimedAction.perform(self);` | Datei, Zeile, Argumente passen |
| BA.duration | shared/Camping/TimedActions/ISAddFuelAction.lua:78 | `if self.character:isTimedActionInstant() then` | Datei, Zeile, Argumente passen |
| Cl.goodText | client/ServerCommands.lua:183 | `HaloTextHelper.addGoodText(player, getText("IGUI_HaloNote_LearnedRecipe", getRecipeDisplay` | Datei, Zeile, Argumente passen |
| Cl.badText | client/ISUI/ISWorldObjectContextMenu.lua:1038 | `HaloTextHelper.addBadText(playerObj, getText("IGUI_Sleep_NotSafe"));` | Datei, Zeile, Argumente passen |
| Cl.addText | client/Foraging/forageClient.lua:73 | `HaloTextHelper.addText(_character, tex .. "    " .. data.count .. " " .. item:getDisplayNa` | Datei, Zeile, Argumente passen |
| Cl.specific0 | client/ISUI/Animal/ISAnimalContextMenu.lua:134 | `local playerObj = getSpecificPlayer(player);` | Datei, Zeile, Argumente passen |
| Cl.nilArgs | client/ServerCommands.lua:211 | `if args then` | Datei, Zeile, Argumente passen |
| Cl.getPlayer | client/ServerCommands.lua:204 | `forageSystem.actionComplete(getPlayer(), args.iconID)` | Datei, Zeile, Argumente passen |
| Cl.OnServerCommand | client/ServerCommands.lua:218 | `Events.OnServerCommand.Add(ServerCommands.OnServerCommand)` | Datei, Zeile, Argumente passen |
| Cl.OnGameStart | client/Chat/ISChat.lua:1186 | `Events.OnGameStart.Add(ISChat.createChat);` | Datei, Zeile, Argumente passen |
| Cl.OnTick | client/Chat/ISChat.lua:943 | `Events.OnTick.Add(ISChat.ontick);` | Datei, Zeile, Argumente passen |
| Mn.addToolTip | client/ISUI/Animal/ISAnimalContextMenu.lua:161 | `local tooltip = ISWorldObjectContextMenu.addToolTip();` | Datei, Zeile, Argumente passen |
| Mn.setName | client/ISUI/Animal/ISAnimalContextMenu.lua:162 | `tooltip:setName(getText("Tooltip_Animal_TooFarAway"));` | Datei, Zeile, Argumente passen |
| Mn.descr | client/ISUI/ISWorldObjectContextMenu.lua:272 | `toolTip.description = getText("Tooltip_GrappleCorpse")` | Datei, Zeile, Argumente passen |
| Mn.notAvail | client/ISUI/Animal/ISAnimalContextMenu.lua:160 | `option.notAvailable = true;` | Datei, Zeile, Argumente passen |
| Mn.fullName | client/ISUI/Animal/ISAnimalContextMenu.lua:140 | `local text = animal:getFullName()` | Datei, Zeile, Argumente passen |
| Mn.getOptFromName | client/Tutorial/Tutorial1.lua:131 | `if not context:getOptionFromName(text) then` | Datei, Zeile, Argumente passen |
| Mn.options | client/ISUI/ISContextMenu.lua:890 | `for i,v in ipairs(self.options) do` | Datei, Zeile, Argumente passen |
| Mn.exist88 | client/ISUI/Animal/ISAnimalContextMenu.lua:88 | `if animal:isExistInTheWorld() then -- animal in world` | Datei, Zeile, Argumente passen |
| Mn.square90 | client/ISUI/Animal/ISAnimalContextMenu.lua:90 | `if luautils.walkAdj(player, animal:getSquare()) then` | Datei, Zeile, Argumente passen |
| Mn.queueClear | client/ISUI/ISWorldObjectContextMenu.lua:1056 | `ISTimedActionQueue.clear(playerObj)` | Datei, Zeile, Argumente passen |
| Mn.transfer | client/ISUI/ISWorldObjectContextMenu.lua:2609 | `ISWorldObjectContextMenu.transferIfNeeded(playerObj, handItem)` | Datei, Zeile, Argumente passen |
| Mn.equip93 | client/ISUI/Animal/ISAnimalContextMenu.lua:93 | `ISWorldObjectContextMenu.equip(player, player:getPrimaryHandItem(), food, true, false)` | Datei, Zeile, Argumente passen |
| Mn.walkKeep | client/ISUI/ISWorldObjectContextMenu.lua:2564 | `if luautils.walkAdj(playerObj, square, true) then` | Datei, Zeile, Argumente passen |
| Mn.queueAdd94 | client/ISUI/Animal/ISAnimalContextMenu.lua:94 | `ISTimedActionQueue.add(ISFeedAnimalFromHand:new(player, animal, food))` | Datei, Zeile, Argumente passen |
| Mn.walkAdjSig | shared/luautils.lua:119 | `function luautils.walkAdj(playerObj, square, keepActions, excludeList)` | Datei, Zeile, Argumente passen |
| Mn.transfer577 | client/ISUI/Animal/ISAnimalContextMenu.lua:577 | `ISWorldObjectContextMenu.transferIfNeeded(playerObj, item)` | Datei, Zeile, Argumente passen |
| Mn.addOpt272 | client/ISUI/Animal/ISAnimalContextMenu.lua:272 | `local lureOption = animalSubMenu:addOption(getText("ContextMenu_Lure"), nil, nil);` | Datei, Zeile, Argumente passen |
| Mn.getNew273 | client/ISUI/Animal/ISAnimalContextMenu.lua:273 | `local lureSubMenu = ISContextMenu:getNew(animalSubMenu);` | Datei, Zeile, Argumente passen |
| Mn.addSub274 | client/ISUI/Animal/ISAnimalContextMenu.lua:274 | `animalSubMenu:addSubMenu(lureOption, lureSubMenu);` | Datei, Zeile, Argumente passen |
| Mn.subOpt280 | client/ISUI/Animal/ISAnimalContextMenu.lua:280 | `local option = lureSubMenu:addOption(getItemDisplayName(item:getType()), animal, AnimalCon` | Datei, Zeile, Argumente passen |
| Mn.pet287 | client/ISUI/Animal/ISAnimalContextMenu.lua:287 | `local option = animalSubMenu:addOption(getText("ContextMenu_PetAnimal"), animal, AnimalCon` | Datei, Zeile, Argumente passen |
| Mn.icon288 | client/ISUI/Animal/ISAnimalContextMenu.lua:288 | `option.iconTexture = getTexture("media/ui/AnimalActions_Pet.png")` | Datei, Zeile, Argumente passen |
| Mn.getSubMenu | client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:41 | `shovelSubMenu = context:getSubMenu(shovelOption.subOption);` | Datei, Zeile, Argumente passen |
| Mn.kill | client/ISUI/Animal/ISAnimalContextMenu.lua:310 | `option = animalSubMenu:addOption(getText("ContextMenu_KillAnimal"), animal, AnimalContextM` | Datei, Zeile, Argumente passen |
| Mn.killText | client/ISUI/Animal/ISAnimalContextMenu.lua:310 | `option = animalSubMenu:addOption(getText("ContextMenu_KillAnimal"), animal, AnimalContextM` | Datei, Zeile, Argumente passen |
| Mn.removeByName | client/ISUI/ISContextMenu.lua:1016 | `function ISContextMenu:removeOptionByName(optName)` | Datei, Zeile, Argumente passen |
| Mn.ctxEvent | client/ISUI/Animal/ISAnimalContextMenu.lua:1235 | `Events.OnClickedAnimalForContext.Add(AnimalContextMenu.clickedAnimals);` | Datei, Zeile, Argumente passen |
| Mn.ctxLoop | client/ISUI/Animal/ISAnimalContextMenu.lua:1013 | `AnimalContextMenu.clickedAnimals = function(player, context, animals, test)` | Datei, Zeile, Argumente passen |
| Mn.setTest | client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81 | `if test then return ISWorldObjectContextMenu.setTest() end` | Datei, Zeile, Argumente passen |
| Mn.sub48 | client/ISUI/Animal/ISAnimalContextMenu.lua:48 | `local subMenuFeed = ISContextMenu:getNew(context);` | Datei, Zeile, Argumente passen |
| Mn.sub49 | client/ISUI/Animal/ISAnimalContextMenu.lua:49 | `context:addSubMenu(feedOption, subMenuFeed);` | Datei, Zeile, Argumente passen |
| Mn.isOutside | client/Foraging/ISZoneDisplay.lua:400 | `if square and square:isOutside() then` | Datei, Zeile, Argumente passen |
| Mn.hutch4 | client/ISUI/Hutch/ISHutchMenu.lua:4 | `if test and ISWorldObjectContextMenu.Test then return true end` | Datei, Zeile, Argumente passen |
| Mn.hutch6 | client/ISUI/Hutch/ISHutchMenu.lua:6 | `local playerObj = getSpecificPlayer(player)` | Datei, Zeile, Argumente passen |
| Mn.hutch8 | client/ISUI/Hutch/ISHutchMenu.lua:8 | `if playerObj:getVehicle() then return false end` | Datei, Zeile, Argumente passen |
| Mn.hutch11 | client/ISUI/Hutch/ISHutchMenu.lua:11 | `for i,v in ipairs(worldobjects) do` | Datei, Zeile, Argumente passen |
| Mn.hutch115 | client/ISUI/Hutch/ISHutchMenu.lua:115 | `Events.OnFillWorldObjectContextMenu.Add(ISHutchMenu.OnFillWorldObjectContextMenu)` | Datei, Zeile, Argumente passen |
| Mn.objSquare | client/ISUI/ISWorldObjectContextMenu.lua:2571 | `local parent = item:getSquare()` | Datei, Zeile, Argumente passen |
| Hud.btnPrompt | client/ISUI/ISButtonPrompt.lua:1244 | `o = ISUIElement:new(0, 0, 1, 1);` | Datei, Zeile, Argumente passen |
| Hud.fenris | client/DebugUIs/Scenarios/FenrisScenario.lua:505 | `local zombies = getCell():getObjectListForLua()` | Datei, Zeile, Argumente passen |
| Hud.instTrailer | shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29 | `if self.animal and instanceof(self.animal, "IsoAnimal") and self.animal:isExistInTheWorld(` | Datei, Zeile, Argumente passen |
| Hud.fontH | client/ISUI/Animal/ISAnimalUI.lua:4 | `local FONT_HGT_SMALL = getTextManager():getFontHeight(UIFont.Small)` | Datei, Zeile, Argumente passen |
| Hud.farming | client/Farming/CFarmingSystem.lua:45 | `local playerObj = getSpecificPlayer(0)` | Datei, Zeile, Argumente passen |
| Hud.isoToScreen | client/Fishing/TensionUI.lua:11 | `local offX = isoToScreenX(self.playerIndex, self.player:getX(), self.player:getY(), self.p` | Datei, Zeile, Argumente passen |
| Hud.ctxGetX | client/TimedActions/ISContextualActions.lua:100 | `local sq = getSquare(animal:getX(), animal:getY(), animal:getZ());` | Datei, Zeile, Argumente passen |
| Hud.drawTextCentre | client/ISUI/ISUIElement.lua:1280 | `function ISUIElement:drawTextCentre(str, x, y, r, g, b, a, font)` | Datei, Zeile, Argumente passen |
| Hud.drawRect | client/ISUI/ISUIElement.lua:1191 | `function ISUIElement:drawRect( x, y, w, h, a, r, g, b)` | Datei, Zeile, Argumente passen |
| Hud.drawRectBorder | client/ISUI/ISUIElement.lua:1219 | `function ISUIElement:drawRectBorder( x, y, w, h, a, r, g, b)` | Datei, Zeile, Argumente passen |
| Hud.removeUI | client/ISUI/ISUIElement.lua:1373 | `function ISUIElement:removeFromUIManager()` | Datei, Zeile, Argumente passen |
| Hud.timestamp | client/Foraging/ISBaseIcon.lua:485 | `self.currentTimestamp = getTimestampMs();` | Datei, Zeile, Argumente passen |
| Hud.init746 | client/ISUI/Animal/ISAnimalContextMenu.lua:746 | `ui:initialise();` | Datei, Zeile, Argumente passen |
| Hud.add747 | client/ISUI/Animal/ISAnimalContextMenu.lua:747 | `ui:addToUIManager();` | Datei, Zeile, Argumente passen |
| Hud.noBg | client/ISUI/ISPanel.lua:9 | `function ISPanel:noBackground()` | Datei, Zeile, Argumente passen |
| Bn.curSquare | client/ISUI/ISWorldObjectContextMenu.lua:112 | `local playerSq = playerObj:getCurrentSquare()` | Datei, Zeile, Argumente passen |
| Bn.say | client/Entity/ISEntityUI.lua:458 | `getPlayer():Say(getText("IGUI_ObjectAlreadyUsedSayMessage"));` | Datei, Zeile, Argumente passen |
| Bn.addItem | client/Tests/RecipeTests.lua:317 | `local item1 = playerObj:getInventory():AddItem("Base.Needle")` | Datei, Zeile, Argumente passen |
| Bn.setHealth | shared/TimedActions/Animals/ISKillAnimal.lua:58 | `self.animal:setHealth(0);` | Datei, Zeile, Argumente passen |

Statisch geprueft, nicht gespielt.
