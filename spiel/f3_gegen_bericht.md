# Lauf baer-f3 -- GEGENPRUEFER (nach der Nachbesserung)

Stand 13.11.2026 ~18:15, Rolle GEGENPRUEFER. **Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und keinem Bericht geglaubt:
jede Zahl unten stammt aus einem eigenen Lauf, jede Aussage ueber den Code aus der selbst geoeffneten Datei.
Geschrieben nur: `f3/GEGEN.md` (dieser Bericht), `f3/anleitung_entwurf.md` (berichtigt), `f3/schnittstelle.md` (Abschnitt GEGENPRUEFER
angehaengt), `f3/gegen_bild/` (eigene Bilder), `f3/probe/gegen/` (eigene Probe), `attrappe/f3_gegen/` (eigene Attrappen und alle Ausgaben).
**Kein Byte im Staging `mod_f3`, im Uebernahme-Skript, in NAEHTE.md, in Test-Mod, NPC Crew, Vanilla, Bandits.** Kein git-Schreiben, kein
Download, kein Spielstart (Spiel lief nicht: `tasklist` ohne ProjectZomboid). Kevin muss nach dem Einbau das Spiel neu starten.
Kuerzel: `S:` = `_arbeit/baer_zaehmen/mod_f3/42/media/lua/`, `V:` = Vanilla `ProjectZomboid/media/lua/`, `G:` = `_arbeit/baer_zaehmen/attrappe/f3_gegen/`,
`UEB` = `baer/tools/baer_uebernahme.py`.

## 0. Urteil zuerst

- **Bereit fuer Kevins Einzelspieler-Test: JA.** Kein offener Blocker. Beide major-Befunde (C1, C2) sind geschlossen, die Nachbesserung
  hat nichts kaputt gemacht (alle Laeufe unten gruen bzw. unveraendert).
- **Eine Sache habe ich berichtigt, die den Test verdorben haette:** die Testanleitung. Zwei ihrer Schritte waeren im Spiel so nicht
  gegangen (Abschnitt 7) -- Kevin haette zwei Fehler gemeldet, die keine sind.
- Von 16 Befunden: 10 geschlossen (C1, C2, C3, C4, C5, C6, C8, C9, P1, P3), 5 bewusst offen als Fragen an Kevin (C7, P2, P4, P5, P6),
  1 ohne Bedarf (P7). Dazu von mir 5 kleine Restbefunde (Abschnitt 8), keiner haelt den Test auf.
- **Kevins Nachtrag zum Herz** (*"oder das herz wird nur angezeigt wenn die namens anzeige vom baeren an ist eins von beiden"*) ist so
  gebaut: Herz nur mit Name-Zeile, kein eigener Schalter (Abschnitt 4 Nr. 7).
- Einzelspieler (`not isServer() and not isClient()`): das eine Programm rechnet alles. **Mehrspieler ungespielt**; der Server-Weg ist nur
  in der Attrappe gelaufen (Abschnitt 5 Stichprobe 2, Dauerlauf).

## 1. Was ich selbst laufen liess (alle Ausgaben in `G:`)

