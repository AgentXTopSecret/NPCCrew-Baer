# Pruefung Baer-Kampf: Ziele, Schaden, Modi

Stand 08.11.2026, Pruefer (adversarisch, nur gelesen). Geprueft: `_arbeit/baer_kampf/mod/42/media/lua/shared/NCBearFight.lua`
und `NCBearDefs.lua`, Berichte `kampf_spez.md`, `kampf_lua.md`. Jar 42.21 mit javap, Vanilla- und Bandits-Lua, NPC-Crew-Lua nur lesend.
Eigene Proben: `_arbeit/baer_kampf/pruefer_regeln/probe.lua` (Attrappe aus `attrappe/test_fight.lua` plus fuenf Faelle P1-P5),
Lauf mit `lua5.1.exe probe.lua ../mod/42/media/lua/shared/NCBearFight.lua`. Die Attrappe des Bauers laeuft gruen (79/0).
**Statisch geprueft, nicht gespielt.**

## Funde

1. **ernst -- NCBearFight.lua:382-405 (hitList), :407-438 (ApplyHit) -- Treffer durch Waende, geschlossene Tueren und Fenster.**
   Beim Treffer werden Regel, Ebene, Abstand und Kegel neu geprueft, die Sicht nicht. Haupt- und Nebenziele hinter einer Wand
   bekommen Schaden, werden umgeworfen und getoetet. Spez 3.2 Punkt 1 verlangt `CanSee` beim Treffer; `kampf_lua.md` sagt "neu
   geprueft" ohne die Luecke zu nennen. Praktisch: Baer im Haus oder an der Basismauer, Zombies druecken von aussen an die Wand
   -> sie fallen durch die Wand. Kein Bruch der harten Regel (es bleiben Zombies), aber gegen "realistisch".
   Beleg: Probe P2 (Nebenziel mit `CanSee = false` im Kegel): 1 Treffer, 1 Mal umgeworfen.
   Vorschlag: in `hitList` je Kandidat `a:CanSee(z)` (dieselbe Form wie `pickTarget`:211, belegt Bandits BanditUpdate.lua:1087,
   :1203; hoechstens 6 je Treffer), dazu fuer Nachbarkacheln Bandits' Wandtest `baerSq:isSomethingTo(zSq)` (BanditUpdate.lua:1205,
   Vanilla ISBBQMenu.lua:108, beide IsoGridSquare). Kein Treffer ohne Sicht, Hauptziel eingeschlossen.

