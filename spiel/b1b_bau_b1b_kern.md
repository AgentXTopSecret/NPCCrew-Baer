# Lauf baer-b1b: Bericht BAUER KERN (shared/ + server/)

Stand 11.11.2026 frueh. **Statisch geprueft, nicht gespielt.** Gebaut nach `PLAN_B1B.md` (Abschnitte 0, 1, 3.3, 4, 5.1-5.3, 9) im Staging
`_arbeit/baer_zaehmen/mod/42/media/lua/`. Abweichungen/Zusaetze stehen in `schnittstelle_aenderungen.md`, Abschnitt "B1b KERN" (10 Punkte,
alle rueckwaertsvertraeglich). Client-Dateien, Texte, Sandbox-Datei, Bench: nicht angefasst (OBERFLAECHE). Nichts in die Test-Mod, nach NPC
Crew, Vanilla oder Bandits geschrieben; kein git.

Fix 2 (`tHas` in `B.T`, `shared/BanditsNPCBear.lua:255-273`) und Fix 3 (Streichel-Ton, `Defs`/`PetAction`) sind unveraendert.

## 1. Dateien

| Datei (`S:` = Staging lua/) | Zustand | Zeilen |
|---|---|---|
| `S:shared/BanditsNPCBear.lua` | geaendert (B.CFG, B.OPTS) | 471 |
| `S:shared/BanditsNPCBearRules.lua` | geaendert (farFromHome, 3 neue Funktionen) | 421 |
| `S:server/BanditsNPCBearFollow.lua` | **neu** | 244 |
| `S:server/BanditsNPCBearRegistry.lua` | geaendert (InitRegistry, NewRec, viewEntry) | 471 |
| `S:server/BanditsNPCBearServer.lua` | geaendert (Handle, WHY_T, buildEnv, liveRec, countMisses, Hirn-Takt) | 927 |
| `S:server/BanditsNPCBearWorld.lua` | geaendert (Players, MoveTo, ScanAnimals + Waisen) | 539 |
| `attrappe/kern/attrappen.lua` | angepasst (Begruendung 6) | |
| `attrappe/b1b_kern/run.lua`, `ergebnis.txt` | **neu** (145 Faelle) | |

Unberuehrt: `shared/BanditsNPCBearDefs.lua`, `...Food.lua`, `...Crew.lua`, `shared/TimedActions/*`.

## 2. Aenderungen mit Datei:Zeile

**shared/BanditsNPCBear.lua**
- `:50-52` `barZ` raus, `tagZ = 0.18` rein (Plan 1.7/2.2). Die heutige Hud (`client/ISUI/BanditsNPCBearHud.lua:295`, B1a) liest
  `cfg.barZ or 0.55` -- laeuft also auch vor dem OBERFLAECHE-Umbau weiter.
- `:65-74` neue Stellwerte: `followNear/followStart/followGap` 3/4,5/2, `followMoveMs/followRepath/followRenewMs` 1200/2,5/4000,
  `followStuckMs/followStuckGain/followRetryMs` 15000/1,0/10000, `stayR` 8, `nameMax` 24, `askMs` 500, `orphanScanMs/orphanAgeMs/orphanMax`
  120000/30000/16. (Das alte Feld `orphanMs` ist ein unbenutzter B1a-Rest mit anderer Bedeutung; nicht angefasst.)
- `:97` `B.OPTS.BearFollowMaxDistance = { def = 40, min = 10, max = 60 }` (vor `BearLog`).

**shared/BanditsNPCBearRules.lua** (rein, keine Engine)
- `:265-271` `farFromHome` nimmt `c.homeR` (sonst `B.CFG.homeR`) -> `B.Decide` Regel 4/8 (Plan 5.3).
- `:330-333` `B.ModeOf(rec)`: "follow" nur bei `rec.mode == "follow"`, sonst "stay".
- `:341-357` `B.CleanName(text)`: Text-Typ; Leerzeichen (Byte 32) vorn/hinten weg (eigene Schleife); leer -> nil; > `nameMax` -> nil; je
  Zeichen `string.byte` < 32, 127, `<` (60), `>` (62), `%` (37) -> nil; > 127 erlaubt. Rueckgabe `clean` oder `nil, "UI_BN_Bear_Why_NameBad"`.
