# Animals Attack Zombies (AAZ) - wie es gebaut ist, was der Baer davon lernt (08.11.2026)

Workshop 3808643352, `mods/AnimalsAttackZombies/42` (Autor `Tien`, `modversion=2.0`, mod.info:3/:13). Alle 16 Dateien gelesen:
4 Lua (1.231 Zeilen), 1 Definitions-Datei, 5 AnimSet-Knoten, `sandbox-options.txt` (71 Optionen), `Translate/EN/Sandbox.json`,
mod.info, drei 80x80-Bilder. **NUR GELESEN, nichts uebernommen.** Engine-Aussagen gegen das Jar 42.21 (javap, Auszuege in
`_arbeit/baer_spionage/jar/*.txt`) und Vanilla `media/` geprueft, wo es unten steht; sonst "AAZ-Kommentar, ungeprueft".
**Statisch gelesen, nicht gespielt.**

Kuerzel: `Sh` = `lua/shared/AnimalsAttackZombies.lua`, `Th` = `lua/server/AnimalsAttackZombies_Threat.lua`,
`At` = `lua/server/AnimalsAttackZombies_Attack.lua`, `Cl` = `lua/client/AnimalsAttackZombies_Client.lua`,
`Df` = `lua/shared/Definitions/animal/AnimalsAttackZombies_GeneralDefinitions.lua`, `Sb` = `Translate/EN/Sandbox.json`.

**Lizenz:** keine. mod.info hat kein Lizenzfeld, es liegt kein README/LICENSE bei (die Kommentare `Sh`:5-6/:29 nennen
`README.md`, `workshop.txt`, `docs/*.md` -- im Download nicht enthalten). Also gilt: alle Rechte beim Autor. Wir beschreiben nur
Mechanik und Ideen mit Herkunft. Steam-Seite nicht gelesen (kein Web in diesem Lauf).

---

## Kurz

* **Gegenwehr loesen sie NICHT.** Ihr eigener Text: Zombies verletzen Tiere nie (`Sb`:50, Tooltip RetreatHealth). Das bleibt
  bei uns offen (`angriff_zombie.md`, Weg 1/2).
* **Was sie loesen, ist unser offener B9-Punkt: Schaden am Zombie im Mehrspieler.** Server entscheidet, schickt jeden Treffer an
  alle Clients, nur der Client mit Hoheit ueber den Zombie setzt das Leben, die anderen spielen nur die Reaktion (`At`:298-323,
  `Cl`:43-55). Kein Schadensbuch noetig.
* **Ein Fund fuer unseren Kampf-Bau:** `zombie:knockDown()` setzt die Position "BEHIND" oder nil, die Umfall-Uebergaenge fragen
  aber nur "FRONT"/"BACK" -- ohne Ragdoll faellt er vermutlich nicht, er taumelt nur (XML + Jar, unten 2). AAZ dreht den Zombie
  dafuer zum Tier und setzt "FRONT" (`Sh`:219-228).
* **Angriff:** eigener Lua-Kampf mit vier Phasen (warnen, anrennen, schlagen, Pause), eigene Strike-Knoten im Vanilla-`idle`
  der Tierart, Treffer nach Uhr statt nach Anim-Ereignis (MP-tauglich).
* **Vertraeglichkeit mit dem Baeren: kein Konflikt.** Mit NPC Crew aber einer: AAZ-Bullen greifen Crew-Leute und freundliche
  Banditen an, Kuehe ohne Kalb fliehen vor dem Tierpfleger (unten 8).

---

## 1. Wie ein Tier einen Zombie angreift

