# Forschung A: Laerm-Seite -- warum der Baer im Garten nicht zum Schlag kommt

Stand 08.11.2026, nur gelesen (Jar per javap, Vanilla-Lua, Bandits, Test-Mod NCBearTest NUR gelesen; das Spiel lief, nichts
in der Test-Mod geschrieben). Statisch geprueft, nicht gespielt.

Werkzeuge und Rohdaten dieses Laufs (alles in `_arbeit/baer_laerm/`):
- `tools/ziehen.py` (Klassen aus projectzomboid.jar nach `jar/` ziehen, `javap -c -p` nach `dump/<klasse>.txt`)
- `tools/aufrufer.py` -> `tools/aufrufer.txt` (jeder Aufruf `WorldSoundManager.addSound*` mit seinen Argumenten)
- `tools/wsm_nutzer.txt` (51 Klassen, die WorldSoundManager benutzen)
- Belege "Klasse.Methode Off. N" = Bytecode-Offset in `dump/<klasse>.txt`; "Datei:Zeile" = Lua.

---------------------------------------------------------------------------------------------------------------------------

## 0. Kurz

1. Ein Baer mit `wild=false` flieht vor jedem Weltgeraeusch mit `stresshumans` oder `stressAnimals`, das 4 bis R Kacheln
   entfernt ist (R = Radius). Die wichtigsten im Spiel: **Zombie-Schlaege (Thump) auf Zaun/Tuer/Fenster/Barrikade/gebaute
   Waende** (Radius 20, an Maschendraht zusaetzlich 40), **Spieler-Schuesse** (Vanilla), Spieler-Ruf (Q), Rauchen/Husten,
   Jukebox, Laermfallen, Fensterbruch, Start einer Autoalarmanlage. **Kein Stress** erzeugen: alles aus Lua `addSound`
   (also unser eigener Kampflaerm, Turret, NPC Crew, Bandits), Generatoren, Nahkampf, Schritte, Explosionen, Hubschrauber,
   Hausalarm, Donner; Fahrzeugmotor/Hupe/Dauer-Alarm werden von zahmen Tieren ignoriert.
2. Ein Geraeusch lebt **16 Bilder** (nicht Sekunden). Unser `fleeStop` (OnTick) und `respondToSound` spielen Ping-Pong:
   **jedes 2. Bild ein neuer Fluchtbefehl, bis zu 9 je Schlag**; die Animation steht die ganze Zeit (~17 Bilder) in
   `pathfind`, danach startet unser Idle-Knoten neu ("2x Schrei"). Lua kann den Wechsel nicht verhindern: OnTick kommt
   erst NACH dem Animations-Uebergang desselben Bildes.
3. Ohne Stoppen haelt das Schild (`t > 0 && isAnimalMoving()`), solange er laeuft; die Zeit selbst ist riesig
   (t = 2000 x Radius, Abbau ~48 je Sekunde bei Tempo 1 -> 14 min bei Radius 20).
4. Im Anlauf ist der saubere Weg belegt: fremde Flucht am wachsenden Abstand zum Ziel erkennen und sofort mit unserem
   `fleeTo` (ISMilkAnimal.lua:38) ueberschreiben -- das Schild bleibt stehen und schuetzt dann UNSEREN Weg.
5. Fuer die Angriffsphase gibt es auf der Laerm-Seite **keinen** belegten Lua-Hebel, der die Flucht verhindert. Was wirkt,
   ist Anim-Seite (Uebergang idle->pathfind sperren, solange `NCBearAct` gesetzt ist) -- Hinweis an Forschung B, ungeprueft.

---------------------------------------------------------------------------------------------------------------------------

## 1. Welche Weltgeraeusche erschrecken den Baeren?

### 1.1 Wie die Schalter gesetzt werden (Jar)

`WorldSoundManager.addSound` hat sieben Formen; alle muenden in
`addSound(Object, x, y, z, radius, volume, float zombieIgnoreDist, float stressMod, bool, bool, bool, bool repeating, short flags)`
(`dump/zombie.WorldSoundManager.txt` bzw. `_arbeit/baer_kampf/wsm.txt` Zeile 85-385). Die Schalter kommen aus
`WorldSound.init(..., short)` (`dump/zombie.WorldSoundManager$WorldSound.txt` init Off. 39-84):
Bit 2 = `stresshumans`, Bit 1 = `stressAnimals`, Bit 4 = `stressZombies`.

