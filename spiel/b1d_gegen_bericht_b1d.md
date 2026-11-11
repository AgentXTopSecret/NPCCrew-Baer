# Gegenpruefung B1d "baer-b1d" (11.11.2026, ~10:50)

Rolle: Gegenpruefer. Nichts davon gebaut, keinem Bericht geglaubt. Gelesen am HEUTIGEN Staging: ganz `server/BanditsNPCBearGrow.lua`,
`shared/BanditsNPCBearStats.lua`; als Diff gegen die Test-Mod (Stand 11.11. 08:12, B1c) `server/BanditsNPCBearServer.lua`, `...Heal.lua`,
`...Registry.lua`, `...Ride.lua`, `shared/BanditsNPCBear.lua`, `...Defs.lua`, `client/BanditsNPCBearClient.lua`, `...Options.lua`,
`client/ISUI/BanditsNPCBearHud.lua`, `client/NCBearBenchCub.lua`, `sandbox-options.txt`, alle 14 geaenderten JSON; dazu die Umgebung
(Langsam- und Hirn-Takt, `B.PlaceCub` und seine drei Aufrufer, `B.FeedComplete`, `B.FindAnimal`, `B.Commit`, `B.Tell`, `B.T`, `U.Opt`).
Vanilla-/Bandits-/Jar-Stellen selbst nachgelesen (`ButcheringUtil.lua:242/566-571/586/674`, `ISAnimalUI.lua:15/31`,
`ISAnimalContextMenu.lua:545`, `ISKillAnimal.lua:58`, `STrapGlobalObject.lua:238`, `ISWorldObjectContextMenu.lua:1435`,
`MainOptions.lua:2809-2813/2910-2933`, `ModOptions.lua:121-156`, `B:server/BanditServerSync.lua:10-12`, `B:media/sandbox-options.txt:11`
(`type = double`), Jar `dec/AnimalData.java:218-234/1353-1356/1539-1546/1717-1751`, `dec/IsoAnimal.java:1156-1163/1583-1586/1862-1863/1945-1946`).
Alle Pruefer, Attrappen, Trockenlaeufe selbst laufen lassen, die Probe in einen EIGENEN Ordner
(`C:/Users/Kevin/AppData/Local/Temp/claude/086a7114045651dc/d5933cc7-7f9d-46b2-a3a8-0929595b654b/scratchpad/probe_gp`).
**Statisch geprueft, nicht gespielt.** Geschrieben nur diese Datei und `anleitung_b1d_entwurf.md`. Kein git, kein Spielstart, nichts in die
Test-Mod, nach NPC Crew, Vanilla oder Bandits. Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`, `B:` Bandits
`42.22/media/lua/`, `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`.

**Achtung fuer den Integrator:** bei der Pruefung LIEF das Spiel (`tasklist` 10:47: `ProjectZomboid64.exe`, `console.txt` 10:47). Geladen
laut zweiter `loading`-Liste (`console.txt:4884` ff.): Bandits2, BanditsCreator, NPCCrew u. a. -- **NCBearTest nicht** (kein einziges
`NCBear` im Log). Nach CLAUDE.md 5 waere der Einbau damit erlaubt; vor dem Kopieren trotzdem neu pruefen.

## 1. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test. Kein Blocker.** Laedt nach allem, was statisch pruefbar ist, ohne rote Fehler (4 Lua-Pruefer
gruen, alle 17 Attrappen-Laeufe gruen und byte-gleich zu den gespeicherten Ausgaben, Probe-Uebernahme gruen). Der Test-Weg ist Zeile fuer Zeile
durchgegangen (4.1): `NCBear_CubGrow` laesst das gezaehmte Junge sichtbar bis 0,75 wachsen und dort stehen, die Werte steigen weiter, Leben- und
Alter-Zeile stehen mit den Vorgaben ueber dem Jungen, Ausdauer nach Umschalten in den Optionen. B1a-B1c: alle alten Attrappen byte-gleich,
alle B1c-Texte unveraendert (je Sprache nur 24 + 10 neue Schluessel, 0 geaendert, 0 weg), alte `NCBear*`-Dateien nicht im Staging.

Von 16 Befunden sind **5 am heutigen Code geschlossen** (B1, B2 fuer die beiden genannten Stellen, B3, B4, B5). **11 bleiben offen, alle
berechtigt** -- als Frage an Kevin oder ausdruecklich aufgeschoben (A1-A8, B6-Rest, B7, B8). **Kein Befund zu Unrecht abgelehnt** (abgelehnt
wurde keiner; bei A5 halte ich das Verlegen vor einer echten Uebernahme fuer Pflicht, nicht nur Empfehlung). **Die Nachbesserung hat nichts
kaputt gemacht.** Neu von mir: 1 Restbefund mit Gewicht nur fuer den Mehrspieler (C1, B2-Rest in `B.PlaceCub`) und 4 Kleinigkeiten (Abschnitt 5).

## 2. Je Befund (Zeilen = heutiges Staging)

| ID | Urteil | Beleg im heutigen Code / selbst nachgesehen |
|---|---|---|
| A1 | offen, berechtigt als Frage 1 | `S:server/BanditsNPCBearGrow.lua:461` heilt `B.HealRate(false)/100 x dt` (Vorgabe 1 %/h), `:236-238` nimmt die Engine-Heilung zurueck. Widerspruch belegt: `ENT:279` ("Heilen erst nach Kevins B1c-Test") gegen Laufauftrag Punkt 5 ("nur wach anwenden, wenn ein belegter Leben-Weg existiert"). Frage 1 nennt ihn jetzt samt Folge "0 = gar keine Heilung". Die Sandbox-Tooltips sagen das NICHT (EN `Sandbox_BanditsNPC_BearHealAwake_tooltip`) -- Kleinigkeit, siehe C4 |
| A2 | offen, berechtigt (Kevins Wort `ENT:285` "A3 entscheidet der MP-Test") | `Grow.lua:216` `a:getHealth()`; Vanilla am Tier nur `V:client/ISUI/Animal/ISAnimalUI.lua:15` (selbst gegrept: einziger Treffer). Am Server dieselbe geerbte Methode am Zombie `B:server/BanditServerSync.lua:11`; `getHealth` ist laut Jar `dec_b1b/IsoGameCharacter.java:3181` ein schlichter Getter ohne Server-Zweig -- ein echter Wurf ist sehr unwahrscheinlich. Rest siehe C1 |
| A3 | offen, berechtigt als Frage 2 | Kommentar jetzt `S:shared/BanditsNPCBearStats.lua:330-341` ("gespielt also sehr wahrscheinlich, belegt nicht"); nachgesehen: `NCBearTest client/NCBearSize.lua:27` setzt `setSizeForced(x)` am lebenden `bear`, `baer/spiel/anleitung_lebend.md:6` nennt es Kevin, `baer/begleiter/PLAN.md:297` die Frage, `ENT:10` Kevins 1,35. `setHealth` mit 0 < x <= 1: Vanilla nur 0 (`ISAnimalContextMenu.lua:545`, `ClientCommands.lua:932/950`, `ISKillAnimal.lua:58`), gleicher Typ Zahl; Jar `dec/IsoAnimal.java:1156-1163` ohne Klemme. Der alte Satz "ob gespielt: ungeprueft" steht noch in `PLAN_B1D.md:620` (nur Plan) |
| A4 | offen, berechtigt als Frage 3 | `Grow.lua:230-235` uebernimmt jeden Verlust in `rec.hp`; `ENT:45` "nicht Spieler, nicht Autos". Ohne B5a gibt es keinen Weg, die Quelle zu unterscheiden -- aufschieben ist richtig |
| A5 | offen, aufgeschoben (Frage 4) -- **vor `--echt` Pflicht** | `Grow.lua:307` `B.SkillSet`, `:623` `B.GrowSetG`, `:642` `B.GrowSetHp`: in meiner Probe-Kopie (`probe_gp/NPCCrew`) nur die Definitionen, kein Aufrufer (selbst gegrept); kein Client-Befehl fuehrt dorthin (`Server.lua`-Handler gegrept). Kein Menue, kein Befehl -- also kein Verstoss gegen die Cheat-Regel, aber "Testwege nur in Bench-Dateien" (CLAUDE.md 0.2) ist erst mit dem Verlegen erfuellt. Fuer den SP-Test egal |
| A6 | offen, berechtigt als Frage 5 | `V:client/OptionScreens/MainOptions.lua:2910-2911` baut die Auswahl ohne Tooltip, die Tickbox `:2810-2813` mit -- bestaetigt. `S:client/BanditsNPCBearOptions.lua:65-73` legt die Schluessel trotzdem an |
| A7 | offen, berechtigt als Frage 6 | `V:client/PZAPI/ModOptions.lua:121-156` gelesen: reines Lua (Tabellen, `getText` beim `addItem` :132), `isEnabled = {}` ist wahr (nicht gesperrt). Kein Aufrufer in V/B -- gleiche Regel-Frage wie B1c A3 (noch unbeantwortet, `ENT:273-287` nennt sie nicht) |
| A8 | offen, berechtigt (Merker) | (1) `NAEHTE.md:3` jetzt `BanditsNPC.Opt` `:6105` -- selbst nachgesehen: `NPCCrew/42/media/lua/shared/BanditsNPC.lua:6105`; NC-Kommentar `:1360` wie im Trockenlauf. (2)-(5) unveraendert, ehrlich in der Nachbesserung genannt |
| B1 | **geschlossen** (Rest ehrlich, Frage 7) | `S:server/BanditsNPCBearHeal.lua:236` `born = num(mark.born, 0, now) or now, tamedAt = num(mark.tamedAt, 0, now)`; `:347` ebenso in `B.TakeNewerMark`; `num` klemmt (`:159-165`). Ein NaN aus dem Spiegel faellt in `Grow.lua:556` (`num` filtert NaN) auf "ohne tamedAt" = Deckel 0,10 -- sichere Seite. Rest: gefaelschtes `tamedAt = 0` bekommt "Zeit seit Weltbeginn + 0,10" (Kommentar `Grow.lua:531-534`, F18) |
| B2 | **geschlossen fuer die zwei genannten Stellen** | `S:server/BanditsNPCBearServer.lua:587-592` eigene `GrowSlow`-Schleife nach `slowRec`/`forestRolls`/`baitNights`, vor `FlushViews`; `:1017-1026` `GrowLive` als letzter Schritt 7 mit `reg.cubs[id] == rec`, `st == "tame"`, `ride == nil`, `s.obj == e.a` (`s.obj` ist genau das Objekt, das `B.FindAnimal` liefert, `World.lua:508-517`). Attrappe `b1d_kern` 20: ein Wurf in `getHealth` steht nur noch als "slow tick"/"brain tick"-Zeile, B1a-B1c laufen. **Rest (neu, C1):** `B.GrowBody` -> `B.BodyHp` -> `getHealth` liegt weiter MITTEN in `B.PlaceCub` (`Ride.lua:86`) |
| B3 | **geschlossen** (P1c ehrlich offen) | `Grow.lua:230` `h < hpB - hpLossEps` (0,0001, `shared/BanditsNPCBear.lua:122`); Setzen weiter erst ab `hpEps` (`:245`). Gleitkomma-Rest float/double liegt weit unter 0,0001 -- kein Schein-Schaden. P1c (Treffer + Engine-Heilung im selben 10-Minuten-Fenster) im Kommentar `:231-232` |
| B4 | **geschlossen** (Pausen-Erholung ehrlich) | `Grow.lua:358` Sprung erst ueber `conStepMax` UND `conStepMul x runSpeed x dts` (`runSpeed = 2.47`, `shared/BanditsNPCBear.lua:91`). Erholung in Echtzeit auch in der Pause: Kommentar `:345`, nur Anzeige |
| B5 | **geschlossen** | `Grow.lua:77-80` `statsOk()`; nachgezaehlt: alle Wege, die Stats-Funktionen brauchen (`GrowFix`, `SkillAdd`, `SkillSet`, `OnFish`, `GrowLive`, `GrowSlow`, `GrowBody`, `GrowFeed`, `GrowFromMark`, `GrowView`, `GrowSetG`, `GrowSetHp`), pruefen es; `BodyHp` braucht nur `B.CFG`. Ausserhalb: Hud-Probe nur mit `B.ApplySize ~= nil` (Hud :443), Bench `growReady()` |
| B6 | offen (Rest), teils gebaut | `S:client/ISUI/BanditsNPCBearHud.lua:659-683`: `split and not isClient()` -> SP wie bisher; MP-Client baut die Liste (Probe), zeichnet nicht. Rest (Sicht-Reichweite 60, ausgeblendete Oberflaeche) ehrlich im Kopf `:27-29`. Nur Bild der MP-Kopie |
| B7 | offen, berechtigt aufgeschoben (B5a) | Jar `dec/AnimalData.java:1544-1546` bestaetigt (`originalSize = size` vor dem Setzen). Folge nur bei Tod/Zerlegen; kein Rueckschritt gegen B1c |
| B8 | offen, berechtigt als Frage 8 | `Stats.lua:233-235` `floor(g x D)` -- gewollte Folge von "g als Anteil" |

## 3. Selbst laufen lassen (Zahlen, 11.11.2026 ~10:40-10:50)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (25 Lua des Stagings) | 25 checked, 0 failed |
| `scopecheck.py` | 25 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 48 (`Hud.lua` Dateiebene), 39 (`Server.lua:921`, Bench `:384`, `Hud.lua:420`); insgesamt hoechstens 77 (`World.lua:640`), 59 (Hud), 58 (`Server.lua:921`) -- weit unter 180/200 |
| `luacheck_pz.py` | 18 x W113, alle erwartet: 3 Aktionsklassen (`Menu.lua:86/97/107`), 15 in der Bench (`NCBearBenchCub.lua:907-922`, eigene Globale und `NCBearMenu` aus der alten Bench) |
| Dateiform (eigenes Skript, 48 .lua/.json/.txt) | 0 Probleme: LF, kein BOM, LF am Ende, keine Leerzeichen am Zeilenende, Lua/.txt ASCII, JSON Round-Trip + sortiert. `attrappe/kern/dateiform.py` auf 24 Kern-Lua: nur die alten "test"-Treffer in `client/BanditsNPCBearMenu.lua` (Datei byte-gleich zur Test-Mod) |
| `kern` / `b1b_kern` / `b1c_kern` / `b1d_kern` | 136/0, 204/0, 192/0, **163/0** -- alle byte-gleich `ergebnis.txt` (b1d_kern aus dem Ordner `attrappe/` gerufen; mit absolutem Pfad unterscheidet sich nur der Pfad in 2 Fehlerzeilen) |
| `gesamt/run.lua` | **1173 / 0**, byte-gleich `ergebnis.txt`; gegen die Probe der Nachbesserung (`probe_b1d/NPCCrew/42/media/lua/`) 1173 / 0, byte-gleich `ergebnis_probe.txt` |
| `ober`, `b1b_ober`, `b1c_ober`, `b1d_ober` (ohne / mit `kern`) | 116+117, 144+134, 193+180, **174+176**, je 0 Fehler |
| `pruef_b/run.lua`, `pruef_b1b/run_nach.lua`, `pruef_b1c/run.lua`, `pruef_b1d/run.lua` | byte-gleich `ergebnis_b1b_nach.txt`, `ergebnis_b1c.txt`, `ergebnis_nach.txt`, `ergebnis_nach.txt`; pruef_b1d: **10 bestanden, 0 Fehler, 3 Befunde** (P1c, P2a, P2c -- alle bekannt) |
| `texte_pruefen.py` / `_b1b` / `_b1c` / `_b1d --tmp <scratch>` | FEHLER gesamt 0 / 0 / 0 / 0; `texte_b1d.py` -> 22 Dateien, abweichend vom Staging keine; `--basis` == `texte_b1c.py` |
| `belege.py` / `_b1b` / `_b1c` / `_b1d` | abweichend 0 von 112 / 51 / 89 / 23 |
| `gesamt/xref_b1d.py` | 0 Luecken, 3 Hinweise (Rueckfallwerte Rules.lua, wie vorher), byte-gleich `xref_b1d.txt` |
| `gesamt/gegenprobe_b1d.py` | 26 von 26 erkannt, byte-gleich `gegenprobe_b1d.txt` |
| `probe_force.py` / `probe_regeln.py` | 23 Faelle, 0 Fehler / 34 Faelle, 0 Fehler |
| Platzhalter + CN (eigenes Skript) | UI.json 133, Sandbox.json 60 Schluessel in allen 7 Sprachen gleich, `%n` je Schluessel gleich (0 Abweichungen); 398 CN-Zeichen, **0** nicht in Vanilla-CN (44 Dateien) |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, byte-gleich `trockenlauf_b1d_nach_vor_b5a.txt` (NPC Crew hat sich seit 10:33 nicht so geaendert, dass es zaehlt) |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler (genau die Altlasten aus ALT_EXPECTED), 2 Warnungen, byte-gleich `trockenlauf_b1d_nach.txt` |
| **Probe** `--probe <scratch>/probe_gp --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen (PROBE)**, 51 Datei(en) geschrieben, je kopierter Lua luacheck/scopecheck/localcount ok (hoechstens 77); IG_UI.json 0 -> 3, Sandbox.json 92 -> 151, UI.json 3812 -> 3945 je Sprache; Tier-Regeln an ihren Orten (`setSizeForced` `Stats.lua:348`, `getData` `:345`, `setHealth` `Grow.lua:250`, `getHealth` `:216`, Probeweg: kein Aufruf). Ausgabe bis auf die Ordnernamen gleich `probe_b1d_nach_ausgabe.txt`. Keine `*bench*`-Datei in der Probe-Kopie |
| `pcall(` | Staging 5, Test-Mod 5 -- kein neuer |

