# Lauf baer-b1e: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung

Stand 11.11.2026 abends. **Statisch geprueft, nicht gespielt.** Rolle Pruefer B: nichts im Staging, in der Test-Mod, in NPC Crew,
Vanilla oder Bandits geaendert; geschrieben nur dieser Bericht und die eigene Attrappe `attrappe/pruef_b1e/` (`run.lua`, `ergebnis.txt`).
Kein git, kein Spielstart, kein Download.

Kurzformen: `S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`, `V:` = Vanilla `media/lua/` (42.22.2), `B:` = Bandits 42.22 `media/lua/`,
`FE` = `forschung_b1e.md`, `PE` = `PLAN_B1E.md`.

Gelesen (ganz bzw. jede B1e-Stelle): `S:server/BanditsNPCBearGrow.lua` (Tausch, Bereitschaft, Beschaeftigt, GrowLive/Body/SetG/View),
`S:server/BanditsNPCBearRide.lua` (ganz), `S:server/BanditsNPCBearWorld.lua` (Kacheln, Erzeugen/Entfernen/Finden, Suchlauf, MoveTo),
`S:server/BanditsNPCBearServer.lua` (handCheck, liveRec, resolve, brainTickBody), `S:server/BanditsNPCBearHeal.lua` (Spiegel, bind,
Restore, HealFromMark), `S:server/BanditsNPCBearRegistry.lua` (RecOf, viewEntry, Close), `S:server/BanditsNPCBearGuard.lua`,
`S:server/BanditsNPCBearFollow.lua`, `S:shared/BanditsNPCBear.lua` (CFG, BodyKind, NoteBd, ViewOf), `S:shared/BanditsNPCBearStats.lua`,
`S:shared/BanditsNPCBearDefs.lua`, `S:shared/BanditsNPCBearRules.lua` (FollowDecide, GuardDecide), beide Zeitaktionen,
`S:client/ISUI/BanditsNPCBearMarker.lua` (ganz), `S:client/ISUI/BanditsNPCBearHud.lua` (Suchlauf, Schild, Probe),
`S:client/BanditsNPCBearMenu.lua`, `S:client/BanditsNPCBearOptions.lua`, `S:client/BanditsNPCBearClient.lua` (TB/NoteText/CubName),
`S:client/NCBearBenchCub.lua` (Grow/Stats/Clean). Dazu FE, PE, `bau_b1e_kern.md`, `schnittstelle_aenderungen.md` (B1e-Abschnitte),
`mess_b1e/ausgabe.txt`, `baer/spiel/tier_spez.md` 2.8, `baer/spiel/bau_lebend.md`, `baer/spiel/baby_fix_baby.md` M5.

---

## 0. Urteil

**Kein Blocker, kein Major.** In keinem geprueften Zustand geht das Tier beim Tausch verloren oder entsteht als zweiter GEBUNDENER Koerper;
der Eintrag bleibt derselbe. Die Schwelle flackert nicht (Hysterese 0,70/0,75 plus Abklingzeit, 3000-Takte-Last P3). Die Groessen-Abbildung
stimmt nachgerechnet mit FE 4.3 und Kevins Tabelle. Jede Art-Frage laeuft ueber `B.BodyKind` (grep: kein `getAnimalType() ==/~=` und kein
`== B.CUB` mehr ausserhalb, nur die Existenz-Riegel `not B.CUB` im Menue). Kosten je Bild klein. Sieben kleine Befunde (B1-B7), alle
"minor": ein Ein-Bild-Fenster mit sichtbarer Kopie (B1), ein kurzer Halt beim Tausch im Lauf (B2), zwei Rechenfehler nur in Kommentaren/Plan
(B3), eine Fuetter-Haltung (B4), zwei Abstaende ohne Koerperlaenge (B5), Rest-Texte "cub" (B6), Klickflaeche der Markierung (B7).

Nachgelaufen (unveraendert gruen): `attrappe/b1e_kern/run.lua` **153/0**, `attrappe/gesamt/run.lua` **1672/0**; Pruefer auf 25 Lua-Dateien:
luacheck 0 failed, scopecheck 0 violations, localcount hoechstens 49 aktiv (Hud) / 77 insgesamt (World `B.ScanAnimals`), luacheck_pz nur die
bekannten Globalen (Zeitaktions-Klassen, Bench-Befehle). Eigene Attrappe `attrappe/pruef_b1e/run.lua`: **25/0** (Abschnitt 9).

---

## 1. Tausch hin und zurueck je Zustand

