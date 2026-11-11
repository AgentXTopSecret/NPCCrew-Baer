# Lauf baer-b1d: Forschung (B1d Wachsen, Werte, Faehigkeiten, Heilen-Vorbereitung, Anzeige, Bench)

Stand 11.11.2026 Nachtschicht. **Statisch gelesen, nichts gebaut, nichts gespielt.** Rolle: Forschung (kein Code im Staging).
Jede Laufzeit-Aussage ohne Spielbeleg ist "ungeprueft".

Schreibweise wie `forschung_b1c.md` (kurz `FC`):
- `V:` = Vanilla-Lua `.../ProjectZomboid/media/lua/` (42.22.2). `B:` = Bandits `.../Bandits/42.22/media/lua/`.
- `NC:` = NPC Crew `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua/` (nur Lernquelle, kein Engine-Beleg, nichts kopiert).
- `T:` = Test-Mod `NCBearTest/42/media/lua/`. `S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/` (B1a + B1b + B1c).
- `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`. `PB1C` = `PLAN_B1C.md`.
- `dec/`, `dec_b1b/`, **`dec_b1d/` (neu)** = Vineflower-Auszuege 42.22.2; `javap/b1d_ModelSlotRenderData.txt` (neu); Klassen dazu in
  `jar_b1d/` (neu, aus `projectzomboid.jar` mit Python zipfile gezogen). **NUR JAR** = Lesehilfe, kein Engine-Beleg.
- **BELEGT** = echter Aufruf in Vanilla-Lua oder Bandits mit gleichen Argumenttypen. **ERLAUBT** = Kevins Wort je Methode
  (`pathToLocation`, `setVariable("animalRunning", false)`; fuer B1d nicht noetig).
- Bandits beruehrt Tiere nirgends (grep `IsoAnimal`/`setSizeForced`/`getAnimalSize` in `42.22/media/lua` und `common/media`: 0 Treffer).
  Alle Tier-Belege kommen aus Vanilla.

---

## 0. Kernbefunde vorweg

