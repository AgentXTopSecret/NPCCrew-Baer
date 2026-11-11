# Test: Baer B1e (Wechsel auf den grossen Baeren, groessere Markierung) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist. Danach Spiel **neu starten, mit -debug** (neue Tierart, neue Bilder und Lua laden nur beim Start).
- Mods an: **NCBearTest**. Bandits und NPC Crew duerfen an oder aus sein (die Markierung kommt seit B1e auch ohne Bandits).
- Im Debug-Menue den **"Tier Cheat" ausschalten** und am Baeren keine Debug-Tierknoepfe (Alter, "max size") benutzen.
- Befehle tippst du in die **Lua-Konsole** (Debug). Texte im Spiel sind englisch. Die Zahlen gelten fuer ein frisch gezaehmtes Junges (Tag 0).

**Teil A: Laden und Markierung oben**
1. Spielstand laden. Erwartet: keine roten Fehler. Hat der Spielstand noch dein ausgewachsenes Junges aus dem B1d-Test, wird es kurz nach dem
   Laden zum grossen Baeren in voller Groesse -- das ist gewollt (ein Tier, gleicher Name). Danach geht es mit einem frischen Jungen weiter.
2. Draussen: `NCBear_CubClean()` (raeumt ALLE Baeren weg), dann `NCBear_CubHere(30)`.
   Erwartet oben in der Mitte: der orange Kreis mit Baerenkopf, Pfeil zum Jungen, Text "Bear cub nearby" -- bei deinem 4K-Bild **etwa doppelt
   so gross** wie bisher, der Kreis gut zu sehen.
3. Esc > Optionen > **Mods** > "NPC Crew: Bear" > **"Size of the cub marker at the top of the screen"**: nacheinander 100 %, 150 %, 300 %
   ausprobieren (100 % = so klein wie frueher). Bei 300 %: ist der Pfeil gleich gross wie der Kreis? Danach zurueck auf **Auto**.
   (Doppelklick auf die Markierung blendet sie fuer dieses Junge aus -- dann `NCBear_CubClean()` und `NCBear_CubHere(30)` neu.)
4. Hingehen. Sieht es dich, bleibt die Markierung noch etwa 1 Minute, dann ist sie weg.

**Teil B: Wechsel auf den grossen Baeren**
5. Direkt neben dem Jungen `NCBear_CubTame(100)`, Rechtsklick aufs Junge > **"Follow me"**. Es ist das ALTE Junges-Modell (laeuft normal).
6. Stehen bleiben (das Junge steht nah bei dir), dann `NCBear_CubGrow(15)`.
   Erwartet: "Your bear is half-grown now.", das Junge verschwindet und an seiner Stelle steht **der grosse Baer in klein** (etwa gleich gross),
   **genau EIN Tier**, gleicher Name, Schild sagt jetzt "bear". In der Konsole: `... body big (swapped)`.
   Steht dort `swap waits: move`: er rannte gerade -- hoechstens 10 Sekunden warten.
7. `NCBear_CubStats()`. Erwartet: `body big / want big / engine type ncbeargrown`, `size inner 0.750 / shown 0.720`, Leben `/ 150`.
   Gehen und rennen: **folgt er weiter? rutschen die Fuesse? sitzt das Schild ueber dem Buckel? war der Sprung beim Wechsel klein?**
8. `NCBear_CubGrow(30)`. Erwartet: "Your bear is strong now.", deutlich groesser, `shown 0.982`, Leben `/ 254`.
9. `NCBear_CubGrow(55)`. Erwartet: "Your bear is full-grown now.", `shown 1.350`, Leben `/ 400`, Ausdauer `/ 160`, Traglast 100 -- so gross wie
   der erwachsene Test-Baer. Folgen lassen: haelt er Abstand und laeuft nicht in dich rein?
10. Rechtsklick auf den grossen Baeren: Fuettern (Figur haelt das Futter hoch), Streicheln, "Stay here" / "Follow me", "Name the bear",
    "Call to me" (`NCBear_CubCallReset()` macht die Wartezeit frei). Alles wie beim Jungen?

**Teil C: zurueck, Speichern**
11. `NCBear_CubGrow(-100)`. Erwartet: wieder das kleine alte Junge (0,35), ein Tier, Name gleich, folgt weiter, keine Meldung.
12. `NCBear_CubGrow(15)`, warten bis "body big (swapped)" da ist, dann Esc > Speichern und beenden, laden. Erwartet: genau EIN grosser Baer,
    gleicher Name und Groesse (hoechstens 2-3 s klein). Ist er weg oder kommt "You have lost track of your bear.": **sofort speichern, beenden
    und mir Bescheid geben** (mit Uhrzeit) -- nicht weiterspielen, nach 24 Spielstunden waere er sonst fort.

**Teil D: Auto (nur wenn du magst)**
13. Kein Auto da? Rechtsklick auf den Boden > Debug > Main > **"Spawn Vehicle"**. Der grosse Baer folgt, du steigst ein: "Your bear climbs in
    with you." Fahren, aussteigen: "Your bear climbs out.", er steht als grosser Baer neben dir.
14. Mit dem Jungen: `NCBear_CubGrow(-100)`, `NCBear_CubGrow(14)`, einsteigen, im Auto `NCBear_CubGrow(1)`, aussteigen. Erwartet: es steigt als
    grosser Baer aus (ein Tier).

**Teil E: Altes bleibt**
15. Namensschild, Lebensbalken und Alter-Zeile wie in B1d; ein wildes Junges (`NCBear_CubClean()`, `NCBear_CubHere(12)`) waechst nicht und
    wechselt nie.

**Wenn etwas nicht geht:** `NCBear_CubStats()` und `NCBear_CubInfo()` eintippen, Uhrzeit merken. Rote Fehler stehen unten rechts (Debug) und in
`C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`, die Testbefehle schreiben `[NCBear]`.
