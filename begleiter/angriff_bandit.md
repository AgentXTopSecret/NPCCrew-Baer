# Koennen Banditen den Baeren angreifen? (Banditen-Leser, 08.11.2026)

Kevins Frage: *"kannste das schonmal recherschieren ob zombies den angreifen koennen? weil sonst waere der baer naja ....
bisschen doof wenn der alles wegklatscht und die wehren sich nie"* -- hier die Banditen-Haelfte (Zombies:
`angriff_zombie.md`).

**Kurz:** Ein Bandit greift den Baeren **nie absichtlich** an: Bandits kennt keine Tiere (0 Treffer fuer `Animal` in
Bandits 42.21 `media/lua` und `common`). Er trifft ihn nur **zufaellig mit einer Kugel**, die an jemand anderen ging -- und
dann passiert am Baeren nichts, im Einzelspieler nach Lesart aber **beim Spieler** (Abschnitt 2.3). Abwehr ist baubar:
eigene Zielsuche plus eigene Bandits-Aufgabe mit `lock = true`, Schaden selbst. Statisch geprueft (Bandits-Lua, Jar 42.21
javap), nicht gespielt.

Quellen: Bandits 42.21 `media/lua` (Pfade unten relativ dazu), Jar `projectzomboid.jar` 42.21 (javap-Auszuege
`_arbeit/baer_angriff/*_bandit.txt`, Scan-Skript `_arbeit/baer_angriff/bandit_tools/putfield_scan.py`), NPC Crew
`42/media/lua` (nur gelesen), `../spiel/kampf_spez.md` 3.4/3.6, `recherche_spiel.md` 5, `angriff_zombie.md`.

---

## 1. Wie ein feindlicher Bandit sein Ziel waehlt

Alles in `ManageCombat` (`client/BanditUpdate.lua:1001-1605`), jedes Bild aus `GenerateTask` (:2040), gerufen aus
`OnBanditUpdate` (:2278), das auf dem Server sofort aussteigt (:2100).

| Quelle | Fundstelle | Tier? |
|---|---|---|
| **Spieler**, nur wenn `brain.hostile or brain.hostileP` | :1082-1183; Liste `BanditPlayer.GetPlayers()` (`client/BanditPlayer.lua:18-29`): Einzelspieler `IsoPlayer.getPlayers()` = das feste Feld der lokalen Spieler (Jar `IsoPlayer.getPlayers` Offset 0-13), Mehrspieler `getOnlinePlayers()` = `GameClient.getPlayers` = `IDToPlayerMap` (Jar Offset 23-29) | **nein** -- ein Tier steht in keiner der zwei Listen (nach Lesart; die Schreiber von `players[]`/`IDToPlayerMap` nicht alle verfolgt) |
| **Zombies und Banditen anderer Clans** | :1185-1305 ueber `BanditZombie.CacheLight` (`client/BanditZombie.lua:9`), gefuellt nur aus `OnZombieUpdate` (:45-90) und `getCell():getZombieList()` (:110, jede Spielminute neu, :98-173); Feind = `BanditUtils.AreEnemies` (`shared/BanditUtils.lua:781-790`) | **nein** -- nur IsoZombie |
| Nahkampf-/Schussziel | die Aufgabe traegt nur `eid = BanditUtils.GetCharacterID(ziel)` (:1324, :1336, :1359); aufgeloest in `ZASmack.lua:483`/`:615`/`:626` und `ZAShoot.lua:57`/`:122` als `BanditZombie.Cache[eid] or BanditPlayer.GetPlayerById(eid)` | **nein** |
| Freund in der Schusslinie | `IsShotClear` (:114) ist tot: Zeile 116 `if true then return true end` | -- |

**Einschleusen ohne Bandits-Dateien -- drei Wege geprueft, zwei verworfen:**

- **A. Baer in `BanditZombie.Cache`/`CacheLight` legen: verworfen.** (1) Jede Spielminute baut `flush` die Tabellen aus
  der Zombieliste neu (:98-161), der Baer faellt raus. (2) Ein Eintrag ohne Gehirn ist fuer `AreEnemies` der "zombie case"
  (`BanditUtils.lua:782-783`) -- dann greifen ihn **alle** an, auch die eigene Crew und Neutrale. (3) `GetCharacterID` gibt
  einem Tier die **Spieler-Id**: es ist IsoPlayer (`IsoAnimal extends IsoPlayer`, Vineflower `IsoAnimal.java:127`), also
  Zweig :665-675, im Einzelspieler fest `1` (:672) wie der Spieler, im Mehrspieler `getOnlineID()` des Tiers. Ein
  `Cache[1] = baer` liesse jede gegen den Spieler gerichtete Aufgabe den Baeren treffen.
