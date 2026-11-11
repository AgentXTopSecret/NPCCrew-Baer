# Lauf baer-b1b: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung (B1b)

Stand 11.11.2026. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/42/media/lua/` (B1a + Fix 1-3 +
B1b, Stand `staging_dateien.txt` 11.11.). Ganz gelesen: `server/BanditsNPCBearFollow.lua`, `...Server.lua`, `...World.lua`, `...Registry.lua`,
`shared/BanditsNPCBear.lua`, `...Rules.lua`, `...Food.lua`, `client/BanditsNPCBearClient.lua`, `...Menu.lua`, `client/ISUI/BanditsNPCBearHud.lua`,
`...NameBox.lua`, B1b-Teil von `client/NCBearBenchCub.lua`; dazu `PLAN_B1B.md`, `bau_b1b_zusammenbau.md`, `schnittstelle_aenderungen.md` (B1b),
Vanilla `client/ISUI/ISTextBox.lua`, `client/ISUI/ISWorldObjectContextMenu.lua:2594-2622`, Jar-Auszuege `dec/IsoAnimal.java`.
Geschrieben habe ich nur diesen Bericht und `attrappe/pruef_b1b/` (`run.lua`, `spur_1a.lua`, `ergebnis.txt`, `spur_1a.txt`). Kein git, kein Spiel.
Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/`, `AP` = meine Attrappe `attrappe/pruef_b1b/run.lua`.

## 0. Ergebnis

| | |
|---|---|
| Befunde | **1 blocker (B1), 0 major, 7 minor (B2-B8)** |
| Kern der Sache | Das **Folgen beim GEHENDEN Besitzer bricht nach ~15 s zusammen**: die Regel "steckt fest" haelt freies Hinterherlaufen fuer festgesteckt, danach gibt es nur noch einen Laufbefehl je 10 s; das Junge faellt auf ~25 Kacheln zurueck und holt erst auf, wenn der Besitzer stehen bleibt (B1). Die Gesamt-Attrappe kann das nicht sehen, weil ihr `fleeTo` das Tier sofort ans Ziel setzt (`bau_b1b_zusammenbau.md` 2 "Grenze der Attrappe"). |
| Rote Linien | kein Gegenstand erzeugt/vernichtet (Futter hinhalten = nur Vanilla `equip`), kein neuer Kick-Weg (nur eigene `sendClientCommand`), nichts haengt endlos (alle Schleifen gedeckelt), keine NPC-Crew-Figur beruehrt -- **gehalten** |
| Waisen (N5) | raeumt in keinem gefundenen Fall ein Junges mit gueltigem Eintrag (auch ohne Spiegel, AP 2a); nie den Erwachsenen, nie fremde Tiere; SP nie im Blick; MP nur ueber 25 Kacheln Abstand (bekannte Grenze wie B1a) |
| Attrappe | `AP`: 3 Faelle, 18 Pruefungen, 8 x BEFUND (= B1, B3, B4, B5), 10 x OK, 0 `***`-Zeilen; Aufruf `C:/Users/Kevin/Tools/lua51/lua5.1.exe C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/pruef_b1b/run.lua` |
| Empfehlung | **B1 vor dem Einbau beheben** (kleine Aenderung in `B.FollowDecide`, Vorschlag unten), B2-B8 nach Kevins Wahl; dann Kevins Test 8.4 Schritt 2 um "30 s geradeaus gehen" erweitern |

## 1. Befunde

### B1 (blocker) -- "steckt fest" schlaegt beim normalen Gehen an; Folgen wird zum Stop-and-go auf ~25 Kacheln
- **Stelle:** `S:shared/BanditsNPCBearRules.lua:389-406` (`B.FollowDecide`, Fortschritt und Regel 15), wirkt ueber `S:server/BanditsNPCBearFollow.lua:115-147`.
- **Was der Code tut:** Fortschritt zaehlt nur, wenn `d <= f.bestD - followStuckGain` (`:390`); `f.bestD` ist der Abstand beim LETZTEN
  Fortschritt. Kommt in `followStuckMs` (15 s) kein Fortschritt, ist das Junge "festgesteckt" (`:395-397`) und bekommt nur noch je
  `followRetryMs` (10 s) einen Laufbefehl (`:400-406`).
