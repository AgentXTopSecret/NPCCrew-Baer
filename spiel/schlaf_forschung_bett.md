# Forschung Baerenbett (Lauf baer-schlaf, Thema Bett)

09.11.2026. **Nur gelesen und gerechnet (CPU, numpy/Pillow), nichts gebaut, nichts gerendert, nichts heruntergeladen, keine
Mod-Datei geaendert. Statisch geprueft, nicht gespielt.** Alle Laufzeit-Aussagen sind Vermutungen mit Beleg, sonst "ungeprueft".

Eigene Dateien: `_arbeit/baer_schlaf/bett/` -- `mess_umriss.py` (Umriss je Clip), `bild_draufsicht.py` (Draufsicht mit
Kachelraster), `glb.py` (Kopie des GLB-Lesers aus `_arbeit/baer_anim/pruef/glb.py`), Ergebnisse `umriss_ncbeartest.json`,
`masse_135.json`, Bild `draufsicht_135.png`, Jar-Auszug `jar/cls*`, Vineflower-Ausgabe `jar/dec*`.
Gemessen am GLB der Test-Mod `Zomboid/mods/NCBearTest/42/media/models_X/Skinned/NCBear.glb` (Stand baer-anim). Der Lauf baer-fell
aendert nur Netz/Textur um Zentimeter (Clips bit-gleich, `_arbeit/baer_fell/bau_netz.md:17`), fuer den Umriss ohne Belang.

---

## 0. Ergebnis in Kuerze

* **Groesse:** der erwachsene Baer (1,35) liegt (Naeherung Clip `DeerStag_Dead`) auf **2,07 x 1,19 Kacheln** (2,54 x 1,45 m), steht
  auf 2,14 x 1,07 Kacheln. **Vorschlag Bett: aussen 2,5 x 1,5 Kacheln (3,06 x 1,84 m), Liegeflaeche innen 2,34 x 1,34 Kacheln**,
  Rand 0,13 Kacheln (16 cm) an den Enden, 0,08 (10 cm) an den Seiten. Auf dem Raster belegt das **2 x 3 Kacheln** (je 0,25 Luft).
  Die endgueltige Zahl kommt aus dem echten Schlaf-Clip (ein Befehl, Abschnitt 1.4).
* **Bester Weg: (a) 3D-Bodengegenstand** `NPCCrew.BearBed` (Weg wie Turret, Rucksack-Bodenmodell und die Baeren-Statue der
  Test-Mod), gebaut per Handwerksrezept (Schreinerei), aufgestellt und gedreht mit Vanillas "Auf den Boden stellen", aufheb- und
  versetzbar wie jeder Gegenstand. Keine eigenen Kacheln, kein `tiledef`, alle Engine-Aufrufe belegt.
* **Spaeter moeglich:** dasselbe Bett zusaetzlich im Rechtsklick-**Bau-Menue** (B42-Entity mit Vanilla-Platzhalter-Sprite, dessen
  `OnCreate` das 3D-Bett hinlegt -- Vorbild Futtertrog und NPC-Crew-Beacon). Eigene Kacheln (.tiles/.pack) lohnen nicht.