| Form (Argumente nach x,y,z,radius,volume) | stresshumans | stressAnimals | zombieIgnoreDist | Beleg |
|---|---|---|---|---|
| `()` 6 Argumente | false | false | 0 | wsm.txt 85-98 (-> Z=false, F 0, F 1) |
| `(Z)` | = Z | false | 0 | wsm.txt 100-113 |
| `(Z, F zid, F stressMod)` | = Z | false | = zid | wsm.txt 115-133 (-> 14er mit letztem Z=false) |
| `(Z, F, F, Z, Z, Z)` | = Z | false | = zid | wsm.txt 155-173 |
| `(Z, F, F, Z, Z, Z, Z, Z stressAnimals)` | = 1. Z | = letztes Z | = zid | wsm.txt 175-208 (Off. 0-25: Flags 4, +1, +2) |
| `addSoundRepeating(Z)` | = Z | false | 0 | wsm.txt 408-421 |
| `addSoundRepeating(Z, Z)` | = 1. Z | = 2. Z | 0 | wsm.txt 388-406 |

Lebensdauer: `WorldSound.init` Off. 6 setzt `life = 16`. `WorldSoundManager.update` (wsm.txt 1145-1229) laesst zuerst jeden
Chunk aufraeumen (`IsoChunk.updateSounds` Off. 37-62: weg, wenn `life <= 0`) und zieht dann `life` um 1 ab. Aufgerufen
genau einmal je Bild aus `IngameState.UpdateStuff` Off. 186, das je `IngameState.updateInternal` einmal laeuft (Off. 1283).
Ergebnis: ein Geraeusch steht **16 bis 17 Bilder** in der Chunk-Liste (bei 60 FPS ~0,28 s, bei 30 FPS ~0,55 s) --
**bildgebunden, nicht zeitgebunden**. `getSoundAnimal` prueft `life` gar nicht, nur die Liste (wsm.txt 503-614).

Im Einzelspieler liest das Tier die Liste SEINES Chunks (`getSoundAnimal` Off. 17-39: Chunk da und nicht Server ->
`chunk.soundList`); `addSound` traegt Stress-Geraeusche in alle Chunks im Umkreis Radius x 3 ein (Off. 95-260).

### 1.2 Wer ruft mit Stress auf? (vollstaendige Liste aller 78 Aufrufer: `tools/aufrufer.txt`)

| Quelle | Radius / Lautst. | Schalter | Quelle-Objekt | erschreckt zahmen Baeren? | Beleg |
|---|---|---|---|---|---|
| **Zombie schlaegt Zaun/Objekt** (`IsoObject.Thump`, auch Maschendraht = BentFences) | **20/20**, Maschendraht zusaetzlich **40/40**; Bruch 10/20; Verbiegen 40/40 | stresshumans | Zombie bzw. null | **ja** (ab 4 Kacheln, zid 4) | IsoObject.Thump Off. 104-141 (40), 363-399 (20), 410-446 (10), 495-531 (40); Vanilla `server/Items/BentFences.lua:5` "tall metal wire fence" fencing_01_56/57/60 |
| Zombie schlaegt Tuer | 20/20, Bruch 10/20 | stresshumans | Zombie / null | **ja** | IsoDoor.Thump (aufrufer.txt Zeile 3711, 3780) |
| Zombie schlaegt Fenster | 20/20, 10/20 | stresshumans | Zombie / null | **ja** | IsoWindow.Thump (1074, 1143) |
| Fenster zerspringt (`smashWindow`) | 10/20 | stresshumans | null | **ja** | IsoWindow.smashWindow (684) |
| Zombie schlaegt gebaute Wand/Zaun (`IsoThumpable`), Barrikade, Kompost | 20/20, Bruch 10/20 | stresshumans | Zombie / null | **ja** | IsoThumpable.Thump (2234, 2324, 2391), IsoBarricade.Thump (884), IsoCompost.Thump (718, 777) |
| Tier rennt gegen IsoThumpable (`animalHit`) | 10/20 | stresshumans | null | ja | IsoThumpable.animalHit (6920), Aufruf AnimalAttackState.animEvent Off. 94 (nicht unser Weg) |
| **Spieler schiesst (Vanilla)** | Waffen-`SoundRadius` x Sandbox `FirearmNoiseMultiplier`, drinnen x 0,5 | stresshumans | Spieler | **ja** (zid 0) | `shared/TimedActions/ISReloadWeaponAction.lua:450` `addWorldSoundUnlessInvisible(radius, vol, true)` -> IsoGameCharacter.addWorldSoundUnlessInvisible (aufrufer 32852) |
| Spieler ruft (Q, `Callout`) | 30 (Megafon 90), schleichend 6 (18) | **stressAnimals** | Spieler | ja; Ausnahme: `callOut` und Akzeptanz >= 40 -> er kommt zum Spieler | IsoGameCharacter.Callout Off. 29-40, 97-114, Aufruf 11937 |
| Spieler hustet beim Rauchen (`triggerCough`) | 35/40 | stresshumans | Spieler | ja | IsoGameCharacter.triggerCough (41416); RecipeCodeOnEat.consumeNicotineLogic Off. 166 |
| Jukebox | 70/70 | stresshumans | IsoPlayer.getInstance() | ja | IsoJukebox.update (323) |
| Laermfalle (Wecker-/Laermfalle, wiederholt) | NoiseRange/1 | stresshumans | null | ja | IsoTrap.updateSounds (861) |
| Autoalarm **Start** | 150/150 | stressAnimals | `VehicleAlarm` selbst (kein VehiclePartOwner) | **ja** | VehicleAlarm.onAlarmStart Off. 27-72; `WorldSound.sourceIsVehicle` = `source instanceof VehiclePartOwner` |
| Autoalarm Dauer, Motor, Hupe, Fahrzeug-Update | 8..150 | stressAnimals / stresshumans | Fahrzeug (VehiclePartOwner) | **nein** (zahm + Fahrzeug -> return) | VehicleAlarm.updateWorldSounds, VehicleEngine.updateWorldSounds, BaseVehicle.onHornStart/update; respondToSound Off. 140-154 |
| Fahrzeugscheibe bricht | 10/20 | stresshumans | null | ja | VehicleWindow.damage (255) |
| Radio/TV laut (> 50) | Geraete-Werte | stresshumans | Geraet | nein, wenn Quelle IsoRadio/IsoTelevision; tragbare Geraete ungeprueft | DeviceData (2358, 2625); respondToSound Off. 119-139 |

