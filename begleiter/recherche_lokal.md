# Baer als Begleiter: was die lokalen Tier-Mods machen (08.11.2026)

Nur gelesen, nichts kopiert. Es geht um Ideen und um die Mechanik dahinter; gebaut wird spaeter eigener Code.
Kevin will nicht wie ein Dieb rueberkommen, deshalb steht bei jeder Idee, woher sie kommt.
`WS` = `C:/Program Files (x86)/Steam/steamapps/workshop/content/108600`. Jar = `projectzomboid.jar` 42.21, mit javap gelesen.
Statisch gelesen, nichts gespielt.

## Kurzfazit

1. **Wachsen geht mit Vanilla-Mitteln.** Ein Tier waechst innerhalb einer Stufe jeden Spieltag von `minSize` bis `maxSize`
   (Jar `AnimalData.growUp`, Offset 40-130). Der Baer hat heute `minSize = maxSize = 1.0` (NCBearDefs.lua:60-61), deshalb waechst er nicht.
2. **Die Falle beim Stufenwechsel:** ein Wechsel Baby -> erwachsen baut ein NEUES Tier und verliert dabei unsere Daten am Tier
   (Level, XP, Besitzer). Die Engine behaelt aber die Tier-Id. Horse Mod und Companion Dogs umgehen das je auf eigene Art.
3. **Unsterblich gibt es in Vanilla schon:** `setIsInvincible` (Lua-belegt). Es wird nicht gespeichert und muss nach jedem Laden
   neu gesetzt werden. Einen Downed-Zustand hat keine der Mods.
4. **Zombies greifen Tiere von sich aus nicht an.** Damit der Baer gegen Zombies sterben kann, muessen wir den Schaden selbst bauen
   (Horse Mod tut das fuer das gerittene Pferd).
5. **Im Mehrspieler laufen alle drei grossen Mods auf dem Server** (Tier-KI ist dort). Das bestaetigt CLAUDE.md Abschnitt 5.

## Gelesene Mods

| Mod | Ordner | Was sie am Tier-System aendert |
|---|---|---|
| Horse Mod 1.1.2 (Horse team) | `WS/3661336777/mods/HorseMod` | eigenes Tier 'horse' in drei Stufen (Fohlen, Stute, Hengst), Reiten, Ausdauer, Sattel und Taschen, Spawn ueber Ranch-Zonen |
| Companion Dogs | `WS/3740052292/mods/CompanionDogs` | Hunde als Begleiter: zaehmen durch Fuettern, Welpen wachsen, 5 Skills bis Level 10, eigener Hunger und Durst, Tierarzt, immer unverwundbar |
| Companion Dogs Pack | `WS/3796123931/mods/CompanionDogsPack` | Rudel aus mehreren Hunden, Formation, Abzug je zusaetzlichem Hund |
| Animal Collectors | `WS/3640001799/mods/AnimalCollectors` | Waschbaer und Schwein lernen per Aktion, Gegenstaende einzusammeln; Bulle und Eber faellen Baeume |
| Baby Animal Food | `WS/3422249642/mods/BabyAnimalFood` | Futter fuer verwaiste Jungtiere (sonst trinken sie nur bei der Mutter) |
| Animals do not ... (5 Stueck) | `WS/3469436421/mods` | je ein Schalter fuer alle Tiere: kein Angriff auf Spieler, auf Gebaeude, auf andere Maennchen, kein Mist, kein Stress |
| Nearby Animals (DBD) | `WS/3658756227/mods/DBD_NearbyAnimals` | Fenster mit allen Tieren in 10 Kacheln: Leben, Hunger, Durst, Stress |
| Increase Animal Trailer Capacity | `WS/3794010524/mods/IncreaseAnimalTrailerCapacity` | Anhaenger fassen 2000 statt Vanilla |
| Meat Expansion 2.0 | `WS/3700009701/mods/Meat Expansion 2.0` | Grizzly nur als Spur im Suchmodus und als Kadaver, kein lebendes Tier |

