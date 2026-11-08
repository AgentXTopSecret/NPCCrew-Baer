# Baer kaempft gegen Zombies und feindliche Banditen (NCBearTest) - Lesebericht

Stand 08.11.2026, PZ 42.21 (`projectzomboid.jar` vom 28.09.2026), Bandits 42.21. Nur gelesen (Vanilla-Lua, Bandits-Lua,
NPC-Crew-Lua nur lesend, Jar mit `javap -c -p`, Lesehilfe Vineflower aus `_arbeit/baer_spiel/dec`). Jar-Auszug fuer
diesen Lauf: `_arbeit/baer_kampf/jar/` (alle `zombie/*`-Klassen), javap-Texte daneben (`ia.txt` IsoAnimal, `iz.txt`
IsoZombie, `igc.txt` IsoGameCharacter, `bab.txt` BaseAnimalBehavior, `cm.txt` CombatManager, `wsm.txt` WorldSoundManager).
**Statisch geprueft, nicht gespielt.** Nichts gebaut, keine Datei der Mod angefasst.

Schreibweise: `Klasse.methode Offset` = Jar; `Datei.lua:Zeile` = Vanilla unter `media/lua`, sonst mit Mod genannt.

---

## 0. Ergebnis in zwoelf Saetzen

1. **Eigene Angriffs-Clips gehen ohne fremde Datei:** neue Knoten-XML unter `42/media/AnimSets/buck/idle/`, Bedingung auf
   eine eigene Text-Variable `NCBearAct`, die Lua am Tier setzt. Vanillas Muster ist das Streicheln:
   `ISPetAnimal.lua:43` setzt `idleAction = "petting"` am Tier, `AnimSets/cow/idle/idlePetting.xml` spielt dann.
2. **Echte Rehe merken nichts:** die Variable setzt nur unser Code; eine fehlende Text-Variable gilt als leerer Text, ohne
   Warnung (`AnimCondition.check` Offset 23-93), und die Clips stehen nur im Baerennetz.
3. **Den Treffermoment liefert die Animation selbst:** Ereignis `SetVariable NCBearHit=true` bei `m_TimePc`, Lua liest es je
   Bild ab. Das Ende ebenso (`NCBearDone=true` bei `End`). Vanilla-Muster: `player/bumped/bumpFall.xml`, Bandits `zsloot.xml`.
4. **Toene ohne Lua:** Ereignis `PlaySound` im Knoten spielt ueber den Emitter des Tiers (`IsoGameCharacter.OnAnimEvent_PlaySound`),
   Vanilla `cockerel/attack/attackDefault.xml`. Eigene `.wav` per Sound-Skript `file = media/sound/...` (Vanilla
   `sounds_zombie_voice_tutorial.txt`, Bandits `zs_sounds.txt`).
5. **Bewegung belegt:** Anrennen mit `animal:fleeTo(square)` (`ISMilkAnimal.lua:38`; setzt `animalRunning` und sucht den Weg),
   Anhalten `animal:stopAllMovementNow()` (`ISAnimalContextMenu.lua:760`), Herumlaufen sperren
   `animal:getBehavior():setBlockMovement(true)` (`ISPetAnimal.lua:36`), Drehen `animal:faceThisObject(obj)` (`ISPetAnimal.lua:17`).
6. **Schaden und Umwerfen belegt:** `zombie:setHealth(h)` (Bandits `BanditClientCommands.lua:36`), `zombie:knockDown(behind)`
   (`DebugContextMenu.lua:668`), toedlich `zombie:Kill(nil)` (Bandits `BanditUpdate.lua:2386`), Blut wie Bandits
   (`BanditCompatibility.lua:130-133`).
7. **Nicht `zombie:Hit(...)` fuer den Schaden:** die Engine rechnet den Wert durch vier Faktoren (0,3 x 1,5 x 0,15, dazu 0,5 bei
   Zweihaendern und ab dem vierten Treffer x (n-2) x 1,5), "fett" waere so nicht planbar (3.3).
8. **Ziel nur IsoZombie aus `getCell():getZombieList()`**: Spieler, Tiere, Fahrzeuge und Kisten stehen gar nicht in der Liste.
   Banditen ueber Bandits' Gehirn: Ziel nur bei `hostile` oder `hostileP`, nie bei `loyal`, nie bei NPC-Crew-Marken
   (`recruited`, `npcNeutral`, Programm `NPC*`). Gehirn fehlt trotz Bandit-Marke: kein Ziel.
9. **Zombies greifen den Baeren nicht an:** `AttackState.triggerPlayerReaction` Offset 20-33 loescht ein Tier als Ziel. Er nimmt
   also heute keinen Schaden ausser von Spielern.
10. **Einzelspieler: alles in einem Prozess, baubar.** Mehrspieler: Baer-KI nur auf dem Server
    (`IsoAnimal.updateInternal` Offset 23-85), Zombie-KI nur beim Client mit Hoheit, der Server rechnet keinen Zombie (CLAUDE.md
    Abschnitt 5). **Schaden im MP ist offen; Vorschlag: im MP kein Kampf in Stufe 1.**
11. **Flucht vor Schuessen** (`IsoAnimal.respondToSound`) hat keinen Lua-Schalter; im Kampf jede fremde Bewegung mit
    `stopAllMovementNow` beenden. **Kein `addSound` vom Baeren:** Tiere hoeren jeden Laerm ohne Quellen-Ausnahme, er floehe vor
    dem eigenen Bruellen (4.4).
12. **Noetig sind fuenf neue Clips im `NCBear.glb`** (Aufrichten+Bruellen, Prankenhieb links/rechts, Doppelschlag aus dem Stand,
    Biss am Boden), fuer das offene Maul ein neuer Knochen `Bip01_Jaw` (Netz pruefen, 5.6).

---

## 1. Eigene Animationen

### 1.1 Laden: Mod-Dateien kommen in den Zustand dazu

