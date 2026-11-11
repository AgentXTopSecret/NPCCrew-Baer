# Lauf baer-b1b: ZUSAMMENBAU + UEBERNAHME (B1b Folgen + Namensschild, Umbenennen, Futter hinhalten, Waisen)

Stand 11.11.2026 frueh. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (B1a + Fix 1-3 + B1b
KERN + B1b OBERFLAECHE). Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart, kein Download.
Geschrieben nur: zwei Kommentarzeilen im Staging (1.3), die Attrappe/Werkzeuge unter `attrappe/gesamt/`, `baer/tools/baer_uebernahme.py`,
`baer/NAEHTE.md`, `staging_dateien.txt`, `mod_info_vorschlag.txt`, die Probe unter `probe_b1b/` und die Ausgaben `trockenlauf_b1b*.txt`,
`probe_b1b_ausgabe.txt`.

## 0. Ergebnis

| Pruefung | Ergebnis |
|---|---|
| Grenze KERN <-> OBERFLAECHE (`attrappe/gesamt/xref_b1b.py`, neu) | **0 Luecken, 0 Hinweise** (`attrappe/gesamt/xref_b1b.txt`) |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` (mit neuem Abschnitt 17 a-i) | **483 bestanden, 0 Fehler**, keine `***`-Zeile des Codes (B1a-Stand vorher 261/0) |
| dieselbe gegen die in die Probe kopierten Dateien | **483 / 0** (`ergebnis_probe.txt`, byte-gleich mit `ergebnis.txt`) |
| Gegenprobe der Attrappe (5 absichtlich verdorbene Kopien im Scratch) | jede Verderbnis rot (1.4) |
| Attrappen der Bauer, wiederholt auf dem Endstand | kern 133/0, b1b_kern 145/0, ober 116/0 und 117/0 (echter Kern), b1b_ober 141/0 und 131/0, pruef_b unveraendert (`diff` gegen `ergebnis_nach.txt`: gleich) |
| Text-/Beleg-Pruefer der OBERFLAECHE | `texte_pruefen.py` 0, `texte_pruefen_b1b.py` 0, `belege.py` 0 von 112 abweichend, `belege_b1b.py` 0 von 51 |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen** (wie B1a; vorher 27, die 27. habe ich behoben, 1.3) |
| Trockenlauf ohne `--vor-b5a` | **24 Fehler = genau die 24 Altlasten** aus `ALT_EXPECTED`, sonst nichts (absichtlich rot bis B5a) |
| Gegenprobe der neuen Skript-Regeln (verdorbene Kopie) | 4 Fehler wie erwartet (3.2) |
| Probe `--probe _arbeit/baer_zaehmen/probe_b1b --staging ... --vor-b5a` | **OK -- 0 Fehler, 26 Warnungen**; 42 Dateien geschrieben (16 Lua, 4 Modell/Textur/Skript/Knoten, 21 Texte, `sandbox-options.txt`), zurueckgelesen; luacheck/scopecheck/localcount auf 16 Lua ok (groesste Funktion 54 lokal, World.lua), luacheck_pz 0 Treffer + 3 erlaubt |
| `staging_dateien.txt` neu | **42 Dateien: 2 neu, 26 ueberschreibt, 14 gleich** (gegen NCBearTest) |

## 1. Grenze KERN <-> OBERFLAECHE

### 1.1 Werkzeug `attrappe/gesamt/xref_b1b.py` (neu; erweitert `xref.py` von B1a)
Aufruf `python xref_b1b.py [lua-Ordner]` (Vorgabe Staging), Exit 1 bei einer Luecke. Prueft:
1. jede `B.*`- und `U.*`-Benutzung definiert (118 / 118 Namen, 14 / 14); `U.*` nie im KERN belegt, `B.*` in der OBERFLAECHE nur
   `ShowNote`/`OnView`/`UI`; keine Doppel-Definition ausser den drei bekannten aus B1a. OBERFLAECHE ruft vom KERN genau: ApplySync, Ask,
   CFG, CMD, CUB, CheckBait, CheckFeed, CheckPet, CleanName, FoodList, IsBaitFood, ModeOf, NearForest, Now, Opt, PlayerKey, SP_KEY, T,
   View, ViewOf, WaitLeft, WaitParts -- deckt sich mit PLAN_B1B.md 5.4 plus B1a.
2. jedes gelesene `B.CFG`-Feld steht in `B.CFG` (66 benutzt von 67; unbenutzt nur der B1a-Rest `orphanMs`, siehe bau_b1b_kern.md); kein
   `barZ` mehr; jede `B.Opt("...")` steht in `B.OPTS` (20); `B.OPTS` == `sandbox-options.txt` (20 Bloecke), Vorgabe/min/max je Option
   gleich (enum: 1..numValues), `translation`/`page` richtig.
3. jeder Befehl hat einen Empfaenger: Client -> Schreiber `BaitDrop`, `Hello`, `Mode` (Menu.lua, Bench), `Rename` (NameBox.lua, Bench) ->
   `B.Handle` (`server/BanditsNPCBearServer.lua:389`, `:393` -> `server/BanditsNPCBearFollow.lua:186`, `:220`); Schreiber -> Client `Note`,
   `Sync` -> `client/BanditsNPCBearClient.lua:315`, `:317`. Felder: Mode `{ id, mode }`, Rename `{ id, name }`; der Schreiber liest genau
   `args.id/mode/name`.
4. Sicht-Felder: `viewEntry` (`server/BanditsNPCBearRegistry.lua:421-437`) baut bond, fedN, feedAt, id, last, **mode, name**, oid, owner,
   petAt, petN, src, st, tame; die OBERFLAECHE liest an Sicht-Eintraegen nur bond, id, mode, name, owner, st, tame -- alle gebaut.
5. Texte in 7 Sprachen: UI.json 94, Sandbox.json 46, IG_UI.json 3 Schluessel je Sprache (EN zusaetzlich die 3 Altlasten des Erwachsenen,
   nie kopiert), gleiche Schluessel, gleiche Platzhalter, sortiert, Round-Trip, kein BOM/CR; `U.EN` 94 == EN/UI.json 94, wortgleich;
   86 Schluessel als Literal im Code, alle in EN; jeder EN-Schluessel wird benutzt (Dir_* ueber `"Dir_"`-Bau); Sandbox-Text zu jeder
   Option; kein `<`/`>` in einem UI-Text; kein Testwort in einem kopierten Text.
6. Meldungen: jede `note(k, t, ...)` des KERNs (32 Stellen) hat ein `t`, das `U.NoteText` kennt (days, dir, name, num, wait;
   `client/BanditsNPCBearClient.lua:159-180`), und `t` passt zum Platzhalter im EN-Text (mit `t` -> `%1` da, ohne `t` -> keiner);
   `tellBad` nur mit Texten ohne Platzhalter; `WHY_T` (4) alle mit Platzhalter.
Negativ-Probe: gegen die B1a-Lua der Test-Mod meldet das Werkzeug u. a. "B.CFG.barZ wird noch gelesen" und die fehlenden B1b-Befehle.

### 1.2 Von Hand nachgesehen (was ein Grep nicht sieht)
- Umschalter nur fuer den Besitzer mit Sicht: `client/BanditsNPCBearMenu.lua:256`; der Schreiber prueft trotzdem selbst
  (`server/BanditsNPCBearFollow.lua:186-216`: Zustand, Besitz, Objekt, Fahrzeug, Abstand). Name: `:220-244` (Vorab-Deckel, Besitz, `B.CleanName`).
- Client-Vorpruefung und Server benutzen dieselbe reine Regel `B.CleanName` (`shared/BanditsNPCBearRules.lua`) -- das Fenster
  (`client/ISUI/BanditsNPCBearNameBox.lua:30-34`) und `B.HandleRename` koennen nicht auseinanderlaufen.
- `ISTextBox`-Aufrufe gegen Vanilla gelesen: `ISTextBox:new` (`V:client/ISUI/ISTextBox.lua:280`, Spielernummer an 9. Stelle),
  `onClick` -> `onclick(target, button, param1, ...)` (`:127-137`), `setValidateFunction(target, func)` ist reines Lua (`:110-114`),
  Pruefer-Aufruf `validateFunc(validateTarget, text, ...)` (`:173-177`). `ISWorldObjectContextMenu.equip` mit Gegenstand
  (`V:client/ISUI/ISWorldObjectContextMenu.lua:2594-2622`) wie Vanillas Fuettern (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:93`).
  Tooltip ist Rich-Text: `V:client/ISUI/ISButton.lua:317-334` -> `ISToolTip.lua:192`, `:358` (`ISRichTextPanel`).
