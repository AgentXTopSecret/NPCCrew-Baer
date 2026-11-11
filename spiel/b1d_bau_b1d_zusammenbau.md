# Lauf baer-b1d: ZUSAMMENBAU + UEBERNAHME (B1d Wachsen, taeglich steigende Werte, Faehigkeiten, Heilen-Vorbereitung, Anzeige, Bench)

Stand 11.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (B1a + B1b + B1c
+ B1d KERN + B1d OBERFLAECHE). Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart, kein
Download. **Im Staging wurde nichts geaendert** (keine Luecke ueber die Grenze gefunden). Geschrieben: `attrappe/gesamt/run.lua`
(FILES, `b1cTag()`, Werkbank-Nachladen fuer die Probe, Abschnitt 19), `attrappe/gesamt/xref_b1d.py` (neu) mit `xref_b1d.txt`,
`attrappe/gesamt/gegenprobe_b1d.py` (neu) mit `gegenprobe_b1d.txt`, `ergebnis.txt`, `ergebnis_probe.txt`, `baer/tools/baer_uebernahme.py`,
`baer/NAEHTE.md`, `staging_dateien.txt`, `mod_info_vorschlag.txt`, ein Absatz in `schnittstelle_aenderungen.md`, die Probe unter
`probe_b1d/` und die Ausgaben `trockenlauf_b1d.txt`, `trockenlauf_b1d_vor_b5a.txt`, `probe_b1d_ausgabe.txt`.
Nach dem Einbau muss Kevin das Spiel neu starten (Lua und die Tier-Definition laden nur beim Start).

## 0. Ergebnis

| Pruefung | Ergebnis |
|---|---|
| Grenze KERN <-> OBERFLAECHE (`attrappe/gesamt/xref_b1d.py`, neu) | **0 Luecken**, 3 Hinweise (die bekannten Rueckfallwerte in Rules.lua, B1c Z3) -- `xref_b1d.txt` |
| Gegenprobe xref (12 Verderbnisse einer Staging-Kopie im Temp-Ordner) | **12 von 12 erkannt** |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` (neu Abschnitt 19a-19m) | **1173 bestanden, 0 Fehler** (vorher 812; Abschnitt 19: 326 Pruefungen); einzige `***`-Zeilen: die gewollten Heilungen in 18c und 19f |
| dieselbe gegen die in die Probe kopierten Dateien | **1173 / 0**, `ergebnis_probe.txt` byte-gleich mit `ergebnis.txt` |
| Gegenprobe Gesamt-Attrappe (14 Verderbnisse) | **14 von 14 rot** (1-35 Fehler je Verderbnis) |
| Attrappen der Bauer auf dem Endstand | kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1d_kern 147/0 (je byte-gleich mit `ergebnis.txt`); ober 116/0 + 117/0, b1b_ober 144/0 + 134/0, b1c_ober 193/0 + 180/0, b1d_ober 171/0 + 173/0; pruef_b == `ergebnis_b1b_nach.txt`, pruef_b1b (`run_nach.lua`) == `ergebnis_b1c.txt`, pruef_b1c == `ergebnis_nach.txt` |
| Text-/Beleg-Pruefer | `texte_pruefen.py` 0, `_b1b` 0, `_b1c` 0, `_b1d --tmp` 0; `belege.py` 0 von 112, `_b1b` 0 von 51, `_b1c` 0 von 89, `_b1d` 0 von 23 |
| Lua-Pruefer (25 Lua-Dateien des Stagings) | luacheck 0 failed, scopecheck 0, localcount hoechstens 77 insgesamt (World.lua:640, unveraendert), luacheck_pz 18 x W113 = die bekannten (3 Aktionsklassen in Menu.lua, 15 in der Bench; B1c 16 + `NCBear_CubGrow`/`_CubStats`); alle LF, reines ASCII |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (wie B1a-B1c) |
| Trockenlauf ohne `--vor-b5a` | **24 Fehler = genau die 24 Altlasten** aus `ALT_EXPECTED`, sonst nichts |
| Gegenprobe der neuen Skript-Regeln (verdorbene Staging-Kopie) | 5 Verderbnisse -> 6 Fehler, jede erkannt (3.3) |
| Probe `--probe probe_b1d --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**; 51 Dateien geschrieben (24 Lua, 5 Modell/Textur/Skript/Knoten/Bild, 21 Texte, `sandbox-options.txt`); alle vier Lua-Pruefer je kopierter Datei gruen, luacheck_pz 0 Treffer + 3 erlaubt |
| `staging_dateien.txt` neu | **51 Dateien: 2 neu, 25 ueberschreibt, 24 gleich** (gegen NCBearTest mit B1c, Stand 11.11. 08:12); jede "ueberschreibt"-Datei ist eine B1d-Aenderung |

