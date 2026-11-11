# Lauf baer-b1c: NACHBESSERUNG (11.11.2026)

**Statisch geprueft, nicht gespielt.** Grundlage: `pruef_b1c_a.md` (A1-A7) und `pruef_b1c_b.md` (B1-B10). Jeden Befund selbst am Code
nachgeprueft (Code gelesen, Jar-Auszuege `dec/IsoAnimal.java`, `dec/IsoGridSquare.java`, Vanilla-Stellen nachgelesen). Geschrieben nur:
Staging `mod/` (9 Lua-Dateien), Attrappen (`kern/attrappen.lua`, `b1c_kern/run.lua` + `ergebnis.txt`, `b1b_kern/ergebnis.txt`,
`pruef_b1c/ergebnis_nach.txt`, `gesamt/xref_b1c.txt`, `b1c_ober/texte_pruefen_b1c.py`, neu `uebernahme_b1c/probe_regeln.py`),
`baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `PLAN_B1C.md` (Kevins Test 7.4), `schnittstelle_aenderungen.md` (Abschnitt "B1c
NACHBESSERUNG"), `staging_dateien.txt`, die Probe unter `probe_b1c/` und die Ausgaben `trockenlauf_b1c_nach*.txt`,
`probe_b1c_nach_ausgabe.txt`. Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits. Kein git, kein Spielstart, kein Download.
Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`, `B:` Bandits `42.22/media/lua/`.

## 0. Ergebnis je Befund

