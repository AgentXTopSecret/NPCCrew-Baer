# Forschung: z Z z ueber dem schlafenden Baeren (Lauf baer-schlaf, Thema zz, 09.11.2026)

Statisch geprueft, nichts gebaut, nichts gespielt, nichts heruntergeladen. Keine Mod-Datei geaendert.
Eigene Hilfsdateien in `_arbeit/baer_schlaf/zz/`: `ziehen.py` (Klassen aus dem Jar, `javap -c -p` nach `zz/dump/`),
`hoehen.py` + `hoehen_ausgabe.txt` (Hoehe des Ankers je Groesse), `zz_kurve.lua` + `zz_kurve_ausgabe.txt` (Rechenprobe der
Bewegung mit Lua 5.1). Jar-Zitate: `zz/dump/<Klasse>.txt`, Klasse.Methode Offset.

## Kurzbefund

1. **NPC Crew zeigt KEIN "Zzz" ueber schlafenden NPCs.** Kein `Zz`/`zzz`/`ZZZ` in `NPCCrew/42/media/lua` (Lua und Translate), keiner in
   `_docs/landkarte_index.txt`; die NPCs schlafen (`shared/BanditsNPCRoutine.lua:223-245`, `shared/BanditsNPCSchedule.lua:1754`), ohne Zeichen.
   Bandits hat auch keins. Vanilla auch nicht (kein Lua-Treffer; `IsoAnimal` hat im Jar 42.21 null Stellen mit "sleep").
2. **Der Stil kommt deshalb von den NPC-Crew-Namensschildern** `client/ISUI/BanditsNPCNameTags.lua` (gespielt, mehrfach von Kevin
   nachgestellt): 1x1-ISPanel in der Ecke, Zeichnen im `prerender`, Liste alle 500 ms, Position je Bild, `isoToScreenX/Y(0, ...)`,
   `UIFont.Small`, Farbe (0,96 0,96 0,90), schwarzer Schatten 1 px. Der groessere Sprechtext derselben Datei zeigt, wie man Schrift
   weich verkleinert (`drawTextZoomed`, groessere Schrift herunterskaliert).
3. **Beste Option: eigenes 1x1-Overlay `BanditsNPCBearOverlay.lua`** (Bauform NameTags/PyreFx), Buchstaben "Z" mit `drawTextZoomed`
   (ISUIElement.lua:1260), Farbe und Schatten wie die Namensschilder. Alles belegt (Belegliste unten), alles rein lokal, kein Paket.
4. **Engine-Wege fallen aus:** Sprechblase (`addLineChatElement`/`Say`) hat keine Lua-Fundstelle an einem Tier und kann nicht
   animieren; `HaloTextHelper` zeichnet nur ueber dem eigenen Spieler (`playerIsSelf`); Vanillas Tiername (`renderCustomName`) nur in
   der Tierzonen-Ansicht.
5. **Hoehe aus der Engine gerechnet:** 1 m am Baeren bei Groesse 1,0 = 0,3331 z-Ebenen = 64 px (Zoom 1). Kopf im Schlaf (Annahme
   0,40 Einheiten) -> Anker 16 px (0,35), 35 px (0,75), 64 px (1,35) ueber dem Boden; dazu der Kopf bis 0,9 Kacheln vor der Mitte.
   Die echte Kopfhoehe misst der Bauer des Schlaf-Clips (Messauftrag 3.4); Regler gleich mitbauen (NPC-Crew-Lehre).
6. **Woher der Client weiss, dass er schlaeft:** von der Animations-Variable an SEINER Kopie (`getVariableString`) -- dieselbe, die den
   Schlaf-Clip startet. Im Einzelspieler setzt sie das Gehirn, im Mehrspieler der Client beim Serverbefehl (B8). Kein eigenes Netz fuer
   z Z z. Im MP offen, bis B8 die Variable an jeden Client bringt (das braucht der Schlaf-Clip ohnehin).
7. **Kosten:** je sichtbarem schlafenden Baeren und Bild 2 Umrechnungen + 6 Textaufrufe; Liste alle 500 ms, Zellsuche hoechstens alle
   5 s, Deckel 8 Baeren. Geteilter Bildschirm: nichts zeichnen (wie NPC Crew).
8. **Kein Text-Schluessel noetig:** "Z" ist in allen sieben Sprachen dieselbe Glyphe (geprueft: `char id=90` in Medium/Large von EN,
   CN, CH, KO, RU; PTBR/ES/FR nutzen EN). Erst der Menue-Schalter braucht `UI_BN_Bear_*`.

---

## 1. Was NPC Crew und Bandits heute zeichnen

### 1.1 Zzz bei NPC Crew: nein

* Gesucht in `NPCCrew/42/media/lua` (alle .lua, .json, .txt) nach `Zz|zZ|z Z|ZZZ|zzz`: nur Fremdtreffer (Variablennamen `zz`, Woerter
  wie "Satz"). In `shared/Translate`: nichts.
* `_docs/landkarte_index.txt`: Schlaf-Eintraege nur fuer den SPIELER-Schlaf (`client/BanditsNPCSleep.lua`, Zeilen 2053-2075 des Index)
  und `OnSleepingTick` (`client/BanditsNPCPersistence.lua:10414`). Kein Zeichner fuer schlafende NPCs.
* NPC-Schlaf ist reine Logik: `BanditsNPC.Routine.SleepStart = 22`, `SleepEnd = 7` (`shared/BanditsNPCRoutine.lua:224-225`),
  Schlafblock im Plan (`shared/BanditsNPCSchedule.lua:1754-1755`).

### 1.2 So zeichnet NPC Crew Namen ueber Figuren (Vorbild fuer den Stil)

`client/ISUI/BanditsNPCNameTags.lua` (1498 Zeilen, Kevins Ansagen v3.7.29-v3.12.26, gespielt):