**Ohne Stress (erschrecken nie):** Lua `addSound(obj,x,y,z,r,v)` (`LuaManager$GlobalObject.addSound` -> 6er-Form, aufrufer
16141) und `AddWorldSound(player,r,v)` (Z=false, 1915) -- damit alle Vanilla-Lua-Arbeitsgeraeusche, **unser
`NCBearFight.lua:871`**, **Turret `BanditsNPCTurretClient.lua:313`**, NPC Crew (kein addSound im Code, nur Kommentare
"kein WorldSoundManager"), **Bandits** (kein addSound, nur auskommentiert `ZASmack.lua:466`); **Generator**
(IsoGenerator.update 360 und 549: Z=false); Spielerschritte (DoFootstepSound 13596: false); Nahkampf-Schwung und -Treffer
(IsoLivingCharacter.DoAttack 380: 6er; CombatManager.attackCollisionCheck Off. 2958-3049: false); Explosion
(IsoTrap.triggerExplosion 1177/1193: 6er); Feuer, Hubschrauber, Hausalarm (`iso.Alarm`), Donner, Ambient-Schuesse, Ball,
Wecker, Waschmaschine/Trockner, Niesen.

Hinweis Schuesse in einer NPC-Crew-Basis: nur der **Spieler** mit Vanilla-Feuerwaffe erzeugt Stress-Laerm; Bandits-/Crew-
Schuesse und Turrets nicht (siehe oben). Der Dauerlaerm einer Basis ist also vor allem **Zombies an Waenden/Zaeunen/Tueren**.

### 1.3 Wann ein Geraeusch wirklich zieht (Reichweite)

- Nur das **lauteste** Geraeusch der Chunk-Liste wird bewertet: `volume x (1 - d^2/R^2)`, R = Radius x (wild ? 3 : 1)
  (getSoundAnimal Off. 73-207). Zahm: R = Radius.
- `getSoundAttractAnimal` gibt 0, wenn d < `zombieIgnoreDist` und gleiche Etage (wsm.txt 939-1072, Off. 88-116): fuer
  Thump ist zid = 4. **Liegt der lauteste Thump naeher als 4 Kacheln, gibt es in diesem Bild keine Flucht** (auch keine vor
  leiseren). Andere Raeume daempfen (x1,2 bzw. x1,4 auf d^2/R^2, Off. 175-228).