| ID | Schwere | Urteil | Was getan |
|---|---|---|---|
| A1 | major | **bestaetigt** (`S:server/BanditsNPCBearRegistry.lua` RecOf fiel nach Heil-Ergebnis nil auf `B.NewRec("found")`) | `B.RecOf`: Spiegel tame/missing (v1 und v2) oder fed (v2) + Heilung nil -> `nil, "heal"` (Menue `Why_Gone`), kein neuer Eintrag, Spiegel bleibt; der Suchlauf stellt es her, sobald ein Platz frei ist. v1 "fed" (nie herstellbar) bleibt ein Fund wie in B1b |
| A2 | minor | **bestaetigt** (`getActionStateName`/`getVariableBoolean`/`IsReanimatedForGrappleOnly` nur clientseitig belegt) | Signal "rennt ohne eigenen Befehl" nur noch im Einzelspieler; am Server Stress-Sprung + neues B5-Signal (nur `getX/getY`); `grapple` nur im SP. Kommentare (Guard.lua Kopf, calmTickBody, World.lua B.ZedNear, Server.lua A3-Ausweitung) und Kevins MP-Test 8 ehrlich |
| A3 | minor (Regelfrage) | **bestaetigt** (grep V/B: nur Definitionen `V:client/PZAPI/ModOptions.lua:64-86`, `:206-228`) | Code bleibt; Kopf `S:client/BanditsNPCBearOptions.lua` und NAEHTE Zeile 19 ehrlich "kein Aufrufer, nur Definition gelesen"; **Frage an Kevin** |
| A4 | minor | **bestaetigt** (Regex-Probe nachgestellt) | Tier-Regeln `animalRunning`/`pathToLocation` werten jedes Vorkommen des Namens im Code-Teil (auch String, Gross/Klein egal), zweite erlaubte Stelle Guard.lua `calmTickBody`; Optionen-Seite ueber neue Funktion `mo_text_hits` (anderes Literal, Verkettung, `getText(...)`/`U.T(...)`, jeder Ausdruck = Fund). Neue Gegenprobe 34/0 |
| A5 | minor | **bestaetigt** (Block fast wortgleich mit `NC:client/ISUI/BanditsNPCMiniMap.lua:237-275`) | eigene Form: Hilfsfunktion `hook(key, cls, mini)` mit Merker `hooked[key]` (`S:client/ISUI/BanditsNPCBearMap.lua`); Kopf nennt ehrlich die Lehre aus NC v3.9.55. Wirkung gleich (gesamt 18b/18i, b1c_ober gruen); `texte_pruefen_b1c.py` prueft die neue Form |
| A6 | minor | **bestaetigt** (alle vier Stellen) | (1) Server.lua: Verweis auf den Kommentar ueber `B.ScanAnimals` statt einer Zeile; (2) Ride.lua Kopf, World.lua `B.Players`/`B.DeadAt`: getZ `:191`; (3) Registry.lua InitRegistry-Kommentar: "kommt beim Wiederfinden zurueck; Call to me fuer Unanklickbare spaeter ueber das Baeren-Fenster (F4)"; (4) ENT nur angemerkt (unten 3) |
| A7 | minor | **bestaetigt** | `b1b_kern/ergebnis.txt` neu (204, Laufbefehle 79/79/93); NAEHTE Stand v3.14.70 / UI.json 3812; unbenutzt entfernt: Guard.lua W311 (Vorbelegung), Heal.lua `capLine(o, ...)`. FR-Geschlecht: **nicht geaendert** -- `texte_pruefen_b1c.py` erzwingt Plan 1.10 "nur ES"; **Frage an Kevin** |
| B1 | major | **bestaetigt** (Attrappe pruef_b1c 1a nachgefahren) | neu `B.TakeNewerMark(rec, mark)` (Heal.lua): ein Spiegel mit gleichem `u` und hoeherem `r` derselben Epoche (oder der Quell-Epoche eines geheilten Eintrags) gewinnt **im Einzelspieler**, geklemmt wie `B.Restore`, nie zurueck aus tame, Deckel je Spieler; gerufen in `bind` (Heil-Regel 1a) und im Suchlauf Schritt 2. **Mehrspieler: das Register gewinnt** (strenger als der Vorschlag, Begruendung 1.2) |
| B2 | major | **bestaetigt** (Attrappe 2a/2b) | `B.SpotNear(x, y, z, r, turn)`: nur Kachel im selben Raum (`getRoom`, `V:shared/Util/AdjacentFreeTileFinder.lua:240`), Weg zum Spieler Schritt fuer Schritt ohne Sperre (`isBlockedTo`, `V:shared/Foraging/ISForageAction.lua:7`, `V:shared/TimedActions/ISDropWorldItemAction.lua:7`), Anfang im Ring wandert mit `rec.gen` (kein Engine-Zufall noetig) |
| B3 | minor | **bestaetigt** (Attrappe 1b) | Suchlauf Schritt 3 sortiert nach `gen`, dann `r` absteigend (stabil ueber die Listen-Reihenfolge); Heil-Regel 1a (nur SP): lebt eine zuerst geheilte alte Kopie, bindet der neuere Koerper und holt dessen Stand (`rec.healed.r`/`.gen` neu) |
| B4 | minor | = A1 | mit A1 |
| B5 | minor | **bestaetigt** (Engine: Stress klemmt bei 100, `dec/IsoAnimal.java:2367-2368`; Zerfall nur ohne Regen/Hunger, `:670-700`) | `B.MoveTo` merkt Ziel und Abstand (`s.tx`, `s.ty`, `s.td0`); `B.CalmTick` meldet "away", wenn ein FOLGENDES Junges waehrend eines eigenen RENN-Befehls mehr als `ownAway` 3 Kacheln weiter vom Ziel ist als beim Befehl; danach `ownAwayQuietMs` 5 s Ruhe. Nicht beim Bleiben/Gehen (Schleifen-Schutz, 1.5) |
| B6 | minor | **bestaetigt** (`dec/IsoAnimal.java:783-784` nur pathToLocation; `:2525` fleeTo setzt true) | nur Kommentar (Guard.lua calmTickBody) und Kevins Test 7.4 Punkt 4; Code nicht geaendert (Kevins Wort offen) |
| B7 | minor | **bestaetigt** (Regel 23 flieht vom Zombie, auch wenn der Besitzer dahinter steht) | **nicht geaendert**: Verhaltens-Frage an Kevin, zusammen mit B5a (Zombies greifen an); haengt nicht (Attrappe 3a endet am Besitzer) |
| B8 | minor | **bestaetigt** | `B.ZedNear`: Rahmen aller Punkte +- r einmal je Aufruf, je Zombie zuerst 4 Vergleiche (beide Zweige); Zombies ausserhalb: nur getX/getY |
| B9 | minor | **bestaetigt** | `B.HandleCall`: findet `B.FindAnimal` das alte Tier nicht und ist dessen Gegend geladen, erst EIN `B.ScanAnimals(nil)` (hoechstens je `scanMs`, Merker `B._callScanAt`), dann wie bisher entfernen. Rest (alte Kopie nach Absturz direkt beim Spieler) bleibt wie Pruefer B empfiehlt |
| B10 | minor | **teils bestaetigt** | MP, Heil-Regel 1a: gleiche `gen` + andere AnimalID als `rec.aid` -> nicht binden, nichts entfernen, Fehlerzeile (AnimalID wird mit dem Tier gespeichert: `dec/IsoAnimal.java:1279`/`:1391`). Teil 2 (`mg > rg` nur ohne geladenes Tier mit `rec.aid`) **nicht gebaut**: braeuchte eine Objektliste je Heilung (teuer, A3); Restrisiko "umsetzen" ohne Diebstahl, offen |

