# Baer -- Stand und alles, was ansteht (10.11.2026 11:00)

> **11.11.2026 ~15:00: KONTOWECHSEL -- zuerst `UEBERGABE.md` (neu) lesen.** Kein Workflow laeuft; alle Laeufe sind fertig und eingebaut.


## LIMIT-REGEL (Kevin 11.11.2026 ~11:00, ueber die Projekte-Sitzung: "nen prompt an alle chats ausser blueprint das die beim abgebrochenen wofklow weiter arbeiten ohne verlust")

- Laeuft ein Workflow: warten, nichts doppelt starten.
- Abgebrochen/haengt: TaskStop, dann Workflow({scriptPath, resumeFromRunId}) mit DERSELBEN Lauf-ID -- nie von vorn.
- "Fertig", aber ins Limit gelaufen: `journal.jsonl` im Transkript-Ordner des Laufs lesen; jeder Agent mit null/leerem Ergebnis/Limit-Fehler gilt als
  NICHT gemacht -> seinen Auftrag im Skript leicht aendern (" (Wiederholung nach Limit)") und mit resumeFromRunId neu starten, oder kleiner
  Nachhol-Workflow nur mit den fehlenden Stuecken. Was auf einem leeren Agenten aufbaut, gilt nicht.
- Halb geschriebene Dateien: vor dem Fortsetzen git status/diff bzw. Dateizeiten pruefen; nichts blind uebernehmen, nichts loeschen, nichts Halbes
  in die Test-Mod, nichts Halbes committen. Hier eintragen: welcher Lauf, welche Agenten nachgeholt, was verloren war.
- Wecker (neu 11.11. ~11:00, Cron `d33c868f`) -- am 11.11. ~13:20 auf Kevins Wort GELOESCHT; nichts startet mehr von selbst.
- **Laufende Workflows:** baer-rig-junges `wf_f7896aa7-c7b`, scriptPath `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/rig_junges_workflow.js`
  (Task waly9lt77; Transkript `C:/Users/Kevin/.claude/projects/C--Users-Kevin-NPCCrew-Nebenprojekte-baer/d5933cc7-7f9d-46b2-a3a8-0929595b654b/subagents/workflows/wf_f7896aa7-c7b/journal.jsonl`).
  Fertig und eingebaut: B1c `wf_99d68702-665`, B1d `wf_472ecf82-135` (keine leeren Agenten: je 9/9 mit Ergebnis).
- 11.11. 13:13 nach dem Reset: baer-rig-junges laeuft von selbst weiter (plan/form/skelett/clips/pruef:optik/pruef:technik fertig, alle mit
  Ergebnis; nachbesserung nach dem Limit neu gestartet 13:11) -- nichts nachzuholen. **Woche alle Modelle 93 %** (Reset 14.11. 04:00):
  nach Kevins Regel (bis 98 %, dann anhalten) KEINEN neuen Workflow starten; nur rig-junges zu Ende laufen lassen, Ergebnis ansehen/einbauen.


## Nachtschicht 11.11.2026 (Start 01:55 auf Kevins "los"; Freigaben: ENTSCHEIDUNGEN.md "Nachtschicht 11.11.2026")

Wecker: Cron `70ef11fd` alle 20 min -- am 11.11. ~09:35 auf Kevins Wort GELOESCHT (die beiden laufenden Workflows laufen weiter, nichts startet mehr von selbst). Regeln: max. 10 Agenten je Workflow, vor jedem Workflow hier
Stand + naechster Schritt + Lauf-ID; abgeschnittene Laeufe mit resumeFromRunId fortsetzen; Test-Mod nur bei geschlossenem Spiel.

**Plan (Reihenfolge):**
1. [FERTIG 05:05] Modell-Lauf baer-gen-schoen `wf_ae849387-409`: Gegenpruefer -- grosser Baer E zeigen (sauber, Kevin waehlt Farbe braun/
   Fototon), Junges C noch NICHT (Ohren von hinten Pilze, Kopf in Fotopose gedreht). Blaetter `spiel/gen_KEVIN_junges.png`, `gen_KEVIN_gross.png`
   (nicht in Git), Bericht `spiel/gen_GEGEN_OPTIK.md`, GLB `../_arbeit/baer_gen/aus/C_schoen.glb`, `E_schoen.glb`, `E_schoen_fototon.glb`.
   Claudes Blick: C in Kevins Kamera klar ein Baerenjunges mit Fellstrichen, viel schoener als der Platzhalter; E gut, Gesicht etwas hell.
2. [FERTIG + EINGEBAUT 08:12, UNGESPIELT] Code **B1c** (49 Dateien byte-gleich, 7 neu; Sicherungen `backups/NCBearTest/NCBearTest_vor_b1c_2026-11-11_081208.zip`/`_mit_`; Test `spiel/anleitung_b1c.md`; Berichte `spiel/b1c_*.md`; Pruefer 23/0, gesamt 812/0) -- vorher: Gegenpruefer bereit=True, Blocker=[]. NAECHSTER SCHRITT: Urteil/Restbefunde in
   `../_arbeit/baer_zaehmen/gegen_bericht_b1c.md` lesen, selbst Pruefer+Attrappen laufen lassen, wenn Spiel zu: sichern, Staging nach
   NCBearTest (staging_dateien.txt), mod.info, Commit/Push beider Repos, Testanleitung aus `anleitung_b1c_entwurf.md`. Fragen F1-F9 in
   `forschung_b1c.md` Abschnitt 12 -> 'Fragen fuer Kevin'. Lauf war:  Workflow `wf_99d68702-665` (Task wbyqd4dj0; 9 Agenten, Skript `spiel/b1c_workflow.js`; abgeschnitten -> Workflow({scriptPath, resumeFromRunId: "wf_99d68702-665"})): Register-Selbstheilung N9, Laerm-Flucht des gezaehmten Jungen abfangen,
   Verstecken hinter dem Besitzer bei Zombies / wilde fliehen, Mitfahren wie NPC Crew, Unstuck "Call to me", Bildschirm-Markierung
   (Symbol 1 + Pfeil), Karten-Symbol (Mini + gross), Anzeige-Optionen (Name ein/aus, Groesse), Gehen mit animalRunning=false (Kevins Ja).
   Danach Einbau (wenn Spiel zu), Commit/Push, Testanleitung.
3. [FERTIG + EINGEBAUT 14:39, UNGESPIELT] **Neues Junges aus dem Generator** ersetzt den Platzhalter in NCBearTest (NCBearCub.glb ee7a0cce, NCBearCub.png
   92a829fa; Sicherungen `NCBearTest_vor_junges_neu_2026-11-11_143915.zip`/`_mit_`). Gegenpruefer: ersetzt Platzhalter JA, bereit JA; Harness OK,
   19.418 Dreiecke, 26 Knochen/15 Clips wie der Erwachsene, Gehen 1,60 / Rennen 2,61 Kacheln/s (Platzhalter 0,52/2,47). Blatt
   `spiel/rig_KEVIN_junges_spielfertig.png` (nicht in Git), Berichte `spiel/rig_*.md`. Offen: M3 Pfoten rutschen, wenn B1d es ueber 0,35 wachsen
   laesst (Tempo waechst nicht mit) -> Code-Frage; Fressen erreicht den Boden nicht (Kopf ~18 cm); Folgen-Schwelle walkSpeed (B1c 0,52) auf 1,6
   anpassen. **Kevin 15:00: "besonders die gesichtsgroesse sieht zu klein aus also das maul"** -> naechste Modell-Runde: Gesicht/Schnauze groesser,
   Kopf hoeher (nach dem Wochen-Reset 14.11.). -- vorher: Modell des Jungen: Workflow baer-rig-junges (8 Agenten, Skript `spiel/rig_junges_workflow.js`; Formrunde Kopf gerade +
   Ohren, Skelett+Gewichte, 15 Clips mit schnellerem Gehen, Pruefer Optik/Technik, Nachbesserung, Gegenpruefer), Ergebnis
   `../_arbeit/baer_gen/rig/out/42/media/...`; Lauf `wf_f7896aa7-c7b` (Task waly9lt77; abgeschnitten -> resumeFromRunId).
4. [FERTIG + EINGEBAUT 10:55, UNGESPIELT] Code **B1d Wachsen** (51 Dateien byte-gleich; Sicherungen `backups/NCBearTest/NCBearTest_vor_b1d_2026-11-11_105508.zip`/`_mit_`;
   Test `spiel/anleitung_b1d.md` (NCBear_CubGrow, NCBear_CubStats); Berichte `spiel/b1d_*.md`; Pruefer 25/0, gesamt 1173/0; Junges waechst bis 0,75 und haelt
   dort, Werte laufen weiter; Leben 40/150/400) -- vorher: Code **B1d Wachsen** (100 Tage, Werte, Faehigkeiten-Daten, Heil-Formeln, Anzeige; Modellwechsel nur vorbereitet), Skript `spiel/b1d_workflow.js`, 9 Agenten; Lauf `wf_472ecf82-135` (Task wmn6g4o1x; abgeschnitten -> resumeFromRunId).
