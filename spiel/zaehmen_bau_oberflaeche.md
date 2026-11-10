# Lauf baer-zaehmen (B1a): Bau OBERFLAECHE -- Bericht

Stand 10.11.2026 ~20:45. **Statisch geprueft, nicht gespielt.** Nichts in die Test-Mod, nichts nach NPC Crew, nichts committet.
Fortsetzung des um 18:11 abgebrochenen Laufs: der Teilstand (7 Lua-Dateien) wurde ganz gelesen, gegen PLAN_ZAEHMEN.md geprueft
und weitergebaut; Texte (21 JSON), sandbox-options.txt, Attrappen und Pruefskripte fehlten und sind neu.
`M/` = `_arbeit/baer_zaehmen/mod/42/media/`, `V:` = Vanilla `media/lua`.

## 1. Dateien

| Nr (Plan 6.1) | Datei | Zeilen | Stand |
|---|---|---|---|
| 10 | `M/lua/shared/TimedActions/BanditsNPCBearFeedAction.lua` | 117 | Teilstand vollstaendig, geprueft |
| 11 | `M/lua/shared/TimedActions/BanditsNPCBearPetAction.lua` | 118 | Teilstand vollstaendig, geprueft |
| 12 | `M/lua/shared/TimedActions/BanditsNPCBearBaitAction.lua` | 69 | Teilstand vollstaendig, geprueft |
| 13 | `M/lua/client/BanditsNPCBearClient.lua` | 263 | Teilstand; ein Kommentar geaendert |
| 14 | `M/lua/client/BanditsNPCBearMenu.lua` | 327 | Teilstand; nachgebessert: zwei gleichnamige Junge werden je NAME gezaehlt (vorher je Index -> falsches Untermenue moeglich), Fundstelle setName :162 |
| 15 | `M/lua/client/ISUI/BanditsNPCBearHud.lua` | 367 | Teilstand vollstaendig, geprueft |
| 16 | `M/lua/client/NCBearBenchCub.lua` | 387 | Teilstand; nachgebessert: zuerst `B.IsSP()` pruefen (MP-Client meldete sonst "core not loaded" statt "singleplayer only") |
| 17 | `M/lua/shared/Translate/<L>/UI.json` x 7 | - | NEU |
| 18 | `M/lua/shared/Translate/<L>/Sandbox.json` x 7 | - | NEU |
| 19 | `M/lua/shared/Translate/<L>/IG_UI.json` x 7 | - | NEU (EN: alte 4 Schluessel wortgleich + 2 neue) |
| 20 | `M/sandbox-options.txt` | 159 | NEU, 19 Optionen, Form NC `sandbox-options.txt:12-17`/`:155-161`, Tabs, LF, ASCII, nur C-Kommentare |

Werkzeuge und Tests (werden nie kopiert):
- `_arbeit/baer_zaehmen/ober_werkzeug/texte.py` -- EINZIGE Quelle aller Texte; schreibt die 21 JSON und sandbox-options.txt
  (sortiert, `json.dumps(data, indent=4, ensure_ascii=False) + "\n"`, UTF-8 ohne BOM, LF).
- `attrappe/ober/run.lua` -- Attrappen-Test (lua5.1), zwei Arten: eigene Kern-Attrappe nach 6.2 bzw. mit `kern` die echten shared-Dateien des Kerns.
- `attrappe/ober/texte_pruefen.py` -- Texte, Platzhalter, Round-Trip, CN-Zeichen, sandbox-options gegen `B.OPTS`, Dateiform, verbotene Woerter.
- `attrappe/ober/belege.py` -- haelt 112 zitierte Fundstellen gegen die heutigen Vanilla-Dateien.

Eigene Helfer liegen nur unter `B.UI` (schnittstelle_aenderungen.md, OBERFLAECHE Eintrag 1); direkt an `B` nur `B.ShowNote` und `B.OnView`.
Globale Namen in den `BanditsNPCBear*`-Dateien: nur `BanditsNPC` und die drei Aktionsklassen. Die Bench setzt ihre `NCBear_Cub*`-Befehle
und haengt sich in `NCBearMenu.extra` (NCBearTest `client/NCBearTest.lua:10-11`, `:132-134`; Ladefolge: NCBearBenchCub vor NCBearTest, beide
mit `or {}`) -- keine alte Datei geaendert.

## 2. Engine-Aufrufe mit Fundstelle (alle von `belege.py` gegen die Dateien gehalten: 112 von 112 stimmen)

