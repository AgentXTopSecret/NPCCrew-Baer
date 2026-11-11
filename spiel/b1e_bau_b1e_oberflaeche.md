# Lauf baer-b1e: Bau OBERFLAECHE (Modellwechsel ab Halbstark -- Client-Seite; groessere Markierung)

Stand 11.11.2026 (Nachmittag). **Statisch geprueft, nicht gespielt.** Gebaut nach `PLAN_B1E.md` 1.4 (Client-Teil), 1.6, 1.7, 3.2 Nr. 12-14/19/20,
6.1 (Zeilen OBERFLAECHE), 6.4-6.10, 7.2 im Staging `_arbeit/baer_zaehmen/mod/42/media/` (nichts in die Test-Mod, nach NPC Crew, Vanilla oder
Bandits geschrieben; kein git, kein Spielstart, kein Download). `shared/` und `server/` nur gelesen (KERN). Abweichungen und Zusaetze:
`schnittstelle_aenderungen.md` Abschnitt "B1e OBERFLAECHE" (10 Punkte; der Abschnitt "B1e KERN" vor dem Abschluss gelesen -- nichts davon
verlangt etwas von der OBERFLAECHE).

Vorab nachgezaehlt (Staging gegen Test-Mod, vor dem Bau): 51 Dateien, 49 byte-gleich, 2 verschieden = genau die zwei Junges-Dateien
(`models_X/Skinned/NCBearCub.glb` ee7a0cce vs. Test-Mod 6c3f0a96, `textures/Body/NCBearCub.png` 92a829fa vs. 2ee25f24) wie im Plan "Vorab".
Die legt der ZUSAMMENBAU zurueck (PLAN_B1E.md 10.1) -- nicht angefasst.

## Kurzfassung
- **Beide Koerper ueberall im Client:** Rechtsklick (Fuettern, Streicheln, Folgen/Bleiben, Name, Call to me), Namensschild, Futter
  hinhalten, Karte (ueber `U.CubObj`/`B.ViewOf`) und Bench erkennen das Junge UND den grossen Koerper -- nur ueber `B.BodyKind` des KERNs.
  Kein Art-Vergleich mit `getAnimalType()` oder `B.CUB` mehr im Client. Der Test-Baer "bear" bekommt nichts.
- **Texte je Koerper:** beim grossen Koerper sagt alles "bear" statt "cub" ("Kevin's bear", "Your bear follows you.", "Name the bear",
  "Name for your bear:", Call-Tooltip/Wartezeit) -- ueber `U.TB` und `U.NoteText` (Feld `bd` der Sicht bzw. der Meldung). 15 Big-Fassungen.
- **Namensschild** sitzt beim grossen Koerper um `tagBigK` 1,06 hoeher (Buckel): Tag 100 Anker x 4,09 (< Deckel 5). Die MP-Groessen-Probe
  setzt nur an einer Kopie der Art, die die Sicht nennt (Tauschfenster).
- **Markierung neu (Kevin: "zumindestens bei 4k"):** eigenes UI-Element nur mit Vanilla-UI-Aufrufen und eigenen Bildern. Auto waechst mit
  der Bildschirmhoehe: 1080 -> 100 %, 1440 -> 125 %, **Kevins 2054 -> 200 %**, 2160 -> 200 %, 3240 -> 300 %. Kreis 96 -> 192 px, Pfeil,
  Symbol, Text in Large. Optionen -> Mods -> "NPC Crew: Bear" -> neue Auswahl "Size of the cub marker at the top of the screen":
  Auto / 100 / 125 / 150 / 200 / 250 / 300 %. Aussehen und Verhalten wie bisher; **kommt jetzt auch ohne Bandits** (F11). Bandits wird nur
  noch gelesen (gemerkte Stelle, Ausweichen vor NPC-Crew-/Bandits-Markern), nie mehr aufgerufen.
- **Bench (nur SP):** `NCBear_CubStats()` zeigt body / want / engine type, ob der Tausch bereit ist (sonst warum), letzter Tausch,
  Fehlversuche; `NCBear_CubGrow(15)` endet mit "body big (swapped)"; `NCBear_CubClean()` raeumt beide Arten, nie "bear".
