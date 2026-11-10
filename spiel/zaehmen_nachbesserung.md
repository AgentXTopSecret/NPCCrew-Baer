# Nachbesserung B1a "baer-zaehmen" (10.11.2026)

Grundlage: `pruef_a.md` (A1-A10), `pruef_b.md` (B1-B7). Jeder Befund am Code und an den Fundstellen nachgeprueft.
**Statisch geprueft, nicht gespielt.** Kein Schreiben in Test-Mod, NPC Crew, Vanilla oder Bandits; kein git.
Zeilen "nachher" = Staging `mod/42/media/lua/...` nach dieser Nachbesserung. Alle Lua-Dateien LF, reines ASCII.

## Ergebnis je Befund

| ID | Schwere | Urteil | Kurz |
|---|---|---|---|
| B1 | blocker | bestaetigt, behoben | Hello mit `{ v = 1 }`; Server nimmt `nil` wie `{}`; erste Sicht auch ohne Hello |
| A1 | major | bestaetigt, behoben | `removeAnimal(animal:getOnlineID())` im Server-Zweig von `B.RemoveCub` |
| A2 | major | bestaetigt, behoben | `serverStart`/`serverStop` in Fuettern und Streicheln, `complete()` loest die Sperre |
| A3 | major | teils bestaetigt | `findBreed` auf Server-Beleg umgestellt; `getObjectListForLua`, `getAnimalID`, `isRotten`/`isBurnt` ohne Server-Beleg: MP OFFEN |
| B2 | major | bestaetigt, behoben (Weg b) | Welt-Deckel zaehlt nur Junge, deren Finder/bond online ist; Uhr-Regel unveraendert (Plan) -> Kevin-Frage |
| A4 | minor | bestaetigt, behoben | nur Kommentare auf shared/Server-Fundstellen |
| A5 | minor | bestaetigt, behoben | `NCBear_CubLog`/`NCBear_CubSet` erst `B.IsSP()` |
| A6 | minor | bestaetigt, behoben | Cheat-Regel `altmenue` (`NCBearMenu`, `NCBearBench*`); Gegenprobe rot |
| A7 | minor | bestaetigt, behoben | eine Zahl mit grep-Muster in NAEHTE.md und Crew.lua |
| A8 | minor | bestaetigt (kein Fehler), keine Aenderung | Testpunkt SP: Konsole bei Treffer/Tod des Jungen |
| A9 | minor | bestaetigt, behoben | "Werkbank" aus zwei Kommentaren; Warnung im Trockenlauf weg |
| A10 | minor | bestaetigt, behoben | Uebernahme kopiert bis B5a nur `NCBear_Eat.xml` |
| B3 | minor | bestaetigt, behoben | `fed` erst nach 3 Suchlaeufen UND `fedMissH` (1 Spielstunde) "verloren" |
| B4 | minor | bestaetigt, behoben | Fuettern am zahmen Jungen meldet `Note_Happy` |
| B5 | minor | bestaetigt, behoben | reifer Koederplatz verfaellt nach (Naechte + baitExtra + 1) Tagen |
| B6 | minor | bestaetigt, behoben | Server: vermisste Zahme nur je 30 s; HUD: dritte Stufe 30 s |
| B7 | minor | bestaetigt, behoben | Regel 7 haelt auch, wenn bond/Besitzer naeher als `reach` steht |

## Im Einzelnen

### B1 (blocker) -- bestaetigt
Nachgeprueft: `dec/SinglePlayerServer.java:179-190` (`hasArgs` false -> `tbl = null`), Vanilla `client/ServerCommands.lua:210-213`
("Can be nil if sending an empty table"), `server/ClientCommands.lua:1349` (`if args then`). Vorher: `client/BanditsNPCBearClient.lua:210`
`B.Ask(player, "Hello", {})`, `server/BanditsNPCBearServer.lua:379` verwarf `args ~= table`, `:763` schickte beim ersten Eintrag nichts.
Geaendert:
- `client/BanditsNPCBearClient.lua:210` -> `:213` `B.Ask(player, "Hello", { v = 1 })` (Kommentar :211-212 mit Fundstellen).
- `server/BanditsNPCBearServer.lua:376-380` -> `:390-397`: `if args == nil then args = {} end` vor der Typpruefung.
- `server/BanditsNPCBearServer.lua:763` -> `:797-800`: `if B._sig[e.uid] ~= sig then` (auch beim ersten Takt eines Spielers).
Keine neuen Engine-Aufrufe. Attrappe: `attrappe/kern/attrappen.lua` bildet die leere Tabelle jetzt als nil nach (gewollt: vorher falsch
modelliert, Pruefer B Fall 15); `pruef_b/run.lua` Fall 1a jetzt OK.

