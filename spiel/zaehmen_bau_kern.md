# Lauf baer-zaehmen (B1a): Bau KERN -- Bericht

Stand 10.11.2026 abends. **Statisch geprueft, nicht gespielt.** Nichts in die Test-Mod, nichts nach NPC Crew, nichts committet.
Grundlage: `PLAN_ZAEHMEN.md` (ganz gelesen), Fortsetzung des abgebrochenen Laufs (17:35-18:11).

## 0. Fortsetzung: was vom Vorgaenger da war

| Datei | Zustand beim Start | Was ich getan habe |
|---|---|---|
| `shared/BanditsNPCBear.lua` | vollstaendig (Ende gelesen) | gegen Plan 6.2.1/6.2.2 geprueft, Fundstellen nachgelesen; unveraendert |
| `shared/BanditsNPCBearCrew.lua` | vollstaendig | geprueft; unveraendert |
| `shared/BanditsNPCBearDefs.lua` | vollstaendig | gegen Plan 6.5 geprueft; unveraendert |
| `shared/BanditsNPCBearFood.lua` | vollstaendig | gegen Plan 6.6 geprueft (Skala `getHungerChange` = Skriptwert / 100: `dec/Food.java:1413` rechnet fuer die Anzeige mal 100, Honig im Skript `HungerChange = -20.0`); unveraendert |
| `shared/BanditsNPCBearRules.lua` | vollstaendig | gegen Plan 3.2/6.7 geprueft; unveraendert |
| `server/BanditsNPCBearRegistry.lua` | vollstaendig | zwei Zeilen geaendert (faelliges Junges belegt keinen Platz, Abschnitt 5) |
| `server/BanditsNPCBearWorld.lua` | vollstaendig | `B.ScanAnimals(players)` erweitert (Tiere mit verwaistem Spiegel) |
| `server/BanditsNPCBearServer.lua` | **fehlte ganz** | neu gebaut (833 Zeilen) |
| `scripts/nc_bear_cub.txt` | fehlte | neu |
| `attrappe/kern/` | fehlte | neu: `attrappen.lua`, `run.lua`, `dateiform.py`, `ergebnis.txt` |

Kein Pruefer war gelaufen; jetzt laufen alle vier auf alle KERN-Dateien (Abschnitt 4).

## 1. Dateien (unter `_arbeit/baer_zaehmen/mod/42/media/`)

