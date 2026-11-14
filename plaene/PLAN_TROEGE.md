# Plan-Lauf baer-plaene-1114: TROEGE + FUTTERLISTE + WASSER IN DER WELT

Stand 14.11.2026 (Rolle PLAN + FORSCHUNG). **Statisch geprueft, nicht gespielt.** Kein Mod-Code gebaut. Geschrieben nur unter
`_arbeit/baer_zaehmen/plaene_1114/`: diese Datei, `bilder/ENTWURF_futterliste_DE_1080.png` (+ `bilder/symbole/`), Werkzeuge `werkzeug/`
(`jar_holen.py`, `such_jar_text.py`, `zeichne_futterliste.py`), Jar-Klassen + Vineflower nach `jar/troege/` (`jar/troege/dec/*.java`).

Kevins Worte gehen vor: `baer/begleiter/ENTSCHEIDUNGEN.md` (`E:Zeile`) ab :686, `baer/begleiter/bedarf_echte_baeren.md`, `baer/STAND.md` oben.
Kuerzel: `T:` = Test-Mod `Zomboid/mods/NCBearTest/42/media/lua/` (Git main 1f7b641 = F1..F4 + Liegen + K1 + Kampf), `TM:` = `.../42/media/`,
`V:` = Vanilla `ProjectZomboid/media/lua/`, `VS:` = Vanilla `media/scripts/`, `VA:` = Vanilla `media/AnimSets/`,
`J:` = Jar 42.22 (Vineflower `plaene_1114/jar/troege/dec/<Klasse>.java`), `JK1:` = `k1/jar/dec/` (schon vorhanden),
`NC:` = NPC Crew `42/media/lua/` (nur gelesen, nichts kopiert). `B` = `BanditsNPC.Bear`, `U` = `B.UI`.

---

## 0. Kurzfassung

1. **Vanilla-Tiere bauen wir NACH, sie laufen nicht mit.** Unser Baer hat absichtlich keinen Vanilla-Hunger/-Durst (`hungerMultiplier` /
   `thirstMultiplier` fehlen, T:shared/BanditsNPCBearDefs.lua:118-119); Vanillas Verhalten sucht Futter/Wasser erst ab `thirstHungerTrigger`
   (J:BaseAnimalBehavior.java:855-857, :1043-1044) und nur in **Tierzonen** (DesignationZoneAnimal, J:BaseAnimalBehavior.java:1179-1188,
   V-Text IG_UI.json:4749 "A trough needs to be placed in a Designation Zone"). Unser eigener Schritt `B.DineStep` macht dasselbe mit unseren
   Beduerfnissen (K1-Werte), nur der Server entscheidet.
2. **Troege:** Vanillas `IsoFeedingTrough` haelt ENTWEDER Futter (Behaelter, jedes `Food` oder Tierfutter-Sack) ODER Wasser (Fluessigkeit, nur
   Water/TaintedWater) -- J:IsoFeedingTrough.java:59-66, :107-109, :488-497. Kevin: **nur markierte Troege** ("Fuer den Baeren", Futter und/oder Wasser,
   mehrere, Deckel 32 je Baer -- E:801-806), in der **ganzen Basis** (E:782-786). Die Suche laeuft nur ueber die <= 32 Marken (kein Flaechen-Scan).
3. **Basis** = NPC Crews Basisflaeche (Register `BanditsNPC.BeaconRegistry`, laeuft auch am dedizierten Server) ODER Vanillas Safehouse; beides nur
   die EIGENE. Ohne beides (Einzelspieler ohne NPC Crew): Vorschlag 40 Kacheln um den Baeren (Frage T-1).
4. **Futterliste "Frisst / Nie" je Futterart** (16 Arten = genau die Arten, die ein Baer heute frisst, T:shared/BanditsNPCBearFood.lua:20-23, :52),
   im **Zahnrad-Menue** -> kleines Fenster (Entwurf-Bild). Gilt fuer Selbst-Fressen aus dem Inventar UND aus Troegen; aus der Hand fuetterst du weiter alles.
   Wasser ist fest: nur Water/TaintedWater (E:741, E:803-805); Troege koennen in Vanilla gar keine Milch halten (FluidFilter, J:IsoFeedingTrough.java:493-495).
5. **Wasser in der Welt:** ab Durst 50 % und Fluss/See bis 20 Kacheln -> geht selbst hin, steht am Ufer (Vanillas Ufer-Regel,
   V:client/ISUI/ISWorldObjectContextMenu.lua:683-720), trinkt **langsam** bis 0 % (Vorschlag 50 % je Spielstunde = 50 -> 0 in ~1 Spielstunde,
   ~3,75 echte Minuten bei Vanillas Standard-Tageslaenge), Gefahr / Befehl / Schlaf bricht ab.
6. **Trink-Bild und -Ton:** Vanilla-Tiere haben KEINEN Trink-Knoten -- sie trinken mit dem Fress-Bild (`idleAction = "eat"`, J:BaseAnimalBehavior.java:490-501;
   VA:buck/eating/eating.xml) und **lautlos** (J:AnimalEatState.java:21-31: Ton nur beim Fressen). Vorschlag: unser vorhandener Clip `NCBear_Eat`
   (TM:AnimSets/buck/idle/NCBear_Eat.xml) in Schleife + Ton ueber die Rasse (`playBreedSound("drink")`, eigenes Ton-Skript auf Vanillas Ereignis
   "Character/Survival/Drink/FromRiver", VS:generated/sounds/player/sounds_player_drinking.txt:75-82). Eigener Trink-Clip = getrennter Modell-Lauf (Abschnitt 13).
7. **Mengen nach K1** (Abschnitt 6): volle Leiste = Junges 83 / halbstark 221 / ausgewachsen 691 Hungerpunkte bzw. 1,5 / 4,8 / 15 l; ein 100-l-Trog
   reicht einem Ausgewachsenen ~6,7 Wach-Tage. Trog/Fluss zaehlen NICHT als "satt gefuettert/getraenkt" fuer das Vertrauen (nur aus der Hand, K1).
8. **Kein neuer Jar-only-Aufruf, kein neuer Sandbox-Regler.** Bau mit 8 Agenten (Abschnitt 12), ein Modell-Lauf nur auf Kevins Wort.

---

## 1. Was Kevin will (woertlich)

- E:733-736 (00:35): *"kann der baer auch spaeter auf kisten zugreifen und essen holen und trinken?"* -> *"okay nur wie die tiere das macht mehr sinn haha"*
  -> wie Vanillas Nutztiere aus Futter- und Wassertroegen, in der Wildnis aus Fluss/See, NICHT aus Kisten.
- E:772 (02:00): *"... das der baer in wassernaehe automatisch zum wasser laeuft wenn man ka 10-20 kacheln entfernt ist und er selbst staendig dann eine
  trink animation abspielt mit sound wenns geht und dann sich komplett voll trinkt aber nicht blitzschnell das soll schon bisschen dauern ;D"*
- E:782 (02:10): *"bei trog mehr range da darf er die ganze base nutzen und ja soll da stehn mit prozent"*; E:786 (02:12): *"beim essen darf er auch die
  ganze base nutzen als range"*.
- E:800 (02:25): *"aber der muss eine futter und trinken einstellung bekommen was erlaubt ist sonst frisst er den huehnern alles weg oder trinkt die milch
  weg haha"*; E:805 (02:30, Auswahl): *"Ja, so"* (nur markierte Troege, Futterliste frisst/nie, nur Wasser); E:806 (02:31): *"aber mehrer troege sind
  erlaubt zu zuweisen"*.
- E:812 (02:45): *"essens/trinken regel auch im zahnrad menue das oben in die baeren ui kommen soll wie bei unserer npc crew mod"*.
- E:741 (00:55): *"ja der darf natuerlich auch dreckiges wasser trinken weils ein tier ist"*.
- Mengen: E:762-771 (6 % Koerpergewicht Wasser, ~10 % Futter nach Saettigung), E:787-799 (Tagesmenge waechst bis Tag 100; 0 -> 100 % in 16 Wachstunden).

---

## 2. Forschung: wie Vanilla-Tiere Troege und Wasser nutzen (Belege)

