# Lauf baer-fix1 -- GEGENPRUEFER

Stand 14.11.2026 ~10:30. **Statisch geprueft, nicht gespielt.** Nichts gebaut, BAU.md und PRUEF.md nicht geglaubt: jeder Punkt am Code nachgelesen, Diff
gegen die Test-Mod Datei fuer Datei, R1 mit eigener Stichprobe (Zufalls-Geschichten statt fester Faelle), alle Pruefer und Attrappen selbst gelaufen.
Geschrieben nur in `fix1/GEGEN.md`, `fix1/anleitung.md`, `fix1/gegen/` (Laeufe, `zeichen_pruefen.py`; Probe-Ordner danach geloescht) und
`attrappe/fix1_gegen/`. Kein Byte im Staging `mod_fix1`, in Test-Mod, NPC Crew, Vanilla, Bandits, `baer/tools`, `baer/NAEHTE.md`; kein git, kein Download,
kein Spielstart. Kuerzel: `S:` = `mod_fix1/42/media/lua/`, `V:` = Vanilla `media/lua/`, `G:` = `attrappe/fix1_gegen/lauf/`.

## 0. Ergebnis zuerst

- **Einbaubar: ja.** Alle sieben Punkte sind zu. Ich habe nichts gefunden, was fix1 kaputt macht: 15 Dateien anders als die Test-Mod (7 Lua + 8 UI.json),
  jede geaenderte Zeile gehoert zu R1-R6 oder G-R3. Keine Modell-Datei geaendert (33 byte-gleich), 0 neue Dateien.
- **R1 eigene Stichprobe** (`attrappe/fix1_gegen/gegen.lua`): 18 Zufalls-Geschichten, Absturz nach JEDEM Ereignis mit den Speicherstaenden, die es
  dann wirklich gaebe. Ebene 1: **309 / 309 ok** (die Test-Mod hat 12 doppelt), **0 Lagen schlechter** als die Test-Mod, 12 besser. Ebene 2 (zweiter
  Absturz in der Sitzung danach): 718 ok, **2 doppelt** -> eigener Befund **G5**, eine alte F4-Luecke (gibt es schon in der Test-Mod).
- **Zwei neue Restbefunde, kein Blocker:** **G5** (alt seit F4, rote Linie: doppelt UND weg, braucht zwei Abstuerze hintereinander; Vorschlag fuer
  eine Zeile, an einer Kopie geprueft) und **G4** (nur bei kaputtem Register: fix1 leert dann den Baeren). Dazu zwei Schoenheitsfehler.
- Pruefer: vier Lua-Pruefer 28 x rc 0; langcheck 8 Sprachen 0 Fehler, 3 Hinweise wie die Test-Mod; Uebernahme Trockenlauf und `--probe` OK
  (0 Fehler, 2 Warnungen wie bisher); 94 Attrappen-Ausgaben gleich wie gegen die Test-Mod, die anderen nur an den gewollten Stellen; Staging-Liste
  185 = 185 auf der Platte, 0 Abweichungen.

## 1. Die sieben Punkte -- geschlossen?

