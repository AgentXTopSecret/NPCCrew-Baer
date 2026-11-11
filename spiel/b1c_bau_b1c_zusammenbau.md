# Lauf baer-b1c: ZUSAMMENBAU + UEBERNAHME (B1c Selbstheilung, Laerm, Zombies, Mitfahren, Call to me, Gehen, Markierung, Karte, Optionen)

Stand 11.11.2026 Nacht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (B1a + B1b + B1c KERN
+ B1c OBERFLAECHE). Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart, kein Download.
Geschrieben: eine Kommentarzeile im Staging (1.3), `attrappe/gesamt/run.lua` (Abschnitt 18 + Attrappen), `attrappe/gesamt/xref_b1c.py`
(neu) mit `xref_b1c.txt`, `ergebnis.txt`, `ergebnis_probe.txt`, `attrappe/pruef_b1b/ergebnis_b1c.txt`, `baer/tools/baer_uebernahme.py`,
`baer/NAEHTE.md`, `staging_dateien.txt`, `mod_info_vorschlag.txt`, die Probe unter `probe_b1c/` und die Ausgaben `trockenlauf_b1c*.txt`,
`probe_b1c_ausgabe.txt`. Nach dem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).

## 0. Ergebnis

| Pruefung | Ergebnis |
|---|---|
| Grenze KERN <-> OBERFLAECHE (`attrappe/gesamt/xref_b1c.py`, neu) | **0 Luecken**, 3 Hinweise (Rueckfallwerte, 6 Z3) -- `xref_b1c.txt` |
| Gegenprobe xref (8 Verderbnisse einer Staging-Kopie im Scratch) | alle 8 erkannt (11 Luecken) |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` (neu Abschnitt 18a-18n) | **812 bestanden, 0 Fehler** (vorher 519); einzige `***`-Zeile ist die gewollte Heilungszeile in 18c |
| dieselbe gegen die in die Probe kopierten Dateien | **812 / 0**, `ergebnis_probe.txt` byte-gleich mit `ergebnis.txt` |
| Gegenprobe Gesamt-Attrappe (12 Verderbnisse) | alle 12 rot (10 mit 1-25 Fehlern, 2 brechen mit Lua-Fehler ab) |
| Attrappen der Bauer auf dem Endstand | kern 136/0, b1b_kern 204/0, b1c_kern 154/0, ober 116/0 + 117/0, b1b_ober 144/0 + 134/0, b1c_ober 193/0 + 180/0; pruef_b == `ergebnis_b1b_nach.txt`; pruef_b1b siehe 6 Z2 |
| Text-/Beleg-Pruefer | `texte_pruefen.py` 0, `_b1b` 0, `_b1c` 0; `belege.py` 0 von 112, `_b1b` 0 von 51, `_b1c` 0 von 89; `probe_force.py` 23 Faelle / 0 |
| Lua-Pruefer (23 Lua-Dateien des Stagings) | luacheck 0 failed, scopecheck 0, localcount hoechstens 69 insgesamt (World.lua `B.ScanAnimals`), luacheck_pz 16 x W113 = die bekannten (3 Aktionsklassen in Menu.lua, 13 in der Bench); alle LF, reines ASCII |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (wie B1a/B1b) |
| Trockenlauf ohne `--vor-b5a` | **24 Fehler = genau die 24 Altlasten** aus `ALT_EXPECTED`, sonst nichts |
| Gegenprobe der neuen Skript-Regeln (verdorbene Kopie) | 7 Fehler wie erwartet (3.3) |
| Probe `--probe probe_b1c --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**; 49 Dateien geschrieben (22 Lua, 5 Modell/Textur/Skript/Knoten/Bild, 21 Texte, `sandbox-options.txt`); alle vier Lua-Pruefer gruen (luacheck_pz 0 Treffer + 3 erlaubt) |
| `staging_dateien.txt` neu | **49 Dateien: 7 neu, 25 ueberschreibt, 17 gleich** (gegen NCBearTest mit B1b, Stand 11.11. 01:19) |

## 1. Grenze KERN <-> OBERFLAECHE

