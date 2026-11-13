# Lauf baer-f4 -- GEGENPRUEFER (nach der Nachbesserung)

Stand 13.11.2026 spaet, Rolle GEGENPRUEFER. **Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und keinem Bericht geglaubt: jede Zahl
unten stammt aus einem eigenen Lauf, jede Code-Aussage aus eigenem Lesen. Geschrieben nur in `f4/GEGEN.md` (dieser Bericht),
`f4/anleitung_entwurf.md` (berichtigt), `f4/bild_gegen/` (eigene Bild-Kette), `f4/gegen_javap/` und `f4/jar/` (gezogene Klassen, nur gelesen),
`f4/probe_gegen/` (Uebernahme-Probe) und `attrappe/f4_gegen/` (eigene Attrappe, Ausgaben). Kein Byte in Staging, Test-Mod, NPC Crew, Vanilla,
Bandits, `baer/`; kein git, kein Download, kein Spielstart.
Kuerzel: `S:` = `mod_f4/42/media/lua/`, `V:`/`B:` = Vanilla / Bandits 42.22 `media/lua/`, `NC:` = NPC Crew `42/media/lua/`, `NCC` = NPC Crews
`CLAUDE.md`, `G:` = `attrappe/f4_gegen/`, `J:` = `f4/gegen_javap/` bzw. `f4/plan_werkzeug/` (javap -c -p, Jar 42.22).

## 0. Urteil zuerst

**Bereit fuer Kevins Einzelspieler-Test: JA.** Alle 6 major-Befunde sind fuer den Einzelspieler geschlossen (C5 und der MP-Teil von C4 sind
Kevins Entscheidung und betreffen nur den Mehrspieler). Keine neue Verlust- oder Verdopplungs-Stelle im normalen Spiel gefunden; meine drei
Stichproben halten die Zaehl-Invariante je Gegenstand UND je Feld (31 bestanden, 0 Fehler). Neu von mir: 2 kleine Befunde (G-A Bedienung, G-B Form
der Jar-Ausnahme), 1 Berichtigung am Rest T10 (beide Richtungen, Fenster laut Jar etwa 1 s), 3 Hinweise. Nichts davon blockiert den SP-Test.

## 1. Befunde einzeln (am Code nachgeprueft)

