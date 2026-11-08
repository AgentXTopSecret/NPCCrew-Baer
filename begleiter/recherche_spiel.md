# Baer als Begleiter: was das Spiel selbst kann (B42.21)

Stand 08.11.2026, PZ 42.21 (`projectzomboid.jar` vom 28.09.2026). **Statisch gelesen, nicht gespielt.**
Fundstellen: `Klasse.methode Offset` = `javap -c -p` (Auszuege unter `_arbeit/baer_begleiter/*.txt`, Klassen in
`_arbeit/baer_begleiter/jar/`). `Datei.lua:Zeile` = Vanilla `media/lua`. Wo nur die Vineflower-Lesung
(`_arbeit/baer_spiel/dec/`) stand und kein Offset geholt wurde, steht "(Lesung)". Ohne Fundstelle: "ungeprueft".
Vorarbeit, auf die sich das hier stuetzt: `../spiel/tier_spez.md` (Definition, Netz, AnimSet, Tod).

---

## 0. Ergebnis in zwoelf Saetzen

1. **Wachsen kann das Spiel schon:** jeden Spieltag waechst die Groesse um `(maxSize - minSize) / ageToGrow * Gesundheit`.
   Ein Baby, das gross wird, ist also nur eine Zahl in der Definition. Ein schlecht versorgter Baer waechst langsamer.
2. **Kein zweites Tier "Jungbaer" nehmen.** Beim Stufenwechsel baut das Spiel ein NEUES Tier und loescht das alte; die
   ModData (dort laege unser Level) geht dabei verloren, und Jungtiere trinken nicht selbst. Eine Art, eine Stufe.
3. **Der Groessenbereich ist frei:** nur `minSize`/`maxSize` der Definition begrenzen. Mit der Groesse wachsen Bild,
   Kollision, Schatten und Anhaenger-Platz mit, **nicht** die Laufgeschwindigkeit (Fuesse rutschen bei grossen Werten).
4. **Hunger und Durst gibt es fertig**, inklusive Tod durch Mangel. Selbst trinken und fressen tut ein Tier aber nur in
   einer Tierzone (Fluss, Trog, Futter am Boden) oder auf der eigenen Kachel (Pfuetze, Gras). Unterwegs muss der Spieler
   ihn fuettern und traenken; dafuer gibt es Vanilla-Menues ("Feed", "Water").
5. **Zombies koennen einem Tier nichts tun**, und Bandits kennt Tiere gar nicht. "Sterben gegen Zombies/Banditen" muessen
   wir selbst bauen (eigener Schaden). Spieler, Autos, andere Tiere und Hunger schaden schon im Spiel.
6. **Unsterblich gibt es als Engine-Schalter** (`setIsInvincible`, Lua-belegt), aber er schaltet auch Hunger und Durst ab
   und wird nicht gespeichert. Ein "Downed" kennt das Spiel nicht; Sitz-Pose plus Bewegungssperre ist der naechste Weg.
7. **Ein Leitseil gibt es** (Seil in der Hand, reisst bei 15 Kacheln). Fuer einen Kaempfer taugt es nicht: nimmt der
   Spieler eine Waffe, faellt das Seil.
8. **Einen Besitzer kennt das Spiel nicht.** Jeder darf jedes zahme Tier anleinen, aufheben, toeten, zerlegen. Besitz,
   Level und "ein Baer je Spieler" gehoeren in unsere ModData.
9. **Speichern/Laden haelt der Baer aus:** er liegt mit seiner ModData in der Kartendatei seines Chunks und bleibt dort, wo
   er zurueckgelassen wurde. Ausserhalb einer Tierzone steht die Zeit fuer ihn still, solange der Chunk nicht geladen ist.
10. **Kein Teleport:** das Spiel holt nie ein Tier zum Spieler. Auto nur im Tier-Anhaenger (Platz 500) oder als kleines
    Jungtier auf dem Arm.
