# Lauf baer-f1, BAUER OBERFLAECHE -- Baeren-Fenster auf V, Taste, Rechtsklick, Sitz-Treiber, Namensschild je Baer, Texte, Bench

Stand 11./12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Grundlage `PLAN_F1.md` (7.1, 7.5-7.8 woertlich), Entwurf
`f1_entwurf/`; Abweichungen stehen in `schnittstelle_aenderungen.md` Abschnitt "F1 OBERFLAECHE" (16 Punkte). Gebaut nur unter `client/`,
`Translate/`, `sandbox-options.txt` des Stagings `_arbeit/baer_zaehmen/mod/42/media/`; `shared/` und `server/` (KERN) nur gelesen.
Vor dem Bau nachgezaehlt: Staging gegen NCBearTest (Git 914ee79) **60 Dateien, alle byte-gleich** (MD5).

## 1. Ergebnis zuerst
- **V oeffnet/schliesst das Fenster des eigenen Baeren**; Taste unter Optionen -> Tastaturbelegung, Abschnitt "NPC Crew: Bear", Zeile "Bear window"
  (Vorgabe V, Vanilla speichert sie selbst in keysB42.ini). Esc oder die Taste schliesst, X oben rechts schliesst, Rechtsklick am eigenen Baeren
  "Bear window", Bench `NCBear_CubWin()`. Kein eigener Baer: Hinweis "You do not have a bear yet." ueber der Figur.
- **Das Fenster sieht aus wie der Entwurf** -- gemessen mit den echten EN-Spielschriften genau **640 x 615 px bei 1080** und **1280 x 1178 px bei
  Kevins 3840 x 2054** (Faktor 2,0, Schrift Large/Medium/Small). Bilder aus der Zeichen-Mitschrift des ECHTEN Lua-Codes:
  `f1_entwurf/fenster_gebaut_1080.png`, `f1_entwurf/fenster_gebaut_4k.png` (Skript `f1_entwurf/zeichne_gebaut.py` + `attrappe/f1_ober/zeichne_dump.lua`).
- Inhalt: Kevins Symbol 1, Name + Rename, "Bear cub - day 12" / "Bear - day 60", naechste Stufe, Zustand-Chip (folgt/bleibt/sitzt/frei/kommt/
  versteckt/faehrt mit/vermisst/ausser Reichweite), Abstand + Richtung; Leben und Ausdauer als Balken mit Zahl und Farbverlauf, Traglast,
  "Coming later: Hunger, Thirst, Tiredness, Trust" OHNE Balken; sechs Faehigkeiten mit Stufe, Prozent, 10 Segmenten und ehrlichem Tooltip;
  Befehle Follow / Stay / Sit / Roam free / Come here / Unstuck (Restzeit "Unstuck  3:12"), Schalter Passive und Name tag; aktiver Befehl
  Honig-Orange, graue Knoepfe mit Grund im Tooltip. Zwei Baeren: Pfeile "< 1 / 2 >".
- B1e-Reste: (a) "bear" statt "cub" fuer Why_Gone / Note_Dead / Menu_Hold / Menu_HoldTip in 7 Sprachen (+ U.WhyText mit bd); (b) Unstuck geht im
  Fenster auch fuer einen vermissten Baeren (C1 selbst baut der KERN); (c) A5 kein Handlungsbedarf (forschung_f1.md 6.2: UI-Bilder werden nicht
  gedeckelt, Vanilla zeigt selbst > 256 px, `V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191`); (d) C3/B7 Markierung unveraendert (Plan 4d).
- Alle Pruefer gruen (Abschnitt 5): neue Attrappe 359/359 (mit Kern-Attrappe und mit echtem Kern), alte Attrappen und `gesamt` (1672) gruen,
  85 Belege Zeile fuer Zeile bestaetigt, Texte in 7 Sprachen geprueft.

