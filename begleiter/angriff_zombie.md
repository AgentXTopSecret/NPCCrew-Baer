# Koennen Zombies den Baeren angreifen? (Zombie-Leser, 08.11.2026)

Kevins Frage: *"kannste das schonmal recherschieren ob zombies den angreifen koennen? weil sonst waere der baer naja ....
bisschen doof wenn der alles wegklatscht und die wehren sich nie"*.

**Kurz:** Von selbst nie. Mit Lua angestossen laufen sie hin und beissen sichtbar (Vanilla-Biss-Animation), aber die Engine
macht einem Tier **nie** Schaden und loescht im Biss-Moment das Ziel. Den Schaden rechnen wir also selbst, die Abwehr ist
baubar. Statisch geprueft (Jar 42.21, javap), nicht gespielt. Probe: `NCBearTest/42/media/lua/client/NCBearAttackProbe.lua`.

Quellen: `projectzomboid.jar` 42.21 (javap, Auszug `_arbeit/baer_angriff/*.txt`), Vineflower-Lesehilfe
`_arbeit/baer_spiel/dec/`, Vanilla `media/`, Bandits 42.21 + common. Vorarbeit `recherche_spiel.md` 3.2 (Zeile 176),
`../spiel/tier_spez.md` 5.3. Beides bestaetigt, hier mit mehr Fundstellen.

---

## 1. Klassenbaum

`IsoAnimal extends IsoPlayer` (javap Kopf), `IsoPlayer extends IsoLivingCharacter extends IsoGameCharacter`;
`IsoZombie extends IsoGameCharacter`. Der Konstruktor ruft `IsoPlayer.<init>(IsoCell, SurvivorDesc, int, int, int, boolean)`
(`IsoAnimal.<init>` Offset 14).

**Folge:** jede Zombie-Stelle, die `instanceof IsoPlayer` oder `Type.tryCastTo(.., IsoPlayer)` fragt, laesst ein Tier
DURCH. Ausgeschlossen werden Tiere nicht durch Typfragen in der Zombie-KI, sondern an zwei anderen Stellen (2. und 3.).
In `IsoZombie` kommt `isAnimal` nur in `updateSearchForCorpse` vor (Offset 227 `IsoDeadBody.isAnimal`, 235
`isAnimalSkeleton`), `IsoAnimal` als Klasse gar nicht (javap-grep).

## 2. Zielwahl

| Schritt | Fundstelle | Tier |
|---|---|---|
| Ein Spieler meldet sich selbst bei jedem Zombie | `IsoPlayer.updateLOS` Offset 589 und 1121 -> `TestZombieSpotPlayer` -> `zombie.spotted(this, false)` (`TestZombieSpotPlayer` Offset 57-60; auf dem Server stattdessen `ZombieControl`-Paket an den Rechner mit Hoheit, Offset 0-56) | **`IsoAnimal` ueberschreibt `updateLOS`** (`IsoAnimal.java:3607`, javap `IsoAnimal.txt:10911`), ruft kein `super.updateLOS` und kein `TestZombieSpotPlayer`; es reicht Zombies nur an das eigene Verhalten (`BaseAnimalBehavior.spotted`, Offset 242/293). **Hier faellt das Tier heraus: kein Zombie wird je vom Baeren "gesehen".** |
| `spotted(obj, forced)` | `IsoZombie.spotted` Offset 0-27: je Sandbox `spottedNew` oder `spottedOld` | nimmt `IsoMovingObject` |
| `spottedNew` | Offset 191-208 `useless` -> Ziel null; 258-283 `tryCastTo IsoPlayer` + `isGhostMode` (Tier besteht); 1042-1113 ein naeheres altes Ziel gewinnt (Manhattan); 2001 `setTarget(obj)`, 2073 `timeSinceSeenFlesh = 0`; 2279 `spottedLast = obj`; 2434/2447 `pathToCharacter(target)` | **keine Tierfrage**: ein Lua-`spotted(baer, true)` setzt das Ziel und schickt den Zombie los |
| Nachfassen | `updateInternal` Offset 957-991: `bonusSpotTime > 0` und `spottedLast` lebt -> `spotted(spottedLast, true)` | `bonusSpotTime = 720` setzt `spottedNew` nur bei `forced == false` (Offset 1909-1917) |
| Ziel verfaellt | `updateInternal` Offset 1496-1518: `timeSinceSeenFlesh > memory` -> `setTarget(null)` | ein Lua-Ziel ohne erneutes `spotted` verfaellt also |
| Geraeusch | `RespondToSound` laeuft zu einem ORT, setzt kein Ziel | ob der Baer Geraeusche macht, ungeprueft |

