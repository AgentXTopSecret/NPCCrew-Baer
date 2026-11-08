# Baer: Spez fuer den Lauf baer-anim (Lua und Engine)

Stand 08.11.2026, PZ 42.21 (`projectzomboid.jar` 28.09.2026), Bandits 42.21. Spez-Leser. Nur gelesen: Vanilla-Lua und
-XML, Bandits, Jar mit `javap -c -p` (Auszug `_arbeit/baer_anim/jar/`, Texte `_arbeit/baer_anim/jt/`), Clipdateien
`media/anims_X/Zombie/*.x` (Parser `_arbeit/baer_anim/xroot2.py`), Kevins Konsole vom 08.11. nachts, Spielstand
`Saves/Apocalypse/2026-11-06_23-55-15/map_sand.bin` (nur gelesen). **Statisch geprueft, nicht gespielt.**

Bau-Stand: `NCBearTest/42` vollstaendig nach `_arbeit/baer_anim/mod/42` kopiert (`diff -rq` gleich). An `NCBearTest`
danach nichts geaendert.

Schreibweise: `Klasse.methode Offset` = Jar; `Datei.lua:Zeile` = Vanilla `media/lua`, sonst mit Mod genannt.
1 Modelleinheit (E) Clipweg = rund 1,6 Kacheln (MotionScale 1,6, `tier_spez.md` 2.8; fuer `Bip01` als Bewegungsknochen
nicht eigens gemessen).

---

## 0. Ergebnis in zehn Saetzen

1. **"Sofort tot" kommt vom Debug-Spawn, nicht von der Sandbox:** der Horde-Spawner setzt jedem Zombie genau den
   Schieberwert als Leben (Vorgabe **1,0**), der Hieb macht 1,3 und der Doppelschlag 1,0. 22 von 22 Doppelschlag-Treffern
   toeteten (Abschnitt 1).
2. **Kevins Zaehigkeit ist "Zufall"** (`ZombieLore.Toughness = 4`): echte Zombies haben 0,5 bis 3,8 Leben.
3. **Knockback geht belegt ueber die Engine:** nach `knockDown` noch `setPlayerAttackPosition(z:testDotSide(baer))`
   (Bandits `ZAPush.lua:42`). Steht der Baer vorn, spielt der Zombie `Zombie_StaggerBackFall`: er taumelt **rund 1,0 E
   (etwa 1,6 Kacheln) zurueck** und faellt. Heute faellt er nur auf der Stelle (`Zombie_Death`, 0,19 E).
4. **Wand und Kante bewacht die Engine wie beim Schubs eines Spielers.** Dazu prueft Lua vorher zwei Kacheln hinter dem
   Zombie (Wand, Fenster, Tuer, Boden, Wasser, Ebene); ist dort etwas, faellt er auf der Stelle.
5. **Ragdoll geht nicht:** `setUsePhysicHitReaction` hat keinen Lua-Aufruf, die Engine setzt es nur bei
   **Fernkampf**-Treffern, und im Mehrspieler ist Ragdoll ganz aus (`IsoGameCharacter.canRagdoll` 0-13).
6. **Auch toedliche Treffer koennen fliegen:** in `idle`, `walktoward`, `pathfind`, `attack` und `lunge` hat der
   Taumel-Uebergang keinen Riegel auf `bDead`. Laut XML taumelt der Tote, faellt und wird erst am Boden zur Leiche.
   Das ist ungespielt und hat einen eigenen Schalter.
7. **Schaden neu:** Hieb 1,0, Biss stehend 1,2, Biss am Boden 1,8, Doppelschlag 0,9, Nebenziel 0,6. Ein normaler Zombie
   braucht dann 2-3 Treffer, ein zaeher 3-4. `NCBear_Tune` bleibt.
8. **Angriffe wechseln nach Gewichten,** nie zweimal derselbe Clip hintereinander. Aufrichten mit Bruellen gibt es nur
   noch zu Kampfbeginn, mit 50 % und hoechstens alle 120 s.
9. **Sitzen und Fressen bekommen vier Knoten nach dem Muster der Kampfknoten.** Es gibt einen einzigen Schreiber von
   `NCBearAct` (`NCBearFight.lua`). Die Konsolenbefehle stehen nur in `client/NCBearBench.lua`. Kampf geht vor:
   erst Aufstehen, dann Kampf.
10. **Keine neue Engine-Methode ohne Fundstelle:** neu sind nur Bandits- und Vanilla-belegte Aufrufe (Tabelle 8).

---

## 1. Kevins Test (console.txt, 08.11. nachts, 81 Zeilen `[NCBear]`)

| Angriff | Angriffe | Treffer | getoetet |
|---|---|---|---|
| swipeL | 25 | 34 | 25 |
| swipeR | 27 | 40 | 25 |
| slam | 7 | 22 | **22** |
| maul | 6 | 6 | 6 |

Keine Zeile `***` (kein Clip fehlte, kein Angriff verfiel). Vor den Kaempfen stehen Zeilen
`Spawning new ... Zed ... at Lua(Vanilla).onSpawn` (f:6924, 10891, 27721 ...): **die Gegner kamen aus dem Debug-Horde-Spawner.**

- `ISSpawnHordeUI.lua:110-111`: Schieber "Health" 0..2, Vorgabe **1,0**. `:276` reicht den Wert an `addZombiesInOutfit`.
- Jar `LuaManager$GlobalObject.addZombiesInOutfit` Offset 380-410: erst `DoZombieStats`, **danach `setHealth(health)`**.
  Jeder gespawnte Zombie hat also genau 1,0.