| Teil | Wie | Fundstelle |
|---|---|---|
| Wer kaempft | nur 7 Tierarten: bull, boar, ram, cockerel, gobblers (Hueter der Herde), sow und cow (nur mit eigenem Jungtier im Umkreis 15) | `Sh`:86-102, `Th`:147-178 |
| Keine eigene Flucht | `fleeZombies = false` fuer genau diese 7 | `Df`:7-13 (Engine: `BaseAnimalBehavior.spotted` ignoriert Zombies dann ganz, CLAUDE.md v3.9.58) |
| Takt | Suche alle 0,5 s Spielanimationszeit, mindestens 100 ms echte Zeit (Zeitraffer); laufende Kaempfe je Bild | `Th`:69-70, :378-391; `At`:452-486 |
| Uhr | Summe aus `getGameTime():getTimeDelta()` | `At`:72, :453-454 (in Vanilla-Lua 0 Aufrufe, unbelegt) |
| Kandidaten | alle Tiere der Zelle (`cell:getAnimals()`), alle Zombies der Zelle (`getZombieList()`), gleiche Ebene | `Th`:103-144 |
| Ziel | der zum Tier naechste Zombie, der in Reichweite eines bewachten Punkts steht (Tier selbst, Herdengenossen 8 Kacheln, Jungtiere) **und** zu dem eine gerade Linie frei ist | `Th`:183-218 |
| Freie Linie | Kachel fuer Kachel entlang der Linie `square:isBlockedTo(next)` (Wand, Zaun, Tor, Tuer, Fenster), max. 64 Schritte | `At`:87-132 (`isBlockedTo` Vanilla-belegt, z. B. `client/Foraging/ISBaseIcon.lua:258`) |
| Kein Ziel | tot, scheintot, ohne Kachel, gezogene Leiche (`isReanimatedForGrappleOnly`, `isBeingGrappled`), aufgegeben | `At`:137-140, `Th`:195 |
| Reichweite | EngageRange 6 x Brunft-Faktor x Rasse x Aggressions-Gen (0,75..1,375) | `Th`:82-94 |
| Zoegern | je Suche Wuerfel; Chance steigt mit der Naehe zum Quadrat, mal Temperament der Art, Gen und Sandbox; ganz nah immer | `Th`:221-236; solange: Tier dreht sich zum Zombie (`Th`:312-316) |
| Warnen | stehen bleiben, Bewegung sperren, Blick, Stress-Ruf (`playBreedSound("stressed")`), 0,3-3 s je Art; Zombie in Reichweite = sofort schlagen; Zombie ueber 125 % weg = loslassen | `At`:204-221, :390-402, `Sh`:166-168 |
| Anrennen | `getBehavior():goAttack(zombie)` (laeuft dem Ziel hinterher), vorher Sperre loesen und `resetBehaviorAction`; alle 0,5 s neu; rennt ab 2 Kacheln (`setVariable("animalRunning", ...)`); fuehrt der Weg woanders hin (Vanilla schickt es zum Fressen), anhalten und neu | `At`:344-387 |
| Schlagen | anhalten, sperren, Blick, `setVariable("idleAction", "aazStrike")`; Knoten im `idle` der Art spielt den VANILLA-Angriffsclip; der Treffer faellt nach Uhr beim Vanilla-AttackConnect-Zeitpunkt; danach 0,3-1,0 s Pause, gesperrt | `At`:325-339, :404-426, `Sh`:55-65, AnimSets `cow/idle/...Strike.xml`:3-12 |
| Ende | Zombie tot, ueber Leine weg (Reichweite + 6), andere Ebene, 6 s ohne 0,5 Kachel Fortschritt, 60 s Kampf; aufgegebene Zombies 20 s gemieden | `At`:355-368, :434-450, :261-281 |
| Tier weg | tot, Anhaenger, Haken, getragen: Sperre und Strike trotzdem loeschen, sonst steht es bis zum Vanilla-Notausgang (~3 min) starr | `At`:257-268, :428-431 |

**Warum nicht der Vanilla-Angriffszustand** (`At`:4-10, gegengelesen): `AnimalAttackState.animEvent` kennt bei
`AttackConnect` nur IsoThumpable (Offset 77), IsoAnimal (203), IsoPlayer (429) und eine Tuer (632) -- **kein IsoZombie**, also
null Schaden. `goAttack(ziel)` (`BaseAnimalBehavior.goAttack` Offset 0-17 Riegel `blockMovement`/schon FIGHTANIMAL, 64-93
FIGHTANIMAL + `stopAllMovementNow` + `pathToCharacter`) setzt nur bei einem TIER-Ziel einen Gegner (96-121); fuer einen Zombie
bleibt es beim Hinlaufen. **`goAttack` ist Vanilla-belegt** (`ISAnimalContextMenu.lua`:622, `server/ClientCommands.lua`:1050;
eine Ueberladung, Parameter IsoGameCharacter -- ein Zombie passt).

