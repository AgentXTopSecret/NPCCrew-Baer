# Pruefer Technik, Lauf baer-laerm (08.11.2026)

Statisch geprueft, nicht gespielt. Geprueft: `_arbeit/baer_laerm/mod/42/media/lua/shared/NCBearFight.lua` (einzige geaenderte
Datei; alle anderen 17 kopierten Dateien byte-gleich zu NCBearTest, per `cmp` nachgezaehlt) gegen den Stand der Test-Mod.
Nichts geaendert ausser diesem Bericht; eigene Versuche nur im Scratch (Pfade unten).

## Ergebnis

- Pruefer, Attrappen, Zeilenenden, SP-Riegel, Deckel und Kosten: in Ordnung, Zahlen des Bauers nachgerechnet und bestaetigt.
- Neue Engine-Aufrufe sind belegt (Tabelle 2), kein neues `pcall`.
- **1 echter Fehler (major): der walk-Fall in `fleeStop` haelt nicht.** Das Modell der Attrappe gibt `bPathfind` immer Vorrang. Die
  echte buck-ActionGroup geht aus `walk` zuerst nach `idle`. Mit der echten Reihenfolge faellt der walk-Fall auf 4 Treffer, 57
  Fluchtbefehle, Stress 57, 30 Clip-Neustarts und eine 60-s-Ruhe in 20 s. Der Bericht nennt 19 / 20 / 20 / 4 / keine.
  In Kevins Garten waren 7 von 21 "left idle"-Zeilen `(walk)` (console.txt). Ein kleiner Fix ist im Scratch gemessen (Befund 1).
- Dazu 4 kleine Befunde (Log-Zeile je Uhr-Treffer, Reload-nil-Fallen, Fundstellen-Kommentare, Zeilenangabe zur Groesse).

## 1. Befunde

### Befund 1 (major): walk-Halt -- walk -> idle -> pathfind, das pathfind gilt dann als NEUER Befehl, Schild aus

`NCBearFight.lua:991-1019` (walk: `stopAllMovementNow` + `setVariable("bPathfind", true)`, `hold`) und `:979-981`
(`if not FLEE_STATES[st] then B.flee = nil`). Kommentar `:970-972` sagt: "betritt die KI im naechsten Bild AnimalPathFindState
wie im Fall pathfind nach Schritt 1, und es wird ebenso gewartet". Fuer die KI stimmt das, fuer den Aktionszustand nicht.

Beleg Kette:
- `media/actiongroups/buck/walk/to_idle.xml`: `<isFalse>bMoving</isFalse>` (1 Bedingung). `walk/to_pathfind.xml`:
  `<isTrue>bPathfind</isTrue>` (1 Bedingung).
- Reihenfolge: `ActionState.load` sortiert die Dateien nach Namen (Collator ENGLISH, `B_ActionState.txt` load Offset 27-43). Danach
  sortiert `sortTransitions` stabil (ArrayList.sort): zuerst nach Prioritaet, dann nach Zahl der Bedingungen, absteigend
  (`lambda$static$0`, `B_ActionState.txt:612-634`). Kein buck-XML hat `conditionPriority`. Damit gilt in `walk`:
  `to_walk`(2) > ... > `to_idle` > `to_pathfind`.
- `ActionStateContainer.evaluateCurrentStateTransitions`: Der erste passende Uebergang gewinnt, je Bild nur ein Wechsel des
  Hauptzustands (`B_ActionStateContainer.txt`, Offset 152-160 setCurrentState, dann `goto 169`).
  `defaultTransitions.xml` liest das Spiel nicht: Keine Klasse im Jar enthaelt den Namen, und `ActionGroup.load` laedt nur
  Ordner als Zustaende (`B_ActionGroup.txt` Offset 105-133).
- Bild N+1 nach dem Halt: `IsoAnimal.update` Offset 29-61 schaltet in `AnimalPathFindState`. `enter` setzt `bPathfind=true` und
  `bMoving=false` (`B_AnimalPathFindState.txt` enter 0-15). `PathFindBehavior2.update` stellt beim ersten Aufruf nach `reset`
  (progress notrunning) die Anfrage nur asynchron und liefert `Working` (`B_PathFindBehavior2.txt` update Offset 0-176). Im
  postupdate steht der Aktionszustand noch auf `walk`, mit bMoving false: `to_idle` passt zuerst, also **walk -> idle**.