### 2.1 Das Trog-Objekt
- Klasse `IsoFeedingTrough` (J:IsoFeedingTrough.java:42). Lua-System "feedingTrough": Server `SFeedingTroughSystem` (V:server/FeedingTrough/SFeedingTroughSystem.lua:5-23;
  gespeichert und an Clients gespiegelt: feedAmount, linkedX/Y, maxFeed, maxWater, water -- :19, :22), Client `CFeedingTroughSystem` (V:client/FeedingTrough/CFeedingTroughSystem.lua).
- **Futter ODER Wasser**: `checkContainer()` -- hat er Wasser, gibt es keinen Behaelter; sonst einen Behaelter Typ "trough" (J:IsoFeedingTrough.java:59-66);
  Futter rein -> Fluessigkeit weg (`onFoodAdded`, :274-291); letztes Futter raus -> neue Fluessigkeit (`onRemoveFood`, :293-299). Vanilla-Text
  V:shared/Translate/EN/Tooltip.json:587-589 und IG_UI.json:4749 ("Troughs can only contain food or water, not both").
- **Was in den Behaelter darf:** jedes `Food` oder ein Tierfutter-Sack (Drainable mit AnimalFeedType) (J:IsoFeedingTrough.java:107-109). Futter wird von
  Hand in den Behaelter gelegt (Tooltip.json:588).
- **Wasser:** Fluessigkeits-Behaelter, Fassung `maxWater` aus der Definition, Regen faengt er mit 0,55, **nur Water und TaintedWater** (J:IsoFeedingTrough.java:488-497).
  `getWater()` / `getMaxWater()` = Liter (J:IsoFeedingTrough.java:404-414; Anzeige x 1000 ml, V:client/FeedingTrough/CFeedingTroughSystem.lua:138-139).
  Fassungen (V:shared/FeedingTrough/Definitions/FeedingTroughDefinitions.lua): simple 50 l (:70), double 50 l (:57), doublemetal 100 l (:10),
  triplemetal 150 l (:23), quadmetal 100 l (:40).
- **Mehrkachel-Troege:** nur das Hauptstueck hat Behaelter/Wasser; die anderen zeigen mit linkedX/linkedY darauf (J:IsoFeedingTrough.java:79-104, :380-402);
  Vanillas Menue springt so zum Hauptstueck (V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:18-32, :78-84).
- Futtermenge (Anzeige): `getCurrentFeedAmount()` = Summe |HungerChange| aller Food + Saecke x 0,1 (J:IsoFeedingTrough.java:467-486), in Lua gelesen
  V:client/FeedingTrough/CFeedingTroughSystem.lua:133.

### 2.2 Wie ein Vanilla-Tier einen Trog findet und nutzt
- Nur Troege in den mit dem Tier verbundenen **Tierzonen**: `getRandomTroughList()` (J:BaseAnimalBehavior.java:1179-1188); die Zone sammelt beim Pruefen
  alle Hauptstuecke in ihrer Flaeche (J:DesignationZoneAnimal.java:215-217) und alle freien Kacheln neben Wasser (`nearWaterSquares`, :223-236).
- Durst (ab `thirstHungerTrigger`, kein Junges, nicht im Kampf): zuerst Fluss in der Zone, dann Pfuetze, dann Wasser am Boden, dann Trog
  (`checkDrinkBehavior`, J:BaseAnimalBehavior.java:855-878). Hunger: Boden, Trog, Gras (`checkEatBehavior`, :1043-1063).
- Hingehen `pathToTrough` (freie Nachbarkachel an der Langseite, keine Wand/Fenster dazwischen, J:IsoAnimal.java:2669-2715); unerreichbar -> Trog auf
  die Liste `ignoredTrough` (J:BaseAnimalBehavior.java:492-494, :508-510; geleert J:IsoAnimal.java:1216-1224).
- Am Ziel: Anim-Variable `idleAction = "eat"` (+ `eatingAnim`), GLEICH fuer Fressen und Trinken (J:BaseAnimalBehavior.java:490-518, :745-756).
  Zustand `AnimalEatState`: je Ende des Clips (Ereignis `idleActionEnd`) ein Schritt `drink()` bzw. `eat()` (J:AnimalEatState.java:66-82), Blick zum Trog
  bzw. zur Wasserkachel (:45-55).
- **Mengen je Schritt:** Trinken aus dem Trog `removeWater(Rand 0,4..0,6 / thirstBoost)` Liter und Durst -0,2 x thirstBoost (J:AnimalData.java:1013-1016);
  Fluss/Pfuetze nur Durst -0,2 x thirstBoost, kein Wasser verbraucht (:978-1004). Fressen: ein Stueck, Teil-Abbiss ueber HungChange (:1085-1129).
- **Ton:** beim Fressen "AnimalFoleyEatGrass", Junges an der Mutter "AnimalFoleyFeedFromMother", **beim Trinken keiner** (J:AnimalEatState.java:21-31).
  Im Jar gibt es "DrinkingFromRiver" nur als Spieler-Ton (Suche `such_jar_text.py`: nur AnimalEatState und SoundKey).
- **MP-Sync (Vanilla, Lua am Server):** Wasser raus `isoObject:removeWater(n)`, `isoObject:sendSyncEntity(nil)`, `isoObject:checkOverlayAfterAnimalEat()`
  (V:server/ClientCommands.lua:1208-1213); Futter raus `sendRemoveItemsFromContainer(container, items)` + `removeAllItems()` (:1259-1260), danach
  `createFluidContainer()` falls keiner da ist (:1262-1264). Einzelspieler-Zweig ohne sendSyncEntity (V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:117-119).
  Das Tier selbst meldet seine Aenderung in Java (`SGlobalObjects.OnIsoObjectChangedItself`, J:AnimalData.java:1016).

### 2.3 Folgerung fuer den Baeren
- Unser Baer laeuft NICHT ueber dieses Verhalten (kein Vanilla-Hunger, keine `eatTypeTrough`, T:shared/BanditsNPCBearDefs.lua:118-119) -- gut so: kein
  Doppel-Fressen, keine Tierzonen noetig, unsere K1-Beduerfnisse bleiben die einzige Wahrheit. Wir bauen den Ablauf mit belegten Lua-Aufrufen nach
  (Tabelle 9). `animal:pathToTrough` (nur Jar) brauchen wir nicht: Weg ueber unser `B.MoveTo` + `B.SpotNear` (T:server/BanditsNPCBearWorld.lua:283-316, :917-981).
- Trog in einer Vanilla-Tierzone (Kuehe, Huehner): stoert nicht -- nur eine Marke erlaubt ihn, und Huehner-/Kuhfutter (AnimalFeed, Hay, Grass, Vegetables)
  frisst ein Baer ohnehin nie (B.FoodClass, T:shared/BanditsNPCBearFood.lua:45-61). Kuehe fressen aber Obst (V:shared/Definitions/animal/CowDefinitions.lua:217) --
  ein gemeinsam markierter Trog wird geteilt (Kevins Wahl ueber die Marke).

---

## 3. "Basis" (E:783-786) -- Belege und Regel

**NPC Crew (Existenz-Riegel, nur lesen):** Register `BanditsNPC.BeaconRegistry.Sites()` = ModData "TrueCompanionsBeacons" (NC:shared/BanditsNPCBeaconRegistry.lua:38-48,
shared -> auch am dedizierten Server). Basisflaeche = `site.zones[i]` mit `kind == "base"`, Teile `parts = { x1, y1, x2, y2 }`, Ebenen z0-1 .. z0+3
(NC:shared/BanditsNPCBaseSweep.lua:85-97; Ebenen-Regel NC:client/BanditsNPCZones.lua:741-742). Innen: `x >= p.x1 and x < p.x2 + 1 and y >= p.y1 and
y < p.y2 + 1` (NC:client/BanditsNPCZones.lua:804-813; Server-Nachbau NC:shared/BanditsNPCBaseSweep.lua:116-128). Eigene Basis = `R.MayWrite(R.KeyFor(site.x,
site.y, site.z or 0), owner)` (NC:shared/BanditsNPCBeaconRegistry.lua:170-208; Einzelspieler immer ja, :193-196; NC selbst so: BaseSweep.lua:99-113).
NICHT `BanditsNPC.Zones` / `Base.Zone`: die liegen in client/ und sind am dedizierten Server nil (NC:shared/BanditsNPCBase.lua:670-674, ForestZones.lua:686-687).
-> **Naht 2** in der einzigen Naht-Datei T:shared/BanditsNPCBearCrew.lua: `B.CrewBaseRects(ownerKey)` (nur lesen, 5-s-Zwischenspeicher wie NC BaseSweep :980-994).

