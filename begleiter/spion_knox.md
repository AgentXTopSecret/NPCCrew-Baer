# Knox Wildlife gelesen: wie sie Baeren bauen (nur Mechanik, nichts uebernommen)

Stand 08.11.2026. Mod: Workshop 3818096743, `mods/KnoxWildlife/42.21`, Version 0.1.6, `versionMin=42.21.0`, Autor "Jordan"
(`42.21/mod.info:1-7`). Alle 204 Dateien ueberblickt, alle 18 Lua-Dateien gelesen (`CarcassSilhouettes.lua` ist reine
Zahlentabelle, nur Aufbau gelesen), alle 90 Clips und 7 Netze mit eigenem Leseskript vermessen
(`_arbeit/baer_spionage/tools/xscan.py`, `xmove.py`), Jar-Klassen nach `_arbeit/baer_spionage/jar/knox/`.
**Nichts kopiert, keine Datei, kein Code, kein Clip, kein Ton.** Statisch gelesen, nicht gespielt.

Schreibweise: `Datei:Zeile` in der fremden Mod (Lua unter `42.21/media/lua/shared/KW/` bzw. `client/KW/`), Vanilla mit
`media/...`, Jar `Klasse.methode Offset`.

## Lizenz und Herkunft (fuer Kevins Regel)

* Code und "authored animation logic": MIT (`LICENSE.txt:1-20`). Ausgenommen: Modelle/Texturen CC BY 4.0 (Sketchfab, sechs
  Urheber, `CREDITS.txt:9-51`), Ton CC0 1.0 bzw. CC BY 3.0 (`AUDIO_CREDITS.txt:5-21`; Baerentoene: U.S. Fish & Wildlife
  Service ueber opengameart "Bear Growls", CC0).
* Selbstauskunft: Umsetzung und Bewegungen "authored for this mod with Codex" (`CREDITS.txt:53`), AnimSet-Knoten "adapt the
  installed game's animal state patterns" (`:54`). Kojote- und Luchsmodell laut Quelle KI-erzeugt (`CREDITS.txt:29, :44`).
* Fuer uns: auch MIT aendert nichts an Kevins Regel. Wir uebernehmen nur Ideen, mit Herkunft in Changelog/Kommentar.

## (1) Tier-Definition und der AnimSet-Trick

**Arten:** sechs, je `kw<Art>Male/Female/Young` (`Definitions.lua:16-18`), Gruppe `kw<Art>`, Rasse `wild`. Tabelle der
Kennzahlen `Definitions.lua:10` (Baeren: Schaden 1.35/1.8, `healthLossMultiplier` 0.022/0.017, Groesse 0.5/0.65, Alter 120/150).

**Wichtige Felder** (`Definitions.lua:50-69`): `animset="pig"`, `bodyModel=KW_<Art>`, `wild=true`, `alwaysFleeHumans=true`,
`fleeZombies` nur fuer Junge und Elch, `attackBack` ausser Junge, `attackIfStressed=false`, `dontAttackOtherMale=true`,
`baseDmg`, `attackDist=1`, `attackTimer=1800`, `healthLossMultiplier`, `canThump=false`, `canClimbStairs=false`,
`canBePicked/Pet/FeedByHand/Domesticated=false`, `idleTypeNbr=3`, `sitRandomly`, `hungerMultiplier=thirstMultiplier=0.001`,
`ropeBone="Bip01_Head"`. Genom: Kopie von `deer` (`:24`). Dazu `AnimalPartsDefinitions` (`:80-82`),
`AnimalAvatarDefinition` mit `hook` fuer Erwachsene (`:85-88`), Spuren (`:96-101`). Nichts an Vanilla-Arten geaendert, nur
kopiert (`clone`, `:11-14`).

