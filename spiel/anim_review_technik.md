# Baer, Lauf baer-anim: Pruefung Technik und Regeln

Stand 08.11.2026, PZ 42.21 (`projectzomboid.jar`), Bandits 42.21. Geprueft: `_arbeit/baer_anim/mod/42` gegen `NCBearTest/42`
(`diff -rq`), dazu `anim_spez.md`, `anim_lua.md`, `anim_clips.md`, `anim_modell.md`, `ENTSCHEIDUNGEN.md`. Selbst gelaufen: Probe.java auf
beide GLB, die vier Lua-Pruefer, die Attrappe, `javap -c -p` auf IsoGameCharacter, IsoZombie, IsoGridSquare, AnimationPlayer,
StaggerBackState, BaseAnimalBehavior (Auszuege und Texte in `_arbeit/baer_anim/pruef/`). Nichts im Mod-Stand geaendert, nichts
gerendert. **Statisch geprueft, nicht gespielt.**

## Funde

1. **ernst -- `NCBearFight.lua:727-736` (knockSetup) -- seitlich stehende Zombies fliegen nie, die Zaehler sagen trotzdem "back".**
   Nach `faceLocationF` liest `z:testDotSide(a)` noch die ALTE Seite, also landet `LEFT`/`RIGHT` in `playerAttackPosition`.
   `to_staggerback-knockeddown` verlangt aber `FRONT`, also gewinnt `to_falldown`: er faellt auf der Stelle, dazu verdreht
   (sein Vorwaerts zeigt schon zum Baeren, der Koerper nicht). `knockStats.back` und `turned` zaehlen ihn trotzdem als Flug.
   Betroffen ist jeder Treffer mit dem Baeren 45-120 Grad neben dem Zombie. Zombies jagen den Spieler und nicht den Baeren,
   das ist also ein grosser Teil.
   **Beleg (Jar):** `IsoGameCharacter.testDotSide` 0-8 -> `testDotSideEnum` 0-7 `getLookVector` -> `getLookAngleRadians` 0-53 =
   `animPlayer.getAngle() + getTwistAngle()` (nur ohne fertigen AnimationPlayer `getDirectionAngleRadians`). `faceLocationF`
   51-58 ruft nur `setForwardDirection` (0-52: Feld `forwardDirection`, kein AnimationPlayer). Den Koerperwinkel zieht erst
   `postUpdateAnimating` nach (`updateForwardDirection` -> `setTargetDirection`), und `interpolateBodyAngle` dreht je Bild
   hoechstens 0,15 rad x Multiplier (`doAnglesInternal` 0-19). XML `actiongroups/zombie/idle/to_staggerback-knockeddown.xml`:
   `compare playerAttackPosition == FRONT`.
   **Die Attrappe ist dort falsch gruen:** `attrappe/test_anim.lua:137-147` rechnet `testDotSide` mit `self.fwd`, und genau das
   setzt `faceLocationF` (:148-156). Der Test "side: flies away from the bear" (:1110-1116) prueft also das Modell, nicht das
   Jar. Spez 2.6 (Kommentar "faceLocationF setzt die Richtung sofort") hat denselben Fehler.
   **Vorschlag:** NICHT einfach `"FRONT"` hart setzen. Dann fliegt er nach seinem ALTEN Hinten:
   `StaggerBackState.execute` 0-14 ruft `setTargetToAngle` und haelt den Koerperwinkel fest. Bei einem Skalarprodukt von -0,5
   ginge der Flug schraeg auf den Baeren zu, und `ClearBehind` haette eine andere Bahn geprueft. Stattdessen: kein Drehen,
   `LEFT`/`RIGHT` wird `down` (why `side`), geflogen wird nur bei `FRONT`. Einen sofortigen Winkel-Setzer gibt es im Jar
   (`setTargetAndCurrentDirection`), er hat aber null Lua-Fundstellen (grep Vanilla und Bandits) und bleibt deshalb ohne
   Kevins Wort tabu. In der Attrappe Blickwinkel und `fwd` trennen (`faceLocationF` aendert nur `fwd`) und eine Mutation
   dazunehmen. In den Zaehlern `back` erst dann zaehlen, wenn wirklich `FRONT` gesetzt wurde.

