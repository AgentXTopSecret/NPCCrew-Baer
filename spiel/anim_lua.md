# Baer: Lua-Bau im Lauf baer-anim

Stand 08.11.2026, PZ 42.21, Bandits 42.21. Gebaut nach `anim_spez.md` unter
`_arbeit/baer_anim/mod/42`. Nichts nach `NCBearTest` kopiert, nichts unter NPC Crew `42`/`common` und nichts in einer fremden
Mod geaendert. Das GLB hat der Animator, ich habe es nicht angefasst. **Statisch geprueft, nicht gespielt.**
Attrappe in Lua 5.1: 289 Pruefungen gruen, 15 von 15 Mutationen fallen auf.

## Dateien (alle LF, ASCII, ohne BOM)

| Datei unter `_arbeit/baer_anim/mod/42/media/` | neu/geaendert | Inhalt |
|---|---|---|
| `lua/shared/NCBearFight.lua` | geaendert | Knockback, Schaden, gewichtete Angriffswahl samt Biss gegen Stehende, Aufrichten nur zu Kampfbeginn, Alltags-Schnauben, Phase `calm` (Sitzen/Fressen), Schnittstelle `F.Calm`, Sonde "wie weit flog er" |
| `lua/client/NCBearBench.lua` | **neu** | nur Testbefehle, wird nie nach NPC Crew kopiert |
| `lua/shared/NCBearDefs.lua` | geaendert | Rassenton `huffsoft` (Prioritaet 5) |
| `scripts/nc_bear_sounds.txt` | geaendert | `NCBear_HuffSoft`: dieselbe wav, `distanceMax = 20`, `volume = 0.6` (Form Bandits `zs_sounds.txt:8-11`) |
| `AnimSets/buck/idle/NCBear_SwipeL.xml`, `_SwipeR.xml` | geaendert | Wusch 0,28, Treffer 0,40 (vorher 0,27/0,42) |
| `AnimSets/buck/idle/NCBear_Slam.xml` | geaendert | Knurren 0,04, Stampfen 0,53, Treffer 0,54 (vorher 0,05/0,55/0,57) |
| `AnimSets/buck/idle/NCBear_Bite.xml` | **neu** | `bite`, Clip `NCBear_Bite`, Blend 0,15, Knurren `NCBear_Growl3` 0,08, Treffer 0,40, Done End |
| `AnimSets/buck/idle/NCBear_SitDown.xml` | **neu** | `sitdown`, nicht geloopt, Blend 0,25, Done End |
| `AnimSets/buck/idle/NCBear_Sit.xml` | **neu** | `sit`, `m_Looped true` (belegt `AnimSets/player/idle.xml`), Blend 0,10, keine Ereignisse |
| `AnimSets/buck/idle/NCBear_StandUp.xml` | **neu** | `standup`, Blend 0,10, Done End |
| `AnimSets/buck/idle/NCBear_Eat.xml` | **neu** | `eat`, geloopt, Blend 0,30, keine Ereignisse |

Alle Knoten wie die Kampfknoten: Prioritaet 10, eine STRING-Bedingung auf `NCBearAct`, `m_SyncTrackingEnabled false`. Mit
Python geparst. **Ausgang aus jedem Knoten** ist die Bedingung selbst: `NCBearFight.lua` loescht oder wechselt `NCBearAct`, dann
nimmt die Engine einen anderen Knoten (Blend). Dazu hat jeder nicht geloopte Knoten eine Frist (Clipdauer + 1 s).

Dauern und Treffer stehen oben in `F.ACTS` (rear 3,00; swipeL/R 1,50/0,40; slam 2,40/0,54; bite 1,30/0,40; maul 1,60/0,34;
sitdown 1,60; sit 4,00 Schleife; standup 1,30; eat 3,20 Schleife). **Weicht der Animator ab, gilt seine Messung:** `F.ACTS`, die
`m_TimePc` in den Knoten und `biteReach` (heute vorlaeufig 1,3) nachziehen.

## Verhalten

**Schaden** (anim_spez 3.2): Hieb 1,0, Nebenziel 0,6 (Hieb und Doppelschlag), Doppelschlag 0,9, Biss stehend 1,2, Biss am Boden 1,8,
alles mal `dmg`. Gerechnet in der Attrappe: 2,0 Leben = 2 Hiebe, 2,1 = 3 Hiebe oder Hieb + Biss, 3,6 = 4 Hiebe. Ein Zombie aus dem
Debug-Spawn hat **1,0** (Schieber "Health"), dort toetet jeder Hieb: den Schieber auf 2,0 stellen oder `NCBear_ZHealth(2, 10)`.

