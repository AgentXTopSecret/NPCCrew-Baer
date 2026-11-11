# Lauf baer-b1b: Forschung "Folgen + Namensschild" (B1b)

Stand 10.11.2026. **Statisch gelesen, nichts gebaut, nichts gespielt.** Rolle: Forschung (kein Code im Staging).
Jede Laufzeit-Aussage ohne Spielbeleg ist "ungeprueft".

Schreibweise der Fundstellen (wie `forschung_engine.md`):
- `V:` = Vanilla-Lua `C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/lua/` (Spiel 42.22.2).
- `VA:` = Vanilla `media/AnimSets/` (XML der Anim-Knoten).
- `B:` = Bandits `.../mods/Bandits/42.22/media/lua/`.
- `NC:` = NPC Crew `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua/` (nur gelesen, gespieltes Vorbild, kein Engine-Beleg).
- `T:` = Test-Mod `C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/lua/` (gespielt).
- `S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/` (B1a + Fix 2/3).
- `Jar:` = nur Lesehilfe. `dec/` = Auszuege von B1a (42.22.2), **neu `dec_b1b/`** (heute aus demselben Jar gezogen und mit
  Vineflower 1.12.0 entpackt: AnimalPathFindState, AnimalWalkState, AnimalIdleState, AnimalFollowWallState, PathFindBehavior2,
  IsoGameCharacter, AnimalPacket, AnimalUpdate*Packet, AnimalOwnershipPacket, AnimalSynchronizationManager, AnimalStateVariables,
  NetworkPlayerAI, NetworkCharacterAI, VGAStar, SearchNode). Klassen dazu in `jar/`.
- **BELEGT** = echter Aufruf in Vanilla-Lua oder Bandits mit gleichen Argumenttypen. **NUR JAR** = braucht Kevins Wort je Methode.
- **ERLAUBT (Kevin 08.11.)** = `animal:pathToLocation(x, y, z)` (`forschung_engine.md:627`).

---

## 0. Die sechs wichtigsten Befunde vorweg

1. **Tiere rechnet im MP nur der Server, die Clients ziehen nach.** `IsoAnimal.updateInternal` laesst Verhalten, Wegsuche,
   `respondToSound` usw. nur laufen, wenn NICHT `GameClient.client` (Jar `dec/IsoAnimal.java:416-460`, Client-Zweig `:419-428` ruft
   nur `super.update()`); die Zustaende Walk/PathFind laufen nur bei `isLocalPlayer()` = `!GameClient.client` (`dec/IsoAnimal.java:3339-3341`,
   `dec_b1b/AnimalWalkState.java:41`). Der Server schickt je Tier alle 800 ms (in Sicht) bzw. 1000 ms ein `AnimalPacket` mit
   Lage, naechstem Wegpunkt (`prediction.pathFindX/Y`, Typ 2) und dem Rennen-Merker (`dec_b1b/AnimalSynchronizationManager.java:27-28`,
   `dec_b1b/NetworkPlayerAI.java:162-169`, `:171-178`, `dec_b1b/AnimalStateVariables.java:8-19`); der Client sucht sich zu diesem Punkt
   selbst den Weg (`dec_b1b/NetworkPlayerAI.java:350-362`). **Folgen muss also am Schreiber (SP-Programm / Server) befohlen werden** --
   genau wie B1a es mit `fleeTo` schon tut (`S:server/BanditsNPCBearWorld.lua:385-414`). Ein Client-Befehl wuerde beim naechsten Paket ueberschrieben.
2. **`fleeTo` ist `animalRunning = true` + `pathToLocation`** (Jar `dec/IsoAnimal.java:2518-2527`). `pathToLocation` allein laesst den
   Rennen-Merker so, wie er gerade steht; zurueck auf "gehen" setzt ihn die Engine nur beim naechsten Wander-Wurf im Stand
   (`dec/BaseAnimalBehavior.java:165-167`) oder beim Vanilla-Seil (`walkToChr`, unten). **Gehen statt Rennen braucht deshalb
   `animal:setVariable("animalRunning", false)`** -- Lage der Belege in 1.3 (Grenzfall, Kevins Wort empfohlen).
3. **Das Platzhalter-Junge ist zu langsam, um einem gehenden Spieler gehend zu folgen.** Weg in `Translation_Data` des Staging-GLB
   (heute nachgemessen): `DeerStag_Walk` 0,294 E je 0,900 s (~0,52 Kacheln/s), `DeerStag_Run` 0,822 E je 0,533 s (~2,47 Kacheln/s);
   Spieler gehend ~2,27 Kacheln/s (`Bob_Walk`, `baer/spiel/tier_spez.md:226-237`, Umrechnung mit MotionScale 1,6 ebenda). Das Junge
   muss also schon zum Mitgehen RENNEN und faellt hinter einem rennenden Besitzer zurueck. Der Weg kennt die Groesse 0,35 nicht
   (`_arbeit/baer_baby/SPEZ_BABY.md:288-293`). Kevins Wunsch "rennt mit, wenn er rennt" geht mit diesen Clips nur bis zum Deckel.
4. **Laerm und der Q-Ruf ziehen ein zahmes Junges weg.** `respondToSound` (Jar `dec/IsoAnimal.java:764-806`): ein nicht wildes Tier
   reagiert auf jeden Nicht-Fahrzeug-Laerm mit Flucht `radius + 10` Kacheln im Rennen; nur wenn die Quelle ein rufender Spieler mit
   Engine-Akzeptanz >= 40 ist, laeuft es zu ihm. Der Q-Ruf hat Radius 30 (geschlichen 6) und ist ein Tier-Laerm
   (Jar `dec_b1b/IsoGameCharacter.java:4956-5038`). **Spielbeleg:** der Erwachsene lief beim Q-Ruf weg (`baer/begleiter/ENTSCHEIDUNGEN.md:97`).
   Nach dem Zaehmen liegt die Engine-Akzeptanz des Jungen rechnerisch meist unter 40 (Start 0..20, je gezaehltem Streicheln +2..6,
   `forschung_engine.md:376-379`, `:505`). `setBlockMovement` haelt davor NICHT fest (respondToSound fragt die Sperre nicht). Folgen
   und Bleiben muessen das im Takt zuruecknehmen (neuer Weg ueberschreibt die Flucht, 1.5).
5. **N5 hat zwei Teile:** (a) `B.ScanAnimals` legt ein Junges ohne Spiegel nur in `loose` und raeumt Uebriggebliebene nie
   (`S:server/BanditsNPCBearWorld.lua:317-345`); (b) **der Suchlauf laeuft nur, wenn einem Eintrag sein Objekt fehlt**
   (`S:server/BanditsNPCBearServer.lua:816-823`). Bei Kevin (b1 gebunden, Waise daneben) lief er also gar nicht. Ein Waisen-Weg braucht
   einen eigenen, seltenen Suchlauf.
