# Forschung baer-schlaf: Wie schlafen die NPCs in NPC Crew -- und was gilt fuer den Baeren

Stand 09.11.2026. NPC Crew v3.14.63 (`shared/BanditsNPC.lua`:1347), Bandits 42.21, PZ 42.21. **Nur gelesen, nichts gebaut,
nichts heruntergeladen, nichts gespielt.** Zeilennummern wandern; es zaehlt der Funktionsname daneben.
Kevins Wunsch (woertlich in `baer/begleiter/ENTSCHEIDUNGEN.md`:113): "... als oder muss dann spaeter noch schlafen wie npc's es
schon tun". Seine festen Regeln: `ENTSCHEIDUNGEN.md`:63-66 (Befehle, Kampf hat Vorrang, Passiv, Jungtier kaempft nie) und :112-119.

---

## 0. Kurzfassung

* **NPC Crew:** Eine Figur schlaeft ueber die Beduerfnis-Routine (`NPCRoutine`, Beduerfnis `fatigue`). Ausloeser: (a) Nachtfenster
  22-7 Uhr UND Muedigkeit >= 30, aber nur wenn sie in der Basis "frei" ist (Programm Stay/Relax); (b) Zusammenbruch bei >= 90 zu
  jeder Zeit; (c) ein Schlafblock im Schichtplan. Folgen und Wache sind Pflicht: dort steigt die Muedigkeit gar nicht. Ort: freies
  Bett der Basis (gescannt oder von Hand zugewiesen), sonst Boden, wo sie steht. Aufwachen: Bedrohung binnen 7 Kacheln, Ende des
  Fensters bzw. des Blocks, ausgeschlafen (<= 5, nur ausserhalb einer Schicht), Befehl des Spielers, Bett weg. Im Mehrspieler
  entscheidet der **Rechner des Besitzers**, der dedizierte Server rechnet keine Beduerfnisse.
* **Bandits** hat nur zwei Mini-Schlaefer (Camper 0-7 Uhr, Verteidiger 0-7 und 13-14 Uhr), Aufwachen durch Sicht auf einen Spieler
  oder einen Treffer. Kein Bett, keine Muedigkeit.
* **Engine:** Tiere schlafen nicht (kein Schlafknoten in der Gruppe `buck`; `AnimalZoneState$StateSleep` ist nur eine Pause im
  Herdentrieb). Der Baer **blockiert den Spielerschlaf nicht** (Jar `IsoPlayer.updateLOS` zaehlt nur `IsoZombie`).
* **Fuer den Baeren (Vorschlag):** dieselben Regeln wie die Crew, aber als eigener Ruhe-Zustand neben Sitzen/Fressen
  (Hinlegen -> Schlafen -> Aufstehen) und **gerechnet auf dem Server** (SP: derselbe Code). Nachts in der Basis aufs eigene
  Baerenbett, sonst Boden; schlaeft der Besitzer, legt er sich daneben. Kampf weckt immer. Drei Abweichungen von der Crew mit Grund:
  Hunger/Durst wecken ihn (beim Baeren haben sie Folgen), er schlaeft im Fenster durch (die Crew steht ausgeschlafen um 2-3 Uhr
  auf), und das Jungtier macht Mittagsschlaf.
* **Naehte:** nur LESEN von NPC Crew, keine Zeile in NPC Crew. Wichtigste: Basisflaeche ueber `BeaconRegistry.Sites` +
  `SiteRules.BaseZone/ZoneContains` (shared, laeuft auf dem Server), Nachtfenster `Routine.InSleepWindow`, und das Baerenbett darf
  **kein** `bed`-Flag tragen (sonst schlafen NPCs und Spieler darin).

---

## 1. NPC Crew: wie die Crew schlaeft (Befund)

### 1.1 Wann

| Ausloeser | Regel | Fundstelle |
|---|---|---|
| Nachtfenster | `SleepStart = 22`, `SleepEnd = 7`, `InSleepWindow(hour)` = `hour >= 22 or hour < 7` | `shared/BanditsNPCRoutine.lua`:224-229 |
| "night" | im Fenster UND Muedigkeit >= 30 UND Programm `NPCStay` oder `NPCRelax` (in der Basis frei) | `Routine.SleepCheck`, :239-248 |
| "collapse" | Muedigkeit >= 90: jede Stunde, jeder Befehl | :241 |
| Pflicht | Folgen/Wache unterdruecken das Fenster ("A guard/follow order is DUTY") | :236-238; `MaybeStart` :689-722 laesst bei `NPCCompanion`/`NPCGuard`/`NPCCorpse`/`NPCLoot` nur Hunger und Durst durch |
| Muedigkeit steigt beim Folgen nicht | `following` -> nur Hunger/Durst steigen | `shared/BanditsNPCNeeds.lua`:470-487 |
| Arbeit zuerst | mitten im Auftrag startet kein Beduerfnis | `Routine.MidJob` :278ff., Aufruf :641 |
| Schichtplan | Block "sleep" (Nacht-Block heisst "Night (10pm-6am)") startet die Routine mit `mode = "shift"`, ohne Muedigkeitsschwelle | `shared/BanditsNPCSchedule.lua`:152, :1883-1990 |
| Bedrohung vor dem Start | keine Routine, wenn binnen 7 Kacheln eine Bedrohung steht; danach 10 s Sperre (`routineThreatMs`) | `Routine.lua`:743-759 |
| Wer fragt | `Routine.MaybeStart(bandit)` aus den Main-Stufen der Programme und Jobs | `shared/BanditsNPCPrograms.lua`:928, :1282, :2035, :2860, :2956 u. a. |

