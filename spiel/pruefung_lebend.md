# Pruefung: Baer als lebendes Tier (NCBearTest)

Stand 07.11.2026, Spiel 42.21. Gelesen in Vanilla und im Jar (javap, Lesehilfe Vineflower), GLB mit dem Importer des Spiels
nachgemessen (`tier_werkzeug/Probe.java`, `Dump.java`, dazu eigene Probe `_arbeit/baer_spiel/pruef_lebend/ProbeSk.java`,
die den Rueckfall wie `FileTask_LoadMesh` mit `skinnedTo = Deer_Stag` laedt). Statisch geprueft und offline gemessen, nicht gespielt.

## Funde

1. **ernst** -- `bau_lebend.md:28` und `42/media/lua/client/NCBearSpawn.lua:61-78` -- Der Satz "Vor dem Abschalten der Mod die
   Baeren entfernen" klingt, als waere der Spielstand danach ohne Mod sicher. "Remove living bears nearby" entfernt aber nur
   LEBENDE Baeren, nur geladene, nur 12 Kacheln. Es bleiben: Leichen aus dem Sturz-/Zerlege-Test, Leichen im Inventar,
   Baeren, die weggelaufen sind (Wandern je Gang +-8 Kacheln ohne Grenze, nach Treffer 20 Kacheln Flucht). -- Beleg: lebender
   Baer ohne Mod: `IsoAnimal.load` Offset 165 `getDef` -> 179 `getBreedByName` ohne Null-Pruefung. Leiche ohne Mod:
   `IsoDeadBody.load` ist null-sicher, aber das Zeichnen geht ueber `DeadBodyAtlas.getBodyKey` Offset 144 nach
   `AnimalVisual.getModel` Offset 275-287 (`getDef(..).bodyModel`, keine Null-Pruefung): Ausnahme bei jedem Bild, in dem die
   Leiche zu sehen ist; mit -debug und Break on Error haelt das Spiel an. Ob die Engine das faengt: ungeprueft. -- Vorschlag:
   Satz ersetzen durch "Nur in einem Wegwerf-Spielstand testen und diesen danach nie ohne NCBearTest laden. Das
   Entfernen-Werkzeug raeumt nur lebende Baeren in der Naehe, keine Leichen." Ein Werkzeug fuer Leichen nur mit
   Vanilla-Fundstelle fuer das Entfernen eines `IsoDeadBody`.

2. **klein** -- `bau_lebend.md:22-28` (fehlt) -- Hinweis aus `tier_spez.md` 5.4 ist nicht beim Bericht angekommen: steht der Baer
   in einer Tierzone von NPC Crew, zaehlt der Tierpfleger ihn mit. -- Beleg: `NPCCrew/42/media/lua/shared/BanditsNPCLivestock.lua:5149`
   `Lv.NOT_TENDED` ohne `bear`, Zaehlung :1873-1880. -- Vorschlag: Satz in die Anleitung: "Nicht in eine Tierzone stellen."

3. **klein** -- `42/media/lua/shared/NCBearDefs.lua:110-114` -- Zerlegen liefert die Teile des Hirsches: Rehfleisch, Hirschkopf
   mit Geweih, und weil der Baer keinen `hook` hat, beim Zerlegen am Boden auch Rehleder. Spez-gemaess Attrappe, Kevin
   aber nicht gesagt. -- Beleg: `AnimalPartsDefinitions.lua:445-454` (`head = Base.Deer_Buck_Head`, `leather = Base.DeerLeather_Full`),
   `ButcheringUtil.lua:36` (`babyLeather` ohne hook) und :117-126 (Leder am Boden). -- Vorschlag: ein Satz in die Anleitung.

4. **klein** -- `bau_lebend.md:48` -- Rueckfall: der Sturz des Rehs drueckt den Baerenkoerper zwischendurch tiefer in den Boden
   als die Liegehaltung: tiefster Punkt -0,182 E bei t = 1,1 s (rund 33 cm), genannt ist nur Dead -0,156. -- Beleg: `ProbeSk`
   mit `DeerStag_Death.x`; Walk -0,050 und Dead -0,156 stimmen mit dem Bericht ueberein. -- Vorschlag: Zahl nachtragen, keine
   Aenderung am Rueckfall.

