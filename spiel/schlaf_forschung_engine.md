# Forschung Engine: Schlafen in der Engine und im AnimSet (Lauf baer-schlaf, 09.11.2026)

Nur gelesen, nichts gebaut, nichts in einer Mod geaendert, nichts heruntergeladen, keine Renders. **Statisch geprueft, nicht
gespielt.** PZ 42.21 (projectzomboid.jar vom 28.09.), Bandits 42.21, Test-Mod NCBearTest (nur gelesen).

Rohdaten dieses Laufs: `_arbeit/baer_schlaf/engine/jar/` (aus dem Jar gezogene Klassen), `_arbeit/baer_schlaf/engine/dump/`
(`javap -c -p`, eine Datei je Klasse), `engine/jar_animal_list.txt` (alle Tier-Klassen des Jars).
Zitierweise: "Klasse.Methode Off. N" = Bytecode-Offset im Dump; "Datei:Zeile" = Lua/XML.

---

## 0. Kurz

1. **Kein IsoAnimal schlaeft in B42.21.** `IsoAnimal.initializeStates` (Off. 0-124) meldet zwoelf KI-Zustaende an (idle, eating,
   attack, walk, pathfind, followwall, hitreaction, falldown, onground, zone, alerted, climbfence) -- keinen Schlaf. "Schlaf" gibt es
   nur (a) fuer **VirtualAnimal** (Wandergruppen auf der Weltkarte, ohne Koerper, ohne Animation) und (b) als **AnimalZoneState.StateSleep**
   (1-3 Spielminuten Pause wilder Zonentiere, ohne Animationsvariable, nur ueber die Aktionsgruppe `cow` erreichbar). Keine
   Sandbox-Option.
2. **Was einem Schlaf am naechsten kommt, ist das Ruhen "sit":** `idleAction = "sit"` -> Knoten `idleSit`. Beim Reh ist das das
   **Hinlegen** (`DeerStag_IdleToSitting` -> `DeerStag_SittingIdle` -> `DeerStag_SittingToStanding`), beim Waschbaer heisst es offen
   `Rac_IdleToLieDown`/`Rac_IdleLyingDown`/`Rac_LyingDownToIdle`. Die Engine setzt es von selbst nur bei `sitRandomly = true`
   (alle 3-7 Spielstunden fuer 1-2 Stunden, nicht nachts gebunden). Unser Baer hat `sitRandomly = false` (NCBearDefs.lua:93).
3. **Unser Baer schlaeft heute nicht heimlich.** Kein Pfad der Engine setzt bei ihm `idleAction = "sit"`; das GLB hat die drei
   Liege-Clips auch gar nicht (Clip-Liste aus NCBear.glb in 2.4, Begruendung in 3.4).
4. **MP-Schluesselfund:** `idleAction` reist mit jedem Tierpaket vom Server zu allen Clients (NetworkPlayerAI.set Off. 224-253,
   NetworkPlayerAI.parse Off. 709-737, alle 800/1000 ms). Unsere eigene Variable `NCBearAct` (Sitzen, Fressen, Kampf) reist **nicht**
   mit. NPC Crew hat denselben Befund schon selbst nachgelesen (BanditsNPCLivestockAnimalOps.lua:1093-1099).
5. **Empfehlung (Weg A):** Schlafen ueber den Ruheplatz der Engine: Lua setzt `idleAction = "sit"` (Form belegt ISPetAnimal.lua:43)
   und loescht es zum Aufwachen (ISPetAnimal.lua:48). Das GLB liefert **drei Clips mit festen Vanilla-Namen**:
   `DeerStag_IdleToSitting` (Hinlegen), `DeerStag_SittingIdle` (Schlafen, Schleife), `DeerStag_SittingToStanding` (Aufwachen).
   Keine neue AnimSet-XML. Dazu umsonst: Bild im MP, halber Hunger/Durst im Schlaf, kein Herumwandern, `isAnimalSitting()` als
   belegte Frage fuer die z Z z-Anzeige. Wann er schlaeft und wann er aufwacht (Nacht, Zombie, Laerm, Treffer) entscheidet unser Lua.

---

## 1. Kennt B42.21 schlafende Tiere?

### 1.1 IsoAnimal: kein Schlafzustand

- `IsoAnimal.initializeStates` Off. 0-124 (`dump/zombie.characters.animals.IsoAnimal.txt:2252` ff.): `registerAIState` fuer idle,
  eating, attack, walk, pathfind, followwall, hitreaction, falldown, onground, zone, alerted, climbfence. Kein "sleep".
- Byte-Suche im ganzen Jar: `isSleeping` steht **nur** in `VirtualAnimal.class`; im Dump von IsoAnimal kommt "sleep"/"wake"
  (gross/klein) gar nicht vor (`grep -i` ueber `dump/zombie.characters.animals.IsoAnimal.txt`: 0 Treffer). AnimalData ebenso 0.
- Tageszeit liest ein IsoAnimal nur fuer Wachstum (`IsoAnimal` `getHour` bei `AnimalData.lastHourCheck`, Dump :5164/:5242) und
  fuer die Stallzeit (1.5). Kein "nachts schlafen".
- Aktionsgruppen (`media/actiongroups/*`): `grep -ril sleep` = 0 Treffer. Der Zustand `onground` (`actiongroups/buck/defaultTransitions.xml`)
  ist nur fuer Tote (`bDead` und `bOnFloor`).

