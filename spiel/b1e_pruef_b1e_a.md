# Lauf baer-b1e: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 11.11.2026 abends. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (60 Dateien laut
`staging_dateien.txt`), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt`. Gelesen gegen Vanilla 42.22.2
(`media/lua`, `media/AnimSets`), Bandits 42.22 + common, NPC Crew v3.14.73 (`42/media/lua`, Landkarte), Test-Mod NCBearTest (alles nur gelesen).
**Geaendert: nur diese Datei.** Meine Laeufe und Ausgaben liegen im Scratchpad (`.../scratchpad/pa/`: Diffs, Trockenlaeufe, Probe, Attrappen-
Ausgaben); die Probe des Uebernahme-Skripts lief nach `.../scratchpad/pa/probe/` (nicht unter Zomboid, nicht in NPC Crew). Kein git, kein Spiel.

## 0. Ergebnis

| Pruefung | Ergebnis (selbst gelaufen) |
|---|---|
| Staging gegen Test-Mod (MD5 jeder Datei) | 60 Dateien, jede MD5 = Spalte in `staging_dateien.txt`, Zustand je Datei stimmt (9 neu / 35 ueberschreibt / 16 gleich); altes Junges 6c3f0a96 / 2ee25f24 = `_arbeit/baer_baby/entwurf/` = `NCBearBenchCubAlt.glb` |
| Engine-Aufrufe in B1e (jede hinzugefuegte Zeile aller 21 geaenderten Lua-Dateien) | alle mit echter Vanilla-/Bandits-Fundstelle, gleiche Argumenttypen; **Jar-only: keiner**; Seite: 1 Aufruf am MP-Server ohne Vorbild (A2, nur Optik, im Code ehrlich markiert) |
| Neue Art `ncbeargrown` + Modell-Skript | richtig angelegt (Kopie der Junges-Art, eigene stages/breeds/genes, `NCBear_Body` liegt in `T:media/scripts/nc_bear_tier.txt`, Textur `NCBear.png` 4cfdb177 da); Kollisionsprobe 16 Muster x 4 Orte: 0 Treffer |
| Alte NCBear*-Dateien | keine im Staging ausser unserer Bench; kein Code beruehrt `"bear"`/`"bearstag"`/`"ncbearcubalt"` (nur die alte Naht `NOT_TENDED["bear"]`, unveraendert) |
| Testbefehle / Testmenues ausserhalb der Bench | 0 (Bench `NCBearBenchCub.lua` nur SP, `ready()` :76-81) |
| Texte 7 Sprachen | UI.json 157 / IG_UI.json 4 (EN 7: 3 alte Test-Schluessel, Altlast) / Sandbox 60; Paritaet, Platzhalter, `%%`, sortiert, Round-Trip, kein BOM/CR, CN nur Vanilla-CN-Zeichen (3512 Zeichen gesammelt): **0 Fehler**; `U.EN` 157 = EN wortgleich; 0 alte Schluessel geaendert |
| Uebernahme Trockenlauf `--staging --vor-b5a` | **OK, 0 Fehler, 28 Warnungen**, Ausgabe byte-gleich mit `trockenlauf_b1e_vor_b5a.txt` |
| Uebernahme Trockenlauf ohne `--vor-b5a` | **26 Fehler = 24 Altlasten + 2 `ALT_DEFS`**, sonst nichts; byte-gleich mit `trockenlauf_b1e.txt` |
| Uebernahme Probe (Scratchpad) | **OK, 0 Fehler, 28 Warnungen**, 60 Dateien; Ausgabe bis auf den Pfad byte-gleich mit `probe_b1e_ausgabe.txt`; Pruefer je kopierter Datei gruen; zusammengefuehrte Texte: 3814 -> 3971 / 92 -> 151 / IG_UI neu 4, je Sprache sortiert, Round-Trip, 0 NC-Schluessel verloren oder geaendert |
| Vier Lua-Pruefer (25 Lua-Dateien) | luacheck 0 failed; scopecheck 0; localcount hoechstens 30 aktiv (Registry.lua :100) / 77 insgesamt (World.lua :664); luacheck_pz 18 x W113 = bekannt (15 Bench, 3 Aktionsklassen Menu.lua :89/:100/:110); luac5.1 -p 0; LF, ASCII |
| Attrappen | alle gruen, Zahlen in 6 |
| Befunde | **0 blocker, 0 major, 6 minor** (A1-A6) |

## 1. Staging
`find mod -type f` = 60; je Datei MD5 gegen Test-Mod und gegen die Liste: 0 Abweichungen. Diff Test-Mod -> Staging je Lua-Datei (Zeilen):
Marker 429 (neu geschrieben), Grow 181, Stats 99, Bench 82, Defs 74, World 63, Bear 50, Client 45, Ride 43, Pet 34, Heal 26, Hud 24, Menu 17,
Follow 16, Options 14, Rules 13, Registry 11, Feed 9, Guard 6, Server 4, NameBox 3; Map, Crew, Food, Bait 0.

## 2. Engine-Aufrufe (jede neue Zeile; Fundstelle selbst nachgelesen)
| Aufruf (Datei) | Fundstelle im Code-Kommentar | nachgelesen | Seite |
|---|---|---|---|
| `animal:getAnimalType()` (Bear.lua `B.BodyKind`) | V `client/ISUI/Animal/ISAnimalUI.lua:65`, `shared/Definitions/animal/ButcheringUtil.lua:13` | ja, Tier, kein Argument | Client + shared |
| `a:getSquare()` (World.lua `B.SwapSpot`) | V `shared/TimedActions/Animals/ISPetAnimal.lua:6` | ja (`self.animal:getSquare()`) | shared |
| `a:getX/getY/getZ()` (World.lua) | V `ButcheringUtil.lua:575-577` | ja | shared |
| `addAnimal(getCell(), x, y, z, Art-Text, Rasse, false)` (World.lua, nur `kind` statt `B.CUB`) | V `server/ClientCommands.lua:809` (`args.type` Text) | ja | Server/SP |
| `AnimalDefinitions.getDef(Text):getBreedByName(Text)` | V `ClientCommands.lua:808` | ja | Server |
| `n:faceThisObject(Spieler)` am Tier (Grow.lua `B.BodySwap`) | V `ISPetAnimal.lua:17` | ja (`self.animal:faceThisObject(self.character)`) | **nur in `update()` einer Zeitaktion; am MP-Server kein Vorbild -> A2** |
| `getTimestampMs()` (Grow.lua `B.BodyBusy`) | V `server/Foraging/forageServer.lua:456` | ja | Server |
| `sq:getX/getY/getZ()` (Grow.lua `B.BodySwap`) | -- (keiner in Grow.lua) | belegt im Mod: V `client/DebugUIs/DebugContextMenu.lua:636` (World.lua :218, Ride.lua :18) -> A6 | -- |
| `character:setVariable("AnimalSizeY", Zahl)`, `("animal", "cow")` (PetAction) | V `ISPetAnimal.lua:32`, `:39`; Knoten `AnimSets/player/petanimal/petcow.xml` (Bedingung `animal` = `cow`, :15-19) | ja | Client/SP |
| `ISUIElement:derive`, `require "ISUI/ISUIElement"` (Marker) | V `client/Chat/ISAlert.lua:1`, `:3` | ja | Client |
| `ISUIElement.new(self, x, y, w, h)` | V `client/ISUI/ISUISprite.lua:71`, `ISUI/Maps/ISMiniMap.lua:345` | ja | Client |
| `drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | V `client/Chat/ISChat.lua:418`, `DebugUIs/ISSpawnVehicleUI.lua:171` | ja | Client |
| `drawTextCentre(text, x, y, r, g, b, a, UIFont.Small/Medium/Large)` | B `client/BanditEventMarkers.lua:176`; V `DebugUIs/StashDebug.lua:86`; V `Chat/ISAlert.lua:35` | ja | Client |
| `DrawTextureAngle(tex, cx, cy, Grad)` | V `client/Fishing/TensionUI.lua:21`, `ISUI/Fireplace/ISKnob.lua:24`; B `BanditEventMarkers.lua:192` | ja (Bildgroesse nur NUR JAR, als solche markiert) | Client |
| `setVisible`, `initialise`, `addToUIManager`, `removeFromUIManager` | V `ISCollapsableWindow.lua:70`, `Chat/ISAlert.lua:54-55`, `ISAnimalContextMenu.lua:746-747`, `ISUIElement.lua:1373` + `ISMap.lua:116` | ja | Client |
| `setX/setY/setWidth/setHeight(Zahl)` | V `client/ISUI/ISToolTip.lua:78-79`, `:173-174` | ja | Client |
| `getCore():getScreenWidth()/getScreenHeight()` | V `client/Challenge/WinterIsComing.lua:18` | ja | Client |
| `getTexture("media/ui/...png")` | V `client/Chat/ISChat.lua:921` | ja | Client |
| `getSpecificPlayer(0)`, `p:isDead()`, `p:getX()/getY()`, `p:getModData()` | V `Farming/CFarmingSystem.lua:45`, `Context/ISMenuContextWorld.lua:37`, `Fishing/TensionUI.lua:11`, `Entity/ISUI/BuildRecipe/ISBuildRecipePanel.lua:48` | ja | Client |
| `Events.OnTick/OnGameStart/OnResolutionChange.Add` | V `Chat/ISChat.lua:943`, `:1186`; `ISUI/PlayerData/ISPlayerData.lua:185`, `:206` | ja | Client |
| `function X:onMouseDoubleClick(x, y)` | V `client/ISUI/ISButton.lua:66`; B `BanditEventMarkers.lua:19-21` | ja | Client |
| Bandits nur lesen: `["BanditEventMarkerPlacement"]`, `.markers`, `m.x/m.y`, `m:getDuration()`, `m:getIsVisible()` | B `BanditEventMarkerHandler.lua:17`, `:22-23`; B `BanditEventMarkers.lua:88`, `:142`, `:235-236`; V `ISUIElement.lua:676` | ja; alle hinter `BanditEventMarker == nil` bzw. `h == nil`; **0 x `BanditEventMarkerHandler.set`** | Client |
| `math.atan2`, `math.deg`; Pfeilwinkel +135 | V `ISKnob.lua:137`, `Foraging/ISBaseIcon.lua:212`; +135 = Bandits `:120-121` umgerechnet (`(rad x 180/pi + 270 + 45) % 360`, rad = atan2 + pi) | ja | Client |
| Kreisfarbe 1,0 / 0,52 / 0,09 | = Bandits-Mischung `colorBlend` (`BanditEventMarkers.lua:150-157`, Farbe quadriert: 0,72^2 = 0,52, 0,30^2 = 0,09) der alten Farbe (Test-Mod `BanditsNPCBearMarker.lua:46`) | ja | -- |
| `PZAPI.ModOptions` `addComboBox`/`addItem` | V `client/PZAPI/ModOptions.lua:121`, `:131` (Lua-API, `getText(name)` :132); Texte `"100%%"` wie V `UI_optionscreen_ActionProgressBarSize1` mit `getText` ohne Argumente (V `OptionScreens/MainOptions.lua:1244`) | ja | Client |
| Kevins Ausnahmen `pathToLocation`, `animalRunning` | nur `B.MoveTo` / Laerm-Wache (Tier-Regeln der Probe) | ja | Schreiber |
Bilder: eigene Zeichnung (`ober_werkzeug/marker_bilder.py`, Bandits-PNG nur nachgemessen, keine Datei geoeffnet), 10 PNG RGBA in Plan-Groesse
(96, 288, Pfeile 96/120/144/192/240/288 = 96 x Stufe); `bilder_pruefen_b1e.py --tmp`: Werkzeug erzeugt byte-gleich.