**Warum `idleAction` mit Vorsicht:** `BaseAnimalBehavior.clearIdleAction` (Offset 0-42) loescht sie nur, wenn sie mit "idle"
beginnt (darum `aazStrike`, `Sh`:54); `checkSit` loescht sie dagegen immer bei Hunger ueber 0,2 oder Leine (Offset 33-39), und
`stopAllMovementNow` laut AAZ auch (`At`:330). **Unsere eigene Variable `NCBearAct` (kampf_spez 1.4) hat das Problem nicht.**

## 2. Schaden am Zombie, Umwerfen

* **Schaden** = Grundwert der Art x (0,5 + Staerke-Gen) x DamageMultiplier (`At`:283-292). Grundwerte: Bulle 0,8, Eber 0,6,
  Kuh 0,6, Sau 0,5, Widder 0,45, Hahn 0,05, Truthahn 0,06 (`Sh`:86-102); Zombie hat rund 2 (1,8-2,1, `Sh`:78-79, deckt sich mit
  `kampf_spez.md` 5.1). Bulle toetet in etwa 3 Hieben.
* **Aufruf:** nur `zombie:setHealth(alt - schaden)` (`Sh`:247-255), nicht `Hit` (braucht Waffe und Spieler, `Sh`:243-244).
* **Toeten ohne `Kill`:** Leben 0 + Umwerfen; liegt er, findet `ZombieOnGroundState` ihn tot und ruft `die()` (`Sh`:244-246).
  Jar bestaetigt: `ZombieOnGroundState.enter` Offset 22-53 und `execute` 5-31 rufen `die()` bei `isDead()`,
  `IsoGameCharacter.isDead` Offset 0-6 = Leben <= 0.
* **Umwerfen** je Treffer mit Chance (Bulle 70 %, Widder 60, Eber 50, Kuh 40, Sau 25, Voegel 0), erster Hieb nach mindestens
  3 Kacheln Anlauf +25 % (`At`:283-292, `At`:194-202). **Sonst Taumeln** (Stagger, Trefferrichtung, Seite aus der Blickrichtung,
  Kraft 0,6). Liegt er schon, keine Reaktion (`Sh`:205-237).
* **Die FRONT-Falle (fuer uns wichtig):** `IsoZombie.knockDown(b)` setzt `playerAttackPosition` auf "BEHIND" (b wahr) oder nil
  (Jar Offset 18-28). Alle Umfall-Uebergaenge der Zombie-Aktionsgruppen vergleichen nur "FRONT" (28x) oder "BACK" (28x), keiner
  "BEHIND" (z. B. `actiongroups/zombie/idle/to_staggerback-knockeddown.xml` FRONT, `..-fromBehind.xml` BACK,
  `staggerback/to_staggerback-knockeddown.xml`). Ohne Position bleibt nur `to_staggerback` (Taumeln) und, mit Ragdoll,
  `staggerback/to_staggerback-knockeddown-ragdoll.xml` (`usePhysicHitReaction` + `canRagdoll`). **Unser Plan `z:knockDown(vonHinten)`
  (`kampf_spez.md` 3.2) wirft also womoeglich nicht um** -- im Spiel pruefen. AAZ dreht den Zombie zum Angreifer und setzt
  FRONT (`Sh`:219-228); die Setter dafuer haben in Vanilla-Lua 0 Aufrufe, Bandits nutzt `setPlayerAttackPosition`/
  `setKnockedDown`/`setHitForce` in `ZAPush.lua`:41-45 (laut `kampf_spez.md` 3.1, Bandits in diesem Lauf nicht gelesen).

## 3. Wehren sich die Zombies? Nein.

* Kein Code laesst einen Zombie ein Tier angreifen oder verletzen. `Sb`:50 sagt es ausdruecklich; RetreatHealth gilt nur fuer
  Tiere, die durch Hunger oder Autos verletzt sind.