| Punkt | Fundstelle | Inhalt |
|---|---|---|
| Warum selbst zeichnen | :17-21 | Spieler-Namensschild der Engine laeuft nur mit `GameClient.client` und am IsoPlayer -- fuer Companions unerreichbar |
| Belegte Aufrufe | :23-37 | `isoToScreenX/Y(playerIndex, x, y, z)` (Zahl, nicht Spielerobjekt), `drawTextCentre`, `getFontHeight`, `isCanSee`, `getNumActivePlayers` |
| Element 1x1, nie unsichtbar | :43-60, :1178-1189 | ein grosses Element frisst jeden Weltklick (v0.72 "Rechtsklick-Killer"); unsichtbar kommt nie zurueck. Dazu `onMouseDown/Up/onRightMouseDown` -> false (:1141-1143) |
| Anker | :66-70, :158 | `z + 0.6667` = Unterkante der Engine-Sprechblase (128 von 192 px je Ebene) |
| Keine Zoom-Division fuer Abstaende | :96-100 | `isoToScreenY` teilt schon durch den Zoom; Text hat feste Groesse; ein geteilter Freiraum schrumpft beim Herauszoomen |
| Einstellung je Rechner | :106-111, :281-302 | `BanditsNPC.ClientCfg`, Datei `Zomboid\NPCCrewClient.ini`, Abschnitt `NameTags`; Vorgabe an mit `== nil` (nicht `or true`) |
| Geteilter Bildschirm | :125-131, :1154-1157 | bei mehr als einem lokalen Spieler wird NICHTS gezeichnet (ausgesprochen) |
| Takt | :143-144, :1165-1168 | Liste alle 500 ms (`RESCAN_MS`), Umkreis 45 Kacheln (`MAX_DIST`) |
| Wer gezeigt wird | :804-951 | nur gleiche Ebene (:893), Abstand (:895), `sq:isCanSee(0)` -- "durch Waende zeigt es nicht" (:897-899) |
| Zeichnen je Bild | :957-1039 | Position JE BILD frisch vom Koerper (:983-985), nicht ausserhalb des Bildschirms (+300 px Rand, :991) |
| Aussehen | :1022, :1035 | Schatten `drawTextCentre(name, x+1, y+1, 0,0,0, 0.65, UIFont.Small)`, Name `(0.96, 0.96, 0.90, 0.95)`; Neutrale orange-gold (:1030), Fremde gruen (:1033), rot bei fremder Hoheit (:1026) |
| Schrift weich skalieren | :394-440, :1116-1117 | Schrifthoehen Small/Medium/Large alle 2 s gemessen; die kleinste, die gross genug ist, mit `drawTextZoomed` VERKLEINERT ("verkleinerte Bitmapschrift bleibt scharf, vergroesserte wird weich", :209-210); Schatten `max(1, floor(lineH/20))` px mit Alpha 0,7 (:1058, :1116) |
| Verblassen | :260, :1101-1105 | `BARK_FADE_MS = 750`, Alpha linear am Ende |
| Aufraeumen | :1196-1205 | `OnMainMenuEnter` leert Panel und Tabellen (sonst tot nach "Hauptmenue -> neu laden") |

Was es je Bild kostet (gelesen, nicht gemessen): je Schild 2 Umrechnungen (`isoToScreenX/Y`), 3 Positionsabfragen, 2 `drawTextCentre`;
die teuren Fragen (`isCanSee`, Hoheit) nur im 500-ms-Sammler (:918-921).

Lehren in `NPCCrew/CLAUDE.md:2448-2470`: (a) wer eine Zahl raten muss, baut den Regler gleich mit (78 gerechnet, 12 im Spiel, heute 0);
(b) keine Zoom-Division fuer einen Freiraum; (c) ein Overlay bleibt 1x1 in der Ecke.

Zweites Vorbild, mit Bewegung nach der Uhr: `client/ISUI/BanditsNPCLivestockPyreFx.lua` (Flamme/Rauch/Asche an einer Weltposition):
Bildnummer aus `getTimestampMs()` (:486), `zoom = getCore():getZoom(0)` (:468), `isoToScreenX/Y(0, ...)` (:489-490),
`drawTextureScaledUniform` (:504-514), gleiche Bauform plus `backMost()` (:549, Vanilla `FishingManager.lua:41`), geteilter Bildschirm
nichts (:532); Verwaltung einmal je Sekunde ueber OnTick, Zeichnen im prerender (Kopf :49-67). Kopfnotiz dort: alles liegt UEBER der
Welt wie ein Namensschild (:13-16).

Balken gibt es in NPC Crew nur in Fenstern, nicht ueber Figuren: `BanditsNPC.UI.StatBar` (`client/ISUI/BanditsNPCUIStyle.lua:490-525`,
Farbe nach Stand: unter 30 % rot (0,78 0,34 0,30), unter 60 % `U.C.warn`, sonst `U.C.good`) und `U.Track` (:920-940: Grund schwarz
0,5, Fuellung, Rand `U.C.hairline`, Hoehe `U.S(8)`). Farbtabelle `U.C` :32-63 (good :59, warn :58, hairline :35), Vorgabe-Schema
"night" (:295); **kein Gruen in der Oberflaeche** (:15-18).

### 1.3 Bandits

* Keine Namen und keine Symbole ueber Figuren. Sprechen nur ueber die Engine-Blase: `zombie:addLineChatElement(getText(text), r, g, b)`
  (`shared/Bandit.lua:1318/1320`, am Zombie).
* Bilder an Weltpositionen: `client/BanditProjectile.lua` -- `Events.OnPreUIDraw` (:88, :172), `ISCoordConversion.ToScreen` (:10, :112),
  `getRenderer():renderline` (:74), `renderPoly` (:160), Hoehe selbst durch `getCore():getZoom(0)` geteilt. Linien und Bilder, kein Text.
  So baut auch der Turret (`NCTurretTest/.../client/BanditsNPCTurretFx.lua:4`, :413).
* `client/BanditEventMarkers.lua:176`: `drawTextCentre` -- Randmarker am Bildschirm, nicht ueber Figuren.

---

## 2. Vanilla-Wege, Text an einer Weltposition zu zeichnen

