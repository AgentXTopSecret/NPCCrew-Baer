# Lauf baer-b1c: Bau KERN (shared/ + server/)

Stand 11.11.2026 Nacht. **Statisch geprueft, nicht gespielt.** Gebaut nach `PLAN_B1C.md` (Abschnitte 0-3, 5.1, 5.2, 6.1-6.3, 6.5, 6.6,
7.1, 8), Abweichungen und Zusaetze stehen in `schnittstelle_aenderungen.md` Abschnitt **"B1c KERN"** (14 Punkte). Kurzformen wie im Plan:
`S:` = Staging `_arbeit/baer_zaehmen/mod/42/media/lua/`, `V:` = Vanilla-Lua 42.22.2, `B:` = Bandits `42.22/media/lua/`.
Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart. Client-Dateien nur gelesen.

## 1. Dateien

| Datei | Zeilen | Was |
|---|---|---|
| `S:shared/BanditsNPCBear.lua` | 502 | geaendert: `B.MARK_V = 2` (:30), `B.CFG` B1c (:81-97), `B.OPTS` BearRideDistance / BearCallCooldownMinutes (:122-124) |
| `S:shared/BanditsNPCBearRules.lua` | 628 | geaendert: N2 in `B.CleanName` (:361-371, :397-425), `B.FollowDecide` (:462-550); neu `B.HideSpot` (:557), `B.CalmSpot` (:566), `B.GuardDecide` (:584) |
| `S:server/BanditsNPCBearRegistry.lua` | 604 | geaendert: Register v2 + Migration (`InitRegistry` :98-182), `B.RecByU`/`NewU`/`NewId`/`BumpN`/`InsertRec` (:228-279), `NewRec` (:284), `RecOf` (:329), `Commit` (:404), `Close` (:455, CalmDrop), `viewEntry`/`BuildView` (:540-604) |
| `S:server/BanditsNPCBearServer.lua` | 1023 | geaendert: `WHY_T` CallWait (:42), `B.Handle` "Call" (:400), `forestRolls` Heil-Fenster (:523), `buildEnv` dt (:634), `markProbe` (:697), `pushMoved` neu (:710), `liveRec` (:739 Wache, :761 Zombie-Wache), `resolve` (:784), `countMisses` (:810), `brainTickBody` (:908-990), `B.BrainTick` (:1008) |
| `S:server/BanditsNPCBearWorld.lua` | 807 | geaendert: Kopf (:10-16), `B.SpotNear` (:225), `B.DeadAt` (:255), `B.ZedNear` (:327), `B.CubDefOk` (:399), `B.ScanAnimals` (:572, B1c-Reihenfolge), `B.Hold` (:707, Ruhefrist), `B.MoveTo` (:740, force/walk/ownUntil) |
| `S:server/BanditsNPCBearFollow.lua` | 278 | geaendert: `B.FollowStep` act "ride" und walk (:140-163), `B.FollowLost` ohne ride (:182), `B.HandleMode` Why_Riding |
| `S:server/BanditsNPCBearGuard.lua` | 306 | **neu**: Laerm-Wache (`B.CalmDrop` :43, `B.CalmWatch` :51, `B.CalmAnswer` :97, `calmTickBody` :159, `B.CalmTick` :203, OnTick :210), Zombie-Wache (`B.GuardScan` :219, `B.GuardStep` :255) |
| `S:server/BanditsNPCBearHeal.lua` | 311 | **neu**: `B.MarkOf` :50, `B.WriteMark` :65, `B.MarkFresh` :72, `bind` :79, `byAnimalId` :130, `B.Restore` :165, `B.HealFromMark` :252 |
| `S:server/BanditsNPCBearRide.lua` | 327 | **neu**: `B.PlaceCub` :66, `B.RideBoard` :97, `B.RideStep` :149, `B.CallLeft` :220, `B.HandleCall` :275 |
| `attrappe/b1c_kern/run.lua` + `ergebnis.txt` | neu | KERN-Attrappe B1c (154 Faelle) |
| `attrappe/kern/attrappen.lua` | geaendert | neue Dateien in `A.FILES`, Tier-Attrappe `getStress`/`getActionStateName`/`getVariableBoolean`/`pathToLocation`, `getZombieList`, `A.zombie`, `A.healWindow` |
| `attrappe/b1b_kern/run.lua`, `attrappe/gesamt/run.lua` | geaendert | gewollt geaenderte Erwartungen, je Kommentar "B1c" (Abschnitt 6) |
| `schnittstelle_aenderungen.md` | angehaengt | Abschnitt "B1c KERN" |

