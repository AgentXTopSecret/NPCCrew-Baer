# Bär als Begleiter – was andere Tier-Mods machen (Web-Recherche, 08.11.2026)

**Zweck:** Ideen für Kevins Bären (Baby, wächst, Level, Füttern/Trinken, Tod/Downed, ein Bär je Spieler).
**Nur Ideen, nichts kopieren.** Companion Dogs verbietet ausdrücklich, Inhalte herauszulösen
(`mod.info`, Abschnitt ASSET USAGE). Die Mechanik dahinter wird hier beschrieben, damit wir sie
selbst bauen können. Wo wir eine Idee übernehmen, nennen wir die Herkunft.

**Quellen und Grenzen:**
* Steam selbst hat jeden Abruf mit **429** abgewiesen (Beschreibungen und Kommentare). Die Angaben
  kommen deshalb von **top-mods.com** (Spiegel der Workshop-Seiten) und aus den **lokal installierten**
  Mods. Die lokal gelesenen Stellen haben eine Fundstelle (Datei:Zeile).
* **Kommentare unter den Mods konnte ich nicht lesen** – die "bekannten Probleme" unten stammen aus den
  Beschreibungen, nicht aus Spielerberichten. Das ist **ungeprüft**.
* Lokal gelesen: Companion Dogs 0.7.4 (`workshop/content/108600/3740052292`), Horse Mod 1.1.2
  (`.../3661336777`). DogPack (`.../3796123931`) liegt auch da, ist aber nicht gelesen.