| ID | geschlossen? | eigener Beleg |
|---|---|---|
| C1 | **ja** | `baer/tools/baer_uebernahme.py:716-718` (PZ_ALLOWED Put/Take). Eigener Trockenlauf + `--probe f4/probe_gegen`: **0 Fehler, 2 Warnungen** (`G:ue_trocken.txt`, `G:ue_probe.txt:365`), luacheck_pz "0 Treffer, 17 erlaubt", Bench `NCBearBenchInv.lua` "wird nie kopiert" (`G:ue_probe.txt:171`) |
| C2 | **ja** | `attrappe/f4_ober/run.lua:136` (`bagAdd = 150`), `:224-225` (`BAG == 150`); eigener Lauf 172/0 und 174/0 (`G:ober_mock.txt`, `G:ober_kern.txt`). Rueckfaelle 150: `S:client/BanditsNPCBearWinData.lua:151/:153`, `S:client/ISUI/BanditsNPCBearInvWindow.lua:97/:404`, `S:client/BanditsNPCBearInvClient.lua:530`, `S:client/BanditsNPCBearMenu.lua:542`; `grep "+50"` im Staging: nur Kommentare "+bagAdd" |
| C3 | **ja** | Abgleich VOR jeder Aenderung: Geben/Nehmen `K.check` -> `B.InvHeal` (`S:server/BanditsNPCBearInv.lua:487`), F5 `:956` / `:973`, Fressen `:1002`, Tod `:778`, Netz `:248`. `K.healFirst` `:225-230` haengt NICHT mehr am Hirn-Takt. Keine weitere Schreibstelle an `rec.inv`/`rec.bag` ausser Abgleich und Probe-Datei (KERN-Attrappe "Dateiregeln" gruen). Attrappe N1-N3 selbst gelaufen: 41/0 (`G:nach.txt`) |
| C4 | **ja (SP)**, MP = Frage | Modul look `S:shared/BanditsNPCBearInvRules.lua:643` (Lesen im MP abgelehnt, auch die Client-Probe), `:676` (Bauen im MP nicht), Schalter `S:shared/BanditsNPCBear.lua:312`. Gegen NCC:444-447 gelesen ("nie auf dem dedizierten Server", "kein setHue in ... Server-Muenze"). Packtaschen sind `base:normal` ohne Aussehen (`42/media/scripts/nc_bear_packs.txt:19`) -> im MP weiter anlegbar |
| C5 | **offen (nur MP)** | Kein Code moeglich ohne Kevins Wahl; benannt in Anleitung, mod.info-Vorschlag, `baer/NAEHTE.md` Zeile 46/46b. Blockiert den SP-Test nicht |
| C6 | **ja** | `S:server/BanditsNPCBearInv.lua:463-469` (nur der erste lokale Spieler gibt/nimmt), `B.InvHeal` `:321-323` |
| C7 | **ja** | `K.bump` `:235-240`, gerufen VOR dem ersten AddItem `:702`, Taschen `:674-678` |
| C8 | benannt (Rest) | nur Mahlzeit doppelt, nie ein Gegenstand (`f4/attrappe/f4_pruef` P7 weiter "Befund", wie vom Nachbesserer gesagt) |
| C9 | **ja** | `S:shared/BanditsNPCBearInvRules.lua:165-176`, Geben `:455`/`:465`, Bauen `:518`/`:522-524` (nur auf ein Stueck OHNE Liste, wie `NC:shared/BanditsNPC.lua:4993`) |
| C10 | **ja** | selbst nachgelesen: `B:shared/BanditUtils.lua:199` `item:setHole(bodyPart.name)` -- `item` = ItemVisual aus `getItemVisuals()` (:186-188), `bodyPart.name` = `BloodBodyPartType.*` (:150-156): gleiche Argument-Art wie `S:...InvRules.lua:596`; `V:shared/TimedActions/ISPadlockAction.lua:30/:43`, `V:client/DebugUIs/AdminContextMenu.lua:152` passen |
| C11 | **ja** | eigener Lauf aller alten Attrappen gegen Test-Mod UND Staging (`G:alte_vorher.txt`, `G:alte_nach.txt`): Unterschiede nur die gewollten (f3_kern 13->14 Optionen, f1_ober "Load", b1e_ober mehr ok); **F4-Kopien f3_kern_run_f4 274/0**, f1_ober_*_f4 = Stand der Test-Mod |
| C12 | **ja** | `B.InvTakeKg` `S:server/BanditsNPCBearInv.lua:631-651`, `S:shared/TimedActions/BanditsNPCBearTakeAction.lua:127-135`. Ob der MP-Server seine Dauer gegen die des Clients abgleicht: ungeprueft |
| C13 | benannt (F6) | unveraendert, nur MP-Last |
| C14 | durch C4 | im MP liest der Server bei Stuecken mit Aussehen nichts (`:643` vor `:649`) |
| C15 | **ja** | `:696-697` |
| P1 | **ja** | `f4/bilder/KEVIN_*.png` 22:06 neu; `KEVIN_inventar_1080.png` selbst angesehen. Eigenes Bild (Abschnitt 4) zeigt "Packtaschen: an (+150 kg)", "180.0 / 250 kg" |
| P2-P12 | **ja** | Stichproben am Code: P3 `...InvWindow.lua:289`, P5 `:247-256`, P7 `:401`, P8 `...InvClient.lua:374-378`, P9 `:393-398` + `...InvWindow.lua:369`, P12 `...InvClient.lua:37` |

**Kaputt gemacht?** Nein gefunden. Pruefer und Attrappen gruen wie berichtet; die zwei "Fehler" der Pruefer-Attrappe (`G:pruef.txt:35`, `:42`)
sind die gewollten Aenderungen C6/C15.

## 2. Kevins Antworten 1-6 am Code

1. Alles tragen: `B.InvRead` `S:shared/BanditsNPCBearInvRules.lua:813-836` + Feld-Module `:218-780`; abgelehnt nur mit Grund (Leiche, Tier, Radio,
   Karte, beschriebenes/gesperrtes Notizbuch, volle Tasche, Mischung, Flicken, ModData > 2 KB; im MP Kleidung/Taschen). Reparatur-Zaehler
   reist nicht und laesst sich ohne Jar nicht einmal erkennen (benannt, Frage). 1b: `invMaxItems = 1000` (`S:shared/BanditsNPCBear.lua:301`),
   Stueck je Stapel gezaehlt (`B.InvSum`), Seiten 100 Zeilen + 200 KB (`K.sendList` `:848-868`), Paketpuffer 1.000.000 Byte (`f4/GATES.md` G5).
