# Lauf baer-f1: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (67 Dateien laut
`staging_dateien.txt`, davon F1: 7 neu, 30 geaendert), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt`.
Gelesen gegen Vanilla 42.22.2 (`media/lua`, `media/ui`, Translate), Bandits 42.22 + common, NPC Crew v3.14.74 (`42/media/lua`, Landkarte),
Test-Mod NCBearTest (alles nur gelesen). **Geaendert: nur diese Datei.** Meine Laeufe und Ausgaben liegen im Scratchpad
(`C:/Users/Kevin/AppData/Local/Temp/claude/086a7114045651dc/8f80868b-c5cd-4de5-ade1-25f74fc113d4/scratchpad/pa/`: Diffs, Aufruf-Liste
`calls.txt`, Trockenlaeufe, Probe `probe/`, Attrappen-Ausgaben `att/`, eigene Werkzeuge `tools/calls.py`, `tools/texte.py`). Kein git, kein Spiel,
nichts nach Test-Mod/NPC Crew/Vanilla/Bandits geschrieben.

## 0. Ergebnis

| Pruefung | Ergebnis (selbst gelaufen) |
|---|---|
| Staging gegen Test-Mod (MD5 jeder Datei) | 67 Dateien, jede MD5 = Spalte in `staging_dateien.txt`, Zustand je Datei stimmt (7 neu / 30 ueberschreibt / 30 gleich); die 30 Ziele "ueberschreibt" tragen in der Test-Mod den Stempel 11.11. 18:22 (B1e-Einbau) |
| Test-Mod seit dem Zusammenbau | **6 neue Dateien** vom Lauf baer-gen-gross (12.11. 01:02: `NCBearBenchGen.lua`, `NCBearBenchGenDefs.lua`, `NCBearBenchGen.txt`, `NCBearGen.glb`, `NCBearGen.png`, `NCBearGenFoto.png`) -- keine davon ist ein Staging-Ziel (A7) |
| Engine-Aufrufe (jede Zeile der 7 neuen Dateien + jede hinzugefuegte Zeile der 15 geaenderten Lua-Dateien, eigenes Werkzeug `calls.py`) | 80 Aufruf-Namen: 66 Engine-/Vanilla-Lua-Aufrufe, **alle mit echtem Vanilla- oder Bandits-Vorkommen**; 11 eigene Methoden, 2 eigene Helfer (`U.WinRect/WinFrame`), 1 NPC-Crew-Lesung (`BanditsNPC.Interact.FindTarget`, nur lesend, hinter Existenz-Riegel). Die genannten Fundstellen je Aufruf selbst nachgelesen (Tabelle 2): gleiche Argumenttypen, Seite passt. **Jar-only: keiner.** `pathToLocation`/`animalRunning` nur in `B.MoveTo` (Kevins Wort). Kein `pcall`, kein `next(`, kein `getVariableString` |
| Taste | einstellbar (Vanillas `keyBinding`, Abschnitt "[NPC Crew Bear]", Zeile "Bear window", Vorgabe V); **absichtlich mehrfach belegt**: V liegt auch auf Vanillas Fahrzeug-Radial (`V:shared/keyBinding.lua:130-132`), Tier-Radial (`:185-187`) und NPC Crews "Talk to NPC" (`NC:client/BanditsNPCInteract.lua:7462`); Bandits benutzt V nicht (G = POSTS, `B:client/BanditModOptions.lua:14`); NPC Crews andere Tasten F6/F7/F8/Num0. Vorfahrt im Code richtig (Key.lua:65-82); Restpunkte A2 |
| Alte NCBear*-Dateien | keine im Staging ausser unserer Bench; Test-Mod-Altdateien unveraendert (Stempel 07./08.11.); kein neuer Code ruft oder aendert sie (Pose.lua setzt `NCBearAct` nur an `ncbearcub`/`ncbeargrown`, `NCBearFight.lua:1787` fuehrt nur `bear`) |
| Testbefehle / Werte-setzende Knoepfe ausserhalb der Bench | **0**. Fenster-Knoepfe sind nur Bitten (Mode/Come/Call/Passive/Rename) + Client-Einstellung (Name tag); neue Bench-Befehle `NCBear_CubWin`/`_CubBodyGone`/`_CubView` je SP-Riegel (`NCBearBenchCub.lua:994-997`, `ready()`, `:1034-1036`) |
| Texte 7 Sprachen (eigenes Werkzeug `texte.py`) | UI.json 274 / Sandbox.json 62 je Sprache; +117 / +2 je Sprache, **0 alte Schluessel geaendert oder entfernt**; Paritaet, Platzhalter, `%%`, kein `<`/`>`, sortiert, Round-Trip, kein BOM/CR: 0 Fehler; CN 455 Zeichen, **0 ausserhalb Vanilla-CN**; 245 Lua-Literale, 0 fehlen in EN; 27 Big-Fassungen, keine sagt "cub"; IG_UI.json EN 7 / sonst 4 = Altlast (3 Test-Schluessel, unveraendert) |
| Bildgroessen | 4 UI-Bilder 288 x 288 (unveraendert seit B1e) -- A5-Begruendung nachgeprueft, s. A8; Koerper-Textur 1024 wie seit B1a |
| Uebernahme Trockenlauf `--staging --vor-b5a` | **OK, 0 Fehler, 31 Warnungen** (27 Altlasten + 2 `ALT_DEFS` + Clip-Warnung + NC-Kommentar); gegen `trockenlauf_f1_vor_b5a.txt` nur die 3 neuen Gen-Altlasten anders (A7) |
| Uebernahme Trockenlauf ohne `--vor-b5a` | **29 Fehler = 27 Altlasten + 2 `ALT_DEFS`**, sonst nichts ("Erwartet rot ... sonst nichts") |
| Uebernahme Probe (Scratchpad) | **OK, 0 Fehler, 31 Warnungen**, 70 Dateien; Pruefer je kopierter Datei gruen (localcount hoechstens 77), luacheck_pz 0 + 3 erlaubt; Texte 3815 -> 4089 / 92 -> 153 / IG_UI neu 4, je Sprache sortiert, Round-Trip, **0 NC-Schluessel verloren oder geaendert**; Cheat-Pruefung Funde 0, 5 Ausnahmen; PlaceCub nur BodySwap/ReviveMissing/RideStep x2/HandleCall |
| Gesamt-Attrappe gegen MEINE Probe | 2329 / 0 |
| Vier Lua-Pruefer (32 Lua-Dateien des Stagings) | luacheck 32 / 0 failed; scopecheck 0; localcount hoechstens **51 aktiv** (Hud :1) / **77 insgesamt** (World :699); luacheck_pz 20 x W113 = bekannt (17 Bench, 3 Aktionsklassen Menu.lua :93/:104/:114); luac5.1 -p 0 Fehler; LF, ASCII, LF am Ende, kein BOM (Lua, JSON, txt) |
| Attrappen | alle wie gespeichert (Abschnitt 6) |
| Befunde | **0 blocker, 0 major, 8 minor** (A1-A8) |

## 1. Staging und Dateien
`find mod -type f` = 67; je Datei MD5 gegen Liste und Test-Mod: 0 Abweichungen. Diff Test-Mod -> Staging (geaenderte Zeilen): Client 131 (fast nur
Texte), Bench 79, Rules 57, Server 54, Follow 44, Menu 40, Registry 37, World 35, Grow 26, Hud 22, Heal 17, Bear 13, Options 10, Ride 3, Guard 2.
Neu: Key 97, Pose 126, Tags 104, WinData 448, WinParts 334, Window 697, Order 386 Zeilen.

## 2. Engine-Aufrufe (Fundstelle selbst nachgelesen, Datei:Zeile im heutigen Vanilla/Bandits)
| Aufruf (unsere Datei) | Fundstelle | nachgelesen / Seite |
|---|---|---|
| `table.insert(keyBinding, { value = T[, key = Keyboard.KEY_V] })` (Key) | V `shared/keyBinding.lua:6`, `:9`, `:130-132` | ja, Datei-Ebene Client |
| `Events.OnKeyPressed.Add`, `getCore():isKey(Text, key)` (Key, Window) | V `client/ISUI/FPS.lua:20`, `:9` | ja |
| `isKey(KeybindId.VEHICLE/ANIMAL_RADIAL_MENU, key)`, `getVehicleToInteractWith(p)`, `getAnimalToInteractWith(p)` | V `client/ISUI/ISUIHandler.lua:36-37`, `:43-44` | ja (gleiche Form) |
| `animal:isWild()`, `menu:undisplay()` | V `client/ISUI/Animal/ISAnimalContextMenu.lua:1171`, `:1164` | ja |
| `getPlayerRadialMenu(0)`, `menu:isReallyVisible()` | V `ISUIHandler.lua:91-92` | ja |
| `ISChat.focused` lesen | V `client/Chat/ISChat.lua:8` | ja |
| `getKeyName(getCore():getKey(Text))` | V `client/Tutorial/Tutorial1.lua:177` | ja |
| `getSpecificPlayer(0)`, `p:isDead()`, `p:getVehicle()`, `p:getX/getY()` (Client) | V `client/Farming/CFarmingSystem.lua:45`, `ISUIHandler.lua:42`, `client/ISUI/Hutch/ISHutchMenu.lua:8`, `client/Fishing/TensionUI.lua:11` | ja |
| `getTimestampMs()` | V `client/Foraging/ISBaseIcon.lua:485`, `server/Foraging/forageServer.lua:456` | ja |
| `ISPanel:derive`, `ISPanel:new(x, y, w, h)`, `o.moveWithMouse` | V `client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1`, `:243`, `:253`; Ziehen `ISPanel.lua:49-95` | ja |
| `o:setWantKeyEvents(true)` in `:new`, `isKeyConsumed`, `onKeyRelease` + `self:isVisible()` | V `client/ISUI/Crafting/ISHandcraftWindow.lua:386`, `:289-297`; `ISUIElement.lua:1828-1831` (Feld vor instantiate), instantiate setzt es | ja |
| `ISButton:derive`, geerbtes `:new`; `ISButton:new(x,y,w,h,"",Ziel,Rueckruf)`, `initialise`, `addChild`, `setImage`, `borderColor.a` | V `ISResizeableButton.lua:1`, `ISInventoryPane.lua:63`; `ISCollapsableWindow.lua:55-61` | ja; `addChild` instanziert selbst (`ISUIElement.lua:1451-1457`) |
| `b:forceImageSize(w, h)` | V `client/ISUI/ISInventoryPage.lua:1479` | ja |
| `b.enable`/`b.tooltip`; `ISButton.updateTooltip(self)`; `tooltipUI:getIsVisible/setVisible/removeFromUIManager` | V `Hutch/ISHutchUI.lua:619-623`; `ISButton.lua:45`, `:176`, `:316-346` | ja (Vanilla ruft `self:updateTooltip()` -- dieselbe Funktion) |
| `drawRect/drawRectBorder/drawText/drawTextRight/drawTextCentre/drawTextureScaled` | V `ISUIElement.lua:1191`, `:1219`, `:1293`, `:1306`, `:1280`, `:1032`; Aufrufer `ISAnimalUI.lua:58/64`, `ISToolTip.lua:120`, `ISChat.lua:418` | ja |
| `getTextManager():getFontHeight(UIFont.*)`, `MeasureStringX(Schrift, Text)` | V `ISAnimalUI.lua:4`, `ISAddSafeZoneUI.lua:8`, `ISAdminTicketsUI.lua:6`; `ISButton.lua:450` | ja |
| `getCore():getScreenWidth/Height()` | V `client/Challenge/WinterIsComing.lua:18` | ja |
| `addToUIManager/removeFromUIManager/setVisible/bringToTop/isReallyVisible/setX..setHeight/getX/getY` | V `ISUIElement.lua:1365`, `:1373`, `:657`, `:1548`, `:690`, `:195-245`; `ISLayoutManager.lua:55` | ja; Schliessen im prerender hat Vanilla-Vorbild (`DebugUIs/ISDebugAnimationTextUI.lua:45`) |
| `ISLayoutManager.RegisterWindow(Name, Klasse, Fenster)`, Save/Restore-Rueckruf | V `client/Chat/ISChat.lua:1172`; `ISLayoutManager.lua:6-13`, `:103`, `:111`; `visible` nie geschrieben (`:45-50`) | ja |
| `getFileReader(Name, true)`/`readLine`/`close`, `getFileWriter(Name, true, false)`/`write`/`close`, `string.trim` | V `ISLayoutManager.lua:127-136`, `:172-185` | ja |
| `getTexture(Pfad)` (eigene Bilder, `inventoryPanes/Button_Close.png`) | V `ISChat.lua:137`, `ISCollapsableWindow.lua:386` | ja |
| `HaloTextHelper.addText(Spieler, Text)` | V `client/Foraging/forageClient.lua:73` | ja |
| `animal:setVariable(Text, Text)`, `animal:clearVariable(Text)` (Pose, Client-Kopie) | V `shared/TimedActions/Animals/ISPetAnimal.lua:43`, `:48` (in `start()`/`stop()`, laeuft auch am MP-Client) | ja |
| `Events.OnTick/OnGameStart/OnResolutionChange.Add` | V `ISChat.lua:943`, `:1186`; `ISUI/PlayerData/ISPlayerData.lua:206` | ja |
| `PZAPI.ModOptions addComboBox/addItem(Name[, true])` (Options) | V `client/PZAPI/ModOptions.lua:121`, `:131` | ja |
| `menu:addOption(Text, Ziel, fn, Arg)` (Menu, Bench) | Form wie B1b-B1e (`S:client/BanditsNPCBearMenu.lua:241`) | ja |
| `isClient()` Dateikopf (Order) | V `server/Traps/STrapSystem.lua:1` | ja |
| `a:getX/getY()` am Tier (Order, World) | V `shared/Definitions/animal/ButcheringUtil.lua:575-576` | ja |
| `player:getVehicle()` / `player:getX/getY()` am Server | V `server/Vehicles/VehicleCommands.lua:11`; B `server/BanditServerSpawner.lua:179` | ja |
| `square:getX/getY/getZ()` am Server (Order) | genannt V `client/DebugUIs/DebugContextMenu.lua:636` (Client-Datei) | ja, Form gleich; Server-Vorbild waere besser -> A6 |
| `ZombRand(n)`, `ZombRandFloat(0, Zahl)`, `getCell():getGridSquare(x, y, z)`, `sq:getRoom()` (Order, World) | V `ISMilkAnimal.lua:25`; B `BanditServerSpawner.lua:217`, V `forageServer.lua:98`; V `server/Animal/ISPickDungCursor.lua:104`; V `shared/Util/AdjacentFreeTileFinder.lua:240` (am Server auch `server/Farming/SFarmingSystem.lua:162`) | ja |
| NPC Crew nur lesen: `BanditsNPC.Interact.KEYBIND`, `.FindTarget(p)` | NC `client/BanditsNPCInteract.lua:35`, `:41-76` (iteriert nur `getZombieList`, keine Wirkung) | ja |
| `%1%%` mit `getText(key, Wert)` | Vanilla tut es selbst: `IGUI_Generator_FuelAmount` "Fuel: %1%%" (`V:shared/Translate/EN/IG_UI.json:439`) | ja |

`attrappe/f1_ober/belege_f1.py` selbst gelaufen: 85 / 85 Belege, 83 `V:...:Zeile`-Fundstellen vorhanden, 0 Fehler; die alten `belege*.py` 0/112,
0/51, 0/89, 0/23, 0/53.

## 3. Regeln, Trennung, MP
- **SP/MP:** jeder Fenster-Befehl geht ueber `B.Ask` (`S:shared/BanditsNPCBear.lua:558-567`: MP `sendClientCommand`, SP `B.Handle` nur bei
  `not isClient()` und `not isServer()`); der Schreiber prueft Kennung (Text), Besitz (Kontoname), Zustand, Lage, Abklingzeit, Fahrzeug, Abstand
  (`Order.lua:239-315`, `Follow.lua:259-290`); `Passive.on` nur als Wahrheitswert. Neue Client-Befehle nur `Come`/`Passive` (Rolle user), kein neuer
  Server->Client-Befehl. Sitz-Treiber und Namensschild sind reine Client-Anzeige; der Server weiss nichts Falsches aus Client-Glauben.
- **Trennung:** KERN (`shared/`, `server/`) und OBERFLAECHE (`client/`) getrennt; die OBERFLAECHE ruft nur `B.*`-Lesehelfer und `B.Ask`;
  `B.PlaceCub(` nur aus BodySwap/ReviveMissing/RideStep/HandleCall (Skript-Regel + `xref_f1.py` 0 Luecken).
- **Rote Linien:** kein Gegenstand beruehrt; C1 mit drei Riegeln gegen ein Doppel (erst Suchlauf, AnimalID, MP erst nach `B._scanSeen`), hoechstens
  ein Koerper je Takt; "missing" schliesst nie mehr; alles Wachsende gedeckelt (`B._aidSeen` je Suchlauf neu, Tags 64, Pose <= Sicht, ein Fenster).
- **Teures je Bild:** Fenster-Modell nur bei neuer Sicht bzw. 1 x je s; je Bild nur Zeichnen aus fertigen Feldern; Pose 250 ms; Taste nur beim Loslassen.
- **Namen:** 15 neue Namen/Muster gegen NPC Crew `42/media/lua`, Landkarte, Vanilla, Bandits: 0 Treffer (u. a. "Bear window", "NPC Crew Bear",
  `BanditsNPCBearWindow`, `BanditsNPCBear.ini`, `BearRoamRadius`, `BanditsNPCBearWin*`, `WinSize`, `UI_BN_Bear_`). Die drei Sitz-Knoten
  `NCBear_SitDown|Sit|StandUp.xml` und `NCBearAct` tragen den alten Namen wie `NCBear_Eat.xml` seit B1a -- in NAEHTE.md :130-132 als B5a-Umbenennung
  gefuehrt (kein Befund).
- **Mehrfachrueckgaben:** keine `a, b = f and f()`-Falle in den neuen Dateien (grep).

## 4. Texte
Eigenes Werkzeug `tools/texte.py` (unabhaengig von den Bauer-Pruefern): siehe Tabelle 0. Dazu die Bauer-Pruefer: `texte_pruefen.py`, `_b1b`, `_b1c`,
`_b1d`, `_b1e`, `_f1` je "FEHLER gesamt: 0"; `texte_pruefen_f1.py --tmp <scratchpad>` 0 Fehler (Werkzeug-Gegenprobe 22 Dateien; ohne Ordner-Argument
bricht es mit IndexError ab -- nur Bedienung, kein Befund). Tasten-Beschriftungen in allen 7 Sprachen vorhanden ("NPC Crew: Bear" / "Bear window" ...).
B1e-Reste (4a): `Why_GoneBig` "The bear is gone.", `Note_DeadBig` "Your bear is dead.", `Menu_HoldBig`, `Menu_HoldTipBig` in 7 Sprachen, Server haengt
`B.NoteBd` an (Registry.lua:504/:512, Follow.lua:267/:281, Ride.lua:368), Menue ueber `U.TB(..., bd)` -- eine Luecke A3.

## 5. Uebernahme
Trockenlauf und Probe siehe Tabelle 0. `probe_regeln_f1.py` (mit TMP im Scratchpad) **10 von 10 wie erwartet**, `gegenprobe_f1.py` **27 von 27
erkannt**. Zusammengefuehrte Texte der Probe gegen NPC Crew und Staging geprueft (0 verloren/geaendert; EN IG_UI ohne die 3 Altlast-Schluessel wie
gewollt). Luecke der Tasten-Regel: A1.

## 6. Attrappen (selbst gelaufen, Ausgabe gegen den gespeicherten Stand)
kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1e_kern 153/0, **f1_kern 188/0** -- je byte-gleich mit `ergebnis_f1.txt` bzw. `ergebnis.txt`;
b1d_kern 162/0 (nur Pfad-Vorsatz der Fehlerzeile anders, bekannt); ober 116 + 117, b1b_ober 144 + 134, b1c_ober 155 + 142, b1d_ober 174 + 176,
b1e_ober 230 + 230, **f1_ober 359 + 359** (Kern-Attrappe + echter Kern), je 0 Fehler; **gesamt 2329 / 0** (byte-gleich mit `ergebnis.txt`, `***`
nur 18c/19f/20e); gesamt gegen meine Probe 2329 / 0; nach_b1e 31/0; pruef_b = `ergebnis_b1b_nach.txt`; pruef_b1b `run_nach` = `ergebnis_f1.txt`;
pruef_b1c = `ergebnis_nach.txt`; pruef_b1d 10/0 (3 Befunde) = `ergebnis_nach.txt`; pruef_b1e `run_nach` 25/0; pruef_b1e `run` 20/5 wie seit
`nachbesserung_b1e.md` :96 dokumentiert; `xref_f1.py` 0 Luecken, 3 Hinweise (byte-gleich mit `xref_f1.txt`).

## 7. Befunde

**A1 (minor, Uebernahme-Skript): Die Tasten-Regel sieht Tasten in UI-Fenstern nicht.** `baer/tools/baer_uebernahme.py:224-227` erkennt
`Events.OnKey*`, `isKeyDown(`, `GameKeyboard.`, `Keyboard.KEY_*` -- aber nicht `setWantKeyEvents(`, `onKeyRelease`/`isKeyConsumed`,
`getCore():isKey("Name", key)` und rohe Tastencodes. Selbst getestet: `o:setWantKeyEvents(true)`, `function Win:onKeyRelease(key) if key == 33 ...`,
`getCore():isKey("Spawn cub", key)`, `return key == 33` -> alle **nicht** erkannt. F1 bringt das erste Fenster mit Tasten
(`client/ISUI/BanditsNPCBearWindow.lua:289`, `:546-556`); eine versehentlich mitkopierte Bench-Taste in einem Fenster ginge heute durch. Vorschlag:
Regel um `setWantKeyEvents\s*\(`, `:isKey\s*\(` und `table\.insert\(\s*keyBinding` erweitern, die heutigen Stellen (Window.lua:289, Key.lua:40-41,
:56/:68/:72/:76, Window.lua:543) als `CHEAT_ALLOWED` mit Grund, Gegenprobe in `probe_regeln_f1.py` ergaenzen.

**A2 (minor, Taste): "eigener Baer" heisst im Code "irgendein Baer unserer Art".** `client/BanditsNPCBearKey.lua:75-81` setzt `ours = B.BodyKind(an) ~= nil`
-- wahr fuer JEDES `ncbearcub`/`ncbeargrown`, auch den gezaehmten Baeren eines anderen Spielers (MP) und das Junge im Zaehmen (`wild = false`,
`S:shared/BanditsNPCBearDefs.lua:100`, darum zeigt Vanilla dort das Radial, `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171`). Folge: V schliesst
dort Vanillas Tier-Radial und oeffnet das eigene Fenster bzw. sagt "You do not have a bear yet."; Plan 0.9/F5 spricht vom EIGENEN Baeren. Nebenpunkt:
solange das Fenster offen ist, verbraucht es V (`Window.lua:546-549`) -- Fahrzeug-Radial/NPC-Gespraech gehen erst mit dem zweiten Druck (gewollt wie
Vanillas Handwerks-Fenster, aber nirgends genannt). Vorschlag: `ours` nur, wenn die Sicht das Tier einem eigenen Eintrag zuordnet (Hud-Weg
`B.ViewOf` + `owner == myKey`, sonst wie ein fremdes Tier: `return`); den Nebenpunkt in Kevins Testliste.

**A3 (minor, B1e-Rest A1/B6): ein Text sagt beim grossen Koerper weiter "cub".** `server/BanditsNPCBearServer.lua:160` und `:171` (`handCheck`, Fuettern/
Streicheln) schicken `Why_Gone` ohne Koerper, obwohl `B.BodyKind(animal)` (:158) ihn kennt -- z. B. beim Fuettern der alten grossen Kopie nach
Unstuck (Z3, `B.RecOf` -> "stale", Registry.lua:370) liest Kevin "The cub is gone.". Plan 4a hat die Stelle bewusst ausgelassen ("ohne Eintrag").
`tellWhy` (:47-53) nimmt heute kein bd. Vorschlag: `bd = "big"` an die Meldung haengen, wenn `B.BodyKind(animal) == "big"` (eine Zeile je Stelle).

**A4 (minor, Auftrag vs. Bau): zwei begruendete Abweichungen vom Auftragstext.** (a) "Frei herumlaufen": Vorgabe-Radius **12** statt der beauftragten
**8** (`S:shared/BanditsNPCBear.lua:198`, `sandbox-options.txt:218-223`; Begruendung PLAN_F1.md 0.3: Kevins "Bleiben-Radius 12" ENT:284, mit 8 rannte das
Junge in B1b heim). (b) "Komm her (= Call to me, gleiche Abklingzeit, Restzeit am Knopf)": gebaut als ZWEI Knoepfe -- "Come here" laeuft ohne
Abklingzeit (`Order.lua:253-287`), die Call-Abklingzeit mit Restzeit traegt "Unstuck" (`WinData.lua:426-436`); Begruendung PLAN_F1.md 0.2 (Kevin
setzte Unstuck = Call to me, ENT:280; "Komm her" ist sein eigener Befehl, ENT:65). Beides steht als Kevin-Frage F1/F2 (PLAN_F1.md 12). Vorschlag: nichts
aendern, in Kevins Morgenliste ganz nach oben.

**A5 (minor, Kevins Wunsch): Zaehm-Fortschritt erscheint nie im Fenster.** Kevin 08.11. ~19:55 (ENT:102): Zaehm-Balken "sichtbar beim Zaehmen und im
Baeren-Fenster". Das Fenster nimmt nur `tame`/`missing` (`client/BanditsNPCBearWinData.lua:187`); waehrend des Zaehmens sagt V "You do not have a bear
yet." (`Window.lua:617-620`), obwohl die Sicht den Wert traegt (`tame`, forschung_f1.md 3.1). Nach dem Zaehmen ist er fest 100 (kein Wert zu zeigen,
"Trust" steht ehrlich unter "Coming later"). Vorschlag: als Kevin-Frage aufnehmen (empfohlen: fuer das an ihn gebundene Junge ein Hinweis "Taming: 40%"
statt "no bear", oder ein schmales Fenster nur mit Name + Zaehm-Balken -- in F1 nicht bauen).

**A6 (minor, Beleg-Kommentar): Server-Aufruf mit Client-Fundstelle.** `server/BanditsNPCBearOrder.lua:16`, `:164`, `:365` belegen `square:getX/getY/getZ()`
(laeuft am Server) mit `V:client/DebugUIs/DebugContextMenu.lua:636`. Form gleich, Seite nicht. Server-Vorbilder gibt es: `V:server/BuildingObjects/
ISBuildingObject.lua:135` (`x = square:getX();`), `V:server/Animal/ISPickDungCursor.lua:26`. Vorschlag: Kommentar umstellen (wie B1e A6).

**A7 (minor, Stand der Unterlagen): Test-Mod hat sich nach dem Zusammenbau geaendert.** Lauf baer-gen-gross legte am 12.11. 01:02 sechs Dateien in
NCBearTest (Tabelle 0). Folge: `trockenlauf_f1.txt`/`_vor_b5a.txt`/`probe_f1_ausgabe.txt` (24 Altlasten, 28 Warnungen; bau_f1_zusammenbau.md :26-29,
:177-183) stimmen nicht mehr -- heute 27 Altlasten, 31 Warnungen, Fehler weiter 0 / nur Altlasten; das Skript kennt die neuen Dateien (ALT_EXPECTED).
Kein Staging-Ziel betroffen (Gen-Arten `ncbeargen*` stehen nicht in `B.TYPE_BODY`, Key.lua behandelt sie als fremdes Tier). Vorschlag: direkt vor dem
Einbau Trockenlauf + Probe neu laufen lassen und die drei Ausgaben ersetzen; im Kopf von `staging_dateien.txt` vermerken.

**A8 (minor, Bildgroesse): vier UI-Bilder bleiben bei 288 px.** `media/ui/BanditsNPCBearCub_marker288.png`, `..._arrow288.png`, `..._disc.png`,
`..._ring.png` je 288 x 288 (> 256), das Fenster nutzt zwei davon (`Window.lua:37-38`). A5 ("kein Handlungsbedarf", forschung_f1.md 6.2) nachgeprueft:
Vanillas Option sagt selbst "non-vehicle-**model** textures" (`V:shared/Translate/EN/UI.json:64`), 442 von 1539 Vanilla-PNG in `media/ui` sind > 256
(z. B. `defense/female_base.png` 123 x 302, geladen `V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191`); das entscheidende Glied (Deckel nur
bei Flag 384) ist NUR JAR (Lesart, kein Aufruf). Schlimmster Fall: leichte Unschaerfe, kein Fehler. Vorschlag: so lassen; in Kevins 4K-Test mit
"Max. Texturgroesse 256" Kopf-Symbol und Pfeil einmal ansehen.

## 8. Fragen fuer Kevin (aus dieser Pruefung; Nachtschicht -- empfohlener Weg in Klammern)
1. Zaehm-Balken auch im V-Fenster, solange du das Junge noch zaehmst (A5)? (Empfehlung: ja, als kleiner Hinweis -- spaeter, nicht in F1.)
2. V an einem FREMDEN Baeren (Mehrspieler): Vanillas Tier-Radial lassen statt dein Fenster zu oeffnen (A2)? (Empfehlung: ja.)

Statisch geprueft, nicht gespielt.