Zahlen: Muedigkeit steigt 1,6 je Spielstunde (x Sandbox `NeedsRateMult`, x Zuneigung), `Needs.lua`:34-35, :422-426. Schwelle
"kritisch" 70 (Sandbox `NeedsCritical`), :41-44; beim Relaxen proaktiv 40 (`Routine.lua`:674-676) -- gilt nicht fuer die Muedigkeit,
die hat `SleepCheck`.

### 1.2 Wo

* **Bett zuerst**, Reihenfolge der Wahl: von Hand zugewiesenes Bett (`brain.spots.bed`), sonst ein gescanntes Bett der Basisflaeche
  (`Base.Resolve`, Kommentar `Routine.lua`:761-766, :831-833). Beanspruchen exklusiv (`Base.Hold`), Belegung aus drei Quellen
  (Gehirn, Anspruch, Kachel) -- NPC-Crew-`CLAUDE.md`:3428-3437.
* **Was ein Bett ist:** Engine-Flag `IsoFlagType.bed` (`Base.P.sleepable`, `shared/BanditsNPCBase.lua`:201-204), dann Ausschluss
  von Stuehlen/Sofas ueber Sitz-Eigenschaft, `BedType`, `CustomName` und Bildnamen (`P.bed` :237-278; `Base.IsBed` :654-657).
* **Gesperrt:** schlafender Spieler neben dem Bett -> "full" (Boden); sitzender Spieler daneben -> "resting" (sie wartet, sagt es)
  (`restingCentres`/`restingPlayerNear` :1715-1782, `Routine.BedOrWait` :196-209, `SayBedWait` :149-155).
* **Boden:** "alle Betten belegt" oder nicht erreichbar -> sie schlaeft auf ihrer Kachel (`Routine.lua`:1044-1083,
  `Programs.lua`:5010-5049, Kevins Entscheidung v3.9.78). Erholung dort 70 % der Bettrate.
* Ein Spieler, der schlaeft, liegt NICHT auf dem Bett, sondern auf einer Nachbarkachel (`Base.lua`:1688-1696; Vanilla
  `setBed`/`setAsleep` ohne Positionswechsel, `ISWorldObjectContextMenu.lua`:1084-1088).

### 1.3 Animation

* Bett: eigene Aktion `BNSleep` mit Bump-Animation `BNSleepBed` (Gemeinschafts-Pose), die sie jedes Bild auf die Kachelmitte pinnt
  und zur Bettrichtung dreht (`shared/BanditsNPCActions.lua`:256-316; Aufruf `Programs.lua`:5102-5113).
* Boden: Bandits' eigene Aktion `Sleep` mit Anim `Sleep`, ohne Pin (`Programs.lua`:5048).
* Aufwachen: gesperrte Aufgabe `{action="Time", lock=true, anim="GetUp", time=150}` (`Programs.lua`:4235-4237).
* Statuswort im Fenster: `UI_BN_Rt_fatigue_at` = "Sleeping" (`Programs.lua`:4079). **Kein z Z z** ueber schlafenden NPCs
  (grep `zzz`/`"z z` in `42/media/lua`: kein Treffer ausser `DrainableComboItem.Use(ZZZ)` in Changelog-Zeilen).

### 1.4 Aufwachen

| Grund | Fundstelle |
|---|---|
| Bedrohung binnen 7 Kacheln (jeder Nicht-Bandit-Zombie oder feindlicher Bandit, gleiche Ebene) -> "!" und Ende | `threatNear` `Programs.lua`:4145-4165; Bett :5077-5084, Boden :5026-5033 |
| Nachtfenster vorbei (Modus "night") | :5085-5088, Boden :5034-5037 |
| Schichtblock gewechselt (Modus "shift") | :5089-5092 |
| ausgeschlafen (<= 5), **nicht** bei "shift" -- d. h. im Modus "night" steht sie ausgeschlafen auf, auch um 3 Uhr | :4310-4319 (Kommentar: "instead of getting up rested at 3am") |
| Bett verschwunden | :5055-5073 |
| Befehl des Spielers (Programm wechselt) -> Aufraeumen `RoutineInterrupted` | `Programs.lua`:4182-4193; `client/BanditsNPCInteract.lua`:5840-5847 (laut Kommentar rufen `SetOrder`/`OrderStay`/`OrderGuard` es nicht, der Guardian raeumt) |
| Waechter raeumt alte Schlafmarken | `client/BanditsNPCGuardian.lua`:4056-4080 ("STALE SLEEP FLAG") |
| Niederschlag / Aufhelfen | `client/BanditsNPCCombat.lua`:215 |
| Spieler kommt nah | **nein**, ungeprueft ob Ansprechen (V) weckt |

Nach dem Aufwachen geht sie zum vorherigen Befehl zurueck (`WayBack`/`prevProgram`, `Programs.lua`:4254-4255).