## 3. Neue Art, Modell-Skript, Kollision
- `S:shared/BanditsNPCBearDefs.lua:144-211`: Kopie der Junges-Definition per `pairs`, `breeds`/`stages`/`genes` neue Tabellen; `bodyModel
  "NCBear_Body"` (`T:media/scripts/nc_bear_tier.txt`: `animationsMesh NCBear` -> `Skinned/NCBear.glb` 08ec7806); Rasse `texture*` `"NCBear"`
  (= `T:shared/NCBearDefs.lua:40-41`); `minSize` 0,72 == `B.CFG.swapSize` (`S:shared/BanditsNPCBear.lua`), `maxSize` 1,35; Avatar = buck, Teile =
  `buckwhitetailed` (V `AnimalPartsDefinitions.lua:445`); Gruppe `ncbear` -> NPC Crews `NOT_TENDED` (Naht 1, `BanditsNPCBearCrew.lua:34`);
  Name `IGUI_AnimalType_ncbeargrown` x 7. Die Art `"bear"` und ihre Definition (`T:shared/NCBearDefs.lua:101`) werden nicht beruehrt;
  `NCBearFight.lua:1787` greift nur `== "bear"`.
- Kollisionsprobe (grep, wie geschrieben): `ncbeargrown`, `NCBearGrown`, `B.BIG`, `BodyKind`, `MarkerSize`, `BanditsNPCBearMarker`,
  `BanditsNPCBearCub_marker288`, `NoteBd`, `BodySwap`, `BodyBusy`, `MarkerFactor`, `MarkerLayout`, `U.TB`, `BODY_TYPE`, `TYPE_BODY` in NPC Crew
  `42/media/lua` + Landkarte, Vanilla `media/lua` + `media/scripts`, Bandits 42.22 + common, Test-Mod `42/media` (alter Stand): **0 Treffer**;
  `UI_BN_Bear_` nur in der Test-Mod (eigene Texte). Uebernahme-Probe: Globale/Modultabellen "Kollision: keine".

