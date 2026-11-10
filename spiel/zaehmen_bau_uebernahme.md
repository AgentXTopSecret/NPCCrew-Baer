# Lauf baer-zaehmen (B1a): ZUSAMMENBAU und Uebernahme-Skript -- Bericht

Stand 10.11.2026 abends. **Statisch geprueft, nicht gespielt.** Nichts in die Test-Mod, nichts nach NPC Crew, nichts committet,
kein `--echt`. Geschrieben nur unter `_arbeit/baer_zaehmen/` sowie (laut Auftrag) `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md`.

## 1. Zusammenbau: passen KERN und OBERFLAECHE zusammen?

Werkzeug: `attrappe/gesamt/xref.py` (Ausgabe `attrappe/gesamt/xref.txt`) sucht in allen 15 Lua-Dateien jede `B.<Name>`-Benutzung, jede
Definition, jeden Textschluessel, jeden Befehl; dazu von Hand gelesen: `client/BanditsNPCBearClient.lua`, `BanditsNPCBearMenu.lua`,
`ISUI/BanditsNPCBearHud.lua`, die drei Zeitaktionen, `shared/BanditsNPCBear.lua`, `BanditsNPCBearFood.lua`, `BanditsNPCBearDefs.lua`,
`BanditsNPCBearCrew.lua`, `server/BanditsNPCBearRegistry.lua`, `server/BanditsNPCBearServer.lua` ganz, `BanditsNPCBearWorld.lua` bis :290.

**Ergebnis: keine Luecke.** Kein `B.*` wird benutzt, das nirgends definiert ist; kein Textschluessel fehlt in EN; jeder EN-Schluessel
wird benutzt; jeder Befehl hat seinen Empfaenger.

### 1.1 Funktionen und Felder ueber die Grenze (Spalte "von": wer ruft)

| Name | definiert (Seite, Datei) | benutzt von | Form passt |
|---|---|---|---|
| `B.ACT` | K `shared/BanditsNPCBear.lua:29` | FeedAction :59, :68 | ja ("eat" hat Knoten `NCBear_Eat.xml`) |
| `B.CFG` (feedTime, petTime, baitTime, petAnim, barZ, hudDist, hudMax, menuFoods, baitEdge) | K `BanditsNPCBear.lua:32-62` | Menue, Hud, drei Aktionen, Bench | ja, alle Felder da |
| `B.CUB`, `B.CMD` | K `:24`, `:23` | Menue, Hud, Client, Bench | ja |
| `B.T(key, fallback, a1..a3)` | K `:236` | Client `U.T` :111, Menue, Hud | ja |
| `B.WaitParts(h)` -> n, unitKey | K `:266` | Client `U.WaitText` :116 | ja |
| `B.View` / `B.ApplySync` / `B.ViewOf` | K `:336`, `:353`, `:387` | Client :255, Menue :186, Hud :112 | ja (Form 6.2.5) |
| `B.OnView()` | O `ISUI/BanditsNPCBearHud.lua:351` | K `ApplySync` :379 (wahlfrei) | ja |
| `B.ShowNote(player, note)` | O `client/BanditsNPCBearClient.lua:163` | K `B.Tell` :433 (nur SP) | ja; Note-Felder k/t/v/tone gleich (Server `note()` :30, Client `U.NoteText` :137) |
| `B.Ask(player, cmd, args)` | K `:412` | Client "Hello" :210, Menue "BaitDrop" :109 | ja; Server `B.Handle` kennt genau Hello/BaitDrop (`BanditsNPCBearServer.lua:354`, `:358`) |
| `B.CheckFeed/CheckPet(rec, pkey, slots, now)` | K `BanditsNPCBearRules.lua:141`, `:160` | Menue :128, :162 (mit Sicht-Eintrag + `B.View.me`) | ja |
| `B.CheckBait(slots[, now])` | K Rules | Menue :261 ohne `now` | ja (KERN Eintrag 1, Punkt 1) |
| `B.WaitLeft(rec, kind, now)` | K Rules :120 | Hud :120, Bench | ja |
| `B.FoodList(player, max)` -> {item, class, name, count} | K `BanditsNPCBearFood.lua:76` | Menue :134, :227 | ja |
| `B.IsBaitFood(item)` -> ok, kind | K Food :64 | Menue :231, :319 | ja |
| `B.NearForest`, `B.Opt`, `B.Now`, `B.PlayerKey` | K | Menue, Hud, Bench | ja |
| `B.FeedComplete/PetComplete/BaitComplete` | K `server/BanditsNPCBearServer.lua:201`, `:242`, `:291` | drei Aktionen `complete()` (ueber `BanditsNPC.Bear.X`, nil auf MP-Client) | ja, Parameter wie Plan 6.2.7 |
| `B.UI.*` | O (Client, Menue, Hud) | nur O und Bench | KERN belegt `B.UI` nicht |
| Bench: `AppearFor`, `BaitDawn`, `BrainTick`, `SlowTick`, `Close`, `Commit`, `FindAnimal`, `NearestRec`, `PushView`, `Reg`, `RemoveCub`, `SlotsOf`, `SquareFits`, `TameCheck`, `Touch`, `OPTS`, `IsSP` | K | `client/NCBearBenchCub.lua` (nur SP, wird nie kopiert) | ja |

