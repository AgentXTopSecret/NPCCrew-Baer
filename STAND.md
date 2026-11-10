# Baer -- Stand und alles, was ansteht (10.11.2026 11:00)

> **Neuer Account oder neue Sitzung? Zuerst `UEBERGABE.md` (10.11. ~11:00): wo wir stehen, was Kevin testen muss, offene Fragen, was als Naechstes kommt.**

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
