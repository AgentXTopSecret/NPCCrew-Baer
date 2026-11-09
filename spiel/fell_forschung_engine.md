# Lauf baer-fell, Forschung B: Grenzen der Engine fuer das Tiermodell

Stand 08.11.2026, PZ 42.21. Nur gelesen, nichts geaendert. **Statisch geprueft, nicht gespielt.**
Belege: Jar-Klassen mit `javap -c -p` (Offset = Bytecode-Offset in der Methode), zum Lesen zusaetzlich mit Vineflower
entpackt. Vanilla-Dateien mit Zeile. Arbeitsdateien: `_arbeit/baer_fell/forschung_engine/` (`jar/` Klassen, `dec/`
Dekompilat, `jp.sh` javap-Auszug je Methode, `texeldichte.py` Messung am Spiel-GLB, `liste.py`/`ziehen.py`).

---

## 1. Texturgroesse, "Max. Texturgroesse", Mipmaps

### 1.1 Ladeweg der Koerpertextur eines Tiers
1. `IsoGameCharacter.checkUpdateModelTextures` (Offset 20-31) -> `ModelInstanceTextureCreator.init(IsoGameCharacter)` ->
   bei `IsoAnimal` -> `init(AnimalVisual, ModelInstance)`. Dort wird der Pfad fest gebaut:
   `"media/textures/Body/" + animalVisual.getSkinTexture() + ".png"` (putfield `baseTexture` Offset 102) und **sofort mit
   `Texture.getSharedTexture(String)` geladen (Offset 134), also OHNE Groessen-Flag**.
   (Das Vorschau-Modell im UI geht ueber `AnimatedModel.renderMain` Offset 47 in dieselbe Methode.)
2. `Texture.getSharedTexture(String)` setzt nur Flag 4 (Kompression, falls an) und ruft `getSharedTexture(name, flags)`
   (Offset 0-18). Der Cache `s_sharedTextureTable` ist **nur nach dem Namen** geschluesselt: wer zuerst laedt, bestimmt die Flags.
3. Erst danach, beim Zeichnen, holt `SmartTexture.add(String)` die Datei mit `getTextureWithFlags` (Offset 2) =
   `ModelManager.getTextureFlags()` = `kompression | 128` (Offset 22-25). Das trifft aber den schon geladenen Eintrag aus Schritt 1.
4. Der Menschen-Zweig `init(HumanVisual, ...)` laedt dagegen gleich mit `getTextureWithFlags` (Offset 577). Nur Menschen
   (und Kleidung) werden also gedeckelt.

### 1.2 Wirkt "Max. Texturgroesse"?
* Deckel sitzt in `TextureID.limitMaxSize` (Offset 17-30): nur wenn `flags & 384` (128 oder 256) gesetzt ist; sonst bleibt das Bild,
  wie es ist. Groesse aus `Core.getMaxTextureSizeFromFlags` (128 -> Option, 256 -> Fahrzeug-Option, sonst 32768) und
  `getMaxTextureSizeFromOption` (1=256, 2=512, 3=1024, 4=2048, Tabelle Offset 1-53).
* Vorgabe der Option `maxTextureSize` ist **1 = 256** (`Core.<init>` Offset 1245-1251: `newOption("maxTextureSize",1,4,1)`),
  Auswahl im Menue `MainOptions.lua:647-661`, Tooltip `Translate/EN/UI.json:66` ("non-vehicle-model textures").
* **Ergebnis: Nein, fuer die Tier-Koerpertextur gilt der Deckel nicht** (Schritt 1 laedt ohne Flag 128). Eine 1024er bleibt
  1024, eine 2048er bliebe 2048, auch bei Kevins Einstellung (seine `options.ini` nicht gelesen, liegt ausserhalb der Suchorte;
  fuer das Tier egal). Das ist ein Nebeneffekt des Ladewegs, kein dokumentiertes Verhalten -- ein Patch koennte es aendern.
