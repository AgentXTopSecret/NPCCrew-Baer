# Lauf baer-b1d: PLAN -- Wachsen, taeglich steigende Werte, Faehigkeiten, Heilen-Vorbereitung, Anzeige, Bench (B1d)

Stand 11.11.2026 Nachtschicht. **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2. Verbindlich fuer zwei Bauer (KERN,
OBERFLAECHE, gleichzeitig, getrennte Dateien) und den ZUSAMMENBAU danach. Baut auf dem Staging `_arbeit/baer_zaehmen/mod/` (B1a + B1b +
B1c inkl. Nachbesserung, Liste `staging_dateien.txt`).
Kurzformen: `FD x.y` = `forschung_b1d.md` Abschnitt x.y; `PB1C x.y` = `PLAN_B1C.md`; `PB x.y` = `PLAN_B1B.md`; `PZ x.y` = `PLAN_ZAEHMEN.md`;
`S:` = Staging `mod/42/media/lua/`; `V:` = Vanilla `media/lua/` (42.22.2); `B:` = Bandits `42.22/media/lua/`; `NC:` = NPC Crew `42/media/lua/`
(nur gelernt); `T:` = Test-Mod `NCBearTest/42/media/lua/`; `dec/` usw. = Jar-Auszuege (**NUR JAR** = Lesehilfe, kein Beleg);
`ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`; `B` = `BanditsNPC.Bear`, `U` = `B.UI`.

Kevins Worte, auf denen der Plan steht (ENT ab "Wachsen und Kampfkraft bis ganz gross", Nachtschicht-Freigabe Punkt 4):
*"standardmaessig bin ich so fuer 100 tage bis max gross"* -- *"ja mach das so als standard und in der sandbox einstellbar und die werte von
baeren muessen pro tag steigen"* -- Werte *"leben und schaden, und vllt noch ausdauer? und fischen als skill?"*, *"genau traglast das stimmt
auch noch"* -- Agilitaet *"das levelt pro hit den er kassiert wie das leben ... aber zusetzlich geht das leben auch hoch pro wachstums tage"* --
Kondition/Kaempfen *"ja und kaempfen damit meinst du ja sicher schaden"*, *"mach +70% bei stufe 10"* -- Spuernase *"in den einstellungen
abschaltbar"* -- Heilen *"echt langsam"*, *"beim schlafen soll er viel schneller geheilt werden"* -- Anzeige *"jeden wert einzelnd ... im balken
oder als zahl frei auswaehlbar"*, *"den rest wil ich aber"* -- Freigabe *"Wachsen 100 Tage + taeglich steigende Werte (Plan + Bau)"*.
Fest aus ENT: Groessen 0,35 / 0,75 / 1,35, Meilensteine Tag 15 / 45 / 100, Traglast 10 / 40 / 100, Ausweichen 5 % .. 40 % (Hoechstwert
Sandbox), Kaempfen +70 % auf Stufe 10, Heilen wach ~1 %/Spielstunde, Schlaf ~15 %/Spielstunde. Alles andere ist VORSCHLAG des Planers
(Stellwert, Sandbox oder Frage in 11).

**Nicht zurueckbauen:** alles aus B1a/B1b/B1c inkl. Nachbesserungen (Spiegel v2, `u`/`gen`/`r`, Heil-Regeln, Mitfahren, Call to me, Laerm-
und Zombie-Wache, Gehen, Markierung, Karte, Optionen-Seite, Fix 1-3). **Nicht anfassen:** die alten Dateien des Erwachsenen in der Test-Mod
(`T:shared/NCBearFight.lua`, `NCBearDefs.lua`, `NCBearSize.lua`, `NCBearBench.lua` ...). Die Werkbank des Jungen
`S:client/NCBearBenchCub.lua` ist KEINE alte Datei (B1a-Bau im Staging) und wird nach Auftrag 7 erweitert.

---

## 0. Entscheidungen des Planers (gelten fuer alle)

**0.1 Die Wachstums-Uhr steht im Register: `rec.g` = Wachstum 0..1** (FD 1.4), nur fuer `st == "tame"`. Je Langsam-Takt (10 Spielminuten,
`dt` in Spielstunden, je Schritt gedeckelt `maxDtH` 1,0, `S:server/BanditsNPCBearServer.lua:565-570`): `g = min(1, g + dt / (D x 24))`,
`D = B.Opt("BearGrowDays")`. Ein Anteil statt "Stunden seit tamedAt": ein Sandbox-Wechsel von D aendert nur das kuenftige Tempo, nie
schrumpft ein Baer. Engine-Alter und Engine-Stufen werden NICHT benutzt (FD 2: Stufenwechsel baut ein neues Tier ohne ModData, Alter zaehlt
nur geladen, Mitfahren/Call to me bauen den Koerper neu).

**0.2 Kurve stueckweise gerade durch Kevins Tabelle** (FD 1.5): Stuetzpunkte `(x = g, Groesse)` = `(0, 0,35) (0,15, 0,75) (0,45, 1,0)
(1,0, 1,35)`. Bei D = 100: Tag 15 = 0,75, Tag 45 = 1,0, Tag 100 = 1,35; bei anderem D anteilig (D = 50: Tag 7,5 / 22,5 / 50). Vorne schneller,
hinten langsamer (Zuwachs je Tag 0,0267 : 0,0083 : 0,0064). Stufen nach der INNEREN Groesse s: `cub` < 0,75 <= `half` < 1,0 <= `strong`
< 1,35 <= `adult`.

**0.3 Definition wird Weg B** (FD 1.3, Frage F1 mit Empfehlung ja): `S:shared/BanditsNPCBearDefs.lua` `minSize = 0.35`, `maxSize = 1.35`,
`stages[CUB] = { ageToGrow = 36500 }`. Grund (NUR JAR, FD 0.2): `setSize` klemmt immer auf [min, max] und laeuft beim Laden, bei der
MP-Erst-Uebertragung, je Alterstag in `growUp` und in einer Tierzone; bei min = max ginge jede gesetzte Groesse dabei auf 0,35 zurueck.
Neue Koerper starten weiter bei 0,35 (`initSize` endet mit `setSize(0.1F)` -> minSize, `dec/AnimalData.java:1353-1358`, gegengelesen);
Engine-Wachsen danach `1,0 / 36500 x Leben` je Alterstag = praktisch 0. Der Plan funktioniert AUCH mit Weg A (das Nachsetzen je Hirn-Takt
in 0.4 deckt beides) -- lehnt Kevin F1 ab, werden nur die zwei Zeilen zurueckgedreht.

**0.4 Groesse setzen: EINE Stelle `B.ApplySize(a, sz)`** (KERN, `shared/BanditsNPCBearStats.lua`): `a:getData():getSize()` lesen, nur bei
`|alt - sz| > B.CFG.sizeEps` (0,002) `a:getData():setSizeForced(sz)` (BELEGT, Abschnitt 8 Nr. 1-3). Gerufen:
- beim Schreiber je Hirn-Takt fuer jedes geladene zahme Junge (`B.GrowLive`, 2 Java-Aufrufe, schreiben selten) -- faengt Laden, Tierzone,
  Debug-Alter und Weg A ab;
- beim Schreiber sofort am neuen Koerper (`B.PlaceCub` -> `B.GrowBody`: Aussteigen, Call to me, Tod-im-Auto);
- **nur am MP-Client** im Listenbau der Anzeige (<= 1 x/s, `isClient()`): an seiner Kopie mit `sz` aus der Sicht. Grund (NUR JAR, FD 0.3): das
  laufende Tierpaket traegt keine Groesse, nur die Erst-Uebertragung. Im SP ist die Kopie das Schreiber-Objekt -> der Client tut nichts.
Gesetzt wird immer die GEZEIGTE Groesse `sz`, gerechnet wird mit der INNEREN `s` (0.10).

**0.5 Leben am Tier = Anteil 0..1, die Wahrheit steht im Register** (FD 3.1, 5.2 Weg B1): `rec.hp` (Anteil, Wahrheit) und `rec.hpB` (Wert,
den wir zuletzt am Koerper gesetzt bzw. gesehen haben). Je Langsam-Takt (EINE Stelle `B.BodyHp`): `h = a:getHealth()`; `h < hpB - hpEps` ->
der Koerper hat seit unserem letzten Blick verloren (Engine-Schaden: Spieler-Waffe, anderes Tier, Anhaenger) -> `hp = hp - (hpB - h)`;
`h > hpB + hpEps` -> die Engine hat selbst geheilt (`dec/AnimalData.java:377-398`, ~1,5-2,2 %/h, FD 0.7) -> zuruecknehmen; dann unsere
Heilung `hp = min(1, hp + BearHealAwake / 100 x dt)`; ist `|h - hp| > hpEps`: `a:setHealth(hp)`, `hpB = hp`. Nie ueber 1,0 (MP-Byte laeuft
ab 1,27 ueber, `dec_b1b/NetworkPlayerAI.java:280`), nie 0 (das ist der Tod), nicht am toten Tier. Punkte = `hp x hpMax` nur in Register und
Sicht. Ohne Koerper (Fahrt, entladen) heilt nur `rec.hp`; der naechste Abgleich setzt den Koerper (ein Anstieg zaehlt nie als Schaden -- das
ist der Grund fuer `hpB`). Fehlt `hp` (alter Eintrag, Heilung aus dem Spiegel): beim ersten Abgleich aus dem Koerper uebernehmen.

**0.6 Werte rein aus der inneren Groesse s, stueckweise gerade zwischen 0,35 / 0,75 / 1,35** (FD 3.2, Stuetzwerte Stellwerte):
| s | 0,35 Jungtier | 0,75 Halbstark | 1,0 (gerechnet) | 1,35 Erwachsen | Quelle |
|---|---|---|---|---|---|
| Leben max (Punkte) | 40 | 150 | 254 | 400 | ENT:14-19 "Vorschlag als Vorgabe" (F3) |
| Ausdauer max | 50 | 100 | 125 | 160 | Vorschlag (F3) |
| Traglast | 10 | 40 | 65 | 100 | **Kevin** (ENT:30, Auftrag) |
| Schaden-Faktor | 0 | 0,35 | 0,62 | 1,0 | Vorschlag; 1,0 = heutige Erwachsenen-Werte `T:shared/NCBearFight.lua:92` (F3) |
Danach die Faehigkeiten obendrauf (0.7). Weil s je Langsam-Takt waechst, steigen alle Werte JEDEN TAG ein Stueck (Kevin), ohne Sprung.

**0.7 Faehigkeiten: je Faehigkeit EINE Zahl (Erfahrung), die Stufe 0..10 wird daraus gerechnet** (NC-Lehre FD 4.1, nie zwei Wahrheiten).
Felder `xAgi` Agilitaet, `xVit` Leben-Bonus, `xCon` Kondition, `xFgt` Kaempfen, `xFsh` Fischen, `xNos` Spuernase. Bedarf je Stufe
`{ 100, 116, 135, 156, 181, 210, 244, 283, 328, 380 }` (je Stufe x 1,16 -- "hinten langsamer"), Summe bis Stufe 10 = **2133** (FD 4.2 nennt
2033: Rechenfehler, hier berichtigt). Tempo-Deckel: Echtzeit-Eimer je Junges und Faehigkeit nur in der Sitzung (`xpPerMin` 6, bis
`xpBucketMin` 3 Minuten ansparen; NC-Lehre `NC:shared/BanditsNPCSkills.lua:475-565`). Wirkung linear in der Stufe:
| Faehigkeit | Wirkung (Formel) | Erfahrung durch | in B1d verdrahtet |
|---|---|---|---|
| Agilitaet | Ausweichen % = `dodgeBase` 5 + (`BearDodgeMax` - 5) x L / 10 -> 5 .. 40 % (**Kevin**) | eingesteckter Treffer `xpHitTaken` 10 | nein (Haken `B.OnHitTaken`) |
| Leben-Bonus | Leben max x (1 + `vitPerLv` 0,05 x L) -> +50 % (ENT:21) | eingesteckter Treffer `xpHitTaken` 10 | nein (Haken `B.OnHitTaken`) |
| Kondition | Ausdauer max x (1 + `conPerLv` 0,05 x L), Erholung ebenso | eigener Rennbefehl: 1 je `conTilesPerXp` 5 Kacheln; ausser Puste `conBreathXp` 5 (je `conBreathMs` 60 s) | **ja** (0.8) |
| Kaempfen | Schaden x (1 + `BearFightBonusMax` / 100 x L / 10) -> +70 % (**Kevin**) | ausgeteilter Treffer `xpHitDealt` 5 | nein (Haken `B.OnHitDealt`) |
| Fischen | Fang-Chance % = 0 unter Halbstark, sonst `fishBase` 10 + (`fishMax` 60 - 10) x (0,5 x L / 10 + 0,5 x (s - 0,75) / 0,6) | Versuch `xpFishTry` 2, Fang `xpFishCatch` 10, erst ab Halbstark | nein (Haken `B.OnFish`) |
| Spuernase | Warnweite Kacheln = `noseBase` 12 + `noseStep` 1,5 x L | rechtzeitige Warnung `xpSniff` 5 | nein (Haken `B.OnSniff`); Schalter kommt mit dem Verhalten |

