# Lauf baer-b1e: Forschung (Modellwechsel ab Halbstark, groessere Markierung)

Stand 11.11.2026 ~15:50. **Statisch gelesen und gemessen, nichts gebaut, nichts gespielt.** Rolle: Forschung (kein Code im Staging, nichts in
Test-Mod / NPC Crew / Vanilla / Bandits geschrieben). Jede Laufzeit-Aussage ohne Spielbeleg ist "ungeprueft".

Schreibweise wie `forschung_b1d.md` (kurz `FD`), `forschung_b1c.md` (`FC`):
- `V:` = Vanilla-Lua `C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/lua/` (42.22.2). `VA:` = Vanilla `media/AnimSets/`.
- `B:` = Bandits `.../Bandits/42.22/media/lua/`; `Bc:` = Bandits `.../Bandits/common/media/`.
- `NC:` = NPC Crew `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua/` (nur gelesen, nichts kopiert).
- `T:` = Test-Mod `NCBearTest/42/media/lua/` (bzw. `T:media/...`). `S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`.
- `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`, `PB1C`/`PB1D` = `PLAN_B1C.md`/`PLAN_B1D.md`.
- **BELEGT** = echter Aufruf in Vanilla-Lua oder Bandits mit gleichen Argumenttypen. **ERLAUBT** = Kevins Wort je Methode
  (`pathToLocation(x, y, z)`, `setVariable("animalRunning", ...)` am Tier). **NUR JAR** = Lesehilfe, kein Engine-Beleg.
- Messwerte: `E` = Modelleinheit (0,544 E = 1 m, Projekt-Konvention `T:shared/NCBearDefs.lua:73`, `baer/spiel/tier_spez.md`); Kacheln
  im Bild = 1,5 je E (`baer/spiel/bau_lebend.md:48`, Core.DoPushIsoStuff); Tempo = Weg `Translation_Data` / Dauer x MotionScale 1,6
  (`baer/spiel/tier_spez.md:229`).

Vorab nachgezaehlt: **Staging = Test-Mod, 51/51 Dateien byte-gleich** (MD5 je Datei aus `staging_dateien.txt` gegen
`C:/Users/Kevin/Zomboid/mods/NCBearTest`, 0 Abweichungen, 11.11. 15:3x). Achtung: im Staging (und in der Test-Mod) liegt als
`42/media/models_X/Skinned/NCBearCub.glb` noch das **Generator-Junge** (MD5 ee7a0cce, Textur 92a829fa). Das alte Junge
(6c3f0a96 / 2ee25f24, `_arbeit/baer_baby/entwurf/`) liegt byte-gleich als `T:media/models_X/Skinned/NCBearBenchCubAlt.glb` /
`T:media/textures/Body/NCBearBenchCubAlt.png` (nachgezaehlt). Der Bau muss es unter dem Namen `NCBearCub.*` ins Staging legen
(Liste `staging_dateien.txt` nachziehen), sonst nimmt die Uebernahme das Generator-Junge mit.

---

## 0. Kernbefunde vorweg

1. **Neue Art ist ungefaehrlich fuer den Kampf:** `NCBearFight.lua` kennt seine Baeren NUR ueber den Artnamen
   (`T:shared/NCBearFight.lua:1787` `if instanceof(o, "IsoAnimal") and o:getAnimalType() == "bear" and not gone(o) then register(o) end`).
   Kein Feld der Definition loest Kampf aus (Art `bear` ist friedlich, `buck` hat keinen Angriffszustand, `T:shared/NCBearDefs.lua:5`,
   `baer/spiel/tier_spez.md` 3.2). Alle anderen Test-Werkzeuge pruefen `"bear"`/`"bearstag"` (`T:client/NCBearSize.lua:24`,
   `T:client/NCBearSpawn.lua:7`, `T:client/NCBearAttackProbe.lua:34`). **Eine eigene Art (Vorschlag `ncbeargrown`) wird von keinem davon
   angefasst.** Kollisionsprobe 11.11.: `ncbeargrown` 0 Treffer in NPC Crew (`42/media/lua` + `_docs/landkarte_index.txt`), Vanilla
   (`media/lua`, `media/scripts`), Test-Mod (`42/media`), Bandits (42.22 + common).
2. **Mit dem grossen Modell braucht die neue Art nur Lua-Daten und vorhandene Dateien:** Definition (wie das Junge, `S:shared/BanditsNPCBearDefs.lua:75-112`)
   mit `bodyModel = "NCBear_Body"` (model-Skript in `module Base`, `T:media/scripts/nc_bear_tier.txt`, Mesh `Skinned/NCBear.glb`) und Rasse
   `texture = "NCBear"` (`T:media/textures/Body/NCBear.png`, wie `T:shared/NCBearDefs.lua:40-41`), `animset = "buck"`, eine Stufe gleich dem
   Artnamen ohne `nextStage`, dazu `AnimalAvatarDefinition[art]` (sonst wirft `V:client/ISUI/Animal/ISAnimalUI.lua:31`),
   `AnimalPartsDefinitions.animals[art .. "brown"]`, Text `IGUI_AnimalType_<art>` x 7. Das grosse Modell traegt dieselben 15 Clips inkl.
   `NCBear_Eat` (Dump, 4.1) -- Fuettern mit Fress-Clip geht. **Naht:** das Uebernahme-Skript prueft `bodyModel`/Rassen-Textur der Defs gegen die
   kopierten Dateien (`baer/tools/baer_uebernahme.py:1121-1132`) und fuehrt `NCBear.glb`, `NCBear.png`, `nc_bear_tier.txt` heute als Altlast bis
   B5a (`:151-158`) -> rot, bis der Plan das entscheidet (Frage F9).
3. **Der Tausch-Weg ist zu 80 % da:** `B.PlaceCub` (neuer Koerper, `gen + 1`, Spiegel sofort, Groesse+Leben sofort, `S:server/BanditsNPCBearRide.lua:67-91`)
   + `B.RemoveCub(old)` danach, genau wie "Call to me" (`:328-335`). Es fehlt: `B.CreateCub` kennt nur `B.CUB` (`S:server/BanditsNPCBearWorld.lua:451`, `:473`),
   und **12 Stellen** pruefen hart auf `B.CUB` (Abschnitt 2) -- darunter `B.FindAnimal`, `B.RecOf`, `B.ScanAnimals`, `B.RemoveCub`: ohne Helfer
   wuerde der grosse Koerper nach dem Tausch sofort "vermisst", nie gebunden und (bei Absturz) als Doppel nie entfernt.
4. **Messung (Spiel-Importer-Dump, Idle Bild 0, bei Groesse 1,0):** altes Junges 0,9966 E lang (1,83 m) / 0,5894 E hoch (Kopf) / 0,4819 E breit;
   grosser Baer 1,0448 E (1,92 m) / 0,6254 E (Schulterbuckel) / 0,4867 E. Bei gleicher Groesse ist das grosse Modell **4,8 % laenger, 6,1 % hoeher**.
   **Gleich gross wie das Junge bei 0,75 wirkt der grosse Baer bei 0,72** (Laenge +0,6 %, Hoehe +1,9 %, Breite -3,0 %; Kevins woertliches 0,75 gaebe
   +4,8 / +6,1 %). Abbildung danach gerade: `sz = 0,72 + 1,05 x (s - 0,75)` -> Tag 15: 0,72, Tag 45: 0,98, Tag 100: **1,35** (2,59 m lang, Oberkante
   1,55 m = Kevins Tabelle ENT:10).
5. **Tempo:** altes Junges gehen **0,523** / rennen **2,465** Kacheln/s (passt zu `walkSpeed 0.52` / `runSpeed 2.47`, `S:shared/BanditsNPCBear.lua:91`),
   grosser Baer gehen **0,673** / rennen **3,173**. Das Tempo kommt nur aus dem Clip und kennt die Groesse nicht (FD 1.2); `buck` hat keinen
   Tempo-Regler (`VA:buck/walk/defaultWalk.xml`, `VA:buck/pathfind/defaultPathfind.xml` ohne `m_SpeedScale`; die Kuh hat `animalSpeed`,
   `VA:cow/walk/defaultWalk.xml:6`). **Fussgleiten nach dem Tausch: -28 % (Tag 15) -> 0 (Tag ~47) -> +35 % (Tag 100)** -- so viel wie beim Jungen
   kurz vor dem Tausch (-28 %), am Ende "Tretmuehle". Mit Lua nicht behebbar (ohne neue Knoten/Clips) -> "im Spiel ansehen" (F6).
6. **Markierung:** Bandits zeichnet Kreis, Pfeil, Symbol in Originalgroesse 96 px (`B:client/BanditEventMarkers.lua:7`, `:174`, `:192-193`; Text
   `UIFont.Small` `:176`; Lage `B:client/BanditEventMarkerHandler.lua:22-23`). Skalieren ohne Bandits-Aenderung geht **nur mit eigenem Element**:
   Kreis und Symbol mit `drawTextureScaled` (BELEGT), Pfeil mit `DrawTextureAngle` (BELEGT, zeichnet aber **immer in Bildgroesse**, NUR JAR) ->
   eigene Pfeil-Bilder je Groessenstufe. Bildschirmhoehe `getCore():getScreenHeight()` (BELEGT). Optionen-Seite: `addComboBox` "Auto / 100-300 %".
   Ein stufenloser gedrehter Pfeil ginge nur ueber `drawTextureAllPoint` (Engine-Aufruf steht in `V:client/ISUI/ISUIElement.lua:1016`, der Lua-Weg hat
   keinen Vanilla-Aufrufer) -> Grenzfall, Kevins Wort.

