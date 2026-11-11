# Gegenpruefung B1e "baer-b1e" (11.11.2026, ~18:15)

Rolle: Gegenpruefer. Nichts davon gebaut, keinem Bericht geglaubt. Gelesen am HEUTIGEN Staging: ganz `server/BanditsNPCBearRide.lua`,
`client/ISUI/BanditsNPCBearMarker.lua`, `client/BanditsNPCBearOptions.lua`, `shared/BanditsNPCBearDefs.lua`, `shared/BanditsNPCBearStats.lua`
(1-370); aus `server/BanditsNPCBearGrow.lua` Tausch, Leben, Wachsen von Hand (196-277, 410-811); aus `server/BanditsNPCBearWorld.lua`
`B.SwapSpot`, `B.SpotNear`, `B.CreateCub`, `B.RemoveCub`, `B.FindAnimal`, `B.ScanAnimals`, `B.MoveTo` (220-319, 455-931); `brainTickBody`,
`resolve`, `countMisses`, `slowRec` (`server/BanditsNPCBearServer.lua`); `B.CalmAnswer`, `B.GuardStep` (`server/BanditsNPCBearGuard.lua`);
`bind`, `B.Restore`, `MARK_FIELDS` (`server/BanditsNPCBearHeal.lua`); `B.Close` (`server/BanditsNPCBearRegistry.lua`); CFG und Helfer
(`shared/BanditsNPCBear.lua` 100-200, 490-530); Hud-Suchlauf und Groessen-Probe; Bench (Kopf, `NCBear_CubHere`, Wachsen, Stats).
Vanilla/Bandits/Jar selbst nachgelesen: `ISPetAnimal.lua:1-35`, `DebugContextMenu.lua:630-640`, `CowDefinitions.lua:175/245/312`,
`DeerDefinitions.lua:92/137/181`, `AnimSets/player/actions/AnimalLureHigh.xml` (vorhanden), `ISUIElement.lua:657/676/1004/1032/1149-1154/1280/1373/1998`,
`ISChat.lua:418/921`, `WinterIsComing.lua:18`, `ISToolTip.lua:78-79/173-174`, `ISKnob.lua:137`, `ISBaseIcon.lua:212`, `ISPlayerData.lua:206`,
`ISFeedAnimalFromHand.lua:15`, `B:client/BanditEventMarkerHandler.lua:1-40`, Jar `dec/IsoGridSquare.java:1161-1171`, dazu selbst gezogen und
dekompiliert (nur im Scratchpad) `zombie/gameStates/IngameState` (NUR JAR, Lesehilfe). Test-Mod: `scripts/nc_bear_tier.txt`,
`shared/NCBearDefs.lua:55-100`, MD5 von `NCBear.glb` 08ec7806 / `NCBear.png` 4cfdb177 / `NCBearCub.glb` 6c3f0a96 (= altes Junges).
**Statisch geprueft, nicht gespielt.** Geschrieben nur diese Datei und `anleitung_b1e_entwurf.md`. Kein git, kein Spielstart, nichts in die
Test-Mod, nach NPC Crew, Vanilla oder Bandits. Probe in einen EIGENEN Ordner im Scratchpad. Kurzformen: `S:` Staging `mod/42/media/lua/`,
`V:` Vanilla `media/lua/`, `B:` Bandits `42.22/media/lua/`.

**Fuer den Integrator:** bei der Pruefung lief das Spiel NICHT (`tasklist` 18:14: kein `ProjectZomboid`, `console.txt` zuletzt 16:30).
Vor dem Kopieren trotzdem neu pruefen (CLAUDE.md 5).

