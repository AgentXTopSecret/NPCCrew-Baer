# Lauf baer-b1c: PLAN -- Selbstheilung, Laerm, Zombies, Mitfahren, Call to me, Gehen, Markierung, Karte, Anzeige-Optionen (B1c)

Stand 11.11.2026 Nacht. **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2. Verbindlich fuer zwei Bauer (KERN, OBERFLAECHE,
gleichzeitig, getrennte Dateien) und den ZUSAMMENBAU danach. Baut auf dem Staging `_arbeit/baer_zaehmen/mod/` (B1a + B1b + Fix 1-3).
Kurzformen: `FC x.y` = `forschung_b1c.md` Abschnitt x.y; `FB1B` = `forschung_b1b.md`; `PZ x.y` = `PLAN_ZAEHMEN.md`; `PB x.y` =
`PLAN_B1B.md`; `S:` = Staging `mod/42/media/lua/`; `V:` = Vanilla `media/lua/` (42.22.2); `B:` = Bandits `42.22/media/lua/`;
`T:` = Test-Mod `NCBearTest/42/media/lua/`; `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`; `B` = `BanditsNPC.Bear`, `U` = `B.UI`.

Kevins Worte, auf denen der Plan steht (ENT ab "Erster Spieltest B1a", Freigaben "Nachtschicht 11.11.2026" Punkte 1-12, STAND N9):
*"hoe der baer der eben getamed war ist jz nichtmehr getamed"* (N9) -- *"kan ndas sein das der baer weg rennt wegen lauten sounds"* --
*"da stand direkt ein zombie neben den baeren und der ist nicht weg gelaufen"* -- *"der kann nicht ins auto einsteigen wie die npc's ? das
soll der aber koennen ... und genauso wie unstuck button"*, *"sowie unser npc crews"* -- *"wie find ich den ich brauch nen map marker mit
unseren baeren icon"* -- Markierung oben *"wie beim npc crew"*, Symbol *"ich will 1 haben"* -- Anzeige *"namen ein/ausblenden ...
groessen einstellung"* -- *"ja alles so wie du vorgeschlagen hast"* (Freigaben 1-12, darunter `setVariable("animalRunning", false)`).
Alles andere hier ist VORSCHLAG des Planers (Stellwert, Sandbox oder "Fragen fuer Kevin" in 11).

**Nicht zurueckbauen:** Fix 2 (`tHas` in `B.T`), Fix 3 (Streichel-Ton), B1b-Nachbesserung (Folgen mit Vorhalt, `stayR` 12, Drossel je
Ausgang, `B.CleanName` ohne `string.byte`, Regel 10 "Besitzer weg -> haelt und bleibt follow"). Nichts an `T:shared/NCBearFight.lua`,
`NCBear*.lua` des Erwachsenen, Defs (`fleeZombies` bleibt `false`, FC 3.2), Food, Crew, Zeitaktionen, Modell, Textur, Skript.

---

## 0. Entscheidungen des Planers (gelten fuer alle)

**0.1 Identitaet eines Jungen = Kennzeichen `u` (neu), nicht die Kennung `id`.** Jeder Eintrag bekommt beim Anlegen ein eindeutiges
Kennzeichen `u` (Zahl, `getTimestampMs() * 1000 + ZombRand(1000)`, gegen vorhandene Eintraege geprueft). `u` steht im Register UND im
Spiegel. Grund: nach einem Registerverlust beginnt `reg.n` wieder bei 0, und "b1" ist dann ein anderes Tier (Kevins Fall, FC 1.1).
Zusaetzlich traegt das Register eine Epoche `ep` (beim ersten Anlegen gestempelt): nur damit laesst sich "in DIESEM Register geschlossen"
(weitergezogen -> weg) von "Register verloren" (-> wiederherstellen) unterscheiden.

**0.2 Koerper-Generation `gen`.** Jedes Neu-Erzeugen eines Koerpers (Aussteigen, Call to me, Tod-im-Auto) und jedes Einsteigen zaehlt
`rec.gen` um 1 hoch; der Spiegel traegt die `gen` seines Koerpers. Ein Koerper mit kleinerer `gen` als sein Eintrag ist eine VERALTETE
Kopie (aus einem Spielstand vor dem Einsteigen/Herholen, nach Absturz) und wird nie gebunden, sondern unbeobachtet entfernt. Ohne `gen`
gaebe es nach Absturz oder Herholen ein Doppel (FC 0.6, 4.4).

**0.3 Mitfahren und Herholen nur ueber Entfernen + Neu-Erzeugen** (`B.RemoveCub` / `B.CreateCub`, belegt), wie NPC Crew es fuer seine
Figuren macht (FC 4.1). Kein Teleport (`setX/setY` am Tier: kein Beleg), kein Vanilla-Anhaenger (nur Fahrzeuge mit Tier-Anhaenger, FC 4.2).
Neuer, ZWEITER Aufrufer von `B.CreateCub`: `B.PlaceCub` (KERN, `server/BanditsNPCBearRide.lua`). **Name ohne "spawn"** (die Cheat-Pruefung
des Uebernahme-Skripts trifft jeden Namen mit "spawn", `baer_uebernahme.py` CHEAT_NAME) -- also nie "Respawn".

**0.4 Laerm-Flucht wird pro Bild beim Schreiber ERSETZT, nicht gestoppt** (FC 2.3): ein eigener kurzer Ersatzweg (gehend, 1,5 Kacheln) oder
der Folgen-Laufbefehl; die Engine laesst ein Tier, das einen Laerm gemerkt hat und sich bewegt, nicht neu fliehen ("Schild",
`dec/IsoAnimal.java:765-769`). Erkennen: **Stress-Sprung** (`getStress`, belegt; die Engine gibt je Flucht `+radius x 0,05`,
`dec/IsoAnimal.java:799`) als Hauptsignal, dazu "laeuft rennend ohne eigenen Befehl" (`getActionStateName`, `getVariableBoolean`).
Waehrend einer Ruhefrist (`calmMs`) wird die Bewegungssperre nicht erneuert (sie loescht das Schild, FC 0.4). Kein Halt-Verfahren wie
beim grossen Baeren (das brauchte er wegen seiner Clips, FC 2.2). Nur `st == "tame"`; wild/scheu/angefuettert erschrecken weiter.

**0.5 Zombies: Wache im Hirn-Takt, kein eigener Engine-Fluchtweg.** `fleeZombies` bleibt `false` (FC 3.2). Zombies kommen im SP mit Bandits
aus `BanditZombie.CacheLightZ` (Lua-Daten, ohne Banditen), sonst aus `getCell():getZombieList()` (Bandits-belegt) mit Deckel und
rollendem Anfang. Steht ein Zombie nah, rechnet der Hirn-Takt schneller (`zedTickMs` 750 statt 1500) -- kein dritter Takt.

**0.6 Gehen nur beim Folgen und im Laerm-Ersatzweg** (Kevins Wort 11.11.): `animal:setVariable("animalRunning", false)` + `animal:pathToLocation(x, y, z)`
(beide ERLAUBT) nur in `B.MoveTo` mit `opt.walk == true`. Gehen nur, wenn die Reststrecke <= `walkDist` (3) UND der Besitzer langsamer als
`walkSpeed` (0,52 Kacheln/s = Gehen des Platzhalters, FB1B 0.3) ist -- also nur zum Aufschliessen an einen stehenden Besitzer; sonst
rennen wie heute. Damit faellt es heute nie zurueck; mit dem neuen Modell wird nur `walkSpeed` hochgesetzt. Heimweg (Regel 8, > 12 Kacheln)
und Zombie-Flucht rennen weiter.

**0.7 Bildschirm-Markierung und Karte rechnet der CLIENT aus seiner Sicht** (`B.View`): Lage live aus der Client-Kopie des Tiers, sonst die
letzte Kachel aus der Sicht. Dafuer traegt die Sicht neu `x`, `y` (ganze Kacheln) und `ride`; das wilde Junge des Finders steht IMMER in
seiner Sicht (nicht nur in 60 Kacheln). Lage wird nur nachgeschickt, wenn sie sich um >= 3 Kacheln aendert und hoechstens je 5 s.

**0.8 Anzeige-Optionen je Rechner** ueber Vanillas `PZAPI.ModOptions` (Seite `BanditsNPCBear`), nicht Sandbox. Schildgroesse in drei
Schriftstufen (Small / Medium / Large = Schieber 100 / 150 / 200 %), weil `drawTextZoomed` keinen Vanilla-Aufrufer hat (FC 9.3, Frage F8).
Der Zaehm-Balken bleibt immer (Kevin, ENT:236); "Namensschilder aus" blendet die Schilder ALLER gezaehmten Baeren aus (eigene und fremde).

**0.9 Aufteilung:** KERN = `shared/` (ohne Translate) + `server/`; OBERFLAECHE = `client/` (mit `ISUI/` und Bench), alle Texte,
`sandbox-options.txt`, das Bild `42/media/ui/BanditsNPCBearCub_marker.png`. Neue Dateien: KERN 3 (`server/BanditsNPCBearGuard.lua`,
`...Heal.lua`, `...Ride.lua`), OBERFLAECHE 3 (`client/BanditsNPCBearOptions.lua`, `client/ISUI/BanditsNPCBearMarker.lua`,
`client/ISUI/BanditsNPCBearMap.lua`) + Bild. Keine Datei fuer beide.

**0.10 Nicht in B1c:** Zombies greifen an (B5a), Kampf, Wachsen, Werte/Faehigkeiten, Heilen, Schlafen, Baeren-Fenster (V), Inventar, Fischen,
neues Modell, Umbenennen der alten `NCBear*`-Dateien, Stress-Ausgleich (F2), Anhaenger-Luecke (F7), "Call to me" ueber Welt-Menue/Karte (F4),
Hinlaufen zum Auto vor dem Einsteigen (F10).

---

## 1. Verhalten je Auftragspunkt, Schritt fuer Schritt

### 1.1 (Auftrag 1) N9 Register-Selbstheilung -- Ablauf (Regeln im Einzelnen: Abschnitt 2)
1. Jeder Eintrag schreibt seinen Spiegel v2 an sein Tier (`B.WriteMark`): beim Anlegen sofort, bei jedem `B.Commit`, und der Takt prueft
   je Hirn-Takt billig (`markProbe`: `v`, `id`, `u`, `r`), ob er noch stimmt.
2. Geht das Register verloren (Absturz, Kevins Fall): `InitRegistry` legt ein neues Register mit neuer Epoche an. Die ersten 2 Minuten
   (`healWindowMs`) sucht der Hirn-Takt je 15 s (`healScanMs`) nach Jungen (die Zellen laden nach) und der Wald-Wurf wartet so lange
   (sonst bekaeme der Spieler ein neues wildes Junges, bevor sein zahmes zurueck ist).
3. Der Suchlauf (`B.ScanAnimals`) und jedes Anfassen (`B.RecOf`, Fuettern/Streicheln) sehen ein Tier mit Spiegel, aber ohne Eintrag ->
   **wiederherstellen** mit gleichem Zustand, Besitzer, bond, finder, Balken, Zaehlern, Zeiten, Heimat, Modus, Name; Kennung = alte
   Kennung, wenn frei, sonst neu; der Zaehler `reg.n` wird nachgezogen. Nie als "found"/"shy" neu, solange die Regeln es erlauben.
4. Meldung: Fehlerzeile IMMER (`B.Err "heal: entry b1 (tame, owner __sp) restored from the mark on the animal"` -- ein Datenverlust ist ein
   echter Fehler); ist der Besitzer (bzw. bond) da, bekommt er `Note_Back` ("Your bear is back."). Sicht an alle Betroffenen.
5. **Speichern/Laden:** Register und Spiegel werden mit dem Spielstand gespeichert (Register: globale ModData; Spiegel: ModData des Tiers,
   `forschung_engine.md:113`). Nach dem Laden bindet der erste Suchlauf wie in B1a/B1b; ein alter B1a/B1b-Spiegel `{ id, st }` wird beim
   ersten Takt auf v2 geschrieben (Abschnitt 2.6).
6. **Tod:** unveraendert B1a (`B.Close(rec, "dead")`, Sperre). Ein totes Tier wird nie geheilt (Suchlauf nimmt nur `not isDead()`).
7. **Besitzer offline (MP):** Heilung haengt nicht vom Besitzer ab; er bekommt die Meldung nicht, sieht sein Junges aber nach dem Einloggen.
8. **Zweiter Spieler / Fremdmanipulation (MP):** Abschnitt 2.5.
9. **Kevins laufender Spielstand (ehrlich):** dort hat B1a/B1b den alten Spiegel schon mit "b2" ueberschrieben (FC 1.1) -- die Heilung wirkt
   fuer kuenftige Verluste, sie bringt die alte Zaehmung nicht zurueck. Die steht nur im Ordner `..._crash` (Hinweis in 11).

### 1.2 (Auftrag 2) Laerm
1. Jeder geladene, lebende, gezaehmte, nicht mitfahrende Junge steht auf der Wache-Liste `B._calm` (Deckel `calmMax` 8, erneuert im Hirn-Takt).
2. Je Bild (`Events.OnTick`, SP + Server) je Junges: Stress lesen; Sprung >= `noiseStressJump` (0,02) seit dem letzten Bild -> Laerm.
   Sonst: bewegt sich (`getActionStateName` walk/pathfind/followwall, oder idle mit `bPathfind`) UND rennt (`animalRunning`) UND kein eigener
   Befehl laeuft (`s.ownUntil` vorbei) -> fremde Flucht.
3. Antwort SOFORT im selben Bild (`B.CalmAnswer`), an keiner Drossel vorbei ausser dem Deckel 4 Antworten je 2 s (`noiseAnswerMax`/`noiseAnswerWinMs`):
   - Zombie-Wache aktiv -> deren Ziel neu (rennen);
   - folgt und Besitzer da, gleiche Ebene, weiter als `followStart` -> Folgen-Laufbefehl zum Folgen-Ziel (rennen, wie Regel 16);
   - sonst Ersatzweg GEHEND `calmGap` (1,5) Kacheln: Richtung Besitzer (folgt) bzw. Heimat (bleibt), wenn der Anker weiter als `calmGap + 1`
     ist, sonst seitlich (abwechselnd links/rechts) -- nie die eigene Kachel (Ankunft = Schild weg).
   - `s.calmUntil = now + calmMs` (2500): bis dahin setzt `B.Hold` die Sperre nicht neu (kein `stopAllMovementNow`, das Schild bleibt).
4. Ergebnis fuer Kevin: Schuss, Q-Ruf (Akzeptanz < 40), Husten, Zombie am Zaun -> das gezaehmte Junge macht hoechstens einen kleinen Schritt
   und bleibt bei ihm. Q-Ruf mit Akzeptanz >= 40 laesst es (wie Vanilla) zu ihm GEHEN -- das ist kein Fliehen und wird nicht abgefangen
   (kein Stress-Sprung, geht statt zu rennen). Rennen allein macht laut Jar keinen Tier-Laerm (FC 0.2, Frage F9).
