# Bau baer-laerm: Baer greift auch bei Weltlaerm an, sitzt und frisst (08.11.2026, nachgebessert)

Statisch geprueft, nicht gespielt. Gebaut nur in `_arbeit/baer_laerm/mod/` (Kopie aus NCBearTest, dort nichts geschrieben;
Kevin spielte waehrend des Laufs). Grundlage: `forschung_laerm.md` (A) und `forschung_zustand.md` (B).
Nur Einzelspieler (isSP-Riegel unveraendert), MP bleibt aus.
**Nachbesserung nach `pruef_technik.md` und `pruef_logik.md`: Einzelheiten je Befund in `fix_bericht.md`.** Der Stand vor der
Nachbesserung liegt in `vor_fix/` (Datei, Attrappe, Bericht).

## 1. Ursache (kurz, Belege in A und B, Ergaenzungen der Pruefer)

- Zombies, die auf Zaun/Tuer/Fenster schlagen (Radius 20, Maschendraht zusaetzlich 40), und Spieler-Schuesse erzeugen
  Weltlaerm mit Stress-Schalter. `IsoAnimal.respondToSound` schickt den zahmen Baeren dann auf einen Fluchtweg. Steht er
  (KI nicht walk/pathfind/followwall), bewertet die Engine jedes Bild neu; laeuft er und hat einen Laerm gemerkt, schweigt
  sie ("Schild", respondToSound Offset 0-35).
- Unser alter `fleeStop` stoppte jedes Bild. Ergebnis (A 2.3): bis zu 9 Fluchtbefehle je Schlag, jeder +Stress
  (Abbau nur getMultiplier/5500 je Update, `IsoAnimal.updateStress` Offset 212-228 in `_arbeit/baer_angriff/IsoAnimal.txt`),
  die Animation haengt ~17 Bilder in `pathfind`, danach startet unser Knoten neu bei 0 (B 3) -> Treffer und Ende kommen
  nach der Lua-Frist -> "did not finish ... (pathfind)", nach 6 Abbruechen 60 s Ruhe. Aufrichten neu = zweites Bruellen.
- Anlauf: der erste Laerm nach einem Halt ersetzt still unseren Weg; `updateApproach` setzte nur bei idle oder gewandertem
  Ziel neu -> "stuck on the way".
- Dazu (Pruefer, Jar): (F1) steht die KI mit fertigem Weg still in AnimalPathFindState, schickt WalkingOnTheSpot sie nach
  30 getMultiplier (0,63 s Animationszeit, Tempo 4: 150) selbst zur Mitte der eigenen Kachel (walk, Neustart, ohne Laerm);
  (F2) die Animation wechselt je Bild einmal, in der Reihenfolge der buck-Uebergaenge (aus walk erst nach idle, dann nach
  pathfind; aus pathfind vor idle nach followwall); (F3) `shouldFollowWall` bleibt im SP nach jedem Failed fuer immer gesetzt.
- Lua kann den Wechsel idle -> pathfind nicht verhindern (OnTick nach dem Animations-Uebergang, B 1.6). Einen voll
  belegten Weg, der den Clip-Neustart verhindert, gibt es nicht. Darum unten: je Fluchtbefehl EIN Halt, der vor
  WalkingOnTheSpot endet, Neustart sauber behandeln, und eine ehrlich markierte Notloesung.

## 2. Was geaendert wurde (nur `42/media/lua/shared/NCBearFight.lua`, Zeilen im nachgebesserten Stand)