### 3.1 `staging_dateien.txt` gegen Platte und Test-Mod nachgezaehlt (eigenes Skript, MD5 + Bytes)
- Liste 51, Platte 51, nur Liste 0, nur Platte 0, **0 Abweichungen** bei MD5, Bytes und Spalte neu/ueberschreibt/gleich.
- **2 neu:** `server/BanditsNPCBearGrow.lua`, `shared/BanditsNPCBearStats.lua`.
- **25 ueberschreibt** (alle gewollt, alle aus der eigenen Linie B1a-B1c, Test-Mod-Stand 08:12 = B1c-Einbau, seither unveraendert):
  10 Lua (`client/BanditsNPCBearClient.lua` 17872 -> 20845, `...Options.lua` 5409 -> 6918, `ISUI/...Hud.lua` 26434 -> 35539,
  `NCBearBenchCub.lua` 34433 -> 42668 (eigene Bench aus B1a, nur angehaengt: 156 neue Zeilen, 1 Kommentarzeile geaendert),
  `server/...Heal.lua`, `...Registry.lua`, `...Ride.lua`, `...Server.lua`, `shared/BanditsNPCBear.lua`, `...Defs.lua`), 14 JSON
  (`UI.json` und `Sandbox.json` x 7 -- je Sprache NUR +24 bzw. +10 Schluessel, 0 geaendert, 0 entfernt) und `42/media/sandbox-options.txt`
  (5536 -> 7055, nur 5 Optionsbloecke angehaengt).
