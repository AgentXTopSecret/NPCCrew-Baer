# Forschung B: Zustand und Animation beim Laerm-Abbruch (Lauf baer-laerm, 08.11.2026)

Statisch geprueft, nicht gespielt. Alles aus Jar-Dumps (`javap -c -p`) und Vanilla-/Bandits-Lua. Neue Dumps dieses Laufs liegen
als `B_*.txt` in `_arbeit/baer_laerm/` (Klassen nach `_arbeit/baer_laerm/jar/` gezogen). Altbestand: `_arbeit/baer_angriff/*.txt`
(IsoAnimal, IsoGameCharacter, IsoPlayer, BaseAnimalBehavior), `_arbeit/baer_kampf/animlayer_t.txt`, `ingame_t.txt`, `wsm.txt`.
Zitierweise: Datei:Zeile im Dump bzw. Klasse.Methode Offset (Bytecode-Offset).

## Kurzbefund

1. **Kein Lua-Ereignis laeuft verlaesslich zwischen respondToSound und dem Anim-Zustandswechsel.** respondToSound setzt
   `bPathfind`/`moving` in `update()`, die ActionGroup wechselt in `postupdate()` desselben Bildes, OnTick kommt erst danach.
2. **Ein Clip ueberlebt keinen Wechsel des Aktionszustands, auch nicht mit gleichnamigem Knoten.** `transitionTo` markiert ALLE
   lebenden Knoten `transitioningOut`, `findLiveNode` ueberspringt genau diese. Jeder Ausflug idle->pathfind->idle startet unseren
   Clip bei 0 neu (daher "2x Schrei").
3. **Unser fleeStop verlaengert den Ausflug selbst:** Im Fall "pathfind" ist der KI-Zustand beim Stopp noch AnimalIdleState,
   `changeState(idle)` ist dann wirkungslos, `bPathfind` bleibt true -> naechstes Bild betritt der Baer AnimalPathFindState mit
   zurueckgesetzter Pfadsuche (Ziel = eigener Standort). Und nach jedem Stopp prueft respondToSound den Laerm neu (Baer "steht")
   -> solange der Laerm in der Liste lebt, Flucht -> Stopp -> Flucht ... alle 2-3 Bilder.
4. Der eigentliche Hebel liegt deshalb auf der **Laerm-Seite** (Forschung A). Von der Zustandsseite gibt es nur Schadensbegrenzung
   (Lua, belegt): bPathfind beim Stopp loeschen, Neustart erkennen und die Clip-Uhr neu starten, Aufrichten bei Neustart abbrechen,
   im Anlauf den Weg neu setzen, wenn die Engine ihn ueberschrieben hat.

---

## 1. Reihenfolge in einem Bild

### 1.1 Der Bildablauf (Einzelspieler)

| Schritt | Was | Beleg |
|---|---|---|
| 1 | `IngameState.updateInternal` ruft `IsoWorld.update` | `baer_kampf/ingame_t.txt:3831` (Offset 1067) |
| 1a | `IsoWorld.updateWorld`: zuerst `IsoCell.update` (darin ProcessObjects -> `MovingObjectUpdateScheduler.update`) | `B_IsoWorld.txt:8758` ff. (Offset 4), `B_IsoCell.txt:8478-8481` |
| 1b | Scheduler: je Objekt `preupdate`, `frameStep`, **`update()`** -- ALLE Objekte | `B_MOUSB.txt:70` ff. (Offset 133/138/143) |
| 1c | danach `CollisionManager.ResolveContacts` | `B_IsoWorld.txt` updateWorld Offset 16 |
| 1d | danach `MovingObjectUpdateScheduler.postupdate` -> je Objekt **`postupdate()`** ("Animation") | `B_IsoWorld.txt` updateWorld Offset 63-66, `B_MOUSB.txt:140` ff. (Offset 96) |
| 2 | `AnimalController.update`, Radio, UpdateStuff | `ingame_t.txt` Offset 1168/1235/1283 |
| 3 | **`onTick()` -> Lua `OnTick`** (unser NCBearFight) | `ingame_t.txt:3951` (Offset 1331), `onTick` `ingame_t.txt:4169-4171` |