**Vanilla Safehouse (Mehrspieler):** am Ort `SafeHouse.getSafeHouse(square)` (V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:31), Mitglied
`safe:getOwner() == name or safe:getPlayers():contains(name)` (V:client/OptionScreens/MapSpawnSelect.lua:427), Rechteck `getX/getY/getW/getH` (:428-429).
Fremdes Safehouse am Server: `SafeHouse.isSafeHouse(square, name, true) ~= nil` (V:server/BuildingObjects/ISBuildUtil.lua:15; Bedeutung J:SafeHouse.java:205-226:
liefert das Safehouse nur, wenn `name` dort NICHT Mitglied ist). Name = Besitzer-Schluessel `rec.owner` (= Benutzername im MP, T:shared/BanditsNPCBear.lua:646-654).
Im Einzelspieler gibt es keine Safehouses (Annahme, Pruef-Tor G-T7).

**Regel (Vorschlag):** ein markierter Trog zaehlt, wenn er geladen ist UND (a) in einer eigenen Basis liegt UND der Baer gerade in einer eigenen Basis steht,
Weg hoechstens `dineTroughMax` 60 Kacheln (unter Lade-Rand 76 und `needFreezeR` 70, T:shared/BanditsNPCBear.lua:335); oder (b) es gibt fuer diesen Besitzer
GAR KEINE Basis -> Trog hoechstens `dineBaseFallR` 40 Kacheln vom Baeren (Frage T-1). MP-Marke in einer FREMDEN Basis (NC-Flaeche, die der Spieler nicht
schreiben darf, oder fremdes Safehouse) lehnt der Server ab (kein Futterklau ueber den Baeren).

---

## 4. Futterliste "Frisst / Nie" (E:800-806, E:812, Bild)

### 4.1 Arten (KERN, `T:shared/BanditsNPCBearFood.lua` erweitert)
`B.FOOD_KINDS` (Reihenfolge = Anzeige): honey (Base.Honey), fish (FoodType Fish + Vanillas Fang-Fische `Fishing.fishes`, :25-39), meat, beef, poultry,
**game (Game UND Venison)**, bacon, sausage, seafood, egg, roe, fruit (Fruits), citrus, berry, nut, insect -- genau die Arten aus OK_TYPES (:20-23) + fav (:52).
`B.FoodKind(item)` -> Schluessel oder nil (gleiche Aufrufe wie B.FoodClass: getFullType, getFoodType, V:client/ISUI/Animal/ISAnimalContextMenu.lua:37, :55).
Namen: eigene Texte `UI_BN_Bear_FoodKind_<k>` (Vanillas `ContextMenu_FoodType_*` hat kein Venison und uebersetzt DE "Roe" falsch als "Roggen",
V:shared/Translate/DE/ContextMenu.json:637). Symbol je Art ueber `U.ItemIcon(Beispieltyp)` (T:client/BanditsNPCBearInvClient.lua:95-103).

### 4.2 Speicher und Regel (KERN)
- Register `rec.fno` = Text der verbotenen Arten, sortiert, Komma ("citrus,insect,roe"); fehlt = alles erlaubt (Vorgabe). Nur bekannte Schluessel, sonst verworfen.
  Spiegel: "fno" in MARK_FIELDS (T:server/BanditsNPCBearHeal.lua:52-60; flacher Text).
- `B.FoodNever(e, kind)` (rein, Register- ODER Sicht-Eintrag). Wirkt in **B.InvEatStep** (T:server/BanditsNPCBearInv.lua:1074-1130: Kandidat nur, wenn nicht nie)
  und beim **Trog-Fressen** (5.4). Hand-Fuettern bleibt frei (Kevin waehlt dort selbst; T:server/BanditsNPCBearServer.lua:233-306 unveraendert).
- Satz im Inventar bekommt `fk` (Art) beim Lesen neben `fc` (T:shared/BanditsNPCBearInvRules.lua:489-493). Saetze von VOR dem Lauf ohne fk: Honig/Fisch ueber
  `t`/`fc == "fav"` erkennbar, sonst "unbekannt" = erlaubt (wie NPC Crews "Food found later is allowed", NC Text UI_BN_Food_ForbidAsk) -- Tooltip sagt es.
- Bitte **"FoodRule"** { id, k = Art oder "*", n = 1 nie / 0 frisst } -> `B.HandleFoodRule` (Besitzer, gezaehmt, Art bekannt), `B.Commit`, Sicht neu.

### 4.3 Oberflaeche (Bild `bilder/ENTWURF_futterliste_DE_1080.png`)
- Zahnrad-Menue (T:client/ISUI/BanditsNPCBearWindow.lua:621-655, Punkte aus d.gear T:client/BanditsNPCBearWinData.lua:1082-1090) bekommt hinten:
  **"Futterliste ..."** (oeffnet das Fenster), **"Troege (n markiert) >"** (Untermenue: je Marke Zustand "Futter fuer ~x % eines Tages" / "Wasser 82 l" / "leer" /
  "nicht geladen", Entfernung; letzter Punkt "Alle Markierungen aufheben"), **"Selbst zu Fluss/See gehen"** (Haken, je Baer, Vorgabe an). Untermenue wie
  Vanilla `ISContextMenu:getNew` + `addSubMenu` (V:client/ISUI/ISContextMenu.lua:1075-1083; Form T:client/BanditsNPCBearMenu.lua:394-395). Vanillas Menue
  schliesst nach jedem Klick (V:client/ISUI/ISContextMenu.lua:66-70) -- darum die 16 Arten im eigenen Fenster, nicht als Untermenue (Frage T-7).
  `UI_BN_Bear_Win_GearTip` ergaenzen: Futterliste/Troege gelten fuer den Baeren (alle sehen sie), der Rest nur fuer dich.
- NEU `T:client/ISUI/BanditsNPCBearFoodWin.lua`: kleines Fenster in Farben/Massen des Baerenfensters (Grundmass x f wie T:client/ISUI/BanditsNPCBearWindow.lua),
  2 Spalten x 8 Zeilen: Symbol, Name, "Lieblingsfutter" bei Honig/Fisch, Schalter **Frisst** (gruen) / **Nie** (rot) (Farbidee NC:client/ISUI/BanditsNPCFoodWindow.lua:193-194,
  nur gelernt); Kasten "Wasser (fest)"; Knoepfe "Alle erlauben" / "Alle verbieten" (ohne Nachfrage, man schaltet einzeln zurueck); Zaehler "13 von 16 erlaubt".
  Schalter tragen den Art-Schluessel als `internal` (nie die Zeilennummer, NC-Lehre :52-57); bis die Sicht die Aenderung zeigt "..." (hoechstens 6 s).
  Zeichnen nur aus gemerkten Zeilen (nichts Teures je Bild).
- Inventar-Fenster: Tooltip eines Futter-Stuecks bekommt "Steht auf deiner Futterliste auf Nie - frisst er nicht selbst." (T:client/ISUI/BanditsNPCBearInvWindow.lua:270-290).

---

## 5. Troege und Wasser in der Welt -- Ablauf beim Schreiber

### 5.1 Marken (KERN, NEU `T:server/BanditsNPCBearDine.lua`)
- Register `rec.tro = { ["x,y,z"] = { x, y, z, f = 0/1, w = 0/1, at = Stunde } }`, hoechstens `troughMax` 32 je Baer (E:806); nur Hauptstueck-Koordinaten.
- Bitte **"Trough"** { id, x, y, z, f, w } (f = w = 0 -> Marke weg), **"TroughClear"** { id }. Server: Besitzer + gezaehmt; Kachel geladen
  (`getCell():getGridSquare`, V:server/ClientCommands.lua:1168); Trog dort (`getObjects()` + `instanceof(obj, "IsoFeedingTrough")`, :1169-1175); Nebenstueck ->
  Hauptstueck ueber `getLinkedX/Y` (V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:78-84); Spieler hoechstens `troughMarkR` 10 Kacheln entfernt;
  MP nicht in fremder Basis (Abschnitt 3); Deckel 32 -> Meldung `UI_BN_Bear_Trough_Full`. Danach Commit + Meldung "markiert (n von 32)".