### A1 (major) -- bestaetigt
`ButcheringUtil.lua:609` `animal:remove()`, `:612-614` im `isServer()`-Zweig `removeAnimal(animal:getOnlineID())`; `server/ClientCommands.lua:841`.
Geaendert `server/BanditsNPCBearWorld.lua:253-258` -> `:248-258`: nach `animal:remove()` `if isServer() then removeAnimal(animal:getOnlineID()) end`
(Argumenttyp Zahl wie ButcheringUtil). Uebernahme-Skript: neue Tier-Regel `removeAnimal` (nur in `B.RemoveCub`), Trockenlauf zeigt
`BanditsNPCBearWorld.lua:254 (B.RemoveCub)`; NAEHTE.md Tier-Regel ergaenzt.

### A2 (major) -- bestaetigt
`ISMilkAnimal.lua:212` (serverStart sperrt), `:169` (serverStop loest), `:196` (complete loest). Plan 6.2.7 "Server ruft NUR complete()" war zu eng.
Geaendert `shared/TimedActions/BanditsNPCBearFeedAction.lua:94-98` -> `:94-112` und `BanditsNPCBearPetAction.lua:95-99` -> `:94-112`:
`serverStart()` `setBlockMovement(true)`, `serverStop()` `setBlockMovement(false)`, `complete()` ruft den Kern und loest danach die Sperre,
Rueckgabe wie vorher das Kern-Ergebnis. Kopf-Kommentare (:4-5) angepasst. Gegenstaende unberuehrt (das Nehmen bleibt im Kern).
Testpunkt MP: Junges waehrend Fuettern/Streicheln am Server stillstehend.

### A3 (major) -- teils bestaetigt
Die eiserne Regel (Werkstatt-CLAUDE.md 3) verlangt Vanilla/Bandits-Aufruf mit gleichen Argumenttypen, keine "gleiche Seite"; alle vier hatten
solche Belege. Das MP-Risiko ist aber echt, und fuer die Rasse gibt es einen Server-Beleg. Gesucht (Vanilla server/ + shared/ + Bandits 42.22/common):
`getObjectListForLua` 0, `getAnimalID` 0, `isRotten()` 0, `isBurnt()` 0 -- bestaetigt.
- Geaendert `server/BanditsNPCBearWorld.lua:205-219` -> `:205-212`: `findBreed` = `AnimalDefinitions.getDef(B.CUB)` (Text), `nil`-Pruefung,
  `def:getBreedByName(B.BREED)` (Text) -- Vanilla `server/ClientCommands.lua:808`, `ButcheringUtil.lua:79/85`.
- `getObjectListForLua` und `getAnimalID`: Kommentar `World.lua:276-277` "im Mehrspieler OFFEN, Testpunkt". `isRotten`/`isBurnt`
  (`shared/BanditsNPCBearFood.lua:58`) unveraendert. Es gibt keinen Server-Beleg; Kevins Wort je Methode oder MP-Test. (NPC Crew selbst ruft
  `getAnimalID` am Server, `server/BanditsNPCLivestockHerdServer.lua:115` -- kein Vanilla-Beleg, nur Hinweis.)
- Attrappe: `AnimalDefinitions.getDef` nachgebildet (`kern/attrappen.lua`, reset).

### B2 (major) -- bestaetigt, Weg b
Die Uhr "nur online" ist erklaerte Plan-Regel (PLAN 2 Zeile 119/122/125, 4.1 Zeile 239, 7 Zeile 808); Zeile 130 meint "nicht geladen", kein
Widerspruch. Der Fehler ist der Deckel: `B.CountWild` zaehlte Junge abwesender Finder fuer immer.
- `server/BanditsNPCBearRegistry.lua:120-129` -> `:120-136`: `B.CountWild(online)` zaehlt nur Junge, deren Finder (new/shy) bzw. bond (fed)
  online ist oder die keinen haben; ohne Argument wie bisher.
- `server/BanditsNPCBearServer.lua`: Helfer `onlineSet` (:59-65); `AppearFor` (:113) und `forestRolls` (:511) uebergeben ihn; Langsam-Takt
  nutzt ihn (:551).
- Attrappe `kern/run.lua` 6g: Spieler "a","b" jetzt online angelegt (gewollte Aenderung). `pruef_b` Fall 2b jetzt OK; 2a bleibt "BEFUND"
  (Eintraege bleiben, so will es der Plan).
- **Kevin-Frage (offen):** sollen Uhren auch laufen, wenn Finder/bond offline sind? Bis dahin bleiben Junge abwesender Spieler im Register
  (hoechstens eines je Spieler; Deckel `maxRecs` 64 bleibt hart).