- `:359-421` `B.FollowDecide(c, o, f, ms)`: Regeln 10-16 genau nach Plan 1.2; Fortschritt vor Regel 15; schreibt nur
  `bestD/bestAt/stuck/retryAt`; Halten (13 UND 14) setzt die Messung zurueck (Abweichung 4); Ziel `followGap` vor dem Besitzer auf der Linie
  Besitzer -> Junges; neuer Befehl nur ab `followMoveMs` und bei (Wanderung >= 2,5 ODER Alter >= 4000 ODER gehalten ODER Wiederholung).

**server/BanditsNPCBearRegistry.lua**
- `:22-23` Kommentar Sitzung: `f` (Folgen), nie gespeichert.
- `:91-104` `InitRegistry`: `mode` nicht "follow"/"stay" -> nil; `name` kein Text oder `B.CleanName(name) ~= name` -> nil; je Fall eine `B.Err`-Zeile.
- `:184` `NewRec`: `mode = nil, name = nil`; `:193-198` Spiegel `{ id, st }` SOFORT ueber `animal:getModData()` (Plan 4.4), ohne die
  `isExistInTheWorld`-Frage (Lehre Fix 1). `B.Commit` unveraendert.
- `:429-436` `viewEntry`: `name = rec.name` (nil fehlt im Eintrag), `mode` nur bei `st == "tame"` (`B.ModeOf`).

**server/BanditsNPCBearFollow.lua (neu)** -- Kopf `if isClient() then return end` (`:1`), Modulkopf `:16-18`, nichts auf Dateiebene eingefangen.
- `:52-71` `B.AskOk(pkey, ms)`: je Schluessel eine angenommene Bitte je `askMs`; verworfene verschieben die Uhr nicht; > 64 Schluessel -> geleert.
- `:79-109` `B.SetMode(rec, mode, why, players)`: setzt `rec.mode`; bei "stay" Heimat = `rec.x/y/z`; leert `B._s[id].f` und `.chk`
  (Abweichung 2); `B.Commit`; Meldung an den naechsten anwesenden Besitzer: ask/follow `Note_Follow`, ask/stay `Note_Stay`, car `Note_StayCar`,
  far `Note_StayFar` (t "dir"), lost `Note_StayBehind` (t "dir"), offline/missing keine; Richtung `B.DirOf(rec.x - e.x, rec.y - e.y)`; `B.Log`.
- `:115-147` `B.FollowStep(rec, a, env, ms, players)`: `c = { x, y, z = rec.z }`, `B.FollowDecide(c, env.owner, f, ms)`; stay -> `B.SetMode`;
  hold -> `B.Hold(rec, a, true)`, `f.held = true`; run -> `B.MoveTo(..., { minMs = followMoveMs, watch = false })`, bei Erfolg
  `f.orderAt/tx/ty`, `f.held = nil`; keep -> nichts. Wechsel nach/aus "steckt fest" -> `B.Log`.
- `:154-159` `B.FollowLost(rec, players)`: zahm + follow + kein Objekt + Gegend NICHT geladen -> `B.SetMode(rec, "stay", "lost")`.
- `:165-182` `askRec`: Schreiber, Register, `args` Tabelle, Schluessel, Drossel, `args.id` Text (sonst still), Eintrag (sonst `Why_Gone`) (Abweichung 1).
- `:186-215` `B.HandleMode`: mode follow/stay (sonst still); missing -> `Why_Gone`; nicht tame / nicht Besitzer -> `Why_NotOwner`;
  `B.FindAnimal` nil -> `Why_Gone`; nur follow: `player:getVehicle()` -> `Why_InCar`, Abstand > `BearFollowMaxDistance` -> `Why_Far`;
  Erfolg `B.SetMode(rec, mode, "ask")` + `B.FlushViews()`.
- `:220-244` `B.HandleRename`: kein Text oder > 4 x `nameMax` -> `Why_NameBad` (t "num", v `nameMax`) OHNE Zeichenschleife; nicht Besitzer /
  st nicht tame/missing -> `Why_NotOwner`; `B.CleanName` nil -> `Why_NameBad`; Erfolg `rec.name`, `B.Commit`, `Note_Renamed` (t "name",
  v = Name), `B.FlushViews()`.