Alle Kern-Dateien: LF, reines ASCII, `if isClient() then return end` am Kopf jeder server/-Datei, kein `next(`, kein `%a`, keine Namen mit
spawn/debug/cheat im Code (Attrappe Fall 9). Ladefolge server: Follow < Guard < Heal < Registry < Ride < Server < World -- auf Dateiebene
wird nichts Fremdes eingefangen, alles zur Laufzeit ueber `B.X` (mit Existenz-Riegel, wo eine Datei fehlen koennte).

## 2. Was der Kern jetzt tut, je Auftragspunkt (SP- und MP-Zweig)

Schreiber = SP-Programm bzw. MP-Server; alles hier laeuft nur dort (`server/`). Im SP ruft `B.Ask` `B.Handle` direkt, `B.Tell`/`B.SendView`
rufen `B.ShowNote`/`B.ApplySync` direkt (sendServerCommand tut im SP nichts). Im MP: Bitte ueber `sendClientCommand` (nur LoginOnServer,
kein Kick), Antwort ueber `sendServerCommand`. Nichts kommt aus einem Client-Glauben: Besitz, Zustand, Abklingzeit, Lage stehen im Register.

**1 N9 Selbstheilung.** Jeder Eintrag hat Kennzeichen `u`, Koerper-Generation `gen`, Aenderungszaehler `r`; das Register eine Epoche `ep`.
Der Spiegel v2 am Tier (26 Felder, nur Zahl/Text) wird bei `NewRec`, `InsertRec`, `PlaceCub`, jedem `Commit` (Tier in der Welt) und von
`markProbe` (nur bei Abweichung von v/id/u/r) geschrieben. Fehlt ein Eintrag, stellt `B.HealFromMark` ihn aus dem Spiegel wieder her
(gleicher Zustand, Besitzer, bond, Balken, Zaehler, Zeiten, Heimat, Modus, Name; Kennung = alte, wenn frei; `reg.n` nachgezogen), eine
Fehlerzeile je Heilung, `Note_Back` an den anwesenden Besitzer. Veraltete Kopien (`gen` kleiner) und Doppel (gleiches `u`, anderes
lebendes Objekt) werden nie gebunden und unbeobachtet entfernt. Heil-Fenster 2 min nach dem Laden: Suchlauf je 15 s, kein Wald-Wurf.
SP: jeder Schluessel im Spiegel wird `__sp`; ein alter v1-Spiegel "tame" wird als tame (100) hergestellt. MP: nur Konten ungleich `__sp`;
Besitzer nil/`__sp` -> nicht als tame herstellbar; ein abwesendes Konto bekommt sein Junges (sieht es beim Einloggen); Deckel
`BearMaxPerPlayer` gilt (sonst nicht hergestellt, Tier bleibt). Faelschungs-Schutz siehe 5.

**2 Laerm.** Gezaehmte, geladene, nicht mitfahrende Junge stehen auf der Wache (`B._calm`, Deckel 8). Je Bild (`OnTick`) erkennt
`calmTickBody` einen Stress-Sprung >= 0,02 oder "bewegt + rennt ohne eigenen Befehl" und ersetzt die Engine-Flucht im selben Bild:
Zombie-Wache aktiv -> deren Ziel (rennen); folgt und Besitzer weiter als 4,5 -> Folgen-Ziel (rennen, ohne Drossel); sonst 1,5 Kacheln
GEHEND Richtung Besitzer/Heimat bzw. seitlich (nie die eigene Kachel). 2,5 s Ruhefrist: `B.Hold` erneuert die Sperre nicht (das Schild
bleibt). Deckel 4 Antworten je 2 s. Wild/scheu/angefuettert: nichts. SP und MP-Server gleich (Wache fragt nicht, wer laermt). Rueckfall bei
Stress am Deckel: `B.FollowDecide` schickt sofort neu, wenn der Abstand zum Besitzer je Takt um >= 2 wuchs.

