# Eigenes Tier "bear" in B42.21 ohne fremde Dateien

Stand 07.11.2026, PZ 42.21 (`projectzomboid.jar` vom 28.09.2026). Gelesen in Vanilla und Jar. Offline-Probe mit dem
spieleigenen `jassimp64.dll` und `ProcessedAiScene` (Abschnitt 2.3). **Nicht gespielt.**

Fundstellen: `Klasse.methode Offset` = `javap -c -p`. `Datei.lua:Zeile` = Vanilla unter `media/lua`. Lesehilfe (Vineflower,
nur zum Lesen): `.../_arbeit/baer_spiel/dec/`.

---

## 0. Ergebnis in zehn Saetzen

1. **Ein eigenes Tier geht ohne fremde Datei.** Lua-Definition unter `media/lua/shared/`, Skripte, Netz, Textur.
2. **Ein eigener Name in `animset` geht NICHT.** `animset` waehlt AnimSet UND ActionGroup, und ActionGroups liest die Engine
   nur aus dem Spielordner (2.5/3.1). `animset = "bear"` ergibt eine leere Zustandsmaschine.
3. **Der Ausweg kostet nichts:** `animset = "buck"`. Clips sucht die Engine je Netz (`skinningData.animationClips`), also darf
   das Baerennetz eigene Clips mit den Namen `DeerStag_*` tragen. Rehe bleiben unberuehrt.
4. **Format: `.glb`, EINE Datei mit Netz und allen Clips, `keepMeshAnimations = true`.** Vanilla macht es so bei allen
   Tueren (ebenfalls aus Blender). FBX scheidet aus: in der Probe verzerrt.
5. **Getrennte Clip-Dateien gehen hier nicht:** `.glb`-Clips laedt die Engine mit Faktor 0,01 und Drehung, das Netz ohne;
   jede Clip-Datei braucht zudem ein gehaeutetes Netz; und bei Kevins Ablauf (Mod nur im Spielstand) werden Clip-Ordner
   eines Mod-Netzes gar nicht geladen (2.6).
6. **Knochennamen sind Pflicht, keine Kosmetik.** `Bip01_Head`, `Bip01_Spine`, `Bip01_L/R_Calf`, `Bip01_L/R_Foot` werden ohne
   Pruefung als Index benutzt; fehlt einer, wirft `modelTransforms[-1]`. Die deutschen Namen aus `baer_c.py` muessen umbenannt
   werden (Tabelle 2.4).
7. **Ohne Weg in `Translation_Data` laeuft das Tier auf der Stelle.** Die Geschwindigkeit kommt nur aus dem Clip.
8. **Das Tier erscheint nie von selbst:** Migration, Ranch und Stories nennen feste Arten. Spawn ueber das Debug-Menue
   (taucht von allein auf) oder `addAnimal`.
9. **`wild = false`, `fleeZombies = false` plus `animset = "buck"` ist friedlich und kann gar nicht angreifen:** Schaden
   entsteht nur im Zustand `attack`, und die Gruppe `buck` hat keinen.
10. **Sicherster Einstieg:** das Baerennetz auf das Rehskelett haengen (`animationsMesh = Deer_Stag`), dann laufen sofort alle
    17 Rehclips (Rueckfall 6.5). Eigene Clips danach.

---

## 1. Definitionen

### 1.1 Wann gelesen, wo die Datei hin muss

- Java liest die Lua-Tabelle `AnimalDefinitions` lazy: `AnimalDefinitions.loadAnimalDefinitions` Offset 27 (`LuaManager.env`),
  erster Aufruf `IsoWorld.init` Offset 2672. In `console.txt` steht `loadAnimalDefinitions start` nach
  `triggerEvent OnLoadedTileDefinitions`. Alle Lua-Dateien sind da schon geladen.
- `LuaManager.LoadDirBase`: Vanilla zuerst, dann Mod fuer Mod. Also darf die Mod-Datei auf Vanilla-Tabellen zugreifen.
  `AnimalAvatarDefinition = {};` (AnimalAvatarDefinition.lua:1) wuerde eine fruehere Datei wegwischen, das trifft uns dadurch nicht.
- **Ort: `42/media/lua/shared/`** (Einzelspieler, Client, Server). Der Server braucht die Definition.
- `AnimalDefinitions.Reset` beim Lua-Neuladen, danach neu gelesen.

### 1.2 Felder von `AnimalDefinitions.animals["bear"]`

Quelle: `AnimalDefinitions.loadAnimalDefinitions`. Alles andere als "Pflicht" hat eine Vorgabe aus dem Konstruktor.