| Weg | Beleg (gleiche Argumenttypen) | taugt fuer z Z z? |
|---|---|---|
| **Weltpunkt -> Bildschirm:** `isoToScreenX/Y(int playerIndex, float x, float y, float z)` | Vanilla `client/Fishing/TensionUI.lua:11-12` (`self.playerIndex`, Zahl), `client/Foraging/ISBaseIcon.lua:167` (`o.player = ...getPlayerNum()`, :870); Jar `LuaManager$GlobalObject.isoToScreenY` (dump :1634): `(YToScreen - cam.offY) / cam.zoom + IsoCamera.getScreenTop(i)` -- Zoom UND Ansichtsfenster schon drin | **ja** (wie NameTags) |
| `ISCoordConversion.ToScreen(x, y, z)` | Vanilla `server/ISCoordConversion.lua:4-16` (ohne Zoom, ohne Ansichtsfenster), Bandits `BanditProjectile.lua:10` | moeglich, aber Zoom selbst teilen; schlechter als isoToScreen |
| **Text skaliert:** `self:drawTextZoomed(str, x, y, zoom, r, g, b, a, font)` | Vanilla-Funktion `client/ISUI/ISUIElement.lua:1260-1268` (ruft `DrawText(font, str, x, y, zoom, r,g,b,a)`); gespielt in NPC Crew `BanditsNPCNameTags.lua:1116-1117` | **ja** -- die einzige belegte Art, Text stufenlos zu skalieren (klein-gross-klein) |
| Text mittig: `self:drawTextCentre(str, x, y, r, g, b, a, font)` | `ISUIElement.lua:1280`; Bandits `BanditEventMarkers.lua:176`; NPC Crew NameTags :1022 | fuer den Namen; fuer z Z z ohne Skalierung zu stufig |
| Breite messen: `getTextManager():MeasureStringX(font, str)` | Vanilla `client/ISUI/ISButton.lua:233`; NPC Crew NameTags :1097 | ja (Buchstabe mittig setzen) |
| Schrifthoehe: `getTextManager():getFontHeight(UIFont.Medium)` | Vanilla `client/ISUI/AdminPanel/ISAddNonPvpZoneUI.lua:4` | ja (Groesse folgt Kevins Schriftgroessen-Option, also 4K) |
| Text ohne Panel: `getTextManager():DrawString(UIFont.X, x, y, str, r,g,b,a)` in `Events.OnPreUIDraw` | Vanilla `client/erosion/debug/DebugDemoTime.lua:117` (Ereignis), :183-196 (`DrawString`/`DrawStringCentre` mit Schatten) | moeglich, aber ohne Zoom-Parameter -> nur drei Schriftstufen, kein weiches Wachsen |
| Bild statt Schrift: `self:drawTextureScaledUniform(tex, x, y, scale, a, r, g, b)` + `getTexture(pfad)` | `ISUIElement.lua:1054`; `getTexture("media/ui/Moodles/Moodle_Icon_Dead.png")` `client/OptionScreens/LoadGameScreen.lua:972`; NPC Crew PyreFx :504 | moeglich mit eigenem "Z"-Bild (eigene Textur noetig). Vanillas `media/ui/Moodles/<n>/Mood_Sleepy.png` ist ein muedes GESICHT, kein Zzz (angesehen) |
| Sprechblase `animal:addLineChatElement(str, r, g, b)` / `Say` | Lua nur an Zombies/Spielern (Bandits `Bandit.lua:1318`, NPC Crew NameTags :563); an einem Tier **keine Fundstelle**. Jar: `IsoAnimal extends IsoPlayer` (dump Kopf), `IsoAnimal.renderlast` ruft am Ende `IsoPlayer.renderlast` (Offset 77) -> `IsoGameCharacter.renderlast` zeichnet die Blase, wenn `chatElement.getHasChatToDisplay()` (Offset 157-170) | **nein**: nur Jar (braucht Kevins Wort), feste Schrift `UIFont.Dialogue`, eine Zeile, kein Wachsen/Steigen; ob `Say` an einem IsoPlayer-Abkoemmling im MP in den Chat geht: ungeprueft |
| `HaloTextHelper.addText(IsoPlayer, String, ...)` | Vanilla `client/Foraging/forageClient.lua:73` (am Spieler) | **nein**: die Engine zeichnet den Halo nur, wenn `playerIsSelf()` (`IsoGameCharacter.renderlast` Offset 893-975), und das ist `IsoPlayer.getInstance() == this` (`IsoGameCharacter.playerIsSelf`, dump :18413) -- also nur ueber dem eigenen Spieler; Schluessel ist `player.getIndex()` (`HaloTextHelper`, dump :326 ff.) |
| Vanillas Tiername `setCustomName` | Jar `IsoAnimal.renderlast` Offset 73 -> `renderCustomName` (dump :2616): bricht ab, wenn der Spieler NICHT `isSeeDesignationZone()` (Offset 16-23); sonst weiss, `UIFont.Small`, am Kopf-Attachment | **nein** (nur in der Tierzonen-Ansicht). Merken fuers Namensschild: nicht `setCustomName` benutzen |

**Splitscreen-Detail:** `isoToScreenY` addiert `IsoCamera.getScreenTop(i)` (GlobalObject.isoToScreenY, dump :1634 ff.) -- die Koordinaten
enthalten das Ansichtsfenster. NPC Crew uebergibt hart 0 und zeichnet bei mehreren lokalen Spielern gar nicht (NameTags :125-131).

---

## 3. Hoehe und Lage des Ankers (Groesse 0,35 / 0,75 / 1,35, Liegehaltung)

### 3.1 Die Masse der Engine (Jar 42.21)

* Modell -> Welt: `IsoAnimal.getAttachmentWorldPos(String, Position3D)` (dump :7856 ff.) baut `translation(getX, getZ, getY)`,
  `rotateY(-renderedAngle)`, `scale(-1.5*animalSize, 1.5*animalSize, 1.5*animalSize)` (Offset 80-140). Der Zeichner selbst skaliert
  ebenso mit 1,5 (`Core.DoPushIsoStuff` Offset 413-422; frueher schon `bau_lebend.md:47` "1,5 Kacheln je Einheit").