**3 Zombies.** Je Hirn-Takt EINE Suche fuer alle geladenen Jungen (`B.GuardScan` -> `B.ZedNear`, Deckel 1500 Zombies, rollender Anfang).
SP mit Bandits: `BanditZombie.CacheLightZ` (Lua-Tabelle ohne Banditen), sonst `getCell():getZombieList()`; Banditen (auch NPC-Crew-Figuren)
zaehlen nie (SP `getVariableBoolean("Bandit")`, Server `GetBanditClusterData`). Gezaehmt + Besitzer da (gleiche Ebene, nicht im Auto,
<= 10): verstecken 1,5 Kacheln hinter dem Besitzer, dem Zombie abgewandt, dort halten; sonst und wild/scheu/angefuettert: 10 Kacheln weg
fliehen. Gefahr ab 6, Ende erst > 9 und 3 s lang (Hysterese). Mit Gefahr Hirn-Takt 750 ms statt 1500. Wache vor Folgen und `B.Decide` --
AUSNAHME: Besitzer im Auto in Einsteige-Weite -> erst einsteigen (schnittstelle "B1c KERN" 1). Zombies greifen nicht an (B5a).

**4 Mitfahren.** Besitzer im Fahrzeug (jede Groesse, `getVehicle`), Junges folgt und <= `BearRideDistance` (15): `B.RideBoard` --
Koerper weg (`B.RemoveCub`), `rec.ride`, `gen + 1`, `Note_RideOn`; weiter weg: Bleiben mit `Note_StayCar`. Waehrend der Fahrt wandert die
letzte bekannte Stelle mit dem Besitzer; `resolve`/`countMisses`/`B.FollowLost` ueberspringen `ride` (nie "missing"). Aussteigen
(`B.RideStep`): SP nach 1000 ms zu Fuss, MP nach 3000 ms zu Fuss UND <= 4 Kacheln/s (getVehicle-Aussetzer) -> freie Kachel 1..3 neben ihm,
nie unter einem Fahrzeug (`B.SpotNear`) -> `B.PlaceCub` (gleicher Eintrag, `gen + 1`, `mode = "follow"`, `Note_RideOff`). Kein Platz ->
bleibt, je Takt neu, ab 20 Versuchen eine Fehlerzeile je Minute. Speichern/Laden: `ride` steht im Register, nach dem Laden weiter bzw.
aussteigen. Absturz: alter Koerper (kleinere `gen`) wird "stale" entfernt -> genau ein Tier. Besitzer tot (`B.DeadAt`, 5 s, Gegend
geladen): steigt an der Leiche aus und bleibt ("stay"); entladen: bleibt `ride`, die neue Figur (gleicher Schluessel) bekommt es zu Fuss.
MP abgemeldet / Neustart: bleibt `ride`, nach dem Einloggen zu Fuss neben ihm. Fremder im selben Auto: nichts (nur `rec.owner` zaehlt).

**5 Call to me.** Bitte `Call { id }` -> `B.HandleCall`: Eintrag (Why_Gone), Besitzer + tame/missing (Why_NotOwner), nicht `ride`
(Why_Riding), Spieler nicht im Auto (Why_InCar), Abklingzeit (Why_CallWait, Minuten aufgerundet), freie Kachel 1..3 (Why_NoRoom). Erfolg:
ERST neuer Koerper neben dem Spieler (`B.PlaceCub`, `gen + 1`), DANN das alte Tier weg (falls geladen; ein nicht geladenes kommt spaeter als
"stale" und wird entfernt), `follow`, `Note_Called`, Abklingzeit startet (`B._callAt`, Echtzeit, Deckel 64, nie gespeichert). Drossel
`B.AskOk("Spieler|Call|ok/no")`. Sicht traegt fuer den Besitzer `callWait` (Sekunden). SP direkt, MP ueber die Bitte.

