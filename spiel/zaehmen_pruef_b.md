# Lauf baer-zaehmen (B1a): PRUEFER B -- Logik, Einzelspieler/Mehrspieler, rote Linien, Leistung

Stand 10.11.2026. **Statisch geprueft, nicht gespielt.** Keine Datei geaendert ausser diesem Bericht und den eigenen Attrappen
(`attrappe/pruef_b/run.lua`, Ausgabe `attrappe/pruef_b/ergebnis.txt`). Gelesen: PLAN_ZAEHMEN.md ganz, bau_kern.md, bau_oberflaeche.md
(Ueberblick), schnittstelle_aenderungen.md, FE 0/1/4-8, alle 15 Lua-Dateien ganz, ENTSCHEIDUNGEN.md (Bekommen/Zaehmen, 10.11.).
Kurzformen: `S` = `server/BanditsNPCBearServer.lua`, `W` = `server/BanditsNPCBearWorld.lua`, `R` = `server/BanditsNPCBearRegistry.lua`,
`K` = `shared/BanditsNPCBear.lua`, `Ru` = `shared/BanditsNPCBearRules.lua`, `F` = `shared/BanditsNPCBearFood.lua`,
`FA`/`PA`/`BA` = die drei Zeitaktionen, `M` = `client/BanditsNPCBearMenu.lua`, `C` = `client/BanditsNPCBearClient.lua`,
`H` = `client/ISUI/BanditsNPCBearHud.lua`. Alle Pfade unter `_arbeit/baer_zaehmen/mod/42/media/lua/`.

Bestehende Attrappen laufen weiter gruen (kern 133/0, gesamt 175/0). Meine drei Faelle zeigen vier Befunde (B1, B2, B3, B4).

---

## 1. Befunde

### B1 (blocker, MP) -- "Hello" kommt beim Server mit `args = nil` an und wird verworfen; ein neu verbundener Spieler bekommt keine Sicht
- **Code:** Client bittet mit leerer Tabelle: `C:210` `B.Ask(player, "Hello", {})`, `K:412-416` `sendClientCommand(player, B.CMD, command, args)`.
  Server verwirft alles ohne Tabelle: `S:376-380` `if type(args) ~= "table" then return end` (und noch einmal `S:353`).
- **Engine (Jar 42.22.2, javap):** `GameClient.sendClientCommand` Offset 47-67: `putBoolean(args != null && !args.isEmpty())` -- eine LEERE Tabelle
  wird als "keine args" geschickt. `GameServer.receiveClientCommand` Offset 18-28: `getBoolean()`, bei false bleibt die Tabelle `null`.
  Dasselbe im SP-Netzweg `dec/SinglePlayerServer.java:180-201`. Vanilla rechnet damit: `V:server/ClientCommands.lua:1349` `if args then`,
  `V:client/ServerCommands.lua:210-213` ("Can be nil if sending an empty table").
- **Zweiter Weg faellt auch aus:** `S:763` schickt eine Sicht nur, wenn `B._sig[e.uid] ~= nil` -- ein Spieler, der zum ersten Mal in der
  Liste steht, bekommt KEINE Sicht, nur seine Signatur wird gemerkt. Danach nur noch bei Aenderung (neues Junges in 60 Kacheln, OnlineID)
  oder `B.Touch` in seiner Naehe (`S:67-92`). `d.all` setzt nur `R:102` beim Register-Start.
- **Gegenbeispiel (Attrappe Fall 1, MP-Server):** Junges 40 Kacheln vom neu verbundenen Spieler, nichts aendert sich: nach "Hello" (args nil)
  0 Syncs, nach 10 Hirn-Takten weiter 0 Syncs; Gegenprobe mit nicht leerer Tabelle: 1 Sync.
- **Folge im Spiel (MP):** `U.Fresh()` bleibt falsch (`C:191-197`) -> `M:294-295` `if not me then return end`: **der Koeder-Punkt erscheint
  im MP nie**, solange keine Aenderung in der Naehe passiert; Balken (`H:185`) fehlt, Menue-Vorpruefung fehlt (Punkte frei, der Server
  lehnt dann ab). Der Client fragt erst 12 x alle 10 s, dann jede Minute weiter (`C:221-237`) -- ewig, aber gedeckelt. Nach einem
  Wiederverbinden bekommt auch der Besitzer seines zahmen Jungen keine Daten. Kein Kick, kein Gegenstand betroffen. MP-Test 10.2 Schritt 5
  (B legt Koeder) scheitert.