5. Danach: Pruefer/Gegenpruefer ueber das Gebaute, Testlisten, naechster Punkt aus "Offen".

**Fertig (diese Nacht):** Modell-Lauf baer-gen-schoen (Blaetter `spiel/gen_KEVIN_*.png`); Code B1c gebaut, geprueft, in NCBearTest (08:12), hochgeladen.
**Ungespielt:** B1c (in NCBearTest seit 08:12), B1d (seit 10:55), neues Junges-Modell (seit 14:39).
**Vergleich (Testhilfe, 11.11. 14:55 in NCBearTest):** `NCBear_Vergleich()` / `NCBear_CubAlt()` / `NCBear_GenE()` -- altes Junges lebend (Art `ncbearcubalt`), grosser Generator-Baer als Standmodell braun + Fototon; 9 Dateien NCBearBench*, Sicherungen `NCBearTest_vor_vergleich_2026-11-11_145515.zip`/`_mit_`.
**Am Limit haengen geblieben:** 11.11. ~06:05 Nutzungslimit erreicht -- B1c fertig, aber nicht eingebaut; Rig-Lauf `wf_f7896aa7-c7b` lief weiter (bei Abbruch mit resumeFromRunId fortsetzen).
**Fragen fuer Kevin:** (aus B1c, je mit Empfehlung; Einzelheiten `spiel/b1c_gegen_bericht_b1c.md` und `spiel/b1c_forschung_b1c.md` Abschnitt 12)
  1. A3: Vanilla-Lua-Bausteine ohne Aufrufer (addTickBox/addSlider der Optionen-Seite) als Beleg zaehlen? -> ja.
  2. MP nach Server-Absturz: aelteres Register gewinnt (Schutz vor gefaelschtem Spiegel), im SP der neuere Stand? -> ja.
  3. Q-Ruf holt ein FOLGENDES Junges, ein bleibendes nicht -- auch beim Bleiben holen? -> erst im Test ansehen.
  4. Zombie zwischen dir (>10 Kacheln) und dem Jungen: es rennt weg und kommt zurueck -- lieber stehen bleiben? -> ja, mit B5a.
  5. Gehen zeigt sich selten (nur bis 3 Kacheln, wenn du fast stehst) -- oefter? -> mit dem neuen Modell einstellen (`NCBear_CubSet("walkDist", 6)`).
  6. FR-Text 'pret' -> 'prete', 'Caresse' Einzahl? -> aendern (klein).
  7. F7: jeder Spieler kann in Vanilla jedes Tier in einen Tier-Anhaenger laden, auch fremde gezaehmte Junge -- Luecke schliessen? -> ja (vor MP).
  9. B1d (je Empfehlung in `spiel/b1d_gegen_bericht_b1d.md`): Selbstheilung 1 %/h ist schon an (Engine-Heilung wird zurueckgenommen) -- so lassen? -> ja;
     setHealth 0..1 und setSizeForced am lebenden Tier als belegt zaehlen? -> ja; Spieler/Autos schaden dem Baeren nicht (mit B5a) -> ja;
     Testwege (Vorspulen, Leben/Erfahrung setzen) vor der Uebernahme in die Bench -> ja; Leben 40/150/400, Ausdauer 50/100/160 -> ja, im Test
     nachstellen; Modellwechsel fuer Halbstark (Junges- oder Erwachsenen-Modell?) -> nach Blick auf Fussgleiten im Test.
  8. Grosser Baer aus dem Generator: Farbe braun oder Fototon (Blatt `spiel/gen_KEVIN_gross.png`); Kopf: 2c-Kopf behalten oder Generator-Kopf?


> **Neuer Account oder neue Sitzung? Zuerst `UEBERGABE.md` (10.11. ~11:00): wo wir stehen, was Kevin testen muss, offene Fragen, was als Naechstes kommt.**

