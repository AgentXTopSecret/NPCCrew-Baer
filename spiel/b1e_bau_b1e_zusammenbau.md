# Lauf baer-b1e: ZUSAMMENBAU + UEBERNAHME (B1e Modellwechsel ab Halbstark, groessere Markierung)

Stand 11.11.2026 abends. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (B1a-B1d + B1e KERN +
B1e OBERFLAECHE). Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart, kein Download.
**Im Staging-Lua wurde nichts geaendert** (keine Luecke ueber die Grenze). Im Staging nur das alte Junge zurueckgelegt (PLAN_B1E.md 10.1).
Geschrieben: `attrappe/gesamt/run.lua` (Abschnitt 20, `addAnimal`-Huelle, Kopf), `attrappe/gesamt/xref_b1e.py` + `xref_b1e.txt` (neu),
`attrappe/gesamt/gegenprobe_b1e.py` + `gegenprobe_b1e.txt` (neu), `attrappe/gesamt/ergebnis.txt`, `ergebnis_probe.txt`,
`attrappe/uebernahme_b1e/probe_regeln_b1e.py` + `.txt` (neu), `attrappe/b1c_kern/ergebnis_b1e.txt`, `attrappe/b1d_kern/ergebnis_b1e.txt`
(Vergleichsstand nach B1e), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `staging_dateien.txt`, `mod_info_vorschlag.txt`, ein Absatz
"B1e ZUSAMMENBAU" in `schnittstelle_aenderungen.md`, die Probe unter `probe_b1e/` und die Ausgaben `trockenlauf_b1e.txt`,
`trockenlauf_b1e_vor_b5a.txt`, `probe_b1e_ausgabe.txt`. Nach dem Einbau muss Kevin das Spiel **neu starten** (neue Tierart, Lua, Bilder).

## 0. Ergebnis

| Pruefung | Ergebnis |
|---|---|
| Vorab: Staging gegen Test-Mod (MD5) | vor dem Bau laut beiden Bauern 49 von 51 gleich, verschieden nur `NCBearCub.glb`/`.png` (Generator-Junges im Staging); beim Zusammenbau nachgezaehlt: 60 Dateien, alle Abweichungen = B1e-Aenderungen + 9 neue Bilder + die zwei Junges-Dateien; jetzt altes Junges 6c3f0a96 / 2ee25f24 im Staging, **gleich mit der Test-Mod** (Git main **96035c3**, nicht mehr 401dd70) |
| Grenze KERN <-> OBERFLAECHE (`attrappe/gesamt/xref_b1e.py`, neu) | **0 Luecken**, 3 Hinweise (bekannte Rueckfallwerte in Rules.lua, B1c Z3) -- `xref_b1e.txt` |
| Gegenprobe (`gegenprobe_b1e.py`, Temp-Kopie, je eine Verderbnis) | **30 von 30 erkannt** (16 x xref, 14 x Gesamt-Attrappe) |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` | **1672 bestanden, 0 Fehler** (vorher 1172; Abschnitt 20 neu: 500 Pruefungen = 150 Ablauf-Pruefungen + 350 Lade-Pruefungen bei 14 Ladevorgaengen); `***`-Zeilen nur die drei gewollten Heilungen 18c, 19f, 20e |
| dieselbe gegen die Probe (`probe_b1e/NPCCrew/42/media/lua/`) | **1672 / 0**, `ergebnis_probe.txt` **byte-gleich** mit `ergebnis.txt` |
| Attrappen der Bauer auf dem Endstand | kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1d_kern 162/0, **b1e_kern 153/0**; ober 116 + 117, b1b_ober 144 + 134, b1c_ober 155 + 142, b1d_ober 174 + 176, **b1e_ober 218 + 218** (Kern-Attrappe + echter Kern), je 0 Fehler; pruef_b, pruef_b1b (`run_nach`), pruef_b1c, pruef_b1d byte-gleich mit ihren gespeicherten Ergebnissen; kern und b1b_kern, b1e_kern byte-gleich mit `ergebnis.txt` |
| Text-/Bild-/Beleg-Pruefer | `texte_pruefen_b1e.py --tmp` 0, `bilder_pruefen_b1e.py --tmp` 0 (Werkzeug byte-gleich), `texte_pruefen*.py` (ober, b1b, b1c, b1d) je 0; Belege `belege.py` 0/112, `_b1b` 0/51, `_b1c` 0/89, `_b1d` 0/23, `_b1e` 0/53 |
| Lua-Pruefer (25 Lua-Dateien des Stagings) | luacheck 0 failed, scopecheck 0, localcount hoechstens 77 insgesamt (World.lua :664, unveraendert), luacheck_pz 18 x W113 = die bekannten (15 Bench, 3 Aktionsklassen im Menue); luac5.1 -p alle ohne Fehler; alle LF, reines ASCII |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen** (24 Altlasten + 2 neue Defs-Fundstellen `ALT_DEFS` + 1 Clip-Warnung GLB + 1 NPC-Crew-Kommentar) |
| Trockenlauf ohne `--vor-b5a` | **26 Fehler = genau die 24 Altlasten + 2 `ALT_DEFS`** ("Erwartet rot ... sonst nichts") |
| Gegenprobe der neuen Skript-Regeln (`probe_regeln_b1e.py`) | **8 von 8 wie erwartet** (7 Verderbnisse erkannt, unveraendertes Staging gruen) |
| Probe `--probe probe_b1e --staging ... --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen**; 60 Dateien geschrieben (24 Lua, 14 Modell/Textur/Skript/Knoten/Bild, 21 Texte, `sandbox-options.txt`); vier Lua-Pruefer je kopierter Datei gruen, luacheck_pz 0 + 3 erlaubt |
| `staging_dateien.txt` neu | **60 Dateien: 9 neu, 35 ueberschreibt, 16 gleich** (gegen NCBearTest 96035c3); 37 gegen die B1d-Liste geaendert (35 + das alte Junge zurueck) |

