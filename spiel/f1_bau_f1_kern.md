# Lauf baer-f1: Bau KERN (shared/ + server/) -- Baeren-Fenster F1

Stand 11./12.11.2026, Nachtschicht. **Statisch geprueft, nicht gespielt.** Spiel 42.22.2. Grundlage: `PLAN_F1.md` 5, 6, 7.1-7.4, 8.1, 4b
(woertlich umgesetzt; Abweichungen/Zusaetze in `schnittstelle_aenderungen.md` Abschnitt "F1 KERN", Punkte 1-13). Nur Staging
`_arbeit/baer_zaehmen/mod/` und Attrappen geschrieben; nichts in Test-Mod, NPC Crew, Vanilla, Bandits; kein git, kein Spielstart.

## 0. Kurzfassung

- **Vorab nachgezaehlt:** Staging gegen `NCBearTest` (Git main 914ee79): 60 Dateien aus `staging_dateien.txt`, **alle 60 MD5-gleich**.
- **Neu:** `server/BanditsNPCBearOrder.lua` (Bleiben/Sitz/Frei-Takt, Aufstehen, Komm her, Passiv, C1). **Geaendert:** 10 Kern-Dateien
  (Liste 1). Client-Dateien, Texte, Bench: nicht angefasst (OBERFLAECHE).
- **Befehle:** `Mode` jetzt mit 4 Modi (follow/stay/sit/roam), neu `Come` und `Passive`; `Call` (Unstuck) und `Rename` unveraendert.
  Bleiben = steht still (zurueck ab 3 Kacheln), Sitz = haelt still und meldet `sit` in der Sicht, sobald er 800 ms ruhig an seiner Stelle
  steht, Frei = eigene gehende Spaziergaenge im Kreis (Vorgabe 12, Sandbox `BearRoamRadius` 4-30) mit 8-20 s Pausen, nie hinaus.
- **B1e-Reste:** A1/B6 `bd` an Why_Gone/Note_Dead/Why_OutOfReach (Kern-Seite); C1 "Baer ohne Koerper kommt von selbst wieder" mit drei
  Riegeln gegen ein Doppel; ein zahmer Baer wird nie mehr nach 24 h als "lost" geschlossen.
- **Pruefer:** luacheck 15/0, scopecheck 0, luacheck_pz W113 0, localcount max 40 aktiv / 77 insgesamt, luac -p ok, LF/ASCII.
- **Attrappen:** neu `attrappe/f1_kern/run.lua` **188 bestanden, 0 Fehler**; kern 136/0, b1b 204/0, b1c 192/0, b1d 162/0, b1e 153/0
  (Ausgabe **wortgleich** wie vor F1, 3 Pruefungen gewollt angepasst), gesamt 1672/0 (wortgleich; laedt Order.lua noch nicht --
  ZUSAMMENBAU), pruef_b/b1c wortgleich, pruef_b1b run_nach bis auf 1 neue erwartete Fehlerzeile gleich, nach_b1e 31/0, pruef_b1e run_nach 25/0.
- **Zwei Zusatz-Riegel fuer C1** (nicht im Plan, Begruendung 5): im MP erst, wenn der Suchlauf schon einen Baeren gesehen hat (A3), und
  nie, wenn ein ungebundenes Tier mit der AnimalID des Baeren geladen ist.

## 1. Dateien (unter `_arbeit/baer_zaehmen/mod/42/media/lua/`)

