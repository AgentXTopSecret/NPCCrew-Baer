# Wehren sich Zombies und Banditen gegen den Baeren? Fazit (Widerleger, 08.11.2026)

**Fuer Kevin (statisch geprueft, nicht gespielt):**
1. Weg 1 laut Code: Von selbst greift kein Zombie den Baeren an. Angestossen laufen sie hin und beissen sichtbar (Vanilla-Biss), aber im Biss-Bild loescht die Engine das Ziel, ohne Schaden zu machen. Den Schaden muessen wir also selbst rechnen, und das ist baubar.
2. Banditen sehen Tiere gar nicht. Ihre Abwehr muessten wir ganz nachbauen (Nahkampf zuerst). Nebenfund: eine verirrte Banditen-Kugel, die ein Tier trifft, geht im Einzelspieler nach Code-Lesart an DEN SPIELER. Das ist ein Bandits-Fehler, den Gegenzug baue ich nur auf dein Wort.
3. Die Probe soll zeigen, ob der Zombie hinkommt, ob er in den Zustand `attack` geht und ob der "Biss-Moment" kommt, ohne dass der Baer Leben verliert.
4. Start: Spiel neu starten (mit -debug), Baeren spawnen (Rechtsklick NC Bear > "Spawn living bear here" oder `NCBear_SpawnLive()`), einen Zombie bis 15 Kacheln daneben, selbst weiter weg vom Zombie stehen als der Baer, keine NPCs in der Naehe.
5. In der Lua-Konsole `NCBear_AttackProbe()` eingeben, dann 15 s zuschauen, die Probe hoert von selbst auf. Abbrechen mit `NCBear_AttackProbeStop()`. Danach die Zeilen `[NCBear-ATK]` an mich.
6. Die Probe macht keinen eigenen Schaden. Sie setzt nur das Ziel EINES Zombies und gibt es am Ende frei.

---

## Was ich nachgeprueft habe (eigenes javap, Jar 42.21, Klassen frisch extrahiert nach `_arbeit/baer_angriff/jar/wid/`, Auszuege `_arbeit/baer_angriff/wid/*.txt`)

### Zombie-Leser (`angriff_zombie.md`): alle Aussagen, die "geht" oder "geht nicht" entscheiden, halten

| Aussage | Beleg | Ergebnis |
|---|---|---|
| `IsoAnimal extends IsoPlayer` | javap-Kopf `IsoAnimal` | haelt |
| Kein Zombie sieht ein Tier von selbst | `IsoAnimal.updateLOS` (IsoAnimal.txt:10911) ruft weder `TestZombieSpotPlayer` noch `super.updateLOS`, reicht Zombies nur an `BaseAnimalBehavior.spotted` (Offset 242/293). Jar-weiter Byte-Scan nach Aufrufern von `IsoZombie.spotted(IsoMovingObject,Z)`: nur `IsoPlayer` (TestZombieSpotPlayer, ueber `IsoMovingObject.spotted` Offset 60), `NetworkZombieMind.doRestorePFBTarget` (Offset 68, Ziel aus einer SPIELER-Id), `SleepingEvent` (Offset 397, Spieler), `IsoZombie` selbst (Nachfassen) | haelt |
| `spottedNew` hat keine Tierfrage | `instanceof`/`tryCastTo` nur gegen `IsoGameCharacter` und `IsoPlayer` (Offset 239-277 `isGhostMode`, 831, 1804, 1866, 2189, 2328), `setTarget` 2001, `pathToCharacter` 2434/2447 | haelt |
| Ziel verfaellt ohne neues `spotted` | `IsoZombie.updateInternal` Offset 1496-1518 (`timeSinceSeenFlesh > memory` -> `setTarget(null)`), Nachfassen 957-991 nur bei `bonusSpotTime > 0` | haelt |
| `getShouldAttack` hat keine Tierfrage | Offset 0-189: `SystemDisabler`, `isReanimatedForGrappleOnly`, Ziel `isZombiesDontAttack` (42, liest `cheats`, das `IsoGameCharacter.<init>` Offset 549-557 fuer jeden anlegt; `IsoAnimal` nennt `ZombiesDontAttack` nie), Ziel am Boden -> Ziel null (71-93), Fahrzeug, Ebene 0,2 (153), `isGhostMode` nur fuer IsoPlayer (168-187) | haelt |
| Uebergang | `media/actiongroups/zombie/idle/to_attack.xml`: `bAttack`, `isFacingTarget`, `isFalse bClient` | haelt |
| **Der Biss macht am Tier 0 Schaden** | `AttackState.animEvent` Offset 46-197: `AttackCollisionCheck`, nicht `isNoTeeth`, dann `triggerPlayerReaction` (197). **`triggerPlayerReaction` Offset 20-33: `target instanceof IsoAnimal` -> `zombie.target = null; return`**, VOR `setAttackedBy` (370) und `BodyDamage.AddRandomDamageFromZombie` (381). Das ist die einzige `IsoAnimal`-Frage in AttackState | **haelt, entscheidet "Weg 1 echt: nein"** |
| Kein Netz-Trefferpaket Zombie->Tier | Jar-Liste `zombie/network/packets/hit/`: kein `ZombieHitAnimal*` | haelt |

