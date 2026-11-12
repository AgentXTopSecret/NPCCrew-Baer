# Test: Baer F2 (Kampf, Fliehen, Am Boden, Tod, Verband) -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1 und F1B (Fenster mit E) sind schon drin.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- **Neuer Wegwerf-Spielstand**, Mods: **nur NCBearTest**. Sandbox Seite "NPC Crew": alles auf Vorgabe lassen. Tipp: "Bear: skill learning speed"
  auf **1000**, dann sieht man die Faehigkeits-Balken wachsen (mit 100 bewegen sie sich absichtlich nur wenig).
- Befehle tippst du in die Lua-Konsole. Die Texte sind englisch, mit Spielsprache Deutsch jetzt deutsch (Faehigkeiten, Leben, Herholen, stark). Fenster: **E** nah am Baeren.

**Teil A: Junges (kaempft nie)**
1. Laden: keine roten Fehler.
2. `NCBear_CubClean()`, `NCBear_CubHere(4)`, zum Jungen gehen, `NCBear_CubTame(100)`.
3. `NCBear_FightZed(2, 6)`: zwei Zombies laufen zum Jungen und beissen (Blut, Ton). Das Junge schlaegt **nicht** zurueck, es versteckt sich hinter
   dir. Fenster (E): Leben sinkt, "Melee damage" zeigt "--". Erledige die Zombies selbst.

**Teil B: Grosser Baer kaempft**
4. `NCBear_CubGrow(15)`: er wird gross (halbstark). Fenster: unter Condition die Zeilen **Melee damage** und **Kills**, Schalter **Show damage**.
5. `NCBear_FightZed(3, 6)`: die Zombies kommen und beissen ihn. Er knurrt und kaempft (Prankenhieb, Biss), ueber den Zombies stehen
   Schadenszahlen, Zombies fallen um. Im Fenster: Status "Fighting", Ausdauer sinkt, Kills zaehlt hoch, ab und zu "DODGE" ueber DEINEM Baeren.
   Waehrenddessen `NCBear_FightInfo()` eintippen.
6. Nach dem Kampf folgt er dir wieder. Dasselbe mit **Stay** und **Sit** im Fenster: er kaempft und geht danach an seinen Platz zurueck.
7. Stell dich so, dass hinter dem Baeren eine Hauswand mit Fenster ist, und hol `NCBear_FightZed(2, 4)` (die Zombies landen hinter dem Baeren,
   moeglichst im Haus): er schlaegt **nicht** durch die Wand in die Luft, und wenn du weggehst, folgt er dir.
8. **Passive** im Fenster an, `NCBear_FightZed(2, 5)`: er kaempft nicht, kommt zu dir ("Backing off"), die Zombies beissen ihn trotzdem. Passive wieder aus.
9. Show damage aus: keine Zahlen mehr ueber den Zombies. Wieder an.
10. Fliehen: `NCBear_CubHurt(15)`, dann `NCBear_FightZed(4, 5)`: er kaempft kurz, dann kommt die Meldung "Your bear is badly hurt ..." und er rennt
    zu dir. Maus ueber "Health" im Fenster: dort steht die Grenze. Zombies selbst erledigen.
11. Freund: mit Speer/Axt auf deinen eigenen Baeren hauen: das Leben bleibt gleich.

**Teil C: Verband, Am Boden**
12. Zwei Verbaende holen: `getPlayer():getInventory():AddItem("Base.Bandage")` zweimal eintippen.
13. Rechtsklick am Baeren "Bandage the bear" und sofort weglaufen: Aktion bricht ab, **beide Verbaende noch da**.
14. Nochmal "Bandage the bear" bis zum Ende: **genau einer weg**, Fenster zeigt "Bandaged: heals faster for 8 more hour(s)". Noch einmal versuchen:
    grau "already bandaged", der zweite Verband bleibt. Zeit vorspulen: Leben steigt schneller als vorher.
15. `NCBear_FightDown()`: er sitzt am Boden, Meldung "Your bear is down! Help it up." `NCBear_FightZed(2, 4)`: die Zombies lassen ihn in Ruhe.
    Rechtsklick "Help up the bear": er steht mit knapp halbem Leben auf.

**Teil D: Faehigkeiten und Tod (zum Schluss)**
16. Nach den Kaempfen: Balken Agility/Toughness (Bisse), Fighting (eigene Treffer), Endurance (Rennen) sind gestiegen. `NCBear_CubXp("fgt", 1000)`:
    Fighting springt auf 6, "Melee damage" wird groesser, daneben steht grau "max for its age" (halbstark lernt hoechstens Stufe 6).
17. Tod: `NCBear_CubHurt(5)`, dann `NCBear_FightZed(6, 3)`, nicht helfen. Er flieht, wird weiter gebissen und stirbt: Meldung "Your bear is dead ...".
    `NCBear_CubInfo()`: kein zahmer Baer mehr, **kein zweiter Baer** taucht auf.

**Altes bleibt:** alle Fenster-Befehle aus F1/F1B (Follow, Stay, Sit, Roam free, Come here, Unstuck, Passive, Name tag, Growth line), E und
Fern-Taste, Mitfahren im Auto (waehrend der Fahrt kein Schaden), Wachsen, alte Testbefehle (`NCBear_SpawnLive`, `NCBear_Sit` ... laufen weiter;
`NCBear_Fight()` sagt nur noch, wie man jetzt kaempft).

**Wenn etwas nicht geht:** `NCBear_FightInfo()`, `NCBear_CubStats()`, `NCBear_CubView()`, `NCBear_CubInfo()` eintippen, Uhrzeit merken. Mehr Zeilen:
`NCBear_FightLog(true)`. Rote Fehler stehen unten rechts (Debug) und in `C:\Users\Kevin\Zomboid\console.txt` -- unsere beginnen mit `[TC-BEAR] ***`.
