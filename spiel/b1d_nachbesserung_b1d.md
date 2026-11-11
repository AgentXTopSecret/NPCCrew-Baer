# Lauf baer-b1d: NACHBESSERUNG (11.11.2026 Nachtschicht)

**Statisch geprueft, nicht gespielt.** Grundlage: `pruef_b1d_a.md` (A1-A8) und `pruef_b1d_b.md` (B1-B8). Jeden Befund selbst am Code
nachgeprueft (Code gelesen, Vanilla-Stellen und Jar-Auszuege `dec/AnimalData.java`, `dec/IsoAnimal.java` nachgelesen, Attrappen gegen den
Stand VOR und NACH der Nachbesserung gefahren). Geschrieben nur: Staging `mod/` (6 Lua-Dateien), Attrappen (`b1d_kern/run.lua` +
`ergebnis.txt`, `b1d_ober/run.lua`, `gesamt/run.lua` eine Zeile, `gesamt/xref_b1d.txt`, neu `pruef_b1d/ergebnis_nach.txt`),
`baer/NAEHTE.md`, `PLAN_B1D.md` (F5, F18, Abschnitt 12), `schnittstelle_aenderungen.md` (Abschnitt "B1d NACHBESSERUNG"),
`staging_dateien.txt`, die Probe unter `probe_b1d/` und die Ausgaben `trockenlauf_b1d_nach*.txt`, `probe_b1d_nach_ausgabe.txt`. Nichts in
die Test-Mod, nach NPC Crew, Vanilla oder Bandits. Kein git, kein Spielstart, kein Download.
Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`, `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`.

## 0. Ergebnis je Befund

| ID | Schwere | Urteil | Was getan |
|---|---|---|---|
| A1 | minor | **bestaetigt** (`ENT:279` "Kampf/Zombie-Angriffe/Heilen erst nach Kevins B1c-Test"; `S:server/BanditsNPCBearGrow.lua` B.GrowSlow heilt 1 %/h, B.BodyHp nimmt die Engine-Heilung zurueck) | Code nicht geaendert (der Laufauftrag Punkt 5 verlangt es); **Frage 1 an Kevin** mit dem Hinweis "BearHealAwake = 0 heisst GAR keine Heilung" |
| A2 | minor | **bestaetigt** (grep `getHealth()` + animal ueber ganz `V:` = 1 Treffer, `V:client/ISUI/Animal/ISAnimalUI.lua:15`) | so gelassen (Kevin: "A3 entscheidet der MP-Test", `ENT:285`); mit B2 reisst ein Fehler dort nur noch B1d mit |
| A3 | minor | **bestaetigt** (Vanilla setzt `setHealth` am Tier nur mit 0: `ISAnimalContextMenu.lua:545`, `ClientCommands.lua:932/950`, `ISKillAnimal.lua:58`, `ISVehicleAnimalUI.lua:204`, `ISKillAnimalInInventory.lua:70`) | Kommentar `S:shared/BanditsNPCBearStats.lua` B.ApplySize ergaenzt (Kevins Anleitung `baer/spiel/anleitung_lebend.md:6`, Antwort 1,35 auf "nach dem Test", `begleiter/PLAN.md:297`; gespielt: sehr wahrscheinlich, nicht belegt); **Frage 2** |
| A4 | minor | **bestaetigt** (`ENT:45`; B.BodyHp uebernimmt jeden Verlust) | kein Code (Schutz gehoert zur Gegenwehr B5a); F5 in `PLAN_B1D.md` praezisiert; **Frage 3** |
| A5 | minor | **bestaetigt** (Definitionen `B.GrowSetG`/`B.GrowSetHp`/`B.SkillSet` im kopierten Grow.lua, kein Aufrufer) | **nicht verlegt**: vier Attrappen (b1d_kern, b1d_ober, pruef_b1d, xref_b1d) rufen sie heute -- das ist kein kleiner, sicherer Eingriff in einer Nachbesserung. `NAEHTE.md` (Absatz "B1d, vom Skript erzwungen") nennt es ehrlich; **Frage 4** (Empfehlung des Pruefers: im naechsten Lauf verlegen) |
| A6 | minor | **bestaetigt** (`V:client/OptionScreens/MainOptions.lua:2910-2911` baut die Auswahl ohne Tooltip, die Tickbox `:2810-2813` mit) | kein Code, keine Texte; **Frage 5** |
| A7 | minor | **bestaetigt** (nur Definition `V:client/PZAPI/ModOptions.lua:121-156`) | so gelassen; **Frage 6** (wie B1c A3) |
| A8 | minor | **bestaetigt** (alle fuenf) | (1) `NAEHTE.md` `BanditsNPC.Opt` `:6101` -> `:6105` (zweimal), Kopfzeile; Trockenlauf/Probe neu (NC-Kommentar jetzt `:1360`). (2) Merker: Sandbox-Tooltips "size 1.35" / "until bears can fight/sleep" mit F11, B5a und dem Schlaf-Lauf anpassen -- jetzt nicht geaendert (Kevins Wort offen). (3) Regex-Grenze der Skript-Regeln bleibt, ehrlich hier. (4) Kommentare "Probebefehl(e) der Test-Mod" bleiben mit A5. (5) `attrappe/pruef_b1b/run.lua` (alte Fassung) nur Ordnung, massgeblich `run_nach.lua` |
| B1 | minor | **bestaetigt** (vorher P2b: Spiegel `tamedAt = -1000000` -> `g 1.0`) | `B.Restore` klemmt `born` und `tamedAt` auf [0, jetzt], `B.TakeNewerMark` `tamedAt` ebenso (`S:server/BanditsNPCBearHeal.lua`); Kommentar Grow.lua `B.GrowFromMark` ehrlich; F18 ergaenzt. Jetzt P2b: `g 0.5167` (Zeit seit Weltbeginn + 0,10), kein Befund |
| B2 | minor | **bestaetigt** (Server.lua: GrowSlow mitten in der Langsam-Schleife, GrowLive mitten in `liveRec`, je ein pcall um den ganzen Takt) | `B.GrowSlow` in eigener Schleife nach `slowRec`/`forestRolls`/`baitNights`, vor `B.FlushViews`; `B.GrowLive` als letzter Schritt 7 von `brainTickBody` (nur derselbe Eintrag mit demselben Objekt, Ort aus Schritt 4); `B.GrowLive` legt erstmals bekanntes Leben mit `B.Touch(rec)` in die Sicht |
| B3 | minor | **bestaetigt** (vorher P1b: Treffer 0,004 verschwand) | Schaden = jeder Verlust unter `hpB - hpLossEps` (0,0001, neu in `B.CFG`); `hpEps` nur fuer Anstieg und Setzen. P1c (Treffer + Engine-Heilung im selben Fenster) bleibt -> F5/B5a, im Code als Grenze vermerkt |
| B4 | minor | **bestaetigt** (vorher P3b/P3b': 0 XP) | Sprung erst ueber `conStepMax` 8 UND ueber `conStepMul` (4, neu in `B.CFG`) x `runSpeed` x Taktdauer. Erholung in Echtzeit (auch Pause) bleibt -- nur Anzeige, im Kommentar genannt |
| B5 | minor | **bestaetigt** (vorher P2d: `InitRegistry` wirft an `GrowDays`) | lokal `statsOk()` in Grow.lua; alle zwoelf oeffentlichen B1d-Wege kehren ohne Stats.lua wirkungslos zurueck |
| B6 | minor | **bestaetigt** (`S:client/ISUI/BanditsNPCBearHud.lua` prerender kehrte bei geteiltem Bildschirm vor dem Listenbau um) | **teils gebaut:** bei geteiltem Bildschirm baut der MP-Client die Liste (und damit die Probe) weiter, gezeichnet wird nichts; SP unveraendert. Nicht gebaut (ehrlich, Hud-Kopf + PLAN 12): Junge ausserhalb der Sicht (fremde ab 60 Kacheln) und ausgeblendete Oberflaeche (ob prerender dann laeuft: ungeprueft) |
| B7 | minor | **bestaetigt** (NUR JAR `dec/AnimalData.java:1544-1546`; `V:shared/Definitions/animal/ButcheringUtil.lua:42-43`) | **nicht geaendert:** Tod/Zerlegen ist B5a; kein Rueckschritt gegen B1c (dort war `originalSize` immer die Vorgabe 1,0). Merker fuer B5a: zweites `d:setSizeForced(sz)` in `B.ApplySize` |
| B8 | minor | **bestaetigt** (`B.GrowDay = floor(g x D)`) | nicht geaendert (gewollte Folge von "g als Anteil"); **Frage 8** (F12) |

**Kein Befund abgelehnt.** Neue Engine-Aufrufe: **keiner** (`isClient()` an einer zweiten Stelle im Hud, Beleg wie vorhanden
`V:client/ISUI/ISWorldObjectContextMenu.lua:1435`; `B.Touch` ist eigener Code). Kein neuer `pcall`. Kein neuer Text, alle 21 JSON byte-gleich.
Kein Befehl, kein Menue, keine Datei NCBear* geaendert.

## 1. Einzelheiten

### 1.1 B2 -- B1d am Ende der Takte
- Langsam-Takt (`S:server/BanditsNPCBearServer.lua` slowTickBody): Reihenfolge jetzt slowRec je Eintrag -> forestRolls -> baitNights ->
  **GrowSlow je Eintrag** -> FlushViews. Wirft GrowSlow, fehlt nur das FlushViews dieses Takts; `B._dirty` bleibt stehen und geht mit dem
  naechsten Hirn-Takt hinaus (FlushViews leert erst nach dem Senden).
- Hirn-Takt (brainTickBody): neuer Schritt 7 nach dem Waisen-Suchlauf. Bedingung je Eintrag aus `loaded`: `reg.cubs[id] == rec`,
  `st == "tame"`, `ride == nil`, `B._s[id].obj == e.a` (nicht geschlossen, nicht eingestiegen, nicht an einen neueren Koerper gebunden);
  Ort `e.x`, `e.y` aus Schritt 4 (gleicher Takt, keine zusaetzliche Java-Abfrage).
- Folge (gewollt): was GrowLive in die Sicht legt, kommt einen Hirn-Takt spaeter (<= 1,5 s). Damit das erstmals bekannte Leben nach einer
  Spiegel-Heilung ueberhaupt hinausgeht, ruft GrowLive dann `B.Touch(rec)` (vorher lief es vor dem FlushViews desselben Takts).
  `gesamt/run.lua` 19f wartet deshalb einen Takt mehr auf "Sicht: Leben 60 %" (Ausgabe sonst byte-gleich).
- "Hoechstens eine Sendung je Spieler und Takt" (FlushViews) bleibt: kein zweites FlushViews.

### 1.2 B3 -- jeder Verlust zaehlt
`h < hpB - hpLossEps` ist Schaden (vorher `hpB - hpEps`). Ein Rest der Gleitkomma-Umwandlung (Leben ist in Java ein float) liegt weit unter
0,0001. Der Koerper wird weiter erst ab `hpEps` Abstand gesetzt -- die Heilung sammelt sich im Register und der Koerper folgt (Attrappe 20 B3:
Treffer 0,004 -> Register 0,596 + 0,01/6, Koerper bleibt 0,596; nach 1 h Register 0,606, Koerper nachgezogen). Pruefer Bs P1b jetzt "kein Befund".

### 1.3 B4 -- Sprung an die Zeit gebunden
`way > conStepMax and way > conStepMul x runSpeed x dts` -> 0 (dts weiter auf 10 s gedeckelt, also hoechstens 98,8 Kacheln). Zaehlt jetzt:
Ruckler 8,6 Kacheln in 3,5 s, Vorspulen x3 (11,1 in 1,5 s), 60 Kacheln in 10 s. Sprung: 20 Kacheln in 1,5 s, 120 nach 30 s. Grenze: schneller
als etwa x4 vorgespult zaehlt der Weg als Sprung (keine XP, keine Ausdauer) -- nur Kondition/Anzeige.

### 1.4 B1 -- Spiegel-Deckel
`num(mark.tamedAt, 0, now)`, `num(mark.born, 0, now) or now` (Weltstunden `getWorldAgeHours` sind nie negativ). Ehrlich: der Deckel rechnet
weiter mit einem Wert aus dem Spiegel -- ein veraenderter Spiegel mit `tamedAt` 0 bekommt "Zeit seit Weltbeginn / D + 0,10"; in einer Welt
aelter als etwa 90 Spieltage ist das ausgewachsen. Erfahrung bleibt unpruefbar. Nur MP, nur mit veraendertem Client, nur nach einem
Registerverlust; kein Kick, kein Gegenstand. Frage 7.

### 1.5 B5 -- ohne Stats.lua
`statsOk()` liest nur Tabellenfelder (`B.SKILLS`, `B.SKILL_FIELD`, `B.XpCum`, `B.GrowDays`, `B.StatsOf`, `B.HealRate`, `B.ApplySize` -- die
letzte Funktion der Datei; bricht Stats.lua beim Laden ab, fehlt sie). Attrappe 20 B5: `InitRegistry` laeuft, Register da, `g` nil,
Langsam- und Hirn-Takt ohne Fehlerzeile.

### 1.6 B6 -- geteilter Bildschirm
`prerender`: `split = getNumActivePlayers() > 1`; im SP (`not isClient()`) Rueckkehr wie bisher; auf dem MP-Client Listenbau (mit
Groessen-Probe, hoechstens 1 x/s), danach Rueckkehr vor dem Zeichnen. Attrappe b1d_ober: MP-Client geteilt -> 1 Probe, 0 Zeichenaufrufe;
SP geteilt -> 0 / 0; gegen den alten Hud rot.

## 2. Neue Zahlen (alle selbst gelaufen, 11.11.)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (25 Lua des Stagings) | 25 checked, 0 failed |
| `scopecheck.py` | 25 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 48 (`Hud.lua` Dateiebene), dann 39 (`Server.lua:921` brainTickBody, `Hud.lua:420`, Bench `:384`); insgesamt hoechstens 77 (`World.lua:640`, unveraendert), 59 (Hud), 58 (`Server.lua:921`) -- weit unter 180/200 |
| `luacheck_pz.py` | 18 x W113, alle erwartet (3 Aktionsklassen `Menu.lua:86/97/107`, 15 Bench); `--unused` auf den 6 geaenderten Kern-/Hud-Dateien: 3 x W212 `self` (`Hud.lua:649-651`, B1a, harmlos) |
| Dateiform (48 .lua/.json/.txt) | alle LF, kein BOM, LF am Ende, keine Leerzeichen am Zeilenende, Lua/.txt ASCII; JSON Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert: 0 Probleme. `attrappe/kern/dateiform.py` (B1a-Werkzeug fuer KERN-Dateien): nur die alten Treffer "test" in `client/BanditsNPCBearMenu.lua` (unveraendert, OBERFLAECHE) |
| `attrappe/kern/run.lua` | **136 / 0** (byte-gleich `ergebnis.txt`) |
| `attrappe/b1b_kern/run.lua` | **204 / 0** (byte-gleich) |
| `attrappe/b1c_kern/run.lua` | **192 / 0** (byte-gleich) |
| `attrappe/b1d_kern/run.lua` | **163 / 0** (vorher 147; Abschnitt 11 B4 +5, neu Abschnitt 20 mit 11; `ergebnis.txt` neu). Gegen den Stand VOR der Nachbesserung: 148 / 15 (jede neue Pruefung rot) |
| `attrappe/gesamt/run.lua` | **1173 / 0**, byte-gleich `gesamt/ergebnis.txt` (einzige `***`: die gewollten Heilungen 18c/19f) |
| dieselbe gegen die neue Probe (`probe_b1d/NPCCrew/42/media/lua/`) | **1173 / 0**, byte-gleich `gesamt/ergebnis_probe.txt` |
| `attrappe/ober` / `b1b_ober` / `b1c_ober` (ohne / mit `kern`) | 116/0 + 117/0, 144/0 + 134/0, 193/0 + 180/0 (unveraendert) |
| `attrappe/b1d_ober` (ohne / mit `kern`) | **174/0 + 176/0** (vorher 171 + 173; +3 B6); gegen den alten Hud 1 Fehler |
| `pruef_b/run.lua`, `pruef_b1b/run_nach.lua`, `pruef_b1c/run.lua` | byte-gleich `ergebnis_b1b_nach.txt` / `ergebnis_b1c.txt` / `ergebnis_nach.txt` |
| `pruef_b1d/run.lua` (Pruefer B, unveraendert) | **10 bestanden, 0 Fehler, 3 Befunde** (vorher 8): P1b, P2b, P2d, P3b, P3b' jetzt "kein Befund"; uebrig P1c (Grenze F5/B5a), P2a (Plan 12 bekannt), P2c (B8, Frage 8) -- `pruef_b1d/ergebnis_nach.txt` |
| `texte_pruefen.py` / `_b1b` / `_b1c` / `_b1d --tmp <scratch>` | FEHLER gesamt: 0 / 0 / 0 / 0; `texte_b1d.py` -> 22 Dateien, abweichend vom Staging keine; `--basis` == `texte_b1c.py` |
| `belege.py` / `_b1b` / `_b1c` / `_b1d` | abweichend 0 von 112 / 51 / 89 / 23 |
| `gesamt/xref_b1d.py` | **0 Luecken, 3 Hinweise** (Rueckfallwerte Rules.lua, wie vorher); B.CFG 158 Felder (+ `conStepMul`, `hpLossEps`), 157 gelesen (`orphanMs` wie vorher); Tier-Stellen `Stats.lua:345/348`, `Grow.lua:216/250` -- `xref_b1d.txt` neu |
| `gesamt/gegenprobe_b1d.py` | **26 von 26 erkannt** (byte-gleich `gegenprobe_b1d.txt`) |
| `uebernahme_force/probe_force.py` / `uebernahme_b1c/probe_regeln.py` | 23 Faelle, 0 Fehler / 34 Faelle, 0 Fehler |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (`trockenlauf_b1d_nach_vor_b5a.txt`); 24 Lua, 6646 Codezeilen; Cheat-Funde 0; Tier-Regeln an ihren Orten (setSizeForced `Stats.lua:348`, getData `:345`, setHealth `Grow.lua:250`, getHealth `:216`, probeweg: kein Aufruf) |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler, alle "noch umzubenennen (B5a)", 2 Warnungen (`trockenlauf_b1d_nach.txt`) |
| Probe `--probe _arbeit/baer_zaehmen/probe_b1d --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, 51 Dateien geschrieben; je kopierter Lua luacheck/scopecheck/localcount ok (Server.lua hoechstens 58); luacheck_pz 0 Treffer + 3 erlaubt; UI.json 3812 -> 3945, Sandbox.json 92 -> 151, IG_UI.json neu 3 (`probe_b1d_nach_ausgabe.txt`) |
| `staging_dateien.txt` neu | **51 Dateien: 2 neu, 25 ueberschreibt, 24 gleich** (gegen NCBearTest); durch die Nachbesserung geaendert 6 Lua: `client/ISUI/BanditsNPCBearHud.lua`, `server/BanditsNPCBearGrow.lua`, `...Heal.lua`, `...Server.lua`, `shared/BanditsNPCBear.lua`, `shared/BanditsNPCBearStats.lua` (nur Kommentar) |

