# Baer als Begleiter - Kritik am Plan

Stand 08.11.2026, PZ 42.21 (`projectzomboid.jar` vom 28.09.2026). **Statisch geprueft, nichts gespielt.** Jar mit
`javap -c -p`, Auszuege unter `_arbeit/baer_begleiter/krit/`. Vanilla-Zeilen = `media/lua`.

## Kurz

1. **Kritisch:** in einer Tierzone springt der Baer beim Wiederkommen auf Baby-Groesse zurueck (Engine-Fehler). Der Plan
   baute genau darauf (Wachsen per Engine, Trog in der Tierzone). Ausweg: eigener Wachstumszaehler, wir setzen die Groesse.
2. **Kritisch:** das Vanilla-Menue "Feed" zeigt einem Baeren kein Fleisch, keinen Fisch, keine Beeren, keinen Honig. Ausweg:
   eigener Menuepunkt, der die Vanilla-Fuetter-Aktion startet.
3. **Ernst, Mehrspieler:** jeder Client darf die Daten am Tier ueberschreiben. Besitz und Level duerfen nie allein am Tier stehen.
4. **Ernst, Aufbau:** "erst nur Einzelspieler" zwingt in B8 zum Umbau und bricht deine Regel "jede Aenderung SP und MP". Besser:
   das Gehirn von Anfang an dort, wo `not isClient()` gilt (Einzelspieler und Server), nur der Kampf bleibt bis B9 SP.
5. Dazu acht kleinere Luecken (Ausdauer beim Folgen, Flucht vor eigenen Schuessen, Diebstahl im MP, Besitzer offline ...).

Stichproben, die **stimmen**: Wachstumsformel (`AnimalData.growUp` Offset 40-130), "Animal age" aendert nur das Alter
(`getAgeGrowModifier` Offset 9-75, `update` Offset 56-77), Unsterblich blockt jedes niedrigere `setHealth`
(`IsoAnimal.setHealth` Offset 0-16) und damit auch "Kill animal" (`ISKillAnimal.lua`:57-59 ruft `setHealth(0)`), Zombie-Biss
auf ein Tier faellt aus (`AttackState.triggerPlayerReaction` Offset 20-33), NPC-Crew-Zahlen 30/45/10 %
(`client/BanditsNPCGuardian.lua`:16, :25, :32).

---

## K1 (kritisch) Tierzone setzt die Groesse auf Baby zurueck

* Kommt eine Tierzone wieder in den geladenen Bereich, ruft das Spiel `DesignationZone.loading` (Offset 0-32) ->
  `DesignationZoneAnimal.doMeta` (Offset 29-48 und 82-101) -> fuer jedes Tier `IsoAnimal.updateStatsAway`.
* `updateStatsAway` endet IMMER mit `AnimalData.init()` (Offset 192-196), auch bei 0 Stunden Abwesenheit.
* `init` ruft `initSize` (Offset 4), und `initSize` endet mit `setSize(0.1)` (Offset 72-76); `setSize` klemmt auf `minSize`
  (Offset 0-15). **Ergebnis: Groesse = minSize, also Baby, bei jedem Zurueckkommen zur Basis.**
* Bei der Kuh faellt das nicht auf (0,9 statt 1,1). Beim Baeren (0,35 -> 1,3) waere alles Wachsen weg.
* Dasselbe beim Debug-Befehl "Alter setzen" (`IsoAnimal.setAgeDebug` Offset 37). Normales Laden ist sicher
  (`IsoAnimal.load` liest die Groesse nach `init` zurueck, Offset 243 und 405).
* **Folge fuer den Plan:** "Die Stufe lesen wir aus der Groesse ab" und "in einer Tierzone zaehlt die Zeit weiter" sind falsch.
  **Ausweg:** eigener Zaehler "Wachstum 0..1" in unseren Daten; in der Definition `ageToGrow` sehr gross (Engine-Wachsen ~0);
  wir setzen die Groesse selbst mit `getData():setSizeForced(x)` (Vanilla `ButcheringUtil.lua`:569) und das Gewicht mit
  `getData():setWeight(x)` (`ButcheringUtil.lua`:566), und pruefen beides regelmaessig nach. Gewinn nebenbei: "Tage bis
  ausgewachsen" wirkt ohne Neustart, "Wachstum anhalten" ist ein Schalter, Stufe und Level-Grenze haengen am Zaehler.
* Im Spiel pruefen (Testpunkt): Baer in Tierzone, weggehen bis die Zone entladen ist, zurueck: Groesse vorher/nachher.

## K2 (kritisch) Vanilla "Feed" bietet Fleisch, Fisch, Beeren, Honig nie an

* Vorfilter `ISAnimalContextMenu.lua`:33-39: nur Tierfutter (`isAnimalFeed`), Milch oder Essen der Art `Fruits`/`Vegetables`.
  Erst danach kommt die Liste der Definition (:43, `getEatTypePossibleFromHand` = `feedByHandType` + `eatTypeTrough`).
* Arten aus `scripts/generated/items/food.txt`: Brombeere `Berry`, Honig `NoExplicit`, Lachs `Fish`, Steak `Beef`,
  Grashuepfer `Insect`, Ei `Egg`. Keines davon kommt durch.
