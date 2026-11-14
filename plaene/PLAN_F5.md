# Lauf baer-f5: PLAN -- Spuernase-Anzeige (ESP) + Fischen

Stand 14.11.2026 ~08:30 (Planungs-Lauf baer-plaene-1114, Rolle PLAN + FORSCHUNG). **Statisch geprueft, nicht gespielt.** Kein Mod-Code gebaut.
Geschrieben nur unter `_arbeit/baer_zaehmen/plaene_1114/`: diese Datei, `werkzeug_f5/` (Fisch-Rechnung, Entwurf-Zeichner, Jar-Zieher),
`jar/f5/` + `jar/f5_dec/` (Jar-Klassen + Vineflower, nur gelesen), `bilder/ENTWURF_nase_DE_1080.png` / `_4k.png`, `bilder/nase_texturen/` (Vorschlag).

Grundlage (geht vor): `baer/begleiter/ENTSCHEIDUNGEN.md` (`E:Zeile`), ab :686 bis :853 ganz gelesen, dazu :25-31, :209-229, :424-439;
`baer/begleiter/bedarf_echte_baeren.md` (`BE:Zeile`); `baer/STAND.md` oben; Form wie `k1/PLAN_K1.md`.
Kuerzel: `T:` = Test-Mod `Zomboid/mods/NCBearTest/42/media/lua/` (Git main 1f7b641 = F1..F4 + Liegen + K1 + Kampf), `TM:` = `.../42/media/`,
`V:` = Vanilla `ProjectZomboid/media/lua/`, `VS:` = Vanilla `media/scripts/`, `J:` = Jar 42.22 dekompiliert `plaene_1114/jar/f5_dec/*.java`,
`B:` = Bandits `42.22/media/lua/`, `NC:` = NPC Crew `42/media/lua/` (nur gelesen, nichts kopiert). `B` = `BanditsNPC.Bear`, `U` = `B.UI`.

---

## 0. Kurzfassung

1. **Umriss (Weg a) geht NICHT fuer das, was Kevin will** (Jar gelesen): ein Zombie, den du nicht siehst, bekommt Ziel-Alpha 0
   (`J:IsoGameCharacter.java:9154-9163`, Sicht-Test `:2269-2333`) und wird dann GAR NICHT gezeichnet (`J:IsoGameCharacter.java:6382-6386`); der
   Umriss entsteht nur beim Zeichnen des Modells (`J:ModelSlotRenderData.java:183`, `:758-767`). Fuer sichtbare Zombies scheint er zwar durch
   Waende (eigener Puffer, oben drueber geblendet, `J:ModelOutlines.java:93-207`), aber die zeigt das Spiel ja schon. Dazu loescht die Engine den
   Umriss jedes Bild wieder (`J:IsoMovingObject.java:1095-1112`).
2. **Empfehlung Weg (b): eigene Markierung auf dem Bildschirm** im vorhandenen Anzeige-Element (`T:client/ISUI/BanditsNPCBearHud.lua:1006-1045`):
   Ecken-Rahmen Fuss..Kopf + Nasen-Bild + Ring am Boden, Baeren-Orange, 3 Bild-Aufrufe je Zombie. Entwurf `bilder/ENTWURF_nase_DE_1080.png`.
   "Siehst du ihn nicht?" = genau die Entscheidung der Engine: `z:getTargetAlpha(0) <= 0,001` (`V:client/DebugUIs/DebugChunkState/
   DebugChunkState_ObjectProperties.lua:94`); die Markierung blendet mit `1 - z:getAlpha(0)` weich ein, waehrend der Zombie ausblendet.
3. **Nur Client-Anzeige**, nur fuer den Besitzer, nur eigener, wacher, geladener Baer; Weite = vorhandener Wert `nose` (12 + 1,5 je Stufe,
   `T:shared/BanditsNPCBearStats.lua:395`). Schalter = vorhandener Zahnrad-Punkt "Nasen-Warnung" (`T:client/BanditsNPCBearWinData.lua:1088`) wird
   scharf, je Baer gespeichert wie "Lebensbalken". Brummen (Ton, nur grosser Koerper) bei neuen Zombies, hoechstens alle 20 s. Spuernase-Erfahrung
   rechnet nur der Server. Deckel 24 Markierungen, Suche je 500 ms. **Kein neuer Netz-Befehl, kein neuer Sandbox-Regler.**
4. **Fischen nach Kevins Regel 12.11.** (`E:430-439`): Ertrag = NPC-Angler von NPC Crew mit gleicher Stufe (`NC:shared/BanditsNPCSkills.lua:933-939`,
   `NC:shared/BanditsNPCFishing.lua:1731-1855`, `:2489`) x Groesse 0,5 (halbstark) .. 1,0 (ausgewachsen), Junges fischt nicht, jedes Vanilla-Wasser.
5. **Rechnung (Vanillas Fischtabellen, `werkzeug_f5/fisch_rechnung.lua`):** ausgewachsen Stufe 0 bringt wie ein NPC ~14 Hungerpunkte je Stunde,
   braucht aber ~43 je Wachstunde (691 je volle Leiste, K1) -> heute verhungert er beim Fischen. **Vorschlag (Frage F5-5):** hungrig (ab 25 %)
   3x so viele Versuche und frisst den Fang sofort; satt angelt er wie ein NPC und packt ein (die Basis bleibt "nicht broken", Kevin `E:426-433`).
6. **Ablauf:** Knopf "Fischen" (heute grau, `T:client/BanditsNPCBearWinData.lua:1052`) = 5. Modus "fish": Wasser bis 20 Kacheln um den Baeren
   suchen (Vanillas Wasser-/Ufer-Regel `V:client/ISUI/ISWorldObjectContextMenu.lua:683-719`), hingehen, alle 10-15 Spielminuten ein Versuch,
   Fisch wie Vanillas Fischnetz am Server bauen (`V:server/Fishing/BuildingObjects/FishingNet.lua:121-146`), ins Inventar ueber die F4-Schnittstelle
   `B.InvAddItem` (`T:server/BanditsNPCBearInv.lua:1049-1062`) oder sofort fressen ueber `B.NeedEat` (`T:server/BanditsNPCBearNeeds.lua:321-333`).
7. **Bild:** bis zum Modell-Lauf Ersatz aus vorhandenen Clips (Sitzen = warten, "swipeL" = Hieb, "eat" = kauen) + Wasser-Spritzer
   (`V:shared/Fishing/Fish.lua:58`) + Vanilla-Ton "StrikeWithFishingSpear"/"CatchFish". Der Modell-Lauf bringt "fishwait"/"fishstrike" (Abschnitt 12).
8. **Kein neuer Nur-Jar-Aufruf.** Zwei Grenzfaelle mit Pruef-Tor (G-N1 getTargetAlpha am MP-Client, G-F1 faceThisObject auf ein Kachel-Objekt).
   Bau: 8 Agenten (Abschnitt 11). 8 Fragen an Kevin (Abschnitt 15).

---

## 1. Was Kevin will (woertlich)

- **Spuernase-ESP** (`E:842`): *"der gespuersinn von den baeren soll machen wenn moeglich das zombies in der naehe die der spieler nicht sehn kann weil
  in gebaeuden oder hinter ihn mit wallhack (esp) angezeigt werden"*. Vorher fest (`E:220`): *"die spuehrnase auch einbauen aber in den einstellungen
  abschaltbar falls es jemand nervig findet wenn er staendig sagt zombie in der naehe"* -> riecht frueher, warnt mit Brummen, abschaltbar, nicht
  staendig (Abklingzeit, nur bei neuen Zombies). Claudes Weg-Notiz dazu `E:843-847` (Umriss pruefen, sonst Marker; nur Besitzer, wach, nah; MP Client).
  Zahnrad (`E:818` I1): "Nasen-Warnung" gehoert ins Zahnrad-Menue.
