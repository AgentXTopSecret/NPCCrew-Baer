# Lauf baer-zaehmen (B1a) -- Forschung Bestand, Namen, Naehte

Stand 10.11.2026 ~17:15. **Statisch gelesen, nichts gebaut, nichts gespielt.** Nur diese Datei geschrieben. Fundstellen als
Datei:Zeile. Kurzformen: `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`, `PLAN` = `baer/begleiter/PLAN.md`, `KRIT` =
`baer/begleiter/KRITIK.md`, `STAND` = `baer/STAND.md`, `UEB` = `baer/UEBERGABE.md`, `SPEZ` = `_arbeit/baer_baby/SPEZ_BABY.md`,
`BT` = `C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media`, `TT` = `C:/Users/Kevin/Zomboid/mods/NCTurretTest/42/media`,
`NC` = `C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua`, `NC-CLAUDE` = `C:/Users/Kevin/Zomboid/mods/NPCCrew/CLAUDE.md`,
`V` = Vanilla `.../ProjectZomboid/media/lua`, `TU` = `turret/tools/turret_uebernahme.py`, `TN` = `turret/NAEHTE.md`,
`dec/` = `_arbeit/baer_zaehmen/dec/` (frischer Vineflower-Auszug dieses Laufs, Jar 42.22.2), `altdec/` =
`_arbeit/baer_spiel/dec/` (Jar vom 07.11.).

## 0. Das Wichtigste zuerst

1. **Das Spiel ist 42.22.2, nicht 42.21** (`C:/Users/Kevin/Zomboid/console.txt:61` und `:101` `version=42.22.2`, Start heute
   17:00:45; `projectzomboid.jar` vom 09.11. 16:07). Bandits hat seit 09.11. 20:47 einen Ordner `42.22`; gegen `42.21` weichen
   genau 4 Lua-Dateien ab (`shared/BanditUtils.lua`, `shared/ZombieActions/ZALootItems.lua`, `ZALootWeapons.lua`,
   `ZATakeFromContainer.lua`; `diff -rq`). Belege fuer Bandits-Aufrufe also gegen `42.22` + `common` pruefen. Die alten
   Vineflower-Auszuege `_arbeit/baer_spiel/dec/` stammen vom Jar des 07.11.; der frische Auszug `_arbeit/baer_zaehmen/dec/`
   (anderer Agent dieses Laufs) ist der heutige Stand -- Stellen mit `dec/` sind dort nachgelesen, Stellen mit `altdec/` und
   alle aus fremden Berichten uebernommenen Jar-Offsets (KRIT, SPEZ, recherche_spiel) nicht.
2. **Das Spiel lief waehrend dieser Forschung** (`tasklist`: ProjectZomboid64.exe). Der Integrator darf nichts in die Test-Mod
   kopieren, solange es laeuft.
3. **Der alte Code sieht das Junge nicht.** Kampf, Testhilfen, Spawn und Groesse fragen alle `getAnimalType()` gegen `"bear"`
   bzw. `bear`/`bearstag` (Abschnitt 2.2). Eine neue Art `ncbearcub` wird von keiner alten Datei erfasst.
4. **Alle festen Namen sind frei** (Abschnitt 3). Zwei Vorsilben-Fallen: `UI_BN_Bear` trifft NPC Crews `UI_BN_Beard_None`,
   `tcBear` trifft `tcBeardColor`. Muster deshalb immer `UI_BN_Bear_` (mit Unterstrich) und `\btcBear\b`.
5. **Wichtigste Naht:** NPC Crews Tierpflegerin behandelt jedes Tier in einer NPC-Crew-Tierzone als Vieh, dessen GRUPPE nicht
   in `Lv.NOT_TENDED` steht -- streicheln, zaehlen, Schlachtplan (Abschnitt 5.1). Das Junge braucht dort einen Eintrag, in
   `OnGameBoot`, hinter Existenz-Riegel.
6. **Ein Junges ohne die Mod im Spielstand ist ein echter Schaden** (`baer/spiel/tier_spez.md:411-419`: `IsoAnimal.load`,
   `getDef` null). Weil B1a Junge von selbst in der Welt entstehen laesst, muss der Artname `ncbearcub` ab dem ersten Kopierzug
   endgueltig sein.

---

## 1. Anforderungen an Finden, Zaehmen, Besitz

"Kevin" = woertlich, mit Fundstelle. "Vorschlag" = Vorschlag, unbestaetigt (Zahl als Sandbox-Option mit dieser Vorgabe).

### 1.1 Allgemein

| Nr | Anforderung | Herkunft |
|---|---|---|
| G1 | Jetzt den Code bauen, mit dem man das Junge findet und zaehmt | Kevin 10.11.: "nebenbei will ich das du schonmal den code programmierst das man das baby finden und tamen kann" (Auftrag dieses Laufs); dazu `UEB:42` "ich wuerd ja gern auch mal baeren features machen das taming und so vom baby baeren" |
| G2 | Alles per Copy-Paste nach NPC Crew: `BanditsNPCBear*.lua`, `BanditsNPC.Bear`, `UI_BN_Bear_*` in sieben Sprachen, Sandbox `BanditsNPC.Bear*`, Testhilfen nur `NCBearBench*` | Kevin, `ENT:50` ("ganz wichtig"), `../CLAUDE.md` Abschnitt 0 |
| G3 | Keine Cheat- oder Testmenues nach NPC Crew; das Uebernahme-Skript prueft und bricht ab | Kevin, `ENT:52` "FESTE REGEL" |
| G4 | Jede Version in SP und MP (oder im MP ehrlich als aus/offen) | Kevins Regel `../CLAUDE.md` Abschnitt 4; `ENT:45` "jede Version in SP und MP, Kampf im MP erst ab B9" (Vorgabe aus dem Plan, ohne eigene Frage) |
| G5 | Jungtier kaempft nicht, versteckt sich bei Zombies hinter dem Besitzer | Kevin-Entscheidung, Tabelle `ENT:8` (das Verstecken ist NICHT B1a, nur vorbereiten) |
| G6 | Groesse Jungtier 0,35 (rund 70 cm lang), Leben 40 | `ENT:8`, `ENT:17` (Leben: Vorschlag als Vorgabe, `ENT:14`) |
| G7 | Eigenes Baby-Modell mit eigenem Gesicht | Kevin `ENT:139` "guck mal das bild sollst du nehmen als vorlage fuer das gesicht vom baby baeren wenn der noch klein ist ;D"; baut der Lauf baer-junges |
| G8 | Artname mit Vorsilbe `nc` | Kevin-Antwort `ENT:44` (`ncbear`), `ENT:101`; fuer das Junge im Auftrag fest `ncbearcub` |

### 1.2 Finden

| Nr | Anforderung | Herkunft |
|---|---|---|
| F1 | Weg A: verwaistes Junges im Wald | Kevin `ENT:41`: "Weg A (verwaistes Junges im Wald, 3-5 Mal aus der Hand fuettern) plus C (Koederplatz mit Honig oder Fisch). Mutter (B) spaeter." |
| F2 | Weg C: Koederplatz mit Honig oder Fisch | Kevin `ENT:41` |
| F3 | Finden statt spawnen | `STAND:116` "Jungtier im Wald finden (Koeder) statt spawnen" (Claudes Fassung von Kevins Reihenfolge `ENT:99`) |
| F4 | Wald = Zonentyp `Forest`/`DeepForest` ueber `square:getZone():getType()` | Vorschlag `PLAN:62` (Beleg dort: Vanilla `Traps/TrapSystem.lua:43`; hier nicht nachgelesen) |
| F5 | Selten, in Spielernaehe, ausser Sicht; Haeufigkeit als Sandbox-Option (Vorgabe "mittel") | Vorschlag, unbestaetigt: `UEB:45`, `ENT:150` ("ihm erklaert, aber noch nicht ausdruecklich bestaetigt"), `PLAN:253` |
| F6 | Koederplatz: nach 1 bis 3 Naechten sitzt dort ein Junges | Vorschlag, unbestaetigt: `PLAN:64`, `UEB:46` |
| F7 | Koederplatz "am Waldrand"; Besitz klar: wer den Koeder legte | Vorschlag `PLAN:64` |
| F8 | Ein Junges erscheint nur fuer Spieler ohne lebenden Baeren | Vorschlag `PLAN:72` |
| F9 | Je Spieler hoechstens ein wildes Junges gleichzeitig | Vorschlag, unbestaetigt `UEB:47` |
| F10 | Ungefuettert und 1 bis 2 Spieltage ohne Kontakt -> das Junge verschwindet; einmal gefuettert -> es bleibt | Vorschlag, unbestaetigt `UEB:46-47`, `ENT:150` |
| F11 | Im MP erzeugt der Server das Junge (eigener Serverbefehl bzw. Server-Takt, nie Client-Debug) | Vorschlag `PLAN:62`, `PLAN:218`, `recherche_spiel.md:298-300`; Kick-Regel `../CLAUDE.md` Abschnitt 4 |
| F12 | Nichts weiter als 76 Kacheln vom Spieler ansprechen | Regel `../CLAUDE.md` Abschnitt 8; NC-CLAUDE:803 (152 x 152 Kacheln, gemessen) |
| F13 | Immer dabei: ein Test-Weg "Junges geben" | Vorschlag `PLAN:67` -- nach G3 NUR in `NCBearBench*.lua` |
| F14 | Mutter verteidigt das Junge (Weg B), seltener Fundort (Weg D), Spur im Suchmodus | Kevin: "Mutter (B) spaeter" (`ENT:41`); D und Spur nur Idee (`PLAN:63-65`, `recherche_lokal.md:71`) -- NICHT B1a |

### 1.3 Zaehmen