| Aufruf | Fundstelle | Datei(en) |
|---|---|---|
| `ISBaseTimedAction:derive`, `.new`, `.stop`, `.forceStop`, `.perform` | V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3, :29, :35, :42; ISPetAnimal.lua:57, :66 | 10-12 |
| `animal:isExistInTheWorld()` | V:client/ISUI/Animal/ISAnimalUI.lua:15; ISFeedAnimalFromHand.lua:14; ISAnimalContextMenu.lua:88 | 10, 11, 14, 15 |
| `animal:isDead()` | V:client/ISUI/Hutch/ISHutchUI.lua:427 | 10, 11, 15 |
| `sq:DistTo(sq)` | V:shared/TimedActions/Animals/ISPetAnimal.lua:6 | 10, 11 |
| `inv:contains(item)` | ISFeedAnimalFromHand.lua:6 | 10, 12 |
| `faceThisObject`, `shouldBeTurning`, `setIsAiming(false)` | ISPetAnimal.lua:10, :11, :15, :17 | 10, 11 |
| `setActionAnim(animal:getFeedByHandAnim())`, `setOverrideHandModels` | ISFeedAnimalFromHand.lua:15-16; ISPetAnimal.lua:25 | 10, 11 |
| `animal:getBehavior():setBlockMovement(b)` | ISFeedAnimalFromHand.lua:19, :28; ISPetAnimal.lua:36, :49 | 10, 11 |
| `playSound("GiveFoodAnimal")`, `getEmitter():isPlaying/stopOrTriggerSound` | ISFeedAnimalFromHand.lua:23, :61-62 | 10 |
| `isTimedActionInstant()` | ISFeedAnimalFromHand.lua:54 | 10-12 |
| `animal:setVariable(name, text)`, `animal:clearVariable(name)` | ISPetAnimal.lua:43, :48 | 10 |
| `character:setVariable("AnimalSizeX"/"AnimalSizeY"/"petanimal"/"animal", ...)` | ISPetAnimal.lua:26, :32, :37, :39, :47 | 11 |
| `setActionAnim("Loot")`, `SetVariable("LootPosition","Low")`, `reportEvent("EventLootItem")` | V:shared/Camping/TimedActions/ISAddFuelAction.lua:41-43 | 11 (Rueckfall), 12 |
| `HaloTextHelper.addGoodText / addBadText / addText` | V:client/ServerCommands.lua:183; ISWorldObjectContextMenu.lua:1038; Foraging/forageClient.lua:73 | 13 |
| `getTimestampMs()` | V:server/Foraging/forageServer.lua:456; client/Foraging/ISBaseIcon.lua:485 | 13, 15 |
| `getSpecificPlayer(0)`, `getPlayer()`, `getNumActivePlayers()` | ISAnimalContextMenu.lua:134; ServerCommands.lua:204; Fishing/FishingHandler.lua:6 | 13-16 |
| `Events.OnServerCommand/OnGameStart/OnTick/OnClickedAnimalForContext/OnFillWorldObjectContextMenu.Add` | ServerCommands.lua:218; Chat/ISChat.lua:1186, :943; ISAnimalContextMenu.lua:1235; Hutch/ISHutchMenu.lua:115 | 13-15 |
| `ISWorldObjectContextMenu.addToolTip()`, `tooltip:setName`, `.description`, `option.notAvailable` | ISAnimalContextMenu.lua:160-162; ISWorldObjectContextMenu.lua:272 | 14 |
| `context:addOption`, `ISContextMenu:getNew`, `addSubMenu`, `iconTexture`, `getTexture("media/ui/AnimalActions_Pet.png")` | ISAnimalContextMenu.lua:272-274, :280, :287-288; :48-49 | 14 |
| `context:getOptionFromName`, `context.options`, `getSubMenu(opt.subOption)`, `removeOptionByName` | Tutorial/Tutorial1.lua:131; ISContextMenu.lua:889-895, :1016; BuildingObjects/ISUI/ISInventoryBuildMenu.lua:41 | 14 |
| `getText("ContextMenu_KillAnimal")`, `animal:getFullName()` | ISAnimalContextMenu.lua:310, :140 | 14 |
| `ISWorldObjectContextMenu.setTest()`, `.Test` | ISInventoryBuildMenu.lua:81; ISHutchMenu.lua:4 | 14 |
| `ISTimedActionQueue.clear/add`, `luautils.walkAdj(p, sq[, true])`, `ISWorldObjectContextMenu.equip/transferIfNeeded` | ISWorldObjectContextMenu.lua:1056, :2564, :2609; ISAnimalContextMenu.lua:90-94, :577; shared/luautils.lua:119 | 14 |
| `o:getSquare()`, `sq:isOutside()`, `p:getVehicle()`, `p:getPrimaryHandItem()` | ISWorldObjectContextMenu.lua:2571; Foraging/ISZoneDisplay.lua:400; ISHutchMenu.lua:8; ISAnimalContextMenu.lua:93 | 14 |
| `getCell():getObjectListForLua()`, `size/get`, `instanceof(o,"IsoAnimal")`, `getAnimalType()` | DebugUIs/Scenarios/FenrisScenario.lua:505; ISAddAnimalInTrailer.lua:29; ISAnimalUI.lua:65 | 15, 16 |
| `isoToScreenX/Y(0, x, y, z)`, `getX()` | Fishing/TensionUI.lua:11-12; TimedActions/ISContextualActions.lua:100 | 15 |
| `drawTextCentre`, `drawRect`, `drawRectBorder`, `getTextManager():getFontHeight(UIFont.Small)` | ISUIElement.lua:1280, :1191, :1219; ISAnimalUI.lua:4 | 15 |
| `ISPanel:derive/new`, `initialise`, `noBackground`, `addToUIManager`, `removeFromUIManager`; 1x1-Element | ISAnimalContextMenu.lua:746-747; ISPanel.lua:9; ISUIElement.lua:1373; ISButtonPrompt.lua:1244 | 15 |
| Bench: `p:Say`, `getCurrentSquare`, `getCell():getGridSquare`, `inv:AddItem("Base.X")`, `animal:setHealth(0)` | Entity/ISEntityUI.lua:458; ISWorldObjectContextMenu.lua:112; server/Animal/ISPickDungCursor.lua:104; Tests/RecipeTests.lua:317; ISKillAnimal.lua:58 | 16 (nie kopiert) |