- OnTick N+1: `fleeStop` sieht `idle` und setzt `B.flee = nil`. `clipWatch` meldet "back" (Neustart 1).
- Bild N+2: bPathfind ist weiter true (Working), also **idle -> pathfind**. `fleeStop` haelt das fuer NEU (`E == nil`): Schritt 1
  stoppt. Jetzt steht die KI aber schon in AnimalPathFindState: `changeState(idle)` ruft `exit`, das setzt `bPathfind=false`
  (`B_AnimalPathFindState.txt` exit 0-15). Damit ist das Schild aus.
- Bild N+3: `respondToSound` bewertet neu, und solange der Laerm lebt (16 Bilder, `WorldSound.init` Offset 6), flieht er wieder.
  Das wiederholt sich etwa alle 3 Bilder, mit 2 Clip-Neustarts je Runde.
- Folge: `ACT_RESTARTS` (2) ist nach einer Runde verbraucht. Dann endet der Angriff mit "noise", meist vor dem Treffermoment,
  also ohne Uhr-Treffer. Nach 6 solchen Abbruechen kommt "attacks keep breaking off", der Baer ruht 60 s.
- Die Ruhe ist betroffen (gleicher fleeStop): `calmBack` zaehlt je walk-Runde doppelt, `CALM_NOISE_MAX` ist frueh erreicht.

Messung (Attrappe mit echter Reihenfolge der ActionGroup, sonst unveraendert; Abschnitt 40, Zaunschlag jede Sekunde, 20 s):

| Fall | Treffer | Fluchtbefehle | Stress | Clip-Neustarts | 60-s-Ruhe |
|---|---|---|---|---|---|
| Bau, Linie nicht frei (pathfind) | 20 | 20 | 20 | 1 | nein |
| **Bau, Linie frei (walk)** | **4** | **57** | **57** | **30** | **ja** |
| Bau ohne walk-Halt (`hold = false`) | 1 | 324 | 100 | 20 | nein (Drift 23,6 Kacheln) |
| Test-Mod-Stand, walk | 1 | 36 | 36 | 3 | nein |
| **Vorschlag unten, walk** | **19** | **20** | **20** | 6 | nein |

Der walk-Halt ist also besser als kein Halt, haelt aber nicht, was der Bericht verspricht. In der Original-Attrappe meldet die
Pruefung `test_anim.lua:2011` OK. Mit der echten Reihenfolge schlaegt genau sie fehl: "line clear (walk flights): attacks land,
held like pathfind (4 hits, drift 3.99, 57 flights)". Alle anderen 365 Pruefungen bleiben gruen.

**Vorschlag, im Scratch gemessen** (366/366 in BEIDEN Attrappen-Modellen): den einen idle-Zwischenschritt nach einem walk-Halt
als denselben Ausflug behandeln. In `fleeStop` vor `B.flee = nil`:

    local H = B.flee
    if H and H.hold and H.tick == F.ticks - 1 then H.tick, H.hold = F.ticks, nil; return st, false end

Und im hold-Zweig nach `E.cancel = false` die Zeile `E.hold = true` setzen. Dann landet das folgende pathfind in Schritt 2 (warten).

Zwei Punkte sollte der Bauer noch bewerten:
- Auch mit dem Vorschlag kostet jede walk-Flucht 2 Neustarts (walk->idle, idle->pathfind->idle) und braucht damit
  `ACT_RESTARTS` = 2 ganz auf. Moeglich: den 1-Bild-idle nicht als eigenen Neustart zaehlen.
- In der Pause sollte `decide` nicht auf diesen 1-Bild-idle hin starten, solange ein Halt laeuft. `beginAct` stoppt sonst
  mitten im Halt, und das Schild ist aus.

Ungeprueft im Spiel bleibt, ob die Anfrage zum eigenen Standort laenger als 1 Bild braucht. Laut Jar ist sie asynchron, die
Attrappe nimmt 3 Bilder an. Kommt sie im selben Bild zurueck, tritt der Fehler nicht auf.

### Befund 2 (major, Werkbank): Die Attrappe bildet die ActionGroup falsch ab

