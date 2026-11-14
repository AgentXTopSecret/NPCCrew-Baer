# Lauf baer-plaene-1114, Thema TALENTE: PLAN fuer den Bau-Lauf "baer-talente" (Reiter "Talente", 3 Talentpunkte, 9 Talente, Icons)

Stand 14.11.2026 (Rolle PLAN). **Statisch geprueft, nicht gespielt.** Kein Mod-Code gebaut. Geschrieben nur diese Datei, das Entwurfsbild
`plaene_1114/bilder/ENTWURF_talente_DE_1080.png` und sein Werkzeug `plaene_1114/werkzeug_talente/zeichne_talente_entwurf.py`.

Grundlage (geht vor): `baer/begleiter/ENTSCHEIDUNGEN.md` ab :686 bis :853 (`E:Zeile`), `baer/begleiter/bedarf_echte_baeren.md`, `baer/STAND.md` oben.
Kuerzel: `T:` = Test-Mod `Zomboid/mods/NCBearTest/42/media/lua/` (Git main 1f7b641 = F1..F4 + Liegen + K1 + Kampf), `TM:` = `NCBearTest/42/media/`,
`V:` = Vanilla `ProjectZomboid/media/lua/`, `B` = `BanditsNPC.Bear`, `U` = `B.UI`. Form wie `k1/PLAN_K1.md`.
Ausgenommen (eigene Plaene dieses Laufs): Troege/Futterliste (PLAN_TROEGE.md), Spuernase-ESP und Fischen (PLAN_F5.md) -- hier nur die Naht "Angler".

---

## 0. Kurzfassung

1. **Was Kevin will** (woertlich): *"skill tab pro baerenstuge ... = 1 skill punkt ... im skilltree auf einen extra tab kann man die skillpunkte
   aisgeben und per knopf altivieten dann leuchtet der skill hell und ist permanent altiv"* (E:813); *"das aktivieren 2 skills sperrt es einen neuen
   skill zu lernen selbst wenn man durch bugs mehr haette"* (E:814); *"skill reset ist erlaubt pro sandbox setting, nur 1x taeglich auch per sandbox
   einstellbar"* -- *"standardmaessig aber nicht erlaubt"* -- *"skills vergeben muss bestaetigt werden beim klicken"* (E:815); Icons *"recht gut
   sichtbar ... wie in anderen spielen"* (E:837), *"hochaufloesend und huebsch"* (E:840); *"ab 10% wachstum schon ein skill punkt"* + Krit (E:848);
   **BERICHTIGT** *"genau also am ende genau 3 punkte zum verteilen"* (E:852): Punkt 1 bei 10 % Wachstum, 2 bei halbstark, 3 bei ausgewachsen.
2. **Eine Wahrheit:** die verdienten Punkte werden NIE gespeichert, sondern aus dem Wachstum `rec.g` gerechnet (hoechstens 3, weil es nur 3 Schwellen
   gibt). Gespeichert wird nur, WAS gelernt ist: `rec.tal` = Text "alert,paw" (hoechstens 3, je Reihe einer) im Register und im Spiegel. Darum kann
   kein Aussehen-Wechsel, Unstuck, Koerper-Tausch, Absturz oder eine falsche MP-Bitte je einen 4. Punkt erzeugen; ab 3 gelernten ist immer Schluss.
3. **Empfehlung Baum-Form A "3 Reihen nach Alter"** (Frage 1): Reihe 1 (ab Tag 10) Genuegsam / Wachsam / Zaeh -- Reihe 2 (ab halbstark) Schwere Pranke /
   Ausdauernd / Lasttier -- Reihe 3 (ausgewachsen) Dickes Fell / Kritischer Treffer / Angler; je Reihe genau 1 lernbar. Alternative B "freie Wahl".
4. **Jede Wirkung an GENAU einer Stelle des heutigen Codes** (Abschnitt 3, je mit Zeile), Werte als `B.CFG`-Block "Talente", ein reiner Regel-Helfer
   `B.TalentK(rec, key, def)` -- kein Talent liest Engine-Werte selbst.
5. **Neue Dateien:** `shared/BanditsNPCBearTalentRules.lua` (rein), `server/BanditsNPCBearTalent.lua` (Bitten, Register, Sicht, Meldung),
   `client/BanditsNPCBearTalentData.lua` (Modell), `client/ISUI/BanditsNPCBearTalentTab.lua` (Kacheln), Bench `client/NCBearBenchTalent.lua`,
   20 Bilder `TM:ui/BanditsNPCBearTalent_*.png`. Texte `UI_BN_Bear_Talent_*` in ACHT Sprachen. **Genau 2 neue Sandbox-Regler** (Kevins Ausnahme):
   `BearTalentReset` (aus) und `BearTalentResetDays` (1, 0..30) in der Gruppe "Wachsen und Faehigkeiten" -> 16 Optionen.
6. **Bestaetigung** = Vanillas Ja/Nein-Fenster `ISModalDialog` (V:client/ISUI/ISWorldObjectContextMenu.lua:953, gleiche Argumenttypen). **Kein neuer
   Jar-only-Aufruf**, nichts braucht Kevins Wort fuer eine Ausnahme.
7. **SP/MP:** nur der Schreiber entscheidet (Bitte "Talent" { id, k } / "TalentReset" { id }); Krit-Wurf und Umwerfen beim Schreiber, der Client zeigt.
   Kein Gegenstand wird beruehrt (Lasttier-Reset bei voller Last: nichts faellt heraus, er ist nur "zu schwer").
8. **Bau: 8 Agenten**, KEIN Modell-Lauf noetig (Icons sind 2D, Abschnitt 6). Bau erst nach Kevins K1-/Kampf-Test (gleiche Dateien).

---

## 1. Kevins Worte -> feste Regeln (R1-R10)

