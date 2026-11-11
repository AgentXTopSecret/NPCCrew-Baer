# Lauf baer-b1e: NACHBESSERUNG (11.11.2026 abends)

**Statisch geprueft, nicht gespielt.** Grundlage: `pruef_b1e_a.md` (A1-A6) und `pruef_b1e_b.md` (B1-B7). Jeden Befund selbst am Code
nachgeprueft (Staging gelesen, Vanilla-Stellen nachgelesen, Jar-Auszug `dec/IsoGridSquare.java`, eigene Attrappe gegen den Stand VOR und NACH
der Nachbesserung). Geschrieben nur: Staging `mod/` (8 Lua-Dateien), `attrappe/nach_b1e/run.lua` + `ergebnis.txt` (neu),
`attrappe/pruef_b1e/run_nach.lua` + `ergebnis_nach.txt` (neu), `attrappe/b1e_kern/run.lua` (ein Pruefungsname), `attrappe/gesamt/xref_b1e.txt`,
`PLAN_B1E.md` (1.1 d, 1.5, 2.5, 5, neu 13), `schnittstelle_aenderungen.md` (Abschnitt "B1e NACHBESSERUNG"), `staging_dateien.txt`, die Probe
unter `probe_b1e/` und die Ausgaben `trockenlauf_b1e_nach.txt`, `trockenlauf_b1e_nach_vor_b5a.txt`, `probe_b1e_nach_ausgabe.txt`.
Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits. Kein git, kein Spielstart, kein Download.
Kurzformen: `S:` Staging `mod/42/media/lua/`, `V:` Vanilla `media/lua/`.

## 0. Ergebnis je Befund

