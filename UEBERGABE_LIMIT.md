> **ERLEDIGT 10.11.2026 10:45:** Lauf 2c ist ohne Stopp fertig geworden und in NCBearTest (STAND.md oben). Nur noch Geschichte.

# Baer -- Uebergabe fuer einen anderen Account (vorbereitet 10.11.2026 ~05:20, wird beim Stopp aktualisiert)

Kevins Regel (10.11. ~01:30-02:00, in der NPC-Crew-Hauptsitzung, von dort uebermittelt): *"wenn die alle durch sind oder das wochenlimit bei
98% angekommen ist egal wie weit grad der workflow ist es werd auch immer weiter gearbeitet ueberall ... und wen nda 98% ist dann soll jeder
worfklow sofort beendet und gespeichert werden der aktuelle stand und alles an die uebergabe uebermittelt werden das ein anderer account da
weiter machen kann"*. Die Hauptsitzung ueberwacht das Wochenlimit und schickt bei 98 % das Stopp-Signal.

Zuerst `../CLAUDE.md`, dann `STAND.md` (oben die Eintraege vom 10.11.), dann `begleiter/ENTSCHEIDUNGEN.md` (ganz unten Kevins Spieltest vom 10.11.).

## Lauf 2c (laeuft bzw. lief zuletzt)
- Arbeitsordner `../_arbeit/baer_2c/`, Skript des Laufs `workflow_baer_2c_v3.js` (alle Auftraege, Regeln, Pfade; CTX + NEU-Block C1-C5).
- **Resume per `resumeFromRunId` geht NUR in der Sitzung, die den Lauf gestartet hat.** Ein anderer Account baut ein Fortsetzungs-Skript:
  dieselben Auftraege ab der ersten Stufe, deren Bericht fehlt; statt der Kurzfassungen aus dem Zwischenspeicher die Berichte von der Platte
  einsetzen (`SPEZ_2C.md`, `bau_koerper.md`, `bau_sitzen.md`, `bau_gebiss.md`, `bau_textur.md`, `pruef_bericht.md`, `fix1_bericht.md`).
  Rueckgabewerte aller fertigen Agenten stehen auch im Journal dieser Sitzung (Pfad unten), falls lesbar.
- Reihenfolge: Forschung (2, fertig) -> Spezifikation (fertig) -> Bau Koerper (fertig) -> Bau Sitzen -> Bau Gebiss -> Textur -> Pruefer ->
  Nachbesserung -> Gegenpruefer. Danach Integrator: selbst pruefen (Dump.java, Clips, Bilder), nur wenn Kevin nicht spielt in NCBearTest
  kopieren (Zip vorher/nachher nach `Zomboid/backups/NCBearTest/`), `sichern.py`, Commit + Push beider Repos.
- Skriptkopien `spiel/*_2c.py` (Originale `*_pfote.py` nie aendern). Bau Sitzen musste einmal neu starten; Halbstand des ersten Versuchs:
  `../_arbeit/baer_2c/sitzen/abgebrochen_baer_kampf_2c_0431.py`.
- Journal (nur diese Sitzung): `C:/Users/Kevin/.claude/projects/C--Users-Kevin-NPCCrew-Nebenprojekte-baer/8f80868b-c5cd-4de5-ade1-25f74fc113d4/subagents/workflows/wf_966982af-cb0/journal.jsonl`

## Lauf baer-baby (fertig, Entwurf)
- `../_arbeit/baer_baby/` (`fix_baby.md` zuerst), Blatt `bilder/kevin_baby_entwurf.png` an Kevin gezeigt. Kevins Antworten offen (Augen groesser?
  Rumpf kuerzer? Schrittweite 0,777/1,0? Halbstark-Modell?). Kommt mit B1 ins Spiel (eigene Tierart `bearcub` -> `bear`).

## Nichts in NCBearTest seit f1ab881 (baer-pfoten). Nichts committet seit 99971a4 (Unterlagen).