### 1.1 Werkzeug `attrappe/gesamt/xref_b1c.py` (neu; loest `xref_b1b.py` ab, das an der neuen Form `viewEntry(rec, pkey, ms)` abbricht)
Aufruf `python -I xref_b1c.py [lua-Ordner]`, Exit 1 bei einer Luecke. Ergebnis auf dem Staging (`xref_b1c.txt`):
1. **B.*/U.***: 157 / 157 Namen definiert, U.* 20 / 20; U.* nie im KERN, B.* in der OBERFLAECHE nur `ShowNote`/`OnView`/`UI`; Doppel nur auf
   Dateiebene gezaehlt (xref_b1b meldete `B._zedFrom` und `B._healScanAt` faelschlich doppelt: das sind Zuweisungen IN Funktionen), sonst 0;
   keine Funktion in zwei Dateien. **43 Funktionen aus Plan 6.3/6.4 je in ihrer Datei aus 6.1** (z. B. `B.PlaceCub` in Ride.lua, `U.Opt` in
   Options.lua). OBERFLAECHE ruft vom KERN genau: ApplySync, Ask, CFG, CMD, CUB, CheckBait, CheckFeed, CheckPet, CleanName, Err, ErrEvery,
   FoodList, IsBaitFood, IsSP, Log, ModeOf, NearForest, Now, Opt, PlayerKey, SP_KEY, T, View, ViewOf, WaitLeft, WaitParts -- deckt sich mit
   Plan 6.4 + B1a/B1b (Err/ErrEvery/Log nennt Plan 4.3). Bench: 39 Kern-Namen, alle definiert. **Ladefolge** (shared < client < server, je
   alphabetisch): 0 Aufrufe einer B.*-Funktion auf Dateiebene vor ihrer Definition.
2. **B.CFG**: 113 Felder, 112 gelesen (unbenutzt nur der B1a-Rest `orphanMs`); die acht Felder, die nur die OBERFLAECHE liest (`markerMs` ...
   `mapListMs`), werden ueber die lokalen Leser `cfg("name", vorgabe)` gelesen und deren Vorgaben sind gleich B.CFG. **B.OPTS == sandbox-
   options.txt**: 22 Optionen, Vorgabe/min/max/translation/page je gleich; `BearRideDistance` 15 (3..40), `BearCallCooldownMinutes` 5 (0..60)
   wie Plan 5.1/Kevin. **Optionen-Seite** `BanditsNPCBear`: `TagShow` (tickbox, true), `TagSize` (slider, 100); beide `U.Opt`-Leser im Hud mit
   derselben Id und Vorgabe.
3. **Befehle**: Client -> Schreiber BaitDrop, **Call** (Menu.lua), Hello, Mode, Rename -> `B.Handle`; `"Call"` geht woertlich an
   `B.HandleCall(player, args)` (`server/BanditsNPCBearServer.lua:400-403`); Schreiber -> Client Note, Sync. Felder: Call `{ id }` == was
   Ride.lua liest (`args.id`).
4. **Sicht**: `viewEntry` baut 18 Felder (neu x, y, ride, callWait); die OBERFLAECHE liest an Sicht-Eintraegen bond, callWait, id, mode, name,
   owner, ride, st, tame, x, y -- alle gebaut. `me` (B.SlotsOf): key, on, wild gelesen, alle gebaut. `B.BuildView` nimmt das wilde Junge des
   Finders immer auf (`wildOf`).
5. **Texte**: UI.json 109, Sandbox.json 50, IG_UI.json 3 je Sprache, gleiche Schluessel und Platzhalter in 7 Sprachen, `%%` gleich oft,
   sortiert, Round-Trip, kein BOM/CR, kein `<`/`>`, kein Testwort; `U.EN` 109 == EN/UI.json, **wortgleich**; 101 Schluessel als Literal im
   Code, alle in EN; jeder EN-Schluessel benutzt; **47 `U.T("KEY", ...)`-Aufrufe mit genau so vielen Werten wie Platzhaltern** (neu);
   Optionen-Seite: 6 Texte, alle Schluessel in EN.
6. **Meldungen**: 45 `note(k, t, ...)`-Stellen des KERNs, `t` passt zu `U.NoteText` (days, dir, name, num, wait) und zum Platzhalter;
   `WHY_T` 5 (neu `Why_CallWait = "num"`); alle 11 Schluessel aus Plan 6.7, die der KERN benutzt, stehen im KERN.
7. **Bild**: `media/ui/BanditsNPCBearCub_marker.png` (Marker.lua, Map.lua) liegt im Staging, 96 x 96, 4429 Bytes, MD5
   `9e45e9368ef389aa9b831689d7bd6721`, byte-gleich mit Kevins Quelle `_arbeit/baer_icon/BanditsNPCBearCub_marker.png`.

**Gegenprobe** (Scratch-Kopie, je eine Verderbnis: `"Call"` ohne Empfaenger, `x` fehlt in viewEntry, `U.Opt("TagSize", 150)`,
`Menu_CallTip` ohne Wert, falsches `cfg`-Feld, fester Titel auf der Optionen-Seite, RU ohne `Why_NoRoom`, Bild veraendert): 11 Luecken,
jede Verderbnis erkannt.