* Senkrecht: `Position3D.z = floor(y) + ((y + 32) mod 1) / 2.44949` (getAttachmentWorldPos Offset 196-221); der Zeichner setzt die
  Ebene mit `(z - camZ) * 2.44949` (`Core.DoPushIsoStuff` Offset 370-388). **1 z-Ebene = 2,44949 Welt-Einheiten.**
* `getAnimalSize()` = `getData().getSize()` (IsoAnimal dump, `getAnimalSize` Offset 0-7) -- also genau der Wert aus `setSizeForced`.
* Bildschirm: `IsoUtils.YToScreen` = `(x + y) * 16 * ts + (cz - z) * 96 * ts` (dump :385-421), `XToScreen` = `(x - y) * 32 * ts`;
  bei `tileScale` 2 also 192 px je z-Ebene, 64 px je Kachel quer; `isoToScreenY` teilt durch den Zoom.
* Netzmassstab des Baeren: 0,544 Einheiten je Meter (`NCBearDefs.lua:73`, NPC-Crew-Nebenprojekte `CLAUDE.md` Abschnitt 8).

**Formel:** Anker-Hoehe in z-Ebenen `dz = H_E * 1.5 * size / 2.44949` (H_E = Hoehe im Netz bei Groesse 1,0 in Modell-Einheiten).
**1 m am Baeren bei Groesse 1,0 = 0,3331 z = 64 px bei Zoom 1.**

Gegenprobe (`zz/hoehen_ausgabe.txt`): Mensch 1,80 m (0,98 E) -> 0,600 z = 115 px; NPC Crews Namensanker 0,6667 z = 128 px liegt also
13 px ueber dem Kopf -- passt zu Kevins Messung "Offset 0 sitzt richtig" (NameTags :145-157). Baer stehend 0,633 E -> 1,164 m bei 1,0 und
1,571 m bei 1,35 -- passt zu "1,16 m" und "1,55 m Schulter" (`begleiter/ENTSCHEIDUNGEN.md:10-12`).

### 3.2 Tabelle (tileScale 2; Zoom 1 / 2 / 0,5)

| Groesse | Kopf im Schlaf, ANNAHME 0,40 E | hoechster Punkt Dead-Clip 0,531 E (`bau_lebend.md:44`) | stehend 0,633 E |
|---|---|---|---|
| 0,35 Jungtier | 0,26 m, 0,086 z, **16 px** / 8 / 33 | 0,34 m, 22 px | 0,41 m, 26 px |
| 0,75 Halbstark | 0,55 m, 0,184 z, **35 px** / 18 / 71 | 0,73 m, 47 px | 0,87 m, 56 px |
| 1,00 | 0,74 m, 0,245 z, 47 px | 0,98 m, 62 px | 1,16 m, 74 px |
| 1,35 Erwachsen | 0,99 m, 0,331 z, **64 px** / 32 / 127 | 1,32 m, 84 px | 1,57 m, 101 px |

Die 0,40 E sind GERATEN (Kopf auf den Vorderpranken, nach echten Baeren). Der Dead-Clip (auf der Seite liegend) ist die Obergrenze aus
dem heutigen Netz. **Der Anker muss aus dem echten Schlaf-Clip kommen** (3.4).

### 3.3 Waagerecht: ueber dem Kopf, nicht ueber der Mitte

Die Tierposition ist die Mitte (Bip01 steht in allen Clips bei x = y = 0, `bau_lebend.md:46`). Der Kopf liegt vorn: Kopfgelenk stehend bei
0,70 m (`bau_lebend.md:57`) = 0,38 E; im Schlaf mit Kopf auf den Pranken eher weiter vorn (ANNAHME 0,45 E). Das sind
`0,45 * 1,5 * size` Kacheln: 0,24 (0,35) / 0,51 (0,75) / **0,91 Kacheln (1,35)**, also bis 58 px seitlich -- sichtbar. Vorschlag:

`hx = x + fwdX * KOPF_VOR_E * 1.5 * size`, `hy = y + fwdY * KOPF_VOR_E * 1.5 * size`, Anker `isoToScreenX/Y(0, hx, hy, z + dz)`.

`fwd = animal:getForwardDirection()`, `fwd:getX()`, `fwd:getY()`: belegt am Zombie (Bandits `shared/ZombieActions/ZAPush.lua:36-37`,
genutzt in `NCBearFight.lua:855-856`) und am IsoPlayer (`ISBaseIcon.lua:216`); IsoAnimal erbt die Methode (`extends IsoPlayer`,
Jar). Dass die Vorwaertsrichtung eines ruhenden Tiers der Blickrichtung des Modells entspricht: plausibel, **ungeprueft** (die Engine
dreht das Modell mit `getRenderedAngle`, getAttachmentWorldPos Offset 98-113). Waehrend er schlaeft dreht er sich nicht -> im
500-ms-Sammler holen, nicht je Bild.

Groesse: `animal:getData():getSize()` (Vanilla `ButcheringUtil.lua:568`, `animal:getData():getSize()` an einem `IsoAnimal.new`). Im
MP setzt der Client die Groesse selbst per `setSizeForced` (`begleiter/PLAN.md:233-234`), der Wert stimmt dann auch lokal.

### 3.4 Messauftrag an den Bau des Schlaf-Clips

Wer die Schlaf-Schleife baut, schreibt zwei Zahlen in seinen Bericht (Modell-Einheiten bei Groesse 1,0, gehaeutet, wie die Tabelle in
`bau_lebend.md:36-44`): **Kopf-Oberkante** (hoechster Hautpunkt am Kopf ueber die ganze Schleife) und **Kopf-Vorlage** (Abstand
Kopfmitte vor Bip01 entlang der Blickrichtung). Liegt der Baer auf dem Baerenbett hoeher als der Boden (dickes Bett, im Clip gehoben),
gilt eine eigene Zahl. Bis dahin: 0,40 / 0,45 E als Vorgabe, verstellbar (3.5).

