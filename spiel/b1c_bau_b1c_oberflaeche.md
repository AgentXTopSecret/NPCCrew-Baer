# Lauf baer-b1c: Bau OBERFLAECHE (B1c)

Stand 11.11.2026 Nacht. **Statisch geprueft, nicht gespielt.** Rolle: Bauer OBERFLAECHE (client/ mit ISUI/ und Bench, Texte in sieben
Sprachen, Sandbox-Texte, sandbox-options.txt, Bild). Gebaut nur im Staging `_arbeit/baer_zaehmen/mod/42/media/`; nichts in der Test-Mod,
NPC Crew, Vanilla oder Bandits geschrieben. Kein git, kein Spielstart. shared/ und server/ (KERN) nur gelesen.
Plan: `PLAN_B1C.md` 1.5, 1.7-1.10, 4, 6.4-6.9, 7.2 woertlich; Abweichungen/Zusaetze in `schnittstelle_aenderungen.md`, Abschnitt
"B1c OBERFLAECHE" (13 Punkte, keiner aendert die Schnittstelle zum KERN). Nach dem Einbau muss Kevin das Spiel neu starten (Lua laedt nur
beim Start).

## 1. Was gebaut ist (je Auftragspunkt, nur OBERFLAECHE)

| Auftrag | Was | Datei |
|---|---|---|
| 5 Unstuck | Rechtsklick am eigenen gezaehmten Jungen: "Call to me" nach "Name the cub". Fehlt bei fremden, ungezaehmten, mitfahrenden. Grau mit Grund: im Fahrzeug (`Why_InCar`), Abklingzeit laeuft (`Why_CallWait`, Minuten aufgerundet, mind. 1; Rest = `callWait` der Sicht minus Zeit seit `U.viewAt`). Tooltip nennt die Sandbox-Minuten. Klick = genau eine Bitte `B.Ask(p, "Call", { id })` (SP direkt, MP `sendClientCommand`, Rolle user). | `client/BanditsNPCBearMenu.lua` |
| 7 Markierung | Pfeil oben auf das wilde Junge des Spielers (`B.View.me.wild`), solange "new" und noch 60 s nach dem ersten "shy", das der Client sieht. Bandits' `BanditEventMarkerHandler.set` mit fester Id, Kevins Symbol, Farbe 1.0/0.72/0.30, Text "Bear cub nearby"; je 400 ms nachgefuehrt (Lage live von der Client-Kopie, sonst Sicht-Kachel + 0,5); Aus genau einmal mit Dauer 0. Doppelklick respektiert (F6), Versatz 100 px bei Ueberlappung (F5), eigenes altes Element wird aus dem UIManager genommen (Deckel). Nur mit Bandits (Riegel). | `client/ISUI/BanditsNPCBearMarker.lua` (neu) |
| 8 Karte | Mini-Karte und grosse Karte: je eigenem Baeren (tame/missing als Besitzer, fed als Gebundener; SP `__sp`, MP nie) Kevins Symbol, 14 px bzw. 18..28 px nach Zoom; live Alpha 1,0, sonst letzte Kachel Alpha 0,55; mitfahrend/fremd/wild nie; ausserhalb des Fensters nie. render-Methoden einmal umwickelt (Datei-Ende + OnGameStart, nie ueber einen fremden Aufsatz). | `client/ISUI/BanditsNPCBearMap.lua` (neu) |
| 9 Anzeige-Optionen | Seite "NPC Crew: Bear" unter Optionen -> Mods: TickBox "Namensschilder" (an), Schieber Groesse 100/150/200 (Small/Medium/Large). Platzhalter-Kommentar fuer spaetere Werte (Leben, Ausdauer ..., DODGE). Lesen nur ueber `U.Opt(id, vorgabe)`, 1 s zwischengespeichert. | `client/BanditsNPCBearOptions.lua` (neu) |
| 9 (Wirkung) | Hud: "Namensschilder aus" -> keine Schilder ueber gezaehmten Baeren (eigene und fremde), Zaehm-Balken bleibt; Groesse waehlt Schrift fuer Schild UND Balken (Balken/Abstaende x Hoehenverhaeltnis); `ride`-Eintraege nie "gewollt"; `U.CubObj`/`U.CubPos` fuer Markierung und Karte. | `client/ISUI/BanditsNPCBearHud.lua` |
| 4/5/6.7 Texte | 15 neue UI-Schluessel x 7 Sprachen, `Note_StayCar` und `Menu_FollowTip` neu, ES `Hud_Pet` "Caricia: %1"; `U.EN` wortgleich; `U.viewAt` bei jeder Sicht. | `client/BanditsNPCBearClient.lua`, `shared/Translate/<L>/UI.json` |
| 5.1 Sandbox | `BearRideDistance` (3..40, 15) und `BearCallCooldownMinutes` (0..60, 5) vor `BearLog`, Titel + Tooltip x 7 Sprachen (Zahlen = `B.OPTS` des KERNs, geprueft). | `sandbox-options.txt`, `shared/Translate/<L>/Sandbox.json` |
| 7 Bild | Kevins Symbol byte-gleich kopiert (MD5 9e45e9368ef389aa9b831689d7bd6721, 4429 Bytes, 96 x 96). | `ui/BanditsNPCBearCub_marker.png` (neu) |
| 6.9 Bench | `NCBear_CubForget`, `NCBear_CubMark`, `NCBear_CubCalm`, `NCBear_CubGuard`, `NCBear_CubRide`, `NCBear_CubCallReset`; `NCBear_CubInfo` mit u/gen/r/ride/healed und Register v/ep/n; `NCBear_CubSet`-Hilfe nennt die B1c-Gruppen; Rechtsklick "NC Bear" +2 (zehn). Nur SP, wird nie kopiert. | `client/NCBearBenchCub.lua` |
| 10 Kleinkram | ES "Caricia: %1" (FR bleibt). N1-N3 liegen beim KERN (Gehen, `B.CleanName`, `B.BuildView`). | Texte |

