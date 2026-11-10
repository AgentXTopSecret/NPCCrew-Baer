# Lauf baer-zaehmen (B1a): Engine-Belege fuer "Junges finden und zaehmen"

Stand 10.11.2026. **Statisch gelesen, nichts gebaut, nichts gespielt.** Jede Laufzeit-Aussage ohne Beleg ist "ungeprueft".

Schreibweise der Fundstellen:
- `V:` = Vanilla-Lua, `C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/lua/` (Stand der Platte heute).
- `B:` = Bandits, `.../workshop/content/108600/3268487204/mods/Bandits/42.22/media/lua/`.
- `NC:` = NPC Crew, `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua/` (nur gelesen; kein Engine-Beleg im Sinn der eisernen Regel, aber gespieltes Vorbild).
- `Jar:` = nur Lesehilfe. Frisch aus dem heutigen Jar gezogen nach `_arbeit/baer_zaehmen/jar/` (Klassen), `_arbeit/baer_zaehmen/javap/`
  (javap -c -p), `_arbeit/baer_zaehmen/dec/` (Vineflower 1.12.0). Werkzeug `_arbeit/baer_zaehmen/jar_holen.py`.
- **VERBOTEN** = nur im Jar belegt, braucht Kevins Wort je Methode. **BELEGT** = echter Aufruf in Vanilla-Lua oder Bandits, gleiche Argumenttypen.

---

## 0. Vier Nebenfunde, die vor dem Bau jeder wissen muss

**0.1 Das Spiel ist 42.22.2, nicht 42.21.** `C:/Users/Kevin/Zomboid/console.txt:61`: `version=42.22.2 3d39148846`. `projectzomboid.jar`
traegt das Datum 09.11.2026 16:07, 117 Vanilla-Lua-Dateien ebenso (u. a. `server/ClientCommands.lua`, `client/DebugUIs/DebugContextMenu.lua`,
`shared/Definitions/animal/ButcheringUtil.lua`, `client/ISUI/ISVehicleAnimalUI.lua`). Folgen:
- Zeilennummern aus aelteren Baer-Unterlagen stimmen fuer diese Dateien nicht mehr: `ClientCommands.lua` "754" ist heute **803-811**
  (animal.add), "964-971" ist heute **1014-1022** (animal.acceptance), "928" ist **978** (setDebugStress); `DebugContextMenu.lua` "1462-1471" ist
  **1450-1468**, "615-623" ist **611-619**, "640" (pathToLocation am Zombie) ist **636**; `ButcheringUtil.lua` "569" (setSizeForced) ist **586**,
  "566" (setWeight) bleibt 566. `ISAnimalContextMenu.lua`, `ISPetAnimal.lua`, `ISFeedAnimalFromHand.lua`, `ISAnimalUI.lua` sind unveraendert.
- Die alten Jar-Auszuege (`_arbeit/baer_spiel/dec`, `_arbeit/baer_angriff`, `_arbeit/baer_begleiter`) stammen aus 42.21. Was hier zitiert
  wird, ist am heutigen Jar nachgelesen. Eine Aussage der alten Recherche ist dadurch **ueberholt**: Tiere werden nicht mehr in
  `IsoGridSquare.save/load` geschrieben (dort steht heute kein `IsoAnimal` mehr), sondern ueber `AnimalPopulationManager` (Abschnitt 1.4).
- Bandits hat seit 09.11. einen Ordner `42.22` (das Spiel laedt den). Gegen `42.21` unterscheiden sich nur `shared/BanditUtils.lua` und drei
  `ZombieActions/ZALoot*.lua`/`ZATakeFromContainer.lua`; `LosUtil.lineClear` steht in 42.22 in Zeile **1290** (42.21: 1288).

**0.2 Bandits' Spielmodus-Frage ist seit dem Update kaputt -- nicht nachbauen.** `B:shared/BanditUtils.lua:171-175` merkt
`getWorld():getGameMode()` und `B:server/BanditServerSpawner.lua:54` vergleicht mit dem Text `"Multiplayer"`; Vanilla vergleicht heute mit
`GameMode.MULTIPLAYER` (`V:client/OptionScreens/CharacterCreationProfession.lua:575`). NPC Crew hat das am 09.11. als v3.14.65 abgefangen
(`NC:shared/BanditsNPC.lua:6288-6312`). Fuer uns: SP/MP nur ueber `isClient()` / `isServer()` fragen (`V:shared/TimedActions/ISEatFoodAction.lua:136`
`if not isClient() and not isServer() then`).

**0.3 Im MP darf nur der Server Gegenstaende entfernen.** NPC-Crew-Lehre vom 09.11. (`NPCCrew/CLAUDE.md:4005`): 42.22.2 hat
`ItemContainer.removeItemOnServer` entfernt, das Paket dahinter verlangt `EditItem` (Rolle user = Kick). Futter verbraucht also immer
`complete()` der Zeitaktion (laeuft im MP auf dem Server), nie Client-Code (Abschnitt 8.3).