- Folgen laeuft am Schreiber: `liveRec` setzt erst `rec.x/y/z` aus dem Tier, dann `B.FollowStep` (`server/BanditsNPCBearServer.lua`,
  liveRec); `env.owner.car` kommt aus `B.Players()` (`server/BanditsNPCBearWorld.lua:43-44`, `:55`) -- kein Client-Glaube.
- Sicht fuer Fremde im MP: `B.BuildView` nimmt jedes Junge in `tellDist` 60 auf, `pushNewSights` schickt neu, wenn ein Junges in die
  Reichweite eines Spielers kommt -- ein folgendes Junges erreicht so auch B (Attrappe 17i).
- Fix 2 (`tHas` in `B.T`, `shared/BanditsNPCBear.lua:250-266`) und Fix 3 (`petting = PetAnimalCalf` in `shared/BanditsNPCBearDefs.lua:60`,
  `playBreedSound` in `shared/TimedActions/BanditsNPCBearPetAction.lua:66`) sind unveraendert da.

### 1.3 Luecken geschlossen (klein, nur Kommentare)
Der Trockenlauf meldete eine neue Warnung "Kommentare in Baeren-Dateien nennen Testbefehle oder die Testhilfe" -- zwei KERN-Kommentare
nannten die Werkbank (sie kommen sonst als Kommentar mit nach NPC Crew):
- `server/BanditsNPCBearWorld.lua:299`: "force (nur die Werkbank) ueberspringt NUR das Alter" -> "force ueberspringt NUR das Alter (der
  Spielcode ruft nie mit force)".