## 1. Grenze KERN <-> OBERFLAECHE

### 1.1 Werkzeug `attrappe/gesamt/xref_b1e.py` (neu; `xref_b1d.py` prueft den B1d-Plan und meldet B1e deshalb als 25 Luecken)
Aufruf `python -I xref_b1e.py [lua-Ordner]` (Vorgabe Staging), Exit 1 bei einer Luecke. Alles aus `xref_b1d.py` plus (Ergebnis `xref_b1e.txt`):
1. **B.*/U.***: 206 / 206 Namen definiert, U.* 24 / 24; **94 Funktionen** aus Plan 6.2/6.3/6.5 je in ihrer Datei (neu: `BodyKind`/`NoteBd`/
   `ViewOf` in `shared/BanditsNPCBear.lua`, `BodyWant`/`BodySize`/`BodyNow`/`BodyNum`/`BodyGap` in Stats.lua, `CreateCub`/`RemoveCub`/
   `FindAnimal`/`SwapSpot` in World.lua, `BodySwapReady`/`BodySwap`/`BodyBusy` in Grow.lua, `U.TB`/`U.CubName` in Client.lua,
   `U.MarkerLayout`/`U.MarkerFactor` in Marker.lua). Die OBERFLAECHE ruft vom KERN nur die Liste aus Plan 6.10 (neu: `BodyKind`, `DistXY`;
   `CUB` nur als Existenz-Riegel). Bench ruft `BodyKind`, `BodySwapReady`, `BodyWant` (Plan 1.6), alle definiert. Ladefolge: 0 Aufrufe auf
   Dateiebene vor ihrer Definition.
2. **B.CFG** (178 Felder): die 26 Stellwerte aus Plan 5 **mit ihren Zahlen** (bodySwap **true**, swapSize 0,72, swapBackSize 0,70,
   swapMinMs 60000, swapRetryMs 10000, swapFailLog 6, swapRing 2, swapFaceDist 30, busyMs 20000, walkSpeedBig 0,67, runSpeedBig 3,17,
   bodyLenBig 1,0448, tilesPerE 1,5, followRefLen 1,12, tagBigK 1,06, petAnimBig "cow", markerAngleAdd 135, markerCloseTiles 6,6,
   markerR/G/B 1,0/0,52/0,09; bleiben cubMaxSize 0,75, walkSpeed 0,52, runSpeed 2,47, markerShift 100, markerMs 400, markerAfterMs 60000),
   alle gelesen (`B.BodyNum(body, "key")` zaehlt `key` UND `keyBig`, auch ueber die Variable `key` in `B.MoveTo`); `markerDur` steht und wird
   bewusst nicht mehr gelesen (Plan 5). **Art `ncbeargrown`** (Defs.lua): `minSize` 0,72 == `B.CFG.swapSize`, `maxSize` 1,35 ==
   `stageAt[3]`, `bodyModel "NCBear_Body"`, `ageToGrow` 36500. **Optionen-Seite**: `MarkerSize` (combobox, 7 Eintraege
   Auto/Pct100...Pct300, Vorgabe Index 1) nach `TagSize`; der Leser `U.Opt("MarkerSize", 1)` hat dieselbe Vorgabe.
