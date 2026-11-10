# Test: Baeren-Junges zaehmen (B1a) -- Einzelspieler, erster Test

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Aussehen:** Das Junge traegt in dieser Version noch das ALTE Entwurfs-Modell (Platzhalter). Das neue Modell aus dem Generator kommt spaeter unter demselben Namen; hier geht es nur darum, ob Finden, Fuettern, Streicheln und Zaehmen funktionieren. In der Test-Mod seit 10.11.2026 21:28.

**Vorher:** Wegwerf-Spielstand (ein gespeichertes Junges bricht den Spielstand, wenn die Mod spaeter fehlt). Nur Mod **NCBearTest**
an (NPC Crew erst beim zweiten Durchgang dazu). Spiel **neu starten, mit -debug** -- die neuen Dateien laden nur beim Start.
Befehle tippst du in die **Lua-Konsole** (Debug). Texte erscheinen auf Englisch (es gibt keine deutsche Uebersetzung).

1. **Neuer Spielstand.** In den Sandbox-Einstellungen gibt es die Seite **"NPC Crew"** mit den Baeren-Zeilen (z. B. "Bear cubs").
   Erwartet: laedt ohne rote Fehler.
2. In einen Wald gehen, dann eintippen: `NCBear_CubFood()` (2 Honig, 3 Barsche, 3 Steaks) und `NCBear_CubHere()`.
   Erwartet: ein kleines Baerenjunges 8 Kacheln weg, ueber der Figur "cub b1 appeared 8 tiles away", kurz danach
   "A bear cub! It looks lost and hungry." Ueber dem Jungen ein Balken **"Taming 0% - shy"** und "Food: ready".
   (Alternativ: Rechtsklick auf den Boden > "NC Bear" > "Cub: give food" / "Cub: appear near me".)
3. **Ohne Futter in der Hand** auf das Junge zurennen. Erwartet: es rennt ein Stueck weg und haelt Abstand.
4. **Barsch in die Hand**, langsam hingehen, stehen bleiben. Erwartet: es bleibt stehen und kommt bis etwa 3 Kacheln heran.
5. Rechtsklick auf das Junge > Untermenue des Jungen > **"Feed"** > Barsch. Erwartet: Figur beugt sich, Junges frisst,
   **genau ein Barsch fehlt**, "+21 trust - it loves this!" und "It ate from your hand...", Balken **21 %**.
   Im Untermenue steht **kein "Kill"**. Bitte ansehen: steht das Junge waehrend des Fuetterns still?
6. Rechtsklick > **"Pet"**. Erwartet: Figur streichelt (Haltung bitte ansehen, Screenshot!), "+12 trust - it likes the change!",
   Balken **33 %**.
7. Sofort noch einmal Rechtsklick > "Feed". Erwartet: grau, Tooltip "It is still full. Try again in about 2 h." -- kein Barsch weg.
   Dann `NCBear_CubSkip(2)`.
8. Fuettern (Barsch, "+31", Balken 64 %), Streicheln ("+12", 76 %), `NCBear_CubSkip(2)`, noch einmal Fuettern.
   Erwartet: "The cub trusts you. It is yours now!", ueber dem Jungen blinkt **"Tamed!"** 5 Sekunden, dann kein Balken mehr.
   Streicheln geht danach weiter ("It enjoys that."), immer mit Pause.
9. Barsch in die Hand, 10 Kacheln weggehen, stehen bleiben. Erwartet: es kommt nach. Ohne Futter bleibt es in seiner Gegend.
10. Speichern, ins Hauptmenue, Spielstand wieder laden. Erwartet: Junges steht noch da; `NCBear_CubInfo()` schreibt in die Konsole
    eine Zeile mit `tame` und `owner __sp`.

**Wenn etwas nicht geht:** `NCBear_CubInfo()` eintippen und mir den Ausschnitt schicken. `NCBear_CubLog(true)` schaltet die
Diagnose-Zeilen `[TC-BEAR]` an. `NCBear_CubClean()` raeumt alle Jungen in der Naehe weg.

**Wo rote Fehler stehen:** im Spiel unten rechts der rote Fehlerzaehler (Debug); in `C:\Users\Kevin\Zomboid\console.txt`
-- unsere Fehler beginnen mit **`[TC-BEAR] ***`**, die Testbefehle schreiben `[NCBear]`. Bitte nach dem Test den Zeitpunkt nennen, dann
lese ich die Datei.

**Freiwillig danach** (Koeder und Tod): `NCBear_CubClean()`, Honig in die Hand, Rechtsklick auf Waldboden > "Lay out bear bait" > Honig:
Honig weg, Schild "Bear bait (honey) / night 0 of up to 3". 25 Kacheln weggehen, `NCBear_CubNight(true)`, zurueck: ein Junges nahe
der Stelle. Dann `NCBear_CubTame(100)` und `NCBear_CubKill()`: "Your bear is dead ... 7 day(s)"; `NCBear_CubHere()` lehnt danach ab.
