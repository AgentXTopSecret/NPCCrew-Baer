# Lauf baer-b1b: NACHBESSERUNG (11.11.2026)

**Statisch geprueft, nicht gespielt.** Grundlage: `pruef_b1b_a.md` (A1-A8) und `pruef_b1b_b.md` (B1-B8). Jeden Befund selbst am Code
nachgeprueft. Geschrieben nur im Staging `mod/`, in den Attrappen, in `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md` (ein Absatz),
`PLAN_B1B.md` (Kevins Test 8.4 + neuer Abschnitt 12), Anmerkungen in `bau_b1b_kern.md` / `bau_b1b_oberflaeche.md` /
`bau_b1b_zusammenbau.md`, `schnittstelle_aenderungen.md`, `staging_dateien.txt`, die Probe unter `probe_b1b/` und javap-Auszuege
`javap/b1b_nach_*.txt`. Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits (das Spiel lief waehrend der Arbeit:
`ProjectZomboid64.exe`). Kein git, kein Spielstart, kein Download. Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`.

## 0. Ergebnis je Befund

| ID | Schwere | Urteil | Was getan |
|---|---|---|---|
| A1 | major | bestaetigt (grep `string.byte(`/`:byte(` in V und Bandits 42.22/common: 0) | `B.CleanName` ohne `string.byte` neu: nur `string.len`, `string.sub`, Textvergleiche (`S:shared/BanditsNPCBearRules.lua:337-411`) |
| A2 | minor | bestaetigt | mit A1: C1, Format-, Richtungs-, Null-Breite-Zeichen, Hangul-Fueller abgelehnt; U+00A0/U+3000 u. a. am Rand weg, "nur Leerraum" = leer |
| A3 | minor | bestaetigt (`media/fonts/<L>/fonts.txt`: NewSmall = Small in allen 8 Sprachordnern) | Code bleibt (schadet nicht), Kommentar `S:client/ISUI/BanditsNPCBearHud.lua:410-415` und die zwei Berichte richtiggestellt; **Frage an Kevin** |
| A4 | minor | bestaetigt (`V:server/Seasons/season.lua:120-145` ist `--[[ ]]`) | Beleg getauscht: `V:server/XpSystem/XpUpdate.lua:298` (`getOnlinePlayers():get(i)` bzw. `getSpecificPlayer(i)`, dann `isDead()`) in `S:server/BanditsNPCBearWorld.lua:29`; `season.lua:139` in `bau_b1b_kern.md:92` gestrichen |
| A5 | minor | bestaetigt (Regex-Probe nachgestellt) | Regel `force` ist jetzt `scan_force_hits` (`baer/tools/baer_uebernahme.py:190`, Aufruf `:1217`): zerlegt jede Erwaehnung von `ScanAnimals` dateiweit mit `call_args`; Gegenprobe 23/0 |
| A6 | minor | bestaetigt (Kommentar `:576` widersprach `:899-900`) | beide Kommentare ehrlich (A3-Ausnahme genannt, Fehler laut ueber `B.ErrEvery`); Kevins MP-Test 8.4 Schritt 7 erweitert. Lauf NICHT eingeschraenkt (Begruendung 1.6) |
| A7 | minor | bestaetigt (Abweichung vom Auftrag 1) | Regel 10: Besitzer fehlt -> **halten, bleibt "follow"**; `B.FollowLost` nur bei anwesendem Besitzer. Ueberlebt jetzt MP-Abmelden und Neustart; Plan 8.4 MP 5/6 angepasst; **Frage an Kevin** |
| A8 | minor | bestaetigt | Kevins Wort vom 11.11. eingebaut: `BearTameFeedPoints` 4, `BearTamePetPoints` 3 in `B.OPTS` (`S:shared/BanditsNPCBear.lua:92-93`) und `sandbox-options.txt:84/:92`; Tooltips ohne Zahlen (geprueft); Attrappen: neue Vorgaben in Fall 1h, alte Rechen-Faelle auf 14/8 gepinnt |
| B1 | blocker | bestaetigt (Attrappe nachgefahren, Ursache in der Rechnung) | "steckt fest" misst jetzt den Weg des JUNGEN auf den Besitzer zu (`gainToward`, `f.bx`/`f.by`, `S:shared/BanditsNPCBearRules.lua:439-486`) |
| B2 | minor | bestaetigt | Vorhalt: Halten (Regel 14) und Ziel (16) rechnen mit dem Ort des Besitzers im naechsten Takt (Weg seit dem letzten Takt aus `B._pp`, Deckel `followLead` 1,5) |
| B3 | minor | bestaetigt | `B.FollowLost` nur fuer ein Junges, das in dieser Sitzung schon ein Objekt hatte (`B._s[id].obj`, `S:server/BanditsNPCBearFollow.lua:171`) |
| B4 | minor | bestaetigt (= A2) | mit A1/A2 |
| B5 | minor | bestaetigt | Drossel je "Spieler|Befehl|Ausgang", gezaehlt erst NACH den Pruefungen (`allow`/`refuse`, `S:server/BanditsNPCBearFollow.lua:52-81`); Deckel 128 |
| B6 | minor | bestaetigt | `holdWanted`: eigenes zahmes Junges nur, wenn es nicht folgt (`S:client/BanditsNPCBearMenu.lua:361`) |
| B7 | minor | bestaetigt (Jar `dec/BaseAnimalBehavior.java:186` `Rand.Next(16) - 8` um das Tier selbst) | `stayR` 12 (`S:shared/BanditsNPCBear.lua:73`); **Frage an Kevin** (Gefuehl) |
| B8 | minor | bestaetigt (ungeprueft, ob PZ das Konto zulaesst) | Server: `B.PlayerKey` gibt im MP fuer das Konto `__sp` nil (`S:shared/BanditsNPCBear.lua:287`); Client: `__sp` nur im SP "eigen", im MP "?" (`Hud.lua:153`, `:166`, `Client.lua:213`) |

**Kein Befund abgelehnt.** Kein neuer Engine-Aufruf. Kein neuer `pcall`. Kein neuer Text (Texte unveraendert, 7 Sprachen).

## 1. Einzelheiten

### 1.1 A1/A2/B4 -- `B.CleanName` ohne `string.byte`
- Jedes Zeichen per `string.sub(text, k, k)`. Gedrucktes ASCII (`" "` bis `"~"`) geht den kurzen Weg (nur `<`, `>`, `%` verboten). Alles
  andere: `ch < " "` (C0) oder in `NAME_BADR` -> abgelehnt; in `NAME_SPACE` -> Leerraum. Rand-Leerraum weg, nichts Sichtbares -> nil, danach
  Laenge > `nameMax` -> nil. Eigener Deckel `4 x nameMax`, bevor ein Zeichen angesehen wird.
- Warum das unter Kahlua stimmt (javap 42.22.2, gesichert `javap/b1b_nach_*.txt`):
  - `string.sub` = `StringLib.sub` -> `String.substring` (UTF-16-Zeichen). `string.len` steht nicht in StringLibs Tabelle; dass beide
    dieselben Einheiten zaehlen, setzt Vanilla voraus: `V:shared/luautils.lua:5` `string.sub(String, 1, string.len(Start)) == Start`.
  - `<` / `<=` zwischen Texten: `KahluaThread`, Befehle LT/LE (24/25) -> `String.compareTo`. Vanilla vergleicht Texte so
    (`V:client/DebugUIs/DebugMenu/Entity/ISEntityScriptsPanel.lua:149` `return a.name < b.name`).
  - Grenzen ueber 127 stehen als UTF-8-Bytefolge in der (ASCII-)Datei, z. B. `"\226\128\139"` = U+200B. Kahluas Lader baut String-Literale
    als Bytes und macht daraus `new String(bytes, "UTF-8")` (`org/luaj/kahluafork/compiler/LexState.newstring`, javap `:601-612`), also EIN
    Zeichen. Laese der Lader es anders, fiele nur die Grenze aus, nie ein erlaubtes Zeichen (Kommentar im Code).
  - Kein Vanilla-Beleg fuer Byte-Escapes ueber 127 in Strings (grep 0) -- das ist Lua-Syntax, kein Aufruf; die Wirkung ist Jar-Lesart.
- Abgelehnt jetzt: U+007F, U+0080-009F, U+00AD, U+061C, U+115F-1160, U+180E, U+200B-200F, U+2028-202E, U+2060-206F, U+3164, U+FEFF,
  U+FFA0, U+FFF9-FFFB. Leerraum: U+0020, U+00A0, U+1680, U+2000-200A, U+202F, U+205F, U+3000. Bekannte Grenze: Zeichen ueber U+FFFF
  (Emoji) sind unter Kahlua zwei Ersatzzeichen und gehen durch (zaehlen doppelt), wie vorher.

### 1.2 B1/B2 -- Folgen beim Gehen
- **B1:** Fortschritt = Abstand um >= `followStuckGain` kleiner ODER das Junge hat sich seit `f.bx/f.by` um >= `followStuckGain` auf den
  Besitzer zu bewegt (Projektion auf die Richtung zum Besitzer). Seitliches Hin und Her an einer Wand und eine zue Tuer bleiben "fest".
- **B2:** `env.owner.mx/my` = Weg des Besitzers seit dem letzten Hirn-Takt (`S:server/BanditsNPCBearServer.lua:655-658`, aus `B._pp`).
  `B.FollowDecide` haelt den Ort um hoechstens `followLead` 1,5 Kacheln vor; Regel 14 haelt nur, wenn das Junge am VORGEHALTENEN Ort nah ist
  (geht der Besitzer weiter, rennt es, statt zu halten).
- Preis von B2 (ehrlich): bleibt der Besitzer genau nach einem Takt abrupt stehen, kommt das Junge bis auf `followGap - followLead` = 0,5
  Kacheln heran (nie an ihm vorbei). Die Gesamt-Attrappe (Besitzer springt 10 Kacheln in einem Takt) zeigte das; ihre zwei Erwartungen
  "~2 Kacheln dahinter" sind auf "hoechstens 3, nicht vor ihm" gestellt (`attrappe/gesamt/run.lua` 17b, mit Kommentar).
- Attrappe mit Bewegungsmodell (`attrappe/b1b_kern/run.lua` 11a-e, Tempo laut `forschung_b1b.md:37-38`; joggen 3,5 = ANNAHME):

| Fall | vorher (Pruefer B) | jetzt |
|---|---|---|
| 1a/11a gehen 2,27, Junges 2,47, 120 s | fest nach 15,1 s, Ende 25,4, 19 Laufbefehle | nie fest, Abstand je Takt (ab 20 s) **3,71-4,40**, Ende 3,94, 80 Laufbefehle |
| 1b/11b Junges 2,20 | Ende 35,7 | nie fest, Ende 13,9 (faellt langsam zurueck: Tempo, nicht Regel) |
| 1c/11c 20 s joggen, dann gehen | Ende 24,2 | nie fest, Ende 3,7 |
| 11d Tuer zu (Junges steht), Besitzer in 10 | -- | fest nach 15,1 s, danach ein Versuch je 10 s (10 Laufbefehle in 80 s) |
| 11e seitlich an der Wand | -- | fest nach 15,1 s |

### 1.3 A7/B3 -- Zustand ueber Abmelden, Neustart und Laden
- Regel 10: `{ act = "hold", why = "offline" }`; `B.FollowStep` haelt (Sperre je Takt), `rec.mode` bleibt "follow". Kommt der Besitzer
  zurueck: nah -> haelt, weiter als 4,5 -> rennt, weiter als 40 -> Bleiben mit Richtung (wie bisher).
- `B.FollowLost` wechselt nur noch auf Bleiben, wenn (a) das Junge in dieser Sitzung schon ein Objekt hatte (B3: nach dem Laden ist jedes
  Junge "ohne Objekt", bis der Suchlauf bindet) und (b) der Besitzer da ist (A7: meldet er sich ab, entlaedt seine Gegend mit ihm -- das
  Junge wartet virtuell als "follow"). Der B1a-Weg (Fehlversuche -> "missing" -> Bleiben) gilt unveraendert, wenn die Gegend geladen ist.
- Folge: im MP haelt ein folgendes Junges eines abgemeldeten Besitzers still, falls andere Spieler seine Gegend geladen halten (Frage 2).
- Attrappe: `b1b_kern` 4e, 8g, 11g (erster Takt nach dem Laden ohne Gegend: bleibt follow; Gegenprobe gesehen + Besitzer da -> StayBehind),
  11h (MP: abmelden, Gegend entladen, kein Fehlversuch, einloggen -> folgt; Neustart ohne Besitzer -> follow); `gesamt` 17i.

### 1.4 A5 -- Uebernahme-Regel `force`
`scan_force_hits(code_text)`: Code-Teil der ganzen Datei (Kommentare weg, Strings da). Erlaubt: die Definition und Aufrufe mit hoechstens
einem Argument (mit `:` zaehlt `self` mit). Fund: jedes zweite Argument in jeder Form, auch ueber mehrere Zeilen, und `ScanAnimals` ohne
Klammer (`local scan = B.ScanAnimals`, `B["ScanAnimals"]`, auch ein `if B.ScanAnimals then`-Riegel -- streng gewollt). Gegenprobe
`attrappe/uebernahme_force/probe_force.py`: 23 Faelle, 0 Fehler; kopierte Dateien 0 Funde, Werkbank 2.

### 1.5 B5 -- Drossel
Wirkungen (Zustand, Name, Meldung) je `"<Spieler>|Mode|ok"`, `"...|Mode|no"`, `"...|Rename|ok"`, `"...|Rename|no"` hoechstens je 500 ms;
eine Bitte falscher Form verbraucht nichts. "Follow me" + 100 ms spaeter OK im Namensfenster: beide wirken (11i); fremde Ablehnung nimmt der
eigenen Bitte den Platz nicht (11i, Pruefer B 3i jetzt OK); zwei Ablehnungen in 100 ms -> eine Meldung (Flutschutz bleibt).

### 1.6 A6 -- warum der eigene Waisen-Lauf im MP NICHT eingeschraenkt wurde
Der Fehler bleibt laut (eine Zeile `brain tick: ...` je 60 s), er steht am Ende des Takts (das Folgen laeuft vorher), und gerade weil der
Lauf auch ohne Junges alle 2 min kommt, zeigt Kevins MP-Test A3 (`getObjectListForLua` am Server) in 3 Minuten -- ohne erst ein Junges zu
zaehmen. Beides steht jetzt ehrlich in den Kommentaren (`S:server/BanditsNPCBearServer.lua:576-581`, `:908-914`) und in Plan 8.4 MP 7.

## 2. Neue Zahlen (alle selbst gelaufen, 11.11.)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (17 Lua) | 17 checked, 0 failed |
| `scopecheck.py` | 17 file(s), 0 violation(s) |
| `localcount.py` | hoechstens 39 aktiv (Bench), insgesamt hoechstens 54 (`B.ScanAnimals`) -- unter 180/200 |
| `luacheck_pz.py` | 14 x W113, alle erwartet (3 Aktionsklassen, 11 Bench); `--unused` ohne Bench: nur die 5 bekannten aus B1a |
| Dateiform (42 Dateien) | LF, kein BOM, Zeilenende am Schluss, Lua/.txt ASCII, kein Backslash am Zeilenende: 0 Probleme |
| JSON (21) | Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert: 0 Probleme (Texte unveraendert) |
| `attrappe/kern/run.lua` | **136 bestanden, 0 Fehler** (vorher 133; neu 1h: Vorgaben 4/3, gezaehmt nach 11-13 bzw. 13-15 Spielstunden) |
| `attrappe/b1b_kern/run.lua` | **203 bestanden, 0 Fehler** (vorher 145; +58: Abschnitt 11 mit 55, je eine in 2j, 3b, 5c); `***` nur die 3 erwarteten aus 6b |
| `attrappe/gesamt/run.lua` | **486 bestanden, 0 Fehler** (vorher 483; +1 in 17d, +2 in 17i), keine `***`-Zeile; gegen die Probe (`probe_b1b/NPCCrew/42/media/lua/`) gleich (486/0) |
| `attrappe/ober/run.lua` ohne / mit Kern | 116 / 117 ok, 0 Fehler |
| `attrappe/b1b_ober/run.lua` ohne / mit Kern | 144 / 134 ok, 0 Fehler (neu: B6 folgt -> kein Punkt, bleibt -> Punkt; B8 MP `__sp` -> "?'s cub" / "belongs to ?") |
| `attrappe/pruef_b1b/run_nach.lua` (Pruefer Bs `run.lua` unveraendert, Zeichen-Modell an) | 15 OK, 1 BEFUND = 3b (erwartet noch den alten Plan offline -> stay; A7 absichtlich anders). Ohne Zeichen-Modell zusaetzlich 3d-3f BEFUND: echtes Lua 5.1 zaehlt Bytes, nicht Kahlua-Zeichen |
| `attrappe/pruef_b/run.lua` (B1a) | dieselben 7 OK + bekannter B1a-Punkt 2a; nur die Zahlen in 3a/3b anders (Punkte 4/3 statt 14/8), `pruef_b/ergebnis_b1b_nach.txt` |
| `gesamt/xref_b1b.py` | 0 Luecken, 0 Hinweise |
| `texte_pruefen.py` / `texte_pruefen_b1b.py` | FEHLER gesamt: 0 / 0 |
| `belege.py` / `belege_b1b.py` | abweichend 0 von 112 / 0 von 51 |
| `uebernahme_force/probe_force.py` | 23 Faelle, 0 Fehler |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten, GLB-Clip, NPC-Crew-Kommentar jetzt `shared/BanditsNPC.lua:1358`); Cheat-Funde 0; "Texte aus der Lua: 86 benutzt, fehlen in EN: 0; Ersatztexte 94, wortgleich: ja" (`trockenlauf_b1b_vor_b5a.txt`) |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler, genau die Altlasten (B5a) (`trockenlauf_b1b.txt`) |
| Probe `--probe _arbeit/baer_zaehmen/probe_b1b --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, 42 Dateien geschrieben; je kopierter Datei luacheck/scopecheck/localcount ok; luacheck_pz 0 + 3 erlaubt; UI.json 3810 -> 3904 je Sprache (NPC Crew hat seit dem Zusammenbau 9 Texte mehr), Sandbox.json 92 -> 137, IG_UI.json neu 3 (`probe_b1b_ausgabe.txt`) |
| `staging_dateien.txt` | 42 Dateien: 2 neu, 26 ueberschreibt, 14 gleich; durch die Nachbesserung geaendert: 8 Lua + `sandbox-options.txt` |

Fix 2 (`tHas` in `B.T`) und Fix 3 (`petting = PetAnimalCalf`, Ton in der Streichel-Aktion) sind unveraendert drin; Streicheln unberuehrt.

## 3. Fragen an Kevin (je mit Empfehlung; nichts davon haelt den Einbau auf)
1. **Zeile 2 des Namensschilds** ("following"/"staying") ist gleich gross wie Zeile 1, nur blasser: das Spiel hat keine kleinere Schrift
   (NewSmall = Small in allen Sprachen). Kleiner ginge nur mit `drawTextZoomed` (Vanilla ruft es nirgends auf -> braucht dein Wort).
   Empfehlung: so lassen und im Spiel ansehen.
2. **Abmelden im Mehrspieler:** das folgende Junge wartet jetzt stehend auf dich und folgt nach dem Einloggen (bzw. nach einem
   Server-Neustart) weiter (vorher: "staying"). Halten andere Spieler die Gegend geladen, steht es dort still, bis du kommst. Ok?
   Empfehlung: ja (so verlangt es "Zustand ueberlebt Speichern/Laden ... im MP").
3. **Bleiben-Radius 12 statt 8** (sonst rannte es oft grundlos heim, weil die Engine beim Wandern bis 8 Kacheln wuerfelt). Empfehlung:
   im Test fuehlen (`NCBear_CubSet("stayR", 10)` zum Vergleich).
4. **Abstand beim Folgen:** beim Gehen ~3,7-4,4 Kacheln (Attrappe); stehst du abrupt still, kommt es bis ~0,5 heran. Stellwert
   `NCBear_CubSet("followLead", 1.0)` = etwas weiter weg, `2.0` = etwas naeher. Empfehlung: 1,5 lassen, im Test 8.4 Schritt 2 ansehen.
5. **Zaehm-Dauer** ist jetzt drin (4 / 3 Punkte): bestes Spiel ~12 Spielstunden, normales Futter ~14. Dein laufender Spielstand behaelt
   seine gespeicherten Sandbox-Werte (14 / 8).

## 4. Fuer den Gegenpruefer
- Neue Kahlua-Lesarten (keine Aufrufe, aber Wirkung nur per Jar belegt): `string.sub` in UTF-16-Zeichen, Textvergleich = `compareTo`,
  Byte-Escapes im Literal = UTF-8-Zeichen. Pruefen: `javap/b1b_nach_StringLib.txt` (`sub` :1839-1930), `b1b_nach_KahluaThread.txt`
  (:1490-1530, `compareTo` :1524), `b1b_nach_LexState.txt` (`newstring` :601-612; `read_string` ab :900, Dezimal-Escape bis 255 und
  `save` in den Byte-Puffer um :980-1015).
- Das Zeichen-Modell der Attrappe (`A.kahluaChars`) zaehlt Zeichen ueber U+FFFF als 1 (Kahlua 2) -- fuer die Tests egal.
- Absichtlich geaenderte Erwartungen (nicht "gruen gemacht"): `b1b_kern` 1.10, 2j (Deckel 128), 3b/3d (stayR 12), 4e, 5c (zaehlt jetzt
  `string.sub`), 8g; `gesamt` 17b (B2-Preis), 17d (stayR 12), 17i (A7); `kern`/`gesamt` rechnen B1a mit gepinnten 14/8 (`A.sandboxBase`).
- `pruef_b1b/run.lua` ist unveraendert; `run_nach.lua` schaltet nur das Zeichen-Modell ein.

## 5. Offen / ungeprueft (unveraendert gueltig)
Alles Laufzeitverhalten (wirkliches Tempo von Junges und Spieler, Wege, Tueren, Treppen, Q-Ruf, MP-Ruckeln, Schildhoehe `tagZ` 0,18),
A3 aus B1a (`getObjectListForLua`/`getAnimalID` am Server), `p:getVehicle()` fremder Spieler am Server (Jar-Lesart), ob PZ ein Konto
`__sp` zulaesst, ob die Kacheln im SP beim ersten `OnTick` nach dem Laden schon da sind (jetzt ohne Folge, B3).

Statisch geprueft, nicht gespielt.