- `AnimationSet.Load` (Lesehilfe `AnimationSet.java`): `resolveAllDirectories("media/AnimSets/" + name)`, je Ordner ein Zustand,
  dann `AnimState.Parse(stateName, stateDir)`.
- `AnimState.Parse`: `ZomboidFileSystem.resolveAllFiles(statePath, *.xml, true)`. Die Suche
  (`ZomboidFileSystem.walkGameAndModFiles`) geht erst durch den Spielordner, dann je aktive Mod durch `common` und den
  Versionsordner. **Doppelte werden am relativen Pfad erkannt** (`if (!result.contains(relPath3))`): eine Mod-Datei mit
  neuem Namen wird ein weiterer Knoten, eine mit dem Namen einer Vanilla-Datei (`idle1.xml`) wuerde verworfen. Also:
  Dateinamen mit Praefix `NCBear_`.
- Der Knotenname kommt aus `<m_Name>`, nicht aus dem Dateinamen (`AnimState.Parse` nimmt `asset.animNode`).
- **Mod nur im Spielstand (Kevins Ablauf):** `Core.ResetLua` Offset 48 `AnimationSet.Reset`, also wird `buck` nach dem
  Mod-Wechsel beim ersten `IsoAnimal.init` neu gelesen (`AnimationSet.GetAnimationSet` ist faul). Derselbe Weg traegt heute
  Bandits' und NPC Crews Zombie-Knoten.
- Muster: Bandits `common/media/AnimSets/zombie/bumped/` (200 Dateien), NPC Crew `common/media/AnimSets/zombie/bumped/BN*.xml`.
  Fuer den Baeren `42/media/AnimSets/buck/idle/` (Versionsordner wie der Rest von NCBearTest; beide Ordner werden gelesen).

### 1.2 Auswahl im Zustand: so gewinnt unser Knoten und nur er

- `AnimState.addNode`: Knoten absteigend nach `conditionPriority`, dann nach Zahl der Bedingungen sortiert
  (`AnimNode.compareSelectionConditions`).
- `AnimState.getAnimNodes`: der erste Knoten, dessen Bedingungen gelten, wird `bestNode`; jeder spaetere mit niedrigerem Rang
  bricht die Schleife ab. Gleichrangige werden zusammen gespielt.
- **Darum `<m_ConditionPriority>10</m_ConditionPriority>`** (Vanilla nutzt 10 in 14 Dateien, z. B.
  `player/deadbody/deadbody_killedbyfall.xml`). Damit verdraengt unser Knoten `idle1` (keine Bedingung) und `idle2/3/Idle4`
  (eine Bedingung, Rang 0). Es gilt immer nur einer von unseren, weil `NCBearAct` genau einen Wert hat.
- Fuer Rehe: unser Knoten besteht die Bedingung nie, `bestNode` bleibt leer, die Schleife laeuft unveraendert weiter. **Rehe
  unberuehrt** (dazu: fehlende STRING-Variable = leerer Text, `AnimCondition.check` Offset 23-93; Warnung `warnOnce` nur bei
  den Zahlen-Typen EQU..ABSGTR, Offset 127-147; Typ-Reihenfolge aus `AnimCondition$Type`).
- Die Rueckfall-Art `bearstag` hat die neuen Clips nicht: **nie fuer `bearstag` setzen** (sonst friert er in der letzten Pose,
  `AnimationPlayer.play` warnt nur).

### 1.3 Geeignete Zustaende

| Zustand | geeignet | Grund |
|---|---|---|
| **idle** | **ja** | `AnimalIdleState.execute`: nur `wanderIdle` (bei `setBlockMovement(true)` sofort `return`, `BaseAnimalBehavior.wanderIdle` Offset 42-56), Trog-Blick, Wechsel nach `walk` bei `bMoving`. Kein Ausgang haengt am Animationsende (`actiongroups/buck/idle/to_*.xml`). |
| walk, pathfind | nein | Clip-Weg treibt die Bewegung (`PathFindBehavior2.update`), Knoten nur ueber `bMoving`/`animalRunning`. Ein Hieb im Lauf waere ein eigenes Projekt. |
| hitreaction | nein | Ausgang `ActiveAnimFinishing` (`actiongroups/buck/hitreaction/to_idle.xml`): ein eigener Knoten dort beendet den Zustand. |
| alerted, eating, trailer | nein | beim Baeren nicht erreichbar (tier_spez.md 3.3). |

### 1.4 Variable setzen und loeschen (Lua)

- Setzen: `animal:setVariable("NCBearAct", "swipeL")` - `ISPetAnimal.lua:43`, gleiche Typen (String, String), gleiche Klasse.
- Loeschen: `animal:clearVariable("NCBearAct")` - `ISPetAnimal.lua:48`.
- Lesen: `animal:getVariableString("NCBearHit")` - Bandits liest so die XML-Marke `BumpAnimFinished` (`ZATime.lua:13`, am IsoZombie;
  `getVariableString` ist eine Default-Methode von `IAnimationVariableSource`, IsoAnimal ueberschreibt nichts davon, javap).
  Vergleich `== "true"`.
- Zustand fragen: `animal:getActionStateName()` (Bandits 17-mal am IsoZombie, `ZASmack.lua:486`; IsoGameCharacter, nicht
  ueberschrieben). Erwartet `"idle"`, `"pathfind"`, `"walk"`, `"hitreaction"`.

### 1.5 Treffermoment und Ende

- `AnimNode.Parse` macht aus `<m_EventName>SetVariable</m_EventName>` ein `AnimEventSetVariable`; dessen Konstruktor teilt
  `"Name=Wert"` (Offset 9-38). Der Charakter setzt den Wert (`IsoGameCharacter.OnAnimEvent_SetVariable` Offset 21-27). Die
  Hoerer werden im Konstruktor fuer jeden Charakter angemeldet, ausser fuer Zombies auf dem Server
  (`IsoGameCharacter.<init>` Offset 1016-1034) - fuer Tiere also ueberall.