### 1.2 Innerhalb von `IsoAnimal.update()` (Schritt 1b)

`baer_angriff/IsoAnimal.txt:921` ff.:
1. Offset 29-61: ist `bPathfind` true und der KI-Zustand nicht AnimalPathFindState -> `changeState(AnimalPathFindState)`.
2. Offset 64-76: `updateEmitter`, `doDeferredMovement` (Wurzelbewegung der Animation).
3. Offset 87: `updateInternal()` (`IsoAnimal.txt:1035`): `behavior.update()` (Offset 90), `data.update`, `separate`, `checkTreeExists`,
   `reattachToTree`, `checkZone` (137), `reattachBackToMom`, **`respondToSound` (145)**, petTimer, `updateStress` (187), `updateLured` (191),
   `updateEmitter`, `tryThump(null)`, `updateLOS` (205, darin `spotted`), dann `IsoPlayer.update` (234).
4. `IsoPlayer.updateInternal1`: fuer Tiere nur `IsoLivingCharacter.update` + `AnimalInstanceManager.update`, kein `updateInternal2`
   (`IsoPlayer.txt:5976` ff., Offset 1-49) -> **OnPlayerUpdate feuert fuer Tiere nie**.
5. `IsoGameCharacter.updateInternal` (`IsoGameCharacter.txt:24231`) -> **`StateMachine.update()`** (Offset 1707-1710,
   `IsoGameCharacter.txt:25030`) = `execute` des KI-Zustands (AnimalIdleState/AnimalPathFindState/AnimalWalkState).

### 1.3 Innerhalb von `postupdate()` (Schritt 1d)

`IsoPlayer.postupdate` -> `IsoLivingCharacter.postupdate` (`IsoPlayer.txt:10092-10128`) -> `IsoGameCharacter.postUpdateInternal`
-> `postUpdateAnimating` (`IsoGameCharacter.txt:29868` ff.):
- Offset 62-65: **`ActionContext.update()`** = Uebergangspruefung der ActionGroup (idle -> pathfind bei `bPathfind`, idle -> walk bei
  `bMoving` und nicht `bPathfind`; `media/actiongroups/buck/idle/to_pathfind.xml`, `to_walk.xml`).
- Offset 89-98: **`AdvancedAnimator.update()`** = AnimLayer.Update (Knoten waehlen, Clips laufen, Anim-Ereignisse wie
  `SetVariable NCBearHit=true` feuern hier).

### 1.4 Wer setzt `bPathfind` (und `bMoving`)?

| Wo | Was | Beleg |
|---|---|---|
| `IsoGameCharacter.pathToAux` | Linie frei (`PolygonalMap2.lineClearCollide`) -> `bPathfind=false`, `setMoving(true)`; sonst `bPathfind=true`, `setMoving(false)` -- **sofort, synchron** | `IsoGameCharacter.txt:15618` ff., Offset 224-271 |
| `IsoAnimal.pathToLocation` / `pathToCharacter` | `PathFindBehavior2.pathToLocation` (asynchrone Anfrage) + `pathToAux` | `IsoAnimal.txt:8076` ff. Offset 115-132; `pathToCharacter` Offset 91-112 |
| `IsoAnimal.fleeTo` (unser Anlauf) | `animalRunning=true`, `pathToLocation` | `IsoAnimal.txt:7629` ff. Offset 48-65 |
| `IsoAnimal.respondToSound` (Flucht) | `animalRunning=true`, `pathToLocation(weg vom Laerm)` | `IsoAnimal.txt:1934` ff. Offset 354-382 |
| `AnimalPathFindState.enter` | `bPathfind=true`, `bMoving=false` | `B_AnimalPathFindState.txt:22` (Offset 0-15) |
| `AnimalPathFindState.execute` Succeeded | `bPathfind=false`, `bMoving=false`, `setPath2(null)` | `B_AnimalPathFindState.txt:42` ff. Offset 162-183 |
| `AnimalPathFindState.exit` | `bPathfind=false`, `bMoving=false`, Anfrage abbrechen, `setPath2(null)`, `doBehaviorAction` | `B_AnimalPathFindState.txt:141` ff. Offset 0-61 |
| `AnimalWalkState.execute` (angestossen) | `pathToLocation(Pfadziel)`, ggf. `bPathfind=true` | `B_AnimalWalkState.txt:46` ff. Offset 14-61 |
| `AnimalIdleState.execute` | `bMoving` true -> `changeState(AnimalWalkState)` (im selben Update) | `B_AnimalIdleState.txt:26` ff. Offset 70-87 |
| `CanUsePathfindState` (Riegel fuer bPathfind in pathToAux) | IsoAnimal: `isLocalPlayer()` | `IsoAnimal.txt:1322` |

