# Lauf baer-b1c: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 11.11.2026 Nacht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (49 Dateien laut
`staging_dateien.txt`: B1a + B1b + B1c KERN + OBERFLAECHE + Zusammenbau). Ich habe KEINE Datei im Staging, in der Test-Mod, in NPC Crew,
Vanilla oder Bandits geaendert; geschrieben nur dieser Bericht und Hilfsdateien im Scratch-Ordner (eigene Pruefskripte `form.py`,
`methoden.py`, `texte.py`, `fundstellen.py`, Diffs gegen die Test-Mod, meine Probe `probe_a/`). Kein git, kein Spielstart, kein Download.
Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/` (42.22.2), `B:` = Bandits `42.22/media/lua/`, `T:` = Test-Mod
`NCBearTest/42/media/lua/`, `NC:` = NPC Crew `42/media/lua/`.

## 0. Ergebnis

**Kein Blocker. 1 major, 6 minor.** Alle Zahlen der Bauer- und Zusammenbau-Berichte habe ich selbst nachgefahren und bestaetigt (Tabelle 1).
Jeder Engine-Aufruf, den B1c neu benutzt, hat eine Vanilla-/Bandits-Fundstelle mit gleichen Argumenttypen -- ausser den beiden mit Kevins
Wort (`setVariable("animalRunning", false)`, `pathToLocation(x, y, z)`), beide genau einmal in `B.MoveTo`. Jar-only: keiner. Keine
Testbefehle ausserhalb der Bench, keine Namenskollision, Texte in sieben Sprachen sauber, Uebernahme-Trockenlauf und Probe gruen.
Der Kern der Befunde: Z1 des Zusammenbaus ist echt und verletzt den Auftrag "nie neu als found/shy" (A1); die Laerm-Wache am MP-Server
ruft zwei Charakter-Methoden, die nur clientseitig belegt sind (A2); `addTickBox`/`addSlider` haben nirgends einen Aufrufer (A3, Regelfrage);
die drei neuen Skript-Regeln sind reine Regex und leicht zu umgehen (A4, wie B1b A5); der Karten-Einhaengeblock ist wortgleich mit NPC Crew
(A5, "lernen, nicht kopieren"); dazu eine verrutschte Fundstelle und Kleinkram (A6, A7).

## 1. Selbst laufen lassen (Zahlen)

| Pruefung | Ergebnis (mein Lauf 11.11. Nacht) | deckt sich mit Bauer/Zusammenbau |
|---|---|---|
| `luacheck.py` auf alle 23 Lua des Stagings (22 kopierte + Bench) | `23 file(s) checked, 0 failed` | ja |
| `scopecheck.py` (23) | `23 file(s), 0 violation(s)` | ja |
| `localcount.py` (23) | aktiv hoechstens 39 (Bench `:369`), kopiert hoechstens 37 (`S:server/BanditsNPCBearWorld.lua:572`, `S:server/BanditsNPCBearServer.lua:908`, `S:client/ISUI/BanditsNPCBearHud.lua:289`); insgesamt hoechstens 69 (World `:572`, `B.ScanAnimals`) -- weit unter 180/200 | ja |
| `luacheck_pz.py` (23) | 16 x W113, alle erwartet: 3 Aktionsklassen `S:client/BanditsNPCBearMenu.lua:86/97/107`, 13 in der Bench (`NCBear_*`, `NCBearMenu`) | ja |
| `luacheck_pz.py --unused` (10 B1c-Dateien) | 7 Hinweise, harmlos: `Guard.lua:110` W311 (kind/tx/ty Vorbelegung), `Guard.lua:255` W212 `players`, `Heal.lua:247` W212 `o`, `Rules.lua:41`/`:160` (B1a) | neu (A7) |
| Dateiform (eigenes `form.py`, 49 Dateien) | alle LF, kein BOM, LF am Ende, keine Leerzeichen am Zeilenende, Lua und `.txt` reines ASCII: 0 Probleme | ja |
| `staging_dateien.txt` gegen Platte und Test-Mod | 49/49 Zeilen: MD5, Bytes, neu/ueberschreibt/gleich stimmen (7 / 25 / 17), keine Datei ausserhalb der Liste | ja |
| `attrappe/kern/run.lua` | 136 bestanden, 0 Fehler (byte-gleich mit `kern/ergebnis.txt`) | ja |
| `attrappe/b1b_kern/run.lua` | 204 bestanden, 0 Fehler (`b1b_kern/ergebnis.txt` ist noch der B1b-Stand 203 -- A7) | ja (Zahl) |
| `attrappe/b1c_kern/run.lua` | 154 bestanden, 0 Fehler (byte-gleich mit `ergebnis.txt`) | ja |
| `attrappe/gesamt/run.lua` | **812 bestanden, 0 Fehler**, einzige `***`-Zeile die gewollte Heilungszeile 18c (byte-gleich mit `gesamt/ergebnis.txt`) | ja |
| dieselbe gegen MEINE Probe (`<scratch>/probe_a/NPCCrew/42/media/lua/`) | 812 / 0, byte-gleich mit `gesamt/ergebnis_probe.txt` | ja |
| `attrappe/pruef_b/run.lua` | byte-gleich mit `pruef_b/ergebnis_b1b_nach.txt` | ja |
| `attrappe/pruef_b1b/run_nach.lua` | byte-gleich mit `pruef_b1b/ergebnis_b1c.txt` (Z2: zwei gewollte BEFUND-Zeilen) | ja |
| `attrappe/ober`, `b1b_ober`, `b1c_ober` (ohne / mit `kern`) | 116/0 + 117/0, 144/0 + 134/0, **193/0 + 180/0** | ja |
| `texte_pruefen.py`, `_b1b.py`, `_b1c.py` | je FEHLER gesamt: 0 | ja |
| `belege.py`, `belege_b1b.py`, `belege_b1c.py` | abweichend 0 von 112, 0 von 51, 0 von 89 | ja |
| `gesamt/xref_b1c.py` | 0 Luecken, Ausgabe byte-gleich mit `xref_b1c.txt` | ja |
| `uebernahme_force/probe_force.py` | 23 Faelle, 0 Fehler | ja |
| Uebernahme Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten, 1 GLB-Clip, 1 NPC-Crew-Kommentar); 22 Lua, 5505 Codezeilen, Cheat-Funde 0; Tier-Regeln je an ihrem Ort (CreateCub: `Ride.lua:68` B.PlaceCub + `Server.lua:121` B.AppearFor; animalRunning/pathToLocation `World.lua:768/769` B.MoveTo; callAt nur Ride.lua); Kollisionen 0; "101 benutzt, fehlen in EN: 0; Ersatztexte 109, wortgleich: ja". NPC Crew ist seit 04:45 v3.14.70: UI.json jetzt 3812 -> 3921 (Bericht 3810 -> 3919), Kommentarzeile `NC:shared/BanditsNPC.lua:1359` (Bericht :1358) | ja (NC hat sich bewegt) |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere | ja |
| **Probe** (eigene, nach `<scratch>/probe_a`) | **OK -- 0 Fehler, 26 Warnungen**, 49 Dateien geschrieben; luacheck/scopecheck/localcount je kopierter Datei ok; luacheck_pz 0 Treffer + 3 erlaubt | ja |
| Texte in der Probe (zusammengefuehrt) | je Sprache UI.json 3921, Sandbox.json 141, IG_UI.json 3; alle 21 Dateien Round-Trip; Baeren-Schluessel 109 / 49 (+ `Sandbox_BanditsNPC` gleich) | ja |
| eigener Text-Pruefer `texte.py` (7 Sprachen) | UI 109, Sandbox 50, IG_UI 3 (EN 6 mit den 3 Altlasten); gleiche Schluessel und Platzhalter (`%1`, `%%`), sortiert, Round-Trip, kein BOM/CR, kein `<`/`>`, keine Testwoerter; CN 378 Zeichen, **0** ausserhalb Vanilla-CN; `U.EN` 109 == EN/UI.json wortgleich; 101 Schluessel als Literal im kopierten Code, alle in EN (die 8 `Dir_*` baut `S:client/BanditsNPCBearClient.lua:188`); neu genau die 15 Plan-Schluessel + 4 Sandbox, geaendert `Note_StayCar`, `Menu_FollowTip` (7 Sprachen) und ES `Hud_Pet`; Kollision mit NC nur `Sandbox_BanditsNPC` (gleicher Wert) | ja |
| eigener Methoden-Abgleich `methoden.py` (jede `:methode(` und jeder Bibliotheks-/Global-Aufruf in den B1c-Codezeilen: neue Dateien ganz, geaenderte nur die neuen Zeilen) gegen V + B | 45 Methodennamen, jeder mit >= 2 Aufrufen in V+B (knappste: `getAnimalID` 2, `fleeTo` 2, `pathToLocation` 2, `getOptions` 2); Bibliothek `math.abs/ceil/floor/sqrt`, `string.format/sub` je viele Vanilla-Aufrufe; **`pcall` 0 in V und B** (ohne Befund, Abschnitt 4); `addTickBox`/`addSlider` nur gleichnamige Fremdfunktionen (A3) | neu |
| eigener Fundstellen-Abgleich `fundstellen.py` (jede `pfad.lua:zeile` in allen 23 Staging-Lua) | 628 Fundstellen, 15 auffaellig: 1 echt verrutscht (A6), Rest Bereichs-Anfaenge auf Kommentarkoepfen (`NC:...MiniMap.lua:249-276`, `NC:...Spawn.lua:238-321`, `T:shared/NCBearFight.lua:28-38`, `B:client/BanditZombie.lua:60-87`), die bekannte B1b-Stelle `V:client/ServerCommands.lua:210` und Pfade ausserhalb meiner Suchorte | neu |

## 2. Belege der in B1c neuen Engine-Aufrufe (selbst in den heutigen Dateien gelesen)

| Aufruf (Typen) | Ort im Staging | Fundstelle (gelesen) | Seite | Urteil |
|---|---|---|---|---|
| `a:setVariable("animalRunning", false)` | `S:server/BanditsNPCBearWorld.lua:768` (einzige Stelle) | **Kevins Wort 11.11.** (`baer/begleiter/ENTSCHEIDUNGEN.md:282`); Methode `V:shared/TimedActions/Animals/ISMilkAnimal.lua:139` (Spieler), `B:shared/ZombieActions/ZAMove.lua:32` (Zombie), am Tier `T:shared/NCBearFight.lua:457/:1064` (bPathfind) | Schreiber | ok (ENT nennt `:138` / `:31`, richtig sind `:139` / `:32` -- der Code nennt die richtigen, A6) |
| `a:pathToLocation(x, y, z)` (ganze Zahlen aus `sq:getX/Y/Z`) | `World.lua:769` (einzige Stelle) | **Kevins Wort 08.11.** (`forschung_engine.md:627`); gleiche Form am Zombie `V:client/DebugUIs/DebugContextMenu.lua:636` | Schreiber | ok |
| `a:getStress()` | `S:server/BanditsNPCBearGuard.lua:175` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:17`; am Server erreicht ueber `update()` `:127` (`if not isClient()`) -> `milk()` `:60` -> `stress()` | SP + Server | ok (auch serverseitig belegt) |
| `a:getActionStateName()` | `Guard.lua:187` | `B:shared/ZombieActions/ZASmack.lua:486` (Charakter), am Tier `T:shared/NCBearFight.lua:1099` (gespielt, SP) | **nur Client/SP belegt** | **A2** |
| `a:getVariableBoolean("bPathfind")`, `("animalRunning")` | `Guard.lua:189/:190` | `B:shared/ZombieActions/ZAMove.lua:61` (Zombie); Name `animalRunning` nur Jar (Plan 8 Nr. 8: nur Zusatzsignal) | **nur Client belegt** | **A2** |
| `Events.OnTick.Add(f)` (Server-Ordner) | `Guard.lua:210` | `V:server/Foraging/forageServer.lua:502` | SP + Server | ok |
| `getCell():getZombieList()`, `:size()`, `:get(i)`, `z:getX/getY/getZ()`, `z:isAlive()` | `World.lua` B.ZedNear | `B:server/BanditSave.lua:15-25`, `:46-52` (beide `if isClient() then return end`, also Server/SP) | SP + Server | ok |
| `z:getVariableBoolean("Bandit")` | `World.lua:291` (nur `B.IsSP()`) | `B:client/BanditZombie.lua:74` | SP | ok |
| `BanditUtils.GetZombieID(z)`, `GetBanditClusterData(id)[id]` | `World.lua` isBanditZ (Server) | `B:server/BanditSave.lua:55-57` | Server | ok |
| `BanditCompatibility.IsReanimatedForGrappleOnly(z)` (Bandits-Lua -> `zombie:isReanimatedForGrappleOnly()`) | `World.lua` B.ZedNear | `B:shared/BanditCompatibility.lua:187-189`; Aufrufer nur `B:client/BanditZombie.lua:118`, `B:client/BanditUpdate.lua:2102` | **am Server nicht belegt** | **A2** (klein) |
| `BanditZombie.CacheLightZ` (Lua-Daten) | `World.lua` B.ZedNear (nur SP) | `B:client/BanditZombie.lua:12`, `:60-87` | SP | ok |
| `getOnlinePlayers()`, `p:isDead()`, `getNumActivePlayers()`, `getSpecificPlayer(i)`, `p:getX/getY/getZ()` | `World.lua` B.DeadAt | `V:server/Foraging/forageServer.lua:463-466`, `V:server/XpSystem/XpUpdate.lua:298`, `V:client/Fishing/FishingHandler.lua:6`, `V:server/BuildingObjects/ISBuildingObject.lua:183`; getZ am Spieler `B:server/BanditServerSpawner.lua:191` | Schreiber | ok (Kommentar nennt `:179`, dort nur getX/getY -- A6) |
| `sq:TreatAsSolidFloor/HasTree/isFree(false)/isVehicleIntersecting`, `getCell():getGridSquare`, `sq:getX/Y/Z()` | `World.lua` spotOk / B.SpotNear | wie `B.SquareFits` (`S:server/BanditsNPCBearWorld.lua:97-100`); `V:server/BuildingObjects/ISBuildUtil.lua:34`, `V:server/Animal/ISPickDungCursor.lua:104`, `V:client/DebugUIs/DebugContextMenu.lua:636` | Schreiber | ok |
| `B.CreateCub` (= `addAnimal` + `addToWorld`) aus `B.PlaceCub` | `S:server/BanditsNPCBearRide.lua:68` | `V:server/ClientCommands.lua:809-810`, `V:client/DebugUIs/DebugContextMenu.lua:1460-1467` | Schreiber | ok |
| `B.RemoveCub` (unveraendert) aus RideBoard / HandleCall / dropCopy | Ride.lua `:114`, `:321`; World.lua dropCopy | `V:shared/Definitions/animal/ButcheringUtil.lua:609-614` | Schreiber | ok |
| `player:getVehicle()` (Bitte "Call") | `Ride.lua:296` | `V:server/Vehicles/VehicleCommands.lua:11` (Spieler eines Client-Befehls, Server) | Server | ok |
| `a:getModData()` (Spiegel v2), `a:getAnimalID()` | Heal.lua, Registry.lua, Ride.lua | `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127`, `V:shared/Definitions/animal/ButcheringUtil.lua:596`; `V:client/ISUI/Animal/ISAnimalUI.lua:53` | Schreiber | ok; getAnimalID am MP-Server = A3 aus B1a, durch B1c weiter ausgeweitet (A2) |
| `getTimestampMs()`, `ZombRand(1000)` | Registry `newUIn` u. a. | `V:server/Foraging/forageServer.lua:456`, `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25` | beide | ok |
| `PZAPI.ModOptions:create(id, key)`, `:addTitle(key)` | `S:client/BanditsNPCBearOptions.lua:47-48` | Definition `V:client/PZAPI/ModOptions.lua:247`, `:28`; Aufrufer `B:client/BanditModOptions.lua:12-13` | Client | ok |
| `options:addTickBox(id, key, true, tipKey)`, `options:addSlider(id, key, 100, 200, 50, 100, tipKey)` | `Options.lua:50`, `:53` | nur die Definitionen `V:client/PZAPI/ModOptions.lua:64-86`, `:206-228`; Darstellung `V:client/OptionScreens/MainOptions.lua:2809-2830`, `:3019-3036` -- **kein Aufrufer** in V, B oder NC | Client | **A3** |
| `PZAPI.ModOptions:getOptions(id)`, `:getOption(id)`, `:getValue()` | `Options.lua:77-80` | `B:shared/BanditCompatibility.lua:98-99` | Client | ok |
| Seitenname/Titel/Tooltips durch `getText` | (Vanilla) | `V:client/OptionScreens/MainOptions.lua:2801`, `:2804`, `:2810-2812`, `:3020` | Client | ok -- darum Schluessel (Bandits uebergibt schon uebersetzt, `B:client/BanditModOptions.lua:12`; doppelt `getText` schadet dort nicht) |
| `BanditEventMarkerHandler.set(id, icon, dur, x, y, color, desc)` | `S:client/ISUI/BanditsNPCBearMarker.lua:95` | `B:client/BanditEventMarkerHandler.lua:6-38`; Aufrufer `B:server/BanditServerSpawner.lua:1093`, `B:server/BanditServerWanderers.lua:697` | Client | ok |
| `markers[id]`, `marker:getDuration()`, `getIsVisible()`, `setX(n)`, `.x/.y`, `old:removeFromUIManager()` | Marker.lua | `B:client/BanditEventMarkers.lua:142`, `:28`, `:81`, `:235-236`; `V:client/ISUI/ISUIElement.lua:1373`, Aufrufer `V:client/ISUI/Maps/ISMap.lua:116` | Client | ok |
| `Events.OnTick.Add`, `Events.OnGameStart.Add`, `getSpecificPlayer(0)`, `p:isDead()` (Client) | Marker.lua, Map.lua | `V:client/Chat/ISChat.lua:943`, `:1186`, `V:client/Farming/CFarmingSystem.lua:45`, `V:client/Context/ISMenuContextWorld.lua:37` | Client | ok |
| `ISMiniMapInner.render` / `ISWorldMap.render` umwickeln | `S:client/ISUI/BanditsNPCBearMap.lua:179-193` | `V:client/ISUI/Maps/ISMiniMap.lua:4` (erbt `V:client/ISUI/ISUIElement.lua:1618`), `V:client/ISUI/Maps/ISWorldMap.lua:384` | Client | ok (Form: A5) |
| `self.mapAPI:worldToUIX(x, y)` / `worldToUIY(x, y)` (zwei Zahlen), `getZoomF()` | Map.lua `:149-150`, `:129` | `V:client/ISUI/Maps/ISWorldMap.lua:478-479`, `:447`; `V:client/ISUI/Maps/ISWorldMapSymbols.lua:347`; beide Karten holen `getAPIv3()` (`ISMiniMap.lua:192`, `ISWorldMap.lua:268`) | Client | ok |
| `self:drawTextureScaledAspect(tex, x, y, w, h, a, 1, 1, 1)`, `getWidth()/getHeight()`, `getTexture(pfad)` | Map.lua | `V:client/ISUI/Maps/ISWorldMap.lua:482` (9 Argumente, gleiche Typen), Signatur `V:client/ISUI/ISUIElement.lua:1065`; `:259-271`; `V:client/ISUI/Maps/ISMap.lua:573` | Client | ok |
| `getTextManager():getFontHeight(UIFont.Medium/Large)`, `drawTextCentre(..., UIFont.Medium/Large)` | Hud.lua | `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8`, `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6`, `V:client/ISUI/ISFitnessUI.lua:204`, `V:client/Chat/ISAlert.lua:35` | Client | ok |
| `playerObj:getVehicle()` (Menue) | Menu.lua `addCall` | `V:client/ISUI/Hutch/ISHutchMenu.lua:8` | Client | ok |
| `getText` mit `%%` ohne Werte (`MO_TagSize`) | (Vanilla) | Vorbild `ContextMenu_FullPercent` = "%% full" (`V:shared/Translate/EN/ContextMenu.json:500`), ohne Werte gerufen `V:client/ISUI/ISInventoryPaneContextMenu.lua:2187`, `V:client/ISUI/ISWorldObjectContextMenu.lua:364` | Client | ok (Anzeige "%" ungespielt) |

Nicht benutzt (grep ueber die 22 kopierten Dateien, Kommentare ausgenommen): `next(`, `%a`, `string.byte/char/gsub/match/find`, `unpack`,
`select`, `setmetatable`, `os.`/`io.`, `goto`, Teleport (`setX/setY` am Tier), `changeStress`, `drawTextZoomed`, `PZMath`. `setVariable` am
Tier ausserhalb B.MoveTo nur das B1a-`B.ACT` (FeedAction). Jar-only ausser den beiden Kevin-Ausnahmen: keiner.

## 3. Befunde

### A1 (major) -- Z1 bestaetigt: eine gescheiterte Heilung macht aus dem gezaehmten Jungen ein neues "found"
- **Wo:** `S:server/BanditsNPCBearRegistry.lua:341-364` (`B.RecOf`: gibt `B.HealFromMark` nil, faellt der Weg auf `B.NewRec("found", ...)` und
  `B.Commit` -- das ueberschreibt auch den Spiegel); Ursachen fuer nil in `S:server/BanditsNPCBearHeal.lua:168` ("full"), `:176` ("nokey"),
  `:177`/`:182` ("cap"), `:288-290`, und `:302-310` (ein v1-Spiegel "tame" ohne Eintrag wird NUR im SP hergestellt, im MP gibt es nil).
  Aufrufer: `S:server/BanditsNPCBearServer.lua:167` (`handCheck`, also jedes Fuettern/Streicheln).
- **Beleg:** Auftrag 1 woertlich: "fehlt der Eintrag, wird er daraus WIEDERHERGESTELLT (gleicher Zustand, gleicher Besitzer), nie neu als
  found/shy" und "Deckel je Spieler gilt weiter". Beides zusammen heisst: kann nicht hergestellt werden, dann warten, nicht neu anfangen. Der
  Suchlauf haelt sich daran (`S:server/BanditsNPCBearWorld.lua` Schritt 3: nil "bleibt, nie entfernt"), `B.RecOf` nicht. Szenario wie
  Zusammenbau Z1 (MP: Register verloren, alice hat schon einen Baeren, bob fuettert alices altes Junges -> `b2 st=shy owner=nil src=found`,
  Spiegel `shy`); dazu im MP jeder v1-Spiegel "tame" ohne Eintrag (genau Kevins N9-Fall, nur am Server). Im SP selten (Deckel voll), im MP
  wahrscheinlicher. Der Plan nennt den Fall "solange die Regeln es erlauben" (PLAN_B1C.md 1.1 Punkt 3) -- der Auftrag kennt diese
  Einschraenkung nicht.
- **Vorschlag:** in `B.RecOf` nach dem Heil-Aufruf: traegt der Spiegel `st` tame/fed/missing (v2) oder ist es ein v1-Spiegel "tame", und kam
  nil zurueck -> `return nil, "heal"` (Menue `Why_Gone`, kein NewRec, Spiegel bleibt). Der seltene Suchlauf stellt es her, sobald ein Platz
  frei ist. Kevins Wort ist mit dem Auftrag schon da (keine neue Frage noetig). Attrappe: b1c_kern Fall 1 um "Deckel voll + Fuettern" und "MP
  v1-tame + Fuettern" ergaenzen.

### A2 (minor) -- Seite: die Laerm-Wache am MP-Server ruft zwei nur clientseitig belegte Charakter-Methoden (und A3 waechst weiter)
- **Wo:** `S:server/BanditsNPCBearGuard.lua:187` `a:getActionStateName()`, `:189-190` `a:getVariableBoolean(...)` (laeuft je Bild am
  MP-Server, `Guard.lua:1`, `:210`); `S:server/BanditsNPCBearWorld.lua` B.ZedNear `grapple(zb)` (`BanditCompatibility.IsReanimatedForGrappleOnly`);
  Plan 8 Nr. 6/7/19 und KERN-Bericht 3 nennen als Seite "Schreiber" bzw. "beide".
- **Beleg:** Bandits fuehrt seine ZombieActions nur vom Client aus (`grep ZombieActions` in `B:` server: 0, client: `B:client/BanditUpdate.lua`);
  alle `getActionStateName` in Bandits liegen unter `B:client/` (`BanditUpdate.lua:414`, `:1623`, `:1656`, `:2193`, `BanditMenu.lua:161`);
  `getVariableBoolean` hat weder in `V:server/` noch in `B:server/` einen Aufruf; `IsReanimatedForGrappleOnly` ruft Bandits nur in
  `B:client/BanditZombie.lua:118` und `B:client/BanditUpdate.lua:2102`; `T:shared/NCBearFight.lua:1099` ist der gespielte Einzelspieler. Die
  Methoden gibt es am Server (gleiche Java-Klasse), ob ein Server-Tier dort einen Zustand liefert, ist ungeprueft. `getStress` dagegen ist am
  Server belegt (`V:shared/TimedActions/Animals/ISMilkAnimal.lua:127` -> `:60` -> `:17`). Wirft `getActionStateName` am Server, bricht
  `calmTickBody` in JEDEM Bild beim ersten Jungen ohne Stress-Sprung ab (der pcall in `B.CalmTick` `Guard.lua:203-206` faengt es, Zeile je
  60 s) -- die uebrigen Jungen werden dann nie beobachtet. Dazu weitet B1c A3 aus B1a weiter aus: Heil-Fenster-Suchlauf je 15 s fuer 2 min nach
  jedem Laden (`Server.lua:939-945`, `getObjectListForLua` am Server), Heilung, Aussteigen und "Call to me" binden ueber `getAnimalID`
  (`Heal.lua:83`, `Ride.lua:72`). Der KERN nennt A3 ehrlich (Bericht 7), die zwei Charakter-Methoden nicht.
- **Vorschlag:** in Kommentar und Bericht wie A3 als MP-Testpunkt fuehren ("Server: `calm tick:` im Log?"); billig absichern, ohne Neues: am
  Server (`isServer()`) nur das belegte Stress-Signal nutzen, oder den Teil "rennt ohne eigenen Befehl" je Junges einzeln schuetzen, damit ein
  Fehler nicht alle uebrigen Jungen abschaltet. `grapple` am Server wahlweise nur im SP fragen (am Server zaehlt ohnehin `isAlive`).

### A3 (minor, Regelfrage) -- `addTickBox` / `addSlider` haben in Vanilla, Bandits und NPC Crew keinen einzigen Aufrufer
- **Wo:** `S:client/BanditsNPCBearOptions.lua:50`, `:53`; Begruendung `bau_b1c_oberflaeche.md` 3 ("die eiserne Regel gilt Engine-Methoden").
- **Beleg:** Vanilla definiert beide nur (`V:client/PZAPI/ModOptions.lua:64-86`, `:206-228`); die 5 Treffer "addTickBox" und 30 "addSlider" in V
  sind andere Funktionen (`ISDebugUtils.addTickBox`, `MainOptions:addSlider`); Bandits benutzt auf seiner Seite nur `addTitle`/`addKeyBind`
  (`B:client/BanditModOptions.lua:13-14`), NPC Crew nur `addTitle`/`addComboBox`/`addKeyBind`/`addDescription`
  (`NC:client/BanditsNPCModOptions.lua:83-124`). Das Risiko ist klein: beide sind reines, gelesenes Lua (nur Tabellen), und die Darstellung
  laeuft durch Vanillas eigene Bausteine (`MainOptions.lua:2810` `addYesNo`, `:3020` `MainOptions:addSlider` -- den benutzt Vanilla selbst,
  `MainOptions.lua:1090`). Aber "mit echtem Aufruf gesehen" ist es nicht; die Auslegung "gilt nur fuer Engine-Methoden" steht bisher nur in
  einem Bauer-Bericht, nicht bei Kevin.
- **Vorschlag:** Kevin als Regelfrage vorlegen ("Vanilla-Lua-Funktion, deren ganzer Code gelesen ist, ohne Aufrufer -- erlaubt?") oder sein
  Wort je Funktion einholen; im Kopf von Options.lua und in NAEHTE Zeile 19 ehrlich "kein Aufrufer, nur Definition gelesen" schreiben;
  Testpunkt: Seite zeigt Haken + Schieber, Wert ueberlebt einen Neustart (ModOptions.ini).

### A4 (minor) -- Die neuen Skript-Regeln `animalRunning`, `pathToLocation` und die Optionen-Text-Regel sind leicht zu umgehen
- **Wo:** `baer/tools/baer_uebernahme.py:271-274` (Regex `setVariable\s*\(\s*["']animalRunning["']` und `:pathToLocation\s*\(`), `:1255-1272`
  (Optionen-Seite: nur ein reines String-Literal oder ein lokaler Satz zaehlt als fester Text).
- **Beleg (eigene Regex-Probe):** nicht erkannt werden `local V = "animalRunning"; a:setVariable(V, false)`, `a.setVariable(a, "animalRunning",
  false)`, `a["setVariable"](a, ...)`, `setVariable("AnimalRunning", ...)` (falls die Engine Namen ohne Gross/Klein vergleicht -- ungeprueft);
  ebenso `a.pathToLocation(a, ...)`, `a["pathToLocation"](...)`, `local f = a.pathToLocation`. Bei der Optionen-Seite geht
  `"Display above" .. x` oder `getText("...")`/`U.T(...)` als Argument durch. Heute ist der kopierte Code sauber (nur `World.lua:768/769`, alle
  Seiten-Texte Schluessel) -- die Regeln schuetzen spaetere Aenderungen schlecht. Genau diese Lehre stand in B1b A5 (`force`-Regel), dort wurde
  sie zur Token-Analyse umgebaut; die B1c-Regeln fallen wieder auf Regex zurueck.
- **Vorschlag:** jedes Vorkommen des Literals `"animalRunning"` und jedes Vorkommen des Bezeichners `pathToLocation` im Code-Teil ausserhalb
  der erlaubten Stellen werten (`Guard.lua` `getVariableBoolean("animalRunning")` als zweite erlaubte Stelle aufnehmen); in Seiten-Argumenten
  jedes Literal mit Buchstaben, das kein `UI_BN_Bear_*`-Schluessel ist, auch in einer Verkettung, als festen Text melden. Gegenprobe um die
  Varianten oben erweitern.

### A5 (minor) -- Der Karten-Einhaengeblock ist wortgleich mit NPC Crew ("lernen, nicht kopieren")
- **Wo:** `S:client/ISUI/BanditsNPCBearMap.lua:166-190`; Kopf `:16-18` ("NC client/ISUI/BanditsNPCMiniMap.lua:249-276, nur gelesen").
- **Beleg:** `NC:client/ISUI/BanditsNPCMiniMap.lua:237-275`: gleiche Namen (`prevMini, prevWorld`, `doneMini, doneWorld`, `miniRender`,
  `worldRender`), gleiche Zeilen (`if prevMini then prevMini(self) end`, die zwei `if not doneX and ISX and ISX.render then prevX = ISX.render
  ISX.render = xRender doneX = true end`-Bloecke), nur `M.Install` -> `U.MapInstall` und `drawDots` -> `draw`. Auftrag 8 und die Suchorte sagen
  "lernen, nicht kopieren" bzw. "nichts kopieren". Funktional ist alles richtig (die Kette Vanilla -> Baer -> NPC Crew haelt, NAEHTE Zeile 18);
  es ist Kevins eigene Mod und ein Allerwelts-Muster -- trotzdem widerspricht "nur gelesen" dem Befund.
- **Vorschlag:** entweder in eigener Form schreiben (z. B. eine kleine Huelle `wrap(cls, prev, fn)`) oder den Kopf ehrlich machen ("gleiche
  Form wie NC v3.9.55, bewusst: Einmal-Einhaengen ist die Lehre") und Kevin fragen, ob das fuer ihn als Kopie zaehlt.

### A6 (minor) -- Fundstellen: eine verrutschte interne Zeilenangabe, zwei ungenaue Hinweise
- **Wo / Beleg:**
  1. `S:server/BanditsNPCBearServer.lua:589` nennt fuer A3 `server/BanditsNPCBearWorld.lua:280-282`; durch die B1c-Einschuebe in World.lua
     steht dort jetzt der B.ZedNear-Kommentar, der A3-Text ist nach `:463-465` gewandert (Test-Mod `T:server/BanditsNPCBearWorld.lua:280-282`
     hatte ihn noch). Mein Fundstellen-Abgleich: die einzige echt verrutschte von 628.
  2. `S:server/BanditsNPCBearRide.lua:17-18` (und World.lua B.DeadAt-Kopf) nennen "getX/getY/getZ am Spieler: Bandits
     server/BanditServerSpawner.lua:179" -- `:179` hat nur `getX/getY`; `player:getZ()` steht dort bei `:191`.
  3. `S:server/BanditsNPCBearRegistry.lua:142-143` (InitRegistry, B1c-Block): ein ungueltiger ride-Zustand werde "missing ...,
     \"Call to me\" holt es" -- ein vermisstes Junges hat kein Tier zum Anklicken, und das Menue bietet "Call to me" nur am Tier mit
     `v.st == "tame"` (`S:client/BanditsNPCBearMenu.lua:304-308`). Ueber die Oberflaeche ist das erst mit dem V-Fenster moeglich (F4).
  4. `baer/begleiter/ENTSCHEIDUNGEN.md:282` (und der Auftragstext) nennen `ISMilkAnimal.lua:138` und `ZAMove.lua:31`; die Aufrufe stehen bei
     `:139` (`setVariable("milkanimalout", false)`) bzw. `:32` (`:31` ist ein Kommentar). Der Code zitiert richtig.
- **Vorschlag:** 1 auf `:463-465` stellen (oder auf den Funktionsnamen statt einer Zeile zeigen, dann verrutscht nichts); 2 `:191`
  ergaenzen; 3 den Satz auf "kommt beim Wiederfinden zurueck; Call to me fuer Unanklickbare spaeter im V-Fenster" aendern; 4 in ENT nur
  anmerken (Kevins Dokument).

### A7 (minor) -- Kleinkram: Stand der Unterlagen, Texte, Hinweise der Pruefer
- `attrappe/b1b_kern/ergebnis.txt` ist noch der B1b-Stand (203 bestanden, Laufbefehle 80/80/94); der Lauf heute zeigt 204 und 79/79/93 (der
  KERN-Bericht nennt 204 richtig) -- `ergebnis.txt` nachziehen, damit ein spaeterer Vergleich nicht falsch rot wird.
- `baer/NAEHTE.md` Kopf/Zeile 5: "NPC Crew v3.14.69", "UI.json 3810" -- seit 04:45 ist NPC Crew v3.14.70 mit 3812 (mein Trockenlauf und meine
  Probe gegen v3.14.70: weiter OK). Vor einer echten Uebernahme (nach B5a) ohnehin neu laufen lassen.
- FR (B1a-Text, nicht B1c-Auftrag): "Nourriture : prêt" und "Caresses : prêt" -- `prêt` passt im Geschlecht nicht zu "Nourriture" (f.) und
  "Caresses" (f. Pl.; richtig waere "prête"/"prêtes" oder ein neutrales Wort). Der Plan hat FR bewusst gelassen ("Plural ist ueblich"); das
  Problem ist aber nicht der Plural. ES ist richtig gerichtet ("Comida: lista", "Caricia: lista").
- `luacheck_pz --unused`: `Guard.lua:110` (Vorbelegung `kind, tx, ty` wird immer ueberschrieben), `Guard.lua:255` unbenutztes `players`,
  `Heal.lua:247` unbenutztes `o` -- schadet nicht.

## 4. Ohne Befund geprueft

- **Trennung:** die sechs neuen Testbefehle (`NCBear_CubForget`, `_CubMark`, `_CubCalm`, `_CubGuard`, `_CubRide`, `_CubCallReset`) und die zwei
  neuen Rechtsklick-Eintraege stehen nur in `S:client/NCBearBenchCub.lua`, jeder hinter `ready()`/`readyCore()` (zuerst `B.IsSP()`, im MP
  "singleplayer only", `:61-70`, `:665-675`); `NCBear_CubCallReset` leert `B._callAt` nur dort. In den 22 kopierten Dateien: kein `NCBear_`,
  kein `NC<Name>_`, kein debug/cheat/bench/spawn im Code, keine Taste, kein Admin-Recht, kein `_G`, keine globale Zuweisung (Trockenlauf
  "Funde: 0"); der einzige `NCBear`-String ist der erlaubte `bodyModel` (`Defs.lua:68`). "Call to me" ist echte Spielmechanik auf Kevins Wort
  (ENT:280), mit Abklingzeit am Server (`Ride.lua:220-256`, `:300-306`); die Bench ist die einzige Stelle, die sie zuruecksetzt.
- **Namen/Kollisionen:** neue Dateien `server/BanditsNPCBear{Guard,Heal,Ride}.lua`, `client/BanditsNPCBearOptions.lua`,
  `client/ISUI/BanditsNPCBear{Map,Marker}.lua`, Bild `42/media/ui/BanditsNPCBearCub_marker.png` (Muster `BanditsNPCBear*`); grep in `NC:` nach
  `BanditsNPCBear`, `BanditsNPC.Bear`, `BanditsNPC_Bear`, `BearRide`, `BearCall`, `MO_Page/MO_Title/MO_Tag`: 0; `UI_BN_Bear` nur als Teil von
  NPC Crews `UI_BN_Beard_None`, `tcBear` nur als Teil von `tcBeardColor` (andere Objekte, kein Tier-Schluessel), `TrueCompanionsBears` 0. NPC
  Crew hat kein `42/media/ui`; Vanilla `media/ui` und Bandits haben keine gleichnamige Datei (Skript prueft je Lauf). Seiten-Id
  `BanditsNPCBear` neben Bandits `Bandits` und NPC Crew `NPCCrew`; Marker-Id `BanditsNPCBearCub` neben NPC Crews `bnwsArrival`
  (`NC:client/BanditsNPCSpawn.lua:254`); Befehlsmodul `BanditsNPCBear` mit neuem Befehl `Call` (in NC 0 Treffer). `landkarte_index.txt`: kein
  Baeren-Name.
- **pcall:** Vanilla und Bandits rufen `pcall` heute nirgends (grep 0). NPC Crews eigener Pruefer fuehrt es deshalb ausdruecklich als
  Kahlua-Grundfunktion (`C:/Users/Kevin/Zomboid/mods/NPCCrew/_docs/tools/luacheck_pz.py:37-41`, `KAHLUA_BUILTINS = ["pcall"]`, "laeuft im Spiel
  nachweislich"), und die gespielte Test-Mod benutzt es seit B1a (`T:server/BanditsNPCBearServer.lua:584`). Die vier neuen pcall-Stellen
  umschliessen belegte Aufrufe bzw. eigenen Code und sind nie stumm (`B.ErrEvery`): `Guard.lua:204` (aber A2), `Marker.lua:95`, `:122`,
  `Map.lua:159`. Options.lua ohne pcall (Riegel + Fehlerzeile), wie Plan 6.8.
- **Sandbox:** `BanditsNPC.BearRideDistance` integer 3..40, Vorgabe 15, und `BanditsNPC.BearCallCooldownMinutes` integer 0..60, Vorgabe 5 (Kevin
  ENT:280-281), `page = BanditsNPC`, `translation` passend; gleich in `B.OPTS` (`S:shared/BanditsNPCBear.lua:123-124`) und
  `sandbox-options.txt`; Name + Tooltip in allen 7 Sprachen, der Menue-Name im Abklingzeit-Text je Sprache wortgleich mit `Menu_Call`; gelesen in
  `Rules.lua:480`, `Guard.lua:268`, `Ride.lua:226`, `Menu.lua:275`. Alle 22 Optionen werden im kopierten Code gelesen (mein grep: 0 ohne Leser).
  Kevins Zaehm-Dauer vom 11.11. (B1b A8) ist inzwischen drin (`BearTameFeedPoints` 4, `BearTamePetPoints` 3).
- **Texte:** Kevins Text "Bear cub nearby" (`Marker_Cub`) in allen Sprachen; ES "Caricia: %1" (Einzahl, zu "lista") wie bestellt; `MO_TagSize`
  traegt `%%` in allen 7 gleich oft (Vanilla-Form, s. Tabelle 2); Optionen-Seite nur mit Schluesseln (Skript-Regel `menue` greift, Vanilla ruft
  `getText`); `Why_CallWait`/`Menu_CallTip` je ein `%1`, Aufrufer mit genau einem Wert (`Menu.lua:271`, `:277`; Server `note(..., "num", mins)`
  `Ride.lua:304`, `WHY_T` `Server.lua:42`). Kein `<`/`>` (Rich-Text-Tooltips).
- **Uebernahme/Naehte:** Skript kopiert 22 Lua + 4 Modell/Textur/Skript/Knoten + 1 Bild (PNG-Kopf + IHDR 96 x 96 geprueft, MD5
  `9e45e9368ef389aa9b831689d7bd6721` = Kevins Quelle `_arbeit/baer_icon/BanditsNPCBearCub_marker.png`); Bench, mod.info, .git nie. Tier-Regeln
  (CreateCub zweiter Aufrufer B.PlaceCub, animalRunning, pathToLocation, callAt) greifen an genau den erwarteten Stellen. Keine Naht in einer
  NPC-Crew-Datei; die zwei Aufsaetze sitzen auf VANILLAS Kartenklassen (Datei-Ende + OnGameStart, begruendet nicht OnGameBoot, NAEHTE Zeile
  18); nach der Uebernahme laedt `BanditsNPCBearMap.lua` alphabetisch vor `BanditsNPCMiniMap.lua`, beide merken die vorige Methode
  (`NC:client/ISUI/BanditsNPCMiniMap.lua:263-280`), die Kette haelt.
- **SP/MP-Zweig:** SP = `B.IsSP()` (`not isClient() and not isServer()`); server/-Dateien beginnen mit `if isClient() then return end`
  (`Guard.lua:1`, `Heal.lua:1`, `Ride.lua:1`); `B.HandleCall` prueft Besitz, Zustand, Mitfahren, Fahrzeug, Abklingzeit und Platz selbst
  (`Ride.lua:275-327`), der Client schickt nur `{ id }` (`Menu.lua` `onCall`) und graut nur vor; Aussteigen im MP erst nach 3 s und unter 4 K/s aus
  SERVER-Orten (`B._pp`, `Ride.lua:123-131`, `:192-198`); Optionen, Markierung und Karte nur Client aus der eigenen Sicht. Kevins Freigabe 9
  ("MP-abgemeldeter Besitzer -> Junges wartet als follow") bleibt: `S:shared/BanditsNPCBearRules.lua` Regel 10 (`o == nil` -> "hold").
- **Rote Linien:** B1c erzeugt und verbraucht keinen Gegenstand; das Junge ist nicht anleinbar und nicht aufhebbar (`canBeAttached` fehlt,
  `canBePicked = false`, `S:shared/BanditsNPCBearDefs.lua:92-97`) -- Entfernen beim Einsteigen/Herholen kann kein Seil o. ae. verlieren. Kein
  neuer Kick-Weg (nur `sendClientCommand` mit eigener Kennung). Deckel: `calmMax` 8, 4 Antworten je 2 s, `B._callAt` 64, `AskOk` 128,
  `zedScanMax` 1500, Marker-Merker 16, Karten-Symbole 5, Groessenstufen 3. Banditen (auch NPC-Crew-Figuren) zaehlen nie als Zombie; Verstecken
  nur hinter Spielern.
- **B1b-Restbefunde:** N2 (`Rules.lua:361-371`, `:403-423`, in `B.CleanName` `:397`) und N3 (`Registry.lua:582`, `wildOf` + `pkey ~= nil`) gebaut; N1 nur "entschaerft"
  (Gehen aendert das Tempo, nicht das Ziel -- im Test ansehen, wie Plan 1.10 sagt).

## 5. Offen / ungeprueft (zusaetzlich zu Zusammenbau 7)
- A2 im MP-Test: Server-Log auf `calm tick:` und `brain tick:` pruefen (3 min mit einem gezaehmten Jungen, einmal ohne).
- Kosten der Zombie-Suche am MP-Server: je Hirn-Takt (1,5 s, bei Gefahr 0,75 s) bis 1500 Zombies x 2 Java-Aufrufe, nur wenn ein Junges geladen
  ist -- gedeckelt, aber nicht "selten erneuert" im engen Sinn; im SP mit Bandits nur Lua-Tabelle. Nicht gemessen.
- Ob die Optionen-Seite erscheint und ihre Werte geladen sind, wenn die Mod erst mit dem Spielstand aktiv wird (`MainOptions.lua:2791` laedt
  beim Bau des Fensters) -- wie OBERFLAECHE 6.

## 6. Fragen fuer Kevin (Kevin schlaeft -- nichts davon haelt den Einbau auf)
1. **A3:** Duerfen Vanilla-Lua-Bausteine, deren ganzer Code gelesen ist, die aber nirgends aufgerufen werden (`addTickBox`, `addSlider` der
   Optionen-Seite), wie ein Beleg zaehlen? Empfehlung: ja, ausdruecklich als Regel-Auslegung festhalten.
2. **A5:** Der Karten-Einhaengeblock ist dieselbe Form wie in NPC Crew (deine eigene Mod). Reicht ein ehrlicher Hinweis im Kopf, oder soll er in
   eigener Form geschrieben werden? Empfehlung: ehrlicher Hinweis.
3. **A1:** keine Frage noetig -- dein Auftrag "nie neu als found/shy" deckt die Ein-Zeilen-Nachbesserung.

Statisch geprueft, nicht gespielt. Nach einem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).