* Die fruehere Lehre (CLAUDE.md 8: "Vorgabe deckelt auf 256") gilt fuer Kleidung/Menschen, nicht fuer den Baeren.

### 1.3 Was im Spiel daraus wird
* Die Datei wird je lebendem Tier in eine eigene Render-Textur kopiert: `TextureCombiner.combine` (Groesse aus
  `getResultingWidth` = naechste Zweierpotenz der Quelle, Offset 39; `createTexture` Offset 11-75 `new Texture(w,h,16)` mit FBO).
  Speicher je Baer: 1024 -> 4 MB, 2048 -> 16 MB Grafikspeicher (RGBA8, ohne Mipmaps), dazu einmal die Quelle.
* **Mipmaps: keine.** Die Option `modelTextureMipmaps` (Vorgabe aus, `Core.<init>` Offset 1209-1213) hat **leere Zweige**:
  `ModelManager.getTextureFlags` Offset 15-18 (`ifeq 21` springt auf die naechste Zeile), `TextureCombiner.combine` Offset 815-821
  ebenso; `TextureCombiner.createMipMaps` wird nirgends aufgerufen (javap: nur die Definition). Die Render-Textur steht auf
  GL_LINEAR (9729) fuer Verkleinern und Vergroessern (`createTexture`). Folge: wenn mehr Texel als Bildpunkte auf dem Baeren
  liegen, flimmern feine Straehnen beim Bewegen (es werden nur 2x2 Texel je Bildpunkt gemischt).
* Kompression: Option `textureCompression` (Vorgabe aus, `Core.<init>` Offset 1197-1201; uebernommen in
  `GameWindow.mainThreadInit` Offset 180-206). Wenn an, wird die Quelle komprimiert (Block-Artefakte im feinen Fell), die Kopie nicht.

### 1.4 Vanilla zum Vergleich (`media/textures/Body`, Kopfzeilen gelesen)
| Tier | Groesse | Format |
|---|---|---|
| Cow_* / Bull_* / DeerStag / DeerDoe / DeerFawn / FarmPig / Sheep | **256 x 256** | RGB (nur `Sheep_Skinned`, `FarmPig_Skinned` RGBA) |
| Chicken / Turkey / Rabbit / Raccoon | 128 x 128 | RGB |
| Rat 64, Mouse 32 | | |
Netze: `CowBody.x` 670 Punkte / 1.044 Flaechen, `Bull_Body.x` 813 / 1.262, `DeerStag.x` 730 / 1.036. Kein Vanilla-Tier hat Alpha.

### 1.5 Lohnt 2048? (Messung)
`texeldichte.py` am Spiel-GLB (`NCBearTest/.../NCBear.glb`): 18.040 Dreiecke, 10.814 Punkte, 1 Netz, 26 Gelenke im Skin,
68 % der Texturflaeche belegt. **1024: im Mittel 589 Texel je Netzeinheit** (Median 595), ~630 Texel ueber die Koerperlaenge
(1,066 Einheiten). 2048 verdoppelt das.
Kevins Spielbild `kevin_rear_unterseite.webp` (Bildschirm 3840x2054 laut Ecke unten rechts, Bild auf 2000 px verkleinert):
Figur ~490 px hoch, aufgerichteter Baer ~450 px hoch -> rund 500 Bildpunkte je Netzeinheit (Schaetzung ueber MaleBody
0,98 Einheiten = Figur). Damit:
* 1024: ~1,2 Texel je Bildpunkt -- schon jetzt so fein wie der Bildschirm bei diesem Zoom.
* 2048: ~2,4 Texel je Bildpunkt -- ohne Mipmaps nicht schaerfer, sondern Flimmern; sichtbar besser erst bei doppelt so nahem Zoom.
  Beim Herauszoomen (z. B. halbe Groesse) 1024: ~2,4, 2048: ~4,7 Texel je Bildpunkt -> deutliches Rauschen.