## 3. Fragen fuer Kevin (je mit Empfehlung; Kevin schlaeft -- nichts davon haelt den Einbau auf)
1. **(A1) Selbstheilung schon an:** das zahme Junge heilt sich jetzt 1 % je Spielstunde, die schnellere Heilung des Spiels (~2 %/h) wird
   zurueckgenommen -- obwohl du "Heilen erst nach meinem B1c-Test" gesagt hast. So lassen? Achtung: Sandbox "Heilung wach" = 0 heisst GAR
   keine Heilung (auch die des Spiels bleibt weg). Empfehlung: so lassen und zusammen mit dem B1c-Test ansehen.
2. **(A3) Regel-Frage:** `setHealth` mit Werten zwischen 0 und 1 und `setSizeForced` an einem LEBENDEN Tier -- Vanilla benutzt beide nur am
   Haken-/toten Tier bzw. mit 0. Gelten sie als belegt? Empfehlung: ja (gleicher Typ; `setSizeForced` am lebenden Baeren stand in deiner
   Anleitung und fuehrte zu deinen 1,35).
3. **(A4) Spieler und Autos** koennen dein zahmes Junges verletzen, und der Schaden bleibt jetzt (auch nach Mitfahren, Call to me, Laden).
   Laut Plan-Vorgabe sollen Spieler und Autos keinen Schaden machen. Mit B5a (Gegenwehr) abschalten? Empfehlung: ja, mit B5a.
