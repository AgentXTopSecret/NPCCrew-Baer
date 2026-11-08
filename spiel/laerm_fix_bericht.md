# Nachbesserung baer-laerm (08.11.2026)

Statisch geprueft, nicht gespielt. Geaendert nur im Arbeitsordner: `mod/42/media/lua/shared/NCBearFight.lua` (einzige
Mod-Datei), Werkbank `attrappe/anim/test_anim.lua`, `attrappe/kampf/test_fight.lua`, `attrappe/mutate_laerm.py`, Berichte
`bau_bericht.md` (nachgezogen) und dieser. Test-Mod NCBearTest nicht angefasst (Kevin spielt). Stand vor der Nachbesserung:
`vor_fix/` (NCBearFight.lua, test_anim.lua, test_fight.lua, mutate_laerm.py, bau_bericht.md). Nur SP, MP bleibt aus.
Zeilen unten = nachgebesserter Stand von `NCBearFight.lua` (kurz `F:`) bzw. `test_anim.lua` (kurz `T:`).

## Ergebnis

- Alle 15 Befunde berechtigt und behoben; Befund 11 (Stress) nur teilweise: Meldung und weniger Fluchtbefehle bei
  Dauerlaerm eingebaut, ein Stress-Ausgleich (`changeStress`, Vanilla ISMilkAnimal.lua:28) bleibt Kevins Wort.
- Kern: `fleeStop` hat jetzt EINEN Halt je Fluchtbefehl (`B.flee`), der ueber idle/followwall-Zwischenbilder haelt und vor
  WalkingOnTheSpot endet; dazu ein "lauter" Halt fuer Dauerlaerm. Drei weitere Luecken fand ich erst mit dem echten Modell
  (Abschnitt "Zusaetzlich").
- Attrappe mit dem Engine-Modell der Pruefer: 528 Pruefungen, 0 fehlgeschlagen; test_fight 114/0 (4 SKIP wie vorher);
  Gegenprobe 34 von 35 Mutationen bemerkt; Pruefer ok (Tabelle unten). Der Bau vor der Nachbesserung faellt mit den neuen
  Pruefungen 91-mal durch (`FORCEFIX=1`).

## Je Befund