### 3.5 Regler (Lehre `NPCCrew/CLAUDE.md:2448-2455`)

`BanditsNPC.Bear.Overlay.SetZzLift(px)` (fester Bildpunkt-Abstand ueber dem Anker, Vorgabe 4 -- wie `BARK_GAP` NameTags :261) und
`SetZzHead(e_hoch, e_vor)` als Funktionen im Spiel-Modul, gespeichert in der Client-Datei. Die KONSOLENbefehle dazu (z. B.
`NCBear_ZzLift(px)`) nur in `NCBearBench.lua` -- NPC Crew traegt Konsolenbefehle in Spieldateien (`TrueCompanions_TagHeight`,
NameTags :1484), unsere Regel verbietet das (Nebenprojekte-`CLAUDE.md` 0.2).

---

## 4. Aussehen und Bewegung

**Gewuenscht:** aufsteigend, klein-gross-klein (`begleiter/ENTSCHEIDUNGEN.md:115`). Vorschlag (Zahlen im Spiel nachstellbar):

* **Drei Buchstaben gleichzeitig**, jeder lebt `LIFE = 2,4 s`, versetzt um 0,8 s. Der erste erscheint beim Einschlafen am Kopf, die
  anderen folgen nacheinander (nicht alle zugleich in der Luft).
* **Groesse ueber das Leben eines Buchstaben:** `s(u) = 0,55 + 0,45 * sin(pi * u)` (u = 0..1) -- unten klein, in der Mitte gross, oben
  wieder klein und verblassend. In einem Moment liest sich die Saeule damit wie "z Z z" (Rechenprobe `zz/zz_kurve_ausgabe.txt`, z. B.
  t = 3,0 s: 21 / 24 / 16 px von unten nach oben).
* **Deckkraft:** `a(u) = min(1, u / 0,15) * min(1, (1 - u) / 0,35)` -- weich ein, weich aus.
* **Weg:** nach oben `2,4 * H` (H = Hoehe des grossen Z), nach rechts `0,9 * H * u + 0,12 * H * sin(2 pi u)` (schraeg aufsteigend mit
  leichtem Pendeln, wie im Comic). Bei H = 24 px: rund 58 px hoch, 12 px nach rechts.
* **Glyphe:** immer "Z"; die Groesse macht "z" und "Z" (ein Glyphenwechsel mitten im Flug wuerde springen). Vorhanden in allen
  Sprachschriften (Abschnitt Kurzbefund 8).
* **Schrift und Groesse:** H = `getFontHeight(UIFont.Medium)` -- waechst mit Kevins Schriftgroessen-Option (4K). Gezeichnet mit der
  kleinsten der drei Schriften Small/Medium/Large, die mindestens H hoch ist, per `drawTextZoomed` VERKLEINERT (scharf, NameTags
  :209-210, :428-440). Jungtier kleiner: `H * (0,75 + 0,25 * min(1, size / 1,35))` (0,35 -> 81 %, 0,75 -> 89 %, 1,35 -> 100 %).
* **Farbe wie das NPC-Crew-Namensschild:** `(0,96 0,96 0,90)`, Alpha `0,95 * a`; Schatten schwarz `0,65 * a`, Versatz `max(1, floor(h / 20))`
  px (NameTags :1022, :1035, :1058). Kein Gruen (UIStyle :15-18). Alternative (Frage an Kevin): ein Hauch Blau (0,80 0,88 1,00) fuer "Nacht".
* **Einschlafen/Aufwachen:** Saeule blendet 0,5 s ein, nachdem die Schlaf-SCHLEIFE laeuft (nicht beim Hinlegen); beim Aufwachen (auch
  "Kampf hat Vorrang", `ENTSCHEIDUNGEN.md:118`) keine neuen Buchstaben, alles blendet in 0,6 s aus -- kein Abreissen.
* **Mit Namensschild und Balken:** Stapel von unten nach oben ab dem Kopf-Anker: Balken, Name, darueber steigen die z Z z (schraeg nach
  rechts). So ueberdeckt nichts den Namen.

---

## 5. Kosten, Zoom, Bildschirmrand, Pause, Splitscreen

* **Je Bild** (nur Baeren in der Sichtliste, nur wenn schlafend): `getX/getY/getZ` (3), `isoToScreenX/Y` (2), je Buchstabe Schatten +
  Buchstabe `drawTextZoomed` (3 x 2 = 6), etwas Rechnen. Schrifthoehen und Breiten von "Z" je Schrift nur alle 2 s neu (wie
  `barkFontTable`, NameTags :394-423). Ohne schlafenden Baeren in der Liste: ein Tabellenblick und zurueck.
* **Alle 500 ms** (Sammler, wie NameTags :1165-1168): je bekanntem Baeren lebt/da (`isExistInTheWorld`, `isDead`; `NCBearFight.lua:1762-1764`,
  Vanilla `ISAnimalUI.lua:15`), gleiche Ebene, Abstand <= 45 Kacheln (NameTags :144), `sq:isCanSee(0)` (Vanilla `ISBaseIcon.lua:256`),
  Schlaf-Variable (Abschnitt 6), Groesse, Blickrichtung. **Deckel:** hoechstens 8 Baeren (die naechsten), Zustandstabelle hoechstens 32
  Eintraege (sonst leeren, wie `sleepSeen` in `BanditsNPCSchedule.lua:1830-1831`).
* **Baeren finden:** das Overlay sucht NICHT selbst je Bild. Es nimmt die Liste des Baeren-Kerns (heute `F.bears` in `NCBearFight.lua`,
  spaeter `BanditsNPC.Bear.*`); fehlt sie (MP-Client vor B8), hoechstens alle 5 s `getCell():getObjectListForLua()` mit
  `instanceof(o, "IsoAnimal")` und `getAnimalType()` (Vanilla `DebugContextMenu.lua:616-620`, `NCBearFight.lua:1784-1787`; die Liste
  kopiert die ganze Menge, darum selten, `NCBearFight.lua:125`).