**Der Trick gegen "ActionGroups nur aus dem Spielordner":** dieselbe Feststellung wie unser `tier_spez.md` 3.1, von ihnen
selbst gemessen (`AnimationCompatibility.lua:1-2`, `PLAYTEST-0.1.2.txt:24-25`; `common/media/actiongroups/` enthaelt nur
`.keep`). Ihr Weg hat drei Teile:
1. `animset = "pig"`: die Vanilla-Gruppe `pig` hat einen Zustand `attack` (`media/actiongroups/pig/attack/`, Uebergang
   `idle/to_attack.xml` auf `isAnimalAttacking`), anders als `buck`.
2. **Aliase im eigenen Netz:** jeder Clip steht zweimal in der Datei, als `KW_BrownBear_Attack` UND als `FarmPig_Attack_Bite`
   (eigenes `AnimationSet`, gleiche Daten). 15 eigene + 17 Aliase = 32 Saetze je Netz (gemessen; `PLAYTEST-0.1.4.txt:19`).
   Die Vanilla-Schweineknoten spielen damit ihre Baerenclips (Clips gelten je Netz, `tier_spez.md` 2.2). Unser Gegenstueck
   ist "Clips heissen `DeerStag_*`" -- dasselbe Prinzip, nur ohne Doppelnamen.
3. **Eigene Knoten in den Vanilla-Ordner** `42.21/media/AnimSets/pig/<zustand>/KW_*.xml`, jeder mit Bedingung
   `KWNativeWildlife = true` (`KW_attack.xml:11`, `KW_falldown.xml:20`, `KW_alert.xml:1`, `KW_scavenging.xml:7-8`,
   `KW_zombieattack.xml:7-8`). Diese Variable setzt `AnimationCompatibility.lua:13-22` je Tick auf JEDEM Rechner fuer jedes
   geladene KW-Tier. Echte Schweine haben sie nie und spielen weiter Vanilla. Das ist unser Plan aus `kampf_spez.md` 1.1-1.2
   (Ordner `buck/idle`, Variable `NCBearAct`), hier ausgeliefert und laut ihnen gespielt.

| Knoten | Zustand | Clip | Unterschied zu Vanilla |
|---|---|---|---|
| `KW_attack` | attack | FarmPig_Attack_Bite | `AttackConnect` bei 0,57 statt 0,95 (`media/AnimSets/pig/attack/attackDefault.xml:8`), `PlayBreedSound attack` bei 0,12 |
| `KW_falldown` | falldown | FarmPig_Death | Bewegungsknochen `Translation_Data`/Y statt `Bip01`/Z (`media/AnimSets/pig/falldown/falldown.xml:5-6`) |
| `KW_alert` | idle | **KW_Wildlife_Alert** (eigener Name) | bei `idleAction = idle3` |
| `KW_scavenging` | idle | FarmPig_IdleEating01 | bei `KWScavenging` (Kojote frisst Leiche) |
| `KW_zombieattack` | idle | FarmPig_Attack_Bite | bei `KWZombieAttack` -- Angriff auf Zombies OHNE Zustand attack |

**Modell und Clips:** DirectX `.x` als Text (`xof 0303txt 0032`), 4800 Ticks/s. Je Art ein Netz mit allen Clips eingebettet,
`animationsMesh { meshFile, keepMeshAnimations = true, animationDirectory, animationPrefix }` in `module Base`
(`KW_Models.txt:2-21`). Zusaetzlich liegen die 90 Clips getrennt unter `common/media/anims_X/KW_<Art>/`. Grund fuer das
Einbetten (Hotfix 0.1.4): nach spaeter Aktivierung der Mod ueber `Core.ResetLua` hatten die Tiere keine Animation
(`CHANGELOG-0.1.4.txt:3-7`, `PLAYTEST-0.1.4.txt:5-15`). **Das ist unabhaengig gemessen genau unser `tier_spez.md` 2.6.**
Weitere eigene Funde: verschachtelte Clip-Ordner liessen den Menschen-Lader die Clips nehmen, darum je Art ein Ordner
oberster Ebene (`PLAYTEST-0.1.2.txt:21-23`); die Hinterfussknochen mussten fuer den Leichen-Renderer umbenannt werden, sonst
Array-Ausnahme (`:26-28`, deckt sich mit `tier_spez.md` 2.4).

