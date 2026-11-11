# Gegenpruefung B1c "baer-b1c" (11.11.2026, ~05:55)

Rolle: Gegenpruefer. Nichts davon gebaut, keinem Bericht geglaubt: jede Stelle der 17 Befunde (A1-A7, B1-B10) und ihre Umgebung im
heutigen Staging gelesen (ganz: `server/BanditsNPCBearHeal.lua`, `...Registry.lua`, `...Ride.lua`, `...Guard.lua`, `...World.lua`
Kacheln/Zombies/Suchlauf/Laufen, `...Server.lua` Hirn-Takt, `...Follow.lua` Folgen/Bitten, `client/BanditsNPCBearOptions.lua`,
`client/ISUI/BanditsNPCBearMap.lua`, `...Marker.lua`, `NCBearBenchCub.lua`; in Teilen Rules, Menu, Hud), die neuen Vanilla-/Bandits-Belege
selbst nachgelesen, alle Pruefer und Attrappen selbst laufen lassen, die Probe in einen EIGENEN Ordner
(`C:/Users/Kevin/AppData/Local/Temp/claude/086a7114045651dc/d5933cc7-7f9d-46b2-a3a8-0929595b654b/scratchpad/gp/probe_gegen`).
**Statisch geprueft, nicht gespielt.** Geschrieben nur diese Datei und `anleitung_b1c_entwurf.md`. Kein git, kein Spiel, nichts in die
Test-Mod, nach NPC Crew, Vanilla oder Bandits. Das Spiel lief waehrend der Pruefung NICHT (`tasklist`: kein ProjectZomboid, 05:52).
Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`, `B:` Bandits `42.22/media/lua/`.

## 1. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test. Kein Blocker.** Von 17 Befunden sind 12 am heutigen Code geschlossen (A1, A2, A4,
A5, A6, B1, B2, B3, B4, B5, B8, B9), 5 bewusst offen oder nur teilweise (A3 Regel-Frage, A7 FR-Geschlecht, B6 nur Kommentar, B7
Verhalten unveraendert, B10 Teil 2) -- alle fuenf ehrlich im Code bzw. Bericht genannt, keiner verhindert den Einzelspieler-Test, keiner
reisst eine rote Linie. Kein Befund zu Unrecht abgelehnt (abgelehnt wurde keiner; B1 im Mehrspieler bewusst STRENGER als Pruefer Bs
Vorschlag, begruendet). Die Nachbesserung hat nichts kaputt gemacht, was ich finden konnte: alle Attrappen gruen und byte-gleich mit den
gespeicherten Ergebnissen, Pruefer Bs EIGENE unveraenderte Attrappe `pruef_b1c` jetzt 6 x OK / 0 x BEFUND (vorher 4 BEFUND). Drei neue
kleine Restbefunde (N1-N3), keiner rot.

## 2. Je Befund (Zeilen = heutiges Staging)

| ID | Urteil | Beleg im heutigen Code / selbst nachgesehen |
|---|---|---|
| A1 major | geschlossen | `S:server/BanditsNPCBearRegistry.lua:353-355`: Spiegel `tame`/`missing` (jede Fassung) oder `fed` (v2) + Heilung nil -> `return nil, "heal"`; einziger Aufrufer `S:server/BanditsNPCBearServer.lua:167-169` sagt dann `Why_Gone`, kein `B.NewRec("found")`, Spiegel bleibt. Der Suchlauf laesst nil stehen (`World.lua:757-766`). Grenze (ehrlich, Frage 3): ein v1-Spiegel `fed` wird weiter ein Fund wie in B1b (nie herstellbar), ein MP-Spiegel ohne Konto bleibt unberuehrbar. Attrappe b1c_kern 10a/10b gruen. |
| A2 minor | geschlossen (MP-Testpunkt bleibt) | `S:server/BanditsNPCBearGuard.lua:212-218`: `getActionStateName`/`getVariableBoolean` nur `elseif B.IsSP()`; `S:server/BanditsNPCBearWorld.lua:422`: `IsReanimatedForGrappleOnly` nur im SP, am Server `isAlive` (`B:server/BanditSave.lua:52`). Am Server bleiben `getStress` (`V:shared/TimedActions/Animals/ISMilkAnimal.lua:17`, selbst gelesen) und getX/getY. Kommentare ehrlich (Guard.lua:13-15, :163-168; Server.lua:586-592 nennt die A3-Ausweitung). Attrappe 10j: 0 Aufrufe am Server. |
| A3 minor | offen (Regel-Frage, zu Recht) | Selbst gegrept: `addTickBox`/`addSlider` haben in Vanilla, Bandits UND NPC Crew keinen Aufrufer (NC benutzt nur `addComboBox`, NC `client/BanditsNPCModOptions.lua:97`; Bandits nur `create`, `B:client/BanditModOptions.lua:12`). Definition `V:client/PZAPI/ModOptions.lua:64-86`, `:206-228` ganz gelesen: reines Lua, legt nur Tabellen an; Vanilla zeichnet sie selbst (`V:client/OptionScreens/MainOptions.lua:2809-2830`, `:3019-3036`, selbst gelesen, kein nil-Zugriff auf fehlende Felder). Kopf `S:client/BanditsNPCBearOptions.lua:10-18` und NAEHTE Zeile 19 ehrlich. Kevins Wort (Frage 1). |
| A4 minor | geschlossen | `baer/tools/baer_uebernahme.py:277-281`: `(?i)\banimalRunning\b` / `(?i)\bpathToLocation\b` auf jedes Vorkommen im Code-Teil (Strings mit), erlaubt nur `World.lua B.MoveTo` und `Guard.lua calmTickBody`; `mo_text_hits` `:302-331`. `attrappe/uebernahme_b1c/probe_regeln.py` selbst gelaufen: 34 Faelle, 0 Fehler; Trockenlauf zeigt genau `Guard.lua:217`, `World.lua:859/860`. |
| A5 minor | geschlossen | `S:client/ISUI/BanditsNPCBearMap.lua:168-187`: eigene Form `hook(key, cls, mini)` mit Merker `hooked[key]`, einmal je Klasse, nie erneut; Kopf `:15-19` nennt die NC-Lehre ehrlich. Wirkung gleich (b1c_ober 193/180 gruen). |
| A6 minor | geschlossen | (1) `Server.lua:586-592` verweist auf den Kommentar ueber `B.ScanAnimals`; (2) `Ride.lua:17-18`, `World.lua:34-35`, `:295`: getZ `B:server/BanditServerSpawner.lua:191` -- selbst gelesen: `local pz = player:getZ()` steht dort; (3) `Registry.lua:142-144` ehrlich ("Call to me fuer Unanklickbare spaeter ueber das Baeren-Fenster, F4"); (4) ENTSCHEIDUNGEN.md:282 nur angemerkt -- richtig: die Aufrufe stehen bei `ISMilkAnimal.lua:139` bzw. `ZAMove.lua:32` (selbst gelesen), der Code zitiert richtig. |
| A7 minor | teils (FR offen, zu Recht) | `b1b_kern/ergebnis.txt` = mein Lauf (204/0, byte-gleich); NAEHTE Kopf v3.14.70 / UI.json 3812 = Trockenlauf; `luacheck_pz --unused` 6 harmlose Reste (siehe 3). FR "Nourriture : prêt"/"Caresses : prêt" unveraendert (Auftrag 10 nennt nur ES) -- Frage 6. |
| B1 major | geschlossen (SP); MP bewusst "Register gewinnt" | `S:server/BanditsNPCBearHeal.lua:271-282` `markAhead` (gleiches `u`, v2, gleiche Epoche `mark.r > rec.r`, oder Quell-Epoche `rec.healed`), `:289-358` `B.TakeNewerMark` (nur SP, geklemmt wie `B.Restore`, nie zurueck aus tame, Deckel mit `mine`-Abzug `:310-315`), gerufen in `bind` `:86` und Suchlauf Schritt 2 `World.lua:727-731` vor `B.Commit`. Selbst durchgerechnet: Kevins Fall (Eintrag `fed` bond `__sp`, Spiegel `tame` owner `__sp`, r 3 > 2) -> `SlotsOf("__sp").bears` = 0 (der fed-Eintrag zaehlt als `bonded`, nicht als `bears`, `Registry.lua:388-391`) -> uebernommen. Pruefer Bs Fall 1a jetzt OK. Im laufenden Spiel ist `mark.r <= rec.r` (jede Spiegel-Schrift traegt das aktuelle `r`, `Registry.lua:419-422`, `Heal.lua:69-73`) -- kein Fehlgriff ausserhalb eines Absturzes. MP: Frage 2. |
| B2 major | geschlossen (Zaeune/Ecken ungeprueft) | `S:server/BanditsNPCBearWorld.lua:224-290`: `sq:getRoom() == room` und `reach` (je Schritt `not cur:isBlockedTo(nxt)`, hoechstens 3, Chebyshev-Abstand <= 3 reicht immer); Belege selbst gelesen: `V:shared/Util/AdjacentFreeTileFinder.lua:240` (`playerSq:getRoom() == gridSquare:getRoom()`), `V:shared/Foraging/ISForageAction.lua:7` und `V:shared/TimedActions/ISDropWorldItemAction.lua:7` (`square:isBlockedTo(square)`). `ringCell` von Hand nachgerechnet: deckt je Ring genau 8k Kacheln einmal ab. Anfang `(gen*3) mod 8k`; `B.PlaceCub` zaehlt `gen` hoch (`Ride.lua:72`), alle drei Aufrufer geben `rec.gen` (`Ride.lua:166`, `:200`, `:308`). Attrappe 10h + Pruefer Bs 2a/2b gruen. |
| B3 minor | geschlossen (SP; MP-Rest N1) | `World.lua:623-629` `newerFirst` (gen, r, Listenplatz -- strenge Ordnung), `:756`; `Heal.lua:378-381` Umbindung nur SP. Pruefer Bs 1b jetzt OK (Bruno, gen 1, echter Koerper bleibt). `table.sort` mit Vergleich: `V:shared/NPCs/MainCreationMethods.lua:127` selbst gelesen. |
| B4 minor | = A1, geschlossen | wie A1. |
| B5 minor | geschlossen | `World.lua:877-878` merkt `s.tx/s.ty/s.td0`; `Guard.lua:202-211` "away" nur bei follow + Rennbefehl + nicht in Ruhe; `ownAway` 3 / `ownAwayQuietMs` 5000 in `S:shared/BanditsNPCBear.lua:86`; `Ride.lua:57` leert die Felder. Ein Fehlalarm (Umweg) loest hoechstens einen neuen Lauf zum Besitzer aus -- harmlos. Attrappe 10i gruen. |
| B6 minor | offen (nur Kommentar, zu Recht) | `Guard.lua:169-173` beschreibt ehrlich: beim Bleiben kommt das Junge auf Q nicht. Kein Code geaendert -- Frage 4. |
| B7 minor | offen (Kevins Wort, zu Recht) | `S:shared/BanditsNPCBearRules.lua:607-627` unveraendert; Pruefer Bs 3a endet am Besitzer (haengt nicht). Gehoert zu B5a -- Frage 5. |
| B8 minor | geschlossen | `World.lua:382-389` Rahmen aller Punkte +- r einmal je Aufruf; `:400` (Cache) und `:429` (Zellenliste) je Zombie zuerst 4 Vergleiche; ausserhalb nur getX/getY (Attrappe 10k zaehlt 2 Aufrufe). |
| B9 minor | geschlossen (Rest: Kopie nach Absturz direkt beim Spieler) | `Ride.lua:318-325`: altes Tier nicht gefunden und Gegend geladen -> EIN `B.ScanAnimals(nil)` (Merker `B._callScanAt`, je `scanMs`), dann `:333` entfernen. Ein Argument -> die force-Regel bleibt sauber (Trockenlauf 0 Funde). |
| B10 minor | teils (Teil 2 offen, MP) | `Heal.lua:396-399`: MP, gleiche gen, andere AnimalID -> nicht binden, nichts entfernen, eine Zeile. Teil 2 (`mg > rg`) nicht gebaut, ehrlich genannt; kein Diebstahl moeglich (Besitzer bleibt). |

## 3. Selbst laufen lassen (Zahlen, 11.11.2026 ~05:45)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (23 Lua im Staging) | 23 file(s) checked, 0 failed |
| `scopecheck.py` | 23 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 39 (Bench `client/NCBearBenchCub.lua` ab :369); kopiert hoechstens 37 (`World.lua` ab :640 und :372, `Server.lua` ab :909, `Hud.lua` ab :289); insgesamt hoechstens 77 (`World.lua` ab :640) -- unter 180/200 |
| `luacheck_pz.py` (23) | 16 x W113, alle erwartet: 3 Aktionsklassen (`Menu.lua:86/97/107`), 13 Bench (`NCBearBenchCub.lua:756-769`) |
| `luacheck_pz.py --unused` (22 kopierte) | 9 Treffer = die 3 W113 + 6 harmlose: `Hud.lua:472-474` self (B1b), `Guard.lua:282` players (Signatur), `Rules.lua:41` W311, `:160` slots (B1a) |
| Eigene Dateiform (49 Dateien) | LF, kein BOM, LF am Ende, keine Leerzeichen am Zeilenende, Lua/.txt ASCII, JSON Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert: 0 Probleme |
| `attrappe/kern/run.lua` | 136 bestanden, 0 Fehler (byte-gleich `kern/ergebnis.txt`) |
| `attrappe/b1b_kern/run.lua` | 204 / 0 (byte-gleich `ergebnis.txt`) |
| `attrappe/b1c_kern/run.lua` | 192 / 0 (byte-gleich `ergebnis.txt`; Abschnitt 10 mit A1/A2/B1/B2/B3/B5/B8/B9/B10) |
| `attrappe/gesamt/run.lua` gegen das Staging | 812 / 0, byte-gleich `gesamt/ergebnis.txt` (einzige `***`-Zeile die gewollte Heilung 18c) |
| dieselbe gegen MEINE Probe (`.../scratchpad/gp/probe_gegen/NPCCrew/42/media/lua/`) | 812 / 0, byte-gleich `gesamt/ergebnis_probe.txt` |
| `attrappe/ober` / `b1b_ober` / `b1c_ober` (ohne / mit `kern`) | 116/0 + 117/0, 144/0 + 134/0, 193/0 + 180/0 |
| `attrappe/pruef_b1c/run.lua` (Pruefer B, unveraendert) | 6 x OK, 0 x BEFUND (byte-gleich `ergebnis_nach.txt`) |
| `attrappe/pruef_b1b/run_nach.lua` | 13 OK, 3 BEFUND = 3a (B1c-Absicht: Bobs Junges faehrt jetzt mit statt zu bleiben), 3b (B1b-A7-Lesart), 3i (klein, B1b) -- byte-gleich `ergebnis_b1c.txt` |
| `attrappe/pruef_b1b/run.lua` (roh, echtes Lua 5.1) | 10 OK, 6 BEFUND: die drei oben + 3d/3e/3f (Lua 5.1 zaehlt Bytes, unter Kahlua nicht -- wie im B1b-Gegenbericht) |
| `attrappe/pruef_b/run.lua` (B1a) | 7 OK, 1 BEFUND = bekannter B1a-Punkt 2a; byte-gleich `ergebnis_b1b_nach.txt` |
| `texte_pruefen.py` / `_b1b` / `_b1c` | FEHLER gesamt: 0 / 0 / 0 |
| `belege.py` / `_b1b` / `_b1c` | abweichend 0 von 112 / 0 von 51 / 0 von 89 |
| `gesamt/xref_b1c.py` | 0 Luecken, 3 Hinweise (Rueckfallwerte followLead/walkDist/walkSpeed, nur ohne B.CFG-Feld) |
| `uebernahme_force/probe_force.py` / `uebernahme_b1c/probe_regeln.py` | 23 / 0 und 34 / 0 |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten B5a, GLB-Clips, NC-Kommentar `shared/BanditsNPC.lua:1359`); 22 Lua, 5678 Codezeilen, Cheat-Funde 0, Tier-Regeln genau an ihren Orten, Kollision keine, "101 benutzt, fehlen in EN: 0"; UI.json 3812 -> 3921, Sandbox.json 92 -> 141 (49 neu, `Sandbox_BanditsNPC` gleich), IG_UI.json neu 3 |
| Trockenlauf ohne `--vor-b5a` | NICHT OK -- 24 Fehler (genau die Altlasten aus ALT_EXPECTED), 2 Warnungen, Exit 1 -- erwartet rot |
| Probe `--probe <scratchpad>/gp/probe_gegen --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, 49 Dateien geschrieben; je kopierter Datei luacheck/scopecheck/localcount ok; luacheck_pz 0 + 3 erlaubt; in der Probe keine Bench-Datei, kein `NCBear_Cub`; Bild `42/media/ui/BanditsNPCBearCub_marker.png` da |