## 2. Dateien (Staging `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | neu / geaendert | Was | Zeilen | MD5 |
|---|---|---|---|---|
| `lua/client/BanditsNPCBearKey.lua` | neu | Tasten-Zeile "Bear window" (V) + Abschnitt, OnKeyPressed mit Vorfahrt, `U.WinKeyName` | 97 | 8368d85d94d21d94e2afb5bea9a96c1c |
| `lua/client/BanditsNPCBearWinData.lua` | neu | `U.WinBears`, `U.WinModel` (alle Texte, Zahlen, Knopf-Zustaende, Tooltips), `U.WinStatics` | 448 | ec4d1df8d3f43622245ffba0517baa75 |
| `lua/client/BanditsNPCBearPose.lua` | neu | Sitz-Treiber `U.PoseTick` (250 ms) / `U.PoseOnView` / `U.PosePhase` | 126 | 2db390f9dd022436f4663c473c6aa629 |
| `lua/client/BanditsNPCBearTags.lua` | neu | Namensschild je Baer: `U.TagOn` / `U.TagSet` / `U.TagLoad`, Datei `BanditsNPCBear.ini` | 104 | 9538f334d8a9bfe3ecf34b36b06a05ca |
| `lua/client/ISUI/BanditsNPCBearWinParts.lua` | neu | Farben `U.WinColor`, Verlauf `U.WinRamp`, Schrift `U.WinFonts`, Klassen `U.WinBtn` / `U.WinRow` / `U.WinTick` | 334 | 988a8766db40229497cbcb40027c2fe2 |
| `lua/client/ISUI/BanditsNPCBearWindow.lua` | neu | Fenster (ISPanel), `U.WinLayout`, Zeichnen, 1-s-Takt, `U.WinOpen/Close/Toggle/IsOpen/OnView`, Lage, Esc/Taste | 697 | 3eedddaece1c3a8fdeef8aadf02e6313 |
| `lua/client/BanditsNPCBearClient.lua` | geaendert | `U.EN` + 115 Schluessel (wortgleich EN), `U.WhyText(key, val, bd)` | | fcaa08fc61834848e914965479483af4 |
| `lua/client/BanditsNPCBearMenu.lua` | geaendert | "Bear window" am eigenen zahmen Baeren, `holdWanted`/`addHold` je Koerper (nur Modus stay), Gruende je Koerper, modeOf 4 Modi | | 7f9cdf9c4f0b2d153fb8290de8707742 |
| `lua/client/BanditsNPCBearOptions.lua` | geaendert | `WinSize` (Auto/100..300 %) nach MarkerSize | | 66dd374c21ca2d898d26bfca258c360d |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | geaendert | Zeile 2 "sitting"/"roaming", Schild je Baer (`U.TagOn`), `B.OnView` -> `U.WinOnView` + `U.PoseOnView` | | 62c154854f6d00351cc1838983da542f |
| `lua/client/NCBearBenchCub.lua` | geaendert (Testhilfe, nie kopiert) | `NCBear_CubWin`, `NCBear_CubBodyGone`, `NCBear_CubView`, `NCBear_CubStats` + Befehl/Sitzung, 2 Rechtsklick-Eintraege | | 3f6fed29bf8680eba532d5ed760ede6a |
| `lua/shared/Translate/<L>/UI.json` x 7 | geaendert | +115 `UI_BN_Bear_*` +2 Tasten-Schluessel | | EN b96be5ce..., RU 1c04c2d1..., CN 3bc71057... |
| `lua/shared/Translate/<L>/Sandbox.json` x 7 | geaendert | `Sandbox_BanditsNPC_BearRoamRadius` + `_tooltip` | | |
| `sandbox-options.txt` | geaendert | `BanditsNPC.BearRoamRadius` integer 12, 4..30 (vor BearLog), TEXTGLEICH mit `B.OPTS` des KERNs | | adc01fe4b324ebcf87186852ae14c15e |
Werkzeuge / Pruefungen (nicht im Mod): `ober_werkzeug/texte_f1.py` (Texte aller 7 Sprachen, `--basis` = Stand B1e byte-gleich),
`attrappe/f1_ober/` (`mock.lua`, `run.lua`, `texte_pruefen_f1.py`, `belege_f1.py`, `schriften_export.py` -> `schriften.lua`, `zeichne_dump.lua`),
`f1_entwurf/zeichne_gebaut.py` -> `fenster_gebaut_1080.png`, `fenster_gebaut_4k.png`. Gewollt angepasst (je mit Kommentar): `attrappe/b1b_ober`,
`b1c_ober`, `b1d_ober`, `b1e_ober` (run.lua und texte_pruefen*), `attrappe/ober/texte_pruefen.py` (Liste in schnittstelle_aenderungen.md F1 OBERFLAECHE 15).
Keine neuen Bilder (Kevins 288-px-Symbol, die Scheibe und Vanillas `media/ui/inventoryPanes/Button_Close.png` reichen).

