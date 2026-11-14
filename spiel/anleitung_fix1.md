# Test fix1 (Restbefunde R1-R6, G-R3) -- fuer Kevin

Statisch geprueft, nicht gespielt. Erst nach dem Einbau in NCBearTest. **Spiel neu starten** (Lua laedt nur beim Start), Sprache **Deutsch**,
Einzelspieler, Spielstand mit einem zahmen Baeren. Konsolen-Befehle sind Testhilfen der Test-Mod (kommen nie nach NPC Crew).

1. **Vertrauen mit Komma, Kopf = Fenster (R2, R4):** Konsole `NCBear_CubNeeds(nil, nil, nil, 0.5)`, im Zahnrad-Menue Vertrauen als Zahl.
   Erwartet: ueber dem Kopf "Vertrauen +0,5%" und im Baeren-Fenster ebenfalls "+0,5%" (vorher Kopf "+1"). Danach `NCBear_CubNeeds(nil, nil, nil, -1.5)`:
   beide "-1,5%". Im Fenster stehen auch Liter, kg und Prozent mit Komma.
2. **Am Boden kostet immer -10 (R3):** `NCBear_CubSleep()` (er legt sich hin, seine Beduerfnisse ruhen), dann `NCBear_FightDown()`.
   Erwartet: Meldung "... vertraut dir weniger (-10)", Vertrauen 10 tiefer. Danach Rechtsklick "Aufhelfen".
3. **"ruhen" auch, wenn er nicht geladen ist (R5) und neuer Hunger-Satz (R6):** Baer auf "Bleiben", so weit weglaufen, bis er nicht mehr geladen ist
   (gut 80 Kacheln), Baeren-Fenster oeffnen, Maus auf Hunger. Erwartet: "Seine Beduerfnisse ruhen: du bist zu weit weg." und
   "Ausgehungert: kein Wachstum, keine Heilung. Bei 100% verliert er Leben bis auf 1%." (Durst genauso).
4. **Leerer Baer bleibt richtig gefuellt (R1, Normalfall):** einem LEEREN Baeren (oder einem frisch gezaehmten) 5 Naegel geben, 15 s warten,
   normal speichern und beenden, wieder laden. Erwartet: 5 Naegel beim Baeren, bei dir 5 weniger, in `console.txt` KEINE Zeile
   "predates its first link". Einen Absturz kann man nicht nachspielen -- der eigentliche R1-Fall ist nur in der Attrappe geprueft.
5. **Kampf gegen einen Fliehenden (G-R3):** im normalen Spiel darauf achten: verfehlt er einen Zombie, der wegrennt, laeuft er ihm hinterher
   (hoechstens bis zur Leine), statt sofort "steckt fest" aufzugeben. Danach kommt er zu dir zurueck.

Nebenbei: `console.txt` ohne neue Fehlerzeilen (Absturz-Zeilen "inv: ..." nur nach einem echten Absturz).