| Nr | Anforderung | Herkunft |
|---|---|---|
| Z1 | Mit Futter zaehmen UND streicheln; die Mischung fuellt den Fortschritt | Kevin `ENT:104`: "ich will das man den irgentwie mit futter tamed und den streicheln kann ;D so eine mischung aus beiden soll den fortschritt fuellen ^^" |
| Z2 | Zaehm-Balken mit sichtbarem Fortschritt | Kevin `ENT:99`: "wir brauchen einen taming balken mit vorschrit und so"; Ausfuehrung `ENT:102` (wie weit er vertraut, was ihn voranbringt; sichtbar beim Zaehmen und spaeter im Baeren-Fenster) |
| Z3 | Aus der Hand fuettern, 3 bis 5 Mal | Kevin `ENT:41` (aelter als Z1; Z1 verfeinert: siehe Widerspruch W4) |
| Z4 | Immer streichelbar, mit Abklingzeit (Jungtier und erwachsen, auch nach dem Zaehmen) | Kevin `ENT:107`: "der baer soll immer streichelbar sein mit cooldown ;D"; Ausfuehrung `ENT:108` |
| Z5 | Nur Fuettern oder nur Streicheln kommt langsamer voran als beides im Wechsel; Zahlen vorschlagen | Claudes Ausfuehrung zu Z1, `ENT:104` ("Zahlen im Bau vorschlagen") -- Vorschlag |
| Z6 | Futter: Fleisch, Fisch, Beeren, Obst, Honig, Insekten, Eier, Nuesse; Honig und Lachs geben extra | Vorschlag `PLAN:136-142` |
| Z7 | Eigener Menuepunkt "Baer fuettern" (Vanillas "Feed" bietet dem Baeren kein Fleisch, Fisch, Honig an) | Befund `KRIT:42-51`, `ENT:104`; Beleg dort `V/client/ISUI/Animal/ISAnimalContextMenu.lua:33-39` |
| Z8 | Kein Futter verloren oder verdoppelt (rote Linie); im MP nimmt der Server | `../CLAUDE.md` Abschnitt 4; NC-CLAUDE:1600-1616 (Kick bei Client-Loeschpaket) |
| Z9 | Streicheln: wer darf im MP -- "nur der Besitzer bzw. wer darf (MP: im Bau klaeren)" | offen, `ENT:108` |
| Z10 | Engine-Akzeptanz direkt setzen ist ein Debug-Cheat (`setDebugAcceptance`) -- nicht fuer NPC Crew | Befund `ENT:97`, `ENT:104` |
| Z11 | Nach dem Zaehmen geht der Balken als Vertrauen/Laune weiter (sichtbar, "wie happy"); merkt sich den Verlauf von Hunger/Durst | Kevin `ENT:107` ("vertrauens system ... wie happy der baer ist"), `ENT:110` -- NICHT B1a (Beduerfnisse), aber das Register so anlegen, dass der Wert weiterlebt |
| Z12 | Fress-Animation beim Fuettern | Kevin `ENT:63`, `ENT:65` ("Fressen spielt beim Fuettern"); Knoten und Clip gibt es schon (2.3) -- in B1a wahlfrei |
| Z13 | Schlechtes/giftiges Futter senkt Vertrauen | nur Idee (Companion Dogs, `recherche_dogs.md:46`) |

### 1.4 Besitz

| Nr | Anforderung | Herkunft |
|---|---|---|
| B1 | Jeder Spieler darf EINEN Baeren als Begleiter haben | Kevin-Grundsatz `ENT:34` |
| B2 | Register beim entscheidenden Rechner (SP bzw. Server): Benutzername -> Tier-Kennung `getAnimalID()` | Vorschlag `PLAN:70-72`; `STAND:117` "Register beim Server, Spiegel am Tier" |
| B3 | Die Wahrheit steht NUR im Register (globaler Speicher des Servers); ModData am Tier ist nur Spiegel; unser Client ruft `transmitModData` am Tier nie | Befund `KRIT:53-62` (jeder Client darf Tier-ModData ueberschreiben, `ObjectModDataPacket` nur `LoginOnServer`), `PLAN:73-76` |
| B4 | Im SP ist der Besitzer-Schluessel fest, nicht der Charaktername | `PLAN:75-76`; NC-CLAUDE:3442-3446 und :3472-3476 (`getUsername()` ist im SP der Charaktername) |
| B5 | Das Adoptieren/Zaehmen prueft das Register noch einmal; der Server prueft bei JEDER Bitte den Besitz | Vorschlag `PLAN:72`, `PLAN:219`; NC-CLAUDE:2655-2690 (v3.7.53) |
| B6 | Nach dem Tod des eigenen Baeren ein neues Junges erst nach 7 Spieltagen | `ENT:45` ("Ohne eigene Frage, Vorgabe aus dem Plan" -- also von Kevin nicht einzeln beantwortet), `PLAN:77`, `PLAN:259`; als Sandbox-Option |
| B7 | Baeren je Spieler als Sandbox-Zahl (Vorgabe 1) | Vorschlag `PLAN:252` -- reibt sich mit B1 (W7) |
| B8 | Besitzer offline: der Baer "ruht" (kein Schaden, kein Hunger); fuer B1a: die Verschwinde-Uhr (F10) darf nicht laufen, waehrend der Finder offline ist | Vorschlag `KRIT:86-87`, `PLAN:229-230`; Uebertragung auf F10 ist meine Ableitung |
| B9 | Fremde duerfen einen fremden Baeren nicht toeten, anleinen, aufheben, in ihren Anhaenger laden | Vorschlag `PLAN:225-228`, `KRIT:81-85` -- fuer B1a mindestens als offen fuehren |
| B10 | Beim spaeteren Wachsen baut die Engine ein NEUES Tier; ModData geht nicht mit, die AnimalID schon -> Register-Schluessel AnimalID | Befund `SPEZ:211-219`, `UEB:59-62`; deshalb im Auftrag "Wahrheit im Register" |
| B11 | Namensschild, Lebensbalken, Baeren-Fenster mit V, Umbenennen | Kevin `ENT:98`, `ENT:103`, `ENT:105-106` -- NICHT B1a |
| B12 | Zombies greifen nur den gezaehmten Baeren an | Vorschlag, unbestaetigt `UEB:48` -- B5a, nicht B1a |

### 1.5 Widersprueche (ENT geht vor)

- **W1 Artname des Jungen:** `SPEZ:341`, `STAND:32`, `UEB:59` sagen `bearcub`; der Auftrag setzt `ncbearcub` (passt zu `ENT:44`). Es
  gilt `ncbearcub`.
- **W2 Modellnamen fuer NPC Crew:** `SPEZ:338-340` schlaegt fuer spaeter `BanditsNPCBearCub.glb` / `BanditsNPCBearCub_Body` vor. Der
  Auftrag setzt `NCBearCub` / `NCBearCub_Body` und "gleiche relative Pfade" (`../CLAUDE.md` 0.1; Vorbild Turret: `NCTurret*.fbx`
  geht unveraendert mit, `TU:93`). Es gilt `NCBearCub*`.
- **W3 Eine Art oder zwei:** `PLAN:83-84` "Eine einzige Tierart, die stufenlos waechst (kein Stufenwechsel der Engine)". Dagegen
  Kevins eigenes Baby-Modell (`ENT:139`) und `SPEZ:318-327` (eigene Art mit eigenem GLB, Vanillas Weg). Der Auftrag folgt SPEZ:
  eigene Art. Folge: beim spaeteren Wachsen entsteht ein neues Tier -> B10.
- **W4 Zaehmen:** `ENT:41` (08.11. frueh) "3-5 Mal aus der Hand fuettern", `ENT:104` (08.11. ~20:00) "mischung aus beiden soll den
  fortschritt fuellen". Die spaetere Aussage verfeinert: der Balken ist das Mass; die Zahlen so vorschlagen, dass 3 bis 5
  Fuetterungen MIT Streicheln reichen und nur Fuettern laenger dauert (Vorschlag).
- **W5 Vanilla-Fuettern:** `PLAN:62` "Vanilla Feed gibt schon Vertrauen" gegen `KRIT:42-51` (Vorfilter laesst Fleisch, Fisch, Honig
  nicht durch). Es gilt KRIT: eigener Menuepunkt.
- **W6 Reihenfolge:** `ENT:150` (09.11.) "Reihenfolge lassen" (erst Gegenwehr, dann Baby); Kevin 10.11. will den Zaehm-Code "nebenbei
  schonmal". Kein echter Widerspruch: B1a kommt vor B5a, das Umbenennen der alten Dateien bleibt bei B5a (`ENT:101`).
- **W7 Zahl der Baeren:** Kevin "einen Baeren" (`ENT:34`) gegen Sandbox "Baeren je Spieler" (`PLAN:252`). Vorschlag: Option mit
  Vorgabe 1 -- Kevin fragen, ob er die Option ueberhaupt will.
- **W8 Ort des Uebernahme-Skripts:** `ENT:50` nennt `_docs/tools/baer_uebernahme.py` (vor dem Umzug); Auftrag und `../CLAUDE.md` 0.3
  sagen `baer/tools/baer_uebernahme.py`. Es gilt der Auftrag.
- **W9 Mittel aus dem Plan, die die Cheat-Pruefung treffen:** `PLAN:160-169` (`setIsInvincible`, `setDebugStress`) und `ENT:97`
  (`setDebugAcceptance`). Jedes `debug` im Code ist nach Turret-Vorbild ein Cheat-Fund (`TU:128-129`). In B1a nicht benutzen.

---

## 2. Bestand NCBearTest

### 2.1 Dateien (alle LF, ASCII, kein BOM -- mit Python an den Bytes gemessen)

| Datei | Zeilen | Was |
|---|---|---|
| `BT/lua/shared/NCBearDefs.lua` | 127 | Arten `bear` und `bearstag` (:101-102), Avatar (:106-121), Zerlege-Teile (:124-127) |
| `BT/lua/shared/NCBearFight.lua` | 2077 | Kampf, Ruhe (Sitzen, Fressen), Laerm; nur SP; am Ende Konsolenbefehle `NCBear_Fight/Tune/FightInfo` (:2002-2077) |
| `BT/lua/client/NCBearBench.lua` | 176 | Testbefehle `NCBear_Sit/Stand/Eat/Huff/NextAttack/AnimTest/ZHealth/KnockInfo` |
| `BT/lua/client/NCBearSpawn.lua` | 121 | `NCBear_SpawnLive`, Menue-Eintraege "Spawn living bear here" / "Remove living bears nearby" |
| `BT/lua/client/NCBearSize.lua` | 34 | `NCBear_Size(x)` |
| `BT/lua/client/NCBearAttackProbe.lua` | 290 | `NCBear_AttackProbe()` (Sonde) |
| `BT/lua/client/NCBearTest.lua` | 157 | Rechtsklick-Untermenue "NC Bear" (stehendes Modell), `NCBear_Spawn()`; Tabelle `NCBearMenu.extra` (:10-11, :132-134) |
| `BT/lua/shared/Translate/EN/IG_UI.json` | 6 | 4 Schluessel: `IGUI_AnimalType_bear`, `IGUI_AnimalType_bearstag`, `IGUI_Animal_Group_bear`, `IGUI_Breed_brown` |
| `BT/scripts/nc_bear.txt` | 24 | `module NCBear`: `model NCBear_World`, `item BearStatic` |
| `BT/scripts/nc_bear_tier.txt` | 24 | `module Base`: `animationsMesh NCBear`, `model NCBear_Body`, `model NCBearStag_Body` |
| `BT/scripts/nc_bear_sounds.txt` | 72 | `module Base`: `NCBear_Roar`, `_Growl1..3`, `_Huff`, `_HuffSoft`, `_Pain` |
| `BT/AnimSets/buck/idle/NCBear_*.xml` | 10 Dateien | Knoten Bite, Eat, Maul, Rear, Sit, SitDown, Slam, StandUp, SwipeL, SwipeR; Bedingung Variable `NCBearAct` (STRING) |
| `BT/models_X/Skinned/NCBear.glb`, `NCBearDeer.glb`, `WorldItems/NCBear.fbx` | | Modelle |
| `BT/textures/Body/NCBear.png`, `Item_NCBear.png`, `WorldItems/NCBear.png`; `BT/sound/NCBear_*.wav` (6) | | |
| `NCBearTest/mod.info` und `42/mod.info` | je 567 Bytes, gleich | `id=NCBearTest`; KEIN `loadModAfter`, kein `require` |