* **Zoom:** der Anker folgt von selbst (`isoToScreenY` teilt durch den Zoom). Buchstaben und Steigweg in festen Bildpunkten (an der
  Schriftgroesse), wie NameTags (:96-100). Folge: weit herausgezoomt ist die Saeule im Verhaeltnis zum Jungtier gross. Gemildert durch
  den Groessenfaktor; mehr nur auf Kevins Wort (Frage 3).
* **Ausserhalb des Bildschirms:** Anker mit 100 px Rand ausserhalb -> dieses Bild nichts zeichnen (Form NameTags :991). Hinter Waenden/
  im Ruecken: `isCanSee(0)` ist der Sichtkegel (NameTags :221-223) -> kein z Z z, genau wie kein NPC-Name. Andere Ebene: nichts.
* **Pause:** eigene Uhr, die nur weiterlaeuft, wenn `not isGamePaused()` (Vanilla `client/Foraging/ISSearchManager.lua:1462`) -- die
  Saeule steht in der Pause still wie der Baer. Schnellvorlauf: Wanduhr-Takt, also normales Tempo (nicht hektisch).
* **UI ausgeblendet:** das Panel wird nicht gezeichnet -> kein z Z z (wie die Namensschilder).
* **Splitscreen:** bei `getNumActivePlayers() > 1` nichts zeichnen (Vanilla `client/Fishing/FishingHandler.lua:6`; NPC Crew NameTags
  :1154-1157, PyreFx :532). Ausdruecklich offen, nicht verschwiegen.
* **Dedizierter Server:** laedt `client/` nicht (NameTags :516) -- das Overlay kostet dort nichts.

---

## 6. Woher weiss der Client, dass der Baer schlaeft?

**IsoAnimal kennt keinen Schlaf** (Jar 42.21: null "sleep" in `IsoAnimal`; es gibt nur `isAnimalSitting/Eating/Moving/Attacking`,
dump :6065-6732). Der Schlaf ist also UNSER Zustand.

**Vorschlag: eine Wahrheit je Rechner -- die Animations-Variable an seiner Kopie.**
* Der Schlaf-Clip haengt (wie Sitzen/Fressen) an `NCBearAct` (`animal:setVariable("NCBearAct", act)`, `NCBearFight.lua:533`, Beleg
  Vanilla `shared/TimedActions/Animals/ISPetAnimal.lua:43` am Tier). Das Overlay fragt im 500-ms-Sammler
  `animal:getVariableString("NCBearAct") == "sleep"` (Vanilla `client/ISUI/ISWorldObjectContextMenu.lua:2624`, in `NCBearFight.lua:1349`
  schon am Baeren benutzt). z Z z erscheint damit genau dann, wenn DIESER Rechner den Schlaf-Clip zeigt -- nie Zz ueber einem stehenden
  Baeren. Name der Variable/des Werts beim Umbenennen (B5a) festlegen.
* **Einzelspieler:** das Gehirn (laeuft unter `not isClient()`, `PLAN.md:236-240`) setzt die Variable; das Overlay liest sie. Fertig.
* **Mehrspieler:** die Variable reist nicht von selbst -- "Die Animations-Variablen muss jeder Client an seiner Kopie setzen"
  (`PLAN.md:224-225`, Risiko 2; Liste "muessen wir schicken" :221). Der Server schickt Zustandswechsel (`sendServerCommand(modul,
  befehl, args)` an alle, Vanilla `shared/TimedActions/ISPickupDung.lua:45`), der Client nimmt sie in `Events.OnServerCommand`
  (Vanilla `client/ServerCommands.lua:218`) und setzt `NCBearAct` an seiner Kopie -- das braucht der Schlaf-CLIP selbst, sonst sehen
  Mitspieler den Baeren stehen. z Z z kostet darum **kein eigenes Paket**. Den Baeren findet der Client ueber `getAnimalID()` (Vanilla
  `ISAnimalUI.lua:53`; dass Server und Client dieselbe Kennung haben, deutet `ISVehicleAnimalUI.lua:199` an -- der Client schickt sie
  dem Server; fuer unseren Fall **ungeprueft**). Wer spaeter dazukommt oder den Baeren erst laedt, braucht den laufenden Zustand
  nachgereicht (B8: Nachfrage beim ersten Sehen oder Wiederholung fuer schlafende Baeren) -- gleicher Weg wie Groesse und Name.
* **Nicht empfohlen:** ModData am Tier als Quelle (jeder Client kann sie ueberschreiben, `ObjectModDataPacket.parse` 51-75, `PLAN.md:231-233`;
  der Plan verbietet `transmitModData` vom Client) und eine zweite Schlaf-Tabelle neben der Variable (zwei Antworten auf eine Frage).
* **Ehrlich:** im MP gibt es z Z z erst mit B8 (und genauso den Schlaf-Clip). Bis dahin: SP ja, MP aus.

---

## 7. Gemeinsame Zeichen-Schicht: `BanditsNPCBearOverlay.lua`

**Ort und Namen (frei geprueft):** `42/media/lua/client/ISUI/BanditsNPCBearOverlay.lua` -- gleicher relativer Pfad in Test-Mod und NPC Crew
(NPC Crew hat seine Overlays dort: NameTags, ForestOverlay, PyreFx). Klasse `BanditsNPCBearOverlay = ISPanel:derive(...)`, Modul
`BanditsNPC.Bear.Overlay`, Client-Datei-Abschnitt `BearOverlay`. Grep in `NPCCrew/42/media`: kein `BanditsNPCBear`, kein
`BanditsNPC.Bear`, kein `UI_BN_Bear_`, kein Abschnitt `Bear`/`BearOverlay` (`CFG_SECTION` nur "NameTags", "Portraits" u. a.).

**Aufbau (Form NameTags/PyreFx, alles oben belegt):**
1. Ein 1x1-ISPanel in der Ecke, `backMost()`, nie vergroessert, nie unsichtbar, Mausfunktionen geben `false`; angelegt in
   `OnGameStart`, geleert in `OnMainMenuEnter`. `require "ISUI/ISPanel"`; NPC-Crew-Module (`BanditsNPC.UI`, `BanditsNPC.ClientCfg`)
   erst IN den Funktionen holen (client/ISUI laedt alphabetisch, PyreFx :47-48) und hinter Existenz-Riegeln (Test-Mod ohne NPC Crew).