- `damage()` rechnet `h <= 0` als tot. Damit toetet der Hieb (1,3) jeden gespawnten Zombie, der Doppelschlag (1,0) auch.
- Der erste Kampf (f:1, vor jedem Spawn, also ein echter Zombie) brauchte zwei Hiebe: `swipeR: 1 hit, 0 killed`,
  dann `swipeL: 1 hit, 1 killed`.

**Fuer Kevins naechsten Test:** den Schieber vor dem Spawnen auf **2,0** stellen (Hoechstwert, entspricht einem normalen
Zombie). Fuer zaehe Zombies gibt es `NCBear_ZHealth(h, r)` in der Testdatei (Abschnitt 6.6).

---

## 2. (A) Knockback

### 2.1 Was heute passiert

`damage()` ruft `z:knockDown(behind)` (`DebugContextMenu.lua:668`). Jar `IsoZombie.knockDown` 0-43: `setKnockedDown(true)`,
`setStaggerBack(true)`, `setHitReaction("")`, `setPlayerAttackPosition(behind ? "BEHIND" : null)`, `setHitForce(1)`,
`reportEvent("wasHit")`.

- Die XML fragt `playerAttackPosition == FRONT` bzw. `== BACK`. **"BEHIND" kommt in keiner Bedingung vor und `null` auch
  nicht.** Also greift `to_falldown` (Abschnitt 2.2), Knoten `falldown/default.xml` = `Zombie_Death`: er faellt **0,19 E
  nach hinten**, rund 0,3 Kacheln. Das hat Kevin als "umwerfen hat geklappt" gesehen.
- **Fehler nebenbei:** welcher Fallclip spielt, entscheidet die Variable `frombehind` = `isHitFromBehind()` (Jar
  `IsoGameCharacter`, BootstrapMethods 37). `knockDown` setzt sie **nicht**, und unser Code ruft `setHitFromBehind` nie.
  Ein Zombie, der von hinten getroffen wird, faellt deshalb rueckwaerts **auf den Baeren zu**.

### 2.2 Wer gewinnt (Jar `ActionState.lambda$static$0`)

Die Uebergaenge werden sortiert, zuerst nach `conditionPriority` absteigend, bei Gleichstand nach Zahl der Bedingungen
absteigend (stabil, Dateireihenfolge). Es gewinnt der erste, dessen Bedingungen alle zutreffen. Gezaehlt in
`actiongroups/zombie/idle/`; `walktoward`, `pathfind`, `attack` und `lunge` haben dieselben fuenf Dateien und Zahlen,
`walktoward` dazu `to_falldown-ragdoll` (canRagdoll, bDead: 2 Bedingungen):

| Uebergang | Bedingungen | Zahl | fuer uns |
|---|---|---|---|
| to_staggerback-knockeddown-ragdoll | bKnockedDown, !bOnFloor, !hashitreaction, Lage BACK oder FRONT, usePhysicHitReaction | 5 | nie (2.5) |
| to_staggerback-knockeddown-fromBehind | bKnockedDown, !bOnFloor, !hashitreaction, Lage **BACK** | 4 | nie: `testDotSide` liefert nie "BACK" |
| **to_staggerback-knockeddown** | bKnockedDown, !bOnFloor, !hashitreaction, Lage **FRONT** | 4 | **der Knockback** |
| to_falldown (3 Uebergaenge) | ...; bKnockedDown, !bOnFloor, !hashitreaction; bDead, !bOnFloor | 3 / 3 / 2 | Fall auf der Stelle |
| to_hitreaction | hashitreaction, ... | 2 | - |
| to_staggerback | bStaggerBack | 1 | verliert immer gegen die oberen |

`testDotSide` (Jar `IsoGameCharacter.testDotSideEnum` 0-112): FRONT bei Skalarprodukt Blick zum Angreifer > 0,7
(Angreifer innerhalb rund 45 Grad vor ihm), BEHIND bei < -0,5, sonst LEFT oder RIGHT. Die Variable `playerattackposition`
liest `IsoZombie.getPlayerAttackPosition` (Feld, String).

Aus `staggerback-knockeddown` gibt es nur `to_onground` (`ActiveAnimFinishing`), `to_falling` und `to_vehicleCollision`.
Die KI ist `StaggerBackState` (`IsoZombie` registerAIState Offset 362-368). Ihr `execute` ruft
`AnimationPlayer.setTargetToAngle()`: der Clip folgt dem Blick des Zombies, und die Flugrichtung ist sein **eigenes Hinten**.

### 2.3 Clips mit Weg (`media/anims_X/Zombie`, Bewegungsknochen laut Knoten)

| Knoten (AnimSets/zombie) | Clip | Bewegungsknochen | Dauer (x 1/SpeedScale) | Weg | Kacheln (x 1,6) |
|---|---|---|---|---|---|
| staggerback-knockeddown/staggerAndFall | Zombie_StaggerBackFall | Bip01 | 1,67 s / 0,8 = 2,08 s | **1,04 E zurueck**, faellt ab 50 % (SetOnFloor), Aufprall-Ton 58 % | **rund 1,7** |
| falldown/default (frombehind = false) | Zombie_Death | Bip01 | 1,10 / 0,8 = 1,38 s | 0,19 E zurueck | rund 0,3 |
| falldown/frombehind (frombehind = true) | Zombie_DeathBehind | Bip01 | 0,97 / 0,8 = 1,21 s | 0,59 E **vor** (vom Baeren weg, der hinten steht) | rund 0,9 |
| staggerback-knockeddown-fromBehind | Zombie_PushedFwdOver_FromBehind | Bip01 | 0,63 / 0,8 s | 0,65 E vor | nie erreicht (BACK) |
| staggerback/fromFront (nur Taumeln) | Zombie_ShoveStagger_2m | Translation_Data | 2,0 s | 0,79 E zurueck | kein Fall |