**Kein Befund abgelehnt.** Neue Engine-Aufrufe: `square:getRoom()` und `square:isBlockedTo(square)` (je Vanilla-Beleg mit gleichen
Argumenttypen, s. B2) -- sonst keiner. Kein neuer `pcall`. Kein neuer Text (Texte unveraendert, alle 21 JSON byte-gleich). Kein Engine-Aufruf
ohne Fundstelle; nichts ueber Jar allein.

## 1. Einzelheiten

### 1.1 A1/B4 -- nie ein neuer Fund aus einem zahmen Spiegel
`B.RecOf` (`S:server/BanditsNPCBearRegistry.lua`, nach dem Heil-Aufruf): `st == "tame"`, `"missing"` oder (Fassung 2) `"fed"` und Heilung nil
-> `return nil, "heal"`. `handCheck` (`S:server/BanditsNPCBearServer.lua:167-169`) sagt dann `Why_Gone` wie bei "stale". Der Suchlauf liess
nil schon immer stehen (World.lua Schritt 3). Folge: ein Junges, das gerade nicht hergestellt werden kann, ist unberuehrbar, bis ein Platz
frei ist (Attrappe 10a: Platz frei -> naechster Suchlauf stellt es tame mit Name her). Grenze (ehrlich): im Mehrspieler bleiben Spiegel, die
NIE herstellbar sind (v1 "tame" ohne Konto, Besitzer `__sp`/nil), auf Dauer unberuehrbar (Frage 4).

### 1.2 B1 -- der neuere Spiegel gewinnt (nur Einzelspieler)
- "Neuer" ist pruefbar: im laufenden Spiel ist `mark.r` nie groesser als `rec.r` (jede Aenderung zaehlt `rec.r` hoch, der Spiegel bekommt
  hoechstens denselben Wert). `mark.r > rec.r` in derselben Epoche heisst: das Register ist aelter als die Zelle des Tiers (Absturz).
- Uebernommen (geklemmt wie `B.Restore`): st (missing -> tame), owner/bond/finder (SP: `__sp`), Balken, fedN/petN/last, Zeiten, mode,
  Name (`B.CleanName`), Heimat; `rec.r` auf `mark.r` (danach `B.Commit` +1). Bleiben: Kennung, `u`, Herkunft, Generation (max). Abgelehnt mit
  Zeile: zurueck aus tame/missing; Deckel `BearMaxPerPlayer` voll; fed bei schon gebundenem anderem Jungen.
- **Mehrspieler: das Register gewinnt** (nur eine Fehlerzeile je Junges und 10 min). Pruefer B schlug "Fortschritt ohne Besitzwechsel" vor;
  ich bin strenger: `r` steht im Spiegel, und den kann ein veraenderter Client am Server schreiben (Jar `dec/ObjectModDataPacket.java`,
  `forschung_b1c.md` 0.1) -- jeder uebernommene Wert (auch Balken eines eigenen angefuetterten Jungen) waere ein Schummel-Weg. Der Auftrag
  sagt "Server vertraut einem Spiegel nur, wenn kein Eintrag widerspricht"; ein aelterer Eintrag widerspricht. Frage 3.
