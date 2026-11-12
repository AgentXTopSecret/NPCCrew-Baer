# Lauf baer-f1: GEGENPRUEFUNG nach der Nachbesserung (Befunde A1-A8, B1-B10)

Stand 12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Geprueft wurde der HEUTIGE Stand im Staging
`_arbeit/baer_zaehmen/mod/` (67 Dateien) und `baer/tools/baer_uebernahme.py`; keinem Bericht geglaubt, alles selbst gelaufen. Geschrieben nur
diese Datei, `anleitung_f1_entwurf.md` und Wegwerf-Skripte im Scratchpad (`.../scratchpad/gp/`: `zaehlen.py`, `json_diff.py`, `jar_such.py`,
`stich_unstuck.lua`, `stich_c1_laden.lua`, eine eigene Probe unter `gp/probe`, danach geloescht; Ausgabe `gp/probe_ausgabe.txt`). Nichts in der Test-Mod, NPC Crew, Vanilla, Bandits; kein git.

## 0. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test.** Kein Blocker. 13 Befunde geschlossen, 5 bewusst offen (A4, A5, A8, B7, B8: Kevin-Fragen
bzw. vertretbar, keiner zu Unrecht abgelehnt). Die Nachbesserung hat nichts kaputt gemacht, das ich finden konnte: alle alten Attrappen
(B1a-B1e) laufen unveraendert gruen, Trockenlauf/Probe genau wie gespeichert. Sechs neue kleine Restbefunde (N1-N6, keiner rot).

## 1. Je Befund am heutigen Code

