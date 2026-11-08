# Baer als stehendes Spielmodell (NCBearTest) - Baubericht

Statisch geprueft, nicht gespielt. Das Spiel habe ich nicht gestartet. Stand 07.11.2026, Spiel 42.21, Blender 5.2.3, alle Renders auf der RTX 4090 (OptiX).

## Was wo liegt

| Was | Pfad |
|---|---|
| Test-Mod | `C:/Users/Kevin/Zomboid/mods/NCBearTest` (mod.info, 42/mod.info, common/media leer) |
| Modell | `42/media/models_X/WorldItems/NCBear.fbx` |
| Textur 2048 | `42/media/textures/WorldItems/NCBear.png` |
| Icon 32 | `42/media/textures/Item_NCBear.png` |
| Skript | `42/media/scripts/nc_bear.txt` (module NCBear, Modell NCBear_World, scale 0.544, Item BearStatic) |
| Spawnen | `42/media/lua/client/NCBearTest.lua` |
| Hochmodell | `NPCCrew-Nebenprojekte/baer/spiel/baer_quelle.py` (Kopie von Entwurf C, drei Stellschrauben geaendert, siehe unten) |
| Exportskript | `NPCCrew-Nebenprojekte/baer/spiel/baer_export.py` (Stufen ansichten, netz, backen, vorschau) |
| Bilder | `vorschau_spiel.png`, `vorschau_nah.png`, `vorschau_wie_spiel.png` (rechnet wie der Spiel-Shader) |

Nichts unter `NPCCrew/42`, `NPCCrew/common`, `NPCCrew/mod.info` geaendert, keine fremde Mod, kein workshop_sync, kein codemap, keine commit-meldung.

## Zahlen

* **Netz:** 14.228 Dreiecke, 7.156 Punkte. Hauptteil rund 13.400 Dreiecke, geschlossen (0 offene Kanten, Volumen positiv, also Normalen aussen), dazu 20 Krallen mit je rund 40 Dreiecken als eigene Schalen im selben Netz. Kopf rund 3.500 Dreiecke (Anteil 0,26), Maul geschlossen, keine Haarkarten.
* **Masse im FBX (Meter):** Laenge 1,955, Breite 0,995, Hoehe 1,164. Ziel war rund 2,2 und rund 1,1: die Laenge liegt 11 % darunter, die Hoehe 6 % darueber. Beides zugleich geht nur mit einem anderen Koerperbau; ich habe die Mitte genommen (`GROESSE = 0.75`).
* **Ursprung:** Boden unter dem Flaechenschwerpunkt. x von -0,798 (hinten) bis +1,157 (Nase), y etwa +-0,5, z ab 0. Kopf zeigt nach +X, dieselbe Achse wie die Turret-Rohre (Turret x bis +2,0, siehe Messung).
* **Abwicklung:** 44 Inseln, davon 20 Krallen; Fuellgrad 58 %. Texel je Meter im Median: Kopf 964, Rumpf 404, Beine 276. Schlecht aufgeloest sind nur die flachen Sohlen, die man nicht sieht.
* **Textur:** aus 37 gerenderten Ansichten MIT Fell auf die Abwicklung projiziert. 99,99 % der Texel direkt gesehen, der Rest von Nachbarn gefuellt. Mittel sRGB (102, 73, 50).

## Wie die Textur entsteht, und warum nicht Selected to Active

Selected to Active geht mit dem Fell nicht. Im Versuch (Blender 5.2.3) lehnt der Bake Hair-Curves als Quelle ab: `Object "h" is not a mesh or cannot be converted to a mesh`. Das Partikelhaar des Rumpfes habe ich nicht eigens versucht. Stattdessen:

1. 22 Ansichten des ganzen Baeren (2048, 96 Samples, OptiX-Entrauscher) und 15 nur des Kopfes (1536) im neutralen Rundumlicht, ohne Boden und ohne Sonne: kein Lichtklecks, keine Grasfarbe.
2. Jeder Texel kennt seinen 3D-Punkt und seine Normale. Je Ansicht: sichtbar laut Z-Puffer des Spielnetzes, Gewicht `cos^7`, Kopfansichten nur am Kopf und dort siebenfach. Hinter dem Fellrand (Alpha unter 0,45) zaehlt die Ansicht nicht.
3. sRGB, heller gebacken (`HELL = 1.95`, Gamma 0,92), kleine Unschaerfemaske, Rand 14 Texel ueber die Inseln hinaus.
4. Nacharbeit aus den Formeln des Kopfes: Auge (schmale dunkle Spalte, Lidrand, kein Glanzpunkt), Nase anthrazit statt Himmelsspiegelung, Mundlinie als dunkle Rille, Pfoten und Krallen dunkel bzw. Horn, Unterbeine aufgehellt.

## Wie die Fellhuelle entsteht

Haut aus Koerper, Kopfhuelle ohne Mund, Nase und Zehen per Voxel (8,5 mm) zu einem Netz, dann je Punkt entlang der Normalen nach aussen, solange der Punkt in JEDER Ansicht noch im Fell liegt (Alpha ab 0,5) und unter einer Grenze bleibt (Rumpf 11 cm, Bein 9 cm, Gesicht rund 60 % der Haarlaenge). Das Netz liegt damit an der echten Fellsilhouette. Dazu Zotteln bis gut 6 cm: am Rumpf gestreckt nach hinten-unten, am Bein nach unten, nie am Gesicht und an den Pfoten. Zweite Voxelrunde (11,5 mm) schliesst Falten und Selbstdurchdringungen, die vorher als dunkle Risse zu sehen waren. Verringern mit Blenders Decimate; die Vertexgruppe des Modifiers tat im Versuch nichts Brauchbares (Rumpf verschwand), deshalb wird die Gegend vorher radial aufgeblasen und hinterher zurueckgerechnet: dort zaehlt jeder Fehler mehr, also bleiben mehr Dreiecke stehen.

## Geaendert gegen Entwurf C (nur in baer_quelle.py, alle drei oben im Skript)

* `LZ_HUB` 0,33 -> 0,20: kuerzere Beine, sonst Schulter 1,6 bei Laenge 2,7 und das Tier wirkt hochbeinig.
* `KOPF_SK` 1,10 -> 1,17: Kopf groesser (Schwaeche im Entwurf: wirkt klein).
* Schnauze ab x=0,23 weich um 22 % gestaucht (`SN_X0, SN_W, SN_S`, l2w/w2l umkehrbar): Schwaeche im Entwurf war die Schnabelform.

Das Skelett und der Hieb stehen weiter in der Datei, sie sind aber nur bis vor "Boden und Licht" gelaufen und mit diesen Werten nicht neu geprueft. Der Folgelauf (lebendes Tier) muss das wissen.

## Scale: Herleitung

Gemessen, nicht geschaetzt:

| | Modellhoehe | scale | Mesh-Einheiten | |
|---|---|---|---|---|
| Turret Stufe 3 (`NCTurret.fbx`, per Import gemessen) | 2,056 | 0,6 | 1,234 | Kevin: passte neben der Figur |
| Spielfigur (`models_X/Skinned/MaleBody.x`, Y 0..0,9798) | 0,98 | 1 | 0,98 | |
| Baer (FBX in Metern) | 1,164 | **0,544** | 0,633 | |

Die Figur steht fuer 1,8 m, also ist 1 m = 0,98 / 1,8 = 0,544 Mesh-Einheiten. Das FBX ist in Metern, darum `scale = 0.544`. Baer zu Figur 65 % (1,164 m zu 1,8 m). Das Turret ist 1,26 Figuren hoch, der Baer halb so hoch wie das Turret. Zur Einordnung die Engine: `Core.DoPushIsoStuff` skaliert ein Modell mit 1,5 (Offset 411-422), eine Mesh-Einheit ist also 1,5 Kachellaengen; der Baer ist rund 1,6 Kacheln lang, das Turret 2,65.