| Nr | Regel | Quelle |
|---|---|---|
| R1 | Genau 3 Talentpunkte: 1. bei 10 % Wachstum, 2. beim Sprung zu halbstark/kampfbereit, 3. bei ausgewachsen (Tag 100) | E:852-853 |
| R2 | Nie mehr als 3 -- auch nicht durch Aussehen-Wechsel, Unstuck, Koerper-Tausch, Absturz (Auftrag: auch nicht durch MP-Bitten mit falschen Daten) | E:813, E:853 |
| R3 | Nach 3 aktiven Talenten gesperrt, selbst wenn ein Fehler mehr Punkte gaebe | E:814, E:853 |
| R4 | Eigener Reiter "Talente" mit Skill-Baum; Punkt ausgeben per Knopf MIT Bestaetigung; aktives Talent leuchtet hell, bleibt fuer immer | E:813, E:815, E:827-828 |
| R5 | Reset nur, wenn die Sandbox es erlaubt (Vorgabe AUS), hoechstens 1x je Tag (auch per Sandbox einstellbar) | E:815, E:829 |
| R6 | 9 Talente: Genuegsam, Dickes Fell, Ausdauernd, Schwere Pranke, Lasttier, Wachsam, Angler, Zaeh, Kritischer Treffer | E:834-836, E:851 |
| R7 | Krit: 25 % je Treffer doppelter Schaden; Zahl ueber dem Zombie gross in Gold (mit "Schaden zeigen") | E:848, E:851 |
| R8 | Name: DE "Talente"/"Talentpunkt", EN "Perks"/"Perk point" | E:849 |
| R9 | Icons eigene Zeichnung, gross und klar, je Talent ein Motiv; aktiv hell leuchtend, nicht vergeben gedimmt, gesperrt mit Schloss; 128-px-Quelle, Vorbild Herz "Goldrand" | E:837-841 |
| R10 | Vor dem Bau ein ENTWURF-Bild mit echten Spielschriften (erledigt, Abschnitt 5) | E:839, ~/.claude/CLAUDE.md |

Namen im Code: "Talent" (nicht "Perk": Vanillas Faehigkeiten heissen `Perks.*` -- Verwechslungsgefahr beim Greppen). Kollisionsprobe 14.11.: `Talent` kommt in
NPC Crew `42/media/lua` und in der Test-Mod nicht vor (grep, 0 Treffer). Die vorhandenen 6 "Faehigkeiten" (Erfahrung, Stufe 0-10, T:shared/BanditsNPCBearStats.lua:110-111)
bleiben unberuehrt -- Talente sind etwas Eigenes.

---

## 2. Punkte, Reihen, Speicher (KERN, `shared/BanditsNPCBearTalentRules.lua` NEU, rein)

### 2.1 Verdiente Punkte (nie gespeichert)
`B.TalentEarned(e)` (Register- ODER Sicht-Eintrag) = Summe aus drei Schwellen, je 0/1:
- g >= `talG1` 0,10 (Kevin "10 % Wachstum"; `rec.g` 0..1, T:server/BanditsNPCBearGrow.lua:6; bei 100 Tagen = Tag 10, bei jeder anderen `BearGrowDays` = 10 % des Wegs),
- innere Groesse s = `B.GrowSize(g)` >= `stageAt[1]` 0,75 = halbstark (T:shared/BanditsNPCBearStats.lua:195-208; g 0,15 = Tag 15),
- s >= `stageAt[3]` 1,35 = ausgewachsen (g 1,0 = Tag 100).
Hoechstens 3 per Bauart. g sinkt im Spiel nie (nur Werkbank `B.GrowSetG` und der MP-Deckel beim Wiederherstellen, T:server/BanditsNPCBearGrow.lua:909-919).

### 2.2 Gelernt (gespeichert)
`rec.tal` = Text, Schluessel durch Komma, in Lern-Reihenfolge (z. B. "alert,paw"). Nur flache Werte, also spiegel-tauglich (T:server/BanditsNPCBearHeal.lua:97-100
`plain`). Dazu `rec.talR` (Spieltag des letzten Resets, `math.floor(B.Now()/24)` wie T:server/BanditsNPCBearNeeds.lua:113-115) und `rec.talN` (zuletzt
gemeldete Punktzahl, gegen doppelte Meldungen nach dem Laden).
`B.TalentFix(rec)` (rein, beim Laden und vor jedem Schreiben): nur bekannte Schluessel, keine Doppelten, im Reihen-Modus hoechstens einer je Reihe, hoechstens
`talMax` 3 (die ersten bleiben, der Rest faellt mit EINER Fehlerzeile weg -- R3). Kein Text -> nil.

### 2.3 Darf er lernen? `B.TalentCan(rec, k)` -> ok, why
Reihenfolge der Gruende: `unknown` (kein Talent) -> `max` (schon `talMax` gelernt -- **zuerst**, R3: auch bei "zu vielen" Punkten) -> `have` (schon gelernt) ->
`soon` (Angler vor F5, `B.CFG.talFishOn == false`) -> `row` (Reihe noch nicht erreicht: `TalentEarned < row`) -> `rowUsed` (in dieser Reihe schon eins; nur
Reihen-Modus) -> `point` (kein freier Punkt: `#gelernt >= TalentEarned`) -> ok.

### 2.4 Tabelle `B.TALENTS` (Reihenfolge = Fenster)
| Schluessel | Name DE / EN | Reihe | Bild |
|---|---|---|---|
| frugal | Genuegsam / Frugal | 1 | Schale + Tropfen |
| alert | Wachsam / Alert | 1 | Auge |
| tough | Zaeh / Tough | 1 | Kreuz (Heilen) |
| paw | Schwere Pranke / Heavy Paw | 2 | Pfote |
| stamina | Ausdauernd / Enduring | 2 | Blitz |
| mule | Lasttier / Pack Animal | 2 | Rucksack |
| fur | Dickes Fell / Thick Fur | 3 | Schild |
| crit | Kritischer Treffer / Critical Hit | 3 | drei Krallenhiebe |
| fisher | Angler / Angler | 3 | Fisch |

Warum diese Reihen (Frage 2): das Junge (Reihe 1, Tag 10) kaempft nie (T:server/BanditsNPCBearGuard.lua Kommentar K6, `B.FightDecide` "cub" T:shared/BanditsNPCBearFightRules.lua:470)
-> dort nur Ueberleben; Kampf, Packtaschen (ab halbstark, T:shared/BanditsNPCBearInvRules.lua:876-883) und Fischen (Fang-Chance erst ab halbstark,
T:shared/BanditsNPCBearStats.lua:388-394) beginnen mit halbstark; +250 Leben gibt es nur am Erwachsenen (am Jungen mit ~110 Leben an Tag 10 waere es das
Dreifache, T:shared/BanditsNPCBearStats.lua:380 mit hpAt {40,150,400}). Modell B (freie Wahl) = `B.CFG.talRows = false`, sonst gleich.