Nicht relevant: ZombieBuddy (Java-Lader), Farming-Mods (Pflanzen).

## 1. Wachsen (Baby -> grosser Baer)

**Vanilla, im Jar gelesen:**
- `AnimalData.update` (Offset 43-112): einmal je neuem Spieltag laeuft `growUp`.
- `growUp` (Offset 40-130): Groesse += (maxSize - minSize) / ageToGrow x Gesundheit, hoechstens maxSize. Gewicht genauso.
  Ein krankes Tier waechst also langsamer. In einem zu kleinen Gehege geht es achtmal langsamer (Offset 86-107, `smallEnclosure`).
- Laeuft auch fuer Tiere, die nicht geladen waren (`IsoAnimal.updateStatsAway` ruft `growUp`).
- Die Darstellung haengt an `getAnimalSize()` = `AnimalData.getSize()` (IsoAnimal, Offset 0-7). Knochen werden damit in
  Weltkoordinaten skaliert (`Model.boneToWorldCoords`, Offset 54-90). Dass das sichtbare Modell mitwaechst, ist sehr wahrscheinlich; im Spiel pruefen.
- Vanilla-Sandbox 'Aging Modifier Speed' beschleunigt das Altern aller Tiere (Translate/EN/Sandbox.json:905; Faktoren 90/10/5/1 in
  `AnimalData.getAgeGrowModifier` 0-75, welche Stufe welcher Faktor ist: ungeprueft).
- Ein Gen `maxSize` wuerde min und max noch mit einem Zufallswert malnehmen (`AnimalData.getMinSize` 11-75). NCBearDefs.lua:14 laesst es weg, gut so.

**Zwei Wege fuer den Baeren:**
- **Weg A, eine Stufe, ein Modell:** `minSize` klein, `maxSize` gross, `ageToGrow` = Tage bis ausgewachsen. Kein Stufenwechsel, also auch keine Datenfalle.
- **Weg B, zwei Stufen** (wie Horse Mod: `filly` -> `mare`/`stallion`, HorseDefinitions.lua:87-107, mit eigenem Fohlen-Modell :226-249):
  eigenes Jungtier-Modell moeglich (Kopf groesser, Beine kuerzer), aber der Stufenwechsel ist die Falle unten.

**Die Falle beim Stufenwechsel (Jar `AnimalData.grow`):** baut ein neues `IsoAnimal` (Offset 58-95), kopiert Alter, Werte, Zahmheit
(`playerAcceptanceList` 213-219), Gene, Name, `invincible` und die **Tier-Id** (298-304), ruft aber nirgends `getModData`.
Alles, was wir am Tier speichern, ist danach weg. Companion Dogs schreibt dasselbe in einen Kommentar (Mounted.lua:168).
- Horse Mod speichert Tierdaten unter der Tier-Id in einem globalen ModData und holt sie beim naechsten Sehen zurueck
  (HorseModData.lua:216-235; genutzt beim Aufheben, AnimalPickup.lua:11-16).
- Companion Dogs laesst den Engine-Wechsel gar nicht zu: haelt das Alter knapp unter der Grenze (Mounted.lua:168-172), erzwingt die
  Welpengroesse (`setSizeForced`, :160-166) und tauscht selbst: neuen Erwachsenen bauen, Daten kopieren, Lebensanteil uebertragen,
  Welpen entfernen (Stash.lua:123-173). Dazu 'Wachstum anhalten' je Welpe (ContextMenu.lua:368, Commands.lua:1189).

## 2. Wie bekommt man den Baeren?

- **Zaehmen durch Fuettern** (Companion Dogs): Streuner, Vertrauen steigt mit Futter bis 'TameThreshold' (Vorgabe 100,
  Sandbox.json:3-4), schlechtes Futter senkt es. Obergrenze 'Max pets per player' (0 = unbegrenzt, Sandbox.json:5). Passt zu
  Kevins 'jeder Spieler einen Baeren': Grenze 1 als Vorgabe.
