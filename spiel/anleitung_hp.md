# Test Lebensanzeige B "Rollenspiel" -- fuer Kevin (Entwurf)

Statisch geprueft, nicht gespielt. Erst nach dem Einbau in NCBearTest. **Spiel neu starten** (Lua laedt nur beim Start), Sprache **Deutsch**,
Einzelspieler, Wegwerf-Spielstand. Optionen -> Mods: **"Leben über gezähmten Bären" = Balken** (Vorgabe). Die Befehle sind Testhilfen der Test-Mod
(kommen nie nach NPC Crew); in die Konsole kopieren. Vorher einen eigenen Baeren: `NCBear_CubHere()` und `NCBear_CubTame()`, dann `NCBear_CubGrow(100)`.
So soll es aussehen: `_arbeit/baer_zaehmen/hp/bilder/KEVIN_hp_B_gebaut.png` (Entwurf links, Gebaut rechts, alle Stufen und Effekte) und
`KEVIN_hp_B_gebaut.gif` (bewegt). Im Spiel steht das Schild hoeher ueber dem Kopf als in den Bildern (Schild folgt der Pose, Frage F10).

1. **Farbstufen:** `NCBear_HpSet(100)`, `NCBear_HpSet(60)`, `NCBear_HpSet(30)`, `NCBear_HpSet(10)`.
   Erwartet: gruen, gelb, orange, rot; bei 10 % pulsiert alles schnell rot mit rotem Schein. Zahl im Balken z. B. "240/400".
2. **Heilen:** `NCBear_HpSet(60)`, dann `NCBear_HpHeal(12)`. Erwartet: neuer Teil leuchtet hell-gruen, Rahmen und Pfote gruen, 8 helle Kreuze steigen
   auf, gruene "+12" rechts daneben. Verband per Rechtsklick ("Bären heilen", saubere Bandage) oder Knopf "Heilen" im Fenster -> Pflaster rechts am Rahmen, solange er wirkt.
3. **Treffer:** `NCBear_HpHit(28)`. Erwartet: Balken wackelt, kurzer weisser Blitz, Rahmen rot, rote "-28" springt hoch, der verlorene Teil bleibt
   hell stehen und laeuft nach. Steht stattdessen **"AUSGEWICHEN"**, noch einmal -- das Wort steht jetzt **ueber dem Namen**, nicht mehr auf dem Balken.
4. **Kleiner Treffer bei viel Leben:** `NCBear_TalentForce("fur")` (Leben +250), dann `NCBear_HpHit(3)` mehrmals mit Pausen. Erwartet: die Zahl
   **springt nicht wieder hoch** (vorher sprang sie nach 3 s zurueck). Sie sinkt meist um 3, manchmal um 4 oder bleibt einmal stehen (Rundung der
   Sicht, Restbefund R2 in `hp/GEGEN.md`). Bekannt (Restbefund R1, falls nicht nachgebessert): EIN Treffer `NCBear_HpHit(5)` (knapp 1 %) laesst die
   Zahl nach etwa 6 s ohne Heilen um 3 hochspringen. Danach `NCBear_TalentWipe()`.
5. **Hunger:** sein Inventar ohne Futter (ab Hunger 50 frisst er sonst selbst), dann `NCBear_HpHunger(true)`. Erwartet: Keule rechts, Rahmen pulsiert langsam orange, **kein** Wackeln, kein Blitz; ungefaehr alle 30
   Spielminuten sinkt eine kleine orange "-4" ab (mit Standard-Tageslaenge etwa alle 75 s). Durst genauso: `NCBear_HpThirst(true)` (Tropfen).
   Darueber steht zusaetzlich die Zeile "Hunger 100%" (Auto-Zeile aus K1, Frage F2). Zurueck: `NCBear_HpHunger(false)` und
   `NCBear_HpThirst(false)`.
6. **Hunger bis ganz unten:** `NCBear_HpSet(3)` und `NCBear_HpHunger(true)`, warten. Erwartet: bei 1 % die letzte orange "-4" (**kein** Treffer-
   Wackeln), danach keine Keule mehr (er verliert dort nichts mehr). Futter in SEIN Inventar legen (Baeren-Fenster), waehrend er hungert: das letzte Sinken mit dem
   Fressen ist ebenfalls orange.
7. **Zu Boden:** `NCBear_FightDown()`. Erwartet: "am Boden" ueber dem ganzen Schild, Balken zeigt 5 %, keine gruenen Kreuze.
8. **Echter Kampf:** `NCBear_FightZed(3)`. Jeder Treffer zeigt genau eine rote Zahl; zieht er sich zurueck ("zu müde -- weicht zurück"),
   steht die rote Zahl **rechts neben** dem langen Text, nicht darauf (heilt er dabei, bleiben die Kreuze unter dem langen Text an der Oberkante des Rahmens stehen und blinken dort).
9. **Groesse:** Optionen -> Mods -> "Größe der Anzeige über Bären" 150 / 200: alles waechst mit, Zahl bleibt lesbar.
10. **Aus / Zahl:** "Leben über gezähmten Bären" = Zahl zeigt nur "Leben 240/400", = Aus nichts; im Zahnrad des Baeren-Fensters schaltet
    "Lebensbalken" ihn je Baer aus und an.

Zustand der Anzeige als Text: `NCBear_HpInfo()`. Nur die Anzeige ohne Schaden: `NCBear_HpShow()` (nach 6 s steht wieder der echte Wert).
Nebenbei: `console.txt` ohne neue Fehlerzeilen. Mehrspieler (Host + zweiter Spieler) ist ungespielt: dort zeigt ein **fremder** gezaehmter Baer die
Keule erst, wenn sein Leben wirklich gesunken ist (Frage F5 in `hp/NACHBESSERUNG.md`).
Gegenpruefung 14.11.: Punkte 2, 4, 5, 6, 8 und der Bild-Hinweis oben berichtigt (`hp/GEGEN.md`).