11. **Im Mehrspieler rechnet der Server alles** (Laufen, Hunger, Wachsen, Schaden). Der Client bekommt Gesundheit, Hunger,
    Durst, Alter, Gewicht, aber weder Groesse noch ModData laufend nachgeschickt.
12. **Ausdauer haben Tiere nicht.** Ein Levelsystem (Ausdauer, mehr Schaden, mehr Leben) ist ganz unseres; die Engine
    bietet dafuer nur die Stellschrauben `baseDmg`, Gen `strength`, `healthLossMultiplier`, Gen `resistance`.

---

## 1. Wachstum

### 1.1 Wie das Spiel ein Tier wachsen laesst

| Was | Fundstelle |
|---|---|
| Einmal je Spieltag: wenn `age < daysSurvived`, wird `age` nachgezogen und `growUp` gerufen | `AnimalData.update` Offset 57-112 |
| Groesse += `(getMaxSize - getMinSize) / stage.ageToGrow * getHealth()`, gedeckelt auf `getMaxSize` | `AnimalData.growUp` Offset 41-130 |
| Gewicht waechst genauso (`maxWeight`/`minWeight`) | `AnimalData.growUp` ab Offset 80 |
| In zu kleiner Tierzone nur ein Achtel (`smallEnclosure`) | `AnimalData.growUp` Offset 90 |
| `setSize` klemmt IMMER auf `[getMinSize, getMaxSize]` | `AnimalData.setSize` Offset 9 (`PZMath.clamp`) |
| Neues Tier startet bei `getMinSize` (`initSize` endet mit `setSize(0.1)`, das klemmt) | `AnimalData.initSize` Offset 73-76 |
| Sandbox "Animal age" vervielfacht das Altern (90 / 10 / 5 / 1) | `AnimalData.getAgeGrowModifier` Offset 3-60 |
| Gen `maxSize` multipliziert min und max, Erbkrankheit `dwarf` teilt | `AnimalData.getMinSize/getMaxSize` (Lesung); Baer hat das Gen absichtlich nicht (`NCBearDefs.lua`:14) |
| Gen `ageToGrow` veraendert die Dauer | `AnimalGrowStage.getAgeToGrow` (Lesung) |

**Vanilla-Werte:** Kuh 0,9 -> 1,1 (`CowDefinitions.lua`:192-193), Kalb 0,9 -> 1,2 mit EIGENEM Modell und eigenem AnimSet
(`CowDefinitions.lua`:121-136), Reh 0,85 -> 1,2 (`DeerDefinitions.lua`:152-153). Vanilla skaliert also nur um rund 30 %;
das "Kleinsein" der Jungtiere steckt im eigenen Modell. Der Baer kann es ueber den Massstab allein machen (Faktor 2-3) --
wie das bei einem Faktor 0,4 aussieht (Kopf zu klein fuer ein Baby), entscheidet nur der Blick. **Ungeprueft.**

### 1.2 Stufen (nextStage) -- warum nicht

- `isBaby()` heisst `currentStage.nextStage != null` (`IsoAnimal.isBaby` Offset 7). Ein Jungtier **trinkt nicht selbst**
  (`BaseAnimalBehavior.checkDrinkBehavior` Offset 4) und frisst zuerst bei der Mutter (`checkEatBehavior`, Lesung).
- Der Wechsel baut ein **neues Objekt** (`AnimalData.grow` Offset 92 `new IsoAnimal`, alter Koerper `delete` 331/540,
  neuer `addToWorld` 545). Mit kommen: Alter, Seil (145), Vertrauen (216-219), Name (268), `AnimalID` (304), unsterblich
  (404). **Nicht mit: ModData** (kein `getModData` in `grow`). Ein Lua-Ereignis dafuer gibt es nicht (`LuaEventManager`
  kennt nur `OnAnimalTracks` und `OnClickedAnimalForContext` mit "Animal" im Namen).
- Folge: Level und Besitz waeren nach dem Erwachsenwerden weg, und unsere Lua muesste den neuen Koerper ueber die
  `AnimalID` wiederfinden. **Eine Art "bear" mit genau einer Stufe ohne `nextStage`** spart beides.