- `shared/BanditsNPCBear.lua:51`: "Im Spiel stellbar ueber den Werkbank-Befehl CubSet" -> "Stellwert: nach Kevins Blick im Spiel nachstellen".
Kein Code geaendert. Danach: luacheck/scopecheck 0, Dateiform LF/ASCII, Trockenlauf 26 Warnungen (wie B1a). Neue MD5:
World.lua `3254fc803decc1a28c8f61c6db0b80ab`, BanditsNPCBear.lua `c9950dc8bfb43fd2f12cc8f6227f5b60` (die Bauer-Berichte nennen den Stand davor).
**Sonst keine Luecke gefunden.**

### 1.4 Gegenprobe der Gesamt-Attrappe (Scratch-Kopien, je eine Verderbnis)
FollowStep tut nichts -> 4+ Fehler ("ein Laufbefehl", "~2 Kacheln hinter dem Besitzer", "Bewegungssperre"); Waisen-Raeumung aus -> 2
Fehler (SP und Server); Sicht ohne `name` -> 4 Fehler; "Hold out food" ohne `equip` -> rot; SP-Zweig von `B.Players` ohne `car` -> 4
Fehler (Auto). Die Attrappe zeigt also echte Fehler, nicht nur gruene Zahlen.

## 2. Gesamt-Attrappe `attrappe/gesamt/run.lua`