4. **(A5) Testwege im Kern:** die drei Vorspul-/Setz-Wege der Testhilfe liegen als Funktionen ohne Aufrufer im Kern und gingen so mit nach
   NPC Crew (kein Befehl, kein Menue). In eine Testhilfe-Datei verlegen? Empfehlung: ja, im naechsten Lauf.
5. **(A6)** Die Erklaerungen der Auswahlen Leben/Ausdauer (Optionen -> Mods) zeigt das Spiel nicht an. Reicht dir der Name? Empfehlung:
   ja; sonst schreibe ich die Kurzinfo in den Namen.
6. **(A7, wie B1c A3) Regel-Frage:** `addComboBox`/`addItem` der Optionen-Seite haben in Vanilla und Bandits keinen Aufrufer (nur die
   gelesene Definition; NPC Crew benutzt sie gespielt). Als belegt zaehlen? Empfehlung: ja.
7. **(B1, F18) Mehrspieler nach Server-Absturz:** ein Junges holt Wachstum und Erfahrung aus der Markierung am Tier zurueck; das Wachstum
   ist gedeckelt auf die Zeit seit dem Zaehmen (+10 Tage Futter-Bonus), die Zaehm-Zeit ist jetzt auf "nicht vor Weltbeginn, nicht nach
   jetzt" geklemmt. Ein veraenderter Client kann in einer alten Welt trotzdem "ausgewachsen" vortaeuschen. So lassen oder nach einem Absturz
   hart neu anfangen? Empfehlung: so lassen (wie B1c F1).