### 1.3 Was mit der Groesse mitwaechst

| Mit | Fundstelle |
|---|---|
| Bild (`FinalScale` = `getSize`) | `../spiel/tier_spez.md` 2.5 (`ModelSlotRenderData` Offset 452-455) |
| Kollisionsbreite = `collisionSize * getSize` | `IsoAnimal.updateInternal` Offset 34-42 und 113-121 |
| Schatten = `shadoww/fm/bm * getSize` | `IsoAnimal.renderShadow` Offset 299 |
| Anhaenger-Platz = `trailerBaseSize * getSize` | `IsoAnimal.getAnimalTrailerSize` Offset 4 |
| Fleisch/Teile beim Zerlegen | `IsoAnimal` (Lesung, `part.minNb * getAnimalSize`) |
| Streichel-Haltung des Spielers (`AnimalSizeY`) | `ISPetAnimal.lua`:32 |

**Nicht mit:** die Laufgeschwindigkeit (kommt nur aus dem Clip, `tier_spez.md` 2.8) und `animalSize` (feste Halteschwelle
der Wegfindung). Ein doppelt so grosser Baer macht doppelt so lange Schritte bei gleichem Weg: Fussgleiten. Ausweg nur
ueber eigene Clips je Groesse oder einen Gang, dessen Weg mitwaechst. **Ungeprueft.**

**Achtung Anhaenger:** Tier-Anhaenger haben 500 Platz (`vehicle_trailer_livestock.txt`:51, `vehicle_trailer_horsebox.txt`:51).
NCBearTest hat `trailerBaseSize = 600` (`NCBearDefs.lua`:72) -- passt schon bei Groesse 1,0 nicht hinein.

**Nachstellen:** `getData():setSizeForced(x)` (ButcheringUtil.lua:569) umgeht die Klemme, haelt aber nicht: der naechste
`growUp` klemmt wieder, und `IsoAnimal.load` liest mit `setSize` (Offset 405). Nur zum Ausprobieren.

### 1.4 Wie gross darf er werden

Keine Obergrenze ausser `maxSize` gefunden. Was bei 2-3facher Groesse an Tueren, Zaeunen und in der Wegfindung passiert
(Breite 0,84+), ist **ungeprueft**. `canClimbStairs` und `canClimbFences` stehen per Vorgabe auf **false**
(`AnimalDefinitions`-Felder; `canClimbStairs` liest nur `IsoMovingObject`, `canClimbFences` auch die Wegfindung
`PathfindNative`/`PMMover`, Suche im Jar nach dem Namen); ohne `canClimbStairs = true` kommt er nicht
mit ins Obergeschoss (Wirkung im Einzelnen ungeprueft).

---

## 2. Fressen und Trinken

### 2.1 Was die Engine je Spielstunde rechnet

| Was | Fundstelle |
|---|---|
| Hunger und Durst steigen nur, wenn **nicht wild und nicht unsterblich** | `AnimalData.updateHungerAndThirst` Offset 4, 41, 138-162 |
| Anstieg = `hungerMultiplier` bzw. `thirstMultiplier` mal Gen und Sandbox "Animal stats" | `getHungerReduction`/`getThirstReduction` (Lesung) |
| Ueber 0,8 Hunger ODER Durst: Gesundheit sinkt um `getHealthLoss(3)` je Stunde | `AnimalData.updateHealth` Offset 55-106 |
| Sonst heilt sie um denselben Betrag bis 1,0 | `AnimalData.updateHealth` Offset 182-195 |
| `getHealthLoss = healthLossMultiplier * (1,5 - Gen resistance) / Teiler` | `AnimalData.getHealthLoss` Offset 13-37 |
| Ueber 0,8 Hunger verliert er Gewicht | `AnimalData.updateWeight` (Lesung) |