- **Warum das beim Gehen immer anschlaegt:** das Ziel liegt `followGap` (2) Kacheln vor dem Besitzer an SEINEM Ort zur Zeit des Befehls
  (`:408`), Befehle gibt es nur im Hirn-Takt (1,5 s). Zum Zeitpunkt jedes Takts steht das Junge also bestenfalls an seinem alten Ziel:
  `d >= 2 + 2,27 x 1,5 = 5,4` Kacheln (Tempo: Spieler gehend 2,27, Junges rennend 2,47, `forschung_b1b.md:37-38`). `f.bestD` ist aber der
  Abstand beim Losrennen (3 bis ~5,5). Ein Fortschritt um eine ganze Kachel unter diesen Wert ist waehrend des Gehens unmoeglich ->
  nach 15 s geradeaus "festgesteckt" -- bei freiem Weg und schnellerem Jungen.
- **Beleg (Attrappe mit echtem `FollowStep`/`MoveTo`/`FollowDecide`, nur `fleeTo` als Bewegungsmodell; `AP` Fall 1, Spur `attrappe/pruef_b1b/spur_1a.txt`):**
  - 1a Plan-Fall (Besitzer geht 2,27, Junges 2,47, 120 s): `stuck` bei 15,1 s, danach Abstand 8,7 -> 12,1 -> ... -> 29,1, Ende 25,4, nur 19 Laufbefehle.
    Spur: bis 13,6 s `d` 5,3-5,9 mit Regel 16 je Takt, ab 15,1 s Regel 15 "keep", das Junge steht am alten Ziel, der Besitzer geht weiter.
  - 1b Junges 3 % langsamer (2,20): mit Regel Ende 35,7; ohne die Regel (Gegenprobe `followStuckMs` riesig) Ende 13,9.
  - 1c 20 s joggen (3,5 = ANNAHME, ungeprueft), dann 120 s gehen: mit Regel Ende 24,2 (holt nie auf), ohne Regel Ende 5,4.
  - 1d joggen, dann stehen: kommt heran (2,0) -- Erholung nur im Stand (Regel 14 setzt zurueck).
  - Die B1b-Kern-Attrappe prueft Regel 15 nur mit stehendem Abstand (`attrappe/b1b_kern/run.lua:108-117`), die Gesamt-Attrappe teleportiert
    beim `fleeTo` -- beide koennen den Fall nicht zeigen.
- **Folge fuer Kevin:** Kevins Test 8.4 Schritt 2 ("15 Kacheln weggehen", ~7 s) besteht noch; jeder laengere Weg zeigt "es bleibt immer
  wieder stehen und ist weit hinten". Mit etwas Rennen dazwischen landet es bei 40 Kacheln -> "could not keep up" (Bleiben).
- **Vorschlag:** "festgesteckt" an der Bewegung des JUNGEN messen, nicht am Abstand zum Besitzer: in `f` die Lage des Jungen beim letzten
  Fortschritt merken (`f.bx, f.by`); Fortschritt = Junges hat sich seitdem um >= `followStuckGain` bewegt ODER `d` ist um >= 1 kleiner
  geworden. Ein frei rennendes Junges ist dann nie "fest"; vor einer zu Tuer bewegt es sich nicht -> wie geplant ein Versuch je 10 s.
  (`f` bekommt zwei feste Felder, kein Wachstum.) Test: `AP` Fall 1 als Vorlage in die Kern-Attrappe uebernehmen (Bewegungsmodell statt Teleport).

### B2 (minor) -- Abstand beim Gehen ~5-6 Kacheln statt "etwa 2-4"
- **Stelle:** `S:shared/BanditsNPCBearRules.lua:407-420` (Ziel `toward(o, c, followGap)` am Ort des Besitzers zur Befehlszeit), Takt 1,5 s.
- **Beleg:** Spur 1a (`attrappe/pruef_b1b/spur_1a.txt`): vor dem Anschlagen von B1 `d` = 5,3-5,9 in jedem Takt; das Junge erreicht sein Ziel
  (2 Kacheln hinter dem ALTEN Ort) und wartet bis zum naechsten Takt. Kevins Auftrag: "Abstand etwa 2-4 Kacheln".