- **Fischen** (`E:31`): *"streift an See oder Fluss, faengt Fische, legt sie ins eigene Inventar und frisst sie selbst"*; (`E:211-213`) ab halbstark,
  *"nur schlecht und dann am ende viel besser"*; **Balance 12.11.** (`E:426-433`): *"halbstark schlechter als ein npc und ausgewachsen besser als ein npc
  aber nicht viel besser weil sonst wird der die ganze base alleine versorgen das waere broken ... ich eher angeln 50% so stark wie ein npc und
  ausgewachsen fuer die balance genauso stark wie ein npc"*; (`E:437-438`) *"einfach wasser das reicht"*.
- **Neu 14.11.** (`E:809`): *"fischen vom baeren staerker machen weil er soviel frisst"*; (`E:810`) *"rausfinden wie viel naehrwert der baer essen muss zb
  wie viele fische noetig baeren damit er satt wird am tag"*. Talent 7 "Angler" (`E:836`, faengt doppelt so viel) kommt mit PLAN_TALENTE.
- **Rahmen K1** (`E:737-740`, `:795-799`): frisst selbst ab 50 % bis 0 %; Hunger 0 -> 100 % in 16 Wachstunden = eine Tagesmenge (ausgewachsen
  691 Hungerpunkte, `k1/PLAN_K1.md:20-22`); Beduerfnisse frieren (Schlaf, offline, > 70 Kacheln, `E:747-752`, `:760-761`).

Widerspruch 12.11. <-> 14.11.: "genauso stark wie ein NPC" gegen "staerker". Kevins neueres Wort geht vor, aber sein Grund von 12.11. ("sonst
versorgt er die ganze Basis") bleibt gueltig -> Vorschlag F5-5 (a) trennt beides: staerker nur fuer das, was er SELBST frisst.

---

## 2. N -- Spuernase-Anzeige

### 2.1 Forschung: Vanillas Umriss (Weg a), Jar 42.22 gelesen
| Frage | Befund | Fundstelle |
|---|---|---|
| Lua-Aufruf | `chr:setOutlineHighlight(n, true)` + `setOutlineHighlightCol(n, r, g, b, a)` am Charakter (n = Spielernummer); ohne n am Debug-Fenster | `V:server/BuildingObjects/ISPickCharacterCursor.lua:48-49`, `V:client/DebugUIs/ISDebugAnimationTextUI.lua:36-37` |
| Wo gezeichnet | nur in `ModelSlotRenderData`, wenn das Modell des Charakters gezeichnet wird (`characterOutline = isOutlineHighlight(n)` beim Vorbereiten, Zeichnen in `renderCharacter`) | `J:ModelSlotRenderData.java:183`, `:316-321`, `:758-767`, `:962-1004` |
| Durch Waende? | ja, fuer GEZEICHNETE Modelle: Umriss in eigenen Puffer (fboA), verdickt, als Bildschirm-Bild oben drueber geblendet | `J:ModelOutlines.java:79-207` |
| Unsichtbare Zombies? | **nein**: nicht gesehen -> `setTargetAlpha(n, 0)`; `render` bricht bei Alpha UND Ziel-Alpha 0 ab -> kein Modell -> kein Umriss | `J:IsoGameCharacter.java:9154-9163`, `:6381-6386`; Sicht-Test `:2269-2333` (Sichtweite, couldSee/canSee, Erkennungsweite, Licht, Blickrichtung) |
| Haelt er? | Engine loescht ihn in `renderlast` jedes Bild, ausser er wurde im selben UI-Bild gesetzt -> jedes Bild neu setzen | `J:IsoMovingObject.java:1095-1112`, `J:IsoObject.java:5400-5422` |
| Sonst | nur EIN Farbpuffer je Bild; jeder Farbwechsel zwingt einen Zwischendurchgang | `J:ModelOutlines.java:79-93` |
-> **Weg (a) zeigt genau die Zombies NICHT, um die es geht.** Er wird nicht gebaut (auch nicht als Zusatz fuer sichtbare: die zeigt das Spiel).

### 2.2 Weg (b): eigene Markierung (Empfehlung)
- **Wo gezeichnet:** im vorhandenen Anzeige-Element des Baeren (ISPanel bei 0,0, Bildschirm-Koordinaten), in `Hud:prerender` VOR den Schildern:
  `if U.NoseDraw then U.NoseDraw(self, now) end` (Form wie `U.FloatDraw`/`U.ZzDraw`, `T:client/ISUI/BanditsNPCBearHud.lua:1042-1044`). Geteilter
  Bildschirm: aus (wie das Element selbst, `:1010-1016`). Bandits' Weg (`B:client/BanditProjectile.lua:10` `ISCoordConversion.ToScreen`, `:160`
  `getRenderer():renderPoly`, `:172` `Events.OnPreUIDraw`) ginge auch, braucht aber Zoom-Rechnung von Hand; das Hud-Element hat alles schon.
- **Bildschirm-Lage:** `isoToScreenX/Y(0, x, y, z)` (`V:client/Fishing/TensionUI.lua:11-12`) fuer Fuss (z) und Kopf (z + `noseHeadZ` 0,8, wie
  `DMG_LIFT` `T:client/BanditsNPCBearFx.lua:55`) -> Hoehe h in Pixeln waechst und schrumpft mit dem Zoom von selbst.
- **Zeichnen:** je Zombie 3 x `self:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` (`V:client/ISUI/ISUIElement.lua:1032`) mit weissen Bildern,
  gefaerbt ueber r, g, b. Bilder `getTexture("media/ui/BanditsNPCBearNose*.png")` (Form `V:client/Chat/ISChat.lua:137`).
- **"Siehst du ihn nicht?"**: `z:getTargetAlpha(0) <= noseSeenA` (0,001 = die Engine-Schwelle `J:IsoObject.java:1920-1922`); Fundstelle
  `obj:getTargetAlpha(pn)` / `obj:getAlpha(pn)` mit Zahl `V:client/DebugUIs/DebugChunkState/DebugChunkState_ObjectProperties.lua:93-94`
  (dort an einem Kachel-Objekt; die Methode gehoert IsoObject `J:IsoObject.java:1673`, `:1898`, der Zombie erbt sie -- gleiche Argumentart Zahl).
  Rueckfall, falls Pruef-Tor G-N1 scheitert: Kachel nicht sichtbar `sq:isCanSee(0) == false` (`V:client/Foraging/ISBaseIcon.lua:256`, Spielernummer
  `:870`) -- ungenauer (die Engine zeigt nahe Zombies hinter dir trotzdem, `J:IsoGameCharacter.java:2282-2285`).
- **Weiches Ein-/Ausblenden:** Deckkraft je Bild = `(1 - z:getAlpha(0))` x Puls (0,75..1,0 in `nosePulseMs` 1400) x Einblenden (`noseFadeMs` 300):
  die Markierung erscheint genau so, wie der Zombie verschwindet -- kein Doppelbild, kein Springen.

### 2.3 Wer, wann, welche Zombies (Regeln, alles Client)
- **Baer:** Sicht-Eintrag mit `st == "tame"`, `U.WinMine(v)` (`T:client/BanditsNPCBearWinData.lua:351-355`), wach (`v.slp ~= true`), nicht mitfahrend
  (`v.ride == nil`), geladen (`v.ld`), nicht am Boden (`v.dn ~= true`), Schalter an (`U.NoseOn(v)`), lebende Client-Kopie `U.CubObj(id)`
  (`T:client/ISUI/BanditsNPCBearHud.lua` B1c-Block). Gilt in JEDEM Modus (Frage F5-4). Junges auch (Weite bis 16,5 Kacheln, Alters-Deckel Stufe 3).