2. **ernst -- `NCBearFight.lua:721-723` mit `F.ClearBehind` :579-598 -- geprueft wird eine andere Bahn als die, auf der er
   fliegt.** `ClearBehind` prueft die Gerade Baer -> Zombie. Der Clip fliegt aber nach dem eigenen Hinten des Zombies
   (Spez 2.2, `StaggerBackState.execute` setTargetToAngle). `FRONT` heisst Skalarprodukt > 0,7
   (`testDotSideEnum` 78-91), die Abweichung kann also bis rund 45 Grad betragen, nach 1,7 Kacheln bis rund 1,2 Kacheln
   seitlich. Waende, Zaeune und Fenster faengt die normale Kollision (Spez 2.3: `doDeferredMovement` -> `moveUnmodded`). Ob
   die Kollision auch Wasser und eine Ebenenkante (Balkon, Dachrand) haelt, ist ungeprueft. Damit kann Kevins Regel *"nie ins
   Wasser oder ueber eine Ebenenkante"* (ENTSCHEIDUNGEN, Nachtrag 02:40) im seltenen Schraegfall reissen.
   **Vorschlag:** zusaetzlich die Bahn entlang `-getForwardDirection()` pruefen (belegt Bandits `ZAPush.lua:36`, schon in
   knockSetup benutzt). Faellt eine der beiden Bahnen durch, dann `down`. Das kostet hoechstens vier Kacheln mehr je Treffer.

3. **klein -- `NCBearFight.lua:63-66`, Kommentar :48-52 -- die Reichweiten folgen noch nicht der Messung des Animators.**
   `anim_clips.md` 3 (Formeln aus Spez 7): Hieb 0,945+0,55 = 1,5 (heute 1,4), Biss 0,948+0,45 = 1,4 (heute 1,3, als
   "vorlaeufig" markiert), Biss am Boden 0,681+0,42 = 1,1 (heute **1,2**, trifft also 0,1 Kachel weiter, als die Schnauze
   reicht). Der Kommentar nennt noch die alten Masse (0,82/0,78/0,60).
   **Vorschlag:** der Integrator traegt 1,5 / 1,5 / 1,4 / 1,1 ein oder laesst die Werte bewusst stehen, und der Kommentar wird
   neu geschrieben. Die Ankunft 1,1 x 1,15 = 1,265 bleibt dabei unter biteReach.

4. **klein -- `NCBearFight.lua:704-707` und `:732-733` -- zwei Masse fuer "von hinten".** `behind` kommt aus
   `getForwardDirection`, `side` aus dem Koerperwinkel (Fund 1). Mitten in einer Drehung (`side` = BEHIND, `behind` = false)
   bekommt er `setHitFromBehind(false)` und faellt mit `Zombie_Death` rueckwaerts, also auf den Baeren zu.
   **Vorschlag:** `local fromBehind = behind or side == "BEHIND"` fuer `setHitFromBehind` und `knockDown`.

5. **klein -- `NCBearFight.lua:412-415` (goApproach) -- lautes Schnauben jetzt fast im 6-s-Takt.** Mit dem Knockback fliegt
   fast jeder Getroffene 1,7 Kacheln weg. `decide` geht dann nach fast jedem Hieb ins Anrennen, und das laute `huff` kommt
   alle 6 s, den ganzen Kampf lang. Vorher fiel der Zombie auf der Stelle, und der Baer musste selten neu anlaufen. Kevin will
   Schnauben, laestig soll es nicht werden.
   **Vorschlag:** das laute Schnauben nur in `startFight` oder mit 15-20 s Abstand.

6. **klein -- `NCBearFight.lua:1084-1088` -- ein Ziel waehrend des Hinsetzens springt mitten in den Aufsteh-Clip.** Aus
   halbem `sitdown` geht es direkt nach `standup`. StandUp beginnt in der Sitzpose S (anim_clips 3), der Blend ist 0,10 s
   (`NCBear_StandUp.xml`), das gibt einen sichtbaren Ruck. Spez 6.4 erlaubt das so.
   **Vorschlag:** `sitdown` zu Ende spielen lassen (hoechstens 1,6 s, `calmNext` merken) oder den Wechsel nur aus `sit`.

7. **klein -- `NCBearFight.lua:562`/`:571` (flyOk) -- eine offene Tuer laesst den Flug durch.** Kevins Wortlaut (ENTSCHEIDUNGEN,
   Nachtrag 02:40): *"nie durch Wand, Tuer, Zaun"*. Gebaut ist "geschlossen sperrt, offen nicht", und das steht ausdruecklich
   als Absicht da.
   **Vorschlag:** Kevin fragen. Die strenge Fassung waere `a:isDoorTo(b)` als Veto (belegt `ISZoneDisplay.lua:403`,
   `ISObjectClickHandler.lua:135`).