| Wo | Was |
|---|---|
| :28-38 | Kopf: Abschnitt LAERM (was die Engine tut, was wir tun, Notloesung, Verweis fix_bericht.md). |
| :79-84, :99, :117 | Stellschrauben `fleeWait` (Bilder, 0..60, Vorgabe 18) und `clockHit` (0/1, Vorgabe 1) mit Klemmen. |
| :174-201 | Konstanten mit Deckeln: FLEE_STATES, FLEE_MOVED 0,03, NOISE_FRAMES 17, WOTS 30/150 und Rand 3 Bilder, STRESS 60/50/300 s, LOUD_GAP 2 / LOUD_REARMS 3 / LOUD_FRAMES 240, ACT_RESTARTS 2 (je Stoerung), NOISE_WAIT_MAX 1 s, NOISE_HIT_GRACE 0,3 s, NOISE_SAY_ACTS 3 / 120 s, NOISE_THUMP_R 40, CALM_NOISE 4 in 30 s, REROUTE 1,0 / 0,25 in 1,5 s / 4. |
| :211-215 | Zaehler `noise`, `noiseActs`, `noiseCalm`, `clockHits`, `reroutes`, `engineWalks`, `loudHolds`; `F.ticks`; `F.stressSayT`; `count()` (nil-fest). |
| :434-464 (`setBlock`) | Laeuft in diesem Bild ein Halt: `false` stoppt erst (sonst bliebe die KI in AnimalPathFindState -> WalkingOnTheSpot, klebendes shouldFollowWall); `true` beendet ihn, ausser im lauten Halt (dann durch den Stopp hindurch erhalten: bPathfind). |
| :468-482 (`refreshBlock`) | Halt zu Ende, ein sofort folgender Fluchtbefehl gilt als Dauerlaerm. |
| :483-523 (`clipBegin`/`clipWatch`) | erstes idle = Clip-Start, "away"/"back"; `B.awayRepeat`/`B.backRepeat`: Wiederholungen im selben Halt sind EINE Stoerung (im lauten Halt je Erneuerung eine). |
| :1010-1186 (`fleeStop` und Helfer) | **Ein Halt je Fluchtbefehl** (`B.flee`): Beginn = Stopp (pathfind; walk: Stopp + bPathfind). Im Halt ist jedes Bild Fortsetzung, auch idle und followwall. Ende nach `fleeWait` Bildern (Stopp im idle-Bild: kein Neustart) oder frueher, bevor WalkingOnTheSpot anspricht (`E.acc` = getMultiplier seit der Antwort, Grenze 30 bzw. 150 bei Tempo 4, `wotsLimit`); lebt der Laerm dann noch, neu halten. walk im Halt = Engine-Ausflug (`engineWalks`, nicht Laerm). Ohne Halt ist auch idle/followwall mit gesetztem `bPathfind` ein neuer Fluchtbefehl (KI noch idle), followwall ohne bPathfind nur Nachlauf. **Dauerlaerm:** kommt der Befehl hoechstens 2 Bilder nach einem Halt-Ende, ist der Halt "laut" und erneuert sich statt loszulassen (3x, 240 Bilder), auch durch beginAct hindurch. `stressNote`: laute Zeile ab Stress 60. `fleeWait 0` = altes Verhalten. |
| :1188-1218 | `noiseInfo` (nur log 2) und `noiseLoud` (EINE laute Zeile ab 3 Angriffen in Folge OHNE jeden Treffer, alle Baeren zusammen hoechstens alle 120 s). |
| :1240-1255 (`clockHit`) | **NOTLOESUNG:** Treffer per Lua-Uhr, wenn ein Fluchtweg den Clip brach und kein Treffer-Ereignis kam (nur ueber `F.ApplyHit`). Zeile je Uhr-Treffer nur bei log 2. Abschaltbar `NCBear_Tune("clockHit", 0)`. |
| :1257-1300 (`finishAct`) | done / hit / noise / left / missing; "attacks disturbed" zaehlt jeden gestoerten Angriff, die Folge der lauten Zeile nur die ohne Treffer. |
| :1302-1335 (`actClip`) | away: Aufrichten abbrechen -> Anlauf (kein zweites Bruellen); Treffer schon da -> fertig. back: Clip-Uhr auf 0, je Stoerung einmal gezaehlt, hoechstens 2, dann Ende (mit Notloesung). nil-fest nach Lua-Reload. |
| :1375-1385, :1387-1432 | **Anlauf:** fremden Weg erkennen und ersetzen ("runs off" / "makes no progress", je Anlauf hoechstens 4 mal); nil-fest nach Lua-Reload; Fundstelle getSquare. |
| :1555-1585 (`calmBack`) | Ruhe nach einer Stoerung: Aufstehen fertig, aus dem Sitzen neu hinsetzen, Hinsetzen/Testclip mit neuer Uhr; Wiederholung im selben Halt nur Uhr neu; mehr als 4 Stoerungen in 30 s: Ruhe aufgeben. |
| :1666-1736 (`updateBear`, Pause :1699, Suche :1708) | pause: naechster Angriff erst, wenn er steht UND kein Halt laeuft (Dauerlaerm: sofort; hoechstens 1 s). seek: Suche nicht mitten im Halt (Dauerlaerm: doch). |
| :2050-2073 | `NCBear_FightInfo()`: "noise interruptions ... \| continuous-noise holds \| engine walks \| approach paths taken back \| fleeWait, clockHit", je Baer der Stress. |