| ID | Urteil | Was getan |
|---|---|---|
| A1 | **bestaetigt** (`S:client/BanditsNPCBearMenu.lua` `holdWanted` / `addHold` mit `U.T("UI_BN_Bear_Menu_Hold")`) | **nicht geaendert**: 4 neue Schluessel x 7 Sprachen + 5 Text-Pruefer mit festen Schluessellisten; beide Pruefer schlagen "naechster Lauf mit Z1" vor -> **Frage 1** |
| A2 | **bestaetigt** (Vorbild nur `V:shared/TimedActions/Animals/ISPetAnimal.lua:17` in `update()`) | `faceThisObject` am neuen Koerper nur noch bei `B.IsSP()` (`S:server/BanditsNPCBearGrow.lua` B.BodySwap); im MP behaelt der neue Koerper die Richtung aus `addAnimal` (offen, nur Optik) -> **Frage 4** |
| A3 | **bestaetigt** | `S:server/BanditsNPCBearGuard.lua` B.GuardStep: `local bd, bsz = B.BodyNow(rec); gap = B.BodyGap(bd, bsz)` (Kopf-Kommentar ebenso) |
| A4 | **bestaetigt** (= B3) | Kommentar `S:shared/BanditsNPCBearStats.lua` B.BodyGap: "Tag 45: ~0,21" |
| A5 | **bestaetigt als ungeprueft** (kein Texturen-Lader in den Jar-Auszuegen) | nicht geaendert; Testpunkt -> **Frage 5** |
| A6 | **bestaetigt** | Kommentar ueber `B.BodySwap`: `square:getX()/getY()/getZ()`: `V:client/DebugUIs/DebugContextMenu.lua:636` |
| B1 | **bestaetigt** (Attrappe P1b; `S:server/BanditsNPCBearRide.lua` B.HandleCall `old = B.FindAnimal(rec)` -> nil im selben Bild) | **gebaut** wie vorgeschlagen: `B.PlaceCub` merkt `s.placedAt`; `B.HandleCall` tut nichts (still, eine Diagnose-Zeile), solange der Koerper der Sitzung juenger als `callFreshMs` (2000) ist UND `B.FindAnimal` ihn nicht findet. Kein neuer Engine-Aufruf |
| B2 | **bestaetigt** (`B.BodySwapReady` ohne `ownUntil`; `clearBodySession` Ride.lua:56) | **gebaut**: neuer Grund "move" (eigener Rennbefehl laeuft), hoechstens `swapMoveMaxMs` (10000) seit dem ersten Takt mit want ~= have (`s.swapWantAt`, setzt `B.GrowLive`) -> **Frage 2** |
| B3 | **bestaetigt** (0,2099; 0,3784 / 0,9 x 1,6 = 0,673) | Kommentare Stats.lua (0,21) und `S:shared/BanditsNPCBear.lua` (`x MotionScale 1,6`), `PLAN_B1E.md` 1.5 Nr. 1 und 3, Tabelle 2.5; Pruefungsname in `attrappe/b1e_kern/run.lua` |
| B4 | **bestaetigt** (`V:shared/Definitions/animal/CowDefinitions.lua:245`, `DeerDefinitions.lua:137`/`:181`; Knoten `media/AnimSets/player/actions/AnimalLureHigh.xml`) | `ncbeargrown.feedByHandAnim = "AnimalLureHigh"` (`S:shared/BanditsNPCBearDefs.lua`), Junges bleibt "AnimalLureLow" -> **Frage 3** |
| B5 | **teils bestaetigt** | Laerm-Ersatzweg (`B.CalmAnswer`, = Z2): **gebaut** `followStart + gap` / `followGap + gap` wie `B.FollowDecide`. Heranlocken mit Futter (Regel 6, `comeFed`): **abgelehnt** -- siehe 1.4 |
| B6 | **bestaetigt** (`S:server/BanditsNPCBearRegistry.lua` B.Close `Note_Dead`/`Why_Gone`, `S:server/BanditsNPCBearServer.lua` handCheck `Why_Gone`) | wie A1 nicht geaendert -> **Frage 1** |
| B7 | **bestaetigt** (`V:client/ISUI/ISUIElement.lua:1998`, `:1004`) | nicht geaendert (Bandits' Element tat dasselbe, der Doppelklick braucht es) -> **Frage 6** |

**Kein Befund falsch.** Neue Engine-Aufrufe: **keiner** (`getTimestampMs` in Ride.lua belegt im Datei-Kopf `V:server/Foraging/forageServer.lua:456`;
`B.IsSP`, `B.FindAnimal`, `B.BodyNow`, `B.BodyGap` sind eigener Code). Kein neuer `pcall`, kein neuer Text (alle 21 JSON byte-gleich), kein Befehl,
kein Menue, keine NCBear*-Datei ausser der Bench beruehrt (die Bench gar nicht).

## 1. Einzelheiten

### 1.1 B1 -- "Call to me" im selben Bild wie ein Tausch
- `B.PlaceCub` (Ride.lua): nach `clearBodySession(s)` jetzt `s.placedAt = getTimestampMs()` -- gilt fuer Tausch, Aussteigen und Call.
- `B.HandleCall`: VOR der Drossel "ok" (sonst verbraucht eine wartende Bitte die Drossel): Sitzung hat ein Objekt, `placedAt` ist juenger als
  `B.CFG.callFreshMs` (2000) und `B.FindAnimal(rec) == nil` -> `B.Log("call: b1 got its body N ms ago, not in the world yet -- nothing done")`,
  sonst nichts (keine Meldung, keine Abklingzeit, keine Sicht). Sobald der Koerper im naechsten Bild in der Welt ist, findet `B.FindAnimal` ihn
  und Call laeuft wie bisher (alter Koerper weg, neuer neben dem Spieler).
- Bewusst NICHT "Objekt nicht in der Welt -> ablehnen" (Pruefer B): nach `callFreshMs` greift die Sperre nie, ein Baer in einer entladenen
  Gegend bleibt herholbar (Attrappe N1c).
- Wirkung: das Ein-Bild-Fenster (seit B1c auch Aussteigen + Call) erzeugt keinen dritten Koerper mehr. Der Klick in genau diesem Bild bleibt
  ohne Antwort -- ein zweiter Klick geht.

### 1.2 B2 -- kein Tausch mitten im Rennen (hoechstens 10 s warten)
- `B.BodySwapReady` (Grow.lua), nach "busy": `s.walk == false` und `pending(s.ownUntil, ms, ownMaxMs)` und `within(s.swapWantAt, ms,
  swapMoveMaxMs)` -> `false, "move"`. Die Funktion liest weiter nur (die Bench fragt dort, Attrappe N2a "schreibt nichts").
- `B.GrowLive`: want ~= have -> `s.swapWantAt = ms`, wenn leer; want == have -> `s.swapWantAt = nil`. `B.BodySwap` leert es nach dem Tausch.
- Grenzen: Gehen sperrt nicht (`s.walk == true`); ohne `swapWantAt` keine Sperre; Uhr rueckwaerts (`swapWantAt` in der Zukunft, `ownUntil`
  weiter als `ownMaxMs` voraus) keine Sperre. Hoechstwartezeit gilt ab dem ERSTEN Takt mit want ~= have, nicht je Rennstrecke -> nie endlos.
- Attrappe N2f (ganzer Hirn-Takt, Besitzer rennt davon, 11 von 12 Takten mit Rennbefehl): Tausch nach 12000 ms (= erster Wunsch bei 1500 +
  10000 + ein Takt), nie zwei Koerper. Die Bench (`NCBear_CubGrow`) zeigt dann "swap waits: move".

### 1.3 A2 -- faceThisObject nur im Einzelspieler
`if fd > 0 and rec.owner ~= nil and B.IsSP() then` (`B.IsSP` = `not isClient() and not isServer()`, `S:shared/BanditsNPCBear.lua:195`). Der
Aufruf steht weiter NACH `B.RemoveCub`. Attrappe N3: MP-Server 0 Aufrufe, SP 1 Aufruf; `b1e_kern` 4/21 und Gesamt 20b unveraendert gruen.

### 1.4 B5 -- Abstaende mit Koerperlaenge
- **Gebaut (Laerm-Ersatzweg, Z2):** in `B.CalmAnswer` `gap` aus `B.BodyNow`/`B.BodyGap` (in Locals), `> cfg.followStart + gap` und
  `toward(..., cfg.followGap + gap)` -- dieselben Zahlen wie `B.FollowDecide` (`S:shared/BanditsNPCBearRules.lua` Regel 14/16). Beim Jungen 0.
  Attrappe N4: gross 1,35 rennt auf followGap + 0,498 (Kachel 103 statt 102); 4,8 Kacheln weg (< 4,5 + 0,498) kein Rennen mehr; Junges wie B1c.
- **Abgelehnt (Heranlocken, Regel 6 `comeFed`):** Fuettern verlangt `here:DistTo(there) < reach` (3; `S:server/BanditsNPCBearServer.lua`
  handCheck, Vorbild `V:shared/TimedActions/Animals/ISPetAnimal.lua:6`). `DistTo(IsoGridSquare)` ist laut Jar der **Manhattan-Abstand** der
  Kachelmitten (NUR JAR `dec/IsoGridSquare.java:1165-1166`). Schon bei 2,0 Kacheln Mitte zu Mitte kann das schraeg 3 ergeben; mit + 0,5
  (Tag 100) stuende der Baer bis 2,5 weg und "You are too far away." kaeme oefter. Kein Durchdringen ohne Zuschlag (Nase ~0,9 Kacheln vor der
  Figur, Pruefer B). Bleibt "im Spiel ansehen".

### 1.5 B4, A3, A4/B3, A6
- B4: eine Datenzeile in der Kopie der Definition (`d.feedByHandAnim = "AnimalLureHigh"`), Kommentar in der Fuetter-Aktion angepasst. Attrappe N5.
- A3: reine Form, gleiche Werte (alle Attrappen byte-gleich). Attrappe N6 sucht `BodyGap(B.BodyNow(` im Code: 0.
- A4/B3: nur Kommentare und Plan-Text; der Code hatte die richtigen Zahlen (Pruefung `b1e_kern` 3 rechnet 0,209).
- A6: nur Kommentar.

### 1.6 Nicht geaendert, mit Grund
- **A1/B6** (Texte "cub" beim grossen Baeren: `Why_Gone`, `Note_Dead`, `Menu_Hold`, `Menu_HoldTip`): Text-Arbeit in 7 Sprachen (CN nur
  Vanilla-Zeichen) plus feste Schluessellisten in `attrappe/ober/texte_pruefen.py`, `b1b_ober/texte_pruefen_b1b.py`,
  `b1e_ober/texte_pruefen_b1e.py`, `ober_werkzeug/texte_b1e.py` (Byte-Vergleich `--tmp`) -- kein kleiner Eingriff in einer Nachbesserung; beide
  Pruefer empfehlen den naechsten Lauf. Weg dann: `B.NoteBd` an B.Close (Note_Dead, Why_Gone), `bd` aus `B.BodyKind(animal)` an handCheck,
  `holdWanted` meldet "alle nahen Baeren gross" -> `U.TB`.
- **A5** (288-px-Bilder gegen "Max. Texturgroesse 256"): ob UI-Bilder gedeckelt werden, ist in keinem Jar-Auszug belegt. Betroffen nur der Pfeil
  bei 300 % (Kreis/Symbol gehen ueber `drawTextureScaled`); Auto bei 2054 px nimmt `arrow192`.
- **B7** (Klickflaeche 45 x f px oben Mitte, hoechstens ~60 s): wie Bandits; der Doppelklick zum Ausblenden braucht die Maus-Ereignisse.

## 2. Pruefungen nach der Nachbesserung (alle selbst gelaufen)

| Pruefung | Ergebnis |
|---|---|
| Vier Lua-Pruefer, 25 Lua-Dateien | luacheck 0 failed; scopecheck 0; localcount hoechstens 49 aktiv (Hud :1) / 77 insgesamt (World :664) -- unveraendert; luacheck_pz 18 x W113 = die bekannten (15 Bench, 3 Aktionsklassen Menu.lua) |
| luac5.1 -p | alle 25 ohne Fehler |
| Form | Lua: LF, reines ASCII; 21 JSON: Round-Trip, kein BOM/CR, **byte-gleich mit vor der Nachbesserung** |
| Attrappen (byte-gleich mit dem gespeicherten Stand) | kern 136/0, b1b_kern 204/0, b1c_kern 192/0 (`ergebnis_b1e.txt`), b1d_kern 162/0 (`ergebnis_b1e.txt`), b1e_kern 153/0, **gesamt 1672/0** (`ergebnis.txt`), pruef_b, pruef_b1b `run_nach`, pruef_b1c, pruef_b1d (je `ergebnis_*nach*`) |
| OBERFLAECHE (Kern-Attrappe / echter Kern) | ober 116/117, b1b_ober 144/134, b1c_ober 155/142, b1d_ober 174/176, b1e_ober 218/218 -- je 0 Fehler |
| **neu `attrappe/nach_b1e/run.lua`** | **31 bestanden, 0 Fehler**; gegen eine Kopie des Stagings VOR der Nachbesserung: 12 / **19 Fehler** (jeder Fall N1-N6 rot) |
| `attrappe/pruef_b1e/run.lua` (Pruefer Bs Beleg) | jetzt 20 / 5: die fuenf P1b-"BEFUND"-Pruefungen schlagen fehl, weil der Befund weg ist (1 Koerper, addAnimal 1); P2/P3 unveraendert |
| **neu `attrappe/pruef_b1e/run_nach.lua`** | **25 / 0** (P1b erwartet den behobenen Stand: 1 Koerper, danach Call normal); P3 weiter 7 Tausche, laengste Wartezeit 2 Takte |
| `xref_b1e.py` | **0 Luecken**, 3 Hinweise (bekannt); 180 CFG-Felder (+2), 91 Rueckfall-Stellen (+3), nur Zeilennummern sonst -> `xref_b1e.txt` neu |
| `gegenprobe_b1e.py` / `probe_regeln_b1e.py` | 30 von 30 / 8 von 8, Ausgabe byte-gleich |
| Text-, Bild-, Beleg-Pruefer | `texte_pruefen*.py` (ober, b1b, b1c, b1d) 0, `texte_pruefen_b1e.py --tmp` 0, `bilder_pruefen_b1e.py --tmp` 0 (ohne `-I`, numpy); `belege.py` 0/112, `_b1b` 0/51, `_b1c` 0/89, `_b1d` 0/23, `_b1e` 0/53 |
| Trockenlauf `--staging mod --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen**; gegen vorher nur Codezeilen 7152 -> 7179 und Zeilennummern der Tier-Regeln |
| Trockenlauf ohne `--vor-b5a` | **26 Fehler = 24 Altlasten + 2 `ALT_DEFS`** ("Erwartet rot ... sonst nichts"), sonst wie oben |
| Probe `--probe probe_b1e --staging mod --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen**, 60 Dateien; Pruefer je kopierter Datei gruen (Guard.lua localcount hoechstens 32); Gesamt-Attrappe gegen die Probe **1672/0, byte-gleich** `ergebnis_probe.txt` |
| `staging_dateien.txt` neu | **60 Dateien: 9 neu, 35 ueberschreibt, 16 gleich** (gegen NCBearTest); in der Nachbesserung geaendert 8 Lua-Dateien (Grow, Guard, Registry, Ride, BanditsNPCBear, Defs, Stats, FeedAction) |

## 3. Neue Zahlen (Stellwerte)
| Feld | Wert | Wofuer |
|---|---|---|
| `swapMoveMaxMs` | 10000 | Rennbefehl sperrt den Tausch hoechstens so lange (B2) |
| `callFreshMs` | 2000 | "Call to me" wartet hoechstens so lange auf einen eben erzeugten Koerper (B1) |
| `ncbeargrown.feedByHandAnim` | "AnimalLureHigh" | Fuetter-Haltung am grossen Koerper (B4) |
| Abstand-Zuschlag `gap` | Tag 15 0,00 / Tag 45 **0,21** / Tag 100 0,50 | jetzt auch Laerm-Ersatzweg "follow" (B5) |
| Tempo gross | 0,673 / 3,173 Kacheln/s = Clip-Weg / Dauer x MotionScale 1,6 | unveraendert, nur Text berichtigt (B3) |

## 4. Fragen fuer Kevin (er testet gerade -- nichts davon haelt den Einbau auf)
1. **A1/B6:** Sollen auch "The cub is gone.", "The bear cub is dead." und das Welt-Menue "Hold out food for the cub" beim grossen Baeren
   "bear" sagen? Empfehlung: ja, im naechsten Lauf (4 Texte x 7 Sprachen).
2. **B2:** Der Wechsel wartet jetzt, solange der Baer hinter dir herrennt -- hoechstens 10 Sekunden, dann wechselt er doch. Ok? (So gebaut.)
3. **B4:** Beim Fuettern des grossen Baeren haelt die Figur das Futter hoch (wie bei Kuh/Hirsch) statt sich zu buecken. Bitte ansehen.
4. **A2:** Im Mehrspieler schaut der neue Baer nach dem Wechsel nicht mehr extra zu dir (dafuer gibt es am Server kein Vorbild). Ok?
5. **A5:** Markierung einmal auf 300 % stellen: ist der Pfeil gleich gross wie der Kreis? (Sonst Stufe 300 % streichen.)
6. **B7:** Stoert es, dass ein Klick oben in der Mitte waehrend der Markierung (bis ~1 Minute) nicht in die Welt geht?
7. (Pruefer B 5) Beim Wechsel springt der Baer auf die Kachelmitte (unter 1 Kachel) -- ok?

## 5. Ungeprueft
Alles Laufzeit-Verhalten: Wartezeit "move" im echten Spiel (ob `s.walk`/`ownUntil` das Rennen treffen), das Ein-Bild-Fenster bei Call,
Fuetter-Haltung "AnimalLureHigh" am Baeren, Richtung des neuen Koerpers im MP, Klickflaeche und 288er Bilder der Markierung. Nach dem Einbau
(erst wenn Kevins Spiel zu ist) muss das Spiel neu gestartet werden. Statisch geprueft, nicht gespielt.