| Pruefung | Ergebnis | Ausgabe |
|---|---|---|
| vier Lua-Pruefer auf ALLEN 66 Lua-Dateien des Stagings (nicht nur den 27 geaenderten) | luacheck 66 / 0 failed; scopecheck 0 violations; localcount hoechstens 64 aktiv / 80 insgesamt (`client/ISUI/BanditsNPCBearHud.lua`, Grenze 180); luacheck_pz 50 x W113: 9 in `client/BanditsNPCBearMenu.lua` (die sechs globalen Aktionsklassen, im Uebernahme-Skript erlaubt), 41 in `NCBearBench*` (nie kopiert) | `G:pruefer_lua_alle.txt` |
| `attrappe/f3_kern/run.lua` | 274 bestanden, 0 Fehler | `G:f3_kern_run.txt` |
| `attrappe/f3_ober/run.lua` (Kern-Attrappe / echter Kern) | 261 ok / 0 und 251 ok / 0 | `G:f3_ober_run.txt`, `G:f3_ober_run_kern.txt` |
| `attrappe/f3_pruef/run.lua` | 40 ok, 0 Fehler, 1 Befund belegt (C7, bewusst offen) | `G:f3_pruef_run.txt` |
| `attrappe/f3_nach/run.lua` | 49 ok, 0 Fehler | `G:f3_nach_run.txt` |
| **eigene** `G:run.lua` (drei Stichproben + Kevins Antworten + Raender, Abschnitt 5) | **72 ok, 0 Fehler, 3 Hinweise** | `G:run_ergebnis.txt` |
| **eigener** Dauerlauf `G:dauerlauf.lua`: 40 Spieltage, feste Saat, zufaellig Fuettern / Traenken / Streicheln / Befehle / Aussehen / Besitzer schlaeft / Zombies / Laden; 8 Saaten Einzelspieler, 4 Server | **12 von 12: 0 Fehlerzeilen, 0 Verstoesse** (Werte immer 0..100, genau ein Baer, nie Futter oder Wasser ohne Wirkung genommen, abgelehnt = nichts genommen, Server genau ein Abgleich) | `G:dauerlauf_ergebnis.txt` |
| alle 45 alten Attrappen-Laeufe, einmal gegen die Test-Mod, einmal gegen das Staging (eigene Kopie des Laeufers) | 21 Kern-Laeufe zeilengleich bis auf `aussehen_kern` A14 ("B.OPTS genau die 12" -> 13, Kevin 6b). Oberflaeche: jede neue / verschwundene Fehlerzeile hat genau einen Grund aus dem F3-Umbau (Optionen + 5, Fenster 769 statt 640, "Coming later" weg, Look in der Knopf-Reihe, 13 Big-Fassungen) | `G:alte_testmod.txt`, `G:alte_f3.txt`, `G:alt_umgestellt.txt` |
| Texte: acht Sprachen / EN + DE / Gegenprobe / Code gegen JSON / Namen | 0 Fehler (3 Hinweise) / 0 Fehler (6 Hinweise) / 0 / 0 / B. und U. ohne Definition 0; EN 461 UI + 32 Sandbox | `G:texte_acht.txt`, `G:texte_ende.txt`, `G:texte_gegen.txt`, `G:code_gegen_json.txt`, `G:namen_gegen.txt` |
| Trockenlauf `python baer/tools/baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod_f3` | **0 Fehler, 2 Warnungen** (die zwei bekannten: 10 Vanilla-Clips fehlen in `NCBearCub.glb`; Baeren-Namen nur in NPC-Crew-Kommentaren) | `G:ue_trocken.txt:281-282` |
| Probe `--probe _arbeit/baer_zaehmen/f3/probe/gegen --staging ...` (eigener Ordner) | **0 Fehler, 2 Warnungen**, 120 Dateien geschrieben, langcheck 8 Sprachen 0 Fehler / 12 Hinweise, luacheck_pz auf 46 kopierten Dateien 0 Treffer / 9 erlaubt, Cheat-Funde 0, 0 Werkbank-Dateien kopiert, 8 Herz-Bilder, 13 Optionen | `G:ue_probe.txt:326-332` |
| `f3/staging_dateien_f3.txt` gegen die Platte und gegen die Test-Mod (eigenes Zaehlskript, MD5) | Liste 159 Zeilen = 159 Dateien, **0 Abweichungen** (MD5 und Bytes); 14 neu, 38 ueberschreibt, 107 byte-gleich; **33 Modell-Dateien (models_X, textures, AnimSets): alle byte-gleich mit der Test-Mod**; keine Datei nur in der Test-Mod; Zeilenenden je Datei wie vorher, Lua ASCII ohne Tabulator und BOM | Zahlen hier |
| Namen frei (`aussehen/werkzeug/kollision.py`): `BanditsNPCBearHeart16`, `...Zz`, `BearNeedsPercent`, `...DrinkAction`, `...NeedRules`, `...Needs`, `...Sleep` | je text 0 / dateinamen 0 | Zahlen hier |
| Kahlua-Heikles (`next(`, `table.unpack`, `string.gmatch`, `goto`, `os.time`, `string.format`) in den fuenf neuen Dateien und allen geaenderten Zeilen | 0 Treffer | -- |

Zu "alle bestehenden Attrappen bleiben gruen": die alten Attrappen waren schon VOR F3 nicht alle gruen (sie halten alte Erwartungen
fest, z. B. `kern/run.lua` 112 bestanden / 24 Fehler auch gegen die Test-Mod). Richtig ist: **F3 aendert kein einziges Kern-Ergebnis** und
jede Oberflaechen-Abweichung ist erklaert. Ein Punkt bleibt (Restbefund R4): das Original `attrappe/f2_ober/run.lua` bricht am F3-Stand an
seiner Zeile 435 ab.

## 2. Die Befunde einzeln -- geschlossen?