**server/BanditsNPCBearServer.lua**
- `:26` `B._orphAt`; `:40` `WHY_T.UI_BN_Bear_Why_NameBad = "num"`.
- `:388-395` `B.Handle`: "Mode" -> `B.HandleMode`, "Rename" -> `B.HandleRename` (je mit Existenz-Riegel, `return`).
- `:616-648` `buildEnv`: bei `st == "tame"` `env.owner = { key, x, y, z, dist, car }` = naechster anwesender Besitzer, ohne Abstandsgrenze.
- `:668-674` `markProbe` (Spiegel-Probe, Plan 4.4): `id` UND `st` vergleichen, sonst `B.Commit` (Abweichung 8); `:689` in `liveRec`.
- `:709-713` `liveRec`: tame + follow -> `B.FollowStep(...)` und `return` (kein `B.Decide`/`steer`/`B.MoveWatch`); `:721-722` sonst bei
  tame `c.homeR = B.CFG.stayR`.
- `:767-770` `countMisses`: tame -> missing und es folgte -> `B.SetMode(rec, "stay", "missing")` (Heimat = letzte Kachel, still; Abweichung 3).
- `:855-871` Hirn-Takt nach `resolve`: `B.FollowLost` fuer jeden Eintrag ohne Objekt; Merker `scanned`; der B1a-Suchlauf stellt auch `B._orphAt`.
- `:898-905` eigener Waisen-Suchlauf je `orphanScanMs` am ENDE des Takts, nur ohne Suchlauf in diesem Takt (Abweichung 5).

**server/BanditsNPCBearWorld.lua**
- `:20` `B._orph`. `:31-58` `B.Players()`: je Eintrag `car = (p:getVehicle() ~= nil)` (Server- und SP-Zweig).
- `:291-351` Waisen: Riegel-Beschreibung, `dropOrphan` (`:304`, nur `B.RemoveCub`, Abstand `vanishKeep`, `B.SeenInSP`), `sweepOrphans` (`:313`,
  Liste `B._orph` `{ o, at }`, bekannte zuerst, Deckel 16, Alter `orphanAgeMs`, `force` ueberspringt nur das Alter; Abweichung 7).
- `:353-463` `B.ScanAnimals(players, force)`: Riegel 1 Identitaet + Spiegel-Reparatur (`:371-385`); Spiegel-Weg wie B1a; Rueckfall ueber die
  AnimalID jetzt fuer jeden Eintrag OHNE LEBENDES Objekt (`:410-440`), Riegel 2 = gleiche AnimalID wie so ein Eintrag schuetzt (abstandsfrei),
  mehrere Kandidaten -> `B.Log`; `stale` wie B1a; Waisen = lose, ohne Spiegel, ungeschuetzt (`:454-461`). Rueckgabe `n, removed`.
- `:489-524` `B.MoveTo(rec, animal, x, y, z, opt)`: `opt.minMs` ersetzt `moveMs`; `opt.watch == false` -> `s.chk = nil`. Ohne `opt` wie B1a.

## 3. Engine-Aufrufe (neu oder an neuer Stelle) mit Fundstelle -- selbst nachgelesen (42.22.2-Dateien, 10./11.11.)