| # | Befund (Datei:Zeile im Auftrag) | Urteil | Wo jetzt |
|---|---|---|---|
| 1 | major, walk-Halt haelt nicht (walk -> idle -> pathfind; das idle-Bild loeschte `B.flee`, das pathfind galt als neuer Befehl) -- NCBearFight.lua:991 | **behoben**, allgemeiner als der Vorschlag (statt "ein idle-Bild als Fortsetzung" gilt im Halt JEDES Bild als Fortsetzung, bis er endet). Der 1-Bild-idle zaehlt nicht als eigener Neustart (Zaehlung je Stoerung), Pause und Suche entscheiden nicht mitten im Halt, Kommentar neu. | F:1093-1186 (`fleeStop`), F:1056-1066 (`holdArm`), F:496-523 (`clipWatch`, Repeat-Marken), F:1326-1335 (`actClip` back), F:1699 (Pause), F:1708 (Suche), Kommentar F:1010-1036 |
| 2 | major, Attrappe gibt bPathfind in jedem Zustand Vorrang -- test_anim.lua:326 | **behoben**: `agNext` mit der Reihenfolge je Zustand (idle: walk > pathfind; walk: walk > idle > pathfind; pathfind: walk > followwall > idle; followwall: idle), ein Wechsel je Bild. walk-Zeilen neu gemessen: 19 Treffer / 20 Fluchtbefehle / Stress 20 (vorher in diesem Modell 4 / 57 / 57). | T:339-356, T:397; bau_bericht.md 4 |
| 3 | minor, Zeile je Uhr-Treffer schon bei log 1 -- :1085 | **behoben**: `sayMore`; Pruefung, dass bei log 1 keine, bei log 2 die Zeile kommt. | F:1250; T:2103, T:2124-2129 (Abschnitt 41) |
| 4 | minor, nil-Fallen nach Lua-Reload (`restarts`, `minI`, `reroutes`) -- :1162 | **behoben**: `(B.restarts or 0)`, `(B.reroutes or 0)`, `minI/bestI/progT` mit dI/F.clock vorbelegt; zusaetzlich wird ein alter Halt (`{cancel, n, ...}` ohne `armT`) verworfen. | F:1330, F:1411, F:1420-1421, F:1097-1101; T: Abschnitt 47 j |
| 5 | minor, Fundstellen-Kommentare (`getSquare`, `setVariable`) -- :1211 | **behoben**: Bandits BanditUpdate.lua:1852; Vanilla ISMilkAnimal.lua:139 neben Bandits ZAMove.lua:31 (an beiden setVariable-Stellen). | F:1377, F:1058-1059, F:454 |
| 6 | minor, Groesse: STAND.md:35 statt :41 -- bau_bericht.md:136 | **behoben**: STAND.md:41 und begleiter/ENTSCHEIDUNGEN.md:10 (selbst nachgelesen; NCBearDefs.lua:73-74 = 1,0). | bau_bericht.md 8 |
| 7 | major, das "Schild" haelt nur ~0,63 s (WalkingOnTheSpot) -- :976 | **behoben**: der Halt zaehlt ab der Antwort (Animation zurueck in idle) getMultiplier mit (`E.acc`) und endet 3 Bilder vor der Grenze (30, bei Tempo 4 150 ueber `UIManager.getSpeedControls():getCurrentGameSpeed()`, Vanilla ISBaseIcon.lua:61-62); normal endet er schon nach `fleeWait` Bildern mit einem Stopp im idle-Bild (die KI geht nach idle, kein Neustart). Lebt der Laerm noch (<= 17 Bilder), wird neu gehalten statt losgelassen. `getCurrentState()` nicht noetig (nur Jar/Debug). Attrappe hat WalkingOnTheSpot. | F:1040-1046, F:1135-1157, F:178-182; T:357-399; T: Abschnitt 47 a, c, d, e, 48 c |
| 8 | major, walk-Halt bricht an der Reihenfolge (gleicher Kern wie 1) -- :979 | **behoben** wie 1: `B.flee` haelt ueber idle-Bilder; pathfind/followwall/idle im Halt sind Fortsetzung; Stopp nur bei Rutschen (FLEE_MOVED), nach `fleeWait` oder vor WalkingOnTheSpot. | wie 1 |
| 9 | major, Ruhe: ein Schlag beendet Sitzen/Fressen (Ausfluege durch WalkingOnTheSpot) -- :1388 | **behoben**: keine WalkingOnTheSpot-Ausfluege mehr im Halt (7); Wiederholungen eines Halts zaehlen in `calmBack` nicht neu (nur die Clip-Uhr); Engine-Ausfluege zaehlen getrennt (`engineWalks`). Sitzen mit EINEM Schlag, Wegzeit 1-5, mit/ohne klebendes shouldFollowWall: sitzt weiter, 1 Stoerung. | F:1555-1562, F:1592; T: Abschnitt 47 g, 48 e |
| 10 | major, `shouldFollowWall` klebt im SP -- :991 | **behoben**, soweit Lua kann: followwall im Halt ist Fortsetzung (kein Stopp); ohne Halt ist followwall mit gesetztem `bPathfind` ein neuer Fluchtbefehl (Schritt 1, KI noch idle), ohne bPathfind nur Nachlauf eines Stopps. Das Pendeln pathfind -> followwall -> idle waehrend der Antwortzeit bleibt (Engine); loeschen koennte es nur `setShouldFollowWall(false)` -- **nur im Jar, braucht Kevins Wort**. Attrappe mit `W.sfwStart`. | F:1128-1134, F:1160-1169; T: Abschnitt 47 b, 48 d |
| 11 | major, Stress haelt Dauerlaerm nicht aus -- bau_bericht.md:108 | **teilweise behoben**: laute Zeile ab Stress 60 (`stressNote`, getStress ISMilkAnimal.lua:17, hoechstens alle 300 s, wieder scharf unter 50); bei Dauerlaerm der "laute" Halt (unten) -- 300 s Schlag alle 8 Bilder: Stress 31 statt 100, 31 statt 314 Fluchtbefehle. Bei einem Schlag je Sekunde bleibt +1 je Schlag (Engine). **Stress-Ausgleich mit `changeStress` (Vanilla ISMilkAnimal.lua:28) nicht eingebaut: Kevins Wort.** | F:1068-1083, F:183, F:1170-1185; T: Abschnitt 41, 47 k, 47 l |
| 12 | minor, laute Zeile auch bei getroffenen Angriffen -- :1116 | **behoben**: die Folge fuer die laute Zeile zaehlt nur Angriffe ohne jeden Treffer (Animation oder Uhr setzen sie zurueck); "attacks disturbed" zaehlt weiter alle. Text "ended without a hit". Aufrichten zaehlt nur noch in der Statistik. | F:1281-1288, F:1209-1218, F:1318 |
| 13 | minor, Zaehler mischen Laerm und Engine-Eigenheit -- :993 | **behoben**: "noise" nur je neuem Fluchtbefehl; walk im Halt zaehlt als `engineWalks` mit "engine walk N frames after back in idle" (log 2); FightInfo zeigt "continuous-noise holds" und "engine walks", je Baer den Stress. | F:1118-1127, F:2058-2061, F:2069-2070 |
| 14 | minor, Attrappe kann F1-F3 nicht abbilden -- test_anim.lua | **behoben**: Modell aus `make_real.py` uebernommen und erweitert (jede Anfrage asynchron nach `W.pathDelay`, auch zum eigenen Standort; WalkingOnTheSpot mit Failed; Ankunft bleibt PathFind; `agNext`; klebendes shouldFollowWall; Bildrate `W.dtNoise`, Tempo `W.multScale`/`W.gameSpeed`); Abschnitte 40/41/41b/44/46 laufen jetzt darin, neu 47 und 48. Modellgrenze im Bericht genannt. FAIL-Zeilen gehen jetzt immer nach stdout. | T:12, T:83, T:202-206, T:222-255, T:290-399, T:2003-2069, T:2370-2374, T:2348-, T:2595- |
| 15 | minor, Bericht 5.1: Failed fuehrt zur eigenen Kachel -- bau_bericht.md:101 | **behoben**: Text in Abschnitt 1 und 5 neu ("Mitte der eigenen Kachel"). | bau_bericht.md 1, 5 |