## 3. Engine-Aufrufe mit Fundstelle (jede Zeile von `attrappe/f1_ober/belege_f1.py` gegen Vanilla gelesen: 85/85 ok)
| Aufruf (gleiche Argumenttypen) | Fundstelle | Datei bei uns |
|---|---|---|
| `table.insert(keyBinding, { value = T })`, `{ value = T, key = Keyboard.KEY_V }` | `V:shared/keyBinding.lua:6`, `:9`, `:132` | Key |
| `Events.OnKeyPressed.Add(fn)`, `getCore():isKey(Text, key)` | `V:client/ISUI/FPS.lua:20`, `:9` | Key, Window |
| `getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU / ANIMAL_RADIAL_MENU, key)` | `V:client/ISUI/ISUIHandler.lua:36`, `:37` | Key |
| `ISVehicleMenu.getVehicleToInteractWith(p)`, `AnimalContextMenu.getAnimalToInteractWith(p)` | `V:client/ISUI/ISUIHandler.lua:43`, `:44` | Key |
| `animal:isWild()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171` | Key |
| `getPlayerRadialMenu(0)`, `menu:isReallyVisible()`, `menu:undisplay()` | `ISUIHandler.lua:91-92`, `ISAnimalContextMenu.lua:1164` | Key |
| `ISChat.focused` (lesen) | `V:client/Chat/ISChat.lua:8` | Key, Window |
| `getKeyName(getCore():getKey(Text))` | `V:client/Tutorial/Tutorial1.lua:177` | Key |
| `getSpecificPlayer(0)`, `player:isDead()`, `player:getVehicle()`, `player:getX()/getY()` | `V:client/Farming/CFarmingSystem.lua:45`, `ISUIHandler.lua:42`, `V:client/ISUI/Hutch/ISHutchMenu.lua:8`, `V:client/Fishing/TensionUI.lua:11` | Key, WinData, Window |
| `getTimestampMs()` | `V:client/Foraging/ISBaseIcon.lua:485` | Key, Window, Pose |
| `ISPanel:derive(T)`, `ISPanel:new(x, y, w, h)`, `o.moveWithMouse = true` | `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1`, `:243`, `:253` (Ziehen `V:client/ISUI/ISPanel.lua:49-95`) | Window |
| `o:setWantKeyEvents(true)`, `isKeyConsumed(key)`, `onKeyRelease(key)`, `Keyboard.KEY_ESCAPE` | `V:client/ISUI/Crafting/ISHandcraftWindow.lua:386`, `:289-297` | Window |
| `ISButton:derive(T)`, geerbtes `:new` | `V:client/ISUI/ISResizeableButton.lua:1`; Aufrufer `V:client/ISUI/ISInventoryPane.lua:63` | WinParts, Window |
| `ISButton:new(x, y, w, h, "", Ziel, Rueckruf)`, `:initialise()`, `parent:addChild(b)`, `b:setImage(tex)`, `borderColor.a = 0` | `V:client/ISUI/ISCollapsableWindow.lua:55-61` | Window |
| `b:forceImageSize(w, h)` | `V:client/ISUI/ISInventoryPage.lua:1479` | Window |
| `b.enable` / `b.tooltip` (Felder) | `V:client/ISUI/Hutch/ISHutchUI.lua:619-620`; onclick nur bei enable `V:client/ISUI/ISButton.lua:45`; Tooltip auch grau `:19`, `:176`, `:316-346` | WinParts, Window |
| `ISButton.updateTooltip(self)`, `tooltipUI:setVisible(false)` + `removeFromUIManager()` | `V:client/ISUI/ISButton.lua:176`, `:342-343` | WinParts, Window |
| `ISButton:setVisible(b)` | `V:client/ISUI/ISButton.lua:9` | Window |
| Tooltip-Text `" <LINE> "`, `" <LINE> <RGB:r,g,b> "` | `V:client/ISUI/ISGarmentUI.lua:136`, `V:client/ISUI/ISWorldObjectContextMenu.lua:376` | WinData |
| `drawRect` / `drawRectBorder (x, y, w, h, a, r, g, b)` | `V:client/ISUI/ISUIElement.lua:1191`, `:1219` | WinParts, Window |
| `drawText` / `drawTextRight` / `drawTextCentre (s, x, y, r, g, b, a, Schrift)` | `V:client/ISUI/Animal/ISAnimalUI.lua:58`, `:64`; `V:client/ISUI/ISToolTip.lua:120` | WinParts, Window |
| `drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | `V:client/Chat/ISChat.lua:418` | WinParts, Window |
| `getTexture(Pfad)` (eigene Bilder, Vanillas `Button_Close.png`) | `V:client/Chat/ISChat.lua:137`, `V:client/ISUI/ISCollapsableWindow.lua:386` | Window |
| `getTextManager():getFontHeight(UIFont.Small / Medium / Large)` | `V:client/ISUI/Animal/ISAnimalUI.lua:4`, `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8`, `ISAdminTicketsUI.lua:6` | WinParts |
| `getTextManager():MeasureStringX(Schrift, Text)` | `V:client/ISUI/ISButton.lua:450` | Window |
| `getCore():getScreenWidth()/getScreenHeight()` | `V:client/Challenge/WinterIsComing.lua:18` | Window |
| `addToUIManager()`, `removeFromUIManager()`, `setVisible(b)`, `bringToTop()`, `isReallyVisible()`, `setX/Y/Width/Height`, `getX/getY` | `V:client/ISUI/ISUIElement.lua:1365`, `:1373`, `:657`, `:1548`, `:690`, `:195-245`; `V:client/ISUI/ISLayoutManager.lua:55` | Window |
| `ISLayoutManager.RegisterWindow(name, Klasse, fenster)`; gerufen `RestoreLayout(target, name, layout)` / `SaveLayout(...)` | `V:client/Chat/ISChat.lua:1172`; `V:client/ISUI/ISLayoutManager.lua:103`, `:111`; NIE `layout.visible` (`:45`) | Window |
| `getFileReader(Name, true)`, `readLine`, `close`; `getFileWriter(Name, true, false)`, `write`, `close`; `string.trim` | `V:client/ISUI/ISLayoutManager.lua:127`, `:131`, `:133`, `:172`, `:174`, `:185`, `:136` | Tags |
| `Events.OnResolutionChange / OnGameStart / OnTick .Add(fn)` | `V:client/ISUI/PlayerData/ISPlayerData.lua:206`; `V:client/Chat/ISChat.lua:1186`, `:943` | Window, Pose, Tags |
| `HaloTextHelper.addText(p, t)` | `V:client/Foraging/forageClient.lua:73` | Window |
| `animal:setVariable(Text, Text)`, `animal:clearVariable(Text)` (am Tier) | `V:shared/TimedActions/Animals/ISPetAnimal.lua:43`, `:48` | Pose |
| `PZAPI.ModOptions addComboBox` / `addItem` | `V:client/PZAPI/ModOptions.lua:121`, `:131` (wie B1e MarkerSize) | Options |
| `menu:addOption(Text, Ziel, fn, Arg)` | `S:client/BanditsNPCBearMenu.lua:241` (Form wie B1b-B1e) | Menu |
| Tasten-Beschriftung `getText("UI_optionscreen_binding_" .. Name)` (Vanilla liest selbst) | `V:client/OptionScreens/MainOptions.lua:2165`, `:2177` | Texte |
| NPC Crew nur lesen: `BanditsNPC.Interact.KEYBIND`, `.FindTarget(p)`; Doppel-Riegel-Schleife gelernt | `NC:client/BanditsNPCInteract.lua:35`, `:41`; `NC:client/ISUI/BanditsNPCFarmPanel.lua:1252` | Key |
**Jar-only-Aufrufe: keine.** **Nicht benutzt:** `getVariableString` (kein Vanilla-Beleg am Tier), `ISCollapsableWindow`-Titelleiste, `ISTickBox`,
`drawTextZoomed`, `drawProgressBar`, 3D-Bild des Baeren, `setDebugAcceptance`, `pcall`.

## 4. Text-Schluessel je Sprache
| Sprache | UI.json gesamt | davon `UI_BN_Bear_*` | neu in F1 | Sandbox.json gesamt (neu) |
|---|---|---|---|---|
| EN | 274 | 272 | 115 + 2 Tasten | 62 (+2) |
| PTBR | 274 | 272 | 115 + 2 | 62 (+2) |
| RU | 274 | 272 | 115 + 2 | 62 (+2) |
| KO | 274 | 272 | 115 + 2 | 62 (+2) |
| ES | 274 | 272 | 115 + 2 | 62 (+2) |
| CN | 274 | 272 | 115 + 2 | 62 (+2) |
| FR | 274 | 272 | 115 + 2 | 62 (+2) |
Neu: 99 Fenster-/Menue-/Options-/Schild-Texte (`Win_*`, `Menu_Window*`, `MO_WinSize*`, `Tag_Sit`, `Tag_Roam`), 16 Meldungen des KERNs mit Big-Fassung
(`Note_Sit/Roam/Coming/Came/ComeFail/PassiveOn/PassiveOff`, `Why_OutOfReach` je + Big), 4 B1e-Reste (`Why_GoneBig`, `Note_DeadBig`, `Menu_HoldBig`,
`Menu_HoldTipBig`) = 115; dazu `UI_optionscreen_binding_NPC Crew Bear` / `..._Bear window`. Gleiche Platzhalter je Sprache, Big = Grundschluessel,
kein `<`/`>`, `%%` fuer Prozent, Round-Trip/sortiert/LF/UTF-8 ohne BOM, CN: 453 verschiedene Zeichen, **alle in Vanilla-CN**. Woerter fuer
"Kacheln" wie die frueheren Sandbox-Texte (quadrados / клетки / 칸 / casillas / 格 / cases).

## 5. Pruefer-Ausgaben (11./12.11. nachts)
```
luacheck.py   (11 Client-Dateien): 11 file(s) checked, 0 failed
scopecheck.py (11): 11 file(s), 0 violation(s)
localcount.py: hoechstens 51 aktiv / 62 insgesamt (Hud, unveraendert hoch); neu: Window 37 / 56, WinData 36, WinParts 22 -- alle < 180
luacheck_pz.py: 20 Treffer (W113) -- B1e-Stand 18 + 2 neue Bench-Rueckrufe auf die eigenen globalen NCBear_*-Befehle (gleiche Art wie bisher:
               globale Bench-Befehle und die Zeitaktions-Klassen aus shared/)