**Knochen (21 Knoten, alle Arten gleich):** `Bip01` (Wurzel, kein `Dummy01`), `Bip01_Pelvis/Spine/Chest/Neck/Head`,
`Bip01_L/R_ForeUpper/ForeLower/ForePaw`, `Bip01_Tail`, `Bip01_L/R_HindUpper/HindLower`, `Bip01_L/R_Foot`, `Translation_Data`,
`KW_Model` (Netz). **Keine `Bip01_L/R_Calf`.** `tier_spez.md` 2.4 nennt Calf als Pflicht (CombatManager); im Jar steht die
Calf-Pruefung in `CombatManager.attackCollisionCheck` (Offset 1388-1439) hinter Kopf (1306-1324) und Wirbelsaeule
(1347-1365), die vorher wegspringen koennen; `Model.boneToWorldCoords` prueft den Index nicht (Offset 0-38). Meine Lesung,
nicht ganz verfolgt: vermutlich wirft es nur, wenn Kopf und Wirbelsaeule verfehlen. KWs bestandene Waffentreffer
(`PLAYTEST-0.1.2.txt:12-14`) widerlegen 2.4 damit nicht. **Offen, vor dem Umbenennen pruefen.** Ragdoll-Warnungen "SkeletonBone not resolved" sind laut ihnen bei jedem
Tierknochen normal und harmlos (`README.txt:133-140`) -- bei uns ebenso erwarten, nicht jagen.

## (2) Angriff

| Gegen | Ausloeser | Schaden | Fundstelle |
|---|---|---|---|
| **Spieler** (nur erwachsene Baeren, 20 Kacheln, gleiche Ebene, `CanSee`, nicht im Auto, nicht unsichtbar/Geist/Gott) | Lua alle 0,5 s; `setWild(false)`, Provokation `a:hitConsequences(nil, ziel, true, 0, false)` + `setHitReaction(nil)`, dann alle 2 s `getBehavior():goAttack(ziel)` mit `animalRunning` | **Engine**: `goAttack` -> `fightAnimal` setzt `atkTarget` in `attackDist` -> Zustand `attack` -> `AnimalAttackState.animEvent` bei `AttackConnect`: `IsoPlayer.hitConsequences(null, tier, false, calcDamage, false)`, `calcDamage = baseDmg * Gen strength` | `Predators.lua:132-163`; Jar `BaseAnimalBehavior.goAttack` Offset 65-93, `fightAnimal` 87-159, `AnimalAttackState.animEvent` 420-626, `IsoAnimal.calcDamage` 0-27 |
| **Zombies** (Sandbox `AggressiveToZombies`, Vorgabe AUS; erwachsene Baeren, Kojote, Luchs, Keiler) | Lua alle 0,75 s naechster sichtbarer Zombie in 8 Kacheln; `pathToCharacter` mit `animalRunning`, im Kontakt `stopAllMovementNow`, `faceThisObject`, `setBlockMovement(true)`, Variable `KWZombieAttack` (Knoten in idle), `playBreedSound("attack")` | **eigener Lua**: bei Start + 713 ms Kontakt NEU pruefen, dann `z:hitConsequences(BareHands, tier, false, baseDmg*0.35, true)`, `getHitDir():set`, `setHitFromBehind(false)`, `setAttackedBy(tier)`, Reaktion `ShotBellyStep`; Ende 1250 ms, Pause 700 ms | `ZombieCombat.lua:4-10, 44-61, 102-153` |

* **Warum Zombies Lua brauchen:** `AnimalAttackState.animEvent` kennt bei `AttackConnect` nur Tier (`HitByAnimal`, Offset
  194-417), Spieler (420-626) und Tuer/Zaun (632-764). Ein Zombie als `atkTarget` bekommt nichts.
* Kontakt: gleiche Ebene (`|dz| < 0,2`), Abstand <= 1,25, `CanSee`, keine Wand/Tuer/Fenster dazwischen
  (`isBlockedTo`, `isWindowTo`, `isDoorBlockedTo`, `isWallTo`; `ZombieCombat.lua:18-24`).