## 4. Trennung, Bench, Regeln
- KERN (shared/server) ruft nichts aus `client/`; OBERFLAECHE ruft vom Kern `B.BodyKind`, `B.DistXY`, `B.ViewOf`, `B.CFG`; Bench zusaetzlich
  `B.BodySwapReady`, `B.BodyWant`, `B.FindAnimal`, liest `B._s` (nur SP). `B.BodyBusy` liegt in `server/BanditsNPCBearGrow.lua` hinter
  `if isClient() then return end` (:1) -- die Zeitaktionen fragen `if B.BodyBusy`, SP-Zweig `not isClient() and not isServer()` (Feed :65, Pet :90).
- Kein neuer `sendClientCommand`/`sendServerCommand`, keine neue Sandbox-Option, keine neue Lua-Datei, kein `next`, keine neuen pcall
  (die drei alten um eigene Takt-Rumpfe: Map :160, Guard :231, Server :606/:1040; der Tausch laeuft im Hirn-Takt darunter, alle seine Aufrufe belegt).
- Deckel: Merk-Tabellen der Markierung 16, Schleife `B.BodyBusy` 64, Marke `busyMs` 20 s. Je Bild: 3 Bilder + 1 Text, Takt 400 ms.

## 5. Texte
24 neue UI-Schluessel + `IGUI_AnimalType_ncbeargrown`, in allen 7 Sprachen gelesen: Big-Fassungen je mit Grundschluessel, gleichen `%1`, anderem
Text, Grammatik/Genus passend (PTBR "Ele", ES "Te espera", FR "Il", RU "Он"); keine Woerter spawn/debug/bench/cheat/test. 23 EN-Schluessel stehen
nicht woertlich in der Lua: 8 `Dir_*` und 15 `*Big` -- alle zusammengesetzt (`U.TB`/`U.NoteText` `key .. "Big"`, `B.DirOf`). Luecke: A1.