Unveraendert: Spielertreffer -> `endFight("hurt")` vor jedem fleeStop (der Halt ist dort nicht "in diesem Bild", setBlock
stoppt also nicht: die Engine laesst ihn fliehen). In Ruhe/Rueckweg kein fleeStop. AnimSets unveraendert. Keine
Cheat-/Testmenues neu; die zwei Stellschrauben gehen ueber das bestehende `NCBear_Tune`.

## 3. Engine-Aufrufe und Fundstellen

| Aufruf | Fundstelle | Status |
|---|---|---|
| `a:getStress()` (Diagnose log 2, Stress-Zeile, FightInfo) | Vanilla `shared/TimedActions/Animals/ISMilkAnimal.lua:17` (`self.animal:getStress()`) | belegt, gleicher Typ |
| `z:getActionStateName() == "thump"` (Diagnose) | Bandits `ZASmack.lua:486`; Zustand `media/actiongroups/zombie/thump` | belegt |
| `a:setVariable("bPathfind", true)` (holdArm, setBlock im lauten Halt) | Vanilla `ISMilkAnimal.lua:139` (`setVariable("milkanimalout", false)`, gleiche Methode, Wahrheitswert); Bandits `ZAMove.lua:31` (`setVariable("bPathfind", true)` am Zombie) | belegt (Methode und Argumenttypen); die Wirkung am Tier ist aus dem Jar abgeleitet (AnimalPathFindState.enter ruft dieselbe Methode) |
| `a:getVariableBoolean("bPathfind")` (neu, fleeStop ohne Halt) | Bandits `shared/ZombieActions/ZAMove.lua:60` (`zombie:getVariableBoolean("bPathfind")`) | belegt, gleiche Methode, gleiches Argument; dort am Zombie |
| `UIManager.getSpeedControls():getCurrentGameSpeed()` (neu, nur je neuem Fluchtbefehl) | Vanilla `client/Foraging/ISBaseIcon.lua:61-62` (samt Riegel `UIManager and UIManager.getSpeedControls`), `ISUI/ISBackButtonWheel.lua:25` (Ergebnis auf nil pruefen) | belegt |
| `z:getSquare()` (issueApproach) | Bandits `client/BanditUpdate.lua:1852` | belegt (Kommentar nachgetragen) |
| `stopAllMovementNow`, `fleeTo`, `getActionStateName`, `getZombieList` | wie bisher (ISAnimalContextMenu.lua:760, ISMilkAnimal.lua:38, Bandits ZASmack.lua:486, BanditZombie.lua:110) | unveraendert |

Nicht eingebaut, nur im Jar belegt (braucht Kevins Wort je Methode): `IsoAnimal.setShouldFollowWall(false)` (wuerde das
Pendeln pathfind -> followwall -> idle beenden; in Vanilla- und Bandits-Lua kein Aufruf), Ereignis `OnWorldSound`,
`getLastSoundRespondedTo()`, Pfadziel-Getter, `OnAIStateChange`, `getCurrentState()` als Text (Vanilla nur im Debug-Fenster
an Spielern). Stress-Ausgleich `animal:changeStress(x)` (Vanilla ISMilkAnimal.lua:28, belegt) ist eine Spielentscheidung:
nicht eingebaut, Kevins Wort.

## 4. Tests

