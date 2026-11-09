> **ERLEDIGT 09.11.2026 ~14:20:** baer-fell fertig geprueft und in NCBearTest (STAND.md Punkt 2). Nur noch Geschichte.

# Baer -- Uebergabe an die naechste Sitzung (09.11.2026 ~00:40, Kevin wechselt den Claude-Account, Wochenlimit 96 %)

Zuerst `../CLAUDE.md`, dann `STAND.md`, dann `begleiter/ENTSCHEIDUNGEN.md` (ganz unten stehen Kevins Wuensche vom 08.11. abends).

## Wo es steht
- **Lauf baer-laerm FERTIG**, in NCBearTest kopiert, committed und gepusht (Test-Mod `main` 0d7f580, Unterlagen `unterlagen` 876900e).
  **Ungespielt.** Testanleitung fuer Kevin: `spiel/anleitung_laerm.md`. Berichte `spiel/laerm_*.md`.
- **Lauf baer-fell LAEUFT/ABGEBROCHEN** (Workflow der alten Sitzung, 9 Agenten; Resume geht NUR in der alten Sitzung). Alles liegt auf
  der Platte in `../_arbeit/baer_fell/`:
  - fertig: `forschung_bestand.md`, `forschung_engine.md`, `bau_netz.md` (+ `netz/uebergabe.md`), `baby/baby_vergleich.png` + `baby/bericht.md`
  - **auch fertig (09.11. 00:39): Textur-Bauer** (`bau_textur.md`, `textur/`, `mod/42/media/textures/`; Body bleibt 1024, Kopf-Variante B
    als eigene Datei). **Danach hat Claude den Lauf absichtlich gestoppt (Wochenlimit)** -- die Pruefer sind NICHT gelaufen
    (`pruef/` enthaelt nur Dumps des Netz-Bauers bzw. Anfaenge, nicht verwerten). Als Naechstes also Schritt 2 unten.
  - noch zu tun: Pruefer Optik + Technik (`pruef_optik.md`, `pruef_technik.md`), Nachbesserung
    (`fix_bericht.md`), Gegenpruefer (`gegen_bericht.md`, `bilder/kevin_vorher_nachher.png`)
  - Skript des Laufs (alle Auftraege, Regeln, Pfade): `../_arbeit/baer_fell/workflow_baer_fell.js`
  - Neue Skriptkopien in `spiel/`: `baer_quelle_fell.py`, `baer_export_fell.py`, `baer_kampf_fell.py` (ggf. `baer_textur_fell.py`)
- **NICHTS von baer-fell ist in NCBearTest.** Die Test-Mod hat noch das Modell aus baer-anim (GLB MD5 4cfe4f29...).

## So weitermachen
1. Netz (`bau_netz.md`) und Textur (`bau_textur.md`) sind fertig -- beide Berichte zuerst lesen.
2. Die fehlenden Stufen als NEUEN Workflow laufen lassen: Pruefer (Optik, Technik) -> Nachbesserung -> Gegenpruefer. Auftraege und den
   gemeinsamen Kontext (CTX, GPU-Regeln: nie rendern, wenn ProjectZomboid laeuft; Sperre `gpu.lock`) aus dem Skript uebernehmen.
   Hoechstens 10 Agenten je Workflow; vorher Verbrauch pruefen und Kevin die Zahl nennen.
3. Selbst nachpruefen (GLB mit `../_arbeit/baer_spiel/harness` Dump.java lesen, Clips bit-gleich, Kopf unveraendert, Bilder ansehen).
4. Nur wenn Kevin NICHT spielt: Test-Mod sichern (Zip nach `C:/Users/Kevin/Zomboid/backups/NCBearTest/`), nur die Mod-Dateien aus
   `../_arbeit/baer_fell/mod/` kopieren (nur hinzufuegen/ueberschreiben), byte-gleich pruefen, Zip danach.
5. `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, dann Commit + `git push` in der Test-Mod (`main`) und hier (`unterlagen`).
6. Kevin ein Vorher/Nachher-Bild zeigen und kurz sagen, was er testen soll (Spiel neu starten).

## Kevins offene Entscheidungen (fragen, nicht selbst entscheiden)
1. **Stress senken** nach Laerm-Fluchten mit `animal:changeStress(...)` (Vanilla `ISMilkAnimal.lua:28`)? Ab Stress 70 flieht ein Tier
   auch vor dem Spieler (statisch, `spiel/laerm_forschung_zustand.md`).
2. **`setShouldFollowWall(false)`** nur im Jar belegt (eiserne Regel: Kevins Wort je Methode) -- loest einen seltenen Fall.
3. **clockHit** (Treffer per Uhr bei Dauerlaerm): stoert es ihn im Spiel?
4. **Baby auftauchen/verschwinden** -- Vorschlag an Kevin (noch ohne Antwort): Zombies beissen nur einen GEZAEHMTEN Baeren (unser
   eigener Biss aus B5a; die Engine laesst Zombies Tiere nie angreifen), ein wildes Junges ist sicher; je Spieler hoechstens ein Baer und
   ein wildes Junges; Junges selten im Wald in Spielernaehe ausser Sicht (Sandbox-Haeufigkeit) plus Koederplatz (Honig/Fisch, 1-3
   Naechte); ungezaehmt und 1-2 Spieltage ohne Kontakt -> verschwindet; einmal gefuettert -> bleibt; nach Tod des eigenen Baeren neues
   Junges nach 7 Spieltagen.
5. **Augen/Gesicht:** Variante `../_arbeit/baer_fell/textur/NCBear_kopf_variante.png` (falls gebaut) gegen die alte -- Kevin waehlt.
6. **Eigenes Baby-Modell** noetig? Bild `../_arbeit/baer_fell/baby/baby_vergleich.png`, Bericht daneben.

## Danach (Reihenfolge, STAND.md)
Clip-Runde (Aufrichten neu, Sitzen Richtung b) -> B5a Gegenwehr (zuerst Umbenennen auf NPC-Crew-Namen) -> B1 + Baby finden und zaehmen
(Zaehm-Balken aus Futter und Streicheln) -> Befehle und Fenster (V-Taste, Namensschild, Balken je Spieler, Vertrauen/Laune) ->
Beduerfnisse, Inventar, Fischen, MP.