* **Ausweg:** eigener Rechtsklick "Baer fuettern" mit eigener Liste, der die Vanilla-Aktion `ISFeedAnimalFromHand` startet
  (`isValid` fragt nur die Tasche, :5-7; `complete` ruft `feedFromHand`, :45-49 -> `AnimalData.eatItem`). Eine Typsperre habe
  ich in `eatItem` nicht gesehen; ob Fleisch den Hunger richtig senkt: **ungeprueft**.
* Fundstelle im Plan berichtigt: die Wasser-Schwelle 0,1 steht in `ISAnimalContextMenu.lua`:300 (Zeile 465 ist das Menue selbst).

## K3 (ernst, MP) Jeder Client kann die Daten am Tier ueberschreiben

* `animal:transmitModData()` (Vanilla `ButcheringUtil.lua`:582) schickt `ObjectModDataPacket`. Das Paket verlangt nur
  `LoginOnServer` (javap -v, PacketSetting), und `parse` laedt die mitgeschickte Tabelle in die ModData des Tiers (Offset 51-75,
  Tiere ausdruecklich behandelt, Offset 148-155). `processServer` reicht nur weiter (Offset 0-28), keine Pruefung.
* Folge: ein veraenderter Client schreibt sich Besitz oder Level 10; ein ehrlicher Client mit alter Kopie ueberschreibt den
  Server. Gleiche Lehre wie NPC Crew v3.7.53 (jeder Empfaenger prueft den Besitz).
* **Regel fuer den Bau:** Besitz, Level, XP, Wachstum stehen im **globalen Register des Servers** (Schluessel `getAnimalID()`),
  die ModData am Tier ist nur ein Spiegel fuer die Anzeige. Unser Client ruft `transmitModData` am Baeren nie. Der Server
  liest seine Werte nie aus der ModData des Tiers zurueck, ausser beim ersten Anlegen.

## K4 (ernst) Aufbau: "erst nur Einzelspieler" ist teurer als noetig

* Bewegungsbefehle am Tier wirken nur im Einzelspieler und auf dem Server (`kampf_spez.md`:173-174). Companion Dogs laesst sein
  ganzes Gehirn unter `if not isClient()` laufen, also in beiden Faellen gleich (`recherche_dogs.md` Abschnitt 1).
* Der Plan riegelt B1-B7 mit `not isClient() and not isServer()` ab und baut das Gehirn in B8 auf den Server um. Das ist ein
  zweiter Bau desselben Codes und widerspricht deiner Regel "jede Aenderung im SP und MP" (Gedaechtnis, CLAUDE.md Regel 7).
* **Vorschlag:** ab B2 das Gehirn unter `not isClient()`, Fenster und Menue auf dem Client, Bitten ueber eine Funktion, die im SP
  direkt aufruft und im MP `sendClientCommand` schickt (Idee: Companion Dogs `CD.request`). Dann laeuft jede Version in beiden
  Modi; nur der Kampf gegen Zombies bleibt bis B9 im MP aus (dort fehlt das Schadensbuch, `kampf_spez.md`:40). -> Frage 7.

## K5 (ernst) Anhaenger baut den Baeren neu

* Ausladen baut ein neues Tier: `BaseVehicle.removeAnimalFromTrailer` Offset 53-103 (`new IsoAnimal` + `copyFrom`).
* `IsoAnimal.copyFrom` nimmt ModData (Offset 1-8), Groesse (dieselbe `AnimalData`, Offset 134-139), Name, Leben, AnimalID mit,
  **aber nicht "unsterblich"** und vergibt eine neue Online-Id. Folge: unser Code muss ihn ueber die AnimalID neu finden und den
  Schalter nicht nur "nach dem Laden", sondern bei jedem neuen Objekt setzen (am einfachsten: jeder Durchlauf).

## K6 MP: Diebstahl und Besitzer offline

* Fremde koennen den Baeren in IHREN Anhaenger laden und wegfahren (Vanilla `ISVehicleMenu.lua`:665-790, keine Besitzpruefung)
  und, falls `canBeAttached = true` fuer das Jungtier, ihn an die Leine nehmen. Beides fehlte in der Liste "fuer fremde Baeren
  sperren". Toeten geht nicht (Unsterblich-Schalter, Stichprobe oben).
* Besitzer offline, aber ein Mitspieler steht daneben: der Baer ist geladen, unser Gehirn rechnet Hunger und Zombieschaden ->
  er koennte allein sterben. **Vorschlag:** Besitzer offline = Baer "ruht" (kein Schaden, kein Hunger, kein XP, bleibt stehen).

## K7 Ausdauer und Folgen beissen sich

* Folgen geht bis zur Antwort auf Frage 6 nur ueber `fleeTo`, das immer RENNT (`IsoAnimal.fleeTo` Offset 32-65). Mit "Rennen -2/s"
  ist der Baer nach 40 s Mitlaufen zu muede zum Kaempfen, und "30 s gerannt +1 XP" waere ein Selbstlaeufer.
