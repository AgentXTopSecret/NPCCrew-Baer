# Test: Baer F1B (Fenster mit E nah am Baeren, Fern-Taste, Growth line) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug** (neue Lua-Dateien
  laden nur beim Start).
- Mods: **nur NCBearTest** (Wegwerf-Spielstand). Nur fuer Teil C, Punkt 12 zusaetzlich **NPC Crew** (braucht Bandits).
- Die Tasten stellst du hier ein: Esc > Optionen > **Mods** > **"NPC Crew: Bear"** > ganz unten **"Bear window keys"**.
- Befehle tippst du in die Lua-Konsole. Die Texte im Spiel sind englisch.

**Teil A: E nah am Baeren**
1. Spielstand laden: keine roten Fehler. Optionen > Mods > NPC Crew: Bear: "Bear window: key near your bear" = **E**,
   "Bear window: key from anywhere" = leer. Optionen > Tastaturbelegung: **kein** Abschnitt "NPC Crew: Bear" mehr.
2. `NCBear_CubClean()`, `NCBear_CubHere(4)`, zum Jungen gehen, `NCBear_CubTame(100)`.
3. Junges anschauen, 1-3 Kacheln weg: **E** -> Fenster auf; **E** -> zu. Unten im Fenster: "Drag to move.  E near your bear or Esc closes."
4. Wegdrehen (Baer hinter dir, 2-3 Kacheln): E tut nichts. 5 Kacheln weg: E tut nichts, keine Meldung.
5. Baer neben eine Tuer holen, vor der Tuer stehen, **E**: nur die Tuer geht auf, KEIN Fenster. Dasselbe vor einem Fenster, an einem Zaun,
   neben einem Auto, beim Zielen (rechte Maustaste halten).
6. Weit weg vom Baeren an einer Tuer: E -> nur die Tuer, keine Meldung.
7. Neben dem Baeren ueber einen Zaun klettern und dabei E druecken: kein Fenster.
8. Neben dem Baeren in einem fremden Textfeld (Karten-Notiz oder Gegenstand umbenennen) und im Chat ein "e" tippen: kein Fenster.

**Teil B: Fern-Taste**
9. Optionen > Mods > NPC Crew: Bear > "Bear window: key from anywhere" auf **K** setzen, uebernehmen. (Meldet das Spiel "schon belegt":
   **Keep Both** waehlen, nie "Assign No Key".)
10. 50 Kacheln weg vom Baeren: **K** -> Fenster auf, K -> zu. Unten stehen jetzt E und K. Danach die Fern-Taste wieder leeren ("Clear"):
    K tut nichts mehr.

**Teil C: V gehoert wieder Vanilla und NPC Crew**
11. Waffe in die Hand (Axt/Messer), direkt vor dem Baeren stehen, **V**: Vanillas Tier-Rad geht auf, **ohne "Kill"**, und **kein** Baeren-Fenster.
    Neben einer Kuh mit Waffe: "Kill" ist da (Vanilla).
12. (Mit NPC Crew) Baeren-Fenster mit E offen lassen, vor einer Crew-Figur **V**: das Gespraech geht wie immer auf, das Baeren-Fenster bleibt offen.
13. Rechtsklick am Baeren -> "Bear window" geht weiter (Tooltip nennt "near your bear (E by default)").

**Teil D: Growth line**
14. `NCBear_CubGrow(12)`: ueber dem Baeren "Day 12 - half-grown in 3 day(s)". Im Fenster in der Schalterreihe rechts neben "Name tag" der Schalter **Growth line**:
    aus -> die Zeile ueber dem Baeren ist weg (Name bleibt); an -> wieder da. Aus lassen, speichern, Hauptmenue, laden: bleibt aus. Wieder an.
15. `NCBear_CubGrow(100)` (ausgewachsen): ueber dem Baeren **keine** Alter-Zeile mehr (auch kein "full-grown"); im Fenster verschwindet
    "Growth line", sonst bewegt sich nichts.
16. `NCBear_CubGrow(-100)`: wieder Junges; Schalter und Zeile (etwa "Day 0 - half-grown in 15 day(s)") sind wieder da.

**Altes bleibt**: alle Fenster-Befehle aus F1 (Follow, Stay, Sit, Roam free, Come here, Unstuck, Passive, Name tag), Rechtsklick-Menue,
Markierung oben, Karten-Symbol, Wachsen.

**Wenn etwas nicht geht:** `NCBear_CubStats()`, `NCBear_CubView()` und `NCBear_CubInfo()` eintippen, Uhrzeit merken. Rote Fehler stehen unten
rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`.