Vanilla-Kuh: Hunger 0,0035/h, Durst 0,0065/h, Verlust 0,01 (`CowDefinitions.lua`:209-216). NCBearTest hat beides auf 0
(nicht gesetzt) -- er hat heute keinen Hunger.

### 2.2 Wann er selbst etwas sucht

- Alle 500 Ticks (bei Hunger/Durst ueber 0,5 alle 150) fragt `checkBehavior` (`BaseAnimalBehavior.update` Offset 124-131).
- Ab `thirstHungerTrigger` (Vorgabe 0,1) sucht er (`checkDrinkBehavior` Offset 30).
- **Fluss** nur mit Tierzone (`tryDrinkFromRiver` Offset 4-7), **Troege** nur der verbundenen Zonen
  (`getRandomTroughList`, Lesung), **Pfuetze** und **Gras** ausserhalb einer Zone nur auf der EIGENEN Kachel
  (`tryAndGetPuddle` Offset 31-171; `tryAndGetGrassFloor`, Lesung; Gras nur mit `eatGrass`).
- Folge: **unterwegs sucht er nichts.** An der Basis mit Tierzone, Trog und Wasser versorgt er sich selbst.

### 2.3 Was der Spieler tun kann (alles Vanilla, gilt fuer jede Art)

| Aktion | Fundstelle | Bedingung |
|---|---|---|
| "Feed" aus der Hand | `ISAnimalContextMenu.lua`:29-85, `ISFeedAnimalFromHand.lua`:45-49 -> `IsoAnimal.feedFromHand` | Futtertyp in `feedByHandType` oder `eatTypeTrough`; dazu Vertrauen +1..3, Stress runter, XP Tierhaltung |
| "Water" aus Flasche/Eimer | `ISAnimalContextMenu.lua`:465, `ISGiveWaterToAnimal.lua`:33/85 | Durst ab 0,1; je Schritt -0,05 * `thirstBoost` |
| Futter in Trog / Wasser in Trog | Tierzone noetig (2.2) | |
| Streicheln | `ISAnimalContextMenu.lua`:286, `ISPetAnimal.lua`:69 | `canBePet`; Vertrauen +2..6, Stress runter |

Streicheln setzt beim SPIELER die Variable `animal` = Tierart (`ISPetAnimal.lua`:39); Streichel-Knoten gibt es nur fuer
Vanilla-Arten (`media/AnimSets/player/petanimal/pet*.xml`). Fuer "bear" braeuchte es eine eigene `petbear.xml` in der Mod
(AnimSet-Ordner liest das Spiel aus Mods, `tier_spez.md` 3.1). Was ohne Knoten passiert: **ungeprueft**.

### 2.4 Wenn der Chunk entladen ist

- Nachgeholt wird nur fuer Tiere **in einer Tierzone** (`DesignationZoneAnimal.doMeta` Offset 48/101 ->
  `IsoAnimal.updateStatsAway`) und fuer Wandertiere (`AnimalManagerMain.fromWorker` Offset 482). Dort frisst er nachtraeglich
  nur aus Troegen und Zonenfutter (`AnimalData.eatAndDrinkAfterMeta` Offset 176-469); ohne Futter hungert er nach.
- Ausserhalb einer Zone wurde kein Nachhol-Weg gefunden (Suche nach `updateStatsAway` und `timeSinceLastUpdate` im ganzen
  Jar). Er bleibt also eingefroren: kein Hunger, kein Wachsen, solange niemand in der Naehe ist. **Statisch, ungespielt.**

### 2.5 Fenster "Tier-Info"

`ISAnimalUI.lua` zeigt Gesundheit als Text (:93), Gewicht (:109), Stress (:185), Vertrauen (:326), Zone (:218). Nur bis 5
Kacheln Abstand (:9). Braucht `AnimalAvatarDefinition["bear"]` (steht schon, `NCBearDefs.lua`:93-108). Eigene Zeilen
(Level, Ausdauer) gibt es dort nicht; das waere ein eigenes Fenster oder ein Aufsatz auf `ISAnimalUI`.

