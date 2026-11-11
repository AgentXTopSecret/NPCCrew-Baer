**Seit 11.11.2026 08:12 in der Test-Mod NCBearTest.** Spiel neu starten (mit -debug). Statisch geprueft, nicht gespielt.

# Test: Baeren-Junges B1c -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist. Danach Spiel **neu starten, mit -debug** (neue Dateien laden nur beim Start).
- Mods an: **NCBearTest UND Bandits** (ohne Bandits gibt es keinen Pfeil oben). NPC Crew darf an oder aus sein.
- Im Debug-Menue den **"Tier Cheat"** ausschalten (sonst verfaelscht er das Tier-Menue).
- Befehle tippst du in die **Lua-Konsole** (Debug). Texte im Spiel sind englisch.
- Fuer Teil F brauchst du einen Zombie in der Naehe und fuer Teil C ein Auto.

**Teil A: Laden, Pfeil oben, zaehmen**
1. Spielstand laden. Erwartet: keine roten Fehler.
2. `NCBear_CubClean()` (raeumt ALLE Jungen und Eintraege weg, auch dein angefuettertes), dann draussen `NCBear_CubHere(30)`.
   Erwartet: oben am Bildschirm der **orange Kreis mit dem Baerenkopf**, Text "Bear cub nearby", Pfeil zeigt zum Jungen.
3. Hingehen. Sieht es dich ("A bear cub! It looks lost and hungry."), bleibt der Pfeil noch etwa 1 Minute, dann ist er weg.
4. Direkt daneben `NCBear_CubTame(100)`. Erwartet: "The cub trusts you ...". Rechtsklick aufs Junge > **"Follow me"**.

**Teil B: Karte und Optionen**
5. Mini-Karte und grosse Karte (M): ein **kleiner Baerenkopf** am Jungen. Stimmt die Groesse?
6. Esc > Optionen > **Mods** > "NPC Crew: Bear": Haken "Show name tags above tamed bears" aus, uebernehmen -> Schild weg; Schieber auf
   150 / 200 -> Schild groesser. Neustart: Werte bleiben.

**Teil C: Auto**
7. Junges folgt, du steigst in **irgendein Auto** (hoechstens 15 Kacheln weg). Erwartet: "Your cub jumps in with you.", es verschwindet.
8. Fahren, aussteigen. Erwartet: nach etwa 1 s "Your cub hops out.", es steht neben dir und folgt, Name und Schild gleich.
9. Im Auto **speichern**, Hauptmenue, laden, aussteigen. Erwartet: es kommt neben dir raus, kein zweites Junges.
10. Weiter als 15 Kacheln weg einsteigen. Erwartet: "Your cub was too far away to get in. It waits here."

**Teil D: Call to me (Unstuck)**
11. Junges "Stay here", 10-20 Kacheln weggehen (es muss noch zu sehen sein). Rechtsklick aufs Junge > **"Call to me"**.
    Erwartet: "Here is your cub again.", es steht neben dir, folgt; das alte ist weg (nur EIN Junges).
12. Dasselbe, aber du stehst **im Haus** an einer Wand und siehst das Junge draussen durchs Fenster. Erwartet: es kommt im selben Raum
    neben dir an, nie hinter der Wand oder im Nachbargarten. (`NCBear_CubCallReset()` macht die 5 Minuten Wartezeit sofort frei.)
13. Gleich nochmal ohne Reset: der Punkt ist grau ("about 5 min"). Du im Auto, Junges draussen: grau "Not while you are in a vehicle."

**Teil E: Register leer (dein Absturz-Fall)**
14. `NCBear_CubForget()`, dann `NCBear_CubSweep()`. Erwartet: weiterhin gezaehmt, gleicher Name, folgt weiter. In der Konsole genau EINE
    Zeile `[TC-BEAR] *** heal: entry b.. (tame, owner __sp) restored ...` -- die ist gewollt.

**Teil F: Laerm, Zombies, Gehen** (Junges folgt)
15. Rennen, sprinten, **Q rufen**, schiessen. Erwartet: es rennt NICHT mehr weg (hoechstens ein kurzer Schritt). `NCBear_CubCalm()` zeigt die Antworten.
16. Ein Zombie kommt auf etwa 6 Kacheln heran. Erwartet: das Junge stellt sich **hinter dich** (vom Zombie abgewandt). Bist du weiter als
    10 Kacheln weg, rennt es vom Zombie weg. (Zombies greifen es noch nicht an.) `NCBear_CubGuard()` zeigt, was es sieht.
17. Gehen: stehen bleiben, wenn es 4-5 Kacheln weg ist -- die letzten Schritte geht es. Selten zu sehen; deutlicher mit
    `NCBear_CubSet("walkDist", 6)`, dann aus ~8 Kacheln stehend herankommen lassen. Sieht das Gehen gut aus oder zu langsam?

**Wenn etwas nicht geht:** `NCBear_CubInfo()` (bei Auto auch `NCBear_CubRide()`) eintippen, Uhrzeit merken. Rote Fehler stehen unten
rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`, die Testbefehle schreiben `[NCBear]`.