---

## 1. Arten und Modelle in der Test-Mod (Auftrag a)

### 1.1 Wie die Test-Mod Arten anlegt

| Art | Datei | Modell (bodyModel -> Skript -> Mesh) | Textur | Groesse | Wer fasst sie an |
|---|---|---|---|---|---|
| `bear` (grosser Baer, 2c) | `T:shared/NCBearDefs.lua:62-101` | `NCBear_Body` -> `T:media/scripts/nc_bear_tier.txt` (`module Base`, `animationsMesh NCBear` meshFile `Skinned/NCBear.glb`) | Rasse `brown` `texture/textureMale = "NCBear"` (`:40-41`) | `minSize = maxSize = 1.0` (`:73-74`, "Massstab steckt im Netz") | `NCBearFight.lua` (Kampf, `:1787`), Bench/Size/Spawn/Probe |
| `bearstag` (Rueckfall) | `T:shared/NCBearDefs.lua:102` | `NCBearStag_Body` (Mesh `NCBearDeer.glb`, `animationsMesh = Deer_Stag`) | wie `bear` | 1,0 | Size/Spawn/Probe; NCBearFight nie (`:1766-1767`) |
| `ncbearcub` (Junges) | `S:shared/BanditsNPCBearDefs.lua:75-112` | `NCBearCub_Body` -> `S:media/scripts/nc_bear_cub.txt` (Mesh `Skinned/NCBearCub.glb`) | `NCBearCub` (`:51-53`) | min 0,35 / max 1,35, `ageToGrow 36500` (`:73`, `:83-84`) | unser Kern (B1a-B1d) |
| `ncbearcubalt` (nur Bench) | `T:shared/NCBearBenchVergleichDefs.lua:14-40` | `NCBearBenchCubAlt_Body` (`T:media/scripts/NCBearBenchVergleich.txt`) | `NCBearBenchCubAlt` | 0,35..1,35 | nur `NCBearBenchVergleich.lua:75`; Kern fasst sie nie an (`:5-6`) |

Bemerkenswert fuer den Bau: `NCBearBenchVergleichDefs.lua:8-33` zeigt die Form "Kopie der Junges-Definition, nur Modell/Rasse/Groesse anders"
(`require "BanditsNPCBearDefs"`, Felder kopieren, `d.bodyModel = ...`, eigene `stages[ART]`, eigene `breeds`). So laesst sich die neue Art
ohne doppelte Pflege aus der Junges-Definition ableiten (Planer entscheidet). Achtung: die Bench-Vergleichsart kopiert ebenfalls die
Junges-Definition -- jede B1e-Aenderung an `ncbearcub` wirkt dort mit (harmlos).

### 1.2 Was eine neue Art mit dem grossen Modell braucht (Bedarf -> Feld/Datei -> Fundstelle -> Urteil)

Die Engine liest diese Schluessel in `AnimalDefinitions.loadAnimalDefinitions` (Liste `forschung_engine.md:125-130`, NUR JAR), erst in
`IsoWorld.init` nach allen Lua-Dateien (`S:shared/BanditsNPCBearDefs.lua:4-5`) -> Definition auf Dateiebene, Aenderung = Neustart.

| Bedarf | Feld / Datei | Wert-Vorschlag | Fundstelle / Grund | Urteil |
|---|---|---|---|---|
| Artname (ENDGUELTIG: ein gespeichertes Tier unbekannter Art bricht das Laden, `S:shared/BanditsNPCBearDefs.lua:9`) | `AnimalDefinitions.animals["ncbeargrown"]` | `ncbeargrown` (Alternativen `ncbearbig`, `ncbearhalf`: ebenfalls frei) | Probe 0.1; Namensraum `ncbear` erlaubt (`baer_uebernahme.py:111-112`) | Planer/Kevin (F2) |
| Modell | `bodyModel` | `"NCBear_Body"` (= heutiges grosses Modell; "der Tausch nimmt das jeweils aktuelle grosse Modell") | model-Skript ohne Punkt sucht nur `module Base` (`baer/spiel/tier_spez.md` 2.7); `T:media/scripts/nc_bear_tier.txt` | ok (Naht F9) |
| Textur | Rasse `brown`: `texture`, `textureMale`, `textureBaby` | `"NCBear"` | `T:shared/NCBearDefs.lua:40-41`; `textureBaby` allein wirkt ohne `nextStage` nicht (`S:...Defs.lua:45`) | ok |
| Animset | `animset` | `"buck"` | nur Vanilla-Gruppen (ActionGroup liest nur den Spielordner, `tier_spez.md` 3.1); Clips heissen wie die Knoten -- NCBear.glb hat `DeerStag_*` + `NCBear_*` (Dump 4.1) | ok |
| Stufe | `stages[art] = { ageToGrow = 36500 }`, kein `nextStage` | wie Junges | sonst Stufenwechsel = neues Tier ohne ModData (FD 2, `dec/AnimalData.java:1381-1443`) | ok |
| Gruppe | `group` | `"ncbear"` (Text `IGUI_Animal_Group_ncbear` existiert) | Debug-Menue braucht sie (`T:shared/NCBearDefs.lua:68`) | ok |
| Groesse | `minSize`, `maxSize` | **min = Tauschgroesse 0,72**, max 1,35 | `setSize` klemmt beim Laden/MP-Erstuebertragung/Alterstag/Tierzone auf [min, max] (FD 0.2); neuer Koerper startet bei minSize (`initSize` -> `setSize(0.1)`, `dec/AnimalData.java:1353-1358`) -> mit min = 0,72 hat ein frischer Koerper sofort die Tauschgroesse, auch wenn `setSizeForced` im selben Bild nicht wirkt (ungeprueft, FD 1.6) | Vorschlag |
| Kollision | `collisionSize` (wirkt x Groesse, `dec/IsoAnimal.java:420`/`:433`, NUR JAR) | **0,30** -> 0,22 beim Tausch (Junges bei 0,75: 0,24 x 0,75 = 0,18), 0,41 bei 1,35 (gespielter Erwachsener: 0,42 bei 1,0) | `S:...Defs.lua:86`, `T:shared/NCBearDefs.lua:76` | im Spiel ansehen (F10) |
| Schatten, Leiche, Bild | `shadoww/fm/bm`, `animalSize`, `corpseSize` | wie `bear`: 0,9 / 1,8 / 1,8, 0,3, 3,0 (wachsen x Groesse) | `T:shared/NCBearDefs.lua:75-80`; Wirkung FD 1.2 | ok (Optik) |
| Gewicht, Blut, Anhaenger | `minWeight/maxWeight`, `minBlood/maxBlood`, `trailerBaseSize` | z. B. 60/200, 800/2000, 300 (egal: kein Hochheben, kein Anhaenger) | `S:...Defs.lua:90-95` | Vorschlag |
| Verhalten | `wild=false`, `canBeDomesticated=false`, `alwaysFleeHumans=false`, `fleeZombies=false`, `canBePicked=false`, `canThump=false`, `canBeAlerted=false`, `sitRandomly=false`, `needMom=false`, `dontAttackOtherMale=true`, `wanderMul=600`, `idleTypeNbr=0`, `spottingDist=10`, `feedByHandAnim="AnimalLureLow"`, `male=true` | **wie das Junge** (`S:...Defs.lua:96-111`) | Vorgaben waeren alwaysFleeHumans/fleeZombies/canBePicked/canThump/canBeDomesticated = true (`forschung_engine.md:131-134`) | Pflicht |
| Gene | `genes` ohne `maxSize`-Gen | wie Junges (`S:...Defs.lua:35-43`) | sonst andere Grenzen (`dec/AnimalData.java:1717-1751`) | Pflicht |
| Toene | `breeds.brown.sounds` | wie Junges: `fallover`, `petting` (`S:...Defs.lua:60-68`); KEINE Erwachsenen-Stimmen (`pain` spielt die Engine bei Treffern selbst, `T:shared/NCBearDefs.lua:31`) | Kampf/Stimme ist B5a | Frage F4b |
| Tier-Info-Fenster | `AnimalAvatarDefinition[art]` | Kopie von `ncbearcub` (= `buck`) | ohne Eintrag wirft `V:client/ISUI/Animal/ISAnimalUI.lua:31` (`S:...Defs.lua:114-131`) | Pflicht |
| Zerlegen nach Tod | `AnimalPartsDefinitions.animals[art .. "brown"]` | Attrappe wie `bear` (`buckwhitetailed`, `T:shared/NCBearDefs.lua:125`) | `V:shared/Definitions/animal/ButcheringUtil.lua:18` | Pflicht |
| Name im Spiel | `IGUI_AnimalType_<art>` in `Translate/<L>/IG_UI.json` x 7 | z. B. EN "Bear" | `S:shared/Translate/EN/IG_UI.json:4` (Junges); Uebernahme erlaubt in IG_UI.json nur drei Schluessel (`baer_uebernahme.py:136`) -> nachziehen | Pflicht (Naht) |
| Tempo | -- (kein Definitionsfeld fuer `buck`) | -- | Tempo nur aus dem Clip (`tier_spez.md` 2.8); `buck`-Knoten ohne Tempo-Variable (0.5) | 4.4 |