> **10.11.2026 ~22:25: Spieltest B1a nach Fix 1:** `NCBear_CubHere()` geht ("cub b1 appeared 8 tiles away"), Junges flieht ohne Futter
> (Kevin: "das rennt weg") -- wie geplant. Kevin sah ZWEI Junge: er hat den Spielstand `Saves/Apocalypse/2026-11-10_22-12-12` geladen (vor
> Fix 1 angelegt); das zweite ist sehr wahrscheinlich die Waise des gescheiterten ersten Versuchs (addAnimal lief, Eintrag nicht).
> **N5 (neu, klein):** ein `ncbearcub` OHNE Spiegel/Eintrag raeumt `B.ScanAnimals` nie weg (`server/BanditsNPCBearWorld.lua`, Zweig
> `mark == nil` merkt es nur als `loose` fuer den AnimalID-Rueckfall) -- Waisen nach Absturz/Fehler bleiben fuer immer. Beheben: Waise
> ohne passenden Eintrag unbeobachtet entfernen (wie der `stale`-Zweig).
> **N6 (neu, Bedienung):** Kevin: *"man kann garkein essen in die hand nehmen?"* -- stimmt: Vanilla bietet fuer Essen kein "Ausruesten"
> (`client/ISUI/ISInventoryPaneContextMenu.lua:431`, `not tests.isAllFood`). Das Anlocken mit Futter in der Hand (Server `playerInfo`
> liest `getPrimaryHandItem`) ist so nur waehrend "Feed" erreichbar (Menue nimmt das Stueck zuerst in die Hand,
> `client/BanditsNPCBearMenu.lua:79`). Anleitung Schritt 4 und 9 waren falsch. Vorschlag fuer Kevin: eigener Menuepunkt am Jungen
> "Futter hinhalten" (nur ausruesten, Vanilla `ISWorldObjectContextMenu.equip` wie Menue :79).
> Kevin: Fuettern ging *"mit hinterherrennen"* -- *"vorher bekommt man das feed fenster ja nicht auf wenn man zuweit weg steht"*: der
> Rechtsklick am Tier geht nur aus der Naehe, das scheue Junge flieht -> man muss es jagen. Zusammen mit N6 loesen (Hinhalten/Hocken).
> **Fix 2 (im Staging, NOCH NICHT in der Test-Mod, weil Kevin spielt):** ~900 Warnungen "Missing arguments for UI_BN_Bear_Hud_Taming"
> u. a. in wenigen Minuten (jede mit Ausnahme + Stacktrace) -- `B.T` fragte `getTextOrNull(key)` ohne Werte bei jedem Aufruf. Jetzt einmal
> je Schluessel und Sitzung (`shared/BanditsNPCBear.lua`, `tHas`), Pruefer 0, Attrappen 261/133/113 ohne Fehler. Rest: hoechstens eine
> Warnung je Platzhalter-Schluessel und Sitzung; ganz weg nur mit NPC Crews Weg `getTextOrNull(key, "%1".."%9")` (kein Vanilla-Beleg mit
> Werten -> braucht Kevins Wort).
> **Kevin 11.11. ~00:20 fuer das Wachsen (B1-Wachsen, nach B1b):** 100 Spieltage bis ausgewachsen (Halbstark ab ~15, 1,0 ab ~45, 1,35 ab
> ~100), Sandbox-Option, Werte steigen JEDEN Tag (Tabelle ganz unten in `begleiter/ENTSCHEIDUNGEN.md`; ersetzt 7 + 14 Tage vom 08.11.).
> **Kevin ~01:50 beim Spielen:** (1) gezaehmtes Junges rennt bei Laerm weg (Rennen/Schuesse; Engine `respondToSound`) -> wie beim grossen
> Baeren abfangen; (2) Zombie direkt daneben, Junges reagiert nicht (`fleeZombies = false`) -> nach Kevins Regel hinter den Besitzer
> verstecken; (3) Zombies sollen Baeren angreifen (B5a; Vorschlag: alle gezaehmten, auch das Junge). Alles naechste Version.
> **11.11.2026 ~01:45: B1b IM SP ANGESPIELT:** nach `NCBear_CubTame(100)` gezaehmt, **Folgen klappt** (Kevin: *"okay klappt jz hab den
> getamed und der folgt"*). Neuer Wunsch: Baeren-Fenster auf **V** (Taste einstellbar), siehe ENTSCHEIDUNGEN.md unten.
>
> **11.11.2026 ~01:35: ZAEHMUNG NACH ABSTURZ VERLOREN (N9, Ursache gefunden, nicht B1b).** Kevin: *"hoe der baer der eben getamed war ist jz
> nichtmehr getamed ist das normal?"*. Belege: Absturz 22:40 (Vanilla-Debug-NPE, `Logs/2026-11-10_22-20_DebugLog.txt:8745`) schrieb den
> Spielstand nach `Saves/Apocalypse/2026-11-10_22-12-12_crash/` -- dort steht im Register b1 `st tame`, `tame 100`, `bond __sp`
> (`global_mod_data.bin`, 598 Bytes). Der normale Ordner hat seit 22:43 ein LEERES Register (`cubs {}`, 182 Bytes); das Tier selbst lag
> mit seinem Spiegel noch da und wurde als neues "found" (b2) aufgenommen; dazu kam ein neues Wald-Junges b1 (48 Kacheln). Kevin fuettert
> jetzt b2 (Balken 33). **Folge-Fix (naechste Version): Register-Selbstheilung** -- Spiegel am Tier (`tcBear` = heute nur {id, st})
> um owner/bond/tame/mode/name erweitern und einen fehlenden Eintrag daraus wiederherstellen statt "found"/"shy" neu anzulegen.
>
> **11.11.2026 01:19: B1b IN NCBearTest -- UNGESPIELT.** Folgen/Bleiben (nur gezaehmt, Besitzer; bewegt per `fleeTo` wie B1a, kein Jar-only),
> Namensschild (Name + "following"/"staying", dicht ueber dem Kopf, Stellwert `tagZ`), Umbenennen ("Name the cub", ISTextBox, max 24,
> Server prueft), "Hold out food for the cub" (Welt-Menue, nur ausruesten), Waisen-Aufraeumen (N5), Sandbox `BearFollowMaxDistance` 40,
> Zaehm-Punkte 4/3 (~12 Spielstunden, nur neue Spielstaende), Fix 2/3 drin. Workflow `wf_65827303-1fd` (9 Agenten, Opus): 16 Befunde, 13
> zu, 3 teils (A3 Zeile 2 nur blasser; A6 Waisen-Suchlauf am MP-Server Testpunkt; A7 Junges eines abgemeldeten Besitzers wartet als
> follow -- Kevins Wort). Gegenpruefer: bereit, kein Blocker. Claudes Gegenprobe: luacheck/scopecheck 17/0, gesamt 486/0, b1b_kern 203/0.
> Einbau 42 Dateien byte-gleich (2 neu, 26 eigene ueberschrieben, 14 gleich), mod.info-Beschreibung ersetzt, Sicherungen
> `backups/NCBearTest/NCBearTest_vor_b1b_2026-11-11_011854.zip` / `..._mit_b1b_...`. **Kevins Test: `spiel/anleitung_b1b.md`.** Berichte
> `spiel/b1b_*.md`. Fragen an Kevin (Gegenpruefer): Zeile 2 nur blasser ok? MP-Abmelden wartet als follow ok? Bleiben-Radius 12?
> Abstand beim Stehenbleiben (bis 0,5 Kacheln, Stellwert followLead)? Offen aus der Forschung: Junges zu langsam (Gehen 0,52 Kacheln/s ->
> rennt immer; schnellere Clips im Modell-Lauf?), Q-Ruf/Laerm laesst es fliehen.
> **Symbol fuer die Bildschirm-Markierung:** zweite Runde im Cartoon-Stil (`spiel/icon_auswahl_2.png`, Dateien `../_arbeit/baer_icon/`),
> **Kevin waehlt Entwurf 1 (Kopf von vorn)** -> `../_arbeit/baer_icon/BanditsNPCBearCub_marker.png`, Einbau naechste Version; Bandits multipliziert die Markierungsfarbe mit sich selbst (Bandits `BanditEventMarkers.lua:153-155`).
>
> **Kevin 11.11. ~01:35 Anzeige ueber dem Baeren:** je Spieler einstellbar (Name ein/aus, jeder Wert einzeln als Balken ODER Zahl, Groesse,
> "DODGE" beim Ausweichen wie NPC Crew) -- Mod-Optionen wie NPC Crew `client/BanditsNPCModOptions.lua`; Name/Groesse nach B1b, Werte mit
> Wachsen/Kampf/Beduerfnissen (ENTSCHEIDUNGEN.md ganz unten).
> **ERLEDIGT in B1b (11.11. 01:19):** Zaehm-Dauer auf ~12 Spielstunden (Kevin 11.11.: Abklingzeiten bleiben, nur laenger):
> Vorgaben `BearTameFeedPoints` 14 -> 4 und `BearTamePetPoints` 8 -> 3 in `shared/BanditsNPCBear.lua` (B.OPTS) UND `sandbox-options.txt`,
> Tooltips mit Zahlen pruefen, Attrappen (erwartete Punkte) nachziehen. Ausserdem Fix 2/3 (schon im Staging) muessen nach dem B1b-Lauf noch drin sein.
>
> **10.11.2026 ~23:10: MODELL-LAUF baer-gen-schoen GESTARTET auf Kevins Wort** (erst `wf_26796352-25b`, nach 5 min angehalten und mit Referenzfotos aus allen Winkeln NEU als `wf_ae849387-409`, Task `wgdq3xjm8`; 6 Agenten, Opus; Skript-Kopie `spiel/gen_schoen_workflow.js`): Junges NEU aus
> Foto C (`begleiter/vorlage_C_junges_steht.jpg`, steht ruhig) -> 10+ Varianten -> Spielnetz -> Nacharbeit; grosser Baer E nacharbeiten
> (Schwanz-Lappen und Kopf-Wulst weg, Augen/Nase/Krallen, Fellstriche); Optik-Pruefer, Nachbesserung, Gegenpruefer. Ergebnis-Blaetter fuer
> Kevin: `../_arbeit/baer_gen/bilder/KEVIN_junges.png`, `KEVIN_gross.png`; Berichte `../_arbeit/baer_gen/C_*.md`, `E_FEIN.md`,
> `OPTIK_PRUEFUNG.md`, `GEGEN_OPTIK.md`. Noch ohne Knochen/Clips (spaeterer Lauf). Laeuft parallel zu B1b.
>
> **10.11.2026 ~23:00: GENERATOR STUFE 2 FERTIG** (Bericht `spiel/gen_STUFE2.md`, Blaetter `spiel/gen_A_spielnetz.png`,
> `gen_E_spielnetz.png`, nicht in Git). 18 Varianten; gewaehlt A_s2 und E_c2_form; Spielnetze `../_arbeit/baer_gen/aus/A_spielnetz.glb`
> (19.124 Dreiecke) und `E_spielnetz.glb` (19.562), je 1 Teil, 0 Loecher, Textur 1024, Farbe am Foto geeicht. **Claudes Urteil nach
> eigenem Ansehen:** beide in Spielgroesse klar als Baer lesbar, E von der Seite ueberzeugend (Buckel, Beine), aber noch Pluesch:
> keine Augen/Augenpartie, E Lappen am Hinterteil + Wulst hinter dem Kopf, A Gesicht cremefarben und Fell fleckig, Pfoten ohne Krallen.
> **Wichtig fuer den naechsten Schritt:** A steht in der Schritt-Pose des Fotos (ein Vorderbein gehoben, Kopf gedreht) -- fuer Skelett und
> Clips muss es erst in die Ruhelage; E steht fast in Ruhelage. Noch kein Skelett, keine Clips, nichts im Spiel. Kevins Urteil steht aus.
> **Spieltest B1a weiter:** Zaehmen + Speichern/Laden geklappt (Kevin: *"der hat den reload ueberlebt"*). Kevins Absturz 22:40 war NICHT
> unser Code: `Logs/2026-11-10_22-20_DebugLog.txt:8745` NullPointerException in `NetworkPlayerAI.checkDebugInput` ->
> `GameClient.sendClientCommand` ohne Verbindung (Debug-Eingabe im SP, kein Lua im Stapel).
> **B1b gestartet 22:45 auf Kevins Wort** (*"Folgen + Namensschild"*): Workflow `wf_65827303-1fd` (10 Agenten, Opus), Plan
> `../_arbeit/baer_zaehmen/PLAN_B1B.md`, dazu Futter hinhalten (N6/N8) und Waisen (N5). Verbrauch 22:42: 5 h 10 %, Woche 8 %.
> **Fix 3 (im Staging, noch NICHT in der Test-Mod):** Streicheln ohne Ton -- Vanilla spielt den Ton ueber das Anim-Ereignis
> `PlayBreedSound` im idlePetting-Knoten (z. B. `AnimSets/cow/idle/idlePetting.xml:13`), das Animset buck hat keinen. Jetzt: Rasse-Ton
> `petting = PetAnimalCalf` (`shared/BanditsNPCBearDefs.lua`), Zeitaktion spielt ihn selbst (`playBreedSound`/`stopOrTriggerSound` wie
> Vanilla `ISPickupAnimal.lua:23/27/33`). Pruefer 0, Attrappen 261/133/113 (Tier- und Spieler-Attrappe um die zwei Ton-Aufrufe ergaenzt).
> **Zaehmen geklappt** (Kevin ~23:00, ueber `NCBear_CubSkip`); nach dem Zaehmen gibt es in B1a nichts mehr zu tun -- Kevin: *"kann jz
> nichtmehr mit dem machen also da steht auch nicht ueber den baeren das es meiner ist"*. Naechste Version (B1b) nach seiner Wahl.
> **N7 (Streichel-Abstand) -- ERLEDIGT, bleibt so** (Kevin: *"diesmal hat er aber richitg gestreichelt also lass das einfach so das kommt wohl auf den blickwinkel an"*). Alter Befund: Kevin: *"zuviel abstand beim streicheln aber danach tut der die hand unter den baeren das sah gut aus"*.
> Vanilla geht zum Kopf-Anhaengepunkt (`client/ISUI/Animal/ISAnimalContextMenu.lua` onPetAnimal: `getAttachmentWorldPos("head")` +
> `ISWalkToTimedActionF`); unser Junges hat KEIN `attachment head` in `scripts/nc_bear_cub.txt`, das Menue nimmt nur `walkAdj`
> (`client/BanditsNPCBearMenu.lua:86-94`). Beheben zusammen mit dem neuen Modell: `attachment head` (Kopfknochen, Versatz am Modell
> gemessen) + Streicheln und Fuettern wie Vanilla zum Kopf gehen lassen.
> **Screenshot Kevin ~22:50 (Taming 62 %):** Untermenue "Brown Bear cub": Tier Information, **Tier mit Seil anleinen**, **aufheben**, Debug,
> Feed (rot = satt, richtig), Pet; Welt-Menue "Lay out bear bait" rot (richtig: gebunden), kein "Kill" (richtig). Aufheben/Anleinen kommen
> vom aktiven **"Tier Cheat"** (`AnimalContextMenu.cheat`, `client/ISUI/Animal/ISAnimalContextMenu.lua:166/173`) bzw. Gottmodus
> (Jar `IsoAnimal.canBePicked`); ohne Cheat: Aufheben nie (`canBePicked = false`), Anleinen nur wenn `getBehavior():canBeAttached()` --
> fuer das Junge UNGEPRUEFT. **N8:** Vanilla hat ein eigenes Anlocken mit Futter aus dem Inventar ("ContextMenu_Lure",
> `ISAnimalContextMenu.lua:270`, Jar `getPossibleLuringItems` = `getAllPossibleFoodFromInv`) -- Kandidat fuer N6, aber Vanillas
> `eatFromLured` laesst das Tier das Stueck selbst fressen (an unserem Register und Balken vorbei) -> vorher klaeren. Balken haengt in
> Kopfhoehe des Spielers, deutlich ueber dem kleinen Jungen (`B.CFG.barZ`) -- evtl. tiefer.
>
> **10.11.2026 ~21:50: ERSTER SPIELTEST B1a, Fehler 1 behoben.** Kevin: `NCBear_CubHere()` -> *"no cub: not inworld"* (console.txt:5454
> `[TC-BEAR] *** create: the new cub is not in the world at 11073,9713`). Ursache: `B.CreateCub` fragte direkt nach `addToWorld()`
> `isExistInTheWorld()`; die Engine haengt ein neues Tier erst beim naechsten Update in die Kachel-Liste (Jar 42.22.2), im selben Bild also
> immer falsch. Korrektur: Pruefung entfernt (`server/BanditsNPCBearWorld.lua:231-238`; Vanilla und der gespielte Erwachsene pruefen dort
> auch nicht), Pruefer 0, Attrappen 261/0 und 133/0, in der Test-Mod nach Kevins "Spiel ist zu". **Lehre:** was "im selben Bild" nach einem
> Engine-Aufruf gilt, kann keine Attrappe zeigen -- solche Sofort-Gegenproben nur mit Spielbeleg. Kevin testet nach Neustart weiter
> (`spiel/anleitung_zaehmen.md`, frischer Spielstand).
>
> **10.11.2026 21:28: B1a "FINDEN UND ZAEHMEN" IST IN NCBearTest -- UNGESPIELT.** Etappe 2 (4 Opus-Agenten, Workflow `wf_9beab0a4-ae9`):
> 17 Befunde, 15 geschlossen (darunter der MP-Blocker B1 "Hello mit leerer Tabelle" und die majors A1 `removeAnimal` am Server, A2
> `serverStart/serverStop`), Gegenpruefer: **bereit fuer den ersten SP-Test, kein Blocker**; Pruefer 15/0, Gesamt-Attrappe 261/0, Probe mit
> `--vor-b5a` OK. Einbau: 40 Dateien byte-gleich (39 neu, nur `Translate/EN/IG_UI.json` ueberschrieben), Beschreibung in beiden `mod.info`
> ersetzt, Sicherungen `Zomboid/backups/NCBearTest/NCBearTest_vor_zaehmen_2026-11-10_212816.zip` und `..._mit_zaehmen_...`; das Spiel lief
> nicht. **Kevins Test: `spiel/anleitung_zaehmen.md`** (Wegwerf-Spielstand, `-debug`, `NCBear_CubFood()`, `NCBear_CubHere()`).
> Das Junge traegt noch das ALTE Entwurfs-Modell als Platzhalter (das neue kommt aus dem Generator, gleiche Dateinamen).
> Berichte: `spiel/zaehmen_*.md` (zuerst `zaehmen_gegen_bericht.md`). **Offen, nur Mehrspieler:** A3 (`getObjectListForLua`, `getAnimalID`,
> `isRotten/isBurnt` am Server ohne Server-Beleg -> Kevins Wort je Methode oder MP-Test), B2 (Uhren laufen nur, solange der Finder online
> ist), N1-N4 klein. **Fragen an Kevin:** B2 Uhren auch offline? B5 reifer Koeder verfaellt nach 8 Spieltagen ok? A3 wie oben.
> Echte Uebernahme nach NPC Crew bleibt gesperrt bis B5a (24 Altlasten der alten `NCBear*`-Dateien).
>
> **10.11.2026 ~21:15: GENERATOR-PROBELAUF FERTIG, Stufe 2 laeuft.** ComfyUI v0.44.0 + TRELLIS.2 laufen lokal (kein weiterer Download),
> Bericht `../_arbeit/baer_gen/PROBELAUF.md`, Startskript `tools/gen_trellis.py` + `tools/trellis2_ablauf_api.json`. Rohmodelle
> `../_arbeit/baer_gen/aus/A_roh.glb`, `E_roh.glb` (je 700.000 Dreiecke, ein Teil, Beine getrennt; A 303 s / 21,4 GB, E 174 s / 18,6 GB
> Grafikspeicher). Blaetter `spiel/gen_A_rundum_roh.png`, `gen_E_rundum_roh.png` (nicht in Git) -- Kevin gezeigt. **Claudes Urteil nach
> eigenem Ansehen: Form und Proportion erstmals wirklich baerenhaft (E von der Seite gut), aber NICHT schoen:** A Fell als Stachel-Geometrie,
> Textur viel zu blass, Pfoten kahl; E weisser Stachel-Fleck auf dem Scheitel, Lappen am Hinterteil, Flossen-Hinterpfoten. Stufe 2
> (Opus-Agent seit ~21:12): je Bild 5+ Varianten mit anderen Seeds, bestes waehlen, Stacheln glaetten, auf 20.000 Dreiecke, Textur 1024
> backen, Farbe ans Foto angleichen, Blaetter in Spielgroesse -> `../_arbeit/baer_gen/STUFE2.md`, `bilder/A_spielnetz.png`,
> `E_spielnetz.png`, `aus/A_spielnetz.glb`, `E_spielnetz.glb`. Danach erst Skelett/Clips. Das Spiel lief um 21:10 nicht.
>
> **10.11.2026 20:50: STAND DER DREI STRAENGE.** Verbrauch 20:46: 5 h 44 %, Woche alle 39 %, **Woche Fable 72 %** (+6 Punkte in 14 min) --
> deshalb laeuft ab jetzt ALLES Neue auf Opus, und Claudes eigene Runden bleiben kurz (der Verlauf dieser Sitzung ist gross und kostet Fable).
> 1. **baer-zaehmen Etappe 1 FERTIG** (6 Agenten, 0 Fehler): Staging `../_arbeit/baer_zaehmen/mod/` 40 Dateien (15 Lua `BanditsNPCBear*` +
>    Bench `NCBearBenchCub.lua`, 21 Textdateien in 7 Sprachen, `sandbox-options.txt`, `nc_bear_cub.txt`, Platzhalter-Modell), Bericht
>    `../_arbeit/baer_zaehmen/bau_uebernahme.md` (Pruefer 0 Fehler, Gesamt-Attrappe 175/0, Trockenlauf rot nur mit den 24 Altlasten, Probe
>    mit `--vor-b5a` OK), neu `tools/baer_uebernahme.py` und `NAEHTE.md`. Claudes Stichprobe: luacheck 15/0, kein Testbefehl ausserhalb der
>    Bench, `addAnimal`/`remove` nur in `BanditsNPCBearWorld.lua`. **Nebenfund: das Spiel ist laut Forschung 42.22.2** (Bandits hat einen
>    Ordner `42.22`, nachgesehen) -- Zeilennummern aelterer Unterlagen sind verschoben. **Etappe 2 laeuft** seit 20:48: Workflow
>    `wf_9beab0a4-ae9` (Task `wrmx0e3gl`; Pruefer A Belege/Regeln, Pruefer B Logik/SP-MP, Nachbesserung, Gegenpruefer; 4 Agenten, alle Opus),
>    Berichte kommen nach `../_arbeit/baer_zaehmen/pruef_a.md`, `pruef_b.md`, `nachbesserung.md`, `gegen_bericht.md`,
>    `anleitung_zaehmen_entwurf.md`. Danach: Einbau in NCBearTest (nur wenn Kevin nicht spielt), Commit + Push.
> 2. **Generator:** alle sechs Dateien da, Groesse und SHA256 stimmen (20:45). Ein Opus-Agent richtet seit 20:48 ComfyUI ein
>    (`C:/Users/Kevin/Tools/ComfyUI/ComfyUI_windows_portable/`), baut den Ablauf nur mit TRELLIS.2, erzeugt `../_arbeit/baer_gen/aus/A_roh.glb`
>    und `E_roh.glb`, rendert Rundum-Blaetter `../_arbeit/baer_gen/bilder/A_rundum.png` / `E_rundum.png`, Bericht
>    `../_arbeit/baer_gen/PROBELAUF.md`, Startskript `tools/gen_trellis.py`. Claude sieht die Blaetter selbst an, bevor Kevin sie bekommt.
> 3. **baer-junges (Skript-Modell) ANGEHALTEN 20:47** mitten im Koerper-Schritt (Task wzy7o3n1j gestoppt; frueher als angekuendigt, wegen
>    der Fable-Woche). Teilstand: `spiel/baer_form_junges.py`, `baer_export_junges.py`, `baer_gewichte_junges.py`,
>    `../_arbeit/baer_junges/glb_koerper/v1.glb`. Fortsetzen ginge mit `resumeFromRunId wf_b8e6ce94-a1a` (nur diese Sitzung) -- nur falls der
>    Generator-Weg scheitert.
>
> **10.11.2026 20:32: GENERATOR-WEG GESTARTET auf Kevins Wort** (*"Ja, alle sechs"*, *"nimm A fuers baby und E fuer den grossen und mach das
> bitte richtig schoen von allen seiten"*). Die sechs Dateien (ComfyUI v0.44.0 + TRELLIS.2, 10,24 GB) laden seit 20:28 nach
> `C:/Users/Kevin/Tools/ComfyUI/_download/` (Skript `laden.sh` dort: prueft Groesse und SHA256, setzt Abbrueche fort; Hintergrund-Task
> br5oq1pey). Vorlagen geladen: `begleiter/vorlage_A_junges.jpg` (Junges) und `begleiter/vorlage_E_gross.jpg` (GROSSER Baer -- auch der
> Erwachsene soll neu aus dem Generator kommen), Zuschnitte `../_arbeit/baer_gen/eingang/`. Naechste Schritte: SHA pruefen, entpacken nach
> `Tools/ComfyUI/`, Modelle nach `models/{diffusion_models,vae,clip_vision,background_removal}`, Ablauf NUR mit TRELLIS.2 bauen (Pixal3D ist
> in der EU gesperrt), Probelauf, dann Netz -> 20.000 Dreiecke -> Skelett/Clips, Rundum-Renders aus der Spielkamera fuer Kevin.
> Laeufe 20:32: baer-zaehmen Kern + Oberflaeche FERTIG (Opus), Uebernahme-Skript laeuft; baer-junges noch im Koerper-Schritt. Claudes Plan:
> baer-junges NACH dem Koerper-Schritt anhalten (Kopf und Textur per Skript waeren mit dem Generator ueberholt; Skelett-Masse und Clips
> bleiben nutzbar), Kevin ist das angekuendigt. Verbrauch 20:32: 5 h 31 %, Woche alle 35 %, **Woche Fable 66 %**.
>
> **10.11.2026 ~20:25: Bild-zu-3D-Generator recherchiert auf Kevins Wort** -> `begleiter/BILD_ZU_3D.md` (Empfehlung TRELLIS.2 ueber ComfyUI,
> sechs Downloads zusammen 10,24 GB mit Quelle und Groesse, acht Baerenbilder A-H, Blatt `begleiter/auswahl_baerenbilder.jpg`).
> Verbrauch ~20:20: 5 h 25 %, Woche alle 33 %, Woche Fable 64 %.
>
> **10.11.2026 nach 20:10: LIMIT-WAECHTER GELOESCHT auf Kevins Wort** (Cron `80551232`, CronDelete). Die beiden Laeufe laufen weiter, aber
> NIEMAND haelt sie mehr vor dem 5-h-Limit an und nichts setzt nach einem Reset von selbst fort; die Abbruch-Riegel in den Skripten bleiben.
>
> **10.11.2026 20:10: BEIDE LAEUFE FORTGESETZT (Wecker 20:04).** Verbrauch 20:04: 5 h 3 % (Reset 01:00), Woche alle 28 %, Woche Fable 55 %.
> Neue Task-IDs: baer-junges `wzy7o3n1j`, baer-zaehmen `ws1rh2ogz` (Run-IDs unveraendert). Die drei fertigen Agenten je Lauf kamen aus dem
> Zwischenspeicher; neu gestartet sind `bau:koerper` bzw. `bau:kern` + `bau:oberflaeche`, je mit einem FORTSETZUNG-Absatz im Auftrag (Teilstand
> ansehen und weiterbauen). **Rechnung:** die 72 min bis 18:11 kosteten 4,1 Mio. Tokens = rund 47 Punkte der Fable-Woche; der Rest beider
> Laeufe samt Etappe 2 passt NICHT mehr in die Fable-Woche. Deshalb (Claudes Entscheidung, Kevin kann sie umwerfen): **baer-zaehmen laeuft ab
> jetzt auf Opus** (`model: 'opus'` bei bau:kern, bau:oberflaeche, bau:uebernahme), baer-junges bleibt auf Fable (das Modell ist Kevins
> wunder Punkt). Dazu Abbruch-Riegel in beiden Skripten (liefert ein Bauer nichts, startet der naechste nicht). **Limit-Waechter** Cron
> `80551232` alle 10 min: haelt bei 5 h >= 85 % sauber an und stellt einen Wecker 4 min nach dem Reset; bei Woche Fable >= 95 % stoppt nur
> baer-junges, bei Woche alle >= 95 % alles. Kopien der geaenderten Skripte: `spiel/junges_workflow.js`, `spiel/zaehmen_workflow.js`.
>
> **10.11.2026 18:11: BEIDE LAEUFE ANGEHALTEN (TaskStop), Fortsetzung automatisch um 20:04** (Kevin 18:10: *"bin bei 94% 5std limit gleich
> wird triggert die sperre kannste die sachen abspweicherund und um 20:00 uhr automatisch beginnen ?"*). Verbrauch beim Anhalten: 5 h 97 %
> (Reset 20:00), Woche alle 26 %, **Woche Fable 52 %** (beim Start 5 %). Fertig auf der Platte: baer-junges -- beide Forschungen und
> `SPEZ_JUNGES.md`, Bau Koerper war mittendrin (`spiel/baer_form_junges.py` ist ein TEILSTAND, nicht committet); baer-zaehmen -- beide
> Forschungen und `PLAN_ZAEHMEN.md`, Bau Kern/Oberflaeche waren mittendrin (Staging `../_arbeit/baer_zaehmen/mod/` unfertig). Fortsetzen geht NUR
> in dieser Sitzung: Workflow mit `scriptPath` (Sitzungsordner `...\workflows\scripts\baer-junges-bau-wf_b8e6ce94-a1a.js` bzw.
> `baer-zaehmen-bau-wf_318e2ac4-9be.js`) + `resumeFromRunId` (`wf_b8e6ce94-a1a`, `wf_318e2ac4-9be`), Skripte dafuer unveraendert lassen. Der
> Wecker (Cron b826bc4c, nur solange die Claude-App offen bleibt) setzt fort und stellt einen Limit-Waechter (alle 12 min; haelt bei 5 h >= 90 %
> sauber an und weckt nach dem naechsten Reset; bei Woche >= 98 % Schluss). Ist die Sitzung weg: beide Laeufe mit den Skripten
> `spiel/junges_workflow.js` / `spiel/zaehmen_workflow.js` neu starten (fertige Berichte in den Arbeitsordnern liegen lassen und nutzen).
>
> **10.11.2026 ~17:00 (neuer Account, neue Sitzung): ZWEI LAEUFE GESTARTET auf Kevins Wort** (ENTSCHEIDUNGEN.md ganz unten), je in zwei
> Etappen, zusammen je 10 Agenten. **baer-junges** (Modell des Jungen neu und hochwertig auf Stand 2c): Etappe 1 Workflow wf_b8e6ce94-a1a
> (Forschung 2, Spezifikation, Bau Koerper+Clips, Bau Kopf, Bau Textur), Ordner `../_arbeit/baer_junges/`, Skripte `spiel/baer_*_junges.py`,
> Ergebnis `mod/42/media/` (NCBearCub.glb + NCBearCub.png), Blatt `bilder/kevin_junges.png`. **baer-zaehmen** (Code B1a: Junges finden und
> zaehmen, Tierart `ncbearcub`, neue Dateien `BanditsNPCBear*`): Etappe 1 Workflow wf_318e2ac4-9be (Forschung 2, Plan, Bau Kern, Bau
> Oberflaeche, Uebernahme-Skript), Ordner `../_arbeit/baer_zaehmen/` (Staging `mod/`, Plan `PLAN_ZAEHMEN.md`), dazu `tools/baer_uebernahme.py`
> und `NAEHTE.md`. Skripte der Laeufe: `spiel/junges_workflow.js`, `spiel/zaehmen_workflow.js`. Etappe 2 je Lauf (Pruefer 2, Nachbesserung,
> Gegenpruefer) startet Claude, nachdem er die Zwischenstaende selbst angesehen hat. NICHTS davon ist in NCBearTest, bis beides fertig,
> nachgeprueft und eingebaut ist. Fortsetzen geht nur in dieser Sitzung (scriptPath + resumeFromRunId). Verbrauch beim Start (dieses Konto):
> 5 h 7 %, Woche 3 %.

> **10.11.2026 10:37: Lauf baer-2c FERTIG und in NCBearTest (ungespielt, Test `spiel/anleitung_2c.md`).** GLB 08ec7806, Deer 91f0c60e, FBX
> da08d469, Body 4cfdb177, WorldItems a640e4cd; 12 Clips byte-gleich, SitDown/Sit/StandUp neu (gleiche Dauer/Proben), Skelett/inverseBind gleich,
> 19.806 Dreiecke (von Claude nachgezaehlt). Sicherungen `Zomboid/backups/NCBearTest/NCBearTest_vor_2c_2026-11-10_103718.zip` / `_mit_2c_...`.
> Gegenpruefer: ready=false, aber keine feste Regel gebrochen und in jedem Bild klar besser (Sitzen eng nach Vorlage, Hinterfuss kurz/dunkel,
> keine Hose-in-Stiefeln, Gebiss mit 4 Eckzaehnen + 6+6 Schneidezaehnen, flache Zunge). **Kevins Entscheidungen offen: G1 Buckel hinter dem Kopf
> tiefer?, G2 Kopf-Rand-Farbe angleichen (Kopf-Texel)?, G3 Kopf im Sitzen geradeaus?** Dazu Baby: Augen groesser? Rumpf kuerzer? Berichte
> `spiel/2c_*.md`, `spiel/baby_*.md`, Bilder `spiel/2c_vorher_nachher.png`, `spiel/baby_entwurf.png`. Woche danach 93 %.

> **10.11.2026 00:04:** Lauf baer-pfoten FERTIG und in NCBearTest (ungespielt, Test `spiel/anleitung_pfote.md`). Als Naechstes
> Lauf 2c (Gebiss, Zunge, ganze Beine) -- Kevin 09.11.: "wenn der worklow durch ist mach direkt weiter".
> **10.11.2026 00:11: Lauf baer-2c GESTARTET** (Workflow wf_966982af-cb0, 10 Agenten: 2 Forschung, Spezifikation, Bau Beine, Bau Gebiss,
> Textur, 2 Pruefer, Nachbesserung, Gegenpruefer). Arbeitsordner `../_arbeit/baer_2c/` (Skript des Laufs `workflow_baer_2c.js`, Ergebnis
> `mod/42/media/`, Abnahme `gegen_bericht.md`), neue Skriptkopien `spiel/*_2c.py`. NICHTS davon ist in NCBearTest, bis der Lauf fertig,
> selbst nachgeprueft und eingebaut ist (Resume geht nur in der Sitzung, die ihn gestartet hat). Verbrauch beim Start: 5 h 46 %, Woche 63 %.
> **10.11.2026 ~01:10: Kevin hat baer-pfoten gespielt** (Sitzen, Aufrichten): Hinterfuss wie ein Menschenfuss, Kopf passt im Sitzen nicht zum
> Koerper (Kragen), Beine zu weit auseinander, Uebergang "Hose in Stiefeln" (ENTSCHEIDUNGEN.md ganz unten). Lauf 2c dafuer angehalten und als
> **v2 fortgesetzt** (`../_arbeit/baer_2c/workflow_baer_2c_v2.js`): Forschung aus dem Zwischenspeicher, neu Spezifikation, Bau Koerper, Bau Sitzen
> (Sitz-Clips nach `begleiter/kevin_sitzvorlage.png`), Bau Gebiss, Textur, Pruefer, Nachbesserung, Gegenpruefer = 10 Agenten (+1 abgebrochener
> Planer). Verbrauch bei der Fortsetzung: 5 h 29 %, Woche 71 %.
> **10.11.2026 ~01:40: Lauf baer-baby GESTARTET, parallel zu 2c** (Kevin: "Jetzt parallel"; Workflow wf_a286bbfd-037, 4 Agenten:
> Spezifikation, Bau, Pruefer, Nachbesserung). ENTWURF des Jungen nach `begleiter/kevin_babygesicht_vorlage.webp` (eigenes Gesicht, Junges-
> Proportionen, Renders, Weg ins Spiel empfohlen), nichts in die Mod. Ordner `../_arbeit/baer_baby/` (Skript `workflow_baer_baby.js`, Blatt
> fuer Kevin `bilder/kevin_baby_entwurf.png`), Skriptkopien `spiel/*_baby.py`. Verbrauch beim Start: 5 h 38 %, Woche 73 % (Risiko: Wochenlimit
> vor Ende beider Laeufe -- Kevin weiss es und hat entschieden).
> **10.11.2026 ~04:35: baer-baby FERTIG (Entwurf, nicht im Spiel).** `../_arbeit/baer_baby/entwurf/NCBearCub.glb` (MD5 6c3f0a96, 19.806
> Dreiecke, 26 Knochen und 15 Clip-Namen wie der Erwachsene, Clips per Skript umgerechnet) + `NCBearCub.png`; Blatt fuer Kevin
> `bilder/kevin_baby_entwurf.png` (ohne Foto, von Claude angesehen: klar ein Junges mit eigenem Gesicht; Augen kleiner als im Foto, Rumpf
> lang wie ein Fass, Koerper-Baustellen aus 2c noch drin). Weg ins Spiel (B1): eigene Tierart `bearcub` -> `bear` wie Vanilla Kitz/Kalb
> (`DeerDefinitions.lua:7-11`), modData geht beim Wachsen NICHT mit (B1 reicht Besitzer/Zaehmen selbst weiter). Kevins Fragen: Gesicht ok/
> Augen groesser?, Schrittweite 0,777 oder 1,0, Halbstark-Modell, zwei Abweichungen (Unterlid dunkel, Ohrrand fellfarben). Berichte
> `SPEZ_BABY.md`, `bau_baby.md`, `pruef_baby.md`, `fix_baby.md`; Skripte `spiel/baer_*_baby.py`.
> **10.11.2026 ~04:35: Lauf 2c ANGEHALTEN (Limits: 5 h 96 %, Woche 89 %).** Fertig und im Zwischenspeicher: Forschung (2), Spezifikation, Bau
> Koerper (Hose-in-Stiefeln im Ton weg, Rumpf 0,79 statt 0,93 m, Hinterfuss 29,3 statt 43 cm, Clips und Kopf bit-gleich; offen: Achsel-Dehnung
> 3,51 > 3,5, Falten liegend 254 > 136, Kragen haengt am neuen Sitzen). Bau Sitzen lief 32 min und wird beim Fortsetzen neu gestartet. Fortsetzen
> NUR in dieser Sitzung: Workflow mit scriptPath = Skript des Laufs (Kopie `../_arbeit/baer_2c/workflow_baer_2c_v2.js`) und resumeFromRunId
> wf_966982af-cb0. Rest: Sitzen, Gebiss, Textur, Pruefer, Nachbesserung, Gegenpruefer (6 Agenten, grob 12-18 % der Woche).
> **10.11.2026 ~05:15: Lauf 2c FORTGESETZT** (Skript v3: Hinweis an den neu startenden Sitz-Bauer). Grund: Kevins Regel aus der NPC-Crew-
> Hauptsitzung (uebermittelt): weiterarbeiten bis Wochenlimit 98 %, dann sofort stoppen, speichern, Uebergabe fuer einen anderen Account
> -> `UEBERGABE_LIMIT.md` (vorbereitet). Die Hauptsitzung schickt das Stopp-Signal. Woche beim Fortsetzen 89 %, 5 h 0 %.

> **09.11.2026 ~14:20 (neue Sitzung, neuer Account):** Lauf baer-fell FERTIG und in NCBearTest (ungespielt, Test
> `spiel/anleitung_fell.md`); Forschungslauf baer-schlaf fertig (`begleiter/SCHLAF_PLAN.md`, Kevins Fragen K1-K21 offen).
> Die damalige `UEBERGABE.md` (09.11.) ist damit erledigt.

Lies zuerst `../CLAUDE.md` (Grundregel: gebaut FUER NPC Crew, am Ende per Copy-Paste uebernehmbar, keine Cheat-/Testmenues kommen mit),
dann **`begleiter/ENTSCHEIDUNGEN.md` (geht vor PLAN.md)**, dann `begleiter/PLAN.md` und `begleiter/KRITIK.md`.

## Wo was liegt
| Was | Pfad |
|---|---|
| Test-Mod (spielbar) | `C:/Users/Kevin/Zomboid/mods/NCBearTest` (Git: `Zomboid/backups/NCBearTest/repo.git`, Zweig `main` -> GitHub `NPCCrew-Baer`) |
| Unterlagen (dieser Ordner) | `C:/Users/Kevin/NPCCrew-Nebenprojekte/baer` (Git-Zweig `unterlagen` -> GitHub `NPCCrew-Baer`) |
| Kevins Entscheidungen | `begleiter/ENTSCHEIDUNGEN.md` (Groesse, Stufen, Leben, Futter, Inventar, Kampf, Sitzen, kein Scheinangriff ...) |
| Spiel-Bau, Berichte | `spiel/` (`anim_*.md` = Lauf baer-anim 08.11., `kampf_*.md` = Lauf baer-kampf, `baer_*_anim.py` = Blender-Quellen der Clips) |
| Modell-Entwuerfe | `entwuerfe/`, Hochmodell-Skript `baer.py` |
| Toene | `sound/` (`roh/QUELLEN.txt`: drei gemeinfreie Aufnahmen, jeder Download von Kevin einzeln freigegeben; `schnitt.py`) |
| Arbeitsdaten (Blender-Laeufe, Renders, Attrappen) | `../_arbeit/baer_anim` (2,5 GB), `baer_spiel`, `baer_kampf`, `baer_angriff`, `baer_begleiter`, `baer_spionage`, `blender_test/baer` |
| Sicherungen | `Zomboid/backups/NCBearTest/*.zip` (u. a. `NCBearTest_mit_anim_2026-11-08_175026.zip`, `baer_docs_2026-11-08_175312.zip`) |

## Stand
- Lebendes Tier `bear` in NCBearTest (eigene Clips, Animset, GLB), Kampf gegen Zombies und FEINDLICHE Banditen: Hieb links/rechts, Biss
  stehend und am Boden, Doppelschlag im Wechsel, Aufrichten+Bruellen nur zu Kampfbeginn (50 %, 120 s), Knockback (frontal ~1,7 Kacheln, seitlich
  auf der Stelle), Schaden 2-3 Hiebe je normalem Zombie, Schnauben im Alltag, Sitzen/Aufstehen/Fressen (`NCBear_Sit/Stand/Eat` in `NCBearBench.lua`).
- Lauf baer-anim (08.11., 10 Agenten) fertig, in NCBearTest kopiert, **gespielt 08.11. ~18-20 Uhr** (Kevin: "er sieht huebscher aus";
  Angriffe brechen bei Laerm ab -> baer-laerm; Unterseite, Sohlen und Sitzen -> baer-fell und Clip-Runde). Kevin hat Videos und `spiel/anim_sitzen_vergleich.png`.
- Kevins letzter Test (08.11. ~03:00, Stand baer-kampf): Umwerfen klappt; "sofort tot" kam vom Debug-Spawn (Leben 1,0) -> Schieber auf 2,0
  oder `NCBear_ZHealth(2, 10)`.

## Offen -- in dieser Reihenfolge bauen (Kevin 08.11. ~19:50: erst Gegenwehr, dann Baby finden und zaehmen -- "das wuerde mehr sinn machen")
1. **Lauf baer-laerm FERTIG, in NCBearTest seit 08.11. ~20:46, ungespielt** (7 Agenten; Berichte `spiel/laerm_*.md`, Test
   `spiel/anleitung_laerm.md`). Ursache: Zombie-Schlaege an Zaun/Tuer, Q-Rufen u. a. schicken den Baeren per
   IsoAnimal.respondToSound weg, das alte fleeStop stoppte jedes Bild -> bis zu 9 Fluchtbefehle je Schlag, Clip-Neustart.
   Jetzt: ein Halt je Fluchtbefehl (fleeWait 18 Bilder), Clip-Neustart erkannt, Anlauf holt fremde Wege zurueck, Notloesung
   clockHit. Dazu knockPush-Vorgabe 0,7, Testbefehle drehen zur Kamera (SE), refreshBlock nicht mitten im Halt.
   **Offen, Kevins Wort:** Stress-Ausgleich mit `changeStress` (Vanilla-belegt, Spielregel); `setShouldFollowWall(false)` (nur Jar).
   Arbeitskopie und Attrappen: `../_arbeit/baer_laerm/` (`attrappe/anim/test_anim.lua`, `attrappe/kampf/test_fight.lua`).
2. **Lauf baer-fell FERTIG, in NCBearTest seit 09.11. ~14:19, ungespielt.** Forschung, Netz, Textur (alte Sitzung), Pruefer Optik +
   Technik, Nachbesserung, Gegenpruefer (neue Sitzung, 4 Agenten). Sohlen mit Ballen (Netz 8 mm + Textur), Unterseite hell und
   ausgearbeitet (Back-Pose-Ansichten), Hautdehnung 99,5 % <= 2,45 (vorher bis 4,13), Achsel/Brust <= 3,02 (vorher 8,21), Ei im Aufrichten
   behoben, Straehnen kraeftiger, Body-Textur bleibt 1024 (keine Mipmaps bei Tieren, 2048 flimmert). 15/15 Clips bit-gleich, Kopf
   unveraendert, 18.930 Dreiecke. Berichte `spiel/fell_*.md`, Bild `spiel/fell_vorher_nachher.png`, Test `spiel/anleitung_fell.md`.
   Sicherungen `backups/NCBearTest/NCBearTest_vor_fell_2026-11-09_141924.zip` / `..._mit_fell_..._141925.zip`. Skripte
   `spiel/baer_{export,kampf,gewichte,textur}_fell.py`, Arbeitsdaten `../_arbeit/baer_fell/`. **Neue Clips -> `baer_gewichte_fell.py` neu
   laufen lassen** (Gewichte sind auf genau diese 15 Clips abgestimmt). **Offen, Kevins Wort:** Zotteln am Umriss (Netz-Zotteln
   verworfen: Noppen), Pranken-Form, Gesaessfalte schwach, Kopf-Variante B (`../_arbeit/baer_fell/textur/NCBear_kopf_variante*.png`),
   eigenes Baby-Modell (`../_arbeit/baer_fell/baby/baby_vergleich.png`; **Kevin 09.11. ~16:09: Gesicht des Jungtiers nach
   `begleiter/kevin_babygesicht_vorlage.webp`** -- runder Kopf, grosse runde Ohren, kurze helle Schnauze, ENTSCHEIDUNGEN.md ganz unten).
2b. **Lauf baer-pfoten FERTIG, in NCBearTest seit 10.11. 00:04, ungespielt** (Kevin 09.11.: "wie ein abgesaegtes Bein"; 9 Agenten:
   Referenz, Bestand, Spezifikation, Netz, Textur, Pruefer Optik + Technik, Nachbesserung, Gegenpruefer). Bein laeuft unter 36 cm zum
   Gelenk schmal zu (~19 cm), Hinterfuss mit Ferse, langer ovaler Sohle und 5 Zehen, Vorderpranke mit quer liegendem Ballen und
   Handwurzelballen; Gewichte trennen am Gelenk. 15/15 Clips bit-gleich (selbst nachgezaehlt gegen das alte GLB), Skelett gleich, Kopf
   unveraendert, 19.426 Dreiecke. 5 Dateien (GLB 5066fa67, Deer 1f704054, FBX 0cab0ff6, Body 4ae148df, WorldItems 603ee699).
   Berichte `spiel/pfote_*.md`, Bild `spiel/pfote_vorher_nachher.png`, Test `spiel/anleitung_pfote.md`, Sicherungen
   `backups/NCBearTest/NCBearTest_vor_pfote_2026-11-10_000429.zip` / `..._mit_pfote_...`. Skripte `spiel/baer_{quelle,export,kampf,
   gewichte,textur}_pfote.py`, Arbeitsdaten `../_arbeit/baer_pfote/` (Bezug `fix1/bau4/textur/zw_fell_2048.png` behalten).
   **Schwaeche, geht in Lauf 2c:** ueber dem Gelenk wird das Bein auf kurzer Strecke wieder dick ("Glocke", `spiel/pfote_kegel.png`),
   weil der Lauf das Bein nur unter 36 cm aendern durfte. **Angenommene Abweichungen von der SPEZ (Kevins Wort offen):** Falten im
   Liegen 136 statt <= 120 (Flaeche wie baer-fell), 13 Rumpfpunkte bis 2,3 cm daneben (unsichtbar). **Clip-Runde:** Pranke beim
   Aufrichten von vorn klotzig (Handflaeche nach vorn drehen), Hinterfuss im Renn-Rueckschwung schmal, Liegen schwebt 4 mm, `Toe0`
   abrollen lassen. Die Pruef-Agenten haben trotz geloeschter Regel nur bei geschlossenem Spiel gerendert (Vorsicht, kein Fehler).
2c. **Lauf baer-2c FERTIG, in NCBearTest seit 10.11. 10:37, ungespielt** (Gebiss, Zunge, ganze Beine + Kevins Spieltest vom 10.11.:
   Sitzen nach Vorlage, Hinterfuss, Kopf/Kragen, Beine eng, keine Hose-in-Stiefeln). Test `spiel/anleitung_2c.md`, Berichte `spiel/2c_*.md`.
   **Offen, Kevins Wort: G1 Buckel hinter dem Kopf, G2 Kopfrand-Farbe, G3 Kopf schaut im Sitzen nach oben** (`UEBERGABE.md` Abschnitt 3).
3. **Clip-Runde auf dem neuen Netz:** Aufrichten (NCBear_Rear) neu (ganzer Koerper, kein Kragen, bleibt 3,0 s); Lefzen beim Bruellen; **Sitzen Richtung (b) ist mit 2c ERLEDIGT**
   (aufrecht, Hinterbeine weniger gespreizt, keine schwarzen Sohlen-Flecken zur Seite), Hinsetzen/Aufstehen nachziehen.
4. **B5a Gegenwehr:** Zombies beissen den Baeren (Weg 2 aus `begleiter/angriff_fazit.md`, Engine laesst sie nicht selbst angreifen:
   Probe 08.11. abends, Zombie bleibt bei 0,24 Kacheln ohne Ziel stehen), feindliche Banditen greifen ihn an.
   **Kevins Ja 08.11.: zu Beginn umbenennen** -- Art `ncbear`, NPC-Crew-Namen (`BanditsNPCBear*`, Module
   `BanditsNPC.Bear`, Texte `UI_BN_Bear_*`), Testhilfen nur in `NCBearBench*` (dorthin auch `NCBear_Fight`, `NCBear_Tune`,
   `NCBear_FightInfo` und die Testteile mit Marke TESTSCHNITTSTELLE), sonst waechst die Umbenennung mit jeder neuen Datei.
5. **B1 + Baby finden + zaehmen:** Wachsen und Groessen (Jungtier 0,35 / Halbstark 0,75 / Erwachsen 1,35, ~7 + 14 Spieltage,
   Sandbox-Tempo, Fuettern beschleunigt, Hunger bremst) -- das Baby braucht diese Stufen; Jungtier im Wald finden (Koeder) statt spawnen;
   Zaehmen und Besitz (Teil von B2a: Register beim Server, Spiegel am Tier) **mit Zaehm-Balken** (Fortschritt sichtbar). `baer_uebernahme.py` nach Vorbild
   `../turret/tools/turret_uebernahme.py` MIT Cheat-Pruefung spaetestens hier.
6. **Befehle und Fenster:** Folgen, Bleiben, Sitz, Frei herumlaufen in der Basisflaeche, Komm her; Passiv; Unstuck. **Fenster mit V** wie das
   NPC-Gespraech (Naht mit `BanditsNPCInteract.lua`, ENTSCHEIDUNGEN.md unten), Rechtsklick-Menue. **Namensschild ueber dem Baeren**, dazu **Lebensbalken** (links nach rechts) und auf Wunsch Hunger/Durst-Balken, alles im Menue einzeln abschaltbar.
   Spur fuer 'Komm her' (Kevin 08.11. abends: der Baer laeuft beim Rufen mit Q weg): die Engine laesst ein Tier bei einem Ruf
   (Spieler-callOut) mit Akzeptanz >= 40 ZUM Spieler laufen, sonst flieht es (Jar IsoAnimal.respondToSound Offset 156-210,
   `_arbeit/baer_angriff/IsoAnimal.txt`). Vanilla setzt Akzeptanz nur im Debug (`setDebugAcceptance`, ISAnimalContextMenu.lua:614) -- Cheat-Weg,
   fuer das fertige Spiel einen echten Weg suchen.
7. **Beduerfnisse:** Fressen/Trinken skaliert je Stufe (Futter 1/2/4, Wasser 1/2/3), Leben 40/150/400, Level +50 % Leben, Downed mit Aufhelfen
   und allein nach 12 h, Unsterblich-Schalter in der Sandbox.
8. **Inventar:** 10/40/100 kg, Packtaschen +50, Sandbox-Faktor.
9. **Fischen** (spaeter): ab Halbstark schlecht, erwachsen besser; faengt am See/Fluss, legt in SEIN Inventar, frisst selbst.
10. **Mehrspieler** offen (heute ist MP im Test aus, der Befehl sagt es).
11. Kleine Reste: auf Kevins Wort Wegschleudern auch bei Treffern von der Seite/von hinten (heute fliegt nur, wer den Baeren ansieht);
    Sit/Stand/Eat waehlen den naechsten passenden Baeren; `slamReach` 1,2 ausprobieren; **offene Tuer** sperrt den Knockback-Flug oder nicht
    (gebaut: nur geschlossene sperrt); Spruenge beim Treffer im Sitzen und beim Fressbeginn (`spiel/anim_fix.md` 'Unsicher, offen',
    `spiel/anim_review_gegen.md`, `spiel/kampf_fix.md`); `NCBear_Stand` sagte einmal "rest", 3 s nachdem sich ein Baer selbst setzte
    (`NCBear_FightInfo()` neben dem sitzenden Baeren lesen).
12. **Neu 09.11. (Kevin): Schlafen** -- Schlaf-Animation (Hinlegen, Schlafen, Aufwachen), z Z z ueber dem schlafenden Baeren, leiser
    Schlafton (nur freie Aufnahme, Download je Datei auf Kevins Ja), **Baerenbett** passend fuer den Erwachsenen (1,35), spaeter **Schlafen wie
    die NPCs**. Forschungslauf `baer-schlaf` FERTIG 09.11. (8 Agenten, nichts gebaut/geladen): `begleiter/SCHLAF_PLAN.md`, Berichte
    `spiel/schlaf_forschung_*.md`. Kern: Haltung Sphinx, Engine-Ruheplatz `idleAction = sit` mit den freien Clipnamen DeerStag_IdleToSitting/
    SittingIdle/SittingToStanding; kein freier Schlafton gefunden (nichts laden, vorerst ohne Ton); Bett als 3D-Bodengegenstand ~2,5 x 1,6
    Kacheln mit Rezept. **Kevins Fragen K1-K21 offen** (Abschnitt 7). ENTSCHEIDUNGEN.md ganz unten.
13. **Nebenfund fuer NPC Crew (statisch, nicht gespielt):** eine Bandit-Kugel, die ein Tier trifft, beschaedigt im Einzelspieler den Spieler --
   erst messen; gehoert in die NPC-Crew-Sitzung, nicht hier bauen.

## Regeln (aus ../CLAUDE.md, kurz)
Je Version ein Workflow (Plan, Bau, Pruefer, Nachbesserung, Gegenpruefer, Integrator), hoechstens 10 Agenten je Workflow. Renders auf der
4090, auch bei laufendem Spiel (Kevin 09.11.); nie in eine Test-Mod kopieren, mit der er gerade spielt. Downloads nur mit Dateiname, Quelle, Groesse und Kevins Ja je Datei. Nichts aus fremden Mods kopieren.
Nach jeder fertigen Version: `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, dann commit + `git push` in beiden Repos.
