# Was wir von Knox Wildlife und Animals Attack Zombies lernen (Abgleich, 08.11.2026)

**Fuer Kevin (statisch gelesen, nicht gespielt):**
1. Ja, beide lassen Tiere Zombies angreifen: eigene Knoten im Vanilla-Idle-Ordner, eigener Lua-Takt, Schaden per `setHealth` am Zombie. Zurueck wehrt sich in KEINER der beiden Mods ein Zombie. Das bauen wir selbst (`angriff_*.md`).
2. Knox-Baeren jagen ausserdem Spieler (Gruppe `pig` mit Vanilla-Angriffszustand). Genau das nehmen wir nicht: unser Baer bleibt `buck`, der kann keinen Spieler angreifen.
3. Der wichtigste Fund ist eine Falle in unserem Kampf-Bau: `knockDown` allein wirft einen Zombie laut Spieldaten nicht um, er taumelt nur. Damit kaeme auch der Biss am Boden nie. Die Loesung ist eine Zeile mehr (Position "FRONT"), die Idee stammt von AAZ.
4. Fuer den Mehrspieler (B9) zeigen beide einen einfachen Weg: Der Server entscheidet und schickt den neuen Lebenswert an alle. Jeder Client nimmt den kleineren Wert, die anderen sehen nur das Taumeln.
5. Anders als beide: Ziele nur Zombies und feindliche Banditen (die zwei kennen keine Crew), Uhr in Spielzeit statt Wanduhr, keine Aufrufe ohne Fundstelle in Vanilla oder Bandits.
6. Zusammen mit unserem Baeren laufen beide ohne Namenskonflikt. Fuer NPC Crew selbst gibt es zwei Nebenwirkungen: AAZ-Bullen greifen Crew-Leute an, und Knox-Kojoten fressen Banditenleichen samt Beute. Das liegt an deren Mods, dein Wort ist noetig, ob wir einen Hinweis bauen.
7. Lizenz: Knox ist MIT (Code), Modelle CC BY, Toene CC0/CC BY. AAZ hat gar keine Lizenz, also alle Rechte beim Autor. Wir uebernehmen nichts davon, nur Ideen mit Herkunft.

---

## Selbst nachgeprueft (Stichproben, alle halten)

| Aussage der Leser | eigene Probe |
|---|---|
| `IsoZombie.knockDown` setzt `playerAttackPosition` auf "BEHIND" bzw. nil | javap `IsoZombie.knockDown` Offset 16-28 (`_arbeit/baer_spionage/jar/IsoZombie.txt:13123-13147`) |
| Umfall-Uebergaenge fragen nur "FRONT"/"BACK" | `media/actiongroups/zombie/idle/to_staggerback-knockeddown.xml` (FRONT), `..-fromBehind.xml` (BACK), `idle/to_staggerback-knockeddown-ragdoll.xml` (FRONT/BACK + `usePhysicHitReaction`); in `staggerback/`: FRONT/BACK, Ragdoll nur mit `usePhysicHitReaction` + `canRagdoll`, sonst `to_idle.xml`. Die Variablenbeschreibung im Jar nennt die Werte FRONT, BEHIND, LEFT, RIGHT, also nie "BACK" (`IsoZombie.txt:15580`) |
| AAZ dreht den Zombie und setzt FRONT | `AnimalsAttackZombies.lua:219-228` (dort Kommentar "BACK, which vanilla never sets") |
| AAZ: Server schickt Treffer an alle, Besitzer zieht ab | `AnimalsAttackZombies_Attack.lua:298-323`, `AnimalsAttackZombies_Client.lua:43-55` |
| Knox: Server setzt, Clients `setHealth(min(alt, neu))` | `KW/ZombieCombat.lua:56-60, 176-190` |
| Knox: Treffer 713 ms nach Start per `getTimestampMs`, Kontakt neu geprueft inkl. Wand/Tuer/Fenster | `ZombieCombat.lua:18-24, 78, 130-133` |
| Kein Zombie verletzt Tiere (AAZ sagt es selbst) | `Translate/EN/Sandbox.json:50` |
| AAZ kennt keine Banditen/Crew | grep `Bandit\|brain\|getVariableBoolean` in AAZ-Lua: 0 Treffer |
| Knox-Kojoten fressen Leichen mit `isZombie()` samt Inhalt, Vorgabe AN | `sandbox-options.txt:2-4`, `KW/Predators.lua:69-88` |
| Lizenzen | Knox `LICENSE.txt:1-25`; AAZ `mod.info` (kein Lizenzfeld, keine Lizenzdatei im Download) |
| NEU: Tier am Client per Netz-Id finden | Global `getAnimal(id)`: Vanilla `server/ClientCommands.lua:767` u. a., Jar `LuaManager$GlobalObject.getAnimal` Offset 0-8 (nur `AnimalInstanceManager.get`, kein Server-Riegel); am Client benutzt es AAZ (`AnimalsAttackZombies_Client.lua:34, 39`). Am Client ungeprueft |