| Zustand | was passiert | Fundstelle | Urteil |
|---|---|---|---|
| folgt (Laufbefehl aktiv) | Tausch NICHT gesperrt; neuer Koerper steht auf der Kachel des alten, Sitzung leer (`ownUntil`, `f`), naechster Takt neuer Laufbefehl | `S:server/BanditsNPCBearGrow.lua:443-459` (kein `ownUntil`), `S:server/BanditsNPCBearRide.lua:54-58` | kein Verlust; sichtbarer Halt bis 1,5 s -> **B2** |
| bleibt / haelt | Sperre am alten geloest (`RemoveCub` `setBlockMovement(false)`), neuer frei, naechster Takt haelt wieder | `S:server/BanditsNPCBearWorld.lua:517-524`, `S:server/BanditsNPCBearRide.lua:55` | ok |
| versteckt (Zombie) | `s.g.on` oder Zombie < `zedSafe` 9 -> "guard", kein Tausch | `S:server/BanditsNPCBearGrow.lua:451-454` | ok (P3, kern 5) |
| flieht vor Laerm | Ruhefrist `calmUntil` (2,5 s) -> "calm"; danach darf getauscht werden, der Ersatzweg endet (neuer Koerper hat Stress 0, flieht nicht) | `S:server/BanditsNPCBearGrow.lua:450`, `S:server/BanditsNPCBearGuard.lua:145` | ok |
| faehrt mit | kein Koerper -> "ride"; Aussteigen/Tod im Auto erzeugt `B.BodyOf(rec)` | `S:server/BanditsNPCBearGrow.lua:445`, `S:server/BanditsNPCBearRide.lua:74-79`, `:194`, `:228` | ok (kern 10) |
| Call to me | ein Lua-Aufruf, erzeugt `B.BodyOf`, entfernt den alten (jede Art) | `S:server/BanditsNPCBearRide.lua:337-356` | ok; Ein-Bild-Fenster direkt nach einem Tausch -> **B1** |
| gefuettert / gestreichelt | Beschaeftigt-Marke (SP `start`, MP `serverStart`), geloescht in `complete/stop/serverStop`, Deckel `busyMs` 20 s; selbst ohne Marke nimmt `handCheck` VOR `takeOne` nichts | `S:server/BanditsNPCBearGrow.lua:455`, `:465-481`; `S:shared/TimedActions/BanditsNPCBearFeedAction.lua:65`, `:89`, `:106-121`; `S:server/BanditsNPCBearServer.lua:154-173` | ok, kein Gegenstand verloren/verdoppelt |
| Besitzer offline (MP) | `g` steht (GrowSlow nur online); Tausch nur fuer einen B1d-Stand, wenn ein anderer Spieler die Gegend laedt; kein `faceThisObject` | `S:server/BanditsNPCBearGrow.lua:575-577`, `:520-524` | ok (kern 21) |
| zweiter Spieler | sieht den Server-Tausch (`removeAnimal(OnlineID)` + neues Tier), Sicht `bd big` + neue OnlineID; Fuettern `Why_NotOwner` | `S:server/BanditsNPCBearWorld.lua:521-523`, `S:server/BanditsNPCBearRegistry.lua:563-569` | ok (kern 21) |
| Speichern / Laden | Register traegt `body`, die Engine die Art (Klemme [0,72; 1,35]); `bind` setzt `body` aus dem Tier | `S:server/BanditsNPCBearHeal.lua:96-103`, `S:shared/BanditsNPCBearDefs.lua:173-174` | ok (kern 11) |
| Absturz mitten im Tausch | EIN Lua-Aufruf (`PlaceCub` -> Commit -> Spiegel -> `RemoveCub`), dazwischen speichert die Welt nicht; Mischstaende heilt der Suchlauf beider Arten | `S:server/BanditsNPCBearGrow.lua:502-531`, `S:server/BanditsNPCBearWorld.lua:675`, `:757` | ok (kern 12, P2) |
| Register leer + Spiegel | `B.Restore` am grossen Koerper -> `body big`; ein grosser Koerper mit Spiegel new/shy/fed nie hergestellt, nie "found" | `S:server/BanditsNPCBearHeal.lua:196-197`, `:263`; `S:server/BanditsNPCBearRegistry.lua:379` | ok; MP-Deckel -> sofort zurueck zum Jungen (P2), immer ein gebundener Koerper |
| Bench `NCBear_CubGrow(-100)` | `B.GrowSetG` loescht Abklingzeiten -> `B.BrainTick(true)` -> "shrink" | `S:server/BanditsNPCBearGrow.lua:763-780`, `S:client/NCBearBenchCub.lua:862-876` | ok (kern 6, P3) |
| Not-Aus `bodySwap = false` | `B.BodyWant` immer "cub" -> grosser Koerper wird Junges | `S:shared/BanditsNPCBearStats.lua:235-245` | ok (P3) |
| B1d-Spielstand (Junges > 0,75) | `rec.body` fehlt -> beim Binden/ersten GrowLive "cub" -> erster sicherer Takt tauscht | `S:server/BanditsNPCBearGrow.lua:547-548` | ok (kern 11) |