| ID | heute | Beleg (S: = Staging `42/media/lua/`, V: = Vanilla `media/lua/`) |
|---|---|---|
| A1 minor | **geschlossen** | Regel `taste` sieht jetzt `setWantKeyEvents(`, `:isKey(`, `isKeyConsumed`, `onKeyPress/Release/Repeat`, `table.insert(keyBinding`, `key == <Zahl>` (`baer/tools/baer_uebernahme.py:228-233`); 14 einzeln begruendete Tasten-Ausnahmen (+2 Befehls-Ausnahmen der Defs), alle greifen (Probe-Ausgabe "Cheat-Pruefung ... Funde: 0"). `probe_regeln_f1.py` selbst gelaufen: 15 von 15. |
| A2 minor | **geschlossen** | `S:client/BanditsNPCBearKey.lua:63-70` `bearKind`: Sicht kennt das Tier, Besitzer gesetzt und nicht ich (`U.WinMine`, `S:client/BanditsNPCBearWinData.lua:198-202`) -> "foreign" -> Vanillas Radial bleibt (`Key.lua:118`). Die Sicht traegt `owner` auch fuer fremde Baeren in `tellDist` (`S:server/BanditsNPCBearRegistry.lua:601`, `:643-650`). Junges im Zaehmen (owner nil) -> Hinweis "no bear yet" (gewollt). |
| A3 minor | **geschlossen** | `S:server/BanditsNPCBearServer.lua:48-55` `tellWhy(..., bd)`; `handCheck` gibt `B.BodyKind(animal)` mit (`:164`, `:175`); Absagen aus CheckFeed/CheckPet mit `rec.body` (`:227`, `:278`). Client waehlt Big nur, wenn es den Schluessel gibt (`S:client/BanditsNPCBearClient.lua:338`, `:385`). Uebrige `Why_Gone` ohne bd nur dort, wo es keinen Eintrag gibt. |
| A4 minor | **offen (Kevin-Frage), begruendet** | Frei-Radius 12 statt 8 (`S:shared/BanditsNPCBear.lua` / `sandbox-options.txt` `BearRoamRadius` default 12); "8" steht nur im Auftragstext, nicht in Kevins ENTSCHEIDUNGEN. "Komm her" ohne Abklingzeit, Unstuck = Call to me mit 5 min: passt zu ENTSCHEIDUNGEN.md:68 und :280 ("Unstuck vorerst als ... Call to me, Abklingzeit 5 min; spaeter ins V-Fenster"). |
| A5 minor | **offen (nicht F1), Kevin-Frage** | `U.WinBears` nimmt nur tame/missing (`WinData.lua:187`). Kein Fehler: im Auftrag steht "Zaehmung/Vertrauen (falls Daten da)"; "Trust" steht ehrlich unter "Coming later". |
| A6 minor | **geschlossen** | Kommentare `S:server/BanditsNPCBearOrder.lua:16`, `:172`, `:398` nennen jetzt `V:server/Map/SGlobalObjectSystem.lua:89` -- nachgelesen: `square:getX(), square:getY(), square:getZ()` in einer Server-Datei (`if isClient() then return end`, Zeile 1). |
| A7 minor | **geschlossen** | Selbst neu gelaufen, Ausgaben **gleich** `trockenlauf_f1_nach.txt` / `trockenlauf_f1_nach_vor_b5a.txt` / `probe_f1_nach_ausgabe.txt` (nur Pfade anders). |
| A8 minor | **offen, vertretbar** | 4 Bilder 288 px (Probe-Liste). `forschung_f1.md` 6.2: Deckel nur bei Textur-Flag 128/256 (NUR JAR), `getTexture` laedt UI-Bilder ohne; Vanilla zeigt selbst UI-Bilder > 256 px (`V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191`). Im Test einmal ansehen. |
| B1 major | **geschlossen** | `S:server/BanditsNPCBearOrder.lua:354-421`: neuer Koerper erst bei `revN >= 2` UND `ms - revAt >= reviveMs` (60 s) UND nicht im Heil-Fenster (`:394`); Frist neu bei "passt nicht" (`:383-384`), Luecke > 50 s / Uhr rueckwaerts (`:388-391`), Gegend entladen (`S:server/BanditsNPCBearServer.lua:843-846`). Deckel ein Koerper je Takt (`made`). Eigene Stichprobe S2 unten. |
| B2 major | **geschlossen (reine Daten)** | `trailerBaseSize = 100000` (`S:shared/BanditsNPCBearDefs.lua:104`, `:190`). Selbst nachgesehen: Java liest das Feld (`dec/AnimalDefinitions.java:627-628`), Platz = trailerBaseSize x Groesse (`dec/IsoAnimal.java:2794-2795`), `canAddAnimalInTrailer` vergleicht mit der Kapazitaet (`attrappe/pruef_f1/jar/BaseVehicle.txt:37653-37667`); Vanilla graut "zu gross" aus, auch fuer das Tier in der Hand (`V:client/Vehicles/ISUI/ISVehicleMenu.lua:758-800`). Eigene Jar-Suche (alle Klassen): `IsoAnimal.getAnimalTrailerSize` nur in BaseVehicle und AnimalCommandPacket; `Food.class` ruft nur `BaseVehicle.getAnimalTrailerSize` (Eier-Bruten, javap). Aufheben ist ohnehin aus (`canBePicked = false`, Defs.lua:109). |
| B3 major | **geschlossen** | `S:client/BanditsNPCBearPose.lua:82-143`: bei busy/eigener Fuetter-Aktion Eintrag behalten, nichts schreiben (`:91-94`); nach dem Streicheln weiter "sit" ohne Hinsetz-Clip (`:114-121`); nach geloeschtem B.ACT neu "sitdown" bzw. fertig (`:103-112`); in "sit" je 2 s nachsetzen (`:130-132`). Naht `U.PoseHands` aus `S:shared/TimedActions/BanditsNPCBearFeedAction.lua:65`, `:77` hinter `B.UI and B.UI.PoseHands` (Server laedt keine Client-Datei). Aufrufe nur `setVariable`/`clearVariable` (`V:shared/TimedActions/Animals/ISPetAnimal.lua:43`, `:48`). Ob gleicher Wert den Clip nicht neu startet: ungeprueft (Laufzeit). |
| B4 minor | **geschlossen** | `S:server/BanditsNPCBearFollow.lua:127` `s.ownCut = s.ownUntil` fuer stay/sit/roam; `ownLive` (`Order.lua:51-54`); `B.HandleMode` setzt die Heimat auf die Kachel von jetzt und haelt sofort an (`Follow.lua:301-305`, `B.Hold` = setBlockMovement, `S:server/BanditsNPCBearWorld.lua:866-881`); `B.MoveTo` loest die Sperre wieder (`World.lua:927`). Der Vorschlag "ownUntil = nil" wurde begruendet NICHT genommen (Laerm-Wache) -- richtig so. |
| B5 minor | **geschlossen** | EN: `Win_HintMissing` "No body now. It can come back while you are near, or use Unstuck." (UI.json:206), `Note_PassiveOn(Big)` "... once bears can fight (comes later)." (:112-113), 7 Sprachen. Wortlaut-Hinweis N6. |
| B6 minor | **geschlossen** | `S:client/BanditsNPCBearWinData.lua:434-443`: Knopf "Unstuck m:ss" und Tooltip `Win_CallWaitClock` mit derselben Uhr; Bild `f1_entwurf/fenster_gebaut_4k.png` zeigt "Unstuck 3:12" / "... again in 3:12." |
| B7 minor | **offen (gewollt), Testliste + Frage** | `Key.lua:112` Vorfahrt Fahrzeug-Radial; `Window.lua:546-549` offenes Fenster verbraucht V. Kein Fehler, Bedienfrage. |
| B8 minor | **offen, vertretbar** | Zeichenaufrufe nur bei offenem Fenster (`Window.lua:512-530`, Modell 1 x je s); keine Kosten bei geschlossenem Fenster. |
| B9 minor | **geschlossen** | `S:client/BanditsNPCBearKey.lua:81-90`, angemeldet `:141-142` (OnKeyStartPressed / OnKeyKeepPressed) und im Loslassen `:131`: schliesst Vanillas Radial nur an UNSEREM Baeren, nie am Auto. Nachgelesen: Vanilla oeffnet das Radial beim Druecken (`V:client/ISUI/ISUIHandler.lua:35-57`, angemeldet erst in OnGameStart `:101-104`); "Kill" fuer jedes nicht wilde Tier mit Waffe (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:1170-1176`); `undisplay` wie Vanilla `:1164`. Hoechstens ein Bild sichtbar (ungeprueft, Laufzeit). |
| B10 minor | **geschlossen** | `U.WinTyping()` (`S:client/ISUI/BanditsNPCBearWindow.lua:672-675`), `openKey` bricht ab (`Key.lua:97`). |

Zu Unrecht abgelehnt: **keiner**. Durch die Nachbesserung kaputt: **nichts gefunden** (alle B1a-B1e-Attrappen unveraendert gruen, Abschnitt 2).

## 2. Selbst gelaufen (Zahlen)

| Pruefung | Ergebnis |
|---|---|
| luacheck.py (32 Lua) | 32 checked, **0 failed** |
| scopecheck.py | **0 violations** |
| localcount.py | hoechstens **51 aktiv** (`client/ISUI/BanditsNPCBearHud.lua` Dateiebene), **77 insgesamt** (`server/BanditsNPCBearWorld.lua:699`) -- weit unter 180 |
| luacheck_pz.py | **20 x W113**, alle bekannt: 17 in `NCBearBenchCub.lua` (Testhilfe, Zeilen 1067-1084), 3 Aktionsklassen `client/BanditsNPCBearMenu.lua:93/:104/:114` (Globale aus den kopierten TimedActions; in der Probe "3 erlaubt") |
| Form | 32 Lua + 21 JSON + 2 txt: kein CR, kein BOM, LF am Ende, Lua reines ASCII; 21 JSON Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` gleich und sortiert |
| Kern-Attrappen | kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1e_kern 153/0 (je byte-gleich `ergebnis_f1.txt`), b1d_kern 162/0 (nur Pfad-Vorsatz anders, bekannt), f1_kern **189/0** (byte-gleich) |
| Oberflaechen-Attrappen (Kern-Attrappe / echter Kern) | ober 116/117, b1b_ober 144/134, b1c_ober 155/142, b1d_ober 174/176, b1e_ober 231/231, **f1_ober 359/359** -- je 0 Fehler |
| Gesamt-Attrappe | **2329 / 0**, byte-gleich `gesamt/ergebnis.txt` ("C1 wieder da 39 Hirn-Takte (62,4 s)") |
| Nachbesserungs-Attrappen | `nach_f1/kern.lua` **28/0**, `nach_f1/ober.lua` **33/0**, `nach_b1e` 31/0 -- je byte-gleich gespeichert |
| Pruefer-Attrappen | `pruef_f1/c1_wartefrist` 0 Befunde, `sitz_treiber` 0 Befunde, `kopf_lage` 1 Grenzfall (1080 + Vanilla-Schrift 4x, Umbenennen beruehrt die Koerper-Zeile; bei Kevins 4K: keine Ueberlappung) -- je inhaltsgleich `*_ergebnis_nach.txt`; pruef_b / b1c / b1d / b1e(run_nach 25/0, run 20/5 bekannt seit B1e) wie gespeichert; `pruef_b1b/run.lua` ohne Kahlua-Zeichen weicht ab (bekannt, `run_nach` mit Kahlua-Zeichen = `ergebnis_f1.txt`), `spur_1a` zeigt den behobenen B1b-Fall (folgt bei ~4 Kacheln statt 26) |
| Text-/Beleg-Pruefer | texte_pruefen / _b1b / _b1c 0, _b1d / _b1e **ohne** `--tmp` 0 (mit `--tmp` je 1: das ALTE Werkzeug kennt die F1-Texte nicht -- erwartet, massgeblich ist das F1-Werkzeug); `texte_pruefen_f1.py --tmp` **0** (22 Dateien Werkzeug == Staging); belege 0/112, _b1b 0/51, _b1c 0/89, _b1d 0/23, _b1e 0/53, `belege_f1.py` 0 (97 V:-Fundstellen vorhanden); `bilder_pruefen_b1e.py --tmp` 0 |
| xref_f1 / Gegenproben | `xref_f1.py` **0 Luecken, 3 Hinweise** (byte-gleich `xref_f1.txt`); `gegenprobe_f1.py` **27 von 27**; `probe_regeln_f1.py` **15 von 15**; `probe_regeln_b1e.py` 8 von 8 |
| Trockenlauf `--staging mod --vor-b5a` | **OK -- 0 Fehler, 31 Warnungen** (27 Altlasten, 2 ALT_DEFS, Clip-Warnung NCBearCub.glb, NC-Kommentar `BanditsNPC.lua:1363`); gleich `trockenlauf_f1_nach_vor_b5a.txt` |
| Trockenlauf ohne `--vor-b5a` | **NICHT OK -- 29 Fehler** = genau 27 Altlasten + 2 ALT_DEFS (so gewollt bis B5a); gleich `trockenlauf_f1_nach.txt` |
| Probe `--probe <scratchpad>/gp/probe --staging mod --vor-b5a` | **OK -- 0 Fehler, 31 Warnungen**, 70 Dateien geschrieben (31 Lua, 17 Modell/Bild/Knoten, Texte), Pruefer je Datei gruen, luacheck_pz 0 + 3 erlaubt, Cheat-Pruefung **Funde 0**; keine Bench-Datei in der Probe (0 Treffer); die 31 kopierten Lua byte-gleich dem Staging; Ausgabe bis auf Pfade gleich `probe_f1_nach_ausgabe.txt` |
| Namen | `BanditsNPCBearWindow/Key/Pose/Tags/WinData/WinParts/Order`, "Bear window", "NPC Crew Bear", `UI_BN_Bear_`, `BearRoamRadius`, `NCBear_Cub`, `WinTyping`, `PoseHands`, `ReviveForget` in NPC Crew `42/media/lua`: je 0 Dateien; Landkarte 0 |

## 3. Nachzaehlung Staging und was in der Test-Mod ueberschrieben wuerde

`staging_dateien.txt` gegen die Platte (eigenes Skript `gp/zaehlen.py`): **67 Eintraege = 67 Dateien**, keine fehlt, keine zu viel, **MD5, Bytes und
Art alle gleich** (0 Abweichungen). Gegen `Zomboid/mods/NCBearTest` heute: **7 neu, 32 ueberschreibt, 28 gleich** -- wie die Liste.

Ueberschrieben wuerden genau diese 32 (alle gewollt, alle schon frueher aus diesem Staging gekommen):
- Lua (17): `client/BanditsNPCBearClient.lua`, `...Menu.lua`, `...Options.lua`, `client/ISUI/BanditsNPCBearHud.lua`, `client/NCBearBenchCub.lua`
  (die Testhilfe DIESES Laufs), `server/BanditsNPCBearFollow / Grow / Guard / Heal / Registry / Ride / Server / World.lua`,
  `shared/BanditsNPCBear.lua`, `...Defs.lua`, `...Rules.lua`, `shared/TimedActions/BanditsNPCBearFeedAction.lua`.
- Texte (14): `Translate/<7 Sprachen>/UI.json` und `Sandbox.json`. Eigener Schluessel-Vergleich (`gp/json_diff.py`): **0 Schluessel weg,
  0 Werte geaendert**, nur dazu (UI.json 157 -> 276, Sandbox.json 60 -> 62 je Sprache).
- `42/media/sandbox-options.txt`: `diff` zeigt **nur 8 Zeilen dazu** (Option `BanditsNPC.BearRoamRadius`), nichts weg.

**Alte NCBear*-Dateien: keine wird beruehrt.** Die Test-Mod hat 12 NCBear*-Lua; im Staging liegt davon nur `NCBearBenchCub.lua` (die eigene
Testhilfe). `NCBearDefs/Fight/Test/Spawn/Size/AttackProbe.lua`, `NCBearBench.lua`, `NCBearBenchVergleich*.lua` und die sechs Dateien des
Laufs baer-gen-gross vom 12.11. 01:02 (`NCBearBenchGen.lua`, `NCBearBenchGenDefs.lua`, `NCBearGen.glb`, `NCBearBenchGen.txt`,
`NCBearGen.png`, `NCBearGenFoto.png`) bleiben unangetastet. Keine der alten Dateien fragt Tasten ab (grep `OnKeyPressed|KEY_V|isKey(`: 0);
die Gen-Testhilfe hat nur `NCBear_Gen*`-Namen (keine Kollision mit `NCBear_CubWin/BodyGone/View`).

Tasten-Kollisionen (fuer Kevins Bericht): V liegt in Vanilla auf Fahrzeug-Radial und Tier-Radial (`V:shared/keyBinding.lua:131-132`,
`:186-187`), "Toggle UI" ist ab Werk leer (`:142-143`); in NPC Crew auf "Talk to NPC" (`NC:client/BanditsNPCInteract.lua:7462`). NPC Crews
andere Tasten: F6 (`NC:client/BanditsNPCModOptions.lua:138-141`), F8 Beacon (`NC:client/ISUI/BanditsNPCBeaconWindow.lua:130`). K ist in
Vanilla frei (kein `KEY_K` in `keyBinding.lua`) -- guter Vorschlag zum Umstellen.

## 4. Eigene Stichproben

**S1 -- Unstuck eines NICHT geladenen Baeren, Zeile fuer Zeile** (`gp/stich_unstuck.lua`, echte Staging-Dateien, SP): **8 / 0**.
- Fenster: `WinData.lua:416` gone (ld fehlt) -> Follow/Stay/Sit/Roam/Come grau "Out of reach"; Unstuck nur grau bei Mitfahren, Auto,
  Abklingzeit (`:443`) -> frei. Klick -> `Window.lua:449-450` `B.Ask(player, "Call", { id })` -> SP direkt `B.Handle` (`S:shared/BanditsNPCBear.lua:561-570`),
  MP `sendClientCommand`; Verteiler `S:server/BanditsNPCBearServer.lua:412`.
- `S:server/BanditsNPCBearRide.lua:301-370`: Eintrag, Besitzer, tame/missing, nicht mitfahrend, Spieler nicht im Auto, Abklingzeit, freie
  stehbare Kachel 1..3 neben dem SPIELER (`B.SpotNear`), Frisch-Riegel, Drossel; alter Koerper nicht gefunden und Gegend nicht geladen -> kein
  Suchlauf; `B.PlaceCub` (gen + 1, missing -> tame, Spiegel sofort, `:72-110`); Modus follow, Abklingzeit, Meldung.
- Attrappe: Eintrag bleibt "tame" solange die Gegend entladen ist; Call -> genau 1 neuer Koerper <= 3 Kacheln neben dem Spieler, gen + 1,
  follow, "Here is your cub again."; zweiter Call sofort abgelehnt, kein zweiter Koerper; Gegend laedt, alter Koerper taucht auf -> "stale",
  nie gebunden, vom Waisen-Suchlauf (je 120 s, `Server.lua:1067-1070`) entfernt (hier nach 102 s, Spieler weit weg), danach **genau ein Baer**.

**S2 -- C1 nach dem LADEN ohne Doppel** (`gp/stich_c1_laden.lua`; Neuladen = `B.InitRegistry()` mit frischer Sitzung und Heil-Fenster 120 s,
alter Koerper vom Tier-Lader spaeter geliefert): **8 / 0**.
- L1: Lader liefert nach 90 s -> an den alten Koerper gebunden, **kein** neuer Koerper in 5 min, genau 1 Baer.
- L2: Lader liefert erst nach 240 s -> C1 macht genau EINEN neuen Koerper nach 133,5 s (nie im Heil-Fenster); der alte kommt als "stale",
  wird nie gebunden; **solange der Spieler naeher als 25 Kacheln steht, stehen zwei Baeren da** (der alte ohne Bindung), nach dem Weggehen
  wird der alte entfernt, Eintrag bleibt am neuen. -> Restbefund N1 (nur wenn der Lader laenger als 2 min braucht; Dauer ungeprueft).

**S3 -- Sitz -> Folgen -> Mitfahren (gelesen):** Sitz: `HandleMode` haelt sofort, Heimat = Kachel von jetzt (`Follow.lua:301-305`),
`OrderStep` "hold" + `settle` -> Sicht `sit` (`Order.lua:132-135`, `Registry.lua:613`) -> Treiber sitdown -> sit (`Pose.lua:96-127`). Folgen:
`SetMode` merkt `standUntil` (`Follow.lua:108-110`), Sicht ohne sit -> Treiber standup -> loeschen (`Pose.lua:136-142`), `StandStep` haelt 2,3 s
(`Order.lua:193-204`), dann folgt er. Einsteigen nur aus dem Folgen (Regel 11, `B.RideBoard`); der Koerper verschwindet -> `U.CubObj` nil ->
Treiber-Eintrag weg (`Pose.lua:86-90`); Aussteigen -> neuer Koerper "follow", kein Sitzen. Ein SITZENDER Baer steigt nie ein (bleibt sitzen,
Folgen-Knopf im Auto grau "in a car") -- schluessig.

## 5. Neue Restbefunde (keiner rot, keiner blockiert den Test)

- **N1 (minor, ungeprueft Laufzeit):** Braucht der Tier-Lader nach dem Laden laenger als ~2 min, macht C1 einen neuen Koerper und der alte
  steht als zweiter Baer ohne Bindung daneben, bis der Spieler > 25 Kacheln weg ist und ein Suchlauf laeuft (S2-L2). Dasselbe nach Unstuck
  eines nicht geladenen Baeren, wenn Kevin schnell zur alten Stelle laeuft (Waisen-Suchlauf nur je 120 s, entfernt nur unbeobachtet,
  `World.lua:669-676`). Bekannte B1c-Bauart, jetzt haeufiger erreichbar. Im Test: "zwei Baeren?" beobachten.
- **N2 (minor, Optik):** Namensschild aus/an wird je RECHNER in `BanditsNPCBear.ini` nach dem Kennzeichen `u` gespeichert
  (`S:client/BanditsNPCBearTags.lua:5-8`). `u` zaehlt je Register; in einem anderen Spielstand kann ein anderer Baer dieselbe Nummer haben ->
  sein Schild ist dann auch aus. Spaeter z. B. Epoche dazunehmen.
- **N3 (minor, Bedienung):** V ohne eigenen Baeren, nicht am Auto/Tier, zeigt jedes Mal "You do not have a bear yet." (`Window.lua:617-620`).
  Mit NPC Crew (V = "Talk to NPC") kommt der Satz bei jedem V, das keinen NPC trifft. Kevin-Frage 9.
- **N4 (minor, nur MP):** An einem FREMDEN gezaehmten Baeren bleibt Vanillas Radial samt "Kill" (A2 so gewollt), der Rechtsklick blendet "Kill"
  fuer alle aus (`S:client/BanditsNPCBearMenu.lua:309-311`). Unstimmig, aber vor F1 genauso; Thema fuer B5a/MP.
- **N5 (trivial):** `B.HandleCall` vergisst die C1-Frist nicht (`B.ReviveForget` fehlt nach Erfolg, `Ride.lua:368-374`); ein sofort wieder
  verlorener Koerper koennte die alte Frist erben. Harmlos (der alte Koerper waere ohnehin "stale").
- **N6 (Wortlaut):** "No body now." liest sich leicht wie "Nobody now". Vorschlag: "It has no body right now. ..." (Fensterbreite pruefen).

## 6. Fragen fuer Kevin (gebaut ist jeweils die Empfehlung)

1. "Komm her" (geht zu dir, keine Wartezeit) und "Unstuck" (= Call to me, 5 min Wartezeit) als zwei Knoepfe -- so lassen?
2. "Frei herumlaufen" hoechstens 12 Kacheln statt 8 (wie dein Bleiben-Radius 12) -- ok?
3. Baer in Vanillas Tier-Anhaenger: gebaut "zu gross" (er faehrt wie die Crew im Auto mit) -- ok?
4. Baer ohne Koerper kommt nach ~1-1,5 min von selbst wieder, nie in den ersten 2 min nach dem Laden -- ok?
5. Zaehm-Fortschritt ("Taming 40%") spaeter im V-Fenster, solange du das Junge noch zaehmst?
6. V an einem fremden Baeren (Mehrspieler): Vanillas Tier-Radial statt deines Fensters -- ok?
7. An deinem Baeren geht Vanillas Tier-Radial (V) sofort zu (dort gab es "Kill"); "Animal info" gibt es weiter im Rechtsklick -- ok?
8. Im Auto gehoert V dem Fahrzeug-Radial; das Baeren-Fenster dort nur, wenn es vorher offen war oder mit anderer Taste -- ok?
9. (neu, N3) Hinweis "You do not have a bear yet." bei jedem V ohne Baeren -- lassen oder nur einmal je Minute?

## 7. Fazit fuer den Test

Laedt statisch ohne Fehler (alle Pruefer gruen, keine neue Engine-Methode ohne Fundstelle; Key/Window/WinParts legen auf Dateiebene nur
Klassen und die eine `keyBinding`-Zeile an, Form wie NPC Crew `BanditsNPCInteract.lua:7451-7462`, gespielt). V oeffnet/schliesst, Taste in
Optionen -> Tastaturbelegung -> "NPC Crew: Bear" -> "Bear window" umstellbar (`MainOptions.lua:2165`, `:2177`, Texte in 7 Sprachen). Werte
im Fenster und `NCBear_CubStats()` kommen aus denselben Formeln (`B.GrowView` / `B.StatsOf`, `B.SkillProgress`); das Fenster rechnet in
ganzen Prozent (Leben/Ausdauer koennen um 1-2 Punkte abweichen). Jeder Befehl hat eine sichtbare Wirkung beim Schreiber; 4K: Faktor 2,0,
Fenster 1280 x 1178, Schrift Large/Medium/Small (40/33/26 px) bei Vanilla-Schrift 2x. B1a-B1e: alle alten Attrappen unveraendert gruen.
Nach dem Einbau (erst wenn Kevins Spiel zu ist, vorher/nachher sichern, direkt davor Trockenlauf und Probe noch einmal) das Spiel neu starten.
Statisch geprueft, nicht gespielt.