- **Texte:** 24 neue UI-Schluessel + `IGUI_AnimalType_ncbeargrown` in allen 7 Sprachen; Sandbox unveraendert.
- **9 neue Bilder** (eigene Zeichnung, nachgemessen statt kopiert); Kevins 96er-Symbol bleibt byte-gleich (Karte).
- Pruefer gruen: 4 Lua-Pruefer, Form, alle OBERFLAECHE-Attrappen (ober, b1b, b1c, b1d, **b1e 218/218** je mit Kern-Attrappe UND echtem
  Kern), `gesamt` 1172/0, alle Text-Pruefer, Bilder-Pruefer, Belege 53/53.

## Dateien

| Datei (unter `_arbeit/baer_zaehmen/`) | Art | Bytes | MD5 | Inhalt |
|---|---|---|---|---|
| `mod/42/media/lua/client/BanditsNPCBearClient.lua` | geaendert | 23685 | 5bc176b8edb2c827fd5af441d2f2e602 | `U.EN` + 24 (wortgleich EN), `U.TB`, `U.NoteText` (bd), `U.CubName` (bd) |
| `mod/42/media/lua/client/BanditsNPCBearMenu.lua` | geaendert | 24080 | fa03d7f6bdf3d9ab0667c37a98ea8461 | `B.BodyKind` statt Art-Vergleich (3.2 Nr. 12), `U.TB` fuer Menu_Name / Menu_CallTip / Why_CallWait |
| `mod/42/media/lua/client/BanditsNPCBearOptions.lua` | geaendert | 7830 | 90ac70ebc24e2b460a6bf69565a38abe | `MarkerSize` (Auswahl, 7 Eintraege, Vorgabe Auto) nach `TagSize` |
| `mod/42/media/lua/client/ISUI/BanditsNPCBearHud.lua` | geaendert | 36962 | 7d4f4a1bcf34629f548fff3bf72ca49c | Suchlauf ueber `B.BodyKind` (Nr. 13), Probe nur passende Art (Nr. 20), Schild x `tagBigK` |
| `mod/42/media/lua/client/ISUI/BanditsNPCBearMarker.lua` | **neu geschrieben** | 18804 | 0438a3d2066a9c6f3fd7ec14566371d8 | eigenes Element `BanditsNPCBearMarkerUI`, `U.MarkerFactor`, `U.MarkerLayout`, `U.MarkerTick` |
| `mod/42/media/lua/client/ISUI/BanditsNPCBearNameBox.lua` | geaendert | 4485 | 4614c6ee665f6bb558d032b3032218f9 | Titel `U.TB("UI_BN_Bear_Name_Title", v.bd)` |
| `mod/42/media/lua/client/NCBearBenchCub.lua` | geaendert, Testhilfe | 46925 | a7bea920600367e4281b58599fd2ac9b | 1.6: Koerper in Stats/Grow/Info, Clean/Mark ueber `B.BodyKind`, CubSet-Hilfe |
| `mod/42/media/lua/shared/Translate/<L>/UI.json` x 7 | geaendert (+24 je Sprache) | EN 9431 | EN a17ac79a7c02b33f78193dd4ef60025c | 15 Big-Fassungen, 9 Markierungs-Groesse |
| `mod/42/media/lua/shared/Translate/<L>/IG_UI.json` x 7 | geaendert (+1 je Sprache) | EN 327 | EN 202587fe30b8510f5bd1a8ea4f4531fb | `IGUI_AnimalType_ncbeargrown` |
| `mod/42/media/ui/BanditsNPCBearMarker_*.png` (8), `BanditsNPCBearCub_marker288.png` | **neu (9)** | siehe "Bilder" | | Scheibe, Ring, 6 Pfeile, Symbol 288 |
| `ober_werkzeug/texte_b1e.py` | **neu** | | | Text-Generator auf `texte_b1d.py` (+24 UI, +1 IG_UI), `--basis` |
| `ober_werkzeug/marker_bilder.py` | **neu** | | | zeichnet die 9 Bilder (PIL + numpy, 8-fach), Selbstprobe 96er == 9e45e936 |
| `attrappe/b1e_ober/run.lua` | **neu** | | | Attrappe 7.2 (218 Pruefungen, beide Modi) |
| `attrappe/b1e_ober/texte_pruefen_b1e.py` | **neu** | | | Texte, IG_UI, CN, Optionen-Argumente, Form, kein Art-Vergleich, Werkzeug-Gegenprobe (`--tmp`) |
| `attrappe/b1e_ober/bilder_pruefen_b1e.py` | **neu** | | | 9 Bilder: Masse, RGBA, Rand, Formen, Symbol, Pfade, Werkzeug-Gegenprobe (`--tmp`) |
| `attrappe/b1e_ober/belege_b1e.py` | **neu** | | | 53 neue Fundstellen gegen die Dateien |
| `attrappe/ober/run.lua`, `b1b_ober/run.lua`, `b1c_ober/run.lua`, `b1d_ober/run.lua`, die vier `texte_pruefen*.py`, `gesamt/run.lua` | gewollt geaendert ("B1e") | | | schnittstelle_aenderungen.md "B1e OBERFLAECHE" Punkt 9 |
| `schnittstelle_aenderungen.md` | angehaengt | | | Abschnitt "B1e OBERFLAECHE" |