---

## 3. Leben, Schaden, Tod

### 3.1 Gesundheit

- Wert 0..1, Heilung deckelt bei 1,0 (`AnimalData.updateHealth` Offset 182-195). Tot bei `health <= 0`
  (`IsoGameCharacter.isDead`, Lesung). Ablauf danach: `falldown` -> `onground` -> `die()` (`tier_spez.md` 4.2).
- `OnCharacterDeath` feuert auch fuer Tiere (`IsoAnimal.OnDeath` Offset 0-4). Darauf kann unsere Lua reagieren.

### 3.2 Wer schaden kann

| Quelle | Fundstelle | Fuer den Baeren |
|---|---|---|
| Spieler mit Waffe | `IsoAnimal.hitConsequences` Offset 0-32: `damage * getHealthLoss(0,025)`, nur ausserhalb eines MP-Clients | auch der Besitzer (Eigenbeschuss) |
| Auto | `IsoAnimal.Hit(BaseVehicle,..)`: Gesundheit sofort 0 (Lesung) | ein Treffer = tot |
| Anderes Tier | `IsoAnimal.HitByAnimal` Offset 4-62: `baseDmg * Gen strength * getHealthLoss(0,04)` | |
| Hunger/Durst | 2.1 | |
| "Kill animal" mit Messer, jeder Spieler | `ISAnimalContextMenu.lua`:307, `ISKillAnimal.lua`:5/45 -- **keine Besitzpruefung** | im MP kann ein Fremder ihn toeten |
| Alter | nur mit `maxAgeGeriatric` (`AnimalData.checkOld`, Lesung) | weglassen |
| **Zombie** | **nein.** `AttackState.triggerPlayerReaction` Offset 20-33: ist das Ziel ein `IsoAnimal`, wird es auf null gesetzt und der Biss faellt aus. Es gibt kein Trefferpaket Zombie->Tier (Paketklassen unter `network/packets/hit/`: nur AnimalHit*, PlayerHitAnimal, VehicleHitAnimal, ZombieHitPlayer, ZombieHitThumpable). | **muessen wir bauen** |
| **Bandit** | **nein.** Kein Wort `Animal` in der ganzen Bandits-Mod (grep `IsoAnimal\|isAnimal\|Animal` ueber `3268487204/mods/Bandits`: 0 Treffer). Bandits waehlt Ziele nur unter Zombies und Spielern. | **muessen wir bauen** |

### 3.3 Unsterblich (Engine)

- `animal:setIsInvincible(b)` ist Lua-belegt (`ISAnimalContextMenu.lua`:558-565; Serverbefehl `ClientCommands.lua`:855-862,
  der braucht `AnimalCheats`).
- Wirkung: `setHealth` verweigert jeden niedrigeren Wert (`IsoAnimal.setHealth` Offset 0-16). Das deckt Spieler, Auto,
  Tier und Hunger ab -- und blockt auch UNSERE eigenen `setHealth`-Aufrufe (vorher kurz ausschalten).
- **Nebenwirkungen:** Hunger und Durst steigen nicht mehr (`updateHungerAndThirst` Offset 41), Stress sinkt nicht mehr
  (`IsoAnimal.changeStress`, Lesung). Der Schalter wird **nicht gespeichert** (nicht in `IsoAnimal.save`); nach jedem Laden
  neu setzen. Beim Stufenwechsel wird er mitgenommen (`AnimalData.grow` Offset 404).

### 3.4 "Downed" -- gibt es nicht, naechster Weg

- Die Engine kennt nur lebend oder Sturz->Tod. Ein Liegen-ohne-Sterben muessen wir bauen.
- Kandidat Pose: **Sitzen** (`idleAction = "sit"`, `IsoAnimal.isAnimalSitting`; Knoten in `AnimSets/buck/idle`, Clips
  `DeerStag_SittingIdle/IdleToSitting/SittingToStanding`, `tier_spez.md` 3.3). Achtung: `BaseAnimalBehavior.checkSit` loescht
  das Sitzen bei Hunger ueber 0,2, mit Seil am Spieler und bei Regen ohne Dach (Offset 13-148). Also je Tick neu setzen
  oder `sitRandomly = false` lassen und selbst steuern (Wirkung ungeprueft).
