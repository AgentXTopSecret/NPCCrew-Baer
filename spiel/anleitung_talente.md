# Test Talente -- fuer Kevin (Entwurf)

Statisch geprueft, nicht gespielt. Erst nach dem Einbau in NCBearTest. **Spiel neu starten** (Lua laedt nur beim Start), Sprache **Deutsch**,
Einzelspieler, **neuer Wegwerf-Spielstand** -- in den Sandbox-Optionen (Seite NPC Crew) **"Bär: Talente zurücksetzen erlaubt" AN** (nur fuer Punkt 7;
Vorgabe ist aus). Die Befehle unten sind Testhilfen der Test-Mod (kommen nie nach NPC Crew); in die Konsole kopieren.

1. **Junges, noch kein Punkt:** `NCBear_CubHere()` und `NCBear_CubTame()`, dann `NCBear_CubWin()` -> Reiter **Talente**.
   Erwartet: 8 Talente grau mit Schloss, Angler mit Sanduhr "Später", unten "Nächster Talentpunkt in etwa ... Tag(en)".
2. **1. Punkt bei 10 %:** `NCBear_CubGrow(10)`. Erwartet: am Reiter sofort eine **1**, 8 Talente hell mit Honigrahmen; die Meldung "Dein Junges
   hat einen Talentpunkt verdient!" kommt spätestens nach 10 Spielminuten. Klick auf **Genügsam** -> Ja/Nein-Fenster des Spiels -> **Nein**: nichts
   passiert. Nochmal -> **Ja**: es leuchtet golden.
3. **2. Punkt bei halbstark:** `NCBear_CubGrow(6)` (Tag 16 = halbstark, er bekommt den großen Körper; Meldung wieder spätestens nach 10 Spielminuten),
   **Schwere Pranke** lernen. Dann `NCBear_FightZed(3)`: jeder Prankenhieb wirft den Zombie um und er fliegt etwa 1,4 Kacheln weg (ohne dieses
   Talent wirft ein halbstarker Bär gar nicht um).
4. **3. Punkt bei ausgewachsen:** `NCBear_CubGrow(100)`, **Kritischer Treffer** lernen. Im Zahnrad **Schaden zeigen** an, `NCBear_FightZed(5)`:
   etwa jede vierte Zahl steht gross in **Gold mit "!"**. Danach: alle anderen grau mit Schloss (Angler mit Sanduhr), oben "Alle 3 Talente gewählt".
5. **Nie mehr als 3:** `NCBear_CubGrow(-100)` (er wird kurz wieder ein Junges -- gewollt), dann `NCBear_CubGrow(100)`. Erwartet: KEINE neue
   Punkt-Meldung, weiter genau 3 aktiv. Aussehen wechseln (Knopf "Aussehen") und Unstuck: weiter dieselben 3. Speichern, ins Hauptmenü, wieder
   laden: weiter dieselben 3, alle anderen gesperrt, keine Punkt-Meldung.
6. **Werte im Fenster:** `NCBear_TalentWipe()`, dann `NCBear_TalentForce("fur,mule,frugal")`. Reiter Übersicht: Leben +250 (z. B. 400 -> 650, Balken
   gleich voll), Last +50 kg; Maus auf Hunger: "Talent Genügsam: 24 statt 16 h satt" und der Tagesbedarf ist 2/3 so gross wie ohne. `NCBear_TalentInfo()`
   zeigt alles als Text.
7. **Zurücksetzen (Sandbox an):** Knopf "Zurücksetzen" -> Ja -> alle Talente frei, 3 Punkte wieder da (Leben wieder ohne +250, Balken gleich
   voll). Der Knopf ist jetzt grau, weil nichts gelernt ist. Ein Talent lernen (Ja) -> der Knopf bleibt grau mit "in ... Std.": der nächste Reset
   geht erst ab dem nächsten Spieltag (Mitternacht im Spiel, siehe Frage "1 Tag").
8. **Symbole ansehen:** Lasttier ist jetzt ein **Lastsack** (vorher Rucksack, sah aus wie das Schloss); wählbare Talente sind voll hell, gesperrte
   grau. Passt die Größe in 1080p (56 px)? Siehe Fragen im Bericht.

Nebenbei: `console.txt` ohne neue Fehlerzeilen. Mehrspieler (Host + zweiter Spieler) ist ungespielt: der Server prüft jeden Punkt selbst.