- Treffer: `SetVariable NCBearHit=true` bei `<m_TimePc>` (Vanilla nutzt 0.1 bis 0.5, z. B. 0.4 dreimal).
- Ende: `SetVariable NCBearDone=true` bei `<m_Time>End</m_Time>` (Vanilla 105-mal, `SatChairIn.xml`; Bandits `zsloot.xml`).
- **Loeschen per Ereignis geht nicht sauber:** `ClearVariable` ist in Java angemeldet, aber in keiner Vanilla-XML benutzt;
  `"NCBearAct="` wuerde wegen `String.split` eine Variable namens `NCBearAct=` setzen. Also loescht Lua nach `NCBearDone`.
- Lua fragt die zwei Marken je Bild (`Events.OnTick`), nur fuer Baeren im Kampf. Gelesen = sofort `clearVariable`, vor jedem
  neuen Angriff beide loeschen (eine Marke aus einem abgebrochenen Hieb darf nicht den naechsten ausloesen).
- **Netz fuer den Fall, dass der Knoten nicht spielt** (Baer verlaesst `idle`, Clip fehlt): Frist in Spielzeit, Summe von
  `getGameTime():getMultiplier()` (`ISAnimalTracksFinder.lua:28`; keine Wanduhr, CLAUDE.md v3.9.43). Frist = Clipdauer + 1 s,
  danach `NCBearAct` loeschen und den Treffer verwerfen, nie nachholen.
- Rueckweg: `NCBearAct` geloescht -> `idle1` gewinnt wieder (Blende ueber `m_BlendTime` des Zielknotens), danach
  `setBlockMovement(false)` (`ISPetAnimal.lua:49`) -> normales Herumlaufen.
- Zweimal derselbe Hieb hintereinander: Variable einmal loeschen (ein Bild `idle1`), erst dann neu setzen; sonst laeuft der
  Knoten nicht neu an.

### 1.6 Knoten-Vorlage (Prankenhieb links)

```xml
<?xml version="1.0" encoding="utf-8"?>
<animNode>
	<m_Name>NCBearSwipeL</m_Name>
	<m_AnimName>NCBear_SwipeL</m_AnimName>
	<m_Looped>false</m_Looped>
	<m_BlendTime>0.15</m_BlendTime>
	<m_SyncTrackingEnabled>false</m_SyncTrackingEnabled>
	<m_ConditionPriority>10</m_ConditionPriority>
	<m_Conditions>
		<m_Name>NCBearAct</m_Name>
		<m_Type>STRING</m_Type>
		<m_Value>swipeL</m_Value>
	</m_Conditions>
	<m_Events>
		<m_EventName>PlaySound</m_EventName>
		<m_TimePc>0.27</m_TimePc>
		<m_ParameterValue>SledgehammerSwing</m_ParameterValue>
	</m_Events>
	<m_Events>
		<m_EventName>SetVariable</m_EventName>
		<m_TimePc>0.42</m_TimePc>
		<m_ParameterValue>NCBearHit=true</m_ParameterValue>
	</m_Events>
	<m_Events>
		<m_EventName>SetVariable</m_EventName>
		<m_Time>End</m_Time>
		<m_ParameterValue>NCBearDone=true</m_ParameterValue>
	</m_Events>
</animNode>
```
Elementnamen gegen das Jar geprueft (`AnimNode`/`AnimCondition` XmlElement: m_ConditionPriority, m_Conditions, m_Value,
m_Events, m_TimePc ...). Translation_Data im Clip still lassen (Bewegungsknochen `idle` ist Translation_Data,
`AnimNode.getDeferredBoneName`): ob ein Weg im Stand den Baeren verschiebt, ist ungeprueft.

---

## 2. Bewegung

| Zweck | Aufruf | Fundstelle | Was es tut (Jar) |
|---|---|---|---|
| Anrennen zur Kachel | `animal:fleeTo(sq)` | `ISMilkAnimal.lua:38`, `ISShearAnimal.lua:38` | loest Leine/Baum, `animalRunning = true`, `pathToLocation(x,y,z)` (`IsoAnimal.fleeTo` Offset 43-65). Galopp-Clip `DeerStag_Run` mit 3,17 Kacheln/s |
| Anhalten | `animal:stopAllMovementNow()` | `ISAnimalContextMenu.lua:760`, `:1000` | `setMoving(false)`, Weg leeren, Standardzustand (`IsoAnimal.stopAllMovementNow` Offset 0-27) |
| Herumlaufen sperren | `animal:getBehavior():setBlockMovement(true/false)` | `ISPetAnimal.lua:36/:49`, `ISAnimalContextMenu.lua:89` | `true` ruft selbst `stopAllMovementNow` (Offset 0-8); `wanderIdle` kehrt zurueck; loest sich nach Summe 8000 der Spieltakte selbst (`wanderIdle` Offset 0-39) |
| Blick | `animal:faceThisObject(obj)` | `ISPetAnimal.lua:17` (Tier sieht Spieler an) | Ziel ist IsoGameCharacter -> `faceThisObjectAlt`, setzt Richtung sofort (`IsoGameCharacter.faceThisObject`). Ein Zombie ist ebenso IsoGameCharacter |
| Blick grob | `animal:setDir(IsoDirections.NE)` | `ButcheringUtil.lua:574` | 8 Richtungen |
| Sicht | `animal:CanSee(zombie)` | Bandits `BanditUpdate.lua:1087` (am IsoZombie) | reine Linienpruefung `LosUtil.lineClear` (`IsoGameCharacter.CanSee(IsoObject)` Offset 0-50), kein Blickkegel |
| Gehen (nicht rennen) zum Ziel | `pathToLocation(x,y,z)` | **nur am Zombie** `DebugContextMenu.lua:640`; IsoAnimal ueberschreibt die Methode | **nicht belegt am Tier, nicht noetig** (Anrennen reicht) |