Doppelt "definiert" laut Querverweis, alle gewollt: `B.LogOn` (Kern-Vorgabe, Bench setzt), `B.UI` (je O-Datei `B.UI = B.UI or {}`),
`B._dirty` (Registry legt an, Server setzt nach dem Verschicken neu).

### 1.2 Befehle, Sicht, Texte

| Was | Seite A | Seite B | passt |
|---|---|---|---|
| Hello (Client -> Schreiber) | Client `sendHello` :210 | Server `B.Handle` :354 -> `B.PushView` | ja (Attrappe 2 und 15) |
| BaitDrop `{ id }` | Menue :109 | Server :358, prueft `bait.owner == Benutzername` | ja (Attrappe 11, 15: fremder Spieler kann nicht aufgeben) |
| Sync (payload 6.2.5) | Registry `B.BuildView` :406 | Client :254 -> `B.ApplySync` | ja; me = `B.SlotsOf`-Form, cubs mit oid |
| Note `{k,t,v,tone}` | Server `note()`/`tellWhy` (t nur bei wait/days), Registry `tellKey` | Client :256 -> `B.ShowNote` | ja |
| Textschluessel | 66 als Text in den 14 kopierten Lua-Dateien, 74 Ersatztexte (`U.EN`) | EN/UI.json 74, je Sprache 74 | ja; Ersatztexte `U.EN` wortgleich (Skript prueft) |
| Kurzform `KEY_HEAD .. "Dir_" .. v` | Client :149 | `UI_BN_Bear_Dir_N..NW` in UI.json | ja |

### 1.3 Behobene Luecken

**Im Code: keine.** Keine Datei der Bauer wurde geaendert. Was der gemeinsame Attrappen-Lauf zuerst rot zeigte, lag an der Attrappe
selbst und ist dort behoben (Code unveraendert):
- Basisklasse der Zeitaktion ohne `waitToStart`/`update` in der Attrappe (Vanilla hat beide) -> Attrappe ergaenzt.
- "entdeckt" mit 1,6 s Takt: ohne lebende Eintraege drosselt der Hirn-Takt auf 10 s (`B.CFG.idleMs`, gewollt) -> Attrappe tickt 11 s.
- "Tamed!" blinkt (450 von 700 ms an, Hud :297) -> Attrappe sieht bis zu vier Bilder an.
- Koeder-Morgen: der Wald-Wurf im selben Langsam-Takt nahm den festen Wurf 0 vorher -> Wald-Wurf in diesem Abschnitt aus.
- MP-Hello: kommt eine Sync schon vor dem ersten Hello an, fragt der Client richtigerweise nicht mehr -> Hello vor dem Wald-Wurf getestet.
- MP-Koeder: ein gebundener Spieler darf keinen Koeder legen (Regel) -> Koeder mit dem zweiten Spieler, der erste wird als Ablehnung getestet.