`bPathfind` ist eine gewoehnliche Variable (`setVariable(String, boolean)`), `bMoving` ist an `isMoving/setMoving` gebunden
(`IsoGameCharacter.txt:1748-1755`, Getter/Setter-Slot).

### 1.5 Der Ausflug Bild fuer Bild (Fall "Zaun": Linie nicht frei -> pathfind)

| Bild | update() | postupdate() | OnTick (wir) |
|---|---|---|---|
| N | respondToSound: Laerm -> `pathToLocation` -> `pathToAux`: `bPathfind=true`, `moving=false`. KI bleibt AnimalIdleState. | ActionContext: **idle -> pathfind**. AnimLayer: alle Knoten transitioningOut, Knoten `pathfindWait` (DeerStag_Idle01) blendet ein. Unser Clip ist verloren. | fleeStop sieht "pathfind": `stopAllMovementNow` = `setMoving(false)`, PFB2.reset (Ziel = eigener Standort), `setPath2(null)`, `changeState(idle)` -> **wirkungslos, KI ist schon idle** (`B_StateMachine.txt:65` changeRootState Offset 0-20: gleicher Zustand -> return, kein exit). **`bPathfind` bleibt true.** |
| N+1 | IsoAnimal.update Offset 29-61: bPathfind -> `changeState(AnimalPathFindState)` (enter: bPathfind=true, bMoving=false). respondToSound: Merker gesetzt, t>0, `isAnimalMoving()`=true -> return. PathFindState.execute -> PFB2.update: neue Anfrage Start=Ziel -> Working. | bleibt pathfind | fleeStop: "pathfind" -> stopAllMovementNow -> changeState(idle) -> **jetzt** PathFindState.exit: bPathfind=false |
| N+2 | respondToSound: Merker gesetzt, t>0, aber nicht in Bewegung -> `setMoving(false)`, Merker frei, **neu abfragen** -> lebt der Laerm noch: Flucht wie in N (Schleife) | ohne neue Flucht: **pathfind -> idle -> unser Knoten NEU bei 0** | -- |

Fall "offen" (Linie frei -> walk): Bild N `pathToAux` setzt `moving=true`, AnimalIdleState.execute wechselt im selben Update nach
AnimalWalkState (enter: bMoving=true), postupdate: idle -> walk; OnTick: fleeStop -> changeState(idle) -> WalkState.exit (bMoving=false);
N+1 postupdate: walk -> idle -> Clip neu. Heutiges console.txt (f:215302 ff.) zeigt auch "left idle (walk)".

### 1.6 Gibt es ein Lua-Ereignis zwischen respondToSound und dem Anim-Wechsel?