### 1.2 Von Hand nachgesehen (was ein Grep nicht sieht)
- **Call to me, Reihenfolge**: `B.HandleCall` setzt `follow` (`B.SetMode`), DANN die Abklingzeit (`callMark`), DANN `B.FlushViews`
  (`server/BanditsNPCBearRide.lua:322-326`) -- die Sicht danach traegt `callWait` 300 s; das Menue rechnet die Restzeit aus `callWait` und
  `U.viewAt` (`client/BanditsNPCBearMenu.lua` callWaitMinutes, `client/BanditsNPCBearClient.lua` U.NoteSync). Jede Ablehnung schickt Note
  UND Sicht (`refuse`, Ride.lua:263-268). Gesamt 18g: nach 1 min "about 4 min" im Menue und beim Schreiber.
- **Mitfahren und Anzeigen**: `ride` steht als `true`/nil in der Sicht; Hud (`wanted`), Karte (`mine`) und Menue (`addCall`) fragen
  `== true` -- kein Suchlauf, kein Symbol, kein Rechtsklick fuer ein mitfahrendes Junges (Gesamt 18f).
- **Lage fuer Markierung/Karte**: Sicht `x/y` = `rec.x/y` (ganze Kachel), nachgeschickt ab 3 Kacheln / 5 s an finder/bond/owner
  (`pushMoved`, Server.lua); Markierung und Karte nehmen zuerst die Client-Kopie (`U.CubObj`/`U.CubPos`, Hud.lua), sonst `x + 0.5` (18a, 18i).
- **Laerm-Wache und Gehen beruehren sich**: die Ersatz-Antwort geht ueber denselben `B.MoveTo` (`opt.walk`), die Ruhefrist haelt `B.Hold`
  ohne Sperre (18d: Sperre erst nach 2,5 s wieder) -- `setVariable("animalRunning", false)` und `pathToLocation(` stehen nur in `B.MoveTo`
  (World.lua:768-769; Skript-Regel 3.2).
- **Map-Aufsatz und NPC Crew**: nach der Uebernahme laedt `client/ISUI/BanditsNPCBearMap.lua` vor `BanditsNPCMiniMap.lua` (alphabetisch);
  beide merken die vorige Methode und haengen nur einmal ein (NC `client/ISUI/BanditsNPCMiniMap.lua:263-280`) -> Vanilla -> Baer -> NPC Crew.

### 1.3 Luecken geschlossen
**Keine Luecke ueber die Grenze gefunden; kein Code geaendert.** Einzige Aenderung im Staging: `client/ISUI/BanditsNPCBearMap.lua:18`,
Kommentar "(Naht 10)" -> "(baer/NAEHTE.md Zeile 18)" -- Plan 10 schlug die Naht-Nummern 10/11/12 vor, die sind in NAEHTE.md schon vergeben
(Modell, Register, Koeder); die B1c-Naehte stehen dort als Zeilen 18-24. Neue MD5 Map.lua `c8d3a80b1a67fc76e2d1e8fc771035e0` (8796 Bytes; der
Bauer-Bericht nennt den Stand davor). Danach luacheck/scopecheck 0, ASCII/LF.

## 2. Gesamt-Attrappe `attrappe/gesamt/run.lua`

Aenderungen: `FILES` + `client/BanditsNPCBearOptions.lua`, `client/ISUI/BanditsNPCBearMap.lua`, `client/ISUI/BanditsNPCBearMarker.lua`
(Ladefolge wie im Spiel); `loadAll` laedt vor den Mod-Dateien **Vanillas echtes `client/PZAPI/ModOptions.lua`** (nur lesen) und legt die
Kartenklassen frisch an (`ISMiniMapInner` ohne eigene render, `ISWorldMap` mit -- wie Vanilla); Attrappen `UIFont.Medium/Large`,
`ISUIElement`, `getCore`, `getTimeInMillis`, `getGametimeTimestamp`, `IsoUtils`, `CharacterTrait`, `getGameTime():getHour`, Spieler
`getModData/hasTrait/isOutside` (fuer Bandits' echte Markierung). Abschnitte 1-17 unveraendert (weiter gruen; mehr Pruefungen nur durch die
drei zusaetzlichen Ladevorgaenge je `loadAll`). **Abschnitt 18 (neu, Plan 7.3; 260 Pruefungen, davon 115 Lade-Pruefungen)** in zwei
Funktionen (Lua 5.1: 200 aktive lokale Namen je Funktion, der Hauptteil ist nah dran):
- **18a** wildes Junges in 40 Kacheln -> Sicht mit `me.wild`, `x/y` -> **Markierung an** (Bandits' `set` ECHT: feste Id, Kevins Symbol,
  1800, Farbe 1.0/0.72/0.30, "Bear cub nearby"; ohne Client-Kopie an Sicht-Kachel + 0,5, mit Kopie live; gleiches Element verschoben) ->
  entdeckt (shy) -> noch an -> gezaehmt -> **genau ein `set(..., 0, ...)`**, Bandits-Element unsichtbar.
