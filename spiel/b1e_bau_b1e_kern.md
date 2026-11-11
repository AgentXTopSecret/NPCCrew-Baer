# Lauf baer-b1e: Bau KERN -- Modellwechsel ab Halbstark (grosser Koerper bis 1,35)

Stand 11.11.2026 abends. Rolle: BAUER KERN (`shared/` ohne Translate, `shared/TimedActions/`, `server/`, Kern-Attrappen). Grundlage
`PLAN_B1E.md` 0-8 (woertlich), Abweichungen/Zusaetze in `schnittstelle_aenderungen.md` Abschnitt "B1e KERN" (10 Punkte).
**Statisch geprueft, nicht gespielt.** Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart.

**Vorab nachgezaehlt (11.11.):** `staging_dateien.txt` gegen `Zomboid/mods/NCBearTest` per MD5: 51 Dateien, **49 byte-gleich, 2 verschieden**
-- `42/media/models_X/Skinned/NCBearCub.glb` (Staging ee7a0cce = Generator-Junges, Test-Mod 6c3f0a96 = altes Junges) und
`42/media/textures/Body/NCBearCub.png` (92a829fa / 2ee25f24). Genau wie PLAN_B1E.md "Vorab"; das alte Junge legt der ZUSAMMENBAU ins
Staging (10.1). Alle Lua-Dateien waren vor dem Bau byte-gleich.

---

## 1. Dateien (Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`)

| Datei | MD5 vorher -> nachher | Zeilen | Was |
|---|---|---|---|
| `shared/BanditsNPCBear.lua` | 251c1c8d -> ce4a7fcc | 573 | `B.BIG`, `B.BODY_TYPE`, `B.TYPE_BODY`, `B.BodyKind`, `B.NoteBd`, `B.ViewOf`, `B.CFG` (B1e-Block), Kopf |
| `shared/BanditsNPCBearDefs.lua` | 1f549dcf -> 1445f366 | 211 | Art `ncbeargrown` (Definition, Avatar, Zerlege-Teile), Kopf |
| `shared/BanditsNPCBearStats.lua` | 8be6a4b1 -> c5210758 | 425 | `B.BodyWant`, `B.BodySize`, `B.BodyOf` (neu), `B.BodyNow`, `B.BodyNum`, `B.BodyGap`, `B.StatsOf` + body/want |
| `shared/BanditsNPCBearRules.lua` | 7271a923 -> 94619ea7 | 633 | `B.FollowDecide` (c.gap, c.walkSpeed), `B.GuardDecide` (c.gap) |
| `shared/TimedActions/BanditsNPCBearPetAction.lua` | c6534e9a -> 9c2650bd | 170 | Haltung je Koerper aus der Sicht, Beschaeftigt-Marke |
| `shared/TimedActions/BanditsNPCBearFeedAction.lua` | 3a4fa68b -> e025ff48 | 140 | Beschaeftigt-Marke |
| `server/BanditsNPCBearWorld.lua` | 00a77e0d -> 7c17b4e2 | 931 | `findBreed(body)`, `B.CubDefOk(body)`, `B.CreateCub(..., body)`, `B.RemoveCub`/`B.FindAnimal`/`B.ScanAnimals` ueber `B.BodyKind`, `B.SwapSpot`, `B.MoveTo` Tempo je Koerper |
| `server/BanditsNPCBearRide.lua` | dcbd67c7 -> 7d4295b7 | 362 | `B.PlaceCub(..., body)` (Koerper, Rueckfall), `B.RideBoard` (`CubDefOk("cub")`), Noten `bd` |
| `server/BanditsNPCBearGrow.lua` | ef40b7d4 -> 28c18847 | 793 | `B.BodySwapReady`, `B.BodyBusy`, `B.BodySwap`, `B.GrowLive` (Tausch statt Fehlerzeile), `B.GrowBody`, `B.GrowSetG`, `B.GrowFix`, `B.GrowView`, `stamina` |
| `server/BanditsNPCBearHeal.lua` | b6835121 -> c00bd28b | 463 | `MARK_FIELDS` + body, `bind` (rec.body), `B.Restore` (Riegel "body") |
| `server/BanditsNPCBearRegistry.lua` | 4361fa2f -> 64e0b4af | 629 | `B.RecOf` (B.BodyKind; grosser Koerper nie "found"), Sitzungs-Kommentar |
| `server/BanditsNPCBearServer.lua` | 3d6679a9 -> 68bdefb3 | 1051 | `handCheck` ueber `B.BodyKind` |
| `server/BanditsNPCBearFollow.lua` | 3334e091 -> 77ef0043 | 286 | `B.FollowStep` (gap, walkSpeed), Noten `bd` in SetMode/HandleMode/HandleRename |
| `server/BanditsNPCBearGuard.lua` | 16c495fb -> 756299ad | 337 | `B.GuardStep` (c.gap) |
| unveraendert | | | `shared/BanditsNPCBearCrew.lua`, `...Food.lua`, `TimedActions/BanditsNPCBearBaitAction.lua` |