Vorzeichen geprueft: `Zombie_DeathBehind` (von hinten getroffen) laeuft +y, `Zombie_StaggerBackFall` -y, der Gang
laeuft auf `Translation_Data` -z (vorn). Bewegt wird ueber `IsoGameCharacter.doDeferredMovement` -> `moveUnmodded`
(Offset 584-631), also mit der normalen Kollision: derselbe Weg wie bei jedem Schubs eines Spielers.

### 2.4 Was Bandits setzt

- **Schubs/Tritt** (`ZAPush.lua:30-48`, Opfer IsoZombie): `setHitFromBehind(behind)` (:41), `setPlayerAttackPosition(
  zombie:testDotSide(attacker))` (:42), `setHitForce(1)` (:43), `setKnockedDown(true)` (:45); `setStaggerBack` ist
  auskommentiert. **Steht der Bandit vorn, ist das genau der Knockback aus 2.2** (laut XML; dass Bandits' Tritte im Spiel so
  fliegen, ist ungeprueft).
- **Hieb** (`ZASmack.lua:419-443`): `setHitFromBehind(attacker:isBehind(victim))`, `setAttackedBy`,
  `setPlayerAttackPosition(testDotSide)`, dann `victim:Hit(item, fakeZombie, ...)` mit dem Kommentar "no-ragdoll hit".
  Der Ragdoll-Treffer mit Attrappen-Pistole steht nur **auskommentiert** (:439) und ist kein Beleg.
- **Schuss** (`BanditUtils.lua:340-371`): dasselbe, aber `Hit` mit einer Schusswaffe. Nur dort kann die Engine Ragdoll
  waehlen (2.5).

### 2.5 Ragdoll: nein

- Uebergaenge `*-ragdoll` verlangen `usePhysicHitReaction` und `canRagdoll`, `to_falldown-ragdoll` (staggerback) dazu
  `isRagdollFall`.
- `canRagdoll` (Jar `IsoGameCharacter.canRagdoll` 0-102): falsch auf einem MP-Client und auf dem Server; sonst nur mit
  Spieler-Option `getOptionUsePhysicsHitReaction` (Optionen, `MainOptions.lua:732-741`), freiem Ragdoll-Platz,
  passender Kleidung und passendem Zustand.