---

## Aenderungen fuer unseren Kampf (Lauf baer-kampf, B4/B5, B9)

**K1 Umwerfen reparieren (Lauf baer-kampf, vor Kevins Test).** Heute ruft `NCBearFight` `z:knockDown(vonHinten)`
(`kampf_lua.md`). Damit faellt der Zombie nur bei Ragdoll-Treffern, sonst taumelt er (Stichprobe oben). Dann gibt es auch keinen
**Biss** (der verlangt "liegt"), und die Attrappe ist an dieser Stelle zu gutglaeubig. Neu: nach `knockDown` noch
`z:faceThisObject(baer)` (am Zombie Bandits-belegt, `BanditUpdate.lua:1905` laut `angriff_zombie.md`) und
`z:setPlayerAttackPosition("FRONT")` (Bandits `ZAPush.lua:41-45` laut `kampf_spez.md` 3.1, Bandits hier nicht selbst gelesen).
Das Argument `vonHinten` faellt weg. In der Attrappe gilt "liegt" nur noch mit FRONT. Idee: AAZ `AnimalsAttackZombies.lua:219-228`.
AAZ nutzt `setForwardDirection`, das hat in Vanilla-Lua 0 Treffer, wir nehmen es nicht. Ob der Zombie danach wieder aufsteht,
entscheidet Kevins Test.

**K2 Halbstark: Taumeln statt Umwerfen (B4).** `knockDown` OHNE FRONT gibt laut XML genau das Taumeln (staggerback -> idle),
ausser wenn die Ragdoll-Reaktion aktiv ist. Ungeprueft: ob `bKnockedDown` danach stehen bleibt und ein spaeterer FRONT-Treffer
ihn sofort umwirft. Rueckfall: nur Schaden, Blut und Ton. Idee: AAZ `AnimalsAttackZombies.lua:229-235` (Stagger mit Kraft 0,6,
unbelegte Setter, nicht uebernommen).

**K3 Treffer nicht durch Fenster und Zaun (Lauf baer-kampf).** Im Treffermoment pruefen wir heute Ziel, Abstand, Kegel und `CanSee`.
Neu fuer Haupt- und Nebenziele: Kachel fuer Kachel von Baer zu Ziel `sq:isBlockedTo(next)`, dazu `isWindowTo`/`isWallTo`
(Vanilla-belegt, Zaehlung in `spion_knox.md` (8)). Bei einer Reichweite bis 2 sind das hoechstens drei Schritte. Ob `CanSee` durch
Fenster sieht, ist ungeprueft, mit der Kantenfrage ist es egal. Idee: Knox `ZombieCombat.lua:18-24`, AAZ `..._Attack.lua:87-132`.

**K4 Ziel um den Besitzer, Leine ab Besitzer (B4).** Heute: Suche 10 Kacheln um den BAEREN, Leine 25 ab Kampfbeginn. Fuer einen
Begleiter rennt er so Zombies hinterher, waehrend der Spieler weitergeht. Neu: ein Ziel zaehlt nur in Reichweite eines bewachten
Punkts (Folgen: der Besitzer, Bewachen: der Punkt aus PLAN 8 mit 6 Kacheln), losgelassen wird ab Reichweite + 6. Das Drohen bricht
ab, wenn das Ziel ueber 125 % davon weicht. Idee: AAZ `..._Threat.lua:183-218` (bewachte Punkte), `..._Attack.lua:390-402`.