5. Rueckfall, falls der Stress am Deckel 100 klebt (dann kein Sprung) und es gerade auf eigenem Laufbefehl rennt: `B.FollowDecide` sieht im
   naechsten Takt, dass der Abstand zum Besitzer um >= `followFleeGrow` (2) gewachsen ist, und schickt sofort neu (Regel 16).
6. Wild/scheu/angefuettert: nichts (Engine-Flucht wie heute). Mitfahrend: kein Koerper, keine Wache.
7. Speichern/Laden, Tod, offline: nichts gespeichert (nur Sitzung). Zweiter Spieler: sein Laerm wird am fremden zahmen Jungen genauso
   abgefangen (die Wache fragt nicht, wer laermt). Stress bleibt (Engine; F2).
8. Diagnose (`B.Log`): je Antwort eine Zeile mit Grund (jump/run) und Art (follow/walk/guard); Zaehler fuer die Bench.

### 1.3 (Auftrag 3) Zombies
1. Hirn-Takt: fuer alle geladenen lebenden Jungen EINE Zombie-Suche (`B.ZedNear`): naechster lebender Nicht-Bandit-Zombie auf gleicher Ebene
   in `zedSense` (12) Kacheln je Junges. Liste je Takt hoechstens `zedScanMax` (1500) Zombies (rollender Anfang).
2. **Gezaehmt, Besitzer da** (gleiche Ebene, nicht im Fahrzeug, Abstand Junges-Besitzer <= `hideOwnerMax` 10) und Zombie <= `zedHide` (6):
   **verstecken** -- Ziel `H = O + (O - Z) / |O - Z| x hideGap` (1,5 Kacheln hinter dem Besitzer, vom Zombie weg); rennen; ist es naeher als
   `hideNear` (1,0) an H: halten. Je Takt neu (Ziel wandert mit Besitzer und Zombie; neuer Befehl nur, wenn H >= `guardRepath` 1,5 wanderte
   oder der letzte >= `guardRenewMs` 3000 alt ist, fruehestens je `guardMoveMs` 800).
3. **Gezaehmt ohne erreichbaren Besitzer** (offline, tot, im Auto, andere Ebene, weiter als 10) oder **wild/scheu/angefuettert**: **fliehen** --
   Ziel `C + (C - Z) / |C - Z| x zedFlee` (10), rennen, je Takt neu solange gefaehrdet.
4. Ende erst, wenn der naechste Zombie weiter als `zedSafe` (9) ist UND das `zedCalmMs` (3000) lang bleibt (Hysterese); bis dahin haelt es an
   seinem Versteck bzw. laeuft nicht neu los. Danach wieder Folgen/Bleiben/B1a-Regeln.
5. Vorrang: die Wache geht vor `B.FollowStep` und `B.Decide` (ein folgendes Junges versteckt sich statt hinterherzurennen).
6. Solange irgendein Junges einen Zombie in `zedSense` hat (`B._hot`), laeuft der Hirn-Takt je `zedTickMs` (750) statt `brainMs`.
7. Meldungen: keine (Kevin sieht es). Diagnose: Zeile bei Beginn/Ende ("guard: b1 hides behind its owner from a zombie at 5.2").
8. Speichern/Laden: nichts gespeichert. Tod durch Zombies gibt es in B1c nicht (greifen nicht an). Zweiter Spieler: ein fremdes zahmes Junges
   versteckt sich hinter SEINEM Besitzer, nie hinter dem zweiten Spieler. Banditen (auch NPC-Crew-Figuren) zaehlen nie als Zombie.
9. Bekannte Grenze: steht der Zombie an der Heimat eines bleibenden Jungen, kann es nach dem Ende heimlaufen und wieder fliehen (F11).