| Ereignis | Wann | Taugt? | Beleg |
|---|---|---|---|
| OnTick | nach ALLEN postupdates | nein, ein Bild zu spaet | `ingame_t.txt` Offset 1067 vs 1331 |
| OnPlayerUpdate | im Update-Durchlauf des Spielers (`IsoPlayer.updateInternal2`), also vor allen postupdates | **nicht verlaesslich**: `IsoCell.objectList` ist ein `HashSet` (`B_IsoCell.txt:585-588`), die Reihenfolge Baer/Spieler ist zufaellig (fest bis zum Umhashen). Nur wenn der Spieler NACH dem Baeren dran ist, laeuft es dazwischen. | `IsoPlayer.txt:6584` (Offset 1141); Vanilla-Fundstelle `media/lua/client/Tutorial/Steps.lua:1919` |
| OnZombieUpdate | im Update jedes Zombies | gleiche Reihenfolge-Falle, dazu teuer | `IsoZombie.txt:8685`; Bandits `BanditUpdate.lua:2638`, `BanditZombie.lua:209` |
| OnAIStateChange | synchron in `StateMachine.changeRootState` (Offset 54-68), jeder KI-Wechsel jedes Charakters | nur Fall "walk" (Wechsel nach AnimalWalkState im selben Update, vor postupdate); Fall "pathfind" kommt der KI-Wechsel erst in N+1 -> zu spaet. Feuert auch fuer jeden Zombie (Kosten). **Keine Vanilla-/Bandits-Lua-Fundstelle** -> braucht Kevins Wort (Jar-Beleg). Registriert ist es (String in `LuaEventManager.class`). | `B_StateMachine.txt:65` ff. |
| OnCharacterCollide / OnObjectCollide | nur bei Kollision (`IsoMovingObject.collideWith`) | nein | `B_IsoMovingObject.txt:455-475` |

**Ergebnis: keins.** Fuer den Zaun-Fall gibt es nachweislich keinen Lua-Zeitpunkt vor der Uebergangspruefung.

---

## 2. Bewegen PathFindState/WalkState/PFB2 den Baeren trotz blockMovement? Und vor Ende der Pfadsuche?

- `blockMovement` wird nur gelesen in BaseAnimalBehavior `wanderIdle` (`BaseAnimalBehavior.txt:66` Offset 1-53), `goAttack` (731),
  `checkBehavior` (1745/1786), `followChr` (4026) und `IsoAnimal.canDoAction` (`IsoAnimal.txt:7065`). **Nicht** in
  AnimalPathFindState, AnimalWalkState, PathFindBehavior2 (grep ueber `B_AnimalPathFindState.txt`, `B_AnimalWalkState.txt`,
  `B_PathFindBehavior2.txt`: kein Treffer). -> Ein Weg, der einmal gesetzt ist, wird gegangen, Sperre hin oder her.
- Bewegung: `PFB2.moveToPoint` nimmt die Laenge der Wurzelbewegung der Animation (`getDeferredMovement`) und schiebt den Baeren damit
  den Weg entlang, dreht ihn per `faceLocation` (`B_PathFindBehavior2.txt:3832` ff., Offset 118-279). Dazu am Wegende ein kleiner
  Schub `0,005 x Multiplikator` (Offset 1197-1235, Zeile ~3420). WalkState dreht per `setForwardDirection` zum Ziel (Offset 63-110).
- Pfadsuche noch nicht fertig: **ja, der Anim-Zustand ist dann schon "pathfind"** -- `bPathfind` setzt `pathToAux` synchron im
  selben Update, die ActionGroup wechselt im postupdate desselben Bildes. Mit `bMoving=false` spielt der Knoten `pathfindWait`
  (DeerStag_Idle01, ohne Bedingung, `AnimSets/buck/pathfind/pathfindWait.xml`). Der KI-Zustand AnimalPathFindState kommt erst ein Bild
  spaeter (IsoAnimal.update Offset 29-61). PFB2.update liefert `Working` solange `notyetfound` (`B_PathFindBehavior2.txt:2922` ff.,
  Offset 0-200); mit gefundenem Weg `setMoving(true)` + `setPath2` (Offset 480-495) -> Knoten `defaultPathfind`/`runPathfind`.

---

## 3. Kann ein Angriffs-Clip einen Ausflug idle->pathfind->idle ueberleben?

**Nein -- auch nicht mit gleichnamigen Knoten in pathfind/walk.**

- `AnimLayer.transitionTo(state)` setzt bei JEDEM Zustandswechsel `transitioningOut = true` auf allen lebenden Knoten
  (`baer_kampf/animlayer_t.txt:572` ff., Offset 196-245).
- `AnimLayer.findLiveNode` ueberspringt Knoten mit `transitioningOut` sofort (Offset 36-44) und nimmt sonst nur gleichen AnimNode
  oder gleichen parentState UND gleichen Namen (Offset 47-98) (`animlayer_t.txt:2606`).