**Was ich dazu NEU gefunden habe (beides ungespielt, beides entscheidet die Probe):**
- **Ein Tier hat `moodles = null` und `xp = null`** (`IsoGameCharacter.<init>` Offset 1213-1247: `instanceof IsoAnimal` -> nur `BodyDamage`, dann `moodles`/`xp` null). Zwei Stellen im Zombie-Weg greifen danach:
  - `spottedNew` Offset 1825/1887 `IsoPlayer.getXp().AddXP(Sneak/Lightfoot)` am Ziel. Liegt im Zweig "nicht gesehen" (endet mit `return` bei 1897) und braucht schleichen. Mit `forced = true` wird die Chance auf 1 geklemmt (Offset 1118 = 1e6, 1566-1598 `min(c,400)/400`, `max 0`, `min 1`), der Wurf gelingt immer, Sprung 1680-1682 nach 1898. **Mit Bandits' Form (`spotted(baer, true)`) also unerreichbar.** Ein Lua-`spotted(baer, false)` waere gefaehrlich.
  - `AttackState.execute` Offset 193 `target.testDefense(zombie)` -> `getMoodles().getMoodleLevel` (testDefense Offset 96-102) wirft am Tier, **aber** nur wenn am Ziel die Variable `PlayerHitReaction` gesetzt ist (execute 168-177), es von vorn steht und hoechstens 3 Zombies angreifen (testDefense 0-29). Am Tier ist sie vermutlich leer, also uebersprungen. Wirft es doch, steht in der Konsole ein State-Fehler und in der Probe `attack` ohne Biss-Moment.
- `AttackState.animEvent` Offset 113-139: steht das Ziel von vorn, zielt es nicht auf den Boden und hat es selbst eine `AttackType`-Variable, dann kehrt der Biss ohne Ziel-Loeschung zurueck. Ob der Baer beim eigenen Angriff `AttackType` setzt, ist ungeprueft (betrifft spaeter den Kampf, nicht die Probe).
- Kleinigkeit: Bandits ruft an der zitierten Stelle zusaetzlich `zombie:addAggro(bandit, 1)` und `zombie:setAttackedBy(bandit)` (BanditUpdate.lua:1832-1836). Fuer das Hinlaufen nicht noetig, die Probe laesst beides weg.

### Banditen-Leser (`angriff_bandit.md`): Stichproben halten, eine Lesart wird staerker