Attrappen in `_arbeit/baer_laerm/attrappe/`, Lua 5.1, gegen `mod/42/media/lua`:
- `anim/test_anim.lua`: **528 Pruefungen, 0 fehlgeschlagen.** Das KI-Modell ist nachgebessert (Vorlage `make_real.py` des
  Pruefers): jede Wegsuche antwortet asynchron nach `W.pathDelay` Bildern (auch die Anfrage zum eigenen Standort),
  WalkingOnTheSpot (30 / 150) mit Failed -> shouldFollowWall, Weg zur Kachelmitte, bMoving; Ankunft bleibt PathFind;
  Aktionszustand je Bild ein Wechsel in der buck-Reihenfolge (`agNext`), followwall; klebendes shouldFollowWall als Startwert
  (`W.sfwStart`); Bildrate und Spieltempo einstellbar. FAIL-Zeilen gehen jetzt immer nach stdout (vorher nur mit VERBOSE).
  Neu Abschnitte 47 (walk/pathfind mit Wegzeit 1-5, klebendes shouldFollowWall, 20-30 Bilder/s, Tempo 4, EIN Schlag in
  Doppelschlag/Hieb/Biss, Engine-Ausflug, Sitzen mit EINEM Schlag, Fressen, Pause/Suche, followwall-Nachlauf, Lua-Reload,
  Dauerlaerm, Stress-Zeile) und 48 (Gegenproben-Faelle). **Modellgrenze:** das Modell ist selbst nur aus dem Jar abgeleitet
  (Antwortzeit der Wegsuche, Reihenfolge innerhalb eines Bildes, Lebensdauer des Laerms in Bildern); im Spiel ungeprueft.
- `kampf/test_fight.lua`: **114 Pruefungen, 0 fehlgeschlagen**, 4 SKIP (alte Regeln, wie vorher); Attrappe um
  `getVariableBoolean` ergaenzt.
- Gegenprobe `attrappe/mutate_laerm.py`: **34 von 35 Mutationen bemerkt** (Muster an den neuen Halt angepasst, 17 neue
  fuer die Nachbesserung). Nicht bemerkt wie vorher: "Stuck-Uhr beim Weglaufen nicht neu" (Sicherheitsnetz).
- Gegenprobe der neuen Pruefungen am Bau VOR der Nachbesserung (`vor_fix/NCBearFight.lua`, `FORCEFIX=1`): 91 von 508
  fehlgeschlagen, darunter genau die Befunde der Pruefer (walk-Halt, WalkingOnTheSpot, shouldFollowWall, Ruhe, Reload).

Messung (Attrappe mit dem nachgebesserten Modell, Wegzeit 3 Bilder, 60 Bilder/s, Zaunschlag 12 Kacheln entfernt, Ziel 1,2
Kacheln vorn; "alt" = Test-Mod, "vorher" = Bau vor der Nachbesserung):

| Fall | alt: Treffer / Flucht / Stress | vorher | nachgebessert |
|---|---|---|---|
| Schlag jede s, 20 s, Linie versperrt | 6 / 145 / 100, 60-s-Ruhe | 20 / 20 / 20 | 20 / 20 / 20 |
| dto., Linie frei (walk) | 1 / 36 / 36 | 4 / 57 / 57, 60-s-Ruhe | 19 / 20 / 20 |
| dto., walk, shouldFollowWall klebt | 1 / 36 / 36 | 3 / 51 / 51, 60-s-Ruhe | 19 / 20 / 20 |
| dto., 24 Bilder/s | 1 / 146 / 100, 60-s-Ruhe | 8 / 126 / 100 | 10 / 20 / 20 (Normaltempo, 6 per Uhr) |
| EIN Schlag im Doppelschlag bei 0,1 s | Treffer ja, 9 Fluchtbefehle | 1 Abbruch, WalkingOnTheSpot | Treffer aus der Animation, 1 Fluchtbefehl |
| Sitzen 30 s, EIN Schlag (shouldFollowWall) | sitzt weiter | Ruhe aus (5 Stoerungen) | sitzt weiter (1 Stoerung) |
| Dauerlaerm 300 s (Schlag alle 8 Bilder) | 2 / 797 / 100, 2 Ruhen | 1 / 314 / 100, 5 Ruhen | 65 (42 per Uhr) / 31 / 31, keine Ruhe |

Grenzfall (Messwert, Abschnitt 48d): Wegsuche 30 Bilder + klebendes shouldFollowWall + Dauerlaerm -> 0 Treffer, eine
60-s-Ruhe: die Animation pendelt die ganze Antwortzeit, ohne `setShouldFollowWall` (Jar) kein Hebel.

Pruefer auf `NCBearFight.lua`: luacheck ok, scopecheck 0 Verstoesse, localcount 97 aktiv / 146 insgesamt (Grenze 200),
luacheck_pz 2x W113 (`NCBearFight` global, Zeile 40/41) wie im Test-Mod-Stand, gewollt. Zeilenenden: nur LF, reines ASCII.
Alle anderen 17 Dateien in `mod/` byte-gleich zur Test-Mod (cmp).

## 5. Offen / ungeprueft