**`zombie:setTarget(tier)` aus Lua:** Parameter `IsoMovingObject` (`IsoZombie.setTarget` Offset 0-23: Feld schreiben +
`NetworkZombieAI.extraUpdate`), das Tier passt. Es wird **nicht sofort** geloescht. Ein `setTarget` allein schickt ihn aber
nicht los (das `pathToCharacter` steht in `spottedNew`) und verfaellt nach `memory`. Bandits' Form fuer seine Banditen ist
genau die Loesung: `zombie:spotted(bandit, true)` + `zombie:setTarget(bandit)` (BanditUpdate.lua:1832-1835) und aus der
Ferne `zombie:CanSee(bandit)` -> `zombie:pathToCharacter(bandit)` (BanditUpdate.lua:1812-1813), jedes Update erneut.
Java-Parameter: `spotted(IsoMovingObject,boolean)`, `pathToCharacter(IsoGameCharacter)`, `CanSee(IsoMovingObject)` --
das Tier hat dieselben Typen wie Bandits' Argument (Lehre v3.10.23 erfuellt), Lua-belegt ist es am Tier aber nicht.

Stoerer im Test: steht der Spieler naeher, gewinnt er (`spottedNew` 1042-1113); Bandits zieht jeden Zombie in 20 Kacheln
zu einem NPC (BanditUpdate.lua:1769-1835).

## 3. Angriff

| Schritt | Fundstelle | Tier |
|---|---|---|
| Will er beissen? | `IsoZombie.getShouldAttack` (Variable `bAttack`): Ziel nicht `isZombiesDontAttack`, nicht am Boden, gleiche Ebene (0,2), IsoPlayer-Ziel nicht `isGhostMode`, nichts dazwischen, `vectorToTarget <= 0.72` (kriechend 1,4), Offset 0-336 | **keine Tierfrage**: kommt er auf 0,72 Kachel an die Mitte heran, beisst er. Ob das bei `collisionSize = 0.42` geht, ungeprueft (die Probe misst den Abstand) |
| Uebergang | `actiongroups/zombie/idle/to_attack.xml`: `bAttack`, `isFacingTarget`, `isFalse bClient` (ebenso `lunge/to_attack.xml`) | Biss-Animation ist Vanilla: `AnimSets/zombie/attack/start.xml` (`Zombie_Bite_Start`), `success.xml` (`Zombie_Bite_Success`, Ereignis `AttackCollisionCheck` bei `m_TimePc 0.2`) |
| `AttackState.execute` | Offset 193 `target.testDefense(zombie)` (Moodles, Perks des Tiers; `IsoGameCharacter.java:13168`), 297-361 `setSlowFactor` am Ziel, 441-452 `AttackType=bite` | laeuft am Tier mit; ob `testDefense` an einem Tier wirft, ungeprueft |
| Treffer | `AttackState.animEvent` Offset 46-197: bei `AttackCollisionCheck` und nicht `isNoTeeth` -> `triggerPlayerReaction` | |
| **Hier faellt das Tier heraus** | **`AttackState.triggerPlayerReaction` Offset 20-33: `if (target instanceof IsoAnimal) { zombie.target = null; return; }`** -- VOR `setAttackedBy` (367-370) und `BodyDamage.AddRandomDamageFromZombie` (373-381) | **0 Schaden**, kein Blut, kein Ton am Tier, Ziel weg |
| Netz-Gegenstueck | `AttackNetworkState.animEvent` Offset 59-168 (fremder Rechner): `instanceof IsoPlayer` -> Biss-Ton + 3x `splatBloodFloorBig` am Ziel | ein Tier waere hier IsoPlayer; erreicht wird es aber nur, wenn das Ziel ueber das Netz als Tier ankommt (4.) |

**Was ein Tier bei Schaden tut** (gilt fuer UNSEREN Schaden): `IsoAnimal.setHealth` Offset 0-16 verweigert jeden kleineren
Wert, solange `isInvincible`; Offset 22-41 auf dem Server bei `<= 0` `sendExtraUpdateToClients`. Tod: `falldown` ->
`onground` -> `die()`, `OnCharacterDeath` (`IsoAnimal.OnDeath` 0-4; `recherche_spiel.md` 3.1). Mit `fleeZombies = false`
flieht er nicht (`BaseAnimalBehavior.spotted`, `tier_spez.md` 5.2). `IsoAnimal.hitConsequences` (Weg ueber `Hit`):
Offset 0-32 Leben `- damage * getHealthLoss(0,025)` nur ausserhalb eines MP-Clients, 136-139 `hitreact` (beim buck rund 6 s
Reaktion, `tier_spez.md` 3.3), 172-184 Stress +20..40, 187-227 Gegenangriff `goAttack(zombie)` **nur auf dem Server** und
nur mit `adef.attackBack`.