- **24 gleich** (u. a. Modell, Textur, Symbol, `nc_bear_cub.txt`, alle IG_UI.json).
- Nicht beruehrt: alle alten `NCBear*`-Dateien des Erwachsenen (`NCBearBench.lua`, `NCBearTest.lua`, `NCBearFight.lua`, `NCBearDefs.lua`,
  `NCBearSize.lua`, `NCBearSpawn.lua`, `NCBearAttackProbe.lua`, Modelle, Toene, AnimSets) -- Auftrag "alte NCBear*-Dateien NICHT aendern" erfuellt.

## 4. Eigene Stichproben

### 4.1 Einzelspieler-Weg `NCBear_CubGrow(15)` Zeile fuer Zeile bis zum Bild
1. `S:client/NCBearBenchCub.lua:817-830` -> `myGrowRec` (`:793`) -> `ready()` (`:69-90`, `B.IsSP()` -> sonst "singleplayer only") -> `growReady`
   (`:784`) -> `myTame` (`:474`, naechstes `st == "tame"` mit `owner == key`). `want = g + 15/100`, geklemmt.
2. `Grow.lua:623` `B.GrowSetG`: `GrowFix` (fehlt `g`, aus `tamedAt`), `rank0`, `rec.g = v`, `commitGrow` -> `B.Commit` (`Registry.lua:420-431`:
   `r + 1`, Spiegel mit `g` an `s.obj`, `B.Touch`), `B.FindAnimal` -> `B.BodyOf` (`Stats.lua:225-230`: `GrowSize(0.15)` = genau 0,75, Deckel
   `cubMaxSize` 0,75) -> `B.ApplySize` (`Stats.lua:343-350`: `|0,35 - 0,75| > 0,002` -> `setSizeForced(0.75)`), Stufe "half" > "cub" ->
   `tellStage` -> `B.Tell` (`shared/BanditsNPCBear.lua:513-522`: SP -> `B.ShowNote` direkt, das ganze Feld `note` geht mit) -> Text
   `UI_BN_Bear_Note_Grown` mit `U.StageName("half")` = "half-grown" (`Client.lua:208-213`, `:237-238`).