3. **Befehle**: unveraendert (B1e bringt keinen neuen Befehl, kein neues `sendClientCommand`).
4. **Sicht**: `B.GrowView` baut zusaetzlich `bd` (aus `B.StatsOf` -> `B.BodyNow(rec)`); die OBERFLAECHE liest `c.bd`/`v.bd` (Hud, Menue,
   Namensfenster, Streich-Haltung) und sonst nichts Neues.
5. **Texte**: UI.json 157, Sandbox.json 60, IG_UI.json 4 je Sprache, Paritaet/Platzhalter/sortiert/Round-Trip/BOM/CR in 7 Sprachen;
   die 24 B1e-Schluessel + `IGUI_AnimalType_ncbeargrown` in allen 7 Sprachen, **EN wortgleich mit Plan 6.8** (dazu "Bear"); **105
   Big-Fassungen** (15 x 7) je mit Grundschluessel, gleichen Platzhaltern und anderem Text; `U.EN` 157 == EN/UI.json; jede Big-Fassung gilt
   als benutzt (Grundschluessel ueber `U.TB` -- Menu_Name, Menu_CallTip, Why_CallWait, Name_Title, Tag_Name -- oder als Meldung durch
   `B.NoteBd`); 0 EN-Schluessel unbenutzt.
6. **Meldungen**: genau die 11 Meldungen aus Plan 6.4 gehen im KERN durch `B.NoteBd(...)` (SetMode baut sie in `n`), je mit Big-Fassung;
   `Note_Grown` ohne; `U.NoteText`/`U.TB` waehlen Big nur bei `bd == "big"` UND vorhandenem `U.EN`-Schluessel.
7. **Bilder**: 10 Bilder in Plan-Groesse, alle RGBA, jedes vom Code genannt; das 96er-Symbol (nur Karte) byte-gleich mit Kevins Quelle
   (9e45e936); die Markierung nimmt die 9 neuen (288er Scheibe/Ring/Symbol, Pfeile 96..288).
8. **Dateiregeln**: `:setSizeForced(`/`:getData(` nur `B.ApplySize`, `:setHealth(`/`:getHealth(` nur `B.BodyHp`; **neu** `:getAnimalType(`
   nur `B.BodyKind` (Bench druckt), `addAnimal(`/`:addToWorld(` nur `B.CreateCub`, `B.CreateCub(` nur aus `B.AppearFor`/`B.PlaceCub`,
   `:faceThisObject(` am Tier nur `B.BodySwap` (TimedActions wie Vanilla ISPetAnimal.lua:17 seit B1a ausgenommen); **0 Vergleiche** mit
   `B.CUB`/`getAnimalType()` (auch Bench); `NCBear_*` ausser der Bench nur `bodyModel "NCBear_Body"`; 0 x `BanditEventMarkerHandler.set`;
   Markierung und Optionen ohne pcall (die drei alten pcall um eigene Takt-Rumpfe aus B1b/B1c als Hinweis).
9. **"keine Stelle prueft mehr nur auf B.CUB"**: 10 Nennungen von `B.CUB`/`"ncbearcub"` im Code, alle eingeordnet (Definition, die zwei
   Tabellen, Defs.lua, 2 Existenz-Riegel im Menue, Fehlerzeilen-Text in Ride.lua, Rueckfall `B.BODY_TYPE[...] or B.CUB` in World.lua).

**Gegenprobe** (`gegenprobe_b1e.py`, Temp-Kopie): xref -- GrowView ohne `bd`, Hud liest `c.bdx`, RideOff ohne `B.NoteBd`, RU ohne
`Note_FollowBig`, PTBR `Tag_NameBig` ohne `%1`, KO ohne IGUI-Name, `minSize` 0,70, `bodySwap = false`, `walkSpeedBig 0.7`, Art-Vergleich im
Menue, Hud-Suchlauf nur Junges, MarkerSize ohne Vorgabe, Markierung ruft `BanditEventMarkerHandler.set`, OBERFLAECHE ruft `B.BodySwap`,
`faceThisObject` in World.lua, Pfeil-Bild 192 fehlt -> **16 von 16 erkannt**. Gesamt-Attrappe -- kein Tausch (49 Fehler), altes Junges
bleibt stehen (57), PlaceCub ohne `B.BodyOf` (9), Groesse ohne Abbildung (6), Tausch ignoriert busy (1), GrowSetG laesst swapAt (3), Hud
bindet nur das Junge (3), `U.TB` ohne Big (3), `B.NoteBd` setzt nichts (5), Markierung immer 100 % (4), Streicheln ohne Kuh-Haltung (2),
Fuettern ohne Marke (1), Sicht ohne `bd` (12), Heilung ohne `body` (1) -> **14 von 14 rot**, jede mit Fehlern in Abschnitt 20 (nur
"altes Junges bleibt stehen" trifft auch 11 Pruefungen davor).

