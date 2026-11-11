# Lauf baer-b1d: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung

Stand 11.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`
(B1a + B1b + B1c + B1d nach dem ZUSAMMENBAU, `staging_dateien.txt`). Ganz gelesen: `shared/BanditsNPCBearStats.lua`,
`server/BanditsNPCBearGrow.lua`, die B1d-Stellen in `server/BanditsNPCBearServer.lua` (Fuettern, Langsam-Takt, Hirn-Takt komplett),
`server/BanditsNPCBearRegistry.lua` (InitRegistry, Commit, Close, Sicht), `server/BanditsNPCBearHeal.lua` (Spiegel, Restore,
TakeNewerMark), `server/BanditsNPCBearRide.lua` (PlaceCub, RideBoard, RideStep, Call), `server/BanditsNPCBearWorld.lua` (Players,
FindAnimal, MoveTo), `shared/BanditsNPCBear.lua` (CFG, OPTS, Opt, Tell, Sicht), `shared/BanditsNPCBearDefs.lua`, `client/ISUI/
BanditsNPCBearHud.lua`, `client/BanditsNPCBearOptions.lua`, die B1d-Teile von `client/BanditsNPCBearClient.lua` und
`client/NCBearBenchCub.lua`, `sandbox-options.txt`. Dazu Jar-Auszuege `dec/AnimalData.java` (update, growUp, updateHealth, hourGrow,
initSize, init, setSize/setSizeForced), `dec/IsoAnimal.java` (load, init, updateInternal, setHealth, updateStatsAway, Alterstext),
`dec/DesignationZoneAnimal.java`, Vanilla `client/PZAPI/ModOptions.lua:120-156`, `shared/Definitions/animal/ButcheringUtil.lua`.
Nichts im Staging geaendert. Eigene Attrappen: `attrappe/pruef_b1d/run.lua`, Ausgabe `attrappe/pruef_b1d/ergebnis.txt` (Abschnitt 3).
Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/`, `dec/` = Jar-Auszug (NUR JAR = Lesehilfe, kein Beleg).

## 0. Ergebnis zuerst

B1d traegt: Kurve und Meilensteine exakt (Tag 15 / 45 / 100 bei 100, anteilig bei 10..365), Wachsen nur gezaehmt, nur mit Besitzer
im Spiel, nicht bei "missing", weiter in der Fahrt; Groesse am Schreiber je Hirn-Takt mit 2 Java-Aufrufen geprobt und nur selten
geschrieben (am Anfang etwa alle 2 Spielstunden), ueberlebt Speichern/Laden (Weg B), Mitfahren, Call to me, Register-Heilung; Leben
als Anteil mit Register-Wahrheit, Engine-Heilung wird zurueckgenommen (eigene Attrappe P1a: 10 Spielstunden mit Engine +2 %/h ->
genau +10 %), nie ueber 1, nie 0; alle Werte und Faehigkeiten gedeckelt, nichts waechst ohne Grenze; Anzeige <= 12 Zeichenaufrufe je
Schild, keine Texte je Bild; kein neuer Client->Server-Befehl (kein Kick-Weg), kein Gegenstand beteiligt, keine NPC-Crew-Figur
beruehrt, alte NCBear*-Dateien unberuehrt. **Kein Blocker, kein Major. 8 kleine Befunde (B1-B8)**, davon zwei mit Wirkung im MP
(B1 Spiegel-Deckel aushebelbar, B2 ein B1d-Fehler am Server reisst die B1a-B1c-Takte mit), der Rest Randfaelle.

Alle vorhandenen Attrappen gruen (nachgelaufen 11.11.): `b1d_kern` 147/0, `kern` 136/0, `b1b_kern` 204/0, `b1c_kern` 192/0, `gesamt`
1173/0, `b1d_ober` (mit echtem Kern) 173/0, `ober` 116/0, `b1c_ober` 193/0. Pruefer: `luacheck.py`, `scopecheck.py` 0, `localcount.py`
groesster Wert 59 (Hud Dateiebene), `luacheck_pz.py` 0 Treffer; alle B1d-Lua-Dateien LF, ASCII, kein `next(`.