### 2.5 B.CFG-Block "Talente" (KERN, an das Ende von B.CFG, T:shared/BanditsNPCBear.lua:96-385)
```
talG1 = 0.10, talMax = 3, talRows = true,            -- Schwelle Punkt 1 (Wachstum) / hoechstens / Reihen-Modell (false = freie Wahl)
talFrugalK = 0.6667,                                 -- Genuegsam: Hunger/Durst-Anstieg x 16/24
talFurHp = 250,                                      -- Dickes Fell: + Lebenspunkte (nach dem Zaehigkeits-Bonus, nicht mit ihm multipliziert)
talStaPct = 0.30, talStaRegK = 1.5,                  -- Ausdauernd: Ausdauer max +30 % / Erholung x 1,5
talPawKnock = 100, talPawPush = 2.0,                 -- Schwere Pranke: Umwerf-Chance Hieb/Doppelschlag / Rueckstoss-Faktor
talMuleKg = 50,                                      -- Lasttier: + kg, NICHT mit BearCarryPercent multipliziert (wie bagAdd)
talAlertK = 1.5,                                     -- Wachsam: Weiten x 1,5 (Kampf-Suche, Wecken, Verstecken)
talHealK = 2.0, talDownK = 0.5,                      -- Zaeh: Selbstheilung x 2 / Zeit am Boden x 0,5 (12 -> 6 h)
talCritPct = 25, talCritK = 2.0,                     -- Krit: Chance je Treffer / Faktor
talFishK = 2, talFishOn = false,                     -- Angler: Fische je Fang / F5 schaltet true
talGlowMs = 2000,                                    -- Leuchten: eine Welle je 2 s (OBERFLAECHE)
```

---

## 3. Die 9 Talente: genaue Wirkung am heutigen Code + Wechselwirkung K1 / Kampf

Helfer (rein, TalentRules): `B.TalentOn(e, k)` (gelernt?), `B.TalentK(e, k, def)` (Wert aus B.CFG, wenn gelernt, sonst def). Jede Naht ist EINE Zeile mit
`B.TalentK` und einem Existenz-Riegel (`if B.TalentK then ... end`), damit die Datei ohne TalentRules wie heute rechnet.