* Treffermoment: 713 ms = 0,57 x 1,25 s (Baeren-Attack-Clip 6000 Ticks) -- fester Zeitgeber, nicht aus der Animation.
* Wirkung am Zombie: `IsoZombie.hitConsequences` ruft die Elternmethode (Offset 44), die laut `kampf_spez.md` 3.3 Nahkampf
  mit x0,15 rechnet. Grob 0,1 je Biss beim Braunbaeren (1,8 x 0,35 x 0,15). **Ungeprueft im Spiel.**
* Vorrang: Spieler schlaegt Zombie (`Predators.lua:135`, `ZombieCombat.lua:107-108`).

**Clips (90 = 6 Arten x 15):** Bewegung Walk, Run; Ruhe Idle01-03, SitIn, SitIdle, SitOut; Aufmerksam Alert; Fressen Eat;
Kampf Attack, Hit; Tod Death, Dead, OnHook. Baer (s): Attack 1,25, Hit 0,55, Walk 1,15, Run 0,65, Death 1,1, Alert 1,5,
Idle 2,7-3,2. Weg im Clip (Translation_Data): Braunbaer Walk 0,339 / Run 0,828 Einheiten, Schwarzbaer 0,367 / 0,880;
mit `MotionScale` 1,6 (`tier_spez.md` 2.8) rund 0,47 bzw. 2,0 Kacheln/s beim Braunbaeren.

## (3) Gegenwehr

* **Zombies verletzen KW-Baeren nicht.** Kein Code dafuer; die Engine loescht ein Tier als Zombieziel
  (`AttackState.triggerPlayerReaction` Offset 20-33, `angriff_zombie.md`). Die Mod beschreibt nichts anderes.
* **Spieler ja, ueber die Engine:** Waffentreffer -> `IsoAnimal.hitConsequences`: Leben minus
  `damage * getHealthLoss(0,025)` (Offset 0-32, nur ausserhalb eines MP-Clients), `getHealthLoss` = `healthLossMultiplier *
  (1,5 - Gen resistance) / 0,025` (`AnimalData.getHealthLoss` Offset 9-106; ohne Gen `resistance` nur
  `healthLossMultiplier`, Offset 31-36). KW macht Baeren zaeh nur ueber das kleine `healthLossMultiplier`.
* Gegenangriff: die Engine startet `goAttack` nur auf dem Server (`IsoAnimal.hitConsequences` Offset 187-227; Angreifer
  IsoPlayer ODER IsoZombie, `attackBack`). Im Einzelspieler baut KW das nach: `OnWeaponHitCharacter`, 250 ms warten, dann
  `goAttack` (`AnimationCompatibility.lua:23-37, 40-44`).
* Fuer uns interessant: die Engine sieht in `hitConsequences` den Zombie als Angreifer eines Tieres ausdruecklich vor
  (Offset 199-204). Lua-belegt ist `hitConsequences` aber nirgends (Vanilla grep 0), KW ist kein Beleg (CLAUDE.md 3).

## (4) Toene

* 20 Ereignisse, 30 WAV (PCM 16 bit, mono, 44,1 kHz, gemessen), unter `42.21/media/sound/KW/`. Skript `KW_Sounds.txt`,
  `module Base`, je Ereignis `category = Animals`, `is3D = true`, `loop = false`, `maxInstancesPerEmitter = 1`, mehrere
  `clip`-Bloecke mit `file =` (jede Datei zweimal, Tonhoehe 0,97 und 1,03; `KW_Sounds.txt:3-41`).
* Lautstaerke/Reichweite: `distanceMin 2`, `distanceMax` Idle 35, Stressed 50, Attack 45, Pain 55, Death 45; Volume 0,34 /
  0,65 / 0,78 / 0,72 / 0,67. "Positional volume falloff" ist nur das (`README.txt:72`).