### 1.2 Von Hand nachgesehen (was ein Grep nicht sieht)
- **MP-Tauschfenster**: der Client ordnet Tiere ohne Spiegel ueber die OnlineID zu (`B.ViewOf`); die Sicht traegt nach dem Tausch die NEUE
  `oid` -> eine noch nicht entfernte alte Junges-Kopie wird nicht gebunden, und die Groessen-Probe setzt nur an einer Kopie der Art aus
  `c.bd` (`client/ISUI/BanditsNPCBearHud.lua:474`). Gesamt 20m: Sync an A und B mit `bd big` + neuer `oid`, Probe an Bs grosser Kopie genau 1 x.
- **Reihenfolge im Tausch**: `B.PlaceCub` setzt `rec.body` VOR `B.Commit`/`B.WriteMark`, die Meldungen danach tragen `bd` (RideOff nach
  `B.PlaceCub`, `server/BanditsNPCBearRide.lua:230-236`; Called nach `B.PlaceCub`, `:345-359`). Gesamt 20g/20h zeigen die Big-Texte.
- **Tageszaehlung 14**: gezeigt 0,7235 -> 0,724 (14 Tage + die 10 Spielminuten des ersten Langsam-Takts); Plan 2.4 nennt 0,723 fuer genau
  Tag 14 -- gleiche Kurve, Rundung auf 3 Stellen.
- **Messung** (`mess_b1e/ausgabe.txt`): mit dem ALTEN Jungen 6c3f0a96 und dem grossen Baeren 08ec7806 (= MD5 von `NCBear.glb` in der
  Test-Mod, nachgezaehlt): Laenge 0,9966 / 1,0448 E, Oberkante 0,5894 / 0,6254 E; 0,72 x gross gegen 0,75 x Junges = Laenge +0,6 %,
  Oberkante +1,9 %; Tag 100: 1,35 = der Erwachsene bei 1,35 (gleiches Netz).
- **NPC Crew** (nur gelesen, v3.14.73): `ncbeargrown`, `BodyKind`, `MarkerSize`, `BanditsNPCBearMarker_` 0 Treffer; `setSizeForced`/
  `getData():setSize`/`:setSize(` 0 Dateien; die neue Art traegt die Gruppe `ncbear` (Kopie der Junges-Definition) -> Naht 1 (NOT_TENDED)
  gilt mit; `BanditsNPC.Opt` jetzt bei `shared/BanditsNPC.lua:6107`.

### 1.3 Luecken geschlossen
**Keine Luecke ueber die Grenze; kein Lua im Staging geaendert.** Erledigt nach PLAN_B1E.md 10.1: das alte Junge liegt wieder im Staging
(`mod/42/media/models_X/Skinned/NCBearCub.glb` 6c3f0a96ba9a2aaf3a06eabc184cdbc3 / 1226188 Bytes, `mod/42/media/textures/Body/NCBearCub.png`
2ee25f24c4f0f05bfbb955d4d4b17aea / 1303826 Bytes, aus `_arbeit/baer_baby/entwurf/`, byte-gleich mit der Test-Mod und mit
`NCBearBenchCubAlt.glb`). Die vom KERN gemeldete Cheat-Ausnahme `"NCBear_Body"` ist im Uebernahme-Skript ergaenzt (3).

## 2. Gesamt-Attrappe `attrappe/gesamt/run.lua`, Abschnitt 20 (neu, Plan 7.3, Vorgabe `bodySwap = true`)
Gewollt geaendert sonst nur: die `addAnimal`-Huelle zaehlt `faceThisObject` wie die Kern-Attrappe (vorher verschluckt), Kopf-Kommentar.
Abschnitt 19 laeuft seit dem KERN-Bau mit dem Not-Aus `bodySwap = false` (gewollt, `bau_b1e_kern.md` 6). Alles in einer namenlosen Funktion.
- **20a** wildes Junges (Art `ncbearcub`) -> ueber Menue und Zeitaktion gezaehmt; erster Hirn-Takt `rec.body = cub`; Schild "Kate's cub";
  Name "Bruno"; **14 Spieltage echte Langsam-Takte**: genau das Junge, gezeigt 0,724 = Engine-Groesse, will weiter cub, Sicht `bd cub`,
  keine "half-grown"-Meldung, kein grosser Koerper in der Welt.
