# Lauf baer-b1c: Forschung (B1c, Punkte 1-10)

Stand 11.11.2026 Nacht. **Statisch gelesen, nichts gebaut, nichts gespielt.** Rolle: Forschung (kein Code im Staging).
Jede Laufzeit-Aussage ohne Spielbeleg ist "ungeprueft".

Schreibweise wie `forschung_b1b.md` (kurz `FB1B`):
- `V:` = Vanilla-Lua `.../ProjectZomboid/media/lua/` (42.22.2). `B:` = Bandits `.../Bandits/42.22/media/lua/`, `Bc:` = `.../Bandits/common/media/`.
- `NC:` = NPC Crew `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua/` (nur Lernquelle, kein Engine-Beleg, nichts kopieren).
- `T:` = Test-Mod `C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/lua/`. `S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/` (B1b).
- `dec/`, `dec_b1b/` = Vineflower-Auszuege 42.22.2 (`_arbeit/baer_zaehmen/`). **NUR JAR** = Lesehilfe, kein Engine-Beleg.
- **BELEGT** = echter Aufruf in Vanilla-Lua oder Bandits mit gleichen Argumenttypen. **ERLAUBT** = Kevins Wort je Methode:
  `animal:pathToLocation(x, y, z)` (08.11., `forschung_engine.md:627`) und `animal:setVariable("animalRunning", false)` (11.11.,
  `baer/begleiter/ENTSCHEIDUNGEN.md:282`).
- Hinweis Zeilen: die Bandits-Belege in `T:shared/NCBearFight.lua` nennen `ZAMove.lua:31/:60`; im heutigen Bandits 42.22 stehen sie
  bei **`B:shared/ZombieActions/ZAMove.lua:32`** (`zombie:setVariable("bPathfind", true)`) und **`:61`**
  (`zombie:getVariableBoolean("bPathfind")`). Vanilla `ISMilkAnimal.lua:139` (`self.character:setVariable("milkanimalout", false)`).

---

## 0. Kernbefunde vorweg

1. **Ein Client kann die ModData eines Tiers am Server ueberschreiben oder loeschen** (Jar `dec/ObjectModDataPacket.java:21`
   `requiredCapability = Capability.LoginOnServer`, `:41-63` `object.getModData().load(...)` bzw. `wipe()`, ausdruecklich auch
   `IsoAnimal` `:65`). Der Spiegel `tcBear` ist im MP also nie vertrauenswuerdig -- Heilung nur, "wenn kein Eintrag widerspricht",
   mit Deckeln und Log (1.4). Im SP gibt es keinen Fremden: Spiegel voll vertrauen.
2. **Rennen allein macht laut Jar KEINEN Tier-Laerm.** Schritte gehen ueber die 12-Argument-Form von `addSound` mit
   `stressHumans = false` und `stressAnimals = false` (`dec_b1b/IsoGameCharacter.java:5506-5521`, Ueberladung
   `dec/WorldSoundManager.java:77-93`), `getSoundAnimal` nimmt aber nur Laerm mit `stresshumans || stressAnimals`
   (`dec/WorldSoundManager.java:259`). Es fliehen also: Q-Ruf (`stressAnimals = true`, `dec_b1b/IsoGameCharacter.java:5019-5034`),
   Husten (`:15171`, Radius 35, stressHumans), Schuesse und Zombie-Schlaege (`_arbeit/baer_laerm/bau_bericht.md:11-14`). Was Kevin
   "beim Rennen" sah, war vermutlich einer davon oder das Hinterherrennen selbst -- im Test mit Log ansehen (Frage F9).
3. **Laerm-Flucht abfangen geht nur pro Bild beim Schreiber** (SP-Programm / Server; `respondToSound` laeuft nur dort,
   `dec/IsoAnimal.java:419-439`). `OnTick` ist am Server belegt (`V:server/Foraging/forageServer.lua:502`). Die Engine hat ein
   "Schild": solange das Tier sich bewegt und den Laerm gemerkt hat, flieht es nicht neu (`dec/IsoAnimal.java:765-769`). Ein
   **eigener kurzer Ersatzweg** ersetzt die Flucht und wird vom Schild geschuetzt -- einfacher als der Halt des grossen Baeren (2.3).
4. **Die Bewegungssperre haelt Laerm-Flucht NICHT auf** (`pathToLocation` und die Bewegungszustaende fragen `blockMovement` nicht:
   `dec/IsoAnimal.java:2651-2667`; grep "block" in `dec_b1b/AnimalPathFindState.java`/`AnimalWalkState.java`: 0) und jede Erneuerung
   der Sperre (`setBlockMovement(true)` ruft `stopAllMovementNow`, `dec/BaseAnimalBehavior.java:1739-1747`) loescht das Schild wieder.
   B1b erneuert die Sperre in jedem Hirn-Takt (`S:server/BanditsNPCBearFollow.lua:141-143`, `S:server/BanditsNPCBearWorld.lua:473-483`).
5. **Zombies sieht das Junge heute gar nicht:** mit `fleeZombies = false` (`S:shared/BanditsNPCBearDefs.lua:91`) ueberspringt die
   Engine den ganzen Zombie-Zweig (`dec/BaseAnimalBehavior.java:1580`). Zombies finden: `getCell():getZombieList()` -- in Vanilla-Lua
   **0 Treffer**, belegt nur in Bandits (SP/Server `B:server/BanditSave.lua:15`, `:46`; Server `B:server/BanditServerWanderers.lua:651`;
   Client `B:client/BanditZombie.lua:110`). Im SP mit Bandits billiger: `BanditZombie.CacheLightZ` (reine Lua-Tabelle mit x/y/z,
   `B:client/BanditZombie.lua:60-87`), am MP-Server gibt es diesen Cache nicht (`:46` `if isServer() then return end`).
6. **Mitfahren eines Tiers geht mit unseren Belegen nur wie bei NPC Crew: entfernen und neu erzeugen** (`B.RemoveCub` /
   `B.CreateCub`, `S:server/BanditsNPCBearWorld.lua:225-262`). Vanillas Tier-Anhaenger braucht ein Fahrzeug mit `getAnimalTrailerSize() > 0`
   (`V:client/Vehicles/ISUI/ISVehicleMenu.lua:301`, `:667`) -- nicht "jedes Auto". Ein Teleport (`setX/setY` am Tier) hat keinen Beleg.
   **Pflicht: eine Generationszahl im Register UND im Spiegel**, sonst entsteht nach Absturz/Neuladen ein Doppel (4.5).
7. **Vanilla-Luecke:** jeder Spieler kann JEDES Tier in 6 Kacheln um einen Tier-Anhaenger einladen -- ohne Besitzfrage
   (`V:client/Vehicles/ISUI/ISVehicleMenu.lua:777-800`); unser Junges passt (trailerBaseSize 100 x Groesse 0,35,
   `S:shared/BanditsNPCBearDefs.lua:87`; Kuh 400, `V:shared/Definitions/animal/CowDefinitions.lua:229`). Danach fehlt es dem Register.
   Nicht B1c, aber Frage F7.
8. **Bandits-Markierung:** `BanditEventMarkerHandler.set(id, icon, dauer, x, y, farbe, text)` (`B:client/BanditEventMarkerHandler.lua:6-38`);
   gleiche Id = verschieben, Dauer 0 = unsichtbar (`B:client/BanditEventMarkers.lua:135-140`); Symbol 96 x 96 (`:7`, unsere Datei ist
   96 x 96, nachgemessen). **Alle Markierungen teilen EINE gemerkte Bildschirmstelle** (`BanditEventMarkerHandler.lua:17-23`, Spieler-ModData
   `BanditEventMarkerPlacement`) -> unser Pfeil liegt genau auf NPC Crews Ueberlebenden-Pfeil, wenn beide da sind (Frage F5).