| ID | Urteil | Beleg (selbst geprueft) |
|---|---|---|
| **C1** major | **geschlossen** | `UEB:639` `("BanditsNPCBearMenu.lua", "BanditsNPCBearDrinkAction")`; eigene Probe gruen (`G:ue_probe.txt:332` "ERGEBNIS: OK -- 0 Fehler, 2 Warnungen (PROBE)") |
| **C2** major | **geschlossen** | `S:server/BanditsNPCBearSleep.lua:233-235` ("hand" + Schlaf aus Muedigkeit: Marke `rec.slpAt` bleibt, `s.slpBack` gemerkt), `:255-257` Sperre 60 s, `:350-359` legt sich wieder hin. Eigener Lauf `G:run.lua` X8 (gefuettert, kurz wach, Marke bleibt) und f3_nach N1-N3 neu gelaufen. Gilt nur fuer den Schlaf aus Muedigkeit; neben dem schlafenden Besitzer gibt es keine Rueckkehr (richtig so) |
| **C3** minor | **geschlossen** | `...Sleep.lua:220-225`; eigener Lauf X4: Stay / Sit / Roam / Follow / Come wecken und loeschen die Marke; G1b: nach "Folgen" bleibt er 3 Spielstunden wach |
| **C4** minor | **geschlossen** | `S:server/BanditsNPCBearGrow.lua:799` (`asleep` nur mit `B.FindAnimal(rec) ~= nil`); f3_nach N5 neu gelaufen |
| **C5** minor | **geschlossen** | `UEB:461-468`, Probe-Zeile "Tier-Regel getForwardDirection: BanditsNPCBearZz.lua:122 (aim), BanditsNPCBearFoe.lua:201 (knock)"; `baer/NAEHTE.md:57-65`; javap selbst: `getForwardDirection()` steht nur in `IsoGameCharacter`, nicht in `IsoAnimal` / `IsoPlayer` / `IsoLivingCharacter` |
| **C6** minor | **geschlossen** | (1) `...Sleep.lua:32-36`, Vanilla selbst geoeffnet: `V:server/ClientCommands.lua:658-661` (`onVehicleSleep` -> `setAsleep`), `V:client/ISUI/ISWorldObjectContextMenu.lua:1098`; (2) `baer/NAEHTE.md:8-10` nennt Funktion und Text, NPC Crew heute `shared/BanditsNPCNeeds.lua:34` (`fatigue = 1.6`), `shared/BanditsNPCPrograms.lua:5265` (`15 * 0.7 * dtH`), `:5319` (`15 * dtH`); (3) `S:client/BanditsNPCBearMenu.lua:383` -> `V:shared/env.lua:1` (`function round`) |
| **C7** minor | **offen, bewusst** (Frage 8) | `S:shared/BanditsNPCBearNeedRules.lua:279-287`; eigener Lauf X7: Regler 0 + Vertrauen 10 -> `B.NoFight` = "trust". Praktisch nur ueber "am Boden" (-5 je Mal) erreichbar, weil bei Regler 0 kein Tag mit Hunger / Durst zaehlt (`:235`) |
| **C8** minor | **geschlossen** fuer den Abgleich | `S:server/BanditsNPCBearNeeds.lua:326` nehmen, `:328` gutschreiben, `:336` Abgleich zuletzt; eigener Lauf G2: wirft `sendSyncEntity`, ist das Wasser einmal genommen UND der Durst 0. Kleiner Rest R3 |
| **C9** minor | **geschlossen** | `...Sleep.lua:202` (`slp.hrs`), `...Needs.lua:191-199`, `:214`; nachgerechnet (20-4 Uhr -> Bonus am zweiten Tag, 16-2 Uhr -> nur am ersten); f3_nach N7 neu gelaufen |
| **P1** minor | **geschlossen** | `S:client/ISUI/BanditsNPCBearZz.lua:69-70`; im selbst gezeichneten Bild (2,6 / 3,0 / 3,4 s) je hoechstens ein grosses Z |
| **P2** minor | **offen, bewusst** (Frage 9) | nicht geaendert |
| **P3** minor | **geschlossen** | `S:client/BanditsNPCBearWinData.lua:591-600`, `:850-854`; Bild `f3/bilder/KEVIN_fenster_f3_regler0_DE_1080.png` angesehen: "Aus" ohne Balken, Vertrauen mit Balken |
| **P4** minor | **offen, bewusst** (Frage 10) | im selbst gezeichneten DE-Bild: Fusszeile orange, Chip "Folgt dir", "81 je Treffer" |
| **P5** minor | **offen, bewusst** (Frage 1) | eingebaut = Entwurf D (MD5 der Dateien 16 / 32 / 64 gleich `f3/herz/herz_D_*.png`) |
| **P6** minor | **offen, bewusst** (Frage 12) | ein Text fuer beide Koerper |
| **P7** minor | **nichts noetig** | `V:client/OptionScreens/MainOptions.lua:2810-2813`: Tooltip nur am Haekchen |

## 3. Etwas kaputt gemacht?

Nein, soweit statisch pruefbar. Die Nachbesserung aendert 8 Lua-Dateien (Diff gegen `f3/werkzeug_nach/vorher/` selbst gelesen): alle
F3-Attrappen gruen, die 45 alten Laeufe gegen das Staging zeilengleich mit dem Stand vor der Nachbesserung bzw. erklaert, Texte
unveraendert 461 / 32, Trockenlauf und Probe gruen, kein neuer Engine-Aufruf (nur `removeFluid` / `sendSyncEntity` in neuer Reihenfolge),
kein neues `pcall`. `math.max` in `S:client/ISUI/BanditsNPCBearWindow.lua:188` ist in derselben Datei schon 28-mal in Gebrauch (Test-Mod, gespielt).