| Datei | Zustand | MD5 | Bytes |
|---|---|---|---|
| `server/BanditsNPCBearOrder.lua` | **neu** | 40d9f4f9a4336d8495e55a6c97624238 | 20381 |
| `shared/BanditsNPCBear.lua` | geaendert | 42fc610309f97e7c38194379baafb2ee | 34496 |
| `shared/BanditsNPCBearRules.lua` | geaendert | f5fb9493495fd4d7cfaa167e65723bfe | 36771 |
| `server/BanditsNPCBearFollow.lua` | geaendert | b2bb32dd3ee3272db61bb7bbed9478c5 | 16847 |
| `server/BanditsNPCBearServer.lua` | geaendert | b3428e67ecfd84aa791f18ddf4c65014 | 52451 |
| `server/BanditsNPCBearRegistry.lua` | geaendert | 70cc0dd5f350c75c9ee021a827b77b3e | 30424 |
| `server/BanditsNPCBearHeal.lua` | geaendert | bcf3f515caeadb1866e5b98b71fae738 | 24816 |
| `server/BanditsNPCBearGrow.lua` | geaendert | f044de9c1a85320a37a99e5c849fc7fb | 42466 |
| `server/BanditsNPCBearGuard.lua` | geaendert | ca9c3ec8ef2c03ff4f47c920a440ff97 | 18983 |
| `server/BanditsNPCBearRide.lua` | geaendert | 548e38593d0e29e32cd4bedf60e0215d | 19410 |
| `server/BanditsNPCBearWorld.lua` | geaendert | 596f8c291e0d233736b30d0458db9adc | 50505 |
Unveraendert (Kern): `BanditsNPCBearDefs.lua`, `...Stats.lua`, `...Food.lua`, `...Crew.lua`, alle `TimedActions/`. Die MD5 oben sind der
Endstand (ZUSAMMENBAU: `staging_dateien.txt` neu).
Attrappen: `attrappe/kern/attrappen.lua` (A.FILES + Order.lua, `ZombRandFloat` mit `A.randF`/`A.randFn`, `A.roomAt`), `kern/run.lua` 3h,
`b1b_kern/run.lua` 2e, `b1e_kern/run.lua` 12.1 (gewollt, je begruendet im Code), neu `f1_kern/run.lua` + `f1_kern/ergebnis.txt`,
`*/ergebnis_f1.txt` in kern, b1b..b1e_kern. `schnittstelle_aenderungen.md` Abschnitt "F1 KERN" angehaengt.

## 2. Aenderungen (Datei:Zeile, Endstand)

**shared/BanditsNPCBear.lua** -- Kopf :15-16; `B.CFG` :151-160 (stayNear 1.5, stayBack 3, backRunDist 8, sitSettleMs 800, standMs 2300,
roamMinStep 3, roamPauseMin/Max 8000/20000, comeNear 3, comeMaxMs 30000, reviveScans 2, reviveFailLog 3); `B.MODES` :164; Sandbox
`BearRoamRadius = { def = 12, min = 4, max = 30 }` :198 (Name in NPC Crew frei, 0 Treffer).

**shared/BanditsNPCBearRules.lua** -- `B.ModeOf` :334 (4 Modi, Register- oder Sicht-Eintrag, Rueckfall-Liste `MODES_DEF` :332);
`B.OrderDecide` :366 (rein; Regeln 31-41 und 6/7, Kommentar :342-359; Helfer `backTo` :361).

**server/BanditsNPCBearOrder.lua (neu)** -- `B.OrderStep` :97 (Bleiben/Sitz/Frei, Heimat-Nachtrag fuer Alt-Eintraege :104, Sitz-Ruhe
`settle` :68 / `unsit` :58, einmal Nachruecken :123/:132-136, Rueckweg ohne Neustart `goBack` :84, Regel 6 mit Heimat :141-149, Spaziergang
mit `B.RoamSpot` und Pause :150-176); `B.StandStep` :185; `B.ComeCheck` :203; `B.HandleCome` :253; `B.HandlePassive` :291; `B.ReviveMissing`
:334 (Riegel: MP-Beweis :341/:346, AnimalID :351).

**server/BanditsNPCBearFollow.lua** -- Kopf :12; `B.SetMode` :101 (Rueckfall-Liste `MODES_DEF` :99; 4 Modi; Heimat fuer stay/sit/roam; s.come/s.roam weg; Aufstehen
`standUntil`; "Sit" an sitzendem Baeren aendert nichts; Noten Note_Sit/Roam/Coming/Came/ComeFail, alle ueber `B.NoteBd`);
`B.FollowStep` :166 (am Anfang `B.ComeCheck` :168, beim Einsteigen `s.come = nil` :190); `B.HandleMode` :259 (4 Modi; Why_Gone +bd;
nicht geladen -> `Why_OutOfReach` +bd :281).