- **Wo es wirkt:** `IsoAnimal.isLocalPlayer` = `!GameClient.client` (Offset 0-11); `AnimalIdleState.execute` arbeitet nur dann
  (Offset 5-12), `IsoAnimal.updateInternal` ruft auf einem MP-Client nur `separate` und `IsoPlayer.update` (Offset 23-85).
  **Bewegungsbefehle wirken im Einzelspieler und auf dem Server, auf einem MP-Client nicht.**
- `animalRunning` setzt erst das naechste normale `wanderIdle` zurueck (Offset 837-840). Nach dem Kampf also kurz traben, das ist harmlos.
- **Flucht vor Laerm:** `IsoAnimal.respondToSound` (aus `updateInternal` Offset 145) laeuft auch zahm, ausser bei Fahrzeuglaerm
  (Offset 141-154), Radio/TV (Offset 120-139). Kein Feld, kein Lua-Schalter. Belegter Gegenzug: im Kampf jede Bewegung, die wir
  nicht selbst befohlen haben (`getActionStateName()` ist `walk`/`pathfind`, eigene Marke "laeuft an" fehlt), sofort mit
  `stopAllMovementNow` beenden. Danach gibt `respondToSound` den Laerm frei (Offset 28-88), ein neuer Schuss startet einen
  neuen Versuch - das gibt ein Bild Zucken, kein Weglaufen.
- **Flucht nach Treffer** (`fleeFromAttacker`) kommt nur, wenn jemand den Baeren schlaegt (Spieler). Vorschlag: dann den Kampf
  abbrechen und ihn fliehen lassen.
- `wild = false`, `fleeZombies = false` (NCBearDefs.lua): Zombies loesen keine Flucht aus (`BaseAnimalBehavior.spotted`, tier_spez 5.2).

---

## 3. Schaden, Umwerfen, wer darf

### 3.1 Belegte Aufrufe am Ziel (IsoZombie, Bandit eingeschlossen)

| Zweck | Aufruf | Fundstelle |
|---|---|---|
| Leben lesen/setzen | `z:getHealth()`, `z:setHealth(h)` | Bandits `BanditClientCommands.lua:33-36`, `BanditUpdate.lua:2397` |
| toedlich | `z:Kill(nil)` | Bandits `BanditUpdate.lua:2386`, `:2394` (am Banditen = IsoZombie) |
| umwerfen | `z:knockDown(hitFromBehind)` | `DebugContextMenu.lua:668`. Jar `IsoZombie.knockDown` Offset 0-43: `setKnockedDown(true)`, `setStaggerBack(true)`, `setHitReaction("")`, `setPlayerAttackPosition(BEHIND/null)`, `setHitForce(1)`, `reportEvent("wasHit")` |
| umwerfen (Bandits-Form) | `setHitFromBehind`, `setPlayerAttackPosition(z:testDotSide(a))`, `setHitForce(1)`, `setKnockedDown(true)` | Bandits `ZAPush.lua:41-45` |
| von hinten? | `(dx*fwd:getX() + dy*fwd:getY()) / len > 0.5`, `fwd = z:getForwardDirection()` | Bandits `ZAPush.lua:32-39` |
| Blut | `z:splatBlood(3, 0.3)` (n-mal), `z:splatBloodFloorBig()`, `z:playBloodSplatterSound()` | Bandits `BanditCompatibility.lua:130-133` (Opfer Zombie in `ZASmack.lua:462`) |
| Treffer-Ton | `z:playSound(name)` | Bandits `ZASmack.lua:444` |
| liegt? | `z:isProne()` oder `z:getActionStateName() == "onground"` | Bandits `ZASmack.lua:486` |
| nicht mehr da | `z:isDead()`, `z:isOnKillDone()` | Bandits `ZASmack.lua:357/:372` |
| gezogene Leiche | `z:isReanimatedForGrappleOnly()` | Bandits `BanditCompatibility.lua:189`, ausgefiltert in `BanditZombie.lua:118` |
| Scheintot | `z:isFakeDead()` | `DebugContextMenu.lua:660` |

**`setBumpFall BanditUtils.lua:323` ist kein Beleg:** die Zeile steht in einem auskommentierten Block (`--[[ ... ]]`,
BanditUtils.lua:303-326) und gilt Spielern. `ZASmack.lua:413` setzt `setBumpFall` nur bei rennenden Opfern (Spieler).
Fuer Zombies ist `knockDown` der Weg.

### 3.2 Reihenfolge je Treffer (Einzelspieler)

1. Ziel neu pruefen (Filter 3.4, Abstand, Kegel, `CanSee`) - das Objekt kann seit dem Ausholen wiederverwendet sein (CLAUDE.md v3.9.35).
2. `h = z:getHealth() - schaden`. Wenn `h <= 0`: Blut, Ton, `z:Kill(nil)`, fertig.
3. Sonst `z:setHealth(h)`, Blut, Ton, `z:knockDown(vonHinten)` - nur wenn er nicht schon liegt.

Im Einzelspieler ist das alles: kein Paket, keine Hoheit. Ungeprueft im Spiel: ob `knockDown` nach `setHealth` aus jedem Zustand
(Angriff, Lunge, bumped) sauber faellt. Bandits ruft es aus denselben Lagen (`ZAPush`), aber ohne vorherigen Schaden.

### 3.3 Warum nicht `zombie:Hit(...)` (Bandits `ZASmack.lua:443`)

Der Weg ist belegt und gibt Trefferbild, Ereignisse und Tod gratis, aber der Schaden ist kaum planbar (javap):
- `IsoGameCharacter.Hit` Offset 10-75: Nahkampf auf Zombie zaehlt `hitTime` hoch, ab dem 4. Treffer `x (hitTime-2) x 1,5`.
- `processHitDamage`: `CombatManager.applyPlayerReceivedDamageModifier` (Nicht-Spieler x 1,5), `applyWeaponLevelDamageModifier`
  (Angreifer ohne Waffe in der Hand: Stufe 0 -> x 0,3), `applyOneHandedDamagePenalty` (Zweihaender ohne zweite Hand x 0,5).