## 1. Grenze KERN <-> OBERFLAECHE

### 1.1 Werkzeug `attrappe/gesamt/xref_b1d.py` (neu; loest `xref_b1c.py` ab, das an `local t = {...}` in `viewEntry` abbricht)
Aufruf `python -I xref_b1d.py [lua-Ordner]`, Exit 1 bei einer Luecke. Alles aus `xref_b1c.py` (1-7) plus die B1d-Punkte. Ergebnis
(`xref_b1d.txt`):
1. **B.*/U.***: 192 / 192 Namen definiert, U.* 21 / 21; U.* nie im KERN, B.* in der OBERFLAECHE nur `ShowNote`/`OnView`/`UI`; keine
   Funktion in zwei Dateien. **75 Funktionen aus Plan 6.2/6.3/6.4 je in ihrer Datei** (neu: 14 in `shared/BanditsNPCBearStats.lua`, 16 in
   `server/BanditsNPCBearGrow.lua`, `U.StageName`/`U.NoteText` in Client.lua). OBERFLAECHE ruft vom KERN genau die B1c-Liste + `ApplySize`
   (Plan 6.9 erlaubt dazu StatsOf, SkillProgress, SKILLS, SKILL_FIELD, GrowDays, GrowDay -- benutzt wird nur ApplySize, im Hud). Bench: 49
   Kern-Namen, alle definiert; die B1d-Liste aus Plan 6.9 ist vollstaendig (Bench ruft GrowDays, GrowSetG, GrowSetHp, SkillProgress,
   SkillSet, SkillXp, StatsOf, XpCum). **Ladefolge**: 0 Aufrufe auf Dateiebene vor ihrer Definition (`B.XpCum()` in Stats.lua steht nach
   seiner Definition).
2. **B.CFG**: 156 Felder; die 41 B1d-Felder aus Plan 5.2 stehen alle darin und werden gelesen (`bodySwap = false`); die lokalen Leser
   `cfg(key, def)` in Stats/Grow sind jetzt mit erfasst, alle Rueckfaelle == B.CFG; die acht Rueckfall-**Tabellen** in Stats.lua
   (`CURVE_DEF` ... `NEED_DEF`) == `growCurve` ... `xpNeed`; Hud `TAG_BASE`/`TAG_Z` == `tagBase`/`tagZ`. **B.OPTS == sandbox-options.txt**:
   27 Optionen; die fuenf B1d-Optionen mit Kevins Zahlen (`BearGrowDays` integer 100 (10..365), `BearDodgeMax` 40 (5..80),
   `BearFightBonusMax` 70 (0..200), `BearHealAwake` **double** 1.0 (0.0..10.0), `BearHealSleep` **double** 15.0 (0.0..100.0)), Text der Zahlen
   in B.OPTS gleich, Reihenfolge zwischen `BearCallCooldownMinutes` und `BearLog`; die lokalen `opt(name, def)`-Leser in Stats.lua (5) mit der
   Vorgabe von B.OPTS. **Optionen-Seite**: Ids und Reihenfolge `TagShow` (tickbox, true), `TagHealth` (combobox, Vorgabe 2 = Balken),
   `TagStamina` (combobox, 1 = Aus), `TagAge` (tickbox, true), `TagSize` (slider, 100); Eintraege je Auswahl Off/Bar/Number; alle fuenf
   Leser im Hud (`U.Opt`, `showMode("Id", SHOW_*)`) mit derselben Id und Vorgabe.
3. **Befehle**: unveraendert (B1d bringt keinen neuen Befehl); BaitDrop, Call, Hello, Mode, Rename -> `B.Handle`; Note, Sync -> Client.
4. **Sicht**: `viewEntry` baut 18 Felder, `B.GrowView` (nur `tame`, hinter `rec.st == "tame" and B.GrowView`) die 9 aus Plan 4.1
   (`sz hp hpMax sta staMax day stg nst nxt`), keine Kollision; die OBERFLAECHE liest an Sicht-Eintraegen nichts anderes (neu: day, hp,
   hpMax, nst, nxt, sta, staMax, sz; `stg` wird nicht gelesen).