### A4, A5, A7, A9 (minor) -- bestaetigt, nur Text/Bench
- A4: `Registry.lua:175` isExistInTheWorld -> `ISAddAnimalInTrailer.lua:29`; `:181` getAnimalType -> `ButcheringUtil.lua:13`, getModData ->
  `ButcheringUtil.lua:596/602`; `:403` getOnlineID -> `ButcheringUtil.lua:614`; `Server.lua:138-139`, `:832` ebenso; `World.lua:232`.
- A5: `client/NCBearBenchCub.lua:339-349` und `:349-357`: `if B.IsSP and not B.IsSP() then out("singleplayer only") return end` vorgeschaltet.
- A7: grep `NOT_TENDED` in NC `42/media/lua`: 24 Treffer in 9 Dateien, davon 14 Code-Zeilen in 8 Dateien. So in `NAEHTE.md` Naht 1 und
  `shared/BanditsNPCBearCrew.lua:9-10` (mit Muster). PLAN 12.2 unveraendert (Plan-Text).
- A9: `Registry.lua:338` "fuer Meldungen und Werkbank" -> "fuer Meldungen"; `shared/BanditsNPCBear.lua:31` -> "zur Laufzeit aenderbar".
  Die Trockenlauf-Warnung "Kommentare ... nennen Testbefehle" ist weg (3 -> 2 Warnungen).

### A6 (minor) -- bestaetigt
`baer/tools/baer_uebernahme.py` CHEAT_RULES neue Regel `altmenue`: `\bNCBearMenu\b|\bNCBearBench\w*`. Gegenprobe (Scratchpad-Kopie des Stagings,
an `BanditsNPCBearMenu.lua` angehaengt `NCBearMenu = NCBearMenu or {}` / `table.insert(NCBearMenu.extra, ...)`): 3 Fehler
(`altmenue` :328, :329; `global` :328), ERGEBNIS NICHT OK. Das echte Staging trifft die Regel nicht.

### A8 (minor) -- bestaetigt, kein Fehler, keine Aenderung
Gewollt (Plan 6.5). Testpunkt SP: Junges treffen und toeten, `console.txt` auf Ton-Warnungen pruefen; bei Bedarf Kitz-Toene
(`DeerDefinitions.lua` fawn_sounds ab :213) als Platzhalter.

### A10 (minor) -- bestaetigt
`baer_uebernahme.py`: `ANIMSET_OK` nur noch `NCBear_Eat.xml`; neu `ANIMSET_ADULT` -> "NICHT kopiert, bleibt bis B5a" (9 Knoten).
Altlasten-Zahl bleibt 24. Hilfetext angepasst. `NAEHTE.md` Naht 9, Abschnitt "Kopiert wird ...", B5a-Liste angepasst.
Probe schreibt jetzt 40 statt 49 Dateien.

### B3 (minor) -- bestaetigt
`server/BanditsNPCBearServer.lua` `countMisses` (:717-741): erster Fehlversuch merkt `rec.missAt` (Weltstunden); `fed` wird erst geschlossen,
wenn `missN >= missScans` UND `now - missAt >= B.CFG.fedMissH` (neu, 1.0 h, `shared/BanditsNPCBear.lua:62`). `liveRec` setzt `missAt = nil`
(:655); tame->missing auch (:732). Registry-Eintrag nennt das Feld (`:165`). new/shy unveraendert (Plan: 3 Suchlaeufe). Abweichung vom Plan-Satz
"3 Suchlaeufe" nur fuer `fed`. `pruef_b` Fall 3a/3b jetzt OK.

### B4 (minor) -- bestaetigt
`B.FeedComplete` (`Server.lua:209-251`): `wasTame` vor dem Nehmen; dann `Note_Happy` statt `tellGain`. Stueck wird weiter genau einmal
verbraucht (Plan 11). `pruef_b` 3c jetzt OK.

### B5 (minor) -- bestaetigt
`baitAppear` (`Server.lua:744-781`): reifer Platz mit `now - t0 >= (BearBaitNights + baitExtra + 1) * 24` (Vorgabe 8 Tage) -> `DropBait`,
`Bait_Expired` an den Besitzer (falls online), Log. Kein neuer Text.

### B6 (minor) -- bestaetigt
- Server `resolve` (:694-712) gibt `needSlow` fuer vermisste Zahme; `brainTickBody` (:816-822) sucht dann nur je `scanMs * missScanMul`
  (neu `missScanMul = 6` -> 30 s). Attrappe `kern/run.lua` 3g wartet entsprechend (gewollt).