- **Vorschlag (zusammen mit B1):** Ziel um den Weg des Besitzers seit dem letzten Takt vorziehen (der Schreiber kennt ihn: `B._pp[uid]`,
  `S:server/BanditsNPCBearServer.lua:886-888`; z. B. Ziel = Besitzer + (Besitzer - letzter Ort) - followGap auf der Linie), oder solange er
  sich bewegt `followGap` 0-1. Reine Rechnung, kein neuer Engine-Aufruf.

### B3 (minor) -- `B.FollowLost` ohne Frist: erster Takt nach dem Laden kann "stayed behind" ausloesen
- **Stelle:** `S:server/BanditsNPCBearFollow.lua:154-159`, gerufen VOR dem Suchlauf `S:server/BanditsNPCBearServer.lua:855-861`.
- **Was passiert:** nach dem Laden ist `B._s` leer (`S:server/BanditsNPCBearRegistry.lua:117`), jedes Junge steht im ersten Takt in
  `missing`. Ist in diesem Takt die Gegend um seine letzte Kachel noch nicht geladen (`B.AreaLoaded`: Kachel und vier Punkte +-12), wechselt
  ein folgendes Junges sofort auf Bleiben, mit Meldung "Your cub stayed behind to the ..." an den Besitzer, der daneben steht. Der B1a-Weg fuer
  "fehlt" hat dafuer eine Frist (`missScans`), dieser nicht.
- **Beleg:** `AP` 2c: Takt 1 ohne geladene Kacheln -> `mode = stay`, Meldung `Note_StayBehind`. Ob im SP beim ersten `OnTick` nach dem Laden die
  Kacheln um den Spieler schon da sind: **ungeprueft** (Kevins Test 8.4 Schritt 7 zeigt es). Im MP ohne Folge (nach Server-Neustart gilt
  ohnehin Regel 10 "offline").
- **Vorschlag:** `FollowLost` nur fuer ein Junges, das in DIESER Sitzung schon ein Objekt hatte (z. B. Merker `B._s[id].seen = true` in
  `liveRec`), sonst nichts tun -- dann bleibt nach dem Laden alles beim B1a-Weg (Suchlauf bindet, Folgen geht weiter).

### B4 (minor) -- `B.CleanName` laesst nicht druckbare Zeichen ueber 127 durch
- **Stelle:** `S:shared/BanditsNPCBearRules.lua:341-356` (Zeichenpruefung `:351-354`), dieselbe Regel im Fenster (`S:client/ISUI/BanditsNPCBearNameBox.lua:30-34`) und am Server (`S:server/BanditsNPCBearFollow.lua:234`).
- **Beleg:** `AP` 3d-3f (Server, MP): U+0085 (C1-Steuerzeichen NEXT LINE), U+202E (Rechts-nach-links-Umschaltung) und ein Name NUR aus U+200B
  (Null-Breite-Leerzeichen) werden angenommen -> unsichtbares bzw. verdrehtes Schild, auch fuer andere Spieler sichtbar. Kevins Auftrag:
  "nur druckbare Zeichen". **Zur Plan-Frage "ungeprueft, FB1B 3":** Kahluas `string.byte` liefert die volle UTF-16-Einheit (Jar
  `se/krka/kahlua/stdlib/StringLib.stringByte`: `String.charAt` -> `KahluaUtil.toDouble`, keine Maske; javap aus `projectzomboid.jar`,
  nur gelesen, nach meinem Scratch gezogen), `string.len` zaehlt dieselben Einheiten. Die Laengen- und `<`/`>`/`%`-Pruefung arbeitet unter
  Kahlua also richtig; Umlaute/Kyrillisch/Koreanisch werden nicht verstuemmelt. Emoji zaehlen doppelt (Ersatzpaar).
- **Vorschlag:** zusaetzlich ablehnen: 128-159, 0x200B-0x200F, 0x2028-0x202E, 0x2060-0x206F, 0xFEFF; und verlangen, dass mindestens ein
  Zeichen sichtbar ist. Achtung Attrappe: echtes Lua 5.1 liefert UTF-8-Bytes (128-159 sind dort Folgebytes legaler Zeichen) -- die Pruefung
  gilt fuer Kahlua; in der Attrappe mit Zeichencodes testen.