8. **klein -- `anim_lua.md` "Fuer den Abschluss" -- die Kopierliste ist veraltet.** Dort steht: elf Dateien, `diff -rq` zeige nur
   diese. Heute unterscheiden sich 17 Dateien. Dazu kommen `models_X/Skinned/NCBear.glb`, `NCBearDeer.glb`, `WorldItems/NCBear.fbx`,
   `textures/Body/NCBear.png` (a800c084 gegen live 58a4ea41) und `textures/WorldItems/NCBear.png`. **Neues GLB und neue
   Body-Textur gehoeren zusammen**: die Rumpf-UVs sind neu gepackt (`anim_modell.md`). Wer nach der Liste nur das GLB mitnimmt,
   bekommt ein verschmiertes Fell.
   **Vorschlag:** der Abschluss kopiert alles, was `diff -rq` meldet, in einem Zug. Die Liste daraus bauen, nicht aus dem
   Bericht.

9. **klein -- `NCBearFight.lua:131`, :159, :1114-1122, :1423-1437, :246/:575/:1307 -- Testschnittstelle in der Spieldatei.**
   `F.Calm.Play` mit dem Unterzustand `play`, `PLAY_LOOP`, `F.forceNext`, `F._posture`/`_flyOk`/`_tickBody` und `knockLog` dienen
   nur der Testdatei und der Attrappe. Sie liegen aber im Modul, das spaeter per Copy-Paste nach NPC Crew geht. Menues sind es
   nicht, und der einzige Schreiber von `NCBearAct` bleibt richtig in Fight. Dazu drucken die Flugsonde und die
   Treffer-Zeilen bei `log = 1` (Vorgabe) in jedem Spiel. In NPC Crew gehoeren sie hinter `BanditsNPC.Log` (CLAUDE.md, Sonden).
   **Vorschlag:** den Block als "nur Testschnittstelle" markieren und vom Uebernahme-Skript ausnehmen lassen. Beim Uebernehmen
   `log` auf den Crew-Logging-Schalter legen.

## Geprueft und in Ordnung

- **Clipnamen:** Probe.java selbst auf `mod/42/.../NCBear.glb` laufen lassen (MD5 f06d9ec1..., = anim_clips). 15 Clips, die zehn
  `NCBear_*` mit genau den Dauern aus `F.ACTS` (Bite 1,3, Eat 3,2, Maul 1,6, Rear 3,0, Sit 4,0, SitDown 1,6, Slam 2,4, StandUp
  1,3, SwipeL/R 1,5). `m_AnimName` aller zehn XML ist gleich. Die Kopfzeilen der fuenf `DeerStag_*` sind byte-gleich zur
  Live-GLB.
- **Treffermomente:** `m_TimePc` = `hitPc` (0,40/0,40/0,54/0,40/0,34), in Sekunden 0,60 / 1,30 / 0,52 / 0,544, passend zu
  anim_clips 3 (Schlag-Ende, Aufsetzen 1,27, Zubeissen 0,48-0,56). Die Toene passen auch: Wusch 0,42 s, Stampfen 1,27 s,
  Knurren 0,10 s, Bruellen 0,81 s. `faceUntil` = Treffermoment.
- **Ziele:** jeder Weg zu Schaden, Umwerfen, Drehen und Schieben geht ueber `F.IsTarget` (pickTarget, countFoes, hitList,
  NCBear_ZHealth). `knockSetup`/`faceLocationF`/`addPush` laufen nur auf hitList-Treffern. Die Reihenfolge der NPC-Crew-Marken
  ist unveraendert.
- **Schaden gegen das Jar:** `IsoZombie.resetForReuse` 316-443 selbst gelesen: zaeh 3,5-3,8, normal 1,8-2,1, zerbrechlich
  0,5-0,8, Zufall 0,5-3,8. Hieb 1,0 heisst normal 2 Treffer bis 2,0 Leben und 3 darueber; Hieb + Bodenbiss 2,8 toetet jeden
  normalen. Das passt zu "2-3 Hiebe".