**Verlust / Doppel -- warum es haelt:** Reihenfolge neuer Koerper ZUERST (`B.PlaceCub`: `gen + 1`, `aid`, `rec.body`, `B.Commit`, Spiegel
sofort), DANN `B.RemoveCub(alt)` (`S:server/BanditsNPCBearGrow.lua:513-515`); misslingt `PlaceCub`, bleibt der alte unberuehrt
(`swapFail`, `:483-491`). Eine veraltete Kopie (kleinere `gen`) wird nie gebunden (`S:server/BanditsNPCBearHeal.lua` HealFromMark "stale")
und nur unbeobachtet entfernt (`dropCopy`, `S:server/BanditsNPCBearWorld.lua`), Waisen nach den B1b-Riegeln -- jetzt fuer beide Arten
(`:675`). Fremde Tiere (`bear`, `bearstag`, `ncbearcubalt`) fasst `B.RemoveCub` nie an (`:519`), P3 bestaetigt (nie entfernt, nie gestempelt).

**Engine-Fenster (eigene Attrappe P1a):** ein neues Tier ist erst im naechsten Bild in der Welt (`S:server/BanditsNPCBearWorld.lua:500-505`,
Kevins Test 10.11.). Nach dem Tausch steht im selben Bild KEIN Koerper sichtbar und `B.FindAnimal` gibt nil -- harmlos, weil der Tausch der
letzte Schritt des Hirn-Takts ist (`S:server/BanditsNPCBearServer.lua:1012-1026`); nach dem Bildwechsel genau EIN gebundener Koerper,
`missN` bleibt 0, kein weiteres `addAnimal`.

---

## 2. Flackern an der Schwelle

`B.BodyWant` (`S:shared/BanditsNPCBearStats.lua:235-245`): hin bei innerer Groesse s >= 0,75 (minus 1e-6, gleiche Toleranz wie
`B.StageOf` -> Tausch und Meldung "half-grown" an derselben Schwelle), zurueck erst bei s < 0,70, dazwischen der Koerper, den der Eintrag hat.
Dazu `swapMinMs` 60 s und `swapRetryMs` 10 s je Eintrag (`S:server/BanditsNPCBearGrow.lua:448-449`; Uhr rueckwaerts = abgelaufen).
`g` waechst sonst nur (GrowSlow, Fuettern, Spiegel "newer" = Maximum); sinken kann es nur ueber Bench, MP-Deckel beim Wiederherstellen oder
eine geaenderte Sandbox-Tageszahl -- jeweils EIN Wechsel, kein Pendeln.
**P3 (3000 Takte):** g pendelt erst um 0,15 (s 0,734..0,766), dann um 0,1313 (s 0,692..0,708), dazu zufaellig Laerm (4 %), Fuettern
(2 %, teils nie beendet), Zombie, keine Kachel, Uhr 30 s rueckwaerts; Not-Aus und Bench dazwischen: **genau 7 Tausche wie erwartet**, keiner
gegen eine Sperre, Abklingzeit eingehalten, je Takt genau ein gebundener Koerper, `addAnimal`-Zahl == Tausch-Zahl, laengste Wartezeit 2 Takte.

---

## 3. Groessen-Abbildung nachgerechnet

Gemessen (`mess_b1e/ausgabe.txt`, Spiel-Importer, Idle Bild 0, Groesse 1,0): Junges L 0,9966 E / Oberkante 0,5894 E; grosser Baer L 1,0448 E /
Oberkante 0,6254 E. Beide model-Skripte ohne `scale` (NCBearTest `media/scripts/nc_bear_tier.txt`, `S:../scripts/nc_bear_cub.txt`) -> die
Dump-Masse gelten im Spiel 1:1.

