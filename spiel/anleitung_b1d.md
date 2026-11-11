**Seit 11.11.2026 in der Test-Mod NCBearTest.** Spiel neu starten (mit -debug). Statisch geprueft, nicht gespielt.

# Test: Baeren-Junges B1d (Wachsen) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (oder NCBearTest nicht geladen ist). Danach Spiel **neu starten, mit -debug** (neue Dateien und
  die geaenderte Tier-Definition laden nur beim Start).
- Mods an: **NCBearTest UND Bandits** (ohne Bandits kein Pfeil oben). NPC Crew darf an oder aus sein.
- Im Debug-Menue den **"Tier Cheat" ausschalten** und am Jungen keine Debug-Tierknoepfe (Alter, "max size") benutzen.
- Befehle tippst du in die **Lua-Konsole** (Debug). Texte im Spiel sind englisch. Zahlen unten sind "etwa" (hast du schon ein Junges,
  ist es seit dem Zaehmen schon ein bisschen gewachsen).

**Teil A: Laden und Anzeige**
1. Spielstand laden. Erwartet: keine roten Fehler.
2. Kein gezaehmtes Junges? `NCBear_CubClean()`, `NCBear_CubHere(8)`, hingehen, `NCBear_CubTame(100)`, Rechtsklick > **"Follow me"**.
3. `NCBear_CubStats()`. Erwartet in der Konsole: `day 0 of 100`, `size inner 0.350 / shown 0.350`, Leben `/ 40`, `carry 10.0`.
   Ueber dem Jungen: Name, Zustand, **"Day 0 - half-grown in 15 day(s)"** und ein **roter Lebensbalken**.
4. Esc > Optionen > **Mods** > "NPC Crew: Bear": Leben auf **Number** -> "Health 40/40"; Ausdauer auf **Bar** -> gelber Balken;
   Alter aus -> die Tag-Zeile ist weg; Namensschilder aus -> nur die Balken bleiben. Danach alles zurueck wie du es magst.
   Sag mir: Reihenfolge und Groesse ok?

**Teil B: Wachsen** (das Junge steht vor dir)
5. `NCBear_CubGrow(5)`. Erwartet: sichtbar groesser, "Day 5 - half-grown in 10 day(s)", `NCBear_CubStats()` Leben `/ 77`.
6. `NCBear_CubGrow(10)`. Erwartet: Meldung **"Your bear is half-grown now."**, Groesse 0,75 (`shown 0.750`), Leben `/ 150`, Traglast 40.
   Jetzt "Follow me", gehen und rennen: **rutschen die Fuesse? sitzt das Schild ueber dem Kopf?**
7. `NCBear_CubGrow(30)`. Erwartet: **"Your bear is strong now."**, das Bild bleibt so gross wie vorher (`inner 1.000 / shown 0.750`),
   Leben `/ 254`, Ausdauer `/ 125`, Traglast 65, "Day 45 - full-grown in 55 day(s)".
8. `NCBear_CubGrow(55)`. Erwartet: **"Your bear is full-grown now."**, "Day 100 - full-grown", Leben `/ 400`. Bild weiter 0,75 (gewollt:
   der Wechsel aufs grosse Modell ist deine offene Frage).
9. `NCBear_CubGrow(-100)`. Erwartet: wieder klein (0,35), keine Meldung.

**Teil C: Leben, Ausdauer, Speichern**
10. `NCBear_CubHurt(50)`: Balken halb. Eine Spielstunde warten, `NCBear_CubStats()`: etwa 51 % (nicht 52-53 %).
11. Ausdauer auf Bar (Teil A 4), "Follow me", 1-2 Minuten sprinten: der gelbe Balken sinkt; stehen bleiben: er steigt wieder.
12. `NCBear_CubGrow(15)`, speichern, Hauptmenue, laden. Erwartet: gleiche Groesse (hoechstens 2-3 s klein), gleicher Tag, gleiches Leben.
13. Mit dem verletzten, gewachsenen Jungen ins Auto, fahren, aussteigen. Erwartet: gleiche Groesse, Leben wie vorher (nicht voll).
    Dasselbe mit Rechtsklick > "Call to me" (`NCBear_CubCallReset()` macht die Wartezeit frei).

**Teil D: wildes Junges waechst nicht**
14. `NCBear_CubClean()`, `NCBear_CubHere(12)`. Erwartet: Pfeil oben, Zaehm-Balken wie immer, **keine** Tag-/Lebenszeile, bleibt klein.

**Wenn etwas nicht geht:** `NCBear_CubStats()` und `NCBear_CubInfo()` eintippen, Uhrzeit merken. Rote Fehler stehen unten rechts (Debug) und in
`C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`, die Testbefehle schreiben `[NCBear]`. Eine einzelne Warnung
"Missing arguments for UI_BN_Bear_..." je Text ist bekannt und harmlos.