- Ist ein markierter Trog bei GELADENER Kachel nicht mehr da (abgebaut, versetzt): Marke weg + Meldung `UI_BN_Bear_Note_TroughGone` (nicht geladen = bleibt).

### 5.2 Rechtsklick (OBERFLAECHE, NEU `T:client/BanditsNPCBearTroughMenu.lua`)
`Events.OnFillWorldObjectContextMenu.Add` (Form T:client/BanditsNPCBearMenu.lua:843-898, V:client/ISUI/Hutch/ISHutchMenu.lua:4-11, :115): Trog unter den
worldobjects (`instanceof`), Hauptstueck wie 5.1. Punkt **"Fuer den Baeren >"** (bei mehreren eigenen Baeren je Name ein Untermenue, `U.WinBears()`
T:client/BanditsNPCBearWinData.lua:333): **"Futter daraus fressen"** (Haken), **"Wasser daraus trinken"** (Haken), **"Nicht mehr fuer den Baeren"**. Haken aus der
Sicht `tro`. Grau mit Grund: Deckel voll, zu weit, Baer faehrt mit. Jeder Klick = eine Bitte (B.Ask, T:shared/BanditsNPCBear.lua:884). Kein Engine-Schreiben am Client.

### 5.3 Der Schritt `B.DineStep(rec, a, env, ms, players)` (KERN)
Eingehaengt in liveRec **nach der Zombie-Wache, vor Aufstehen/Folgen/Befehl** (T:server/BanditsNPCBearServer.lua:882 -> neue Zeile danach): Schlaf, Kampf und
Wache gehen damit immer vor. Rueckgabe true = er steuert den Baeren in diesem Takt.
- **Darf er?** gezaehmt, nicht mitfahrend/am Boden/liegend (`B.IsLying`, T:server/BanditsNPCBearSleep.lua:173), kein Kampf (`B.FightState`, T:server/BanditsNPCBearFight.lua:718),
  Beduerfnisse an (`B.NeedsOn`), Modus in `dineModes` = Folgen / Frei / Bleiben, **nicht Sitz** (Frage T-2), kein "Komm her" (s.come).
- **Will er?** Wasser ab `dineStart` 50 % Durst, Futter ab 50 % Hunger (E:773, wie K1 invDrinkStart/needHungry), bis 0 % (`ZERO` 0,0005 wie
  T:server/BanditsNPCBearInv.lua:1072). Beides: das hoehere zuerst, Gleichstand Wasser.
- **Quelle waehlen** (rein: `B.DinePick`, shared): Futter -> markierte Troege mit f = 1, geladen, Regel Abschnitt 3, nicht auf der Sperrliste, mit mindestens
  einem erlaubten Stueck (5.4); Wasser -> markierte Troege mit w = 1 und `getWater() > 0`, sonst (Schalter "Selbst zu Fluss/See" an, Modus Folgen/Frei/Bleiben)
  Ufer bis `dineWaterR` 20 Kacheln (5.5). Naechste zuerst. Nichts -> `s.dineNone[art] = jetzt + dineRetryMin` (30 Spielminuten) -> **dann** darf das
  Inventar ran (5.6). Vanillas Reihenfolge (Fluss vor Trog) nicht noetig -- unsere: naechste Quelle.
- **Hingehen ("go"):** Stehplatz neben dem Trog `B.SpotNear(tx, ty, tz, 2)` bzw. die Uferkachel; `B.MoveTo(rec, a, x, y, z, { walk = Weg < dineRunAt 8 })` je
  `moveMs` (T:server/BanditsNPCBearWorld.lua:917-981, gehen/rennen mit Kevins Wort). Frist = Weg / Tempo x 2 + 15 s, hoechstens 90 s; verpasst -> Quelle
  `dineIgnoreMin` 60 Spielminuten sperren (wie Vanillas ignoredTrough) + gedrosselte Meldung. Folgen: entfernt sich der Besitzer mehr als `dineLeash` 30 Kacheln
  -> Abbruch (er folgt wieder).
- **Am Ziel ("at"):** `B.Hold(rec, a, true)` (T:server/BanditsNPCBearWorld.lua:883-899); im Einzelspieler `a:faceThisObject(trog / wasserKachel:getFloor())`
  (Form V:shared/FeedingTrough/TimedActions/ISAddWaterToTrough.lua:10; am Baeren schon T:server/BanditsNPCBearFight.lua:923). Sicht `dine = "drink"/"eat"`,
  `dsrc = "trough"/"river"`, `dx, dy` (Blickziel) -> die Clients spielen das Bild (Abschnitt 7). Je `dineStepMs` 3200 ms (eine Clip-Schleife, B.CLIPS.eat
  T:shared/BanditsNPCBearFightRules.lua:74) ein Rechenschritt mit der Spielzeit seit dem letzten Schritt (`B.Now`, Deckel 0,05 h je Schritt):
  - Trinken: `dPct = min(Durst, dineDrinkPctH 50 x dtH)`, `l = B.DrinkNeedL(rec, dPct)` (T:shared/BanditsNPCBearNeedRules.lua:176-181). Trog: `take = min(l,
    trog:getWater())`, `trog:removeWater(take)`, Server zusaetzlich `trog:sendSyncEntity(nil)`, dann `trog:checkOverlayAfterAnimalEat()` (V:server/ClientCommands.lua:1208-1213);
    Fluss: take = l (kostet nichts, wie Vanilla J:AnimalData.java:978-990). Dann `B.NeedDrink(rec, take / bowlL, "trough"/"river")` (T:server/BanditsNPCBearNeeds.lua:335-347).
  - Fressen: 5.4.
  - Ende: Wert <= 0 -> naechstes Beduerfnis >= 50 an derselben Quelle? sonst fertig: `B.Hold(false)`, Sicht ohne dine, gedrosselte Meldung. Quelle leer -> neu waehlen.
- **Abbruch (nichts haengt):** jeder Befehl (`B.DineStop(rec, "order")` als erste Zeile nach dem Schlaf-Wecken in `B.SetMode`, T:server/BanditsNPCBearFollow.lua:109 --
  deckt Komm her T:server/BanditsNPCBearOrder.lua:298 und Herholen T:server/BanditsNPCBearRide.lua:428 mit ab); **kein DineStep im letzten Takt** (`ms - s.dine.last >
  dineLostMs` 3000: Schlaf, Kampf oder Wache hatten Vorrang) -> Ausflug endet, Kampf-Gefahr sperrt die Quelle nicht; Sicherheit `dineMaxH` 3 Spielstunden;
  Koerper-Tausch (Wachsen/Aussehen) -> neues Objekt, s.dine weg. Nach dem Ende rechnet der Modus wieder: Bleiben geht an seine Stelle zurueck (B.OrderStep, stayBack).
- Session `s.dine = { k = "water"/"food", src = "trough"/"river", x, y, z, sx, sy, ph = "go"/"at", t0, last, lastH, until, nextH }`; nichts davon im Register
  (nach dem Laden entscheidet er neu).

### 5.4 Fressen am Trog (KERN, nichts verloren, nichts doppelt)
- Kandidaten = `trog:getContainer():getItems()` (V:server/ClientCommands.lua:1177-1179; `items:size()/get(i)` V:server/Items/LootLog.lua:11-14), je Stueck
  `B.FoodClass(item)` (nicht verdorben/verbrannt) UND `not B.FoodNever(rec, B.FoodKind(item))`. Wahl wie K1 (T:server/BanditsNPCBearInv.lua:1086-1110): deckt
  ein Stueck den Rest-Hunger, das KLEINSTE davon; sonst Lieblingsfutter vor ok vor snack.