| Pruefung | Rechnung | Ergebnis |
|---|---|---|
| Tausch 0,72 gegen Junges 0,75 | L 1,0448 x 0,72 / (0,9966 x 0,75) = 1,0064; Oberkante 0,6254 x 0,72 / (0,5894 x 0,75) = 1,0186 | +0,6 % / +1,9 % = FE 4.3 |
| Abbildung `S:shared/BanditsNPCBearStats.lua:248-265` | 0,72 + (s - 0,75) x 0,63 / 0,60 = 0,72 + 1,05 (s - 0,75), geklemmt [0,72; 1,35], 3 Stellen | Tag 15 0,720 / Tag 45 0,982(5) / Tag 100 **1,350** |
| Tag 100 = Erwachsener bei 1,35 | gleiches Netz NCBear.glb, gleiche Groesse -> L 1,0448 x 1,35 / 0,544 = 2,59 m, Oberkante 0,6254 x 1,35 / 0,544 = 1,55 m | = Kevins Tabelle (ENT: 1,55 m Schulter) |
| Definition | `minSize 0.72` = `swapSize 0.72`, `maxSize 1.35` (`S:shared/BanditsNPCBearDefs.lua:173-174`, `S:shared/BanditsNPCBear.lua:116`) | passt; frischer Koerper steht ohne Setzen bei 0,72 |
| Schild-Faktor | 0,6254 / 0,5894 = 1,061 -> `tagBigK 1.06`; Tag 100: 1,35 / 0,35 x 1,06 = 4,09 < `ZK_MAX` 5 | ok (`S:client/ISUI/BanditsNPCBearHud.lua:376-384`) |
| Abstand-Zuschlag | (1,0448 x sz x 1,5 - 1,12) / 2: Tag 30 0,107 / Tag 45 **0,210** / Tag 60 0,288 / Tag 100 0,498 | Code richtig; Kommentar/Plan sagen fuer Tag 45 "0,27" -> **B3** |
| Tempo | 0,3784 E / 0,9 s x 1,6 = 0,673; 1,0578 / 0,5333 x 1,6 = 3,173 Kacheln/s (Umrechnung `baer/spiel/tier_spez.md` 2.8: E/s x MotionScale 1,6) | `walkSpeedBig 0.67`, `runSpeedBig 3.17` richtig; Plan schreibt "x 1,6 x 1,5" -> **B3** |

Werte (Leben, Traglast ...) rechnen weiter mit s (`B.StatsOf`), unveraendert. Gesetzt wird nur ueber `B.ApplySize` und nur am passenden
Koerper (`S:server/BanditsNPCBearGrow.lua:560`, `:615`, `:775`; MP-Client-Probe nur bei `B.BodyKind(obj) == (c.bd or "cub")`,
`S:client/ISUI/BanditsNPCBearHud.lua:474`).

---

## 4. Erkennt jede Stelle beide Koerper? (Liste FE 2 abgehakt)

| FE # | Stelle | heute | Urteil |
|---|---|---|---|
| 1 | Konstanten | `S:shared/BanditsNPCBear.lua:33-36` `B.BIG`, `B.BODY_TYPE`, `B.TYPE_BODY` (nie bear/bearstag/ncbearcubalt) | ok |
| 2 | `B.ViewOf` | `S:shared/BanditsNPCBear.lua:514-516` ueber `B.BodyKind` (Menue, Hud, `U.CubObj`, Karte, Streicheln) | ok |
| 3 | `handCheck` | `S:server/BanditsNPCBearServer.lua:156` | ok |
| 4 | `B.RecOf` | `S:server/BanditsNPCBearRegistry.lua` `B.RecOf` (BodyKind; grosser Koerper nie "found", `:379`) | ok (kern 14) |
| 5/6/7 | `findBreed`/`B.CubDefOk`/`B.CreateCub` | `S:server/BanditsNPCBearWorld.lua:466-470`, `:474`, `:485-506` (Art je Koerper, Vorgabe Junges) | ok |
| 8/9/10 | `RemoveCub`/`FindAnimal`/`ScanAnimals` | `:519`, `:536`, `:675`, AnimalID-Rueckfall setzt `body` `:757` | ok |
| 11 | `B.RideBoard` | `S:server/BanditsNPCBearRide.lua:123` `CubDefOk("cub")` (Rueckfall-Koerper) | ok |
| 12 | Menue | `S:client/BanditsNPCBearMenu.lua:320-327` | ok |
| 13 | Hud-Suchlauf | `S:client/ISUI/BanditsNPCBearHud.lua:249-258` | ok |
| 14 | Bench | `S:client/NCBearBenchCub.lua:405`, `:646-652` | ok (nur SP: `:78-81`) |
| 15/16/21 | Tausch/BodyOf/Groesse | `S:server/BanditsNPCBearGrow.lua:543-567`, `S:shared/BanditsNPCBearStats.lua:270-273` | ok |
| 17 | `rec.kind` | bleibt "cub" (Eintrag-Art), Koerper in `rec.body` | ok |
| 18/19 | Definition, `IGUI_AnimalType_ncbeargrown` | `S:shared/BanditsNPCBearDefs.lua:146-211`; IG_UI x 7 je 1 Treffer | ok |
| 20 | MP-Groessen-Probe | `S:client/ISUI/BanditsNPCBearHud.lua:459`, `:474` | ok |
| -- | indirekt (Laerm-Wache, Zombie-Wache, Folgen, MoveTo, Hold, RideStep, markProbe, BodyHp, Zeitaktionen, Karte, Markierung) | bekommen das Objekt; mit 9/10 fuer beide | ok |
| -- | Schild/Texte | `U.TB`/`U.NoteText`/`U.CubName` (`S:client/BanditsNPCBearClient.lua:257-262`, `:309-326`); Rest-Texte -> **B6** | ok |