## 6. Lua-Pruefer und Attrappen (selbst gelaufen, lua5.1 / Python, Ausgaben verglichen)
| Lauf | Ergebnis | gegen gespeichert |
|---|---|---|
| `kern/` | 136 / 0 | byte-gleich `ergebnis.txt` |
| `b1b_kern/` | 204 / 0 | byte-gleich `ergebnis.txt` |
| `b1c_kern/` | 192 / 0 | byte-gleich `ergebnis_b1e.txt` |
| `b1d_kern/` | 162 / 0 | byte-gleich `ergebnis_b1e.txt` (Aufruf als `run.lua` im Ordner) |
| `b1e_kern/` | 153 / 0 | byte-gleich `ergebnis.txt` |
| `gesamt/` (Staging) | **1672 / 0**, 3 `***` = gewollte Heilungen 18c/19f/20e | byte-gleich `ergebnis.txt` |
| `gesamt/` gegen MEINE Probe | 1672 / 0 | byte-gleich `ergebnis_probe.txt` |
| `ober/` / `b1b_ober/` / `b1c_ober/` / `b1d_ober/` / `b1e_ober/` (Kern-Attrappe + echter Kern) | 116+117 / 144+134 / 155+142 / 174+176 / **218+218**, je 0 Fehler | -- |
| `pruef_b/` | 7 OK, 1 Befund | byte-gleich `ergebnis_b1b_nach.txt` |
| `pruef_b1b/run_nach.lua` | 13 OK, 3 Befunde | byte-gleich `ergebnis_b1c.txt` |
| `pruef_b1c/` | 6 OK, 0 Befunde | byte-gleich `ergebnis_nach.txt` |
| `pruef_b1d/` | 10 / 0, 3 Befunde | byte-gleich `ergebnis_nach.txt` |
| `xref_b1e.py` | 0 Luecken, 3 Hinweise | byte-gleich `xref_b1e.txt` |
| `gegenprobe_b1e.py` | 30 von 30 erkannt | -- |
| `probe_regeln_b1e.py` | 8 von 8 wie erwartet | -- |
| `texte_pruefen_b1e.py --tmp` / `bilder_pruefen_b1e.py --tmp` | 0 / 0 | -- |
| `texte_pruefen.py`, `_b1b`, `_b1c`, `_b1d` | je 0 | -- |
| `belege.py`, `_b1b`, `_b1c`, `_b1d`, `_b1e` | 0/112, 0/51, 0/89, 0/23, 0/53 | -- |
(`pruef_b1b/run.lua` ohne Kahlua-Zeichenmodell: 10 OK / 6 Befunde -- der bekannte B1b-Stand, durch `run_nach.lua` abgeloest.)