* Einen fertigen **Bären-Begleiter** gibt es für PZ nicht (Suche: "project zomboid bear companion /
  pet bear"). Kevins Idee ist also neu.

---

## 1. Tabelle

| Mod (Build) | Workshop | Bekommen | Befehle | Bedürfnisse | Wachstum / Level | Tod | Ausrüstung | Sandbox (Auswahl) | Mehrspieler | Probleme |
|---|---|---|---|---|---|---|---|---|---|---|
| **Companion Dogs [ALPHA]** (B42.18+, lokal 0.7.4) | [3740052292](https://steamcommunity.com/sharedfiles/filedetails/?id=3740052292) | Streuner in schon erkundeten Gebieten, **füttern bis Vertrauen 100** (`TameThreshold`, sandbox-options.txt:3-8) | Herkommen, Folgen, Bleiben, Nächsten angreifen, Pfeifen (lockt Zombies), Bewachen, Jagen (IG_UI.json:29-34, :213, :317); Radialmenü, Pfoten-Menü, Rechtsklick | Hunger, Durst, Gesundheit, Stress, Loyalität (IG_UI.json:84-87, :196-199); **Eiweiß** nötig, sonst nach 72 h "schwach" (`ProteinHours`) | **5 Skills mit XP**: Spürnase, Kampf, Gehorsam, Jagen, Hüten (IG_UI.json:171-173, :309, :392). **Gene**: Stärke, Angriffslust, Widerstand – steigen nie (:179-203). Welpe → erwachsen nach `MaturityDays` (Vorgabe 90) | Begleiter ist im Normalfall **unverwundbar**: `setIsInvincible(true)` in jedem Update (server/CompanionDogs_Companion.lua:744). Leben sinkt nur durch Hunger, Durst, Gift (IG_UI.json:198). Option "Krankheit/Hunger kann töten" **Vorgabe aus** (`Death`, Sandbox.json) | Satteltaschen (Kapazität per Sandbox), Namensschild | 39 Optionen, u. a. `MaxCompanions`, `DogDamageMultiplier`, `NeedsRateMultiplier`, `LoyaltyDecayPerDay` 12, `SkillXPRate` 0.5, `DespawnOnOwnerOffline` an, `TripOverDogs`, Tierarzt (Wunde je Biss 0,4 %, Verstauchung je Zaunsprung 0,5 %, Würmer, Grippe …) | SP, Co-op, dedizierter Server. Server rechnet die Tier-KI, der Besitzer-Client bekommt die Positionshoheit geliehen (`client/` + `server/systems/CompanionDogs_NetAuthority.lua`; CLAUDE.md Abschnitt 5) | Ohne Eintrag im Hauptmenü fehlt beim Co-op-Host das Modell; bis 0.7 nur **ein** Folgender |
| **CD: Cats** (B42.19+) | [3791294616](https://steamcommunity.com/sharedfiles/filedetails/?id=3791294616) | Streuner in Häusern/Läden, füttern | wie Basis, **kämpft nicht** | wie Basis; Loyalität sinkt 1,5× schneller | wie Basis, kein Kampf-Skill | nur durch Hunger | Satteltasche fest 2 Plätze | eigener Spawn-Faktor | ja | nur ein Folgender |
| **Companion Dogs: DogPack** (B42.18+) | [3796123931](https://steamcommunity.com/sharedfiles/filedetails/?id=3796123931) | – (Zusatz) | Rudel bis 4 (Vorgabe 3), Anführer, Rollen (Beschützer, Angreifer, Späher, Träger), Formationen, HUD | mehr Hunde = mehr Futter | – | – | Platz im Auto je Hund, sonst Stress | Rudelgröße, Schaden je Extra-Hund (abnehmend) | Server prüft Befehle; jeder Hund hat einen **dauerhaften Datensatz** über Logout und Autofahrt | – |
| **CD-Rassen** (Rottweiler, Dobermann, Dog Goblin, Ratten, Herdenschutz) | über Suche "CD" | Fundort je Rasse (z. B. Dobermann 18 % je Polizeigebäude) | wie Basis | wie Basis | rassenabhängig | wie Basis | – | – | wie Basis | – |
| **Horse Mod [B42.20+/MP]** (lokal 1.1.2) | [3661336777](https://steamcommunity.com/sharedfiles/filedetails/?id=3661336777) | auf Farmen/Ranches finden, 7 Rassen | Reiten (Trab, Galopp, Sprung, Tritt gegen Zombies) | **Ausdauer 0–100**: Galopp −2/s, Trab +3, Gehen +5, Stehen +7,5 (shared/HorseMod/Stamina.lua:8-21) | **Gene** über Vanillas Gen-System: Tempo, Ausdauer, Tragkraft, Stärke (shared/HorseMod/definitions/HorseGenes.lua:2-25) | nicht beschrieben | Sattel (ohne Sattel: Schmerzen), Zügel, Satteltaschen | Gehtempo, Galopptempo, Ausdauer-Faktor, Schmerzlaute | ja, alle brauchen den "Meatball Fix" | Animationen nur bei Spielstart mit Mod; Treppe runterreiten tötet; Absteigen hängt manchmal |
| **Knox Wildlife [B42.21 Beta]** | [3818096743](https://steamcommunity.com/sharedfiles/filedetails/?id=3818096743) | wilde Tiere, **Schwarz- und Braunbär** je männlich/weiblich/**Jungtier** | – | – | – | jagbar, Fleisch/Fell/Knochen/Sehnen | – | nicht beschrieben | nicht beschrieben | Beta |
| **Animals Attack Zombies** (B42) | [3808643352](https://steamcommunity.com/sharedfiles/filedetails/?id=3808643352) | – (Nutztiere) | Bulle/Eber/Widder greifen an, Hahn stört, Mütter verteidigen Junge | Kampf macht Stress | – | **verletzte Tiere kämpfen nicht** | – | "per Sandbox einstellbar" (Liste nicht genannt) | nicht beschrieben | – |
| **Dogs** (Dislaik, B41) | [2908053151](https://steamcommunity.com/sharedfiles/filedetails/?id=2908053151) (zweite Id 2980870692, welche aktuell ist: ungeprüft) | Zufallsspawn in vier Städten, **bis 3 Hunde** | Befehle (nicht einzeln genannt) | Futter (Hundefutter, Fleischwurst), Wasser; Werte im **Gesundheitsfenster des Spielers** | – | verhungert; Zombies ignorieren die Hunde | – | – | – | Hunde öffnen Türen mit Menschen-Animation |
| **Pocket Kittens** (B41) | [2883925239](https://steamcommunity.com/sharedfiles/filedetails/?id=2883925239) | Kätzchen | – | Streicheln, Füttern | – | – | – | – | – | – |
| **Fauna** (Scimmia, B41) | [2873433741](https://steamcommunity.com/sharedfiles/filedetails/?id=2873433741) | per Sammeln in der Stadt | **keine** (unbewegliche Requisiten) | Streicheln senkt Stress, Unglück, Langeweile | – | schlachtbar | Polizeiweste am Schäferhund | – | – | B42-Fassung offen |

---

## 2. Die zehn besten Ideen für Kevins Bären

1. **Ein Jungtier finden und durch Füttern gewinnen** – *Herkunft: Companion Dogs (Vertrauen bis 100 durch Füttern), Knox Wildlife (Bär mit Jungtier-Variante).*
   Für uns: ein verwaistes Bärenjunges im Wald, Vertrauen wächst mit jeder Mahlzeit. **Ein Bär je Spieler**
   ist dort ein Sandbox-Wert (`MaxCompanions`) – bei uns fest 1 oder als Option. Stirbt er, gibt es ein neues Junges.

2. **Wachsen in Stufen, mit echter Größe** – *Herkunft: Companion Dogs.* Dort ist der Welpe eine eigene
   Tierart, die per `getData():setSizeForced(...)` klein gesetzt wird (server/CompanionDogs_Breeding.lua:194-197).
   Erwachsen wird er, indem ein neues erwachsenes Tier entsteht und der **Anteil** der Gesundheit mitwandert
   (server/systems/CompanionDogs_Stash.lua:123-145). Für den Bären: Baby → Jung → Halbstark → Ausgewachsen,
   "Tage bis ausgewachsen" als Sandbox. Ob `setSizeForced` auch die Trefferfläche mitwachsen lässt: **ungeprüft**.

3. **Baby kämpft nicht, flieht und meldet nur** – *Herkunft: CD: Cats (Späher ohne Kampf), Animals Attack Zombies (Jungtiere fliehen, Mütter verteidigen).*
   Ab einer Stufe darf er angreifen, Schaden und Leben steigen mit der Stufe.

4. **Skills mit XP statt nur ein Level** – *Herkunft: Companion Dogs (5 Skills, XP-Faktor in der Sandbox).*
   Für den Bären z. B. **Kampf** (mehr Schaden, weniger Panik), **Ausdauer**, **Gehorsam** (verweigert seltener
   Befehle, lernt Kunststücke), **Spürnase** (riecht Zombies weiter). Kunststücke werden mit Gehorsam-Stufen
   freigeschaltet (dort Stufe 1/3/5/10, IG_UI.json:394-408).

5. **Ausdauer als eigener Wert** – *Herkunft: Horse Mod.* Rennen und Kämpfen ziehen ab, Stehen füllt schneller
   auf als Gehen (Stamina.lua:8-21). Für Kevins Wunsch "mehr Ausdauer durch Level": das Level hebt das Maximum
   oder die Erholung.

6. **Jeder Bär ist anders (Gene)** – *Herkunft: Companion Dogs (Stärke, Angriffslust, Widerstand, steigen nie), Horse Mod (Vanillas Gen-System).*
   Das Junge würfelt bei der Geburt seine Anlagen, das Training baut darauf auf. Horse Mod zeigt, dass
   Vanillas `AnimalGenomeDefinitions.genes` dafür offen ist (HorseGenes.lua:2-25).

7. **Füttern und Trinken mit Folgen** – *Herkunft: Companion Dogs.* Hunger und Durst bremsen die Heilung
   und lassen die Loyalität schneller sinken (IG_UI.json:196-197); Eiweiß ist eine eigene Pflicht (72 h).
   Für den Bären als Allesfresser: Fleisch/Fisch für Eiweiß, dazu Beeren, Obst, Honig. Loyalität sinkt
   täglich, schneller bei Hunger.

8. **Tod oder Downed per Sandbox** – *Herkunft: Kevins Wunsch; Gegenbeispiel Companion Dogs.*
   Companion Dogs macht den Begleiter **immer unverwundbar** und lässt nur Hunger, Durst und Gift das Leben
   senken; Kampfwunden sind Würfel (0,4 % je Biss), die einen Verband brauchen. Kevins Plan ist schärfer:
   Option "Bär unsterblich" (**Vorgabe aus**): aus = er kann im Kampf sterben; an = bei wenig Leben liegt er
   am Boden wie die NPCs von NPC Crew und muss aufgerichtet werden. Die Verband-Idee (Wunde heilen) passt
   in beide Fälle.
   **Wichtig:** in Vanilla greifen Zombies Tiere gar nicht an (CLAUDE.md Abschnitt 5, 17.09., Bytecode-Beleg;
   PZwiki sagt dasselbe). Damit Zombies den Bären verletzen, brauchen wir eigenen Code. Ob Bandits Tiere
   angreift: **ungeprüft**.
   Hinweis aus deren Code: Feuer geht an `setIsInvincible` vorbei (server/systems/CompanionDogs_Fire.lua:46-47,
   **im Jar ungeprüft**).

9. **Rückzug statt Selbstmord im Kampf** – *Herkunft: Animals Attack Zombies, Companion Dogs (Stress).*
   Er schätzt die Lage ein, zieht sich vor großen Horden zurück, verletzt kämpft er nicht. Kampf macht
   Stress, bei Panik folgt er nur noch (IG_UI.json:199).

10. **Befehle, Taschen und Beziehung** – *Herkunft: Companion Dogs, DogPack, Horse Mod, Fauna.*
    Folgen, Bleiben, Bewachen, Angreifen, Herpfeifen (Pfiff lockt Zombies). Großer Bär trägt Satteltaschen,
    die Tragkraft wächst mit der Größe. Neben ihm schlafen gibt einen "Ausgeruht"-Bonus (IG_UI.json:256-257),
    Streicheln senkt Langeweile und Stress (Fauna). Freilassen behält seine Skills (IG_UI.json:215).

**Dazu für den Mehrspieler (kein Extra, eine Pflicht):** loggt der Besitzer aus, geht der Bär mit
(Companion Dogs `DespawnOnOwnerOffline`, Vorgabe an; DogPack hält einen dauerhaften Datensatz je Hund).
Das ist dieselbe Entscheidung wie Kevins Logout-Parken in NPC Crew. Bei Tieren rechnet im MP der Server
die KI – also gehört der Bär auf den Server, nicht wie die Zombie-Companions auf den Client.

---

## Quellen (Web)

* [Companion Dogs (top-mods)](https://top-mods.com/mods/project-zomboid/gameplay/16273-companion-dogs-alpha.html)
* [CD: Cats](https://top-mods.com/mods/project-zomboid/gameplay/17465-cd-cats.html)
* [Companion Dogs: DogPack](https://top-mods.com/mods/project-zomboid/gameplay/16632-companion-dogs-dogpack.html)
* [Horse Mod](https://top-mods.com/mods/project-zomboid/gameplay/16688-horse-mod-b42-20-mp.html)
* [Knox Wildlife](https://top-mods.com/mods/project-zomboid/gameplay/16613-knox-wildlife-b42-21-beta.html)
* [Animals Attack Zombies](https://top-mods.com/mods/project-zomboid/gameplay/16363-animals-attack-zombies.html)
* [Dogs (Dislaik), Katalog](https://catalogue.smods.ru/archives/147965)
* [Pocket Kittens, Changelog](https://steamcommunity.com/sharedfiles/filedetails/changelog/2883925239)
* [Fauna (top-mods)](https://top-mods.com/mods/project-zomboid/gameplay/11505-fauna.html)
* PZwiki "Animal" (nur als Suchtreffer, Abruf 403): Zombies greifen Tiere nicht an.