**Welche Felder der alten Art `bear` Kampf/Verhalten ausloesen:** keine. Der Kampf ist reines Lua in `T:shared/NCBearFight.lua`, das nur
Tiere mit `getAnimalType() == "bear"` registriert (`:1787` in `scanBears`, `:1741-1759` `register`); Ereignisse nur `OnTick`/`OnGameStart`
(`:1888`, `:1895`). Die 9 Kampf-Knoten `T:media/AnimSets/buck/idle/NCBear_*.xml` laufen nur, wenn jemand `NCBearAct` setzt (Bedingung
`NCBear_Sit.xml:9-12`); unser Kern setzt nur `"eat"` (`S:shared/TimedActions/BanditsNPCBearFeedAction.lua:60`). Unterschiede `bear` vs.
Junges, die NICHT uebernommen werden sollen: `group "bear"`, Stimmen `pain/death/huff/growl1-3/huffsoft` (`T:shared/NCBearDefs.lua:48-57`),
`minSize = maxSize = 1.0`.

---

## 2. Jede Stelle, die auf die Art des Jungen prueft (Auftrag b)

Grep `B\.CUB|ncbearcub|getAnimalType|CubDefOk|AnimalDefinitions` im Staging (11.11.), dazu die Stellen, die ueber diese Funktionen laufen.
"beide" = muss Junges- UND grossen Koerper erkennen (ein Helfer, z. B. `B.IsBody(a)` / `B.BodyKind(type)`); "Junges" = bleibt nur Junges.

| # | Datei:Zeile | zitierte Zeile | Seite | wird gebraucht fuer | B1e |
|---|---|---|---|---|---|
| 1 | `S:shared/BanditsNPCBear.lua:29` | `B.CUB = "ncbearcub"             -- Tierart des Jungen` | beide | Konstante | + `B.BIG = "ncbeargrown"` (o. ae.) |
| 2 | `S:shared/BanditsNPCBear.lua:476` (`B.ViewOf`) | `if animal:getAnimalType() ~= B.CUB then return nil end` | Client (+SP) | Menue (`S:client/BanditsNPCBearMenu.lua:295`), Hud-Suchlauf (`S:client/ISUI/BanditsNPCBearHud.lua:248`), `U.CubObj` (`:733`) -> Namensschild, Karten-Symbol (`S:client/ISUI/BanditsNPCBearMap.lua:94`), Markierung (`U.CubPos`, nur Wild) | beide |
| 3 | `S:server/BanditsNPCBearServer.lua:156` (`handCheck`) | `if animal:getAnimalType() ~= B.CUB then return nil end` | Schreiber | Fuettern, Streicheln (`B.FeedComplete`, `B.PetComplete`) | beide |
| 4 | `S:server/BanditsNPCBearRegistry.lua:341` (`B.RecOf`) | `if animal:getAnimalType() ~= B.CUB then return nil, "kind" end` | Schreiber | Tier -> Eintrag (Menue-Bitten, Fuettern, Heilung) | beide; Fund "found" (`:376`) nur Junges (ein grosser Koerper ohne Eintrag ist nie ein neuer Wildfund) |
| 5 | `S:server/BanditsNPCBearWorld.lua:451` (`findBreed`) | `local def = AnimalDefinitions.getDef(B.CUB)` | Schreiber | `B.CreateCub`, `B.CubDefOk` | je Art (Parameter) |
| 6 | `S:server/BanditsNPCBearWorld.lua:457` (`B.CubDefOk`) | `return findBreed() ~= nil` | Schreiber | Einsteigen (`S:server/BanditsNPCBearRide.lua:102`) | je Art (die Art, die beim Aussteigen entsteht) |
| 7 | `S:server/BanditsNPCBearWorld.lua:473` (`B.CreateCub`) | `addAnimal(getCell(), ..., B.CUB, breed, false)` | Schreiber | einzige Erzeuger-Stelle (`B.AppearFor`, `B.PlaceCub`) | Art-Parameter, Vorgabe Junges (wilde Junge) |
| 8 | `S:server/BanditsNPCBearWorld.lua:497` (`B.RemoveCub`) | `if animal:getAnimalType() ~= B.CUB then return end` | Schreiber | Entfernen (Tausch, Einsteigen, Call to me, Waisen, Kopien, Verschwinden) | beide (nie `bear`) |
| 9 | `S:server/BanditsNPCBearWorld.lua:514` (`B.FindAnimal`) | `if a:getAnimalType() ~= B.CUB then return nil end` | Schreiber | jeder Hirn-Takt, GrowSlow/GrowSetG, Bench | beide (sonst gilt der grosse Koerper als "fehlt" -> nach 3 Suchlaeufen "missing") |
| 10 | `S:server/BanditsNPCBearWorld.lua:651` (`B.ScanAnimals`) | `if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB and not o:isDead() then` | Schreiber | Binden, Heilung, veraltete Kopien/Doppel entfernen, Waisen | beide (sonst bleibt eine veraltete grosse Kopie nach Absturz fuer immer = Doppel, rote Linie) |
| 11 | `S:server/BanditsNPCBearRide.lua:102-103` | `if not B.CubDefOk() then` / `"ride: animal definition " .. tostring(B.CUB)` | Schreiber | Einsteigen nur, wenn beim Aussteigen ein Koerper entstehen kann | Art des kuenftigen Koerpers (4.6 Rueckfall) |
| 12 | `S:client/BanditsNPCBearMenu.lua:315`, `:318` (`onClickedAnimals`) | `if a:getAnimalType() == B.CUB then` | Client | Rechtsklick-Menue (Fuettern, Hinhalten, Streicheln, Folgen/Bleiben, Name, Call to me) | beide; `:434` (`onFillWorld`) prueft nur `not B.CUB` (Existenz) -- bleibt |
| 13 | `S:client/ISUI/BanditsNPCBearHud.lua:247` (`scan`) | `if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB then` | Client | Objekt je Sicht-Eintrag (Schild, Balken, Karte live, Markierung live) | beide |
| 14 | `S:client/NCBearBenchCub.lua:397` (`NCBear_CubClean`), `:640` (`nearestCubObject`) | `if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB then` | Bench (SP) | Aufraeumen, `NCBear_CubMark` | beide |
| 15 | `S:server/BanditsNPCBearGrow.lua:416-425` (`B.GrowLive`) | `if B.CFG.bodySwap == true then` ... `B.Err("grow: body swap is not built yet, ...")` | Schreiber | Haken fuer den Tausch | ersetzen durch den Tausch (3) |
| 16 | `S:shared/BanditsNPCBearStats.lua:225-230` (`B.BodyOf`) | `return "cub", math.floor(sz * 1000 + 0.5) / 1000` | beide | Koerper + gezeigte Groesse | `"big"` ab Schwelle, Abbildung 4.3 |
| 17 | `S:server/BanditsNPCBearRegistry.lua:298` (`B.NewRec`), `S:server/BanditsNPCBearHeal.lua:226` (`B.Restore`) | `id = id, nr = nr, kind = "cub",` | Schreiber | Eintrag-Art (immer "cub") | bleibt; Koerper als NEUES Feld (`rec.body`), nicht `kind` |
| 18 | `S:shared/BanditsNPCBearDefs.lua:29`, `:75` | `local CUB = "ncbearcub"` / `AnimalDefinitions.animals[CUB] = {` | Definition | Art | + neue Art |
| 19 | `S:shared/Translate/<L>/IG_UI.json` | `"IGUI_AnimalType_ncbearcub": "Bear cub"` (EN `:4`) | Text | Tiername | + `IGUI_AnimalType_<neu>` x 7 |
| (20) | Hud-Groessen-Probe `S:client/ISUI/BanditsNPCBearHud.lua:443`, `:459` | `B.ApplySize(obj, c.sz)` | nur MP-Client | Groesse der Client-Kopie | nur wenn Koerper der Kopie = Koerper der Sicht (4.3) |
| (21) | `S:server/BanditsNPCBearGrow.lua:427-428`, `:479-480`, `:633-634` | `local _, sz = B.BodyOf(rec)` / `B.ApplySize(a, sz)` | Schreiber | Groesse nachsetzen | nur am passenden Koerper, sonst zuerst tauschen |

Indirekt koerper-frei (bekommen das Tier-Objekt, pruefen keine Art; mit dem Helfer in 9/10 laufen sie fuer beide): Laerm-Wache
`B.CalmWatch`/`B.CalmTick` (`S:server/BanditsNPCBearGuard.lua:54`, `:230`), Zombie-Wache `B.GuardStep`, Folgen `B.FollowStep`, `B.MoveTo`
(`S:server/BanditsNPCBearWorld.lua:831`), `B.Hold`, Mitfahren `B.RideStep`, Spiegel-Probe `markProbe` (`S:server/BanditsNPCBearServer.lua:709`),
`B.GrowLive`/`B.BodyHp`, Zeitaktionen Fuettern/Streicheln (`S:shared/TimedActions/*`). Die Markierung zeigt nur WILDE Junge
(`S:client/ISUI/BanditsNPCBearMarker.lua:150-165`) -> vom Tausch nicht betroffen.

Koerper-abhaengige Stellwerte (gelten heute fuer das Junge, brauchen einen Wert je Koerper, Abschnitt 4.4/4.5): `walkSpeed`/`runSpeed`
(`S:server/BanditsNPCBearWorld.lua:866-867`, `S:shared/BanditsNPCBearRules.lua:530`, `S:server/BanditsNPCBearGrow.lua:358`),
`followNear/followStart/followGap` (`S:shared/BanditsNPCBearRules.lua:500`, `:525`), `hideGap` (`:612`), Schild-Anker `tagZ x sz / tagBase`
(`S:client/ISUI/BanditsNPCBearHud.lua:364-371`, `:619-623`), Streichel-Haltung `petAnim "lamb"` + `AnimalSizeY 0.5`
(`S:shared/TimedActions/BanditsNPCBearPetAction.lua:50-59`). Die Regeln lesen `B.CFG` direkt (`S:shared/BanditsNPCBearRules.lua:470`) -> der Wert
je Koerper muss ueber den Zustand `c`/`env` kommen (Planer).