Attrappen (`_arbeit/baer_zaehmen/attrappe/`): `b1e_kern/run.lua` **neu** (1162 Zeilen) + `b1e_kern/ergebnis.txt`; `kern/attrappen.lua`,
`b1d_kern/run.lua`, `gesamt/run.lua` gewollt angepasst (Abschnitt 6). Vorher-Staende im Scratchpad gesichert (nicht Teil der Lieferung).
Neue Lua-Dateien im Mod: keine. Alle Kern-Dateien LF, reines ASCII, Ende mit LF (per Python gezaehlt: 0 x CR, 0 Bytes > 127).

---

## 2. Aenderungen mit Datei:Zeile (S: = Staging `mod/42/media/lua/`)

**Helfer und Stellwerte**
- `S:shared/BanditsNPCBear.lua:34-36` `B.BIG = "ncbeargrown"`, `B.BODY_TYPE`, `B.TYPE_BODY` (nie "bear"/"bearstag"/"ncbearcubalt").
- `:497-502` `B.BodyKind(animal)` -> "cub"/"big"/nil -- die EINZIGE Stelle mit `getAnimalType()` im Kern (Attrappe 22 prueft es).
- `:506-509` `B.NoteBd(note, rec)` (bd = "big" nur bei `rec.body == "big"`). `:514-516` `B.ViewOf` fragt `B.BodyKind`.
- `:111-129` B.CFG: `bodySwap = true` (war false), `swapSize 0.72`, `swapBackSize 0.70`, `swapMinMs 60000`, `swapRetryMs 10000`,
  `swapFailLog 6`, `swapRing 2`, `swapFaceDist 30`, `busyMs 20000`, `walkSpeedBig 0.67`, `runSpeedBig 3.17`, `bodyLenBig 1.0448`,
  `tilesPerE 1.5`, `followRefLen 1.12`, `tagBigK 1.06`, `petAnimBig "cow"`, `markerAngleAdd 135`, `markerCloseTiles 6.6`,
  `markerR/G/B 1.0/0.52/0.09`. `cubMaxSize 0.75`, `stageAt`, `walkSpeed/runSpeed 0.52/2.47`, `marker*` unveraendert.

**Neue Art** `S:shared/BanditsNPCBearDefs.lua:146-211`: Kopie der Junges-Definition per `pairs` (`:156-186`), `bodyModel "NCBear_Body"`
(`:159`), Rasse brown = Kopie mit `texture/textureMale/textureBaby "NCBear"` und Junges-Toenen (fallover, petting), eigene `stages`
`{ ncbeargrown = { ageToGrow = 36500 } }`, eigene `genes`-Kopie, `minSize 0.72` (= swapSize, Kommentar an beiden Stellen) / `maxSize 1.35`,
`animalSize 0.3`, `collisionSize 0.30`, `shadoww/fm/bm 0.9/1.8/1.8`, `corpseSize 3.0`, `minWeight/maxWeight 60/200`, `minBlood/maxBlood
800/2000`, `trailerBaseSize 300`; alles andere (wild false, fleeZombies false, canBePicked false, ...) aus der Kopie. `:193` Avatar wie buck,
`:210` `AnimalPartsDefinitions.animals["ncbeargrownbrown"] = ["buckwhitetailed"]`. Name im Spiel `IGUI_AnimalType_ncbeargrown` = OBERFLAECHE.