Aenderungen an der Datei (ZUSAMMENBAU): `FILES` + `client/ISUI/BanditsNPCBearNameBox.lua` und `server/BanditsNPCBearFollow.lua`
(alphabetisch vor Registry); UI-Attrappen `UIFont.NewSmall` (11 px, Small 14), `drawTextCentre` merkt `y`/Schrift, `ISTextBox`
(Form Vanilla, OK nur mit ja vom Pruefer), `getJoypadFocus`/`setJoypadFocus`, `equip` zaehlt Aufrufe und Argumente, Spieler
`getVehicle()` = `self.car` (vorher immer nil) und `getPlayerNum()`. **Gewollt geaenderte B1a-Erwartung** (Abschnitt 8, frueher
`:355`): nach 5 s steht am zahmen Jungen das Namensschild ("kev's cub" / "staying", 4 Texte) statt nichts. Abschnitte 1-16 sonst unveraendert.

Abschnitt 17 (neu, Plan 8.3; 206 Pruefungen, davon 68 Lade-Pruefungen der vier neuen Ladevorgaenge):
- **17a** Junges erscheint -> Spiegel sofort beim Erzeugen -> entdeckt -> Menue ohne Follow/Name -> Fuettern ueber Menue + Zeitaktion ->
  gezaehmt; Zaehm-Meldung nennt "Follow me"; `mode` fehlt = Bleiben; Schild "Kate's cub" / "staying" (Vorname der Figur, nie `__sp`);
  Anker: Unterkante Zeile 2 = `isoToScreenY(z + tagZ)`, `tagZ` 0,18, Zeile 2 in NewSmall, Zeile 1 1 px darueber.
- **17b** "Follow me" (nie zugleich "Stay here") -> `mode` follow, Meldung, SP ohne Sende-Eintrag, Sicht und Schild "following" sofort;
  Besitzer 10 Kacheln weg -> genau ein `fleeTo`, Junges ~2 Kacheln hinter ihm; nah -> Sperre, kein neuer Befehl; Besitzer rennt 7 weiter ->
  neuer Weg; Ziel weitergezogen -> neu berechnet; beim Laufen keine Sperre.
- **17c** 45 Kacheln (Deckel 40) -> Bleiben + "could not keep up. It waits to the west.", Heimat = Kachel, Schild "staying"; wieder Folgen;
  Besitzer im Auto -> Bleiben + "cannot follow a vehicle"; im Auto ist "Follow me" grau mit "Not while you are in a vehicle."; gebastelte
  Bitte im Auto -> Schreiber lehnt ab.
- **17d** Gegend des folgenden Jungen entladen -> Bleiben + "stayed behind to the west.", Heimat = letzte Kachel; Gegend wieder geladen ->
  wieder gebunden, zahm (nicht vermisst), bleibt bei Bleiben; 9 Kacheln von der Heimat -> zurueck (stayR 8).
- **17e** "Name the cub" -> Fenster (Titel, leer vorbelegt, maxChars 24, noEmpty, Eingabe 24, Spielernummer, Kennung, Ziel); Pruefer sperrt
  `<b>`, `a%1`, 25 Zeichen, nur Leerzeichen; Abbrechen tut nichts; OK "  Bruno " -> Register "Bruno", Meldung, Sicht, Schild "Bruno", SP
  ohne Sende-Eintrag; gebastelte Bitte "x<y" -> Schreiber lehnt mit der 24-Zeichen-Meldung ab; Fenster danach mit "Bruno" vorbelegt.
- **17f** Speichern/Laden (Register als Kopie, Tier behaelt seinen Spiegel, alle Lua-Tabellen neu): `mode` follow und Name bleiben,
  Sitzung leer, Junges ueber den Spiegel wieder gebunden, Schild "Bruno" / "following", folgt weiter.
- **17g** Waise (`B.CreateCub` ohne Eintrag, ohne Spiegel): Spieler in der Naehe -> bleibt (3 Waisen-Laeufe); Spieler 40 Kacheln weg,
  unbeobachtet, aelter als 30 s -> entfernt; eigenes Junges unberuehrt.
