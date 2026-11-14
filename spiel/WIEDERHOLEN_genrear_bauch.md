# WIEDERHOLEN.md -- Lauf baer-gen-rear-bauch: Aenderungen mit EINEM Befehl je Teil wieder aufsetzen

Wozu: spaetere Modell-Laeufe (Maul, Schlafpose, Prankenhieb) ersetzen NCBearGen.glb bzw. NCBear.png; danach setzt je Teil ein Befehl die
Aenderung dieses Laufs wieder auf. Pfade relativ zu `C:/Users/Kevin/NPCCrew-Nebenprojekte`. `EIN` = Ordner der geltenden Dateien (heute die
Test-Mod `C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media`, wird nur gelesen). Statisch gerechnet, nicht gespielt.
Je Bauer ein Abschnitt (A Generator-Rear, B Bauch-Fell).

**`<AUS>` (Nachbesserung 14.11., Befund T2):** der Ausgabe-Ordner des Laufs, der den Befehl ausfuehrt, z. B. `_arbeit/baer_<neuer_lauf>/out`.
**Nie** `_arbeit/baer_modell_1114/...` einsetzen -- das ueberschreibt Ergebnis, Berichte und `out/md5.txt` dieses Laufs. Berichte (`--bericht`)
ebenfalls unter `<AUS>` (oder weglassen). Alle Python-Aufrufe mit `python -B` (kein `__pycache__` in `baer/spiel`, Befund T9b).
Dieser Lauf selbst hatte `<AUS>` = `_arbeit/baer_modell_1114/out` (Berichte in `gen_rear/`, `bauch/`); der Nachbau der Nachbesserung liegt in
`nachbesserung/wdh/a|b` (byte-gleich, `NACHBESSERUNG.md`).

## A -- Generator-Baer bekommt das neue Aufrichten/Bruellen (NCBearGen.glb, nur Clip NCBear_Rear)

Bauer A, 14.11.2026. Skript `baer/spiel/baer_genrear_1114.py` (Python 3 + numpy, importiert `baer/spiel/baer_kern_liegen.py` aus demselben Ordner;
kein Blender, nichts aus `_arbeit/`). Bericht und Bilder: `_arbeit/baer_modell_1114/BAU_A.md`, `bilder/a_*.png`. (Der PLAN nannte das Skript
`baer_rear_gen_1114.py` -- es gibt nur `baer_genrear_1114.py`.)

```
python -B baer/spiel/baer_genrear_1114.py EIN/models_X/Skinned/NCBear.glb EIN/models_X/Skinned/NCBearGen.glb <AUS>/42/media/models_X/Skinned/NCBearGen.glb --arm 14,8 --bericht <AUS>/bericht_a.json
```

* Was es tut: schreibt die Rear-Werte des Klassisch-GLB an Ort und Stelle ins BIN des Generator-GLB (JSON byte-gleich), dreht dann NUR die
  Oberarme (Bip01_L/R_UpperArm) 14 Grad weiter vor und 8 Grad weiter aus (weich 0,30-0,55 s ein, 2,25-2,45 s aus; Bild 0..8 und 74..90 bit-gleich
  zum Klassisch-Clip), damit die Unterarme am dickeren Generator-Netz nicht in der Brust stecken. Ohne `--arm` gilt dieselbe Vorgabe 14,8.
* Dauer ~25 s (Abnahme an allen 91 Bildern in bis zu 24 Prozessen; `--jobs N` begrenzt).
* Ende gut: `REAR_GEN_OK MD5 <md5> <datei>`, Code 0. Mit den heutigen Eingaengen (NCBear.glb dc50d350..., NCBearGen.glb 867b558b...) kommt genau
  heraus: **NCBearGen.glb 8fe4012533a6467d716f57dd617db4cc** (1 267 904 Bytes, gleiche Laenge wie der Eingang).
* Ende schlecht: `REAR_GEN_FEHLER ...`, Code 2, nichts geschrieben (Eingang fehlt -- seit der Nachbesserung, T10 --, Skelett/Rear-Zeiten
  verschieden, Rear-Ausgabe mit anderem Clip geteilt, Selbstpruefung oder Abnahme A3/A4 verletzt). Schreibt nie auf einen Eingang und nie in
  `.../Zomboid/mods/...` oder `.../steamapps/...`.
* Zweimal gebaut = gleiche MD5, auch auf dem eigenen Ergebnis als Generator-Eingang (`gen_rear/bau/zweimal_a|b`, beide 8fe40125; Nachbesserung
  `nachbesserung/wdh/a`, 8fe40125).