| Aussage | Beleg | Ergebnis |
|---|---|---|
| Bandits kennt keine Tiere | `grep -rci animal` in Bandits 42.21 `media/lua`: 0 Treffer | haelt |
| Lua-`instanceof` ist `Class.isInstance`, der Baer zaehlt als IsoPlayer | `LuaManager$GlobalObject.instof` Offset 6-36 | haelt |
| Schusslinie nimmt jede IsoZombie/IsoPlayer-Figur | `BanditUtils.lua:560-572` | haelt |
| Verfehlt -> `landed = true` | `BanditUtils.lua:382-386` | haelt |
| `IsoAnimal.isLocalPlayer()` = nicht `GameClient.client` | IsoAnimal.txt, Offset 0-11 | haelt |
| `sendClientCommand` sendet nur fuer `isLocalPlayer()` | `GlobalObject.sendClientCommand` Offset 17-28, SP-Zweig 71-75 | haelt |
| SP schickt `playerIndex`, der Server nimmt `connection.players[index]` | `SinglePlayerClient.sendClientCommand` Offset 16-30; `SinglePlayerServer.receiveClientCommand` Offset 61-66 -> `getPlayerFromConnection` 0-17 | haelt |
| Ein Tier hat `playerIndex` 0 | Schreiber von `IsoPlayer.playerIndex` (Byte-Scan): nur `GlobalObject.addPlayerToWorld` Offset 55, `setPlayerJoypad` 321, `GameServer`; `IsoPlayer.<init>`/`IsoAnimal` schreiben es nie | haelt |
| Der Handler nimmt den Spieler der Verbindung | Bandits `server/BanditServerCommands.lua:290-291` (`player:getBodyDamage()`) | haelt |
| `BulletHit` laeuft am Tier bis zum Senden | `PlayerDamageModel.lua:5` `getBodyDamage()`: ein Tier HAT eine BodyDamage (`IsoGameCharacter.<init>` 1213-1229), wirft dort also nicht. Offen bleiben `getWornItem` (:49) und die Kleidungsabwehr am Tier | **staerker belegt als im Bericht, weiter ungespielt** |
| `setHealth` verweigert kleinere Werte bei `isInvincible` | `IsoAnimal.setHealth` Offset 0-16 | haelt |

## Die Probe

`C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/lua/client/NCBearAttackProbe.lua` (neu geschrieben, CRLF wie die Nachbardateien).
Die Fassung des Zombie-Lesers hatte die Modi `hurt` und `bite`, die dem Baeren Leben abziehen. Der Auftrag erlaubt nur, was ein Zombie-Ziel ohnehin tut, deshalb sind sie raus.

- `NCBear_AttackProbe()`: nur Einzelspieler (`not isClient() and not isServer()`). Sie nimmt den naechsten lebenden `bear`/`bearstag` bis 30 Kacheln um den Spieler und den naechsten lebenden Zombie bis 15 Kacheln um den Baeren auf derselben Ebene. Dann druckt sie Klassen (`instanceof` IsoAnimal/IsoPlayer/IsoZombie), Leben, `isInvincible`, `isOnFloor`, Zustand (`getActionStateName` + `getCurrentState`), Ziel, `useless`, kriechend, `bAttack`, `isFacingTarget` und die Abstaende. Steht der Spieler naeher am Zombie als der Baer, warnt sie.
- Weg 1 im pcall, alle 0,5 s erneut: `spotted(baer, true)`, `setTarget(baer)`, ab 3 Kacheln `CanSee` -> `pathToCharacter`.
- In jedem Bild: naechster Abstand, Zustandsfolge und der **Biss-Moment** (Zustand `attack`, das Ziel Baer verschwindet im selben Bild). Eine halbe Sekunde danach prueft sie, ob Leben fehlt.
- Alle 0,5 s eine Zeile, nach 15 s eine Zusammenfassung mit Lesart. Verliert der Baer Leben, sagt sie ausdruecklich, dass das dem Code-Befund widerspricht.
- `NCBear_AttackProbeStop()` oder Ablauf: `setTarget(nil)`, wenn das Ziel noch der Baer ist, dann `Events.OnTick.Remove`. Danach bleibt nur `spottedLast` auf dem Baeren stehen (kein Lua-Setter). Ein Nachfassen ist moeglich, solange `bonusSpotTime` laeuft (`updateInternal` 957-991).
- Unbelegte Aufrufe am Tier (`spotted`, `setTarget`, `CanSee`, `pathToCharacter` sind nur mit einem IsoZombie-Banditen belegt; Java-Parameter passen) stehen je im eigenen pcall. Beim ersten Fehler kommt eine `***`-Zeile, danach ist der Teil fuer den Lauf aus.
- Pruefer: luacheck.py 0 failed, scopecheck.py 0 violations, localcount.py hoechstens 22 Locals (insgesamt 22), luacheck_pz.py 0 W113.

**Lesart der Ausgabe:** `attack` in den Zustaenden plus Biss-Momente > 0 ohne Lebensverlust = Code-Befund bestaetigt (der Mittelweg "Engine-Biss, unser Schaden" ist dann baubar). Kein `attack` und naechster Abstand > 0,72 = er kommt nicht nah genug an den Baeren heran (Kollision, `getShouldAttack`); dann bleibt nur Weg 2 (Bandits' nachgebauter Biss). `***`-Zeile oder ein Java-Fehler in der Konsole = ein Aufruf am Tier geht nicht; Konsole an Claude.