| ID | am Code (selbst gelesen) | Beleg | Urteil |
|---|---|---|---|
| **R1** | Stempel des Charakters `K.stamp` (`S:server/BanditsNPCBearInv.lua:224-239`), gesetzt beim ersten Abgleich (`:399`); der Abgleich verknuepft IMMER, leer mit Marke `e0`/`e0c` (`:344-353`); `K.linkFirst` (`:269-276`) VOR jeder Aenderung aus `K.check` (`:562`) und `K.healFirst` (`:259-265`: Fressen, Trinken, F5-`InvAddItem`, Tod); "Datei aelter als die erste Verknuepfung" nur bei `c == nil` (`:331`, Haertung des Pruefers) -> leerer Stand mit neuer Fassung r+1 (`:337`); leerer Baer stirbt -> Grabstein (`:928-939`); Werkbank loescht die Marke (`:1393`). Alle neuen Wege hinter `K.copyOn()` -> Mehrspieler wie vorher. | `G:gegen_fix1.txt` Ebene 1 309/309 (Test-Mod `G:gegen_testmod.txt` 297/309, alle 12 = "volles Speichern, Absturz vor dem Spieler"); `bau.lua` 105/0, `pruef.lua` 33/0 selbst gelaufen; `k1_gegen` G1b/G1W(a) jetzt Invariante true | **zu** |
| **R2** | Kopf `S:client/ISUI/BanditsNPCBearHud.lua:566-569` = Fenster `S:client/BanditsNPCBearWinData.lua:713-720` Zeichen fuer Zeichen (auf 0,1, ganz ohne Stelle) | `ober_fix1` 200/0 + 202/0; `k1_nach/ober_nach` NO1 jetzt rot = gewollt (alte Erwartung "+1") | **zu** |
| **R3** | `B.TrustAdd` "down" ohne Sperre (`S:server/BanditsNPCBearNeeds.lua:284-286`); Aufrufer `S:server/BanditsNPCBearHurt.lua:157`; Tooltip "every time it goes down" passt jetzt | `k1_nach_fix1` 40/0; Original `k1_nach` N3 3 rot und `k1_pruef` P6 = gewollt (Kevin 14.11. ~00:00 "verliert er -10") | **zu** |
| **R4** | `B.DecText` + `argText` (`S:shared/BanditsNPCBear.lua:566-604`), Zeichen aus `UI_BN_Bear_Num_Dec` ("," DE/FR/ES/PTBR/RU, "." EN/KO/CN); nur Rechnen, gelesen ueber das vorhandene `B.T`; schwebende Zahlen `S:client/BanditsNPCBearFx.lua:129-137`. Keine Rekursion (`DEC = "."` vor dem Lesen, `argText(nil)` ruft nichts); `B.T` laeuft nur im Client (grep `server/`: 0) -> Sprache des jeweiligen Spielers. Jede `%.1f`/`%.2f`-Stelle im Client geht als Argument durch `U.T` (selbst nachverfolgt: `U.Kg`, `U.DayPctText`, `fmt100`/`atk`, `trustRow`, `NeedDay`, Hud) | `ober_fix1_de` 17/0 (Test-Mod 5/12) | **zu** |
| **R5** | `counts`: kein Koerper und nicht mitfahrend -> `"far"` (`S:server/BanditsNPCBearNeeds.lua:258`); einziger Verbraucher `B.NeedsSlow` (`:510-519`) legt dafuer eine Sitzung an -- selbst geprueft, dass keine `B._s[id]`-Stelle "Sitzung da" als "geladen" liest (`Server.lua:916/954/1104/1173`, `Registry.lua:493/640`, `Look.lua:161`, `Ride.lua:400`, `Heal.lua:212`, `Grow.lua:970`: alle fragen `s.obj` oder setzen nur Felder) | `ober_fix1` FIX1 R5 | **zu** |
| **R6** | Hunger-/Durst-Tooltip in acht Sprachen + `U.EN` "At 100% it loses health down to 1%"; Code: Leben sinkt nur ab 100 (`S:server/BanditsNPCBearNeeds.lua:570-571`) | `fix1/gegen/zeichen_pruefen.txt`: je Sprache 587 Schluessel, genau 3 anders (Num_Dec, HungerTip, ThirstTip), Platzhalter wie EN, jedes Zeichen kommt in Vanillas Texten derselben Sprache vor | **zu** |
| **G-R3** | `enterAct` merkt `f.actD` (`S:server/BanditsNPCBearFight.lua:913`); erster Lauf-Takt danach: Ziel >= fightStuckGain weiter weg -> Uhr neu (`:1205-1209`), sonst wie bisher (C1) | `G:sim_gegen_*`: nur G2a anders (28 Zeilen): statt "skip 7000: stuck at d 6.2" nach 5,3 s laeuft er nach bis "out-of-leash" (22,5 Kacheln, Leine 25); `sim_kampf`/`sim_nach` 0 Zeilen anders; `kampf_nach` 41/0 (N1d gruen). Die bedingte statt der woertlichen Form ist richtig begruendet (woertlich oeffnet C1 wieder, PRUEF.md 1) | **zu** |

Engine-Aufrufe neu: keine neue Methode. `getTimestampMs()` = `V:server/Foraging/forageServer.lua:456`, `player:getModData()` = `V:server/XpSystem/XpUpdate.lua:333`
(beide selbst gelesen, gleiche Form). Kein `pcall` dazu. Neue Namen `BanditsNPCBearInvId`, `UI_BN_Bear_Num_Dec`, `DecText` in NPC Crew `42/media/lua`, Vanilla und
Bandits gegrept: frei (der einzige Treffer `weightDecTexture` in Vanilla ist kein Name von uns).

## 2. Etwas kaputt gemacht? (Diff gegen `C:/Users/Kevin/Zomboid/mods/NCBearTest`)

- `diff -rq`: 15 Dateien anders, nur in der Test-Mod `.git`/`.gitattributes`, sonst nichts. Jede Code-Zeile oben einem Punkt zugeordnet; Kommentare
  passen zum Code (Ausnahme S1 unten). Zeilenenden/BOM/Zeichensatz je Datei gleich wie in der Test-Mod (LF, ohne BOM, Lua nur ASCII).