### 1.2 VirtualAnimal (Wandergruppen auf der Karte)

- Felder `timeToSleep`, `sleepPeriodStart`, `sleepPeriodEnd`, `debugForceSleep`, Methoden `isSleeping()` (= Zustand ist
  `VirtualAnimalState$StateSleep`), `isTimeToSleep()`, `getNextSleepPeriod()` (`dump/zombie.characters.animals.VirtualAnimal.txt:31-57, 495-790`).
- Werte aus `media/lua/shared/Definitions/animal/MigrationGroupDefinitions.lua`: Reh `minTimeBeforeSleep 1500`, `maxTimeBeforeSleep 1900`,
  `timeToSleep 60` Minuten (:12-21), Schlafzeiten nach Uhr nur beim Debug-Trupp "predator" (Hasen, 12-16 Uhr, :88-90, "TODO RJ: remove").
- `VirtualAnimalState$StateSleep` legt nur Spuren ("sleep": `flattenedherb`, `fur`, AnimalTracksDefinitions.lua:38/:45) und setzt
  `wakeTime`; ein VirtualAnimal ist kein Koerper in der Welt. Werden daraus echte Tiere, erben sie keinen Schlaf: `idleAction`
  steht im Jar nur in 7 Klassen (AnimalEatState, AnimalIdleState, NetworkPlayerAI, IsoAnimal, BaseAnimalBehavior, AnimalData,
  AnimalPacket), kein VirtualAnimal/AnimalCell darunter (Byte-Suche).
- Lua sieht das nur im Debug der Weltkarte: `virtualAnimal:isSleeping()` / `forceWakeUp()` (ISWorldMap.lua:968-969).

### 1.3 AnimalZoneState.StateSleep (wilde Tiere auf Zonen)

- `AnimalZoneState$StateFollow.update` Off. 46-101: alle 2-5 Spielminuten (`Rand.Next(2,5)/60` h) -> `StateSleep`.
- `AnimalZoneState$StateSleep.<init>` Off. 5-23: `wakeTime = WorldAgeHours + Rand.Next(1,3)/60`; `update` Off. 0-37: danach zurueck
  nach Follow. **Setzt keine Animationsvariable** -- es ist eine Pause.
- Erreichbar nur ueber den Aktionszustand `zone` (`actiongroups/cow/idle/to_zone.xml`, Bedingung `hasAnimalZone`); dessen Knoten spielt
  stehendes Idle (`AnimSets/cow/zone/zone1.xml:4` `Cow_Idle01`). **Die Gruppe `buck` hat keinen Zustand `zone`** (Ordnerliste
  `actiongroups/buck`, kein `zone`), unser Baer kommt also nie hinein.

### 1.4 Ruhen "sit" (das Liegen der Hoftiere und Rehe)

- Wer es setzt: `BaseAnimalBehavior.checkSit` (Dump :792-936), aufgerufen aus `wanderIdle` Off. 296-310 nur bei
  `adef.sitRandomly`. Ablauf:
  - Off. 181-243: erstes Mal `sitInTime = jetzt + Rand.Next(10800, 25200)` s (3-7 Spielstunden), `sitOutTime = sitInTime +
    Rand.Next(3600, 7200)` s (1-2 Stunden).
  - Off. 246-290: ab `sitInTime` -> `setVariable("idleAction", "sit")`.
  - Off. 293-336: ab `sitOutTime` -> `clearVariable("idleAction")`.
  - Aufstehen vorher (Off. 0-49, 63-111): Hunger > 0,2, an der Leine (`getAttachedPlayer`), Regen > 0,05 ohne Dach.
  - Gar nicht erst hinsetzen (Off. 114-180): Hunger > 0,3, an der Leine, Regen ohne Dach.
- Wer `sitRandomly = true` hat: Kuh, Stier, Reh (fawn/doe/buck, DeerDefinitions.lua:77/:121/:165), Schwein, Schaf, Waschbaer,
  Hase (ohne Junges), Huhn, Truthahn (Fundstellen per `grep -rn sitRandomly media/lua`: ChickenDefinitions.lua:94/:156/:209,
  CowDefinitions.lua:196/:260, PigDefinitions.lua:105/:171/:234, RabbitDefinitions.lua:184/:233, RaccoonDefinitions.lua:100,
  SheepDefinitions.lua:160/:227/:294, TurkeyDefinitions.lua:75/:142).
- Was "sit" sonst bewirkt (alles nur, solange `idleAction == "sit"`, Test `IsoAnimal.isAnimalSitting` Off. 0-13):
  - **Halber Hunger und Durst:** `AnimalData.updateHungerAndThirst` Off. 11-36 (Faktor 0,5 im Stall oder sitzend).
  - **Kein Herumwandern:** `wanderIdle` Off. 313-398 (sitzend nur eine Geste `sittingAnim`, dann `return`).
  - **Kein Trinken/Fressen am Trog von selbst:** `checkBehavior` Off. 114-129 (`return`, solange `idleAction` nicht leer).
  - **Kein Tierkampf:** `IsoAnimal.canDoAction` Off. 7-11, gerufen aus `BaseAnimalBehavior.checkAttackBehavior`.