## 4. Kevins Antworten 1-7 Punkt fuer Punkt am Code

| Nr. | Antwort | Fundstelle im Staging | eigener Beleg |
|---|---|---|---|
| 1 | beide Schlafhaltungen -- hier nur die 8 Schluessel | `S:shared/BanditsNPCBearFightRules.lua:77-84` (liedown, sleep, wakeup, wakealarm, curlin, sleepcurl, curlout, wakecurl); `S:shared/BanditsNPCBear.lua:291` `sleepClips = false`; ohne Schlaf-Clips setzt der Ruhe-Treiber nur sitdown / sit / standup (`S:client/BanditsNPCBearPose.lua:135-137`, `:207-209`) | keine Modell-Datei geaendert (Abschnitt 1) |
| 2 | vom Zombie geweckt: 5 s schlaftrunken weg, dann kaempfen; sehr muede -> weiter weg | `...BanditsNPCBear.lua:285` `wokeFleeMs = 5000`; `S:server/BanditsNPCBearSleep.lua:248-252`; `S:server/BanditsNPCBearFight.lua:313-322`; `S:shared/BanditsNPCBearFightRules.lua:397-399` | `G:run.lua` A2b: aufgeschreckt, bei 3,8 s noch Rueckzug "woke", bei 6,8 s Kampf (= 1,6 s Aufsteh-Halt + 5 s); A2: bei Muedigkeit 100 kein Kampf |
| 3 | Muedigkeit steigt auch beim Folgen; ab 90 % kaempft er nicht und SAGT es; erst bei 100 % schlaeft er ein | `...BanditsNPCBear.lua:274` `tirVery = 90, tirCollapse = 100`; Anstieg in jedem Modus `S:server/BanditsNPCBearNeeds.lua:466-474`; Meldung `:389-395`, `:404-420`; Fenster-Fusszeile `S:client/BanditsNPCBearWinData.lua:792-793`; Schild "too tired - backing off" `S:client/ISUI/BanditsNPCBearHud.lua:409` | G1: folgend von 99 auf 100 -> schlaeft von selbst ein (Grund tired), genau eine Meldung |
| 4 | Vertrauen: viel -> bis 20 % langsamer, wenig -> bis 20 % schneller (neutral 50); sehr wenig -> weigert sich zu kaempfen, sichtbar; andere Befehle gehen; frisch gezaehmt nie betroffen | `...BanditsNPCBear.lua:277` `trStart = 50, trBonus = 0.2, trMalus = 0.2, trRefuse = 15`; `S:shared/BanditsNPCBearNeedRules.lua:186-191`, `:279-287`; Meldungen `...Needs.lua:168-177`; Fenster `...WinData.lua:790-791` | X6: Faktor 1,2 / 1,1 / 1,0 / 0,9 / 0,8 bei 0 / 25 / 50 / 75 / 100; X1: 15 -> kaempft, 14,9 -> Rueckzug "trust", Sicht `nof`, eine Meldung, Follow und Sit gehen weiter, frisch gezaehmt 50, Junges nie |
| 5 | z Z z hellblau ueber dem Kopf, Blickrichtung fragen, weich z -> Z -> z | `...BanditsNPCBear.lua:291` `sleepCol = { 0.70, 0.85, 1.00 }`; `S:client/ISUI/BanditsNPCBearZz.lua:122` (Jar-Ausnahme, Abschnitt 10), `:204-231` Ueberblenden mit `drawTextCentre`; kein `drawTextZoomed`-Aufruf im Staging (grep 0) | Bild selbst gezeichnet (Abschnitt 6) |
| 6a | Hunger / Durst leer: Leben bis 1 %, nie Tod, nie am Boden | `...BanditsNPCBear.lua:262` `needHpFloor = 0.01`; `...Needs.lua:482-495`; `S:server/BanditsNPCBearGrow.lua:321-331` | X2: 200 Spielstunden bei 100 / 100 -> Leben genau 0,01, `rec.down` nil, nicht tot |
| 6b | EIN neuer Regler, 13 | `...BanditsNPCBear.lua:325`; `mod_f3/42/media/sandbox-options.txt:93-98`; 13 `option BanditsNPC.Bear*` gezaehlt | Probe: "B.OPTS 13 Optionen" |
| 6c | keine Uhrzeiten; bei 100 % schlafen bis 0 %; Folgen weckt, Muedigkeit bleibt | kein `getHour` / `getTimeOfDay` / `sleepFrom` im Code (grep 0, Tier-Regel `getHour`: "kein Aufruf"); `...NeedRules.lua:331-349`, `:358-373`; `...Sleep.lua:185-204` | G1: Schlaf 100 -> 0 in 58 Takten = 9,67 Spielstunden, Meldung "ausgeruht", danach wach; G1b: nach 2 h bei 79 "Folgen" -> wach, 79 bleibt |
| 6d | Besitzer schlaeft + Baer folgt -> legt sich neben ihn | `...NeedRules.lua:337`; `...Sleep.lua:334-348`; Client meldet `S:client/ISUI/BanditsNPCBearZz.lua:313-327` | X3: liegt 1,41 Kacheln neben dem Besitzer, steht auf, wenn er aufwacht; in Bleiben nicht; ohne Auffrischung nach 90 s wach |
| 6e | kein Schlaf-Knopf; jeder Befehl weckt; Streicheln nicht; Fuettern / Traenken kurz | `S:server/BanditsNPCBearFollow.lua:107`; `S:server/BanditsNPCBearServer.lua:275`, `:318-321`; `...Needs.lua:327` | X4; C2 oben; im Fensterbild kein Schlaf-Knopf |
| 6f | kein Schlafton, kein Bett, kein selbst Trinken | nichts davon im Code (`tirSleepBed` nur als Stellwert `...BanditsNPCBear.lua:270`) | -- |
| 6g | Balken mit Prozent, Wort im Tooltip | `...WinData.lua:591-600`; Text `UI_BN_Bear_Win_NeedNow` "Now: %1 (%2%%)" | im Bild: "64%" im Balken, "Now: Tired (64%)" im Tooltip |
| 7 | Herz bei maximalem Vertrauen ueber dem Namensschild, NUR mit Namensanzeige, kein eigener Schalter | `S:client/ISUI/BanditsNPCBearHud.lua:469` `e.showName = md.tags and tagOn(c)`, `:532-543` (Herz nur in `if e.showName`), `:803-810` (gezeichnet nur in `if e.showName`); `S:client/BanditsNPCBearOptions.lua:96-155` kein Herz-Eintrag; `trHeart = 100` (`...BanditsNPCBear.lua:277`), Sicht `trM` `...Needs.lua:527` | X5: 99,9 kein `trM`, 100 `trM` + Meldung, 99 weg; f3_ober neu gelaufen: "Namensschilder aus -> kein Herz", "Name tag dieses Baeren aus -> kein Herz", "kein eigener Schalter fuers Herz". Bild eigen (numpy / PIL, `f3/herz/herz_zeichne.py`, kein Download), 8 Groessen RGBA |