- Flucht-Ziel (zahm): auf der Linie Laerm->Baer, (Radius + 10) Kacheln vom Laerm (respondToSound Off. 238-382). Bei Thump 20:
  Baer zwischen 4 und 20 Kacheln -> rennt 10 bis 26 Kacheln; bei 40: 4..40 -> 10..46 Kacheln. Dazu `animalRunning=true`,
  `changeStress(Radius x 0,05)` je Befehl (Off. 341-362).

### 1.4 Was zu Kevins Szene passt (Garten, Maschendraht, Zombies, Spieler 4 Kacheln weg)

- **Passt am besten:** Zombies vor dem Zaun bzw. am Haus (Tuer/Fenster) schlagen -> je Schlag (ThumpState.execute
  Off. 111-165: `Thump` je Schlag-Ereignis der Animation) ein Radius-20-Geraeusch, an hohem Maschendraht zusaetzlich 40.
  Der Baer im Garten ist fast immer 4..20 Kacheln davon weg. Viele Zombies = mehrere Schlaege je Sekunde.
- **Moeglich, ungeprueft:** Kevin schoss mit einer Vanilla-Feuerwaffe oder rief (Q).
- **Passt nicht:** Kevins Schritte, sein Nahkampf, unser eigener Laerm (T.noise = 0, und selbst dann ohne Stress).
- Gegenprobe im selben console.txt: nach `f:122824` (Spawn von ~20 Zombies direkt beim Baeren, keine Wand dazwischen) laufen
  die Angriffe durch (`swipeR: 2 hit` ...). Freies Gelaende 02:09 ebenso. Das stuetzt "Thump an Hindernissen", beweist es
  aber nicht (Zombies klettern auch: Zeile "state climbfence" bei f:116257; Klettern erzeugt kein Weltgeraeusch,
  ClimbOverFenceState ist kein WorldSoundManager-Nutzer).

---------------------------------------------------------------------------------------------------------------------------

## 2. respondToSound exakt nachgerechnet

### 2.1 Der Ablauf (IsoAnimal.respondToSound, `dump/zombie.characters.animals.IsoAnimal.txt` Zeile 1934)

```
Off.  0- 91  wenn lastSoundRespondedTo != null:
               t -= GameTime.getMultiplier()
               wenn t > 0 UND isAnimalMoving()  -> return            (das SCHILD)
               sonst setMoving(false); lastSound = release(lastSound) = null   (und weiter, gleiches Bild)
Off. 92-108  s = getSoundAnimal(this); a = getSoundAttractAnimal(s, this)
Off.109-139  s == null oder a <= 0 oder Quelle IsoRadio/IsoTelevision -> return
Off.140-154  nicht wild UND Quelle ist Fahrzeug -> return
Off.155-210  Quelle Spieler mit callOut UND Akzeptanz >= 40 -> pathToLocation(Spieler); return
Off.211-385  FLUCHT: lastSound = Kopie(s); t = 2000 x Radius; animalRunning = true; changeStress; pathToLocation(weg)
```
Es gibt **keine** Pruefung "dieses Geraeusch hatte ich schon" -- dasselbe Geraeusch kann beliebig oft neu wirken.
`respondToSound` liest **kein** Feld aus AnimalDefinitions (kein `adef`-Zugriff im Bytecode): `canBeAlerted`, `fleeZombies`
usw. wirken hier nicht. `blockMovement` wird nur in wanderIdle/goAttack/checkBehavior/followChr/canDoAction/
isPushedByForSeparate gelesen (Grep ueber `dump/`), nie hier.

`isAnimalMoving()` = KI-Zustand AnimalWalkState, AnimalPathFindState oder AnimalFollowWallState (Zeile 6065).

### 2.2 Reihenfolge in EINEM Bild (alles Jar)

1. `IngameState.updateInternal` Off. 1067 `IsoWorld.update` -> Zellen -> `MovingObjectUpdateSchedulerUpdateBucket.update(int)`
   (Zeile 128/132: je Objekt preupdate + update; Zombies schlagen hier, Baer-Update hier).
   - `IsoAnimal.update` (Zeile 921): Off. 29-61 **wenn `bPathfind` gesetzt und KI nicht PathFind -> changeState(PathFind)**;
     Off. 88 `updateInternal` -> Off. 145 `respondToSound` -> ggf. `pathToLocation` -> `pathToAux`
     (`_arbeit/baer_angriff/IsoGameCharacter.txt` Zeile 15618, Off. 224-271): Weg frei -> `bPathfind=false` + `setMoving(true)`;
     sonst **`bPathfind=true`** + `setMoving(false)`.