9. **Karte:** Vanilla zeichnet Kartensymbole selbst genau so: `worldToUIX/Y(x, y)`, um die halbe Groesse versetzen,
   `drawTextureScaledAspect(tex, x, y, w, h, a, r, g, b)` (`V:client/ISUI/Maps/ISWorldMap.lua:478-482`). Groesse dort nach Zoom
   32-64 px (`:446-449`).
10. **Mod-Optionen:** `PZAPI.ModOptions:create(id, name)` mit `addTickBox`/`addComboBox`/`addSlider` (`V:client/PZAPI/ModOptions.lua:64`,
    `:121`, `:206`, `:247`), gespeichert je Rechner in `ModOptions.ini` (`:259-290`, geladen `V:client/OptionScreens/MainOptions.lua:2791`).
    Namen/Tooltips gehen durch `getText` (`MainOptions.lua:2810-2812`, `:3020`) -> Schluessel uebergeben. Text skaliert nur stufig
    (Schriften Small/Medium/Large) oder per `drawTextZoomed` (Grenzfall, 9.3).

---

## 1. N9 Register-Selbstheilung (Auftrag 1)

### 1.1 Was heute passiert (Beleg Kevins Fall)

- Register = globale ModData `TrueCompanionsBears` beim Schreiber (`S:server/BanditsNPCBearRegistry.lua:66-120`), Spiegel am Tier
  `md.tcBear = { id, st }` (`S:shared/BanditsNPCBear.lua:27`, geschrieben `S:...Registry.lua:197-198` und `:279-300`).
- Fehlt der Eintrag: `B.RecOf` legt `NewRec("found")` an (`S:...Registry.lua:225-241`) -- neuer Eintrag, Zustand "shy", neue Id, und
  `NewRec` UEBERSCHREIBT den alten Spiegel (`:197-198`). Der Suchlauf laesst ein zahmes Tier ohne Eintrag liegen (`S:...World.lua:387-408`).
- `reg.n` beginnt bei leerem Register wieder bei 0 (`S:...Registry.lua:75`, `:171-172`) -> **Id-Kollision**: Kevins neues Wald-Junges
  bekam "b1", waehrend das alte zahme Tier noch den Spiegel "b1" trug (`baer/STAND.md:52-58`).
- Folge fuer Kevins laufenden Spielstand (Schluss, ungeprueft): der alte Spiegel ist durch `b2` ersetzt; die Zaehmung steht nur noch in
  `Saves/Apocalypse/2026-11-10_22-12-12_crash/global_mod_data.bin`. Die Heilung wirkt erst fuer kuenftige Verluste.

### 1.2 Engine-Grundlagen

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Spiegel lesen/schreiben | `animal:getModData()` (Tabelle) | schreiben `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127`; lesen `V:shared/Definitions/animal/ButcheringUtil.lua:596` | Schreiber | **BELEGT** (B1a) |
| Spiegel bleibt beim Speichern | (kein Aufruf) | Jar `IsoAnimal.save` schreibt ModData (`forschung_engine.md:113`); Spielbeleg indirekt `baer/STAND.md:56-57` | - | belegt genug |
| Spiegel ist im MP manipulierbar | (Client-Paket) | NUR JAR `dec/ObjectModDataPacket.java:21`, `:41-63`, `:65` | Client -> Server | **Gefahr**, siehe 1.4 |
| Register-Generation stempeln | `getTimestampMs()` als Zahl | `V:server/Foraging/forageServer.lua:456` | Schreiber | **BELEGT**; alternativ `ZombRand(n)` (`V:shared/TimedActions/Animals/ISMilkAnimal.lua:25`) |
| AnimalID als Gegenprobe | `animal:getAnimalID()` | nur Client `V:client/ISUI/Animal/ISAnimalUI.lua:53` | Schreiber | wie B1a: A3, MP offen |
| Zaehlen/Deckel | `B.SlotsOf`, `B.Opt("BearMaxPerPlayer")`, `B.CFG.maxRecs` | `S:...Registry.lua:245-275`, `S:shared/BanditsNPCBear.lua:45`, `:87` | Schreiber | eigener Code |

### 1.3 Vorschlag Spiegel v2 und Heil-Regeln (Planer entscheidet)

Spiegel `tcBear` (nur Zahlen/Texte, kein Objekt):
`{ v = 2, ep, id, nr, gen, r, st, src, finder, bond, owner, tame, fedN, petN, feedAt, petAt, tamedAt, mode, name, hx, hy, hz }`
- `ep` = Register-Generation (beim ersten `InitRegistry` einmal gestempelt, z. B. `getTimestampMs()` als Text). `nr` = Zaehlerstand der Id.
  `gen` = Koerper-Generation des Eintrags (+1 bei jedem Einsteigen und jedem Neu-Erzeugen, Abschnitt 4/5). `r` = Aenderungszaehler
  (in `B.Commit` +1) -- dann vergleicht `markProbe` (`S:server/BanditsNPCBearServer.lua:681-685`) nur `id`, `st`, `r`, nicht alle Felder.
- Schreiben: `B.NewRec` (sofort, ohne `isExistInTheWorld`, wie heute `:193-198`) und `B.Commit` (`:279-300`). Ein alter v1-Spiegel wird
  beim ersten Takt durch `markProbe` auf v2 gebracht (er weicht in `r` ab).

Heil-Regeln (Reihenfolge, beim Schreiber; Orte: `B.RecOf` beim Anfassen und `B.ScanAnimals` beim Suchlauf):
1. Objekt dieser Sitzung (`B._s[id].obj == o`) -> gebunden (Riegel 1 aus B1b, `S:...World.lua:372-386`). Unveraendert.
2. `reg.cubs[mark.id]` da, gleiche AnimalID, kein anderes lebendes Objekt -> binden (B1a). Unveraendert.
3. **Widerspruch** (`reg.cubs[mark.id]` da, aber anderes lebendes Objekt ODER andere AnimalID):
   - `mark.ep ~= reg.ep` -> Spiegel aus einem frueheren Register (Kevins Fall): **wiederherstellen unter NEUER Id** (Regel 4, Zaehler
     `reg.n + 1`), Spiegel neu schreiben.
   - `mark.ep == reg.ep` und `mark.gen < rec.gen` -> **veraltete Kopie** (vor dem Einsteigen/Herholen gespeichert): nie binden; entfernen
     ueber `B.RemoveCub`, wenn unbeobachtet (Riegel 3 der Waisen: `vanishKeep`, `B.SeenInSP`, `S:...World.lua:305-312`).
   - sonst (gleiche Generation, beide leben) -> **Doppel** (Engine-Doppel oder Faelschung): nie einen zweiten Eintrag; das gebundene Tier
     bleibt, das andere wie eine Waise behandeln (Alter + unbeobachtet). Log-Zeile.
4. **Kein Eintrag** zu `mark.id`, Spiegel v2 gueltig -> **wiederherstellen**: gleicher Zustand (`missing` -> `tame`, das Tier lebt ja),
   gleicher Besitzer/bond/finder, Balken/Zaehler/Zeiten, `mode`, `name` nur durch `B.CleanName`; Id = `mark.id`, wenn frei, sonst neu;
   `reg.n = max(reg.n, mark.nr)` (**Zaehler nachziehen**). Deckel: `maxRecs`; `owner` hat schon `BearMaxPerPlayer` Baeren bzw. `bond`
   schon ein gebundenes Junges (`slots.bonded`, `S:...Registry.lua:258-259`) -> NICHT als tame/fed herstellen, sondern B1a-Weg ("found")
   mit Log. `st` new/shy aus DEMSELBEN Register (`mark.ep == reg.ep`) -> wie heute "stale" (weitergezogen, `S:...World.lua:389-393`).
5. v1-Spiegel ohne Besitzer: SP -> Besitzer `__sp` (der einzige Schluessel, `S:shared/BanditsNPCBear.lua:283-291`); MP -> nicht herstellbar,
   B1a-Weg + Log.