* Abspielen: Rasse `sounds` mit `slot = "voice"`, `priority` (Idle 0, Stressed 10, Attack 30, Pain 50, Death 100) und
  `intervalMin/Max` fuer Idle/Stressed (`Sounds.lua:3-30`); Vanilla-Muster `PigDefinitions.lua:289-300`. Koerpergeraeusche
  aus dem Hirsch kopiert (`Definitions.lua:31-35`). Stimmen verwaltet `AnimalVocalsManager`, alle 500 ms, nicht auf dem
  Server (`update` Offset 0-21). Ausgeloest per Knoten-Ereignis `PlayBreedSound` (`KW_attack.xml:11`) bzw. `playBreedSound`
  (`ZombieCombat.lua:145`).
* Mehrere `clip`-Bloecke mit `file =` sind damit in einer Mod geladen (`PLAYTEST-0.1.3.txt:36-38`, 60 Bindungen) -- gehoert
  hat es dort niemand (`PLAYTEST-0.1.2.txt:36`). Fuer `kampf_spez.md` 4.1 ein Hinweis, kein Beleg.

## (5) Jungtiere, Groesse, Wachstum

* Stufen ueber die Engine: `young` mit `ageToGrow = Alter`, `nextStage = female`, `nextStageMale = male`
  (`Definitions.lua:19-23`); Erwachsene `minAge = Alter` (`:66`). Vermehrung an: `babyType`, Tragzeit 90, Pause 180,
  Paarungszeit 9-11 (`:67-68`).
* Groesse je Stufe als Faktor: Maennchen 1,0, Weibchen 0,90, Junges 0,46 (`:46`); `minSize/maxSize = 1,2/1,4 x Faktor`,
  `animalSize`, `collisionSize`, Gewicht mit Faktor^2 (`:54-56`). Junge = gleiches Modell kleiner (`README.txt:46`).
* Junge kaempfen nicht und fliehen (`fleeZombies`, kein `attackBack`, `Predators.lua:10` `isBaby`).
* Kein `setSizeForced`; Wachstum ist der native Stufenwechsel. Wie die Groesse zwischen den Stufen gleitet: **ungeprueft**.

## (6) Spawn

* Eigene `MigrationGroupDefinitions["kw<Art>"]` als Kopie von `deer` mit eigenen Tieren, Rasse `wild`, Anzahl, `maxMale=1`,
  `babyChance=8`, Tempo, Spurgroesse (`Definitions.lua:90-94`), eingehaengt in die Vanilla-Sammelgruppen `large`/`small`
  mit Gewicht (`:95`; Vanilla `MigrationGroupDefinitions.lua:59-73`: `large` = deer 100, `small` = rabbit 100). Baeren:
  Schwarz 7, Braun 3 -- grob 6 % aller grossen Gruppen.
* Sandbox-Schalter je Art entfernt nur den Gruppeneintrag, die Definition bleibt (sonst laden alte Tiere nicht); neu gesetzt
  vor dem Zwischenspeicher des Populationsmanagers, plus `OnInitGlobalModData`/`OnLoadMapZones` (`Settings.lua:19-31`).
* Eigene Angaben: kein Nachwachsen, alte Gebiete werden nicht neu besiedelt (`README.txt:122-126`).

## (7) Mehrspieler

* Entscheidungen nur ausserhalb eines Clients (SP und Server): Zielwahl, Fressen, Zombieschaden
  (`Predators.lua:115-120`, `ZombieCombat.lua:79-86`). Spieler-Liste: Server `getOnlinePlayers`, sonst
  `getSpecificPlayer` (`Predators.lua:12-20`).
* Clients bekommen nur das Bild: `sendServerCommand` mit Variable und Verfall (1,5 s Angriff, 2,5 s Fressen) und beim Zombie
  die Gesundheit als `setHealth(min(alt, neu))` + Reaktion + `reportEvent("wasHit")` (`ZombieCombat.lua:29-31, 58-60,
  163-192`; `Predators.lua:41-44, 196-207`). Kein Client-Befehl nimmt Schaden an (`ZombieCombat.lua:162`).
* Speichern: `OnSave` beendet alle Kaempfe, `wild` wird ueber ModData nach Entladen wiederhergestellt
  (`ZombieCombat.lua:89-97, 156-160`; `Predators.lua:129-131, 191-195`).
