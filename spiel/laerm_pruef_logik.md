# Pruefung baer-laerm: Logik und Wirkung (08.11.2026)

Statisch geprueft, nicht gespielt. Geprueft: `mod/42/media/lua/shared/NCBearFight.lua` (neu, 1893 Zeilen) gegen
`Zomboid/mods/NCBearTest/42/media/lua/shared/NCBearFight.lua` (alt, nur gelesen), `bau_bericht.md`, `forschung_laerm.md`,
`forschung_zustand.md`, die Attrappe `attrappe/anim/test_anim.lua` (laeuft: 366 Pruefungen, 0 fehlgeschlagen, nachgezaehlt) und
die Jar-Dumps (`B_*.txt`, `dump/*.txt`). Nichts im Bau geaendert. Eigene Gegenrechnung nur im Scratchpad (Abschnitt 3).

## 0. Urteil

- **Kevins Garten (Fluchtlinie durch den Zaun versperrt, Fall "pathfind"), Schlag etwa jede Sekunde: der Fix verbessert die Lage
  sehr wahrscheinlich deutlich.** Hiebe und Bisse landen wieder; im eigenen Modell 20 statt 6 Treffer in 20 s, 20 statt 145
  Fluchtbefehle. Das liegt aber vor allem an der Neustart-Behandlung und an der Notloesung `clockHit`, nicht an einem stabilen
  "Schild".