6. **Vanilla hat schon einen Tiernamen -- und jeder darf ihn aendern.** `customName` wird gespeichert (`dec/IsoAnimal.java:1275`,
   `:1378-1381`), mit dem `AnimalPacket` an die Clients verteilt (`dec_b1b/NetworkPlayerAI.java:267-269`, `:467-468`) und in Menues
   ueber `getFullName()` gezeigt (`dec/IsoAnimal.java:2249-2257`; `V:client/ISUI/Animal/ISAnimalContextMenu.lua:140`). Ueber dem Tier
   zeichnet ihn Vanilla nur in der Zonen-Ansicht (`dec/IsoAnimal.java:946-985`, `isSeeDesignationZone`). **Aber:** "Animal info" gibt es
   fuer jedes nicht wilde Tier (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:152-171`), dort ist "Umbenennen"
   (`V:client/ISUI/Animal/ISAnimalUI.lua:389`, `:459-485`) und der Server-Befehl `animal.rename` prueft keinen Besitz
   (`V:server/ClientCommands.lua:1102-1123`). Die Wahrheit ueber den Namen gehoert deshalb ins Register (wie Besitz und Balken).

---

## 1. Folgen / Bleiben (Auftrag Punkt 1; Forschung a, b)

### 1.1 Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil

| Bedarf | Aufruf | Fundstelle (Zeile zitiert) | Seite | Urteil |
|---|---|---|---|---|
| zu einem Punkt **rennen** | `animal:fleeTo(square)` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38` `self.animal:fleeTo(sq);`; ebenso `V:shared/TimedActions/Animals/ISShearAnimal.lua:38`; in B1a `S:server/BanditsNPCBearWorld.lua:405` | Schreiber (im Jar nur dort wirksam, 0.1) | **BELEGT**, in B1a gespielt (Kevin: *"das rennt weg"*, `baer/STAND.md` 10.11. ~22:25) |
| zu einem Punkt laufen (Rennen-Merker bleibt, wie er ist) | `animal:pathToLocation(x, y, z)` (ganze Zahlen) | am Zombie `V:client/DebugUIs/DebugContextMenu.lua:636` `DebugContextMenu.selectedZombie:pathToLocation(square:getX(), square:getY(), square:getZ())`; IsoAnimal ueberschreibt (Jar `dec/IsoAnimal.java:2651-2667`: 15-Kachel-Seilpruefung, dann `getPathFindBehavior2().pathToLocation` + `pathToAux`) | Schreiber | **ERLAUBT (Kevin 08.11.)** |
| gehen statt rennen | `animal:setVariable("animalRunning", false)` vor `pathToLocation` | Methode `IsoGameCharacter.setVariable(String, boolean)`: am Spieler `V:shared/TimedActions/Animals/ISMilkAnimal.lua:138` `self.character:setVariable("milkanimalout", false)`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:37` `self.character:setVariable("petanimal", true)`; am Zombie `B:shared/ZombieActions/ZAMove.lua:31` `zombie:setVariable("bPathfind", true)`; **am Tier** im gespielten `T:shared/NCBearFight.lua:457` und `:1064` (`B.a:setVariable("bPathfind", true)`, Begruendung dort `:1062-1063` "gleiche Methode, gleiche Argumenttypen"). Am Tier in Vanilla nur `(String, String)`: `V:shared/TimedActions/Animals/ISPetAnimal.lua:43` `self.animal:setVariable("idleAction", "petting")` | Schreiber; der Merker reist mit dem Paket zum Client (`dec_b1b/AnimalStateVariables.java:12`, `:18`) | **GRENZFALL**: geerbte Methode, gleiche Argumenttypen, am Tier nur in der eigenen Test-Mod. Name -> derselbe Speicherplatz wie die Engine-Kennung: Jar `dec_b1b/IsoGameCharacter.java:12212-12222` (Text) und `:12244-12256` (Kennung -> `getVariableName()`), Kennung `animalRunning` aus `AnimationVariableHandlePool.getOrCreate("animalRunning")` (javap `AnimationVariableHandles` static Offset 0-5). Empfehlung: Kevins Wort einholen (wie fuer pathToLocation), sonst nur rennen (`fleeTo`) |
| anhalten | `animal:getBehavior():setBlockMovement(true)` (ruft intern `stopAllMovementNow`) | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:89`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:36`, `V:shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:30`; Jar `dec/BaseAnimalBehavior.java:1739-1747` | Schreiber | **BELEGT**, B1a `B.Hold` (`S:server/BanditsNPCBearWorld.lua:367-377`). Die Engine loest die Sperre nach `blockedFor >= 8000` (Multiplikator-Ticks) selbst (`dec/BaseAnimalBehavior.java:74-80`) -> je Takt erneuern (macht B1a). Sperre wird NICHT gespeichert (`forschung_engine.md:113-114`) |
| sofort stoppen ohne Sperre | `animal:stopAllMovementNow()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:760`, `:1000`, `:1007` | in Vanilla nur Client-Menue; im MP beim Client nur an der Kopie | **BELEGT**; fuer den Schreiber reicht `setBlockMovement(true)`/(false) |
| Ankunft erkennen | Lage vergleichen: `animal:getX()/getY()` gegen Ziel | `V:shared/Definitions/animal/ButcheringUtil.lua:575-577`; B1a-Muster `B.MoveWatch` (`S:server/BanditsNPCBearWorld.lua:418-428`) | Schreiber | **BELEGT**. Engine-Lesart: Walk endet bei \|dx\|,\|dy\| < 0,5 (`dec_b1b/AnimalWalkState.java:57-59`); PathFind meldet Succeeded/Failed (`dec_b1b/AnimalPathFindState.java:38-60`). `isAnimalMoving()` hat KEINE Lua-Fundstelle (grep 0) -> nicht benutzen |
| Haengen erkennen | wie oben ueber Zeit: kein Fortschritt in N Takten | gespieltes Vorbild `T:shared/NCBearFight.lua:199` (STALL_TIME/STALL_GAIN, neuer fleeTo) | Schreiber | **BELEGT** (nur getX/getY). Engine: Weg gescheitert -> `pathFailed()` + Wandfolge + gleicher Weg neu (`dec_b1b/AnimalPathFindState.java:40-47`), Wandfolge mit Zeitdeckel `max(500, Abstand*80)` (`dec_b1b/AnimalFollowWallState.java:31-44`); auf der Stelle laufen -> Reset (`dec_b1b/AnimalWalkState.java:61-67`). Haengt also nicht endlos, versucht aber ohne unser Zutun nicht weiter |
| Besitzer: Ort, Ebene | `p:getX()/getY()/getZ()` | `B:server/BanditServerSpawner.lua:179`; `B.Players()` liefert sie schon (`S:server/BanditsNPCBearWorld.lua:29-54`) | Schreiber | **BELEGT** |
| Besitzer rennt | `p:isRunning() or p:isSprinting()` | `V:client/Foraging/ISBaseIcon.lua:702`; `B:shared/PlayerDamageModel.lua:81`; in B1a `S:server/BanditsNPCBearServer.lua:585` | Client belegt; am Server fuer fremde Spieler ungeprueft | **BELEGT** (Werte am Server: ungeprueft). Robuster Zusatz: Weg je Takt aus den Lagen (`B._pp`, `S:server/BanditsNPCBearServer.lua:586-587`, `:838-840`) |
| Besitzer im Auto | `p:getVehicle()` | Server: `V:server/Vehicles/VehicleCommands.lua:11` `local vehicle = player:getVehicle()`, `V:server/Seasons/season.lua:139`; Client: `V:client/ISUI/Hutch/ISHutchMenu.lua:8` | beide | **BELEGT** -> auf "Bleiben" wechseln, Meldung |
| Besitzer online? | `B.PlayerByKey(owner, players)` (Spielerliste) | `S:server/BanditsNPCBearWorld.lua:57-64` | Schreiber | eigener Code, **BELEGT** |
| Zielkachel geladen, kein Wasser | `getCell():getGridSquare(x, y, z)` (nil = nicht geladen), Wasser wie B1a | `V:server/Animal/ISPickDungCursor.lua:104`; `B.MoveTo` prueft beides schon (`S:server/BanditsNPCBearWorld.lua:393-403`) | Schreiber | **BELEGT**. Wichtig: Ziel in nicht geladener Gegend -> PathFind meldet Erfolg, laeuft aber mit `bMoving = true` weiter (`dec_b1b/AnimalPathFindState.java:49-56`) -> nie ein Ziel ausserhalb geladener Kacheln geben |
| Meldung "bleibt hier" | `B.Tell(p, note)` | `S:shared/BanditsNPCBear.lua:439-448` | Schreiber -> Client | **BELEGT** (B1a) |

### 1.2 Was Vanilla beim Seil macht (Vorbild fuer den Algorithmus, NICHT als Weg)

`BaseAnimalBehavior.followChr` (Jar `dec/BaseAnimalBehavior.java:1271-1303`, gerufen in `update` `:325`), nur wenn keine Sperre:
- Takt: `followChrTimer = 150` (Multiplikator-Ticks) zwischen zwei Pruefungen.
- Spieler bewegt sich und Abstand > 2 -> `walkToChr(chr, 2)`; Abstand < 4 und das Tier steht -> nichts; Abstand >= 4 und Spieler steht ->
  `walkToChr(chr, 5)`; Abstand >= 15 -> Seil reisst (`setAttachedPlayer(null)`).
- `walkToChr` (javap `javap/BaseAnimalBehavior.txt:4138-4198`, Vineflower hat den Rumpf verschluckt): `animalSpeed = 1.2`, Ziel = Tier +
  (Richtung zum Spieler, Laenge minus 1), `pathToLocation(..., chr.getZi())`; **rennt, wenn die Reststrecke > 5, sonst geht es**
  (`animalRunning` true/false, Offset 134-173).
- Dazu wandert ein angeleintes Tier im Stand um den SPIELER statt um sich selbst (`xRef` = Spieler, `dec/BaseAnimalBehavior.java:166-179`).

Urteil: als Muster gut (Takt, Abstaende 2/4, gehen/rennen ab 5 Restkacheln, Riss = unser "zu weit weg"). Als Weg ungeeignet: braucht
`canBeAttached` (fuer das Junge mit Absicht aus, `S:shared/BanditsNPCBearDefs.lua:96-97`), ein Seil, im MP darf jeder anleinen
(`baer/begleiter/PLAN.md:205-208`), `fleeTo` loest das Seil (`dec/IsoAnimal.java:2519-2523`). `animalSpeed` wirkt im Animset `buck` nicht
(`VA:buck/walk/defaultWalk.xml` hat kein `m_SpeedScale`; die Kuh hat es: `VA:cow/walk/defaultWalk.xml:6` `<m_SpeedScale>animalSpeed</m_SpeedScale>`).
Gehen/Rennen schaltet in `buck` allein `animalRunning` (`VA:buck/walk/run.xml`: Bedingung `animalRunning = true` -> `DeerStag_Run`).

### 1.3 Gehen und Rennen -- was die Engine selbst setzt

- `fleeTo`: setzt `animalRunning = true` (`dec/IsoAnimal.java:2525`).
- Wander-Wurf im Stand: setzt `animalRunning = false`, dann ggf. `periodicRun` (`dec/BaseAnimalBehavior.java:165-167`, `:219-225`). Nur
  wenn das Tier frei, nicht gesperrt, nicht in Bewegung und ohne gemerkten Laerm ist (`dec/BaseAnimalBehavior.java:83-93`).
- Laerm-Flucht: `animalRunning = true` (`dec/IsoAnimal.java:800`).
- Folge fuer B1b: nach einem `fleeTo` rennt jeder spaetere `pathToLocation` weiter, bis die Engine selbst zuruecksetzt. Ohne
  `setVariable("animalRunning", false)` (Grenzfall, 1.1) gibt es kein verlaessliches Gehen. Mit den Platzhalter-Clips (Befund 0.3) ist
  Gehen ohnehin nur in der Naehe sinnvoll (Abstand < ~5, wie Vanillas Seil).

### 1.4 Besitzer im Auto, Treppen, Tueren, Zaeune, entladene Gegend (Forschung b)

| Fall | Engine (Jar-Lesart 42.22.2, ungespielt) | Folge fuer B1b |
|---|---|---|
| **Besitzer im Auto** | nichts haelt ein Tier davon ab, hinterherzulaufen; ein Auto, das ein Tier trifft, kostet Leben (`forschung_engine.md:601`) | `p:getVehicle()` (BELEGT, 1.1) -> sofort "Bleiben" + Meldung. Mitfahren ist nicht B1b |
| **Treppe / andere Ebene** | `pathToAux` nimmt die gerade Linie nur auf GLEICHER Ebene, sonst die Wegsuche (`dec_b1b/IsoGameCharacter.java:6152-6195`). Die Definition kennt `canClimbStairs` (Vorgabe aus, `V:shared/Definitions/animal/RaccoonDefinitions.lua:143` "most animals can't climb stairs, this is defaulted to false"), aber der einzige Leser im Jar ist eine Abfrage ohne Wirkung (`IsoMovingObject.doStairs`, javap Offset 33-43: beide Zweige springen nach 43); in den Pfadfinder-Klassen kein Treffer | **ungeprueft**, ob das Junge Treppen nimmt. Vorschlag: nur auf gleicher Ebene folgen; ist der Besitzer auf einer anderen Ebene, wartet das Junge (halten), statt einen Weg zu suchen; Testpunkt fuer Kevin |
| **Geschlossene Tuer** | Tiere kommen nur durch OFFENE Tueren (`isUnblockedDoorN/W`), sonst blockt die Kante; durchbrechen nur mit `canThump` (`dec_b1b/VGAStar.java:169-200`, `:276-287`); das Junge hat `canThump = false` (`S:shared/BanditsNPCBearDefs.lua:93`) | Weg scheitert -> Wandfolge -> Wiederholung (1.1). Unser Takt: Fortschritt pruefen, gedrosselt neu versuchen, nie endlos schnell |
| **Zaun** | `animalCantClimb = isAnimal && !canClimbFences` (`dec_b1b/SearchNode.java:70`); das Junge hat `canClimbFences` nicht (Vorgabe false) | ein Zaun haelt das Junge auf (wie Vieh im Gehege) -- ungeprueft im Spiel |
| **Gegend entladen** | Kachel entladen -> Tier wird virtuell und kommt beim Laden an derselben Stelle zurueck (`forschung_engine.md:105-117`); Ziel ausserhalb geladener Kacheln -> blindes Weiterlaufen (1.1) | Deckel "zu weit weg" (Sandbox) deutlich unter der geladenen Flaeche (CLAUDE.md: ~76 Kacheln; B1a deckelt Platzsuchen bei 65, `S:server/BanditsNPCBearWorld.lua:158`), dazu `B.AreaLoaded` um das Junge (`S:server/BanditsNPCBearWorld.lua:104-115`) |
| **Besitzer offline / tot (MP)** | Spieler fehlt in `B.Players()` (`S:server/BanditsNPCBearWorld.lua:29-45`, `isDead`-Filter) | "Bleiben" am jetzigen Ort; Meldung erst, wenn er wieder da ist (Planer) |
| **Laerm / Schuss / Q-Ruf** | Befund 0.4. Waehrend ein Laerm gemerkt ist und das Tier laeuft, fragt `respondToSound` nicht neu (`dec/IsoAnimal.java:764-776`); ein neuer `pathToLocation` von uns ersetzt das Ziel der Flucht | Folgen: weicht das Junge weg, im naechsten Hirn-Takt neuer Weg zum Besitzer. Bleiben: die Heimat-Regel holt es zurueck (B1a Regel 8, `S:shared/BanditsNPCBearRules.lua:314-317`) |
| **Wandern im Stand** | Wander-Wurf +-8 Kacheln um das Tier selbst (`dec/BaseAnimalBehavior.java:165-225`, Wurf `:186`), `wanderMul = 600` (`S:shared/BanditsNPCBearDefs.lua:101`) | Bleiben: Wandern zulassen, ueber `homeR` zurueckholen (= "kleiner Radius"); Folgen in der Naehe: halten (`setBlockMovement(true)` je Takt), sonst wandert es vom Besitzer weg |

### 1.5 respondToSound / callOut (Q) mit einem zahmen Jungen -- stoert es oder hilft es?

- Q-Ruf (`dec_b1b/IsoGameCharacter.java:4956-5038`): Radius 30 (Megafon 90, geschlichen 6/18); `addSound(..., stressAnimals = true)`
  (Parameterfolge `dec/WorldSoundManager.java:95-121`); `callOut = true` (`:5037`), wird zurueckgesetzt, sobald die Figur nicht mehr
  spricht (`:7183-7189`).
- Tier hoert ihn, wenn der Laerm Tiere stresst und es im Radius steht (nicht wild: Radius x1, `dec/WorldSoundManager.java:241-271`, `:370-400`).
- Akzeptanz >= 40 -> `pathToLocation` zum Spieler, **ohne** den Rennen-Merker zu aendern; sonst Flucht `radius + 10` = 40 Kacheln
  im Rennen (`dec/IsoAnimal.java:782-803`).
- Akzeptanz haengt an der OnlineID des Spielers (`forschung_engine.md:269-272`) und steigt nur ueber `petAnimal` (B1a ruft es auch am
  zahmen Jungen, `S:server/BanditsNPCBearServer.lua:268`) bzw. `feedFromHand` (benutzen wir nicht).
- **Urteil:** stoert eher (Spielbeleg Erwachsener, `ENTSCHEIDUNGEN.md:97`); hilft erst, wenn die Akzeptanz >= 40 ist -- dann aber
  zufaellig je Neuverbindung (MP). Nicht als Folgen-Weg einplanen; im Takt abfangen (1.4). Ein eigener "Komm her" ist B2b
  (`ENTSCHEIDUNGEN.md:97`, `PLAN.md:193-194`).

### 1.6 Speichern/Laden, SP/MP

- Zustand Folgen/Bleiben und Heimat ins Register (globale ModData beim Schreiber, `S:server/BanditsNPCBearRegistry.lua:65-107`;
  Vanilla `V:server/Foraging/forageServer.lua:26`). Die Sperre am Tier wird nicht gespeichert (`forschung_engine.md:113-114`) -> nach dem
  Laden setzt der Takt sie neu.
- Bitte vom Client: `B.Ask(player, "Mode", { id, mode })` -> `B.Handle` (`S:shared/BanditsNPCBear.lua:425-434`,
  `S:server/BanditsNPCBearServer.lua:365-386`); im SP direkt (sendServerCommand tut dort nichts, `forschung_engine.md:282`). Der Server
  prueft Besitz (`rec.owner == B.PlayerKey(player)`) und Zustand `tame`; nur `LoginOnServer` noetig -> kein Kick.
- Sicht: neues Feld `mode` (und `name`) im Sicht-Eintrag (`S:server/BanditsNPCBearRegistry.lua:398-410`); `B.Touch`/`B.FlushViews`
  verteilen es schon an Besitzer und Nahe (`S:server/BanditsNPCBearRegistry.lua:43-63`, `S:server/BanditsNPCBearServer.lua:74-99`).

---

## 2. Namensschild (Auftrag Punkt 2; Forschung c)

### 2.1 Wie die Test-Mod heute den Balken zeichnet (`S:client/ISUI/BanditsNPCBearHud.lua`, gleich in NCBearTest)

- Ein `ISPanel` 1x1 in der Ecke, nie unsichtbar, Maus-Funktionen `false` (`:8-17`, `:337-340`, `:369-376`; Vorbild
  `V:client/ISUI/ISButtonPrompt.lua:1244`, `NC:client/ISUI/BanditsNPCNameTags.lua:41-62`).
- Liste hoechstens 1x je Sekunde (`LIST_MS`, `:32`, `:348-353`), Suchlauf `getCell():getObjectListForLua()` nur fuer gesuchte Junge ohne
  Objekt, gedrosselt (`:109-121`, `:225-245`), Deckel `hudDist 20` / `hudMax 6` (`S:shared/BanditsNPCBear.lua:50`).
- Je Bild: `isoToScreenX/Y(0, x, y, z + barZ)` (`V:client/Fishing/TensionUI.lua:11-12`), zwei Rechtecke, ein Rahmen, zwei Texte mit Schatten
  (`drawTextCentre`, `V:client/ISUI/ISUIElement.lua:1280`), `UIFont.Small` (`:284-335`). Anker = `a:getZ() + B.CFG.barZ` mit `barZ = 0.55`
  (`:295`, `:303`); der Block waechst nach OBEN (Zeile 2 bei `sy - fh`, Balken darueber, Zeile 1 darueber, `:312-324`).
- Gezeichnet werden nur ungezaehmte Junge und die 5 s "Tamed!" danach (`wanted`, `:88-93`) -- deshalb steht nach dem Zaehmen nichts mehr
  (Kevins Beobachtung).
- Spielbeleg: Kevins Bildschirmfoto "Taming 33% / Food: 50 min / Petting: ready" gut lesbar (`ENTSCHEIDUNGEN.md:184`), aber zu hoch ueber
  dem kleinen Jungen (`baer/STAND.md` Screenshot ~22:50).

### 2.2 Kopfhoehe des Jungen (gerechnet, nicht gemessen)

- Platzhalter-GLB: hoechster Punkt des Netzes y = 0,556 Modell-Einheiten bei Groesse 1,0 (heute aus den Accessor-Grenzen gelesen).
- Engine zeichnet Tiere mit `1.5 * getAnimalSize()` (Jar `dec/IsoAnimal.java:2602`), Hoehe in Ebenen = Einheiten / 2,44949 (`:2609`);
  Groesse 0,35 (`S:shared/BanditsNPCBearDefs.lua:75-76`).
- Oberkante Junges ~ 0,556 x 1,5 x 0,35 / 2,449 = **~0,12 Ebenen** ueber dem Boden. Gegenprobe Mensch: 0,98 E x 1,5 / 2,449 = 0,60
  (NPC Crew misst den Anker ueber dem Kopf bei 0,6667, `NC:client/ISUI/BanditsNPCNameTags.lua:63-70`) -- die Rechnung passt.
- Heute 0,55 = rund das Viereinhalbfache der Jungen-Hoehe. **Vorschlag: gemeinsamer Stellwert (z. B. `tagZ`) um 0,15-0,20**, fuer Balken
  UND Schild derselbe Anker; einstellbar ueber die vorhandene Testhilfe `NCBear_CubSet("barZ", wert)` (`S:client/NCBearBenchCub.lua:20`,
  `:349-372`). Das neue Generator-Modell kann anders hoch sein -> im Spiel nachstellen (NPC-Crew-Lehre "wer eine Zahl raten muss, baut den
  Regler gleich mit", `NC:client/ISUI/BanditsNPCNameTags.lua:78-93`).
- Kein Zoom-Teilen: der Anker folgt dem Zoom schon in `isoToScreenY`, die Schrift bleibt in Bildschirmpixeln
  (`NC:client/ISUI/BanditsNPCNameTags.lua:95-100`).
- `getAttachmentWorldPos("head")` waere der Kopfpunkt (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:752`), braucht aber ein
  `attachment head` im Modell-Skript (fehlt, `S:../scripts/nc_bear_cub.txt`) und rechnet Matrizen -> nicht je Bild.