**Empfehlung: 1024 behalten** und das Detail anders holen: UV-Flaeche besser nutzen (68 % -> 80 %+, mehr Flaeche fuer Unterseite
und Sohlen statt fuer verdeckte Stellen), Straehnen als Buschel von 3-6 Texeln Breite (1-2 cm) mit Hell/Dunkel-Paaren statt
1-Texel-Haaren, weiter bei 2048 backen und mit gutem Filter auf 1024 verkleinern (wie bisher 2x2-Mittel). Wenn Kevin 2048 sehen
will: als Vergleichsdatei (gleicher Name nur in einer Kopie der Test-Mod), mit Hinweis auf Flimmern beim Herauszoomen.

---

## 2. Alpha (Haarkarten am Rand)

### 2.1 Was Shader und GL-Zustand koennen
* `animalEffect.frag:33-37`: `if (texSample.w < 0.01) discard;` -- Ausschneiden geht. `:78`: Ausgabe-Alpha = `Alpha * texSample.w`
  -> halbtransparente Pixel werden geblendet.
* GL-Zustand fuer Figuren/Tiere (`IsoAnimal extends IsoPlayer`): `ModelSlotRenderData.performRenderCharacter` Offset 10-41:
  Blend an, `glBlendFunc(SRC_ALPHA, ONE_MINUS_SRC_ALPHA)`, Alpha-Test GREATER 0, Tiefentest an. `Model.DrawChar` Offset 69-147:
  Culling aus dem Modell-Skript (`cullFace`, Vorgabe -1 -> `glCullFace(1028)` an), `glDepthFunc(LESS)`, Alpha-Test GREATER 0,01.
  **Tiefe wird geschrieben** (`ModelSlotRenderData.renderCharacter`: `ModelCamera.depthMask = true`; `CharacterModelCamera.Begin`
  `glDepthMask(depthMask)`). Das Netz geht in **einem** `glDrawElements` in Index-Reihenfolge raus
  (`VertexBufferObject` Offset 21-25), **ohne Sortierung**.

### 2.2 Die Falle: die Textur wird zweimal "vormultipliziert"
Die Tier-Textur geht nie direkt auf das Modell, sondern zweimal durch `TextureCombiner.combine`
(`ModelInstanceTextureCreator.render`: `createFullCharacterTexture` und `applyCharacterTexture`, jeweils `calculate`).
Jedes Mal: Ziel geleert auf (0,0,0,**0**) (`combine` Offset 57 `startDrawing(true,true)` -> `TextureFBO.startDrawing`
`glClearColor(0,0,0,0)`), dann Blit mit `glBlendFuncSeparate(SRC_ALPHA, ONE_MINUS_SRC_ALPHA, ONE, ONE_MINUS_SRC_ALPHA)`
(`combine` Offset 442; Werte aus `TextureCombinerCommand.init(tex, shader)` = 770/771/1/771; Blend an in
`Core.DoStartFrameStuffInternal`; Shader `blit.frag` kopiert nur). Rechnung:
Farbe = rgb * a (1. Durchgang) -> rgb * a^2 (2. Durchgang), Alpha bleibt a. Danach gibt `animalEffect.frag:78` diese Farbe mit
Alpha a aus und das Blending multipliziert noch einmal: **auf dem Schirm rgb * a^3**. Ein Haarpixel mit a = 0,5 erscheint mit
12,5 % seiner Farbe statt 50 % -> **dunkle bis schwarze Saeume**. Voll durchsichtige Texel werden schwarz (0,0,0,0); die lineare
Filterung mischt am Kartenrand deshalb immer Schwarz hinein (etwa 1 Bildpunkt dunkle Kante), auch bei hartem 0/255-Alpha.
(Kleidung mit eigenem Modell und einfacher Textur bekommt die Datei direkt, `render` `data.modelInstance.tex = itemTexture`
-- nur deshalb gehen dort halbtransparente Stellen wie das Glas der Gasmaske, 7 % Teil-Alpha in `clothes/hat/gasmask.png`.)