2. Ansehen ueberall: `B.HandleInvList` `:889-903` ohne Abstand; geben/nehmen `B.CFG.reach = 3` (`S:shared/BanditsNPCBear.lua:112`) ueber
   `handCheck` `S:server/BanditsNPCBearServer.lua:166-186`; mitfahrend/Spieler im Auto abgelehnt `:470-477`.
3. Tod: `B.Close` -> `B.InvDrop` `S:server/BanditsNPCBearRegistry.lua:544` VOR `reg.cubs[id] = nil` (:548), Packtaschen mit (`K.dropAll` `:745`).
4. Packtaschen: `nc_bear_packs.txt` (Schneidern 3, 4 Jute/Stoff, 4 Lederstreifen, 2 Seil, 4 Faden, Schere + Nadel bleiben; alle Zutaten in
   Vanilla vorhanden, Form wie `VS:generated/recipes/recipes_tailoring.txt:85-116`), Icon/Bodenmodell nur Verweis (`VS:generated/items/container.txt:5228/:5242`),
   ab halbstark `K.half` (selbst nachgerechnet: Wachstumstag 15 = innere Groesse 0,750 -> halbstark, Last 40 / mit Taschen 190), +150 `bagAdd`.
5. `BearCarryPercent` 50-250, Vorgabe 100, 14 Optionen (`42/media/sandbox-options.txt:62`), wirkt nur auf die Grundlast (`B.InvCapOf` `:880-885`).
6. Fressen: ab `needHungry` 50 (`B.InvEatStep` `:997`), nur `fc` (Baerenfutter), nie verdorben (`B.InvFresh ~= 2`) und nie verbrannt, Lieblingsfutter
   zuerst (`RANK` `:990`, `:1012-1015`), nicht schlafend/liegend, kaempfend, mitfahrend, am Boden (`:993`, `:1001`, `:1004-1005`).
Ohne Frage: nicht langsamer (kein Tempo-Aufruf im Inventar-Code), nur der Besitzer (`:456`), kein Wecken (Put/Take ohne Weck-Aufruf).

## 3. Drei eigene Stichproben (Zaehl-Invariante je Gegenstand UND je Feld) -- `G:gegen.lua`, Ergebnis `G:gegen_ergebnis.txt`: **31 bestanden, 0 Fehler**

- **G1 Absturz nach Geben (SP):** 10 Stuecke jeder Art (Naegel-Stapel, Apfel mit Alter, Axt mit Schaerfe, Hemd, Wasserflasche, Schluessel mit
  Nummer, leere Tasche, Pistole). Register und Spieler zu verschiedenen Zeiten gespeichert: Register alt / Spieler mitten drin, Register alt /
  Spieler neu, Register NEU / Spieler alt, beide alt, zweimal hintereinander abgestuerzt -- in jedem Fall Spieler + Baer = Wahrheit des
  Spieler-Stands, je Feld. (Hinweis: meine erste Fassung zeigte 4 "Fehler" -- das war meine eigene Uhr: die Attrappe stellt beim Neuladen die
  Weltzeit zurueck, die Volkszaehlung rechnet das Essens-Alter hoch. Im Code klemmt `B.InvAgeNow` `S:...InvRules.lua:925` eine zurueckgestellte
  Uhr, das Alter sinkt nie.)
- **G2 Tod mit vollem Inventar:** Packtaschen + 900 Naegel + 99 Aepfel + Hammer = 1000 Stueck (101 Saetze); das 1001. abgelehnt und beim Spieler.
  `B.BearDie` -> 1001 Stueck am Boden (1000 + Taschen), Invariante je Feld, Kopie = Grabstein. Absturz danach mit Kachel UND Grabstein
  gespeichert: nichts doppelt. Die zwei T10-Faelle siehe 5.1.