2. Danach `MovingObjectUpdateSchedulerUpdateBucket.postupdate(int)` (Zeile 184) -> `IsoGameCharacter.postUpdateAnimating`
   Off. 65 `ActionContext.update` -> **Uebergang idle -> pathfind** (`actiongroups/buck/idle/to_pathfind.xml`: isTrue bPathfind).
3. Off. 1283 `UpdateStuff` -> `WorldSoundManager.update` (life - 1).
4. Off. 1331 `onTick` -> **unser OnTick** (`NCBearFight.lua:1361`).

Ein Lua-Ereignis zwischen 1. und 2. fuer den Baeren gibt es nicht: Tiere nehmen in `IsoPlayer.updateInternal1`
(Zeile 5980, Off. 0-49) den kurzen Zweig, `updateInternal2` mit `OnPlayerUpdate` (Zeile 6588, Off. 1141) laeuft fuer sie nie.
(OnPlayerUpdate/OnZombieUpdate ANDERER Objekte koennen zwischen Baer-Update und Baer-Postupdate fallen, aber nur je nach
Reihenfolge im Eimer -- nicht verlaesslich, nicht empfohlen.)

### 2.3 Mit unserem fleeStop (OnTick, nur wenn Zustand walk/pathfind) -- ein einziger Schlag

`stopAllMovementNow` (Zeile 1574) = setMoving(false), PFB2.reset, setPath2(null), changeState(Standard, restart=false).
`StateMachine.changeRootState` Off. 0-20: gleicher Zustand und restart=false -> **nichts** (kein exit). `bPathfind` loescht nur
`AnimalPathFindState.exit` (dump AnimalPathFindState exit).

| Bild | Baer-Update | Postupdate (Animation) | OnTick (wir) |
|---|---|---|---|
| k | kein lastSound -> Schlag gefunden -> FLUCHT 1, bPathfind=true | idle -> **pathfind** (Clip weg) | Zustand "pathfind" -> stopAllMovementNow; KI noch Idle -> bPathfind bleibt true |
| k+1 | bPathfind -> KI PathFind; respondToSound: t>0 und moving -> return | pathfind | stopAllMovementNow -> PathFind.exit -> bPathfind=false |
| k+2 | nicht moving -> release -> Schlag noch in der Liste -> FLUCHT 2, bPathfind=true | bleibt pathfind | wie k |
| ... | jedes 2. Bild eine neue Flucht | bleibt pathfind | |
| k+16 | letztes Bild, in dem der Schlag in der Liste steht -> FLUCHT 9 | pathfind | |
| k+18 | release, nichts mehr in der Liste | bPathfind=false -> **idle: NCBear-Knoten startet NEU** | |

Also **bis zu 9 Fluchtbefehle je Schlag** (jeder ein Pfad-Auftrag und +Radius x 0,05 Stress, bei 20 also +1, Deckel 100,
`changeStress` Zeile 7148), die Animation haengt ~17 Bilder in pathfind und springt dann nach idle zurueck
(`AnimLayer.findLiveNode`, Aufgabe: neuer Knoten = Clip von vorn = Kevins "2x Schrei"). Folgt der naechste Schlag innerhalb
der Angriffsdauer (Treffer bei 0,52-1,3 s, `NCBearFight.lua:36-41`), faellt der Treffer aus -> "did not finish ... (pathfind)".
Unser Zaehler `F.stats.fleeStops` muesste nach so einem Kampf sehr hoch sein (`NCBear_FightInfo()` zeigt ihn) -- billige
Gegenprobe fuer Kevins naechsten Test.

`a:setVariable("bPathfind", false)` zusaetzlich im fleeStop (Vanilla-Fundstelle `client/DebugUIs/DebugContextMenu.lua:642`,
gleiche Typen) macht es NICHT besser: dann flieht er jedes Bild neu (1-Bild-Takt), die Animation bleibt trotzdem in pathfind,
weil der Uebergang in Schritt 2 VOR unserem OnTick passiert.

### 2.4 Wenn wir ihn NICHT stoppen -- wie lange haelt das Schild?