- **Die Kernannahme des Berichts stimmt so nicht.** Laut Bericht 5.1 bleibt die KI nach geglueckter Anfrage zum eigenen Standort in
  AnimalPathFindState, und das Schild haelt "bis zu unserem naechsten Stopp". Laut Jar endet das Stillstehen in
  AnimalPathFindState nach rund 0,63 s von selbst (WalkingOnTheSpot, F1). Dann setzt die Engine `bMoving`, und der Clip bricht
  wieder ab, auch ohne neuen Laerm. Die Attrappe bildet das nicht ab. Ihre Zahlen ("1 Fluchtbefehl je Schlag", "Doppelschlag
  trifft aus dem Neustart") stammen aus einem Modell ohne F1 bis F3.
- **Ruhe (Sitzen, Fressen) wird schlechter als vorher:** Ein einziger Schlag kann die Ruhe nach etwa 3 s beenden (F1, Befund 3).
- **Fall "walk" (Linie frei, offenes Gelaende):** das Halten scheitert an der Reihenfolge der Uebergaenge (F2), sobald die Engine
  fuer die Wegsuche 3 oder mehr Bilder braucht. Dann kommt alle 3 Bilder ein neuer Fluchtbefehl, und die 60-s-Ruhe kommt zurueck.
- **Klebriges `shouldFollowWall` (F3):** ist der Schalter einmal gesetzt, faellt auch der Fall "pathfind" ins alte Ping-Pong zurueck
  (mehr Fluchtbefehle, mehr Stress). Treffer landen trotzdem meist.
- **Stress in Basen:** selbst im besten Fall +1 je Schlag (+2 am Maschendraht). Der Abbau ist fast null. In einer lauten Basis ist
  Stress 70 nach etwa 1 bis 2 Minuten erreicht (Befund 5).
- Spielertreffer, Ziel hinter dem Zaun, Knockback, Rueckweg, mehrere Baeren und das Laden eines Spielstands: kein Rueckschritt
  gefunden (Abschnitt 4).
- Die Notloesung ist ehrlich markiert (Abschnitt 5).

## 1. Engine-Fakten, die Bau und Attrappe fehlen (alles Jar, javap -c -p)

**F1 WalkingOnTheSpot beendet das Stillstehen in AnimalPathFindState.**
- `PathFindBehavior2.update(float)`: Ist die Anfrage "found", ruft die Methode JEDES Bild `walkingOnTheSpot.check(chr)` auf und gibt
  bei true `Failed` zurueck. Das steht vor `setMoving(true)` und vor `Succeeded` (`B_PathFindBehavior2.txt:3123-3135`, Offset
  461-495; Succeeded erst Offset 1247-1255, Zeile 3469). Zurueckgesetzt wird der Zaehler nur in `reset()` und beim Absenden einer
  Anfrage (Offset 82-94 bzw. 148-166).
- `WalkingOnTheSpot.check(IsoGameCharacter)`: Bei einem Tier liegt die Grenze bei 30, bei Spieltempo 4 bei 150 (Offset 0-31).
  Steht er naeher als 0,1 Kachel am gemerkten Punkt, kommt je Aufruf `getMultiplier` dazu; bei `time > 30` gibt die Methode true
  zurueck (Offset 32-133). Belegt aus `_arbeit/baer_kampf/jar/zombie/ai/WalkingOnTheSpot.class`, Dump im Scratchpad (Abschnitt 3).
  30 entspricht 30/48 = **0,63 s Animationszeit** bei Tempo 1 bis 3, bei Tempo 4 sind es 3,1 s.
- Bei Failed fuehrt `AnimalPathFindState.execute` (Offset 13-71, `B_AnimalPathFindState.txt`) drei Schritte aus:
  `pathFailed`, `setShouldFollowWall(true)` und `PFB2.pathToLocation(getPathTarget)`, dazu **`bMoving = true`**. Die KI bleibt
  PathFind, `bPathfind` ist nach Succeeded false. Darum geht die Animation idle -> walk (`idle/to_walk.xml`): unser Knoten ist
  weg, ohne neuen Laerm.
- Ablauf also: Die Anfrage gelingt, die Animation geht nach idle (Neustart 1), dann bleiben 0,63 s Schild. Danach folgt ein
  walk-Ausflug durch WalkingOnTheSpot: Neustart 2, oft auch 3 (F2/F3). Das wiederholt sich alle rund 0,66 s, bis jemand die KI
  nach idle holt (`beginAct`/`goSeek` ueber setBlock -> stopAllMovementNow). In act/calm/pause/seek holt unser `fleeStop` sie
  wegen des walk-Halts sogar jedes Mal nach PathFind zurueck (:1010-1015).

**F2 Die Reihenfolge der Uebergaenge je Zustand zaehlt, nicht "bPathfind vor bMoving".**
- `ActionState.load` sortiert die Dateien mit `Collator` (ENGLISH) und parst sie in dieser Reihenfolge (`B_ActionState.txt:274-318`).
  `sortTransitions` sortiert stabil nach `conditionPriority`, dann nach Zahl der Bedingungen, absteigend (:557-632).
  `evaluateCurrentStateTransitions` nimmt den ERSTEN passenden Uebergang (`B_ActionStateContainer.txt:256-335`, Offset 152-160).
  `defaultTransitions.xml` laedt die ActionGroup gar nicht (`ActionGroup.load` liest nur Unterordner, `B_ActionGroup.txt:36-106`).
- `walk`: `to_idle` (isFalse bMoving) steht vor `to_pathfind` (isTrue bPathfind). Mit bMoving=false und bPathfind=true geht
  es also **walk -> idle**, erst im naechsten Bild idle -> pathfind.
- `pathfind`: `to_followwall` (isTrue shouldFollowWall) steht vor `to_idle`.
- Die Attrappe rechnet den Zustand ohne Gedaechtnis als `bPathfind and "pathfind" or (moving and "walk" or "idle")`
  (`test_anim.lua`, kiStep). Sie springt also walk -> pathfind direkt und kennt followwall nicht.

**F3 `shouldFollowWall` bleibt im Einzelspieler kleben.**
- Gesetzt wird der Schalter bei jedem Failed in AnimalPathFindState (F1 oder ein unerreichbares Fluchtziel im Zaungarten).
  Geloescht wird er nur in AnimalFollowWallState (`B_AnimalFollowWallState.txt:390-511`, 1106, 1129) und in
  `IsoAnimal.removeFromWorld` (`dump/...IsoAnimal.txt:3622`).
- In AnimalFollowWallState kommt die KI im SP nie. Eine Suche ueber alle Klassen im Jar (zipfile) findet die Klasse nur in sich
  selbst und in IsoAnimal (`initializeStates` :2276, `isAnimalMoving` :6077). Der Weg ueber den Namen (`tryGetAIState`) laeuft
  nur im MP-Client (`B_ActionContext.txt:230`, transferActionState Offset 135-166 unter `GameClient.client`).
- Folge: Jeder Ausflug nach pathfind springt im Bild danach auf followwall. `fleeStop` stoppt dort sofort (:991-994, kein Halten),
  die KI verlaesst PathFind, und das Schild ist aus. Das ist wieder das alte Ping-Pong mit einem Zustand mehr.

**F4 Kleine Korrektur zu Bericht 5.1.** Bei Failed geht er nicht "zum alten Fluchtziel". `PFB2.reset` setzt targetX/Y/Z auf die
eigene Position (`B_PathFindBehavior2.txt:194-241`, Offset 33-54), und `getPathTargetX` = `fastfloor(PFB2.getTargetX)`
(`dump/...IsoGameCharacter.txt:8588`). Ziel ist also die Mitte der eigenen Kachel. An der Wirkung (fleeStop stoppt) aendert das
nichts.

Gegengeprueft und bestaetigt: Die KI ist im Bild der Flucht noch idle (`AnimalIdleState.execute` prueft kein bPathfind,
`B_AnimalIdleState.txt` Offset 0-90). Der Stopp in Schritt 1 laesst bPathfind stehen (`stopAllMovementNow` :1574,
changeRootState-No-op). Im Bild danach greift `IsoAnimal.update` Offset 29-61 VOR `respondToSound`, das Schild steht also.
`actionStateChanged` ist leer (`IsoGameCharacter.txt:34392`); die KI folgt der Animation im SP nicht.

## 2. Bild fuer Bild

**2.1 Garten, Fall pathfind, shouldFollowWall noch false (bester Fall).**
- N: respondToSound -> pathToAux: bPathfind=true. Die Animation geht idle -> pathfind (Clip weg). Bei OnTick folgt Schritt 1:
  der Stopp verwirft den Weg, bPathfind bleibt.
- N+1: KI -> PathFind, das Schild steht. Eine Anfrage vom eigenen Standort zum eigenen Standort ist offen ("Working"), fleeStop
  wartet.
- N+k: Die Anfrage gelingt, bPathfind=false, die Animation geht nach idle, clipWatch meldet "back" (Neustart 1). fleeStop sieht idle
  und vergisst `B.flee` (:979-981). Die KI bleibt PathFind.
- N+k+37: WalkingOnTheSpot (F1) schlaegt an: bMoving=true, shouldFollowWall=true, die Animation geht nach walk. fleeStop haelt
  (Stopp plus bPathfind=true), dann folgt walk -> idle (F2). Das ist Neustart 2.
- Folgen: Hieb (Treffer 0,60 s) und Biss (0,52 s) treffen knapp vor dem Bruch bei 0,63 s; der Rand ist 1 bis 2 Bilder. Der
  Doppelschlag (Treffer 1,30 s) trifft nach einem Laermschlag **nie mehr aus der Animation**: nach Neustart 3 endet er ueber
  `finishAct("noise")`, und clockHit setzt den Treffer. Der Bericht zeigt dafuer den Gegenbefund (Attrappe 41b "the hit came from
  the restarted clip").

**2.2 Fall walk (Linie frei).**
- N: Flucht geht los: KI Walk, Animation walk. fleeStop stoppt und setzt bPathfind (:1010-1015).
- N+1: KI PathFind, das Schild steht. Die Animation geht walk -> idle (F2). Das gilt als Neustart, und fleeStop setzt
  `B.flee = nil`.
- N+2: Ist die Anfrage noch offen, geht die Animation idle -> pathfind. fleeStop haelt das fuer einen NEUEN Fluchtbefehl
  (:984-999, Schritt 1). Der Stopp holt die KI diesmal aus PathFind, und `exit` setzt bPathfind=false.
- N+3: Das Schild ist aus, respondToSound bewertet neu. Lebt der Laerm noch (16 Bilder), kommt die naechste Flucht.
- Bilanz: alle 3 Bilder ein Fluchtbefehl, je Schlag rund 6, dazu Neustarts im Takt. Das Halten im walk-Fall wird also nie zu
  "Schritt 2 warten"; es haengt allein daran, ob die Wegsuche in hoechstens 1 Bild antwortet (ungeprueft).

**2.3 Mit klebendem shouldFollowWall (F3).**
- N+1: pathfind -> followwall. fleeStop stoppt sofort, KI aus PathFind, bPathfind=false.
- N+2: followwall -> idle (Neustart), das Schild ist aus, und es folgt die naechste Flucht.
- Bilanz: wieder alle 2 bis 3 Bilder ein Fluchtbefehl, solange der Laerm lebt.

**2.4 Ruhe.**
- Jeder walk-Ausflug durch WalkingOnTheSpot ist fuer `calmBack` eine Stoerung (:1388-1411).
- Nach 5 solchen Stoerungen in 30 s (CALM_NOISE_MAX 4, :182) endet die Ruhe mit "too much noise". Das sind bei einem einzigen
  Schlag rund 5 x 0,66 s = 3,3 s.

## 3. Gegenrechnung mit einem Pruefer-Modell (Scratchpad, nicht im Bau)

`C:\Users\Kevin\AppData\Local\Temp\claude\086a7114045651dc\cccbd9d6-dd89-4eba-8fad-b3beed093bcb\scratchpad\make_real.py` baut aus
`test_anim.lua` die Datei `exp_real.lua` (gleicher Ordner) mit einem Schalter `W.real`. Das Modell enthaelt:
- die Anfrage zum eigenen Standort nach `W.trivDelay` Bildern, danach "found";
- WalkingOnTheSpot (Tier 30) mit Failed: shouldFollowWall, Weg zur Kachelmitte, bMoving=true;
- die Ankunft, bei der die KI PathFind bleibt;
- die Uebergaenge je Zustand in der Reihenfolge von F2, dazu followwall.

Das Modell ist selbst nur aus dem Jar abgeleitet und **ungeprueft**. Werte nach 20 s, Schlag jede Sekunde 12 Kacheln entfernt,
Ziel 1,2 Kacheln vorn, wie Abschnitt 40 der Attrappe. "delay" ist die Antwortzeit der Wegsuche: 2 ist das fruehestmoegliche
(Anfrage in N+1, Antwort fruehestens in N+2), 3 oder mehr ist bei Last plausibel.

| Lauf | neu: Treffer / Flucht / Stress | alt: Treffer / Flucht / Stress |
|---|---|---|
| pathfind, delay 2..5 | 20 / 20 / 20 | 6 / 145 / 100, 60-s-Ruhe |
| walk, delay 2 | 20 / 20 / 20 | 1 / 36 / 36 |
| walk, delay 3..5 | **3-4 / 51-57 / 51-57, 60-s-Ruhe** | 1 / 36 / 36 |
| pathfind, shouldFollowWall klebt, Schlag 1 s, delay 2 / 3 | 20 / **58 / 58**; 20 / **134 / 100** | 6 / 16 / 16, 60-s-Ruhe |
| dto., Schlag alle 2 s, delay 2 / 3 | **14 / 34**; **10 / 67** | 9 / 11; 8 / 11 |
| EIN Schlag im Doppelschlag bei 0,1 s | Treffer **per Lua-Uhr** nach 2 walk-Ausfluegen (0,62 s) | -- |
| EIN Schlag im Hieb/Biss bei 0,1/0,4 s | Treffer aus der Animation, 0,02 s vor dem Bruch | -- |
| Sitzen 30 s, EIN Schlag, delay 1/2 | **Ruhe aus** ("too much noise", 5 Stoerungen, 14 x WalkingOnTheSpot) | sitzt weiter |
| Sitzen 30 s, EIN Schlag, delay 3/5 | sitzt weiter (3 Stoerungen) | sitzt weiter |
| Fressen 20 s, Schlag alle 5 s, delay 2/3 | **nach 12 s Ruhe aus** | frisst weiter |

Die Testliste des Bauers bleibt im Modell gruen (366/0), weil sie mit `W.real = false` laeuft.

## 4. Rueckschritte (Pruefliste des Auftrags)

- **Spielertreffer: ok.** In `updateBear` steht der Treffer-Zweig vor jedem fleeStop (:1496-1506). `endFight("hurt")` bzw.
  `calmEnd` geben die Sperre frei; in rest/return gibt es kein fleeStop, `fleeFromAttacker` laeuft. Unveraendert.
- **Ziel hinter dem Zaun: ok, kein Pendeln.** Neu sind bis 4 Neusetzungen je Anlauf (:1238-1260), "runs off" stellt die Stuck-Uhr
  neu. Danach greifen Stuck, Block und STUCK_MAX 3 wie bisher. Das Urteil kommt nur etwas spaeter.
- **Knockback: unveraendert.** Ausnahme Notloesung: Bei clockHit fliegt der Zombie, waehrend der Baer im Wartebild steht.
- **Sitzen/Aufstehen: Rueckschritt** (F1, Befund 3). Aufstehen gilt als fertig, wenn er wieder steht: das stimmt.
- **Rueckweg: unveraendert** (kein fleeStop in return).
- **Mehrere Baeren: ok.** Zustand je Baer; `F.ticks` und `F.noiseSayT` sind global, das ist gewollt. Deckel unveraendert.
- **Tempo 1x-4x: Wirkung haengt am Tempo.** fleeWait zaehlt Bilder, passend zum Laerm. WalkingOnTheSpot hat bei Tempo 4 die Grenze
  150 (3,1 s) statt 30 (0,63 s). Bei 4x sieht der Fix also besser aus als bei 1x. **Kevin sollte bei 1x testen.**
- **Laden: ok.** Neue Zaehler sind nil-fest (`count`, `or 0`). shouldFollowWall ist nach dem Laden wieder false (neues Objekt,
  removeFromWorld).

## 5. Ist die Notloesung ehrlich markiert?

**Ja.**
- Kopf der Datei (:35-36), Kommentar an `clockHit` (:1075-1078), Bericht 2 und 5.3, abschaltbar mit `NCBear_Tune("clockHit", 0)`.
- Je Uhr-Treffer kommt eine Zeile bei log 1 (:1085), dazu ein Zaehler in `NCBear_FightInfo`.

**Zwei Luecken:**
- Der Bericht stellt die Attrappen-Zahlen ohne ihre Modellgrenzen dar (F1-F3 fehlen).
- Der Doppelschlag laeuft unter Laerm praktisch immer ueber die Notloesung (2.1); das steht nirgends.

## 6. Befunde

1. **(major) Das "Schild" haelt nur rund 0,63 s.**
   - Fundstelle: `NCBearFight.lua:959-1022`, Bericht 5.1.
   - Beleg: F1. Bericht 5.1 sagt "bleibt die KI ... in AnimalPathFindState -> Schild bis zu unserem naechsten Stopp" und "Wer
     AnimalPathFindState sonst verlaesst, habe ich im Jar nicht gefunden". Laut PFB2.update Offset 461-478 und
     WalkingOnTheSpot.check (Tier 30) gibt die Wegsuche nach 0,63 s Stillstand Failed zurueck; execute Offset 13-71 setzt dann
     bMoving=true. Folgen: walk-Ausflug ohne neuen Laerm, Neustart, Doppelschlag nur per Uhr, Ruhe bricht ab.
   - Fix: WalkingOnTheSpot in die Attrappe aufnehmen (Vorlage `make_real.py`).
   - Fix: Nach einem Halt die KI wieder nach idle holen, sobald die Animation nach idle zurueck ist und der Laerm sicher vorbei
     ist. Das waere `stopAllMovementNow` ohne bPathfind, etwa 16 bis 18 Bilder nach dem Fluchtbefehl, statt die KI in PathFind
     altern zu lassen. Alternativ den walk-Ausflug ~0,63 s nach "back" als Engine-Eigenheit erkennen.
   - Hilfe: Den KI-Zustand direkt lesen ueber `a:getCurrentState()`, als Text wie in Vanilla
     `DebugUIs/DebugChunkState/DebugChunkState_ObjectProperties.lua:216-220` (OPH_IsoPlayer, `tostring` + `string.split`; IsoAnimal
     erbt von IsoPlayer). Die Fundstelle ist belegt, der Gegenpruefer soll die Kosten je Bild bewerten.

2. **(major) Der walk-Halt bricht an der Reihenfolge der Uebergaenge.**
   - Fundstelle: `NCBearFight.lua:979-981` (`B.flee = nil` bei jedem idle-Bild), `:984-999` (dann Schritt 1) und `:1010-1015`.
   - Beleg: F2, Ablauf 2.2. Nach dem Halt kommt walk -> idle (to_idle vor to_pathfind). Das eine idle-Bild loescht `B.flee`; das
     pathfind im Bild danach gilt als neuer Fluchtbefehl, und Schritt 1 holt die KI aus PathFind (exit: bPathfind=false). Das
     Schild ist aus, die naechste Flucht kommt.
   - Wirkung im Modell, Wegsuche ab 3 Bildern: 3-4 Treffer statt 20, 51-57 Fluchtbefehle und Stress, 60-s-Ruhe.
   - Fix: `B.flee` nach einem Halt bzw. nach Schritt 1 fuer die Wartezeit (fleeWait) halten, auch ueber idle-Bilder. pathfind,
     followwall und idle in diesem Fenster gelten als Fortsetzung (kein neuer Schritt 1). Gestoppt wird nur bei Rutschen
     (FLEE_MOVED) oder wenn das Fenster abgelaufen ist.

3. **(major) Ruhe: ein einzelner Schlag kann Sitzen/Fressen beenden.**
   - Fundstelle: `NCBearFight.lua:1388-1411` (calmBack zaehlt jedes "back") und `:182` (CALM_NOISE 4 in 30 s).
   - Beleg: F1 und 2.4. Im Modell endet die Ruhe nach EINEM Schlag (delay 1/2), beim Fressen nach Schlaegen alle 5 s. Der alte
     Stand sitzt bzw. frisst in beiden Faellen weiter.
   - Das widerspricht Bericht 6 ("bei einem Schlag steht er kurz, setzt sich wieder hin") und dem Attrappen-Test 44 (dort ohne
     WalkingOnTheSpot gruen).
   - Fix: wie 1; zusaetzlich engine-eigene walk-Ausfluege nicht als Laermstoerung zaehlen.

4. **(major) Klebendes shouldFollowWall hebelt Schritt 2 auch im Fall pathfind aus.**
   - Fundstelle: `NCBearFight.lua:991-994` (followwall: nur stoppen) und `:1016-1019`.
   - Beleg: F3 (geloescht nur in AnimalFollowWallState und removeFromWorld; der SP betritt diesen Zustand nie) und
     `actiongroups/buck/pathfind/to_followwall.xml` vor `to_idle.xml`. Gesetzt wird der Schalter durch jedes Failed: durch den
     Fix selbst (F1) oder durch eine unerreichbare Flucht im Zaungarten.
   - Wirkung im Modell: 58-134 Fluchtbefehle, Stress 58-100 in 20 s (statt 20/20), bei Schlaegen alle 2 s nur 10-14 Treffer.
   - Fix: followwall direkt nach Schritt 1 bzw. einem Halt nicht stoppen, solange er nicht rutscht (FLEE_MOVED). Er steht dann ohne
     Weg (bMoving false), followwall -> idle folgt von selbst.

5. **(major) Stress in lauten Basen.**
   - Fundstelle: Bericht 4/5.4.
   - Beleg: `respondToSound` Offset 341-351 gibt +Radius x 0,05 je Fluchtbefehl, also +1 (Thump 20) bzw. +2 (Maschendraht 40).
     `updateStress` Offset 212-228 baut nur getMultiplier/5500 je Update ab, rund 0,5 je Minute.
   - Rechnung: Auch im besten Fall (1 Fluchtbefehl je Schlag) ist Stress 70 bei 1 Schlag/s nach etwa 70 s erreicht, am
     Maschendraht nach etwa 35 s. Bei Befund 2 oder 4 geht es noch schneller. Ab 70 kann er vor dem gehenden Spieler fliehen
     (forschung_zustand.md 4, ungeprueft).
   - Der Auftrag sagt "In NPC-Crew-Basen wird es IMMER Laerm geben -> der Fix muss das aushalten"; das haelt er beim Stress nicht.
   - Fix (Kevins Wort): Stress ausgleichen mit `animal:changeStress(x)`, Vanilla-Fundstelle `ISMilkAnimal.lua:28` (vom Bauer schon
     genannt, nicht eingebaut). Oder den Stress per `getStress()` (ISMilkAnimal.lua:17) bei log 1 laut melden, ab 60.

6. **(minor) Die laute Zeile meldet auch erfolgreiche Angriffe als Stoerung.**
   - Fundstelle: `NCBearFight.lua:1116-1122` und `:1044-1052`.
   - `noiseActs` zaehlt jeden Angriff mit einem Ausflug, auch wenn er traf ("done"/"hit"). In einer lauten Basis kommt so alle
     120 s eine "***"-Zeile, obwohl alles klappt. Der Fehlerwaechter und Kevin lesen "***" als Fehler.
   - Fix: nur Angriffe ohne Treffer zaehlen, oder die Zeile ohne "***" bzw. hinter log 2.

7. **(minor) Die Zaehler in NCBear_FightInfo vermischen Laerm und Engine-Eigenheit.**
   - Fundstelle: `NCBearFight.lua:993` und `:999`.
   - Jeder walk-Ausflug durch WalkingOnTheSpot zaehlt als "noise interruption". Die Zahlen, mit denen der Bericht den Erfolg
     messen will (Abschnitt 6), sind dadurch zu hoch.
   - Fix: bei log 2 "held N frames" plus den Abstand zum letzten "back" ausgeben (Signatur siehe Abschnitt 7).

8. **(minor) Bericht 5.1: Failed fuehrt zur eigenen Kachel, nicht zum alten Fluchtziel** (F4). Nur Text.

9. **(minor) Die Attrappe kann F1 bis F3 nicht sehen.**
   - Fundstelle: `attrappe/anim/test_anim.lua`, kiStep und die Zustandsfunktion.
   - Die Variante "trivial" beantwortet die Anfrage im selben Bild und haelt PathFind fuer immer. Die Grundvariante beantwortet
     die Anfrage nie. Der Zustand wird ohne Uebergangsreihenfolge gerechnet.
   - Fix: das Modell aus `make_real.py` uebernehmen, Abschnitte 40, 41b, 44 und 46 mit delay 2/3 und shouldFollowWall
     wiederholen.

## 7. Was Kevin im Spiel pruefen kann (log 2), damit F1/F3 belegt oder widerlegt sind

- **Signatur F1:** "<act> back in idle after N frames, clip restarts (1/2)", dann ohne neuen Schlag etwa 0,6 s spaeter
  "<act> interrupted at X s: the bear left idle (walk)". Kommt das, ist WalkingOnTheSpot bestaetigt.
- **Signatur F3:** viele "stopped a move we did not order (followwall)" direkt nach "(pathfind)", und `flee stops` weit ueber der
  Zahl der Schlaege.
- Bei **Tempo 1** testen: bei Tempo 4 liegt die Grenze von WalkingOnTheSpot 5-mal hoeher (F1).
- Den Doppelschlag beobachten: Kommt sein Treffer unter Laerm je aus der Animation, oder immer "hit set by the Lua clock"?

## 8. Kevins Frage: Baerengroesse

Nachgezaehlt in der Test-Mod (nur gelesen):
- `NCBearTest/42/media/lua/shared/NCBearDefs.lua:73-74` setzt `minSize = 1.0`, `maxSize = 1.0`. **Gespawnt wird noch der kleine
  Baer (Groesse 1,0), nicht 1,35.**
- 1,35 steht erst als Plan in `baer/STAND.md:41` (B1: Jungtier 0,35 / Halbstark 0,75 / Erwachsen 1,35; der Bericht nennt :35).
- Vorlaeufig geht `NCBear_Size(1.35)` (`client/NCBearSize.lua:27`, setSizeForced, Fundstelle ButcheringUtil.lua:569). Das gilt
  nur bis der Baer einen Spieltag aelter wird (Kommentar :3-4).