- **G3 Aussehen-Wechsel mit Packtaschen:** `B.HandleLook(look = "gen")` -> neuer Koerper, `rec.inv`/`rec.bag` dieselben Tabellen, Kopie zeigt auf
  dieselbe Tabelle, Invariante je Feld; Absturz direkt danach: gleich; Packtaschen am NEUEN Koerper abnehmen: Invariante haelt.

## 4. Eigenes Fensterbild aus dem echten Code

Kette des Bild-Pruefers kopiert nach `f4/bild_gegen/werkzeug/` (Texte frisch aus dem Staging exportiert, Mitschrift 1x/2x mit echtem Client UND
echtem Kern, 0 Fehlerzeilen, U.EN = EN/UI.json), zwei EIGENE Szenen: ausgewachsen mit Packtaschen und 180 kg (Maus ueber grauem "Abnehmen") und
Junges mit Packtaschen im Gepaeck (Maus ueber grauem "Anlegen"). Gemalt mit Vanillas Schriften und Symbolen ueber Kevins Spielbild:
`f4/bild_gegen/gegen_packs_DE_1080.png` (angesehen), `_EN_1080`, `_DE_4k`, `_EN_4k`. Zu sehen: "Last 180.0 / 250 kg", "Packtaschen: an (+150 kg)",
Tooltip "Nimm zuerst etwas heraus -- ohne die Packtaschen kann dein Baer nicht alles tragen."; rechts "0.4 / 10 kg", "Ein Junges ist zu klein fuer
Packtaschen." Stimmt mit Kern und Texten. (Fussnote des Blatts traegt noch die Unterschrift der kopierten Kette -- nur Beschriftung.)

## 5. Neue Befunde des Gegenpruefers

### 5.1 Berichtigung Rest T10 (Tod + Absturz) -- beide Richtungen, Fenster etwa 1 s (Hinweis, kein Code)
Plan T10 und `baer/NAEHTE.md` 46b nennen nur "Kachel noch nicht geschrieben" bzw. "mitten im Abwurf". Attrappe G2 zeigt beide Richtungen:
**G2b** Kachel gespeichert, Spieler (ohne Grabstein) noch nicht -> **doppelt** (2003 statt 1002 Stueck); **G2c** Grabstein gespeichert, Kachel noch
nicht -> **verloren** (1 statt 1002). Wie gross das Fenster ist, laut Jar (nur gelesen): abgelegte Stuecke markieren ihre Kachel sofort
(`IsoGridSquare.AddWorldInventoryItem` Offset 505 `IsoWorldInventoryObject.addToWorld`, J:`IsoGridSquare.txt:17585`; dort Offset 78
`IsoObject.addToWorld`, J:`IsoWorldInventoryObject.txt:1629`; darin Offset 335-336 `flagForHotSave` ohne Bedingung, J:`plan_werkzeug/IsoObject.txt:11786`);
der Einzelspieler legt markierte Kacheln je **1000 ms** in die Speicher-Schlange (`IsoChunkMap.<init>` Offset 75-85 `UpdateLimit(1000)`,
`updateInternal` Offset 323-429 `AddHotSave`, J:`IsoChunkMap.txt:126-130`, `:548-589`), danach sofort die Spieler (`ChunkSaveWorker.Update` Offset 144-167
`HotsaveAncilliarySystems`, J:`plan_werkzeug/ChunkSaveWorker.txt:110-121`). Also ist das Fenster in beiden Richtungen etwa eine Sekunde (Spieler
alle 10 s dazwischen moeglich) -- ein Absturz genau in dieser Sekunde. Vanilla verliert in derselben Lage ebenso, was gerade auf den Boden fiel.
Vorschlag: in `NAEHTE.md` 46b und Plan T10 "beide Richtungen, ca. 1 s" eintragen; kein Code.