Texte, die nach dem Tausch "cub" sagen (gezaehmter Baer): EN `UI_BN_Bear_Tag_Name` "%1's cub" (`S:shared/Translate/EN/UI.json:107`), `Note_Follow`
(`:75`), `Note_Stay` (`:88`), `Note_StayBehind/StayCar/StayFar` (`:89-91`), `Note_Called` (`:72`), `Note_RideOn/RideOff` (`:84-85`),
`Note_Renamed` (`:83`), `Note_Dead` (`:73`), `Menu_Name` (`:63`), `Menu_CallTip` (`:57`), `Name_Title` (`:68`), `Why_CallWait` (`:114`),
`Why_Riding` (`:132`), `Why_Gone` (`:118`). Frage F3.

---

## 3. Der Tausch-Weg (Auftrag c)

### 3.1 Was heute schon geht

| Baustein | Fundstelle | was er tut |
|---|---|---|
| `B.PlaceCub(rec, x, y, z, why)` | `S:server/BanditsNPCBearRide.lua:67-91` | `B.CreateCub` (`:69`), `rec.gen + 1` (`:72`), `rec.aid` neu, `s.obj = a`, Sitzung leeren, Lage = Kachel, `missing` -> `tame`, `B.Commit` (r + 1), `B.WriteMark` sofort (`:84`), `B.GrowBody` (Groesse + Leben aus dem Register, `:86`), Laerm-/Zombie-Wache leeren, Log |
| `B.RemoveCub(animal)` | `S:server/BanditsNPCBearWorld.lua:495-503` | Sperre loesen, `animal:remove()`, am Server `removeAnimal(getOnlineID())` -- Belege dort (`V:shared/Definitions/animal/ButcheringUtil.lua:609`, `:612-614`) |
| Muster "neu zuerst, dann alt weg" | `B.HandleCall` `S:server/BanditsNPCBearRide.lua:328-335` | `PlaceCub` -> bei Erfolg `if old ~= nil and old ~= a then B.RemoveCub(old) end`; misslingt `PlaceCub`, bleibt alles wie es war (`:329-333`) |
| veraltete Kopie / Doppel | PB1C 0.2, `S:server/BanditsNPCBearHeal.lua` (`B.HealFromMark` `:369`), `S:server/BanditsNPCBearWorld.lua:612-620` (`dropCopy`) | ein Koerper mit kleinerer `gen` wird nie gebunden und unbeobachtet entfernt |
| Haken | `S:server/BanditsNPCBearGrow.lua:416-425` | Kommentar "HIER tauscht er den Koerper", heute Fehlerzeile je 10 min |
| Groesse/Leben an neuen Koerper | `B.GrowBody` `S:server/BanditsNPCBearGrow.lua:477-485` | `B.ApplySize(a, sz)` + `B.BodyHp(rec, a, 0)` |
| Uebernahme-Regel | `baer/tools/baer_uebernahme.py:264-270` | `addAnimal`/`addToWorld` nur in `B.CreateCub`, `B.CreateCub(` nur aus `B.AppearFor` und `B.PlaceCub` -> **der Tausch muss ueber `B.PlaceCub` gehen** (sonst rot) |

### 3.2 Was fehlt

1. `B.CreateCub(x, y, z, kind)` mit Art-Parameter (Vorgabe Junges); `findBreed(kind)` je Art (`AnimalDefinitions.getDef(Text)` +
   `def:getBreedByName(Text)` BELEGT `V:server/ClientCommands.lua:808`, `V:shared/Definitions/animal/ButcheringUtil.lua:79/85`).
2. `B.PlaceCub` erzeugt den Koerper, den `B.BodyOf(rec)` will (dann erledigen Aussteigen, Call to me und Tod-im-Auto den Tausch von selbst, ohne
   eigenen Tausch-Takt; ein waehrend der Fahrt ueber 0,75 gewachsenes Junges steigt gross aus).
3. Ein Art-Helfer fuer alle 12 Stellen aus 2 (nie `"bear"`).
4. `rec.body` ("cub"/"big") im Register und im Spiegel (MARK_FIELDS `S:server/BanditsNPCBearHeal.lua:40-44`), damit die Schwelle einen Abstand hat
   (3.4) und eine Heilung den Koerper kennt; Wahrheit beim Binden = `a:getAnimalType()`.
5. Der Tausch selbst in `B.GrowLive` (laeuft je Hirn-Takt fuer jedes geladene zahme Junge mit `s.obj == a`, `S:server/BanditsNPCBearServer.lua:1017-1025`)
   statt der Fehlerzeile; `B.ApplySize` nur am passenden Koerper (sonst bekaeme der Junges-Koerper kurz Erwachsenen-Groesse oder umgekehrt).
6. Rueckfall: misslingt der grosse Koerper (Definition/Rasse fehlt, `addAnimal` gibt nil), bleibt das alte Tier, Fehlerzeile gedrosselt
   (`B.ErrEvery`), neuer Versuch fruehestens nach `swapRetryMs` (Vorschlag 10 s). Beim Aussteigen/Call to me: lieber ein Junges-Koerper als keiner
   ("nie verloren") -- sonst stuende ein mitfahrendes Tier mit kaputter grosser Definition fuer immer im Auto (`placeFail`, `S:server/BanditsNPCBearRide.lua:136-142`).

### 3.3 Vorschlag Ablauf "Tausch" (Planer entscheidet; nur Lua-Logik, alle Engine-Aufrufe aus 3.1 belegt)

```
GrowLive(rec, a, ...):
  want = BodyOf(rec)            -- "cub"/"big" mit Abstand (3.4)
  have = Koerper von a          -- a:getAnimalType() (BELEGT V:client/ISUI/Animal/ISAnimalUI.lua:65)
  wenn want ~= have und sicher (3.5):
      x, y, z = Kachel von a (rec.x/y/z aus liveRec)
      n = B.PlaceCub(rec, x, y, z, "grow")     -- neuer Koerper (gen + 1, Spiegel, Groesse, Leben)
      wenn n: B.RemoveCub(a); s.swapAt = ms; Log; (Sicht geht mit dem Commit von PlaceCub)
      sonst: alter Koerper bleibt, ErrEvery, s.swapTryAt = ms
  sonst ApplySize(a, sz) nur wenn want == have
```

Genau EIN Tier: der neue Koerper steht, bevor der alte geht; Lua laeuft in einem Takt durch, dazwischen speichert die Welt nicht. Stuerzt das
Spiel genau dazwischen ab, haelt der Spielstand hoechstens eine veraltete Kopie (`gen` kleiner) -- die heilt der Suchlauf (Stelle 10 MUSS dafuer
beide Arten sehen). Register-Eintrag bleibt derselbe (`id`, `u`, Besitzer, Name, Zaehmung, `g`, Erfahrung, `hp`-Anteil, Modus, Heimat).

### 3.4 Schwelle mit Abstand (kein Flackern)

- Hin: innere Groesse `s >= stageAt[1]` (0,75 = `cubMaxSize`, `S:shared/BanditsNPCBear.lua:105`; bei D = 100 Tag 15, anteilig `0,15 x D`).
- Zurueck: nur bei `s < 0,70` (Vorschlag `swapBackSize`); zwischen 0,70 und 0,75 bleibt der Koerper, wie er ist. Der grosse Koerper zeigt dort
  0,72 (= minSize der neuen Art).
- Mindestabstand zweier Tausche je Eintrag `swapMinMs` (Vorschlag 60 s, Sitzung) -- normal waechst `g` nur, zurueck geht es nur ueber die Bench
  (`NCBear_CubGrow(-100)`) oder eine MP-Heilung mit gedeckeltem `g` (`S:server/BanditsNPCBearGrow.lua:554-564`).

### 3.5 "Sicher" (sonst naechster Takt)

| Bedingung | Quelle | Grund |
|---|---|---|
| `rec.st == "tame"`, `rec.ride == nil`, `s.obj == a`, lebt, in der Welt | `B.FindAnimal` | mitfahrend: kein Koerper (Tausch beim Aussteigen ueber 3.2 Nr. 2) |
| keine Laerm-Antwort laeuft (`s.calmUntil` vorbei) | `S:server/BanditsNPCBearGuard.lua:145` | Ersatzweg nicht zerreissen |
| keine Zombie-Gefahr (`B._zed[rec.id]` fehlt oder weiter als `zedSafe`) | `S:server/BanditsNPCBearGuard.lua:37` | Verstecken nicht zerreissen |
| Abklingzeit `swapMinMs` / `swapTryAt` | 3.4 / 3.2 Nr. 6 | kein Flackern, keine addAnimal-Flut |
| Call to me | `B.HandleCall` laeuft in EINEM Aufruf (`S:server/BanditsNPCBearRide.lua:278-341`) | kann nicht dazwischen kommen; erzeugt selbst den richtigen Koerper (3.2 Nr. 2) |
| Fuettern/Streicheln laeuft gerade | **nicht abfragbar**: `isBlockMovement` gibt es nur am Spieler (`V:client/ISUI/ISWorldObjectContextMenu.lua:2302`), am Tier kein Getter | Folge eines Tauschs mitten in der Aktion: `complete()` -> `handCheck` sagt `Why_Gone`, **nichts wird genommen** (`S:server/BanditsNPCBearServer.lua:215-234`: Pruefung vor `takeOne`) -> kein Verlust. Wer das vermeiden will: die Aktionen melden "beschaeftigt bis" an den Kern (SP `start`, MP `serverStart`, `S:shared/TimedActions/BanditsNPCBearFeedAction.lua:98-100`) -- Planer |