- **20b** Tag 15: genau eine "Your bear is half-grown now." (Langsam-Takt), Junges noch da; **naechster Hirn-Takt tauscht**: altes Junges
  entfernt, genau ein `addAnimal`, **genau ein Koerper `ncbeargrown`**, gleicher Eintrag (id, u, Besitzer, Name, Modus, Zaehmung, Heimat, g,
  Erfahrung, Leben, Fuetter-Bonus, tamedAt ...), gen + 1, r gestiegen, neue AnimalID/OnlineID, `body big`, Groesse ~0,72 nach der
  Abbildung, Leben aus dem Register, Spiegel `body big`/neue gen, schaut zum Besitzer, keine eigene Meldung, Sitzung `swapAt`; Sicht `bd big`
  + neue `oid` + halbstark; kein zweiter Tausch; Schild "Bruno" ueber dem grossen Koerper; `NCBear_CubStats()` "body big / want big /
  engine type ncbeargrown", "swap waits (cool)"; Werte halbstark (Leben max ~150).
- **20c** grosser Koerper: Menue Feed/Pet/Follow me/**"Name the bear"**/Call mit "your bear"-Tooltip, kein Kill; "Your bear follows you.";
  Abstand-Zuschlag ~0; Tempo 0,67 / 3,17; rennt hinterher; **Fuettern**: waehrend der Aktion `B.BodySwapReady` -> "busy", nach `complete()`
  frei; **Streicheln** Haltung "cow", AnimalSizeY aus der Sicht (~0,01); **Zombie**: versteckt sich (hide), Tausch "guard"; **Laerm**: eine
  Antwort im selben Bild, Tausch "calm"; immer genau ein Koerper.
- **20d** Tag 45: "strong", gezeigt = 0,72 + (s - 0,75) x 1,05 (~0,982); **Tag 100**: "full-grown", g 1, **Engine-Groesse 1,35**,
  Abstand-Zuschlag ~0,50, Sicht `bd big` / 1,35 / Tag 100 / erwachsen, Leben max 400, ein Koerper.
- **20e** Register verloren (Absturz), Spiegel am grossen Koerper bleibt -> Eintrag zurueck (Besitzer, Name), **body big, gleiche gen**, "Your
  bear is back.", kein Tausch, derselbe grosse Koerper bei 1,35.
- **20f** `NCBear_CubGrow(-100)` -> "body cub (swapped)", grosser Koerper entfernt, ein Junges 0,35, Sicht `bd cub`; `NCBear_CubGrow(15)` ->
  "body big (swapped)" (von Hand ohne Abklingzeit); **Tod** des grossen Koerpers -> Eintrag zu, Sitzung leer, "Your bear is dead. ...".
- **20g um die Schwelle -- Mitfahren**: Junges bei 0,74 steigt ein (Koerper weg, body bleibt cub), 1 Spieltag Fahrt -> "half-grown" in der
  Fahrt, **Speichern/Laden in der Fahrt** (ride, body cub, gen gleich), steigt **gross** aus (ein Koerper, body big, gen + 1, Groesse nach der
  Abbildung, "Your bear climbs out."), kein Junges mehr in der Welt, danach kein weiterer Tausch.
- **20h um die Schwelle -- Call to me**: will gross, hat noch das Junge (nur Langsam-Takte) -> Call: Junges entfernt, ein grosser Koerper
  neben dem Besitzer, gen + 1, "Here is your bear again.", danach kein weiterer Tausch.
- **20i um die Schwelle -- Speichern/Laden**: gross bleibt gross (gleiche gen, verstellte Groesse wird nachgesetzt); **Spielstand von B1d**
  (Not-Aus, Junges bei 0,75 mit innerer Groesse 0,85, `body` aus Register und Spiegel genommen) -> mit Vorgabe geladen -> erster sicherer
  Takt tauscht (gen + 1), Groesse nach der Abbildung, **keine Fehlerzeile**.
- **20j / 20k Sandbox 30 / 365 Tage**: zwei Langsam-Takte vor Tag 4,5 bzw. 54,75 noch das Junge; Tausch mit dem ersten Hirn-Takt nach der
  Schwelle (je auf einen Takt genau), ~0,72; ohne Namen Schild **"Kate's bear"**.
- **20l Markierung 3840 x 2054**: ohne Bandits sichtbar, Auto 200 % (Kreis 192, Klickflaeche 90, Large, Lage (1824, 96), Pfeil-Bild 192);
  mit Bandits gleich, kein `BanditEventMarkerHandler.set`.
- **20m MP** (Server + A Besitzer + B fremd, Sandbox 10 Tage): A 2 Spieltage abgemeldet -> kein Wachstum, kein Tausch; nach 1,5 Spieltagen mit
  A tauscht der Server: ein Koerper, `removeAnimal(alte OnlineID)`, gen + 1, kein `sendClientCommand`; Sicht an A und B `bd big`, neue `oid`,
  gleiche `sz`; Client B: Probe setzt die Groesse seiner grossen Kopie genau einmal; A "Follow me" -> `Note_Follow` mit `bd big` nur an A,
  Client zeigt "Your bear follows you."; B fuettert -> `Why_NotOwner`, Fisch bleibt; Server-Neustart: derselbe grosse Koerper, kein Tausch;
  keine `***`-Zeile.