- t = 2000 x Radius (Off. 225-235). Abbau je Tier-Update um `GameTime.getMultiplier()` = Tempo x fpsMultiplier x Bias x
  perObject x Slomo x 0,8 (GameTime Zeile 2422, Off. 103-141); fpsMultiplier = 60/FPS (FPSTracking Off. 109-139), Bias aus
  der Sandbox-Option Tempo 0,8..1,2 (SandboxOptions Off. 112-137). Je echter Sekunde also ~48 x Tempo x Bias.
- Radius 20: 40.000 / 48 = **~833 s (14 min)**; Radius 40: ~28 min; Ruf 30: ~21 min (Tempo 1, Bias 1).
- Praktisch endet das Schild also **nur, wenn er nicht mehr laeuft**: Ziel erreicht, oder wir stoppen ihn, oder irgendwas
  setzt ihn nach idle. Im selben Bild danach wird neu bewertet (Off. 38-92 laufen in den Suchteil durch).
- Die Fluchtstrecke (10..46 Kacheln) ist im eingezaeunten Garten oft unerreichbar; was der Pfadfinder dann macht
  (AnimalPathFindState.execute Off. 17-71: `pathFailed`, `setShouldFollowWall`, neuer Auftrag zum alten Ziel), ist
  "laeuft weiter" (FollowWall zaehlt auch als moving) -- genaues Verhalten ungeprueft.

---------------------------------------------------------------------------------------------------------------------------

## 3. Hebel -- jeder mit Jar-Beleg und Lua-Status

| # | Hebel | Jar-Beleg | Lua/Bandits-Fundstelle (gleiche Typen)? | Wirkung / Nebenwirkung | Urteil |
|---|---|---|---|---|---|
| 1 | **Schild nutzen**: waehrend er laeuft (Walk/PathFind/FollowWall) und lastSound gesetzt ist, wird nichts neu bewertet | respondToSound Off. 0-35 | `fleeTo(sq)` ISMilkAnimal.lua:38 (schon benutzt) | Haelt im Anlauf/Rueckweg; im Angriff (idle) nicht | **nutzen (Abschnitt 4)** |
| 2 | Lauteste Quelle < 4 Kacheln (zid) -> keine Flucht | wsm getSoundAttractAnimal Off. 88-116 | -- (nicht steuerbar) | erklaert, warum es direkt am Zaun manchmal klappt | nur Wissen |
| 3 | `wild=false` | getSoundAnimal Off. 130-154, respondToSound Off. 140-154, 274-307 | `setWild(false)` ISPickupAnimal.lua:52 | Radius x1 statt x3, Fahrzeuge ignoriert, kuerzere Flucht | **schon richtig** (NCBearDefs.lua:86) |
| 4 | Leine (`attachedPlayer`): pathToLocation bricht ab, wenn Ziel > 15 Kacheln vom Spieler | pathToLocation Off. 4-49 | `getData():setAttachedPlayer(chr)` ISAttachAnimalToPlayer.lua:47 | Spielsystem (Seil, getAttachedAnimals, Folgen); haelt nur Ziele > 15 Kacheln vom Spieler ab; **unser `fleeTo` loest die Leine selbst** (fleeTo Off. 0-32) | nein |
| 5 | Baum-Anbindung (`attachedTree`): Abbruch, wenn Ziel > 15 Kacheln vom Baum | pathToLocation Off. 50-114 | `setAttachedTree(self.tree)` ISAttachAnimalToTree.lua:47 | Spielsystem, `reattachToTree` je Update; `fleeTo` loest auch das (Off. 35-40) | nein |
| 6 | Schlachthaken (`isOnHook`) | IsoAnimal.update Off. 0-28 (ganzes Update aus) | `setOnHook(true)` ButcheringUtil.lua:578 | Tier tot gestellt | nein |
| 7 | `fromMeta` | updateInternal Off. 0-7 (ganzes Update aus) | nur oeffentliches Feld, kein Setter, keine Fundstelle | Baer erstarrt | nein |
| 8 | Spieler-Ruf mit Akzeptanz >= 40 | respondToSound Off. 155-210 | `getPlayerAcceptance` ISAnimalUI.lua:323 (nur lesen) | nur fuer Spieler-Laerm mit callOut; zieht ihn zum Spieler | hilft nicht gegen Zombies |
| 9 | Quelle Radio/TV | Off. 119-139 | -- | nicht steuerbar | nein |
| 10 | Eigener Lua-Laerm | GlobalObject.addSound -> 6er-Form, Flags nur 4 | `addSound` AdminContextMenu.lua:260 | erschreckt den Baeren NIE, lockt nur Zombies | harmlos, kein Hebel |
| 11 | Ereignis `OnWorldSound(x,y,z,radius,volume,source)` | WorldSound.init Off. 129-155; registriert LuaEventManager Off. 889 | **keine** Vanilla-/Bandits-Fundstelle | nur erkennen (keine Stress-Schalter im Ereignis, nicht abbrechbar); gut fuer Diagnose | **braucht Kevins Wort (Jar-Beleg)** |
| 12 | `getLastSoundRespondedTo()` | Zeile 1928 | keine Fundstelle | nur erkennen | braucht Kevins Wort |
| 13 | Pfadziel lesen (`getPathTargetX/Y`, `getPathFindBehavior2():getTargetX`) | AnimalPathFindState.execute Off. 21-33, 83-93 | keine Fundstelle (nur `getPathFindBehavior2():pathToLocation/update/cancel`, WalkToTimedAction.lua:18/42/49; Bandits ZAMove.lua:70-73) | fremde Flucht exakt erkennen | braucht Kevins Wort; Ersatz in Abschnitt 4 |
| 14 | `getVariableBoolean("bPathfind")` | pathToAux Off. 224-271 | Bandits ZAMove.lua:60 | erkennt frischen Fluchtbefehl (auch unseren), Zeitpunkt wie getActionStateName | belegt, nur erkennen |
| 15 | `setVariable("bPathfind", false)` | AnimalPathFindState / IsoAnimal.update Off. 29-61 | DebugContextMenu.lua:642 | zu spaet (2.2), verdoppelt die Fluchtbefehle | nein |
| 16 | `setBlockMovement(true)` | BaseAnimalBehavior.setBlockMovement Zeile 5764 (= stopAllMovementNow) | ISPetAnimal.lua:36 | schuetzt NICHT vor respondToSound | kein Laerm-Hebel |
| 17 | Hutch, Anhaenger, Sitzen | updateGoingToHutch / Anhaenger nicht untersucht; `isAnimalSitting` nur in canDoAction (Zeile 7065) | -- | Spielsysteme bzw. ohne Wirkung auf respondToSound | nein / ungeprueft |
| 18 | **Anim-Seite**: Uebergang idle->pathfind (und idle->walk, defaultTransitions) sperren, solange `NCBearAct` gesetzt | `to_pathfind.xml`, `to_walk.xml`, `defaultTransitions.xml` (buck); Bewegung im Pfad kommt aus der Animation: PFB2.update `getDeferredMovement` -> `moveUnmodded` (dump PathFindBehavior2 Zeile 3110/3118, 3567/3715), moveToPoint Zeile 3893/3952 | Mod-Datei gleichen Pfads; fuer Hirsche ohne Wirkung, solange die Variable nur am Baeren steht | KI darf PathFind sein (= moving = **Schild an**), Anim bleibt im Angriffsknoten, ohne Lauf-Clip kaum Bewegung | **Hinweis an Forschung B, ungeprueft** (Naht: Vanilla-Datei ueberlagert) |