### 2.3 Wie Vanilla und NPC Crew Namen billig zeichnen

| Weg | Fundstelle | Urteil |
|---|---|---|
| `drawTextCentre(str, x, y, r, g, b, a, font)` aus einem 1x1-Panel, Liste gedrosselt | `V:client/ISUI/ISUIElement.lua:1280`; `NC:client/ISUI/BanditsNPCNameTags.lua:979-1037` (gespielt); B1a-Hud (gespielt) | **empfohlen** (derselbe Weg wie der Balken) |
| `TextDrawObject.new(...)`, `:ReadString(font, text, -1)`, `:Draw(x, y)` (Text-Aufbau gemerkt) | `V:client/ISUI/ISMoveableInfoWindow.lua:384-392` (anlegen), `:130` (`self.header:Draw(...)` in `render`) | BELEGT, Alternative, nur noetig, wenn viele Schilder; `AddBatchedDraw` (Engine-Weg, `dec/IsoAnimal.java:984`) hat keine Lua-Fundstelle |
| Vanillas eigenes Tier-Namensschild | Jar `dec/IsoAnimal.java:946-985`: nur bei `player.isSeeDesignationZone()`, Anker Kopf-Anhaengepunkt oder z + 0,5 | nicht benutzbar (Zonen-Ansicht); nur wissen: mit `customName` erscheint dort ein zweites Schild |
| Schrift Zeile 2 kleiner | `UIFont.Small` (ueberall); `UIFont.NewSmall` mit `drawText` belegt `V:client/ISUI/Animal/ISAddDesignationAnimalZoneUI.lua:261` | ob NewSmall kleiner ist: **ungeprueft**; sonst Zeile 2 nur blasser |