- Wann: der erste Hirn-Takt laeuft einen Suchlauf (Waisen-Takt bei `B._orphAt == nil`, `S:server/BanditsNPCBearServer.lua:915-918`),
  danach alle 120 s. Vorschlag: solange das Register leer ist oder in den ersten 2 Minuten nach `InitRegistry` je 15 s suchen
  (Zellen laden nach). Damit kommt die Heilung meist VOR dem naechsten Wald-Wurf (Langsam-Takt `EveryTenMinutes`,
  `S:...Server.lua:939`) -- Reihenfolge ungeprueft.

### 1.4 Fremdmanipulation im MP (ehrlich)

- Ein veraenderter Client darf per `ObjectModDataPacket` die ModData jedes Tiers ersetzen oder leeren (NUR JAR, 0.1). Folgen:
  (a) Spiegel eines gebundenen Jungen geloescht/verfaelscht -> harmlos (Regel 1 + `markProbe` schreibt neu).
  (b) Gefaelschter Spiegel auf einem **ungebundenen** Jungen (Waise, oder nach Registerverlust) -> Regel 4 wuerde es dem Faelscher geben.
- Was schuetzt: Regeln 2/3 (Eintrag widerspricht), Deckel je Spieler, Log. Eine Unterschrift `sig = hash(geheim, ep, id, owner, st)`
  waere faelschungssicher, aber das Geheimnis muesste ausserhalb der globalen ModData liegen (die ist im Absturzfall mit weg):
  `getFileWriter(name, true, false)` ist in shared belegt (`V:shared/Foraging/forageSystem.lua:681`), `getFileReader(name, true)` nur
  im Client (`V:client/Entity/ISEntityUI.lua:679`) -> am Server unbelegt. **Empfehlung:** B1c ohne Unterschrift, MP-Heilung mit Deckeln
  und einer Log-Zeile je Heilung; Unterschrift ist Frage F1.

---

## 2. Laerm (Auftrag 2)

### 2.1 Engine (NUR JAR, `dec/IsoAnimal.java:764-806`, aufgerufen je Update beim Schreiber `:439`)

- Gemerkter Laerm + `timeSinceFleeFromSound > 0` + `isAnimalMoving()` (Walk/PathFind/FollowWall, `:1949-1953`) -> **keine neue Flucht**
  ("Schild", `:765-769`). Sonst loslassen und neu bewerten.
- Neuer Laerm (Radius x1 fuer nicht wilde, `dec/WorldSoundManager.java:259-263`, `:380-382`), nicht Radio/Fernseher, und fuer nicht
  wilde nicht vom Fahrzeug (`:781-782`):
  - Quelle ist ein rufender Spieler mit Engine-Akzeptanz >= 40 -> `pathToLocation` ZUM Spieler (`:783-784`), sonst
  - Flucht `radius + 10` Kacheln weg, `timeSinceFleeFromSound = 2000 x radius`, **`changeStress(radius x 0,05)`**,
    `animalRunning = true`, `pathToLocation` (`:786-801`).
- Laerm lebt 16 Bilder (`T:shared/NCBearFight.lua:180`, `_arbeit/baer_laerm/forschung_laerm.md`), am MP-Server in Server-Ticks (Dauer in
  Sekunden ungeprueft).
- Wandern im Stand setzt `animalRunning = false` (`dec/BaseAnimalBehavior.java:167`); `periodicRun` hat das Junge nicht (Def ohne Feld,
  `S:shared/BanditsNPCBearDefs.lua:67-104`) -> **wanderndes Junges geht, fliehendes rennt** -> gutes Unterscheidungsmerkmal.

### 2.2 Wie der grosse Baer es macht (`T:shared/NCBearFight.lua:28-38`, `:1015-1190`; Berichte `_arbeit/baer_laerm/bau_bericht.md`,
`fix_bericht.md`; **in NCBearTest seit 08.11., ungespielt**, `baer/STAND.md:288`; nur SP)

- Je Bild (`OnTick`): Aktionszustand lesen (`a:getActionStateName()`, `B:shared/ZombieActions/ZASmack.lua:486`), dazu im idle-Bild
  `a:getVariableBoolean("bPathfind")` (`B:...ZAMove.lua:61`). pathfind/walk ohne eigenen Befehl = Fluchtbefehl.
