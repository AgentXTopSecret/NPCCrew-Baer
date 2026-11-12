# Forschung F1 -- Baeren-Fenster auf V + B1e-Reste (Lauf baer-f1, Rolle FORSCHUNG, 11.11.2026 nachts)

Nur gelesen und belegt, kein Code im Staging. **Statisch geprueft, nicht gespielt.** Jede Laufzeit-Aussage ist eine Lesart.

Kuerzel: `V:` = Vanilla `media/lua/` (Spiel 42.22.2), `B:` = Bandits `42.22/media/lua/`, `NC:` = NPC Crew `42/media/lua/` (nur gelesen),
`S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/` (B1e-Stand, Liste `staging_dateien.txt`), `T:` = Test-Mod `NCBearTest/42/media/`
(nur gelesen), `J:` = Jar-Auszug (`_arbeit/baer_zaehmen/jar_f1/` neu fuer diesen Lauf: `GameKeyboard.txt`, `Texture.txt`,
`TextureID.txt`, `Core.txt`, `GlobalObject.txt`; aeltere `dec/`, `dec_b1b/`). Seite: C = Client (SP und MP-Client), S = Schreiber
(SP und MP-Server), beide = shared.

---

## 0. Ergebnis zuerst

1. **Taste:** Weg wie NPC Crews "Talk to NPC": auf Dateiebene eine Zeile in Vanillas Tabelle `keyBinding` (Reiter
   *Tastaturbelegung*, Vanilla speichert sie selbst in `keysB42.ini`), abfragen in `Events.OnKeyPressed` mit
   `getCore():isKey(NAME, key)`. Belegt (`V:shared/keyBinding.lua`, `V:client/ISUI/FPS.lua:9`, `NC:client/BanditsNPCInteract.lua:7451-7479`).
   Name frei: `"Bear window"` (0 Treffer in NC, Vanilla, Bandits).
2. **V ist schon dreifach belegt:** Vanilla *Animal Radial Menu* (V; zeigt sich bei JEDEM nicht wilden Tier in ~2 Kacheln -- unser
   Baer ist `wild = false`, also oeffnet V neben dem Baeren AUCH Vanillas Tier-Radialmenue), Vanilla *Vehicle Radial Menu* (V, nur am
   Auto), NPC Crew *Talk to NPC* (V, nur mit freundlichem NPC vor einem). Loesungswege in 1.3.
3. **Fenster:** `ISCollapsableWindow` + `ISButton` (grau + Grund-Tooltip geht) + `ISTickBox` + selbst gezeichnete Balken
   (`drawRect`). Vorbilder: Vanillas Tier-Info `ISAnimalUI` (Kopf, Zeilen, Umbenennen) und die Faehigkeits-Kaestchen des
   Charakter-Fensters `ISSkillProgressBar` (10 Kaestchen, Gold 1/0,89/0,38 -- passt zum Honig-Orange). Esc/V schliesst wie
   `ISHandcraftWindow` (`setWantKeyEvents` + `isKeyConsumed` + `onKeyRelease`). Lage ueber `ISLayoutManager` (layout.ini) -- Achtung:
   Vanilla oeffnet ein beim Speichern offenes Fenster nach dem Laden wieder (2.3).
4. **Daten:** Die Sicht hat schon Name, Koerper, Alter/Stufe, Leben, Ausdauer, Modus, Mitfahren, Call-Restzeit, Fuettern/Streicheln.
   **Es FEHLEN in der Sicht:** Faehigkeiten (Erfahrung je Faehigkeit), Traglast, Passiv, "versteckt sich", "geladen", das Kennzeichen
   `u`, die neuen Modi. Die Sicht kopiert nur flache Felder (`S:shared/BanditsNPCBear.lua:458-464`) -> Faehigkeiten als Einzelfelder;
   `B.SkillProgress` (shared) rechnet dann direkt auf dem Sicht-Eintrag (gleiche Feldnamen `xAgi` ... `xNos`).
5. **Sitzen:** gespielter Weg der Test-Mod (`setVariable("NCBearAct", "sitdown"|"sit"|"standup")` + Halten), Clips in BEIDEN
   Koerpern (je 1,6 / 4,0 / 1,3 s, selbst aus den GLBs gelesen). Zwei Luecken: (a) die drei Sitz-Knoten liegen nur in der Test-Mod
   und das Uebernahme-Skript sperrt sie (nur `NCBear_Eat.xml` erlaubt); (b) im MP wird `NCBearAct` NICHT uebertragen (NUR JAR) ->
   jeder Client setzt es an seiner Kopie aus der Sicht.
6. **Frei herumlaufen:** alle Bausteine belegt (Zufallspunkt wie `B.PickForestSquare`, Kachel-Pruefung wie `B.SpotNear`, Gehen ueber
   `B.MoveTo` walk = pathToLocation mit Kevins Wort). **Widerspruch:** das heutige "Bleiben" laesst die Engine schon in 12 Kacheln
   wandern (Kevin: "Bleiben-Radius 12") -- "Frei" mit Vorgabe 8 waere ENGER als "Bleiben" (Frage F-b).