- Attrappe b1c_kern 10c-10e: SP ueber Suchlauf Schritt 2 und ueber Heil-Regel 1a -> tame, Bruno, follow, genau eine Zeile; MP -> fed bleibt,
  Zeile "entry wins"; "shy"-Spiegel am zahmen Eintrag -> bleibt tame; Deckel voll -> bleibt fed. Pruefer Bs Fall 1a jetzt OK.

### 1.3 B2 -- Platz neben dem Spieler
- Raum: `sq:getRoom() == ownerSq:getRoom()` (draussen beide nil). Weg: von der Kandidaten-Kachel je Schritt eine Kachel Richtung Spieler
  (hoechstens 3), jeder Schritt `not cur:isBlockedTo(next)`. Jar `dec/IsoGridSquare.java:954-963`: Wand, Fenster, Tuer, Treppe zwischen den
  beiden Kacheln; Kanten-Test `:725-727` ueber die Kollisions-Merker `collideN/collideW` (`:813-830`). Ob niedrige Zaeune und jede Ecke so
  erfasst sind: **ungeprueft** (Testpunkt in 7.4 Punkt 8).
- Reihenfolge: Ring k = 8k Kacheln im Uhrzeigersinn, Anfang `(turn * 3) mod 8k`, `turn` = `rec.gen` (jedes Herholen erhoeht sie) -- ein zweiter
  Ruf probiert zuerst eine andere Kachel, ohne Zufall (in der Attrappe pruefbar). Kachel des Spielers nicht geladen -> nil.
- Kosten: hoechstens 48 Kacheln x (6 + 3 x 4) Aufrufe, nur beim Aussteigen/Rufen.
- Attrappe 10h (Haus, Wand, Weg ueber zwei Schritte, turn, zweiter Ruf); Pruefer Bs 2a/2b jetzt OK.

### 1.4 B3 -- der neuere Koerper zuerst
Schritt 3 heilt in der Reihenfolge gen, r (absteigend), Listenplatz. Fuer den Fall ueber zwei Suchlaeufe (erst nur die alte Kopie geladen):
Heil-Regel 1a bindet im SP das Tier mit hoeherer `gen`, wenn sein Spiegel aus derselben Quell-Epoche neuer ist (`rec.healed.ep/.r`, neu in
`B.Restore`); `B.TakeNewerMark` holt Name/Modus; die alte Kopie ist danach ungebunden und wird "stale" entfernt. Attrappe 10f/10g, Pruefer
Bs 1b jetzt OK.

### 1.5 B5 -- Flucht waehrend eines eigenen Befehls
Neues Signal "away" in `calmTickBody` (Fall (a)): nur bei Modus follow, nur bei einem Renn-Befehl (`s.walk ~= true`), Abstand zum eigenen
Ziel > `s.td0 + ownAway` (3). Warum so eng: beim Bleiben/Gehen fuehrt die Ersatz-Antwort einen kurzen Gehweg Richtung Heimat -- liegt die
Heimat hinter einem Haus, koennte "Umweg = Flucht" sonst eine Schleife bauen. Beim Folgen misst jede Antwort ab ihrer neuen Stelle neu
(`s.td0`), ein Umweg loest also hoechstens eine Antwort aus; dazu 5 s Ruhe je Junges. Kosten: 2 Aufrufe (getX/getY) je Bild, nur waehrend
eines eigenen Befehls; hoechstens 4 je Bild bleibt (getStress + 2). Attrappe 10i (Umweg 2 -> nichts, 4 -> "away", Ruhe, Bleiben, Gehen).
Grenze: ein BLEIBENDES Junges auf dem Heimweg bei Stress 100 wird weiter erst vom Bleiben-Weg zurueckgeholt.