Wilde Junge wachsen und tauschen nie: `B.BodyWant` "cub" fuer jeden Zustand ausser tame/missing (`S:shared/BanditsNPCBearStats.lua:238`),
`B.GrowLive` nur tame (`S:server/BanditsNPCBearGrow.lua:544`), GrowSlow nur tame (`:576`). Alte Art "bear": `B.BodyKind` nil -> nie
angefasst. NPC Crew: `NC:client/BanditsNPCPortrait.lua:324` liest `AnimalAvatarDefinition[getAnimalType()]` -- fuer `ncbeargrown` angelegt
(`S:shared/BanditsNPCBearDefs.lua:192-206`). Kollisionsprobe `ncbeargrown` nachgezogen: 0 Treffer in NPC Crew `42/media/lua` +
`landkarte_index.txt`, Vanilla `media/lua` + `media/scripts`, Bandits 42.22 + common, Test-Mod `42/media`.

---

## 5. Tempo und Fussgleiten

Tempo kommt nur aus dem Clip; `buck` hat keinen Tempo-Regler (FE 4.4) -- kein Lua-Hebel, ehrlich als F6 "im Spiel ansehen" gemeldet.
Gleiten = gezeigte Groesse - 1 (beide Clips sind bei Groesse 1,0 gleitfrei gebaut: Baer `bau_lebend.md` "Clip-Weg = Stuetzweg / 1,0667",
Junges `baby_fix_baby.md` M5 Weg x 0,777 = Beinfaktor): nach dem Tausch -28 % (wie das Junge davor), um Tag 47 null, Tag 100 +35 %.
Stellwerte je Koerper sind richtig verdrahtet: Gehen-Regel `c.walkSpeed` (`S:server/BanditsNPCBearFollow.lua:139-145`,
`S:shared/BanditsNPCBearRules.lua:474-475`, `:534`), Wegzeit `ownUntil` (`S:server/BanditsNPCBearWorld.lua:892-896`), Kondition-Sprungdeckel
(`S:server/BanditsNPCBearGrow.lua:370`). Abstaende mit Koerperlaenge auf followNear/Start/Gap und hideGap (`Rules.lua:504`, `:529`, `:617`);
NICHT auf dem Laerm-Ersatzweg und dem Heranlocken -> **B5**. Fuetter-Haltung der neuen Art -> **B4**.

---

## 6. Kosten je Bild

| Was | Kosten | Urteil |
|---|---|---|
| Markierung `Mk:render` | nur sichtbar: 3 x `drawTextureScaled`/`DrawTextureAngle` + 1 Text, nur Felder (`S:client/ISUI/BanditsNPCBearMarker.lua:153-170`) | billig |
| Markierung Takt | je Bild 1 `getTimestampMs` + Vergleich; je 400 ms Ziel/Winkel/Abstand (`:346-373`); Lage nur bei Einblenden/Option/Aufloesung | billig |
| Schreiber je Hirn-Takt | je geladenem zahmen Baeren 1 `getAnimalType` + Lua; wartet ein Tausch: dazu `getDef`+`getBreedByName` (`B.CubDefOk`) | billig |
| Tausch | selten (Abklingzeit 60 s, Neuversuch 10 s) | ok |
| Beschaeftigt-Marke | je Aktions-Start/-Ende Schleife <= 64 | ok |
| Suchlauf / Hud-Suchlauf | wie B1d (je Tier 1 `getAnimalType`) | unveraendert |
| Deckel | `M.shyAt`/`M.gone` 16, ein UI-Element je Spielstart, ErrEvery-Schluessel je Kennung | ok |