**0.8 Ausdauer (aktueller Wert) wird in B1d gefuehrt, nur in der Sitzung, ohne Wirkung** (FD 4.5): `s.sta` Anteil 0..1 (Vorgabe voll).
Sinkt nur bei UNSEREM Rennbefehl (`s.walk == false` und `ms < s.ownUntil`, beides setzt `B.MoveTo`, `S:server/BanditsNPCBearWorld.lua:873-874`)
um `Weg x staRunCost / staMax` (0,4 Punkte je Kachel), steigt sonst um `staRegen x dt_s x (1 + 0,05 x L_con) / staMax` (2 Punkte je s).
Bei 0 "ausser Puste" -> Kondition-Bonus. Wozu: Kevins Anzeige (Ausdauer-Balken) und "vor allem Ausser-Puste-Kommen" (ENT:226). Gemuetliches
Hinterhergehen zaehlt nicht (Gehen ist `walk = true`), Laerm-Ersatzweg auch nicht. Nicht gespeichert: nach dem Laden voll (ehrlich, F13).

**0.9 Alle B1d-Uhren laufen nur, solange der Besitzer im Spiel ist** (`online[rec.owner]`, wie die Uhren in B1a, F4) und nicht bei
`st == "missing"` (F8; der Langsam-Takt kehrt dort heute frueh zurueck, `S:server/BanditsNPCBearServer.lua:485-491`). Mitfahrend: laeuft weiter.
Wilde, scheue, angefuetterte Junge: nichts (Kevin "ab dem Zaehmen").

**0.10 Modellwechsel nur vorbereitet, abgeschaltet** (Auftrag 2): `B.BodyOf(rec)` entscheidet Koerper und gezeigte Groesse:
`"cub", min(s, B.CFG.cubMaxSize)` (0,75). `B.CFG.bodySwap = false`. Steht `bodySwap` auf true, gibt `B.BodyOf` in B1d trotzdem `"cub"` und
`B.GrowLive` schreibt EINE Fehlerzeile je 10 min ("body swap is not built yet"). Die Stelle, an der der spaetere Lauf tauscht, steht als
Kommentar in `B.GrowLive` (Tausch ueber `B.RemoveCub` + `B.PlaceCub` mit `gen + 1`, PB1C 0.2/0.3; `B.CreateCub` kennt heute nur `B.CUB`,
FD 1.7). Nie die alte Art `bear` (deren `NCBearFight.lua` greift sofort an = B5a). Groesse und Werte laufen intern weiter bis 1,35.

**0.11 Sicht traegt fertige Zahlen** (Client rechnet nie mit eigenen Sandbox-Annahmen): `sz hp hpMax sta staMax day stg nst nxt`, nur bei
`st == "tame"` (4.1). Neu geschickt mit jedem `B.Commit` (Wachstum hoechstens je Spielstunde, sofort bei Stufenwechsel, Stufenaufstieg einer
Faehigkeit, Schaden >= `hpCommit` 2 %) und fuer die Ausdauer gedrosselt (>= `staViewStep` 10 Punkte Aenderung UND >= `viewMoveMs` 5 s, nur an
den Besitzer).

**0.12 Aufteilung:** KERN = `shared/` (ohne Translate) + `server/` + `attrappe/kern/attrappen.lua` + `attrappe/b1d_kern/`; OBERFLAECHE =
`client/` (mit `ISUI/` und Bench), alle Texte, `sandbox-options.txt`, `ober_werkzeug/texte_b1d.py`, `attrappe/b1d_ober/`. Neue Dateien:
KERN 2 (`shared/BanditsNPCBearStats.lua`, `server/BanditsNPCBearGrow.lua`), OBERFLAECHE 0 Lua (nur Werkzeug + Attrappe). Keine Datei fuer beide.

**0.13 Nicht in B1d:** Kampf, Zombie-Angriffe, Treffer (die Haken bleiben ohne Aufrufer), Schlafen (`BearHealSleep` wirkt noch nicht),
Fischen- und Spuernase-Verhalten (auch kein Spuernase-Schalter), Hunger/Durst/Muedigkeit, Inventar (Traglast nur Zahl), Baeren-Fenster (V),
Modellwechsel einschalten, neues Modell, DODGE-Anzeige, Aenderung an `T:`-Dateien des Erwachsenen, Streichel-Haltung (`PetAction` bleibt fest 0,5).

---

## 1. Verhalten je Auftragspunkt, Schritt fuer Schritt

### 1.1 (Auftrag 1) Wachsen
1. **Zaehmen:** `B.TameCheck` setzt wie bisher `st = "tame"`, `tamedAt = now` (`S:shared/BanditsNPCBearRules.lua:68-80`, unveraendert).
   `rec.g` fehlt noch -> der naechste Langsam-Takt (oder `B.InitRegistry` nach dem Laden) setzt ueber `B.GrowFix` `g = clamp((now - tamedAt)
   / (D x 24), 0, 1)` -- frisch gezaehmt also 0. Groesse 0,35, Leben 40, Traglast 10.
2. **Je Langsam-Takt** (`B.GrowSlow`, aus `slowTickBody` nach `slowRec`): nur `st == "tame"` mit Besitzer online. `g` waechst (0.1); alte und
   neue Stufe vergleichen; Leben abgleichen und heilen (0.5); hoechstens je `growCommitH` (1 Spielstunde) EIN `B.Commit` (r + 1 -> Spiegel und
   Sicht). Stufe gestiegen -> sofort `B.Commit` und Meldung an den Besitzer (wenn da) `UI_BN_Bear_Note_Grown` mit `t = "stage"`, `v = "half"` /
   `"strong"` / `"adult"`: "Your bear is half-grown now." / "... strong now." / "... full-grown now." + `B.Log("grow: b1 is half-grown (day 15)")`.
3. **Je Hirn-Takt** (`B.GrowLive`, aus `liveRec` fuer jedes geladene zahme Junge): Groesse nachsetzen (0.4), fehlendes Leben aus dem Koerper
   holen (0.5), Ausdauer/Kondition (0.8). Kein Commit (ausser Stufenaufstieg einer Faehigkeit).
4. **Fuettern beschleunigt etwas** (Kevin 08.11., F7): `B.FeedComplete` Zweig `wasTame` (`S:server/BanditsNPCBearServer.lua:243`; Abklingzeit
   120 min und "nur der Besitzer" gelten schon, `Rules.lua:144-156`) ruft `B.GrowFeed(rec, class, now)` VOR dem vorhandenen `B.Commit`:
   `add = h / (D x 24)` mit `h` = `feedGrowFav` 3 (Lieblingsfutter) / `feedGrowOk` 2 / `feedGrowSnack` 1 Spielstunden; hoechstens `feedGrowDay`
   2 Gutschriften je Spieltag (`gFd` = Tag, `gFn` = Zahl), Summe `gF <= feedGrowMax` 0,10 (= 10 Tage bei D = 100); nie ueber g = 1. Meldung
   bleibt "It enjoys that." (keine neue). Bestes Fuettern: 2 x 3 h je Tag = 25 % schneller, bis 10 Tage frueher. Hunger bremst noch nicht
   (es gibt ihn nicht).
5. **Wilde/scheue/angefuetterte Junge:** kein `g`, keine Groessen-Probe, kein Wert in der Sicht. (Engine-Wachsen ~0 mit Weg B.)
6. **Speichern/Laden:** `g`, `gF`, `gFd`, `gFn` stehen im Register (globale ModData, Spielstand); der Koerper speichert seine Groesse selbst
   (Laden mit Klemme [0,35, 1,35] -> bleibt, Weg B). Der erste Hirn-Takt nach dem Binden setzt ohnehin nach.
7. **Tod:** `B.Close(rec, "dead")` wie B1a -- Eintrag und alle Werte weg, Sperre 7 Tage, ein neues Junges beginnt wieder bei 0.
8. **Besitzer offline (MP):** keine Uhr laeuft; das Tier bleibt in seiner Groesse stehen, andere sehen es so. Nach dem Einloggen geht es weiter.
9. **Zweiter Spieler:** kann ein fremdes zahmes Junges nicht fuettern (`Why_NotOwner`, unveraendert) -> kein Bonus; sieht dieselbe Groesse
   (seine Client-Probe) und dieselben Werte-Zeilen (ENT:106).
10. **Vermisst / Mitfahren / Call to me:** 0.9 und Abschnitt 3.

### 1.2 (Auftrag 2) Modellwechsel vorbereitet
1. Das Junge waechst mit seinem Modell bis `cubMaxSize` 0,75 (bei D = 100: Tag 15) und bleibt dort im Bild stehen; `s`, Stufe, Werte, Tage
   laufen weiter (Bench `NCBear_CubStats()` zeigt "inner 1.02 / shown 0.75").
2. Namensschild-Hoehe waechst mit der gezeigten Groesse: Anker `a:getZ() + tagZ x sz / tagBase` (`tagBase` 0,35; FD 1.7, Wert im Spiel ansehen).
3. Kein Tausch, keine neue Art, kein Engine-Aufruf dafuer. Haken siehe 0.10. Offene Frage F11 (Junges- oder Erwachsenen-Modell fuer Halbstark).
4. Rest-Risiken (alle ungeprueft, Kevins Blick): Fussgleiten (Tempo liest die Groesse nicht, FD 1.2, F2), Streichel-Haltung "lamb" mit fester
   Hoehe, Folgen-Abstaende `followNear` 3 / `followStart` 4,5 bei 1,5 m Koerperlaenge.

### 1.3 (Auftrag 3) Werte, die jeden Tag steigen
1. `B.StatsOf(rec)` (rein, shared) rechnet aus `g` -> `s` und den Faehigkeiten: `hpMax`, `staMax`, `carry`, `dmg`, `dodge`, `fightBonus`, `fish`,
   `nose`, `stage`, `next`, `nextDays`, `day`, `sz`, Stufen je Faehigkeit. Beispiele (D = 100, alle Faehigkeiten 0): Tag 5 -> s 0,48 / Leben 77 /
   Traglast 20; Tag 15 -> 0,75 / 150 / 40; Tag 30 -> 0,875 / 202 / 52; Tag 45 -> 1,0 / 254 / 65; Tag 70 -> 1,16 / 321 / 81; Tag 100 -> 1,35 / 400 / 100.
2. Leben am Tier: Anteil (0.5); waechst `hpMax`, bleibt der Anteil -- ein voller Baer bleibt voll.
3. Traglast: nur Zahl (das Inventar kommt spaeter, FD 3.3). Schaden: nur Faktor (B5a liest ihn).
4. Meldungen: keine eigenen fuer Werte (die Stufen-Meldung 1.1.2 genuegt). Speichern/Laden, Tod, offline, zweiter Spieler: wie 1.1 (die Werte
   sind gerechnet, nicht gespeichert -- nur `g`, `x*`, `hp`, `hpB`).

### 1.4 (Auftrag 4) Faehigkeiten -- Daten, Formeln, Kurve, Haken
1. Daten und Formeln wie 0.7. `B.SkillAdd(rec, key, xp, ms)` ist der EINE Weg, Erfahrung gutzuschreiben (Eimer, Deckel `CUM[10]` = 2133).
2. **Stufenaufstieg:** `B.Commit` + Meldung an den Besitzer (wenn da) `UI_BN_Bear_Note_SkillUp` mit `t = "skill"`, `v = "con"`, `w = 3`:
   "Your bear's endurance is now level 3." + `B.Log`. Kein Abstieg (nur die Bench setzt XP zurueck).
3. **In B1d wirkt nur Kondition** (0.8): Rennen beim Folgen, Verstecken/Fliehen vor Zombies (beides unser Rennbefehl). Weg je Hirn-Takt aus den
   Lagen, die `liveRec` ohnehin liest (`S:server/BanditsNPCBearServer.lua:741`); mehr als `conStepMax` 8 Kacheln je Takt = Neu-Erzeugen ->
   nicht gezaehlt. Wie viel Rennen in 100 Tagen zusammenkommt: unbekannt (F14, Stellwerte).
4. Haken ohne Aufrufer (fuer B5a, Fischen, Spuernase): `B.OnHitTaken(rec, dmg, ms)` (Agilitaet + Leben-Bonus), `B.OnHitDealt(rec, ms)`
   (Kaempfen), `B.OnFish(rec, caught, ms)` (nur ab Halbstark), `B.OnSniff(rec, ms)`. Nur Erfahrung, kein Verhalten.