**Grenze der Attrappe** (wie B1a-B1d): ein Lua-Zustand fuer Server und Clients; `addToWorld` ist sofort "in der Welt", `fleeTo`/
`pathToLocation` setzen das Tier sofort ans Ziel; Groesse/Leben/Laden/Netz bildet sie nach (NUR JAR), beweist sie nicht.

## 3. Uebernahme-Skript `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md` (Plan 10.3/10.4)

### 3.1 Was sich aenderte
- `TEXT_NS["IG_UI.json"]` + `IGUI_AnimalType_ncbeargrown`.
- **`ALT_DEFS`** (neu, wie `ALT_EXPECTED`): Rassen-Textur `NCBear` und `bodyModel "NCBear_Body"` der Art `ncbeargrown` sind erlaubte Fundstellen
  bis B5a -- ohne `--vor-b5a` Fehler (Trockenlauf absichtlich rot), mit Warnung; liegt das Teil spaeter in der Uebernahme, warnt das Skript
  "streichen". `NCBear.glb`/`nc_bear_tier.txt` werden NICHT mitkopiert (Hirsch-Rueckfall `NCBearStag_Body`, F9). Der Schluss "Erwartet rot"
  zaehlt 24 + 2.
- **Cheat-Ausnahme** `bodyModel = "NCBear_Body"` (Regel `befehl`), mit Grund.
- **Neue Tier-Regeln**: `getAnimalType` (jedes Vorkommen im Code-Teil, auch als String) nur in `B.BodyKind`; `artvergleich` (`== / ~= B.CUB`)
  nirgends erlaubt. Die alten Tier-Regeln bleiben gruen (Tausch ueber `B.PlaceCub` -> `B.CreateCub`, `B.RemoveCub`). Neue Bilder ueber `UI_ASSET`.
- Kopftext (B1e-Zeile, Punkt 6 mit den B1e-Regeln), Naehte-Zeile im Plan-Ausdruck.
- `NAEHTE.md`: Kopf (B1e, NPC Crew v3.14.73, `Opt` :6107), Zeilen 3, 5 (157 / IG_UI 4), 6, 8, 10 (altes Junges zurueck; grosser Koerper
  nutzt `NCBear_Body`), 11 (`body`, Sitzung, Spiegel, Sicht `bd`), 14, 15 (Modellwechsel gebaut), 17 (Suchlauf beide Arten), 19 (`MarkerSize`),
  20 (Markierung als eigenes Element, Bandits nur gelesen, laeuft ohne Bandits), 24 (10 Bilder), **neu 26** (Art `ncbeargrown`); "Erlaubte
  Fundstellen" 25-26; Cheat-Ausnahme; Absatz "B1e, vom Skript erzwungen"; B5a-Abhaengigkeit (endgueltiges model-Skript, `bodyModel`/Textur
  nachziehen, Artname bleibt, Kampf/Stimmen fuer `ncbeargrown`).

### 3.2 Laeufe (Ausgaben im Ordner `_arbeit/baer_zaehmen/`)
- `trockenlauf_b1e_vor_b5a.txt`: **OK, 0 Fehler, 28 Warnungen**. Kopieren: 24 Lua, 14 Modell/Textur/Skript/Knoten/Bild (2,9 MB). Texte: UI.json
  157 neu (NPC Crew 3814 -> 3971), Sandbox.json 59 neu (92 -> 151), IG_UI.json 4 (neu). Sandbox 27 Optionen (NPC Crew vorher 42). Cheat-Pruefung:
  24 Lua, 7152 Codezeilen, **Funde 0**, 2 Ausnahmen greifen; Tier-Regeln je an ihrem Ort (getAnimalType Bear.lua:499 `B.BodyKind`,
  artvergleich: kein Vorkommen). "Texte aus der Lua: 134 benutzt, fehlen in EN: 0; Ersatztexte 157, wortgleich: ja". Kollisionen 0.
- `trockenlauf_b1e.txt` (ohne `--vor-b5a`): 26 Fehler, alle "noch umzubenennen (B5a)", 0 andere.
- `probe_b1e_ausgabe.txt` (nur unter `_arbeit/baer_zaehmen/probe_b1e/`): OK, 0 Fehler, 28 Warnungen, 60 Dateien; luacheck/scopecheck/localcount je
  kopierter Datei gruen (hoechstens 77, World.lua), luacheck_pz 0 Treffer + 3 erlaubt.