---

## 7. SP- und MP-Zweig

| Teil | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Tausch | im einen Programm (`server/` laeuft im SP, `S:server/BanditsNPCBearGrow.lua:1`) | nur Server; `removeAnimal(OnlineID)` (`S:server/BanditsNPCBearWorld.lua:521-523`); Sicht mit `bd` + neuer OnlineID im naechsten Takt (`pushNewSights`) |
| Beschaeftigt | `start()` setzt (`FeedAction.lua:65`, `PetAction.lua:90`), `stop/complete` loeschen | `serverStart/serverStop/complete` am Server; am Client fehlt `B.BodyBusy` -> nichts |
| Streichel-Haltung | Sicht direkt (`B.ViewOf`) | Server-Sicht `bd/sz`; kein `getData` |
| Groesse | `B.ApplySize` am Schreiber | Server + Client-Probe nur an passender Art |
| Markierung / Optionen | Client | Client, nur Spieler 1 |
| Bench | nur SP (`S:client/NCBearBenchCub.lua:78-81`) | "singleplayer only" |
| Kick / AntiCheat | kein neuer `sendClientCommand` (kern 21 zaehlt c2s = 0) | ok |

Eiserne Regel, Stichprobe der neuen Aufrufe (Vanilla-Zeile gelesen): `animal:getSquare()` `V:shared/TimedActions/Animals/ISPetAnimal.lua:6`,
`animal:faceThisObject(Spieler)` `:17`, `drawTextureScaled(9 Argumente)` `V:client/Chat/ISChat.lua:418`, `DrawTextureAngle` `V:client/Fishing/TensionUI.lua:21`,
`ISUIElement.new(self, ...)` `V:client/ISUI/ISUISprite.lua:71`, `setX/setY` `V:client/ISUI/ISToolTip.lua:78-79`, `OnResolutionChange`
`V:client/ISUI/PlayerData/ISPlayerData.lua:206`, `getScreenHeight` `V:client/Chat/ISChat.lua:1167`, `setVisible` `V:client/Chat/ISAlert.lua:55`,
`onMouseDoubleClick` `V:client/ISUI/ISButton.lua:66` -- alle mit gleichen Argumenttypen. Kein neues `pcall`. Pfeil-Winkel: Bandits rechnet
deg(atan2) + 180 + 270 + 45 = deg(atan2) + 135 (`B:client/BanditEventMarkers.lua:118-121`), unser `markerAngleAdd 135` ist dieselbe Formel.

---

## 8. Markierung (Punkt 7) -- Logik

Ziel/Zeiten unveraendert (`target`, `S:client/ISUI/BanditsNPCBearMarker.lua:302-328`), Bandits wird nur noch gelesen (Riegel `:201`, `:218-219`),
laeuft ohne Bandits. Faktor: Kevins 2054 px -> 1,90 -> naechste Stufe 2,0 (192 px Pfeil, Kreis 192 px, Schrift Large); 1080 -> 1,0; 1440 -> 1,25.
Option Index 1 Auto / 2..7 feste Stufen (`:108-123`, `S:client/BanditsNPCBearOptions.lua:84-91`), Lesen ueber `U.Opt` (1 s Zwischenspeicher).
Genau ein Element je Spielstart (`:397-417`). Klickflaeche -> **B7**.

---

## 9. Eigene Attrappe `attrappe/pruef_b1e/run.lua` (25 bestanden, 0 Fehler; `ergebnis.txt`)

Nutzt `attrappe/kern/attrappen.lua` unveraendert; bildet zusaetzlich nach, dass `addToWorld` erst mit dem naechsten Bild wirkt (`frame()`).