Es gibt keinen Ordner `lua/server`, keine `sandbox-options.txt`, keine `UI.json`, keine `Sandbox.json`; `common/media` ist leer.
`.git` ist eine Zeigerdatei (`gitdir: C:/Users/Kevin/Zomboid/backups/NCBearTest/repo.git`), `.gitattributes` = `* -text`.

### 2.2 Wie der alte Code Baeren findet, merkt, bewegt -- und warum das Junge draussen bleibt

- **Finden:** alle 5 s (`SCAN_EVERY`, `NCBearFight.lua:125`) `getCell():getObjectListForLua()` und
  `instanceof(o, "IsoAnimal") and o:getAnimalType() == "bear"` (`:1784-1788`). Genau der String `"bear"`, nicht einmal `bearstag`.
- **Merken:** `register(a)` (`:1741-1760`), Tabellen `F.bears` / `F.byObj`, Deckel `MAX_BEARS = 8` (`:122`).
- **Takt:** `Events.OnTick` nur im SP (`:1869-1870` `if not F.enabled or not isSP() then return end`; eingehaengt in `OnGameStart`
  nur im SP, `:1886-1895`). Im MP tut die Datei nichts (`:4-5`).
- **Bewegen:** `getBehavior():setBlockMovement` (`:451`), `stopAllMovementNow` (`:446`), `setVariable("NCBearAct", ..)` (`:533`,
  `:1494`), `clearVariable` (`:422`, `:1756`), `faceThisObject` (`:428`), `playBreedSound` (`:543`, `:557`), `fleeTo(sq)` (`:581`, `:1383`).
- **Ziele:** nur `IsoZombie` (`F.IsTarget`, `:271-293`; erste Zeile `instanceof(z, "IsoZombie")`). Tiere sind nie Ziel.
- **Testhilfen:** `NCBearBench.lua` geht nur ueber `F.NearestBear` (`:58`, gemerkte Baeren); `NCBearSpawn.lua:7` `ARTEN = { bear,
  bearstag }` (auch fuer das Entfernen, `:69`); `NCBearSize.lua:24` `typ == "bear" or typ == "bearstag"`;
  `NCBearAttackProbe.lua:77` `ARTEN[...]`.

**Ergebnis:** ein Tier der Art `ncbearcub` wird nie registriert, nie bewegt, nie von einem Testbefehl angesprochen und nie als
Ziel gewaehlt. Der Kampf-Code erfasst das Junge nicht (statisch; Gegenprobe im Spiel: `NCBear_FightInfo()` zaehlt nur Baeren).
Kehrseite: die alten Testbefehle helfen beim Jungen nicht -- neue Testhilfen noetig (`NCBearBench*.lua`, neue Datei).

**Zwei Beruehrungen bleiben, beide gewollt nutzbar:**
1. Die Knoten `AnimSets/buck/idle/NCBear_*.xml` gelten fuer JEDES Tier mit `animset = "buck"`, also auch fuer das Junge, sobald
   jemand an ihm `NCBearAct` setzt (Clips sucht die Engine je Netz, `SPEZ:295-304`; der Platzhalter `NCBearCub.glb` traegt
   dieselben 15 Clip-Namen, selbst aus dem GLB gelesen). `NCBearFight.lua:19` sagt "NCBearAct schreibt NUR diese Datei" -- das
   gilt fuer gemerkte Baeren; am Jungen darf der neue Code die Variable setzen (z. B. `eat`), muss sie aber selbst wieder
   loeschen. Spaeter (B4/B5a) wieder EIN Schreiber.
2. Das Rechtsklick-Untermenue "NC Bear" nimmt Eintraege anderer Dateien ueber `NCBearMenu.extra` an (`NCBearTest.lua:132-134`,
   Vorbild `NCBearSpawn.lua:90-99`). Eine neue Bench-Datei kann sich dort einhaengen, ohne alte Dateien zu aendern (nur SP: das
   Menue ist im MP grau, `NCBearTest.lua:113-121`).

### 2.3 Was fuer das Junge NEU angelegt werden muss (keine alte Datei wird geaendert -- eine Ausnahme)

| Neu | Inhalt | Beleg/Vorbild |
|---|---|---|
| `scripts/nc_bear_cub.txt` (Name frei waehlbar, muss mit `nc_bear` beginnen) | `module Base { animationsMesh NCBearCub { meshFile = Skinned/NCBearCub.glb, keepMeshAnimations = true, } model NCBearCub_Body { mesh = Skinned/NCBearCub.glb, shader = animalEffect, static = false, animationsMesh = NCBearCub, } }` | Form `BT/scripts/nc_bear_tier.txt:3-15` |
| `models_X/Skinned/NCBearCub.glb` | Platzhalter `_arbeit/baer_baby/entwurf/NCBearCub.glb` (MD5 6c3f0a96ba9a2aaf3a06eabc184cdbc3, 1.226.188 Bytes, 15 Clips, 26 Gelenke, 1 Netz -- selbst gelesen); endgueltig aus Lauf baer-junges unter demselben Namen | `SPEZ:22-25` |
| `textures/Body/NCBearCub.png` | Platzhalter `.../entwurf/NCBearCub.png` (1024 x 1024 RGB, MD5 2ee25f24...) | `SPEZ:28-30` |
| Lua-Definition (neue `BanditsNPCBear*`-Datei in `shared/`) | `AnimalDefinitions.animals["ncbearcub"]`, `AnimalAvatarDefinition["ncbearcub"]`, `AnimalPartsDefinitions.animals["ncbearcub" .. rasse]` | Form `NCBearDefs.lua:62-127`; Avatar ist Pflicht (`V/client/ISUI/Animal/ISAnimalUI.lua:622`, :31), Teile-Schluessel = Art .. Rasse (`V/.../ButcheringUtil.lua:18`) |
| Tiernamen-Texte `Translate/<L>/IG_UI.json` | `IGUI_AnimalType_ncbearcub`; `IGUI_Animal_Group_<gruppe>`; `IGUI_Breed_<rasse>` | Leser: `V/client/DebugUIs/DebugContextMenu.lua:257-276`, `ISAnimalUI.lua:65/:69`, `ISAnimalContextMenu.lua:1134/1136`; Engine `IsoAnimal.getFullName` (frischer Auszug `_arbeit/baer_zaehmen/dec/IsoAnimal.java`, Text `IGUI_AnimalType_` + Art) |
| `Translate/<L>/UI.json` (7), `Translate/<L>/Sandbox.json` (7), `media/sandbox-options.txt` | gibt es in NCBearTest noch nicht | 3.2 |
| `lua/server/` | Ordner neu | |
| `lua/client/NCBearBench<Name>.lua` | Testhilfen fuer das Junge | G3 |

**Die Ausnahme: `Translate/EN/IG_UI.json` gibt es schon** (4 Schluessel). Je Mod und Sprache gibt es nur eine Datei dieses Namens,
und `IGUI_`-Schluessel liest das Spiel NUR aus `IG_UI.json` (Vorsilbe entscheidet die Tabelle: `Translator.getText`,
`altdec/Translator.java:397-445` (alter Auszug, im neuen Jar nicht nachgelesen); geladen je Mod aus `common` und Versionsordner, `:345-362`). Die Staging-Datei
EN muss also die 4 alten Schluessel UNVERAENDERT plus die neuen tragen; die sechs anderen Sprachen sind neue Dateien. Fuer die
Paritaet der Uebernahme (alle sieben Sprachen, gleiche Schluessel, `TU:488-501`) brauchen die sechs anderen Sprachen dieselben
Schluessel -- auch die alten Test-Namen, oder das Skript fuehrt die alten als benannte Alt-Schluessel (4.1 Punkt 8).

**Hinweise zur Definition des Jungen (gegen den frischen Jar-Auszug nachgelesen):**
- Eine Stufe gleich dem Artnamen, OHNE `nextStage` (Wachsen ist nicht B1a): dann tut `AnimalData.checkStages` nichts
  (`dec/AnimalData.java:118-134`), `isBaby()` ist falsch (`dec/IsoAnimal.java:1775-1777`), und die Textur kommt aus
  `texture`/`textureMale` -- **`textureBaby` wirkt nur mit `nextStage`** (`dec/IsoAnimal.java:1527-1533`). `SPEZ:365` nennt nur
  `textureBaby`; fuer B1a `texture` UND `textureMale = "NCBearCub"` setzen (dazu `textureBaby`, damit es mit spaeterem
  `nextStage` weiter stimmt).
- Groesse: das Junge-GLB ist bei Groesse 1,0 gebaut (1,90 m lang, `SPEZ:474`) und wird bei 0,35 gezeigt -> `minSize = maxSize =
  0.35` (Form `NCBearDefs.lua:73-74`; `setSize` klemmt auf `minSize`, `KRIT:30-31`). Ob die Schritte bei 0,35 gleiten, ist offen
  (`SPEZ:283-293`, Sache des Modell-Laufs). Ungespielt.
