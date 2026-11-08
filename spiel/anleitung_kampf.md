1. **Wegwerf-Spielstand, nur Einzelspieler**, Mod NCBearTest an, **Spiel neu starten** (mit -debug): Kampf, Clips und Toene gibt es erst nach dem Neustart.
2. Rechtsklick auf den Boden, "NC Bear", "Spawn living bear here"; dann Rechtsklick, Debug, **"Horde Manager"**: 3-5 Zombies 4-8 Kacheln neben den Baeren, du selbst 10+ Kacheln weg (er sucht bis 10, feindliche Banditen bis 12).
3. Sehen und hoeren: beim ersten Kontakt stellt er sich auf zwei Beine und bruellt (wieder nach 45 s), rennt mit Schnauben an, Prankenhieb links/rechts mit Wusch und Treffer, Zombies fallen um; bei 2+ vorn der Doppelschlag mit Stampfen (trifft bis 5), Liegende beisst er; danach zurueck zum Startplatz. Nie Spieler, Crew, neutrale NPCs, Tiere.
4. Konsole: `NCBear_Fight(false)` aus, `NCBear_Fight(true)` an, `NCBear_Fight()` Stand, `NCBear_FightInfo()` Zaehler; `NCBear_Tune()` listet alle Stellschrauben, z. B. `NCBear_Tune("dmg", 2)` mehr Schaden, `NCBear_Tune("arrive", 1.3)` wenn er nicht rankommt (gilt bis Neustart).
5. Durch Wand, Zaun, geschlossene Tuer und Fenster trifft er nicht, durch eine **offene** Tuer schon; kommt er an drei Ziele nicht heran, hoert er auf und ruht 20 s.
6. **Mehrspieler fehlt ganz:** dort kein Kampf, kein Schaden, der Befehl sagt es (wer den Zombie rechnet und wer den Baeren, ist nicht belegt).
7. Sag mir: Aufrichten + Bruellen da? Pranke am Zombie oder in der Luft? Fallen sie um, tot nach etwa 2 Hieben? Toene ok? Rote Fehler ja/nein; console.txt (`[NCBear]`, `***`) lese ich selbst.
8. Statisch geprueft (Attrappe 118/0), nicht gespielt.