- **Weite:** `v.nose` aus der Sicht (Kern rechnet `noseBase + noseStep x Stufe`, `T:shared/BanditsNPCBearStats.lua:395`; Sicht `T:server/BanditsNPCBearGrow.lua:995`),
  gemessen vom BAEREN (seine Nase), Ebenen-Abstand hoechstens `noseZ` 1 (Keller/Obergeschoss im Haus).
- **Zombies:** mit Bandits die Lua-Tabelle `BanditZombie.CacheLightZ` (nur Zombies OHNE Banditen, `B:client/BanditZombie.lua:11-12`, `:121-149`) +
  `BanditZombie.GetInstanceById(id)` (prueft Kennung und Welt, `:176-186`); ohne Bandits `getCell():getZombieList()` + `:size()` + `:get(i)`
  (`B:client/BanditZombie.lua:110-115`) und `z:getVariableBoolean("Bandit")` (`:131`) als Filter. Lebt: `z:isAlive()` (`:49`). Lage
  `z:getX()/getY()/getZ()` (`:125`). Liegend/kriechend: `B.FoePosture(z) == "down"` (`T:shared/BanditsNPCBearFoe.lua:91-94`) -> flacher Rahmen.
  NPC-Crew-Figuren und Banditen werden nie markiert (spaeter rote Feind-Banditen = eigene Frage, nicht F5).
- **Ablauf:** je `noseScanMs` 500 eine Liste (hoechstens `noseScanCap` 1500 Eintraege ansehen, `noseMax` 24 naechste behalten, je Eintrag
  Objekt + Abstand + Haltung); je Bild nur aus dieser Liste zeichnen (Lage je Bild frisch vom Objekt, damit nichts nachzieht).

### 2.4 Aussehen und Masse (Entwurf `bilder/ENTWURF_nase_DE_1080.png`, `_4k.png`; Zeichner `werkzeug_f5/zeichne_nase_entwurf.py`)
| Teil | Bild (weiss, gefaerbt) | Masse (h = Pixel Fuss..Kopf) |
|---|---|---|
| Ring am Boden | `media/ui/BanditsNPCBearNoseRing.png` 256x64 | 1,4 h x 0,36 h, Mitte am Fuss, Deckkraft 0,55 |
| Ecken-Rahmen | `BanditsNPCBearNoseBox.png` 128x256 (liegend `...NoseBoxLow.png` 256x104: 1,0 h x 0,38 h) | 0,5 h x 1,0 h, Unterkante am Fuss, Deckkraft 0,95 |
| Nasen-Bild | `BanditsNPCBearNose64.png` / `...128.png` (farbig, nicht gefaerbt; Wahl wie das Herz: groesstes, das nicht groesser ist) | 0,30 h, 12..48 px, 0,06 h ueber dem Rahmen |
- Farbe `noseR/G/B` = Baeren-Markierung 1,00 / 0,52 / 0,09 (`T:shared/BanditsNPCBear.lua:182`). Vorschlag-Bilder liegen in `bilder/nase_texturen/`
  (OBERFLAECHE darf sie verbessern; Quelle bleibt ein Skript wie beim Herz, `f3/herz/herz_zeichne.py`).
- Kein Text an der Markierung (keine Sprache, kein Platz). Zombies ausserhalb des Bildschirms: nichts (Rand-Pfeile = spaeter, nur auf Kevins Wort).

### 2.5 Brummen und Spuernase-Erfahrung
- **Brummen (Client, nur der Besitzer hoert es):** steigt die Zahl der UNSICHTBAREN Markierungen eines Baeren von 0 auf >= 1 und war es davor
  `noseCalmMs` 20000 ruhig -> `a:playBreedSound("huffsoft")` an der Client-Kopie (Form `T:client/BanditsNPCBearFx.lua:233-235`, Vanilla
  `V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19`). Nur grosser Koerper (das Junge hat keine Stimme, `T:shared/BanditsNPCBearDefs.lua:68-76`
  gegen `:180-186`). Schalter aus -> kein Ton. Nicht im Kampf (er knurrt dann ohnehin).
- **Erfahrung (Server/SP-Schreiber):** je `noseXpMs` 3000 fuer alle wachen, geladenen, gezaehmten Baeren EIN Aufruf `B.ZedNear(punkte, r, maxN)`
  (`T:server/BanditsNPCBearWorld.lua:425-500`, r = groesste Nasen-Weite); naechster Zombie in SEINER Weite und davor `noseCalmMs` keiner -> `B.OnSniff(rec, ms)`
  (`T:server/BanditsNPCBearGrow.lua:431-433`, `xpSniff` 5; Echtzeit-Deckel je Faehigkeit gilt). Unabhaengig vom Schalter (Faehigkeit waechst immer).
  Nur, wenn er zaehlt (eingefroren = nichts, `T:server/BanditsNPCBearNeeds.lua:249-264` `counts`, als `B.NeedCounts` ausgeben).

### 2.6 Zahnrad-Schalter "Nasen-Warnung"
- `T:client/BanditsNPCBearTags.lua`: vierte Liste `"noseoff <u>"` (Form `tag`/`age`/`hp` `:41-45`; IMMER alle Listen schreiben; alte Datei laedt
  unveraendert = alle an), neu `U.NoseOn(c)` / `U.NoseSet(c, on)` (Form `:166-174`). Vorgabe AN (Frage F5-2).
- `T:client/BanditsNPCBearWinData.lua:1087-1088`: Punkt `nose` ohne `off`, `on = U.NoseOn(v)`, Tooltip `UI_BN_Bear_Win_NoseTip` mit Weite (`v.nose`).
- `T:client/ISUI/BanditsNPCBearWindow.lua:600-619` `Win.onGearPick`: Zweig `key == "nose"` -> `U.NoseSet(v, not U.NoseOn(v))` (Kommentar :617 weg).

### 2.7 Leistung (Deckel)
Suche 2 x je s, hoechstens 1500 Eintraege (reines Lua bei Bandits); hoechstens 24 Markierungen x (3 Bild-Aufrufe + 4 Lage-Abfragen + 2 Alpha-Abfragen)
je Bild = 72 Bild-Aufrufe (Hud-Deckel heute 150, `T:client/ISUI/BanditsNPCBearHud.lua` F3-Kopf). Kein `getText`, keine Suche je Bild. Server: 1 Aufruf
`B.ZedNear` je 3 s fuer alle Baeren zusammen.

### 2.8 SP / MP
- SP (`not isServer() and not isClient()`, `B.IsSP` `T:shared/BanditsNPCBear.lua`): alles in einem Programm. MP: Anzeige NUR auf dem Client
  (dedizierter Server laedt `client/` nicht), Erfahrung NUR am Server. Kein neuer Befehl Client->Server, kein Gegenstand, nichts haengt.
- **G-N1 (Pruefer, Jar):** laeuft `updateSeenVisibility` auf dem MP-Client auch fuer fremd gesteuerte Zombies (`J:IsoGameCharacter.java:8857-8859`
  `if (!GameServer.server)`, Aufrufer pruefen)? Nein -> Rueckfall `isCanSee` (2.2).
- **G-N2:** `BanditZombie.CacheLightZ` auf dem MP-Client gefuellt (`B:client/BanditZombie.lua:99` `if isServer() then return end`)? Sonst Zellenliste.

---

## 3. F -- Fischen