- **17h** Futter hinhalten am scheuen Jungen (10 Kacheln): Balken hat dieselbe Unterkante am Anker wie das Schild; ohne Futter grau mit
  Grund; mit Fisch: Untermenue wie beim Fuettern, Klick -> genau ein `equip(p, Hand, Fisch, true, false)`, keine Aktion angestellt, Fisch in
  der Hand, kein Gegenstand erzeugt/verbraucht; stillstehen -> Junges kommt bis <= 4,5 Kacheln; "Feed" dann frei und angenommen (ohne
  Hinterherrennen); 16 Kacheln -> kein Punkt.
- **17i** MP (Server + Client A Besitzer, B fremd in 12 Kacheln): A "Follow me" -> genau ein `sendClientCommand`, Server setzt follow,
  Note nur an A, Sync an A und B mit `mode` und Besitzer; B "Rename"/"Mode" -> abgelehnt (`Why_NotOwner`), nichts geaendert; A nennt
  "Bruno" -> `Note_Renamed` (t "name") nur an A, B bekommt den Namen; B's Client-Schild "Bruno" / "belongs to alice", ohne Namen
  "alice's cub"; B hat am fremden Jungen kein Follow/Stay/Name und kein "Hold out food"; Server rechnet das Folgen (Client schickt dafuer
  nichts); A offline -> Bleiben ohne Meldung, A wieder da -> Sicht "staying", Name bleibt; `Mode` mit nil-args still; Waise am Server mit
  `remove()` und `removeAnimal(OnlineID)`, As Junges unberuehrt. Am Ende: keine `***`-Zeile des Codes im ganzen Abschnitt 17.

Grenze der Attrappe (wie B1a): `fleeTo` setzt das Tier sofort ans Ziel; Wege, Laufzeit, Tueren, Treppen, Netz-Ruckeln zeigt sie nicht.
Ein Lua-Zustand fuer Server und Client (der Hirn-Takt wird im Client-Teil von 17i deshalb ausdruecklich angehalten, Kommentar dort).

## 3. Uebernahme-Skript `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md`

### 3.1 Was sich aenderte
- Dateien/Texte/Optionen: **keine Code-Aenderung noetig** (wie Plan 7 erwartet): Muster `BanditsNPCBear*.lua` erfasst Follow.lua und
  NameBox.lua (Trockenlauf listet 16 Lua), Texte 94 / 46 / 3 je Sprache zusammengefuehrt (UI.json NPC Crew 3801 -> 3895, Sandbox.json
  92 -> 137), 20 Sandbox-Optionen gegen `B.OPTS` geprueft, `U.EN` wortgleich, Bench `NCBearBenchCub.lua` nie kopiert.
- **Neu, Cheat-Pruefung Regel `force`** (`baer_uebernahme.py:184`): `B.ScanAnimals(..., <zweites Argument>)` im kopierten Code ist ein
  Fund -- Waisen ohne die 30-s-Frist entfernen darf nur die Werkbank (`NCBear_CubSweep`). Die Definition `function B.ScanAnimals(players,
  force)` und `B.ScanAnimals(players)` treffen nicht (Regex-Probe).
- **Neu, Text-Regel** (`baer_uebernahme.py:627-633`): kein `<`/`>` in einem `UI.json`-Text irgendeiner Sprache (Tooltip ist Rich-Text;
  Grund: schnittstelle_aenderungen.md "B1b OBERFLAECHE" 1).
- Kopftext: B1b genannt, Punkte 3 und 6 um die zwei Regeln ergaenzt.
- `NAEHTE.md`: Kopf (Stand 11.11., NPC Crew v3.14.68, B1b ohne neue Naht in einer NPC-Crew-Datei), Zeilen 4 (20 Optionen,
  `BearFollowMaxDistance`), 5 (94/46 Texte, `<`/`>`-Regel), 6 (Follow/Stay/Name, `ISTextBox`), 7 ("Hold out food" nur `equip`, kein
  Vanilla-Locken), 11 (Befehle Mode/Rename, Felder), 13 (Folgen kennt nur den Besitzer), 14 (Namensschild: NPC Crews
  `client/ISUI/BanditsNPCNameTags.lua` zeichnet keine Tiere -- grep `IsoAnimal|getAnimalType|isAnimal` = 0 am 11.11. -> keine Naht),
  15 (Wachsen spaeter), **16 neu** (Tiername nur im Register, Vanillas Tier-Info zeigt "Bear cub"; NPC Crew setzt keinen Tiernamen,
  `setCustomName` dort nur an Gegenstaenden `NC:shared/BanditsNPCLivestockButcher.lua:1760`), **17 neu** (Waisen: nur `ncbearcub`,
  nur ueber `B.RemoveCub`, MP A3 offen), Kommentar-Fundstelle NC `shared/BanditsNPC.lua:1357`, Absatz zu den B1b-Cheat-Regeln.

