# Baer -- Stand und alles, was ansteht (08.11.2026 abends)

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
2. **Lauf baer-fell** (Kevins Startwort 08.11.): Hautdehnung Achsel/Brustunterseite (>3-fach), Fell "wie Hubbel" (Netz, Textur 2048,
   Zotteln statt Beulen, Alpha-Haarkarten pruefen), **echte Sohlen mit Ballen** (Vorlage `begleiter/kevin_pfotenvorlage.png`, nur ansehen)
   und **ausgearbeitete Unterseite** (Bauch, Brust, Achseln, Innenbeine, Kehle; Spielbild `begleiter/kevin_rear_unterseite.webp`).
3. **Clip-Runde auf dem neuen Netz:** Aufrichten (NCBear_Rear) neu (ganzer Koerper, kein Kragen, bleibt 3,0 s); **Sitzen Richtung (b)**
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
12. **Nebenfund fuer NPC Crew (statisch, nicht gespielt):** eine Bandit-Kugel, die ein Tier trifft, beschaedigt im Einzelspieler den Spieler --
   erst messen; gehoert in die NPC-Crew-Sitzung, nicht hier bauen.

## Regeln (aus ../CLAUDE.md, kurz)
Je Version ein Workflow (Plan, Bau, Pruefer, Nachbesserung, Gegenpruefer, Integrator), hoechstens 10 Agenten je Workflow. Renders auf der
4090, nie waehrend Kevin spielt. Downloads nur mit Dateiname, Quelle, Groesse und Kevins Ja je Datei. Nichts aus fremden Mods kopieren.
Nach jeder fertigen Version: `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, dann commit + `git push` in beiden Repos.