### 3.3 Gegenprobe der Skript-Regeln (`attrappe/uebernahme_b1e/probe_regeln_b1e.py`, Temp-Kopie, Trockenlauf `--vor-b5a`)
Unveraendert: 0 Fehler. `o:getAnimalType() == B.CUB` im Hud, `"getAnimalType"` als String in Server.lua, `B.CUB ==` in World.lua, unbekanntes
`bodyModel`, unbekannte Rassen-Textur, fremder IG_UI-Schluessel, Testbefehl `NCBear_Grow` im Code -> **je erkannt (8 von 8 wie erwartet)**.

## 4. `staging_dateien.txt` und `mod_info_vorschlag.txt`
- `staging_dateien.txt` (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen NCBearTest 96035c3): **60 Dateien, 9 neu** (die Bilder
  `ui/BanditsNPCBearCub_marker288.png`, `ui/BanditsNPCBearMarker_disc/ring/arrow096..288.png`), **35 ueberschreibt** (14 Kern-Lua, 6 Client-Lua,
  Bench, 7 UI.json, 7 IG_UI.json), **16 gleich** (darunter das alte Junge). Bench weiter "nur Testhilfe".
- `mod_info_vorschlag.txt`: Beschreibung um B1e (ab Tag 15 grosser Baer in klein, waechst bis Tag 100 auf volle Groesse, "bear"-Texte,
  alles gilt fuer beide, wartet waehrend Fuettern/Streicheln/Verstecken/Fahrt, Markierung groesser und einstellbar, auch ohne Bandits), der
  Satz "nur mit Bandits" gestrichen, Testhilfen-Liste 25 (gegen die Bench gezaehlt); ASCII, LF, fuer `mod.info` UND `42/mod.info`.

## 5. Einzelspieler und Mehrspieler
| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Tausch | Hirn-Takt beim einen Programm (20b, 20f, 20j/k) | nur der Server; `removeAnimal(alte OnlineID)`; Sicht mit `bd` + neuer `oid` an alle (20m) |
| Groesse | `B.ApplySize` am Schreiber, nur am passenden Koerper | Server setzt; Client-Probe nur an der Kopie der Art aus `c.bd` (20m) |
| Beschaeftigt-Marke | `start()` setzt, `complete()` loescht (20c) | `serverStart()`/`serverStop()`/`complete()` am Server (b1e_kern 19) |
| Meldungen mit `bd` | `B.ShowNote` direkt (20c, 20g, 20h) | `sendServerCommand(Note)` mit flachem `bd`, nur an den Besitzer (20m) |
| Mitfahren / Call / Laden / Heilung | 20g / 20h / 20i / 20e | Server-Neustart 20m; Heilung im MP b1e_kern 12 |
| Probebefehle | `NCBear_CubGrow/_CubStats` (20b, 20f) | Bench lehnt ab ("singleplayer only", b1e_ober) |
Rote Linien: kein Gegenstand erzeugt/vernichtet (Fuettern unveraendert, 20m: Bs Fisch bleibt); **nie zwei Koerper und nie keiner** (20b, 20f,
20g, 20h, 20i, 20m zaehlen die lebenden Koerper je Eintrag); kein neuer Client-Befehl (kein Kick-Weg); nichts haengt (Abklingzeiten,
Marke gedeckelt 20 s); keine NPC-Crew-Figur beruehrt.

## 6. Befunde des Zusammenbaus (kein Lua geaendert)
- **Z1 (Text, klein):** zwei seltene Meldungen sagen beim grossen Koerper weiter "cub": `Why_Gone` "The cub is gone." (Eintrag fehlt) und
  `Note_Dead` "The bear cub is dead." (nur bei Sandbox-Sperre 0 Tage; mit Sperre kommt "Your bear is dead. ..."). Nicht in Plan 6.8 -> Frage 1.
- **Z2 (aus KERN 9):** der Laerm-Ersatzweg `B.CalmAnswer` rechnet ohne Abstand-Zuschlag (grosser Baer bei 1,35 laeuft auf 2 statt 2,5 Kacheln
  heran) -- im Spiel ansehen.
- **Z3 (aus KERN 8):** `forceStop()` der Zeitaktionen loescht die Beschaeftigt-Marke nicht; der Deckel 20 s faengt das.
- **Z4 (Werkzeug):** `xref_b1e.py` prueft nur das Staging (im Probe-Ordner liest es NPC Crews eigene Dateien mit, 4771 Fremd-"Luecken");
  `xref_b1d.py`/`b1c`/`b1b` sind durch B1e ueberholt. `b1c_kern`/`b1d_kern` weichen von ihrem alten `ergebnis.txt` gewollt ab (neuer
  Fehlerzeilen-Text "fallback body", B1d-Fall 8 ersetzt); Vergleichsstand jetzt `ergebnis_b1e.txt` daneben.