Nur ueber den Kern (nicht selbst gerufen): `B.T` (getText/getTextOrNull), `B.ViewOf` (getModData/getOnlineID), `B.NearForest`,
`B.FoodList`/`B.FoodClass`/`B.IsBaitFood`, `B.Ask` (sendClientCommand). Kein Aufruf aus dem Jar allein, kein pcall, nichts aus FE 0.8.

## 3. Texte (Schluessel je Sprache, von `texte_pruefen.py` gezaehlt)

| Sprache | UI.json | Sandbox.json | IG_UI.json |
|---|---|---|---|
| EN | 74 | 44 | 6 (3 neu + 3 alte Test-Namen; `IGUI_Breed_brown` war schon da, wortgleich "Brown") |
| PTBR / RU / KO / ES / CN / FR | je 74 | je 44 | je 3 |

- 74 = genau die Liste aus Plan 6.2.8; jeder im Code benutzte `UI_BN_Bear_*`-Schluessel (Kern UND Oberflaeche, 74) steht darin;
  `B.UI.EN` (englische Ersatztexte im Code) ist wortgleich mit EN/UI.json.
- Sandbox.json = `Sandbox_BanditsNPC` ("NPC Crew", in allen sieben) + 19 x Name + 19 x Tooltip + 5 Stufen von `BearCubForestRate`.
- Platzhalter (`%1`, `%2`, `%%`) in allen Sprachen gleich; Prozent als `%%` (Vanilla-Form, z. B. EN `Sandbox_ZombieRespawnPercent_option1`).
- CN: 296 verschiedene Nicht-ASCII-Zeichen, alle in Vanilla-CN (`media/lua/shared/Translate/CN/*`) belegt. Die vollbreiten Zeichen
  `（）：；` kommen in Vanilla-CN NICHT vor und wurden durch ASCII `( ) : ;` ersetzt.
- Keine Schluessel/EN-Texte mit spawn/debug/bench/cheat/test; EN ohne "single player"/"multi player".
- Richtungen `Dir_*` sind fuer `Note_Heard` gebaut (RU im Praepositiv, FR mit Praeposition) -- schnittstelle_aenderungen.md Eintrag 2.

## 4. Pruefer-Ausgaben (alle auf die 7 Lua-Dateien der Oberflaeche)

- `luacheck.py`: `7 file(s) checked, 0 failed`.
- `scopecheck.py`: `7 file(s), 0 violation(s)`.
- `localcount.py` (aktiv / insgesamt): hoechstens 39 aktiv (Bench `NCBear_CubClean`), 41 insgesamt (Balken `rebuild`); in den
  kopierten Dateien hoechstens 30 aktiv / 41 insgesamt (`BanditsNPCBearHud.lua` rebuild), Hauptbloecke <= 22. Grenze 200, weit darunter.
- `luacheck_pz.py`: 11 Treffer W113, alle erklaert: 3 x die Aktionsklassen (globale Klassen aus shared/TimedActions, der Pruefer kennt nur
  Namen, die NPC Crew setzt), 5 x `NCBear_Cub*` (setzt die Bench-Datei selbst), 3 x `NCBearMenu` (setzt die Test-Mod). Mit `--unused`
  zusaetzlich 3 x W212 `self` in den Maus-Funktionen des Balkens (Absicht) und 1 x W212 `player` im Bench-Menue.