- Also baut `getOrCreateLiveNode` nach jedem Wechsel einen NEUEN LiveAnimNode und startet seine Spur (`animlayer_t.txt:2577`
  Offset 16-24; `startLiveNodeTracks` 2657 ff. reicht nur die Geschwindigkeit weiter, keinen Startzeitpunkt; unsere Knoten haben
  `m_SyncTrackingEnabled false`). -> Clip ab 0. Ein gleichnamiger Knoten in `AnimSets/buck/pathfind` haette dazu noch einen anderen
  parentState.
- Ein neu gestarteter Knoten liefert seine Ereignisse ganz normal (Blend 0,15 s, Aufrichten 0,25 s; Treffer bei 0,40 x Dauer,
  `End` am Ende). Das Problem ist nur unsere Lua-Frist: sie zaehlt ab `beginAct`, nicht ab dem Neustart. Beispiel swipeR (1,5 s):
  Neustart bei 1,0 s -> Treffer bei 1,6 s (passt zu "swipeR: 0 hit"), Ende bei 2,5 s + Bilder -> Frist 2,5 s ist schon abgelaufen ->
  "did not finish". Aufrichten: Bruellen `PlaySound` bei 0,27 x 3,0 = 0,81 s nach JEDEM Start (`NCBear_Rear.xml:15-17`) -> "2x Schrei".
- Vanilla-Knoten: `pathfind/`: `defaultPathfind` (DeerStag_Walk, `bMoving=true`, Blend 0,20), `runPathfind` (erbt, DeerStag_Run,
  +`animalRunning=true`), `pathfindWait` (DeerStag_Idle01, keine Bedingung, Blend 0,40). `walk/`: `defaultWalk` (DeerStag_Walk,
  keine Bedingung, Blend 0,75), `run` (DeerStag_Run, `animalRunning=true`, 0,75). Keiner hat `m_ConditionPriority`; unsere 10 wuerde
  dort gewinnen (Auswahl `AnimState.getAnimNodes` mit `compareSelectionConditions`, `B_AnimState.txt:32` ff.).
- AnimSets mischen Mod- und Spieldateien (`AnimState.Parse` -> `ZomboidFileSystem.resolveAllFiles`, `B_AnimState.txt:160` ff. Offset
  33-39) -- deshalb laufen unsere Knoten in `idle/`. **ActionGroups mischen NICHT**: `ActionGroup.load` holt EIN Verzeichnis per
  `getMediaFile` und listet nur dessen Dateien (`B_ActionGroup.txt:36` ff. Offset 25-133), und `searchFolders` traegt nur Dateien in
  die Mod-Liste ein, keine Ordner (`B_ZFS.txt:686` ff.). Ein eigener Aktionszustand oder ein geaenderter `to_pathfind.xml` ist per Mod
  also nicht moeglich (passt zur alten Lehre "AnimSet muss eine Vanilla-Gruppe sein").

---

## 4. Andere Kandidaten waehrend des Angriffs (blockMovement=true, wild=false, fleeZombies=false, canBeAlerted=false)