### 3.1 `staging_dateien.txt` gegen die Platte und die Test-Mod nachgezaehlt
49 Dateien auf der Platte = 49 in der Liste; MD5, Bytes und Status jeder Zeile stimmen (0 Abweichungen). Gegen `Zomboid/mods/NCBearTest`
heute: **7 neu** (Options, Map, Marker, Guard, Heal, Ride, `42/media/ui/BanditsNPCBearCub_marker.png`), **25 ueberschreibt**, **17 gleich**.
Ueberschrieben wuerden nur eigene, gewollte Dateien:
- 9 Kern-/Oberflaechen-Lua: `client/BanditsNPCBearClient.lua`, `client/BanditsNPCBearMenu.lua`, `client/ISUI/BanditsNPCBearHud.lua`,
  `server/BanditsNPCBearFollow.lua`, `...Registry.lua`, `...Server.lua`, `...World.lua`, `shared/BanditsNPCBear.lua`, `shared/BanditsNPCBearRules.lua`;
- die Testhilfe `client/NCBearBenchCub.lua` (nie nach NPC Crew);
- 14 Texte: je Sprache UI.json 94 -> 109, Sandbox.json 46 -> 50, **kein Schluessel geht verloren**; geaendert nur `Menu_FollowTip`,
  `Note_StayCar` (Mitfahren) und in ES `Hud_Pet` ("Caricia: %1", Auftrag 10);
