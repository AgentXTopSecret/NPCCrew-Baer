# Lauf baer-b1e: PLAN -- Modellwechsel ab Halbstark (grosser Koerper bis 1,35) und groessere Markierung (B1e)

Stand 11.11.2026 ~16:30. **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2. Verbindlich fuer zwei Bauer (KERN,
OBERFLAECHE, gleichzeitig, getrennte Dateien) und den ZUSAMMENBAU danach. Baut auf dem Staging `_arbeit/baer_zaehmen/mod/` (B1a-B1d inkl.
Nachbesserung, Liste `staging_dateien.txt`).
Kurzformen: `FE x.y` = `forschung_b1e.md`; `FD` = `forschung_b1d.md`; `PB1D x.y` = `PLAN_B1D.md`; `PB1C x.y` = `PLAN_B1C.md`;
`S:` = Staging `mod/42/media/lua/`; `V:` = Vanilla `media/lua/` (42.22.2); `VA:` = Vanilla `media/AnimSets/`; `B:` = Bandits `42.22/media/lua/`;
`Bc:` = Bandits `common/media/`; `NC:` = NPC Crew `42/media/lua/` (nur gelernt); `T:` = Test-Mod `NCBearTest/42/media/lua/`; `ENT` =
`baer/begleiter/ENTSCHEIDUNGEN.md`; `M:` = `_arbeit/baer_zaehmen/mess_b1e/ausgabe.txt`; `B` = `BanditsNPC.Bear`, `U` = `B.UI`.
**NUR JAR** = Lesehilfe, kein Beleg.

Kevins Worte, auf denen der Plan steht (ENT unten): *"Ab Tag 15 (halbstark)"* auf Claudes Vorschlag *"Ab Tag 15 wird das Junge zum grossen
Baeren in klein, mit 0,75, und waechst bis Tag 100 auf die volle Groesse 1,35"* -- Groessen-Tabelle ENT:5-10 (Jungtier 0,35 / Halbstark 0,75 /
Erwachsen 1,35, "rund 2,65 m lang, 1,55 m Schulter") -- *"der neue baby baer laeuft auch wie eine giraffe ... das alte ist definitiv besser"*
(altes Junges 6c3f0a96 / 2ee25f24) -- Markierung: *"waer cooler wenn das symbol was groesser waere zumindestens bei 4k aufloesung"* (3840 x 2054),
*"brauch ich dafuer eine zusatz mod? ... hab nur die baeren mod aktiv grade"*. Alles andere ist VORSCHLAG des Planers (Stellwert oder Frage in 11).

**Vorab nachgezaehlt (11.11. ~16:20):** Staging gegen Test-Mod 51 Dateien, **49 byte-gleich, 2 verschieden**: die Test-Mod hat schon wieder das
ALTE Junge (`models_X/Skinned/NCBearCub.glb` 6c3f0a96, `textures/Body/NCBearCub.png` 2ee25f24), das Staging noch das Generator-Junge
(ee7a0cce / 92a829fa). Der ZUSAMMENBAU legt die alten Dateien aus `_arbeit/baer_baby/entwurf/` ins Staging (10.1). Gemessen und geplant wird nur mit
dem alten Jungen.

**Nicht zurueckbauen:** alles aus B1a-B1d inkl. Nachbesserungen. **Nicht anfassen:** alle `T:`-Dateien des Erwachsenen (`NCBearFight.lua`,
`NCBearDefs.lua`, `NCBearSize.lua`, `NCBearSpawn.lua`, `NCBearAttackProbe.lua`, `NCBearTest.lua`, `NCBearBench*.lua` ausser unserer
`NCBearBenchCub.lua`), Modell-/Textur-/Skript-Dateien (`NCBear.glb`, `NCBear.png`, `nc_bear_tier.txt`, `nc_bear_cub.txt`), AnimSets.

---

## 0. Entscheidungen des Planers (gelten fuer alle)

**0.1 Zwei Koerper, ein Eintrag.** Der Register-Eintrag (Kennung `id`, Kennzeichen `u`, alles aus B1a-B1d) bleibt immer derselbe. Er hat zu
jeder Zeit hoechstens EINEN Koerper: `"cub"` = Art `ncbearcub` (altes Junges-Modell) oder `"big"` = NEUE Art **`ncbeargrown`** (grosses
Modell des 2c-Baeren). Neues Register-Feld `rec.body` = der Koerper, den der Eintrag zuletzt HATTE (gesetzt beim Erzeugen und Binden; Wahrheit
ist immer `animal:getAnimalType()` des gebundenen Tiers). Wilde/scheue/angefuetterte Junge: `body` fehlt (= cub), sie wachsen und tauschen nie.

**0.2 Tausch NUR ueber den vorhandenen Weg** `B.PlaceCub` (neuer Koerper, `gen + 1`, Spiegel sofort, Groesse+Leben sofort) und danach
`B.RemoveCub(alt)` -- genau wie "Call to me" (`S:server/BanditsNPCBearRide.lua:328-335`). Kein neuer Erzeuger (Uebernahme-Regel
`baer_uebernahme.py` TIER_RULES: `B.CreateCub(` nur aus `B.AppearFor`/`B.PlaceCub`, `addAnimal`/`addToWorld` nur in `B.CreateCub`). Nie die
alte Art `bear` (NCBearFight greift sofort an = B5a); keine `NCBear*`-Datei wird geaendert.

**0.3 `B.PlaceCub` erzeugt immer den Koerper, den der Eintrag haben WILL** (`B.BodyOf(rec)`). Damit tauschen Aussteigen, Call to me und
Tod-im-Auto von selbst richtig, ohne eigenen Tausch-Takt (ein waehrend der Fahrt ueber 0,75 gewachsenes Junges steigt gross aus). Nur
der Tausch selbst gibt den Koerper ausdruecklich vor. Rueckfall "nie verloren": kann der grosse Koerper nicht entstehen (Definition fehlt),
entsteht beim Aussteigen/Call ein Junges-Koerper + gedrosselte Fehlerzeile.

**0.4 Schwelle mit Abstand (nie flackern)** auf der INNEREN Groesse s (`B.GrowSize(g)`, PB1D 0.2): hin zum grossen Koerper bei
`s >= cubMaxSize` (0,75 = Halbstark; D = 100 -> Tag 15, sonst Tag 0,15 x D); zurueck zum Jungen erst bei `s < swapBackSize` (0,70);
dazwischen bleibt der Koerper, den der Eintrag hat. Dazu je Eintrag hoechstens ein Tausch je `swapMinMs` (60 s Echtzeit, Sitzung).
`g` waechst nur; zurueck geht es nur ueber die Bench (`NCBear_CubGrow(-100)`) oder den Not-Aus `B.CFG.bodySwap = false`.

**0.5 Gezeigte Groesse je Koerper (gemessen, 2.4):** Junges `sz = min(s, 0,75)`; grosser Koerper
`sz = 0,72 + (s - 0,75) x (1,35 - 0,72) / (1,35 - 0,75) = 0,72 + 1,05 x (s - 0,75)`, geklemmt [0,72, 1,35]. Beim Tausch wirkt der grosse
Baer bei 0,72 so gross wie das Junge bei 0,75 (Laenge +0,6 %, Oberkante +1,9 %, `M:60`); an Tag 100 ist er bei 1,35 genau so gross wie der
erwachsene 2c-Baer bei 1,35 (gleiches Netz). Gesetzt wird weiter NUR ueber `B.ApplySize` (`setSizeForced`, B1d) und NUR am passenden
Koerper. Werte (Leben, Traglast ...) rechnen weiter mit s (PB1D 0.6) -- unveraendert.

**0.6 Wann ist ein Tausch sicher** (sonst naechster Hirn-Takt; nichts haengt, der alte Koerper bleibt solange voll benutzbar): gezaehmt,
nicht mitfahrend, Objekt der Sitzung lebt (Schleife in `brainTickBody` Schritt 7), keine Laerm-Antwort (`s.calmUntil` vorbei), keine
Zombie-Wache (`s.g.on` nicht wahr UND kein Zombie naeher als `zedSafe` in `B._zed[id]`), kein Fuettern/Streicheln (`s.busyUntil` vorbei, 0.7),
Abklingzeit (`swapMinMs` seit dem letzten Tausch, `swapRetryMs` seit dem letzten Fehlversuch), Definition des Ziel-Koerpers geladen. "Call
to me" laeuft in EINEM Aufruf (`B.HandleCall`) und erzeugt selbst den richtigen Koerper (0.3) -- er kann nie dazwischenkommen.

**0.7 Beschaeftigt-Marke statt Raten:** Fuettern und Streicheln melden beim Schreiber `B.BodyBusy(animal, true)` (SP in `start()`, MP-Server in
`serverStart()`), loeschen in `complete()`/`stop()`/`serverStop()`; Deckel `busyMs` (20 s). Grund: ein Tausch mitten in der Aktion verliert
nichts (`handCheck` vor `takeOne`, FE 3.5), meldete aber "The cub is gone." -- unschoen.

**0.8 Ein Helfer fuer "ist unser Baer"**: `B.BodyKind(animal)` -> `"cub"` / `"big"` / nil (shared, einzige Art-Frage; Abschnitt 3). Kein
Code vergleicht mehr selbst `getAnimalType()` mit `B.CUB`. Nie `"bear"`, `"bearstag"`, `"ncbearcubalt"`.

**0.9 Werte je Koerper ueber EINE Funktion** `B.BodyNum(body, key, def)`: beim grossen Koerper `B.CFG[key .. "Big"]`, sonst/fehlt
`B.CFG[key]` (Tempo `walkSpeed`/`runSpeed`). Abstaende mit der Koerperlaenge ueber `B.BodyGap(body, sz)` (2.5). Die reinen Regeln
(`S:shared/BanditsNPCBearRules.lua`) bekommen beides ueber `c.walkSpeed` / `c.gap` (sie lesen B.CFG weiter selbst; fehlt das Feld: wie B1c).

**0.10 Keine neue Meldung zum Tausch.** Er faellt mit der vorhandenen B1d-Meldung "Your bear is half-grown now." zusammen (`Note_Grown`,
Stufe `half` = dieselbe Schwelle s >= 0,75; Bench/Fuettern koennen sie ein paar Sekunden vorziehen). Nur eine Diagnose-Zeile (`B.Log`).
Texte, die heute "cub" sagen, bekommen fuer den grossen Koerper eine **Big-Fassung** (15 Schluessel, 6.8); der Kern haengt `bd = "big"` an
die betroffenen Meldungen, der Client waehlt den Text.

**0.11 Markierung: eigenes UI-Element nur mit Vanilla-UI-Aufrufen, eigene Bilder** (FE 6.2 Weg A). Bandits wird NICHT mehr aufgerufen
(nur noch gelesen: Ueberdeckung und gemerkte Stelle, je hinter Riegel). Groesse in Stufen 100/125/150/200/250/300 % (Pfeil zeichnet
`DrawTextureAngle` immer in Bildgroesse -> ein Pfeil-Bild je Stufe), Auto = naechste Stufe zu Bildschirmhoehe / 1080. Folge: die
Markierung erscheint jetzt **auch ohne Bandits** (Kevins Frage "brauch ich dafuer eine zusatz mod?" -- F11).

**0.12 Aufteilung:** KERN = `shared/` (ohne Translate, MIT `TimedActions/`) + `server/` + Kern-Attrappen; OBERFLAECHE = `client/` (mit `ISUI/`
und Bench), alle Texte (`UI.json`, `IG_UI.json`), Bilder `42/media/ui/`, Werkzeuge, Oberflaechen-Attrappen. Keine Datei fuer beide (6.1).
Neue Lua-Dateien: keine. Neue Bilder: 9 (OBERFLAECHE). Sandbox: nichts Neues.

**0.13 Modell des grossen Koerpers = das heutige Modell-Skript `NCBear_Body`** (`T:media/scripts/nc_bear_tier.txt`, Mesh
`Skinned/NCBear.glb`, gespielt seit 2c). Kein neues Modell-Skript (ein zweites `animationsMesh` auf dieselbe GLB hat in Vanilla kein Vorbild:
jede `meshFile` steht dort genau einmal, gezaehlt in `media/scripts`). Der Tausch nimmt damit von selbst das jeweils aktuelle grosse Modell.
Uebernahme-Naht bis B5a (F9, 10.3).

**0.14 Nicht in B1e:** Kampf/Zombie-Angriffe/Stimmen des grossen Baeren (B5a), neue Modelle/Clips/Knoten, Farbe/Kopf des grossen Baeren,
Fussgleiten beheben (kein Lua-Hebel, FE 4.4), Schlafen, Fischen, Spuernase, Inventar, Baeren-Fenster, Ziehen der Markierung (F7), neue
Sandbox-Optionen.

---

## 1. Verhalten je Auftragspunkt, Schritt fuer Schritt

### 1.1 (Auftrag 1) Tausch Junges -> grosser Koerper
1. **Ausloeser:** je Hirn-Takt (1,5 s, bei Zombie 0,75 s) ruft `brainTickBody` Schritt 7 fuer jedes geladene, lebende, gezaehmte, nicht
   mitfahrende Junge mit `s.obj == a` `B.GrowLive(rec, a, x, y, ms)` (`S:server/BanditsNPCBearServer.lua:1017-1025`, unveraendert). Dort:
   `have = B.BodyKind(a)` (ist `rec.body` anders: `rec.body = have`, Wahrheit = Tier), `want = B.BodyWant(rec)` (0.4).
