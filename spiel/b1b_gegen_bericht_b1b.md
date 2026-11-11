# Gegenpruefung B1b "baer-b1b" (11.11.2026)

Rolle: Gegenpruefer. Nichts davon gebaut, keinem Bericht geglaubt: jede Stelle der 16 Befunde und ihre Umgebung im heutigen Staging
gelesen, die Engine-Lesarten der Nachbesserung im javap nachgesehen, alle Pruefer und Attrappen selbst laufen lassen, dazu eine eigene
kleine Folgen-Simulation gegen das echte `shared/BanditsNPCBearRules.lua`. **Statisch geprueft, nicht gespielt.** Geschrieben nur diese
Datei und `anleitung_b1b_entwurf.md`; die Probe lief in einen eigenen Scratchpad-Ordner (nicht `_arbeit/.../probe_b1b`). Kein git, kein
Spiel, nichts in die Test-Mod (das Spiel lief waehrend der Pruefung: `ProjectZomboid64.exe`). Kurzformen: `S:` Staging
`mod/42/media/lua/`, `V:` Vanilla `media/lua/`.

## 1. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test. Kein Blocker.** Alle 16 Befunde am heutigen Code nachgesehen: 13 geschlossen,
3 bewusst nur teilweise (A3 Zeile 2 nicht kleiner moeglich, A6 Waisen-Lauf am MP-Server bleibt Testpunkt, A7 Zustand bei Abmelden:
Plan-Lesart geaendert) -- alle drei ehrlich im Code und im Bericht genannt, keiner davon stoert den SP-Test. Kein Befund zu Unrecht
abgelehnt (es wurde keiner abgelehnt). Die Nachbesserung hat nichts kaputt gemacht, was ich finden konnte: alle Attrappen gruen,
Fix 2 (`tHas`, `S:shared/BanditsNPCBear.lua:259-269`) und Fix 3 (`petting = PetAnimalCalf`, `S:shared/BanditsNPCBearDefs.lua:60`,
`S:shared/TimedActions/BanditsNPCBearPetAction.lua:66/76`) sind drin, das Streicheln selbst ist unberuehrt. Vier neue kleine
Restbefunde (N1-N4), keiner rot.

## 2. Je Befund (Zeilen = heutiges Staging)