- **SP:** nicht betroffen (`K:418-420` ruft `B.Handle` direkt mit der Tabelle).
- **Vorschlag:** (a) `B.Ask(player, "Hello", { v = 1 })` (nie leer) UND (b) im Server `onClientCommand` fuer "Hello" `args = args or {}`
  zulassen; (c) `S:763` auch beim ersten Eintrag schicken: `if B._sig[e.uid] ~= sig then` (erstes Mal = nil ~= sig) -- dann bekommt jeder
  neu Verbundene im ersten Takt seine Sicht, auch ohne Hello. Attrappe: Fall 15 der Gesamt-Attrappe reicht `{}` unveraendert durch und
  bildet die Engine hier nicht nach (`gesamt/run.lua:483`).

### B2 (major, MP) -- Junge von Spielern, die nicht wiederkommen, bleiben fuer immer und fuellen den Welt-Deckel
- **Code:** Die Verschwinde-Uhr laeuft nur, wenn der Finder (bei `fed`: bond) online ist: `S:430-433` `relevant = online[key] == true`,
  `Ru:227` `if relevantOnline and dtH > 0 then idle = idle + dtH end`. Ungezaehmte (new/shy/fed) zaehlen fuer den Welt-Deckel:
  `R:121-128` (`CountWild`), Pruefung `S:106` und `S:494`. Die Aufgabe-Frist `fed -> shy` (168 h) laeuft auch nur mit bond online (`Ru:229-231`).
- **Gegenbeispiel (Attrappe Fall 2, MP-Server):** 8 Spieler bekommen je ein Junges und verlassen den Server; 300 Spielstunden Langsam-Takt:
  alle 8 Eintraege stehen noch, groesstes `idleH` = 0. Ein neuer Spieler: `B.AppearFor` -> `UI_BN_Bear_Why_Full`; der Wald-Wurf
  (`S:494`) wuerfelt fuer niemanden mehr. Auf einem oeffentlichen Server reicht es, dass 8 Leute (Vorgabe `BearCubWorldCap` 8) ein Junges
  bekommen und nie wiederkommen -- danach erscheint fuer **niemanden** mehr ein Junges im Wald (Koeder-Junge auch nicht, `S:106`).
- **Plan ist sich selbst uneinig:** PLAN 2 Zeile 119 "zaehlt nur, waehrend der Finder online ist", aber Zeile 130 "`idleH` laeuft weiter (ein
  unbeobachtetes Junges zieht weiter)". Der Code folgt Zeile 119.
- **SP:** nicht betroffen (der einzige Schluessel `__sp` ist immer online, solange das Spiel laeuft).
- **Vorschlag:** die Uhr bei abwesendem Finder/bond ebenfalls laufen lassen (ggf. langsamer), oder Junge abwesender Finder nicht in
  `CountWild` zaehlen; fuer `fed` die 168 h auch ohne bond online zaehlen (bond weg, Balken halbiert -- das ist ohnehin die Regel).
  Kevin fragen, falls "nur online" Absicht ist.

### B3 (minor, ungeprueft: Engine-Zeitpunkt) -- angefuettertes Junges wird nach ~15 s "Luecke" geschlossen, Fortschritt weg
- **Code:** `S:678-694` zaehlt jeden Eintrag ohne Objekt bei geladener Gegend (`W:104-115`, nur Kacheln) als fehlend; nach 3 Suchlaeufen
  (`scanMs` 5 s, `K:33`, `K:44`) wird ein nicht zahmes Junges geschlossen (`S:702-711` -> `B.Close(rec, "lost")`). Kommt das Tier danach,
  traegt es den Spiegel `st = "fed"` und gilt nicht als "stale" (`W:304`); beim naechsten Anfassen legt `R:207-212` einen NEUEN Eintrag
  `found`/`shy` ohne bond und Balken an.