- `hitConsequences` Offset 4-21: `applyGlobalDamageReductionMultipliers` (Nahkampf x 0,15), dann `applyDamage` (Leben minus Wert).
- Vorgaben aus `CombatConfigKey.<clinit>`: 0,3 / 0,1 je Stufe / 1,5 / 0,15 / 0,5 (Konfiguration kann sie aendern, ungeprueft wo).
- Toedlich: nur ausserhalb eines MP-Clients (`hitConsequences` Offset 55-77).
- Nebenwirkung: `OnHitZombie`, `OnWeaponHitCharacter` feuern - Bandits' und NPC Crews Aufsaetze laufen mit.
`setHealth` + `knockDown` + `Kill(nil)` ist enger und rechnet genau das, was Kevin will. Die Engine-Reaktion (Taumeln) ersetzt
das Umwerfen.

### 3.4 Wer ist ein Ziel (harte Regel)

Liste: nur `getCell():getZombieList()` (Bandits `BanditZombie.lua:110`, `BanditServerZombie.lua:15`). Darin stehen nur
IsoZombie: Spieler, Tiere, Fahrzeuge, Kisten sind ausgeschlossen, ohne Filter.

```
kein Ziel, wenn:  isDead / isOnKillDone / isReanimatedForGrappleOnly / isFakeDead / andere Ebene (|dz| >= 0.5)
Bandit?           z:getVariableBoolean("Bandit") (BanditZombie.lua:137)  oder  z:getModData().brain (BanditBrain.lua:3-5)
  Gehirn fehlt, Marke da          -> kein Ziel (im Zweifel nicht)
  brain.recruited                 -> nie (NPC Crew, BanditsNPCInteract.lua:1055)
  brain.npcNeutral, brain.programFallback == "NPCNeutral", Programmname beginnt mit "NPC"  -> nie (NPC Crew, BanditsNPCCompat.lua:32-43)
  brain.loyal                     -> nie (Bandits "babe", BanditUtils.lua:785-786)
  brain.hostile or brain.hostileP -> Ziel (Bandit.IsHostile, Bandit.lua:600-605)
  sonst (Zivilist, neutral)       -> nie
kein Bandit -> Zombie -> Ziel
```
- Bandits und NPC Crew sind optional: Gehirn direkt aus ModData lesen (das ist `BanditBrain.Get`), NPC-Crew-Felder sind nur Tabellenfelder.
  Kein Aufruf in NPC Crew, keine Abhaengigkeit.
- NPC Crew setzt waehrend eines Spieler-Treffers kurz `hostileP = true` auf Crew und Neutrale und nimmt es im selben Aufruf
  zurueck (`BanditsNPCCompat.lua:171-195`). Lua ist einfaedig, unser Test laeuft nie dazwischen; trotzdem steht `recruited`/
  `npcNeutral` VOR `hostileP` in der Pruefung.
- Mehrspieler: das Gehirn im Koerper kann veraltet sein (CLAUDE.md v3.9.8, aktuell ist nur `GetBanditClusterData(id)[id]`) - fuer Stufe 1 egal (SP).

### 3.5 Einzelspieler / Mehrspieler

| | Einzelspieler | Mehrspieler |
|---|---|---|
| Baer-KI, Bewegung | lokal | **nur Server** (`IsoAnimal.updateInternal` Offset 23-85, `AnimalIdleState.execute` Offset 5-12) |
| Zombie-KI | lokal | Client mit Hoheit (`bClient` falsch, CLAUDE.md Abschnitt 5); Server rechnet keinen Zombie, `OnZombieUpdate` feuert dort nie |
| Animation, Anim-Ereignisse, Toene | lokal | jeder Client fuer seine Kopie; der Server spielt keine Ereignisse (Vanilla emuliert sie: `ISPetAnimal.lua:83` `emulateAnimEventOnce`) |
| Leben | lokal | Bandits schickt `Sync.Health` an den Server, der an alle (`BanditServerSync.lua:5`), Clients **senken** nur (`BanditClientCommands.lua:35`) |
| Tod | `Kill(nil)` | auf einem Client toetet `hitConsequences` nie (Offset 68-77); was `Kill(nil)` auf einem Client ohne Hoheit tut: **ungeprueft** |
| Umwerfen | lokal | Bandits wirft vom Rechner des Banditen aus um (`ZAPush`, ohne Paket); ob der Besitzer-Client das sieht: **ungeprueft** |

**Vorschlag:** Stufe 1 nur Einzelspieler (`not isClient() and not isServer()`, `ISEatFoodAction.lua:136`), im MP tut der Baer
nichts Neues. Stufe 2 (eigener Lauf, eigenes Wort): Server rechnet Ziel und Bewegung und schickt `sendServerCommand`; jeder Client
spielt den Knoten an seiner Kopie und rechnet Schaden nur fuer Zombies mit eigener Hoheit (`not z:getVariableBoolean("bClient")`),
Leben ueber Bandits' `Sync.Health`. Davor zu belegen: Tod auf dem Client, Umwerfen fremder Zombies, ob eine Client-seitige
Variable am Tier gegen die Server-Pakete haelt.

### 3.6 Was Zombies mit dem Baeren machen, und Schaden am Baeren (Vorschlag, nicht bauen)

- Zombies nehmen ihn nie als Ziel (`AttackState.triggerPlayerReaction` Offset 20-33: Tier-Ziel -> `target = null`); `IsoZombie`
  fragt `isAnimal` sonst nur bei Leichen (`updateSearchForCorpse`). Bandits schiessen nur auf Spieler und Zombies (BanditUtils um 330).
  **Er ist im Kampf heute unverwundbar.**