**Angriffswahl** (4.1): erst Blick aufs Ziel, dann Kandidaten mit Gewicht, der zuletzt gespielte Clip faellt raus, dann
`ZombRand(summe)`. Biss am Boden 70 (Ziel liegt oder faellt), Biss 30 (Ziel steht, bis 1,3, Kegel +-30), Hieb links/rechts je 25,
+15 zur Seite des Ziels, Doppelschlag 40 (Abklingzeit frei und **ein** weiterer Gegner vorn, vorher zwei). Nie zweimal derselbe Clip.
Alle Gewichte per `NCBear_Tune` (`wSwipe`, `wSide`, `wBite`, `wMaul`, `wSlam`).

**Aufrichten mit Bruellen** (4.2): nur zu Kampfbeginn, Abklingzeit 120 s, Chance 50 %, nur wenn das Ziel weiter als 2,5 Kacheln weg
ist; sonst greift er sofort an. Der alte Zweig "mitten im Kampf nochmal" ist ganz weg (Feld `reRoar` gestrichen, statt eines Reglers,
der nichts tut). Kein Scheinangriff: jede Wahl ist ein Angriff mit Treffer.

**Knockback** (2.6/2.7): Hieb und Doppelschlag werfen nach hinten, der stehende Biss wirft auf der Stelle, der Biss am Boden wirft
nicht. Je Treffer: Seite aus Sicht des Zombies (`testDotSide`), liegt der Baer seitlich, dreht `faceLocationF` den Zombie zu ihm, dann
`setHitFromBehind(false)`, `knockDown`, **danach** `setPlayerAttackPosition(FRONT)`. Laut XML spielt er dann `Zombie_StaggerBackFall`
(rund 1,7 Kacheln zurueck). Auf der Stelle faellt er, wenn der Baer hinter ihm steht (dann mit `frombehind` nach vorn, also auch vom
Baeren weg; nie um 180 Grad gedreht), wenn er naeher als 0,05 ist oder wenn die Pruefung hinter ihm etwas findet: Pruefpunkte alle
0,45 bis 1,8 Kacheln, je neue Kachel Vanillas Ablege-Frage `ISInventoryTransferAction:canDropOnFloor` (:585-608: Boden, solid,
Wand/geschlossene Tuer/Treppenkante, Fenster, Treppe) plus Wasser (`ISWorldObjectContextMenu.lua:686-688`) und `isFree(false)`
(Moebel, Baum). Nicht geladen = auf der Stelle. Offene Tuer laesst ihn durch. Toedliche Treffer werden vor `Kill(nil)` genauso
umgeworfen (`knockKill`, ungespielt).

**Rueckfall 2.8** (eigenes Schieben, Form Bandits `ZAMove.lua:11-19`) ist gebaut, **Vorgabe aus** (`knockPush 0`). Nur
einschalten, wenn `knock: back` im Spiel auf der Stelle faellt: `NCBear_Tune("knockPush", 1)`, dazu ggf. `knockBack 0`. Je Bild
hoechstens 0,05 Kacheln, hoechstens 0,6 s, jede neue Kachel geprueft wie oben, Deckel 8.

**Sonde** "wie weit flog er": je umgeworfenem Zombie nach 2,3 s (toedlich: bis die Leiche liegt, hoechstens 4 s) eine Zeile, Stufe 1:
`[NCBear] knock: back | 1 frame later staggerback-knockeddown | after 2.30 s moved 1.70 tiles, state onground`. Das beantwortet
Spez 9 Punkt 1 und 3 direkt. Deckel 8 Messungen, letzte 8 Zeilen in `NCBear_KnockInfo()`.

**Schnauben im Alltag** (5): leiser Rassenton `huffsoft`. Ruhe und Rueckweg: alle 90-240 s. Sitzen: alle 270-720 s. Nie beim
Hinsetzen, Aufstehen, Fressen. Spieler unter 3 Kacheln (gleiche Ebene): einmal, wieder scharf erst ueber 6 und fruehestens 60 s
spaeter. Zwischen zwei Alltags-Schnauben immer mindestens 60 s, nach dem Kampf 20 s still. Das laute Schnauben beim Losrennen bleibt.
Regler `huff` (0/1), `huffMin`, `huffSpread`.

