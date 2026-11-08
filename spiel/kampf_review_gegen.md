# Baer kaempft - Gegenpruefung nach der Nachbesserung (adversarisch)

Stand 08.11.2026, PZ 42.21. Geprueft: `kampf_fix.md` und der ganze Bau unter
`_arbeit/baer_kampf/mod/42` gegen `NCBearTest/42`. Nur gelesen; eigene Laeufe: javap auf IsoGridSquare, IsoGameCharacter,
IsoAnimal, IsoZombie, BaseAnimalBehavior, AnimalDefinitions, IsoDoor (Ausgaben `_arbeit/baer_kampf/gegen/`), GLB-Clips mit
Python (`gegen/glb_anims.py`), wav-Kopfdaten, Attrappe neu (110/0), die vier Lua-Pruefer neu. Spiel nicht gestartet, nichts
gerendert, nichts kopiert. **Statisch geprueft, nicht gespielt.**

## Urteil

**Kein toedlicher, kein ernster Fund.** Die harte Regel haelt, die drei ernsten Funde der Vorpruefungen sind wirksam behoben,
im Mehrspieler laeuft nichts. Sieben kleine Funde, alle ohne Gegenstandsverlust, ohne Absturz und ohne Haenger; Fund 1 ist
der einzige, den ich vor Kevins Test noch nachbauen wuerde (ein belegter Einzeiler).

## Funde (alle klein)

1. **Offene Tueren und niedrige Zaeune sperren die Pranke** -- `NCBearFight.lua:201-207` (`canStrike`).
   `isSomethingTo` = isWallTo / isWindowTo / isDoorTo (Jar `IsoGridSquare.isSomethingTo(..,GetSquare)` 0-32). `isDoorTo` fragt
   nur das Tuer-Flag der Kante (`isDoor(GridSquareEdgeFacingDirection)` 46-63: `doorN`/`doorW`), **nicht ob sie zu ist**;
   `isWall` ist `collideN`/`collideW` ohne Fenster (46-82), also auch niedrige Zaeune. Folge: ein Zombie auf der Tuerkachel
   einer OFFENEN Tuer (der typische Engpass, durch den Zombies ins Haus kommen) ist fuer den Baeren auf der anderen Seite der
   Kante unangreifbar; der Baer rennt an, kommt nicht naeher, nach 3 s Sperre 20 s. `kampf_fix.md` nennt nur "Wand, Tuer,
   Fenster". **Reparatur (belegt, gleiche Typen IsoGridSquare/IsoGridSquare):** Vanillas eigene Greif-Frage
   `bsq:isBlockedTo(zsq) or bsq:isWindowTo(zsq)` (`client/TimedActions/ISInventoryTransferAction.lua:598`, auch
   `ISGrabItemAction.lua:16`) statt `isSomethingTo`. Jar: `isBlockedTo` = isWallTo / isWindowBlockedTo / isDoorBlockedTo /
   isStairBlockedTo (0-40), `isDoorBlockedTo` -> `IsoDoor.isBlocked()` = nicht offen ODER verbarrikadiert (0-19). Damit: offene
   Tuer frei, geschlossene Tuer, Wand, jedes Fenster gesperrt. Zaeune bleiben gesperrt (isWallTo) -- das ist Kevins Wahl.

2. **Pendeln an unerreichbaren Zielen** -- `NCBearFight.lua:600-603` (Steckenbleiben) mit `pickTarget` :218-246.
   Stehen Zombies hinter einem Zaun oder an Fenstern (sichtbar: `CanSee` ist `LosUtil.lineClear`, Zaun und Fenster lassen die
   Sicht durch), nimmt der Baer alle 3 s das naechste, sperrt es 20 s, bis `fightMax` (90 s), ruht 20 s und beginnt mit
   Bruellen neu. Kein Haenger (Deckel 32, Fristen), aber sichtbar ziellos. **Vorschlag:** Zaehler je Kampf (`B.stucks`, in
   `startFight` auf 0); beim dritten "stuck on the way" `endFight(B, "targets unreachable", F.T.restAfter)`.