| Talent | Heute (Stelle) | Neu (Formel) | Wechselwirkung K1 / Kampf |
|---|---|---|---|
| **Genuegsam** | Hunger UND Durst `rise = needRiseH x k x dt` (T:server/BanditsNPCBearNeeds.lua:546-549), k = Sandbox x Vertrauen (`B.TrustK`, T:shared/BanditsNPCBearNeedRules.lua:200-205) | `rise x talFrugalK` (6,25 -> 4,17 je Wachstunde = 0 -> 100 % in 24 statt 16 h). Muedigkeit (:550) bleibt | Vertrauen +100 und Genuegsam multiplizieren: 6,25 x 0,75 x 0,667 = 3,1/h (32 h). -5 bei 90 % (:562-570) kommt nach 21,6 statt 14,4 Wachstunden. Die volle Leiste bleibt eine Tagesmenge (`B.HunDayPts`/`B.WaterDayL`, NeedRules.lua:136-147) -> er braucht je Tag 2/3 Futter/Wasser; Selbst-Fressen ab 50 % (Needs.lua:613-616) seltener. Hunger-/Durst-Tooltip sagt heute fest "16 Stunden" (T:shared/Translate/DE/UI.json:433, :553) -> Zusatzzeile, Schluessel bleiben |
| **Dickes Fell** | `hpMax = lerp(hpAt) x (1 + vitPerLv x Stufe)` (T:shared/BanditsNPCBearStats.lua:380) | `+ talFurHp` (250) danach | Leben ist ein Anteil (`rec.hp` 0..1, Grow.lua:229-240) -> der Balken bleibt gleich voll: 200/400 -> 325/650 (Frage 7). Hunger/Durst-Verlust ist % je Stunde (Needs.lua:574-588) -> gleiche Zeit bis 1 %. Flucht-Schwelle in Punkten (`B.FleeHp`, FightRules.lua:388-400) -> flieht relativ spaeter. Zombie-Treffer 6 Punkte (FightRules.lua:355-359) -> ~42 Treffer mehr. Reset: Anteil bleibt, nie 0 (`B.BodyHp` klemmt 0,01, Grow.lua:275) |
| **Ausdauernd** | `staMax = lerp(staAt) x (1 + conPerLv x Stufe)` (Stats.lua:381); Erholung `staRegen x dts x (1 + conPerLv x Stufe) x needK / staMax` (Grow.lua:543) | staMax x (1 + talStaPct); Erholung x talStaRegK | Kampf: mehr Angriffe bis zur Pause (staAttackCost 3, Rast unter 5 %, weiter ab 30 %; B.lua:228, FightRules.lua:485-487). Muedigkeit aus Anstrengung = verbrauchte Punkte / staMax x tirPerBar (Needs.lua:551-556) -> je Kachel Rennen ~23 % weniger Muedigkeit (Nebenwirkung, gewollt). Hunger/Durst >= 50 oder Muedigkeit >= 70 halbieren die Erholung weiter (NeedRules.lua:238-252). Spaeterer Bett-Buff "+20 % Ausdauer" (E:830-831) multipliziert |
| **Schwere Pranke** | Umwerf-Chance `allow.knockPct`: halbstark 0, kraeftig 30 -> 100, ausgewachsen 100 (FightRules.lua:137-156), gewuerfelt je Ziel (Fight.lua:865-874); Rueckstoss `knockPush` 0,7 Kacheln (Foe.lua:224-233, :273) | Hieb (swipeL/R) und Doppelschlag (slam): kpct = talPawKnock (100) ab halbstark; Fx "hit" traegt `kp = talPawPush` -> `addPush` mit 0,7 x 2 = 1,4 Kacheln, `pushMs` x kp (sonst schneidet die Frist bei 30 FPS den Weg ab) | Am Ausgewachsenen wirft er heute schon jeden um -> dort bleibt nur der doppelte Rueckstoss (Frage 3). Biss bleibt "down" mit Stufen-Chance. Kampf K2: liegt das Ziel, waehlt er Zerfleischen (FightRules.lua:228-230) -> mehr Zerfleischen ab kraeftig. Rueckstoss nur, wenn hinten frei, sonst faellt er auf der Stelle (Foe.lua:257-266) |
| **Lasttier** | Kapazitaet `carry x BearCarryPercent/100 (+ bagAdd 150 mit Taschen ab halbstark)` (T:shared/BanditsNPCBearInvRules.lua:880-885; Aufrufer T:server/BanditsNPCBearInv.lua:139-143, :742) | `B.InvCapOf(carry, pct, bagOn, half, extra)` + extra = `B.TalentK(rec, "mule", 0)` (50); beide Aufrufer reichen es durch | Nur der Schreiber rechnet (Sicht ivC, Inv.lua:999-1014). Taschen ablegen prueft `capNo` MIT +50 (:742). Reset bei voller Last: nichts faellt heraus, Sicht ivX "zu schwer" (:1014), er nimmt nur nichts mehr an |
| **Wachsam** | Kampf-Suche `fightRadius 10 / fightBanditRadius 12` fuer alle Baeren gleich (T:server/BanditsNPCBearFightFoes.lua:260, `take` :135-157); Wecken `sleepWakeR 8` (Sleep.lua:332-336); Verstecken des Jungen `zedHide 6 / zedSafe 9` (T:shared/BanditsNPCBearRules.lua:711-719, Aufrufer Guard.lua:350); schlaftrunken `wokeFleeMs 5000` (Sleep.lua:267-268, -> `B.FightDecide` "woke" FightRules.lua:476) | Weiten je Baer x talAlertK: Kampf 15 / 18 (Punkt-Felder p.rz / p.rb in `B.FoeScan`, Rahmen mit dem Groessten), Wecken 12, Verstecken 9 / 12 (c.hideR / c.safeR an `B.GuardDecide`); `s.wokeUntil = nil` statt +5 s (der Aufsteh-Halt bleibt) | Alle Weiten bleiben unter der Suche: `zedSense 12` liefert B._zed bis 12 (Guard.lua:270) -> Wecken 12 / Sicher 12 passen ohne neue Suche. Kampf 15 liegt unter der Leine 25 (B.lua:218). Kampf K7 (Sicht fuer sightMax 12 Kandidaten) unveraendert. Locken K5 (Zombies sehen IHN, lureR 10) bleibt -- Wachsam ist SEIN Blick. Spuernase (F5) bleibt getrennt |
| **Zaeh** | Selbstheilung `B.HealRate(asleep) x needK.heal` (Grow.lua:800; HealRate Stats.lua:407-412: wach 1 %/h, Schlaf 15 %/h x BearHealPercent); allein aufstehen nach `downedHours` 12 (Hurt.lua:190) und Sicht-Rest (Hurt.lua:257) | Selbstheilung x talHealK (2 / 30 %/h); EINE Funktion `B.DownHours(rec)` = downedHours x talDownK (6 h), gerufen an beiden Stellen | Verband bleibt gleich (Mend.lua). Ab 80 % Hunger/Durst heilt er weiter gar nicht (needK.heal 0). K1: jedes Mal am Boden -10 Vertrauen bleibt (Hurt.lua:157) -- er liegt nur kuerzer. Aufhelfen 45 % unveraendert |
| **Kritischer Treffer** | Schaden je Ziel `md[...]` (Fight.lua:869-872), aus `B.MeleeDamage` inkl. Schwaeche-Faktor (FightRules.lua:409-436); Zahl `U.DmgFloat` (T:client/BanditsNPCBearFx.lua:142-156, Schrift :93-98) | je Ziel `ZombRand(100) < talCritPct` (V:shared/TimedActions/Animals/ISMilkAnimal.lua:25) -> dmg x talCritK; Fx "hit" + `crit = true`; Client: Schrift `UIFont.Large` (statt Medium), Gold {1.00, 0.84, 0.25}, zweimal 1 px versetzt (fett wie der Name, Window.lua:721-722), "!" dahinter, 1,3 x Steighoehe | Krit verdoppelt den SCHON geschwaechten Schaden (Hunger/Durst x 0,85 / 0,7). Kills und Erfahrung unveraendert (ein Treffer bleibt ein Treffer). Nur mit "Schaden zeigen" (Fx.lua:205) sichtbar. Grenze: groesser als `UIFont.Large` gibt es ohne Beleg nicht (`UIFont.Massive` kommt in Vanilla-Lua nicht vor, grep 14.11.) -- "gross" = Large + fett + Gold. Fenster: Tooltip "Nahkampfschaden" + Zeile "Krit: 25 % doppelt" |
| **Angler** | Fischen gibt es noch nicht (Knopf grau, T:client/ISUI/BanditsNPCBearWindow.lua:704; Fang-Chance nur Anzeige, Stats.lua:388-394) | F5 ruft beim Fang `n = B.TalentK(rec, "fisher", 1)` (2 Fische je Fang, Chance unveraendert) und setzt `talFishOn = true` | Bis F5: Kachel "Kommt spaeter" (gesperrt, Grund im Tooltip), lernen abgelehnt (`soon`, Frage 4). Naht in PLAN_F5.md |

---

## 4. Register, Bitten, Sicht, Meldung (KERN, `server/BanditsNPCBearTalent.lua` NEU)

### 4.1 Bitten (nur der Schreiber; Form wie `B.HandleLook`, T:server/BanditsNPCBearLook.lua:115-158)
- `B.Handle` (T:server/BanditsNPCBearServer.lua:424-489) bekommt zwei Zweige: `"Talent"` -> `B.HandleTalent`, `"TalentReset"` -> `B.HandleTalentReset`.
- **HandleTalent(player, args)**: liest NUR `args.id` (Text) und `args.k` (Text, muss in `B.TALENTS` stehen -- sonst still verworfen). Drossel `B.AskOk(pkey.."|Talent", ms)`
  (T:server/BanditsNPCBearFollow.lua:56-75). Eintrag fehlt -> Why_Gone; nicht Besitzer oder nicht tame/missing -> Why_NotOwner. Dann `B.TalentFix`,
  `B.TalentCan` -> Grund als Meldung (`UI_BN_Bear_Why_Talent<Grund>`). Ok -> `rec.tal = alt .. "," .. k`, `B.Commit(rec)` (Spiegel + Sicht),
  Meldung `UI_BN_Bear_Note_TalentLearned`, Log-Zeile, `B.FlushViews()`; bei "fur": `B.BodyHp(rec, B.FindAnimal(rec), 0)` (Anteil bleibt, Koerper gleich).
  Kein Wert aus der Bitte wird geglaubt (keine Punktzahl, keine Reihe, kein Zustand). Zwei schnelle Klicks: Drossel + zweite Pruefung `have`/`rowUsed`/`point`.
