## 8. Kevins Test (nach dem Einbau durch den Integrator)
1. Spiel NEU starten (mit -debug), einen Wegwerf-Spielstand laden, ruhige offene Wiese.
2. Konsole: `NCBear_GenLive()` -> links 2c, Mitte braun, rechts Fototon, alle schauen zu dir.
3. ~5 s warten, dann `NCBear_GenAct("sit", 30)`, danach `"rear"`, `"eat"`, `"bite"`, `"swipeL"`, `"slam"` -- alle drei machen mit.
4. `NCBear_GenRun()` zweimal (hin und zurueck) = Rennen von der Seite; zwischendurch gehen sie von selbst.
5. Achten auf: Aufrichten (schwarzes Band?), Fressen (Kopf von oben), heller Punkt an der Kehle, Farbe im Spiel-Licht.
6. Zum Schluss `NCBear_GenClean()`, den 2c per Rechtsklick "Remove living bears nearby" entfernen, speichern.

## 9. Dateien
- Blatt fuer Kevin: `R/bilder/KEVIN_gross_vergleich.png` (MD5 f83708d5; 2c | neu braun | neu Fototon; Stehen Spielkamera, Seite, Gehen,
  Sitzen, Aufrichten, Spielgroesse 101 px/m 2x; ohne fremde Fotos).
- Blaetter: `R/gegen/blaetter/` (z_* Vergleiche, n1..n6 Nahaufnahmen, g1..g10 alle Ansichten 2c | braun | Fototon | Ton | 2c Ton).
- Messungen: `R/gegen/g_mess.json` (+ `.log`), `g_topo.json`, `g_zwilling.json`, `g_form.json`, `g_naht_tex.json`; Dumps `dump_gen.txt`, `dump_2c.txt`.
- Skripte: `R/gegen/g_dump.py`, `g_glb.py`, `g_mess.py`, `g_topo.py`, `g_zwilling.py`, `g_form.py`, `g_kralle.py`, `g_durch.py`, `g_farbe.py`,
  `g_naht_tex.py`, `g_flecken.py`, `g_pick.py`, `g_posen.py`, `g_render.py`, `g_auftrag.py`, `g_auftrag2.py`, `g_blatt.py`, `g_zeig.py`,
  `g_kevin_blatt.py`, `g_gpu.sh`; Patch-Probe `R/gegen/m2probe/`.
- Nach dem Kopieren muss Kevin das Spiel neu starten (Lua und Modelle laden nur beim Start).