**Formeln** `S:shared/BanditsNPCBearStats.lua`: `:235` `B.BodyWant` (Not-Aus / nicht zahm -> cub; s >= 0,75 -> big; s < 0,70 -> cub; dazwischen
rec.body), `:248` `B.BodySize` (big: `0,72 + (s - 0,75) x 0,63 / 0,6` geklemmt [0,72, 1,35], 3 Nachkommastellen; cub: min(s, 0,75)),
`:270` `B.BodyOf` (want, BodySize(want)), `:277` `B.BodyNow` (rec.body, sonst want), `:285` `B.BodyNum`, `:298` `B.BodyGap`,
`:355-356` `B.StatsOf` body/sz aus `B.BodyNow`, `want` neu (`:391`). `B.ApplySize` unveraendert (einzige Stelle setSizeForced/getData).

**Regeln** `S:shared/BanditsNPCBearRules.lua:474-475` gap/walkSpeed; `:504` `followNear + gap` / `followStart + gap`; `:529` `followGap + gap`;
`:534` Gehen gegen `walkSpeed` des Koerpers; `:617` `hideGap + c.gap`. Fehlen c.gap/c.walkSpeed: Zahlen wie B1c.

**Zeitaktionen** `S:shared/TimedActions/BanditsNPCBearPetAction.lua:54-64` `bigSizeY` (Groesse aus der Sicht, (sz - swapSize) /
(stageAt[3] - swapSize), geklemmt 0,01..1); `:66-94` `start()`: Sicht `bd == "big"` -> Haltung `petAnimBig` ("cow"), AnimalSizeY aus `v.sz`,
sonst wie B1d ("lamb", 0,5); SP-Marke `:90`. `:119` stop(), `:136` serverStart(), `:141` serverStop(), `:149` complete().
`.../BanditsNPCBearFeedAction.lua:65` start() (SP), `:89` stop(), `:106` serverStart(), `:111` serverStop(), `:119` complete().

**Welt** `S:server/BanditsNPCBearWorld.lua`: `:242-248` `B.SwapSpot(a, turn)`; `:466-470` `findBreed(body)`; `:474` `B.CubDefOk(body)`;
`:485-499` `B.CreateCub(x, y, z, body)` (Art je Koerper, Fehlerzeile je Art); `:519` `B.RemoveCub` und `:536` `B.FindAnimal` ueber
`B.BodyKind`; `:675` Suchlauf sieht beide Arten; `:757` AnimalID-Rueckfall setzt rec.body (nur tame/missing); `:892-896` Wegzeit mit
`B.BodyNum(rec.body, "runSpeed"/"walkSpeed", 1)`.

**Mitfahren / Call** `S:server/BanditsNPCBearRide.lua:72-92` `B.PlaceCub(rec, x, y, z, why, body)`: body gegeben -> genau dieser; nil ->
`B.BodyOf(rec)`; grosser Koerper ohne Definition -> vorher gefragt (`:82`, `B.CubDefOk("big")`), Junges + `ErrEvery("placebig", 600000)`;
`rec.body = want` (`:92`) VOR `B.Commit`. `:123` `B.RideBoard` prueft `B.CubDefOk("cub")`. Noten mit `B.NoteBd`: `:141` RideOn, `:236`
RideOff, `:317` Why_Riding, `:328` Why_CallWait, `:359` Called.

**Wachsen / Tausch** `S:server/BanditsNPCBearGrow.lua`: `:43` FIELDS + "body"; `:195-198` GrowFix (body nur cub/big); `:370` Sprungdeckel
mit `B.BodyNum(rec.body, "runSpeed", 2.47)`; `:424-438` Uhr-Helfer; `:443` `B.BodySwapReady` (state, ride, cool, retry, calm, guard, busy,
nodef); `:465` `B.BodyBusy` (Schleife <= 64); `:483` swapFail (Fehlerzeile ab 6. Versuch, je Minute); `:502-532` `B.BodySwap` (Kachel ->
BodyHp -> PlaceCub(want) -> RemoveCub(alt) -> Uhren -> faceThisObject -> Log); `:543-567` `B.GrowLive` (have/want, Tausch oder Groesse des
VORHANDENEN Koerpers, "swapdef"-Zeile je 10 min); `:611-616` `B.GrowBody` (rec.body = Koerper des Tiers); `:737` Sicht `t.bd`; `:771`
`B.GrowSetG` loescht swapAt/swapTryAt, Groesse nur am vorhandenen Koerper. Die B1d-Fehlerzeile "body swap is not built yet" ist weg.

