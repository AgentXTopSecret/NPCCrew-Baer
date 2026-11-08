1. **Neuer Wegwerf-Spielstand**, nur fuer den Baeren, danach nie ohne NCBearTest laden: ein gespeicherter Baer oder eine Baerenleiche ohne die Mod wirft beim Laden bzw. Zeichnen. Nicht in eine Tierzone von NPC Crew stellen.
2. Im Spielstand die Mod **NCBearTest** aktivieren, Spiel neu starten (mit -debug wie immer). Nur Einzelspieler.
3. Rechtsklick auf den Boden, **"NC Bear"**, **"Spawn living bear here"**. Das stehende Modell und seine drei Menuepunkte bleiben wie bisher.
4. Sehen sollst du: er steht, laeuft ab und zu gemaechlich ein Stueck herum, flieht nicht vor dir oder Zombies, greift nie an. Ein Schuss in der Naehe oder ein Treffer laesst ihn wegrennen. Toeten: Hammer oder Metallrohr im Inventar, Rechtsklick auf ihn, "Kill Animal"; Zerlegen gibt Rehteile (Attrappe).
5. **Rueckfall** "Spawn living bear (deer motion)": dasselbe Fell auf dem Rehskelett mit Rehbewegung, sieht aus wie ein Reh im Baerenfell. Nimm ihn, wenn der eigene nicht erscheint, auf der Stelle laeuft oder verzerrt ist. "Remove living bears nearby" raeumt nur lebende in 12 Kacheln, keine Leichen.
6. Groesse nachstellen in der Debug-Konsole: `b = NCBear_SpawnLive()` und dann `b:getData():setSizeForced(1.2)` (jetzt 1.0; gilt, bis er einen Spieltag aelter wird).
7. Sag mir: erscheint er, laeuft er vorwaerts mit sauberen Beinen, passen Groesse und Farbe, Sturz und Leiche ok, rote Fehler ja/nein. console.txt lese ich selbst.
8. Statisch geprueft und offline gemessen, nicht gespielt.