## 2. Dateien im Staging (`_arbeit/baer_zaehmen/mod/`)

| Pfad | MD5 | Bytes | Art |
|---|---|---|---|
| 42/media/lua/client/BanditsNPCBearClient.lua | 3a8eb6df488ac4a2fdd2f91e2126ed2f | 17872 | geaendert |
| 42/media/lua/client/BanditsNPCBearMenu.lua | 03e0ce5bfbba3cc839be1441dce5a957 | 23436 | geaendert |
| 42/media/lua/client/BanditsNPCBearOptions.lua | 0ea244e0c12884a0837d10064419d5d3 | 4965 | **neu** |
| 42/media/lua/client/ISUI/BanditsNPCBearHud.lua | c3fa8c1674598d82b6f1f77559808ef5 | 26434 | geaendert |
| 42/media/lua/client/ISUI/BanditsNPCBearMarker.lua | 9b39c9b8a2ca539e80e51301c9440a91 | 10638 | **neu** |
| 42/media/lua/client/ISUI/BanditsNPCBearMap.lua | cba63bca1268ff34ebfc1dd4ea809903 | 8780 | **neu** |
| 42/media/lua/client/NCBearBenchCub.lua | 7b41b80a1dfdabbec5b40d29749b11c0 | 34433 | geaendert (Bench, nie kopieren) |
| 42/media/ui/BanditsNPCBearCub_marker.png | 9e45e9368ef389aa9b831689d7bd6721 | 4429 | **neu** |
| 42/media/sandbox-options.txt | 2b61e74acfa16dcef0155fd87b374c1f | 5536 | geaendert |
| 42/media/lua/shared/Translate/{EN,PTBR,RU,KO,ES,CN,FR}/UI.json | EN f99403888c559f74e18e8b2c93f48501, PTBR e120ad0f1fdfcce61123f2154051a3ff, RU 4433bd6eef93fb614a1ddc3cd1c33835, KO 0696c78a97599215a18cad3df7ca9a3c, ES f866e77b20a29afacbd01a69170e5477, CN b921944ed0e481aeb47757ddd28ac703, FR 939236f63b7a29b014695a66f05e317c | 6721 / 7246 / 9953 / 7993 / 7140 / 6737 / 7459 | geaendert |
| 42/media/lua/shared/Translate/{EN,PTBR,RU,KO,ES,CN,FR}/Sandbox.json | EN 179726769c35ea4e952988efc2d0e673, PTBR fc23dde1ce7c1628cd306b1934083aed, RU bc833325cb20789dddd24bb35bc9a4a6, KO ce8844d6569656798400cdb2aa3f5f0a, ES 5e3b8d0b996e459eb624fa08d95e641e, CN 0f9931578f9d0bba20399222bb4dee86, FR fcb557152362f6257ebd2634a17fe5ca | 5463 / 5962 / 8415 / 6360 / 5903 / 5424 / 6052 | geaendert |