- Nehmen genau wie unser Fuettern: `container:Remove(item)`, `sendRemoveItemFromContainer(container, item)`, Gegenprobe `container:contains(item)` -- nur
  wenn wirklich weg, wird gutgeschrieben (T:server/BanditsNPCBearServer.lua:193-203; Vanilla shared/Camping/TimedActions/ISAddFuelAction.lua:66-68,
  V:server/BuildingObjects/ISBuildUtil.lua:149). Dann `B.NeedEat(rec, B.MealsOf(item:getHungerChange()), "trough")` (T:server/BanditsNPCBearNeeds.lua:321-333).
  Alles in EINEM Lua-Aufruf (kein Speichern dazwischen). Leer danach -> `if not trog:getFluidContainer() then trog:createFluidContainer() end` +
  `trog:checkOverlayAfterAnimalEat()` (V:server/ClientCommands.lua:1262-1268).
- Tempo: das naechste Stueck erst nach `fill / dineEatPctH` Stunden (fill = Prozent des Stuecks; Steak ausgewachsen 5,8 % -> ~7 Spielminuten, Junges 48 % -> ~58).
  Gutschrift sofort -> ein Abbruch kostet nichts. Was ueber 0 ginge, verfaellt wie heute (B.Feed); die Wahl "kleinstes, das deckt" haelt das klein.

### 5.5 Ufer suchen (KERN, gedeckelt)
- Wasser-Kachel = `sq:getFloor()` + `floor:hasProperty(IsoFlagType.water)` (V:client/ISUI/ISWorldObjectContextMenu.lua:683-689; am Baeren schon
  T:server/BanditsNPCBearWorld.lua:98-100). Ufer = nicht `isSolid()`/`isSolidTrans()`, Boden ohne Wasser, eine der 8 Nachbarn Wasser
  (`getAdjacentSquare(IsoDirections.fromIndex(i-1))`) -- Vanillas `isValidShoreSquare`/`isSquareAdjacentToWater` (:691-720) nachgebaut; dazu `isFree(false)`
  (V:client/ISUI/ISWorldObjectContextMenu.lua:2219). Nur Ebene 0 (Vanilla :747-749).
- Ringweise von innen nach aussen bis 20 (wie Vanillas `getSquaresAdjacentToWater` :722-745, aber naechste zuerst), **hoechstens `dineScanPerTick` 160 Kacheln je
  Hirn-Takt** (41 x 41 = 1681 -> ~11 Takte), Ergebnis 5 Spielminuten gemerkt; nichts gefunden -> 30 Spielminuten Ruhe. Mess-Tor G-T6 (Zeit je Takt in der Bench).

### 5.6 Inventar und Reihenfolge (KERN)
`B.InvEatStep` / `B.InvDrinkStep` (T:server/BanditsNPCBearInv.lua:1074, :1193; gerufen T:server/BanditsNPCBearNeeds.lua:614-615) fragen zuerst `B.DineWants(rec, art)`:
laeuft ein Ausflug oder ist die Suche noch offen -> nichts; erst wenn `s.dineNone[art]` steht (nichts erreichbar), fressen/trinken sie wie heute.
Vorschlag: **erst was nichts aus seinem Gepaeck kostet** (Trog, Fluss), das Inventar ist die Reise-Ration (Frage T-3).

---

## 6. Mengen nach K1 (E:762-771, E:787-799; K1-Rechnung `k1/PLAN_K1.md` 1.1, gebaut T:shared/BanditsNPCBearNeedRules.lua:136-186)

Volle Leiste (0 -> 100 % in 16 Wachstunden) = Tagesmenge: `playerHunDay 55,3 x foodAt {1,5 / 4 / 12,5}`, Wasser `6 % x {25 / 80 / 250 kg}` (T:shared/BanditsNPCBear.lua:332).

| Groesse | Punkte je 100 % | je 50 % (ein Trog-Besuch) | Steak -40 | Lachs -30 | Honig -20 | Wild -80 | Wasser je 100 % | je 50 % | Trinken bei 50 %/h |
|---|---|---|---|---|---|---|---|---|---|
| Junges | 83 | 41,5 | 1,0 | 1,4 | 2,1 | 0,5 | 1,5 l | 0,75 l | 0,75 l je Spielstunde |
| halbstark | 221 | 110,6 | 2,8 | 3,7 | 5,5 | 1,4 | 4,8 l | 2,4 l | 2,4 l je Spielstunde |
| ausgewachsen | 691 | 345,6 | 8,6 | 11,5 | 17,3 | 4,3 | 15 l | 7,5 l | 7,5 l je Spielstunde |

- Troege (Liter, Abschnitt 2.1): 50 l = ausgewachsen ~3,3 volle Leisten (~3,3 Wach-Tage), Junges ~33; 100 l ~6,7; 150 l ~10.
- Tempo-Vorschlag `dineDrinkPctH = dineEatPctH = 50`: 50 -> 0 in 1 Spielstunde fuer JEDE Groesse (Kevins "~1 Spielstunde ausgewachsen"); waehrend er trinkt,
  steigt der Wert weiter (6,25 %/h x Tempo x Vertrauen, T:shared/BanditsNPCBear.lua:332) -> netto ~1,15 h. Eine Spielstunde = 3,75 echte Minuten bei Vanillas
  Vorgabe-Tageslaenge 90 min (JK1:SandboxOptions.java:71 Vorgabe 4, :406-415). Vergleich Vanilla-Tier: je Clip-Schleife 0,4-0,6 l (J:AnimalData.java:1014).
- Vertrauen: Trog/Fluss zaehlen NICHT als "satt gefuettert/getraenkt" (+0,5 nur aus der Hand, K1, T:server/BanditsNPCBearNeeds.lua:277-313) -- wie das Selbst-Fressen.
- Einfrieren (K1, E:747-761): weiter als 70 Kacheln vom Besitzer steigt nichts -> Troege wirken, solange du in der Naehe bist (z. B. du arbeitest in der Basis).
- Anzeige "mit Prozent" (E:782): Troege-Untermenue zeigt je Trog "Futter fuer ~x % eines Tages" (Summe `B.FoodDayPct` der erlaubten Stuecke) bzw. Liter.

---

## 7. Bild und Ton (OBERFLAECHE)

- **Bild:** Sicht `dine` = "eat"/"drink" -> der Sitz-Treiber spielt `U.PoseAct(id, "eat")` immer wieder, solange das Feld steht (heute einmal je Fress-Fenster,
  T:client/BanditsNPCBearPose.lua:214-221; neue Marke je Schleife statt EAT[id] einmal). Clip `NCBear_Eat` (Schleife 3,2 s, TM:AnimSets/buck/idle/NCBear_Eat.xml,
  B.CLIPS.eat). Mit Trink-Clip spaeter (Abschnitt 13) nur der Schluessel "drink" statt "eat" (`B.CLIPS.drink`, Riegel `B.CFG.drinkClip`).
  Im MP dreht jeder Client seine Kopie zum Ziel (`obj:faceThisObject(...)` mit Trog bzw. `getFloor()` der Wasserkachel aus dx/dy -- gleiche Typen wie V:shared/FeedingTrough/
  TimedActions/ISAddWaterToTrough.lua:10; Pruef-Tor G-T4).
- **Ton:** je Schleifen-Start einmal `a:playBreedSound("drink")` bzw. `("eat")` (Form T:client/BanditsNPCBearFx.lua:191, V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19),
  Ende ueber `stopOrTriggerSound` wie T:shared/TimedActions/BanditsNPCBearPetAction.lua:101-104. Rasse (KERN, T:shared/BanditsNPCBearDefs.lua:178-186):
  `b.sounds.drink = { name = "NCBear_Drink" }`, `b.sounds.eat = { name = "AnimalFoleyEatGrass" }` (Vanillas Fress-Ton am Trog, J:AnimalEatState.java:27;
  Vorbild "petting" mit Vanilla-Ton T:shared/BanditsNPCBearDefs.lua:69-75). Ton-Skript `NCBear_Drink` in TM:scripts/nc_bear_sounds.txt:
  `category = Animals, clip { event = Character/Survival/Drink/FromRiver, volume = 0.6, distanceMax = 20 }` (Felder: event VS:generated/sounds/player/
  sounds_player_drinking.txt:75-82, volume VS:generated/sounds/zombies/sounds_zombie_foley.txt:243, distanceMax TM:scripts/nc_bear_sounds.txt:9).
  **Skript-Syntax genau pruefen** (ein Skriptfehler laesst das Spiel nicht laden, Gedaechtnis "Rezept-Syntax pruefen"). Pruef-Tor G-T3: klingt es?
