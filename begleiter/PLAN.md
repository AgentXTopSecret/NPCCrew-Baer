# Baer als Begleiter - Plan fuer Kevin

> **Kevins Entscheidungen gehen vor (`ENTSCHEIDUNGEN.md`, 08.11.):** Groesse Jungtier 0,35, Halbstark ab 0,75, Erwachsen **1,35** (nicht 1,3); Wachstum etwa 7 Spieltage bis Halbstark und weitere 14 bis Erwachsen (nicht 60), Sandbox-Tempo; Leben 40/150/400; Futter 1/2/4, Wasser 1/2/3; Traglast 10/40/100 plus Packtaschen +50; Fischen spaeter. Wo dieser Plan andere Zahlen nennt, gelten die dort.

Stand 08.11.2026, PZ 42.21. **Statisch recherchiert, nichts gebaut, nichts gespielt.** Grundlage: `recherche_spiel.md`,
`recherche_dogs.md`, `recherche_lokal.md`, `recherche_web.md`, `../spiel/tier_spez.md`, `../spiel/bau_lebend.md`,
`../spiel/kampf_spez.md` (Lauf baer-kampf, nur gelesen). Zahlen ohne Fundstelle sind Vorschlaege zum Einstellen im Test.
Ideen aus fremden Mods: nur die Idee, eigener Code, Herkunft steht dabei.

---

## 1. Waer sowas moeglich?

Ja: das Spiel laesst ein Tier schon von selbst wachsen, kennt Hunger und Durst und hat einen Unsterblich-Schalter; Stufen,
Level, Ausdauer, Downed und Befehle bauen wir dazu. Die Engine laesst Zombies und Banditen ein Tier gar nicht angreifen,
also wuerfeln wir den Schaden am Baeren selbst (er wird verletzt, ohne dass der Zombie sichtbar zuschlaegt). **Groesstes
Risiko ist der Mehrspieler:** dort rechnet der Server das Tier, aber das Leben eines Zombies gehoert einem anderen Rechner
-- deshalb bleibt der KAMPF im Mehrspieler bis B9 aus; alles andere laeuft von Anfang an in beiden Modi (Abschnitt 9).
**Zwei Engine-Fallen** hat die Kritik gefunden, beide umgehbar: in einer Tierzone springt die Groesse auf Baby zurueck
(darum zaehlt unser eigener Wachstumszaehler, Abschnitt 4), und das Vanilla-Fuettern bietet einem Baeren kein Fleisch an
(darum ein eigener Menuepunkt, Abschnitt 6). Einzelheiten in `KRITIK.md`.

---

## 2. Groesse jetzt