Unveraendert von der OBERFLAECHE: `client/ISUI/BanditsNPCBearNameBox.lua` (d7b9c92f16ce962e8a135b6a94d34660), `IG_UI.json` x 7, alle
`shared/TimedActions/*`. Werkzeug und Pruefer ausserhalb des Staging: `ober_werkzeug/texte_b1c.py` (neu), `attrappe/b1c_ober/run.lua`,
`texte_pruefen_b1c.py`, `belege_b1c.py` (neu); geaendert `attrappe/b1b_ober/run.lua` (4 Erwartungen), `attrappe/ober/texte_pruefen.py`
und `attrappe/b1b_ober/texte_pruefen_b1b.py` (Schluesselliste +15). Alle Lua-Dateien ASCII, LF, ohne BOM; JSON UTF-8 ohne BOM, LF.

## 3. Engine-Aufrufe der OBERFLAECHE (neu in B1c) mit Fundstelle (gleiche Argumenttypen)

V: = Vanilla `media/lua/` 42.22.2, B: = Bandits `42.22/media/lua/`. Jede Zeile von `attrappe/b1c_ober/belege_b1c.py` gegen die heutigen
Dateien geprueft: **0 von 89 abweichend**. Jar-only-Aufrufe: **keine**. Nicht benutzt: `drawTextZoomed`, `PZMath`, `setVariable`,
`pathToLocation`, `getStress`, `B.CreateCub`/`B.RemoveCub` (alles KERN bzw. verboten).