| Aufruf (Argumenttypen) | Wo im KERN | Fundstelle (gleiche Typen) | Seite |
|---|---|---|---|
| `player:getVehicle()` (IsoPlayer, keine Argumente) | `World.lua:44` (Server), `:55` (SP), `Follow.lua:205` | `V:server/Vehicles/VehicleCommands.lua:11` `local vehicle = player:getVehicle()` (Spieler eines Client-Befehls); `V:client/ISUI/Hutch/ISHutchMenu.lua:8` `playerObj:getVehicle()` mit `getSpecificPlayer(player)` [Nachbesserung B1b A4: `V:server/Seasons/season.lua:139` gestrichen -- steht in einem `--[[ ]]`-Block] | Schreiber (SP + Server) |
| `animal:getModData()` schreiben, sofort nach `addAnimal`/`addToWorld` | `Registry.lua:197-198` | Schreiben in Tier-ModData `V:client/ISUI/ISInventoryPaneContextMenu.lua:4127` `animal:getModData()["skeleton"] = "true"`; lesen `V:shared/Definitions/animal/ButcheringUtil.lua:596` | Schreiber |
| `animal:getModData()` (lesen, je Takt) | `Server.lua:671` (markProbe) | `V:shared/Definitions/animal/ButcheringUtil.lua:596` | Schreiber |
| `getTimestampMs()` | `Follow.lua:173`, `World.lua:461` | `V:server/Foraging/forageServer.lua:456` `local now = getTimestampMs();` | Schreiber |
| `player:getX()/getY()` (Server) | `Follow.lua:209` | `B:server/BanditServerSpawner.lua:179` `player:getX(), player:getY()` | Schreiber |
| `animal:getX()/getY()` | `Follow.lua:124`, `:209`, `World.lua:305-307` | `V:shared/Definitions/animal/ButcheringUtil.lua:575-576` | Schreiber |
| `animal:fleeTo(square)` | ueber `B.MoveTo` (unveraendert `World.lua:514`) | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38` `self.animal:fleeTo(sq);` | Schreiber |
| `animal:getBehavior():setBlockMovement(b)` | ueber `B.Hold` (unveraendert) | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:89` | Schreiber |
| `getObjectListForLua`, `:size/:get`, `instanceof`, `getAnimalType`, `getAnimalID`, `isDead`, `isExistInTheWorld`, `getSquare`, `isCanSee`, `remove`, `removeAnimal(getOnlineID())` | `B.ScanAnimals`/`B.RemoveCub` (wie B1a) | wie B1a `World.lua` (Kommentare dort; `getObjectListForLua`/`getAnimalID` am Server weiter UNBELEGT = A3) | Schreiber |
| `string.byte`, `string.sub`, `string.len` | `Rules.lua:341-357`, `Follow.lua:226` | Lua-Grundbibliothek, keine Engine-Methode | beide |

**Nicht benutzt** (Attrappe 10 greppt den Code-Teil): `pathToLocation`, `setVariable("animalRunning", ...)`, `setCustomName`/`getCustomName`,
`isAnimalMoving`, `pathToCharacter`, Vanillas Locken, `string.trim`. Kein Jar-only-Aufruf, kein neues `pcall`.
**[Nachbesserung B1b A1, 11.11.: falsch -- `string.byte` (in `B.CleanName`) hatte keinen Vanilla-/Bandits-Aufruf. Jetzt ohne
`string.byte` (nur `string.len`, `string.sub`, Textvergleiche), siehe `nachbesserung_b1b.md`.]**

## 4. SP- und MP-Zweig je Vorgang

| Vorgang | Einzelspieler (`not isServer() and not isClient()`) | Mehrspieler |
|---|---|---|
| "Follow me"/"Stay here" | `B.Ask` -> `B.Handle` direkt -> `B.HandleMode`; Meldung `B.Tell` -> `B.ShowNote`; Sicht direkt (`B.SendView` -> `B.ApplySync`) | Client `sendClientCommand("Mode")` -> Server `OnClientCommand` -> `B.HandleMode` prueft Besitz im Register; `Note` nur an den Besitzer, `Sync` an Besitzer + alle in 60 Kacheln |
| Folgen-Takt | das eine Programm rechnet (`B.FollowStep`), Besitzer `__sp` = naechster lokaler Spieler | nur der Server rechnet; Clients ziehen ueber das Tierpaket nach (FB1B 0.1) |
| Wechsel auf Bleiben (offline/Auto/zu weit/entladen/vermisst) | wie MP; "offline" nur bei totem/fehlendem Spieler | Besitzer getrennt -> Regel 10, ohne Meldung; Server-Neustart -> erster Takt ohne Besitzer -> Bleiben |
| Umbenennen | direkt, `B.HandleRename` | Server prueft Typ, Vorab-Deckel, Besitz, `B.CleanName`; verteilt ueber `Sync` |
| Waisen | `B.SeenInSP` schuetzt, was ein lokaler Spieler sieht; `animal:remove()` | Server: nur der Abstand schuetzt; `remove()` + `removeAnimal(OnlineID)`; `getObjectListForLua` am Server unbelegt (A3) -> Suchlauf am Takt-Ende |
| Speichern/Laden | `rec.mode`/`rec.name` in der globalen ModData; `B._s`, `B._orph`, Sperren nie gespeichert | gleich; `InitRegistry` prueft die Felder |

