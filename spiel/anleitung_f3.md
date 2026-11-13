# Test: Baer F3 -- Hunger, Durst, Muedigkeit, Vertrauen, Schlafen, Herz -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1, F1B, F2, Deutsch und der Aussehen-Knopf sind schon drin.
(Vom Gegenpruefer am 13.11. abends gegen den Code berichtigt: Schritte 9, 10, 11, 12/13, 15, 20 und der neue Schritt 16b -- in der
ersten Fassung waeren 13 und 15 so nicht gegangen, siehe `f3/GEGEN.md` Abschnitt 7.)

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- **Neuer Wegwerf-Spielstand**, Mods: **nur NCBearTest**. Sandbox-Seite "NPC Crew": jetzt **13** Baeren-Optionen, neu
  **"Bear: needs speed (percent)"** (100). Alles auf Vorgabe lassen.
- Befehle tippst du in die Lua-Konsole. Fenster: **E** nah am Baeren. Du brauchst eine **volle Wasserflasche** (Debug-Itemliste
  "Water Bottle" oder am Waschbecken fuellen). Schlafen sieht in F3 noch aus wie **Sitzen** -- die Liege-Bewegung kommt mit dem Modell-Lauf.
- **Merke fuer alle Schritte:** `NCBear_CubSleep()` stellt die Muedigkeit auf **100 %**. Solange sie so hoch bleibt, ist er nach dem Wecken
  "zu muede zum Kaempfen" (ab 90 %) und schlaeft nach einer Minute wieder ein (bei 100 %). Das ist die Regel, kein Fehler -- wo es stoert,
  steht unten ein `NCBear_CubNeeds(nil, nil, <Zahl>)` dabei (dritte Zahl = Muedigkeit; er schlaeft dabei weiter).

**Teil A: Fenster und Beduerfnisse (Junges)**
1. `NCBear_CubClean()`, `NCBear_CubHere(4)`, hingehen, `NCBear_CubTame(100)`, `NCBear_CubFood()`.
2. **E**: drei Karten **Condition | Needs | Skills**. In Needs vier Balken mit Prozent: Hunger 20, Thirst 20, Tiredness 10, Trust 50.
   Maus auf einen Balken: Tooltip mit dem **Wort** ("Now: Full (20%)"). **Fish, Inventory, Nose alerts** sind grau ("Comes with a later version.").
3. `NCBear_CubNeeds(85)`: Hunger rot, Tooltip "Starving"; spaetestens nach 10 Spielminuten die Meldung "Your cub is starving! Feed it.".
4. Rechtsklick aufs Junge, **Feed** mit Honig: Meldung "Fed. Hunger 35%." (ein Honig = 50 % beim Jungen). Gleich noch einmal fuettern geht
   (keine Wartezeit mehr, Hunger 0 %); danach ist **Feed** grau mit dem Grund "Your cub is not hungry." (unter 5 %), der Honig bleibt.
5. `NCBear_CubNeeds(nil, 80)`: Durst hoch. Rechtsklick, **Give water to the cub**, Flasche waehlen: Meldung "Watered. Thirst 0%.", die Flasche
   wird leerer (etwa ein halber Liter). Danach ist der Punkt grau mit dem Grund "Your cub is not thirsty.", die Flasche bleibt, wie sie ist.
   Ohne Wasser im Inventar ist der Punkt ebenfalls grau.

**Teil B: Schlafen und z Z z**
6. `NCBear_CubSleep()`: es setzt sich (= schlaeft), Meldung "Your cub is exhausted and lies down to sleep.", Schild-Zeile **"sleeping"**
   hellblau, darueber steigt ein hellblaues **z Z z** auf -- bitte ansehen: immer nur **ein** grosses Z, sitzt es ueber dem Kopf?
   (`NCBear_ZzLift(10)` hoeher, `NCBear_ZzHead(0)` ueber die Mitte.) Sagt die Zeile "NOT asleep yet", legt es sich hin, sobald die Sperre
   um ist (hoechstens eine Minute nach einem Befehl).
7. Fenster: Chip **"Sleeping"**, unten "Your bear is asleep. Any order wakes it up." -- es gibt keinen Schlaf-Knopf.
8. **Streicheln**: es schlaeft weiter. **Fuettern** (vorher `NCBear_CubNeeds(40)`): es wacht auf und frisst -- und **legt sich nach etwa
   einer Minute von selbst wieder hin** (ohne neue Meldung, wenn du bei ihm stehen bleibst). Das ist "weckt kurz".
9. Wecken mit einem Befehl: erst `NCBear_CubNeeds(nil, nil, 60)` (es schlaeft weiter, Muedigkeit 60 %), dann **Follow** klicken (oder
   `NCBear_CubWake()`): es wacht auf und **bleibt wach**; die Muedigkeit bleibt bei 60 %. (Ohne die 60 waere es gleich wieder bei 100 %
   und legte sich nach einer Minute erneut hin -- richtig, sieht aber aus wie ein Fehler.)
10. Ausschlafen: `NCBear_CubSet("tirSleepGround", 300)`, `NCBear_CubSleep()` -- nach dem Befehl aus Schritt 9 dauert es bis zu einer Minute,
    bis es sich hinlegt. Dann ein bis zwei Minuten warten: bei 0 % steht es von selbst auf, Meldung "Your cub wakes up, well rested.".
    Danach `NCBear_CubSet("tirSleepGround", 10.5)`.
