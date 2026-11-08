# Baer als lebendes Tier (NCBearTest) - Baubericht

Statisch geprueft und offline gemessen, nicht gespielt. Stand 07.11.2026, Spiel 42.21, Blender 5.2.3. Gemessen wurde mit
dem Importer des Spiels (`jassimp64.dll`, `ProcessedAiScene`, Harness `tier_werkzeug/Probe.java` und `Dump.java`), das
Spiel lief dabei nicht. Renders auf der RTX 4090 (OptiX mit Entrauscher), vor jedem Render `tasklist`: das Spiel lief nie.

## Was jetzt in der Mod liegt (in einem Zug kopiert, byte-gleich geprueft)

| Datei unter `NCBearTest/42/media/` | Inhalt |
|---|---|
| `models_X/Skinned/NCBear.glb` | Spielnetz (14.228 Dreiecke) auf eigenem Skelett, fuenf Clips |
| `models_X/Skinned/NCBearDeer.glb` | dasselbe Netz auf dem Skelett des Rehs, ohne Clips (Rueckfall) |
| `textures/Body/NCBear.png` | 1024er, 2x2-Mittel der gebackenen 2048er |
| `scripts/nc_bear_tier.txt` | `module Base`: `animationsMesh NCBear`, `model NCBear_Body`, `model NCBearStag_Body` |
| `lua/shared/NCBearDefs.lua` | Arten `bear` und `bearstag` |
| `lua/shared/Translate/EN/IG_UI.json` | Namen im Debug-Menue |
| `lua/client/NCBearSpawn.lua` | drei Menuepunkte, Konsole `NCBear_SpawnLive()` |
| `lua/client/NCBearTest.lua` | Haken fuer weitere Menuepunkte, Hinweis im Mehrspieler |

Unveraendert: stehendes Modell, Item `NCBear.BearStatic`, `nc_bear.txt`, `WorldItems/*`, mod.info. Nichts unter NPC Crew, keine fremde Mod.

## So kommt er ins Spiel

Spiel neu starten. Einzelspieler, Rechtsklick auf den Boden, "NC Bear":
"Spawn living bear here" (eigene Bewegung), "Spawn living bear (deer motion)" (Rueckfall), "Remove living bears nearby" (12 Kacheln).
Konsole: `NCBear_SpawnLive()` bzw. `NCBear_SpawnLive("bearstag")`. Mit -debug zusaetzlich Debug-Menue, Tiere, "Bear (NC test)".
Mehrspieler: "NC Bear" grau, Hinweis auf das Debug-Menue (dort spawnt der Server, Rolle noetig, ClientCommands.lua:754).
**Nur in einem Wegwerf-Spielstand testen und diesen danach nie ohne NCBearTest laden.** Das Entfernen-Werkzeug raeumt nur
lebende, geladene Baeren in 12 Kacheln, keine Leichen und keine weggelaufenen (tier_spez.md 6.3, pruefung_lebend.md Fund 1:
lebender Baer ohne Mod `IsoAnimal.load` Offset 179, Leiche ohne Mod `AnimalVisual.getModel` Offset 275-287 bei jedem Bild).
Nicht in eine Tierzone von NPC Crew stellen (der Tierpfleger zaehlt `bear` mit, `Lv.NOT_TENDED`). Zerlegen liefert Rehteile
(Rehfleisch, Hirschkopf, am Boden Rehleder): Attrappe.

## Zahlen (aus der Datei, wie die Engine sie liest)

Massstab 0,544 Einheiten je Meter im Netz, `minSize = maxSize = 1.0`, kein `scale=`. Ruhehaltung gehaeutet (-0,269 0 -0,629) .. (0,272 0,633 0,434).

| Clip | Dauer | Schleife | Weg | Tempo | gehaeutet (x y z) |
|---|---|---|---|---|---|
| DeerStag_Idle01 | 3,20 s | ja, erstes = letztes Bild | 0 | - | (-0,274 0,000 -0,624)..(0,276 0,634 0,436) |
| DeerStag_Walk | 0,90 s | ja | 0,378 E | 0,420 E/s = **0,67 Kacheln/s** | (-0,276 -0,013 -0,623)..(0,276 0,635 0,439) |
| DeerStag_Run | 0,533 s | ja | 1,058 E | 1,98 E/s = **3,17 Kacheln/s** | (-0,272 -0,016 -0,637)..(0,275 0,667 0,460) |
| DeerStag_Death | 2,57 s | nein | 0 | - | (-0,363 -0,008 -0,629)..(0,282 0,621 0,434) |
| DeerStag_Dead | 2 Bilder | - | 0 | - | (-0,363 0,002 -0,592)..(0,221 0,531 0,430) |