`attrappe/anim/test_anim.lua:326`: `local ns = a.bPathfind and "pathfind" or (a.moving and "walk" or "idle")`. Damit hat
bPathfind immer Vorrang, auch in `walk`. Echt ist es je Zustand anders (Befund 1):
- walk: `to_walk` > `to_idle` > `to_pathfind`
- idle: `to_walk` > `to_pathfind`
- pathfind: `to_walk` > `to_followwall` > `to_idle`
- je Bild ein Wechsel

Darum sind die Zeile "neu, Linie frei (walk) 19 / 20 / 20" in `bau_bericht.md` 4 und die Pruefung `test_anim.lua:2011` nicht
belastbar. Ersatz, im Scratch erprobt (`patch_ag.py`), eingesetzt vor `kiStep`, dann `local ns = agNext(a)`:

    function agNext(a)
        local s, m, p = a.state, a.moving, a.bPathfind
        if s == "walk" then
            if m and not p then return "walk" end
            if not m then return "idle" end
            if p then return "pathfind" end
            return s
        elseif s == "pathfind" then
            if m and not p then return "walk" end
            if not p then return "idle" end
            return s
        end
        if m and not p then return "walk" end
        if p then return "pathfind" end
        return s
    end

### Befund 3 (minor): Unter Laerm eine Log-Zeile je Uhr-Treffer schon bei log 1

`NCBearFight.lua:1085` `say(B.act .. ": clip broken by noise, hit set by the Lua clock (fallback)")` druckt bei der Vorgabe `log 1`.
Unter Dauerlaerm kommt sie bei jedem Angriff, zusaetzlich zur Trefferzeile aus `F.ApplyHit` (`:955`). In der Attrappe (41, 300 s)
sind das 137 Uhr-Treffer, also 137 Zeilen. Der Bericht verspricht: "Statt der Zeile je Angriff gibt es hoechstens alle 120 s EINE
laute Zeile". Vorschlag: `sayMore`. Der Zaehler `clockHits` steht schon in `NCBear_FightInfo`.

### Befund 4 (minor): nil-Fallen nach einem Lua-Reload mitten im Kampf

`F.bears` ueberlebt einen Reload (`:192` `F.bears = F.bears or {}`), und die Datei rechnet selbst mit alten Staenden (`count()`,
`:227-230`). Alte B-Tabellen haben die neuen Felder aber nicht:
- `:1162` `B.restarts = B.restarts + 1` (Phase act)
- `:1245/1248/1253` `B.minI`, `B.reroutes` (Phase approach). Die Wache `B.ix and` hilft nicht: Der alte Code setzte `B.ix` in
  `updateApproach`.

Folge: "attempt to compare/perform arithmetic on nil". Das `pcall` in `onTick` schaltet den Kampf dann laut ab. Das passiert nur
beim Debug-Reload, ein Spielstart ist nicht betroffen. Vorschlag: `(B.restarts or 0)`, `(B.reroutes or 0)`, und `B.minI` per
`B.minI or dI` vorbelegen.

### Befund 5 (minor): Fundstellen-Kommentare

- `:1211` `z:getSquare()` in `issueApproach` hat keinen Fundstellen-Kommentar (die Zeile ist verschoben, alt ohne Kommentar).
  Beleg: Bandits `BanditUpdate.lua:1852` (`zombie:getSquare()`).
- `:1011-1013` `setVariable("bPathfind", true)`: Beleg ist Bandits `ZAMove.lua:31` (an einem Zombie). Besser zusaetzlich Vanilla
  `shared/TimedActions/Animals/ISMilkAnimal.lua:139` (`self.character:setVariable("milkanimalout", false)`, gleiche Methode
  `IsoGameCharacter.setVariable(String, boolean)`, Vanilla, Wahrheitswert) nennen. Der Jar zeigt dazu, dass
  `AnimalPathFindState.enter` dieselbe Methode mit `bPathfind` am Tier ruft (`B_AnimalPathFindState.txt` enter Offset 0-4).

### Befund 6 (minor): Zeilenangabe zur Groesse

`bau_bericht.md` 8 nennt `baer/STAND.md:35`. Die Stufen 0,35 / 0,75 / 1,35 stehen heute in `STAND.md:41` (die Datei ist im
Arbeitsbaum geaendert), Kevins Entscheidung in `begleiter/ENTSCHEIDUNGEN.md:10`. Die Antwort selbst stimmt (siehe 7).

## 2. Engine-Aufrufe (neu oder verschoben)