### B5 (minor) -- Drossel verwirft die zweite Bitte binnen 500 ms still, auch nach einer abgelehnten
- **Stelle:** `S:server/BanditsNPCBearFollow.lua:52-71`, Aufruf `:173` VOR der Pruefung von `args.id` (`:174`) und vor Besitz/Zustand.
- **Beleg:** `AP` 3i: Bob bittet (abgelehnt, fremdes Junges), 100 ms spaeter "Mode" fuer sein eigenes -> keine Meldung, kein Wechsel. Ebenso
  "Follow me" und gleich danach "Name the cub" -> OK im Fenster tut nichts. Keine rote Linie, aber "geht manchmal nicht".
- **Vorschlag:** die Uhr erst NACH den Feldpruefungen stellen und je Befehl getrennt drosseln (`pkey .. command`), oder bei verworfener Bitte
  eine kurze Meldung. Deckel 64 bleibt.

### B6 (minor) -- "Hold out food" erscheint auch fuer das eigene FOLGENDE Junge (ohne Wirkung)
- **Stelle:** `S:client/BanditsNPCBearMenu.lua:352-363` (`:360` `st == "tame" and c.owner == key`).
- **Warum:** beim Folgen rechnet der Schreiber `B.FollowDecide` statt `B.Decide` (`S:server/BanditsNPCBearServer.lua:710-713`); Futter in
  der Hand spielt dort keine Rolle (Plan 1.2). Der Punkt ist dann Menue-Muell (Kevin: kein Muell in der Stadt).
- **Vorschlag:** `and B.ModeOf(c) ~= "follow"` fuer `tame`.

### B7 (minor) -- `stayR` 8 = Wander-Wurf +-8: das bleibende Junge rennt oft zur Heimat zurueck
- **Stelle:** `S:shared/BanditsNPCBear.lua:70`, `S:server/BanditsNPCBearServer.lua:722`, Regel 8 `S:shared/BanditsNPCBearRules.lua:316-319`.
- **Warum:** die Engine wuerfelt beim Wandern +-8 Kacheln um das TIER selbst (`forschung_b1b.md:120`, `dec/BaseAnimalBehavior.java:165-225`);
  nach zwei Wuerfen in dieselbe Richtung ist es ueber 8 -> `fleeTo` (immer RENNEN) zurueck. Sieht wie grundloses Sprinten aus; steht es dabei
  fest, kommen `B.MoveWatch`-Zeilen (B1a, gedrosselt 60 s). Keine rote Linie, Gefuehlsfrage.
- **Vorschlag:** `stayR` 10-12 (Kevin fuehlt es im Test 8.4 Schritt 9) oder Plan-Frage 3 so stellen.

### B8 (minor, Randfall MP) -- Besitzerschluessel `__sp` im Mehrspieler
- **Stelle:** Client `S:client/ISUI/BanditsNPCBearHud.lua:151` (`c.owner == B.SP_KEY` zaehlt als "eigen"), `S:client/BanditsNPCBearClient.lua:211`
  (`__sp` -> eigener Vorname); Server `S:shared/BanditsNPCBear.lua:277-283` (MP-Schluessel = Kontoname ohne Pruefung).
- **Warum:** heisst ein MP-Konto woertlich `__sp`, zeigt jeder Client dessen Junges als "eigen" mit SEINEM Vornamen und "staying"; auf einem
  Server aus einem SP-Spielstand (Besitzer `__sp`, `bau_b1b_zusammenbau.md` 6.4) wuerde dieses Konto Besitzer aller alten Jungen (Folgen,
  Name, Fuettern). Ob PZ den Kontonamen `__sp` zulaesst: **ungeprueft**.
- **Vorschlag:** Client: `B.SP_KEY` nur im SP als "eigen" werten (`B.IsSP()`); Server: im MP einen Kontonamen `__sp` nie als Schluessel
  annehmen (z. B. `PlayerKey` gibt nil -> Bitte verworfen).

## 2. Geprueft ohne Befund (mit Fundstelle)