**Vanilla-Weg Zombie -> Tier: keiner.** `IsoZombie` kennt Tiere nur als Leiche; `IsoAnimal` nennt `IsoZombie` nur in
`updateLOS`, `hitConsequences` (Gegenangriff) und `BaseAnimalBehavior.spotted`/`fleeFromChr` (Flucht); Trefferpakete unter
`network/packets/hit/`: AnimalHit*, PlayerHit*, VehicleHit*, ZombieHit, ZombieHitPlayer, ZombieHitThumpable -- **kein
ZombieHitAnimal** (Jar-Liste).

## 4. Mehrspieler

- **Zombie-KI rechnet der Rechner mit Hoheit.** `spottedNew` 0-130: auf einem fremden Client nur Blickrichtung, kein Ziel;
  `to_attack.xml` `isFalse bClient`; der Server leitet das Sehen an den Besitzer weiter (`TestZombieSpotPlayer` 0-56).
  `OnZombieUpdate` laeuft auf dem dedizierten Server nie (CLAUDE.md v3.9.42).
- **Biss-Paket nur fuer Spieler:** `GameClient.sendZombieHit(IsoZombie, IsoPlayer, ..)` Offset 0-27 (Ziel lokaler Spieler,
  Zombie nicht remote), gerufen nur aus `BodyDamage.AddRandomDamageFromZombie` (Offset 1288/1567/1819), das ein Tier nie
  erreicht (3.).
- **Tierleben rechnet der Server:** `hitConsequences` 0-3 ueberspringt auf einem Client; Vanillas Serverweg
  `ClientCommands.lua:863-883` (`getAnimal(id)`, `setAttackedBy`, `setHealth(0)`), Client-Id `animal:getOnlineID()`.
- **Neu und unschoen:** das Ziel eines Zombies reist als `getOnlineID()` (`NetworkZombieAI.set` Offset 42-74) und wird beim
  Empfaenger als SPIELER-Id gelesen (`NetworkZombiePacker.applyZombie` 215-290 auf dem Server, `NetworkZombieSimulator.parseZombie`
  385-456 auf dem Client, je `IDToPlayerMap`). Ein Tier als Ziel kommt dort als nil oder als **falscher Spieler** mit
  gleicher Zahl an. Folgen ungeprueft; Bandits lebt mit demselben Fehler fuer seine Banditen-Ziele.
- **Was zu senden waere:** der Hoheits-Client des Zombies erkennt den Biss und bittet den Server
  (`sendClientCommand`, Tier-Id, Zombie, Schaden); der Server prueft Abstand und Besitz und setzt das Leben. Jeder Spieler kann
  das senden, also pruefen (CLAUDE.md: alles, was ein Client senden kann, kann ein veraenderter Client auch).

## 5. Fazit

**Weg 1 "echt" (Engine zielt und beisst mit Schaden): nein. Teilweise ja fuers Verhalten.**
- Von selbst: nie (2., `IsoAnimal.updateLOS`).
- Angestossen per `zombie:spotted(baer, true)` + `zombie:setTarget(baer)` + `zombie:pathToCharacter(baer)` (Bandits-Form):
  er laeuft hin und spielt den Vanilla-Biss -- aber im Treffer-Bild `AttackState.triggerPlayerReaction` 20-33: Ziel null,
  kein Schaden. Danach muss Lua ihn erneut hetzen.
- **Daraus der Mittelweg "Engine-Biss, unser Schaden":** Biss-Moment erkennen am Zustand `attack`
  (`getActionStateName`, Bandits-belegt BanditUpdate.lua:414) plus Ziel Baer -> nil, im selben Bild unseren Schaden setzen.
  Braucht Bandits nicht. Im MP mit dem Ziel-Problem aus 4.