### 1.4 (Auftrag 4) Mitfahren -- Ablauf (Zustandsmaschine: Abschnitt 3)
1. Besitzer steigt in ein Fahrzeug (jede Groesse, auch als Beifahrer; `p:getVehicle()`), Junges gezaehmt, `mode == "follow"`, geladen, und
   hoechstens `BearRideDistance` (Sandbox, Vorgabe **15**, Kevin) Kacheln weg -> im selben Hirn-Takt **Einsteigen**: Junges verschwindet,
   Meldung `Note_RideOn` ("Your cub jumps in with you."). Weiter weg -> wie B1b "Bleiben", Meldung `Note_StayCar` mit NEUEM Text ("Your cub
   was too far away to get in. It waits here.").
2. Waehrend der Fahrt: kein Tier in der Welt; der Eintrag steht `ride` und wandert als "letzte bekannte Stelle" mit dem Besitzer mit.
   Karte: kein Symbol (es ist ja beim Spieler, NC-Lehre). Rechtsklick gibt es nicht (kein Tier). "Call to me" -> `Why_Riding`.
3. Besitzer steigt aus: im SP nach `rideOffMsSP` (1000 ms) zu Fuss, im MP nach `rideOffMsMP` (3000 ms) zu Fuss UND langsamer als `rideSpeedMax`
   (4 Kacheln/s; `getVehicle()` liefert im MP sekundenlang nil waehrend der Fahrt, NC-Lehre FC 4.1) -> freie Kachel 1-3 Kacheln neben ihm
   (`B.SpotNear`, nie unter dem Fahrzeug) -> neues Tier (`B.PlaceCub`), gleicher Eintrag, gleicher Name, gleiche Zaehmung, `mode = "follow"`,
   Meldung `Note_RideOff` ("Your cub hops out."). Kein Platz -> bleibt `ride`, naechster Takt; nach 20 Fehlversuchen eine Fehlerzeile je Minute.
4. **Speichern/Laden waehrend der Fahrt:** `ride` steht im Register; nach dem Laden: Besitzer im Auto -> faehrt weiter mit; zu Fuss -> steigt
   nach `rideOffMs` neben ihm aus. **Absturz:** 3.4.
5. **Besitzer stirbt im Auto:** ist eine tote Figur mit seinem Schluessel da (`B.DeadAt`) und deren Gegend geladen, steigt das Junge nach
   `rideLostMs` (5000) an dieser Stelle aus und wartet dort (`mode = "stay"`). Ist die Gegend schon entladen: bleibt `ride`; die neue Figur
   (SP gleicher Schluessel `__sp`, MP gleicher Kontoname) bekommt es beim ersten Schritt zu Fuss neben sich (F3).
6. **Besitzer meldet sich ab (MP) / Server-Neustart:** `ride` bleibt, nichts erscheint; nach dem Einloggen: im Auto -> faehrt weiter, zu Fuss ->
   steigt neben ihm aus (wie A7: "wartet als follow").
7. **Zweiter Spieler:** im selben Auto zaehlt nur der Besitzer (`rec.owner`). Fremde sehen das Junge verschwinden und neben dem Besitzer
   wieder auftauchen (Server erzeugt, Clients bekommen es ueber das Netz).
8. Nichts geht verloren, nichts verdoppelt: Abschnitt 3.3/3.4.

### 1.5 (Auftrag 5) Unstuck "Call to me"
1. Rechtsklick am eigenen gezaehmten Jungen -> im Untermenue (bei Follow/Stay/Name) **"Call to me"**, Tooltip `Menu_CallTip` ("Brings your
   cub right next to you if it is stuck. Works once every %1 minutes."; %1 = Sandbox `BearCallCooldownMinutes`).
2. Grau mit Grund (Vorpruefung beim Client aus der Sicht): im Fahrzeug -> `Why_InCar`; Abklingzeit laeuft -> `Why_CallWait` ("You can call your
   cub again in about %1 min."). Nicht da fuer Fremde, fuer mitfahrende, fuer ungezaehmte.
3. Klick -> `B.Ask(p, "Call", { id })`. Schreiber prueft (Reihenfolge): Eintrag da (`Why_Gone`), Besitzer und `st` tame/missing
   (`Why_NotOwner`), nicht `ride` (`Why_Riding`), Spieler nicht im Fahrzeug (`Why_InCar`), Abklingzeit (`Why_CallWait`, Minuten aufgerundet),
   freie Kachel 1-3 neben dem Spieler auf seiner Ebene (`Why_NoRoom`).
4. Erfolg: altes Tier (falls geladen) ueber `B.RemoveCub`, neues ueber `B.PlaceCub` neben dem Spieler (`gen + 1`), `mode = "follow"`,
   Meldung `Note_Called` ("Here is your cub again."), Abklingzeit startet (nur bei Erfolg). Ist das alte Tier nicht geladen (weit weg),
   wird es beim Wiederauftauchen als veraltete Kopie entfernt (0.2).
5. Abklingzeit **5 Minuten Echtzeit** (Kevin; Sandbox `BearCallCooldownMinutes`, Vorgabe 5, 0..60) je Junges in einer Sitzungs-Tabelle
   (`B._callAt`, nie gespeichert; Uhr rueckwaerts = abgelaufen). Speichern/Laden setzt sie zurueck (Echtzeit-Regel, ehrlich).
6. MP: nur der Server erzeugt/entfernt; gedrosselt ueber `B.AskOk` (Schluessel "Spieler|Call|ok/no"); kein Kick (nur `sendClientCommand`).

### 1.6 (Auftrag 6) Gehen
1. Folgen Regel 16 bekommt `walk`: gehen, wenn Reststrecke Junges -> Ziel <= `walkDist` (3) UND Besitzer-Tempo <= `walkSpeed` (0,52 K/s);
   sonst rennen. Wechselt `walk`, geht SOFORT ein neuer Befehl hinaus (gilt als "Ziel gewandert").
2. Besitzer-Tempo = Weg seit dem letzten Hirn-Takt / echte Zeit seitdem (`B._ppAt`, nicht fest 1,5 s -- der Takt ist bei Zombies schneller).
3. Ergebnis: bleibt Kevin stehen, kommt das Junge die letzten Kacheln gehend heran (kein "Anrennen" bis 0,5 Kacheln, N1); geht/rennt er,
   rennt es wie heute. Stellwerte zur Laufzeit: `NCBear_CubSet("walkDist", 2)`, `("walkSpeed", 1.2)` (neues Modell).

### 1.7 (Auftrag 7) Bildschirm-Markierung oben
1. Nur wenn Bandits geladen ist (Riegel `BanditEventMarkerHandler`, `.set`, `BanditEventMarker`, `BanditUtils`, `BanditUtils.DistTo`).
2. Ziel: das wilde Junge des Spielers = `B.View.me.wild` (Finder = ich, ungebunden, new/shy, nicht "faellig"; Wald ODER Koeder, PZ 4.1).
   Gezeigt, solange `st == "new"` (nicht entdeckt) und noch `markerAfterMs` (60 s) nach dem ersten "shy", das dieser Client sieht.
3. Je `markerMs` (400 ms): `BanditEventMarkerHandler.set("BanditsNPCBearCub", "media/ui/BanditsNPCBearCub_marker.png", 1800, x, y,
   { r = 1.0, g = 0.72, b = 0.30 }, U.T("UI_BN_Bear_Marker_Cub"))` -- gleiche Id = verschieben (B:client/BanditEventMarkerHandler.lua:31-36).
   Lage: live von der Client-Kopie (`U.CubPos(id)`), sonst `c.x + 0.5, c.y + 0.5` aus der Sicht.
4. Aus (`set(..., 0, ...)` genau einmal): gezaehmt/angefuettert (me.wild faellt weg), Eintrag weg, keine Lage, Frist nach "entdeckt" um.
5. Doppelklick (Bandits blendet aus, `BanditEventMarkers.lua:21`) wird respektiert: sieht der Client unseren Marker mit Dauer 0, ohne dass
   wir 0 gesetzt haben, zeigt er ihn fuer DIESES Junge nicht wieder (F6).
6. Ueberlappung mit NPC Crews Ueberlebenden-Pfeil (Bandits merkt EINE Stelle fuer alle, FC 0.8): beim Anlegen unseres Markers, liegt ein
   anderer sichtbarer Marker auf denselben Bildschirm-Koordinaten, unseren um `markerShift` (100 px) nach rechts schieben (0 = aus; F5).
7. MP: aus der Sicht des Clients (Bandits nimmt `getSpecificPlayer(0)`). Geteilter Bildschirm: nur Spieler 1 (Bandits-Grenze).

### 1.8 (Auftrag 8) Karten-Symbol
1. Mini-Karte und grosse Karte (M): je eigenem Baeren ein kleines Symbol (dasselbe Bild). Eigen = `owner == ich` und `st` tame/missing,
   oder `bond == ich` und `st == "fed"` (Kevin: auch das angefuetterte eigene). "ich" wie im Hud (`describeTag`): `me.key`, im SP zaehlt
   `__sp` als eigen (`B.IsSP()`), im MP nie. Mitfahrend: kein Symbol (F14). Fremde: nie.
2. Lage: live (Client-Kopie) mit Alpha 1,0; sonst letzte Kachel aus der Sicht mit Alpha 0,55 ("letzte bekannte Stelle"; vermisst ebenso).
3. Groesse: Mini-Karte `mapMiniPx` 14; grosse Karte nach Zoom wie Vanillas Druckmedien `lerp(mapWorldMin 18, mapWorldMax 28)` ueber
   `getZoomF()` 12..15 (`V:client/ISUI/Maps/ISWorldMap.lua:446-449`). Ausserhalb des Elements: nicht zeichnen.
4. Einhaengen EINMAL (Datei-Ende + `OnGameStart`, je Klasse ein "erledigt"-Merker, nie neu ueber einen fremden Aufsatz -- NC-Lehre
   Stapelueberlauf, FC 8). Geht mit NPC Crews eigenem Aufsatz derselben zwei Methoden zusammen (jeder merkt die vorige Methode).

### 1.9 (Auftrag 9) Anzeige-Optionen je Spieler (Optionen -> Mods)
1. Seite `BanditsNPCBear`, Name `UI_BN_Bear_MO_Page` ("NPC Crew: Bear"), Titel `UI_BN_Bear_MO_Title` ("Display above bears").
2. `TagShow` (TickBox, Vorgabe an): Namensschilder ueber gezaehmten Baeren; Tooltip: der Zaehm-Balken bleibt immer.
3. `TagSize` (Schieber 100..200, Schritt 50, Vorgabe 100): 100 = Small (heute), 150 = Medium, 200 = Large; Balken und Abstaende wachsen mit
   dem Verhaeltnis der Schrifthoehen.
4. Gelesen nur beim Listenbau der Anzeige (hoechstens 1 x/s) ueber EINE Funktion `U.Opt(id, vorgabe)`; fehlt die Seite: Vorgabe.
5. Erweiterbar: spaeter je Wert (Leben, Ausdauer, Hunger, Durst, Muedigkeit) eine `addComboBox` (aus / Balken / Zahl) und "DODGE" als
   TickBox -- die Seite bekommt dafuer schon den Kommentar-Platzhalter, nichts davon wird jetzt angelegt.
6. MP: je Client; der Server kennt die Seite nicht und braucht sie nicht.

### 1.10 (Auftrag 10) Kleinkram
- ES `UI_BN_Bear_Hud_Pet`: "Caricias: %1" -> **"Caricia: %1"** (passt zu "lista"). FR ("Caresses : %1" / "prêt") bleibt (Plural ist dort
  ueblich, FC 10) -- nur ES aendern.
- **N1** (Anrennen beim Stehenbleiben): durch Gehen (1.6) entschaerft; `followLead` bleibt 1,5.
- **N2** (`B.CleanName`): zusaetzlich ablehnen: Privatbereich U+E000-U+F8FF (`"\238\128\128"`..`"\239\163\191"`), U+FFFC-U+FFFD
  (`"\239\191\188"`..`"\239\191\189"`), Ersatzzeichen-Haelften (Zeichen `> "\237\159\191"` UND `< "\238\128\128"`, also U+D800-U+DFFF; als
  ECHTE Ungleichungen, weil eine Haelfte allein kein gueltiges UTF-8-Literal hat), und ein Name, dessen sichtbare Zeichen ALLE
  Kombinationszeichen U+0300-U+036F (`"\204\128"`..`"\205\175"`) sind. Sonst unveraendert (Datei bleibt ASCII).
- **N3** (`B.BuildView`): `pkey ~= nil and (rec.owner == pkey or rec.bond == pkey or ...)`; ein Konto ohne Schluessel bekommt nur Junge in
  `tellDist`.

---

## 2. Register-Selbstheilung im Einzelnen

### 2.1 Register v2 (globale ModData `TrueCompanionsBears`, nur beim Schreiber)
```
R = { v = 2, ep = <Zahl: getTimestampMs() beim ersten Anlegen>, epAt = <Weltstunden beim ersten Anlegen>, n, nb, at, cubs, players, baits }
rec (neu, zusaetzlich zu B1a/B1b) = {
  u = <Zahl, eindeutig>,       -- Kennzeichen des Jungen (0.1); nie aendern
  gen = 0,                     -- Koerper-Generation (0.2)
  r = 0,                       -- Aenderungszaehler, +1 in jedem B.Commit (fuer markProbe)
  ride = nil | { at = <Weltstunden> },   -- faehrt mit (3); nur bei st "tame"
  healed = nil | { at = <Weltstunden>, ep = <Epoche des Spiegels> },   -- Diagnose: wiederhergestellt
}
```
`InitRegistry` (Migration, je Feld eine `B.Err`-Zeile nur bei Unsinn): `v = 2`; `ep`/`epAt` nur setzen, wenn sie fehlen; je Eintrag `u`
nachtragen (`B.NewU`), `gen`/`r` = Zahl oder 0; `ride` muss Tabelle mit Zahl `at` sein UND `st == "tame"` UND `owner` gesetzt, sonst nil
(Junges steht dann ohne Koerper da -> "missing" nach den Fehlversuchen -> "Call to me" holt es). `B._healUntil = getTimestampMs() + healWindowMs`.

### 2.2 Spiegel v2 (`animal:getModData().tcBear`, nur Zahlen/Texte, nil-Felder fehlen)
```
{ v = 2, ep, u, id, nr, gen, r, kind, src, st, finder, bond, owner, tame, fedN, petN, last, feedAt, petAt, born, tamedAt, mode, name, hx, hy, hz }
```
- `B.MarkOf(rec)` baut die Tabelle (ep aus dem Register, `v = B.MARK_V` = 2). Nicht im Spiegel: Lage (das Tier IST die Lage), `aid` (das Tier
  kennt sie selbst), Uhren der Sitzung, `ride`, `idleH`, `goneP`, `miss*`, `hintAt`.
- Schreiben: `B.WriteMark(rec, a)` ersetzt `md[B.MARK]` ganz (kein `isExistInTheWorld`-Riegel, wie `NewRec` B1b). Aufrufer: `B.NewRec`,
  `B.InsertRec`, `B.PlaceCub` (sofort), `B.Commit` (nur wenn das Tier in der Welt ist), `markProbe` (wenn `B.MarkFresh` falsch ist).
- `B.MarkFresh(rec, mark)`: `type(mark) == "table" and mark.v == B.MARK_V and mark.id == rec.id and mark.u == rec.u and mark.r == rec.r`.
- Version: `v` fehlt = v1 (B1a/B1b `{ id, st }`). Kuenftige Felder kommen mit `v = 3`; Leser behandeln unbekannte Felder als nicht da.
- Lesen am Client (`B.ViewOf`) unveraendert ueber `mark.id`.

### 2.3 Heil-Regeln `B.HealFromMark(o, mark, players)` (beim Schreiber; o = lebendes `ncbearcub`, das in dieser Sitzung KEINEM Eintrag als Objekt gehoert)
Rueckgabe: `rec` (gebunden bzw. wiederhergestellt), `"stale"` (veraltete Kopie), `"dup"` (Doppel) oder `nil` (nichts; B1a-Weg beim Anfassen).
1. **v2 mit `u`:**
   a. `rec = B.RecByU(mark.u)` (Schleife ueber hoechstens 64 Eintraege). Gefunden:
      - lebt `B.FindAnimal(rec)` und ist ein anderes Objekt -> `mark.gen < rec.gen` ? `"stale"` : `"dup"`.
      - `mark.gen < rec.gen` -> `"stale"` (z. B. Koerper vor dem Einsteigen/Herholen gespeichert, oder waehrend `ride`).
      - sonst **binden**: `B.Ses(id).obj = o`, `rec.aid = o:getAnimalID()`, `rec.gen = max(rec.gen, mark.gen)`, `rec.ride = nil` (ein Koerper
        ist da), `rec.missN = 0`, `st` missing -> tame (+ `Note_Back`), `B.WriteMark`, `B.Commit`. Rueckgabe rec.
   b. Kein Eintrag mit diesem `u`, aber **Widerspruch per AnimalID**: genau EIN Eintrag ohne lebendes Objekt mit `aid == o:getAnimalID()` in
      40 Kacheln seiner letzten Kachel -> an DEN binden (das Register gewinnt), Spiegel neu, `B.Log("heal: mark of ... did not match, bound to
      its entry by animal id")`. Mehrere -> `nil` (nie raten).
   c. `mark.ep == reg.ep` und `mark.st` new/shy -> `"stale"` (in diesem Register weitergezogen, B1a-Regel bleibt).
   d. sonst **wiederherstellen** `B.Restore(o, mark, players)` (2.4).
2. **v1 (`v` fehlt) -- B1a/B1b-Spiegel:**
   a. `rec = reg.cubs[mark.id]` da und `rec.aid == o:getAnimalID()`: lebt ein anderes Objekt dieses Eintrags -> `"dup"`; sonst binden, Spiegel
      v2 schreiben (Migration).
   b. kein Eintrag, `mark.st` new/shy -> `"stale"` (B1b wie heute).
   c. kein Eintrag, `mark.st == "tame"`, **nur SP** -> `B.Restore` mit `{ st = "tame", owner = B.SP_KEY, tame = 100, fedN =
      B.Opt("BearTameMinFeedings"), src = "found" }` (ein v1-Spiegel kennt sonst nichts).
   d. sonst `nil`.
3. Zaehler nachziehen: jeder v2-Spiegel mit `mark.ep == reg.ep` und `mark.nr > reg.n` -> `B.BumpN(mark.nr)` (auch wenn gebunden).

### 2.4 `B.Restore(o, mark, players)` -- Rueckgabe rec oder nil, why
- Deckel: `B.CountRecs() >= maxRecs` -> nil "full".
- Zustand: `st = mark.st` (missing -> tame; unbekannt -> nil "state").
- Schluessel: SP -> jeder gesetzte `owner`/`bond`/`finder` wird `B.SP_KEY` (es gibt nur einen Spieler). MP -> nur Texte ungleich `B.SP_KEY`,
  sonst nil (bei tame: nicht herstellbar -> nil "nokey").
- Plaetze (`B.SlotsOf(key, now)`):
  - `tame`: `owner` noetig; `slots.bears >= BearMaxPerPlayer` -> nil "cap" (Fehlerzeile).
  - `fed`: `bond` noetig; `slots.bonded ~= nil` oder `slots.bears >= BearMaxPerPlayer` -> nil "cap".
  - `new`/`shy` (nur aus fremder Epoche, 2.3 1c): `st = "shy"`; `finder` bleibt nur, wenn dessen `slots.wild == nil`, sonst nil.
- Kennung: `mark.id` (Text) und frei -> behalten, `B.BumpN(mark.nr)`; sonst `B.NewId()`.
- Felder: alle aus 2.2 geklemmt (`tame` 0..100, Zahlen per `tonumber`, `mode` nur follow/stay, `name` nur durch `B.CleanName`, Heimat nur als
  drei Zahlen), `u = mark.u` (v1: `B.NewU()`), `gen = tonumber(mark.gen) or 0`, `r = 0`, `aid = o:getAnimalID()`, Lage = Kachel von o,
  `idleH = 0`, `missN = 0`, `healed = { at, ep = mark.ep }`. `mode` "follow" ohne anwesenden Besitzer bleibt "follow" (B1b A7).
- `B.InsertRec(rec, o)`; `B.Err("heal: entry " .. id .. " (" .. st .. ", owner " .. tostring(owner) .. ") restored from the mark on the animal")`;
  Besitzer/bond da -> `Note_Back` ("good"). `B.FlushViews` am Ende des Takts (Touch).

### 2.5 Konflikte und Fremdmanipulation (MP)
| Fall | Ergebnis |
|---|---|
| Register leer, Tier mit Spiegel (Kevins Fall) | 2.3 1d / 2c: wiederhergestellt, gleicher Zustand und Besitzer |
| Neues Register hat "b1" (anderes `u`), altes Tier traegt "b1" | 2.4: Wiederherstellung unter NEUER Kennung, `reg.n` nachgezogen |
| Zwei Tiere, gleicher Spiegel (`u`, `gen`) | erstes gebunden, zweites `"dup"` -> unbeobachtet entfernt |
| Tier mit kleinerer `gen` (vor Einsteigen/Herholen gespeichert) | `"stale"` -> unbeobachtet entfernt, nie gebunden |
| Eintrag lebt mit Objekt A, Tier B traegt dessen `u` | B ist `"dup"`/`"stale"` |
| Spiegel geloescht/verfaelscht an einem GEBUNDENEN Tier | Riegel 1 (Objekt der Sitzung) gewinnt; `markProbe` schreibt neu |
| Gefaelschter Spiegel an einem UNGEBUNDENEN Tier, das zu einem Eintrag gehoert | 2.3 1b: AnimalID-Widerspruch bindet an den Eintrag |
| Gefaelschter Spiegel an einem Tier ganz ohne Eintrag (Waise/Fund) | wird hergestellt -- gedeckelt durch `BearMaxPerPlayer`, Fehlerzeile je Heilung (F1) |
| Spiegel nennt ein fremdes/abwesendes Konto | hergestellt fuer DIESES Konto (es bekommt sein Junges beim Einloggen); nie fuer den Heilenden |
| MP-Spiegel mit Besitzer nil / "__sp" | nicht als tame herstellbar (nil) -> B1a-Weg |
- "Unbeobachtet entfernen" = wie Waisen/stale (B1b Riegel 3 ohne Alters-Frist): niemand naeher als `vanishKeep` (25) und im SP keiner sieht hin;
  sonst bleibt das Tier ungebunden stehen (kein Schild, Menue lehnt ab: `B.RecOf` gibt nil "stale"/"dup" -> `Why_Gone`), naechster Suchlauf.
- Ein Junges ohne Spiegel bleibt wie B1b (Waise nach Riegel 1-3).

### 2.6 Wo geheilt wird
- `B.ScanAnimals(players, force)` (KERN `World.lua`), neue Reihenfolge je Lauf:
  1. je lebendes `ncbearcub`: Riegel 1 (Objekt der Sitzung) -> gebunden, Spiegel reparieren, wenn nicht `B.MarkFresh`; sonst mit Spiegel ->
     Liste `marked` (und `B.BumpN` bei v2 gleicher Epoche); ohne Spiegel -> `loose`.
  2. AnimalID-Rueckfall (B1b) fuer Eintraege ohne lebendes Objekt ueber `loose` UND `marked` -- ein `marked` mit `mark.u` ungleich `rec.u` ist
     KEIN Kandidat.
  3. je verbliebenem `marked`: `B.HealFromMark` -> rec / "stale" / "dup" / nil.
  4. "stale"/"dup" nach dem Durchlauf unbeobachtet entfernen (`B.RemoveCub`, `B.Log`).
  5. Waisen (ohne Spiegel) wie B1b.
  Rueckgabe weiter `n, removed` (removed zaehlt Waisen + stale + dup).
- `B.RecOf(animal)` (Anfassen): Riegel 1; mit Spiegel -> `B.HealFromMark(animal, mark, nil)`: rec -> rec; "stale"/"dup" -> `nil, "stale"`;
  nil -> B1a "found" (NewRec). Ohne Spiegel -> "found". **Ein Doppel wird so nie ein neuer Eintrag** (B1a tat das).
- Takt (KERN `Server.lua`): im Heil-Fenster (`now < B._healUntil`) ein Suchlauf je `healScanMs`, auch ohne Vermisste; Wald-Wurf
  (`forestRolls`) wartet bis zum Ende des Fensters.

---

## 3. Mitfahren und Unstuck im Einzelnen

### 3.1 Zustandsmaschine (nur `st == "tame"`)
```
 follow (Koerper)  --[Besitzer car, d <= BearRideDistance, CubDefOk]-->  riding (kein Koerper, rec.ride)       Note_RideOn
 follow (Koerper)  --[Besitzer car, d > BearRideDistance]---------->  stay (B1b Regel 11)                  Note_StayCar (neuer Text)
 riding            --[Besitzer zu Fuss offMs (+ MP Tempo <= 4), Platz]-> follow (neuer Koerper, gen+1)    Note_RideOff
 riding            --[Besitzer tot (DeadAt), Gegend geladen, lostMs]-->  stay (neuer Koerper am Toten)    -
 riding            --[Besitzer offline / Gegend entladen]---------->  riding (wartet)                       -
 tame/missing      --[Call to me: Besitzer, Abklingzeit, Platz]------>  follow (neuer Koerper, gen+1)    Note_Called
```
Einsteigen (`B.RideBoard`): erst `B.CubDefOk()` (Definition + Rasse da, sonst kommt kein Koerper zurueck -> nicht einsteigen, stay +
`Note_StayCar`, Fehlerzeile); dann `rec.ride = { at = B.Now() }`, `rec.gen = gen + 1`, Lage = Kachel des Besitzers, `B.Commit` (Spiegel wird
nicht geschrieben: kein Koerper mehr), `B.RemoveCub(a)`, Sitzung leeren (`obj`, `f`, `chk`, `held`, `g`), `s.ride = { offMs = nil, lostMs = nil,
failN = 0 }`, Meldung, `B.Log`.

### 3.2 Was im Register steht, was verloren geht
- Register (bleibt): alles aus PZ 4.1 + B1b + `u`, `gen`, `r`, `ride`. Name, Zaehmung, Zaehler, Zeiten, Heimat, Modus bleiben.
- Verloren beim Neu-Erzeugen (Engine-Daten des alten Koerpers): AnimalID (neue Zahl -> `rec.aid` neu), OnlineID (Sicht schickt neu, B1a
  `pushNewSights`), Engine-Stress (neu 0 -- eher gut), **Engine-Akzeptanz** (neu 0: der Q-Ruf holt es danach nicht mehr heran, bis Streicheln sie
  wieder hebt; der Ruf erschreckt es aber auch nicht -- die Laerm-Wache faengt die Flucht ab), Engine-Hunger/-Durst/-Gesundheit (B1c benutzt
  keinen davon; ab B5a/Beduerfnisse gehoeren sie ins Register), Blickrichtung, Wander-Ziel. **Warum ok:** die Wahrheit fuer alles, was der
  Spieler sieht und erarbeitet hat, lebt im Register (PZ 0.1/4.1); die Engine-Werte benutzt B1c nicht.

### 3.3 Sonderfaelle
| Fall | Verhalten | warum nichts verloren/verdoppelt |
|---|---|---|
| Speichern waehrend der Fahrt | `rec.ride` gespeichert, kein Tier in der Zelle | Register = Wahrheit; nach dem Laden weiter (1.4 Schritt 4) |
| Absturz, Register neuer als Zelle (ride gespeichert, alte Zelle haelt noch den Koerper mit gen N-1) | Aussteigen baut gen N+1; der alte Koerper ist "stale" -> entfernt | `gen` (0.2) |
| Absturz, Zelle neuer als Register (Koerper weg, Register ohne ride) | Eintrag ohne Koerper -> "missing" nach 3 Suchlaeufen -> "Call to me" holt es | kein Doppel |
| Absturz, Register aelter, Zelle hat den NEUEN Koerper (gen hoeher) | 2.3 1a: `mark.gen >= rec.gen` -> binden, `gen` und `aid` uebernehmen, `ride` faellt | Spiegel gewinnt nur bei gleicher Identitaet `u` |
| Besitzer stirbt im Auto (SP/MP) | 1.4 Schritt 5 (F3) | - |
| Besitzer meldet sich ab / Neustart | `ride` bleibt | - |
| Kein freier Platz beim Aussteigen | bleibt `ride`, je Takt neu, Fehlerzeile je Minute ab 20 Versuchen | nichts haengt: Spieler kann weitergehen |
| Definition fehlt beim Aussteigen | bleibt `ride`, Fehlerzeile | Eintrag unveraendert |
| Call to me, altes Tier nicht geladen | neues gen+1; altes beim Laden "stale" | `gen` |
| Fremder Spieler im selben Auto | nichts | nur `rec.owner` zaehlt |
| B1a/B1b-Wege ohne Objekt (`resolve`, `countMisses`, `B.FollowLost`, Hud-Suche) | ueberspringen `rec.ride` | sonst "missing" waehrend der Fahrt |

### 3.4 `B.RideStep(rec, players, ms)` je Hirn-Takt fuer jeden Eintrag mit `rec.ride` (vor `resolve`)
1. `o` = naechster anwesender Spieler mit `key == rec.owner`. Fehlt er: `s.ride.lostMs` setzen (erstes Mal); `x, y, z = B.DeadAt(rec.owner)`;
   tot UND `ms - lostMs >= rideLostMs` UND `B.AreaLoaded(x, y)` -> Platz bei (x, y, z) (`B.SpotNear`), `B.PlaceCub(rec, ..., "dead")`, `mode = "stay"`
   (Heimat = Kachel); sonst nichts. Fertig.
2. `lostMs = nil`; `rec.x, rec.y, rec.z` = Kachel des Besitzers (ohne `B.Touch`).
3. `o.car` -> `offMs = nil`, fertig.
4. Zu Fuss: `offMs` nil -> `offMs = ms`, fertig. Noch nicht `rideOffMsSP`/`rideOffMsMP` (MP = `isServer()`) lang -> fertig. MP und Tempo seit dem
   letzten Takt > `rideSpeedMax` -> fertig.
5. `sq = B.SpotNear(o.x, o.y, o.z, rideRing)`; nil -> `failN + 1`, ab `rideFailLog` `B.ErrEvery`; fertig.
6. `B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "ride")` -> gelungen: `rec.ride = nil`, `s.ride = nil`, `B.SetMode(rec, "follow", "ride",
   players)` (keine Meldung von SetMode), `Note_RideOff` an den Besitzer, `B.Log`.

### 3.5 `B.PlaceCub(rec, x, y, z, why)` -- der zweite Weg, ein Tier in die Welt zu setzen (nur Ride.lua)
`a = B.CreateCub(x, y, z)` (nil -> nil, why); `rec.gen = gen + 1`; `rec.aid = a:getAnimalID()`; Sitzung: `obj = a`, `f`/`chk`/`held`/`g` = nil;
`B.WriteMark(rec, a)` SOFORT (Fix-1-Lehre: `isExistInTheWorld` ist im selben Bild falsch); Lage = (x, y, z); `missN = 0`, `missAt = nil`;
`st` missing -> tame, `missH = 0`; `B.Commit(rec)`; `B.Log("place " .. id .. " (" .. why .. ") at ...")`. Rueckgabe a.
Im selben Takt findet `B.FindAnimal` das neue Tier noch nicht (nicht in der Welt) -- `liveRec` ueberspringt es einmal, `resolve` zaehlt einen
harmlosen Fehlversuch (3 noetig), der naechste Takt bindet ueber Riegel 1.

### 3.6 `B.SpotNear(x, y, z, r)` (World.lua)
Ringe 1..r um `floor(x), floor(y)` auf Ebene `floor(z)`, je Ring feste Reihenfolge (8, 16, 24 Kacheln); erste Kachel mit: geladen
(`getGridSquare`), `TreatAsSolidFloor`, kein Wasser, kein Baum, `isFree(false)`, nicht `isVehicleIntersecting`. **Ohne** `isOutside` (im Haus
erlaubt) und **ohne** `B.SeenInSP` (das Junge SOLL sichtbar neben dem Spieler stehen). Hoechstens 48 Kacheln, nur bei Aussteigen/Call.

---

## 4. Markierung, Karten-Symbol, Anzeige-Optionen: Daten, Kosten, Deckel, Riegel

### 4.1 Sicht (KERN liefert, OBERFLAECHE liest)
```
viewEntry(rec, pkey, ms) = { ... B1a/B1b ..., x = rec.x, y = rec.y,           -- ganze Kacheln (letzte bekannte Stelle)
                             ride = true | nil,                            -- faehrt mit
                             callWait = <Sekunden, ganze Zahl> | nil }     -- nur fuer den Besitzer: Rest der Call-Abklingzeit
B.BuildView(player): eigene Eintraege (owner / bond) wie B1b UND das wilde Junge des Finders (finder == pkey, bond nil, new/shy, nicht goneP)
                     immer, gleich wie weit; N3-Riegel pkey ~= nil.
me unveraendert (me.wild = Kennung des wilden Jungen).
```
Lage nachschicken (`liveRec`): hat sich die Kachel gegenueber `s.vx, s.vy` um >= `viewMoveTiles` (3) geaendert UND `ms - s.vAt >= viewMoveMs`
(5000) -> `B.Touch(nil, key)` fuer jeden gesetzten Schluessel aus owner / bond / finder (nur diese Spieler bekommen die neue Sicht), `s.vx,
s.vy, s.vAt` neu. Mitfahrend: nicht (kein Symbol).

### 4.2 Kosten je Bild und Deckel
| Teil | je Bild | seltener | Deckel |
|---|---|---|---|
| Laerm-Wache (Server/SP) | je gezaehmtem Jungen 1 `getStress` + 1 `getActionStateName` (+ 1-2 `getVariableBoolean` nur wenn idle bzw. bewegt) + `isExistInTheWorld`/`isDead` | Antwort selten | `calmMax` 8 Junge, 4 Antworten je 2 s |
| Zombie-Suche (Server/SP) | - | je Hirn-Takt 1 Lauf; SP mit Bandits nur Lua-Tabelle; sonst je Zombie 2 Aufrufe, nahe 2-4 mehr | `zedScanMax` 1500 je Takt |
| Markierung (Client) | - | je 400 ms 1 `set` (+ ggf. 3 Objekt-Aufrufe) | 1 Marker |
| Karte (Client, nur wenn eine Karte offen ist) | je Symbol 2 Umrechnungen + 1 Bild + bis 3 Objekt-Aufrufe | Liste je 500 ms | `BearMaxPerPlayer` (<= 4) + 1 angefuettertes |
| Anzeige-Optionen | - | gelesen beim Listenbau (<= 1 x/s) | - |
| Lage in der Sicht | - | je Junges hoechstens je 5 s an <= 3 Spieler | - |
Kein `getText` je Bild (Texte beim Listenbau bzw. einmal je Sprache zwischengespeichert), keine Tabelle je Bild.

### 4.3 Riegel
- Bandits: Markierung nur mit `BanditEventMarkerHandler and BanditEventMarkerHandler.set and BanditEventMarker and BanditUtils and
  BanditUtils.DistTo`; Zombie-Quellen `BanditZombie.CacheLightZ` (nur `B.IsSP()`), `BanditCompatibility.IsReanimatedForGrappleOnly`,
  `BanditUtils.GetZombieID`/`GetBanditClusterData` je hinter eigenem Existenz-Riegel; ohne Bandits: `getZombieList` und keine Banditen-Frage
  (ohne Bandits gibt es keine Banditen).
- NPC Crew: nichts Neues (die Karte kettet sich hinter/vor NPC Crews Aufsatz, beide merken die vorige Methode).
- Karte: `ISMiniMapInner`/`ISWorldMap` und `.render` muessen da sein; sonst beim `OnGameStart` nochmal (einmal).
- Optionen: `PZAPI and PZAPI.ModOptions and PZAPI.ModOptions.create`; fehlt es -> `B.Err`-Zeile, `U.Opt` gibt Vorgaben.
- Fehler beim Zeichnen: `pcall` NUR um belegte Aufrufe und NIE stumm (`B.ErrEvery("map", 60000, ...)`) -- sonst ein Fehler je Bild.

---

## 5. Stellwerte und Sandbox

### 5.1 Sandbox (Seite `BanditsNPC`; KERN `B.OPTS`, OBERFLAECHE `sandbox-options.txt` + `Sandbox.json` x 7, gleiche Zahlen)
| Name | Typ | min | max | Vorgabe | Bedeutung |
|---|---|---|---|---|---|
| `BanditsNPC.BearRideDistance` | integer | 3 | 40 | **15** (Kevin) | so weit darf ein folgendes Junges beim Einsteigen weg sein |
| `BanditsNPC.BearCallCooldownMinutes` | integer | 0 | 60 | **5** (Kevin) | Echtzeit-Minuten zwischen zwei "Call to me" |
Namen frei (grep NPC Crew `BearRide`/`BearCall`: 0 Treffer, 11.11.). Blockform wie `BearFollowMaxDistance`, vor `BearLog`.

### 5.2 `B.CFG` neu (KERN `shared/BanditsNPCBear.lua`; zur Laufzeit per `NCBear_CubSet`)
| Feld | Vorgabe | Bedeutung |
|---|---|---|
| `healWindowMs` / `healScanMs` | 120000 / 15000 | Heil-Fenster nach `InitRegistry` / Suchlauf darin je |
| `calmMax` / `calmMs` / `calmGap` | 8 / 2500 / 1.5 | Wache-Deckel / Ruhefrist (keine Sperre) / Ersatzweg-Laenge |
| `noiseStressJump` / `noiseAnswerMax` / `noiseAnswerWinMs` | 0.02 / 4 / 2000 | Stress-Sprung je Bild = Laerm / Antworten je Fenster |
| `ownSlackMs` / `ownMaxMs` | 1500 / 15000 | eigener Befehl gilt Wegzeit + so viel, hoechstens so lange |
| `followFleeGrow` | 2.0 | Rueckfall: Abstand zum Besitzer wuchs je Takt so viel -> sofort neu |
| `walkDist` / `walkSpeed` / `runSpeed` | 3 / 0.52 / 2.47 | gehen bis Reststrecke / bis Besitzer-Tempo (K/s) / Tempo fuer die Wegzeit |
| `zedSense` / `zedHide` / `zedSafe` / `zedCalmMs` | 12 / 6 / 9 / 3000 | Suche / Gefahr ab / sicher ab / so lange sicher bis Ende |
| `zedFlee` / `hideGap` / `hideNear` / `hideOwnerMax` | 10 / 1.5 / 1.0 / 10 | Fluchtweite / Versteck hinter dem Besitzer / angekommen / Besitzer hoechstens so weit |
| `zedScanMax` / `zedTickMs` / `zedKeepMs` | 1500 / 750 / 3000 | Zombies je Takt / Hirn-Takt bei Gefahr / letzte Sichtung gilt so lange (rollende Liste) |
| `guardMoveMs` / `guardRepath` / `guardRenewMs` | 800 / 1.5 / 3000 | Wache: fruehester neuer Befehl / Ziel-Wanderung / Auffrischen |
| `rideOffMsSP` / `rideOffMsMP` / `rideSpeedMax` | 1000 / 3000 / 4 | Aussteigen nach / im MP / nur langsamer als (K/s) |
| `rideRing` / `rideLostMs` / `rideFailLog` | 3 / 5000 / 20 | Platz-Ringe / Besitzer tot so lange / Fehlerzeile ab Versuch |
| `callRing` | 3 | Platz-Ringe fuer Call to me |
| `viewMoveTiles` / `viewMoveMs` | 3 / 5000 | Lage in der Sicht nachschicken ab / hoechstens je |
| `markerMs` / `markerAfterMs` / `markerDur` / `markerShift` | 400 / 60000 / 1800 / 100 | Markierung (OBERFLAECHE liest): Takt / nach "entdeckt" noch / Dauer an Bandits / Versatz px (0 = aus) |
| `mapMiniPx` / `mapWorldMin` / `mapWorldMax` / `mapListMs` | 14 / 18 / 28 / 500 | Karte (OBERFLAECHE liest) |
Konstante `B.MARK_V = 2`. Die OBERFLAECHE liest `markerMs` ... `mapListMs` mit eigenem Rueckfall (`tonumber(B.CFG.x) or Vorgabe`).

---

## 6. GENAUE SCHNITTSTELLE (WOERTLICH einhalten; Abweichung sofort nach `schnittstelle_aenderungen.md`, Abschnitt "B1c KERN" / "B1c OBERFLAECHE")

### 6.1 Wer schreibt welche Datei (alles unter `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | Bauer | Was |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | KERN | `B.MARK_V`, `B.CFG` (5.2), `B.OPTS` (5.1) |
| `lua/shared/BanditsNPCBearRules.lua` | KERN | `B.FollowDecide` (Regel 11 ride, `walk`, `followFleeGrow`), `B.GuardDecide`, `B.HideSpot`, `B.CalmSpot`, `B.CleanName` (N2) |
| `lua/server/BanditsNPCBearRegistry.lua` | KERN | Register v2 + Migration, `B.NewU`, `B.NewId`, `B.BumpN`, `B.RecByU`, `B.InsertRec`, `B.NewRec`/`B.Commit`/`B.RecOf` neu, `viewEntry`/`B.BuildView` (4.1, N3) |
| `lua/server/BanditsNPCBearServer.lua` | KERN | `B.Handle` "Call", `WHY_T`, `markProbe`, `liveRec` (Wache, Lage, Wache-Liste), `resolve`/`countMisses` ohne `ride`, `brainTickBody` (Ride-Schritte, Heil-Fenster, Zombie-Suche, `B._ppAt`), `B.BrainTick` (`zedTickMs`), `forestRolls` (Heil-Fenster) |
| `lua/server/BanditsNPCBearWorld.lua` | KERN | `B.MoveTo` (`opt.walk`, `opt.force`, `s.ownUntil`), `B.Hold` (Ruhefrist), `B.SpotNear`, `B.CubDefOk`, `B.DeadAt`, `B.ZedNear`, `B.ScanAnimals` (2.6); Kopf-Kommentar "CreateCub: AppearFor und PlaceCub" |
| `lua/server/BanditsNPCBearFollow.lua` | KERN | `B.FollowStep` (ride, walk), `B.FollowLost` (ohne ride), `B.SetMode` (why "call"/"ride"/"dead" ohne Meldung) |
| `lua/server/BanditsNPCBearGuard.lua` (**neu**) | KERN | Laerm-Wache (`B.CalmWatch`, `B.CalmTick`, `B.CalmAnswer`, OnTick), Zombie-Wache (`B.GuardScan`, `B.GuardStep`) |
| `lua/server/BanditsNPCBearHeal.lua` (**neu**) | KERN | `B.MarkOf`, `B.WriteMark`, `B.MarkFresh`, `B.HealFromMark`, `B.Restore` |
| `lua/server/BanditsNPCBearRide.lua` (**neu**) | KERN | `B.RideBoard`, `B.RideStep`, `B.PlaceCub`, `B.HandleCall`, `B.CallLeft` |
| `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `U.EN` (6.7, wortgleich mit EN/UI.json), `U.NoteSync` merkt `U.viewAt = getTimestampMs()` |
| `lua/client/BanditsNPCBearMenu.lua` | OBERFLAECHE | "Call to me" (`addCall`, `onCall`) |
| `lua/client/BanditsNPCBearOptions.lua` (**neu**) | OBERFLAECHE | Mod-Optionen-Seite (1.9), `U.Opt(id, def)` |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | `wanted` ohne `ride`, Optionen (Zeigen, Groesse), `U.CubPos(id)` |
| `lua/client/ISUI/BanditsNPCBearMarker.lua` (**neu**) | OBERFLAECHE | Bildschirm-Markierung (1.7) |
| `lua/client/ISUI/BanditsNPCBearMap.lua` (**neu**) | OBERFLAECHE | Karten-Symbole (1.8) |
| `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | Bench (6.9) -- wird nie kopiert |
| `lua/shared/Translate/<L>/UI.json` x 7 | OBERFLAECHE | neue/geaenderte Schluessel (6.7), ES `Hud_Pet` |
| `lua/shared/Translate/<L>/Sandbox.json` x 7 | OBERFLAECHE | 2 Optionen + `_tooltip` |
| `sandbox-options.txt` | OBERFLAECHE | 2 Bloecke (5.1) |
| `ui/BanditsNPCBearCub_marker.png` (**neu**) | OBERFLAECHE | Kopie von `_arbeit/baer_icon/BanditsNPCBearCub_marker.png`, byte-gleich (MD5 `9e45e9368ef389aa9b831689d7bd6721`, 4429 Bytes, 96 x 96) |
| `staging_dateien.txt`, `attrappe/gesamt/`, `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt` | ZUSAMMENBAU | 10 |
Unveraendert: `shared/BanditsNPCBearDefs.lua`, `...Food.lua`, `...Crew.lua`, `shared/TimedActions/*`, `IG_UI.json` x 7, Modell, Textur, `nc_bear_cub.txt`.
Kopf jeder neuen Lua-Datei wie PZ 6.1; `server/`-Datei beginnt mit `if isClient() then return end`. Ladefolge server: Follow < Guard < Heal <
Registry < Ride < Server < World (alphabetisch) -> auf Dateiebene nichts Fremdes einfangen, nur zur Laufzeit ueber `B.X`.

### 6.2 Register, Spiegel, Sitzung (KERN)
Register/Spiegel: 2.1, 2.2. Sitzung (nie gespeichert):
```
B._s[id] += { calmUntil, ownUntil, walk, g = { on, mode, safeAt, zx, zy, zAt, tx, ty, orderAt }, ride = { offMs, lostMs, failN }, vx, vy, vAt }
B._calm = { [id] = { a, seen, stress, side, hits = { ms, ... } (<= noiseAnswerMax) } }   B._calmN = Anzahl
B._zed = { [id] = { x, y, d } }     B._zedFrom = Zahl (rollender Anfang)     B._hot = boolean
B._callAt = { [id] = ms } (Deckel 64)     B._healUntil, B._healScanAt, B._ppAt = ms
```

### 6.3 Funktionen des KERNs
shared (`BanditsNPCBearRules.lua`, rein; auch der Client darf rufen):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.FollowDecide(c, o, f, ms)` | `{ act, why, tx, ty, rule, walk }` | wie B1b, dazu: Regel 11 `o.car` und `o.dist <= B.Opt("BearRideDistance")` -> `{ act = "ride", rule = 11 }`, weiter -> `{ act = "stay", why = "car", rule = 11 }`. `o` traegt neu `dt` (ms seit dem letzten Takt; fehlt -> `B.CFG.brainMs`). Regel 16: `walk = (Reststrecke c->Ziel <= walkDist) and (sqrt(mx^2+my^2) / (dt/1000) <= walkSpeed)`; neuer Befehl auch, wenn `f.walk ~= walk`. Rueckfall: `f.lastD ~= nil and d - f.lastD >= followFleeGrow` -> "run" sofort. `f.lastD = d` je Aufruf. |
| `B.GuardDecide(c, o, z, g, ms)` | `{ act, tx, ty, rule, mode }` | `c = { x, y, z, st }`; `o` = Besitzer `{ x, y, z, dist, car }` (nur tame) oder nil; `z = { x, y, d }` oder nil; `g` = Sitzung (fortgeschrieben: `on`, `mode`, `safeAt`, `zx`, `zy`). Regeln: 20 nichts ("none", g aus); 21 verstecken rennen ("hide", tx/ty = `B.HideSpot`); 22 am Versteck halten ("hold"); 23 fliehen ("flee", tx/ty); 24 Nachlauf ("keep": gefaehrdet war, jetzt > zedSafe, noch < zedCalmMs). Gefahr = `z.d <= zedHide`, solange `g.on`: `z.d <= zedSafe`. |
| `B.HideSpot(ox, oy, zx, zy, gap)` | x, y | `O + (O - Z)/|O - Z| x gap`; O == Z -> O + (gap, 0) |
| `B.CalmSpot(cx, cy, ax, ay, gap, side)` | x, y | Anker weiter als gap + 1 -> gap Kacheln Richtung Anker; sonst gap Kacheln quer zur Linie C->A (side 1 / -1); A nil -> quer zur x-Achse |
| `B.CleanName(text)` | wie B1b | + N2 |

server (`BanditsNPCBearHeal.lua`, neu):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.MarkOf(rec)` | Tabelle | 2.2 |
| `B.WriteMark(rec, a)` | - | 2.2; `getModData()` am Tier (belegt) |
| `B.MarkFresh(rec, mark)` | boolean | 2.2 |
| `B.HealFromMark(o, mark, players)` | rec / "stale" / "dup" / nil | 2.3 |
| `B.Restore(o, mark, players)` | rec oder nil, why | 2.4 |

server (`BanditsNPCBearRegistry.lua`):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.NewU()` | Zahl | `getTimestampMs() * 1000 + ZombRand(1000)`, bis zu 8 Versuche gegen `B.RecByU` |
| `B.NewId()` | id, nr | `reg.n + 1`, ueberspringt belegte Kennungen |
| `B.BumpN(nr)` | - | `reg.n = max(reg.n, nr)` (nur Zahlen) |
| `B.RecByU(u)` | rec oder nil | Schleife ueber `reg.cubs` |
| `B.InsertRec(rec, a)` | rec | einfuegen, `B.Ses(id).obj = a`, `B.WriteMark`, `B.Touch` |
| `B.NewRec(src, pkey, animal, x, y, z, now)` | wie B1a | + `u = B.NewU()`, `gen = 0`, `r = 0`, Kennung ueber `B.NewId`, Spiegel ueber `B.WriteMark` |
| `B.Commit(rec)` | - | + `rec.r = r + 1`; Spiegel ueber `B.WriteMark`, wenn das Tier in der Welt ist |
| `B.RecOf(animal)` | rec oder nil, why | 2.6 |
| `B.BuildView(player)` | payload | 4.1, N3 |

server (`BanditsNPCBearWorld.lua`):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.MoveTo(rec, animal, x, y, z, opt)` | boolean | wie B1b; `opt.force == true` ueberspringt `minMs`; `opt.walk == true`: statt `fleeTo(sq)` -> `animal:setVariable("animalRunning", false)` DANN `animal:pathToLocation(gx, gy, gz)` (ganze Zahlen der gewaehlten Kachel, gleiche TURN-/Wasser-Wahl); setzt `s.ownUntil = ms + min(ownMaxMs, Weg / (walk and walkSpeed or runSpeed) x 1000 + ownSlackMs)`, `s.walk = (opt.walk == true)`. Einzige Stelle mit `setVariable("animalRunning"` und `pathToLocation(` |
| `B.Hold(rec, animal, on)` | - | `on == true` und `s.calmUntil` noch nicht um -> NICHTS (kein Engine-Aufruf, `s.held` unveraendert) |
| `B.SpotNear(x, y, z, r)` | Kachel oder nil | 3.6 |
| `B.CubDefOk()` | boolean | `findBreed() ~= nil` |
| `B.DeadAt(key)` | x, y, z oder nil | toter Spieler mit diesem Schluessel (SP: lokale Spieler; MP: `getOnlinePlayers`) |
| `B.ZedNear(points, r, maxN)` | Liste (gleich lang wie points) aus `{ x, y, d }` oder `false`, hot | points = `{ { x, y, z }, ... }`; SP + `BanditZombie.CacheLightZ` -> Lua-Tabelle (x/y/z, ohne Banditen); sonst `getCell():getZombieList()` ab `B._zedFrom`, hoechstens maxN; je Zombie `getX/getY`, nur in r eines Punktes: `getZ` (gleiche ganze Ebene), `isAlive`, kein `IsReanimatedForGrappleOnly`, kein Bandit (SP `getVariableBoolean("Bandit")`, Server `GetBanditClusterData(BanditUtils.GetZombieID(z))[id]`) |
| `B.ScanAnimals(players, force)` | n, removed | 2.6 |

server (`BanditsNPCBearGuard.lua`, neu):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.CalmWatch(rec, a, ms)` | - | aus `liveRec` fuer `st == "tame"` ohne `ride`: `B._calm[id] = { a, seen = ms, ... }` (Deckel `calmMax`; voll -> nicht aufnehmen, `B.ErrEvery` einmal je Minute) |
| `B.CalmTick()` | - | Rumpf des OnTick (1.2 Schritt 2-3); `B._calmN == 0` -> sofort zurueck; Eintraege mit `seen` aelter als 3 x `brainMs`, totem oder nicht mehr vorhandenem Tier fallen heraus; `Events.OnTick.Add(function() B.CalmTick() end)` auf Dateiebene (V:server/Foraging/forageServer.lua:502) |
| `B.CalmAnswer(rec, a, w, ms, why)` | boolean | 1.2 Schritt 3; holt Besitzer ueber `B.Players()` (nur bei Antwort); `B.MoveTo(..., { force = true, walk = ..., watch = false })`; setzt `B.Ses(id).calmUntil`, `w.hits`; `B.Log` |
| `B.GuardScan(live, ms)` | - | `live = { { rec, a, x, y, z }, ... }` -> `B.ZedNear` -> `B._zed[id]`, `B._hot`; Eintraege ohne lebendes Objekt fallen aus `B._zed` |
| `B.GuardStep(rec, a, env, ms, players)` | boolean | baut c/o/z, `B.GuardDecide`, fuehrt aus (hide/flee -> `B.MoveTo` rennend mit `minMs = guardMoveMs`, nur bei Wanderung/Alter; hold -> `B.Hold(true)`; keep -> nichts); true = diesen Takt erledigt (liveRec ruft dann weder FollowStep noch Decide); `B.Log` bei Beginn/Ende |

server (`BanditsNPCBearRide.lua`, neu):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.RideBoard(rec, a, o, players)` | boolean | 3.1; false -> der Aufrufer setzt stay "car" |
| `B.RideStep(rec, players, ms)` | - | 3.4 |
| `B.PlaceCub(rec, x, y, z, why)` | IsoAnimal oder nil, why | 3.5 -- einziger Aufrufer von `B.CreateCub` ausser `B.AppearFor` |
| `B.HandleCall(player, args)` | - | 1.5 Schritt 3-4; Drossel `B.AskOk(pkey .. "|Call|" .. ok/no, ms)`; schickt selbst Meldung und Sicht |
| `B.CallLeft(rec, ms)` | ms (0 = bereit) | aus `B._callAt` und `B.Opt("BearCallCooldownMinutes")`; Uhr rueckwaerts = 0 |

server (Aenderungen in vorhandenen Dateien):
| Stelle | Aenderung |
|---|---|
| `B.Handle` (`Server.lua`) | `if command == "Call" then if B.HandleCall then B.HandleCall(player, args) end return end` |
| `WHY_T` (`Server.lua`) | `UI_BN_Bear_Why_CallWait = "num"` |
| `markProbe` | `if B.MarkFresh and not B.MarkFresh(rec, mark) then B.WriteMark(rec, a) end` |
| `buildEnv` | `env.owner.dt = ms - (B._ppAt or ms)` (0 -> nil) |
| `liveRec` | nach dem Spiegel: Lage nachschicken (4.1); `if rec.st == "tame" and B.CalmWatch then B.CalmWatch(rec, a, ms) end`; VOR dem Folgen-Zweig: `if B.GuardStep and B.GuardStep(rec, a, env, ms, players) then return end` |
| `resolve`, `countMisses` | Eintraege mit `rec.ride` ueberspringen |
| `brainTickBody` | 1. `for rec with ride: B.RideStep`; 2. `resolve` ...; 3. Heil-Fenster-Suchlauf (2.6); 4. Liste `live` (Eintraege mit `B.FindAnimal`) -> `B.GuardScan(live, ms)`; 5. liveRec-Schleife wie bisher; 6. `B._pp` + `B._ppAt = ms` |
| `B.BrainTick` | `if B._hot then every = B.CFG.zedTickMs end` |
| `forestRolls` | `if getTimestampMs() < (B._healUntil or 0) then return end` |
| `B.FollowStep` (`Follow.lua`) | act "ride" -> `if not (B.RideBoard and B.RideBoard(rec, a, env.owner, players)) then B.SetMode(rec, "stay", "car", players) end`; act "run" -> `B.MoveTo(..., { minMs = followMoveMs, watch = false, walk = d.walk })`, bei Erfolg `f.walk = d.walk` |

Neue Felder an `B` (Kern-intern, die Bench darf lesen): `B._calm`, `B._calmN`, `B._zed`, `B._zedFrom`, `B._hot`, `B._callAt`, `B._healUntil`,
`B._healScanAt`, `B._ppAt`, `B.MARK_V`.

### 6.4 Funktionen der OBERFLAECHE (nur unter `U`; an `B` nichts Neues)
| Funktion | Datei | Bemerkung |
|---|---|---|
| `U.Opt(id, def)` | Options.lua | Wert der Seite `BanditsNPCBear` (`PZAPI.ModOptions:getOptions(PAGE):getOption(id):getValue()`); nil/Seite fehlt -> def; zwischengespeichert 1 s |
| `U.CubPos(id)` | Hud.lua | x, y, z der lebenden Client-Kopie aus `S.objs` oder nil (3 Engine-Aufrufe) |
| `U.MarkerTick()` | Marker.lua | Rumpf des `Events.OnTick` (Client, V:client/Chat/ISChat.lua:943), gedrosselt auf `markerMs` |
| `U.MapInstall()` | Map.lua | einhaengen (einmal je Klasse); Datei-Ende + `OnGameStart` |
| Menue lokal `addCall`, `onCall` | Menu.lua | 1.5; `onCall` -> `B.Ask(playerObj, "Call", { id = v.id })`; Restzeit = `v.callWait x 1000 - (now - U.viewAt)` |
| Hud lokal | Hud.lua | `wanted(c)`: `c.ride ~= true`; `rebuild`: `U.Opt("TagShow", true)` (aus -> keine Schilder, Balken bleiben), `U.Opt("TagSize", 100)` -> Schrift (< 125 Small, < 175 Medium, sonst Large), Hoehe einmal je Schrift holen, Balken x Verhaeltnis |
Die OBERFLAECHE ruft vom KERN nur: `B.Ask`, `B.View` (`cubs[id].x/y/ride/callWait/st/owner/bond`, `me.wild`, `me.key`), `B.CFG`, `B.Opt`,
`B.ModeOf`, `B.PlayerKey`, `B.SP_KEY`, `B.IsSP`, `B.T`; Bench zusaetzlich (nur SP) `B.Reg`, `B._s`, `B._calm`, `B._zed`, `B._callAt`,
`B.ScanAnimals`, `B.MarkOf`, `B.FindAnimal`, `B.NearestRec`, `B.CallLeft`.

### 6.5 Befehle (Modul `BanditsNPCBear`, Ergaenzung zu PZ 6.2.6 / PB 5.5)
| Richtung | Befehl | Felder | Antwort |
|---|---|---|---|
| Client -> Schreiber | `Call` | `{ id = Text }` | `Note` (`Note_Called` / `Why_*`) + `Sync` |
Nie eine leere Tabelle schicken. `Note` `Why_CallWait`: `t = "num"`, `v` = Minuten (ganze Zahl, aufgerundet, mindestens 1).

### 6.6 Sicht (KERN schreibt, OBERFLAECHE liest): 4.1. `B.ApplySync` kopiert die neuen flachen Felder von selbst (`copyFlat`).

### 6.7 Texte (OBERFLAECHE schreibt alle sieben Sprachen; KERN benutzt nur diese Schluessel)
Vom KERN benutzt (neu): `UI_BN_Bear_Note_RideOn` (Your cub jumps in with you.) - `Note_RideOff` (Your cub hops out.) - `Note_Called`
(Here is your cub again.) - `Why_CallWait` (You can call your cub again in about %1 min.) - `Why_Riding` (Your cub is riding with you.) -
`Why_NoRoom` (There is no free spot next to you.). Geaendert: `Note_StayCar` -> "Your cub was too far away to get in. It waits here.".
Weiter benutzt: `Note_Back`, `Why_InCar`, `Why_NotOwner`, `Why_Gone`.
Nur OBERFLAECHE (neu): `Menu_Call` (Call to me) - `Menu_CallTip` (Brings your cub right next to you if it is stuck. Works once every %1
minutes.) - `Marker_Cub` (Bear cub nearby) (Kevin) - `MO_Page` (NPC Crew: Bear) - `MO_Title` (Display above bears) - `MO_TagShow` (Show
name tags above tamed bears) - `MO_TagShowTip` (Name and state. The taming bar always shows.) - `MO_TagSize` (Size of the display above
bears (%)) - `MO_TagSizeTip` (100, 150 or 200.). Geaendert: `Menu_FollowTip` -> "It runs after you and rides along in vehicles. If you get
too far ahead, it waits.". ES `Hud_Pet` -> "Caricia: %1".
Sandbox: `Sandbox_BanditsNPC_BearRideDistance` (Bear: ride-along distance), `..._tooltip` (Tiles. A following cub gets into the vehicle with
its owner if it is at most this far away.); `Sandbox_BanditsNPC_BearCallCooldownMinutes` (Bear: Call to me cooldown), `..._tooltip`
(Real-time minutes between two uses of Call to me on the same cub.).
Regeln wie PB 6.2: alle sieben `UI.json`, gleiche Platzhalter, sortiert, Round-Trip `json.dumps(data, indent=4, ensure_ascii=False) + "\n"`,
UTF-8 ohne BOM, LF; CN nur Zeichen aus Vanilla-CN (`ober_werkzeug/texte.py`); `U.EN` wortgleich; keine Woerter spawn/debug/bench/cheat/test;
Menue-Eintraege nur ueber `U.T(...)`; Mod-Optionen bekommen SCHLUESSEL (Vanilla ruft `getText`, `V:client/OptionScreens/MainOptions.lua:2810-2812`).

### 6.8 Mod-Optionen (OBERFLAECHE, `client/BanditsNPCBearOptions.lua`, auf Dateiebene, Existenz-Riegel, KEIN pcall um das Anlegen)
```
PAGE = "BanditsNPCBear"
o = PZAPI.ModOptions:create(PAGE, "UI_BN_Bear_MO_Page")
o:addTitle("UI_BN_Bear_MO_Title")
o:addTickBox("TagShow", "UI_BN_Bear_MO_TagShow", true, "UI_BN_Bear_MO_TagShowTip")
o:addSlider("TagSize", "UI_BN_Bear_MO_TagSize", 100, 200, 50, 100, "UI_BN_Bear_MO_TagSizeTip")
-- spaeter (nicht anlegen): je Wert addComboBox(id, name, tip) + addItem("...Off"/"...Bar"/"...Number"), "DODGE" als addTickBox
```

### 6.9 Bench (`client/NCBearBenchCub.lua`, OBERFLAECHE, nur SP, wird nie kopiert)
| Befehl | Tut |
|---|---|
| `NCBear_CubForget()` | Eintrag meines naechsten zahmen Jungen aus dem Register loeschen, Spiegel BLEIBT (N9 nachstellen); `B._s[id] = nil`; druckt "entry removed, mark kept -- wait up to 2 min or NCBear_CubSweep()" |
| `NCBear_CubMark()` | Spiegel meines naechsten Jungen drucken (alle Felder) und `B.MarkFresh` |
| `NCBear_CubCalm()` | Wache: beobachtete Junge, je Junges Stress, letzte Antwort (Grund, Art, Alter), Antworten gesamt |
| `NCBear_CubGuard()` | naechster Zombie je Junges (`B._zed`), Wache an/aus, Modus, `B._hot` |
| `NCBear_CubRide()` | `ride`, `gen`, Sitzung (`offMs`, `lostMs`, `failN`), Besitzer im Fahrzeug |
| `NCBear_CubCallReset()` | `B._callAt` leeren |
| `NCBear_CubInfo()` | zusaetzlich `u`, `gen`, `r`, `ride`, `healed` je Eintrag; Register `ep`/`v` |
| `NCBear_CubSet` | Hilfetext nennt die neuen Felder (5.2) |
Rechtsklick "NC Bear": "Cub: forget entry (keep mark)", "Cub: reset call cooldown" (englische Literale, nur Bench).

---

## 7. Tests

### 7.1 KERN-Attrappe (`attrappe/b1c_kern/run.lua`, neu; die bestehenden `kern/`, `b1b_kern/`, `gesamt/` muessen gruen bleiben; gewollt
geaenderte Erwartungen -- B1b Regel 11 "Auto -> Bleiben" nur noch ueber 15 Kacheln, `Note_StayCar`-Fall -- im Bericht einzeln begruenden)
Tier-Attrappe zaehlt `getStress`, `getActionStateName`, `getVariableBoolean`, `setVariable`, `pathToLocation`, `fleeTo`, `setBlockMovement`,
`getModData`, `remove`; Zellen-Attrappe `getZombieList`; Bandits-Attrappe `BanditZombie.CacheLightZ`, `GetBanditClusterData`, `BanditUtils.GetZombieID`.
1. **Heilung:** (a) SP: Register leer + Tier mit v2-Spiegel tame (Name "Bruno", follow) -> gleiche Kennung, tame, `__sp`, Name, follow, 1 Fehlerzeile,
   `Note_Back`; (b) neues Register mit "b1" (anderes `u`) + altes Tier "b1" -> neue Kennung, `reg.n` nachgezogen, nie zwei "b1"; (c) `mark.nr 7`,
   `reg.n 3` -> 7; (d) zwei Tiere gleiches `u`/`gen` -> eins gebunden, eins "dup", entfernt nur ohne Spieler in 25 und ohne Sicht; (e) `mark.gen <
   rec.gen` -> "stale", nie gebunden; (f) v1 tame ohne Eintrag: SP hergestellt (100), MP nil; (g) v1 new/shy ohne Eintrag -> stale (B1b);
   (h) v2 gleiche Epoche shy ohne Eintrag -> stale; fremde Epoche -> shy, finder nur bei freiem Platz; (i) Besitzer hat schon `BearMaxPerPlayer`
   Baeren -> nil, Tier bleibt, nie entfernt; (j) MP Besitzer nil / "__sp" -> nil; (k) AnimalID-Widerspruch bindet an den Eintrag; (l) `B.RecOf` an
   ungebundenem Tier mit Spiegel -> Heilung statt "found"; Doppel -> nil "dup" (kein neuer Eintrag); (m) Migration B1b-Register (ohne u/gen/r)
   + v1-Spiegel -> gebunden, `markProbe` schreibt v2; (n) `markProbe` schreibt nur bei abweichendem v/id/u/r (Zaehler `WriteMark`); (o) Heil-Fenster:
   Suchlauf je 15 s fuer 2 min, `forestRolls` ruft in der Zeit kein `B.AppearFor`; (p) Spiegel enthaelt nur Zahl/Text/Wahrheitswert.
2. **Laerm:** (a) gehaltenes zahmes Junges, Stress +1,0 -> im SELBEN Tick `setVariable("animalRunning", false)` dann `pathToLocation` (ganze Zahlen),
   Ziel >= 1,4 Kacheln weg, nie die eigene Kachel; `calmUntil` gesetzt; `B.Hold(true)` waehrend der Frist ohne `setBlockMovement`, danach wieder;
   (b) folgt + Besitzer 8 Kacheln weg + Sprung -> `fleeTo` (rennen) zum Folgen-Ziel trotz `followMoveMs`; (c) eigener Lauf aktiv, kein Sprung ->
   keine Antwort; (d) bewegt + rennt ohne eigenen Befehl -> Antwort; gehend (Wandern/Q-Ruf) -> keine; (e) shy/fed/new -> nie; (f) 10 Spruenge in 1 s ->
   4 Antworten; (g) Tier entfernt (mitfahrend) -> faellt aus der Liste; (h) Kosten: je Tick und Junges <= 4 Engine-Aufrufe, > 8 zahme -> 8 beobachtet;
   (i) Stress 100 (kein Sprung) + Abstand +2,5 je Takt -> `FollowDecide` "run" sofort.
3. **Zombies:** (a) Besitzer 3 Kacheln, Zombie 5 vom Jungen -> Ziel auf der zombie-abgewandten Seite (Skalarprodukt < 0), 1,5 vom Besitzer, rennen;
   dort -> halten; (b) Besitzer 12 weg -> fliehen 10; (c) Besitzer im Auto / andere Ebene / offline -> fliehen; (d) shy -> fliehen, fed -> fliehen;
   (e) Hysterese 6/9 + 3 s; (f) Bandit, toter Zombie, andere Ebene -> nie; (g) 2000 Zombies -> 1500 je Takt, rollend; (h) SP mit `CacheLightZ` ->
   kein `getZombieList`; (i) Wache vor FollowStep und Decide; (j) `B._hot` -> Hirn-Takt 750 ms, ohne -> 1500.
4. **Mitfahren:** (a) follow, Auto, 14,9 -> `RemoveCub` 1 x, `ride`, gen+1, `Note_RideOn`; 15,1 -> stay + neuer `Note_StayCar`; stay-Modus -> nichts;
   `CubDefOk` falsch -> stay; (b) 10 Takte Fahrt: kein "missing", Lage = Besitzer; (c) SP aussteigen nach 1000 ms, MP nach 3000 ms und Tempo <= 4
   (Tempo 10 -> wartet); Kachel nicht unter dem Fahrzeug; gen+1, follow, Spiegel-gen = rec.gen; (d) kein Platz -> bleibt, ab 20 Fehlerzeile;
   (e) Speichern/Laden in der Fahrt: weiter / Aussteigen; (f) Absturz: ride gen 6 + alter Koerper gen 5 -> stale, Aussteigen gen 7, genau ein Tier;
   (g) Besitzer tot (`DeadAt`) 5 s + Gegend geladen -> am Toten, stay; entladen -> bleibt; neue Figur zu Fuss -> neben ihr; (h) MP abgemeldet -> bleibt,
   Einloggen zu Fuss -> neben ihm; (i) Fremder im Auto -> nichts.
5. **Call to me:** (a) Besitzer -> altes `RemoveCub`, neues neben ihm, gen+1, follow, `Note_Called`; (b) zweiter Ruf nach 1 min -> `Why_CallWait` v = 4,
   nach 5 min ok, Sandbox 0 -> nie gesperrt; (c) `ride` -> `Why_Riding`, Auto -> `Why_InCar`, Fremder -> `Why_NotOwner`, voll -> `Why_NoRoom`;
   (d) altes Tier nicht geladen -> neues gen+1, altes spaeter stale; (e) MP ueber die `sendClientCommand`-Liste; Drossel.
6. **Gehen:** Besitzer steht, Rest 2,5 -> walk; Rest 3,5 -> run; Besitzer 2 Kacheln je Takt -> run; walk->run sofort neu; `opt.walk` ruft
   `setVariable` VOR `pathToLocation`, nie `fleeTo`; rennen unveraendert `fleeTo`.
7. **Sicht:** `x`/`y`/`ride`/`callWait`; wildes Junges des Finders in 200 Kacheln trotzdem in seiner Sicht; Lage nur bei >= 3 Kacheln und >= 5 s und
   nur an die Schluessel; N3.
8. **N2:** Privatbereich, U+FFFC/FFFD, Ersatzzeichen-Haelften, nur Kombinationszeichen -> nil; "Bruno", "Brünhild", Kyrillisch, Koreanisch ok.
9. **Dateien:** kein `next(`, kein `%a`; `B.CreateCub(` nur in `B.AppearFor` und `B.PlaceCub`; `setVariable("animalRunning"` und `pathToLocation(`
   nur in `B.MoveTo`; keine Namen/Texte mit spawn/debug/test; LF, ASCII.

### 7.2 OBERFLAECHE-Attrappe (`attrappe/b1c_ober/run.lua`, neu; eigene Kern-Attrappe nach 6.3-6.6, nicht auf den KERN warten)
1. Menue: eigenes Zahmes -> "Call to me" mit Tooltip (Minuten aus Sandbox); `ride` -> fehlt; im Auto -> grau `Why_InCar`; `callWait` 120 vor 10 s ->
   grau "about 2 min" (aufgerundet); Klick -> genau ein `B.Ask("Call", { id })`; fremdes Zahmes / ungezaehmt -> fehlt.
2. Markierung: ohne Bandits -> kein Aufruf, kein Fehler; `me.wild` new -> `set("BanditsNPCBearCub", "media/ui/BanditsNPCBearCub_marker.png", 1800,
   x+0.5, y+0.5, {1.0, 0.72, 0.30}, "Bear cub nearby")` hoechstens je 400 ms; Lage live vor Sicht; shy -> 60 s weiter, dann genau ein `set(..., 0, ...)`;
   gezaehmt/angefuettert/weg -> aus; Doppelklick (Dauer 0 ohne uns) -> fuer dieses Junge nie wieder; neues Junges -> wieder; Versatz um 100 px nur
   beim Anlegen und nur bei Ueberlappung.
3. Karte: einmal eingehaengt (zweiter Install und fremder Aufsatz danach: keine zweite Huelle, kein Kreis); zeichnet nur eigene (tame/missing,
   fed mit bond); `ride` nie; ausserhalb des Elements nie; `worldToUIX/Y` je mit ZWEI Zahlen; `drawTextureScaledAspect(tex, x, y, w, h, a, 1, 1, 1)`;
   Groessen 14 / 18..28; Liste <= je 500 ms; je Bild und Symbol <= 2 Umrechnungen + 1 Bild.
4. Optionen: Seite mit Schluesseln angelegt; Seite fehlt -> Vorgaben; `TagShow` aus -> keine Schilder, Balken bleiben; `TagSize` 150 -> Medium,
   200 -> Large, Balken skaliert; `U.Opt` hoechstens 1 x/s gelesen.
5. Hud: `ride`-Eintraege nie "gewollt" (kein Suchlauf ihretwegen); `U.CubPos` nil ohne lebende Kopie.
6. Texte: sieben Sprachen, Schluessel gezaehlt, Platzhalter gleich, Round-Trip, CN-Zeichen, ES "Caricia: %1", geaenderte `Note_StayCar`/
   `Menu_FollowTip`, `U.EN` == EN.
7. Bench: neue Befehle im MP "singleplayer only"; keine Bench-Funktion ausserhalb `NCBearBenchCub.lua`.
8. Bild: `42/media/ui/BanditsNPCBearCub_marker.png` byte-gleich mit der Quelle (MD5), 96 x 96.

### 7.3 GESAMT (`attrappe/gesamt/run.lua` Abschnitt "18 B1c", ZUSAMMENBAU)
Junges -> gezaehmt -> "Follow me" -> Register leeren (Spiegel bleibt) -> Suchlauf -> gleich wieder da -> Schuss (Stress-Sprung) am zahmen Jungen ->
Ersatzweg, am scheuen nicht -> Zombie naht -> versteckt sich hinter dem Besitzer; Besitzer weit -> flieht -> Besitzer steigt ein (14 Kacheln) ->
weg, `ride` -> Speichern/Laden in der Fahrt -> Aussteigen -> steht daneben (ein Tier) -> "Call to me" -> neben ihm, zweiter Ruf gesperrt ->
Gehen/Rennen -> Markierung an/aus -> Karten-Symbol -> Optionen. Einmal SP, einmal Server + zwei Client-Attrappen (A Besitzer, B fremd).
B1a/B1b-Faelle bleiben gruen.

### 7.4 Kevins Test im Spiel (nach dem Einbau: Spiel neu starten; `bugwatch.py` mitlaufen lassen; Wegwerf-Spielstand, `-debug`; Debug-"Tier
Cheat" AUS; Bandits muss geladen sein; `NCBear_CubLog(true)` fuer die Diagnose)
Einzelspieler:
1. Spielstand mit gezaehmtem Jungen laden (sonst `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`). Erwartet: Mini-Karte und grosse
   Karte (M) zeigen ein kleines Baeren-Symbol am Jungen.
2. Optionen -> Mods -> "NPC Crew: Bear": Namensschilder aus -> Schild weg; an; Groesse 150 und 200 -> Schild groesser. Melden: passt die Groesse?
3. "Follow me", 6 Kacheln weggehen und stehenbleiben. Erwartet: die letzten Kacheln GEHT es heran (rennt nicht in dich hinein). Losgehen: es rennt.
4. Laerm: Waffe abfeuern, mit Q rufen, rennen, husten. Erwartet: das gezaehmte Junge rennt NICHT weg (hoechstens ein kleiner Schritt).
   (Nachbesserung B1c B6: "Q holt es heran" gilt nur beim FOLGEN -- ein BLEIBENDES Junges kommt auf Q im Einzelspieler nicht, die Engine
   laesst es nach einem eigenen Rennbefehl rennend kommen, und das wird als Flucht ersetzt. Bitte sagen, ob Q auch beim Bleiben holen soll.
   B5: auch nach vielen Schuessen hintereinander -- Stress am Deckel -- soll ein FOLGENDES Junges nicht mehr wegrennen.)
   `NCBear_CubCalm()` zeigt die Antworten. Zum Vergleich ein wildes Junges (`NCBear_CubClean()`, `NCBear_CubHere(12)`): flieht beim Schuss weiter.
5. Zombie: einen Zombie herankommen lassen. Erwartet: das Junge stellt sich hinter dich (dem Zombie abgewandt). Dann 15 Kacheln vom Jungen
   weggehen ("Stay here" vorher) und einen Zombie zum Jungen locken: es flieht vom Zombie weg. `NCBear_CubGuard()` zeigt den Zustand.
6. Auto: "Follow me", in 10 Kacheln Abstand in ein Auto steigen. Erwartet: "Your cub jumps in with you.", Junges weg, kein Karten-Symbol.
   200 Kacheln fahren, aussteigen. Erwartet: nach ~1 s "Your cub hops out.", es steht neben dir, gleicher Name, folgt. Zum Vergleich 20 Kacheln
   Abstand beim Einsteigen: "too far away to get in", es wartet.
7. Im Auto speichern, Hauptmenue, laden, aussteigen. Erwartet: das Junge kommt, und es gibt genau EIN Junges (`NCBear_CubInfo()`).
8. "Call to me": "Stay here", 30 Kacheln weggehen, Junges rechtsklicken (es muss im Bild sein) -> "Call to me". Erwartet: es steht neben dir,
   folgt. Sofort nochmal: grau "about 5 min". (Nachbesserung B1c B2: neben einer Hauswand oder einem Zaun stehen und rufen -- es darf nie
   im Haus oder hinter dem Zaun landen; zwei Rufe (Sandbox-Abklingzeit 0) nehmen verschiedene Kacheln. Ebenso beim Aussteigen am Zaun.)
9. Selbstheilung: `NCBear_CubForget()`. Erwartet: nach bis zu 2 Minuten (oder sofort mit `NCBear_CubSweep()`) in der Konsole
   `[TC-BEAR] *** heal: entry ... restored`, Meldung "Your bear is back.", gleicher Name, gleicher Zustand (`NCBear_CubInfo()`).
10. Markierung: `NCBear_CubClean()`, `NCBear_CubHere(40)`. Erwartet: oben ein orangener Kreis mit dem Baeren-Kopf, Pfeil in die Richtung,
    "Bear cub nearby". Hingehen; nach dem Entdecken noch ~1 Minute, dann weg. Doppelklick blendet ihn aus (kommt fuer dieses Junge nicht wieder).
11. `NCBear_CubKill()` am Jungen. Erwartet: wie B1b, Symbol weg, keine roten Fehler.
Mehrspieler (dedizierter Server, Rolle user, Spieler A und B; Sandbox Abklingzeiten 0):
1. Server startet ohne Fehler, beide verbinden, kein Kick.
2. A zaehmt (ueber die Sandbox schnell), "Follow me", steigt ein: beide sehen das Junge verschwinden; A faehrt, steigt aus: beide sehen es neben
   A; B sieht "belongs to A".
3. A meldet sich IM Auto ab, meldet sich an, steigt aus: das Junge kommt, genau eins. Server-Neustart waehrend der Fahrt: ebenso.
4. B schiesst neben A's Junges: es flieht nicht. B's wildes Junges flieht.
5. Zombie bei A's Jungen: es versteckt sich hinter A, nie hinter B.
6. B: Rechtsklick auf A's Junges -> kein "Call to me". A: "Call to me" klappt, zweiter Ruf gesperrt.
7. Karte: A sieht sein Symbol, B sieht A's Junges NICHT auf der Karte. Markierung: jeder nur fuer sein wildes Junges.
8. Server-Log nach `[TC-BEAR] ***` durchsehen (A3: `getObjectListForLua`/`getAnimalID` am Server; `getZombieList` am Server; Nachbesserung
   B1c A2: `calm tick:` -- am Server laufen nur Stress-Sprung und "weg vom eigenen Ziel"; Heil-Suchlauf, Heilung, Aussteigen und "Call to me"
   haengen an `getObjectListForLua`/`getAnimalID`).

---

## 8. Belege: jeder geplante Engine-Aufruf (aus `forschung_b1c.md`; der Bauer liest die Stelle selbst nach und nennt sie im Kommentar)
| Nr | Aufruf | Beleg (gleiche Argumenttypen) | Seite | Wer |
|---|---|---|---|---|
| 1 | `a:getModData()` lesen/schreiben (Spiegel v2) | `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127`, `V:shared/Definitions/animal/ButcheringUtil.lua:596` (FC 1.2) | Schreiber | KERN |
| 2 | `getTimestampMs()` (ep, u, Uhren) | `V:server/Foraging/forageServer.lua:456` | alle | beide |
| 3 | `ZombRand(n)` (u, Seite) | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25` | Schreiber | KERN |
| 4 | `a:getAnimalID()` (Neu-Binden) | `V:client/ISUI/Animal/ISAnimalUI.lua:53` (MP-Server unbelegt, A3) | Schreiber | KERN |
| 5 | `Events.OnTick.Add(f)` | Server `V:server/Foraging/forageServer.lua:502`; Client `V:client/Chat/ISChat.lua:943` | beide | beide |
| 6 | `a:getActionStateName()` | `B:shared/ZombieActions/ZASmack.lua:486` (am Tier `T:shared/NCBearFight.lua:1099`) | Schreiber | KERN |
| 7 | `a:getVariableBoolean("bPathfind")` | `B:shared/ZombieActions/ZAMove.lua:61` | Schreiber | KERN |
| 8 | `a:getVariableBoolean("animalRunning")` | Methode `B:shared/ZombieActions/ZAMove.lua:61`; Gleichheit Name/Kennung nur Jar (FC 2.3) -> nur Zusatzsignal | Schreiber | KERN |
| 9 | `a:getStress()` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:17` | Schreiber | KERN |
| 10 | `a:setVariable("animalRunning", false)` | **ERLAUBT** Kevin 11.11. (`ENT:282`); Methode `V:shared/TimedActions/Animals/ISMilkAnimal.lua:139`, `ISPetAnimal.lua:37`, `B:shared/ZombieActions/ZAMove.lua:32`, am Tier `T:shared/NCBearFight.lua:457`, `:1064` | Schreiber | KERN |
| 11 | `a:pathToLocation(x, y, z)` (ganze Zahlen) | **ERLAUBT** Kevin 08.11. (`forschung_engine.md:627`) | Schreiber | KERN |
| 12 | `a:fleeTo(sq)` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38` | Schreiber | KERN |
| 13 | `a:getBehavior():setBlockMovement(b)` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:36`, `V:client/ISUI/Animal/ISAnimalContextMenu.lua:89` | Schreiber | KERN |
| 14 | `getCell():getZombieList()`, `:size()`, `:get(i)` | `B:server/BanditSave.lua:46-48` (SP+Server), `:15`, `B:server/BanditServerZombie.lua:15`, `B:client/BanditZombie.lua:110` | SP + Server | KERN |
| 15 | `z:getX()/getY()/getZ()` | `B:client/BanditZombie.lua:69-71` | beide | KERN |
| 16 | `z:isAlive()` | `B:server/BanditSave.lua:52` | beide | KERN |
| 17 | `z:getVariableBoolean("Bandit")` (SP) | `B:client/BanditZombie.lua:74` | SP | KERN |
| 18 | `BanditUtils.GetZombieID(z)`, `GetBanditClusterData(id)` (Server, Bandits-Lua, Riegel) | `B:server/BanditSave.lua:55-56` | Server | KERN |
| 19 | `BanditCompatibility.IsReanimatedForGrappleOnly(z)` (Bandits-Lua, Riegel) | `B:shared/BanditCompatibility.lua:187-189`, gerufen `B:client/BanditZombie.lua:118` | beide | KERN |
| 20 | `BanditZombie.CacheLightZ` (Lua-Daten, SP) | `B:client/BanditZombie.lua:12`, `:60-87` | SP | KERN |
| 21 | `p:getVehicle()` | `V:server/Vehicles/VehicleCommands.lua:11`, `V:client/ISUI/Hutch/ISHutchMenu.lua:8` | beide | beide |
| 22 | `getOnlinePlayers()`, `:size()`, `:get(i)`, `p:isDead()`, `p:getUsername()`, `getNumActivePlayers()`, `getSpecificPlayer(i)` (`B.DeadAt`) | wie `B.Players` (`S:server/BanditsNPCBearWorld.lua:26-33`) | Schreiber | KERN |
| 23 | `B.CreateCub` = `addAnimal(...)` + `addToWorld()`; `AnimalDefinitions.getDef`, `def:getBreedByName` | `V:server/ClientCommands.lua:808-810`, `V:client/DebugUIs/DebugContextMenu.lua:1460-1467` (unveraendert) | Schreiber | KERN |
| 24 | `B.RemoveCub` = `setBlockMovement(false)`, `remove()`, `removeAnimal(getOnlineID())` | wie B1b (`V:shared/Definitions/animal/ButcheringUtil.lua:609-614`) | Schreiber | KERN |
| 25 | `getCell():getGridSquare`, `TreatAsSolidFloor`, `getFloor():hasProperty(IsoFlagType.water)`, `HasTree`, `isFree(false)`, `isVehicleIntersecting` (`B.SpotNear`) | wie `B.SquareFits` (`S:server/BanditsNPCBearWorld.lua:86-106`) | Schreiber | KERN |
| 26 | `sq:getX()/getY()/getZ()` (Kachel -> Zahlen) | `V:client/DebugUIs/DebugContextMenu.lua:1128` (`square:getX()`) | Schreiber | KERN |
| 27 | `BanditEventMarkerHandler.set(id, icon, dauer, x, y, farbe, text)` | `B:client/BanditEventMarkerHandler.lua:6-38` | Client | OBERFLAECHE |
| 28 | `BanditEventMarkerHandler.markers[id]`, `marker:getDuration()`, `marker.x/.y`, `marker:setX(n)` (Versatz) | Bandits-Lua `B:client/BanditEventMarkers.lua:142` (getDuration), `:103` (`self:setX(self.x + dx)`), `:235-236` (x/y) | Client | OBERFLAECHE |
| 29 | `getTexture(pfad)` | `V:client/ISUI/Maps/ISMap.lua:573`; `B:client/BanditEventMarkers.lua:259` | Client | OBERFLAECHE |
| 30 | `ISMiniMapInner.render` / `ISWorldMap.render` umwickeln, `self.mapAPI` | `V:client/ISUI/Maps/ISMiniMap.lua:4`, `:190-193`; `V:client/ISUI/Maps/ISWorldMap.lua:384` | Client | OBERFLAECHE |
| 31 | `self.mapAPI:worldToUIX(x, y)` / `worldToUIY(x, y)` | `V:client/ISUI/Maps/ISWorldMap.lua:478-479`, `V:client/ISUI/Maps/ISWorldMapSymbols.lua:347` | Client | OBERFLAECHE |
| 32 | `self.mapAPI:getZoomF()` | `V:client/ISUI/Maps/ISWorldMap.lua:447` | Client | OBERFLAECHE |
| 33 | `self:drawTextureScaledAspect(tex, x, y, w, h, a, r, g, b)`, `self:getWidth()/getHeight()` | `V:client/ISUI/Maps/ISWorldMap.lua:482`; Signatur `V:client/ISUI/ISUIElement.lua:1065` | Client | OBERFLAECHE |
| 34 | `PZAPI.ModOptions:create(id, name)`, `:addTitle`, `:addTickBox(id, name, wert, tip)`, `:addSlider(id, name, min, max, schritt, wert, tip)`, `:getOptions(id)`, `:getOption(id)`, `:getValue()` | `V:client/PZAPI/ModOptions.lua:28`, `:64`, `:206`, `:247-257` | Client | OBERFLAECHE |
| 35 | `drawTextCentre(..., UIFont.Medium)` / `(..., UIFont.Large)`; `getTextManager():getFontHeight(UIFont.Medium/Large)` | `V:client/ISUI/ISFitnessUI.lua:204`; `V:client/Chat/ISAlert.lua:35`; `V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8`, `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6` | Client | OBERFLAECHE |
| 36 | Menue/Sicht wie B1b (`addOption`, `notAvailable`, `addToolTip`, `B.Ask` -> `sendClientCommand`) | PB 9 Nr. 12, 15 | Client | OBERFLAECHE |
| - | `string.sub`, `string.len`, Textvergleich | Lua-Grundbibliothek (B1b-Nachbesserung) | beide | KERN |
**Nicht benutzt (auch nicht hinter pcall):** `isAnimalMoving`, `getLastSoundRespondedTo`, `OnWorldSound`, `setShouldFollowWall`, `changeStress`
(F2), `addAcceptance`, `setDebugStress`, Teleport (`setX/setY` am Tier), Vanillas Anhaenger-Aufrufe, `drawTextZoomed` (F8), `stopAllMovementNow`
direkt (nur ueber `setBlockMovement(true)`), `addSound` (keine Bench-Laermquelle: die 6-Argument-Form erschreckt Tiere laut Jar vermutlich nicht).
**Jar-only-Aufrufe in B1c: keine** ausser den beiden von Kevin erlaubten (Nr. 10, 11). Grenzfall Nr. 8 (Methode belegt, Name nur Jar) nur als
Zusatzsignal neben dem belegten Stress-Sprung.

---

## 9. Leistung (Ergaenzung zu PZ 7 / PB 11)
| Was | Wie oft | Deckel |
|---|---|---|
| Laerm-Wache | je Bild, je zahmem geladenem Jungen 2-4 Java-Aufrufe | 8 Junge, 4 Antworten / 2 s |
| Zombie-Suche | je Hirn-Takt (1,5 s; bei Gefahr 0,75 s), nur mit geladenen Jungen | 1500 Zombies je Takt |
| Heil-Suchlauf | 2 min lang je 15 s nach dem Laden, danach B1b | Kandidaten wie B1b |
| Spiegel | `markProbe` 1 x je Takt und Junges (1 `getModData`), schreiben nur bei Abweichung | 26 Felder |
| Mitfahren | `B.RideStep` je Takt und mitfahrendem Jungen, Platzsuche nur beim Aussteigen (<= 48 Kacheln) | Baeren je Spieler |
| Call to me | auf Klick, Platzsuche <= 48 Kacheln | 1 je 5 min und Junges |
| Lage in der Sicht | je Junges hoechstens je 5 s | 3 Schluessel |
| Markierung | je 400 ms ein `set` | 1 |
| Karte | je Bild je Symbol 2 Umrechnungen + 1 Bild (nur offene Karte), Liste je 500 ms | <= 5 Symbole |
| Optionen | 1 x/s beim Listenbau | - |

---

## 10. Fuer den ZUSAMMENBAU
- `staging_dateien.txt` neu (6 neue Lua-Dateien + 1 Bild, geaenderte MD5).
- `attrappe/gesamt/run.lua` Abschnitt "18 B1c" (7.3); beide Bauer-Attrappen gegen die echten Dateien wiederholen; `xref` ueber die Grenze
  (jede `B.*`-/`U.*`-Benutzung definiert, Befehl "Call" hat Empfaenger, Sicht-Felder `x/y/ride/callWait` passen, jeder Schluessel in allen sieben
  Sprachen, `U.EN` wortgleich).
- `baer/tools/baer_uebernahme.py`: (a) `CreateCub`-Regel (Zeile ~248) um `("42/media/lua/server/BanditsNPCBearRide.lua", "B.PlaceCub")`
  erweitern; (b) neue Regeln: `setVariable("animalRunning"` und `pathToLocation(` nur in `B.MoveTo` (`World.lua`); (c) das Bild
  `42/media/ui/BanditsNPCBearCub_marker.png` in die kopierten Dateien aufnehmen (wie `CUB_ASSET`) und auf Kollision mit NPC Crews `media/ui`
  pruefen; (d) die neuen Lua-Dateien deckt `LUA_BEAR` schon (`:95`); (e) neue Sandbox-Optionen in `B.OPTS` UND `sandbox-options.txt` (`:779`).
  Trockenlauf mit `--vor-b5a`, Probe nur unter `_arbeit/baer_zaehmen/probe_b1c/`.
- `baer/NAEHTE.md`: Naht 10 Karte (Aufsatz auf `ISMiniMapInner.render`/`ISWorldMap.render` neben NPC Crews `client/ISUI/BanditsNPCMiniMap.lua`;
  beide merken die vorige Methode, Reihenfolge egal, einmal einhaengen); Naht 11 Mod-Optionen (eigene Seite `BanditsNPCBear` neben NPC Crews
  `NPCCrew`; spaeter zusammenlegen moeglich, keine NPC-Crew-Datei geaendert); Naht 12 Bandits-Markierung (geteilte Bildschirmstelle mit NPC Crews
  `bnwsArrival`, F5); keine Zeile in einer NPC-Crew-Datei.
- `mod_info_vorschlag.txt` um B1c ergaenzen (Mitfahren, Call to me, Markierung, Karte, Optionen).
- Einbau in NCBearTest nur, wenn Kevin nicht spielt; vorher und nachher sichern.

---

## 11. Fragen fuer Kevin (jede mit Empfehlung; Kevin schlaeft -- nichts davon haelt den Bau auf)
1. **F1 MP-Spiegel faelschbar:** ein veraenderter Client kann Tier-Daten schreiben (`dec/ObjectModDataPacket.java`). Schutz in B1c: das Register
   gewinnt bei Widerspruch (Kennzeichen, AnimalID), Deckel je Spieler, Fehlerzeile je Heilung. Eine Unterschrift braeuchte einen Dateileser am
   Server ohne Vanilla-Beleg. Empfehlung: so lassen.
2. **F2 Stress durch Laerm:** die Engine erhoeht ihn je Flucht weiter (+radius x 0,05), auch wenn wir die Flucht abfangen. Ausgleichen
   (`changeStress`, negativ ohne Vanilla-Beleg) oder lassen? Empfehlung: lassen, Streicheln senkt ihn.
3. **F3 Besitzer stirbt im Auto:** das Junge steigt dort aus und wartet ("stay"). Ist die Gegend schon entladen, kommt es zur neuen Figur. Ok?
   Empfehlung: ja.
4. **F4 "Call to me" fuer ein Junges, das man nicht anklicken kann** (weit weg, vermisst): spaeter im Baeren-Fenster (V) oder schon jetzt im
   Welt-Rechtsklick? Empfehlung: im V-Fenster (deine Freigabe 5).
5. **F5 Markierung ueberlappt NPC Crews Ueberlebenden-Pfeil** (Bandits merkt eine Stelle fuer alle): eingebaut ist ein Versatz um 100 px nur bei
   Ueberlappung (`NCBear_CubSet("markerShift", 0)` = aus). Ok? Empfehlung: ja.
6. **F6 Doppelklick blendet die Markierung aus** und sie kommt fuer dieses Junge nicht wieder. Ok? Empfehlung: ja.
7. **F7 Tier-Anhaenger:** jeder Spieler kann jedes Tier in einen Tier-Anhaenger laden, auch dein Junges (Vanilla prueft keinen Besitz). Eigener
   Lauf nach B1c? Empfehlung: ja.
8. **F8 Schildgroesse in drei Stufen** (100/150/200 %), weil stufenlos (`drawTextZoomed`) keinen Vanilla-Aufrufer hat. Reicht das, oder willst du
   dafuer dein Wort geben? Empfehlung: drei Stufen.
9. **F9 Was scheucht es?** Rennen macht laut Spiel-Code keinen Tier-Laerm. Bitte im Test mit `NCBear_CubLog(true)` und `NCBear_CubCalm()` ansehen,
   was die Flucht ausloest (Schuss, Q, Husten, Zombie am Zaun).
10. **F10 Einsteigen:** das Junge verschwindet sofort (bis 15 Kacheln weg), statt erst zum Auto zu laufen. Ok fuer jetzt? Empfehlung: ja;
    Hinlaufen spaeter mit dem neuen Modell.
11. **F11 Zombie an der Heimat:** ein bleibendes Junges kann nach der Flucht heimlaufen und wieder fliehen. Ok bis B5a? Empfehlung: ja.
12. **F12 Gehen:** nur die letzten 3 Kacheln zu einem stehenden Besitzer. Mehr? Empfehlung: erst mit dem schnelleren Gehen des neuen Modells.
13. **F13 Wildes Junges aus einem verlorenen Register** kommt als scheues Junges zurueck (finder nur, wenn frei). Ok? Empfehlung: ja.
14. **F14 Karte:** mitfahrendes Junges ohne Symbol (es ist ja bei dir), vermisstes blasser an der letzten Stelle. Ok? Empfehlung: ja.
15. **F15 Namensschild aus** gilt fuer alle gezaehmten Baeren (eigene und fremde), der Zaehm-Balken bleibt. Ok? Empfehlung: ja.
16. **Dein laufender Spielstand:** die alte Zaehmung von "b1" steht nur noch in `Saves/Apocalypse/2026-11-10_22-12-12_crash/` (die Heilung kann
    sie dort nicht holen, der Spiegel wurde in B1b ueberschrieben). Weiter mit "b2" (Balken 33) oder den `_crash`-Stand laden? Empfehlung: mit b2
    weiterzaehmen.

## 12. Offen / ungeprueft (Testpunkte)
Ob die Ersatz-Antwort die Flucht vor dem ersten sichtbaren Schritt ersetzt (OnTick nach dem Tier-Update; am Server ungeprueft); Laerm-Lebensdauer
in Server-Ticks; ob `getStress` am Client der Kopie folgt (nur der Schreiber liest); `getVehicle()` fremder Spieler am Server; ob ein Spieler
beim Einloggen im Auto sitzt; Neu-Erzeugen direkt neben einem gebremsten Fahrzeug; ob die tote Figur im SP nach dem Tod noch in
`getSpecificPlayer` steht (`B.DeadAt`); `getZombieList`/`getVariableBoolean("Bandit")` am Server; A3 (`getObjectListForLua`/`getAnimalID` am
Server); ob `ModOptions.ini` vor dem ersten Lesen geladen ist (NC liest genauso, gespielt); Bandits-Markierung nach Tod/geteiltem Bildschirm;
genaue Groesse der Schriftstufen; ob Doubles (`u`, `ep`) die ModData exakt ueberstehen (Zahlen bis 2^53, wie die Weltstunden in B1a).

Statisch geplant, nichts gebaut, nichts gespielt.