* **Berichtigt:** Ausdauer sinkt nur im Kampf und beim Sprint auf ein Ziel, nicht beim Mitlaufen; XP fuer Ausdauer nur aus Kampf.

## K8 Die Engine zieht den Baeren selbst herum

* `wanderMul = 600` (`NCBearDefs.lua`:82): er laeuft alle paar Sekunden ein Stueck - auch bei "Bleiben".
* Flucht vor Laerm: jeder Schuss des Besitzers loest `respondToSound` aus, ohne Schalter (`kampf_spez.md`:177-181). Der Kampf-Lauf
  faengt das nur IM Kampf ab. Ein Begleiter, der bei jedem Schuss wegrennt, ist nicht spielbar.
* **Berichtigt:** B2 bekommt denselben Gegenzug fuer alle Befehle (fremde Bewegung mit `stopAllMovementNow` beenden,
  Vanilla `ISAnimalContextMenu.lua`:760), "Bleiben" ueber `getBehavior():setBlockMovement(true)` (Vanilla :89).

## K9 Schaden am Baeren: unsichtbar und Freund/Feind

* Kein Zombie nimmt den Baeren von selbst als Ziel: `IsoZombie` kennt die Klasse `IsoAnimal` gar nicht (javap: 0 Treffer), und
  ein gesetztes Tier-Ziel loescht der Angriff (`AttackState.triggerPlayerReaction` Offset 20-33). Bandits kennt Tiere nicht.
* Der Plan wuerfelt deshalb Schaden "je Zombie dicht vor ihm". Ohne sichtbares Zeichen meldest du "Baer stirbt ohne Grund".
  **Berichtigt:** jeder Treffer zeigt sich (Zucken/Knurren, Blut, Zahl im Fenster), und die Freund-Liste ist dieselbe wie beim
  Kampf: nie NPC-Crew-Leute oder freundliche Banditen (`kampf_spez.md`:34-35).

## K10 Unsterblich-Schalter: drei Nebenwirkungen fehlten

* Die Engine heilt ihn weiter jede Stunde (`AnimalData.updateHealth`, Heilzweig) - "Downed" muss eine eigene Marke sein, kein
  Lebens-Wert, sonst steht er von selbst auf, sobald er geheilt ist.
* Stress kann mit dem Schalter nur steigen (`IsoAnimal.changeStress` Offset 0-13). Gegenmittel: `animal:setDebugStress(x)`,
  belegt `server/ClientCommands.lua`:928, reiner Feldschreiber (Offset 0-5). Ob hoher Stress ihn stoert: ungeprueft.
* Wird nicht mitgenommen beim Ausladen aus dem Anhaenger (K5).

## K11 Kleineres

* **Groessentest:** `NCBear_Size` gilt auch nur bis zum naechsten Laden, nicht nur bis zum naechsten Spieltag (`IsoAnimal.load`
  Offset 405 klemmt wieder auf 1,0).
* **Mitspieler sehen das Wachsen nicht:** die Groesse steht nicht im laufenden Tierpaket (`recherche_spiel.md` 5). Der Server muss
  sie selbst schicken (eigener Befehl oder seine eigene `transmitModData`), der Client setzt sie mit `setSizeForced`.
* **Frage 6 genauer:** `pathToLocation(x, y, z)` ist in Vanilla belegt, aber am Zombie (`DebugContextMenu.lua`:640, gleiche
  Argumenttypen). `IsoAnimal` ueberschreibt die Methode (Offset 0-115: prueft die 15-Kachel-Leine, dann die Wegsuche). Belegt ist
  also Name und Form, nicht die Fassung am Tier.
* **NPC Crew:** steht der Baer in einer NPC-Crew-Tierzone, zaehlt ihn der Tierpfleger als Vieh (`tier_spez.md` 5.4) - inklusive
  Schlachtregeln, wenn du sie an hast. Vor jeder Tierzone fuer den Baeren: in NPC Crew ausnehmen (eigene Version, dein Wort).
* **Artname "bear":** Knox Wildlife (Workshop 3818096743, hier nicht installiert) hat Braunbaeren. Ob es denselben Namen nimmt:
  ungeprueft. Umbenennen geht nur, solange es nur Wegwerf-Spielstaende gibt (eine unbekannte Art laesst die Tierzelle nicht laden,
  `bau_lebend.md` Fund 1). -> Frage 8.
* **B4 haengt an fuenf neuen Clips** (`kampf_spez.md`:44-45) - nicht vor dem Kampf-Lauf und deinem Test.
* **Liege-Pose:** der Baer hat schon den Clip "Dead" (liegt, `bau_lebend.md`:11 fuenf Clips). Fuer Downed zuerst den nehmen, ein
  eigener Clip spaeter.
* **Zu gross:** B2 (Besitz + Befehle + Treppe) und B5 (Schaden + Tod + Downed + Aufhelfen) je in zwei Versionen geteilt; B8
  schrumpft durch K4.

## Was im Plan geaendert wurde

Siehe `PLAN.md`, Abschnitt "Berichtigt durch Kritik".

Statisch geprueft, nichts gespielt.
