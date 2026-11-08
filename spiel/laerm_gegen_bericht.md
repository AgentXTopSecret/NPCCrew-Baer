# Gegenpruefung baer-laerm (08.11.2026)

Statisch geprueft, nicht gespielt. Geprueft wurde der nachgebesserte Stand `mod/42/media/lua/shared/NCBearFight.lua` (2073 Zeilen)
gegen `vor_fix/NCBearFight.lua` und den Stand der Test-Mod. Der Code wurde selbst gelesen und nicht aus dem Bericht uebernommen.
Alle Pruefer und Attrappen liefen selbst, die Engine-Fundstellen wurden stichprobenartig selbst geoeffnet, dazu kam eine eigene
Gegenprobe im Scratch. Im Bau wurde nichts geaendert, in NCBearTest nichts geschrieben (git status sauber, keine Datei neuer als
`forschung_laerm.md`). Das Spiel lief waehrend der Pruefung nicht (`tasklist`). Nur Einzelspieler, MP bleibt aus (isSP-Riegel
unveraendert, `onTick` :1866, `hook` :1889).

## 0. Urteil

- **Bereit, in die Test-Mod kopiert zu werden (SP-Test).** Es gibt keinen blocker und keinen neuen major.
- **Die 7 major-Befunde der Pruefer sind im Code behoben** (Abschnitt 2):
  - Technik 1 und 2, Logik 1 bis 4: behoben.
  - Logik 5 (Stress): nur teilweise behoben, wie der Bericht ehrlich sagt. Der Ausgleich braucht Kevins Wort.
- **Die zwei ungefragten neuen Regeln sind vertretbar** (Abschnitt 3):
  - `setBlock(false)` stoppt einen laufenden Halt.
  - Der "laute" Halt hilft bei Dauerlaerm. Er hat aber einen sichtbaren Preis: Unter Dauerlaerm kommt rund die Haelfte bis drei
    Viertel der Treffer per Lua-Uhr, also ohne passenden Prankenhieb im Bild.
- **Neu gefunden: 2 minor und 2 Hinweise** (Abschnitt 6):
  - `refreshBlock` prueft das falsche Bild (toter Zweig).
  - Bei freier Linie und wenig Bildern pro Sekunde steigen Fluchtbefehle und Stress unter Dauerlaerm weiter deutlich (nur im
    Modell gemessen).
  - Die Zahl der Gegenprobe im Bericht ist veraltet.
  - Die Konsolenbefehle stehen weiter in der shared-Datei (bekannt, B1).

## 1. Selbst gelaufen

| Lauf | Ergebnis |
|---|---|
| `luacheck.py` | ok, 0 failed |
| `scopecheck.py` | 0 Verstoesse |
| `localcount.py` | 97 aktiv / 146 insgesamt (Grenze 200, Warnung ab 180); groesste Funktion `updateBear` 26 |
| `luacheck_pz.py` | 2x W113 `NCBearFight` (:40/:41), gewollt wie in der Test-Mod |
| `anim/test_anim.lua` gegen den Bau (`METRICS=1`) | **528 Pruefungen, 0 fehlgeschlagen** |
| dasselbe gegen `vor_fix/` mit `FORCEFIX=1` | 528, **102 fehlgeschlagen** (Bericht: "91 von 508", siehe 6.3) |
| dasselbe gegen den Test-Mod-Stand (nur gelesen) | 337, 0 |
| `kampf/test_fight.lua` | 114 Pruefungen, 0 fehlgeschlagen, 4 SKIP (alte Regeln) |
| `mutate_laerm.py` (Kopie im Scratch) | **34 von 35 bemerkt**; unbemerkt wie vorher nur "stuck clock not reset when it runs off" |
| Zeilenenden NCBearFight.lua | 2073 LF, 0 CR, 0 Nicht-ASCII, Zeilenumbruch am Ende |
| uebrige 17 Dateien in `mod/` | byte-gleich zur Test-Mod (`cmp`); nur NCBearFight.lua weicht ab |

## 2. Die major-Befunde im Code