* Knochen: 25 (Grenze 60). Dummy01 Index 0, Bip01 Index 1, Translation_Data ohne Eltern. 18 mit Gewicht; Clavicle und Toe0 ohne. Jeder Knochen hat in jedem Clip Schluessel. Hoechstens 4 Einfluesse, Summe 1,0000.
* Weg nur auf Translation_Data, lokal (0, 0, -Weg), Seitenweg 0. Bip01 steht in allen Clips still bei x = y = 0: der Sturz (Bewegungsknochen Bip01, Achse Z) verschiebt damit nichts.
* **Fussgleiten:** gerechnet mit dem Spiel selbst: Tier laeuft 1,6 x Weg (MotionScale, Defaults.xml), das Bild zeigt 1,5 Kacheln je Einheit (Core.DoPushIsoStuff 413-422). Darum ist der Clip-Weg = Stuetzweg / 1,0667. Ergebnis Walk: der Ballen wandert in der Stuetze 0,01 bis 0,02 Kacheln (Tempo 0,03 bis 0,06 Kacheln/s gegen 0,67 des Rumpfs). Run: 0,02 bis 0,05 Kacheln je Stuetze. Zum Vergleich: das Reh gleitet etwa 10 %.
* Walk liegt bei 0,67 Kacheln/s statt 0,76 (2.8): schneller ginge nur mit laengerem Schritt, und dann knicken die Beine. Ein Zyklus = ein Doppelschritt.
* Dehnung der Hautkanten (Kanten ueber 4 mm, 99,5 %-Wert / Maximum): Idle 1,15 / 1,40; Walk 1,68 / 3,72; Run 2,09 / 4,18; Death 2,10 / 4,59; Dead 2,08 / 4,57. Die Spitzen sitzen am Handgelenk, am Ellbogen und in der Achsel beim Schwung bzw. beim Liegen.
* Tiefster Punkt: Walk -0,013 E (2,4 cm im Boden, Krallenspitzen), Run -0,016, Death -0,008, Dead +0,002.
* Rueckfall: 40 Knochen, Ruhehaltung gleich dem Reh (Offsets auf 0,000001 genau), 21 mit Gewicht. Mit den Rehclips: Walk tiefster Punkt -0,050 E, Dead **-0,156 E** (der Rumpf sinkt etwa 29 cm ein, das Reh liegt flacher), im Sturz (DeerStag_Death) zwischendurch **-0,182 E bei t = 1,1 s** (rund 33 cm; Nachmessung der Pruefung mit `ProbeSk`), Dehnung 99,5 % 3,3 (Walk) bis 6,2 (Death).

## Wie es gebaut ist (`baer_tier.py`)

* Netz aus `WorldItems/NCBear.fbx` der Mod, gedreht (Kopf nach -Y), mal 0,544, ein Material ohne Bild.
* Skelett neu, an die heutige Figur angepasst: Gelenke aus Querschnitten des Spielnetzes (Beine mittig, Ellbogen hinter, Knie vor der Beinlinie, Kopfgelenk bei x 0,70 m fuer den groesseren Kopf und die kuerzere Schnauze). Das alte Skelett aus `baer_quelle.py` und der Hieb werden nicht benutzt; die Bemerkung des Vorlaufs (LZ_HUB, KOPF_SK, Schnauze ungeprueft) ist damit hinfaellig.
* Gewichte neu gerechnet: Rumpf entlang der Laengsachse, Beine nach Abstand zur Beinachse (zum Bauch hin strenger), weicher Uebergang am Bauchrand, unter 17 cm reines Bein, Krallen starr an der Pfote, zwei Glaettungsrunden ueber die Netzkanten.
* Clips aus Formeln, je Bild in Knochenschluessel gerechnet (Zwei-Knochen-IK von Hand, keine Constraints): Passgang (Beine einer Seite fast zugleich, Rumpf rollt zur Stuetzseite, Schulter rollt nach), Rumpf sinkt nur, wenn die stuetzenden Beine es verlangen; Galopp mit Beugen und Strecken; Sturz: wankt, sackt, kippt immer schneller auf die rechte Flanke, federt nach, Kopf kommt zuletzt auf. Die Liegehoehe wird an der Haut gemessen, damit nichts im Boden steckt.
* Rueckfall `NCBearDeer.glb`: eigene Datei, weil die Ruhehaltung jedes Knochens genau die des Rehs sein muss; mit den Knochen von NCBear.glb waeren die Teile verdreht. Beine nach Hoehe auf die langen Rehknochen, der Stummelschwanz am Becken (der Rehschwanz stellt sich sonst als Stachel auf).

Neu bauen: `blender --background --factory-startup --python baer_tier.py -- <Zielordner> <deer_walk.txt>` (wenige Sekunden; zweimal gebaut, beide GLB und die Textur byte-gleich; `deer_walk.txt` macht `tier_werkzeug/Dump.java` aus `anims_X/Deer/DeerStag_Walk.x`). Pruefen: Dump der GLB, dann `tier_werkzeug/tier_pruef.py`. Bilder: `baer_tier_bild.py` (rendert die Engine-Daten, nicht die Blender-Szene).

## Definition und Lua