- Steuerwerte der Definition: `sitRandomly` (bool), `sittingTypeNbr` und `idleEmoteChance` (Gesten im Sitzen, Vorgabe
  `idleEmoteChance = 1000` im Konstruktor `AnimalDefinitions.<init>`; gelesen `AnimalDefinitions` Off. 1236-1256 / 1420).
- Vanilla-Debug: "Force sit" (ISAnimalContextMenu.lua:383-387, :549-556; Server ClientCommands.lua:829-836 mit
  `Capability.AnimalCheats`) ruft `debugForceSit` (`IsoAnimal` Dump :9827): stellt nur `sitInTime`/`sitOutTime` -- wirkt also
  **nur bei `sitRandomly = true`** (checkSit muss laufen). Fuer unseren Baeren ohne Wirkung.

### 1.5 Nachtrhythmus gibt es nur beim Stall

`AnimalDefinitions.isInsideHutchTime` (Dump :1890 ff.) vergleicht `GameTime.getHour` mit `enterHutchTime`/`exitHutchTime`; gesetzt nur
fuer Kueken/Huhn/Hahn/Truthahnkueken (ChickenDefinitions.lua:104-105 "20"/"7", TurkeyDefinitions.lua:85-86). Die Tiere gehen in den
Stall (IsoHutch) und sind dann aus der Welt -- kein sichtbares Schlafen.

### 1.6 Sandbox

`zombie/SandboxOptions.class` kennt an Tier-Optionen nur AnimalEggHatch, AnimalRanchChance, AnimalTrackChance, AnimalSpeed,
AnimalGrassRegrowTime, AnimalStatsModifier, AnimalMilkIncModifier, AnimalPregnancyTime, AnimalAgeModifier, AnimalWoolIncModifier,
AnimalPathChance, AnimalMatingSeason, AnimalMetaPredator, AnimalMetaStatsModifier, AnimalSoundAttractZombies (Byte-Suche nach
`[Aa]nimal`). **Nichts zu Schlaf.**

---

## 2. AnimSet `buck` und Vorbilder

### 2.1 Vanilla `AnimSets/buck/idle` (Zustand idle)

| Knoten (Datei) | Clip | Bedingung | Uebergaenge |
|---|---|---|---|
| idle1 (`idle1.xml:4`) | DeerStag_Idle01 | keine | -> idleSit mit **DeerStag_IdleToSitting** (`idle1.xml:7-8`) |
| idle2 (`idle2.xml:4`) | DeerStag_Idle02, nicht geloopt | idleAction = idle1 | -> idleSit mit DeerStag_IdleToSitting (`idle2.xml:19-20`) |
| idle3, Idle4 | Idle03, IdleEating01 | idleAction = idle2/idle3 | erben von idle2 |
| **idleSit** (`idleSit.xml`) | **DeerStag_SittingIdle** (:4), Blend 0,50, geloopt (Vorgabe `AnimNode.<init>` Off. 86-87 `isLooped = true`) | **idleAction = sit** (:6-10) | -> idle1/idle2/idle3/idle mit **DeerStag_SittingToStanding** (:11-26) |

Weitere Zustaende der Gruppe: alerted, deadbody, death, eating (`DeerStag_IdleEating01`, idleAction = eat), falldown, followwall,
hitreaction, onground (`DeerStag_Dead`), onhook, pathfind, trailer, walk. **Kein Liege-/Schlafzustand ausser idleSit.**
Aktionsgruppe `actiongroups/buck`: idle wechselt nur nach eating/walk/pathfind/hitreaction/alerted/falldown/onground/onhook/trailer
(`idle/to_*.xml`) -- Liegen bleibt also im Zustand idle, ein Unterknoten.

### 2.2 Unsere Kopie in NCBearTest

`NCBearTest/42/media/AnimSets/buck/idle/` enthaelt **nur Zusatzknoten** (keine Vanilla-Datei ueberschrieben): NCBear_Bite, _Eat,
_Maul, _Rear, _Sit, _SitDown, _Slam, _StandUp, _SwipeL, _SwipeR. Alle mit `m_ConditionPriority 10` und einer STRING-Bedingung auf
**`NCBearAct`** (z. B. `NCBear_Sit.xml`: Wert `sit`, `m_Looped true`). Kein Liege-/Schlafknoten.

### 2.3 Vorbilder anderer Gruppen (alle ueber `idleAction = "sit"`, Knoten `idle/idleSit.xml`)

| Gruppe | Hinlegen (Uebergang hinein) | Liegen/Ruhen | Aufstehen |
|---|---|---|---|
| buck / doe / fawn | DeerStag_/Deer_/DeerFawn_IdleToSitting | ..._SittingIdle | ..._SittingToStanding |
| raccoon | **Rac_IdleToLieDown** (`raccoon/idle/idle1.xml:10-11`) | **Rac_IdleLyingDown** (`idleSit.xml:4`) | **Rac_LyingDownToIdle** (:12-13) |
| cow / pig / ewe / lamb / ram | Cow_/FarmPig_/Sheep_..._Sit_In | ..._Sit_Idle01 | ..._Sit_Out |
| piglet | (kein Clip im Uebergang) | Piglet_Sit_Idle01 | Piglet_Sit_Out |
| hen/chick/cockerel/turkey | idleSit + Varianten `idleSit2/3` ueber `sittingAnim` (z. B. `hen/idle/idleSit2.xml`: `sittingAnim = sit1`, Ereignis `idleActionEnd`) | | |

