# Baer kaempft - Lua-Bau (NCBearTest)

> **Nachgebessert 08.11. (Fixer):** Weiten jetzt 1,1 / 1,4 / 1,5 / 1,2, Treffer nur mit Sicht und ohne Wand, Geist-Ziel,
> Fahrzeug, Fehldiagnose u. a. -- die Werte unten sind teils ueberholt, gueltig ist `kampf_fix.md`.

Stand 08.11.2026, PZ 42.21, Bandits 42.21. Gebaut nach `kampf_spez.md` unter
`_arbeit/baer_kampf/mod/42` (nichts in `NCBearTest` kopiert, nichts unter NPC Crew oder Bandits geaendert).
**Statisch geprueft, nicht gespielt.** Attrappe in Lua 5.1: 79 Pruefungen gruen.

## Dateien (alle LF, ASCII, ohne BOM)

| Datei unter `_arbeit/baer_kampf/mod/42/media/` | neu/geaendert | Inhalt |
|---|---|---|
| `AnimSets/buck/idle/NCBear_Rear.xml` | neu | `NCBearAct=rear`, Clip `NCBear_Rear`, PlaySound `NCBear_Roar` 0,27, Done End |
| `AnimSets/buck/idle/NCBear_SwipeL.xml`, `NCBear_SwipeR.xml` | neu | `swipeL`/`swipeR`, PlaySound `SledgehammerSwing` 0,27, Hit 0,42, Done End |
| `AnimSets/buck/idle/NCBear_Slam.xml` | neu | `slam`, `NCBear_Growl1` 0,05, `AttackStomp` 0,55, Hit 0,57, Done End |
| `AnimSets/buck/idle/NCBear_Maul.xml` | neu | `maul`, `NCBear_Growl2` 0,10, Hit 0,34, Done End |
| `scripts/nc_bear_sounds.txt` | neu | `module Base`, sechs Toene `NCBear_Roar/Growl1/Growl2/Growl3/Huff/Pain`, je `file = media/sound/<Name>.wav` |
| `lua/shared/NCBearFight.lua` | neu | Kampf, Konsole |
| `lua/shared/NCBearDefs.lua` | geaendert | nur Rasse `brown.sounds`: `pain`, `death` (beide `NCBear_Pain`), `huff`, `growl1..3` |
| `sound/*.wav` | vom Tonschnitt | sechs Dateien, Namen passen zum Skript |

Alle Knoten: Prioritaet 10, eine STRING-Bedingung auf `NCBearAct` (Form wie Vanilla `buck/idle/idle2.xml`, `m_Value`),
nicht geloopt, `m_SyncTrackingEnabled false`. Ereignisse wie `player/bumped/bumpFall.xml` (SetVariable End, PlaySound TimePc).
XML mit Python geparst: wohlgeformt.

**Fuer den Integrator:** die `m_AnimName` muessen den Aktionsnamen im neuen `NCBear.glb` gleichen; Dauern stehen als
Konstanten oben in `NCBearFight.lua` (`F.ACTS`: 3,0 / 1,1 / 1,1 / 2,2 / 1,6 s). Weicht der Animator ab: `F.ACTS` und die
`m_TimePc` der Treffer nachziehen. `mod.info` sagt noch "friedlich" (nicht von mir geaendert).

## Verhalten (Spez 5.2)

Je Baer (nur Art `bear`, nie `bearstag`) ein Zustand: Ruhe -> **Drohen** (Aufrichten + Bruellen beim ersten Kontakt, wenn das
letzte Bruellen 45 s her ist) -> **Anrennen** (`fleeTo`, alle 0,75 s neu, Huff beim Losrennen) -> **Angriff** -> 0,35 s Pause ->
naechster. Angriffswahl: liegt das Ziel in 1,7 -> **Biss**; mindestens 2 weitere vorne in 2,0 und Doppelschlag 10 s frei ->
**Doppelschlag**; bei 3+ Gegnern in 3 und Bruellen frei 25 % **erneut Aufrichten**; sonst **Prankenhieb** links/rechts im Wechsel
(50 % ein Knurren dazu). Ende: 3 s kein Ziel, 25 Kacheln vom Kampfbeginn, 90 s Kampf (dann 20 s Ruhe), vom Spieler getroffen
(Kampf ab, 20 s Ruhe, die Engine laesst ihn fliehen). Danach **Rueckkehr**: ueber 5 Kacheln vom Kampfbeginn rennt er dorthin zurueck.