**0.4 `getAnimalID()` ist nicht eindeutig.** Jar `IsoAnimal.init` (dec/IsoAnimal.java:1484, javap IsoAnimal Offset 44-50):
`this.animalId = Rand.Next(10000)`. Die Zahl wird gespeichert und geladen (dec/IsoAnimal.java:1279/1391), ist aber nur eine von 10000.
NPC Crew sagt dasselbe (`NC:client/BanditsNPCLivestockNet.lua:711-712`: "nie die animalID allein, sie ist nicht eindeutig") und benennt Tiere
ueber das Paar (getOnlineID, getAnimalID). Dazu loescht die Engine beim Erzeugen/Laden ein Tier, wenn in 4 Kacheln schon eines mit gleicher
ID steht (`checkForChickenpocalypse`, gerufen in jedem Konstruktor, dec/IsoAnimal.java:229; javap Offset 134-158 "Possible chickenpocalypse, deleting the newly
created animal"). Folge fuer das Register: eigener Schluessel in der ModData des Tiers (Abschnitt 5.2), AnimalID nur als Gegenprobe.

---

## 1. Tier erzeugen, finden, entfernen

### 1.1 Erzeugen

| Aufruf | Fundstelle (Zeile zitiert) | Argumente | Seite |
|---|---|---|---|
| `addAnimal(getCell(), x, y, z, typ, breed, skeleton)` danach `animal:addToWorld()` | `V:client/DebugUIs/DebugContextMenu.lua:1460-1467` `local animal = addAnimal(getCell(), square:getX(), square:getY(), square:getZ(), type, breed, skeleton)` / `animal:addToWorld()` | IsoCell, 3 ganze Zahlen, Text, AnimalBreed-Objekt, boolean | SP (der `else`-Zweig von `if isClient()`) |
| dasselbe auf dem Server | `V:server/ClientCommands.lua:808-810` `local breed = AnimalDefinitions.getDef(args.type):getBreedByName(args.breed)` / `local animal = addAnimal(getCell(), tonumber(args.x), tonumber(args.y), tonumber(args.z), args.type, breed, args.skeleton)` / `animal:addToWorld()` | wie oben | Server (und SP: `server/` laedt auch dort) |
| Rasse ueber die Definitionsliste | `V:client/DebugUIs/DebugContextMenu.lua:246-275` `local defs = getAllAnimalsDefinitions()` ... `def:getAnimalType()` ... `local breeds = def:getBreeds()` ... `breeds:get(i)` | - | Client/SP; so macht es `NCBearSpawn.lua:15-27` |
| Rasse ueber den Namen | `V:server/ClientCommands.lua:808` (oben), `V:client/ISUI/Hutch/ISHutchUI.lua:176` | Text, Text | Server und Client |
| Variante der Falle: `IsoAnimal.new(getCell(), x, y, z, typ, breedName)` | `V:server/Traps/STrapGlobalObject.lua:211` | Rasse als TEXT | Server/SP -- nicht noetig, `addAnimal` reicht |

Fallen:
- **Der Vanilla-Serverbefehl `animal.add` ist tabu:** er verlangt `Capability.AnimalCheats` (`V:server/ClientCommands.lua:804`). Wir bauen einen
  EIGENEN Weg, bei dem der Server von sich aus (Takt) oder nach eigener Pruefung `addAnimal` ruft -- derselbe Aufruf, aber kein Client-Debug-Weg,
  kein Kick-Risiko. Im SP ruft derselbe Code direkt.
- **Wasser:** steht die Kachel im Wasser, kehrt der Konstruktor vor `init` zurueck, das Tier bleibt halb gebaut (Jar dec/IsoAnimal.java
  Konstruktoren, dec/IsoAnimal.java:229/255/308/322: der ganze Aufbau steht in `if (!this.checkForChickenpocalypse(null) && !this.checkForWater()) { ... }`). Vorher pruefen wie `NCBearSpawn.lua:30-33`
  (`V:client/ISUI/ISWorldObjectContextMenu.lua:687-688` `local floor = square:getFloor()` / `return floor ~= nil and floor:hasProperty(IsoFlagType.water)`).
- `AnimalDefinitions.getDef(typ)` gibt nil, wenn die Art nicht geladen ist -> vor `:getBreedByName` auf nil pruefen; `addAnimal` kann nil
  liefern (NCBearSpawn.lua:52 prueft es schon).
- Koordinaten als ganze Zahlen uebergeben (`square:getX()`); die Java-Signatur ist `(IsoCell, int, int, int, String, AnimalBreed, boolean)`
  (Jar javap LuaManager_GlobalObject `addAnimal`).
- Neues Tier ist wild, wenn die Definition `wild = true` sagt (Jar `IsoAnimal.init`: `this.setWild(this.adef.wild)`), und bekommt dabei
  Stress 50..80 (Jar `setWild`, dec/IsoAnimal.java:3190-3200).

### 1.2 Wiederfinden (auch nach dem Laden)

| Aufruf | Fundstelle | Seite | Bemerkung |
|---|---|---|---|
| `getCell():getObjectListForLua()` + `instanceof(o, "IsoAnimal")` + `o:getAnimalType()` | `V:client/DebugUIs/DebugContextMenu.lua:612-615` `local animals = getCell():getObjectListForLua()` / `if instanceof(animal, "IsoAnimal") then`; Typ: `V:client/ISUI/Animal/ISAnimalUI.lua:65`; so sucht `NCBearFight.lua:1784-1788` | SP/Client belegt; Server: dieselbe Funktion, kein Vanilla-Aufruf in `server/` (ungeprueft, Jar: `IsoCell.getObjectListForLua` kopiert die ganze Liste je Aufruf, dec/IsoCell.java:2990 -> selten rufen) | findet alle geladenen Tiere |
| `sq:getAnimals()` | `V:client/ISUI/ISVehicleAnimalUI.lua:165` `local animals = sq:getAnimals();` | Client belegt; gleiche Methode auf dem Server | billig, wenn die letzte Kachel im Register steht (Umkreis absuchen) |
| `getAnimal(onlineId)` | `V:server/ClientCommands.lua:817` `local animal = getAnimal(tonumber(args.id))` | **nur Server** belegt | Schluessel ist die OnlineID (Jar: `AnimalInstanceManager.get(short)`), nicht die AnimalID |
| `animal:getOnlineID()` / `animal:getAnimalID()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:432` `"id", animal:getOnlineID())`; `V:client/ISUI/Animal/ISAnimalUI.lua:53` `self.animal:getAnimalID()` | Client | |
| lebt / ist in der Welt | `V:client/ISUI/Animal/ISAnimalUI.lua:15` `self.animal:isExistInTheWorld()`; `V:client/ISUI/Hutch/ISHutchUI.lua:427` `if animal:isDead() then` | Client | wie `NCBearFight.lua:1762-1764` |
| ModData am Tier | `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127` `animal:getModData()["skeleton"] = "true";`; `V:shared/Definitions/animal/ButcheringUtil.lua:586` | beide | wird gespeichert (1.4) |

Fallen:
- Im SP steht ein frisch per `addAnimal` erzeugtes Tier NICHT in der OnlineID-Tabelle (Jar `IsoAnimal.init` Offset 121-137: `AnimalInstanceManager.add`
  nur bei `GameServer.server`); nach dem Laden schon (Jar `AnimalManagerMain.fromWorker`). `getAnimal(id)` taugt im SP also nicht als einziger Weg
  -> dort ueber die Liste bzw. `sq:getAnimals()` und den eigenen Schluessel in der ModData suchen.
- `getCell():getAnimals()` hat keine Vanilla-Lua-Fundstelle (grep `getCell():getAnimals`: 0) -> nicht benutzen (so auch `NC:client/BanditsNPCCompat.lua:316`).

### 1.3 Entfernen (kein Geistertier, keine Leiche)

| Aufruf | Fundstelle | Seite |
|---|---|---|
| `animal:remove()` | `V:client/DebugUIs/DebugContextMenu.lua:616` `animal:remove()`; `V:shared/Definitions/animal/ButcheringUtil.lua:609` `animal:remove();` (shared, laeuft auch auf dem Server); `NCBearSpawn.lua:72` | SP und Server |
| `removeAnimal(onlineId)` | `V:server/ClientCommands.lua:841` `removeAnimal(tonumber(args.id))`; `V:shared/Definitions/animal/ButcheringUtil.lua:612-614` `if isServer() then ... removeAnimal(animal:getOnlineID());` | Server |

Jar (Lesehilfe): `remove()` loest Mutter, Seil und Spieler, dann `delete()` = `removeFromWorld` + `removeFromSquare` + `setSquare(null)` +
`removeFromUpdateLists` (auf dem Server meldet das die Loeschung an die Clients, `AnimalSynchronizationManager.delete`). Es entsteht keine
Leiche (die gibt es nur ueber den Tod). `removeAnimal(id)` ist `getAnimal(id):remove()` mit Rueckfall auf die Sync-Tabelle.
Fallen: nur der Server bzw. SP entfernt; ein Client, der `remove()` an seiner Kopie ruft, erzeugt genau das Geistertier. Vor dem Entfernen die
eigene Sperre loesen (`animal:getBehavior():setBlockMovement(false)`), falls gesetzt.

### 1.4 Bleibt ein per Lua erzeugtes Tier beim Speichern/Entladen erhalten?

Kein Lua-Beleg noetig (wir rufen nichts dafuer), nur Verstaendnis. **Jar 42.22.2, ungespielt:**
- Beim Entladen einer Kachel: `AnimalPopulationManager.removeChunkFromWorld` -> je Tier `animal.unloaded()`, `n_addAnimal(animal)` (das Tier
  wird als `VirtualAnimal` an den Worker gegeben, das Objekt haengt daran), `removeFromUpdateLists()` (dec/AnimalPopulationManager.java:59-87).
- Beim Speichern: `AnimalManagerMain.saveRealAnimals` sammelt alle `IsoAnimal` der Zelle (dec/AnimalManagerMain.java:46-56).
- Beim Laden der Kachel: `AnimalManagerMain.fromWorker` setzt Tiere OHNE `migrationGroup` und mit `virtualId == 0` genau auf ihre alte
  Stelle zurueck (`setForceX/Y`), ruft `addToWorld()` und traegt sie in die OnlineID-Tabelle ein (dec/AnimalManagerMain.java:58-113).
- `IsoAnimal.save` schreibt u. a. `customName`, **ModData**, `animalId`, Stress, die Akzeptanz-Liste, `petTimer`, `wild`
  (dec/IsoAnimal.java:1250-1362). Nicht gespeichert: unverwundbar, Bewegungssperre.
- Ein Tier ohne Wandergruppe bewegt sich als virtuelles Tier nicht (`MigrationGroupDefinitions.initValueFromDef` setzt ohne Definition
  nichts, dec/MigrationGroupDefinitions.java:289-311). **Ob es wirklich an derselben Stelle wieder steht: ungespielt** (mit dem
  erwachsenen "bear" in NCBearTest hat es bisher gehalten -- Kevins Spielstaende; unter 42.22.2 noch nicht bewusst geprueft).
- Ein Spielstand mit gespeichertem Jungen ohne die Mod wirft beim Laden (bekannt aus `NCBearSpawn.lua:77-78`); gilt fuer die neue Art genauso.

---

## 2. Tier-Definition des Jungen

Vorbild `NCBearDefs.lua:62-99` und `V:shared/Definitions/animal/DeerDefinitions.lua:58-92` (fawn). Die Engine liest diese Schluessel
(Jar `AnimalDefinitions.loadAnimalDefinitions`, Zeichenketten aus javap/AnimalDefinitions.txt): bodyModel, animset, group, stages, breeds,
genes, minSize, maxSize, animalSize, collisionSize, shadoww/fm/bm, wanderMul, idleTypeNbr, sittingTypeNbr, eatingTypeNbr, spottingDist,
wild, canBeDomesticated, fleeZombies, alwaysFleeHumans, canBePicked, canBePet, canBeFeedByHand, feedByHandType, eatTypeTrough,
feedByHandAnim, canBeAttached, canBeAlerted, sitRandomly, canThump, collidable, needMom, attackIfStressed, hungerMultiplier,
thirstMultiplier, healthLossMultiplier, thirstHungerTrigger, minWeight, maxWeight, corpseSize, minBlood, maxBlood, trailerBaseSize,
canClimbStairs, canClimbFences, stressUnderRain, stressAboveGround, canBeKilledWithoutWeapon, male/female, wildFleeTimeUntilDeadTimer u. a.

**Vorgaben, wenn ein Feld fehlt** (Jar Konstruktor `AnimalDefinitions()`, javap Offset 4-181): alwaysFleeHumans = **true**, fleeZombies = **true**,
canBePicked = **true**, canThump = **true**, collidable = true, needMom = true, canBeDomesticated = **true**, spottingDist 10, wanderMul 400,
healthLossMultiplier 0,05, thirstHungerTrigger 0,1; alles andere false/0 (also wild, canBePet, canBeFeedByHand, canBeAttached = false;
hungerMultiplier/thirstMultiplier = 0 -> kein Hunger, kein Durst).

| Feld | Vanilla-Vorbild | Wirkung (Jar-Lesart, ungespielt) |
|---|---|---|
| `wild = true` | `V:DeerDefinitions.lua:79` `AnimalDefinitions.animals["fawn"].wild = true; -- wild animal will have some other behavior, they don't require to eat/drink and will always flee humans`; Waschbaer/Kaninchen `V:RaccoonDefinitions.lua:81`, `V:RabbitDefinitions.lua:129` | kein Hunger/Durst, keine Gesundheitsaenderung durch Mangel (dec/AnimalData.java:347-398); Stress baut sich NICHT von selbst ab (dec/IsoAnimal.java:670-671); **flieht immer**, sobald ein Spieler naeher als 3 Kacheln ist, und zwar 30 Kacheln weit im Rennen (dec/BaseAnimalBehavior.java:1581-1583, 1471-1479); weiter weg je nach Gang/Schleichen/Blickwinkel; Laerm: Fluchtweite `radius*3+20` (dec/IsoAnimal.java:790-794); ein Waffentreffer startet einen Verblutungs-Zaehler (`wildFleeTimeUntilDeadTimer`, dec/IsoAnimal.java:1129-1134); im Vanilla-Menue ist "Animal info" gesperrt und "Kill" fehlt (`V:ISAnimalContextMenu.lua:166-171`, `:307`); Name bekommt den Zusatz "(Wild)" (`IGUI_Animal_Wild`, dec/IsoAnimal.java:2265) |
| `canBeDomesticated` | `V:DeerDefinitions.lua:83` `= false`; Waschbaer laesst die Vorgabe true (`V:RaccoonDefinitions.lua:88` auskommentiert) | nur mit true wirkt `animal:setWild(false)` (dec/IsoAnimal.java:3190-3200). **`animal:setWild(false)` ist BELEGT:** `V:server/Traps/STrapGlobalObject.lua:223` `animal:setWild(false);`, `V:shared/TimedActions/Animals/ISPickupAnimal.lua:52`. `setWild(true)` hat keine Lua-Fundstelle (grep `setWild`: nur die zwei) -> zurueck zu wild geht nicht belegt |
| `alwaysFleeHumans = false` | `V:CowDefinitions.lua:205` `= false; -- animal can flee or not humans` | gilt nur fuer NICHT wilde Tiere: dann flieht es nur, wenn der Spieler sich bewegt, mit Zufall aus Stress/2,2 - Akzeptanz/2 + Abstand*5 (x4 bei rennendem Spieler); ab Akzeptanz >= 40 und Stress < 70 nie (dec/BaseAnimalBehavior.java:1431-1458) |
| `fleeZombies` | `NCBearDefs.lua:88` false; Vorgabe true | true: flieht vor Zombies (passt zum Jungen "versteckt sich"); Zombies in 10 Kacheln heben den Stress (dec/BaseAnimalBehavior.java:1691-1699) |
| `canBePicked = false` | `NCBearDefs.lua:91`; Gegenbeispiel `V:CowDefinitions.lua:158` | Menuepunkt "Pick up" erscheint nur bei `animal:canBePicked(playerObj)` (`V:ISAnimalContextMenu.lua:265`); Jar: false AUSSER der Spieler hat Unlimited Carry oder God Mode (dec/IsoAnimal.java:3146-3150). **Hochheben ist damit fuer normale Spieler aus.** |
| `canBePet` | `V:CowDefinitions.lua:230` `= true` | schaltet nur den VANILLA-Menuepunkt "Pet" frei (`V:ISAnimalContextMenu.lua:286`). Fuer unseren eigenen Punkt egal. Achtung 7.3: ohne Attachment `head` am Modell tut der Vanilla-Punkt nichts |
| `canBeAttached` | `V:CowDefinitions.lua:206`; Vorgabe false | false lassen: sonst kann jeder das Junge anleinen (`V:ISAnimalContextMenu.lua:173-186`) |
| `feedByHandType` / `eatTypeTrough` | `V:SheepDefinitions.lua:179` `feedByHandType = "SheepMilk"`; `V:ChickenDefinitions.lua:113` `eatTypeTrough = "AnimalFeed,Grass,Hay,Vegetables,Fruits,Seeds,Nuts,Nut,Insect"`; `V:MouseDefinitions.lua:111` `"All"` | steuert nur Vanillas "Feed"/"Lure". Vanillas Futterliste ist hart auf Tierfutter, Milch, `Fruits`, `Vegetables` begrenzt (Jar `ItemContainer.getAllFoodsForAnimals`, dec/ItemContainer.java:3376-3392; `V:ISAnimalContextMenu.lua:33-39`) -- **Honig und Fisch kommen dort nie vor** |
| `sitRandomly` | `V:DeerDefinitions.lua:77` true; `NCBearDefs.lua:93` false | true braucht die Sitz-Clips im Netz des Jungen (Aufgabe: dieselben 15 Clip-Namen) -- Wirkung ungespielt |
| `stages` ohne `nextStage` | `NCBearDefs.lua:63-64` `stufen[name] = { ageToGrow = 60 }`; Gegenbeispiel `V:DeerDefinitions.lua:8-11` (fawn mit nextStage) | ohne `nextStage` ist `isBaby()` false (Jar) -> kein "braucht Mutter", kein Stufenwechsel (der ein neues Objekt baute). `needMom = false` trotzdem setzen (`V:ChickenDefinitions.lua:127`) |
| `minSize = maxSize = 0.35` | `NCBearDefs.lua:73-74` (dort 1,0) | Groesse fest. **Falle:** Vanillas Streichel-Aktion teilt durch `getMaxSize() - getMinSize()` (`V:ISPetAnimal.lua:27-32`) -> bei 0 wird `AnimalSizeY` unendlich. Eigene Aktion: festen Wert setzen |
| `hungerMultiplier` / `thirstMultiplier` | `V:CowDefinitions.lua:209` `= 0.0035; -- per hour, set it to 0 to ignore hunger` | weglassen = 0 = kein Hunger. Dann frisst `feedFromHand` nichts weg (Abschnitt 8.3) |
| `group` | `NCBearDefs.lua:68`; Pflicht fuer das Debug-Menue `V:DebugContextMenu.lua:249-253` | braucht `IGUI_Animal_Group_<group>` |
| Tier-Info-Fenster, Zerlegen | `NCBearDefs.lua:104-127` | `AnimalAvatarDefinition["ncbearcub"]` (sonst wirft `V:ISAnimalUI.lua:31`) und `AnimalPartsDefinitions.animals["ncbearcub" .. rasse]` (`V:ButcheringUtil.lua:18`) wie beim Erwachsenen anlegen -- stirbt ein Junges, entsteht eine Leiche |

**Was heisst das fuer "scheu, kommt naeher, wenn man Futter hat"?** Zwei belegbare Bauarten:
- (W) **wild = true, canBeDomesticated = true** (Vorbild Waschbaer): das Junge ist echt scheu (flieht unter 3 Kacheln immer), die Engine
  laesst es nicht hungern, niemand kann es ueber das Vanilla-Menue toeten. Zaehmen muss dann aus der Entfernung beginnen oder unser Code
  haelt es mit `getBehavior():setBlockMovement(true)` (BELEGT `V:ISAnimalContextMenu.lua:89`) bzw. `stopAllMovementNow()` (`:760`) fest,
  solange der Spieler ruhig mit Futter herankommt. Beim Zaehmen `animal:setWild(false)` (BELEGT). Achtung: in einer Tierzone macht die
  Engine von selbst `setWild(false)` (Jar `checkZone`, dec/IsoAnimal.java:600-613).
- (Z) **wild = false, alwaysFleeHumans = false** (wie der heutige Baer): weicht nur manchmal aus, Akzeptanz steigt schon von selbst, wenn
  ein Spieler in 10 Kacheln steht (dec/BaseAnimalBehavior.java:1551-1559) -- weniger "scheu", dafuer nichts festzuhalten. Scheu muesste
  dann unser Code spielen (`animal:fleeTo(sq)`, BELEGT `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38` `self.animal:fleeTo(sq);`, rennt immer).
- "Naeher kommen": Vanillas Locken (`ISLureAnimal`, `V:shared/TimedActions/Animals/ISLureAnimal.lua:22` `self.character:lureAnimal(self.item)`)
  geht nur mit Obst/Gemuese/Tierfutter/Milch (oben) und nur, wenn die Definition den Typ fuehrt; es wirkt laut Jar auch bei wilden Tieren
  (`tryLure` hat keine wild-Frage, dec/IsoAnimal.java:2541-2573). Mit Honig/Fisch bleibt nur der eigene Weg: `animal:pathToLocation(x, y, z)`
  (Kevins Ausnahme vom 08.11., Jar-Beleg, Riegel, pcall, Gegenprobe; am Zombie belegt `V:DebugContextMenu.lua:636`) oder `fleeTo` (rennt).
  **Entscheidung W oder Z gehoert Kevin bzw. dem Planer** (offener Punkt O1).

---

## 3. Wald erkennen, Platz ausser Sicht waehlen

| Bedarf | Aufruf | Fundstelle | Seite |
|---|---|---|---|
| Zonen einer Kachel (alle) | `getWorld():getMetaGrid():getZonesAt(x, y, z)` -> Liste, je `zone:getType()` | `V:shared/Traps/TrapSystem.lua:12-16` `local mapZones = getWorld():getMetaGrid():getZonesAt(square:getX(), square:getY(), square:getZ());` ... `tempZoneType = tempZone and tempZone:getType();`; `V:client/Foraging/ISZoneDisplay.lua:327-334` | shared -> SP, Server, Client |
| Zone einer Kachel (eine) | `square:getZone()` -> `zone:getType()` | `V:shared/Traps/TrapSystem.lua:43` `modData.zone = square:getZone() and square:getZone():getType() or "TownZone"`; `B:server/BanditServerSpawner.lua:133-136`; `B:server/BanditServerWanderers.lua:670-675` (`if zoneType == "DeepForest" then`) | Server/SP |
| Wald-Namen | Texte `"Forest"`, `"DeepForest"`, dazu in B42 `"PHForest"`, `"PHMixForest"`, `"PRForest"`, `"FarmMixForest"`, `"FarmForest"`, `"BirchForest"`, `"BirchMixForest"`, `"OrganicForest"` | `V:shared/Foraging/forageZones.lua:3,27,72,79,91,98,110,122,129,140`; `V:server/metazones/BiomeMapConfig.lua:5-23`; Fallen-Zonen `V:server/Traps/TrapDefinition.lua:77-78` | Daten |
| Kachel geladen | `getCell():getGridSquare(x, y, z)` (nil = nicht geladen) | `B:server/BanditServerSpawner.lua:222-223`; `V:server/Traps/STrapSystem.lua:89` `getWorld():getCell():getGridSquare(luaObject.x, luaObject.y, luaObject.z)` | Server/SP |
| frei | `square:isFree(false)` | `B:server/BanditServerSpawner.lua:231` `elseif not square:isFree(false) then`; `V:client/ISUI/ISWorldObjectContextMenu.lua:2219` | Server/SP |
| fester Boden | `square:TreatAsSolidFloor()` | `B:server/BuildingObjects/ZSGuardposts.lua:12` `return square:TreatAsSolidFloor() and square:isFree(false)` | Server |
| nicht massiv | `square:isSolid() or square:isSolidTrans()` | `V:client/ISUI/ISWorldObjectContextMenu.lua:695` | Client belegt |
| kein Wasser | `square:getFloor()`, `floor:hasProperty(IsoFlagType.water)` | `V:client/ISUI/ISWorldObjectContextMenu.lua:687-688`; `NCBearSpawn.lua:30-33` | Client belegt, gleiche Methode Server |
| kein Baum auf der Kachel | `square:HasTree()` | `V:server/Foraging/forageServer.lua:276` | Server |
| draussen, kein Raum | `square:isOutside()`, `square:getRoom()` | `B:server/BanditServerSpawner.lua:152` `sp.outside = square:isOutside()`; `V:client/Challenge/AReallyCDDAy.lua:14` | Server / Client |
| kein Auto | `square:isVehicleIntersecting()` | `V:server/BuildingObjects/ISBuildUtil.lua:34` | Server |
| kein Safehouse | `SafeHouse.isSafeHouse(square, nil, true)` | `B:server/BanditServerSpawner.lua:229` | Server |
| Zufallspunkt im Ring um den Spieler | `ZombRandFloat(0, 2 * math.pi)`, `px + d * math.cos(theta)` | `B:server/BanditServerSpawner.lua:216-222` (16 Versuche) | Server |
| Abstand zu ALLEN Spielern | Schleife ueber die Spielerliste, Abstand < 35 = zu nah | `B:server/BanditServerSpawner.lua:175-184` | Server |
| Spielerliste | MP `getOnlinePlayers()` (`V:server/Foraging/forageServer.lua:463`, `B:server/BanditServerSpawner.lua:55`); SP `IsoPlayer.getPlayers()` (`B:...:57`) oder `getSpecificPlayer(0)` (`V:DebugContextMenu.lua:24`) | | Server / SP |
| Sichtlinie | `LosUtil.lineClear(cell, x1, y1, z1, x2, y2, z2, false)`, Ergebnis als Text gegen `"Blocked"` | `B:shared/BanditUtils.lua:1286-1290` `return tostring(LosUtil.lineClear(cell, x1, y1, z1, x2, y2, z2, false)) ~= "Blocked"`; Aufrufer `B:shared/ZombieActions/ZAShoot.lua:194` | Bandits ruft es auf dem CLIENT (Banditen-KI); auf dem dedizierten Server ungeprueft |
| Sichtbar fuer den Spieler | `square:isCanSee(playerIndex)` | `V:client/Foraging/ISBaseIcon.lua:256`, `V:client/Foraging/ISSearchManager.lua:722` | **nur Client/SP** (Spielerindex eines lokalen Spielers) |

Fallen:
- **"Ausser Sicht" kennt der dedizierte Server nicht** (kein Sichtfeld je Spieler). Belegt ist dort nur: Mindestabstand zu jedem Spieler
  (Bandits nimmt 35) plus Wald/draussen. `isCanSee` waere Client-Glauben -> nicht fuer die Server-Entscheidung benutzen. Im SP kann
  `isCanSee(0)` zusaetzlich gefragt werden.
- Obergrenze: nichts jenseits von rund 70 Kacheln ansprechen (CLAUDE.md: 76 geladen); `getGridSquare` gibt dort nil.
- `getZone()` liefert nur EINE Zone; liegt eine Ortszone ueber dem Wald, entscheidet `getZonesAt` (ganze Liste) sicherer.
- Suche teuer? 16 Versuche je Wurf wie Bandits, Wurf in grossen Abstaenden (Abschnitt 4) -- kein Flaechen-Scan je Bild.

---

## 4. Zeit und seltene Arbeit

| Bedarf | Aufruf | Fundstelle | Seite |
|---|---|---|---|
| Weltalter in Stunden / Tagen | `getGameTime():getWorldAgeHours()`, `/ 24` | `V:server/Traps/STrapSystem.lua:77` `luaObject.lastUpdate = getGameTime():getWorldAgeHours() / 24;`; `V:client/Challenge/WinterIsComing.lua:8` | Server/SP/Client |
| Stunde des Tages | `getGameTime():getHour()` | `V:server/Traps/STrapGlobalObject.lua:535` `local current = getGameTime():getHour()` | Server/SP |
| Uhrzeit als Kommazahl | `getGameTime():getTimeOfDay()` | `V:shared/Foraging/forageSystem.lua:1948` | shared |
| Nacht | `getClimateManager():getSeason()`, `season:getDawn()`, `season:getDusk()` | `V:shared/Foraging/forageSystem.lua:1944-1951` `if (timeOfDay < dawn) or (timeOfDay > dusk) then return "isNight"; end;` -- die fertige Funktion `forageSystem.getTimeOfDay()` liegt in `shared/` | shared (SP, Server, Client) |
| alle 10 Spielminuten / Stunde / Tag | `Events.EveryTenMinutes.Add(f)`, `Events.EveryHours.Add(f)`, `Events.EveryDays.Add(f)` | `V:server/Traps/STrapSystem.lua:132-134` (Datei beginnt mit `if isClient() then return end`, laeuft also SP und Server) | Server/SP |
| jede Spielminute | `Events.EveryOneMinute.Add(f)` | `V:server/Camping/SCampfireSystem.lua:183` | Server/SP |
| OnTick mit Echtzeit-Drossel | `Events.OnTick.Add(f)` + `getTimestampMs()` | `V:server/Foraging/forageServer.lua:455-461` `local now = getTimestampMs(); if now < forageServer._nextRelevanceMs then return; end;` und `:502` | Server; im SP ebenso (`V:DebugContextMenu.lua:1487`) |

Fallen: Abklingzeiten, die einen Neustart ueberleben sollen, in **Spielstunden** (`getWorldAgeHours`) speichern, nicht in `getTimestampMs`
(Echtzeit). `EveryDays` feuert um Mitternacht Spielzeit, nicht 24 h nach dem Ereignis -> "nach 1 bis 3 Naechten" ueber gemerkte
Weltalter-Stunden plus Nacht-Frage rechnen. Vanillas Fallen wuerfeln je Stunde nur, wenn die Kachel NICHT geladen ist
(`V:server/Traps/STrapGlobalObject.lua:391-403` "you won't find an animal if a player is near the trap") -- ein Tier erzeugen koennen wir
dagegen nur auf einer GELADENEN Kachel; ein Koederplatz kann also unbeobachtet "reif" werden (Register), das Junge entsteht erst, wenn die
Kachel wieder geladen ist und kein Spieler naeher als der Mindestabstand steht.

---

## 5. Daten halten

### 5.1 Globale ModData (das Register)

| Aufruf | Fundstelle | Seite |
|---|---|---|
| `ModData.getOrCreate("Name")` | `V:server/Foraging/forageServer.lua:26` `forageData = ModData.getOrCreate("forageData");`; `B:shared/BanditGMD.lua:17` | Server/SP (und Client fuer eine eigene Kopie) |
| im richtigen Moment holen | `Events.OnInitGlobalModData.Add(f)` | `V:server/Vehicles/ProfessionVehicles.lua:347`; `V:client/Foraging/forageClient.lua:9`; `B:shared/BanditGMD.lua:115` | beide |
| zum Client schicken | `ModData.transmit("Name")` | `V:server/Foraging/forageServer.lua:49` | Server |
| Client fragt an | `ModData.request("Name")` + `Events.OnReceiveGlobalModData.Add(function(key, data) ... end)` | `B:shared/BanditGMD.lua:18-20` und `:52-67`, `:116` (in keiner Vanilla-Lua-Zeile, NPC-Crew-Lehre `NPCCrew/CLAUDE.md:1880-1897`) | Client |
| loeschen | `ModData.remove("Name")` | `V:server/Foraging/forageServer.lua:33` | Server |

Fallen:
- Die Tabelle erst in `OnInitGlobalModData` holen und nie eine frueher geholte Referenz behalten (Jar `GlobalModData.init`: erst `load()`,
  dann das Ereignis, dec/GlobalModData.java:51-55).
- Ein ankommendes Paket ersetzt die Tabelle des Empfaengers NICHT von selbst, es feuert nur `OnReceiveGlobalModData` (NPC-Crew-Lehre
  oben). Gut fuer uns: registriert der SERVER keinen annehmenden Empfaenger fuer unseren Schluessel, kann kein Client das Register
  ueberschreiben. Aber: `ModData.request` darf jeder Client fuer jeden Schluessel -> nichts Geheimes hinein.
- Ein MP-Client schreibt seine ModData nie auf die Platte (NPC-Crew-Lehre `CLAUDE.md:1898-1903`): Anzeige-Einstellungen je Spieler gehoeren
  nicht hierher.
- Deckel: je Spieler ein Eintrag, Koederplaetze und wilde Junge gedeckelt; alte Eintraege (tot, verschwunden) raeumen.
- Einfacher als das ganze Register zu uebertragen: dem betroffenen Spieler nur seine Zahlen per `sendServerCommand` schicken (Abschnitt 6).

### 5.2 ModData am Tier und ihr Abgleich

- Lesen/Schreiben BELEGT (1.2). Gespeichert mit dem Tier (1.4). Beim Stufenwechsel der Engine ginge sie verloren -- das Junge hat keine
  naechste Stufe; fuer das spaetere Wachsen liegt die Wahrheit deshalb im Register (Auftrag).
- **Zum Client kommt sie nicht laufend.** Jar: das laufende Tierpaket traegt Alter, Gewicht, Stress, Durst, Hunger, Gesundheit, Name; ModData
  nur in der Vollantwort (alte Recherche `recherche_spiel.md` Abschnitt 5, am 42.22-Jar nicht neu vermessen -> "ungeprueft, wie oft").
- `animal:transmitModData()` hat am TIER keine Fundstelle (grep `transmitModData`: nur Tueren und Spieler, z. B.
  `V:client/Hotbar/ISHotbar.lua:677` `self.chr:transmitModData()`). Am Tier **nicht benutzen**; laut `KRITIK.md` K3 kann zudem jeder Client
  die ModData eines Objekts ueberschreiben. Spiegel = der Server schreibt am Tier (fuer Speichern/Wiederfinden), die Anzeige bekommt der
  Client per `sendServerCommand`.
- Vorschlag Schluessel am Tier: ein vom Server vergebener Text (z. B. laufende Nummer aus dem Register), dazu Besitzer-Kennung. Die
  AnimalID nur als Gegenprobe (0.4).

### 5.3 Spielerkennung

| Kennung | Fundstelle | Stabil? |
|---|---|---|
| `player:getUsername()` | `V:shared/Traps/TrapSystem.lua:45` `modData.player = player:getUsername()` (Vanilla merkt so den Fallensteller, Vergleich `V:server/Traps/STrapGlobalObject.lua:219`); `V:server/Foraging/forageServer.lua:70-72` `return _player and (_player:getUsername() or _player:getDisplayName());` | MP: Kontoname, ueber Neustarts stabil -> **der Schluessel im MP** |
| `player:getOnlineID()` | `V:shared/Fishing/FishingRod.lua:354`; Gegenstueck `getPlayerByOnlineID(id)` `V:client/ServerCommands.lua:10` | NEIN: Nummer je Verbindung, wird wiederverwendet (`NC:shared/BanditsNPC.lua:6268-6275`) -- nur fuer "wer ist das gerade" |
| Steam-ID am Spieler | **nicht gefunden** (grep `:getSteamID()`: nur `bannedSteamID:getSteamID()` in `V:client/ISUI/AdminPanel/ISBannedSteamIDViewer.lua:106`; `getSteamIDFromUsername` / `getCurrentUserSteamID`: 0 Lua-Treffer, nur Jar) | nicht benutzen |
| Einzelspieler | fester Schluessel (NPC Crew nimmt 1, `NC:shared/BanditsNPC.lua:6288-6312`; Bandits `B:shared/BanditUtils.lua:668`) | der Name kann sich nach dem Tod der Figur aendern (PLAN.md Abschnitt 3) -> im SP nie den Namen nehmen |

**Engine-Falle:** die Akzeptanz eines Tiers haengt an der OnlineID (Jar `playerAcceptanceList` ist `HashMap<Short, Float>`, Schluessel
`chr.getOnlineID()`, dec/IsoAnimal.java:177, 2529-2535, gespeichert :1329-1334). Im MP kann sie nach einer Neuverbindung bei einem
anderen Spieler landen oder fuer den Besitzer weg sein. Der Zaehm-Balken darf also NIE die Engine-Akzeptanz sein -- er steht im Register
(Abschnitt 10).

---

## 6. Client <-> Server

| Richtung | Aufruf | Fundstelle | Wer empfaengt im SP |
|---|---|---|---|
| Client -> Server | `sendClientCommand(playerObj, "modul", "befehl", args)` | `V:client/DebugUIs/DebugContextMenu.lua:956` `sendClientCommand(playerObj, 'bbq', 'setFuel', args)` | Jar: im SP geht es ueber `SinglePlayerClient.sendClientCommand` und feuert `OnClientCommand` im selben Programm (dec/SinglePlayerServer.java:176-201) -- ueber eine Paket-Warteschlange, also nicht im selben Aufruf (wann genau: ungeprueft); args werden dabei wie ueber das Netz gepackt -> **nur Zahlen, Texte, Wahrheitswerte, Tabellen** |
| Server nimmt an | `Events.OnClientCommand.Add(function(module, command, player, args) ... end)` | `V:server/ClientCommands.lua:1346-1357`; `V:server/Foraging/forageServer.lua:56-68` (filtert zuerst `if _module ~= "forageData" then return; end`) | derselbe Rechner |
| Server -> ein Client | `sendServerCommand(playerObj, "modul", "befehl", args)` | `V:server/BuildingObjects/ISBuildUtil.lua:291` `sendServerCommand(playerObj, 'ui', 'dirtyUI', { });`; `V:shared/Fishing/FishingRod.lua:353-356` (`if isServer() then ... sendServerCommand(self.player, 'fishing', 'consumeLure', args)`) | **niemand**: Jar `sendServerCommand` tut ausserhalb von `GameServer.server` nichts (javap LuaManager_GlobalObject Offset 0-12). Im SP die Empfaenger-Funktion DIREKT rufen |
| Server -> alle | `sendServerCommand("modul", "befehl", args)` | `V:shared/TimedActions/ISPickupDung.lua:45`; `V:server/BuildingObjects/ISEmptyGraves.lua:47` | wie oben |
| Client nimmt an | `Events.OnServerCommand.Add(function(module, command, args) ... end)` | `V:client/ServerCommands.lua:207-218` (Datei beginnt mit `if not isClient() then return end`) | - |
| Tier benennen | Client: `animal:getOnlineID()`; Server: `getAnimal(tonumber(args.id))` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:432`; `V:server/ClientCommands.lua:817` | im SP 1.2 beachten (frisches Tier ohne OnlineID-Eintrag) |
| Spieler benennen | `player:getOnlineID()` / `getPlayerByOnlineID(id)` | `V:shared/Fishing/FishingRod.lua:354`; `V:client/ServerCommands.lua:10` | |

Fallen:
- **Welche Datei laeuft wo:** `server/`-Dateien laden auch im SP und auf MP-Clients. Riegel fuer "SP und Server": `if isClient() then return end`
  (`V:server/Traps/STrapSystem.lua:1`). **Nicht** `if not isServer() then return end` (`V:server/Foraging/forageServer.lua:1`) -- das schliesst
  den Einzelspieler aus.
- Der Server prueft bei JEDER Bitte selbst (Besitz, Abstand, Abklingzeit, Grenzen); nichts aus den args glauben ausser der Benennung.
  Das Tier beim Server ueber OnlineID holen UND Art (`getAnimalType() == "ncbearcub"`) und eigenen Schluessel in der ModData gegenpruefen.
- Beide Befehlswege sind zuverlaessig zugestellt (NPC-Crew-Lehre `CLAUDE.md:3196-3200`); "keine Antwort" heisst Verbindungsabbruch.
- Auf dem Client hat `getAnimal(id)` keine Fundstelle (nur `server/ClientCommands.lua`) -> dort die Kopie ueber
  `getCell():getObjectListForLua()` und `getOnlineID()` suchen (beides Client-belegt).
- **Am wenigsten Eigenbau:** Fuettern und Streicheln als Zeitaktionen (Abschnitt 8) -- die Engine traegt Spieler, Tier und Gegenstand
  selbst zum Server; eigene Befehle braucht es dann nur fuer die Anzeige (Fortschritt an den Client) und fuer Meldungen.

---

## 7. Rechtsklick auf ein Tier

### 7.1 Wie Vanilla das Tier-Menue fuellt

- `ISWorldObjectContextMenu.createMenu` sammelt die angeklickten Objekte (`V:client/ISUI/ISWorldObjectContextMenu.lua:186-188`
  `ISWorldObjectContextMenuLogic.fetch(fetch, v, player, true)`; `fetch.clickedAnimals = {}` in `:43`). Die Logik ist eine Java-Klasse
  (Jar `zombie.iso.ISWorldObjectContextMenuLogic`): sie traegt jedes `IsoAnimal` der angeklickten Kachel und der Nachbarkacheln in
  `clickedAnimals` ein und feuert in `createMenuEntries` das Ereignis **`OnClickedAnimalForContext`** mit (Spielernummer, Menue, Tabelle der
  Tiere, test) (javap ISWorldObjectContextMenuLogic Offset 3372-3416).
- Vanilla haengt sich so an: `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1013-1017` und `:1235`
  `AnimalContextMenu.clickedAnimals = function(player, context, animals, test)` / `for i,v in ipairs(animals) do AnimalContextMenu.doMenu(player, context, v, test); end` /
  `Events.OnClickedAnimalForContext.Add(AnimalContextMenu.clickedAnimals);`
- `doMenu` (`:132-151`) legt je Tier einen Eintrag mit dem Namen `animal:getFullName()` an (`:140-141`) und darunter ein Untermenue.

### 7.2 Eigener Eintrag fuer EINE Tierart, ohne Vanilla zu aendern

| Schritt | Aufruf | Fundstelle |
|---|---|---|
| anhaengen | `Events.OnClickedAnimalForContext.Add(function(player, context, animals, test) ... end)` | `V:ISAnimalContextMenu.lua:1235` (gleiche vier Argumente) |
| Art filtern | `v:getAnimalType() == "ncbearcub"` | `V:client/ISUI/Animal/ISAnimalUI.lua:65`; `NCBearSpawn.lua:69` |
| Spieler | `getSpecificPlayer(player)` | `V:ISAnimalContextMenu.lua:134` |
| eigener Punkt (oberste Ebene) | `context:addOption(text, ziel, funktion, arg...)` | `V:ISAnimalContextMenu.lua:13`, `:287` |
| ODER ins Vanilla-Untermenue des Tiers | `context:getOptionFromName(animal:getFullName())`, dann `context:getSubMenu(option.subOption)` | `V:client/Tutorial/Tutorial1.lua:131` `if not context:getOptionFromName(text) then`; `V:client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:41` `shovelSubMenu = context:getSubMenu(shovelOption.subOption);` |
| Vanilla-Punkt fuer unser Tier ausblenden | `untermenue:removeOptionByName(name)` | reine Lua-Funktion `V:client/ISUI/ISContextMenu.lua:1016` (kein Engine-Aufruf) |
| gesperrter Punkt mit Erklaerung | `option.notAvailable = true`, `ISWorldObjectContextMenu.addToolTip()`, `tooltip:setName(text)`, `option.toolTip = tooltip` | `V:ISAnimalContextMenu.lua:160-163` |
| Symbol | `option.iconTexture = getTexture("media/ui/AnimalActions_Pet.png")` | `V:ISAnimalContextMenu.lua:288` |
| Umriss beim Ueberfahren | `option.onHighlight` mit `_animal:setOutlineHighlight(_menu.player, true)` | `V:ISAnimalContextMenu.lua:143-148` |

Fallen:
- Unser Empfaenger laeuft NACH Vanillas (Vanilla-Datei laedt zuerst) -> das Untermenue existiert schon. Trotzdem auf nil pruefen
  (`getOptionFromName` findet nichts, wenn zwei gleichnamige Tiere angeklickt sind oder der Name sich aendert).
- `test == true` (Controller-Probe): nichts tun bzw. wie Vanilla frueh zurueck (`V:client/ISUI/Hutch/ISHutchMenu.lua:4`).
- `OnFillWorldObjectContextMenu` waere der zweite Weg (`V:ISWorldObjectContextMenu.lua:213`), kennt die Tiere aber nur ueber
  `ISWorldObjectContextMenu.fetchVars.clickedAnimals` -- der Tier-Ereignisweg ist der direktere.
- Das Menue ist reiner Client. Es darf nur ANBIETEN; ob Fuettern/Streicheln gilt, entscheidet der Server in `complete()` (8.2).

### 7.3 Was das Vanilla-Untermenue bei unserem Jungen von selbst zeigt

Animal info (bei wild gesperrt, `:166-171`), Attach (nur bei `canBeAttached`, `:173`), Pick up (nur bei `canBePicked(player)`, `:265`),
Lure (nur wenn `getPossibleLuringItems` etwas liefert, `:270-284`), Pet (nur bei `canBePet`, `:286`), Water/Feed (nur ab Durst/Hunger 0,1,
`:300-305`), Kill (nur wenn NICHT wild, `:307-324`). **Zwei Vanilla-Wege brauchen ein Attachment `head` am Modell:** `onPetAnimal`
(`:750-757` `local vec = animal:getAttachmentWorldPos("head"); if not vec then return; end`) tut ohne es still nichts, `onFeedAnimalFood`
(`:91-92`) reicht ein nil an `ISWalkToTimedActionF` weiter (wirft dort in `start`, `V:client/TimedActions/WalkToTimedActionF.lua:41`).
Unser Baerenmodell hat kein `attachment head` (`nc_bear_tier.txt`); Vanilla-Tiere mit Streicheln haben es
(`media/scripts/generated/models_animals.txt:9-14` `attachment head { offset = ..., rotate = ..., bone = Dummy01, }`). Also entweder
`canBePet` weglassen und nur den eigenen Punkt bieten, oder dem Modell-Skript des Jungen ein `attachment head` geben (Naht zum Lauf
baer-junges).

---

## 8. Zeitaktion: Streicheln und Fuettern

### 8.1 Vanilla-Streicheln ganz gelesen (`V:shared/TimedActions/Animals/ISPetAnimal.lua`, 102 Zeilen)

- `isValid` (`:5-7`): `self.character:getSquare():DistTo(self.animal:getSquare()) < 3`.
- `waitToStart` (`:9-12`): `faceThisObject(self.animal)`, `return self.character:shouldBeTurning()`.
- `update` (`:14-18`): Spieler und Tier schauen sich an (`self.animal:faceThisObject(self.character)`), `setIsAiming(false)`.
- `start` (`:20-44`): `forceDropHeavyItems` (nicht auf dem Client), `setOverrideHandModels(nil, nil)`, Variablen am SPIELER
  `AnimalSizeX` 0.01, `AnimalSizeY` (Groessenanteil), `petanimal` true, `animal` = Tierart (`:39`); am TIER
  `getBehavior():setBlockMovement(true)` (`:36`) und `setVariable("idleAction", "petting")` (`:43`).
- `forceStop` / `stop` / `perform` (`:46-67`): `petanimal` false, `self.animal:clearVariable("idleAction")`, `setBlockMovement(false)`.
- `complete` (`:69-72`): `self.animal:petAnimal(self.character); return true`.
- `getDuration` (`:74-79`): 400. `serverStart` (`:81-84`): `emulateAnimEventOnce(self.netAction, 3000, "pettingFinished", nil)`.
- `animEvent` (`:86-93`): bei `"pettingFinished"` `petAnimal` und (nicht auf dem Server) `forceStop`.
- `new(character, animal)` (`:95-102`): `useProgressBar = false`, `stopOnAim = false`.
- Start aus dem Menue: `V:ISAnimalContextMenu.lua:750-757` (Sperre setzen, zum Kopf gehen, Aktion anhaengen).
- Spieler-Animation: Knoten in `media/AnimSets/player/petanimal/`. Fuer eine unbekannte Tierart greift `defaultpet.xml` (keine
  Bedingung, Clip `Bob_PetBull`, Ereignis `pettingFinished` am Ende). Niedrige Tiere haben eigene Knoten mit Bedingung `animal` = Art
  (z. B. `petraccoonkit.xml`, `petlamb.xml`). Vanilla setzt die Variable selbst auf eine ANDERE Art (`:41`
  `self.character:setVariable("animal", self.animal:getBabyType())`) -> eine eigene Aktion darf `"animal"` auf z. B. `"raccoonkit"` setzen,
  damit sich die Figur zu einem 40 cm hohen Jungen hinunterbeugt. Wie das aussieht: ungespielt.
- Tier-Seite: `idleAction = "petting"` braucht einen Knoten im Animset `buck`; den gibt es dort nicht (Rehe werden nicht gestreichelt) ->
  das Junge steht einfach still. Eigener Knoten (wie die `NCBear_*.xml`) waere ein Zusatz, kein Muss.

Was `petAnimal` tut (Jar dec/IsoAnimal.java:2470-2483): nur ausserhalb eines MP-Clients und nur bei `petTimer == 0`: Stress -7..-11 (minus
Tierhaltung), **Akzeptanz +2..6**, `petTimer` = 15000..25000 minus Tierhaltung*200 (zaehlt je Durchlauf um den Zeit-Multiplikator herunter,
dec/IsoAnimal.java:439-445; Umrechnung in Minuten ungeprueft), XP Tierhaltung 5..9. Die Vanilla-Abklingzeit ist also eingebaut, aber
nirgends sichtbar (nur im Cheat-Menue, `V:ISAnimalContextMenu.lua:289-297`); `animal:petTimerDone()` ist BELEGT (`:289`).

### 8.2 Aufbau einer B42-Zeitaktion und was im MP wo laeuft

Belegt durch die beiden Vanilla-Dateien oben und `V:shared/Camping/TimedActions/ISAddFuelAction.lua`; die Mechanik dahinter aus dem Jar
(dec/LuaTimedActionNew.java, dec/NetTimedAction.java -- Lesehilfe):

| Funktion | SP | MP-Client | MP-Server |
|---|---|---|---|
| `new(character, ...)` | ja | ja | **ja, neu gebaut**: der Server ruft `<Type>.new(Klasse, args...)` mit den uebertragenen Werten |
| `isValid` | laufend | laufend | **nie** (`NetTimedAction.isValid` gibt false zurueck und wird nicht gefragt) |
| `waitToStart`, `start`, `update`, `stop`, `perform` | ja | ja (Bild, Ton, Sperren) | nein |
| `serverStart`, `serverStop`, `animEvent` (emuliert) | nein | nein | ja |
| `getDuration` | Ticks | Ticks (wird vom Server ueberschrieben) | ja; der Server rechnet den Wert mal 20 als Wartezeit bis `complete` (Lesart: Millisekunden) |
| `complete` | **ja, nach `perform`** | **nein** | **ja** -- Rueckgabe true = erledigt, false = abgelehnt (Client bricht ab) |

Pflichten fuer eine EIGENE Aktion (alle aus dem Jar gelesen, an den Vanilla-Aktionen sichtbar erfuellt):
1. Datei in `shared/` (Server und Client brauchen die Klasse), abgeleitet mit `ISBaseTimedAction:derive("Name")`.
2. **Die Klasse muss eine GLOBALE Variable mit genau dem Namen ihres Typs sein** (der Server sucht `LuaManager.get(type)` und
   `type .. ".new"`, dec/NetTimedAction.java `parse`). Also z. B. `BanditsNPCBearFeedAction = ISBaseTimedAction:derive("BanditsNPCBearFeedAction")`
   -- nicht als Feld von `BanditsNPC.Bear`. Namen vorher in NPC Crew und Vanilla greppen.
3. **Die Parameternamen von `new` muessen so heissen wie die Felder am Objekt** (der Client liest je Parameter `action[paramName]`,
   dec/NetTimedAction.java `set`): `function X:new(character, animal, food)` braucht `o.character`, `o.animal`, `o.food`.
4. Uebertragbare Werte: Spieler, `IsoAnimal` (ueber die OnlineID), `InventoryItem` (ueber Behaelter + Gegenstands-ID, der Server holt
   SEIN Stueck mit `getItemWithID`, sonst nil), Zahlen, Texte, Wahrheitswerte (dec/PZNetKahluaTableImpl.java). Kein Funktionswert.
5. `o.maxTime = o:getDuration()` in `new` (`V:ISPetAnimal.lua:98`); `stopOnWalk`/`stopOnRun` wie `V:ISFeedAnimalFromHand.lua:71-72`.
6. **Alle Pruefungen gehoeren in `complete()`**, weil der Server `isValid` nie fragt: Tier noch da und richtige Art, Abstand, Gegenstand
   noch im Inventar DIESES Spielers, Abklingzeit, Besitz/Grenzen. Vanilla-Vorbild: `V:shared/TimedActions/Animals/ISPickupAnimal.lua:41-44`
   `function ISPickupAnimal:complete() if not self:isValid() then return false end`.
7. `complete()` laeuft im SP im selben Programm -> derselbe Code fuer SP und Server; `isClient()`-Zweige nur fuer Bild und Ton.

Hingehen zum Tier (alles Client, vor der Aktion in die Warteschlange):
- `luautils.walkAdj(player, animal:getSquare())` (`V:ISAnimalContextMenu.lua:90`) -- braucht kein Attachment; oder
- `ISTimedActionQueue.add(ISWalkToTimedActionF:new(player, vec))` mit `vec = animal:getAttachmentWorldPos("head")` (`:91-92`) -- nur mit `head`.
- Futter in die Hand: `ISWorldObjectContextMenu.transferIfNeeded(playerObj, item)` (`:577`) und
  `ISWorldObjectContextMenu.equip(player, player:getPrimaryHandItem(), food, true, false)` (`:93`).
- Tier festhalten, solange der Spieler kommt: `animal:getBehavior():setBlockMovement(true)` (`:89`); in JEDEM Ausgang wieder loesen
  (`V:ISFeedAnimalFromHand.lua:27-47` loest in forceStop, stop, perform UND complete). Die Sperre wird nicht gespeichert, bleibt aber bis
  zum Entladen haengen, wenn ein Ausgang sie vergisst -> der Server-Takt sollte verwaiste Sperren an unseren Jungen loesen (wie
  `NCBearFight.lua:1772-1777`).

### 8.3 Fuettern: Vanilla-Vorbild und der sichere Verbrauch

`V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua` (74 Zeilen): `isValid` (`:5-7`) `self.character:getInventory():contains(self.food)`;
`start` (`:13-25`) `setActionAnim(self.animal:getFeedByHandAnim())`, `setOverrideHandModels(self.food, nil)`, Sperre, Ton
`playSound("GiveFoodAnimal")`; `complete` (`:45-51`) `self.animal:feedFromHand(self.character, self.food)` und
`sendFeedAnimalFromHand(self.animal, self.character, self.food)`; Dauer 150 (`:53-58`).

**`feedFromHand` taugt NICHT als unser Verbrauch** (Jar dec/IsoAnimal.java:2452-2464, dec/AnimalData.java:1035-1203):
- es ruft `AnimalData.eatItem(food, false)`. Das entfernt den Gegenstand nur, wenn der HUNGER des Tiers mindestens so gross ist wie der
  Naehrwert (`doesItemSatisfyHunger`, :1031-1033); sonst wird das Futter nur "angebissen" (`setHungChange`) und bleibt im Inventar.
  Bei einem Tier ohne Hunger (wild, oder `hungerMultiplier` 0) passiert am Gegenstand **nichts** -- die Akzeptanz steigt aber trotzdem um
  1..3. Mit einem einzigen Fisch liesse sich so endlos zaehmen.
- Daraus: unsere Aktion verbraucht selbst, genau ein Stueck, in `complete()`:

| Schritt | Aufruf | Fundstelle |
|---|---|---|
| noch da? (Server/SP) | `self.food ~= nil` und `self.character:getInventory():contains(self.food)` | `V:ISFeedAnimalFromHand.lua:6`; ID-Form `containsID(self.item:getID())` `V:shared/Camping/TimedActions/ISAddFuelAction.lua:12` |
| aus der Hand | `self.character:removeFromHands(self.food)` | `V:ISAddFuelAction.lua:66` |
| entfernen | `self.character:getInventory():Remove(self.food)` | `V:ISAddFuelAction.lua:67` |
| Clients informieren | `sendRemoveItemFromContainer(self.character:getInventory(), self.food)` | `V:ISAddFuelAction.lua:68` (alle drei Zeilen stehen dort in `complete()`) |

  Reihenfolge fuer "kein Verlust, keine Verdopplung": erst ALLE Pruefungen (Tier, Abstand, Abklingzeit, Grenzen), dann entfernen, dann
  den Fortschritt gutschreiben -- alles in einem Aufruf ohne Wurf dazwischen (Mehrfachrueckgaben vorher in Locals holen). Lehnt eine
  Pruefung ab: `return false`, nichts ist verbraucht. Im MP ist `self.food` das Stueck des SERVERS; ist es nil (schon weg), ablehnen.
  Steckt das Futter in einer Tasche, bringt `transferIfNeeded` es vorher ins Hauptinventar (Client-Seite, eigene Vanilla-Aktion).
- Angebrochenes: wer nur einen Teil verfuettern will, braeuchte `item:setHungChange(x)` (BELEGT `V:server/Traps/STrapGlobalObject.lua:314`)
  plus Abgleich (`syncItemFields(character, item)`, `V:shared/Farming/TimedActions/ISWaterPlantAction.lua:120`). Einfacher und sicherer fuer
  B1a: ein ganzes Stueck je Fuetterung.
- Soll die Engine-Akzeptanz mitsteigen (fuer den spaeteren Q-Ruf), kann `complete()` zusaetzlich `self.animal:petAnimal(self.character)` bzw.
  beim Fuettern `feedFromHand` NACH dem eigenen Entfernen nicht mehr rufen (der Gegenstand ist dann aus dem Behaelter; `eatItem` fasst
  `item.getContainer()` an) -> fuer die Akzeptanz beim Fuettern gibt es dann keinen sauberen belegten Weg ausser dem Streicheln
  (Abschnitt 10, offener Punkt O3).

---

## 9. Futter erkennen, Koeder am Boden

### 9.1 Honig und Fisch

| Was | Beleg | Erkennen in Lua |
|---|---|---|
| Honig | `media/scripts/generated/items/food.txt:13071-13092` `item Honey` (ItemType base:food, `Spice = true`, `HungerChange = -20.0`, kein FoodType); einziger Honig-Gegenstand (grep `item .*[Hh]oney`: 1 Treffer) | `item:getFullType() == "Base.Honey"` (`getFullType`: `V:ISAnimalContextMenu.lua:55`, Vergleich `V:client/ISUI/ISBBQMenu.lua:112`) |
| gefangener Fisch (20 Arten im Skript, 21 Eintraege in `Fishing.fishes`) | `food.txt:7080-7108` `item LargemouthBass` ... `Tags = base:fishmeat;base:uncutfish`, `OnCreate = Fishing.onCreateFish` | Vanillas eigene Liste: `Fishing.fishes` (`V:shared/Fishing/fishing_properties.lua:216-237`, je Eintrag `.itemType`, z. B. `"Base.LargemouthBass"`) -- reine Lua-Tabelle, einmal in eine Menge umfuellen |
| Lachs, Fischfilet | `food.txt:6935-6959` `item Salmon` (FoodType Fish, Tags fishmeat;uncutfish), `:6834` `FishFillet` | `item:getFoodType() == "Fish"` (`getFoodType`: `V:ISAnimalContextMenu.lua:37`, `:64`); trifft auch Dosen-Sardinen/Thunfisch offen, Fischstaebchen, gebratenen Fisch |
| Tag statt Liste | `item:hasTag(ItemTag.X)` ist BELEGT (`V:client/Fishing/FishingHandler.lua:38` `primaryHandItem:hasTag(ItemTag.FISHING_ROD)`); die Konstante `ItemTag.FISH_MEAT` steht aber in keiner Lua-Zeile, nur im Jar (`zombie.scripting.objects.ItemTag`) | nur hinter `if ItemTag.FISH_MEAT then`; die Liste oben braucht das nicht |
| essbar, nicht verdorben | `instanceof(item, "Food")`, `item:getHungerChange() < 0`, `not item:isRotten()` | `V:ISAnimalContextMenu.lua:37`; `V:client/ISUI/ISInventoryPane.lua:990` (dazu `isBurnt`) |
| frisch / gefroren / gekocht | `item:isFresh()`, `item:isFrozen()`, `item:isCooked()` | `V:client/Farming/CFarming_Interact.lua:9`; `V:client/ISUI/Animal/ISButcherHookUI.lua:571`; `V:CFarming_Interact.lua:7` |
| im Inventar suchen | `playerObj:getInventory():getAllEvalRecurse(function(item) ... end)` | `V:ISAnimalContextMenu.lua:33-42` (Client, fuer das Menue) |

Fallen: Honig ist ein Gewuerz (`isSpice()`), Vanillas Futterfilter schliesst ihn aus -- unser eigener Filter darf das nicht uebernehmen.
`getFoodType()` ist bei den gefangenen Fischen leer (kein FoodType im Skript) -> ohne `Fishing.fishes` wuerden Barsch und Wels nicht erkannt.
Verdorbener Fisch: Entscheidung Bau (ablehnen mit Text ist ehrlicher als fressen lassen).

### 9.2 Koeder am Boden lesen und entfernen

| Schritt | Aufruf | Fundstelle | Seite |
|---|---|---|---|
| Bodengegenstaende einer Kachel | `square:getWorldObjects()`, `wobs:get(i)`, `o:getItem()`, `:getFullType()` | `V:client/ISUI/ISBBQMenu.lua:109-112` | Client belegt; gleiche Methoden auf dem Server |
| vom Gegenstand zum Bodenobjekt | `item:getWorldItem()` | `V:server/BuildingObjects/ISBuildUtil.lua:167` `local worldObj = item:getWorldItem()` | Server |
| entfernen (Server -> alle) | `worldObj:getSquare():transmitRemoveItemFromSquare(worldObj)` | `V:server/BuildingObjects/ISBuildUtil.lua:169`; `V:shared/BuildingObjects/TimedActions/ISMultiStageBuild.lua:133-135` (in `complete`) | Server/SP |
| dazu lokal | `sq:removeWorldObject(worldItem)`, `item:setWorldItem(nil)` | `V:shared/Moveables/ISMoveableSpriteProps.lua:2013-2015` | Server/SP |
| ablegen | `square:AddWorldInventoryItem(item, x, y, z)` | `V:client/DebugUIs/Scenarios/FenrisScenario.lua:8` (Gegenstand als Objekt), `Trailer3Scenario.lua:240` (als Text) | nur in Debug-Szenarien belegt -> fuer uns nicht noetig, wenn der Spieler ueber die Vanilla-Ablage ablegt |

**Kein Verlust dessen, was der Spieler nicht hergab:** ein Bodenscan, der jeden herumliegenden Fisch frisst, waere genau das. Sicherer
Weg: der Koederplatz entsteht nur durch eine ausdrueckliche Spieler-Handlung (eigene Zeitaktion "als Koeder auslegen": verbraucht das
Stueck in `complete()` wie 8.3 und traegt den Platz ins Register ein). Soll der Koeder sichtbar liegen, merkt das Register die
Gegenstands-ID des abgelegten Stuecks (`item:getID()`, `V:ISAddFuelAction.lua:12`) und der Server entfernt spaeter NUR dieses eine
Bodenobjekt; fehlt es (aufgehoben, verrottet), verfaellt der Platz ohne Ersatz. Bodenobjekte verrotten und koennen von anderen Mods/NPCs
aufgehoben werden -> die unsichtbare Variante (Gegenstand verbraucht, Platz nur im Register, Hinweis-Text) ist die robusteste. Entscheidung
gehoert dem Planer (offener Punkt O4). Vorbild fuer "Koeder + Zone + Stundenwurf": `V:server/Traps/STrapGlobalObject.lua:368-420`.

---

## 10. Akzeptanz: hebt ein ehrlicher Vanilla-Weg sie, so dass das Tier auf den Ruf kommt?

**Ja.** Belegt und im Jar nachgelesen:

| Weg | Lua-Beleg | Wirkung laut Jar |
|---|---|---|
| Streicheln `animal:petAnimal(character)` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:70` `self.animal:petAnimal(self.character);` (in `complete`, also Server/SP) | Akzeptanz +2..6, Stress -7..-11, nur bei abgelaufenem `petTimer`, nie auf einem MP-Client (dec/IsoAnimal.java:2470-2483) |
| Fuettern `animal:feedFromHand(character, food)` | `V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:47` | Akzeptanz +1..3, Stress -1..-4; frisst nur bei Hunger (8.3) |
| Naehe (nur NICHT wild) | kein Aufruf noetig | je Durchlauf +0,0005..0,0006 x (100 - Stress)/100 x Multiplikator, wenn ein Spieler in 10 Kacheln steht (dec/BaseAnimalBehavior.java:1551-1559) |
| lesen `animal:getPlayerAcceptance(playerObj)` | `V:client/ISUI/Animal/ISAnimalUI.lua:323` `local playerAcceptance = self.animal:getPlayerAcceptance(self.chr);` | gerundeter Wert; neuer Spieler startet zufaellig bei 0..20 |
| Ruf | kein Aufruf noetig | `respondToSound`: ruft der Spieler (`callOut`) und ist `getPlayerAcceptance(player) >= 40`, laeuft das Tier per `pathToLocation` zu ihm -- auch ein wildes (dec/IsoAnimal.java:764-800); sonst flieht es vor dem Laerm |

Rechnung (Jar-Zahlen, ungespielt): Start 0..20, Schwelle 40, je Streichler +2..6 -> im Mittel etwa 7 Streichler (zwischen 4 und 20),
jeder durch die Vanilla-Abklingzeit getrennt.

Grenzen und Verbote:
- **`setDebugAcceptance(player, wert)`** ist zwar Lua-belegt (`V:ISAnimalContextMenu.lua:614`, `V:server/ClientCommands.lua:1021` hinter
  `Capability.AnimalCheats`), aber nur als Debug-/Cheat-Weg; Kevin hat ihn fuer NPC Crew ausgeschlossen (ENTSCHEIDUNGEN.md 08.11. ~19:40).
  Nicht benutzen. (Am Rande: `petAnimal` und `feedFromHand` rufen intern genau diese Methode -- der ehrliche Weg IST also derselbe Speicher.)
- **`addAcceptance(player, x)`** gibt es nur im Jar (dec/IsoAnimal.java:2441-2450), grep in Vanilla-Lua und Bandits: 0 -> VERBOTEN ohne Kevins Wort.
- Die Akzeptanz haengt an der OnlineID (5.3) -> im MP kein Besitzmerkmal, und nach einer Neuverbindung kann der Ruf fuer den Besitzer
  wieder ausbleiben, bis er erneut streichelt. Fuer B1a unschaedlich (der Ruf gehoert zu den Befehlen spaeter), aber als offener Punkt O3 notiert.
- Der eigene Zaehm-Balken (Register) und die Engine-Akzeptanz sind zwei Dinge. Vorschlag: unsere Streichel-Aktion ruft in `complete()`
  zusaetzlich `petAnimal` -- dann steigt die Engine-Akzeptanz ehrlich mit und der Stress des (wilden) Jungen sinkt. Unsere eigene
  Abklingzeit muss dann nicht kuerzer sein als Vanillas `petTimer`, sonst zaehlt der Balken, die Engine aber nicht (kein Fehler, nur wissen).

---

## 11. Balken und Text ueber dem Tier, Fortschritt waehrend der Aktion

| Bedarf | Aufruf | Fundstelle |
|---|---|---|
| Vanilla-Vorbild "Anzeige haengt an einer Figur" | UI-Element, in `prerender`/`render` `isoToScreenX(playerIndex, x, y, z + 0.6)` / `isoToScreenY(...)`, dann zeichnen | `V:client/Fishing/TensionUI.lua:10-22` (Angel-Spannung ueber dem Spieler) |
| Bildschirmpunkt | `isoToScreenX(spielerNummer, x, y, z)`, `isoToScreenY(...)` (erstes Argument eine ZAHL) | `V:client/Fishing/TensionUI.lua:11-12`; `V:client/Foraging/ISBaseIcon.lua:167` |
| Bandits-Weg | `ISCoordConversion.ToScreen(isox, isoy, isoz)`, `getRenderer():renderline(tex, x1, y1, x2, y2, r, g, b, a)`, Ereignis `Events.OnPreUIDraw.Add(f)`, Zoom `getCore():getZoom(0)` | `B:client/BanditProjectile.lua:10`, `:49-51`, `:74`, `:88` |
| NPC-Crew-Weg (Namensschilder, gespielt) | ein 1x1-`ISPanel` in der Ecke, das in `prerender` weit daneben zeichnet; `self:drawTextCentre(str, x, y, r, g, b, a, font)` | `NC:client/ISUI/BanditsNPCNameTags.lua:1145-1176` (prerender), `:1178-1191` (Panel anlegen in `OnGameStart`), `:989-1035` (Zeichnen); Begruendung im Kopf `:14-62` |
| Text | `self:drawTextCentre(...)`, `self:drawText(...)` | `V:client/ISUI/ISUIElement.lua:1280`, `:1293` |
| Rechteck / Rahmen | `self:drawRect(x, y, w, h, a, r, g, b)`, `self:drawRectBorder(...)` | `V:client/ISUI/ISUIElement.lua:1191`, `:1219` |
| fertiger Balken | `self:drawProgressBar(x, y, w, h, f, fg)` (f 0..1, fg = {r,g,b,a}) | `V:client/ISUI/ISUIElement.lua:1805-1813`; Aufruf `V:client/ISUI/Gamepad/ISControllerTestPanel.lua:94` |
| Schrifthoehe | `getTextManager():getFontHeight(UIFont.Small)` | `B:client/ISUI/BanditMap.lua:3` |
| 1x1-Element ist Vanilla-Praxis | `ISUIElement:new(0, 0, 1, 1)` | `V:client/ISUI/ISButtonPrompt.lua:1244` |
| geteilter Bildschirm | `getNumActivePlayers()` | `V:client/Fishing/FishingHandler.lua:6` |
| kurze Meldung ueber dem Spieler | `HaloTextHelper.addText(character, text)`, `HaloTextHelper.addBadText(player, text)` | `V:client/Foraging/forageClient.lua:73`; `V:client/ISUI/ISWorldObjectContextMenu.lua:1038` |
| Fortschritt der Zeitaktion | eingebauter Balken ueber dem Spieler: Feld `useProgressBar` (Vorgabe an; Vanilla-Streicheln schaltet ihn aus, `V:ISPetAnimal.lua:99`) | Jar dec/LuaTimedActionNew.java liest das Feld |

"Nichts Teures je Bild" -- was die Vorbilder tun:
- Die Liste der zu beschriftenden Tiere NICHT je Bild suchen: NPC Crew baut sie alle `RESCAN_MS` neu (`NC:...NameTags.lua:1161-1166`) und
  zeichnet je Bild nur aus der fertigen Liste (Position lesen, zwei Umrechnungen, ein Text, zwei Rechtecke je Tier).
- Deckel: nur Junge in Sichtweite (z. B. 20 Kacheln) und hoechstens eine Handvoll.
- Das Element bleibt 1x1 und wird nie unsichtbar geschaltet (frisst sonst Klicks bzw. kommt nie wieder, `NC:...NameTags.lua:42-62`);
  Maus-Funktionen geben false zurueck (`:1141-1143`).
- Bei mehr als einem lokalen Spieler lieber nicht zeichnen (`:1154-1157`).
- Die Werte (Zaehm-Fortschritt, Abklingzeit) kommen im MP per `sendServerCommand` vom Server und liegen beim Client in einer Tabelle je
  OnlineID des Tiers; im SP liest die Anzeige das Register direkt. Der Zeichner fragt nie den Server.
- Anker ueber dem Kopf: `z + Hoehe` (Vanilla nimmt 0,6 ueber dem Spieler; das Junge ist rund 40 cm hoch -> Zahl im Spiel einstellen,
  am besten als Regler in der Bench-Datei).

---

## 12. Sandbox

Format (Datei `42/media/sandbox-options.txt`, C-Kommentare, keine `--`):
- NPC Crew `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/sandbox-options.txt:12-17`:
  `option BanditsNPC.UIScale { type = double, min = 0.0, max = 2.0, default = 0.0, page = BanditsNPC, translation = BanditsNPC_UIScale, }`
- Typen dort: `boolean`, `integer` (min/max/default), `double`, `enum` (`type = enum, numValues = 4, default = 2,` plus
  `valueTranslation = BanditsNPC_WildSpawn,`, Zeile 155-161), `string`.
- Bandits (Engine-Beleg, dass das Format geladen wird): `B:../sandbox-options.txt:5-8`
  `option Bandits.General_KillCounter = { type = boolean, default = true, page = Bandits_General, translation = Bandits.KillCounter, }`.
- Die Turret-Test-Mod hat (noch) keine eigene `sandbox-options.txt` (`NCTurretTest/42/media/` enthaelt nur lua, models_X, scripts, textures,
  UI.json); ihr Uebernahme-Plan nennt die Naht (`turret/NAEHTE.md:51`: `sandbox-options.txt` und `Translate/*/Sandbox.json` anhaengen und
  sortiert zusammenfuehren).

Texte (`Translate/<L>/Sandbox.json`): `"Sandbox_BanditsNPC": "NPC Crew"` (Seitentitel), `"Sandbox_BanditsNPC_UIScale"`,
`"Sandbox_BanditsNPC_UIScale_tooltip"`, bei enum `"Sandbox_BanditsNPC_Diagnostics_option1"` ... (NPC Crew `EN/Sandbox.json:2-22`).

Lesen: `local sv = SandboxVars and SandboxVars.BanditsNPC` und dann `sv.BearX` (`NC:shared/BanditsNPC.lua:6105`; Bandits
`B:client/BanditUpdate.lua:495` `SandboxVars.Bandits.Ge...`). Live-Wert mit Namen: `getSandboxOptions():getOptionByName("Name"):getValue()`
(`V:client/Farming/CPlantGlobalObject.lua:19`).

Fallen:
- Seite `BanditsNPC`: in der Test-Mod OHNE NPC Crew fehlt der Seitentitel `Sandbox_BanditsNPC` -> die Test-Mod muss ihn selbst mitbringen;
  das Uebernahme-Skript darf ihn dann nicht doppelt eintragen (zusammenfuehren, nie neu anlegen).
- Optionsnamen `BanditsNPC.Bear*` vorher gegen NPC Crews 42 Optionen greppen (keine `Bear*` darunter, Stand heute).
- **Namens-Nachbar in NPC Crew:** der Textschluessel `UI_BN_Beard_None` (Bart-Auswahl, `NC:client/BanditsNPCAppearance.lua` und alle sieben
  `UI.json`; grep `UI_BN_Bear` ueber `NPCCrew/42/media/lua`: 8 Treffer, alle `UI_BN_Beard_None`). Kein Zusammenstoss mit `UI_BN_Bear_*`, aber
  jede Pruefung und jedes Zusammenfuehren im Uebernahme-Skript muss auf `UI_BN_Bear_` MIT Unterstrich pruefen, nie auf `UI_BN_Bear`.
  `BanditsNPCBear*`, `BanditsNPC.Bear*`, `ncbearcub`, `NCBearCub` sind in NPC Crew und in Vanilla (lua, scripts) frei (grep 10.11., 0 Treffer).
- Jede Zahl mit nil-Rueckfall auf die Vorgabe lesen (alte Spielstaende kennen neue Optionen nicht).
- Im MP gelten die Werte des Servers; Entscheidungen (Haeufigkeit, Grenzen) trifft ohnehin der Server.
- Tiernamen-Texte: `IGUI_AnimalType_ncbearcub`, `IGUI_Animal_Group_<gruppe>`, `IGUI_Breed_<rasse>` in `Translate/<L>/IG_UI.json`
  (Vanilla `EN/IG_UI.json:1907` `"IGUI_AnimalType_buck": "Buck"`, `:4770` `"IGUI_Animal_Group_deer"`, `:1886` `"IGUI_Breed_whitetailed"`;
  die Engine baut den Namen aus `"IGUI_AnimalType_" .. Art`, `IGUI_AnimalFullName`, `"IGUI_Breed_" .. Rasse`, dec/IsoAnimal.java:2249-2271).
  NPC Crew hat heute `UI.json`, `Sandbox.json`, `Tooltip.json`, **kein `IG_UI.json`** -> Naht fuer das Uebernahme-Skript (neue Datei in NPC
  Crew oder zusammenfuehren, falls bis dahin eine entsteht). Ob ein `IGUI_`-Schluessel auch aus `UI.json` gelesen wuerde: ungeprueft.

---

## 13. Stoerfaelle: was die Engine mit einem fremden Tier ohne Stall macht

| Stoerfall | Engine (Jar-Lesart 42.22.2, ungespielt) | Muss B1a abfangen? |
|---|---|---|
| Wandern | laeuft alle paar Sekunden ein Stueck (`wanderMul`, `NCBearDefs.lua:95`); kein Heimatpunkt | ja, leicht: das Register merkt die letzte Kachel beim Takt; "verschwunden" heisst nicht "weggelaufen" |
| Flucht vor dem Spieler | wild: unter 3 Kacheln immer, 30 Kacheln weit; nicht wild: Zufall (Abschnitt 2) | ja: sonst ist Fuettern aus der Hand bei `wild` unmoeglich (Sperre/Stopp waehrend der Annaeherung, Abschnitt 2 W) |
| Flucht vor Laerm | jeder Schuss/Ruf in Hoerweite: wild `radius*3+20` Kacheln, sonst `radius+10`; Stress steigt (dec/IsoAnimal.java:764-806) | nein (Verhalten ist gewollt scheu); nur wissen: nach einer Schiesserei ist das Junge weg vom Fleck |
| Rand der geladenen Flaeche | bleibt dort stehen bzw. wird mit der Kachel entladen und kommt an derselben Stelle wieder (1.4); echtes "Virtualisieren" nur fuer Wandertiere im Zonen-Zustand (javap IsoMovingObject.postupdate Offset 377-438) | nein; aber der Takt darf ein entladenes Junges nicht fuer tot halten (Zustand "nicht geladen" im Register) |
| Hunger/Durst, Verhungern | wild: nie. Nicht wild: nur mit `hungerMultiplier`/`thirstMultiplier` > 0; ab 0,8 sinkt die Gesundheit je Stunde (dec/AnimalData.java:347-398) | fuer B1a: Multiplikatoren weglassen (0) -> kein Verhungern in der Zaehm-Zeit. Beduerfnisse kommen spaeter (eigener Takt) |
| Stress | wild: startet bei 50..80 und sinkt nur durch Streicheln/Fuettern; nicht wild: sinkt von selbst; ueber 80 kein Locken | nein; als Anzeige "scheu" brauchbar (`animal:getStress()` BELEGT `V:shared/TimedActions/Animals/ISMilkAnimal.lua:17`) |
| Zombies | greifen Tiere nie an (bekannt, `angriff_zombie.md`); mit `fleeZombies` flieht das Junge | nein (Kampf/Gegenwehr ist nicht B1a) |
| Autos | SP: Treffer setzt die Gesundheit auf 0 (dec/IsoAnimal.java:506-522); MP: eigenes Paket | **Tod behandeln** (unten) |
| Spieler-Schlag | Waffentreffer zieht Gesundheit ab; ein wildes Tier bekommt dazu den Verblutungs-Zaehler (dec/IsoAnimal.java:1124-1140) | **Tod behandeln**; Schutz per `setIsInvincible(true)` waere Lua-belegt (`V:ISAnimalContextMenu.lua:563`, `V:server/ClientCommands.lua:911`), ist aber nicht gespeichert und Sache der spaeteren Version (PLAN.md 7) -> offener Punkt O5 |
| "Kill animal" im Menue | nur bei nicht wilden Tieren (`V:ISAnimalContextMenu.lua:307`), ohne Besitzfrage | bei Bauart W bis zum Zaehmen kein Thema; danach Vanilla-Punkt fuer fremde Junge ausblenden (7.2) -- echter Schutz ist B2b |
| Hochheben / Anleinen / Anhaenger | `canBePicked = false`, `canBeAttached` weglassen -> beides aus; Anhaenger: `V:client/Vehicles/ISUI/ISVehicleMenu.lua:667-768` bietet Tiere nach `getAnimalTrailerSize()` an | Hochheben ist aus (ausser God Mode/Unlimited Carry). Anhaenger-Diebstahl: bekannt (PLAN.md 9), nicht B1a |
| Tierzone des Spielers | betritt das Junge eine `DesignationZoneAnimal`, wird es von selbst zahm (`setWild(false)`, dec/IsoAnimal.java:600-613) und die Groesse faellt auf `minSize` (`KRITIK.md` K1; bei min = max egal) | nur wissen: "zahm laut Engine" ist nicht "gehoert jemandem" -- der Besitz steht im Register |
| Tod | `OnCharacterDeath` feuert auch fuer Tiere (Jar `IsoAnimal.OnDeath`, dec/IsoAnimal.java:1120-1122); Leiche entsteht (braucht die Zerlege-Definition, Abschnitt 2) | **ja**: Register-Eintrag raeumen, Sperre "neues Junges nach X Tagen" nur beim EIGENEN (gezaehmten) Baeren starten, wildes Junges einfach austragen. Ereignis: `Events.OnCharacterDeath.Add` hat keine Vanilla-/Bandits-Fundstelle (nur `NC:shared/BanditsNPCPlayerBody.lua:89`) -> hinter `if Events.OnCharacterDeath then`, und zusaetzlich im Takt `animal:isDead()` fragen (BELEGT) |
| Spielstand ohne Mod | wirft beim Laden eines gespeicherten Jungen (1.4) | nur dokumentieren (wie beim Erwachsenen) |
| ID-Zwilling | zwei Tiere mit gleicher AnimalID in 4 Kacheln: die Engine loescht das neu geladene (0.4) | Register darf "Tier fehlt" nicht als Tod werten, ohne `isDead` gesehen zu haben; Verschwinde-Regel und "fehlt seit N Takten trotz geladener Kachel" getrennt fuehren |
| Verschwinde-Regel (unsere) | - | Server/SP entfernt mit `animal:remove()` nur, wenn kein Spieler in der Naehe ist (kein sichtbares Wegploppen); ist die Kachel nicht geladen, bleibt der Eintrag "soll weg" stehen und wird beim naechsten Sehen vollzogen |

---

## 14. Verbotene und offene Punkte

**Nur im Jar belegt -> VERBOTEN ohne Kevins Wort je Methode (nicht einbauen):**
| Methode | Wofuer sie verlocken wuerde | Belegter Ersatz |
|---|---|---|
| `animal:addAcceptance(player, x)` | Akzeptanz gezielt heben | `petAnimal` (Streichel-Aktion), siehe 10 |
| `animal:setWild(true)` | zurueck zu wild | keiner -> nicht vorsehen |
| `animal:tryLure(...)`, `eatFromLured`, `cancelLuring` | Locken mit Honig/Fisch | Vanilla `ISLureAnimal` nur mit Obst/Gemuese; sonst `pathToLocation` (unten) |
| `animal:forceFleeFromChr(chr)` (`getBehavior()`) | scheues Ausweichen | `animal:fleeTo(sq)` (BELEGT) |
| `animal:pathToCharacter(chr)` | zum Spieler kommen | `pathToLocation` (unten) |
| `getCell():getAnimals()` | Tierliste | `getObjectListForLua()` / `sq:getAnimals()` |
| `getSteamIDFromUsername`, `getCurrentUserSteamID`, `player:getSteamID()` | Besitzer-Kennung | `player:getUsername()` (MP), fester Schluessel (SP) |
| Konstante `ItemTag.FISH_MEAT` | Fisch am Tag erkennen | `Fishing.fishes` + `getFoodType() == "Fish"` |

**Schon erlaubt (Kevins Ja 08.11.):** `animal:pathToLocation(x, y, z)` -- mit Jar-Beleg (IsoAnimal ueberschreibt die Methode; am Zombie
`V:DebugContextMenu.lua:636`), Existenz-Riegel, pcall und Gegenprobe (bewegt es sich danach wirklich?). Scheitert es: `fleeTo`.

**Belegt, aber von Kevin ausgeschlossen:** `setDebugAcceptance` (Cheat-Weg). **Belegt nur im Debug-/Cheat-Menue, Einsatz waere eine
Entscheidung:** `setIsInvincible`, `setDebugStress` (`V:server/ClientCommands.lua:978`).

**Offene Punkte fuer Planer/Kevin:**
- **O1 Bauart der Scheu:** (W) `wild = true` + `canBeDomesticated` + beim Zaehmen `setWild(false)` -- oder (Z) nicht wild. W ist naeher an
  "scheues wildes Junges", braucht aber Festhalten bei der Annaeherung; Z ist einfacher, aber kaum scheu. Beides belegt baubar.
- **O2 Version:** alle Unterlagen sagen 42.21, gespielt wird 42.22.2. Vor dem Bau die uebrigen Fundstellen aus PLAN.md/KRITIK.md, die
  dieser Lauf benutzt, gegen die heutigen Dateien halten (dieses Papier ist schon auf 42.22.2).
- **O3 Ruf nach Neuverbindung (MP):** die Engine-Akzeptanz haengt an der OnlineID. Soll der Q-Ruf fuer den Besitzer immer gehen, braucht es
  spaeter (Befehle) einen eigenen Ruf oder Kevins Wort fuer einen Weg, der die Akzeptanz dem Besitzer wiedergibt. Nicht B1a.
- **O4 Koederplatz:** sichtbarer Bodengegenstand (kann verrotten/aufgehoben werden, Server entfernt genau dieses Stueck) oder
  unsichtbar (Stueck beim Auslegen verbraucht, Platz nur im Register). Empfehlung: unsichtbar + Text.
- **O5 Schutz des Jungen vor Spieler-Schlag und Auto** in der Zaehm-Zeit: ohne `setIsInvincible` kann es sterben. B1a muss den Tod nur
  sauber verbuchen; ob es geschuetzt wird, entscheidet Kevin (ENTSCHEIDUNGEN.md: Schaden spaeter nur von Zombies/Banditen/Hunger/Durst).
- **O6 `attachment head`** am Modell-Skript des Jungen (Naht zu baer-junges), falls Vanillas "Pet"/"Feed" je benutzt werden sollen;
  die eigene Aktion braucht es nicht (`luautils.walkAdj`).
- **O7 `IG_UI.json` in NPC Crew** fuer die Tiernamen (Abschnitt 12) -- Naht fuer das Uebernahme-Skript.
- **O8 Ungespielt und im Test zuerst ansehen:** (a) steht ein Lua-erzeugtes Junges nach Speichern/Laden und nach Entladen/Laden der Kachel
  wieder da (42.22.2)? (b) feuert `OnClickedAnimalForContext` fuer die neue Art? (c) wie sieht die Streichel-Haltung mit
  `"animal" = "raccoonkit"` bzw. `defaultpet` aus? (d) laedt der dedizierte Server `Skinned/NCBearCub.glb` (alte offene Frage
  `tier_spez.md` 6.3)? (e) haelt `setBlockMovement(true)` ein WILDES Junges wirklich fest, wenn der Spieler naeher als 3 Kacheln kommt?

## 15. Nicht gefunden (mit Suchmustern)

Alle Suchen ueber `V:` (ganzes `media/lua`) und `B:` (42.22 und common), Muster als grep:
- `Events.OnCharacterDeath.Add` -- 0 (nur NPC Crew).
- `ModData.request`, `OnReceiveGlobalModData` in Vanilla -- 0 (nur Bandits `shared/BanditGMD.lua`).
- `getCell():getAnimals`, `:getAnimalsInZone()` -- 0.
- `forceFleeFromChr`, `pathToCharacter`, `addAcceptance`, `eatFromLured`, `cancelLuring`, `tryLure` -- 0.
- `animal:transmitModData` bzw. `transmitModData()` an einem Tier -- 0 (nur Tueren, Spieler).
- `:getSteamID()` an einem Spieler, `getSteamIDFromUsername`, `getCurrentUserSteamID` -- 0.
- `ItemTag.FISH_MEAT`, `ItemTag.UNCUT_FISH` -- 0.
- `setWild(true)` -- 0 (nur `setWild(false)` zweimal).
- `getAnimal(` ausserhalb von `server/ClientCommands.lua` -- 0.
- Ein Vanilla-Aufruf, der ein Tier OHNE Debug-Recht in die Welt setzt, ausser der Falle (`STrapGlobalObject.lua:211`) und dem Huehnerstall --
  keiner; unser Server-Aufruf von `addAnimal` stuetzt sich auf dieselbe Funktion mit denselben Argumenttypen wie `ClientCommands.lua:809`.
- Ein Sichtfeld-Aufruf fuer den dedizierten Server -- keiner (`isCanSee` ist Client).

Statisch gelesen, nicht gespielt.