### 5.2 G-A (minor, Bedienung): frisches Essen stapelt im Baeren nie
`B.InvSame` vergleicht ALLE Felder (`S:shared/BanditsNPCBearInvRules.lua:863-873`), Essen traegt Alter `ag` und Weltstunde `at` beim Geben
(`:432-435`); "All" stellt je Stueck eine eigene Zeitaktion an (`S:client/BanditsNPCBearInvClient.lua:449-455`), jede zu einer anderen Weltstunde.
Attrappe G4: 3 gleich alte Aepfel nacheinander -> **3 Saetze** (Dosen, die nie verderben: 1 Satz). Folge: 20 Aepfel = 20 gleich aussehende Zeilen
"Apple" (die Zustands-Marke aus P6 greift nur bei `cp`, Essen hat keins, `S:client/ISUI/BanditsNPCBearInvWindow.lua:323`); zurueck nur Zeile fuer
Zeile, 1000 Aepfel = 100 Seiten; die Daten-Waage der Kopie fuellt sich schneller (ca. 0,4 KB je Essens-Satz). Kein Verlust. Vorschlag: gleich,
wenn das HOCHGERECHNETE Alter (`B.InvAgeNow`) bis auf eine kleine Toleranz gleich ist (dann `ag`/`at` des Satzes behalten), oder Kevin fragen.

### 5.3 G-B (minor, Form der Jar-Ausnahme): Schreibseite ohne Existenz-Riegel
JAR_LISTE.md Abschnitt 0 und NCC:227 / :237 verlangen "jeder [Aufruf] hinter einem Existenz-Riegel"; NPC Crew prueft jeden Setter
(`NC:shared/BanditsNPC.lua:5019` `if item.setBurnt then`, :5021, :5029-5030, :5035-5036). Der Baer prueft die Riegel nur beim GEBEN
(`S:...InvRules.lua:454`, `:464`, `:483-487`, `:644`); beim BAUEN rufen `:519`, `:527`, `:529-540`, `:681` ohne Riegel (nur `setSharpness` `:255` hat einen).
Faellt eine Methode nach einem PZ-Update weg, wirft `B.InvBuild` statt "field food" zu melden: Nehmen lehnt dann nur mit Fehlerzeile ab (nichts
verloren), aber beim **Tod** wirft `K.dropAll` jedes Mal neu, `B.Close` kommt nie bis `reg.cubs[id] = nil` und wiederholt das je Hirn-Takt
(selbst durchgerechnet: schon abgeworfene Saetze stehen auf k = 0 und werden nicht doppelt abgeworfen, `:748`). Heute (42.22) gibt es alle
Methoden -- nur nach einem Update. Vorschlag: je Setter `if item.setX == nil then return false end` (dann Satz bleibt bzw. `invLost`).

### 5.4 Hinweise
- **H1** Die Zeitaktionen drehen den Baeren zum Spieler (`animal:faceThisObject`, `S:shared/TimedActions/BanditsNPCBearPutAction.lua:62-65`, Take
  ebenso) -- auch wenn er schlaeft (hineinlegen weckt nicht). Ob er sich im Liegen dreht: ungeprueft, nur Optik.
- **H2** Daten-Grenze der Kopie 512 KB (`S:shared/BanditsNPCBear.lua:307`) statt der 256 KB aus `f4/GATES.md` G6 -- Kevins Frage 8 in BAU_KERN; die
  Waage zaehlt Text dreifach (`S:...InvRules.lua:98`), ist also vorsichtig.
- **H3** Reparatur-Zaehler: kommt als 0 zurueck (Jar-only, nicht gedeckt) -- das ist ein Wert, der still wechselt, und ausnutzbar (ein oft
  reparierter Gegenstand repariert danach wieder voll). Benannt in BAU_KERN 7 Frage 5; ich ergaenze den Ausnutz-Hinweis fuer Kevin.

## 6. Eigene Laeufe (Ausgaben unter `G:`)