3. `B.BrainTick(true)` (`Server.lua:1030-1042`) -> `brainTickBody` Schritt 7 -> `B.GrowLive` (`Grow.lua:412-435`): `bodySwap` aus,
   `ApplySize` schreibt nicht mehr (gleich), `rec.hp == nil` -> `BodyHp(rec, a, 0)` holt 1,0 vom Koerper und `B.Touch`, Ausdauer.
4. `push(p)` -> `B.PushView` -> Sicht mit `B.GrowView` (`Grow.lua:596-616`, aus `viewEntry` `Registry.lua:581-582`): `sz 0.75`, `hp 100`,
   `hpMax 150`, `sta 100`, `staMax 100`, `day 15`, `stg half`, `nst strong`, `nxt 30`.
5. Hud (`Hud.lua:497-525`): `md` einmal je Liste (Vorgaben Leben = Balken, Ausdauer = aus, Alter = an), `tameShown`, `describe` ->
   `describeValues` -> Alter-Zeile "Day 15 - strong in 30 day(s)", roter Balken voll; Anker `tagZ x 0,75 / 0,35` (`:362-371`, Deckel 5).
   `draw` (`:628`) nur aus der fertigen Liste. Im SP keine Client-Probe (`isClient()` falsch, `:443`).
Nachgerechnet (Formeln `Stats.lua:276-320` mit `B.CFG`): Tag 0 -> Leben 40, Ausdauer 50, Traglast 10; Tag 5 -> 77 / 67 / 20; Tag 15 -> 150 /
100 / 40; Tag 45 -> 254 / 125 / 65 (Bild 0,75); Tag 100 -> 400 / 160 / 100. Deckt sich mit PLAN_B1D.md 7.4. **Kein Fehler gefunden.**
Nebenbefund dabei: `B.GrowFeed` steht in `B.FeedComplete` (`Server.lua:243`) NACH `takeOne` und VOR `B.Commit` -- wuerfe es, waere das Futter weg
ohne Commit. Durchgesehen: reines Lua ohne unbelegten Engine-Aufruf, alle Felder nach `GrowFix` Zahlen, `tellStage(..., nil)` ->
`B.PlayerByKey(key, nil)` holt die Spieler selbst (`World.lua:68-75`). Kein Wurfweg gefunden; als Merker C5.