### 1.5 Muedigkeits-Uhr

* Im Schlaf steigt die Muedigkeit nicht; der Abzug laeuft ueber Weltstunden seit `rt.sleepHour`: Bett 15/h, Boden 10,5/h
  (`Programs.lua`:5044-5047, :5098-5101; `Needs.lua`:428-452). 70 -> 5 = 4,3 h im Bett, 6,2 h am Boden.
* Hunger, Durst, Langeweile, Hygiene steigen im Schlaf weiter (`Needs.lua`:441-442). Die Beduerfnisse der Crew haben **keine
  Folgen** ausser der Routine (`Routine.lua`:256-263).
* Ohne geladenen Koerper friert alles ein (v3.13.10, `shared/BanditsNPC.lua`:1500, Punkt 4 "SLEEP FREEZES TOO").

### 1.6 Mehrspieler: wer entscheidet

* Programme und Beduerfnisse laufen nur auf der Kopie, die zaehlt: Einzelspieler immer, im MP der Rechner des **Besitzers**
  (`BanditsNPC.OwnerRuns`, `shared/BanditsNPC.lua`:6483ff.). "Der dedizierte Server hat kein Gehirn" (`Needs.lua`:386-387).
* Ergebnis reist per `Bandit.ForceSyncPart` (Programm, `routineTask`) in den Cluster (`Routine.lua`:1212-1217).
* Fremde Clients spielen Posen nach (`shared/BanditsNPCPoseShow.lua`:51).

### 1.7 Spieler-Schlaf und Crew

* NPC Crew ersetzt Vanillas Schlaf-Tor, damit Crew den Spielerschlaf nicht blockiert (`client/BanditsNPCSleep.lua`:1-30,
  `friendlyBody` :59-74). Option "Sleep (the crew keeps watch)" nur mit Crew binnen 12 Kacheln (:528-547, Abstand :186).
* Einschlafen und `SleepingEvent`: die Engine weckt den Spieler, wenn `getNumVeryCloseZombies() > 0` (:310-322).
* `Events.OnSleepingTick` (Vanilla `ISSleepingUI.lua`:92) nutzt NPC Crew als Zeitstempel (`client/BanditsNPCPersistence.lua`:10412-10419).

---

## 2. Bandits

| Was | Fundstelle |
|---|---|
| `Bandit.SetSleeping(zombie, b)` / `Bandit.IsSleeping` setzen nur `brain.sleeping` (Bandits-Gehirn am IsoZombie) | `shared/Bandit.lua`:486-498 |
| Aktion `Sleep`: setzt nur die Bump-Animation, optional Pin mit `facing`/`eoffset` | `shared/ZombieActions/ZASleep.lua` (ganz) |
| Programm Camper: schlaeft 0-7 Uhr, sitzt 7-8, 12-13, 19-22; wacht auf, wenn er einen Spieler binnen 5 (Schlaf) bzw. 20/30 Kacheln sieht -> `SetSleeping(false)` + GetUp | `shared/ZombiePrograms/ZPCamper.lua`:17-90 |
| Programm Defend: schlaeft 0-7 und 13-14 Uhr auf einer Matratze | `shared/ZombiePrograms/ZPDefend.lua`:35-48 |
| Kampf aus, solange er schlaeft | `client/BanditUpdate.lua`:1004 |
| Treffer weckt: gesperrtes GetUp, `SetSleeping(false)` | `client/BanditUpdate.lua`:2348-2353 |