- Spieler koennen ihn treffen: dann Flucht 20 Kacheln (`fleeFromAttacker`), Tod moeglich.
- Optionen fuer Kevin:
  A. so lassen (unverwundbar gegen Zombies).
  B. "Kratzer" selbst rechnen: je Zombie, der vor ihm steht (unter 0,8 Kacheln, ihm zugewandt), alle 2 s Leben minus 2 %, bei
     unter 30 % Kampf abbrechen und fliehen. `animal:setHealth(x)` ist am Tier belegt (`ISVehicleAnimalUI.lua:201`, `ClientCommands.lua:882`);
     `IsoAnimal.setHealth` beachtet `isInvincible` und schickt im MP selbst ein Update (Offset 1-38).
  C. Schalter "unverwundbar" zum Testen: `animal:setIsInvincible(true)` (`ISAnimalContextMenu.lua:563`, Server `ClientCommands.lua:861`).

---

## 4. Toene

### 4.1 Eigene Dateien

- Sound-Skript (Vanilla `generated/sounds/zombies/sounds_zombie_voice_tutorial.txt`):
  ```
  module Base
  {
      sound NCBearRoar1
      {
          category = Animals,
          clip
          {
              file = media/sound/ncbear_roar1.wav,
              distanceMax = 100,
              volume = 1.0,
          }
      }
  }
  ```
  `category = Animals` wie die Tierstimmen (`sounds_animal_bull.txt`, 184-mal), `distanceMax` Vanilla 150 bei Tieren.
  Bandits zusaetzlich `is3D = true`, `distanceMin`, `reverbFactor` (`zs_sounds.txt`), Bandits-Modul `Bandits` - Namen gelten global.
- Ablage wie Bandits: Skript im Versionsordner (`42/media/scripts/nc_bear_sounds.txt`), Dateien unter `common/media/sound/`
  (Bandits `common/media/sound/zs_hit1.wav`). Fuer eine Mod nur im Spielstand: `Core.ResetLua` Offset 51 `GameSounds.Reset`, Laden danach - **ungeprueft** fuer unseren Ablauf, Bandits ist bei Kevin vermutlich dauerhaft aktiv.
- Format: Vanilla `fzombierand5.wav` ist mono 44,1 kHz 16 bit (gemessen); Bandits' `zs_hit1.wav` stereo 44,1 kHz. **Mono 44,1 kHz 16 bit nehmen**, kurz (unter 3 s).
- Zufall zwischen Dateien: `GameSound.getRandomClip` (Jar) spricht fuer mehrere `clip`-Bloecke je Ton, mit `file =` in Vanilla nicht belegt. Sicher: je Datei ein Ton-Name.

### 4.2 Rohaufnahmen (Lautstaerke-Huelle, `_arbeit/baer_kampf/werkzeug/huelle.py`, 100-ms-Fenster)

| Datei | Laenge | laut (> -12 dB) | Vorschlag Schnitt (anhoeren!) |
|---|---|---|---|
| soundbible_242 (48 kHz stereo) | 20,8 s | fast durchgehend | **NCBearRoar1** 1,6-4,0 s, **NCBearRoar2** 11,1-13,4 s (Aufrichten) |
| soundbible_241 (48 kHz stereo) | 15,5 s | Stoesse 0,2-0,9, 2,9-3,5, 6,6-7,8, 8,6-9,4, 11,3-12,1 s | **NCBearGrowl1** 2,8-3,6 s, **NCBearGrowl2** 8,5-9,5 s (Hieb, Anrennen) |
| soundbible_868 (44,1 kHz mono) | 6,2 s | 0,5-1,4, 3,2-3,9 s | "Baer und Junge": kann Jungtiere enthalten, **nur nach Anhoeren** (z. B. Schnauben 0,5-1,4 s) |

Umwandeln mit Python 3.12 (`wave`, `audioop` ist in 3.12 noch da): mono mischen, 48 -> 44,1 kHz, auf -1 dB normalisieren,
30 ms ein-/ausblenden. Kevin hoert die Schnitte vor dem Einbau.

### 4.3 Abspielen

| Weg | Wo belegt | Wann nehmen |
|---|---|---|
| Anim-Ereignis `PlaySound` mit Tonname | `cockerel/attack/attackDefault.xml`, `hen/death/death.xml`; Java `IsoGameCharacter.OnAnimEvent_PlaySound` -> `getEmitter().playSoundImpl` | **Bruellen, Wusch, Knurren**: genau im Bild, auf jedem Rechner, der die Animation spielt |
| Anim-Ereignis `PlayBreedSound` | `buck/hitreaction/hitreaction1.xml`; im Zustand idle verarbeitet (`AnimalIdleState.animEvent` Offset 57-139) | nur wenn der Ton in `breeds.brown.sounds` steht (Muster `CowDefinitions.lua:315-330`, `slot = "voice"`, `priority`) |
| Lua am Tier | `animal:playBreedSound("roar")` (`ISHutchGrabAnimal.lua:31`) | wenn ohne Knoten |
| Lua am Ziel | `z:playSound(name)` (Bandits `ZASmack.lua:444`) | **Treffer**, Ton sitzt am Getroffenen |

### 4.4 Laerm fuer Zombies: nicht in Stufe 1

`addSound(quelle, x, y, z, radius, lautstaerke)` ist belegt (`ISBuildAction.lua:103`). Aber: `WorldSoundManager.getSoundAnimal`
schliesst die Quelle nicht aus, und im Lua-Weg setzt `addSound(..14 Argumente)` Offset 0-1 immer Bit 4 der Flags, aus denen
`WorldSound.init` `stressAnimals` schreibt (welches Bit welches Feld ist: ungeprueft). `IsoAnimal.respondToSound` laesst ihn dann
vor dem eigenen Bruellen fliehen. Wenn Kevin will, dass Zombies den Kampf hoeren: erst im Spiel pruefen, mit dem Fluchtstopp aus 2.