**6 Gehen.** `B.FollowDecide` Regel 16 traegt `walk`: Reststrecke <= `walkDist` 3 UND Besitzer-Tempo (Weg seit dem letzten Takt / echte
Zeit `B._ppAt`) <= `walkSpeed` 0,52 -> `B.MoveTo(..., { walk = true })` = `setVariable("animalRunning", false)` dann
`pathToLocation(x, y, z)`; sonst rennen wie B1b. Wechsel walk <-> run gibt sofort einen neuen Befehl. Mit dem neuen Modell nur `walkSpeed`
hochsetzen (`NCBear_CubSet`). Die B1b-Folgen-Simulation (b1b_kern 11a-e) laeuft mit gleichen Abstaenden (faellt nicht zurueck).

**7/8 Sicht fuer Markierung und Karte.** `viewEntry` traegt `x`, `y` (ganze Kacheln), `ride`, `callWait`; das wilde Junge des Finders steht
immer in seiner Sicht. Lage wird nachgeschickt, wenn sie sich um >= 3 Kacheln aenderte und hoechstens je 5 s, nur an finder/bond/owner
(`pushMoved`). Mitfahrend: nicht. N3: ein Konto ohne Schluessel bekommt nur Junge in `tellDist`.

**9 Anzeige-Optionen**: nichts im Kern (je Client, OBERFLAECHE).

**10 Kleinkram.** N2 in `B.CleanName`: Privatbereich U+E000-F8FF, U+FFFC/FFFD, Ersatzzeichen-Haelften U+D800-DFFF (echte Ungleichungen),
Name nur aus Kombinationszeichen U+0300-036F -> abgelehnt (Datei bleibt ASCII). N3 wie oben. N1 durch Gehen entschaerft. ES-Text: OBERFLAECHE.

## 3. Engine-Aufrufe, die B1c NEU benutzt (selbst nachgeprueft)