## 1. Befunde (Schwere: blocker / major / minor)

### B1 (minor) MP: der Deckel fuer `g` aus dem Spiegel ist ueber `mark.tamedAt` aushebelbar
- **Wo:** `S:server/BanditsNPCBearGrow.lua:527-541` (`B.GrowFromMark "restore"`: `cap = feedGrowMax + (now - rec.tamedAt) / (D x 24)`),
  `rec.tamedAt` kommt ungeklemmt aus dem Spiegel `S:server/BanditsNPCBearHeal.lua:234` (`tamedAt = num(mark.tamedAt)`). Der Kommentar
  `Grow.lua:509-510` sagt "ein veraenderter Spiegel macht keinen fertigen Baeren".
- **Beleg (eigene Attrappe P2b):** Server, Register verloren, Spiegel mit `g = 1`, `tamedAt = -1000000`, `xFgt = 99999` -> Eintrag
  `g 1.0000, tamedAt -1000000, Stufe adult, Kaempfen L10`. Gegenprobe mit ehrlichem `tamedAt` (2 Tage): gedeckelt 0,12 (wie b1d_kern 12).
  Dass ein Client Tier-ModData am Server schreiben kann, steht schon im Code (`Heal.lua:290-291`, Jar `dec/ObjectModDataPacket.java`).
- **Folge:** nur MP, nur mit veraendertem Client, nur ueber den Heil-Weg (Restore). Kein Kick, kein Gegenstand. Wie B1c F1 (Besitz und
  "tame" kommen dort ebenfalls aus dem Spiegel) -- B1d macht es nicht schlimmer, aber der Kommentar verspricht mehr, als der Code haelt.
- **Vorschlag:** `tamedAt` (und `born`) in `B.Restore` auf `[0, now]` klemmen (Weltstunden sind nie negativ; dann hoechstens
  "gezaehmt bei Weltbeginn"), den Kommentar `Grow.lua:509-511` ehrlich machen (Deckel nur gegen ein zu hohes `g` bei ehrlichem
  `tamedAt`), F18 im Plan um `tamedAt` ergaenzen; ob im MP ueberhaupt `g`/Erfahrung aus dem Spiegel kommen sollen, ist Kevins Frage (4.1).

### B2 (minor) Ein Fehler im B1d-Schritt am MP-Server bricht die B1a-B1c-Takte mit ab
- **Wo:** `S:server/BanditsNPCBearServer.lua:582` (`B.GrowSlow` in der Schleife von `slowTickBody`, VOR `forestRolls`, `baitNights`,
  `B.FlushViews` und vor den uebrigen Eintraegen) und `:747` (`B.GrowLive` mitten in `liveRec`, vor Wache/Folgen; danach im Hirn-Takt
  noch alle weiteren Jungen, `baitAppear`, `pushNewSights`, `FlushViews`, Waisen-Suchlauf). Beide Takte haben nur EIN pcall um den ganzen
  Koerper (`:599`, `:1019`).
- **Warum:** `animal:getHealth()` am Tier ist am MP-Server ehrlich offen (`Grow.lua:202-205`, PLAN_B1D.md 8 Nr. 4; Vanilla `server/`
  und `shared/` haben keinen Aufruf am Tier -- grep 11.11.). Scheitert er, wirft `B.BodyHp` je Langsam-Takt (aus `GrowSlow`) UND je
  Hirn-Takt (aus `GrowLive`, solange `rec.hp` nil bleibt -- es bleibt nil, weil der Fehler vor dem Setzen kommt, `Grow.lua:413`). Dann
  laufen im MP Folgen/Verstecken des ersten zahmen Jungen, alle spaeteren Jungen, Koeder, Sichten und die B1a-Uhren nicht mehr. Die
  Fehlerzeile kommt (B.ErrEvery), der Rest der Mod steht trotzdem. Wahrscheinlichkeit klein (geerbte Methode, wie A3 aus B1a), Wirkung gross.