---

## 4. Messung (Auftrag d)

### 4.1 Werkzeug und Befehle

Spiel-Importer-Harness (liest das GLB mit dem Importer des Spiels, startet das Spiel nicht), dann Python (numpy) mit eigener Haut-Rechnung.
Skripte und Ausgaben: `_arbeit/baer_zaehmen/mess_b1e/` (`mess_dump.py`, `landmarken.py`, `tabelle.py`, `ausgabe.txt`, beide Dumps).

```
JB=C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin; G="C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"
H=C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness; D=C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/mess_b1e
"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/entwurf/NCBearCub.glb $D/dump_junges_alt_6c3f0a96.txt skin
"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Dump C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/models_X/Skinned/NCBear.glb $D/dump_gross_2c_08ec7806.txt skin
cd $D; python mess_dump.py dump_junges_alt_6c3f0a96.txt altes_Junges; python mess_dump.py dump_gross_2c_08ec7806.txt grosser_Baer
python landmarken.py dump_junges_alt_6c3f0a96.txt altes_Junges; python landmarken.py dump_gross_2c_08ec7806.txt grosser_Baer; python tabelle.py 0.72
```

Gemessen: altes Junges `_arbeit/baer_baby/entwurf/NCBearCub.glb` **MD5 6c3f0a96** (= `T:media/models_X/Skinned/NCBearBenchCubAlt.glb`), grosser
Baer `T:media/models_X/Skinned/NCBear.glb` **MD5 08ec7806** (2c, 10.11. 10:37). Beide 26 Knochen, 15 Clips (gleiche Namen inkl. `NCBear_Eat`).
Achsen im Dump: y = oben (Boden y = 0,0000), -z = vorn (`Translation_Data` laeuft nach -z), x = quer. Pruefung der Haut-Rechnung: Idle Bild 0
gehaeutet liegt im Mittel 0,013 E (Junges) / 0,015 E (Baer) neben der Ruhelage (gleiche Pose, kleine Atem-Abweichung) -> Rechnung stimmt; die
`BIND`-Matrizen des Dumps sind KEINE Modellraum-Ruhe (Probezeile "Konvention" in `ausgabe.txt` deshalb ohne Aussage). Der Dump des alten Jungen
ist byte-gleich gross wie `_arbeit/baer_baby/entwurf/dump_fix1.txt` (7.704.451 Bytes).

### 4.2 Masse bei Groesse 1,0 (DeerStag_Idle01 Bild 0; Gehen = Mittel ueber DeerStag_Walk)

| Mass | altes Junges (6c3f0a96) | grosser Baer 2c (08ec7806) | gross / Junges |
|---|---|---|---|
| Laenge Nase - Rumpf | 0,9966 E = 1,832 m (Gehen 0,9697) | 1,0448 E = 1,921 m (Gehen 1,0167) | **1,048** |
| Oberkante (hoechster Punkt) | 0,5894 E = 1,083 m (= Kopf; Gehen 0,6062) | 0,6254 E = 1,150 m (= Schulterbuckel; Gehen 0,6222) | **1,061** (Gehen 1,026) |
| Schulterhoehe | 0,5338 E = 0,981 m | 0,6254 E = 1,150 m | 1,172 |
| Kopf-Oberkante | 0,5894 E | 0,5090 E | 0,864 |
| Breite | 0,4819 E = 0,886 m | 0,4867 E = 0,895 m | 1,010 |
| Kopfbreite / Kopflaenge | 0,3554 / 0,3100 E | 0,2357 / 0,2678 E | 0,66 / 0,86 |
| Ruhelage roh (Laenge/Hoehe/Breite) | 1,014 / 0,556 / 0,441 E | 1,0645 / 0,623 / 0,432 E | 1,050 |

Gegenprobe: grosser Baer roh 1,0645 E = 1,957 m (ENT:12 "1,96 m lang, 1,16 m Schulter"); bei 1,35: 1,0645 x 1,35 / 0,544 = 2,64 m und Oberkante
0,6254 x 1,35 / 0,544 = 1,55 m = Kevins Tabelle ENT:10 ("rund 2,65 m lang, 1,55 m Schulter"). Junges roh 1,014 E = 1,864 m (Bericht
`baer/spiel/baby_fix_baby.md:59`: L 1,857 m).

### 4.3 Groesse beim Tausch und Abbildung bis 1,35

| Tauschgroesse a (grosses Modell) | Laenge | Oberkante | Breite | Schulter | Beurteilung |
|---|---|---|---|---|---|
| 0,7154 (Laenge gleich) | +0,0 % | +1,2 % | -3,7 % | +11,8 % | |
| 0,7068 (Oberkante gleich) | -1,2 % | 0,0 % | -4,8 % | +10,4 % | |
| **0,72 (Vorschlag)** | **+0,6 %** | **+1,9 %** | -3,0 % | +12,5 % | kleinster Sprung in Laenge und Hoehe zugleich |
| 0,75 (Kevins Wortlaut "mit 0,75") | +4,8 % | +6,1 % | +1,0 % | +17,2 % | auch klein (Laenge +7 cm) |

(Schulter und Kopf unterscheiden sich durch die Form -- der Buckel kommt, der grosse Kopf geht; das ist der gewollte Modellwechsel.)

Abbildung (stueckweise gerade wie FD 1.5; Stellwerte `swapSize` 0,72, Ziel 1,35 = `stageAt[3]`):
`sz = s` (Junges, s < 0,75) bzw. `sz = 0,72 + (s - 0,75) x (1,35 - 0,72) / (1,35 - 0,75) = 0,72 + 1,05 x (s - 0,75)` (gross).

| Tag (D = 100) | s innen | Koerper | sz gezeigt | Laenge m | Laenge Kacheln | Oberkante m | Gehen Rumpf / Fuesse (Kacheln/s) | Rennen Rumpf / Fuesse |
|---|---|---|---|---|---|---|---|---|
| 0 | 0,350 | Junges | 0,350 | 0,64 | 0,52 | 0,38 | 0,523 / 0,183 (-65 %) | 2,47 / 0,86 |
| 10 | 0,617 | Junges | 0,617 | 1,13 | 0,92 | 0,67 | 0,523 / 0,322 (-38 %) | 2,47 / 1,52 |
| 14 | 0,723 | Junges | 0,723 | 1,33 | 1,08 | 0,78 | 0,523 / 0,378 (-28 %) | 2,47 / 1,78 |
| **15** | 0,750 | **gross** | **0,720** | 1,38 | 1,13 | 0,83 | 0,673 / 0,484 (-28 %) | 3,17 / 2,28 |
| 30 | 0,875 | gross | 0,851 | 1,63 | 1,33 | 0,98 | 0,673 / 0,573 (-15 %) | 3,17 / 2,70 |
| 45 | 1,000 | gross | 0,982 | 1,89 | 1,54 | 1,13 | 0,673 / 0,661 (-2 %) | 3,17 / 3,12 |
| 60 | 1,095 | gross | 1,083 | 2,08 | 1,70 | 1,24 | 0,673 / 0,728 (+8 %) | 3,17 / 3,44 |
| 80 | 1,223 | gross | 1,216 | 2,34 | 1,91 | 1,40 | 0,673 / 0,818 (+22 %) | 3,17 / 3,86 |
| **100** | 1,350 | gross | **1,350** | 2,59 | 2,12 | 1,55 | 0,673 / 0,908 (+35 %) | 3,17 / 4,28 |

Zuwachs je Tag nach dem Tausch 0,0087 (Tag 15-45) / 0,0067 (Tag 45-100) gezeigte Groesse -- kein sichtbarer Sprung. Werte (Leben, Traglast ...)
rechnen weiter mit der INNEREN Groesse s (PB1D 0.6), unveraendert.

**Groesse setzen:** wie bisher nur `B.ApplySize` -> `animal:getData():setSizeForced(zahl)` (BELEGT, FD 1.1; Grenzfall lebendes Tier wie B1d).
**Definition** der neuen Art: `minSize = 0,72`, `maxSize = 1,35` (Weg B, FD 1.3), damit Laden/MP-Erstuebertragung die Groesse halten und ein
frischer Koerper gleich 0,72 hat. **MP-Client:** die Probe `S:client/ISUI/BanditsNPCBearHud.lua:459` setzt `c.sz` an die Kopie -- im Tauschfenster
(alte Kopie noch da, Sicht schon neu) muss sie pruefen, dass der Koerper der Kopie (`getAnimalType`) zum Koerper der Sicht passt -> Sicht traegt
neu `bd` ("cub"/"big") aus `B.GrowView` (`S:server/BanditsNPCBearGrow.lua:596-620`).

**Namensschild-Hoehe:** heute `a:getZ() + tagZ x sz / tagBase` (`S:client/ISUI/BanditsNPCBearHud.lua:364-371`, `:619-623`; `tagZ` 0,18 fuer die
Kopfoberkante des Jungen bei 0,35). Der grosse Koerper ist bei gleicher Groesse 1,061 x hoeher (Oberkante = Buckel) -> Faktor je Koerper
`tagBody = { cub = 1.0, big = 1.06 }` (Stellwert; Gehen nur 1,026). Bei 1,35: 1,35 / 0,35 x 1,06 = 4,09 < Deckel `ZK_MAX` 5 (`:67`). Im Spiel ansehen.

### 4.4 Tempo und Fussgleiten