### 4.5 Spieltoene fuer Wusch und Treffer (Namen aus `media/scripts/generated/sounds`)

| Zweck | Name | Datei |
|---|---|---|
| Wusch Prankenhieb | `SledgehammerSwing` | `weapons/sounds_melee_bluntlong.txt:957` |
| Wusch, leichter | `LargeAnimalBoneSwing` / `AxeSwing` | `sounds_melee_bluntlong.txt:3090` / `sounds_melee_bladelong.txt:93` |
| Treffer wuchtig | `SledgehammerHit` | `sounds_melee_bluntlong.txt:939` |
| Treffer Krallen | `MacheteHit` / `HeadSlice` | `sounds_melee_bladelong.txt:39` / `zombies/sounds_zombie_foley.txt:30` |
| toedlicher Treffer | `HeadSmash` | `sounds_zombie_foley.txt:12` |
| Biss | `ZombieBite` / `ZombieScratch` | `sounds_zombie_foley.txt:210/:201` |
| Doppelschlag auf Boden | `AttackStomp` | `player/sounds_player_combat.txt:12` |
| Aufprall des Umgeworfenen | `BodyHitGround` | `sounds_zombie_foley.txt:256` - spielt die Sturz-Animation des Zombies schon selbst (44 Zombie-Knoten unter `AnimSets/zombie` mit `PlaySound BodyHitGround`) |

---

## 5. Vorschlag Kampfablauf

### 5.1 Zahlen zur Orientierung (gemessen bzw. gelesen)

- Baer: Gang 0,67 Kacheln/s, Galopp 3,17 Kacheln/s (bau_lebend.md). 1 Kachel = rund 1,23 m (0,544 E/m x 1,5 Kacheln/E). Koerper
  rund 2 Kacheln lang, Mitte bis Brust rund 0,8 Kacheln.
- Zombie-Leben (`IsoZombie.resetForReuse` Offset 316-443): zaeh 3,5-3,8, **normal 1,8-2,1**, zerbrechlich 0,5-0,8, Zufall 0,5-3,8.
- Banditen: `brain.health` = Lerp(Einstellung 1..9) auf 1,0..2,6, Vorgabe 5 -> 1,8 (`BanditServerSpawner.lua:343-344`).

### 5.2 Ablauf (Zustaende in Lua, je Baer)

1. **Ruhe** (heute): alle 0,5 s Spielzeit Ziel suchen: gleiche Ebene, 10 Kacheln (Feinde mit Gehirn 12), `CanSee`, Filter 3.4.
   Wahl: naechster, feindlicher Bandit zaehlt 3 Kacheln naeher (er schiesst auf den Spieler). Kein Ziel -> Ruhe.
2. **Drohen** beim ersten Kontakt, wenn das letzte Bruellen ueber 45 s her ist: `stopAllMovementNow`, `setBlockMovement(true)`,
   `faceThisObject(ziel)`, Knoten `rear` (3,0 s, Bruellen im Bild). Danach sofort Angriff.
3. **Anrennen**: `setBlockMovement(false)`, `fleeTo(ziel:getSquare())`, alle 0,75 s neu, wenn das Ziel ueber 1 Kachel gewandert ist
   oder der Weg endete. Ankunft bei Abstand <= 1,5: `stopAllMovementNow`, `setBlockMovement(true)`.
   Steckt fest (Abstand sinkt in 3 s um weniger als 0,5): Ziel 20 s sperren, naechstes.
4. **Zuschlagen**: Blick aufs Ziel bis zum Treffer, dann fest. Auswahl:
   - Ziel liegt (`isProne`/`onground`) und <= 1,4 vor ihm: **Biss** (`maul`).
   - mindestens 2 weitere Gegner <= 2 Kacheln im vorderen Halbkreis und Doppelschlag 10 s nicht benutzt: **Doppelschlag** (`slam`).
   - sonst **Prankenhieb** abwechselnd links/rechts.
   Pause 0,35 s zwischen zwei Angriffen. Bei 3 oder mehr Gegnern in 3 Kacheln und Bruellen frei: 25 % Chance erneut `rear`.
5. **Ende**: Ziel tot -> neu suchen (8 Kacheln). 3 s kein Ziel, Baer ueber 25 Kacheln vom Kampfbeginn, 90 s Kampf am Stueck
   (dann 20 s Ruhe), Baer getroffen von einem Spieler, Baer tot -> Variablen loeschen, `setBlockMovement(false)`, Ruhe.

### 5.3 Treffer-Flaechen (Mitte des Baeren, Blickrichtung `getForwardDirection`)

| Angriff | Reichweite | Winkel | Ziele | Schaden (Leben) | Umwerfen |
|---|---|---|---|---|---|
| Prankenhieb L/R | 1,8 Kacheln | 110 Grad, 15 Grad zur Schlagseite verschoben (-40..+70) | Hauptziel + bis 3 im Kegel | Haupt **1,3** (65 % eines normalen Zombies), Neben **0,8** (40 %) | alle Ueberlebenden |
| Doppelschlag | 2,0 Kacheln | 160 Grad | bis 5 | je **1,0** (50 %) | alle |
| Biss am Boden | 1,4 Kacheln | 60 Grad | 1, nur liegend | **2,5** (toedlich fuer normal) | - |

Normaler Zombie: Hieb (liegt, Rest 0,5-0,8) + Biss = tot, zwei Hiebe = tot. Zaeh: drei Hiebe. Ein Faktor `NCBear.DMG` (Vorgabe 1,0)
zum Nachstellen ohne Neustart. Jedes Ziel je Hieb hoechstens einmal; Deckel 6 Treffer je Angriff.

### 5.4 Deckel und Kosten