**K5 Rueckzug bei Horde und Wunden (B4/B5a).** Kein neuer Kampf und Abbruch bei: unter 40 % Leben, oder ab N Zombies in 8 Kacheln
(Halbstark 3 wie PLAN, Erwachsen Vorschlag 6), N plus 1 je Verbuendetem in 8 Kacheln (Besitzer, Crew). Flucht per `fleeTo` zu einer
Kachel beim Besitzer, nicht mit `forceFleeFromChr` (Vanilla 0 Treffer). Idee: AAZ `..._Threat.lua:251-271, 96-99, 339-352`.

**K6 Ende beim Verschwinden und beim Speichern (Lauf baer-kampf).** Ist der Baer nicht mehr in der Welt (Anhaenger, Haken, entladen;
`isExistInTheWorld()`, belegt `ISAnimalUI.lua:15`), wird nur der Eintrag geloescht, es gibt keinen Aufruf mehr am Tier. Danach findet
die AnimalID ihn wieder (PLAN 7). Vor `OnSave` loest der Einzelspieler laufende Kaempfe (`setBlockMovement(false)`, `NCBearAct`
loeschen). Idee: AAZ `..._Attack.lua:257-268`, Knox `ZombieCombat.lua:33-43, 156-160`. Pruefen, ob der Bau das schon tut.

**K7 Sichtbarer Treffer am Baeren (B5a).** Ein eigener kurzer Zuck-Clip als Idle-Knoten (`NCBearAct = "hurt"`, rund 0,5 s, Ton
`NCBear_Pain`), nie ueber `animal:Hit` (die buck-Reaktion haelt rund 6 s still, `tier_spez.md` 3.3). Idee: Knox' eigener kurzer
Hit-Clip je Art (`spion_knox.md` (2)). Den Clip baut unser Animator.

**K8 Mehrspieler (B9), statt Schadensbuch:**
- Der Server waehlt Ziel und Treffer und schickt `{zombie onlineId, neues Leben, Umwerfen ja/nein, Ort des Baeren}` an alle. Jeder
  Client setzt `setHealth(min(alt, neu))` und spielt das Bild. Das ist idempotent und haelt auch beim Hoheitswechsel. AAZ laesst
  dagegen den Besitzer den Schaden abziehen, das zaehlt bei einem Wechsel doppelt oder gar nicht. Das Leben reist mit dem
  naechsten Paket des Besitzers zum Server (CLAUDE.md v3.11.2). Ideen: Knox `ZombieCombat.lua:176-190`, AAZ Client-Kommentar `:11-16`.
- Tod im MP: Leben 0 plus FRONT-Umwerfen, `ZombieOnGroundState` ruft `die()` (Jar laut `spion_aaz.md` 2). Das ist eine
  Alternative zu `Kill(nil)` auf einem fremden Client (`kampf_spez.md` 3.5 ungeprueft). Idee: AAZ `AnimalsAttackZombies.lua:244-246`.
- Tier am Client: `getAnimal(onlineId)` (Stichprobe oben). Das schliesst die offene Stelle in `kampf_lua.md` MP.
- `NCBearAct` setzt jeder Client an seiner Kopie, auf Serverbefehl, mit Verfall (Knox 1,5 s, `ZombieCombat.lua:172`).
- Den Treffer auf dem Server legt eine Spielzeit-Uhr fest (Summe `getMultiplier`, belegt), weil der Server keine
  Anim-Ereignisse spielt (`ISPetAnimal.lua:83`). Im SP bleibt `NCBearHit`. Idee: AAZ `..._Attack.lua:404-418`.
- Die Hoheit fragen wir nur ueber `getVariableBoolean("bClient")` ab, nie ueber `isRemoteZombie`/`getOwnerPlayer`.

## Fuer den Begleiter-Plan

- **Artname:** Knox nennt seine Tiere `kw<Art>Male/Female/Young`. Mit `bear` gibt es also schon heute keine Kollision
  (PLAN Frage 8). `ncbear` bleibt trotzdem, wegen der Copy-Paste-Regel (`ENTSCHEIDUNGEN.md`).