Der Waschbaer zeigt am deutlichsten: **"sit" ist in der Engine das Hinlegen/Ausruhen.** Ein echter Schlafzustand fehlt in jeder Gruppe.

### 2.4 Welche Clipnamen braucht unser GLB?

`AnimationPlayer.play(String, Z, Z, F)` Off. 97-111 sucht den Namen in `skinningData.animationClips` **des Baer-Modells**. Die Namen
kommen aus der XML, also:

- **Weg A (Empfehlung, Ruheplatz der Engine):** genau diese drei, Schreibweise fest:
  - `DeerStag_IdleToSitting` -- Hinlegen, einmal. Anfang = Grundhaltung (wie DeerStag_Idle01), Ende = Schlafhaltung.
  - `DeerStag_SittingIdle` -- Schlafen, Schleife (erstes = letztes Bild, ruhiges Atmen).
  - `DeerStag_SittingToStanding` -- Aufwachen/Aufstehen, einmal. Anfang = Schlafhaltung, Ende = Grundhaltung.
  Wie alle Ruheclips: Translation_Data ohne Weg, Bip01 still (sonst wandert er beim Hinlegen; Muster `anim_clips.md` "Alle neuen
  Clips: Translation_Data ueber den ganzen Clip 0"). Die echten Rehe behalten ihre eigenen Clips (Aufloesung je Netz).
- **Weg B (eigene Variable wie heute beim Sitzen):** freie Namen, z. B. `NCBear_LieDown`, `NCBear_Sleep`, `NCBear_WakeUp`, dazu drei
  neue Knoten `AnimSets/buck/idle/NCBear_LieDown.xml` usw. mit `NCBearAct`.
- Heute im GLB (`NCBear.glb`, JSON-Kopf gelesen): DeerStag_Dead, _Death, _Idle01, _Run, _Walk, NCBear_Bite, _Eat, _Maul, _Rear, _Sit,
  _SitDown, _Slam, _StandUp, _SwipeL, _SwipeR; 26 Gelenke. **Keiner der Liege-Clips.**

---

## 3. NCBearTest heute

### 3.1 Wie Sitzen und Fressen ausgeloest werden

- Ein Schreiber: `NCBearFight.lua` (Kopf :19). `calmTo` (:1492-1498) setzt `B.a:setVariable("NCBearAct", sub)` (Form ISPetAnimal.lua:43);
  `calmStart` (:1500-1507) sperrt die Bewegung (`setBlock` :442 ff. -> `getBehavior():setBlockMovement(true)`, ISPetAnimal.lua:36)
  und erneuert die Sperre, bevor die Engine sie bei 8000 aufhebt (`refreshBlock` :470 ff.; Jar `wanderIdle` Off. 0-39).
- Unterzustaende `sitdown` -> `sit` (Schleife) -> `standup`, `eat` (Schleife). Ende eines Einmal-Clips ueber das Knoten-Ereignis
  `NCBearDone=true` oder die Frist Dauer + 1 s (`updateCalm` :1591-1668). Von selbst sitzen: `autoSit` (:1536-1547, alle 20 s,
  Chance `sitChance` 10 %).
- Kampf geht vor: in der Ruhe wird weiter gesucht (`pickTarget`); sitzend erst `standup`, dann `startFight` (:1607-1625, `standDone`
  :1549-1554). Laerm-Ausflug: `clipWatch` "away"/"back", `calmBack` (:1559-1588), mehr als `CALM_NOISE_MAX` = 4 Stoerungen in 30 s
  (:197) -> Ruhe aufgeben. Getroffen -> `calmEnd(B, "hurt")` (:1679).
- **Nur Einzelspieler:** `isSP()` (:227-229, `not isClient() and not isServer()`), Kopf :4-5 ("tut im Mehrspieler nichts").
- Testbefehle nur in `client/NCBearBench.lua` (`NCBear_Sit/Stand/Eat` :76-93, ueber `F.Calm`).

### 3.2 Geht Schlafen auf demselben Weg?

Ja, technisch ohne Neues: ein weiterer Unterzustand der Phase `calm` (z. B. `liedown` -> `sleep` -> `wakeup`) mit derselben
Bewegungssperre, Suche, Laerm- und Treffer-Behandlung. Unterschied je Weg:
- **Weg B** (`NCBearAct = liedown/sleep/wakeup`): 1:1 wie Sitzen, eigene XML-Knoten, Ende per `NCBearDone`. Aber: nur SP sichtbar (5.2).
- **Weg A** (`idleAction = sit`): keine XML; Hinlegen und Aufstehen spielt die Engine als Uebergang von selbst, sobald Lua die
  Variable setzt bzw. loescht. Die Vanilla-Uebergaenge tragen **keine Ereignisse** (idle1.xml/idleSit.xml), also kein `NCBearDone`:
  Ende nur per Uhr (Clipdauer + `F.FRIST`), wie heute schon als Rueckfall.

### 3.3 Was passiert, wenn ein Clip fehlt?

- `AnimationPlayer.play(String, Z, Z, F)` Off. 113-152: Clip nicht gefunden -> Warnung "Anim Clip %snot found: %s" (nur mit
  Debug-Typ `Animation`) und `null`. `AnimLayer.startTrackGeneric` Off. 182-217: bei `null` bekommt der Knoten keine Spur.
- `AnimationPlayer.updateInternal` Off. 35-44: bei 0 Spuren werden die Knochen nicht mehr gerechnet -> die letzte Haltung bleibt
  stehen. **Lesart: der Baer erstarrt stehend** (kein T-Pose: seine Ruhehaltung ist ohnehin fast gleich Idle01, bau_lebend.md:36 vs.
  Tabelle :40). Was genau waehrend des 0,5-s-Ausblendens zu sehen ist: **ungeprueft**.
- Heute nicht ausloesbar, weil niemand `idleAction = sit` beim Baeren setzt (3.4).

### 3.4 Schlaeft unser Baer heute schon nachts, unsichtbar?

**Nein.** (1) Kein Schlaf-KI-Zustand (1.1). (2) `sitRandomly = false` (NCBearDefs.lua:93) -> `checkSit` laeuft nie (`wanderIdle`
Off. 296-310); `debugForceSit` wirkt ohne checkSit nicht (1.4). (3) Kein Zonenzustand in `buck` (1.3), keine Wandergruppe
(NCBearDefs.lua Kopf :5-6). (4) Ausserdem blockiert die Ruhe-Phase per `setBlockMovement(true)`: dann kehrt `wanderIdle` schon
Off. 4-149 zurueck. Hunger und Durst laufen also heute immer voll (kein halber Satz).

### 3.5 Nebenfund (nicht Schlaf, betrifft Fuettern/Zaehmen)

`IsoAnimal.eatFromLured` Off. 21-27 setzt `idleAction = "eat"` -> Aktionsgruppe `buck/idle/to_eating.xml` (`isAnimalEating`) ->
Knoten `eating` mit **`DeerStag_IdleEating01`**, das unser GLB nicht hat -> Erstarren wie 3.3. Ob der Baer mit Futter lockbar ist
(Locken der Engine), **ungeprueft**; vor dem Zaehmen-Bau (Fuettern aus der Hand) pruefen, sonst unseren Fress-Clip zusaetzlich
unter diesem Namen ins GLB legen.

### 3.6 Nebenfund fuer den Schlafton (anderer Bericht)

Ein Rassenton ueber `animal:playBreedSound(name)` (heute schon benutzt, ISHutchGrabAnimal.lua:31 laut NCBearDefs.lua-Kopf) geht ueber
`AnimalSoundState` (`IsoAnimal.playBreedSound` Dump :9006 ff.). `AnimalSoundState.start` Off. 33-112 erzeugt ein Weltgeraeusch
(lockt Zombies) nur, wenn die Sandbox `AnimalSoundAttractZombies` an ist **und** die Definition `idleSoundRadius > 0` und
`idleSoundVolume > 0` hat. Der Baer setzt beides nicht (NCBearDefs.lua), der Konstruktor `AnimalDefinitions.<init>` setzt
`idleSoundRadius` nicht vor -> 0. Lesart: ein leises Schnarchen als Rassenton lockt keine Zombies (ungespielt).

---

## 4. Aufwachen

### 4.1 Was bei Vanilla das Ruhen beendet

- `checkSit` (nur mit `sitRandomly`): Ablauf der Ruhezeit, Hunger > 0,2, Leine, Regen ohne Dach (1.4).
- `ISPetAnimal` (Streicheln): setzt `idleAction = "petting"` (:43) und loescht danach (:48/:55/:62) -> das Tier steht auf.
- `IsoAnimal.eatFromLured` (Locken mit Futter): `idleAction = "eat"` (3.5).
- **Nicht** beendet wird es durch Laerm oder Treffer: `respondToSound` und `fleeFromAttacker` schicken das Tier auf einen Weg
  (`bPathfind`, Aktionszustand pathfind), loeschen `idleAction` aber nicht (IsoAnimal ruft `clearVariable` gar nicht auf: 0 Treffer
  im Dump; `BaseAnimalBehavior.clearIdleAction` Off. 0-42 loescht nur Werte, die mit "idle" beginnen).
  Folge: das Tier springt aus dem Liegen ohne Aufsteh-Clip in den Lauf und legt sich am Ende **ohne** Hinlege-Clip wieder hin
  (idleSit direkt, Blend 0,50) -- die bekannte Luecke aus `anim_review_gegen.md:81-83` (Sitzen, 62,7 cm Sprung).
- Zombies: mit `fleeZombies = false` und `wild = false` (NCBearDefs.lua:86/:88) reagiert die Engine auf Zombies gar nicht.

### 4.2 Kevins Regel "Kampf hat Vorrang" -- passt, aber nur mit unserem Lua

Die Engine weckt nie. Also entscheidet unser Lua, je Takt der Ruhe-Phase (wie heute beim Sitzen):

| Ausloeser | Vorschlag | Beleg / Grundlage |
|---|---|---|
| Zombie oder feindlicher Bandit im Suchradius | wecken: `clearVariable("idleAction")`, Aufsteh-Clip abwarten (Dauer + Frist), dann `startFight` | heutiger Sitz-Zweig `updateCalm` :1607-1625 |
| Getroffen | wecken, `idleAction` sofort loeschen (sonst legt er sich nach der Flucht wieder hin) | `updateBear` :1676-1682, 4.1 |
| Laerm-Ausflug (Engine-Flucht) | beim "away" sofort `idleAction` loeschen; beim "back": Ziel da -> Kampf, sonst nach kurzer Pause neu hinlegen; mehr als 4 Stoerungen/30 s -> wach bleiben | `calmBack` :1559-1588, `CALM_NOISE_MAX` :197 |
| Besitzer streichelt/fuettert | Lua merkt `idleAction ~= "sit"` und beendet den Schlaf ohne eigenen Clip | 4.1 (Engine schreibt "petting"/"eat") |
| Morgen | Schlaffenster wie NPC Crew: 22-7 Uhr | `BanditsNPC.Routine.SleepStart/End` BanditsNPCRoutine.lua:223-229; Uhr `getGameTime():getHour()` (Vanilla STrapGlobalObject.lua:535) |
| Hunger/Durst zu hoch | wach werden, fressen gehen (Zahlen im Bau) | eigene Werte (Beduerfnisse spaeter) |

- **Zeitbedarf:** zwischen "Zombie gesehen" und erstem Hieb liegt die Dauer des Aufsteh-Clips (Richtwert wie `NCBear_StandUp`
  1,30 s, `F.ACTS` NCBearFight.lua:56). Wer das kuerzer will: Weckradius etwas groesser als den Kampfradius (`radius = 10`, :86) oder den
  Aufsteh-Clip kurz halten. Ein direkter Sprung Liegen -> Angriff (NCBearAct waehrend `idleAction = sit`) gewinnt wegen
  Prioritaet 10 sofort und sieht wie ein Ruck aus -- vermeiden.
- **Passiv:** offen (Frage an Kevin, Abschnitt 8).
- **Hinlegen nur aus idle1:** die Vanilla-Uebergaenge fuehren nur von idle1/idle2 nach idleSit (2.1). Kommt der Baer aus einem
  NCBear-Knoten (z. B. nach `standup`), erst `NCBearAct` loeschen und ~0,5 s (Blend idle1 0,40) stehen lassen, dann `sit` setzen;
  sonst legt er sich ohne Hinlege-Clip hin.

### 4.3 Zusammenspiel mit dem Laerm-Code (baer-laerm)

- `respondToSound` laeuft in `IsoAnimal.updateInternal` vor der Animation, OnTick kommt danach (laerm_forschung_zustand.md 1.1/1.2):
  der Sprung aus dem Liegen in den Fluchtweg ist von Lua aus **nicht** zu verhindern -- genau wie heute beim Sitzen.
- Was schreckt: Weltgeraeusche mit `stresshumans`/`stressAnimals` 4 bis R Kacheln weit, vor allem Zombie-Schlaege an Zaun/Tuer/Fenster
  (laerm_forschung_laerm.md 0.1). Fuer einen Schlafenden ist "aufwachen" darauf sogar richtig (Zombie am Zaun = Gefahr).
- `fleeStop`/`fleeWait` und `clipWatch` koennen unveraendert weiterlaufen; neu ist nur: im Schlaf beim ersten "away" `idleAction`
  loeschen (sonst 4.1-Sprung zurueck ins Liegen).
- Eigener Kampflaerm (Lua `addSound`) erzeugt keinen Stress (laerm_forschung_laerm.md 0.1) -> weckt nicht ueber die Engine.

---

## 5. Mehrspieler

### 5.1 Wer rechnet

- Die Tier-KI laeuft nur, wo `IsoAnimal.isLocalPlayer()` wahr ist: Off. 0-11 = `not GameClient.client` -> Einzelspieler und Server.
  `AnimalIdleState.execute` Off. 5-17 kehrt auf Clients sofort zurueck (kein `wanderIdle`, kein `checkSit`).
- Unser Schlaf-Lua muss im MP also auf dem **Server** laufen. Heute ist die ganze Baer-KI SP-only (NCBearFight.lua :4-5, :227-229);
  MP gehoert nach PLAN in B9. Server-Lua mit Takt ist belegt (z. B. `Events.EveryOneMinute.Add` SCampfireSystem.lua:183,
  `Events.OnTick.Add` forageServer.lua:502).

### 5.2 Was zum Client reist

- `AnimalSynchronizationManager.sendUpdateToClient` Off. 436 -> `NetworkPlayerAI.setAnimalPacket` -> `NetworkPlayerAI.set(AnimalPacket,
  UdpConnection)` **Off. 224-253**: `getVariableString("idleAction")` ins Paket, Flag 2, wenn nicht leer. `AnimalPacket.write` Off. 83-97
  schreibt es (`putUTF`). Takt: `SHORT_DISTANCE_ANIMAL_UPDATE_RATE_MS = 800`, `LONG_... = 1000` (`javap -constants`).
- Client: `AnimalUpdatePacket.parse` Off. 728 -> `NetworkPlayerAI.parse(AnimalPacket)` **Off. 709-737**: Flag 2 -> `setVariable("idleAction",
  wert)`, sonst `clearVariable("idleAction")`. **Jeder Wert reist**, nicht nur "sit".
- Sonst reist an Animationszustand nur `AnimalStateVariables$Flags`: isOnFloor, isDead, isRunning, isAttacking. **`NCBearAct` reist
  nicht** (kein Feld im AnimalPacket; Feldliste `dump/zombie.network.packets.character.AnimalPacket.txt:3-65`).
- NPC Crew hat denselben Weg fuer die Streichel-Reaktion selbst nachgelesen und gemessen beschrieben
  (BanditsNPCLivestockAnimalOps.lua:1093-1099: gleiche Offsets, 800/1000 ms).

### 5.3 Folgen

- **Weg A:** Server setzt `idleAction = "sit"` -> spaetestens nach ~1 s haben alle Clients den Wert und spielen idleSit samt
  Uebergang selbst. Ob der Client den Uebergangs-Clip sauber spielt (Wert kommt sprunghaft), **im MP ungeprueft** (Lesart: ja, die
  Hoftiere liegen im MP nur ueber genau diesen Weg, weil checkSit nur auf dem Server laeuft).
- **z Z z-Anzeige auf dem Client:** `animal:isAnimalSitting()` (belegt clientseitig ISAnimalContextMenu.lua:383) oder
  `getVariableString("idleAction") == "sit"` (Form NPC Crew BanditsNPCLivestockCoop.lua:917, Vanilla-Methode IsoGameCharacter
  ISWorldObjectContextMenu.lua:2624). Kein eigener Netzbefehl noetig.
- **Weg B:** Clients saehen den Schlaf nicht; noetig waere ein eigener Server->Client-Befehl und ein Setzen von `NCBearAct` auf jeder
  Client-Kopie (das Tierpaket fasst `NCBearAct` nicht an, es bliebe also stehen) -- eine neue Netz-Naht mit eigenen Fehlerquellen
  (spaet beitretende Clients, Baer entlaedt/laedt neu), ungeprueft.
- **Nebenfund fuer B9 (alle Ruhe-Posen):** Sitzen und Fressen laufen heute ueber `NCBearAct` und waeren im MP unsichtbar. Ein eigener
  `idleAction`-Wert (z. B. "ncsit") mit Knoten, deren Bedingung auf `idleAction` statt `NCBearAct` steht, reiste umsonst mit. Dabei:
  Wert darf **nicht mit "idle" beginnen** (`BaseAnimalBehavior.clearIdleAction` Off. 0-42 loescht solche) und die Knoten duerfen kein `idleActionEnd`
  senden (`AnimalIdleState.animEvent` Off. 0-54 loescht dann alles ausser "sit").
- Risiko MP: Streichelt ein Client den schlafenden Baeren, loescht ISPetAnimal auf seiner Kopie `idleAction`; das naechste Paket
  setzt "sit" wieder -> kurzes Aufstehen/Hinlegen auf diesem Client (ungeprueft). Der Server entscheidet ueber den Schlaf.

---

## 6. Empfehlung

### 6.1 Weg A: Ruheplatz der Engine (`idleAction = "sit"`) als Schlaf -- empfohlen

| Punkt | Weg A (idleAction "sit") | Weg B (NCBearAct) | Weg C (eigener idleAction-Wert + eigene Knoten) |
|---|---|---|---|
| Neue AnimSet-XML | **keine** | 3 Knoten | 1-3 Knoten |
| Hinlegen/Aufstehen | Vanilla-Uebergaenge spielen von selbst | eigene Einmal-Knoten, Ende per `NCBearDone` | Aufstehen per `m_Transitions` im eigenen Knoten moeglich, Hinlegen nur als eigener Einmal-Knoten (Uebergang aus idle1 nur durch Ueberschreiben der Vanilla-idle1.xml = trifft alle Rehe -> nein) |
| Clipnamen | fest: DeerStag_IdleToSitting / _SittingIdle / _SittingToStanding | frei | frei |
| MP-Bild | **umsonst** (5.2) | eigener Netzbefehl noetig | umsonst |
| Halber Hunger/Durst, kein Wandern | **ja** (1.4) | nein (Sperre ja) | nein |
| z Z z-Frage auf dem Client | `isAnimalSitting()` | eigene Marke | `getVariableString` |
| Ende-Erkennung | nur Uhr | Ereignis + Uhr | Ereignis (eigene Knoten) + Uhr |
| Gefahr | ein Mod/Patch, der `sitRandomly` des Baeren wahr setzt, laesst ihn alle 3-7 h von selbst liegen; Vanilla-Patch benennt idleSit-Clips um | wie heute | Wert-Falle "idle..." |

Ablauf fuer den spaeteren Bau (Unterzustand der Phase `calm`, nur Skizze):
1. Einschlafen (Nacht 22-7 Uhr, Ruhe, kein Ziel in den letzten Suchtakten, nicht kurz nach Kampf/Treffer): `NCBearAct` loeschen,
   Bewegung sperren (wie `calmStart`), nach >= 0,5 s in idle1 `setVariable("idleAction", "sit")` -> Engine spielt
   `DeerStag_IdleToSitting`, dann `DeerStag_SittingIdle` in Schleife.
2. Waehrend des Schlafs: Suche weiter, Schnauben aus (oder eigenes leises Schlaf-Atmen, anderer Bericht), Sperre erneuern.
3. Aufwachen (4.2): `clearVariable("idleAction")` -> Engine spielt `DeerStag_SittingToStanding`; nach Dauer + `F.FRIST` frei bzw.
   `startFight`. Bei Treffer/Laerm-"away" sofort loeschen.
4. Jede Ruhe-Ende-Stelle (`calmEnd`) loescht `idleAction` nur, wenn sie "sit" ist (NPC Crews Muster:
   BanditsNPCLivestockAnimalOps.lua:1060 "nur loeschen, wenn noch unser Wert").
5. `sitRandomly = false` bleibt Pflicht (NCBearDefs.lua:93); in `BanditsNPCBear*` als Kommentar festhalten.

Optional spaeter (nicht im ersten Bau): Schlafgesten (Ohr zuckt, dreht sich) ueber `sittingTypeNbr` + `idleEmoteChance` und eigene
Knoten mit Bedingung `sittingAnim = sitN` (Vorbild `hen/idle/idleSit2.xml`). Laeuft nur ohne Bewegungssperre (`wanderIdle` kehrt mit
Sperre schon Off. 4-149 zurueck) und `sittingAnim` reist nicht ins MP. Deshalb eher eine eigene Lua-Geste.

### 6.2 Engine-Aufrufe (eiserne Regel)

| Aufruf | Fundstelle (gleiche Argumenttypen) |
|---|---|
| `animal:setVariable("idleAction", "sit")` (String, String) | ISPetAnimal.lua:43 (`"petting"`); NPC Crew BanditsNPCLivestockAnimalOps.lua:1077/:1112 |
| `animal:clearVariable("idleAction")` (String) | ISPetAnimal.lua:48/:55/:62 |
| `animal:isAnimalSitting()` | ISAnimalContextMenu.lua:383 |
| `animal:getVariableString("idleAction")` (String) | Methode IsoGameCharacter, ISWorldObjectContextMenu.lua:2624 (am Spieler); am Tier NPC Crew BanditsNPCLivestockCoop.lua:917; heute schon im Baeren NCBearFight.lua:1349 |
| `animal:getBehavior():setBlockMovement(bool)` | ISPetAnimal.lua:36/:49 (heute schon benutzt) |
| `getGameTime():getHour()` | STrapGlobalObject.lua:535 |
| **nicht vorschlagen:** `debugForceSit` (Debug, wirkungslos ohne sitRandomly), `VirtualAnimal:forceWakeUp` (anderes Objekt) | -- |

### 6.3 Copy-Paste nach NPC Crew

- Weg A bringt **keine** neue AnimSet-Datei und **keine** neue Animationsvariable mit: nur drei Clips im selben GLB-Pfad und Lua in
  `BanditsNPCBear*.lua`. Keine Namenskollision moeglich (idleAction ist Vanilla).
- Naht: NPC Crews Tierpfleger setzt/loescht `idleAction` (Wert "petting") auf Tieren, die er streichelt
  (BanditsNPCLivestockAnimalOps.lua:1033-1115, nur eigener Wert, "nur wenn noch petting"). Ob der Baer je in dessen Kandidatenlisten
  faellt (Artfilter), **ungeprueft** -- bei der Uebernahme in die Naht-Liste.

---

## 7. Risiken

1. **Sprung bei Laerm/Treffer** (Engine-Flucht aus dem Liegen ohne Aufsteh-Clip) -- von Lua nicht verhinderbar (4.3), wie beim Sitzen.
2. **Ende nur per Uhr** bei Weg A (Vanilla-Uebergaenge ohne Ereignis): stimmen `F.ACTS`-Dauern nicht mit dem GLB, steht er zu frueh/spaet.
3. **Hinlegen ohne Clip**, wenn `sit` gesetzt wird, waehrend noch ein NCBear-Knoten laeuft (Prioritaet 10 haelt bis zum Loeschen,
   danach Blend 0,50 statt Uebergang) -> Reihenfolge 4.2 einhalten.
4. **Halber Hunger** im Schlaf (1.4) wirkt auf die Engine-Werte; spaetere eigene Beduerfnisse muessen das wissen.
5. **MP ungespielt**: Client-Bild der Uebergaenge, Streicheln eines Schlafenden auf einem Client (5.3).
6. Fehlende Clips -> Erstarren (3.3). Nur zusammen mit dem neuen GLB ausrollen.
7. Nebenfund Fressen per Locken -> `DeerStag_IdleEating01` fehlt (3.5).

## 8. Offene Fragen an Kevin

1. **Passiv und Schlaf:** Ein passiver Baer, ein Zombie kommt -- weiterschlafen, oder aufwachen und zum Besitzer gehen?
2. **Wann schlafen:** nur nachts (wie die NPCs 22-7 Uhr) oder auch tagsueber kurze Nickerchen?
3. **Jungtier/Halbstark:** gleicher Schlaf, oder schlaeft das Jungtier oefter/laenger?
4. **Wecken durch den Besitzer:** soll Streicheln/Fuettern ihn wecken (Engine tut das ohnehin), oder soll ein schlafender Baer gar
   nicht streichelbar sein?

## 9. Was ich nicht pruefen konnte

- Bild im Spiel (Uebergaenge, Erstarren bei fehlendem Clip, MP-Client): alles Lesart aus dem Jar.
- Ob der Baer mit Futter gelockt werden kann (3.5).
- Ob NPC Crews Tierpfleger den Baeren je anfasst (6.3).

Statisch geprueft, nicht gespielt.