| Feld | Status | Was bei fehlt passiert (Fundstelle) |
|---|---|---|
| `bodyModel` | **Pflicht** | `getLoadedModel(null)` in der Schleife ueber ALLE Tiere (Offset 2665). Ein kaputter Eintrag gefaehrdet alle Tierarten. Name muss ein `model`-Skript in `module Base` sein (2.7). |
| `animset` | **Pflicht** | `ActionGroup.getActionGroup(null)` -> `toLowerCase` NPE (`IsoAnimal.initType` Offset 33-36). |
| `stages` mit Eintrag gleich dem Tiernamen | **Pflicht** | `currentStage` null -> NPE in `AnimalData.initSize` Offset 25. |
| `stages[..].ageToGrow` >= 1 | **Pflicht** | Teilung durch 0 in `initSize`, `initWeight`, `growUp`; bei `minSize == maxSize` wird die Groesse NaN. |
| `breeds` | **Pflicht** | `getBreeds` leer; das Debug-Menue bietet nichts an. |
| `breed.texture` und `breed.textureMale` | **Pflicht** | Weiblich: `texture.get` NPE; maennlich: Textur `null.png` (`IsoAnimal.initTexture`). Beide auf denselben Namen. |
| `minSize`, `maxSize` | **Pflicht** | Vorgabe 0 -> `setSize` klemmt auf 0 -> unsichtbar. |
| `group` | **Pflicht** | DebugContextMenu.lua:253 `animals[def:getGroup()]` -> "table index is nil": ganzes Debug-Tiermenue tot. |
| `genes` mit `meatRatio` | **Pflicht fuer den Tod** | ButcheringUtil.lua:40 `getUsedGene("meatRatio"):getCurrentValue()` wirft. |
| `collisionSize`, `shadoww/fm/bm` | dringend | Vorgabe 0: Kollision 0 (`IsoAnimal.updateInternal`), kein Schatten (`renderShadow`). |
| `animalSize` | dringend | Halteschwelle in `PathFindBehavior2.update(float)` Offset 1125. Reh 0,3. |
| `canThump` | setzen `false` | Vorgabe true. |
| `canBePicked` | setzen `false` | Vorgabe true; Gewichtsgrenze 40 + Staerke*7. |
| `minWeight`, `maxWeight` | setzen | Vorgabe 10/100. `maxWeight` > Anfangsgewicht, sonst Teilung durch 0 in `getBloodQuantity`. |
| `corpseSize`, `minBlood`, `maxBlood`, `wildFleeTimeUntilDeadTimer` | setzen | Letzteres nur bei wild: 0 heisst toedlich beim ersten Treffer (`hitConsequences`). |
| `modelscript`, `carcassItem` | ohne Wirkung | Java liest `modelscript` gar nicht; `carcassItem` wird nur gespeichert (Jar-Suche: nur `AnimalDefinitions`). |

Ohne Wirkung sicher weglassbar (null-sicher geprueft): `mate` (`findFemaleToInseminate`), `eatTypeTrough` (`canEatThis`-Aufrufer,
`eatAndDrinkAfterMeta`), `bodyModelSkel*` und `textureSkeleton` (`canBeSkeleton`, `AnimalVisual.getModel`), `bodyModelHeadless`,
`textureSkinned`, `babyType`, `maxAgeGeriatric` (`isGeriatric`, `checkOld`), `hungerMultiplier`/`thirstMultiplier` (0 = kein Hunger).

**`genes` ohne `maxSize` lassen:** dann ist `getUsedGene("maxSize")` null und `getMinSize` = `adef.minSize` exakt, und die
Erbkrankheit `dwarf` greift nicht. `initSize` setzt am Ende `setSize(0.1)`, das klemmt auf `getMinSize` (`AnimalData.initSize`).
Mit `minSize = maxSize = 1.0` ist die Groesse also fest 1,0.

### 1.3 Weitere Tabellen

| Tabelle | Noetig? | Grund |
|---|---|---|
| `AnimalDefinitions.stages/breeds/genome` | frei | Nur Hilfstabellen fuer das Einsetzen; Java liest `animals[..].stages/breeds/genes`. |
| `AnimalAvatarDefinition["bear"]` | **ja** | ISAnimalUI.lua:622, :31, :367: `self.avatarDefinition.zoom` wirft beim Fenster "Tier-Info". Felder von `buck` kopieren, `hook` weglassen. |
| `AnimalPartsDefinitions.animals["bear<breed>"]` | **ja** | ButcheringUtil.lua:18+:27: `def.feather` auf nil beim Tod (wird gefangen, aber Leichendaten fehlen). Attrappe: `= AnimalPartsDefinitions.animals["buckwhitetailed"]` (AnimalPartsDefinitions.lua:445-454). |
| `AnimalGenomeDefinitions` | nein | Vorhandene Gene benutzen. |
| `AnimalTracksDefinitions`, `MigrationGroupDefinitions`, `RanchZoneDefinitions` | **absichtlich nein** | Siehe 1.4. |

Texte (optional, sonst steht der Schluessel da): `42/media/lua/shared/Translate/EN/IG_UI.json` mit `IGUI_AnimalType_bear`,
`IGUI_Breed_<breed>`, `IGUI_Animal_Group_bear` (Vanilla: EN/IG_UI.json:1907, :1886, :4770).

### 1.4 Das Tier erscheint nie von selbst

- Wandergruppen: nur `MigrationGroupDefinitions` (AnimalPopulationManager, VirtualAnimal). Kein Eintrag = kein Spawn.
- Hoefe: `RandomizedRanchBase` nur aus `RanchZoneDefinitions`.
- Stories mit festen Listen: `RZSAttachedAnimal` und `RVSAnimalTrailerOnRoad` (javap: nur angus, simmental, ... und bull, cow, ram, ...).
- Tierzucht: nur mit `mate`/`babyType`. Beides weglassen.

---

## 2. Netz und Clips

### 2.1 Was das Spiel lesen kann

`FileTask_AbstractLoadModel.checkExtensionType`: Pfad ohne Endung sucht `.fbx`, dann `.glb`, dann `.x`, dann `.txt`; Pfad mit `.` wird
direkt genommen. Alle vier gehen durch Assimp.

| Format | Lader-Einstellung | Vanilla-Beleg | Urteil |
|---|---|---|---|
| `.x` | Netz und Clip ohne Aenderung | alle Tiere, Kopfbytes `xof 0303txt 0032` | Geht, aber Blender 5.2 hat keinen Exporter (eigener Schreiber noetig). Reserve. |
| `.glb` | Netz: Massstab 1, keine Drehung (`FileTask_LoadMesh.loadGLTF` Offset 187-188). **Clip-Datei: Massstab 0,01 + Drehung** (`FileTask_LoadAnimation.loadGLTF` Offset 142) | `IsoObject/*.glb`: 57 Dateien, alle Generator "Khronos glTF Blender I/O", 53 mit Skin und Clips (nachgezaehlt) | **Nehmen, nur mit eingebetteten Clips.** |
| `.fbx` | Netz und Clip: 0,01 + -90 Grad X (`loadFBX`) | Kein gehaeutetes FBX in Benutzung (`door1.fbx` hat Knochen, kein Skript nennt es als Netz) | In der Probe verzerrt, siehe 2.3. **Nicht nehmen.** |

