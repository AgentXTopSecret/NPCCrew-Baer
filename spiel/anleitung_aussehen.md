# Test: Baer "Aussehen"-Knopf und kuerzere Sandbox -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1, F1B, F2 und Deutsch sind schon drin.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- **Neuer Wegwerf-Spielstand**, Mods: **nur NCBearTest**. Sandbox-Seite "NPC Crew" ansehen, alles auf Vorgabe lassen.
- Befehle tippst du in die Lua-Konsole. Fenster: **E** nah am Baeren. Steht dein Spiel auf Deutsch, heisst der Knopf "Aussehen" und die
  Namen Klassisch / Braun / Natur.

**Teil A: Sandbox (39 -> 12)**
1. Beim Anlegen, Seite "NPC Crew": genau **12** Baeren-Optionen, darunter neu **"Taming: speed (percent)"** und **"Bear: healing speed (percent)"**
   (beide 100). Weg sind z. B. "roaming radius", "zombies attack tamed bears", "bandage heal".
2. Laden: keine roten Fehler.

**Teil B: Junges**
3. `NCBear_CubClean()`, `NCBear_CubHere(4)`, zum Jungen gehen, `NCBear_CubTame(100)`.
4. **E**: neben "Unstuck" steht **"Look: Classic"**. Klick: kleines Menue mit **Classic** (Haken) und **Brown**. Brown waehlen.
   Meldung "Your cub has a new look."; das Junge steht an derselben Stelle (oder 1-2 Kacheln daneben), Name und Leben gleich.
5. Sieh dir das neue Junge an (du kennst es noch nicht): Gang (es geht etwas langsamer), Schild-Hoehe ueber dem Kopf, Sitzen, Fressen.
6. Knopf zeigt jetzt grau **"Look  4:59"** und zaehlt runter, **Unstuck auch** (dieselbe Uhr). `NCBear_CubLookInfo()` zeigt die Restzeit.
7. `NCBear_CubCallReset()`: beide wieder frei. **Eine Minute warten** (so lange ruht jeder Koerper-Tausch), zurueck auf Classic; wieder
   `NCBear_CubCallReset()`, eine Minute warten, wieder auf Brown.

**Teil C: Kein Heilen**
8. `NCBear_CubHurt(50)`. Fenster: Leben 50. `NCBear_CubCallReset()`, eine Minute warten, Look wechseln: **Leben bleibt 50**, Ausdauer gleich.

**Teil D: Gesperrt**
9. `NCBear_FightZed(2, 6)`: solange Zombies nah sind, ist Look grau ("Not now: zombies or enemies are close ..."). Zombies selbst erledigen.
10. Waehrend du das Junge fuetterst oder streichelst (Futter: `NCBear_CubFood()`), Look klicken: "Not now: your cub is busy ...".
11. Kurz nach einem Wechsel (bis 1 Minute) kann der Knopf hell sein und trotzdem "busy" sagen -- das ist gewollt.

**Teil E: Grosser Baer**
12. Das Junge steht auf **Brown**. `NCBear_CubGrow(15)`: es wird gross (nach einem Wechsel bis zu einer Minute spaeter) und bleibt **Brown**
    (Generator-Baer braun).
13. `NCBear_CubCallReset()`, eine Minute warten, Look: Menue mit **Classic / Brown / Natural**. **Natural** waehlen (Fototon). Schild-Hoehe und Aufrichten ansehen.
14. Wieder `NCBear_CubCallReset()`, dann **Unstuck**: er kommt zu dir und bleibt **Natural**. Ins Auto steigen, fahren, aussteigen: bleibt Natural.
15. Speichern, ins Hauptmenue, laden: er ist **Natural**, genau **ein** Baer. Look und Unstuck sind nach dem Laden sofort frei (bekannt).

**Teil F (wenn du einen alten Test-Spielstand von vorher hast)**
16. Alten Spielstand mit NCBearTest laden: laedt ohne rote Fehler, dein Baer ist da, Sandbox zeigt die 12.

**Bitte sag mir danach:** Gefaellt dir das braune Junge (soll es waehlbar bleiben)? Passen die Namen Classic / Brown / Natural? Und soll die
Wartezeit nach dem Laden frei sein (heute so) oder weiterlaufen?

**Wenn etwas nicht geht:** `NCBear_CubLookInfo()`, `NCBear_CubStats()`, `NCBear_CubView()`, `NCBear_CubInfo()` eintippen, Uhrzeit merken. Mehr
Zeilen: `NCBear_CubLog(true)`. Rote Fehler stehen unten rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit
`[TC-BEAR] ***`. Zwei Baeren gleichzeitig: Screenshot, dann weggehen (mehr als 25 Kacheln) und zurueck.