- `sandbox-options.txt`: 20 -> 22 Optionen, keine faellt weg, neu `BanditsNPC.BearRideDistance`, `BanditsNPC.BearCallCooldownMinutes`.
Keine alte `NCBear*`-Datei des Erwachsenen (34 Test-Mod-Dateien ausserhalb des Stagings bleiben unberuehrt), kein `mod.info` (Vorschlag
getrennt in `mod_info_vorschlag.txt`). Einbau nur bei geschlossenem Spiel.

## 4. Eigene Stichproben

**Stichprobe 1 -- Folgen und Mitfahren im MP-Zweig Zeile fuer Zeile** (Server -> Tier -> Register): Hirn-Takt `Server.lua:909-1000`:
zuerst `B.RideStep` fuer jeden `rec.ride` (`:916-921`), dann `resolve` (mitfahrend = nie "fehlt", `:793-794`), `liveRec` `:726-780`:
Laerm-Wache `B.CalmWatch` nur `tame` (`:740`), `buildEnv` `:635-676` (Besitzer = naechster Spieler mit `rec.owner`-Schluessel aus
`B.Players()` = `getOnlinePlayers()` am Server, `car` aus `p:getVehicle()`, `World.lua:41-55`), Zombie-Wache zuerst (`:762`; Ausnahme
"Besitzer im Auto und nah" `Guard.lua:295-297`), dann `B.FollowStep` `Follow.lua:128-169` -> `B.FollowDecide` `Rules.lua:469-550`
(Regel 11: `o.car` und `d <= BearRideDistance` -> "ride", sonst "stay"/"car"). Einsteigen `Ride.lua:98-121`: Definition da, Sitzung
geloest, `rec.ride = { at }`, `gen + 1`, Lage = Besitzer, `B.Commit` (ohne Objekt kein Spiegel), `B.RemoveCub` (am Server mit
`removeAnimal(getOnlineID())`, `World.lua:495-503`). Waehrend der Fahrt `Ride.lua:150-215`: Lage = Besitzer (ohne Touch), im Auto
warten; zu Fuss erst nach `rideOffMsMP` 3 s und <= 4 Kacheln/s (`:193-199`), Platz ueber `B.SpotNear` (B2), `B.PlaceCub` -> `B.CreateCub`
(einziger belegter Erzeugungsweg), "follow", Meldung nur an den Besitzer. Abgemeldet: `ownerEntry` nil, `B.DeadAt` nil -> wartet, `ride`
bleibt im Register (`Registry.lua:156-162` prueft ihn beim Laden). Tot im Auto: `B.DeadAt` + 5 s + Gegend geladen -> neben der Leiche,
"stay". Ergebnis: **was gilt, kommt nur aus dem Register und den Server-Objekten**; kein Client-Glaube; ein Koerper je Eintrag (gen schuetzt
vor Doppeln: `Heal.lua:373`, `:392`). Ungeprueft (Laufzeit, schon Kevins MP-Testpunkte): `getVehicle()` fremder Spieler am Server
waehrend der Fahrt, Gang-Animation der Client-Kopie nach `setVariable("animalRunning", false)` am Server, A3 aus B1a.