### 3.1 Forschung: NPC-Angler (NPC Crew, nur gelesen) und Vanillas Fischdaten
| Teil | Wert | Fundstelle |
|---|---|---|
| Chance je Wurf | `(0,35 + 0,03 x Stufe) x (0,5 + 0,5 x bester Lockwert des Koeders)` | `NC:shared/BanditsNPCSkills.lua:342-343`, `:933-939`; `NC:shared/BanditsNPCFishing.lua:1763-1766`, `:2489` |
| Konstanten lesbar | `BanditsNPC.Skills.FX.fishBase / fishCatchPerLvl` (ausgegeben `S.FX = FX`) | `NC:shared/BanditsNPCSkills.lua:371` |
| Wurf-Dauer | 10..15 Spielminuten | `NC:shared/BanditsNPCFishing.lua:67-68` (`F.CAST_MIN/MAX_MINUTES`) |
| Wer beisst | Arten mit `maxWeight <= Fishing.Utils.skillSizeLimit[Stufe]` und Lockwert > 0, gewichtet nach Lockwert | `NC:...Fishing.lua:1731-1754`, `:1770-1794`; `V:shared/Fishing/FishingUtils.lua:161-172` (1,4 kg .. 45 kg) |
| Groesse | `getFishSizeChancesBySkillLevel(Stufe, false, 1)` -> Klein/Mittel/Gross, dann `cfg:getFishSizeData(s, m, b)` | `NC:...Fishing.lua:1817-1825`; `V:shared/Fishing/FishingUtils.lua:175-206`; `V:shared/Fishing/fishing_properties.lua:146-213` |
| Saettigung | `max(Gewicht kg / weightFactor, 0,05)` = BaseHunger (x 100 = Hungerpunkte) | `V:shared/Fishing/Fish.lua:194-205`, `V:server/Fishing/BuildingObjects/FishingNet.lua:132-144` |
| Arten | 21 in `Fishing.fishes` (z. B. Bluegill 1,4 kg/wf 2, Largemouth 2,8/2, Striped Bass 9/4, Blue Catfish 32/6, Alligator Gar 45/6, BaitFish 0,05/6) | `V:shared/Fishing/fishing_properties.lua:216-663` |
| Gegenstand | z. B. `Base.LargemouthBass` Gewicht 0,4, HungerChange -15, `OnCreate = Fishing.onCreateFish` (wird beim Bauen ersetzt) | `VS:generated/items/food.txt:7080-7100`; `V:shared/Fishing/fishing_properties.lua:709-750` |
| Baer heute | Platzhalter `fishBase 10 / fishMax 60` (%), `B.OnFish` (Haken ohne Aufrufer, ab halbstark) | `T:shared/BanditsNPCBear.lua:191`, `T:shared/BanditsNPCBearStats.lua:387-394`, `T:server/BanditsNPCBearGrow.lua:423-429` |

Rechnung `werkzeug_f5/fisch_rechnung.lua` (Lua 5.1 laedt Vanillas `fishing_properties.lua` + `FishingUtils.lua`, Erwartungswerte, Koeder-Bezug Wurm),
Ausgabe `werkzeug_f5/fisch_rechnung_ausgabe.txt`:
| Stufe | Chance/Wurf | kg je Fang | Hunger je Fang | Fische/h | Hunger/h (NPC) | Fische je volle Leiste ausgewachsen (691) |
|---|---|---|---|---|---|---|
| 0 | 33 % | 0,17 | 8,6 | 1,6 | 13,8 | 80 |
| 3 | 42 % | 0,30 | 15,1 | 2,0 | 30,2 | 46 |
| 5 | 48 % | 0,50 | 23,6 | 2,3 | 53,9 | 29 |
| 8 | 56 % | 2,26 | 61,0 | 2,7 | 164,2 | 11 |
| 10 | 62 % | 3,68 | 85,8 | 3,0 | 254,2 | 8 |
Zum Vergleich echte Baeren: Brooks Falls im Mittel ~15 Lachse je Tag (`BE:39`) -- Stufe 8-10 liegt dort.

### 3.2 Kevins Regel + Vorschlag "staerker" (Frage F5-5)
- **Fest:** Chance je Versuch = NPC-Formel (Konstanten aus `BanditsNPC.Skills.FX`, fehlt NPC Crew: Kopie `fishNpcBase 0,35` / `fishNpcStep 0,03` mit
  Fundstelle) x Wurm-Lockwert (`fishLure "Base.Worm"`, Vanillas haeufigster Koeder; der Baer braucht keinen) x **Groesse `gk`** = 0,5 bei halbstark
  (innere Groesse 0,75) bis 1,0 bei ausgewachsen (1,35), dazwischen gleitend wie `grown` (`T:shared/BanditsNPCBearStats.lua:389-391`). Junges: 0.
  Arten/Groesse wie 3.1 mit der Fischen-Stufe des Baeren (0..10, Alters-Deckel `skillCapAt`). Talent "Angler" spaeter als Faktor `B.FishK(rec)` (heute 1).
- **Problem:** ausgewachsen braucht ~43 Hungerpunkte je Wachstunde (691/16). Wie ein NPC: Stufe 0 = 14/h (verhungert beim Fischen), Stufe 5 = 54/h.
- **Vorschlag (a, Empfehlung):** solange Hunger >= `fishHungryAt` 25 % -> Versuche `fishHungryK` 3x so oft, Fang wird sofort gefressen. Darunter: Tempo
  wie ein NPC, Fang in die Taschen (Vorrat wie NPC = Kevins 12.11.-Balance). Folgen (hungrig):
  | | Stufe 0 | Stufe 3 | Stufe 5/6 | Stufe 8 | Stufe 10 |
  |---|---|---|---|---|---|
  | halbstark (221/Leiste, 13,8/h) | 20,7/h -> 10,7 h | 45/h -> 4,9 h | (6) 108/h -> 2,0 h | -- | -- |
  | ausgewachsen (691/Leiste, 43,2/h) | 41/h -> 16,7 h (haelt sich knapp) | 91/h -> 7,6 h | (5) 162/h -> 4,3 h | 493/h -> 1,4 h | 763/h -> 0,9 h |
  Andere Antworten: (b) immer x2, auch Vorrat (Vorrat doppelt so gross wie ein NPC); (c) immer x3; (d) wie NPC (dann fuettert man ihn nebenbei).

### 3.3 Ablauf (KERN, nur Schreiber; neue Datei `server/BanditsNPCBearFish.lua`, Regeln `shared/BanditsNPCBearFishRules.lua`)
1. **Befehl:** Knopf "Fischen" schickt die vorhandene Bitte "Mode" mit `mode = "fish"` (`B.HandleMode`, `T:server/BanditsNPCBearFollow.lua:294`).
   `B.MODES` + `fish` (`T:shared/BanditsNPCBear.lua:388`, auch `MODES_DEF` in Follow :101, Rules :371, Heal :92, Registry :138). Ablehnen mit Notiz:
   Junges (`rankOf(g) < 1` wie `B.OnFish`), mitfahrend, am Boden, kein Wasser.
2. **Wasser suchen (einmal je Befehl, Deckel):** Ringe d = 1..`fishR` 20 um den BAEREN, Ebene 0: Wasser = `sq:getFloor():hasProperty(IsoFlagType.water)`
   (`V:client/ISUI/ISWorldObjectContextMenu.lua:683-688`, im Baer schon `T:server/BanditsNPCBearWorld.lua:98-101`); Standplatz = Nachbar-Kachel ohne Wasser,
   nicht `isSolid()`/`isSolidTrans()`, Boden da (`:691-707`), ueber `sq:getAdjacentSquare(IsoDirections.fromIndex(i))` (`:709-719`), zusaetzlich
   `isFree(false)` (wie `B.SquareFits` `T:server/BanditsNPCBearWorld.lua:108-118`). Hoechstens (2 x 20 + 1)^2 = 1681 Kacheln. Naechster Standplatz gewinnt.
   Gemerkt im Register `rec.fw = { x, y, z, wx, wy }` (Stand + Wasserkachel), `rec.hx/hy/hz` = Stand (Leine fuer den Kampf wie Bleiben,
   `T:server/BanditsNPCBearFight.lua:144` um `fish` erweitern). Naht zu PLAN_TROEGE ("Wasser in der Welt"): EINE Suche `B.WaterNear(x, y, z, r)`.