Unveraendert (byte-gleich, geprueft): `client/ISUI/BanditsNPCBearMap.lua`, `ui/BanditsNPCBearCub_marker.png` (9e45e936), `Sandbox.json` x 7,
`sandbox-options.txt` (5b182174). `staging_dateien.txt` nicht angefasst (ZUSAMMENBAU). Neue Lua-Dateien: keine.

## Was wie gebaut ist (Plan-Bezug)
- **Helfer (0.8, 3.2):** Menue `onClickedAnimals` (Riegel `not B.BodyKind` -> still), Hud `scan`, Bench `NCBear_CubClean` und
  `nearestCubObject` fragen nur `B.BodyKind(o) ~= nil`. `B.ViewOf` (KERN) traegt den Rest (Menue-Sicht, `U.CubObj`, Karte).
- **Texte je Koerper (0.10, 6.4, 6.5):** `U.TB(key, bd, a1, a2, a3)` -> Big nur bei `bd == "big"` UND vorhandenem `U.EN[key .. "Big"]`.
  `U.NoteText`: dieselbe Regel auf `note.k` vor dem Einsetzen (Meldungen ohne Big-Fassung, z. B. `Note_Grown`, bleiben). `U.CubName` ->
  `U.TB("UI_BN_Bear_Tag_Name", c.bd, who)`. Menue: Name, Call-Tooltip, Call-Wartezeit; Namensfenster: Titel.
- **Hud (1.2.4, 1.2.5):** `e.zk = sz / tagBase`, beim grossen Koerper x `tagBigK` (1,06, Rueckfall 1,06), Deckel 5. Probe nur
  `isClient()` und `B.BodyKind(obj) == (c.bd or "cub")`.