### 3.2 Laeufe (Ausgaben im Ordner `_arbeit/baer_zaehmen/`)
- `trockenlauf_b1b_vor_b5a.txt`: OK, 0 Fehler, 26 Warnungen (1 Clip-Warnung des GLB, 24 Altlasten, 1 NPC-Crew-Kommentar). Cheat-Pruefung:
  16 Lua, Funde 0, 1 Ausnahme greift (Defs `bodyModel`), Tier-Regeln je an ihrem einen Ort. "Texte aus der Lua: 86 benutzt, fehlen in
  EN: 0; Ersatztexte 94, wortgleich: ja". Kollisionen 0 (nur der eine NPC-Crew-Kommentar).
- `trockenlauf_b1b.txt` (ohne `--vor-b5a`): 24 Fehler, alle "noch umzubenennen (B5a)", 0 andere.
- Gegenprobe (Scratch-Kopie mit `B.ScanAnimals(players, true)` in beiden Hirn-Takt-Zeilen und `<staying>` in EN/UI.json): 4 Fehler
  (2 x `force`, `<`/`>`-Regel, dazu "Ersatztext weicht ab").
- `probe_b1b_ausgabe.txt` (Probe nur unter `_arbeit/baer_zaehmen/probe_b1b/`): OK, 0 Fehler, 26 Warnungen, 42 Dateien, alle vier Lua-Pruefer gruen.

## 4. `staging_dateien.txt` und `mod_info_vorschlag.txt`
- `staging_dateien.txt` neu erzeugt (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen NCBearTest): **42 Dateien, 2 neu**
  (`server/BanditsNPCBearFollow.lua`, `client/ISUI/BanditsNPCBearNameBox.lua`), **26 ueberschreibt** (B1b-Code und -Texte, Fix 2/3,
  `sandbox-options.txt`, Bench), **14 gleich** (Crew/Food/Bait-/FeedAction, 7 x IG_UI.json, Modell, Textur, Skript). Einbau: nur
  hinzufuegen/ueberschreiben, nie loeschen.
- `mod_info_vorschlag.txt`: Beschreibung um B1b ergaenzt (Folgen/Bleiben, Namensschild, Umbenennen, Futter hinhalten, Waisen) und die
  fuenf neuen Testhilfen `NCBear_CubFollow`, `_CubName`, `_CubFollowTest`, `_CubOrphan`, `_CubSweep`; ASCII, LF, fuer `mod.info` UND `42/mod.info`.

## 5. Einzelspieler und Mehrspieler
| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Follow me / Stay here, Name the cub | `B.Ask` -> `B.Handle` direkt, Meldung/Sicht direkt (17b, 17e: 0 Sende-Eintraege) | `sendClientCommand` -> Server prueft Besitz/Zustand/Auto/Abstand/Name -> Note an den Besitzer, Sync an Besitzer + alle in 60 Kacheln (17i) |
| Folgen-Takt | das eine Programm rechnet | nur der Server; der Client schickt nichts (17i) |
| Wechsel auf Bleiben | Auto, zu weit, Gegend entladen (mit Meldung); offline nur ohne Spieler | dazu Besitzer getrennt (ohne Meldung, 17i) |
| Schild | Vorname der Figur | Kontoname; Fremde sehen "belongs to <Konto>" (17i) |
| Futter hinhalten | nur `equip`, danach die Regel des Schreibers (17h) | gleich; der Server liest die Hand wie B1a |
| Waisen | `B.SeenInSP` schuetzt Gesehenes (17g) | `remove()` + `removeAnimal(OnlineID)` (17i); `getObjectListForLua` am Server weiter unbelegt (A3) |