| Fall | Was | Ergebnis |
|---|---|---|
| **P1a** Engine-Takt | Tausch im Hirn-Takt, Bildwechsel, 8 Takte | 1 Bild lang 0 Koerper sichtbar (erwartet), danach genau EIN gebundener grosser Koerper, `missN` 0, kein weiteres `addAnimal` |
| **P1b** Call im selben Bild | Tausch, im SELBEN Bild "Call to me" | gebunden ist der Call-Koerper, aber der Tausch-Koerper (gen kleiner) steht als **zweiter grosser Baer** in der Welt; bleibt, solange der Besitzer naeher als `vanishKeep` 25 ist; `B.ViewOf(Kopie)` = `b1` (Schild/Menue koennen an der Kopie haengen); `B.RecOf(Kopie)` = nil "stale" (Fuettern nimmt nichts); Besitzer weg + Waisen-Suchlauf (<= 120 s) -> entfernt -> **B1** |
| **P2** Register leer + beide Koerper + MP-Deckel | grosser Koerper (gen N+1) und altes Junges (gen N) in der Zelle, Register geloescht, MP | ein Eintrag (kein "found"), Wiederherstellen am grossen Koerper, Deckel g 0,10 -> s 0,617 -> naechster Takt Tausch zurueck: gebunden ein NEUES Junges (gen N+2), grosser entfernt (`removeAnimal`), altes Junges ungebunden bis unbeobachtet; SP: grosser Koerper hergestellt, kein Tausch |
| **P3** Schwelle unter Last | 3000 Takte, Pendeln um 0,75 und um 0,70, zufaellige Sperren, Uhr rueckwaerts, Not-Aus, Bench | genau 7 Tausche (erwartet), nie gegen Sperre, Abklingzeit gehalten, je Takt genau ein gebundener Koerper, fremde Tiere unberuehrt |

---

## 10. Befunde

| id | Schwere | Datei:Zeile | Behauptung | Vorschlag |
|---|---|---|---|---|
| B1 | minor | `S:server/BanditsNPCBearRide.lua:337-356` | "Call to me" im selben Bild wie ein Tausch erzeugt einen DRITTEN Koerper: `B.FindAnimal` findet den eben erzeugten Tausch-Koerper noch nicht (nicht in der Welt, `S:server/BanditsNPCBearWorld.lua:535`), also wird er nicht entfernt; er steht danach als ungebundene grosse Kopie da, bis der Besitzer > 25 Kacheln weg ist. Kein Verlust, kein zweiter Eintrag, Fuettern nimmt nichts; Schild/Menue koennen an der Kopie haengen (SP-`B.ViewOf` liest den Spiegel). Fenster = 1 Bild (gilt seit B1c auch fuer Aussteigen + Call). Beleg: Attrappe P1b. | In `B.PlaceCub` `s.placedAt = getTimestampMs()` merken; `B.HandleCall` lehnt in den ersten ~2 s danach ab (`Why_CallWait` mit 1 min oder still). Kein Engine-Aufruf noetig. NICHT pauschal "Objekt der Sitzung nicht in der Welt -> ablehnen" (dann ginge Call bei einem in entladener Gegend steckenden Baeren nie). |
| B2 | minor | `S:server/BanditsNPCBearGrow.lua:443-459` | Ein laufender eigener Laufbefehl (Folgen rennend, `s.ownUntil`) sperrt den Tausch nicht; `clearBodySession` loescht ihn (`S:server/BanditsNPCBearRide.lua:56`). Folge: der rennende Baer steht nach dem Tausch bis zum naechsten Hirn-Takt (<= 1,5 s) auf der Kachelmitte des alten. Kein Verlust. Auftrag 1 "kein Tausch waehrend ... anderer laufender Vorgaenge" ist hier eng ausgelegt. | Weiche Sperre "move" (`ms < s.ownUntil` und `s.walk == false`) mit Hoechstwartezeit (z. B. 10 s seit dem ersten "want ~= have", sonst tauscht er doch) -- oder als "im Spiel ansehen" lassen. |
| B3 | minor | `S:shared/BanditsNPCBearStats.lua:297`; `PLAN_B1E.md:178`, `:183`, `:279` | Zwei Rechenfehler NUR in Text: Abstand-Zuschlag Tag 45 ist 0,21 (1,0448 x 0,9825 x 1,5 - 1,12) / 2), nicht "0,27"; Tempo ist "Clip-Weg / Dauer x 1,6" (`baer/spiel/tier_spez.md` 2.8, `mess_b1e/ausgabe.txt`), nicht "x 1,6 x 1,5". Zahlen im Code (0,67 / 3,17, Formel) stimmen. | Kommentar `Stats.lua:297` auf "~0,21" und Plan-Texte berichtigen (Nachbesserung, kein Code). |
| B4 | minor | `S:shared/BanditsNPCBearDefs.lua:156-186` (Kopie, `feedByHandAnim` aus `:111`) | Der grosse Koerper erbt `feedByHandAnim = "AnimalLureLow"` vom Jungen; bei Schulterhoehe 0,83-1,55 m nutzt Vanilla fuer grosse Tiere "AnimalLureHigh" (Kuh `V:shared/Definitions/animal/CowDefinitions.lua:245`, Hirschkuh `DeerDefinitions.lua:137`). Die Fuetter-Aktion spielt `a:getFeedByHandAnim()` (`S:shared/TimedActions/BanditsNPCBearFeedAction.lua:55`) -> Figur bueckt sich vor einem 1,5-m-Baeren. Nur Optik, ungespielt. | `d.feedByHandAnim = "AnimalLureHigh"` fuer `ncbeargrown` (Daten, Beleg wie oben), im Spiel ansehen; als Frage an Kevin. |
| B5 | minor | `S:server/BanditsNPCBearGuard.lua:124-127`; `S:shared/BanditsNPCBearRules.lua:283-285`, `:303` | Zwei Abstaende rechnen ohne Koerperlaenge: Laerm-Ersatzweg (`followStart`/`followGap`, im Bau-Bericht schon genannt) und Heranlocken mit Futter (`comeUnfed`/`comeFed` 3/2 Kacheln Mitte-zu-Mitte). Bei 1,35 (Laenge 2,12 Kacheln) steht die Nase ~0,9 Kacheln vor der Figur -- kein Durchdringen, aber enger als beim Folgen. | `+ B.BodyGap(B.BodyNow(rec))` auch dort (nur gezaehmt), oder "im Spiel ansehen". |
| B6 | minor | `S:shared/Translate/EN/UI.json:86`, `:141`, `:71-72`; `S:server/BanditsNPCBearRegistry.lua:491` | Rest-Texte sagen beim grossen Koerper weiter "cub": `Note_Dead` ("The bear cub is dead.", kommt bei zahmem Tod, wenn keine Sperrfrist laeuft), `Why_Gone` ("The cub is gone."), `Menu_Hold`/`HoldTip`. F3 deckt nur die 15 Plan-Schluessel. | Big-Fassungen + `B.NoteBd` an `B.Close`/`tellWhy` (OBERFLAECHE/KERN) oder bewusst lassen (Frage). |
| B7 | minor | `S:client/ISUI/BanditsNPCBearMarker.lua:410-413`, `:290-294` | Das neue Element nimmt Mausklicks in seiner Flaeche (ISUIElement-Vorgabe `wantMouseEvents = true`, `V:client/ISUI/ISUIElement.lua:1998`, umgesetzt `:1004`); bei 4K sind das 90 x 90 px oben Mitte, solange die Markierung (<= ~60 s) sichtbar ist. Bandits' 45-px-Element tat dasselbe; noetig fuer den Doppelklick. | Lassen; im Spiel ansehen (Klick in die Welt oben Mitte waehrend der Markierung). |