5. **Texte**: UI.json 133, Sandbox.json 60, IG_UI.json 3 je Sprache, Paritaet und Platzhalter in 7 Sprachen, sortiert, Round-Trip, kein
   BOM/CR, kein `<`/`>`, kein Testwort; die 24 UI- und 10 Sandbox-Schluessel aus Plan 6.7 in allen 7 Sprachen, 12 EN-Texte wortgleich mit
   Plan 6.7; `U.EN` 133 == EN/UI.json **wortgleich**; 125 Schluessel als Literal im Code, alle in EN; jeder EN-Schluessel benutzt; 49
   `U.T("KEY", ...)` mit so vielen Werten wie Platzhaltern; Optionen-Seite 18 Texte, alle Schluessel (auch `addComboBox`/`addItem`).
6. **Meldungen**: U.NoteText setzt je `t` ein: days/dir/name/num/stage/wait 1 Wert, skill 2; die zwei B1d-Meldungen in Tabellen-Form
   `B.Tell(p, { k = ..., t = ... })`: `Note_Grown` t `stage` (1 Platzhalter), `Note_SkillUp` t `skill` (2) -- passt; Stufen
   half/strong/adult (Client `STAGE_KEY` == Stats.lua `STAGE_KEYS` == Grow.lua `STAGE_LOG`), Faehigkeiten agi/vit/con/fgt/fsh/nos (Client
   `SKILL_KEY` == `B.SKILLS`).
7. **Bild**: unveraendert (96 x 96, byte-gleich mit Kevins Quelle).
8. **Dateiregeln (Plan 7.1 Nr. 18)**: `:setSizeForced(` und `:getData(` je genau einmal, Stats.lua:345/:342 in `B.ApplySize`; `:setHealth(` und
   `:getHealth(` je genau einmal, Grow.lua:237/:205 in `B.BodyHp` (ohne Bench); `NCBear_*` im Code ausserhalb der Bench: 0.