- `B.InvCommit` ruft `K.healFirst(rec, owner, true)` ohne `linkFirst` (`:294`) -- richtig: nach der Aenderung waere die Marke falsch; jeder Aenderungsweg
  verknuepft vorher (Put/Take ueber `K.check`, `InvTakeUnits`, `InvAddItem`, `InvDrinkStep`, `InvDrop` ueber `healFirst` -- selbst nachgezaehlt).
- R3 nimmt mit Absicht Nachbesserung K1 C2 zurueck (Kevins Wort); R2 aendert mit Absicht die Erwartung NO1. Beides in BAU/PRUEF genannt.

## 3. Eigene R1-Stichprobe (`attrappe/fix1_gegen/gegen.lua`, Aufruf `lua5.1.exe gegen.lua [lua-ordner] [name] [V1:saat]`)

Idee: nicht dieselben festen Faelle wie Bauer und Pruefer, sondern **Zufalls-Geschichten** (feste Saaten, eigener Zufall): je Geschichte ein Baer --
V1 leer aus frueherer Sitzung, V2 erst in dieser Sitzung gezaehmt, V3 wie V2 mit Spieler-Datei von VOR fix1 (ohne Stempel) --, dann 14 zufaellige
Ereignisse: Geben (Naegel / Patronen / Hammer, k 1..6), Nehmen (zufaelliger Satz, zufaelliges k), Spieler-Speichern, volles Speichern (Register, dann
Spieler; ein Absturz DAZWISCHEN ist ein eigener Zeitpunkt). Absturz nach jedem Ereignis mit dem letzten Register, dem letzten Spieler-Stand und den
Kacheln von jetzt; aus jeder vierten heilen Lage geht es weiter (Ebene 2: auf der Platte liegen noch die geladenen Dateien) und stuerzt wieder ab.
Zaehl-Invariante je Gegenstand und Feld ueber Spieler + Boden + Baer.

| | fix1 | Test-Mod |
|---|---|---|
| Ebene 1 (309 gleiche Lagen) | **309 ok** | 297 ok, 12 doppelt (alle "Absturz zwischen Register und Spieler") |
| Ebene 2 | 718 ok, **2 doppelt (G5)** | 651 ok, 6 doppelt (wieder der R1-Fall) |
| Lagen schlechter als die Test-Mod | **0** | -- |
| Rest-Klasse "Datei ohne Stempel" | 5 / 5 ok (Zufall; der Rest bleibt laut BAU 5.1 / PRUEF 5.1 doppelt) | -- |

Ausgaben `G:gegen_fix1.txt`, `G:gegen_testmod.txt`, Spur des G5-Falls `G:spur_V1_7777777.txt`.

## 4. Restbefunde (neu, kein Blocker)

- **G5 (Bestand F4, rote Linie, zwei Abstuerze noetig):** "Kopie gewinnt" setzt die Fassung auf die der Kopie zurueck
  (`S:server/BanditsNPCBearInv.lua:377` `r = cr`, unveraendert seit F4). Ist die Kopie aelter als das Register (Absturz zwischen vollem Speichern und
  Spieler-Speichern -- genau das R1-Fenster), liegt auf der Platte weiter das Register mit der HOEHEREN Fassung. Nach so vielen Aenderungen wie
  Unterschied hat die neue Kopie dieselbe Zahl wie das alte Register; ein zweiter Absturz vor dem naechsten vollen Speichern haelt dann beide fuer gleich
  und das alte Register gilt. Attrappe G5 (Baer mit 3 Naegeln, Hammer geben, Absturz, 1 Nagel geben, Spieler speichert, Absturz): **Hammer doppelt,
  1 Nagel weg** -- in der Test-Mod genauso (`G:gegen_testmod.txt` G5). fix1 macht es nicht haeufiger (beim leeren Baeren war dort schon der erste Absturz
  doppelt), aber der leere Baer laeuft jetzt auch ueber diesen Weg (die 2 Ebene-2-Lagen). **Vorschlag naechster Lauf (eine Zeile):** `r = math.max(cr, inv.r) + 1`
  (neue Fassung ueber beiden, wie fix1 es im neuen Zweig `:337` schon macht). An einer Kopie gemessen (`attrappe/fix1_gegen/variante_r_neu/`, Staging nicht
  angefasst): eigene Geschichten 1024 / 1024, G5 ok, `pruef.lua` 33/0, `bau.lua` 105/0.
- **G4 (nur bei kaputtem Register):** vergibt `B.InitRegistry` einem Eintrag eine neue Kennzahl u (`S:server/BanditsNPCBearRegistry.lua:163-167`, nur bei
  unbrauchbarem u), findet der Abgleich die Kopie nicht mehr; bei leer verknuepftem Baeren mit Inhalt und gleichem Stempel greift dann "Datei aelter"
  und **leert den Baeren** (Attrappe G4: 5 Naegel weg; Test-Mod: Register gilt, 5 bleiben). Normal kommt das nie vor (u wird nur bei Unsinn neu).
  Vorschlag: beim Neuvergeben von u auch `rec.inv.e0`/`e0c` loeschen.