**server/BanditsNPCBearServer.lua** -- Kopf :14-15; `B.FeedComplete` Heimat bleibt bei Sitz/Frei :241-244; `B.Handle` "Come"/"Passive"
:411-419; `slowRec` missing schliesst nie, eine Diagnose-Zeile :500-511; `liveRec` `B.StandStep` :796, `B.OrderStep` :804;
`countMisses` revN/revFail leeren :862-864; `brainTickBody` C1 nach dem Suchlauf :977-986, ld/busy-Wechsel -> Touch :999-1021.

**server/BanditsNPCBearRegistry.lua** -- `B._s`-Kommentar :31-32; `B.InitRegistry` mode (4 Modi) / passive :133-145; `B.Close` Note_Dead
und Why_Gone mit bd :496-512; `viewEntry` :579 (ld :604, pas/u :606-609, hide/sit/cm/busy :611-617, GrowView auch missing :619).

**server/BanditsNPCBearHeal.lua** -- `MARK_FIELDS` + "passive" :42-48; `markMode` :51; `B.Restore` mode :236, passive :271;
`B.TakeNewerMark` mode/passive :377-380.

**server/BanditsNPCBearGrow.lua** -- Kopf :16-17; `B.BodyBusy` Touch bei Wechsel, `s.busySent` :476-501; `B.GrowView` tame+missing
:761-800 (`VIEW_X` :765, Erfahrung abgerundet auf 0,1, carry/dodge/fgtB/fish/nose :788-800).

**server/BanditsNPCBearGuard.lua** -- `B.GuardStep` Touch bei Wechsel von `g.on` :318-319.

**server/BanditsNPCBearRide.lua** -- `clearBodySession` + sat/satAt/backTried/standUntil/roam :54-61; `B.HandleCall` Why_Gone mit bd :368.

**server/BanditsNPCBearWorld.lua** -- `B.RoamSpot` :314-340 (Kommentar mit Belegen :307-313); `B.ScanAnimals` `B._aidSeen` :705/:764,
`B._scanSeen` :711-714.

## 3. Engine-Aufrufe (alle selbst nachgelesen; KEIN neuer Methodenname -- nur schon belegte Aufrufe an neuen Stellen)