* **Risiken:** Bodengegenstaende greift NPC Crews Foersterin/Pluenderer (Naehte wie Turret #39/#40); Verdecken an Waenden ist
  ungesehen; der Schlaf-Clip muss in die Liegeflaeche passen (Vorgabe fuer den Anim-Forscher: bei Groesse 1,0 hoechstens
  1,15 x 0,66 E Bodenumriss in Bettrichtung).

---

## 1. Groesse

### 1.1 Masseinheiten (Belege)

| Groesse | Wert | Beleg |
|---|---|---|
| Modell-Einheit E je Meter | 0,544 E = 1 m (MaleBody 0,98 E = 1,8 m) | `NPCCrew-Nebenprojekte/CLAUDE.md` Abschnitt 8; `baer/spiel/anim_review_optik.md:12` |
| Kacheln je E | **1 E = 1,5 Kacheln**, also 1 Kachel = 0,667 E = **1,225 m** (Spielfigur 1,8 m = 1,47 Kacheln) | `Core.DoPushIsoStuff` `scale(-1.5, 1.5, 1.5)` (`turret/T1b_bau.md:52`, `turret/T1_modelldaten.md:77`), `baer/spiel/bau_lebend.md:48`, `anim_clips.md:96` |
| Bodengegenstand | 1 Blender-Meter x `scale` 0,544 = 0,544 E = 0,816 Kacheln | `turret/T1_modelldaten.md:77`; `NCBearTest/42/media/scripts/nc_bear.txt` (`scale = 0.544`) |
| Tier-Groesse im Bild | gleichmaessig `FinalScale = AnimalData.getSize()` | `baer/spiel/tier_spez.md:184` (ModelSlotRenderData 452-455) |
| Tier-Modellskript | ohne `scale`, GLB-Einheiten = E | `NCBearTest/42/media/scripts/nc_bear_tier.txt:9-15` |

### 1.2 Messung (Haut des GLB, Wurzelbewegung `Translation_Data` abgezogen)

`python -B mess_umriss.py <glb> umriss_ncbeartest.json`, `python -B bild_draufsicht.py <glb> draufsicht_135.png masse_135.json`.
Rechteck = kleinstes umschliessendes Rechteck am Boden (x quer, z laengs, Kopf +z).

| Pose | bei 1,0 (E) | bei **1,35** (Kacheln) | bei 1,35 (m) | Mitte der Pose gegen Tier-Ursprung (Kacheln quer/laengs) |
|---|---|---|---|---|
| Stehen `DeerStag_Idle01` | 1,058 x 0,528 | **2,14 x 1,07** | 2,62 x 1,31 | 0,00 / +0,19 |
| Liegen `DeerStag_Dead` (Naeherung Schlaf) | 1,019 x 0,561 (Achse 6 Grad gedreht) | **2,07 x 1,19** | 2,54 x 1,45 | -0,14 / +0,16 |
| Sitzen `NCBear_Sit` | 0,823 x 0,703 | 1,87 x 1,56 | 2,30 x 1,92 | 0,00 / +0,19 |
| Fressen `NCBear_Eat` | 0,99 x 0,528 | 2,00 x 1,07 | -- | -- |

Tiefster Hautpunkt im Liegen 0,0000 E (der Clip liegt auf dem Boden, deckt sich mit `_arbeit/baer_fell/bau_netz.md:75`). Hoechster
Punkt im Dead-Bild ist das Becken (0,523 E = 0,96 m bei 1,0): `DeerStag_Dead` ist eine Reh-Pose, kein Baeren-Schlaf -- nur fuer den
Umriss tauglich. Sitzen ist breiter als das Bett (Hinterbeine gespreizt); Sitzen ist kein Schlafen, haengt dann ueber den Rand.

### 1.3 Vorschlag und Kachelzahl

* Liegeflaeche innen = Schlaf-Umriss bei 1,35 + rund 0,12 Kacheln je Seite -> **2,34 x 1,34 Kacheln**; Rahmen 0,08 Kacheln (10 cm) je
  Seite -> **aussen 2,5 x 1,5 Kacheln = 3,06 x 1,84 m = 1,67 x 1,00 E**.
* Raender mit Dead bei 1,35, Pose mittig: 0,13 Kacheln an jedem Ende, 0,08 an jeder Seite (`masse_135.json`). Stehen: 0,10 / 0,14.
* **Kacheln:** 1x2 und 2x2 sind zu klein (Baer 2,07 lang). Die 2,5 x 1,5 belegen **2 x 3 Kacheln**, wenn die Bettmitte laengs auf
  einer Kachelmitte und quer auf einer Kachelkante liegt (dann je 0,25 Luft). Liegt die Mitte quer auf einer Kachelmitte, ragt das
  Bett 0,25 in die dritte Kachelreihe. Wer das Raster ganz fuellen will: 3,0 x 2,0 Kacheln (3,67 x 2,45 m) -- dann liegt der Baer
  aber verloren darin ("perfekt drauf passen" spricht fuer 2,5 x 1,5). **Kevins Wort.**
* Jungtier (0,35) und Halbstark (0,75) liegen mittig im selben Bett, ein Bett fuer alle Groessen. Groesser als 1,35 (etwa ein
  spaeteres Gen oder eine Sandbox-Option) passt nicht mehr.
* **Liegepunkt:** damit die Pose mittig liegt, steht der Tier-Ursprung nicht in der Bettmitte, sondern 0,16 Kacheln zum Schwanz und
  0,14 zur Beinseite versetzt (Dead). Mit dem Ursprung in der Bettmitte ragt der Kopf 0,03 und die Rueckenseite 0,06 Kacheln ueber
  die Liegeflaeche (`masse_135.json`, `rand_wenn_ursprung_in_bettmitte`). Den Versatz liefert der echte Schlaf-Clip.

### 1.4 Abstimmung mit dem Schlaf-Clip (Anim-Forscher)

* **Vorgabe fuer den Clip:** Bodenumriss der Schlafschleife bei Groesse 1,0 hoechstens **1,15 x 0,66 E** (2,12 x 1,22 m), in
  Bettrichtung (Laengsachse = Blickrichtung des Tiers). Seitenlage und Bauchlage mit Kopf auf den Pfoten passen (Dead 1,02 x 0,56;
  Stehlaenge 1,06). **Knapp wird eine "Frosch"-Bauchlage mit nach hinten gestreckten Hinterbeinen** (geschaetzt +0,15 E, also
  rund 2,4 Kacheln bei 1,35, ungemessen) -- dann Bett 2,75 lang oder Pose anpassen.
* Sobald der Clip im GLB ist: `python -B mess_umriss.py <neues GLB>` (Wert der Schlafschleife ablesen, alle Bilder pruefen: dafuer
  `ts` im Skript auf alle Bilder stellen) und Bettmass = Umriss x 1,35 + 0,12 Kacheln je Seite + Rahmen.
* **Hoehe:** der Clip liegt auf dem Boden (z = 0). Kein Hoehenversatz am Tier vorschlagen (eine gebrochene z-Lage eines Tiers ist
  nirgends belegt). Darum **flach**: Strohoberflaeche 2-4 cm ueber dem Boden (der Baer sinkt so viel ins Stroh, sieht natuerlich
  aus), Rahmen 12-18 cm hoch AUSSEN herum (der Baer liegt "im" Bett, nicht "auf" einem Podest).

---

## 2. Wege fuer ein grosses aufstellbares Objekt in B42.21

### (a) 3D-Bodengegenstand (InventoryItem mit `WorldStaticModel`) -- EMPFOHLEN

* **Belegt im Projekt:** Turret (`turret/T1_plan.md:11-12, 145-155, 220-253`; Kevin hat es gesehen: unbeschnitten, richtige Lage,
  `turret/KEVIN_ENTSCHEIDUNGEN.md:23`), Baeren-Statue `NCBear.BearStatic` (`NCBearTest/42/media/scripts/nc_bear.txt`,
  `client/NCBearTest.lua:17-60`), Rucksack-Bodenmodelle `NPCCrew_CrewBackpack_Ground` (`rucksack/mod_neu_BERICHT.md:55`).
* **Aufrufe (alle Vanilla-belegt):** `square:AddWorldInventoryItem(item, x, y, z[, false])` (`ISDropWorldItemAction.lua:81`),
  `item:setWorldZRotation(zahl)` (`ISDropWorldItemAction.lua:83`), `getWorldItem():setIgnoreRemoveSandbox(true)` (:85, gegen den
  Aufraeumer), `getWorldItem():transmitCompleteItemToClients()` (:87, MP), Lesen `square:getWorldObjects()` /
  `obj:getItem()` / `item:getFullType()` (`ISWorldObjectContextMenu.lua:2973-2975`, `ISInventoryPaneContextMenu.lua:4290`),
  Lage `obj:getWorldPosX/Y/Z()` (`client/Foraging/ISSearchManager.lua:501-503`), Drehung `item:getWorldZRotation()`
  (`ISExtendedPlacementUI.lua:160`, so zitiert in `NCBearTest/42/media/lua/client/NCBearTest.lua:81`).
* **Aufstellen durch den Spieler ohne eigenen Code:** jedes Item mit `WorldStaticModel` bekommt "Place item on ground"
  (`ISInventoryPaneContextMenu.lua:4420-4436`, Bedingung `getWorldStaticItem()`), mit Drehgriff und Verschieben
  (`ISExtendedPlacementUI.lua:429-454`); die Aktion setzt Aufraeum-Riegel und sendet an alle (`ISDropWorldItemAction.lua:81-87`).
  Aufheben/Versetzen: Vanillas Aufheben, dann neu hinstellen.
* **Zeichnen:** Atlas bis 512 Pixel, darueber `tooBig` -> echtes 3D je Bild; nicht beschnitten (`baer/spiel/bau_stehend.md:64-71`).
  Bett 2,5 x 1,5 Kacheln: rund (2,5+1,5) x 64 = 256 x ~140 Pixel bei Zoom 1 (Raster +1 X = (+64,+32) Pixel,
  `turret/T1_modelldaten.md:69`), mit "High-res placed items" x 2,5 = 640 -> dort Direktweg, sonst Atlas. Der Atlas ist Vanillas
  Normalweg (das Turret lief am 06.11. darueber in richtiger Lage, `turret/KEVIN_ENTSCHEIDUNGEN.md:23`), der Direktweg legt den
  Ursprung seit T1b ebenfalls richtig auf den Boden (`turret/T1b_bau.md:14-21, 57`); ob beim Zoomwechsel zwischen beiden ein
  Versatz oder Lichtsprung sichtbar ist: **ungeprueft**. Wer jeden Zoom gleich will: Streupunkt wie das Turret (immer Direktweg,
  `turret/T1_plan.md:80`, im Spiel bewaehrt). Bauentscheidung.
* **Nachteile/Risiken:** (1) Das Modell ragt ueber seine Kachel hinaus und auch durch Waende (`turret/T1_modelldaten.md:114`);
  Verdecken an Waenden ist ungesehen (`baer/spiel/bau_stehend.md:73`). (2) Ein Bodengegenstand ist fuer NPC Crew Beute: Foersterin
  sammelt jeden Bodengegenstand ihrer Pflanzflaeche (`turret/NAEHTE.md:54` (a)), Pluenderer fragt nur `^NCTurret%.`
  (`NPCCrew/42/media/lua/shared/BanditsNPCSiteRules.lua:926-929`), Farmer graebt darunter (`turret/NAEHTE.md:54` (d)). (3) Der
  Spieler kann das Bett im Platzier-Fenster anheben oder kippen (z-Regler, Drehgriff, `ISExtendedPlacementUI.lua:30-32, 429`);
  der Baer nimmt dann nur Betten am Boden (Abschnitt 3.3). (4) Keine Kollision -- fuer ein flaches Bett gewollt.
* **Aufwand:** klein bis mittel (Modell + Skript + Rezept + Lua fuer "Baer findet Bett"). Kein `tiledef`, keine neue Engine-Art.

### (b) Moebel/Moveable mit eigenen Kacheln (.tiles/.pack)

* Vanilla-Moebel sind Kachel-Sprites mit Eigenschaften, mehrteilig ueber `SpriteGridPos`; das Vanilla-Bett `carpentry_02_72..75`
  hat `CustomName = Bed`, `IsMoveAble`, `PickUpTool = Hammer`, `PickUpWeight = 75`, `SpriteGridPos`
  (`media/newtiledefinitions.tiles.txt:19906-19925`); die Matratze ist ein Moveable-Item mit `WorldObjectSprite = carpentry_02_76`
  (`scripts/generated/items/moveable.txt:2379-2388`).
* Eigene Kacheln brauchen `pack=` und `tiledef=<name> <nummer>` in `mod.info`; die Nummer muss zwischen 100 und 8189 liegen und
  ueber ALLE Mods eindeutig sein (`ChooseGameInfo`, Vineflower `bett/jar/dec/zombie/gameStates/ChooseGameInfo.java:260-313`). Das
  Spiel laedt nur die binaere `.tiles` (Kennung `tdef`, `media/newtiledefinitions.tiles` Byte 0-3; `IsoWorld` enthaelt
  `LoadTileDefinitions`); eine `.tiles.txt` laedt die Laufzeit nicht (Jar-Suche nach "tiles.txt" in `zombie/*`: kein Treffer).
* Dazu 2D-Sprites je Richtung und Kachel (2 x 3 Kacheln x 4 Richtungen = 24 isometrische Bilder), gepackt in eine `.pack`. Werkzeug
  waere TileZed/Pack-Ersteller (Download, Kevins Ja je Datei) oder ein eigener Schreiber nach Jar-Lesung (ungeprueft).
* **Nachteile:** grosser Aufwand, Nummern-Kollision mit fremden Mods, neue `mod.info`-Zeilen in NPC Crew (Naht). Ein `bed`-Flag
  waere sogar schaedlich: NPC Crews Figuren und Spieler wuerden darin schlafen (`NPCCrew/42/media/lua/shared/BanditsNPCBase.lua:196-203`
  `P.sleepable` fragt `IsoFlagType.bed`). Bandits und alle Mods unter `Zomboid/mods` haben kein `tiledef` (grep).
* **Urteil:** nicht lohnend.

### (c) B42-Entities / Bau-Menue

* Format belegt: `entity` mit `SpriteConfig` (Gesichter N/E/S/W, `row = ...` je Kachelreihe) und `CraftRecipe` (Werkzeug, Material,
  Fertigkeit) -- Vanilla-Bett `Wood_Bed` 2 Kacheln, Woodwork 4, 6 Bretter, 4 Naegel, 1 Matratze
  (`scripts/generated/entities/furniture/entity_carpentry_bed.txt:3-45`); mehrteilig bis 3 breit (`entity_forge_iii.txt:23-34`).
  `Tags = Carpentry;Furniture` setzt es ins Rechtsklick-Bau-Menue (NPC Crew `42/media/scripts/entity_tcbeacon.txt:29-31, 136-137`).
  Haken: `OnIsValid` (`ISBuildIsoEntity.lua:177-178`) und `OnCreate` (`ISBuildIsoEntity.lua:740-760`, SP auf dem Rechner, MP auf
  dem Server laut `entity_tcbeacon.txt:114-118`).
* **3D an Kacheln gibt es in B42:** `media/spriteModels.txt` haengt Vanilla-Kacheln an Modellskripte (Tueren, Radios, Toiletten,
  Waschmaschinen, `carpentry_01`), **das Vanilla-Bett nicht**. Mods duerfen eine eigene `common/media/spriteModels.txt` liefern
  (`SpriteModelManager.init`, Vineflower `bett/jar/dec/zombie/spriteModel/SpriteModelManager.java:30-42`), sie bindet aber nur an
  vorhandene Sprites (`SpriteModelsFile$Tileset.initSprites`, `bett/jar/dec2/.../SpriteModelsFile$Tileset.java:48-59`:
  `IsoSpriteManager.namedMap.get(name)`, sonst nichts) -- also wieder eigene Kacheln wie (b). Nur Jar, im Spiel ungeprueft.
* **Mischform (c+a), alles belegt:** Entity `NPCCrewBearBed` im Bau-Menue mit einem Vanilla-Platzhalter-Sprite (z. B. Heuballen
  `vegetation_farm_01_16/17/8/9`, alle vier Seiten: `entity_haybundles.txt:20-49`); `OnCreate` entfernt den Platzhalter
  (`thumpable:removeFromWorld()`, `removeFromSquare()`, `square:transmitRemoveItemFromSquare(thumpable)`, Vorbild
  `server/BuildRecipeCode/buildRecipeCode.lua:492-494`) und legt das 3D-Bett aus (a) hin (`AddWorldInventoryItem` + Drehung aus
  `params.facing`, `ISBuildIsoEntity.lua:741-743`), Rueckgabe `{ objectAlreadyTransmitted = true }` (`buildRecipeCode.lua:498`).
  `OnIsValid` prueft die ganze Bettflaeche. Vorteil: Bauen wie Moebel. Nachteil: der Bau-Cursor zeigt einen Heuballen, nicht das
  Bett; mehr Code; der Heuballen traegt `bed`/`BedType = badBed` (`newtiledefinitions.tiles.txt:233984-233999`) -- nur waehrend
  des Cursors, aber pruefen. **Erst nach (a), auf Kevins Wort.**

### (d) Was Vanilla fuer Tiere hat (Vorbild)

* **Kein Tierbett.** Kachel-Namen mit Hay/Straw/Dog/Pet/Nest/Kennel/Trough/Mattress: nur Trog (24), Schlafsaecke, Matratze,
  "Single/Double Stacked Hay" (Ballen, `BedType = badBed`, `:233925-233941`, `:233984`), "Hay Floor" (`vegetation_farm_01_12/13`,
  `MoveType = FloorRug`, `attachedFloor`, `solidfloor`, Schaufel, `:233956-233983`) (grep `CustomName` in
  `newtiledefinitions.tiles.txt`).
* **Futtertrog:** Entity mit `OnCreate = BuildRecipeCode.feedingTrough.OnCreate` (`entity_feedingtrough.txt:13`), die den Bau in
  ein Objekt des globalen Objektsystems verwandelt (`buildRecipeCode.lua:476-498`, `server/FeedingTrough/SFeedingTroughSystem.lua:7-22`:
  `SGlobalObjectSystem`, gespeicherte und synchronisierte Felder). Das ist Vanillas MP-feste Art fuer "Objekt mit Zustand".
* **Stall (Hutch):** nur fuer Kleintiere, das Tier verschwindet hinein (`animal:needHutch()`, `getHutch()`,
  `client/ISUI/Animal/ISAnimalUI.lua:15-25, 317`); Bau-Code ersetzt das Objekt (`buildRecipeCode.lua:473`). Fuer den Baeren nicht passend.
* **Heu:** `Base.HayTuft` (`items/food.txt:624-635`, Tierfutter) aus dem Trockengestell (`entity_Herb_Drying_Rack_craftRecipe.txt:387-401`,
  Gras -> Heu) oder vom Heuballen (`ContextMenuCode.TakeHay`, `client/ContextMenuCode.lua:117`).

---

## 3. Wie bekommt der Spieler das Bett, und wie findet der Baer es

### 3.1 Bauweg (keine Cheat-Menues)

**Vorschlag A (zu (a)): Handwerksrezept** in `category = Carpentry` (Form `MakeWoodenToolbox`, `recipes_carpentry.txt:296-317`):

```
craftRecipe MakeNPCCrewBearBed      (Name frei: grep NPC Crew, Vanilla, NCBearTest = 0)
  timedAction = Making, time = 300, Tags = AnySurfaceCraft;Carpentry, category = Carpentry,
  xpAward = Woodwork:15, SkillRequired = Woodwork:2,
  inputs  item 1 tags[base:hammer] mode:keep flags[MayDegradeVeryLight]   (recipes_carpentry.txt:306)
          item 8 [Base.Plank]                       (items/weapon.txt:8855)
          item 12 [Base.Nails]                      (items/normal.txt:3414)
          item 30 [Base.HayTuft]                    (items/food.txt:624)
          item 2 [Base.Sheet;Base.Leather_Crude_Large]  (normal.txt:10516, :114; Alternativliste wie recipes_camping.txt:13)
  outputs item 1 NPCCrew.BearBed
```

Zahlen sind ein Vorschlag (Vanilla-Bett: Woodwork 4, 6 Bretter, 4 Naegel, 1 Matratze). `Base.Mattress` als Eingang waere auch
moeglich (`recipes_tailoring.txt:64-82`). Fell vom Baeren selbst: es gibt kein Baerenfell-Item (grep), also nur Vanilla-Leder.
**Kevins Wort** zu Material und Fertigkeit.

**Vorschlag B (spaeter, zu (c+a)):** dasselbe als Bau-Menue-Eintrag (`Tags = Carpentry;Furniture`, `category = Furniture`).

* **Gegenstand:** `NPCCrew.BearBed` (Modul `NPCCrew` wie `NPCCrew.CrewBackpack`, `rucksack/mod_neu_BERICHT.md:46`), Bodenmodell
  `NPCCrew_BearBed_Ground` in `module Base` (`mod_neu_BERICHT.md:55-57`), Icon `textures/Item_NPCCrew_BearBed.png`, FBX
  `models_X/WorldItems/NPCCrew_BearBed_Ground.fbx`. **Name fuer immer stabil.** Frei geprueft (grep, 0 Treffer) in
  `NPCCrew/42`, `NPCCrew/common`, Vanilla `media/scripts` + `media/lua`, Bandits `42.21` + `common`, `NCBearTest/42`: `BearBed`,
  `NPCCrew_BearBed`, `NPCCrewBearBed`, `ES_NPCCrewBearBed`, `BanditsNPCBearBed`, `UI_BN_Bear_Bed`, `MakeNPCCrewBearBed`, `BuildBearBed`.
* Gewicht Vorschlag 15 (Matratze 8,0: `moveable.txt:2382`), `DisplayCategory = Furniture`.
* Texte: Name in `Translate/<L>/ItemName.json` (Schluessel `NPCCrew.BearBed`, Form Zweihaender), Rezept in `Recipes.json`
  (Vanilla-Form `"MakeMattress": "Sew Mattress"`, `Translate/EN/Recipes.json:960`), Tooltip `Tooltip_BN_Bear_Bed` in
  `Tooltip.json`, Meldungen `UI_BN_Bear_Bed*` in `UI.json`, je sieben Sprachen. NPC Crew hat heute nur `Sandbox.json`,
  `Tooltip.json`, `UI.json` -> `ItemName.json`/`Recipes.json` sortiert zusammenfuehren, wer zuerst kommt legt an (Naht wie
  Zweihaender/Rucksack, CLAUDE.md 7).
* Testhilfe "Bett hinlegen" nur in `NCBearBench*.lua` (nie kopieren).

### 3.2 Aufheben und Versetzen

(a): Vanillas Aufheben und "Place item on ground" -- nichts zu bauen. Der Baer merkt sich keine Gegenstands-Id, sondern sucht
neu (3.3), darum bricht ein versetztes Bett nichts. (b)/(c) mit Kacheln: Moveable-Aufheben mit Hammer (Vanilla-Bett
`PickUpTool = Hammer`) -- nur mit eigenen Kacheln.

### 3.3 Wie der Baer sein Bett findet (SP und MP)

* **Ohne Register (Vorschlag fuer den Anfang):** wenn der Baer schlafen will (selten, nicht je Bild), sucht der Rechner, der den
  Baeren fuehrt, im Umkreis R (z. B. 25 Kacheln um Zuhause/Besitzer; Deckel (2R+1)^2 = 2.601 Kacheln, einmal je Entscheidung)
  nach Bodengegenstaenden `NPCCrew.BearBed` -- Suchform wie `NCBearTest/42/media/lua/client/NCBearTest.lua:44-60`
  (`getCell():getGridSquare`, `getWorldObjects`, `getItem():getFullType()`). Gueltig nur, wenn: liegt am Boden
  (`getWorldPosZ()` gleich der Ebene, Toleranz wenige cm), alle Kacheln unter der Bettflaeche (Rechteck nach
  `getWorldZRotation()` gedreht, Stichpunkte alle 0,25 Kacheln) frei und ohne Wand dazwischen -- Pruefung wie `flyOk`
  (`NCBearTest/42/media/lua/shared/NCBearFight.lua:707-718`, jede Zeile mit Vanilla-Fundstelle: `TreatAsSolidFloor`, `HasStairs`,
  Wasser, `isSolid`/`isSolidTrans`, `isFree(false)`, `isBlockedTo`, `isWindowTo`), und kein anderer Baer liegt darauf.
* **Merken:** Lage und Drehung des gewaehlten Betts im Baeren-Gedaechtnis (wo der Baer seine Daten speichert, legt B1/PLAN fest);
  bei der naechsten Nacht erst dort nachsehen, sonst neu suchen.
* **MP:** Aufstellen/Aufheben sind Vanilla-Aktionen mit Server-Sendung (`ISDropWorldItemAction.lua:81-87`). Soll mehr als ein
  Rechner wissen, welches Bett wem gehoert, dann ein Register wie NPC Crews Beacon: globale ModData, Client fragt, Server prueft,
  schreibt und sendet (`NPCCrew/42/media/lua/shared/BanditsNPCBeaconRegistry.lua:20-47`; Vanilla `ModData.getOrCreate`
  `server/Foraging/forageServer.lua:26`, `ModData.transmit` `:49`). Schluessel `x,y,z` (`R.KeyFor`, `:50-52`). Wer den Baeren im
  MP fuehrt, ist im Projekt noch offen (STAND.md: MP zuletzt) -> **MP offen**.
* **Hinlegen:** hinlaufen wie jeder Baeren-Gang (`pathToLocation` am Tier: `begleiter/PLAN.md:200, 304, 334` -- Jar-Lage dort
  beschrieben), am Liegepunkt (1.3) in Bettrichtung drehen. Drehen: `faceThisObject` am Tier belegt (`ISPetAnimal.lua:17`, so
  benutzt in `NCBearFight.lua:428`), `faceLocationF(x, y)` nur am Spieler belegt (`client/BuildingObjects/TimedActions/ISBuildAction.lua:248`),
  am Tier gleiche Java-Methode -- **im Bau belegen oder Kevins Wort**. Feinsetzen per `setX/setY` ist am Zombie belegt (Bandits
  `ZAMove.lua:12/17`), am Tier nicht -- ebenso.
* **"Schlafen wie die NPCs" (spaeter):** NPC Crew schlaeft im Fenster 22-7 Uhr bei Muedigkeit >= 30 bzw. bricht bei >= 90 ein
  (`NPCCrew/42/media/lua/shared/BanditsNPCRoutine.lua:224-249`); Bett = Objekt mit `IsoFlagType.bed`, ohne Stuehle
  (`BanditsNPCBase.lua:196-240`), dazu ein manueller "Set bed"-Cursor (`BanditsNPCBase.lua:649`) und Bettsuche/Schlafbefehl
  (`client/BanditsNPCSleep.lua:483-528`, Landkarte `findNearbyBed`, `SleepHere`). Fuer den Baeren dieselbe Form,
  aber eigener Typ: das Baerenbett hat bewusst KEIN `bed`-Flag (sonst legen sich Crew-Figuren hinein).

### 3.4 Naehte zu NPC Crew (nur fuer Weg (a))

Je ein Aufsatz in `OnGameBoot` in einer Baeren-Datei, keine NPC-Crew-Datei geaendert (Vorbild `turret/NAEHTE.md` #39/#40):
1. Foersterin: `BanditsNPC.Forestry.PolicyIn` / `.NoteIn` -> `NPCCrew.BearBed` immer "leave" (`turret/NAEHTE.md:54` (a)).
2. Pluenderer: `BanditsNPC.SiteRules.LootTypeRefused` einpacken -> `"bearbed"` fuer `NPCCrew.BearBed`
   (`BanditsNPCSiteRules.lua:926-929`, heute nur `^NCTurret%.`). Oder, weil das Bett nach der Uebernahme Teil von NPC Crew ist,
   eine Zeile dort -- dann als Naht-Zeile im Uebernahme-Skript fuehren.
3. Pflanzen/Graben auf Bettkacheln: `F.Blocked` / `Fm.DigOk` (`turret/NAEHTE.md:54` (d)).
4. MP-Nehm-Tuer ohne Typpruefung (`turret/NAEHTE.md:54` (e)) -- gleiche Grenze wie beim Turret.

---

## 4. Aussehen und Modell-Kette (nur Idee)

* **Form:** flaches Strohlager in einem niedrigen Rahmen aus vier groben Balken/Brettern (12-18 cm hoch, Ecken mit Seil
  gebunden), Stroh/Heu innen 2-4 cm ueber dem Boden, am Rand leicht aufgehaeuft, am Kopfende eine alte Decke oder ein Leder halb
  ueber das Stroh gelegt, ein paar Halme ausserhalb. Farben: warmes Strohgelb, dunkles Holz, rotbraune Decke. Aussen 3,06 x
  1,84 m (Blender-Meter), Liegeflaeche 2,86 x 1,64 m. Optional ein eingeschnitztes "BEAR"-Brett am Kopfende (wie der Aufnaeher
  am Rucksack) -- bei der Texturdeckelung 256 (CLAUDE.md 8) aber kaum lesbar; Kevins Wort.
* **Kette** (Vorbild `rucksack/spiel_b/spiel_b.py:1-20`, Turret-Export `turret/T1_plan.md:145-146`): ein Skript
  `baer/bett/bett_bau.py -- alles` in Blender 5.2.3 `--background --factory-startup`: (1) Modell prozedural (Balken, Strohflaeche
  mit Rauschen, Halmbueschel, Decke), Ziel 1.500-3.000 Dreiecke; Laengsachse = Blender +X (Turret: Mesh +X -> Welt (cos a, sin a)
  bei Drehung a, `turret/T1b_bau.md:53`), Ursprung = Mitte der Liegeflaeche auf z = 0. (2) UV, Stroh als wiederholte Inseln auf
  demselben Texturfeld (traegt auch bei 256). (3) Backen Farbe + AO in 512 (OPTIX nur auf der 4090 und nur, wenn PZ nicht laeuft,
  `tasklist`). (4) FBX `axis_forward="-Z"`, `axis_up="Y"`, `apply_scale_options="FBX_SCALE_ALL"` (CLAUDE.md 8), Material ohne
  Bildpfad (Rucksack-Lehre `spiel_b.py:10-11`), optional Streupunkt. (5) Icon 32x32. (6) Pruefung offline: Masse gegen den
  Schlaf-Umriss (`mess_umriss.py`), Draufsicht mit dem Baeren darauf (`bild_draufsicht.py` erweitern).
* **Skript-Zeilen (Form `nc_bear.txt`, Rucksack):** `model NPCCrew_BearBed_Ground { mesh = WorldItems/NPCCrew_BearBed_Ground,
  texture = WorldItems/NPCCrew_BearBed, scale = 0.544, }` in `module Base`; `item BearBed { DisplayCategory = Furniture,
  ItemType = base:normal, Weight = 15, Icon = NPCCrew_BearBed, WorldStaticModel = NPCCrew_BearBed_Ground, Tooltip = ... }` in
  `module NPCCrew`.

---

## 5. Offen / ungeprueft

1. Endmass haengt am Schlaf-Clip (1.4). Heute nur Dead als Naeherung.
2. Verdecken an Waenden und Nachbarkacheln bei einem 2,5 x 1,5 grossen Bodenmodell: ungesehen (bau_stehend.md:73).
3. Ob der Baer auf dem Bett natuerlich aussieht (Stroh 2-4 cm verdeckt die Unterseite): ungesehen; Tiefe des Atlasbilds gegen das
   Tier ungeprueft.
4. Ob "Place item on ground" bei einem so grossen Modell Grenzen hat (Ablageflaeche, Reichweite): ungeprueft.
5. MP: wer den Baeren fuehrt und wo er sein Bett speichert -- offen bis B1/MP.
6. Mischform (c+a): ob der Heuballen-Platzhalter mit `bed`-Flag im Bau-Cursor stoert; ob `OnCreate` im MP sicher auf dem Server
   laeuft (Kommentar NPC Crew, nicht selbst im Jar gelesen).
7. `faceLocationF` und `setX/setY` am Tier: nur an Spieler/Zombie belegt.