## 7. Befunde
- **A1 (minor, Text):** Ab Halbstark sagen weiter "cub": `Why_Gone` "The cub is gone." und `Note_Dead` "The bear cub is dead." (= Z1 des
  Zusammenbaus, bestaetigt: `server/BanditsNPCBearRegistry.lua:491`, `:499`, `Server.lua:158`) **und zusaetzlich, nicht in Plan 6.8 und nicht in Z1:**
  das Welt-Menue `Menu_Hold` "Hold out food for the cub" mit Tipp `Menu_HoldTip` "... and the cub comes closer." -- `client/BanditsNPCBearMenu.lua:409-416`
  (`holdWanted`: zahmer Eintrag des Besitzers, nicht folgend -> true; die Sicht kennt beide Koerper) und `:422`/`:428` (`U.T`, kein `U.TB`). Steht
  nur der eigene bleibende grosse Baer in der Naehe, heisst der Menuepunkt "for the cub". Vorschlag: im naechsten Lauf (mit Z1) eine neutrale bzw.
  Big-Fassung (`Menu_HoldBig` "Hold out food for your bear" + Tipp, Wahl nur, wenn alle nahen Baeren gross sind), 7 Sprachen; Frage 1.
- **A2 (minor, Beleg-Seite):** `n:faceThisObject(p)` am neuen Koerper (`server/BanditsNPCBearGrow.lua:523`) laeuft im MP am Server. Vorbild
  `ISPetAnimal.lua:17` steht in `update()` einer Zeitaktion; grep `faceThisObject` in V `media/lua/server` + `shared` und in Bandits 42.22/common:
  am Server kein Aufruf an irgendeiner Figur (Bandits nur `client/BanditUpdate.lua`). Argumenttypen gleich (Tier, Spieler), im Code als
  "am MP-Server Wirkung ungeprueft, nur Optik" markiert (:499-500). Vorschlag: so lassen und im MP-Test ansehen, oder auf den SP-Zweig begrenzen.