---------------------------------------------------------------------------------------------------------------------------

## 4. Anlauf: fremden Fluchtweg erkennen und durch unseren fleeTo ersetzen

Belegt, nur Lua mit Fundstellen:

- **Warum es heute haengt:** `updateApproach` (`NCBearFight.lua:968-977`) schickt `fleeTo` nur neu, wenn Zustand idle
  oder Ziel > 1 Kachel gewandert. Kapert die Engine den Weg (Zustand bleibt pathfind), schickt niemand neu -> nach
  `stuckTime` 3 s kein Fortschritt -> "stuck on the way" (auch bei Ziel 2,01 Kacheln).
- **Wann die Engine kapert:** nur wenn `lastSound == null` oder t <= 0 (Off. 0-91). Das ist nach jedem Halt der Fall
  (der naechste Aufruf gibt lastSound frei, Off. 38-88). Also: der ERSTE Stress-Laerm nach einem Halt kapert den Anlauf
  einmal; danach gilt das Schild.
- **Ersetzen haelt:** `fleeTo` (Zeile 7629) setzt nur animalRunning und ruft `pathToLocation`; es fasst `lastSoundRespondedTo`
  und t NICHT an. Nach dem Kapern ist lastSound gesetzt und t = 2000 x Radius; laeuft er auf unserem neuen Weg weiter,
  bleibt `isAnimalMoving()` wahr -> respondToSound kehrt jedes Bild an Off. 35 zurueck. **Unser Weg haelt, bis er ankommt.**
