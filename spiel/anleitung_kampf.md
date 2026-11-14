# Test: Baer-Kampf (K1-K8) -- Bruellen, Liegende, Einholen, Tempo, Zombies auf den Baeren, Leine 25 -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1 bis F4, Liegen und K1 sind schon drin.
(Entwurf der Nachbesserung 14.11.2026, `kampf/NACHBESSERUNG.md`; vom Gegenpruefer berichtigt, `kampf/GEGEN.md` Abschnitt 7.) Was in console.txt stehen soll, steht kursiv darunter; `b1` ist dein Baer
(bei dir kann es `b2` heissen), `<z>` die Nummer eines Zombies.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- **Neuer Wegwerf-Spielstand**, Mods: **nur NCBearTest**, Sandbox alles auf Vorgabe (Zombies Schlurfer). Fuer Teil C einen zweiten Spielstand
  mit Sandbox **Zombies -> Geschwindigkeit: Sprinter**.
- Befehle tippst du in die Lua-Konsole. Zuerst immer: `NCBear_FightLog(true)` (Antwort: *fight / diagnosis lines [TC-BEAR] on*).
- Ausgewachsener Baer: `NCBear_CubClean()`, `NCBear_CubHere(4)`, hingehen, `NCBear_CubTame(100)`, `NCBear_CubGrow(100)` (bis eine Minute warten,
  bis der grosse Baer da ist). Er soll dir folgen (Rechtsklick Folgen).

**Teil A: Bruellen beim ersten Kontakt (K1) und Zombies greifen IHN an (K5)**
1. Stell dich neben den Baeren, `NCBear_FightZed(1, 9)` (ein Zombie 9 Kacheln hinter dem Baeren). Er bleibt kurz stehen (knapp eine halbe
   Sekunde), richtet sich auf und bruellt, dann stuermt er los.
   *`fight: b1 pick z <z> at 9` -- `fight: b1 rear planned (looking)` -- `fight: b1 rear yes` -- `fight: b1 act rear at d ...`*
2. Gleich danach (unter 2 Minuten) `NCBear_FightZed(1, 8)`: KEIN Aufrichten, er knurrt und greift sofort an. *`rear no (cooldown ... s)`*
3. Zombie direkt dran (2 Minuten nach dem letzten Aufrichten): `NCBear_FightZed(1, 2)`: kein Aufrichten, sofort Hieb.
   *`rear no (foe at 2 <= 2.5)`* (steht der Zombie knapp weiter weg und laeuft schon, auch *`rear no (foe reaches the bear ...)`*).
4. Baer auf **Bleiben**, du 3 Kacheln neben ihm, `NCBear_FightZed(3, 12)`, dann sofort 8 Kacheln **zur Seite** gehen (quer zur Linie Baer -
   Zombies). Die Zombies sollen auf den BAEREN gehen, nicht auf dich -- auch wenn sie dich sehen.
   *`lure: z <z> -> bear b1 (sees ...), target was player`* (frisch hingestellte Zombies, die dich noch nicht gesehen haben: `target was none`).
   Nur wer schon bis 2 Kacheln an dir ist, bleibt bei dir:
   *`lure: z <z> stays (player at 1.5) ...`* -- dann soll der Baer GENAU diesen zuerst angreifen: *`switch to <z> at ..., at the owner`* bzw.
   *`pick z <z>`* fuer ihn.
5. Dasselbe in der Welt mit echten Zombies (eine Strasse mit ein paar Zombies, der Baer folgt dir): sie sollen ihn angreifen, nicht nur dich.
   `NCBear_Lure()` zeigt, wer gerade gelockt ist. Danach den Baeren wieder auf **Folgen** stellen (Rechtsklick Folgen) -- Teil D braucht es.

**Teil B: Liegende zerfleischen (K2)**
6. `NCBear_FightZed(2, 6)` und zusehen: wirft er einen um, laeuft er hin und **zerfleischt** ihn am Boden (nicht warten, bis er aufsteht).
   *`act maul at d ... (..., down, ...)` -- `maul hit 1`*. Fliegt der Zombie nach dem Hieb weg, laeuft er hinterher.