- **Wann:** die Tiere einer frisch geladenen Kachel kommen ueber den Tier-Worker zurueck (`FE 1.4`, `dec/AnimalManagerMain.java:58-113`,
  asynchron) -- wie lange die Kacheln schon da sind, bevor das Tier wieder in der Liste steht: ungeprueft.
- **Gegenbeispiel (Attrappe Fall 3a/b, SP):** Junges gefuettert (Balken 14, bond `__sp`), Tier 18 s nicht in der Welt bei geladener Gegend
  -> Eintrag geschlossen, Meldung `Why_Gone`; Tier wieder da, gefuettert -> neuer Eintrag `b2`, src `found`, `fedN` 1 (alter Fortschritt weg).
- Gezaehmte sind geschuetzt (gehen nach `missing`, `S:703-708`, und kommen zurueck, `S:639-644`). Kein Gegenstand betroffen.
- **Vorschlag:** `fed` wie `tame` behandeln (erst `missing`-artig warten), oder Fehlversuche in Spielminuten statt in 5-s-Laeufen zaehlen;
  `W:304` koennte Tiere mit Spiegel auf einen geschlossenen `fed`-Eintrag ueber `aid` wieder anbinden. Testpunkt im Spiel: Gegend verlassen
  und wiederkommen, `NCBear_CubInfo()`.

### B4 (minor) -- Fuettern am gezaehmten Jungen verbraucht ein Stueck und meldet "+0 Vertrauen"
- **Code:** `S:221-230` nimmt das Stueck und ruft `tellGain` ohne Unterscheidung; `Ru:88-104` gibt am zahmen Jungen `gain = 0`; `S:184-191`
  meldet dann `Note_Gain`/`Note_GainFav` mit `v = 0`. Das Menue bietet es an (`M:125-139`, `B.CheckFeed` erlaubt dem Besitzer, `Ru:144-145`).
  Beim Streicheln gibt es dafuer den Zweig `wasTame` -> `Note_Happy` (`S:252-262`).
- **Gegenbeispiel (Attrappe Fall 3c, SP):** zahmes Junges, Honig gefuettert -> `true`, Honig weg, Meldung `UI_BN_Bear_Note_GainFav` mit `v = 0`
  ("+0 trust - it loves this!").
- PLAN 11 Zeile 871: am zahmen Jungen "nur Abklingzeit und Meldung". Kein Verlust im Sinn der roten Linie (gewollter Verbrauch), aber
  die Meldung ist falsch.
- **Vorschlag:** in `B.FeedComplete` wie in `B.PetComplete` `wasTame` merken und dann `Note_Happy` melden.

### B5 (minor) -- reifer Koederplatz verfaellt nie; der 16er-Deckel kann sich im MP fuer immer fuellen
- **Code:** `S:388` `if not bait or bait.ready then return end` -- ein reifer Platz zaehlt keine Morgen mehr, also auch keinen Verfall.
  Erscheinen nur bei geladener Kachel und Spieler 20+ Kacheln weg (`S:725-727`); traegt der Besitzer gerade ein wildes Junges, bleibt der
  Platz stehen (`S:730`, `why == "UI_BN_Bear_Why_HasCub"`). Deckel `S:313` (`maxBaits` 16, `K:45`).
- **Gegenbeispiel (statisch):** 16 Spieler legen je einen Koeder, er wird reif, sie verlassen den Server bzw. kommen nie wieder in 20-38
  Kacheln der Stelle -> alle Plaetze bleiben, jeder weitere Spieler bekommt `Why_Full` (`S:313-315`). PLAN 5.2 "reifer Platz haengt nicht
  still (Hinweis, Verfall)". Aufgeben (`S:358-371`) kann nur der Besitzer.
- **Vorschlag:** reifer Platz verfaellt nach z. B. `BearBaitNights + baitExtra` Tagen ab `t0` (Meldung `Bait_Expired`).

### B6 (minor, Leistung) -- zwei Suchlaeufe, die lange alle 5 s laufen koennen
- **Server:** ein zahmes Junges im Zustand `missing` mit geladener letzter Kachel (z. B. im Anhaenger, oder weggefuehrt) haelt `need` wahr
  (`S:688-691`), also `getObjectListForLua()` (kopiert die ganze Objektliste der Zelle, FE 1.2) alle 5 s (`S:780-783`) -- bis zu 24 Stunden,
  in denen der Besitzer online ist (`S:450-455`). Im MP mit vielen Zombies teuer, aber gedeckelt.