**Gegenprobe** (`gegenprobe_b1d.py`, Temp-Kopie des Stagings, je eine Verderbnis): GrowView ohne `nxt`, Hud liest `c.foo`, TagHealth-Vorgabe
Zahl, RU ohne `Tag_Age`, `BearHealAwake def = 1` statt `1.0`, `STAGE_KEY` ohne adult, `setHealth` in Server.lua, `Note_Grown` mit `t = "num"`,
`CURVE_DEF` weicht ab, `bodySwap = true`, Probebefehl im Code, fester Optionen-Text -> **12 von 12 erkannt** (die Regel "Note_Grown traegt t
stage, Note_SkillUp t skill" kam durch die Gegenprobe dazu).

### 1.2 Von Hand nachgesehen (was ein Grep nicht sieht)
- **Groesse ueber die Grenze**: der Schreiber setzt am Tier `sz = min(s, cubMaxSize)` (Hirn-Takt, neuer Koerper, Probebefehl); der MP-Client
  setzt seine Kopie im Listenbau aus `c.sz` ueber dieselbe `B.ApplySize` (Hud.lua:441-458, nur `isClient()`, nur gewollte lebende zahme
  Junge); im SP schreibt der Hud nie (Gesamt 19b: Kopie verstellt -> Hud schreibt nicht, der naechste Hirn-Takt setzt den Schreiber-Wert).
- **Leben**: die Sicht traegt `hp` in Prozent; nach dem Zaehmen holt der erste Hirn-Takt das Leben vom Koerper und die Sicht traegt es
  danach (19a: `hp` 100); nach der Register-Heilung ebenso (19f: 60).
- **Stufen-Meldung**: einmal je Aufstieg, auch aus dem Fuetter-Bonus (`tellStage`), nur an den Besitzer; im MP nur A (19m), B bekommt keine.
- **Fuetter-Bonus haengt am vorhandenen Fuetter-Weg**: `B.GrowFeed` vor dem vorhandenen Commit in `B.FeedComplete`, nach `takeOne`; ein
  Fremder scheitert vorher an `B.CheckFeed` (19m: Why_NotOwner, Bs Fisch bleibt, kein Bonus).
- **NPC Crew** setzt an fremden Tieren weder Groesse noch Leben: `grep setSizeForced|getData():setSize|:setSize(` in `NC 42/media/lua`: 0;
  `setHealth(` an Tieren nur `NC shared/BanditsNPCLivestockSlaughter.lua:2016` (`setHealth(0)` beim Schlachten des eigenen Viehs), dieselbe
  Datei liest `Lv.NOT_TENDED` (`:548-550`, `:1025-1026`) -- unser Junges ist dort ueber Naht 1 nicht gepflegt (NAEHTE.md Zeile 25).

### 1.3 Luecken geschlossen
**Keine Luecke ueber die Grenze gefunden; im Staging nichts geaendert.** Werkzeug-Befund (Z3): der Zahlen-Ausdruck von `xref_b1c.py`
schnitt `0.10`/`1.5` am Zeilenende vor einem Tabellenfeld auf `0.`/`1.` ab (haette falsche Rueckfall-Hinweise gemeldet) -- in `xref_b1d.py`
berichtigt.

## 2. Gesamt-Attrappe `attrappe/gesamt/run.lua`

Aenderungen: `FILES` + `shared/BanditsNPCBearStats.lua`, `server/BanditsNPCBearGrow.lua` (Ladefolge wie im Spiel); `ISPanel:drawRect` merkt
sich die Rechtecke (Fuellbreite der Wert-Balken, Zaehlung wie bisher); **gewollt geaendert (je Kommentar "B1d")**: die Abschnitte 8, 17a
und 17i schalten ueber `b1cTag()` die neuen Vorgabe-Zeilen aus (Alter-Zeile, Leben-Balken) -- mit B1d-Dateien fielen dort sonst 5 alte
B1b-Erwartungen (Schild jetzt 6 Texte, Zustand 12 px hoeher), wie beide Bauer gemeldet hatten; die alten Pruefungen selbst sind
unveraendert. Lauf gegen die Probe (ohne Werkbank): die Werkbank wird aus dem Staging dazugeladen (nur die Testhilfe). **Abschnitt 19
(neu, Plan 7.3; 326 Pruefungen)** in einer namenlosen Funktion (der Hauptteil hat schon 200 lokale Namen, Lua 5.1); Wachsen ueber ECHTE
Langsam-Takte (`EveryTenMinutes` je 10 Spielminuten):
- **19a** wild -> entdeckt -> gefuettert -> gezaehmt; vor dem ersten Langsam-Takt kein `g`; danach `g` = 10 min / 2400 h (aus `tamedAt`, nicht
  doppelt); Sicht Tag 0, sz 0,35, Jungtier, "halbstark in 15 Tagen", Leben max 40, Ausdauer 50/50; Traglast 10, Schaden 0; erster Hirn-Takt:
  Leben vom Koerper (1,0, Sicht 100). **Anzeige**: Vorgaben = Name, Zustand, "Day 0 - half-grown in 15 day(s)" + roter Balken voll (64 px),
  kein gelber; Leben als Zahl "Health 40/40"; Ausdauer als Zahl "Stamina 50/50", als Balken voll; Name/Alter/Leben aus + Ausdauer Balken ->
  nur der gelbe Balken; alles aus -> kein Schild.
- **19b** 15 Spieltage (2160 Langsam-Takte): **jeden Tag** innere Groesse, Leben, Ausdauer, Traglast und Schaden groesser als am Vortag; Tag 5:
  Engine-Groesse folgt der Kurve, Sicht Tag 5 / Leben max 77; genau eine "Your bear is half-grown now."; Sicht Tag 15, halbstark, "kraeftig in
  30 Tagen", sz 0,75, Leben 150, Ausdauer 100; Werte 0,75 / 40 / 0,35; Hirn-Takt -> Engine-Groesse 0,75; Schild "Day 15 - strong in 30
  day(s)"; weiter zahm. Wildes Vergleichs-Junges: kein `g`, Groesse 0,35, nie gesetzt, keine Werte in der Sicht. SP: der Hud schreibt nie.
- **19c** Fuettern am zahmen Jungen (Fisch = Lieblingsfutter): + 3 Spielstunden, `gF`, Spiegel mit g/gF/gFn; zweite Fuetterung nach der
  Abklingzeit + 3 h; dritte am selben Spieltag: kein Bonus; je Fuetterung genau ein Stueck weg.
- **19d** Follow me, Besitzer rennt 30 x 5 Kacheln: das Junge rennt hinterher, Kondition +5..24 XP (Eimer), Ausdauer (Sitzung) gesunken, Sicht
  < 100, Schild "Stamina N/100"; Stehen -> voll, Sicht 100.
- **19e** weitere 30 Spieltage: genau eine "Your bear is strong now."; innere Groesse >= 1,0, Leben >= 254, Traglast >= 65; Engine-Groesse
  bleibt 0,75 (keine Schreibung); Sicht kraeftig / naechste erwachsen / Tag 45-47; `NCBear_CubStats()` "size inner 1.0.. / shown 0.750".
- **19f** `NCBear_CubHurt(60)` -> Leben 60 % (Register und Koerper), Spiegel v2 traegt g/gF/xCon, nicht hp/hpB/gAt -> **Absturz** (Register
  weg, Spiegel bleibt) -> zurueck mit gleichem `g`, gleicher Erfahrung, gleichem Fuetter-Bonus, gleichem Tag; "Your bear is back."; Leben vom
  Koerper (60 %, nicht 100 %), Groesse 0,75, Sicht 60.
- **19g** einsteigen (14 Kacheln) -> 1 Spieltag Fahrt: `g` + 1/100, Leben + 24 % nur im Register -> **Speichern/Laden in der Fahrt** (ride, g,
  hp im Register) -> aussteigen: genau ein neues Tier, sofort 0,75 (`B.GrowBody`), Leben aus dem Register (0,84), nicht 100 %.
- **19h** Call to me: altes Tier weg, genau ein neues, Groesse 0,75, Leben wie im Register, gleicher Tag.
- **19i** Speichern/Laden: g, xCon, hp gleich; Engine setzt die Groesse zurueck (0,35) -> der Hirn-Takt setzt wieder 0,75; Sicht Ausdauer voll
  (Sitzung neu), Leben wie vorher.
- **19j** `NCBear_CubGrow(100)`: g = 1, genau eine "Your bear is full-grown now."; innere Groesse 1,35, Tag 100, erwachsen; Leben 400,
  Traglast 100, Schaden 1,0, Ausdauer 160; Bild bleibt 0,75; Sicht ohne naechste Stufe; Schild "Day 100 - full-grown"; **Tod** -> Eintrag
  und Sitzung weg.
- **19k / 19l** Sandbox **30 Tage**: halbstark nach 4,5, kraeftig nach 13,5, ausgewachsen nach 30 Spieltagen (je auf einen Takt genau), Sicht
  Tag 30 / Leben 400. Sandbox **365 Tage**: halbstark nach 54,75 Spieltagen, Sicht Tag 54, "kraeftig in 110 Tagen", Engine-Groesse 0,75.
  SP am Ende: genau 1 Heilungszeile (19f), sonst keine `***`-Zeile.
- **19m** MP (Server, A Besitzer, B fremd, Sandbox 10 Tage): Server fuehrt g und Leben; **A abgemeldet -> 1 Spieltag ohne Wachstum**; nach 1,5
  Spieltagen genau eine `Note_Grown` (t stage, v half) nur an A; Sync an A und B mit denselben Zahlen (sz 0,75, Tag 1, Leben 100, "in 3
  Tagen"); Server-Tier 0,75; **Client-Probe**: Bs Kopie mit 0,35 -> Listenbau setzt genau einmal 0,75, danach keine Schreibung mehr; B und A
  sehen "Day 1 - strong in 3 day(s)" und den Leben-Balken; B fuettert As Junges -> abgelehnt, Why_NotOwner, kein Bonus, Fisch bleibt;
  Server-Neustart: g und hp bleiben, Groesse 0,75; keine `***`-Zeile.

**Gegenprobe** (`gegenprobe_b1d.py`, je eine Verderbnis): GrowSlow waechst nie (35 Fehler), cubMaxSize ignoriert (13), kein GrowBody (2),
Spiegel-Heilung ohne GrowFromMark (2), MARK_FIELDS ohne g (3), Hud ignoriert TagAge (7), Client-Probe auch im SP (1), Fuetter-Bonus ohne
Tagesdeckel (1), Uhr ohne Besitzer-Pruefung (4), Ausdauer sinkt nie (2), Heilen ohne Koerper aus (2), GrowView ohne hp (7), Kurve ohne Knick
bei 0,45 (11), kein GrowFeed (4) -> **14 von 14 rot**.

**Grenze der Attrappe** (wie B1a-B1c): Langsam-Takte laufen ohne Hirn-Takte dazwischen (100 Tage in Sekunden); `fleeTo`/`pathToLocation`
setzen das Tier sofort ans Ziel; `setSizeForced` und `setHealth` an einem lebenden Tier, die Engine-Heilung, die Klemme beim Laden und die
Netz-Uebertragung der Groesse bildet sie nur nach (NUR JAR), sie beweist sie nicht. Ein Lua-Zustand fuer Server und beide Clients.

## 3. Uebernahme-Skript `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md`

### 3.1 Was sich aenderte (Plan 10)
- **Tier-Regeln neu** (jedes Vorkommen des Namens im Code-Teil, auch als String, wie B1c `animalRunning`/`pathToLocation`):
  `setSizeForced`, `getData` nur in `B.ApplySize` (`shared/BanditsNPCBearStats.lua`); `setHealth`, `getHealth` nur in `B.BodyHp`
  (`server/BanditsNPCBearGrow.lua`).
- **Cheat-Pruefung neu, Regel `probeweg`**: `B.GrowSetG`, `B.GrowSetHp`, `B.SkillSet` (Vorspulen, Leben/Erfahrung setzen) haben im kopierten
  Code keinen erlaubten Aufrufer (leere Menge, nur die Definition -- `TIER_DEF` um die drei Namen erweitert); eine Regel ohne erlaubten Aufrufer
  meldet keine "kein erlaubter Aufruf"-Warnung. Die Namen selbst treffen kein Cheat-Muster (`CHEAT_NAME`), Umbenennen war nicht noetig.
- Die zwei neuen Lua-Dateien deckt `LUA_BEAR`; die fuenf neuen Optionen (zwei `double`) prueft `plan_sandbox` unveraendert (Zahlen als Text gegen
  `B.OPTS`); `addComboBox`/`addItem` kannte `mo_text_hits` schon (B1c).
- Kopftext (B1d-Zeile, Punkt 6 mit den B1d-Regeln), Naehte-Zeile im Plan-Ausdruck.
- `NAEHTE.md`: Kopf (Stand B1d, keine neue Naht, 2 Lua, 24 Texte, 5 Optionen), Zeilen 4 (27 Optionen, B1d-Zahlen, `type = double` hat NPC
  Crew selbst, NC `42/media/sandbox-options.txt:14` -- gelesen in der Probe-Kopie), 5 (133 / 60 Texte), 11 (Register-/Spiegel-/Sicht-Felder
  B1d), 14 (Werte-Zeilen), 15 (Wachsen gebaut, Engine-Stufen bewusst nicht, Modellwechsel aus), 19 (`addComboBox`/`addItem`, NPC Crew
  gespielt `client/BanditsNPCModOptions.lua:95-103`), **neu 25** (Groesse und Leben am Tier; NPC Crews Tier-Code gegrept, Plan 10); Absatz "B1d,
  vom Skript erzwungen"; "Die Zeilen: keine" auch fuer B1d.

### 3.2 Laeufe (Ausgaben im Ordner `_arbeit/baer_zaehmen/`)
- `trockenlauf_b1d_vor_b5a.txt`: **OK, 0 Fehler, 26 Warnungen** (1 Clip-Warnung GLB, 24 Altlasten, 1 NPC-Crew-Kommentar). Kopieren: 24 Lua,
  5 Modell/Textur/Skript/Knoten/Bild. Texte: UI.json 133 neu (NPC Crew 3812 -> 3945), Sandbox.json 59 neu (92 -> 151), IG_UI.json 3 (neu).
  Sandbox: 27 Optionen (NPC Crew vorher 42). Cheat-Pruefung: 24 Lua, 6621 Codezeilen, **Funde 0**; Tier-Regeln je an ihrem Ort
  (setSizeForced Stats.lua:345, getData :342 -- B.ApplySize; setHealth Grow.lua:237, getHealth :205 -- B.BodyHp; probeweg: kein Aufruf).
  "Texte aus der Lua: 125 benutzt, fehlen in EN: 0; Ersatztexte 133, wortgleich: ja". Kollisionen 0.
- `trockenlauf_b1d.txt` (ohne `--vor-b5a`): 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere.
- `probe_b1d_ausgabe.txt` (nur unter `_arbeit/baer_zaehmen/probe_b1d/`): OK, 0 Fehler, 26 Warnungen, 51 Dateien, luacheck/scopecheck/localcount
  je kopierter Datei gruen (Stats.lua hoechstens 32, Grow.lua 24 lokale Namen), luacheck_pz 0 Treffer + 3 erlaubt.

### 3.3 Gegenprobe der Skript-Regeln
Scratch-Staging mit `obj:getData():setSizeForced(c.sz)` im Hud (statt `B.ApplySize`), `a:setHealth(1)` in `liveRec`, `local HPNAME =
"getHealth"` in Guard.lua, `B.GrowSetG(nil, 1)` in `B.FeedComplete`, `local skillSet = B.SkillSet` im Menue -> **6 Fehler** (Hud trifft
`setSizeForced` UND `getData`), jeder an seiner Stelle.

## 4. `staging_dateien.txt` und `mod_info_vorschlag.txt`
- `staging_dateien.txt` neu (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen NCBearTest mit B1c): **51 Dateien, 2 neu**
  (`server/BanditsNPCBearGrow.lua` 1ffbff14beb28025261bdc48c5d1025d / 28411, `shared/BanditsNPCBearStats.lua`
  42dfb2e084023be34d2059377c37b0eb / 13895), **25 ueberschreibt** (Client, Options, Hud, Bench, Heal, Registry, Ride, Server, Bear, Defs, 14
  JSON, `sandbox-options.txt`), **24 gleich**. Jede "ueberschreibt"-Datei ist gegen die B1c-Liste geaendert; keine Datei, in der die Test-Mod
  vom B1c-Staging abweicht. Bench weiter "nur Testhilfe".
- `mod_info_vorschlag.txt`: Beschreibung um B1d ergaenzt (100 Tage, Meilensteine, taeglich steigende Werte, Bild bis halbstark, Fuettern,
  langsame Selbstheilung, Kondition, Faehigkeiten vorbereitet, Anzeige-Optionen), die vier neuen Testhilfen `NCBear_CubGrow/_CubStats/_CubXp/
  _CubHurt` (25 gesamt, gegen die Bench gezaehlt); ASCII, LF, fuer `mod.info` UND `42/mod.info`.

## 5. Einzelspieler und Mehrspieler
| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Wachsen | Langsam-Takt beim einen Programm, Besitzer `__sp` (19b, 19e, 19k, 19l) | Server, nur mit eingeloggtem Besitzer (19m: abgemeldet steht die Uhr); Clients rechnen nie |
| Groesse am Tier | Schreiber-Objekt = gezeigtes Objekt; der Hud schreibt nie (19b) | Server setzt seine Kopie; Client-Probe im Listenbau aus `c.sz`, nur bei Abweichung (19m) |
| Leben | `B.BodyHp` am Schreiber; ohne Koerper nur im Register (19g) | Server (`getHealth` am Tier am MP-Server: Testpunkt); Clients sehen `hp` aus der Sicht |
| Fuetter-Bonus | direkt (19c) | am Server; Fremde scheitern an `B.CheckFeed` (19m) |
| Meldungen | `B.Tell` -> `B.ShowNote` direkt | `sendServerCommand(Note)` nur an den Besitzer (19m) |
| Register-Heilung / Mitfahren / Call / Laden | 19f / 19g / 19h / 19i | Server-Neustart 19m; Spiegel-Deckel im MP (b1d_kern 12) |
| Probebefehle | `NCBear_CubGrow/_CubStats/_CubHurt` (19e, 19f, 19j) | Bench lehnt ab ("singleplayer only", b1d_ober) |
Rote Linien: kein Gegenstand erzeugt oder vernichtet (der Bonus haengt am vorhandenen `takeOne`, 19c: ein Stueck je Fuetterung; 19m: Bs Fisch
bleibt), nie zwei Tiere eines Eintrags (19g/19h zaehlen), kein neuer Client-Befehl (kein neuer Kick-Weg), nichts haengt (alles in
vorhandenen Takten, Deckel je Eintrag und Eimer), keine NPC-Crew-Figur beruehrt (1.2).

## 6. Befunde des Zusammenbaus (fuer Pruefer / Kevin; kein Code geaendert)
- **Z1 (Hinweis, so geplant):** die Ausdauer-Zeile bei FREMDEN ist bis zu einer Spielstunde alt -- nur der Besitzer bekommt die gedrosselten
  Ausdauer-Nachschuebe (`B.Touch(nil, rec.owner)`, Grow.lua:387, Plan 0.11); ein Fremder sieht den Wert der letzten Sicht (stuendliches
  Commit). Die Zeile ist per Vorgabe aus. Frage an Kevin unten.
- **Z2 (Hinweis):** nach einem Registerverlust hat der erste Langsam-Takt `dt` 0 (das neue Register kennt keine letzte Uhrzeit,
  Server.lua:567-569): 10 Spielminuten Wachstum und Heilung fehlen, zusaetzlich zu hoechstens einer Spielstunde seit dem letzten Spiegel-Commit
  (Gesamt 19f/19g, die Attrappe rechnet damit). Harmlos.
- **Z3 (Werkzeug):** Zahlen-Ausdruck in `xref_b1c.py` (siehe 1.3), in `xref_b1d.py` berichtigt.
- **Z4 (Test-Grenze):** in der Gesamt-Attrappe laufen 100 Spieltage ohne Hirn-Takt; ob `EveryTenMinutes` beim Schlafen/Vorspulen im Spiel jede
  Stufe feuert (Deckel 1 h je Schritt), bleibt offen (Plan 12).

## 7. Offen / ungeprueft (Testpunkte; PLAN_B1D.md 7.4 ist Kevins Testliste)
1. **Alles Laufzeit-Verhalten ungespielt**: `setSizeForced` an einem lebenden Tier in der Welt (Vanilla nur an Haken-Tieren; sieht man den
   Wechsel, ruckt es, wirkt es direkt nach `addToWorld`); `setHealth` mit Werten zwischen 0 und 1 an einem lebenden Tier (Vanilla setzt nur 0);
   die Engine-Heilung ~1,5-2,2 %/h (NUR JAR) und ihr Zuruecknehmen; ob die Engine eine gespeicherte Groesse > 0,35 beim Laden behaelt (Weg B,
   NUR JAR); Fussgleiten und Schild-Hoehe bei 0,5-0,75 (F2).
2. MP: `getHealth` am Tier am dedizierten Server (scheitert es: "slow tick: ..." / "brain tick: ..." im Log); ob die Client-Kopie die gesetzte
   Groesse behaelt und kein Kick kommt; A3 aus B1a gilt weiter.
3. Wie viel Rennen in 100 Tagen zusammenkommt (F14); `addItem` uebersetzt beim Laden (Sprachwechsel bis zum Neustart alt).
4. NPC Crew wird parallel weitergebaut (v3.14.70): Trockenlauf und Probe vor einer echten Uebernahme (erst nach B5a) neu laufen lassen und NPC
   Crews Tier-Code erneut greppen (NAEHTE.md Zeile 25).

## 8. Fragen fuer Kevin (Kevin schlaeft -- nichts davon haelt den Einbau auf; gebaut ist jeweils die Empfehlung; die Planer-Fragen F1-F18 in PLAN_B1D.md 11 gelten weiter)
1. **F1** Definition geaendert (`maxSize` 1,35, `ageToGrow` 36500), damit die Groesse Laden und MP uebersteht? Empfehlung: ja (so gebaut).
2. **F2/F11** Das Bild des Jungen waechst bis halbstark (0,75) und bleibt dort; bitte mit `NCBear_CubGrow(15)` ansehen (Fuesse, Schild). Junges-
   oder Erwachsenen-Modell fuer halbstark? Empfehlung: nach dem Ansehen entscheiden.
3. **F3** Leben 40 / 150 / 400, Ausdauer 50 / 100 / 160, Schaden 0 / 0,35 / 1,0 als Vorgabe? Empfehlung: ja.
4. **F5** Das Spiel heilt das Junge selbst ~2 %/h; B1d nimmt das zurueck, damit es bei deinen 1 % bleibt. Empfehlung: so lassen, mit B5a neu fragen.
5. **F7** Fuetter-Bonus +3 h (Lieblingsfutter) / +2 / +1, hoechstens 2 je Tag, gesamt hoechstens 10 Tage frueher? Empfehlung: ja.
6. **F9** Anzeige-Vorgaben: Leben als Balken an, Ausdauer aus, Alter-Zeile an? Empfehlung: ja.
7. **F16** Meldungen "Your bear is half-grown now." / "Your bear's endurance is now level 3." -- gewuenscht? Empfehlung: lassen.
8. **F17 + Z1** Fremde sehen die Werte deines Baeren, wenn sie die Zeilen einschalten; ihre Ausdauer-Zeile ist dabei bis zu einer Spielstunde alt.
   So lassen oder die Ausdauer fuer Fremde ganz weglassen? Empfehlung: so lassen (Zeile ist per Vorgabe aus).
9. **F18** MP: die Erfahrung ist nach einem Server-Registerverlust aus dem Tier nicht pruefbar (Wachstum ist gedeckelt). Empfehlung: so lassen.
10. **Regel-Frage (wie B1c A3)**: `addComboBox`/`addItem` haben in Vanilla und Bandits keinen Aufrufer (nur die Definition, reines Lua); NPC Crew
    benutzt sie gespielt. Zaehlt das als Beleg? Empfehlung: ja.

## 9. Einbau (NICHT gemacht -- nur wenn Kevin nicht spielt)
`tasklist | grep -i ProjectZomboid` leer -> Zip der Test-Mod nach `Zomboid/backups/NCBearTest/`, die 27 Dateien mit Zustand neu/ueberschreibt
aus `staging_dateien.txt` in EINEM Zug kopieren (die 24 "gleich" aendern nichts), byte-gleich nachzaehlen (MD5-Spalte), Beschreibung aus
`mod_info_vorschlag.txt` in `mod.info` und `42/mod.info`, zweites Zip. Danach **Spiel neu starten** (Lua und Tier-Definition laden nur beim
Start), `bugwatch.py` mitlaufen lassen, Test nach PLAN_B1D.md 7.4 (Debug-"Tier Cheat" AUS, `NCBear_CubLog(true)`). Kevins B1c-Junges bekommt
beim ersten Laden sein Alter aus der Zaehm-Zeit (eine Diagnose-Zeile, keine Fehlerzeile).

Statisch geprueft, nicht gespielt.