**Echte Braunbaeren** (Quellen: [dimensions.com Grizzly](https://www.dimensions.com/element/grizzly-bear),
[Wikipedia Brown bear](https://en.wikipedia.org/wiki/Brown_bear)):

| | Schulterhoehe auf vier Beinen | Laenge | aufgerichtet | Gewicht |
|---|---|---|---|---|
| Maennchen | 1,07-1,37 m | 2,1-2,4 m | 2,5-3 m | 180-360 kg (Kuestenbaeren bis 600) |
| Weibchen | 0,91-1,12 m | 1,7-2,0 m | - | 135-180 kg |
| Junges im ersten Sommer | ca. 0,4 m (geschaetzt, ungeprueft) | ca. 0,7 m (ungeprueft) | - | 7-9 kg |

**Unser Baer heute** (Groesse 1,0): 1,95 m lang, Schultergelenk bei 0,72 m und Ruecken um 1,0 m, hoechster Punkt 1,16 m
(`../spiel/bau_stehend.md`:24 und :60, Skelett `../spiel/baer_tier.py`:64), gegen eine Spielfigur von 1,80 m. Nach den
Zahlen ein Weibchen. **Gegenprobe im Spiel:** eine Kuh ist bei Groesse 1,0 schon 2,66 m lang (`../spiel/pruefung_stehend.md`:30)
und waechst bis 1,1 (`CowDefinitions.lua`:192-193). Der Baer ist heute 2/3 einer Kuh -- darum wirkt er wie ein Baby.

**Vorschlag ausgewachsen: Groesse 1,3** = 2,54 m lang, Ruecken um 1,3 m, aufgerichtet rund 2,6 m (aus der Koerperlaenge
geschaetzt, ungeprueft). Das ist ein grosses Maennchen und im Spiel etwa so lang wie eine ausgewachsene Kuh, nur flacher.
**Vorschlag Jungtier: Groesse 0,35** = 0,68 m lang, um 0,4 m hoch (wie ein mittelgrosser Hund).

**Sofort ausprobieren** (Einzelspieler, Konsole mit -debug; die Datei `NCBearTest/42/media/lua/client/NCBearSize.lua` steht
schon da -- Spiel neu starten, falls es seit heute Nacht nicht neu gestartet wurde):

    NCBear_Size(1.3)

Gilt fuer alle Baeren in 20 Kacheln, bis der Baer einen Spieltag aelter wird oder der Spielstand neu geladen wird (dann
setzt das Spiel 1,0 zurueck, `AnimalData.growUp` Offset 130, `IsoAnimal.load` Offset 405). Danach auch `NCBear_Size(0.35)` (Jungtier) und `NCBear_Size(1.6)`, falls 1,3 noch klein
wirkt. Zum Vergleich eine Kuh daneben stellen (Debug-Menue, Tiere). **Dabei bitte ansehen:** rutschen die Fuesse beim Gehen
(das Spiel nimmt das Tempo aus der Animation, nicht aus der Groesse, `recherche_spiel.md` 1.3), und passt er bei 1,3 durch
eine Tuer.

---

## 3. Wie man ihn bekommt

| Weg | Wie | Vorteil | Nachteil |
|---|---|---|---|
| **A. Verwaistes Junges im Wald** | Beim Laden von Waldkacheln erscheint selten ein Junges (Zonentyp `Forest`/`DeepForest` per `square:getZone():getType()`, Vanilla `Traps/TrapSystem.lua`:43). Spieler fuettert es 3-5 Mal aus der Hand (Vanilla "Feed" gibt schon Vertrauen, `ISFeedAnimalFromHand.lua`:45-49), dann "Adoptieren". Optional fuehrt eine Spur im Suchmodus hin. | Abenteuer, Vanilla-Fuettern gratis, kein Gegenstand aus dem Nichts | Spawn-Code neu; Zufall (Haeufigkeit als Sandbox); im MP spawnt der Server |
| B. Mutter verteidigt das Junge | wie A, aber eine wilde Baerin steht dabei und greift den Spieler an | Spannung | Baer gegen SPIELER ist ein eigener Kampf (die Gruppe `buck` kann nicht angreifen, `tier_spez.md` 5.3); teuer, spaeter als Ausbau von A |
| C. Koederplatz | Honig oder Fisch am Waldrand ablegen, nach 1-3 Naechten sitzt dort ein Junges (Idee: Vanilla-Fallen) | Spieler steuert es, Besitz klar (wer den Koeder legte) | weniger Abenteuer, Koederplatz noetig |
| D. Seltener Fundort | Junges in einer Jagdhuette oder Foersterei | gut als Zusatz | Gebaeudearten suchen, schwer zu finden |

**Immer dabei:** ein Test-Weg (Konsole / Debug-Menue "Junges geben").
**Empfehlung: A, dazu C fuer alle, die keinen Wald finden; B spaeter.**

**Ein Baer je Spieler:** ein Register auf dem Rechner, der entscheidet (Einzelspieler bzw. Server), Schluessel
Benutzername -> Tier-Kennung (`getAnimalID()`, gespeichert und auf Client und Server gleich, `recherche_spiel.md` 4.3).
Ein Junges erscheint nur fuer Spieler ohne lebenden Baeren, und das Adoptieren prueft das Register noch einmal.
**Besitz, Level, XP und Wachstum stehen NUR in diesem Register** (globaler Speicher des Servers, Schluessel AnimalID); die
ModData am Tier ist nur ein Spiegel fuer die Anzeige. Grund: jeder eingeloggte Client darf die ModData eines Tiers ueberschreiben
(`ObjectModDataPacket.parse` Offset 51-75, Faehigkeit nur `LoginOnServer`), `KRITIK.md` K3. Im
Einzelspieler ist der Schluessel fest (nicht der Charaktername: nach dem Spielertod hiesse man anders, NPC-Crew-Lehre v3.9.66).
Stirbt der Baer, wird der Platz frei (Vorschlag: nach 7 Spieltagen). Herkunft "Grenze je Spieler": Companion Dogs (`MaxCompanions`).

---

## 4. Stufen

Eine einzige Tierart, die stufenlos waechst (kein Stufenwechsel der Engine: der baut ein neues Tier und wirft unsere Daten weg,
`recherche_spiel.md` 1.2). **Gewachsen wird ueber UNSEREN Zaehler** "Wachstum 0..1" im Register, nicht ueber die Engine:
die Engine setzt die Groesse jedes Tiers in einer Tierzone beim Zurueckkommen auf `minSize` zurueck (`updateStatsAway` Offset
192-196 -> `AnimalData.init` -> `initSize` Offset 72-76, `KRITIK.md` K1). Darum: `ageToGrow` in der Definition sehr gross
(Engine-Wachsen praktisch null), Groesse = 0,35 + Zaehler x 0,95 per `getData():setSizeForced(x)` (Vanilla `ButcheringUtil.lua`:569),
Gewicht per `getData():setWeight(x)` (:566), beides regelmaessig nachgesetzt. Die Stufe kommt aus dem Zaehler, nie aus der
angezeigten Groesse. Vorgabe 60 Tage bis ausgewachsen, in der Sandbox ohne Neustart einstellbar.

| Stufe | Tage (bei 60) | Groesse | Laenge | Leben (unsere Punkte) | Schaden je Hieb | Kann |
|---|---|---|---|---|---|---|
| **Jungtier** | 0-15 | 0,35-0,59 | 0,7-1,15 m | 40-70 | 0 | folgt, frisst, spielt; versteckt sich bei Zombies hinter dem Spieler; kaempft nie. Vanilla-Seil geht (reisst bei 15 Kacheln) |
| **Halbstark** | 15-40 | 0,59-0,98 | 1,15-1,9 m | 70-150 | 0,4-0,9 | Prankenhieb, wirft um; nimmt es mit einzelnen Zombies auf, zieht sich ab 3 Gegnern zurueck |
| **Erwachsen** | ab 40, voll bei 60 | 0,98-1,30 | 1,9-2,5 m | 150-200 | 1,0-1,3, Biss 2,5 | alles aus dem Kampf-Lauf: Aufrichten + Bruellen, Prankenhieb links/rechts, Doppelschlag, Biss am Boden |

Schaden in Zombie-Leben: ein normaler Zombie hat 1,8-2,1 (`kampf_spez.md` 5.1), der Erwachsenen-Hieb 1,3 kommt aus
`kampf_spez.md` 5.3. Leben und Schaden wachsen mit der Groesse mit, die Faehigkeiten springen an den Grenzen.

**Zeit:** unser Zaehler waechst je Spielstunde, in der der Baer geladen ist (in deiner Naehe), um 1 / (Tage x 24); hungrig
oder durstig (ueber 50 %) halb so schnell, verletzt (unter 50 % Leben) gar nicht; "Wachstum anhalten" stoppt ihn. Zur Engine
(nur noch Hintergrund): sie wuerde einmal je Spieltag um `(maxSize - minSize) / ageToGrow x Gesundheit` wachsen
(`AnimalData.growUp` Offset 40-130), "Animal age" aendert dort nur das Alter (`getAgeGrowModifier` Offset 9-75); die Tierzone
macht das zunichte (oben). Konsole "Tage vorspulen" setzt unseren Zaehler, nie `setAgeDebug` (das setzt die Groesse ebenfalls
zurueck, `IsoAnimal.setAgeDebug` Offset 37).

---

## 5. Level-System

Vier Faehigkeiten, je Level 1-10, eigene Zahlen (Idee "Faehigkeiten mit XP": Companion Dogs; "Ausdauer": Horse Mod).

| Faehigkeit | XP durch | Wirkung je Level | Grenze |
|---|---|---|---|
| **Kraft** | Treffer +1, Zombie getoetet +5 | +5 % Schaden, mehr Umwerf-Chance | +50 % |
| **Zaehigkeit** | Treffer eingesteckt +1, ueberlebter Kampf +3 | +6 % Leben | +60 % |
| **Ausdauer** | Kampf +2, Kampf mit wenig Ausdauer durchgehalten +3 | +10 Ausdauer und schnellere Erholung | 100 -> 200 |
| **Spuersinn** | Zombie zuerst entdeckt +1 | +1 Kachel Warnweite, er brummt frueher | 10 -> 20 Kacheln |

* **Ausdauer** (neuer Wert 0-100, gibt es fuer Tiere nicht, `recherche_spiel.md` 3.5): Hieb -15, Doppelschlag -30,
  Sprint auf einen Gegner -2/s; Erholung im Stehen +5/s, im Gehen +2/s. Unter 20: kein Angriff, er zieht sich zum Spieler zurueck.
  **Mitlaufen beim Folgen kostet nichts**, auch wenn er dabei rennt (bis Frage 6 geht Folgen nur ueber `fleeTo`, das immer rennt;
  sonst waere er nach 40 s Mitlaufen zu muede zum Kaempfen, `KRITIK.md` K7).
* **Kurve:** Level n braucht 30 x n XP (Level 10 = 1650 XP insgesamt). Sandbox-Faktor fuer die XP.
* **Obergrenze je Stufe:** Jungtier hoechstens Level 3, Halbstark 6, Erwachsen 10 -- Wachsen und Lernen haengen zusammen.
* **Nicht dabei: Tempo.** Das Spiel nimmt die Geschwindigkeit aus der Animation (`tier_spez.md` 2.8); dafuer braeuchte es
  eigene Gang-Animationen.
* **Bindung** (kein Level, ein Balken): steigt mit Fuettern und Streicheln, sinkt bei Hunger. Bei wenig Bindung gehorcht er
  schlechter (Idee: Companion Dogs `LoyaltyDecayPerDay`).
* **Anzeige:** im Baeren-Fenster je Faehigkeit Level und XP-Balken; beim Aufstieg eine kurze Meldung.

---

## 6. Beduerfnisse

* **Futter:** Fleisch (roh und gekocht), Fisch, Beeren, Obst, Honig, Insekten, Eier, Nuesse. **Das Vanilla-Menue "Feed" bietet
  davon nur Obst an:** sein Vorfilter laesst nur Tierfutter, Milch und die Arten `Fruits`/`Vegetables` durch
  (`ISAnimalContextMenu.lua`:33-39; Brombeere ist `Berry`, Honig `NoExplicit`, Lachs `Fish`, Steak `Beef`, `food.txt`). Darum
  ein **eigener Rechtsklick "Baer fuettern"** mit unserer Liste, der die Vanilla-Aktion `ISFeedAnimalFromHand` startet (`isValid`
  fragt nur die Tasche, :5-7; `complete` -> `feedFromHand` -> `AnimalData.eatItem`). Ob `eatItem` Fleisch richtig verrechnet:
  ungeprueft, erster Testpunkt in B3. Die Liste in der Definition (`feedByHandType`, `eatTypeTrough`) braucht es nur fuer den Trog.
  Honig und Lachs geben extra Bindung.
* **Wasser:** Vanilla-Menue "Water" aus Flasche oder Eimer (ab Durst 0,1, `ISAnimalContextMenu.lua`:300). Unterwegs sucht ein Tier
  nichts (`recherche_spiel.md` 2.2). **Tierzone mit Trog an der Basis erst nach zwei Vorarbeiten:** unser Groessen-Nachsetzen
  (Abschnitt 4, die Zone setzt sonst die Groesse zurueck) und NPC Crew muss den Baeren auslassen (heute zaehlt der Tierpfleger
  `bear` als Vieh mit, samt Schlachtregeln, `tier_spez.md` 5.4) -- das ist eine NPC-Crew-Version und braucht dein Wort.
* **Takt (Vorschlag):** erwachsen etwa eine Mahlzeit am Tag und zweimal trinken; das Jungtier oefter und weniger.
  Sandbox-Faktor. Nur solange er geladen ist -- an der Basis verhungert er nicht, waehrend du weit weg bist (dieselbe Regel
  hat Companion Dogs).
* **Mangel:** ab halb hungrig: Ausdauer erholt sich halb so schnell, kein XP, Bindung sinkt. Ab 80 %: Leben sinkt jede Stunde,
  er waechst nicht mehr; ohne Unsterblich stirbt er daran, mit Unsterblich liegt er am Boden (Abschnitt 7).
* **Jungtier-Idee:** in den ersten Tagen Milch (Idee: Baby Animal Food), danach normales Futter. Optional.
* **NPC Crew (optional, spaeter, eigene Entscheidung):** der Tierpfleger fuellt Trog und Futter, wenn der Baer an der Basis
  bleibt. Dafuer muss NPC Crew den Baeren kennen (heute zaehlt der Tierpfleger `bear` einfach mit, `tier_spez.md` 5.4).

---

## 7. Tod und Unsterblich

**Ein Weg fuer beide Einstellungen:** der Engine-Schalter `setIsInvincible(true)` ist immer an (Lua-belegt
`ISAnimalContextMenu.lua`:563). Damit kann nur unser Code sein Leben aendern (er schaltet dafuer kurz aus, wie Companion Dogs);
Spieler, Autos und andere Tiere tun ihm nichts. Hunger und Durst laufen mit dem Schalter in der Engine nicht mehr
(`AnimalData.updateHungerAndThirst` Offset 41) -- also zaehlt unser Takt sie hoch (`animal:getStats():set(CharacterStat.HUNGER, x)`,
Vanilla `ISAnimalContextMenu.lua`:739-740). Der Schalter wird nicht gespeichert und beim Ausladen aus dem Anhaenger nicht
mitgenommen (`IsoAnimal.copyFrom` hat kein Feld dafuer, `BaseVehicle.removeAnimalFromTrailer` Offset 53-103 baut ein neues Tier)
-- also in jedem Durchlauf neu setzen und den Baeren ueber die AnimalID wiederfinden, nie ueber ein gemerktes Objekt.
**Zwei Nebenwirkungen:** die Engine heilt ihn trotz Schalter jede Stunde ein Stueck (`AnimalData.updateHealth`), und Stress kann
nur steigen (`IsoAnimal.changeStress` Offset 0-13); unser Takt haelt den Stress mit `animal:setDebugStress(x)` unten (belegt
`server/ClientCommands.lua`:928, reiner Feldschreiber Offset 0-5).

**Schaden am Baeren (selbst gewuerfelt, Zahlen fuer den Test):** je Zombie, der dicht vor ihm steht und nicht liegt, alle 2 s
4 Punkte; feindlicher Bandit im Nahkampf 8-15, mit Waffe 10-25 bei Treffer-Chance. Teilt man durch seine Lebenspunkte, ist ein
Kratzer fuer das Jungtier 10 %, fuer den Erwachsenen 2 %. **Ein Wert fuer das Leben:** das Engine-Leben (0..1) ist der Anteil,
die Lebenspunkte aus Abschnitt 4 sind nur der Teiler (Schaden / Lebenspunkte = Abzug); so kommt das Leben im MP von selbst zu
den Clients (`recherche_spiel.md` 5).
**Freund und Feind** wie beim Kampf: nie NPC-Crew-Leute, nie freundliche oder neutrale Banditen (`kampf_spez.md`:34-35).
**Jeder Treffer sichtbar** (Zucken oder Knurren, Blut, Zahl im Fenster): kein Zombie nimmt den Baeren von selbst als Ziel
(`IsoZombie` kennt `IsoAnimal` nicht, javap; `AttackState.triggerPlayerReaction` Offset 20-33), also schlaegt auch keiner
sichtbar zu -- ohne Zeichen saehe ein Tod aus wie ohne Grund.

| Sandbox "Baer unsterblich" | Was passiert, wenn das Leben ausgeht |
|---|---|
| **aus (Vorgabe)** | Er stirbt: Sturz-Animation, Leiche (gibt es schon, `bau_lebend.md`). Meldung an den Besitzer, Register-Platz wird frei. |
| **an** | Unter 30 % Leben legt er sich hin (zuerst der vorhandene Clip "Dead", eigener Clip spaeter), kaempft nicht, bewegt sich nicht; "liegt" ist eine eigene Marke, kein Lebenswert (die Engine heilt ihn weiter); sein Leben faellt nicht unter 10 %. **Aufhelfen:** Rechtsklick "Aufhelfen", 5 s, dann 45 % Leben und eine Minute ohne Kampf -- dieselben Zahlen wie bei den NPCs (Niederschlag 30 %, Aufhelfen 45 %, Boden 10 %, `client/BanditsNPCGuardian.lua`:15-32, nur gelesen). Vorschlag: ohne Hilfe steht er nach 12 Spielstunden mit 15 % selbst auf. |

Ein "Downed" kennt das Spiel nicht (`recherche_spiel.md` 3.4); keine der gelesenen Mods hat es. Die Liege-Animation baut sich wie
die Kampf-Animationen (eigener Knoten unter `AnimSets/buck/idle/` mit eigener Variable, `kampf_spez.md` 1.1-1.5).

---

## 8. Befehle und Fenster

**Rechtsklick auf den eigenen Baeren:** Folgen, Bleiben (hier), Bewachen (Umkreis 6 Kacheln um diesen Punkt), Kampf an /
nur verteidigen / aus, Komm her, Umbenennen, Wachstum anhalten (Idee: Companion Dogs), Aufhelfen, Fenster oeffnen.

**Fenster (klein):** Name, Stufe mit Balken bis ausgewachsen, Leben, Hunger, Durst, Ausdauer, Bindung, die vier Faehigkeiten
mit Level, aktueller Befehl, "zuletzt gesehen" wenn er weit weg ist. Namensschild ueber dem Kopf optional.

**Folgen:** belegt ist nur `animal:fleeTo(kachel)` (`ISMilkAnimal.lua`:38) -- das RENNT immer. Ruhiges Mitgehen braucht
`pathToLocation(x, y, z)`: in Vanilla belegt, aber am Zombie (`DebugContextMenu.lua`:640, gleiche Argumente); `IsoAnimal`
ueberschreibt die Methode (Offset 0-115: prueft die 15-Kachel-Leine, dann die Wegsuche) -> Frage 6. Das Jungtier kann bis
dahin am Vanilla-Seil gehen (mit einer Waffe in der Hand faellt das Seil, `recherche_spiel.md` 4.1); im MP kann dann aber jeder
Fremde es anleinen (Abschnitt 9). Treppen: per Vorgabe aus (`canClimbStairs`), in B2b testen.

**Die Engine zieht ihn selbst herum, das muss B2b abfangen:** er wandert alle paar Sekunden (`wanderMul = 600`,
`NCBearDefs.lua`:82), auch bei "Bleiben", und er flieht vor JEDEM Schuss, auch vor deinem (`respondToSound`, kein Schalter,
`kampf_spez.md`:177-181). Gegenzug fuer alle Befehle, nicht nur im Kampf: fremde Bewegung mit `stopAllMovementNow()` beenden
(Vanilla `ISAnimalContextMenu.lua`:760), "Bleiben" mit `getBehavior():setBlockMovement(true)` (:89).

**Kein Teleport.** Kommt er nicht durch, sagt das Fenster es; nichts holt ihn automatisch zum Spieler (Kevins rote Linie).

---

## 9. Mehrspieler

| Wer | rechnet |
|---|---|
| **Server** (im Einzelspieler der eine Rechner) | Laufen, Leben (Engine); unser Gehirn: Wachstum, Befehle, Zielwahl, Beduerfnisse, XP, Downed, Tod, Register, Junges-Spawn |
| **Client** | Fenster, Rechtsklick, Bitten per Befehl an den Server; der Server prueft bei JEDER Bitte den Besitz |
| Kommt von selbst zum Client | Leben, Hunger, Durst, Alter, Gewicht (`recherche_spiel.md` 5) |
| Muessen wir schicken | Groesse, Level, Ausdauer, Name, Befehl (stehen nicht im laufenden Tierpaket) |

**Risiken:** (1) Das Leben eines Zombies gehoert dem Client mit Hoheit; ein Treffer vom Server haelt nicht -- Companion Dogs
loest das mit einem Schadensbuch, den Todesstoss fuehrt der Besitzer-Client aus (Idee). Das ist der teure Teil. (2) Die
Animations-Variablen muss jeder Client an seiner Kopie setzen. (3) Vanilla laesst JEDEN Spieler ein Tier toeten, anleinen,
aufheben -- fuer fremde Baeren sperren (Menue und Server). **Dazu zwei Diebstahl-Wege:** ein Fremder laedt ihn in SEINEN Anhaenger
und faehrt weg (`ISVehicleMenu.lua`:665-790) oder nimmt das Jungtier an die Leine (falls `canBeAttached`). Toeten geht wegen des
Unsterblich-Schalters nicht (`ISKillAnimal.lua`:57-59 ruft `setHealth(0)`). (4) Ob der Server unsere `.glb` laedt, ist ungeprueft
(`tier_spez.md` 6.3). (5) Logout: der Baer bleibt stehen, wo er ist, und **ruht, solange der Besitzer offline ist** (kein Schaden,
kein Hunger, kein XP) -- sonst stirbt er neben einem Mitspieler allein. Kein Verstauen und Neubauen wie bei Companion Dogs -- jeder
Neubau ist eine Kopie- oder Verlustquelle (sie brauchen neun Retter dafuer). (6) **Jeder Client kann die ModData am Tier
ueberschreiben** (`ObjectModDataPacket`, nur `LoginOnServer`): die Wahrheit steht im Register des Servers (Abschnitt 3), unser
Client ruft `transmitModData` am Baeren nie. (7) Groesse und Level sieht ein Mitspieler nur, wenn der Server sie schickt
(nicht im laufenden Tierpaket); der Client setzt sie mit `setSizeForced`.

**Beide Modi von Anfang an, nur der Kampf nicht** (berichtigt, `KRITIK.md` K4; Frage 7): das Gehirn laeuft ab B2 dort, wo
`not isClient()` gilt -- im Einzelspieler und auf dem Server derselbe Code (Idee: Companion Dogs). Fenster und Menue laufen
auf dem Client und bitten ueber eine Funktion, die im Einzelspieler direkt aufruft und im Mehrspieler `sendClientCommand`
schickt; der Server prueft bei jeder Bitte den Besitz. Nur der Kampf gegen Zombies (Baer trifft Zombie) bleibt im Mehrspieler bis
B9 aus (Schadensbuch fehlt, `kampf_spez.md`:40). Jede Version wird in beiden Modi getestet.

---

## 10. Sandbox, Ideen, Versionen, Fragen

### Sandbox-Seite "NC Bear" (Vorschlag)

| Option | Vorgabe | Herkunft der Idee |
|---|---|---|
| Baer unsterblich (liegt statt zu sterben) | aus | Kevin; Companion Dogs `Death` |
| Tage bis ausgewachsen | 60 (10-365) | Companion Dogs `MaturityDays` |
| Baeren je Spieler | 1 | Companion Dogs `MaxCompanions` |
| Haeufigkeit Junges im Wald | mittel | Companion Dogs `DogSpawnMultiplier` |
| Hunger- und Durst-Tempo | 1,0 | Companion Dogs `NeedsRateMultiplier` |
| Schaden des Baeren / Schaden am Baeren | 1,0 / 1,0 | Companion Dogs `DogDamageMultiplier` |
| XP-Tempo | 1,0 | Companion Dogs `SkillXPRate` |
| Ausdauer-Tempo | 1,0 | Horse Mod `StaminaMultiplier` |
| Selbst aufstehen nach Stunden (0 = nie) | 12 | eigen |
| Neues Junges nach dem Tod, Tage | 7 | eigen |

### Ideen aus anderen Mods (nur die Idee)

| Idee | Herkunft |
|---|---|
| Zaehmen durch Fuettern bis Vertrauen voll | Companion Dogs (`TameThreshold`) |
| Junges ueber eine Spur im Suchmodus finden | Meat Expansion (Grizzly-Spuren) |
| Ausdauer sinkt beim Rennen, kommt im Stehen zurueck | Horse Mod (Stamina) |
| Jeder Baer etwas anders (Anlagen) | Horse Mod, Companion Dogs (Gene) |
| Warn-Brummen, wenn Zombies kommen | Companion Dogs (Sentinel) |
| Rueckzug bei wenig Leben; verletzt kaempft er nicht | Companion Dogs, Animals Attack Zombies |
| Wachstum anhalten | Companion Dogs |
| Daten zusaetzlich unter der Tier-Kennung im globalen Speicher | Horse Mod (HorseModData) |
| Besitzer-Boni nie ueber die Engine-XP-Faktoren | Companion Dogs (OwnerXP.lua:4-7) |
| Milch fuer das Junge | Baby Animal Food |
| Spaeter: Satteltaschen am grossen Baeren, Trauer beim Tod, Reiten | Companion Dogs, Horse Mod |

### Versionen (jede laeuft als Workflow: Bau, Pruefer, Nachbesserung, Integrator; hoechstens 10 Agenten)

| Version | Inhalt | Agenten |
|---|---|---|
| **B1** | Wachsen ueber UNSEREN Zaehler (Abschnitt 4; Zaehler im globalen Speicher je AnimalID, laeuft unter `not isClient()`, also SP und Server): Groesse 0,35 -> 1,3 (nach deinem Test) per `setSizeForced`, Gewicht 10-350 kg per `setWeight`, 60 Tage, Nachsetzen nach Zone/Laden, Anhaenger passt (Platz 300 statt 600, Tier-Anhaenger fasst 500, `vehicle_trailer_livestock.txt`:51), Konsole "Tage vorspulen"; Artname festlegen (Frage 8) | 6 |
| **B2a** | Besitz und Test-Weg: Register im globalen Speicher des Servers (einer je Spieler), Spiegel am Tier, "Junges geben", Name, Unsterblich-Schalter je Durchlauf, Bitten-Funktion SP/MP, kleines Fenster | 6 |
| **B2b** | Befehle: Folgen/Bleiben/Komm her, Wandern und Flucht vor Schuessen abfangen, Treppe testen; fremde Menues und Anhaenger sperren | 6 |
| **B3** | Beduerfnisse: eigener Menuepunkt "Baer fuettern" + Vanilla-Water, Takt, Mangel, Bindung, Stress niedrig halten; Ruhe bei Besitzer offline | 6 |
| **B4** | Stufen an den Kampf haengen (erst nach dem Lauf baer-kampf, seinen fuenf neuen Clips und deinem Test): Jungtier kaempft nicht, Halbstark nur Hieb, Erwachsen alles; Schaden waechst mit; im MP noch aus | 6 |
| **B5a** | Schaden am Baeren (sichtbar, Freund/Feind wie beim Kampf), Tod, Sandbox Unsterblich, Meldung, Register-Platz | 7 |
| **B5b** | Downed: Marke "liegt", Clip "Dead" als Liege-Pose, Aufhelfen per Rechtsklick, selbst aufstehen | 7 |
| **B6** | Level, Ausdauer (Folgen kostet nichts), Spuersinn-Brummen, Fenster mit Balken | 7 |
| **B7** | Junges im Wald finden (Weg A), Koederplatz (C), Haeufigkeit | 7 |
| **B8** | Mehrspieler-Rest: Groesse/Level/Name an die Clients, Animations-Variablen je Client, Abnahme aller Versionen im MP mit Rolle 'user' | 7 |
| **B9** | Kampf im Mehrspieler (Schadensbuch, Todesstoss beim Client mit Hoheit) | 10 |

Nach jeder Version testest du; ich nenne vorher die Zahl der Agenten und pruefe das Kontingent.

### Fragen an dich

1. **Groesse:** nach dem Test mit `NCBear_Size` -- Vorschlag Jungtier 0,35, ausgewachsen 1,3. Passt das, oder groesser?
2. **Bekommen:** Vorschlag Weg A (Junges im Wald finden und anfuettern), C als Zusatz, die Mutter (B) spaeter. Einverstanden?
3. **Wachstum:** Vorschlag 60 Spieltage bis ausgewachsen (nur Zeit, in der er in deiner Naehe ist), in der Sandbox einstellbar.
4. **Wer darf ihm schaden:** Vorschlag nur Zombies, Banditen, Hunger und Durst -- Spieler und Autos nicht (kein Eigenbeschuss).
   Nach dem Tod ein neues Junges nach 7 Spieltagen. Ok?
5. **Downed (Unsterblich an):** Vorschlag Aufhelfen per Rechtsklick (5 s, dann 45 % Leben wie bei den NPCs); ohne Hilfe steht
   er nach 12 Spielstunden mit 15 % allein auf. Ok, oder nur per Aufhelfen?
6. **Gehen statt Rennen:** ruhiges Mitgehen braucht `pathToLocation` am Tier. Vanilla benutzt den Aufruf nur am Zombie
   (`DebugContextMenu.lua`:640), am Tier ueberschreibt das Spiel ihn (Jar gelesen: prueft die Leinen-Grenze, dann Wegsuche).
   Vorschlag: als Ausnahme mit Jar-Beleg in B2b erlauben -- sonst rennt er immer hinterher.
7. **Beide Modi:** Vorschlag: jede Version laeuft und wird getestet im Einzelspieler UND im Mehrspieler (deine Regel), nur der
   Kampf gegen Zombies bleibt im Mehrspieler bis B9 aus. Statt "erst alles Einzelspieler, Mehrspieler am Ende" (dann muesste
   B8 vieles neu bauen). Einverstanden?
8. **Name der Tierart:** heute `bear`. Eine andere Tier-Mod (Knox Wildlife) hat auch Braunbaeren; ob sie denselben Namen nimmt,
   ist ungeprueft. Umbenennen (z. B. `ncbear`) geht nur jetzt, solange es nur Testspielstaende gibt -- spaeter wirft ein alter
   Spielstand beim Laden. Umbenennen in B1?

---

## Berichtigt durch Kritik (08.11., `KRITIK.md`)

Selbst im Jar bzw. in Vanilla nachgelesen, nicht gespielt.

| Wo | Vorher | Jetzt | Beleg |
|---|---|---|---|
| 4 Stufen, B1 | Engine laesst ihn wachsen, Stufe aus der Groesse, Tierzone zaehlt mit | eigener Zaehler 0..1, Groesse und Gewicht per `setSizeForced`/`setWeight` nachgesetzt, `ageToGrow` sehr gross, Stufe aus dem Zaehler | Tierzone setzt beim Zurueckkommen auf `minSize`: `DesignationZone.loading` 0-32 -> `doMeta` 29-48 -> `updateStatsAway` 192-196 -> `AnimalData.init` -> `initSize` 72-76 |
| 6 Futter, B3 | Vanilla "Feed" nimmt Fleisch, Fisch, Beeren, Honig ueber die Definition | eigener Menuepunkt, startet `ISFeedAnimalFromHand` | Vorfilter `ISAnimalContextMenu.lua`:33-39 laesst nur Futter, Milch, Obst/Gemuese durch |
| 6 Wasser | Schwelle `:465`, Tierzone an der Basis als Selbstversorgung | Schwelle `:300`; Tierzone erst nach Groessen-Nachsetzen und NPC-Crew-Ausnahme | `tier_spez.md` 5.4 |
| 3, 9 Besitz | "Daten am Tier plus Sicherung" | Wahrheit nur im Server-Register (AnimalID), Tier-ModData nur Spiegel | `ObjectModDataPacket.parse` 51-75, `LoginOnServer` |
| 9 Aufbau, Frage 7 | B1-B7 nur Einzelspieler, B8 baut auf den Server um | Gehirn ab B2 unter `not isClient()` (SP und Server), jede Version in beiden Modi getestet, nur Kampf im MP bis B9 aus | `kampf_spez.md`:173-174, Companion Dogs `if not isClient()` |
| 7 Unsterblich | "nach jedem Laden neu setzen" | in jedem Durchlauf, Baer ueber AnimalID finden; Engine heilt weiter; Stress per `setDebugStress` | `removeAnimalFromTrailer` 53-103 + `copyFrom` ohne Schalter; `changeStress` 0-13; `ClientCommands.lua`:928 |
| 7 Downed | unter 30 % liegt er (eigene Animation) | eigene Marke "liegt", zuerst Clip "Dead" | Heilzweig in `AnimalData.updateHealth`; fuenf Clips `bau_lebend.md`:11 |
| 7 Schaden | Wuerfel je Zombie dicht vor ihm | dazu: jeder Treffer sichtbar, Freund/Feind wie im Kampf, Engine-Leben = Anteil | `IsoZombie` kennt `IsoAnimal` nicht; `kampf_spez.md`:34-35 |
| 5 Ausdauer | Rennen -2/s, 30 s Rennen = XP | Mitlaufen kostet nichts und gibt keine XP | Folgen nur per `fleeTo` (rennt immer, Offset 32-65) |
| 8 Befehle, B2b | fehlte | Wandern und Flucht vor Schuessen abfangen (`stopAllMovementNow`, `setBlockMovement`) | `NCBearDefs.lua`:82, `kampf_spez.md`:177-181, `ISAnimalContextMenu.lua`:760/:89 |
| 9 MP-Risiken | Toeten, Anleinen, Aufheben sperren | dazu: fremder Anhaenger, Leine des Jungtiers; Ruhe bei Besitzer offline; Groesse an Clients schicken | `ISVehicleMenu.lua`:665-790 |
| 2 Groessentest | gilt bis einen Spieltag aelter | auch bis zum Neuladen | `IsoAnimal.load` 405 |
| Frage 6 | `pathToLocation` nur Jar und fremde Mods | am Zombie Vanilla-belegt, am Tier ueberschrieben | `DebugContextMenu.lua`:640, `IsoAnimal.pathToLocation(III)` 0-115 |
| Versionen | B2 und B5 je eine, B8 mit 9 Agenten | B2a/B2b, B5a/B5b, B8 nur Rest (7); B4 erst nach den Kampf-Clips | `kampf_spez.md`:44-45 |
| Fragen | 6 | 8 (neu: beide Modi, Artname) | Knox Wildlife hat Braunbaeren (`recherche_web.md`), Name ungeprueft |

Statisch recherchiert, nichts gebaut.