Zeilenenden/ASCII: 45 Dateien (Client-Lua, 21 JSON, sandbox-options.txt, Werkzeuge) LF, Lua ASCII, kein BOM
attrappe/f1_ober/run.lua:          Attrappe OBERFLAECHE F1 (mit Kern-Attrappe): 359 ok, 0 Fehler
attrappe/f1_ober/run.lua kern:     Attrappe OBERFLAECHE F1 (mit echtem Kern (shared)): 359 ok, 0 Fehler
attrappe/f1_ober/texte_pruefen_f1.py --tmp: FEHLER gesamt: 0 (Werkzeug-Gegenprobe 22 Dateien: F1 == Staging, --basis == texte_b1e.py)
attrappe/f1_ober/belege_f1.py:     85/85 Belege, 83 'V:...:Zeile'-Fundstellen in den neuen Dateien vorhanden, FEHLER gesamt: 0
ober / b1b_ober / b1c_ober / b1d_ober / b1e_ober run.lua (Attrappe und kern): 116/117, 144/134, 155/142, 174/176, 230/230 ok, je 0 Fehler
ober .. b1e_ober texte_pruefen*: je FEHLER gesamt: 0
gesamt/run.lua:                    ERGEBNIS: 1672 bestanden, 0 Fehler (mit dem heutigen Staging inkl. KERN-Stand)
baer_uebernahme.py --staging --vor-b5a (Trockenlauf, schreibt nichts): 5 Fehler = genau die geplanten Naehte (Plan 11.3):
  2 x TEXT_NS "UI_optionscreen_binding_*", 3 x Regel taste: Key.lua:41 KEY_V, Key.lua:96 Events.OnKeyPressed, Window.lua:543 KEY_ESCAPE