- **Feste Orte auf der Karte** (Horse Mod): Ranch-Zonen ueber `OnLoadMapZones` (HorseZones.lua:308). Wirkt nur in NEUEN Welten,
  die Mod warnt sonst per Fenster (ChangeLog.txt:11, WorldStamp.lua).
- **Spur im Suchmodus** (Idee aus Meat Expansion, dort Grizzly-Spuren -> Jagd, MEH_Definitions.lua:20-24): bei uns koennte
  eine Baerenspur zu einem verwaisten Jungtier fuehren.
- **Ausbilden per Aktion mit Skill-Voraussetzung** (Animal Collectors: Animal Husbandry Stufe 5, Sandbox; Babys und wilde
  Tiere ausgeschlossen; gibt dem Spieler XP, ISTrainAnimalAction.lua). Idee fuer 'Kunststuecke' des Baeren.

## 3. Baby kann nicht kaempfen

- Horse Mod: Reiten erst ab erwachsen (MountingUtility.lua:125-126). Animal Collectors: 'Cannot train baby animals'.
- Companion Dogs: je Rasse `combatPower`, `canKill`, `canKnockdown`, `lethalityCurve` (Skills.lua:11-28: der Caramelo darf
  umwerfen, aber nicht toeten). Idee: Baby = kein Angriff, Jungbaer = nur umwerfen, erwachsen = toeten.

## 4. Staerker werden, Level

- **Companion Dogs:** 5 Skills (Witterung, Kampf, Gehorsam, Jagd, Hueten), je bis Level 10 (Skills.lua:4-6). XP fuer Level n
  gesamt = 20 x n x (n+1) / 2 (Lineage.lua:165-167). Sandbox 'SkillXPRate' (Vorgabe 0.5) und 'DogDamageMultiplier'.
  Kampf-Level: mehr Schaden, weniger Panik (IG_UI.json). Gehorsam: weniger verweigerte Befehle.
- **Horse Mod:** eigene Gene `speed`, `stamina`, `carryWeight`, `strength` mit festen Spannen (HorseGenes.lua:1-25), gelesen mit
  `getUsedGene(...):getCurrentValue()` (HorseManager.lua:69-76). Idee: jeder Baer hat leicht andere Anlagen, das Level kommt obendrauf.
- Bei uns heisst das: Lebenspunkte, Schaden, Ausdauer aus Alter UND Level rechnen; Level-Daten unter der Tier-Id ablegen (Abschnitt 1).

## 5. Ausdauer

Horse Mod (Stamina.lua): Wert 0-100 im ModData des Pferds, je Sekunde Galopp -2, Trab +3, Schritt +5, Stehen +7.5
(:14-23); Galopp erst ab 15 % (:10, :109); Abgleich ueber `transmitModData` (:71). Gerechnet nur im Einzelspieler und auf dem
Server (StaminaSystem.lua:1). Sandbox 'StaminaMultiplier'. Idee: Baeren-Ausdauer, die mit dem Level waechst; muede = langsamer, kein Sprint.

## 6. Sterben, unsterblich, downed

**Vanilla:** `animal:setIsInvincible(bool)` ist Lua-belegt (Vanilla ISAnimalContextMenu.lua:563, Debug-Menue). Im Jar: `setHealth`
ignoriert jede Senkung, solange invincible (IsoAnimal.setHealth 0-16); `changeStress` ignoriert dann negative Werte, Stress kann
also nicht sinken (changeStress 0-13). Das Feld lesen und schreiben nur Getter und Setter (javap IsoAnimal; im ganzen Jar rufen nur
IsoAnimal und AnimalData sie), also **wird es nicht gespeichert**. Jungtiere und der Stufenwechsel erben es (addBaby 234-239, grow 398-404).