`validatePrefix`: "Invalid prefix" (Bandits' `.X`) stand zuletzt im Log vom 25.09., seit 42.21 null Treffer; `Zomboid\mods` ist erlaubt
(`getAllModFolders`), das Turret-FBX ist dort im Spiel geladen worden.

### 2.2 Woher der Clipname kommt

**Nicht aus dem Dateinamen.** `ImportedSkeleton.processAnimation`: `srcAnim.getName()`, Teil nach `|`, getrimmt. In `.x` der Name des
`AnimationSet`, in `.glb` der Name der Blender-Aktion. `animationPrefix` filtert nur, welche Dateien eines Ordners fuer welches Netz
geladen werden (`ModelManager.checkAnimationMeshPrefixes`).

Clips gelten **je Netz**: `AnimationPlayer.play` Offset 101 `skinningData.animationClips.get(name)`. Darum duerfen zwei Tiere denselben
Clipnamen haben. Fehlt ein Clip: nur eine Warnung, die Figur bleibt in der letzten Pose.

**Eine reine Clip-Datei ohne Netz geht nie:** `ProcessedAiScene.processAiScene` verlangt ein Netz mit Knochen, sonst `skeleton = null` und
`applyToAnimation` wirft. Deshalb sind Vanillas Clip-Dateien so gross wie das Netz (`cmp`: `DeerStag.x` = `DeerStag_Walk.x`).

### 2.3 Messung mit dem Importer des Spiels

Harness `.../_arbeit/baer_spiel/harness/Probe.java`, ruft `Jassimp.importFile` mit denselben Schritten wie `FileTask_LoadMesh` und dann
`ProcessedAiScene.process` mit den Parametern des Laders. Das Spiel lief nicht. Testmodell (Blender 5.2.3): `probe/mini*.py`.

| Datei | Wurzel | Knochen | Clips | Kopf (Modellraum) | Gehaeutet | Weg am Clipende (x,-z) |
|---|---|---|---|---|---|---|
| `DeerStag.x` (Kontrolle) | `$dummy_root` | 40 | DeerStag_Walk | 0,015 / 0,708 / -0,615 | -0,15..0,18 / -0,02..1,04 / -0,82..0,44 | 0 / 0,9055 |
| `mini3.glb` | `Rig` | 5 | DeerStag_Idle01, DeerStag_Walk | 0 / 0,650 / -0,500 | **gleich der Ruhehaltung** | 0 / 0,9000 |
| `door_n_sw.glb` (Vanilla) | `Dummy01` | 3 | Close, Open | | passt | |
| `mini.fbx` (Einstellungen vom Turret) | `RootNode` | 5 | DeerStag_Idle01, DeerStag_Walk | 0 / 0,006 / -0,005 | **verzerrt**, Knochen 100-mal zu klein | 0 / **0** |

Daraus, belegt: Blender-Front (-Y) wird Modell -Z wie beim Reh, Blender-Hoehe (Z) wird Modell Y. UV kommt in `.glb` gleich an wie in FBX
(u 0,25 / v 0,10 in beiden), also wie beim Turret. FBX wird nicht weiter verfolgt.

### 2.4 Skelett

**Baumstruktur frei, Namen nicht.** Bleibt ein Name weg, wirft die Engine, weil sie -1 als Index benutzt:

| Name | Wofuer | Fundstelle | Ohne ihn |
|---|---|---|---|
| `Dummy01` | Wurzel, Index 0 | `ImportedSkeleton.processAiScene` Offset 48 | Ohne: "Fahrzeug"-Zweig, geht auch (Vanilla-Tueren), aber ohne Index-Gleichheit zum Reh |
| `Bip01` | Index 1 (`SkeletonBone.Bip01`), `setCounterRotationBone` (`IsoAnimal.onAnimPlayerCreated` Offset 23), Bewegungsknochen im Sturz | | Sturz falsch |
| `Translation_Data` | Standard-Bewegungsknochen (`AnimNode.deferredBoneName`) | `AnimationPlayer.play` Offset 89 | Fehlerzeile, **Tier laeuft nicht** |
| `Bip01_Head`, `Bip01_L_Foot`, `Bip01_R_Foot` | `IsoGameCharacter.calculateShadowParams`: `boneToWorldCoords(.., getSkinningBoneIndex(x, -1), ..)` | Index -1 auf `modelTransforms` | Ausnahme |
| `Bip01_Spine`, `Bip01_L_Calf`, `Bip01_R_Calf` (+ Head, Feet) | `CombatManager` Offset 1306-1511, `DoSwingCollisionBoneCheck` | wie oben, beim Treffer | Ausnahme beim Schlag |
| `Bip01_Pelvis` | `getNearestTargetPosAndDot` (faengt -1 ab) | | Zielen ungenau |
| `Bip01_Neck` | `IsoAnimal.drawRope` am Baum | | nur mit Seil |

Schnittmenge aller Knochen von Reh, Kuh, Waschbaer, Huhn, Ratte, Maus, Schwein, Lamm, Hase (gemessen): Dummy01, Translation_Data, Bip01, Pelvis,
Spine, Neck, Head, Tail, je L/R: Clavicle, UpperArm, Forearm, Hand, Thigh, Calf, Foot, Toe0. **Diese Liste ist die Vorgabe.**

Weitere harte Grenze: `uniform mat4 MatrixPalette[60]` (`animalEffect.vert`:16). Hoechstens 60 Knochen. Der Baer hat rund 30.

**Umbenennung (baer_c.py -> Spiel):** wurzel=Bip01_Pelvis, ruecken=Bip01_Spine, brust=Bip01_Spine1, hals=Bip01_Neck, kopf=Bip01_Head,
kiefer=Bip01_Jaw, kiefer_1..7 duerfen bleiben, schwanz=Bip01_Tail, oberarmX=Bip01_X_UpperArm, unterarmX=Bip01_X_Forearm, prankeX=Bip01_X_Hand,
schenkelX=Bip01_X_Thigh, wadeX=Bip01_X_Calf, fussX=Bip01_X_Foot. Dazu neu Dummy01, Bip01, Translation_Data; Clavicle und Toe0 als Knochen ohne Gewichte.

**Aufbau, in der Probe bestaetigt (`mini3.py`), ergibt dieselben lokalen Achsen wie das Reh** (`Bip01` lokal 0 / -0,2 / 0,5 gegen Reh 0 / -0,14 / 0,57):

- Armature-OBJEKT heisst NICHT Dummy01 (hier `Rig`), Netz als Kind, sonst nichts in der Szene exportieren (Hilfs-Empties und IK-Ziele nicht).
- Knochen `Dummy01`: Kopf (0,0,0), Spitze (0,-0.1,0), **Roll 180 Grad**, kein Elternteil.
- Knochen `Bip01`: Kind von Dummy01. Alle anderen darunter.
- Knochen `Translation_Data`: **kein Elternteil**, Kopf (0,0,0), Spitze (0,0,0.1), Roll 0, keine Gewichte, keine Kinder. (Die Engine zieht den Weg von diesem Knochen ab, `updateBoneAnimationTransform`; haengt das Netz daran, wandert es.)
- Tier schaut in Blender nach **-Y** (Kopf von +X auf -Y: -90 Grad um Z drehen und anwenden), Fuesse auf Z = 0, Objekte ohne Rest-Skalierung.
- **Genau ein Netz, ein Material.** `ProcessedAiScene.findMesh` nimmt das erste Netz mit Knochen, ein zweites Material waere ein zweites Assimp-Netz und fehlt dann.

Jeder Knochen braucht in jedem Clip Schluessel: ohne Schluessel steht er auf Identitaet, nicht in der Ruhehaltung (`AnimationTrack$KeyframeSpan.lerp`).
Blender schreibt je Knochen T/R/S (gemessen, auch bei konstanten Werten). Einstellungen, in der Probe so gelaufen:
`bpy.ops.export_scene.gltf(export_format="GLB", export_yup=True, export_skins=True, export_animations=True, export_animation_mode="ACTIONS", export_anim_slide_to_zero=True, export_apply=False, export_morph=False)`,
dazu `use_selection=True` und Aktionen mit `use_fake_user`. Ohne `slide_to_zero` beginnt der Clip bei 1/30 s.

### 2.5 Massstab

- Modellraum: Bob 0,98 hoch (Arme +-0,49), Reh 1,05 hoch mit Geweih, 1,11 lang, Kopf bei -Z (`xgeo.py`).
- Endgroesse im Bild: `FinalScale` = `AnimalData.getSize()` (`ModelSlotRenderData`, Offset 452-455; `Model` `effect.setScale`; `animalEffect.vert`:57). Reh beginnt bei rund 0,77 (`minSize` 0,85 mal Gen) und waechst bis rund 1,08.
- `scale =` im Modellskript nicht benutzen: `ModelInstance` Offset 23 uebernimmt den Wert, fuer den Tierkoerper ist die Wirkung **ungeprueft**. Massstab gehoert in die Datei.
- Baer aus `baer_c.py`: rund 2,64 Blender-Einheiten lang, Schulter um 0,84. Mit Bob als Mensch ist **Faktor 0,5** der Startwert: 1,32 lang, Schulter 0,42 ohne Fell. Beim Export anwenden, `minSize = maxSize = 1.0`.
- **Nachstellen ohne Neustart:** `animal:getData():setSizeForced(x)` (ButcheringUtil.lua:569). Das Bild folgt, der Weg nicht (die Bewegung kennt die Groesse nicht).
- Textur: `media/textures/Body/<name>.png` fest (`ModelInstanceTextureCreator.init(AnimalVisual,..)`, nach Offset 84). Vanilla 256x256. Die Ergebnisgroesse kommt aus den Eingangstexturen (`TextureCombiner.getResultingWidth`); ein Deckel ist nicht gesehen, bei 2048 **ungeprueft**.

### 2.6 Laden: warum Clips in die eine Datei gehoeren

Kevins Mods stehen nur im Spielstand: `NCTurretTest` steht nicht in `mods\default.txt`, `console.txt` laedt es erst beim zweiten `loadMods` (Zeile 8359).
Der Weg ist dann `Core.ResetLua`: `initAnimationMeshes(true)` Offset 261 (startet das Laden, wartet NICHT), direkt danach `loadModAnimations` Offset 267.
Dort steht `if (am2.modelMesh.isReady())` (Offset 268). Das frische Mod-Netz ist noch nicht fertig, also werden die Clip-Ordner dieses Netzes uebersprungen,
und `modAnimations` merkt sich die Mod als erledigt. **Clip-Dateien in `anims_X` eines eigenen Netzes kaemen nie an**, ausser die Mod steht beim Spielstart in der Liste.

Eingebettet trifft das nicht: `ProcessedAiScene.applyToMesh` legt die Clips in die Skinning-Daten, `ModelMesh.onLoadedX` kopiert sie zurueck, und
`setActiveAnimations` behaelt sie bei `keepMeshAnimations` (Offset 62). `models_isoobject_animationsMesh.txt` (Vanilla) macht genau das: `meshFile` plus `keepMeshAnimations = true`, ohne Ordner.

### 2.7 Skripte

`ScriptBucketCollection.getScript`: Name ohne Punkt sucht NUR in `module Base`. Java fragt `getAnimationsMesh(name)` und `getModelScript(name)` mit dem nackten Namen.
**Also `module Base { ... }`**, nicht `module NCBear` wie beim Turret (dort loest das Item den Namen auf).

```
module Base
{
    animationsMesh NCBear
    {
        meshFile = Skinned/NCBear.glb,
        keepMeshAnimations = true,
    }

    model NCBear_Body
    {
        mesh = Skinned/NCBear.glb,
        shader = animalEffect,
        static = false,
        animationsMesh = NCBear,
    }
}
```

Muster: Vanilla `models_animals.txt`:248-254, `models_isoobject_animationsMesh.txt`:3-6.

### 2.8 Geschwindigkeit

`PathFindBehavior2.update`: `speed` = Laenge der Clip-Bewegung des Bildes, `if (speed <= 0) ... return Working`. **Kein Weg im Clip = Gehanimation auf der Stelle.**
Die Bewegung liest `Translation_Data` lokal als `(x, -z)` (`AnimationTrack.getDeferredMovement`), Faktor `MotionScale` 1,6 (`AnimSets/Defaults.xml`, `AdvancedAnimator.LoadDefaults`; die 0,76 im Code ist nur die Vorgabe).

| Clip | Dauer s | Weg | Einheiten/s | Kacheln/s |
|---|---|---|---|---|
| DeerStag_Walk | 1,067 | 0,906 | 0,849 | 1,36 |
| DeerStag_Run | 0,667 | 2,244 | 3,366 | 5,39 |
| Cow_Walk | 1,2 | 1,063 | 0,886 | 1,42 |
| Cow_Run | 0,533 | 1,772 | 3,322 | 5,32 |
| Bob_Walk | 0,667 | 0,945 | 1,417 | 2,27 |

Blender: `Translation_Data.location = (0, 0, +weg)` je Bild linear ergibt in der Datei z = -weg (gemessen, Knochen wie 2.4). In `baer_c.py` liegt der Weg auf `ao.location`: beim Backen dort auf 0 stellen und auf `Translation_Data` legen. IK und Copy Rotation (`baer_c.py`:1855-1860) gehoeren in Knochen-Schluessel gebacken.
Gang: `T` = 37,5 Bilder je Zyklus (Zeile 1863), also **zwei Zyklen = Bild 1..76 = 75 Abschnitte** als Schleife nehmen. Fussgleiten vermeiden: Weg je Zyklus = 0,95 m/s * 1,25 s * Faktor 0,5 = 0,594, also 0,475 Einheiten/s = 0,76 Kacheln/s. Schneller nur mit kuerzerem Zyklus (in `buck` ist `m_SpeedScale` fest).

---

## 3. AnimSet

### 3.1 Warum kein eigener Name

- `IsoAnimal.init` Offset 28: `AnimationSet.GetAnimationSet(adef.animset)`. Das liest Mod-Ordner mit (`AnimationSet.Load` Offset 36 `resolveAllDirectories`), Bandits und NPC Crew nutzen das.
- `IsoAnimal.initType` Offset 33-36: `ActionGroup.getActionGroup(adef.animset)`. **`ActionGroup.load` Offset 30 und 62 benutzt `getMediaFile`, und das ist `new File(workdir, ..)`: nur der Spielordner.** Bandits' `media/actiongroups` enthaelt nur `empty_folder.txt`.
- Mit `animset = "bear"`: Gruppe ohne Zustaende, `ActionContext.setGroup` Offset 7 setzt null, `getCurrentStateName` Offset 24 wirft NPE, und ohne Zustand gibt es keine Animation.
- Beides haengt am selben Feld. Vanilla teilt es selbst: `bull.animset = "cow"` (CowDefinitions.lua:253).

### 3.2 Die drei Wege

| Weg | Dateien | Vorteil | Nachteil |
|---|---|---|---|
| **A: `animset = "buck"`, Clips heissen `DeerStag_*`** | keine | Alle Knoten, Sounds, Uebergaenge fertig; kein Angriff moeglich | `m_SpeedScale` fest |
| B: `animset = "deerdead"` + eigener Ordner `media/AnimSets/deerdead/` | je Zustand XML | Die Gruppe `actiongroups/deerdead` existiert und benutzt niemand (kein AnimSet, keine Definition), eigene Clipnamen, eigene Tempi | Kein `followwall`, `onhook`, `trailer`; mehr Dateien |
| C: `animset = "cow"`, Clips heissen `Cow_*` | keine | Gruppe hat `attack`: `Cow_Attack_HeadSwipe` traegt `AttackConnect` bei 35 %. **Weg fuer den Krallenhieb spaeter.** `cow` skaliert das Gehen mit `animalSpeed` | Kann angreifen, je nach Feldern |

**Empfehlung: A.** Das Rehtier merkt nichts, weil `AnimationSet` die XML teilt und die Clips je Netz aufgeloest werden.

### 3.3 `AnimSets/buck`: was der Baer braucht

Variablen, die die Knoten fragen: `idleAction`, `bMoving`, `animalRunning`, `TrailerAnimation`, `AlertX`, `AlertY`. Ereignisse: `idleActionEnd`, `PlayBreedSound`, `PlayDeathSound`.

| Zustand / Knoten | Clip | Schleife | Bedingung | Fuer den Baeren |
|---|---|---|---|---|
| idle/idle1 | DeerStag_Idle01 | ja | - | **Pflicht** |
| pathfind/pathfindWait | DeerStag_Idle01 | ja | - | dieselbe |
| hitreaction/hitreaction1 | DeerStag_Idle01 | nein | - | dieselbe. **Uebergang zurueck braucht `ActiveAnimFinishing`**, also 6 s Reaktion wie beim Reh; kuerzer ist besser |
| walk/defaultWalk, pathfind/defaultPathfind, followwall/default | DeerStag_Walk | ja | bMoving (ausser walk) | **Pflicht, mit Weg** |
| walk/run, pathfind/runPathfind, followwall/run | DeerStag_Run | ja | animalRunning | **Pflicht, mit Weg**. Notfalls gleiche Bewegung wie Walk, schneller |
| falldown/falldown | DeerStag_Death | nein | - | **Pflicht:** `falldown` -> `onground` nur auf `ActiveAnimFinishing`, und erst `AnimalOnGroundState.enter` ruft `die()`. Ohne Clip bleibt der Tote stehen. Bewegungsknochen hier `Bip01`, Achse Z |
| death, deadbody, onground | DeerStag_Dead | | - | **Pflicht** (Leichenhaltung, 2 Bilder) |
| idle/idle2, idle3, Idle4 | Idle02, Idle03, IdleEating01 | nein | idleAction idle1/2/3 | Nur wenn `idleTypeNbr` > 0. **Am Anfang 0.** |
| eating/eating | IdleEating01 | ja | idleAction eat | Nur bei `eatGrass`, Trog. Weglassen |
| idle/idleSit, Uebergaenge | SittingIdle, IdleToSitting, SittingToStanding | | idleAction sit | Nur bei `sitRandomly`. Weglassen |
| alerted/alerted | AlertLookFwd/Left/Right | ja | - | Nur bei `canBeAlerted`. Weglassen |
| onhook/onhook, trailer/* | OnHook, Dead, Idle01 | | | Ohne `hook`, ohne Anhaenger nicht erreichbar |
| (kein Knoten) | DeerStag_WalkLimp, SittingToDeath | | | In `buck` nirgends benutzt |

**Mindestsatz: `DeerStag_Idle01`, `DeerStag_Walk`, `DeerStag_Run`, `DeerStag_Death`, `DeerStag_Dead`.** Fuer Run und Walk zaehlt der Weg; Idle, Death, Dead haben keinen Weg. `Death` kann ohne waagerechte Bewegung von `Bip01` auskommen (Bewegungsknochen).

---

## 4. Spawn, Tod, Leiche

### 4.1 Spawn

Vanilla-Weg, beide Modi (DebugContextMenu.lua:1454-1472):

- Einzelspieler: `local a = addAnimal(getCell(), x, y, z, type, breed, false); a:addToWorld()`. `addAnimal` ist `LuaManager$GlobalObject.addAnimal(IsoCell,int,int,int,String,AnimalBreed,boolean)`.
- Mehrspieler: `sendClientCommandV(player, "animal", "add", "type", t, "breed", breed:getName(), "x", x, "y", y, "z", z, "skeleton", false)`; Server ClientCommands.lua:753-761 braucht `Capability.AnimalCheats`, holt `AnimalDefinitions.getDef(args.type):getBreedByName(args.breed)`, ruft `addAnimal` und `addToWorld`.
- Breed-Objekt: `def:getBreeds():get(i)` (DebugContextMenu.lua:277-279) aus `getAllAnimalsDefinitions()` (:250), oder `AnimalDefinitions.getDef(t):getBreedByName(n)` (ClientCommands.lua:758).

**Kein eigener Code noetig:** die Liste liest `getAllAnimalsDefinitions`, also steht der Baer im Debug-Rechtsklick unter "Tiere" automatisch (mit `-debug`, doDebugAnimalMenu DebugContextMenu.lua:230, Gruppe aus `group`, "Add <Name>", dann die Rasse). Eine kleine Konsolenfunktion ist Komfort.

Riegel in Konstruktor: auf Wasser (`checkForWater`) bleibt das Tier uninitialisiert, nicht auf Wasser spawnen.

### 4.2 Tod und Zerlegen

Reihenfolge: `isDead` -> Gruppe `falldown` -> `ActiveAnimFinishing` -> `onground` -> `die()` -> `IsoDeadBody.setAnimalData` -> Lua `setAnimalBodyData`.

| Feld | Muss? | Wenn fehlt |
|---|---|---|
| `AnimalPartsDefinitions.animals[typ..breed]` | ja | ButcheringUtil.lua:27 `def.feather` wirft (geschuetzt gerufen, Leichendaten unvollstaendig) |
| Gen `meatRatio` | ja | ButcheringUtil.lua:40 wirft; ausserdem Text :70 |
| `invIcon*Dead`, `invIcon*Skel` | setzen | `IsoDeadBody.getItem`: `Texture.getSharedTexture(icon)` mit null; Reh-Icons nehmen (`Item_DeerMale_Dead`, `Item_Skeleton_Deer_Stag`) |
| `parts`, `bones` | ja, in der Attrappe | ButcheringUtil.lua:98-101 |
| `leather`, `head`, `skull`, `feather` | nein | null-sicher |
| `AnimalAvatarDefinition[..].hook` | **nein, weglassen** | ohne hook kein Schlachthaken; Zerlegen am Boden (ButcheringUtil.lua:36, ISButcherAnimal.lua:80) |
| `rottenTexture` | nein | `AnimalVisual.getModel` prueft auf leer |
| `textureSkeleton` + `bodyModelSkel` | nein | `canBeSkeleton` false; Knochenreste bleiben Baer-Modell |

Attrappe erlaubt: `AnimalPartsDefinitions.animals["bearbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]` liefert Reh-Fleisch, Reh-Kopf.

---

## 5. Verhalten

### 5.1 `wild = true` (wie Reh)

`IsoAnimal.init` setzt `setWild(adef.wild)`, Stress 50-80. `BaseAnimalBehavior.spotted`: Spieler unter 3 Kacheln -> flieht; laufender Spieler in `spottingDist` wird zufaellig bemerkt; flieht 30 Kacheln im Rennen. Kein Hunger. Treffer: blutet, flieht, faellt nach `wildFleeTimeUntilDeadTimer`. **Fuer Kevins Wunsch nicht passend, man sieht ihn nur fliehen.**

### 5.2 `wild = false` (empfohlen)

- Laufen: `wanderIdle` alle `wanderMul`..`wanderMul*5` Ticks, Ziel +-8 Kacheln, freie Kachel, im Schritt. Das ist das Herumlaufen.
- Spieler: `spotted` setzt `spotted = true` nur fuer wilde (`isWild() && Spieler`). Zahm: **flieht nie vor dem Spieler**, trotz `alwaysFleeHumans` (das wird nur in `fleeFromChr` gefragt, wenn `spottedChr` gesetzt ist). Treffer: rennt 20 Kacheln weg (`fleeFromAttacker`), wenn `attackBack` aus.
- Zombies: mit `fleeZombies = false` steigt `spotted` aus (`if (!(zombie) || fleeZombies)`): keine Flucht, kein Stress.
- Laerm: `IsoAnimal.respondToSound` laeuft auch zahm (ausser bei Fahrzeuglaerm). Ein Schuss in der Naehe laesst ihn rennen. Dafuer braucht es `DeerStag_Run` mit Weg.
- Hunger: `hungerMultiplier`/`thirstMultiplier` Vorgabe 0: bleibt satt, kein Sterben (`updateHungerAndThirst`, `getHungerReduction`).
- Alter: ohne `maxAgeGeriatric` altert er nicht zu Tode. Ohne `mate`/`babyType` keine Vermehrung.
- `canBeDomesticated = false`: `setWild(false)` macht dann nichts, das Feld ist ohnehin false.

### 5.3 Angriff

Schaden am Spieler entsteht **nur** in `AnimalAttackState.animEvent` bei `AttackConnect`. Der Zustand `attack` existiert nur in den Gruppen cow, pig, ram, cockerel, turkey (`media/actiongroups/*`). In `buck` und `deerdead` nicht. Felder, die sonst ausloesen:

| Feld | Vorgabe | Wirkung |
|---|---|---|
| `attackBack` | false | `fleeFromAttacker`: Gegner setzen statt fliehen; `hitConsequences` (Server) `goAttack` |
| `attackIfStressed` | false | `spotted`: Stress > 80, Akzeptanz < 30 -> `goAttack` |
| `canThump` | **true** | Tritt gegen Tueren bei Stress >= 80; `isAnimalAttacking` |
| `dontAttackOtherMale` | false | Kampf unter Maennchen nur in Tierzonen |
| Gen `aggressiveness` | | Von keiner Tierklasse gelesen (Jar-Suche: nur `SurvivorDesc`) |

Mit `animset = "buck"` ist Angriff ausgeschlossen, egal was gesetzt ist. Trotzdem `canThump = false` setzen.

**Zombie greift Tier an: nein.** In `IsoZombie` kommt `isAnimal` nur in `updateSearchForCorpse` vor (javap 42.21); kein Treffer-Paket, passt zu CLAUDE.md.

### 5.4 NPC Crew

`shared/BanditsNPCAnimals.lua:51-73` `A.ApplyNoFear`: jede Art ohne `wild == true` bekommt `fleeZombies = false`. Fuer den Baeren ohne Wirkung (schon gesetzt), wenn beide Mods laufen.
`shared/BanditsNPCLivestock.lua:5149` `Lv.NOT_TENDED` zaehlt nur rabbit, mouse, rat, raccoon, deer und Weitere auf, **`bear` nicht**. Steht der Baer in einer Tierzone, zaehlt der Tierpfleger ihn mit (:1872-1880). Beim Test nicht in eine Tierzone stellen; bei Uebernahme in NPC Crew `group = "bear"` eintragen.

---

## 6. Fazit

### 6.1 Dateiliste lebendes Tier (Weg A)

```
Zomboid/mods/NCBearTest/
  mod.info, 42/mod.info
  42/media/scripts/nc_bear.txt                    module Base: animationsMesh + model (2.7)
  42/media/models_X/Skinned/NCBear.glb            Netz + Clips (2.3, 2.4)
  42/media/textures/Body/NCBear.png               (2.5)
  42/media/lua/shared/NCBearDefs.lua              Definition (unten)
  42/media/lua/shared/Translate/EN/IG_UI.json     optional
  42/media/lua/client/NCBearSpawn.lua             optional, Konsole
```
**Nicht noetig:** `AnimSets`, `actiongroups`, `anims_X`, `fileGuidTable.xml`. Auch nichts unter `common/` (Turret lief genauso).

### 6.2 Definition (Vorschlag, alle Felder aus Abschnitt 1)

```lua
AnimalDefinitions = AnimalDefinitions or {}
AnimalDefinitions.animals = AnimalDefinitions.animals or {}

local stages = { bear = { ageToGrow = 60 } }
local genes = { meatRatio="meatRatio", maxWeight="maxWeight", resistance="resistance", strength="strength",
    hungerResistance="hungerResistance", thirstResistance="thirstResistance", stress="stress" }
local breeds = { brown = {
    name="brown", texture="NCBear", textureMale="NCBear",
    invIconMale="Item_DeerMale_Dead", invIconFemale="Item_DeerFemale_Dead",
    invIconMaleDead="Item_DeerMale_Dead", invIconFemaleDead="Item_DeerFemale_Dead",
    invIconMaleSkel="Item_Skeleton_Deer_Stag", invIconFemaleSkel="Item_Skeleton_Deer_Doe",
} }

AnimalDefinitions.animals["bear"] = {
    bodyModel="NCBear_Body", animset="buck", group="bear", male=true,
    stages=stages, breeds=breeds, genes=genes,
    minSize=1.0, maxSize=1.0, animalSize=0.3, collisionSize=0.42,
    shadoww=0.9, shadowfm=1.8, shadowbm=1.8, corpseSize=3.0,
    minWeight=200, maxWeight=400, minBlood=1500, maxBlood=4000, trailerBaseSize=600,
    wild=false, canBeDomesticated=false, fleeZombies=false, alwaysFleeHumans=false,
    canThump=false, canBePicked=false, canBeAlerted=false, sitRandomly=false, dontAttackOtherMale=true,
    wanderMul=600, idleTypeNbr=0, spottingDist=10,
}

local b = AnimalAvatarDefinition["buck"]
AnimalAvatarDefinition["bear"] = { zoom=b.zoom, xoffset=b.xoffset, yoffset=b.yoffset, avatarWidth=b.avatarWidth,
    avatarDir=b.avatarDir, trailerDir=b.trailerDir, trailerZoom=b.trailerZoom,
    trailerXoffset=b.trailerXoffset, trailerYoffset=b.trailerYoffset }

AnimalPartsDefinitions.animals["bearbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
```
`maxSize` absichtlich nicht in `genes` (1.2). Ein Reh-Icon ist Attrappe.

### 6.3 Risiken

| Risiko | Einschaetzung | Gegenmittel |
|---|---|---|
| `.glb` im Tierweg nie benutzt (nur Tueren) | mittel-gering. Lader und Skinning sind dieselben, offline gemessen. Nicht geprueft: das Bild im Spiel (`animalEffect`, `ModelInstanceTextureCreator`) | Zuerst Rueckfall 6.5 |
| Export aus Hochmodell: Baken von IK, Umbenennung | mittel | Mit `Probe.java` pruefen, bevor Kevin startet: Clips, Knochennamen, `gehaeutet bbox`, Weg |
| Textur 2048 | gering, **ungeprueft** | Mit 1024 anfangen |
| Mehrspieler: Server muss `.glb` laden, um den Weg zu rechnen | **ungeprueft**. `GameServer` ruft `ModelManager.create` mit `noOpenGL` (Offset 275), die DLL liegt dabei | Erst Einzelspieler; dann Testserver |
| Spielstand ohne Mod mit gespeichertem Baer | **real.** `IsoAnimal.load` Offset 165: `getDef` null, dann `adef.getBreedByName` NPE; ob das gefangen wird: ungeprueft | **Wegwerf-Spielstand**, oder vor dem Abschalten "Alle entfernen" im Debug-Menue |
| Echte Rehe veraendern sich? | nein | Clips je Netz, keine Datei von `buck` geaendert |
| Tippfehler in `bodyModel` | ernst | `getLoadedModel` liefert null: Tier ohne Bild. Fehlt das Feld ganz: Ausnahme in der Schleife ueber alle Tiere (1.2) |
| `-debug` kann Fehler auf den Bildschirm legen (Break on Error) | gering | `console.txt` lesen, bugwatch mitlaufen |

### 6.4 Was nur Kevins Test entscheidet

- Sieht der Baer richtig aus (Groesse, Licht, Textur, keine zerrissenen Stellen)? `setSizeForced` zum Nachstellen.
- Dreht er sich und laeuft er in Blickrichtung? (Rechnerisch ja, Vorzeichen wie beim Reh gemessen.)
- Passt der Gang zum Boden (Fussgleiten)?
- Sturz, Leiche, Zerlegen ohne Fehlerzeile.
- Wirft er einen Schatten an der richtigen Stelle?
- Mehrspieler: Spawn als Admin, Laufen beim zweiten Client.

### 6.5 Einfachste Form, die sicher etwas Laufendes zeigt

**Ja, Baeren-Haut auf vorhandenem Skelett geht, und zwar als eigenes Netz:**

```
model NCBear_Body { mesh = Skinned/NCBear.glb, shader = animalEffect, static = false, animationsMesh = Deer_Stag, }
```
Vanilla-Beleg: `Bull_Body` auf `CowAndBull`, `DeerStag_Headless` auf `Deer_Stag` (models_animals.txt:80-85, :788-793). Der Lader (`applyToMesh`, `skinnedTo != null`) nimmt die Clip-Tabelle des Rehs und die Haut-Matrizen des eigenen Netzes; jeder Knochen findet sein Gegenstueck ueber den Namen.

- Ohne eigene Clips, ohne Backen: alle 17 Rehclips inklusive Weg, Sturz, Leiche.
- Noetig sind nur Umbenennung (2.4) und Export. Eigene Knochen wie `Bip01_Jaw1..7` bekommen keine Schluessel und stehen auf Identitaet: **vor diesem Weg die Kieferstufen weglassen oder ihre Gewichte auf `Bip01_Jaw`/`Bip01_Head` legen.**
- Der Baer haelt dabei die Knochenpositionen des Rehs: kleiner, schmale Haltung, Springen statt Trotten. Es sieht nach Baer in Rehhaltung aus, nicht nach Baer.
- Reine Textur auf `DeerStag`-Modell (`bodyModel = "DeerStag"`, eigene Textur) prueft nur Definition und Spawn, ohne Baerenform. Als **Stufe 0** sinnvoll: testet Abschnitt 1 ohne jedes Modellrisiko.

**Reihenfolge fuer den Folgelauf:**
1. Stufe 0 optional mitliefern (ein Schalter in der Lua-Datei).
2. Rueckfall 6.5: Netz auf `Deer_Stag`. Das zeigt sicher einen laufenden Baeren.
3. Eigene fuenf Clips in dieselbe `.glb`, `animationsMesh = NCBear` wie 2.7. Mit `Probe.java` abnehmen. Das ist der eigentliche Baer.

---

## Anhang: Probe wiederholen

```
JB=C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin ; G="C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"
H=C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness
"$JB/java.exe" -Djava.library.path="$G" -cp "$H;$G/projectzomboid.jar" Probe <datei.glb> glb tree
```
Zeigt Knotenbaum, Clips, Knochenliste, Weltposition von Kopf und Becken, gehaeutete Ausmasse, Weg am Clipende. Drittes Wort `x` oder `fbx` statt `glb` waehlt die Laderparameter.
Die Probe ersetzt keinen Spieltest, sie liest nur, was die Engine aus der Datei macht. Sie laedt `jassimp64.dll` aus dem Spielordner und startet das Spiel nicht.

Statisch geprueft und offline gemessen, nicht gespielt.