- **HandleTalentReset(player, args)**: `args.id`; Besitzer; `B.Opt("BearTalentReset") ~= true` -> Why_TalentResetOff; nichts gelernt -> Why_TalentNone (keine Uhr);
  `tag - rec.talR < BearTalentResetDays` -> Why_TalentResetWait mit Stunden bis zum naechsten Spieltag; sonst `rec.tal = nil`, `rec.talR = tag`, Commit,
  Meldung `UI_BN_Bear_Note_TalentReset`. Beruehrt nichts anderes (Leben-Anteil, Ausdauer-Anteil, Inventar bleiben).
- Rolle "user" genuegt (wie alle Bitten: `sendClientCommand` ueber `B.Ask`, T:shared/BanditsNPCBear.lua:884-893) -> kein Kick, kein Admin-Aufruf.

### 4.2 Langsam-Takt `B.TalentSlow(rec, now, players)`
Eigene Schleife in `slowTickBody` NACH `B.NeedsSlow` (T:server/BanditsNPCBearServer.lua:686-691), nur tame, Besitzer online. `n = B.TalentEarned(rec)`;
`n > (rec.talN or 0)` -> Meldung `UI_BN_Bear_Note_TalentPoint` ("Talentpunkt! Baerenfenster, Reiter Talente"), `rec.talN = n`, Commit. `n < talN`
(Werkbank senkte g) -> nur `rec.talN = n`, keine Meldung. So kommt jede Meldung genau einmal, auch nach Laden/Absturz.

### 4.3 Spiegel und Absturz (T:server/BanditsNPCBearHeal.lua)
- `MARK_FIELDS` (:52-60) + `"tal", "talR", "talN"`.
- `B.Restore` (:260, nach `B.GrowFromMark(rec, mark, "restore")` :344): `B.TalentFromMark(rec, mark)` -> Text uebernehmen, `B.TalentFix`, dann auf
  `B.TalentEarned(rec)` kuerzen (im MP ist g dort schon gedeckelt, Grow.lua:909-919 -> ein veraenderter Spiegel bringt hoechstens so viele Talente,
  wie das ehrliche Wachstum erlaubt; R2).
- `B.TakeNewerMark` (:396, nach "newer" :473, nur SP): der neuere Spiegel ist die Wahrheit -> `tal`/`talR`/`talN` aus ihm, `TalentFix`, kuerzen.
- `B.GrowFix` (Grow.lua:134-226) ruft am Ende `B.TalentFix` (Existenz-Riegel); an nicht gezaehmten Eintraegen `tal/talR/talN = nil` (wie FIELDS :58, :136-138).
- Koerper-Tausch / Unstuck / Aussehen (`B.PlaceCub`, `B.BodySwap` Grow.lua:672-715) beruehren `rec` nicht -> Talente bleiben, Punkte bleiben.

### 4.4 Sicht (`viewEntry`, T:server/BanditsNPCBearRegistry.lua:638-695) -> `B.TalentView(rec, t, pkey, now)`, nur Besitzer
`tal` (Text), `talE` (verdient 0..3), `talRo` (Reset erlaubt laut Server-Sandbox), `talRw` (Stunden bis Reset wieder geht, nur > 0), `talNx` (Tage bis zur
naechsten Reihe, aus `B.GrowXAt`, Stats.lua:176-193, wie `nextDays` Stats.lua:365-373). Der Client rechnet Zustaende mit DENSELBEN reinen Regeln (`B.TalentCan`
auf dem Sicht-Eintrag) -- graue Kacheln und Server-Ablehnung laufen nie auseinander.

---

## 5. Reiter "Talente" im Baerenfenster (OBERFLAECHE)

Entwurfsbild: `plaene_1114/bilder/ENTWURF_talente_DE_1080.png` (A links = Empfehlung, B rechts = freie Wahl; echte Spielschriften 1x, Farben aus
T:client/ISUI/BanditsNPCBearWinParts.lua:52-87, Masse aus K1 DE 1080p gemessen 802 x 615). Zustand im Bild: Tag 100, 3 Punkte, 2 gelernt (Wachsam, Schwere
Pranke), 1 frei -> in A sind in Reihe 3 zwei Kacheln waehlbar (Angler "kommt spaeter"), die 4 nicht gewaehlten der Reihen 1-2 gesperrt; Maus ueber Dickes Fell
mit Tooltip; in B die Bestaetigung nach Klick auf Kritischer Treffer. Unten die 9 Platzhalter-Symbole und die drei Zustaende.

### 5.1 Reiterleiste (T:client/ISUI/BanditsNPCBearWindow.lua)
- `metrics` (:143-244): neue Zeile `m.tabY = headH + R(8)`, `m.tabH = lb + R(10)`, Karten ab `m.y1 = tabY + tabH + R(8)` (statt headH + 16). Fenster wird
  29 x f hoeher (1080p DE 615 -> 644; 4K 1288, unter FIT 0,92 x 2054). Beide Reiter gleich hoch -> nichts springt beim Wechsel.
- Zwei Reiter "Uebersicht" | "Talente" als `U.WinBtn` mit style "tab" (WinParts: aktiv = cardBg + 2 px accent oben, verbunden mit der Karte; inaktiv = btnBg).
  Abzeichen: freie Punkte als Honig-Kaestchen mit Zahl (nur > 0). Klick setzt `win.tab` (nur Sitzung) und legt neu.
- Wechsel: `hideTip` (:444-450) an allen Kindern, dann `setVisible` (V:client/ISUI/ISButton.lua:9) -- Uebersicht: rows/btn/tick/care/look; Talente: 9 Kacheln
  + Reset-Knopf. `prerender` (:759-778) zeichnet je Reiter nur seine Karten.

### 5.2 Kacheln (`client/ISUI/BanditsNPCBearTalentTab.lua` NEU)
- Klasse `U.WinTalent = ISButton:derive(...)` wie `U.WinRow` (WinParts.lua:245-347; Klick nur bei enable, Tooltip auch grau, V:client/ISUI/ISButton.lua:18-23, :45, :316-346).
- Lage (f = 1): Karte "Talente" volle Breite, Kopfzeile Titel + rechts "1 Talentpunkt frei -- 2 von 3 vergeben"; 3 Reihen je (Hoehe - Kopf - Fuss) / 3; links
  128 x f Stufen-Pfad (Knoten + Linie gold, wenn erreicht; "Reihe n / ab Tag 10 / erreicht" bzw. "in 5 Tag(en)"), daneben 3 Kacheln. Kachel: Bild 56 x f
  oben mittig, Name (Text-Schrift), kurze Wirkung (Klein), Zustand oben links.
