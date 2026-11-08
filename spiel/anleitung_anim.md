1. **Spiel neu starten** (mit -debug, Einzelspieler, Wegwerf-Spielstand): Clips, Toene und Lua gibt es erst danach. Rechtsklick auf den Boden, "NC Bear", "Spawn living bear here".
2. Zombies ueber Debug, **Horde Manager**, vorher den Leben-Schieber auf **2,0** stellen (Vorgabe 1,0 = jeder Hieb toetet), oder danach `NCBear_ZHealth(2, 10)`; du selbst 10+ Kacheln weg.
3. Sehen: Hieb links/rechts, Biss gegen Stehende, Biss am Boden und Doppelschlag **im Wechsel**, Koerper und Hinterbeine arbeiten mit; ein Zombie stirbt nach etwa **2-3 Hieben**. **Knockback fliegt nur, wer ihn von vorn ansieht**, seitlich und von hinten Getroffene fallen auf der Stelle.
4. Ruhe: `NCBear_Sit()`, `NCBear_Stand()`, `NCBear_Eat()`; Schnauben von selbst ab und zu und mit `NCBear_Huff()` (jetzt lauter). Sitzen ist Fassung (a), nicht ganz dein Bild; (b) siehst du in `anim_sitzen_vergleich.png` unten.
5. Offen: **Aufrichten ist noch das alte** (der Kragen ueber den Armen bleibt), Hautdehnung an der Achsel (braucht das Netz), offene Tuer laesst den Flug durch.
6. Sag mir: sieht der Hieb jetzt wie ein Baer aus, knickt noch ein Arm? Biss ok? Fliegen sie, wie weit? Schnauben hoerbar? Sitzen (a) oder (b)? Rote Fehler ja/nein; console.txt (`[NCBear]`, `***`) lese ich selbst.
7. Mehrspieler bleibt aus (der Befehl sagt es). Vorschau vorher: `anim_kampf_vorschau.mp4`, `anim_sitzen_vorschau.mp4`.
8. Statisch geprueft (Attrappe 300/0), nicht gespielt.