Rote Linien: kein Gegenstand erzeugt/vernichtet (17h zaehlt das Inventar), kein neuer Kick-Weg (nur eigene Client-Befehle), nichts
haengt endlos (Laufbefehl hoechstens je 1,2 s, festgesteckt je 10 s), keine NPC-Crew-Figur beruehrt.

## 6. Offen / ungeprueft (fuer Kevins Test, Plan 8.4)
1. **Alles Laufzeit-Verhalten ungespielt**: Abstand beim Folgen im Spiel, Tueren, Treppen (wartet unten), Q-Ruf, Ruckeln im MP, Hoehe
   des Schilds (`tagZ` 0,18 ist gerechnet; nachstellen mit `NCBear_CubSet("tagZ", 0.25)`), ob `UIFont.NewSmall` kleiner ist [Nachbesserung B1b A3: statisch entschieden, NICHT kleiner -- `font NewSmall` und `font Small` laden in jeder Vanilla-Sprache dieselbe Datei, `media/fonts/EN/fonts.txt:75-79`/`:93-97`].
2. MP A3 (B1a): `getObjectListForLua`/`getAnimalID` am Server ohne Server-Beleg; B1b fragt dort zusaetzlich je 120 s (Waisen).
   `p:getVehicle()` am Server fuer jeden Spieler ist Jar-Lesart (bau_b1b_kern.md 7.4).
3. Namen mit Nicht-ASCII-Zeichen: Laenge/Zeichen haengen an Kahluas `string.len`/`string.byte` (ungeprueft).
4. Bekannte Grenzen: geteilter Bildschirm zeichnet nichts und bietet "Hold out food" nicht an (B1a-Grenze); Vanillas Tier-Info zeigt
   weiter "Bear cub" (Plan 0.3); ein SP-Spielstand, der spaeter als MP gehostet wird, hat Besitzer `__sp` (PLAN_ZAEHMEN.md:882,
   "Umzug spaeter") -- das Schild zeigt so ein Junges dann jedem als "eigen" mit "staying", Folgen geht nicht (ungespielt, Randfall).
5. Aufheben/Absetzen mit Cheat (Kevins Frage): ob Spiegel/AnimalID die Engine-Kopie ueberleben, ist ungeprueft; ohne beide wuerde das
   abgesetzte Tier nach 30 s unbeobachtet als Waise geraeumt, mit gleicher AnimalID schuetzt Riegel 2.
6. Ein ueber Vanillas Debug-Menue erzeugtes `ncbearcub` ist eine Waise und wird unbeobachtet geraeumt (gewollt, N5).
7. NPC Crew wird parallel in seiner eigenen Sitzung weitergebaut (z. B. `client/BanditsNPCInteract.lua` 10.11. 23:56, vor meiner Probe
   00:05): Trockenlauf und Probe gelten fuer NPC Crew v3.14.68 von heute Nacht; vor einer echten Uebernahme (erst nach B5a) neu laufen lassen.

## 7. Einbau (NICHT gemacht -- Kevin spielt mit der Test-Mod)
Wenn Kevin "Spiel ist zu" sagt: `tasklist | grep -i ProjectZomboid` leer -> Zip der Test-Mod nach `Zomboid/backups/NCBearTest/`,
die 28 Dateien mit Zustand neu/ueberschreibt aus `staging_dateien.txt` in EINEM Zug kopieren (die 14 "gleich" aendern nichts),
byte-gleich nachzaehlen (MD5-Spalte), Beschreibung aus `mod_info_vorschlag.txt` in `mod.info` und `42/mod.info`, zweites Zip.
Danach Spiel neu starten (Lua laedt nur beim Start), `bugwatch.py` mitlaufen lassen, Test nach PLAN_B1B.md 8.4.

Statisch geprueft, nicht gespielt.