- **B. `BanditPlayer.GetPlayers` erweitern: verworfen.** Dieselbe Id-Falle: `GetPlayerById(1)` (`BanditPlayer.lua:31-42`)
  liefert den ersten mit Id 1, also den Spieler; dazu `IsGhost` ueber die Spieler-Id (:9-16), `WakeEveryone` und
  `GetClosestPlayerLocation` (`BanditUtils.lua:815-874`) -- Banditen wuerden dem Baeren wie einem Spieler nachlaufen.
- **C. Eigene Zielsuche + eigene Bandits-Aufgabe: empfohlen** (Abschnitt 5). Bandits ruft jede Aufgabe ueber ihren Namen
  auf (`ProcessTask`, `BanditUpdate.lua:1961/1975/1999`: `ZombieActions[task.action].onStart/onWorking/onComplete`), NPC
  Crew baut so seit langem eigene (`ZombieActions.BNAtAnimal`, `shared/BanditsNPCActions.lua:336`). Gegen Bandits'
  Wegwischen hilft `lock = true`: `Bandit.ClearTasks` behaelt gesperrte Aufgaben (`shared/Bandit.lua:365-377`, :369-373),
  Muster NPC Crew `NPCDowned` (`shared/BanditsNPCPrograms.lua:9911`).

## 2. Wie ein Bandit Schaden macht, und was davon am Tier ankommt

### 2.1 Nahkampf (`shared/ZombieActions/ZASmack.lua`)

- Treffer-Bild: `task.time <= task.attackTime` (56), :603; Reichweite `item:getMaxRange() + 0.1` (:371-372).
- Zombie-Opfer: `dmg = getMaxDamage() * strengthBoost * 2.60` -> `victim:Hit(item, fakeZombie, dmg, false, 1, false)`,
  dann `Sync.Health` (:423-451).
- Spieler-Opfer (alles, was nicht IsoZombie ist): `PlayerDamageModel.BareHandHit`/`MeleeHit` (:452-457), Schaden
  `ZombRandFloat(min,max) * 10` auf der 0-100-Skala des Spielers (`shared/PlayerDamageModel.lua:204-206`), Faeuste 3/7
  (:155-160).
- **Am Baeren: nie**, weil er nie Ziel ist (1.).

### 2.2 Schuss (`ZAShoot.lua` -> `BanditUtils.ManageLineOfFire` -> `BanditUtils.Hit`)

- `ZAShoot.onWorking` beim Zielbild (:188-196) ruft `ManageLineOfFire` zur Zielkachel (einziger lebender Aufrufer,
  :195; :274 steht in einem Kommentarblock).
- `ManageLineOfFire` (`BanditUtils.lua:399-603`) geht die Linie ab und am Ende ein **5x5-Feld um das Ziel** (:434-443) und
  fragt je Kachel `square:getMovingObjects()` mit `instanceof(chr, "IsoZombie") or instanceof(chr, "IsoPlayer")` (:560-563).
  **Lua-`instanceof` ist `Class.isInstance`** (Jar `LuaManager$GlobalObject.instof`, `@LuaMethod(name="instanceof")`,
  Offset 6-36) -> **der Baer ist dort ein Spieler.** Jede Figur ausser dem Schuetzen geht nach `BanditUtils.Hit` (:572).
- `BanditUtils.Hit` (:251-397): Trefferwurf ueber Entfernung (:264-293). Getroffen + IsoPlayer + Schuetze `hostile/hostileP`
  -> `PlayerDamageModel.BulletHit(shooter, item, baer)` (:295-302). Getroffen + Schuetze friedlich -> nichts, `landed =
  false`, Kugel fliegt weiter. **Verfehlt -> `landed = true` (:382-386), die Kugel bleibt am Baeren**, egal wer schoss.
  Danach `victim:getHealth() <= 1` -> Bandit ruft "DEATH" (:388-390); ein Tierleben ist 0..1, das gilt also immer.
- `BulletHit` (`PlayerDamageModel.lua:4-124`): Koerperteil 5-75 Punkte (:9-27), am Ende
  `sendClientCommand(baer, "Commands", "PlayerDamage", args)` (:74/:103/:122) -> Server `BanditServer.Commands.PlayerDamage`
  (`server/BanditServerCommands.lua:290-335`): `ReduceGeneralHealth`, Wunde, Kugel, Blut, Loch -- an dem Spieler, den der
  Server zum Befehl findet.