- HUD `client/ISUI/BanditsNPCBearHud.lua:33-40`, `:226-246`: nach 17 vergeblichen Laeufen nur noch je 30 s; neue Sicht setzt auf schnell zurueck.
  Die Variante "x,y in der Sicht" haette die Schnittstelle geaendert -- nicht gemacht.

### B7 (minor) -- bestaetigt
`shared/BanditsNPCBearRules.lua:306-313`: fed/tame mit `mate.dist < cfg.reach` -> `hold` (Regel 7). Damit loest der Takt die Sperre einer
laufenden Streichel-Aktion nicht mehr (SP; im MP zusammen mit A2). Testpunkt im Spiel bleibt.

## Schnittstelle, Uebernahme, Naehte
- `schnittstelle_aenderungen.md`: "NACHBESSERUNG, Eintrag 3" angehaengt (Hello-Nutzlast, CountWild, serverStart/Stop, CFG, missAt, Regel 7, HUD).
- Keine neuen Texte (Note_Happy, Bait_Expired gab es schon, 7 Sprachen).

## Pruefer-Ausgaben (alle 15 Lua-Dateien, Staging)
| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` | 15 file(s) checked, 0 failed |
| `scopecheck.py` | 15 file(s), 0 violation(s) |
| `luacheck_pz.py` | 11 x W113 (wie vorher, alle erwartet: 3 Aktionsklassen in `BanditsNPCBearMenu.lua:81/92/102`, 8 in der Bench) |
| `localcount.py` | hoechstens 39 aktiv / 42 insgesamt je Funktion (Hud :183); Grenze 200 |
| Zeilenenden/ASCII | 15 Lua, `sandbox-options.txt`, `nc_bear_cub.txt`: LF, ASCII, kein BOM, Zeilenende am Schluss |
| JSON-Round-Trip | 21 Dateien: Round-Trip gleich, sortiert, LF, ohne BOM (unveraendert) |
| Gesamt-Attrappe | `attrappe/gesamt/run.lua`: **261 bestanden, 0 Fehler** (vorher 175; neu Abschnitt 16 mit je einer Probe zu A1, A2, B1-B5, B7), `ergebnis.txt`; gegen die Probe: 261/0 (`ergebnis_probe.txt`) |
| Kern-Attrappe | `attrappe/kern/run.lua`: 133/0 (3g, 6g angepasst, s. o.) |
| Oberflaechen-Attrappe | `attrappe/ober/run.lua`: 113 ok, 0 Fehler |
| Pruefer-B-Attrappe | `attrappe/pruef_b/ergebnis_nach.txt`: 1a/1b/1c/2b/3a/3b/3c OK; 2a BEFUND (gewollt, Kevin-Frage B2) |
| Trockenlauf | `trockenlauf.txt`: NICHT OK -- 24 Fehler (genau die 24 Altlasten), 2 Warnungen (vorher 3) |
| Trockenlauf `--vor-b5a` | `trockenlauf_vor_b5a.txt`: OK -- 0 Fehler, 26 Warnungen |
| Probe `--vor-b5a` | `probe_ausgabe.txt`: OK -- 0 Fehler, 26 Warnungen; 40 Dateien geschrieben (14 Lua, 4 Dateien, 21 Texte, sandbox-options.txt); Pruefer auf der Probe: alle 14 luacheck/scopecheck/localcount ok, luacheck_pz 0 Treffer + 3 erlaubt |

`staging_dateien.txt` neu: 40 Dateien, 39 neu, 1 ueberschreibt (EN/IG_UI.json, Begruendung unveraendert); 11 Lua-Dateien mit neuer MD5.

## Offen
- **Kevin-Frage B2:** Uhren auch offline laufen lassen (ggf. langsamer)? Heute: nur online (Plan), Deckel zaehlt Abwesende nicht.
- **MP ungeprueft (A3):** `getCell():getObjectListForLua()` und `getAnimalID` am Server, `isRotten`/`isBurnt` am Server: kein Server-Beleg.
  Kevins Wort je Methode oder MP-Test.
- Testpunkte im Spiel: A2 (Junges steht beim Fuettern/Streicheln im MP), A1 (kein Geistertier nach Verschwinden im MP), B3 (Gegend verlassen
  und wiederkommen), B7 (Streicheln ohne Futter in der Hand), A8 (Konsole bei Treffer/Tod), B1 (Spieler verbindet neu: Balken/Menue da).
- PLAN_ZAEHMEN.md nicht nachgezogen (Abweichungen: B3 1 h fuer `fed`, B5 Verfallsfrist, B2 Deckel, A2 serverStart); hier dokumentiert.
- Staging ist NICHT in der Test-Mod (das macht der Integrator).
