# Test: Baeren-Junges folgt, bleibt, Namensschild (B1b) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Vorher**
- **Seit 11.11.2026 01:19 in der Test-Mod.** Spiel **neu starten, mit -debug** (die neuen Dateien laden nur beim Start).
- Im Debug-Menue den **"Tier Cheat"** ausschalten (sonst stehen "aufheben"/"anleinen" im Menue und verfaelschen den Test).
- Essen kann man im Spiel selbst **nicht** in die Hand nehmen (Vanilla hat dafuer kein "Ausruesten"). Futter in die Hand geht nur ueber
  unseren Rechtsklick **"Hold out food for the cub"** (oder von selbst beim "Feed").
- Dein Spielstand mit dem gezaehmten Jungen geht (Apocalypse 2026-11-10_22-12-12). Er zaehmt noch mit den alten Punkten (14 / 8);
  die neue, laengere Zaehm-Dauer gilt nur in neuen Spielstaenden.
- Befehle tippst du in die **Lua-Konsole** (Debug). Texte sind englisch.

**Teil A: dein gezaehmtes Junges** (keins da? `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`)
1. Laden. Erwartet: keine roten Fehler. Ueber dem Jungen **"<dein Vorname>'s cub"**, darunter blasser **"staying"**, dicht ueber dem Kopf.
   Zu hoch oder zu tief? `NCBear_CubSet("tagZ", 0.25)` (hoeher) bzw. `NCBear_CubSet("tagZ", 0.12)` (tiefer) -- die beste Zahl melden.
2. Rechtsklick aufs Junge > Untermenue des Jungen > **"Follow me"**. Erwartet: "Your cub follows you.", Schild "following".
3. 30 Sekunden geradeaus **gehen**. Erwartet: es laeuft etwa 3-4 Kacheln hinter dir und bleibt NICHT immer wieder stehen.
   Stehenbleiben: es kommt heran und wartet neben dir (kommt es zu nah? melden).
4. Lange die Strasse entlang **sprinten**. Erwartet: es faellt zurueck; bei etwa 40 Kacheln "Your cub could not keep up. It waits to
   the ..." und "staying". Zurueckgehen, wieder "Follow me".
5. In ein **Auto** steigen. Erwartet (noch!): "Your cub cannot follow a vehicle. It waits here.", "staying". Aussteigen, wieder "Follow me".
   (Mitfahren wie die NPC-Crew-Leute und der Unstuck-Knopf kommen in der NAECHSTEN Version -- Kevin 11.11.)
6. In ein Haus gehen, **Tuer zu**. Erwartet: es wartet draussen ruhig; Tuer auf -> es kommt nach. Treppe hoch: es wartet unten (melden).
7. **Speichern**, Hauptmenue, laden. Erwartet: Junges da, Schild "following", nach ein paar Sekunden folgt es weiter.
8. Rechtsklick > **"Name the cub"** > "Bruno" > OK. Erwartet: "Your cub is now called Bruno.", Schild "Bruno".
   Gegenprobe: mehr als 24 Zeichen oder ein "<" -> OK ist grau mit Hinweis.
9. Rechtsklick > **"Stay here"**. Erwartet: "Your cub stays here.", "staying"; es bleibt in der Gegend (wandert hoechstens ~12 Kacheln).
   Zum Vergleich `NCBear_CubSet("stayR", 10)`.
   Komisch? `NCBear_CubFollowTest()` und `NCBear_CubInfo()` eintippen und mir den Konsolen-Ausschnitt schicken.

**Teil B: Futter hinhalten** (Achtung: `NCBear_CubClean()` raeumt auch dein gezaehmtes Junges weg)
10. `NCBear_CubClean()`, `NCBear_CubFood()`, `NCBear_CubHere(12)` (draussen, am besten am Wald). Erwartet: scheues Junges 12 Kacheln weg,
    Balken "Taming 0% - shy" an derselben Stelle wie vorher das Schild (dicht ueber dem Kopf).
11. Rechtsklick auf den **Boden** (nicht aufs Junge) > **"Hold out food for the cub"** > Barsch. Erwartet: Barsch in der Hand, ohne
    hinzugehen. **Stillstehen:** das Junge kommt bis etwa 3 Kacheln. Dann langsam hin (nicht rennen, sonst flieht es), Rechtsklick aufs
    Junge > "Feed" > Barsch -> klappt **ohne Hinterherrennen**, genau ein Barsch fehlt.

**Teil C: Reste aufraeumen (Waise)**
12. `NCBear_CubLog(true)`, dann `NCBear_CubOrphan(8)`: ein zweites Junges OHNE Balken. 30+ Kacheln weggehen, nicht hinsehen, etwa
    3 Minuten warten (oder schneller: von dort weit weg einmal `NCBear_CubSweep()` eintippen).
    Erwartet: es ist weg, in der Konsole "[TC-BEAR] scan: removed an orphan cub". Das andere Junge bleibt.

**Freiwillig:** `NCBear_CubTame(100)`, "Follow me", dann `NCBear_CubKill()`. Erwartet: "Your bear is dead ... 7 day(s)", Schild weg,
keine roten Fehler.

**Wenn etwas nicht geht:** `NCBear_CubInfo()` eintippen, Uhrzeit merken. Rote Fehler stehen unten rechts (Debug) und in
`C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`, die Testbefehle schreiben `[NCBear]`.