| Kandidat | Riegel? | Beleg |
|---|---|---|
| `respondToSound` | **nein** (kein blockMovement, kein wild-Riegel fuer die Flucht) | `IsoAnimal.txt:1934` ff. |
| ... dort Spieler-`callOut` mit Akzeptanz >= 40 | nein: Weg ZUM Spieler (Offset 155-210), nur wenn Kevin ruft | dto. |
| `fleeFromAttacker` | ja, solange `getAttackedBy()` null (Offset 1-14); Zombies greifen Tiere nie an; ein Spielerschlag beendet unseren Kampf ohnehin ("hurt") | `BaseAnimalBehavior.txt:4350` |
| `fleeFromChr` mit Zombie | ja: `spotted` bricht bei Zombie und `fleeZombies=false` ab (Offset 435-454); `fleeFromChr` selbst Offset 302-352 | `BaseAnimalBehavior.txt:5021`, `:4561` |
| `fleeFromChr` mit Spieler | **teilweise**: zahm + `canBeAlerted=false` -> `spottedChr = Spieler`, `fleeFromChr()` (spotted Offset 1565-1634, Spieler in `spottingDist` 10). Dort: Spieler steht -> return (168-174); Akzeptanz >= 40 UND Stress < 70 -> return (267-290); sonst Zufall -> Weg weg vom Spieler (632-765). **Kein blockMovement-Riegel.** Jede Laerm-Flucht hebt den Stress um `Radius x 0,05` (respondToSound 341-351) -> viele Fluchten koennen Stress >= 70 machen -> dann flieht er vor dem gehenden Kevin (4 Kacheln!). Ungeprueft im Spiel. | `BaseAnimalBehavior.txt:4561`, `:5021` |
| `spotted` -> `goAttack` (attackIfStressed, Stress > 80) | ja: `attackIfStressed` Vorgabe false (nur Parser setzt es, `B_AnimalDefinitions.txt:1124`), NCBearDefs setzt es nicht; `goAttack` prueft blockMovement (731) | `BaseAnimalBehavior.txt:5021` Offset 314-432 |
| `followChr` | ja: blockMovement -> return (Offset 1-27) | `BaseAnimalBehavior.txt:4023` |
| `checkBehavior` (alle 500 Multiplikator, update Offset 82-131) | ja: blockMovement -> return vor Essen/Trinken (Offset 95-129); ruft immer `clearIdleAction` (nur `idleAction`) | `BaseAnimalBehavior.txt:1738` |
| `wanderIdle` (aus Idle-/WalkState.execute) | ja (Offset 1-53; zaehlt blockedFor, loest bei 8000 -> unser refreshBlock); auch return bei gesetztem Laerm-Merker | `BaseAnimalBehavior.txt:66` |
| `updateGoingToHutch` | ja (nur isDoingBehavior + ENTERHUTCH) | `BaseAnimalBehavior.txt:1113` |
| `updateLured` | ja (`luredBy` null -> return, Offset 0-7) | `IsoAnimal.txt:1621` |
| `checkZone` | kein Weg (nur DZone, `setWild(false)` in Zonen, Offset 0-92) | `IsoAnimal.txt:1483` |
| `separate` | kein Weg, nur Kollisionskontakte (`CollisionManager.AddContact`) | `B_IsoMovingObject.txt` separate |
| `AnimalPathFindState.execute` Failed | `pathFailed`, `shouldFollowWall=true`, `pathToLocation(getPathTarget...)` = ALTES Ziel (Offset 13-71). Ob die Nullweg-Anfrage aus N+1 (Start=Ziel) je Failed liefert: ungeprueft. | `B_AnimalPathFindState.txt:42` |
| State-exit -> `doBehaviorAction` | ja, ohne isDoingBehavior nur `timerFleeAgain=0` (Offset 0-191) | `BaseAnimalBehavior.txt:1173` |

---

## 5. Fix-Kandidaten fuer act (und calm)