- Baeren finden: beim Spawnen merken; dazu alle 5 s `getCell():getObjectListForLua()` (kopiert die ganze Menge in eine Liste,
  `IsoCell.getObjectListForLua` Offset 0-14 - darum nicht oefter), `instanceof(o, "IsoAnimal")` und `getAnimalType() == "bear"`
  (Form `NCBearSpawn.lua:65-75`). Hoechstens 4 Baeren gleichzeitig im Kampf, 8 gemerkt.
- Zielsuche: Zombie-Liste einmal je 0,5 s fuer alle Baeren, nur Abstand (Quadrat) und Ebene, `CanSee` nur fuer den Kandidaten.
- Je Bild nur fuer kaempfende Baeren: zwei Variablen lesen, ein Abstand, eine Frist. Nichts im `render`.
- Gesperrte Ziele: Tabelle mit hoechstens 32 Eintraegen, Frist 20 s.
- Kahlua: kein `next`, `pairs` nehmen (CLAUDE.md v3.9.13). Keine Mehrfachrueckgabe in ein Argument.

### 5.5 Noetige Clips (30 Bilder/s wie `baer_tier.py`, Translation_Data still)

| Clip / `NCBearAct` | Dauer | Bilder | Ereignisse (`m_TimePc`) | Inhalt |
|---|---|---|---|---|
| `NCBear_Rear` / `rear` | 3,00 s | 90 | PlaySound `NCBearRoar1` 0,27 (0,8 s), Done End | 0-0,8 s auf die Hinterbeine, 0,8-2,2 s stehen, Kopf hoch, Maul offen, Pranken vor der Brust, 2,2-3,0 s zurueck auf vier |
| `NCBear_SwipeL` / `swipeL` | 1,10 s | 33 | PlaySound `SledgehammerSwing` 0,27, Hit 0,42 (0,46 s), Done End | Gewicht nach rechts, linke Pranke holt aussen-oben aus, schlaegt quer nach innen-unten, Schulter dreht mit, zurueck |
| `NCBear_SwipeR` / `swipeR` | 1,10 s | 33 | gespiegelt | gespiegelt |
| `NCBear_Slam` / `slam` | 2,20 s | 66 | PlaySound `NCBearGrowl1` 0,05, PlaySound `AttackStomp` 0,55, Hit 0,57 (1,25 s), Done End | halb aufrichten (0-0,9 s), beide Pranken nach unten (0,9-1,25), Rumpf faellt nach vorn, aufstehen |
| `NCBear_Maul` / `maul` | 1,60 s | 48 | PlaySound `NCBearGrowl2` 0,10, Hit 0,34 (0,55 s), Done End | Kopf tief, Biss, zweimal Schuetteln, hoch |

Der Knoten-Name ist frei (`NCBear_*`), nur `m_AnimName` muss dem Aktionsnamen im GLB gleichen (tier_spez 2.2). Alle Knochen in
jedem Clip mit Schluesseln (tier_spez 2.4). Danach `Probe.java` und die Dehnungsmessung wie bau_lebend.md: beim Aufrichten
dreht das Becken rund 70 Grad, Bauch und Hueften sind die Stellen, an denen die Haut reissen kann.

### 5.6 Knochen und Netz

- Heute 25 Knochen ohne Kiefer (`baer_tier.py`:56-75). Fuer das offene Maul **neuer Knochen `Bip01_Jaw`** (Kind von
  `Bip01_Head`, Gewichte nur am Unterkiefer). Grenze 60 Knochen (`animalEffect.vert`:16) bleibt weit. **Ungeprueft:** ob das
  Spielnetz einen getrennten Unterkiefer hat; wenn nicht, reisst das Maul auf. Rueckfall: Kopf hoch, Maul zu, nur der Ton.
- Ein neuer Knochen heisst neuer Export aller Clips (die vorhandenen fuenf bekommen fuer ihn Schluessel in Ruhehaltung).

### 5.7 Neue und geaenderte Dateien (Stufe 1, Einzelspieler)

```
42/media/AnimSets/buck/idle/NCBear_Rear.xml, NCBear_SwipeL.xml, NCBear_SwipeR.xml, NCBear_Slam.xml, NCBear_Maul.xml
42/media/models_X/Skinned/NCBear.glb          +5 Clips (+ Bip01_Jaw)
42/media/scripts/nc_bear_sounds.txt            NCBearRoar1/2, NCBearGrowl1/2
common/media/sound/ncbear_*.wav                mono 44,1 kHz
42/media/lua/shared/NCBearFight.lua            Kampf, nur wenn not isClient() and not isServer()
42/media/lua/client/NCBearSpawn.lua            (optional) Menue "Bear fights: on/off", Konsole NCBear_Fight(true/false)
```
Keine Datei von `buck` geaendert, nichts unter NPC Crew oder Bandits.

---

## 6. Was nur Kevins Test entscheidet

- Spielen die Knoten am Baeren (und an keinem Reh)? Kommen `NCBearHit`/`NCBearDone` an?
- Fallen Zombies nach `setHealth` + `knockDown` aus jedem Zustand, stehen sie wieder auf?
- Dreht `faceThisObject` ihn sichtbar ruckartig (setzt sofort)?
- Haelt der Fluchtstopp bei Schuessen, ohne Zucken im Dauerfeuer?
- Klingen die Schnitte, Lautstaerke, Reichweite?
- Haut beim Aufrichten, Maul.
- Wirkt "fett" richtig (Faktor `NCBear.DMG`)?

## 7. Fragen an Kevin

1. Soll der Baer Schaden nehmen koennen (3.6: A unverwundbar, B Kratzer, C Testschalter)?
2. Mehrspieler-Kampf als eigene Stufe 2 - oder erst mal nur Einzelspieler?
3. Kiefer-Knochen fuer das offene Maul versuchen (Risiko Netz), oder Bruellen mit geschlossenem Maul?
4. Sollen Zombies den Kampf hoeren (Laerm zieht weitere an, 4.4)?

Statisch geprueft, nicht gespielt.