- `texte_pruefen.py`: `FEHLER gesamt: 0` (Hinweise: 6 x Ereignis-Parameter `test` -- Vanillas Signatur, kein Testname).
- Zeilenenden/Form (in `texte_pruefen.py`): alle 7 Lua-Dateien und sandbox-options.txt reines ASCII, LF, kein BOM, keine Zeile mit `\`
  am Ende, kein `next(`, kein `%a`. JSON: UTF-8 ohne BOM, LF, Round-Trip exakt.
- `belege.py`: `abweichend: 0 von 112`.
- Attrappe `run.lua`: mit Kern-Attrappe `113 ok, 0 Fehler`; mit den echten shared-Dateien des Kerns `114 ok, 0 Fehler`.
  Geprueft: jede Note-Art (wait in Stunden/Minuten, days, dir, num ohne ".0", name, ohne t, fremde/kaputte), Tone, `%%`; Hello beim
  Start, Drossel 10 s, Ende nach erster Sicht, MP per sendClientCommand; Tier-Menue gegen Kontext-Attrappe ("Kill" am Jungen weg, am
  Hirsch bleibt; Fuettern frei/grau mit Grund und Restzeit; Streicheln grau "zu scheu"; fremd gebunden; unbekanntes Junges frei + Hello;
  kein Futter grau; Probelauf baut nichts; zwei gleichnamige Junge); Klick = Futter zuerst in die Hand, dann Aktion; Welt-Menue Koeder
  (Wald frei, nur Honig/Fisch, Stadt ohne/mit Honig in der Hand, drinnen grau, zweiter Platz grau, Aufgeben in 3 Kacheln -> BaitDrop);
  Zeitaktionen (jeder Ausgang stop/forceStop/perform loest Sperre, Variable, Ton; complete ruft genau den Kern; ohne Kern false; Haltung
  lamb mit fester Groesse, Rueckfall loot); Balken (1x1, Maus durch, 6 Zeichenaufrufe je Balken, kein Suchlauf je Bild, Texte, Restzeiten,
  5 s "Tamed!", Reichweite, Koeder-Schild, geteilter Bildschirm); Bench im MP "singleplayer only", CubLog, CubSet mit Typpruefung.

## 5. Nicht gebaut, offen, ungeprueft

- **Ungespielt, alles.** Laufzeit-Behauptungen sind Vermutungen. Besonders: erscheint `OnClickedAnimalForContext` fuer `ncbearcub`
  (Plan 11); sieht die Streichel-Haltung `"lamb"` beim kleinen Jungen gut aus (sonst `NCBear_CubSet("petAnim", "loot")`); steht der Balken
  bei `barZ = 0.55` an der richtigen Hoehe; blinkt "Tamed!" lesbar; wird `%%` in `getText` ohne Einsetzung zu `%` (Vanilla verlaesst sich
  darauf, z. B. `ContextMenu_FullPercent`, ISWorldObjectContextMenu.lua:364 -- ungeprueft im Spiel).
- **MP ungeprueft:** baut der Server die Zeitaktion aus den uebertragenen Feldern neu (Plan FE 8.2); kommt "Sync" an; OnlineID-Zuordnung
  des Balkens nach Neuladen. Fress-Animation `NCBearAct` nur beim Fuetternden (ehrliche Grenze, Plan 5.3).
- **Fuettern in MP:** `ISWorldObjectContextMenu.equip` stellt eine Vanilla-Ausruest-Aktion vor die Fuetter-Aktion; geprueft nur in der Attrappe.
- Sandbox-Texte nennen in den Stufen feste Prozente (2/5/12/30) -- stimmen nur, solange `B.CFG.forestRate` so bleibt.
- `Menu_BaitTip` sagt "one to three nights" -- bei einem anderen `BearBaitNights` stimmt der Tooltip nicht mehr (Plan-Text woertlich).
- Uebersetzungen von mir, nicht von Muttersprachlern gegengelesen. KO `Hud_Other` "%1 님을 믿음" setzt den Benutzernamen ein.
- NICHT Sache der OBERFLAECHE (Zusammenbau): Platzhalter-Modell/-Textur kopieren, Gesamt-Attrappe (`attrappe/gesamt/`),
  Uebernahme-Skript und NAEHTE.md, Erlaubt-Liste fuer die drei globalen Aktionsklassen und `test`-Parameter.

## 6. Schnittstelle

Keine Abweichung von Plan 6.2. Eintraege in `schnittstelle_aenderungen.md`: OBERFLAECHE 1 (Unterraum `B.UI`), OBERFLAECHE 2 (Dir-Texte nur
fuer `Note_Heard`; Bench prueft zuerst den Modus). Die Zusaetze des KERNs (Eintrag 1) sind gelesen und vertraeglich: `B.CheckBait(me)`
ohne `now`, `B.Touch()` ohne Argumente, Kurzgruende von `B.AppearFor` in der Bench als Text.