* **Selbst nicht im MP gespielt** (`README.txt:119-121`, `PLAYTEST-0.1.6.txt:8`). Offene Frage aus CLAUDE.md 5: der
  dedizierte Server rechnet keinen Zombie, Leben kommt vom Client mit Hoheit -- ihr `min`-Rundruf haelt das bei, ob ein Tod
  auf dem Server sauber bei allen ankommt: **ungeprueft**.

## (8) Was wir davon brauchen koennen (Idee, Herkunft)

| Idee | Herkunft | Bei uns |
|---|---|---|
| Eigene Knoten in Vanilla-AnimSet-Ordner, Bedingung eigene Variable | KW `AnimSets/pig/*` | **bestaetigt** unseren Plan `kampf_spez.md` 1; bleibt `buck/idle` |
| Variable auf JEDEM Rechner setzen (Anim-Variablen sind lokal) | `AnimationCompatibility.lua:13-22` | fuer B9 (MP) einplanen |
| Clips ins Netz einbetten, `keepMeshAnimations` | `CHANGELOG-0.1.4.txt` | bestaetigt `tier_spez.md` 2.6, so bauen wir schon |
| Kontakt im Treffermoment NOCHMAL pruefen (Abstand, Ebene, Sicht, Wand) | `ZombieCombat.lua:130-133, 18-24` | in unseren Treffer uebernehmen (eigener Code); Wandfragen sind Vanilla-belegt (`isBlockedTo` 9, `isWallTo` 7, `isDoorBlockedTo` 5, `isWindowTo` 4 Treffer) |
| Server entscheidet, Client bekommt Variable + Gesundheit mit Verfall | `ZombieCombat.lua:163-192` | Muster fuer B9 |
| Zustand vor `OnSave` loesen, Marke im ModData fuer Wiederaufnahme | `ZombieCombat.lua:89-97, 156-160` | Kampfzustand nie gespeichert halten |
| Kurzer eigener Hit-Clip statt 6-s-Reaktion | Gruppe `pig`: `media/AnimSets/pig/hitreaction/hitreaction1.xml:4` spielt `FarmPig_HitReaction` (bei KW 0,55 s) | bei `buck` ist die Reaktion `DeerStag_Idle01` (`tier_spez.md` 3.3); fuer Gegenwehr pruefen |
| Ton-Varianten: gleiche Datei mit Tonhoehe 0,97/1,03, `maxInstancesPerEmitter 1`, Prioritaet im Slot `voice` | `KW_Sounds.txt`, `Sounds.lua` | Vanilla-Muster `PigDefinitions.lua:289-300` reicht als Beleg |
| Natives Stufensystem young -> adult | `Definitions.lua:19-23, 46` | Alternative zu `setSizeForced`; Kevin hat drei Stufen mit festen Groessen gewaehlt, Zwischengroesse ungeprueft |
| Eigene Migrationsgruppe in `large` | `Definitions.lua:90-95` | fuer Weg A (verwaistes Junges) ungeeignet: Gruppen mit Erwachsenen, kein Neubesiedeln; `addAnimal` bleibt besser |

**Was bei uns anders sein muss:**
* KW-Baeren JAGEN Spieler; unser Baer darf nie Spieler verletzen. Mit `pig` traefe `AttackConnect` jeden Spieler als
  `atkTarget` -- deshalb bleibt `buck` ohne Zustand `attack` richtig (`tier_spez.md` 3.2 A).
* KW-Zombieangriff nimmt jeden `IsoZombie` (`ZombieCombat.lua:65-75`) -- also auch Banditen und NPC-Crew-Figuren. Wir
  filtern nach `kampf_spez.md` 3.4.
* Schaden ueber `z:hitConsequences` und Laufen ueber `animal:pathToCharacter` sind in Vanilla-Lua nicht belegt (grep 0); wir
  bleiben bei `setHealth`/`knockDown`/`Kill` und `fleeTo` (`kampf_spez.md` Abschnitt 0, Punkte 5-7). Auch `CanSee`,
  `setHitReaction`, `getHitDir` haben in Vanilla 0 Treffer.