- **Z5 (Stand):** die Test-Mod steht auf Git main **96035c3** (altes Junges zurueck, dazu `NCBearBenchVergleich*`/`ncbearcubalt` aus anderen
  Commits) -- `staging_dateien.txt` vergleicht gegen diesen Stand. Die Vergleichs-Testhilfen nennt `mod.info` nicht (nicht Teil von B1e).

## 7. Offen / ungeprueft (Testpunkte; PLAN_B1E.md 7.4 ist Kevins Testliste)
1. **Alles Laufzeit-Verhalten ungespielt**: Sprung beim Wechsel (F1), Fussgleiten (F6: -28 % nach dem Tausch, +35 % bei 1,35),
   Folgen-/Versteck-Abstaende, Kollision 0,30 (F10), Kuh-Haltung (F4), Blick zum Besitzer (F5), Schild ueber dem Buckel (1,06).
2. `setSizeForced` direkt nach `addToWorld` (mit `minSize` 0,72 unkritisch); ob `isFree(false)` die eigene Kachel eines Tiers als belegt
   meldet (dann Tausch eine Kachel daneben); `faceThisObject` am Tier am MP-Server (nur Optik).
3. MP: Reihenfolge `addAnimal`/`removeAnimal` bei den Clients (ein Bild lang zwei Koerper moeglich, F12); `getAnimalID`/`getObjectListForLua`
   am Server (A3 seit B1a); Sicht evtl. einen Takt mit `oid -1` (der naechste Takt schickt sie neu).
4. Markierung: Pfeil-Ausrichtung der eigenen Bilder (`markerAngleAdd` per `NCBear_CubSet` stellbar), Doppelklick ohne eigenes `onMouseDown`,
   Lesbarkeit der Schrift, Aufloesungswechsel im Spiel; ob die Option "Max. Texturgroesse" auch UI-Bilder > 256 px deckelt (288er Bilder).
5. NPC Crew wird parallel weitergebaut (v3.14.73): Trockenlauf und Probe vor einer echten Uebernahme (erst nach B5a) neu laufen lassen.

## 8. Fragen fuer Kevin (er testet gerade -- nichts davon haelt den Einbau auf; gebaut ist jeweils die Empfehlung; F1-F14 in PLAN_B1E.md 11)
1. **Z1:** Sollen auch "The cub is gone." und "The bear cub is dead." beim grossen Baeren "bear" sagen? Empfehlung: ja, im naechsten Lauf
   (2 Texte x 7 Sprachen, `B.NoteBd` an zwei Stellen).
2. **4K-Groesse:** bei deinem Bildschirm (2054 hoch) ist die Markierung jetzt doppelt so gross (Kreis 192 px, grosse Schrift). Reicht das,
   oder lieber 250 % fest? Empfehlung: Auto lassen, im Spiel unter Optionen ausprobieren.
3. **F1** Wechsel bei 0,72 (wirkt gleich gross wie das Junge, gemessen) statt woertlich 0,75? Empfehlung: 0,72 (so gebaut).
4. **F3** Ab halbstark "Kevin's bear" / "Your bear follows you."? Empfehlung: ja (so gebaut).
5. **F9** Das grosse Modell geht erst mit B5a nach NPC Crew (Uebernahme bis dahin absichtlich rot)? Empfehlung: ja.
6. **F11** Markierung jetzt auch OHNE Bandits? Empfehlung: ja (so gebaut).

## 9. Einbau (NICHT gemacht -- nur wenn Kevin nicht spielt)
`tasklist | grep -i ProjectZomboid` leer -> Zip der Test-Mod nach `Zomboid/backups/NCBearTest/`, die **44 Dateien** mit Zustand neu/ueberschreibt
aus `staging_dateien.txt` in EINEM Zug kopieren (die 16 "gleich" aendern nichts), byte-gleich nachzaehlen (MD5-Spalte), Beschreibung aus
`mod_info_vorschlag.txt` in `mod.info` und `42/mod.info`, zweites Zip. Danach **Spiel neu starten** (neue Tierart `ncbeargrown`, Lua, Bilder),
`bugwatch.py` mitlaufen lassen, Test nach PLAN_B1E.md 7.4 (Debug-"Tier Cheat" AUS, `NCBear_CubLog(true)`). Ein Spielstand von heute (Junges
nach Tag 15 im Junges-Modell) tauscht beim ersten sicheren Takt nach dem Laden (Gesamt 20i).

Statisch geprueft, nicht gespielt.