3. **Kosten der Suche: ein Listendurchlauf je ruhendem Baeren, alle im selben Bild** -- `:633-646`, `:644-647` mit
   `searchNow` aus `tickBody` :751-756. Jeder Baer in Ruhe/Suche laeuft alle 0,5 s die ganze `getZombieList()` (je Zombie
   `get`, `getX`, `getY`), und weil `searchNow` fuer alle gilt, faellt alles in EIN Bild. Spez 5.4 verlangt "einmal je 0,5 s
   fuer alle Baeren". Bei 1-2 Baeren unkritisch; bei 8 Baeren und ~1000 Zombies rund 24.000 Java-Aufrufe in einem Bild
   (geschaetzt, nicht gemessen) -- ein Ruckler alle 0,5 s. **Vorschlag:** Suchtakt je Baer versetzen (`B.nextSearch` mit
   Versatz i x 0,5/8) oder ein gemeinsamer Durchlauf mit Vorfilter je Baer.

4. **Leine und Baum werden still geloest** -- `goApproach`/`updateApproach` :585, `endFight` :327 (`fleeTo`). Jar
   `IsoAnimal.fleeTo` 0-40: `getAttachedPlayer` -> aus der Liste des Spielers, `setAttachedPlayer(null)`, `setAttachedTree(null)`.
   Erreichbar nur mit dem Tier-Cheat im Debug: der Baer hat kein `canBeAttached` (NCBearDefs; Jar `AnimalDefinitions` liest den
   Schluessel nur, wenn er da ist), das Menue zeigt "Anbinden" nur mit `canBeAttached` oder `AnimalContextMenu.cheat`
   (`ISAnimalContextMenu.lua:173`). **Vorschlag:** keinen Kampf beginnen, solange `a:getData():getAttachedPlayer()` oder
   `getAttachedTree()` gesetzt ist (`ISAnimalContextMenu.lua:173/188/193`), oder in die Anleitung.

5. **Biss nach dem Hieb geht oft ins Leere** (Beobachtung, kein Fehler) -- `F.ChooseAct` :378, `ApplyHit` :459.
   `lying` = `isProne` (nur ZombieOnGroundState) oder "onground"; waehrend des Fallens ist beides falsch, und am Boden bleibt ein
   Zombie nur rund 0,5-1,5 s (Countdown Rand(60)+30 Bilder, CLAUDE.md v1.8.2). Die Wahl kommt ~1,0 s nach dem Treffer, der Biss
   trifft 0,54 s spaeter: oft faellt er noch (dann Hieb statt Biss) oder steht schon (dann verwirft `ApplyHit` den Biss
   richtig). "Hieb + Biss = tot" (Spez 5.3) wird selten; zwei Hiebe toeten trotzdem. Nur Kevins Test.

6. **Abschluss-Kopie: Spielpruefung fehlt in der Kopierregel** -- `kampf_fix.md` "Abschluss-Kopie". Vor dem Kopieren
   `tasklist | grep -i ProjectZomboid`; laeuft das Spiel, nicht kopieren und Kevin fragen (Schreiben in `Zomboid\mods` laesst
   das Hauptmenue die Modliste neu lesen, CLAUDE.md Abschnitt 2; Lua und GLB gelten erst nach Neustart). Sonst stimmt die
   Liste: nur hinzufuegen/ueberschreiben; `NCBearDefs.lua` weicht nur im Tonblock ab (diff), `mod.info` nur in der Beschreibung.

7. **Sperre der Engine im Schlaf** (nur notiert) -- Jar `BaseAnimalBehavior.wanderIdle` 0-39 zaehlt `blockedFor` mit dem rohen
   `getMultiplier` hoch und loest bei 8000; `setBlockMovement(true)` setzt den Zaehler NICHT zurueck (0-24, nur `false` tut es).
   Bei Tempo 1 reicht das fuer ~167 s (laenger als `fightMax`), im Schlaf (Multiplikator ~100 je Bild) nach ~80 Bildern: dann
   koennte er mitten im Angriff loslaufen, `fleeStop` haelt ihn je Bild an -- Zucken, kein Haenger.