3. **Hingehen:** `B.MoveTo(rec, a, x, y, 0, { walk = true })` (`T:server/BanditsNPCBearWorld.lua:917`), angekommen bis `fishArrive` 1,2; nach
   `fishWalkMs` 60000 ohne Ankunft: neuer Standplatz (hoechstens 3), dann Notiz "kommt nicht ans Wasser" und Modus Bleiben.
4. **Am Ufer:** `B.Hold` (`:883`), im SP zum Wasser drehen `a:faceThisObject(wasserKachel:getFloor())` (Grenzfall G-F1); Sicht `fsh = "wait"`.
5. **Versuche:** nur wenn er zaehlt (`B.NeedCounts`, 2.5), wach, nicht im Kampf/Flucht (`B.FightState`), nicht liegend. Uhr in Spielstunden (`B.Now`,
   je Schritt gedeckelt `maxDtH`, kein Nachholen nach dem Laden -- `E:752`): naechster Versuch nach `fishTryMin..fishTryMax` (10..15) Spielminuten,
   hungrig geteilt durch `fishHungryK`. Je Versuch: `B.OnFish(rec, caught, ms)` (Erfahrung +2 / +10), Wuerfel `ZombRandFloat(0.0, 1.0)`
   (`V:shared/Fishing/fishing_properties.lua:204`) gegen die Chance, Fx `"fish"` an die Clients (3.5).
6. **Fang:** Art + Groessen-Eintrag wuerfeln (3.1). Dann:
   - Hunger >= `fishEatHalf` x Saettigung des Fischs -> **sofort fressen**: `B.NeedEat(rec, B.MealsOf(-saett), "fish")` -- KEIN Gegenstand wird gebaut.
     Sicht `eat` wie das Fressen aus dem Inventar (`T:server/BanditsNPCBearInv.lua` `invEatShowMs`).
   - sonst Gegenstand bauen (3.4) und `B.InvAddItem(rec, item, "fish")`; passt er nicht (falsch): auf den Boden der Standkachel
     `sq:AddWorldInventoryItem(item, ZombRandFloat(0.1, 0.9), ZombRandFloat(0.1, 0.9), 0)` (Form `T:server/BanditsNPCBearInv.lua:812`, `:835`) -- nie weg.
7. **Ende/Pause:** anderer Befehl (jeder Modus-Knopf), Schlaf mit dem Besitzer (K1 SL, danach zurueck zum Stand), Kampf (danach zurueck), Taschen voll
   und satt (Rest < `fishFullKg` 1 kg UND Hunger < 25) -> Sicht `fsh = "full"`, liegt am Ufer und wartet (Frage F5-7), Notiz einmal; frisst spaeter
   seine Fische selbst ab 50 % (K1, `T:server/BanditsNPCBearInv.lua:1074`), dann geht das Fischen weiter. Futterliste "Fisch: nie" (PLAN_TROEGE) ->
   frisst den Fang nicht sofort, alles in die Taschen.

### 3.4 Fisch-Gegenstand (nur Server/SP) -- rote Linie "nichts verloren, nichts doppelt"
Genau Vanillas Fischnetz (`V:server/Fishing/BuildingObjects/FishingNet.lua:121-146`, laeuft dort am Server): `instanceItem(cfg.itemType)` (:125),
Naehrwerte x `2,2 x Gewicht / item:getActualWeight()` (:126-130), `setBaseHunger(-max(w/wf, 0,05))` (:132-142), `setHungChange(getBaseHunger())` (:144),
`setActualWeight(w x 2,2)`, `setCustomWeight(true)` (:145-146). KEIN Name am Server (Fischnetz setzt keinen; ein Server-Name waere in der Server-Sprache).
Gebaut wird erst, wenn klar ist, wohin er geht; danach genau EIN Weg (Satz im Inventar ODER Boden). Der Client bekommt nie einen Gegenstand geschickt.
`setWorldScale` reist nicht (F4-Befund `f4/PLAN_F4.md:213-214`) -- ein grosser Fisch liegt nach dem Nehmen in Normalgroesse, Gewicht stimmt.

### 3.5 Bild und Ton (OBERFLAECHE; Fx-Weg `T:shared/BanditsNPCBear.lua:929-955` -> `B.OnFx` -> `U.FightFx`)
- Fx `"fish"` { id, wx, wy, c = gefangen, s = "Small"/"Medium"/"Big" } an Spieler in `fxDist` 40. Client: `U.PoseAct(id, "fishstrike")` (mit Clips)
  bzw. `"swipeL"` (Ersatz, `fishClips = false`), nach `fishSplashMs` 500 Spritzer `getCell():getGridSquare(wx, wy, 0):startWaterSplash(true, dx, dy)`
  (`V:shared/Fishing/Fish.lua:58`; kein `transmitBigWaterSplash` -- jeder Client zeichnet selbst), Ton an der Wasserkachel `sq:playSound("CatchFish")` /
  `"CatchFishSmall"` / `"CatchFishBig"` bei Fang, sonst `"StrikeWithFishingSpear"` (Namen `VS:generated/sounds/player/sounds_player_fishing.txt:3`, `:21`,
  `:30`, `:39`; Form `sq:playSound(Text)` `V:shared/TimedActions/Fishing/TimedActions/ISCheckFishingNetAction.lua:19`; Bandits spielt denselben Hieb-Ton am
  Zombie `B:shared/ZombieActions/ZAFishing.lua:25`). Mit Clips traegt der Clip den Hieb-Ton selbst (PlaySound-Ereignis wie `TM:AnimSets/buck/idle/NCBear_SwipeL.xml`).
- Warten: Sicht `fsh = "wait"` -> Pose-Treiber `"fishwait"` (Clips) bzw. Sitzen (Ersatz, wie `sleepClips` in F3). Fressen am Ufer: vorhandener Clip `"eat"`.

### 3.6 Fenster und Schild (OBERFLAECHE)
- Knopf Fish (`T:client/BanditsNPCBearWinData.lua:1051-1052`, Reihe 2 `T:client/ISUI/BanditsNPCBearWindow.lua:84`) scharf: aktiv hervorgehoben bei Modus
  `fish`, grau mit Grund (Junges: "ab halbstark, etwa Tag %1"; mitfahrend; am Boden; weg). Klick -> `Window.lua:678` Zweig um `fish` erweitern (wie die Modi).
  Befehls-Info darunter: "Fischt: %1 gefangen, %2 gefressen" (Zaehler der Sitzung aus der Sicht `fsN`/`feN`).
- Faehigkeit Fischen-Tooltip (`UI_BN_Bear_Win_SkTip_Fsh`): Chance je Versuch + "etwa %2 Fische je Stunde" (Sicht `fish` = neue Chance in %, Kern rechnet).
- Schild Zeile 2: Modus `fish` -> "fischt" / "wartet am Wasser" (`T:client/ISUI/BanditsNPCBearHud.lua:445`, `T:client/BanditsNPCBearWinData.lua:304`,
  `T:client/BanditsNPCBearMenu.lua:467`).