* Der Zombie hat auch kaum Gelegenheit: jeder Treffer laesst ihn taumeln oder umfallen (2.), und die Engine nimmt ein Tier ohnehin
  nie als Ziel (`AttackState.triggerPlayerReaction` Offset 20-33, `angriff_zombie.md` 3).
* AAZ-Kommentar `At`:5-7: auf dem dedizierten Server schickt `IsoAnimal.hitConsequences` ein Tier mit `attackBack` gegen einen
  Zombie, der es TRIFFT -- das passiert nie, weil kein Zombie trifft (deckt sich mit `angriff_zombie.md` 3, Offset 187-227).

## 4. Rueckzug, Stress, verletzte Tiere

| Fall | Was | Fundstelle |
|---|---|---|
| Horde | ab 4 Zombies in 8 Kacheln Kampf abbrechen und fliehen; je Mitkaempfer derselben Gruppe in 8 Kacheln +1 | `Th`:251-271, :356-359 |
| Verletzt | unter 40 % Leben: kein Kampf, Abbruch, Flucht vor Zombies in 8 Kacheln | `Th`:96-99, :339-352 |
| Nicht-Kaempfer der 7 Arten (Art aus, Mutter ohne Junges) | fliehen wie Vanilla ab 6 Kacheln | `Th`:342-352 |
| Flucht | `getBehavior():forceFleeFromChr(zombie)`, hoechstens alle 4 s | `Th`:273-297; Jar `BaseAnimalBehavior.forceFleeFromChr` Offset 0-122: 10 Kacheln weg, `animalRunning`, `resetBehaviorAction`, `timerFleeAgain = 200`, Stress-Ruf. In Vanilla-Lua 0 Aufrufe |
| Stress | Kaempfen stresst nicht (mod.info:8): ueber `fleeZombies = false` sieht `spotted` keine Zombies | `Df`:7-13 |

## 5. Sandbox (71 Optionen, drei Seiten)

* **Grundseite (13):** je Art an/aus (7), EngageRange 6, DamageMultiplier 1,0, HerdRadius 8, YoungRadius 15, FleeRange 6,
  GeneInfluence 100 % (`sandbox-options.txt`:3-117).
* **Verhalten (19):** Hesitation, Aggression, ChargeChanceAtEdge 4 %, ChargeChanceUpClose 60 %, AlwaysChargePercent 15,
  WarningDisplay, WarningStandDown 125 %, CrowdLimit 4, CrowdRadius 8, RetreatHealth 40, ChaseDistance 6, StuckTime 6 s,
  GiveUpTime 20 s, MaxFightTime 60 s, PauseMin/Max 0,3/1,0 s, ChargeRunDistance 2, RunUpDistance 3, RunUpKnockdown 25 (:119-303).
* **Arten (39):** je Art Damage, Knockdown, Temper, WarnMin, WarnMax; RutRange 50 %; Bullen-Rasse Holstein 100/Simmental 85/Angus 75 (:305-693).
* Jede Zahl hat einen Rueckfall, falls die Option fehlt (`Sh`:109-117). Nur Englisch (`Sb`).

## 6. Mehrspieler: wer rechnet

| Was | Wo | Fundstelle |
|---|---|---|
| Suche, Ziel, Phasen, Bewegung, Wuerfel | Server bzw. Einzelspieler (`if isClient() then return end`) | `Th`:46, `At`:47; Engine: Tier-KI nur ohne `GameClient.client` (`kampf_spez.md` 3.5, `IsoAnimal.updateInternal` 23-85) |
| Strike-Knoten starten | Server setzt `idleAction`, schickt `Strike` an alle; jeder Client setzt sie an seiner Kopie | `At`:331-335, `Cl`:38-42 |
| Blickrichtung sofort | `animal:sendExtraUpdateToClients()` (sonst erst mit dem naechsten Tierpaket, laut AAZ 0,8-1 s) | `At`:188-192, `Sh`:37-39 (Methode im Jar `IsoAnimal`, Vanilla-Lua 0 Aufrufe) |
| Warnruf | Server schickt `Warn`, jeder Client spielt ihn (Tierstimmen kommen laut AAZ vom AnimalSoundState des Clients) | `At`:209-214, `Cl`:33-37 (AAZ-Aussage ungeprueft) |
| **Schaden am Zombie** | Server schickt `Hit` (Zombie-OnlineID, Ort, Schaden, Umwerfen, toedlich) an ALLE; der Client, dem der Zombie bei Ankunft gehoert, setzt Leben + Reaktion, die anderen nur die Reaktion; Zombie ohne Besitzer (`getOwnerPlayer()` nil) trifft der Server selbst | `At`:304-320, `Cl`:43-55 |
| Tod im MP | das Leben reist mit dem naechsten Paket des Besitzers zum Server, der toetet fuer alle | `Sh`:244-246, `Cl`:11-16; deckt sich mit CLAUDE.md v3.11.2 (`NetworkZombiePacker.applyZombie` 179-192) |