2. `want == have` -> wie B1d: `B.ApplySize(a, B.BodySize(rec, have))`, Leben/Ausdauer. Fertig.
3. `want ~= have` und `B.BodySwapReady(rec, s, ms)` (0.6) wahr -> `B.BodySwap(rec, a, want, ms)`; sonst B1d-Weg am alten Koerper (das Junge
   bleibt bei 0,75 stehen) und naechster Takt.
4. **Ablauf `B.BodySwap`** (alles in einem Lua-Aufruf, kein Speichern dazwischen):
   a. Kachel: `sq = B.SwapSpot(a, rec.gen)` = eigene Kachel des Tiers (`a:getSquare()`), wenn sie die Platzregeln von `B.SpotNear` erfuellt,
      sonst Ring 1..`swapRing` (2) wie `B.SpotNear` (gleicher Raum, erreichbar). Keine Kachel -> Fehlversuch (5.).
   b. `B.BodyHp(rec, a, 0)` -- noch nicht verbuchter Schaden am alten Koerper geht ins Register (sonst verloren).
   c. `n, why = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "grow" | "shrink", want)`: `B.CreateCub(..., want)` -> neue Art;
      `rec.gen + 1`; `rec.aid` = neue AnimalID; `rec.body = want`; Sitzung des Koerpers leer (Folgen, Laerm-Uhr, Zombie-Wache, Gegenprobe);
      Lage = neue Kachel; `B.Commit` (r + 1, Sicht); `B.WriteMark` sofort (Spiegel mit `body`); `B.GrowBody` -> Groesse `B.BodySize(rec, want)`
      (0,72) und Leben = `rec.hp` sofort; Laerm-/Zombie-Wache leeren.
   d. Gelungen: `B.RemoveCub(a)` (alter Koerper: Sperre los, `remove()`, am Server `removeAnimal(OnlineID)`); `s.swapAt = ms`, `s.swapFailN = 0`;
      neuer Koerper schaut zum Besitzer (`n:faceThisObject(p)`, nur wenn der Besitzer anwesend und naeher als `swapFaceDist` 30, F5;
      seit der Nachbesserung B1e A2 nur im Einzelspieler -- am MP-Server ruft weder Vanilla noch Bandits faceThisObject);
      `B.Log("body: b1 cub -> big (grow) at x,y gen 4, inner 0.750 shown 0.720")`.
   e. Misslungen: alter Koerper bleibt unberuehrt, `s.swapTryAt = ms`, `s.swapFailN + 1`; ab `swapFailLog` (6) eine Fehlerzeile je Minute
      (`B.ErrEvery("swap:" .. id, 60000, ...)`).
   **Kennungen:** `rec.id` (z. B. "b1"), `u`, Besitzer, Name, Zaehmung, `g`, Erfahrung, `hp`-Anteil, Modus (follow/stay), Heimat bleiben;
   NEU sind AnimalID (`rec.aid`), OnlineID (Sicht schickt sie, `pushNewSights`), `gen` (+1), `r` (+1), `body`.
5. **Meldung:** keine eigene (0.10). Sicht geht mit dem naechsten Takt hinaus (Commit -> `B.Touch`), Schild/Karte springen auf den neuen Koerper.
6. **Speichern/Laden:** die Engine speichert Art + Groesse (Klemme [0,72, 1,35] der neuen Definition), das Register `body`/`gen`; nach dem Laden
   bindet der Suchlauf das grosse Tier ueber den Spiegel (`u`, `gen`) -> `rec.body = "big"`, kein neuer Tausch.
7. **Tod** des grossen Koerpers: wie B1a (`resolve` sieht `isDead` am Objekt der Sitzung -> `B.Close(rec, "dead")`, Meldung "Your bear is dead...",
   Sperre). Leiche zerlegbar (`AnimalPartsDefinitions["ncbeargrownbrown"]`, 2.2).
8. **Besitzer offline (MP):** `g` steht (B1d 0.9), also kein neuer Wunsch-Koerper. Ist die Gegend geladen (anderer Spieler nah), tauscht nur ein
   B1d-Spielstand (Nr. 11) -- harmlos, beide Koerper gehoeren zum selben Eintrag.
9. **Zweiter Spieler:** sieht das Junge verschwinden und den grossen Koerper an derselben Stelle erscheinen (Server erzeugt/entfernt; F12);
   seine Sicht bekommt `bd = "big"`, `sz` und die neue OnlineID; seine Groessen-Probe setzt nur an einer Kopie der passenden Art (1.2.4).
   Fuettern/Streicheln durch ihn: wie B1b (`Why_NotOwner`).
10. **Absturz mitten im Tausch:** dazwischen speichert die Welt nicht (ein Lua-Aufruf). Was nach einem Absturz von verschiedenen Speicherstaenden
    uebrig bleiben kann und was die Heilung tut: Tabelle 4.3 -- in jedem Fall genau ein gebundener Koerper, Kopien werden unbeobachtet entfernt
    (Voraussetzung: `B.ScanAnimals` sieht BEIDE Arten, Stelle 3.10).
11. **Spielstand von B1d** (Junges ueber 0,75 im Junges-Modell, `rec.body` fehlt): beim Binden `rec.body = "cub"`, erster sicherer `GrowLive`
    tauscht (und `B.GrowFix` meldet nichts -- erwartet).
12. **Wilde Junge:** `B.BodyWant` gibt fuer jeden Zustand ausser `tame`/`missing` `"cub"`; `GrowLive` laeuft nur fuer `tame`. Nie ein Tausch.

### 1.2 (Auftrag 2) Groesse
1. Junges: waechst wie B1d bis 0,75 (Tag 15) im Junges-Modell. Grosser Koerper ab Tausch: 0,72 -> Tag 45 0,982 -> Tag 100 1,35 (Tabelle 2.4).
2. Jeder Hirn-Takt setzt die Groesse des VORHANDENEN Koerpers nach (`B.ApplySize(a, B.BodySize(rec, have))`); beim Warten auf einen sicheren
   Tausch bleibt das Junge bei 0,75 (nie bekommt ein Junges-Koerper Erwachsenen-Groesse oder umgekehrt).
3. Neue Definition `minSize = 0,72`, `maxSize = 1,35`, `ageToGrow = 36500` -> Laden, MP-Erstuebertragung, Alterstag und Tierzone klemmen in
   [0,72, 1,35] (FD 0.2, Weg B wie B1d); ein frischer grosser Koerper steht ohne unser Setzen schon bei 0,72 (`initSize` -> minSize, NUR JAR
   FD 0.8) -- falls `setSizeForced` direkt nach `addToWorld` nicht wirkt (ungeprueft), faellt nichts auf.
4. MP-Client: Groessen-Probe der Anzeige (`S:client/ISUI/BanditsNPCBearHud.lua:459`) nur, wenn `B.BodyKind(kopie) == (c.bd or "cub")`
   (im Tauschfenster ist die alte Kopie evtl. noch da).
5. Namensschild sitzt beim grossen Koerper ueber dem Buckel: Anker `tagZ x sz / tagBase x tagBigK` (1,06 = Oberkante gross/Junges bei
   gleicher Groesse, `M:57`); Tag 100: 1,35 / 0,35 x 1,06 = 4,09 < Deckel `ZK_MAX` 5.

### 1.3 (Auftrag 3) Zurueck, Speichern/Laden, Mitfahren, Call to me, Heilung
1. **Zurueck:** `NCBear_CubGrow(-100)` -> `B.GrowSetG(rec, 0)` (setzt jetzt auch `s.swapAt = nil`, `s.swapTryAt = nil`: von Hand gibt es keine
   Abklingzeit) -> `B.BrainTick(true)` -> `GrowLive`: s 0,35 < 0,70 -> Tausch "shrink" (gleicher Ablauf 1.1.4, Ziel `"cub"`, Groesse 0,35).
   Zwischen 0,70 und 0,75 bleibt der grosse Koerper bei 0,72 (Schwelle 0.4).
2. **Mitfahren:** Einsteigen entfernt den Koerper wie B1c (`rec.body` bleibt der letzte Koerper). Waehrend der Fahrt waechst `g`. Aussteigen:
   `B.PlaceCub(..., "ride")` ohne Koerper-Vorgabe -> `B.BodyOf(rec)` -> steigt als der Koerper aus, den es haben will. Einsteigen prueft
   weiter `B.CubDefOk("cub")` (Rueckfall-Koerper, 0.3).
3. **Call to me:** `B.PlaceCub(..., "call")` erzeugt `B.BodyOf(rec)`, dann `B.RemoveCub(alt)` (jede der beiden Arten). Ein wartender Tausch ist
   damit erledigt.
4. **Speichern/Laden:** 1.1.6. Abklingzeiten des Tauschs nur in der Sitzung (nach dem Laden frei).
5. **Register-Heilung:** Spiegel v2 traegt neu `body` (`MARK_FIELDS`, `B.MARK_V` bleibt 2). Beim Binden/Wiederherstellen gilt der Koerper
   des Tiers (`B.BodyKind(o)`), der Spiegel-Wert nur zur Diagnose (weicht er ab: `B.Log`). Ein grosser Koerper mit Spiegel eines NICHT
   gezaehmten Eintrags wird nie wiederhergestellt (nil + `capLine`), und `B.RecOf` macht aus einem grossen Koerper ohne Eintrag nie einen
   neuen Fund ("found") -- er bleibt unberuehrt (Menue: `Why_Gone`) bzw. wird als Waise/Kopie nach den B1b/B1c-Riegeln entfernt.

### 1.4 (Auftrag 4) Alles aus B1a-B1d gilt fuer beide Koerper
Jede Art-Frage geht ueber `B.BodyKind` (Liste 3.2). Folgen/Bleiben, Name und Schild, Rechtsklick (Fuettern, Hinhalten, Streicheln, Modus,
Name, Call to me), Verstecken vor Zombies, Laerm-Flucht abfangen, Mitfahren, Call to me, Karten-Symbol, Anzeige-Optionen, Spiegel und
Bench sehen beide Koerper. Zusaetzlich je Koerper: Tempo und Abstaende (1.5), Schild-Hoehe (1.2.5), Streichel-Haltung (`petAnimBig =
"cow"`, `AnimalSizeY = (sz - 0,72) / (1,35 - 0,72)` geklemmt 0,01..1, Form `V:shared/TimedActions/Animals/ISPetAnimal.lua:27-32`, Werte
aus der Sicht `B.ViewOf(animal)` statt `getData` -- F4), Texte (Big-Fassung, 6.8). Fuettern: der Fress-Knoten `NCBear_Eat` traegt das grosse
Modell auch (FE 4.1). Die Markierung zeigt nur WILDE Junge (vom Tausch nicht betroffen).

### 1.5 (Auftrag 5) Tempo und Abstaende
1. Tempo kommt nur aus dem Clip (FE 4.4; `buck` hat keinen Tempo-Regler). Stellwerte je Koerper = gemessener Clip-Weg: Junges `walkSpeed`
   0,52 / `runSpeed` 2,47 (alt, passt wieder), gross `walkSpeedBig` **0,67** / `runSpeedBig` **3,17** (FE 4.4: 0,3784 E / 0,9 s bzw.
   1,0578 E / 0,533 s x MotionScale 1,6; Nachbesserung B1e B3: vorher stand hier faelschlich "x 1,6 x 1,5"). Benutzt in: Gehen-Regel (Besitzer langsamer als walkSpeed -> gehen; `c.walkSpeed`), Wegzeit des eigenen
   Befehls (`B.MoveTo` -> `ownUntil`, Laerm-Wache), Sprungdeckel der Kondition (`stamina`, `runSpeed`).
2. **Fussgleiten (ehrlich):** nach dem Tausch -28 % (wie das Junge kurz vorher), um Tag 47 null, bei 1,35 +35 % "Tretmuehle" (FE 4.3). Mit Lua
   nicht behebbar -> **im Spiel ansehen** (F6); ein eigener Geh-Knoten mit `m_SpeedScale` waere Modell-/Animset-Arbeit (nicht B1e).
3. **Abstaende mit der Koerperlaenge** (Mitte zu Mitte): `gap = B.BodyGap(body, sz) = max(0, (bodyLenBig x sz x tilesPerE - followRefLen) / 2)`,
   nur gross; 1,0448 E (`M:51`) x 1,5 Kacheln/E; Bezug 1,12 = Laenge des Jungen bei 0,75. Tag 15: 0,00 / Tag 45: 0,21 / Tag 100: **0,50** Kacheln
   (Nachbesserung B1e B3: vorher "0,27"; (1,0448 x 0,9825 x 1,5 - 1,12) / 2 = 0,21).
   Wirkt auf `followNear` (halten bis), `followStart` (losrennen ab), `followGap` (Ziel vor dem Besitzer) und `hideGap` (Versteck hinter
   dem Besitzer). Beim Jungen 0 -> Zahlen wie B1c. Im Spiel ansehen.