**Stichprobe 2 -- eine Sprache ganz gegengelesen: Franzoesisch (FR)**, alle 109 UI-Texte und die 4 neuen Sandbox-Texte gegen EN:
inhaltlich richtig und natuerlich ("Viens ici", "Ramène votre ourson juste à côté de vous s'il est coincé. Utilisable une fois toutes les
%1 minutes.", "Votre ourson monte avec vous." / "saute dehors.", "Ourson à proximité", "NPC Crew : Ours", "Taille de l'affichage
au-dessus des ours (%%)" -- `%%` wie Vanilla `UI_optionscreen_ActionProgressBarSize1`). Platzhalter vollstaendig. Einziger Fehler wie
bekannt: `Hud_Ready` "prêt" passt nicht zu "Nourriture" (f.) und "Caresses" (f. Pl.) -- Frage 6. ES `Hud_Pet` jetzt "Caricia: %1"
(Einzahl zu "lista") -- Auftrag 10 erfuellt.

**Stichprobe 3 (Zusatz) -- Kevins Spielstand nach dem Einbau:** sein Register (B1b-Form, b1 wild, b2 angefuettert, Spiegel v1 `{id, st}`)
wird beim Laden v2 (`Registry.lua:106-163`: Epoche, `u` je Eintrag), der Suchlauf bindet die Tiere ueber den AnimalID-Rueckfall (v1-Spiegel
ohne `u` gilt als derselbe Koerper, `World.lua:709`), `B.Commit` schreibt Spiegel v2. Die alte, beim Absturz verlorene Zaehmung (N9)
kommt NICHT zurueck (das Register ist da und widerspricht nicht -- richtig so); b2 bleibt angefuettert. Fuer den Test deshalb erst zaehmen
(Anleitung).

## 5. Neue Restbefunde (keiner rot, keiner verhindert den Test)

- **N1 (minor, nur MP, selten):** B3 im Mehrspieler ueber ZWEI Suchlaeufe: wird nach einem Server-Absturz mit verlorenem Register zuerst
  eine alte Kopie hergestellt und erst spaeter der echte Koerper (hoehere gen) geladen, ist dieser "dup" (`Heal.lua:378` nur SP, dann
  `:384-390`) und wird unbeobachtet entfernt -- der alte Stand (Name, Modus) bleibt. Kein Gegenstand, kein Doppel, ein Junges bleibt.
  Im selben Suchlauf gewinnt auch im MP der neuere (Sortierung `World.lua:756`).
- **N2 (Hinweis, Gefuehl):** Gehen zeigt sich heute selten: nur wenn der Besitzer fast steht (<= `walkSpeed` 0,52 Kacheln/s) UND die
  Reststrecke <= `walkDist` 3 ist (`Rules.lua:530`, `S:shared/BanditsNPCBear.lua:88`); weil das Junge unter 3 bzw. 4,5 Kacheln haelt
  (`Rules.lua:500`), bleibt dafuer nur ein schmales Fenster (Abstand ~3-5 Kacheln). So gewollt (Auftrag 6: Platzhalter-Modell geht 0,52
  Kacheln/s, darf nicht zurueckfallen). Zum Ansehen im Test: `NCBear_CubSet("walkDist", 6)`. Mit dem neuen Modell neu einstellen.
- **N3 (Kleinkram):** `baer/NAEHTE.md:116` nennt `NC shared/BanditsNPC.lua:1357 (v3.14.68)`, der Trockenlauf findet die Stelle heute bei
  `:1359` (v3.14.70). Nur eine wandernde Zeilennummer (NAEHTE Kopf: "es zaehlt die Fundstelle").

Weiter offen (aus den Berichten, unveraendert gueltig): B9-Rest (alte Kopie nach Absturz direkt beim Spieler, bis 25 Kacheln weg; zerlegbar),
B10 Teil 2 (MP "umsetzen" ohne Diebstahl), ob `isBlockedTo` niedrige Zaeune und Diagonal-Ecken erfasst, ob Zellen beim Entladen vor dem
naechsten Speichern geschrieben werden (macht B1 haeufig oder selten), A3 aus B1a (`getObjectListForLua`/`getAnimalID` am MP-Server).

## 6. Fragen an Kevin (alle mit Empfehlung; keine haelt den Test auf)
1. **A3:** Duerfen Vanilla-Lua-Bausteine, deren Code ganz gelesen ist, die aber niemand aufruft (`addTickBox`, `addSlider` der
   Optionen-Seite), als Beleg zaehlen? Empfehlung: ja, als Regel-Auslegung festhalten (es sind keine Engine-Methoden).
2. **B1 Mehrspieler:** nach einem Server-Absturz gewinnt dort das aeltere Register, auch wenn das Tier einen neueren Stand traegt (sonst
   koennte ein veraenderter Client Zaehmung vortaeuschen); im Einzelspieler gewinnt der neuere Stand. Empfehlung: ja.
3. **A1 Grenze (MP):** ein Junges mit einem nie herstellbaren alten Spiegel bleibt unberuehrbar stehen statt wild zu werden. Empfehlung:
   so lassen (braucht einen B1a/B1b-MP-Spielstand, den es nicht gibt).
4. **B6:** Q holt ein FOLGENDES Junges heran; ein BLEIBENDES kommt auf Q nicht. Empfehlung: im Test ansehen.
5. **B7:** steht ein Zombie zwischen dir (mehr als 10 Kacheln weg) und deinem Jungen, rennt es erst weg und kommt dann zurueck. Lieber
   stehen bleiben? Empfehlung: ja, zusammen mit B5a.
6. **FR-Text:** "prêt" -> "prête" und "Caresse : %1" (Einzahl wie ES)? Empfehlung: aendern.
7. **Gehen (N2):** Soll es oefter gehen (z. B. bis 6 Kacheln, solange du stehst)? Empfehlung: erst mit dem neuen, schnelleren Modell
   einstellen; im Test mit `NCBear_CubSet("walkDist", 6)` ansehen.

Statisch geprueft, nicht gespielt. Nach dem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).