## 7. Was der Baer davon brauchen kann

| Idee (Herkunft AAZ) | Fuer uns | Haken |
|---|---|---|
| **Treffer-Rundruf an alle, Besitzer des Zombies setzt das Leben** (`At`:298-323, `Cl`:43-55) | loest B9 (Kampf im MP) einfacher als ein Schadensbuch; Server bleibt Richter | `isRemoteZombie` ist bei uns tabu (CLAUDE.md, 0 Lua-Belege) -> belegter Ersatz `getVariableBoolean("bClient")` (`BanditsNPC.HasAuthority`); "kein Besitzer" auf dem Server (`getOwnerPlayer`) ist unbelegt -> eigener Beleg oder Ausnahme noetig; beim Hoheitswechsel kann ein Treffer verloren gehen oder doppelt zaehlen |
| **Treffer nach Uhr statt nach Anim-Ereignis** (`At`:404-418, `Sh`:59-65) | unser `NCBearHit`-Ereignis (`kampf_spez.md` 1.5) feuert auf dem dedizierten Server nicht (der Server spielt keine Anim-Ereignisse, `ISPetAnimal.lua`:83 emuliert sie) -> fuer B9 die Uhr nehmen; im SP darf das Ereignis bleiben | Uhr ueber `getTimeDelta` ist unbelegt; belegt ist die Summe `getGameTime():getMultiplier()` (`kampf_spez.md` 1.5) |
| **FRONT-Umwerfen**: Zombie zum Baeren drehen, Position "FRONT" (`Sh`:219-228) | rettet unser Umwerfen (2.) | Setter ueber Bandits belegt (NPC Crew ok), in NCBearTest ohne Bandits nur mit Bandits-Beleg |
| **Taumeln statt Umwerfen** (`Sh`:229-235) | genau Kevins Halbstark ("wenig Schaden, wirft nicht um"), und ein taumelnder Zombie beisst nicht sofort zurueck | Setter in Vanilla-Lua unbelegt |
| **Anrennen mit `goAttack(zombie)`** (`At`:376-384) | folgt einem laufenden Zombie, `fleeTo(kachel)` (unser Plan) nicht; Vanilla-belegt | vorher Sperre loesen; "vom Kurs abgekommen" pruefen sie mit `getPathFindBehavior2():isGoalCharacter()/getTargetChar()` -- unbelegt |
| **Warnen vor dem Angriff** mit Abbruch, wenn der Zombie zurueckweicht, und Sofortschlag, wenn er heranlaeuft (`At`:390-402) | passt auf "Aufrichten + Bruellen" | - |
| **Zoegern mit Naehe zum Quadrat** (`Th`:221-236) | Baer greift nicht blind alles an; Temperament je Stufe | Balance, im Test stellen |
| **Freie Linie per `isBlockedTo` je Kante** (`At`:87-132) | kein Anrennen gegen Zaun/Hauswand (unser `CanSee` ist Sichtlinie, nicht "kommt er hin") | 64 Schritte je Pruefung, nur bei Kandidaten |
| **Aufgeben: 6 s ohne Fortschritt, 60 s Kampf, 20 s meiden, Leine** (`At`:355-368, :434-450) | kein Hin-und-her am Zaun | Merkliste mit dem Zombie-OBJEKT als Schluessel (`At`:69); Objekte werden recycelt (CLAUDE.md v3.9.35) -> harmlos, ein neuer Zombie gilt hoechstens 20 s als aufgegeben |
| **Horde: Grenze + 1 je Verbuendetem** (`Th`:251-271) | Halbstark ab 3, Erwachsen spaeter; Spieler und Crew koennten als Verbuendete zaehlen | - |
| **Ende beim Verschwinden** (Anhaenger, Haken, getragen): Sperre und Strike trotzdem loeschen (`At`:257-268) | gilt fuer unseren Baeren im Anhaenger (PLAN K5) | - |
| **Gezogene Leiche ist kein Ziel** (`At`:137-140) | `isBeingGrappled` fehlt in unserem Filter (`kampf_spez.md` 3.4) | `isBeingGrappled` in Vanilla-Lua 0 Aufrufe |
| **Bewegung sperren ueber Warnen, Schlag, Pause; frei nur zum Anrennen** (`At`:30-34, :174-184) | deckt sich mit unserem Plan | - |