### 3.7 SP / MP, rote Linien
SP-Zweig wie ueberall (`B.IsSP`). Alles Rechnen beim Schreiber; Client bittet nur "Mode" (vorhandener, geprufter Weg). Kein Gegenstand vom Client,
keine Client-Zahl ungeprueft (nur der Modus-Text). Nichts haengt: Weg-Frist 60 s, hoechstens 3 Standplaetze, Suche gedeckelt, Uhr gedeckelt.
Drehen zum Wasser nur SP (wie der Kampf, `T:server/BanditsNPCBearFight.lua:923`). Fischen nur mit Besitzer im Spiel (F4-Folge `f4/PLAN_F4.md:118`).
- **G-F1:** `faceThisObject` mit einem Kachel-Objekt am Tier: Methode am Tier belegt (`V:shared/TimedActions/Animals/ISPetAnimal.lua:17`), Welt-Objekt als
  Argument am Spieler (`V:shared/TimedActions/Animals/ISAttachAnimalToTree.lua:10`); Pruefer liest die Signatur im Jar (IsoGameCharacter.faceThisObject(IsoObject)).
  Scheitert es: nicht drehen (nur Optik).
- **G-F2:** `instanceItem` eines Fischs am dedizierten Server ruft `Fishing.onCreateFish` (`V:shared/Fishing/fishing_properties.lua:709-711`, `isClient()`-Riegel)
  -- Reihenfolge wie das Fischnetz, danach unsere Werte (Pruefer bestaetigt, dass nichts doppelt skaliert: Faktor bezieht sich auf das aktuelle Gewicht).
- **G-F3:** `startWaterSplash` / `sq:playSound` auf dem MP-Client (Fish.lua ist shared; Pruefer bestaetigt Client-Seite).

---

## 4. B.CFG (KERN, Block "F5" am Ende von `T:shared/BanditsNPCBear.lua` B.CFG; `fishBase`/`fishMax` :191 entfallen, Bench-Liste `T:client/NCBearBenchCub.lua:498` nachziehen)
| Wert | Vorgabe | Bedeutung |
|---|---|---|
| noseScanMs / noseScanCap / noseMax | 500 / 1500 / 24 | Client-Suche je / Eintraege je Suche / Markierungen |
| noseZ / noseHeadZ / noseSeenA | 1 / 0.8 / 0.001 | Ebenen-Abstand / Kopfhoehe (Ebenen) / Ziel-Alpha "nicht gesehen" |
| noseFadeMs / nosePulseMs / nosePulseMin | 300 / 1400 / 0.75 | Einblenden / Puls |
| noseRingK / noseBoxK / noseIconK, noseIconMin / noseIconMax | 1.4 / 0.5 / 0.30, 12 / 48 | Masse x h, Nasen-Bild px |
| noseR / noseG / noseB | 1.00 / 0.52 / 0.09 | Farbe (= markerR/G/B) |
| noseCalmMs / noseXpMs | 20000 / 3000 | Ruhe vor Brummen bzw. Erfahrung / Server-Suche je |
| fishR / fishArrive / fishWalkMs / fishStandMax | 20 / 1.2 / 60000 / 3 | Wasser-Suche / Ankunft / Weg-Frist / Standplatz-Versuche |
| fishTryMin / fishTryMax | 10 / 15 | Spielminuten je Versuch (= NC :67-68; mit NPC Crew von dort gelesen) |
| fishNpcBase / fishNpcStep / fishLure | 0.35 / 0.03 / "Base.Worm" | Rueckfall ohne NPC Crew (`NC:...Skills.lua:342-343`) / Koeder-Bezug |
| fishGrowLo / fishGrowHi | 0.5 / 1.0 | Groessen-Faktor halbstark / ausgewachsen (Kevin 12.11.) |
| fishHungryAt / fishHungryK / fishEatHalf / fishFullKg | 25 / 3 / 0.5 / 1.0 | Vorschlag F5-5 (a); 1 = aus |
| fishClips / fishSplashMs | false / 500 | Clips aus dem Modell-Lauf da? / Spritzer nach dem Hieb |

## 5. Sandbox
**Kein neuer Regler** (Kevin hat gekuerzt, `E:514-519` 12.11. "komplett uebertrieben"). Erfahrung beider Faehigkeiten laeuft ueber den vorhandenen
`BearSkillXpPercent`; der Spuernase-Schalter ist je Spieler/Baer (Zahnrad). Server-Verbot nur, wenn Kevin F5-3 mit (b) beantwortet.