- Kandidat Stillstand: `getBehavior():setBlockMovement(true)` (Lua-belegt `ISPetAnimal.lua`, `ISFeedAnimalFromHand.lua`).
- Vorbild NPC Crew (nur lesen): Niederschlag unter 30 %, Aufhelfen auf 45 %, Boden 10 % solange liegend
  (`client/BanditsNPCGuardian.lua`:15-32), Schalter `ImmortalCompanions` Vorgabe **an** (`media/sandbox-options.txt`:115-120).
  Die Lehre von dort (CLAUDE.md, v3.9.74): ein Boden im Tick ist Nachsorge, der toedliche Treffer passiert vorher im selben
  Aufruf. Beim Tier ist das Gegenstueck von `setNoDamage` der Engine-Schalter aus 3.3.
- **Vorschlag (nicht entschieden):** Sandbox "Baer unsterblich" AN -> Engine-unsterblich dauerhaft an, eigene Lebenspunkte und
  eigener Hunger/Durst in der ModData, Downed bei eigenem Wert unter X. AUS (Vorgabe, Kevins Wunsch) -> Engine-unsterblich aus,
  der Baer kann echt sterben.

### 3.5 Mehr Leben, mehr Schaden, Ausdauer

- Leben: `health` bleibt 0..1. "Mehr HP" geht nur ueber kleineren Schaden: `healthLossMultiplier` (Definition, fest je Art)
  oder Gen `resistance` (je Tier, `getHealthLoss` Offset 13-37). Fuer Zombie- und Banditenschaden rechnen wir ohnehin selbst.
- Schaden: `baseDmg * Gen strength` (`HitByAnimal` Offset 4-9). Angreifen kann ein Tier nur im Zustand `attack`, den `buck` nicht
  hat (`tier_spez.md` 5.3); das klaert der Lauf baer-kampf.
- Ausdauer: kein Ausdauer-System fuer Tiere (kein `ENDURANCE` in `IsoAnimal`, `AnimalData`, `BaseAnimalBehavior`). Ganz unseres.

---

## 4. Begleiter

### 4.1 Leitseil (Vanilla)

| Punkt | Fundstelle |
|---|---|
| Nur mit `canBeAttached = true` (Vorgabe false) und einem Seil je Tier | `ISAnimalContextMenu.lua`:173-184 |
| Anbinden ist eine Timed Action, `complete` haengt das Tier an | `ISAttachAnimalToPlayer.lua`:40-46 |
| Seil wandert in die Haupthand | `AnimalData.setAttachedPlayer` Offset 7-37 |
| Folgt alle 150 Ticks: ueber 2 Kacheln wenn der Spieler geht, ab 4 wenn er steht; **ab 15 reisst das Seil** | `BaseAnimalBehavior.followChr` Offset 67-214 |
| Wege mehr als 15 Kacheln vom Spieler sind verboten | `IsoAnimal.canGoThere` Offset 53/123 |
| Nimmt der Spieler etwas anderes in die Haupthand, fallen ALLE Seile | `IsoPlayer.checkAnimalAttachedToRope` Offset 0-29 |
| Mit Tier am Seil wird der Spieler gebremst | `IsoPlayer.calculateWalkSpeed` Offset 89-118 |
| Seil wird nicht gespeichert (nur der Baum: `IsoAnimal.save`) | `IsoAnimal.save`/`load`, `IsoPlayer` ohne Speichern von `attachedAnimals` |

Fuer ein Baby passt das; fuer einen kaempfenden Begleiter nicht (Waffe = Seil weg).

### 4.2 Folgen ohne Seil

