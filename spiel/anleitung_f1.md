# Test: Baer F1 (Baeren-Fenster mit V, neue Befehle) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. So soll das Fenster aussehen:
`C:\Users\Kevin\NPCCrew-Nebenprojekte\_arbeit\baer_zaehmen\f1_entwurf\fenster_gebaut_4k.png` (links Junges, rechts grosser Baer).

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug** (neue Taste und neue
  Lua-Dateien laden nur beim Start).
- Mods: **nur NCBearTest** muss an sein (NPC Crew und Bandits duerfen aus sein). Wegwerf-Spielstand.
- Im Debug-Menue den "Tier Cheat" aus lassen. Befehle tippst du in die **Lua-Konsole**. Die Texte im Spiel sind englisch.

**Teil A: Taste V**
1. Spielstand laden. Erwartet: keine roten Fehler.
2. Draussen, nicht an einem Auto oder Tier: **V** druecken. Erwartet: ueber deiner Figur "You do not have a bear yet."
3. `NCBear_CubClean()`, dann `NCBear_CubHere(4)`, zum Jungen gehen, `NCBear_CubTame(100)`.
4. **V**: das Baeren-Fenster geht auf (wie im Bild links). **V** noch einmal: zu. Auf und dann **Esc**: zu (kein Pausenmenue).
5. Rechtsklick auf das Junge: Eintrag **"Bear window"** oeffnet dasselbe Fenster.
6. Taste umstellen: Esc > Einstellungen > **Tastaturbelegung** > ganz unten **"NPC Crew: Bear"** > **"Bear window"** auf **K** (in Vanilla frei).
   Zurueck ins Spiel: K oeffnet/schliesst, V nicht mehr. Danach wieder auf **V** stellen.
7. Neben dem Jungen eine Waffe in die Hand (Axt/Messer), **V gedrueckt halten**: Vanillas Tier-Rad mit "Kill" darf hoechstens kurz
   aufblitzen, beim Loslassen geht das Fenster auf.

**Teil B: Werte und Faehigkeiten**
8. `NCBear_CubGrow(12)`. Im Fenster oben: "Bear cub - day 12", orange "half-grown in 3 day(s)".
9. `NCBear_CubStats()` und das Fenster vergleichen: Leben (Health x / y), Ausdauer, "Can carry", bei jeder Faehigkeit die Stufe (Lv).
   Leben/Ausdauer duerfen um 1-2 Punkte abweichen (das Fenster rechnet in ganzen Prozent).
10. `NCBear_CubHurt(50)`: der Lebensbalken wird halb so lang und wechselt die Farbe. `NCBear_CubXp("fsh", 100)`: bei Fishing waechst der Balken; Lv wie
    in `NCBear_CubStats()`.
11. Maus ueber jede Faehigkeit: Tooltip sagt, was sie bewirkt; bei Agility, Toughness, Fighting, Fishing und Keen nose steht ehrlich, was erst spaeter kommt.
    Unten links "Coming later: Hunger, Thirst, Tiredness, Trust" -- ohne Balken (gibt es noch nicht).

**Teil C: Befehle (Knoepfe im Fenster)**
12. **Follow**: Knopf leuchtet orange, oben "Following you". Laufen -- es folgt.
13. Beim Rennen mitten im Lauf **Stay**: es bleibt **sofort** stehen (kein Weiterrennen), "Staying".
14. **Sit**: es setzt sich hin und bleibt sitzen, "Sitting". Streicheln (Rechtsklick): bleibt sitzen, kein neues Hinsetzen. Fuettern (Futter: `NCBear_CubFood()`):
    frisst, setzt sich danach wieder hin.
15. Im Sitzen **Follow**: es steht auf (Aufsteh-Bewegung) und folgt.
16. **Roam free**: es bummelt langsam um die Stelle, nie weiter als 12 Kacheln; im Fenster "up to 12 tiles".
17. **Stay**, 15-20 Kacheln weggehen, **Come here**: "Coming to you", es kommt und wartet neben dir ("... is with you and waits here.").
18. **Unstuck**: es steht sofort neben dir. Danach ist der Knopf grau mit Uhr (etwa "Unstuck 4:59"), der Tooltip zeigt **dieselbe** Uhr.
    `NCBear_CubCallReset()` macht ihn wieder frei.
19. **Passive** an: Meldung "... is passive now ... (comes later)". Fenster zu und auf: Haken ist noch da.
20. **Name tag** aus: das Schild ueber dem Jungen ist weg; an: wieder da.
21. **Rename**: Namensfeld geht auf; einen Namen mit "v" tippen -- das Fenster bleibt offen. Daneben klicken, V: Fenster bleibt offen.
22. Gerade nicht moegliche Knoepfe sind grau, die Maus zeigt den Grund.

**Teil D: Auto, Koerper weg, grosser Baer**
23. Auto holen (Rechtsklick Boden > Debug > Main > "Spawn Vehicle"), Junges auf **Follow**, einsteigen: es steigt mit ein. **Im Auto oeffnet V
    das Auto-Rad, nicht das Fenster** (gewollt). Fenster vorher mit V offen lassen: oben "Riding with you", Knoepfe grau mit Grund.
    Aussteigen: es steht neben dir und folgt.
24. `NCBear_CubBodyGone()`: nach ~15 s oben "Missing", unten "No body now. ..."; **Unstuck** holt es sofort zurueck (vorher `NCBear_CubCallReset()`, falls der Knopf noch grau ist). Noch einmal
    `NCBear_CubBodyGone()` und nur warten: nach **etwa 1-1,5 Minuten** "Your bear is back." -- **genau EIN** Junges. Weggehen (60 Kacheln) und
    zurueck: kein zweites.
25. `NCBear_CubGrow(15)`: grosser Baer; Fenster "Bear - day 27"; alle Knoepfe wie oben, Meldungen sagen "bear".
26. Esc > Einstellungen > Mods > "NPC Crew: Bear" > **"Size of the bear window"**: Auto und groesser probieren. Bei 4K muss alles gut lesbar
    sein. Fenster an eine andere Stelle ziehen, speichern, beenden, laden, V: es steht wieder dort.
27. (Wenn du magst) Vieh-Anhaenger: Rechtsklick am Anhaenger > Tier hinein: der Baer ist grau "zu gross" (gewollt).

**Altes bleibt**: Rechtsklick-Menue (Follow me, Stay here, Name, Call to me, Fuettern, Streicheln), Markierung oben, Karten-Symbol, Wachsen.

**Achte auf**: zwei Baeren auf einmal, ein Baer, der nach "Sit" wieder aufspringt, ein Fenster, das bei 4K zu klein ist.

**Wenn etwas nicht geht:** `NCBear_CubStats()`, `NCBear_CubView()` und `NCBear_CubInfo()` eintippen, Uhrzeit merken. Rote Fehler stehen unten
rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`, die Testbefehle schreiben `[NCBear]`.
