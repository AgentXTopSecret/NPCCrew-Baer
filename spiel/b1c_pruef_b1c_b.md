# Lauf baer-b1c: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung

Stand 11.11.2026 Nacht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`
(B1a + B1b + B1c, Stand nach dem ZUSAMMENBAU, `staging_dateien.txt`). Gelesen ganz: `server/` (Heal, Ride, Guard, Registry, Server,
World, Follow), `shared/BanditsNPCBearRules.lua` (Folgen, Wache, Namen), `client/` (Marker, Map, Options, Hud, Menue-Teil "Call",
Client-Teil Sicht). Dazu Jar-Auszuege `dec/IsoAnimal.java`, `dec/BaseAnimalBehavior.java`, Bandits `client/BanditEventMarkerHandler.lua`,
`client/BanditEventMarkers.lua`, `client/BanditZombie.lua`, Vanilla `client/PZAPI/ModOptions.lua`. Nichts im Staging geaendert.
Eigene Attrappen: `attrappe/pruef_b1c/run.lua` (Ausgabe unten in 3). Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla
`media/lua/`, `B:` = Bandits `42.22/media/lua/`, `dec/` = Jar-Auszug.

## 0. Ergebnis in einem Satz

Der Hauptweg von B1c traegt (leeres Register heilt, Mitfahren/Abmelden/Neustart/Tod ohne Verlust oder Doppel, Call to me am Server
geprueft, Gehen/Rennen sauber gesetzt, Markierung/Karte/Optionen billig und mit Riegeln) -- aber **zwei Stellen verfehlen Kevins
Auftrag im Spiel**: (B1) ist das Register nach einem Absturz nicht LEER, sondern AELTER als der Spiegel, gewinnt das alte Register
und die Zaehmung ist wieder weg (N9 in anderer Form, Attrappe 1a); (B2) die Platzwahl fuer Aussteigen und "Call to me" prueft keine
Wand zwischen Besitzer und Kachel und waehlt immer dieselbe Kachel -- das Junge kann hinter einer Hauswand/einem Zaun landen, und
"Call to me" setzt es beim naechsten Mal genau wieder dorthin (Attrappe 2a/2b). Dazu 8 kleine Befunde.

## 1. Befunde (Schwere: blocker / major / minor)

### B1 (major) Register aelter als der Spiegel: das alte Register gewinnt, die Zaehmung ist weg
- **Wo:** `S:server/BanditsNPCBearWorld.lua:636-654` (Suchlauf Schritt 2, AnimalID-Rueckfall: `sameBody = mu == rec.u and mg >= rec.gen`,
  bindet und ruft `B.Commit`) und `S:server/BanditsNPCBearHeal.lua:276-277` mit `bind` (:79-105) -- beide nehmen vom Spiegel hoechstens
  `gen`, nie Zustand/Besitzer/Balken, und `B.Commit` schreibt danach den ALTEN Stand in den Spiegel.
- **Wie es im Spiel entsteht:** Junges wird angefuettert, Kevin speichert (Register: `fed`). Spaeter zaehmt er es, laesst es "bleiben" und
  geht weg -- die Zelle entlaedt und wird mit dem Spiegel `tame` (r hoeher) gespeichert; die globale ModData nur beim Speichern
  (Annahme, Jar nicht nachgelesen). Absturz -> beim Laden: Register `fed` (gleiche Epoche, gleiches `u`), Tier mit Spiegel `tame`. Dass
  Zelle und Register so auseinanderlaufen, zeigt Kevins N9-Ordner selbst (`baer/STAND.md:55-56`: Register leer, Tier mit Spiegel da).
- **Beleg Attrappe 1a:** "Spiegel vorher tame -> Eintrag jetzt st=fed owner=nil name=nil, Spiegel jetzt st=fed r=3" -- gebunden ueber
  Schritt 2 (Spur: `[TC-BEAR] scan: b1 found again by its animal id, mark written anew`). Plan 3.3 behandelt nur "gen hoeher", nicht
  "Fortschritt hoeher".
- **Vorschlag:** an BEIDEN Stellen: ist `mark.ep == reg.ep` und `tonumber(mark.r) > rec.r`, ist der Spiegel neuer -> seine Felder wie
  in `B.Restore` geklemmt uebernehmen (st missing->tame, tame, fedN, petN, last, feedAt, petAt, tamedAt, mode, name, Heimat; owner/bond
  ueber `keyOf`), `rec.r = mark.r`, Deckel `BearMaxPerPlayer` pruefen, eine Fehlerzeile "heal: entry ... updated from a newer mark".
  **SP:** voll vertrauen (kein Fremder, `forschung_b1c.md` 0.1). **MP:** nur Fortschritt OHNE Besitzwechsel (owner/bond im Spiegel
  gleich dem Eintrag oder Eintrag ohne owner/bond), sonst Register behalten + Zeile -- ein gefaelschter Spiegel kann so nichts stehlen.

### B2 (major) Aussteigen / "Call to me": Kachel hinter Wand oder Zaun, und immer dieselbe
- **Wo:** `S:server/BanditsNPCBearWorld.lua:215-248` (`spotOk` prueft nur Boden, Wasser, Baum, `isFree(false)`, Fahrzeug; ausdruecklich
  ohne `isOutside`; feste Reihenfolge, erste Kachel immer (x-1, y-1)); gerufen `S:server/BanditsNPCBearRide.lua:199` (Aussteigen),
  `:165` (Tod), `:307` (Call to me).
- **Folge:** steht Kevin neben einer Hauswand oder einem Zaun (beim Parken fast immer), liegt in etwa der Haelfte der Lagen schon die
  ERSTE Kachel jenseits der Wand -- frei, Boden, also gewaehlt: das Junge steht im Haus bzw. im Nachbargarten. Folgt es, kommt es nur
  durch eine offene Tuer heraus; sonst "steckt fest". "Call to me" (5 min Abklingzeit) setzt es **wieder genau dorthin** -- der
  Unstuck-Knopf hilft dann nie.
- **Beleg Attrappe 2a/2b:** "SpotNear -> 999,999, isBlockedTo/getRoom gefragt 0 x"; "1. 999,999, 2. 999,999".
- **Vorschlag (belegte Aufrufe, gleiche Argumenttypen):** Kachel nur, wenn `sq:getRoom() == ownerSq:getRoom()` (`V:shared/Util/
  AdjacentFreeTileFinder.lua:240`, `playerSq:getRoom() == gridSquare:getRoom()`) UND fuer Ring 1 `not sq:isBlockedTo(ownerSq)`
  (`V:shared/Foraging/ISForageAction.lua:7`, `square:isBlockedTo(square)`); fuer Ring 2-3 Schritt fuer Schritt gegen die Nachbarkachel
  zum Besitzer hin (hoechstens 3 Fragen je Kachel). Fuer "Call to me" den Anfang im Ring mit `ZombRand` (belegt `V:shared/TimedActions/
  Animals/ISMilkAnimal.lua:25`) drehen, damit ein zweiter Ruf eine andere Kachel nimmt. Ob `isBlockedTo` Diagonalen sauber prueft:
  ungeprueft (Testpunkt).

### B3 (minor) Register leer + zwei Koerper mit gleichem u: die Reihenfolge entscheidet, die alte Kopie gewinnt
- **Wo:** `S:server/BanditsNPCBearWorld.lua:664-684` (Schritt 3 in Listenreihenfolge), `S:server/BanditsNPCBearHeal.lua:262-275`
  (die erste Kopie wird per `B.Restore` Eintrag; die zweite mit HOEHERER gen ist dann "dup", weil nur `mg < rg` -> stale gefragt wird).
- **Wann:** alte Kopie (gen kleiner, z. B. in einer frueher gespeicherten Zelle nach "Call to me" oder vor dem Einsteigen) und echter
  Koerper sind beide geladen, und das Register ist verloren. Selten, aber genau der Absturz-Fall.
- **Beleg Attrappe 1b:** "Eintrag name=Old mode=stay gen=0, gebunden an alte Kopie, echter Koerper entfernt=true" -- der echte Koerper
  (Name "Bruno", Folgen) wird entfernt, der alte Stand wiederhergestellt.
- **Vorschlag:** in `B.ScanAnimals` vor Schritt 3 `marked` nach `tonumber(mark.gen)` absteigend sortieren (`table.sort`, wie
  `S:...Registry.lua:590`), und in 1a bei `otherAlive` mit `mg > rg`: an `o` binden und das andere Objekt als "stale" melden.

### B4 (minor, bestaetigt Z1) Nicht herstellbarer zahmer Spiegel wird beim Anfassen ein neuer "found"-Eintrag
- **Wo:** `S:server/BanditsNPCBearRegistry.lua:341-364` (HealFromMark nil -> `B.NewRec("found")` ueberschreibt den Spiegel).
- **Wann:** Deckel `BearMaxPerPlayer` voll (`cap`), MP-Spiegel ohne Besitzer/`__sp` (`nokey`), MP-v1-Spiegel `tame` (Heal.lua:302 nur SP).
  Der Suchlauf laesst das Tier stehen (nil, World.lua:568), aber das erste Fuettern/Streicheln macht es zu einem scheuen Fund -- ein
  Fremder kann es dann zaehmen. Unabhaengig vom ZUSAMMENBAU nachgelesen, gleicher Schluss wie Z1.
- **Vorschlag:** wie Z1 -- Spiegel mit `st` tame/fed/missing und Heil-Ergebnis nil -> `return nil, "heal"` (Menue `Why_Gone`).

### B5 (minor) Laerm: Stress am Deckel + eigener Laufbefehl -> Flucht wird nicht erkannt
- **Wo:** `S:server/BanditsNPCBearGuard.lua:177-191`. Hauptsignal ist der Stress-Sprung (+radius x 0,05 je Flucht,
  `dec/IsoAnimal.java:799`); bei Stress 100 gibt es keinen Sprung mehr. Das Zweitsignal "rennt" ist abgeschaltet, solange
  `s.ownUntil` laeuft (Folgen, Heimweg, Wache setzen es bei jedem Befehl, `S:...World.lua:779-782`).
- **Folge:** nach vielen Schuessen (Stress klebt oben) fliehen folgende Junge wieder ein Stueck -- aufgefangen erst vom Rueckfall
  `followFleeGrow` im naechsten Hirn-Takt (Rules.lua:531-537, 1,5-3 s, dann 4-7 Kacheln weg); ein BLEIBENDES Junges mit laufendem
  Heimweg gar nicht. Plan 1.2 Schritt 5 nennt den Rueckfall nur fuer Folgen.
- **Vorschlag:** `B.MoveTo` merkt sein Ziel (`s.tx, s.ty`); `calmTickBody` vergleicht waehrend `own` billig (2 x getX/getY, belegt
  `V:shared/Definitions/animal/ButcheringUtil.lua:575-576`), ob das Tier sich um mehr als 1 Kachel VOM eigenen Ziel entfernt -> "run".
  Damit faellt auch der bekannte Fehlalarm bei langen eigenen Wegen weg (`bau_b1c_kern.md` 7: Heimweg wird durch 1,5 Kacheln ersetzt).

### B6 (minor) Q-Ruf mit Akzeptanz >= 40: die Annahme "geht statt zu rennen" stimmt nicht immer
- **Wo:** Kommentar `S:server/BanditsNPCBearGuard.lua:156-157`, Plan 1.2 Schritt 4. Der Engine-Zweig setzt `animalRunning` gar nicht
  (`dec/IsoAnimal.java:783-784`, nur `pathToLocation`), es bleibt beim letzten Wert -- nach unserem `fleeTo` also `true`
  (`dec/IsoAnimal.java:2525`).
- **Folge:** das Herankommen auf Q laeuft dann rennend ohne eigenen Befehl -> "run" -> ersetzt: beim folgenden Jungen harmlos (es rennt
  ohnehin zum Besitzer), beim BLEIBENDEN wird Q ignoriert (Ersatzschritt Richtung Heimat). Kein Schaden, nur Kommentar und Erwartung in
  Kevins Test 7.4 Punkt 4 anpassen ("Q mit hoher Akzeptanz: es kommt" gilt nur beim Folgen).

### B7 (minor) Zombie zwischen Besitzer (> 10 Kacheln) und Junges: Hin-und-Her Flucht / Folgen
- **Wo:** `S:shared/BanditsNPCBearRules.lua:607-627` (verstecken nur bis `hideOwnerMax` 10, sonst fliehen VOM Zombie, also vom Besitzer
  weg); nach `zedSafe` + `zedCalmMs` folgt es wieder -- auf den Zombie zu.
- **Beleg Attrappe 3a** (Bewegungsmodell 2,47 / 0,52 K/s, Zombie steht 5 Kacheln vor dem Besitzer, Junges 12): "Flucht-Beginne 2,
  Versteck-Beginne 1, groesster Abstand zum Besitzer 24.0, Abstand am Ende 1.0" -- endet zwar am Besitzer (haengt nicht), rennt aber
  zweimal bis 24 Kacheln weg; ob der dritte Anlauf klappt, haengt am Takt. 3b (Zombie 2 Kacheln vor dem Besitzer): kein Hin-und-Her.
- **Vorschlag:** Hysterese auf den Besitzer-Abstand (verstecken bis `hideOwnerMax`, einmal "hide" bis `hideOwnerMax + 4`) und/oder
  nach einer Flucht beim Folgen halten, solange der Zombie in `zedSense` steht (statt auf ihn zuzulaufen). Bis B5a (Zombies greifen nicht
  an) nur ein Schoenheitsfehler.

### B8 (minor, Leistung) Zombie-Suche rechnet jeden Zombie gegen jedes Junge
- **Wo:** `S:server/BanditsNPCBearWorld.lua:318-325` (`anyNear`) in der Schleife `:365-378`, ebenso der SP-Cache-Zweig `:341-348`.
- **Kosten:** je Takt bis `zedScanMax` 1500 Zombies x Zahl der geladenen Jungen (Deckel nur `maxRecs` 64) Lua-Schleifen; auf einem
  MP-Server mit 20-30 Jungen ~30-45 Tsd. Durchlaeufe je 0,75-1,5 s (unter Kahlua spuerbar, Groesse ungemessen). SP mit 1-2 Jungen: egal.
- **Vorschlag:** vor der Zombie-Schleife einmal den Rahmen aller Punkte +- r (min/max x/y) bilden und je Zombie zuerst 4 Vergleiche;
  nur im Rahmen die Punktschleife.

### B9 (minor) Sichtbare Doppel neben dem Spieler (und Fleisch daraus)
- **Wo:** `S:server/BanditsNPCBearWorld.lua:554-561` (`dropCopy` nur, wenn niemand in 25 Kacheln und SP keiner hinsieht) und
  `S:server/BanditsNPCBearRide.lua:313`, `:321` (Call to me entfernt das alte Tier nur, wenn es GEBUNDEN ist).
- **Wann:** "Call to me", waehrend das alte Tier geladen, aber noch nicht gebunden ist (Sekunden nach dem Laden, bis zum naechsten
  Suchlauf je `scanMs` 5 s), oder eine alte Kopie nach Absturz direkt beim Spieler. Dann steht ein zweites Junges ohne Schild da, bis
  Kevin 25 Kacheln weggeht. Es hat Zerlege-Teile (`S:shared/BanditsNPCBearDefs.lua:127-128`): erschlagen und zerlegen gibt Fleisch aus
  einem Tier, das es nicht geben duerfte (ein totes Doppel raeumt kein Suchlauf, World.lua:583 nimmt nur lebende).
- **Vorschlag:** in `B.HandleCall` bei `B.FindAnimal(rec) == nil` und geladener Gegend erst `B.ScanAnimals(nil)` (bindet das alte Tier,
  hoechstens ein Suchlauf je Ruf und 5 min), dann wie heute entfernen.

### B10 (minor, MP) Heil-Regel 1a bindet einen Spiegel mit hoeherer gen ohne AnimalID-Gegenprobe
- **Wo:** `S:server/BanditsNPCBearHeal.lua:276-277`. Ist das Junge eines Spielers gerade nicht geladen (kein `otherAlive`), bindet ein
  Spiegel mit seinem `u` und `gen >= rec.gen` auf JEDEM ungebundenen Jungen den Eintrag dorthin; der echte Koerper wird spaeter "stale".
  Ein veraenderter Client koennte so ein fremdes Junges "umsetzen" (kein Diebstahl: Besitzer bleibt). Braucht ein ungebundenes
  Junges ohne Eintrag und das `u` des Opfers -- ob der Client den Server-Spiegel ueberhaupt sieht, ist ungeprueft (`B.ViewOf`,
  `S:shared/BanditsNPCBear.lua:439`: "im Einzelspieler immer da, sonst die OnlineID").
- **Vorschlag:** im MP bei `mg == rg` zusaetzlich `rec.aid == o:getAnimalID()` verlangen; `mg > rg` (Absturz-Fall) nur, wenn kein
  geladenes Tier mit `rec.aid` in 40 Kacheln der letzten Kachel steht.

## 2. Gegengeprueft und in Ordnung (Fundstelle je Punkt)

| Thema | SP | MP | Fundstelle |
|---|---|---|---|
| Leeres Register (Kevins N9) | wird aus dem Spiegel hergestellt, gleiche Kennung, `__sp`, Name, Modus, eine Fehlerzeile | nur Konten ungleich `__sp`, Deckel je Spieler | Heal.lua:165-241; Gesamt 18c; Attrappe 1b (Restore-Zeile) |
| Kennung/Zaehler eindeutig | `B.NewId` ueberspringt belegte, `B.BumpN` bei Wiederherstellung und gleicher Epoche | gleich | Registry.lua:242-257, Heal.lua:192-201, World.lua:604-605 |
| Doppel gleicher gen / kleinere gen | erstes gebunden, zweites "dup" bzw. "stale" | gleich | Heal.lua:262-277 (Ausnahme B3) |
| Fremder Spiegel auf Jungem MIT Eintrag | Riegel 1 (Objekt der Sitzung) bzw. 1b (AnimalID) gewinnt; Schritt 2 nimmt fremdes `u` nie | gleich | World.lua:589-599, :641; Heal.lua:280-284 |
| Einsteigen | nur tame + follow + <= `BearRideDistance`, Koerper weg, gen+1, Sitzung leer, Laerm-/Zombie-Wache raus | dazu `removeAnimal(OnlineID)` | Rules.lua:478-482, Ride.lua:97-120, World.lua:437-445 |
| Waehrend der Fahrt | kein "missing", kein "lost", Lage = Besitzer, kein Symbol | gleich | Server.lua:792-793, :813; Follow.lua:182; Map.lua:61 |
| Speichern/Laden in der Fahrt | `ride` im Register, `InitRegistry` prueft ihn, `s.ride` neu | Neustart ebenso | Registry.lua:155-161, Ride.lua:154-157 |
| Aussteigen | nach 1 s zu Fuss, genau ein neuer Koerper (gen+1), follow, Meldung | nach 3 s und <= 4 K/s (getVehicle-Flackern) | Ride.lua:188-213 |
| Besitzer tot im Auto | `B.DeadAt` + 5 s + Gegend geladen -> neben der Leiche, "stay"; sonst zur neuen Figur | ebenso ueber `getOnlinePlayers` | Ride.lua:160-180, World.lua:255-276 |
| Abmelden im Auto | `ride` bleibt, nichts erscheint, beim Einloggen zu Fuss neben ihm | -- | Ride.lua:160-181 |
| Zwei Spieler / Fremder im Auto | nur `rec.owner` zaehlt | gleich | Ride.lua:35-46 |
| Call to me am Schreiber | Eintrag, Besitz, tame/missing, nicht ride, nicht im Auto, Abklingzeit, Platz; erst NEUER Koerper, dann altes weg; Drossel je Ausgang | nur `sendClientCommand`, kein Kick-Weg | Ride.lua:275-327, Follow.lua:53-72 |
| Abklingzeit | Echtzeit am Schreiber, Uhr rueckwaerts = frei, Deckel 64 | Sicht `callWait` nur fuer den Besitzer | Ride.lua:220-256, Registry.lua:551-555 |
| Gehen/Rennen | jeder Befehl setzt den Laufmerker neu: gehen `setVariable(false)` vor `pathToLocation`, rennen `fleeTo` (setzt selbst `true`, `dec/IsoAnimal.java:2525`); gehen nur Rest <= 3 und Besitzer <= 0,52 K/s -> faellt heute nicht zurueck | gleich (Anzeige der Variable am Client ungeprueft) | World.lua:767-772, Rules.lua:527-547 |
| Laerm nur am gezaehmten | Wache nur `st == "tame"` ohne ride, Deckel 8, 4 Antworten / 2 s, Ruhefrist ohne Sperre | Server; fragt nicht, wer laermt | Guard.lua:51-69, :97-148, :159-199; World.lua:710-714 |
| Rennen des Spielers scheucht nicht | nicht wilde Tiere setzen `spottedChr` fuer Spieler nie (nur Wild- und Zombie-Zweig) | gleich | `dec/BaseAnimalBehavior.java:1534-1580`, `:1688` (Wild-Zweig), `:1691-1692` (Zombie-Zweig) (stuetzt F9) |
| Zombies | Banditen/NPC-Crew-Figuren nie, tote/Grapple nie; Wache vor Folgen; Einsteigen geht vor; Takt 750 ms nur bei Gefahr | `GetBanditClusterData` hinter Riegel | World.lua:290-300, :365-378; Guard.lua:255-306 |
| Markierung | nur mit Bandits; feste Id; aus genau einmal; Doppelklick respektiert; altes Element aus dem UIManager | aus der eigenen Sicht | Marker.lua:77-81, :101-105, :177-221; `B:client/BanditEventMarkerHandler.lua:6-38` |
| Karte | einmal je Klasse, Kette mit NPC Crew, nur eigene, nie ride, je Bild <= 5 Symbole x (1+2+2+1) Aufrufe | eigene Sicht | Map.lua:60-73, :114-156, :179-193 |
| Optionen | Seite mit Schluesseln, `U.Opt` 1 x/s, Vorgaben ohne Seite | je Client | Options.lua:46-61, :67-90; `V:client/PZAPI/ModOptions.lua:206-257` |
| Bandits fehlt / NPC Crew fehlt | Markierung tut nichts, Zombie-Suche ueber `getZombieList` ohne Banditen-Frage; keine NC-Abhaengigkeit | gleich | Marker.lua:181, World.lua:337-353 |
| Kleinkram | ES "Caricia: %1"; N2 Bereiche; N3 `pkey ~= nil` | -- | ES/UI.json:31; Rules.lua:360-371, :412-415; Registry.lua:582 |
| Rote Linien | B1c erzeugt/vernichtet keine Gegenstaende (Ausnahme Fleisch aus einem Doppel, B9); kein neuer Kick-Weg; Deckel ueberall; NPC-Crew-Figuren unberuehrt | gleich | -- |

## 3. Eigene Attrappen (`attrappe/pruef_b1c/run.lua`, Lua 5.1, echter Kern aus dem Staging)

Aufruf: `C:/Users/Kevin/Tools/lua51/lua5.1.exe C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/pruef_b1c/run.lua`
```
== Fall 1: Register aelter als der Spiegel / alte Kopie zuerst geheilt
BEFUND  1a Register aelter (fed, r 2), Spiegel neuer (tame, r 3): Zaehmung nach der Heilung weg  -- Spiegel vorher tame -> Eintrag jetzt st=fed owner=nil name=nil, Spiegel jetzt st=fed r=3
BEFUND  1b Register leer, alte Kopie (gen 0) + echter Koerper (gen 1): die ALTE gewinnt, der echte wird entfernt  -- Eintrag name=Old mode=stay gen=0, gebunden an alte Kopie, echter Koerper entfernt=true, lebende Junge 1
== Fall 2: Platzwahl neben dem Besitzer (Aussteigen / Call to me)
BEFUND  2a Kachel hinter einer Wand (999,999) wird gewaehlt, Wand/Raum nie gefragt  -- SpotNear -> 999,999, isBlockedTo/getRoom gefragt 0 x
BEFUND  2b zweimal 'Call to me' -> beide Male dieselbe Kachel (kein zweiter Versuch woanders)  -- 1. 999,999, 2. 999,999
== Fall 3: Zombie zwischen Besitzer und Junges (Bewegungsmodell)
   3a Zombie 5 Kacheln vor dem Besitzer: Flucht-Beginne 2, Versteck-Beginne 1, groesster Abstand zum Besitzer 24.0, Abstand am Ende 1.0, mode follow, Laufbefehle 11