**Companion Dogs** (Vorgabe: Begleiter immer unverwundbar):
- Setzt `invincible` bei jedem neu erzeugten Hund wieder, weil das Flag nach dem Laden fehlt (Mounted.lua:89-113), dazu `setShootable(false)`.
- Leben aendern sie selbst: im selben Lua-Schritt aus, `setHealth`, wieder an (Upkeep.lua:126-141).
- Sandbox 'Death' (Vorgabe aus, Sandbox.json:71): aus = Hunger und Krankheit senken das Leben nur bis 10 % (Upkeep.lua:131-134, Wert in config/Vet.lua:35).
  Das kommt Kevins 'downed statt tot' am naechsten, ist aber kein eigener Zustand.
- Kampf mit Zombies: kein Tod, sondern Wuerfel auf Wunde, Bruch, Floehe (Vet.lua:800-825), die man behandeln muss.

**Horse Mod:** Zombies schlagen das Pferd nicht von selbst. Beisst ein Zombie den REITER, wird der Treffer aufs Pferd umgelenkt
(OnZombieUpdate, `AttackOutcome == "success"`, PlayerDamage.lua:430-452), 0.1-0.3 Leben (HorseDamage.lua:10-12, 54-58). Ihr eigener
Hinweis: Zombie-Updates laufen beim Hoheits-Rechner, nicht auf dem Server (PlayerDamage.lua:426). Stirbt das Pferd unter dem
Reiter, fallen Zombies im Umkreis 2.5 um (Riding.lua `dismountOnHorseDeath`, HorseDamage.lua:19-41).

**Fuer uns:** keine Mod hat einen Downed-Zustand (grep 'downed/unconscious' in Companion Dogs: 0). Den bauen wir selbst, z. B.
bei wenig Leben `invincible` an, liegen, Aufhelfen mit Gegenstand. Wo NPC Crew das fuer Menschen macht, liest ein anderer Lauf.

## 7. Fuettern und Trinken

- Vanilla-Felder je Tier (Beispiel Horse Mod HorseDefinitions.lua:190-197): `eatTypeTrough`, `hungerMultiplier`, `thirstMultiplier`,
  `healthLossMultiplier`, `thirstHungerTrigger`. Jungtiere mit `eatFromMother = true` trinken nur bei der Mutter (Vanilla PigDefinitions.lua:117).
- Baby Animal Food: gibt Jungtieren eine eigene Futterart (BabyAnimalDifinitions.lua:2-5) und ein Schuessel-Futter mit
  `AnimalFeedType` aus Milch (BabyAnimalFood_items.txt, _recipes.txt). Idee: Baerenjunges braucht Milchbrei, spaeter Fleisch, Fisch, Beeren.
- Companion Dogs: eigener Hunger und Durst mit Nachholen nach Abwesenheit (hoechstens 6 Stunden auf einmal, Needs.lua:158),
  Eiweiss-Bedarf ('ProteinHours' 72), Napf, Auto-Fuettern ab Schwelle, Zuneigung sinkt bei Hunger schneller ('LoyaltyDecayPerDay' 12).
- Animal Collectors: bei Hunger oder Durst ueber 0.6 hoert die Arbeit auf und die Vanilla-KI uebernimmt (AnimalCollectorsConfig.lua:28).

## 8. Anzeige

- Nearby Animals: Balken fuer Leben, Hunger, Durst, Stress. Falle laut ihrer Notiz: `getStress` liefert 0-100, die anderen 0-1 (mod.info).
- Companion Dogs: Statusfenster und Liste 'Meine Begleiter' mit 'in der Naehe / weg / vermisst / zuletzt gesehen vor', Namensschild,
  Rufen mit Pfiff (lockt Zombies).

## 9. Mehrspieler

- Companion Dogs: fast alles unter `server/`, Rueckmeldung an Clients per Befehl. Sandbox 'DespawnOnOwnerOffline' (Vorgabe an):
  der Hund geht mit dem Besitzer offline.