### 2.3 Wohin der Schuss-Schaden dann geht (Jar)

| Schritt | Fundstelle | Folge |
|---|---|---|
| `sendClientCommand(spieler, ...)` sendet nur fuer `isLocalPlayer()` | `GlobalObject.sendClientCommand` Offset 17-28 | |
| `IsoAnimal.isLocalPlayer()` = `not GameClient.client` | `IsoAnimal.txt:10160`, Offset 0-11 | **Mehrspieler-Client: false -> nichts gesendet, kein Schaden.** Einzelspieler: true |
| Einzelspieler schickt den `playerIndex` des Absenders | `SinglePlayerClient.sendClientCommand` Offset 16-30 | |
| `IsoPlayer.playerIndex` schreiben nur `addPlayerToWorld` (Offset 55), `setPlayerJoypad` (321) und `GameServer` (jar-weiter putfield-Scan); `IsoAnimal` nie | `putfield_scan.py` | ein Tier hat **0** (Java-Vorgabe) |
| Server sucht `connection.players[index]` | `SinglePlayerServer.receiveClientCommand` Offset 61-66, `getPlayerFromConnection` 0-17 | Index 0 = **Spieler 1** |
| Tier selbst | eigene `BodyDamage` (`IsoGameCharacter.<init>` Offset 1213-1232), aber `BodyDamage.Update` kehrt fuer Tiere sofort zurueck (Offset 0-20); `IsoAnimal` liest `BodyDamage` nirgends (javap-grep) | **Tierleben: 0 Schaden** |

**Folge (Lesart, nicht gespielt):** im Einzelspieler bekommt der **Spieler** die Kugel, die ein feindlicher Bandit dem
Baeren -- oder jedem anderen Tier: Kuh, Huhn -- versehentlich verpasst, auch wenn der Bandit auf einen Zombie schoss und
der Spieler weit weg steht. Ungeprueft, ob `BulletHit` am Tier bis zum Senden durchlaeuft (`getBodyPartClothingDefense`,
`playerVoiceSound`, beim Kopftreffer `getWornItem` am Tier). Das ist ein Bandits-Fehler, unabhaengig vom Baeren.
Gegenmittel von aussen ohne Bandits-Datei: ein verketteter Aufsatz auf `PlayerDamageModel.BulletHit/MeleeHit/BareHandHit`,
der bei `instanceof(opfer, "IsoAnimal")` (Muster NPC Crew `client/BanditsNPCDoors.lua:446`) nichts tut -- **nicht gebaut,
braucht Kevins Wort**; vorher mit einer Sonde messen (6.).

### 2.4 Was der Baer NICHT benutzen darf: `Hit()` an einem Banditen

`OnHitZombie` (`BanditUpdate.lua:2295-2404`) ruft `BanditPlayer.CheckFriendlyFire(bandit, angreifer)` (:2356); das laesst
nur Nicht-IsoPlayer und `isNpc()` aus (`BanditPlayer.lua:104`). Der Baer ist IsoPlayer: schluege er ueber `Hit` einen
FRIEDLICHEN Banditen, wuerden alle friedlichen Zeugen in 12 Kacheln gegen den Spieler feindlich (:106-125). `kampf_spez.md`
3.3 verbietet `zombie:Hit` ohnehin, und 3.4 nimmt nur `hostile/hostileP` als Ziel -- beides bleibt richtig. (`isNpc` am
Tier ungeprueft.)

## 3. NPC Crew

- **Die Crew greift ihn nie an.** Sie kaempft ueber Bandits' `ManageCombat`: der Spieler-Block laeuft nur fuer
  `hostile/hostileP` (:1082), der Zombie-Block kennt kein Tier (1.). NPC Crew setzt keine eigene Zielwahl darueber
  (`BanditUtils.AreEnemies`-Aufsatz `shared/BanditsNPCPrograms.lua:9934-9949`: passiv, liegend, zwei Angeworbene -> nie
  Feinde). Neutrale (`hostile` falsch) ebenso.
- **Crew-Kugeln in der Linie:** `Combat.lua`-Aufsatz (`client/BanditsNPCCombat.lua:320-344`) faengt nur Companions und
  Neutrale ab, der Baer faellt durch zu Bandits: Schuetze friedlich -> kein Schaden; verfehlt -> Kugel bleibt am Baeren
  (2.2). Kleinigkeit: der Ziel-XP-Aufsatz (`client/BanditsNPCSkillsHooks.lua:1705-1707`) gibt XP schon vor der Typfrage
  (:1714-1716), also auch fuer eine Kugel ueber den Baeren -- wie heute fuer eine ueber den Spieler.