1. **Groesse setzen ist BELEGT, auf beiden Seiten:** `animal:getData():setSizeForced(zahl)` am Schreiber
   (`V:shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70` complete -> `V:shared/Definitions/animal/ButcheringUtil.lua:586`) und am
   Client (`V:client/ISUI/Animal/ISButcherHookUI.lua:520` -> `ButcheringUtil.lua:535` -> `:569`/`:571`; `ISButcherHookUI.lua:530` -> `:586`).
   Lesen `animal:getData():getSize()` (`V:client/ISUI/Animal/ISAnimalUI.lua:31`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:28`).
   Grenzfall ehrlich: Vanilla ruft es nur an Haken-Tieren; an einem lebenden Tier in der Welt nur unsere Test-Mod (`T:client/NCBearSize.lua:27`,
   ob gespielt: ungeprueft).
2. **Die Engine setzt die Groesse von selbst zurueck, solange die Definition `minSize = maxSize = 0.35` hat**
   (`S:shared/BanditsNPCBearDefs.lua:75-76`): `setSize` klemmt IMMER auf [min, max] (NUR JAR `dec/AnimalData.java:1539-1542`), und
   `setSize` laeuft (a) einmal je Alterstag in `growUp` (`:218-235`, aus `update` `:144-158`), (b) beim LADEN jedes Spielstands
   (`dec/IsoAnimal.java:1413`), (c) im MEHRSPIELER bei der Erst-Uebertragung an jeden Client (Server `animal.save`, Client `animal.load`:
   `dec_b1b/AnimalUpdatePacket.java:72`, `:177`), (d) in einer Tierzone nach Abwesenheit (`updateStatsAway` -> `init` -> `initSize`,
   `dec/IsoAnimal.java:1681-1715`, `dec/DesignationZoneAnimal.java:281-297`). `setSizeForced` umgeht die Klemme nur bis zum naechsten
   dieser Ereignisse. **Empfehlung: Definition auf `minSize = 0.35`, `maxSize = 1.35`, Stufe `ageToGrow` sehr gross** (1.4), dann ueberlebt
   die gesetzte Groesse Laden und Erst-Uebertragung, und die Engine waechst selbst praktisch nicht.
3. **Im Mehrspieler kommt eine spaetere Groessen-Aenderung des Servers NIE beim Client an:** das laufende Tierpaket traegt Alter, Gewicht,
   Stress, Durst, Hunger, Leben, aber keine Groesse (NUR JAR `dec_b1b/AnimalPacket.java:21-82`, `:154-159`; Client `dec_b1b/NetworkPlayerAI.java:480-488`);
   die volle Uebertragung (mit Groesse) gibt es nur, wenn ein Client das Tier zum ersten Mal sieht (`dec_b1b/AnimalUpdatePacket.java:60-79`,
   `:141-177`). Also: **der Client setzt die Groesse seiner Kopie selbst** aus der Sicht (`setSizeForced` am Client ist belegt, Punkt 1) --
   nur Anzeige und Kollision seiner Kopie, nichts geht zum Server.
4. **Was mit der Groesse mitwaechst** (NUR JAR): Bild (`ModelSlotRenderData` Offset 452-455 `finalScale = AnimalData.getSize()`,
   `javap/b1d_ModelSlotRenderData.txt:746-752`), Kollisionsbreite `collisionSize x Groesse` (`dec/IsoAnimal.java:420` Client, `:433` Schreiber),
   Schatten (`:1087-1089`), Anbau-Punkte (`:2602`), Anhaenger-Platz (`:2795`). **Nicht mit:** Lauf-Tempo (Weg kommt aus dem Clip; im ganzen Jar
   liest keine Bewegungs-/Wegfindungs-Klasse die Groesse, Abschnitt 1.2) -> ein groesseres Junges macht laengere Schritte bei gleichem Weg =
   Fussgleiten (ungeprueft, Kevins Blick); Futterbedarf (Hunger haengt nur an `hungerMultiplier`, beim Jungen 0, `dec/AnimalData.java:347-367`, `:694-707`).
5. **Engine-Alter und Engine-Stufen taugen nicht** (Abschnitt 2): Stufenwechsel baut ein NEUES Tier ohne ModData (`dec/AnimalData.java:1381-1443`),
   das Alter zaehlt nur, solange das Tier geladen ist und rechnet (`:136-150`), Sandbox "Animal age" vervielfacht es (`:207-216`), und B1c baut
   den Koerper bei Mitfahren / Call to me neu (`S:server/BanditsNPCBearRide.lua:67-90`) -> Engine-Alter 1. **Unsere Uhr steht im Register.**
6. **Leben am Tier lesen/setzen ist BELEGT:** `animal:getHealth()` (`V:client/ISUI/Animal/ISAnimalUI.lua:15`; im SP gespielt: Kevins Probe
   "Baer-Leben 1,000 unveraendert", ENT:60 ueber `T:client/NCBearAttackProbe.lua:104`), `animal:setHealth(zahl)` (SP-Zweig
   `V:client/ISUI/Animal/ISAnimalContextMenu.lua:545`, Server `V:server/ClientCommands.lua:932`, `V:shared/TimedActions/Animals/ISKillAnimal.lua:58`)
   -- Vanilla setzt nur 0, der Typ (Zahl) ist gleich. **Das Engine-Leben ist ein Anteil 0..1** (Vorgabe 1,0 `dec_b1b/IsoGameCharacter.java:574`,
   Engine-Heilung deckelt bei 1,0 `dec/AnimalData.java:395`) und reist im MP als **Byte = Leben x 100** (`dec_b1b/NetworkPlayerAI.java:280`,
   `dec_b1b/AnimalPacket.java:58`). **Ueber 1,27 laeuft das Byte ueber** (Client bekaeme ein negatives Leben). Also: Engine-Leben = Anteil am
   eigenen Hoechstwert, nie Punkte.
7. **Die Engine heilt das Junge schon selbst:** je Spielstunde `+ healthLossMultiplier x (1,5 - Gen resistance) / 3` (`dec/AnimalData.java:377-398`,
   `:472-489`), Vorgabe 0,05 (`dec/AnimalDefinitions.java:62`), Gen meist 0,2..0,6 (`dec_b1d/AnimalGenomeDefinitions.java:15-16`) -> **rund
   1,5-2,2 % je Spielstunde** (Rand 0,4-2,4 %), nur solange geladen, nur nicht-wilde Tiere (unser Junges ist nie engine-wild, `S:...Defs.lua:88`).
   Eine eigene "1 % je Stunde" kaeme OBENDRAUF. Weg in 5.2.
8. **Ein neu erzeugter Koerper (Mitfahren, Call to me) hat Groesse 0,35 und Leben 1,0** (`initSize` `dec/AnimalData.java:1353-1358`,
   Vorgabe-Leben `dec_b1b/IsoGameCharacter.java:574`) -> `B.PlaceCub` muss Groesse UND Leben aus dem Register sofort setzen, sonst heilt jede
   Autofahrt voll.
9. **NPC Crew fuehrt Faehigkeiten als EINE Zahl (XP) je Faehigkeit, die Stufe wird daraus gerechnet**, mit sanfter Kurve (2:1) und einer
   Echtzeit-Obergrenze je Minute, die nie gespeichert wird (`NC:shared/BanditsNPCSkills.lua:52-59`, `:129-182`, `:475-565`). Ausweichen ist
   dort KEINE Faehigkeit, sondern fester Sandbox-Wert (`:966-975`). Lehren in 4.1.
10. **Anzeige-Seite erweitern geht mit `addComboBox` + `addItem`** (reines Vanilla-Lua `V:client/PZAPI/ModOptions.lua:121-156`; `getValue` =
    Index; NPC Crew benutzt es gespielt `NC:client/BanditsNPCModOptions.lua:97-103`). Die B1c-Seite hat den Platzhalter schon
    (`S:client/BanditsNPCBearOptions.lua:58-62`).
11. **Kondition durch Rennen braucht keinen neuen Engine-Aufruf:** unser `B.MoveTo` merkt schon, ob WIR rennen lassen (`s.walk`, `s.ownUntil`,
    `S:server/BanditsNPCBearWorld.lua:828-874`); der Weg je Hirn-Takt kommt aus den Lagen, die `liveRec` ohnehin liest
    (`S:server/BanditsNPCBearServer.lua:741`).
12. Namen frei: grep NPC Crew `42/media` nach `BearGrow|BearDodge|BearHeal|BearFight|BearCarry|BearStamina|BearNose|BearFish|BearSkill|BearXP|BearStats|BearAge|BearHealth`:
    0 Treffer (11.11.). NPC Crew hat keine Datei `BanditsNPCBear*`.

---

## 1. Wachsen und Modellwechsel (Auftrag 1 und 2)

### 1.1 Engine-Wege (Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Datenteil des Tiers | `animal:getData()` | `V:shared/Definitions/animal/ButcheringUtil.lua:566`, `:569` | beide | **BELEGT** |
| Groesse setzen (ohne Klemme) | `animal:getData():setSizeForced(zahl)` | Schreiber: `V:shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70` (complete) -> `ButcheringUtil.lua:586`; `ButcheringUtil.lua:674` (`if isServer()`) -> `:586`. Client: `V:client/ISUI/Animal/ISButcherHookUI.lua:520` -> `ButcheringUtil.lua:535` -> `:569`, `:571`; `ISButcherHookUI.lua:530` -> `:586` | SP, Server, Client | **BELEGT** (Zahl). Grenzfall: Vanilla nur an Haken-Tieren |
| Groesse lesen | `animal:getData():getSize()` | `V:client/ISUI/Animal/ISAnimalUI.lua:31`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:28`; am Tier in `T:shared/NCBearFight.lua:250` | beide | **BELEGT** |
| Groesse mit Klemme | `getData():setSize(x)` | kein Vanilla-Lua-Aufrufer (grep) | - | **nicht nehmen** |
| Weltstunden (Uhr) | `getGameTime():getWorldAgeHours()` | `V:server/Traps/STrapSystem.lua:77`; S: `B.Now` `S:shared/BanditsNPCBear.lua:318-320` | Schreiber | **BELEGT** (B1a) |
| seltener Takt | `Events.EveryTenMinutes.Add` (heute `B.SlowTick`) bzw. `Events.EveryHours.Add` | `V:server/Traps/STrapSystem.lua:134` / `:133`; S: `S:server/BanditsNPCBearServer.lua:1022` | SP + Server | **BELEGT** |
| Gewicht mitwachsen (wahlfrei) | `animal:getData():setWeight(zahl)` | `V:shared/Definitions/animal/ButcheringUtil.lua:566` | Schreiber | **BELEGT**; Gewicht reist im Tierpaket (`dec_b1b/NetworkPlayerAI.java:278`, `:482`) |

### 1.2 Was die Engine mit der Groesse macht (alles NUR JAR)

| Wirkung | Fundstelle | Folge fuer B1d |
|---|---|---|
| `setSize` klemmt auf [getMinSize, getMaxSize]; `setSizeForced` nicht (merkt `originalSize`) | `dec/AnimalData.java:1539-1547` | nur `setSizeForced` hebt ueber `maxSize` |
| min/max = Definition, ausser Gen `maxSize` (haben wir nicht, `S:...Defs.lua:28-36`) | `dec/AnimalData.java:1717-1751` | Grenzen = genau die Def-Zahlen |
| je Alterstag `growUp`: `setSize(min(max, size + (max - min) / ageToGrow x Leben))`, in kleiner Tierzone /8 | `dec/AnimalData.java:218-235`, gerufen `:144-158` | bei min = max: zurueck auf 0,35 einmal je Spieltag |
| `ageToGrow` der Stufe x Gen-Faktor (Gen fehlt -> 1,0) | `dec_b1d/AnimalGrowStage.java` (getAgeToGrow); geparst als Ganzzahl `dec/AnimalDefinitions.java:813-814` | sehr gross -> Engine-Wachsen ~0 |
| neues Tier / `init`: `initSize` endet mit `setSize(0.1)` -> minSize | `dec/AnimalData.java:1353-1358`, `:1455-1460`; `dec/IsoAnimal.java:1478-1499` (`:1490`) | jeder neue Koerper startet bei 0,35 |
| Speichern schreibt die Groesse, Laden liest sie mit `setSize` (Klemme) | `dec/IsoAnimal.java:1299` / `:1389` (init) + `:1413` | bei min = max: nach jedem Laden 0,35 |
| MP-Erstuebertragung = save/load | `dec_b1b/AnimalUpdatePacket.java:60-79` (Server), `:153-177` (Client) | dieselbe Klemme beim Client |
| laufendes Tierpaket ohne Groesse | `dec_b1b/AnimalPacket.java:21-82`, `:116-160`; `dec_b1b/NetworkPlayerAI.java:277-282`, `:480-488` | Client-Kopie bleibt bei der Erst-Groesse |
| Tierzone nach Abwesenheit: `updateStatsAway` -> `growUp(true)` je Mitternacht und am Ende `init()` | `dec/IsoAnimal.java:1681-1715`; `dec/DesignationZoneAnimal.java:281-297` | Groesse = minSize, nur in einer Spieler-Tierzone |
| Debug "Alter setzen": `setAgeDebug` -> `init()` | `dec/IsoAnimal.java:1583-1587`; V: Debug-Menue `ISAnimalContextMenu.lua:967`, Server-Cheat `ClientCommands.lua:986` | nur Cheat; Groesse = minSize |
| `data.update()` (Alter, Stunden, growUp, Heilung) laeuft nur beim Schreiber | `dec/IsoAnimal.java:416-462` (Client-Zweig `:419-428` ohne `data.update`, Schreiber `:430-431`) | Client wird nie von der Engine zurueckgesetzt (nur durch Neu-Laden der Kopie) |
| Bild: `finalScale = AnimalData.getSize()` | `javap/b1d_ModelSlotRenderData.txt:746-752` (Offset 440-455); Vorarbeit `baer/spiel/tier_spez.md:184` | Bild folgt sofort, auch am Client |
| Kollisionsbreite `collisionSize x Groesse` (0,24 x 0,75 = 0,18; x 1,35 = 0,32) | `dec/IsoAnimal.java:420` (Client), `:433` (Schreiber) | waechst mit, je Seite aus der eigenen Kopie |
| Schatten, Anbau-Punkte, Anhaenger-Platz, Fleisch/Teile | `dec/IsoAnimal.java:1087-1089`, `:2602`, `:2795`, `:3475-3500`; `dec_b1b/IsoGameCharacter.java:6601` | waechst mit (harmlos) |
| Gewicht als Gegenstand `baseEncumbrance x Groesse` | `dec_b1d/AnimalInventoryItem.java:100` | egal (`canBePicked = false`) |
| Tempo: kein Bewegungscode liest die Groesse | Byte-Suche im ganzen Jar: `AnimalData.getSize` nur in `AnimalData`, `IsoAnimal`, `ModelSlotRenderData` (`IsoGameCharacter`/`BaseVehicle` per javap gegengeprueft: kein `AnimalData.getSize`); `getAnimalSize` nur in Bild-/Schatten-/Leichen-Klassen und `PathFindBehavior2:678` (Leiche greifen); Clip-Tempo `baer/spiel/tier_spez.md:226-237` | **Fussgleiten-Risiko** beim Wachsen (ungeprueft) |
| Futter/Hunger | `dec/AnimalData.java:347-367`, `:694-707` (nur `hungerMultiplier`, Gene, Sandbox) | Groesse aendert den Bedarf nicht |
| Streichel-Haltung Vanilla `AnimalSizeY = (size - min) / (max - min)` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:26-32` | unsere Zeitaktion setzt fest 0,5 (`S:shared/TimedActions/BanditsNPCBearPetAction.lua:58`); mit min < max koennte sie mitwachsen (Vorschlag, Wirkung ungeprueft) |

### 1.3 Zwei Wege fuer die Definition (Planer entscheidet; Empfehlung B)

| | A: Definition bleibt (min = max = 0,35) | **B: min 0,35 / max 1,35 / ageToGrow gross** |
|---|---|---|
| Daily `growUp` | setzt 0,35 zurueck -> Schreiber muss oft nachsetzen (Hirn-Takt-Probe, sonst bis zu 10 Spielminuten klein) | `size + (1,0 / 36500) x Leben` -> bleibt praktisch |
| Laden (SP) | kurz 0,35, bis der erste Takt bindet und nachsetzt (2-3 Hirn-Takte, ungeprueft) | gespeicherte Groesse bleibt |
| MP-Erstuebertragung | Client sieht 0,35 bis zur eigenen Client-Probe | Client sieht sofort die Server-Groesse |
| spaetere Aenderung im MP | Client setzt selbst (Punkt 0.3) | Client setzt selbst (Punkt 0.3) -- gleich |
| Tierzone / Debug-Alter | zurueck auf 0,35 -> Nachsetzen | zurueck auf 0,35 -> Nachsetzen -- gleich |
| Nebenwirkung | Vanillas `max - min = 0` (Falle `forschung_engine.md:149`) bleibt | Falle weg; neue Junge starten weiter bei 0,35 (`initSize`); Bestand mit 0,35 laedt als 0,35 |
| Vorschlag Werte | - | `minSize = 0.35`, `maxSize = 1.35`, `stages[CUB] = { ageToGrow = 36500 }` (100 Jahre; Ganzzahl-Parser `dec/AnimalDefinitions.java:814`) |

Beide Wege brauchen das **Nachsetzen beim Schreiber** (Probe `math.abs(a:getData():getSize() - ziel) > 0.002` -> `setSizeForced(ziel)`) und die
**Client-Probe im MP**. B macht beides selten noetig. Die Def-Datei ist keine alte `NCBear*`-Datei (Auftrag erlaubt), wird aber nur beim
Spielstart gelesen (`S:...Defs.lua:4-5`) -> Neustart. Uebernahme-Skript: keine Cheat-Regel betroffen (`baer/tools/baer_uebernahme.py:175-198`).

### 1.4 Wachstums-Uhr (Vorschlag)

- **Register-Feld `g` = Wachstum 0..1** (wie `begleiter/PLAN.md:84-89` "unser Zaehler"), nur Zahl, auch im Spiegel. Im Langsam-Takt
  (`slowRec`, `S:server/BanditsNPCBearServer.lua:484-516`; `dt` in Weltstunden, je Schritt gedeckelt `maxDtH` 1,0 `:565-570`):
  `g = min(1, g + dt / (D x 24))`, D = `BearGrowDays`. Nur `st == "tame"` (wild/scheu/angefuettert: nie; Kevin "ab dem Zaehmen", Auftrag).
- Warum ein Anteil statt "Stunden seit tamedAt": ein Sandbox-Wechsel von D aendert nur das kuenftige Tempo -- kein Sprung, kein Schrumpfen
  (bei "Stunden / D" wuerde ein groesseres D einen fertigen Baeren wieder kleiner machen). Deckel: `g <= 1`.
- Migration (`B.InitRegistry`, `S:server/BanditsNPCBearRegistry.lua:98-183`): gezaehmt ohne `g` -> `g = clamp((B.Now() - tamedAt) / (D x 24), 0, 1)`
  (`tamedAt` setzt `B.TameCheck`, `S:shared/BanditsNPCBearRules.lua:75`); unlesbar -> 0 und eine Fehlerzeile.
- Vermisst (`missing`): `slowRec` kehrt dort heute frueh zurueck (`:485-491`) -> Wachstum steht still. Mitfahren (`ride`): laeuft weiter.
- MP und abwesender Besitzer: Frage F4 (Empfehlung wie die Uhren in B1a: nur, solange der Besitzer im Spiel ist, `online[rec.owner]`).
- **Fuetter-Bonus** (klein, gedeckelt): in `B.FeedComplete` Zweig `wasTame` (`S:server/BanditsNPCBearServer.lua:243-246`; die Abklingzeit
  120 min gilt schon) z. B. `g + feedGrowH / (D x 24)` mit `feedGrowH` 3 Spielstunden, hoechstens `feedGrowDay` 2 je Spieltag, Summe
  `gF <= feedGrowMax` 10 % von D (Felder `gF`, `gFd`, `gFn` im Register). Bestes Fuettern: 25 % schneller, bis 10 Tage frueher. Alles Stellwerte.

### 1.5 Kurve (Vorschlag): stueckweise gerade durch Kevins Tabelle (ENT:199-204), anteilig in x = g

| x = g | 0 | 0,15 | 0,45 | 1,0 |
|---|---|---|---|---|
| Groesse innen | 0,35 | 0,75 | 1,0 | 1,35 |
| bei D = 100 | Tag 0 | Tag 15 | Tag 45 | Tag 100 |
| Zuwachs je Tag (D = 100) | 0,0267 | 0,0083 | 0,0064 | - |

Vorne schneller, hinten langsamer (4,2 : 1,3 : 1), Meilensteine exakt, bei anderem D anteilig. Je Spielstunde am Anfang +0,0011 -> unsichtbar
kleine Schritte. (Alternative glatt: `0,35 + x^0,48` trifft Tag 15 / 45 nur ungefaehr; Kahlua kennt `^`, die gerade Form braucht ihn nicht.)

### 1.6 Wann setzen, wo, welche Seite (Vorschlag)

| Wann | Wer | Was |
|---|---|---|
| Langsam-Takt (10 Spielminuten) | Schreiber | `g` fortschreiben, `B.Commit` hoechstens je Spielstunde (jedes Commit = r + 1 = neuer Spiegel + Sicht, `S:...Registry.lua:413-424`) |
| Hirn-Takt (1,5 s), je geladenem zahmen Jungen | Schreiber | Probe `getSize` gegen Ziel, nur bei Abweichung `setSizeForced` (2 Java-Aufrufe je Junges, kein Bild-Takt) |
| `B.PlaceCub` (Aussteigen, Call to me) | Schreiber | sofort Groesse UND Leben setzen (`S:server/BanditsNPCBearRide.lua:67-90`) |
| Binden nach Laden/Heilung (`bind`, `S:server/BanditsNPCBearHeal.lua:85-112`) | Schreiber | dasselbe (sonst bis zum naechsten Hirn-Takt) |
| Hud-Liste (<= 1 x je s, `S:client/ISUI/BanditsNPCBearHud.lua:289-387`) | **nur MP-Client** (`isClient()`) | Kopie aus `S.objs`: `|getSize - v.sz| > 0.002` -> `setSizeForced(v.sz)`; im SP ist die Kopie das Schreiber-Objekt -> nichts |

Gesetzt wird immer die **gezeigte** Groesse `sz = min(innen, cubMaxSize)` (1.7), die Werte rechnen mit der **inneren**.

### 1.7 Modellwechsel vorbereiten, abgeschaltet (Auftrag 2)

- Stellwerte `B.CFG.cubMaxSize = 0.75` (Auftrag) und `B.CFG.bodySwap = false`. Eine Funktion entscheidet Koerper und gezeigte Groesse,
  z. B. `B.BodyOf(rec)` -> `"cub", sz`; mit `bodySwap` spaeter `"adult"` ab `cubMaxSize`.
- Der spaetere Tausch geht ueber den belegten B1c-Weg: altes Tier `B.RemoveCub`, neues ueber `B.PlaceCub` an derselben Kachel, `gen + 1`
  (alte Kopie wird "stale", PB1C 0.2). Das Uebernahme-Skript erlaubt `B.CreateCub` nur aus `B.AppearFor` und `B.PlaceCub`
  (`baer/tools/baer_uebernahme.py:262-264`) -- passt. Offen fuer den spaeteren Lauf: `B.CreateCub` kennt nur `B.CUB`
  (`S:server/BanditsNPCBearWorld.lua:466-478`), `B.RecOf`/Suchlauf fragen `getAnimalType() == B.CUB` (`S:...Registry.lua:334`).
- **Nie die alte Art `bear`** (NCBearFight greift sofort an, Auftrag; `forschung_bestand.md:23`).
- Namensschild-Hoehe: `B.CFG.tagZ` 0,18 ist fuer 0,35 gemessen (`S:shared/BanditsNPCBear.lua:53-55`, Anker `S:client/ISUI/BanditsNPCBearHud.lua:439-453`);
  Vorschlag `tagZ x sz / 0.35` (Kopfhoehe waechst linear mit dem Massstab; Wert im Spiel ansehen).
- Rest-Risiken beim Wachsen bis 0,75 (alles ungeprueft): Fussgleiten (1.2), Streichel-Haltung "lamb" (feste Hoehe), Folgen-Abstaende
  `followNear` 3 / `followStart` 4,5 (`S:shared/BanditsNPCBear.lua:70`) bei 1,5 m Koerperlaenge noch ok.

---

## 2. Engine-Alter und -Stufen: warum NICHT (Auftrag "Alter/Stufen der Engine")

| Engine-Teil | Fundstelle (NUR JAR) | Warum nicht fuer uns |
|---|---|---|
| Stufenwechsel `checkStages` -> `grow(nextStage)` | `dec/AnimalData.java:118-134`, `:1381-1443` | baut ein NEUES `IsoAnimal` der naechsten Art (`:1388`), loescht das alte (`:1430`); ModData (unser Spiegel) wird NICHT kopiert (nur Alter, Seil, Vertrauen, Name, AnimalID `:1389-1404`) -> Bindung und Spiegel weg; die naechste Art waere der alte Erwachsene |
| `isBaby()` = Stufe hat `nextStage` | `dec/IsoAnimal.java:1775-1777` | Babys trinken nicht selbst usw. (`begleiter/recherche_spiel.md:64-65`); wir bleiben "kein Baby" |
| Alter `age` / `hoursSurvived` | `dec/AnimalData.java:136-150`, `:1445-1449` | zaehlt nur, solange `data.update` laeuft (geladen, Schreiber, `dec/IsoAnimal.java:430-431`); ausserhalb einer Tierzone steht es still |
| Sandbox "Animal age" | `dec/AnimalData.java:207-216` (90 / 10 / 5 / 1) | wuerde Kevins 100 Tage verfaelschen |
| neuer Koerper | `dec/IsoAnimal.java:1537-1544` (`initAge` -> 1) | B1c erzeugt bei Mitfahren / Call to me neu (`S:server/BanditsNPCBearRide.lua:67-90`) -> Alter 1 |
| Engine-Wachsen | `dec/AnimalData.java:218-235` | linear, mal Leben, /8 in kleiner Tierzone -- keine Kurve "vorne schneller" |
| Tierzone | `dec/IsoAnimal.java:1681-1715` | setzt Groesse auf minSize |

Folge (wie `begleiter/PLAN.md:83-89`, `recherche_spiel.md:62-71`): eine Art `ncbearcub` mit einer Stufe ohne `nextStage`
(`S:shared/BanditsNPCBearDefs.lua:64-65`), Wachstum nur ueber unser Register, die Engine bekommt nur die Groesse.

---

## 3. Werte, die jeden Tag mit der Groesse steigen (Auftrag 3)

### 3.1 Leben am Tier

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| lesen | `animal:getHealth()` | `V:client/ISUI/Animal/ISAnimalUI.lua:15`; gespielt im SP `T:client/NCBearAttackProbe.lua:104` (ENT:60) | beide | **BELEGT** |
| setzen | `animal:setHealth(zahl)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:545` (SP-Zweig), `V:server/ClientCommands.lua:932` (Server), `V:shared/TimedActions/Animals/ISKillAnimal.lua:58` | SP + Server | **BELEGT** (Zahl; Vanilla setzt nur 0 -- Werte 0..1 nur aus dem Jar) |
| Wertebereich 0..1 | - | Vorgabe `dec_b1b/IsoGameCharacter.java:574`; Engine-Heilung `min(1, ...)` `dec/AnimalData.java:395`; keine Klemme in `setHealth` `dec/IsoAnimal.java:1156-1163` | - | NUR JAR |
| MP-Uebertragung | (Engine) Byte = Leben x 100 | `dec_b1b/NetworkPlayerAI.java:280`, `dec_b1b/AnimalPacket.java:58`, `:159`, `:234`; Client `setHealth(byte / 100)` `dec_b1b/NetworkPlayerAI.java:486-488` | Server -> Client | NUR JAR; **ueber 1,27 Ueberlauf** -> nie ueber 1,0 setzen |
| Speichern/Laden | (Engine) | `dec/IsoAnimal.java:1340`, `:1451` | - | Leben bleibt am Koerper; neu erzeugter Koerper = 1,0 |
| Tod | `isDead()` (Leben <= 0) | B1a: `S:server/BanditsNPCBearServer.lua:795-797` | Schreiber | nie 0 setzen ausser fuer den Tod |

**Regel:** Engine-Leben `h` = Anteil am eigenen Hoechstwert; angezeigte Punkte = `h x hpMax`. Waechst `hpMax` jeden Tag, bleibt der Anteil
(ein voller Baer bleibt voll). Das Register fuehrt `hp` (Anteil) fuer gezaehmte Junge, damit Mitfahren/Call to me nicht voll heilen (0.8).

Engine-Schaden ueber `getHealthLoss` (NUR JAR, Wissen fuer B5a): Waffe eines Spielers `dec/IsoAnimal.java:1124-1127`, anderes Tier `:817-826`,
Unfall im Anhaenger `:2620-2628`; Fahrzeug-Treffer setzt im SP sofort 0 (`:506-521`). `setIsInvincible` ist in der Cheat-Pruefung
gesperrt (`baer/tools/baer_uebernahme.py:187-190`) -- fuer B5a "unsterblich" (ENT:24) einen anderen Weg suchen.

### 3.2 Hoechstwerte aus der inneren Groesse s (Vorschlag; stueckweise gerade zwischen den Stufen)

| s | 0,35 Jungtier | 0,75 Halbstark | 1,0 | 1,35 Erwachsen | Quelle |
|---|---|---|---|---|---|
| Leben max (Punkte) | 40 | 150 | 254 | 400 | ENT:14-19 ("Vorschlag als Vorgabe") |
| Traglast | 10 | 40 | 65 | 100 | ENT:30, Auftrag (Kevin) |
| Ausdauer max | 50 | 100 | 125 | 160 | Vorschlag (keine Kevin-Zahl) |
| Schaden-Faktor | 0 | 0,35 | 0,62 | 1,0 | Vorschlag; 1,0 = heutige Erwachsenen-Werte `T:shared/NCBearFight.lua:92` (ENT:230); Jungtier kaempft nie (ENT:8) |

Bei D = 100: Tag 5 -> s 0,48 / Leben 77 / Traglast 20; Tag 15 -> 0,75 / 150 / 40; Tag 30 -> 0,875 / 202 / 52; Tag 45 -> 1,0 / 254 / 65;
Tag 70 -> 1,16 / 320 / 81; Tag 100 -> 1,35 / 400 / 100. Leben steigt jeden Tag (Tag 0-15 +7,3, 15-45 +3,5, 45-100 +2,7). Danach die Boni der
Faehigkeiten (4.3). Alles als eine reine shared-Funktion `B.StatsOf(rec)` (Rules-Stil, auch am Client rechenbar), die Sicht traegt aber die
fertigen Zahlen (Client rechnet nie selbst mit eigenen Sandbox-Annahmen).

### 3.3 Traglast-Begriff (fuer spaeter, nur Zahl in B1d)

Ein lebendes Tier hat in der Engine kein eigenes Inventar (`IsoAnimal.getContainer` ist der Behaelter, in dem ein getragenes Tier liegt;
ungeprueft, ob mehr). Fuer das spaetere Baeren-Inventar gibt es belegte Behaelter-Wege: `ItemContainer.new(...)` + `container:setCapacity(x)`
(`V:server/Camping/SCampfireGlobalObject.lua:103`, `:109`, Schreiber). Ob die Engine eine Obergrenze fuer die Kapazitaet hat: ungeprueft.
Kevin: Packtaschen +50, Sandbox-Faktor (ENT:30) -- nicht B1d.

---

## 4. Faehigkeiten 0-10 (Auftrag 4)

### 4.1 Was NPC Crew tut (gelesen, nicht kopiert)

| Lehre | NC-Stelle |
|---|---|
| EINE Zahl je Faehigkeit (Gesamt-XP), Stufe immer daraus gerechnet -- nie Stufe zusaetzlich speichern (zwei Wahrheiten) | `NC:shared/BanditsNPCSkills.lua:52-59` |
| Kurve: Bedarf je Stufe steigt gleichmaessig (+128), Stufe 10 kostet das Doppelte von Stufe 1; 40:1 war zu steil (erste Stufen in einer Stunde) | `:129-166`; Summen `:168-182` |
| Tempo: Ereignis-XP setzen die FORM, eine Echtzeit-Obergrenze je Minute (Eimer, bis 3 min ansparen) das TEMPO; Eimer nur in der Sitzung, nie gespeichert | `:184-216`, `:475-565` |
| Lesen mit Nachfuellen: fehlt/NaN/negativ -> 0, gedeckelt auf das Maximum | `:601-611` |
| `Progress` liefert Stufe, XP in der Stufe, Bedarf (bei 10 voller Balken) | `:631-646` |
| Abgleich nur bei Stufenaufstieg, nicht je XP | `:655-664` |
| Wirkung als Konstante "je Stufe" an einem Ort | `:323-371` |
| Ausweichen ist dort fester Sandbox-Wert, kein Skill (Deckel 95 %) | `:966-975` |

### 4.2 Daten (Vorschlag)

- Register und Spiegel je Faehigkeit EINE Zahl (flach, der Spiegel nimmt nur Zahlen/Texte, `S:server/BanditsNPCBearHeal.lua:43-46`, `:54-65`):
  `xAgi` (Agilitaet), `xVit` (Leben-Bonus), `xCon` (Kondition), `xFgt` (Kaempfen), `xFsh` (Fischen), `xNos` (Spuernase).
- Kurve (Vorschlag, "hinten langsamer"): Bedarf je Stufe `NEED = { 100, 116, 135, 156, 181, 210, 244, 283, 328, 380 }` (je Stufe x 1,16;
  Summe 2033; Stufe 10 kostet 3,8 x Stufe 1 -- zwischen NCs 2:1 und dem verworfenen 40:1). Stufe = groesstes L mit `XP >= CUM[L]`.
- Echtzeit-Eimer je Junges und Faehigkeit nur in `B._s[id]` (nie gespeichert), Deckel z. B. 6 XP je Echtzeit-Minute.
- Haken (Funktionen, in B1d nur Kondition verdrahtet): `B.SkillAdd(rec, key, xp, ms)`, `B.SkillLevel(rec, key)`, `B.SkillProgress(rec, key)`;
  Ereignis-Haken `B.OnHitTaken(rec, dmg)` (Agilitaet + Leben-Bonus), `B.OnHitDealt(rec)` (Kaempfen), `B.OnFish(rec, caught)`, `B.OnSniff(rec)`
  -- leer bzw. nur XP, kein Verhalten.

### 4.3 Wirkung (Formeln, Vorschlag; Hoechstwerte aus der Sandbox)

| Faehigkeit | XP durch (spaeter, ausser Kondition) | Wirkung | Kevin |
|---|---|---|---|
| Agilitaet | eingesteckter Treffer (z. B. +10) | Ausweichen = 5 % + (BearDodgeMax - 5 %) x L / 10 -> 5 .. 40 % | ENT:221-227 (5 % / 40 %, Hoechstwert Sandbox) |
| Leben-Bonus | eingesteckter Treffer (z. B. +10) | Leben max x (1 + 0,05 x L) -> +50 % | ENT:221-223; "+50 % Leben" ENT:21 |
| Kondition | Rennen, Kaempfen, ausser Puste (Hinterhergehen kaum) | Ausdauer max x (1 + 0,05 x L), Erholung x (1 + 0,05 x L) | ENT:226 (Zahlen Vorschlag) |
| Kaempfen | ausgeteilter Treffer (z. B. +5) | Schaden x (1 + BearFightBonusMax x L / 10) -> +70 % | ENT:228, ENT:230 |
| Fischen | Versuch / Fang | Fang-Chance aus Groesse UND Stufe, erst ab Halbstark | ENT:213 |
| Spuernase | rechtzeitige Warnung | Warnweite, abschaltbar | ENT:220 |

Wirkung linear in der Stufe, "hinten langsamer" steckt in der XP-Kurve.

### 4.4 Kondition schon in B1d (Rennen beim Folgen), ohne neuen Engine-Aufruf

- `B.MoveTo` merkt je Befehl `s.walk` (gehend/rennend) und `s.ownUntil` (eigener Befehl laeuft) (`S:server/BanditsNPCBearWorld.lua:828-874`;
  rennen = `animal:fleeTo(sq)` `:862`, belegt `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38`).
- `liveRec` liest je Hirn-Takt `a:getX()/getY()` (`S:server/BanditsNPCBearServer.lua:741`). Vorschlag: Weg seit dem letzten Takt
  (`s.px, s.py` in der Sitzung), gezaehlt nur, wenn `s.walk == false` und `ms < s.ownUntil` (UNSER Rennbefehl; Laerm-Flucht der Engine zaehlt
  nicht), Deckel je Takt (z. B. 8 Kacheln, sonst war es ein Neu-Erzeugen), z. B. 1 XP je 5 Kacheln, Eimer 4.2. Zusatz "ausser Puste":
  erst mit der Ausdauer (B5a) -- in B1d nur die Formel.
- `animal:getVariableBoolean("animalRunning")` ginge auch (Grenzfall aus B1c, FC 11) -- nicht noetig.
- Wieviel Rennen Kevin in 100 Tagen macht: unbekannt -> Zahlen sind Stellwerte fuer seinen Test.

### 4.5 Ausdauer (aktueller Wert) -- wahlfrei in B1d

Tiere haben in der Engine keine Ausdauer (`begleiter/recherche_spiel.md:36-37`). Wenn B1d den aktuellen Wert schon fuehrt (fuer die Anzeige):
nur Sitzung + Register, sinkt bei unserem Rennbefehl, steigt sonst; keine Wirkung. Sonst zeigt die Anzeige nur den Hoechstwert.

---

## 5. Heilen-Vorbereitung (Auftrag 5)

### 5.1 Formel (Kevin ENT:271-272)

`hp = min(1, hp + rate / 100 x dt)` je Langsam-Takt; `rate` wach = `BearHealAwake` (Vorgabe 1,0 % des Hoechstwerts je Spielstunde -> fast tot bis
voll ~4 Spieltage), im Schlaf `BearHealSleep` (15 %, erst mit Schlafen). Anteil statt Punkte -> waechst mit dem Hoechstwert.

### 5.2 Die Engine heilt schon (Kernbefund 7) -- zwei Wege

| | B1: Register fuehrt, Engine-Heilung zuruecknehmen (**Empfehlung B1d**) | B2: Def `healthLossMultiplier = 0` |
|---|---|---|
| Wie | je Langsam-Takt `h = a:getHealth()`: `h > rec.hp + 0,005` -> Engine hat geheilt -> `setHealth(rec.hp neu)`; `h < rec.hp - 0,005` -> Engine-Schaden -> `rec.hp = h`; dann unsere Formel | Engine heilt 0 und verliert 0 ueber `getHealthLoss` (Waffe, Tier, Anhaenger-Unfall, Hunger > 0,8, Milch; `dec/AnimalData.java:472-489`) |
| Vorteil | keine Def-Aenderung, Engine-Schaden bleibt sichtbar | sauber, kein Gegenarbeiten |
| Nachteil | bis zu 10 Spielminuten +2 % sichtbar (Engine heilt bei Stundenwechsel `dec/AnimalData.java:136-153`) | gilt fuer ALLE `ncbearcub`, auch wilde: Spieler-Waffen verletzen keine Jungen mehr (passt zu ENT:45 "nicht Spieler" -- fuer wilde offen, Frage F5); Fahrzeug toetet weiter (`dec/IsoAnimal.java:506-521`) |

Leben nur am Schreiber setzen; der Client bekommt es mit dem Tierpaket (1 %-Schritte, 0.6). Kein Schlaf in B1d -> nur wach.

---

## 6. Anzeige (Auftrag 6)

### 6.1 Optionen-Seite (B1c) erweitern

| Bedarf | Aufruf | Fundstelle | Urteil |
|---|---|---|---|
| Auswahl aus / Balken / Zahl | `o:addComboBox(id, nameKey, tipKey)` + `opt:addItem(key, gewaehlt)` | `V:client/PZAPI/ModOptions.lua:121-156` (addItem ruft `getText`, getValue = Index 1..n); NC gespielt `NC:client/BanditsNPCModOptions.lua:97-103` | reines Vanilla-Lua; Schluessel uebergeben (B1c-Regel, Uebernahme-Pruefung `baer/tools/baer_uebernahme.py:291-299`) |
| Alter-Zeile an/aus | `o:addTickBox(id, nameKey, true, tipKey)` | `V:client/PZAPI/ModOptions.lua:64-86` (wie B1c `TagShow`) | wie B1c |
| lesen | `U.Opt(id, vorgabe)` (Typ-Pruefung: Zahl bzw. boolean) | `S:client/BanditsNPCBearOptions.lua:71-94` | eigener Code |

Vorschlag Ids: `TagHealth` (1 aus / 2 Balken / 3 Zahl, Vorgabe 2), `TagStamina` (Vorgabe 1), `TagAge` (TickBox, Vorgabe an). Spaeter dazu
Hunger, Durst, Muedigkeit, "DODGE" (ENT:234-237). Texte (EN-Vorschlag, alle sieben Sprachen, CN nur Vanilla-Zeichen, `ober_werkzeug/texte.py`):
`UI_BN_Bear_MO_Health` "Health above my bears", `..._MO_HealthTip`, `..._MO_Stamina`, `..._MO_StaminaTip`, `..._MO_Age` "Age and growth line",
`..._MO_AgeTip`, `..._MO_Off` "Off", `..._MO_Bar` "Bar", `..._MO_Number` "Number"; Schild `UI_BN_Bear_Tag_Health` "Health %1/%2",
`UI_BN_Bear_Tag_Stamina` "Stamina %1/%2", `UI_BN_Bear_Tag_Age` "Day %1 - %2 in %3 days", `UI_BN_Bear_Tag_AgeDone` "Day %1 - fully grown",
Stufen `UI_BN_Bear_Stage_Half` "half-grown", `..._Stage_Big` (1,0; Name Frage F6), `..._Stage_Adult` "full-grown".

### 6.2 Sicht (KERN liefert, flache Felder, `viewEntry` `S:server/BanditsNPCBearRegistry.lua:549-573`)

`sz` (gezeigte Groesse, 3 Nachkommastellen; fuer die Client-Probe 1.6), `hp` (0..100 ganze Prozent), `hpMax`, `sta`/`staMax` (wenn gefuehrt),
`day` (ganze Spieltage seit `tamedAt`), `stg` (Stufen-Schluessel), `nxt` (ganze Tage bis zur naechsten Stufe oder nil). Nur bei `st == "tame"`.
Geht mit jedem Commit (hoechstens je Spielstunde) an Besitzer und Spieler in Reichweite (`B.Touch(rec)`, `S:...Registry.lua:50-70`).

### 6.3 Namensschild (`S:client/ISUI/BanditsNPCBearHud.lua`)

Heute Zeile 1 Name, Zeile 2 Zustand (`describeTag` `:213-234`, `drawTag` `:404-414`), Groessenstufen `:61-66`, `:101-129`. Neue Zeilen fertig im
Listenbau (<= 1 x je s), je Bild nur zeichnen (`drawRect`/`drawRectBorder` `V:client/ISUI/ISUIElement.lua:1190-1191`/`:1219`, `drawTextCentre` `:1280`
-- alles schon in B1b/B1c belegt). Fremde Baeren: dieselben Zeilen (Kevin: "was ich sehe", ENT:106). Anker wachsen mit (1.7 tagZ).

---

## 7. Bench (Auftrag 7, nur `client/NCBearBenchCub.lua`, nur SP, nie kopiert)

| Befehl | Tut | Muster |
|---|---|---|
| `NCBear_CubGrow(tage)` | naechstes eigenes zahmes Junges: `g = clamp(g + tage / D, 0, 1)` (negativ = zurueck), `B.Commit`, Groesse sofort setzen (`B.BrainTick(true)`), Sicht schicken, Zeile wie `NCBear_CubStats` | `NCBear_CubSkip` `:190-224` (Register aendern, `B.SlowTick()`, `B.BrainTick(true)`, `push`); `myTame` `:454` |
| `NCBear_CubStats()` | drucken: Tag, g, Groesse innen/gezeigt, Stufe, naechster Meilenstein, Leben (Anteil, Punkte, Hoechstwert), Ausdauer, Schaden-Faktor, Traglast, je Faehigkeit XP/Stufe, Ausweichen %, Kampf-Bonus %, Engine `getSize` und `getHealth` | `NCBear_CubInfo` `:311` |
| wahlfrei `NCBear_CubXp(key, xp)` | XP einer Faehigkeit setzen (Kurve pruefen) | - |

`ready()` lehnt im MP ab (`:61-82`). Namen `NCBear_*` nur hier (Cheat-Regel "befehl" `baer/tools/baer_uebernahme.py:176`).

---

## 8. Register und Spiegel v2 (Ergaenzung)

- Neue Register-Felder (gezaehmt): `g`, `gF`/`gFd`/`gFn` (Fuetter-Bonus), `hp` (Anteil), `xAgi xVit xCon xFgt xFsh xNos`, wahlfrei `sta`.
  `B.InitRegistry` traegt nach / klemmt (Form `:142-163`), je Feld eine Fehlerzeile nur bei Unsinn.
- Spiegel: dieselben Felder in `MARK_FIELDS` (`S:server/BanditsNPCBearHeal.lua:38-41`); `B.Restore` (`:172-250`) und `B.TakeNewerMark`
  (`:289-358`) lesen sie geklemmt (`num(v, 0, 1)`, XP `0..CUM[10]`). `hp` muss nicht in den Spiegel (das Tier traegt sein Leben selbst,
  `dec/IsoAnimal.java:1340`), schadet aber nicht. Fassung: `B.MarkFresh` vergleicht v/id/u/r (`:76-79`) -- neue Felder brauchen kein v = 3,
  wenn Leser fehlende Felder als 0 nehmen; das hourly Commit erneuert den Spiegel. Register-Verlust kostet hoechstens eine Spielstunde Wachstum.
- Sitzung (nie gespeichert): `px, py` (Kondition), XP-Eimer, Zeitpunkt der letzten Groessen-Probe.

## 9. Sandbox (Vorschlag; Seite `BanditsNPC`, Form `S:shared/BanditsNPCBear.lua:102-127`, `type = double` ist in NPC Crew gespielt)

| Name | Typ | min | max | Vorgabe | Quelle |
|---|---|---|---|---|---|
| `BanditsNPC.BearGrowDays` | integer | 10 | 365 | 100 | Kevin (ENT:196-206, Auftrag) |
| `BanditsNPC.BearDodgeMax` | integer | 5 | 80 | 40 | Kevin "Hoechstwert als Sandbox" (ENT:227) |
| `BanditsNPC.BearFightBonusMax` | integer | 0 | 200 | 70 | Kevin (ENT:230) |
| `BanditsNPC.BearHealAwake` | double | 0.0 | 10.0 | 1.0 | Kevin (ENT:271-272), % je Spielstunde |
| `BanditsNPC.BearHealSleep` | double | 0.0 | 100.0 | 15.0 | Kevin (ENT:272); wirkt erst mit Schlafen |

Spuernase-Schalter erst mit ihrem Verhalten (ENT:220). Stellwerte (`B.CFG`, kein Sandbox): `cubMaxSize`, `bodySwap`, `sizeEps`, `feedGrow*`,
Kurven-Tabellen, XP-Raten, Eimer.

---

## 10. NUR im Jar belegt (getrennt) -- Wissen, kein Engine-Aufruf

| Was | Fundstelle | Benutzt als |
|---|---|---|
| Klemme `setSize`, kein Klemmen bei `setSizeForced` | `dec/AnimalData.java:1539-1547` | Begruendung 1.3 |
| `growUp` je Alterstag, `initSize`, Laden mit `setSize` | `:218-235`, `:1353-1358`; `dec/IsoAnimal.java:1389`, `:1413` | 1.2 / 1.3 |
| MP: Groesse nur bei Erst-Uebertragung | `dec_b1b/AnimalUpdatePacket.java:60-79`, `:141-177`; `dec_b1b/AnimalPacket.java:21-82` | 1.6 Client-Probe |
| Bild = `getSize` | `javap/b1d_ModelSlotRenderData.txt:746-752` | 1.2 |
| Tempo kennt die Groesse nicht | Byte-Suche Jar (1.2) | Fussgleiten-Hinweis |
| Engine-Heilung je Stunde, Gen resistance 0,2..0,6 | `dec/AnimalData.java:377-398`, `:472-489`; `dec_b1d/AnimalGenomeDefinitions.java:15-16`; `dec_b1d/AnimalGene.java:139-175`, `:261-285` | 5.2 |
| Leben 0..1, Byte x 100 im MP | `dec_b1b/IsoGameCharacter.java:574`; `dec_b1b/NetworkPlayerAI.java:280`, `:486-488` | 3.1 Regel |
| Stufenwechsel ohne ModData | `dec/AnimalData.java:1381-1443` | Abschnitt 2 |
| Tierzone setzt Groesse zurueck | `dec/IsoAnimal.java:1681-1715`, `dec/DesignationZoneAnimal.java:281-297` | Nachsetzen |
| `getVariableBoolean("animalRunning")`-Grenzfall (Methode belegt, Speicher-Gleichheit nur Jar) | FC 11 | nicht noetig |

---

## 11. Fragen fuer Kevin (Kevin schlaeft -- jede mit Empfehlung, nichts haelt den Bau auf)

- **F1 Definition aendern?** `maxSize` 1,35 und `ageToGrow` sehr gross (1.3 Weg B), damit die Groesse Laden und Mehrspieler uebersteht.
  Empfehlung: ja (Neustart noetig; bestehende Junge bleiben 0,35, bis der Takt sie setzt).
- **F2 Fussgleiten:** waechst das Junge-Modell bis 0,75, bleibt das Lauftempo gleich (Engine) -- die Fuesse koennen rutschen. Bitte beim Test mit
  `NCBear_CubGrow(15)` ansehen. Empfehlung: ansehen, dann Clip-Tempo oder Modellwechsel-Frage zusammen entscheiden.
- **F3 Leben-Zahlen** 40 / 150 / 400 (ENT:17-19) und Ausdauer 50 / 100 / 160, Schaden 0 / 0,35 / 1,0 als Vorgabe? Empfehlung: ja, im Test nachstellen.
- **F4 Mehrspieler:** waechst der Baer, wenn sein Besitzer nicht eingeloggt ist? Empfehlung: nein (wie die Uhren in B1a, ENT:285).
- **F5 Engine-Heilung:** B1 (Register nimmt die Engine-Heilung zurueck) jetzt; spaeter B2 (Def ohne Engine-Schaden) mit B5a? Dann koennen Spieler
  auch WILDE Junge nicht mehr verletzen. Empfehlung: B1 jetzt, B2 mit B5a fragen.
- **F6 Name der Stufe bei 1,0** (Tag 45, "Biss, Umwerfen moeglich", ENT:203)? Vorschlag "kraeftig" / "strong".
- **F7 Fuetter-Bonus** +3 Spielstunden je Fuetterung, hoechstens 2 je Tag, gesamt hoechstens 10 Tage frueher? Empfehlung: ja.
- **F8 Wachsen beim Vermisstsein** (st "missing") anhalten? Empfehlung: ja (so steht es heute im Langsam-Takt).
- **F9 Anzeige-Vorgaben:** Leben als Balken an, Ausdauer aus, Alter-Zeile an? Empfehlung: ja.
- **F10 Stufe "zurueck" in der Bench** (`NCBear_CubGrow(-5)`) erlauben? Empfehlung: ja, nur Testhilfe.

## 12. Luecken (ungeprueft, Testpunkte)

`setSizeForced` an einem lebenden Tier in der Welt (Vanilla nur Haken-Tiere) -- sieht man den Wechsel sofort, ruckt es; Fussgleiten und
Streichel-Haltung bei 0,5-0,75; Namensschild-Hoehe x Groesse; ob der erste Hirn-Takt nach dem Laden schnell genug bindet (Weg A); ob ein MP-Client
seine `setSizeForced`-Kopie behaelt, bis er das Tier verliert; Tierzone-Ruecksetzen in Kevins Basis; Engine-Heilung tatsaechlich 1,5-2,2 %/h
(Gen); `setHealth` mit Werten zwischen 0 und 1 an einem lebenden Tier (Vanilla setzt nur 0); Kapazitaets-Deckel eines Behaelters (Traglast spaeter);
wie viel Rennen in 100 Tagen zusammenkommt (Kondition-Raten); Kahlua-Rundung der Groessen-Zahl in der Sicht.

Statisch geprueft, nicht gespielt.