| Befund (fix_bericht #) | Stelle jetzt | Urteil |
|---|---|---|
| Technik 1 / Logik 2 (#1, #8): walk-Halt bricht an walk -> idle -> pathfind | `fleeStop` :1102-1159. Im Halt loescht idle `B.flee` nicht mehr, sondern zaehlt als Fortsetzung (:1135-1158); pathfind/followwall im Halt sind ebenfalls Fortsetzung (:1128-1134). Pause und Suche entscheiden nicht mitten im Halt (:1699, :1708). | **behoben.** Die Mutation "hold dropped on idle" faellt mit 85 Pruefungen durch. 47a walk mit Wegzeit 1-5: 18-20 Treffer, 20 Fluchtbefehle (vorher im Modell 3-4 / 51-57). |
| Technik 2 (#2): Attrappe gibt bPathfind ueberall Vorrang | `agNext` T:339-356 | **behoben.** Gegen die XML in `media/actiongroups/buck/{idle,walk,pathfind,followwall}` selbst nachgelesen: idle `to_walk`(2) > `to_pathfind`; walk `to_walk`(2) > `to_idle` > `to_pathfind`; pathfind `to_walk`(2) > `to_followwall` > `to_idle`; followwall `to_idle` (bMoving false bzw. shouldFollowWall false). Das stimmt. |
| Logik 1 (#7): Schild nur ~0,63 s (WalkingOnTheSpot) | `near` :1139 mit `E.wl = wotsLimit()` :1040-1046, Rand 3 Bilder | **behoben.** Jar selbst gelesen (`WalkingOnTheSpot.check` Offset 0-31, Dump im Scratch): Tier 30, bei `SpeedControls.instance.getCurrentGameSpeed() == 4` 150, nicht auf dem Server. Je Aufruf kommt `GameTime.getMultiplier()` dazu, solange er unter 0,1 Kacheln steht. `UIManager.getSpeedControls()` ist dasselbe Objekt wie `SpeedControls.instance` (UIManager.<clinit> Offset 39-52, `jar/gegen/UIManager.txt`). `E.acc += F.rawMult` (= `getGameTime():getMultiplier()`) zaehlt also dieselbe Groesse. 48c: Halt 20 Bilder, KI danach idle; 47f: kein Failed. |
| Logik 3 (#9): ein Schlag beendet Sitzen/Fressen | `calmBack` :1555-1562 (Wiederholung im Halt: nur die Uhr neu) | **behoben.** 47g: Sitzen mit EINEM Schlag, Wegzeit 1-5, mit und ohne klebendes shouldFollowWall: sitzt weiter, `noiseCalm 1`, `tooMuch 0`. |
| Logik 4 (#10): klebendes shouldFollowWall | followwall im Halt ist Fortsetzung (:1128); ohne Halt ist followwall/idle mit `bPathfind` ein Fluchtbefehl (:1163-1164) | **behoben, soweit Lua kann.** Die Mutation "followwall in a hold stops" faellt mit 40 Pruefungen durch. Rest: das Pendeln waehrend der Wegsuche; dagegen hilft nur `setShouldFollowWall` (nur im Jar, Kevins Wort). Grenzfall 48d steht ehrlich im Bericht. |
| Logik 5 (#11): Stress in lauten Basen | `stressNote` :1071-1083 (Zeile ab 60); der laute Halt senkt die Zahl der Fluchtbefehle | **teilweise.** Eigene Gegenprobe (Abschnitt 5): EIN Zombie, der etwa jede Sekunde schlaegt, gibt weiter rund 1 Fluchtbefehl je Schlag, also **Stress 55 nach 60 s** und 70 nach etwa 75 s. Erst ab 3 Zombies greift der laute Halt (20-30 in 60 s). Ausgleich `changeStress` (Vanilla `ISMilkAnimal.lua:28`, selbst gesehen) nicht eingebaut: Kevins Wort. |

Kleine Befunde (#3 bis #6, #12 bis #15) stichprobenartig angesehen:
- #3: Uhr-Treffer-Zeile nur noch per `sayMore` :1250.
- #4: nil-Waechter :1330, :1411, :1420; alter Halt ohne `armT` wird verworfen (:1098).
- #5: Fundstellen-Kommentare :1377, :1058-1059, :454.
- #12: Folge fuer die laute Zeile nur bei Angriffen ohne Treffer (:1283).
- #13: `engineWalks` getrennt gezaehlt (:1118).
- Alles in Ordnung.

## 3. Neue Regeln der Nachbesserung (bewertet)

**3.1 `setBlock(false)` stoppt einen laufenden Halt (:441-448).**
- `live` verlangt `E.tick == F.ticks`, also dass fleeStop in DIESEM Bild lief.
- Der Spielertreffer-Zweig in `updateBear` (:1671-1680) kehrt vor jedem fleeStop zurueck. `live` ist dort falsch, die Engine darf
  wie bisher fliehen (fleeFromAttacker). Kein Rueckschritt.
- `releaseAll`/`scanBears` laufen ausserhalb des Halt-Bildes und sind nicht betroffen.
- Nach `goApproach` setzt das naechste `updateApproach` ohnehin `fleeTo` (`issueT = -1000`).
- **Urteil: richtig und noetig.** Sonst bliebe die KI nach dem Kampf in AnimalPathFindState, und WalkingOnTheSpot setzt
  shouldFollowWall.

**3.2 Der "laute" Halt (:1115, :1140-1148, :1173, :453-460).**

Mechanik selbst belegt:
- `BaseAnimalBehavior.setBlockMovement(true)` ruft IMMER `stopAllMovementNow` (`baer_angriff/BaseAnimalBehavior.txt:5753-5767`,
  Offset 0-8), auch wenn schon gesperrt. Der Zweig in setBlock ist damit gleichwertig zu `holdArm` (Stopp + bPathfind).
- `IsoAnimal.update` Offset 29-61 betritt AnimalPathFindState bei `getVariableBoolean("bPathfind")` VOR `updateInternal`, also vor
  respondToSound (`baer_angriff/IsoAnimal.txt:921-961`). Das Schild bleibt damit an.
- Laerm lebt 16 Bilder (`WorldSound.init` Offset 6 `bipush 16`, je `WorldSoundManager.update` -1, `dump/...WorldSoundManager.txt`
  Offset 162-169). `NOISE_FRAMES 17` stimmt.

Deckel:
- `LOUD_REARMS 3` und `LOUD_FRAMES 240`; das Alter laeuft ab `E.t0` und wird auch von den setBlock-Erneuerungen nicht
  zurueckgesetzt.
- Ein lauter Halt dauert also hoechstens 240 Bilder, dann laesst er los und prueft. Kein endloses Haengen.

Wirkung (Attrappe und eigene Gegenprobe):
- Bei Dauerlaerm halbieren sich die Fluchtbefehle.
- Treffer kommen wieder (vorher 0-1).
- Preis: Jede Erneuerung startet den Angriffs-Clip neu (rund alle 0,5 s). Dadurch kommen 50-75 % der Treffer per Lua-Uhr
  (41: 42 von 65; eigene Probe 3-6 Zombies: 20-29 von 41-44). Kevin sieht dann einen Zombie fliegen, ohne dass der Hieb im Bild
  ganz durchlaeuft.
- Das ist ehrlich als Notloesung markiert und abschaltbar (`NCBear_Tune("clockHit", 0)`).

**Urteil: behalten.** Ob das Bild unter Dauerlaerm stoert, entscheidet Kevin im Spiel.

**3.3 `bPathfind` lesen (:1164).** Die Engine liest dieselbe Variable am Tier selbst auf dieselbe Weise (IsoAnimal.update Offset
29-33, Jar). Die Lua-Fundstelle Bandits `ZAMove.lua:60` (am Zombie) ist selbst gesehen. Vanilla nutzt die Methode auch an Spielern,
z. B. `client/ISUI/ISFitnessUI.lua:245`. Der Kommentar koennte diese Stelle zusaetzlich nennen; kein Fehler.

## 4. Engine-Fundstellen (Stichprobe, selbst geoeffnet)

| Aufruf | Fundstelle | Ergebnis |
|---|---|---|
| `a:getVariableBoolean("bPathfind")` | Bandits `shared/ZombieActions/ZAMove.lua:60` | gesehen, gleiche Methode und Argument |
| `UIManager.getSpeedControls():getCurrentGameSpeed()` | Vanilla `client/Foraging/ISBaseIcon.lua:61-62` (mit Riegel), `client/ISUI/ISBackButtonWheel.lua:25` | gesehen; der Riegel ist in `wotsLimit` nachgebaut |
| `a:setVariable("bPathfind", true)` | Vanilla `ISMilkAnimal.lua:139` (`setVariable("milkanimalout", false)`), Bandits `ZAMove.lua:31` | gesehen |
| `a:getStress()` | Vanilla `ISMilkAnimal.lua:17` | gesehen |
| `z:getSquare()` | Bandits `client/BanditUpdate.lua:1852` | gesehen |
| `stopAllMovementNow()` | Vanilla `ISAnimalContextMenu.lua:760` | gesehen |
| nur Jar, richtig NICHT eingebaut | `setShouldFollowWall`, `getCurrentState`, `OnWorldSound`, `getLastSoundRespondedTo`, `changeStress`-Ausgleich (Vanilla belegt, aber Spielentscheidung) | ok |

Kein neues `pcall`. Das einzige bleibt in `onTick` (:1873); es meldet laut und schaltet ab, ist also keine Tarnkappe.

## 5. Eigene Gegenprobe (Scratch, nicht im Bau)

- Datei: `...\scratchpad\gegen\probe_anim.lua`, `probe2.lua`, `probe3.lua`. Das ist `test_anim.lua` mit einem angehaengten
  Block und demselben Engine-Modell.
- Abweichend von den vorhandenen Tests: **1, 3 oder 6 Zombies schlagen unregelmaessig**, jeder alle 0,8 bis 1,4 s (fester
  Zufallskeim). Dazu jede Kombination aus Linie frei, klebendem shouldFollowWall, Wegzeit 2/3/5 und 60/40/30/20 Bildern je
  Sekunde, je 60 s.
- Das Modell ist selbst nur aus dem Jar abgeleitet und ungeprueft.

| Fall (60 s) | neu: Treffer (Uhr) / Flucht / Stress / Drift | vor_fix |
|---|---|---|
| 60 Bilder/s, Linie versperrt (Garten), 1 Zombie | 42-43 (0) / 55 / 55 / 0 | 46 (13) / 379 / 100 |
| dto., 3 Zombies | 41-43 (20-25) / 25-30 / 25-30 / 0 | 0-1 / 50-59, 60-s-Ruhe |
| dto., 6 Zombies | 41-44 (23-29) / 20-23 / 20-23 / 0 | -- |
| 60 Bilder/s, Linie frei, 3 Zombies | 43 (19-22) / 43-53 / 43-53 / 2,8-3,2 | 0 / 114 / 100 |
| 30 Bilder/s, Linie frei, 3 Zombies | 36-39 (23) / **80-86** / **80-86** / **8-9** | 0 / 62 / 62 |
| 20 Bilder/s, Linie frei, 1-3 Zombies | 28-35 (30-36) / **76-94** / **76-94** / **13,4-13,8** | 0-1 / 30-41 |
| Maschendraht (Radius 40), 3 Zombies | 44 (23) / 27 / **54** / 0 | -- |
| 300 s, 3 Zombies | 65 (33) / 46 / 46 / 0, keine Ruhe | -- |

Was die Probe zeigt:
- Ueberall gilt: **keine 60-s-Ruhe, keine "***"-Serien, Treffer statt 0.** Die einzige "***"-Zeile ist die neue Stresszeile ab 60.
  Das ist eine deutliche Verbesserung gegen vor_fix in jedem Fall.
- Schwaechen: Stress bei EINEM schlagenden Zombie (6.4) und der Fall "Linie frei + wenig Bilder/s" (6.2).

## 6. Befunde

### 6.1 (minor) `refreshBlock` prueft das falsche Bild -- :477

- `refreshBlock` laeuft in `updateBear` (:1682) VOR fleeStop. `B.flee.tick` stammt dann aus dem Vorbild, also ist
  `B.flee.tick == F.ticks` nie wahr und `B.holdEndT` wird nie gesetzt.
- Folgen, rund alle 83 s gesperrter Zeit:
  - Der Stopp aus `setBlockMovement(true)` beendet einen laufenden Halt mitten im Lauf. Die KI verlaesst PathFind, das Schild ist
    aus.
  - Lebt der Laerm noch, kommt ein neuer Fluchtbefehl (+1 Stress), und er wird nicht als Dauerlaerm erkannt.
  - Steht die Animation gerade auf pathfind, zaehlt fleeStop im selben Bild einen falschen "noise".
- Harmlos, aber der Kommentar :476 verspricht etwas anderes.
- Vorschlag: waehrend eines Halts nicht erneuern, also `if B.flee and B.blockRaw < 7000 then return end` vor dem Erneuern.
  Bis zur Engine-Grenze 8000 bleiben genug Bilder, ein Halt dauert hoechstens 240 Bilder.
- Die Attrappe sieht das nicht: Keine Pruefung laeuft 83 s mit Halt UND Laerm genau im Erneuerungsbild.

### 6.2 (minor, nur Modell) Linie frei + wenig Bilder/s: Fluchtbefehle und Stress bleiben hoch -- fleeStop/decide

Beobachtung:
- Bei 20 bis 30 Bildern je Sekunde und freier Linie bringen 1-3 schlagende Zombies 76-94 Fluchtbefehle und Stress 76-94 in 60 s.
  Der Baer rutscht dabei 8-14 Kacheln.
- Bei 60 Bildern/s sind es 43-53 statt 25-30 im Garten-Fall.

Ablauf (Spur in `...\scratchpad\gegen\p3.txt`, Bild 899-946):
1. Jede walk-Flucht bewegt ihn ein Bild lang, bevor OnTick stoppt; das ist die Reihenfolge der Engine, Lua kann sie nicht aendern.
   Bei 20 Bildern/s sind das 0,2 Kacheln je Flucht.
2. Nach einigen Fluchten steht er falsch zum Ziel: `decide` -> `goApproach` -> `setBlock(false)` beendet den lauten Halt.
3. `fleeTo`, Ankunft, `beginAct` -> Stopp -> Schild aus -> der Laerm lebt noch -> neue Flucht, aber nicht "laut", weil seit dem
   Halt-Ende mehr als 2 Bilder vergingen.

Einordnung:
- Kein Fehler im Lua-Ablauf.
- vor_fix ist in denselben Faellen schlechter: 0 Treffer, bis Stress 100.
- In Kevins Garten (Zaun, Linie versperrt) greift der Fall nicht.
- Offen fuer offenes Gelaende; im Spiel mit `NCBear_FightInfo()` (flee stops, Stress) beobachten.

### 6.3 (Hinweis) Zahl der Gegenprobe im Bericht veraltet

- `fix_bericht.md` und `bau_bericht.md` 4 nennen "91 von 508". Selbst gemessen am heutigen `test_anim.lua`: 102 von 528.
- Die Attrappe wuchs nach der Zaehlung. Die Aussage (die neuen Pruefungen fangen den alten Bau) stimmt trotzdem.

### 6.4 (Hinweis, offen) Stress mit EINEM Zombie am Zaun

- Der laute Halt greift erst, wenn der naechste Fluchtbefehl hoechstens 2 Bilder nach einem Halt-Ende kommt.
- Ein einzelner Zombie, der etwa jede Sekunde schlaegt, gibt weiter +1 je Schlag, also 70 nach rund 75 s (Maschendraht +2).
- Der Stress-Ausgleich ist Kevins Entscheidung (Befund 11 bleibt offen).
- In der Praxis toetet der Baer den Zombie meist vorher; ungeprueft.

### 6.5 (Hinweis, bekannt) Konsolenbefehle in der shared-Datei

- `NCBear_Fight`, `NCBear_Tune` und `NCBear_FightInfo` stehen schon in der Test-Mod in `shared/NCBearFight.lua`. Die Nachbesserung
  hat FightInfo nur erweitert.
- Nach Regel 2 der Werkstatt muessen sie vor einer Uebernahme nach NPC Crew in eine Bench-Datei bzw. vom Uebernahme-Skript
  herausgenommen werden.
- Das steht als B1-Aufgabe in `baer/STAND.md`. Kein Thema fuer diesen Lauf.

## 7. Offen / ungeprueft

1. Die ganze Engine-Abfolge ist aus dem Jar abgeleitet und nicht gespielt: Schild in PathFind, Antwortzeit der Anfrage zum eigenen
   Standort, WalkingOnTheSpot, Reihenfolge der Uebergaenge, klebendes shouldFollowWall. Die Attrappe bildet nur dieses Modell ab.
2. Stress-Ausgleich (`changeStress`, Vanilla `ISMilkAnimal.lua:28`): Kevins Wort.
3. `setShouldFollowWall(false)` gegen das Pendeln (Grenzfall 48d): nur im Jar, Kevins Wort.
4. Unter Dauerlaerm kommen die meisten Treffer per Lua-Uhr (Bild und Schaden laufen auseinander): Kevins Urteil im Spiel.
5. 6.1 (`refreshBlock`), wenn gewuenscht, vor oder nach dem Kopieren als Einzeiler.
6. 6.2: freie Linie bei wenig Bildern/s.

## 8. Kevins Frage: ist der Baer schon 1,35?

**Nein, gespawnt wird noch der kleine Baer mit Groesse 1,0.**
- `NCBearTest/42/media/lua/shared/NCBearDefs.lua:73-74` setzt `minSize = 1.0` und `maxSize = 1.0`, selbst gelesen. Kein anderer
  Lua-Ort setzt eine Groesse; per grep gefunden wurde nur `NCBearSize.lua`.
- 1,35 ist Kevins Entscheidung (`baer/begleiter/ENTSCHEIDUNGEN.md:10`) und fuer B1 geplant (`baer/STAND.md:41`: 0,35 / 0,75 / 1,35).
- Bis dahin geht es nur von Hand mit `NCBear_Size(1.35)` (`client/NCBearSize.lua:27`, `setSizeForced`, Vanilla
  `ButcheringUtil.lua:569`). Das wirkt auf Baeren in 20 Kacheln Umkreis. Laut Kommentar :3-4 haelt es, bis der Baer einen Spieltag
  aelter ist (nicht selbst geprueft).

## 9. Fuer Kevin (nach dem Kopieren, Spiel neu starten, Tempo 1)

- Gleicher Garten mit Zombies am Zaun: Der Baer soll zuschlagen und treffen. In der Konsole soll keine Serie
  "*** ... did not finish ... left idle" mehr kommen.
- Aufrichten: nur noch EIN Schrei.
- Bei dauerndem Zaun-Haemmern fliegen Zombies, ohne dass der Hieb ganz zu sehen ist (Notloesung). Kevin sagt, ob das stoert.
- Ab und zu `NCBear_FightInfo()` eintippen und den Stress des Baeren ansehen; ab 60 kommt eine "***"-Zeile.

## 10. Scratch (nur Versuche, nicht zum Kopieren)

`C:\Users\Kevin\AppData\Local\Temp\claude\086a7114045651dc\cccbd9d6-dd89-4eba-8fad-b3beed093bcb\scratchpad\gegen\`:
- `probe_block.lua`, `probe_anim.lua`, `probe2.lua`: Gegenprobe Abschnitt 5
- `trace_block.lua`, `probe3.lua`, `p3.txt`: Spur zu 6.2
- `gegen_mut\`: Kopie fuer `mutate_laerm.py`

Jar-Auszug: `_arbeit/baer_laerm/jar/gegen/` (UIManager, SpeedControls, javap -c -p).