| Datei | Zeilen | Was sie tut |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | 446 | Modul `BanditsNPC.Bear`, Konstanten (6.2.1), `B.CFG` (3.3 + 10 Zusatzfelder), `B.OPTS` (19 Optionen, 3.1), `B.IsSP`/`IsWriter`, `B.Opt` (NPC Crew `BanditsNPC.Opt` falls da, sonst `SandboxVars.BanditsNPC`, Typ + Bereich), `B.Log`/`Err`/`ErrEvery`, `B.T`, `B.PlayerKey`, `B.Now`, `B.WaitParts`, `B.DirOf`, `B.IsForestAt`/`NearForest`, `B.View`/`ApplySync`/`ViewOf`, `B.Ask`/`Tell`/`SendView` |
| `lua/shared/BanditsNPCBearCrew.lua` | 38 | Naht 1: in `OnGameBoot`, hinter Riegel, `BanditsNPC.Livestock.NOT_TENDED["ncbear"/"bear"] = true` |
| `lua/shared/BanditsNPCBearDefs.lua` | 123 | Tierart `ncbearcub` auf Dateiebene (6.5), `AnimalAvatarDefinition["ncbearcub"]`, `AnimalPartsDefinitions.animals["ncbearcubbrown"]` |
| `lua/shared/BanditsNPCBearFood.lua` | 119 | `B.FoodClass`, `B.IsBaitFood`, `B.FoodList` (6.6) |
| `lua/shared/BanditsNPCBearRules.lua` | 317 | reine Regeln: `B.Gain`, `ApplyGain`, `TameCheck`, `WaitLeft`, `CheckFeed`, `CheckPet`, `CheckBait`, `MayAppear`, `BaitChance`, `VanishStep`, `ReleaseBond`, `Decide` |
| `lua/server/BanditsNPCBearRegistry.lua` | 438 | Register `TrueCompanionsBears` (nur Schreiber, nie uebertragen), Sitzungsobjekte `B._s`, "geaendert"-Merker, `B.NewRec`, `RecOf`, `SlotsOf`, `Commit` (Spiegel `tcBear`), `Close` (Sperre bei Tod), `NearestRec`, Koeder-Eintraege, `B.BuildView` |
| `lua/server/BanditsNPCBearServer.lua` | 833 | Takte (`EveryTenMinutes`, `OnTick` gedrosselt), `OnClientCommand`, `B.Handle` (Hello, BaitDrop), `B.FeedComplete`/`PetComplete`/`BaitComplete`, `B.AppearFor`, Wald-Wurf, Koeder-Naechte und -Erscheinen (`B.BaitDawn`), Verschwinden, Tod, Vermisst, Verhalten (Hirn-Takt -> `B.Decide` -> Halten/Laufen), Sicht verschicken (`B.PushView`, `B.FlushViews`) |
| `lua/server/BanditsNPCBearWorld.lua` | 429 | alle Welt-Griffe: `B.Players`, `PlayerByKey`, `IsNight`, `SquareFits`, `AreaLoaded`, `SeenInSP`, `PickForestSquare`, `FreeSquareNear`, `CreateCub` (einzige Stelle `addAnimal`), `RemoveCub` (einzige Stelle `remove()`), `FindAnimal`, `ScanAnimals`, `Hold`, `MoveTo`, `MoveWatch` |
| `scripts/nc_bear_cub.txt` | 19 | `module Base`: `animationsMesh NCBearCub`, `model NCBearCub_Body` (mesh `Skinned/NCBearCub.glb`, shader `animalEffect`), Form `NCBearTest scripts/nc_bear_tier.txt:3-15`; Kommentare innerhalb des Blocks wie Vanilla xui-Skripte |

Server-Dateien beginnen mit `if isClient() then return end` (V:server/Traps/STrapSystem.lua:1): SP und dedizierter Server.
Lade-Reihenfolge egal: keine Datei faengt auf Dateiebene Funktionen einer anderen ein.

Nicht von mir (OBERFLAECHE, nur gelesen): `shared/TimedActions/*`, `client/*`, `Translate/*`, `sandbox-options.txt`, `NCBearBenchCub.lua`.
Gegen deren Aufrufe geprueft: jede `B.*`-Funktion, die Menue, Balken, Zeitaktionen und Bench rufen, gibt es mit passender Form
(u. a. `B.Touch`, `B.PushView`, `B.SlowTick`, `B.BrainTick(true)`, `B.BaitDawn(bait, now)`, `B.AppearFor` -> rec, why).

## 2. Engine-Aufrufe mit Fundstelle (alle selbst in den heutigen Dateien nachgelesen)

`V:` = Vanilla `media/lua`, `Bd:` = Bandits `42.22/media/lua`.

