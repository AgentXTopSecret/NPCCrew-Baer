# Lauf baer-b1b: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 11.11.2026. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (42 Dateien laut
`staging_dateien.txt`, B1a + Fix 1-3 + B1b KERN + OBERFLAECHE + Zusammenbau). Ich habe KEINE Datei im Staging, in der Test-Mod, in NPC Crew,
Vanilla oder Bandits geaendert; geschrieben nur dieser Bericht und Hilfsdateien im Scratch-Ordner (eigene Pruefskripte, Diffs, die Probe).
Kein git, kein Spielstart, kein Download. Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/` (42.22.2),
`BD:` = Bandits 42.22/common, `NC:` = NPC Crew `42/media/lua/`.

## 0. Ergebnis

**Kein Blocker. 1 major, 7 minor.** Alle Zahlen der Bauer-Berichte habe ich selbst nachgefahren und bestaetigt (Tabelle 1). Der Kern der
Befunde: `string.byte` (Namenspruefung) hat keinen Vanilla-/Bandits-Aufruf (A1); "nur druckbare Zeichen" ist nicht ganz erfuellt (A2);
Zeile 2 des Schilds kann mit Vanilla-Schriften nicht kleiner werden -- das ist statisch entscheidbar, nicht "ungeprueft" (A3); ein
Kommentar-Beleg zeigt auf auskommentierten Vanilla-Code (A4); die neue Cheat-Regel `force` ist leicht zu umgehen (A5); B1b weitet den
offenen MP-Punkt A3 aus und rechnet ausdruecklich mit dem pcall (A6); im MP ueberlebt "following" kein Neuladen (A7, Auftragsabweichung);
Kevins Zaehm-Dauer vom 11.11. steht noch nicht im Staging (A8, nicht B1b-Umfang, aber "vor dem Einbau").

## 1. Selbst laufen lassen (Zahlen)

| Pruefung | Ergebnis (mein Lauf 11.11.) | deckt sich mit Bauer/Zusammenbau |
|---|---|---|
| `luacheck.py` auf alle 17 Lua des Stagings (16 kopierte + Bench) | `17 file(s) checked, 0 failed` | ja |
| `scopecheck.py` (17) | `17 file(s), 0 violation(s)` | ja |
| `localcount.py` (17) | hoechstens 39 aktiv (Bench `:319`), kopiert hoechstens 36 aktiv (`S:client/ISUI/BanditsNPCBearHud.lua:219`); insgesamt hoechstens 54 deklariert (`S:server/BanditsNPCBearWorld.lua:353`, `B.ScanAnimals`) -- weit unter 180/200 | ja (KERN-Bericht nennt 29 aktiv fuer World:353, mein Lauf 28 -- unerheblich) |
| `luacheck_pz.py` (17) | 14 x W113, alle erwartet: 3 Aktionsklassen `S:client/BanditsNPCBearMenu.lua:84/95/105`, 11 in der Bench | ja |
| `luacheck_pz.py --unused` (ohne Bench) | zusaetzlich 3 x W212 `self` (Hud `:394-396`), `Rules.lua:41` W311, `Rules.lua:160` W212 -- alle B1a | ja |
| Dateiform (eigenes Skript, 42 Dateien) | alle LF, kein BOM, Zeilenende am Schluss, Lua und `.txt` reines ASCII: 0 Probleme | ja |
| `attrappe/kern/run.lua` | 133 bestanden, 0 Fehler (byte-gleich mit `kern/ergebnis.txt`) | ja |
| `attrappe/b1b_kern/run.lua` | 145 bestanden, 0 Fehler; nur die drei erwarteten `***`-Zeilen aus 6b (byte-gleich mit `ergebnis.txt`) | ja |
| `attrappe/gesamt/run.lua` | **483 bestanden, 0 Fehler**, keine `***`-Zeile (byte-gleich mit `gesamt/ergebnis.txt`) | ja |
| dieselbe gegen MEINE Probe (`<scratch>/probe_a/NPCCrew/42/media/lua/`) | 483 / 0, byte-gleich mit `gesamt/ergebnis_probe.txt` | ja |
| `attrappe/pruef_b/run.lua` | byte-gleich mit `pruef_b/ergebnis_nach.txt` (BEFUND 2a ist der bekannte B1a-Punkt) | ja |
| `attrappe/ober/run.lua` ohne / mit `kern` | 116 ok, 0 Fehler / 117 ok, 0 Fehler | ja |
| `attrappe/b1b_ober/run.lua` ohne / mit `kern` | 141 ok, 0 Fehler / 131 ok, 0 Fehler | ja |
| `gesamt/xref_b1b.py` | 0 Luecken, 0 Hinweise | ja |
| `ober/texte_pruefen.py`, `b1b_ober/texte_pruefen_b1b.py` | je FEHLER gesamt: 0 | ja |
| `ober/belege.py`, `b1b_ober/belege_b1b.py` | abweichend 0 von 112, 0 von 51 | ja |
| Uebernahme Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten, 1 GLB-Clip-Warnung, 1 NPC-Crew-Kommentar `NC:shared/BanditsNPC.lua:1357`); 16 Lua, Cheat-Funde 0, Tier-Regeln je an ihrem Ort, "Texte aus der Lua: 86 benutzt, fehlen in EN: 0; Ersatztexte 94, wortgleich: ja", Kollisionen 0; wuerde 42 Dateien schreiben | ja |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere | ja |
| **Probe** (eigene, nach `<scratch>/probe_a`, nicht ins Arbeitsverzeichnis) | **OK -- 0 Fehler, 26 Warnungen**, 42 Dateien geschrieben; luacheck/scopecheck/localcount je kopierter Datei ok; luacheck_pz 0 Treffer + 3 erlaubt | ja |
| Texte in der Probe (zusammengefuehrt) | je Sprache UI.json 3895, Sandbox.json 137, IG_UI.json 3; alle 21 Round-Trip und sortiert; `sandbox-options.txt` 62 Optionen (42 NPC Crew + 20) | ja |
| `staging_dateien.txt` gegen Platte und Test-Mod | 42/42 Zeilen: MD5, Bytes und neu/ueberschreibt/gleich stimmen (2 / 26 / 14), keine Datei im Staging ausserhalb der Liste | ja |
| eigener Text-Pruefer (7 Sprachen) | UI 94, Sandbox 46, IG_UI 3 (EN 6 mit den 3 Altlasten); gleiche Schluessel, gleiche Platzhalter, sortiert, Round-Trip, kein BOM/CR, kein `<`/`>` in irgendeinem Text (auch Sandbox), CN: 0 Zeichen ausserhalb Vanilla-CN; `U.EN` 94 == EN/UI.json wortgleich; neu genau die 20 Plan-Schluessel + 2 Sandbox, geaendert nur `Note_Tamed`; Kollision mit NC nur `Sandbox_BanditsNPC` (gleicher Wert "NPC Crew", vom Skript erlaubt) | ja |
| eigener Methoden-Abgleich (jede `:methode(` der neuen/geaenderten Codezeilen gegen V+BD) | 32 Methodennamen, jeder mit Vanilla-/Bandits-Aufruf; Grundbibliothek: `string.len` 23, `string.sub` 86, `table.sort` 116, `math.sqrt` 17 Vanilla-Aufrufe -- **`string.byte` 0** (A1) | neu |
| eigener Kommentar-Beleg-Abgleich (jede `pfad.lua:zeile` in allen 17 Staging-Lua) | 191 Fundstellen; 1 zeigt in einen `--[[ ]]`-Block (A4); 2 zeigen absichtlich auf einen erklaerenden Kommentar (`S:client/BanditsNPCBearClient.lua:269/:310` -> `V:client/ServerCommands.lua:210`, ok) | neu |

Fix 2 (`tHas` in `B.T`, `S:shared/BanditsNPCBear.lua:255-266`) und Fix 3 (`petting = { name = "PetAnimalCalf" }`
`S:shared/BanditsNPCBearDefs.lua:60`, `playBreedSound("petting")` / `stopOrTriggerSound` in `S:shared/TimedActions/BanditsNPCBearPetAction.lua`,
Form `V:shared/TimedActions/Animals/ISPickupAnimal.lua:23/:27/:33` nachgelesen) sind unveraendert drin. Streicheln (Haltung, Abstand) unberuehrt.

## 2. Belege der in B1b neuen Engine-Aufrufe (selbst in den heutigen Dateien gelesen)

| Aufruf (Typen) | Ort im Staging | Fundstelle (gelesen) | Urteil |
|---|---|---|---|
| `player:getVehicle()` (IsoPlayer, Server) | `S:server/BanditsNPCBearFollow.lua:205`, `S:server/BanditsNPCBearWorld.lua:44` | `V:server/Vehicles/VehicleCommands.lua:11` `local vehicle = player:getVehicle()` | ok (fuer FREMDE Spieler am Server Jar-Lesart, KERN 7.4 ehrlich genannt) |
| `p:getVehicle()` (SP, Client-Menue, Bench) | World `:55`, Menu `addMode`, Bench | `V:client/ISUI/Hutch/ISHutchMenu.lua:8` `if playerObj:getVehicle() then return false end` | ok |
| `animal:getModData()` schreiben/lesen | `S:server/BanditsNPCBearRegistry.lua:197-198`, `S:server/BanditsNPCBearServer.lua:671` | `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127`, `V:shared/Definitions/animal/ButcheringUtil.lua:596` | ok (gleiche Form wie B1a `B.Commit`) |
| `getTimestampMs()` | Follow `:173`, World `:461` | `V:server/Foraging/forageServer.lua:456` | ok |
| `player:getX()/getY()` (Server) | Follow `:209` | `BD:42.22/media/lua/server/BanditServerSpawner.lua:179` | ok |
| `animal:getX()/getY()` | Follow `:124/:209`, World `dropOrphan` | `V:shared/Definitions/animal/ButcheringUtil.lua:575-577` | ok |
| `if isClient() then return end` | Follow `:1` | `V:server/Traps/STrapSystem.lua:1` | ok |
| `ISWorldObjectContextMenu.equip(p, p:getPrimaryHandItem(), food, true, false)` | `S:client/BanditsNPCBearMenu.lua` `onHold` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:93` (gleiche Argumente, Futter als InventoryItem); Funktion `V:client/ISUI/ISWorldObjectContextMenu.lua:2594-2622` | ok; Vanillas Locken nicht benutzt (grep 0) |
| `ISContextMenu:getNew(context)`, `context:addSubMenu(opt, sub)` | Menu `addHold` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:48/:49` | ok |
| `ISTextBox:new(0,0,280,180, Titel, Vorgabe, Ziel, Rueckruf, Spielernr, param1)` | `S:client/ISUI/BanditsNPCBearNameBox.lua:62` | Signatur `V:client/ISUI/ISTextBox.lua:280`; Form mit Spielernr + param1 `V:client/ISUI/ISInventoryPage.lua:1912`; 280 x 180 `V:client/ISUI/Animal/ISAnimalUI.lua:460` | ok |
| `:initialise()`, `:addToUIManager()`, `.maxChars`, Joypad (`getJoypadFocus`, `centerOnScreen`, `setJoypadFocus`) | NameBox `:63-74` | `V:client/ISUI/Animal/ISAnimalUI.lua:461-468` | ok |
| `.noEmpty`, `:setValidateFunction`, `:setValidateTooltipText` | NameBox `:66-68` | Wirkung `V:client/ISUI/ISTextBox.lua:111-119, :174, :178-185`; Aufrufe `V:client/ISUI/Maps/ISWorldMapSymbols.lua:203`, `V:client/OptionScreens/CharacterCreationProfession.lua:1297` | ok (Lua-Seite von Vanilla; Ziel nil statt Tabelle ist reines Lua) |
| `entry:setMaxTextLength(n)` | NameBox `:69` | `V:client/ISUI/ISMPEditAccount.lua:19`; Feld entsteht `V:client/ISUI/ISTextBox.lua:20`, `:instantiate()` dort `:23` | ok |
| Rueckruf `onclick(target, button, param1)`, `button.internal`, `button.parent.entry:getText()` | NameBox `:39-45` | `V:client/ISUI/ISTextBox.lua:134`; `V:client/ISUI/Animal/ISAnimalUI.lua:471-473` | ok |
| `playerObj:getPlayerNum()` | NameBox `:59` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1069` | ok |
| `getSpecificPlayer(0):getDescriptor():getForename()` | `S:client/BanditsNPCBearClient.lua` `U.LocalName` | `V:client/Farming/CFarmingSystem.lua:45`, `V:client/XpSystem/ISUI/ISCharacterScreen.lua:84` | ok |
| `getTextManager():getFontHeight(UIFont.NewSmall)`, `drawTextCentre(..., UIFont.NewSmall)` | Hud `:411`, `drawTag` | `V:client/Entity/ISUI/Controls/ISWidgetTitleHeader.lua:4`, `V:client/Foraging/ISSearchManager.lua:148` | ok (aber A3) |
| `string.byte(text, i)` | `S:shared/BanditsNPCBearRules.lua:345/:346/:352` | **kein Aufruf in V und BD** | **A1** |
| `string.len`, `string.sub`, `table.sort`, `math.sqrt` | Rules, Follow `:226`, Hud `U.CubsNear` | je viele Vanilla-Aufrufe (z. B. `V:client/DebugUIs/BrushTool/BrushToolChooseTileUI.lua:440` `string.len(name)`) | ok |

Nicht benutzt (grep ueber die 16 kopierten Dateien, nur Kommentare): `pathToLocation`, `setVariable("animalRunning"`, `setCustomName`/
`getCustomName`, `ContextMenu_Lure`/`eatFromLured`/`tryLure`, `next(`, `%a`, `string.trim`; kein neues `pcall`. Jar-only ausser
`string.byte`: keiner gefunden.

## 3. Befunde

### A1 (major) -- `string.byte` ohne Vanilla-/Bandits-Aufruf (eiserne Regel)
- **Wo:** `S:shared/BanditsNPCBearRules.lua:345`, `:346`, `:352` (`B.CleanName`; laeuft beim Schreiber UND jedes Bild im Namensfenster).
- **Beleg:** grep `string.byte(` und `:byte(` in `V:` (42.22.2) und `BD:42.22` + `BD:common`: **0 Treffer**. Vorhanden ist es nur im Jar
  (Kahluas `se/krka/kahlua/stdlib/StringLib`: Name "byte" in `names[2]` -> `stringByte`, das `String.charAt` liefert -- javap von mir
  gelesen) und in NPC Crews gespieltem Code (`NC:client/BanditsNPCLootList.lua:225`, `NC:client/ISUI/BanditsNPCWorkPlanWindow.lua:103`,
  NC belegt es dort selbst nur mit sich selbst, `NC:client/BanditsNPCLootList.lua:114`). Die Forschung sah das (`forschung_b1b.md:219`
  "Vanilla nutzt es nicht (grep 0)") und erklaerte es zur "Lua-Grundbibliothek, kein Engine-Aufruf"; `PLAN_B1B.md:511` und
  `bau_b1b_kern.md:104` schreiben daraus "Jar-only-Aufrufe in B1b: keiner". Die Werkstatt-Regel (CLAUDE.md 3) und NPC Crews eigener
  Pruefer sehen das anders: `luacheck_pz.py` erlaubt die Standardbibliothek "NICHT pauschal" -- ein Name, den Vanilla/Bandits nie
  benutzen, ist ein Verdaechtiger (Kahlua ist kein echtes 5.1). luacheck_pz meldet es nur deshalb nicht, weil es das Feld `string.byte`
  nicht ansieht (nur das Global `string`). Laufzeitrisiko niedrig (Jar + NPC Crew gespielt), Regelfrage offen.
- **Nebenbei (ungeprueft):** NPC Crews `utf8Chars` (`WorkPlanWindow.lua:100-108`) nimmt UTF-8-Bytes an, B1b und der Jar sagen
  Zeichencodes (`charAt`). Fuer `B.CleanName` ist das Ergebnis in beiden Faellen gleich (in einer UTF-8-Folge kommt kein Byte < 32, 37, 60,
  62 oder 127 vor); nur `nameMax` 24 waeren dann 24 Bytes statt 24 Zeichen.
- **Vorschlag:** ohne `string.byte` bauen, nur mit belegten Mitteln: `string.find(clean, "<", 1, true)` / `">"` / `"%"` (Form
  `V:client/OptionScreens/LoadGameScreen.lua:601` `string.find(..., text, 1, true)`), Steuerzeichen ueber `string.sub(clean, k, k)` und
  Vergleich mit `" "` bzw. `"\127"`; Rand-Leerzeichen mit `string.trim` (`V:client/ISUI/ISTextBox.lua:182`,
  `V:client/DebugUIs/AnimationClipViewer.lua:571` -- der Plan hat das belegte `string.trim` ausdruecklich gemieden und dafuer das unbelegte
  `string.byte` genommen). Oder Kevins Wort fuer `string.byte(String, Zahl)` (Jar-Beleg StringLib + NPC Crew gespielt) einholen und im
  Kommentar nennen. Danach Attrappen 8.1.5 / 17e erneut.

### A2 (minor) -- "nur druckbare Zeichen" nicht ganz erfuellt
- **Wo:** `S:shared/BanditsNPCBearRules.lua:351-354` (lehnt nur < 32, 127, `<`, `>`, `%` ab; Rand-Abschnitt nur Byte 32, `:345-346`).
- **Beleg:** Laut Jar liefert `string.byte` den Java-Zeichencode (A1). Damit gehen durch: C1-Steuerzeichen U+0080-U+009F,
  Format-/Richtungszeichen U+200B-U+200F, U+202A-U+202E (Rechts-nach-links-Umkehr), U+2066-U+2069, U+FEFF, und Namen nur aus
  NBSP U+00A0 bzw. U+3000 (sichtbar leer, `noEmpty` greift dort nicht: Vanilla prueft mit `string.trim`). Im MP kann ein gebastelter
  `Rename` (der Server prueft mit derselben Regel, `S:server/BanditsNPCBearFollow.lua:234`) so einen Namen setzen, den alle in 60 Kacheln
  im Schild sehen (harmlos, aber gegen den Auftrag 3 "nur druckbare Zeichen"). Ungespielt.
- **Vorschlag:** zusaetzlich 128-159 und die genannten Bereiche ablehnen und U+00A0/U+3000 wie Leerzeichen behandeln (eine kleine
  Bereichsliste in `B.CleanName`, Client und Server nutzen sie ohnehin gemeinsam); Faelle in `b1b_kern` 5 ergaenzen.

### A3 (minor) -- Zeile 2 des Schilds wird nie kleiner; "ungeprueft" ist statisch entscheidbar
- **Wo:** `S:client/ISUI/BanditsNPCBearHud.lua:407-418` (NewSmall nur, wenn niedriger als Small); Berichte `bau_b1b_oberflaeche.md:178`,
  `bau_b1b_zusammenbau.md:176` ("ob UIFont.NewSmall kleiner ist: ungeprueft").
- **Beleg:** Vanilla `media/fonts/<L>/fonts.txt`: `font NewSmall` und `font Small` laden in JEDER Sprache dieselbe Datei
  (EN/PL `zomboidSmall.fnt`, RU `zomboidSmallCyrillic.fnt`, CN/CH `zomboidSmallChinese.fnt`, KO `zomboidSmallKorean.fnt`, JP `...Japanese`;
  EN `fonts.txt:75-79` und `:93-97`; Legasthenie-Satz ebenso). Also gleiche Hoehe -> der Code nimmt immer `Small`; Zeile 2 ist nur grauer,
  nicht klein (Auftrag 2: "Zeile 2 klein"). Ein kleineres Zeichnen gaebe es nur ueber `ISUIElement:drawTextZoomed` (`V:client/ISUI/ISUIElement.lua:1260`) --
  davon gibt es in Vanilla nur die Definition, keinen Aufruf (waere eine Ausnahme mit Kevins Wort).
- **Vorschlag:** Kevin ehrlich sagen "Zeile 2 ist gleich gross, nur blasser" (oder fragen, ob ihm das reicht); den toten NewSmall-Zweig
  entweder lassen (schadet nicht) oder entfernen; die Berichte von "ungeprueft" auf "statisch: nicht kleiner" stellen.

### A4 (minor) -- Kommentar-Beleg zeigt auf auskommentierten Vanilla-Code
- **Wo:** `S:server/BanditsNPCBearWorld.lua:29` ("isDead am Spieler: server/Seasons/season.lua:127", B1a-Zeile, steht direkt ueber der
  neuen B1b-Beschreibung von `car`); ebenso nennt `bau_b1b_kern.md:92` `V:server/Seasons/season.lua:139` als Beleg fuer `getVehicle`.
- **Beleg:** `V:server/Seasons/season.lua:1` "TODO NOTE: disabled this class"; die Zeilen 127 und 139 liegen im Block `--[[` (`:120`) bis
  `--]]` (`:145`), dort zudem `if isServer() then return end` -- kein echter Aufruf. `belege.py` sieht das nicht (prueft nur, ob der Text in
  der Zeile steht). Mein Abgleich aller 191 Fundstellen der Staging-Kommentare: nur diese eine liegt in einem Kommentarblock.
- **Vorschlag:** Beleg tauschen, z. B. `playerObj:isDead()` `V:server/ISObjectClickHandler.lua:187`; `season.lua:139` aus dem Bericht
  streichen (`VehicleCommands.lua:11` und `ISHutchMenu.lua:8` reichen). `belege.py` koennte Kommentarzeilen/-bloecke als Fehler melden.

### A5 (minor) -- Neue Cheat-Regel `force` im Uebernahme-Skript ist leicht zu umgehen
- **Wo:** `baer/tools/baer_uebernahme.py:184-185`, Muster `(?<!function )\bB\.ScanAnimals\s*\([^)\n]*,\s*(?!nil\b)[\w.\"']+\s*\)`.
- **Beleg (eigene Regex-Probe):** trifft `B.ScanAnimals(players, true)` und `(nil, true)`, aber NICHT `B.ScanAnimals(B.Players(), true)`
  (die innere Klammer beendet `[^)\n]*` -- und genau so holt der Kern seine Spieler), nicht `(players, not false)`, `(players, 1 == 1)`
  und nicht einen Aufruf ueber einen lokalen Namen (`local scan = B.ScanAnimals`). Heute ist der kopierte Code sauber (Funde 0, alle
  Aufrufe einargumentig, `S:server/BanditsNPCBearServer.lua:869/:903`), die Regel schuetzt aber spaetere Aenderungen schlecht.
- **Vorschlag:** jeden `B.ScanAnimals(`-Aufruf im kopierten Code mit den schon vorhandenen Klammer-Mustern (`_TL2`) zerlegen und mehr als
  ein Argument auf oberster Ebene als Fund werten; zusaetzlich `ScanAnimals` ohne folgende `(` (Zuweisung an einen Namen) melden.

### A6 (minor) -- B1b weitet den offenen MP-Punkt A3 aus und rechnet dabei mit dem pcall
- **Wo:** `S:server/BanditsNPCBearServer.lua:898-904` (neuer eigener Waisen-Suchlauf), Kommentar `:899-900`; pcall `:916`; dagegen
  `:576` "pcall um EIGENEN Code (alle Engine-Aufrufe darin sind belegt, keine Tarnkappe)".
- **Beleg:** Vor B1b lief `getCell():getObjectListForLua()` am Server nur bei vermissten Eintraegen (`:865`). Jetzt laeuft der Suchlauf je
  120 s auf JEDEM Schreiber, auch ganz ohne Junges (`orphanScanMs`, `S:shared/BanditsNPCBear.lua:74`), und der neue Kommentar sagt selbst:
  `getObjectListForLua` am Server unbelegt (A3, `S:server/BanditsNPCBearWorld.lua:280`) -- ein Engine-Fehler dort "kostet dann nur diesen
  Suchlauf". Das ist genau die Lage, die CLAUDE.md 3 meint ("ein pcall um einen unbelegten Aufruf ist eine Tarnkappe"); gemildert, weil der
  Fehler laut bleibt (`B.ErrEvery`, eine Zeile je 60 s). Die zwei Kommentare widersprechen sich.
- **Vorschlag:** Kommentar `:576` richtigstellen (MP-Ausnahme A3 nennen); den Punkt in Kevins MP-Test ausdruecklich machen ("Server 3 min
  ohne Junges laufen lassen, Log auf `brain tick:` pruefen", PLAN_B1B 8.4 MP 7 erweitern); wahlweise im MP den eigenen Suchlauf nur
  laufen lassen, wenn es Eintraege gibt oder ein `B.AppearFor` scheiterte (Waisen entstehen nur so), bis A3 im MP gespielt ist.

### A7 (minor) -- Auftragsabweichung: im MP ueberlebt "following" kein Neuladen und kein Abmelden
- **Wo:** `S:shared/BanditsNPCBearRules.lua:377` (Regel 10: kein Besitzer -> "stay"), `S:server/BanditsNPCBearFollow.lua:127-129`;
  Plan 1.5/1.6 (gewollt).
- **Beleg:** Auftrag 1: "Zustand ueberlebt Speichern/Laden und gilt im SP und im MP". Im SP stimmt das (Attrappe 17f). Im MP setzt der
  erste Takt nach einem Server-Neustart (Besitzer noch nicht verbunden) und jedes Abmelden das Junge still auf "staying"; Plan 8.4 MP 5/6
  erwartet das so. Die Abweichung steht im Plan, aber nicht unter den Fragen an Kevin (Plan 10).
- **Vorschlag:** Kevin als Frage vorlegen ("im MP nach Abmelden/Neustart wieder auf Folgen schalten -- ok?"); Alternative ohne
  Engine-Neues: bei `o == nil` nur halten statt `B.SetMode`, solange der Besitzer offline ist (Zustand bleibt "following").

### A8 (minor, nicht B1b-Umfang) -- Kevins Zaehm-Dauer vom 11.11. steht noch nicht im Staging
- **Wo:** `S:shared/BanditsNPCBear.lua:88-89` (`BearTameFeedPoints` def 14, `BearTamePetPoints` def 8), `S:../sandbox-options.txt`
  default 14 / 8.
- **Beleg:** `baer/STAND.md:23-25` "OFFEN NACH B1b (vor dem Einbau erledigen)": 14 -> 4 und 8 -> 3 (`ENTSCHEIDUNGEN.md:192`, Kevin
  *"nein nein ich will das streicheln und fuettern immer noch so oft geht nur es soll laenger dauern"*). Der verworfene Vorschlag
  (180 min / 5 Fuetterungen) ist richtigerweise NICHT drin (`:92-94` 3 / 120 / 60).
- **Vorschlag:** der Integrator zieht es vor dem Einbau nach (B.OPTS UND sandbox-options.txt, Tooltips mit Zahlen, Attrappen-Erwartungen)
  oder sagt Kevin, dass der Einbau es noch nicht hat.

## 4. Ohne Befund geprueft

- **Trennung:** alle fuenf neuen Testbefehle (`NCBear_CubFollow`, `_CubName`, `_CubFollowTest`, `_CubOrphan`, `_CubSweep`) und die drei
  Rechtsklick-Eintraege nur in `S:client/NCBearBenchCub.lua`, jeder hinter `ready()` (`:52-70`, zuerst `B.IsSP()`, im MP "singleplayer
  only"); in den 16 kopierten Dateien kein `NCBear_`, `bench`, `cheat`, `spawn`, `debug` ausser Fundstellen-Pfaden in Kommentaren;
  `B.CreateCub` im Spielcode nur aus `B.AppearFor`, `:remove()`/`removeAnimal` nur in `B.RemoveCub` (Trockenlauf). Die zwei
  Werkbank-Kommentare hat der Zusammenbau entfernt.
- **Namen/Kollisionen:** neue Dateien `server/BanditsNPCBearFollow.lua`, `client/ISUI/BanditsNPCBearNameBox.lua` (Muster `BanditsNPCBear*`);
  grep in `NC:` nach den Dateinamen und nach `AskName|CubsNear|HandleMode|HandleRename|FollowStep|FollowLost|FollowDecide|CleanName|
  SetMode|FollowMaxDistance|BearFollow`: 0; in V und BD weder `BanditsNPC` noch `UI_BN_`; `landkarte_index.txt`: kein Baeren-Name.
  NPC Crews Schilder `NC:client/ISUI/BanditsNPCNameTags.lua` zeichnen keine Tiere (grep `IsoAnimal|getAnimalType|isAnimal` = 0), NC setzt
  `setCustomName` nur an Gegenstaenden (`NC:shared/BanditsNPCLivestockButcher.lua:1760`) -- NAEHTE 14/16 stimmen.
- **Sandbox:** `BanditsNPC.BearFollowMaxDistance` integer 10..60, Vorgabe 40, `page = BanditsNPC`, `translation` passend; gleich in
  `B.OPTS` (`S:shared/BanditsNPCBear.lua:97`) und `sandbox-options.txt`; Name + Tooltip in allen 7 Sprachen; benutzt in
  `S:shared/BanditsNPCBearRules.lua:380` und `S:server/BanditsNPCBearFollow.lua:209`. Jede der 20 Optionen wird im kopierten Code gelesen.
- **Texte:** Dir-Satzbau je Sprache wie Plan 6.1 (KO `%1쪽에서`/`%1쪽에`, FR ohne Praeposition, weil `Dir_*` sie traegt), `Note_Tamed` nennt
  `Menu_Follow` der Sprache wortgleich, RU `Tag_Name` "Медвежонок (%1)" begruendet (schnittstelle B1b OBERFLAECHE 2), `Why_NameBad` ohne
  `<`/`>`/`%%` begruendet (Rich-Text-Tooltip, `V:client/ISUI/ISButton.lua` -> `ISToolTip`); keine Testwoerter; Menue-Texte nur ueber `U.T`.
- **SP/MP-Zweig:** SP `B.IsSP()` = `not isClient() and not isServer()` (`S:shared/BanditsNPCBear.lua:111-113`); `B.Ask` ruft im SP
  `B.Handle` direkt, `B.Tell`/`B.SendView` direkt (`:437-471`); `server/BanditsNPCBearFollow.lua` beginnt mit `if isClient() then return end`.
  Was der Server wissen muss (Besitz, Zustand, Fahrzeug, Abstand, Name), prueft `B.HandleMode`/`B.HandleRename` selbst; der Client glaubt
  nichts davon. Drossel 500 ms, Tabelle gedeckelt 64; `B._orph` gedeckelt 16; `f` feste Felder.
- **Rote Linien:** "Hold out food" nur `equip` (kein Gegenstand erzeugt/verbraucht, Attrappe 17h zaehlt); kein neuer Kick-Weg (nur eigene
  `sendClientCommand`); Folgen mit Zeitdeckeln (Laufbefehl hoechstens je 1,2 s, festgesteckt je 10 s); nur `ncbearcub` wird angefasst.
- **Kosten je Bild:** Schild 2 Umrechnungen + 4 `drawTextCentre`, keine Texte/Suche je Bild (Hud `draw`/`drawTag`); `U.CubsNear` nur auf
  Rechtsklick. Der Namens-Pruefer laeuft je Bild im offenen Fenster (Vanilla `ISTextBox:prerender` -> `updateButtons`, `:162`), auf
  hoechstens 24 Zeichen -- billig.
- **Uebernahme/Naehte:** NAEHTE.md-Zahlen (NC UI.json 3801, Sandbox.json 92, 42 Optionen) durch die Probe bestaetigt; keine neue Naht in
  einer NPC-Crew-Datei; Text-Regel `<`/`>` (`baer_uebernahme.py:627-633`) greift auf UI.json (die Sandbox-Texte enthalten ebenfalls keins).

## 5. Offen / ungeprueft (unveraendert gueltig)
Alles Laufzeitverhalten (Abstand beim Folgen, Tueren, Treppen, Schildhoehe `tagZ` 0,18, Ruckeln im MP), A3 aus B1a
(`getObjectListForLua`/`getAnimalID` am Server), `p:getVehicle()` fremder Spieler am Server (Jar-Lesart), Namen mit Nicht-ASCII-Zeichen.

Statisch geprueft, nicht gespielt.