OK      3a ... Hin-und-Her (>= 3 Fluchten in 90 s)  -- Fluchten 2, Verstecke 1, Ende 1.0 Kacheln, follow
   3b Zombie 2 Kacheln vor dem Besitzer: Flucht-Beginne 0, Versteck-Beginne 1, groesster Abstand zum Besitzer 12.0, Abstand am Ende 1.0
OK      3b Zombie direkt am Besitzer: versteckt sich ohne Hin-und-Her
[TC-BEAR] ***-Zeilen waehrend des Laufs: 1   (die gewollte Heilungszeile aus 1b)
```
Grenzen: die Attrappe kennt keine Waende (Fall 2 zeigt nur, dass der Kern nie fragt, und die feste Reihenfolge); Fall 3 ist ein
einfaches Bewegungsmodell ohne Wegsuche; ob Zellen beim Entladen gespeichert werden (Fall 1a), ist Annahme.

## 4. Fragen fuer Kevin (Kevin schlaeft -- nichts davon haelt den Einbau auf; B1 und B2 vor dem naechsten Spieltest nachbessern)
1. **B1:** soll nach einem Absturz der NEUERE Stand am Tier gewinnen (im Einzelspieler immer, im Mehrspieler nur ohne Besitzwechsel)?
   Empfehlung: ja.
2. **B2:** das Junge darf beim Aussteigen / "Call to me" nur auf eine Kachel, die du ohne Wand erreichst (gleicher Raum, kein Zaun
   dazwischen), und ein zweiter Ruf probiert eine andere. Ok? Empfehlung: ja.
3. **B7:** steht ein Zombie zwischen dir und deinem Jungen, rennt es heute erst weg und kommt dann zurueck. Lieber stehen bleiben, bis der
   Zombie weg ist? Empfehlung: ja (klein, mit B5a zusammen).
4. **B9:** ein Doppel neben dir (selten) soll sofort verschwinden, auch wenn du hinsiehst? Empfehlung: nein -- lieber beim Ruf zuerst das
   alte Tier suchen (Vorschlag B9).

## 5. Offen / ungeprueft (zusaetzlich zu PLAN_B1C.md 12 und bau_b1c_zusammenbau.md 7)
- Ob `isBlockedTo` / `getRoom` an der Kachel am MP-Server dasselbe liefern wie am Client (Belege sind `shared/`).
- Ob `setVariable("animalRunning", false)` am Server die Gang-Animation der Client-Kopie mitnimmt (MP).
- Ob die Zelle eines Tiers beim Entladen VOR dem naechsten Speichern geschrieben wird (macht B1 haeufig oder selten).
- Ob Bandits' Markierung nach `RemoveOldMarkers` (Spielzeit `start + duration`, `B:client/BanditEventMarkerHandler.lua:40-49`) sauber
  neu entsteht: der Kern legt dann ein neues Element an und raeumt das alte (Marker.lua:186-189) -- statisch richtig, ungespielt.

Statisch geprueft, nicht gespielt. Nach einem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).