**Heilung / Register / Server / Folgen / Wache**: `S:server/BanditsNPCBearHeal.lua:46` MARK_FIELDS + "body"; `:99-103` bind (rec.body =
Koerper des Tiers bei tame/missing, abweichender Spiegel nur B.Log); `:196-197` B.Restore -> nil "body" fuer grossen Koerper mit nicht
zahmem Spiegel; `:263` neuer Eintrag `body`. `S:server/BanditsNPCBearRegistry.lua:344-345`, `:379` B.RecOf. `S:server/BanditsNPCBearServer.lua:156`
handCheck. `S:server/BanditsNPCBearFollow.lua:118` (SetMode), `:140-145` (FollowStep c.gap/c.walkSpeed), `:232`, `:283`.
`S:server/BanditsNPCBearGuard.lua:306-307` GuardStep c.gap.

---

## 3. Engine-Aufrufe (jede Fundstelle selbst nachgelesen, 42.22.2)

| Aufruf (gleiche Argumenttypen) | Stelle im Kern | Beleg | Seite |
|---|---|---|---|
| `animal:getAnimalType()` | `shared/BanditsNPCBear.lua:499` (nur `B.BodyKind`) | `V:client/ISUI/Animal/ISAnimalUI.lua:65`; `V:shared/Definitions/animal/ButcheringUtil.lua:13` | beide |
| `AnimalDefinitions.getDef(Text)`, `def:getBreedByName(Text)` | `server/BanditsNPCBearWorld.lua:467`, `:469` | `V:server/ClientCommands.lua:808`; `ButcheringUtil.lua:79`, `:85` | Schreiber |
| `addAnimal(getCell(), x, y, z, Art-Text, Rasse, false)` + `animal:addToWorld()` | `World.lua:494`, `:499` (nur `B.CreateCub`; neu nur der Artname "ncbeargrown") | `V:server/ClientCommands.lua:809-810` (`args.type` = Text) | Schreiber |
| `animal:getSquare()` | `World.lua:244` (`B.SwapSpot`) | `V:shared/TimedActions/Animals/ISPetAnimal.lua:6` | Schreiber |
| `getX/getY/getZ` am Tier | `World.lua:246` | `ButcheringUtil.lua:575-577` | Schreiber |
| `animal:faceThisObject(Spieler)` | `server/BanditsNPCBearGrow.lua:523` (`B.BodySwap`) | `ISPetAnimal.lua:17` (`self.animal:faceThisObject(self.character)`) | SP belegt; am MP-Server Wirkung ungeprueft (nur Optik) |
| `character:setVariable("AnimalSizeY", Zahl)`, `("animal", Text)` | `shared/TimedActions/BanditsNPCBearPetAction.lua:83`, `:85` (neuer Wert "cow" bzw. Zahl aus der Sicht) | `ISPetAnimal.lua:32`, `:39` | Client / SP |
| `getTimestampMs()` | `Grow.lua:473` (`B.BodyBusy`) | `V:server/Foraging/forageServer.lua:456` | Schreiber |
| unveraendert benutzt: `remove()`, `removeAnimal(getOnlineID())`, `getBehavior():setBlockMovement`, `getData():getSize/setSizeForced`, `getHealth/setHealth`, `getAnimalID`, `isExistInTheWorld`, `isDead` | `B.RemoveCub`, `B.ApplySize`, `B.BodyHp`, `B.PlaceCub` ... | wie B1a-B1d (Kommentare an den Aufrufen) | wie dort |

**Jar-only-Aufrufe in B1e: keine.** Kevins zwei Ausnahmen (`pathToLocation`, `setVariable("animalRunning", ...)`) bleiben unveraendert
nur in `B.MoveTo`. Kein neues `pcall`. Nicht benutzt: `getForwardDirection`/`setDir` am Tier, `getData` ausserhalb `B.ApplySize`,
`BanditEventMarkerHandler` (Markierung = OBERFLAECHE).

---

## 4. SP- und MP-Zweig je Vorgang