- **18b** "Follow me" und "Call to me" im Menue -> folgt -> "Bruno" -> **Karten-Symbol**: Mini-Karte 1 Symbol,
  `drawTextureScaledAspect(tex, x, y, 14, 14, 1.0, 1, 1, 1)`, an der Stelle des Jungen; grosse Karte 28 px bei Zoom 15, Vanilla-render 1 x;
  `worldToUIX/Y` immer mit zwei Zahlen.
- **18c** **Absturz** (globale ModData ohne Register, Tier mit Spiegel bleibt, alles Lua neu, Heil-Fenster offen) -> erster Takt:
  Eintrag `b1` zurueck, tame, `__sp`, Bruno, follow, 100, gleiches `u`; genau eine Fehlerzeile `heal: entry b1 (tame, owner __sp) restored
  from the mark on the animal`; "Your bear is back."; dasselbe Tier gebunden, genau ein Eintrag.
- **18d** **Schuss** (Stress + 1,0 an beiden Jungen, je ein Bild): das zahme antwortet im SELBEN Bild genau einmal mit
  `setVariable:animalRunning=false` DANN `pathToLocation:<ganze Zahlen>`, bleibt beim Besitzer, Ruhefrist laeuft; der Hirn-Takt in der Frist
  haelt ohne Sperre, danach wieder mit; das scheue Vergleichs-Junge (ohne Besitzer) bekommt keine Antwort und steht nicht auf der Wache.
- **18e** **Zombie** 4 Kacheln hinter dem Jungen -> `B._hot`, Junges auf der dem Zombie abgewandten Seite dicht am Besitzer (`hide`), Takt
  schon nach 800 ms, am Versteck Sperre; Besitzer 15 Kacheln weg -> **flieht** (Abstand >= 9, `flee`), Nachlauf ohne Befehl, nach 3 s Wache aus,
  folgt wieder.
- **18f** Besitzer steigt in 14 Kacheln ein -> **faehrt mit** (Koerper entfernt, gen + 1, follow, "Your cub jumps in with you.", kein Tier, Sicht
  `ride`, kein Karten-Symbol) -> Fahrt 200 Kacheln (Lage wandert, nie vermisst) -> **Speichern/Laden in der Fahrt** (ride + Name im Register,
  weiter kein Tier) -> aussteigen: nach 1 s **genau ein Tier** neben ihm, follow, gen + 2, "Your cub hops out.", Spiegel mit neuer gen, Name/
  Zaehmung/Besitzer gleich.
- **18g** "Stay here", 30 Kacheln weg -> **"Call to me"** frei mit Tooltip "... every 5 minutes." -> altes Tier entfernt, neues neben dem
  Besitzer, genau eins, follow, "Here is your cub again.", Sicht `callWait` 300; nach 1 min grau "about 4 min", Schreiber lehnt ab (Why_CallWait
  4), weiter ein Tier; im Auto grau "Not while you are in a vehicle."
- **18h** **Gehen**: Rest 2,8 Kacheln, Besitzer steht -> `pathToLocation` (erst `setVariable(animalRunning, false)`), kein `fleeTo`; Rest 7 ->
  rennt; Besitzer geht -> rennt.
- **18i** Karte live (Alpha 1,0) / ohne Client-Kopie an der letzten Kachel (0,55); **Optionen**: Seite `BanditsNPCBear` (Name als Schluessel) mit
  TagShow/TagSize; Schild an -> TagShow aus: kein Schild -> TagSize 200: Zeile 1 Large, Zeile 2 Medium. SP am Ende: genau 1 Heilungszeile, sonst
  keine `***`-Zeile.
- **18m** MP (Server, A Besitzer, B fremd): A steigt ein -> Koerper weg mit `removeAnimal(OnlineID)`, Note_RideOn nur an A, Sync mit `ride` an A
  und B; **A meldet sich im Auto ab** -> faehrt weiter mit, kein Tier erscheint, keine Meldung; **meldet sich zu Fuss an** -> nach 3 s genau ein
  Tier neben A, Note_RideOff; **Server-Neustart in der Fahrt** -> ride im Register, danach genau ein Tier.