8. **(B8, F12)** Stellst du "Tage bis ausgewachsen" spaeter um, bleibt die Groesse, aber die Zahl "Tag" im Schild wird neu gezaehlt (z. B.
   30 -> 15). Ok? Empfehlung: ja; ein Satz dazu im Sandbox-Tooltip mit der naechsten Textrunde.
9. **(B4, F14)** Vorspulen schneller als etwa x4: Rennen zaehlt dann nicht fuer die Kondition (nur Anzeige/Uebung). Ok? Empfehlung: ja.

## 4. Fuer den Gegenpruefer
- Neue Engine-Aufrufe: keine. `isClient()` jetzt auch in `Hud:prerender` (nur bei geteiltem Bildschirm), Beleg im Kommentar. `B.Touch(rec)`
  in `B.GrowLive` ist eigener Code (Registry.lua).
- Geaenderte Erwartungen: `b1d_kern` 11 (Sprung jetzt 20 statt 12 Kacheln, B4), `gesamt` 19f (ein Takt mehr, B2). Sonst nur neue Faelle.
  Gegenprobe: `b1d_kern` gegen den Stand vor der Nachbesserung 15 rot, `b1d_ober` 1 rot.
- Bewusst nicht gebaut: A5 (Verlegen, Kevins Wort), A6 (Texte), A8.2 (Tooltips mit F11/B5a/Schlaf), B6 Rest (Sicht-Reichweite,
  ausgeblendete Oberflaeche), B7 (B5a), B8 (Kevins Wort F12). P1c (Treffer und Engine-Heilung im selben Fenster) bleibt bis F5/B5a.
- Die Regel "hoechstens eine Sendung je Spieler und Takt" bleibt: B1d-Aenderungen im Hirn-Takt gehen mit dem naechsten Takt hinaus.

## 5. Offen / ungeprueft (zusaetzlich zu bau_b1d_zusammenbau.md 7 und pruef_b1d_*.md 5)
- `animal:getHealth()` am MP-Server (A2): weiter offen; ein Fehler steht als "[TC-BEAR] *** slow tick: ..." / "brain tick: ..." im
  Server-Log (PLAN_B1D.md 7.4 MP 7) und stoppt jetzt nur B1d.
- Ob `prerender` bei ausgeblendeter Oberflaeche laeuft (B6-Rest); `originalSize` beim echten Tod (B7, NUR JAR).
- Laufzeit aller B1d-Wege: ungespielt.

Statisch geprueft, nicht gespielt. Nach einem Einbau muss Kevin das Spiel neu starten (Lua und die Definition laden nur beim Start).