5. Speichern/Laden: `x*` im Register und Spiegel; Eimer nur Sitzung (nach dem Laden voll). Tod: weg. Offline: es gibt keine Uebung.
   Zweiter Spieler: sein Rennen zaehlt nie fuer fremde Junge (nur deren eigener Rennbefehl).

### 1.5 (Auftrag 5) Heilen-Vorbereitung
1. Formel (Kevin, ENT:271-272): `hp = min(1, hp + rate / 100 x dt)`, `rate` = `BearHealAwake` (1,0 % des Hoechstwerts je Spielstunde -> fast tot
   bis voll ~4 Spieltage) bzw. spaeter im Schlaf `BearHealSleep` (15 %, `B.HealRate(asleep)` kennt beide; in B1d immer wach).
2. Belegter Leben-Weg existiert (`setHealth(Zahl)`, Abschnitt 8 Nr. 5) -> wach WIRD angewendet, und die Engine-Heilung wird zurueckgenommen (0.5,
   F5: damit es wirklich "echt langsam" ist; sonst heilte die Engine ~2 %/h obendrauf).
3. Ohne Koerper (Fahrt, entladen, Besitzer online) heilt nur der Register-Wert; Besitzer offline: nichts.
4. Meldungen: keine. Diagnose: `B.Log("hp: b1 0.62 -> 0.63 (+0.01 heal, engine +0.02 taken back)")` nur bei Abgleich mit Aenderung.
5. Speichern/Laden: `hp`, `hpB` im Register, das Tier speichert sein Leben selbst (`dec/IsoAnimal.java:1340`/`:1451`). Tod: Engine (Leben 0) ->
   `B.Close` wie B1a. Zweiter Spieler: sieht dieselbe Zahl (Sicht) bzw. die Engine-Kopie (Tierpaket, 1 %-Schritte).
6. Von-Hand-Heilen und NPC-Heiler: spaeter (ENT:270); `B.GrowSetHp` ist schon der Weg dafuer.

### 1.6 (Auftrag 6) Anzeige
1. **Optionen -> Mods -> "NPC Crew: Bear"** (B1c-Seite, `S:client/BanditsNPCBearOptions.lua:50-65`) bekommt nach `TagShow`:
   `TagHealth` (Auswahl Off / Bar / Number, Vorgabe **Bar**), `TagStamina` (Vorgabe **Off**), `TagAge` (TickBox, Vorgabe **an**), danach wie
   bisher `TagSize` (F9). Je Spieler (ENT:106), der Server kennt sie nicht.
2. **Namensschild** (`S:client/ISUI/BanditsNPCBearHud.lua`): je zahmem Jungen wahlweise bis zu fuenf Zeilen. Der Block waechst vom Anker nach
   oben, von unten: Ausdauer -> Leben -> Alter-Zeile -> Zustand -> Name. Jede Zeile einzeln: Name + Zustand an `TagShow` (B1c, unveraendert
   "Name and state"), Leben an `TagHealth`, Ausdauer an `TagStamina`, Alter an `TagAge`. Ist ALLES aus, bekommt das zahme Junge keinen Eintrag
   (zaehlt nicht gegen `hudMax`). Zaehm-Balken wilder Junge: unveraendert (immer).
3. **Balken:** Breite/Hoehe der Groessenstufe (B1c `tierOf`), Hintergrund schwarz, Rahmen wie der Zaehm-Balken, Fuellung Leben rot
   (0,85 / 0,20 / 0,20), Ausdauer gelb (0,95 / 0,80 / 0,25); ohne Text. **Zahl:** "Health 92/150", "Stamina 40/50" (Punkte gerundet).
   **Alter:** "Day 12 - half-grown in 3 day(s)"; ausgewachsen "Day 100 - full-grown". "Tag" = Wachstumstag `floor(g x D)` (Fuettern zieht ihn
   vor, Pausen halten ihn an, F12).
4. Gleiche Zeilen fuer eigene und fremde zahme Baeren (Kevin "was ich sehe"). Fehlt ein Wert in der Sicht (z. B. `hp` noch unbekannt): die
   Zeile entfaellt.
5. MP-Client: im selben Listenbau die Groessen-Probe an der Kopie (0.4).

### 1.7 (Auftrag 7) Bench (nur `client/NCBearBenchCub.lua`, nur SP, nie kopiert)
| Befehl | Tut |
|---|---|
| `NCBear_CubGrow(tage)` | mein naechstes zahmes Junges (`myTame`): `B.GrowSetG(rec, g + tage / D)` (geklemmt 0..1, negativ = zurueck, F10), dann `B.BrainTick(true)`, Sicht schicken, eine Zeile wie `NCBear_CubStats` (Tag, Groesse innen/gezeigt, Stufe, Leben) |
| `NCBear_CubStats()` | drucken: Kennung, Name, g, Wachstumstag, Kalendertage seit dem Zaehmen, Groesse innen / gezeigt, Stufe, naechste Stufe in Tagen, Leben (Anteil, Punkte / Hoechstwert, `hpB`), Ausdauer (Sitzung, Punkte / Hoechstwert), Schaden-Faktor, Traglast, je Faehigkeit XP / Stufe / XP in der Stufe / Bedarf, Ausweichen %, Kampf-Bonus %, Fang-Chance %, Warnweite, Fuetter-Bonus (gF, gFn heute), Engine `getSize` und `getHealth` des lebenden Tiers |
| `NCBear_CubXp(key, xp)` | `B.SkillSet(rec, key, xp)` (agi/vit/con/fgt/fsh/nos, absolut, geklemmt); falscher Schluessel -> Liste der Schluessel |
| `NCBear_CubHurt(pct)` | `B.GrowSetHp(rec, pct / 100)` (1..100) -- Heilen und Balken pruefen |
Rechtsklick "NC Bear" zusaetzlich "Cub: grow 5 days", "Cub: stats" (englische Literale, nur Bench). `NCBear_CubSet`-Hilfetext nennt die
B1d-Gruppe (5.2). `NCBear_CubInfo` druckt je Eintrag zusaetzlich `g`, `hp`, `hpB`, `x*`. `ready()` lehnt im MP ab (`:61-82`).

---

## 2. Register und Spiegel (B1d-Ergaenzung zur Register-Selbstheilung)

### 2.1 Neue Register-Felder (nur `st == "tame"`/`"missing"`; nur Zahlen; bei allen anderen nil)
```
rec += {
  g   = 0..1,                 -- Wachstum (0.1)
  gF  = 0..feedGrowMax,       -- Summe Fuetter-Bonus (Anteil)
  gFd = <Spieltag-Zahl> | nil, gFn = 0..feedGrowDay,   -- Fuetter-Bonus heute
  gAt = <Weltstunden> | nil,  -- letztes Wachstums-Commit (nicht im Spiegel)
  hp  = 0..1 | nil, hpB = 0..1 | nil,                  -- Leben (0.5; nicht im Spiegel)
  xAgi, xVit, xCon, xFgt, xFsh, xNos = 0..2133,        -- Erfahrung (0.7)
}
Sitzung B._s[id] += { sta, sta0, breathAt, kx, ky, kAt, kAcc, staV, staVAt, xb = { [key] = { t, at } }, swapErrAt }
```
Die Sitzung wird mit `B._s[id] = nil` in `B.Close` und `B.InitRegistry` geleert (Deckel = Zahl der Eintraege). `clearBodySession` (Ride.lua)
leert `kx/ky/kAt/kAcc` NICHT -- das macht `B.GrowBody` am neuen Koerper selbst.

### 2.2 `B.GrowFix(rec, now, log)` -- Migration und Klemmen (KERN Grow.lua)
- Gerufen in `B.InitRegistry` je Eintrag mit `log = true` (eine `B.Err`-Zeile nur bei UNSINN: Text, NaN, ausserhalb), und je Langsam-Takt in
  `B.GrowSlow` mit `log = false` (billig: ~15 `tonumber`).
- tame/missing: `g` Zahl -> 0..1; fehlt -> aus `tamedAt` (`(now - tamedAt) / (D x 24)`, geklemmt; ohne `tamedAt` 0) und nur `B.Log` (B1c-Eintrag,
  erwartet); `gF` 0..feedGrowMax, `gFn` 0..feedGrowDay (ganz), `gFd` Zahl oder nil; `x*` 0..2133 (fehlt -> 0); `hp`/`hpB` 0..1 oder nil (<= 0
  -> nil: neu aus dem Koerper holen).
- andere Zustaende: alle B1d-Felder nil.
- Kevins laufender Spielstand: sein Junges (gezaehmt 11.11.) bekommt `g` aus `tamedAt` -> es ist nach dem Neustart "Tag N" seit dem Zaehmen.

### 2.3 Spiegel (Fassung bleibt `B.MARK_V = 2`)
- `MARK_FIELDS` (`S:server/BanditsNPCBearHeal.lua:38-41`) += `"g", "gF", "gFd", "gFn", "xAgi", "xVit", "xCon", "xFgt", "xFsh", "xNos"`.
  Nicht im Spiegel: `hp`, `hpB` (das Tier traegt sein Leben selbst, `dec/IsoAnimal.java:1340`), `gAt`, Sitzung.
- Keine neue Fassung: `B.MarkFresh` vergleicht weiter v / id / u / r (`:76-79`); Leser nehmen fehlende Felder als "nicht da" (2.2 holt `g` dann
  aus `tamedAt`). Das stuendliche Commit erneuert den Spiegel -> ein Registerverlust kostet hoechstens eine Spielstunde Wachstum und die
  Erfahrung dieser Stunde.

### 2.4 Wiederherstellungs-Regeln (`B.GrowFromMark(rec, mark, how)`, KERN Grow.lua; gerufen aus Heal.lua)
| how | Wo | Regel |
|---|---|---|
| `"restore"` | `B.Restore` (`Heal.lua:222-242`), direkt VOR `B.InsertRec`, nur wenn der neue Eintrag `tame` ist | Felder aus dem Spiegel geklemmt (wie 2.2); fehlt `g`: aus `mark.tamedAt`. **Nur MP:** `g <= (now - tamedAt) / (D x 24) + feedGrowMax` (ein gefaelschter Spiegel macht keinen fertigen Baeren; PB1C F1). `hp` bleibt nil -> erster Abgleich holt das Leben aus dem Koerper |
| `"newer"` | `B.TakeNewerMark` (`Heal.lua:289-358`, nur SP), direkt VOR `B.Touch(rec)` | `g` und `x*` = max(Register, Spiegel) (nie schrumpfen); `gF/gFd/gFn` aus dem Spiegel |

### 2.5 Konflikte (Regeln von B1c bleiben; was B1d dazu bedeutet)
| Fall | Ergebnis fuer Wachstum/Werte |
|---|---|
| Register leer, Tier mit Spiegel (Kevins N9) | `g`, `x*` aus dem Spiegel, Leben aus dem Koerper -> gleicher Tag, gleiche Groesse (nach dem naechsten Hirn-Takt) |
| Zwei Tiere, ein Eintrag (gleiches `u`) | gebunden wird nach B1c (`gen` absteigend, `r` absteigend); die Werte stehen im EINTRAG, die verworfene Kopie nimmt ihr `g` mit (verfaellt) |
| Eintrag lebt, fremdes Tier traegt seinen Spiegel (MP-Faelschung) | B1c: das Register gewinnt (`u`, `gen`, AnimalID); das fremde Tier bekommt keine Groessen-Probe (nicht gebunden) |
| Spiegel neuer als Register (SP, Absturz) | `B.TakeNewerMark` -> `"newer"`: max |
| MP-Spiegel mit hohem `g`/`x*` ohne Register | `g` gedeckelt (2.4); `x*` nicht pruefbar (bis 2133) -- wie PB1C F1 ehrlich offen, F1 hier |
| B1c-Spiegel ohne B1d-Felder | `g` aus `tamedAt`, `x*` = 0 |

---

## 3. Mitfahren, Call to me, Unstuck mit B1d

### 3.1 Zustandsmaschine (B1c, unveraendert) und was B1d je Kante tut
```
 follow (Koerper)  --[Einsteigen]--> riding (kein Koerper)    B1d: g, hp im Register; Ausdauer/Kondition stehen (kein GrowLive)
 riding            --[Langsam-Takt]-> riding                  B1d: g waechst, hp heilt (nur Register), Besitzer online
 riding            --[Aussteigen / Besitzer tot]--> follow / stay (neuer Koerper, gen+1)
                                                               B1d: B.PlaceCub -> B.GrowBody: setSizeForced(sz) + setHealth(hp) SOFORT
 tame/missing      --[Call to me]--> follow (neuer Koerper, gen+1)   B1d: wie Aussteigen
```
`B.GrowBody(rec, a)` steht in `B.PlaceCub` direkt nach `B.WriteMark(rec, a)` (`S:server/BanditsNPCBearRide.lua:83-85`): `B.ApplySize(a, sz)`,
`B.BodyHp(rec, a, 0)` (der neue Koerper hat 1,0 > `hpB` -> gilt als Engine-Heilung -> wird auf `rec.hp` gesetzt; fehlt `hp`: 1,0 uebernehmen),
`s.kx/ky/kAt/kAcc = nil`. Ob `setSizeForced` direkt nach `addToWorld` im selben Bild wirkt: ungeprueft -- der naechste Hirn-Takt setzt sicher nach.