**Sitzen und Fressen** (6): Phase `calm`. Hinsetzen -> Sitzen (Schleife) -> Aufstehen, Fressen (Schleife). Beim Eintritt
Bewegung gesperrt, beim Austritt frei. Die Sperre der Engine laeuft bei 8000 roh ab (Jar `BaseAnimalBehavior.wanderIdle` 0-39,
selbst nachgelesen), wir erneuern sie bei 4000 im selben Bild (false, dann true); das gilt jetzt auch im Kampf. Von selbst: alle
20 s, nur in Ruhe und im Stehen, drei Suchtakte ohne Ziel, nicht 20 s nach einem Treffer oder Schmerz, nicht 180 s nach dem
letzten Aufstehen, Chance 10 % (`sitChance`), Dauer 45-150 s. **Kampf geht vor:** sitzend erst aufstehen, dann kaempfen;
fressend sofort los. Getroffen: Ruhe ab. Fehlt ein Hinsetz-/Aufsteh-Clip, geht es nach der Frist weiter, eine laute Zeile erst
beim dritten Mal in Folge.

**Ein Schreiber:** `NCBearAct` schreibt nur `NCBearFight.lua`. Die Testdatei ruft `F.Calm.Sit/Stand/Eat/Play`,
`F.NearestBear`, `F.forceNext`.

## Abweichungen von der Spez (mit Grund)

1. **Haltung mit drei Stufen statt "liegt ja/nein".** Ein Zombie im Taumeln oder Fallen (Aktionszustand beginnt mit `falldown`,
   `staggerback-knockeddown`, `knockeddown`, `onground`, `getup`, `getdown`, `falling`, ...) gilt als "faellt". Er wird **nicht noch
   einmal umgeworfen**: sonst haette `faceLocationF` ihn mitten im Flug gedreht (`StaggerBackState` dreht den Clip nach seinem
   Blick). Biss am Boden darf ihn nehmen, der stehende Biss nicht. Nach hinten fliegen nur Zombies aus `idle`, `walktoward`,
   `pathfind`, `attack`, `lunge` (die fuenf Ordner aus Spez 2.2); aus jedem anderen stehenden Zustand faellt er auf der Stelle.
2. **Die Pruefung hinter ihm ist strenger:** vier Pruefpunkte statt zwei, dazu `isSolid`/`isSolidTrans`/`HasStairs` aus Vanillas
   Ablege-Frage. Treppe = auf der Stelle.
3. **Nebenziele des Doppelschlags bekommen 0,6** (Spez-Tabelle: "dmgSide (Hieb/Slam Nebenziel)").
4. **`knockKill` gilt auch fuer "auf der Stelle"**: vor `Kill(nil)` dann `setHitFromBehind` + `knockDown`, damit ein von hinten
   Getoeteter nicht auf den Baeren zu faellt. `knockKill 0` = genau wie heute.
5. `NCBear_AnimTest(name)` spielt jeden Clip aus `F.ACTS` einmal (Schleifen zweimal), ohne Treffer; ein Zombie bricht ihn ab.

## Neue Engine-Aufrufe (je Fundstelle, gleiche Argumenttypen; selbst gegrept)

| Aufruf | Fundstelle |
|---|---|
| `z:testDotSide(baer)` | Bandits `ZAPush.lua:42` (Jar: Parameter `IsoMovingObject`, Rueckgabe String) |
| `z:setPlayerAttackPosition(String)`, `z:setHitFromBehind(bool)` | Bandits `ZAPush.lua:41-42` |
| `z:faceLocationF(x, y)` | Bandits `ZAAim.lua:12`; Jar 0-50: bei Abstand 0 Warnung mit Stacktrace, deshalb erst ab 0,05 |
| `sq:TreatAsSolidFloor()`, `isSolid()`, `isSolidTrans()`, `isBlockedTo(sq)`, `isWindowTo(sq)`, `HasStairs()` | `ISInventoryTransferAction.lua:589-601` |
| `sq:getFloor()`, `floor:hasProperty(IsoFlagType.water)` | `ISWorldObjectContextMenu.lua:687-688` |
| `sq:isFree(false)` | `ISFarmingMenu.lua:463` (Jar: solid, solidtrans, Baum, kein Boden; Treppe gilt als frei) |
| `z:setX(f)`, `z:setY(f)` (nur Rueckfall, Vorgabe aus) | Bandits `ZAMove.lua:12-19` |
| `getSpecificPlayer(0)` | `DebugContextMenu.lua:921` |
| `z:setHealth(h)` (nur Testdatei) | Bandits `BanditClientCommands.lua:36` |
| `getBehavior():setBlockMovement(false/true)` im selben Bild | `ISPetAnimal.lua:36/:49` |

Nicht benutzt: `setUsePhysicHitReaction`, `setRagdollFall`, `zombie:Hit`, `setStaggerBack` allein, die Lage "BACK".