| Aufruf | Wo (S:) | Fundstelle (gleiche Argumenttypen) | Seite |
|---|---|---|---|
| `a:getStress()` | Guard.lua calmTickBody | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:17` (`self.animal:getStress()`) | Schreiber |
| `a:getActionStateName()` | Guard.lua calmTickBody | `B:shared/ZombieActions/ZASmack.lua:486` (Charakter-Methode); am Tier `T:shared/NCBearFight.lua:1099` | Schreiber |
| `a:getVariableBoolean("bPathfind")` | Guard.lua calmTickBody | `B:shared/ZombieActions/ZAMove.lua:61` | Schreiber |
| `a:getVariableBoolean("animalRunning")` | Guard.lua calmTickBody | Methode wie oben (Text-Argument); dass der Name den Engine-Merker trifft: nur Jar -> NUR Zusatzsignal neben dem Stress-Sprung | Schreiber |
| `a:setVariable("animalRunning", false)` | World.lua B.MoveTo :768 (einzige Stelle) | **Kevins Wort 11.11.2026** (ENTSCHEIDUNGEN.md); Methode `V:shared/TimedActions/Animals/ISMilkAnimal.lua:139`, `B:shared/ZombieActions/ZAMove.lua:32` | Schreiber |
| `a:pathToLocation(x, y, z)` (ganze Zahlen aus `sq:getX/Y/Z`) | World.lua B.MoveTo :769 (einzige Stelle) | **Kevins Wort 08.11.2026** (`forschung_engine.md:627`); gleiche Form am Zombie `V:client/DebugUIs/DebugContextMenu.lua:636` | Schreiber |
| `Events.OnTick.Add(f)` (Laerm-Wache) | Guard.lua :210 | `V:server/Foraging/forageServer.lua:502` | SP + Server |
| `getCell():getZombieList()`, `:size()`, `:get(i)` | World.lua B.ZedNear | `B:server/BanditSave.lua:15-18`, `:46-47` (SP + Server) | SP + Server |
| `z:getX()/getY()/getZ()` | World.lua B.ZedNear | `B:client/BanditZombie.lua:69-71` | SP + Server |
| `z:isAlive()` | World.lua B.ZedNear | `B:server/BanditSave.lua:52` | SP + Server |
| `z:getVariableBoolean("Bandit")` | World.lua isBanditZ (nur SP) | `B:client/BanditZombie.lua:74` | SP |
| `BanditUtils.GetZombieID(z)`, `GetBanditClusterData(id)[id]` (Bandits-Lua, Riegel) | World.lua isBanditZ (Server) | `B:server/BanditSave.lua:55-57` (Definitionen `B:shared/BanditUtils.lua:620`, `B:shared/BanditGMD.lua:81`) | Server |
| `BanditCompatibility.IsReanimatedForGrappleOnly(z)` (Bandits-Lua, Riegel) | World.lua B.ZedNear | `B:shared/BanditCompatibility.lua:187`, gerufen `B:client/BanditZombie.lua:118` | SP + Server |
| `BanditZombie.CacheLightZ` (Lua-Daten, kein Engine-Aufruf) | World.lua B.ZedNear (nur SP) | `B:client/BanditZombie.lua:12`, gefuellt `:60-87` | SP |
| `p:isDead()`, `getOnlinePlayers()`, `getNumActivePlayers()`, `getSpecificPlayer(i)`, `p:getX/Y/Z()` | World.lua B.DeadAt | wie `B.Players` (`V:server/XpSystem/XpUpdate.lua:298`, `V:server/Foraging/forageServer.lua:463-466`, `V:client/Fishing/FishingHandler.lua:6`, `V:server/BuildingObjects/ISBuildingObject.lua:183`, `B:server/BanditServerSpawner.lua:179`) | Schreiber |
| `sq:getX()/getY()/getZ()` | Ride.lua, World.lua MoveTo | `V:client/DebugUIs/DebugContextMenu.lua:636`; `V:shared/Traps/TrapSystem.lua:12` | Schreiber |
| `TreatAsSolidFloor`, Wasser, `HasTree`, `isFree(false)`, `isVehicleIntersecting`, `getGridSquare` | World.lua spotOk/B.SpotNear | wie `B.SquareFits` (Belege dort: `B:server/BuildingObjects/ZSGuardposts.lua:12`, `V:server/Foraging/forageServer.lua:276`, `B:server/BanditServerSpawner.lua:231`, `V:server/BuildingObjects/ISBuildUtil.lua:34`, `V:server/Animal/ISPickDungCursor.lua:104`) | Schreiber |
| `B.CreateCub` = `addAnimal` + `addToWorld` (unveraendert) | NEUER Aufrufer Ride.lua B.PlaceCub | `V:server/ClientCommands.lua:809-810`, `V:client/DebugUIs/DebugContextMenu.lua:1460-1467` | Schreiber |
| `B.RemoveCub` (unveraendert) | Ride.lua RideBoard/HandleCall, World.lua dropCopy | `V:shared/Definitions/animal/ButcheringUtil.lua:609-614` | Schreiber |
| `a:getModData()` (Spiegel v2) | Heal.lua, Registry.lua, World.lua | schreiben `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127`, lesen `V:shared/Definitions/animal/ButcheringUtil.lua:596` | Schreiber |
| `a:getAnimalID()` (Neu-Binden, Heilung) | Heal.lua, Ride.lua | `V:client/ISUI/Animal/ISAnimalUI.lua:53` -- am MP-Server nur Client-belegt (A3 aus B1a, offen) | Schreiber |
| `getTimestampMs()`, `ZombRand(n)` (u, ep, Uhren) | Registry.lua newUIn u. a. | `V:server/Foraging/forageServer.lua:456`; `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25` | Schreiber |

**Nicht benutzt** (auch nicht hinter pcall): `isAnimalMoving`, `getLastSoundRespondedTo`, `OnWorldSound`, `setShouldFollowWall`, `changeStress`,
`addAcceptance`, `setDebugStress`, Teleport (`setX/setY` am Tier), Vanillas Anhaenger-Aufrufe, `stopAllMovementNow` direkt. **Jar-only-Aufrufe:
keine** ausser den beiden mit Kevins Wort. pcall nur um EIGENEN Code (`B.CalmTick` wie `B.BrainTick`, laut ueber `B.ErrEvery`).

## 4. Pruefer-Ausgaben (alle neun Kern-Dateien)

```
luacheck.py      9 file(s) checked, 0 failed
scopecheck.py    9 file(s), 0 violation(s)
localcount.py    hoechstens 37 aktiv (World.lua B.ScanAnimals :572, Server.lua brainTickBody :908), 69 insgesamt (Grenze 200, ab 180 aufteilen)
luacheck_pz.py   0 Treffer (W113)
Zeilenenden      alle LF, reines ASCII (file: "ASCII text", kein CR)
```

## 5. Attrappen

| Lauf | Ergebnis |
|---|---|
| `attrappe/kern/run.lua` (B1a) | 136 bestanden, 0 Fehler (unveraendert) |
| `attrappe/b1b_kern/run.lua` | 204 bestanden, 0 Fehler (vorher 203; ein Fall 1.11 mehr) |
| `attrappe/gesamt/run.lua` | 519 bestanden, 0 Fehler (laedt die drei neuen Kern-Dateien und die heutigen OBERFLAECHE-Dateien des Stagings) |
| `attrappe/b1c_kern/run.lua` (**neu**) | **154 bestanden, 0 Fehler** (`b1c_kern/ergebnis.txt`) |

b1c_kern deckt PLAN_B1C.md 7.1 Gruppe 1 (a-p + k2 Faelschung), 2 (a-i), 3 (a-j), 4 (a-i + Einsteigen bei Zombie, Mode waehrend der Fahrt,
kaputter ride-Zustand), 5 (a-e), 6, 7 (+ N3), 8 (N2 mit Kahlua-Zeichen), 9 (Dateiregeln: `B.CreateCub(` nur in `B.AppearFor` und
`B.PlaceCub`; `setVariable("animalRunning"` und `pathToLocation(` nur in `B.MoveTo`). Erwartete Fehlerzeilen im Lauf: die Heilungen
(`heal: entry ... restored`), die Deckel-/Schluessel-Ablehnungen, "more than 8 tamed cubs", "definition not loaded", "could not get out
(20 tries)", "unusable ride state".

## 6. Gewollt geaenderte Erwartungen in bestehenden Attrappen (je Stelle Kommentar "B1c")

- `kern/attrappen.lua`: die drei neuen Dateien in `A.FILES`; neue Tier-/Zellen-Attrappen (nur Zusatz). `A.load` schliesst das Heil-Fenster
  (`_healUntil = 0`), weil die B1a/B1b-Faelle ein Spiel lange nach dem Laden abbilden -- ohne das blockierte das Fenster (2 min nach
  `InitRegistry` kein Wald-Wurf, gewollt) Fall 3a "Wald-Wurf". `A.healWindow = true` laesst es offen (b1c_kern 1o).
- `b1b_kern/run.lua` 1.11: Auto in 5 Kacheln ist jetzt "ride" (Kevin: mitfahren bis 15), "stay car" erst bei 15,1 (neuer Fall).
  1 (Feldliste von `f`): zwei feste Felder mehr (`lastD`, `walk`), Deckel 12 statt 10. 4f: Besitzer steigt 16 Kacheln weg ins Auto (sonst
  stiege das Junge ein). 10 (Dateiregeln): `pathToLocation` und `setVariable("animalRunning"` sind in World.lua (B.MoveTo) erlaubt.
- `gesamt/run.lua`: FILES um die drei Kern-Dateien (alphabetisch), Heil-Fenster zu in `loadAll`, 17c Auto erst ab 16 Kacheln "Bleiben",
  Text-Erwartung `Note_StayCar` auf den neuen Text (Plan 6.7, OBERFLAECHE hat ihn gesetzt). **Fuer den ZUSAMMENBAU:** Options/Marker/Map
  fehlen dort weiter in FILES (OBERFLAECHE-Hinweis 13); Abschnitt "18 B1c" kann `A.healWindow = true` vor `loadAll` setzen.

## 7. Offen / ungeprueft (Testpunkte, nichts davon gespielt)

- Ob die Ersatz-Antwort die Engine-Flucht ersetzt, bevor ein Schritt zu sehen ist (OnTick nach dem Tier-Update; am Server ungeprueft); wie
  lange ein Laerm am Server lebt; ob `getStress` den Sprung im selben Bild zeigt. Diagnose: `NCBear_CubLog(true)` -> "calm: b1 noise
  answered (jump|run, walk|follow|guard)".
- Fehlalarm "rennt ohne eigenen Befehl": laeuft ein eigener langer Lauf laenger als Wegzeit + 1,5 s (Hindernisse), haelt die Wache ihn fuer
  fremd und ersetzt ihn durch einen kurzen Schritt (gedeckelt 4 je 2 s). Moegliches Ruckeln beim Heimweg im Bleiben -- Stellwerte
  `ownSlackMs` / `ownMaxMs`.
- `getZombieList` / `getVariableBoolean("Bandit")` / `GetBanditClusterData` am dedizierten Server; ob `CacheLightZ` im SP immer gefuellt ist.
- `getVehicle()` fremder Spieler am Server; Einloggen im Auto; Neu-Erzeugen direkt neben einem gebremsten Fahrzeug; ob die tote Figur im SP
  noch in `getSpecificPlayer` steht (`B.DeadAt`) -- steht sie nicht, kommt das Junge zur neuen Figur (F3).
- A3 (B1a): `getObjectListForLua` und `getAnimalID` am MP-Server -- Heilung, Aussteigen und Call to me haengen am Server daran.
- Ob Doubles (`u` ~ 1,7e15, `ep`) die ModData exakt ueberstehen (Vergleich `mark.ep == reg.ep` mit `==`); weicht `ep` ab, gilt der Spiegel als
  "fremde Epoche" (ein wildes Junges kaeme dann als scheues zurueck statt zu verschwinden -- kein Verlust).
- Engine-Werte gehen beim Neu-Erzeugen (Aussteigen, Call to me) verloren: Akzeptanz (Q-Ruf holt es danach nicht mehr heran -- die Laerm-Wache
  faengt die Flucht ab), Stress, Hunger/Durst/Gesundheit der Engine (B1c benutzt keinen davon).
- MP-Faelschung (F1): ein veraenderter Client kann einen gueltigen Spiegel eines anderen Jungen auf ein Junges OHNE Eintrag schreiben ->
  wird fuer das Konto im Spiegel hergestellt (Deckel je Spieler, Fehlerzeile). Auf ein Junges MIT Eintrag: das Register gewinnt (b1c 1k, 1k2).

## 8. Fragen fuer Kevin (Kern; die Planer-Fragen F1-F16 in PLAN_B1C.md 11 gelten weiter)

1. **Zombie am Auto:** steigt der Besitzer ein, waehrend ein Zombie nah am Jungen ist, steigt es trotzdem ein (das Auto ist das beste
   Versteck), statt erst wegzurennen. Ok? Empfehlung: ja.
2. **Kleiner Schritt statt Flucht:** beim Laerm macht das zahme Junge 1,5 Kacheln GEHEND (seitlich, wenn es schon bei dir ist) -- reicht dir
   das, oder soll es ganz stehen bleiben? Stehen ginge nur wie beim grossen Baeren (Halt-Verfahren, mehr Code). Empfehlung: erst ansehen.
3. **Dein laufender Spielstand:** die Heilung wirkt ab jetzt; die alte Zaehmung von "b1" steht nur im `_crash`-Ordner (Plan F16).

Statisch geprueft, nicht gespielt. Spiel muss nach dem Einbau neu gestartet werden (Lua laedt nur beim Start).