## 6. Texte (`UI_BN_Bear_*`, ACHT Sprachen EN DE PTBR RU KO ES CN FR; CN/DE nur Vanilla-Zeichen; Platzhalter wie `langcheck`)
Neu: `Win_NoseTip` ("Marks zombies within %1 tiles of your bear that you cannot see. Only on your screen. Growls softly when new ones come close."),
`Win_FishTip` ("Goes to the nearest water (up to %1 tiles) and fishes. Eats when hungry, keeps the rest in its packs."), `Win_FishCub` ("Too young --
fishes from half-grown (about day %1)."), `Win_FishInfo` ("Fishing: %1 caught, %2 eaten."), `Note_FishGo`, `Note_FishNoWater` (%1 Kacheln),
`Note_FishLost`, `Note_FishFull`, `Tag_Fishing` ("fishing"), `Tag_FishWait` ("waits at the water"). Geaendert: `Win_SkTip_Fsh` (+ %2 Fische/h).
Nicht mehr benutzt: `Win_LaterFish`, `Win_LaterNose` (Uebernahme-Pruefung "unbenutzter Schluessel": entfernen in allen acht). Bench-Ausgaben nur EN.

## 7. Dateien (Namen frei: grep 14.11. in T und NC -- 0 Treffer fuer `BanditsNPCBearNose|Fish|Sniff`, `U.NoseOn`, `B.FishStep`, `UI_BN_Bear_Fish_`)
- **KERN:** NEU `T:shared/BanditsNPCBearFishRules.lua` (Chance, Arten, Groesse, Saettigung; rein rechnend, Vanillas `Fishing`-Tabellen), NEU
  `T:server/BanditsNPCBearFish.lua` (Modus-Schritt, Wasser, Versuch, Gegenstand, Fx), NEU `T:server/BanditsNPCBearSniff.lua` (Erfahrung 2.5);
  geaendert `shared/BanditsNPCBear.lua` (CFG, MODES), `shared/BanditsNPCBearStats.lua` (fish = neue Chance), `shared/BanditsNPCBearRules.lua:369-424`,
  `server/BanditsNPCBearFollow.lua` (:101, :147 Notizen), `...Order.lua:105-120` (Schritt `fish`), `...Fight.lua:144` (Leine), `...Heal.lua:92`,
  `...Registry.lua:138`, `:638-700` (Sicht `fsh fsN feN`, `B.FishView`), `...Server.lua:265` (keepHome), `...Needs.lua` (`B.NeedCounts` ausgeben).
- **OBERFLAECHE:** NEU `T:client/BanditsNPCBearNose.lua` (Suche, Liste, `U.NoseDraw`, Brummen), Bilder NEU `TM:ui/BanditsNPCBearNose*.png` (Skript
  wie Herz), geaendert `client/ISUI/BanditsNPCBearHud.lua` (Haken, Zeile 2), `client/BanditsNPCBearTags.lua` (noseoff), `client/BanditsNPCBearWinData.lua`,
  `client/ISUI/BanditsNPCBearWindow.lua`, `client/BanditsNPCBearMenu.lua:467`, `client/BanditsNPCBearPose.lua` (fishwait/fishstrike/Ersatz),
  `client/BanditsNPCBearFx.lua` (Art `fish`), `shared/Translate/EN|DE/UI.json`.
- **TEXTE:** sechs Sprachen. **Bench:** NEU `T:client/NCBearBenchFish.lua`, `T:client/NCBearBenchNose.lua` (nie kopiert).

## 8. Engine-Aufrufe (neu benutzt; alle mit Vanilla-/Bandits-Fundstelle, gleiche Argumentart; **kein Nur-Jar-Aufruf**)
| Aufruf | Argument | Fundstelle | Seite |
|---|---|---|---|
| `isoToScreenX/Y(0, x, y, z)` | Zahlen | `V:client/Fishing/TensionUI.lua:11-12` (im Baer schon) | Client |
| `el:drawTextureScaled(tex, x, y, w, h, a, r, g, b)` | Bild, Zahlen | `V:client/ISUI/ISUIElement.lua:1032` | Client |
| `z:getTargetAlpha(n)`, `z:getAlpha(n)` | Zahl | `V:client/DebugUIs/DebugChunkState/DebugChunkState_ObjectProperties.lua:93-94` (Grenzfall Empfaenger, G-N1) | Client |
| `sq:isCanSee(n)` (Rueckfall) | Zahl | `V:client/Foraging/ISBaseIcon.lua:256` | Client |
| `BanditZombie.CacheLightZ`, `.GetInstanceById(id)` | Lua | `B:client/BanditZombie.lua:11-12`, `:176-186` | Client |
| `getCell():getZombieList()`, `z:getVariableBoolean("Bandit")`, `z:isAlive()`, `z:getX/Y/Z()` | -- / Text | `B:client/BanditZombie.lua:110-115`, `:131`, `:49`, `:125` | Client |
| `a:playBreedSound("huffsoft")` | Text | `V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19`; im Baer `T:client/BanditsNPCBearFx.lua:235` | Client |
| `sq:getFloor():hasProperty(IsoFlagType.water)`, `sq:isSolid()`, `sq:isSolidTrans()`, `sq:getAdjacentSquare(IsoDirections.fromIndex(i))` | Flag / Zahl | `V:client/ISUI/ISWorldObjectContextMenu.lua:687-688`, `:695`, `:713` | Schreiber |
| `getCell():getGridSquare(x, y, z)`, `sq:isFree(false)` | Zahlen / bool | `V:server/Animal/ISPickDungCursor.lua:104`; `B:server/BanditServerSpawner.lua:231` (im Baer schon) | Schreiber |
| `a:faceThisObject(obj)` (nur SP) | IsoObject | `V:shared/TimedActions/Animals/ISPetAnimal.lua:17` + `V:shared/TimedActions/Animals/ISAttachAnimalToTree.lua:10` (G-F1) | Schreiber |
| `instanceItem(t)`, `cfg:getFishSizeData(s, m, b)`, Naehrwert-/Hunger-/Gewicht-Setter | Text / Zahlen | `V:server/Fishing/BuildingObjects/FishingNet.lua:123-146` | Schreiber |
| `Fishing.fishes`, `Fishing.Utils.skillSizeLimit`, `Fishing.Utils.getFishSizeChancesBySkillLevel(l, false, 1)` | Lua | `V:shared/Fishing/fishing_properties.lua:216`, `V:shared/Fishing/FishingUtils.lua:161-206` | Schreiber |
| `ZombRandFloat(0.0, 1.0)` | Zahlen | `V:shared/Fishing/fishing_properties.lua:204` | Schreiber |
| `sq:AddWorldInventoryItem(item, x, y, 0)` | Gegenstand, Zahlen | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:46` (im Baer `T:server/BanditsNPCBearInv.lua:812`) | Schreiber |
| `sq:startWaterSplash(true, dx, dy)` | bool, Zahlen | `V:shared/Fishing/Fish.lua:58` | Client |
| `sq:playSound("CatchFish")` | Text | `V:shared/TimedActions/Fishing/TimedActions/ISCheckFishingNetAction.lua:19` | Client |

## 9. Bench (nur `NCBearBench*.lua`, nie kopiert; Uebernahme-Pruefung kennt das Muster)
- `NCBearBenchFish.lua` (KERN): `NCBear_FishInfo()` (Modus, Stand, Wasser, Chance, hungrig x, naechster Versuch, gefangen/gefressen/eingepackt),
  `NCBear_FishNow(n)` (SP: n Versuche sofort), `NCBear_FishWater()` (zeigt die gefundene Wasser-/Standkachel). Fischen-Stufe ueber den vorhandenen
  Faehigkeits-Befehl der Werkbank (B.SkillSet).
- `NCBearBenchNose.lua` (OBERFLAECHE): `NCBear_NoseInfo()` (Weite, Zombies in Weite, davon unsichtbar, Markierungen, letztes Brummen),
  `NCBear_NoseAll(on)` (zeichnet auch GESEHENE Zombies -- nur zum Testen bei Tag), `NCBear_NoseLog(on)`.

## 10. Attrappen (lua5.1 `C:/Users/Kevin/Tools/lua51/lua5.1.exe`; alte Attrappen F1..Kampf bleiben gruen, bewusst geaenderte Erwartung: `fishBase/fishMax`)
- **KERN `attrappe/f5_kern/`:** F1 Chance: ausgewachsen St. 0 = 0,3325, halbstark St. 0 = 0,166, Junges = 0, mit NPC-Crew-Attrappe liest FX;
  F2 Arten je Stufe aus Vanillas Tabellen (St. 0: 7 Arten, St. 10: 21) -- Werte wie `werkzeug_f5/fisch_rechnung_ausgabe.txt`;
  F3 Takt: hungrig 3x, satt 1x, eingefroren 0 Versuche, nach 3 h Entladen kein Nachholen; F4 Fang-Wege: Hunger 60 -> gefressen, KEIN Gegenstand;
  Hunger 0 -> genau ein Satz; Taschen voll -> genau ein Boden-Gegenstand; satt + voll -> vor dem Wuerfeln Schluss ("full"); Zahl Gegenstaende vorher/nachher;
  F5 Wasser-Suche (Karten-Attrappe Fluss): naechster Stand; kein Wasser -> Ablehnung; Weg-Frist -> neuer Stand, nach 3 -> Bleiben;
  F6 Erfahrung +2/+10 nur ab halbstark; F7 Speichern/Laden mit `mode fish` + `rec.fw`; Stand ungueltig -> neu suchen; F8 Sniff-Erfahrung: Ruhe 20 s.
- **OBERFLAECHE `attrappe/f5_ober/`:** N1 Weite 12/27/16,5 (Junges-Deckel); schlafend/mitfahrend -> keine; N2 Ziel-Alpha 0 -> Markierung, 1 -> keine;
  Alpha 0,4 -> Deckkraft 0,6; N3 30 Zombies -> 24 naechste; Banditen nie; N4 Brummen: 0 -> 1 nach 20 s Ruhe einmal, Junges nie, Schalter aus nie;
  N5 ini: noseoff neben tag/age/hp, alte Datei = an; N6 Mitschrift-Dump: je Markierung genau 3 Bild-Aufrufe, Masse wie 2.4; N7 Fisch-Knopf/Zeile 2.
  Mitschrift-Bilder (Regel "UI-Bilder aus echtem Code"): Markierungen ueber Kevins Spielbild 1080/4K EN+DE, Fenster mit Fischen-Knopf und Zahnrad offen.

## 11. Aufteilung Bau (hoechstens 8 Agenten; getrennte Dateien; Schnittstelle `f5/schnittstelle.md`)
1. **G Pruef-Tore** (Jar lesen, parallel): G-N1, G-N2, G-F1, G-F2, G-F3 -> `f5/GATES.md`.
2. **KERN** (Abschnitt 7 KERN + Bench Fish + Attrappen kern + Uebernahme-Skript/NAEHTE).
3. **OBERFLAECHE** (Abschnitt 7 OBERFLAECHE + Bench Nose + Bilder-Skript + EN/DE + Attrappen ober).
4. **TEXTE** (sechs Sprachen, `langcheck`).
5. **PRUEF Code** (luacheck, scopecheck, localcount aktiv+gesamt < 180, luacheck_pz; Hud.lua vorher messen).
6. **PRUEF Bild** (Mitschrift-Kette, Bilder 1080/4K EN/DE).
7. **NACHBESSERUNG**. 8. **GEGENPRUEFER + Integrator** (Staging-Liste, mod.info-Vorschlag, Testanleitung; Einbau erst, wenn NCBearTest nicht geladen ist).

## 12. Modell-Lauf (getrennt, NUR grosser Koerper: NCBear + NCBearGen; das Junge fischt nicht)
- Clips "fishwait" (Schleife ~4 s: steht am Ufer, Kopf tief ueber dem Wasser, wiegt, hebt ab und zu eine Vordertatze) und "fishstrike" (~2,4 s: Tatze
  schlaegt ins Wasser bei ~35 %, Kopf taucht nach, kommt kauend hoch; Ende -> `NCBearDone=true`). AnimSet-Knoten `TM:AnimSets/buck/idle/NCBear_FishWait.xml`
  / `NCBear_FishStrike.xml` nach dem Muster `NCBear_Eat.xml` / `NCBear_SwipeL.xml` (Bedingung `NCBearAct`, PlaySound "StrikeWithFishingSpear" beim Treffer).
  Dauern in `B.CLIPS` (`T:shared/BanditsNPCBearFightRules.lua:64-89`); erst wenn ALLE grossen GLBs sie haben: `fishClips = true`.
- Sinnvoll im selben Lauf: Trink-Clip fuer "Wasser in der Welt" (PLAN_TROEGE, `E:772-776`) -- beide am Ufer, gleiche Haltung. Blatt fuer Kevin mit Spielkamera.
- Wiederholung nach `../_arbeit/baer_liegen/WIEDERHOLEN.md` (Kern- und Spuren-Skripte), Modell-Dateien nie aus dem Staging.

## 13. Naehte / Uebernahme
- NPC Crew optional: `BanditsNPC.Skills.FX` und `BanditsNPC.Fishing.CAST_MIN/MAX_MINUTES` nur hinter Existenz-Riegel gelesen (nichts geaendert) -> Absatz
  in `baer/NAEHTE.md`. Bandits-Cache `BanditZombie.*` hinter Riegel. Neue Dateien passen in die Muster von `baer/tools/baer_uebernahme.py`; Bench-Dateien
  als Bench gefuehrt; `BanditsNPCBear.ini` bekommt die Liste `noseoff`.
- Naht zu PLAN_TROEGE: eine Wassersuche `B.WaterNear`; Futterliste "Fisch nie" -> kein Sofort-Fressen. Naht zu PLAN_TALENTE: `B.FishK(rec)` (Angler x2),
  `B.NoseRange(rec)` als einzige Stelle der Nasen-Weite (Talent "Wachsam" darf sie vergroessern).

## 14. Testanleitung (Skizze; statisch geprueft, nicht gespielt; Spiel neu starten)
1. Ausgewachsener Baer folgt, Nacht oder Haus: Zombies hinter Waenden/hinter dir -> orange Rahmen + Nasen-Bild; dreh dich um -> Markierung blendet aus,
   Zombie ein. Leises Brummen beim ersten. Zahnrad -> Nasen-Warnung aus -> nichts mehr. `NCBear_NoseInfo()`.
2. Junges: Markierungen ja, kein Brummen. Baer schlaeft -> keine. Im Auto -> keine.
3. Baer halbstark+ an einen Fluss (< 20 Kacheln), Knopf "Fischen" -> geht hin, wartet, Hieb, Spritzer, Ton; `NCBear_FishNow(10)`.
4. `NCBear_CubNeeds(80, 10, 10, 0)` -> faengt schneller, frisst sofort; Hunger 0 -> Fische landen im Inventar. Taschen voll -> "wartet am Wasser".
5. Weg vom Wasser ohne Wasser in 20 Kacheln -> Notiz "kein Wasser". Junges -> Knopf grau mit Tag.

## 15. Fragen fuer Kevin (einfach; gebaut wird jeweils die Empfehlung, wenn du "Ja, alle so" sagst)
- **F5-1 Wie soll die Markierung aussehen?** (Der Vanilla-Umriss geht nicht: unsichtbare Zombies malt das Spiel gar nicht.)
  (a) **Empfehlung:** orange Ecken-Rahmen + Nasen-Bild + Ring am Boden wie im Entwurf-Bild; (b) nur Ring + Nasen-Bild (ruhiger); (c) wie (a), aber rot.
- **F5-2 Nasen-Warnung am Anfang?** (a) **Empfehlung:** an, mit leisem Brummen bei neuen Zombies (hoechstens alle 20 s); (b) an, ohne Brummen;
  (c) aus -- jeder schaltet sie im Zahnrad selbst ein.
- **F5-3 Darf ein Server die Anzeige verbieten?** (a) **Empfehlung:** nein, kein neuer Regler; (b) ja, ein Schalter "Spuernase-Anzeige erlaubt" (Vorgabe an).
- **F5-4 Wann zeigt die Nase?** (a) **Empfehlung:** immer, wenn dein Baer wach und in deiner Naehe ist -- egal ob er folgt, bleibt oder fischt;
  (b) nur wenn er dir folgt; (c) auch im Schlaf (mit halber Weite).
- **F5-5 Wie viel staerker fischen?** (Ausgewachsen Stufe 0 faengt wie ein NPC nur ein Drittel von dem, was er frisst.)
  (a) **Empfehlung:** hat er Hunger, faengt er 3x so schnell und frisst alles gleich; satt angelt er wie ein NPC und packt ein; (b) immer 2x so stark,
  auch der Vorrat; (c) immer 3x; (d) wie ein NPC lassen.
- **F5-6 Wie faengt er an?** (a) **Empfehlung:** Knopf "Fischen": er geht zum naechsten Wasser (bis 20 Kacheln) und fischt, bis du was anderes sagst;
  (b) dazu von selbst, wenn er im Modus "Frei" Hunger hat und Wasser nah ist; (c) nur von selbst.
- **F5-7 Satt und Taschen voll?** (a) **Empfehlung:** legt sich ans Ufer und wartet (eine Meldung), frisst spaeter seine Fische und fischt dann weiter;
  (b) kommt zu dir zurueck und folgt; (c) fischt weiter, Fische bleiben am Ufer liegen.
- **F5-8 Animation?** (a) **Empfehlung:** eigener Modell-Lauf "Fischen" (Tatze ins Wasser, Kopf taucht, kaut) zusammen mit dem Trink-Clip -- bis dahin
  Ersatz aus vorhandenen Bewegungen; (b) nur Ersatz-Bewegungen, kein Modell-Lauf.
Was jede andere Antwort aendert: F5-1 nur Bilder/Masse (OBERFLAECHE); F5-2 Vorgabe in `U.NoseOn` + Ton; F5-3 (b) = 1 Regler `BearNoseAllowed` +
Sandbox-Texte; F5-4 nur die Bedingung in 2.3; F5-5 nur `fishHungryK/fishHungryAt` bzw. ein fester Faktor; F5-6 (b)/(c) = Zusatz-Schritt im Modus
"roam" (Wasser in 10-20 Kacheln, wie PLAN_TROEGE); F5-7 nur Schritt 7 in 3.3; F5-8 (b) = `fishClips` bleibt false, Abschnitt 12 entfaellt.