- **18n** **B schiesst** neben As Junges -> abgefangen; Bs wildes Junges nicht; **Zombie** auf Bs Seite -> As Junges versteckt sich hinter A
  (nie bei B); je Client: B hat am fremden Jungen kein "Call to me", keine Symbole auf Bs Karte, Bs Markierung zeigt auf SEIN wildes Junges;
  A: "Call to me" frei, eigenes Symbol live, keine Markierung; Klick -> genau ein `sendClientCommand` "Call" `{ id }` -> Server: altes Tier weg,
  neues neben A, Note_Called; zweiter Ruf -> `Why_CallWait` (t num, v 5) an A; Bs gebastelte Bitte -> `Why_NotOwner`; weiter genau ein Tier;
  keine `***`-Zeile.

**Gegenprobe** (Scratch-Kopien, je eine Verderbnis; Lauf mit `run.lua <ordner>`): Laerm-Antwort aus 5 Fehler; Aussteigen aus -> rot (Abbruch);
Heilung aus -> rot (Abbruch); Karte nie eigen 8; Markierung nie aus 2; TagShow wirkungslos 1; nie gehen 2; kein `callWait` 2; Zombie-Suche
blind 7; Einsteigen nie 25; Call ohne Besitzpruefung 1 (Bs Bitte); Versteck vor statt hinter dem Besitzer 3. Die Attrappe zeigt echte Fehler.

**Grenze der Attrappe** (wie B1a/B1b): `fleeTo`/`pathToLocation` setzen das Tier sofort ans Ziel (deshalb hinkt in 18a die Sicht-Lage dem Tier
nach -- gewollt, "letzte bekannte Stelle"); Wege, Laufzeit, Tueren, Engine-Flucht, Netz-Ruckeln, echtes Fahrzeug zeigt sie nicht. Ein
Lua-Zustand fuer Server und beide Clients (Markierungs-Zustand teilen sich die "Clients" -- deshalb fuer A nur "keine positive Markierung").

## 3. Uebernahme-Skript `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md`

### 3.1 Was sich aenderte (Plan 10)
- (a) Tier-Regel `CreateCub`: zweiter erlaubter Aufrufer `("42/media/lua/server/BanditsNPCBearRide.lua", "B.PlaceCub")`.
- (b) neue Regeln `animalRunning` (`setVariable("animalRunning"`) und `pathToLocation` (`:pathToLocation(`) je nur in `B.MoveTo`
  (World.lua) -- die beiden Aufrufe mit Kevins Wort an genau einer Stelle.
- (c) Bilder: `UI_ASSET` = `42/media/ui/BanditsNPCBear*.png` wird kopiert; neuer Block "Bilder der Oberflaeche": PNG-Kopf + IHDR,
  hoechstens 512 x 512, jedes kopierte Bild von der Lua genannt (sonst Warnung), jedes genannte Bild in der Uebernahme (sonst Fehler);
  Kollision gegen NPC Crew (`42|common/media/ui`, eigener Namensraum), Vanilla und **Bandits** (`42.22`, `common`) -- heute 0.
- (d) die sechs neuen Lua-Dateien deckt `LUA_BEAR` (22 Lua kopiert); (e) Sandbox generisch (22 Optionen gegen B.OPTS und Sandbox.json).
- **Neu, Cheat-Pruefung** `callAt`: `B._callAt` (Abklingzeit von Call to me) nur in `server/BanditsNPCBearRide.lua` (Dateiebene, `B.CallLeft`,
  `callMark`) -- zuruecksetzen kann nur die Werkbank (`NCBear_CubCallReset`). **Optionen-Seite**: jedes Text-Argument von
  `ModOptions:create`/`addTitle`/`addTickBox`/`addSlider`/... ist ein Schluessel `UI_BN_Bear_*` (Regel `menue`).