- **Vorschlag (ohne neues pcall):** die B1d-Schritte ans ENDE der Takte legen -- im Langsam-Takt eine eigene Schleife `B.GrowSlow` NACH
  `B.FlushViews(players)` (die Sicht der Commits geht dann im naechsten Hirn-Takt hinaus), im Hirn-Takt eine eigene Schleife
  `B.GrowLive` ueber `loaded` nach `B.FlushViews(players, sent)`. Dann reisst ein B1d-Fehler nur B1d mit. Testpunkt bleibt PLAN_B1D.md 7.4
  MP 7 ("[TC-BEAR] ***" im Server-Log).

### B3 (minor) Leben-Abgleich: kleiner Schaden unter `hpEps` wird beim Heilen ueberschrieben; Engine-Heilung frisst Schaden im selben Fenster
- **Wo:** `S:server/BanditsNPCBearGrow.lua:219-240` -- Schaden zaehlt nur bei `h < hpB - eps` (:219), gesetzt wird aber, sobald
  `|h - hp| > eps` (:232). `schnittstelle_aenderungen.md:326-328` verspricht "Kleine Abweichungen ... sammeln sich ... (kein
  schleichender Verlust unter der Schwelle)".
- **Beleg (P1b):** Leben 0,60 (Register = Koerper), Treffer -0,004 am Koerper, ein Langsam-Takt mit Heilung +0,0017 -> Register und Koerper
  **0,6017** statt ~0,5977: der Treffer ist weg (Gratis-Heilung). **(P1c):** Treffer -0,03 und Engine-Stunde +0,02 im selben 10-Minuten-
  Fenster -> nur -0,01 gezaehlt (Register 0,5900 statt ~0,5717).
- **Folge in B1d:** gering -- B1d hat keine eigene Schadensquelle; Engine-Schaden kommt nur von Spieler-Waffe, anderem Tier, Anhaenger
  (forschung_b1d.md 3.1). Wird mit B5a wichtig, wenn Treffer haeufig und klein werden.
- **Vorschlag:** Verluste ohne Schwelle werten (z. B. `h < hpB - 0.0001` -> Schaden), `hpEps` nur fuer Anstiege (Engine-Heilung)
  behalten; den Satz in `schnittstelle_aenderungen.md` berichtigen. Das Fenster-Problem (P1c) loest erst F5 (Engine-Heilung in der
  Definition aus) oder der eigene Schadensweg von B5a -- dort mitnehmen.

### B4 (minor) Kondition/Ausdauer: fester Weg-Deckel je Takt -- bei Ruckeln oder Vorspulen zaehlt Rennen gar nicht
- **Wo:** `S:server/BanditsNPCBearGrow.lua:340-343`: `dts` wird auf 10 s gedeckelt, der Weg aber fest gegen `conStepMax` 8 Kacheln je
  Takt geprueft (gedacht als "Neu-Erzeugen"-Erkennung), egal wie lang der Takt war; Erholung `:361` rechnet in Echtzeit.
- **Beleg (P3a/P3b):** Takt 1,5 s / 3,7 Kacheln (2,47 Kacheln/s, `B.CFG.runSpeed`): XP und Ausdauer wie geplant. Takt 3,5 s (Ruckler,
  8,6 Kacheln) oder Vorspulen x3 (11,1 Kacheln je 1,5-s-Takt): **0 XP, Ausdauer bleibt voll**. Ebenso erholt sich die Ausdauer in einer
  Pause (Echtzeit laeuft, das Tier steht) -- harmlos, nur Anzeige.