| ID | Urteil | Beleg im heutigen Code / selbst nachgesehen |
|---|---|---|
| A1 major | geschlossen | `S:shared/BanditsNPCBearRules.lua:387-411` `B.CleanName` nur noch `string.len`, `string.sub`, Textvergleiche; grep `string.byte`/`:byte(`/`string.char` im Staging: 0 Code-Treffer (nur der Kommentar `:337`). `string.sub`/`string.len` hat Vanilla (`V:shared/luautils.lua:5`), Textvergleich `<` `V:client/DebugUIs/DebugMenu/Entity/ISEntityScriptsPanel.lua:149` (selbst gelesen). |
| A2 minor | geschlossen (Rest N2) | `NAME_BADR` `Rules.lua:347-361` (DEL, C1, U+00AD, U+061C, Hangul-Fueller, U+180E, U+200B-200F, U+2028-202E, U+2060-206F, U+FEFF, U+FFF9-FFFB), `NAME_SPACE` `:363-371`, Rand-Leerraum weg, nur Leerraum = abgelehnt (`:403-409`). Lesart selbst im javap geprueft: `LexState.newstring` = `new String(bytes, "UTF-8")` (`javap/b1b_nach_LexState.txt:601-612`), Dezimal-Escape bis 255 geht per `save(int)` in den Byte-Puffer (`:1002-1021`) -> `"\226\128\139"` ist unter Kahlua EIN Zeichen; `StringLib.sub` -> `String.substring` (`b1b_nach_StringLib.txt`, Abschnitt sub); Textvergleich `KahluaThread` -> `String.compareTo` (`b1b_nach_KahluaThread.txt`, ~Bytecode 2438). Unter echtem Lua 5.1 (Attrappe ohne Zeichen-Modell) greifen die Grenzen ueber 127 NICHT -- erwartet, im Code-Kommentar `:342-345` genannt. |
| A3 minor | teils (zu Recht) | `S:client/ISUI/BanditsNPCBearHud.lua:409-425`. Selbst nachgesehen: in allen 8 Sprachordnern `media/fonts/<L>/fonts.txt` laden `font Small` und `font NewSmall` dieselbe Datei (CH/CN zomboidSmallChinese, EN/PL zomboidSmall, JP, KO, RU Cyrillic, TH). Zeile 2 ist also gleich gross, nur blasser (`:341` Farbe 0,78 / Deckkraft 0,80). Kleiner nur mit `drawTextZoomed` (kein Vanilla-Aufruf -> Kevins Wort). Frage an Kevin, stoert den Test nicht. |
| A4 minor | geschlossen | `S:server/BanditsNPCBearWorld.lua:29` nennt jetzt `V:server/XpSystem/XpUpdate.lua:298` -- selbst gelesen (`:294-298`: `isServer() and players:get(i) or getSpecificPlayer(i)`, dann `playerObj:isDead()`), kein Kommentarblock. `bau_b1b_kern.md:92` streicht `season.lua:139`. `V:server/Vehicles/VehicleCommands.lua:11` (`player:getVehicle()`) selbst gelesen. |
| A5 minor | geschlossen | `baer/tools/baer_uebernahme.py:190-220` `scan_force_hits` zerlegt jede Erwaehnung von `ScanAnimals` dateiweit (Kommentare weg), zaehlt Argumente mit `call_args`, `:` zaehlt `self` mit, ohne Klammer = Fund. `uebernahme_force/probe_force.py` selbst gelaufen: 23 Faelle, 0 Fehler. Im kopierten Code nur `Server.lua:880` und `:917` mit einem Argument; Trockenlauf 0 Funde. |
| A6 minor | teils (zu Recht) | Kommentare jetzt ehrlich: `S:server/BanditsNPCBearServer.lua:576-581` (A3-Ausnahme `getObjectListForLua`/`getAnimalID` am Server genannt) und `:909-914`. Der Lauf selbst (`:915-918`, je 120 s, auch ohne Junges) ist unveraendert; Fehler wuerden je 60 s als `brain tick: ...` geloggt (`:930-931`, `B.ErrEvery`), kein Verschlucken. Bleibt Kevins MP-Testpunkt (PLAN_B1B.md 8.4 MP 7). Im SP belegt (`V:client/DebugUIs/DebugContextMenu.lua:612-615`). |
| A7 minor | geschlossen durch Plan-Aenderung (Frage) | `Rules.lua:450-453` Regel 10: Besitzer fehlt -> `hold`, `rec.mode` bleibt "follow". `S:server/BanditsNPCBearFollow.lua:168-176` `B.FollowLost` nur mit Objekt in dieser Sitzung UND anwesendem Besitzer. Folge im MP: das Junge eines Abgemeldeten steht still (`setBlockMovement` je Takt), solange andere die Gegend laden. Kevins Wort steht aus (Frage 2). |
| A8 minor | geschlossen | `S:shared/BanditsNPCBear.lua:92-93` Vorgaben 4 / 3; `sandbox-options.txt` selbst gegen die Test-Mod gedifft: nur Zeile 84 (14 -> 4), 92 (8 -> 3) und die neue Option `BearFollowMaxDistance`. Tooltips ohne Zahlen (EN/ES/FR gelesen). Kevins laufender Spielstand behaelt 14 / 8. |
| B1 blocker | geschlossen | `Rules.lua:438-445` `gainToward` (Weg des Jungen auf den Besitzer zu), `:476-486`. **Eigene Simulation** (echtes Rules.lua, Takt 1,5 s, Junges laeuft geradlinig mit fester Geschwindigkeit): Besitzer geht 2,27 Kachel/s, Junges 2,47, 120 s -> nie "fest", 81 Laufbefehle, Abstand ab 20 s hoechstens 3,91, Ende 3,90. Junges 2,20 -> nie fest, Ende 13,5 (faellt langsam zurueck, Tempo). Sprinten 4,5 -> nie fest, nach ~20 s `stay`/"far" bei 41,8. Deckt sich mit `attrappe/b1b_kern` 11a-e. |
| B2 minor | geschlossen (Preis N1) | `Rules.lua:461-470` Vorhalt, gedeckelt `followLead` 1,5; Owner-Weg aus `B._pp` (`Server.lua:654-658`). Eigene Simulation: Gehen ~3,9 Kacheln Abstand (Auftrag "etwa 2-4"). Preis: Besitzer bleibt abrupt stehen -> Ende 0,50 Kacheln (siehe N1). |
| B3 minor | geschlossen | `Follow.lua:170-171`: `B.FollowLost` nur, wenn `B._s[id].obj` in dieser Sitzung gesetzt war. `s.obj` wird nie geleert (nur `B.Close`, `Registry.lua:346`), deshalb greift "zurueckgeblieben" nach einem Entladen weiter (`B.FindAnimal` prueft `isExistInTheWorld`, `World.lua:272`). |
| B4 minor | geschlossen (mit A2, Rest N2) | wie A2. `pruef_b1b/run_nach.lua` (Zeichen-Modell an): 3d/3e/3f jetzt OK. |
| B5 minor | geschlossen | `Follow.lua:52-81`: Schluessel "Spieler|Befehl|ok/no", gezaehlt erst nach den Pruefungen (`:224`, `:254`), Ablehnungen ueber `refuse` (`:79-81`), Deckel 128 (`:61-68`). |
| B6 minor | geschlossen | `S:client/BanditsNPCBearMenu.lua:361` eigenes zahmes Junges nur, wenn es NICHT folgt. |
| B7 minor | geschlossen (Frage) | `S:shared/BanditsNPCBear.lua:73` `stayR = 12`; Regel 8 `Rules.lua:316-319`, Server `:733`. Gefuehl im Spiel offen (Frage 3). |
| B8 minor | geschlossen (Rest N3) | `S:shared/BanditsNPCBear.lua:285-288` Server: Konto `__sp` bekommt keinen Schluessel; Client `Hud.lua:153`, `:166`, `S:client/BanditsNPCBearClient.lua:212-213`: `__sp` nur im SP "eigen", im MP "?". |