## Geprueft und in Ordnung

- **Ziele:** nur `getZombieList()` (ArrayList<IsoZombie>), dazu `instanceof`; tot, KillDone, Leben <= 0, gezogene Leiche,
  scheintot, im/unter Fahrzeug, andere Ebene, NPC-Crew-Marke `tcUid` (Guardian.lua:1298, BaseSweep.lua:848), `recruited`,
  `npcNeutral` (Interact.lua:1439, Guardian.lua:7274), `npcUid`, Programm `NPC*`, `loyal` vor `hostile`/`hostileP`
  (`Bandit.IsHostile`, Bandit.lua:599-605). Bandits banditisiert JEDEN Koerper beim ersten Update unabhaengig vom Abstand
  (BanditUpdate.lua:2161-2166, der "distant"-Zweig :2208 kommt danach) -- kein Fernfenster, in dem ein Begleiter als Zombie
  gilt. NPC Crew enthaelt kein `NCBear` (grep 0), keine Namensgleichheit mit `NCBearSpawn/Test/Size/AttackProbe`.
- **Neue Aufrufe des Fixers:** `getCurrentSquare`, `isSomethingTo(IsoGridSquare)` (Bandits BanditUpdate.lua:1203-1206 gleiche
  Typen), `getVehicle`, `isUnderVehicle` (BanditMenu.lua:162-163; Jar: zwei bis vier Chunks, deren Fahrzeugliste, billig),
  `CanSee` (Jar IsoGameCharacter 0-61, von IsoPlayer/IsoAnimal nicht ueberschrieben). Gleiche Kachel -> `isSomethingTo` false.
- **Geist-Ziel:** `getCurrentSquare() == nil` plus `dropVanished` (ein Durchlauf, frueher Abbruch, Sprung > 8); ein auf nil
  gesetztes Ziel fuehrt in jeder Phase sauber nach `goSeek` (decide, updateApproach, ApplyHit mit `main = false`).
- **Haengen:** jede Phase hat einen Ausgang (Frist Dauer + 1 s, 3 s ohne Ziel, 90 s, Leine 25, getroffen, aus, Lua-Fehler ->
  `releaseAll`); jede Sperre wird geloest (endFight, releaseAll, scanBears beim Verschwinden). Kein Hunger (Spez 6, Multiplikator
  0), also kein falsches "hurt". Zwei gleiche Angriffe in Folge nur beim Biss, Pause >= 0,3 (Seiten wechseln immer).
- **Clips:** GLB 10 Clips, `NCBear_Rear/SwipeL/SwipeR/Slam/Maul` 3,0/1,1/1,1/2,2/1,6 s = `F.ACTS` = `m_AnimName`; 26 Knochen mit
  `Bip01_Jaw`; MD5 GLB `2e9a6d17...`, PNG `58a4ea41...` = Bericht. Treffer 0,462/1,254/0,544 s = Knoten-XML.
- **Toene:** sechs wav mono 44,1 kHz 16 bit (Roar 1,18 s), Namen Skript = Datei = XML = Rasse; Vanilla-Namen alle vorhanden
  (SledgehammerSwing/Hit, MacheteHit, ZombieBite, HeadSmash, AttackStomp, AnimalFoleyBuckBodyfall). Hoechstens 2 Treffertoene.
- **Pruefer:** luacheck 0, scopecheck 0, localcount max 57, luacheck_pz nur 2 x W113 auf `NCBearFight`; LF, ASCII, ohne BOM.
- **Beide Modi:** Einzelspieler alles; Mehrspieler kein OnTick (`isSP`), `NCBear_Fight` verweigert, kein Paket, kein Schaden,
  kein `setVariable`. Im MP aendert sich nur, dass ein getroffener Baer `NCBear_Pain` spielt (Rassenton). Offen ehrlich markiert.

Statisch geprueft, nicht gespielt.