- **Vorschlag:** die Teleport-Erkennung an die Zeit binden, z. B. `way > conStepMax and way > runSpeed x dts x 2` -> 0 (oder ueber die
  Spielzeit `B.Now()` messen, dann stimmt auch Vorspulen). Kein Engine-Aufruf noetig. F14 (Tempo der Kondition) bleibt Kevins Blick.

### B5 (minor) Riegel in `B.InitRegistry` prueft nur `B.GrowFix` -- fehlt `shared/BanditsNPCBearStats.lua`, bleibt das Register leer
- **Wo:** `S:server/BanditsNPCBearRegistry.lua:167-170` (`if B.GrowFix then ... B.GrowFix(rec, now, true)`); `B.GrowFix` ruft
  `B.GrowDays`, `B.XpCum`, `B.SKILLS` aus Stats.lua (`Grow.lua:110`, `:150-151`). PLAN_B1D.md 4.3: "Kern ruft alles ueber if B.X then".
- **Beleg (P2d):** Grow.lua geladen, Stats.lua nicht -> `B.InitRegistry` wirft "attempt to call field 'GrowDays' (a nil value)" an
  `Grow.lua:110`; im Spiel vor `reg = r` (`Registry.lua:181`) -> `B.Reg()` bleibt nil, alle Takte kehren um (der ganze Baer ist aus).
- **Folge:** nur bei einer Teilkopie (z. B. Uebernahme mit Fehler); beide Dateien liegen in `LUA_BEAR`. Klein, aber der Riegel ist schief.
- **Vorschlag:** in `B.GrowFix` (und `B.GrowSlow`/`B.GrowLive`/`B.GrowView`) frueh zurueck, wenn `B.GrowDays`, `B.XpCum` oder `B.SKILLS`
  fehlen -- oder der Riegel in `Registry.lua:167` fragt alle drei.

### B6 (minor) MP-Client-Probe der Groesse haengt am Zeichnen der Anzeige
- **Wo:** `S:client/ISUI/BanditsNPCBearHud.lua:441`, `:456-457` (Probe im Listenbau), aufgerufen nur aus `Hud:prerender` (`:657`), das bei
  geteiltem Bildschirm schon `:655` umkehrt; die Sicht traegt nur Junge in `tellDist` 60 Kacheln (`S:shared/BanditsNPCBear.lua:48`,
  `Registry.lua:605-606`).
- **Folge:** nur MP, nur Bild/Kollision der CLIENT-Kopie (der Server rechnet richtig): geteilter Bildschirm -> die Kopie behaelt die Groesse
  der Erst-Uebertragung, bis der Client das Tier neu bekommt; ein Junges zwischen 60 Kacheln und der Ladeweite (~76) ebenso. Ob ein mit
  der UI-Taste ausgeblendetes Panel `prerender` bekommt: ungeprueft (dann ebenso).
- **Vorschlag:** die Probe (<= 1 x/s, 2 Java-Aufrufe je Junges) in einen eigenen kleinen Client-Takt legen (z. B. aus dem vorhandenen
  `B.OnView`/OnTick in `client/BanditsNPCBearClient.lua`), unabhaengig vom Panel; als bekannte Grenze in PLAN 12 nennen.

### B7 (minor, fuer B5a) `setSizeForced` verbiegt `originalSize` -- Leiche und Zerlegen nach dem Tod mit falscher Groesse (NUR JAR)
- **Wo:** `S:shared/BanditsNPCBearStats.lua:340-347` (`B.ApplySize`, ein `setSizeForced` je Abweichung). NUR JAR `dec/AnimalData.java:
  1544-1546` (`setSizeForced` merkt `originalSize = size` VOR dem Setzen), `:64` (Vorgabe 1,0), Laden setzt nur `setSize`
  (`dec/IsoAnimal.java:1413`, `originalSize` bleibt 1,0). Vanilla liest beim Tod `getAnimalOriginalSize()` fuer die Leiche
  (`V:shared/Definitions/animal/ButcheringUtil.lua:42-43`) und fuer das Zerlegen (`V:shared/TimedActions/Animals/ISButcherAnimal.lua:81`
  `animalSize < 0.4`).