### 3.2 Was verloren geht und warum das ok ist
Beim Neu-Erzeugen verliert der Koerper (B1c-Liste PB1C 3.2) zusaetzlich Engine-Groesse (neu 0,35) und Engine-Leben (neu 1,0) -- beides kommt
SOFORT aus dem Register zurueck (3.1), sonst heilte jede Autofahrt voll (FD 0.8). Verloren bleiben: die Sitzungs-Ausdauer bei Call to me nicht
(sie haengt am Eintrag, nicht am Koerper), die Eimer nicht. Nichts davon ist ein Gegenstand.

### 3.3 Sonderfaelle
| Fall | B1d-Verhalten |
|---|---|
| Speichern waehrend der Fahrt | `g`, `hp` im Register; nach dem Laden waechst/heilt es weiter, beim Aussteigen gilt 3.1 |
| Besitzer stirbt im Auto | Aussteigen "dead" (B1c) -> `B.GrowBody`; danach steht die Uhr (Besitzer nicht in `B.Players()`), bis die neue Figur da ist (SP gleicher Schluessel `__sp`) |
| Absturz, Register aelter als Zelle | B1c-Regeln (`gen`); SP: `"newer"` = max; das stuendliche Commit begrenzt den Verlust auf <= 1 Spielstunde |
| Absturz, Zelle aelter als Register | Register gewinnt; der Koerper bekommt im naechsten Hirn-Takt Groesse/Leben aus dem Register |
| Call to me, altes Tier nicht geladen | neues Tier gen+1 mit Groesse/Leben aus dem Register; das alte ist "stale" (B1c) |
| Vermisst | keine Uhr (0.9); nach "Your bear is back." geht es weiter |

---

## 4. Anzeige: Daten aus der Sicht, Kosten je Bild, Deckel, Riegel

### 4.1 Sicht (KERN liefert ueber `B.GrowView(rec, t)` aus `viewEntry`, OBERFLAECHE liest; nur `st == "tame"`)
| Feld | Typ | Bedeutung |
|---|---|---|
| `sz` | Zahl, 3 Nachkommastellen | gezeigte Groesse (Client-Probe 0.4, Schild-Anker) |
| `hp` | ganze Zahl 0..100 oder fehlt | Leben in Prozent (fehlt, solange `rec.hp` nil) |
| `hpMax` | ganze Zahl | Leben-Hoechstwert in Punkten (mit Leben-Bonus) |
| `sta` | ganze Zahl 0..100 | Ausdauer in Prozent (Sitzung; ohne Sitzung 100) |
| `staMax` | ganze Zahl | Ausdauer-Hoechstwert (mit Kondition) |
| `day` | ganze Zahl | Wachstumstag `floor(g x D + 0,000001)` |
| `stg` | Text `cub`/`half`/`strong`/`adult` | Stufe jetzt |
| `nst` | Text `half`/`strong`/`adult` oder fehlt | naechste Stufe (fehlt = ausgewachsen) |
| `nxt` | ganze Zahl >= 1 oder fehlt | Tage bis `nst` (aufgerundet) |
`B.ApplySync` kopiert flache Felder von selbst (`copyFlat`, `S:shared/BanditsNPCBear.lua:402-408`). Keine Kollision mit den B1a-B1c-Feldern.

### 4.2 Kosten und Deckel
| Teil | je Bild | seltener | Deckel |
|---|---|---|---|
| Groessen-Probe Schreiber | - | je Hirn-Takt und zahmem Jungen 2 Java-Aufrufe (+1 bei Abweichung) | `B.CFG.maxRecs` 64, real `BearMaxPerPlayer` je Spieler |
| Leben-Abgleich | - | je Langsam-Takt und zahmem geladenem Jungen 1 `getHealth` (+1 `setHealth` bei Aenderung) | wie oben |
| Ausdauer/Kondition | - | je Hirn-Takt reine Lua-Rechnung (`B.StatsOf`) | Eimer je Faehigkeit |
| Sicht | - | Commit <= 1 je Spielstunde + Ereignisse; Ausdauer >= 5 s und >= 10 Punkte, nur Besitzer | - |
| Client-Probe (nur MP) | - | im Listenbau <= 1 x/s je Junges der Sicht mit Objekt 2 Java-Aufrufe | `viewMax` 16 |
| Schild-Zeilen | je zahmem Jungen bis 2 Balken (je 3 Zeichenaufrufe) + bis 4 Textzeilen (je 2 `drawTextCentre`) = <= 14 | Texte und Fuellbreiten im Listenbau | `hudMax` 6 -> <= 84 Zeichenaufrufe je Bild |
| Optionen | - | `U.Opt` im Listenbau (Zwischenspeicher 1 s) | 6 Ids |
Kein `getText`/`U.T`, keine Tabelle, kein `B.StatsOf` je Bild.

### 4.3 Riegel
- Bandits: B1d braucht nichts von Bandits. Bildschirm-Markierung (wildes Junges, Bandits-Riegel B1c) und Karten-Symbol (feste Pixel,
  waechst nicht mit) bleiben unveraendert; sie lesen keines der neuen Felder.
- NPC Crew: nichts Neues; `B.Opt` geht wie bisher ueber `BanditsNPC.Opt`, wenn da.
- Optionen: `PZAPI.ModOptions` wie B1c (Riegel, KEIN pcall um das Anlegen). `addComboBox`/`addItem` nur mit Schluesseln (Uebernahme-Regel
  `MO_TEXT_ARGS`, `baer/tools/baer_uebernahme.py`).
- `B.ApplySize`/`B.StatsOf` fehlen (Datei nicht geladen): Hud zeichnet ohne Probe und ohne Werte-Zeilen; Kern ruft alles ueber `if B.X then`.
- Fehler beim Zeichnen: kein neues pcall (B1c-Regel: nur um belegte Aufrufe und nie stumm).

---

## 5. Stellwerte und Sandbox

### 5.1 Sandbox (Seite `BanditsNPC`; KERN `B.OPTS`, OBERFLAECHE `sandbox-options.txt` + `Sandbox.json` x 7; Zahlen TEXTGLEICH)
| Name | Typ | min | max | Vorgabe | Bedeutung / Quelle |
|---|---|---|---|---|---|
| `BanditsNPC.BearGrowDays` | integer | 10 | 365 | **100** | Spieltage vom Zaehmen bis ausgewachsen (**Kevin**) |
| `BanditsNPC.BearDodgeMax` | integer | 5 | 80 | **40** | Ausweichen in Prozent auf Agilitaet 10 (**Kevin**: Hoechstwert als Sandbox) |
| `BanditsNPC.BearFightBonusMax` | integer | 0 | 200 | **70** | Mehr-Schaden in Prozent auf Kaempfen 10 (**Kevin**) |
| `BanditsNPC.BearHealAwake` | double | 0.0 | 10.0 | **1.0** | Prozent des Lebens je Spielstunde, wach (**Kevin** ~1 %) |
| `BanditsNPC.BearHealSleep` | double | 0.0 | 100.0 | **15.0** | Prozent je Spielstunde im Schlaf (**Kevin** ~15 %); wirkt erst mit dem Schlafen |
Reihenfolge in `sandbox-options.txt`: nach `BearCallCooldownMinutes`, vor `BearLog`. In `B.OPTS` die Doubles GENAU so schreiben:
`BearHealAwake = { def = 1.0, min = 0.0, max = 10.0 }`, `BearHealSleep = { def = 15.0, min = 0.0, max = 100.0 }` (das Uebernahme-Skript vergleicht
den Text, `baer_uebernahme.py:870`, `:930-937`). `type = double` ist in NPC Crew gespielt (`NC/42/media/sandbox-options.txt:14`). Namen frei
(grep NPC Crew `42/media` nach `BearGrow|BearDodge|BearFight|BearHeal|BearStats|BearStage|BearSkill|UI_BN_Bear|BanditsNPCBear`: nur
`UI_BN_Beard_None`, kein Treffer, 11.11.). Prozentzeichen in Sandbox-Texten nur als Wort "percent" oder `%%` (Vanilla `Sandbox.json:169`).

### 5.2 `B.CFG` neu (KERN `shared/BanditsNPCBear.lua`; flache Werte zur Laufzeit per `NCBear_CubSet`)
| Feld | Vorgabe | Bedeutung |
|---|---|---|
| `growCurve` | `{ {0, 0.35}, {0.15, 0.75}, {0.45, 1.0}, {1.0, 1.35} }` | Kurve (x = g, Groesse) -- Tabelle, nicht per CubSet |
| `stageAt` | `{ 0.75, 1.0, 1.35 }` | Schwellen half / strong / adult (innere Groesse) -- Tabelle |
| `cubMaxSize` / `bodySwap` / `sizeEps` / `tagBase` | 0.75 / false / 0.002 / 0.35 | groesste gezeigte Groesse mit dem Junges-Modell / Tausch (aus) / Probe-Schwelle / Bezug des Schild-Ankers (OBERFLAECHE liest) |
| `growCommitH` | 1.0 | Wachstum festschreiben hoechstens je (Spielstunden) |
| `feedGrowFav` / `feedGrowOk` / `feedGrowSnack` / `feedGrowDay` / `feedGrowMax` | 3 / 2 / 1 / 2 / 0.10 | Fuetter-Bonus (Spielstunden je Fuetterung, je Tag, Summe als Anteil) |
| `statAt` / `hpAt` / `staAt` / `carryAt` / `dmgAt` | `{0.35, 0.75, 1.35}` / `{40, 150, 400}` / `{50, 100, 160}` / `{10, 40, 100}` / `{0, 0.35, 1.0}` | Stuetzwerte der Werte (0.6) -- Tabellen |
| `vitPerLv` / `conPerLv` / `dodgeBase` | 0.05 / 0.05 / 5 | Leben-/Ausdauer-Bonus je Stufe / Ausweichen auf Stufe 0 (%) |
| `fishBase` / `fishMax` / `noseBase` / `noseStep` | 10 / 60 / 12 / 1.5 | Fang-Chance % / Warnweite Kacheln |
| `xpNeed` | `{100, 116, 135, 156, 181, 210, 244, 283, 328, 380}` | Bedarf je Stufe -- Tabelle |
| `xpPerMin` / `xpBucketMin` | 6 / 3 | Echtzeit-Deckel je Faehigkeit / Minuten ansparen |
| `xpHitTaken` / `xpHitDealt` / `xpFishTry` / `xpFishCatch` / `xpSniff` | 10 / 5 / 2 / 10 / 5 | Erfahrung je Ereignis (Haken) |
| `conTilesPerXp` / `conBreathXp` / `conBreathMs` / `conStepMax` | 5 / 5 / 60000 / 8 | Kondition: Kacheln je XP / ausser Puste / Abklingzeit / groesster Weg je Takt |
| `staRunCost` / `staRegen` / `staViewStep` | 0.4 / 2 / 10 | Ausdauer: Punkte je Kachel Rennen / Punkte je s Erholung / Sicht ab Aenderung |
| `hpEps` / `hpCommit` | 0.005 / 0.02 | Leben: Abgleich-Schwelle / sofort festschreiben ab Verlust |
Die OBERFLAECHE liest `tagBase`, `tagZ` mit eigenem Rueckfall (`tonumber(B.CFG.x) or Vorgabe`).

---

## 6. GENAUE SCHNITTSTELLE (WOERTLICH einhalten; Abweichung sofort nach `schnittstelle_aenderungen.md`, Abschnitt "B1d KERN" / "B1d OBERFLAECHE")

