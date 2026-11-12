# Test: neues Generator-Junges neben dem Standard-Jungen (Lauf baer-gen-junges-v2) -- nur Einzelspieler

Statisch geprueft, nicht gespielt. Nur Testhilfe (kommt nie nach NPC Crew). Eingebaut 12.11. 17:17 (NCBearTest 99e0368).
Bild zum Ansehen vorher: `C:\Users\Kevin\NPCCrew-Nebenprojekte\_arbeit\baer_gen_junges\v2\bilder\KEVIN_gen_junges_v2.png` (nur lokal, Foto C drin).
(`beine.png` / `gesicht.png` daneben zeigen Zwischenstaende VOR der Nachbesserung.)

**Deine Frage "laeuft das andere baby anders?"** Das alte Generator-Junge: ja -- es trabte mit Erwachsenen-Beinen im dreifachen Takt
(1,60 Kacheln/s, "Giraffe"). Das neue geht im Baerenschritt wie das Standard-Junge, mit doppelt so vielen, halb so langen Schritten;
die Pfoten bleiben stehen. Es ist deutlich langsamer: Gehen 0,34 statt 0,52 Kacheln/s (rund ein Drittel), Rennen 2,25 statt 2,47
(gemessen am Modell; das Standard-Junge ist schneller, weil seine Pfoten dabei gleiten). Im Spiel noch nicht gesehen.

1. Spiel NEU starten (mit -debug), Wegwerf-Spielstand laden (oder vorher speichern), draussen auf offener Wiese stehen.
2. Lua-Konsole, eine Zeile:

   `NCBear_CubGen()`

   -> 2 Kacheln vor dir: **links das Standard-Junge, rechts das neue**, beide Groesse 0,35, Blick zu dir. Sie gehen ab und zu von selbst ein Stueck.
3. Ansehen (deine normale Kamera, dann einmal herumgehen):
   - Beine kurz statt Stelzen, Bauch naeher am Boden? (Von vorn sieht man die Vorderbeine noch mehr als beim Standard-Jungen.)
   - Baerenfuesse wie beim Standard-Jungen (dunkle Sohle, Krallen)?
   - Gesicht: grosse helle Schnauze, Kopf nicht gesenkt, Augen dunkel, Ohren rund? Suess genug?
   - Gang: tapsiger Baerenschritt, Pfoten rutschen nicht, nichts schwebt? Zu langsam neben dem Standard-Jungen?
4. Groesse (optional): `NCBear_CubGenSize(0.5)` = beide auf 0,5 (geht 0,35 bis 0,75).
   Das neue ist bei gleicher Groesse kuerzer (Modell 1,51 m gegen 1,86 m); gleich lang: `NCBear_CubGenSize(0.43, 0.35)`.
5. Zum Schluss `NCBear_CubGenClean()` und speichern. Die Vergleichs-Jungen nicht toeten (ein gespeichertes Vergleichs-Junges oder
   seine Leiche braucht die Testhilfe beim Laden). Dein eigenes Junges fassen die drei Befehle nie an.

Nicht im Test: Sitzen, Liegen und Fressen des neuen Jungen per Befehl gibt es noch nicht (nur im Bild) -- sag Bescheid, wenn du das im Spiel sehen willst.

Fragen an dich danach:
- Gehen so lassen (ruhig, 0,34) oder schneller? Die Variante "3 Schritte je Clip" (0,51 Kacheln/s) hat denselben schnellen Takt wie das alte
  Giraffen-Junge, nur mit kurzen Schritten; sie ist nur ein Vergleich vom Zwischenstand, nicht nachgebessert.
- Vorderbeine von vorn: stoert es dich, dass man sie unter dem Kopf mehr sieht als beim Standard-Jungen?
- Nase so gross lassen? Augen so gross lassen?
- Liegen: es liegt auf dem Ruecken (Pfoten oben), das Standard-Junge auf der Seite -- so lassen?
- Soll das neue Junge spaeter (Aussehen-Knopf) gleich lang sein wie das Standard-Junge?