- **Tierpfleger:** schlachtet nur nach Kevins Regeln (Vorgabe aus); `Lv.SlaughterUsable` lehnt wild, angebunden und
  `isInvincible` ab (`shared/BanditsNPCLivestockSlaughter.lua:1607-1620`). Ein Baer (`wild = false`, `NCBearDefs.lua:73`)
  in einer Tierzone waere nicht ausgeschlossen -- ob er in der Schlachtliste auftaucht, ungeprueft. Spaeter: ausdruecklich
  ausnehmen.
- Fuer unsere Abwehr gilt dieselbe Freund-Feind-Regel wie in `kampf_spez.md` 3.4, nur umgedreht: angreifen duerfen nur
  `hostile or hostileP` (`Bandit.IsHostile`, `shared/Bandit.lua:600-605`), nie `loyal`, nie NPC-Crew-Marken (`recruited`,
  `npcNeutral`, Programm `NPC*`).

## 4. Mehrspieler

- **Banditen-Kampf rechnet jeder Client, der den Banditen geladen hat**: `OnBanditUpdate` nur `isServer()`-Riegel (:2100),
  `ManageCombat`, `ZASmack`, `ZAShoot` ohne `IsController` (grep: `IsController` nur in Move/GoTo/Unload/... ). Zombie-Leben:
  lokal + `Sync.Health` -> Server-Rundruf (`server/BanditServerSync.lua:4-5`) -> Clients **senken** nur
  (`client/BanditClientCommands.lua:28-40`). Spieler-Schaden: nur der Rechner des Opfers sendet (`isLocalPlayer`-Riegel,
  2.3). Der dedizierte Server rechnet keinen Banditen (`OnZombieUpdate` feuert dort nie, CLAUDE.md v3.9.42).
- **Tierleben rechnet der Server**: er schickt es im `AnimalPacket` (`NetworkPlayerAI.set` Offset 790-801, Leben x 100 als
  Byte), der Client setzt es (`NetworkPlayerAI.parse` Offset 1173-1183, `setHealth`) -- ein Client-`setHealth` haelt nur
  bis zum naechsten Paket (`recherche_spiel.md` 5). Waffenschaden am Tier nur ausserhalb eines Clients
  (`IsoAnimal.hitConsequences` Offset 0).
- **Also fuer die Abwehr:** genau ein Rechner meldet den Treffer -- der mit Hoheit ueber den Banditen
  (`not bandit:getVariableBoolean("bClient")`, NPC Crew `BanditsNPC.HasAuthority`, CLAUDE.md v3.9.2) -- per
  `sendClientCommand` mit Tier-Id und Bandit-Id; der Server prueft Abstand (eigene Zombieliste, Bandits
  `server/BanditServerZombie.lua:15`), Feindschaft aus dem Cluster (`GetBanditClusterData(id)[id]`, nie
  `BanditBrain.Get` auf dem Server, CLAUDE.md v3.7.44) und eine Bremse je Bandit, dann setzt er das Leben. Jeder Client kann
  das senden, also pruefen.

## 5. Fazit

**"Echt" (Bandits zielt und trifft mit Schaden): nein.**
- Bandits sieht Tiere nie (1.). Der einzige Weg zum Baeren ist eine verirrte Kugel; die macht am Baeren 0 Schaden, haelt
  aber die Kugel auf, und im Einzelspieler landet der Schaden nach Lesart beim Spieler (2.3).

**"Nachgebaut": ja, ohne Bandits-Datei.** Vorschlag (nichts gebaut):