| Clip | altes Junges: Weg / Dauer -> Kacheln/s | grosser Baer: Weg / Dauer -> Kacheln/s | heutige Stellwerte |
|---|---|---|---|
| DeerStag_Walk | 0,2940 E / 0,900 s -> **0,523** | 0,3784 E / 0,900 s -> **0,673** | `walkSpeed = 0.52` (`S:shared/BanditsNPCBear.lua:91`) |
| DeerStag_Run | 0,8218 E / 0,533 s -> **2,465** | 1,0578 E / 0,533 s -> **3,173** | `runSpeed = 2.47` (ebd.) |

(Zahlen gleich `forschung_b1b.md:37` fuer das Junge und `baer/spiel/bau_lebend.md:41-42` fuer den Baeren.) Spieler gehend ~2,27 Kacheln/s
(`baer/spiel/tier_spez.md:237`): beide muessen zum Mitgehen rennen; der grosse rennt 29 % schneller als das Junge.

- **Warum es gleitet:** beide Clips sind fuer Groesse 1,0 ohne Gleiten gebaut (Baer: Ballen wandert 0,01-0,02 Kacheln je Stuetze,
  `baer/spiel/bau_lebend.md:48`; Junges: Weg x 0,777 = Beinfaktor, `baer/spiel/baby_fix_baby.md:31`). Das Bild waechst mit der Groesse
  (`finalScale = AnimalData.getSize()`, NUR JAR FD 1.2), der Weg nicht (kein Bewegungscode liest die Groesse, FD 1.2) -> Fuesse bewegen sich mit
  `Tempo x sz`, der Rumpf mit `Tempo`. Tabelle 4.3: nach dem Tausch -28 % (wie das Junge kurz davor), um Tag 47 null, bei 1,35 +35 %
  (Fuesse schneller als der Boden: "Tretmuehle").
- **Hebel in B1e:** keiner fuer das Gleiten selbst. `buck` hat in Gehen/Wegfindung keine Tempo-Variable (`VA:buck/walk/defaultWalk.xml`,
  `VA:buck/walk/run.xml`, `VA:buck/pathfind/defaultPathfind.xml`, `runPathfind.xml`: kein `m_SpeedScale`); Vanillas Kuh skaliert mit
  `<m_SpeedScale>animalSpeed</m_SpeedScale>` (`VA:cow/walk/defaultWalk.xml:6`) -- das ginge nur ueber eigene Knoten (Modell-/Animset-Arbeit, nicht B1e)
  plus Kevins Wort fuer `setVariable("animalSpeed", zahl)` am Tier. Achtung: ein Knoten in `AnimSets/buck/walk` gilt auch fuer Vanillas Hirsche.
- **Was B1e einstellen muss:** `walkSpeed`/`runSpeed` JE KOERPER (gross 0,673 / 3,17) -- sie stehen in der Gehen-Regel (`S:shared/BanditsNPCBearRules.lua:530`,
  "Besitzer langsamer als walkSpeed") und in der Wegzeit des eigenen Befehls (`S:server/BanditsNPCBearWorld.lua:866-871`, `ownUntil` -> Laerm-Wache
  B5) sowie im Kondition-Sprungdeckel (`S:server/BanditsNPCBearGrow.lua:358`). Mit dem alten Jungen passen 0,52 / 2,47 wieder (gemessen).
- **Folgen-Abstaende mit der Koerperlaenge** (`followNear 3`, `followStart 4.5`, `followGap 2`, `hideGap 1.5`, `calmGap 1.5`; Kacheln von Mitte zu Mitte,
  `S:shared/BanditsNPCBear.lua:73`, `:86`, `:93`): Laenge in Kacheln (1,5 je E) Junges 0,75 -> 1,12; gross 0,72 -> 1,13; s 1,0 -> 1,54; 1,35 -> 2,12. Bei
  `followGap 2` steht die Nase des ausgewachsenen Baeren (halbe Laenge 1,06) ~0,9 Kacheln vor der Mitte des Besitzers; beim Verstecken
  (`hideGap 1.5`) ragt er in den Besitzer. Vorschlag: je Abstand `+ (L_kacheln(sz) - 1,12) / 2` (bei 1,35 +0,5) -- Stellwert, im Spiel ansehen.
- **Streichel-Haltung:** heute fest `animal = "lamb"`, `AnimalSizeY 0.5` (`S:shared/TimedActions/BanditsNPCBearPetAction.lua:55-58`). Vanilla hat je
  Tier eigene Knoten, die ueber `AnimalSizeY` 0..1 zwischen klein und gross mischen: `VA:player/petanimal/petlamb.xml` (Bob_PetLamb_Small/_/Large),
  `petcow.xml` (Bob_PetCow_*), `petcalf.xml`, `defaultpet.xml` (Bob_PetBull_*); Vanilla rechnet `AnimalSizeY = (size - min) / (max - min)`
  (`V:shared/TimedActions/Animals/ISPetAnimal.lua:27-32`). Fuer den grossen Koerper bietet sich z. B. `"cow"` mit `AnimalSizeY` aus der Groesse an --
  Wirkung ungespielt (F4).

---

## 5. Was die Engine beim Entfernen / Neuanlegen mit den Daten tut (Auftrag e)

| Daten | beim neuen Koerper | Fundstelle | Folge fuer den Tausch |
|---|---|---|---|
| Art | die von `addAnimal` | `S:server/BanditsNPCBearWorld.lua:473` | Parameter (3.2 Nr. 1) |
| ModData (unser Spiegel) | leer | FD 0.5 (Stufenwechsel kopiert sie auch nicht, `dec/AnimalData.java:1389-1404`) | `B.PlaceCub` schreibt den Spiegel sofort (`Ride.lua:84`) |
| Groesse | minSize (`initSize` -> `setSize(0.1)`) | `dec/AnimalData.java:1353-1358` (NUR JAR, FD 0.8) | `B.GrowBody` setzt sofort (`Ride.lua:86`); mit `minSize = 0,72` der neuen Art faellt ein spaetes Setzen nicht auf |
| Leben | 1,0 | `dec_b1b/IsoGameCharacter.java:574` (NUR JAR, FD 0.8) | `B.BodyHp(rec, a, 0)` setzt den Anteil `rec.hp` (`S:server/BanditsNPCBearGrow.lua:481`); `hpB` verhindert, dass der Anstieg als Heilung zaehlt (PB1D 0.5) |
| AnimalID, OnlineID | neu | PB1C 3.2 | `rec.aid` neu (`Ride.lua:73`); die Sicht schickt die neue OnlineID (`pushNewSights`, `S:server/BanditsNPCBearServer.lua:893-917`) |
| Alter, Stress, Akzeptanz, Hunger/Durst | Alter 1, Stress/Akzeptanz 0 | `dec/IsoAnimal.java:1537-1544` (NUR JAR, FD 2), PB1C 3.2 | B1a-B1d benutzen keinen davon (Akzeptanz 0: Q-Ruf holt es nicht -- wie nach jeder Autofahrt) |
| Lage | ganze Kachel (`math.floor`) | `S:server/BanditsNPCBearWorld.lua:473` | Sprung innerhalb der Kachel (< 1 Kachel) |
| Blickrichtung | Vorgabe | PB1C 3.2 | **nicht uebertragbar mit Belegen**: `getForwardDirection()`/`:set(x, y)` nur am Spieler/Zombie (`V:client/DebugUIs/ISFastTeleportMove.lua:7`, `B:shared/Bandit.lua:1452`), `setDir(IsoDirections)` nur am Spieler/Zombie (`V:client/Tutorial/Steps.lua:831`). Am Tier BELEGT ist nur `animal:faceThisObject(Spieler)` (`V:shared/TimedActions/Animals/ISPetAnimal.lua:17`) -> Vorschlag: neuer Koerper schaut zum Besitzer (F5) |
| Register | bleibt (Besitzer, Name, Zaehmung, g, Erfahrung, hp, Modus, Heimat, u) | PB1C 3.2, PB1D 3 | `gen + 1`, `r + 1`, `aid` neu |
| alter Koerper | `remove()` hinterlaesst keine Leiche; MP `removeAnimal(OnlineID)` | `S:server/BanditsNPCBearWorld.lua:488-503` | Clients verlieren die Kopie |
| Speichern/Laden | die Engine speichert Art + Groesse, laedt mit Klemme [min, max] | FD 1.2 (`dec/IsoAnimal.java:1299`, `:1413`) | grosser Koerper bleibt gross; Art muss fuer immer definiert sein |
| Sitzung (Kern) | leer | `clearBodySession` `Ride.lua:52-56`, `B.CalmDrop`, `B._zed` (`:87-88`) | Folgen/Wachen beginnen im naechsten Takt neu |

Speichern/Laden, Mitfahren, Call to me, Heilung behalten den Koerper von selbst, wenn `B.PlaceCub` immer `B.BodyOf(rec)` erzeugt und der Suchlauf
beide Arten bindet. Ein B1d-Spielstand (Junges ueber 0,75 im Junges-Koerper) tauscht beim ersten sicheren `GrowLive`.

---

## 6. Markierung groesser (Auftrag f, Punkt 7)

### 6.1 Heute

- Unser Weg: `S:client/ISUI/BanditsNPCBearMarker.lua` -- je 400 ms (`markerMs`, `Events.OnTick`, `:177-221`, `:236`) Bandits'
  `BanditEventMarkerHandler.set(ID, ICON, 1800, x, y, COLOR, text)` mit fester Id (`:94-98`), Farbe `{ r = 1.0, g = 0.72, b = 0.30 }` (`:46`), Text
  `UI_BN_Bear_Marker_Cub`, Ausblenden mit Dauer 0 (`:101-105`), Doppelklick-Erkennung (`:191-198`), Verschieben bei Ueberdeckung um 100 px
  (`:128-144`), altes Element selbst aus dem UIManager (`:120-124`). Nur mit Bandits (Riegel `:77-81`), nur wilde Junge (`:147-173`).