| Aufruf | Datei | Fundstelle | Bemerkung |
|---|---|---|---|
| `PZAPI.ModOptions:create(id, nameKey)` | Options | V:client/PZAPI/ModOptions.lua:247; Aufrufer B:client/BanditModOptions.lua:12 | reines Vanilla-Lua (Tabellen) |
| `options:addTitle(key)` | Options | V:...ModOptions.lua:28; B:client/BanditModOptions.lua:13 | Lua |
| `options:addTickBox(id, key, true, tipKey)` | Options | V:...ModOptions.lua:64 (Definition) | reines Lua (Tabellen), kein Engine-Aufruf; Aufrufer in Vanilla/Bandits keiner (Bandits ruft auf derselben Seite `addKeyBind`), die Funktion selbst ist gelesen -- die eiserne Regel gilt Engine-Methoden |
| `options:addSlider(id, key, 100, 200, 50, 100, tipKey)` | Options | V:...ModOptions.lua:206 (Definition) | wie oben |
| `PZAPI.ModOptions:getOptions(id)`, `page:getOption(id)`, `opt:getValue()` | Options | V:...:255, :24, :67/:215; Aufrufer B:shared/BanditCompatibility.lua:98-99 | Lua |
| Namen/Tooltips durch `getText` | (Vanilla) | V:client/OptionScreens/MainOptions.lua:2801, :2804, :2810-2812, :3020 | darum Schluessel |
| `getTimestampMs()` | Client, Menu, Options, Marker, Map | V:client/Foraging/ISBaseIcon.lua:485 | |
| `getTextManager():getFontHeight(UIFont.Medium)` | Hud | V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8 | einmal je Schrift |
| `getTextManager():getFontHeight(UIFont.Large)` | Hud | V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6 | einmal |
| `self:drawTextCentre(s, x, y, r, g, b, a, UIFont.Medium)` | Hud | V:client/ISUI/ISFitnessUI.lua:204 | |
| `self:drawTextCentre(s, x, y, r, g, b, a, UIFont.Large)` | Hud | V:client/Chat/ISAlert.lua:35 | |
| `a:getX()/getY()/getZ()`, `a:isExistInTheWorld()` | Hud, Map | V:client/TimedActions/ISContextualActions.lua:100, V:client/ISUI/Animal/ISAnimalUI.lua:15 | wie B1b |
| `playerObj:getVehicle()` | Menu | V:client/ISUI/Hutch/ISHutchMenu.lua:8 | wie B1b |
| `Events.OnTick.Add(f)` | Marker | V:client/Chat/ISChat.lua:943 | gedrosselt 400 ms |
| `Events.OnGameStart.Add(f)` | Marker, Map | V:client/Chat/ISChat.lua:1186 | |
| `getSpecificPlayer(0)` | Marker | V:client/Farming/CFarmingSystem.lua:45 | |
| `player:isDead()` | Marker | V:client/Context/ISMenuContextWorld.lua:37 | |
| `BanditEventMarkerHandler.set(id, icon, dur, x, y, color, desc)` | Marker | B:client/BanditEventMarkerHandler.lua:6; Aufrufer B:server/BanditServerSpawner.lua:1093, B:server/BanditServerWanderers.lua:697 | Bandits-Lua; Riegel; pcall + `B.ErrEvery` |
| `BanditEventMarkerHandler.markers[id]` | Marker | B:...Handler.lua:2, :9 | Lua-Tabelle |
| `marker:getDuration()` | Marker | B:client/BanditEventMarkers.lua:142 | Bandits-Lua |
| `marker:getIsVisible()` | Marker | V:client/ISUI/ISUIElement.lua:676; Aufrufer B:...BanditEventMarkers.lua:28 | Lua |
| `marker:setX(n)`, `marker.x/.y` | Marker | V:...ISUIElement.lua:195; Aufrufer B:...BanditEventMarkers.lua:81, :103; Felder :235-236 | Lua |
| `old:removeFromUIManager()` | Marker | V:client/ISUI/ISUIElement.lua:1373; Aufrufer V:client/ISUI/Maps/ISMap.lua:116 | Lua, Deckel |
| `ISMiniMapInner.render` / `ISWorldMap.render` umwickeln | Map | V:client/ISUI/Maps/ISMiniMap.lua:4 (erbt V:...ISUIElement.lua:1618), V:client/ISUI/Maps/ISWorldMap.lua:384 | einmal je Klasse |
| `self.mapAPI:worldToUIX(x, y)` / `worldToUIY(x, y)` | Map | V:client/ISUI/Maps/ISWorldMap.lua:478-479, V:client/ISUI/Maps/ISWorldMapSymbols.lua:347 | immer ZWEI Zahlen (Pruefer zaehlt) |
| `self.mapAPI:getZoomF()` | Map | V:client/ISUI/Maps/ISWorldMap.lua:447 | nur grosse Karte |
| `self:drawTextureScaledAspect(tex, x, y, w, h, a, 1, 1, 1)` | Map | V:client/ISUI/Maps/ISWorldMap.lua:482; Signatur V:client/ISUI/ISUIElement.lua:1065 | a, r, g, b |
| `self:getWidth()` / `getHeight()` | Map | V:client/ISUI/Maps/ISMiniMap.lua:356 (Lua V:...ISUIElement.lua:259/:266) | je Bild und Karte |
| `getTexture(pfad)` | Map | V:client/ISUI/Maps/ISMap.lua:573 | einmal (Marker: Bandits ruft es selbst) |
| Bench: `a:getModData()`; `getCell():getObjectListForLua()`, `instanceof(o, "IsoAnimal")`, `o:getAnimalType()` | Bench | V:client/ISUI/ISInventoryPaneContextMenu.lua:4127; V:client/DebugUIs/Scenarios/FenrisScenario.lua:505, V:shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29, V:client/ISUI/Animal/ISAnimalUI.lua:65 | nur SP |