- **Client:** die Sicht traegt das eigene gebundene/zahme Junge unabhaengig vom Abstand (`R:416-417`); `H:207-209` will fuer jedes `fed`
  einen Balken, findet kein Objekt -> Suchlauf jede Sekunde (5 x), dann alle 5 s (`H:221-233`), solange das Junge ausserhalb der geladenen
  Gegend steht -- also im Grunde immer, wenn man sich vom angefuetterten Jungen entfernt.
- **Vorschlag:** Server: fuer `missing` nur jeden n-ten Takt suchen bzw. Abstand verdoppeln; Client: Sicht-Eintrag mit `x, y` schicken und
  nur suchen, wenn die letzte Kachel in `hudDist` liegt.

### B7 (minor, ungeprueft) -- der Hirn-Takt kann die Sperre einer laufenden Zeitaktion loesen (SP)
- **Code:** Takt und Aktion teilen dasselbe `setBlockMovement`. `S:629-631`: bei `act == "free"` und `s.held` -> `B.Hold(rec, a, false)`
  (`W:368-378`). Die Streichel-Aktion setzt die Sperre in `start` (`PA:180`), der Spieler hat beim Streicheln meist KEIN Futter in der Hand
  -> beim angefuetterten Jungen greift Regel 9 `free` (`Ru:300-316`). Hatte der Takt vorher gehalten (Spieler kam mit Futter), loest der
  naechste Takt waehrend des Streichelns die Sperre; das Junge kann wandern (wanderMul 600, `shared/BanditsNPCBearDefs.lua:95`), `isValid` (`PA:142-150`, Abstand < 3)
  bricht dann ab -> kein Punkt, kein Verlust. Im MP setzt die Aktion die Sperre nur an der Client-Kopie (FE 8.2), dort zaehlt der Takt des
  Servers allein. bau_kern.md nennt es selbst als Testpunkt.
- **Vorschlag:** Regel 7 auch ohne Futter fuer bond/owner in `reach` (stehen bleiben, wenn der eigene Mensch direkt daneben steht).

---

## 2. Vorgaenge Schritt fuer Schritt

### 2.1 Erscheinen im Wald
`Events.EveryTenMinutes` (`S:831`) -> `B.SlowTick` (pcall um eigenen Code, `S:548-554`) -> `slowTickBody` (`S:523-546`): `dt` gedeckelt
auf 1 h (`S:531`), `B.Players()` (`W:29-54`: Server `getOnlinePlayers`, SP `getSpecificPlayer`), `B.CleanLocks`, je Eintrag `slowRec`,
dann `forestRolls` (`S:484-505`): Schalter (`S:485`), Rate (`S:486`), je Schluessel einmal (`S:491`), `B.MayAppear(B.SlotsOf)` (`Ru:189-197`,
`R:216-246`), Welt-Deckel, Wurf `ZombRand(10000) < pct*100/6` -> `B.PickForestSquare` (`W:148-178`: 8 Versuche im Ring, Min..Max geklemmt
auf 65, Wald, `SquareFits`, Abstand zu allen >= Min, SP `isCanSee`) -> `B.AppearFor` (`S:98-134`): Register, Schreiber, `MayAppear`
erneut, Deckel, `B.CreateCub` (`W:226-246`, einziges `addAnimal`, Gegenprobe `isExistInTheWorld`) -> `B.NewRec` (`R:145-172`, Deckel 64;
bei Fehlschlag `B.RemoveCub`, `S:113-116`) -> `B.Commit` (Spiegel) -> Hinweis mit Richtung -> `B.FlushViews`.
SP und MP gleich; MP ohne Sichtfeld (`W:120-128`, ehrliche Grenze). Kein Client-Weg. Befund B2 (Deckel).