| Aufruf (Zeile) | Fundstelle, selbst gelesen | Urteil |
|---|---|---|
| `a:getStress()` (:1030, nur log 2) | Vanilla `ISMilkAnimal.lua:17` `self.animal:getStress() > 40` | belegt, gleicher Typ (Tier, keine Argumente) |
| `a:setVariable("bPathfind", true)` (:1013) | Bandits `ZAMove.lua:31` (Zombie), Vanilla `ISMilkAnimal.lua:139` (Spieler, boolean) | belegt (Methode und Argumenttypen gleich, Empfaenger erbt von IsoGameCharacter). Die Wirkung ist nur im Jar abgeleitet, und der walk-Fall ist falsch (Befund 1). |
| `z:getActionStateName() == "thump"` (:1038) | Bandits `ZASmack.lua:486` `enemy:getActionStateName()`; Zustand `media/actiongroups/zombie/thump` vorhanden | belegt |
| `a:getActionStateName()` (:448, :978, :1234) | Bandits `ZASmack.lua:486`; liefert nie nil (`ActionContext.getCurrentStateName`: sonst Name des Startzustands) | belegt, nil-fest |
| `a:stopAllMovementNow()` (:1007) | Vanilla `ISAnimalContextMenu.lua:760` | belegt (unveraendert) |
| `a:fleeTo(sq)` (:1213) | Vanilla `ISMilkAnimal.lua:38` | belegt (unveraendert, verschoben) |
| `getCell():getZombieList()` (:1034) | Bandits `BanditZombie.lua:110` | belegt (wie bisher) |
| `z:getSquare()` (:1211) | Bandits `BanditUpdate.lua:1852` | belegt, Kommentar fehlt (Befund 5) |

- Kein neues `pcall`. Das einzige `pcall` bleibt das in `onTick` (`:1696`): Es meldet einmal laut und schaltet den Kampf ab. Das
  ist keine Tarnkappe.
- Nur im Jar belegt und richtig NICHT eingebaut: `OnWorldSound`, `OnAIStateChange`, `getLastSoundRespondedTo`, die Pfadziel-Getter.

## 3. Pruefer (selbst gelaufen)

| Pruefer | Ergebnis |
|---|---|
| `luacheck.py` | ok, 0 failed |
| `scopecheck.py` | 0 Verstoesse |
| `localcount.py` | 87 aktiv auf Dateiebene, 131 insgesamt (Grenze 200, Warnung ab 180). Groesste Funktion: updateBear 26. |
| `luacheck_pz.py` | 2x W113 `NCBearFight` (Zeile 38/39). Test-Mod-Stand: dieselben 2 (Zeile 28/29), gewollt. |

## 4. Attrappen (selbst gelaufen, Lua 5.1)

| Lauf | Ergebnis |
|---|---|
| `anim/test_anim.lua` gegen den Bau | 366 Pruefungen, 0 fehlgeschlagen (bestaetigt) |
| `anim/test_anim.lua` gegen den Test-Mod-Stand | 312 Pruefungen, 0 fehlgeschlagen (die Laerm-Pruefungen laufen dort nicht, `NEW=false`) |
| `kampf/test_fight.lua` gegen den Bau | 114 Pruefungen, 0 fehlgeschlagen, 4 SKIP |
| `kampf/test_fight.lua` gegen den Test-Mod-Stand | dieselben 4 SKIP. Die Aussage "scheitern auch am alten Stand" stimmt. |
| `mutate_laerm.py` | 17 von 18 bemerkt, nicht bemerkt nur "stuck clock not reset when it runs off" (bestaetigt) |
| `test_anim.lua` mit echter ActionGroup-Reihenfolge (Scratch) | 1 fehlgeschlagen: `:2011` walk (Befund 1/2) |
| dasselbe mit dem Vorschlag aus Befund 1 (Scratch) | 366/366. Auch die Original-Attrappe 366/366. |

## 5. Kosten, Deckel, nil, Zeilenenden, SP

- **Je Bild und Baer** (hoechstens 8 Baeren) laufen nur `fleeStop`, `clipWatch` und `updateAct` bzw. `updateApproach`, also
  ein `getActionStateName`, ein paar Vergleiche und ein `distTo`. Die Tabelle `B.flee` entsteht je Ausflug, nicht je Bild.
