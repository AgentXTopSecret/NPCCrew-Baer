# Companion Dogs: was es loest, wie, und was davon fuer den Baeren taugt

Stand 08.11.2026. Nur gelesen, nichts kopiert. Quelle: Companion Dogs 0.7.4 (Workshop 3740052292, "ALPHA", pzversion
42.19) und DogPack 0.9.8 (Workshop 3796123931, Zusatzmod). Rund 46.000 Zeilen Lua zusammen. Die mod.info erlaubt
Add-ons mit Nennung, sonst kein Weiterverwenden ihrer Inhalte; wir nehmen nur Ideen und nennen die Herkunft.
Fundstellen unter `CD:` = `C:\Program Files (x86)\Steam\steamapps\workshop\content\108600\3740052292\mods\CompanionDogs\42\media\lua\`,
`PACK:` = `...\3796123931\mods\CompanionDogsPack\42\media\`. Jar-Stellen aus `projectzomboid.jar` 42.21 (javap im Scratchpad).

## Kurz

* Fast alles, was Kevin will, hat Companion Dogs schon fuer Hunde geloest: zaehmen durch Fuettern, Folgen/Bleiben/Wache,
  kaempfen, Hunger/Durst/Treue, Level (5 Faehigkeiten bis 10), Welpen, Tod per Sandbox-Schalter, Speichern, Mehrspieler.
* **Die zwei Luecken sind genau Kevins Kernwuensche:** der Hund stirbt NICHT im Kampf (Zombies greifen Tiere gar nicht an,
  und Companion Dogs macht ihn zusaetzlich unverwundbar), und er waechst nur in EINEM Sprung (Welpe -> Erwachsen), nicht stetig.
* Stetiges Wachsen kann die Engine selbst (taeglich etwas groesser, mit Gesundheit gewichtet). Der Stufenwechsel der Engine
  baut aber ein NEUES Tier ohne ModData -- das ist der Grund, warum Companion Dogs ihn umgeht. Beides im Jar belegt (Abschnitt 7).
* Mehrspieler: bei ihnen rechnet ALLES der Server (bzw. der Einzelspieler), Clients schicken nur Bitten. Das ist das
  Gegenteil von NPC Crew und passt zum Tier, weil der Server die Tier-KI rechnet.

---

## 1. Bauweise

* Das Gehirn laeuft nur ausserhalb eines MP-Clients: `if not isClient()` meldet den OnTick an (`CD:server/CompanionDogs_Companion.lua:1046-1048`),
  also im Einzelspieler und auf dem dedizierten Server. Ein MP-Client hat nur Fenster, Menues und Bitten.
* Bitten: `CD.request` ruft im SP den Server-Handler direkt, im MP `sendClientCommand` (`CD:shared/CompanionDogs/kennel/Registry.lua:492-505`);
  der Server verteilt per `Events.OnClientCommand` an `CD.Server.<befehl>` (`CD:server/CompanionDogs_Commands.lua:2439-2455`, rund 70 Befehle).
  Jeder Handler prueft den Besitz selbst (z. B. `notyourdog` `Commands.lua:213-216`, `setgrowthmode` `:1188`).
* Zustand des Hundes: eine Tabelle im ModData des Tiers (`getModData().CompanionDogs`), verschickt mit `animal:transmitModData()`
  (`CD:shared/CompanionDogs/core/Identity.lua:93-97`). Zustand des Spielers: ModData des Spielers (`CD.playerData`, `Identity.lua:111`).
* Der Hund ist ein gewoehnliches `IsoAnimal` mit eigener Art (`dogmale`, `dogfemale`, `dogpup` usw.,
  `CD:shared/Definitions/animal/DogDefinitions.lua`). Modell auf dem Waschbaer-Skelett, AnimSet `raccoon`; ihr Kommentar: ein
  eigener AnimSet-Name lade nicht und das Tier friere ein (`DogDefinitions.lua:169`, ihre Aussage, ungeprueft).
  Eigene Bewegungen haengen sie als zusaetzliche Knoten in den Vanilla-Ordner `AnimSets/raccoon/idle|walk|pathfind/`, jeder
  hinter einer eigenen Variable (`cdAttack`, `cdEat`, `cdRest` ... `CD:../AnimSets/raccoon/idle/cdAttack.xml`), Clips von Vanilla (`Rac_Attack`).
  **Fuer den Baeren:** derselbe Weg geht unter `AnimSets/buck/` (Kevins Baer nutzt `buck`), die Clips muessen dann aus dem
  Baeren-Modell kommen.

## 2. Wie bekommt man den Hund

* **Streuner** entstehen beim Laden eines Chunks in Gebaeuden je Gebaeudeart: Haus, Polizei (Schaeferhund), Tierarzt, Hof
  (Border Collie), Husky nur im Winter (`CD:shared/CompanionDogs/config/SpawnRegistry.lua:31-41`, `CD:server/CompanionDogs_Spawn.lua:570-588`).
  Sandbox `DogSpawnMultiplier`.
* **Zaehmen = Vertrauen durch Fuettern**: jedes Futter aus der Hand gibt Vertrauen nach dem Hungerwert; ab `TameThreshold`
  (Vorgabe 100) wird er zum Begleiter (`Commands.lua:212-306`, Schwelle `:278`, `CD.makeCompanion` `CD:shared/CompanionDogs/kennel/Kennel.lua:240-267`).
  Giftiges Futter kostet Vertrauen (`Commands.lua:267-272`).
* **Limit je Spieler**: Sandbox `MaxCompanions` (0 = unbegrenzt), geprueft beim Zaehmen (`Commands.lua:279-283`).
* **Welpen** aus eigener Zucht (`CD:server/CompanionDogs_Breeding.lua`, `CD.makePuppy` `Kennel.lua:273`). Sie schalten die
  Zucht der Engine absichtlich ab (kein `mate`, `DogDefinitions.lua:246`).

**Taugt fuer den Baeren:** ja, fast 1:1 als Idee. Ein Baerenjunges an einem seltenen Ort (Wald, Wildnis statt Gebaeude),
anfuettern bis Vertrauen voll, Limit 1 je Spieler als Sandbox-Zahl. Herkunft: Companion Dogs (Streuner + TameThreshold + MaxCompanions).

## 3. Folgen und Befehle

* Drei Zustaende: folgen, bleiben, Wache (`CD:shared/CompanionDogs/config/Base.lua:40-42`), dazu Komm-her, Angriff, Jagd an/aus,
  Pflege-Modus (Hoftiere), Tricks (Gehe-zu, Ablenken, Erschnueffeln, Apportieren -- je nach Gehorsam-Level).
* Laufen ueber die Engine: `pathToLocation` / `pathToCharacter` + Variable `bPathfind` + `getBehavior():setBlockMovement(false)`
  (`Companion.lua:77-97`, `:163-180`; Folgen `CD:server/systems/CompanionDogs_Follow.lua:518/:577`).
* Steckt ein FOLGENDER Hund fest (Abstand waechst nicht, Weg scheitert), setzen sie ihn neben den Besitzer
  (`Follow.lua:313-340`, `CD.teleportRecover`). Ein Hund auf "Bleiben" wird so nicht versetzt (nur im Folge-Zweig).
* Treue sinkt je Tag (Sandbox `LoyaltyDecayPerDay`), unter einer Untergrenze gehorcht er nicht (`CD.isDisloyal`,
  `CD:shared/CompanionDogs/core/Status.lua:7-9`); ein ungeuebter Hund kann einen Befehl ignorieren (mod.info, Sandbox abschaltbar).
* Bedienung: Rechtsklick-Menue, Radialmenue, eigene Tasten (`CD:client/CompanionDogs_ContextMenu.lua`, `_RadialCommands.lua`, `_Keybinds.lua`).

**Taugt:** Befehlsliste und Folgen ueber `pathToCharacter` direkt. Das "Versetzen beim Feststecken" nur beim Folgen und nur zum
Besitzer -- Kevins rote Linie (kein Basis-Begleiter beim Spieler) bleibt so gewahrt.

## 4. Kampf

* Ziele: Zombies im Umkreis (`CD.ZOMBIE_ATTACK_RADIUS = 8`, `CD:shared/CompanionDogs/config/Base.lua:118`), dazu FEINDLICHE
  Bandits-NPCs; freundliche (rekrutiert/loyal) und markierte NPCs anderer Mods werden ausgenommen, auf dem Server ueber den
  Bandits-Cluster (`Identity.lua:17-78`, Cluster `:23-28`, `brain.recruited` `:31`). **Damit greift er die Crew von NPC Crew nicht an.**
* Ein Biss ist KEIN Engine-Angriff: Animation ueber eine Variable (`CD.emitAnim` `CD:server/CompanionDogs/core/Anim.lua:196-205`,
  Client `CD:client/CompanionDogs_Client.lua:548-556`), Schaden per `setHealth` am Zombie (`CD:server/systems/CompanionDogs_Strike.lua:14-129`).
  Abklingzeit 0,9 s, Grundschaden 0,6 (`CD:shared/CompanionDogs/config/Motion.lua:139-142`), mal Rasse, Level, Gen, Sandbox
  `DogDamageMultiplier` (`CD:shared/CompanionDogs/skills/Lineage.lua:298-312`).
* Umwerfen: Chance 10 % + 4 % je Kampf-Level, hoechstens 50 % (`Motion.lua:144-146`, `Lineage.lua:317-320`), ausgefuehrt mit
  `z:knockDown(false)` (`Kennel.lua:566-576`).
* Rassen-Schalter: `canKill = false` (kann nur verletzen, Zombie bleibt ueber einem Rest), `combatPower`, Faehigkeit "combat"
  abschaltbar je Rasse (`CD:shared/CompanionDogs/skills/Skills.lua:303-358`).
* Rueckzug bei 10 % Gesundheit (`Companion.lua:474`, `Motion.lua:147`).

**Taugt:** sehr. Baby = "kann nicht kaempfen" ist bei ihnen genau so ein Rassen-Schalter; beim Baeren waere es ein Schalter je
Alter/Groesse. Schaden und Umwerfen wachsen mit dem Level -- beim Baeren zusaetzlich mit der Groesse. Herkunft: Companion Dogs.

## 5. Schaden, Tod, kein "Downed"

* **Zombies greifen Tiere in der Engine nicht an** (CLAUDE.md Abschnitt 5, 17.09.: AttackState kennt kein Tier, spottedNew nur
  Spieler; Bytecode). Companion Dogs simuliert deshalb keinen Kampfschaden am Hund.
* **Dazu machen sie den Begleiter unverwundbar:** `setIsInvincible(true)` beim Zaehmen (`Kennel.lua:264`) und in jedem Durchlauf
  neu (`CD:server/CompanionDogs/life/Mounted.lua:77-87`; ihr Kommentar `:89`: der Wert wird nicht gespeichert, ungeprueft),
  Waffentreffer werden in `OnWeaponHitCharacter` mit `setAvoidDamage(true)` geschluckt (`CD:server/systems/CompanionDogs_GunGuard.lua:91-97`,
  `:219`) -- das trifft auch Kugeln von Bandits. Feuer: loeschen, Leben zuruecksetzen, wegsetzen (`CD:server/systems/CompanionDogs_Fire.lua:72-100`).
* Leben verliert er nur ueber eigene Rechnungen: Vernachlaessigung (Hunger/Durst ueber 0,8, `CD:server/systems/CompanionDogs_Upkeep.lua:128-141`),
  Krankheiten und Wunden des Tierarzt-Systems (`CD:server/systems/CompanionDogs_Vet.lua:201-217`; Wunde 0,4 % je Biss, `:802-826`),
  ein Hirsch, der sich wehrt (`CD:server/systems/CompanionDogs_Hunting.lua:217-222`). Zum Abziehen schalten sie die
  Unverwundbarkeit fuer genau zwei Zeilen aus (`Upkeep.lua:137-139`).
* Sandbox `Death` (Vorgabe AUS): aus = jede Abnahme stoppt bei 10 % (`CD:shared/CompanionDogs/config/Sandbox.lua:242-250`,
  `CD:shared/CompanionDogs/config/Vet.lua:35`); an = bei 0 stirbt er endgueltig (`Upkeep.lua:84-92`: `Kill`, Platz frei,
  Satteltasche faellt, Trauer-Moodle beim Besitzer, naechster Hund rueckt nach `:6-80`).
* Einen Zustand "liegt am Boden, muss aufgeholfen werden" gibt es NICHT. Naechstes Gegenstueck: 10 % Boden + Humpeln
  (`cdLimpFront/Back`, `Vet.lua:234-235`) + verweigert den Kampf (`Status.lua:165-167`).

**Fuer den Baeren heisst das:** "stirbt gegen Zombies/Bandits" muessen WIR rechnen (Zombie in Reichweite -> Treffer-Wurf ->
Leben ab, weniger mit Level/Groesse), Bandits-Waffentreffer kommen dagegen als echtes Ereignis an und koennen durchgelassen statt
geschluckt werden (dass Bandits ueberhaupt auf Tiere zielen: ungeprueft). "Unsterblich = downed" ist bei ihnen nicht geloest;
naheliegende Form: bei 0 nicht sterben, sondern hinlegen (Liege-Clip), nicht kaempfen, Aufhelfen per Rechtsklick. NPC Crew hat das
fuer Zombie-Begleiter (Downed-Programm); beim Tier faellt alles weg, was Bandits dort liefert. Vorgabe bei Kevin umgekehrt: Tod AN, Unsterblich AUS.

## 6. Beduerfnisse

* Hunger und Durst sind die Engine-Werte (`Stats` HUNGER/THIRST, `Companion.lua:8-20`), aber das Steigen rechnet ihr eigener
  Takt alle 3 Spielminuten nach der Weltuhr (`Upkeep.lua:97-127`, `CD:shared/CompanionDogs/config/Needs.lua:139`), Sandbox
  `UpkeepEnabled`, `NeedsRateMultiplier`.
* **Zeit, in der der Hund nicht geladen war, zaehlt nicht** (`Upkeep.lua:104-110`, `CD.wasInPlay` `Mounted.lua:67`); ihr Grund:
  sonst kam ein an der Basis gelassener Hund mit einem Schlag 0,75 Leben weniger zurueck (`Mounted.lua:58-61`). Zeit, in der der
  BESITZER offline war, laeuft als "Schuld" mit (`Companion.lua:65-73`).
* Futter: aus der Hand (Timed Action `CD:client/TimedActions/ISCDFeedDog.lua`), aus Napf (eigener Gegenstand, `CD:shared/CompanionDogs/core/Dish.lua`)
  und aus dem Vanilla-Trog (`CD:server/systems/CompanionDogs_Feed.lua:4-90`, er laeuft selbst hin `:340`). Wasser ebenso.
  Eiweissbedarf (Sandbox `ProteinNeedEnabled`), Liste schaedlicher Speisen (`CD:shared/CompanionDogs/core/Diet.lua`).
* Fuettern hebt Gesundheit und Treue, senkt Stress (`Commands.lua:238-264`).

**Taugt:** alles. Fuer einen Baeren passen Fisch, Fleisch, Beeren, Honig als eigene Liste. Die Regel "nicht geladen = keine
Zeit" ist wichtig, sonst verhungert ein Baer an der Basis, waehrend man weit weg ist.

## 7. Wachstum (Welpe -> Erwachsen) und was die Engine kann

* Companion Dogs: zwei Stufen. Welpe hat feste Groesse (`CD.PUPPY_SIZE = 0.6`, `Base.lua:38`), jeden Durchlauf neu gesetzt mit
  `getData():setSizeForced(...)` (`Mounted.lua:160-166`). Nach `MaturityDays` (Vorgabe 90 Tage) baut ihr Code ein NEUES
  erwachsenes Tier an derselben Stelle und kopiert die ModData hinueber, Gesundheit als Anteil (`CD:server/systems/CompanionDogs_Stash.lua:123-172`, Takt `:175-192`).
  Wachstum pausieren per Menue (`Commands.lua:1185-1191`).
* Warum so umstaendlich: sie halten `hoursSurvived` zwei Tage unter der Stufengrenze, weil der Stufenwechsel der Engine ein neues
  Tier baut und die ModData verwirft (`Mounted.lua:168-172`, ihr Kommentar).
* **Im Jar nachgelesen, stimmt:** `AnimalData.checkStages` ruft `grow(naechsteStufe)` nur, wenn die Stufe ein `nextStage` hat
  (Offset 84-123). `AnimalData.grow(String)` baut `new IsoAnimal(...)` (Offset 58-92), uebernimmt Alter, Stufe, Hunger, Durst,
  Stress, Gene, Name, Geschlecht, AnimalID, Unverwundbarkeit, loescht das alte Tier und setzt das neue in die Welt (Offset 99-545);
  ein ModData-Zugriff kommt in der ganzen Methode nicht vor.
* **Was die Engine OHNE Stufenwechsel kann:** `AnimalData.growUp` laeuft je Alterstag (`AnimalData.update` Offset 106-112) und setzt
  `Groesse = min(maxSize, Groesse + (maxSize - minSize) / ageToGrow * Gesundheit)` (`growUp` Offset 40-130), Gewicht genauso.
  Ein gesundes Tier waechst also linear von minSize bis maxSize, ein krankes langsamer, ohne neues Objekt -- solange die Stufe
  kein `nextStage` hat.

**Fuer den Baeren:** EINE Stufe `bear` mit kleinem minSize (Baby), grossem maxSize, langem `ageToGrow`, kein nextStage -- dann
waechst er stetig von selbst, und Hunger bremst es (Gesundheit). Staerke, Leben, Schaden koennen wir aus `getData():getSize()`
ableiten. Heute steht in NCBearTest `minSize = maxSize = 1.0` (`NPCCrew-Nebenprojekte/baer/spiel/bau_lebend.md`). Ungeprueft:
ob Laufen und Kollision mitskalieren (tier_spez.md Zeile 187: "Das Bild folgt, der Weg nicht"), und ob `setSizeForced` mit
growUp gegeneinander laeuft (bau_lebend.md letzter Punkt: growUp klemmt beim naechsten Alterstag). Idee "Wachstum pausieren": Companion Dogs.

## 8. Level, Werte, Gene

* Fuenf Faehigkeiten: Spuersinn, Kampf, Gehorsam, Jagd, Hueten, je bis Stufe 10 (`Skills.lua:4-6`). XP-Bedarf
  20 x L x (L+1) / 2 (Stufe 10 = 1100 XP, `Lineage.lua:165-196`), Sandbox `SkillXPRate` (Vorgabe 0,5).
  Kampf-XP: 1 je Biss, 5 je Toetung (`Needs.lua:258-259`, `Strike.lua:119-123`). Rassen haben XP-Faktoren (`Skills.lua:16-120`).
* Wirkung je Level: Schaden (Kurve min..max je Rasse, `Lineage.lua:298-312`), Umwerfen, weniger Wunden, weniger Kampfstress,
  groessere Warn- und Spuerradien (`Lineage.lua:317-430`). Gehorsam schaltet Tricks frei (Stufe 1/3/5/10, mod.info).
* Gene je Rasse (Staerke, Aggressivitaet, Widerstand, Stress) mit Bereich, bei Zucht gemischt (`Lineage.lua:112-160`).
* **Besitzer-Boni** (z. B. mehr XP fuer bestimmte Perks): ausdruecklich NICHT ueber `addXpMultiplier`, weil die Engine den
  Faktor im Spielstand speichert und er Entlassen und Deinstallieren ueberlebt; stattdessen Extra-XP im Ereignis `AddXP`
  (`CD:shared/CompanionDogs/skills/OwnerXP.lua:4-7`). Gute Lehre fuer uns.
* **Ausdauer gibt es nicht** (kein Treffer fuer stamina/endurance in der Logik). Am naechsten: "Kampfstress" je Biss, ab einer
  Schwelle Panik (`Needs.lua:166`, `Skills.lua:450`).

**Taugt:** Level-Kurve, XP aus Kampf, Wirkung je Level. Ausdauer fuer den Baeren waere neu (z. B. Vorrat, der beim Rennen und
Kaempfen sinkt und mit Level waechst) -- dafuer gibt es bei ihnen keine Vorlage.

## 9. Sandbox-Optionen (39 Stueck, `CD:../sandbox-options.txt`)

Die fuer uns passenden: `TameThreshold` 100, `MaxCompanions` 0, `CombatEnabled` an, `DogDamageMultiplier` 1,0, `UpkeepEnabled` an,
`NeedsRateMultiplier` 1,0, `LoyaltyDecayPerDay` 12, `ProteinNeedEnabled`/`ProteinHours` 72, `SentinelEnabled` (warnt vor Zombies),
`BondingEnabled` (Streicheln gegen Langeweile), `SkillXPRate` 0,5, `DogNoiseAttractsZombies` an, `ShowNameTags` an,
`DogSpawnMultiplier` 1,0, `WildDogsInvincible` aus, `DespawnOnOwnerOffline` an, `CargoCapacityMultiplier` (Satteltasche),
`MaturityDays` 90, `TripOverDogs` an, `Death` aus, dazu zwoelf zum Tierarzt-System (Krankheitschancen). Texte in
`CD:shared/Translate/EN/Sandbox.json`. Zusaetzlich koennen Admins Konstanten im Spiel nachstellen (`tuningset`, `Commands.lua:2231`,
gespeichert in globalem ModData `:2183`).

## 10. Speicherung

* Der lebende Hund ist ein Tier der Engine und wird von ihr gespeichert (Tierdateien `apop`), seine Werte stehen in seinem ModData.
* Zusaetzlich ein **Zwinger-Abbild** je Hund: im ModData des Spielers und gespiegelt in globalem ModData, das den Charakter
  ueberlebt (`Kennel.lua:4-15` Feldliste, `CD:server/CompanionDogs_Kennel.lua:228-275`). Daraus bauen sie einen verlorenen Hund
  neu (Rueckruf, `Kennel.lua:6-31`; Wiedererkennung an der AnimalID, nie raten, `Kennel.lua:49-90`).
* **Fahrzeug und Logout:** der Hund wird "verstaut" (Datensatz schreiben, Tier entfernen) und beim Aussteigen/Einloggen neu gebaut
  (`Stash.lua:8-35`, `:40-121`, `:194-200`; Sandbox `DespawnOnOwnerOffline`). DogPack setzt Hunde stattdessen auf Sitze
  (`PACK:sandbox-options.txt` `DogsUseVehicleSeats`).
* Besitzer-Schluessel: im MP der Benutzername, im SP die Steam-ID (`CD:shared/CompanionDogs/core/State.lua:48-56`). Damit verliert
  man den Hund im SP nicht, wenn die Spielfigur stirbt (die Falle, die NPC Crew in v3.9.66 hatte).
* Wie schwer das ist, zeigt ihr Takt: neun Aufraeumer und Retter laufen dauernd mit -- Waisen adoptieren, Besitz reparieren,
  geteilte Identitaet, Zwinger zurueckholen, verstaute/getragene/Anhaenger-Hunde retten, Klone entfernen (`Companion.lua:1033-1041`).
* Warnung aus ihrem Code, deckt sich mit Kevins Baer-Pruefung: ohne die Mod wirft `IsoAnimal.load` bei der unbekannten Art,
  die ganze Tierzelle laedt nicht und das Spiel bevoelkert sie neu (`CD:server/systems/CompanionDogs_ApopSweep.lua:1-3`;
  `NPCCrew-Nebenprojekte/baer/spiel/bau_lebend.md`, Fund 1).

**Taugt:** Abbild im Spieler- und globalen ModData, Neubau aus Datensatz mit positiver Wiedererkennung, Verstauen im Auto. Der
Baer passt nicht in ein Inventar (`canBePicked false` bei Kevin), Tragen faellt weg.

## 11. Mehrspieler

* Server rechnet KI und Wege der Tiere. Ihr Kommentar: ein Client kann fuer ein Tier keine Wegsuche (A*) anfordern
  (`CD:server/systems/CompanionDogs_NetAuthority.lua:5-6`).
* **Positionshoheit:** fuer glattes Folgen leiht der Server dem Client des Besitzers die Position; der Client schiebt den Hund
  mit `setX/setY` in gerader Linie und gibt bei jedem Hindernis zurueck (Wand, Tuer, Fenster, Treppe ... `NetAuthority.lua:15-34`;
  Client `CD:client/CompanionDogs_NetAuthority.lua:3-4`, `:158-160`). Rund 800 Zeilen nur dafuer.
* **Schaden am Zombie auf dem dedizierten Server:** ein Teil-`setHealth` des Servers haelt nicht, weil der Client mit der
  Zombie-Hoheit dessen Leben alle 200 ms neu schickt; sie fuehren deshalb ein eigenes Schadensbuch je Zombie und lassen den
  Todesstoss den Client des Besitzers ausfuehren, mit Bestaetigung (`Strike.lua:54-56`, `:72-97`, `killzombieack` `Commands.lua:2312`).
* Umwerfen: Server schickt Koordinaten an alle, jeder Client wirft den naechsten Zombie in 1,5 Kacheln um (`Anim.lua:207-212`,
  `Client.lua` `knockdownZombie`). Toene nur an Spieler in Reichweite (`Registry.lua:509-522`).

**Fuer den Baeren:** derselbe Aufbau (Gehirn auf Server/SP, Clients bitten, Besitz pruefen) ist der natuerliche Weg -- anders als
bei den Zombie-Begleitern von NPC Crew. Die Positionshoheit ist teuer; erst ohne sie bauen und messen, ob das Folgen im MP reicht.
Das Schadensbuch fuer Zombies brauchen wir genauso, sobald der Baer Zombies verletzt (Schaden vom Server haelt nicht).

## 12. Oberflaeche

Statusfenster mit Reitern Status, Gesundheit, Befehle, Faehigkeiten (`CD:client/CompanionDogs_StatusUI.lua:90-95`), Zwinger-Liste
aller Hunde (`_KennelUI.lua`), Streuner-Suche (`_StrayScanUI.lua`), Namensschild (`_NameTags.lua`), Kartenmarke (`_MapMarker.lua`),
eigene Moodles fuer Hund und Besitzer (Trauer, Gut ausgeruht, Rassen-Bonus; `_Moodles.lua`), Tasten in eigener Datei
(`_Settings.lua:116/:150`), Rechtsklick: Fuettern, Traenken, Streicheln, Untersuchen, Umbenennen, Freilassen, Wachstum pausieren,
Satteltasche, Wunde versorgen.

## 13. DogPack (Zusatz)

Mehrere Hunde gleichzeitig aktiv (Vorgabe 3), Rollen Beschuetzer/Angreifer/Spaeher/Traeger, Formationen, "Zusammenhalt",
Abzug bei Schaden und Beduerfnissen je weiterem Hund, Sitzplaetze im Auto (`PACK:sandbox-options.txt`, `PACK:lua/shared/CompanionDogsPack_Core.lua:10-18`).
Fuer "ein Baer je Spieler" nicht noetig.

---

## Ideen fuer den Baeren (Herkunft jeweils Companion Dogs)

1. Junges finden und anfuettern bis Vertrauen voll; Sandbox-Schwelle. (TameThreshold)
2. Ein Baer je Spieler als Sandbox-Zahl. (MaxCompanions)
3. Wachstum pausieren per Rechtsklick, wer ein Junges behalten will. (Pause growth)
4. Schaden-Faktor als Sandbox. (DogDamageMultiplier)
5. Rueckzug bei wenig Leben; bei "Unsterblich" stattdessen hinlegen. (RETREAT_HEALTH_FRAC, Death-Schalter)
6. Umwerfen-Chance waechst mit Level -- beim Baeren auch mit Groesse. (knockdownChance)
7. Nicht geladene Zeit verbraucht keinen Hunger. (wasInPlay)
8. Napf und Vanilla-Trog, er geht selbst hin. (Dish/Trough)
9. Warnt vor Zombies (Brummen), Laerm lockt Zombies an (Sandbox). (Sentinel, DogNoiseAttractsZombies)
10. Streicheln senkt Langeweile, Trauer-Moodle beim Tod. (Bonding, Grief)
11. Satteltasche: ein grosser Baer traegt Gepaeck. (Saddlebag)
12. Verstauen bei Logout und im Auto, Neubau beim Wiederkommen. (Stash, DespawnOnOwnerOffline)
13. Besitzer-Boni nur ueber AddXP, nie ueber addXpMultiplier. (OwnerXP.lua:4-7)

## Grenzen und Warnungen

* Kein Kampfschaden, kein Downed, kein stetiges Wachsen, keine Ausdauer -- genau das muessen wir selbst bauen.
* Ihr Stufenwechsel ist ein Neubau des Tiers (neue onlineID); jeder Neubau ist eine Kopie/Verlust-Gefahr, ihre neun Retter zeigen es.
  Der Baer sollte deshalb nie die Stufe wechseln (eine Stufe, growUp).
* MP kostet viel: Positionshoheit, Schadensbuch, Rundruf-Umwerfen. Alles im SP UND MP pruefen (CLAUDE.md Regel 7).
* Ihr Animationsweg haengt an der Vanilla-Gruppe `raccoon`; der Baer an `buck` -- eigene Knoten dort sind ungespielt.
* Companion Dogs ist ALPHA und fuer 42.19 gebaut; Zeilennummern koennen sich mit jedem Update verschieben.

## Ungeprueft

* Ob Bandits-NPCs auf Tiere schiessen/schlagen (dann ist "stirbt gegen Bandits" ein echtes Ereignis).
* Ob `isInvincible` gespeichert wird (ihre Aussage: nein, `Mounted.lua:89`).
* Skala der Tier-Gesundheit (Companion Dogs merkt nur den Startwert als `maxHealth`, `Kennel.lua:250`); ob "mehr HP" ueber den
  Engine-Wert geht oder ein eigenes Lebenskonto braucht.
* Ob Kollision und Laufweg bei groesserem `size` mitwachsen.

Statisch gelesen, nicht gespielt.