**Weg 2 "nachgebaut" (Bandits' eigenes Muster fuer Zombie -> Bandit, BanditUpdate.lua:1642-1694 und 1852-1901):**
| Teil | Aufruf | Fundstelle |
|---|---|---|
| Hinlaufen | `zombie:spotted(baer, true)`, `zombie:setTarget(baer)`, `zombie:CanSee(baer)`, `zombie:pathToCharacter(baer)` | BanditUpdate.lua:1812-1813, 1832-1835 |
| In Reichweite | Abstand < 0,8, gleiche Ebene, `zombieSquare:isSomethingTo(baerSquare)` falsch, `zombie:isFacingObject(baer, 0.3)` sonst `zombie:faceThisObject(baer)` | BanditUpdate.lua:1852-1859, 1905 |
| Animation | `zombie:setBumpType("Bite")` (liegend `"BiteLow"`), Knoten `Bandits/common/media/AnimSets/zombie/bumped/zszombiebite.xml` (BumpType `Bite`, Clip Vanilla `anims_X/Zombie/Zombie_Bite.x`, `BumpAnimFinished` am Ende). **Nur mit Bandits** -- ohne Knoten friert der Zombie still ein | BanditUpdate.lua:1890-1897; Alternative ohne Bandits: der echte Vanilla-Biss aus Weg 1 |
| Treffer-Bild | 14 Bilder nach dem Ausloesen, erneut Abstand < 0,8 | BanditUpdate.lua:1657-1663 |
| Ton | `zombie:playSound("ZombieBite")` bzw. `"ZombieScratch"` | BanditUpdate.lua:1664-1668; Ton Vanilla `scripts/generated/sounds/zombies/sounds_zombie_foley.txt:210` |
| Blut | `baer:splatBlood(3, 0.3)`, `baer:splatBloodFloorBig()`, `baer:playBloodSplatterSound()` (IsoGameCharacter-Methoden) | BanditCompatibility.lua:126-133 (an einem IsoZombie) |
| Schaden | `baer:setHealth(baer:getHealth() - x)`, vorher `baer:setAttackedBy(zombie)` | Vanilla `ISKillAnimal.lua:58`, `ClientCommands.lua:881-882`, `ISAnimalUI.lua:15`; blockiert von `isInvincible` (`ISAnimalContextMenu.lua:565`) -- PLAN 7: dafuer kurz ausschalten |
| nicht empfohlen | `baer:Hit(waffe, zombie, x, false, 1, false)` (Bandits ruft es am Banditen, BanditUpdate.lua:1682): loest `hitreact` (~6 s Starre), Stress und `OnWeaponHitCharacter` aus | `IsoGameCharacter.Hit` (`IsoGameCharacter.java:5869`), `IsoAnimal.hitConsequences` |

**Empfehlung:** Weg 2 fuer NPC Crew (Bandits ist dort ohnehin Pflicht), der Mittelweg als Rueckfall fuer die Test-Mod
ohne Bandits. Beide Wege brauchen das Hinlaufen ueber `spotted`/`setTarget`, also beide das MP-Zielproblem aus 4. --
Ausweg ungeprueft: Hinlaufen ohne Ziel per Wegfindung zum Ort.

## 6. Probe

**UEBERHOLT (Widerleger, 08.11.):** die Datei ist neu geschrieben, ohne die Modi `lure`, `hurt` und `bite`. Es gibt nur noch `NCBear_AttackProbe()` (Weg 1, ein Zombie, 15 s, eine Zeile je 0,5 s, kein eigener Schaden) und `NCBear_AttackProbeStop()`. Siehe `angriff_fazit.md`. Der Text darunter beschreibt die alte Fassung.

`NCBearTest/42/media/lua/client/NCBearAttackProbe.lua`, nur Einzelspieler, nur auf Zuruf, hoechstens 30 s:
- `NCBear_AttackProbe()` -- beobachtet, ob ein Zombie den Baeren von selbst als Ziel hat (Erwartung 0).
- `NCBear_AttackProbe("lure")` -- Weg 1 ohne Schaden; Ergebnis je Zombie: naechster Abstand, Zustaende, "im Biss Ziel
  verloren", Leben vorher/nachher.
- `NCBear_AttackProbe("hurt", 0.05)` -- Mittelweg: Engine-Biss, unser Schaden.
- `NCBear_AttackProbe("bite", 0.05)` -- Weg 2, nur mit Bandits.
- `NCBear_AttackProbeStop()`.
Testaufbau: Spieler 6+ Kacheln vom Baeren, keine NPCs in 20 Kacheln. Jeder Tier-Aufruf ohne Lua-Beleg am Tier steht im
eigenen `pcall` und schaltet sich nach dem ersten Fehler ab. Geprueft: luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py (0 W113).