**Ungeprueft:** ob die Animation die Figur noch skaliert; gemessen ist nur das Mesh. Passt die Groesse im Spiel nicht, ist es eine Zahl in `nc_bear.txt`, Neustart noetig.

## Wird die Figur abgeschnitten? Nein (Jar 42.21 gelesen)

`WorldItemModelDrawer.renderMain` fragt zuerst `renderAtlasTexture` (Offset 38), sonst zeichnet es das Modell direkt.

* `renderAtlasTexture` nimmt den Atlas, ausser: `isDoingExtendedPlacement` (18-26), Debug-Schalter `worldItemAtlas.enable` aus (Vorgabe an, `zombie/debug/options/WorldItemAtlas`), Chunk-Caching (Vorgabe aus: `itemsInChunkTexture` ist `newDebugOnlyOption(..., false)`), oder `isTooBig` (201-208).
* `WorldItemAtlas$RenderJob.render` rechnet die Eintragsgroesse aus dem Modell selbst: `calcModelBounds` nimmt alle acht Ecken von `mesh.minXyz/maxXyz` samt `ItemParams.transform` (dort steckt `scale x worldScale`, ItemParams Offset 742-794), `calcEntrySize` gibt 2 Pixel Rand und rundet auf 16. **Der Eintrag waechst also mit dem Modell.**
* Grenze: Breite oder Hoehe ueber 512 (`ATLAS_SIZE`) setzt `tooBig` (Offset 88-113); dann kehrt `renderAtlasTexture` mit false zurueck und das Modell wird direkt in 3D gezeichnet. In beiden Faellen wird nicht beschnitten; der Viewport ist 1024 (`MATRIX_SIZE`) und wird um den Mittelpunkt des Eintrags verschoben.
* Rechnung (tileScale 2): 1 Mesh-Einheit = 1920 x `Core.scale` (0,04714, Core.clinit Offset 164-183) x 1,5 = 135,8 Atlas-Pixel. Baer bei scale 0,544: rund 154 x 152 Pixel, Eintrag 160-176; mit `MAX_ZOOM` 2,5 (nur bei `getOptionHighResPlacedItems` und Zoom unter 0,75) rund 385 x 380, immer noch im Atlas. Turret: 275 x 283, gezoomt 690 x 706, dort also der 3D-Weg. Kevin hat das Turret unbeschnitten gesehen, es ist groesser als der Baer.

**Was das nicht sagt:** ob Waende oder Nachbarkacheln einen Teil richtig verdecken. Das Atlasbild traegt eine eigene Tiefe (`ItemTextureDepthDrawer`), mehr als eine Kachel Ausdehnung neben einer Wand habe ich nicht durchgerechnet. Das sieht man nur im Spiel.

Drehen: `ItemParams.isStillValid` vergleicht `worldZRotation` (Offset 12-21), eine neue Drehung baut einen neuen Eintrag. Der Menuepunkt wirkt also sofort.

## Warum das Turret dunkel war, und was ich dagegen getan habe

`basicEffect.frag`: Bildfarbe = Textur x min(Licht, 1), ohne Gamma. `RenderJob.renderModel`: Umgebung 0,4, ein Licht aus Richtung (0,5,-2) mit 0,375 (Offset 413-438, 561-638). Eine senkrechte Flaeche sieht also 0,4 bis 0,54 der Texturfarbe, die Oberseite bis 0,75, dazu kommt das Kachellicht. Deshalb ist die Textur um das rund 1,95-fache heller gebacken; `vorschau_wie_spiel.png` rechnet genau diese Formel ohne Kachellicht. Abgeschnittene Werte 0,01 %. Ist es im Spiel zu dunkel oder zu hell: `BAER_HELL` setzen und nur `backen` und `vorschau` laufen lassen, rund 40 Sekunden.