### 1.6 A2 -- Seite am Mehrspieler-Server
Am Server (`not B.IsSP()`) fragt die Laerm-Wache weder `getActionStateName` noch `getVariableBoolean`, `B.ZedNear` nicht
`IsReanimatedForGrappleOnly` (dort zaehlt `isAlive`, `B:server/BanditSave.lua:52`). Attrappe 10j zaehlt: 0 Aufrufe am Server, Stress-Sprung
antwortet weiter. Kein pcall dazugebaut (ein pcall um unbelegte Aufrufe waere eine Tarnkappe).

### 1.7 A4 -- Skript-Regeln
- `TIER_RULES` (`baer/tools/baer_uebernahme.py`): `animalRunning` = `(?i)\banimalRunning\b`, erlaubt `(World.lua, B.MoveTo)` und
  `(Guard.lua, calmTickBody)`; `pathToLocation` = `(?i)\bpathToLocation\b`, erlaubt nur `B.MoveTo`. Im Code-Teil zaehlen Strings mit, also
  auch `local V = "animalRunning"`, `a["setVariable"](a, "AnimalRunning", ...)`, `a.pathToLocation(a, ...)`, `local f = a.pathToLocation`.
- `mo_text_hits(code_text)` (neu, Modul-Ebene) ersetzt die Inline-Pruefung der Optionen-Seite.
- Gegenprobe `attrappe/uebernahme_b1c/probe_regeln.py`: 16 Tier-Faelle, 17 Optionen-Faelle, echte Dateien (nur die drei erlaubten
  Stellen, 0 Funde auf der Seite) -> 34 Faelle, 0 Fehler. Trockenlauf zeigt die Tier-Regeln an `Guard.lua:217 (calmTickBody)`,
  `World.lua:859/860 (B.MoveTo)`.