- **Fenster-Status:** Zeile unter dem Modus "trinkt am Fluss" / "trinkt am Trog" / "frisst am Trog" / "geht trinken" / "geht fressen" (aus dine/dsrc).

---

## 8. Neue / geaenderte B.CFG-Werte (KERN, `T:shared/BanditsNPCBear.lua` Block nach :342) -- KEIN neuer Sandbox-Regler

| Wert | neu | Zweck |
|---|---|---|
| troughMax, troughMarkR | 32, 10 | Marken je Baer / Spieler-Abstand beim Markieren |
| dineModes | { follow = true, roam = true, stay = true } | Sitz nie (Frage T-2) |
| dineStart | 50 | ab hier selbst hingehen (Hunger und Durst) |
| dineDrinkPctH, dineEatPctH | 50, 50 | Prozent je Spielstunde am Trog/Fluss (Frage T-4) |
| dineWaterR, dineScanPerTick, dineScanKeepMin | 20, 160, 5 | Ufer-Suche (Frage T-8) |
| dineTroughMax, dineBaseFallR | 60, 40 | Weg zum Trog / ohne Basis (Frage T-1) |
| dineRetryMin, dineIgnoreMin | 30, 60 | nichts gefunden / Quelle unerreichbar (Spielminuten) |
| dineRunAt, dineGoMaxMs, dineArrive, dineLeash | 8, 90000, 1.6, 30 | Weg |
| dineStepMs, dineLostMs, dineMaxH, dineNoteH | 3200, 3000, 3, 6 | Takt, Abbruch, Sicherheit, Meldungen |
| drinkClip | false | true erst mit dem Trink-Clip (Modell-Lauf) |
Register: `rec.tro`, `rec.fno`, `rec.dww` (true = Fluss/See aus). Sicht: `tro` (Liste je Marke { x, y, z, f, w, st, fp, wl, d }, nur Besitzer), `fno`, `dww`,
`dine`, `dsrc`, `dx`, `dy`. Bitten: "Trough", "TroughClear", "FoodRule", "WildWater" (Dispatch T:server/BanditsNPCBearServer.lua:424-490).

---

## 9. Engine-Aufrufe (alle mit Vanilla-Fundstelle, gleiche Typen; KEIN Jar-only-Aufruf)

| Aufruf | Typen | Fundstelle |
|---|---|---|
| `instanceof(obj, "IsoFeedingTrough")` | Objekt, Text | V:server/ClientCommands.lua:1171; V:server/FeedingTrough/SFeedingTroughSystem.lua:48 |
| `getCell():getGridSquare(x, y, z)`, `sq:getObjects():size()/get(i-1)` | Zahlen | V:server/ClientCommands.lua:1168-1170 |
| `trog:getLinkedX()/getLinkedY()/getZ()` | -- | V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:78-84 |
| `trog:getContainer()`, `:getItems()`, `:isEmpty()` | -- | V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:56; V:server/ClientCommands.lua:1177-1179 |
| `items:size()`, `items:get(i)` | Zahl | V:server/Items/LootLog.lua:11-14 |
| `container:Remove(item)`, `sendRemoveItemFromContainer(container, item)`, `container:contains(item)` | Gegenstand | T:server/BanditsNPCBearServer.lua:193-203 (V:shared/Camping/TimedActions/ISAddFuelAction.lua:66-68, V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6); V:server/BuildingObjects/ISBuildUtil.lua:149 |
| `trog:getWater()`, `trog:getMaxWater()` | -- | V:client/FeedingTrough/CFeedingTroughSystem.lua:134-139; ISFeedingTroughMenu.lua:60-61 |
| `trog:removeWater(l)` | Zahl | V:server/ClientCommands.lua:1209; ISFeedingTroughMenu.lua:118 |
| `trog:sendSyncEntity(nil)` (nur Server) | nil | V:server/ClientCommands.lua:1212 |
| `trog:checkOverlayAfterAnimalEat()` | -- | V:server/ClientCommands.lua:1213; ISFeedingTroughMenu.lua:119 |
| `trog:getFluidContainer()`, `trog:createFluidContainer()` | -- | V:server/ClientCommands.lua:1182-1184, :1262-1264 |
| `trog:getCurrentFeedAmount()` (nur Anzeige, wahlfrei) | -- | V:client/FeedingTrough/CFeedingTroughSystem.lua:133 |
| `sq:getFloor()`, `floor:hasProperty(IsoFlagType.water)`, `sq:isSolid()`, `sq:isSolidTrans()`, `sq:getAdjacentSquare(IsoDirections.fromIndex(n))` | Zahl | V:client/ISUI/ISWorldObjectContextMenu.lua:683-720 (:695, :714) |
| `sq:isFree(false)` | Wahrheitswert | V:client/ISUI/ISWorldObjectContextMenu.lua:2219 |
| `a:faceThisObject(obj)` | IsoObject | V:shared/FeedingTrough/TimedActions/ISAddWaterToTrough.lua:10; T:server/BanditsNPCBearFight.lua:923 |
| `a:playBreedSound(Text)` | Text | V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19; T:client/BanditsNPCBearFx.lua:191 |
| `item:getFoodType()`, `item:getFullType()`, `item:getHungerChange()` | -- | V:client/ISUI/Animal/ISAnimalContextMenu.lua:37, :55 |
| `SafeHouse.getSafeHouse(sq)`, `safe:getOwner()`, `safe:getPlayers():contains(n)`, `safe:getX/getY/getW/getH()` | Kachel, Text | V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:31; V:client/OptionScreens/MapSpawnSelect.lua:425-429 |
| `SafeHouse.isSafeHouse(sq, name, true)` (Server) | Kachel, Text, Wahrheitswert | V:server/BuildingObjects/ISBuildUtil.lua:15 |
| Bewegung `B.MoveTo` / `B.Hold` / `B.SpotNear` / `B.AreaLoaded` | -- | vorhanden (T:server/BanditsNPCBearWorld.lua; pathToLocation/animalRunning mit Kevins Wort) |
| Kontextmenue `ISContextMenu:getNew`, `addSubMenu`, `addOption`, `setOptionChecked`, `notAvailable` | -- | V:client/ISUI/ISContextMenu.lua:1075-1085; T:client/BanditsNPCBearMenu.lua:394-397; T:client/ISUI/BanditsNPCBearWindow.lua:625-648 |
Bewusst NICHT: `animal:pathToTrough` (nur Jar, J:IsoAnimal.java:2669), `SGlobalObjects.OnIsoObjectChangedItself` (nur Java). Den Lua-Spiegel des Trogs (water-Feld)
zieht Vanillas eigener Debug-Weg auch nicht nach (V:server/ClientCommands.lua:1192-1214); Anzeigen lesen `getWater()` direkt (CFeedingTroughSystem.lua:134).

---

## 10. SP und MP, rote Linien

- SP-Zweig: `not isServer() and not isClient()` (`B.IsSP`, T:shared/BanditsNPCBear.lua:438). Alles Rechnen beim Schreiber (SP das Programm, MP der Server);
  Client zeigt nur aus der Sicht, schickt nur Bitten mit Zahlen/Texten (id, x, y, z, 0/1, Art) -> kein Kick.
- **Nichts verloren/doppelt:** Futter erst nehmen + Gegenprobe, dann gutschreiben, in EINEM Lua-Aufruf; Wasser genau die Liter, die gutgeschrieben werden
  (Trog: min(Bedarf, Inhalt)); Fluss kostet nichts; Inventar unveraendert (K1-Regeln). Zwei Baeren / Vanilla-Kuehe am selben Trog: jedes Stueck wird vor dem
  Nehmen neu gelesen (contains), nie gutgeschrieben, was ein anderer schon nahm.
- **Nichts haengt:** jede Phase mit Frist (go 90 s, at 3 h, Ufer-Suche gedeckelt, "..." im Fenster 6 s), Abbruch bei Befehl/Schlaf/Kampf/Takt-Luecke.
- **Fremde Basis** (MP) nie markierbar; der Besitz der Marke haengt am Baeren (Besitzer prueft jede Bitte).
- MP offen (ehrlich): Ton und Blickrichtung an fremden Kopien (G-T3/G-T4); `sendSyncEntity` laut Vanilla belegt, Wirkung ungespielt.