- **Folge:** ein neuer Koerper (Aussteigen, Call to me: 0,35 -> 0,75 in einem Schritt) behaelt `originalSize` 0,35, solange die gezeigte
  Groesse bei 0,75 stehen bleibt; nach dem Laden ist sie 1,0. Stirbt das Junge, ist die Leiche zu klein/zu gross (ungespielt). Kein
  Gegenstand geht verloren; Tod/Kampf ist B5a.
- **Vorschlag:** in B5a beachten; billig waere in `B.ApplySize` beim Schreiben ein zweites `d:setSizeForced(sz)` (dann `originalSize = sz`),
  gleicher belegter Aufruf, gleicher Typ.

### B8 (minor) Sandbox-Wechsel von "Tage bis ausgewachsen": Groesse bleibt, die Anzeige "Tag" springt
- **Wo:** `S:shared/BanditsNPCBearStats.lua:233-235` (`B.GrowDay = floor(g x D)`), Sicht `day`/`nxt` aus `B.StatsOf`.
- **Beleg (P2c):** `g` 0,3 -> bei D 100 "Day 30", nach dem Umstellen auf D 50 "Day 15" (Groesse und Werte unveraendert, wie geplant 0.1).
- **Folge:** nur Anzeige, gewollte Folge von "g als Anteil" (kein Schrumpfen). Kann verwirren ("mein Baer ist juenger geworden").
- **Vorschlag:** so lassen und im Sandbox-Tooltip erwaehnen ("changing it later keeps the size; the shown growth day is recounted"), oder
  Kevins Wort zu F12 (Wachstumstag vs. Kalendertage) abwarten.

## 2. Verfolgt und in Ordnung (mit Fundstelle)