### Folgen / Bleiben
- Rechnen nur beim Schreiber: `liveRec` -> `B.FollowStep` (`S:server/BanditsNPCBearServer.lua:709-713`); Client schickt nur "Mode"
  (`S:client/BanditsNPCBearMenu.lua:117-121`). SP: `B.Ask` -> `B.Handle` direkt (`S:shared/BanditsNPCBear.lua:437-446`); MP: `sendClientCommand`.
- Besitzer ueber den Schluessel, naechster anwesender (`buildEnv` `S:server/BanditsNPCBearServer.lua:624-648`). Zwei Besitzer mit je einem
  Jungen: getrennt (`AP` 3a: nur Bobs Junges bleibt im Auto, Meldung nur an Bob). Offline / tot: `B.Players` filtert (`S:server/BanditsNPCBearWorld.lua:40`, `:53`)
  -> Regel 10 ohne Meldung (`AP` 3b). SP-Tod: neue Figur hat wieder `__sp` -> bleibt Besitzer.
- Auto: `car` je Spieler beim Schreiber (`S:server/BanditsNPCBearWorld.lua:44`, `:55`), Regel 11 vor allem anderen; Bitte "follow" aus dem Auto
  abgelehnt (`S:server/BanditsNPCBearFollow.lua:205-208`); Menue grau (`S:client/BanditsNPCBearMenu.lua:220-223`).
- Zu weit: Regel 12 mit Sandbox-Deckel (`S:shared/BanditsNPCBearRules.lua:380`), Bitte ebenso (`S:server/BanditsNPCBearFollow.lua:209`);
  Max 60 + `loadRing` 12 < 76 geladene Kacheln.
- Treppen: Regel 13 haelt auf der anderen Ebene (Sperre je Takt), "zu weit" gilt weiter; `floor` auf beiden Seiten (`:381`). Ein Besitzer
  mitten auf der Treppe (gebrochenes z) zaehlt als dieselbe Ebene -- unschaedlich.
- Haengen: Engine-Weg hat laut Jar einen Zeitdeckel (Plan 1.2); unser Code schickt im Fest-Fall hoechstens je 10 s einen Befehl, sonst je
  1,2 s und nur bei Bedarf. `B.MoveTo` faellt bei Wasser/ungeladen auf fuenf Punkte zurueck, dann nichts (`S:server/BanditsNPCBearWorld.lua:504-512`).
- Wechsel nach Bleiben: Heimat = aktuelle Kachel, Folgen-Sitzung und Gegenprobe geleert (`S:server/BanditsNPCBearFollow.lua:79-88`); eine alte
  Sperre loest der naechste Takt (Regel 9 -> `steer` `:663-665`). "Vermisst" setzt still Bleiben (`S:server/BanditsNPCBearServer.lua:767-770`).
- Speichern/Laden: `mode`/`name` im Register, `InitRegistry` prueft beide (`S:server/BanditsNPCBearRegistry.lua:91-105`), Sitzung nie
  gespeichert; SP folgt nach dem Laden weiter (ausser B3), MP nach Neustart "staying" (Regel 10).

### Namensschild
- Liste hoechstens 1 x/s, alle Texte dabei fertig (`S:client/ISUI/BanditsNPCBearHud.lua:404`, `:147-166`); je Bild je Schild 1
  `isExistInTheWorld`, 3 Lagefragen, 2 Umrechnungen, 4 `drawTextCentre` (`:363-382`, `:329-339`); Deckel `hudMax` 6, `hudDist` 20; geteilter
  Bildschirm zeichnet nichts (`:402`). Schrifthoehen einmal (`:405-419`).
- Balken und Schild am selben Anker `a:getZ() + tagZ` (`:373`); beide wachsen nach oben, Unterkante Zeile 2 = Anker (`:330`, `:356`).
- Fremde im MP: Name bzw. "<Konto>'s cub" / "belongs to <Konto>" (`:161-165`); Sicht an alle in 60 Kacheln bei Name/Zustand
  (`S:server/BanditsNPCBearServer.lua:76-101` ueber `B.Touch`), ein folgendes Junges erreicht neue Zuschauer ueber `pushNewSights` (`:823-846`).