11. Neben dir schlafen: Modus **Follow**, `NCBear_CubNeeds(nil, nil, 20)`, dann selbst schlafen (Bett oder Boden; deine Figur muss dafuer
    muede sein). Es legt sich 1-2 Kacheln neben dich und steht auf, wenn du aufwachst. Waehrend du schlaefst, ist dein Bild dunkel --
    du siehst es also erst **beim Aufwachen**: es sitzt neben dir und steht gerade auf. Zum Nachsehen vorher `NCBear_CubLog(true)`:
    in `console.txt` steht dann "sleep: ... lies down (owner)".
12. Im Schlaf heilen: `NCBear_CubHurt(50)`, `NCBear_CubSleep()`: das Leben steigt deutlich schneller als wach (etwa 15 % je Spielstunde).
    **Danach wecken und Muedigkeit senken** (wichtig fuer Teil C): **Follow** klicken, `NCBear_CubNeeds(nil, nil, 20)`.

**Teil C: Grosser Baer -- kaempft nicht**
13. Er muss **wach** sein (ein schlafender Baer waechst nicht um). `NCBear_CubGrow(15)` (er wird gross; bis zu einer Minute -- warten, bis
    der grosse Baer da ist). Dann `NCBear_CubNeeds(20, 20, 92)`: Fenster unten orange **"Your bear is too tired to fight. Let it sleep."**.
    `NCBear_FightZed(2, 6)`: er weicht zurueck, Schild "too tired - backing off", Meldung "Your bear is too tired to fight. Let it sleep.".
    Zombies selbst erledigen.
14. `NCBear_CubNeeds(nil, nil, 20, 10)`: **"Your bear refuses to fight: ..."** im Fenster und als Meldung. Alle Befehle gehen weiter
    (Follow, Stay, Sit ausprobieren). `NCBear_CubNeeds(nil, nil, nil, 50)`: er kaempft wieder ("trusts you enough to fight for you again").
15. Vom Zombie geweckt: `NCBear_CubSleep()`, warten bis er sitzt, dann **`NCBear_CubNeeds(nil, nil, 60)`** (er schlaeft weiter, ist aber
    nicht mehr "zu muede"), dann `NCBear_FightZed(1, 6)`: er schreckt hoch, weicht etwa **5 Sekunden** zurueck, dann kaempft er (sobald der
    Zombie bei ihm ist). Ohne die 60 kaempft er NICHT (Muedigkeit 100 % = zu muede) -- das waere die Regel aus Schritt 13.
    Danach schlaeft er nicht von selbst weiter (er ist bei 60 %).
16. Hunger schwaecht: `NCBear_CubNeeds(85)`: "Melee damage" im Fenster ist kleiner; Tooltip sagt warum.
16b. Verhungern geht nicht (wahlfrei): `NCBear_CubNeeds(100)`, `NCBear_CubSet("needHpHun", 300)`, bis zu 20 Spielminuten warten: das Leben
    sinkt auf **1 %** und bleibt dort, er faellt nicht um und stirbt nicht. Danach `NCBear_CubSet("needHpHun", 2)`, fuettern,
    `NCBear_CubHurt(100)`.

**Teil D: Vertrauen und Herz**
17. `NCBear_CubNeeds(nil, nil, nil, 100)`: Meldung "Your bear trusts you completely.", ein **Herz ueber dem Namen**. Sieh es dir bei deinem Zoom an.
18. Im Fenster **Name tag** ausschalten: Name **und Herz** sind weg. Wieder an: beide da. (Optionen -> Mods "Show name tags above tamed
    bears" aus: ebenso.) Einen eigenen Herz-Schalter gibt es nicht.
19. `NCBear_CubNeeds(nil, nil, nil, 99)`: Herz weg.

**Teil E: Optionen und Sandbox**
20. Optionen -> Mods -> **NPC Crew: Bear**: **"Hunger / Thirst / Tiredness / Trust above tamed bears"** je Off / Bar / Number (Vorgabe Off) und
    "z Z z above sleeping bears". Alle vier auf Bar: vier Balken mehr ueber dem Baeren -- kann man sie auseinanderhalten?
21. Neuer Spielstand mit **"Bear: needs speed" = 0**: im Fenster steht bei Hunger, Thirst, Tiredness **"Off"** (kein Balken), Trust laeuft
    weiter; er schlaeft dann nur noch neben dir.

**Teil F: Laden**
22. `NCBear_CubSleep()`, speichern, ins Hauptmenue, laden: er schlaeft weiter (sitzt sofort), genau **ein** Baer, Werte wie vorher.

**Bitte sag mir danach** (je ein Wort genuegt):
- Herz: so lassen (D, Goldrand) oder A (Klassik, rot)? Blatt `C:\Users\Kevin\NPCCrew-Nebenprojekte\_arbeit\baer_zaehmen\f3\bilder\KEVIN_herz.png`.
- Wird er oft genug muede? (Ohne Rennen und Kampf: Junges nach ~42, halbstark nach ~50, ausgewachsen nach ~62 Spielstunden wach, dann
  9,5 Stunden Schlaf bei jeder Groesse.)
- Nach dem Fuettern wieder hinlegen: gut so? Und nach einem Zombie: soll er dann auch weiterschlafen, solange er noch muede ist?
- Ueber dem Kopf: Vertrauens-Balken in Rosa statt Gelb (sieht sonst aus wie Ausdauer)?
- "Kaempft nicht" nur unten im Fenster -- reicht das, oder auch oben bei Melee damage?

**Wenn etwas nicht geht:** `NCBear_CubNeedsInfo()`, `NCBear_CubStats()`, `NCBear_CubView()`, `NCBear_CubInfo()` eintippen, Uhrzeit merken. Mehr
Zeilen: `NCBear_CubLog(true)`. Rote Fehler stehen unten rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit
`[TC-BEAR] ***`.