## Lua: Fundstellen (jede steht auch als Kommentar im Code)

| Aufruf | Fundstelle |
|---|---|
| `not isClient() and not isServer()` | ISEatFoodAction.lua:136 |
| `square:AddWorldInventoryItem(instanceItem(typ), x, y, z)` | FenrisScenario.lua:8 |
| `item:setWorldZRotation(zahl)` | FenrisScenario.lua:39, ISDropWorldItemAction.lua:83 |
| `item:getWorldZRotation()` | ISExtendedPlacementUI.lua:160 |
| `getWorldItem():setIgnoreRemoveSandbox(true)` | ISDropWorldItemAction.lua:84-85 |
| `square:getX/getY/getZ` | DebugContextMenu.lua:640 |
| `getCell():getGridSquare(x, y, z)` | DebugContextMenu.lua:1436 |
| `square:getWorldObjects()`, `:get(i):getItem()` | ISWorldObjectContextMenu.lua:2973-2975 |
| `item:getFullType()` | ISInventoryPaneContextMenu.lua:4290 |
| Entfernen (fuenf Aufrufe, Einzelspieler) | ISGrabItemAction.lua:129-134 |
| `context:addOption(text, worldobjects, nil)`, `ISContextMenu:getNew`, `addSubMenu` | ISWorldObjectContextMenu.lua:585, DebugContextMenu.lua:54-56 |
| `subMenu:addOption(text, ziel, fn)` | AdminContextMenu.lua:46 |
| `notAvailable`, `addToolTip`, `description` | ISWorldObjectContextMenu.lua:271-275 |
| `getSpecificPlayer`, `getCurrentSquare` | DebugContextMenu.lua:24, :348 |
| `Events.OnFillWorldObjectContextMenu.Add` | ISHutchMenu.lua:115 |

Pruefer: luacheck.py ok, scopecheck.py ok, localcount.py hoechstens 21 Locals, luacheck_pz.py 0 Treffer. Neuer Global ist nur `NCBear_Spawn`. Einzelspieler: alle Menuepunkte; Mehrspieler: "NC Bear" grau mit Hinweis "singleplayer only", `NCBear_Spawn()` druckt dasselbe. Nichts laeuft je Bild.

## Unsicher, bis Kevin es sieht

1. Lage, Drehachse und Groesse: nach dem Turret-Muster gebaut, im Spiel ungesehen.
2. Ob die Textur richtig herum sitzt: gleicher Weg wie beim Turret (Blender-UV, Blender-PNG, gleiche FBX-Optionen), die Vorschau liest das fertige FBX und PNG aus der Mod.
3. Helligkeit: gerechnet, nicht gesehen.
4. Der Baer liegt ueber mehrere Kacheln: Verdecken an Waenden siehe oben.
5. Zweite Gefahr fuer Kevins Test: die Option 3D-Bodengegenstaende muss an sein (`renderMain` Offset 12-24 gibt sonst NoModel); beim Turret war sie es.

## Neu bauen

Sechs Runden gebraucht. `baer_export.py` lief hintereinander mit `ansichten` (rund 6 Minuten, nur noetig, wenn sich das Hochmodell aendert; die Bilder liegen im Scratchpad unter `baer_spiel/ansichten`, 474 MB, und gehen mit der Sitzung weg), `netz` (rund 25 s), `backen` (rund 30 s), `vorschau` (rund 5 s). Die kurze Spielprobe `vorschau_wie_spiel.png` rechnet ohne Kachellicht und ohne Tiefe.

## So kommt er ins Spiel

Spiel neu starten (Lua und Skripte laden nur beim Start), Mod "NC Bear Test" aktivieren, im Einzelspieler Rechtsklick auf den Boden: "NC Bear" -> "Spawn bear model here", "Turn nearest bear model 45 degrees", "Remove bear models nearby" (Umkreis 8 Kacheln). Oder in der Konsole `NCBear_Spawn()`.