| | Kandidat | Beleg-Status | Bewertung |
|---|---|---|---|
| (a) | Knoten zusaetzlich in `AnimSets/buck/pathfind` und `walk`, Baer festhalten | Laden belegt (resolveAllFiles) | **hilft nicht**: jeder Zustandswechsel startet einen neuen Knoten (Abschnitt 3), der Clip beginnt beim Hin- UND beim Rueckweg neu. Nur wenn der Baer die ganze Clipdauer in pathfind bliebe -- dann zieht PFB2 ihn mit der Wurzelbewegung unseres Clips den Fluchtweg entlang und dreht ihn weg (moveToPoint 118-279). Verworfen. |
| (b) | `bPathfind` ueberschreiben | `setVariable(String, boolean)` an einem Charakter: Vanilla `ISMilkAnimal.lua:139` (`self.character:setVariable("milkanimalout", false)`), gleiche Java-Methode `IsoGameCharacter.setVariable(String,Z)` | **als Aufraeumen ja, als Fix nein**: aus OnTick zu spaet fuer den Wechsel in N. Aber in fleeStop (wenn st == "pathfind") nach `stopAllMovementNow` `setVariable("bPathfind", false)` verhindert den Schein-PathFindState in N+1 (changeRootState-No-op, Abschnitt 1.5) -> Ausflug ein Bild kuerzer, kein Nullweg, kein moegliches Failed -> FollowWall -> altes Fluchtziel. |
| (c) | frueheres Ereignis | OnPlayerUpdate: Vanilla `Steps.lua:1919`, aber HashSet-Reihenfolge; OnAIStateChange: nur Jar | **nicht tragfaehig**: kein verlaesslicher Zeitpunkt (Abschnitt 1.6). OnAIStateChange deckt nur den walk-Fall und braucht Kevins Wort (Jar-Beleg). |
| (d) | Treffer/Ende per Lua-Uhr | reine Lua-Logik | Logik robust, aber Bild und Schaden laufen auseinander (Neustart sichtbar, Treffer kommt waehrend der Clip wieder ausholt). Nur als Rueckfall. |
| (e1) | **Neustart erkennen, Clip-Uhr neu** | Neustart bei 0 belegt (Abschnitt 3); `getActionStateName` (Bandits `ZASmack.lua:486`) | **empfohlen**: in act und calm jeden Wechsel nicht-idle -> idle mitzaehlen und dann `B.actT = 0` (bzw. `B.calmT = 0`) -- der Clip beginnt genau dann. `hitDone` bleibt (kein Doppeltreffer; NCBearHit wird ohnehin geloescht). Ereignisse des neuen Knotens liefern Treffer/Ende. Deckel: hoechstens 2 Neustarts je Angriff, dann wie heute abbrechen. Heute wird ein Ausflug in den ersten 0,5 s gar nicht bemerkt (`NCBearFight.lua:1176`). |
| (e2) | **Aufrichten bei Neustart abbrechen** | `NCBear_Rear.xml:15-17` (Bruellen bei 0,81 s) | empfohlen: bei Neustart von `rear` sofort `clearAct` + Anlauf -> kein zweites Bruellen (Knoten blendet in 0,25 s aus, bevor 0,81 s erreicht sind). |
| (e3) | **Anlauf: Weg neu, wenn die Engine ihn ueberschrieben hat** | `fleeTo` (`ISMilkAnimal.lua:38`); respondToSound schweigt, solange der Baer laeuft und t>0 (Offset 0-35, 91) | empfohlen: im Anlauf gibt es kein fleeStop; die Laermflucht ersetzt still unseren Weg, und `updateApproach` setzt nur neu, wenn `st == "idle"` oder das Ziel > 1 Kachel wanderte (`NCBearFight.lua:970`) -> "stuck on the way". Neu setzen, sobald der Abstand zum Ziel waehrend des Laufens waechst. Danach haelt unser Weg (Engine bewertet neuen Laerm nicht, solange er sich bewegt). Achtung: "stuck" bei 2,01 Kacheln kann auch echt sein (Maschendraht: Weg um den Zaun). |
| (e4) | eigener Aktionszustand / geaenderte Uebergaenge | ActionGroup liest nur den Spielordner (Abschnitt 3) | unmoeglich per Mod. |
| (e5) | Laerm-Seite: respondToSound gar nicht erst ausloesen | Forschung A | **der eigentliche Fix.** Von der Zustandsseite ist bewiesen, dass jeder ausgeloeste Laerm-Weg den Clip neu startet. |

Diagnose ohne Umbau: `NCBear_Tune("log", 2)` druckt jede fleeStop-Zeile ("stopped a move we did not order (pathfind)",
`NCBearFight.lua:885`); `NCBear_FightInfo()` zaehlt `flee stops`. Zusaetzlich sinnvoll (Lua-Fundstellen vorhanden): je Angriff die
Folge der Zustandsnamen mit Bildzaehler und `getStress()` (`ISMilkAnimal.lua:17`) loggen -> zeigt, wie oft und in welchem Abstand
der Laerm nachfeuert und ob der Stress Richtung 70 laeuft.

Calm (Sitzen, Hinsetzen, Aufstehen, Fressen): gleicher Ablauf, gleiche Folgen (`updateCalm` ruft fleeStop, `NCBearFight.lua:1096`);
Sitz-Schleife merkt man kaum, Hinsetzen/Aufstehen sichtbar doppelt.

MP: unveraendert aus (isSP-Riegel); alles oben ist SP-Zweig.