Bandits kennt keine Muedigkeit, kein Bett, keine Basis. Fuer den Baeren nur als Muster (Uhrzeit-Fenster, Mittagsschlaf, "Treffer
weckt", gesperrtes Aufstehen); die Aufrufe selbst gelten fuer `IsoZombie` mit Bandits-Gehirn, **nicht** fuer ein `IsoAnimal`.

---

## 3. Engine (Tiere)

* Die Gruppe `buck` hat keinen Schlafknoten: Ordner `alerted, deadbody, death, eating, falldown, followwall, hitreaction, idle
  (idle1-4, idleSit), onground, onhook, pathfind, trailer, walk`; "sleep" steht in allen AnimSets nur bei `player/onbed`
  (`media/AnimSets`, grep). Schlafen braucht also einen eigenen Knoten wie Sitzen (`NCBearTest/42/media/AnimSets/buck/idle/NCBear_Sit.xml`,
  Variable `NCBearAct`).
* `AnimalZoneState$StateSleep` (Jar, Dump `_arbeit/baer_laerm/dump/zombie.ai.states.animals.AnimalZoneState$StateSleep.txt`):
  setzt nur `wakeTime = WorldAgeHours + Rand/60` und wechselt danach auf "Follow" -- eine Pause im Herdentrieb einer Tierzone,
  keine Animation. Bringt nichts.
* **Der Baer blockiert den Spielerschlaf nicht:** `IsoPlayer.updateLOS` (Dump `_arbeit/baer_laerm/dump/zombie.characters.IsoPlayer.txt`
  ab Zeile 16953) castet jedes Objekt auf `IsoAnimal`/`IsoPlayer`/`IsoZombie` (Offset 279-337); die Zaehler `numVisibleZombies`
  und "very close" laufen nur im Zweig `zombie != null` (Offset 648-650 `aload 19; ifnull 886`). NPC Crews eigenes Tor scannt die
  Zombieliste (`Sleep.lua`:163-216), dort steht kein Tier. Also auch kein `SleepingEvent`-Wecken durch den Baeren.
* Engine-Bewegung waehrend er liegt: `setBlockMovement(true)` schuetzt NICHT vor `respondToSound` (Flucht vor Laerm),
  `laerm_forschung_laerm.md`:220; Wandern alle 600..3000 Ticks (`NCBearDefs.lua`:95). Dasselbe Problem wie beim Sitzen, dort schon
  geloest ueber `fleeStop` und `calmBack` (`laerm_bau_bericht.md`:40, :46).

---

## 4. Uebertrag auf den Baeren (Vorschlag)

### 4.1 Grundsatz

* **Ein neuer Ruhe-Zustand** neben Sitzen/Fressen, gleiche Form wie `F.Calm.Sit` (`NCBearFight.lua`:1925-1945) und `autoSit`
  (:1536-1546): `liedown` (Hinlegen, einmal) -> `sleep` (Schleife) -> `wakeup` (Aufstehen, einmal), ueber `NCBearAct` gesteuert.
  Hinlegen und Aufstehen laufen gesperrt zu Ende wie GetUp bei Crew und Bandits; Ausnahme Kampf (4.4).
* **Gerechnet dort, wo das Baeren-Gehirn laeuft:** `not isClient()` -- Einzelspieler und Server derselbe Code (`PLAN.md`:216-240).
  Das ist ein bewusster Unterschied zur Crew (die rechnet beim Besitzer-Client): Tiere rechnet der Server.
* **Nie eine gespeicherte Marke "schlaeft" allein:** der Zustand wird aus Uhrzeit, Muedigkeit und Befehl abgeleitet; eine Marke, die
  ihr Programm ueberlebt, hat bei der Crew Figuren eingefroren (`Guardian.lua`:4056-4062).

### 4.2 Wann

| Befehl / Lage | Schlaeft er? | Muster |
|---|---|---|
| Frei herumlaufen (Basis), Bleiben, Sitz | nachts: im Fenster 22-7 und Muedigkeit >= 30 | Crew Stay/Relax, `Routine.lua`:239-248 |
| Folgen, Komm her, (spaeter) Bewachen | nein -- Pflicht; Muedigkeit steigt dabei nicht | `Routine.lua`:236-238, `Needs.lua`:470-487 |
| **Besitzer schlaeft** (`isAsleep`) und Baer binnen Folge-Abstand | ja, egal welcher Befehl -- legt sich neben ihn | neu (Kevin: "beim Besitzer") |
| Muedigkeit >= 90 | ja, wo er steht (nur moeglich ausserhalb von Folgen, weil sie dort nicht steigt) | Crew "collapse" :241 |
| Jungtier, 13-15 Uhr, Muedigkeit >= 30 | Mittagsschlaf (Vorschlag) | Muster Bandits `ZPDefend.lua`:39 (13-14 Uhr) |
| Bedrohung in Suchweite | nie einschlafen; 10 s Sperre nach jedem Abbruch | `Routine.lua`:743-759 |
| hungrig/durstig >= kritisch und Futter im eigenen Inventar/Trog | erst fressen/trinken, dann schlafen | Abweichung, 4.5 |

**Durchschlafen:** im Fenster schlaeft er bis 7 Uhr, auch wenn die Muedigkeit vorher 0 erreicht (wie der Schichtschlaf der Crew,
`Programs.lua`:4310-4313). Die Crew im Modus "night" steht ausgeschlafen mitten in der Nacht auf -- fuer einen Baeren, den man
schlafen sehen will, waere das unschoen. Kevins Wort (Frage 1).

### 4.3 Wo (Reihenfolge)

1. **Beim Besitzer, wenn der schlaeft:** freie, stehbare Kachel 1-2 Kacheln neben ihm (`square:isFree(false)`, Vanilla
   `ISWorldObjectContextMenu.lua`:2199), nie seine Kachel, nie eine Kachel mit `IsoFlagType.bed` (Vanilla :2642) oder einer
   Bettgruppe. Wacht auf, wenn der Besitzer aufwacht (ausser es greift 4.2 Zeile 1).
2. **Eigenes Baerenbett in derselben Basisflaeche** (Frei herumlaufen; Bleiben/Sitz, wenn die Bleib-Stelle in der Basis liegt):
   hingehen, auf die Bettmitte setzen, zur Bettrichtung drehen; nach dem Aufwachen zurueck zum Befehl (bei Bleiben zur Bleib-Stelle;
   Crew: `WayBack`, `Programs.lua`:4254). Welches Bett: das dem Besitzer gehoert (Erbauer), sonst ein freies; exklusiv (ein Baer je Bett).
   Die Lage steht im Baeren-Register (Server), nicht in einem Kachel-Scan (der laeuft bei der Crew nur auf dem Client).
3. **Boden, wo er steht** -- kein Bett, Bett belegt, nicht geladen oder nicht erreichbar (Crew-Regel "Boden", `Routine.lua`:1044-1083),
   nie auf Bett-/Moebelkacheln. Erholung 70 %.
4. **Bleiben ausserhalb der Basis:** Boden an der Bleib-Stelle -- er laeuft nicht davon (Kevin: Bleiben heisst bleiben).

### 4.4 Aufwachen

| Grund | Was danach | Muster |
|---|---|---|
| **Bedrohung** -- dieselbe Zielsuche wie der Kampf (`pickTarget`, Radius 10 Zombies / 12 Banditen, `NCBearFight.lua`:86, :376), EINE Regel | Halbstark/Erwachsen: kaempft; **Passiv**: steht auf, bleibt beim Befehl bzw. zieht sich zum Besitzer zurueck; **Jungtier**: versteckt sich beim Besitzer. Danach 10 s ruhig -> wieder hinlegen, wenn noch faellig | Crew `threatNear` 7 Kacheln; Kevin `ENTSCHEIDUNGEN.md`:66, :118 |
| **Treffer/Schaden** (B5a) | sofort wach, wie Bedrohung | Bandits `BanditUpdate.lua`:2348-2353 |
| Morgen (Fensterende 7 Uhr) | Aufstehen, zurueck zum Befehl | `Programs.lua`:5086 |
| ausgeschlafen (<= 5) ausserhalb des Fensters | Aufstehen | `Programs.lua`:4313 |
| **jeder Befehl** des Besitzers (Folgen, Komm her, Bleiben, Sitz, Frei, Q-Ruf) | Aufstehen, Befehl | Crew: Befehl beendet die Routine; Q-Ruf zieht ihn ab Akzeptanz 40 ohnehin (`ENTSCHEIDUNGEN.md`:97) |
| Besitzer wacht auf (nur Ort 1) | Aufstehen, folgt wieder | neu |
| **Hunger oder Durst >= 90** | wach, frisst/trinkt aus Inventar/Trog, legt sich wieder hin | Abweichung, 4.5 |
| Laerm (Engine-Flucht `respondToSound`) | gilt als Stoerung wie im Sitzen: Kopf hoch/aufstehen, nach 30 s Ruhe wieder hinlegen; mehr als 4 Stoerungen in 30 s: wach bleiben | `CALM_NOISE`, `NCBearFight.lua`:197, `calmBack` |
| Niederschlag (Unsterblich), Tod, Unstuck-Knopf | Schlafzustand restlos weg, ohne Aufstehen-Clip | Crew `RoutineInterrupted` `Programs.lua`:4182-4193 |

**Kampf hat Vorrang auch vor dem Aufsteh-Clip:** ein gesperrtes Aufstehen von 2-4 s waere im Kampf zu lang. Vorschlag: bei Gefahr ein
kurzes "Aufschrecken" (hoechstens rund 1 s) statt des ruhigen Aufstehens -- Sache des Animations-Laufs.

### 4.5 Muedigkeit und Beduerfnisse

| | Jungtier | Halbstark | Erwachsen | Herkunft |
|---|---|---|---|---|
| Muedigkeit steigt je Spielstunde wach (nicht beim Folgen) | 2,6 | 2,0 | 1,6 | Crew 1,6 (`Needs.lua`:34); Junge schlafen mehr (allgemeines Wissen, ungeprueft) |
| Abzug im Schlaf je Spielstunde: Baerenbett / Boden | 15 / 10,5 | 15 / 10,5 | 15 / 10,5 | Crew `Programs.lua`:5101 / :5047 |
| Nacht-Schwelle / Zusammenbruch | 30 / 90 | 30 / 90 | 30 / 90 | Crew `Routine.lua`:241-245 |
| Mittagsschlaf 13-15 Uhr | ja | nein | nein | Vorschlag |

* **Uhr wie bei der Crew** (v3.13.12): im Schlaf steigt die Muedigkeit nicht, der Abzug kommt aus Weltstunden seit dem Einschlafen
  -- das haelt auch bei Zeitraffer und Spielerschlaf (grosses dt je Bild). Ohne geladenen Baeren zaehlt nichts (`PLAN.md`:148-149,
  Crew v3.13.10).
* **Hunger und Durst steigen im Schlaf weiter** (wie Crew, `Needs.lua`:441-442). **Abweichung mit Grund:** beim Baeren haben sie
  Folgen (ab 80 % verliert er Leben, `PLAN.md`:150-151), bei der Crew nicht (`Routine.lua`:256-263). Darum weckt Hunger/Durst >= 90
  ihn, und vor dem Hinlegen frisst/trinkt er, wenn er kritisch ist und etwas im eigenen Inventar bzw. am Trog liegt (Kevins
  "frisst aus dem eigenen Inventar", `ENTSCHEIDUNGEN.md`:65).
* **Laune / Vertrauen** (`ENTSCHEIDUNGEN.md`:107-110, merkt sich den Verlauf): Vorschlag -- eine durchgeschlafene Nacht im
  Baerenbett hebt sie, eine Nacht am Boden ist neutral, oft geweckt (mehr als 3 Mal in einer Nacht, ohne Kampf) senkt sie leicht;
  gezaehlt als "gute Naechte der letzten 3 Tage". Zahlen im Bau.
* **Ausdauer** (`PLAN.md`:120-123): Vorschlag -- ab Muedigkeit 70 erholt sie sich halb so schnell. Kein Zusammenbruch beim Folgen
  (dort steigt die Muedigkeit nicht).

### 4.6 Stufen

* **Jungtier:** schlaeft oefter (Rate, Mittagsschlaf), bevorzugt den Besitzer (liegt neben ihm, wenn der schlaeft), wacht bei Gefahr
  auf und versteckt sich -- kaempft nie. Liegt im grossen Baerenbett genauso (das Bett ist fuer 1,35 gebaut).
* **Halbstark/Erwachsen:** wie oben, wachen auf und kaempfen (ausser Passiv; im MP bis B9 kein Kampf, dann wie Passiv).

### 4.7 Laden, Speichern, Zeitraffer

* Nach dem Laden mitten in der Nacht: neu ableiten (4.2). Vorschlag: liegt er beim Laden in einem schlaffaelligen Zustand, startet er
  direkt in der Schlaf-Schleife statt mit dem Hinlege-Clip (sonst legt er sich nach jedem Laden sichtbar neu hin). Crew-Gegenstueck:
  `bedResumeDue` (`Schedule.lua`:1812-1845).
* Das Register liegt im globalen ModData. Lehre der Crew: das wird im SP nur bei Beenden, Schlafen und `saveGame()` geschrieben
  (NPC-Crew-`CLAUDE.md`:3352-3358) -- nach einem Absturz sind Weltzeit und Tier neuer als das Register. Deshalb nichts Schlaf-Spezifisches
  im Register ausser der Muedigkeit und der Bett-Lage.

### 4.8 Mehrspieler

* **Entscheidung beim Server** (Baeren-Gehirn), der Client zeigt. Server schickt den Ruhe-Zustand (`liedown`/`sleep`/`wakeup`) an
  die Clients; jeder Client setzt `NCBearAct` an SEINER Kopie (`PLAN.md`:224-225, Risiko 2) und zeichnet das z Z z aus demselben
  Zustand. Wer spaeter in Sichtweite kommt, braucht den Zustand noch einmal (Nachfrage oder Wiederholung alle paar Sekunden,
  solange er schlaeft) -- gehoert in B8.
* **Schlaeft der Besitzer?** Auf dem Client belegt (`playerObj:isAsleep()`, Vanilla `client/Context/ISMenuContextWorld.lua`:41).
  Ob der Server den Schlaf eines Spielers im Bett sieht: **ungeprueft** (Vanilla setzt `otherPlayer:setAsleep(args.isAsleep)` auf
  dem Server nur fuer den Fahrzeugschlaf, `server/ClientCommands.lua`:638; im MP schickt das Bett-Einschlafen sonst nichts aus Lua,
  `ISWorldObjectContextMenu.lua`:1093-1100). Rueckfall: der Besitzer-Client meldet "schlaeft/wach" per `sendClientCommand`
  (`OnSleepingTick` feuert nur auf dem Client); der Server prueft nur den Besitz -- eine falsche Meldung legt hoechstens den eigenen
  Baeren hin.
* Logout des Besitzers: Baer ruht (`PLAN.md`:229-230) -- Vorschlag: er legt sich dafuer an Ort und Stelle schlafen (sieht ruhig aus),
  wacht bei Gefahr trotzdem (sonst steht er im Kampf liegend).
* Kampf im MP erst ab B9 (`PLAN.md`:239-240): bis dahin weckt Gefahr ihn, er kaempft aber nicht (Rueckzug wie Passiv).

### 4.9 Was von der Crew NICHT uebernommen wird

| Crew-Teil | Warum nicht |
|---|---|
| `Bandit.SetSleeping`, `brain.sleeping`, Aktionen `Sleep`/`BNSleep`, GetUp-Task | gelten fuer IsoZombie mit Bandits-Gehirn und Bandits' Aufgabenliste; der Baer ist ein IsoAnimal mit eigenem OnTick (`NCBearFight.lua`:1888) |
| `Base.Resolve`/`Hold`/`Spots` fuer Menschenbetten | Baer benutzt keine Menschenbetten; der Scan braucht `getCell`-Kacheln und `BanditsNPC.Zones` (client/, auf dem dedizierten Server nil, `Base.lua`:724) |
| `Base.SiteNear` | fragt `siteUsable` mit `getSpecificPlayer(0)` (`Base.lua`:684-690) -- auf dem Server sinnlos |
| Schichtplan (`Schedule`) | kein Schichtplan fuer den Baeren (Vorschlag) |
| Sprueche (`Bark`) | Baer spricht nicht; statt "All beds are taken" hoechstens ein Brummen (optional) |

---

## 5. Naehte zu NPC Crew (Form wie `turret/NAEHTE.md`)

**Regel:** keine NPC-Crew-Datei wird geaendert. Jeder Zugriff liest zur LAUFZEIT ueber ein Feld und steht hinter einem Existenz-Riegel
(`local R = BanditsNPC and BanditsNPC.Routine; if R and R.InSleepWindow then ... else Vorgabe end`); jeder Aufsatz/Eintrag in
`Events.OnGameBoot`. Ohne NPC Crew gilt die rechte Spalte.

| # | Was der Baer braucht | Fundstelle NPC Crew | Von aussen? | Wie | Ohne NPC Crew |
|---|---|---|---|---|---|
| S1 | Nachtfenster | `shared/BanditsNPCRoutine.lua`:224-229 `Routine.SleepStart/SleepEnd/InSleepWindow` | Ja, Felder, shared (auch Server) | zur Laufzeit lesen; der Baer schlaeft dann genau, wenn die Crew schlaeft | eigene Vorgabe 22/7 in `BanditsNPCBearSleep*.lua` |
| S2 | Basisflaeche (Frei herumlaufen, Baerenbett in der Basis, Bleib-Stelle in der Basis?) | `shared/BanditsNPCBeaconRegistry.lua`:46 `R.Sites`; `shared/BanditsNPCSiteRules.lua`:110 `SR.BaseZone`, :549 `SR.ZoneContains` | Ja, shared, reine Tabellenrechnung, laeuft auf dem Server | **woertlich die Form von** `ownZoneAt` (`shared/BanditsNPCNav.lua`:255-277) bzw. `Lv.ForeignBaseAt` (`shared/BanditsNPCLivestock.lua`:4916-4950): Flaeche mit `site.owner == Besitzername` (MP) bzw. jede (SP, `not isClient() and not isServer()`), Ebene `bz.z` | eigener vom Spieler gesetzter Bereich (`ENTSCHEIDUNGEN.md`:65) |
| S3 | NICHT benutzen: `BanditsNPC.Zones.Contains` / `Base.SiteNear` / `Base.Zone` | `client/BanditsNPCZones.lua`:697, :801; `Base.lua`:664-713 | client/ bzw. Client-Sicht | keine Naht -- nur als Warnung fuer den Bau (auf dem dedizierten Server nil bzw. falsch) | - |
| S4 | Baerenbett darf kein NPC-/Spielerbett werden | `Base.P.sleepable` :201-204, `P.bed` :237-278 (Rescan); Vanilla-Schlafmenue `ISWorldObjectContextMenu.lua`:2642 | Nein (lokal) | **keine Zeile noetig, aber Pflicht am Objekt:** das Baerenbett traegt KEIN `IsoFlagType.bed` (sonst legen sich NPCs und Spieler hinein), ist kein Behaelter (`P.container` :328) und kein Stuhl. Pruefpunkt im Uebernahme-Skript (Kachel-/Objekt-Eigenschaften ohne `bed`) | gleich |
| S5 | Baer liegt nie in einem Menschenbett | `Base.lua`:1603-1619 `tileHasOther` **ignoriert IsoAnimal** | Nein | Baer-seitig: nie auf Kachel mit `bed`-Flag oder Bettgruppe -- sonst pinnt die Crew eine Figur in den Baeren | gleich (Vanilla-Betten) |
| S6 | Spielerschlaf | `client/BanditsNPCSleep.lua` (ganzes Tor), Jar `IsoPlayer.updateLOS` | - | nichts noetig: der Baer zaehlt weder bei Vanilla noch bei NPC Crew als Bedrohung (Abschnitt 3). Optional spaeter "Sleep (the bear keeps watch)" -- eigene Option, nur mit Kevins Wort | gleich |
| S7 | Tierpfleger der Crew | `shared/BanditsNPCLivestock*.lua` zaehlt `bear` als Vieh (`tier_spez.md` 5.4, `PLAN.md`:144-146) | - | schon bekannt: Ausnahme braucht eine NPC-Crew-Version und Kevins Wort; fuer den Schlaf wichtig, weil der Pfleger sonst den schlafenden Baeren streichelt/fuettert (stoert Zaehm-/Vertrauensbalken) | entfaellt |
| S8 | Angst vor Zombies | `shared/BanditsNPCAnimals.lua` `A.ApplyNoFear` (nicht-wilde Arten -> `fleeZombies = false`) | - | nichts: `NCBearDefs.lua`:86-88 hat `wild = false`, `fleeZombies = false` schon | gleich |
| S9 | `OnSleepingTick` | `client/BanditsNPCPersistence.lua`:10412-10419 | Event | eigener `Events.OnSleepingTick.Add` (additiv, Vanilla-Muster `ISSleepingUI.lua`:92); kein Konflikt | gleich |
| S10 | Bandits' Schlafmarke | Bandits `shared/Bandit.lua`:486-498 | - | nicht benutzen (Baer hat kein Bandits-Gehirn) | - |
| S11 | Texte | `Translate/*/UI.json` (Crew hat `UI_BN_Rt_fatigue_at` = "Sleeping") | Skript | eigene Schluessel `UI_BN_Bear_Sleep_*` (z. B. `UI_BN_Bear_Sleep_Status` "Sleeping", `..._Bed` "Bear bed"), sieben Sprachen, Kollisionsprobe gegen NPC Crew | gleich (Test-Mod-UI.json) |
| S12 | Sandbox | `42/media/sandbox-options.txt` | Skript | nur falls Kevin will: `BanditsNPC.BearSleepAtNight` (an/aus). Vorschlag: erst ohne Option | gleich |
| S13 | Lua-Dateien | - | - | `shared/BanditsNPCBearSleep.lua` (Zustand, Regeln, Server/SP), Zeichnen z Z z in `client/BanditsNPCBearSleepFx.lua`; Testhilfen (Sofort-Schlafen, Uhr vorstellen) NUR in `NCBearBench*.lua` | gleich |

Pruefung im Uebernahme-Skript (Vorschlag): grep, dass `R.Sites`, `SR.BaseZone`, `SR.ZoneContains`, `Routine.InSleepWindow` in NPC
Crew noch existieren und `BASE_KIND = "base"` (`SiteRules.lua`:100) gilt; sonst rote Meldung (Datenform-Naht S2).

---

## 6. Engine-Aufrufe fuer den Vorschlag (alle Lua-belegt, gleiche Argumenttypen)

| Aufruf | Beleg |
|---|---|
| `getGameTime():getHour()` (auch auf dem Server) | Vanilla `server/radio/ISWeatherChannel.lua`:89; Crew `Routine.lua`:244 |
| `getGameTime():getWorldAgeHours()` (Server) | Vanilla `server/Farming/SFarmingSystem.lua`:258 |
| `player:isAsleep()` | Vanilla `client/Context/ISMenuContextWorld.lua`:41 (Wert auf dem Server ungeprueft, 4.8) |
| `getOnlinePlayers()` (Server) | Vanilla `server/ClientCommands.lua`:658 |
| `getCell():getZombieList()` (Server) | Bandits `server/BanditServerZombie.lua`:15 |
| `animal:getBehavior():setBlockMovement(true)` | Vanilla `client/ISUI/Animal/ISAnimalContextMenu.lua`:89 |
| `animal:stopAllMovementNow()` | ebd. :760 |
| `animal:setVariable(String, String)` / `clearVariable(String)` | Vanilla `ISPetAnimal.lua`:43/:48 (schon in `NCBearFight.lua`:533, :1756) |
| `animal:setDir(IsoDirections.X)` (Bettrichtung) | Vanilla `ButcheringUtil.lua`:574 |
| `animal:setX(n)` / `setY(n)` (Bettmitte) | Vanilla `ButcheringUtil.lua`:575-576; Server `server/ClientCommands.lua`:845-846 |
| `obj:getProperties():has(IsoFlagType.bed)` | Vanilla `ISWorldObjectContextMenu.lua`:2642 |
| `square:isFree(false)` | Vanilla `ISWorldObjectContextMenu.lua`:2199 |
| `Events.OnSleepingTick.Add` | Vanilla `ISSleepingUI.lua`:92 |

**Nur Jar:** keiner noetig. (Gelesen, nicht vorgeschlagen: `AnimalZoneState$StateSleep`, `IsoPlayer.updateLOS`.)

---

## 7. Risiken

1. **Engine schiebt den liegenden Baeren** (Wandern, Flucht vor Laerm) -- gleiche Abwehr wie beim Sitzen noetig; ohne sie "laeuft er im
   Liegen" weg. Statisch nicht pruefbar, erster Testpunkt.
2. **MP:** Animations-Variable je Client und Nachzuegler (sieht einen stehenden Baeren); ob der Server den Bett-Schlaf des Besitzers
   sieht (ungeprueft, Rueckfall per Client-Meldung).
3. **Grosser Koerper auf einer Kachel:** erwachsen 2,65 m lang -- am Boden neben Waenden/Moebeln ragt er hinein. Bodenplatz mit freien
   Nachbarkacheln in Laengsrichtung waehlen; gehoert zum Bett-/Animations-Lauf.
4. **Datenform-Naht S2:** aendert NPC Crew das Format der Basisflaeche, irrt der Baer. Das Uebernahme-Skript muss es pruefen.
5. **Tierpfleger der Crew** fasst den schlafenden Baeren an (S7), solange die Ausnahme fehlt.
6. **Absturz-Schere** des globalen ModData (4.7): Muedigkeit kann nach einem Absturz alt sein -- harmlos.
7. **Hunger weckt** ist eine bewusste Abweichung von der Crew; zu oft geweckt sieht unruhig aus -> Schwelle 90 und vorher fressen.

---

## 8. Offene Fragen an Kevin

1. Schlaeft der Baer die ganze Nacht (22-7) durch -- oder wie die NPCs, die ausgeschlafen auch um 2-3 Uhr wieder aufstehen?
   (Vorschlag: durchschlafen.)
2. Wenn du schlaefst und er dir folgt: legt er sich neben dich (Vorschlag) oder haelt er wach Wache?
3. Passiv und Gefahr im Schlaf: aufstehen und zu dir kommen (Vorschlag) oder liegen bleiben?
4. Jungtier mit Mittagsschlaf (13-15 Uhr)? (Vorschlag: ja.)
5. Weckt Streicheln ihn? (Vorschlag: nein -- man kann ihn im Schlaf streicheln, er bleibt liegen, Vertrauen steigt etwas.)
6. Braucht es einen eigenen Befehl "Schlafen gehen" oder einen Weck-Knopf im Baeren-Fenster? (Vorschlag: nein, jeder Befehl weckt.)
7. Mehrspieler: darf jeder Baer jedes freie Baerenbett nehmen oder nur das seines Besitzers? (Vorschlag: eigenes zuerst, sonst freies.)
8. z Z z gibt es bei den NPCs bisher nicht -- spaeter auch fuer NPC Crew? (waere eine NPC-Crew-Version, nur mit deinem Wort.)

Statisch geprueft, nicht gespielt.