* `NCBearDefs.lua`: alle Pflichtfelder aus 1.2 (bodyModel, animset `buck`, stages mit dem Tiernamen, ageToGrow 60, breeds mit texture und textureMale, minSize/maxSize, group, genes mit meatRatio, ohne maxSize-Gen), dazu AnimalAvatarDefinition (ohne hook) und AnimalPartsDefinitions als Reh-Attrappe (1.3). Friedlich: wild false, fleeZombies false, canThump false, canBePicked false; Gruppe buck hat keinen Angriff. Kein Eintrag in Migration, Hof, Geschichte, keine Zucht. Ton nur beim Aufschlag (der des Rehs).
* Lua-Pruefer: luacheck.py, scopecheck.py ok; localcount hoechstens 21; luacheck_pz 6 Treffer W113, alle der neue eigene Global `NCBearMenu`, gesetzt mit `or {}` in derselben Datei. Neue Globale: `NCBearMenu`, `NCBear_SpawnLive`. Jeder Engine-Aufruf mit Vanilla-Fundstelle als Kommentar (DebugContextMenu.lua:250-280, :615-623, :1462-1471; ISWorldObjectContextMenu.lua:683-689; ISAnimalContextMenu.lua:90; ISAnimalUI.lua:65). Alle Dateien ASCII, LF. Nichts laeuft je Bild.

## Vorschau

`baer_gang.mp4` (250 Bilder, 1024x576): 3 s Walk, 2 s Run (Kamera faehrt mit, Kachelraster am Boden), Sturz, liegen. Gerendert aus den Daten, die Assimp mit den Schritten des Spiels liest. Einzelbilder: `lebend_gang.png`, `lebend_gang_seite.png`, `lebend_nah.png`, `lebend_sturz.png`, `lebend_liegend.png`, `lebend_rueckfall_reh.png` (`lebend_galopp_seite_alt.png` ist ein Zwischenstand vor der letzten Galopp-Korrektur). Angesehen: kein gerissenes Knie, keine zerrissene Schulter, Kopf dreht richtig. Sichtbare Falten an Ellbogen und Achsel im Schwung.

## Was unsicher bleibt

1. **Nicht gespielt.** `.glb` im Tierweg benutzt Vanilla nie (nur Tueren); Lader und Haut sind dieselben und offline gemessen, das Bild im Spiel (animalEffect, Texturweg) nicht.
2. Groesse: ob die Engine den Tierkoerper noch skaliert, ist ungeprueft (spez 2.5). Nachstellen ohne Neustart: `animal:getData():setSizeForced(x)`.
3. Helligkeit: Textur ist fuer das Bodengegenstand-Licht hell gebacken; animalEffect rechnet gleich (Textur x min(Licht,1)), das Kachellicht ist ungeprueft.
4. Galopp: ein Bild des linken Hinterbeins ist 3,7 cm zu kurz (im Schwung, Pfote schwebt), Gleiten bis 0,05 Kacheln je Stuetze. Tempo 3,17 Kacheln/s ist meine Wahl, das Reh rennt 5,39.
5. Hautdehnung an Handgelenk, Ellbogen, Achsel (Werte oben): im Bild Falten, kein Riss. Liegend am staerksten.
6. Rueckfall sieht nach Reh im Baerenfell aus: federnd, Kopf hoch, Pfoten bis 9 cm im Boden, die Leiche halb im Boden.
7. Mehrspieler: ob der Server die `.glb` laedt (er rechnet den Weg), ist ungeprueft (spez 6.3). Erst Einzelspieler.
8. Treffer am lebenden Baeren: die Reaktion spielt Idle01 einmal ganz, also 3,2 s.
9. Ohne -debug fehlt das Debug-Menue; das eigene Menue geht trotzdem (nur Einzelspieler).

## Nachbesserung nach `pruefung_lebend.md` (07.11.)

* Fund 1 (ernst): Satz oben berichtigt; die Konsolenzeile von "Remove living bears nearby" sagt jetzt, dass Leichen und
  weiter entfernte Baeren bleiben (`NCBearSpawn.lua`, nur Text). Kein Leichen-Entferner: Wegwerf-Spielstand deckt es, und
  eine Leiche im Inventar erreichte er ohnehin nicht.
* Fund 2 und 3 (klein): Tierzone und Rehteile oben und in `anleitung_lebend.md`. Fund 4: Zahl in "Zahlen" nachgetragen.
* Danach: vier Lua-Pruefer gruen (luacheck_pz nur die 6 W113 auf den eigenen Global `NCBearMenu`), `Probe.java` auf beide
  GLB unveraendert (5 Clips, 25 bzw. 40 Knochen). Alle 8 Dateien aus `tier_mod/42` in einem Zug nach `NCBearTest/42`,
  byte-gleich nachgezaehlt; stehendes Modell, Item, `nc_bear.txt`, `WorldItems/*` unberuehrt. `mod.info` (beide):
  Beschreibung nennt das lebende Tier. Das Spiel lief beim Kopieren nicht.
* `setSizeForced(float)` (ButcheringUtil.lua:569, Jar: schreibt `size` ohne Klemme) haelt, bis `AnimalData.growUp` beim
  naechsten Alterstag `setSize` mit Klemme auf 1,0 ruft (`AnimalData.update` Offset 112, `growUp` Offset 130).

Statisch geprueft und offline gemessen, nicht gespielt.