7. **Unstuck:** "Call to me" (`B.HandleCall`) IST der Unstuck-Weg (Kevins Freigabe 11.11. Nr. 5: "Unstuck vorerst als Rechtsklick
   ('Call to me'), spaeter ins V-Fenster"); geht auch fuer "missing" und nicht geladene Baeren. "Komm her" und "Unstuck" waeren damit
   derselbe Knopf (Frage F-a).
8. **C1:** Anschluss im Hirn-Takt nach `countMisses` (Server) mit `B.SpotNear(rec.x, rec.y)` + `B.PlaceCub` -- gleicher Weg wie Call;
   ein spaeter auftauchender alter Koerper ist eine veraltete Kopie (kleinere Generation) und wird nie gebunden.
9. **A5 erledigt:** UI-Bilder ueber `getTexture` werden NICHT auf 256 gedeckelt (NUR JAR: der Deckel greift nur bei Textur-Flag
   128/256; `getTexture` laedt mit 0 oder 4). Vanilla selbst zeigt im Spiel 123 x 302 px grosse UI-Bilder per `getTexture`
   (`V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191`). Kein Handlungsbedarf.
10. **A1/B6:** 4 Schluessel, 12 Fundstellen (Tabelle 6.1). **C3/B7:** keine kleine sichere Aenderung ohne Kevins Antwort (6.3).
11. **Nebenfund (rote Linie "Baer geht nie verloren"):** Vanillas V-Radialmenue bietet am eigenen Baeren "Toeten" an, sobald der
    Spieler eine Waffe mit Tag `KILL_ANIMAL` traegt (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171-1176`); das Rechtsklick-Menue
    blendet "Kill" aus (`S:client/BanditsNPCBearMenu.lua:293`), das Radial nicht. Mit Bestaetigungsfenster (`:1079-1095`).

---

## 1. Tasten (Auftrag a)

### 1.1 Anlegen, abfragen, speichern

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Zeile in Vanillas Tastenbelegung | `table.insert(keyBinding, { value = NAME, key = Keyboard.KEY_V })` auf Dateiebene (client/) | Tabelle `V:shared/keyBinding.lua:6` (Form `:8-14`); gespielt `NC:client/BanditsNPCInteract.lua:7462` (V), `NC:client/ISUI/BanditsNPCBeaconWindow.lua:3538-3540` (F8) | C | **BELEGT** (Lua-Tabelle, kein Engine-Aufruf) |
| Abschnitts-Ueberschrift | `{ value = "[NPC Crew Bear]" }` | `V:shared/keyBinding.lua:8-10`; NC `Interact.lua:7451` (`"[NPC Crew]"`); Anzeige `V:client/OptionScreens/MainOptions.lua:2159-2165` (`getText("UI_optionscreen_binding_" .. Name ohne Klammern)`) | C | BELEGT |
| Beschriftung | Text-Schluessel `UI_optionscreen_binding_<NAME>` in 7 Sprachen | `MainOptions.lua:2177`; NC `shared/Translate/EN/UI.json:3807-3815` | Texte | BELEGT. **Uebernahme-Skript erlaubt in UI.json nur `UI_BN_Bear_*`** (`baer/tools/baer_uebernahme.py:141-142`) -> Ausnahme-Satz wie bei IG_UI.json (`:144-145`) noetig (Naht) |
| keine doppelte Zeile (Test-Mod UND NPC Crew aktiv) | vorher `for _, row in ipairs(keyBinding)` auf `row.value == NAME` | `NC:client/ISUI/BanditsNPCFarmPanel.lua:1250-1255` | C | BELEGT (Lua) |
| Laden / Speichern | macht Vanilla: `MainOptions.loadKeys` registriert jede Zeile (`getCore():addKeyBinding`, `:3467-3510`), liest dann `keysB42.ini` und ordnet ueber den NAMEN zu (`:3516-3585`); Schreiben beim "Anwenden" `saveKeys` (`:3701-3738`, aus `apply` `:3741-3742`) | `V:client/OptionScreens/MainOptions.lua` | C | nichts zu bauen. Lehre NC `Interact.lua:19-34`: **der NAME ist die Identitaet in keysB42.ini -- nie wieder umbenennen** |
| Zeitpunkt | Einfuegen auf Dateiebene reicht: Vanillas `loadKeys` laeuft beim Start NACH den Mod-Dateien | Lehre `NC:client/ISUI/BanditsNPCBeaconWindow.lua:166-172` (gespielt) | C | belegt (NC) |
| Tastendruck | `Events.OnKeyPressed.Add(function(key) ...)`, darin `getCore():isKey(NAME, key)` | `V:client/ISUI/FPS.lua:9` (`getCore():isKey("Display FPS", key)`), `:21`; NC `Interact.lua:7464-7479` | C | **BELEGT** (String-Variante). `isKey` beachtet Shift/Strg/Alt und die Zweittaste (Lehre NC `Interact.lua:7468-7473`) |
| nicht beim Tippen | `ISChat and ISChat.focused` | `V:client/Chat/ISChat.lua:8`, `:615`, `:630`; NC `Interact.lua:7467` | C | BELEGT. Dazu NUR JAR (7): waehrend ein Textfeld tippt, feuert `OnKeyPressed` gar nicht |
| ModOptions-Taste (Alternative) | `PZAPI.ModOptions` `options:addKeyBind(id, name, key, tip)`, gelesen `getOptions(..):getOption(id):getValue()` | `V:client/PZAPI/ModOptions.lua:182`; `B:client/BanditModOptions.lua:14` (POSTS, Vorgabe G), `B:shared/BanditCompatibility.lua:95-99` | C | belegt, landet aber im Reiter **Mods**, nicht in der Tastaturbelegung (Kevin: "einstellbar in den keystings") -> **nicht empfohlen**. NPC Crews `crewKey` (`NC:client/BanditsNPCModOptions.lua:138-155`, F6 fuer die Munitionsanzeige) ist so eine ModOptions-Taste -- Lernstueck, nicht der Weg fuer Kevins Wunsch; NC selbst legt seine Sprechtaste bewusst in Vanillas Tabelle (`BanditsNPCModOptions.lua:120-124`) |
| Hinweis "kein eigener Baer" | `HaloTextHelper.addText(player, text)` | `V:client/Foraging/forageClient.lua:73` (schon in `S:client/BanditsNPCBearClient.lua:341`) | C | BELEGT |
| Rechtsklick "Bear window" | `menu:addOption(text, playerObj, fn, v)` im Block des eigenen zahmen Baeren | `S:client/BanditsNPCBearMenu.lua:307-312` (dort `addMode/addName/addCall`), Form `:241` | C | BELEGT |

### 1.2 Wer belegt V schon?

| Belegung | Taste | wann sie wirkt | Fundstelle | Folge mit unserer Taste V |
|---|---|---|---|---|
| Vanilla **Animal Radial Menu** | V | `OnKeyStartPressed` (beim Druecken): `AnimalContextMenu.showRadialMenu`, wenn `playerObj:getUseableAnimal()` ein Tier liefert und es **nicht wild** ist | `V:shared/keyBinding.lua:186-187`; `V:client/ISUI/ISUIHandler.lua:35-58` (Anzeige `:55-57`), Loslassen `:87-95`; `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1151-1153`, `:1155-1171` | **unser Baer: `wild = false`** (`S:shared/BanditsNPCBearDefs.lua:100`; der grosse Koerper kopiert das). `getUseableAnimal` nimmt jedes Tier in den Kacheln x-2..x+1 / y-2..y+1 (NUR JAR, 7) -- ein folgender Baer (Halteabstand 3, `S:shared/BanditsNPCBear.lua:80`) ist oft darin. Dann oeffnet V BEIDES. Mit Vanillas Vorgabe "Radialmenue-Taste umschalten = aus" verschwindet das Radial beim Loslassen (`ISUIHandler.lua:87-93`) und unser Fenster oeffnet beim Loslassen (OnKeyPressed) -> das Radial blitzt kurz; mit "umschalten = an" bleibt es offen. Im Radial steht "Toeten" (Nebenfund 0.11) und "Tier-Info" (`:1222`) |
| Vanilla **Vehicle Radial Menu** | V | nur wenn `ISVehicleMenu.getVehicleToInteractWith(player)` ein Fahrzeug liefert (im/am Auto) | `keyBinding.lua:131-132`; `ISUIHandler.lua:49-53`, `:76-85` | im Auto oeffnen Radial und Fenster (Fenster dort sinnvoll: Baer faehrt mit) |
| Vanilla **Toggle UI** | keine (KEY_NONE) | nur wenn der Spieler sie auf V legt (Kommentar "V can be Toggle UI when outside a vehicle") | `keyBinding.lua:142-143`; `ISUIHandler.lua:45-48`, `:71-74` | nur dann |
| NPC Crew **Talk to NPC** | V | nur wenn `BanditsNPC.Interact.FindTarget(p)` einen freundlichen/neutralen NPC in 3,5 Kacheln VOR dem Spieler findet; sonst still | `NC:client/BanditsNPCInteract.lua:35-36`, `:7462`, `:7474`, `:120-139` (still ohne Ziel `:131-137`) | beide Fenster oeffnen |
| NPC Crew sonst | F8 Beacon (`NC:client/ISUI/BanditsNPCBeaconWindow.lua:127-130`), Zonen-/Feld-Tasten, CrewKey F6 (ModOptions) | -- | NC `table.insert(keyBinding ...)` nur Interact/Beacon/FarmPanel/ZoneLegend | kein V |
| Bandits | POSTS = G (ModOptions) | -- | `B:client/BanditModOptions.lua:14` | kein V |
| Vanilla Debug | Shift+V nur mit Debug | -- | `V:client/DebugUIs/ISFilmingToolsUI.lua:146` | nur Debug |

Eine doppelte Taste ist in Vanilla erlaubt (NPC Crew lebt seit Jahren mit V neben den zwei Radialmenues, `NC Interact.lua:7459-7461`);
stellt Kevin selbst um, zeigt Vanilla bei Doppelbelegung einen Hinweis (`MainOptions.lua:3807` `ISDuplicateKeybindDialog`).

### 1.3 Vorfahrt (Empfehlung, je Weg belegt)

- **NPC Crew:** in unserem Handler zuerst fragen: gibt es `BanditsNPC.Interact.FindTarget` (Existenz-Riegel), liegt die Taste auch auf
  "Talk to NPC" (`getCore():isKey("Talk to NPC", key)`) und findet FindTarget fuer einen lokalen Spieler einen NPC -> **nichts tun, der
  NPC gewinnt.** Nur lesen, keine NC-Datei aendern (Kevin 08.11.: "wer gewinnt ... im Bau klaeren", `begleiter/ENTSCHEIDUNGEN.md:98`).
  FindTarget liest nur (`NC Interact.lua:40-...`, `getCell():getZombieList()`); im MP-Client erlaubt. Naht dokumentieren.
- **Vanilla-Tier-Radial**, drei Wege:
  (a) hinnehmen (Radial blitzt beim Halten von V);
  (b) nach dem Oeffnen unseres Fensters ein offenes Radial schliessen: `getPlayerRadialMenu(nr)`, `menu:isReallyVisible()`,
      `menu:undisplay()` -- dieselben Aufrufe wie Vanilla (`ISAnimalContextMenu.lua:1157`, `:1160`, `:1164`), Client;
  (c) Aufsatz in `OnGameBoot`: `AnimalContextMenu.showRadialMenu` umwickeln und fuer UNSEREN Baeren (`B.BodyKind(player:getUseableAnimal())`,
      `getUseableAnimal` belegt `ISAnimalContextMenu.lua:1152`) kein Radial zeigen -- loest nebenbei den Nebenfund "Toeten im Radial",
      ersetzt aber eine Vanilla-Funktion (Naht; bei Vanilla-Updates pruefen).
  **Empfehlung:** (b) in F1; (c) als Frage F-e an Kevin (mit dem Nebenfund).
- **Oeffnen/Schliessen:** oeffnen in `OnKeyPressed`; schliessen im Fenster selbst (1.4/2.1 Esc-Zeile). NUR JAR (7): ein Tastendruck,
  den ein Fenster verbraucht (`isKeyConsumed`), loest danach KEIN `OnKeyPressed` aus -> V schliesst und oeffnet nicht gleich wieder.

---

## 2. Fenster-Bausteine in Vanilla (Auftrag b)

### 2.1 Tabelle

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Fenster mit Titelleiste, Schliessen-Knopf, Ziehen | `ISCollapsableWindow:derive(name)`, `:new(x,y,w,h)`, `:initialise()`, `:addToUIManager()`, `:setTitle(t)`, `:setResizable(false)`, `:close()` (setVisible false) | `V:client/ISUI/ISCollapsableWindow.lua:9`, `:366-401`, `:14-16`, `:18-20`, `:326-334`, `:134-136`; Schliessen-Knopf `:55-61`; Ziehen `:206-217`, `:270-280`; Vorbild `V:client/ISUI/Animal/ISAnimalUI.lua:8`, `:617-630` (`setResizable(false)` `:628`, Farben `:624-625` = Hintergrund 0/0/0/0,8, Rahmen 0,4) | C | **BELEGT** |
| Joypad-Faehigkeit (optional) | `ISCollapsableWindowJoypad` | `V:client/ISUI/ISCollapsableWindowJoypad.lua:1-48` (Basis von ISAnimalUI) | C | belegt, optional |
| "?"-Knopf mit Erklaer-Text | `window:setInfo(text)` | `ISCollapsableWindow.lua:95-132`; Aufrufer `ISAnimalUI.lua:424-430` | C | BELEGT -- gut fuer Kevins Faehigkeits-Saetze |
| Knopf | `ISButton:new(x,y,w,h,title,target,onclick)`, `:initialise()`, `:instantiate()`, `self:addChild(btn)` | `V:client/ISUI/ISButton.lua:479-532`; Aufrufer `ISAnimalUI.lua:389-394` | C | BELEGT |
| Knopf grau MIT Grund | `btn:setEnable(false)` + `btn:setTooltip(text)` (oder Felder `.enable` / `.tooltip`) | `ISButton.lua:416-439`, `:445-447`; der Tooltip kommt auch grau: `onMouseMove` setzt `mouseOver` ohne enable-Frage (`:18-20`), `updateTooltip` laeuft in prerender (`:176`, `:316-346`); grauer Text `:251-257`; Vorbild `V:client/ISUI/Hutch/ISHutchUI.lua:617-623` (enable = false + Grund-Tooltip) | C | **BELEGT** |
| aktiven Befehl hervorheben | `btn:setBackgroundRGBA`, `setBorderRGBA`, Feld `textColor` | `ISButton.lua:352-378`, `:492` | C | BELEGT (Vanilla-Lua) |
| Ankreuzfeld | `ISTickBox:new(x,y,w,h,name,target,method)`, `:addOption(text)`, `:setSelected(1, bool)`; Rueckruf `(target, index, selected, arg1, arg2, box)` | `V:client/ISUI/ISTickBox.lua:282-322`, `:227`, `:51`, `:156-182`; Aufrufer `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:165` | C | BELEGT |
| Balken selbst gezeichnet | `self:drawRect(x,y,w,h,a,r,g,b)`, `self:drawRectBorder(...)` | `V:client/ISUI/ISUIElement.lua:1191-1198`, `:1219-1227`; im Staging schon so: `S:client/ISUI/BanditsNPCBearHud.lua:568-576` (valueBar) | C | **BELEGT** (empfohlen: eigene Farben, eigene Masse) |
| fertiger Balken (Alternativen) | `self:drawProgressBar(x,y,w,h,f,fg)`; `ISProgressBar:new(...)` | `ISUIElement.lua:1805-1813` (Aufrufer `V:client/ISUI/Gamepad/ISControllerTestPanel.lua:94`; Rest fest grau 0,15); `V:client/ISUI/ISProgressBar.lua:94` (Aufrufer `ISUI/Animal/ISButcherHookUI.lua:407`, `ISUI/ISVehicleAnimalUI.lua:85`) | C | belegt; weniger frei in den Farben |
| Faehigkeiten wie im Charakter-Fenster | `self:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` mit `getTexture("media/ui/SkillPanel/SkillUnit_Fill.png")` / `"SkillUnit_Border.png"`: erreichte Stufen gefuellt Gold, die laufende Stufe anteilig gefuellt, Rest dunkel | `V:client/XpSystem/ISUI/ISSkillProgressBar.lua:128-210` (Farbe `:13-16` = 1 / 0,89 / 0,38; Kaestchen-Groesse `:4-6`; Bilder `:245-246`) | C | **BELEGT**, Vorbild fuer "Stufe 0-10 + Fortschritt" |
| Farbe nach Wert | reine Rechnung (lineare Mischung) + drawRect; Farben des Spielers `getCore():getGoodHighlitedColor()` / `getBadHighlitedColor()` (:getR/G/B) | Mischung wie `ISSkillProgressBar.lua:150-160`; Farben `ISSkillProgressBar.lua:8-10`, `V:client/Chat/ISChat.lua:1125` | C | BELEGT. Lesart: diese Farben folgen Vanillas Farbschwaeche-Einstellung (ungeprueft) |
| Kevins Symbol 1 im Kopf | `getTexture("media/ui/BanditsNPCBearCub_marker288.png")` (288 px; auch 96 px `_marker.png`) + `drawTextureScaled` / `drawTextureScaledAspect` | Laden wie `S:client/ISUI/BanditsNPCBearMarker.lua:377-392` (`getTexture` `V:client/Chat/ISChat.lua:921`); Zeichnen `V:client/Chat/ISChat.lua:418`, Aspect `V:client/ISUI/Maps/ISWorldMap.lua:482` (`S:...BearMap.lua:25`) | C | BELEGT (Groessen selbst aus dem PNG-Kopf: 96 x 96, 288 x 288, RGBA) |
| Text | `drawText` / `drawTextRight` / `drawTextCentre` `(str, x, y, r, g, b, a, font)`; Breite `getTextManager():MeasureStringX(font, str)` | `ISUIElement.lua:1280`, `:1293`, `:1306`; Muster "Etikett rechtsbuendig, Wert links blasser" `ISAnimalUI.lua:64-65`, Name Medium + Unterstrich `:56-61` | C | BELEGT |
| Schrifthoehen | `getTextManager():getFontHeight(UIFont.Small / Medium / Large)` | `ISAnimalUI.lua:4-5`; Large `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6` (so zitiert in `S:...BearHud.lua:120-121`) | C | BELEGT |
| Skalierung 4K | (1) Vanillas Mass `FONT_SCALE = getFontHeight(UIFont.Small) / 19` ("normalize to 1080p"); (2) B1e-Faktor `U.MarkerFactor(H, idx)` mit `getCore():getScreenHeight()` (2054 -> 2,0); (3) Schriftstufen wie `tierOf` | (1) `V:client/Entity/ISUI/BuildRecipe/ISWidgetBuildControl.lua:7`; (2) `S:client/ISUI/BanditsNPCBearMarker.lua:108-123`, `:264-268` (`getScreenHeight` `V:client/Challenge/WinterIsComing.lua:18`); (3) `S:client/ISUI/BanditsNPCBearHud.lua:122-148` | C | BELEGT. Empfehlung: Masse = Grundmass x f, f = MarkerFactor (Kevins 2054 px -> 2,0), Schrift Small/Medium/Large nach f wie die Markierung (`Marker.lua:275-281`) |
| Titelleiste bei 4K | ISCollapsableWindow nimmt fest `UIFont.Small` (`titleFont`, `titleFontHgt` `:398-399`; Hoehe `:298-300`); der Titeltext nutzt `self.titleBarFont` (`:173-174`, nirgends gesetzt) | `ISCollapsableWindow.lua` | C | **ungeprueft**, ob ein Ueberschreiben von `titleFont`/`titleFontHgt` nach `:new` ueberall wirkt (kein Vanilla-Aufrufer mit Medium). Sicherer: Titelleiste schmal lassen, den Kopf (Symbol, Name gross) selbst in den Fensterkoerper zeichnen |
| Lage merken | `ISLayoutManager.RegisterWindow(name, Klasse, fenster)`; speichert beim Spielspeichern (`OnPostSave`) in `layout.ini` je Aufloesung | `V:client/ISUI/ISLayoutManager.lua:6-13`, `:191-232`, Datei `:125-127` / `:169-172`; nur Spieler 0 wie `V:client/TimedActions/ISGeneratorInfoAction.lua:23-24` | C | **BELEGT.** ACHTUNG: `DefaultRestoreWindow` oeffnet das Fenster nach dem Laden wieder, wenn es beim Speichern offen war (`:45-50` `layout.visible`) -> eigenes `SaveLayout` ohne `visible` (ueberschreibbar wie `ISCollapsableWindow:SaveLayout` `:351-354`; Klasse mit eigenen Funktionen: `V:client/Chat/ISChat.lua:1172`) |
| Esc / eigene Taste schliesst | in `:new` `o:setWantKeyEvents(true)`; `isKeyConsumed(key)` -> `key == Keyboard.KEY_ESCAPE or getCore():isKey(NAME, key)`; `onKeyRelease(key)` -> `close()` + `removeFromUIManager()` | `V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-297`, `:386`; `V:client/ISUI/Hutch/ISHutchUI.lua:884-893` (nur Spieler 0) | C | **BELEGT** |
| Startlage | `getPlayerScreenLeft/Top/Width/Height(nr)` | `ISGeneratorInfoAction.lua:15-18` | C | BELEGT |
| An-/Abmelden | `addToUIManager()`, `removeFromUIManager()`, `setVisible`, `bringToTop`, `isReallyVisible` | `ISUIElement.lua:1365`, `:1373`, `:657`, `:1548`, `:690` | C | BELEGT |
| 3D-Bild des Baeren (optional) | `ISCharacterScreenAvatar:new(...)`, `setCharacter(animal)`, `setAnimSetName(animal:GetAnimSetName())`, `setState("idle")` | `ISAnimalUI.lua:369-376`; Klasse `V:client/XpSystem/ISUI/ISCharacterScreen.lua:30-36` | C | belegt; geht nur mit geladener Kopie; NPC-Crew-Lehre "genau EIN ISUI3DModel, ein GPU-Puffer (Absturz v0.77.9)" (`NC:client/BanditsNPCModOptions.lua:10-14`) -> **nicht in F1** (Frage F-f) |

### 2.2 Vorbild-Fenster (zum Ansehen im Bau)
- **Tier-Info `ISAnimalUI`** (`V:client/ISUI/Animal/ISAnimalUI.lua`): Bildfeld links mit Rahmen (`:37-39`), Name in Medium mit Linie
  (`:56-61`), Zeilen "Etikett rechts / Wert links, Alpha 0,5" (`:64-97`), Umbenennen-Knopf rechts in der Namenszeile (`:48-49`,
  `:389-394`), Hoehe waechst mit dem Inhalt (`:338-341`), "?"-Info (`:424-430`), schliesst sich bei Abstand > 5 (`:19-20`; fuer uns
  NICHT gewollt -- das Fenster soll auch fuer einen fernen Baeren gehen).
- **Faehigkeiten des Charakter-Fensters** `ISSkillProgressBar` (2.1): 10 Kaestchen, Gold, laufende Stufe anteilig.
- **ISHutchUI** (`V:client/ISUI/Hutch/ISHutchUI.lua:617-623`, `:884-893`): grauer Knopf mit Grund, Esc schliesst.

### 2.3 Lage merken -- Einzelheiten
`ISLayoutManager` ist die Vanilla-Datei `layout.ini` des Rechners (Client), je Bildschirmaufloesung (`:196-211`), geschrieben bei JEDEM
Spielspeichern (`Events.OnPostSave`, `:232`). Im MP schreibt der Client sie selbst (Vanilla tut das fuer Inventar, Chat, Minikarte:
`V:client/ISUI/PlayerData/ISPlayerDataObject.lua:151-155`). Der Fenstername steht in einer gemeinsamen Datei -> eindeutiger Name
(`BanditsNPCBearWindow`, 0 Treffer, Abschnitt 8).

---

## 3. Daten im Staging, die das Fenster zeigt (Auftrag c)

### 3.1 Der Sicht-Eintrag (Client `B.View.cubs[id]`, gebaut `S:server/BanditsNPCBearRegistry.lua:563-590`)

| Feld | Inhalt | Quelle | im Fenster |
|---|---|---|---|
| `id`, `oid` | Kennung; OnlineID der Kopie (-1, wenn kein Koerper in der Welt) | `Registry.lua:564-570`, `:582` | Zuordnung; `oid` NICHT als "geladen" nehmen (Einzelspieler-Wert ungeprueft) |
| `st` | new / shy / fed / tame / missing | `Registry.lua:303`, `S:server/BanditsNPCBearServer.lua:832-842` | eigener Baer = `tame` oder `missing` |
| `owner`, `bond`, `finder`, `src` | Spielerschluessel (SP immer `"__sp"`, `S:shared/BanditsNPCBear.lua:41`, `:363-371`) | `Registry.lua:583` | "eigen" = `owner == B.View.me.key` |
| `tame` | Zaehm-Balken 0..100 (nach dem Zaehmen fest 100) | `Registry.lua:305`, `S:shared/BanditsNPCBearRules.lua:68-80` | nur "gezaehmt"; Vertrauen gibt es nicht (3.7) |
| `fedN`, `petN`, `last`, `feedAt`, `petAt` | Zaehler, letzte Handlung, Zeiten (Weltstunden) | `Registry.lua:582-583` | Fuettern/Streicheln-Bereitschaft ueber `B.WaitLeft(v, "feed"/"pet", B.Now())` (`Rules.lua:120`; Client nutzt es schon `S:client/ISUI/BanditsNPCBearHud.lua:263-267`) |
| `name` | Name oder nil (dann Vorgabe `U.CubName`) | `Registry.lua:584`; `S:client/BanditsNPCBearClient.lua:312-326` | Kopf |
| `mode` | NUR bei `tame`: `B.ModeOf` = "follow" / "stay" | `Registry.lua:572-573`, `Rules.lua:330-333` | Zustand; neue Modi siehe 3.5 |
| `x`, `y` | letzte bekannte Kachel (ganze Zahl) | `Registry.lua:585` | Abstand / Richtung |
| `ride` | true = faehrt mit | `Registry.lua:579-580` | Zustand, Knoepfe grau |
| `callWait` | Sekunden Rest "Call to me" (nur fuer den Besitzer, fehlt = bereit) | `Registry.lua:574-578`; Client-Rest mit `U.viewAt` `S:client/BanditsNPCBearMenu.lua:247-260` (Funktion ist LOCAL -> fuer das Fenster ausschreiben oder nach `U.` heben) | Restzeit am Knopf |
| `sz`, `bd` | gezeigte Groesse; Koerper "cub"/"big" | `S:server/BanditsNPCBearGrow.lua:753-755` (nur `tame`) | "Junges" / "grosser Baer" |
| `hp`, `hpMax` | Leben in % (fehlt, solange `rec.hp` fehlt) / Hoechstwert in Punkten | `Grow.lua:756-762` | Balken "92/150" |
| `sta`, `staMax` | Ausdauer % (nur Sitzung; ohne Sitzung 100) / Hoechstwert | `Grow.lua:763-767`; Sicht gedrosselt (10 Punkte UND 5 s, `Grow.lua:405-416`) | Balken |
| `day`, `stg`, `nst`, `nxt` | Wachstumstag; Stufe cub/half/strong/adult; naechste Stufe; Tage bis dahin | `Grow.lua:768-771`; Formeln `S:shared/BanditsNPCBearStats.lua:200-218`, `:307-309`, `:358-367` | "Tag 12 -- halbstark in 3 Tagen" (`UI_BN_Bear_Tag_Age` "Day %1 - %2 in %3 day(s)", `Client.lua:143-144`) |
| `me.*` (je Spieler) | key, on, bears, maxBears, bonded, wild, bait, lockUntil | `Registry.lua:390-420` | "kein eigener Baer" = `me.bears == 0` (zaehlt auch missing) |

Zuordnung Tier <-> Eintrag auf dem Client: `B.ViewOf(animal)` (`S:shared/BanditsNPCBear.lua:516-532`, Spiegel, sonst OnlineID);
lebende Kopie: `U.CubObj(id)` / `U.CubPos(id)` (`S:client/ISUI/BanditsNPCBearHud.lua:745-758`, aus der Balken-Tabelle, kein eigener
Suchlauf). Die Sicht traegt den eigenen Baeren IMMER (vor allen anderen, `Registry.lua:608-609`), auch weit weg.
Sicht frisch? `U.Fresh()` (`Client.lua:362-368`); sonst `U.AskHello(player)` (`:386-392`).
Neue Sicht -> `B.OnView()` (`Hud.lua:763-766`) -> das Fenster kann sich dort "neu lesen" merken; zeichnen nur aus fertigen Feldern
(hoechstens ein paar Mal je Sekunde neu lesen, wie der Balken mit LIST_MS 1000, `Hud.lua:55`).

### 3.2 Was in der Sicht FEHLT (Liste fuer KERN/Plan)

| Fehlt | wo die Wahrheit liegt | Vorschlag | Beachten |
|---|---|---|---|
| Faehigkeiten | `rec.xAgi ... rec.xNos` (`Grow.lua:43`; Spiegel `S:server/BanditsNPCBearHeal.lua:45`) | in `B.GrowView` 6 Zahlen `xAgi..xNos` mitschicken; der Client rechnet `B.SkillProgress(v, key)` -> Stufe, XP in Stufe, Bedarf (`Stats.lua:316-344`, shared, rein; Feldnamen passen 1:1 ueber `B.SKILL_FIELD` `:111`) | `copyFlat` kopiert nur Zahl/Text/Wahrheitswert auf oberster Ebene (`S:shared/BanditsNPCBear.lua:458-464`) -> keine Untertabelle |
| Traglast, Ausweichen, Schaden-Bonus, Fang-Chance, Warnweite | `B.StatsOf(rec)` (`Stats.lua:350-395`: `carry`, `dodge`, `fightBonus`, `fish`, `nose`) | als gerundete Zahlen mitschicken (Server rechnet `StatsOf` ohnehin in `GrowView`) | "Traglast als Wert" (Auftrag); Wirkung erst F4/B5a/F5 |
| Passiv | gibt es nicht | neues Register-Feld (`rec.passive`, Wahrheitswert) + Spiegel (`MARK_FIELDS` `Heal.lua:42-47`) + `B.Restore` / `B.TakeNewerMark` (`Heal.lua:189-283`, `:316-388`) + Sicht | Bitte mit Besitzerpruefung (3.5) |
| versteckt sich | nur Sitzung `B._s[id].g.on / g.mode` (`S:server/BanditsNPCBearGuard.lua:291-347`) | Sicht-Feld (z. B. `hide = true`) + `B.Touch(nil, rec.owner)` beim Wechsel (heute KEIN Touch bei Guard-Wechsel) | sonst zeigt das Fenster es erst mit der naechsten anderen Aenderung |
| geladen | Schreiber: `B.FindAnimal(rec)` (`S:server/BanditsNPCBearWorld.lua:530-539`) | Sicht-Feld (z. B. `ld = true/false`) | Zustand "nicht geladen", Knoepfe grau |
| Kennzeichen `u` | `rec.u` (eindeutig: Zeitstempel x 1000 + Zufall, `Registry.lua:77-79`) | mitschicken, falls Einstellungen je Baer beim Client (Namensschild) gespeichert werden | Zahl < 2^53 (`Registry.lua:79`) |
| neue Modi | -- | 3.5 | "mode" ist heute an 7 Stellen auf follow/stay festgenagelt |
| Stufe "Jungtier" als Wort | `U.StageName` kennt nur half/strong/adult (`Client.lua:198`, `:245-250`) | neuer Schluessel (z. B. `UI_BN_Bear_Stage_Cub`, frei) | Kopfzeile |
| Faehigkeiten-Namen gross | vorhandene Schluessel klein fuer Satzmitte ("agility", "toughness", "keen nose"; `Client.lua:148-153`) | eigene Fenster-Schluessel | 7 Sprachen |

### 3.3 Werte und Faehigkeiten (Formeln, alle `S:shared/BanditsNPCBearStats.lua`)

| Wert | Formel / Stelle | wirkt heute? |
|---|---|---|
| Leben max | Kurve 40/150/400 an Groesse 0,35/0,75/1,35 x (1 + 0,05 x Stufe "Leben") (`:374`; `S:shared/BanditsNPCBear.lua:137`, `:139`) | ja (Hoechstwert, Heilung `S:server/BanditsNPCBearHeal...`/`Grow.lua`) |
| Ausdauer max | 50/100/160 x (1 + 0,05 x Kondition) (`:375`) | Anzeige; sinkt nur bei unseren Rennbefehlen, "ohne Wirkung" bis B5a (`Grow.lua:352-357`) |
| Traglast | 10/40/100 (`:376`) | Anzeige (Inventar F4) |
| Schaden | 0/0,35/1,0 x (1 + Kaempfen-Bonus) (`:377-378`, Bonus bis `BearFightBonusMax` 70 %) | B5a |
| Ausweichen | 5 % + (BearDodgeMax 40 - 5) x Agilitaet/10 (`:379-380`) | B5a |
| Fang-Chance | ab Halbstark 10..60 % aus Fischen-Stufe und Groesse (`:381-388`) | F5 |
| Warnweite | 12 + 1,5 x Spuernase (`:389`) | F5 |
| Stufe 0-10 | Kurve `xpNeed` 100 ... 380, Summe 2133 (`S:shared/BanditsNPCBear.lua:141`); `B.SkillLevel` `:327-335`, `B.SkillProgress` `:338-344` | -- |
| Erfahrung kommt aus | `B.SkillAdd` mit Eimer 6/min (`Grow.lua:278-314`); Treffer genommen -> agi + vit (`:329-333`, B5a), Treffer ausgeteilt -> fgt (`:335-337`, B5a), Fischen (`:340-345`, F5), Schnueffeln (`:347-349`, F5), **Kondition schon heute** beim Rennen und Ausser-Puste (`Grow.lua:378-400`) | -- |

**Kevins Saetze fuer die Tooltips** (woertlich in `baer/begleiter/ENTSCHEIDUNGEN.md`):
- Agilitaet `:221` *"ein agilitaets skill wie bei den npc's das erhoeht die ausweichchance vom baeren das er garnicht erst getroffen
  wird, das levelt pro hit den er kassiert"*; Fest `:222`, `:227` (Stufe 0 = 5 %, 10 = 40 %). -> **wirkt erst mit dem Kampf (B5a)**.
- Leben `:221` *"...wie das leben das wer skill hoeher geht aber zusetzlich geht das leben auch hoch pro wachstums tage"*; `:223`. ->
  Bonus wirkt jetzt im Hoechstwert, **steigt aber erst mit Treffern (B5a)**.
- Kondition `:226` (steigt durch Rennen, Kaempfen, vor allem Ausser-Puste; groessere Ausdauer-Leiste, schnellere Erholung). -> **steigt
  schon jetzt beim Rennen**; Ausdauer hat bis B5a keine Wirkung.
- Kaempfen `:225`/`:228` *"kaempfen damit meinst du ja sicher schaden"*, `:230` *"mach +70% bei stufe 10"*. -> **B5a**.
- Fischen `:211`, `:213` *"fischen soll er ja auch koennen ab dann wann der kaempfen kann aber nur schlecht und dann am ende viel besser"*.
  -> **kommt spaeter (F5), ab Halbstark**.
- Spuernase `:214`, `:220` (riecht Zombies frueher, warnt mit Brummen, abschaltbar). -> **kommt spaeter (F5)**.

### 3.4 Zustand (Kopfzeile) -- woher

| Zustand | heute erkennbar aus | Luecke |
|---|---|---|
| folgt / bleibt | `v.mode` (3.1) | -- |
| sitzt / frei | -- | neue Modi (3.5) |
| versteckt sich | -- | Sicht-Feld (3.2) |
| faehrt mit | `v.ride == true` | -- |
| vermisst | `v.st == "missing"` | -- |
| nicht geladen | -- (Client: `U.CubObj(id)` nil heisst auch "nur zu weit fuer DIESEN Client") | Sicht-Feld `ld` (3.2) |

### 3.5 Befehle: Weg Client -> Schreiber (alles schon gespielt bis auf die neuen)

`B.Ask(player, befehl, args)` (`S:shared/BanditsNPCBear.lua:541-550`): MP-Client `sendClientCommand(player, "BanditsNPCBear", befehl, args)`
(`V:client/DebugUIs/DebugContextMenu.lua:956`, Rolle user genuegt), SP direkt `B.Handle`. Server: `Events.OnClientCommand`
(`S:server/BanditsNPCBearServer.lua:412-418`, `:1051`; `V:server/ClientCommands.lua:1357`) -> `B.Handle` (`:371-406`). Antwort:
Meldung `B.Tell` (`S:shared/BanditsNPCBear.lua:555-564`) + `B.FlushViews()`. Leere Tabelle kommt als nil an -> nie leer senden
(`Client.lua:381-383`). Drossel je "Spieler|Befehl|ok/no" 500 ms (`S:server/BanditsNPCBearFollow.lua:53-82`, `askMs`
`S:shared/BanditsNPCBear.lua:89`).

| Befehl | Pruefungen beim Schreiber | Fundstelle | fuer das Fenster |
|---|---|---|---|
| `Mode {id, mode}` | mode nur follow/stay (`:221`); Eintrag, nicht missing (`:222-225`); Besitzer + tame (`:226-229`); nicht ride (`:230-234`); **Koerper geladen** (`:235-239`); follow: nicht im Auto, Abstand <= BearFollowMaxDistance 40 (`:240-249`) | `Follow.lua:217-253`, `B.SetMode` `:92-122` (mode nur follow/stay `:93`; stay: Heimat = jetzige Kachel `:95-97`) | Folgen, Bleiben; Sitz/Frei als neue Werte |
| `Rename {id, name}` | Besitzer, tame ODER missing, `B.CleanName` | `Follow.lua:257-286`; Fenster `U.AskName(playerObj, v)` `S:client/ISUI/BanditsNPCBearNameBox.lua:56-77` | Umbenennen-Knopf |
| `Call {id}` | Eintrag; Besitzer, tame ODER missing; nicht ride; Spieler nicht im Auto; Abklingzeit; freie Kachel 1..3 Ringe; frisch erzeugter Koerper wartet | `S:server/BanditsNPCBearRide.lua:300-375` | Unstuck / Komm her (Frage F-a) |
| `Hello` | -- | `Server.lua:374-377` | Sicht nachfragen |
| neu: Passiv | Besitzer, tame/missing (wie Rename) | -- | Schalter je Baer |

**"mode" ist heute an 7 Stellen auf follow/stay festgenagelt** -- neue Modi muessen dort alle nachziehen:
`S:shared/BanditsNPCBearRules.lua:330-333` (`B.ModeOf`), `S:server/BanditsNPCBearFollow.lua:93` (`B.SetMode`), `:221` (`HandleMode`),
`S:server/BanditsNPCBearRegistry.lua:131-135` (Laden: unbekannt -> stay mit Fehlerzeile!), `S:server/BanditsNPCBearHeal.lua:228-229`
und `:368-369` (Spiegel), Client `S:client/BanditsNPCBearMenu.lua:215-220` und `S:client/ISUI/BanditsNPCBearHud.lua:271-276`
(Schild-Zeile 2: alles ausser follow heisst "staying"). Folgen-Takt nur bei follow (`Server.lua:776-779`), sonst `B.Decide`
(`:780-791`).

### 3.6 Abklingzeiten

| Was | Wert | Fundstelle | im Fenster |
|---|---|---|---|
| Call to me | Sandbox `BearCallCooldownMinutes` 5 (Echtzeit-Minuten), je Baer, nur Sitzung | `S:shared/BanditsNPCBear.lua:175`; `B.CallLeft` `S:server/BanditsNPCBearRide.lua:245-256`; Sicht `callWait` | Restzeit am Knopf, grau |
| Fuettern / Streicheln | Sandbox 120 / 60 Spielminuten | `S:shared/BanditsNPCBear.lua:168-169`; `B.WaitLeft` `Rules.lua:120` | optional "bereit / in 40 min" |
| Mode / Rename / Call Drossel | 500 ms | `Follow.lua:53-77` | nur Spam-Schutz |

### 3.7 Zaehmung, Vertrauen, Beduerfnisse
- Zaehmung: am eigenen Baeren immer 100 (`Rules.lua:71-74`); am zahmen Baeren gibt Fuettern/Streicheln keine Punkte mehr, nur die
  Abklingzeit (`Rules.lua:85-99`, `:111-113`).
- Vertrauen/Laune (Kevin 08.11., `ENTSCHEIDUNGEN.md:107-110`): **keine Daten** -> Platz vorsehen, nichts anzeigen.
- Hunger/Durst/Muedigkeit: **keine Daten** (Art ohne `hungerMultiplier`, `S:shared/BanditsNPCBearDefs.lua:109-110`; F3) -> Platz
  vorsehen, nichts Falsches.

### 3.8 Mehrere eigene Baeren
Sandbox `BearMaxPerPlayer` 1 (bis 4, `S:shared/BanditsNPCBear.lua:158`); `me.bears` zaehlt (`Registry.lua:401-402`). Das Fenster
braucht bei > 1 eine Auswahl (Frage F-c).

---

## 4. Sitzen und frei herumlaufen (Auftrag d)

### 4.1 Wie die Test-Mod heute sitzen laesst (gespielt: Kevin 11.11. ~15:40 "der sitz schonmal viel besser", `ENTSCHEIDUNGEN.md:310-312`)

| Teil | Fundstelle |
|---|---|
| Befehl `NCBear_Sit(sek)` -> `F.Calm.Sit` | `T:lua/client/NCBearBench.lua:76-81`; `T:lua/shared/NCBearFight.lua:1925-1945` (Stand `:1947-1962`) |
| Ablauf: Halten (`setBlock` = setBlockMovement + stopAllMovementNow), `NCBearAct = "sitdown"`; nach `NCBearDone == "true"` ODER Dauer + 1 s Frist -> `"sit"` (Schleife) bis Ende -> `"standup"` -> Ende: Variable weg, Halten aus | `NCBearFight.lua:1491-1513` (calmTo/calmStart/calmEnd), `:1629-1660`, `F.FRIST` `:61`, Clip-Tabelle `:54-56` |
| Knoten (Bedingung `NCBearAct` STRING, idle) | `T:AnimSets/buck/idle/NCBear_SitDown.xml` (nicht geloopt, Ende -> `NCBearDone=true`), `NCBear_Sit.xml` (Schleife), `NCBear_StandUp.xml` (Ende -> `NCBearDone=true`) |
| Clips | **beide Koerper**: `S:../models_X/Skinned/NCBearCub.glb` (= Test-Mod, byte-gleich) und `T:models_X/Skinned/NCBear.glb` (grosser Koerper, Altlast 14): je `NCBear_SitDown` 1,6 s, `NCBear_Sit` 4,0 s, `NCBear_StandUp` 1,3 s (selbst aus dem glTF-Kopf gelesen) |
| Einschraenkung | NUR SP, nur Art `"bear"`, nur mit `NCBear_Fight` an (`NCBearFight.lua:1-5`, `:1899-1905`) -- nicht fuer unseren Baeren nutzbar; nur der Weg wird uebernommen |

### 4.2 Belegter Weg fuer den gezaehmten Baeren

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Anim-Variable setzen / loeschen | `animal:setVariable("NCBearAct", "sitdown")` (Text, Text) / `animal:clearVariable("NCBearAct")` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:43` (`self.animal:setVariable("idleAction", "petting")`), `:48`; im Staging schon `S:shared/TimedActions/BanditsNPCBearFeedAction.lua:62`, `:73` (`B.ACT = "NCBearAct"`, `S:shared/BanditsNPCBear.lua:42`) | beide | **BELEGT** |
| Ende eines Clips lesen | `animal:getVariableString("NCBearDone") == "true"` | Methode/Typ `V:client/ISUI/ISWorldObjectContextMenu.lua:2660` (am Spieler; die Test-Mod zitiert noch `:2624` aus 42.21), am Tier gespielt `T:lua/shared/NCBearFight.lua:1629`; am Tier auch `V:client/DebugUIs/DebugMenu/Anims/ISAnimDebugMonitor.lua:289` | beide | BELEGT |
| still halten | `animal:getBehavior():setBlockMovement(true)` je Takt neu (`B.Hold`) | `V:shared/TimedActions/Animals/ISPetAnimal.lua:36`, `V:client/ISUI/Animal/ISAnimalContextMenu.lua:89`; `S:server/BanditsNPCBearWorld.lua:823-838` (Engine loest die Sperre von selbst, deshalb je Takt) | S | BELEGT |
| Bewegung sofort stoppen | `animal:stopAllMovementNow()` | `ISAnimalContextMenu.lua:760` | S | BELEGT (setBlockMovement(true) ruft es laut Jar schon, `World.lua:821`) |
| zur Kamera/zum Besitzer drehen (optional) | `animal:setDir(IsoDirections.SE)` / `faceThisObject` | `V:shared/Definitions/animal/ButcheringUtil.lua:574`; `S:...FeedAction.lua:49` | beide | BELEGT |

**Luecken und Regeln fuer den Bau:**
1. **Knoten nicht im Staging, Uebernahme sperrt sie:** die drei Sitz-Knoten liegen nur in `T:AnimSets/buck/idle/`. Das Uebernahme-Skript
   kopiert nur `NCBear_Eat.xml` und meldet alle anderen als "Knoten des Erwachsenen, bleibt bis B5a" (`baer/tools/baer_uebernahme.py:30-32`,
   `:127-135` `ANIMSET_OK`, `:531-534`; `baer/NAEHTE.md:46` Naht 9). Fuer F1: `NCBear_SitDown.xml`, `NCBear_Sit.xml`, `NCBear_StandUp.xml`
   byte-gleich ins Staging und `ANIMSET_OK` um genau diese drei erweitern (Kampf-Knoten bleiben gesperrt); Naht 9 nachziehen. Das Skript
   prueft schon "genau eine Bedingung NCBearAct" und "Clip im GLB des Jungen" (`:37-40`, `:631`, `:656-658`).
2. **MP: `NCBearAct` wird NICHT uebertragen** (NUR JAR 7: das Tierpaket traegt nur OnFloor/Dead/Running/Attacking und `idleAction`).
   Lesart schon in `baer/begleiter/PLAN.md:224-225` ("Die Animations-Variablen muss jeder Client an seiner Kopie setzen") und
   `forschung_bestand.md:567-568`. Folge: der Schreiber haelt das Tier (Bewegung ist Server-Sache); **jeder Client setzt `NCBearAct` an
   SEINER Kopie aus der Sicht** (Modus "sit"), z. B. im Listenbau des Hud, der im MP schon die Groessen-Probe macht
   (`S:client/ISUI/BanditsNPCBearHud.lua:459-477`, 1 x je s). Im SP ist Schreiber = Client (ein Objekt).
3. **`idleAction` NICHT benutzen** (obwohl es uebertragen wird): die Engine schreibt und loescht es selbst (NUR JAR
   `dec/BaseAnimalBehavior.java:150-155`, `:263-288` inkl. eigenem "sit"; `dec/AnimalData.java:936-1019`), und Vanillas "sit" spielt
   `DeerStag_*Sitting*`-Clips, die unsere GLBs nicht haben (GLB-Liste oben; `ENTSCHEIDUNGEN.md:64`).
4. Knoten spielen nur im Zustand idle (`forschung_bestand.md:571-572`): waehrend des Sitzens jeden Takt halten; Laerm-Flucht des
   zahmen Baeren faengt die Laerm-Wache schon ab (`Server.lua:751`, `S:server/BanditsNPCBearGuard.lua:54-`).
5. Zombie-Vorrang: `B.GuardStep` laeuft vor allem anderen (`Server.lua:774`) -> beim Verstecken `NCBearAct` loeschen (sonst setzt er sich
   am Versteck hin), danach wieder hinsetzen.
6. Koerper-Tausch/Call/Aussteigen erzeugen einen neuen Koerper ohne Variable (`B.PlaceCub` `Ride.lua:72-112`, Sitzung geleert `:53-58`)
   -> wieder "sitdown".
7. Aufstehen vor dem Losgehen: nach einem Wechsel weg von "sit" ~1,3 s (+ Frist) halten, sonst rutscht er im Aufsteh-Clip.

### 4.3 Frei herumlaufen

| Bedarf | Aufruf | Fundstelle | Seite | Urteil |
|---|---|---|---|---|
| Mittelpunkt | Heimat `rec.hx/hy/hz` (gibt es; "stay" setzt sie auf die jetzige Kachel) | `S:server/BanditsNPCBearFollow.lua:95-97` | S | vorhanden |
| Radius | neue Sandbox-Option (Vorgabe laut Auftrag 8, s. Widerspruch) | Muster `B.OPTS` `S:shared/BanditsNPCBear.lua:152-183` | S | Name frei (`BearWanderRadius`, Abschnitt 8) |
| Zufallspunkt im Kreis | `ZombRandFloat(0, 2 * math.pi)`, `ZombRandFloat(rmin, R)` | `S:server/BanditsNPCBearWorld.lua:175-179` (Form `B:server/BanditServerSpawner.lua:216-222`); `ZombRand(n)` `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25` | S | BELEGT |
| Kachel ok | `getCell():getGridSquare(x, y, z)`; Regeln wie `spotOk` (fester Boden, kein Wasser, kein Baum, `isFree(false)`, kein Fahrzeug) + gleicher Raum wie der Mittelpunkt (`sq:getRoom()`) | `V:server/Animal/ISPickDungCursor.lua:104`; `S:server/BanditsNPCBearWorld.lua:227-235`, `:291-301` (Raum: `V:shared/Util/AdjacentFreeTileFinder.lua:240`) | S | BELEGT; Deckel `B.CFG.tries` 8 Versuche (`S:shared/BanditsNPCBear.lua:56`) |
| hingehen | `B.MoveTo(rec, a, x, y, z, { walk = true, minMs = ... })` -> `setVariable("animalRunning", false)` + `pathToLocation(x, y, z)` | `S:server/BanditsNPCBearWorld.lua:857-917` (`:884-886`) | S | **ERLAUBT** (Kevins Wort je Methode: `ENTSCHEIDUNGEN.md:43`, `:282`; einzige Stelle, Uebernahme-Regel `baer_uebernahme.py:295-302`) |
| zurueckholen | wie Regel 8 "home" (`farFromHome` mit `c.homeR`), aber gehend | `S:shared/BanditsNPCBearRules.lua:266-271`, `:316-319` | S | vorhanden |
| Takt | Hirn-Takt 1,5 s (`S:shared/BanditsNPCBear.lua:46`, `Server.lua:1030-1042`); neues Ziel erst, wenn angekommen/still + Pause (Vorschlag 8-20 s Zufall) | -- | S | Deckel: ein Ziel je Baer in der Sitzung, keine wachsende Tabelle |
| Engine-Wandern | `wanderMul = 600` (`S:shared/BanditsNPCBearDefs.lua:113`); Wurf +-8 Kacheln je Achse um das TIER (NUR JAR, `forschung_b1b.md:120` aus `dec/BaseAnimalBehavior.java:165-225`) | -- | S | bei R = 8 oft draussen -> zwischen eigenen Wegen halten (`B.Hold`) ODER wandern lassen und zurueckholen |

**Widerspruch (Frage F-b):** Das heutige "Bleiben" IST schon "frei in 12 Kacheln": Regel 9 "free" laesst die Engine wandern
(`Rules.lua:321-322`), Regel 8 holt ab `stayR` 12 zurueck (`S:shared/BanditsNPCBear.lua:84-86`), Kevin bestaetigte "Bleiben-Radius 12"
(`ENTSCHEIDUNGEN.md:284`); der Tooltip sagt "It stays around this spot." (`Client.lua:114`). "Frei" mit Vorgabe 8 waere also ENGER.
Empfehlung: **Bleiben = wirklich stehen** (Halten je Takt an der Heimat, wie Folgen-"hold") und **Frei = das heutige Verhalten mit eigenem
Radius (Vorgabe 12, wie Kevins Bleiben-Radius) plus eigene Spazierziele**; oder Vorgabe 8 lassen und Bleiben unveraendert -- Kevin
entscheidet morgens.

**Beacon-Naht (nur dokumentieren, Auftrag):** NPC Crews Basisflaeche: `BanditsNPC.Base.Zone(site)` / `Base.SiteNear`
(`NC:shared/BanditsNPCForestZones.lua:687-694`: *"ohne das Modul, z. B. auf dem dedizierten Server, nein"*), Liste der Standorte
`BanditsNPC.BeaconRegistry.Sites()` (`NC:shared/BanditsNPCHaul.lua:263-272`). Unser Frei-Takt laeuft beim Schreiber -> im MP auf dem
Server; ob `Base.Zone` dort da ist, ist laut NC selbst fraglich -> die Naht muss das spaeter klaeren (Existenz-Riegel, Rueckfall Kreis).

---

## 5. Unstuck und C1 (Auftrag e)

### 5.1 Unstuck = der vorhandene Call-to-me-Weg

| Schritt | Fundstelle |
|---|---|
| Bitte "Call" mit Besitz/Zustand (auch **missing**)/ride/Auto/Abklingzeit/freie Kachel | `S:server/BanditsNPCBearRide.lua:300-336` |
| freie STEHBARE Kachel neben dem Spieler: Ringe 1..3, fester Boden, kein Wasser, kein Baum, `isFree(false)`, kein Fahrzeug, gleicher Raum, Weg zum Spieler ohne Wand/Tuer/Fenster (`isBlockedTo`), Startpunkt wandert je Generation | `S:server/BanditsNPCBearWorld.lua:215-235`, `:255-305` (Belege dort: `V:client/ISUI/ISWorldObjectContextMenu.lua:687-688`, `V:server/BuildingObjects/ISBuildUtil.lua:34`, `V:shared/Foraging/ISForageAction.lua:7`, `V:shared/Util/AdjacentFreeTileFinder.lua:240`) |
| frisch erzeugter Koerper wartet ein Bild | `Ride.lua:337-348` |
| alter Koerper geladen, aber ungebunden: erst ein Suchlauf | `Ride.lua:350-361` |
| neuer Koerper (gen + 1, Spiegel, Groesse, Leben, st missing -> tame) | `B.PlaceCub` `Ride.lua:72-112` -> `B.CreateCub` `World.lua:485-507` (`addAnimal` + `addToWorld`, `V:server/ClientCommands.lua:809-810`) |
| alter Koerper weg (falls geladen) | `B.RemoveCub` `World.lua:517-525` (am Server `removeAnimal(getOnlineID())`, `V:shared/Definitions/animal/ButcheringUtil.lua:612-614`) |
| alter Koerper NICHT geladen | taucht spaeter mit kleinerer Generation auf -> "stale" -> nie gebunden, unbeobachtet entfernt (`World.lua:767-800`, `:634-641`, `vanishKeep` 25 `S:shared/BanditsNPCBear.lua:52`) |
| danach Folgen, Meldung, Abklingzeit | `Ride.lua:370-374` |
| MP | nur der Server erzeugt/entfernt (`World.lua:10-12`); Client schickt nur die Bitte (Rolle user) |

Vergleich NPC Crew (gelernt, nicht kopiert): `P.Unstuck` nimmt `AdjacentFreeTileFinder.Find(sq, player)` mit Rueckfall auf die Kachel
des Spielers (`NC:client/BanditsNPCPersistence.lua:9703-9707`), Teleport verweigert Kacheln ohne Boden (`:9426-9428`), Abklingzeit je
Figur, nur Sitzung (`:9433-9455`). Unser `B.SpotNear` ist strenger (nie die eigene Kachel, nie unstehbar) -- passt zu Kevins
"nie auf eine unstehbare" (`ENTSCHEIDUNGEN.md:68`).
"Auch wenn er liegt": ein Liegen/Downed gibt es noch nicht (B5a) -- heute ohne Bedeutung.
**Ergebnis:** Der Unstuck-Knopf im Fenster braucht KEINEN neuen Schreiber-Code: `B.Ask(player, "Call", { id = v.id })`.

### 5.2 C1: zahmer Eintrag ohne Koerper bekommt von selbst genau EINEN Koerper

Heutiger Weg (`S:server/BanditsNPCBearServer.lua`): `resolve` sammelt Eintraege ohne Objekt (`:797-818`) -> Suchlauf je 30 s fuer
Vermisste (`scanMs` 5 s x `missScanMul` 6, `S:shared/BanditsNPCBear.lua:46`, `:78`; `Server.lua:942-951`) -> nach 3 Fehlversuchen in
GELADENER Gegend `st = "missing"`, follow -> stay, Meldung (`countMisses` `:823-849`, `missScans` 3 `S:shared/BanditsNPCBear.lua:57`)
-> `missH` laeuft nur mit anwesendem Besitzer -> nach 24 Spielstunden `B.Close(rec, "lost")` (`:486-493`, `missingH` 24) = **verloren**.

Vorschlag (alles vorhandene Wege, kein neuer Engine-Aufruf):
1. Anschluss im Hirn-Takt direkt nach `countMisses` fuer jeden Eintrag mit `st == "missing"`, `ride == nil`, Besitzer anwesend (wie
   `missH`), `B.AreaLoaded(rec.x, rec.y)` (`World.lua:118-129`) und **in diesem Takt lief ein Suchlauf, der ihn nicht fand** ("erst
   suchen").
2. Wartefrist: mindestens 2 weitere vergebliche Vermissten-Suchlaeufe (~60 s Echtzeit) in geladener Gegend -- Tiere kommen nach den
   Kacheln ueber einen eigenen Lader zurueck, Dauer ungeprueft (`Server.lua:820-822`).
3. Kachel: `B.SpotNear(rec.x, rec.y, rec.z, B.CFG.callRing, rec.gen)` (an SEINER letzten Stelle, nicht beim Spieler -- Kevins
   "nichts holt ihn automatisch zum Spieler", `baer/begleiter/PLAN.md:210`; C1 hat Kevins Ja, `ENTSCHEIDUNGEN.md:335-336`).
4. `B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "heal")` -> gen + 1, st -> tame, `missH` 0, Spiegel sofort, Groesse/Leben
   (`Ride.lua:89-111`); Meldung `UI_BN_Bear_Note_Back` (gibt es, `Client.lua:56`).
5. Kein Doppel: taucht der alte Koerper doch noch auf, ist er "stale"/"dup" (kleinere Generation) -> nie gebunden, unbeobachtet entfernt
   (`World.lua:729-736`, `:767-800`, `:634-641`). **Restrisiko (wie Call seit B1c):** steht der Spieler naeher als 25 Kacheln, bleibt die
   alte Kopie sichtbar ohne Schild stehen, bis niemand mehr nah ist.
6. Deckel: hoechstens ein Versuch je Eintrag und Wartefrist; Fehlversuche gedrosselt mit Fehlerzeile wie `placeFail` (`Ride.lua:158-164`).
7. Absturz-/Lade-Faelle: `PlaceCub` schreibt den Spiegel im selben Aufruf (`Ride.lua:103-104`); das Ein-Bild-Fenster von `addToWorld`
   (gegen_bericht_b1e.md 4.2 b) bleibt wie bei Call/Aussteigen -- C1 deckt es jetzt selbst ab (der naechste Takt sieht wieder "missing").
Der Unstuck-Knopf wirkt fuer "missing" schon heute (5.1).

---

## 6. B1e-Reste (Auftrag f)

### 6.1 A1/B6: Texte sagen beim grossen Koerper "cub"

| Schluessel (EN heute) | Fundstelle | Eintrag bekannt? | Weg |
|---|---|---|---|
| `UI_BN_Bear_Why_Gone` "The cub is gone." | `S:server/BanditsNPCBearFollow.lua:223` (rec nil ODER missing), `:237` (rec da), `:261` (rec nil) | teils | bei vorhandenem rec `B.NoteBd(note, rec)` (`S:shared/BanditsNPCBear.lua:508-511`) |
| dto. | `S:server/BanditsNPCBearRide.lua:310` (nil), `:365` (rec da) | teils | dto. |
| dto. | `S:server/BanditsNPCBearRegistry.lua:500` (`B.Close` "lost", rec da) | ja | `tellKey` mit NoteBd |
| dto. | `S:server/BanditsNPCBearServer.lua:158`, `:169` (Fuettern/Streicheln-Abschluss, kein rec) | nein | Grundtext bleibt (meist Junges) |
| dto. (Client-Menue) | `S:shared/BanditsNPCBearRules.lua:142`, `:161` -> `U.WhyText` (`Client.lua:230-241`) | Menue kennt `v.bd` | `U.WhyText` um `bd` erweitern (heute ohne) |
| `UI_BN_Bear_Note_Dead` "The bear cub is dead." | `Registry.lua:492` (zahm, Sperrfrist 0) | ja | NoteBd |
| dto. | `Registry.lua:495` (ungezaehmt) | -- | immer Junges, bleibt |
| `UI_BN_Bear_Menu_Hold` / `_HoldTip` "...for the cub" | `S:client/BanditsNPCBearMenu.lua:422`, `:428` | `holdWanted` (`:408-419`) kennt das Junge `c` (mit `c.bd`), gibt aber nur true/false zurueck | `holdWanted` gibt `c` zurueck, dann `U.TB(key, c.bd)` (`Client.lua:215-220`) |

Big-Fassungen `..Big` in `U.EN` (`Client.lua:166-181`, Muster) UND allen 7 `UI.json`; `U.TB`/`U.NoteText` waehlen sie nur, wenn `U.EN`
die Big-Fassung kennt (`Client.lua:216`, `:261`). CN: die noetigen Zeichen (z. B. 熊) gibt es in Vanilla-CN (geprueft); Pruefer
`_arbeit/baer_zaehmen/attrappe/ober/texte_pruefen.py`.

### 6.2 A5: 288-px-Bilder gegen den Texturdeckel 256 -- **erledigt, kein Handlungsbedarf**

| Glied | Beleg | Art |
|---|---|---|
| Lua `getTexture(path)` = `Texture.getSharedTexture(String)` | `J:jar_f1/GlobalObject.txt:10024-10028` | NUR JAR |
| `getSharedTexture(String)` laedt mit Flags `0 | (useCompression ? 4 : 0)` | `J:jar_f1/Texture.txt:962-977` | NUR JAR |
| die Flags gehen 1:1 in die TextureID | `J:jar_f1/Texture.txt:248-257` (aus Datei), `:200-245` (ohne Parameter: nur 4) | NUR JAR |
| verkleinert wird NUR bei `flags & 384` (128 = "Maximale Texturgroesse", 256 = Fahrzeug-Option) | `J:jar_f1/TextureID.txt:1115-1135ff` (limitMaxSize), `J:jar_f1/Core.txt:9158-9175` | NUR JAR |
| Vanillas Option sagt selbst "non-vehicle-**model** textures" | `V:shared/Translate/EN/UI.json:64` | Lua/Text |
| Vanilla zeigt im Spiel UI-Bilder > 256 px per `getTexture` | `V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191` (`media/ui/defense/*.png`, 123 x 302 px, selbst aus dem PNG-Kopf; 442 UI-Bilder > 256 px in `media/ui`) | Lua |
Die Rucksack-Lehre "Deckel 256" gilt fuer Kleidungs-/Modell-Texturen (Flag 128), nicht fuer `media/ui`. Unsere 9 Bilder (96-288 px)
bleiben unveraendert; `DrawTextureAngle` zeichnet den 288er Pfeil in voller Groesse.

### 6.3 C3/B7: Klickflaeche der Markierung

Fakten: das Element ist 45 x f px gross (`S:client/ISUI/BanditsNPCBearMarker.lua:40`, `:270-294`; 4K: 90 px), verschluckt Klicks
(Vanilla-Vorgabe `wantMouseEvents = true`, `V:client/ISUI/ISUIElement.lua:1998`, `:1004`), solange das wilde Junge "new" ist plus 60 s
ab dem ersten "shy" (`Marker.lua:311-320`); Doppelklick blendet aus (`:184-191`).
Klein und sicher waere nur: `el:setWantMouseEvents(false)` (`ISUIElement.lua:1837-1844`; Aufrufer
`V:client/ISUI/Gamepad/ISControllerBindingsEditorPanel.lua:279`) -- dann geht jeder Klick in die Welt, aber der Doppelklick zum
Ausblenden faellt weg (Kevins Funktion). **Empfehlung: in F1 nichts aendern**, Kevins Frage 6 (gegen_bericht_b1e.md:170) steht offen.

---

## 7. NUR mit Jar belegt (getrennt; keiner davon ist ein neuer Engine-AUFRUF, nur Lesarten)

| Lesart | Fundstelle | wofuer |
|---|---|---|
| `OnKeyPressed` feuert beim LOSLASSEN, nicht waehrend ein Textfeld tippt (`Core.currentTextEntryBox.isDoingTextEntry`), und nicht, wenn eine UI die Taste verbraucht hat (`UIManager.onKeyRelease` -> true) | `J:jar_f1/GameKeyboard.txt:47-75` (Textfeld), `:150-154`, `:157-173` (UI), `:209-221` (Ereignis) | V im Namensfeld oeffnet nichts; Fenster mit `isKeyConsumed` schliesst ohne Wieder-Oeffnen |
| `getUseableAnimal` = naechstes Tier in den Kacheln x-2..x+1, y-2..y+1 (zur Kachel vor dem Spieler) | `dec/IsoPlayer.java:8870-8900` | wann Vanillas V-Radial am Baeren aufgeht |
| Textur-Deckel nur bei Flag 128/256; `getTexture` laedt mit 0/4 | 6.2 | A5 |
| Tierpaket uebertraegt nur OnFloor/Dead/Running/Attacking (+ Text `idleAction`) | `dec_b1b/AnimalStateVariables.java:8-19`; `dec_b1b/AnimalPacket.java:36`, `:101-103`, `:176-178` | `NCBearAct` im MP je Client setzen |
| Engine schreibt/loescht `idleAction` selbst (inkl. "sit", "eat", "idleN") | `dec/BaseAnimalBehavior.java:150-155`, `:263-288`, `:495-539`; `dec/AnimalData.java:936-1019`, `:1230-1261`, `:1656` | `idleAction` nicht fuer unser Sitzen |
| Engine-Wandern +-8 je Achse um das Tier | `forschung_b1b.md:120` (`dec/BaseAnimalBehavior.java:165-225`) | Frei-Radius |

---

## 8. Kollisionsprobe neuer Namen (11.11. nachts; NC = `42/media/lua` + `_docs/landkarte_index.txt`, dazu Vanilla `media/lua`, Bandits)

| Name | NC lua | NC Landkarte | Vanilla | Bandits |
|---|---|---|---|---|
| `"Bear window"` (Tastenname) / `UI_optionscreen_binding_Bear window` | 0 | 0 | 0 | 0 |
| `"[NPC Crew Bear]"` / `"NPC Crew Bear"` | 0 | 0 | 0 | 0 |
| `BanditsNPCBearWindow` (Datei, Klasse, layout.ini-Name) | 0 | 0 | 0 | 0 |
| `UI_BN_Bear_Win_` (Text-Praefix), `UI_BN_Bear_Stage_Cub` | 0 | 0 | -- | -- |
| `BearWanderRadius`, `BearPassive` (Sandbox) | 0 | 0 | -- | -- |
| `NCBear_CubWin` (Bench) | 0 | 0 | -- | -- |
| `NPCCrewBear.ini` / `BanditsNPCBear.ini` (Client-Datei, falls gebraucht) | 0 | 0 | -- | -- |
Achtung beim Greppen: `UI_BN_Bear` trifft NC `UI_BN_Beard_None` -- nur mit Unterstrich `UI_BN_Bear_` suchen (`baer_uebernahme.py:116`).

---

## 9. Naehte und Uebernahme-Folgen (fuer `baer/NAEHTE.md` und `baer_uebernahme.py`)

1. **Tastenzeile in Vanillas `keyBinding`** (Lua-Tabelle, Dateiebene client/): Doppel-Riegel (Test-Mod + NPC Crew gleichzeitig); Name
   ewig stabil; Beschriftung `UI_optionscreen_binding_*` -> **TEXT_NS-Ausnahme fuer UI.json** im Skript.
2. **Vorfahrt V gegen NPC Crew "Talk to NPC"**: nur lesen (`BanditsNPC.Interact.FindTarget`), Existenz-Riegel; keine NC-Datei.
3. **Vanilla-Tier-Radial auf V**: Weg (b) ruft nur Vanilla-Aufrufe; Weg (c) waere ein Funktions-Aufsatz in `OnGameBoot` (eigene Naht).
4. **Sitz-Knoten** `AnimSets/buck/idle/NCBear_SitDown|Sit|StandUp.xml`: Naht 9 + `ANIMSET_OK` erweitern; der grosse Koerper haengt
   weiter am Modell der Test-Mod (Altlast 14/26, unveraendert).
5. **Beacon-Basisflaeche** fuer "Frei" nur dokumentieren (4.3).
6. **layout.ini-Name** `BanditsNPCBearWindow` (gemeinsame Vanilla-Datei; frei).
7. Falls Einstellungen je Baer beim Client (Namensschild): eigene Datei ueber `getFileWriter(name, true, false)` / `getFileReader(name, true)`
   (Vanilla `V:client/ISUI/ISLayoutManager.lua:127`, `:172`; NC-Lehre `NC:client/BanditsNPCClientCfg.lua:1-60`: MP-Clients schreiben
   ihre globale ModData nie auf die Platte) -> Dateiname frei (Abschnitt 8).
8. Neue Sandbox-Option(en) -> `sandbox-options.txt` + 7 x `Sandbox.json` (Muster vorhanden).

---

## 10. Offene Fragen (mit empfohlenem Weg; Nachtschicht: so bauen, morgens Kevin zeigen)

- **F-a Komm her vs. Unstuck:** Beides auf `Call` waeren zwei gleiche Knoepfe. Empfehlung: **"Komm her" = gehender Ruf** (der Baer
  laeuft ueber `B.MoveTo` zum Spieler und bleibt dort -- kein Versetzen, wie Kevins Q-Ruf-Idee `ENTSCHEIDUNGEN.md:97`; grau wenn nicht
  geladen oder weiter als `BearFollowMaxDistance`), **"Unstuck" = Call to me** (Versetzen, 5-min-Abklingzeit, Kevins Freigabe Nr. 5
  `ENTSCHEIDUNGEN.md:280`). Alternative laut Auftrag: ein Knopf "Komm her (Call to me)".
- **F-b Bleiben vs. Frei** (4.3): Empfehlung Bleiben = stehen (halten), Frei = heutiges Bleiben mit Radius-Vorgabe 12.
- **F-c Mehrere eigene Baeren** (bis 4): Empfehlung: Fenster zeigt den naechsten, Pfeile < > wenn mehr als einer.
- **F-d Namensschild je Baer:** Empfehlung: Client-Datei, Schluessel = `u` des Baeren (Deckel 64 Eintraege), die globale Option
  `TagShow` (`S:client/BanditsNPCBearOptions.lua:63`) bleibt der Hauptschalter. Alternative: nur die globale Option.
- **F-e Vanilla-V-Radial am eigenen Baeren** inkl. "Toeten": Empfehlung F1 = Weg (b); Kevin fragen, ob wir das Radial fuer den eigenen
  Baeren ganz unterdruecken (Weg c, loest "Toeten").
- **F-f 3D-Bild des Baeren im Fenster:** Empfehlung nicht in F1 (Symbol 1 reicht; Risiko 2.1).
- **F-g Passiv beim Jungen:** Schalter zeigen, Tooltip "Jungtier kaempft nie; wirkt ab Halbstark mit dem Kampf (B5a)".
- **F-h Abschnitt in den Tastenbelegungen:** eigener Abschnitt "NPC Crew Bear" (Empfehlung; unabhaengig von der Ladereihenfolge) statt
  unter "NPC Crew" (dort haengt es an der Dateireihenfolge, Ueberschrift kommt aus `NC Interact.lua:7451`).
- **F-i C1-Wartefrist:** 2 weitere vergebliche Suchlaeufe (~60 s) -- oder laenger?
- **F-j Fenster schliesst sich bei Abstand?** Vanillas Tier-Info schliesst ab 5 Kacheln (`ISAnimalUI.lua:19-20`); unser Fenster soll
  auch fuer einen fernen/nicht geladenen Baeren gehen (Unstuck!) -> Empfehlung: NIE wegen Abstand schliessen.

---

## 11. Rote Linien, MP, Leistung (kurz)

- **Kein Gegenstand verloren/verdoppelt:** das Fenster nimmt/gibt nichts.
- **Baer nie verloren/verdoppelt:** Unstuck/C1 nur ueber `B.PlaceCub` (gen + 1) + Doppel-Riegel der Heilung; Restrisiko 5.2 Nr. 5.
- **Kein Kick:** nur `sendClientCommand` (LoginOnServer), Rolle user; kein `transmitModData` am Tier.
- **Nichts haengt:** Sitz-Ablauf mit Frist (Clipdauer + 1 s wie `T:lua/shared/NCBearFight.lua:61`); Hello mit Rueckfall (`Client.lua:394-410`).
- **NPC-Crew-Figuren:** werden nicht beruehrt; V-Vorfahrt laesst NPC Crew den Vortritt.
- **SP-Test** `not isClient() and not isServer()` (`S:shared/BanditsNPCBear.lua:195-197`); Bench `NCBear_CubWin()` nur SP wie die
  anderen Bench-Befehle (`S:client/NCBearBenchCub.lua:5`). Fuer C1 hilft ein Bench-Griff "Koerper weg, Eintrag bleibt" (heute gibt es
  nur `NCBear_CubForget` = Eintrag weg, Spiegel bleibt, `NCBearBenchCub.lua:623-641`).
- **Nichts Teures je Bild:** Fenster liest die Sicht hoechstens ein paar Mal je Sekunde neu und zeichnet nur fertige Felder; keine Suche,
  kein `getText` je Bild (Muster `S:client/ISUI/BanditsNPCBearHud.lua:30-37`).
- **localcount heute:** groesste Funktion Hud 49 aktiv / 60 insgesamt (`localcount.py`) -- das Fenster gehoert in eine NEUE Datei
  (`client/ISUI/BanditsNPCBearWindow.lua`), ggf. Taste getrennt.