Kein toedlicher Fund.

## Geprueft und in Ordnung

* **Definition gegen `AnimalDefinitions.loadAnimalDefinitions`:** jeder Schluessel in `NCBearDefs.lua` wird dort gelesen, kein
  Tippfehler; Zahlen, Wahrheitswerte und Tabellen passen zu den Lesern (`parseFloat`, `intValue`, `parseBoolean`, `loadStages`,
  `loadBreeds`, `loadGenes`, `loadSounds`). `bodyModel` gesetzt, also kein `getLoadedModel(null)` in der Schleife ueber alle
  Arten; `getLoadedModel` laedt asynchron und wirft dort nicht. Stufe heisst wie die Art (`bear`, `bearstag`), `ageToGrow` 60,
  `minSize = maxSize = 1,0` ohne `maxSize`-Gen: `initSize` rechnet 0/60, kein NaN, Groesse 1,0 (`AnimalData.initSize`,
  `getMinSize`). `male = true` -> `setFemale(false)` (AnimalData-Konstruktor) -> `textureMale` (`IsoAnimal.initTexture`).
  `group`, `genes` mit `meatRatio`, Rassenname `brown` (Schluessel `bearbrown`, `bearstagbrown`). Altern aus
  (`isGeriatric`: `maxAgeGeriatric <= 0`), Hunger/Durst bleiben 0 (Multiplikator 0, `updateHungerAndThirst`).
* **Ladefolge:** `NCBearDefs.lua` in `shared`, Vanilla vor Mods (`LuaManager.LoadDirBase`); `AnimalAvatarDefinition` und
  `AnimalPartsDefinitions` sind Vanilla-`shared`, auch auf dem Server da. `buckwhitetailed` existiert (AnimalPartsDefinitions.lua:454).
* **Skripte:** `module Base`; `animationsMesh NCBear` und `model NCBear_Body` nennen dieselbe Datei, also derselbe Asset wie beim
  Reh und den Vanilla-Tueren; `.glb` mit Punkt wird direkt genommen (`FileTask_AbstractLoadModel.checkExtensionType`).
  `NCBearStag_Body` auf `Deer_Stag` wie `Bull_Body`; `applyToMesh` leert nur das eigene Netz, das Reh bleibt unberuehrt.
* **GLB mit Probe.java:** 1 Netz, 1 Material, 25 Knochen (Grenze 60), Dummy01 = 0, Bip01 = 1, Translation_Data ohne Eltern
  (Hierarchie wie beim Reh: Elternindex 0). Clips `DeerStag_Idle01/Walk/Run/Death/Dead`, jeder Knochen in jedem Clip mit
  Schluesseln, alle Clips ab t = 0. Weg nur auf Translation_Data: Walk 0,3784 in 0,9 s, Run 1,0578 in 0,533 s, Vorzeichen wie
  `DeerStag_Walk.x` (0,9055), Seitenweg 0, linear. Idle/Walk/Run nahtlos, Ende Death = Dead. Bip01 in allen Clips fest bei
  (0, 0, 0,392) ohne Drehung: der Sturz (Bewegungsknochen Bip01, Achse Z, `AnimationTrack.getDeferredMovement` liest x/y)
  verschiebt nichts. Pflichtknochen Head, Spine, L/R Calf, L/R Foot, Pelvis, Neck da. Gewichte: Summe 1,0, hoechstens 4, 18
  Knochen, kein Punkt ohne Gewicht.
* **Rueckfall unabhaengig:** eigene Datei, eigenes Modell, nur auf `Deer_Stag`. Mit `skinnedTo` nachgeladen: keine neuen
  Knochen (40 = 40), Haut-Offsets der 21 gewichteten Knochen gleich dem Reh auf 1,3e-6.