- Zustaende: **aktiv** = warmer Grund, 2 px accent-Rahmen, Leuchten hinter dem Bild (glow-Bild, Alpha 0,55-0,85 per `math.sin` je talGlowMs; Beleg
  V:client/ISUI/ISEquippedItem.lua:391), Name gold; **waehlbar** = btnBg, Honigrahmen, Bild mit Farbe 0,85, Maus darueber accent; **gesperrt** = btnOff,
  graues Bild (_off), Schloss unten rechts; **kommt spaeter** = wie gesperrt, Text "Kommt spaeter".
- Bilder: `getTexture("media/ui/BanditsNPCBearTalent_<k>.png")` (V:client/Chat/ISChat.lua:137), einmal je Spielstart wie `textures()` (:833-838);
  `drawTextureScaled(tex, x, y, w, h, a, r, g, b)` (V:client/ISUI/ISUIElement.lua:1032, Aufrufer V:client/Chat/ISChat.lua:418).
- Fusszeile der Karte: Hinweis links; rechts Knopf "Zuruecksetzen" (grau mit Grund, wenn Sandbox aus oder Wartezeit; daneben "aus (Sandbox)" / "in 14 h").
- Je Bild nur fertige Felder (Modell 1 x je s, `U.TalentModel` in `client/BanditsNPCBearTalentData.lua` NEU); nur die Glow-Alpha wird je Bild gerechnet.

### 5.3 Bestaetigung (Kevin E:815)
Klick auf waehlbare Kachel -> `ISModalDialog:new(0, 0, 350, 150, text, true, win, Win.onTalentYes, 0, k, id)` -> `modal:initialise()` -> `modal:addToUIManager()`
(Form V:client/ISUI/ISWorldObjectContextMenu.lua:953 mit player + zwei Werten; initialise/addToUIManager V:client/ISUI/Animal/ISAnimalContextMenu.lua:1084-1086).
Rueckruf `onclick(target, button, param1, param2)` (V:client/ISUI/ISModalDialog.lua:58-63), Ja = `button.internal == "YES"` (V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:219)
-> gehoert der Baer laut Sicht noch mir: `B.Ask(player, "Talent", { id = id, k = k })`. Text mehrzeilig mit "\\n" wie Vanilla
(V:shared/Translate/EN/UI.json:34 + V:client/OptionScreens/CoopOptionsScreen.lua:383-384; `ISModalDialog:new` macht daraus Zeilenumbrueche, :188).
Reset genauso (Text nennt den Namen und die Wartezeit). Nebenwirkung Vanilla: `destroy()` setzt im Spiel das Tempo auf 1 (ISModalDialog.lua:47-49) -- wie beim
Schlafen-Fragen; harmlos.

### 5.4 Andere Fenster-Stellen
Tooltips (T:client/BanditsNPCBearWinData.lua) bekommen je gelerntem Talent EINE Zusatzzeile `UI_BN_Bear_Win_TalentLine` "Talent %1: %2" an Leben, Ausdauer, Last,
Nahkampfschaden, Hunger, Durst; die alten Schluessel bleiben (keine Platzhalter-Aenderung in 8 Sprachen).

---

## 6. Icons (Kevin E:837-841) -- Weg, Dateien, KEIN Modell-Lauf

**Empfohlener Weg: eigene Vektor-Zeichnung mit Python/numpy wie das Herz** (`_arbeit/baer_zaehmen/f3/herz/herz_zeichne.py`, Kevin hat dort D "Goldrand" gewaehlt,
STAND.md:71-72): jedes Motiv aus Abstandsfeldern (Kreise, Kapseln, Vielecke, Boegen), je Pixel ueberabgetastet, DIREKT in 128 px gerechnet -> gestochen scharf,
kein Download, nichts kopiert. Aufbau je Icon: dunkles Medaillon mit Verlauf, Goldring mit Glanzlicht (wie Herz D), Motiv in Elfenbein mit 3-px-Rand, weichem
Schatten und Lichtkante. Dateien `TM:ui/`: `BanditsNPCBearTalent_<k>.png` (farbig, 128) und `BanditsNPCBearTalent_<k>_off.png` (grau, Ring grau) fuer 9 Talente
+ `BanditsNPCBearTalent_glow.png` (128, Leuchten) + `BanditsNPCBearTalent_lock.png` (64, Schloss) = **20 Dateien**, je ~5-20 KB. Im Fenster 56 x f (1080p 56 px,
4K 112 px <= 128 Quelle). Werkzeug im Bau-Lauf: `_arbeit/baer_zaehmen/talente/icons/talent_icons.py` (+ Blatt `KEVIN_talent_icons.png` 512 px zum Ansehen, vor dem
Fenster-Bau Kevin zeigen). Alternative (nur auf Kevins Wunsch): Blender-Medaillons (3D-Glanz, OPTIX) -- deutlich mehr Arbeit je Motiv.
**Modell-Lauf: keiner noetig** (keine neuen Clips, kein Modell). Angler braucht das Fischen (F5, eigener Plan).

---

## 7. Dateien und Aufteilung (KERN / OBERFLAECHE / ICONS / TEXTE / BENCH)

| Teil | Dateien |
|---|---|
| KERN | NEU `shared/BanditsNPCBearTalentRules.lua`, NEU `server/BanditsNPCBearTalent.lua`; Naehte: `shared/BanditsNPCBear.lua` (CFG-Block, B.OPTS +2), `shared/BanditsNPCBearStats.lua` (:380-381), `shared/BanditsNPCBearInvRules.lua` (:880), `shared/BanditsNPCBearRules.lua` (:717-719), `shared/BanditsNPCBearFoe.lua` (FoeHurt/knock/addPush + kp), `server/BanditsNPCBearNeeds.lua` (:547), `server/BanditsNPCBearGrow.lua` (:543, :800, GrowFix), `server/BanditsNPCBearHurt.lua` (B.DownHours :190/:257), `server/BanditsNPCBearSleep.lua` (:267, :335), `server/BanditsNPCBearGuard.lua` (:350), `server/BanditsNPCBearFightFoes.lua` (:251-261, take), `server/BanditsNPCBearFight.lua` (:865-881), `server/BanditsNPCBearInv.lua` (:142, :742), `server/BanditsNPCBearHeal.lua` (MARK_FIELDS, Restore, TakeNewerMark), `server/BanditsNPCBearRegistry.lua` (viewEntry), `server/BanditsNPCBearServer.lua` (Handle, Schleife), `TM:sandbox-options.txt` (+2 Bloecke nach BearSkillAgeCap :118-122) |
| OBERFLAECHE | `client/ISUI/BanditsNPCBearWindow.lua` (Reiter, Sichtbarkeit, Bestaetigung), NEU `client/ISUI/BanditsNPCBearTalentTab.lua`, NEU `client/BanditsNPCBearTalentData.lua`, `client/BanditsNPCBearWinData.lua` (Zusatzzeilen), `client/ISUI/BanditsNPCBearWinParts.lua` (Farben tab/talOn/talFree/talOff, style "tab"), `client/BanditsNPCBearFx.lua` (Krit-Zahl) |
| ICONS | `TM:ui/BanditsNPCBearTalent_*.png` (20) + Werkzeug |
| TEXTE | `Translate/<EN PTBR RU KO ES CN FR DE>/UI.json` (+ ~62), `Sandbox.json` (+4) |
| BENCH | NEU `client/NCBearBenchTalent.lua` (nie kopiert, BENCH_ANY) |