```
Die neue Attrappe deckt Plan 8.2 Nr. 1-13: Schriftwahl (1x/2x/4x), Masse 640 x 615 / 1280 x 1178 und Wachsen bei langen Knopftexten, f eine Stufe
kleiner bei H > 0,92 x Bild; Modell fuer Junges/gross/vermisst/faehrt mit/ausser Reichweite/im Auto/zu weit/kommt/versteckt/Leben fehlt/alte Sicht;
Farbverlauf; Taste mit allen Vorfahrten, Radial-Schliessen, Esc, Debounce, Namensfeld, umgelegte Taste, kein Baer, Sicht nicht frisch; Klicks (Mode x 4,
Come, Call, Passive on/off, Rename, grau = keine Bitte, MP sendClientCommand, Tooltip am grauen Knopf); Lage (nur x/y, Klemmen, Aufloesung); Takt
(5 Bilder: 0 x U.T, 0 x MeasureStringX; neues Modell erst nach 1 s oder neuer Sicht; geschlossen nichts); Pose (sitdown -> sit nach 1,7 s,
standup -> loeschen nach 1,4 s, busy ohne Schreiben, Tausch-Kopie neu, Deckel); Tags (Datei, Neuladen, Deckel 64, Hud ohne Name-Zeile mit Balken);
Menue "Bear window" nur am eigenen zahmen Baeren, Texte je Koerper; Bench SP/MP; Dateiform. Vanillas ISPanel.lua/ISButton.lua laufen dabei ECHT.

## 6. Kollisionen (Taste und neue Namen)
- **V liegt in Vanilla schon auf** "Vehicle Radial Menu" (`V:shared/keyBinding.lua:131-132`) und "Animal Radial Menu" (`:186-187`); "Toggle UI" hat keine
  Vorgabe (`:142-143`); Debug Shift+V nur mit Debug. **NPC Crew:** "Talk to NPC" = V (`NC:client/BanditsNPCInteract.lua:35`, `:7462`); F6 (CrewKey,
  ModOptions), F8 (Beacon) und Bandits G (POSTS) beruehren V nicht. Vorfahrt im Code: NPC vor dem Spieler > Auto > fremdes zahmes Tier > Baeren-Fenster;
  am eigenen Baeren oeffnet das Fenster und Vanillas Tier-Radial wird geschlossen. Doppelte Tasten erlaubt Vanilla (Hinweis-Dialog nur beim Umstellen).
- Neue Namen (Dateien, Klassen `BanditsNPCBearWindow/WinBtn/WinRow/WinTick`, Tasten-Name "Bear window", Abschnitt "NPC Crew Bear", layout.ini-Name
  `BanditsNPCBearWindow`, Datei `BanditsNPCBear.ini`, `UI_BN_Bear_Win_*`, `MO_WinSize`, `BearRoamRadius`): **0 Treffer** in NPC Crew `42/media/lua`,
  `_docs/landkarte_index.txt`, Vanilla `media/lua` und Bandits 42.22/common (grep 11./12.11. nachts).

## 7. MP und rote Linien
- Jeder Befehl geht als Bitte: Einzelspieler `B.Handle` direkt, MP `sendClientCommand` (Rolle user genuegt, nie eine leere Tabelle); Besitz, Lage,
  Abklingzeit, Fahrzeug, Abstand entscheidet der Schreiber. Die grauen Knoepfe sind nur Vorpruefung aus der Sicht. Das Fenster setzt nie einen Wert
  (kein Cheat-Knopf). Namensschild und Fenster-Lage sind Client-Sachen (je Spieler), der Server weiss nichts davon. Der Sitz-Treiber setzt die
  Anim-Variable an der Client-Kopie (MP: jeder Client selbst). Der dedizierte Server laedt `client/` nicht.
- Kein Gegenstand wird erzeugt, genommen oder vernichtet. Nichts haengt endlos (Takt 1 s nur bei offenem Fenster, Pose 250 ms mit Deckel = Sicht).
  Bench nur im Einzelspieler ("singleplayer only").

## 8. Offen / ungeprueft (Testpunkte fuer Kevin, nach dem Einbau Spiel NEU starten)
- Alles Laufzeit-Verhalten. Besonders: ob das ISPanel mit `moveWithMouse` und den ISButton-Kindern sauber zieht und klickt (Ziehen an freien Stellen);
  ob Esc mit `isKeyConsumed` das Spielmenue NICHT oeffnet; ob ein verbrauchtes V wirklich kein OnKeyPressed ausloest (NUR JAR, zusaetzlich 250-ms-Sperre);
  ob Vanillas Tier-Radial am eigenen Baeren nur kurz blitzt; ob die Taste in der Tastaturbelegung unter "NPC Crew: Bear" erscheint (Zeile auf Dateiebene,
  Lehre NPC Crew).
- Tooltip-Schrift bei 4K (Vanillas ISToolTip waehlt sie selbst nach der Tooltip-Option); lange Texte in RU/FR (das Fenster wird dann breiter, nie
  abgeschnitten); Sitz-Clips am Jungen und am grossen Koerper (Clip-Laengen 1,6 / 1,3 s angenommen -- aendern sie sich, nur `SIT_DOWN_MS`/`STAND_UP_MS`
  nachziehen); `setVariable` an der Client-Kopie im MP (ob ein Tierpaket sie ueberschreibt); `layout.ini` im MP-Client; `tostring(v.u)` bei ~2e15 unter
  Kahlua (NUR Lesart: stabil je Baer, darum fuer die Datei egal).
- Die KERN-Seite (Order.lua, C1, neue Sicht-Felder) baut der andere Bauer; die Attrappe "kern" lief gegen seinen heutigen shared-Stand gruen,
  der Server-Teil nur ueber `gesamt` (die sechs neuen Client-Dateien laedt `gesamt/run.lua` noch nicht -- ZUSAMMENBAU, Abschnitt "21 F1").

## 9. Fragen fuer Kevin (Nachtschicht: gebaut ist der empfohlene Weg)
| # | Frage | gebaut |
|---|---|---|
| O1 | Fusszeile nennt deine echte Taste ("V or Esc closes", nach Umbelegen die neue Taste) -- ok? | ja |
| O2 | "Hold out food" (Rechtsklick) nur noch, wenn dein Baer auf "Stay" steht -- sitzend oder frei laufend lockt ihn Futter nicht. Ok? | ja |
| O3 | Abstand im Fenster kommt von der lebenden Figur, wenn sie geladen ist (genauer als die Server-Sicht) -- ok? | ja |
| O4 | Bei mehreren Baeren oeffnet V den naechstgelegenen; Pfeile blaettern (Plan F6). Ok? | ja |
| O5 | Tooltips der Faehigkeiten: Kopfzeile in Honig-Orange, darunter Wirkung mit Zahl, woher die Erfahrung kommt, "kommt spaeter", Fortschritt. Ok? | ja |
Die Plan-Fragen F1-F15 (`PLAN_F1.md` 12) sind wie empfohlen gebaut (zwei Knoepfe Come here / Unstuck, Roam-Radius 12 als Sandbox, Mittelpunkt = Stelle
des Baeren, Vorfahrt NPC > Auto > fremdes Tier, Radial nur schliessen, Pfeile, Schild je Spieler, Passiv beim Jungen sichtbar, eigener Tasten-Abschnitt,
Fenster bleibt bei jedem Abstand offen, Auto-Groesse 200 % bei 4K, kein 3D-Bild, Coming later ohne Balken).

Statisch geprueft, nicht gespielt.