- Bandits zeichnet (alles fest 96 px, keine Skalierung): `BanditEventMarker.iconSize = 96` (`B:client/BanditEventMarkers.lua:7`), Klickflaeche 45 px
  (`:8`, `:240-241`); Kreis `drawTexture(self.textureBG, centerX-48, centerY-48, 1, r, g, b)` (`:174`); Text `drawTextCentre(desc, centerX, centerY + 25,
  ..., UIFont.Small)` (`:176`); Pfeil `DrawTextureAngle(textureForPoint, centerX, centerY, self.angle)` (`:192`); Symbol `drawTexture(self.textureIcon, ...)`
  (`:193`). Lage beim Anlegen `getCore():getScreenWidth()/2 - 48`, `y = 48` oder die gezogene Stelle aus `player:getModData()["BanditEventMarkerPlacement"]`
  (`B:client/BanditEventMarkerHandler.lua:17-23`). Bilder `Bc:ui/eventMarkerBase.png`, `eventMarker.png`, `eventMarker_close/_medium/_far.png`: je
  96 x 96 (nachgemessen). Unser Symbol `S:media/ui/BanditsNPCBearCub_marker.png` 96 x 96.
- Farbe im Bild: `colorBlend` (`B:client/BanditEventMarkers.lua:147-157`) mit `fade = 0,2 + 0,8 x (1 - Abstand/Radius)` (`:168`; Radius 1245 Kacheln
  draussen am Tag, `:302-325`) -> bei unseren <= 65 Kacheln fade >= 0,96 -> Kreis etwa **(1,0 / 0,52 / 0,09)** (Farbe quadriert) = Kevins "kraeftiges
  Orange" (ENT Markierung). Pfeil-Bild nach Abstand: "close" bis ~6,6 Kacheln draussen (`:182-190`), sonst `eventMarker.png`.
- Bei 3840 x 2054 ist der Kreis 96 px = 4,7 % der Bildhoehe (bei 1080: 8,9 %).

### 6.2 Wege (Planer waehlt; Empfehlung A)

| Weg | wie | Belege | Urteil |
|---|---|---|---|
| **A eigenes UI-Element** (empfohlen) | `ISUIElement:derive`, eigenes `render`: Kreis + Symbol mit `drawTextureScaled` (beliebige Groesse), Pfeil mit `DrawTextureAngle` aus **eigenen Pfeil-Bildern je Groessenstufe**, Text mit groesserer Schrift; Ziel/Lage/Frist wie heute (`target()`), Doppelklick blendet aus | Tabelle 6.3 | alles BELEGT; laeuft auch ohne Bandits; eigene Bilder noetig (OBERFLAECHE) |
| B Bandits-Element umzeichnen | nach `set()` am EIGENEN Marker-Objekt `markers[ID].render` ersetzen | Bandits-Felder (`textureBG`, `angle`, `desc` ...) sind Bandits-Interna | zerbrechlich bei Bandits-Updates; Pfeil braucht trotzdem eigene Bilder (DrawTextureAngle skaliert nicht) -> kein Gewinn |
| C `BanditEventMarker.iconSize` aendern | Klassenfeld (`B:client/BanditEventMarkers.lua:7`) | -- | **kein Weg**: verschiebt nur die Lage (`drawTexture` zeichnet in Bildgroesse) und traefe ALLE Bandits-/NPC-Crew-Marker |
| D stufenloser Pfeil | `self:drawTextureAllPoint(tex, 4 Ecken, r, g, b, a)` mit selbst gedrehten Ecken | Lua-Wrapper `V:client/ISUI/ISUIElement.lua:1013-1018` (darin der Engine-Aufruf `self.javaObject:DrawTexture(texture, tlx, ... , r,g,b,a)` `:1016`); **kein Vanilla-/Bandits-Aufrufer** des Wrappers; gleiche Java-Methode mit `nil` statt Bild in `drawLine2` (`:1231`, Aufrufer `V:client/DebugUIs/SeamEditor/SeamEditorUI.lua:246`) | Grenzfall -> nur mit Kevins Wort |