Kick-Gefahr: keine neue (nur `sendClientCommand` im eigenen Modul; der Server glaubt dem Client nur die Kennung, den Wunsch-Zustand und den Text).
Kein Gegenstand wird erzeugt oder vernichtet. Nichts haengt endlos (Folgen: Laufbefehl hoechstens je 1,2 s, festgesteckt je 10 s; Engine
selbst mit Zeitdeckel). NPC-Crew-Figuren werden nicht beruehrt (nur `ncbearcub`).

## 5. Pruefer-Ausgaben (6 KERN-Dateien)

- `luacheck.py`: `6 file(s) checked, 0 failed`
- `scopecheck.py`: `6 file(s), 0 violation(s)`
- `luacheck_pz.py`: `0 Treffer (W113)`; mit `--unused` die 2 alten B1a-Hinweise (`Rules.lua:41` Vorbelegung `base`, `Rules.lua:160` Parameter
  `slots` von `B.CheckPet`), nichts Neues.
- `localcount.py`: groesste Funktion `B.ScanAnimals` (`World.lua:353`) 54 insgesamt deklariert / 29 aktiv; Hirn-Takt-Koerper (`Server.lua:848`)
  39 / 32. Weit unter 180/200.
- Dateiform (`attrappe/kern/dateiform.py`): alle 6 Dateien LF, reines ASCII, kein BOM, Zeilenende am Schluss, keine verbotenen Woerter im Code.

## 6. Attrappen

- **`attrappe/kern/attrappen.lua` angepasst** (Begruendung: der Code ruft gewollt Neues): `server/BanditsNPCBearFollow.lua` in der Ladeliste
  (alphabetisch vor Registry, wie im Spiel); Spieler-Attrappe `getVehicle()` (neu in `B.Players`/`HandleMode`); dazu `getDescriptor():getForename()`
  fuer die OBERFLAECHE (`U.LocalName`, Beleg 10), weil die Gesamt-Attrappe diese Spieler-Attrappe mitlaedt.
- **`kern/run.lua`: 133 bestanden, 0 Fehler** (unveraendert; einzige `***`-Zeile die erwartete aus Fall 4).
- **`gesamt/run.lua`** (Datei des ZUSAMMENBAUS, nicht geaendert):
  - mit den B1a-Client-Dateien (Kopie im Scratch-Ordner, Client aus NCBearTest, MD5 = `staging_dateien.txt`) und dem neuen KERN: **261 / 0**;
    dieselbe Kopie mit `BanditsNPCBearFollow.lua` in der Ladeliste: **268 / 0**.
  - mit den Client-Dateien der OBERFLAECHE im jetzigen Stand: **260 / 1** -- `FEHLER: nach 5 s kein Balken mehr am zahmen Jungen (ist 4, soll 0)`.
    Das ist die gewollte B1b-Aenderung (ueber dem zahmen Jungen steht jetzt das Schild); der ZUSAMMENBAU muss diese B1a-Erwartung in `gesamt/run.lua`
    umstellen und `BanditsNPCBearFollow.lua` in dessen `FILES` aufnehmen (Plan 7).