Treffer erst, wenn die Animation `NCBearHit=true` setzt; Ziel, Abstand, Kegel und Regel werden dann neu geprueft.

| Angriff | Weite (x Baerengroesse) | Kegel | Ziele | Schaden | Umwerfen |
|---|---|---|---|---|---|
| Prankenhieb L/R | 1,8 | 110 Grad, 15 Grad zur Schlagseite (-40..+70 bzw. -70..+40) | Haupt + 3 | 1,3 / 0,8 | alle Ueberlebenden |
| Doppelschlag | 2,0 | 160 Grad | 5 | 1,0 | alle |
| Biss | 1,7 | 60 Grad | nur Hauptziel, nur liegend | 2,5 | - |

Alles mal `dmg` (1,0). Normaler Zombie (1,8-2,1): zwei Hiebe oder Hieb + Biss. Treffer: Leben setzen, Blut, Ton am Ziel
(`SledgehammerHit`, Nebenziele `MacheteHit`, Biss `ZombieBite`, toedlich `HeadSmash`, hoechstens 2 Toene je Angriff), toedlich
`Kill(nil)`, sonst `knockDown(vonHinten)` wenn er noch steht. Jedes Ziel je Angriff einmal, Deckel 6.

**Abweichung von der Spez:** Bisswerte 1,4 -> 1,7, weil er bei 1,5 ankommt und der Umgeworfene dort liegt (mit 1,4 gab es in der
Attrappe nie einen Biss). Laerm-Mitte am Hauptziel statt am Baeren (unten).

## Harte Regel (F.IsTarget)