### 2.4 Name, Besitzer, Zustand in der Sicht

- Hat ein Tier schon einen Namen? Ja: `getCustomName()` / `setCustomName(text)` (`V:client/ISUI/Animal/ISAnimalUI.lua:474`, `:481`;
  Server `V:server/ClientCommands.lua:1120-1121`); `getFullName()` nimmt ihn, sonst "Rasse + Art" (`dec/IsoAnimal.java:2249-2271`;
  `V:client/ISUI/Animal/ISAnimalContextMenu.lua:140`). Ein `getData():getName()` gibt es nicht (Jar `dec/AnimalData.java`, nur Icon-Namen).
- Achtung Menue: B1a findet Vanillas Untermenue ueber `animal:getFullName()` (`S:client/BanditsNPCBearMenu.lua:53-63`, `:215`). Bekommt
  das Junge einen `customName`, aendert sich der Eintragsname -- bleibt aber stimmig, weil beide Seiten `getFullName()` fragen.
- Vorgabe-Name "<Spielername>'s cub": je Sprache per Textschluessel mit `%1`. Spielername: im SP der Vorname der Figur
  `player:getDescriptor():getForename()` (`V:client/XpSystem/ISUI/ISCharacterScreen.lua:84`, nur Client belegt), im MP der Kontoname
  `getUsername()` (`V:shared/Traps/TrapSystem.lua:45`; steht schon als `owner` in der Sicht, `S:server/BanditsNPCBearRegistry.lua:408`).
  Der Server muss den Vornamen nicht kennen: der Client setzt den Vorgabe-Namen beim Zeichnen zusammen.