---

## 11. Attrappen (lua5.1, `attrappe/troege_kern/`, `attrappe/troege_ober/`; alte Attrappen F3/F4/K1/Kampf bleiben gruen)

KERN: A1 `B.FoodKind` (Honig -> honey; Lachs/Fang-Fisch -> fish; Venison und Game -> game; Vegetables/Hay/AnimalFeed -> nil). A2 Futterliste (FoodRule setzt/loescht,
"*" alle; unbekannte Art verworfen; fno sortiert, idempotent; InvEatStep nimmt kein "nie"-Stueck, fk fehlt -> erlaubt). A3 Marken (Hauptstueck ueber linked;
33. Marke abgelehnt; f = w = 0 loescht; fremde Basis MP abgelehnt, SP ja; zu weit abgelehnt; Trog weg bei geladener Kachel -> Marke weg, ungeladen -> bleibt).
A4 Basis (NC-Rechteck innen/aussen, Ebene z0-1..z0+3; Safehouse Mitglied/fremd; keine Basis -> 40 Kacheln). A5 Wahl (naechster erlaubter, ignoriert gesperrte,
Wasser leer zaehlt nicht, Futter nur mit erlaubtem Stueck). A6 Trinken (ausgewachsen 50 -> 0: genau 7,5 l aus dem Trog in 1 Spielstunde ohne Anstieg; Trog mit
3 l -> stoppt leer, Durst sinkt um 3 l; MP ruft sendSyncEntity, SP nicht). A7 Fressen (Stueck weg erst nach contains = false; Gegenprobe scheitert -> keine
Gutschrift; letztes Stueck -> createFluidContainer; kleinstes deckendes zuletzt). A8 Abbruch (SetMode, Takt-Luecke 3 s, Kampf, Frist 90 s -> Sperre 60 min).
A9 Ufer (Gitter-Attrappe: naechstes Ufer innerhalb 20, Ring-Deckel 160 je Takt, kein Ufer -> 30 min Ruhe, Ebene 1 nie). A10 Reihenfolge (Inventar wartet, solange
DineWants; danach frisst es). A11 Sicht (tro/fno/dww/dine nur fuer den Besitzer).
OBERFLAECHE: O1 Futterliste-Fenster (16 Zeilen, Schalter -> genau eine Bitte, "..." bis Sicht/6 s, Alle erlauben/verbieten), O2 Zahnrad (drei neue Punkte, Troege-
Untermenue mit Zustand/Prozent, Haken Fluss/See), O3 Trog-Rechtsklick (Haken aus der Sicht, grau mit Grund, mehrere Baeren), O4 Pose (dine haelt den eat-Clip in
Schleife, Ton je Schleife einmal, Ende stoppt), O5 Status-Zeile. **Bilder aus dem echten Code** (Mitschrift wie k1/werkzeug_ober/zeichne_k1.py): Fenster DE/EN
1080p + 4K mit Zahnrad offen, Futterliste, Troege-Untermenue, Trog-Rechtsklick -- ersetzen das Entwurf-Bild.

## 11a. Bench (nur `T:client/NCBearBenchDine.lua`, nie in Spiel-Dateien)
`NCBear_DineInfo()` (Zustand, Marken mit Inhalt, Basis-Rechtecke, Sperren), `NCBear_DineScan()` (Ufer-Suche jetzt, Zeit je Takt -> G-T6), `NCBear_TroughFill(art, n)`
(SP: n Stueck Futter bzw. n Liter Wasser in den Trog unter dir -- nur Testhilfe), `NCBear_DineSpeed(k)` (SP: Tempo x k), `NCBear_FoodRule(art, nie)` (SP),
`NCBear_DineForget()` (Sperren loeschen). Uebernahme-Skript `baer/tools/baer_uebernahme.py`: neue `BanditsNPCBear*`-Dateien laufen ueber die Muster mit,
`NCBearBench*` bleibt draussen; Cheat-Pruefung um die neuen Befehle erweitern.

---

## 12. Aufteilung fuer den Bau (8 Agenten, getrennte Dateien)

1. **BAU KERN** -- NEU `shared/BanditsNPCBearDineRules.lua` (reine Regeln: Basis-Test, Wahl, Tempo, fno), NEU `server/BanditsNPCBearDine.lua` (Schritt, Troege,
   Ufer, Bitten, Sicht `B.DineView`), geaendert `shared/BanditsNPCBear.lua` (CFG), `shared/BanditsNPCBearFood.lua` (Arten, FoodKind), `shared/BanditsNPCBearInvRules.lua` (fk),
   `shared/BanditsNPCBearCrew.lua` (Naht 2), `shared/BanditsNPCBearDefs.lua` (Rasse-Toene), `server/BanditsNPCBearServer.lua` (Dispatch + liveRec-Zeile),
   `server/BanditsNPCBearFollow.lua` (DineStop in SetMode), `server/BanditsNPCBearInv.lua` (Futterliste + DineWants), `server/BanditsNPCBearNeeds.lua` (NeedsView ruft
   DineView), `server/BanditsNPCBearHeal.lua` (MARK_FIELDS fno, dww), `TM:scripts/nc_bear_sounds.txt` (NCBear_Drink), `client/NCBearBenchDine.lua`, `baer/NAEHTE.md`,
   Uebernahme-Skript. Attrappen A1-A11.
2. **BAU OBERFLAECHE** -- NEU `client/BanditsNPCBearTroughMenu.lua`, NEU `client/ISUI/BanditsNPCBearFoodWin.lua`, geaendert `client/ISUI/BanditsNPCBearWindow.lua`
   (Untermenue im Zahnrad, neue Schluessel), `client/BanditsNPCBearWinData.lua` (d.gear, Status), `client/BanditsNPCBearPose.lua` (dine-Schleife, Ton, Blick),
   `client/ISUI/BanditsNPCBearInvWindow.lua` (Tooltip "nie"), EN- und DE-Texte. Attrappen O1-O5, Bilder aus dem Code.
3. **BAU TEXTE** -- PTBR, RU, KO, ES, CN, FR (Liste 12a); `NPCCrew/_docs/tools/langcheck.py`; CN/DE nur Zeichen, die Vanilla-CN/-DE benutzt.
4. **PRUEFER CODE** -- vier Pruefer je Datei (luacheck, scopecheck, localcount aktiv+gesamt < 180 -- Server.lua 1206 / Inv.lua 1348 / Window.lua 955 Zeilen
   vorher messen, notfalls Teile in die neue Datei --, luacheck_pz), Engine-Tabelle 9 Zeile fuer Zeile, Namen mit `aussehen/werkzeug/kollision.py`
   (BanditsNPCBearDine*, BanditsNPCBearTroughMenu, BanditsNPCBearFoodWin, NCBearBenchDine, B.Dine*, B.FoodKind, B.FOOD_KINDS, B.CrewBaseRects, UI_BN_Bear_FoodKind_*,
   UI_BN_Bear_FoodList_*, UI_BN_Bear_Trough_*, UI_BN_Bear_Dine_*, NCBear_Drink -- am 14.11. in NPC Crew und Test-Mod frei gegreppt), Ton-Skript-Syntax.
5. **PRUEFER SIM/BILD** -- Attrappen gruen, Mengen-Tabelle 6 nachgerechnet, Bilder aus dem Code gegen Entwurf.
6. **NACHBESSERUNG**, 7. **GEGENPRUEFER** (bereit fuer SP-Test?), 8. **INTEGRATOR** (Staging `mod_troege/` = Test-Mod-Stand, Einbau-Skript nach `tools/einbau_kampf.py`,
   Zips vorher/nachher, nicht bei geladenem NCBearTest, sichern.py, Commit + Push beider Repos, Testanleitung `spiel/anleitung_troege.md`).