* Voraussetzungen fuer einen spaeteren Lauf: gleiches Skelett (Namen, Eltern, Ruhe-TRS, inverse Bind) und gleiche Rear-Abtastzeiten in beiden GLB;
  der Maul-Lauf darf andere Clips von NCBearGen.glb aendern -- Rear wird hier nur an seinen eigenen Accessoren angefasst (das Skript prueft, dass
  kein anderer Clip sie mitbenutzt). Aendert ein spaeterer Lauf den Klassisch-Rear, uebernimmt dieser Befehl dessen neue Fassung; dann die
  Arm-Drehung neu rastern: `python -B baer/spiel/baer_genrear_1114.py --scan EIN/models_X/Skinned/NCBear.glb EIN/models_X/Skinned/NCBearGen.glb 12,14,16,18 6,8,10,12`.
* Beweis "nur Rear": `python -B baer/spiel/baer_genrear_1114.py --pruefe EIN/models_X/Skinned/NCBear.glb EIN/models_X/Skinned/NCBearGen.glb <AUS>/42/media/models_X/Skinned/NCBearGen.glb`
  (JSON byte-gleich, 0 Bytes ausserhalb der Rear-Ausgaben, andere Clips 2184/2184 Sampler-Puffer gleich, Rear = Klassisch ausser UpperArm).
  Importer des Spiels: `bash _arbeit/baer_modell_1114/werkzeug/dump.sh <AUS>/42/media/models_X/Skinned/NCBearGen.glb <AUS>/neu.txt` und
  `python -B _arbeit/baer_2c/werkzeug/pruef/glb_pruef.py <alt.txt> <AUS>/neu.txt` -> 14 Clips Abweichung 0, Rear 3,0000 s 91/91.
* **Schild-Tabelle gehoert zum Einbau (Befund T3; F6, Vorgabe ja):** `tagpose_schirm.py` LIEST keine Lua-Datei -- das **erste Argument ist die
  AUSGABE** und wird komplett neu geschrieben (`write(sys.argv[1], ...)`, `_arbeit/baer_zaehmen/k1/werkzeug_nach/tagpose_schirm.py:146`). Darum
  erst nach `<AUS>` schreiben, dann vergleichen; nie direkt in die Test-Mod oder nach NPC Crew:
  ```
  python -B _arbeit/baer_zaehmen/k1/werkzeug_nach/tagpose_schirm.py <AUS>/BanditsNPCBearTagPose.lua cub=EIN/models_X/Skinned/NCBearCub.glb cubgen=EIN/models_X/Skinned/NCBearCubGen.glb big=EIN/models_X/Skinned/NCBear.glb biggen=<AUS>/42/media/models_X/Skinned/NCBearGen.glb
  diff EIN/lua/shared/BanditsNPCBearTagPose.lua <AUS>/BanditsNPCBearTagPose.lua
  ```
  (Nicht `python -I`, wie es der Kopf von tagpose_schirm.py nennt: `-I` blendet hier die Benutzer-Pakete aus -> `No module named 'numpy'`.)
  Erwartet heute: genau **Zeile 62** (`biggen.rear`, max 1,56 -> 1,61) anders. Ergebnis dieses Laufs `gen_rear/mess/tagpose_v1.lua`
  (MD5 0a8c61e76fd5dc23ec4e6af456f04bd3; in der Nachbesserung mit genau diesem Befehl nachgebaut, byte-gleich). NCBearGen.glb und diese Zeile
  **nur zusammen** einbauen -- ohne die Zeile haengt das Schild beim Generator-Baeren im Bruellen zu tief (Kevins K1-Klage).

`out/md5.txt` (Zeile fuer A):
```
8fe4012533a6467d716f57dd617db4cc  42/media/models_X/Skinned/NCBearGen.glb
```

## B -- Bauch-Fell am Klassisch-Baeren (textures/Body/NCBear.png, nur Bauch/Brust/Innenschenkel)

Bauer B, 14.11.2026. Skript `baer/spiel/baer_bauch_1114.py` (Python 3 + numpy + PIL, eigenstaendig: importiert nichts aus `baer/spiel/` oder
`_arbeit/`; kein Blender). Bericht und Bilder: `_arbeit/baer_modell_1114/BAU_B.md`, `bilder/b_*.png`, Arbeitsdaten `bauch/`. (Der PLAN nannte
das Skript `baer_bauchfell_1114.py` -- es gibt nur `baer_bauch_1114.py`.)

```
python -B baer/spiel/baer_bauch_1114.py EIN/models_X/Skinned/NCBear.glb EIN/textures/Body/NCBear.png <AUS>/42/media/textures/Body/NCBear.png --bericht <AUS>/bau_bericht_b.json
```