- Fremde Junge (MP): die Sicht traegt schon alle Jungen in `tellDist 60` (`S:server/BanditsNPCBearRegistry.lua:412-435`) mit `owner`;
  dazu `name` und `mode` -> Zeile 1 Name, Zeile 2 Besitzer. Keine neue Uebertragung noetig.
- Ein/Aus je Spieler (Kevin 08.11.: `ENTSCHEIDUNGEN.md:103`, `:106`) ist eine Client-Einstellung und gehoert zum Baeren-Fenster (spaeter);
  fuer B1b nur vormerken.

---

## 3. Umbenennen (Auftrag Punkt 3; Forschung d)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Eingabefenster | `ISTextBox:new(0, 0, 280, 180, titel, vorgabe, ziel, rueckruf)`, `:initialise()`, `:addToUIManager()` | `V:client/ISUI/Animal/ISAnimalUI.lua:459-469` (Tier umbenennen, genau so); Signatur `V:client/ISUI/ISTextBox.lua:280` | Client | **BELEGT** |
| Laenge begrenzen | `modal.maxChars = 30` (OK-Knopf grau + Tooltip) | `V:client/ISUI/Animal/ISAnimalUI.lua:463`; Wirkung `V:client/ISUI/ISTextBox.lua:178-181` | Client | **BELEGT** |
| harte Grenze im Feld | `modal.entry:setMaxTextLength(n)` nach `initialise` | `ISTextEntryBox:setMaxTextLength` `V:client/ISUI/ISTextEntryBox.lua:170-172`, Aufruf `V:client/ISUI/ISMPEditAccount.lua:19`; das Feld entsteht in `ISTextBox:initialise` (`V:client/ISUI/ISTextBox.lua:8-23`); NC macht es so `NC:client/BanditsNPCVesselNameUI.lua:100-102` | Client | **BELEGT** |
| leere Eingabe sperren | `modal.noEmpty = true` | `V:client/ISUI/Maps/ISWorldMapSymbols.lua:203`; Wirkung `V:client/ISUI/ISTextBox.lua:182-185` | Client | **BELEGT** |
| eigene Pruefung (Zeichen) | `modal:setValidateFunction(ziel, fn)` | `V:client/OptionScreens/CharacterCreationProfession.lua:1297` (Pruefer `:1272-1275` lehnt `/ \ : ; "` ab); Wirkung `V:client/ISUI/ISTextBox.lua:111-115`, `:176-177` | Client | **BELEGT** |
| Antwort lesen | `button.internal == "OK"`, `button.parent.entry:getText()` | `V:client/ISUI/Animal/ISAnimalUI.lua:471-485` | Client | **BELEGT** |
| Joypad | `modal:centerOnScreen(playerNum)` + Fokus | `V:client/ISUI/Animal/ISAnimalUI.lua:464-468` | Client | **BELEGT** |
| nur druckbare Zeichen | `string.byte(s, i)` je Zeichen, >= 32 und ~= 127 | Lua-Grundbibliothek (kein Engine-Aufruf); gespielt in `NC:server/BanditsNPCCorpseJobServer.lua:289-296`, `NC:shared/BanditsNPCEditorData.lua:1000-1020`; Vanilla nutzt es nicht (grep 0) | beide | **erlaubt** (Lua, kein Engine-Aufruf). Kahlua-Strings sind Java-Strings: `string.byte` liefert Zeichencodes ueber 255 fuer Umlaute/Kyrillisch/Koreanisch/Chinesisch -> nicht abweisen (nur < 32 und 127) -- **ungeprueft im Spiel** |
| Server prueft und verteilt | eigene Bitte `B.Ask(player, "Rename", { id, name })` -> `B.Handle`: Besitz, Typ `string`, Laenge (Vanilla: 30, `V:server/ClientCommands.lua:1107-1111`), Zeichen, trimmen | `S:shared/BanditsNPCBear.lua:425-434`; `S:server/BanditsNPCBearServer.lua:365-399`; `string.trim` `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:42` | Server / SP direkt | **BELEGT**, kein Kick (nur LoginOnServer) |
| Name am Tier spiegeln | `animal:setCustomName(name)` beim Schreiber | Server `V:server/ClientCommands.lua:1121`; SP `V:client/ISUI/Animal/ISAnimalUI.lua:481` | Schreiber | **BELEGT**; Verteilung an Clients ueber das Tierpaket (Jar `dec_b1b/NetworkPlayerAI.java:267-269`, `:467-468`, nur nicht-leere Namen); gespeichert (`dec/IsoAnimal.java:1275`) |