**Rhythmus (6c), nachgerechnet:** wach von 0 auf 100 % ohne Rennen / Kampf bei Vertrauen 50: Junges 100 / 2,4 = **41,7**, halbstark 100 / 2,0 =
**50**, ausgewachsen 100 / 1,6 = **62,5 Spielstunden** (`tirAt`, `...BanditsNPCBear.lua:269`; bei Vertrauen 100 x 1,25 laenger, bei 0 x 0,83);
Schlaf von 100 auf 0 %: 100 / 10,5 = **9,5 Spielstunden bei jeder Groesse** (`tirSleepGround`, `:270`; im Lauf G1 gemessen 9,67 h wegen des
10-Minuten-Takts). Ausgewachsen = der NPC-Crew-Wert 1,6 (`NPCCrew/42/media/lua/shared/BanditsNPCNeeds.lua:34`), Abbau = `15 * 0.7`
(`...BanditsNPCPrograms.lua:5265`). Frage 2.

## 5. Meine drei Stichproben (`G:run.lua`, am echten Kern)

1. **100 % -> Schlaf bis 0 %, Wecken durch Folgen** (G1, ganzer Weg ueber `B.SlowTick` + `B.BrainTick`): ausgewachsener Baer folgt, 99 % ->
   nach 4 Takten 100 % -> schlaeft (eine Meldung, Marke gesetzt, Sicht `slp`) -> 58 Takte spaeter 0 %, wach, Meldung "ausgeruht", Marke weg;
   Hunger / Durst stiegen im Schlaf weiter. Zweiter Schlaf: nach 2 h bei 79 "Folgen" -> wach, Marke weg, 79 bleibt, 3 h spaeter weiter wach.
2. **Wasser genau einmal im MP-Weg** (G2, Modus Server, ueber `BanditsNPCBearDrinkAction:complete()`): ein `removeFluid(0,4, false)`, ein
   `sendSyncEntity(nil)`, Flasche 1,0 -> 0,6 l, Durst 0. Zweites `complete()` derselben Aktion: abgelehnt, nichts genommen. Fremder
   Spieler, Behaelter nicht im Inventar, Benzin, leer: je nichts genommen, Durst unveraendert. Rest 0,1 l: genau 0,1 l und 15 Punkte.
   Wirft der Abgleich: einmal genommen und angerechnet. Ohne Kern (MP-Client): nichts. Einzelspieler: kein `sendSyncEntity`.