2. **ernst (selten) -- NCBearFight.lua:175-182 (targetOk), :468-474 (decide) -- Kampf gegen einen Geist bis 90 s.**
   `targetOk` fragt nie, ob das Ziel noch in der Welt ist. Ein lebend entfernter Zombie (`removeFromWorld` +
   `removeFromSquare`: NPC Crews Kopien-Netz in der Basis, Bandits' Abraeumen, Engine-Virtualisieren, Pool) behaelt `isAlive`,
   Leben und x/y. Steht er in Ankunftsweite, schlaegt der Baer ins Leere, bis `fightMax` greift. Wird das Pool-Objekt fuer einen
   neuen Zombie bis 25 Kacheln weiter benutzt, rennt er ihm nach (die Regel wird neu geprueft, also kein Regelbruch).
   Beleg: Probe P1: nach dem Entfernen 44 Angriffe, Ruhe erst nach 87,4 s. Jar: `IsoMovingObject.removeFromSquare` Offset 38-45
   setzt `current` und `last` auf null, `IsoObject.removeFromSquare` laesst `square` stehen. Darum taugt `getSquare()` nicht
   (gibt `square` zurueck, Offset 12-16), `getCurrentSquare()` schon (gibt `current`, Offset 0-4).
   Vorschlag: in `targetOk` `if z:getCurrentSquare() == nil then return false end` (belegt am IsoZombie: Bandits
   BanditUpdate.lua:574). Sicherer dazu: im 0,5-s-Takt fuer jeden kaempfenden Baeren pruefen, ob `B.target` in
   `getZombieList()` steht (ein Durchlauf, hoechstens 4 Baeren), sonst Ziel weg.

3. **klein -- NCBearFight.lua:124-144 (F.IsTarget) -- Bandit im oder unter einem Fahrzeug ist Ziel.**
   Banditen sitzen in Autos (Bandits BanditUpdate.lua:270, beim Tod `veh:exit(bandit)` :2414-2415). Der Baer kann einen
   sitzenden feindlichen Banditen treffen und `knockDown` rufen; was das mit dem Sitz macht: ungeprueft. Probe P5: Ziel.
   Vorschlag: `z:getVehicle() ~= nil` oder `z:isUnderVehicle()` -> kein Ziel (beide am IsoZombie belegt, Bandits
   BanditMenu.lua:162-163).

4. **klein -- NCBearFight.lua:134 -- ein Koerper ohne Gehirn und ohne Bandit-Marke gilt als gewoehnlicher Zombie.**
   Bandits' eigene Spawns (auch freundliche Zivilisten und Begleiter) bekommen das Gehirn erst im ersten `OnZombieUpdate`
   (Server-Spawner schreibt nur `gmd[id] = brain`, BanditServerSpawner.lua:463, :582; der Koerper erst beim Banditize).
   Bis dahin ist er fuer uns ein Zombie (Probe P4). Das Fenster ist hoechstens ein Bild, und der Schaden faellt erst beim
   Treffer nach neuer Pruefung -- praktisch ausgeschlossen. NPC Crew ist im SP NICHT betroffen: ihr Neubau schreibt das Gehirn
   im selben Aufruf in den Koerper (Persistence.lua:5453-5455, `gmd[id] = brain` + `BanditBrain.Update`).
   Vorschlag (wahlweise): Ziel erst, wenn der Koerper in einem frueheren Suchtakt schon gesehen wurde (Marke im ModData des
   Zombies, die `resetForReuse` wieder loescht).

5. **klein -- NCBearFight.lua:599-608 (scanBears), :580-591 (register) -- ein Baer, der mitten im Kampf die Welt verlaesst,
   behaelt Sperre und Marken.** `gone()` wirft den Eintrag weg, ohne `setBlockMovement(false)` und `clearVariable`. Kommt
   dasselbe Objekt zurueck (Anhaenger o. ae., ungeprueft ob moeglich), wird es als "rest" neu gemerkt, steht aber gesperrt da,
   bis ein Kampf beginnt oder die Engine die Sperre nach Summe 8000 selbst loest (Spez 2). Probe P3: nach 30 s ohne Gegner
   `block = true`. Vorschlag: beim Verwerfen eines nicht toten Baeren `clearAct` + `setBlock(false)`; in `register` einmal
   `clearVariable("NCBearAct")` und `setBlockMovement(false)`.

6. **klein -- NCBearFight.lua:340-349 (ChooseAct) vor :253 (face in beginAct) -- Doppelschlag-Wahl mit alter Blickrichtung.**
   `countFoes(..., frontOnly)` liest `B.fx/fy` aus dem letzten `face`, nach dem Anrennen also oft eine alte Richtung (beim
   neuen Baeren die Vorgabe 1,0). Nur die Wahl ist betroffen, der Treffer selbst rechnet mit der frischen Richtung.
   Vorschlag: `face(B, z)` am Anfang von `decide`/`ChooseAct`.

7. **klein -- NCBearFight.lua:497-504 -- falsche Diagnose nach drei verfallenen Angriffen.** Verlaesst der Baer `idle` (Flucht
   vor Schuessen, `hitreaction`), verfallen die Angriffe, und die Zeile sagt "fight clips probably missing" plus 60 s Ruhe.
   Kein Fehlverhalten, aber eine Sonde mit Fehlalarm. Vorschlag: den Zustand beim Verfall mitschreiben
   (`getActionStateName()`), "clips missing" nur, wenn er dabei `idle` war.

## Geprueft und in Ordnung

- **Wer in der Liste steht:** `IsoCell.getZombieList()` ist `ArrayList<IsoZombie>` (javap). Spieler, Tiere (IsoAnimal erbt von
  IsoPlayer), Fahrzeuge, Kisten und Leichen (IsoDeadBody) koennen gar nicht hinein; `instanceof(z, "IsoZombie")` zusaetzlich.
  Tot, `isOnKillDone`, Leben <= 0, gezogene Leiche, scheintot, andere Ebene: kein Ziel. Die Attrappe legt Spieler und Tiere
  sogar absichtlich in die Liste -- kein Treffer.
- **Feind-Erkennung:** genau `Bandit.IsHostile` (Bandit.lua:600-605: `hostile or hostileP`); `loyal` davor (AreEnemies "babe",
  BanditUtils.lua:785-786); `hostileP` = "hostility against players" (BanditServerSpawner.lua:409-410). Gehirn fehlt trotz
  Marke, Gehirn kein table: kein Ziel. NPC-Crew-Marken stehen vor `hostileP`; NPC Crews kurzer `hostileP`-Tausch
  (Compat.lua:171-195) laeuft im selben Aufruf, unser OnTick nie dazwischen.
- **Mit NPC Crew bleiben feindliche Raeuber Ziel:** `npcUid` vergibt NPC Crew nur beim Anwerben und Aufzeichnen
  (`P.EnsureUid`, Persistence.lua:634-639; Changelog v3.13.98), `tcUid` nur bei `npcUid` (Guardian.lua:1297-1298). Bewusst
  konservativ: entlassene Begleiter, NPC-Crew-Neutrale, die Bandits nach einem Spielertreffer feindlich macht
  (BanditPlayer.lua:116-120), und zombifizierte Ex-Begleiter (`tcUid` bleibt, CLAUDE.md v3.9.35) werden nie angegriffen --
  "im Zweifel kein Ziel". Bandits' eigene Neutrale, die der Spieler veraergert hat, sind nach Bandits' Regel feindlich und Ziel.
- **NPC Crews getauschtes `instanceof`** (fuenfte Ausnahme) faengt nur (Schuetze, "IsoPlayer"); wir rufen nur mit "IsoZombie"
  und "IsoAnimal".
- **Schaden mit belegten Aufrufen, gleiche Typen:** `setHealth(Zahl)` und `Kill(nil)` am Banditen/IsoZombie (Bandits
  BanditUpdate.lua:2386-2397), `knockDown(boolean)` (DebugContextMenu.lua:666-668, Menue uebergibt true/false :562-563; Jar
  IsoZombie.knockDown 0-43). "Von hinten" wie Bandits ZAPush.lua:32-39, true = faellt nach vorn (Menue "Knock Forward" = true).
  Kein `Hit`, also keine `OnHitZombie`-Aufsaetze. Bandits setzt das Leben eines Banditen nicht je Bild zurueck (nur einmal in
  ApplyVisuals, Bandit.lua:264-269, und beim Bandagieren auf 1,2, ZABandage.lua:50) -- der Schaden bleibt.
- **Kegel:** `AngleLeft` richtig herum (Blick Nord, links = West; Blick Ost, links = Nord), Prankenhieb L -40..+70,
  R -70..+40, Doppelschlag +-80, Biss +-30, nie hinter dem Baeren. Weiten ab Baerenmitte: Ankunft 1,5 < neu anrennen 1,725 <
  Hieb 1,8 < Doppelschlag 2,0; Biss 1,7 nur liegendes Hauptziel. Seitlich reicht der Doppelschlag bei 80 Grad 1,97 Kacheln neben
  die Mitte -- grosszuegig, Sache von Kevins Test (`NCBear_Tune("slamHalf", ...)`). Deckel 4/5/1 Ziele, je Angriff ein Treffer.
- **Abklingzeiten und Pause:** Im SP laeuft im Pausenzustand kein OnTick: `GameWindow.logic` Offset 406-491 ruft
  `states.update` nur bei `!GameTime.isGamePaused()`, und das ist im SP Spieltempo 0 (GameTime.isGamePaused 43-63). Die Uhr steht
  also, Fristen verfallen nicht. Schnelllauf/Schlaf: `getMultiplier` im Schlaf 200 x 30/FPS (Offset 18-35), die Uhr ist auf 0,5 s je
  Bild gedeckelt und laeuft dann langsamer als die Animation -- kein falscher Verfall. `perObjectMultiplier` ist zur OnTick-Zeit 1
  (MovingObjectUpdateSchedulerUpdateBucket.update 155-156), `multiplierBias` 1 (GameTime.<init> 33-35).
- **Kein Haengen** (ausser Fund 2): Ziel tot -> Suche, nach 3 s Ende; Baer tot/entladen -> uebersprungen, beim naechsten Scan
  raus; vom Spieler getroffen -> Kampf ab, Sperre los; 90 s Deckel; Steckenbleiben 3 s -> Ziel 20 s gesperrt; `NCBear_Fight(false)`
  und Lua-Fehler -> `releaseAll`, eine laute Zeile statt Stacktrace je Bild.
- **Mehrspieler: nichts, kein Kick.** OnTick nur bei `not isClient() and not isServer()` (onGameStart :666-669), `NCBear_Fight`
  verweigert im MP (:678-681), kein `sendClientCommand`, kein `setVariable`, kein Schaden. Der Server laedt `shared/`, tut aber
  nichts. Offenes MP ehrlich als offen markiert.
- **Ohne NPC Crew und ohne Bandits:** nur ModData-Felder und `getVariableBoolean("Bandit")` (false, wenn nie gesetzt); kein
  Aufruf in fremden Code. Dann ist jeder Zombie Ziel.

## Urteil

Die harte Regel haelt: kein Weg trifft Spieler, Crew, Neutrale, Tiere, Fahrzeuge, Kisten oder Leichen, Schaden und Umwerfen
sind belegt, der Mehrspieler bleibt still. Vor Kevins Test sollten Fund 1 (Treffer durch Waende) und Fund 2 (Geist-Ziel bis 90 s)
nachgebaut werden, beide mit belegten Einzeilern.