## Zusaetzlich (beim Messen mit dem echten Modell gefunden)

- **Halt bei Kampf-/Ruhe-Ende nicht stehen lassen:** `setBlock(false)` (endFight, calmEnd, goApproach) stoppt einen in diesem
  Bild laufenden Halt; sonst blieb die KI in AnimalPathFindState, WalkingOnTheSpot schickte ihn zur Kachelmitte und setzte
  shouldFollowWall fuer immer (in der Attrappe nach 90 s Dauerlaerm gesehen). Spielertreffer unveraendert (dort laeuft kein
  Halt "in diesem Bild", die Engine darf fliehen). F:434-464.
- **Spaeter Schritt 1:** ein Fluchtbefehl im Bild nach einem Halt-Ende liess die Animation pathfind -> followwall bzw.
  walk -> idle gehen; fleeStop sah kein pathfind und stoppte erst, als die KI schon in AnimalPathFindState war (Schild aus,
  zweiter Fluchtbefehl). Jetzt wird `bPathfind` gelesen: `getVariableBoolean("bPathfind")`, **Bandits ZAMove.lua:60**
  (am Zombie, gleiche Methode und Argument). F:1160-1169.
- **Dauerlaerm ("lauter" Halt):** kommt ein Fluchtbefehl hoechstens 2 Bilder nach einem Halt-Ende, lebte der Laerm noch. Dieser
  Halt laesst nach fleeWait nicht los, sondern erneuert sich vor WalkingOnTheSpot (Stopp + bPathfind, kein neuer
  Fluchtbefehl, kein Stress; hoechstens 3 Erneuerungen bzw. 240 Bilder, dann loslassen und pruefen), auch durch beginAct/goSeek
  hindurch (`setBlock`). Jede Erneuerung ist eine eigene Stoerung (Neustart-Deckel, Ruhe-Deckel). Pause/Suche warten im
  lauten Halt nicht. Wirkung (Attrappe, 300 s): 65 Treffer (42 per Uhr) statt 1, Stress 31 statt 100, keine 60-s-Ruhe.
  F:184-187, F:1115, F:1140-1147, F:1170-1176, F:453-460. **Bitte im Gegenpruefer bewerten** (neue Regel; ungeprueft im Spiel).
- `kampf/test_fight.lua`: Attrappe um `getVariableBoolean` ergaenzt (sonst "fight error"). Zeile 121.
- `mutate_laerm.py`: Muster an den neuen Halt angepasst, 17 Mutationen fuer die neuen Regeln. Neue Pruefungen fuer
  vorher unbemerkte Mutationen (T: Abschnitt 48: Deckel der lauten Zeile, Halt-Laenge, bPathfind-Lesen, Pendeln als eine
  Stoerung, Pause wartet, toter Halt nach Sperren, Frist bei festgehaltener Animation).

## Engine-Aufrufe neu in der Nachbesserung