3. **Aussehen-Wechsel behaelt die vier Werte** (G3): gen -> foto -> std, je ein neuer Koerper; `nH 37,3 / nT 61,7 / nF 88,8 / tr 93,4`,
   Verlauf `trD` und Tagesbuch nach jedem Wechsel gleich, der Spiegel am neuen Koerper traegt sie, Sicht 37 / 61 / 88 / 93.

Dazu X1-X9, A1, A2 (Abschnitt 4 und 7) und der Dauerlauf.

## 6. Fensterbild selbst aus dem Code gezeichnet und angesehen

Eigene Kopie der Kette (`f3/gegen_bild/zeichne_gegen.py`: Lua 5.1 `attrappe/f3_ober/zeichne_dump_f3.lua` gegen das Staging, Mitschrift nach
`f3/gegen_bild/dump/`, gemalt mit den echten Spielschriften ueber Kevins Spielbild). Ergebnis: Fenster 769 x 615 (EN 1080p), 808 x 615 (DE),
1373 x 1178 (4K). **Alle sechs Bilder byte-gleich mit `f3/bilder/`** (MD5) -- die veroeffentlichten Bilder stammen also wirklich aus dem
Code. Angesehen: `KEVIN_fenster_f3_1080.png`, `..._DE_1080.png`, `KEVIN_zzz.png`, `KEVIN_herz_im_spiel.png`, dazu `..._regler0_DE_1080.png`.
Drei Karten, Befehle 5 x 3, graue Platzhalter Fish / Inventory / Nose alerts, "Look" ueberlappt nicht mit "Show damage", Tooltip-Texte
passen zu Kevins Antworten (90 % / 100 % / "Any order wakes it" / "lies down next to you" / Herz am Namensschild). Auffaellig nur R5.

## 7. Testanleitung `f3/anleitung_entwurf.md` -- geprueft und berichtigt

Jeden Befehl und jeden zitierten Text gegen Code und `EN/UI.json` geprueft (Befehle existieren, Texte stimmen woertlich). Berichtigt:

| Schritt | Fehler der ersten Fassung | Beleg | jetzt |
|---|---|---|---|
| **13** | nach Schritt 12 schlaeft er noch (Muedigkeit ~100); ein liegender Baer waechst nicht um -> `NCBear_CubGrow(15)` braechte keinen grossen Baeren, Teil C liefe mit dem Jungen | `S:server/BanditsNPCBearGrow.lua:593`; `G:run.lua` A1: 40 Takte spaeter noch "cub", nach Follow "big" | Schritt 12 endet mit "Follow klicken, `NCBear_CubNeeds(nil, nil, 20)`"; 13 sagt "er muss wach sein" |
| **15** | `NCBear_CubSleep()` stellt die Muedigkeit auf 100 -> vom Zombie geweckt ist er "zu muede" und kaempft NIE; die Anleitung versprach "dann kaempft er" | `S:client/NCBearBenchNeeds.lua:149`, `...NeedRules.lua:284`; A2: kein Kampf; A2b mit 60 %: Kampf nach 6,8 s | Zusatz `NCBear_CubNeeds(nil, nil, 60)` nach dem Einschlafen |
| 9 | "bleibt wach" stimmt nur, bis er wieder 100 % hat -- nach `NCBear_CubSleep()` waere das nach Sekunden | `...NeedRules.lua:344-345` | vorher `NCBear_CubNeeds(nil, nil, 60)` |
| 10 | nach dem Befehl aus 9 liegt eine Sperre von 60 s | `...Sleep.lua:255-257` | Hinweis "bis zu einer Minute" |
| 11 | waehrend man schlaeft, ist das Bild dunkel -- man sieht ihn nicht liegen | -- | Hinweis: beim Aufwachen hinsehen, sonst Log-Zeile |
| 4, 5 | "lehnt ab" -- im Spiel ist der Menuepunkt grau mit dem Grund | `S:client/BanditsNPCBearMenu.lua:348-352`, `:391-396` | Wortlaut |
| 20 | Seite heisst "NPC Crew: Bear" | `UI_BN_Bear_MO_Page` | Wortlaut |
| neu 16b | Kevins 6a (Leben bis 1 %, nie Tod) stand in keinem Schritt | `...Needs.lua:482-495` | wahlfreier Schritt mit `NCBear_CubSet("needHpHun", 300)` |

## 8. Restbefunde (neu, von mir; keiner haelt den Test auf)