2. **Sammler (500 ms):** Liste `vis` = bekannte Baeren, die da sind, gleiche Ebene, <= 45 Kacheln, sichtbar (`isCanSee(0)`), und fuer die
   mindestens eine Zeile etwas zeigt; sortiert nach Abstand, Deckel 8. Je Eintrag gemerkt: Objekt, Groesse, Blickrichtung, `sleep`,
   Werte der Zeilen.
3. **Zeichnen (je Bild im `prerender`):** geteilter Bildschirm -> nichts. Je Eintrag Position frisch, Kopf-Anker (3.3), ausserhalb des
   Bildschirms -> weiter. Dann die **Zeilen von unten nach oben** ab Anker - Abstand: jede Zeile meldet ihre Hoehe und zeichnet sich.
4. **Zeilen als Liste, nicht als Sonderfaelle** (eine Stelle, die stapelt):
   * `bars` (spaeter): Leben, Hunger, Durst, Laune -- je ein waagerechter Balken, links nach rechts gefuellt (`ENTSCHEIDUNGEN.md:105`),
     Form `U.Track` (Grund schwarz 0,5, Rand `U.C.hairline`, Fuellung nach `U.StatBar`-Schwellen, `UIStyle.lua:490-525/920-940`),
     gezeichnet mit `self:drawRect`/`drawRectBorder` (`ISUIElement.lua:1191/1219`). Breite fest (Vorschlag 48 px, an `U.S` gekoppelt),
     Hoehe `U.S(4)`; Hunger/Durst "steigend" (rot wenn hoch), Leben/Laune "fallend".
   * `name` (spaeter): `drawTextCentre`, `UIFont.Small`, Farbe/Schatten wie NameTags :1022/:1035.
   * `zz` (jetzt): Abschnitt 4, beginnt UEBER dem Stapel.
5. **Daten ueber EINE Frage an den Baeren-Kern:** `BanditsNPC.Bear.OverlayInfo(animal)` -> `{ name, hp, hunger, thirst, mood }` (0..1),
   im SP vom Gehirn, im MP aus dem Client-Spiegel (B8: Leben/Hunger/Durst kommen laut `PLAN.md:220` von selbst, Name/Laune muessen
   geschickt werden). Der Schlaf kommt aus der Variable (Abschnitt 6). Das Overlay rechnet selbst keine Werte aus.
6. **Einstellungen JE SPIELER** (`ENTSCHEIDUNGEN.md:106`): `BanditsNPC.ClientCfg.Table("BearOverlay")` mit `zz`, `name`, `hp`, `hunger`,
   `thirst`, `mood` (Vorgabe an, Abfrage `== nil`, NameTags :287-292), `Save()` nach jeder Aenderung (`BanditsNPCClientCfg.lua:139/145`).
   Ohne NPC Crew (Test-Mod): nur im Speicher mit Vorgabe an. Geschaltet wird spaeter im Baeren-Fenster/-Menue (echte Spielmechanik, kein
   Cheat). Texte dafuer `UI_BN_Bear_Show*` in sieben Sprachen erst mit dem Menue.
7. **Was NIE hinein darf:** Konsolenbefehle, Testmenues, Zwangsschlaf -> `NCBearBench.lua` (z. B. `NCBear_Sleep()` zum Pruefen der
   Saeule, Regler-Befehle 3.5). Fehler hinter `pcall`, je Grund hoechstens einmal je Minute melden (Form `BanditsNPC.ErrEvery`,
   `BanditsNPCClientCfg.lua:165`), Diagnose nur hinter Schalter.
8. **Naehte mit NPC Crew (nur lesend, keine NPC-Crew-Datei geaendert):** `BanditsNPC.ClientCfg` (Datei `NPCCrewClient.ini`, neuer Abschnitt),
   `BanditsNPC.UI.C` (Farben, Schema "night"). Beide in die Naht-Liste des Baeren (Vorbild `turret/NAEHTE.md`). Optisch: Baeren-Name in
   derselben Schrift/Farbe wie NPC-Namen; bei NPC und Baer dicht beieinander koennen sich Name und Baeren-Stapel ueberlappen (im Spiel ansehen).

**Spaetere Balken passen ohne Umbau:** neue Zeile in die Liste, ein Schalter mehr, ein Feld mehr in `OverlayInfo`. Die Kosten wachsen je
Balken um 3 Zeichenaufrufe je Baer und Bild (Grund, Fuellung, Rand).

Skizze nur der z Z z-Rechnung (fuer den Bauer; reine Mathematik, Beispielwerte in `zz/zz_kurve.lua`):
```lua
-- t = Sekunden seit die Schlaf-Schleife laeuft (eigene Uhr, steht bei isGamePaused()), k = 0..2
local born = k * LIFE / 3
if t >= born then
    local u = ((t - born) / LIFE) % 1
    local s = 0.55 + 0.45 * math.sin(math.pi * u)
    local a = math.min(1, u / 0.15) * math.min(1, (1 - u) / 0.35) * fadeAll
    local up, side = RISE * u, DRIFT * u + WOB * math.sin(2 * math.pi * u)
    -- zoom = H * s / fontH; w = MeasureStringX(font, "Z") * zoom
    -- self:drawTextZoomed("Z", x - w/2 + sh, y + sh, zoom, 0, 0, 0, 0.65 * a, font); danach in (0.96, 0.96, 0.90, 0.95 * a)
end
```

---

## 8. Risiken

1. **Kopfhoehe/-vorlage geraten**, bis der Schlaf-Clip steht (3.4). Gegenmittel: Regler (3.5), Messung im Clip-Bau.
2. **Vorwaertsrichtung = Modellblick am Tier ungeprueft** (3.3). Faellt es falsch aus, steht die Saeule ueber dem Hintern -> im ersten
   Test von allen Seiten ansehen; Rueckfall: ueber der Mitte (Vorlage 0).