- Vorgaben der Engine, wenn ein Feld fehlt (`dec/AnimalDefinitions.java:56-126`): `alwaysFleeHumans = true`, `fleeZombies =
  true`, `canBePicked = true`, `needMom = true`, `canBeDomesticated = true`; `canBePet`, `canBeFeedByHand`, `canBeAttached`,
  `canBeTransported`, `wild` = false. Die Felder des Erwachsenen (`NCBearDefs.lua:86-97`) einzeln uebernehmen und bewusst
  entscheiden.
- `bodyModel` muss genau `NCBearCub_Body` heissen: ein Tippfehler gibt ein Tier ohne Bild, ein fehlendes Feld eine Ausnahme in der
  Schleife ueber alle Tiere (`baer/spiel/tier_spez.md:418`).
- `group`: in der Engine nur Text und Debug-Menue (Vanilla selbst: "just used for debug menu to spawn animal",
  `V/shared/Definitions/animal/CowDefinitions.lua:163`; im Jar nur Getter, `dec/AnimalDefinitions.java` `getGroup`). NPC Crew
  aber liest die Gruppe fuer die Tierpflege (5.1). Wahl in 3.1.
- Gene ohne `maxSize` lassen (`NCBearDefs.lua:14`, `SPEZ:367`).
- Vanillas Tier-Menue erscheint auch am Jungen: Untermenue mit `animal:getFullName()`, "Animal info", bei `canBePet` "Pet"
  (`ISAnimalContextMenu.lua:286-287`), ab Durst/Hunger 0,1 Wasser/Feed (`:300-305`), fuer nicht wilde Tiere "Kill"
  (`:307-317`), Anleinen bei `canBeAttached` (`:173`), Aufheben bei `canBePicked` (`:265`). Was davon am Jungen stehen darf, im
  Plan entscheiden (B9).

### 2.4 SPEZ_BABY Abschnitt 3 geprueft

| Aussage | Urteil |
|---|---|
| 3.1 Vanilla-Jungtiere sind eigene Arten mit eigenem Netz und animationsMesh | uebernommen (nicht neu nachgezaehlt) |
| 3.2 `isBaby()` = Stufe hat `nextStage`; `checkStages` ruft `grow` nur mit `nextStage` | **stimmt**, frischer Auszug `dec/IsoAnimal.java:1775-1777`, `dec/AnimalData.java:118-134` |
| 3.2 `grow` baut ein neues Tier, AnimalID geht mit, ModData nicht | uebernommen (`SPEZ:211-219`, dort javap-belegt; hier nicht neu gelesen) |
| 3.3 Punkt 5: gleiche Clip-Namen in zwei Netzen gehen, `NCBear_*`-XML gelten fuer beide | uebernommen; der Platzhalter traegt die 15 Namen (selbst gelesen) |
| 3.6 Namen `bearcub`, spaeter `BanditsNPCBearCub*` | **ueberholt** durch den Auftrag (W1, W2) |
| 3.6 Kollisionsprobe 0 Treffer | **bestaetigt** und erweitert (3.1) |
| 3.6 "NPC Crew liest die Tabelle nur, z. B. LivestockPanel:4079, mit `group = "bear"` gegen Livestock pruefen" | **geprueft:** die Stelle selbst ist harmlos, die Tierpflege insgesamt nicht (5.1) |
| 3.7 Punkt 2 `textureBaby = "NCBearCub"` | **fuer B1a zu wenig** (ohne `nextStage` wirkungslos, 2.3) |
| 3.7 Punkt 2 Stufen `bearcub` -> `bear` | NICHT B1a |

---

## 3. Namen

### 3.1 Kollisionsprobe (10.11.2026; grep ueber NPC Crew `42` + `common`, Vanilla `media/lua` + `media/scripts`, Bandits alle Ordner)

| Name | NPC Crew | Vanilla | Bandits | Urteil |
|---|---|---|---|---|
| `ncbearcub` (Art) | 0 | 0 | 0 | frei |
| `bearcub`, `ncbear` (ohne Gross/Klein) | 0 (ein Kommentar nennt `NCBearTest`, `shared/BanditsNPC.lua:1356`) | 0 | 0 | frei |
| `animals["bear"`, Gruppe `bear` | 0 | 0 (nur `IGUI_ItemCat_Bear`, Teddy, Buchtitel) | 0 | frei |
| `NCBearCub`, `NCBearCub_Body` | 0 | 0 | 0 | frei |
| `BanditsNPCBear*` (Dateien, Klassen) | 0 | 0 | 0 | frei |
| `BanditsNPC.Bear` (Modul, Sandbox) | 0 | 0 | 0 (Bandits nennt `BanditsNPC` nirgends) | frei |
| `UI_BN_Bear_` | 0 | 0 | 0 | frei -- **aber `UI_BN_Bear` ohne Unterstrich trifft `UI_BN_Beard_None`** (8 Treffer: `client/BanditsNPCAppearance.lua:244` + 7 x `UI.json:292`) |
| `Sandbox_BanditsNPC_Bear` | 0 | 0 | 0 | frei |
| `TrueCompanionsBear*` (ModData-Schluessel nach Turret-Form) | 0 | - | - | frei |
| `TC-BEAR` (Log-Praefix nach Turret-Form) | 0 | - | - | frei |
| `tcBear` (Marke am Tier, NC-Form `tc...`) | **`tcBeardColor`** (11 Stellen) | - | - | nur als ganzes Wort frei: Muster `\btcBear\b` |
| `BNBear`, `BN_Bear_` | 0 (`BN_Bear` trifft wieder `UI_BN_Beard`) | - | - | frei mit derselben Vorsicht |

Sortierung: `UI_BN_Bear_*` faellt in NPC Crews `UI.json` VOR `UI_BN_Beard_None` (`_` 0x5F < `d` 0x64) -- unkritisch, das
Uebernahme-Skript fuegt sortiert ein.

**Vorschlag fuer die noch offenen Namen (Planer entscheidet; alle oben als frei gemessen):**

| Was | Vorschlag | Vorbild |
|---|---|---|
| Kern-Datei | `shared/BanditsNPCBear.lua` (laedt in `shared/` vor allen `BanditsNPCBear<X>.lua`: `.` 0x2E < Buchstabe) | `TT/lua/shared/BanditsNPCTurret.lua` |
| Modul | `BanditsNPC = BanditsNPC or {}` / `BanditsNPC.Bear = BanditsNPC.Bear or {}` am Kopf JEDER Datei | `TT/.../BanditsNPCTurret.lua:14-16`; alle NC-Dateien nutzen `or {}` (grep: kein nacktes `BanditsNPC = {`) |
| Globaler Speicher (Register) | `"TrueCompanionsBears"` | `T.KEY = "TrueCompanionsTurrets"`, `BanditsNPCTurret.lua:19` |
| Befehlsmodul | `"BanditsNPCBear"` | `T.CMD = "BanditsNPCTurret"`, `:20` |
| Log-Praefix | `[TC-BEAR]` | `[TC-TURRET]`, `:100` |
| Spiegel am Tier | ein Feld `tcBear` (Tabelle) in `animal:getModData()` | NC-Marken `tcUid`, `tcHkZ`; Vorsilben-Falle oben |
| Gruppe | `ncbear` (neu, eigener Text `IGUI_Animal_Group_ncbear`) ODER `bear` wie der Erwachsene (`SPEZ:362`; Text gibt es in EN) | siehe unten |
| Rasse | `brown` wie der Erwachsene (Text `IGUI_Breed_brown` gibt es in EN; Teile-Schluessel dann `ncbearcubbrown`) | `NCBearDefs.lua:38-39` |
| Sandbox-Option | `BanditsNPC.Bear<Name>`, `translation = BanditsNPC_Bear<Name>`, Texte `Sandbox_BanditsNPC_Bear<Name>` (+ `_tooltip`, `_option1..n`) | 3.2 |
| Testhilfe | `client/NCBearBenchCub.lua`, Befehle `NCBear_Cub*` | `TT/lua/client/NCTurretBench*.lua` |
| Skript-Datei | `scripts/nc_bear_cub.txt` | `nc_bear_tier.txt` |

Zur Gruppe: der Auftrag sagt "Gruppe laut Plan". Fuer `ncbear` spricht die Namensregel (nichts Neues muss bei B5a umbenannt
werden) und dass eine fremde Baeren-Mod eher `bear` belegt; fuer `bear` spricht, dass das Debug-Menue Junges und Erwachsenen
zusammen zeigt und der EN-Text schon da ist. Die Gruppe steht nur in der Definition, nicht im Tier (Annahme aus dem Getter-Befund
2.3; **ob sie im Spielstand steht: ungeprueft**). Die Naht 5.1 traegt am besten BEIDE Gruppen ein.

**Woerter, die in Datei-, Options-, Text- und Befehlsnamen sowie in Strings NICHT vorkommen duerfen** (sonst Cheat-Fund nach
Turret-Vorbild, `TU:122-152`): `spawn` (auch in Strings, `CHEAT_STRING`; `despawn` ist ausgenommen), `debug`, `bench`, `cheat`,
`test`/`Test`, `Dbg`; im Dateinamen-Rest hinter `BanditsNPCBear` ausserdem `Dev`, `Tools`, `Admin`, `Console`, `Tweak`, `Tune`
(`CHEAT_FILE_REST`, `TU:151`). Also z. B. Option `BearCubWildChance` statt `...SpawnChance`, Befehl `"Appear"` statt `"Spawn"`.

### 3.2 Wie es in NPC Crew heisst und liegt (damit die relativen Pfade gleich sind)