### 2.3 Weitere Risiken
* Sortierung: Karte vor dem Rumpf, aber im Index-Buffer frueher -> schreibt Tiefe, der Rumpf dahinter wird verworfen, man sieht
  den Boden durch das Fell. Reihenfolge der Dreiecke bleibt vermutlich wie in der Datei (Nachbearbeitung des Importers ohne
  `IMPROVE_CACHE_LOCALITY`, s. 3) -- Karten ans Ende legen hilft nur teilweise (Selbstueberdeckung je Blickwinkel). **ungeprueft**.
* Einseitig: Culling an -> Karten nur von einer Seite sichtbar, sonst doppelte Dreiecke (Budget!) oder `cullFace = None` fuer das
  ganze Modell (Vanilla nur bei Muendungsfeuer: `scripts/generated/weapons/firearm/fx/muzzle_flash_models.txt:7`).
* Schatten: keine Gefahr -- Tiere haben einen Fleck-Schatten (`IsoAnimal.renderShadow` -> `FBORenderShadows.addShadow` mit
  `shadoww/shadowfm/shadowbm`), die Netzform zaehlt nicht.
* Atlas: lebende Tiere werden nicht in einen Atlas gezeichnet (es gibt nur `DeadBodyAtlas` fuer Leichen und `WorldItemAtlas`);
  der tote Baer landet im `DeadBodyAtlas` (Eintraege in 1024er Seiten, geleert auf Alpha 0, `DeadBodyAtlas.frag` verwirft
  Alpha 0) -- Saeume dort ebenfalls dunkel.
* Vanilla nutzt **keine** Haarkarten: Haare sind feste Netze mit RGB-/Grau-Texturen ohne Alpha (`hairStyles/hairStyles.xml:5-6`
  `F_Hair_White` -> `textures/F_Hair_White.png` 128x128 RGB; `F_HairCurly_Long`, `F_Hair_Braids` Graustufen).

**Ergebnis: Alpha-Haarkarten technisch moeglich (Ausschneiden bei a < 0,01), praktisch nein**: weiche Kanten werden schwarz
(a^3), harte Kanten bekommen eine dunkle Linie, Sortierfehler moeglich, Kosten an Dreiecken. Empfehlung: spitze Zotteln als
echte Geometrie im Umriss (kleine Dreiecks-Spitzen an der Silhouette) und Straehnen in der Textur. Wenn ueberhaupt ein Versuch:
nur hartes Alpha 0/255, Karten am Ende der Index-Liste, Saum-Texel in Fellfarbe sehr dunkel einplanen, im Spiel pruefen.

---

## 3. Netz-Grenzen am Tier