- Kopftext (B1c, Punkte 1 und 6), Plan-Zeile "Naehte" nennt den Vanilla-Karten-Aufsatz, Tier-Regel-Liste zeigt "Dateiebene".
- `NAEHTE.md`: Kopf (Stand 11.11., NPC Crew v3.14.69, B1c ohne Naht in einer NPC-Crew-Datei), Zeilen 4 (22 Optionen), 5 (109/50 Texte,
  `%%`), 6 ("Call to me"), 11 (Befehl Call, Register/Spiegel v2, Sicht-Felder), 13, 14, 17, **neu 18** Karte (Aufsatz auf Vanillas Klassen
  neben NPC Crews, Datei-Ende + OnGameStart, begruendet nicht OnGameBoot), **19** Mod-Optionen (eigene Seite neben `NPCCrew`), **20**
  Bildschirm-Markierung (geteilte Stelle mit `bnwsArrival`, Versatz), **21** Zombies/Banditen (nur lesen, Riegel), **22** Mitfahren (gelernt
  von P.BeginRide, nicht kopiert), **23** Laerm, **24** Bild; Absatz zu den B1c-Regeln; "Die Zeilen: keine" auch fuer B1c.

### 3.2 Laeufe (Ausgaben im Ordner `_arbeit/baer_zaehmen/`)
- `trockenlauf_b1c_vor_b5a.txt`: OK, 0 Fehler, 26 Warnungen (1 Clip-Warnung GLB, 24 Altlasten, 1 NPC-Crew-Kommentar). Bilder: 1 (96 x 96).
  Texte: UI.json 109 neu (NPC Crew 3810 -> 3919), Sandbox.json 49 neu (92 -> 141), IG_UI.json 3 (neu angelegt). Cheat-Pruefung: 22 Lua,
  5505 Codezeilen, **Funde 0**; Tier-Regeln je an ihrem Ort (CreateCub: Ride.lua:68 B.PlaceCub + Server.lua:121 B.AppearFor;
  animalRunning/pathToLocation: World.lua:768/769 B.MoveTo; callAt: Ride.lua:28/222/235/245/251). Kollisionen 0 (Dateinamen, Vanilla,
  Bandits, Skriptnamen, Globale, v3.8.38). "Texte aus der Lua: 101 benutzt, fehlen in EN: 0; Ersatztexte 109, wortgleich: ja".
- `trockenlauf_b1c.txt` (ohne `--vor-b5a`): 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere.
- `probe_b1c_ausgabe.txt` (nur unter `_arbeit/baer_zaehmen/probe_b1c/`): OK, 0 Fehler, 26 Warnungen, 49 Dateien, luacheck/scopecheck/localcount
  je kopierter Datei gruen, luacheck_pz 0 Treffer + 3 erlaubt.