pcall nur um belegte Aufrufe und nie stumm: Marker (`BanditEventMarkerHandler.set`, `removeFromUIManager`) und Karte (eigener Zeichenteil)
mit `B.ErrEvery` je 60 s; die vorige render-Methode laeuft ausserhalb (ihre Fehler bleiben, wie sie sind). Options: KEIN pcall.

## 4. Text-Schluessel je Sprache (gezaehlt, `attrappe/b1c_ober/texte_pruefen_b1c.py`)

| Sprache | UI.json | Sandbox.json | IG_UI.json |
|---|---|---|---|
| EN | 109 (94 + 15) | 50 (46 + 4) | 6 (unveraendert) |
| PTBR, RU, KO, ES, CN, FR | je 109 | je 50 | je 3 (unveraendert) |

Neu (15): `Note_RideOn`, `Note_RideOff`, `Note_Called`, `Why_CallWait`, `Why_Riding`, `Why_NoRoom` (vom KERN gemeldet), `Menu_Call`,
`Menu_CallTip`, `Marker_Cub`, `MO_Page`, `MO_Title`, `MO_TagShow`, `MO_TagShowTip`, `MO_TagSize`, `MO_TagSizeTip`. Geaendert: `Note_StayCar`,
`Menu_FollowTip` (7 Sprachen), ES `Hud_Pet`. Sandbox: `BearRideDistance`, `BearCallCooldownMinutes` (+ `_tooltip`). Gleiche Platzhalter in allen
Sprachen, sortiert, Round-Trip `json.dumps(data, indent=4, ensure_ascii=False) + "\n"`, CN: 346 verschiedene Zeichen, **alle** in Vanilla-CN.
Menue-Name je Sprache wortgleich im Sandbox-Text der Abklingzeit ("Call to me", "Venha até mim", «Ко мне», '이리 와', "Ven aquí", “过来”,
"Viens ici"). EN-Texte = Plan 6.7 (MO_TagSize mit `%%`, siehe Abweichung 5). Generator: `python -I ober_werkzeug/texte_b1c.py`; Gegenprobe
`--basis` byte-gleich mit dem Staging vor B1c.

## 5. Pruefer-Ausgaben