| Grenze | Wert | Beleg |
|---|---|---|
| Netze/Materialien | **genau eins** wird genommen: das erste Netz mit Knochen (oder nach Name) | `ProcessedAiScene.findMesh` Offset 48-65; ein 2. Material = 2. Netz -> **verschwindet** |
| Textur je Modell | eine (`ModelInstance.tex`, Shader-Sampler `Texture`) | `animalEffect.frag:7`, `Shader.startCharacter` (`setTexture(tex,"Texture",0)`) |
| Knochen | **hoechstens 60** | `animalEffect.vert:16` `MatrixPalette[60]`; Java-Puffer 1024 floats = 64 Matrizen (`Shader.setMatrixPalette`, `createFloatBuffer(1024)`), 61-64 ignoriert der Shader, ab 65 laeuft der Puffer ueber (Ausnahme). Baer: 26 Gelenke im Skin |
| Einfluesse je Punkt | **4** (staerkste 4 durch Assimp `LIMIT_BONE_WEIGHTS`, dann erste 4 je Punkt, Summe neu auf 1) | `FileTask_LoadMesh.loadGLTF` Offset 19-59; `ImportedSkinnedMesh.processAiScene` (`iconst_4` Offset 13-16, Normierung) ; `animalEffect.vert:28-36` |
| Dreiecke/Punkte | **keine Engine-Grenze gefunden**: Indizes 32 Bit (`GL_UNSIGNED_INT` 5125, `VertexBufferObject` Offset 21-25), keine 65.535-Schranke | 20.000 ist unser eigenes Budget (Vanilla-Kuh ~1.044 Flaechen) |
| Normalen | **aus der Datei, 1:1** (keine Neuberechnung: Schrittliste ohne `GEN_NORMALS`/`GEN_SMOOTH_NORMALS`); fehlen sie -> (0,1,0) = flach | `ImportedSkinnedMesh` Offset 353 (`NormalArray`), 470 (`hasNormals`) |
| Tangenten / Normal-Map | **nein**: Punktformat nur Position, Normale, 4 Gewichte, 4 Indizes, UV; Shader ohne Tangente und mit einem Sampler | `ImportedSkinnedMesh` Offset 353-399; `animalEffect.vert:3-7` |
| Punktfarben | **nein** (nicht importiert; Shader setzt `vertColour = vec3(1.0)`) | `animalEffect.vert:41-42` |
| UV | V wird gespiegelt (`1 - v`); mehrere UV-Saetze werden gelesen, der Shader nutzt nur den ersten | `ImportedSkinnedMesh.processAiScene` |
| Nachbearbeitung | FIND_INSTANCES, MAKE_LEFT_HANDED, LIMIT_BONE_WEIGHTS, TRIANGULATE, OPTIMIZE_MESHES, REMOVE_REDUNDANT_MATERIALS, JOIN_IDENTICAL_VERTICES; per Modell-Skript `postProcess = +X;-Y` aenderbar | `FileTask_LoadMesh.loadGLTF` / `handlePostProcessFlags` |
| Modell-Skript | `cullFace = Back/Front/None`, `postProcess`, `shader`, `texture` | `ModelScript.Load` (Schluessel `cullFace`, `postProcess`) |

Ein eigener Shader in der Mod (fuer Normal-Maps) waere ein Engine-Eingriff ohne Vanilla-Vorbild -> nicht empfohlen, nicht geprueft.

---

## 4. Licht auf der Unterseite

### 4.1 Was der Shader rechnet (`animalEffect.frag:47-79`)
`licht = Ambient + Summe(5 Richtungslichter: Farbe * max(dot(Normale, Richtung), 0))`, je Kanal auf 1,0 gedeckelt, dann
`Farbe = Textur * licht`. Kein Glanz, kein Schatten auf dem Modell, kein AO, kein Gamma (der sRGB-Wert der Textur wird direkt
multipliziert), `vertColour` immer 1.
Woher die Werte kommen (`ModelInstance$PlayerData.updateLights`, `Shader.startCharacter`):
* Ambient im Shader = **0,45 x A** (A = Licht der Kachel, `Shader.startCharacter` Offset 42-83, `setAmbient`).
* Draussen (und in Raeumen) **zwei Fuell-Lichter** fest in der Welt: bei (x-2, y-2, z+1) und (x+2, y+2, z+1), Farbe je
  **A x 1,7 / 4 = 0,425 A** (`updateLights` Offset 1090-1210), also von schraeg oben aus **19,5 Grad** Hoehe, eines von der
  Kameraseite (Sued-Ost), eines von hinten (Nord-West). Dazu bis zu 3 Lampen/Feuer der Kachel (x 0,7) und die Taschenlampe.
* Kamera: 30 Grad von oben (`Core.DoPushIsoStuff` Offset 332-350: Drehung pi/6 um X, 3pi/4 um Y).