**Grenzen von AAZ:** keine Gegenwehr (3.); viele Engine-Aufrufe ohne Vanilla-Beleg (`forceFleeFromChr`, `resetBehaviorAction`,
`sendExtraUpdateToClients`, `isRemoteZombie`, `getOwnerPlayer`, `getTimeDelta`, `isAnimalMoving`, `getPathTargetX`,
`isGoalCharacter`, `getTargetChar`, `setHitReaction`, `setStaggerBack`, `getHitDir`, `setForwardDirection`, `isBeingGrappled`;
grep ueber Vanilla `media/lua`) -- bei uns braucht jeder einen Beleg oder Kevins Ausnahme; kennt keine Banditen und keine Crew
(8.); nur gleiche Ebene; sucht zweimal je Sekunde ueber alle Tiere und Zombies der Zelle; ein Treffer = ein Paket an alle Clients.

## 8. Vertraeglichkeit, wenn jemand AAZ und unseren Baeren hat

* **AAZ und der Baer: kein Konflikt (statisch).** Unser Tier heisst `bear` (bald `ncbear`), Gruppe `bear` (`NCBearDefs.lua`:55,
  :88) -- nicht in der AAZ-Liste (`Sh`:86-102), also nie Kaempfer, nie Herdengenosse (`Th`:112-126). AAZ greift nur Zombies an
  (`Th`:132-144), der Baer steht nicht in der Zombieliste. AnimSets: AAZ legt `aazStrike` in `cow/pig/ram/cockerel/turkey/idle`,
  wir `NCBear_*` in `buck/idle` mit eigener Variable -- verschiedene Ordner und Namen (doppelt waere nur gleicher relativer Pfad,
  `kampf_spez.md` 1.1). Schlagen beide denselben Zombie: beide ziehen vom aktuellen Leben ab, `isDead` filtern beide.
* **AAZ und NPC Crew (wo der Baer landen soll): echter Konflikt, ungespielt.**
  1. AAZ-Bullen, -Eber, -Widder, -Haehne, -Truthaehne und Muetter halten Crew-Leute und freundliche Banditen fuer Zombies
     (IsoZombie in `getZombieList()`, kein Bandit-Filter, `At`:137-140) und greifen sie an. Schaden ueber `setHealth` geht an
     unserem Treffer-Schild vorbei (der haengt an `OnHitZombie`/`OnWeaponHitCharacter`, CLAUDE.md fuenfte Ausnahme); ob der
     Gesundheitsboden des Guardian es auffaengt: ungeprueft.
  2. Nicht-Kaempfer dieser 7 Arten (z. B. Kuh ohne Kalb) fliehen vor jedem Crew-Mitglied in 6 Kacheln (`Th`:342-352,
     `forceFleeFromChr`) -- hebt NPC Crews "Hoftiere fuerchten keine Companions" (v3.9.58, `landkarte.md`:27) fuer diese Arten auf;
     der Tierpfleger kaeme an Kuehe und Saeue schlecht heran.
  Gegenmittel liegt nur bei uns (Regel 8: fremde Mod nicht aendern) -- z. B. ein Hinweis in der Beschreibung oder ein eigener
  Riegel; erst Kevin fragen.

Statisch gelesen, nicht gespielt. Nichts aus AAZ kopiert.