| Aufruf | Wo im KERN | Fundstelle |
|---|---|---|
| `isClient()` / `isServer()` (beide Negationen) | ueberall | V:shared/TimedActions/ISEatFoodAction.lua:136, V:server/Traps/STrapSystem.lua:1 |
| `getGameTime():getWorldAgeHours()` | `B.Now` | V:server/Traps/STrapSystem.lua:77 |
| `getGameTime():getTimeOfDay()`, `getClimateManager():getSeason():getDawn()/getDusk()` | `B.IsNight` | V:shared/Foraging/forageSystem.lua:1944-1951 |
| `getTimestampMs()` | `B.ErrEvery`, `B.BrainTick`, `B.MoveTo` | V:server/Foraging/forageServer.lua:456 (Drossel :455-461) |
| `getText(key, a, b)`, `getTextOrNull(key)` | `B.T` | V:shared/Definitions/animal/ButcheringUtil.lua:394, V:client/Vehicles/ISUI/ISVehicleMenu.lua:403, V:shared/TimedActions/ISReadABook.lua:220 |
| `player:getUsername()` | `B.PlayerKey` | V:shared/Traps/TrapSystem.lua:45 |
| `getWorld():getMetaGrid():getZonesAt(x,y,z)`, `:size()`, `:get(i)`, `zone:getType()` | `B.IsForestAt` | V:shared/Traps/TrapSystem.lua:12-16 |
| `sendClientCommand(p, mod, cmd, args)` | `B.Ask` (nur MP-Client) | V:client/DebugUIs/DebugContextMenu.lua:956 |
| `sendServerCommand(p, mod, cmd, args)` | `B.Tell`, `B.SendView` (nur Server) | V:server/BuildingObjects/ISBuildUtil.lua:291 |
| `animal:getAnimalType()` | `ViewOf`, `RecOf`, `FindAnimal`, `RemoveCub`, `handCheck` | V:client/ISUI/Animal/ISAnimalUI.lua:65 |
| `animal:getModData()` (erst nach Art-Frage) | `ViewOf`, `RecOf`, `Commit`, `ScanAnimals` | V:client/ISUI/ISInventoryPaneContextMenu.lua:4127 |
| `animal:getOnlineID()` | `ViewOf`, `BuildView`, Hirn-Takt | V:client/ISUI/Animal/ISAnimalContextMenu.lua:432 |
| `animal:getAnimalID()` | `NewRec`, `RecOf`, `FindAnimal`, `ScanAnimals` | V:client/ISUI/Animal/ISAnimalUI.lua:53 |
| `animal:isExistInTheWorld()` | `CreateCub`, `FindAnimal`, `Commit`, `handCheck` | V:client/ISUI/Animal/ISAnimalUI.lua:15 |
| `animal:isDead()` | Tod, `FindAnimal`, `handCheck` | V:server/Traps/STrapGlobalObject.lua:238 |
| `animal:getX()/getY()/getZ()` | `RecOf`, `tileOf`, Hirn-Takt | V:shared/Definitions/animal/ButcheringUtil.lua:575-577 |
| `animal:getSquare()`, `square:DistTo(square) < 3` | `handCheck`, `baitSpotWhy`, Verschwinden | V:shared/TimedActions/Animals/ISPetAnimal.lua:6 |
| `getAllAnimalsDefinitions()`, `def:getAnimalType()`, `def:getBreeds()`, `:size()`, `:get(i)` | `findBreed` | V:client/DebugUIs/DebugContextMenu.lua:246-275 |
| `addAnimal(getCell(), x, y, z, typ, breed, false)`, `animal:addToWorld()` | `B.CreateCub` (einzige Stelle) | V:server/ClientCommands.lua:809-810, V:client/DebugUIs/DebugContextMenu.lua:1460-1467 |
| `animal:getBehavior():setBlockMovement(b)` | `B.Hold`, `B.RemoveCub` | V:client/ISUI/Animal/ISAnimalContextMenu.lua:89, V:shared/TimedActions/Animals/ISPetAnimal.lua:36, ISFeedAnimalFromHand.lua:28 |
| `animal:remove()` | `B.RemoveCub` (einzige Stelle) | V:shared/Definitions/animal/ButcheringUtil.lua:609, V:client/DebugUIs/DebugContextMenu.lua:616 |
| `animal:fleeTo(sq)` | `B.MoveTo` | V:shared/TimedActions/Animals/ISMilkAnimal.lua:38 |
| `animal:petAnimal(character)` | `B.PetComplete` | V:shared/TimedActions/Animals/ISPetAnimal.lua:70 |
| `getCell():getObjectListForLua()`, `:size()`, `:get(i)`, `instanceof(o, "IsoAnimal")` | `B.ScanAnimals` | V:client/DebugUIs/DebugContextMenu.lua:612-615 |
| `getCell():getGridSquare(x, y, z)` | Kachel-Fragen, `AreaLoaded`, Koeder | V:server/Animal/ISPickDungCursor.lua:104 |
| `sq:isOutside()` | `SquareFits` | Bd:server/BanditServerSpawner.lua:152 |
| `sq:TreatAsSolidFloor()` | `SquareFits` | Bd:server/BuildingObjects/ZSGuardposts.lua:12, V:server/BuildingObjects/ISWalkToCursor.lua:35 |
| `sq:getFloor():hasProperty(IsoFlagType.water)` | `isWater` | V:client/ISUI/ISWorldObjectContextMenu.lua:687-688 |
| `sq:HasTree()` | `SquareFits` | V:server/Foraging/forageServer.lua:276 |
| `sq:isFree(false)` | `SquareFits` | Bd:server/BanditServerSpawner.lua:231, V:client/ISUI/ISWorldObjectContextMenu.lua:2219 |
| `sq:isVehicleIntersecting()` | `SquareFits` | V:server/BuildingObjects/ISBuildUtil.lua:34 |
| `sq:isCanSee(nr)` (nur SP) | `B.SeenInSP` | V:client/Foraging/ISBaseIcon.lua:256 |
| `sq:getX()/getY()/getZ()` | Wald-Wurf, Koeder | V:shared/Traps/TrapSystem.lua:12 |
| `getOnlinePlayers()`, `:size()`, `:get(i)` | `B.Players` (Server) | V:server/Foraging/forageServer.lua:463-466 |
| `getNumActivePlayers()`, `getSpecificPlayer(i)` | `B.Players` (SP) | V:client/Fishing/FishingHandler.lua:6, V:server/BuildingObjects/ISBuildingObject.lua:183 |
| `player:isDead()`, `getX()/getY()` | `B.Players` | V:server/Seasons/season.lua:127, Bd:server/BanditServerSpawner.lua:179 |
| `player:getPrimaryHandItem()` | Hirn-Takt (`playerInfo`) | V:server/BuildingObjects/ISEmptyGraves.lua:18 |
| `player:isRunning()`, `isSprinting()` | Hirn-Takt | V:client/Foraging/ISBaseIcon.lua:702, Bd:shared/PlayerDamageModel.lua:81 |
| `inv:contains(item)` | `FeedComplete`, `BaitComplete`, `takeOne` | V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6 |
| `character:removeFromHands(item)`, `inv:Remove(item)`, `sendRemoveItemFromContainer(inv, item)` | `takeOne` | V:shared/Camping/TimedActions/ISAddFuelAction.lua:66-68 |
| `instanceof(item, "Food")`, `getFoodType`, `getHungerChange`, `isRotten` | `B.FoodClass` | V:client/ISUI/Animal/ISAnimalContextMenu.lua:37 |
| `item:getFullType()` / `isBurnt()` / `getDisplayName()` | Futter | V:ISAnimalContextMenu.lua:55, V:client/ISUI/ISInventoryPane.lua:990, V:ButcheringUtil.lua:334 |
| `inv:getAllEvalRecurse(fn)` | `B.FoodList` (nur Client) | V:client/ISUI/Animal/ISAnimalContextMenu.lua:33 |
| `Fishing.fishes[i].itemType` | Fisch-Menge | V:shared/Fishing/fishing_properties.lua:94, :216 |
| `ZombRand(n)`, `ZombRandFloat(a, b)` | Wuerfe, Platzsuche | V:shared/TimedActions/Animals/ISMilkAnimal.lua:25, Bd:server/BanditServerSpawner.lua:216-222 |
| `ModData.getOrCreate(name)` | `B.InitRegistry` | V:server/Foraging/forageServer.lua:26 |
| `Events.OnInitGlobalModData.Add` | Register | V:server/Vehicles/ProfessionVehicles.lua:347 |
| `Events.EveryTenMinutes.Add` | Langsam-Takt | V:server/Traps/STrapSystem.lua:134 |
| `Events.OnTick.Add` | Hirn-Takt | V:server/Foraging/forageServer.lua:502 |
| `Events.OnClientCommand.Add(f(module, command, player, args))` | Bitten | V:server/ClientCommands.lua:1357, Filter wie forageServer.lua:56-57 |
| `Events.OnGameBoot.Add` | Naht 1 | V:client/Foraging/ISSearchManager.lua:1481 |
| Tabellen `AnimalDefinitions.animals`, `AnimalAvatarDefinition`, `AnimalPartsDefinitions.animals` | Datei 3 | V:shared/Definitions/animal/DeerDefinitions.lua:1, :56, :92; V:client/ISUI/Animal/ISAnimalUI.lua:31; V:AnimalPartsDefinitions.lua:456; V:ButcheringUtil.lua:18 |
| `pcall(f, ...)` (Lua-Grundfunktion, keine Engine-Methode) | nur um EIGENE Takt-Koerper, Fehler gedrosselt gemeldet | Vanilla/Bandits benutzen es nicht; im gespielten NCTurretTest shared/BanditsNPCTurretCrew.lua:128; `luacheck_pz.py` fuehrt es als Kahlua-Grundfunktion |