1. **Kern ungeprueft:** die Engine-Abfolge (Schild in AnimalPathFindState, Antwortzeit der Anfrage zum eigenen Standort,
   WalkingOnTheSpot, Reihenfolge der Uebergaenge, klebendes shouldFollowWall) ist aus dem Jar abgeleitet, nicht gespielt.
2. Die Grenze von WalkingOnTheSpot wird in Lua mit getMultiplier nachgezaehlt (Rand 3 Bilder). Bei Tempo 2/3 und wenig
   Bildern endet der Halt dadurch frueher als der Laerm und erneuert sich (mehr Neustarts, kein Stress).
3. Notloesung clockHit: unter Dauerlaerm steht der Baer im Wartebild und Zombies werden trotzdem getroffen. Ehrlich eine
   Notloesung; aus mit `NCBear_Tune("clockHit", 0)`. Der Doppelschlag (Treffer 1,3 s) trifft unter Dauerlaerm praktisch
   nur per Uhr.
4. Stress: je Schlag +1 (Maschendraht +2), Abbau rund 0,5 je Minute; bei Dauerlaerm durch den lauten Halt etwa +0,1 je s.
   Ab 60 eine laute Zeile; ab 70 kann er vor dem gehenden Spieler fliehen (B 4, ungeprueft). Ausgleich: Kevins Wort.
5. Welche Quelle in Kevins Garten wirklich feuerte: nur per Messung (log 2 zaehlt Zombies im Zustand thump).
6. Rand: "stands up to fight" mitten in einem Halt startet das Aufstehen aus der Sitzpose (kurzer Sprung moeglich).
7. MP: unveraendert aus.

## 6. Was Kevin im Spiel sehen soll (nach dem Kopieren und Spielneustart, bei Tempo 1)

- Gleicher Garten, Zombies am Zaun: der Baer schlaegt zu und trifft; keine Serie "did not finish ... the bear left idle".
  Eine Zeile "*** noise keeps interrupting the bear ..." nur, wenn drei Angriffe in Folge ganz ohne Treffer blieben
  (hoechstens alle 2 Minuten).
- Aufrichten nur noch EIN Schrei, auch wenn Laerm dazwischenkommt (dann rennt er direkt los).
- Kein "stuck on the way", nur weil er kurz vor Laerm weglief; er dreht um und rennt zum Ziel.
- Sitzen/Fressen: bei einem Schlag steht er kurz, setzt sich wieder hin; bei dauerndem Laerm steht er auf und bleibt stehen.
- Bei Stress ab 60 eine Zeile "*** bear stress ...".
- In der Konsole `NCBear_FightInfo()`: "noise interruptions ... | continuous-noise holds | engine walks ..." und je Baer der
  Stress. Fuer Einzelheiten `NCBear_Tune("log", 2)` ("stopped a move we did not order (..., held N frames)", "engine walk N
  frames after back in idle" = WalkingOnTheSpot). Vergleich ohne Neustart: `NCBear_Tune("fleeWait", 0)` (alte Stopp-Art),
  `NCBear_Tune("clockHit", 0)` (ohne Notloesung).
- Schlaegt Kevin den Baeren, flieht er weiter wie bisher (Kampf aus, "hurt").

## 7. Geaenderte Dateien (relativ zu `_arbeit/baer_laerm/mod`)

- `42/media/lua/shared/NCBearFight.lua` (einzige Mod-Datei; alle anderen kopierten Dateien byte-gleich zur Test-Mod)

Werkbank (nicht zum Kopieren): `attrappe/anim/test_anim.lua`, `attrappe/kampf/test_fight.lua`, `attrappe/mutate_laerm.py`.

## 8. Kevins Frage (Baerengroesse 1,35)

Gespawnt wird noch der kleine Baer: `42/media/lua/shared/NCBearDefs.lua:73-74` setzt `minSize`/`maxSize` = 1,0 (Test-Mod und
Kopie gleich). Die Stufen 0,35 / 0,75 / 1,35 sind erst geplant (`baer/STAND.md:41`, B1), Kevins Entscheidung fuer 1,35 steht
in `baer/begleiter/ENTSCHEIDUNGEN.md:10`. 1,35 geht nur vorlaeufig per `NCBear_Size(1.35)` (`client/NCBearSize.lua:27`,
setSizeForced), laut Kommentar dort nur bis der Baer einen Spieltag aelter wird.