| Was | NPC Crew | Folge fuer das Staging |
|---|---|---|
| Lua | `42/media/lua/client` (67 Dateien, Unterordner `ISUI/` 51 und `TimedActions/` 1), `server` (33), `shared` (83) | dieselben Ordner; Unterordner nur `ISUI/` und `TimedActions/` (so prueft es `TU:94`) |
| Zeitaktionen | `client/TimedActions/BanditsNPCUpgradeBeaconAction.lua` (einzige; `ISBaseTimedAction:derive`, die Wirkung in `perform()` ueber eine Modulfunktion, :17-52) | Vanilla-B42-Aktionen liegen in `shared/TimedActions/`; welcher Ordner, entscheidet die Engine-Forschung -- das Uebernahme-Muster erlaubt `TimedActions/` unter allen dreien |
| Texte | `42/media/lua/shared/Translate/<L>/UI.json`, `Sandbox.json`, `Tooltip.json` fuer EN, PTBR, RU, KO, ES, CN, FR; **keine `IG_UI.json`, keine `ItemName.json`, keine `ContextMenu.json`** | `UI_BN_Bear_*` nach `UI.json`; Tiernamen brauchen `IG_UI.json` = in NPC Crew eine NEUE Datei (Regel `../CLAUDE.md` Abschnitt 7 "Naht zum Crew Backpack": wer spaeter kommt, fuehrt sortiert zusammen, legt nie neu an) |
| Text-Stand | je Sprache 3801 Schluessel `UI.json`, 92 `Sandbox.json`, 2 `Tooltip.json`; alle 21 Dateien Round-Trip-gleich (`json.dumps(indent=4, ensure_ascii=False) + "\n"`), sortiert, LF, kein BOM (selbst gemessen) | genau dieses Format schreiben |
| Text-Helfer | `BanditsNPC.T(key, fallback)` (`NC/shared/BanditsNPC.lua:2836`): englischer Ersatztext im Code | in der Test-Mod ohne NPC Crew eigener Helfer hinter Existenz-Riegel (zur Laufzeit holen, nie auf Dateiebene) |
| Sandbox | EINE Datei `42/media/sandbox-options.txt` (LF, Tabs, 42 Optionen, `VERSION = 1,` am Kopf, **nur C-Kommentare `/* */`**, `:28-31`); Form `option BanditsNPC.<Name> { type = ..., default = ..., page = BanditsNPC, translation = BanditsNPC_<Name>, }`; Arten boolean, integer (min/max), double, enum (`numValues`, `valueTranslation`), string (`:150-175`) | Optionen `BanditsNPC.Bear<Name>` in einer eigenen `sandbox-options.txt` der Test-Mod |
| Sandbox-Texte | `Sandbox_BanditsNPC` = "NPC Crew" (Seitentitel, in ALLEN sieben Sprachen wortgleich "NPC Crew"), `Sandbox_BanditsNPC_<Name>`, `_tooltip`, `_option1..n` (`Translate/EN/Sandbox.json`) | mit `page = BanditsNPC` muss die Test-Mod `Sandbox_BanditsNPC` = "NPC Crew" selbst mitbringen (gleicher Wert = keine Kollision, `TU:538-541`); eine eigene Seite braeuchte einen eigenen Titel-Schluessel |
| Sandbox lesen | `BanditsNPC.Opt(name, default)` (`NC/shared/BanditsNPC.lua:6101-6109`: Weltregel-Speicher vor `SandboxVars.BanditsNPC[name]`) | ohne NPC Crew `SandboxVars.BanditsNPC` direkt, mit Riegel; mit NPC Crew `Opt` zur Laufzeit |
| Melden | `BanditsNPC.Log(...)` nur ab Crew logging 2 (`:156-159`), `BanditsNPC.Err(...)` immer (`:187-190`), `LogEvery`/`ErrEvery` gedrosselt | Form `T.Log`/`T.Err` aus `TT/.../BanditsNPCTurret.lua:90-115` (eigener Schalter ODER `BanditsNPC.DIAG`) |
| Skripte, Modelle | `42/media/scripts/*.txt`; NPC Crew hat KEIN `models_X`, kein `sound`, kein `textures/Body`, kein `42/media/AnimSets` (nur `common/media/AnimSets`, `common/media/anims_X`) | Baeren-Ordner entstehen bei der Uebernahme neu; AnimSets des Baeren liegen heute unter `42/media/AnimSets/buck/idle` (gespielt) -- Ablage bei der Uebernahme entscheiden (spaeter, kein B1a-Thema) |
| mod.info | `id=NPCCrew`, `require=Bandits2` | Test-Mod: NPC Crew und Bandits bleiben optional (kein `require`) |

---

## 4. Vorbild Turret

### 4.1 Aufbau von `turret/tools/turret_uebernahme.py` (1566 Zeilen) und was der Baer anders braucht

Ablauf (`TU:18-55`, `main` `TU:1450-1562`): Quelle einordnen -> Texte planen -> Naht-Zeilen -> Kollisionen -> Cheat-Pruefung;
geschrieben wird erst, wenn ALLES fehlerfrei ist.