| Teil | Aufruf | Fundstelle |
|---|---|---|
| Wer greift an | `BanditZombie.CacheLightB` (geladene Banditen), Objekt per `BanditZombie.GetInstanceById(id)` (prueft Identitaet), Gehirn `light.brain`; nur `hostile or hostileP`, nicht `loyal`, keine NPC-Crew-Marke | `client/BanditZombie.lua:16/:81/:176-186`; `Bandit.lua:600-605`; `kampf_spez.md` 3.4 |
| Darf er gerade | nicht kriechend, nicht schlafend; keine Aufgabe `NCBearSmack`; Aktionszustand nicht getup/staggerback | `BanditUpdate.lua:1003-1004`; `ZASmack.lua:607-610`; `Bandit.HasTaskType` (`Bandit.lua:327`) |
| Vorrang | Baer naeher als jeder Zombie in `CacheLightZ` (selbst gerechnet; Bandits' eigenes Ziel ist lokal und nicht lesbar) | `BanditZombie.lua:12` |
| Sicht, Wand | gleiche Ebene (< 0,5), `bandit:CanSee(baer)`, `banditSquare:isSomethingTo(baerSquare)` falsch | `BanditUpdate.lua:1087/:1094/:1096` (am Spieler) |
| Drehen | `bandit:isFacingObject(baer, 0.5)`, sonst `bandit:faceThisObject(baer)` | :1354/:1363 |
| Aufgabe | `Bandit.ClearTasks(bandit)`, `Bandit.AddTask(bandit, {action = "NCBearSmack", anim = <Angriff>, time = 65, lock = true, ...})`, eigene `ZombieActions.NCBearSmack` mit `onStart/onWorking` | `Bandit.lua:365/:282`; `BanditUpdate.lua:1961/:1975`; Muster `BanditsNPCActions.lua:336` |
| Animation, Ton | Name je Waffenart wie Bandits (`WeaponType.getWeaponType(BanditCompatibility.InstanceItem(brain.weapons.melee))` -> `Attack2H1..4`, `Attack1H1..5`, `AttackBareHands1..6`, `AttackKnife`, ...), `getSwingSound()`, `VoiceMale/FemaleMeleeAttack`; Knoten liegen in Bandits `common` | `ZASmack.lua:488-583` |
| Treffer-Bild | `task.time <= 56` (wie `attackTime`), Abstand < `getMaxRange() + 0.1` | `ZASmack.lua:493/:603`, :371-372 |
| Schaden | Einzelspieler `baer:setHealth(h - d)` (blockiert bei `isInvincible`), Blut wie `Splash`; Hoehe wie beim Spieler, in Prozent: Nahkampf `ZombRandFloat(min,max) * 10 / 100`, Faeuste 0,03/0,07 -- dann mit der Baeren-Zaehigkeit teilen (Zahlen zum Einstellen) | `angriff_zombie.md` 5 (Vanilla `ISKillAnimal.lua:58`); `PlayerDamageModel.lua:155-160/:204-206`; `BanditCompatibility.lua:126-133` |
| Mehrspieler | nur der Hoheits-Rechner meldet, der Server setzt | 4. |

Schuss nachgebaut ist teurer (eigene Zielbild-Logik, `brain.weapons.primary/secondary.bulletsLeft` herunterzaehlen,
`BanditCompatibility.StartMuzzleFlash`, Trefferkurve abschreiben, `ZAShoot.lua:32-196`, `BanditUtils.lua:264-293`).
Vorschlag: erst Nahkampf; Schuetzen laufen auf Nahkampfweite heran oder "schiessen" mit Ton + Wurf ohne Kugelweg.

**Grenzen:** `lock = true` laesst unseren Hieb Bandits' eigene Aufgaben ueberholen (Bandits haengt seine hinten an,
`BanditUpdate.lua:2086-2091`); deshalb nur kurze Aufgaben (Zeit begrenzt) und Vorrang nur, wenn der Baer naeher ist.
Ungeprueft im Spiel: ob die Angriffsposen bei einem Ziel ohne Bandits' eigenes `enemyCharacter` sauber enden
(`BumpAnimFinished`), ob `CanSee`/`isFacingObject` am Tier wie am Spieler antworten.

## 6. Sonde (Vorschlag, nicht gebaut)

Die Probe-Datei `NCBearTest/42/media/lua/client/NCBearAttackProbe.lua` gehoert dem Zombie-Leser und deckt Banditen nicht
ab. Vorschlag fuer eine Erweiterung, Einzelspieler, auf Zuruf, 30 s:
- **`watch-bandit`:** `PlayerDamageModel.BulletHit/MeleeHit/BareHandHit` fuer die Laufzeit verketten (danach zurueck), je
  Aufruf eine Zeile: Opfer IsoAnimal ja/nein, Schuetze, Spielerleben vorher/nachher (eine Sekunde spaeter). Mit `block`
  gibt der Aufsatz bei einem Tier sofort zurueck. Entscheidet 2.3 in einem Lauf.
- Aufbau: Baer zwischen Spieler und einem feindlichen Banditen oder neben einem Zombie, auf den ein feindlicher Bandit
  schiesst; Spieler mit voller Gesundheit, Wegwerf-Spielstand.