| Vorgang | Einzelspieler (`not isServer() and not isClient()`) | Mehrspieler |
|---|---|---|
| Tausch (Hirn-Takt Schritt 7 -> `B.GrowLive` -> `B.BodySwap`) | im einen Programm; neuer Koerper per `addAnimal`, alter per `remove()` | NUR der Server (server/-Dateien kehren am Client zurueck); `removeAnimal(OnlineID)` nimmt die alte Kopie bei allen Clients; neue OnlineID geht mit der Sicht (Commit -> `B.FlushViews` / `pushNewSights`) |
| Groesse | `B.ApplySize` am Schreiber | Server setzt; Client-Probe in der Hud nur bei passender Art (`c.bd`, OBERFLAECHE) |
| Beschaeftigt-Marke | `start()` setzt, `stop()`/`complete()` loeschen | `serverStart()` am Server setzt, `serverStop()`/`complete()` loeschen; am Client fehlt `B.BodyBusy` (nil) -> nichts |
| Streichel-Haltung | `start()` aus `B.ViewOf` (Sicht direkt) | `start()` am Client aus der Server-Sicht (`bd`, `sz`); kein `getData` |
| Aussteigen / Call to me / Tod im Auto | `B.PlaceCub` -> `B.BodyOf` | dasselbe am Server; Bitte "Call" wie B1c (Besitz, Abklingzeit beim Schreiber) |
| Heilung (bind / Restore / Suchlauf) | Spiegel darf neuer sein (B1c B1) | Register gewinnt (B1c); grosser Koerper mit nicht zahmem Spiegel nie hergestellt |
| Noten mit `bd` | `B.ShowNote` direkt | `sendServerCommand(..., "Note", {..., bd = "big"})` (flaches Feld) |
| Folgen / Verstecken / Wegzeit | Schreiber | Server |

Kevins rote Linien: kein neuer Client-Befehl (kein Kick); nichts haengt (Beschaeftigt-Deckel 20 s, Neuversuch 10 s, Abklingzeit 60 s,
Fehlerzeilen gedrosselt); kein Gegenstand verloren/verdoppelt (Fuettern unveraendert; waehrend einer Aktion kein Tausch, und selbst danach
prueft `handCheck` vor `takeOne`); das Junge geht beim Tausch nie verloren und wird nie verdoppelt (neuer Koerper zuerst, dann der alte weg,
in EINEM Lua-Aufruf; Absturz-Faelle heilt der Suchlauf mit beiden Arten, Attrappe 12); keine NPC-Crew-Figur beruehrt.

---

## 5. Pruefer-Ausgaben (14 Kern-Dateien)

```
luacheck.py      14 file(s) checked, 0 failed
scopecheck.py    14 file(s), 0 violation(s)
localcount.py    hoechstens 39 aktiv (Server.lua brainTickBody :921) / 77 insgesamt (World.lua B.ScanAnimals :664); Grenze 200
luacheck_pz.py   0 Treffer (W113); --unused je Datei: 0 neue Treffer (3 alte aus B1c bleiben: Rules.lua:41 'base', Rules.lua:160 'slots',
                 Guard.lua:284 'players' -- im Vorher-Stand identisch)
luac5.1 -p       alle 17 shared/server-Dateien ohne Fehler
Zeilenenden      LF, ASCII (0 x CR, 0 Bytes > 127); Zeilen > 140 Zeichen nur die 9 alten
Trockenlauf      baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a (schreibt nichts): NICHT OK -- 4 Fehler, 26 Warnungen.
                 Tier-Regeln alle gruen (B.CreateCub nur in B.AppearFor/B.PlaceCub; addAnimal/addToWorld/remove/removeAnimal/setSizeForced/
                 getData/getHealth/setHealth je an EINER Stelle). Die 4 Fehler sind die geplanten ZUSAMMENBAU-Punkte (PLAN_B1E.md 10.3):
                 1 IGUI_AnimalType_ncbeargrown nicht im TEXT_NS, 2/3 Defs-Pruefung NCBear.png / NCBear_Body (Altlast bis B5a),
                 4 Cheat-Pruefung Defs.lua:159 "NCBear_Body" sieht aus wie ein Werkbank-Befehl -> braucht dieselbe "erlaubt"-Ausnahme wie
                 "NCBearCub_Body" (Defs.lua:81) -- steht so NICHT in 10.3, bitte im ZUSAMMENBAU ergaenzen.
```

---

## 6. Attrappen

