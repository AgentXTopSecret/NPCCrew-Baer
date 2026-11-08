# Baer: Test nach Lauf baer-laerm (08.11.2026 abends)

Statisch geprueft (Attrappen 532 + 114 Pruefungen gruen, Lua-Pruefer gruen), **nicht gespielt**. Nur Einzelspieler.

1. **Spiel neu starten** (Lua laedt nur beim Start). Gleicher Garten mit Maschendraht und Zombies am Zaun ist der beste Test, Tempo 1.
2. **Kampf:** Der Baer soll zuschlagen und treffen. In der Konsole keine Serie `*** ... did not finish ... left idle` mehr und kein
   "6 attacks in a row broke off" mit Weglaufen. "stuck on the way" nur noch, wenn er wirklich nicht hinkommt (Zaun dazwischen).
3. **Aufrichten:** nur noch EIN Schrei, auch wenn es laut ist (bei Laerm bricht er das Aufrichten ab und rennt los).
4. **Notloesung bei Dauer-Haemmern:** Wenn Zombies ohne Pause am Zaun schlagen, kommt ein Teil der Treffer ueber die Uhr: der Zombie
   faellt, ohne dass der Hieb ganz zu sehen ist. Sag, ob dich das stoert (abschaltbar: `NCBear_Tune("clockHit", 0)`).
5. **Knockback:** Vorgabe jetzt `knockPush` 0,7 (dein Wert). Von vorn Getroffene fliegen rund 2,1 Kacheln; von der Seite/hinten fallen
   sie weiter nur um.
6. **Testbefehle zur Kamera:** `NCBear_Sit()`, `NCBear_Eat()`, `NCBear_AnimTest("rear")` drehen ihn vorher zur Kamera. Sag, ob er
   wirklich zu dir nach vorn schaut (Richtung SE ist berechnet, nicht gesehen). Ein schon sitzender Baer wird nicht gedreht.
7. **Infos:** `NCBear_FightInfo()` zeigt jetzt auch "noise interruptions" und den Stress. Ab Stress 60 kommt eine `***`-Zeile.
   Mehr Einzelheiten: `NCBear_Tune("log", 2)`.
8. Rote Fehler ja/nein; console.txt (`[NCBear]`, `***`) lese ich selbst.

**Offen, braucht dein Wort:**
- **Stress senken:** jeder Zaun-Schlag macht den Baeren ein bisschen gestresster (Engine). Ab Stress 70 laeuft ein Tier auch vor dem
  Spieler weg. Vanilla senkt Stress mit `changeStress` (ISMilkAnimal.lua:28). Darf unser Kampfcode den Stress nach Laerm wieder senken?
- **`setShouldFollowWall(false)`** steht nur im Jar (kein Vanilla-Lua-Beleg): wuerde einen seltenen Fall loesen (sehr lange Wegsuche +
  Dauerlaerm = 0 Treffer, eine 60-s-Ruhe). Nach der eisernen Regel nur mit deinem Wort.