## 2. Pruefer (alle 15 neuen Lua-Dateien, Staging)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` | 15 file(s) checked, 0 failed |
| `scopecheck.py` | 15 file(s), 0 violation(s) |
| `luacheck_pz.py` | 11 x W113: 3 Aktionsklassen in `BanditsNPCBearMenu.lua:81/92/102` (setzt `shared/TimedActions/*`), 8 in der Bench (`NCBear_Cub*`, `NCBearMenu` der Test-Mod) -- alle erwartet; in der Probe 0 Treffer + 3 erlaubt |
| `localcount.py` | hoechstens 41 je Funktion (alle 15 Dateien); Grenze 200, Warnschwelle 180 |
| Zeilenenden / Kodierung | 15 Lua, `sandbox-options.txt`, `nc_bear_cub.txt`: LF, reines ASCII, kein BOM (Skript `form_check`) |
| JSON-Round-Trip | 21 Dateien (7 x UI/Sandbox/IG_UI) der Quelle: `json.dumps(indent=4, ensure_ascii=False)+"\n"` == Datei, UTF-8 ohne BOM, LF, sortiert; ebenso die 21 zusammengefuehrten Dateien in der Probe |
| CN-Zeichen | alle in Vanilla-CN (Skript `plan_texts`) |
| Gesamt-Attrappe | `attrappe/gesamt/run.lua`: **175 bestanden, 0 Fehler**, keine Fehlerzeile des Codes (`attrappe/gesamt/ergebnis.txt`); derselbe Lauf gegen die in die Probe kopierten Dateien: 175/0 (`ergebnis_probe.txt`) |

### 2.1 Gesamt-Attrappe (ein Junges durch den ganzen Ablauf)

Laedt wie das Spiel shared -> client -> server (alle 15 Dateien, echte Kern-, Oberflaechen- und Bench-Datei), Engine-Attrappen aus
`attrappe/kern/attrappen.lua`, UI-Attrappen (Menue, Zeitaktion, Panel, HaloText) in `run.lua`. Texte kommen absichtlich aus den
englischen Ersatztexten (`getTextOrNull` = nil), damit die Meldungen als Saetze geprueft werden. Abschnitte:
1. Laden SP mit NPC Crew: Naht 1 gesetzt, drei globale Aktionsklassen, Art `ncbearcub`, ein Balken-Element.
2. Hello -> Sicht (SP direkt), `B.UI.Fresh()`.
3. Wald-Wurf -> `new`, Hinweis "...whimpering from the forest to the west.", Spiegel am Tier, `me.wild`.
4. Hingehen -> `shy`, "A bear cub! It looks lost and hungry."
5. Menue am scheuen Jungen: Vanillas "Kill" entfernt, "Feed" frei mit Untermenue (Honig zuerst "Base.Honey - loves it (2)"), "Pet" grau
   mit "It is still too shy...".
6. Fuettern als Zeitaktion ueber das Menue: genau ein Stueck weg, `sendRemoveItemFromContainer` einmal, `fed`, bond `__sp`, 21 Punkte,
   "+21 trust - it loves this!", Sperre und Fress-Variable nach der Aktion geloest, Sicht nachgezogen, Balken "Taming 21%", "Food: 2 h",
   "Petting: ready".
7. Fuettern grau "It is still full. Try again in about 2 h.", Streicheln +12 (Mischung) -> 33, `petAnimal` einmal.
8. F/P/F bis gezaehmt: 64,5 -> 76,5 -> Fisch -> `tame`, Besitzer, 100, "The cub trusts you...", `me.bears = 1`, "Tamed!" blinkt, nach 5 s kein Balken.
9. Ein Baer je Spieler (`Why_HasBear`); zahmes Junges bleibt streichelbar, "It enjoys that.", kein Zuwachs.
10. Tod -> Eintrag zu, "Your bear is dead... 7 day(s)...", Sperre in der Sicht, `MayAppear` lehnt mit 7 Tagen ab, nach 7 Tagen geraeumt.
11. Koeder ueber das Welt-Menue: nur Honig angeboten, ein Stueck weg, "Bait laid out...", Schild "Bear bait (honey)" / "night 0 of up to 3";
    "Give up bait spot" -> "Bait spot given up.", Sicht und Register ohne Koeder.