- **Erkennen ohne Jar-Methode:** im Anlauf je ~0,25 s den Abstand zum Ziel (`distTo`, eigene Rechnung) merken; ist Zustand
  walk/pathfind (`getActionStateName`, Bandits ZASmack.lua:486) und der Abstand seit der letzten Messung um mehr als ~0,5
  Kachel GEWACHSEN, ist es ein fremder Weg -> sofort `fleeTo(Ziel-Feld)` (ISMilkAnimal.lua:38), `B.issueT` und die
  Stuck-Uhr (`chkT/chkD`) neu setzen, damit das Kapern nicht als "stuck" zaehlt. Genauer waere das Pfadziel lesen
  (Hebel 13) -- braucht Kevins Wort.
- **Grenze:** Beim Ankommen stoppt `beginAct` ihn (setBlock -> stopAllMovementNow) -> Schild aus -> im naechsten Bild
  bewertet er neu. Der Anlauf wird also sicher; der Angriff selbst bleibt angreifbar (Abschnitt 2.3).
- Nebenbei ungeprueft: ob `fleeTo` mitten in AnimalPathFindState sauber umplant (Weg frei -> pathToAux setzt bPathfind=false,
  KI bleibt PathFind). Der heutige Code tut das schon bei "Ziel > 1 Kachel gewandert", ohne bekannte Fehler.

---------------------------------------------------------------------------------------------------------------------------

## 5. Empfehlung

1. **Erst messen (billig, belegt):** in `fleeStop` bei jedem fremden Stopp eine Zeile hinter dem Log-Schalter: Zahl der Zombies
   im Umkreis 4..40 mit `getActionStateName() == "thump"` (Zustand `actiongroups/zombie/thump`, Methode Bandits ZASmack.lua:486)
   und `F.stats.fleeStops`. Kevin: nach dem Gartenkampf `NCBear_FightInfo()`. Sehr viele flee stops + Thump-Zombies = bestaetigt.
2. **Anlauf reparieren (belegt, Abschnitt 4):** fremden Weg am wachsenden Abstand erkennen, sofort `fleeTo` zum Ziel, Stuck-Uhr
   neu. Das behebt "stuck on the way" bei Laerm und wird in jeder Basis gebraucht.
3. **Ping-Pong beenden (belegt):** in act/pause/seek nicht mehr jedes zweite Bild gegen die Engine stoppen. Stattdessen bei der
   ersten fremden Bewegung den Angriff EINMAL abbrechen und in den Anlauf wechseln (`fleeTo` Ziel) -- dann schuetzt das Schild
   den Weg, statt 9 Fluchtbefehle und Stress je Schlag zu erzeugen. Der Angriff selbst bleibt bei Dauerlaerm stoerbar.
4. **Echte Loesung fuer den Angriff liegt auf der Anim-Seite (Forschung B):** Hebel 18 pruefen (Uebergaenge idle->pathfind/walk
   sperren, solange `NCBearAct` gesetzt; dann `fleeStop` im Angriff weglassen, damit die KI im PathFind bleibt = Schild an).
   Vorher klaeren: Bewegt ihn PathFind ohne Lauf-Clip wirklich nicht (deferred movement des Angriffs-Clips), und was macht
   `pathFailed`/FollowWall dabei.
5. Fuer die Basen: Turrets, Generatoren, Crew-/Bandits-Schuesse sind laut Jar harmlos; gefaehrlich sind Zombies an Waenden,
   Tueren, Fenstern, Zaeunen, Spieler-Schuesse, Rufe, Jukebox, Laermfallen, Alarmstart. Der Fix muss also "Dauer-Thump" aushalten.
6. Jar-only (nur auf Kevins Wort): `OnWorldSound` als Diagnose (welcher Laerm, wo, wer) und Pfadziel-Getter zur exakten Erkennung.

## 6. Offen / ungeprueft

- Welche Quelle in Kevins Garten wirklich feuerte (Thump vs. Schuss/Ruf) -- nur per Messung (5.1).
- Verhalten des Pfadfinders bei unerreichbarem Fluchtziel im eingezaeunten Garten (pathFailed, FollowWall).
- Tragbare Radios als Quelle; Anhaenger/Hutch; genaue Zahl der Schlag-Ereignisse je Thump-Clip (ThumpAnimations).
- Ob ein Mod Uebergangsdateien von `actiongroups/buck` ueberlagern oder ergaenzen kann (Hebel 18) -- Sache von Forschung B.