4. Kollision `collisionSize 0,30` (wirkt x Groesse: 0,22 beim Tausch, 0,41 bei 1,35; gespielter Erwachsener 0,42 bei 1,0) -- im Spiel ansehen (F10).

### 1.6 (Auftrag 6) Bench (nur `client/NCBearBenchCub.lua`, nur SP)
- `NCBear_CubStats()`: zusaetzlich `body <rec.body> / want <B.BodyWant> / engine type <getAnimalType des lebenden Tiers>`, `swap ready / waits
  (<Grund aus B.BodySwapReady>)`, `last swap <s> s ago`, `fails <n>`.
- `NCBear_CubGrow(tage)`: unveraendert `B.GrowSetG` + `B.BrainTick(true)` -> der Tausch kommt im selben Aufruf; die Ausgabezeile nennt den Koerper
  danach ("... body big (swapped)" / "... body cub, swap waits: calm").
- `NCBear_CubClean()` und `nearestCubObject` (fuer `NCBear_CubMark`) ueber `B.BodyKind` (beide Arten, nie `bear`).
- Rechtsklick "NC Bear": kein neuer Eintrag noetig ("Cub: grow 5 days" loest den Tausch an Tag 15 aus).

### 1.7 (Auftrag 7) Markierung groesser (OBERFLAECHE, `client/ISUI/BanditsNPCBearMarker.lua` neu geschrieben)
1. **Ziel und Zeiten wie heute** (`target(now)` unveraendert): das wilde Junge des Spielers (`B.View.me.wild`), solange `new` und bis
   `markerAfterMs` (60 s) nach dem ersten `shy`, das dieser Client sieht; weg bei angefuettert/gezaehmt/Eintrag weg/keine Lage; Doppelklick blendet
   fuer DIESES Junge aus. Takt `markerMs` 400 ms (OnTick, gedrosselt).
2. **Eigenes Element** `local Mk = ISUIElement:derive("BanditsNPCBearMarkerUI")`, genau EINES je Spielstart (OnGameStart: altes abmelden, neues
   anlegen, unsichtbar). Sichtbar nur mit Ziel (`setVisible`); gezeichnet wird nur, wenn sichtbar.
3. **Groesse:** Faktor f aus der Option `MarkerSize` (Index 1 = Auto, 2..7 = 100/125/150/200/250/300 %); Auto = naechste Stufe zu
   `getCore():getScreenHeight() / 1080` (geklemmt 1..3; Gleichstand -> groessere Stufe): 1080 -> 1,0, 1440 -> 1,25, Kevins 2054 -> **2,0**,
   2160 -> 2,0, 3240 -> 3,0. Neu gerechnet bei `OnResolutionChange` und wenn sich der Optionswert aendert (`U.Opt`, 1 s Zwischenspeicher).
4. **Lage wie Bandits x f:** Element (Klickflaeche) `45 f` x `45 f` an `(Breite/2 - 48 f, 48 f)`; ist Bandits geladen und hat der Spieler eine
   gemerkte Stelle (`player:getModData()["BanditEventMarkerPlacement"]` = { x, y }, nur LESEN, Bandits-Riegel), dann dort. Mitte des Kreises =
   Elementmitte, geklemmt, so dass der Kreis ganz auf dem Bild bleibt. **Ueberdeckung** (beim Einblenden einmal): liegt ein sichtbarer
   Bandits-/NPC-Crew-Marker (`BanditEventMarkerHandler.markers[*]`, `getDuration() > 0`, `getIsVisible()`) mit seiner Kreismitte
   (`m.x + 22,5`, `m.y + 22,5`) naeher als `48 + 48 f` an unserer, wird unsere um `markerShift x f` (100 x f) nach rechts geschoben.