| Aufruf (Argumenttypen) | Wo neu benutzt | Fundstelle (gleiche Argumenttypen) |
|---|---|---|
| `animal:getX()` / `getY()` | Order.lua OrderStep :116, HandleCome :278; World.lua RoamSpot :327 | Vanilla `shared/Definitions/animal/ButcheringUtil.lua:575-576` |
| `player:getVehicle()` | Order.lua HandleCome :274 | Vanilla `server/Vehicles/VehicleCommands.lua:11` |
| `player:getX()` / `getY()` | Order.lua HandleCome :278 | Bandits `server/BanditServerSpawner.lua:179` |
| `square:getX()/getY()/getZ()` | Order.lua OrderStep (Spaziergang), ReviveMissing | Vanilla `client/DebugUIs/DebugContextMenu.lua:636` |
| `ZombRand(Zahl)` | Order.lua OrderStep (Pause) | Vanilla `shared/TimedActions/Animals/ISMilkAnimal.lua:25` |
| `ZombRandFloat(0, 2 * math.pi)`, `ZombRandFloat(0, Zahl)` | World.lua RoamSpot | Bandits `server/BanditServerSpawner.lua:217`; zwei Zahlen Vanilla `server/Foraging/forageServer.lua:98` |
| `getCell():getGridSquare(x, y, z)` | World.lua RoamSpot | Vanilla `server/Animal/ISPickDungCursor.lua:104` |
| `square:getRoom()` | World.lua RoamSpot | Vanilla `shared/Util/AdjacentFreeTileFinder.lua:240` |
| `getTimestampMs()` | Order.lua, Follow.lua SetMode | Vanilla `server/Foraging/forageServer.lua:456` |
| `animal:isExistInTheWorld()` | Registry.lua viewEntry (ld) | Vanilla `shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29` |
| Platzregeln `spotOk` (TreatAsSolidFloor, getFloor/hasProperty, HasTree, isFree(false), isVehicleIntersecting) | World.lua RoamSpot (vorhandene lokale Funktion) | Belege in World.lua :100-114, :227-235 (B1c) |
| `getBehavior():setBlockMovement(b)` | ueber `B.Hold` (unveraendert) | Vanilla `shared/TimedActions/Animals/ISPetAnimal.lua:36`, `:49` |
| `fleeTo`, `setVariable("animalRunning", false)`, `pathToLocation(x, y, z)` | NUR in `B.MoveTo` (unveraendert; die beiden letzten mit Kevins Wort) | World.lua B.MoveTo |
| `addAnimal`/`addToWorld` | ueber `B.PlaceCub` -> `B.CreateCub` (unveraendert) | Vanilla `server/ClientCommands.lua:809-810` |
| `sendServerCommand` / `sendClientCommand` | ueber `B.Tell` / `B.Ask` / `B.SendView` (unveraendert) | wie B1a |
Jar-only: keine. Nicht benutzt: `getVariableString` (Plan 0.5; Dateiregel f1_kern 16), `setDebugAcceptance`.

## 4. SP- und MP-Zweig je Befehl

| Befehl | Einzelspieler (`not isServer() and not isClient()`) | Mehrspieler |
|---|---|---|
| Mode follow/stay/sit/roam | `B.Ask` -> `B.Handle` direkt -> `B.HandleMode` | Client `sendClientCommand("Mode", {id, mode})` -> Server prueft Kennung, Besitz (Kontoname), tame, ride, Koerper geladen, (follow: Fahrzeug, Abstand) -> `B.SetMode`; Meldung `sendServerCommand`, Sicht an Besitzer + alle in tellDist |
| Come | dto. -> `B.HandleCome` | Server prueft wie oben + Fahrzeug + BearFollowMaxDistance; `s.come` nur am Server |
| Passive | dto. -> `B.HandlePassive` | Server: `on` muss Wahrheitswert sein, Besitzer tame/missing; Register + Spiegel |
| Unstuck (Call) / Rename | unveraendert (B1b/B1c) | unveraendert |
| Takt (Bleiben/Sitz/Frei/Komm her/Aufstehen) | Hirn-Takt des einen Programms | Hirn-Takt am Server; Clients sehen nur die Sicht (mode, sit, cm, hide, busy, ld) |
| C1 | im Suchlauf, ohne MP-Riegel | im Suchlauf, erst nach Beweis `B._scanSeen` (A3) |
Kein Befehl vom Server an Clients ausser Note/Sync; kein neuer Client-Befehl ausser Come/Passive (Rolle user genuegt, wie Mode).
Leere Tabelle / falsche Typen -> still verworfen (f1_kern 3).

## 5. Abweichungen vom Plan (Kurz; ausfuehrlich in schnittstelle_aenderungen.md "F1 KERN")

1. **Sitz rueckt einmal nach** (Regel 33) und `ownBusy` -> keep auch bei Sitz/Bleiben: sonst stoppte `B.Hold` den Rueckweg bei 3 Kacheln,
   und zwischen 1,5 und 3 Kacheln setzte er sich nie (stuende fuer immer). Ist die Stelle unerreichbar, setzt er sich, wo er steht.