12. Koeder -> Nacht -> Morgen (Spieler 100 Kacheln weg) -> reif -> Junges am Koeder, Heimat = Platz, "A bear cub has found your bait!", Koeder verbraucht.
13. Ungefuettert, ohne Kontakt: nach 36 h faellig, belegt keinen Platz, verschwindet ohne Spieler in 25 Kacheln, "The bear cub has wandered off."
14. Ohne NPC Crew geladen: laeuft, keine Fehlerzeile.
15. MP-Rundlauf (Server-Modus; Client durch Umschalten von `isClient`): Hello per `sendClientCommand`, Server antwortet genau dem Fragenden
    mit Sync; Wald-Wurf schickt Note + Sync; Fuettern am Server mit dem Stueck des Servers; zweiter Spieler fremd gebunden -> abgelehnt,
    behaelt sein Stueck, bekommt `Why_Other` per `sendServerCommand`; Client-Menue graut "Feed" allein ueber die Sicht (OnlineID, ohne
    Spiegel am Client-Tier); gebundener Spieler darf keinen Koeder legen; fremder Spieler kann einen Koeder nicht aufgeben, der Besitzer schon.

Beweist Logik und Zusammenpassen, nicht Engine-Verhalten (Kahlua ist kein echtes 5.1; die Attrappen bilden Methoden so nach, wie wir sie
verstehen). Der MP-Teil laeuft in EINEM Lua-Zustand: echte Serialisierung von `sendServerCommand` ist nicht nachgebildet.

## 3. Staging vollstaendig

- Platzhalter kopiert: `mod/42/media/models_X/Skinned/NCBearCub.glb` MD5 `6c3f0a96ba9a2aaf3a06eabc184cdbc3` (1 226 188 Bytes),
  `mod/42/media/textures/Body/NCBearCub.png` MD5 `2ee25f24c4f0f05bfbb955d4d4b17aea` (1 303 826 Bytes) -- byte-gleich mit
  `_arbeit/baer_baby/entwurf/`. Das GLB: 1 Netz, 1 Haut, 26 Knochen, 15 Clips (dieselben Namen wie `NCBear.glb` des Erwachsenen).
  Das endgueltige Modell aus `baer-junges` ersetzt beide unter demselben Namen.
- Skript `mod/42/media/scripts/nc_bear_cub.txt`: `module Base`, `animationsMesh NCBearCub` (meshFile `Skinned/NCBearCub.glb`,
  keepMeshAnimations), `model NCBearCub_Body` (mesh `Skinned/NCBearCub.glb`, shader `animalEffect`, animationsMesh `NCBearCub`) --
  Form wie `NCBearTest scripts/nc_bear_tier.txt:3-15`; `bodyModel = "NCBearCub_Body"` in Defs :62 und die Rassen-Textur `NCBearCub`
  (Defs :44-46) finden ihre Dateien (Skript prueft).
- `mod_info_vorschlag.txt`: neuer Text fuer beide `mod.info` (Name/ID bleiben, B1a und die Testbefehle `NCBear_Cub*` genannt); `mod.info`
  selbst NICHT im Staging.
- `staging_dateien.txt`: **40 Dateien, 39 neu, 1 ueberschreibt**: `42/media/lua/shared/Translate/EN/IG_UI.json` (Plan 6.1 Nr. 19: die
  Datei gibt es in der Test-Mod schon; die 4 alten Schluessel stehen wortgleich darin, nachgeprueft, dazu sortiert die 2 neuen).
  Die Bench `client/NCBearBenchCub.lua` liegt im Staging (sie gehoert in die Test-Mod), wird aber nie nach NPC Crew kopiert.

## 4. Uebernahme-Skript `baer/tools/baer_uebernahme.py`

Aufbau nach `turret/tools/turret_uebernahme.py` (gelesen), angepasst: Quelle Test-Mod mit wahlfreiem `--staging` darueber; `--probe`
baut `<probe>/quelle` (Test-Mod ohne Git + Staging, byte-gleich nachgeprueft) und `<probe>/NPCCrew` (Lua, Skripte, AnimSets, Sandbox,
mod.info von NPC Crew); `--echt` nur mit `--ja-kevin-hat-es-gesagt`, verbietet `--staging` und `--vor-b5a`, prueft `tasklist`.
Neu gegenueber dem Turret: Altlasten-Liste (24, `ALT_EXPECTED`), Sandbox-Anhang mit Abgleich gegen `B.OPTS` und Sandbox-Texte,
`IG_UI.json` neu anlegen, Namensraum je Textdatei, Vanilla-Kollisionen (Dateien, Skriptnamen, Textschluessel, Lua), GLB-Clips gegen
Animations-Knoten und Vanillas buck, Knoten-Bedingung genau `NCBearAct`, Tier-Regel (Plan 12.1 Punkt 7), Ersatztexte gegen EN,
luacheck_pz mit einzeln erlaubten W113. Keine Naht-Zeilen-Maschine (der Baer setzt keine Zeile in NPC Crew).