- **NEU `attrappe/b1b_kern/run.lua`: 145 bestanden, 0 Fehler** (`b1b_kern/ergebnis.txt`). Abschnitte nach Plan 8.1:
  1 `B.FollowDecide` je Regel 10-16 treffend / knapp nicht (40,1/40,0; 2,9/3,1; gehalten 4,4/4,6; Ebene 1,5/0,7; Ziel genau 2 vor dem Besitzer;
  1100 -> keep, 1300 + 2,6 -> run; 2,4 + 3900 -> keep, 4100 -> run; stuck genau bei 15000, danach je ein run bei 25000 und 35000; Fortschritt und
  Regel 14 heben stuck auf; `f` nur feste Felder). 2 Bitte Mode (Besitzer, fed, missing, nicht geladen, Auto, 41 Kacheln, fly/Zahl/nil still, Drossel
  400/600 ms, Tabelle > 64, Fremder im MP). 3 Bleiben (Heimat = Kachel, stayR 8,1/7,9, fed homeR 10, im Takt). 4 Folgen im Takt (10 Kacheln -> fleeTo,
  nah -> Sperre, je Takt genau ein `getModData`, stiller Folgen-Befehl ist kein Fehler, offline/Auto/45 Kacheln mit Richtung W/entladen mit Richtung
  W/geladen -> missing + stay, andere Ebene, `B.MoveTo` opt). 5 Umbenennen (alle `B.CleanName`-Faelle, Server, 200 Zeichen mit 0 `string.byte`-Aufrufen,
  vermisst, fed, Fremder). 6 Speichern/Laden (mode/name bleiben, fly/99 Zeichen/Zahl -> nil mit `B.Err`, erster Takt haelt, folgt weiter). 7 Waisen
  a-m (a Alter 29 s/30 s, RemoveCub genau 1 x; b Spieler in 24; c gesehen; d frisch erzeugt mit `isExistInTheWorld` falsch: Spiegel trotzdem, nie
  Kandidat; e Spiegel-Reparatur; f zwei Kandidaten -> keiner, auch > 40 Kacheln; g force mit Riegel b/c; h 20 Waisen -> Liste 16, force alle 20;
  i Waisen-Takt ohne Eintraege genau je 120 s; j Erwachsener/Reh nie; k Kevins Fall N5; l Server `removeAnimal`; m Rueckfall bei altem Objekt).
  8 MP-Rundlauf (Client-Ask -> Draht -> Server; Sync an Besitzer UND Spieler B in 30 Kacheln mit mode/name; Note nur an den Besitzer; B-Rename
  abgelehnt; args nil still; Server rechnet Folgen; Besitzer offline -> stay; SP ohne Sende-Eintraege). 9 Nutzlast (rein, `name` nil fehlt,
  `mode` nur bei tame). 10 Dateien (KERN: kein `next(`, kein `%a`, im Code kein `pathToLocation`/`setCustomName`/`getCustomName`/
  `setVariable("animalRunning"`; Hinweis-Lauf ueber die OBERFLAECHE-Dateien: keine Treffer).
  Erwartete `***`-Zeilen: nur die drei aus 6b (`InitRegistry` meldet fly, 99 Zeichen, Name als Zahl).

Aufruf: `C:/Users/Kevin/Tools/lua51/lua5.1.exe C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/b1b_kern/run.lua`

## 7. Offen / ungeprueft

1. **Alles Laufzeit-Verhalten ist ungeprueft** (statisch geprueft, nicht gespielt): ob das Junge beim `fleeTo` hinter dem Besitzer wirklich
   2-4,5 Kacheln haelt, ob `setBlockMovement` je Takt das Wandern neben ihm verhindert, ob es vor einer Tuer ruhig wartet, ob es Treppen nimmt.
   Kevins Test: `PLAN_B1B.md` 8.4.
2. **MP A3 unveraendert offen:** `getObjectListForLua`/`getAnimalID` am Server ohne Server-Beleg. Neu: der Waisen-Suchlauf laeuft im MP alle
   120 s auch ohne Vermisste. Er steht am Ende des Hirn-Takts mit vorher gestellter Uhr -- wirft die Engine dort, kommt hoechstens alle 60 s eine
   gedrosselte `brain tick`-Fehlerzeile, das Folgen laeuft weiter. MP-Testpunkt (Plan 8.4 MP 7).
3. `string.byte` unter Kahlua fuer Zeichen > 255 (Umlaute, Kyrillisch, Koreanisch, Chinesisch): Zeichencode erwartet, **ungeprueft im Spiel**;
   ebenso, ob `string.len` dort Zeichen statt Bytes zaehlt (dann passt `nameMax` 24 genau; sonst waeren es weniger Zeichen fuer Nicht-ASCII-Namen).
4. `p:getVehicle()` am Server fuer FREMDE Spieler: belegt ist der Aufruf am Spieler eines Client-Befehls (`VehicleCommands.lua:11`), dass der
   Server den Sitz jedes Spielers kennt, ist Jar-Lesart -- ungeprueft im Spiel.
5. Wie schnell ein Server nach dem Einloggen des Besitzers wieder "following" zulaesst: sofort (Bitte), aber das Junge steht vorher auf "staying"
   (gewollt, Plan 1.5).
6. Fuer den ZUSAMMENBAU: `gesamt/run.lua` (FILES + B1a-Erwartung "kein Balken am zahmen Jungen"), `staging_dateien.txt` (neue Datei, MD5),
   Uebernahme-Trockenlauf/Probe (`B.OPTS.BearFollowMaxDistance` muss auch in `sandbox-options.txt` stehen -- Teil der OBERFLAECHE).

Statisch geprueft, nicht gespielt.