- **Locken** mit Futter in der Hand: das Tier laeuft hinterher, solange der Spieler lockt (`IsoAnimal.tryLure`, `updateLured`, Lesung).
- **Eigene Lua:** `pathToLocation`/`pathToCharacter` am Tier hat **keine** Lua-Fundstelle in Vanilla (grep 0). Belegt ist nur
  `animal:fleeTo(sq)` (`ISMilkAnimal.lua`:38) -- das RENNT immer und loest das Seil (`IsoAnimal.fleeTo` Offset 32-65). Nach der
  eisernen Regel braucht ein Gehen per `pathToLocation` Kevins Wort mit Jar-Beleg (oeffentliche Methode, prueft die
  Seil-Grenze, `IsoAnimal.pathToLocation`, Lesung).
- **Idee aus Companion Dogs** (Workshop 3740052292, Mechanik aus CLAUDE.md Abschnitt 5 nacherzaehlt, nichts uebernommen): dort
  schiebt der Besitzer-Client den Hund per eigenem Serverbefehl mit `setX/setY` hinterher, ohne Wegfindung. Die Einzelheiten
  stehen in `recherche_dogs.md`.

### 4.3 Besitzer und Vertrauen

- **Besitzer: gibt es nicht.** Anleinen, Aufheben (`ISPickupAnimal.lua`:5-48), Toeten (`ISKillAnimal.lua`), Zerlegen fragen
  niemanden. Im MP kann jeder Fremde den Baeren anleinen oder toeten -- unsere Mod muesste diese Menues fuer fremde Baeren sperren.
- **Vertrauen** (`acceptance`) haengt an der `getOnlineID()` des Spielers (`IsoAnimal.getAcceptanceLevel` Offset 5-47) und wird so
  gespeichert (`IsoAnimal.save` Offset 632-690). Im MP ist die Online-Id eine Sitzungsnummer; als Besitzmerkmal ungeeignet
  (Stabilitaet ueber Sitzungen **ungeprueft**). Fuer "Zaehmen" brauchbar als Anzeige, nicht als Besitz.
- **Stabile Kennung des Tiers:** `getAnimalID()`, gespeichert (`IsoAnimal.save` Offset 203), auf Client und Server gleich
  (NPC Crew Sonde, `_docs/diag_konsolen_2026-10-12_mp/testaccount-console.txt`: "gleich 5, verschieden 0").
- **ModData** des Tiers wird gespeichert und geladen (`IsoAnimal.save` Offset 163-167, `load` Offset 227). Dort koennen Besitzer
  (Benutzername), Level und XP stehen. Belegt: `animal:getModData()` (`ISInventoryPaneContextMenu.lua`:4154).

### 4.4 Speichern, Laden, Chunk entladen

- Tiere liegen in der Kartendatei ihrer Kachel und werden beim Laden der Kachel neu gebaut (`IsoGridSquare.load` Offset 94-240).
  Der Baer bleibt also dort, wo der Spieler ihn verlassen hat, samt ModData.
- Beim Entladen auf dem Client: aus der Verwaltung genommen (`IsoChunk.removeFromWorld` Offset 303-327). Zeit ausserhalb einer
  Zone: eingefroren (2.4).
- Ein Spielstand ohne die Mod mit gespeichertem Baeren wirft beim Laden (`tier_spez.md` 6.3).

### 4.5 Auto

- Nur im Tier-Anhaenger: `ISVehicleMenu.lua`:665-790, passt nur wenn `trailerBaseSize * Groesse` <= freier Platz (500).
- Als Jungtier auf dem Arm: `canBePicked` und Gewicht < 40 + 7 * Staerke (`IsoAnimal.canBePicked` Offset 20-42) wird es ein
  Gegenstand `Base.Animal` (`ISPickupAnimal.lua`:46-48). Ob man damit ins Auto steigen kann: **ungeprueft**.

### 4.6 Teleport