- `setUsePhysicHitReaction`: **null Lua-Aufrufe** in Vanilla und Bandits (grep). Java setzt es in
  `CombatManager.setUsePhysicHitReaction` 0-41 nur bei `HandWeapon.isRanged()`, in `processInstantExplosion` und beim
  Spawnen (`addZombiesInOutfit` 459-473). Erreichbar waere es nur ueber `zombie:Hit` mit einer Schusswaffe: das ist der
  Schadensweg, den die Kampf-Spez 3.3 verworfen hat, mit einem Tier als Angreifer (andere Typen als Bandits' IsoZombie)
  und nur bei eingeschalteter Spieler-Option.
- `setRagdollFall` setzt nur `RagdollController` (Jar).

**Urteil: kein Ragdoll.** Nebenfall: hat ein Spieler den Zombie vorher mit Physik-Option angeschossen, kann das Feld noch
gesetzt sein. Dann faellt er als Ragdoll, ebenfalls nach hinten. Harmlos.

### 2.6 Empfehlung Weg 1 (Engine), je Treffer mit Umwerfen

Nur wenn er steht (`not lying(z)`), Einzelspieler, in dieser Reihenfolge:

```lua
-- Seite aus Sicht des Zombies (Form Bandits ZAPush.lua:32-39, wie heute in damage())
local behind = ...                                    -- Skalarprodukt Blick des Zombies / Richtung Baer -> Zombie > 0.5
local side = z:testDotSide(B.a)                       -- Bandits ZAPush.lua:42 (Arg IsoMovingObject, Rueckgabe String)
local mode = F.KnockMode(B, z, side, act)             -- "back", "down" oder "none", Regeln unten
if mode ~= "none" then
  if mode == "back" and side ~= "FRONT" and side ~= "BEHIND" then
    z:faceLocationF(B.a:getX(), B.a:getY())           -- Bandits ZAAim.lua:12 (IsoZombie, float, float); nie bei Abstand 0
    side = "FRONT"                                    -- faceLocationF setzt die Richtung sofort (Jar 51-58 setForwardDirection)
  end
  z:setHitFromBehind(behind and mode ~= "back")       -- Bandits ZAPush.lua:41; waehlt falldown/frombehind
  z:knockDown(behind)                                 -- DebugContextMenu.lua:668 (schreibt BEHIND/nil in die Lage)
  if mode == "back" and side == "FRONT" then
    z:setPlayerAttackPosition(z:testDotSide(B.a))     -- Bandits ZAPush.lua:42; MUSS nach knockDown stehen
  end
end
```

`KnockMode` je Angriff (Vorschlag):

| Angriff | Hauptziel | Nebenziele |
|---|---|---|
| Hieb L/R | back | back |
| Doppelschlag | back | back |
| Biss stehend | down (Fall auf der Stelle: er zieht, statt zu stossen) | - |
| Biss am Boden | none | - |

`back` wird zu `down`, wenn (a) der Zombie hinter sich hat (`side == "BEHIND"`), dann faellt er mit `frombehind` nach vorn,
also vom Baeren weg, rund 0,9 Kacheln, oder (b) die Vorpruefung 2.7 scheitert. Schalter `NCBear_Tune("knockBack", 0/1)`,
Vorgabe 1.

Die 45-120 Grad Drehung beim Treffer sieht man vermutlich als Ruck (der Clip blendet 0,4 s). Ob das stoert, entscheidet
Kevins Test. Ein Zombie von hinten wird absichtlich **nicht** um 180 Grad gedreht.

### 2.7 Vorpruefung "ist hinter ihm frei?" (nur bei `back`, je Treffer, hoechstens 3 Kacheln)

Richtung r = vom Baeren zum Zombie (nach dem Drehen ist das sein Hinten). Pruefpunkte p1 = Zombie + 0,9 r und
p2 = Zombie + 1,8 r. `back` nur, wenn fuer die Kette `zsq -> sq(p1) -> sq(p2)` alles gilt:

| Pruefung | Aufruf | Fundstelle |
|---|---|---|
| Kachel da, gleiche Ebene | `getCell():getGridSquare(x, y, z)` mit `floor(z:getZ())` | `DebugContextMenu.lua:1436` |
| Boden (keine Ebenenkante, kein Loch) | `sq:TreatAsSolidFloor()` | `DebugContextMenu.lua:641` |
| kein Wasser | `sq:getFloor()` nil oder `not floor:hasProperty(IsoFlagType.water)` | `ISWorldObjectContextMenu.lua:686-688` |
| keine Wand, keine geschlossene Tuer, keine Treppenkante | `not a:isBlockedTo(b)` (je Paar aufeinander folgender Kacheln) | `ISInventoryTransferAction.lua:598` |
| kein Fenster | `not a:isWindowTo(b)` | `ISInventoryTransferAction.lua:598` |
| keine Kiste, kein Moebel | `sq:isFree(false)` | `ISFarmingMenu.lua:463`, `ISWorldObjectContextMenu.lua:2199` |

Faellt eine Kachel zweimal hintereinander an (p1 und p2 auf derselben Kachel), wird sie nur einmal geprueft. Zaeune
sperren ueber `isBlockedTo` (isWallTo, Jar 0-40), das ist gewollt. Scheitert die Pruefung, wird `back` zu `down`, er
faellt also auf der Stelle.

### 2.8 Rueckfall: eigenes Zurueckschieben (nur falls Weg 1 im Spiel nicht greift)

Nur bauen, wenn Kevins Test zeigt, dass der Zombie trotz FRONT auf der Stelle faellt. Dann sagt die Zeile
`[NCBear] knock: back ... state <name>` den Zustand eines Bildes nach dem Treffer. Form Bandits `ZASmack.lua:590-596`
(`bandit:setX(newx)`, `setY`, kleiner Schritt je Bild am IsoZombie) und `ZAMove.lua:11-19` (Schritt 0,05):

- Liste `F.pushes` mit Deckel 8 Eintraegen: `{ z, dx, dy, left, t0 }`, `left` = `NCBear_Tune("knockPush", 0..2)`,
  Vorgabe **0** (aus).
- Je Bild: `step = min(left, 0.05)`. Der Zielpunkt ist neue x/y. Wechselt die Kachel, gelten dieselben Pruefungen wie 2.7
  fuer das Paar alt -> neu. Scheitert eine: Eintrag weg. Sonst `z:setX(nx)`, `z:setY(ny)` und `left = left - step`.
- Ende: `left <= 0`, nach 0,6 s Kampfuhr, `z:getCurrentSquare() == nil` (entfernt oder zur Leiche geworden, Jar
  `IsoMovingObject.removeFromSquare`) oder `z:getZ()` hat die Ebene gewechselt.
- Nie im Mehrspieler, nie fuer Liegende ausser in diesem Fall, nie mehr als 0,05 Kacheln je Bild.

### 2.9 Tote fliegen auch (Schalter `knockKill`, Vorgabe 1)

Heute toetet `damage()` mit `Kill(nil)` ohne Umwerfen, also `to_falldown` (bDead, 2 Bedingungen) und `Zombie_Death` auf
der Stelle. Wird **vor** `Kill(nil)` dasselbe wie in 2.6 gesetzt (Modus back, Vorpruefung bestanden), gewinnt
`to_staggerback-knockeddown`: 4 Bedingungen, in idle/walktoward/pathfind/attack/lunge **ohne** `isFalse bDead`, gegen 2.
Die Leiche entsteht erst in `ZombieOnGroundState.enter` 22-53 (`isDead -> die()`); `Kill` setzt nur Leben 0 und ruft
`onKilled` (Jar `IsoGameCharacter.Kill` 0-53, `IsoZombie.onKilled` ohne Aenderung an knockedDown oder der Lage).
**Ungespielt:** ob die Leiche sauber am Ende des Fluges liegt. Bei `knockKill 0` stirbt er wie heute auf der Stelle.

---

## 3. (B) Schaden

### 3.1 Zombie-Leben aus dem Jar (`IsoZombie.resetForReuse` 316-443, bei jedem Neubau und jeder Wiederverwendung)

| `ZombieLore.Toughness` | Wert | Leben |
|---|---|---|
| Zaeh | 1 | 3,5 + Rand(0..0,3) = 3,5-3,8 |
| Normal | 2 | 1,8-2,1 |
| Zerbrechlich | 3 | 0,5-0,8 |
| **Zufall (Kevin)** | **4** | Rand(0,5..3,5) + Rand(0..0,3) = 0,5-3,8 |

`DoZombieStats` setzt kein Leben. Debug-Spawn: Schieberwert (Abschnitt 1). Kevins Spielstand: `ZombieLore.Toughness = 4`,
`Strength = 2`, `Speed = 4`, `ZombieHealthImpact = false` (map_sand.bin, gelesen, nicht geaendert).
Banditen: 1,0..2,6, Vorgabe 1,8 (`BanditServerSpawner.lua:343-344`, Kampf-Spez 5.1).

### 3.2 Vorgabe (alles mal `dmg` = 1,0)

| Feld | heute | neu | Grund |
|---|---|---|---|
| dmgMain (Hieb, Hauptziel) | 1,3 | **1,0** | normal: 2 Hiebe bis 2,0 Leben, 3 darueber |
| dmgSide (Hieb/Slam Nebenziel) | 0,8 | **0,6** | Nebenziel stirbt nicht mit dem Hauptziel |
| dmgSlam (Doppelschlag) | 1,0 | **0,9** | Flaeche, darf nicht staerker als der Hieb sein |
| dmgBite (Biss stehend, neu) | - | **1,2** | Hauptwaffe des Baeren laut Kevin/Referenz |
| dmgMaul (Biss am Boden) | 2,5 | **1,8** | erledigt einen angeschlagenen normalen Zombie, keinen zaehen |

Gerechnet (h <= 0 = tot):

| Zombie | typische Folge | Treffer |
|---|---|---|
| normal 1,8-2,0 | Hieb + Hieb = 2,0 | 2 |
| normal 2,0-2,1 | Hieb + Hieb + x, oder Hieb + Biss = 2,2 | 2-3 |
| normal, liegt nach dem 1. Hieb | Hieb + Bodenbiss = 2,8 | 2 |
| zaeh 3,5-3,8 | Hieb, Biss, Hieb = 3,2, dann der 4. | 4 |
| zaeh, mit Bodenbiss | Hieb + Bodenbiss + Hieb = 3,8 | 3 |
| Debug-Spawn 1,0 | Hieb 1,0 | **1** (Schieber auf 2,0 stellen) |

Ein normaler Zombie braucht also 2-3 Treffer, ein zaeher 3-4. `NCBear_Tune` bleibt, `F.RANGE` bekommt `dmgBite {0, 20}`.
Fester Eintrag erst nach Kevins Wahl.

---

## 4. (C) Angriffs-Wechsel

### 4.1 Wahl je Angriff (`F.ChooseAct`)

Erst Blick auf das Ziel (wie heute `face` vor der Wahl). Kandidaten mit Gewicht, dann **der zuletzt gespielte Clip
`B.lastAct` raus**, dann gewichteter Zufall (`ZombRand(summe)`, `ISMilkAnimal.lua:25`):

| Kandidat | Bedingung | Gewicht (Tune) |
|---|---|---|
| maul | Ziel liegt und `d <= maulReach * s`, Kegel +-30 | `wMaul` 70 |
| bite | Ziel steht, `d <= biteReach * s`, Kegel `biteHalf` +-30 | `wBite` 30 |
| swipeL | immer | `wSwipe` 25, **+15**, wenn das Ziel links ist (`F.AngleLeft > 12`) |
| swipeR | immer | `wSwipe` 25, **+15**, wenn das Ziel rechts ist (`< -12`) |
| slam | `slamCD` frei und **mindestens ein weiterer Gegner** vorn in `slamReach * s` (2+ vorn insgesamt; heute verlangt der Code 2 weitere) | `wSlam` 40 |

- Hieb L und Hieb R zaehlen als zwei Clips: L, R, L, R ist erlaubt, L, L nicht.
- Liegt das Ziel und war der letzte Clip `maul`, kommt ein Hieb (der Kegel trifft auch Liegende).
- Bleibt nach dem Entfernen nichts uebrig (geht nicht, Hiebe gibt es immer), dann wie heute im Wechsel.

### 4.2 Aufrichten und Bruellen

- Nur in `startFight`, nie mitten im Kampf: der Zweig `reRoar` faellt weg, Vorgabe 0.
- Nur wenn `clock - lastRoar >= roarCD` (Vorgabe **120 s**, heute 45), `ZombRand(100) < rearChance` (Vorgabe **50**) und das
  Ziel weiter als **2,5 Kacheln** weg ist. Steht der Zombie schon an ihm, greift er sofort an (Kevin: "soll immer angreifen").
- Kein Scheinangriff: weder Stoppen vor dem Ziel noch Schnauben ohne Treffer noch Bodenschlag ins Leere.

### 4.3 Pause

`pause` bleibt 0,35 s (Minimum 0,3 wegen `AnimLayer.findLiveNode`, `kampf_fix.md`). Weil nie zweimal derselbe Knoten
folgt, entfaellt der Sonderfall "derselbe Angriff zweimal".

---

## 5. (D) Schnauben im Alltag

Rassenton `huff` gibt es schon (`NCBearDefs.lua`, slot voice, priority 10). Fuer leise einen zweiten Eintrag:

- `nc_bear_sounds.txt`: `sound NCBear_HuffSoft { category = Animals, clip { file = media/sound/NCBear_Huff.wav,
  distanceMax = 20, volume = 0.6, } }`. `volume` neben `file` ist belegt in Bandits `zs_sounds.txt:8-11`
  (`volume = 0.7`); Vanilla nutzt `volume` im clip-Block nur neben `event` (`sounds_zombie_foley.txt:242-243`).
- Rasse: `huffsoft = { name = "NCBear_HuffSoft", slot = "voice", priority = 5 }`.
- Abspielen: `B.a:playBreedSound("huffsoft")` (`ISHutchGrabAnimal.lua:31`). Ueber den Emitter, kein WorldSound, er
  flieht also nicht davor (Kampf-Spez 4.4 gilt nur fuer `addSound`).

Regeln je Baer (Uhr ist die Kampfuhr `F.clock`):

| Fall | Regel |
|---|---|
| Herumlaufen und Stehen (Phase `rest`/`return`, Zustand `idle`, `walk` oder `pathfind`) | naechster Termin `B.nextHuff = clock + 90 + ZombRand(151)` (90-240 s); also nie jede Minute |
| Sitzen-Schleife | Abstand mal 3 (270-720 s); nie in `sitdown`, `standup`, `eat` |
| Spieler kommt nah | `getSpecificPlayer(0)` (`DebugContextMenu.lua:900`), Abstand aus `getX`/`getY`: faellt er unter **3 Kacheln**, einmal schnauben. Erst wieder scharf, wenn er ueber **6** war, und fruehestens 60 s spaeter |
| Kampf | wie heute beim Losrennen (`huff`, hoechstens alle 6 s); danach 20 s kein Alltags-Schnauben |
| Abstand zwischen zwei Alltags-Schnauben | mindestens 60 s, auch wenn beide Regeln zusammenfallen |

Kosten: die Spielerpruefung laeuft im Suchtakt (0,5 s), Zufall und Termin je Baer, keine Liste.

---

## 6. (E) Sitzen und Fressen

### 6.1 Knoten (neu, `42/media/AnimSets/buck/idle/`, Muster wie `NCBear_SwipeL.xml`)

| Datei | m_Name | NCBearAct | Clip | Schleife | Blend | Ereignisse |
|---|---|---|---|---|---|---|
| NCBear_SitDown.xml | NCBearSitDown | `sitdown` | NCBear_SitDown | nein | 0,25 | SetVariable `NCBearDone=true` bei End |
| NCBear_Sit.xml | NCBearSit | `sit` | NCBear_Sit | **ja** | 0,10 | keine |
| NCBear_StandUp.xml | NCBearStandUp | `standup` | NCBear_StandUp | nein | 0,10 | SetVariable `NCBearDone=true` bei End |
| NCBear_Eat.xml | NCBearEat | `eat` | NCBear_Eat | **ja** | 0,30 | keine |

Alle `m_ConditionPriority 10`, `m_SyncTrackingEnabled false`, eine STRING-Bedingung. Damit gilt fuer echte Rehe
dasselbe wie in Kampf-Spez 1.2.
**Warum nicht Vanillas Sitzen** (`buck/idle/idleSit.xml` mit `idleAction = sit` und `m_Transitions`): der Uebergang
Stehen -> Sitzen steht in `idle1.xml` (Vanilla-Datei, nicht aenderbar), und `idleAction` setzt die Engine selbst
(`sitRandomly`). Mit eigener Variable steht er nur auf, wenn wir es sagen, und das Ende ist messbar (`NCBearDone`).

### 6.2 Ablauf (Phase `calm`, Unterzustand `B.calm`)

```
rest --(Befehl oder Zufall 6.3)--> sitdown --NCBearDone--> sit --(Zeit um, Befehl, Ziel)--> standup --NCBearDone--> rest
rest --(Befehl)--> eat --(Zeit um, Befehl, Ziel)--> NCBearAct loeschen (Blend idle1 0,4) --> rest
```

- Beim Eintritt: `setBlockMovement(true)` (`ISPetAnimal.lua:36`), `NCBearAct` setzen (`ISPetAnimal.lua:43`). Beim Austritt:
  loeschen (`:48`), `setBlockMovement(false)` (`:49`).
- **Frist** je Uebergang: Clipdauer + 1 s (wie die Angriffe). Verfaellt `sitdown`, geht er nach `sit`; verfaellt
  `standup`, geht er nach `rest`. Eine laute Zeile nur bei drei Verfaellen in Folge.
- **Die Sperre der Engine laeuft ab** (`BaseAnimalBehavior.wanderIdle` 0-39: Summe des rohen `getMultiplier` bis 8000,
  `kampf_review_gegen.md` Fund 7; bei Tempo 1 rund 167 s, im Schlaf nach Bildern). Darum je Baer `B.blockRaw` mit dem
  **ungedeckelten** `getGameTime():getMultiplier()` (`ISAnimalTracksFinder.lua:28`) aufaddieren und bei 4000
  `setBlockMovement(false)`, dann sofort `(true)` im selben Takt (false setzt den Zaehler zurueck). Die Kampfuhr taugt
  dafuer nicht: sie ist je Bild auf 0,5 s gedeckelt.
- **Fremde Bewegung** (Flucht vor Laerm, `IsoAnimal.respondToSound`): in `calm` wie im Kampf `fleeStop`
  (`stopAllMovementNow`, `ISAnimalContextMenu.lua:760`). Ein Bild Zucken, kein Aufspringen.
- **Getroffen** (Leben sinkt, nur Spieler koennen das): `calm` sofort beenden, `NCBearAct` loeschen, Sperre loesen,
  fliehen lassen (wie `endFight("hurt")`).

### 6.3 Von selbst sitzen (im Spiel)

- Pruefen alle **20 s** Kampfuhr je Baer, nur in Phase `rest` (nicht `return`), Zustand `idle`, kein Ziel in den letzten
  drei Suchtakten (`pickTarget` laeuft dort ohnehin), nicht in den 20 s nach einem Treffer, nicht in den **180 s** nach dem
  letzten Aufstehen.
- Chance `sitChance` **10 %** je Pruefung (im Mittel einmal in rund 3-4 Minuten Ruhe), Dauer 45 + ZombRand(106) s
  (45-150 s), danach Aufstehen.
- Nie fuer `bearstag` (hat die Clips nicht), nie im Mehrspieler.

### 6.4 Kampf geht vor

Im Suchtakt (0,5 s) sucht `pickTarget(radius)` auch in `calm`. Mit Ziel:

| Unterzustand | dann |
|---|---|
| `sitdown` oder `sit` | `NCBearAct = standup`, merken `B.calmNext = z`; bei `NCBearDone` (oder Frist 2,3 s): `clearAct`, Ziel neu pruefen (`targetOk`), `startFight` |
| `standup` | laeuft weiter, dann wie oben |
| `eat` | `NCBearAct` loeschen, `startFight` sofort (Blend 0,3/0,4 s) |

Nach dem Kampf kommt **kein** automatisches Wiederhinsetzen; das macht wieder 6.3 bzw. ein Befehl. Spaeter in B2b gilt
"Sitz" als Befehl: danach wieder hinsetzen.

### 6.5 Ein Schreiber

`NCBearAct` schreibt weiter **nur** `NCBearFight.lua`. Fuer Testdatei und spaetere Befehle gibt es eine kleine Schnittstelle
im Modul (keine Konsole): `F.Calm.Sit(B, sek)`, `F.Calm.Stand(B)`, `F.Calm.Eat(B, sek)`, `F.NearestBear(x, y, r)`. Die
Phase-Funktionen von heute (`fightingCount`, `updateBear`) lernen `calm`. Sonst gaebe es zwei Schreiber derselben
Variable (Familie `autoTrip`).

### 6.6 Testdatei `42/media/lua/client/NCBearBench.lua` (neu, nur Testhilfen, wird nie nach NPC Crew kopiert)

Nur Einzelspieler (`not isClient() and not isServer()`, `ISEatFoodAction.lua:136`), sonst eine Zeile "singleplayer only".
Baer = naechster gemerkter in 12 Kacheln um `getSpecificPlayer(0)`.

| Befehl | tut |
|---|---|
| `NCBear_Sit(sek)` | `F.Calm.Sit` (Vorgabe 60 s) |
| `NCBear_Stand()` | `F.Calm.Stand` |
| `NCBear_Eat(sek)` | `F.Calm.Eat` (Vorgabe 30 s) |
| `NCBear_Huff()` | `playBreedSound("huffsoft")` am naechsten Baeren |
| `NCBear_NextAttack(name)` | erzwingt den naechsten Clip (`swipeL`, `swipeR`, `bite`, `maul`, `slam`, `rear`), einmal (`F.forceNext`) |
| `NCBear_ZHealth(h, r)` | setzt allen Zielen (`F.IsTarget`) in r Kacheln das Leben h (`z:setHealth(h)`, Bandits `BanditClientCommands.lua:36`), Deckel 50 Zombies |
| `NCBear_KnockInfo()` | Zaehler: back, down, verworfen durch die Vorpruefung, Zustand ein Bild nach dem Treffer (letzte 8) |

`NCBear_Fight`, `NCBear_Tune` und `NCBear_FightInfo` stehen heute in `NCBearFight.lua`. Sie bleiben dort bis B1, dann
ziehen sie in die Testdatei um (Copy-Paste-Regel). Das gehoert nicht in diesen Lauf.

---

## 7. (F) Vertrag Animator <-> Lua

30 Bilder/s. In jedem Clip haben alle 26 Knochen Schluessel, der Kiefer eingeschlossen. `Translation_Data` und `Bip01`
bleiben still (wie `kampf_anim.md`). Die Kampfclips beginnen und enden in der Grundhaltung (Mittel von DeerStag_Idle01).
Alte Clips (Idle01, Walk, Run, Death, Dead): **Abweichung 0** messen (Probe.java wie `kampf_anim.md`). Treffer und Ton als
`m_TimePc` mit zwei Stellen; Lua `F.ACTS` traegt dieselbe Dauer und dasselbe `hitPc`.

| NCBearAct | Clip | Dauer | Bilder | Schleife | Ereignisse (`m_TimePc` -> Sekunde) | Treffer bei | Blend |
|---|---|---|---|---|---|---|---|
| rear | NCBear_Rear | **3,00** (bleibt) | 90 | nein | PlaySound `NCBear_Roar` 0,27 (0,81 s); Done End | - | 0,25 |
| swipeL | NCBear_SwipeL | **1,50** | 45 | nein | PlaySound `SledgehammerSwing` 0,28 (0,42 s); Hit **0,40 (0,60 s)**; Done End | Pranke | 0,15 |
| swipeR | NCBear_SwipeR | 1,50 | 45 | nein | gespiegelt | gespiegelt | 0,15 |
| slam | NCBear_Slam | **2,40** | 72 | nein | PlaySound `NCBear_Growl1` 0,04 (0,10 s); PlaySound `AttackStomp` 0,53 (1,27 s); Hit **0,54 (1,30 s)**; Done End | beide Pranken am Boden | 0,20 |
| bite | NCBear_Bite (neu) | **1,30** | 39 | nein | PlaySound `NCBear_Growl3` 0,08 (0,10 s); Hit **0,40 (0,52 s)**; Done End | Schnauze in Halshoehe eines Stehenden | 0,15 |
| maul | NCBear_Maul | 1,60 (bleibt, nach Referenz pruefen) | 48 | nein | PlaySound `NCBear_Growl2` 0,10; Hit 0,34 (0,544 s); Done End | Schnauze am Boden | 0,20 |
| sitdown | NCBear_SitDown (neu) | **1,60** | 48 | nein | Done End | - | 0,25 |
| sit | NCBear_Sit (neu) | **4,00** | 120 | ja | - | - | 0,10 |
| standup | NCBear_StandUp (neu) | **1,30** | 39 | nein | Done End | - | 0,10 |
| eat | NCBear_Eat (neu) | **3,20** | 96 | ja | - | - | 0,30 |

Posen an den Naehten:

- SitDown: Anfang = Grundhaltung, Ende = Sitzpose S.
- Sit: erstes = letztes Bild = S.
- StandUp: Anfang = S, Ende = Grundhaltung.
- Eat: erstes = letztes Bild = Fresspose E (Kopf unten). Rein und raus blendet die Engine.

Sitzpose nach `kevin_sitzvorlage.png`: aufrecht auf dem Hinterteil, Oberkoerper senkrecht und rund, Vorderbeine gerade
zwischen den Hinterbeinen, Pranken flach am Boden, Hinterbeine vorn und leicht gespreizt, Sohlen nach vorn/oben, Kopf leicht
seitlich. Nichts im Boden (tiefster Hautpunkt >= 0 wie `kampf_anim.md`).

**Was der Animator zurueckmeldet** (sonst kann Lua die Weiten nicht setzen):

| Clip | Mass | Lua daraus |
|---|---|---|
| SwipeL/R | Pranke zum Treffer: Kacheln vor Bip01, seitlich, Hoehe | `swipeReach` = vorn + 0,55 (heute 0,82 -> 1,4) |
| Slam | beide Pranken: vorn, seitlich | `slamReach` = vorn + 0,9 (heute 0,60 -> 1,5) |
| Bite | Schnauze zum Treffer: vorn, Hoehe | `biteReach` = vorn + 0,45, `biteHalf` 30 |
| Maul | Schnauze: vorn | `maulReach` = vorn + 0,42 (heute 0,78 -> 1,2) |
| alle | Dauer und Treffermoment, gemessen mit dem Importer | `F.ACTS` dur/hitPc und Knoten-XML gleich |

Treffermomente in Lua (Konstanten oben in `NCBearFight.lua`):

```lua
F.ACTS = {
  rear    = { clip = "NCBear_Rear",    dur = 3.00, hitPc = nil },
  swipeL  = { clip = "NCBear_SwipeL",  dur = 1.50, hitPc = 0.40 },
  swipeR  = { clip = "NCBear_SwipeR",  dur = 1.50, hitPc = 0.40 },
  slam    = { clip = "NCBear_Slam",    dur = 2.40, hitPc = 0.54 },
  bite    = { clip = "NCBear_Bite",    dur = 1.30, hitPc = 0.40 },
  maul    = { clip = "NCBear_Maul",    dur = 1.60, hitPc = 0.34 },
  sitdown = { clip = "NCBear_SitDown", dur = 1.60 },
  standup = { clip = "NCBear_StandUp", dur = 1.30 },
}
-- sit und eat sind Schleifen: keine Frist auf das Ende, nur auf die Dauer des Befehls
```

Weicht der Animator ab, gilt seine Messung, und Lua und XML ziehen nach.

---

## 8. Neue Aufrufe (jeder mit Fundstelle, gleiche Argumenttypen)

| Aufruf | am | Fundstelle |
|---|---|---|
| `z:testDotSide(obj)` -> String | IsoZombie, Arg IsoMovingObject (Baer = IsoAnimal) | Bandits `ZAPush.lua:42` (Arg IsoZombie), `BanditUtils.lua:353` |
| `z:setPlayerAttackPosition(String)` | IsoZombie | Bandits `ZAPush.lua:42`, `ZASmack.lua:431`, `BanditUtils.lua:353` |
| `z:setHitFromBehind(bool)` | IsoZombie | Bandits `ZAPush.lua:41`, `BanditUtils.lua:350` |
| `z:faceLocationF(x, y)` | IsoZombie, float, float | Bandits `ZAAim.lua:12`, `ZABuildFloor.lua:9` |
| `sq:TreatAsSolidFloor()` | IsoGridSquare | `DebugContextMenu.lua:641` |
| `sq:getFloor()`, `floor:hasProperty(IsoFlagType.water)` | IsoGridSquare, IsoObject | `ISWorldObjectContextMenu.lua:686-688` |
| `sq:isBlockedTo(sq2)`, `sq:isWindowTo(sq2)` | IsoGridSquare x2 | `ISInventoryTransferAction.lua:598` (heute schon in `canStrike`) |
| `sq:isFree(false)` | IsoGridSquare | `ISFarmingMenu.lua:463`, `ISWorldObjectContextMenu.lua:2199` |
| `z:setX(f)`, `z:setY(f)` (nur Rueckfall 2.8) | IsoZombie | Bandits `ZASmack.lua:595-596`, `ZAMove.lua:11-19` |
| `getSpecificPlayer(0)` | - | `DebugContextMenu.lua:900` |
| `z:setHealth(h)` (nur Testdatei) | IsoZombie | Bandits `BanditClientCommands.lua:36` |
| `volume =` neben `file =` im Tonskript | Skript | Bandits `zs_sounds.txt:8-11` |

Bereits belegt und weiter benutzt: `knockDown`, `Kill(nil)`, `playBreedSound`, `setVariable/clearVariable/getVariableString`,
`setBlockMovement`, `stopAllMovementNow`, `getActionStateName`, `getMultiplier`, `ZombRand` (`kampf_lua.md`).
**Nicht benutzen:** `setUsePhysicHitReaction`, `setRagdollFall`, `zombie:Hit` fuer Schaden oder Ragdoll, `setStaggerBack`
allein (verliert in 2.2 immer), die Lage "BACK" als Text (erreicht in Vanilla kein Weg).

Mehrspieler: nichts davon. Der Kampf bleibt im MP aus, `NCBear_Fight` sagt es. Die Testdatei verweigert.

---

## 9. Was nur Kevins Test entscheidet

1. Fliegt der Zombie nach FRONT wirklich rund 1,7 Kacheln zurueck und faellt, auch aus `walktoward` und `attack`?
   Zeile `[NCBear] knock: back ...` mit Zustand ein Bild spaeter.
2. Sieht die Drehung zum Baeren beim Treffer (45-120 Grad) als Ruck aus?
3. Sterben Getoetete sauber nach dem Flug (2.9), und liegt die Leiche dort, wo der Flug endet?
4. Stimmen die Schadenszahlen mit Schieber 2,0 und mit echten Zombies (Zufall 0,5-3,8)?
5. Sitzt er nach 2-3 Minuten Ruhe von selbst, steht er beim Zombie zuerst auf, und haelt die Sperre ueber 150 s?
6. Ist das Alltags-Schnauben leise und selten genug?
7. Rueckfall 2.8 nur bauen, wenn 1. scheitert.

Statisch geprueft, nicht gespielt.