- **Markierung (1.7, 6.6):** `local Mk = ISUIElement:derive("BanditsNPCBearMarkerUI")`, `Mk:new` ueber `ISUIElement.new(self, ...)`; genau EIN
  Element je Spielstart (altes abgemeldet), unsichtbar ohne Ziel. Takt 400 ms (`markerMs`): Ziel wie B1c (`target()` unveraendert: neu, bis
  60 s nach dem ersten "shy", nie angefuettert/gezaehmt, Doppelklick-Sperre je Junges), Winkel `(deg(atan2(dy, dx)) + 135 + 360) % 360`
  (Bandits' Ausrichtung, `markerAngleAdd`), nah (<= 6,6 Kacheln) -> Ring statt Pfeil. Lage: Klickflaeche 45 f an (Breite/2 - 48 f, 48 f)
  bzw. Bandits' gemerkte Stelle, Kreis ganz auf dem Bild, Ausweichen um 100 f vor einem sichtbaren Bandits-/NPC-Crew-Marker naeher als
  48 + 48 f. Groesse neu bei Einblenden, Aufloesungswechsel und geaendertem Optionswert. Je Bild 3 Bilder + 1 Text aus fertigen Feldern.
- **Optionen (6.7):** `addComboBox("MarkerSize", ...)` + 7 `addItem` (Auto Vorgabe); Seite: TagShow, TagHealth, TagStamina, TagAge, TagSize,
  MarkerSize. Gelesen ueber `U.Opt("MarkerSize", 1)` (1 s Zwischenspeicher).
- **Bench (1.6):** siehe Kurzfassung; `NCBear_CubGrow` merkt den Koerper vor `B.GrowSetG` + `B.BrainTick(true)` und vergleicht danach.

## Engine-Aufrufe mit Fundstelle (neu in B1e; jede Zeile per `attrappe/b1e_ober/belege_b1e.py` gegen die Dateien geprueft: 53/53 OK)

| Datei | Aufruf | Fundstelle (gleiche Argumenttypen) | Seite |
|---|---|---|---|
| Marker | `require "ISUI/ISUIElement"`, `ISUIElement:derive(Text)` | `V:client/Chat/ISAlert.lua:1`, `:3` | Client |
| Marker | `ISUIElement.new(self, x, y, w, h)` | `V:client/ISUI/ISUISprite.lua:71`, `V:client/ISUI/Maps/ISMiniMap.lua:345` | Client |
| Marker | `el:initialise()`, `el:addToUIManager()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:746-747` | Client |
| Marker | `el:removeFromUIManager()` | `V:client/ISUI/ISUIElement.lua:1373`, Aufrufer `V:client/ISUI/Maps/ISMap.lua:116` | Client |
| Marker | `el:setVisible(false/true)` | `V:client/ISUI/ISCollapsableWindow.lua:70` / `V:client/Chat/ISAlert.lua:55` | Client |
| Marker | `el:setX/setY/setWidth/setHeight(Zahl)` | `V:client/ISUI/ISToolTip.lua:78-79`, `:173-174` | Client |
| Marker | `self:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | `V:client/Chat/ISChat.lua:418`, `V:client/DebugUIs/ISSpawnVehicleUI.lua:171` | Client |
| Marker | `self:DrawTextureAngle(tex, cx, cy, Grad)` | `V:client/Fishing/TensionUI.lua:21`, `V:client/ISUI/Fireplace/ISKnob.lua:24` (zeichnet in Bildgroesse -- NUR JAR, FE 8 -> Bild je Stufe) | Client |
| Marker | `self:drawTextCentre(text, x, y, r, g, b, a, UIFont.Small/Medium/Large)` | `B:client/BanditEventMarkers.lua:176` / `V:client/DebugUIs/StashDebug.lua:86` / `V:client/Chat/ISAlert.lua:35` | Client |
| Marker | `function Mk:onMouseDoubleClick(x, y)` (Rueckruf) | `V:client/ISUI/ISButton.lua:66`, `B:client/BanditEventMarkers.lua:19` | Client |
| Marker | `getTexture("media/ui/<datei>.png")` | `V:client/Chat/ISChat.lua:921` | Client |
| Marker | `getCore():getScreenWidth()`, `getCore():getScreenHeight()` | `V:client/Challenge/WinterIsComing.lua:18` | Client |
| Marker | `Events.OnResolutionChange.Add(f(oldw, oldh, neww, newh))` | `V:client/ISUI/PlayerData/ISPlayerData.lua:185`, `:206` | Client |
| Marker | `Events.OnTick.Add`, `Events.OnGameStart.Add`, `getTimestampMs()` | `V:client/Chat/ISChat.lua:943`, `:1186`; `V:client/Foraging/ISBaseIcon.lua:485` | Client |
| Marker | `getSpecificPlayer(0)`, `p:isDead()`, `p:getX()/getY()` | `V:client/Farming/CFarmingSystem.lua:45`; `V:client/Context/ISMenuContextWorld.lua:37`; `V:client/Fishing/TensionUI.lua:11` | Client |
| Marker | `p:getModData()["BanditEventMarkerPlacement"]` (nur lesen) | `V:client/Entity/ISUI/BuildRecipe/ISBuildRecipePanel.lua:48`; Feld `B:client/BanditEventMarkerHandler.lua:17`, geschrieben `B:client/BanditEventMarkers.lua:88` | Client |
| Marker | Bandits-Marker lesen: `.x/.y`, `m:getDuration()`, `m:getIsVisible()` | `B:client/BanditEventMarkers.lua:235-236`, `:142`; `V:client/ISUI/ISUIElement.lua:676` | Client |
| Marker | `math.atan2`, `math.deg` | `V:client/ISUI/Fireplace/ISKnob.lua:137`; `V:client/Foraging/ISBaseIcon.lua:212` | - |
| Options | `addComboBox` / `addItem` (Prozent-Texte `"100%%"`) | wie B1d (`V:client/PZAPI/ModOptions.lua:121`, `:131-137`); `%%` wie Vanilla `V:shared/Translate/EN/UI.json:117`, gelesen `V:client/OptionScreens/MainOptions.lua:1244` | Client |
| Bench | `a:getAnimalType()` (nur gedruckt) | `V:client/ISUI/Animal/ISAnimalUI.lua:65` | SP |
| Bench | `getTimestampMs()` | `V:server/Foraging/forageServer.lua:456` | SP |
| Menue, Hud, Bench | `B.BodyKind(a)` (KERN; darin `getAnimalType`) | KERN `shared/BanditsNPCBear.lua:497` | beide |

**Nicht benutzt:** `BanditEventMarkerHandler.set` (B1e ruft Bandits nicht mehr), `drawTextureAllPoint`, `drawTextZoomed`, `pcall`, `getData`/
`setSizeForced`/`setHealth`/`getHealth` ausserhalb der Bench. Keine Jar-only-Aufrufe. Kevins zwei Ausnahmen sind nicht betroffen.

## Text-Schluessel je Sprache (gezaehlt von `attrappe/b1e_ober/texte_pruefen_b1e.py`)

| Sprache | UI neu | IG_UI neu | UI gesamt | Sandbox gesamt | IG_UI gesamt | Tiername `ncbeargrown` |
|---|---|---|---|---|---|---|
| EN | 24 | 1 | 157 | 60 | 7 | Bear |
| PTBR | 24 | 1 | 157 | 60 | 4 | Urso |
| RU | 24 | 1 | 157 | 60 | 4 | Медведь |
| KO | 24 | 1 | 157 | 60 | 4 | 곰 |
| ES | 24 | 1 | 157 | 60 | 4 | Oso |
| CN | 24 | 1 | 157 | 60 | 4 | 熊 |
| FR | 24 | 1 | 157 | 60 | 4 | Ours |

Platzhalter je Schluessel gleich EN UND gleich dem Grundschluessel; jede Big-Fassung unterscheidet sich vom Grundtext (sagt "Baer"); kein
`<`/`>`, kein Testwort, kein einzelnes `%`; Prozent-Stufen "100%%" ... "300%%" wie Vanilla in allen 7 Sprachen; sortiert, UTF-8 ohne BOM, LF,
Round-Trip; `U.EN` == EN/UI.json (157); EN wortgleich mit Plan 6.8; CN: 404 verschiedene Zeichen, alle in Vanilla-CN; "Auto" je Sprache wie
Vanilla (`UI_modselector_auto` / `GameSound_Category_AUTO`: Automático, Авто, 자동, 自动, Auto). `texte_b1e.py` schreibt byte-gleich das
Staging, `--basis` byte-gleich `texte_b1d.py`; Sandbox.json x 7 + sandbox-options.txt unveraendert.

## Bilder (`ober_werkzeug/marker_bilder.py`, geprueft von `attrappe/b1e_ober/bilder_pruefen_b1e.py`)

| Datei (`mod/42/media/ui/`) | Masse | Bytes | MD5 | Befund |
|---|---|---|---|---|
| `BanditsNPCBearMarker_disc.png` | 288 x 288 | 2898 | 3c36b62865485c225702ca79fd40367d | weiss, Radius 22,51/96, Rand frei |
| `BanditsNPCBearMarker_ring.png` | 288 x 288 | 4356 | 6e5184104c421e5217746cd493131e3f | weiss, Ring 20,50..23,51/96, Rand frei |
| `BanditsNPCBearMarker_arrow096.png` | 96 x 96 | 1099 | 80e72a24216a3aba2d05a25b320ed42d | Ring + Spitze oben bis ~30/96, Schwerpunkt -1,6 px |
| `BanditsNPCBearMarker_arrow120.png` | 120 x 120 | 1496 | f9d27e425b70f94791b45aa91b5babea | dto. |
| `BanditsNPCBearMarker_arrow144.png` | 144 x 144 | 1999 | 5a26431fc6c7618e4ff3360dce17e35c | dto. |
| `BanditsNPCBearMarker_arrow192.png` | 192 x 192 | 2805 | 197b6ba74c82b81a056af3cb6d8eb9cc | dto. (Kevins 4K: 200 %) |
| `BanditsNPCBearMarker_arrow240.png` | 240 x 240 | 3578 | 3ebf798e4425757652957a99dc9fbf1a | dto. |
| `BanditsNPCBearMarker_arrow288.png` | 288 x 288 | 4485 | 95663bc0065332c279758faaaaa270d0 | dto. |
| `BanditsNPCBearCub_marker288.png` | 288 x 288 | 19849 | cf0a1f980d540fd3e34b88467819dff0 | Kevins Symbol W1, ganzer 96er-Ausschnitt 3-fach (24-fach ueberabgetastet); 3:1 verkleinert Alpha-Mittel 0,001 gegen das 96er |

Alle RGBA, Rand frei, <= 288 px (Uebernahme-Deckel 512, Namensraum `UI_ASSET` ok). **Selbstprobe:** der Weg des Zeichen-Skripts
`baer/spiel/icon_zeichne_v2.py` (nur importiert, nichts dort geschrieben) gibt bei 8-facher Ueberabtastung das 96er byte-gleich 9e45e936
-> kein Rueckfall noetig. Proportionen an Bandits' `eventMarker*.png` NACHGEMESSEN (Scheibe 45 px, Ring ~21..24, Spitze bis Zeile 17), nicht
kopiert. Eine Vorschau (eigene Bilder 100/150/200/300 % neben dem heutigen Bandits-Bild) lag nur im Sitzungs-Ordner; bei 100 % sieht die neue
Markierung aus wie die alte.

## Pruefer-Ausgaben (alle im Staging, 11.11.2026)
- `luacheck.py` (7 Client-Dateien): 0 failed. `scopecheck.py`: 0 violation(s). `localcount.py`: groesster Wert 49 aktiv / 60 insgesamt
  (Hud, Dateiebene; Markierung 19) -- weit unter 180.
- `luacheck_pz.py`: 18 x W113, alle alt (15 Bench-Globale `NCBear_Cub*`/`NCBearMenu`, 3 Zeitaktions-Klassen im Menue, geladen aus shared/).
  `--unused`: nur `self` der drei Hud-Mausfunktionen (alt), `self` in `Mk:onMouseDoubleClick` (Rueckruf-Form), `player` der Bench-Huelle (alt).
- Form: alle geaenderten/neuen Lua-Dateien LF, ASCII, kein BOM, keine Leerzeichen am Zeilenende, kein `next(`, kein `%a`.
- Attrappen: `ober` 116 / 117, `b1b_ober` 144 / 134, `b1c_ober` 155 / 142 (Markierungs-Abschnitt ersetzt, s. u.), `b1d_ober` 174 / 176,
  **`b1e_ober` 218 / 218** (Kern-Attrappe / echter Kern shared) -- je 0 Fehler; `gesamt` 1172 bestanden, 0 Fehler (die zwei "Fehlerzeilen des
  Codes" sind die erwarteten Heilungs-Zeilen 18c/19f wie bisher).
- Text-Pruefer `ober/texte_pruefen.py`, `b1b_ober/...b1b.py`, `b1c_ober/...b1c.py`, `b1d_ober/...b1d.py`, `b1e_ober/texte_pruefen_b1e.py --tmp`:
  je FEHLER gesamt 0. `bilder_pruefen_b1e.py --tmp`: FEHLER 0 (Werkzeug byte-gleich). Belege: `belege_b1e.py` 0 von 53 abweichend; alte
  `belege.py` 0/112, `b1b` 0/51, `b1c` 0/89, `b1d` 0/23.
- Uebernahme-Trockenlauf `python -I baer/tools/baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a` (schreibt nichts): NICHT OK,
  4 Fehler, alle erwartet bis der ZUSAMMENBAU das Skript nachzieht (PLAN_B1E.md 10.3): 1 OBERFLAECHE (`IGUI_AnimalType_ncbeargrown` noch
  nicht in `TEXT_NS`), 3 KERN-Defs (`bodyModel NCBear_Body`, Textur `NCBear`, "Testbefehl" `NCBear_Body`). Zur OBERFLAECHE sonst: Cheat-Funde
  in Client-Dateien 0, Ersatztexte 157 wortgleich, die 9 Bilder als Uebernahme-Dateien erkannt.

## Was die Attrappe b1e_ober beweist (Logik, nicht Engine)
Texte: `U.TB` Big nur mit bd big UND vorhandenem Schluessel; 8 Meldungen mit bd big ("Your bear follows you.", Richtung, Name, Minuten);
`Note_Grown` ohne Big-Fassung bleibt; unbekannter Schluessel bleibt; 15 Big-Fassungen je mit Grundschluessel. Optionen: Reihenfolge ...
TagSize, MarkerSize; 7 Eintraege als Schluessel, Vorgabe Auto; beim Laden 13 x getText nur mit Schluesseln. Faktor: 1080/1440/2054/2160/
3240/720/9999/Gleichstand 1890 -> 1,0/1,25/2,0/2,0/3,0/1,0/3,0/2,0; Index 2/5/7 fest, Index 9 -> Auto. Menue: grosser Koerper bekommt Feed,
Pet, Follow me, "Name the bear", Call mit "bear"-Tooltip und -Wartezeit, Kill weg; Junges wie bisher; "bear" -> Vanillas Menue unveraendert;
Namensfenster "Name for your bear:" / "...cub:"; MP-Call per sendClientCommand. Hud: Suchlauf bindet gross und Junges, nie "bear"; "Kevin's
bear"/"Kevin's cub"; Anker x 4,09 (gross, 1,35), x 2,18 bei 0,72 (gross), x 2,14 (Junges 0,75); Probe SP nie, MP nur an passender Art (4
Faelle). Markierung bei 3840 x 2054 Auto: sichtbar ohne Bandits, Element 1824/96, 90 px; Scheibe 192 um (45, 45) in 1,0/0,52/0,09; Text
Large +50; Pfeil 192er-Bild; Symbol 288er auf 192; Winkel Ost 135 / Nord 45 / Sued 225 / West 315; 20 Kacheln Pfeil, 5 Kacheln Ring;
2000 Bilder ohne neue Tabelle, ohne getText/U.T/getCore/U.Opt; Takt 400 ms; shy 59 s an / 60 s aus; angefuettert, gezaehmt, Eintrag weg,
Spieler tot, kein Spieler -> aus; Doppelklick -> aus fuer dieses Junge, neues Junges -> an; Bandits-Stelle (100, 50) -> (100, 51); sichtbarer
Bandits-Marker an der Standardstelle -> +200 px, nur beim Einblenden; unsichtbarer / Dauer 0 / kaputter Marker -> kein Versatz, kein Fehler;
Option 100 % (45 px, Pfeil 96, Small), 150 % (67,5 px, Pfeil 144, Medium), zurueck Auto; Aufloesung 1440 -> 56,25 px; 5 Spielstarts -> genau
ein Element; Bild fehlt -> Fehlerzeile, kein Pfeil, Rest sichtbar. Bench: MP "singleplayer only"; Grow(15) "body big (swapped)"; Stats
body/want/engine type/swap ready/last swap/fails, "swap waits (calm)"; Grow(-100) bei calm "body big, swap waits: calm", danach "body cub
(swapped)"; ohne Sitzung "no session yet"; Kern ohne B1e klare Zeile; Clean 2 Tiere, nie "bear"; CubSet-Hilfe B1e. Dateien: kein
`getAnimalType() ==/~=`, kein `== B.CUB`, kein pcall/NCBear_ ausser Bench, kein `BanditEventMarkerHandler.set`, kein
drawTextureAllPoint/drawTextZoomed, ASCII/LF.

## Fuer den ZUSAMMENBAU
- `staging_dateien.txt`: 6 Client-Dateien + Bench (MD5 oben), 7 UI.json, 7 IG_UI.json geaendert; 9 Bilder neu; Bench weiter "nur Testhilfe".
- `baer/tools/baer_uebernahme.py`: `TEXT_NS["IG_UI.json"]` += `IGUI_AnimalType_ncbeargrown` (sonst 1 Fehler); die Bilder laufen ueber `UI_ASSET`.
- `attrappe/gesamt/run.lua`: von mir nur so weit angepasst, dass es gruen bleibt (Markierung 18a/18n, Mock) -- "20 B1e" und `xref_b1e.py`
  bleiben beim ZUSAMMENBAU (Markierung mit/ohne Bandits: `MK.el()`, `MK.ang()`, `MK.near()` stehen bereit). `xref_b1d.py` meldet die
  B1e-Aenderungen als Luecken (prueft den B1d-Plan); `xref_b1b.py`/`xref_b1c.py` brechen an `server/BanditsNPCBearRegistry.lua` `viewEntry`
  ab (KERN-Datei).
- `NAEHTE.md` (Plan 10.4): Markierung ruft Bandits nicht mehr, liest nur `BanditEventMarkerHandler.markers` und
  `BanditEventMarkerPlacement` (beides hinter Riegeln), laeuft ohne Bandits.
- Nach dem Einbau: Spiel NEU starten (neue Lua, neue Bilder, neue Tierart).

## Offen / ungeprueft (Testpunkte)
- Alles ungespielt. Pfeil-Ausrichtung des eigenen Bildes mit Bandits' Konvention (`markerAngleAdd` per `NCBear_CubSet` stellbar);
  Lesbarkeit Small/Medium/Large bei Kevins Schrift; ob der Doppelklick ohne eigenes `onMouseDown` ankommt (Bandits' Element hat eins) und
  ob das 45 f-Element Klicks darunter schluckt (Bandits' Element tut es genauso); Aufloesungswechsel im laufenden Spiel.
- Bilder ueber 256 px (288er Scheibe/Ring/Symbol/Pfeil-300 %): ob die Vanilla-Option "Max. Texturgroesse" auch UI-Bilder deckelt, ist
  ungeprueft (bekannt nur fuer Kleidungs-Texturen). Scheibe/Ring/Symbol werden mit fester Groesse gezeichnet (nur unschaerfer); der
  300-%-Pfeil (`DrawTextureAngle` zeichnet in Bildgroesse) koennte dann kleiner ausfallen.
- 1440p bekommt in Auto 125 % (Stufe), nicht 133 % (Auftrag "~1,33"): stufenlos ginge nur mit `drawTextureAllPoint` (F8).
- Namensschild-Faktor 1,06 am grossen Koerper, Vorgabe-Name/Meldungen "bear" ab Halbstark (F3) -- im Spiel ansehen.
- MP: Sicht `bd` und Groessen-Probe im Tauschfenster (ein Bild lang zwei Kopien) -- statisch, nicht gespielt.

## Fragen fuer Kevin (er testet gerade -- gebaut ist jeweils die Empfehlung)
| # | Frage | Gebaut |
|---|---|---|
| F7 | Markierung ziehbar (Stelle merken) wie bei Bandits? Heute blendet nur ein Doppelklick sie aus. | nein (erst auf Wunsch) |
| F8 | Groesse in Stufen Auto + 100/125/150/200/250/300 % ok? Stufenlos nur mit deinem Wort fuer `drawTextureAllPoint` (kein Vanilla-Aufrufer). | Stufen |
| F11 | Die Markierung kommt jetzt auch OHNE Bandits ("brauch ich dafuer eine zusatz mod?" -- nein). Ok? | ja |
| F3 | Ab Halbstark sagen Schild und Meldungen "bear" statt "cub" ("Kevin's bear", "Your bear follows you.")? | ja |
| neu | Bei 4K (2054 hoch) ist die Markierung jetzt doppelt so gross (Kreis 192 px, grosse Schrift). Reicht das, oder lieber 250 % fest? | Auto = 200 % |

Statisch geprueft, nicht gespielt.