2. **Frei: Rueckweg IN den Kreis** (r - 3 vom Mittelpunkt), damit "Tier bei 15 -> zurueck gehend" (Plan 8.1 Nr. 6) gilt.
3. **Fuettern verschiebt bei Sitz/Frei die Heimat nicht** (`B.FeedComplete`) -- "Futter zieht den Mittelpunkt nie".
4. **C1 zwei Riegel mehr:** (a) MP erst, wenn der Suchlauf in dieser Sitzung einen Baeren gesehen hat (A3 offen -- sonst Doppel);
   (b) kein neuer Koerper, wenn ein ungebundenes Tier mit seiner AnimalID geladen ist (B1b-Riegel 2; sonst wurde der echte Koerper als
   Waise entfernt, `pruef_b1b/run_nach.lua` 2a). Beide mit gedrosselter Fehlerzeile; Unstuck geht weiter.
5. Sicht: Erfahrung abgerundet (nie hoehere Stufe als der Schreiber); `busy` laeuft von selbst ab -> ein Touch; `hideSent` unnoetig.

## 6. Pruefer-Ausgaben (15 Kern-Dateien)

```
luacheck.py      15 file(s) checked, 0 failed
scopecheck.py    15 file(s), 0 violation(s)
luacheck_pz.py   0 Treffer (W113); --unused: 3 alte (Rules.lua:41 'base', Rules.lua:160 'slots', Guard.lua:291 'players') + 2 neue
                 W212 (Order.lua:97 'players' in B.OrderStep, Order.lua:334 'ms' in B.ReviveMissing -- Signaturen aus PLAN_F1.md 7.2,
                 Form wie B.GuardStep)
localcount.py    hoechstens 40 aktiv (Server.lua brainTickBody :949) / 77 insgesamt (World.lua B.ScanAnimals :699); Order.lua max 22
luac5.1 -p       alle shared/server-Dateien ohne Fehler
Zeilenenden      LF, ASCII, Dateiende LF; keine neue Zeile > 140 Zeichen
Dateiregeln      (f1_kern 16) B.CreateCub( nur AppearFor/PlaceCub; B.PlaceCub( nur RideStep/HandleCall/BodySwap/ReviveMissing;
                 pathToLocation und setVariable("animalRunning" nur in B.MoveTo; kein next(, %a, getVariableString, spawn/debug/bench/
                 cheat/test im Code
Trockenlauf      baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a (schreibt nichts): NICHT OK -- 6 Fehler, 29 Warnungen.
                 Alle Tier-Regeln gruen (CreateCub, addAnimal, remove, pathToLocation, animalRunning, callAt, setSizeForced ...).
                 Die 6 Fehler gehoeren der OBERFLAECHE/dem ZUSAMMENBAU (PLAN_F1.md 11.3): 2 x Binding-Schluessel ausserhalb des
                 Namensraums, 4 x Tasten-Ausnahmen (Key.lua KEY_V/OnKeyPressed, Window.lua KEY_ESCAPE). Kern: 0 Fehler, 0 Kern-Warnung
                 (zwei Kommentare mit dem Clip-Namen "NCBear_StandUp" umformuliert, sonst Warnung "nennt Testbefehle").
```

## 7. Attrappen