5. **Zeichnen je Bild** (4 Bilder + 1 Text, keine Tabelle, kein `getText`): Scheibe `BanditsNPCBearMarker_disc.png` skaliert auf `96 f`,
   gefaerbt `markerR/G/B` (1,0 / 0,52 / 0,09 = heutiges Orange nach Bandits' Mischung, FE 6.1); Pfeil: `DrawTextureAngle(arrow[f], mx, my,
   winkel)` mit dem Pfeil-Bild der Stufe (`_arrow096` ... `_arrow288`), in der Naehe (<= `markerCloseTiles` 6,6 Kacheln) stattdessen der Ring
   ohne Spitze (`_ring.png` skaliert); Symbol `BanditsNPCBearCub_marker288.png` skaliert auf `96 f`, weiss; Text "Bear cub nearby"
   (`UI_BN_Bear_Marker_Cub`, einmal je Sitzung gebaut) zentriert bei `my + 25 f`, Schrift Small (f < 1,25) / Medium (< 1,75) / Large.
6. **Richtung:** im 400-ms-Takt `winkel = (deg(atan2(zy - py, zx - px)) + markerAngleAdd) % 360` aus Welt-Koordinaten (Spieler `getX/getY`,
   Ziel live oder aus der Sicht) mit `markerAngleAdd` 135 -- dieselbe Ausrichtung wie Bandits' gespielter Pfeil (Form `B:client/BanditEventMarkers.lua`
   `setAngleFromPoint`, Pfeil-Bild mit der Spitze nach OBEN wie `Bc:ui/eventMarker.png`, nachgemessen: Spitze bei y 16 von 96). Abstand
   `B.DistXY` -> nah/fern. Ausrichtung im Spiel ansehen (Stellwert).
7. **Ohne Bandits:** zeigt genauso (F11). Mit Bandits: wir rufen `BanditEventMarkerHandler.set` NICHT mehr; ein altes Element mit unserer Id
   gibt es nach dem Neustart nicht (Bandits-Marker werden nicht gespeichert).
8. **MP / geteilter Bildschirm:** rein Client, Sicht dieses Clients, nur Spieler 1 (`getSpecificPlayer(0)`, wie heute).
9. **Optionen-Seite** (`client/BanditsNPCBearOptions.lua`): nach `TagSize` `addComboBox("MarkerSize", "UI_BN_Bear_MO_MarkerSize",
   "UI_BN_Bear_MO_MarkerSizeTip")` mit `addItem` "UI_BN_Bear_MO_Auto" (Vorgabe, true), "..._Pct100" ... "..._Pct300" (6.7).

---

## 2. Die neue Art

### 2.1 Name (Kollisionsprobe)
**`ncbeargrown`** (Konstante `B.BIG`). Probe 11.11. ~16:25 (grep, Gross/Klein wie geschrieben): `ncbeargrown`, `B.BIG`, `BodyKind`,
`MarkerSize`, `BanditsNPCBearMarker_`, `NCBearGrown` -> **0 Treffer** in NPC Crew `42/media/lua` + `_docs/landkarte_index.txt`, Vanilla
`media/lua` + `media/scripts`, Bandits 42.22 + common, Test-Mod `42/media`. Namensraum `ncbear` erlaubt (`baer_uebernahme.py` OWN_NAME_RES).
**Endgueltig** (steht in Spielstaenden; ein gespeichertes Tier unbekannter Art bricht das Laden, `S:shared/BanditsNPCBearDefs.lua:9`). F2.
Tiername im Spiel `IGUI_AnimalType_ncbeargrown`: EN "Bear" (7 Sprachen, 6.8).

### 2.2 Definition (KERN, `S:shared/BanditsNPCBearDefs.lua`, Dateiebene, nach der Junges-Art)
Kopie der Junges-Definition (Form wie `T:shared/NCBearBenchVergleichDefs.lua:13-40`: Felder per `pairs` kopieren, `breeds`/`stages` NEUE
Tabellen), dann:
| Feld | Wert | Grund |
|---|---|---|
| `bodyModel` | `"NCBear_Body"` | heutiges grosses Modell (`T:media/scripts/nc_bear_tier.txt`, module Base), 0.13 |
| `breeds.brown` | Kopie der Junges-Rasse mit `texture`/`textureMale`/`textureBaby = "NCBear"`; `sounds` wie Junges (`fallover`, `petting`) | `T:shared/NCBearDefs.lua:40-41`; keine Erwachsenen-Stimmen (B5a) |
| `stages` | `{ ncbeargrown = { ageToGrow = 36500 } }`, kein `nextStage` | wie Junges (PB1D 0.3) |
| `minSize` / `maxSize` | **0,72** / 1,35 | 1.2.3; `swapSize` muss = minSize sein (Kommentar an beiden Stellen) |
| `animalSize` / `collisionSize` | 0,3 / **0,30** | wie `bear` (`T:shared/NCBearDefs.lua:75`) / F10 |
| `shadoww` / `shadowfm` / `shadowbm` / `corpseSize` | 0,9 / 1,8 / 1,8 / 3,0 | wie `bear` (`:77-80`), wachsen x Groesse |
| `minWeight` / `maxWeight` / `minBlood` / `maxBlood` / `trailerBaseSize` | 60 / 200 / 800 / 2000 / 300 | Vorschlag (kein Hochheben, kein Anhaenger) |
| alles andere | wie Junges: `animset "buck"`, `group "ncbear"`, `male true`, `genes` (Kopie), `wild false`, `canBeDomesticated false`, `alwaysFleeHumans false`, `fleeZombies false`, `canBePicked false`, `canThump false`, `canBeAlerted false`, `sitRandomly false`, `needMom false`, `feedByHandAnim "AnimalLureLow"`, `dontAttackOtherMale true`, `wanderMul 600`, `idleTypeNbr 0`, `spottingDist 10` | FE 1.2 (Vorgaben waeren Fliehen/Aufheben/Stossen) |
Dazu `AnimalAvatarDefinition["ncbeargrown"]` = Werte von `buck` (wie `:114-131`), `AnimalPartsDefinitions.animals["ncbeargrownbrown"] =
...["buckwhitetailed"]` (wie `bear`, `T:shared/NCBearDefs.lua:125`). Gruppe `ncbear` steht schon in NPC Crews `NOT_TENDED` (Naht 1).

### 2.3 Modell-Skript
Keins neu (0.13). bodyModel `NCBear_Body` -> `T:media/scripts/nc_bear_tier.txt` (`animationsMesh NCBear`, meshFile `Skinned/NCBear.glb`,
MD5 08ec7806, 26 Knochen, 15 Clips inkl. `NCBear_Eat`, FE 4.1). Textur `T:media/textures/Body/NCBear.png` (4cfdb177). Beide liegen in der
Test-Mod (Altlast bis B5a) -> Naht 10.3.

### 2.4 Groessen-Abbildung (gemessen, Spiel-Importer-Dump, Idle Bild 0, bei Groesse 1,0)
| Mass | altes Junges 6c3f0a96 | grosser Baer 08ec7806 | gross/Junges | Fundstelle |
|---|---|---|---|---|
| Laenge Nase-Rumpf | 0,9966 E (1,83 m) | 1,0448 E (1,92 m) | 1,048 | `M:36`, `M:51`, `M:57` |
| Oberkante | 0,5894 E (Kopf) | 0,6254 E (Buckel) | 1,061 | `M:57`, FE 4.2 |
| Breite | 0,4819 E | 0,4867 E | 1,010 | `M:57` |
Tauschgroesse gross **`swapSize` 0,72** (Laenge +0,6 %, Oberkante +1,9 %, `M:60`; woertlich 0,75 gaebe +4,8 / +6,1 %, `M:61` -> F1).
| Tag (D 100) | s innen | Koerper | sz gezeigt | Laenge m | Oberkante m | Gehen Rumpf / Fuss (Kacheln/s) | Abstand-Zuschlag |
|---|---|---|---|---|---|---|---|
| 0 | 0,350 | Junges | 0,350 | 0,64 | 0,38 | 0,52 / 0,18 | 0 |
| 14 | 0,723 | Junges | 0,723 | 1,33 | 0,78 | 0,52 / 0,38 | 0 |
| **15** | 0,750 | **gross** | **0,720** | 1,38 | 0,83 | 0,67 / 0,48 | 0,00 |
| 30 | 0,875 | gross | 0,851 | 1,63 | 0,98 | 0,67 / 0,57 | 0,11 |
| 45 | 1,000 | gross | 0,982 | 1,89 | 1,13 | 0,67 / 0,66 | 0,21 |
| 60 | 1,095 | gross | 1,082 | 2,08 | 1,24 | 0,67 / 0,73 | 0,29 |
| **100** | 1,350 | gross | **1,350** | 2,59 | **1,55** | 0,67 / 0,91 | 0,50 |
Kontrolle Tag 100: 1,0448 E x 1,35 / 0,544 = 2,59 m Nase-Rumpf (Ruhelage 1,0645 E -> 2,64 m), Oberkante 0,6254 x 1,35 / 0,544 = 1,55 m = Kevins
Tabelle ENT:10. Abstand-Zuschlag = 2.5. Gehen "Fuss" = Clip-Tempo x sz (Gleiten = Differenz, F6).

### 2.5 Tempo und Abstaende je Koerper (Stellwerte, 5)
| Wert | Junges | gross | Quelle |
|---|---|---|---|
| `walkSpeed` / `runSpeed` (Kacheln/s) | 0,52 / 2,47 | `walkSpeedBig` 0,67 / `runSpeedBig` 3,17 | FE 4.4 (Clip-Weg / Dauer x MotionScale 1,6; Nachbesserung B1e B3) |
| Abstand-Zuschlag `gap` | 0 | `max(0, (1,0448 x sz x 1,5 - 1,12) / 2)` | FE 4.4 letzter Punkt |
| Schild-Faktor | 1 | `tagBigK` 1,06 | `M:57` |
| Streicheln | `petAnim "lamb"`, `AnimalSizeY 0,5` | `petAnimBig "cow"`, `AnimalSizeY` aus sz | Vanilla `AnimSets/player/petanimal/petcow.xml` (Knoten `petcow`), F4 |

---

## 3. Der Helfer und alle Stellen

### 3.1 Helfer (KERN, `S:shared/BanditsNPCBear.lua`, nach `B.CUB`)
```
B.BIG = "ncbeargrown"                                   -- Tierart des grossen Koerpers (B1e)
B.BODY_TYPE = { cub = B.CUB, big = B.BIG }              -- Koerper -> Art
B.TYPE_BODY = { [B.CUB] = "cub", [B.BIG] = "big" }      -- Art -> Koerper (nie "bear", "bearstag", "ncbearcubalt")
function B.BodyKind(animal)   -- "cub" | "big" | nil; einziger Engine-Aufruf animal:getAnimalType() (V:client/ISUI/Animal/ISAnimalUI.lua:65)
```

### 3.2 Alle Stellen (FE 2), die ihn benutzen
| # | Datei:Zeile (heute) | heute | B1e | Bauer |
|---|---|---|---|---|
| 1 | `S:shared/BanditsNPCBear.lua:29` | `B.CUB = "ncbearcub"` | + `B.BIG`, Tabellen, `B.BodyKind` | KERN |
| 2 | `S:shared/BanditsNPCBear.lua:476` `B.ViewOf` | `~= B.CUB` | `if not B.BodyKind(animal) then return nil end` (Menue, Hud, `U.CubObj`, Karte, Markierung, Streicheln) | KERN |
| 3 | `S:server/BanditsNPCBearServer.lua:156` `handCheck` | `~= B.CUB` | `B.BodyKind` (Fuettern, Streicheln) | KERN |
| 4 | `S:server/BanditsNPCBearRegistry.lua:341` `B.RecOf` | `~= B.CUB` -> "kind" | `B.BodyKind`; grosser Koerper ohne Eintrag nach der Heilung -> `nil, "kind"` (nie "found") | KERN |
| 5 | `S:server/BanditsNPCBearWorld.lua:450-455` `findBreed` | `getDef(B.CUB)` | `findBreed(body)` mit `B.BODY_TYPE[body or "cub"]` | KERN |
| 6 | `S:server/BanditsNPCBearWorld.lua:457` `B.CubDefOk` | ohne Argument | `B.CubDefOk(body)` (nil = "cub") | KERN |
| 7 | `S:server/BanditsNPCBearWorld.lua:466-493` `B.CreateCub` | Art fest | `B.CreateCub(x, y, z, body)` (nil = "cub"; wilde Junge unveraendert) | KERN |
| 8 | `S:server/BanditsNPCBearWorld.lua:497` `B.RemoveCub` | `~= B.CUB` | `if not B.BodyKind(animal) then return end` | KERN |
| 9 | `S:server/BanditsNPCBearWorld.lua:514` `B.FindAnimal` | `~= B.CUB` | `B.BodyKind` | KERN |
| 10 | `S:server/BanditsNPCBearWorld.lua:651` `B.ScanAnimals` | `== B.CUB` | `B.BodyKind(o) ~= nil` (Binden, Heilung, Kopien, Doppel, Waisen beider Arten); AnimalID-Rueckfall setzt `rec.body` | KERN |
| 11 | `S:server/BanditsNPCBearRide.lua:102-103` `B.RideBoard` | `B.CubDefOk()` | `B.CubDefOk("cub")` (Rueckfall-Koerper), Text nennt beide Arten | KERN |
| 12 | `S:client/BanditsNPCBearMenu.lua:318` `onClickedAnimals` | `== B.CUB` | `B.BodyKind(a)`; `:315`/`:434` (`not B.CUB` = Existenz) bleiben | OBERFLAECHE |
| 13 | `S:client/ISUI/BanditsNPCBearHud.lua:247` `scan` | `== B.CUB` | `B.BodyKind(o)` | OBERFLAECHE |
| 14 | `S:client/NCBearBenchCub.lua:397`, `:640` | `== B.CUB` | `B.BodyKind(o)` | OBERFLAECHE |
| 15 | `S:server/BanditsNPCBearGrow.lua:416-425` `B.GrowLive` | Fehlerzeile `bodySwap` | Tausch (1.1) | KERN |
| 16 | `S:shared/BanditsNPCBearStats.lua:225-230` `B.BodyOf` | immer "cub" | `want, BodySize(want)` (6.2.2) | KERN |
| 17 | `S:server/BanditsNPCBearRegistry.lua:298`, `S:server/BanditsNPCBearHeal.lua:226` | `kind = "cub"` | bleibt (Eintrag-Art); Koerper ist NEUES Feld `rec.body` | - |
| 18 | `S:shared/BanditsNPCBearDefs.lua:29`, `:75` | Art Junges | + Art `ncbeargrown` (2.2) | KERN |
| 19 | `S:shared/Translate/<L>/IG_UI.json` | `IGUI_AnimalType_ncbearcub` | + `IGUI_AnimalType_ncbeargrown` x 7 | OBERFLAECHE |
| 20 | `S:client/ISUI/BanditsNPCBearHud.lua:443-459` Groessen-Probe | ohne Art-Frage | nur `B.BodyKind(obj) == (c.bd or "cub")` | OBERFLAECHE |
| 21 | `S:server/BanditsNPCBearGrow.lua:427-428`, `:479-480`, `:633-634` | `B.BodyOf` -> `ApplySize` | `B.BodySize(rec, B.BodyKind(a))` (nur passender Koerper) | KERN |
| 22 | `S:server/BanditsNPCBearHeal.lua` `bind`, `B.Restore` | - | `rec.body = B.BodyKind(o)`; Restore: grosser Koerper + Spiegel nicht tame/missing -> nil "body" | KERN |
| 23 | `S:shared/TimedActions/BanditsNPCBearPetAction.lua:48-62` | Haltung fest | Haltung je Koerper aus `B.ViewOf` (1.4) + Beschaeftigt-Marke | KERN |
Indirekt koerper-frei (bekommen das Objekt, laufen mit 9/10 fuer beide): Laerm-Wache, Zombie-Wache, Folgen, `B.MoveTo`, `B.Hold`, `B.RideStep`,
`markProbe`, `B.BodyHp`, Fuetter-Aktion, Karte (`U.CubObj` -> `B.ViewOf`), Markierung (`U.CubPos`).

---

## 4. Register, Spiegel, Sicht, Sitzung (Ergaenzungen)

### 4.1 Register und Sitzung
```
rec += { body = "cub" | "big" | nil }          -- nur tame/missing; Koerper, den der Eintrag zuletzt hatte (nil = noch nie gebunden/B1d-Stand)
B._s[id] += { swapAt, swapTryAt, swapFailN, busyUntil }   -- nur Sitzung, nie gespeichert; geleert mit der Sitzung (B.Close, InitRegistry)
```
`B.GrowFix` (Grow.lua): `body` nur "cub"/"big", sonst nil; bei anderen Zustaenden nil (`FIELDS` += "body"). Gesetzt in `B.PlaceCub`
(VOR `B.Commit`/`B.WriteMark`), `bind` und `B.Restore` (Heal.lua), AnimalID-Rueckfall in `B.ScanAnimals`, `B.GrowBody`, `B.GrowLive`
(Korrektur ohne Commit). `clearBodySession` (Ride.lua) laesst `swap*`/`busyUntil` stehen (sie gehoeren zum Eintrag).

### 4.2 Spiegel und Sicht
- `MARK_FIELDS` (`S:server/BanditsNPCBearHeal.lua:40-44`) += `"body"`; `B.MARK_V` bleibt 2; `B.MarkFresh` unveraendert (v/id/u/r).
- Sicht (`B.GrowView`, nur `tame`): neu `bd` = Koerper (Text "cub"/"big"); `sz` = gezeigte Groesse des VORHANDENEN Koerpers
  (`B.BodyNow`). `B.ApplySync` kopiert flach (`copyFlat`) -- nichts zu tun. Wilde: kein `bd` (= cub).
- Meldungen: `bd = "big"` an den Noten 6.4 (flaches Feld, geht durch `sendServerCommand`).

### 4.3 Absturz / Speicherstaende (was liegt wo, was heilt)
| Fall | Zustand nach dem Laden | Ergebnis |
|---|---|---|
| Register NACH dem Tausch gespeichert, Zelle davor | Eintrag `gen N+1`, `body big`; Zelle: Junges mit Spiegel `gen N` | Junges = "stale" (`mark.gen < rec.gen`) -> unbeobachtet entfernt; Eintrag ohne Koerper -> "missing" nach 3 Suchlaeufen -> "Call to me" erzeugt `B.BodyOf` = gross |
| Zelle NACH dem Tausch, Register davor | Eintrag `gen N`, `body cub`; Zelle: grosser Koerper `gen N+1` | Heil-Regel 1a: `mark.gen >= rec.gen`, gleiches `u` -> binden, `rec.body = big`, `gen`/`aid` uebernommen |
| beide Koerper in der Zelle (verschiedene Chunks verschieden alt) | grosser `gen N+1` + Junges `gen N` | Suchlauf neueste zuerst (`newerFirst`), Junges "stale"/"dup" -> entfernt (beide Arten im Suchlauf, 3.2 Nr. 10) |
| Register leer, grosser Koerper mit Spiegel `tame` | - | `B.Restore` -> Eintrag mit `body big`, `g`/`x*` aus dem Spiegel, kein Tausch |
| Register leer, grosser Koerper mit Spiegel `new/shy/fed` (nur Faelschung moeglich) | - | nie hergestellt (nil "body", Fehlerzeile `capLine`), nie "found"; bleibt ungebunden stehen |
| grosser Koerper ohne Spiegel, kein Eintrag | - | Waise nach B1b-Riegeln (Alter, Beobachter) -> entfernt |

---

## 5. Stellwerte (`B.CFG`, KERN `S:shared/BanditsNPCBear.lua`; flach, zur Laufzeit per `NCBear_CubSet`)
| Feld | Vorgabe | Bedeutung |
|---|---|---|
| `bodySwap` | **true** (war false) | Tausch an; false = Not-Aus (`B.BodyWant` immer "cub": ein grosser Koerper wird wieder Junges) |
| `swapSize` | 0.72 | gezeigte Groesse des grossen Koerpers beim Tausch (= `minSize` der Art!) |
| `swapBackSize` | 0.70 | innere Groesse, unter der der grosse Koerper zurueck zum Jungen wechselt |
| `swapMinMs` / `swapRetryMs` / `swapFailLog` / `swapRing` | 60000 / 10000 / 6 / 2 | Abklingzeit je Eintrag / neuer Versuch nach Fehlschlag / Fehlerzeile ab Versuch / Ersatzkachel-Ringe |
| `swapFaceDist` | 30 | neuer Koerper schaut zum Besitzer, wenn naeher (0 = aus) |
| `busyMs` | 20000 | Fuettern/Streicheln sperren den Tausch hoechstens so lange |
| `swapMoveMaxMs` | 10000 | Nachbesserung B1e B2: eigener Rennbefehl sperrt den Tausch hoechstens so lange (seit dem ersten Takt mit want ~= have) |
| `callFreshMs` | 2000 | Nachbesserung B1e B1: "Call to me" tut nichts, solange ein eben erzeugter Koerper noch nicht in der Welt ist (hoechstens so lange) |
| `walkSpeedBig` / `runSpeedBig` | 0.67 / 3.17 | Tempo des grossen Koerpers (Kacheln/s) |
| `bodyLenBig` / `tilesPerE` / `followRefLen` | 1.0448 / 1.5 / 1.12 | Abstand-Zuschlag (2.5) |
| `tagBigK` | 1.06 | Schild-Hoehe gross / Junges (OBERFLAECHE liest) |
| `petAnimBig` | "cow" | Streichel-Haltung am grossen Koerper |
| `markerAngleAdd` / `markerCloseTiles` | 135 / 6.6 | Pfeil-Ausrichtung (Bandits-Konvention) / ab hier kein Pfeil (OBERFLAECHE liest) |
| `markerR` / `markerG` / `markerB` | 1.0 / 0.52 / 0.09 | Kreisfarbe (OBERFLAECHE liest) |
Bleiben: `cubMaxSize` 0,75 (= Schwelle hin), `stageAt[3]` 1,35 (= Ende), `walkSpeed`/`runSpeed` 0,52 / 2,47 (Junges), `markerShift` 100,
`markerMs` 400, `markerAfterMs` 60000 (`markerDur` wird unbenutzt, bleibt stehen). OBERFLAECHE liest jeden Wert mit eigenem Rueckfall.

---

## 6. GENAUE SCHNITTSTELLE (WOERTLICH einhalten; Abweichung sofort nach `schnittstelle_aenderungen.md`, Abschnitt "B1e KERN" / "B1e OBERFLAECHE")

### 6.1 Wer schreibt welche Datei (unter `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | Bauer | Was |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | KERN | `B.BIG`, `B.BODY_TYPE`, `B.TYPE_BODY`, `B.BodyKind`, `B.NoteBd`, `B.ViewOf` (3.2 Nr. 2), `B.CFG` (5), Kopf-Kommentar |
| `lua/shared/BanditsNPCBearDefs.lua` | KERN | Art `ncbeargrown` (2.2) |
| `lua/shared/BanditsNPCBearStats.lua` | KERN | 6.2.2 |
| `lua/shared/BanditsNPCBearRules.lua` | KERN | `B.FollowDecide`/`B.GuardDecide` lesen `c.gap`, `c.walkSpeed` (6.3) |
| `lua/shared/TimedActions/BanditsNPCBearPetAction.lua`, `...FeedAction.lua` | KERN | Beschaeftigt-Marke; Pet: Haltung je Koerper (6.3) |
| `lua/server/BanditsNPCBearWorld.lua` | KERN | 3.2 Nr. 5-10, `B.SwapSpot`, `B.MoveTo` Tempo je Koerper |
| `lua/server/BanditsNPCBearRide.lua` | KERN | `B.PlaceCub(..., body)`, `B.RideBoard`, Noten `bd` |
| `lua/server/BanditsNPCBearGrow.lua` | KERN | `B.GrowLive`, `B.BodySwap`, `B.BodySwapReady`, `B.BodyBusy`, `B.GrowBody`, `B.GrowSetG`, `B.GrowFix`, `B.GrowView`, `stamina` |
| `lua/server/BanditsNPCBearHeal.lua` | KERN | `MARK_FIELDS`, `bind`, `B.Restore` (3.2 Nr. 22) |
| `lua/server/BanditsNPCBearRegistry.lua` | KERN | `B.RecOf` (3.2 Nr. 4) |
| `lua/server/BanditsNPCBearServer.lua` | KERN | `handCheck` (3.2 Nr. 3) |
| `lua/server/BanditsNPCBearFollow.lua` | KERN | `B.FollowStep` (`c.gap`, `c.walkSpeed`), Noten `bd` in `B.SetMode`/`B.HandleMode`/`B.HandleRename` |
| `lua/server/BanditsNPCBearGuard.lua` | KERN | `B.GuardStep` (`c.gap`) |
| `attrappe/kern/attrappen.lua` (Tier-Attrappe: zweite Art, `getSquare`, `faceThisObject`), `attrappe/b1e_kern/run.lua` (**neu**) | KERN | 7.1 |
| `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `U.EN` (+24, wortgleich EN), `U.TB`, `U.NoteText` (bd), `U.CubName` (bd) |
| `lua/client/BanditsNPCBearMenu.lua` | OBERFLAECHE | 3.2 Nr. 12; `U.TB` fuer `Menu_Name`, `Menu_CallTip`, `Why_CallWait` |
| `lua/client/BanditsNPCBearOptions.lua` | OBERFLAECHE | `MarkerSize` (1.7.9, 6.7) |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | 3.2 Nr. 13, 20; Schild-Faktor `tagBigK` |
| `lua/client/ISUI/BanditsNPCBearMarker.lua` | OBERFLAECHE | neu geschrieben (1.7, 6.6) |
| `lua/client/ISUI/BanditsNPCBearNameBox.lua` | OBERFLAECHE | Titel `U.TB("UI_BN_Bear_Name_Title", v.bd)` |
| `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | 1.6 -- wird nie kopiert |
| `lua/shared/Translate/<L>/UI.json` x 7, `.../IG_UI.json` x 7 | OBERFLAECHE | 24 + 1 Schluessel (6.8) |
| `ui/BanditsNPCBearMarker_disc.png`, `_ring.png`, `_arrow096/120/144/192/240/288.png`, `ui/BanditsNPCBearCub_marker288.png` (**9 neu**) | OBERFLAECHE | 6.9 |
| `ober_werkzeug/texte_b1e.py`, `ober_werkzeug/marker_bilder.py` (**neu**), `attrappe/b1e_ober/` (**neu**: `run.lua`, `texte_pruefen_b1e.py`, `bilder_pruefen_b1e.py`) | OBERFLAECHE | 7.2 |
| `staging_dateien.txt`, `models_X/Skinned/NCBearCub.glb` + `textures/Body/NCBearCub.png` (altes Junges), `attrappe/gesamt/` ("20 B1e", `xref_b1e.py`), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt` | ZUSAMMENBAU | 10 |
Unveraendert: `shared/BanditsNPCBearFood.lua`, `...Crew.lua`, `...TimedActions/BanditsNPCBearBaitAction.lua`, `client/ISUI/BanditsNPCBearMap.lua`,
`sandbox-options.txt`, `Sandbox.json` x 7, `scripts/nc_bear_cub.txt`, `ui/BanditsNPCBearCub_marker.png` (96er bleibt fuer die Karte).
Ladefolge wie PB1D 6.1 (shared `...Bear < Crew < Defs < Food < Rules < Stats`; server alphabetisch) -> fremde Funktionen nur zur Laufzeit.
Lua-Dateien LF, ASCII; kein `next(`, kein `%a`; keine Namen/Texte mit spawn/debug/test/bench/cheat ausser in der Bench. localcount < 180.

### 6.2 KERN: neue/geaenderte Funktionen
**6.2.1 `S:shared/BanditsNPCBear.lua`**
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.BodyKind(animal)` | `"cub"` / `"big"` / nil | `animal == nil` -> nil; `B.TYPE_BODY[animal:getAnimalType()]`. Auch Client. |
| `B.NoteBd(note, rec)` | note | `type(note) == "table" and type(rec) == "table" and rec.body == "big"` -> `note.bd = "big"`; sonst unveraendert |
| `B.ViewOf(animal)` | wie B1b | Art-Frage ueber `B.BodyKind` |

**6.2.2 `S:shared/BanditsNPCBearStats.lua`** (rein, auch Client)
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.BodyWant(rec)` | `"cub"`/`"big"` | `bodySwap == false` oder `rec.st` nicht tame/missing -> "cub"; s = `B.GrowSize(g)`; `s >= cubMaxSize - 1e-6` -> "big"; `s < swapBackSize` -> "cub"; sonst `rec.body` (fehlt -> "cub") |
| `B.BodySize(rec, body)` | sz (3 Nachkommastellen) | "big": `clamp(swapSize + (s - cubMaxSize) x (top - swapSize) / (top - cubMaxSize), swapSize, top)` mit `top = stageAt[3]`; sonst `min(s, cubMaxSize)` |
| `B.BodyOf(rec)` | want, sz | `B.BodyWant(rec)`, `B.BodySize(rec, want)` (Signatur wie B1d; jetzt auch "big") |
| `B.BodyNow(rec)` | body, sz | `body = rec.body` (nur "cub"/"big") sonst `B.BodyWant(rec)`; `B.BodySize(rec, body)` |
| `B.BodyNum(body, key, def)` | Zahl | `body == "big"` und `tonumber(B.CFG[key .. "Big"])` -> diese; sonst `tonumber(B.CFG[key])`; sonst def |
| `B.BodyGap(body, sz)` | Zahl >= 0 | nur "big": `max(0, (bodyLenBig x sz x tilesPerE - followRefLen) / 2)`; sonst 0 |
| `B.StatsOf(rec)` | + `body`, `want` | `body`, `sz` aus `B.BodyNow`; `want` aus `B.BodyWant` |
`B.ApplySize` unveraendert (einzige Stelle mit `setSizeForced`/`getData`).

**6.2.3 `S:server/BanditsNPCBearWorld.lua`**
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `findBreed(body)` (lokal) | Rasse oder nil | `AnimalDefinitions.getDef(B.BODY_TYPE[body] or B.CUB)` + `:getBreedByName(B.BREED)` |
| `B.CubDefOk(body)` | boolean | body nil -> "cub" |
| `B.CreateCub(x, y, z, body)` | animal, why | body nil/unbekannt -> "cub"; `addAnimal(getCell(), ..., B.BODY_TYPE[body], breed, false)` + `addToWorld()`; "nodef"-Zeile nennt die Art |
| `B.RemoveCub(animal)` | - | Riegel `B.BodyKind` |
| `B.FindAnimal(rec)` | animal/nil | Riegel `B.BodyKind` |
| `B.ScanAnimals(players, force)` | n, removed | Riegel `B.BodyKind`; im AnimalID-Rueckfall `rec.body = B.BodyKind(hit)` |
| `B.SwapSpot(a, turn)` | Kachel oder nil | `sq = a:getSquare()`; `spotOk(sq)` -> sq; sonst `B.SpotNear(x, y, z, swapRing, turn)` |
| `B.MoveTo(rec, animal, x, y, z, opt)` | wie B1c | Tempo `B.BodyNum(rec.body, "runSpeed"/"walkSpeed", 1)` |

**6.2.4 `S:server/BanditsNPCBearRide.lua`**
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.PlaceCub(rec, x, y, z, why, body)` | a, why | body gegeben -> genau dieser (kein Rueckfall); nil -> `B.BodyOf(rec)` (fehlt Stats: "cub"); misslingt "big" mit "nodef" -> `B.ErrEvery("placebig", 600000, ...)` + Junges-Koerper. `rec.body` = erzeugter Koerper VOR `B.Commit`. Rest wie B1c/B1d |
| `B.RideBoard` | wie B1c | `B.CubDefOk("cub")`; `Note_RideOn` ueber `B.NoteBd` |
| `B.RideStep`, `B.HandleCall` | wie B1c | `Note_RideOff`, `Note_Called`, `Why_Riding`, `Why_CallWait` ueber `B.NoteBd` |

**6.2.5 `S:server/BanditsNPCBearGrow.lua`**
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.BodySwapReady(rec, s, ms)` | ok, why | why: "state", "ride", "cool", "retry", "calm", "guard", "busy", "nodef"; Uhr rueckwaerts = abgelaufen (0.6) |
| `B.BodySwap(rec, a, want, ms)` | neues Tier oder nil, why | 1.1 Nr. 4 a-e; why "nospot" oder von `B.PlaceCub` |
| `B.BodyBusy(animal, on)` | boolean (gefunden) | Eintrag mit `s.obj == animal` (Schleife <= 64); on -> `s.busyUntil = ms + busyMs`, sonst nil |
| `B.GrowLive(rec, a, cx, cy, ms)` | - | 1.1 Nr. 1-3; die B1d-Fehlerzeile "body swap is not built yet" entfaellt |
| `B.GrowBody(rec, a)` | - | `have = B.BodyKind(a) or "cub"`, `rec.body = have`, `B.ApplySize(a, B.BodySize(rec, have))`, Rest B1d |
| `B.GrowSetG(rec, g, players)` | neues g | + `s.swapAt = nil`, `s.swapTryAt = nil`; Groesse nur fuer den vorhandenen Koerper |
| `B.GrowFix`, `B.GrowView` | wie B1d | + `body` (4.1) / + `t.bd`, `t.sz` aus `B.BodyNow` |
| `stamina` (lokal) | - | Sprungdeckel mit `B.BodyNum(rec.body, "runSpeed", 2.47)` |

**6.2.6 Heal.lua, Registry.lua, Server.lua, Follow.lua, Guard.lua, Rules.lua, Zeitaktionen** -- genau diese Stellen (6.3).

### 6.3 Aenderungen in vorhandenen KERN-Stellen
| Stelle | Aenderung |
|---|---|
| `Heal.lua` `MARK_FIELDS` (`:40-44`) | + `"body"` |
| `Heal.lua` `bind` (`:88-115`) | nach `rec.aid = ...`: `rec.body = B.BodyKind(o)`; weicht `mark.body` ab -> `B.Log` |
| `Heal.lua` `B.Restore` (`:175-261`) | `local body = B.BodyKind(o)`; `body == "big"` und `st ~= "tame"` -> `return nil, "body"`; neuer Eintrag `body = body` (nur bei tame) |
| `Registry.lua` `B.RecOf` (`:338-382`) | `B.BodyKind(animal)` statt `~= B.CUB`; vor `B.NewRec("found", ...)`: `if B.BodyKind(animal) == "big" then return nil, "kind" end` |
| `Server.lua` `handCheck` (`:154-156`) | `if not B.BodyKind(animal) then return nil end` |
| `Follow.lua` `B.FollowStep` (`:137`) | `local body, sz = B.BodyNow(rec)` (fehlt Stats: "cub", 0) ; `c = { x, y, z, gap = B.BodyGap(body, sz), walkSpeed = B.BodyNum(body, "walkSpeed", 0.52) }` |
| `Follow.lua` `B.SetMode` (`:104-117`), `B.HandleMode` (Why_Riding `:224`), `B.HandleRename` (`:275`) | Noten durch `B.NoteBd(n, rec)` |
| `Guard.lua` `B.GuardStep` (`:303`) | `{ x, y, z, st, gap = B.BodyGap(B.BodyNow(rec)) }` (nur gezaehmt; sonst 0) |
| `Rules.lua` `B.FollowDecide` (`:500`, `:525`, `:530`) | `local gap = tonumber(c.gap) or 0`; `followNear + gap`, `followStart + gap`, `followGap + gap`; `walkSpeed = tonumber(c.walkSpeed) or cfg.walkSpeed` |
| `Rules.lua` `B.GuardDecide` (`:612`) | `cfg.hideGap + (tonumber(c.gap) or 0)` |
| `PetAction.lua` `start()` (`:48-62`) | `local v = B.ViewOf and B.ViewOf(self.animal)`; `v and v.bd == "big"` -> Haltung `cfg.petAnimBig or "cow"`, `AnimalSizeY` aus `v.sz` (1.4); sonst wie B1d. SP (`not isClient() and not isServer()`): `if B.BodyBusy then B.BodyBusy(self.animal, true) end` |
| `PetAction.lua`/`FeedAction.lua` `serverStart()` | + `B.BodyBusy(self.animal, true)` (hinter `if B.BodyBusy`) |
| `PetAction.lua`/`FeedAction.lua` `complete()`, `serverStop()`, `stop()` | + `B.BodyBusy(self.animal, false)` (hinter `if B.BodyBusy`; im MP-Client fehlt die Funktion) |
| `FeedAction.lua` `start()` | SP: + Beschaeftigt-Marke wie Pet |

### 6.4 Meldungen (KERN schickt, OBERFLAECHE zeigt)
Mit `bd = "big"` (nur wenn `rec.body == "big"`): `Note_Follow`, `Note_Stay`, `Note_StayCar`, `Note_StayFar`, `Note_StayBehind`,
`Note_Renamed`, `Note_RideOn`, `Note_RideOff`, `Note_Called`, `Why_Riding`, `Why_CallWait`. Keine neue Meldung (0.10). `U.NoteText`:
`note.bd == "big"` und `U.EN[k .. "Big"] ~= nil` -> Schluessel `k .. "Big"`, sonst `k`.

### 6.5 OBERFLAECHE: Funktionen (nur unter `U`; an `B` nichts Neues)
| Funktion | Datei | Rueckgabe | Bemerkung |
|---|---|---|---|
| `U.TB(key, bd, a1, a2, a3)` | Client.lua | Text | `bd == "big"` und `U.EN[key .. "Big"]` -> `U.T(key .. "Big", ...)`, sonst `U.T(key, ...)` |
| `U.NoteText(note)` | Client.lua | Text/nil | 6.4 |
| `U.CubName(c, meKey)` | Client.lua | Text | Vorgabe-Name ueber `U.TB("UI_BN_Bear_Tag_Name", c.bd, who)` |
| `U.MarkerTick()` | Marker.lua | - | 1.7 (Takt, Ziel, Winkel, Sichtbarkeit) |
| `U.MarkerLayout()` | Marker.lua | - | Faktor, Lage, Groesse neu (Spielstart, Aufloesung, Option) |
| `U.MarkerFactor(h, idx)` | Marker.lua | f | rein (Tests): idx 2..7 -> Stufe, sonst Auto aus h |

### 6.6 Markierungs-Element (OBERFLAECHE, `client/ISUI/BanditsNPCBearMarker.lua`)
- `local Mk = ISUIElement:derive("BanditsNPCBearMarkerUI")`; `Mk:new(x, y, w, h)` ueber `ISUIElement.new(self, x, y, w, h)`; Felder nur
  Zahlen/Bilder; `Mk:render()` zeichnet 1.7.5 (nur wenn `self.on`); `Mk:onMouseDoubleClick()` -> `M.gone[M.cid] = true`, `setVisible(false)`,
  `return true`; keine Ziehen-Funktion (F7).
- Bilder je Sitzung einmal `getTexture("media/ui/<datei>.png")`, Tabelle `ARROW = { [1.0] = _arrow096, [1.25] = _arrow120, ... [3.0] = _arrow288 }`.
- Merk-Tabellen wie heute (`shyAt`, `gone`, Deckel 16). Element-Deckel: eins.
- Kein `pcall` (alles Vanilla-Lua; Bandits nur gelesen, je hinter Riegel `BanditEventMarkerHandler and type(BanditEventMarkerHandler.markers) == "table"`
  bzw. `BanditEventMarker ~= nil`); Lesefehler an Bandits-Feldern mit `tonumber`/`type` abfangen.

### 6.7 Mod-Optionen (OBERFLAECHE, nach `TagSize`, KEIN pcall)
```
local mk = o:addComboBox("MarkerSize", "UI_BN_Bear_MO_MarkerSize", "UI_BN_Bear_MO_MarkerSizeTip")
mk:addItem("UI_BN_Bear_MO_Auto", true)  mk:addItem("UI_BN_Bear_MO_Pct100")  mk:addItem("UI_BN_Bear_MO_Pct125")
mk:addItem("UI_BN_Bear_MO_Pct150")      mk:addItem("UI_BN_Bear_MO_Pct200")  mk:addItem("UI_BN_Bear_MO_Pct250")  mk:addItem("UI_BN_Bear_MO_Pct300")
```
Lesen `U.Opt("MarkerSize", 1)` (Index). Reihenfolge der Seite danach: TagShow, TagHealth, TagStamina, TagAge, TagSize, MarkerSize.

### 6.8 Texte (OBERFLAECHE, alle sieben Sprachen; Regeln wie PB1D 6.7: sortiert, Round-Trip, UTF-8 ohne BOM, LF, CN nur Vanilla-CN-Zeichen, `U.EN` wortgleich)
EN-Vorschlag, 24 neue `UI.json`-Schluessel:
`Tag_NameBig` "%1's bear" - `Note_FollowBig` "Your bear follows you." - `Note_StayBig` "Your bear stays here." - `Note_StayCarBig` "Your bear was too far
away to get in. It waits here." - `Note_StayFarBig` "Your bear could not keep up. It waits to the %1." - `Note_StayBehindBig` "Your bear stayed behind
to the %1." - `Note_RenamedBig` "Your bear is now called %1." - `Note_RideOnBig` "Your bear climbs in with you." - `Note_RideOffBig` "Your bear climbs
out." - `Note_CalledBig` "Here is your bear again." - `Why_RidingBig` "Your bear is riding with you." - `Why_CallWaitBig` "You can call your bear
again in about %1 min." - `Menu_NameBig` "Name the bear" - `Menu_CallTipBig` "Brings your bear right next to you if it is stuck. Works once every
%1 minutes." - `Name_TitleBig` "Name for your bear:" (15) -- `MO_MarkerSize` "Size of the cub marker at the top of the screen" - `MO_MarkerSizeTip`
"Auto grows with the screen height (1080p = 100%%, 4K = 200%%)." - `MO_Auto` "Auto" - `MO_Pct100` "100%%" - `MO_Pct125` "125%%" - `MO_Pct150` "150%%" -
`MO_Pct200` "200%%" - `MO_Pct250` "250%%" - `MO_Pct300` "300%%" (9; `%%` wie Vanilla `EN/UI.json` `UI_optionscreen_ActionProgressBarSize1` "100%%").
Platzhalter je Big-Schluessel gleich dem Grundschluessel. `IG_UI.json` x 7: `IGUI_AnimalType_ncbeargrown` (EN "Bear", PTBR "Urso", RU "Медведь",
KO "곰", ES "Oso", CN "熊" (in Vanilla-CN, FE 6.4), FR "Ours"). Keine Woerter spawn/debug/bench/cheat/test.

### 6.9 Bilder (OBERFLAECHE, eigene Zeichnung, `ober_werkzeug/marker_bilder.py`, PIL + numpy, 8-fach ueberabgetastet, RGBA)
| Datei | Groesse | Inhalt (Proportionen nach Bandits' Bild NACHGEMESSEN, nicht kopiert) |
|---|---|---|
| `BanditsNPCBearMarker_disc.png` | 288 | weisse Scheibe, Radius 22,5/96 der Bildgroesse (wird gefaerbt) |
| `BanditsNPCBearMarker_ring.png` | 288 | weisser Ring, Mitte 22/96, Dicke 3/96, ohne Spitze ("nah") |
| `BanditsNPCBearMarker_arrow096/120/144/192/240/288.png` | 96/120/144/192/240/288 | Ring wie oben + Spitze nach OBEN bis Radius 30/96 (Bandits: Spitze bis y 16 von 96) |
| `BanditsNPCBearCub_marker288.png` | 288 | Kevins Symbol W1 aus `baer/spiel/icon_zeichne_v2.py`, GLEICHER Bildausschnitt wie die 96er-Datei, 3-fach |
Nachweis im Bericht: Masse, Alpha-Rand, MD5; die 96er-Ausgabe des Symbol-Skripts ist byte-gleich mit `ui/BanditsNPCBearCub_marker.png`
(9e45e936) -- gelingt das nicht, Rueckfall: Symbol aus der 96er-Datei skaliert (unscharf ab 150 %) und Frage im Bericht. Deckel 512 px (Uebernahme
`UI_MAX_PX`), Namen im Raum `BanditsNPCBear` (`UI_ASSET`).

### 6.10 Was die OBERFLAECHE vom KERN ruft
`B.BodyKind`, `B.BIG`, `B.ViewOf`, `B.View` (`cubs[id].bd/sz`), `B.CFG` (`tagBigK`, `marker*`), `B.ApplySize`, `B.DistXY`, `B.Log`/`B.ErrEvery`
und die B1b-B1d-Liste (PB1D 6.9); Bench zusaetzlich (nur SP) `B.BodyWant`, `B.BodyNow`, `B.BodySwapReady`, `B.Reg`, `B._s`, `B.FindAnimal`,
`B.GrowSetG`, `B.BrainTick`.

---

## 7. Tests

### 7.1 KERN-Attrappe (`attrappe/b1e_kern/run.lua`, neu; `kern/`, `b1b_kern/`, `b1c_kern/`, `b1d_kern/`, `gesamt/` bleiben gruen -- gewollt
geaendert und im Bericht einzeln begruendet: `b1d_kern` 8 "bodySwap = true -> Fehlerzeile" entfaellt, Sicht-Feld `bd`, `MARK_FIELDS` + body)
Tier-Attrappe: zwei Arten (`getDef("ncbeargrown")` mit Rasse brown; abschaltbar), `getSquare`, `faceThisObject` (Zaehler), Welt-Liste fuer
"wie viele Tiere eines Eintrags leben".
1. **Helfer:** `B.BodyKind` fuer ncbearcub / ncbeargrown / bear / bearstag / ncbearcubalt / nil -> cub / big / nil / nil / nil / nil.
2. **Schwelle:** body nil s 0,74 -> cub; s 0,75 -> big; body big s 0,72 -> big; s 0,699 -> cub; body cub s 0,72 -> cub; `st` shy/fed -> cub;
   `bodySwap = false` -> cub.
3. **Groesse:** cub s 0,8 -> 0,75; big s 0,75 -> 0,72; 1,0 -> 0,982 (Gleitkomma: 0,9825 rundet auf 0,982, Vergleich mit 0,001 Spiel); 1,35 -> 1,35; big s 0,71 -> 0,72; streng steigend in 1000 Schritten
   ueber [0,75, 1,35]; D 100: Tag 14 cub 0,723, Tag 15 big 0,720, Tag 100 1,35; D 50: Tag 7,5 big.
4. **Tausch hin:** zahm, Folgen, g 0,15, sicher -> genau ein `addAnimal` mit Art `ncbeargrown`, DANACH `remove()` am alten (Reihenfolge), am Ende
   genau EIN lebender Koerper des Eintrags; `id`/`u`/`owner`/`name`/`mode`/`hx..`/`tame`/`g`/`x*`/`hp` gleich; `gen + 1`, `r + 1`, `aid` neu,
   `body = big`; neuer Koerper `setSizeForced(0.72)`, `setHealth(rec.hp)`; Spiegel `body = big`, `gen` neu; `s.swapAt` gesetzt; eine `B.Log`-Zeile;
   keine `B.Tell`.
5. **Nicht sicher:** `calmUntil > ms` / `s.g.on` / Zombie bei 5 Kacheln / `busyUntil > ms` / Abklingzeit -> kein Tausch, Junges bleibt bei 0,75;
   danach (Uhr weiter) -> Tausch; Uhr rueckwaerts -> gilt als abgelaufen.
6. **Kein Flackern:** g pendelt 1000 Takte um 0,15 +- 0,002 -> genau 1 Tausch; `B.GrowSetG(rec, 0)` + Takt -> zurueck (cub, 0,35), auch innerhalb
   `swapMinMs` (von Hand); `B.GrowSetG` auf s 0,72 -> bleibt gross bei 0,72.
7. **Definition fehlt:** `getDef("ncbeargrown")` nil -> kein Tausch, `ErrEvery` hoechstens 1 je 10 min, Junges `setSizeForced(0.75)`; Aussteigen mit
   s 0,9 -> Junges-Koerper + "placebig"-Zeile; mit Definition -> grosser Koerper.
8. **Kachel:** eigene Kachel frei -> gleiche Kachel; eigene gesperrt -> Ring; keine -> kein Tausch, `swapTryAt`, nach 6 Fehlversuchen Fehlerzeile je Minute.
9. **Offener Schaden:** alter Koerper Leben 0,5 bei `hpB` 0,6 -> vor dem Tausch `rec.hp` - 0,1; neuer Koerper `setHealth(0.5)`, nie 1,0.
10. **Mitfahren/Call:** Einsteigen bei s 0,74 (cub), 2 Spieltage Fahrt (s 0,80), Aussteigen -> grosser Koerper, kein Junges; Call to me bei
    `want big`/`have cub` -> neuer grosser, alter Junges entfernt, ein Koerper; Tod-im-Auto ebenso.
11. **Speichern/Laden:** `A.load` -> `body` bleibt; grosser Koerper gleicher `gen` gebunden, `body big`, kein Tausch; B1d-Eintrag ohne `body` mit
    Junges bei g 0,3 -> beim Binden `body cub`, erster `GrowLive` tauscht.
12. **Absturz-Faelle 4.3** (alle sechs Zeilen) -> je genau ein gebundener Koerper bzw. erwartetes nil; Kopien nur unbeobachtet entfernt.
13. **Suchlauf:** sieht beide Arten, bindet `big`, entfernt `big`-Waise nach den Riegeln, faesst `bear`/`bearstag`/`ncbearcubalt` nie an;
    `B.RemoveCub(bearTier)` tut nichts.
14. **RecOf:** grosser Koerper ohne Eintrag und ohne Spiegel -> nil "kind" (kein NewRec); Junges ohne Spiegel -> "found" wie B1a.
15. **Regeln:** `FollowDecide` mit `c.gap 0,5`: halten bis 3,5, losrennen ab 5,0, Ziel 2,5 vor dem Besitzer, Gehen bis Besitzer-Tempo 0,67;
    `c.gap` fehlt -> B1c-Zahlen; `GuardDecide` mit `c.gap 0,5` -> Versteck 2,0 hinter dem Besitzer.
16. **Tempo:** `B.MoveTo` gross rennend 10 Kacheln -> `ownUntil = ms + 10 / 3,17 s + 1,5 s`; Junges wie B1c; Kondition-Sprungdeckel gross mit 3,17.
17. **Sicht:** zahm big -> `bd = "big"`, `sz` des vorhandenen Koerpers (Junges wartend bei s 0,8 -> `bd cub`, `sz 0.75`); wild -> kein `bd`.
18. **Noten:** `SetMode` follow bei big -> `{ k = Note_Follow, bd = "big" }`; bei cub ohne `bd`; Ride/Call/Rename ebenso; `Note_Grown` ohne `bd`.
19. **Beschaeftigt:** Fuetter-Aktion `serverStart` -> 20 s kein Tausch; `complete` -> sofort frei; Aktion nie beendet -> nach `busyMs` frei.
20. **Streicheln:** Sicht `bd big`, `sz 1.035` -> Haltung "cow", `AnimalSizeY` 0,5; Junges -> "lamb", 0,5; kein `getData`-Aufruf.
21. **MP-Rundlauf:** Server + Client A (Besitzer) + Client B: Tausch nur am Server; Sichten von A und B tragen `bd big` + neue OnlineID; B kann nicht
    fuettern; A offline -> `g` steht, kein Tausch (ausser B1d-Fall); kein `sendClientCommand` neu.
22. **Dateien:** `B.CreateCub(` nur in `B.AppearFor`/`B.PlaceCub`; `addAnimal`/`addToWorld` nur in `B.CreateCub`; `setSizeForced`/`getData` nur in
    `B.ApplySize`; `getHealth`/`setHealth` nur in `B.BodyHp`; kein Vergleich `getAnimalType() == / ~=` ausserhalb `B.BodyKind`; Text `"bear"` nirgends
    als Art; kein `next(`, kein `%a`; LF, ASCII.

### 7.2 OBERFLAECHE-Attrappe (`attrappe/b1e_ober/run.lua`, neu; eigene Kern-Attrappe nach 6.2/6.4; `ober/`, `b1b_ober/`-`b1d_ober/` bleiben gruen)
1. **Menue:** grosser Koerper bekommt Fuettern, Streicheln, Modus, Name ("Name the bear"), Call ("...your bear..."); Art `bear` bekommt nichts.
2. **Hud:** `scan` bindet beide Arten; Schild `bd big`, `sz 1.35` -> Faktor 4,09 (`tagBigK`), Junges 0,75 -> 2,14; Probe (isClient) nur bei passender
   Art, SP nie; Vorgabe-Name "Kevin's bear" bei `bd big`.
3. **Texte:** `U.TB` waehlt Big nur mit `bd big` UND vorhandenem Schluessel; `U.NoteText({ k = Note_Follow, bd = "big" })` -> "Your bear follows you.";
   unbekannter Big-Schluessel -> Grundtext.
4. **Optionen:** `MarkerSize` mit 7 Schluesseln, Vorgabe Index 1, Reihenfolge 6.7; `U.Opt("MarkerSize", 1)`.
5. **Faktor:** `U.MarkerFactor(1080, 1)` 1,0; 1440 -> 1,25; 2054 -> 2,0; 2160 -> 2,0; 3240 -> 3,0; 720 -> 1,0; Index 5 -> 2,0 (gleich welche Hoehe).
6. **Lage (3840 x 2054, Auto):** Element x 1824, y 96, Groesse 90; Scheibe 192 px um die Elementmitte; Pfeil `_arrow192`; Schrift Large; mit gemerkter
   Bandits-Stelle (100, 50) -> dort, geklemmt auf das Bild; mit sichtbarem Bandits-Marker an der Standardstelle -> 200 px nach rechts.
7. **Pfeil:** Ziel genau oestlich (+x) -> Winkel 135; noerdlich (-y) -> 45; Abstand 5 Kacheln -> kein Pfeil, Ring; 20 Kacheln -> Pfeil.
8. **Verhalten:** ohne Bandits -> sichtbar; `new` -> sichtbar; `shy` -> 60 s, dann aus; gezaehmt -> aus; Doppelklick -> aus fuer dieses Junge,
   neues Junges -> wieder an; je Bild <= 4 Bilder + 1 Text, kein `getText`, keine neue Tabelle; Aufloesung geaendert -> neu gelegt; Spielstart ->
   genau ein Element (altes abgemeldet).
9. **Bilder:** 9 Dateien da, Masse exakt, RGBA, <= 288 px, Spitze oben (Alpha-Schwerpunkt ueber der Mitte); Symbol-96er byte-gleich 9e45e936 (6.9).
10. **Texte-Pruefer:** 24 + 1 Schluessel in 7 Sprachen, Platzhalter gleich, CN-Zeichen, Round-Trip, `U.EN` == EN, `%%` in den Prozent-Stufen,
    Optionen-Argumente nur Schluessel.
11. **Bench:** `NCBear_CubStats()` druckt body/want/engine type/swap; `NCBear_CubGrow(15)` -> Zeile "body big (swapped)"; `NCBear_CubClean()` entfernt
    beide Arten, nie `bear`; MP -> "singleplayer only".

### 7.3 GESAMT (`attrappe/gesamt/run.lua` Abschnitt "20 B1e", ZUSAMMENBAU)
Junges zaehmen -> 15 Spieltage Langsam-Takte -> `Note_Grown half` + Tausch (ein Koerper, `ncbeargrown`, 0,72) -> Folgen (Gap 0), Verstecken,
Laerm, Fuettern (Beschaeftigt-Marke), Streicheln ("cow") -> Einsteigen, 1 Tag Fahrt, Aussteigen gross -> Call to me -> Speichern/Laden -> Register
leeren -> Heilung `body big` -> Tag 100 (1,35, Gap 0,5) -> Bench zurueck (Junges 0,35) -> Tod -> Eintrag weg; Markierung mit/ohne Bandits.
Einmal SP, einmal Server + zwei Clients. `xref_b1e.py`: jede `B.*`/`U.*`-Benutzung definiert, Sicht-Feld `bd`, Noten-Feld `bd`, 25 Schluessel
in 7 Sprachen, 9 Bilder, die Big-Schluessel haben je einen Grundschluessel.

### 7.4 Kevins Test im Spiel (nach dem Einbau: Spiel NEU starten -- neue Tierart und Lua laden nur beim Start; `bugwatch.py` mitlaufen lassen;
Wegwerf-Spielstand, `-debug`; Debug-"Tier Cheat" AUS; `NCBear_CubLog(true)`)
Einzelspieler:
1. Spielstand mit gezaehmtem Jungen (sonst `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`). `NCBear_CubStats()`: body cub.
2. `NCBear_CubGrow(15)`: im selben Augenblick wird aus dem Jungen der grosse Baer, etwa gleich gross; "Your bear is half-grown now."; das Schild
   sitzt ueber dem Buckel. `NCBear_CubStats()`: body big, engine type ncbeargrown, Groesse 0,72. **Melden: Sprung zu sehen? Groesse ok (F1)?**
3. "Follow me": gehen und rennen -- **rutschen die Fuesse (F6)?** Steht er zu nah/zu weit hinter dir? Zombie in der Naehe: versteckt er sich hinter
   dir? Schuss/Laerm: rennt er weg? Fuettern und Streicheln (Haltung F4).
4. `NCBear_CubGrow(85)` (Tag 100): ausgewachsen. Daneben `NCBear_SpawnLive()` und den Test-Baeren mit `getData():setSizeForced(1.35)` wie in
   `baer/spiel/anleitung_lebend.md` -- **gleich gross?** Abstand beim Folgen ok?
5. Speichern, Hauptmenue, laden: gleicher grosser Baer, gleiche Groesse.
6. Ins Auto, fahren, aussteigen: grosser Baer steigt aus. "Call to me": grosser Baer neben dir.
7. `NCBear_CubGrow(-100)`: wieder das Junge (0,35).
8. Markierung: `NCBear_CubClean()`, `NCBear_CubHere(12)`: oben in der Mitte die Markierung, bei 4K doppelt so gross. Optionen -> Mods ->
   "NPC Crew: Bear" -> "Size of the cub marker ...": Auto / 100 % ... 300 % ausprobieren. Pfeil zeigt zum Jungen? Doppelklick blendet aus.
   Einmal OHNE Bandits starten: Markierung kommt trotzdem (F11).
9. Alter Spielstand von heute (Junges nach Tag 15 im Junges-Modell): wird nach dem Laden zum grossen Baeren.
Mehrspieler (dedizierter Server, Rolle user, A und B; Sandbox "Bear: days until fully grown" = 10, kurze Tageslaenge):
1. Server startet ohne Fehler, beide verbinden, kein Kick. 2. A zaehmt, nach ~1,5 Spieltagen Tausch: A und B sehen EINEN Baeren, keinen
doppelten. 3. B kommt spaeter: sieht den grossen Baeren in richtiger Groesse. 4. A ab- und anmelden: Baer gross. 5. A faehrt mit, steigt aus: gross.
6. Server-Log nach `[TC-BEAR] ***` durchsehen.

---

## 8. Belege: jeder geplante Engine-Aufruf (der Bauer liest die Stelle selbst nach und nennt sie im Kommentar)
| Nr | Aufruf | Beleg (gleiche Argumenttypen) | Seite | Wer |
|---|---|---|---|---|
| 1 | `animal:getAnimalType()` | `V:client/ISUI/Animal/ISAnimalUI.lua:65`; `V:shared/Definitions/animal/ButcheringUtil.lua:13` | beide | KERN (`B.BodyKind`) |
| 2 | `AnimalDefinitions.getDef(Text):getBreedByName(Text)` | `V:server/ClientCommands.lua:808`; `ButcheringUtil.lua:79/85` | Schreiber | KERN |
| 3 | `addAnimal(getCell(), x, y, z, Art-Text, Rasse, false)` + `animal:addToWorld()` | `V:server/ClientCommands.lua:809-810`; `V:client/DebugUIs/DebugContextMenu.lua:1460-1467` (wie B1a, nur anderer Artname) | Schreiber | KERN (`B.CreateCub`) |
| 4 | `animal:remove()`, `removeAnimal(animal:getOnlineID())`, `getBehavior():setBlockMovement(false)` | wie B1a/B1c (`B.RemoveCub`, `ButcheringUtil.lua:609`, `:612-614`) | Schreiber | KERN, unveraendert |
| 5 | `animal:getSquare()` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:5` | Schreiber | KERN (`B.SwapSpot`) |
| 6 | `animal:faceThisObject(Spieler)` | `V:shared/TimedActions/Animals/ISPetAnimal.lua:17` (Tier -> Spielfigur) | SP belegt; am MP-Server Wirkung ungeprueft (nur Optik) | KERN (`B.BodySwap`) |
| 7 | `getData():setSizeForced`, `getHealth`, `setHealth`, `getX/getY/getZ`, `isExistInTheWorld`, `isDead`, `getModData`, `getAnimalID` | wie B1d/B1c (PB1D 8 Nr. 1-5, PB1C 8) | wie dort | KERN, unveraendert |
| 8 | `character:setVariable("animal", Text)`, `("AnimalSizeY", Zahl)` | `ISPetAnimal.lua:26-39` (wie B1a, Wert "cow" statt "lamb") | Client/SP | KERN (PetAction) |
| 9 | `X = ISUIElement:derive(Text)`, `ISUIElement.new(self, x, y, w, h)` | `V:client/Chat/ISAlert.lua:3`; `B:client/BanditEventMarkers.lua` `new` (`ISUIElement:new(screenX, screenY, 1, 1)`) | Client | OBERFLAECHE |
| 10 | `:initialise()`, `:addToUIManager()`, `:removeFromUIManager()`, `:setVisible(b)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:517-518`; `V:client/ISUI/Maps/ISMap.lua:116`; `V:client/ISUI/ISCollapsableWindow.lua:70` | Client | OBERFLAECHE |
| 11 | `:setX/:setY/:setWidth/:setHeight(Zahl)` | `V:client/ISUI/ISToolTip.lua:78-79`, `:173-174` | Client | OBERFLAECHE |
| 12 | `self:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | `V:client/Chat/ISChat.lua:418`; `V:client/DebugUIs/ISSpawnVehicleUI.lua:171` | Client | OBERFLAECHE |
| 13 | `self:DrawTextureAngle(tex, cx, cy, winkel)` | `V:client/Fishing/TensionUI.lua:21`; `V:client/ISUI/Fireplace/ISKnob.lua:24`; `B:client/BanditEventMarkers.lua` render | Client | OBERFLAECHE (zeichnet in Bildgroesse, NUR JAR FE 8 -> Bild je Stufe) |
| 14 | `self:drawTextCentre(text, x, y, r, g, b, a, UIFont.Small/Medium/Large)` | `B:client/BanditEventMarkers.lua:176` (Small); `V:client/DebugUIs/StashDebug.lua:86` (Medium); `V:client/Chat/ISAlert.lua:35` (Large) | Client | OBERFLAECHE |
| 15 | `getTexture("media/ui/<datei>.png")` | `V:client/Chat/ISChat.lua:921` | Client | OBERFLAECHE |
| 16 | `getCore():getScreenWidth()`, `getCore():getScreenHeight()` | `V:client/Challenge/WinterIsComing.lua:18`; `V:client/Chat/ISChat.lua:1167` | Client | OBERFLAECHE |
| 17 | `Events.OnResolutionChange.Add(function(oldw, oldh, neww, newh) ... end)` | `V:client/ISUI/PlayerData/ISPlayerData.lua:185`, `:206` | Client | OBERFLAECHE |
| 18 | `function X:onMouseDoubleClick(x, y)` | `V:client/ISUI/ISButton.lua:66`; `B:client/BanditEventMarkers.lua:19-21` | Client | OBERFLAECHE |
| 19 | `getSpecificPlayer(0)`, `player:getX()/getY()`, `player:isDead()` | `V:client/Farming/CFarmingSystem.lua:45`; `V:client/Fishing/TensionUI.lua:11`; `V:client/Context/ISMenuContextWorld.lua:37` (wie heute `S:client/ISUI/BanditsNPCBearMarker.lua:176`, `:203`) | Client | OBERFLAECHE |
| 20 | `player:getModData()["BanditEventMarkerPlacement"]` (nur lesen) | `B:client/BanditEventMarkerHandler.lua:17` | Client | OBERFLAECHE |
| 21 | Bandits-Marker lesen: `.markers`, `m.x/.y`, `m:getDuration()`, `m:getIsVisible()` | heute `S:client/ISUI/BanditsNPCBearMarker.lua:128-144`; `V:client/ISUI/ISUIElement.lua:676` | Client | OBERFLAECHE |
| 22 | `math.atan2`, `math.floor/abs/min/max/sqrt`, `%` | Lua; `math.atan2` in `V:client/ISUI/Fireplace/ISKnob.lua:137` | beide | beide |
| 23 | `PZAPI.ModOptions` `addComboBox`/`addItem`/`getValue` | `V:client/PZAPI/ModOptions.lua:121`, `:131-137`; NC gespielt `NC:client/BanditsNPCModOptions.lua:97-103` (wie B1d) | Client | OBERFLAECHE |
| 24 | `getTimestampMs()`, `Events.OnTick/OnGameStart.Add` | `V:client/Foraging/ISBaseIcon.lua:485`; `V:client/Chat/ISChat.lua:943`, `:1186` | Client | OBERFLAECHE |
**Jar-only-Aufrufe in B1e: keine.** Kevins zwei Ausnahmen (`pathToLocation`, `setVariable("animalRunning", ...)`) bleiben unveraendert nur in
`B.MoveTo`. **Nicht benutzt:** `drawTextureAllPoint` (stufenloser Pfeil, ohne Vanilla-Aufrufer -> F8), `drawTextZoomed`, `setSize`, Engine-Alter,
`BanditEventMarkerHandler.set` (B1e ruft Bandits nicht mehr), `getForwardDirection`/`setDir` am Tier (unbelegt), `getData` ausserhalb `B.ApplySize`.

---

## 9. Leistung (Ergaenzung zu PB1D 9)
| Was | Wie oft | Deckel |
|---|---|---|
| Koerper-Frage am Schreiber | je Hirn-Takt und geladenem zahmem Jungen 1 `getAnimalType` (+ Lua-Rechnung) | Eintraege 64, praktisch `BearMaxPerPlayer` |
| Tausch | selten: hoechstens je `swapMinMs` je Eintrag; Fehlversuch je `swapRetryMs` | ein Koerper je Eintrag |
| Beschaeftigt-Marke | je Aktions-Start/-Ende 1 Schleife ueber <= 64 Sitzungen | - |
| Markierung | je Bild 4 Bilder + 1 Text (nur sichtbar); je 400 ms Ziel/Winkel (2 Spieler-Getter + Lua); Option 1 s Zwischenspeicher | 1 Element |
| Client-Probe | wie B1d + 1 `getAnimalType` | `viewMax` 16 |

---

## 10. Fuer den ZUSAMMENBAU
1. **Altes Junges ins Staging:** `_arbeit/baer_baby/entwurf/NCBearCub.glb` (6c3f0a96) und `NCBearCub.png` (2ee25f24) nach
   `mod/42/media/models_X/Skinned/` bzw. `mod/42/media/textures/Body/`, MD5 nachweisen (= Test-Mod seit 96035c3). `staging_dateien.txt` neu
   (9 neue Bilder, geaenderte MD5; Bench als Testhilfe).
2. `attrappe/gesamt/run.lua` Abschnitt "20 B1e" (7.3), beide Bauer-Attrappen gegen die echten Dateien, `xref_b1e.py`.
3. `baer/tools/baer_uebernahme.py`: `TEXT_NS["IG_UI.json"]` += `IGUI_AnimalType_ncbeargrown`; Defs-Pruefung (`:1121-1132`): `bodyModel
   "NCBear_Body"` und Rassen-Textur `"NCBear"` der Art `ncbeargrown` als **erlaubte Fundstelle bis B5a** (wie ALT_EXPECTED: ohne `--vor-b5a`
   absichtlich rot, mit nur Warnung) -- NICHT `NCBear.glb`/`nc_bear_tier.txt` jetzt mitkopieren (Hirsch-Rueckfall `NCBearStag_Body`); TIER_RULES
   unveraendert gruen (Tausch geht ueber `B.PlaceCub`); neue Bilder ueber `UI_ASSET`; Pruefung "kein `getAnimalType() ==`/`~=` ausserhalb
   `B.BodyKind`" als neue Regel. Trockenlauf mit `--vor-b5a`, Probe nur unter `_arbeit/baer_zaehmen/probe_b1e/`.
4. `baer/NAEHTE.md`: Zeile 3 (`AnimalAvatarDefinition`) + `ncbeargrown`; Zeile Markierung: kein Bandits-Aufruf mehr (nur Lesen: Ueberdeckung, gemerkte
   Stelle), laeuft ohne Bandits; neue Notiz **B5a**: endgueltiges Modell-Skript des grossen Baeren ohne Hirsch-Rueckfall, dann `bodyModel` der Art
   `ncbeargrown` nachziehen (der ARTNAME bleibt), Kampf/Stimmen fuer `ncbeargrown` (NCBearFight kennt nur `bear`).
5. `mod_info_vorschlag.txt` um B1e (ab Tag 15 grosser Baer, waechst bis 1,35; Markierung skaliert).
6. Einbau in NCBearTest nur, wenn Kevin nicht spielt; vorher/nachher sichern; Kevin muss das Spiel neu starten.

---

## 11. Fragen fuer Kevin (er testet gerade -- jede mit Empfehlung; gebaut wird die Empfehlung)
| # | Frage | Empfehlung |
|---|---|---|
| F1 | Groesse beim Wechsel: 0,72 (wirkt gleich gross wie das Junge, gemessen) oder woertlich 0,75 (+5 % laenger, +6 % hoeher)? | 0,72; am Ende genau 1,35 |
| F2 | Name der neuen Art `ncbeargrown` (fuer immer im Spielstand), Name im Spiel "Bear"? | ja |
| F3 | Nach dem Wechsel sagen Schild und Meldungen "bear" statt "cub" ("Kevin's bear", "Your bear follows you.")? | ja (so gebaut) |
| F4 | Streicheln am grossen Baeren mit der Kuh-Haltung (steht mehr, mit Groesse gemischt) statt der Lamm-Haltung? | ja, im Spiel ansehen |
| F5 | Beim Wechsel schaut der neue Koerper zu dir (die alte Blickrichtung laesst sich mit Belegen nicht uebertragen)? | ja |
| F6 | Fussgleiten: nach dem Wechsel -28 %, um Tag 47 null, bei 1,35 +35 % ("Tretmuehle"). So lassen, bis ein eigener Geh-Knoten kommt? | ansehen, dann entscheiden |
| F7 | Markierung ziehbar (Stelle merken) wie bei Bandits? Heute: nur Doppelklick blendet aus. | erst auf Wunsch |
| F8 | Groessen-Stufen Auto + 100/125/150/200/250/300 %? Stufenlos ginge nur mit deinem Wort fuer `drawTextureAllPoint` (kein Vanilla-Aufrufer). | Stufen |
| F9 | Uebernahme: das grosse Modell geht erst mit B5a (eigenes Modell-Skript ohne Hirsch-Rueckfall) nach NPC Crew? | ja |
| F10 | Kollision des grossen Koerpers 0,30 (0,22 beim Wechsel, 0,41 ausgewachsen)? | im Spiel ansehen |
| F11 | Die Markierung kommt jetzt auch OHNE Bandits (du hattest danach gefragt). Ok? | ja |
| F12 | Der Wechsel passiert vor deinen Augen (im Mehrspieler evtl. ein Bild lang zwei Koerper im Netz). Ok? | ja |
| F13 | Zwischen innerer Groesse 0,70 und 0,75 bleibt der Koerper, wie er ist (kein Hin und Her). Ok? | ja |
| F14 | Versteckt sich der grosse Halbstarke weiter hinter dir bei Zombies, bis der Kampf (B5a) kommt? | ja |

## 12. Offen / ungeprueft (Testpunkte)
`setSizeForced` direkt nach `addToWorld` (mit `minSize` 0,72 unkritisch); ob `isFree(false)` auf der eigenen Kachel eines Tiers falsch ist (dann
Ersatzkachel daneben); `faceThisObject` am Tier am MP-Server; Reihenfolge `addAnimal`/`removeAnimal` bei MP-Clients; Fussgleiten, Abstaende,
Kollision, Schild-Faktor, Kuh-Haltung; Pfeil-Ausrichtung des eigenen Bildes mit der Bandits-Konvention (`markerAngleAdd` per `NCBear_CubSet`
stellbar); ob ein UI-Element ohne eigenes `onMouseDown` den Doppelklick bekommt und Klicks darunter nicht schluckt (Bandits' Element tut es
genauso, 45 x f px); Lesbarkeit von Small/Medium/Large bei Kevins Schriftgroesse; Aufloesungswechsel im Spiel; getAnimalID/getObjectListForLua
am MP-Server (A3, offen seit B1a).

Statisch geplant, nichts gebaut, nichts gespielt.


## 13. Nachbesserung B1e (11.11.2026 abends, `nachbesserung_b1e.md`)
- **B1** "Call to me" im selben Bild wie ein Tausch (oder Aussteigen) tut nichts (still), bis der eben erzeugte Koerper in der Welt ist
  (`s.placedAt` aus `B.PlaceCub`, hoechstens `callFreshMs` 2000) -- kein dritter Koerper mehr.
- **B2** Neue Sperre "move" in `B.BodySwapReady`: eigener Rennbefehl laeuft (`s.walk == false`, `ms < s.ownUntil`) -> warten, hoechstens
  `swapMoveMaxMs` 10000 seit dem ersten Takt mit want ~= have (`s.swapWantAt`, setzt `B.GrowLive`); Gehen sperrt nicht.
- **A2** `faceThisObject` am neuen Koerper nur im Einzelspieler. **B4** `ncbeargrown.feedByHandAnim = "AnimalLureHigh"`.
- **B5** Laerm-Ersatzweg "follow" (`B.CalmAnswer`) mit Koerperlaenge wie `B.FollowDecide`; das Heranlocken mit Futter (Regel 6,
  `comeFed` 2) bleibt OHNE Zuschlag: mit + gap stuende der Baer bis 2,5 Kacheln weg und Fuettern (`reach` 3, Kachel-Abstand) koennte
  "zu weit" melden.
- **A3/A4/A6/B3** Code-Form und Text: Mehrfachrueckgabe in Locals, Kommentar-Zahlen (0,21; x MotionScale 1,6), Fundstelle `square:getX()`.
- Nicht geaendert (Fragen): A1/B6 (Rest-Texte "cub"), A5 (288er Bilder), B7 (Klickflaeche der Markierung).