**Nicht benutzt** (Plan 0.8, per grep gegengeprueft): `setWild`, `addAcceptance`, `setDebug*`, `setIsInvincible`, `tryLure`, `pathToCharacter`,
`pathToLocation`, `forceFleeFromChr`, `isAnimalMoving`, `getCell():getAnimals()`, `transmitModData`, `ModData.transmit`/`request`,
`OnCharacterDeath`, `LosUtil`, `feedFromHand`. Kein Jar-only-Aufruf.

**Nur auf Client/SP in Vanilla belegt, auf dem dedizierten Server dieselbe Java-Methode (MP-Testpunkte, kein pcall als Tarnkappe):**
`getCell():getObjectListForLua()`, `getAllAnimalsDefinitions()` + `addAnimal` aus eigenem Antrieb (am Server belegt nur ueber
ClientCommands), `sq:isFree`/`getFloor`, `animal:getOnlineID`/`getAnimalID`/`getModData`.

## 3. SP- und MP-Zweig je Vorgang

| Vorgang | Einzelspieler | Mehrspieler (dedizierter Server) |
|---|---|---|
| Register | `ModData.getOrCreate` im einen Programm, ab `OnInitGlobalModData` | nur der Server; nie uebertragen, Client hat nur `B.View` |
| Wald-Wurf (5.1) | Langsam-Takt; je Spielerschluessel ein Wurf (`ZombRand(10000) < % x 100 / 6`); Platz im Ring Min..Max, Wald, frei, Mindestabstand, **nicht sichtbar** (`isCanSee`) | derselbe Code ueber `getOnlinePlayers()`; **ehrliche Grenze:** "ausser Sicht" nur ueber den Mindestabstand (kein Sichtfeld am Server) |
| Erscheinen (`B.AppearFor`) | `addAnimal` + `addToWorld` + Gegenprobe, Eintrag, Spiegel, Hinweis mit Richtung | derselbe Code, aus eigenem Antrieb beim Server (kein Client-Weg, kein Kick) |
| Neugier, Flucht, Halten, Locken (6.7) | Hirn-Takt alle 1,5 s: `B.Decide` -> `setBlockMovement` / `fleeTo` (hoechstens alle 3 s) | derselbe Code am Server; Hand und Tempo fragt der Server an SEINEN Spielerobjekten |
| new -> shy | erster Spieler in 15 Kacheln, `Note_Seen` | ebenso, Meldung per `sendServerCommand` |
| Fuettern (5.3) | `complete()` nach `perform()` ruft `B.FeedComplete`; Meldungen direkt (`B.ShowNote`), Sicht direkt (`B.ApplySync`) | `complete()` am Server mit dem Stueck des Servers; alle Pruefungen dort; nehmen (`Remove` + `sendRemoveItemFromContainer`) und gutschreiben im selben Aufruf; Fress-Animation nur beim fuetternden Client (OBERFLAECHE) |
| Streicheln (5.4) | wie Fuettern, dazu `petAnimal` | wie Fuettern |
| Koeder auslegen (5.2) | `B.BaitComplete`: Wald, draussen, Abstand <= 3, Plaetze, Deckel, Abstand 10, Stueck, dann nehmen + eintragen | derselbe Code am Server |
| Koeder-Naechte | Langsam-Takt merkt Nacht, beim Morgengrauen `B.BaitDawn` (Spieler in 20 -> Fehlmorgen; 4 -> Verfall) | ebenso |
| Koeder-Junges | Hirn-Takt: reif, Kachel geladen, niemand in 20, nicht sichtbar -> freie Kachel in 2 -> `B.AppearFor(owner, "bait")`, Heimat = Platz | ebenso (Sicht nur ueber Abstand) |
| Koeder aufgeben | `B.Ask` -> `B.Handle` direkt | `sendClientCommand` -> `OnClientCommand` -> Server prueft `bait.owner == Benutzername` |
| Verschwinden (5.5) | Uhr nur bei Finder online; faellig -> `goneP`; vollzogen nur geladen, niemand in 25, nicht sichtbar | ebenso ohne Sichtfrage; ein Client ruft nie `remove()` |
| Aufgabe fed -> shy | 168 h ohne Kontakt, bond online | ebenso |
| Tod | `isDead()` am gemerkten Objekt -> `B.Close(rec, "dead")`, bei zahm Sperre 7 x 24 h | ebenso |
| Vermisst / verloren | 3 Suchlaeufe bei geladener Gegend ohne Fund; zahm -> `missing` (24 h, dann frei, keine Sperre), sonst Eintrag weg | ebenso; OnlineID/Neuladen ungeprueft |
| Sicht | `B.SendView` -> `B.ApplySync` direkt | `sendServerCommand(..., "Sync", payload)`; nach jeder Aenderung an Betroffene, bei neuem Jungen in 60 Kacheln oder neuer OnlineID; hoechstens eine je Spieler und Takt |
| Geteilter Bildschirm (SP) | alle lokalen Spieler teilen `"__sp"` (ein Besitz), `uid` trennt sie fuer "steht still" und Sendungen | - |