### 6.1 Wer schreibt welche Datei (Lua unter `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | Bauer | Was |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | KERN | `B.CFG` (5.2), `B.OPTS` (5.1) |
| `lua/shared/BanditsNPCBearDefs.lua` | KERN | `maxSize = 1.35`, `stages[CUB] = { ageToGrow = 36500 }`, Kommentar (0.3, F1) |
| `lua/shared/BanditsNPCBearStats.lua` (**neu**) | KERN | reine Formeln 6.2 + `B.ApplySize` (einzige Engine-Stelle der Datei) |
| `lua/server/BanditsNPCBearGrow.lua` (**neu**) | KERN | Takte und Register-Seite 6.3 (`B.GrowFix`, `B.GrowSlow`, `B.GrowLive`, `B.GrowBody`, `B.GrowFeed`, `B.GrowFromMark`, `B.GrowView`, `B.BodyHp`, `B.SkillAdd`, `B.SkillSet`, `B.GrowSetG`, `B.GrowSetHp`, Haken) |
| `lua/server/BanditsNPCBearServer.lua` | KERN | drei Haken-Zeilen (6.4) |
| `lua/server/BanditsNPCBearRegistry.lua` | KERN | `B.GrowFix` in `B.InitRegistry`, `B.GrowView` in `viewEntry` (6.4) |
| `lua/server/BanditsNPCBearHeal.lua` | KERN | `MARK_FIELDS`, zwei Haken (6.4) |
| `lua/server/BanditsNPCBearRide.lua` | KERN | `B.GrowBody` in `B.PlaceCub` (6.4) |
| `attrappe/kern/attrappen.lua`, `attrappe/b1d_kern/run.lua` (**neu**) | KERN | Tier-Attrappe + Tests 7.1 |
| `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `U.EN` (wortgleich EN), `U.NoteText` Typen `"stage"`/`"skill"`, `U.StageName(key)` |
| `lua/client/BanditsNPCBearOptions.lua` | OBERFLAECHE | `TagHealth`, `TagStamina`, `TagAge` (6.8) |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | Werte-Zeilen, Anker x Groesse, MP-Client-Probe (6.6) |
| `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | Bench 1.7 -- wird nie kopiert |
| `lua/shared/Translate/<L>/UI.json` x 7 | OBERFLAECHE | 24 neue Schluessel (6.7) |
| `lua/shared/Translate/<L>/Sandbox.json` x 7 | OBERFLAECHE | 5 Optionen + `_tooltip` |
| `sandbox-options.txt` | OBERFLAECHE | 5 Bloecke (5.1) |
| `ober_werkzeug/texte_b1d.py` (**neu**, auf `texte_b1c.py`), `attrappe/b1d_ober/` (**neu**: `run.lua`, `texte_pruefen_b1d.py`) | OBERFLAECHE | Texte erzeugen/pruefen, Tests 7.2 |
| `staging_dateien.txt`, `attrappe/gesamt/` (Abschnitt "19 B1d", `xref_b1d.py`), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt` | ZUSAMMENBAU | 10 |
Unveraendert: `shared/BanditsNPCBearRules.lua`, `...Food.lua`, `...Crew.lua`, `shared/TimedActions/*`, `server/...Follow/Guard/World.lua`,
`client/BanditsNPCBearMenu.lua`, `client/ISUI/...Map/Marker/NameBox.lua`, `IG_UI.json` x 7, Modell, Textur, Skript, `ui/BanditsNPCBearCub_marker.png`.
Kopf jeder neuen Lua-Datei wie PZ 6.1; `server/`-Datei beginnt mit `if isClient() then return end`. Ladefolge: shared `...Bear < Crew < Defs
< Food < Rules < Stats`; server `Follow < Grow < Guard < Heal < Registry < Ride < Server < World` -> auf Dateiebene nichts Fremdes einfangen.
Lua-Dateien LF, ASCII; kein `next(`, kein `%a`, keine Namen/Texte mit spawn/debug/test/bench/cheat ausser in der Bench.

### 6.2 `shared/BanditsNPCBearStats.lua` (KERN; rein bis auf `B.ApplySize`; auch der Client darf rufen)
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.SKILLS` | `{ "agi", "vit", "con", "fgt", "fsh", "nos" }` | Reihenfolge fest |
| `B.SKILL_FIELD` | `{ agi = "xAgi", vit = "xVit", con = "xCon", fgt = "xFgt", fsh = "xFsh", nos = "xNos" }` | |
| `B.XP_CUM` | `{ [0] = 0, 100, 216, 351, 507, 688, 898, 1142, 1425, 1753, 2133 }` | aus `B.CFG.xpNeed` beim Laden gerechnet; `B.XpCum(L)` liest neu, falls `xpNeed` geaendert wurde |
| `B.GrowDays()` | Zahl D | `B.Opt("BearGrowDays")` |
| `B.GrowSize(g)` | innere Groesse s | stueckweise gerade ueber `B.CFG.growCurve`; g nil/unsinnig -> 0; geklemmt 0..1 |
| `B.GrowXAt(s)` | x oder nil | Umkehrung (s ausserhalb der Kurve -> nil) |
| `B.StageOf(s)` | `"cub"`/`"half"`/`"strong"`/`"adult"` | Schwellen `B.CFG.stageAt` mit 0,000001 Spiel |
| `B.NextStage(s)` | key, s-Schwelle oder nil | |
| `B.BodyOf(rec)` | `"cub"`, sz | 0.10; sz = `min(s, cubMaxSize)` auf 3 Nachkommastellen |
| `B.GrowDay(rec)` | ganze Zahl | `floor(g x D + 0.000001)` |
| `B.SkillXp(rec, key)` | Zahl 0..`CUM[10]` | fehlt/unsinnig -> 0 |
| `B.SkillLevel(rec, key)` | 0..10 | groesstes L mit `xp >= CUM[L]` |
| `B.SkillProgress(rec, key)` | L, xpIn, need | Stufe 10: need = 0 |
| `B.StatsOf(rec)` | Tabelle | `{ g, day, s, sz, body, stage, next, nextDays, hpMax, staMax, carry, dmg, dodge, fightBonus, fish, nose, lv = { agi, vit, con, fgt, fsh, nos } }`; rein (liest `B.Opt`, `B.CFG`); neue Tabelle je Aufruf (nie je Bild rufen) |
| `B.HealRate(asleep)` | Prozent je Spielstunde | `asleep == true` -> `BearHealSleep`, sonst `BearHealAwake` |
| `B.ApplySize(a, sz)` | boolean (geschrieben) | nur `a ~= nil`, `type(sz) == "number"`, `sz > 0`; `local d = a:getData()`; `math.abs(d:getSize() - sz) > sizeEps` -> `d:setSizeForced(sz)`. **Einzige Stelle mit `setSizeForced`** |

### 6.3 `server/BanditsNPCBearGrow.lua` (KERN, neu)
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.GrowFix(rec, now, log)` | - | 2.2 |
| `B.GrowSlow(rec, dt, online, now, players)` | - | 1.1 Schritt 2: nur tame + `online[rec.owner] == true`; `B.GrowFix`; g; Stufe; `a = B.FindAnimal(rec)` (nil bei Fahrt/entladen); `B.BodyHp(rec, a, B.HealRate(false) / 100 x dt)`; Commit-Regel 0.11; Stufen-Meldung ueber `B.PlayerByKey(rec.owner, players)` + `B.Tell` |
| `B.GrowLive(rec, a, cx, cy, ms)` | - | 1.1 Schritt 3: `B.BodyOf` (bodySwap-Fehlerzeile 0.10), `B.ApplySize(a, sz)`; `rec.hp == nil` -> `B.BodyHp(rec, a, 0)`; Ausdauer/Kondition 0.8 (dt_s aus `s.kAt`, gedeckelt 10 s; Weg aus `s.kx/ky`, > `conStepMax` -> 0); Sicht-Drossel -> `B.Touch(nil, rec.owner)` |
| `B.GrowBody(rec, a)` | - | 3.1 (aus `B.PlaceCub`) |
| `B.GrowFeed(rec, class, now)` | Zahl (Zuwachs an g, 0 = keiner) | 1.1 Schritt 4; `class` "fav"/"ok"/"snack"; Spieltag = `floor(now / 24)` |
| `B.GrowFromMark(rec, mark, how)` | - | 2.4 |
| `B.GrowView(rec, t)` | - | 4.1; schreibt nur in `t`; nur `rec.st == "tame"` |
| `B.BodyHp(rec, a, add)` | Zahl (Verlust als Anteil, 0 = keiner) | 0.5; `a == nil` -> nur `rec.hp = min(1, hp + add)`. **Einzige Stelle mit `setHealth`**; `getHealth` nur hier und in `B.GrowLive` ueber diese Funktion |
| `B.SkillAdd(rec, key, xp, ms)` | gegeben, hochgestuft (boolean) | 1.4; Eimer in `B.Ses(id).xb[key] = { t, at }` (startet voll `xpPerMin x xpBucketMin`, fuellt `xpPerMin` je Echtzeit-Minute, Uhr rueckwaerts = voll); nur tame; Stufenaufstieg -> `B.Commit`, Meldung `{ k = "UI_BN_Bear_Note_SkillUp", t = "skill", v = key, w = L, tone = "good" }` |
| `B.SkillSet(rec, key, xp)` | neue Stufe | absolut, geklemmt, ohne Eimer, `B.Commit` (Bench) |
| `B.GrowSetG(rec, g, players)` | neues g | geklemmt 0..1, Stufen-Meldung nur aufwaerts, `B.Commit`, Groesse sofort (`B.FindAnimal` -> `B.ApplySize`) (Bench; spaeter V-Fenster/Spielmechanik) |
| `B.GrowSetHp(rec, frac)` | - | 0,01..1, `rec.hp = frac`, `B.BodyHp(rec, B.FindAnimal(rec), 0)`, `B.Commit` (Bench; spaeter Von-Hand-Heilen) |
| `B.OnHitTaken(rec, dmg, ms)`, `B.OnHitDealt(rec, ms)`, `B.OnFish(rec, caught, ms)`, `B.OnSniff(rec, ms)` | - | Haken 1.4.4, nur `B.SkillAdd`; `B.OnFish` nur ab Stufe half |
Neue Felder an `B` (Kern-intern, Bench darf lesen): keine globalen Tabellen -- alles in Register und `B._s[id]`.

### 6.4 Aenderungen in vorhandenen KERN-Dateien (genau diese Stellen)
| Stelle | Aenderung |
|---|---|
| `Server.lua` `slowTickBody` (`:574-579`) | nach `slowRec(...)`: `if B.GrowSlow and reg.cubs[rec.id] == rec then B.GrowSlow(rec, dt, online, now, players) end` |
| `Server.lua` `liveRec` (`:741`, nach `local cx, cy = ...`) | `if rec.st == "tame" and B.GrowLive then B.GrowLive(rec, a, cx, cy, ms) end` |
| `Server.lua` `B.FeedComplete` (vor dem `B.Commit(rec)` in `:242`) | `if wasTame and B.GrowFeed then B.GrowFeed(rec, class, now) end` |
| `Registry.lua` `B.InitRegistry` (nach der B1c-Schleife `:145-163`) | `if B.GrowFix then local now = B.Now() for _, rec in pairs(r.cubs) do B.GrowFix(rec, now, true) end end` |
| `Registry.lua` `viewEntry` (`:549-573`) | Tabelle erst in `local t = { ... }`, dann `if rec.st == "tame" and B.GrowView then B.GrowView(rec, t) end`, `return t` |
| `Heal.lua` `MARK_FIELDS` (`:38-41`) | + 10 Felder (2.3) |
| `Heal.lua` `B.Restore` (vor `B.InsertRec(rec, o)`, `:242`) | `if st == "tame" and B.GrowFromMark then B.GrowFromMark(rec, mark, "restore") end` |
| `Heal.lua` `B.TakeNewerMark` (vor `B.Touch(rec)`, `:356`) | `if st == "tame" and B.GrowFromMark then B.GrowFromMark(rec, mark, "newer") end` |
| `Ride.lua` `B.PlaceCub` (nach `B.WriteMark(rec, a)`, `:84`) | `if B.GrowBody then B.GrowBody(rec, a) end` |
| `BanditsNPCBear.lua` Kopf-Kommentar | B1d-Zeile |
Grenzen: localcount (aktiv und gesamt) unter 180 je Funktion bleibt (heute groesster Wert 77 in `World.lua:640`).

### 6.5 Meldungen (KERN schickt, OBERFLAECHE zeigt; `B.Tell` traegt das neue Feld `w` mit)
| Schluessel | t | v | w |
|---|---|---|---|
| `UI_BN_Bear_Note_Grown` | `"stage"` | `"half"`/`"strong"`/`"adult"` | - |
| `UI_BN_Bear_Note_SkillUp` | `"skill"` | `"agi"`/`"vit"`/`"con"`/`"fgt"`/`"fsh"`/`"nos"` | Stufe 1..10 |
`U.NoteText` (Client.lua): `t == "stage"` -> `U.T(k, U.StageName(v))`; `t == "skill"` -> `U.T(k, U.T("UI_BN_Bear_Skill_" .. SK[v]), math.floor(tonumber(note.w) or 0))`
mit fester Liste `SK = { agi = "Agi", vit = "Vit", con = "Con", fgt = "Fgt", fsh = "Fsh", nos = "Nos" }`; unbekannter Wert -> "?". `U.StageName(key)`:
`half`/`strong`/`adult` -> `U.T("UI_BN_Bear_Stage_Half"/"_Strong"/"_Adult")`, sonst "?".

### 6.6 OBERFLAECHE: Hud (`client/ISUI/BanditsNPCBearHud.lua`)
- `rebuild`: einmal je Liste `showTags = tagsWanted()`, `hpMode = U.Opt("TagHealth", 2)`, `staMode = U.Opt("TagStamina", 1)`, `showAge = U.Opt("TagAge",
  true) ~= false` (Zahl 1..3 klemmen, sonst Vorgabe).
- Schritt 1 (Schleife ueber `cubs`): `if isClient() and B.ApplySize and c.st == "tame" and c.ride ~= true and type(c.sz) == "number" and alive(S.objs[id])
  then B.ApplySize(S.objs[id], c.sz) end` (0.4; im SP nie).
- Filter (`:363`): zahmes Junges nur, wenn `showTags or hpMode > 1 or staMode > 1 or showAge`.
- `describeTag`: `e.showName = showTags`; `e.ageLine` (nur `showAge` und `c.day ~= nil`: `c.nst ~= nil` -> `U.T("UI_BN_Bear_Tag_Age", c.day, U.StageName(c.nst),
  c.nxt or 1)`, sonst `U.T("UI_BN_Bear_Tag_AgeDone", c.day)`); Leben (nur `hpMode > 1` und `hp`/`hpMax` Zahlen): Balken `e.hpFill = floor(barW x hp / 100)`
  bzw. Text `U.T("UI_BN_Bear_Tag_Health", floor(hp x hpMax / 100 + 0.5), hpMax)`; Ausdauer ebenso mit `sta`/`staMax` und `Tag_Stamina`;
  `e.zk = (tonumber(c.sz) or base) / base` (base = `tonumber(B.CFG.tagBase) or 0.35`; wilde: 1).
- `draw`: `lift = tagZ x e.zk`; `drawTag` zeichnet von unten nach oben (1.6.2); Balken: `drawRect` Hintergrund, `drawRect` Fuellung, `drawRectBorder`
  (Fundstellen wie der Zaehm-Balken `:418-434`). Zeilenhoehe Balken `t.barH + t.gap2`, Textzeile `t.h2 + 1` (Schrift `t.f2`), Name `t.h1` (`t.f1`).
- Die Optionen-Seite fehlt -> Vorgaben (Leben Balken, Ausdauer aus, Alter an, Name an).

### 6.7 Texte (OBERFLAECHE schreibt alle sieben Sprachen; KERN benutzt nur `Note_Grown`, `Note_SkillUp`)
EN (Vorschlag): `UI_BN_Bear_Tag_Health` "Health %1/%2" - `Tag_Stamina` "Stamina %1/%2" - `Tag_Age` "Day %1 - %2 in %3 day(s)" - `Tag_AgeDone`
"Day %1 - full-grown" - `Stage_Half` "half-grown" - `Stage_Strong` "strong" (F6) - `Stage_Adult` "full-grown" - `Skill_Agi` "agility" -
`Skill_Vit` "toughness" - `Skill_Con` "endurance" - `Skill_Fgt` "fighting" - `Skill_Fsh` "fishing" - `Skill_Nos` "keen nose" (F15) -
`Note_Grown` "Your bear is %1 now." - `Note_SkillUp` "Your bear's %1 is now level %2." - `MO_Health` "Health above tamed bears" - `MO_HealthTip`
"Off, as a bar or as a number (now / most)." - `MO_Stamina` "Stamina above tamed bears" - `MO_StaminaTip` "Off, as a bar or as a number. Stamina drops
while a bear runs and comes back while it rests." - `MO_Age` "Age and growth above tamed bears" - `MO_AgeTip` "Growth day and when the next stage
comes." - `MO_Off` "Off" - `MO_Bar` "Bar" - `MO_Number` "Number". (24 Schluessel.)
Sandbox (EN-Vorschlag): `Sandbox_BanditsNPC_BearGrowDays` "Bear: days until fully grown" / `_tooltip` "In-game days from taming until a cub is
fully grown (size 1.35). It grows faster at first and slower later; good feeding speeds it up a little. Health, stamina, carrying capacity and damage
rise every day with its size." - `BearDodgeMax` "Bear: dodge chance at agility 10" / "In percent. Agility level 0 dodges 5 percent of hits, level 10
this much. Agility rises with every hit the bear takes." - `BearFightBonusMax` "Bear: extra damage at fighting 10" / "In percent, on top of the
damage from growing. Fighting rises with every hit the bear lands." - `BearHealAwake` "Bear: healing per hour while awake" / "Percent of its health a
tamed bear heals per in-game hour on its own while awake." - `BearHealSleep` "Bear: healing per hour while asleep" / "Percent of its health per
in-game hour while it sleeps. Has no effect until bears can sleep."
Regeln wie PB1C 6.7: alle sieben Dateien, gleiche Platzhalter, sortiert, Round-Trip `json.dumps(data, indent=4, ensure_ascii=False) + "\n"`,
UTF-8 ohne BOM, LF; CN nur Zeichen aus Vanilla-CN (`ober_werkzeug/texte_b1d.py`, Gegenprobe `--basis` byte-gleich mit dem Staging vor B1d);
`U.EN` wortgleich; keine Woerter spawn/debug/bench/cheat/test; Optionen bekommen SCHLUESSEL.

### 6.8 Mod-Optionen (OBERFLAECHE, `client/BanditsNPCBearOptions.lua`, auf Dateiebene im vorhandenen Riegel, KEIN pcall)
```
o:addTickBox("TagShow", ...)                                                      -- B1c, unveraendert
local hp = o:addComboBox("TagHealth", "UI_BN_Bear_MO_Health", "UI_BN_Bear_MO_HealthTip")
hp:addItem("UI_BN_Bear_MO_Off")  hp:addItem("UI_BN_Bear_MO_Bar", true)  hp:addItem("UI_BN_Bear_MO_Number")
local st = o:addComboBox("TagStamina", "UI_BN_Bear_MO_Stamina", "UI_BN_Bear_MO_StaminaTip")
st:addItem("UI_BN_Bear_MO_Off", true)  st:addItem("UI_BN_Bear_MO_Bar")  st:addItem("UI_BN_Bear_MO_Number")
o:addTickBox("TagAge", "UI_BN_Bear_MO_Age", true, "UI_BN_Bear_MO_AgeTip")
o:addSlider("TagSize", ...)                                                       -- B1c, unveraendert
```
`getValue` einer Auswahl = Index 1..3 (`V:client/PZAPI/ModOptions.lua:137`). Der Platzhalter-Kommentar von B1c wird ersetzt (Hunger, Durst,
Muedigkeit, DODGE bleiben als "spaeter" im Kommentar).

### 6.9 Was die OBERFLAECHE vom KERN ruft
`B.ApplySize`, `B.StatsOf`, `B.SkillProgress`, `B.SKILLS`, `B.SKILL_FIELD`, `B.GrowDays`, `B.GrowDay`, `B.CFG` (`tagBase`, `tagZ`), `B.View`
(`cubs[id].sz/hp/hpMax/sta/staMax/day/stg/nst/nxt`) und die B1c-Liste (PB1C 6.4); Bench zusaetzlich (nur SP) `B.Reg`, `B._s`, `B.FindAnimal`,
`B.GrowSetG`, `B.GrowSetHp`, `B.SkillSet`, `B.BrainTick`, `B.PushView`. An `B` legt die OBERFLAECHE nichts an (nur `U.StageName` unter `U`).

---

## 7. Tests

### 7.1 KERN-Attrappe (`attrappe/b1d_kern/run.lua`, neu; `kern/`, `b1b_kern/`, `b1c_kern/`, `gesamt/` muessen gruen bleiben; gewollt
geaenderte Erwartungen -- z. B. neue Sicht-Felder, `MARK_FIELDS` -- im Bericht einzeln begruenden)
Tier-Attrappe (`attrappe/kern/attrappen.lua`): `a:getData()` mit `getSize`, `setSizeForced` (Zaehler, letzte Zahl), `getMinSize`/`getMaxSize`
(0,35 / 1,35); `a:getHealth()`, `a:setHealth(n)` (Zaehler, Liste der Werte); neue Tiere Groesse 0,35, Leben 1,0.
1. **Kurve:** g 0 / 0,15 / 0,45 / 1 -> 0,35 / 0,75 / 1,0 / 1,35 (auf 1e-9); streng steigend in 1000 Schritten; g 0,075 -> 0,55; Umkehrung;
   g < 0 / > 1 / Text -> geklemmt.
2. **Tage:** D 100: Tag 15 -> 0,75, Tag 45 -> 1,0, Tag 100 -> 1,35; D 50: Tag 7,5 -> 0,75 (anteilig); D 365: Tag 54,75 -> 0,75; D-Wechsel 100 -> 200
   bei g 0,5: Groesse gleich, Tempo halb.
3. **Stufen:** g 0,12 -> cub, naechste half in 3 Tagen; g 0,15 -> half; g 0,45 -> strong; g 1 -> adult, `nst` fehlt.
4. **Werte:** an den Stufen Leben 40 / 150 / 400, Traglast 10 / 40 / 100, Ausdauer 50 / 100 / 160, Schaden 0 / 0,35 / 1,0; Tag 5 Leben 77; jeder
   Spieltag 0..100 hat ein groesseres `hpMax` und `carry` als der vorige.
5. **Faehigkeiten:** XP 0 -> 0; 99 -> 0; 100 -> 1; 2133 -> 10; 5000 -> geklemmt 2133; Fortschritt; Ausweichen 5 / 22,5 / 40 bei L 0 / 5 / 10;
   `BearDodgeMax` 80 -> 80; Kampf-Bonus 70 % bei L 10; Leben-Bonus +50 %, Kondition +50 %; Fischen 0 unter Halbstark.
6. **GrowSlow:** tame + Besitzer da -> `g += dt / 2400`; Besitzer weg -> gleich; missing -> gleich; shy/fed -> nie ein `g`; ride -> waechst; g <= 1;
   r + 1 hoechstens einmal je Spielstunde (6 Takte je 10 min -> 1 Commit); Stufenwechsel -> sofort Commit + genau eine `Note_Grown` (`t = "stage"`,
   `v = "half"`); Bench-Ruecksetzen (`B.GrowSetG` kleiner) -> keine Meldung.
7. **Migration:** B1c-Eintrag tame ohne `g`, `tamedAt` 48 h alt -> Tag 2, nur `B.Log`; `g = "x"` -> aus `tamedAt` + eine `B.Err`; wilder Eintrag ->
   alle B1d-Felder nil; `x*` fehlt -> 0; `hp = 0` -> nil.
8. **Groessen-Probe:** `GrowLive` am Tier 0,35 bei g 0,15 -> `setSizeForced(0.75)` genau einmal; naechster Takt -> kein Schreiben; g 0,6 -> weiter
   0,75 (cubMaxSize); Engine setzt auf 0,35 zurueck (Attrappe) -> naechster Takt wieder 0,75; wildes Junges -> nie; `bodySwap = true` -> "cub" + eine
   Fehlerzeile je 10 min; Kosten je Takt und Junges <= 2 Getter-Aufrufe ohne Schreiben.
9. **Leben:** Koerper 0,62, `hp`/`hpB` 0,60 -> Engine-Heilung zurueckgenommen (`setHealth(0.6x)`); Koerper 0,50 bei `hpB` 0,60 -> `hp` - 0,10 und
   sofort Commit; 10 Takte x 10 min -> + 1,67 %; nie `setHealth(0)`, nie > 1; totes Tier -> nichts; ohne Koerper -> nur `rec.hp`; nach "entladen"
   (hp 0,70, Koerper 0,60 = hpB) -> kein Schaden, gesetzt 0,70; `hp` nil -> aus dem Koerper.
10. **Fuetter-Bonus:** zahm + Lieblingsfutter -> g + 3/2400; drittes am selben Spieltag -> 0; neuer Tag -> wieder; Snack 1 h; Summe <= 0,10; g = 1 -> 0;
    wildes Junges -> `GrowFeed` nie gerufen.
11. **Kondition/Ausdauer:** eigener Rennbefehl (`walk = false`, `ownUntil > ms`) mit 2,5 Kacheln je Takt -> `sta` sinkt um 1,0 / 50 je Takt, XP 1 je
    5 Kacheln; Gehen (`walk = true`) -> keine XP, Erholung; Weg 12 Kacheln je Takt -> ignoriert; Eimer (startet VOLL mit `xpPerMin x xpBucketMin`
    = 18, fuellt 6 je Echtzeit-Minute nach): 500 Kacheln in 1 Echtzeit-Minute -> hoechstens 24 XP; ausser Puste -> +5, zweites Mal innerhalb 60 s -> 0;
    Stufenaufstieg bei 100 XP -> Commit + `Note_SkillUp` (`t = "skill"`, `v = "con"`, `w = 1`); Sicht-Touch nur an `rec.owner`, fruehestens je 5 s
    und ab 10 Punkten.
12. **Spiegel:** `B.MarkOf` traegt die 10 Felder (nur Zahlen); `B.Restore` mit `g` 0,3 / `xCon` 400 -> Eintrag 0,3 / 400; ohne `g` -> aus
    `mark.tamedAt`; MP: `g` 0,9 bei 2 Tagen seit `tamedAt` -> gedeckelt auf 0,02 + 0,10; `B.TakeNewerMark` (SP) -> max; `v` bleibt 2; B1c-Faelle
    (`b1c_kern` Abschnitt Heilung) unveraendert gruen.
13. **Mitfahren/Call:** `B.RideBoard` -> 6 Langsam-Takte -> g gewachsen, hp geheilt, keine Engine-Aufrufe; `B.PlaceCub` -> am neuen Tier genau
    `setSizeForced(sz)` und `setHealth(rec.hp)` (hp 0,55), `gen` + 1 wie B1c; Call to me ebenso; Tod-im-Auto ebenso.
14. **Sicht:** zahm -> `sz hp hpMax sta staMax day stg nst nxt` (Zahlen/Texte), wild -> keins davon; `hp` nil -> Feld fehlt; ausgewachsen -> `nst`/`nxt` fehlen.
15. **Speichern/Laden:** `A.load` -> `g`, `x*`, `hp`, `hpB` bleiben; Sitzung (Ausdauer, Eimer) neu; erster Hirn-Takt setzt Groesse.
16. **Tod:** `B.Close(rec, "dead")` -> Eintrag und Sitzung weg, keine Fehlerzeile von B1d.
17. **MP-Rundlauf:** Server + zwei Client-Attrappen (A Besitzer, B fremd): Server rechnet; A offline -> Uhr steht; Sicht von B traegt dieselben
    Werte fuer A's Junges; `B.FeedComplete` durch B -> `Why_NotOwner`, kein Bonus.
18. **Dateien:** `setSizeForced` nur in `B.ApplySize`, `setHealth`/`getHealth` nur in `B.BodyHp`, `getData` nur in `B.ApplySize`; kein `next(`,
    kein `%a`; LF, ASCII; `B.CreateCub(` weiter nur in `B.AppearFor`/`B.PlaceCub`.

### 7.2 OBERFLAECHE-Attrappe (`attrappe/b1d_ober/run.lua`, neu; eigene Kern-Attrappe nach 6.2-6.5, nicht auf den KERN warten; `ober/`,
`b1b_ober/`, `b1c_ober/` bleiben gruen, gewollte Aenderungen mit Kommentar "B1d")
1. **Optionen:** `addComboBox("TagHealth", Schluessel, Schluessel)` mit drei `addItem`-Schluesseln, Vorgabe-Index 2; `TagStamina` Vorgabe 1; `TagAge`
   TickBox true; Reihenfolge TagShow, TagHealth, TagStamina, TagAge, TagSize; `U.Opt("TagHealth", 2)` liefert den Index; Seite fehlt -> Vorgaben.
2. **Hud:** Sicht `hp 61, hpMax 150` + Balken -> Fuellung `floor(barW x 0.61)`; Zahl -> "Health 92/150"; Ausdauer aus -> keine Zeile; Alter: `day 12,
   nst half, nxt 3` -> "Day 12 - half-grown in 3 day(s)", ohne `nst` -> "Day 100 - full-grown"; `TagShow` aus + Leben Balken -> nur die Balken-Zeile,
   Eintrag gelistet; alles aus -> zahmes Junges nicht gelistet (zaehlt nicht gegen `hudMax`); wildes Junges -> Zaehm-Balken wie B1c; Anker `tagZ x sz /
   0.35` (sz 0,75 -> x 2,14); je Bild <= 14 Zeichenaufrufe je Schild, kein `U.T` je Bild.
3. **Client-Probe:** `isClient()` wahr -> `B.ApplySize(obj, c.sz)` je lebendem zahmem Objekt einmal je Listenbau; SP -> nie; `ride` -> nie; `sz` fehlt -> nie.
4. **Meldungen:** `{ k = Note_Grown, t = "stage", v = "half" }` -> "Your bear is half-grown now."; `t = "skill", v = "con", w = 3` -> "Your bear's endurance
   is now level 3."; unbekanntes `v` -> "?" (kein roher Schluessel).
5. **Texte:** 24 neue Schluessel in 7 Sprachen, Platzhalter gleich, CN-Zeichen, Round-Trip, `U.EN` == EN; Sandbox 10 Schluessel; `sandbox-options.txt`
   Bloecke == `B.OPTS` textgleich (auch die Doubles); Optionen-Argumente nur Schluessel (`mo_text_hits`).
6. **Bench:** neue Befehle im MP "singleplayer only"; `NCBear_CubGrow(15)` -> `B.GrowSetG(rec, g + 0.15)` bei D 100; `NCBear_CubGrow(-200)` -> 0;
   `NCBear_CubHurt(50)` -> `B.GrowSetHp(rec, 0.5)`; `NCBear_CubXp("xyz", 5)` -> Schluesselliste; zwoelf Menue-Eintraege; keine Bench-Funktion
   ausserhalb `NCBearBenchCub.lua`.

### 7.3 GESAMT (`attrappe/gesamt/run.lua` Abschnitt "19 B1d", ZUSAMMENBAU)
Junges -> gezaehmt -> Tag 0 (Sicht `day 0`, `sz 0.35`) -> 15 Spieltage Langsam-Takte (Besitzer da) -> `Note_Grown` half, `sz 0.75`, Engine-Groesse 0,75 ->
Fuettern (Bonus) -> Register leeren (Spiegel bleibt) -> Heilung -> gleicher Tag -> Einsteigen, 1 Tag Fahrt (waechst), Aussteigen -> neuer Koerper mit
Groesse und Leben -> Call to me -> gleich -> Rennen (Kondition +) -> Speichern/Laden -> gleich -> Tod -> Eintrag weg. Einmal SP, einmal Server + zwei
Clients. B1a-B1c-Faelle bleiben gruen; `xref_b1d.py`: jede `B.*`/`U.*`-Benutzung definiert, Sicht-Felder passen, jeder Schluessel in 7 Sprachen.

### 7.4 Kevins Test im Spiel (nach dem Einbau: Spiel NEU starten; `bugwatch.py` mitlaufen lassen; Wegwerf-Spielstand, `-debug`; Debug-"Tier
Cheat" AUS; `NCBear_CubLog(true)` fuer die Diagnose)
Einzelspieler:
1. Spielstand mit gezaehmtem Jungen laden (sonst `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`). `NCBear_CubStats()`. Erwartet:
   Tag = Spieltage seit dem Zaehmen, Groesse 0,35 (bzw. gewachsen), Leben x/40, Traglast 10.
2. Optionen -> Mods -> "NPC Crew: Bear": Leben = Balken (Vorgabe) -> roter Balken ueber dem Jungen; Leben = Zahl -> "Health 40/40"; Ausdauer = Balken;
   Alter an -> "Day 0 - half-grown in 15 day(s)". Namensschilder aus -> Balken bleiben. Melden: Reihenfolge und Groesse ok?
3. `NCBear_CubGrow(5)`: sichtbar groesser, "Day 5 - half-grown in 10 day(s)", Leben 77. `NCBear_CubGrow(10)`: Meldung "Your bear is half-grown now.",
   Groesse 0,75. **"Follow me", gehen und rennen: rutschen die Fuesse (F2)? Sitzt das Schild richtig ueber dem Kopf?**
4. `NCBear_CubGrow(30)`: "Your bear is strong now.", Bild bleibt 0,75, `NCBear_CubStats()` "inner 1.0 / shown 0.75", Leben 254. `NCBear_CubGrow(-45)`: zurueck.
5. Heilen: `NCBear_CubHurt(50)` -> Balken halb; eine Spielstunde warten -> 51 % (nicht 52-53 %).
6. Kondition: "Follow me", 2 Minuten sprinten -> Ausdauer-Balken sinkt, nach dem Stehen steigt er; `NCBear_CubStats()` zeigt Kondition-XP; bei 100 XP
   Meldung "Your bear's endurance is now level 1."
7. Zahmes Junges mit Lieblingsfutter fuettern -> `NCBear_CubStats()` Fuetter-Bonus 3 h.
8. Speichern, Hauptmenue, laden: gleiche Groesse (hoechstens 2-3 s klein), gleiche Werte.
9. Verletzt (`NCBear_CubHurt(60)`) und gewachsen ins Auto, fahren, aussteigen: gleiche Groesse, Leben 60 % (nicht 100 %). "Call to me": ebenso.
10. `NCBear_CubForget()`: nach der Heilung gleicher Tag, gleiche Erfahrung (`NCBear_CubStats()`).
11. Wildes Junges (`NCBear_CubClean()`, `NCBear_CubHere(12)`): waechst nicht, keine Werte-Zeilen, Zaehm-Balken wie immer.
Mehrspieler (dedizierter Server, Rolle user, Spieler A und B; Sandbox "Bear: days until fully grown" = 10, kurze Tageslaenge, Abklingzeiten 0):
1. Server startet ohne Fehler, beide verbinden, kein Kick.
2. A zaehmt (Sandbox schnell): nach ~1,5 Spieltagen "Your bear is half-grown now." bei A; A UND B sehen das Junge wachsen.
3. B kommt erst spaeter in die Naehe: sieht sofort die richtige Groesse (Weg B).
4. A meldet sich ab: das Junge bleibt gleich gross; A meldet sich an: es waechst weiter.
5. B sieht ueber A's Jungem dieselben Zeilen (Leben, Alter), wenn B sie eingeschaltet hat. B kann es nicht fuettern.
6. A faehrt mit dem Jungen: beide sehen es mit gleicher Groesse aussteigen.
7. Server-Log nach `[TC-BEAR] ***` durchsehen (Testpunkt: `getHealth` am Tier am Server, Abschnitt 8 Nr. 4).

---

## 8. Belege: jeder geplante Engine-Aufruf (aus `forschung_b1d.md`, nachgelesen 11.11.; der Bauer liest die Stelle selbst und nennt sie im Kommentar)
| Nr | Aufruf | Beleg (gleiche Argumenttypen) | Seite | Wer |
|---|---|---|---|---|
| 1 | `animal:getData()` | `V:shared/Definitions/animal/ButcheringUtil.lua:566`, `:569`, `:586`; Client `V:client/ISUI/Animal/ISAnimalUI.lua:31` | beide | KERN |
| 2 | `animal:getData():setSizeForced(Zahl)` | `ButcheringUtil.lua:569`, `:571` (`createAnimalForHook`, Client ueber `V:client/ISUI/Animal/ISButcherHookUI.lua:520` -> `ButcheringUtil.lua:535`); `:586` (`onRemoveCorpseFromHook`; Server `:673-674` `isServer()`, `V:shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70`; Client `ISButcherHookUI.lua:530`). Grenzfall: Vanilla nur an Haken-Tieren; am lebenden Tier nur `T:client/NCBearSize.lua:27` (ob gespielt: ungeprueft) | SP, Server, Client | KERN (`B.ApplySize`) |
| 3 | `animal:getData():getSize()` | `ButcheringUtil.lua:570`; `ISAnimalUI.lua:31`; `V:shared/TimedActions/Animals/ISPetAnimal.lua:28` | beide | KERN, Bench |
| 4 | `animal:getHealth()` | am Tier: `V:client/ISUI/Animal/ISAnimalUI.lua:15` (Client); im SP gespielt `T:client/NCBearAttackProbe.lua:104` (ENT:60). Am Server dieselbe geerbte Methode an `IsoZombie`: `B:server/BanditSave.lua:52`, `B:server/BanditServerSync.lua:11` (Vererbung NUR JAR). **Am MP-Server am Tier ehrlich offen wie A3** -> MP-Test 7.4 MP 7 | SP + Server | KERN (`B.BodyHp`), Bench |
| 5 | `animal:setHealth(Zahl)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:545` (SP-Zweig), `V:server/ClientCommands.lua:932` (Server), `V:shared/TimedActions/Animals/ISKillAnimal.lua:58` -- Vanilla setzt nur 0; Werte 0..1 und "keine Klemme" nur aus dem Jar (`dec/IsoAnimal.java:1156-1163`, `dec_b1b/IsoGameCharacter.java:574`) | SP + Server | KERN (`B.BodyHp`) |
| 6 | `getGameTime():getWorldAgeHours()` (`B.Now`) | `V:server/Traps/STrapSystem.lua:77` (B1a) | Schreiber | KERN |
| 7 | `getTimestampMs()` (Eimer, Drosseln) | `V:server/Foraging/forageServer.lua:456`; Client `V:client/Foraging/ISBaseIcon.lua:485` | beide | beide |
| 8 | Takte: vorhandene `EveryTenMinutes` / `OnTick` (keine neuen Ereignisse) | `V:server/Traps/STrapSystem.lua:134`, `V:server/Foraging/forageServer.lua:502` (B1a) | Schreiber | KERN |
| 9 | `PZAPI.ModOptions` `addComboBox(id, name, tip)`, `option:addItem(key, wahl)`, `getValue()` | `V:client/PZAPI/ModOptions.lua:121`, `:131` (ruft `getText`), `:137`; gezeichnet `V:client/OptionScreens/MainOptions.lua:2910-2911` (`getText(option.name)`); NC gespielt `NC:client/BanditsNPCModOptions.lua:97-103`. Wie B1c A3: in Vanilla/Bandits kein Aufrufer, nur die Definition (Frage aus `gegen_bericht_b1c.md` 6.1 gilt mit) | Client | OBERFLAECHE |
| 10 | `addTickBox` (TagAge) | `V:client/PZAPI/ModOptions.lua:64-86` (wie B1c `TagShow`) | Client | OBERFLAECHE |
| 11 | `drawRect`, `drawRectBorder`, `drawTextCentre(..., UIFont.X)`, `isoToScreenX/Y(0, x, y, z)`, `getFontHeight` | wie B1b/B1c im Hud: `V:client/ISUI/ISUIElement.lua:1191`, `:1219`, `:1280`; `V:client/Fishing/TensionUI.lua:11-12`; Schriften `ISFitnessUI.lua:204`, `ISAlert.lua:35` | Client | OBERFLAECHE |
| 12 | `isClient()` (Client-Probe), `getSpecificPlayer(0)`, `HaloTextHelper.*` | wie B1a-B1c (`V:client/Farming/CFarmingSystem.lua:45`, `V:client/ServerCommands.lua:183`) | Client | OBERFLAECHE |
| 13 | Bench: `p:Say`, `B.FindAnimal(rec):getData():getSize()`, `:getHealth()` | wie die vorhandene Bench (`V:client/Entity/ISEntityUI.lua:458`) + Nr. 3 / 4 | Client (SP) | OBERFLAECHE |
| - | `math.floor/abs/min/max`, `tonumber`, `string.format("%d")`, Tabellen | Lua-Grundbibliothek | beide | beide |
**Nicht benutzt (auch nicht hinter pcall):** `getData():setSize` (Klemme), `setWeight` (wahlfrei laut FD 1.1, nicht noetig), Engine-Alter
(`setAgeDebug`, `getAge`, `checkStages`), `setIsInvincible` (Cheat-Pruefung), `healthLossMultiplier = 0` in der Definition (Weg B2, F5),
`getMaxSize/getMinSize` (Vanilla-Streichel-Haltung), `drawTextZoomed`, `transmitModData`. **Jar-only-Aufrufe in B1d: keine** (die zwei von Kevin
erlaubten -- `pathToLocation`, `setVariable("animalRunning", false)` -- benutzt B1d nicht neu; sie bleiben in `B.MoveTo`).

---

## 9. Leistung (Ergaenzung zu PB1C 9)
| Was | Wie oft | Deckel |
|---|---|---|
| Groessen-Probe (Schreiber) | je Hirn-Takt und geladenem zahmem Jungen 2 Java-Aufrufe, Schreiben nur bei Abweichung | Eintraege (64), praktisch `BearMaxPerPlayer` |
| Leben-Abgleich | je Langsam-Takt (10 Spielminuten) 1-2 Java-Aufrufe je geladenem zahmem Jungen | dito |
| Wachstum/Heilen ohne Koerper | je Langsam-Takt reine Rechnung | dito |
| Kondition/Ausdauer | je Hirn-Takt reine Rechnung, `B.StatsOf` einmal | Eimer 6 XP/min je Faehigkeit |
| Commit (Spiegel + Sicht) | <= 1 je Spielstunde je Junges + Ereignisse (Stufe, Aufstieg, Schaden) | - |
| Ausdauer-Sicht | <= 1 je 5 s je Junges, nur an den Besitzer | - |
| Client-Probe (MP) | <= 1 x/s je Junges der Sicht mit Objekt | 16 |
| Schild | <= 14 Zeichenaufrufe je zahmem Jungen und Bild | 6 Junge |

---

## 10. Fuer den ZUSAMMENBAU
- `staging_dateien.txt` neu (2 neue Lua-Dateien, geaenderte MD5; Bench als Testhilfe markiert).
- `attrappe/gesamt/run.lua` Abschnitt "19 B1d" (7.3; FILES-Liste um `shared/BanditsNPCBearStats.lua`, `server/BanditsNPCBearGrow.lua`), beide Bauer-
  Attrappen gegen die echten Dateien wiederholen; `xref_b1d.py` ueber die Grenze (6.9, Sicht-Felder 4.1, Meldungs-Typen 6.5, 24 + 10 Schluessel).
- `baer/tools/baer_uebernahme.py`, `TIER_RULES` erweitern (jedes Vorkommen des Namens im Code-Teil, wie die B1c-Regel `animalRunning`):
  `setSizeForced` nur `("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")`; `setHealth` und `getHealth` nur
  `("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp")` (Bench ausgenommen, wird nie kopiert). Neue Lua-Dateien deckt `LUA_BEAR`
  (`:95`); neue Sandbox-Optionen pruefen `plan_sandbox` (`:876-940`, Doubles textgleich). Cheat-Pruefung: Namen `GrowSetG`, `GrowSetHp`,
  `SkillSet` treffen kein Muster (`CHEAT_NAME`), sonst umbenennen. Trockenlauf mit `--vor-b5a`, Probe nur unter `_arbeit/baer_zaehmen/probe_b1d/`.
- `baer/NAEHTE.md`: keine neue Naht (kein Aufsatz, keine NPC-Crew-Zeile). Hinweis aufnehmen: NPC Crews Tierpflege (Naht 6, `BanditsNPCBearCrew.lua`)
  darf das Leben des Jungen nicht setzen -- bei der Uebernahme pruefen, ob NPC Crews Tier-Code `setHealth`/`setSizeForced` an fremden Tieren ruft (Lernen,
  kein Kopieren).
- `mod_info_vorschlag.txt` um B1d ergaenzen (Wachsen in 100 Tagen, Werte, Anzeige).
- Einbau in NCBearTest nur, wenn Kevin nicht spielt; vorher und nachher sichern; Kevin muss das Spiel neu starten (Definition und Lua laden nur beim Start).

---

## 11. Fragen fuer Kevin (Kevin schlaeft -- jede mit Empfehlung, nichts haelt den Bau auf; gebaut wird die Empfehlung)
1. **F1 Definition aendern** (`maxSize` 1,35, `ageToGrow` 36500), damit die Groesse Laden und Mehrspieler uebersteht? Empfehlung: ja (so gebaut).
2. **F2 Fussgleiten:** waechst das Junge-Modell bis 0,75, bleibt das Lauftempo gleich -- die Fuesse koennen rutschen. Bitte mit `NCBear_CubGrow(15)`
   ansehen. Empfehlung: ansehen, dann mit F11 zusammen entscheiden.
3. **F3 Zahlen:** Leben 40 / 150 / 400, Ausdauer 50 / 100 / 160, Schaden 0 / 0,35 / 1,0 als Vorgabe? Empfehlung: ja, im Test nachstellen.
4. **F4 Mehrspieler:** waechst (und heilt) der Baer, wenn sein Besitzer nicht eingeloggt ist? Empfehlung: nein (so gebaut, wie die Uhren in B1a).
5. **F5 Engine-Heilung:** das Spiel heilt das Junge selbst ~2 % je Stunde; B1d nimmt das zurueck, damit es bei deinen 1 % bleibt. Spaeter mit B5a
   lieber die Engine-Heilung in der Definition abschalten (dann koennen Spieler auch WILDE Junge nicht mehr verletzen)? Empfehlung: jetzt so, mit B5a fragen.
   *Nachbesserung B1d A4:* heute uebernimmt `B.BodyHp` JEDEN Verlust am Koerper (Spieler-Waffe, Auto/Anhaenger, anderes Tier) dauerhaft in `rec.hp` -- er ueberlebt Mitfahren, Call to me und Laden; laut ENT:45 sollen Spieler und Autos keinen Schaden machen. Mit B5a abschalten.
6. **F6 Name der Stufe bei 1,0** (Tag 45, "Biss, Umwerfen moeglich"): "kraeftig" / "strong"? Empfehlung: ja.
7. **F7 Fuetter-Bonus:** +3 Spielstunden je Fuetterung mit Lieblingsfutter (normal 2, Happen 1), hoechstens 2 je Tag, gesamt hoechstens 10 Tage
   frueher? Empfehlung: ja.
8. **F8 Wachsen beim Vermisstsein anhalten?** Empfehlung: ja (so gebaut).
9. **F9 Anzeige-Vorgaben:** Leben als Balken an, Ausdauer aus, Alter-Zeile an? Empfehlung: ja.
10. **F10 Bench zurueck** (`NCBear_CubGrow(-5)`)? Empfehlung: ja, nur Testhilfe.
11. **F11 Modellwechsel:** Junges- oder Erwachsenen-Modell fuer Halbstark? Bis dahin bleibt das Bild bei 0,75 stehen (Werte wachsen weiter).
    Empfehlung: nach deinem Blick in F2 entscheiden.
12. **F12 "Tag" in der Anzeige** ist der WACHSTUMSTAG (Fuettern zieht ihn vor, Vermisst/abgemeldet haelt ihn an), nicht die Kalendertage seit dem
    Zaehmen -- so passt "halbstark in 3 Tagen". Ok? Empfehlung: ja.
13. **F13 Ausdauer** sinkt nur, wenn der Baer RENNT (gemuetliches Gehen nicht), erholt sich im Stehen, und nach dem Laden ist sie voll. Ok? Empfehlung: ja.
14. **F14 Kondition-Tempo:** 1 Erfahrung je 5 Kacheln Rennen, +5 beim Ausser-Puste-Kommen, hoechstens 6 je Minute; Stufe 10 braucht 2133.
    Empfehlung: so lassen und nach ein paar Spieltagen mit `NCBear_CubStats()` nachsehen.
15. **F15 Namen der Faehigkeiten** in der Meldung: agility, toughness (Leben-Bonus), endurance (Kondition), fighting, fishing, keen nose. Ok? Empfehlung: ja.
16. **F16 Meldungen** "Your bear is half-grown now." und "Your bear's endurance is now level 3." -- gewuenscht oder zu viel? Empfehlung: lassen.
17. **F17 Fremde sehen** die Werte deines Baeren (Leben, Ausdauer, Alter), wenn sie die Zeilen einschalten (wie das Namensschild). Ok? Empfehlung: ja.
18. **F18 MP-Spiegel** (Erfahrung ist nach einem Server-Registerverlust aus dem Tier nicht pruefbar; Wachstum wird gedeckelt). Empfehlung: so lassen (wie B1c F1).
    *Nachbesserung B1d B1:* der Deckel rechnet mit `tamedAt`, das selbst aus dem Spiegel kommt; `B.Restore` klemmt es auf [0, jetzt] -- ein veraenderter Spiegel bekommt also hoechstens die Zeit seit Weltbeginn (in einer alten Welt kann das 'ausgewachsen' sein).

## 12. Offen / ungeprueft (Testpunkte)
`setSizeForced` an einem lebenden Tier in der Welt (Vanilla nur Haken-Tiere) -- sieht man den Wechsel, ruckt es, wirkt es direkt nach `addToWorld`;
Fussgleiten und Streichel-Haltung bei 0,5-0,75; Schild-Hoehe x Groesse; ob ein MP-Client seine `setSizeForced`-Kopie behaelt, bis er das Tier verliert;
Tierzone-Ruecksetzen in Kevins Basis; Engine-Heilung tatsaechlich 1,5-2,2 %/h (Gen); `setHealth` mit Werten zwischen 0 und 1 an einem lebenden Tier
(Vanilla setzt nur 0); `getHealth` am Tier am MP-Server (Nr. 4); ob `EveryTenMinutes` beim Schlafen/Vorspulen jede Stufe feuert (der Deckel 1 h je Schritt
kann Wachstum kosten, nie doppelt geben); wie viel Rennen in 100 Tagen zusammenkommt; geteilter Bildschirm im MP (seit der Nachbesserung B1d B6 laeuft die Client-Probe dort weiter, gezeichnet wird nichts; ohne Probe bleiben ein Junges ausserhalb der Sicht -- fremde ab 60 Kacheln -- und eine ausgeblendete Oberflaeche, ob prerender dann laeuft: ungeprueft); Vorspulen schneller als etwa x4 (Kondition zaehlt den Weg dann als Sprung, B4);
`addItem` ruft `getText` schon beim Laden der Datei (bei Sprachwechsel bleiben die Eintraege in der alten Sprache bis zum Neustart).

Statisch geplant, nichts gebaut, nichts gespielt.
