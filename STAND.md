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
- Lauf baer-anim (08.11., 10 Agenten) fertig, in NCBearTest kopiert, **ungespielt**. Kevin hat Videos und `spiel/anim_sitzen_vergleich.png`.
- Kevins letzter Test (08.11. ~03:00, Stand baer-kampf): Umwerfen klappt; "sofort tot" kam vom Debug-Spawn (Leben 1,0) -> Schieber auf 2,0
  oder `NCBear_ZHealth(2, 10)`.

## Offen -- in dieser Reihenfolge besprechen/bauen
1. **Kevins Test des baer-anim-Stands** (`spiel/anleitung_anim.md`). Dazu seine Wahl **Sitzen (a) oder (b)** (Vergleichsbild; (a) ist gebaut,
   breitbeinig und plump, nicht sein Bild; (b) aufrecht, naeher an der Vorlage) -- oder beide nochmal. Und: **offene Tuer** sperrt den
   Knockback-Flug oder nicht (gebaut: nur geschlossene sperrt).
2. **Aufrichten (NCBear_Rear) neu** -- noch der alte Clip, harter Kragen ueber den Armen (Kevin: bleibt 3,0 s, nur schoener, ganzer Koerper).
3. **Hautdehnung Achsel/Brustunterseite** (>3-fach) und Fell "wie Hubbel" -> Lauf **baer-fell** (Netz, Textur 2048, Zotteln statt Beulen,
   Alpha-Haarkarten pruefen). Kevin hat das Startwort dafuer am 08.11. gegeben.
4. **B1:** Wachsen und Groessen (Jungtier 0,35 / Halbstark 0,75 / Erwachsen 1,35, ~7 + 14 Spieltage, Sandbox-Tempo, Fuettern beschleunigt,
   Hunger bremst), Art umbenennen nach `ncbear`, NPC-Crew-Namen (`BanditsNPCBear*`, Module `BanditsNPC.Bear`, Texte `UI_BN_Bear_*`),
   Testhilfen nur in `NCBearBench*` (dorthin ziehen auch `NCBear_Fight`, `NCBear_Tune`, `NCBear_FightInfo` und die Testteile ohne Marke
   TESTSCHNITTSTELLE), `baer_uebernahme.py` nach Vorbild `../turret/tools/turret_uebernahme.py` MIT Cheat-Pruefung.
5. **B5a:** Zombies beissen den Baeren (Weg 2 aus `begleiter/angriff_fazit.md`), Gegner wehren sich.
6. **Befehle:** Folgen, Bleiben, Sitz, Frei herumlaufen in der Basisflaeche, Komm her; Passiv; Unstuck.
7. **Beduerfnisse:** Fressen/Trinken skaliert je Stufe (Futter 1/2/4, Wasser 1/2/3), Leben 40/150/400, Level +50 % Leben, Downed mit Aufhelfen
   und allein nach 12 h, Unsterblich-Schalter in der Sandbox.
8. **Bekommen:** Jungtier im Wald finden (Koeder) statt spawnen.
9. **Inventar:** 10/40/100 kg, Packtaschen +50, Sandbox-Faktor.
10. **Fischen** (spaeter): ab Halbstark schlecht, erwachsen besser; faengt am See/Fluss, legt in SEIN Inventar, frisst selbst.
11. **Mehrspieler** offen (heute ist MP im Test aus, der Befehl sagt es).
12. Kleine Reste: `slamReach` 1,2 ausprobieren, nur frontal Getroffene fliegen (gewollt?), Spruenge beim Treffer im Sitzen und beim Fressbeginn
    (`spiel/anim_fix.md` 'Unsicher, offen', `spiel/anim_review_gegen.md`, `spiel/kampf_fix.md`).
13. **Nebenfund fuer NPC Crew (statisch, nicht gespielt):** eine Bandit-Kugel, die ein Tier trifft, beschaedigt im Einzelspieler den Spieler --
   erst messen; gehoert in die NPC-Crew-Sitzung, nicht hier bauen.

## Regeln (aus ../CLAUDE.md, kurz)
Je Version ein Workflow (Plan, Bau, Pruefer, Nachbesserung, Gegenpruefer, Integrator), hoechstens 10 Agenten je Workflow. Renders auf der
4090, nie waehrend Kevin spielt. Downloads nur mit Dateiname, Quelle, Groesse und Kevins Ja je Datei. Nichts aus fremden Mods kopieren.
Nach jeder fertigen Version: `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, dann commit + `git push` in beiden Repos.