## 3. Selbst laufen lassen (Zahlen, 11.11.2026)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (17 Lua im Staging) | 17 file(s) checked, 0 failed |
| `scopecheck.py` | 17 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 39 (`client/NCBearBenchCub.lua` Funktion ab :319), insgesamt hoechstens 54 (`server/BanditsNPCBearWorld.lua` `B.ScanAnimals` ab :354) -- unter 180/200 |
| `luacheck_pz.py` | 14 x W113, alle erwartet: 3 Aktionsklassen (`Menu.lua:84/95/105`), 11 Bench (`NCBearBenchCub.lua:536-547`) |
| `attrappe/kern/run.lua` | 136 bestanden, 0 Fehler (einzige `***`-Zeile die erwartete aus Fall 4) |
| `attrappe/b1b_kern/run.lua` | 203 bestanden, 0 Fehler (`***` nur die 3 erwarteten aus 6b) |
| `attrappe/gesamt/run.lua` | 486 bestanden, 0 Fehler -- gegen das Staging UND gegen meine eigene Probe (`.../scratchpad/probe_gegen/NPCCrew/42/media/lua/`): 486 / 0 |
| `attrappe/ober/run.lua` ohne / mit Kern | 116 ok / 117 ok, 0 Fehler |
| `attrappe/b1b_ober/run.lua` ohne / mit Kern | 144 ok / 134 ok, 0 Fehler |
| `attrappe/pruef_b1b/run_nach.lua` (Zeichen-Modell an) | 15 OK, 1 BEFUND = 3b (erwartet: Pruefer B erwartete noch "offline -> stay", A7 absichtlich anders) |
| `attrappe/pruef_b1b/run.lua` (roh, echtes Lua 5.1) | BEFUND 3b (wie oben) und 3d/3e/3f (echtes Lua 5.1 zaehlt Bytes -- unter Kahlua nicht, siehe A2) |
| `attrappe/pruef_b/run.lua` (B1a) | 7 OK, 1 BEFUND = bekannter B1a-Punkt 2a (Eintraege Abwesender bleiben; Kevin-Frage aus B1a) |
| `gesamt/xref_b1b.py` | 0 Luecken, 0 Hinweise |
| `ober/texte_pruefen.py` / `b1b_ober/texte_pruefen_b1b.py` | FEHLER gesamt: 0 / 0 |
| `ober/belege.py` / `b1b_ober/belege_b1b.py` | abweichend 0 von 112 / 0 von 51 |
| `uebernahme_force/probe_force.py` | 23 Faelle, 0 Fehler |
| Eigene Dateiform-Pruefung (42 Dateien) | LF, kein BOM, Zeilenende am Schluss, Lua/.txt reines ASCII, JSON Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert: 0 Probleme |
| Eigene Textpruefung (7 Sprachen) | UI.json 94 / Sandbox.json 46 Schluessel je Sprache, keiner fehlt/zu viel, Platzhalter `%n` und `%%` gleich wie EN, kein `<`/`>`, CN: alle Zeichen kommen in Vanilla-CN vor; `Note_Tamed` nennt in jeder Sprache woertlich den Menuetext von "Follow me" |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten B5a, GLB-Clips, NPC-Crew-Kommentar `shared/BanditsNPC.lua:1358`), Cheat-Funde 0, wuerde 42 Dateien schreiben |
| Probe `--probe <scratchpad>/probe_gegen --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, 42 Dateien geschrieben; je kopierter Datei luacheck/scopecheck/localcount ok; luacheck_pz 0 + 3 erlaubt; UI.json 3810 -> 3904, Sandbox.json 92 -> 137, IG_UI.json neu 3 je Sprache; keine Bench-Datei und kein `NCBear_Cub` in der Probe |
| Eigene Folgen-Simulation (`.../scratchpad/sim/sim.lua`) | siehe B1/B2 |

### 3.1 `staging_dateien.txt` gegen die Platte und die Test-Mod nachgezaehlt
42 Dateien auf der Platte = 42 in der Liste; MD5, Bytes und Status jeder Zeile stimmen (0 Abweichungen). Gegen
`Zomboid/mods/NCBearTest` heute: **2 neu** (`server/BanditsNPCBearFollow.lua`, `client/ISUI/BanditsNPCBearNameBox.lua`),
**26 ueberschreibt**, **14 gleich**. Ueberschrieben wuerden nur eigene Dateien:
- 10 Kern-/Oberflaechen-Lua: `client/BanditsNPCBearClient.lua`, `client/BanditsNPCBearMenu.lua`, `client/ISUI/BanditsNPCBearHud.lua`,
  `server/BanditsNPCBearRegistry.lua`, `server/BanditsNPCBearServer.lua`, `server/BanditsNPCBearWorld.lua`, `shared/BanditsNPCBear.lua`,
  `shared/BanditsNPCBearDefs.lua` (Fix 3), `shared/BanditsNPCBearRules.lua`, `shared/TimedActions/BanditsNPCBearPetAction.lua` (Fix 3);
- die Testhilfe `client/NCBearBenchCub.lua` (wird nie nach NPC Crew kopiert);
- 14 Texte `Translate/<L>/UI.json` und `Sandbox.json`: je Sprache **kein Schluessel geht verloren**, UI +20, Sandbox +2, geaendert nur
  `UI_BN_Bear_Note_Tamed` (neuer Hinweis auf "Follow me");
- `sandbox-options.txt`: keine Option faellt weg; Vorgaben 14 -> 4 und 8 -> 3, neu `BanditsNPC.BearFollowMaxDistance`.
Keine alte `NCBear*`-Datei des Erwachsenen, kein `mod.info` wird beruehrt. Einbau erst, wenn Kevin das Spiel geschlossen hat.

## 4. Eigene Stichproben

**Stichprobe 1 -- Folgen im MP-Zweig Zeile fuer Zeile** (Client -> Server -> Tier -> Sicht):
Menue `Menu.lua:256` nur bei `v.st == "tame"` und `v.owner == key` (Client-Schluessel = Kontoname, `BanditsNPCBear.lua:283-291`) ->
`onMode` `:117-121` -> `B.Ask` `BanditsNPCBear.lua:445-449` `sendClientCommand(player, B.CMD, "Mode", {id, mode})` (nie leer). Server:
`Server.lua:403-409` filtert Modul, `nil -> {}`, `B.Handle` `:389-391` -> `B.HandleMode` `Follow.lua:196-227`: Schreiber, Register, `id`
als Text, Besitzer laut Register (nicht laut Client), Junges geladen (`B.FindAnimal`), Fahrzeug und Abstand am SERVER-Spieler, Drossel,
`B.SetMode` (`:89-119`: Zustand, bei "stay" Heimat = Standort, Sitzung geleert, `B.Commit`, Meldung nur an den Besitzer) und
`B.FlushViews`. Hirn-Takt `Server.lua:859-919` -> `liveRec` `:721-723` -> `B.FollowStep` `Follow.lua:126-158` mit `env.owner` aus
`buildEnv` `:623-661` (naechster Spieler mit dem Besitzer-Schluessel, `car` aus `B.Players` `World.lua:44-45`) -> `B.FollowDecide`
-> `B.MoveTo` (`fleeTo`, `World.lua:493-526`) bzw. `B.Hold`. Sicht an die Clients: `viewEntry` `Registry.lua:421-437` traegt `name` und
`mode`; fremde Clients zeigen "<Name>" / "belongs to <Konto>" (`Hud.lua:163-169`). Ergebnis: **was gilt, kommt nur aus dem Register und
den Server-Objekten**; kein Client-Glaube. Ungeprueft (Laufzeit): ob `fleeTo` am Server fluessig bei den Clients ankommt (B1a-Weg),
A3 (`getObjectListForLua` am Server). Kleiner Nebenfund N3 (s. u.).

**Stichprobe 2 -- eine Sprache ganz gegengelesen: Spanisch (ES)**, alle 94 UI-Texte und die neuen Sandbox-Texte gegen EN: inhaltlich
richtig und natuerlich ("Sígueme", "Quédate aquí", "Cría de %1", "te sigue" / "se queda aquí", "pertenece a %1", "Ofrecer comida a la
cría", "Tu cría no pudo seguirte el ritmo. Te espera al %1."). Platzhalter vollstaendig. Einziger Schoenheitsfehler: "Caricias: lista"
(Einzahl "lista" zu Mehrzahl "Caricias"; B1a-Text, kein Fehler im Spiel).

**Stichprobe 3 (Zusatz) -- Kahlua-Lesart von `B.CleanName`** im javap selbst nachgesehen (siehe A2). Und: `for _, _ in pairs(...)`
(`Follow.lua:63`) hat keinen Vanilla-Treffer, laeuft aber schon im GESPIELTEN `NCBearTest/.../server/BanditsNPCBearRegistry.lua:115/140`
-- Kahlua nimmt die Form also an.

## 5. Neue Restbefunde (keiner rot, keiner verhindert den Test)

- **N1 (minor, Gefuehl):** bleibt der Besitzer nach dem Gehen abrupt stehen, laeuft das Junge bis ~0,5 Kacheln an ihn heran (Preis von B2;
  eigene Simulation Ende 0,50). Sieht vielleicht aus wie "rennt in mich rein". Stellwert `NCBear_CubSet("followLead", 1.0)` (weiter weg).
  Im Test ansehen.
- **N2 (minor, nur Anzeige):** `B.CleanName` laesst weiter durch, was die Schriften des Spiels nicht zeigen: Zeichen ueber U+FFFF (Emoji, unter
  Kahlua zwei Ersatzzeichen, zaehlen doppelt -- im Bericht genannt), ausserdem Privatbereich U+E000-F8FF, U+FFFC/FFFD und ein Name nur aus
  Kombinationszeichen (z. B. allein U+0301). Folge hoechstens ein Kaestchen oder fast leeres Schild; kein `<`, `>`, `%` kommt durch, kein
  Schaden. Spaeter, falls Kevin will.
- **N3 (minor, nur MP, Randfall):** `B.BuildView` (`Registry.lua:441, :449`): fuer ein Konto ohne Schluessel (nur das Konto "__sp", B8) ist
  `pkey == nil`, und `rec.bond == pkey` ist dann fuer jedes ungebundene Junge wahr -- dieses Konto bekaeme alle wilden Jungen (bis 16) in
  seine Sicht, gleich wie weit weg. Harmlos (nur Anzeige-Daten), ein Wort: `pkey ~= nil and (...)`.
- **N4 (Hinweis fuer den Test):** solange Kevin ein gezaehmtes Junges hat, lehnt `NCBear_CubHere()` ab ("You already have a bear",
  `BearMaxPerPlayer` 1). Die Anleitung testet deshalb erst das eigene Junge und raeumt erst danach mit `NCBear_CubClean()` auf (das entfernt
  auch das gezaehmte Junge). Und: Kevins laufender Spielstand zaehmt weiter mit 14 / 8 Punkten (gespeicherte Sandbox-Werte).

## 6. Offen / ungeprueft (unveraendert gueltig)
Alles Laufzeitverhalten: wirkliches Tempo von Junges und Spieler, Wege um Ecken, Tueren, Treppen, Q-Ruf, Schildhoehe `tagZ` 0,18,
Hinterherlaufen im MP (Ruckeln), A3 aus B1a (`getObjectListForLua`/`getAnimalID` am Server), `p:getVehicle()` fremder Spieler am Server,
ob PZ ein Konto `__sp` zulaesst, ob Namen mit Umlauten/Koreanisch die globale ModData unbeschadet durch Speichern/Laden bringen.

## 7. Fragen an Kevin (aus der Nachbesserung, alle mit Empfehlung; keine haelt den Test auf)
1. Zeile 2 des Schilds ist gleich gross wie Zeile 1, nur blasser (das Spiel hat keine kleinere Schrift). So lassen? (Empfehlung: ja, ansehen.)
2. Mehrspieler: meldet sich der Besitzer ab, wartet das folgende Junge stehend und folgt nach dem Einloggen weiter. Ok? (Empfehlung: ja.)
3. Bleiben-Radius 12 statt 8 -- im Test fuehlen (`NCBear_CubSet("stayR", 10)` zum Vergleich).
4. Abstand beim Folgen ~3-4 Kacheln beim Gehen, beim Stehenbleiben kommt es ganz nah (N1). Passt das?
5. Die neue Zaehm-Dauer (~12 Spielstunden) gilt nur in NEUEN Spielstaenden.

Statisch geprueft, nicht gespielt.
