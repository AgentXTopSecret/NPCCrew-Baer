# Lauf baer-zaehmen (B1a): PLAN -- Baeren-Junges finden und zaehmen

Stand 10.11.2026 abends. **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2 (nicht 42.21, FE 0.1).
Verbindlich fuer drei Bauer: KERN und OBERFLAECHE gleichzeitig mit getrennten Dateien, danach ZUSAMMENBAU (Uebernahme-Skript, Naehte).
Kurzformen: `FE x.y` = `forschung_engine.md` Abschnitt x.y; `FB x.y` = `forschung_bestand.md`; `ENT:n` = `baer/begleiter/ENTSCHEIDUNGEN.md`
Zeile n; `V:` Vanilla `media/lua`; `B:` Bandits `42.22/media/lua`; `NC:` NPC Crew `42/media/lua`; `dec/` = `_arbeit/baer_zaehmen/dec/`
(Jar 42.22.2, nur Lesehilfe). `M/` = `_arbeit/baer_zaehmen/mod/42/media/`. Modul-Tabelle im Text immer `B` = `BanditsNPC.Bear`.
"Weltstunden" = `getGameTime():getWorldAgeHours()` (FE 4).

Kevins Worte, auf denen der Plan steht: "nebenbei will ich das du schonmal den code programmierst das man das baby finden und tamen kann"
(10.11.); "Weg A (verwaistes Junges im Wald, 3-5 Mal aus der Hand fuettern) plus C (Koederplatz mit Honig oder Fisch)" (ENT:41); "mit
futter tamed und den streicheln kann ... so eine mischung aus beiden soll den fortschritt fuellen" (ENT:104); "taming balken mit vorschrit"
(ENT:99); "immer streichelbar ... mit cooldown" (ENT:107); ein Baer je Spieler (ENT:34); neues Junges 7 Spieltage nach dem Tod (ENT:45).
Alles andere in diesem Plan ist VORSCHLAG und steht deshalb als Sandbox-Option oder als Frage in Abschnitt 11.

---

## 0. Entscheidungen des Planers (gelten fuer alle Bauer)

**0.1 Bauart der Scheu: NICHT wild, die Scheu spielt unser eigener Takt (FE O1, Bauart Z).** Grund, selbst im Jar nachgelesen:
ein wildes Tier flieht IMMER, sobald ein Spieler naeher als 3 Kacheln ist (`dec/BaseAnimalBehavior.java:1581-1583`), und die
Fluchtfunktion fragt die Bewegungssperre gar nicht (`fleeFromChr`, `:1418-1512`, kein `blockMovement` darin; die Sperre wirkt nur auf
Wandern und Verhalten, `:75-84`, `:556-570`). Fuettern "aus der Hand" (Spieler steht daneben) waere mit `wild = true` also nicht
zuverlaessig baubar; `setWild(true)` gibt es belegt nicht (FE 14). Folge: `wild = false`, `alwaysFleeHumans = false`; "scheu" ist ein
ZUSTAND im Register, das Weglaufen macht `animal:fleeTo(sq)` (belegt, FE 2). Nebenbei gewonnen: kein Verbluten-Zaehler, kein
Engine-Zahmwerden in Tierzonen, "Animal info" geht. Preis: Vanillas Menuepunkt "Kill" erscheint (wird am Jungen ausgeblendet, 5.7) und
der Namenszusatz "(Wild)" fehlt (der Zaehm-Balken zeigt stattdessen "scheu").

**0.2 Bewegung des Jungen nur ueber `fleeTo(sq)`** (rennt immer; V:shared/TimedActions/Animals/ISMilkAnimal.lua:38, laeuft dort auch
auf dem Server: `milk()` ruft `stress()` und hat einen `isServer()`-Zweig, :60-66). `pathToLocation` (Kevins Ausnahme) wird in B1a NICHT benutzt -- ein
tapsig rennendes Junges ist fuer B1a gut genug, und es bleibt bei null Ausnahmen. Stehenbleiben: `getBehavior():setBlockMovement(true)`
(FE 2; loest sich laut Jar nach rund 8000 Zaehleinheiten von selbst, `dec/BaseAnimalBehavior.java:75-80` -- haengt also nie endlos).

**0.3 Eigene Zeitaktionen, eigener Verbrauch.** Vanillas "Feed"/"Pet"/"Lure" werden nicht benutzt (`feedFromHand` verbraucht ohne
Hunger nichts, FE 8.3; Vanillas Streicheln teilt durch `maxSize - minSize` = 0 und braucht `attachment head`, FE 2/7.3). Fuettern
verbraucht genau EIN ganzes Stueck in `complete()` (FE 8.3). Die Engine-Akzeptanz ist nie der Balken (FE 5.3); unser Streicheln ruft
zusaetzlich `animal:petAnimal(character)` (FE 10), damit die Akzeptanz ehrlich mitsteigt (spaeterer Q-Ruf).

**0.4 Koederplatz unsichtbar** (FE O4): das Stueck wird beim Auslegen verbraucht, der Platz steht nur im Register, der Besitzer sieht
ein Schild ueber der Kachel. Kein Bodengegenstand, also nichts, was verrottet oder von NPC-Crew-Figuren eingesammelt wird (FB 5.1).

**0.5 Wer zaehmt (MP):** wer ein Junges ZUERST fuettert, an den bindet es sich (`bond`); ab dann zaehlen nur seine Fuetterungen und
Streichler. Nach dem Zaehmen streichelt und fuettert nur der Besitzer. (Frage 3 in Abschnitt 11.)

**0.6 Namen:** Art `ncbearcub`, Gruppe `ncbear` (neu, endgueltig; der Erwachsene zieht bei B5a dorthin), Rasse `brown`, Register
`TrueCompanionsBears`, Befehlsmodul `BanditsNPCBear`, Log `[TC-BEAR]`, Marke am Tier `tcBear`, SP-Besitzerschluessel `__sp`,
Sandbox-Seite `BanditsNPC` (die Test-Mod bringt `Sandbox_BanditsNPC` = "NPC Crew" selbst mit, FB 3.2). Alle frei (FB 3.1).

**0.7 Aufteilung der Bauer (WICHTIG, weicht von "KERN = shared + server" in zwei Punkten ab, so wie die Bau-Auftraege es nennen):**
die drei ZEITAKTIONEN liegen in `shared/TimedActions/` (der Server braucht die Klasse), gebaut werden sie von der OBERFLAECHE; ihr
`complete()` ist eine Zeile und ruft den KERN. `sandbox-options.txt` baut die OBERFLAECHE (zusammen mit `Sandbox.json`), die Namen und
Vorgaben stehen fest in 3.1. Platzhalter-Modell und -Textur kopiert der ZUSAMMENBAU. Kein Bauer fasst eine Datei des anderen an.

**0.8 Nicht benutzt in B1a** (auch nicht hinter pcall): `setWild`, `addAcceptance`, `setDebugAcceptance`, `setDebugStress`,
`setIsInvincible`, `tryLure`/`eatFromLured`/`cancelLuring`, `pathToCharacter`, `pathToLocation`, `forceFleeFromChr`, `isAnimalMoving`
(0 Lua-Treffer, selbst gegreppt), `getCell():getAnimals()`, `transmitModData` am Tier, `getSteamID*`, `ItemTag.FISH_MEAT`,
`Events.OnCharacterDeath` (nur NC belegt; Tod wird ueber `isDead()` am gemerkten Objekt erkannt), `ModData.transmit`/`request` fuer das
Register (kein Client bekommt das Register), `LosUtil` auf dem Server, Vanillas `animal.add`, `feedFromHand`, `ISPetAnimal`,
`ISFeedAnimalFromHand`, `ISLureAnimal`.

**0.9 Die alten Dateien `NCBear*.lua`, die Art `bear` und `mod.info` werden nicht geaendert.** Einzige ueberschriebene Datei:
`Translate/EN/IG_UI.json` (alte 4 Schluessel unveraendert + neue, FB 2.3).

---

## 1. Spielablauf aus Sicht des Spielers

**Weg A, Wald**
1. Ich bin im oder am Wald unterwegs und habe keinen Baeren. Selten (Sandbox) erscheint 30-50 Kacheln entfernt, ausser Sicht, ein
   Junges. Ich lese kurz: "Du hoerst ein leises Wimmern aus dem Wald im Nordosten." (jede Spielstunde wieder, bis ich es gefunden habe).
2. Das Junge ist neugierig und kommt von selbst bis auf etwa 9 Kacheln heran, bleibt aber auf Abstand. Komme ich ohne Futter naeher
   als 6 Kacheln oder renne ich, laeuft es rund 12 Kacheln weg. Ueber ihm steht ein Balken "Zaehmung 0 % -- scheu".
3. Nehme ich Futter in die Hand (Fleisch, Fisch, Honig, Beeren, Obst, Eier, Nuesse, Insekten) und gehe langsam hin, bleibt es stehen
   und schaut. Bleibe ich stehen, kommt es bis auf 3 Kacheln heran ("Futter in der Hand lockt").
4. Rechtsklick auf das Junge -> "Fuettern" -> Futter waehlen: meine Figur beugt sich hinunter, das Junge frisst, genau ein Stueck ist
   weg. "+14 Vertrauen" (Honig/Fisch: "+21, das liebt es!"), der Balken waechst. Ab jetzt bleibt es in der Gegend (verschwindet nicht
   mehr) und laeuft vor mir nicht mehr weg.