- **R1 (minor, behoben in der Anleitung):** Schritte 13 und 15, siehe Abschnitt 7.
- **R2 (minor, Verhalten uneinheitlich):** kurz geweckt (Fuettern / Traenken) und in dieser Minute kommt ein Zombie OHNE Treffer: die Marke
  bleibt, er kaempft und **legt sich nach der Gefahr wieder hin** (`S:server/BanditsNPCBearSleep.lua:431-453`: der wache Zweig loescht
  die Marke nicht; `G:run.lua` X8 "2 min nach der Gefahr: schlaeft wieder = true"). Ein vom Zombie GEWECKTER schlaeft dagegen nicht weiter
  (`:236-238`). NACHBESSERUNG Frage 8 sagt "nach Gefahr schlaeft er NICHT von selbst weiter" -- das stimmt in diesem Randfall nicht.
  Kein Schaden; mit Kevins Antwort auf Frage 7 unten wird es so oder so einheitlich.
- **R3 (kosmetisch):** der Kommentar `S:server/BanditsNPCBearNeeds.lua:325` ("ohne Engine-Aufruf dazwischen") stimmt nicht woertlich:
  zwischen Nehmen (`:326`) und Gutschrift (`:328`) laeuft `B.SleepStop` (`:327`) mit `getTimestampMs()` und `B.Now()`
  (`...Sleep.lua:227-229`). Kein Wurf-Kandidat; die Gutschrift koennte trotzdem eine Zeile hoeher stehen.
- **R4 (Hinweis, Attrappen):** das Original `attrappe/f2_ober/run.lua` bricht am F3-Stand an Zeile 435 ab (liest das entfernte Mass
  `m.divY`, `G:alte_f3/f2_ober_attrappe.txt`) und prueft danach nichts mehr; nur die umgestellte Kopie laeuft durch (287 / 288 ok,
  2 Fehler wie vor F3, `G:alt_umgestellt.txt`). Vor F4 einmal an Variante B anpassen.
- **R5 (Hinweis, Bild):** im Fensterbild scheinen unter dem Tooltip die Knoepfe durch (`f3/gegen_bild/KEVIN_fenster_f3_DE_1080.png`
  rechts: "Inventar", "Verbinden" hinter dem Text). Ob das Spiel den Tooltip genauso durchsichtig zeigt, ist ungeprueft (Testpunkt beim Ansehen).
- Nicht als Befund, nur zur Kenntnis: Verbinden weckt nicht (kein `B.SleepStop` in `S:server/BanditsNPCBearMend.lua`); schlaeft er beim
  Folgen bei 100 % ein, steigt er nicht mit ins Auto (`B.SleepStep` vor `B.FollowStep`, `S:server/BanditsNPCBearServer.lua:869` / `:877`),
  die Meldung kommt, "Herholen" holt ihn; die Fusszeile "Your bear is asleep." steht auch beim Jungen (`...WinData.lua:205`, ein Text).

## 9. Fragen fuer Kevin (gebaut ist jeweils der genannte Weg)

1. Herz: D "Goldrand" bleibt eingebaut -- oder A "Klassik" (bei 1080p klarer rot)?
2. Rhythmus: wach bis 100 % ohne Rennen und Kampf: Junges ~42, halbstark ~50, ausgewachsen ~62 Spielstunden; dann 9,5 Stunden Schlaf bei
   jeder Groesse. Oft genug muede?
3. In Bleiben / Sitz / Frei schon frueher hinlegen (z. B. ab 90 %)? Heute ueberall erst bei 100 % (`tirStaySleep`).
4. Weigerung zu kaempfen unter 15 % Vertrauen (`trRefuse`) -- passt die Schwelle?
5. Herz bei genau 100 % Vertrauen (`trHeart`) -- oder schon frueher (z. B. ab 95)?
6. Fuettern / Wasser im Schlaf: er steht auf, frisst und legt sich nach einer Minute wieder hin. Richtig so?
7. Vom Zombie oder Laerm geweckt: heute bleibt er danach wach, bis er wieder 100 % hat. Soll er weiterschlafen, solange er noch muede ist?
8. Regler "needs speed" auf 0: unter 15 % Vertrauen weigert er sich auch dann zu kaempfen. So lassen?
9. Balken ueber dem Kopf: Vertrauen in Rosa statt Gelb (sieht sonst aus wie Ausdauer)?
10. "Kaempft nicht" steht orange unten im Fenster und in den Tooltips. Auch oben bei "Melee damage"?
11. z Z z: immer nur ein grosses Z, Groesse und Abstand gut?
12. Tooltip Muedigkeit und Zeile "Your bear is asleep" beim Jungen: eigene Fassung fuers Junge (acht Sprachen)?
13. Ein Zombie hinter einer Wand weckt ihn auch (8 Kacheln, ohne Sichtpruefung). Ok?
14. Beim Traenken nimmt die Figur die Flasche nicht in die Hand (die Waffe bleibt). Ok?
15. Verbinden laesst ihn schlafen (wie Streicheln). Ok?
16. Schlaeft er beim Folgen ein und du faehrst los, bleibt er liegen (Meldung kommt). Ok, oder soll Einsteigen ihn wecken?
17. Die 5 Sekunden schlaftrunken zaehlen nach dem Aufschrecken (1,6 s) -- zusammen 6,6 s bis zum Kampf. Ok?