### 2.2 Koeder legen / aufgeben / Nacht / Morgen
- **Legen:** `M:280-324` (nur mit frischer Sicht, `M:294-295` -> Befund B1 im MP), `M:250-278` Untermenue, `M:98-104` `walkAdj` +
  `transferIfNeeded` + `BA:new(character, food, x, y, z)`. Server/SP: `BA:279-283` -> `B.BaitComplete` (`S:291-346`): Schalter, Kachel
  geladen und <= 3 (`S:274-282`), `SquareFits`, Wald in 8, `B.CheckBait` (`Ru:175-186`), 16er-Deckel, Abstand 10, `contains`,
  verdorben, Honig/Fisch; erst dann `takeOne` (`S:166-176`: `removeFromHands`, `Remove`, `sendRemoveItemFromContainer`, Gegenprobe
  `contains`) und im selben Aufruf `B.NewBait` (`R:366-377`). Ablehnung: Meldung, `false`, nichts verbraucht. Zwei Klicks: der zweite
  scheitert an `Bait_HasOne`. Client-Koordinaten werden gegen den Spieler (<= 3) geprueft -- kein Client-Glaube.
- **Aufgeben:** `M:240-248` -> `B.Ask("BaitDrop", { id })` -> `S:358-371` prueft `bait.owner == pkey`. Fremde id: nichts.
- **Nacht/Morgen:** `S:508-521` merkt `wasNight` (`W:68-74`), am Morgen `B.BaitDawn` (`S:387-412`): Spieler in 20 -> `miss+1`, ab 4
  Verfall; sonst `nights+1`, Wurf mit `B.BaitChance` (`Ru:201-208`). Befund B5 (reif verfaellt nie).
- **Erscheinen:** Hirn-Takt `S:718-747`: reif, Kachel geladen, niemand in 20, SP nicht sichtbar, Besitzer berechtigt (`HasCub` wartet,
  anderes -> Verfall) -> `B.FreeSquareNear` (`W:182-199`, hoechstens 25 Kacheln) -> `B.AppearFor(..., "bait")` -> Heimat = Platz, Platz weg.

### 2.3 Entdecken, Verhalten
`Events.OnTick` (`S:832`) -> `B.BrainTick` (Drossel 1,5 s / 10 s, `S:814-824`) -> `brainTickBody` (`S:773-811`): `resolve` (Tod, fehlend,
`S:678-694`), Suchlauf gedrosselt 5 s (`S:780-784`, `W:286-359`), je geladenem Jungen `liveRec` (`S:635-675`): Ort, `missing -> tame`,
`buildEnv` (`S:589-616`, Hand/Tempo nur fuer Spieler in 15, je Takt gemerkt `S:562-575`), `goneP` vollziehen (25 Kacheln, SP unsichtbar,
`S:652-658`), `new -> shy` mit `Note_Seen` (`S:659-664`), `B.Decide` (`Ru:271-317`), `steer` (`S:619-632`) -> `B.Hold`/`B.MoveTo`
(`W:368-415`, Laufbefehl hoechstens alle 3 s, Wasser/ungeladen -> Ersatzpunkte, sonst nichts). Danach Koeder, Spieler-Orte, Sicht.
Befund B7.

### 2.4 Fuettern
`M:72-83`: Warteschlange leeren, `equip` (holt aus der Tasche), `walkAdj(..., true)`, `FA:new(player, animal, food)`. Client/SP:
`FA:26-35` isValid (billig), `FA:49-61` start (Sperre, `NCBearAct = eat`, Ton), jeder Ausgang `FA:64-91` loest Sperre und Variable.
Schreiber: `FA:94-98` -> `B.FeedComplete` (`S:201-235`): `handCheck` (`S:142-161`: Art, da/lebt, Abstand < 3, `RecOf`), `CheckFeed`
(`Ru:141-158`: Besitz/Bindung, Plaetze, Sperre, Abklingzeit), `contains`, `FoodClass` (`F:45-61`), `takeOne`, `ApplyGain` (`Ru:85-117`),
Heimat, `Commit`, Meldungen, Sicht.
- **Gegenstand genau einmal:** nur der Schreiber nimmt (`S:221`), erst nach allen Pruefungen; Gutschrift nur, wenn `contains` danach falsch
  ist (`S:171-174`). Abbruch der Aktion: `complete` laeuft nicht (SP nach `perform`, MP Server), nichts genommen. Volles Tier
  (Abklingzeit): `Why_FeedWait`, nichts genommen. Tier waehrenddessen weg/tot: `handCheck` -> `Why_Gone`, nichts genommen. Zwei Spieler
  gleichzeitig: der zweite scheitert an `bond ~= pkey` (`Ru:146-147`). Server lehnt ab, nachdem der Client angefangen hat: `false`, Client
  bricht ab (FE 8.2), nichts genommen. Futter in der Hand: `removeFromHands` vor `Remove`. Doppelklick mit Abklingzeit 0: zwei Stuecke,
  zwei Gutschriften (kein Verlust). In Ordnung bis auf Befund B4 (zahmes Junges).