## Testdatei `client/NCBearBench.lua` (nur Einzelspieler)

`NCBear_Sit(sek)` (Vorgabe 60), `NCBear_Stand()`, `NCBear_Eat(sek)` (Vorgabe 30), `NCBear_Huff()`, `NCBear_NextAttack(name)`
(swipeL, swipeR, bite, maul, slam, rear; einmal), `NCBear_AnimTest(name)` (ohne Namen: Liste), `NCBear_ZHealth(h, r)` (nur Ziele
nach der harten Regel, Deckel 50), `NCBear_KnockInfo()`. Baer = naechster in 12 Kacheln; Baeren werden alle 5 s gefunden.
`NCBear_Fight`/`_Tune`/`_FightInfo` bleiben bis B1 in `NCBearFight.lua` (Spez 6.6).

## Pruefungen

* luacheck 0, scopecheck 0, localcount hoechstens 105 insgesamt (Hauptteil `NCBearFight.lua`), luacheck_pz auch `--unused`: nur
  W113 auf den eigenen Global `NCBearFight` (wie vorher). Kollisionsprobe: `NCBear_Sit/Stand/Eat/Huff/NextAttack/AnimTest/ZHealth/
  KnockInfo` gibt es sonst nirgends (NCBearTest, NPC Crew).
* Attrappe `_arbeit/baer_anim/attrappe/test_anim.lua` (aufrufen mit Fight- und Bench-Pfad): die 118 alten Pruefungen (an Bruellen
  120 s/Zufall und Gewichte angepasst) und 171 neue: Kandidaten und Wahl (3000 Zuege, nie doppelt), Aufrichten nur zu Kampfbeginn,
  Biss nur gegen Stehende in echten Kaempfen, Knockback vorn/seitlich/hinten mit Aufrufreihenfolge, 13 Faelle der Pruefung hinter ihm
  (Wand, geschlossene Tuer, Fenster, Wasser, Ebenenkante, Treppe vor und unter ihm, nicht geladen, Kiste, Baum, schraege Wand, offene
  Bahn), Schaden, toedlicher Flug, Rueckfall-Schieben samt Wand/Wasser/Deckel, Schnauben-Takt, Sitzen von selbst und auf Befehl,
  Kampf geht vor, Fristen, Sperre-Erneuerung, Absagen, Testdatei, Mehrspieler. Spieler, Crew, Neutrale, Zivilisten, Tiere und
  `tcUid` bekommen nie Treffer, Umwerfen oder Drehung.
* Gegenprobe `attrappe/mutate.py`: 15 Mutationen (u. a. FRONT vor knockDown, Pruefung hinter ihm immer frei, Aufstehen uebersprungen,
  Sperre nie erneuert, Biss auf Liegende, ZHealth ohne Regel), **15 fallen auf**.

## Was nur Kevins Test entscheidet

1. Fliegt ein Zombie wirklich rund 1,7 Kacheln? Die Zeile `knock: back | 1 frame later ... | moved ...` sagt es.
2. Sieht das Drehen zum Baeren beim Treffer wie ein Ruck aus?
3. Liegt ein getoeteter Zombie am Ende des Flugs (`killing blow ... body gone`)?
4. Passt der Schaden mit Schieber 2,0 und mit echten Zombies (Zaehigkeit Zufall 0,5-3,8)?
5. Setzt er sich nach 2-3 Minuten Ruhe von selbst, steht er beim Zombie erst auf, haelt die Sperre?
6. **Ist das Alltags-Schnauben hoerbar?** `volume 0.6` auf einem Huff, den Kevin schon "sehr leise" fand: kaum hoerbar, dann
   `volume` in `nc_bear_sounds.txt` hoch (Neustart) oder den Huff neu schneiden.

## Fuer den Abschluss

* **Nur zusammen mit dem neuen `NCBear.glb` kopieren** (Clips `NCBear_Bite`, `NCBear_SitDown`, `NCBear_Sit`, `NCBear_StandUp`,
  `NCBear_Eat`). Ohne den Biss-Clip verfaellt jeder Biss mit einer Zeile `*** bite did not finish`; Notbremse dann
  `NCBear_Tune("wBite", 0)`.
* Vorher `tasklist | grep -i ProjectZomboid`; laeuft das Spiel, nicht kopieren. Nur hinzufuegen/ueberschreiben, nie spiegeln.
* Zu kopieren: die elf Dateien der Tabelle oben. `diff -rq` gegen `NCBearTest/42` zeigt heute nur diese.

Statisch geprueft, nicht gespielt.