Keine weiteren Befunde: Reihenfolge Neu-dann-Alt, Fehlversuch ohne Wirkung am alten Koerper, Leben-Anteil (`B.BodyHp` vor dem Tausch,
`S:server/BanditsNPCBearGrow.lua:510`), Register-Felder, Spiegel `body` (nur Diagnose), Not-Aus, Bench, MP-Probe, Kosten.

---

## 11. Fragen fuer Kevin (er testet gerade -- nichts davon haelt auf)

1. (B1) Soll "Call to me" in den ersten 2 Sekunden nach einem Wechsel kurz "warte" sagen? Sonst kann (sehr selten) ein zweiter grosser Baer ohne
   Schild stehen bleiben, bis du weggehst. Empfehlung: ja.
2. (B2) Darf der Wechsel mitten im Rennen passieren (der Baer steht dann bis 1,5 s still), oder soll er bis zu 10 s warten, bis er nicht rennt?
   Empfehlung: warten (hoechstens 10 s).
3. (B4) Fuettern am grossen Baeren mit erhobener Hand (wie bei Kuh/Hirschkuh) statt gebueckt? Empfehlung: ja, im Spiel ansehen.
4. (B6) Sollen auch "The bear cub is dead." / "The cub is gone." beim grossen Baeren "bear" sagen? Empfehlung: ja.
5. Auftrag 1 nennt "Lage/Richtung" bleibt: die Lage springt auf die Kachelmitte (< 1 Kachel), die Richtung wird "schaut zu dir" (die alte
   Richtung ist am Tier unbelegt, PE F5). Ok?

Statisch geprueft, nicht gespielt.