**Gegenprobe der Cheat-Pruefung** (Kopie des Stagings im Scratchpad, absichtlich verdorben: globale `NCBear_CubHere2`, `addAnimal` im Menue,
Menuepunkt "Spawn cub here", `isDebugEnabled`, eine `NCBearBenchX.xml`, eine fremde `Foo.json`): 8 Fehler, alle gefunden; die
`NCBearBenchX.xml` wurde uebersprungen statt kopiert.

### 4.1 Trockenlauf (`python baer/tools/baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod`)

Volle Ausgabe: `_arbeit/baer_zaehmen/trockenlauf.txt`. Kurz:
- kopieren: 14 Lua, 13 Dateien (10 Animations-Knoten `NCBear_*.xml`, GLB, PNG, `nc_bear_cub.txt`), 2,6 MB; NICHT: `.git`, `.gitattributes`,
  `NCBearBench.lua`, `NCBearBenchCub.lua`, beide `mod.info`.
- Texte: IG_UI.json 3 neu (Datei neu), Sandbox.json 43 neu (92 -> 135), UI.json 74 neu (3801 -> 3875), je 7 Sprachen.
- Sandbox: 19 Optionen, NPC Crew vorher 42, LF.
- Kollisionen: 0 im Code von NPC Crew, 1 nur im Kommentar (NC `shared/BanditsNPC.lua:1356`, Changelog), 0 Vanilla-Dateien, 0 Skriptnamen,
  0 Baeren-Namen in Vanilla-Lua, v3.8.38 keine; 66 Textschluessel aus der Lua, alle in EN; 74 Ersatztexte wortgleich.
- Cheat-Pruefung: 14 Dateien, 3053 Codezeilen, 847 Texte, 46 Werkbank-Texte, 36 Werkbank-Funktionsnamen, **0 Funde**, 1 Ausnahme
  (`NCBearCub_Body`, Defs :62); Tier-Regel: `addAnimal` World :233 und `addToWorld` :238 (B.CreateCub), `B.CreateCub` Server :110
  (B.AppearFor), `B.AppearFor` Server :498 (forestRolls) und :737 (baitAppear), `:remove()` World :257 (B.RemoveCub).
- **ERGEBNIS: NICHT OK -- 24 Fehler, 3 Warnungen. "Erwartet rot: genau die 24 Altlasten aus ALT_EXPECTED, sonst nichts."**

Mit `--vor-b5a` (`trockenlauf_vor_b5a.txt`): **OK -- 0 Fehler, 27 Warnungen** (24 Altlasten + 3 unten).

### 4.2 Probe (`... --probe _arbeit/baer_zaehmen/probe --staging _arbeit/baer_zaehmen/mod --vor-b5a`)

Volle Ausgabe: `_arbeit/baer_zaehmen/probe_ausgabe.txt` (auch `probe/NPCCrew/bericht.txt`).
- geschrieben: **49 Dateien** nach `probe/NPCCrew` (14 Lua, 13 Dateien, 21 Texte, `sandbox-options.txt`), zurueckgelesen.
- Pruefer im Probe-Baum: alle 14 Lua luacheck/scopecheck ok, localcount hoechstens 41; luacheck_pz 0 Treffer, 3 erlaubt
  (`BanditsNPCBearMenu.lua:81/92/102`, die Aktionsklassen).
- Nachgezaehlt: `sandbox-options.txt` 61 Optionen (42 + 19), einmal `VERSION`, ASCII/LF; 21 Textdateien Round-Trip, sortiert, LF, ohne BOM.
- Gesamt-Attrappe gegen die Lua im Probe-Baum: 175/0.
- **ERGEBNIS: OK -- 0 Fehler, 27 Warnungen (PROBE).**

Die drei Warnungen ausser den Altlasten:
1. GLB des Jungen: 10 Clips aus Vanillas buck fehlen (AlertLook*, Idle02/03, IdleEating01, IdleToSitting, OnHook, SittingIdle,
   SittingToStanding) -- wie beim gespielten Erwachsenen; Defs schaltet Alarm/Sitzen ab (`canBeAlerted = false`, `sitRandomly = false`,
   `idleTypeNbr = 0`); ungespielt, ob ein anderer Zustand einen fehlenden Clip verlangt.