3. **MP erst mit B8.** Ohne die Variable an jedem Client gibt es im MP weder Clip noch z Z z. Gleichheit von `getAnimalID()` auf
   Server und Client ungeprueft.
4. **Sichtkegel:** `isCanSee(0)` laesst die Saeule verschwinden, sobald der Spieler sich wegdreht (wie NPC-Namen). Ohne die Frage
   zeigte sie durch Waende. Bewusst wie NPC Crew.
5. **Alles liegt UEBER der Welt** (UI-Schicht): ein Baum oder Dach vor dem Baeren verdeckt die Buchstaben nicht (PyreFx :13-16, Turret
   `BanditsNPCTurretFx.lua:7`).
6. **Splitscreen:** keine Anzeige (wie NPC Crew).
7. Statisch geprueft, nicht gespielt: wie gross die Saeule in 4K wirkt, ob 2,4 s ruhig genug ist, ob "Z" in Large verkleinert sauber
   bleibt -- im ersten Test ansehen.

## 9. Fragen an Kevin

1. **Farbe:** wie die NPC-Namen (fast weiss) oder ein Hauch Nachtblau?
2. **Abschaltbar je Spieler** wie Name und Balken (Vorschlag: ja, Schalter "z Z z" im Baeren-Menue, Vorgabe an)?
3. **Zoom:** Buchstaben immer gleich gross auf dem Bildschirm (wie NPC-Namen, Vorschlag) oder mit dem Herauszoomen kleiner werden?
4. **Hinter dem Ruecken/Waenden:** verschwinden wie NPC-Namen (Vorschlag) oder immer zeigen, solange der Baer auf dem Bildschirm ist?
5. Reihenfolge: z Z z zusammen mit dem Schlaf-Clip bauen (Vorschlag), Namensschild/Balken spaeter in dieselbe Datei.

---

## Belegliste (jede vorgeschlagene Engine-Frage)

| Aufruf | Argumenttypen | Fundstelle |
|---|---|---|
| `ISPanel:derive`, `:new(0,0,1,1)`, `:initialise()`, `:instantiate()`, `:addToUIManager()` | Zahlen | NPC Crew NameTags :136, :1182-1187 (gespielt); Vanilla 1x1-Element `ISButtonPrompt.lua:1244` |
| `:backMost()` | - | Vanilla `client/Fishing/FishingManager.lua:41` |
| `isoToScreenX/Y(0, x, y, z)` | int, float, float, float | Vanilla `TensionUI.lua:11-12`; Jar `GlobalObject.isoToScreenY` (dump :1634) |
| `self:drawTextZoomed(str, x, y, zoom, r, g, b, a, font)` | String, Zahlen, UIFont | Vanilla `ISUIElement.lua:1260`; NPC Crew NameTags :1116-1117 |
| `self:drawTextCentre(str, x, y, r, g, b, a, font)` | String, Zahlen, UIFont | `ISUIElement.lua:1280`; Bandits `BanditEventMarkers.lua:176` |
| `self:drawRect(x, y, w, h, a, r, g, b)`, `self:drawRectBorder(...)` | Zahlen | `ISUIElement.lua:1191`, `:1219`; NPC Crew `UIStyle.lua:368-374` |
| `getTextManager():getFontHeight(UIFont.Medium)` | UIFont | Vanilla `ISAddNonPvpZoneUI.lua:4` |
| `getTextManager():MeasureStringX(font, str)` | UIFont, String | Vanilla `ISButton.lua:233` |
| `getCore():getScreenWidth()` / `getScreenHeight()` | - | Vanilla `TensionUI.lua:11`; NPC Crew NameTags :962-963 |
| `getNumActivePlayers()` | - | Vanilla `FishingHandler.lua:6` |
| `getTimestampMs()` | - | Vanilla `client/Chat/ISChat.lua:469` |
| `isGamePaused()` | - | Vanilla `client/Foraging/ISSearchManager.lua:1462` |
| `square:isCanSee(0)` | int | Vanilla `ISBaseIcon.lua:256` (`self.player` = Zahl, :870) |
| `getCell():getObjectListForLua()`, `instanceof(o, "IsoAnimal")` | -, Objekt/String | Vanilla `DebugContextMenu.lua:616-620` |
| `animal:getAnimalType()` | - | Vanilla `ISAnimalUI.lua:65` |
| `animal:isExistInTheWorld()`, `animal:isDead()` | - | Vanilla `ISAnimalUI.lua:15`; `NCBearFight.lua:1762-1764` |
| `animal:getVariableString(name)` | String | Vanilla `ISWorldObjectContextMenu.lua:2624` (am Spieler); am Baeren `NCBearFight.lua:1349` |
| `animal:setVariable(name, wert)` | String, String | Vanilla `shared/TimedActions/Animals/ISPetAnimal.lua:43` (am Tier) |
| `animal:getData():getSize()` | - | Vanilla `ButcheringUtil.lua:568` (an `IsoAnimal.new`) |
| `animal:getForwardDirection()`, `:getX()`, `:getY()` | - | Bandits `ZAPush.lua:36-37` (Zombie); Vanilla `ISBaseIcon.lua:216` (IsoPlayer); IsoAnimal erbt (Jar) |
| `animal:getAnimalID()` | - | Vanilla `ISAnimalUI.lua:53`, `ISVehicleAnimalUI.lua:199` |
| `sendServerCommand(modul, befehl, args)` / `Events.OnServerCommand.Add` | String, String, Tabelle | Vanilla `ISPickupDung.lua:45` / `client/ServerCommands.lua:218` |
| `BanditsNPC.ClientCfg.Table(abschnitt)`, `.Save()` | String | NPC Crew `client/BanditsNPCClientCfg.lua:139`, `:145` |

**Nicht vorgeschlagen (nur Jar oder ungeeignet):** `addLineChatElement`/`Say` am Tier, `HaloTextHelper`, `setCustomName`,
`getAttachmentWorldPos` (nur gelesen, um die Masse zu belegen; kein Lua-Aufruf in Vanilla oder Bandits).