7. Mindestens 2 Minuten nach dem letzten Aufrichten (sonst steht nur *`rear no (cooldown ... s)`*): schubs einen Zombie um (Leertaste), bevor
   der Baer ihn hat: liegt das ERSTE Ziel schon, richtet er sich nicht auf, sondern zerfleischt sofort. *`rear no (target down)`*
8. Es darf KEIN *`skip <z>: stuck at d ...`* fuer einen Liegenden direkt vor ihm kommen.

**Teil C: Laufende einholen, Tempo (K3, K4) -- Spielstand mit Sprintern**
9. `NCBear_FightZed(1, 10)`: rennt der Sprinter schon auf euch zu, wenn der Baer ihn bemerkt, richtet er sich NICHT auf (sonst beisst dich der
   Sprinter), er rennt los. *`rear no (foe reaches the bear (... at 3.6 t/s))`* oder *`(foe reaches the owner ...)`*. (Steht der frisch
   hingestellte Zombie in dieser knappen halben Sekunde noch still, richtet er sich auf -- dann *`rear yes`*; mit echten Sprintern in der Welt
   ansehen.)
10. Im Anlauf deutlich schneller als der Sprinter: *`run to ... speed 4.6 t/s`*; `NCBear_FightSpeed()` zeigt die letzten Anlaeufe (Ziel 4,6).
    Im Schlag nur ein kurzer Schritt nach vorn (nicht meterweit rutschen): *`act swipeR at d ... lunge 0.7)`* -- hoechstens 0.7.
    Ehrlich: einen Sprinter, der QUER oder WEG von ihm rennt (nicht auf euch zu), erwischt er meist nicht -- das waere der Sprung-Hieb (spaeter).
    Mit Sprintern geht er manchmal erst bei 7 statt 10 Kacheln los (er schaut nur alle 1,5 s nach, solange kein Zombie in 12 Kacheln war).
11. Nach dem Kampf geht er ruhig zu dir zurueck (8 Sekunden lang Gehen statt Rennen, solange du nicht weiter als 8 Kacheln weg bist).
    Kein Hin- und Herrennen zwischen mehreren Zombies.

**Teil D: Leine 25 und Sprint zurueck (K7), Verstecken (K6)**
12. Baer auf **Folgen**. Waehrend er kaempft: renn weg, mehr als 25 Kacheln. Er bricht ab und **sprintet** zu dir, bis er bei dir ist, dann geht er ruhig.
    *`fight: b1 leash run, owner at 25.x > 25` -- `fight: b1 ends (leash) ...` -- `follow: b1 leash run over (owner at ...)`*
13. Er geht bis 10 Kacheln auf Zombies los. Es darf NIE *`guard: b1 hides behind its owner`* kommen (nur das Junge versteckt sich).
14. Passiv (Fenster, Knopf Passiv) und `NCBear_FightZed(2, 8)`: er kaempft nicht, versteckt sich nicht und **lockt keine Zombies** (sie gehen
    auf dich -- du musst dich wehren). *`decide retreat (passive) ...` -- `guard: b1 big body does not hide ...`*, KEIN `lure: ... -> bear`.
    Danach Passiv wieder aus.

**Teil E: Zaun (Nachbesserung C1)**
15. Stell den Baeren an einen Zaun, ein Zombie auf der anderen Seite (2-3 Kacheln weg): er darf nicht lange davor stehen bleiben.
    Steht er in Schlagweite vor dem Zaun: *`skip <z>: wall` -- `target <z> is in reach but cannot be struck ... ignored for 8 s (1. time)`*,
    beim naechsten Mal `16 s (2. time)`. Kommt er gar nicht nah heran: *`skip <z>: stuck at d ...`* (ohne "ignored"-Zeile; Sperre 20 s, dann 40 s).

**Was du mir schickst:** console.txt (ab dem Spielstart) und, was komisch aussah (Screenshot mit roten Kreisen ist perfekt). Besonders:
ob der Ausfallschritt (Punkt 10) natuerlich aussieht, ob der Sprint (Fussgleiten) stoert, und ob die Zombies im Spiel wirklich auf ihn gehen
(Punkt 4/5). Alles danach: `NCBear_FightLog(false)`.