| Pruefer | Ergebnis |
|---|---|
| `luacheck.py` (Syntax), 8 Client-Dateien | 8 x "1 file(s) checked, 0 failed" |
| `scopecheck.py` | 8 x "0 violation(s)" |
| `localcount.py` (Grenze 200, ab 180 aufteilen) | aktiv hoechstens 39 (Bench), Hud 37, Map 21, Marker 18, Menu 18, Client 13, Options 8, NameBox 6; insgesamt hoechstens 44 (Hud) |
| `luacheck_pz.py` (nil-Globals) | 16 x W113, alle erwartet: 3 Aktionsklassen in `Menu.lua` (wie B1b, `PZ_ALLOWED`) + 13 in der Bench (eigene `NCBear_*`, `NCBearMenu`; B1b 11, +2 neue Befehle) |
| `luacheck_pz.py --unused` | 3 x W212 `self` (Maus-Funktionen des Hud, Absicht, wie B1b), 1 x W212 `player` (Bench-Menue, wie B1b); neue Dateien 0 |
| Zeilenenden / Kodierung | alle Lua ASCII + LF + ohne BOM + LF am Ende, keine Leerzeichen am Zeilenende; JSON/sandbox-options.txt LF |
| `attrappe/b1c_ober/run.lua` (neu, Kern-Attrappe) | **193 ok, 0 Fehler** |
| `attrappe/b1c_ober/run.lua ... kern` (echte shared-Dateien des KERNs) | **180 ok, 0 Fehler** |
| `attrappe/b1c_ober/texte_pruefen_b1c.py` | FEHLER gesamt: 0 |
| `attrappe/b1c_ober/belege_b1c.py` | abweichend: 0 von 89 |
| `attrappe/ober/run.lua` (B1a) / `... kern` | 116 ok, 0 Fehler / 117 ok, 0 Fehler (unveraendert gruen) |
| `attrappe/b1b_ober/run.lua` / `... kern` | 144 ok, 0 Fehler / 134 ok, 0 Fehler (4 Erwartungen gewollt nachgezogen, s. u.) |
| `attrappe/ober/texte_pruefen.py`, `b1b_ober/texte_pruefen_b1b.py` | je FEHLER gesamt: 0 (Plan-Liste +15) |
| `attrappe/ober/belege.py`, `b1b_ober/belege_b1b.py` | 0 von 112, 0 von 51 abweichend |
| `attrappe/gesamt/run.lua` (Stand ~04:00, vom KERN mitgepflegt) | 519 bestanden, 0 Fehler -- laedt die drei neuen Client-Dateien noch NICHT (ZUSAMMENBAU, Abschnitt "18 B1c") |

Gewollt geaenderte Erwartungen in `attrappe/b1b_ober/run.lua` (je mit Kommentar "B1c"): Note_StayCar-Text, Menu_FollowTip-Text,
Reihenfolge (Umschalter jetzt an drittletzter Stelle, weil "Call to me" nach "Name the cub" kommt), Bench-Rechtsklick 10 statt 8 Eintraege.

Was `attrappe/b1c_ober/run.lua` zeigt (Auszug, Plan 7.2): Seite mit Schluesseln (echtes Vanilla-ModOptions.lua), Vorgaben ohne Seite/ohne
PZAPI (Fehlerzeile), Zwischenspeicher 1 s; Call to me frei/grau (Fahrzeug, "about 2 min" bei 120 s - 10 s, mind. 1 min, Uhr rueckwaerts),
fehlt bei fremd/angefuettert/scheu/ride, genau eine Bitte mit nur der Kennung, MP per `sendClientCommand`; Hud ohne Suchlauf fuer `ride`,
TagShow aus (Balken bleibt), Groesse 150 Medium/Balken 18/14, 200 Large/Zeile 2 Medium, Large-Hoehe genau einmal geholt, je Bild kein Text,
keine Suche, kein U.Opt; Markierung mit ECHTEM Bandits-Lua: ohne Bandits kein Fehler, set(feste Id, Symbol, 1800, live-Lage, Farbe, Text),
400-ms-Takt, Sicht-Lage ohne Kopie, shy 60 s dann genau ein Aus, angefuettert/gezaehmt/Eintrag weg aus, Doppelklick -> fuer dieses Junge nie
wieder, neues Junges wieder, Spieler tot/fehlt aus, RemoveOldMarkers -> altes Element aus dem UIManager (5 Raeumungen: immer 1 Element),
Versatz 100 px nur beim Anlegen und nur bei Ueberlappung, `markerShift` 0, set-Fehler 1 Zeile/min; Karte: 3 von 7 Sicht-Eintraegen gezeichnet
(zahm live 1,0, vermisst/angefuettert 0,55; fremd/ride/wild/weit weg nie), 9 Argumente mit r/g/b = 1, je Bild und Symbol <= 2 Umrechnungen
und 1 Bild, <= 3 Objekt-Aufrufe, Liste nicht vor 500 ms, Zoom 12/13,5/15/20 -> 18/23/28/28 px, Rand-Symbol weg, Spieler-2-Karte leer, MP nur
Kontoname, Einhaengen einmal (zweiter Install, fremder Aufsatz + OnGameStart: keine zweite Huelle, Kette Vanilla 1 x / wir 1 x / fremd 1 x),
Zeichenfehler 1 Zeile/min bei weiterlaufender Vanilla-render, fehlendes Bild 1 Zeile; Bench im MP "singleplayer only", in SP alle sechs
Befehle; keine Bench-Befehle, kein `next(`, kein `:drawTextZoomed(`, kein `PZMath.` in den kopierten Client-Dateien.