- **A3 (minor, Hausregel):** `server/BanditsNPCBearGuard.lua:306` `gap = B.BodyGap(B.BodyNow(rec))` reicht die zwei Rueckgaben direkt als
  Argumente weiter -- gegen die Regel "Mehrfachrueckgaben erst in Locals holen" (CLAUDE.md 5). In Lua 5.1 richtig (Attrappen gruen); faellt
  `sz` weg, gaebe `B.BodyGap` still 0. Vorschlag: `local bd, bsz = B.BodyNow(rec); gap = B.BodyGap(bd, bsz)` (wie `Follow.lua` B.FollowStep).
- **A4 (minor, Kommentar-Zahl):** `shared/BanditsNPCBearStats.lua:297` nennt "Tag 45: ~0,27"; gerechnet (1,0448 x 0,982 x 1,5 - 1,12) / 2 =
  **0,21** (= PLAN_B1E.md 2.4; 0,27-0,29 waere Tag 60). Nur Kommentar.
- **A5 (minor, ungeprueft):** Disc/Ring/Symbol und `arrow288` sind 288 px; CLAUDE.md 8 haelt fest "Texturen deckelt die Vorgabe-Option
  'Max. Texturgroesse' auf 256" (gelernt an Kleidung). Kreis/Symbol gehen ueber `drawTextureScaled` (Groesse bleibt), der Pfeil ueber
  `DrawTextureAngle` in Bildgroesse (NUR JAR, Marker.lua :152) -- betroffen waere nur die Stufe 300 % (`arrow288`); Auto bei 2054 nimmt `arrow192`.
  Zusammenbau 7.4 nennt es offen. Vorschlag: bei Kevins Test einmal 300 % ansehen.
- **A6 (minor, Fundstelle fehlt):** `B.BodySwap` (`server/BanditsNPCBearGrow.lua:513`, `:523`, `:526`) ruft `sq:getX()/getY()/getZ()` an der
  Kachel ohne Fundstelle im Kommentar dieser Datei (belegt im Mod: V `client/DebugUIs/DebugContextMenu.lua:636`, genannt in World.lua :218 und
  Ride.lua :18). Vorschlag: eine Zeile im Kommentar ueber `B.BodySwap`.

Sonst nichts gefunden: kein Jar-only-Aufruf, kein Aufruf ohne Vanilla-/Bandits-Vorbild, keine Aenderung an alten NCBear*-Dateien, keine
Testbefehle ausserhalb der Bench, Uebernahme absichtlich rot nur durch die 26 erwarteten Altlasten.

## 8. Fragen fuer Kevin (er testet gerade; nichts davon haelt den Einbau auf)
1. A1/Z1: Sollen auch "The cub is gone.", "The bear cub is dead." und das Welt-Menue "Hold out food for the cub" beim grossen Baeren "bear" sagen?
   Empfehlung: ja, im naechsten Lauf.
2. A5: Markierung einmal auf 300 % stellen -- ist der Pfeil gleich gross wie der Kreis? (Wenn nicht: Stufe 300 % streichen oder Pfeil anders.)

## 9. Ungeprueft
Alles Laufzeit-Verhalten (Tausch, Groesse, Tempo, Fussgleiten, Haltung, Schild, Markierung bei 4K, Klickflaeche, Aufloesungswechsel); MP-Reihenfolge
`addAnimal`/`removeAnimal`; ob UI-Bilder > 256 px gedeckelt werden; Lade-Reihenfolge `AnimalAvatarDefinition` vor unserer Defs-Datei (Muster seit
B1a unveraendert). Statisch geprueft, nicht gespielt.