| Punkt | Ergebnis | Fundstelle |
|---|---|---|
| Kurve, Meilensteine, andere Sandbox-Tage | stueckweise gerade, exakt 0,35/0,75/1,0/1,35 bei g 0/0,15/0,45/1; D 10..365 anteilig; D-Wechsel aendert nur das Tempo | `Stats.lua:155-170`; b1d_kern 1-2, gesamt 19k/19l |
| Rundung | Stufen mit 1e-6 Spiel (Gleitkomma-Summe aus 2160 Takten), Tag mit floor+1e-6, `nextDays` >= 1; gezeigte Groesse 3 Stellen, geschrieben ab 0,002 | `Stats.lua:197-215`, `:229`, `:288-290`, `:344` |
| Zeitspruenge Schlafen/Vorspulen | `dt` = echte Weltzeit seit dem letzten Takt, je Schritt <= 1 h (`Server.lua:567-571`) -> nie doppelt; nur ein Sprung > 1 h in EINEM Takt (Debug-Zeit) kostet Wachstum (P2a, im Plan 12 bekannt) | eigene Attrappe P2a |
| Frisch gezaehmt | erster Takt rechnet `g` aus `tamedAt` und gibt `dt` nicht doppelt | `Grow.lua:427-438` |
| Nur gezaehmt, Besitzer im Spiel, nicht vermisst | `GrowSlow` nur `st == "tame"` und `online[owner]`; `GrowLive` nur tame; wilde/scheue/angefuetterte: alle B1d-Felder nil (`GrowFix`), Engine-Wachsen ~0 (`ageToGrow` 36500; `dec/AnimalData.java:218-235`) | `Grow.lua:105-108`, `:396-397`, `:422-424` |
| Groesse: Seite und Haeufigkeit | Schreiber je Hirn-Takt 2 Java-Aufrufe, Schreiben ab 0,002 (am Anfang ~alle 2 Spielstunden), neuer Koerper sofort (`PlaceCub` -> `GrowBody`); MP-Client im Listenbau <= 1 x/s; SP nie doppelt | `Grow.lua:411-412`, `:456-463`, `Ride.lua:86`, `Hud.lua:441-457` |
| Groesse ueberlebt Laden / Tierzone / Debug-Alter | Laden: `setSize` mit Klemme [0,35; 1,35] (`dec/IsoAnimal.java:1413`) -> bleibt; Tierzone/`init` -> minSize, naechster Hirn-Takt setzt nach | `Defs.lua:83-84`, gesamt 19i |
| Wirkung auf Kollision/Tempo/Folgen | Kollision waechst mit (NUR JAR `dec/IsoAnimal.java:420/433`), Tempo nicht (Fussgleiten = F2, Kevins Blick); Folgen-Abstaende 3/4,5 bei 1,5 m Koerper ok; Haltung beim Streicheln fest 0,5 (Plan 1.2.4) | forschung_b1d.md 1.2 |
| Alterstext / Stufen der Engine | kein `nextStage` -> `isBaby()` falsch, `checkStages` tut nichts, Alterstext unabhaengig von `ageToGrow`; kein Greis-Verlust (`maxAgeGeriatric` 0) | `dec/IsoAnimal.java:1966-2017`, `dec/AnimalData.java:118-134`, `:467` |
| Leben: Engine-Heilung, Mitfahren, Call, Spiegel-Heilung | Engine +2 %/h wird zurueckgenommen (P1a: 0,50 -> 0,60 in 10 h); Hand-Wert in der Fahrt (hp < hpB) kommt am neuen Koerper an (P1d); Restore holt das Leben vom Koerper | `Grow.lua:191-246`; eigene P1a/P1d, b1d_kern 9/13, gesamt 19f-19h |
| Nie 0, nie > 1, totes Tier | Untergrenze min(0,01; Koerper), Obergrenze 1; `isDead` -> nichts | `Grow.lua:201`, `:227-229` |
| Werte taeglich, Formeln | Leben/Ausdauer/Traglast/Schaden stetig aus s; +50 % Leben/Ausdauer, 5..40 % Ausweichen (Sandbox 5..80), +70 % Kaempfen, Fischen erst ab halbstark | `Stats.lua:276-320` |
| Faehigkeiten, Kurve, Deckel | eine Zahl je Faehigkeit, Stufe gerechnet; XP <= 2133; Eimer 18 + 6/min je Faehigkeit (P3c: 30 min Dauerrennen -> 197,6 XP); Sitzung <= 6 Eimer; Sicht-Touch nur bei Aenderung (P3c: 5 in 30 min) | `Grow.lua:254-290`, `:333-389`; eigene P3c |
| Fuetter-Bonus | nur zahm, nur Besitzer (CheckFeed), 3/2/1 h, <= 2 je Tag, Summe <= 0,10, nie ueber 1; Stufen-Meldung, wenn er die Schwelle reisst | `Grow.lua:470-505`, `Server.lua:243` |
| Spiegel | 10 Felder, Fassung 2; SP "newer" = max; Restore klemmt; `hp` nicht im Spiegel (Koerper traegt es) | `Heal.lua:40-44`, `Grow.lua:522-566` |
| Tod | `B.Close` loescht Eintrag + Sitzung (`Registry.lua:476-477`), neues Junges beginnt bei 0 | b1d_kern 16 |
| Anzeige, Kosten je Bild | Texte und Fuellbreiten im Listenbau (<= 1 x/s, `LIST_MS` 1000), je Schild <= 12 Zeichenaufrufe, `hudMax` 6 -> <= 72; kein `U.T` je Bild; Anker x sz/0,35 gedeckelt (`ZK_MAX` 5) | `Hud.lua:313-352`, `:563-588`, `:615-635` |
| Optionen | `addComboBox`/`addItem` mit Schluesseln, `getValue` = Index (V:`client/PZAPI/ModOptions.lua:120-137`), Unsinn -> Vorgabe | `Options.lua:63-75`, `Hud.lua:164-174` |
| SP- und MP-Zweig | Grow.lua `if isClient() then return end`; Meldungen ueber `B.Tell` (Server `sendServerCommand`, SP direkt); Sicht fertig gerechnet vom Server; der Client rechnet nie mit eigenen Sandbox-Werten; Bench lehnt MP ab | `Grow.lua:1`, `shared/BanditsNPCBear.lua:511-531` |
| Rote Linien | kein neuer Client->Server-Befehl (kein Kick-Weg), kein Gegenstand beteiligt (Fuettern unveraendert ein Stueck), keine Schleife ohne Deckel, `ApplySize` nur an `ncbearcub` (Art-Probe in `FindAnimal`/Hud-Suchlauf), NPC Crew und alte NCBear*-Dateien unberuehrt | `World.lua:508-517`, `Hud.lua:241-250`, `staging_dateien.txt` |