Kein Vanilla-Weg holt ein Tier zum Spieler; das Seil reisst stattdessen (4.1). Kevins rote Linie (keine zufaelligen
Teleports) gilt hier genauso. Bleibt der Baer zurueck, wartet er in seinem Chunk (4.4). Ein "Herholen"-Knopf waere ein
bewusster Spielerklick, kein Automatismus -- Entscheidung Kevins.

---

## 5. Mehrspieler

| Punkt | Fundstelle |
|---|---|
| Auf dem Client laufen weder Verhalten noch Hunger/Wachsen: nur Kollision und Bewegung | `IsoAnimal.updateInternal` Offset 23 (`GameClient.client`), Verhalten Offset 90, Daten Offset 97 nur im anderen Zweig |
| Schaden durch Waffen nur auf dem Server | `IsoAnimal.hitConsequences` Offset 0 |
| Client bekommt laufend: Alter, Gewicht, Stress, Durst, Hunger, Gesundheit (1/100), Name | `NetworkPlayerAI.parse(AnimalPacket)` Offset 1079-1183 |
| **Nicht** laufend: Groesse, ModData, unsterblich | Felder von `AnimalPacket` (javap); Groesse und ModData nur in der Vollantwort `AnimalUpdatePacket` (ruft `IsoAnimal.save` Offset 227 / `load` Offset 446) auf Anfrage des Clients |
| Was ein Client lokal am Tier aendert, ueberschreibt das naechste Paket | wie oben (`setHealth` Offset 1183) |
| Debug-Befehle (Spawnen, Unsterblich, Toeten, Alter) brauchen `AnimalCheats` | `ClientCommands.lua`:753-936 |
| `AnimalCommandPacket` braucht `AnimalCheats`, der Server verarbeitet davon nur `UpdateGenome` | PacketSetting (javap -v), `processServer` Offset 8-15 |
| Normale Handgriffe (Fuettern, Traenken, Streicheln, Seil) sind Timed Actions, `complete` laeuft auf dem Server; keine Faehigkeit noetig | z. B. `ISFeedAnimalFromHand.lua`:45-49, `ISPetAnimal.lua` `serverStart` |
| Treffer Spieler->Tier: Pruefungen `HitDamage`, `HitLongDistance`, `HitWeapon` | `PlayerHitAnimalPacket` PacketSetting |

Folgen fuer den Bau:
- **Alles, was den Baeren steuert (Folgen, Downed, Level, Zombieschaden), gehoert auf den Server** (und im Einzelspieler in
  den einen Rechner). Das ist das Gegenteil der NPC-Crew-Begleiter, deren KI der Client mit Hoheit rechnet.
- `OnZombieUpdate` laeuft auf dem dedizierten Server nie (CLAUDE.md v3.9.42); also `OnTick`/`EveryOneMinute` und Tiere ueber
  `getAnimal(onlineId)` (`ClientCommands.lua`:767) oder `sq:getAnimals()` (`ISVehicleMenu.lua`:779) finden.
- **Baer bekommen** im MP: eigener Serverbefehl, der auf dem Server `addAnimal` + `addToWorld` ruft wie `ClientCommands.lua`:759.
  Unser eigener Befehl braucht keine Faehigkeit, aber eine eigene Regel ("einer je Spieler", Besitzpruefung -- CLAUDE.md
  v3.7.53: jeder Empfaenger prueft den Besitz).
- Groesse und Level an Clients: selbst schicken (eigenes Serverpaket), sonst sieht der Client bis zum naechsten Vollabgleich die
  alte Groesse. **Ungeprueft**, wie oft dieser Vollabgleich kommt.

---

## 6. Offene Fragen fuer Kevins Test (nur das, was Lesen nicht entscheidet)

1. Wie sieht der Baer bei Groesse 0,4 und bei 2,0 aus (`setSizeForced`)? Rutschen die Fuesse?
2. Passt ein grosser Baer durch Tueren und Zauntore?
3. Was passiert beim Streicheln ohne `petbear.xml`?
4. Sitzt er stabil, wenn wir `idleAction = "sit"` halten (Downed-Pose)?

Statisch gelesen, nicht gespielt.