### 4.2 Eine Sprache ganz gegengelesen: RU (24 + 10 neue Schluessel)
Alle 34 neuen RU-Texte gelesen (ausgegeben ueber `python -X utf8`): Sinn passt zu EN, Platzhalter vollstaendig, Satzbau mit den eingesetzten
Werten richtig ("Ваш медведь теперь полувзрослый.", "День 12 - полувзрослый через 3 дн.", "Навык медведя «ловкость» теперь на уровне 2.").
Zusaetzlich FR, PTBR, ES, KO, CN ueberflogen: KO und CN stellen `%3` vor `%2` -- geht, `B.T` reicht an `getText(key, s1, s2, s3)` weiter
(drei Einsetzungen belegt `V:client/DebugUIs/DebugMenu/Anims/ISAnimDebugMonitor.lua:114`, vier `ISVehicleMenu.lua:403`), Vanilla ersetzt
nach Nummer. Platzhalter-Paritaet und CN-Zeichen per Skript: 0 Abweichungen (Abschnitt 3). **Kein Fehler.**

### 4.3 Mehrspieler-Zweig von "neuer Koerper" (Aussteigen, Call to me) -- daraus C1
`S:server/BanditsNPCBearRide.lua:67-92` `B.PlaceCub`: `CreateCub` (Tier in der Welt), `gen + 1`, `s.obj = a`, `Commit`, `WriteMark`, **dann
`B.GrowBody` (`:86`) -> `B.BodyHp` -> `a:getHealth()`**, erst danach `CalmDrop`, `_zed`, Rueckgabe. Die Aufrufer setzen `rec.ride = nil` erst
NACH der Rueckgabe (`:178`, `:212`; Call to me entfernt den alten Koerper erst `:335`). Unter genau der Annahme, die B2 begruendet hat (`getHealth`
wirft am MP-Server), bricht beim Aussteigen `B.RideStep` = Schritt 1 des Hirn-Takts (`Server.lua:928-933`) ab -- der ganze Takt steht, und der
naechste Takt (1,5 s) setzt das Junge NOCH EINMAL in die Welt, weil `rec.ride` stehen blieb; das vorige Tier bleibt als alte Kopie bei einem
zusehenden Besitzer stehen. Bei Call to me bleiben zwei Koerper. Im SP nicht betroffen (`getHealth` im SP gespielt, `NCBearAttackProbe.lua:104`,
`ENT:60`). Wahrscheinlichkeit gering (schlichter Getter, Jar `IsoGameCharacter.java:3181`; Bandits ruft ihn am Server am Zombie), aber die Folge
ist schlimmer als bei B2 -- vor dem MP-Test beheben (Vorschlag: `B.GrowBody` von den drei Aufrufern NACH `rec.ride = nil` / nach
`B.RemoveCub(old)` rufen, oder in `GrowBody` nur die Groesse setzen und das Leben dem naechsten Langsam-Takt lassen -- `BodyHp` nimmt die
1,0 des neuen Koerpers dort als Engine-Heilung zurueck, weil `hpB` im Register steht).