## 6. Offen / ungeprueft (Testpunkte im Spiel)

- Ob die Seite "NPC Crew: Bear" im Optionen-Fenster erscheint, wenn die Mod erst mit dem Spielstand aktiv wird (Vanilla laedt die Werte beim
  Bau des Fensters, MainOptions.lua:2790-2791; Bandits und NPC Crew machen es genauso und sind gespielt) -- ungeprueft.
- `getText` mit `%%` ohne Argumente zeigt "%" (Vanilla-Vorbild ContextMenu_FullPercent) -- fuer unseren Text ungeprueft.
- Wie gross die Stufen Medium/Large ueber dem kleinen Jungen wirken (Kevins Blick; Stellwert-frei, nur 3 Stufen, F8).
- Markierung: Text unter dem Symbol setzt Bandits nur beim Anlegen (Handler :26); nach Tod/neuer Figur zeigt der Pfeil von der alten Figur aus,
  bis Bandits raeumt (Bandits-Grenze, FC 7); Lage im MP aus der Client-Kopie (Spiegel am Client-Tier oder OnlineID, wie B1a).
- Karte: Symbol liegt ueber Vanillas Kartenknoepfen, wenn es darunter faellt (nach `prev` gezeichnet, wie NPC Crew); isometrische Karte
  ueber dieselbe Umrechnung wie Vanilla -- nicht im Spiel angesehen.
- Kosten je Bild nur in der Attrappe gezaehlt, nicht im Spiel gemessen.
- Zusammenspiel mit dem echten KERN (Sicht x/y/ride/callWait, Bitte "Call", Meldungen) nur ueber die gelesenen KERN-Dateien und die
  Kern-Attrappe geprueft; der Gesamtlauf mit den neuen Client-Dateien ist Sache des ZUSAMMENBAUs.

## 7. Fragen fuer Kevin (OBERFLAECHE; Kevin schlaeft -- nichts davon haelt den Bau auf)

1. **Schildgroesse in drei Stufen** (100/150/200 = klein/mittel/gross, F8) -- reicht das? Empfehlung: ja.
2. **"Namensschilder aus"** gilt fuer alle gezaehmten Baeren, eigene und fremde; der Zaehm-Balken bleibt immer (F15). Ok? Empfehlung: ja.
3. **Abklingzeit 0 in der Sandbox:** der Tooltip sagt dann "Works once every 0 minutes". Eigenen Satz ("No waiting time.") anlegen?
   Empfehlung: lassen (0 ist nur eine Testeinstellung).
4. **"Follow me" im Auto** bleibt grau (B1b): ein bleibendes Junges steigt nicht nachtraeglich zu, nur ein folgendes steigt mit ein. Ok?
   Empfehlung: ja.
5. **Doppelklick blendet die Markierung fuer dieses Junge ganz aus** (F6), **Versatz 100 px** neben NPC Crews Pfeil (F5), **kein Kartensymbol
   fuer ein mitfahrendes Junges** (F14) -- wie im Plan; bitte beim Test ansehen.

Statisch geprueft, nicht gespielt.