- **Kick:** der Client entfernt nichts, schickt keine Mengen; das Stueck des Servers kommt ueber die Aktion (FE 8.2 Nr. 4).

### 2.5 Streicheln
`M:86-94` -> `PA:new(player, animal)`; `PA:165-181` Haltung fest 0.5, Sperre; `PA:184-209` jeder Ausgang loest. Schreiber `PA:212-216`
-> `B.PetComplete` (`S:242-267`): `handCheck`, `CheckPet` (`Ru:160-172`: ungefuettert -> `Why_Shy`, fremd -> `Why_Other`, zahm nur Besitzer,
Abklingzeit), `ApplyGain`, `animal:petAnimal`, `Commit`, `Note_Happy` bzw. Punkte. Kein Gegenstand.

### 2.6 Zaehmen, Zahlen
`Ru:68-80` `TameCheck`: `tame >= 100`, `st == fed`, bond, `fedN >= BearTameMinFeedings` -> `tame`, `owner = bond`; sonst 99.
Vorgaben (`K:65-85`) = PLAN 3.1; `B.CFG` (`K:32-62`) = PLAN 3.3 plus Zusatz. `B.Opt` (`K:110-129`) klemmt Typ und Bereich, Rueckfall auf
die Vorgabe; mit NPC Crew `BanditsNPC.Opt(name, def)` (NC `shared/BanditsNPC.lua:6101-6109`). Randwerte: `BearTameMinFeedings 0` ok
(Bindung noetig), `BearTamePetPoints 0` ok, `BearCubVanishHours 0` = nie (Absicht, verschaerft aber B2), `BearDeathLockDays 0` -> nur
`Note_Dead` (`R:274-285`, `R:321-326`), `BearBaitNights 1` -> 100 % (`Ru:206`), `BearCubsEnabled false` -> keine neuen, vorhandene zaehmbar
(`CheckFeed` fragt den Schalter nicht), reife Koeder verfallen dann (`S:730-733`). Kevins Worte (ENT:41, :99, :104, :107, :34, :45)
sind abgebildet: Weg A + C, Balken, Mischung, Streicheln immer mit Abklingzeit, einer je Spieler, 7 Tage.

### 2.7 Verschwinden, Tod, Sperre, Vermisst
- **Verschwinden:** `slowRec` (`S:449-481`) -> `B.VanishStep` (`Ru:217-236`) -> `goneP`; vollzogen im Hirn-Takt (`S:652-658`, `B.RemoveCub`
  `W:253-258` loest vorher die Sperre) oder, bei nicht geladener Gegend, Eintrag schliessen (`S:476-479`) und spaeter das verwaiste Tier
  ueber `W:302-308`, `W:347-357` entfernen. Befund B2.
- **Tod:** `S:683-688`: nur `isDead()` am gemerkten Objekt -> `B.Close(rec, "dead")` (`R:311-336`): Eintrag weg, bei `tame/missing` Sperre
  `now + Tage*24` (`R:274-285`). Sperre wirkt in `MayAppear`, `CheckBait`, `CheckFeed` (nur beim Binden) und raeumt sich (`R:288-299`).
- **Vermisst:** `S:697-715` 3 Laeufe -> `missing` (zahm) bzw. `lost`; `S:450-455` 24 h (Besitzer online) -> `lost` ohne Sperre; Rueckkehr
  `S:639-644`. Befund B3 (angefuettert), B6 (Suchlauf).

### 2.8 Sicht zum Client, Hello/Sync
Schreiber: `B.BuildView` (`R:406-438`: nur Zahlen/Texte, hoechstens 16 Junge, eigene zuerst), `B.SendView` (`K:438-446`: Server
`sendServerCommand`, SP `B.ApplySync` direkt), `B.FlushViews` (`S:67-92`, eine Sendung je Spieler und Takt), `pushNewSights` (`S:750-771`).
Client: `C:251-259` nimmt `Sync`/`Note`, `K:353-381` fuellt `B.View` an Ort und Stelle, `H:351-354` zaehlt; `C:191-197` "frisch".
**Befund B1** (MP: Hello mit leerer Tabelle, erster Eintrag ohne Sendung).