## 5. Neue Restbefunde (keiner rot, keiner verhindert den SP-Test)
- **C1 (minor, nur MP):** B2-Rest in `B.PlaceCub` (`Ride.lua:86`), Begruendung 4.3. Vor dem MP-Test beheben; Testpunkt "Server-Log nach
  `[TC-BEAR] *** brain tick:` beim Aussteigen" in PLAN_B1D.md 7.4 MP 6/7 aufnehmen.
- **C2 (Kleinkram):** `ageToGrow = 36500` (`Defs.lua:73`) macht die Debug-Tier-Knoepfe gefaehrlich: "max size" ruft laut Jar
  `setMaxSizeDebug` -> `setAgeDebug(Alter + 36497)` (`dec/IsoAnimal.java:1862-1863`, `:1583-1586`, danach `init()`), das Junge waere ~100 Jahre
  alt. Nur Debug (Tier Cheat); die Groesse holt `GrowLive` sofort zurueck. In der Anleitung: Tier Cheat aus, am Jungen keine Debug-Knoepfe.
  `randomizeAge` (`:1945-1946`) rufen nur Fallen (`V:server/Traps/STrapGlobalObject.lua:236`) und Wanderherden (`dec/MigrationGroupDefinitions.java:222`)
  -- unser Junges ist in keinem von beiden.