### 12a. Texte (je EN + DE im Bau OBERFLAECHE, sechs weitere im Bau TEXTE; Platzhalter %1 wie langcheck)
`UI_BN_Bear_FoodKind_honey/fish/meat/beef/poultry/game/bacon/sausage/seafood/egg/roe/fruit/citrus/berry/nut/insect` (DE: Honig, Fisch, Fleisch, Rindfleisch, Geflügel,
Wild, Speck, Wurst, Meeresfrüchte, Eier, Rogen, Obst, Zitrusfrüchte, Beeren, Nüsse, Insekten); `UI_BN_Bear_FoodList_Title` ("Futterliste - %1"), `_Intro1/2/3`, `_Head`
("Futterarten"), `_Count` ("%1 von %2 erlaubt"), `_Eats` ("Frisst"), `_Never` ("Nie"), `_Fav` ("Lieblingsfutter"), `_WaterHead` ("Wasser (fest)"), `_Water1/2`,
`_AllowAll`, `_ForbidAll`, `_Hint`; `UI_BN_Bear_Gear_FoodList` ("Futterliste ..."), `_FoodListTip`, `_Troughs` ("Tröge (%1 markiert)"), `_TroughsTip`, `_TroughFood`
("Futter für ~%1 %% eines Tages"), `_TroughWater` ("Wasser %1 l"), `_TroughEmpty`, `_TroughFar`, `_TroughRow` ("%1 - %2 Kacheln"), `_TroughClear`, `_Wild`
("Selbst zu Fluss/See gehen"), `_WildTip`; `UI_BN_Bear_Win_GearTip` (geaendert); `UI_BN_Bear_Trough_Menu` ("Für den Bären"), `_Food`, `_Water`, `_Unmark`, `_Tip`,
`_Full`, `_Foreign`, `_TooFar`; `UI_BN_Bear_Note_TroughMarked` ("%1: Trog markiert (%2 von 32)."), `_TroughUnmarked`, `_TroughGone`, `_DineGoWater`, `_DineGoTrough`,
`_DineGoFood`, `_DineFail`; `UI_BN_Bear_State_GoDrink/GoEat/DrinkRiver/DrinkTrough/EatTrough`; `UI_BN_Bear_Inv_FoodNever`. Keine Sandbox-Texte.

---

## 13. Modell-Lauf (getrennt, nur auf Kevins Wort -- Frage T-5)

Ein eigener Trink-Clip `NCBear_Drink` (Schleife ~2,4 s: Kopf tief bis knapp ueber den Boden, Maul leicht auf, 3-4 Zungen-/Kieferschlaege, Schultern sinken etwas,
Vorderbeine leicht gespreizt; Ohren zucken), in ALLEN Koerpern: TM:models_X/Skinned/NCBear.glb, NCBearGen.glb (auch Foto), NCBearCub.glb, NCBearCubGen.glb
(= NCBearBenchCubGen.glb byte-gleich). Knoten `TM:AnimSets/buck/idle/NCBear_Drink.xml` (Form NCBear_Eat.xml: `NCBearAct = drink`, m_Looped true, BlendTime 0,3,
ConditionPriority 10), `B.CLIPS.drink = { dur = 2.40, loop = true }` (T:shared/BanditsNPCBearFightRules.lua:64-87), Schild-Tabelle neu erzeugen
(`k1/werkzeug_plan/kopfhoehe.py --lua ...`, PLAN_K1.md 3), dann `B.CFG.drinkClip = true`. Weg wie baer-liegen (`_arbeit/baer_liegen/WIEDERHOLEN.md`, Kern
`spiel/baer_kern_liegen.py`, Spuren-Skripte), Renders nur RTX 4090/OPTIX, Pruefblatt fuer Kevin. Bis dahin traegt der Fress-Clip (wie Vanilla-Tiere).
Eigener Ton (WAV) nur mit einer Datei von Kevin (kein Download ohne sein Ja je Datei).

---

## 14. Pruef-Tore fuer den Bau
- **G-T1** Trog-Aufrufe am dedizierten Server: alle aus V:server/ClientCommands.lua:1160-1270 (Server-Lua) -- belegt; im Pruefer Zeile fuer Zeile.
- **G-T2** Sicht-Groesse mit 32 Marken (Bytes messen, nur an den Besitzer).
- **G-T3** Ton `NCBear_Drink` (Skript laedt? klingt?) -- Rueckfall `name = "DrinkingFromRiver"` direkt.
- **G-T4** Blick der Kopie im MP (faceThisObject am Client) -- harmlos, wenn nicht.
- **G-T5** Trog in einem Raum (Stall): `B.SpotNear` sucht nur im selben Raum wie die Trog-Kachel (T:server/BanditsNPCBearWorld.lua:294-305) -- Testpunkt.
- **G-T6** Ufer-Suche: Zeit je Takt in der Bench messen (Ziel < 1 ms).
- **G-T7** Safehouse im Einzelspieler: Liste leer erwartet (Log-Zeile).
- **G-T8** Mehrkachel-Trog: Marke auf jedem Stueck landet beim Hauptstueck (alle fuenf Vanilla-Arten).

## 15. Testanleitung (Skizze fuer Kevin; Spiel neu starten)
1. Trog bauen, Wasser einfuellen, Rechtsklick -> "Fuer den Baeren" -> "Wasser daraus trinken". `NCBear_CubNeeds(10, 60, 10, 0)` -> er geht hin, trinkt langsam
   bis 0 %, Trog-Liter sinken; Zahnrad -> "Troege" zeigt Liter.
2. Zweiten Trog mit Steaks + Zitronen, markieren (Futter). Futterliste: Zitrusfruechte auf Nie. Hunger 60 -> frisst nur Steaks.
3. Am Fluss (bis 20 Kacheln), Durst 60, "Folgen" -> er geht trinken; waehrend er trinkt: Zombie kommt -> bricht ab und kaempft; "Bleiben" druecken -> bricht ab.
4. Zahnrad -> "Selbst zu Fluss/See gehen" aus -> er trinkt aus seinem Inventar (K1) statt zu gehen.
5. 33. Trog markieren -> Meldung "voll".

---

## 16. Fragen fuer Kevin (gebaut wird jeweils die Empfehlung)

- **T-1 Ohne Basis:** Wenn es keine NPC-Crew-Basis und kein Safehouse gibt (z. B. Einzelspieler ohne NPC Crew): (a) markierte Troege bis 40 Kacheln um den Baeren
  **(Empfehlung)**, (b) Troege nur mit Basis, (c) jede Entfernung, solange die Gegend geladen ist.
- **T-2 In welchem Befehl geht er selbst hin?** (a) Folgen, Frei laufen und Bleiben -- bei Bleiben kommt er danach an seine Stelle zurueck; Sitz nie **(Empfehlung)**,
  (b) nur Folgen und Frei laufen, (c) auch im Sitz.
- **T-3 Was zuerst?** (a) erst Trog/Fluss (kostet nichts), sein Inventar nur, wenn nichts erreichbar ist **(Empfehlung)**, (b) erst sein Inventar, dann Trog/Fluss.
- **T-4 Wie langsam?** (a) Trinken UND Fressen am Trog/Fluss 50 % je Spielstunde -- von 50 auf 0 in etwa einer Spielstunde (~4 echte Minuten) **(Empfehlung)**,
  (b) Trinken so langsam, Fressen schneller (ein Stueck je 10 Spielminuten wie aus dem Inventar), (c) doppelt so schnell (halbe Spielstunde).
- **T-5 Trink-Animation:** Vanilla-Tiere haben keine eigene -- sie trinken mit dem Fress-Bild. (a) erst mit unserem Fress-Clip bauen, eigener Trink-Clip spaeter im
  Modell-Lauf **(Empfehlung)**, (b) eigenen Trink-Clip zuerst bauen (Modell-Lauf vor dem Funktions-Bau), (c) Fress-Clip reicht fuer immer.
- **T-6 Trink-Ton:** Vanilla-Tiere trinken lautlos. (a) Vanillas Ton "aus dem Fluss trinken" leiser am Baeren **(Empfehlung)**, (b) kein Ton, (c) eigener Ton --
  dann brauche ich eine Ton-Datei von dir.
- **T-7 Futterliste als:** (a) 16 Futterarten in einem kleinen Fenster ueber das Zahnrad, Frisst/Nie je Klick (Bild) **(Empfehlung)**, (b) direkt im Zahnrad als
  Untermenue (je Klick eine Art, das Menue geht danach zu), (c) wie NPC Crew je einzelnem Lebensmittel (lange Liste).
- **T-8 Wie weit zum Fluss/See?** (a) bis 20 Kacheln **(Empfehlung)**, (b) bis 10, (c) bis 30.