| Lauf | Ergebnis | Bemerkung |
|---|---|---|
| **f1_kern** (neu) | **188 / 0** | 1 ModeOf/Register, 1b OrderDecide (26 Regel-Faelle), 2 Mode SP, 3 MP-Rundlauf, 4 Bleiben, 5 Sitz (genau eine Sicht mehr; Laerm-Versatz; Nachruecken; Aufstehen 2,3 s; Zombie zuerst), 6 Frei (200 Takte Zufall: Ziele <= 12, >= 3 vom Tier, nie Raum, Pausen 8-20 s, zurueck gehend aus 15, Futter zieht nie), 7 Komm her (came, 30 s, stuck, Ablehnungen, aus dem Sitz), 8 Passiv (+ Restore/TakeNewerMark, Drossel), 9 Unstuck unveraendert, 10 C1 (genau EIN addAnimal, gen N+1, alter Koerper stale entfernt, nicht geladen / offline / keine Kachel / zwei Vermisste / ride / ungebunden-geladen / AnimalID-Riegel / MP-Riegel), 11 nie verloren (48 h) + fed wie B1a, 12 Sicht (ld genau ein Touch, missing GrowView, hide, busy), 13 bd, 14 Tausch im Sitz/Frei, 15 Speichern/Laden + Spiegel-Heilung, 16 Dateiregeln |
| kern / b1b / b1c / b1d / b1e | 136/0, 204/0, 192/0, 162/0, 153/0 | Ausgabe wortgleich wie vor F1 (`*/ergebnis_f1.txt`). Gewollt angepasst: kern 3h (missing bleibt), b1b 2e (Why_OutOfReach), b1e 12.1 (C1 fuer den Fall aus) |
| gesamt | 1672/0 | wortgleich (laedt Order.lua noch nicht). Probe-Kopie MIT Order.lua: 1708/2 -- genau die zwei B1b-Bleiben-Pruefungen :1023/:1027 (Bleiben wanderte im Radius 12; jetzt gewollt still) -> ZUSAMMENBAU |
| pruef_b, pruef_b1c, pruef_b1d, nach_b1e, pruef_b1e run_nach | wortgleich / 10/0 (3 Befunde) / 31/0 / 25/0 | unveraendert |
| pruef_b1b run_nach | wie `ergebnis_b1c.txt` bis auf 1 neue Fehlerzeile (AnimalID-Riegel, erwartet) | 2a wieder OK |
| pruef_b1e run.lua | 20/5 | wie seit der B1e-Nachbesserung dokumentiert (nachbesserung_b1e.md :96) |

## 8. Offen / ungeprueft (alles Laufzeit)

- Ob `pathToLocation` den Baeren beim Spazieren/Zurueckgehen wirklich an die Zielkachel bringt (Attrappe setzt ihn hin); Fussgleiten.
- Ob `setBlockMovement(true)` je Takt den sitzenden Baeren ruhig haelt, ohne den Sitz-Clip der Clients zu stoeren (OBERFLAECHE-Treiber).
- MP: `getObjectListForLua` am Server (A3) -- solange der Suchlauf dort nichts sieht, kommt ein Baer ohne Koerper NICHT von selbst
  wieder (Fehlerzeile "revive: ... has not seen any bear on this server yet"); Unstuck geht. Kevins MP-Test: Server-Log danach durchsehen.
- `tostring(v.u)` mit Zahlen bis ~2e15 unter Kahlua (Schluessel der Namensschild-Datei, OBERFLAECHE).
- Komm her: `comeMaxMs` 30 s und "steckt fest" (followStuckMs 15 s) -- im Spiel ansehen, ob er vor Tueren zu frueh aufgibt.
- Restrisiko C1 wie Call (Plan 4b Nr. 5): steht der Spieler naeher als 25 Kacheln an einer spaet geladenen alten Kopie, bleibt sie bis
  dahin sichtbar (ohne Schild, nie gebunden).

## 9. Fragen fuer Kevin (gebaut wurde der empfohlene Weg)

| # | Frage | gebaut |
|---|---|---|
| K1 | Sitz: wurde er 1,5-3 Kacheln verschoben, geht er einmal zu seiner Stelle zurueck und setzt sich sonst dort, wo er steht? | ja |
| K2 | Mehrspieler: ein Baer ohne Koerper kommt erst von selbst wieder, wenn der Server bewiesen hat, dass er Baeren findet (sonst Gefahr eines Doppels); bis dahin hilft "Unstuck"? | ja |
| K3 | Liegt der echte Koerper ohne Spiegel weit weg (nur ueber seine Tier-Nummer erkennbar), wartet der Baer auf "Unstuck" statt einen zweiten Koerper zu bekommen? | ja |
| K4 | Fuettern im Sitz- oder Frei-Modus verschiebt seine Stelle bzw. den Kreis NICHT (bei Bleiben weiter: Stelle = wo du fuetterst)? | ja |

Statisch geprueft, nicht gespielt.