## 10. Jar-Ausnahmen im Staging (jede nur im Jar belegte Methode, mit Datei:Zeile)

| Aufruf | Stelle | Kevins Wort |
|---|---|---|
| **`animal:getForwardDirection()`** am Tier -- `zombie.characters.IsoGameCharacter.getForwardDirection()` -> `zombie.iso.Vector2`, javap -c 42.22: Offset 0 `aload_0`, 1 `getfield forwardDirection`, 4 `areturn`; in `IsoAnimal` / `IsoPlayer` / `IsoLivingCharacter` nicht ueberschrieben (javap -p selbst) | `S:client/ISUI/BanditsNPCBearZz.lua:122` (Funktion `aim`, hoechstens 1 x je Sekunde je schlafendem Baeren) | **13.11.2026, Antwort 5 -- die EINE neue in F3** |
| `animal:pathToLocation(x, y, z)` | `S:server/BanditsNPCBearWorld.lua:946` (`B.MoveTo`) | 08.11. |
| `animal:setVariable("animalRunning", false)` (gelesen `a:getVariableBoolean("animalRunning")` `S:server/BanditsNPCBearGuard.lua:230`) | `S:server/BanditsNPCBearWorld.lua:945` (`B.MoveTo`) | 11.11. |
| `pcall(getTextOrNull, key, "%1", ..., "%9")` | `S:shared/BanditsNPCBear.lua:508` (`B.T`) | 12.11. |

F3 bringt sonst keinen unbelegten Aufruf: alle 8 Methodennamen, die es in der Test-Mod noch nicht gab (`getAllWaterFluidSources`,
`getAmount`, `getFluidContainer`, `getName`, `getStaticModel`, `isEmpty`, `removeFluid`, `sendSyncEntity`), haben einen Vanilla-Aufrufer mit
gleichen Argumenttypen (`V:shared/TimedActions/Animals/ISGiveWaterToAnimal.lua:6`, `:34`, `:51`, `:86-87`,
`V:client/ISUI/Animal/ISAnimalContextMenu.lua:466`, `:485`, `V:shared/Vehicles/TimedActions/ISWashVehicle.lua:6`); die Empfaenger in allen
neuen Zeilen einzeln durchgesehen (`player:isAsleep()` `V:client/ISUI/ISButtonPrompt.lua:440`, `character:shouldBeTurning()`
`ISGiveWaterToAnimal.lua:16`, `animal:faceThisObject(character)` `ISPetAnimal.lua:17`, `isGamePaused()` `V:client/Foraging/ISSearchManager.lua:1462`,
`drawTextureScaled` `V:client/Chat/ISChat.lua:418`, `getTexture("media/ui/...")` `:921`). Kein neues `pcall`.

## 11. Ungeprueft

Alles Laufzeit-Verhalten: Bild Aufstehen -> Fressen -> wieder Hinsetzen, z Z z und Herz im Spiel, Lage ueber dem Kopf (Blickrichtung
eines ruhenden Tiers), `removeFluid` mit einer groesseren Menge am MP-Server, der ganze Mehrspieler. Die Attrappe beweist Logik, nicht die
Engine (Beispiel aus diesem Lauf, `G:probe_a2.lua`: in der Attrappe stehen Zombies still und ein Lauf ist ein Sprung -- bei 6 Kacheln
springt der schlaftrunkene Baer weg und der Zombie ist ausser Reichweite; im Spiel kommt der Zombie nach).

## 12. Dateien dieser Rolle (alle unter `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/`)

- `f3/GEGEN.md` (dieser Bericht), `f3/anleitung_entwurf.md` (berichtigt), `f3/schnittstelle.md` (Abschnitt GEGENPRUEFER angehaengt).
- `attrappe/f3_gegen/`: `run.lua` + `run_ergebnis.txt`, `dauerlauf.lua` + `dauerlauf_ergebnis.txt`, `probe_a2.lua`, `pruefer_lua_alle.txt`,
  `f3_*_run*.txt`, `alte_testmod/` + `alte_f3/` (je 45 Laeufe) + `alt_umgestellt.txt`, `texte_*.txt`, `namen_gegen.txt`,
  `code_gegen_json.txt`, `ue_trocken.txt`, `ue_probe.txt`.
- `f3/gegen_bild/` (sechs Bilder, Mitschrift `dump/`, `zeichne_gegen.py`), `f3/probe/gegen/` (Probe, 73 MB -- kann nach dem Einbau weg).

Statisch geprueft, nicht gespielt.