### 2.9 Speichern/Laden, Gegend entladen/neu laden
Register nur in `OnInitGlobalModData` geholt (`R:67-107`), kaputte Zeilen raus, Sitzungsobjekte neu. Tiere werden ueber den Spiegel und
`aid` wiedergefunden (`W:286-359`, `R:183-213`), Spiegel wird nie geglaubt ausser der id mit Gegenprobe. Nicht geladen: `B.AreaLoaded`
(`W:104-115`) verhindert Fehlversuche. Sperre (Bewegung) wird nicht gespeichert (FE 1.4) -- nichts haengt. Befund B3 fuer die Luecke
"Kacheln da, Tier noch nicht".

### 2.10 Spieler verlaesst den Server, zweiter Spieler
Verlassen: laufende Aktion endet ohne `complete`, nichts genommen; sein Junges bleibt im Register (B2); seine `_pp`/`_sig` fallen im
naechsten Takt heraus (`S:799-801`, `S:769`). Zweiter Spieler: fremd gebunden -> `Why_Other`; zahm -> `Why_NotOwner`; Koeder je Spieler
einer; `Hud_Other` zeigt den Kontonamen (Plan 6.2.5: oeffentlich). Geteilter Bildschirm (SP): alle `__sp`, `uid` trennt, kein Balken.

---

## 3. Pruefliste aus dem Auftrag

| Nr | Frage | Ergebnis |
|---|---|---|
| 1 | Gegenstand verloren/verdoppelt | nein; nur der Schreiber nimmt, nach allen Pruefungen, Gegenprobe `contains` (`S:166-176`, `S:221`, `S:335`). B4 = falsche Meldung, kein Verlust |
| 2 | Kick | Client entfernt/erzeugt nichts; Befehle `Hello` (leer), `BaitDrop` (id, Besitz geprueft); Koeder-Koordinaten gegen Spieler <= 3 geprueft; Sicht <= 16 Junge, hoechstens eine je Spieler und Takt. Kein Fund |
| 3 | Haenger/Lecks | Schleifen gedeckelt (8 Versuche, 25 Kacheln, 64/16); `_s`, `_pp`, `_sig`, `_errAt` (64) begrenzt; Bewegungssperre loest die Engine (FE 2) und jeder Aktionsausgang; Zustaende mit Ausgang **ausser** B2 (Abwesende) und B5 (reifer Koeder) |
| 4 | SP-Zweig | `K:97-103`, `K:412-446` richtig; Riegel `if isClient() then return end` richtig herum (`S:1`, `W:1`, `R:1`); Server-Pfad ohne UI/`getPlayer` (`getSpecificPlayer` nur im SP-Zweig `W:46-52`); `OnGameBoot` feuert auch am Server (javap GameServer Offset 519) |
| 5 | Zahlen/Plan | stimmen (2.6); Plan-Widerspruch Zeile 119/130 -> B2; reifer Koeder ohne Verfall -> B5 |
| 6 | Stoerung anderer | Menue nur bei `ncbearcub` (`M:198-219`), "Kill" nur in dessen Untermenue; erwachsener `bear` nur ueber Naht 1 (`NOT_TENDED["bear"]`, gewollt); NPC Crew nur hinter Riegeln (`BanditsNPCBearCrew.lua`, `K:114-120`, `K:150-155`); ohne NPC Crew laeuft alles (Gesamt-Attrappe Fall 14) |
| 7 | Leistung | je Bild nur Zeichnen aus fertiger Liste (`H:331-346`); Takte gedrosselt; B6 (zwei lange 5-s-Suchlaeufe) |
| 8 | eigene Attrappen | `attrappe/pruef_b/run.lua`, Ausgabe `ergebnis.txt`: Fall 1 (B1), Fall 2 (B2), Fall 3 (B3, B4) -- alle vier Befunde reproduziert |

Statisch geprueft, nicht gespielt.