* **AnimSet `buck`:** jeder erreichbare Knoten hat einen Clip. `idle2/3/4` nur bei `idleTypeNbr > 0`
  (`BaseAnimalBehavior` :154), Sitzen nur bei `sitRandomly` (:108), `alerted` nur bei `canBeAlerted` (:1717, `IsoAnimal` :3215),
  Fressen erst ab Hunger 0,1. Fehlende Toene sind null-sicher (`IsoAnimal.playBreedSound`).
* **Textur:** Pfad `media/textures/Body/NCBear.png` (`ModelInstanceTextureCreator.init(AnimalVisual,..)`), 1024 x 1024 RGB wie
  die Rehtextur RGB, kein Deckel im `TextureCombiner` (`getResultingWidth` = naechste Zweierpotenz). Ausrichtung mit
  Nahtpaaren gemessen (gleiche Position, andere UV): Reh 16,6 (richtig) gegen 34,9, Baer 5,0 gegen 40,8 -- Baer sitzt wie das
  Reh. Helligkeit an den Punkten Median 84, Reh 115, Kuh braun 97: im Bereich der Vanilla-Tiere.
* **Verhalten:** zahm, flieht nicht vor Spieler und Zombie; Treffer: `hitConsequences`, Flucht 20 Kacheln mit Run-Clip, kein
  Gegenangriff (`attackBack` aus, `buck` ohne `attack`), kein Tuertritt. Kontextmenue: Streicheln und Anleinen aus (Vorgabe
  false), Futter/Wasser erscheinen nicht (Hunger/Durst 0), also kein Aufruf von `getAttachmentWorldPos("head")` ohne
  Attachment; "Kill animal" geht ueber `ISKillAnimal` ohne Attachment. Spuren null-sicher (`getRandomTrack`).
* **Tod, Leiche, Zerlegen:** `falldown` -> `onground` (Death endet, Dead folgt ohne Sprung); `setAnimalBodyData` findet Teile und
  `meatRatio`; Leichenbild: ohne Skelett-, Faul-, Fell-, Kopflos-Felder bleibt `bodyModel` (`AnimalVisual.getModel`); ohne hook
  `isCorpseValid` false, Zerlegen am Boden (ISAnimalContextMenu.lua:678-693).
* **Spawn:** `addAnimal(IsoCell,int,int,int,String,AnimalBreed,boolean)` und `getAllAnimalsDefinitions` im Jar als globale
  Lua-Funktionen; Einzelspieler wie `DebugContextMenu.AddAnimal`; Mehrspieler grau mit Hinweis, Debug-Menue nur mit
  `UseDebugContextMenu`, Server prueft `AnimalCheats` (ClientCommands.lua:753-761). Texte fuer Gruppe, Art und Rasse da.
* **Lua-Pruefer:** luacheck.py und scopecheck.py ok, localcount hoechstens 21, luacheck_pz 6 x W113 nur `NCBearMenu` (in beiden
  Dateien mit `or {}`). Alle Fundstellen-Kommentare gegen Vanilla gelesen. ASCII, LF, kein BOM.
* **Stand:** die acht Dateien in der Mod sind byte-gleich mit `tier_mod`; stehendes Modell, Item, `nc_bear.txt`, `WorldItems/*`
  unveraendert; unter `NPCCrew/42` kein Treffer fuer `NCBear`/`bearstag`. Rehe: keine `buck`-Datei geaendert, Clips je Netz.
* **Bilder angesehen:** Gang, Nah, Sturz, Liegen, Rueckfall. Textur sitzt (Nase, Ohren, Krallen), Kopf vorn. Liegend sind die
  gefalteten Glieder dunkle Lappen (Dehnung, im Bericht genannt); im Rueckfall stehen die Hinterbeine im Galopp und im Sturz
  als Spitze ab (Rehknochen, im Bericht als "Reh im Baerenfell" genannt).

## Nicht geprueft

Video `baer_gang.mp4` (kein Abspielwerkzeug auf der Platte), das Spiel selbst, ob der Server die `.glb` laedt, ob die
Ausnahmen aus Fund 1 gefangen werden. Das Spiel lief waehrend der Pruefung nicht.

## Urteil

Der Bau traegt ohne toedlichen Fund; vor Kevins Test nur den Satz zum Abschalten der Mod berichtigen (Fund 1).