- Die Schleife ueber `getZombieList` in `noiseInfo` laeuft nur bei log 2 und nur je Ereignis (Ausflug, Neusetzung). Bei log 1
  kehrt `noiseInfo` sofort mit "" zurueck. Bei log 2 kaeme die Schleife im walk-Fall aus Befund 1 alle ~3 Bilder je Baer, das
  ist Diagnose und vertretbar.
- **Deckel:**
  - `ACT_RESTARTS` 2, `REROUTE_MAX` 4 je Anlauf
  - `NOISE_SAY_GAP` 120 s (fuer alle Baeren zusammen), `CALM_NOISE_MAX` 4 in 30 s, `NOISE_WAIT_MAX` 1 s
  - Klemmen im Tune: `fleeWait` 0..60, `clockHit` 0..1
  - Zaehler (`F.ticks`, `F.stats.*`) sind reine Zahlen. Nichts waechst als Tabelle.
- **nil:**
  - `getActionStateName` liefert nie nil (Tabelle 2).
  - Die `count()`-Zaehler sind nil-fest.
  - Offen sind nur die Reload-Fallen aus Befund 4.
- **Zeilenenden:** nur LF (1893 LF, 0 CR) wie in der Test-Mod (1543 LF, 0 CR), reines ASCII, Zeilenumbruch am Ende.
- **SP-Riegel** unveraendert: `onTick` prueft `isSP()` (`:1689`), `hook` nur im SP (`:1712`). Alle neuen Aufrufe stecken in
  `tickBody`. Im MP bleibt alles aus.

## 6. Hinweise ohne Befund (ungeprueft, fuer den Gegenpruefer)

- Variante "Anfrage zum eigenen Standort gelingt": Die KI bleibt in AnimalPathFindState (execute Offset 162-183 ohne
  `changeState`), waehrend unser Angriffsknoten im Aktionszustand idle laeuft. Ich habe nicht geprueft, was
  `PathFindBehavior2.update` in den Bildern danach mit einem leeren Weg tut. Moeglich waere ein Drehen per `faceLocation` oder der
  kleine Schub am Wegende (`moveToPoint`). Das ist ungeprueft; der erste Blick im Spiel waere: dreht er sich nach einem
  Zaunschlag mitten im Hieb weg?
- `clockHit` zaehlt auch Uhr-Treffer ohne Ziel im Kegel als "resolved by clock" (gezaehlt wird vor `F.ApplyHit`). Das ist nur
  eine Anzeige.

## 7. Kevins Frage: ist der Baer schon 1,35?

**Nein, gespawnt wird der Baer mit Groesse 1,0.**
- `NCBearDefs.lua:73-74` setzt `minSize = 1.0` und `maxSize = 1.0`, in der Test-Mod und in der Kopie byte-gleich.
- Weder `NCBearSpawn.lua` noch `NCBearBench.lua` noch `NCBearTest.lua` setzen beim Spawnen eine Groesse (grep "size": nur
  Listengroessen).
- 1,35 ist beschlossen (`begleiter/ENTSCHEIDUNGEN.md:10`) und fuer B1 geplant (`STAND.md:41`).
- Bis dahin geht es nur von Hand mit `NCBear_Size(1.35)` (`client/NCBearSize.lua`, `setSizeForced`, Vanilla
  `ButcheringUtil.lua:569`). Laut Kommentar dort haelt das, bis der Baer einen Spieltag aelter ist. Das habe ich nicht selbst
  nachgeprueft.

## 8. Scratch (nur Versuche, nicht zum Kopieren)

- `C:\Users\Kevin\AppData\Local\Temp\claude\086a7114045651dc\cccbd9d6-dd89-4eba-8fad-b3beed093bcb\scratchpad\patch_ag.py`
  (Attrappe mit echter ActionGroup-Reihenfolge, schreibt `...\scratchpad\test_anim_ag.lua`)
- `C:\Users\Kevin\AppData\Local\Temp\claude\086a7114045651dc\cccbd9d6-dd89-4eba-8fad-b3beed093bcb\scratchpad\patch_fix.py`
  (Vorschlag aus Befund 1 an einer Kopie, schreibt `...\scratchpad\fix.lua`)
- Aufruf: `METRICS=1 lua5.1.exe test_anim_ag.lua <NCBearFight.lua> <NCBearBench.lua>`