5. Rechtsklick -> "Streicheln": der Balken waechst wieder. Abwechseln lohnt sich: nach dem Wechsel gibt es 50 % mehr ("es mag die
   Abwechslung"). Fuettern geht alle 2 Spielstunden, Streicheln jede Spielstunde; der Balken zeigt, wann es wieder geht.
6. Nach 3 bis 5 Fuetterungen mit Streicheln dazwischen ist der Balken voll: "Das Junge vertraut dir. Es gehoert jetzt dir!" Der
   Balken blinkt "Gezaehmt!" und verschwindet. Streicheln geht weiter (mit Abklingzeit), mit Futter in der Hand lockt man es mit.
7. Kuemmere ich mich nicht: ein nie gefuettertes Junges ist nach 36 Spielstunden ohne Kontakt weg ("... ist weitergezogen"), und zwar
   nie vor meinen Augen.

**Weg C, Koederplatz**
1. Mit Honig oder Fisch im Inventar: Rechtsklick auf Waldboden (oder bis 8 Kacheln neben dem Wald) -> "Baeren-Koeder auslegen" -> Stueck
   waehlen. Meine Figur legt es hin, das Stueck ist verbraucht, ueber der Stelle steht fuer mich "Baeren-Koeder (Honig) -- Nacht 0 von
   bis zu 3". Ein Koederplatz je Spieler.
2. Ich gehe weg (mindestens 20 Kacheln). Nach jeder Nacht wird gewuerfelt (40 %, 70 %, 100 %). Stehe ich beim Morgengrauen zu nah,
   zaehlt die Nacht nicht: "Etwas schleicht um den Koeder, traut sich aber nicht heraus, solange jemand in der Naehe ist."
3. Hat es geklappt und bin ich noch oder wieder mindestens 20 Kacheln weg, sitzt beim naechsten Hinkommen ein Junges am Platz ("Ein
   Baerenjunges hat deinen Koeder gefunden!") und bleibt dort in der Naehe. Dann weiter wie Weg A ab Schritt 2.

**Was ich sehe, wenn etwas nicht geht** (grauer Menuepunkt mit Erklaerung UND dieselbe Meldung, falls der Server ablehnt): "Es ist noch
satt. In etwa 2 Std. wieder." / "Es braucht eine Pause." / "Noch zu scheu zum Streicheln. Biete ihm zuerst Futter an." / "Dieses Junge
vertraut schon jemand anderem." / "Du hast schon einen Baeren." / "Du zaehmst schon ein anderes Junges." / "Du trauerst noch um deinen
Baeren (noch etwa N Tage)." / "Das frisst ein Baer nicht." / "Vor verdorbenem Futter dreht es sich weg." / "Das Junge ist weg." /
"Koeder wirkt nur im oder am Wald." / "Koeder muss draussen liegen." / "Du hast schon einen Koederplatz." Alle Texte in 6.2.8.

---

## 2. Zustaende des Jungen

Alle Zustaende rechnet der SCHREIBER (Einzelspieler: das eine Programm; Mehrspieler: der Server). Der Client zeigt nur an.
Lebende Zustaende stehen im Feld `st` des Register-Eintrags; Endzustaende loeschen den Eintrag.

| `st` | Bedeutung | Verhalten (Hirn-Takt, 7.) |
|---|---|---|
| `new` (erschienen) | erzeugt, noch kein Spieler war naeher als 15 Kacheln | neugierig: naehert sich dem Finder bis 9 Kacheln; Hinweis-Text je Spielstunde |
| `shy` (scheu) | entdeckt, nie gefuettert | flieht vor Spielern ohne Futter in der Hand und vor Rennenden (unter 6 Kacheln); bleibt stehen bzw. kommt bis 3 Kacheln, wenn jemand ruhig Futter haelt |
| `fed` (angefuettert) | mindestens einmal gefuettert, an `bond` gebunden, Balken unter 100 | bleibt im Umkreis von 10 Kacheln um seine Heimat (Ort der letzten Fuetterung); kommt zu `bond` mit Futter bis 2 Kacheln |
| `tame` (gezaehmt) | Balken voll, `owner` gesetzt | wie `fed`; mit Futter in der Hand lockt der Besitzer es mit, die Heimat wandert dabei mit |
| `missing` (vermisst) | nur gezaehmte: Tier trotz geladener Gegend nicht auffindbar | nichts; Platz bleibt 24 Stunden belegt |

| Von | Nach | Ausloeser | Wo gerechnet |
|---|---|---|---|
| - | `new` | Wald-Wurf gelingt und Platz gefunden (5.1) / Koeder reif, Kachel geladen, kein Spieler naeher als 20 (5.2) | Langsam-Takt / Hirn-Takt |
| `new` | `shy` | erster Spieler innerhalb 15 Kacheln (Meldung "Ein Baerenjunges!") | Hirn-Takt |
| `new`, `shy` | weg (verschwunden) | `idleH` >= Verschwinde-Frist (36 h, zaehlt nur, waehrend der Finder online ist) -> Marke `goneP`; vollzogen erst, wenn das Tier geladen ist und kein Spieler naeher als 25 Kacheln steht (SP zusaetzlich: Kachel nicht sichtbar); kommt vorher jemand in 15 Kacheln, faellt die Marke | Langsam-Takt setzt, Hirn-Takt vollzieht |
| `new`, `shy` | `fed` | erste gewertete Fuetterung: `bond` = Fuetternder, Heimat = Ort | `B.FeedComplete` |
| `fed` | `tame` | `tame` >= 100 UND `fedN` >= Mindest-Fuetterungen (3); `owner` = `bond` | `B.FeedComplete` / `B.PetComplete` |
| `fed` | `shy` | 168 h ohne Kontakt (nur Zeit, in der `bond` online ist): `bond` weg, `tame` halbiert, `idleH` = 0 -- damit kein Platz ewig belegt bleibt | Langsam-Takt |
| `tame` | `missing` | 3 Suchlaeufe hintereinander: Gegend geladen, Tier nicht da (kein `isDead` gesehen) | Hirn-Takt |
| `missing` | `tame` | Tier wiedergefunden (z. B. aus dem Anhaenger geladen: neues Objekt, ModData kopiert) | Hirn-Takt |
| `missing` | weg (verloren) | 24 h vermisst (Besitzer online): Platz frei, KEINE Sperre | Langsam-Takt |
| `new`, `shy`, `fed` | weg (verloren) | 3 Suchlaeufe ohne Fund bei geladener Gegend | Hirn-Takt |
| jeder | weg (tot) | `isDead()` am in dieser Sitzung gemerkten Objekt. War es `tame`: Sperre 7 Spieltage fuer den Besitzer. Sonst keine Sperre | Hirn-Takt |

Abklingzeiten laufen in Weltstunden und ueberleben Neustarts. "Kontakt" = irgendein Spieler innerhalb 15 Kacheln (bei `fed`: `bond`).
Nicht geladen ist kein eigener Zustand: der Eintrag bleibt, wie er ist; `idleH` laeuft weiter (ein unbeobachtetes Junges zieht weiter).

---

## 3. Zahlen

### 3.1 Sandbox-Optionen (Seite `BanditsNPC`; Namen fest, OBERFLAECHE schreibt Datei und Texte, KERN liest mit `B.Opt(name)`)

Form je Option wie NC `sandbox-options.txt:12-17` / `:155-161` (FE 12): `option BanditsNPC.<Name> { type = ..., page = BanditsNPC,
translation = BanditsNPC_<Name>, }`, enum zusaetzlich `numValues`, `valueTranslation = BanditsNPC_<Name>`. Nur C-Kommentare. `VERSION = 1,`
am Kopf. Texte `Sandbox_BanditsNPC_<Name>`, `..._tooltip`, enum `..._option1..5`. Alle Werte gelten im MP vom Server.

| Nr | Name (`BanditsNPC.` davor) | Typ | Bereich | Vorgabe | Wirkung | Herkunft |
|---|---|---|---|---|---|---|
| 1 | `BearCubsEnabled` | boolean | - | true | Hauptschalter: aus = keine neuen Jungen (Wald und Koeder); vorhandene bleiben zaehmbar | Vorschlag |
| 2 | `BearCubForestRate` | enum 5 | 1..5 | 3 | Haeufigkeit im Wald: 1 aus, 2 selten (2 % je Spielstunde), 3 normal (5 %), 4 oft (12 %), 5 sehr oft (30 %); gewuerfelt je 10 Spielminuten mit einem Sechstel davon | Vorschlag (ENT:150 "selten ... Sandbox-Haeufigkeit") |
| 3 | `BearCubMinDistance` | integer | 15..60 | 30 | Mindestabstand zu JEDEM Spieler beim Erscheinen (Bandits nimmt 35, FE 3) | Vorschlag |
| 4 | `BearCubMaxDistance` | integer | 20..65 | 50 | groesster Abstand zum Spieler, fuer den gewuerfelt wurde (Code klemmt auf mindestens Min + 5 und hoechstens 65: geladen sind 76) | Vorschlag |
| 5 | `BearCubWorldCap` | integer | 1..32 | 8 | hoechstens so viele UNGEZAEHMTE Junge gleichzeitig in der Welt | Deckel |
| 6 | `BearMaxPerPlayer` | integer | 1..4 | 1 | gezaehmte Baeren je Spieler | Kevin: einer (ENT:34); Option Vorschlag |
| 7 | `BearBaitEnabled` | boolean | - | true | Koederplatz an/aus | Vorschlag |
| 8 | `BearBaitNights` | integer | 1..7 | 3 | spaetestens nach so vielen (gezaehlten) Naechten ist der Koeder reif | Vorschlag "1 bis 3 Naechte" |
| 9 | `BearBaitFirstChance` | integer | 0..100 | 40 | Chance in der ersten Nacht in Prozent; steigt gleichmaessig bis 100 in der letzten (40 / 70 / 100) | Vorschlag |
| 10 | `BearTameFeedPoints` | integer | 1..100 | 14 | Balken-Punkte je Fuetterung | Vorschlag |
| 11 | `BearTamePetPoints` | integer | 0..100 | 8 | Balken-Punkte je Streicheln | Vorschlag |
| 12 | `BearTameMixBonus` | integer | 0..200 | 50 | Prozent mehr, wenn die vorige gewertete Handlung die ANDERE war (Mischung) | Kevin: Mischung zaehlt (ENT:104); Zahl Vorschlag |
| 13 | `BearTameFavoriteBonus` | integer | 0..200 | 50 | Prozent mehr fuer Lieblingsfutter (Honig, Fisch) | Vorschlag |
| 14 | `BearTameMinFeedings` | integer | 0..10 | 3 | so oft muss mindestens gefuettert sein, bevor der Balken voll werden kann (bis dahin bleibt er bei 99) | Kevin: "3-5 Mal fuettern" (ENT:41) |
| 15 | `BearFeedCooldownMinutes` | integer | 0..2880 | 120 | Spielminuten zwischen zwei gewerteten Fuetterungen desselben Jungen | Vorschlag |
| 16 | `BearPetCooldownMinutes` | integer | 0..2880 | 60 | Spielminuten zwischen zwei Streichlern (gilt auch nach dem Zaehmen, ENT:107) | Kevin: Cooldown; Zahl Vorschlag |
| 17 | `BearCubVanishHours` | integer | 0..240 | 36 | ungefuettert so viele Spielstunden ohne Kontakt -> verschwindet; 0 = nie | Vorschlag "1 bis 2 Spieltage" |
| 18 | `BearDeathLockDays` | integer | 0..60 | 7 | Spieltage nach dem Tod des eigenen Baeren ohne neues Junges | ENT:45 |
| 19 | `BearLog` | boolean | - | false | Diagnose-Zeilen `[TC-BEAR]` in die Konsole (echte Fehler laufen immer) | Regel Leistung |

`B.Opt(name)` liest mit nil-Rueckfall auf die Vorgabe (alte Spielstaende), prueft den Typ und klemmt auf den Bereich; ist NPC Crew
da, zur Laufzeit ueber `BanditsNPC.Opt(name, default)` (NC shared/BanditsNPC.lua:6101), sonst `SandboxVars.BanditsNPC[name]` (FE 12).

### 3.2 Was die Vorgaben ergeben (Rechnung fuer die Attrappe, 9.)

Punkte einer Handlung = Grundpunkte x Futterfaktor x Mischfaktor. Futterfaktor: Lieblingsfutter 1,5; normales Futter 1,0; Happen 0,5
(Naehrwert kleiner als 5, z. B. eine Grille) -- beim Streicheln 1,0. Mischfaktor 1,5, wenn `last` die andere Art war, sonst 1,0 (die
allererste Handlung hat keinen Bonus). Balken 0..100, eine Nachkommastelle, Anzeige abgerundet.

| Ablauf | Punkte | voll nach |
|---|---|---|
| Lieblingsfutter und Streicheln im Wechsel: F 21, S 12, F 31,5, S 12, F 31,5 | 108 | **3 Fuetterungen + 2 Streichler** |
| normales Futter und Streicheln im Wechsel: F 14, S 12, F 21, S 12, F 21, S 12, F 21 | 113 | **4 Fuetterungen + 3 Streichler** |
| normales Futter, nur zwei Streichler: F 14, S 12, F 21, F 14, F 14, F 14, S 12 | 101 | **5 Fuetterungen + 2 Streichler** |
| nur normales Futter (kein Streicheln): 8 x 14 | 112 | 8 Fuetterungen |
| nur Lieblingsfutter: 5 x 21 | 105 | 5 Fuetterungen |
| einmal fuettern, dann nur streicheln: 14, 12, dann je 8 | - | geht nicht voll: Mindest-Fuetterungen 3, der Balken haelt bei 99 |

Dauer mit den Abklingzeiten: Wechsel mit normalem Futter mindestens 6 Spielstunden (Fuetterungen bei 0, 2, 4, 6 h), mit Lieblingsfutter
4 Spielstunden. Das ist "ein Nachmittag im Spiel"; bei einstuendigen Tagen rund 15 echte Minuten.

### 3.3 Feste Stellwerte (Tabelle `B.CFG` in `shared/BanditsNPCBear.lua`; keine Sandbox, die Bench darf sie zur Laufzeit aendern)

| Feld | Wert | Bedeutung |
|---|---|---|
| `brainMs` / `idleMs` / `scanMs` | 1500 / 10000 / 5000 | Hirn-Takt bei lebenden Eintraegen / ohne / fruehester Abstand zweier Suchlaeufe (Echtzeit) |
| `shyDist` / `fleeDist` | 6 / 12 | Fluchtabstand eines scheuen Jungen / so weit laeuft es weg |
| `lureDist` / `comeUnfed` / `comeFed` | 15 / 3 / 2 | Futter in der Hand wirkt bis / so nah kommt ein scheues / ein angefuettertes oder zahmes |
| `curiousMin` / `curiousMax` / `curiousStop` / `curiousMs` | 12 / 45 / 9 / 60000 | Neugier: nur wenn der Finder so weit weg ist / haelt in diesem Abstand / hoechstens so oft |
| `contactDist` | 15 | Kontakt (haelt die Verschwinde-Uhr an) |
| `homeR` | 10 | Radius um die Heimat (angefuettert, zahm, Koeder-Junges) |
| `vanishKeep` | 25 | Verschwinden nur, wenn kein Spieler naeher ist |
| `baitKeep` / `baitAppear` / `baitEdge` / `baitApart` / `baitExtra` | 20 / 20 / 8 / 10 / 4 | Nacht zaehlt nur ohne Spieler in / Junges erscheint nur ohne Spieler in / Wald hoechstens so weit weg / Abstand zweier Plaetze / so viele ungezaehlte Morgen bis der Platz verfaellt |
| `hintH` | 1.0 | Hinweis "Wimmern" hoechstens je Spielstunde |
| `tellDist` | 60 | so nah bekommt ein Spieler die Daten eines Jungen geschickt |
| `moveMs` / `tries` | 3000 / 8 | fruehestens neuer Laufbefehl / Versuche bei der Platzsuche |
| `abandonH` / `missScans` / `missingH` | 168 / 3 / 24 | siehe Abschnitt 2 |
| `maxRecs` / `maxBaits` | 64 / 16 | harte Deckel des Registers |
| `snackBelow` / `snack` / `fav` | 0.05 / 0.5 / - | Happen: `getHungerChange() > -0.05`; Faktor |
| `forestRate` | { 0, 2, 5, 12, 30 } | Prozent je Spielstunde zu Option 2 |
| `feedTime` / `petTime` / `baitTime` | 150 / 150 / 100 | Dauer der Zeitaktionen (Vanilla: Fuettern 150, FE 8.3) |
| `petAnim` | "lamb" | Wert der Spieler-Variable `animal` beim Streicheln (Knoten `AnimSets/player/petanimal/petlamb.xml`); `"loot"` = Rueckfall Buecken |
| `barZ` / `hudDist` / `hudMax` / `menuFoods` | 0.55 / 20 / 6 / 12 | Anzeige: Hoehe ueber dem Tier / Reichweite / hoechstens so viele Balken / Futterzeilen im Menue |

---

## 4. Daten

### 4.1 Register (globale ModData `TrueCompanionsBears`, NUR beim Schreiber; FE 5.1)

Geholt mit `ModData.getOrCreate(B.KEY)`, fruehestens in `Events.OnInitGlobalModData` (bis dahin gibt `B.Reg()` nil und alles wartet).
Wird NIE uebertragen (`ModData.transmit` / `request` gibt es fuer diesen Schluessel nicht): kein Client erfaehrt fremde Zeilen, kein
Client kann es ueberschreiben. Nur Zahlen, Texte, Wahrheitswerte, Tabellen.

```
R = {
  v = 1,                 -- Schema
  n = 0,                 -- Zaehler fuer Kennungen der Tiere ("b1", "b2", ...)
  nb = 0,                -- Zaehler fuer Koederplaetze ("k1", ...)
  at = <Weltstunden>,    -- letzter Langsam-Takt (fuer dt)
  cubs = { [id] = rec },         -- Junge und spaeter erwachsene Baeren
  players = { [pkey] = prec },   -- nur Eintraege, die etwas tragen (Sperre)
  baits = { [bid] = bait },
}
rec = {
  id = "b7", kind = "cub",       -- spaeter "bear" (Wachsen aendert kind, nicht id)
  aid = <getAnimalID()>,         -- Gegenprobe und Wiederfinden nach dem Wachsen (neues Tier, gleiche AnimalID, ModData weg; FB B10)
  src = "forest" | "bait" | "found",
  st = "new" | "shy" | "fed" | "tame" | "missing",
  finder = pkey | nil,           -- fuer wen es erschien (belegt dessen "wildes Junges", solange bond nil ist)
  bond = pkey | nil,             -- wer zuerst gefuettert hat
  owner = pkey | nil,            -- gesetzt beim Zaehmen
  tame = 0..100, fedN = 0, petN = 0, last = "feed" | "pet" | nil,
  feedAt = <Weltstunden> | nil, petAt = <Weltstunden> | nil,
  born = <Weltstunden>, tamedAt = nil,
  idleH = 0,                     -- Stunden ohne Kontakt (nur gezaehlt, waehrend finder bzw. bond online ist)
  goneP = nil | true,            -- soll verschwinden (wartet auf "geladen und niemand in der Naehe")
  missN = 0, missH = 0,          -- Suchlaeufe ohne Fund / Stunden vermisst
  hintAt = nil,                  -- letzter Wimmer-Hinweis
  x, y, z,                       -- letzte bekannte Kachel
  hx, hy, hz,                    -- Heimat (Koederplatz bzw. Ort der letzten Fuetterung) | nil
  -- fuer spaeter vorgesehen, in B1a nie geschrieben: name, grow, trust, mood, cmd
}
prec = { lockUntil = <Weltstunden> | nil, tamedN = 0 }
bait = { id = "k3", owner = pkey, x, y, z, kind = "honey" | "fish", t0 = <Weltstunden>,
         nights = 0, miss = 0, wasNight = false, ready = false, warnAt = nil }
```

- **Plaetze je Spieler werden nie doppelt gefuehrt**, sondern aus `cubs`/`baits` gezaehlt (`B.SlotsOf(pkey, now)`, eine Antwort je
  Frage): `bears` = Eintraege mit `owner == pkey` (auch `missing`), `bonded` = id mit `bond == pkey` und `st == "fed"`, `wild` = id mit
  `finder == pkey` und `bond == nil`, `bait` = id, `lockUntil`.
- **Spielerschluessel** `B.PlayerKey(player)`: im MP (`isClient() or isServer()`) `player:getUsername()` (FE 5.3), im SP der feste Text
  `"__sp"` (nie der Charaktername). Geteilter Bildschirm im SP: alle lokalen Spieler teilen `"__sp"`.
- **Deckel:** `cubs` hoechstens 64 (darin ungezaehmte hoechstens Option 5), `baits` hoechstens 16 und einer je Spieler, `players` nur
  mit laufender Sperre (abgelaufene raeumt der Langsam-Takt).
- **Passt zum spaeteren Wachsen:** alles Wichtige steht unter `id`; das neue erwachsene Tier wird ueber `aid` wiedergefunden und neu
  gestempelt; der Balken lebt als `tame`/spaeter `trust` im selben Eintrag weiter (ENT:107); `kind` wechselt.

### 4.2 Spiegel am Tier (`animal:getModData().tcBear`, FE 5.2)

`{ id = rec.id, st = rec.st }` -- geschrieben nur vom Schreiber (`B.Commit`), nie mit `transmitModData`. Zweck: Wiederfinden nach
Laden/Anhaenger (die ModData wird mit dem Tier gespeichert und beim Anhaenger kopiert) und im SP die Zuordnung Tier -> Eintrag.
Der Schreiber liest daraus NUR die `id` und prueft sie gegen `rec.aid == animal:getAnimalID()` und die Art; Besitz, Balken, Zeiten
kommen nie aus dem Spiegel (jeder Client koennte ihn ueberschreiben, FB B3). `getModData()` erst NACH dem Art-Test rufen (legt sonst an
jedem fremden Tier eine Tabelle an).

### 4.3 Was der Client weiss (`B.View`, gefuellt von `B.ApplySync`)

Der Schreiber schickt jedem Spieler NUR seine Sicht: die Jungen in 60 Kacheln, dazu sein eigenes gebundenes/gezaehmtes, seinen
Koederplatz, seine Plaetze. Im SP wird dieselbe Tabelle direkt uebergeben. Felder heissen wie im Register, damit dieselben
Regel-Funktionen (`B.CheckFeed`, `B.CheckPet`) auf beiden Seiten rechnen. Genaue Form in 6.2.5.

---

## 5. Einzelspieler und Mehrspieler je Vorgang

Grundsatz: Dateien unter `server/` beginnen mit `if isClient() then return end` (V:server/Traps/STrapSystem.lua:1) -- sie laufen im
SP und auf dem dedizierten Server, auf einem MP-Client definieren sie nichts. Der Schreiber-Code ist in beiden Faellen DERSELBE.
SP-Test, wo noetig: `not isClient() and not isServer()`. Vom Schreiber zum Spieler: `B.SendView` / `B.Tell` -- auf dem Server
`sendServerCommand(player, B.CMD, ...)`, im SP der direkte Aufruf (`sendServerCommand` tut im SP nichts, FE 6). Vom Spieler zum
Schreiber: `B.Ask` -- auf dem MP-Client `sendClientCommand`, im SP der direkte Aufruf von `B.Handle`. Der Schreiber glaubt aus einer
Bitte nichts ausser der Benennung.

### 5.1 Erscheinen im Wald
- **Wer bittet:** niemand. **Wer prueft und tut:** Langsam-Takt des Schreibers (`Events.EveryTenMinutes`).
- Je Spieler (MP `getOnlinePlayers()`, SP `getSpecificPlayer(i)`): `B.MayAppear(slots, now)` (Schalter an, kein Baer, kein gebundenes,
  kein wildes Junges, keine Sperre, Welt-Deckel frei) -> wuerfeln (`ZombRand(10000) < Prozent x 100 / 6`) -> erst bei Erfolg
  `B.PickForestSquare`: bis 8 Zufallspunkte im Ring Min..Max um den Spieler (Form B:server/BanditServerSpawner.lua:216-222); Kachel
  geladen, z = 0, Waldzone (`getZonesAt`, Namen aus FE 3), draussen, frei, fester Boden, kein Wasser, kein Baum, kein Fahrzeug,
  Abstand zu ALLEN Spielern >= Min; im SP zusaetzlich `not sq:isCanSee(0)`. Kein Punkt -> nichts (kein Nachholen).
- `B.AppearFor(pkey, "forest", x, y, z)`: `addAnimal(getCell(), x, y, z, "ncbearcub", breed, false)` + `addToWorld()` (FE 1.1; Rasse
  wie `NCBearSpawn.lua:15-27` ueber `getAllAnimalsDefinitions()`), pruefen dass das Tier da ist (`isExistInTheWorld()`), Eintrag
  anlegen, stempeln, Hinweis-Meldung an den Finder mit Himmelsrichtung, Sicht schicken.
- **SP-Zweig:** derselbe Code im einen Programm; "ausser Sicht" zusaetzlich ueber `isCanSee`.
- **MP:** der Server erzeugt von sich aus (kein Client-Weg, kein `animal.add`, kein Kick). **Ehrliche Grenze:** ein Sichtfeld kennt der
  dedizierte Server nicht (FE 3) -- dort gilt nur der Mindestabstand; bei weit herausgezoomter Kamera kann ein Spieler das Auftauchen
  sehen. Steht im Changelog, kein Spielertext.
- **Rote Linien:** nichts haengt (kein Platz -> kein Junges, naechster Wurf in 10 Minuten); Deckel; nie jenseits 65 Kacheln.

### 5.2 Koederplatz
- **Auslegen -- wer bittet:** Client-Menue stellt die Zeitaktion `BanditsNPCBearBaitAction` an (vorher `transferIfNeeded`, hingehen
  mit `luautils.walkAdj`). **Wer prueft und tut:** `complete()` -> `B.BaitComplete(character, food, x, y, z)` beim Schreiber (im MP
  fragt der Server `isValid` nie, FE 8.2 -- ALLE Pruefungen stehen in `B.BaitComplete`): Schalter, Zahlen, Kachel geladen, Spieler
  hoechstens 3 Kacheln entfernt, draussen/frei, Wald oder Wald innerhalb 8 Kacheln, `B.CheckBait(slots)` (kein Baer, kein Junges, keine
  Sperre, kein eigener Platz, Deckel), kein anderer Platz naeher als 10, Stueck noch im Inventar DIESES Spielers und Koeder-Futter
  (Honig oder Fisch, nicht verdorben). Erst dann: nehmen (FE 8.3), Platz eintragen, Meldung, Sicht.
- **Naechte:** Langsam-Takt. Morgengrauen = `wasNight` war wahr und jetzt ist Tag (`getClimateManager():getSeason()` Dawn/Dusk gegen
  `getTimeOfDay()`, FE 4). Dann: steht ein Spieler innerhalb 20 Kacheln -> `miss + 1`, Hinweis an den Besitzer (hoechstens je Tag);
  sonst `nights + 1` und wuerfeln mit `B.BaitChance(nights)` -> `ready = true`. `miss >= 4` -> Platz verfaellt mit Meldung.
- **Erscheinen:** Hirn-Takt: Platz `ready`, Kachel geladen, naechster Spieler mindestens 20 Kacheln weg (SP: Kachel nicht sichtbar),
  Besitzer noch berechtigt (`B.MayAppear`) -> freie Kachel im Umkreis 2 suchen -> `B.AppearFor(owner, "bait", x, y, z)` mit Heimat =
  Platz; Platz loeschen. Ist der Besitzer nicht mehr berechtigt (hat inzwischen einen Baeren): Platz verfaellt mit Meldung.
- **Aufgeben -- wer bittet:** `B.Ask(player, "BaitDrop", { id = bid })`; der Schreiber prueft `bait.owner == pkey`, loescht, meldet.
  Der Koeder kommt nicht zurueck (steht im Tooltip des Menuepunkts).
- **SP-Zweig:** Zeitaktion laeuft ganz lokal, `complete()` nach `perform()`; `B.Ask` ruft `B.Handle` direkt.
- **Rote Linien:** Koeder genau einmal verbraucht (lehnt eine Pruefung ab: `return false`, nichts ist verbraucht; nach dem Nehmen wird
  der Platz im selben Aufruf eingetragen); kein Bodenscan frisst fremde Gegenstaende; reifer Platz haengt nicht still (Hinweis, Verfall).

### 5.3 Fuettern
- **Wer bittet:** Client-Menue: `transferIfNeeded`, ZUERST Futter in die Hand (`ISWorldObjectContextMenu.equip`), dann
  `luautils.walkAdj(player, animal:getSquare())`, dann `BanditsNPCBearFeedAction:new(player, animal, food)` in die Warteschlange
  (FE 8.2). Reihenfolge Hand vor Gehen ist Absicht: mit Futter in der Hand haelt der Hirn-Takt das Junge fest.
- **Wer prueft und tut:** `complete()` -> `B.FeedComplete(character, animal, food)` beim Schreiber, in dieser Reihenfolge und ohne
  Engine-Wurf dazwischen (Mehrfachrueckgaben vorher in Locals):
  1. Grund: Schreiber; `character`, `animal`, `food` nicht nil (im MP ist `food` das Stueck des SERVERS, FE 8.2); Art `ncbearcub`;
     `isExistInTheWorld()`, nicht `isDead()`; Abstand `character:getSquare():DistTo(animal:getSquare()) < 3` (V:ISPetAnimal.lua:6).
  2. Eintrag: `B.RecOf(animal)` (Spiegel-`id` -> Register, Gegenprobe `aid`; ein Junges ganz ohne Eintrag wird hier aufgenommen,
     `src = "found"`, wenn der Deckel es erlaubt).
  3. Regel: `B.CheckFeed(rec, pkey, slots, now)` (Bindung, Besitz, Plaetze, Sperre, Abklingzeit).
  4. Futter: `character:getInventory():contains(food)`; `B.FoodClass(food)` (erlaubt, nicht verdorben, nicht verbrannt).
  5. **Nehmen:** `removeFromHands(food)`, `getInventory():Remove(food)`, `sendRemoveItemFromContainer(inv, food)` (alle drei
     V:shared/Camping/TimedActions/ISAddFuelAction.lua:66-68); danach MUSS `contains(food)` falsch sein, sonst `B.Err` und `return false`.
  6. **Gutschreiben:** `B.ApplyGain(rec, pkey, "feed", class, now)`; Heimat = Kachel des Jungen; `idleH = 0`; `B.Commit(rec)`.
  7. Melden: `B.Tell` und Sicht an alle in 60 Kacheln. Punkte-Meldung: `Note_GainMix`, wenn gemischt, sonst `Note_GainFav` bei
     Lieblingsfutter, sonst `Note_Gain`; dazu bei der ersten Fuetterung `Note_FirstFed`, beim Zaehmen `Note_Tamed`, bei `need > 0`
     `Why_MoreFood`. `return true`.
  Lehnt Schritt 1-4 ab: Meldung mit Grund, `return false`, nichts verbraucht.
- **SP-Zweig:** `complete()` laeuft im selben Programm nach `perform()`; `B.Tell` ruft `B.ShowNote` direkt.
- **MP:** Bild, Ton, Fress-Animation spielt nur der Client; verbraucht und gutgeschrieben wird nur auf dem Server. **Ehrliche Grenze:**
  die Fress-Animation des Jungen (`NCBearAct = "eat"`) setzt der fuetternde Client an SEINER Kopie -- Mitspieler sehen das Junge still
  stehen (Anim-Variablen je Client, FB Falle 20).
- **Rote Linien:** Futter genau einmal (nehmen und gutschreiben in einem Aufruf, Gutschrift nur wenn das Stueck wirklich weg ist; kein
  Client entfernt etwas, FE 0.3); nichts haengt, wenn das Tier weg ist (Schritt 1 lehnt ab, die Sperre am Tier loest jeder Ausgang der
  Aktion und spaetestens der Hirn-Takt); kein Kick (Zeitaktion und `sendClientCommand` brauchen nur `LoginOnServer`).

### 5.4 Streicheln
- **Wer bittet:** Client-Menue: `walkAdj`, dann `BanditsNPCBearPetAction:new(player, animal)`.
- **Wer prueft und tut:** `B.PetComplete(character, animal)`: Schritte 1-3 wie oben mit `B.CheckPet` (ungefuettert -> "zu scheu";
  fremd gebunden -> abgelehnt; gezaehmt: nur der Besitzer; Abklingzeit), dann `B.ApplyGain(..., "pet", nil, now)`, dann
  `animal:petAnimal(character)` (V:ISPetAnimal.lua:70; hebt Akzeptanz, senkt Stress, gibt Tierhaltungs-XP; wirkt laut Jar nur bei
  abgelaufenem Vanilla-`petTimer` -- kein Fehler, wenn nicht), `B.Commit`, Meldung, Sicht. Am gezaehmten Jungen gibt es keine Punkte,
  nur Abklingzeit und die Meldung "Es geniesst das."
- **SP-Zweig / MP / rote Linien:** wie Fuettern (kein Gegenstand im Spiel).

### 5.5 Verschwinden, Tod, Vermisst
- **Wer tut:** nur der Schreiber. Verschwinden: `animal:getBehavior():setBlockMovement(false)`, `animal:remove()` (FE 1.3) -- nur bei
  geladenem Tier und ohne Spieler in 25 Kacheln; sonst bleibt `goneP` stehen. Eintrag loeschen, Meldung an Finder (falls online).
- Tod: Hirn-Takt sieht `isDead()` am gemerkten Objekt -> `B.OnCubDead(rec)`: Eintrag loeschen; war es `tame`: `prec.lockUntil = now +
  Tage x 24`, Meldung an den Besitzer. Die Leiche ist Sache der Engine (Zerlege-Eintrag `ncbearcubbrown` vorhanden).
- **SP-Zweig:** derselbe Code. **MP:** ein Client ruft nie `remove()` (sonst Geistertier, FE 1.3).
- **Rote Linien:** "Tier fehlt" ist nie "tot" (keine Sperre ohne gesehenes `isDead`); nichts haengt endlos (Vermisst-Frist, Aufgabe-Frist).
- **Nicht in B1a:** Schutz vor Waffen und Autos (Frage 4); Diebstahl per Anhaenger (PLAN 9). In B1a wird der Tod nur sauber verbucht.

### 5.6 Balken und Daten anzeigen
- **Wer bittet:** der Client einmal beim Start (`B.Ask(player, "Hello", {})`, im MP wiederholt alle 10 s, bis `B.View.ready`), und
  wenn er ein Junges ohne Daten anklickt (hoechstens alle 5 s).
- **Wer tut:** der Schreiber baut `B.BuildView(player)` und schickt sie: bei "Hello", nach jeder Aenderung an einem Jungen an alle
  Spieler in 60 Kacheln und an `finder`/`bond`/`owner`, und wenn ein Spieler neu in die 60 Kacheln eines Jungen kommt oder dessen
  OnlineID sich geaendert hat (Hirn-Takt, hoechstens eine Sendung je Spieler und Takt).
- Zuordnung Tier -> Daten beim Client `B.ViewOf(animal)`: zuerst der Spiegel (`getModData().tcBear.id`, im SP immer da), sonst die
  OnlineID (`B.View.byOid[animal:getOnlineID()]`, MP). Abklingzeiten rechnet der Client selbst aus `feedAt`/`petAt` und den
  Sandbox-Werten (im MP die des Servers) -- der Zeichner fragt nie den Server.
- **SP-Zweig:** `B.SendView` ruft `B.ApplySync` direkt. **MP ehrlich:** ob die OnlineID eines Tiers nach Entladen/Laden gleich bleibt,
  ist ungeprueft -- deshalb schickt der Server bei jeder Aenderung neu; schlimmster Fall ist ein Balken, der bis zu einem Takt fehlt.

### 5.7 Vanilla-Menue am Jungen
Die Definition laesst Aufheben (`canBePicked = false`), Anleinen (kein `canBeAttached`), Vanilla-Streicheln (kein `canBePet`), Feed/Water
(kein Hunger) weg. "Kill" (fuer nicht wilde Tiere, V:ISAnimalContextMenu.lua:307-324) blendet die OBERFLAECHE im Untermenue UNSERER Art
aus: `context:getOptionFromName(animal:getFullName())` -> `context:getSubMenu(opt.subOption)` -> `sub:removeOptionByName(getText(
"ContextMenu_KillAnimal"))` (FE 7.2). Das ist Menue-Hygiene, kein Schutz (ein veraenderter Client oder eine Waffe toetet weiter).

---

## 6. Dateien und Schnittstelle

### 6.1 Dateiliste (alles unter `_arbeit/baer_zaehmen/mod/`, spiegelt die Wurzel der Test-Mod)

| Nr | Pfad (`42/media/` davor) | Besitzer | Zweck | Zeilen etwa |
|---|---|---|---|---|
| 1 | `lua/shared/BanditsNPCBear.lua` | KERN | Modul, Konstanten, `B.CFG`, `B.OPTS`, Modus, Meldungen, Text, Sandbox, Spielerschluessel, Zeit, Wald-Frage (`B.FOREST`, `B.IsForestAt`, `B.NearForest`), Sicht (`B.View`, `B.ApplySync`, `B.ViewOf`), `B.Ask`, `B.Tell`, `B.SendView`, kleine reine Helfer | 420 |
| 2 | `lua/shared/BanditsNPCBearCrew.lua` | KERN | Naht-Datei: Tierpflege-Ausnahme in `Events.OnGameBoot` hinter Existenz-Riegel (12.2) | 50 |
| 3 | `lua/shared/BanditsNPCBearDefs.lua` | KERN | Tierart `ncbearcub`, Avatar, Zerlege-Teile (Dateiebene, 6.5) | 120 |
| 4 | `lua/shared/BanditsNPCBearFood.lua` | KERN | Futter erkennen: `B.FoodClass`, `B.IsBaitFood`, `B.FoodList` | 160 |
| 5 | `lua/shared/BanditsNPCBearRules.lua` | KERN | reine Regeln ohne Engine: Punkte, Pruefungen, Zustandswechsel, Koeder-Chance, Verschwinde-Schritt, `B.Decide` | 450 |
| 6 | `lua/server/BanditsNPCBearRegistry.lua` | KERN | Register: Eintraege, Plaetze, Deckel, Spiegel, Sicht bauen | 400 |
| 7 | `lua/server/BanditsNPCBearServer.lua` | KERN | Takte, `OnClientCommand`, `B.Handle`, `B.FeedComplete`/`PetComplete`/`BaitComplete`, Wald-Wurf, Koeder, Verschwinden, Tod | 520 |
| 8 | `lua/server/BanditsNPCBearWorld.lua` | KERN | Engine-Seite: Spielerliste, Tier erzeugen/finden/entfernen, Kachel- und Waldpruefung, Halten und Laufen | 450 |
| 9 | `scripts/nc_bear_cub.txt` | KERN | `module Base`: `animationsMesh NCBearCub`, `model NCBearCub_Body` (Form `nc_bear_tier.txt:3-15`) | 16 |
| 10 | `lua/shared/TimedActions/BanditsNPCBearFeedAction.lua` | OBERFLAECHE | Zeitaktion Fuettern (globale Klasse) | 110 |
| 11 | `lua/shared/TimedActions/BanditsNPCBearPetAction.lua` | OBERFLAECHE | Zeitaktion Streicheln | 110 |
| 12 | `lua/shared/TimedActions/BanditsNPCBearBaitAction.lua` | OBERFLAECHE | Zeitaktion Koeder auslegen | 90 |
| 13 | `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `OnServerCommand` (Sync, Note), "Hello", `B.ShowNote`, Zeit-Texte | 220 |
| 14 | `lua/client/BanditsNPCBearMenu.lua` | OBERFLAECHE | Tier-Menue (Fuettern, Streicheln, Stand, "Kill" ausblenden), Welt-Menue (Koeder auslegen/aufgeben) | 420 |
| 15 | `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | Zaehm-Balken ueber dem Jungen, Koeder-Schild | 360 |
| 16 | `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | Testhilfe (Abschnitt 8), wird nie kopiert | 300 |
| 17 | `lua/shared/Translate/<L>/UI.json` x 7 | OBERFLAECHE | `UI_BN_Bear_*` (6.2.8) | - |
| 18 | `lua/shared/Translate/<L>/Sandbox.json` x 7 | OBERFLAECHE | `Sandbox_BanditsNPC` + Optionstexte | - |
| 19 | `lua/shared/Translate/<L>/IG_UI.json` x 7 | OBERFLAECHE | Tiernamen (6.2.9); EN ueberschreibt die vorhandene Datei, alte 4 Schluessel bleiben wortgleich | - |
| 20 | `sandbox-options.txt` | OBERFLAECHE | 19 Optionen aus 3.1 | 140 |
| 21 | `models_X/Skinned/NCBearCub.glb`, `textures/Body/NCBearCub.png` | ZUSAMMENBAU | Platzhalter aus `_arbeit/baer_baby/entwurf/` (MD5 notieren; das endgueltige Modell aus baer-junges ersetzt sie unter denselben Namen) | - |

Sprachen `<L>`: EN, PTBR, RU, KO, ES, CN, FR. Berichte: `bau_kern.md`, `bau_oberflaeche.md`, Abweichungen sofort nach
`schnittstelle_aenderungen.md`. Attrappen: `attrappe/kern/`, `attrappe/ober/`, `attrappe/gesamt/`.

**Locals-Haushalt:** Grenze 200 je Funktion (mit `-debug` die Summe aller je angelegten), ab 180 teilen. Ziel hier: Hauptblock jeder
Datei hoechstens 60 Locals, jede Funktion hoechstens 100; `B.FeedComplete`, `B.BrainTick`, das Tier-Menue und `prerender` des Balkens
frueh in Helfer teilen. `localcount.py` auf jede Datei, beide Zahlen in den Bericht.

**Kopf jeder Lua-Datei:** `BanditsNPC = BanditsNPC or {}` / `BanditsNPC.Bear = BanditsNPC.Bear or {}` / `local B = BanditsNPC.Bear`.
Auf Dateiebene wird kein anderes Modul und keine Funktion einer anderen Datei eingefangen (Ladefolge: `shared` vor `client` vor
`server`, darin alphabetisch); jeder Griff zur Laufzeit, fremde Module (`BanditsNPC.Livestock`, `BanditsNPC.Opt`, `BanditsNPC.Log`)
hinter Existenz-Riegel. Mit und ohne NPC Crew und Bandits muss alles laufen.

### 6.2 Schnittstelle (WOERTLICH einhalten; Abweichung -> `schnittstelle_aenderungen.md`)

#### 6.2.1 Konstanten (KERN, Datei 1)
`B.KEY = "TrueCompanionsBears"`, `B.CMD = "BanditsNPCBear"`, `B.CUB = "ncbearcub"`, `B.BREED = "brown"`, `B.GROUP = "ncbear"`,
`B.MARK = "tcBear"`, `B.SP_KEY = "__sp"`, `B.ACT = "NCBearAct"` (Anim-Variable am Tier), `B.CFG` (3.3), `B.OPTS` (Name -> `{ def, min,
max }` aus 3.1), `B.LogOn` (Wahrheitswert, Vorgabe false; die Bench darf ihn setzen).

#### 6.2.2 Funktionen des KERNs, die ueberall da sind (shared; die OBERFLAECHE darf sie rufen)

| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.IsSP()` / `B.IsWriter()` | boolean | `not isClient() and not isServer()` / `not isClient()` |
| `B.Log(msg)` / `B.Err(msg)` / `B.ErrEvery(key, ms, msg)` | - | Log nur bei `B.LogOn`, Option `BearLog` oder `BanditsNPC.DIAG`; Err immer; Form `TT BanditsNPCTurret.lua:90-135` |
| `B.T(key, fallback, a1, a2, a3)` | Text | `getText` mit bis zu drei Einsetzungen; gibt es den Schluessel nicht, der englische Ersatztext mit `%1..%3` ersetzt |
| `B.Opt(name)` | Wert | 3.1 |
| `B.PlayerKey(player)` | Text | 4.1 |
| `B.Now()` | Zahl | Weltstunden |
| `B.FoodClass(item)` | `"fav"` / `"ok"` / `"snack"` / nil, whyKey | nil + `"UI_BN_Bear_Why_NotFood"` oder `"UI_BN_Bear_Why_Rotten"` |
| `B.IsBaitFood(item)` | boolean, `"honey"` / `"fish"` | nur Klasse `fav`, nicht verdorben |
| `B.FoodList(player, max)` | Liste `{ item, class, name, count }` | Lieblingsfutter zuerst, je Anzeigename eine Zeile, hoechstens `max`; nur Client |
| `B.CheckFeed(rec, pkey, slots, now)` | ok, whyKey, whyVal | rein; `rec` darf Register- oder Sicht-Eintrag sein |
| `B.CheckPet(rec, pkey, slots, now)` | ok, whyKey, whyVal | rein |
| `B.CheckBait(slots)` | ok, whyKey, whyVal | rein |
| `B.MayAppear(slots, now)` | ok, whyKey, whyVal | rein: Schalter an, kein Baer, kein gebundenes, kein wildes Junges, keine Sperre |
| `B.Gain(kind, class, last)` | Punkte, mixed | rein; `kind` = `"feed"` / `"pet"` (3.2) |
| `B.ApplyGain(rec, pkey, kind, class, now)` | `{ gain, mixed, first, tamed, need }` | rein, aendert `rec`: Punkte, Zaehler, `last`, Zeit, erste Fuetterung (`bond`, `st = "fed"`), ruft `B.TameCheck`; `need` = fehlende Fuetterungen, wenn der Balken bei 99 haelt; am zahmen Jungen `gain = 0` |
| `B.TameCheck(rec, now)` | boolean | rein: `tame >= 100` und `fedN >=` Mindest-Fuetterungen -> `st = "tame"`, `owner = bond`, `tamedAt`; sonst `tame` hoechstens 99 |
| `B.BaitChance(night)` | Prozent | rein (3.1 Nr. 8, 9) |
| `B.VanishStep(rec, dtH, contact, relevantOnline)` | `"keep"` / `"go"` / `"release"` | rein: fuehrt `idleH`; `"go"` = Verschwinde-Frist um (nur `new`/`shy`), `"release"` = Aufgabe-Frist um (nur `fed`) |
| `B.Decide(c, env)` | `{ act, tx, ty, lead }` | rein (6.7) |
| `B.WaitLeft(rec, kind, now)` | Stunden (0 = bereit) | rein; Rest der Abklingzeit fuer `"feed"` / `"pet"` (fuer Balken und Tooltip) |
| `B.WaitParts(hours)` | n, unitKey | unter 1 h Minuten (aufgerundet auf 5), sonst Stunden (aufgerundet); `unitKey` = `UI_BN_Bear_Time_Minutes` / `_Hours` |
| `B.IsForestAt(x, y, z)` / `B.NearForest(x, y, z, r)` | boolean | Datei 1; `getZonesAt` + `zone:getType()` gegen die Menge `B.FOREST` (Forest, DeepForest, PHForest, PHMixForest, PRForest, FarmMixForest, FarmForest, BirchForest, BirchMixForest, OrganicForest; FE 3); `NearForest` prueft die Kachel und 8 Punkte im Abstand `r`. Auch der Client darf sie rufen (Vorpruefung im Koeder-Menue) |
| `B.Tell(player, note)` / `B.SendView(player, payload)` | - | Schreiber -> Spieler: auf dem Server `sendServerCommand(player, B.CMD, "Note" / "Sync", ...)`, im SP direkt `B.ShowNote` / `B.ApplySync`; ruft nur der KERN |
| `B.DirOf(dx, dy)` | `"N"`, `"NE"`, `"E"`, `"SE"`, `"S"`, `"SW"`, `"W"`, `"NW"` | rein; Welt-Achsen: -y = Norden, +x = Osten |
| `B.View` | Tabelle | 6.2.5; nur lesen |
| `B.ApplySync(payload)` | - | fuellt `B.View` an Ort und Stelle (Referenz bleibt), ruft danach `B.OnView()` falls vorhanden |
| `B.ViewOf(animal)` | Sicht-Eintrag oder nil | 5.6; prueft zuerst die Art |
| `B.Ask(player, command, args)` | - | MP-Client: `sendClientCommand(player, B.CMD, command, args)`; SP: `B.Handle(player, command, args)` |

`whyVal` ist bei Wartezeiten die Reststunden (Zahl), bei der Sperre die Resttage (Zahl, aufgerundet), sonst nil.

#### 6.2.3 Funktionen des KERNs nur beim Schreiber (server-Dateien; die OBERFLAECHE ruft davon nur die drei `...Complete`; die Bench
darf im SP alle rufen)

| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.FeedComplete(character, animal, food)` | boolean | 5.3; meldet und schickt selbst |
| `B.PetComplete(character, animal)` | boolean | 5.4 |
| `B.BaitComplete(character, food, x, y, z)` | boolean | 5.2 |
| `B.Handle(player, command, args)` | - | Bitten "Hello", "BaitDrop" |
| `B.Reg()` | Register oder nil | nil vor `OnInitGlobalModData` |
| `B.SlotsOf(pkey, now)` | slots | 6.2.5 `me` |
| `B.AppearFor(pkey, src, x, y, z)` | rec oder nil, why | der EINE Weg, ein Junges in die Welt zu setzen (Wald-Wurf, Koeder; die Bench ruft ihn auch) |
| `B.RecOf(animal)` | rec oder nil, why | |
| `B.FindAnimal(rec)` | IsoAnimal oder nil | gemerktes Objekt mit Gegenprobe, sonst nil (der naechste Suchlauf findet es) |
| `B.NearestRec(player, radius)` | rec, animal | fuer Meldungen und Bench |
| `B.Commit(rec)` | - | klemmt, schreibt den Spiegel, merkt "geaendert" (Sicht geht im selben oder naechsten Takt raus) |
| `B.Close(rec, how)` | - | `how` = `"vanish"`, `"dead"`, `"lost"`, `"clean"`; loescht den Eintrag, setzt bei `"dead"` + `tame` die Sperre, meldet |
| `B.RemoveCub(animal)` | - | Sperre loesen, `animal:remove()` |
| `B.SlowTick()` / `B.BrainTick(force)` | - | die Takte; `force` ueberspringt nur die Echtzeit-Drossel |
| `B.BaitDawn(bait, now)` | - | ein Morgen fuer diesen Platz (wuerfelt nach Regel) |
| `B.PushView(player)` | - | Sicht bauen und schicken |
| `B.Players()` | Liste `{ p, key, x, y, z }` | Datei 8; MP `getOnlinePlayers()`, SP lokale Spieler |
| `B.CreateCub(x, y, z)` | IsoAnimal oder nil, why | Datei 8; einzige Stelle mit `addAnimal` |
| `B.SquareFits(sq)` | boolean, why | Datei 8: geladen, draussen, frei, fester Boden, kein Wasser, kein Baum, kein Fahrzeug |
| `B.PickForestSquare(player, players)` | Kachel oder nil | Datei 8 (5.1) |
| `B.Hold(rec, animal, on)` / `B.MoveTo(rec, animal, x, y, z)` | - / boolean | Datei 8 (6.7) |

Auf einem MP-Client sind diese Felder nil. Die Zeitaktionen rufen deshalb so: `local f = BanditsNPC.Bear.FeedComplete` /
`if not f then return false end` / `return f(self.character, self.animal, self.food)`.

#### 6.2.4 Funktionen der OBERFLAECHE, die der KERN ruft (nur im SP direkt; im MP kommen sie ueber `OnServerCommand`)

| Funktion | Datei | Bemerkung |
|---|---|---|
| `B.ShowNote(player, note)` | `client/BanditsNPCBearClient.lua` | zeigt eine Meldung (6.2.6); der KERN ruft `if B.ShowNote then B.ShowNote(player, note) end` |
| `B.OnView()` | `client/ISUI/BanditsNPCBearHud.lua` | wahlfrei: Balken-Liste sofort neu bauen |

#### 6.2.5 Sicht (`B.View`, Nutzlast von "Sync")

```
payload = {
  me = { key = pkey, on = <BearCubsEnabled>, bears = n, maxBears = n, bonded = id|nil, wild = id|nil, bait = bid|nil,
         lockUntil = <Weltstunden>|0 },
  cubs = { { id, oid = <OnlineID oder -1>, st, tame, fedN, petN, last, feedAt, petAt, bond, owner, src }, ... },   -- Liste
  bait = { id, x, y, z, kind, nights, max = <BearBaitNights>, ready = bool } | nil,
}
B.View = { ready = bool, me = {...}, cubs = { [id] = eintrag }, byOid = { [oid] = id }, bait = {...}|nil }
```
`me` hat genau die Form von `slots` (Rueckgabe von `B.SlotsOf`): die Regel-Funktionen bekommen beim Client `B.View.me`. Fehlende
Zeiten sind nil (nie 0). `bond`/`owner` sind Spielerschluessel (im MP Benutzernamen: oeffentlich). Nur Zahlen, Texte, Wahrheitswerte,
Tabellen (FE 6).

#### 6.2.6 Befehle (Modul `BanditsNPCBear`)

| Richtung | Befehl | Felder | Antwort |
|---|---|---|---|
| Client -> Schreiber | `Hello` | `{}` | `Sync` |
| Client -> Schreiber | `BaitDrop` | `{ id = bid }` | `Note` + `Sync` |
| Schreiber -> Client | `Sync` | payload 6.2.5 | - |
| Schreiber -> Client | `Note` | `{ k = Textschluessel, t = "wait" / "days" / "dir" / "num" / "name" / nil, v = Wert, tone = "good" / "bad" / nil }` | - |

`Note`: `t = "wait"`: `v` = Stunden -> `%1` = Dauer-Text (`B.WaitParts` + `B.T`); `"days"`: `v` = Tage; `"dir"`: `v` = Richtungskuerzel ->
`%1` = `B.T("UI_BN_Bear_Dir_" .. v)`; `"num"`: `v` = Punkte, abgerundet; `"name"`: `v` = Text. Anzeige: `tone` good ->
`HaloTextHelper.addGoodText(player, text)`, bad -> `addBadText`, sonst `addText` (FE 11; `addGoodText` V:client/ServerCommands.lua:183).
Server-Handler beginnt mit `if module ~= B.CMD then return end`, `if isClient() then return end`, `if type(args) ~= "table" then return end`.
Fuettern, Streicheln, Koeder auslegen sind KEINE Befehle, sondern Zeitaktionen.

#### 6.2.7 Zeitaktionen (OBERFLAECHE; Pflichten aus FE 8.2)

Jede Klasse ist eine GLOBALE Variable mit genau dem Namen ihres Typs; die Parameter von `new` heissen wie die Felder.

| Klasse | `new(...)` | `complete()` |
|---|---|---|
| `BanditsNPCBearFeedAction` | `(character, animal, food)` | `B.FeedComplete(self.character, self.animal, self.food)` |
| `BanditsNPCBearPetAction` | `(character, animal)` | `B.PetComplete(self.character, self.animal)` |
| `BanditsNPCBearBaitAction` | `(character, food, x, y, z)` | `B.BaitComplete(self.character, self.food, self.x, self.y, self.z)` |

- Kopf `require "TimedActions/ISBaseTimedAction"`, `X = ISBaseTimedAction:derive("X")`, `o.maxTime = o:getDuration()`,
  `stopOnWalk`/`stopOnRun` wahr, `getDuration` wie V:ISFeedAnimalFromHand.lua:53-58 mit `B.CFG.feedTime` usw.
- `isValid` (nur Client/SP, billig): Tier da und nicht tot, Abstand unter 3, Futter im Inventar (`contains`). Die echten Pruefungen
  macht `complete()` ueber den KERN.
- Fuettern `start`: `setActionAnim(self.animal:getFeedByHandAnim())` (Definition: `"AnimalLureLow"`), `setOverrideHandModels(self.food,
  nil)`, `faceThisObject`, `self.animal:getBehavior():setBlockMovement(true)`, `self.animal:setVariable(B.ACT, "eat")` (Knoten
  `AnimSets/buck/idle/NCBear_Eat.xml` der Test-Mod), Ton `playSound("GiveFoodAnimal")` -- alles Form V:ISFeedAnimalFromHand.lua:13-25.
  JEDER Ausgang (`stop`, `forceStop`, `perform`) loest die Sperre, loescht die Variable (`clearVariable`, V:ISPetAnimal.lua:48) und
  stoppt den Ton.
- Streicheln `start`: Form V:ISPetAnimal.lua:20-44, aber `AnimalSizeX` 0.01 und `AnimalSizeY` FEST 0.5 (nie die Vanilla-Division),
  `self.character:setVariable("animal", B.CFG.petAnim)`, `petanimal` wahr; bei `B.CFG.petAnim == "loot"` stattdessen
  `setActionAnim("Loot")` + `SetVariable("LootPosition", "Low")` (V:shared/Camping/TimedActions/ISAddFuelAction.lua:41-42). Dauer fest
  (`B.CFG.petTime`), KEIN `animEvent`, kein `emulateAnimEventOnce` -- gewertet wird einmal in `complete()`. Jeder Ausgang: `petanimal`
  falsch, Sperre loesen.
- Koeder `start`: `setActionAnim("Loot")`, `SetVariable("LootPosition", "Low")`, `reportEvent("EventLootItem")` (ebenda :41-43).
- `useProgressBar` bleibt an (Balken der Aktion ueber dem Spieler).

#### 6.2.8 Textschluessel `UI_BN_Bear_*` (in allen sieben `UI.json`; der KERN verwendet NUR diese Schluessel in `Note` und als whyKey)

Englischer Ausgangstext in Klammern; `%1` ist die Einsetzung; ein woertliches Prozent ist `%%`.

Meldungen des Schreibers (whyKey / Note):
`Why_Gone` (The cub is gone.) - `Why_Far` (You are too far away.) - `Why_FeedWait` (It is still full. Try again in about %1.) -
`Why_PetWait` (It wants a break. Try again in about %1.) - `Why_Shy` (It is still too shy to be petted. Offer it food first.) -
`Why_Other` (This cub already trusts someone else.) - `Why_NotOwner` (Only its owner can do that.) - `Why_HasBear` (You already have a
bear.) - `Why_HasCub` (You are already taming another cub.) - `Why_Locked` (You are still mourning your bear. A new cub will trust you
in about %1 day(s).) - `Why_NotFood` (A bear will not eat that.) - `Why_Rotten` (It turns away from spoiled food.) - `Why_NoItem` (You
no longer have that food.) - `Why_Full` (There are too many wild cubs around right now.) - `Why_Off` (Bear cubs are switched off in the
sandbox settings.) - `Why_MoreFood` (It still wants to be fed %1 more time(s) before it fully trusts you.) -
`Note_Heard` (You hear a faint whimpering from the forest to the %1.) - `Note_Seen` (A bear cub! It looks lost and hungry.) -
`Note_Gain` (+%1 trust) - `Note_GainMix` (+%1 trust - it likes the change!) - `Note_GainFav` (+%1 trust - it loves this!) -
`Note_FirstFed` (It ate from your hand. It will stay around here now.) - `Note_Tamed` (The cub trusts you. It is yours now!) -
`Note_Happy` (It enjoys that.) - `Note_Vanished` (The bear cub has wandered off.) - `Note_Dead` (The bear cub is dead.) -
`Note_BearDead` (Your bear is dead. A new cub will trust you in %1 day(s) at the earliest.) - `Note_Missing` (You have lost track of
your bear.) - `Note_Back` (Your bear is back.) - `Note_Abandoned` (The cub has stopped waiting for you.) -
`Bait_Placed` (Bait laid out. Come back after a night or two - and keep your distance.) - `Bait_NotForest` (Bait only works in or right
next to a forest.) - `Bait_Inside` (Bait has to lie outdoors on free ground.) - `Bait_HasOne` (You already have a bait spot.) -
`Bait_TooClose` (Another bait spot is too close.) - `Bait_BadFood` (Only honey or fish lures a bear cub.) - `Bait_Near` (Something is
circling the bait but will not come out while people are close.) - `Bait_Came` (A bear cub has found your bait!) - `Bait_Expired` (The
bait is gone. No cub came.) - `Bait_Dropped` (Bait spot given up.) - `Bait_Off` (Bear bait is switched off in the sandbox settings.)
Richtungen: `Dir_N` (north) `Dir_NE` (north-east) `Dir_E` (east) `Dir_SE` (south-east) `Dir_S` (south) `Dir_SW` (south-west) `Dir_W`
(west) `Dir_NW` (north-west).

Nur OBERFLAECHE (Menue, Balken):
`Menu_Feed` (Feed) - `Menu_Pet` (Pet) - `Menu_NoFood` (You carry nothing a bear would eat: meat, fish, honey, berries, fruit, eggs, nuts
or insects.) - `Menu_Bait` (Lay out bear bait) - `Menu_BaitTip` (The bait is used up. A cub may come after one to three nights.) -
`Menu_BaitDrop` (Give up bait spot) - `Menu_BaitDropTip` (The bait will not come back.) - `Food_Fav` (%1 - loves it) - `Food_Ok` (%1) -
`Food_Snack` (%1 - only a nibble) - `Time_Minutes` (%1 min) - `Time_Hours` (%1 h) - `Hud_Taming` (Taming %1%%) - `Hud_Shy` (shy) -
`Hud_Feed` (Food: %1) - `Hud_Pet` (Petting: %1) - `Hud_Ready` (ready) - `Hud_Tamed` (Tamed!) - `Hud_Other` (trusts %1) -
`Hud_Bait` (Bear bait (%1)) - `Hud_BaitNight` (night %1 of up to %2) - `Hud_BaitReady` (something was here) - `Bait_Honey` (honey) -
`Bait_Fish` (fish) - `Tip_Mix` (Taking turns between feeding and petting earns more trust.)

Regeln: Schluessel ohne die Woerter spawn, debug, bench, cheat, test; EN-Texte ebenso ("appear" statt "spawn"); EN `singleplayer` /
`multiplayer` zusammen; Platzhalter in allen Sprachen gleich; CN nur Zeichen aus Vanilla-CN (belegen); Round-Trip
`json.dumps(data, indent=4, ensure_ascii=False) + "\n"`, sortiert, UTF-8 ohne BOM, LF. Menue-Eintraege im Code nur ueber `B.T("UI_BN_...",
"englischer Ersatz", ...)` oder `getText`, nie fester Text.

#### 6.2.9 Tiernamen `IG_UI.json` und Sandbox-Texte
- Neu in allen sieben Sprachen: `IGUI_AnimalType_ncbearcub` (EN "Bear cub"), `IGUI_Animal_Group_ncbear` (EN "Bear"),
  `IGUI_Breed_brown` (EN "Brown", steht in EN schon). Nur in EN bleiben die drei alten Test-Namen `IGUI_AnimalType_bear`,
  `IGUI_AnimalType_bearstag`, `IGUI_Animal_Group_bear` wortgleich stehen (Alt-Schluessel bis B5a, 12.1 Punkt 8).
- `Sandbox.json`: `Sandbox_BanditsNPC` = "NPC Crew" (in allen sieben wortgleich), je Option `Sandbox_BanditsNPC_<Name>` und
  `..._tooltip`, fuer Option 2 `Sandbox_BanditsNPC_BearCubForestRate_option1..5` (off / rare / normal / often / very often).

### 6.3 Engine-Aufrufe und ihr Beleg

Jeder Aufruf steht in `forschung_engine.md`; der Bauer liest die Stelle selbst nach und nennt sie im Kommentar. Was hier und dort
fehlt, wird nicht benutzt. "Nachbeleg" = nicht in FE, am 10.11. vom Planer in den heutigen Dateien gelesen.

| Zweck | Aufruf | Beleg | Seite |
|---|---|---|---|
| Tier erzeugen | `addAnimal(getCell(), x, y, z, typ, breed, false)`, `animal:addToWorld()`; Rasse `getAllAnimalsDefinitions()` / `def:getAnimalType()` / `def:getBreeds():get(0)` | FE 1.1 | Schreiber |
| Tier finden | `getCell():getObjectListForLua()`, `instanceof(o, "IsoAnimal")`, `o:getAnimalType()`, `getAnimalID()`, `getOnlineID()`, `getModData()` | FE 1.2, 5.2 | Schreiber, Client |
| lebt, da | `animal:isDead()`, `animal:isExistInTheWorld()` | FE 1.2, 13 | beide |
| Ort | `animal:getX()`, `getY()`, `getZ()`, `animal:getSquare()` | Nachbeleg V:shared/Definitions/animal/ButcheringUtil.lua:575-576, V:client/TimedActions/ISContextualActions.lua:100; FE 8.1 | beide |
| entfernen | `animal:remove()` | FE 1.3 | Schreiber |
| halten, laufen | `animal:getBehavior():setBlockMovement(b)`, `animal:fleeTo(sq)` | FE 2, 8.2 | Schreiber (halten auch in den Aktionen wie Vanilla) |
| Anim am Tier | `animal:setVariable(name, text)`, `animal:clearVariable(name)` | FE 8.1 (V:ISPetAnimal.lua:43, :48) | Client/SP |
| Streicheln zaehlt | `animal:petAnimal(character)` | FE 8.1, 10 | Schreiber, in `complete` |
| Zone, Kachel | `getWorld():getMetaGrid():getZonesAt(x, y, z)`, `zone:getType()`, `getCell():getGridSquare`, `isFree(false)`, `TreatAsSolidFloor()`, `getFloor():hasProperty(IsoFlagType.water)`, `HasTree()`, `isOutside()`, `isVehicleIntersecting()`, `isCanSee(nr)` (nur SP) | FE 3 | Schreiber; Zone auch Client |
| Spieler | `getOnlinePlayers()` (+ `:size()`, `:get(i)`), `getSpecificPlayer(i)`, `getNumActivePlayers()`, `p:getX()`..., `p:getUsername()`, `p:isDead()` | FE 3, 5.3, 11 | Schreiber |
| Hand, Tempo | `p:getPrimaryHandItem()`; `p:isRunning()`, `p:isSprinting()` | Nachbeleg V:server/BuildingObjects/ISEmptyGraves.lua:18 (Hand, Server-Ordner), V:ISAnimalContextMenu.lua:93; B:shared/PlayerDamageModel.lua:81, B:shared/BanditUtils.lua:320, V:client/Foraging/ISBaseIcon.lua:702 | Schreiber |
| Zeit | `getGameTime():getWorldAgeHours()`, `:getTimeOfDay()`, `getClimateManager():getSeason()`, `:getDawn()`, `:getDusk()`, `getTimestampMs()` | FE 4 | alle |
| Takte | `Events.EveryTenMinutes.Add`, `Events.OnTick.Add`, `Events.OnInitGlobalModData.Add`, `Events.OnGameBoot.Add` | FE 4, 5.1; OnGameBoot V:client/Foraging/ISSearchManager.lua:1481 | Schreiber / Naht |
| Register | `ModData.getOrCreate(name)` | FE 5.1 | Schreiber |
| Netz | `sendClientCommand(p, mod, cmd, args)`, `Events.OnClientCommand.Add`, `sendServerCommand(p, mod, cmd, args)`, `Events.OnServerCommand.Add` | FE 6 | je Seite |
| Wuerfel | `ZombRand(n)`, `ZombRandFloat(a, b)` | V:shared/TimedActions/Animals/ISMilkAnimal.lua:25; FE 3 | Schreiber |
| Futter | `instanceof(item, "Food")`, `getFullType()`, `getFoodType()`, `getHungerChange()`, `isRotten()`, `isBurnt()`, `getDisplayName()`, `Fishing.fishes[i].itemType`, `getInventory():getAllEvalRecurse(fn)` | FE 9.1 | beide; Liste nur Client |
| verbrauchen | `inv:contains(item)`, `character:removeFromHands(item)`, `inv:Remove(item)`, `sendRemoveItemFromContainer(inv, item)` | FE 8.3 | Schreiber, in `complete` |
| Aktion | `ISBaseTimedAction:derive`, `setActionAnim`, `setOverrideHandModels`, `faceThisObject`, `shouldBeTurning`, `playSound`, `getEmitter():stopOrTriggerSound`, `isTimedActionInstant`, `getFeedByHandAnim()`, `character:setVariable(...)`, `SetVariable("LootPosition", "Low")`, `reportEvent` | FE 8.1-8.3; Nachbeleg V:shared/Camping/TimedActions/ISAddFuelAction.lua:41-43; Wert `"AnimalLureLow"` V:shared/Definitions/animal/DeerDefinitions.lua:92 | Client/SP |
| anstellen | `luautils.walkAdj(p, sq)`, `ISTimedActionQueue.add`, `ISWorldObjectContextMenu.transferIfNeeded`, `.equip(p, p:getPrimaryHandItem(), item, true, false)` | FE 8.2 | Client |
| Menue | `Events.OnClickedAnimalForContext.Add(f(player, context, animals, test))`, `Events.OnFillWorldObjectContextMenu.Add`, `context:addOption`, `ISContextMenu:getNew`, `addSubMenu`, `getOptionFromName`, `getSubMenu`, `removeOptionByName`, `option.notAvailable`, `ISWorldObjectContextMenu.addToolTip()`, `tooltip:setName`, `iconTexture`, `ISWorldObjectContextMenu.setTest()` | FE 7.1-7.2; Nachbeleg V:ISAnimalContextMenu.lua:149-150 (Untermenue), :310 (`ContextMenu_KillAnimal`), V:client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81 (setTest) | Client |
| Anzeige | `ISPanel:derive`, `addToUIManager`, `isoToScreenX/Y(nr, x, y, z)`, `drawTextCentre`, `drawRect`, `drawRectBorder`, `getTextManager():getFontHeight(UIFont.Small)`, `HaloTextHelper.addText/addGoodText/addBadText`, `Events.OnGameStart.Add` | FE 11 | Client |
| Sandbox, Text | `SandboxVars.BanditsNPC`, `getText(key, ...)` | FE 12 | alle |

Unbelegt auf dem dedizierten Server (gleiche Java-Methode, in Vanilla nur Client/SP gerufen), deshalb MP-Testpunkte und KEIN pcall als
Tarnkappe: `getCell():getObjectListForLua()`, `isFree`/`getFloor` am Server. Faellt eines davon im MP-Test, wird der Weg ersetzt.

### 6.4 Regeln fuer beide Bauer

- **Woerter, die in Code, Strings, Datei-, Options-, Text- und Befehlsnamen der `BanditsNPCBear*`-Dateien NICHT vorkommen duerfen**
  (das Uebernahme-Skript bricht sonst ab, `turret_uebernahme.py:122-152`): `spawn`, `debug` (in jeder Schreibweise, auch als Teil eines
  Methodennamens), `bench`, `cheat`, `test` als eigener Name (`Test`, `TEST`), `Dbg`, `godmode`; kein `_G`, keine globale Funktion,
  keine `Capability.`/Admin-Frage, kein Tasten- oder Maus-Ereignis, kein `AddItem`/`instanceItem`, kein `print("[NCBear] ...")`, kein
  `NCBear_...`-Name. Meldungen nur ueber `B.Log`/`B.Err`. Erlaubte globale Namen: die drei Aktionsklassen (Engine verlangt es) und die
  Vanilla-Tabellen `AnimalDefinitions`, `AnimalAvatarDefinition`, `AnimalPartsDefinitions`.
- **Tier erzeugen und entfernen nur in je EINER Funktion:** `addAnimal(` nur in `B.CreateCub` (Datei 8), gerufen nur von `B.AppearFor`
  (Datei 7); `animal:remove()` nur in `B.RemoveCub` (Datei 8). `B.AppearFor` rufen im Kern nur der Wald-Wurf und der Koeder.
- **Dateiform:** LF, reines ASCII, kein BOM, keine Zeile endet mit `\` (mit Python an den Bytes pruefen). Kahlua: kein `next`, kein
  `%a`, Mehrfachrueckgaben erst in Locals, `and` kappt Mehrfachrueckgaben.
- **Jeder Engine-Aufruf mit Fundstelle im Kommentar.** NPC Crew ist kein Beleg. Kein pcall um einen unbelegten Aufruf.
- Pruefer auf jede Lua-Datei: `luacheck.py`, `scopecheck.py`, `localcount.py`, `luacheck_pz.py`.

### 6.5 Tierart `ncbearcub` (KERN, Datei 3; Form `NCBearDefs.lua:62-127`, auf Dateiebene, weil Java die Tabelle erst in `IsoWorld.init` liest)

| Feld | Wert | Grund |
|---|---|---|
| `bodyModel` / `animset` / `group` | `"NCBearCub_Body"` / `"buck"` / `"ncbear"` | Auftrag; gleiche 15 Clip-Namen wie der Erwachsene |
| `stages` | `{ ncbearcub = { ageToGrow = 60 } }`, kein `nextStage` | Wachsen ist B1b; ohne `nextStage` kein Stufenwechsel (FB 2.3) |
| `breeds.brown` | `name = "brown"`, `texture` = `textureMale` = `textureBaby` = `"NCBearCub"`, Symbole wie `NCBearDefs.lua:42-47`, `sounds = { fallover = { name = "AnimalFoleyBuckBodyfall" } }` | `textureBaby` allein wirkt ohne `nextStage` nicht (FB 2.3); keine Erwachsenen-Stimme am Jungen |
| `genes` | wie `NCBearDefs.lua:16-26` (ohne `maxSize`) | |
| `minSize` = `maxSize` | 0.35 | Kevin (ENT:8); das GLB ist bei 1,0 gebaut |
| `animalSize` / `collisionSize` / `shadoww` / `shadowfm` / `shadowbm` | 0.1 / 0.24 / 0.4 / 0.8 / 0.8 | nach dem Kitz (V:DeerDefinitions.lua:65-70); ungespielt |
| `minWeight` / `maxWeight` / `corpseSize` / `minBlood` / `maxBlood` / `trailerBaseSize` | 8 / 20 / 1.0 / 200 / 500 / 100 | Vorschlag (Kitz: 15-100, 1.5, 200-600, 100) |
| `wild` / `canBeDomesticated` | false / false | 0.1 |
| `alwaysFleeHumans` / `fleeZombies` | false / false | Scheu spielt unser Takt; `fleeZombies` = der Wert, den NPC Crew ohnehin setzt (FB N2) |
| `canBePicked` / `canThump` / `canBeAlerted` / `sitRandomly` / `needMom` | false / false / false / false / false | wie der Erwachsene; `needMom` V:ChickenDefinitions.lua:127 |
| `canBePet`, `canBeFeedByHand`, `canBeAttached`, `hungerMultiplier`, `thirstMultiplier` | weglassen | Vorgabe false bzw. 0: kein Vanilla-Streicheln (auch NPC Crews Tierpflegerin streichelt dann nie), kein Anleinen, kein Hunger |
| `feedByHandAnim` | `"AnimalLureLow"` | Haltung der Figur beim Fuettern |
| `male` / `dontAttackOtherMale` / `wanderMul` / `idleTypeNbr` / `spottingDist` | true / true / 600 / 0 / 10 | wie der Erwachsene |

Dazu `AnimalAvatarDefinition["ncbearcub"]` (Felder von `"buck"` wie `NCBearDefs.lua:106-121`, ohne `hook`; Pflicht fuer "Animal info"
und NPC Crews Portrait) und `AnimalPartsDefinitions.animals["ncbearcubbrown"] = AnimalPartsDefinitions.animals["fawnwhitetailed"]`
(V:shared/Definitions/animal/AnimalPartsDefinitions.lua:456-465). Der Artname ist ab dem ersten Kopierzug endgueltig (ein
gespeichertes Tier unbekannter Art bricht das Laden).

### 6.6 Futterklassen (KERN, Datei 4)

`fav`: `getFullType() == "Base.Honey"`; Typ in der Menge aus `Fishing.fishes` (einmal beim ersten Gebrauch gebaut, hinter Riegel
`Fishing and Fishing.fishes`); `getFoodType() == "Fish"`. `ok`: `getFoodType()` in { Meat, Beef, Poultry, Game, Venison, Bacon,
Sausage, Seafood, Egg, Fruits, Citrus, Berry, Nut, Insect, Roe } (Werte am 10.11. aus `food.txt` gezaehlt; der Bauer prueft die Liste
nach). `snack`: Klasse `ok`, aber `getHungerChange() > -B.CFG.snackBelow`. Immer noetig: `instanceof(item, "Food")`,
`getHungerChange() < 0`, sonst nil + `Why_NotFood`; `isRotten()` oder `isBurnt()` -> nil + `Why_Rotten`. Honig ist ein Gewuerz: KEIN
`isSpice`-Filter. Ein angebrochenes Stueck zaehlt als ganzes Stueck. Skala von `getHungerChange()` (Skriptwert / 100?) gegen
`dec/Food.java:1713` und eine Vanilla-Zeile pruefen.

### 6.7 Verhalten `B.Decide(c, env)` (KERN, Datei 5, rein)

`c` = `{ st, src, x, y, hx, hy, held, sinceMoveMs, sinceCuriousMs }`. `env` = `{ near = P|nil, lure = P|nil, mate = P|nil }` mit
`P` = `{ key, x, y, dist, food, fast, still }`: `near` = naechster Spieler ueberhaupt; `lure` = naechster Spieler mit Futter in der Hand,
nicht schnell, hoechstens `lureDist` (bei `fed`/`tame` zaehlt nur `bond`/`owner`); `mate` = `finder` bzw. `bond`/`owner`, falls online
und hoechstens 70 Kacheln weg. `food` = `B.FoodClass(p:getPrimaryHandItem()) ~= nil`, `fast` = `isRunning() or isSprinting()`, `still` =
Ort seit dem letzten Takt um weniger als 0,3 Kacheln geaendert. Rueckgabe `{ act, tx, ty, lead }`, erste passende Regel gewinnt:

| Nr | Zustand | Bedingung | `act` |
|---|---|---|---|
| 1 | `new`, `shy` | `near.dist <= shyDist` und (`not near.food` oder `near.fast`) | `flee`: Punkt `fleeDist` vom Spieler weg |
| 2 | `new`, `shy` | `lure` und `lure.still` und `lure.dist > comeUnfed` | `come`: Punkt `comeUnfed` vor dem Spieler |
| 3 | `new`, `shy` | `lure` | `hold` |
| 4 | `new`, `shy` | `hx` gesetzt (Koeder-Junges) und Abstand zur Heimat > `homeR` | `home` |
| 5 | `new`, `shy` | `hx` nil, `mate` mit `curiousMin < dist <= curiousMax`, `sinceCuriousMs >= curiousMs` | `come`: Punkt `curiousStop` vor `mate` |
| 6 | `fed`, `tame` | `lure` und `lure.still` und `lure.dist > comeFed` | `come`: Punkt `comeFed` vor dem Spieler; bei `tame` `lead = true` (Heimat = Ziel) |
| 7 | `fed`, `tame` | `lure` und `lure.dist <= shyDist` | `hold` |
| 8 | `fed`, `tame` | Abstand zur Heimat > `homeR` | `home` |
| 9 | alle | sonst | `free` (Sperre loesen, falls von uns gesetzt; die Engine laesst es wandern) |

Ausfuehren (Datei 8): `hold` -> `setBlockMovement(true)` (jeden Takt neu, die Engine loest von selbst); `flee`/`come`/`home` -> Sperre
loesen, Zielkachel `getCell():getGridSquare(tx, ty, z)`, nil oder Wasser -> bis 4 gedrehte Ersatzpunkte, dann nichts; `fleeTo(sq)`;
derselbe Befehl fruehestens nach `moveMs`. Gegenprobe: hat sich das Tier 3 Takte nach einem Laufbefehl nicht bewegt, eine
`B.ErrEvery`-Zeile (Diagnose, kein Abbruch). `missing` und nicht geladene Junge: nichts.

### 6.8 Menue und Anzeige (OBERFLAECHE)

**Tier-Menue** (`Events.OnClickedAnimalForContext`, Datei 14): bei `test` wie Vanilla frueh zurueck (`ISWorldObjectContextMenu.setTest()`).
Je angeklicktem Tier der Art `B.CUB`: Vanillas Untermenue suchen (`getOptionFromName(animal:getFullName())`, `getSubMenu`); fehlt es,
die eigenen Punkte auf die oberste Ebene. Darin:
- "Kill" entfernen (5.7).
- `Menu_Feed` mit Untermenue aus `B.FoodList(player, B.CFG.menuFoods)`: je Zeile `Food_Fav` / `Food_Ok` / `Food_Snack` mit dem
  Anzeigenamen; Klick stellt 5.3 an. Leere Liste: grauer Punkt mit Tooltip `Menu_NoFood`.
- `Menu_Pet` (Symbol `media/ui/AnimalActions_Pet.png`); Klick stellt 5.4 an.
- Vorpruefung mit `v = B.ViewOf(animal)`, `B.CheckFeed(v, key, B.View.me, B.Now())` bzw. `B.CheckPet`: bei Ablehnung Punkt grau
  (`notAvailable`) mit dem Grund als Tooltip. Tooltip der freien Punkte: `Hud_Taming` mit Prozent, `Tip_Mix`. Kennt der Client das
  Junge nicht (`v == nil`), bleiben die Punkte frei (der Schreiber entscheidet) und "Hello" wird nachgefragt.
**Welt-Menue** (`Events.OnFillWorldObjectContextMenu`, Datei 14): nur wenn der Spieler Koeder-Futter traegt (`B.IsBaitFood`) UND die
Kachel `B.NearForest(x, y, z, B.CFG.baitEdge)` erfuellt (sonst kein Eintrag: kein Menue-Muell in der Stadt) -- Ausnahme: traegt er
Honig/Fisch in der Hand, erscheint der Punkt immer, ausserhalb des Waldes grau mit `Bait_NotForest`. `Menu_Bait` mit Untermenue (je
Koeder-Stueck eine Zeile, Tooltip `Menu_BaitTip`); Vorpruefung `B.CheckBait(B.View.me)`. Hat er einen Platz und klickt in 3 Kacheln
davon: `Menu_BaitDrop` (Tooltip `Menu_BaitDropTip`) -> `B.Ask(player, "BaitDrop", { id = ... })`.
**Balken** (Datei 15; Vorbild `NC:client/ISUI/BanditsNPCNameTags.lua:1145-1191`, FE 11): ein 1 x 1-`ISPanel`, angelegt in
`Events.OnGameStart`, zeichnet in `prerender`, wird nie unsichtbar geschaltet, Maus-Funktionen geben false. Liste alle 1000 ms neu:
Tiere der Art `B.CUB` in `B.CFG.hudDist` mit Sicht-Eintrag, die naechsten `B.CFG.hudMax`. Je Bild und Eintrag: Objekt gegenpruefen
(`isExistInTheWorld()`), Punkt `isoToScreenX/Y(nr, x, y, z + B.CFG.barZ)`, dann:
- ungezaehmt (`new`, `shy`, `fed`): Rahmen 64 x 7, Fuellung `tame / 100`, darueber `Hud_Taming`; bei `new`/`shy` dahinter `Hud_Shy`;
  ist es an jemand anderen gebunden: `Hud_Other` statt der zweiten Zeile; sonst zweite Zeile klein `Hud_Feed` und `Hud_Pet` mit
  `Hud_Ready` oder der Restzeit (`B.WaitLeft` + `B.WaitParts`).
- gerade gezaehmt (Wechsel nach `tame` gesehen): 5 Sekunden `Hud_Tamed`, danach nichts mehr.
- eigener Koederplatz in 25 Kacheln: ueber der Kachel `Hud_Bait` mit `Bait_Honey`/`Bait_Fish`, darunter `Hud_BaitNight` oder
  `Hud_BaitReady`.
Bei mehr als einem lokalen Spieler wird nichts gezeichnet. Kein Server-Zugriff, keine Suche je Bild.

---

## 7. Leistung

| Was | Wie oft | Deckel |
|---|---|---|
| Langsam-Takt (`EveryTenMinutes`): Wald-Wurf je Spieler, Koeder-Morgen, `idleH`, Aufgabe, Vermisst-Frist, Sperren raeumen, Hinweise | alle 10 Spielminuten | je Spieler ein Wurf; Platzsuche (8 Versuche) nur nach gelungenem Wurf; Eintraege <= 64, Plaetze <= 16 |
| Hirn-Takt (`OnTick` + `getTimestampMs`): Verhalten, Kontakt, Tod, Verschwinden vollziehen, reife Koeder, Sicht verschicken | alle 1500 ms, wenn es lebende Eintraege oder reife Plaetze gibt; sonst nur ein Zaehlervergleich alle 10 s | je Junges: Abstand zu jedem Spieler (reine Rechnung), Hand/Tempo nur fuer Spieler in 15 Kacheln; hoechstens ein Laufbefehl je 3 s und Junges |
| Suchlauf `getObjectListForLua()` (kopiert die Liste) | nur wenn ein Eintrag kein gemerktes Objekt hat UND seine letzte Kachel geladen ist; fruehestens alle 5 s | ein Lauf loest alle Eintraege auf |
| Sicht verschicken | bei Aenderung; hoechstens eine je Spieler und Takt | Nutzlast <= 16 Junge |
| Client: Balken-Liste | alle 1000 ms neu, nur wenn `B.View` Junge oder einen Koeder kennt | hoechstens 6 Balken, 20 Kacheln |
| Client: Zeichnen | je Bild nur aus der fertigen Liste: je Balken 2 Umrechnungen, 2 Rechtecke, 1 Rahmen, 2 Texte | 1 x 1-Panel, nie unsichtbar geschaltet, bei mehr als einem lokalen Spieler nichts |
| Client: Menue | nur beim Rechtsklick; Futterliste hoechstens 12 Zeilen | - |

Nichts laeuft je Bild ausser dem Zeichnen. Nichts spricht Kacheln jenseits 65 an. Objekte werden nur innerhalb der Sitzung gemerkt und
jedes Mal gegengeprueft. Diagnose: `B.Log` (Schalter `BearLog`, `B.LogOn`, oder NPC Crews Crew logging); `B.Err` immer; wiederholte
Fehler ueber `B.ErrEvery`. Log-Zeilen nennen Vorgang, id, Spieler, Grund (z. B. `[TC-BEAR] feed b7 Kevin +21 mix tame 47.0`).

---

## 8. Bench (`client/NCBearBenchCub.lua`, OBERFLAECHE; wird nie kopiert)

Nur Einzelspieler (im MP druckt jeder Befehl "singleplayer only" -- MP testet man ueber die Sandbox-Werte, 10.2). Die Bench ruft
dieselben Kern-Funktionen wie das echte Spiel (6.2.3) und aendert sonst nur Register-Felder; der Kern kennt die Bench nicht. Einhaengen
ins vorhandene Rechtsklick-Untermenue "NC Bear" ueber `NCBearMenu.extra` (`NCBearTest.lua:132-134`), ohne alte Dateien zu aendern.

| Befehl | Tut | Weg |
|---|---|---|
| `NCBear_CubHere(n)` | Junges `n` Kacheln (Vorgabe 8) neben mir erscheinen lassen | `B.AppearFor(B.PlayerKey(p), "forest", x, y, z)` -- dieselben Regeln (habe ich schon einen Baeren, lehnt es mit Grund ab) |
| `NCBear_CubFood()` | 2 Honig, 3 Barsche, 3 Steaks ins Inventar | `getInventory():AddItem("Base.X")` (V:client/DebugUIs/Scenarios/AiteronScenario.lua:74) |
| `NCBear_CubTame(x)` | Balken des naechsten Jungen auf `x` (0..100); bei 100 gilt es als fertig gezaehmt | Felder setzen (`tame = x`; bei 100 zusaetzlich `bond` = ich, `st = "fed"`, `fedN` mindestens die Mindest-Fuetterungen), dann die echte Regel `B.TameCheck(rec, now)` und `B.Commit(rec)` |
| `NCBear_CubSkip(h)` | `h` Spielstunden ueberspringen: Abklingzeiten, Verschwinde-Uhr, Sperre, Vermisst-Uhr | Felder verschieben (`feedAt`/`petAt`/`lockUntil` - h, `idleH`/`missH` + h), dann `B.SlowTick()` und `B.BrainTick(true)` |
| `NCBear_CubNight(force)` | ein Morgen fuer meinen Koederplatz | `B.BaitDawn(bait, now)`; `force` setzt `ready = true` |
| `NCBear_CubInfo()` | Zustand drucken: Sandbox-Werte, meine Plaetze, alle Eintraege mit Abstand, Koeder, `B.View` | nur lesen |
| `NCBear_CubKill()` | naechstes Junges toeten (Tod und Sperre pruefen) | `animal:setHealth(0)` (V:shared/TimedActions/Animals/ISKillAnimal.lua:58) |
| `NCBear_CubClean()` | alle Jungen in der geladenen Gegend entfernen, Register leeren (auch Koeder und Sperren) | je Eintrag `B.Close(rec, "clean")` + `B.RemoveCub`; Tiere ohne Eintrag ueber die Objektliste |
| `NCBear_CubLog(on)` | Diagnose an/aus | `B.LogOn` |
| `NCBear_CubSet(feld, wert)` | einen Stellwert aus `B.CFG` aendern (z. B. `barZ`, `petAnim`, `shyDist`) | Tabelle |

Menue-Eintraege (englisch, fest): "Cub: appear near me", "Cub: give food", "Cub: skip 2 hours", "Cub: info", "Cub: clean up".

---

## 9. Attrappen-Test (lua5.1 ohne Spiel)

Kahlua ist kein echtes 5.1; der Test beweist Logik, nicht Engine-Verhalten. Aufbau: `attrappe/kern/run.lua` legt Attrappen an
(`Events` mit `Add`, das die Funktion merkt; `isClient`/`isServer` umschaltbar; `getGameTime`, `getClimateManager`, `getTimestampMs` mit
stellbarer Uhr; `ModData.getOrCreate` als Tabelle; `SandboxVars`; `ZombRand` mit fester Folge; `getText` gibt den Schluessel;
`sendServerCommand`/`sendClientCommand` schreiben in eine Liste; Spieler-, Tier-, Inventar-, Kachel-Attrappen mit genau den Methoden
aus 6.3) und laedt die Kern-Dateien mit `dofile` in Ladefolge. Engine-Zugriffe des Kerns laufen ueber wenige Funktionen (Datei 8:
`B.Players`, `B.CreateCub`, `B.RemoveCub`, `B.SquareFits`, `B.MoveTo`, `B.Hold`; Datei 1: `B.IsForestAt`, `B.Now`), die der Test
ersetzen kann.

Pflichtfaelle KERN (`attrappe/kern/`):
1. Punkte: die sechs Ablaeufe aus 3.2 ergeben genau die Zahlen und die Zahl der Fuetterungen; Mindest-Fuetterungen halten bei 99.
2. Abklingzeiten: zweite Fuetterung vor Ablauf wird abgelehnt mit `Why_FeedWait` und Reststunden; nach Ablauf angenommen; ebenso Streicheln.
3. Zustandswechsel: jede Zeile der Tabelle in Abschnitt 2 einmal (inklusive `fed` -> `shy` nach 168 h, `missing` hin und zurueck).
4. Futter genau einmal: Inventar-Attrappe zaehlt `Remove`; abgelehnte Fuetterung (jede Ablehnung aus 5.3 Schritt 1-4) -> 0 Entnahmen,
   0 Punkte; angenommene -> genau 1 Entnahme; `Remove` wirkt nicht (Attrappe behaelt das Stueck) -> keine Gutschrift, `false`.
5. Koeder: Chance 40/70/100; Nacht mit Spieler in der Naehe zaehlt nicht; Verfall nach 4; Stueck genau einmal verbraucht; zweiter
   Platz abgelehnt; reifer Platz erzeugt erst bei Abstand >= 20.
6. Plaetze: Spieler mit Baer, mit gebundenem Jungen, mit wildem Jungen, mit Sperre bekommt kein neues; Welt-Deckel; 64er-Deckel.
7. Verschwinden: `idleH` laeuft nur, wenn der Finder online ist; Kontakt setzt zurueck; vollzogen nur ohne Spieler in 25 Kacheln.
8. Tod: `tame` -> Sperre 7 x 24 h; `fed` -> keine; "fehlt" ohne `isDead` -> nie Sperre.
9. SP und MP: mit `isClient = false, isServer = false` gehen `B.Tell`/`B.SendView` direkt an `B.ShowNote`/`B.ApplySync`, kein Eintrag in
   der Sende-Liste; mit `isServer = true` genau ein `sendServerCommand` je Meldung; mit `isClient = true` definieren die server-Dateien
   nichts und `B.Ask` sendet. Spielerschluessel: SP `"__sp"`, MP Benutzername.
10. `B.Decide`: jede der neun Regeln mit einem treffenden und einem knapp nicht treffenden Fall.
11. Nutzlast: `B.BuildView` enthaelt nur Zahl/Text/Wahrheitswert/Tabelle, keine Funktion, kein Objekt; `B.CheckFeed` gibt auf dem
    Register-Eintrag und auf dem daraus gebauten Sicht-Eintrag dieselbe Antwort.
12. Kein `next(`, kein `%a` in den Dateien (grep im Testlauf).

OBERFLAECHE (`attrappe/ober/`): mit einer EIGENEN Kern-Attrappe nach 6.2 (die Kern-Dateien entstehen gleichzeitig; nicht auf sie
warten): Dateien laden ohne Fehler (UI-Attrappen), `B.ShowNote` baut fuer jede Note-Art den richtigen Text,
`B.WaitParts`-Anzeige, Menue-Aufbau gegen eine Kontext-Attrappe (graue Punkte bei Ablehnung, "Kill" entfernt), JSON: sieben Sprachen,
gleiche Schluessel, Platzhalter gleich, Round-Trip, jeder Schluessel aus 6.2.8 vorhanden und jeder im Code benutzte Schluessel in der
Liste. GESAMT (`attrappe/gesamt/`, Zusammenbau): ein Junges von Erscheinen ueber vier Fuetterungen und drei Streichler bis `tame`, einmal
im SP-Modus und einmal als Server mit Client-Attrappe; danach Tod und Sperre.

---

## 10. Kevins Test im Spiel

Vorher: Wegwerf-Spielstand (ein gespeichertes Junges bricht den Spielstand ohne die Mod), Spiel neu starten, `bugwatch.py` mitlaufen
lassen. Im SP zuerst. Was zuerst angesehen wird, weil ungespielt (FE O8): steht das Junge nach Speichern/Laden wieder da; erscheint
der Rechtsklick am Jungen; sieht das Streicheln aus der Naehe gut aus.

### 10.1 Einzelspieler (12 Schritte)
1. Neuer Spielstand mit NCBearTest (einmal ohne, spaeter einmal mit NPC Crew). Sandbox-Seite "NPC Crew": die Baeren-Zeilen sind da.
   Erwartet: laedt ohne rote Fehler.
2. In einen Wald gehen. Konsole `NCBear_CubFood()`, dann `NCBear_CubHere()`. Erwartet: ein kleines Baerenjunges 8 Kacheln entfernt,
   Meldung "Ein Baerenjunges!", Balken "Zaehmung 0 % -- scheu".
3. Ohne Futter in der Hand hinrennen. Erwartet: es laeuft ein Stueck weg, haelt Abstand.
4. Fisch in die Hand, langsam hingehen, stehenbleiben. Erwartet: es bleibt stehen und kommt bis auf etwa 3 Kacheln.
5. Rechtsklick aufs Junge -> "Fuettern" -> Fisch. Erwartet: Figur beugt sich, Junges frisst, GENAU ein Fisch fehlt, "+21 Vertrauen -
   das liebt es!", "bleibt jetzt hier", Balken 21 %.
6. Rechtsklick -> "Streicheln". Erwartet: Figur streichelt (Haltung ansehen!), "+12 - es mag die Abwechslung", Balken 33 %.
7. Sofort noch einmal fuettern. Erwartet: Punkt grau mit "noch satt, in etwa 2 Std."; kein Fisch weg. Dann `NCBear_CubSkip(2)`.
8. Fuettern und Streicheln wiederholen, bis der Balken voll ist. Erwartet: nach der 3. Fuetterung (Fisch) "Es gehoert jetzt dir!",
   Balken blinkt "Gezaehmt!" und verschwindet; "Kill" steht nicht im Rechtsklick.
9. Mit Fisch in der Hand 10 Kacheln weggehen, stehenbleiben. Erwartet: es kommt nach. Ohne Futter: es bleibt in seiner Gegend.
10. Speichern, ins Hauptmenue, laden. Erwartet: Junges steht da, `NCBear_CubInfo()` zeigt `tame`, Besitzer `__sp`.
11. Koeder: `NCBear_CubClean()`. Honig nehmen, Rechtsklick auf Waldboden -> "Baeren-Koeder auslegen". Erwartet: Honig weg, Schild
    "Baeren-Koeder (Honig) -- Nacht 0 von bis zu 3". 25 Kacheln weggehen, `NCBear_CubNight(true)`, zurueckgehen. Erwartet: Junges nahe
    der Stelle, Schild weg. In der Stadt: Punkt grau "nur im oder am Wald".
12. Verschwinden und Tod: `NCBear_CubSkip(40)` beim ungefuetterten Jungen, 30 Kacheln weggehen: "ist weitergezogen", Junges weg.
    Dann `NCBear_CubHere()`, `NCBear_CubTame(100)` (sofort gezaehmt) und `NCBear_CubKill()`: "Dein Baer ist tot ... 7 Tage",
    `NCBear_CubHere()` lehnt mit dem Grund ab; `NCBear_CubSkip(168)` hebt die Sperre auf.
Zum Schluss der echte Weg ohne Bench: Sandbox Haeufigkeit "sehr oft", im Wald warten: Meldung "Wimmern ... im Nordosten", hingehen.

### 10.2 Mehrspieler (dedizierter Server, Rolle `user`, zwei Spieler; Sandbox: Haeufigkeit "sehr oft", Mindestabstand 15, Abklingzeiten 0)
1. Server startet ohne Fehler (laedt er das GLB? Zeile im Server-Log), beide Spieler verbinden, kein Kick.
2. Im Wald warten, bis ein Junges erscheint (Meldung beim Finder). Beide sehen es an derselben Stelle.
3. Spieler A fuettert: nur A verliert genau ein Stueck, beide sehen den Balken wachsen. Spieler B versucht zu fuettern: "vertraut schon
   jemand anderem", B verliert nichts.
4. A zaehmt zu Ende, trennt die Verbindung, kommt wieder: Balken/Besitz stimmen, Streicheln geht.
5. B legt einen Koeder, beide gehen weg, Nacht abwarten: B bekommt sein Junges; A (hat einen Baeren) kann keinen Koeder legen.
6. Server neu starten: Junge und Register sind noch da. Kein Kick in keinem Schritt.

---

## 11. Offen, nicht gebaut, Fragen

**Nicht in B1a (vorbereitet: Register-Felder, `kind`, `aid`):** Wachsen zum Erwachsenen (B1b); Kampf, Gegenwehr, Verstecken hinter dem
Besitzer; Befehle Folgen/Bleiben/Sitz (das Mitlocken mit Futter ist bewusst der einzige Weg, das Junge zu bewegen); Baeren-Fenster mit
V; Namensschild, Lebensbalken, Name; Beduerfnisse, Vertrauen/Laune nach dem Zaehmen (Streicheln und Fuettern am zahmen Jungen geben nur
Abklingzeit und Meldung); Inventar; Schlafen; Umbenennen der alten Dateien und der Art `bear` (B5a); Stimme des Jungen (kein Ton, kein
Download); Mutter (Weg B), Fundort (D), Spur.

**Ungespielt / ungeprueft, Testpunkte:** Junges nach Speichern/Laden und Entladen/Laden (42.22.2); `OnClickedAnimalForContext` fuer die
neue Art; Streichel-Haltung mit `"lamb"`; haelt `setBlockMovement` das nicht wilde Junge waehrend der Aktion; rennt `fleeTo` wie
gedacht und sieht das "Naeherkommen" gut aus; Gleiten der Schritte bei 0,35; dedizierter Server: GLB, `getObjectListForLua`,
Kachel-Fragen, OnlineID nach Neuladen; Schatten- und Kollisionsgroesse.

**Bekannte Grenzen:** kein Schutz vor Waffen/Autos/Feuer (Tod wird verbucht, Frage 4); Fremde koennen ein zahmes Junges in ihren
Anhaenger laden (PLAN 9, spaeter); "ausser Sicht" im MP nur ueber den Mindestabstand; Fress-Animation im MP nur beim Fuetternden; ein
SP-Spielstand, der spaeter als MP gehostet wird, kennt den Besitzer `__sp` nicht mehr (Baer verwaist -- Umzug spaeter); im geteilten
Bildschirm teilen sich alle lokalen Spieler einen Besitz und es wird kein Balken gezeichnet; NPC Crews Tierpflege braucht die Naht 12.2;
Engine-Akzeptanz (Q-Ruf) haengt an der OnlineID (FE O3, Sache der Befehle).

**Fragen an Kevin (5, jede mit Empfehlung)**
1. **Tempo des Zaehmens:** 3 Fuetterungen mit Honig/Fisch oder 4 mit anderem Futter, dazwischen streicheln; Fuettern alle 2
   Spielstunden, Streicheln jede Stunde -- also ein Nachmittag im Spiel. Empfehlung: so lassen und im Test fuehlen (alles Sandbox).
2. **Koeder unsichtbar:** der Honig/Fisch wird beim Auslegen verbraucht, ueber der Stelle steht ein Schild, statt dass ein Glas am
   Boden liegt (das verrotten oder von der Crew eingesammelt werden koennte). Empfehlung: unsichtbar mit Schild.
3. **Mehrspieler, wem das Junge gehoert:** wer zuerst fuettert, an den bindet es sich; nach dem Zaehmen darf nur der Besitzer
   streicheln und fuettern. Empfehlung: ja.
4. **Schutz jetzt schon?** In dieser Version kann das Junge durch Auto, Waffe oder Feuer sterben (bei einem gezaehmten: 7 Tage
   Sperre). Unverwundbar ginge nur mit dem Engine-Schalter `setIsInvincible`, den Vanilla nur im Cheat-Menue ruft -- braucht dein Ja.
   Empfehlung: jetzt nein, erst mit der Gegenwehr (B5a), wo der Schaden ohnehin selbst gerechnet wird.
5. **Finden leichter machen:** Hinweis-Text mit Himmelsrichtung ("Wimmern aus dem Wald im Nordosten") und das Junge kommt neugierig bis
   auf 9 Kacheln heran. Ohne das findet man ein Junges 40 Kacheln tief im Wald kaum. Empfehlung: beides an.

---

## 12. Fuer den ZUSAMMENBAU (Uebernahme-Skript `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`)

### 12.1 Was das Skript ueber das Turret-Vorbild hinaus koennen muss (FB 4.1)
1. Lua-Muster `^(42|common)/media/lua/(shared|client|server)/(ISUI/|TimedActions/)?BanditsNPCBear[A-Za-z0-9_]*\.lua$`; Bench
   `NCBearBench*` in jedem Ordner und mit jeder Endung ueberspringen; `mod.info`, `.git*` nie.
2. Sandbox: die `option BanditsNPC.Bear*`-Bloecke an NPC Crews `sandbox-options.txt` anhaengen (LF, Tabs, nur C-Kommentare, `VERSION`
   nicht doppelt), Abbruch bei vorhandenem Namen; `Sandbox_BanditsNPC` nicht doppelt eintragen (gleicher Wert = kein Fehler).
3. `IG_UI.json` gibt es in NPC Crew nicht: sortiert neu anlegen bzw. zusammenfuehren, falls inzwischen vorhanden.
4. Eigene Namen fuer die Kollisionsprobe: `BanditsNPC\.Bear\b`, `BanditsNPCBear`, `TrueCompanionsBears`, `TC-BEAR`, `UI_BN_Bear_` (MIT
   Unterstrich: `UI_BN_Beard_None` ist NPC Crews), `\btcBear\b` (nicht `tcBeardColor`), `ncbear`, `NCBear`, `nc_bear`.
5. Regel "Testbefehl" (`NC[A-Z]..._...`) trifft echte Asset-Namen in Strings: Erlaubt-Liste aus Skripten und GLB ableiten
   (`NCBearCub_Body`; `NCBearAct` und `NCBearCub` haben keinen Unterstrich).
6. Regel "globale Zuweisung": erlaubt sind genau `BanditsNPC = BanditsNPC or {}`, die drei Aktionsklassen (`... =
   ISBaseTimedAction:derive("...")`, Engine verlangt globale Klassen, FE 8.2) und `AnimalDefinitions = AnimalDefinitions or {}`.
7. Tier-Gegenstueck zur Regel "Gegenstand erzeugen": `addAnimal(` nur in `B.CreateCub`, Aufrufer von `B.CreateCub` nur `B.AppearFor`,
   Aufrufer von `B.AppearFor` nur Wald-Wurf und Koeder in `BanditsNPCBearServer.lua`; `:remove()` am Tier nur in `B.RemoveCub`.
8. Alt-Liste bis B5a: `NCBearDefs.lua`, `NCBearFight.lua`, `NCBearSpawn.lua`, `NCBearSize.lua`, `NCBearAttackProbe.lua`,
   `NCBearTest.lua` und die drei Test-Texte in EN `IG_UI.json` -- gemeldet als "noch umzubenennen (B5a)"; mit einem Schalter (Form
   `--vor-t10`, z. B. `--vor-b5a`) nur Warnung, mit `--echt` immer Fehler; der Trockenlauf ohne Schalter ist absichtlich rot.
9. Clips liegen im GLB, nicht in Vanilla `anims_X`: die Clip-Namen der `AnimSets/buck/idle/NCBear_*.xml` gegen die Animationsnamen im
   GLB-JSON pruefen (`NCBear.glb` und `NCBearCub.glb`).
10. Abhaengigkeit festhalten: das Junge benutzt `AnimSets/buck/idle/NCBear_Eat.xml` (alte Datei der Test-Mod) fuer die Fress-Animation.

### 12.2 Naehte (alle zur Laufzeit, in `Events.OnGameBoot`, hinter Existenz-Riegel, genau einmal; keine NPC-Crew-Datei wird geaendert)

| Nr | Stelle | Fundstelle | Wie |
|---|---|---|---|
| 1 | Tierpflege zaehlt jedes Tier einer Gruppe, die nicht in `Lv.NOT_TENDED` steht, als Vieh (zaehlen, Schlachtplan) | `NC:shared/BanditsNPCLivestock.lua:5152` (Literal auf Dateiebene), Leser u. a. `:1875` | `shared/BanditsNPCBearCrew.lua`: in `OnGameBoot`, Riegel `BanditsNPC.Livestock and type(BanditsNPC.Livestock.NOT_TENDED) == "table"`, dann `NOT_TENDED["ncbear"] = true` und `NOT_TENDED["bear"] = true`; alle Leser per grep nachzaehlen (24 Treffer am 10.11.) |
| 2 | NPC Crew setzt `fleeZombies = false` fuer jede nicht wilde Art | `NC:shared/BanditsNPCAnimals.lua:51-89` | kein Aufsatz: unsere Definition setzt denselben Wert |
| 3 | Portrait und "Animal info" lesen `AnimalAvatarDefinition[Art]` | `NC:client/BanditsNPCPortrait.lua:324`, V:ISAnimalUI.lua:31 | Eintrag in Datei 3 |
| 4 | Sandbox-Seite `BanditsNPC`, Texte `UI.json`/`Sandbox.json`/`IG_UI.json` | FB 3.2 | zusammenfuehren (12.1) |
| 5 | Vanilla-Tiermenue | V:ISAnimalContextMenu.lua:1235 (Ereignis), :307-324 ("Kill") | eigener Empfaenger, blendet "Kill" nur am Jungen aus |
| 6 | Vanilla-Tabellen `AnimalDefinitions`, `AnimalAvatarDefinition`, `AnimalPartsDefinitions` | Datei 3 | nur neue Schluessel, nichts Fremdes veraendert |
| 7 | Koeder gegen Foersterin/Pluenderer | FB 5.1 | entfaellt: kein Bodengegenstand |
| 8 | Taste V / Baeren-Fenster, Namensschilder | ENT:98 | spaeter |

---

Statisch geplant, nichts gebaut, nichts gespielt.