## 1. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test. Kein Blocker.** Nach allem, was statisch pruefbar ist, laedt es ohne rote Fehler (4 Lua-Pruefer
gruen, `luac -p` 25/25, Form 48/48, alle 26 Attrappen-Laeufe gruen und -- wo es eine gespeicherte Ausgabe gibt -- byte-gleich, Trockenlauf und Probe
gruen und byte-gleich zu den gespeicherten Laeufen). Kevins Testweg ist Zeile fuer Zeile durchgegangen (4.3): `NCBear_CubGrow(15)` tauscht im
selben Aufruf (oder nach hoechstens 10 s, wenn der Baer gerade hinterherrennt) auf `ncbeargrown`, genau ein Tier, Eintrag mit Name/Besitzer/
Zaehmung/Werten/Modus bleibt; bis 100 waechst er auf `shown 1.350`; `-100` tauscht zurueck; `NCBear_CubHere(30)` zeigt bei 3840 x 2054 die
Markierung auf Stufe 200 % (Kreis 192 px statt 96), einstellbar in den Optionen. B1a-B1d: alle alten Attrappen gruen (ein B1d-Fall gewollt auf
den neuen Normalfall umgestellt), alte `NCBear*`-Dateien nicht im Staging, 2 `pcall` der alten Markierung weg, kein neuer.

Von 13 Befunden sind **9 am heutigen Code geschlossen** (A2, A3, A4, A6, B1, B2, B3, B4, B5 -- B5 mit berechtigt abgelehntem Rest). **4 bleiben
offen, alle berechtigt als Frage an Kevin** (A1 = B6 Texte "cub", A5 288er Bilder, B7 Klickflaeche). **Kein Befund zu Unrecht abgelehnt.**
**Die Nachbesserung hat nichts kaputt gemacht.** Neu von mir: 3 kleine Restbefunde (C1-C3, Abschnitt 5), keiner haelt den Test auf. Der
wichtigste ist C1: im sehr seltenen Fall "Speichern/Absturz genau im Bild des Wechsels" kann der neue Koerper fehlen, und einen Baeren ohne
Koerper kann man heute nicht rufen (Call haengt am Tier) -- nach 24 Spielstunden waere er weg. Das Fenster besteht seit B1c auch bei
Aussteigen/Call; B1e fuegt einen automatischen Ausloeser hinzu. Vorschlag fuer den naechsten Lauf und Frage 9.

## 2. Je Befund (Zeilen = heutiges Staging)