| Teil | Turret | Fundstelle |
|---|---|---|
| Modi | ohne Schalter Trockenlauf (schreibt nichts); `--probe <ordner>` baut `<ordner>/NPCCrew` aus NC-Lua, Skripten, AnimSets, `sandbox-options.txt`, `mod.info` und schreibt dort echt, danach die vier Pruefer; `--echt` nur mit `--ja-kevin-hat-es-gesagt`, bricht ab, wenn das Spiel laeuft | `TU:1417-1447`, `:1486-1512`, `:1409-1414` |
| Probe-Schutz | Probe-Ordner nie unter `Zomboid`, NPC Crew oder der Test-Mod; Marke `.turret_probe`, sonst wird nichts geloescht | `TU:1417-1434` |
| Einordnen | `mod.info`, `.git*` und jede Datei `NCTurretBench*` (jede Endung, jeder Ordner) werden uebersprungen; `Translate/<L>/*.json` zusammengefuehrt; Lua nur `BanditsNPCTurret*.lua` in `shared|client|server` (+ `ISUI/`, `TimedActions/`); Assets nur mit Turret-Namen; **alles andere ist ein Fehler** | `TU:303-336`, Muster `:93-107` |
| Lua-Form | neue Lua: kein CR, reines ASCII, keine Zeile endet mit `\` | `TU:1344-1352` |
| Texte | alle sieben Sprachen Pflicht, gleiche Schluessel, EN `singleplayer`/`multiplayer` zusammen, Platzhalter `%1`/`<LINE>` gleich, CN nur Vanilla-CN-Zeichen, Ziel muss Round-Trip-gleich sein, neue Schluessel sortiert einfuegen (nie die Datei neu sortieren), vorhandener Schluessel mit anderem Wert = Kollision, fehlende Zieldatei wird sortiert neu angelegt, Paritaet danach | `TU:468-587`, `dump_json` `:445-446` |
| Naht-Zeilen | maschinell aus `NAEHTE.md` Abschnitt "Die Zeilen": Anker genau einmal, Zeilenenden der Zieldatei bleiben | `TU:593-733`, Format `TN:100-112` |
| Kollisionen | eigene Namen (`OWN_NAME_RES`) in NPC Crew = Kollision, ausser erlaubten Fundstellen (`NC_ALLOWED`: ganze Code-Zeile, Hoechstzahl, Pflicht); nur im Kommentar = Warnung | `TU:87-91`, `:113-117`, `:761-960` |
| Cheat-Pruefung | Code-Teil jeder kopierten Lua-Zeile und Naht-Zeile, Dateinamen, Textschluessel, EN-Texte: Testbefehl `NC[A-Z]..._...`, bench/cheat/testmodus, `debug` in jeder Form, Admin-Rechte, Tasten/Maus-Ereignisse, Engine-Cheats, `_G`, globale Funktion/Zuweisung, Gegenstand erzeugen (`instanceItem`, `AddItem`), Menue-Eintrag mit festem Text statt Textschluessel, Fingerabdruck der Werkbank; Ausnahmen einzeln mit Grund (`CHEAT_ALLOWED`); Spawn-Weg nur ueber benannte Aufrufer (`SPAWN_CALLERS`) | `TU:119-212`, `:1069-1258` |
| Schalter fuer die Bauzeit | `--vor-t10`: Cheat-Funde nur Warnung; mit `--echt` verboten | `TU:1480-1494` |
| Pruefer danach | `luacheck.py`, `scopecheck.py`, `localcount.py`, `luacheck_pz.py` je kopierter Lua | `TU:1279-1336` |
| Mutationsprobe | `turret_uebernahme_probe.py`: je Fall eine Mutation, Durchschluepfer muessen rot werden, echte Formen duerfen nichts Neues melden | Kopf `turret_uebernahme_probe.py:1-22` |

**Was `baer_uebernahme.py` zusaetzlich oder anders koennen muss:**
1. **Sandbox zusammenfuehren.** Das Turret-Skript bricht bei `sandbox-options.txt` ab (`TU:329-330`, "T6 baut es"). Neu:
   `option BanditsNPC.Bear*`-Bloecke an NPC Crews Datei anhaengen (LF, Tabs, nur C-Kommentare), Abbruch bei vorhandenem
   Optionsnamen; `Sandbox.json` laeuft ueber die allgemeine Textzusammenfuehrung.
2. **`IG_UI.json`** ist in NPC Crew neu: der Zweig "Zieldatei fehlt" (`TU:561-564`) legt sie sortiert an; hat inzwischen ein
   anderes Projekt sie angelegt, greift der Zusammenfuehr-Zweig. Schluessel-Muster dafuer: `IGUI_AnimalType_ncbear*`,
   `IGUI_Animal_Group_...`, `IGUI_Breed_...` (tragen kein `Bear_`, die Turret-Warnung "Schluessel ohne Thema" `TU:506-507`
   anpassen).
3. **Alte Dateien bis B5a.** `NCBearDefs.lua`, `NCBearFight.lua`, `NCBearSpawn.lua`, `NCBearSize.lua`, `NCBearAttackProbe.lua`,
   `NCBearTest.lua` heissen weder `BanditsNPCBear*` noch `NCBearBench*` -> nach Turret-Regel Fehler ("Lua-Datei ohne den Namen",
   `TU:327-328`). Vorschlag: benannte Alt-Liste, mit Schalter (Form `--vor-t10`, z. B. `--vor-b5a`) nur Warnung, mit `--echt`
   immer Fehler. Der Trockenlauf ohne Schalter ist dann absichtlich rot (wie beim Turret, `../CLAUDE.md` Abschnitt 7).
4. **Asset-Muster:** `^(NCBear|nc_bear|Item_NCBear)`; AnimSets-Regel fuer `42/media/AnimSets/buck/idle/NCBear_*.xml`. Die
   Turret-Pruefung "jeder Clip liegt als `.x` in Vanilla `anims_X/Bob`" (`TU:347-426`) passt nicht: beim Baeren liegen die Clips
   IM GLB -- gegen die Animationsnamen im GLB-JSON pruefen (`NCBear.glb` und `NCBearCub.glb`).
5. **Regel `befehl`** (`\bNC[A-Z][A-Za-z]*_[A-Za-z]\w*`, `TU:123`) trifft beim Baeren echte Asset-Namen in Lua-Strings:
   `NCBearCub_Body`, `NCBear_Body`, Clip-Namen `NCBear_Eat`, Ton-Namen `NCBear_Pain` ... Entweder eine Erlaubt-Liste aus den
   Skripten und GLBs ableiten (model/animationsMesh/sound/Clip) oder die Regel auf bekannte Testbefehle plus Aufruf-Form
   beschraenken.
6. **Spawn-Regel fuer Tiere:** das Gegenstueck zu "Gegenstand erzeugen" ist `addAnimal(`. Erlaubt nur in benannten Funktionen des
   Schreibers (Wald-Wuerfel, Koederplatz; SP bzw. Server), nie in `client/`, nie aus einem Menue erreichbar -- Liste nach Form
   `SPAWN_CALLERS` (`TU:171-176`). Dasselbe fuer das Entfernen eines Tiers (Verschwinde-Regel).
7. **Eigene Namen fuer die Kollision:** `BanditsNPC\.Bear\b`, `BanditsNPCBear`, `TrueCompanionsBears`, `TC-BEAR`, `UI_BN_Bear_`,
   `NCBear`, `ncbear`, `\btcBear\b`, `nc_bear` -- mit den Vorsilben-Fallen aus 3.1.
8. **Alte Test-Texte:** `IGUI_AnimalType_bear` = "Brown bear (test)", `IGUI_Animal_Group_bear` = "Bear (NC test)" treffen
   `CHEAT_TEXT` (`\btest`, `TU:152`). Bis B5a als benannte Alt-Schluessel fuehren.
9. Nicht kopieren: `mod.info`, `.git`, `.gitattributes` (`TU:107`, `../CLAUDE.md` Abschnitt 9).

### 4.2 Aufbau von `turret/NAEHTE.md`

1. Kopf mit Stand (NPC-Crew-Version) und DER Regel (`TN:3-5`): alles zur Laufzeit in EINER Naht-Datei (`shared/BanditsNPCTurretCrew.lua`),
   hinter Existenz-Riegeln; **jeder Aufsatz und jeder Tabelleneintrag in `Events.OnGameBoot`, nichts auf Dateiebene**, weil Lua je
   Mod in der Reihenfolge der Mod-Liste laedt und nur innerhalb einer Mod alphabetisch (Jar `LuaManager.LoadDirBase`); genau
   einmal einhaengen; kein `BanditsNPC.X` auf Dateiebene einfangen.
2. `## Tabelle` (`TN:11-98`): je Naht Nummer, Stelle, Fundstelle (Datei:Zeile), "Von aussen?", Wie, ab welcher Version -- auch die
   Zeilen "Nicht noetig" mit Grund.
3. `## Die Zeilen` (`TN:100-153`): maschinenlesbar -- `**Zn**`, Datei in Backticks, Anker in Backticks, `davor`/`danach`, genau ein
   lua-Codeblock. Nur fuer das, was sich NICHT von aussen aufsetzen laesst.
4. `## Wo der Pluenderer stoert` (`TN:155-164`): Reibung mit laufenden NPC-Crew-Bauten.
5. `## Erlaubte Fundstellen und Cheat-Ausnahmen` (`TN:166-196`): jede Ausnahme mit Grund, doppelt gefuehrt (hier und im Skript).
6. `## Vorschlaege, nicht bauen` (`TN:198 ff.`).

Vorbild der Naht-Datei: `TT/lua/shared/BanditsNPCTurretCrew.lua:1-52` (Riegel `if not F then return end`, laute `***`-Zeile, wenn
NPC Crew da ist, aber das Feld fehlt; Original mit allen Argumenten weiterreichen), `:228-234` (`installed`-Riegel,
`Events.OnGameBoot.Add`).

### 4.3 Wie die Bench-Dateien getrennt sind

- `TT/lua/client/NCTurretBench.lua`, `...BenchCrew.lua`, `...BenchKnock.lua`, `...BenchRocket.lua`: nur `client/`, Kopf "TESTHILFE,
  wird NICHT nach NPC Crew kopiert ... Kein Kern-Code ruft diese Datei" (`NCTurretBench.lua:1-3`).
- Sie holen dasselbe Modul (`BanditsNPC.Turret`, `:12-14`) und haengen sich in `OnGameBoot` VOR das, was der Kern schon gesetzt
  hat (ketten, nie ersetzen, `:30-32`). Der Kern kennt die Bank nicht.
- Konsolenbefehle `NCTurret_*`, Rechtsklick-Untermenue "NC Turret", englische feste Texte, `print("[NCTurret] ...")` -- alles nur
  dort. Im Kern: keine globale Funktion, Meldungen nur ueber `T.Log`/`T.Err`.
- Geteilte Speicher ohne NPC Crews `SharedStore`: eigene Annahme (`TT/lua/shared/BanditsNPCTurretWorld.lua:22-81`:
  `ModData.getOrCreate`, Server `ModData.transmit`, Client `ModData.request`, `OnInitGlobalModData`, `OnReceiveGlobalModData`,
  Fuellen in place; Beleg dort Bandits `shared/BanditGMD.lua`), entschieden in `TN:50` (#36).
- Server-Datei: `TT/lua/server/BanditsNPCTurretServer.lua:33-67` -- `Events.OnClientCommand`, erste Zeilen `if module ~= T.CMD`,
  `if not isServer()`, `type(args) ~= "table"`; Ablehnung mit Grund ueber `sendServerCommand(player, T.CMD, "Refused", ...)`.
  Kopf-Hinweis `:4-5`: `server/` laedt auch im SP und auf dem MP-Client mit.
- `mod.info` der Turret-Test-Mod traegt `loadModAfter=NPCCrew` (NCBearTest nicht).

### 4.4 Sandbox und Texte beim Turret

- Texte: `TT/lua/shared/Translate/<L>/UI.json` in allen sieben Sprachen, 9 Schluessel `UI_BN_Turret_*` plus `UI_BN_Prog_Turret`.
- **Sandbox: die Turret-Test-Mod hat KEINE `sandbox-options.txt`** (Dateiliste). Geplant sind `BanditsNPC.TurretsEnabled`,
  `.RocketsEnabled`, `.TurretL3Mobile` (`TN:51`, #37). Vorbild fuer die Sandbox ist deshalb nur NPC Crew selbst (3.2).

---

## 5. Naehte zu NPC Crew (nur gelesen, Stand v3.14.67 laut `NC/shared/BanditsNPC.lua:1347`)

### 5.1 Neue Tierart und die Tierpflege

- **`client/ISUI/BanditsNPCLivestockPanel.lua:4074-4090` (`PF.hookGroup`)** liest `AnimalDefinitions.animals` in einem `pcall` und
  merkt je `group`, ob eine ihrer Arten eine Vanilla-Haken-Art ist (`Lv.IsHookType(typ)`). Eine neue Art/Gruppe, die keine
  Haken-Art ist, aendert nichts. Harmlos.
- **Ernst ist die Regel dahinter:** `Lv.NOT_TENDED = { rabbit, mouse, rat, raccoon, deer }` (`NC/shared/BanditsNPCLivestock.lua:5152`,
  Schluessel = GRUPPE). Jedes Tier in einer NPC-Crew-Tierzone mit anderer Gruppe gilt als gepflegt:
  zaehlt als Vieh (`:1868-1880`), darf gestreichelt werden, wenn `canBePet` und nicht `wild`
  (`shared/BanditsNPCLivestockPet.lua:188-203`, der Kern ruft `a:petAnimal(chr)` `:466`), steht im Schlachtplan
  (`shared/BanditsNPCLivestockSlaughter.lua:548-550` `row.tended`), in Herde, Futter, Uhr (Leser u. a.
  `BanditsNPCLivestockHerd.lua:199`, `...Clock.lua:151`, `...Butcher.lua:538`, `server/BanditsNPCLivestockHerdServer.lua:515`).
  Eine Art OHNE Definition oder Gruppe zaehlt ebenfalls ("sichere Richtung", `:1837`). Bekannt fuer den Erwachsenen seit
  `baer/spiel/tier_spez.md:352-355`.
- **Naht N1 (noetig, sobald ein Junges in eine NPC-Crew-Tierzone geraten kann):** in `Events.OnGameBoot`, hinter Riegel
  `BanditsNPC.Livestock and type(BanditsNPC.Livestock.NOT_TENDED) == "table"`, die Gruppe(n) des Baeren eintragen. Die Tabelle
  ist exportiert (`BanditsNPC.Livestock`, `:107-108`) und wird auf Dateiebene als Literal gesetzt (`:5152`) -- ein Eintrag VOR
  dem Laden von NPC Crew ginge verloren, deshalb `OnGameBoot`. Alle gelesenen Leser fragen zur Laufzeit (`Lv.NOT_TENDED or {}`
  in Funktionen). Keine NPC-Crew-Datei wird geaendert. **Ob jeder Leser ueber das Feld geht, hat diese Forschung nur an den
  genannten Stellen gesehen** -- der Bauer wiederholt den grep `NOT_TENDED` (25 Treffer).
- **`shared/BanditsNPCAnimals.lua:51-89` (`A.ApplyNoFear`)**: setzt fuer JEDE Art ohne `wild == true` `fleeZombies = false`, auf
  Dateiebene und in `OnGameBoot`. Mit NPC Crew flieht ein nicht wildes Junges also nie vor Zombies, gleich was unsere Definition
  sagt; ohne NPC Crew gilt unser Wert. Damit beide Faelle gleich sind: `fleeZombies = false` selbst setzen (wie
  `NCBearDefs.lua:88`) -- das "Verstecken hinter dem Besitzer" (G5) wird spaeter eigener Code, kein Engine-Schalter. Mit
  `wild = true` liesse NPC Crew die Art aus (`:57-58`), aber `wild` aendert Vanillas Menue ("Animal info" gesperrt, kein "Kill",
  `V/client/ISUI/Animal/ISAnimalContextMenu.lua:166-171`, `:307`) und das Engine-Verhalten -- Sache der Engine-Forschung.
- `client/BanditsNPCPortrait.lua:324` liest `AnimalAvatarDefinition[animal:getAnimalType()]` -- noch ein Grund fuer den
  Avatar-Eintrag (2.3).
- **Koeder am Boden (Weg C):** NPC-Crew-Figuren heben Bodengegenstaende auf: die Foersterin JEDEN Gegenstand ihrer Pflanzflaeche,
  den ihre Liste nicht "liegen lassen" nennt (`TN:54` #40 a: `shared/BanditsNPCForestry.lua:1326` "Absent means take"; eine Regel
  "loeschen" vernichtet), der Pluenderer in Lootflaechen (`TN:53` #39, `TN:161`). Ein Honigglas als Koeder im Wald kann also von
  der Crew eingesammelt werden. Das ist kein Verlust im Sinn der roten Linie (das Stueck liegt dann im Lager), aber der
  Koederplatz muss "Koeder ist weg" ohne Fehler vertragen und darf nichts nachlegen. Der Koeder ist ein Vanilla-Gegenstand: ein
  Aufsatz wie beim Turret (Typ-Regel) passt nicht; ein Schutz waere eine eigene Entscheidung (Kevin).

### 5.2 Wie NPC Crew sich Besitzer/Spieler im MP merkt (Muster fuer das Register)

- **Besitzer-Schluessel:** im MP der Benutzername `p:getUsername()`, auf Client UND Server massgeblich; im SP eine feste Kennung
  (`BanditsNPC.PlayerId` gibt 1, `NC/shared/BanditsNPC.lua:6295-6310`; `ownerMatches` `:6312-6343`). Grund: `getUsername()` ist
  im SP der Charaktername und aendert sich nach dem Spielertod (NC-CLAUDE:3442-3446, :3472-3476: "jeder Vergleich ohne
  `isClient()`-Riegel ist im SP ein Vergleich mit dem Charakternamen"). Vanilla-Beleg fuer den Aufruf am Server:
  `V/server/ClientCommands.lua:149` `player:getUsername()`, `V/server/BuildingObjects/ISBuildUtil.lua:15`. Die Online-Id ist nur
  eine Sitzungsnummer (`recherche_spiel.md:248-250`).
- **Tier ueber das Netz benennen:** das Paar `aid` = `getAnimalID()` (gespeichert, auf Client und Server gleich, NC-Sonde "gleich
  5, verschieden 0", `recherche_spiel.md:251-252`) plus `oid` = `getOnlineID()`; der Server sucht das Tier SELBST
  (`Lv.AnimalByPair`, `NC/shared/BanditsNPCLivestockAnimalOps.lua:959`): 0 Treffer "gone", mehrere "ambiguous", nie geraten; die
  Kachel aus dem Paket ist nur ein Hinweis, Anker ist die Kachel beim SERVER (weiter als 8 Kacheln = "moved"); "kein else, das
  eine unbekannte Form annimmt"; jede Ablehnung mit Grund (`NC/server/BanditsNPCLivestockServer.lua:714-728`). Vanilla-Belege:
  `animal:getAnimalID()` `V/client/ISUI/Animal/ISAnimalUI.lua:53`, `V/client/ISUI/ISVehicleAnimalUI.lua:202`;
  `getAnimal(tonumber(args.id))` am Server `V/server/ClientCommands.lua:817`.
- **Geteilter Speicher:** `ModData.getOrCreate(key)` ist je Spielstand (NC-CLAUDE:4008). Ein MP-Client bekommt eine geteilte
  Tabelle nur mit `ModData.request` UND `OnReceiveGlobalModData`; ein Paket baut eine FRISCHE Tabelle und ueberschreibt die des
  Empfaengers nicht (`NC/shared/BanditsNPCSharedStore.lua:8-38`; NC-CLAUDE:1915-1929). Fuer den Baeren nach Turret-Entscheid
  (`TN:50`) eine eigene Annahme, kein `S.Register` (muss ohne NPC Crew laufen). Frage an den Plan: braucht der Client das ganze
  Register ueberhaupt? Fuer Balken und Menue reichen der Spiegel am Tier und Antworten des Servers; dann erfaehrt kein Client
  fremde Zeilen.
- **Speichern:** der dedizierte Server speichert nicht von selbst (`SaveWorldEveryMinutes` 0 in der Vorlage, NC-CLAUDE:1957-1964).
  Ein Register im globalen Speicher lebt nur so sicher wie der Weltstand.
- **Eigene Client-Befehle kicken nicht:** `sendClientCommand` braucht nur `LoginOnServer` (NC-Changelog v3.14.67,
  `NC/shared/BanditsNPC.lua:1347`: "ClientCommand, capability LoginOnServer, so no kick for role user"). Gekickt wird bei Paketen
  mit Faehigkeit (Rolle `user` hat keine, `AntiCheatPermission` Vorgabe 2 = Kick, NC-CLAUDE:1604-1611) -- z. B. Vanillas
  `animal.add` verlangt `Capability.AnimalCheats` (`V/server/ClientCommands.lua:803-811`). Der Server ruft `addAnimal` selbst.
- **Tier erzeugen, Vanilla-Form:** `local breed = AnimalDefinitions.getDef(args.type):getBreedByName(args.breed)`;
  `addAnimal(getCell(), x, y, z, type, breed, skeleton)`; `animal:addToWorld()` (`V/server/ClientCommands.lua:808-810` am Server,
  `V/client/DebugUIs/DebugContextMenu.lua:1460-1467` im SP; heute schon `NCBearSpawn.lua:51-56`).
- **Jeder Empfaenger prueft den Besitz selbst** (NC-CLAUDE:2655-2690, v3.7.53: zwei Tueren in derselben Datei, nur eine hatte den
  Riegel).

### 5.3 Wo NPC Crew Namen/Balken ueber Figuren zeichnet (Muster fuer den Zaehm-Balken)

`NC/client/ISUI/BanditsNPCNameTags.lua` (1498 Zeilen), Kopf `:1-60`:
- Ein `ISPanel:derive`-Element (`:136`), **1 x 1 Pixel in der Ecke**, das in `prerender` (`:1145-1150`, Eltern-`prerender`
  zuerst) ueber den ganzen Bildschirm zeichnet; ein UI-Element wird nicht auf seine Flaeche beschnitten (Vanilla
  `ISButtonPrompt.lua:1244`). Klein bleiben, weil ein grosses Element jeden Weltklick frisst (`:46-54`). **Nie unsichtbar
  schalten** (ein unsichtbares Element erreicht `prerender` nie wieder, `:56-60`): Ein/Aus im Zeichencode.
- Angelegt in `OnGameStart` (`:1187-1191`, `addToUIManager`).
- Ort: `isoToScreenX(playerIndex, x, y, z)` / `isoToScreenY(...)`, erstes Argument eine ZAHL (`:24-29`; Vanilla
  `V/client/Fishing/TensionUI.lua:11-12`, `client/Foraging/ISBaseIcon.lua:167`); die Rueckgabe enthaelt den
  Ansichtsfenster-Ursprung (`:128`); keine Zoom-Division fuer den Anker (`:96`).
- Text: `self:drawTextCentre(str, x, y, r, g, b, a, font)` (`V/client/ISUI/ISUIElement.lua:1280`), Schatten = zweimal zeichnen
  (`:1022-1035`). Sicht: `square:isCanSee(playerIndex)` (`:34`).
- Balken (NameTags zeichnet keine): Vanilla `ISUIElement:drawRect(x, y, w, h, a, r, g, b)` (`ISUIElement.lua:1191`),
  `drawRectBorder` (`:1219`), `drawProgressBar(x, y, w, h, f, fg)` (`:1805`); in NPC Crew z. B.
  `client/ISUI/BanditsNPCAmmoHUD.lua`, `BanditsNPCBeaconPrompt.lua`.
- Nichts Teures im `render()`; abgeleiteter Zustand in einen Zwischenspeicher mit Verfallszeit (NC-CLAUDE:4021-4022).
- `client/ISUI/` laedt alphabetisch: nie auf Dateiebene ein anderes Modul einfangen (NC-CLAUDE:750-752).

### 5.4 Lehren aus NPC Crews CLAUDE.md, die hier gelten

| Lehre | Fundstelle |
|---|---|
| 200 Locals je Funktion, mit `-debug` zaehlt die SUMME aller je angelegten (auch in geschlossenen Bloecken); Kevin spielt immer mit `-debug`; ab 180 aufteilen; `localcount.py` meldet beide | NC-CLAUDE:736-749 |
| Kahlua hat kein `next`; ein `pcall` darum macht den Fehler unsichtbar; "Tabelle leer" ueber `pairs` oder `table.isempty`; vor jedem neuen Global-Namen in Vanilla greppen | NC-CLAUDE:1152-1161 |
| `and` kappt Mehrfachrueckgaben (`local a, b = f and f(...)` liefert einen Wert); Mehrfachrueckgaben erst in Locals | NC-CLAUDE:763-764 |
| Kahlua-Zeichenklassen: `%a` ist nirgends belegt, `[%l%u]` nehmen | `NC/shared/BanditsNPC.lua:6118-6123` |
| SP-Test mit BEIDEN Negationen; `getUsername()` im SP = Charaktername | NC-CLAUDE:3442-3446, :3472-3477 |
| Der MP-Client laedt `media/lua/server` mit; "Funktion ist erreichbar" ist kein Server-Beweis | NC-CLAUDE:1942-1943; `TT/lua/server/BanditsNPCTurretServer.lua:4-5` |
| `OnZombieUpdate` feuert auf dem dedizierten Server nie -- Server-Takte ueber `OnTick`/`EveryOneMinute` | NC-CLAUDE:3094-3095 |
| Kick: Pakete mit Faehigkeit von einem `user`-Client; Kevin war dreifach abgeschirmt (admin) -- mit Rolle `user` gegenpruefen | NC-CLAUDE:1600-1616 |
| Nie `AddItem` + `Remove` ohne den Add zu pruefen; erst erzeugen, dann aufraeumen kostete 252 Gegenstaende; wer nimmt, ist der Server | NC-CLAUDE:765-767, :2476-2477 |
| Vanilla-Aktionen mit Weltwirkung sind Netzwerkaktionen: der Client spielt nur Effekte, gewirkt wird am Server | NC-CLAUDE:2071-2075, :2478-2482 |
| Geteilter Speicher braucht `request` + `OnReceiveGlobalModData`; reine Client-Einstellungen gehoeren in eine Datei, nicht in ModData | NC-CLAUDE:1915-1929, :1898 |
| Genau einmal einhaengen (doppelter Aufsatz = Endlosschleife) | NC-CLAUDE:3241-3252 (v3.9.55) |
| Jede Sonde haengt an der Sandbox-Einstellung, nie an einem nackten `print`; echte Fehler laufen immer | NC-CLAUDE:4094-4099; `BanditsNPC.Log`/`Err` |
| Nichts Teures im `render()` | NC-CLAUDE:4021-4022 |
| Das Spiel haelt 152 x 152 Kacheln um den Spieler geladen | NC-CLAUDE:803 |
| Eine Antwort je Frage (zwei Kopien derselben Pruefung laufen auseinander) | NC-CLAUDE passim (v3.4.3), z. B. `NC/shared/BanditsNPCSharedStore.lua:20-24` |

---

## 6. Fallen fuer die Bauer

**Kahlua und Lua**
1. Kein `next`, kein `%a`; `string.format`, `math.atan2`, `table.sort`, `ipairs`, `pairs` sind im Bestand benutzt
   (`NCBearFight.lua:240`, `:260`, `:399`).
2. 200 Locals je Funktion, mit `-debug` in Summe (5.4). Grosse Funktionen frueh teilen.
3. Mehrfachrueckgaben erst in Locals; `and` kappt sie.
4. Ein `pcall` um einen unbelegten Engine-Aufruf ist eine Tarnkappe. NPC Crew ist KEIN Beleg im Sinn der eisernen Regel (nur
   Vanilla-Lua und Bandits) -- z. B. `petAnimal(chr)` steht in `NC/.../BanditsNPCLivestockPet.lua:466`, der zaehlende Beleg ist
   Vanilla (`ISPetAnimal.lua`, von der Engine-Forschung zu liefern).
5. Bandits-Belege gegen Ordner `42.22` + `common` (0.1); `BanditUtils.lua` weicht gegen `42.21` ab, Zeilen koennen wandern.

**Laden**
6. Reihenfolge: je Mod in der Reihenfolge der Mod-Liste, innerhalb einer Mod alphabetisch ohne Gross/Klein (`TN:5`, Jar
   `LuaManager.LoadDirBase`); `shared` vor `client` vor `server`. Auf Dateiebene nie ein fremdes Modul einfangen
   (`local X = BanditsNPC.Y` ganz oben), auch kein eigenes aus einer anderen Datei, wenn die Reihenfolge nicht sicher ist.
7. Nach der Uebernahme (eine Mod) laden `BanditsNPCBear*.lua` NACH `BanditsNPC.lua`, `BanditsNPCAnimals.lua`,
   `BanditsNPCBeacon*.lua`, aber VOR `BanditsNPCLivestock*.lua` -- `BanditsNPC.Livestock` gibt es auf Dateiebene dann noch nicht.
   Naehte nur in `OnGameBoot`.
8. `AnimalDefinitions` liest Java erst in `IsoWorld.init`, nach allen Lua-Dateien und nach `OnGameBoot` (`NCBearDefs.lua:7`;
   `NC/shared/BanditsNPCAnimals.lua:15-18`). Die Definition gehoert auf Dateiebene einer `shared`-Datei (wie
   `NCBearDefs.lua:101-102`); spaetere Aenderungen an der Lua-Tabelle (nach Weltstart) sieht die Engine nicht mehr.
   Sandbox-Werte koennen die Definition deshalb nicht zur Laufzeit aendern.
9. `server/` laedt auch im SP und auf dem MP-Client: jeder Server-Handler beginnt mit `if not isServer() then return end` bzw.
   der Schreiber-Frage `not isClient()` (SP und Server). SP-Test: `not isServer() and not isClient()`.
10. `Events.OnGameStart` feuert auf dem dedizierten Server nie (`NC/shared/BanditsNPCAnimals.lua:82-83`); dort
    `OnInitGlobalModData`/`OnServerStarted`/`OnTick`. Welche belegt sind: Engine-Forschung.

**Dateien**
11. Neue Lua: LF, reines ASCII, keine Zeile endet mit `\` (`TU:1344-1352`). Zeilenenden mit Python an den Bytes pruefen --
    **`grep -c $'\r'` in Git Bash zaehlte hier JEDE Zeile als Treffer** (falscher Alarm bei dieser Forschung).
12. `sandbox-options.txt`: nur C-Kommentare `/* */`; ein unlesbarer Kommentar nimmt die ganze Seite mit
    (`NC .../sandbox-options.txt:28-31`).
13. JSON-Texte: ein Syntaxfehler wirft beim Laden hart (`RuntimeException("JSON Error in: ...")`, `altdec/Translator.java:325-343`).
    Format `json.dumps(indent=4, ensure_ascii=False) + "\n"`, UTF-8 ohne BOM, sortiert. `%1`..`%9` sind Platzhalter, ein
    woertliches Prozent ist `%%` (`altdec/Translator.java:881`; NC-Beispiel "dodge chance %%"). CN nur Zeichen aus Vanilla-CN
    (`TU:428-442`, `:512-517`). EN: `singleplayer`/`multiplayer` zusammen.
14. Schluessel-Vorsilbe entscheidet die Datei: `UI_` -> `UI.json`, `IGUI_` -> `IG_UI.json`, `Sandbox_` -> `Sandbox.json`,
    `ContextMenu_` -> `ContextMenu.json`, `Tooltip_` -> `Tooltip.json` (`altdec/Translator.java:397-445`). Ein `UI_BN_`-Schluessel in
    einer anderen Datei wird nie gefunden.
15. `EN/IG_UI.json` der Test-Mod: die 4 alten Schluessel muessen in der Staging-Fassung unveraendert stehen bleiben (2.3).
16. Menue-Eintraege im Kern nur mit Textschluessel (`getText`/Helfer mit `"UI_..."`), nie mit festem Text (`TU:155-164`); keine
    globale Funktion, kein `_G`, kein `print("[NCBear] ...")` im Kern.

**Tiere und Welt**
17. Artname endgueltig; ein gespeichertes Tier einer unbekannten Art bricht das Laden (`tier_spez.md:417`). B1a legt Junge von
    selbst in die Welt -> in Kevins echtem Spielstand nur, wenn er das weiss.
18. Tier-Objekte nie merken: Anhaenger und (spaeter) Wachsen bauen ein neues Objekt (`KRIT:74-79`, `SPEZ:211-216`); Wiederfinden
    ueber `getAnimalID()`. Der alte Code zeigt das Muster "gemerkt, aber `gone()` pruefen" (`NCBearFight.lua:1762-1764`:
    `isExistInTheWorld()`, `isDead()`).
19. `getCell():getObjectListForLua()` kopiert die ganze Menge -- selten rufen (`NCBearFight.lua:125`: alle 5 s). `getObjectList()`
    ist ein HashSet ohne `get(i)` (`NC/shared/BanditsNPCAnimals.lua:117-119`).
20. Im MP rechnet der Server das Tier; was ein Client lokal am Tier aendert, ueberschreibt das naechste Paket; Groesse und
    ModData kommen nicht laufend zum Client (`recherche_spiel.md:281-286`). Anim-Variablen muss jeder Client an seiner Kopie
    setzen (`PLAN:224`) -- eine Fress-Animation im MP ist ohne eigenen Weg nicht sichtbar (offen).
21. Jeder Client kann Tier-ModData ueberschreiben (`KRIT:53-62`): der Server liest seine Wahrheit nie aus dem Spiegel zurueck,
    unser Client ruft `transmitModData` am Tier nie.
22. Die Knoten `NCBear_*.xml` liegen unter `buck/idle`: sie spielen nur im Zustand idle; die Engine laesst das Tier wandern
    (`wanderMul`, `NCBearDefs.lua:95`) und bei Laerm fliehen (`NCBearFight.lua:28-38`) und startet den Clip dann neu.
23. Ob der dedizierte Server das `.glb` laedt: ungeprueft (`tier_spez.md:416`) -- MP-Risiko fuer jede Tierart mit GLB.
24. Tierzone: `updateStatsAway` -> `AnimalData.init` setzt die Groesse auf `minSize` (`KRIT:25-34`) -- mit `minSize = maxSize`
    beim Jungen ohne Folge.
25. NPC Crew aendert `fleeZombies` fremder Arten (5.1); Verhalten mit und ohne NPC Crew gleich halten.
26. Wasser: auf Wasserkacheln bleibt ein Tier uninitialisiert (`NCBearSpawn.lua:29-33`, `tier_spez.md` 4.1) -- der Fundort-Wuerfel
    braucht dieselbe Pruefung.
27. Nichts weiter als 76 Kacheln vom Spieler; Deckel fuer Register, Koederplaetze, gemerkte Junge; Wuerfeln in grossen
    Abstaenden; Diagnose hinter Schalter.

**Uebernahme**
28. Verbotene Woerter in Namen und Strings (3.1): `spawn`, `debug`, `bench`, `cheat`, `test`, `tune`, `dev`, `admin`, `console`,
    `tweak`. Auch Engine-Methoden mit `Debug` im Namen (`setDebugStress`, `setDebugAcceptance`, `debugForceSit`) waeren Funde.
29. Asset-Namen `NCBear..._...` in Lua-Strings sehen fuer die Turret-Regel wie Testbefehle aus (4.1 Punkt 5) -- im Baeren-Skript
    loesen, nicht im Kern umgehen.
30. Muster mit `UI_BN_Bear_` (Unterstrich) und `\btcBear\b` (3.1).

---

## 7. Offen (fuer Plan bzw. Kevin)

1. Gruppe `ncbear` oder `bear` (3.1).
2. `page = BanditsNPC` (mit eigenem `Sandbox_BanditsNPC` = "NPC Crew") oder eigene Sandbox-Seite (3.2).
3. Braucht die Test-Mod jetzt `loadModAfter=NPCCrew` in beiden `mod.info` (Turret hat es)? `mod.info` ist eine alte Datei; fuer die
   Naht N1 in `OnGameBoot` ist es nicht noetig. Die Beschreibung in `mod.info` nennt nur Testbefehle des Erwachsenen.
4. Vanilla-Menue am Jungen (Toeten, Anleinen, Aufheben, Anhaenger) und Schutz vor Fremden im MP (B9): bauen oder als offen melden.
5. Wer darf im MP ein fremdes wildes bzw. gezaehmtes Junges fuettern/streicheln (Z9).
6. Koeder und NPC-Crew-Figuren (5.1): hinnehmen oder schuetzen.
7. Stimme des Jungen: heute nur die Toene des Erwachsenen (`nc_bear_sounds.txt`); ein Junges mit Erwachsenen-Schmerzlaut --
   hinnehmen oder weglassen (kein Download ohne Kevins Ja).
8. Sieben Sprachen fuer die alten Test-Namen in `IG_UI.json` oder Alt-Schluessel-Liste im Skript (2.3, 4.1 Punkt 8).
9. W7: Option "Baeren je Spieler" ueberhaupt?
10. Unbestaetigte Zahlen (F5, F6, F10, B6, Z3/Z5): alle als Sandbox-Option mit Vorgabe; Kevin beim Test fragen.

Statisch geprueft, nicht gespielt.