| Lauf | Ergebnis |
|---|---|
| `attrappe/b1e_kern/run.lua` (**neu**, 22 Abschnitte nach PLAN_B1E.md 7.1) | **153 bestanden, 0 Fehler** (`b1e_kern/ergebnis.txt`) |
| `attrappe/kern/run.lua` | 136/0 (unveraendert) |
| `attrappe/b1b_kern/run.lua` | 204/0 (unveraendert) |
| `attrappe/b1c_kern/run.lua` | 192/0 (unveraendert) |
| `attrappe/b1d_kern/run.lua` | **162/0** (vorher 163/0, gewollt geaendert, unten) |
| `attrappe/gesamt/run.lua <neuer Kern + B1d-Client>` | **1173/0** (gleich wie vorher; Abschnitt 19 gewollt geaendert, unten) |
| `attrappe/gesamt/run.lua` (Staging, OBERFLAECHE noch im Bau) | bricht beim Laden ab: `client/ISUI/BanditsNPCBearMarker.lua:291: attempt to call method 'setWidth'` -- die UI-Attrappe der Gesamt-Attrappe kennt `setWidth` nicht (neue Markierung der OBERFLAECHE) -> ZUSAMMENBAU |
| `pruef_b`, `pruef_b1b` (run_nach), `pruef_b1c`, `pruef_b1d` | Ausgabe byte-gleich mit den gespeicherten Ergebnissen |

**Gewollte Aenderungen an bestehenden Attrappen (begruendet):**
1. `kern/attrappen.lua`: `AnimalDefinitions.getDef` kennt "ncbeargrown" (abschaltbar `A.noBigDef = true`, Fall "Definition fehlt");
   ein neuer grosser Koerper startet bei 0,72 (minSize, NUR JAR initSize), `getMinSize` je Art; `a:faceThisObject(o)` mit Zaehler
   (`faced`, `facedTo`). Rein ergaenzend -- alle alten Laeufe bleiben gleich.
2. `b1d_kern/run.lua`: prueft das B1d-Verhalten (Junges bleibt bei 0,75). Seit B1e ist das der Not-Aus `bodySwap = false`; eine
   `A.load`-Huelle setzt ihn nach jedem Laden. Fall 8 "bodySwap = true -> Fehlerzeile 'body swap is not built yet' (+ zweite nach 10 min)"
   entfaellt laut Plan 7.1 und ist ersetzt durch "bodySwap = true -> Tausch auf ncbeargrown, keine Fehlerzeile" (eine Pruefung weniger:
   163 -> 162). Ohne die Huelle liefen die B1d-Faelle 8, 13 und 15 in den Tausch (10 rote Pruefungen, alle "Junges bleibt 0,75").
3. `gesamt/run.lua` Abschnitt 19 (B1d): dieselbe Begruendung -- Lader `load19` / `saveLoad19` setzen `bodySwap = false` (4 + 3 Stellen nur
   in Abschnitt 19). Ohne das: 19b-19j rot (Junges 0,484/0,35 statt 0,75, Absturz in 19c am entfernten Jungen). Den Tausch im ganzen Ablauf
   prueft der ZUSAMMENBAU in "20 B1e" (mit der Vorgabe `bodySwap = true`).