| ID | Urteil | Beleg im heutigen Code / selbst nachgesehen |
|---|---|---|
| A1 | offen, berechtigt (Frage 1) | `S:client/BanditsNPCBearMenu.lua:408-419` `holdWanted`, `:421-428` `addHold` mit `U.T("UI_BN_Bear_Menu_Hold")` / `..._HoldTip` ohne Big-Fassung; EN `UI.json:71-72` sagt "cub". Nur Text |
| A2 | **geschlossen** (Rest Optik, Frage 4) | `S:server/BanditsNPCBearGrow.lua:535` `if fd > 0 and rec.owner ~= nil and B.IsSP() then`; `:537` `n:faceThisObject(p)` NACH `B.RemoveCub` (`:528`). Vorbild `V:shared/TimedActions/Animals/ISPetAnimal.lua:17` (`self.animal:faceThisObject(self.character)`, Tier -> Spielfigur) nachgelesen. Attrappe `nach_b1e` N3 gruen |
| A3 | **geschlossen** | `S:server/BanditsNPCBearGuard.lua:313-315` `local bd, bsz = B.BodyNow(rec)` / `gap = B.BodyGap(bd, bsz)`; ebenso `:127-129` (neu, B5). `nach_b1e` N6 sucht `BodyGap(B.BodyNow(` im Code: 0 |
| A4 | **geschlossen** | `S:shared/BanditsNPCBearStats.lua:297` "Tag 45: ~0,21"; nachgerechnet mit dem echten Code (lua5.1): Tag 45 `gap 0.2095`, Tag 100 `0.4979` |
| A5 | offen, ungeprueft (Frage 5) -- **kein Blocker** | 288-px-Bilder `S:../ui/BanditsNPCBearMarker_arrow288.png`, `_disc`, `_ring`, `Cub_marker288` (Groessen selbst aus dem PNG-Kopf gelesen). Der Deckel 256 gilt laut Rucksack-Forschung fuer Texturen mit Flag 128 (`rucksack/forschung/REZEPT_ENGINE.md:572`); welche Flags `getTexture("media/ui/...")` setzt, ist nicht belegt. Wirkung hoechstens: Kreis/Ring/Symbol (`drawTextureScaled`, Groesse gesetzt) nur unschaerfer; der Pfeil (`DrawTextureAngle`, Bildgroesse) nur bei 300 %. Kevins Auto (2054 px) nimmt `arrow192` (< 256). Hinweis: Vanilla hat 442 UI-Bilder ueber 256 px (z. B. `media/ui/survival_guide_spiffo/*.png` 350 px, benutzt per `<IMAGECENTRE:...>`) -- kein Beweis |
| A6 | **geschlossen** | Kommentar `S:server/BanditsNPCBearGrow.lua:512-513`; `V:client/DebugUIs/DebugContextMenu.lua:636` `square:getX(), square:getY(), square:getZ()` nachgelesen |
| B1 | **geschlossen** (Rest: ein stiller Klick) | `S:server/BanditsNPCBearRide.lua:95` `s.placedAt = getTimestampMs()` in `B.PlaceCub` (gilt fuer Tausch, Aussteigen, Call); `:342-348` `B.HandleCall`: Objekt da, juenger als `callFreshMs` (2000, `S:shared/BanditsNPCBear.lua`), `B.FindAnimal(rec) == nil` -> nur `B.Log`, return -- VOR der Drossel `:349`. Ohne Objekt (eingestiegen) greift die Sperre nicht. Beleg, dass der Fehler weg ist: `attrappe/pruef_b1e/run.lua` (Pruefer Bs Fehler-Nachweis) jetzt 20/5 -- genau die 5 P1b-"BEFUND"-Pruefungen schlagen fehl ("1 lebende Koerper ..., addAnimal 1"); `run_nach.lua` 25/0 |
| B2 | **geschlossen** (Frage 2) | `S:server/BanditsNPCBearGrow.lua:461-464` "move" nur bei `s.walk == false` (Rennbefehl, `fleeTo` `S:server/BanditsNPCBearWorld.lua:888`, `s.walk` `:903`) UND `ownUntil` laeuft (`pending`, `:424-429`) UND `within(s.swapWantAt, ms, 10000)`; `swapWantAt` setzt `B.GrowLive` beim ersten Takt mit want ~= have (`:566`), leert bei want == have (`:576`) und nach dem Tausch (`:533`). Hoechstwartezeit ab dem ersten Wunsch, nicht je Strecke -> nie endlos; Uhr rueckwaerts -> keine Sperre. `BodySwapReady` schreibt weiter nichts (Bench fragt dort) |
| B3 | **geschlossen** | Kommentar `S:shared/BanditsNPCBear.lua:124` (CFG "Clip-Weg / Dauer x MotionScale 1,6"), `PLAN_B1E.md:179/185/281`. Nachgerechnet: 0,3784 / 0,9 x 1,6 = 0,673; 1,0578 / 0,533 x 1,6 = 3,175; Gegenprobe Junges 0,2940 / 0,9 x 1,6 = 0,523 = gespielter `walkSpeed` 0,52 -- die Formel ohne x 1,5 stimmt |
| B4 | **geschlossen** (Frage 3) | `S:shared/BanditsNPCBearDefs.lua:189` `d.feedByHandAnim = "AnimalLureHigh"` (nur Kopie der grossen Art; Junges `:111` bleibt "AnimalLureLow"). `V:shared/Definitions/animal/CowDefinitions.lua:245` (cow) und `DeerDefinitions.lua:137` (doe), `:181` (buck = doe) nachgelesen, Knoten-Datei `AnimSets/player/actions/AnimalLureHigh.xml` vorhanden. Aktion spielt `a:getFeedByHandAnim()` (`S:shared/TimedActions/BanditsNPCBearFeedAction.lua:55`, Vorbild `V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:15`) |
| B5 | **geschlossen** fuer den Laerm-Weg, Rest **berechtigt abgelehnt** | `S:server/BanditsNPCBearGuard.lua:126-134` `followStart + gap` / `followGap + gap` wie `B.FollowDecide`. Ablehnung beim Heranlocken (`S:shared/BanditsNPCBearRules.lua:303-305`, `comeFed` 2) stimmt: Fuettern verlangt `here:DistTo(there) < reach` (`S:server/BanditsNPCBearServer.lua:163`, `reach = 3` `S:shared/BanditsNPCBear.lua:67`), und `DistTo(IsoGridSquare)` ist der Manhattan-Abstand der Kachelmitten (NUR JAR `dec/IsoGridSquare.java:1165-1166`, selbst gelesen). Mit +0,5 fiele "zu weit" oefter |
| B6 | offen, berechtigt (= A1, Frage 1) | `S:server/BanditsNPCBearRegistry.lua:492` `Note_Dead` (nur bei Sperrfrist 0), `:495` (nicht gezaehmt), `:500` `Why_Gone`; EN `UI.json:86` "The bear cub is dead.", `:141` "The cub is gone." Nur Text, seltene Faelle |
| B7 | offen, berechtigt (Frage 6) -- Zeitangabe korrigiert (C3) | `S:client/ISUI/BanditsNPCBearMarker.lua:410-413` Element 45 x f, `V:client/ISUI/ISUIElement.lua:1998` `o.wantMouseEvents = true`, `:1004` `setConsumeMouseEvents`. Doppelklick `Marker.lua:184-191` braucht es |