- **C3 (Kleinkram):** Hilfe von `NCBear_CubSet` (Bench `:447-451`) nennt die neuen Stellwerte `conStepMul` und `hpLossEps` nicht (setzbar sind sie).
- **C4 (Kleinkram, zu A1):** Tooltip "Bear: healing per hour while awake" sagt nicht, dass 0 auch die Heilung des Spiels abstellt (nur der
  Kommentar in `sandbox-options.txt` nennt das Zuruecknehmen). Mit Kevins Antwort auf Frage 1 nachziehen.
- **C5 (Merker):** `B.GrowFeed` zwischen `takeOne` und `B.Commit` (`Server.lua:234-244`) -- heute ohne Wurfweg (4.1); wer `GrowFeed` spaeter
  erweitert, muss das wissen (sonst Futter weg ohne Gutschrift = rote Linie).
- Bekannt und weiter offen (nicht neu): P1c, B6-Rest, B7, Pausen-Erholung der Ausdauer, `originalSize` beim Tod; je Text mit Platzhalter
  hoechstens eine "Missing arguments"-Warnung je Sitzung (B1a Fix 2, `shared/BanditsNPCBear.lua:308-312`) -- jetzt 6 Schluessel mehr.

## 6. Fragen an Kevin (alle mit Empfehlung; keine haelt den Test auf)
Die neun Fragen der Nachbesserung (`nachbesserung_b1d.md` 3) gelten unveraendert; ich stimme allen Empfehlungen zu, mit einer Aenderung:
1. (A1) Selbstheilung 1 %/h ist schon an, obwohl du "Heilen erst nach meinem B1c-Test" gesagt hast -- so lassen? (Empfehlung: ja, mit dem Test ansehen.)
2. (A3) `setHealth` (Werte zwischen 0 und 1) und `setSizeForced` am lebenden Tier als belegt zaehlen? (Empfehlung: ja.)
3. (A4) Spieler und Autos sollen dem Baeren nicht schaden -- mit B5a abschalten? (Empfehlung: ja.)
4. (A5) Die drei Testwege (Vorspulen, Leben setzen, Erfahrung setzen) aus dem Kern in die Testhilfe verlegen? **Empfehlung: ja, und zwar vor
   jeder echten Uebernahme nach NPC Crew** (nicht nur "irgendwann").