- **Halt** je Fluchtbefehl: `stopAllMovementNow()` (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:760`) + `setVariable("bPathfind", true)`
  (`B:...ZAMove.lua:32`) -> die KI steht mit einer Anfrage zum eigenen Standort in AnimalPathFindState = Schild an, ohne Bewegung;
  `fleeWait` 18 Bilder (> 16 Bilder Laerm), Ende vor WalkingOnTheSpot (30 getMultiplier ~ 0,63 s, sonst schickt die Engine ihn zur
  Kachelmitte); Dauerlaerm-Sonderfall ("lauter Halt"), Deckel 3 Erneuerungen/240 Bilder (`:184-189`, `:1097-1190`).
- Im **Anlauf** dagegen: fremden Weg erkennen und durch den eigenen ersetzen -- "das Schild schuetzt dann unseren Weg" (`:31-33`,
  `:198-203`).
- Grund fuer den Aufwand dort: der Angriffs-Clip darf nicht neu starten. **Das Junge hat keinen Clip, der weiterlaufen muss.**

### 2.3 Uebertragung auf das gezaehmte Junge (Vorschlag)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Takt je Bild beim Schreiber | `Events.OnTick.Add(f)` | Server `V:server/Foraging/forageServer.lua:502`; S: schon `S:...Server.lua:940` | SP + Server | **BELEGT** |
| bewegt es sich? | `a:getActionStateName()` == "walk"/"pathfind"/"followwall" | `B:shared/ZombieActions/ZASmack.lua:486`; am Tier `T:shared/NCBearFight.lua:1099` | Schreiber | **BELEGT** (Methode, Text) |
| Fluchtbefehl im selben Bild (Animation noch idle) | `a:getVariableBoolean("bPathfind")` | `B:shared/ZombieActions/ZAMove.lua:61`; am Tier `T:...NCBearFight.lua:1168` | Schreiber | **BELEGT** |
| rennt es? (Flucht rennt, Wandern geht) | `a:getVariableBoolean("animalRunning")` | gleiche Methode/Typ wie oben; dass der Text-Name denselben Speicher trifft wie die Engine-Kennung: NUR JAR (`dec_b1b/IsoGameCharacter.java:12200-12256`, FB1B 1.1) | Schreiber | **BELEGT** (Methode), Wirkung Jar |
| Bestaetigung: Stress-Sprung | `a:getStress()` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:17` | Schreiber | **BELEGT**; Flucht = +radius x 0,05 x (1 + Gen "stress") (`dec/IsoAnimal.java:799`, `:2348-2357`), sonstige Zunahme je Bild ~0,001 (`dec/BaseAnimalBehavior.java:1560-1562`, `:1693-1696`) |
| Ersatzweg gehend | `a:setVariable("animalRunning", false)` dann `a:pathToLocation(x, y, z)` | **ERLAUBT** (beide); Reihenfolge wie Vanilla-Wandern `dec/BaseAnimalBehavior.java:167`, `:224` | Schreiber | ok |
| Ersatzweg rennend (Folgen) | `a:fleeTo(sq)` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38`; S: `B.MoveTo` `S:...World.lua:493-526` | Schreiber | **BELEGT** |
| sofort stehen | `getBehavior():setBlockMovement(true)` (ruft `stopAllMovementNow`) | `V:shared/TimedActions/Animals/ISPetAnimal.lua:36`; Jar `dec/BaseAnimalBehavior.java:1739-1747` | Schreiber | **BELEGT**; loescht aber das Schild |
| Stress ausgleichen | `a:changeStress(x)` | `V:...ISMilkAnimal.lua:28` (nur POSITIVE Werte) | Schreiber | negativ = Grenzfall; `petAnimal` senkt Stress -7..-11 (`forschung_engine.md:499`). Frage F2 |

Ablauf (nur `st == "tame"`, lebendes Objekt, nicht mitfahrend; Deckel z. B. 8 Junge je Bild; wild/scheu/angefuettert: nichts):
1. Je Bild: bewegt (Zustand oder `bPathfind`) UND `animalRunning == true` UND kein eigener Befehl in den letzten `ownMs` (~400 ms; wir
   merken `s.moveAt`, `S:...World.lua:516`) -> **fremde Flucht** (oder Q-Ruf mit Akzeptanz >= 40 zum Spieler -- harmlos). Zusatz: Stress
   stieg seit dem letzten Bild um mehr als ~0,04 -> sicher Laerm.
2. Antwort SOFORT im selben Bild, ohne die Drossel `followMoveMs`/`moveMs`:
   - "follow" und Besitzer da: der Folgen-Laufbefehl (rennen) zum Folgen-Ziel (wie `B.FollowStep` Regel 16).
   - sonst (Bleiben, Halten neben dem Besitzer): **gehender Ersatzweg** 1,5-2 Kacheln Richtung Besitzer bzw. Heimat (nie die eigene
     Kachel: Ankunft sofort = Schild weg). Bei 0,52 Kacheln/s (FB1B 0.3) dauert er 3-4 s und deckt die Laerm-Lebensdauer ab.
3. Waehrend `s.calmUntil` (~2,5 s) die Sperre NICHT erneuern (`B.Hold`/`FollowStep` Regel 14 sonst `stopAllMovementNow` -> Schild weg,
   0.4) -- wie der grosse Baer "nicht mitten in einem Halt erneuern" (`T:...NCBearFight.lua:473-474`).
4. Dauerlaerm: hoechstens eine Flucht je Ersatzweg (Schild), Stress +radius x 0,05 je Schlag bleibt (Engine). Zaehler/Diagnose hinter `B.Log`.
5. Kosten: je zahmem Jungen und Bild 1-2 Java-Aufrufe (Zustand, ggf. 1 Variable); `getStress` nur bei Verdacht.
- Alternative (gespielte Form gibt es nicht): der Halt des grossen Baeren (2.2). Mehr Code, ebenfalls nur Jar-abgeleitet; fuer das Junge
  nicht noetig.
- **Ungeprueft:** Reihenfolge `OnTick` <-> Tier-Update am dedizierten Server (im SP kommt OnTick nach dem Uebergang, bau_bericht 1);
  wie viele Server-Ticks ein Laerm lebt; ob die Flucht am Client (Kopie) einen Ruck zeigt, bevor das naechste Tierpaket kommt
  (Pakete alle 800 ms, FB1B 0.1).

---

## 3. Zombies (Auftrag 3)

### 3.1 Zombies finden

| Weg | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Zellenliste | `getCell():getZombieList()`, `:size()`, `:get(i)` | `B:server/BanditSave.lua:15`, `:46` (Riegel `if isClient() then return end`, also SP + Server), `B:server/BanditServerWanderers.lua:651` (Server), `B:client/BanditZombie.lua:110`; am Tier-Code `T:shared/NCBearFight.lua:1202` | SP + Server | **BELEGT (Bandits)**, Vanilla 0 Treffer. Keine Kopie (anders als `getObjectListForLua`) |
| Lage | `z:getX()/getY()/getZ()` | `B:client/BanditZombie.lua:66-69` | beide | **BELEGT** |
| lebt / echt | `z:isAlive()`; `z:isReanimatedForGrappleOnly()` | `B:server/BanditSave.lua:52`, `B:client/BanditZombie.lua:49`; `B:shared/BanditCompatibility.lua:187-189` (B42) | beide | **BELEGT** |
| Bandit (z. B. NPC-Crew-Figur) ausschliessen, SP | `z:getVariableBoolean("Bandit")` | `B:client/BanditZombie.lua:74` (gesetzt nur im Client-Code `B:client/BanditUpdate.lua:199`) | SP (Schreiber = Client) | **BELEGT**; am Server nicht gesetzt (ungeprueft) |
| Bandit ausschliessen, MP-Server | `GetBanditClusterData(BanditUtils.GetZombieID(z))` -> `gmd[id]` | `B:server/BanditSave.lua:19-21`, `:46-56` | Server | Bandits-Lua (Riegel: nur wenn Bandits da); ohne Bandits gibt es keine Banditen |
| SP billig | `BanditZombie.CacheLightZ` (id -> { x, y, z }) | `B:client/BanditZombie.lua:12`, `:60-87` (je `OnZombieUpdate` frisch, ohne Banditen) | nur SP/Client | Lua-Daten, kein Engine-Aufruf; am Server leer (`:46`) |
| Kacheln absuchen | `sq:getMovingObjects()` je Kachel | (S: nicht benutzt) | - | teurer als die Liste ((2r+1)^2 Kacheln) -> nicht nehmen |

Vorschlag: im Hirn-Takt (1,5 s) EIN Durchlauf ueber die Liste fuer alle geladenen Jungen zusammen (je Zombie Abstand zu jedem Jungen,
nur gleiche Ebene), Deckel `zedScanMax` (z. B. 1500 Eintraege je Takt, Rest im naechsten Takt). Schneller Takt (z. B. 500 ms) nur,
solange ein Zombie in `zedSense` steht. Im SP mit Bandits zuerst `CacheLightZ`.

### 3.2 Verhalten (Vorschlag, Stellwerte)

- gezaehmt, Zombie <= `zedHide` (6; Engine-Fluchtgrenze fuer Zombies ist 6, `dec/BaseAnimalBehavior.java:1701`), Besitzer da, gleiche
  Ebene, nicht im Fahrzeug, Abstand Junges-Besitzer <= `hideOwnerMax` (~10): **Verstecken** -- Ziel `O + (O - Z)/|O - Z| x hideGap`
  (~1,2 Kacheln hinter dem Besitzer, vom naechsten Zombie Z weg), rennen (`fleeTo`), dort halten; je Takt neu rechnen.
- sonst: **fliehen** -- Ziel `C + (C - Z)/|C - Z| x zedFlee` (~10), Kachel geladen/kein Wasser (`B.MoveTo` prueft beides, `S:...World.lua:503-513`).
- wild/scheu/angefuettert: fliehen (neue Regel VOR Regel 1 in `B.Decide`, `S:shared/BanditsNPCBearRules.lua:273-322`).
- Ende erst bei `zedSafe` (~9, Hysterese) plus kurzer Nachlauf, sonst laeuft ein "Bleiben"-Junges heim (Regel 8) mitten in die Zombies.
- `fleeZombies` bleibt `false` (sonst flieht die Engine selbst und kaempft gegen das Verstecken).

---

## 4. Mitfahren (Auftrag 4)

### 4.1 Was NPC Crew tut und was wir daraus lernen (nur gelesen)

| Lehre | NC-Stelle |
|---|---|
| Figur faehrt nie wirklich mit (Zombie im Sitz = Absturz); sie wird entfernt und als Roster-Eintrag `riding` gefuehrt, beim Aussteigen neben dem Besitzer neu gebaut | `NC:client/BanditsNPCPersistence.lua:7941-7947` |
| Einsteigen: nur folgend, Besitzer im Auto, nah am Auto (dist < 3 nach Hinlaufen) | `NC:shared/BanditsNPCPrograms.lua:1002-1034` |
| Vor dem Entfernen pruefen, ob die Rueckkehr sicher klappt, sonst zu Fuss bleiben | `NC:...Persistence.lua:8006-8017` |
| Im MP entfernt nur der Server (Client-Entfernen kommt nach 1 s zurueck) | `:8018-8056` |
| Das Verschwinden in der Welt ist die Bestaetigung, nicht die Antwort | `:8322-8387` |
| `getVehicle()` liefert im MP sekundenlang nil waehrend der Fahrt -> Aussteigen erst nach 3 s zu Fuss (SP 1 s) | `:8429-8449`, `:8576-8579` |
| Zweites Signal nur im MP: > 4 und < 80 Kacheln/s = faehrt | `:8190-8191`, `:8526-8555` |
| "riding" faellt erst, wenn wirklich ein Koerper zurueckkommt (sonst naechster Versuch) | `:8729-8737` |
| Auf einer freien Nachbarkachel bauen, nicht im Auto / unter dem Rumpf (`isVehicleIntersecting`) | `:8155-8183`, `:8710-8725` |
| Nur der Besitzer holt seine Mitfahrer heraus | `:8662-8669` |
| Frisch geladen mit riding-Eintraegen: sofort zuruecksetzen | `:8556-8561`, `:8612-8621` |
| Jeder Server-Befehl an einer geparkten Figur antwortet "parked" | z. B. `NC:server/BanditsNPCFarmServer.lua:666`, `NC:server/BanditsNPCDeathServer.lua:275` |
| Karte: Mitfahrer nicht zeichnen (Punkt laege unter dem Spieler) | `NC:client/ISUI/BanditsNPCMiniMap.lua:159-161` |
| `BanditsNPCVehiclePanel.lua` ist der Auto-Zonen-Reiter (Gegenstaende), hat mit dem Mitfahren nichts zu tun | `NC:client/ISUI/BanditsNPCVehiclePanel.lua:1-15` |

### 4.2 Was fuer ein Tier mit unseren Belegen geht

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Besitzer im Fahrzeug | `p:getVehicle()` | `V:server/Vehicles/VehicleCommands.lua:11`; S: `B.Players` `S:...World.lua:44-56` | Schreiber | **BELEGT**; MP-Aussetzer laut NC (4.1) -> entprellen |
| Tempo des Besitzers (zweites Signal) | Lagen je Takt `B._pp` | `S:...Server.lua:653-659`, `:897-899` | Schreiber | eigener Code |
| Junges entfernen | `B.RemoveCub(a)` = `setBlockMovement(false)`, `remove()`, am Server `removeAnimal(getOnlineID())` | `S:...World.lua:254-262` (Belege dort: `V:shared/Definitions/animal/ButcheringUtil.lua:609-614`) | Schreiber | **BELEGT** |
| neu erzeugen | `B.CreateCub(x, y, z)` = `addAnimal(...)` + `addToWorld()` | `S:...World.lua:225-245` (`V:server/ClientCommands.lua:809-810`, `V:client/DebugUIs/DebugContextMenu.lua:1460-1467`) | Schreiber | **BELEGT**. Neuer Aufrufer ausser `B.AppearFor` -> Kommentar `:10`/`:220` anpassen |
| neu binden | `B._s[id].obj = a`, `rec.aid = a:getAnimalID()`, Spiegel sofort (wie `NewRec` `S:...Registry.lua:192-198`) | `getAnimalID` nur Client-belegt (A3) | Schreiber | eigener Code |
| freie Kachel neben dem Besitzer | Ring 1..3: `getCell():getGridSquare`, `TreatAsSolidFloor`, Wasser, `isFree(false)`, `isVehicleIntersecting` (gleiche Belege wie `B.SquareFits` `S:...World.lua:93-106`), OHNE `isOutside` und OHNE `B.SeenInSP` (das Junge SOLL sichtbar neben dem Spieler stehen) | wie links | Schreiber | **BELEGT** (Teile). `AdjacentFreeTileFinder.Find(sq, p)` ist Vanilla-Lua in shared (`V:shared/Util/AdjacentFreeTileFinder.lua:135-184`), kennt aber keine Fahrzeuge und ist nur im Client aufgerufen -> eigener Ring besser |
| Vanilla-Anhaenger | `vehicle:addAnimalFromHandsInTrailer` u. a. | `V:shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:60-66`, nur Fahrzeuge mit `getAnimalTrailerSize() > 0` (`V:client/Vehicles/ISUI/ISVehicleMenu.lua:301`) | - | **nicht** "jedes Auto" -> nicht nehmen |
| Teleport des Tiers | `setX/setY` | kein Beleg am Tier | - | **nicht** nehmen |

### 4.3 Ablauf (Vorschlag)

- **Einsteigen** (Hirn-Takt): `st == "tame"`, `mode == "follow"`, Besitzer `car == true`, Abstand <= `rideDist` 15 (Kevin) ->
  `rec.ride = { at = B.Now() }`, `rec.gen = rec.gen + 1`, `B.Commit`, `B.RemoveCub(a)`, `B._s[id].obj = nil`. Weiter als 15 -> B1b-Regel 11
  (Bleiben + Meldung `Note_StayCar`). Ersetzt B1b-Regel 11 (`S:shared/BanditsNPCBearRules.lua:454`).
- **Waehrend der Fahrt:** `rec.x/y/z` = Lage des Besitzers (letzte bekannte Stelle fuer Karte und Notfall). Alle Befehle/Bitten an dieses
  Junge: "parked" (`Why_Riding`), auch Fuettern/Streicheln.
- **Aussteigen:** Besitzer da, `car == false` seit `offMs` (SP 1000, MP 3000, NC 4.1) und im MP kein Tempo > 4 Kacheln/s -> freie Kachel
  neben ihm (4.2) -> `B.CreateCub` -> neu binden, `rec.gen = rec.gen + 1` (Spiegel mit neuer gen), `rec.ride = nil`, `mode = "follow"`.
  Keine freie Kachel / Definition fehlt -> `ride` bleibt, naechster Takt (nichts haengt: Log je Zustandswechsel).
- **B1a/B1b-Wege ausnehmen:** ein Eintrag mit `ride` hat kein Objekt -- `resolve` (`S:...Server.lua:741-760`) wuerde ihn als vermisst zaehlen
  und `countMisses` (`:765-790`) nach drei Suchlaeufen auf "missing" setzen; `B.FollowLost` (`S:...Follow.lua:168-176`) und die Hud-Suche
  ebenso. Alle drei muessen `rec.ride` ueberspringen.

### 4.4 Sonderfaelle

| Fall | Vorschlag | Begruendung |
|---|---|---|
| Speichern/Laden waehrend der Fahrt | `rec.ride` steht im Register, kein Tier in der Welt. Nach dem Laden: Besitzer im Auto -> weiter mitfahren; zu Fuss -> Aussteigen (SP sofort, wie NC `:8556-8561`) | Register = Wahrheit |
| Absturz: Register neuer als die Zelle (riding, aber das alte Tier liegt in der Zelle) | Aussteigen baut ein neues Tier mit hoeherer `gen`; das alte (Spiegel mit kleinerer `gen`) wird beim Suchlauf als veraltete Kopie entfernt (1.3 Regel 3) | **ohne `gen` = Doppel** |
| Absturz: Zelle neuer als das Register (Tier entfernt, Register ohne riding) | Eintrag ohne Objekt -> "missing" nach den Fehlversuchen; "Call to me" holt es (5) | nichts verdoppelt |
| Besitzer stirbt im Auto | MP: am Server ist er tot noch online (`p:isDead()`, `B.Players` filtert ihn, `S:...World.lua:41`) -> Junges an `rec.x/y` (Auto) neu erzeugen, `mode = "stay"`. SP: Besitzer `rideLostMs` (~5 s) nicht da -> dasselbe, solange die Gegend geladen ist (`B.AreaLoaded`); sonst bleibt `ride`, und die neue Figur (gleicher Schluessel `__sp`) bekommt es beim ersten Schritt zu Fuss neben sich | Frage F3 |
| Besitzer meldet sich ab (MP) | nicht in `getOnlinePlayers()` -> `ride` bleibt; beim naechsten Einloggen zu Fuss -> neben ihm | wie B1b A7 (Kevin: ja, `ENTSCHEIDUNGEN.md:284`) |
| Server-Neustart | wie Abmelden | - |
| fremder Spieler im selben Auto | nur der Besitzer zaehlt (`rec.owner`) | NC `:8662-8669` |

Ungeprueft: `getVehicle()` am Server fuer fremde Spieler (Aussetzer?), ob ein Spieler beim Einloggen im Auto sitzt, Neuerzeugen direkt
neben einem gerade gebremsten Fahrzeug (Physik).

---

## 5. Unstuck "Call to me" (Auftrag 5)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Menuepunkt am Tier | `Events.OnClickedAnimalForContext` + `context:addOption` | `S:client/BanditsNPCBearMenu.lua:434`, `:213-229` (Muster Follow/Name) | Client | **BELEGT** (B1a/B1b) |
| Bitte | `B.Ask(p, "Call", { id })` -> `sendClientCommand` | `S:shared/BanditsNPCBear.lua:445-454`; `V:client/DebugUIs/DebugContextMenu.lua:956` | Client -> Schreiber | **BELEGT**, nur LoginOnServer -> kein Kick |
| Pruefen | Besitz (`rec.owner == B.PlayerKey(p)`), `st` "tame" (Vorschlag: auch "missing"), nicht `ride`, `p:getVehicle() == nil` (`V:server/Vehicles/VehicleCommands.lua:11`), Abklingzeit, freie Kachel (4.2) | wie links | Schreiber | eigener Code + Belege |
| Abklingzeit 5 min Echtzeit | `getTimestampMs()` je `rec.id` in einer Sitzungs-Tabelle (nie speichern, Rueckwaerts-Uhr = abgelaufen) | `V:server/Foraging/forageServer.lua:456`; Lehre `NC:client/BanditsNPCPersistence.lua:9440-9486`, Pruefung in der Funktion statt nur im Menue `:9616-9620` | Schreiber | **BELEGT** |
| Herholen | geladen: `B.RemoveCub(alt)`; dann `B.CreateCub` neben dem Besitzer, neu binden, `gen + 1`, `mode = "follow"` (Vorschlag) | 4.2 | Schreiber | **BELEGT** |

- Nicht geladen (Junges weit weg/virtuell): ohne `gen` waere das ein Doppel, mit `gen` wird die alte Kopie beim Wiederauftauchen entfernt
  (1.3 Regel 3). Damit hilft "Call to me" genau in Kevins Fall "wie find ich den" -- aber nur, wenn man das Tier anklicken kann. Ein
  vermisstes/fernes Junges kann man nicht rechtsklicken -> Vorschlag Zusatzpunkt im Welt-Menue (`S:client/BanditsNPCBearMenu.lua:435`) bzw.
  spaeter im V-Fenster (Frage F4).
- Meldungen (Schluessel-Vorschlag): `UI_BN_Bear_Menu_Call`, `..._CallTip`, `Note_Called`, `Why_Cooldown` (%1 Minuten), `Why_Riding`,
  `Why_NoRoom`; `Why_InCar`, `Why_NotOwner` gibt es schon.

---

## 6. Gehen (Auftrag 6)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| gehen | `a:setVariable("animalRunning", false)` + `a:pathToLocation(x, y, z)` | **ERLAUBT** (Kevin 11.11. / 08.11.); Methode am Spieler `V:shared/TimedActions/Animals/ISMilkAnimal.lua:139`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:37`, am Zombie `B:shared/ZombieActions/ZAMove.lua:32`, am Tier `T:shared/NCBearFight.lua:457`, `:1064`; Reihenfolge wie Vanilla `dec/BaseAnimalBehavior.java:167`/`:224` | Schreiber; Merker reist im Tierpaket mit (`dec_b1b/AnimalStateVariables.java:12`, `:18`) | ok |
| rennen | `a:fleeTo(sq)` | `V:...ISMilkAnimal.lua:38` | Schreiber | **BELEGT** |
| Vanilla-Muster | Seil: rennt bei Reststrecke > 5, sonst geht | `javap/BaseAnimalBehavior.txt:4138-4198` (FB1B 1.2) | - | Vorbild |

Zahlen (FB1B 0.3; `baer/spiel/tier_spez.md:226-237`): Junges geht 0,52, rennt 2,47 Kacheln/s; Spieler geht 2,27. B1b haelt bis
`followNear` 3 und laeuft ab `followStart` 4,5 (`S:shared/BanditsNPCBear.lua:67`). Vorschlag: **gehen nur, wenn die Reststrecke
<= `walkDist` (5, Vanilla) UND der Besitzer langsamer ist als `walkSpeed` (0,52, = Tempo des Gehen-Clips)** -- also nur zum
Aufschliessen an einen stehenden Besitzer, sonst rennen. Mit dem neuen Modell nur `walkSpeed` hochsetzen. Das loest nebenbei N1
(Anrennen bis 0,5 Kacheln beim Stehenbleiben, `gegen_bericht_b1b.md:106-108`). Auch Heimweg im Bleiben (Regel 8) und der
Laerm-Ersatzweg (2.3) gehen.

---

## 7. Bildschirm-Markierung (Auftrag 7)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| setzen/verschieben | `BanditEventMarkerHandler.set(id, icon, dauer, x, y, farbe, text)` | `B:client/BanditEventMarkerHandler.lua:6-38` (gleiche Id -> `setDuration` + `update`, `:31-36`; neu nur bei `dauer > 0` und `dist <= 1500`, `:11-13`) | Client (MP: Sicht des Clients) | **BELEGT (Bandits)**, gespielt bei NC `NC:client/BanditsNPCSpawn.lua:296-321` |
| ausblenden | dieselbe Id mit `dauer = 0` | `B:client/BanditEventMarkers.lua:135-140` (`setVisible(false)`); NC `:311-317` | Client | **BELEGT** |
| Dauer | NC und Bandits geben 1800 (`NC:...Spawn.lua:308`, `B:server/BanditServerSpawner.lua:1093`); `RemoveOldMarkers` alle 10 Spielminuten raeumt bei `start + dauer < getGametimeTimestamp()` (`B:client/BanditEventMarkerHandler.lua:40-51`), danach baut das naechste `set` eine neue | Client | so wie NC |
| Symbol | Pfad-Text `"media/ui/BanditsNPCBearCub_marker.png"`, `getTexture(icon)` | `B:client/BanditEventMarkerHandler.lua:33`; Bandits' eigene `Bc:ui/friend.png` 96 x 96 (nachgemessen); unsere `_arbeit/baer_icon/BanditsNPCBearCub_marker.png` 96 x 96 (nachgemessen) | Client | ok; gezeichnet mit `drawTexture` in Originalgroesse (`B:client/BanditEventMarkers.lua:193`) |
| Farbe | `{ r = 1.0, g = 0.72, b = 0.30 }` | `colorBlend` quadriert die Farbe (`B:client/BanditEventMarkers.lua:147-157`) -> kraeftiges Orange (Kevin: so lassen) | Client | ok |
| Text | `U.T("UI_BN_Bear_Marker_Cub")` | unter dem Symbol, `UIFont.Small` (`:175-177`) | Client | 7 Sprachen |
| Riegel | `BanditEventMarkerHandler and BanditEventMarkerHandler.set and BanditEventMarker and BanditUtils and BanditUtils.DistTo` | `set` braucht `BanditUtils.DistTo` (`:12`) | Client | Existenz-Riegel |
| Takt 0,4 s | `Events.OnTick` + `getTimestampMs()` (oder `OnPlayerUpdate` wie NC) | `V:client/Chat/ISChat.lua:943`; `V:client/Tutorial/Steps.lua:1919` (`OnPlayerUpdate`) | Client | **BELEGT** |

- Ziel: das Junge aus `B.View.me.wild` (Finder = ich, `S:server/BanditsNPCBearRegistry.lua:260-264`), Zustand "new" (noch nicht
  entdeckt) und nach "shy" noch `markerAfterMs` (Vorschlag 60 s, Zeitpunkt merkt der Client selbst). Aus bei: tame/fed, kein Eintrag,
  keine Lage.
- Lage: live von der Client-Kopie, wenn geladen (Hud-Tabelle `S.objs`, `S:client/ISUI/BanditsNPCBearHud.lua:58-66`, `:117-126`), sonst aus der
  Sicht. **Die Sicht hat heute KEINE Lage** (`viewEntry` `S:...Registry.lua:421-437`) und fuehrt das Wald-Junge des Finders nur bis
  `tellDist` 60 (`:448-462`; Wald-Junges 30..50, `S:shared/BanditsNPCBear.lua:84-85`) -> Planer: `x, y` (ganzzahlig) in eigene Eintraege
  (owner/bond/finder) und den Finder immer in die Sicht; Lage nur nachschicken, wenn sie sich um >= 3 Kacheln aendert, hoechstens je 5 s.
- Fallen: `set` nimmt immer `getSpecificPlayer(0)` (`:8`; geteilter Bildschirm nur Spieler 1) und merkt `marker.player` beim Anlegen
  (nach Tod/Neuer Figur zeigt er von der alten Figur aus, bis `RemoveOldMarkers` raeumt -- wie bei NC). Doppelklick blendet aus
  (`:19-21`), unser naechstes `set` zeigt ihn wieder (Frage F6). Gleiche Bildschirmstelle wie alle Bandits-/NC-Markierungen (0.8, Frage F5).
  Unsichtbare alte Marker bleiben im UIManager (Bandits raeumt nur die Tabelle, `:40-49`) -- ein Element je 1800 Spielsekunden, klein.

---

## 8. Karten-Symbol (Auftrag 8)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Mini-Karte umwickeln | `ISMiniMapInner.render` (erbt `ISUIElement.render`), alte merken, danach zeichnen | Klasse `V:client/ISUI/Maps/ISMiniMap.lua:4`; `mapAPI` `:190-193`; Karte malt in `prerender` `:206-212`; Lehre `NC:client/ISUI/BanditsNPCMiniMap.lua:19-26`, `:264-275` | Client | Lua-Aufsatz (Naht-frei, Vanilla bleibt unveraendert) |
| grosse Karte umwickeln | `ISWorldMap.render` | `V:client/ISUI/Maps/ISWorldMap.lua:384` (eigene Methode), `mapAPI` `:268` | Client | wie oben |
| Welt -> Bildschirm | `self.mapAPI:worldToUIX(x, y)` / `worldToUIY(x, y)` (ZWEI Zahlen) | `V:client/ISUI/Maps/ISWorldMap.lua:478-479`, `V:client/ISUI/Maps/ISWorldMapSymbols.lua:347` | Client | **BELEGT** |
| Symbol zeichnen | `self:drawTextureScaledAspect(tex, x - s/2, y - s/2, s, s, a, r, g, b)` | `V:client/ISUI/Maps/ISWorldMap.lua:480-482`; Signatur `V:client/ISUI/ISUIElement.lua:1065` (Reihenfolge a, r, g, b!) | Client | **BELEGT** |
| Bild laden (einmal) | `getTexture("media/ui/BanditsNPCBearCub_marker.png")` | `V:client/ISUI/Maps/ISMap.lua:573`; `B:client/BanditEventMarkers.lua:259` | Client | **BELEGT** |
| Groesse | grosse Karte nach Zoom wie Vanilla `PZMath.lerp(32, 64, ...)` mit `getZoomF()` (`V:client/ISUI/Maps/ISWorldMap.lua:446-449`) -- fuer ein Tier kleiner (Vorschlag 18..28 px); Mini-Karte fest (Vorschlag 14 px) | Client | Stellwert |
| welcher Spieler | `self.playerNum` | `V:client/ISUI/Maps/ISMiniMap.lua:344-347`; ISWorldMap `:1478` | Client | **BELEGT** |

- Wer: eigene Eintraege der Sicht mit `owner == ich` (tame/missing) oder `bond == ich` und `st == "fed"`; Kevin: nur der eigene Baer
  (`ENTSCHEIDUNGEN.md:283`). Mitfahrend: nicht zeichnen (NC-Lehre). Lage: live (Client-Kopie) sonst Sicht-Lage blasser
  ("letzte bekannte Stelle", NC `COL_AWAY` `BanditsNPCMiniMap.lua:62`). Ausserhalb des Elements nicht zeichnen (`:202-205`, `:224`).
- Kosten: Liste je 0,5 s neu (wie NC `RESCAN_MS` `:69`), je Bild 2 Umrechnungen + 1 Bild je Junges (<= `BearMaxPerPlayer` 4).
- **Einmal einhaengen, ohne Identitaets-Neuversuch** (NC-Lehre Stapelueberlauf mit "Aegis Panel", `BanditsNPCMiniMap.lua:249-276`);
  NPC Crew umwickelt dieselben zwei Methoden -- die Kette haelt, weil beide die alte Methode merken.

---

## 9. Anzeige-Optionen je Spieler (Auftrag 9)

### 9.1 API (Vanilla, `V:client/PZAPI/ModOptions.lua`)

| Baustein | Fundstelle | Rueckgabe |
|---|---|---|
| `PZAPI.ModOptions:create(id, name)` | `:247-253` | Seite; Bandits `B:client/BanditModOptions.lua:12`, NC `NC:client/BanditsNPCModOptions.lua:82` |
| `opts:addTitle(name)` / `addDescription(key)` / `addSeparator()` | `:28-38` (Beschreibung ruft sofort `getText`) | - |
| `opts:addTickBox(id, name, wert, tooltip)` | `:64-86` | `opt:getValue()` = true/false |
| `opts:addComboBox(id, name, tooltip)` + `opt:addItem(key, gewaehlt)` | `:121-156` (`addItem` -> `getText`) | `getValue()` = Index (1..n) |
| `opts:addSlider(id, name, min, max, schritt, wert, tooltip)` | `:206-228` | `getValue()` = Zahl; im Fenster ohne Tooltip (`V:client/OptionScreens/MainOptions.lua:3019-3036`) |
| lesen zur Laufzeit | `PZAPI.ModOptions:getOptions(id):getOption(key):getValue()` | `:255-257`; Bandits `B:shared/BanditCompatibility.lua:98`; NC `BanditsNPCModOptions.lua:72-80` |
| speichern / laden | `ModOptions.ini` je Rechner | `:259-290`, `:292-333`; aufgerufen `V:client/OptionScreens/MainOptions.lua:2791` (load), `:3761` (save) |

- Namen und Tooltips laufen beim Bau des Fensters durch `getText` (`MainOptions.lua:2810-2812`, `:3020`) -> **Schluessel** uebergeben
  (`UI_BN_Bear_MO_*`, 7 Sprachen).
- Je Rechner, nicht je Spielfigur (geteilter Bildschirm teilt sie); im MP je Client, nie beim Server -- genau richtig fuer Anzeige.
- Anlegen auf Dateiebene (Client-Datei), mit Existenz-Riegel und Fehlerzeile statt `pcall` (NC-Lehre `BanditsNPCModOptions.lua:47-51`,
  `:136-140`). Seiten-Id frei: in NC nur "NPCCrew" (grep `ModOptions:create`), Bandits "Bandits"; Vorschlag `"BanditsNPCBear"`. Spaeter
  koennte die Seite in NPC Crews Seite aufgehen (Naht, nicht B1c).
- Erweiterbar: weitere `addComboBox` je Wert (aus/Balken/Zahl) haengen einfach an; Lesen nur ueber EINE Funktion `U.Opt(id, vorgabe)`
  (nil = Seite fehlt -> Vorgabe), Wert hoechstens 1 x je Sekunde holen.

### 9.2 Inhalt B1c (Vorschlag)

| Id | Art | Vorgabe |
|---|---|---|
| `BearTagShow` | TickBox "Show the name tag above my bear" | true (Zaehm-Balken bleibt IMMER, Kevin `ENTSCHEIDUNGEN.md:236`) |
| `BearTagSize` | Slider (Kevin: "Groesse als Schieberegler", `ENTSCHEIDUNGEN.md:237`) z. B. 50..200 %, Schritt 25, Vorgabe 100 | 100 |

### 9.3 Groesse umsetzen

| Weg | Aufruf | Fundstelle | Urteil |
|---|---|---|---|
| stufige Schrift | `UIFont.Small` / `UIFont.Medium` / `UIFont.Large` an `drawTextCentre(str, x, y, r, g, b, a, font)` | `V:client/ISUI/ISUIElement.lua:1280`; Hoehen `getTextManager():getFontHeight(UIFont.Medium)` `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8`, `(UIFont.Large)` `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6` | **BELEGT**; Schieber auf 3 Stufen abbilden |
| stufenlos | `self:drawTextZoomed(str, x, y, zoom, r, g, b, a, font)` | Vanilla-Lua-Huelle `V:client/ISUI/ISUIElement.lua:1260-1268` (innen `javaObject:DrawText(font, str, x, y, zoom, ...)` woertlich in Vanilla), aber **kein Vanilla-Aufrufer** der Huelle; Breite fuers Zentrieren `getTextManager():MeasureStringX(font, str)` (`V:client/ISUI/AdminPanel/ISAddNonPvpZoneUI.lua:54`) x zoom = ungeprueft | **Grenzfall** -> im Spiel ansehen; Balken (`drawRect`) skaliert frei |

---

## 10. Kleinkram (Auftrag 10)

- **ES:** `S:shared/Translate/ES/UI.json:31` `"UI_BN_Bear_Hud_Pet": "Caricias: %1"` + `:32` `"lista"` -> "Caricias: lista" (Mehrzahl +
  Einzahl). Einzahl: `"Caricia: %1"`. (Am Rande: FR `"Caresses : %1"` + `"prêt"` hat dasselbe Muster, `FR/UI.json:31-32`; PTBR
  "Carinho: pronto" und RU "Ласка: готово" passen.)
- **N1** (Anrennen bis 0,5 Kacheln beim Stehenbleiben, `gegen_bericht_b1b.md:106-108`): loest sich mit dem Gehen (6) weitgehend; sonst
  Stellwert `followLead` 1,0.
- **N2** (`B.CleanName` laesst Zeichen ueber U+FFFF, Privatbereich, U+FFFC/FFFD und reine Kombinationszeichen durch, `:109-112`): klein und
  sicher -- Ersatzzeichen-Paare (Kahlua liefert dafuer zwei Zeichen) und U+E000-F8FF, U+FFFC-FFFD in die Sperrliste `NAME_BADR`
  (`S:shared/BanditsNPCBearRules.lua:347-361`), Name nur aus Kombinationszeichen (U+0300-036F) ablehnen.
- **N3** (`B.BuildView` gibt einem Konto ohne Schluessel alle ungebundenen Jungen, `:113-115`): ein Wort `pkey ~= nil and (...)` in
  `S:server/BanditsNPCBearRegistry.lua:449`. Klein und sicher.

---

## 11. NUR im Jar belegt (getrennt) -- nicht als Engine-Aufruf benutzen

| Was | Wofuer | Ersatz |
|---|---|---|
| `animal:getLastSoundRespondedTo()`, Ereignis `OnWorldSound` | Laerm direkt erkennen | Zustand + `animalRunning` + Stress (2.3) |
| `animal:isAnimalMoving()` (grep Lua 0) | "bewegt es sich" | `getActionStateName()` (2.3) |
| `animal:setShouldFollowWall(false)`, `getCurrentState()` | Halt-Feinheiten | nicht noetig |
| `vehicle:canAddAnimalInTrailer(animal)` (Inhalt nicht gelesen) | Anhaenger-Luecke schliessen | Frage F7 (z. B. `trailerBaseSize` sehr gross -- ungeprueft) |
| `addAcceptance`, `setDebugStress`, `setDebugAcceptance` | Akzeptanz/Stress setzen | nicht benutzen (`forschung_engine.md:509-513`, `:630-631`) |
| Teleport (`setX/setY/setLx...`) am Tier | Herholen | Entfernen + Neu erzeugen (4, 5) |
| `ObjectModDataPacket` (Client schreibt Tier-ModData) | -- (Gefahr, kein Werkzeug) | 1.4 |
| Grenzfall: `animal:getVariableBoolean("animalRunning")` -- Methode belegt, Speicher-Gleichheit Name/Kennung nur Jar | Flucht erkennen | Zusatzsignal Stress |
| Grenzfall: `ISUIElement:drawTextZoomed` -- innen woertlich Vanilla, Huelle ohne Vanilla-Aufrufer | stufenlose Schildgroesse | Schriftstufen |

---

## 12. Offene Fragen (Fragen fuer Kevin; Kevin schlaeft -- jeweils mit Empfehlung)

- **F1 MP-Spiegel faelschungssicher?** Ein veraenderter Client kann Tier-ModData schreiben (1.4). Unterschrift mit Geheimnis in einer Datei am
  Server waere sicher, braucht aber einen am Server unbelegten Dateileser. Empfehlung: B1c ohne, mit Deckeln und Log.
- **F2 Stress durch Laerm** (je Flucht +radius x 0,05, Abbau sehr langsam): ausgleichen (z. B. nach jeder abgefangenen Flucht) oder lassen?
  Gleiche offene Frage wie beim grossen Baeren (`_arbeit/baer_laerm/fix_bericht.md:11-12`). Empfehlung: lassen, Streicheln senkt ihn.
- **F3 Besitzer stirbt im Auto:** Junges steigt am Auto aus und wartet dort (stay). Im SP: ist die Gegend schon entladen, taucht es bei der
  neuen Figur auf (gleicher Schluessel). Ok? Empfehlung: ja.
- **F4 "Call to me" auch fuer ein vermisstes/fernes Junges** (das man nicht rechtsklicken kann): Zusatzpunkt im Welt-Menue? Empfehlung: ja
  (genau Kevins Fall "wie find ich den").
- **F5 Markierung ueberlappt** NPC Crews Ueberlebenden-Pfeil (Bandits merkt EINE Stelle fuer alle). Unsere einmal nach dem Anlegen um eine
  Symbolbreite versetzen (Lua am Marker-Element, `setX` wie `B:client/BanditEventMarkers.lua:81`)? Empfehlung: ja.
- **F6 Doppelklick blendet die Markierung aus** -- respektieren (bis das Junge entdeckt ist) oder wieder zeigen? Empfehlung: respektieren.
- **F7 Anhaenger-Luecke** (jeder laedt jedes Tier in einen Tier-Anhaenger): schliessen? Ungeprueft wie (Jar `canAddAnimalInTrailer` nicht
  gelesen). Empfehlung: eigener Lauf nach B1c.
- **F8 Schild-Groesse:** Schieber auf 3 Schriftstufen (sicher) oder stufenlos per `drawTextZoomed` (Grenzfall)? Empfehlung: Stufen.
- **F9 "Rennen"** erzeugt laut Jar keinen Tier-Laerm (0.2). Bitte beim Test mit Log ansehen, was die Flucht ausloest (Q, Schuss, Husten,
  Zombie am Zaun).
- Planer-Fragen: Wildes Junges aus einem verlorenen Register wiederherstellen oder verschwinden lassen? Mitfahrendes Junges auf der Karte
  beim Spieler zeigen oder weglassen (NC: weglassen)? `hideOwnerMax`/`zedHide`/`walkDist`-Zahlen.

## 13. Luecken (ungeprueft, Testpunkte)

`getObjectListForLua`/`getAnimalID` am MP-Server (A3 aus B1a); `getVehicle()` fremder Spieler am Server; Reihenfolge OnTick/Tier-Update am
Server und Laerm-Lebensdauer in Server-Ticks; ob der Ersatzweg die Flucht wirklich vor dem ersten sichtbaren Schritt ersetzt; Zombie-Liste
und `getVariableBoolean("Bandit")` am Server; Neuerzeugen neben dem Auto; Einloggen im Auto; Bandits-Markierung nach Tod/geteiltem
Bildschirm; `drawTextZoomed`-Breite; ob `ModOptions.ini` vor dem ersten Lesen geladen ist (laedt beim Bau des Optionsfensters,
`MainOptions.lua:2790-2791`; NC liest erst zur Laufzeit und ist gespielt).

Statisch geprueft, nicht gespielt.