## 2. Neue Zahlen (alle selbst gelaufen, 11.11.)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (23 Lua des Stagings) | 23 checked, 0 failed |
| `scopecheck.py` | 23 file(s), 0 violation(s) |
| `localcount.py` | aktiv hoechstens 39 (Bench `:369`), kopiert 37 (`World.lua:640` B.ScanAnimals, `:372` B.ZedNear, `Server.lua:909`, `Hud.lua:289`); insgesamt hoechstens 77 (`World.lua:640`) -- unter 180/200 |
| `luacheck_pz.py` | 16 x W113, alle erwartet (3 Aktionsklassen in Menu.lua, 13 Bench); `--unused` (22 kopierte): 6 Hinweise, alle harmlos (Hud.lua:472-474 `self` aus B1b, Guard.lua:282 `players` = Signatur `B.GuardStep`, Rules.lua:41/:160 aus B1a); die zwei B1c-Reste Guard.lua W311 (Vorbelegung) und Heal.lua `o` sind entfernt |
| Dateiform (49 Dateien) | alle LF, kein BOM, LF am Ende, keine Leerzeichen am Zeilenende, Lua/.txt ASCII: 0 Probleme |
| JSON (21) | Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert: 0 Probleme (byte-gleich wie vorher) |
| `attrappe/kern/run.lua` | **136 / 0** (byte-gleich `kern/ergebnis.txt`) |
| `attrappe/b1b_kern/run.lua` | **204 / 0** (`ergebnis.txt` neu geschrieben, A7) |
| `attrappe/b1c_kern/run.lua` | **192 / 0** (vorher 154; neu Abschnitt 10 mit 38 Pruefungen: A1/B4, B1, B3, B2, B5, A2, B8, B9, B10) |
| `attrappe/gesamt/run.lua` | **812 / 0**, byte-gleich mit `gesamt/ergebnis.txt` (einzige `***`-Zeile die gewollte Heilungszeile 18c) |
| dieselbe gegen die neue Probe (`probe_b1c/NPCCrew/42/media/lua/`) | **812 / 0**, byte-gleich mit `gesamt/ergebnis_probe.txt` |
| `attrappe/ober` / `b1b_ober` / `b1c_ober` (ohne / mit `kern`) | 116/0 + 117/0, 144/0 + 134/0, 193/0 + 180/0 (unveraendert) |
| `attrappe/pruef_b/run.lua`, `pruef_b1b/run_nach.lua` | byte-gleich mit `ergebnis_b1b_nach.txt` bzw. `ergebnis_b1c.txt` |
| `attrappe/pruef_b1c/run.lua` (Pruefer B, unveraendert) | **6 x OK, 0 x BEFUND** (vorher 4 BEFUND: 1a, 1b, 2a, 2b), `pruef_b1c/ergebnis_nach.txt` |
| `texte_pruefen.py` / `_b1b` / `_b1c` | FEHLER gesamt: 0 / 0 / 0 (`_b1c` prueft den Karten-Aufsatz jetzt in der Form `hook`) |
| `belege.py` / `_b1b` / `_b1c` | abweichend 0 von 112 / 0 von 51 / 0 von 89 |
| `gesamt/xref_b1c.py` | 0 Luecken, 3 Hinweise (unveraendert); B.* 159 / 159 (+ `TakeNewerMark`, `_callScanAt`), B.CFG 115 Felder, 114 gelesen (+ `ownAway`, `ownAwayQuietMs`) -- `xref_b1c.txt` neu |
| `uebernahme_force/probe_force.py` | 23 Faelle, 0 Fehler |
| `uebernahme_b1c/probe_regeln.py` (neu) | 34 Faelle, 0 Fehler |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (24 Altlasten, GLB-Clip, NC-Kommentar `shared/BanditsNPC.lua:1359`); 22 Lua, 5678 Codezeilen, Cheat-Funde 0; Tier-Regeln an ihren Orten; Kollisionen 0; "101 benutzt, fehlen in EN: 0; Ersatztexte 109, wortgleich: ja"; NPC Crew v3.14.70: UI.json 3812 -> 3921, Sandbox.json 92 -> 141, IG_UI.json neu 3 (`trockenlauf_b1c_nach_vor_b5a.txt`) |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere (`trockenlauf_b1c_nach.txt`) |
| Probe `--probe _arbeit/baer_zaehmen/probe_b1c --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**, 49 Dateien geschrieben; je kopierter Datei luacheck/scopecheck/localcount ok; luacheck_pz 0 Treffer + 3 erlaubt; die 28 Text-Dateien der Probe Round-Trip ok (`probe_b1c_nach_ausgabe.txt`) |
| `staging_dateien.txt` neu | **49 Dateien: 7 neu, 25 ueberschreibt, 17 gleich** (gegen NCBearTest, Stand 11.11. 01:19); MD5/Bytes gegen die Platte 0 Abweichungen; durch die Nachbesserung geaendert 9 Lua: Options, Map, Guard, Heal, Registry, Ride, Server, World, shared/BanditsNPCBear |

## 3. Fragen fuer Kevin (je mit Empfehlung; Kevin schlaeft -- nichts davon haelt den Einbau auf)
1. **A3 Regel-Auslegung:** Duerfen Vanilla-Lua-Bausteine, deren ganzer Code gelesen ist, die aber nirgends aufgerufen werden
   (`addTickBox`, `addSlider` der Optionen-Seite), als Beleg zaehlen? Empfehlung: ja, als Regel-Auslegung festhalten. Testpunkt: Haken und
   Schieber erscheinen, der Wert ueberlebt einen Neustart.
2. **A5:** Der Karten-Aufsatz ist jetzt in eigener Form (nur die Lehre aus NPC Crew). Nichts zu tun -- nur zur Kenntnis.
3. **B1 Mehrspieler:** nach einem Server-Absturz gewinnt im Mehrspieler das (aeltere) Register, auch wenn das Tier einen neueren Stand traegt
   (sonst koennte ein veraenderter Client Zaehmung vortaeuschen). Im Einzelspieler gewinnt der neuere Stand. Ok? Empfehlung: ja.
4. **A1 Grenze:** im Mehrspieler bleibt ein Junges mit einem Spiegel, der nie herstellbar ist (sehr alter B1a/B1b-Spiegel "tame", Besitzer
   unbekannt), unberuehrbar stehen statt ein wildes Junges zu werden. Soll es nach einer Frist wieder wild werden? Empfehlung: so lassen
   (der Fall braucht einen B1a/B1b-Mehrspieler-Spielstand, den es nicht gibt).
5. **B6:** "Q holt es heran" klappt beim Folgen; ein BLEIBENDES Junges kommt im Einzelspieler auf Q nicht (die Ersatz-Antwort haelt es).
   Soll Q auch beim Bleiben holen? Empfehlung: erst im Test ansehen.
6. **B7:** steht ein Zombie zwischen dir und deinem Jungen (du weiter als 10 Kacheln), rennt es erst weg und kommt dann zurueck. Lieber
   stehen bleiben, bis der Zombie weg ist? Empfehlung: ja, zusammen mit B5a (Zombies greifen an).
7. **FR-Text (A7):** "Nourriture : prêt" / "Caresses : prêt" passt im Geschlecht nicht (richtig "prête"/"prêtes"; ein Schluessel fuer
   beide Zeilen). Vorschlag: "Caresse : %1" (Einzahl wie ES) + "prête". Plan 1.10 sagte "nur ES" -- deshalb nicht geaendert. Empfehlung:
   aendern.
8. **ENT-Anmerkung (A6.4, nur Hinweis):** `baer/begleiter/ENTSCHEIDUNGEN.md:282` nennt `ISMilkAnimal.lua:138` und `ZAMove.lua:31`; die
   Aufrufe stehen bei `:139` bzw. `:32`. Der Code zitiert richtig; das Dokument ist Kevins, ich habe es nicht geaendert.

## 4. Fuer den Gegenpruefer
- Neue Engine-Aufrufe NUR in `B.SpotNear`: `sq:getRoom()` (`V:shared/Util/AdjacentFreeTileFinder.lua:240`, Vergleich zweier Raeume mit `==`
  wie dort; am Server auch `V:server/Farming/SFarmingSystem.lua:162`) und `cur:isBlockedTo(nxt)` mit Nachbarkachel
  (`V:shared/TimedActions/ISDropWorldItemAction.lua:7`, `V:shared/Foraging/ISForageAction.lua:7`). `getX/getY` an Kachel und Tier wie bisher.
- Bewusst nicht gebaut: B7 (Kevins Wort), B10 Teil 2 (Kosten/A3), FR-Text (Plan 1.10), "away" beim Bleiben (Schleifen-Schutz).
- `B.TakeNewerMark` laeuft im Mehrspieler nie bis zur Uebernahme (Zeile 1 der Funktion); die B3-Umbindung in Heil-Regel 1a ebenso nur SP.
- `table.sort` mit Vergleichsfunktion (Lua-Bibliothek; Vanilla `shared/NPCs/MainCreationMethods.lua:127`): strenge Ordnung mit
  Listenplatz als letztem Kriterium (Kahlua-`sort` wirft sonst bei inkonsistentem Vergleich).
- Absichtlich geaenderte Pruefer-Erwartung: `b1c_ober/texte_pruefen_b1c.py` (Karten-Aufsatz in der Form `hook`); sonst nur neue Faelle.

## 5. Offen / ungeprueft (zusaetzlich zu bau_b1c_zusammenbau.md 7 und pruef_b1c_*.md 5)
- Ob Zellen beim Entladen vor dem naechsten Speichern geschrieben werden (macht B1 haeufig oder selten) -- Annahme.
- Ob `isBlockedTo` niedrige Zaeune und Ecken erfasst; ob `getRoom`/`isBlockedTo` am MP-Server dasselbe liefern (Belege sind `shared/`).
- "away": echte Umwege beim Folgen (wie oft eine Ersatz-Antwort ohne Laerm kommt) -- `NCBear_CubCalm()` zeigt `why`.
- A3 aus B1a weiter offen (`getObjectListForLua`/`getAnimalID` am Server; B9 ruft den Suchlauf jetzt auch aus "Call to me").

Statisch geprueft, nicht gespielt. Nach einem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).