- **S1 (Schoenheit):** alter Kommentar `S:client/ISUI/BanditsNPCBearHud.lua:552` sagt noch "+0,5 -> +1"; die fix1-Zeile darunter stimmt.
- **S2 (Schoenheit):** `B.DecText` aendert jede reine Dezimalzahl in Text-Argumenten -- auch einen Baeren-Namen wie "1.5" (erlaubt laut
  `S:shared/BanditsNPCBearRules.lua:515-540`) zeigt das Deutsche als "1,5".

Offene Fragen des Bauers (BAU.md 5) bleiben fuer Kevin: R1-Rest ohne Stempel / Stempel in jeder Spieler-Datei, G-R3 (er verfolgt einen Fliehenden bis zur
Leine), R5 gleicher Satz fuer "nicht geladen", R4 Komma auch in den Schadenszahlen.

## 5. Pruefungen (alles selbst gelaufen)

| Pruefung | Ergebnis |
|---|---|
| vier Lua-Pruefer auf den 7 Lua-Dateien (`fix1/gegen/pruefer4.txt`) | 28 x rc 0: luacheck 0 failed, scopecheck 0 violations, localcount hoechstens 73 aktiv / 90 insgesamt (< 180), luacheck_pz 0 Treffer |
| langcheck 8 Sprachen (`fix1/gegen/langcheck_acht_staging.txt` / `_testmod.txt`) | 0 Fehler; 3 Hinweise wie die Test-Mod (nur CN-Blase U+65F6 82 statt 80 -- der neue Satz) |
| eigene Zeichen-/Platzhalter-Pruefung (`fix1/gegen/zeichen_pruefen.py`) | 8 Sprachen je 587 Schluessel, 3 geaendert, 0 fremde Zeichen, Platzhalter wie EN |
| Zeilenenden / BOM / ASCII (15 Dateien) | je Datei gleich wie in der Test-Mod |
| alle Attrappen (`attrappe/fix1_gegen/alle_gegen.sh`, Vergleich `G:vergleich.txt`) | 92 Ausgaben gleich wie gegen die Test-Mod; anders nur: `k1_nach` N3 (R3), `k1_ober_nach` NO1 (R2), `k1_pruef` P6, `k1_gegen` G1b/G1W(a) jetzt true, `f4_pruef` P9 Kopie bei p1 true, `f3_pruef` nur Pfad, `pruef_f2` nur Lua-Zeit 0/1 ms, `sim_gegen` G2a (G-R3); Kopien und eigene: `k1_nach_fix1` 40/0, `ober_fix1` 200/0 + 202/0, `ober_fix1_de` 17/0, `bau` 105/0, `pruef` 33/0, kampf_baer 118/0, echt_foe 12/0, kampf_zomb 73/0, kampf_pruef 8 + 1 Befund (Bestand C1), kampf_nach 41/0, nach_zomb 10/0, umgestellte F3/F4 261/0 + 251/0 + 172/0 + 172/0, alte Oberflaechen vorher/nachher gleich (`attrappe/fix1_gegen/ober_alte_vergleich.txt` = der des Pruefers) |
| Uebernahme Trockenlauf / `--probe` mit `--staging mod_fix1` (`fix1/gegen/ue_trocken.txt`, `ue_probe.txt`) | OK, 0 Fehler, 2 Warnungen (Bestand); Probe: luacheck_pz 0 + 17 erlaubt, Bench-Dateien "wird nie kopiert" |
| Staging-Liste `fix1/staging_dateien_fix1.txt` gegen die Platte (MD5 + Bytes + Status selbst neu gerechnet) | 185 = 185, 0 Abweichungen: 15 ueberschreibt, 0 neu, 137 gleich, 33 Modell-Dateien byte-gleich (NICHT KOPIEREN), nichts nur in der Test-Mod |
| `baer/NAEHTE.md` | genau Zeile 47 ergaenzt (Stempel-Schluessel, `reg.invSt`, `e0`/`e0c`), LF, ohne BOM |

## 6. Fuer den Einbau

Liste `fix1/staging_dateien_fix1.txt` (direkt vorher neu erzeugen), mod.info-Text `fix1/mod_info_vorschlag_fix1.txt` (ASCII, LF), Testanleitung
`fix1/anleitung.md`. Danach muss Kevin das Spiel **neu starten**. G5 und G4 gehoeren in den naechsten Lauf (je eine Zeile, Vorschlag oben).

Statisch geprueft, nicht gespielt.