**Falle "jeder darf umbenennen":** Vanillas "Animal info" steht fuer jedes nicht wilde Tier offen (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:152-171`),
der Server-Befehl `animal.rename` prueft keinen Besitz (`V:server/ClientCommands.lua:1102-1123`). Wege (Planer waehlt):
- (A) Name nur im Register, KEIN `setCustomName` -> Vanilla zeigt "Brown Bear cub", unser Schild den Namen; eine Vanilla-Umbenennung
  stoert unser Schild nicht.
- (B) Register ist die Wahrheit, `customName` ist Spiegel; der Langsam-Takt setzt ihn zurueck, wenn er abweicht (nur geladene Junge,
  ein Textvergleich). SP: eine Vanilla-Umbenennung durch Kevin wuerde dann still zurueckgedreht -> dort lieber uebernehmen.
- (C) zusaetzlich Vanillas Befehl mithoeren: `Events.OnClientCommand` bekommt jedes Modul (`V:server/ClientCommands.lua:1346-1357`);
  bei `module == "animal"`, `command == "rename"` und unserem Jungen: Besitzer -> ins Register uebernehmen, sonst zuruecksetzen.
  Reihenfolge der Empfaenger: ungeprueft (deshalb im naechsten Takt vergleichen, nicht im selben Aufruf).

---

## 4. Futter hinhalten (Auftrag Punkt 4; Forschung e)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Welt-Rechtsklick | `Events.OnFillWorldObjectContextMenu.Add(f(player, context, worldobjects, test))` | `V:client/ISUI/Hutch/ISHutchMenu.lua:3-8`, `:115`; Ausloeser `V:client/ISUI/ISWorldObjectContextMenu.lua:213`; B1a hat den Empfaenger schon (`S:client/BanditsNPCBearMenu.lua:280-327`) | Client | **BELEGT** |
| Punkt mit Untermenue | `context:addOption(text)`, `ISContextMenu:getNew(context)`, `context:addSubMenu(opt, sub)`, `sub:addOption(text, ziel, fn, arg...)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:48-49`, `:272-280`; so in B1a `S:client/BanditsNPCBearMenu.lua:126-155`, `:268-277` | Client | **BELEGT** |
| Futterliste | `B.FoodList(player, max)` (eigener Code, `getAllEvalRecurse`) | `S:shared/BanditsNPCBearFood.lua:73-119`; Vanilla `V:client/ISUI/Animal/ISAnimalContextMenu.lua:33-53` | Client | **BELEGT** |
| in die Hand nehmen | `ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:93` (**nachgeprueft: steht dort mit Futter**, in `onFeedAnimalFood` `:85-95`); Funktion `V:client/ISUI/ISWorldObjectContextMenu.lua:2594-2622` (holt aus Taschen per `transferIfNeeded` `:2587-2591`, stellt `ISEquipWeaponAction` an); B1a `S:client/BanditsNPCBearMenu.lua:79` | Client stellt an, `ISEquipWeaponAction:complete` setzt die Hand (`V:shared/TimedActions/ISEquipWeaponAction.lua:138-...`, im MP am Server) | **BELEGT** |
| warum es den Punkt braucht | Vanilla bietet "Ausruesten" fuer Essen nicht an | `V:client/ISUI/ISInventoryPaneContextMenu.lua:431` `if tests.isWeapon and not tests.isAllFood ...` | Client | bestaetigt (N6) |
| Server sieht die Hand | `p:getPrimaryHandItem()` + `B.FoodClass` | `S:server/BanditsNPCBearServer.lua:578-591` (`playerInfo`), Beleg `V:server/BuildingObjects/ISEmptyGraves.lua:18` | Schreiber | **BELEGT** |

**Was die bestehende Regel daraus macht** (`S:server/BanditsNPCBearServer.lua:597-632`, `S:shared/BanditsNPCBearRules.lua:271-321`):
- Lock-Spieler: scheues Junges (`new`/`shy`) -> jeder; `fed` -> nur `bond`; zahm -> nur `owner` (`keysOf`, `:598-602`). Wirkt bis
  `lureDist 15` (`S:shared/BanditsNPCBear.lua:35`), nur wenn der Spieler NICHT rennt (`:617`).
- Scheu: Regel 1 Flucht nur, wenn naeher als `shyDist 6` OHNE Futter oder im Lauf; Regel 2 steht der Spieler still (`stillEps 0.3` je Takt)
  -> Junges kommt bis `comeUnfed 3`; Regel 3 Futter in der Naehe -> stehen bleiben (`setBlockMovement`). Zahm/fed: Regeln 6/7 entsprechend.
- Ablauf fuer Kevin: "Hold out food" -> Futter in der Hand -> stehen bleiben -> Junges kommt bis ~3 Kacheln und haelt -> Rechtsklick
  auf das Junge "Feed" (geht ohne Hingehen nur in Klickweite; `onFeed` geht mit `walkAdj` hin, gehend = kein "fast", Regel 3 haelt).
- **Fallen:** `ISEquipWeaponAction` hat `stopOnRun = true` (`V:shared/TimedActions/ISEquipWeaponAction.lua:258`) -> "Hold out food" im
  Rennen bricht ab; `stopOnWalk = false` (`:257`) -> im Gehen klappt es. Ein Gegenstand in der Hand faellt beim Gehen/Rennen nicht von
  selbst heraus: `forceDropHeavyItems` greift nur bei schweren Dingen (`V:shared/TimedActions/ISEquipWeaponAction.lua:75-95`,
  `isForceDropHeavyItem`) -- sonst kein Vanilla-Code, der beim Laufen ablegt (**ungeprueft im Spiel**).
- "In der Naehe": die Sicht kennt die Jungen in 60 Kacheln, aber ohne Ort (`S:server/BanditsNPCBearRegistry.lua:398-410`). Fuer "nur
  anbieten, wenn ein Junges in ~lureDist ist" entweder die Hud-Objekte (Client-Kopie, `S:client/ISUI/BanditsNPCBearHud.lua:60`) oder
  `x, y` in den Sicht-Eintrag aufnehmen (billig, Server kennt `rec.x/y`). Nur Anzeige -- entscheiden tut weiter der Server.
- Vanillas eigenes Locken ("ContextMenu_Lure", `eatFromLured`) bleibt aus: es frisst am Register vorbei und gibt Akzeptanz +5
  (`dec/IsoAnimal.java:2579-2588`).

---

## 5. N5 Waisen (Forschung f)

Heute (`S:server/BanditsNPCBearWorld.lua:285-358`):
- Junges mit Spiegel und Eintrag + passende AnimalID -> gebunden (`:309-316`).
- Spiegel auf GESCHLOSSENEN Eintrag und Spiegel-Zustand `new`/`shy` -> `stale` -> entfernt, wenn niemand naeher als `vanishKeep 25`
  und keiner hinsieht (`:301-307`, `:346-356`).
- Spiegel `fed`/`tame` ohne Eintrag -> bleibt (wird beim Anfassen ueber `B.RecOf` als `found` neu aufgenommen, `S:server/BanditsNPCBearRegistry.lua:185-219`).
- **Kein Spiegel** -> `loose` -> nur der AnimalID-Rueckfall fuer Eintraege OHNE Objekt (gleiche AnimalID, genau ein Kandidat, <= 40 Kacheln,
  `:323-345`). Was danach in `loose` uebrig bleibt (`loose[j] ~= false`), wird **nie** angefasst = Kevins zweites Junges.
- Suchlauf nur, wenn ein Eintrag sein Objekt in geladener Gegend vermisst (`S:server/BanditsNPCBearServer.lua:696-715`, `:816-823`); ohne
  Eintraege laeuft der Hirn-Takt nur alle 10 s und sucht gar nicht (`B._live`, `:843-849`, `:853-859`).

Was fehlt:
1. Nach dem AnimalID-Durchgang die Uebriggebliebenen ohne Spiegel als Waisen sammeln und wie `stale` entfernen (gleiche Riegel:
   `vanishKeep`, `B.SeenInSP`, nur `B.RemoveCub` -> Server `removeAnimal`, `S:server/BanditsNPCBearWorld.lua:248-256`).
2. Ein seltener eigener Suchlauf auch ohne vermisste Eintraege (z. B. im Langsam-Takt, `S:server/BanditsNPCBearServer.lua:540-562`;
   `getObjectListForLua` kopiert die ganze Liste, `forschung_engine.md:79`), mit Deckel je Lauf.
3. Riegel gegen Fehlgriff: ein Junges, das gerade jemand anfasst, ist durch `vanishKeep 25` geschuetzt; ein zahmes Junges, dessen Spiegel
   ein Client geloescht hat (`forschung_engine.md:253-256`), wird vorher ueber den AnimalID-Rueckfall wieder gebunden -- **nur wenn sein
   Eintrag gerade kein Objekt hat**. Hat der Eintrag schon ein lebendes Objekt, ist das zweite Tier mit gleicher AnimalID wirklich ein
   Doppel. Im MP gilt "ausser Sicht" nur ueber den Abstand (`S:server/BanditsNPCBearWorld.lua:117-128`).
4. Server-Beleg fuer `getObjectListForLua` und `getAnimalID` fehlt weiter (A3, `S:server/BanditsNPCBearWorld.lua:275-276`) -- MP offen wie in B1a.

---

## 6. Sandbox (Forschung g)

Aufbau heute (`S:../sandbox-options.txt:1-159`, 19 Optionen): `VERSION = 1,`, C-Kommentare, je Option
`option BanditsNPC.<Name> { type = boolean|integer|enum, (min, max,) default, page = BanditsNPC, translation = BanditsNPC_<Name>, }`,
Enum mit `numValues` + `valueTranslation` (`:16-23`). Dieselben Zahlen stehen in `B.OPTS` (`S:shared/BanditsNPCBear.lua:67-87`); gelesen
ueber `B.Opt` (`:112-131`: mit NPC Crew ueber `BanditsNPC.Opt`, sonst `SandboxVars.BanditsNPC`, Typpruefung, Klemmen, nil -> Vorgabe).
Texte `Translate/<L>/Sandbox.json`: `Sandbox_BanditsNPC` (Seitentitel), `Sandbox_BanditsNPC_<Name>`, `..._tooltip`, bei Enum `..._optionN`
(`S:shared/Translate/EN/Sandbox.json:2-30`). Engine-Beleg fuer das Format: `forschung_engine.md:552-570`.

Bedarf B1b:
| Option (Vorschlag) | Typ / Bereich | Wofuer |
|---|---|---|
| `BanditsNPC.BearFollowMaxDistance` | integer, z. B. min 10, max 60, Vorgabe 40 | Kevins Deckel "zu weit weg" -> Wechsel auf Bleiben. Max unter der geladenen Flaeche (1.4) |

Alles andere als Stellwert in `B.CFG` (nicht Sandbox): Folge-Abstand 2-4, Lauf-Schwelle ~5, Bleiben-Radius (heute `homeR 10`), Anker
`tagZ`/`barZ`, Namenslaenge (Vanilla 30). Name frei: grep `BearFollow|BearStay|UI_BN_Bear_|BanditsNPCBear` ueber NPC Crew `42/media/lua`: 0;
`sandbox-options.txt` von NPC Crew: kein `Bear` (42 Optionen).

---

## 7. NUR im Jar belegt (getrennt) -- nicht als Engine-Aufruf benutzen ohne Kevins Wort

| Methode | Wofuer sie locken wuerde | Ersatz |
|---|---|---|
| `animal:isAnimalMoving()` | Ankunft/Haengen | Lagevergleich (1.1) |
| `animal:pathToCharacter(chr)` | dem Spieler direkt folgen | `pathToLocation` auf einen Punkt neben dem Besitzer (ERLAUBT) |
| `getData():setAttachedPlayer(p)` / Seil | Vanillas Folgen | eigener Takt (1.2) |
| `animal:setShouldFollowWall(b)` | Wandfolge abschalten | keiner noetig |
| `TextDrawObject:AddBatchedDraw` | Engine-Namensweg | `drawTextCentre` oder `TextDrawObject:Draw` (BELEGT, 2.3) |
| `getAttachmentWorldPos` ohne `attachment head` | Kopfpunkt | fester Stellwert (2.2) |
| Grenzfall (BELEGT am Spieler/Zombie und in T:, am Tier nicht in Vanilla): `animal:setVariable("animalRunning", false)` | gehen statt rennen | Kevins Wort empfohlen; sonst nur `fleeTo` (rennt) |

---

## 8. Offene Fragen (fuer Planer / Kevin)

1. **Gehen:** Kevins Wort fuer `animal:setVariable("animalRunning", false)`? (Ohne: Folgen rennt immer; mit den Platzhalter-Clips muss
   es zum Mitgehen ohnehin rennen.)
2. **Tempo:** das Junge rennt ~2,5 Kacheln/s; ein rennender Besitzer haengt es ab (Deckel greift). Schnellere Clips (SPEZ_BABY.md 4:
   "trippelt schneller") gehoeren zum Modell-Lauf -- Kevin fragen oder bewusst so lassen.
3. **Name am Tier:** Weg A/B/C (Abschnitt 3). Empfehlung: B mit SP-Ausnahme oder C; A ist am einfachsten.
4. **Andere Ebene / geschlossene Tuer:** warten (halten) oder nach N Sekunden ohne Fortschritt mit Meldung auf Bleiben? (Kevins Liste nennt
   nur Auto, zu weit, entladen; "nichts haengt endlos" verlangt einen Deckel.)
5. **Besitzer offline (MP):** sofort Bleiben; Meldung beim naechsten Einloggen oder gar keine?
6. **Folgen nah am Besitzer:** halten (steht still) oder wandern lassen und zurueckholen? Vanilla-Seil laesst es um den Spieler wandern.
7. **Laerm/Q:** Flucht nur im Takt zuruecknehmen (so geplant) -- oder soll Bleiben/Folgen kurz "erschrocken" bleiben duerfen?
8. Ungeprueft und im Spiel zuerst ansehen: Treppen; Zaun/Tuer; ob `isRunning` fremder Spieler am Server stimmt; `UIFont.NewSmall`-Groesse;
   `string.byte` mit Nicht-ASCII-Namen; Schildhoehe 0,15-0,20 am neuen Modell; MP: Tierpaket bringt den Namen (`customName`) zu allen.

Statisch geprueft, nicht gespielt.