Liste nur `getCell():getZombieList()`, dazu `instanceof(z, "IsoZombie")`. Nie: tot, `isOnKillDone`, gezogene Leiche, scheintot,
andere Ebene, NPC-Crew-Marke `tcUid` am Koerper, Bandit-Marke ohne Gehirn, `recruited`, `npcNeutral`, `npcUid`, `programFallback ==
"NPCNeutral"`, Programm `NPC*`, `loyal`. Bandit nur mit `hostile` oder `hostileP` (Bandits' `Bandit.IsHostile`). Crew-Marken stehen VOR
`hostileP` (NPC Crew setzt es kurz, `BanditsNPCCompat.lua:171-195`). Nur ModData-Felder, kein Aufruf in NPC Crew oder Bandits.
`brain.master` ist kein Begleiter-Merkmal (Bandits setzt es beim Spawnen, `BanditServerSpawner.lua:423`) - nicht benutzt.

## Fundstellen der Engine-Aufrufe

| Aufruf | Fundstelle |
|---|---|
| `isClient()`/`isServer()` SP-Test | ISEatFoodAction.lua:136 |
| `getCell():getZombieList()` | Bandits client/BanditZombie.lua:110 |
| `getCell():getObjectListForLua()`, `instanceof(o,"IsoAnimal")`, `getAnimalType()` | DebugContextMenu.lua:615-623, ISAnimalUI.lua:65 (wie NCBearSpawn.lua) |
| `getCell():getGridSquare(x,y,z)` | DebugContextMenu.lua:1436 |
| `animal:setVariable/clearVariable(String..)` | ISPetAnimal.lua:43 / :48 |
| `animal:getVariableString(String)` | ISWorldObjectContextMenu.lua:2624 (Spez nannte ZATime.lua:13 - das steht in einem Kommentarblock) |
| `animal:getBehavior():setBlockMovement(bool)` | ISPetAnimal.lua:36 / :49 |
| `animal:faceThisObject(obj)` | ISPetAnimal.lua:17 |
| `animal:fleeTo(square)` | ISMilkAnimal.lua:38 |
| `animal:stopAllMovementNow()` | ISAnimalContextMenu.lua:760 |
| `animal:getActionStateName()` | Bandits ZASmack.lua:486 (am Charakter) |
| `animal:CanSee(zombie)` | Bandits BanditUpdate.lua:1087, :1203 |
| `animal:getData():getSize()` | ISPetAnimal.lua:31 |
| `animal:getHealth()`, `isExistInTheWorld()` | ISAnimalUI.lua:15 |
| `animal:isDead()` | ISHutchUI.lua:427 |
| `animal:playBreedSound(String)` | ISHutchGrabAnimal.lua:31 |
| `z:isOnKillDone()` | Bandits ZASmack.lua:357 |
| `z:isAlive()`, `z:getHealth()` | Bandits BanditUpdate.lua:1203 |
| `z:isReanimatedForGrappleOnly()` | Bandits BanditCompatibility.lua:189 |
| `z:isFakeDead()` | DebugContextMenu.lua:662 |
| `z:getModData()`, `.brain` | Bandits BanditBrain.lua:4-5 |
| `z:getVariableBoolean("Bandit")` | Bandits BanditZombie.lua:137 |
| `z:isProne()`, `z:getActionStateName()` | Bandits ZASmack.lua:486 |
| `z:setHealth(h)`, `z:Kill(nil)` | Bandits BanditUpdate.lua:2386-2397 |
| `z:splatBlood(3, 0.3)`, `z:splatBloodFloorBig()` | Bandits BanditCompatibility.lua:130-132 |
| `z:playSound(String)` | Bandits ZASmack.lua:444 |
| `z:getForwardDirection()` + `getX/getY` | Bandits ZAPush.lua:36-37 |
| `z:knockDown(bool)` | DebugContextMenu.lua:668 |
| `z:getSquare()` | Bandits BanditUpdate.lua:1205 |
| `ZombRand(n)` | ISMilkAnimal.lua:25 |
| `getGameTime():getMultiplier()` | ISAnimalTracksFinder.lua:28 |
| `addSound(quelle, x, y, z, r, v)` | ISBuildAction.lua:103, AdminContextMenu.lua:260; Jar `LuaManager$GlobalObject.addSound(IsoObject,int x5)` |
| `Events.OnTick.Add`, `Events.OnGameStart.Add` | DebugContextMenu.lua:1491, ISChat.lua:1186 |
| `math.atan2`, `math.deg`, `string.format("%.2f")` | ISBaseIcon.lua:210/:212, AnimationClipViewer.lua:67 |

Kein `zombie:Hit` (Spez 3.3). Kein neuer unbelegter Aufruf.

## Toene

* Eigene: `nc_bear_sounds.txt` (Form `sounds_zombie_voice_tutorial.txt:3-11`, Kategorie `Animals` wie `sounds_animal_bull.txt`).
  Die wav liegen in `42/media/sound` (Tonschnitt), nicht in `common` wie bei Bandits. Belegt im Jar: `ZomboidFileSystem.loadMod`
  liest `getCommonDir` UND `getVersionDir` in `activeFileMap`, `FMODManager.loadSound` fragt `getAbsolutePath` = diese Karte.
* Abgespielt: Bruellen, Wusch, Doppelschlag-Knurren, Stampfen, Biss-Knurren als `PlaySound`-Ereignis im Knoten; Treffer am Ziel
  per `playSound`; Huff (Losrennen) und Knurren beim Hieb per `playBreedSound` mit eigenen Rassenschluesseln.
* `pain` und `death` spielt die Engine selbst: `buck/hitreaction/hitreaction1.xml` (PlayBreedSound pain), `falldown.xml`
  (PlayDeathSound, Jar `IsoAnimal` liest "death"). Schluessel klein (`AnimalBreed.loadSounds`/`getSound` setzen `toLowerCase`).
* **Laerm** (`NCBear_Tune("noise", radius)`), **Vorgabe aus**. Grund (Jar `IsoAnimal.respondToSound`): Tiere hoeren jeden
  WorldSound ohne Quellen-Ausnahme und rennen von `Baer minus Laermort` weg - Laerm AM Baeren gaebe einen Nullvektor. Darum
  Mitte am Hauptziel, nur beim Treffer, und im Nahkampf beendet `fleeStop` jede fremde Bewegung im naechsten Bild. Ungetestet.

## Kosten und Deckel

Baeren suchen alle 5 s (`getObjectListForLua`), hoechstens 8 gemerkt, 4 kaempfen. Zielsuche alle 0,5 s, `CanSee` nur fuer die
drei besten. Je Bild nur fuer Baeren: zwei Variablen, ein Abstand, eine Frist. Gesperrte Ziele hoechstens 32. Kampfuhr in
Animationssekunden (`getMultiplier/48`, Jar `GameTime.getTimeDeltaFromMultiplier`, `IsoGameCharacter.getAnimationTimeDelta`), je
Bild hoechstens 0,5 s. Frist je Angriff = Dauer + 1 s; drei verfallene in Folge -> laute Zeile "clips probably missing", 60 s Ruhe.
Ein Lua-Fehler im Tick wird einmal laut gemeldet und schaltet den Kampf ab (kein Stacktrace je Bild, keine Tarnkappe).

## Einzelspieler / Mehrspieler

* **Einzelspieler:** alles oben. `OnTick` wird in `OnGameStart` nur bei `not isClient() and not isServer()` angemeldet.
* **Mehrspieler: offen, nichts gebaut.** Baer-KI und `fleeTo` wirken nur auf dem Server (Spez 2), Zombie-Schaden nur beim Client
  mit Hoheit, der Server rechnet keinen Zombie (CLAUDE.md `bClient`, v3.9.42); `setVariable` am Tier auf dem Server erreicht die
  Clients nicht belegt. Bild und Ton im MP braeuchten einen eigenen Serverbefehl und eine Fundstelle, ein Tier auf dem Client
  ueber eine Netz-Id zu finden - nicht belegt. Die Knoten liegen im MP mit, die Variable setzt dort niemand. `NCBear_Fight` sagt es.
* Mit NPC Crew zusammen: nur deren ModData-Felder gelesen; ihr getauschtes `instanceof` (CLAUDE.md fuenfte Ausnahme) reicht
  Aufrufe mit "IsoZombie"/"IsoAnimal" unveraendert durch. Rehe: Variable nie gesetzt, Knoten bestehen die Bedingung nie (Spez 1.2).

## Konsole

* `NCBear_Fight()` Stand, `NCBear_Fight(true/false)` an/aus (aus loest alle Baeren).
* `NCBear_Tune()` listet alles mit Bereich, `NCBear_Tune("dmg", 2)` setzt (geklemmt, bis Neustart). Felder u. a. `radius`,
  `banditRadius`, `arrive`, `swipeReach`, `slamReach`, `maulReach`, `dmg`, `dmgMain`, `dmgSide`, `dmgSlam`, `dmgMaul`, `roarCD`,
  `slamCD`, `pause`, `reRoar`, `leash`, `fightMax`, `noise`, `knock`, `log` (0 still, 1 je Kampf/Angriff eine Zeile, 2 mehr).
* `NCBear_FightInfo()` je Baer Zustand, Ziel, Abklingzeiten, Zaehler.

## Pruefungen

* luacheck.py, scopecheck.py: 0 Fehler (beide Dateien). localcount: hoechstens 52 insgesamt (NCBearFight Hauptteil).
  luacheck_pz: 2 x W113 nur auf den eigenen Global `NCBearFight` (mit `or {}` gesetzt), sonst nichts, auch nicht mit `--unused`.
* Attrappe `_arbeit/baer_kampf/attrappe/test_fight.lua` (Lua 5.1, Engine-Nachbau mit Ereignissen, Bewegung 3,17 Kacheln/s):
  harte Regel an 21 Faellen (Spieler, Tier, Crew auch mit hostile, Neutrale mit hostileP, npcUid, NPC-Programm, Zivilist, loyal,
  Marke ohne Gehirn, tcUid, Leiche, scheintot, tot ...); Kegel links/rechts/hinten; Wahl (Bandit 3 Kacheln bevorzugt, Ebene, Sicht);
  ganzer Kampf: drei Zombies tot, Spieler/Crew/Neutrale/Zivilist/Tier daneben ohne einen Treffer; Bruellen genau einmal, nicht
  innerhalb 45 s, danach wieder; Doppelschlag hoechstens alle 10 s; Biss nur am Boden; ein Treffer je Angriff auch bei neu
  anlaufendem Knoten; fehlende Clips -> kein Schaden, laute Zeile, Ruhe; getroffen -> Kampf ab; Fluchtstopp; aus/an; im MP nichts;
  Rueckkehr; Laerm nur mit `noise`; Deckel 8/4. Gegenprobe mit vier Mutationen (Crew-Riegel weg, Biss immer, Doppeltreffer-Riegel weg,
  instanceof weg): jede faellt auf.

## Was nur Kevins Test entscheidet

Spielen die Knoten am Baeren, kommen `NCBearHit`/`NCBearDone` an (sonst Zeile `*** ... did not finish`)? Fallen Zombies nach
`setHealth` + `knockDown` sauber, auch Banditen? Klingen Toene aus `42/media/sound`? Dreht `faceThisObject` ruckartig? Haelt der
Fluchtstopp bei Schuessen? Laeuft das Anrennen mit `fleeTo` sauber zum Ziel, und die Rueckkehr? Passt "fett" (`dmg`)?

Statisch geprueft, nicht gespielt.