## 4. Pruefer-Ausgaben (auf alle 8 KERN-Lua-Dateien)

- `luacheck.py`: `8 file(s) checked, 0 failed`
- `scopecheck.py`: `8 file(s), 0 violation(s)`
- `luacheck_pz.py`: `0 Treffer (W113)`. Mit `--unused`: 2 harmlose Hinweise (`Rules.lua:41` Vorbelegung `base = 0`, `Rules.lua:160` unbenutztes `slots` in `B.CheckPet` -- Parameter laut Schnittstelle).
- `localcount.py`: groesste Funktion 29 aktive / 36 insgesamt deklarierte Locals (`BanditsNPCBearServer.lua` Hirn-Takt-Koerper :773 bzw. `BanditsNPCBearWorld.lua` `ScanAnimals` :286); Hauptblock Server 30 insgesamt. Weit unter 180/200.
- Dateiform (`attrappe/kern/dateiform.py`, an den Bytes): alle 9 Dateien LF, reines ASCII, kein BOM, Zeilenende am Schluss, keine Zeile endet mit `\`;
  im Code-Teil (ohne Kommentare) keines der verbotenen Woerter (spawn, debug, bench, cheat, test, Dbg, godmode, `_G`, `Capability.`, `AddItem`, `instanceItem`, `NCBear_`, `next(`, `%a`).
  In KOMMENTAREN stehen Fundstellen-Dateinamen wie `DebugContextMenu.lua` und `BanditServerSpawner.lua`; das Uebernahme-Vorbild prueft nur den Code-Teil (`turret_uebernahme.py:121`, "Kommentare nicht").
- Globale: nur `BanditsNPC = BanditsNPC or {}`, `AnimalDefinitions = AnimalDefinitions or {}` (Datei 3); keine globale Funktion.

## 5. Attrappen-Test (`attrappe/kern/run.lua`, lua5.1)

Aufruf: `C:/Users/Kevin/Tools/lua51/lua5.1.exe C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/kern/run.lua`
Ergebnis (`attrappe/kern/ergebnis.txt`): **133 bestanden, 0 Fehler.** Einzige Fehlerzeile des Kerns im ganzen Lauf ist die erwartete aus Fall 4
("take: the food is still in the inventory after Remove, nothing credited"); keine von `pcall` gefangene Ausnahme.

Die Attrappe laedt die echten KERN-Dateien in Ladefolge und ersetzt nur Engine-Globale (`attrappen.lua`). Pflichtfaelle:
1. Punkte: alle sechs Ablaeufe aus 3.2 genau (21/12/31,5/12/31,5 -> 3 F + 2 S; 113 -> 4 + 3; 101 -> 5 + 2; 8 x normal; 5 x Lieblingsfutter; Halt bei 99 mit `need = 2`), Happen 7.
2. Abklingzeiten Fuettern/Streicheln mit Grund und Reststunden; nach Ablauf angenommen; `petAnimal` je angenommenem Streicheln.
3. Zustaende: Wald-Wurf -> new (Ring 30..50, Hinweis), new -> shy, shy -> fed (bond, Heimat), fed -> shy nach 168 h (Balken halbiert, Meldung), fed -> tame, tame -> missing -> tame (neues Objekt mit kopiertem Spiegel), missing -> verloren nach 24 h ohne Sperre, new -> verloren nach 3 Suchlaeufen, nicht geladene Gegend zaehlt nicht.
4. Futter genau einmal: tot, fremde Art, zu weit, nicht im Inventar, kein Futter, verdorben -> je 0 Entnahmen, 0 Punkte; angenommen -> genau 1 `Remove`, 1 `sendRemove`; MP fremder bond -> abgelehnt, nichts verbraucht; `Remove` wirkt nicht -> false, keine Gutschrift.
5. Koeder: 40/70/100; Steak abgelehnt; nicht am Wald abgelehnt; genau 1 Entnahme; zweiter Platz abgelehnt; Morgen mit Spieler nah zaehlt nicht (Hinweis); Verfall nach 4; Wuerfe; reifer Platz erzeugt erst bei Abstand >= 20 ein Junges mit Heimat am Platz.
6. Plaetze: Baer / gebunden / wild / Sperre (Resttage) lehnen ab; echter Weg lehnt zweites wildes Junges ab; Welt-Deckel; 64er-Deckel (ohne erzeugtes Tier); Option geklemmt und Rueckfall auf Vorgabe.
7. Verschwinden: Uhr nur mit Finder online, Kontakt setzt zurueck, faellig nach 36 h, vollzogen erst ohne Spieler in 25; SP sichtbar -> bleibt.
8. Tod: zahm -> Sperre 168 h und Meldung, dann AppearFor abgelehnt, Sperre laeuft ab und wird geraeumt; angefuettert -> keine Sperre; fehlt ohne `isDead` -> nie Sperre.
9. SP: Tell/SendView direkt, keine Sendung, Ask -> Handle; Server: genau ein `sendServerCommand` je Meldung, Hello -> Sync an genau diesen Spieler, fremdes Modul / kaputte args -> nichts; Client: Server-Dateien definieren nichts, Ask sendet, Tell tut nichts; Schluessel `__sp` / Benutzername.
10. `B.Decide`: jede der neun Regeln mit treffendem und knapp nicht treffendem Fall, Fluchtpunkt 12 Kacheln weg, `lead` beim zahmen.
11. Sicht nur Zahl/Text/Wahrheitswert/Tabelle mit OnlineID; `CheckFeed`/`CheckPet` auf Register- und Sicht-Eintrag gleiche Antwort (3 Lagen); `B.ViewOf` ueber OnlineID.
12. kein `next(`, kein `%a` in den 8 Dateien.
Zusatz: Flucht und Herankommen im Hirn-Takt, Drossel (kein Suchlauf bei 20 OnTicks), kein zweites Junges neben einem wilden.

Der Test beweist Logik, nicht Engine-Verhalten (Kahlua ist kein echtes 5.1; die Attrappe bildet Engine-Methoden nach, wie wir sie verstehen).

## 6. Nicht gebaut, ungeprueft, offen

**Nicht gebaut (laut Auftrag):** Wachsen (vorbereitet: `kind`, `aid`, Wahrheit im Register), Kampf/Gegenwehr, Befehle, Fenster, Namensschild,
Beduerfnisse, Inventar, Schlafen, Umbenennen der alten `NCBear*`/Art `bear`. Die alten Dateien sind unberuehrt. `prec.tamedN` wird nicht
gefuehrt (Spieler-Eintraege tragen nur die Sperre). `B.OnCubDead` ist `B.Close(rec, "dead")`.

**Ungeprueft (nur im Spiel zu klaeren):**
- Junges nach Speichern/Laden: Spiegel `tcBear` am Tier wiedergefunden? (`ScanAnimals` Rueckfall ueber AnimalID, genau ein Kandidat in 40 Kacheln)
- haelt `setBlockMovement(true)` das nicht wilde Junge; rennt `fleeTo` wie gedacht; sieht das Naeherkommen gut aus; Gleiten bei 0,35
- Hirn-Takt "free" loest nur eine Sperre, die WIR gesetzt haben; waehrend einer Streichel-Aktion (Spieler ohne Futter in der Hand) kann
  der Takt eine eigene, vorher gesetzte Sperre loesen -- die Aktion setzt ihre eigene in `start()`; ob das Junge dabei wegwandert: Testpunkt
- `isDead()` nach `setHealth(0)` (Bench) und nach echtem Tod am gemerkten Objekt; ob das Objekt danach `isExistInTheWorld` bleibt, ist egal (Tod wird vorher gefragt)
- dedizierter Server: GLB laedt, `getObjectListForLua`, `addAnimal` aus eigenem Antrieb, Kachel-Fragen, OnlineID stabil nach Neuladen
- `sendRemoveItemFromContainer` im SP (Vanilla ruft es in `complete()` auch im SP, ISAddFuelAction.lua:68)

**Ehrliche Grenzen MP:** "ausser Sicht" nur ueber den Mindestabstand; Fress-Animation nur beim Fuetternden; kein Schutz vor Waffen/Autos (Tod
wird verbucht); Anhaenger-Diebstahl; SP-Spielstand spaeter als MP gehostet kennt `__sp` nicht.

**Abweichungen / Zusaetze zur Schnittstelle:** alle in `schnittstelle_aenderungen.md`, Eintrag "KERN 1" (wahlfreie Zusatz-Parameter,
`rule` in `B.Decide`, weitere Helfer, faelliges Junges belegt keinen Platz + Aufraeumen verwaister Tiere, Gruende fuer Koeder-Abstand/-Deckel).

**Fuer den ZUSAMMENBAU:** Platzhalter-Modell/Textur (`models_X/Skinned/NCBearCub.glb`, `textures/Body/NCBearCub.png`) liegen noch NICHT im
Staging (Plan 0.7: Sache des Zusammenbaus). Erlaubt-Liste fuer das Uebernahme-Skript: `NCBearCub_Body` (Skript), globale Zuweisungen
`BanditsNPC = ...`, `AnimalDefinitions = ...`; `addAnimal(` nur in `B.CreateCub`, dessen einziger Rufer `B.AppearFor` ist; `B.AppearFor`
rufen im Kern nur `forestRolls` und `baitAppear` (Server-Datei); `:remove()` am Tier nur in `B.RemoveCub` (gerufen aus `AppearFor`
bei vollem Register, Verschwinden im Hirn-Takt, `ScanAnimals` fuer verwaiste Tiere, Bench).

Statisch geprueft, nicht gespielt.