### 3.3 Gegenprobe der Skript-Regeln
Scratch-Staging mit: zweitem `pathToLocation` + `setVariable("animalRunning"` in `B.CalmAnswer`, `B._callAt = {}` in Server.lua, festem Titel
"Display above bears" auf der Optionen-Seite, `B.CreateCub` aus `B.CalmDrop`, fehlendem Marker-Bild und einer Text-Datei als
`BanditsNPCBearExtra.png` -> **7 Fehler**, jeder an seiner Stelle (Regeln pathToLocation, animalRunning, callAt, menue, CreateCub, "Lua nennt
ein fehlendes Bild", "kein PNG").

## 4. `staging_dateien.txt` und `mod_info_vorschlag.txt`
- `staging_dateien.txt` neu (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen NCBearTest mit B1b): **49 Dateien, 7 neu** (Options.lua,
  Map.lua, Marker.lua, Guard.lua, Heal.lua, Ride.lua, `ui/BanditsNPCBearCub_marker.png`), **25 ueberschreibt** (B1c-Code, Texte, Sandbox,
  Bench), **17 gleich** (Crew/Defs/Food, Zeitaktionen, NameBox, 7 x IG_UI.json, Modell, Textur, Skript).
- `mod_info_vorschlag.txt`: Beschreibung um B1c ergaenzt (Selbstheilung, Laerm, Zombies, Mitfahren, Call to me, Gehen, Pfeil, Karten-Symbol,
  Optionen), die sechs neuen Testhilfen `NCBear_CubForget/_CubMark/_CubCalm/_CubGuard/_CubRide/_CubCallReset` (21 gesamt, gegen die Bench
  gezaehlt), "ohne Bandits fehlt nur der Pfeil"; ASCII, LF, fuer `mod.info` UND `42/mod.info`.

## 5. Einzelspieler und Mehrspieler
| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Selbstheilung | Spiegel-Schluessel -> `__sp`; Heil-Fenster 2 min, Suchlauf je 15 s (18c) | nur Konten ungleich `__sp`, Deckel je Spieler, Register gewinnt bei Widerspruch (b1c_kern 1i-1k2) |
| Laerm | Wache je Bild (`OnTick`) beim einen Programm (18d) | Wache am Server, fragt nicht, wer laermt (18n) |
| Zombies | `getZombieList` bzw. `BanditZombie.CacheLightZ` (b1c_kern 3h) | `getZombieList`, Banditen ueber `GetBanditClusterData` (Riegel); hinter SEINEM Besitzer (18n) |
| Mitfahren | Aussteigen nach 1 s (18f) | nach 3 s zu Fuss und <= 4 K/s; Abmelden/Neustart in der Fahrt sauber (18m) |
| Call to me | `B.Ask` -> `B.Handle` direkt, Note/Sicht direkt (18g) | genau ein `sendClientCommand` `{ id }`; Server prueft Besitz/Abklingzeit/Fahrzeug/Platz (18n) |
| Markierung / Karte / Optionen | aus der eigenen Sicht (18a, 18b, 18i) | je Client aus seiner Sicht; Fremde sehen keine Symbole (18n); Optionen je Rechner |
Rote Linien: kein Gegenstand erzeugt/vernichtet (B1c erzeugt keine Gegenstaende), nie zwei Tiere eines Eintrags (18c/18f/18g/18m/18n zaehlen),
kein neuer Kick-Weg (nur eigene Client-Befehle mit Kennung), nichts haengt endlos (Deckel je Wache/Antworten/Versuche), keine NPC-Crew-Figur
beruehrt (Banditen zaehlen nie als Zombie, Verstecken nur hinter Spielern).

## 6. Befunde des Zusammenbaus (fuer Pruefer / Kevin; kein Code geaendert)
- **Z1 (klein, Randfall, belegt): `B.RecOf` macht aus einem nicht herstellbaren zahmen Spiegel einen neuen Fund.** Gibt `B.HealFromMark`
  nil (Deckel `BearMaxPerPlayer` voll, MP-Besitzer nil/`__sp`), legt `B.RecOf` (`server/BanditsNPCBearRegistry.lua:358-363`) wie in Plan 2.6
  vorgesehen einen NEUEN "found"-Eintrag an und ueberschreibt dabei den Spiegel. Probe im Scratch (MP: Register verloren, alice hat schon einen
  anderen Baeren, bob fuettert ihr altes Junges): `heal: ... was not restored: cap`, danach `b2 st=shy owner=nil src=found`, Spiegel `shy` --
  alices Zaehmung ist weg und bob kann es zaehmen. Widerspricht dem Auftrag "nie neu als found/shy" (Plan 1.1: "solange die Regeln es
  erlauben"). Vorschlag (eine Zeile, nach Kevins Wort): in `B.RecOf` bei einem Spiegel mit `st` tame/fed/missing und Heil-Ergebnis nil
  `return nil, "heal"` (Menue sagt `Why_Gone`); der seltene Waisen-Suchlauf (je 120 s) stellt es her, sobald ein Platz frei ist.
- **Z2 (gewollt)**: `attrappe/pruef_b1b/run_nach.lua` (Pruefer B aus B1b, unveraendert) zeigt auf dem B1c-Stand 2 neue BEFUND-Zeilen und je
  einen Laufbefehl weniger in 1a-1d (`ergebnis_b1c.txt` gegen `ergebnis_nach.txt`): 3a "Bob im Auto: Bleiben" -- Bobs Junges steigt jetzt ein
  (Note_RideOn an Bob, Spur im Scratch belegt); 3i -- Bobs Junges faehrt noch mit (`rec.ride` gesetzt, kein Takt nach dem Aussteigen), die
  Bitte wird mit `Why_Riding` abgelehnt und gedrosselt. Abstaende in 1a-1d unveraendert (faellt nicht zurueck).
- **Z3 (Hinweis)**: drei Rueckfallwerte in `shared/BanditsNPCBearRules.lua` (`followLead or 0`, `walkDist or 0`, `walkSpeed or 0`) weichen von
  B.CFG ab -- wirkt nur, wenn das Feld fehlt (dann kein Vorhalt, nie gehen: die sichere Seite). Gelassen.
- **Z4**: `attrappe/gesamt/xref_b1b.py` bricht auf dem B1c-Stand ab (neue Signatur `viewEntry(rec, pkey, ms)`) -- abgeloest durch
  `xref_b1c.py`, das alles von xref_b1b plus die B1c-Punkte prueft.

## 7. Offen / ungeprueft (Testpunkte; Plan 7.4 ist Kevins Testliste)
1. **Alles Laufzeit-Verhalten ungespielt**: ob die Laerm-Antwort die Engine-Flucht vor dem ersten sichtbaren Schritt ersetzt (OnTick nach dem
   Tier-Update; am Server ungeprueft) und ob `getStress` den Sprung im selben Bild zeigt (Diagnose `NCBear_CubLog(true)`, `NCBear_CubCalm()`);
   Fehlalarm "rennt ohne eigenen Befehl" bei langen eigenen Wegen (`ownSlackMs`/`ownMaxMs`); wie gross Medium/Large ueber dem kleinen Jungen
   wirken; ob die Optionen-Seite erscheint, wenn die Mod erst mit dem Spielstand aktiv wird; ob `getText` `%%` als "%" zeigt (Vanilla-Vorbild
   `ContextMenu_FullPercent` "%% full" ohne Werte, `V:client/ISUI/ISInventoryPaneContextMenu.lua:2187`).
2. MP: `getZombieList`/`getVariableBoolean("Bandit")`/`GetBanditClusterData` am dedizierten Server; `getVehicle()` fremder Spieler am Server;
   Einloggen im Auto; A3 aus B1a (`getObjectListForLua`/`getAnimalID` am Server -- Heilung, Aussteigen, Call to me haengen daran); Lage der
   Markierung im MP aus der Client-Kopie (OnlineID).
3. Neu-Erzeugen (Aussteigen, Call to me) verliert Engine-Werte (Akzeptanz, Stress, Hunger/Durst/Gesundheit der Engine; B1c benutzt keinen).
4. Ob die tote Figur im SP noch in `getSpecificPlayer` steht (`B.DeadAt`) -- sonst kommt das Junge zur neuen Figur (F3).
5. Doubles (`u` ~ 1,7e15, `ep`) durch die ModData (Vergleich mit `==`); weicht `ep` ab, kommt ein wildes Junges als scheues zurueck (kein Verlust).
6. Markierung nach Tod/neuer Figur zeigt von der alten Figur aus, bis Bandits raeumt; geteilter Bildschirm nur Spieler 1 (Bandits-Grenze).
7. NPC Crew wird parallel weitergebaut (v3.14.69 heute Nacht): Trockenlauf und Probe vor einer echten Uebernahme (erst nach B5a) neu laufen lassen.

## 8. Fragen fuer Kevin (Kevin schlaeft -- nichts davon haelt den Einbau auf; die Planer-Fragen F1-F16 in PLAN_B1C.md 11 gelten weiter)
1. **Z1**: soll ein zahmes Junges, das nach einem Absturz nicht sofort zurueck kann (Platz voll), lieber unberuehrbar warten, bis ein Platz frei
   ist, statt beim ersten Fuettern ein neues wildes zu werden? Empfehlung: ja, warten (eine Zeile, naechste Nachbesserung).
2. Zombie am Auto: steigt das Junge trotz Zombie ein, wenn du einsteigst (das Auto ist das beste Versteck)? Empfehlung: ja (KERN-Frage 1).
3. Beim Laerm macht das zahme Junge einen kleinen Schritt (1,5 Kacheln gehend) -- reicht das, oder soll es ganz stehen? Empfehlung: erst ansehen.
4. Schildgroesse in drei Stufen (100/150/200) als Schieber; "Namensschilder aus" gilt fuer alle zahmen Baeren, der Zaehm-Balken bleibt. Ok?
   Empfehlung: ja.
5. Abklingzeit 0 in der Sandbox zeigt "Works once every 0 minutes" -- lassen (nur Testeinstellung)? Empfehlung: lassen.
6. Markierung: Doppelklick blendet sie fuer dieses Junge ganz aus; 100 px Versatz neben NPC Crews Pfeil; kein Karten-Symbol fuer ein
   mitfahrendes Junges. Bitte beim Test ansehen.
7. Dein laufender Spielstand: die alte Zaehmung von "b1" steht nur im `_crash`-Ordner (Plan F16); weiter mit "b2"? Empfehlung: ja.

## 9. Einbau (NICHT gemacht -- nur wenn Kevin nicht spielt)
`tasklist | grep -i ProjectZomboid` leer -> Zip der Test-Mod nach `Zomboid/backups/NCBearTest/`, die 32 Dateien mit Zustand neu/ueberschreibt
aus `staging_dateien.txt` in EINEM Zug kopieren (die 17 "gleich" aendern nichts), byte-gleich nachzaehlen (MD5-Spalte), Beschreibung aus
`mod_info_vorschlag.txt` in `mod.info` und `42/mod.info`, zweites Zip. Danach Spiel neu starten (Lua laedt nur beim Start), `bugwatch.py`
mitlaufen lassen, Test nach PLAN_B1C.md 7.4 (Bandits geladen, Debug-"Tier Cheat" AUS, `NCBear_CubLog(true)`).

Statisch geprueft, nicht gespielt.