- **Knockback-Aufrufe:** alle belegt, mit gleichen Argumenttypen (`ZAPush.lua:36/41/42`, `ZAAim.lua:12`,
  `DebugContextMenu.lua:668`, `ISInventoryTransferAction.lua:585-608`, `ISWorldObjectContextMenu.lua:684-688`,
  `ISFarmingMenu.lua:463`). `knockDown` (Jar 0-43) schreibt BEHIND/null, deshalb muss `setPlayerAttackPosition` danach stehen.
  XML-Rangfolge selbst gelesen: FRONT 4 Bedingungen gegen falldown 3. Die ragdoll-Variante braucht `usePhysicHitReaction`.
  Nicht geladene Kachel, kein Boden, Treppe, Wasser, solid, Moebel, Wand/geschlossene Tuer, Fenster: Veto. Schritt 0,45 < 1,
  also bleiben die Kacheln benachbart. Das Schieben ist aus (Vorgabe 0), hat einen Deckel von 8 und hoechstens 0,05 je Bild.
- **Angriffswahl:** der letzte Clip faellt raus, bei Summe 0 kommt ein Hieb im Wechsel, nie zweimal derselbe. Biss nur gegen
  Stehende (`posture == "up"`) bei Wahl und Treffer, Biss am Boden nur gegen Liegende oder Fallende. Aufrichten nur in
  `startFight` (120 s, 50 %, > 2,5 Kacheln). Kein Scheinangriff.
- **Sitzen und Fressen:** jeder Unterzustand hat einen Ausgang (Done, Frist Dauer + 1 s, Zeit, Befehl, Ziel, Treffer). Kampf geht
  vor: aus `sit` erst aufstehen, aus `eat`/`play` sofort. Ein verschwundenes Ziel faengt `targetOk` nach dem Aufstehen ab. Ein
  toter oder entladener Baer faellt bei `scanBears` raus, Marke und Sperre werden geloest, `register` loescht die Marke,
  `releaseAll` raeumt alles. Ohne Spieler (`pl` nil) ist alles abgesichert. Die Sperre ist gegen
  `BaseAnimalBehavior.wanderIdle` 0-39 (8000) und `setBlockMovement` 0-24 selbst nachgelesen, Erneuerung bei 4000. Es gibt
  einen Schreiber von `NCBearAct` (zwei `setVariable`-Stellen, beide in Fight).
- **Schnauben im Alltag:** 90-240 s, sitzend 270-720 s, nie beim Hinsetzen, Aufstehen oder Fressen. Spieler unter 3 Kacheln:
  einmal, wieder scharf erst ueber 6 und nach 60 s. Zwischen zwei Schnauben mindestens 60 s, nach dem Kampf 20 s still.
  Leiser Rassenton (Prioritaet 5, volume 0,6, distanceMax 20), kein WorldSound.
- **Testhilfen:** die acht neuen Befehle stehen nur in `NCBearBench.lua`, ohne Namenskollision (grep NCBearTest, NPC Crew `42`,
  Stand). Es gibt kein neues Menue. Die Spawn- und Testmenues sind unveraendert (diff).
- **Kosten und Deckel:** je Bild hoechstens 8 Sonden, 8 Schiebe-Eintraege, 8 Baeren. Listendurchlaeufe nur im 0,5-s-Takt oder
  je Angriff, Sichtpruefungen 12 je Treffer, gesperrte Ziele 32. Mehrfachrueckgaben sind sauber (`report(F.Calm.X(...))`
  letztes Argument, `local ok = F.IsTarget`).
- **Pruefer:** luacheck 0, scopecheck 0, localcount hoechstens 105. luacheck_pz meldet nur W113 auf den eigenen Global
  `NCBearFight`. LF, ASCII, ohne BOM (NCBearAttackProbe CRLF, unveraendert wie live). Attrappe selbst gelaufen: 289 Pruefungen,
  0 Fehler (aber Fund 1).
- **Mehrspieler:** bleibt aus, `onTick` hinter `isSP()`, `NCBear_Fight` und die Testdatei sagen es.

## Urteil

Regeln, Ziele, Schaden, Clipnamen und Ruhe-Knoten stehen sauber. Der Knockback, Kevins Hauptwunsch, wirkt aber nur, wenn der
Baer vorn steht: seitlich getroffene Zombies fallen auf der Stelle, und die Zaehler melden trotzdem "back" (Fund 1). Die
Pruefbahn hinter dem Zombie ist nicht die Flugbahn (Fund 2). Beides gehoert vor Kevins Test repariert, beides ohne neuen
unbelegten Aufruf.

Statisch geprueft, nicht gespielt.