- **Bestaetigt, keine Aenderung:** eigene Knoten in einem Vanilla-AnimSet-Ordner mit eigener Bedingung und Clips im Netz
  eingebettet (Knox `AnimSets/pig/*`, `CHANGELOG-0.1.4.txt`; deckt sich mit `tier_spez.md` 2.6 und `kampf_spez.md` 1).
- **Test-Hinweis:** Die Meldungen "SkeletonBone not resolved" bei Tierknochen sind harmlos (Knox `README.txt:133-140`). Nicht jagen.
- **Wachstum:** Knox nutzt den Stufenwechsel der Engine. Wir bleiben beim eigenen Zaehler, sonst setzt die Tierzone die Groesse
  zurueck (`KRITIK.md` K1).
- **Anrennen mit `getBehavior():goAttack(zombie)`** (AAZ `..._Attack.lua:376-384`, folgt einem laufenden Ziel): Vanilla ruft es nur
  mit einem Spieler als Ziel und nur im Debug (`ISAnimalContextMenu.lua:622`, `ClientCommands.lua:1050`). Nur mit Probe, `fleeTo`
  bleibt die Vorgabe.
- **NPC Crew (eigene Version, braucht dein Wort):** Wer AAZ hat, bei dem greifen Bullen, Eber, Widder, Hahn, Truthahn und
  Muttertiere Crew und freundliche Banditen an, und Kuehe ohne Kalb fliehen vor dem Tierpfleger. Bei Knox mit `AggressiveToZombies`
  (Vorgabe aus) beissen Knox-Tiere die Crew, und Kojoten (Vorgabe an) fressen Zombie- und Banditenleichen samt Beute. Das betrifft
  Leichen entsorgen und Pluendern. Moegliche Gegenmittel: ein Hinweis in der Beschreibung oder ein eigener Riegel, nie an den
  fremden Mods.

## Was wir ausdruecklich NICHT uebernehmen

- Keine Datei, keinen Code, keinen Clip, kein Netz, keinen Ton, keine Textur. Das gilt auch fuer Knox, obwohl MIT es erlauben
  wuerde (Kevins Regel). Ideen tragen ihre Herkunft im Changelog und Kommentar.
- Gruppe `pig` oder irgendeinen Vanilla-Angriffszustand: der trifft jeden Spieler als `atkTarget` (Knox `Predators.lua:132-163`).
- Doppelnamen-Aliase im Netz (Knox): wir nennen die Clips im eigenen Netz ohnehin wie `buck` (`DeerStag_*`).
- `z:hitConsequences(...)` (Knox): unbelegt, und die Engine-Faktoren machen den Schaden unplanbar (`kampf_spez.md` 3.3).
- Wanduhr-Timer `getTimestampMs` (Knox) und `getTimeDelta` (AAZ, unbelegt). Wir nehmen Spielzeit-Summen (CLAUDE.md v3.9.43).
- Unbelegte Aufrufe aus beiden Mods: `pathToCharacter` am Tier, `forceFleeFromChr`, `resetBehaviorAction`,
  `sendExtraUpdateToClients`, `setForwardDirection`, `setStaggerBack`, `setHitReaction`, `getHitDir`, `isBeingGrappled`,
  `isRemoteZombie`, `getOwnerPlayer`, `getCell():getAnimals()` (Vanilla kennt es nur an Kachel und Fahrzeug). Jeder davon braeuchte
  dein Wort und einen Jar-Beleg.
- "Jeder IsoZombie ist ein Ziel" (beide): wir behalten die harte Regel aus `kampf_spez.md` 3.4.
- Je Bild ueber alle Tiere der Zelle laufen (Knox `AnimationCompatibility.lua:13-22`, `ZombieCombat.lua:90-97`). Wir suchen
  alle 5 s und merken uns hoechstens 8.
- Wilde Baeren, Migration, Gene als Schadensfaktor, Gegenangriff auf Spieler (Knox `AnimationCompatibility.lua:23-44`).

Statisch gelesen, nicht gespielt. Nichts aus beiden Mods kopiert.