| Pruefung | Ergebnis |
|---|---|
| luacheck / scopecheck / localcount / luacheck_pz auf allen 18 geaenderten bzw. neuen Lua-Dateien | 0 / 0 / hoechstens 51 aktiv, 71 insgesamt (< 180) / 17 x W113 = nur die globalen Aktionsklassen (in der Probe "17 erlaubt") |
| KERN `f4_kern/run.lua` | 229 bestanden, 0 Fehler |
| Nachbesserung `f4_nach/nach.lua` | 41 ok, 0 Fehler |
| Pruefer `f4_pruef/pruef.lua` | 30 ok, 2 "Fehler" = gewollt (C6, C15), 1 Befund = C8 (benannt) |
| OBERFLAECHE `f4_ober/run.lua` | 172/0 (Attrappe), 174/0 (echter Kern) |
| alle alten Attrappen (Test-Mod / Staging) | gleich bis auf die gewollten; F4-Kopien gruen |
| eigene `f4_gegen/gegen.lua` | 31 bestanden, 0 Fehler |
| langcheck (alle acht Sprachen aus dem Staging) | 0 Fehler, 3 Hinweise; `ItemName.json`/`Recipes.json` je acht Sprachen Round-Trip, LF, ohne BOM, Schluessel wie Vanilla (`SewClothSatchel`-Form) |
| Feldpruefer | 0 Luecken |
| Uebernahme Trockenlauf / Probe | je 0 Fehler, 2 Warnungen |
| Kollision (`aussehen/werkzeug/kollision.py`) BearPacks, SewBearPacks, Put/TakeAction, InvRules/InvClient/InvWindow, BearCarryPercent, BanditsNPCBearInv, NCBearBenchInv | je 0 Treffer |
| `staging_dateien_f4.txt` gegen die Platte (MD5, Groesse, Art je Datei) | 183 = 183, **0 Abweichungen**: 24 neu + 28 ueberschreibt = 52 kopieren, 98 gleich, 33 Modell-Dateien NICHT KOPIEREN (28 gleich, 5 GLBs in der Test-Mod neuer, 13.11. 21:00 vom Modell-Lauf). Staging-GLBs tragen Daten vom 11./12.11. -- **keine Modell-Datei im Staging geaendert**. Test-Mod-Lua seit 18:09 unveraendert -> der Einbau ueberschreibt nichts Neueres |
| Zeilenenden | alle geaenderten/neuen Text-Dateien LF ohne BOM, wie in der Test-Mod |

## 7. Jar-Ausnahmen im Staging (nur Jar belegt; jede mit NC-Zeile selbst gelesen)

A3 `getHeadCondition` `S:...InvRules.lua:243` (NC:4539), `getSharpness` `:248` (NC:4538), `setSharpness` `:256` (NC:4587); A4 `addExtraItem` `:519`
(NC:4993), `setSpices` `:527` (NC:5006); A2 `setBurnt` `:529` (NC:5019), `setCooked` `:530` (NC:5021), `setCookingTime` `:531` (NC:5027), `setOffAge`
`:533` (NC:5029), `setOffAgeMax` `:534` (NC:5030), `setFreezingTime` `:538` (NC:5035), `setFrozen` `:540` (NC:5036); A10 `getHue` `:660`, `setHue` `:681`
(NC:client/BanditsNPCInteract.lua:6181 / :6247; NCC:403-447, nur SP und MP-Client -- im MP am Server abgelehnt). Kein weiterer Jar-only-Aufruf
(`grep` ueber alle Staging-Lua ohne Kommentare und ohne Bench); `getTint()` ohne Argument 0 Treffer.

## 8. Fragen fuer Kevin (kurz)
1. Farbton im Mehrspieler: darf der Baer ihn auch am Server lesen/setzen? Bis dahin im MP keine Kleidung und keine Taschen.
2. MP-Absturz: kurzes Welt-Speichern auf deinem Server (z. B. 5 Minuten) -- oder Geben/Nehmen im MP bis F6 aus?
3. Blaettern: Mausrad 1 Seite, Umschalt + Pfeil 10 Seiten -- so lassen?
4. Geteilter Bildschirm: nur Spieler 1 darf hineinlegen/herausnehmen -- ok?
5. Taschen nur leer ("erst ausraeumen") -- ok, oder Inhalt mitnehmen wie NPC Crew?
6. Flicken, Karten, beschriebene Notizbuecher, Radios, Mischungen werden abgelehnt (auch NPC Crew kann sie nicht verlustfrei) -- ok?
7. Reparatur-Zaehler, Langeweile eines Gerichts, Fischgroesse am Boden, befruchtetes Ei gehen beim Baeren verloren (wie NPC Crew); der
   Reparatur-Zaehler steht danach auf 0 (= wieder voll reparierbar) -- so lassen?
8. Frisches Essen stapelt im Baeren nicht (jeder Apfel eine Zeile) -- stapeln, wenn gleich alt?
9. Waisen-Kopien nach einem Absturz (Baer nie gespeichert): als Daten behalten (heute) oder spaeter beim Spieler auf den Boden?
10. Daten-Grenze 512 KB fuer alle Baeren-Kopien eines Spielers -- passt?

Statisch geprueft, nicht gespielt. Nach dem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Spielstart).