5. (A6) Erklaertexte unter "Leben"/"Ausdauer" zeigt das Spiel nicht -- reicht der Name? (Empfehlung: ja.)
6. (A7, wie B1c A3) `addComboBox`/`addItem` als belegt zaehlen (Vanilla-Definition gelesen, NPC Crew benutzt sie gespielt)? (Empfehlung: ja.)
7. (B1/F18) Mehrspieler nach Server-Absturz: Wachstum aus der Markierung, gedeckelt -- so lassen? (Empfehlung: ja.)
8. (B8/F12) "Tag" im Schild wird bei geaenderter Sandbox-Zahl neu gezaehlt -- ok? (Empfehlung: ja.)
9. (B4/F14) Vorspulen schneller als etwa x4 zaehlt Rennen nicht -- ok? (Empfehlung: ja.)
Dazu aus PLAN_B1D.md 11 vor allem **F11 Modellwechsel** (Junges- oder Erwachsenen-Modell fuer Halbstark; Empfehlung: nach dem Blick in F2
entscheiden) und **F2 Fussgleiten** bei 0,75 (im Test ansehen); F3 Zahlen (Leben 40/150/400, Ausdauer 50/100/160) im Test nachstellen.

## 7. Fuer den Integrator
- Einbau erst nach neuem `tasklist` und Mod-Liste des GELADENEN Spielstands (10:47 lief das Spiel, NCBearTest nicht geladen); vorher/nachher Zip
  nach `Zomboid/backups/NCBearTest/`, 51 Dateien in einem Zug (2 neu, 25 ueberschreiben, 24 gleich), danach byte-gleich nachzaehlen.
- `mod.info` / `42/mod.info`: Beschreibung nach `mod_info_vorschlag.txt` (nicht im Staging).
- Offene Aenderungen im Repo `baer/` (NAEHTE.md, STAND.md, tools/baer_uebernahme.py, neue `spiel/*.py`) gehoeren zum Commit des Laufs.
- C1 in den Plan des naechsten Laufs (vor dem MP-Test); A5 vor `--echt`.

Statisch geprueft, nicht gespielt. Nach dem Einbau muss Kevin das Spiel neu starten (Lua und die Tier-Definition laden nur beim Start).