* Was es tut: Maske Bauch/Brust/Innenschenkel aus dem Netz (Formeln wie PLAN 3.1), Kopf/Kiefer/Pfoten/Schwanz-Inseln gesperrt (bit-gleich);
  dort Feinanteil (Matsch) durch Fell ersetzt (Rueckenfell derselben Textur in 3D entlang der Wuchsrichtung getupft), Grobfarbe in 3D wie heute;
  alles in 3D gerechnet -> stetig ueber UV-Naehte. Nur Texel mit Maske > 0 und das Rand-Polster daneben aendern sich.
* Dauer ~50 s (eine CPU-Kette). Fester Samen: zweimal = gleiche MD5.
* Ende gut: `BAUCHFELL_OK MD5 <md5> (...) -> <datei>`, Code 0. Mit den heutigen Eingaengen (NCBear.glb dc50d350..., NCBear.png 5a841f0c...)
  kommt genau heraus: **NCBear.png 3493a5e6556e3b9b04a7e527b1608911** (1024 x 1024 RGB 8 bit, Zusatz-Bloecke sRGB/gAMA/cHRM/eXIf/oFFs/pHYs
  byte-gleich zur alten Datei).
* Wieder aufsetzen: das Skript erkennt am Fingerabdruck des Maskenbereichs, ob er noch ALT (ce05d378) oder schon NEU (a233e1be) ist.
  Schon NEU -> `BAUCHFELL_SCHON`, Eingang unveraendert nach `<AUS>` (Code 0, dann ohne `--bericht`-Datei; ein Maul-/Schlaf-Lauf kann den Befehl
  also gefahrlos immer laufen lassen). Weder ALT noch NEU (jemand hat den Bauch anders bemalt) -> `BAUCHFELL_FEHLER`, Code 2, nichts geschrieben; `--trotzdem` rechnet dennoch.
  Aendert ein spaeterer Lauf nur ANDERE Stellen der Textur (z. B. Gesicht), bleibt der Fingerabdruck gueltig und der Befehl setzt den Bauch auf.
* Ende schlecht: `BAUCHFELL_FEHLER ...`, Code 2, nichts geschrieben: Eingang fehlt oder Textur unlesbar (seit der Nachbesserung, T10), Netz/UV
  anders als dc50d350 (11 914 Punkte, 59 430 Indizes, UV-MD5 5e392a66; dann muss die Maske neu gerechnet werden -- Clips duerfen sich aendern,
  sie werden nicht gelesen), Textur nicht 1024x1024 RGB, Aenderung ausserhalb der Maske oder in einer gesperrten Insel, PNG-Rueckleseprobe weicht
  ab. Schreibt nie auf einen Eingang und nie in `.../Zomboid/mods/...` oder `.../steamapps/...`; erst `.tmp`, dann umbenennen.
* Beweis "nur Maske" und Masse B1-B5: `python -B _arbeit/baer_modell_1114/bauch/werkzeug/abnahme_b.py EIN/models_X/Skinned/NCBear.glb
  EIN/textures/Body/NCBear.png <AUS>/42/media/textures/Body/NCBear.png <AUS>/abn_b` -> `<AUS>/abn_b.txt/.json` und Pixel-Diff-Bild
  `<AUS>/abn_b_diff.png` (abnahme_b.py schreibt seit der Nachbesserung auch ohne `-B` keinen Cache nach `baer/spiel`).
  Bilder: `bauch/werkzeug/auftrag_b.py` (Saetze nah/kevin/folge/gross) + `werkzeug/gpu_render.sh werkzeug/render_1114.py ...`,
  Blaetter `bauch/werkzeug/bilder_b.py`, Kantensuche im Render `bauch/werkzeug/kanten_render.py` (Ausgaben ebenfalls unter `<AUS>` legen).
* Nicht beruehrt: `NCBearGen.png`, `NCBearGenFoto.png`, die Jungen, `textures/WorldItems/NCBear.png` (Bodenmodell, PLAN F5), alle GLB.
* Hinweis (T11): die alte Werkbank-Art `bearstag` (`shared/NCBearBenchDefs.lua:104`, Modell `NCBearDeer.glb`, andere UV) zeichnet mit derselben
  Textur -- dort liegt das neue Fell an anderen Stellen. Nur Werkbank, geht nie nach NPC Crew; war bei jedem Textur-Lauf so.

`out/md5.txt` (Zeile fuer B):
```
3493a5e6556e3b9b04a7e527b1608911  42/media/textures/Body/NCBear.png
```