### 4.2 Ergebnis je Flaechenrichtung (Tageslicht, ohne Lampen; gerechnet aus den Formeln oben)
| Normale zeigt | Licht |
|---|---|
| waagrecht zur Kamera (SO) oder weg (NW) | 0,85 A |
| 45 Grad nach oben zur Kamera | 0,83 A |
| nach oben (Ruecken) | 0,73 A |
| 45 Grad nach unten zur Kamera | 0,63 A |
| **nach unten (Bauch, Brust-Unterseite, Achsel, Pfotenunterseite), auch waagrecht nach NO/SW** | **0,45 A** (nur Ambient) |
Die Unterseite bekommt also hoechstens 53 % des hellsten Lichts und 61 % des Rueckens -- jede Flaeche, die mehr als 19,5 Grad
nach unten zeigt, sieht kein Fuell-Licht. Wird die Unterseite in der Textur zusaetzlich dunkel gebacken (Rundumlicht-Bake = AO,
plus verdeckte Ansichten, `baer_export_anim.py:99-106`), multipliziert sich das: Fell sRGB 90 x 0,45 = 40 -> fast schwarz.
Darum wirken Brust/Bauch verschmiert und die Sohlen wie Loecher. Beim Sitzen/Aufrichten zeigen Brust und Sohlen eher zur
Kamera (0,6-0,85 A); dort ist es vor allem die **dunkle Textur**, nicht das Licht.

### 4.3 Was hilft
1. **Unterseite in der Textur aufhellen**: Bauch/Brust/Achsel/Innenschenkel/Kehle als eigene Fellfarbe malen, Albedo etwa
   +20-40 % gegen den Ruecken, damit sie im Spiel bei ~75-85 % des Rueckens landet (Zielrechnung: 0,45/0,73 = 0,61; x 1,3 = 0,8).
2. **AO-Mass**: offene Unterseite nicht unter ~0,85 abdunkeln (die Engine dunkelt schon); nur echte Falten/Knicke (Achselfalte,
   Ellbogen, Schenkelansatz, Zehenzwischenraeume) tiefer, Minimum ~0,55-0,6. Richtungslicht nie einbacken.
3. **Sohlen**: Ballen dunkelgrau-ledrig, nicht schwarz: Grundwert sRGB ~60-75, Ballenkuppen heller (~85-100), Furchen ~35-45,
   Fellrand heller als die Haut -> bleibt auch bei 0,45 A lesbar (65 x 0,45 = 29 ist schon dunkel genug).
4. **Normalen biegen (billigster Hebel, kostet kein Dreieck)**: die Engine nimmt die Normalen der Datei 1:1. Unterseiten-Normalen
   um 30-40 Grad Richtung waagrecht/aussen kippen (oder von einer stark geglaetteten Huelle uebernehmen, "Fell-Normalen")
   bringt dort Fuell-Licht (z. B. von 0,45 auf ~0,6 A) und macht das Fell weicher. Gilt nur fuer Licht, nicht fuer die Form.
5. Hellere Lichtkante oben am Umriss in der Textur (Spitzen der Zotteln heller) hilft gegen den "Klumpen" von hinten, weil das
   Spiel keine Glanz- oder Randlichter hat.

---

## 5. Kurz fuer die Bauer
* Textur: Ja, 2048 wuerde geladen (kein Deckel fuer Tiere), aber keine Mipmaps -> 1024 behalten, Detail ueber UV-Nutzung und
  breitere Straehnen; 2048 hoechstens als Vergleichsdatei.
* Alpha-Karten: Nein (schwarze Saeume durch a^3, Tiefe ohne Sortierung, einseitig). Spitze Zotteln als Geometrie.
* Netz: ein Netz, ein Material, <= 60 Knochen, 4 Einfluesse, Normalen aus der Datei, keine Tangenten/Normal-Map/Punktfarben,
  keine Engine-Dreiecksgrenze (Budget 20.000 bleibt unsere Regel).
* Licht: Unterseite bekommt nur 0,45 A -> Albedo dort heller, AO sparsam, Sohlen dunkelgrau statt schwarz, Normalen biegen.
* Offen/ungeprueft: Dreiecks-Reihenfolge nach dem Import (wichtig nur fuer Alpha-Versuche), Kevins Zoomstufe (Texel je Bildpunkt
  ist eine Schaetzung aus einem Bild), Wirkung im Spiel generell.