## 3. Selbst laufen lassen (Zahlen, 11.11.2026 ~18:00-18:15)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (25 Lua) | 25 checked, 0 failed |
| `scopecheck.py` | 25 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 49 (`Hud.lua` Dateiebene), 39 (`Server.lua:921`, Bench `:391`, `Hud.lua:434`); insgesamt hoechstens 77 (`World.lua:664`) -- weit unter 180/200 |
| `luacheck_pz.py` | 18 x W113, alle erwartet: 3 Aktionsklassen (`Menu.lua:89/100/110`), 15 in der Bench (`NCBearBenchCub.lua:977-992`) |
| `luac5.1 -p` | 25 von 25 ohne Fehler |
| Dateiform (eigenes Skript, 48 .lua/.json/.txt) | 0 Probleme: kein BOM, kein CR, LF am Ende, keine Leerzeichen am Zeilenende, Lua/.txt ASCII, JSON Round-Trip + sortiert |
| `pcall(` | Staging 4 (Map, Guard, Server x2); Test-Mod 6 -- die 2 aus der alten Markierung sind weg, kein neuer |
| neue Methoden gegen die Test-Mod (eigenes Skript) | nur UI: `DrawTextureAngle`, `drawTextureScaled`, `getScreenWidth/Height`, `setWidth/Height/Y`, `setVisible`, `math.atan2/deg`, Rueckrufe `render`/`onMouseDoubleClick`; Fundstellen stichprobenweise nachgelesen (Kopfzeile oben) |
| `kern` / `b1b_kern` / `b1c_kern` / `b1d_kern` / `b1e_kern` | 136/0, 204/0, 192/0, 162/0, 153/0 -- byte-gleich `ergebnis.txt` bzw. `ergebnis_b1e.txt` (b1d aus seinem Ordner gerufen; sonst weicht nur der Pfad in 2 Fehlerzeilen ab). b1d 163 -> 162: Fall 8 gewollt auf `bodySwap = true` umgestellt (Diff `ergebnis.txt` / `ergebnis_b1e.txt` gelesen) |
| `gesamt/run.lua` | **1672 / 0**, byte-gleich `ergebnis.txt`; gegen MEINE Probe (`probe_gp/NPCCrew/42/media/lua/`) 1672 / 0, byte-gleich `ergebnis_probe.txt` |
| `nach_b1e/run.lua` | 31 / 0, byte-gleich `ergebnis.txt` (Gegenlauf gegen den Stand VOR der Nachbesserung nicht wiederholt: die Kopie liegt nicht vor) |
| `pruef_b/run.lua`, `pruef_b1b/run_nach.lua`, `pruef_b1c/run.lua`, `pruef_b1d/run.lua` | byte-gleich `ergebnis_b1b_nach.txt`, `ergebnis_b1c.txt`, `ergebnis_nach.txt`, `ergebnis_nach.txt` (pruef_b1d 10/0, 3 bekannte Befunde) |
| `pruef_b1e/run.lua` / `run_nach.lua` | 20 / 5 (nur P1b, der Fehler-Nachweis von B1, siehe 2) / **25 / 0**, byte-gleich `ergebnis_nach.txt`; P3: 7 Tausche in 3000 Takten, laengste Wartezeit 2 Takte |
| `ober`, `b1b_ober`, `b1c_ober`, `b1d_ober`, `b1e_ober` (Kern-Attrappe / echter Kern) | 116+117, 144+134, 155+142, 174+176, **218+218**, je 0 Fehler (b1c_ober seit B1e kleiner: Markierungs-Teil gewollt nach b1e_ober verlegt, Kommentare `b1c_ober/run.lua:174/412/623`) |
| `texte_pruefen.py` / `_b1b` / `_b1c` / `_b1d` / `_b1e --tmp <scratch>` | FEHLER gesamt 0 / 0 / 0 / 0 / 0; `texte_b1e.py --basis` == `texte_b1d.py`, Sandbox unveraendert gegen B1d |
| `bilder_pruefen_b1e.py --tmp <scratch>` | `marker_bilder.py` -> 9 Dateien, abweichend vom Staging keine; FEHLER 0 |
| `belege.py` / `_b1b` / `_b1c` / `_b1d` / `_b1e` | abweichend 0 von 112 / 51 / 89 / 23 / 53 |
| `gesamt/xref_b1e.py` | 0 Luecken, 3 Hinweise (bekannte Rueckfallwerte Rules.lua), byte-gleich `xref_b1e.txt` |
| `gesamt/gegenprobe_b1e.py` / `uebernahme_b1e/probe_regeln_b1e.py` | 30 von 30 erkannt / 8 von 8 wie erwartet, beide byte-gleich |
| `uebernahme_force/probe_force.py` / `uebernahme_b1c/probe_regeln.py` | 23 Faelle, 0 Fehler / 34 Faelle, 0 Fehler |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen**, byte-gleich `trockenlauf_b1e_nach_vor_b5a.txt` |
| Trockenlauf ohne `--vor-b5a` | 26 Fehler = 24 Altlasten (ALT_EXPECTED) + 2 ALT_DEFS (`ncbeargrown` -> `NCBear_Body` / Textur `NCBear`), byte-gleich `trockenlauf_b1e_nach.txt` -- gewollt rot bis B5a (Naht 10.3, Frage F9) |
| **Probe** `--probe <scratch>/probe_gp --staging ... --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen (PROBE)**, 60 Datei(en) geschrieben, je kopierter Lua luacheck/scopecheck/localcount ok (hoechstens 77), `luacheck_pz` 0 Treffer + 3 erlaubt; bis auf die Ordnernamen gleich `probe_b1e_nach_ausgabe.txt`; keine `*bench*`-Datei in der Probe-Kopie (find: 0) |

### 3.1 `staging_dateien.txt` gegen Platte und Test-Mod (eigenes Skript, MD5 + Bytes)
- Liste 60, Platte 60, nur Platte 0, nur Liste 0, **MD5/Bytes 0 Abweichungen**, Einordnung gegen `NCBearTest` 0 Abweichungen:
  **9 neu, 35 ueberschreibt, 16 gleich** (wie die Liste).
- **Ueberschrieben wuerden genau:** 20 x `BanditsNPCBear*.lua` (client 6 inkl. `ISUI/`, server 8, shared 4, `TimedActions/` 2), die eigene
  Testhilfe `client/NCBearBenchCub.lua` und 14 Texte (`Translate/<7 Sprachen>/UI.json` + `IG_UI.json`). Alles gewollt.
- **Alte `NCBear*`-Dateien: keine.** Die einzigen `NCBear*`-Namen ausser der Bench sind `models_X/Skinned/NCBearCub.glb` und
  `textures/Body/NCBearCub.png` -- beide "gleich" (MD5 6c3f0a96 / 2ee25f24 = altes Junges, schon in der Test-Mod), Kopieren aendert nichts.
  `NCBear.glb`, `NCBear.png`, `nc_bear_tier.txt`, `NCBearDefs.lua`, `NCBearFight.lua` usw. stehen nicht in der Liste.
- Neu: 9 Bilder `42/media/ui/BanditsNPCBearMarker_*` (6 Pfeile 96-288 px, disc, ring 288) und `BanditsNPCBearCub_marker288.png`.
- Ausserhalb des Stagings: mod.info-Beschreibung (`mod_info_vorschlag.txt`, LF, ASCII).

## 4. Eigene Stichproben

### 4.1 Tausch waehrend Mitfahren (Zeile fuer Zeile)
1. Einsteigen: `liveRec` (Schritt 5, `S:server/BanditsNPCBearServer.lua:979`) -> `B.FollowStep` -> `B.RideBoard` (`Ride.lua:122-145`): Pflicht
   ist nur die Junges-Definition (`:124`), `s.obj = nil` (`:130`), `rec.ride` (`:133`), `gen + 1`, Commit, `B.RemoveCub(a)` (`:139`; beide Arten,
   `World.lua:519`). Ein Tier weniger, kein Koerper mehr.
2. Im selben Takt danach Schritt 7: nur `rec.ride == nil and s.obj == e.a` (`Server.lua:1022`) -> uebersprungen. Zweiter Riegel:
   `B.BodySwapReady` -> `false, "ride"` (`Grow.lua:446`). Kein Tausch waehrend der Fahrt.
3. Waehrend der Fahrt waechst `g` nur ueber `B.GrowSlow` (Spielzeit, Besitzer online); ueber Tag 15 kommt "half-grown" als Meldung, der Koerper
   bleibt weg.
4. Aussteigen: `B.RideStep` (Schritt 1, `Server.lua:931`) -> `B.PlaceCub(rec, ..., "ride")` OHNE Koerper-Vorgabe (`Ride.lua:229`) ->
   `want = B.BodyOf(rec)` (`:77`) = "big", Definition da -> `B.CreateCub(..., "big")` (`:87`); fehlte sie: Junges-Koerper + Fehlerzeile (`:82-86`).
   `rec.body = want` vor Commit/Spiegel (`:92-104`), `B.GrowBody` setzt 0,72 + Leben (`Grow.lua:629-637`). Genau ein neues Tier.
5. Im selben Takt: `resolve` findet es noch nicht (nicht in der Welt) -> ein harmloser Fehlversuch (3 noetig, B1c-Verhalten); Schritt 7 laeuft
   nicht (`B.FindAnimal` nil -> nicht in `loaded`). Naechster Takt: have == want -> kein zweiter Tausch.
6. "Call to me" im selben Bild wie dieses Aussteigen: jetzt durch B1 abgefangen (`Ride.lua:342-348`). Waehrend der Fahrt lehnt Call ohnehin ab
   (`:317-320`, Why_Riding mit Big-Text).
Ergebnis: kein Verlust, kein Doppel, kein Hin und Her. Statisch geprueft.

### 4.2 Speichern genau im Tausch
- `B.BodySwap` ist EIN Lua-Aufruf (`Grow.lua:515-545`): Kachel, Schaden verbuchen, `B.PlaceCub` (neu: gen + 1, Commit, Spiegel mit `body`
  (`Heal.lua:42-47` `MARK_FIELDS` + "body"), Groesse, Leben), DANN `B.RemoveCub(alt)`. Zwischen zwei Lua-Zeilen speichert die Welt nicht.
- Offen bleibt das Engine-Fenster: `addToWorld` haengt das neue Tier erst beim naechsten Update in seine Kachel (`World.lua:500-505`). Was dann
  aus dem Code folgt (Plan 4.3 nachgeprueft):
  (a) Zelle mit neuem Koerper gespeichert -> Suchlauf bindet ihn ueber den Spiegel (gen = rec.gen), `rec.body = "big"` (`Heal.lua:93-125`), kein Tausch.
  (b) Zelle ohne neuen Koerper -> Eintrag gen N+1 ohne Tier -> nach 3 Suchlaeufen "missing" + Meldung (`Server.lua` `countMisses`). Plan 4.3
      sagt "Call to me erzeugt B.BodyOf" -- aber Call haengt nur am Tier-Menue, ein Baer ohne Koerper ist nicht anklickbar (C1). Dann schliesst
      `slowRec` den Eintrag nach `missingH` 24 Spielstunden ("lost", `Server.lua:487-490`).
  (c) Register alt (gen N, cub), Zelle neu (gross gen N+1): `bind` uebernimmt gen und `body` vom Tier.
  (d) alter Koerper doch noch in der Zelle (gen N < rec.gen): "stale" -> unbeobachtet entfernt (`dropCopy`, `World.lua:634-641`), nie gebunden.
- In keinem Fall ein zweiter GEBUNDENER Koerper. Fall (b) ist dasselbe Fenster wie seit B1c bei Aussteigen/Call und kann -- ohne Weg, einen
  koerperlosen Baeren zu rufen -- nach 24 Spielstunden zum Verlust fuehren. Restbefund C1.

### 4.3 Kevins Testweg (Bench, SP)
- `NCBear_CubHere(30)` (`NCBearBenchCub.lua:120-152`) geht ueber `B.AppearFor` -> lehnt ab, solange Kevin schon einen Baeren hat -> in der
  Anleitung ZUERST die Markierung, dann zaehmen.
- Markierung: `Marker.lua:108-123` bei H = 2054: 2054/1080 = 1,90 -> naechste Stufe 2,0 (Abstand 0,10 gegen 0,40 zu 1,5) -> Kreis/Symbol 192 px,
  Pfeil `arrow192`, Schrift Large, Klickflaeche 90 px; Optionen `S:client/BanditsNPCBearOptions.lua:83-90` (Auto + 6 Stufen), Wechsel wirkt beim
  naechsten 400-ms-Takt (`Marker.lua:368-372`).
- `NCBear_CubGrow(15)` ab Tag 0 (`:865-879`): g = 0,15 -> s = 0,75 -> `BodyWant` "big" (`Stats.lua:240`); `B.GrowSetG` leert Abklingzeiten
  (`Grow.lua:789`), meldet "half-grown"; `B.BrainTick(true)` -> Schritt 7 -> Tausch, ausser "move" (rennt gerade, hoechstens 10 s), "calm",
  "guard", "busy". Die Zeile meldet "body big (swapped)" auch im selben Bild (`bodyNow` faellt auf `rec.body` zurueck, `:831-838`).
- Werte mit dem echten Code nachgerechnet (lua5.1, Sandbox 100): Tag 15 `shown 0.720`, Leben 150; Tag 45 `0.982`, 254; Tag 100 `1.350`, 400 /
  Ausdauer 160 / Traglast 100 / Schaden 1,0. Tag 14,5 mit grossem Koerper bleibt gross, Tag 13 (s 0,697) will zurueck (Schwelle 0,70).
- `NCBear_CubGrow(-100)` -> g 0 -> "cub" -> Tausch zurueck auf 0,35 (Abklingzeit von Hand geleert).

## 5. Restbefunde (neu, alle minor, keiner haelt den Test auf)

- **C1 (ungeprueft, Fenster ein Bild; wichtigster Rest):** Speichern/Absturz genau zwischen `addToWorld` und dem naechsten Engine-Update (4.2 b)
  kann den neuen Koerper verlieren. Dann wird der Eintrag nach 3 Suchlaeufen "missing" -- und **"Call to me" gibt es fuer einen Baeren OHNE
  Koerper nicht**: der Punkt haengt nur am Tier-Menue (`S:client/BanditsNPCBearMenu.lua:284-313` `cubMenu`, `addCall` `:265`), ein Ruf ohne anklickbaren
  Koerper ist auf das Baeren-Fenster verschoben (`S:server/BanditsNPCBearRegistry.lua:146-147`, B1c Frage F4). Nach `missingH` 24 Spielstunden
  (Besitzer online) schliesst `slowRec` den Eintrag ("lost", `S:server/BanditsNPCBearServer.lua:487-490`) = verloren. Plan 4.3 Zeile 1
  ("Call to me erzeugt B.BodyOf") setzt diesen Weg voraus. Das Fenster gibt es seit B1c auch bei Aussteigen und Call; B1e bringt einen
  automatischen Ausloeser dazu (einmal je Stufenwechsel). Wahrscheinlichkeit sehr klein (der Wechsel muss im letzten Spielbild vor dem
  Speichern/Absturz liegen); Nebenfrage, ungeprueft: ob der Hirn-Takt (OnTick, Echtzeit) bei offenem Esc-Menue weiterlaeuft (NUR JAR
  `IngameState.updateInternal`: das Feld `paused` setzt nur der Server, `:1919`; wie das SP-Pausemenue den Zustand haelt, nicht verfolgt).
  Vorschlag naechster Lauf (Kevins Wort): ein vermisster ZAHMER Eintrag, dessen Gegend geladen ist und der seit dem letzten `B.PlaceCub` nie
  gefunden wurde, bekommt nach den Fehlversuchen von selbst einen neuen Koerper an `rec.x/y` (derselbe Weg wie Call) -- oder "Call to me" auch
  ueber Karte/Schild. Kein Blocker fuer den SP-Test.
- **C2 (Optik, schon Frage F5):** Auftrag 1 nennt "Lage/Richtung" als bleibend; gebaut ist: Kachelmitte der alten Kachel (oder daneben), im SP
  schaut der neue Koerper zum Besitzer, im MP Richtung von `addAnimal`. Die alte Blickrichtung wird nicht uebernommen (kein Beleg fuer ein Setzen).
- **C3 (Korrektur zu B7/Frage 6):** Die Klickflaeche der Markierung gilt nicht nur ~60 s: `target()` zeigt sie ohne Frist, solange das wilde Junge
  "new" ist, plus 60 s ab dem ersten "shy" (`Marker.lua:311-320`). Wie in B1c mit Bandits' Element. Frage 6 sollte "bis du das Junge gefunden hast"
  sagen.
- Kleinigkeit: `mod_info_vorschlag.txt` nennt "rennt hinter dir her" (B2) nicht unter den Warte-Gruenden des Wechsels.

## 6. Fragen fuer Kevin (unveraendert aus Plan 11 und Nachbesserung 4; nichts davon haelt den Test auf)
1. Sollen auch "The cub is gone.", "The bear cub is dead." und "Hold out food for the cub" beim grossen Baeren "bear" sagen? (Empfehlung: ja, naechster Lauf.)
2. Der Wechsel wartet, solange der Baer hinter dir herrennt -- hoechstens 10 Sekunden. Ok?
3. Beim Fuettern des grossen Baeren haelt die Figur das Futter hoch (wie Kuh/Hirsch). Bitte ansehen.
4. Im Mehrspieler dreht sich der neue Baer nach dem Wechsel nicht zu dir. Ok?
5. Markierung auf 300 %: ist der Pfeil gleich gross wie der Kreis?
6. Stoert es, dass oben in der Mitte ein Klick nicht in die Welt geht, solange die Markierung da ist (bis du das Junge gefunden hast, plus ~1 Minute)?
7. Groesse beim Wechsel 0,72 (wirkt gleich gross) statt woertlich 0,75 -- ok? Fussgleiten (F6), Kollision (F10) im Spiel ansehen.
8. Die Markierung kommt jetzt auch ohne Bandits (F11). Ok?
9. (C1) Geht ein Baer ganz selten ohne Koerper verloren (Speichern/Absturz genau im Wechsel-, Aussteige- oder Call-Bild), gibt es heute keinen
   Knopf, ihn zu rufen; nach 24 Spielstunden ist er weg. Soll er dann von selbst an seiner letzten Stelle wieder erscheinen? (Empfehlung: ja.)

## 7. Ungeprueft (Laufzeit)
Alles Laufzeit-Verhalten: ob `setSizeForced` direkt nach `addToWorld` wirkt (mit `minSize` 0,72 unkritisch), ob die eigene Kachel eines Tiers
`isFree(false)` besteht (sonst Kachel daneben), Fussgleiten und Abstaende des grossen Koerpers, Fuetter-/Streichel-Haltung, Schild-Hoehe,
Pfeil-Ausrichtung des eigenen Bildes, Doppelklick und Klickflaeche, 288er Bilder bei 300 %, das Ein-Bild-Fenster von C1, alles im Mehrspieler.
Nach dem Einbau (erst wenn Kevins Spiel zu ist) muss das Spiel neu gestartet werden. **Statisch geprueft, nicht gespielt.**