### 6.3 Aufrufe fuer Weg A (Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil)

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| eigenes Element | `X = ISUIElement:derive("Name")` | `V:client/Chat/ISAlert.lua:3`, `V:client/Fishing/TensionUI.lua:3` | Client | BELEGT |
| anlegen / anmelden / abmelden | `X:new(x, y, w, h)`, `:initialise()`, `:addToUIManager()`, `:removeFromUIManager()` | `V:client/Chat/ISAlert.lua:54`; `V:client/ISUI/Animal/ISAnimalContextMenu.lua:746-747`; `V:client/ISUI/ISUIElement.lua:1373`, `V:client/ISUI/Maps/ISMap.lua:116` (wie Hud `S:client/ISUI/BanditsNPCBearHud.lua:754-761`) | Client | BELEGT |
| Kreis, Symbol skaliert + gefaerbt | `self:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | `V:client/Chat/ISChat.lua:418` (9 Argumente), `V:client/DebugUIs/ISSpawnVehicleUI.lua:171` | Client | BELEGT |
| Pfeil gedreht | `self:DrawTextureAngle(tex, cx, cy, winkel)` | `V:client/Fishing/TensionUI.lua:21`, `V:client/ISUI/Fireplace/ISKnob.lua:24`, `B:client/BanditEventMarkers.lua:192` | Client | BELEGT -- zeichnet in **Bildgroesse**, Winkel in Grad (+180 intern), Mitte relativ zum Element (NUR JAR, 8) -> ein Pfeil-Bild je Stufe |
| Text groesser | `self:drawTextCentre(text, x, y, r, g, b, a, UIFont.Medium / UIFont.Large)` | `V:client/DebugUIs/StashDebug.lua:86` (Medium), `V:client/Chat/ISAlert.lua:35` (Large) | Client | BELEGT; `drawTextZoomed` hat KEINEN Aufrufer (grep, wie PB1C 0.8) -> Schrift in Stufen |
| Schrifthoehe | `getTextManager():getFontHeight(UIFont.X)` | `V:client/DebugUIs/AnimationClipViewer.lua:4-5` | Client | BELEGT |
| Bildschirmhoehe/-breite | `getCore():getScreenHeight()`, `getCore():getScreenWidth()` | `V:client/Chat/ISChat.lua:1167`, `V:client/Chat/ISAlert.lua:34`; `V:client/Challenge/WinterIsComing.lua:18` | Client | BELEGT |
| Aufloesung geaendert | `Events.OnResolutionChange.Add(function(oldw, oldh, neww, newh) ... end)` | `V:client/ISUI/PlayerData/ISPlayerData.lua:185`, `:206`; `V:client/OptionScreens/MainScreen.lua:2155` | Client | BELEGT (Wert zwischenspeichern, nicht je Bild fragen) |
| Bilder | `getTexture("media/ui/<datei>.png")` | `V:client/Chat/ISChat.lua:921`; Bandits-Bilder zur Laufzeit nur, wenn Bandits geladen (Riegel wie `S:...Marker.lua:77-81`) | Client | BELEGT |
| Richtung auf dem Bildschirm | `isoToScreenX/Y(spielerNr, x, y, z)` fuer Spieler und Ziel, Winkel = atan2 der Differenz | `V:client/Fishing/TensionUI.lua:11-12` (wie Hud `S:client/ISUI/BanditsNPCBearHud.lua:613`) | Client | BELEGT (genauer als Bandits' feste 45-Grad-Formel `B:...Markers.lua:118-128`; Ausrichtung des eigenen Pfeil-Bildes im Spiel ansehen) |
| Doppelklick | `function X:onMouseDoubleClick(x, y)` | `V:client/ISUI/ISButton.lua:66`, `B:client/BanditEventMarkers.lua:19-21` | Client | BELEGT |
| Takt | `Events.OnTick` + `getTimestampMs()` (heute 400 ms) | `V:client/Chat/ISChat.lua:943` | Client | BELEGT (wie heute) |
| Ueberdeckung mit NPC Crews Pfeil | nur LESEN `BanditEventMarkerHandler.markers[*].x/.y`, `getDuration()`, `getIsVisible()` (Riegel) | heute `S:...Marker.lua:128-144` | Client | wie heute; Schub x Faktor |

Kosten je Bild: 3 Texturen + 1 Text + (optional) 2 `isoToScreen`; Ziel/Lage weiter je 400 ms. Deckel: genau ein Element (feste Variable, alt
abmelden wie die Hud `S:client/ISUI/BanditsNPCBearHud.lua:754-761`).

Groesse: Faktor `f` = Option (Index -> 1,0 / 1,25 / 1,5 / 2,0 / 2,5 / 3,0) oder **Auto = clamp(Bildschirmhoehe / 1080, 1, 3)** (1080 -> 1,0, 1440 -> 1,33,
2160 -> 2,0; Kevins 2054 -> 1,90), fuer den Pfeil auf die naechste Bild-Stufe gerundet (Kevin: 200 % = 192 px). Lage wie Bandits mal f: Element
(Klickflaeche 45 f) bei `Breite/2 - 48 f`, `48 f`; Kreis 96 f um die Elementmitte, Text bei `+25 f` (Small < 1,25 <= Medium < 1,75 <= Large).
Farbe des Kreises fest ~(1,0 / 0,52 / 0,09) (= heutiges Bild, 6.1), Symbol weiss (1, 1, 1).

Eigene Bilder (OBERFLAECHE, eigene Zeichnung, nichts von Bandits): Kreis 288 px (weiss, wird gefaerbt), Pfeil-Ring je Stufe 96 / 120 / 144 / 192 /
240 / 288 px (+ wahlweise "close"), Symbol 288 px -- das Zeichen-Skript kann es schon (`baer/spiel/icon_zeichne_v2.py:150-169`: "auf 96 und auf 288
verkleinern"). Namen `42/media/ui/BanditsNPCBear*.png` -- die Uebernahme nimmt sie (`baer_uebernahme.py:122-123`, Deckel 512 px).

Verhalten wie heute: verschwindet ~60 s nach dem ersten "shy" (`markerAfterMs`), bei angefuettert/gezaehmt, ohne Eintrag, ohne Lage; Doppelklick
blendet fuer dieses Junge aus. Offen: ziehbar wie bei Bandits (dort gemeinsame Stelle aller Bandits-Marker, `BanditEventMarkerPlacement`)? (F7)

### 6.4 Optionen-Seite (B1c) erweitern

Seite `BanditsNPCBear` (`S:client/BanditsNPCBearOptions.lua:58-84`). Neu `o:addComboBox("MarkerSize", "UI_BN_Bear_MO_MarkerSize",
"UI_BN_Bear_MO_MarkerSizeTip")` mit `addItem` "Auto" (Vorgabe) / 100 / 125 / 150 / 200 / 250 / 300 % -- reines Vanilla-Lua
`V:client/PZAPI/ModOptions.lua:121-156` (`addItem` ruft `getText` sofort `:132` -> Schluessel; `getValue` = Index `:137`), gespielt bei NPC Crew
(`NC:client/BanditsNPCModOptions.lua:97-103`). Nicht `addSlider` (kein Aufrufer, Regel-Frage aus B1c, `:21-24`). Lesen ueber `U.Opt` (1 s Cache, `:90-113`).
Texte x 7 (Vorschlag EN): `UI_BN_Bear_MO_MarkerSize` "Size of the cub marker at the top of the screen", `UI_BN_Bear_MO_MarkerSizeTip` "Auto grows with
the screen height (1080p = 100 %, 4K = 200 %).", `UI_BN_Bear_MO_Auto` "Auto", Stufen `UI_BN_Bear_MO_Pct100` ... `_Pct300` ("100 %" ...). CN-Zeichen
geprueft in Vanilla-CN vorhanden: 自 动 标 记 大 小 屏 幕 顶 部 高 度 随 变 化 分 辨 率 熊 示 显 图 的.

---

## 7. Register, Spiegel, Sicht, Bench (Ergaenzungen)

- Register: `rec.body` ("cub"/"big"; fehlt = aus `s` mit Schwelle 3.4). Spiegel v2 (`B.MARK_V` bleibt 2): `"body"` in `MARK_FIELDS`
  (`S:server/BanditsNPCBearHeal.lua:40-44`); beim Binden/Wiederherstellen gilt der Koerper des Tiers (`getAnimalType`), nicht der Spiegel.
  `B.Restore` an einem grossen Koerper mit einem nicht zahmen Spiegel: nie ein neuer Wildfund (Stelle 4) -- unberuehrt lassen + Fehlerzeile.
- Sicht: `bd` je gezaehmtem Eintrag (fuer Schild-Faktor, MP-Groessen-Probe, Anzeige).
- Bench (nur `NCBearBench*`, nur SP): `NCBear_CubStats()` druckt `st.body` schon (`S:client/NCBearBenchCub.lua:841`) -- dazu `getAnimalType()` des lebenden
  Tiers (`:867`); `NCBear_CubGrow(t)` ruft `B.GrowSetG` + `B.BrainTick(true)` (`:817-830`) -> der Tausch kommt im selben Aufruf ueber `GrowLive`;
  `NCBear_CubGrow(-100)` -> g = 0 -> `s` 0,35 < 0,70 -> zurueck zum Junges-Koerper. `B.GrowSetG` setzt heute die Groesse direkt am gefundenen Tier
  (`S:server/BanditsNPCBearGrow.lua:630-635`) -> nur am passenden Koerper.
- Lokale je Datei (localcount, 11.11.): hoechstens 48 (Hud Hauptteil) -- weit unter 180.

---

## 8. NUR im Jar belegt (getrennt) -- Wissen, kein Engine-Aufruf

| Aussage | Fundstelle |
|---|---|
| `UIElement.DrawTextureAngle(tex, cx, cy, angle)` zeichnet mit `tex.getWidth()/2`, `getHeight()/2` (Bildgroesse), Winkel `toRadians(180 + angle)`, Mitte + `getAbsoluteX/Y` | `javap -c -p zombie/ui/UIElement.class`, Zeilen 786-992 der Ausgabe (Scratchpad, aus `projectzomboid.jar` mit Python zipfile gezogen) |
| `UIElement.DrawTexture(tex, 8 Ecken, r, g, b, a)` nimmt die Ecken absolut (ohne `getAbsoluteX/Y`) | ebd. Zeile 994-1035 |
| Groesse wirkt auf Bild, Kollision, Schatten; Tempo nicht | FD 1.2 (`javap/b1d_ModelSlotRenderData.txt:746-752`, `dec/IsoAnimal.java:420`, `:433`) |
| neuer Koerper: minSize, Leben 1,0, Alter 1, keine ModData | FD 0.8, FD 2 |
| Weg je Clip = `Translation_Data` x MotionScale 1,6 | `baer/spiel/tier_spez.md:229` (Defaults.xml, AdvancedAnimator) |
| Masse/Wege der Modelle | Spiel-Importer (Harness `Dump.java`), keine Engine-Lua |

---

## 9. Fragen fuer Kevin (er spielt gerade -- jede mit Empfehlung; nichts haelt den Bau auf)

| # | Frage | Empfehlung |
|---|---|---|
| F1 | Groesse beim Wechsel: 0,72 (wirkt gleich gross wie das Junge) oder woertlich 0,75 (+5 % laenger, +6 % hoeher)? | 0,72, am Ende genau 1,35 |
| F2 | Name der neuen Art (fuer immer, steht in Spielstaenden): `ncbeargrown`? | ja (Ingame-Name EN "Bear") |
| F3 | Meldungen und Schild nach dem Wechsel "your bear" statt "your cub" ("%1's bear")? | ja, Texte je Koerper |
| F4 | Streichel-Haltung beim grossen Koerper: Vanilla-Haltung "cow" (mit Groesse gemischt) statt "lamb"? b) Toene: bleibt das Junges-Set (kein Brummen) bis B5a? | ja / ja |
| F5 | Blickrichtung beim Wechsel: neuer Koerper schaut zum Besitzer (belegt) statt die alte Richtung (am Tier unbelegt)? | ja |
| F6 | Fussgleiten: nach dem Wechsel -28 % (wie heute das Junge), am Ende +35 %. So lassen bis ein eigener Geh-Knoten kommt? | im Spiel ansehen, dann entscheiden |
| F7 | Markierung als eigenes Element: Doppelklick blendet aus wie heute; soll sie auch ziehbar sein (Stelle merken)? | Doppelklick ja, Ziehen erst auf Wunsch |
| F8 | Markierungs-Stufen: Auto + 100 / 125 / 150 / 200 / 250 / 300 %? Stufenlos nur mit deinem Wort fuer `drawTextureAllPoint`. | Stufen |
| F9 | Uebernahme: das grosse Modell (NCBear.glb/.png, Modell-Skript) geht ab B1e mit nach NPC Crew (heute Altlast bis B5a)? | ja, mit eigenem kleinen Modell-Skript ohne den Hirsch-Rueckfall (Plan) |
| F10 | Kollision des grossen Koerpers 0,30 (0,22 beim Wechsel, 0,41 ausgewachsen) | im Spiel ansehen |
| F11 | Versteckt sich der Halbstarke weiter hinter dir (bis der Kampf B5a kommt)? | ja (Auftrag 4) |
| F12 | Wechsel vor deinen Augen sichtbar (ein Bild lang zwei Koerper nur im Mehrspieler-Netz denkbar) -- ok? | ja |

---

## 10. Luecken (ungeprueft, Testpunkte)

1. Ob `setSizeForced` direkt nach `addToWorld` im selben Bild wirkt (FD 1.6) -- mit `minSize = 0,72` unkritisch beim Wechsel, bei Call/Aussteigen
   spaeter kurz 0,72 bis zum naechsten Hirn-Takt.
2. MP: `getObjectListForLua`/`getAnimalID` am Server (A3), `setHealth`/`getHealth` am Tier am Server (PB1D 8), Reihenfolge `addAnimal` + `removeAnimal`
   im selben Takt bei den Clients, Groessen-Probe im Tauschfenster.
3. Optik: Schild-Faktor 1,06, Folgen-Abstaende, Kollision 0,30, Fussgleiten, Streichel-Haltung, Pfeil-Ausrichtung des eigenen Bildes, Lesbarkeit
   der Schrift in Stufen (Kevins Schriftgroessen-Option veraendert `UIFont.*`).
4. Fuettern/Streicheln waehrend des Wechsels: kein Verlust (statisch), aber Meldung "The cub is gone." -- unschoen (3.5).
5. Der Generator-Junge liegt noch als `NCBearCub.glb` im Staging (Abschnitt Vorab).
6. Ob ein grosser Koerper an engen Stellen (Tuer) nach dem Wechsel festsitzt -- "Call to me" holt ihn (B1c).