Texte (Schluessel, je 8 Sprachen; EN "Perks"): `UI_BN_Bear_Win_TabMain`, `_Win_TabTalents`, `_Win_TalentLine`; `UI_BN_Bear_Talent_Title`, `_Points` ("%1 Talentpunkt(e)
frei -- %2 von %3 vergeben"), `_PointsAll`, `_Row` ("Reihe %1"), `_Row1At` ("ab Tag %1"), `_Row2At`, `_Row3At`, `_RowDone`, `_RowIn` ("in %1 Tag(en)"),
`_StOn`/`_StFree`/`_StLocked`/`_StSoon`, `_Hint`, `_Reset`, `_ResetOff`, `_ResetWait` ("in %1 h"), `_LearnAsk` ("Talent \"%1\" lernen?\\n%2\\nEs bleibt fuer immer
aktiv."), `_ResetAsk`, je Talent `_<K>` / `_<K>_Short` / `_<K>_Tip` (27); Meldungen `UI_BN_Bear_Note_TalentPoint`, `_Note_TalentLearned`, `_Note_TalentReset`;
Gruende `UI_BN_Bear_Why_TalentMax`/`_Have`/`_Soon`/`_Row`/`_RowUsed`/`_Point`/`_ResetOff`/`_ResetWait`/`_None`. Sandbox `Sandbox_BanditsNPC_BearTalentReset`(+_tooltip),
`Sandbox_BanditsNPC_BearTalentResetDays`(+_tooltip). Pruefung wie NPC Crews langcheck (gleiche Platzhalter, CN/DE nur Vanilla-Zeichen), Round-Trip-JSON.

### 7.1 Sandbox (Kevins Ausnahme: hier bis zu 2 neue Regler)
```
BearTalentReset     = { def = false }                     -- Wachsen und Faehigkeiten: Talente zuruecksetzen erlaubt (Vorgabe AUS, Kevin E:815)
BearTalentResetDays = { def = 1, min = 0, max = 30 }      -- Spieltage zwischen zwei Resets (1 = hoechstens 1x je Spieltag; 0 = jederzeit)
```
`sandbox-options.txt`: zwei Bloecke `option BanditsNPC.BearTalentReset` (type = boolean) / `...ResetDays` (type = integer), `page = BanditsNPC`,
`translation = BanditsNPC_BearTalentReset...` wie :118-122. Das Uebernahme-Skript prueft sie schon allgemein gegen B.OPTS und Sandbox.json
(baer/tools/baer_uebernahme.py:1570-1633). 14 -> 16 Optionen; keine weitere.

### 7.2 Uebernahme-Skript (Naehte, `baer/tools/baer_uebernahme.py`)
- Regel `probeweg` (:510) + `TalentForce|TalentWipe` (nur Werkbank).
- Neue Regel `talentSet`: `rec.tal =` / `.tal =` nur in B.HandleTalent, B.HandleTalentReset, B.TalentFix, B.TalentFromMark (eine Schreibstelle je Weg).
- Neue Dateien heissen BanditsNPCBear* bzw. BanditsNPCBearTalent_*.png (gleicher relativer Pfad); keine NPC-Crew-Datei wird geaendert; NAEHTE.md: Sandbox +2.

---

## 8. SP / MP und rote Linien

| Punkt | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Lernen / Reset | `B.Ask` ruft `B.Handle` direkt (T:shared/BanditsNPCBear.lua:890-892) | `sendClientCommand` -> Server prueft alles (4.1), Client zeigt nur Sicht |
| Punkte | aus `rec.g` beim Schreiber | dito; Client rechnet nur Anzeige aus `talE` |
| Krit / Umwerfen / Rueckstoss | Schreiber wuerfelt (`ZombRand`), `B.OnFx` direkt | Server wuerfelt, Fx "hit" { dmg (schon x2), crit, knock, kp } an Spieler bis fxFoeDist (B.lua:927-950); der Zombie-Rechner (`hasAuth`, Foe.lua:284) setzt Leben/Umwerfen |
| Sandbox | `B.Opt` (B.lua:454-476) | Werte des Servers (B.lua:449) |
| Bestaetigung | Client-Fenster | Client-Fenster, nichts an den Server ausser der Bitte |

Rote Linien: **kein Gegenstand verloren/verdoppelt** (kein Talent fasst Inventar an; Lasttier-Reset ueberlaedt nur, Inv.lua:1014); **kein Kick** (nur Bitten der
Rolle user, keine Admin-/Cheat-Befehle, keine Engine-Werte vom Client); **nichts haengt** (keine Schleife ohne Deckel: 9 Talente, 3 Reihen; Dialog schliesst sich
selbst); **keine NPC-Crew-Figur gestoert** (Wachsam/Krit/Pranke gelten nur fuer B.FoeIsTarget-Ziele, FightRules.lua:366-380; NPC-Crew-Figuren sind nie Ziel).
Rueckwaerts: ein Spielstand ohne `tal` = nichts gelernt; Punkte erscheinen sofort nach Wachstum (ein Baer an Tag 50 hat beim ersten Laden 2 Punkte, Meldung einmal).

---

## 9. Attrappen-Faelle (lua5.1, `C:/Users/Kevin/Tools/lua51/lua5.1.exe`; alte Attrappen F3/F4/K1/Kampf bleiben gruen)

1. Punkte: g 0,09/0,10/0,149/0,15/0,999/1,0 -> 0/1/1/2/2/3; BearGrowDays 10 und 365 -> dieselben g-Schwellen; Kurve aus B.CFG.
2. Lernen: kein Punkt -> point; Reihe 3 vor ausgewachsen -> row; zweites in Reihe 1 -> rowUsed; 4. bei (gemockt) 5 Punkten -> max (R3); unbekannt -> still;
   fremder Spieler -> NotOwner; Angler -> soon; doppelte Bitte in 100 ms -> Drossel, nie 2 in einer Reihe; Modell B (`talRows=false`): beliebige 3, das 4. -> max.
3. Fix: "crit,crit,paw,fur,alert,zzz" -> "crit,paw" (Reihen) bzw. "crit,paw,fur" (frei) + eine Fehlerzeile; Zahl/Tabelle -> nil.
4. Spiegel: MarkOf hat tal/talR/talN; Restore MP mit g-Deckel 0,05 und "alert,paw" -> ""; SP TakeNewerMark: Spiegel "alert" gewinnt gegen Register "alert,paw"
   nur, wenn neuer; Koerper-Tausch/Unstuck/Aussehen: rec.tal unveraendert, TalentEarned unveraendert.
5. Reset: Sandbox aus -> ResetOff; an + Tage 1: Tag 5 ok, Tag 5 nochmal -> Wait, Tag 6 ok; Tage 0 -> immer; nichts gelernt -> None ohne Uhr; mit Lasttier und 120/90 kg
   -> Inventar gleich, ivX; mit Dickes Fell bei hp 0,5 -> 0,5 (Punkte 325 -> 200), nie 0.
6. Wirkung: rise 6,25 -> 4,1667; hpMax 400 -> 650 (Zaehigkeit 10: 600 -> 850); staMax x1,3 / Erholung x1,5; kpct halbstark 0 -> 100 nur swipe/slam (bite nicht);
   Fx kp 2; Cap +50 bei 50 % und 250 % Sandbox; FoeScan zwei Baeren (einer Wachsam): 15/18 und 10/12 im selben Lauf; Wecken 12; Verstecken 9/12; woke nie;
   HealRate x2 (wach 2, Schlaf 30); DownHours 6 in DownSlow UND DownView; Krit: ZombRand-Folge 10 -> krit (dmg x2, crit=true), 30 -> nicht.
7. Meldung: g ueber 0,10 -> eine Note; Sitzung weg (Laden) -> keine zweite (talN); GrowSetG runter/rauf -> keine zweite.
8. Sicht/Modell: tal/talE/talRo/talRw/talNx; Kachel-Zustaende A und B wie im Entwurf; Abzeichen = talE - #tal; Client-`TalentCan` = Server-`TalentCan`.
9. Fenster (Mitschrift-Kette wie k1/bild_nach): Reiterwechsel ohne stehende Tooltips, gleiche Hoehe beide Reiter, 1080p/4K, alle 8 Sprachen passen in die Kachel
   (sonst 2 Zeilen / Klein-Schrift), Krit-Zahl Large + Gold.
10. Dialog: Ja -> genau eine Bitte { id, k }; Nein / Esc -> keine; Baer inzwischen weg -> Server lehnt ab (Why_Gone).

## 10. Bench (`client/NCBearBenchTalent.lua`, nur Einzelspieler, nie kopiert)
`NCBear_TalentInfo()` (Punkte, gelernt, alle Werte vorher/nachher, Reset-Uhr) -- `NCBear_TalentLearn("crit")` (normaler Bitten-Weg) -- `NCBear_TalentForce("alert,paw")`
(setzt ohne Punkte, Regel probeweg) -- `NCBear_TalentWipe()` (Reset ohne Sandbox/Uhr, probeweg) -- dazu vorhandene `NCBear_CubGrow(days)` (T:client/NCBearBenchCub.lua:911)
und `NCBear_FightLog(true)` (Krit- und Umwerf-Zeilen ueber `B.LogEvery`, B.lua:529-544).

## 11. Bau-Lauf "baer-talente" (hoechstens 8 Agenten; vorher Verbrauch pruefen und Kevin die Zahl nennen)
Staging `_arbeit/baer_zaehmen/mod_talente/` = Test-Mod NACH Kevins K1-/Kampf-Test (+ deren Korrekturen; Needs/Grow/Fight/FightFoes/Sleep/Guard/Inv u. a. hat auch K1/Kampf geaendert). Berichte `_arbeit/baer_zaehmen/talente/`.
1. **KERN** (Abschnitte 2-4, 7 KERN) -- 2. **ICONS** (Abschnitt 6, parallel; Blatt fuer Kevin) -- 3. **TEXTE** (nach `talente/schnittstelle.md`, parallel) --
4. **OBERFLAECHE** (Abschnitt 5, nach der Schnittstelle parallel zu KERN) -- 5. **PRUEF_CODE** (luacheck/scopecheck/localcount/luacheck_pz, Attrappen 1-8, Uebernahme
Trockenlauf + Probe) -- 6. **PRUEF_BILD** (Mitschrift-Kette aus dem ECHTEN Code: Fenster DE/EN 1080p + 4K, Icons-Blatt) -- 7. **NACHBESSERUNG** -- 8. **GEGENPRUEFER +
INTEGRATOR** (Einbau-Skript nach `tools/einbau_kampf.py`, Anleitung, sichern.py, Commit/Push erst nach Einbau).

## 12. Testanleitung (Skizze fuer Kevin; Spiel neu starten)
1) Sandbox "Talente zuruecksetzen" an (nur zum Testen). 2) `NCBear_CubGrow(10)` -> Meldung "Talentpunkt", Reiter Talente: Reihe 1 offen. 3) Wachsam lernen (Ja) ->
leuchtet; Zombie naehert sich: Junges versteckt sich ab ~9 Kacheln. 4) `NCBear_CubGrow(15)` -> Punkt 2 -> Schwere Pranke -> jeder Hieb wirft um. 5) `NCBear_CubGrow(100)`
-> Punkt 3 -> Kritischer Treffer -> ab und zu goldene grosse Zahl. 6) Alle Kacheln gesperrt, kein 4. Talent. 7) Unstuck, Aussehen wechseln, speichern + laden ->
Talente bleiben, keine neuen Punkte. 8) Zuruecksetzen -> 3 frei; nochmal am selben Tag -> abgelehnt mit Wartezeit.

## 13. Fragen fuer Kevin -- siehe Rueckgabe (8 Fragen, je Empfehlung zuerst; "Ja, alle so" nimmt jede Empfehlung)