- Horse Mod: der Server bewegt das gerittene Pferd (`setX`/`setY`, ServerRiding.lua:402-403), der Client schickt nur Eingaben.
  Ihr Hinweis: ein dedizierter Server tickt mit etwa 10 Hz (ServerRiding.lua:31).
- Animal Collectors: Server-OnTick schickt das Tier mit `animal:pathToLocation(x, y, z)` (AnimalCollectorsServer.lua:417, :479) und
  haelt es mit `stopAllMovementNow()` an.

## 10. Vertraeglichkeit

- Die fuenf 'Animals do not ...'-Mods aendern beim Start ALLE Tiere, also auch den Baeren (z. B. `attackBack = false`,
  `knockdownAttack = false`, 'do not attack player'.lua:2-7). Haengt der Baeren-Kampf an diesen Feldern, schaltet so eine Mod ihn ab.
- Horse Mod meldet sich unvertraeglich mit RIDINGAPI, WolfoMod, Run and Reload (mod.info). Fuer uns nur wichtig, falls wir reiten wollen.
- Anhaenger: der Baer hat `trailerBaseSize = 600` (NCBearDefs.lua:72). Ob er in einen Vanilla-Anhaenger passt: ungeprueft.

## Ideenliste fuer Kevin (eigener Code, Herkunft dabei)

| Idee | Herkunft |
|---|---|
| Baby waechst jeden Tag sichtbar, Dauer als Sandbox-Wert | Vanilla `growUp`; Sandbox wie Companion Dogs 'MaturityDays' |
| Wachstum anhalten (Baby bleibt klein) | Companion Dogs |
| Zaehmen durch Fuettern, ein Baer je Spieler | Companion Dogs 'TameThreshold', 'Max pets per player' |
| Junges ueber eine Spur im Suchmodus finden | Meat Expansion (Spuren) |
| Baby kaempft nicht, Jungbaer wirft nur um, erwachsen toetet | Companion Dogs `canKnockdown`/`canKill` |
| Level und XP je Faehigkeit, XP-Faktor in der Sandbox | Companion Dogs Skills |
| Anlagen je Baer (Kraft, Ausdauer, Tempo leicht verschieden) | Horse Mod Gene |
| Ausdauer, die beim Laufen sinkt und im Stehen zurueckkommt | Horse Mod Stamina |
| Unsterblich-Schalter in der Sandbox (Vorgabe aus), dann downed statt tot | Vanilla `setIsInvincible`; Companion Dogs 'Death' |
| Wunden aus Kaempfen, die man behandelt | Companion Dogs Tierarzt |
| Milch fuer das Junge, spaeter Fleisch/Fisch, Wassernapf | Baby Animal Food, Companion Dogs Napf |
| Zuneigung sinkt bei Hunger | Companion Dogs 'LoyaltyDecayPerDay' |
| Statusfenster mit Balken, 'zuletzt gesehen' | Nearby Animals, Companion Dogs |
| Erwachsenen Baeren reiten, Satteltaschen | Horse Mod (gross, eigener Lauf, erst sehr spaet) |
| Baer geht mit dem Besitzer offline | Companion Dogs 'DespawnOnOwnerOffline' (wie NPC Crew Logout-Parken) |

## Offen und ungeprueft

- Ob das sichtbare Modell wirklich mit `getSize` skaliert wird (sehr wahrscheinlich, im Spiel ansehen).
- Was passiert, wenn der Baer mit nur einer Stufe `ageToGrow` erreicht (kein `nextStage`): `AnimalData.checkStages` nicht gelesen.
- Ob `invincible` im Mehrspieler zum Client reist (nur der Server braucht es, weil dort Schaden gerechnet wird): nicht gelesen.
- Eigene Zahlen der Mods (Companion Dogs Schaden, Horse Mod Ausdauer) sind deren Balance, keine Engine-Werte.