- Client-Suchlauf fuer ein weit entferntes eigenes Junges: 5 x 1 s, 12 x 5 s, dann je 30 s (`:262-281`) -- gedeckelt.

### Umbenennen
- Fenster genau wie Vanilla (`V:client/ISUI/ISTextBox.lua:110-114`, `:173-186`, `:280`): Pruefer `validateFunc(nil, text, nil, nil)` passt zu
  `validName(_target, text)`; `maxChars`/`noEmpty` greifen zusaetzlich.
- Server: Vorab-Deckel 4 x 24 vor jeder Zeichen-Schleife (`S:server/BanditsNPCBearFollow.lua:226`, `AP` 3g), Besitz/Zustand (`:230`), dann
  `CleanName`; Fremde abgelehnt (`AP` 3h); Tabulator/Steuerzeichen < 32 abgelehnt (`AP` 3c). Name nur im Register (kein `setCustomName`).
- Name in Meldungen: `getText(key, name)` setzt ueber Javas `String.formatted` ein (Jar `zombie/core/Translator.getText` ->
  `reportMissingArgumentsFromPastAbuse` -> `String.formatted`, javap, nur gelesen) -- ein `$` oder `\` im Namen bricht nichts; `%` lehnt
  `CleanName` ohnehin ab.

### Futter hinhalten
- Nur `ISWorldObjectContextMenu.equip(p, hand, food, true, false)` (`S:client/BanditsNPCBearMenu.lua:133-136`); Vanilla holt das Stueck
  ueber `transferIfNeeded` und stellt `ISEquipWeaponAction` an (`V:client/ISUI/ISWorldObjectContextMenu.lua:2606-2613`) -- kein Gegenstand
  erzeugt oder vernichtet, Abbruch laesst das Stueck im Inventar (Vanilla), kein eigener Netzweg, kein Kick. Verdorbenes steht nicht in der Liste
  (`S:shared/BanditsNPCBearFood.lua:58`, `:81-84`). Vanillas Locken nicht benutzt.
- Danach die B1a-Regeln: mit Futter in der Hand flieht das scheue Junge nicht (Regel 1 nur ohne Futter oder im Lauf), kommt im Stand bis 3,
  haelt beim Hingehen (Regel 3) -- das loest N6/N8 (kein Hinterherrennen).

### Waisen (N5)
- Riegel 1 (Objekt der Sitzung), Riegel 2 (AnimalID eines Eintrags ohne lebendes Objekt -> nie entfernt, unabhaengig vom Abstand),
  Riegel 3 (Alter >= 30 s, niemand in 25, SP nicht im Blick) -- `S:server/BanditsNPCBearWorld.lua:302-463`. `AP` 2a: gueltiger Eintrag,
  Spiegel geloescht, Kachel im Register 60 Kacheln daneben, niemand nah, 320 s -> nicht entfernt. Gegenprobe 2b: Spiegel UND AnimalID weg -> geraeumt (Grenze).
- Spiegel und AnimalID ueberleben Speichern/Laden und Kopien (Jar `dec/IsoAnimal.java:1276`, `:1279`, `:1387`, `:1391`; `copyFrom` `:2089-2098`).
- Neues Junges: Spiegel sofort in `B.NewRec` (`S:server/BanditsNPCBearRegistry.lua:197-198`) plus `s.obj` -> nie Kandidat.
- Nur `ncbearcub`, nur ueber `B.RemoveCub` (`S:server/BanditsNPCBearWorld.lua:253-261`, MP mit `removeAnimal`); Kandidaten <= 16, Waisen-Lauf
  je 120 s am Ende des Takts (ein MP-Fehler von `getObjectListForLua`, A3, kostet dann nur diesen Lauf).

### Zusammenspiel mit B1a
- Zaehmen: `mode` fehlt = Bleiben, Heimat = letzte Fuetterung (Zaehmen setzt immer eine Fuetterung voraus: `B.CheckPet` braucht `bond`).
- Tod: am gemerkten Objekt (`resolve`, `S:server/BanditsNPCBearServer.lua:738-740`), Sperre und Meldung wie B1a; Schild verschwindet mit der Sicht.
- Fuettern/Streicheln am folgenden Jungen: Regel 14 haelt bei `d <= 3`, Reichweite der Aktionen < 3 -- die Sperre der Zeitaktion wird nicht geloest.
- Koeder, Sperre, Vermisst: unveraendert; Fix 2 (`tHas`, `S:shared/BanditsNPCBear.lua:255-273`) und Fix 3 (`S:shared/BanditsNPCBearDefs.lua:60`,
  `S:shared/TimedActions/BanditsNPCBearPetAction.lua:66`, `:76`) sind da.

## 3. SP- und MP-Zweig

| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Follow/Stay, Name | `B.Ask` -> `B.Handle` direkt, Meldung/Sicht direkt | Client bittet, Server prueft Besitz, Zustand, Objekt, Auto, Abstand, Name; Note an den Bittenden, Sync an Besitzer + 60 Kacheln |
| Folgen-Takt | das eine Programm (B1/B2 gelten hier wie dort) | nur der Server; Client schickt nichts |
| Auto / weg / offline | Auto, zu weit, entladen (B3); tot = offline | dazu getrennt (Regel 10, ohne Meldung); nach Neustart "staying" |
| Schild | Vorname der Figur | Kontoname (B8 Randfall) |
| Futter hinhalten | Vanilla `equip` | Vanilla `equip` (Zeitaktion), Server liest die Hand wie B1a |
| Waisen | `B.SeenInSP` schuetzt Gesehenes | nur Abstand 25 (kein Sichtfeld am Server); `getObjectListForLua` am Server weiter A3 |

## 4. Leistung
Je Hirn-Takt (1,5 s) und folgendem Jungen: 1 `getModData`, eine Spielerschleife, reine Rechnung, hoechstens 1 `fleeTo` (Weg-Suche) -- gedeckelt
ueber `BearMaxPerPlayer` (1-4). Waisen: eine Objektliste je 120 s. Drossel-Tabelle 64, Waisen 16, Sitzungen je Eintrag (<= 64, beim Schliessen
geloescht). Client: Liste 1 x/s, je Bild nur Zeichnen aus der Liste. Nichts Teures je Bild. Mit B1 behoben wird das Junge ~1 Weg je 1,5 s
anfordern statt je 10 s -- das ist der geplante Normalfall (Plan 11).

## 5. Attrappe `attrappe/pruef_b1b/`
- `run.lua` (laedt `attrappe/kern/attrappen.lua` unveraendert und den echten Kern aus dem Staging), Ausgabe `ergebnis.txt`:
  Fall 1 Folgen mit Bewegungsmodell (1a-1d), Fall 2 Waisen nach dem Laden + erster Takt (2a-2c), Fall 3 MP zwei Besitzer, boese Namen,
  Drossel (3a-3i). Ergebnis: BEFUND 1a, 1b, 1c (B1), 2c (B3), 3d, 3e, 3f (B4), 3i (B5); OK 1d, 2a, 2b, 3a, 3b, 3c, 3g, 3h; 0 `***`-Zeilen.
- `spur_1a.lua` / `spur_1a.txt`: je Hirn-Takt Abstand, Regel, `bestD`, `stuck` fuer Fall 1a.
- Grenze: das Bewegungsmodell kennt keine Wege, Anlauf, Tueren; die Ursache von B1 liegt aber in der Takt-/Ziel-Rechnung (Abschnitt B1) und
  haengt nicht an diesen Einzelheiten.

## 6. Offen / ungeprueft
1. Alles Laufzeitverhalten (Wege, Tempo im Spiel, Treppen, Q-Ruf, MP-Ruckeln) -- ungespielt.
2. B3: ob die Kacheln im SP beim ersten `OnTick` nach dem Laden schon da sind.
3. B8: ob PZ den Kontonamen `__sp` zulaesst.
4. Bekannte Grenzen (kein Befund): geteilter Bildschirm (Folgen nimmt den naechsten lokalen Spieler, kein Schild, kein "Hold out food");
   zwei Junge eines Besitzers laufen zum selben Punkt; MP-Waisen nur ueber Abstand; A3 wie B1a.

Statisch geprueft, nicht gespielt.