## 3. Eigene Attrappen (`attrappe/pruef_b1d/run.lua`)

Drei Faelle fuer die riskantesten Stellen; "BEFUND" = Beleg fuer einen Punkt in 1, kein roter Test. Ergebnis: **10 bestanden, 0 Fehler,
8 Befunde** (Ausgabe `attrappe/pruef_b1d/ergebnis.txt`).
- **P1 Leben ueber Stunden** (`B.BodyHp` mit Engine-Heilung je Spielstunde, kleiner Schaden, Fahrt): P1a ok (0,6000 nach 10 h, Koerper
  folgt), P1b/P1c Befund B3, P1d ok (Hand-Wert in der Fahrt kommt am neuen Koerper an).
- **P2 Zeitspruenge, Sandbox, MP-Spiegel, Teilkopie:** P2a bekannt (Plan 12), P2b Befund B1 (+ Gegenprobe ok), P2c Befund B8, P2d Befund B5.
- **P3 Kondition/Ausdauer** (`B.GrowLive` direkt mit gesetztem Rennbefehl): P3a ok, P3b/P3b' Befund B4, P3c ok (Eimer-Deckel 197,6 <= 198,
  Ausdauer 0..1, 1 Eimer-Schluessel, 5 Sicht-Touches in 30 min, Stufe aus XP).
Aufruf: `C:/Users/Kevin/Tools/lua51/lua5.1.exe C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/pruef_b1d/run.lua`

## 4. Fragen fuer Kevin (Kevin schlaeft; nichts davon haelt den Einbau auf)

1. **(B1, Erweiterung F18)** Mehrspieler nach einem Verlust des Server-Registers: soll ein Junges sein Wachstum und seine Erfahrung aus
   der Markierung am Tier zurueckbekommen (bequem, aber mit veraendertem Client faelschbar) oder hart gedeckelt neu anfangen?
   Empfehlung: zurueckbekommen wie heute, `tamedAt` nur auf [0, jetzt] klemmen.
2. **(B8, zu F12)** Stellst du "Tage bis ausgewachsen" spaeter um, bleibt die Groesse, aber die Zahl "Tag" in der Anzeige wird neu
   gezaehlt (z. B. 30 -> 15). Ok so? Empfehlung: ja, mit Hinweis im Tooltip.
3. **(B4, zu F14)** Beim Vorspulen (x3) oder starkem Ruckeln zaehlt Rennen heute nicht fuer die Kondition. Empfehlung: an die Zeit binden
   (Vorschlag B4), damit es auch dann zaehlt.

## 5. Nicht geprueft / offen (ehrlich)

`animal:getHealth()` am MP-Server (B2, PLAN 8 Nr. 4); ob `setSizeForced` direkt nach `addToWorld` wirkt (der naechste Hirn-Takt setzt
sicher nach); ob ein ausgeblendetes Panel `prerender` bekommt (B6); Engine-Schaden-Groessen echter Treffer am Tier (B3); `originalSize`
beim echten Tod (B7, NUR JAR); Fussgleiten und Schild-Hoehe bei 0,75 (F2, Kevins Blick). Alles statisch geprueft, nicht gespielt.