| Aufruf | Fundstelle | Urteil |
|---|---|---|
| `a:getVariableBoolean("bPathfind")` | Bandits `shared/ZombieActions/ZAMove.lua:60` | belegt (gleiche Methode, gleiches Argument; dort am Zombie) |
| `UIManager.getSpeedControls():getCurrentGameSpeed()` | Vanilla `client/Foraging/ISBaseIcon.lua:61-62` (mit Riegel), `client/ISUI/ISBackButtonWheel.lua:25` | belegt; nur je neuem Fluchtbefehl |
| `a:setVariable("bPathfind", true)` (jetzt auch in setBlock) | Vanilla `ISMilkAnimal.lua:139`, Bandits `ZAMove.lua:31` | belegt (Methode/Typen), Wirkung am Tier aus dem Jar |
| `a:getStress()` (jetzt auch Stress-Zeile, FightInfo) | Vanilla `ISMilkAnimal.lua:17` | belegt |
| nur Jar, NICHT eingebaut | `setShouldFollowWall(false)`, `getCurrentState()`, `OnWorldSound`, `getLastSoundRespondedTo` | braucht Kevins Wort je Methode |

Kein neues `pcall`. Kosten je Bild und Baer (hoechstens 8): ein `getActionStateName`, im idle-Bild ohne Halt ein
`getVariableBoolean`, ein paar Vergleiche; `wotsLimit`, `getStress` und die Halt-Tabelle nur je neuem Fluchtbefehl.

## Pruefer und Attrappen (selbst gelaufen)

| Lauf | Ergebnis |
|---|---|
| `luacheck.py` NCBearFight.lua | ok, 0 failed |
| `scopecheck.py` | 0 Verstoesse |
| `localcount.py` | 97 aktiv / 146 insgesamt (Grenze 200, Warnung ab 180) |
| `luacheck_pz.py` | 2x W113 `NCBearFight` (Zeile 40/41), wie im Test-Mod-Stand, gewollt |
| `anim/test_anim.lua` gegen den Bau | **528 Pruefungen, 0 fehlgeschlagen** |
| dasselbe gegen `vor_fix/NCBearFight.lua` mit `FORCEFIX=1` | 91 fehlgeschlagen (Gegenprobe) |
| dasselbe gegen den Test-Mod-Stand (nur gelesen) | 337, 0 (die Laerm-Pruefungen laufen dort nicht) |
| `kampf/test_fight.lua` | 114 Pruefungen, 0 fehlgeschlagen, 4 SKIP (alte Regeln) |
| `mutate_laerm.py` | **34 von 35 bemerkt**; unbemerkt wie vorher "stuck clock not reset when it runs off" |
| Zeilenenden / Zeichen | NCBearFight.lua, test_anim.lua, test_fight.lua, mutate_laerm.py: nur LF, ASCII, Zeilenumbruch am Ende |
| uebrige 17 Dateien in `mod/` | byte-gleich zur Test-Mod (cmp) |

Aufruf: `METRICS=1 lua5.1.exe attrappe/anim/test_anim.lua mod/42/media/lua/shared/NCBearFight.lua mod/42/media/lua/client/NCBearBench.lua`

## Offen / ungeprueft

1. Alles zur Engine ist aus dem Jar abgeleitet (Schild, Antwortzeit, WalkingOnTheSpot, Uebergangsreihenfolge, klebendes
   shouldFollowWall); die Attrappe bildet nur dieses Modell ab. Im Spiel bei **Tempo 1** pruefen; log 2 zeigt "held N frames",
   "engine walk ..." (= WalkingOnTheSpot trotz Halt) und "continuous noise ...".
2. Grenzfall: sehr lange Wegsuche (30 Bilder) + klebendes shouldFollowWall + Dauerlaerm -> Angriffe brechen ab (Attrappe
   48d: 0 Treffer, eine 60-s-Ruhe). Hebel nur `setShouldFollowWall` (Jar, Kevins Wort).
3. Stress-Ausgleich (Kevins Wort). Der laute Halt verlangsamt den Anstieg nur.
4. Der laute Halt erneuert sich nach Laerm-Ende noch bis zu 3 Mal (je ein Clip-Neustart, rund 2 s).

## Kevins Frage

Nein, noch nicht 1,35: gespawnt wird der kleine Baer mit Groesse 1,0 (`NCBearDefs.lua:73-74`, Test-Mod und Kopie gleich).
1,35 ist beschlossen (`baer/begleiter/ENTSCHEIDUNGEN.md:10`) und fuer B1 geplant (`baer/STAND.md:41`); vorlaeufig nur per
Konsole `NCBear_Size(1.35)`, laut Kommentar in `client/NCBearSize.lua` bis der Baer einen Spieltag aelter wird.