* Fester 713-ms-Zeitgeber statt Animationsereignis: wir nehmen `SetVariable NCBearHit` bei `m_TimePc` (`kampf_spez.md`
  Abschnitt 0, Punkt 3), das bleibt bei Tempoaenderung richtig.
* KW `wild = true` mit `setWild`-Umschalten; unser Baer ist `wild = false`.
* Zombies sollen unseren Baeren verletzen -- das hat KW nicht. Bleibt Weg 1/2 aus `angriff_zombie.md`.

## (9) Vertraeglichkeit mit unserem Baeren

| Bereich | Knox Wildlife | Wir (heute / spaeter) | Kollision |
|---|---|---|---|
| Art, Gruppe, Rasse | `kw<Art>Male/Female/Young`, `kw<Art>`, `wild` | `bear`, `bearstag` / `ncbear`; Gruppe `bear`; Rasse `brown` | keine |
| Texte | `IGUI_AnimalType_kw*`, `IGUI_Animal_Group_kw*`, `IGUI_Breed_wild` | `IGUI_AnimalType_bear*`, `IGUI_Breed_brown` | keine |
| Teile-Schluessel | `kw<Art><Stufe>wild` | `bearbrown` | keine |
| Modell-Skripte (`module Base`) | `KW_<Art>`, `KW_Carry_<Art>_<n>` | `NCBear`, `NCBear_Body`, `NCBearStag_Body` | keine |
| Clipnamen | `KW_*`, Aliase `FarmPig_*`, `KW_Wildlife_Alert` | `DeerStag_*` im eigenen Netz | keine (je Netz, `tier_spez.md` 2.2) |
| AnimSet-Dateien | `AnimSets/pig/{attack,falldown,idle}/KW_*.xml` | `AnimSets/buck/idle/NCBear*` (geplant) | keine; andere Gruppe |
| Anim-Variablen | `KWNativeWildlife`, `KWScavenging`, `KWZombieAttack` | `NCBearAct`, `NCBearHit`, `NCBearDone` | keine |
| Tonnamen / Pfade | `KW_<Art>_<Ereignis>`, `media/sound/KW/*.wav` | `NCBearRoar1/2`, `NCBearGrowl1/2`, `media/sound/ncbear_*.wav` | keine |
| Texturen | `textures/Body/KW/*.png`, `textures/KW/*`, `Item_KW_*` | `textures/Body/NCBear.png` | keine |
| Lua-Globale | `KnoxWildlife` | `NCBear*`, spaeter `BanditsNPC.Bear` | keine |
| Vanilla-Aufsaetze | `ButcheringUtil.createAnimalForHook/updateCorpseDatas` (reicht fremde Arten durch, `Carcasses.lua:7-36`), Kontextmenue-Vorfilter nur fuer KW-Leichen (`CarcassPicking.lua:78-92`) | keine | keine |
| Migration | haengt sich an `large`/`small` | unser Baer nicht in Migration | keine |

**Nebenwirkungen, die NPC Crew betreffen (nicht den Baeren):**
* Mit `AggressiveToZombies` (Vorgabe aus) beissen KW-Tiere Banditen und Crew-Figuren (`ZombieCombat.lua:65-75, 56`).
* `CoyotesEatCorpses` ist **Vorgabe AN** und loescht Leichen mit `isZombie()` samt Inhalt (`Predators.lua:69-89`). Laut
  CLAUDE.md (neunte Ausnahme) ist `isZombie()` auch fuer Banditen- und Crew-Leichen wahr: Kojoten koennen also Leichen
  fressen, die Leichen entsorgen oder das Pluendern gerade nutzen will, mit allem Inhalt. **Ungeprueft im Spiel.**
* KW fragt je Tick `getModData()` jedes geladenen Tiers (`ZombieCombat.lua:90-97`), auch unseres Baeren; liest nur eigene
  Schluessel. Harmlos.

Statisch gelesen, nicht gespielt.