**Neue Faelle (b1e_kern)**, u. a.: Helfer (alle 6 Arten), Schwelle (0,74/0,75/0,72/0,699, shy/fed, Not-Aus), Groesse (0,75 / 0,72 / 0,982 /
1,35, Klemme, 1000 Schritte nie fallend + 600 Schritte zu 0,001 streng steigend -- woertlich "streng in 1000 Schritten" geht mit 3
Nachkommastellen nicht), **Tausch hin** (genau ein `addAnimal` ncbeargrown DANN `remove()`, genau EIN lebender Koerper, id/u/owner/name/
mode/Heimat/tame/g/Erfahrung/hp gleich, gen+1, r+1, aid neu, body big, Groesse 0,72, `setHealth(rec.hp)`, Spiegel body/gen, swapAt, eine
Log-Zeile, keine Meldung, faceThisObject), **nicht sicher** (calm/guard/Zombie 5/busy/cool/retry/ride/state, Uhr rueckwaerts = abgelaufen),
**kein Flackern** (1000 Takte um g 0,15 +- 0,002 -> 1 Tausch), **zurueck** (GrowSetG 0 -> Junges 0,35 auch in swapMinMs; s 0,72 bleibt gross;
Not-Aus -> Junges), Definition fehlt (eine Zeile je 10 min, Aussteigen als Junges + placebig), Kachel (eigene / Ring / keine: 13 Fehlversuche,
Zeile beim 6. und 12.), offener Schaden, Mitfahren 2 Spieltage -> steigt gross aus, Call to me (will gross, hat Junges) -> gross, Tod im Auto,
**Speichern/Laden** (gross bleibt gross; B1d-Stand tauscht beim ersten Takt), **Absturz-Faelle 4.3 alle sechs**, Suchlauf (bear/bearstag/
ncbearcubalt nie angefasst, grosse Waise entfernt), RecOf, Regeln (3,5 / 5,0 / 2,5 / Gehen bis 0,67 / Versteck 2,0), Tempo (10/3,17+1,5 s;
Kondition-Sprungdeckel 3,17), Sicht (bd big, sz 1,035, neue oid; wartendes Junges bd cub 0,75; wild ohne bd), Noten (11 Schluessel mit bd,
Note_Grown ohne), **Beschaeftigt-Marke** (echte Zeitaktions-Dateien mit Stub-Basisklasse: serverStart/complete/serverStop, SP start/stop,
Deckel 20 s, MP-Client ohne B.BodyBusy), Streich-Haltung (cow 0,5 / lamb 0,5, kein getData), MP-Rundlauf (Tausch nur am Server,
`removeAnimal` der alten OnlineID, Sichten von A und B mit bd big + neuer oid, B fuettert nicht, A offline -> g steht, kein c2s; B1d-Fall
tauscht auch ohne A), Dateiregeln (CreateCub/addAnimal/setSizeForced/getData/getHealth/setHealth/getAnimalType/faceThisObject je an EINER
Stelle; kein `"bear"` als Art -- einzige Ausnahme die Gruppe in `Crew.lua` NOT_TENDED aus B1a; kein next(, %a, spawn/debug/bench/cheat).
Erwartete Fehlerzeilen des Laufs: 7 (Definition fehlt, 3), 8 (keine Kachel, 2), 12 (Heilungen, 3).

---

## 7. Offen / ungeprueft (Testpunkte, nichts davon ist gespielt)

1. `setSizeForced` direkt nach `addToWorld`: mit `minSize = 0,72` steht ein frischer grosser Koerper ohnehin bei 0,72 (NUR JAR); die Attrappe
   bildet das so ab -- bei genau s 0,75 schreibt `B.ApplySize` deshalb gar nicht (Plan 7.1.4 nennt "setSizeForced(0.72)"; geprueft ist "Groesse
   0,72", bei s 0,8 ist das Schreiben 0,773 geprueft).
2. Ob `isFree(false)` die eigene Kachel eines Tiers als belegt meldet (dann Tausch eine Kachel daneben).
3. `faceThisObject` am Tier am MP-Server und an einem Tier im selben Bild nach `addToWorld` (nur Optik).
4. MP: Reihenfolge `addAnimal`/`removeAnimal` bei den Clients (evtl. ein Bild zwei Koerper, F12); `getAnimalID`/`getObjectListForLua` am
   Server (A3 seit B1a); im Tausch-Takt hat die Sicht evtl. einen Takt lang oid -1 (das neue Tier ist erst im naechsten Bild "in der Welt"),
   der naechste Takt schickt sie neu (`pushNewSights`).
5. Laerm-Ersatzweg `B.CalmAnswer` (Guard.lua :124-127) rechnet ohne Abstand-Zuschlag (nicht in Plan 6.3; Kleinigkeit, schnittstelle Punkt 9).
6. Im Spiel ansehen: Sprung beim Wechsel (F1), Fussgleiten (F6), Folgen-/Versteck-Abstaende, Kollision 0,30 (F10), Kuh-Haltung (F4),
   Blick zum Besitzer (F5), Verhalten des grossen Modells mit animset buck unter der neuen Art (dasselbe Modell spielt seit 2c als "bear").
7. ZUSAMMENBAU: altes Junges ins Staging (10.1), Uebernahme-Skript (10.3 + Ausnahme "NCBear_Body" in der Cheat-Pruefung, Abschnitt 5),
   gesamt-Attrappe "20 B1e" und UI-Stub `setWidth` fuer die neue Markierung.

## 8. Fragen fuer Kevin

Keine neuen aus dem Kern-Bau; es gelten PLAN_B1E.md 11 F1-F14 (gebaut ist je die Empfehlung: Wechsel bei 0,72, Art `ncbeargrown`, Texte
"bear", Kuh-Haltung, Blick zum Besitzer, Schwelle 0,70/0,75, Verstecken weiter wie das Junge). Nach dem Einbau muss Kevin das Spiel NEU
starten (neue Tierart und Lua laden nur beim Start).

Statisch geprueft, nicht gespielt.