2. `NCBear` nur in einem NPC-Crew-Kommentar (keine Kollision).
3. Kommentare `server/BanditsNPCBearRegistry.lua:338` und `shared/BanditsNPCBear.lua:31` nennen die "Werkbank" (kein Cheat; vor der
   echten Uebernahme streichen waere sauberer).

## 5. Naehte-Liste `baer/NAEHTE.md`

15 Eintraege (Tierpflege `NOT_TENDED`, `fleeZombies`, Avatar/Portrait, Sandbox-Seite, Texte, Tier-Menue, Welt-Menue, Vanilla-Tabellen,
Animset buck, Modell in `module Base`, Register/Befehlsmodul, Pluenderer entfaellt, NPC-Crew-Figuren entfaellt, V-Taste spaeter,
Wachsen spaeter), "Die Zeilen: keine", Laufzeit-Aufsaetze (nur Naht 1, OnGameBoot, Riegel, `installed`), die 24 erlaubten Fundstellen
des Trockenlaufs, Cheat-Ausnahmen und erlaubte Treffer, was beim Umbenennen in B5a mitziehen muss. Fundstellen am 10.11. nachgelesen:
NC `BanditsNPCLivestock.lua:5152` (heute 14 Code-Zeilen mit `NOT_TENDED` in 9 Dateien), `BanditsNPCAnimals.lua:50-89`,
`BanditsNPCPortrait.lua:324`, `BanditsNPC.lua:6101` (`Opt(name, default)`), `:187` (`Err`), `:95` (`DIAG`); Vanilla
`ISAnimalContextMenu.lua:1235`, `:310`, `:317`.

## 6. Offen, ungeprueft

- **Alles ungespielt.** Laufzeitfragen aus `bau_kern.md` 6 und `bau_oberflaeche.md` bleiben: Rechtsklick am Jungen erscheint ueberhaupt,
  Streichel-Haltung "lamb", Balkenhoehe `barZ`, `%%` in `getText`, Spiegel/OnlineID nach Speichern/Laden, `setBlockMovement`, `fleeTo`,
  dedizierter Server (GLB, `getObjectListForLua`, `addAnimal` aus eigenem Antrieb, Neubau der Zeitaktion aus den Feldern, Sync).
- **Echte Uebernahme gesperrt bis B5a:** 24 Altlasten. Bis dahin nur Trockenlauf/Probe mit `--vor-b5a`.
- **Platzhalter-Modell:** das GLB/PNG aus `baer_baby/entwurf`; das Modell aus `baer-junges` ersetzt es (gleiche Namen, gleiche 15 Clips
  noetig -- das Skript prueft Clips gegen die Knoten). Die PNG ist 1,3 MB; die Vorgabe-Option "Max. Texturgroesse" deckelt laut
  Werkstatt-CLAUDE.md 8 auf 256.
- **Nicht im Staging, nur Vorschlag:** `mod_info_vorschlag.txt` (beide `mod.info` der Test-Mod von Hand ersetzen, wenn das Staging in die
  Test-Mod geht).
- **Klein, kein Fehler:** steht ein reifer Koeder an, waehrend der Welt-Deckel voll ist, versucht `baitAppear` es bei jedem Hirn-Takt
  (1,5 s) erneut (je hoechstens 25 Kachelfragen, gedeckelt durch 16 Koeder); haengt nicht, kostet wenig.
- **Sandbox-Tooltips mit festen Zahlen** (2/5/12/30 %, "eine bis drei Naechte") stimmen nur, solange `B.CFG.forestRate` und
  `BearBaitNights` bleiben (aus `bau_oberflaeche.md`).
- **Uebersetzungen** ohne Muttersprachler gegengelesen.
- **Nicht in B1a** (Auftrag): Wachsen, Kampf/Gegenwehr, Befehle, Baeren-Fenster/V-Taste, Namensschild/Lebensbalken, Beduerfnisse,
  Inventar, Schlafen, Umbenennen der alten `NCBear*`-Dateien und der Art `bear` (B5a).

Statisch geprueft, nicht gespielt.
