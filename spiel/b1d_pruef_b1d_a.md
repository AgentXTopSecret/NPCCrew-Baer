# Lauf baer-b1d: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme

Stand 11.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (51 Dateien laut
`staging_dateien.txt`: B1a + B1b + B1c + B1d KERN + OBERFLAECHE + Zusammenbau). Ich habe KEINE Datei im Staging, in der Test-Mod, in NPC Crew,
Vanilla oder Bandits geaendert; geschrieben nur dieser Bericht und Hilfsausgaben im Scratch-Ordner der Sitzung (Attrappen-Ausgaben, meine
Probe `probe/`, Trockenlaeufe, Gegenprobe mit TMP im Scratch). Kein git, kein Spielstart, kein Download.
Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/` (42.22.2), `B:` = Bandits `42.22/media/lua/`, `T:` = Test-Mod
`NCBearTest/42/media/lua/`, `NC:` = NPC Crew `42/media/lua/`, `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`.

## 0. Ergebnis

**Kein Blocker, kein major, 8 minor.** Alle Zahlen des Zusammenbaus habe ich selbst nachgefahren und bestaetigt (Tabelle 1). Jeder Engine-
Aufruf, den B1d neu benutzt, hat eine Fundstelle in Vanilla oder Bandits mit gleichem Empfaenger und gleichen Argumenttypen, im Kommentar
genannt und von mir in den heutigen Dateien nachgelesen (Tabelle 2). Jar-only: keiner (die zwei Ausnahmen mit Kevins Wort benutzt B1d nicht
neu). Kein pcall um einen neuen Aufruf. Keine Testbefehle ausserhalb der Bench, keine Namenskollision, Texte in sieben Sprachen sauber
(Paritaet, Platzhalter, Round-Trip, sortiert, CN-Zeichen), Sandbox-Optionen mit Texten und Benutzung, Uebernahme-Trockenlauf und Probe gruen.
Die Befunde sind Regel- und Freigabefragen und Ehrlichkeit im Bericht, kein Code-Fehler: Heilen laeuft schon vor Kevins B1c-Test (A1),
`getHealth` am MP-Server nur clientseitig belegt (A2, wie B1a A3), zwei Grenzfall-Belege ohne ausdrueckliche Kevin-Frage (A3), Spieler-Schaden
wird zur Wahrheit gegen ENT:45 (A4), Probe-Wege im kopierten Kern (A5), unsichtbare Auswahl-Tooltips (A6), `addComboBox` ohne Vanilla-Aufrufer
(A7), Kleinkram (A8).

## 1. Selbst laufen lassen (Zahlen)

| Pruefung | Ergebnis (mein Lauf 11.11.) | deckt sich mit Zusammenbau |
|---|---|---|
| `luacheck.py` (25 Lua des Stagings, 24 kopierte + Bench) | `25 file(s) checked, 0 failed` | ja |
| `scopecheck.py` (25) | `25 file(s), 0 violation(s)` | ja |
| `localcount.py` (25) | aktiv hoechstens 48 (`S:client/ISUI/BanditsNPCBearHud.lua` Dateiebene), dann 39 (Bench `:384`, Hud `:418`); B1d-Dateien: `Stats.lua:276` (`B.StatsOf`) 28; insgesamt hoechstens 77 (`S:server/BanditsNPCBearWorld.lua:640`, unveraendert), 59 (Hud), 51 (Server `:915`) -- weit unter 180/200 | ja |
| `luacheck_pz.py` (25) | 18 x W113, alle erwartet: 3 Aktionsklassen `S:client/BanditsNPCBearMenu.lua:86/97/107`, 15 in der Bench (`NCBear_*` :907-918, `NCBearMenu` :920-922) | ja |
| `luacheck_pz.py --unused` (11 geaenderte/neue Lua ohne Bench) | 3 Hinweise W212 `self` in `Hud.lua:647-649` (B1a, harmlos) | neu, harmlos |
| Dateiform (eigenes Skript ueber alle .lua/.json/.txt) | alle LF, kein BOM, Lua reines ASCII, jede JSON Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` und sortiert | ja |
| `staging_dateien.txt` gegen Platte und Test-Mod | 51/51 Zeilen: MD5, Bytes, neu/ueberschreibt/gleich stimmen (2 / 25 / 24), keine Datei ausserhalb der Liste | ja |
| `attrappe/kern/run.lua` | 136 / 0 (byte-gleich `ergebnis.txt`) | ja |
| `attrappe/b1b_kern/run.lua` | 204 / 0 (byte-gleich) | ja |
| `attrappe/b1c_kern/run.lua` | 192 / 0 (byte-gleich) | ja |
| `attrappe/b1d_kern/run.lua` | **147 / 0** (byte-gleich) | ja |
| `attrappe/gesamt/run.lua` | **1173 / 0** (byte-gleich `gesamt/ergebnis.txt`); einzige `***`-Zeilen die gewollten Heilungen 18c und 19f | ja |
| dieselbe gegen MEINE Probe (`<scratch>/probe/NPCCrew/42/media/lua/`) | 1173 / 0, byte-gleich `gesamt/ergebnis_probe.txt` | ja |
| `attrappe/pruef_b/run.lua` | byte-gleich `ergebnis_b1b_nach.txt` | ja |
| `attrappe/pruef_b1b/run_nach.lua` | byte-gleich `ergebnis_b1c.txt` (die drei BEFUND-Zeilen sind die gewollten Alt-Befunde) | ja |
| `attrappe/pruef_b1c/run.lua` | byte-gleich `ergebnis_nach.txt` | ja |
| `attrappe/ober`, `b1b_ober`, `b1c_ober`, `b1d_ober` (ohne / mit `kern`) | 116/0 + 117/0, 144/0 + 134/0, 193/0 + 180/0, **171/0 + 173/0** | ja |
| `texte_pruefen.py`, `_b1b`, `_b1c`, `_b1d --tmp <scratch>` | je `FEHLER gesamt: 0`; `texte_b1d.py` byte-gleich mit dem Staging, `--basis` == `texte_b1c.py` | ja |
| `belege.py`, `_b1b`, `_b1c`, `_b1d` | abweichend 0 von 112 / 51 / 89 / 23 | ja |
| `attrappe/gesamt/xref_b1d.py` | **0 Luecken, 3 Hinweise** (Rueckfallwerte Rules.lua, B1c Z3), byte-gleich `xref_b1d.txt` | ja |
| `attrappe/gesamt/gegenprobe_b1d.py` (TMP im Scratch) | **26 von 26 erkannt** (12 xref + 14 Gesamt), byte-gleich `gegenprobe_b1d.txt` | ja |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod --vor-b5a` | **OK, 0 Fehler, 26 Warnungen**, byte-gleich `trockenlauf_b1d_vor_b5a.txt`; Cheat-Funde 0; Tier-Regeln je an ihrem Ort (setSizeForced `Stats.lua:345`, getData `:342` -- B.ApplySize; setHealth `Grow.lua:237`, getHealth `:205` -- B.BodyHp; probeweg: kein Aufruf) | ja |
| Trockenlauf ohne `--vor-b5a` | 24 Fehler = genau die 24 Altlasten (`ALT_EXPECTED`); Ausgabe weicht von `trockenlauf_b1d.txt` nur in `NC shared/BanditsNPC.lua:1359` -> `:1360` ab (NPC Crew wird gerade weitergebaut, A8) | ja |
| Probe `--probe <scratch>/probe --staging ... --vor-b5a` | **OK, 0 Fehler, 26 Warnungen**; 51 Dateien geschrieben (24 Lua ohne Bench, 5 Modell/Textur/Skript/Knoten/Bild, 21 Texte, sandbox-options.txt); alle vier Lua-Pruefer je kopierter Datei gruen (Stats.lua hoechstens 32, Grow.lua 24), luacheck_pz 0 Treffer + 3 erlaubt; Texte UI.json 3812 -> 3945, Sandbox.json 92 -> 151, IG_UI.json neu 3; Ausgabe bis auf Pfade gleich `probe_b1d_ausgabe.txt` | ja |

## 2. Belege der in B1d neuen Engine-Aufrufe (selbst in den heutigen Dateien gelesen)

| Aufruf (Stelle) | Fundstelle (gelesen) | Typen / Seite | Urteil |
|---|---|---|---|
| `a:getData()` (`S:shared/BanditsNPCBearStats.lua:342`, Bench `:867`) | `V:shared/Definitions/animal/ButcheringUtil.lua:566`, `:569`, `:586`; Client `V:client/ISUI/Animal/ISAnimalUI.lua:31` | IsoAnimal, ohne Argument; Server `:586` ueber `:674` (isServer-Zweig), Client `ISAnimalUI` | belegt |
| `d:getSize()` (`Stats.lua:344`, Bench) | `ButcheringUtil.lua:570` (aus `ISPutAnimalOnHook.lua:88` in `complete`, Server), `ISAnimalUI.lua:31` (Client), `V:shared/TimedActions/Animals/ISPetAnimal.lua:28` | ohne Argument, beide Seiten | belegt |
| `d:setSizeForced(Zahl)` (`Stats.lua:345`) | `ButcheringUtil.lua:569`, `:571`, `:586`, `:242`; Client ueber `V:client/ISUI/Animal/ISButcherHookUI.lua:520`/`:530`, Server `:674` -> `:586`, `V:shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70` | Zahl, SP/Server/Client | belegt; Grenzfall lebendes Tier (A3) |
| `a:getHealth()` (`S:server/BanditsNPCBearGrow.lua:205`, Bench) | am Tier nur `V:client/ISUI/Animal/ISAnimalUI.lua:15` (Client); am Server nur am Zombie `B:server/BanditSave.lua:52`, `B:server/BanditServerSync.lua:11` | ohne Argument; **am MP-Server am Tier ohne Beleg** | A2 (wie B1a A3) |
| `a:setHealth(Zahl)` (`Grow.lua:237`) | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:545` (SP-Zweig), `V:server/ClientCommands.lua:932` (Server), `V:shared/TimedActions/Animals/ISKillAnimal.lua:58`; Zahl > 0 am Zombie `B:server/BanditServerSync.lua:12` | Zahl; Vanilla setzt am Tier nur 0 | belegt; Grenzfall Wert 0..1 (A3) |
| `a:isDead()` (`Grow.lua:201`) | `V:server/Traps/STrapGlobalObject.lua:238` | Server | belegt |
| `getTimestampMs()` (`Grow.lua:260`, `:398`) | `V:server/Foraging/forageServer.lua:456` | Server | belegt |
| `isClient()` (`S:client/ISUI/BanditsNPCBearHud.lua:441`, `Grow.lua:1`) | `V:client/ISUI/ISWorldObjectContextMenu.lua:1435`, `V:server/Traps/STrapSystem.lua:1` | Client / beide | belegt |
| `drawRect` / `drawRectBorder` (Hud `valueBar`) | `V:client/ISUI/ISUIElement.lua:1191` / `:1219` (Vanilla-Lua) | Client | belegt (wie B1a-Balken) |
| `addComboBox` / `addItem` / `getValue` (`S:client/BanditsNPCBearOptions.lua:65-73`) | Definition `V:client/PZAPI/ModOptions.lua:121-156` (`addItem` :131-136 ruft `getText` :132, `getValue` :137, gespeichert :272-273, geladen :319-320), gezeichnet `V:client/OptionScreens/MainOptions.lua:2910-2933` | reines Vanilla-Lua | A7 (Regelfrage) |
| `addTickBox("TagAge", ...)` | `V:client/PZAPI/ModOptions.lua:64-86`, gezeichnet `MainOptions.lua:2809-2813` | reines Vanilla-Lua | wie B1c A3 |
| Lua-Grundbibliothek: `math.ceil`, `string.format("%." .. d .. "f")`, `table.concat` | `V:client/BuildingObjects/TimedActions/ISBuildAction.lua:88`, `V:shared/env.lua:38`, `V:client/OptionScreens/ModSelector/ModSelectorModel.lua:354` | -- | ok (Kahlua kennt sie) |
| Definition `maxSize = 1.35`, `stages[CUB] = { ageToGrow = 36500 }` (`S:shared/BanditsNPCBearDefs.lua:73`, `:84`) | Felder belegt `V:shared/Definitions/animal/CowDefinitions.lua:136`, `:193` (Kommentar erklaert das Engine-Wachsen), `ChickenDefinitions.lua:8` | Daten, keine Methode | ok; Wirkung NUR JAR (Testpunkt) |

Kein `next(`, kein `%a`, kein `goto`, kein neuer `pcall` in den B1d-Zeilen. Der einzige pcall auf dem Weg ist der vorhandene um EIGENEN Code
(`S:server/BanditsNPCBearServer.lua:590`, `B.ErrEvery`, laut) -- keine Tarnkappe.

## 3. Befunde

### A1 (minor, Freigabe) -- Heilen laeuft schon vor Kevins B1c-Test
Kevin, Nachtschicht Punkt 4 (`ENT:279`): *"Wenn Zeit: Wachsen 100 Tage + taeglich steigende Werte (Plan + Bau); Kampf/Zombie-Angriffe/Heilen
erst nach Kevins B1c-Test."* B1d baut nicht nur die Formel, sondern schaltet die Selbstheilung wach ein (`B.GrowSlow` -> `B.BodyHp(rec, a,
B.HealRate(false) / 100 * dt)`, `S:server/BanditsNPCBearGrow.lua:440`) und **nimmt die Engine-Heilung zurueck** (`Grow.lua:223-224`, F5). Das
aendert das Spiel gegen den B1c-Stand: das Junge heilt etwa halb so schnell (Engine ~1,5-2,2 %/h laut NUR JAR `dec/AnimalData.java:377-398`
-> 1 %/h), und Schaden bleibt ueber Mitfahren/Call to me erhalten (vorher brachte jeder neue Koerper 1,0). Der Laufauftrag Punkt 5 verlangt
"nur wach anwenden, wenn ein belegter Leben-Weg existiert" -- der Bau folgt dem Auftrag; der Widerspruch zu Kevins Wort steht aber nirgends
als Frage (Zusammenbau 8 Nr. 4 fragt nur "so lassen?" zur Ruecknahme). Vorschlag: keine Code-Aenderung; im Bericht an Kevin ausdruecklich:
"Die langsame Selbstheilung (1 %/h, Spiel-Heilung zurueckgenommen) ist schon an, obwohl du Heilen erst nach deinem B1c-Test wolltest -- so
lassen?" (eine Abschaltung waere `BearHealAwake = 0`, dann heilt es GAR nicht -- das gehoert mit in die Frage).

### A2 (minor, Seite) -- `getHealth()` am Tier ist am MP-Server nicht belegt
`B.BodyHp` liest je Langsam-Takt `a:getHealth()` beim Schreiber (`Grow.lua:205`); im MP ist das der dedizierte Server. Am Tier gibt es den
Aufruf in Vanilla nur clientseitig (`V:client/ISUI/Animal/ISAnimalUI.lua:15`; grep `getHealth()` mit "animal" ueber ganz `V:` = 1 Treffer);
am Server nur am Zombie (`B:server/BanditSave.lua:52`, `B:server/BanditServerSync.lua:11`, Vererbung NUR JAR). Ehrlich benannt
(`Grow.lua:202-204`, PLAN_B1D.md 8 Nr. 4, Zusammenbau 7.2), gleiche Lage wie B1a A3 / B1c A2; Kevin: *"A3 entscheidet der MP-Test"*
(`ENT:285`). Im SP gilt der Client-Beleg (eine Maschine). Vorschlag: so lassen, MP-Test 7.4 MP 7 behalten; scheitert es, kommt es laut
("slow tick: ..." ueber `B.ErrEvery`).

### A3 (minor, Belege) -- zwei Grenzfall-Belege ohne ausdrueckliche Kevin-Frage
- `a:setHealth(hp)` mit 0 < hp <= 1 an einem LEBENDEN Tier: Vanilla ruft `setHealth` am Tier nur mit 0 (`ISAnimalContextMenu.lua:545`,
  `ClientCommands.lua:932`/`:950`, `ISKillAnimal.lua:58`). Typ gleich (Zahl) -- der Buchstabe der eisernen Regel ist erfuellt, die Wirkung
  eines Werts zwischen 0 und 1 nicht (NUR JAR `dec/IsoAnimal.java:1156-1163`).
- `getData():setSizeForced(Zahl)` an einem lebenden Tier in der Welt: Vanilla nur an Haken-Tieren und der Totgeburt (`ButcheringUtil.lua:242`,
  `:569`, `:571`, `:586`, `:713`, `:716`).
Der Auftrag Punkt 3 sagt woertlich *"Leben am Tier ueber einen belegten Weg setzen, falls es einen gibt (sonst nur fuehren und als Frage
melden)"*. Der Zusammenbau fuehrt beides nur als Testpunkte (7.1), nicht als Frage. Dazu eine Beleg-Verbesserung: der Kommentar
`S:shared/BanditsNPCBearStats.lua:337` sagt zu `T:client/NCBearSize.lua:27` "ob gespielt: ungeprueft" -- Kevins eigene Anleitung
`baer/spiel/anleitung_lebend.md:6` (`b:getData():setSizeForced(1.2)` am lebenden Erwachsenen), die Groessenfrage `begleiter/PLAN.md:297`
(`NCBear_Size`) und Kevins Antwort 1,35 (`ENT:10`) sowie `CLAUDE.md` Abschnitt 8 ("setSizeForced ... bezahlt") sprechen dafuer, dass es am
lebenden Tier gespielt ist. Vorschlag: eine Regel-Frage fuer Kevin ("`setHealth` mit Werten zwischen 0 und 1 und `setSizeForced` am lebenden
Tier gelten als belegt -- ok?"), den Kommentar um die Anleitung ergaenzen (Nachbesserung optional, kein Laufzeit-Risiko).

### A4 (minor, Kevins Vorgabe) -- Spieler- und Fahrzeug-Schaden wird zur Wahrheit (gegen ENT:45)
`ENT:45` (Plan-Vorgabe, von Kevin nicht widersprochen): *"Schaden nur von Zombies, Banditen, Hunger, Durst (nicht Spieler, nicht Autos)"*.
`B.BodyHp` uebernimmt JEDEN Verlust am Koerper in `rec.hp` (`Grow.lua:182-184`: "Spieler-Waffe, anderes Tier, Anhaenger"; `:219-222`), und
`rec.hp` ueberlebt jetzt Mitfahren, Call to me, Laden (`B.GrowBody`). Die Forschung kannte es (`forschung_b1d.md:314`: Weg B2 "passt zu ENT:45
'nicht Spieler'"), der Plan erwaehnt es nur fuer WILDE Junge (F5). Die Engine verletzte das zahme Junge schon in B1c -- neu ist, dass der
Schaden haften bleibt. Vorschlag: keine Code-Aenderung in B1d (Schutz vor Spieler/Auto ist B5a-Gegenwehr); F5 fuer Kevin praezisieren: "Ein
Spieler oder Auto kann dein zahmes Junges verletzen, und das bleibt jetzt -- laut ENT:45 sollen Spieler und Autos keinen Schaden machen;
mit B5a abschalten?"

### A5 (minor, Trennung) -- Probe-Wege `B.GrowSetG` / `B.GrowSetHp` / `B.SkillSet` gehen mit nach NPC Crew
Die drei Funktionen (`Grow.lua:294-301`, `:600-629`) sind reine Testwege ("Vorspulen", Leben und Erfahrung von Hand setzen; Kommentar
`Grow.lua:292`, `:596`: "Probebefehl(e) der Test-Mod"). Die Regel `probeweg` des Uebernahme-Skripts (`baer/tools/baer_uebernahme.py:307-308`,
`TIER_DEF` :355) erzwingt, dass im kopierten Code niemand sie ruft -- als tote Definition kommen sie aber in NPC Crew an. Werkstatt-CLAUDE.md
0.2: Testhilfen leben NUR in eigenen Bench-Dateien. Es ist kein Befehl, kein Menue, kein Global (Grow.lua laedt am MP-Client gar nicht,
`Grow.lua:1`), also kein Cheat-Weg im MP; im SP koennte man ueber die Debug-Konsole ohnehin `rec.g` setzen. Vorschlag: entweder in die Bench
verlegen (sie darf im SP `B.GrowFix`, `B.Commit`, `B.ApplySize`, `B.BodyHp` rufen; die Tier-Regeln bleiben, weil die Bench nie kopiert wird)
oder in `NAEHTE.md` "Erlaubte Fundstellen" mit Grund ("spaeter Baeren-Fenster / Von-Hand-Heilen") und als Kevin-Frage. Plan 6.3 hat es so
gewollt -- deshalb nur minor.

### A6 (minor, Texte) -- die Tooltips der zwei Auswahlen sieht der Spieler nie
`MainOptions.lua:2910-2911` baut die Mod-Auswahl ohne Tooltip (`addCombo(..., getText(option.name), option.values, option.selected)`), die
Tickbox dagegen mit (`:2810-2813`). `UI_BN_Bear_MO_HealthTip` und `UI_BN_Bear_MO_StaminaTip` (2 x 7 Texte) erreichen das Spiel also nie --
insbesondere die einzige Erklaerung *"Stamina drops while a bear runs and comes back while it rests"*. Der Kommentar
`S:client/BanditsNPCBearOptions.lua:17` sagt es ehrlich. Vorschlag: Kevin fragen, ob ihm das reicht; sonst die Kurzinfo in den Namen
("Health above tamed bears (off / bar / number)") -- `addDescription` waere kein Ausweg (nimmt `option.text` ohne `getText`,
`MainOptions.lua:2807-2808`, und das Skript verbietet `getText` als Argument).

### A7 (minor, Regelfrage, bekannt) -- `addComboBox` / `addItem` ohne Aufrufer in Vanilla und Bandits
Wie B1c A3 (`addTickBox`/`addSlider`): grep ueber `V:` und `B:` (42.22 + common) findet nur die Definition `V:client/PZAPI/ModOptions.lua:121`;
NPC Crew benutzt beide gespielt (`NC:client/BanditsNPCModOptions.lua:95-104`, gelesen, nicht kopiert -- unsere Zeilen sind eigene). Steht als
Frage 10 im Zusammenbau. Vorschlag: so lassen, Kevins Wort abwarten.

### A8 (minor) -- Kleinkram
1. **NPC Crew wandert waehrend des Laufs:** mein Trockenlauf ohne `--vor-b5a` weicht vom gespeicherten nur in `NC shared/BanditsNPC.lua:1359`
   -> `:1360` ab; `NAEHTE.md` Zeile 4 nennt `BanditsNPC.Opt` bei `shared/BanditsNPC.lua:6101`, heute steht die Funktion bei `:6105`. Kein
   Fehler (NAEHTE sagt "Zeilen wandern"), aber vor einer echten Uebernahme Trockenlauf, Probe und den Tier-Grep (NAEHTE Zeile 25) neu.
2. **Texte, die spaeter falsch werden:** Sandbox-Tooltip `BearGrowDays` verspricht "fully grown (size 1.35)", das Bild bleibt in B1d bei 0,75
   stehen; "Has no effect until bears can fight." (`BearDodgeMax`, `BearFightBonusMax`) und "... can sleep." (`BearHealSleep`) muessen mit
   B5a bzw. dem Schlaf-Lauf heraus (schnittstelle_aenderungen.md B1d OBERFLAECHE 7 nennt nur den Kampf-Satz). Merker fuer die spaeteren Laeufe.
3. **Skript-Regeln bleiben Regex** (wie B1c A4): `"setSize" .. "Forced"` oder `a["get" .. "Health"]` umginge `setSizeForced`/`getHealth`
   (`baer_uebernahme.py:297-304`); `getData` ist als einzige der vier Regeln ohne `(?i)` (harmlos, Lua unterscheidet Gross/Klein). Die
   Gegenprobe deckt nur direkte Namen. Kein Handlungsbedarf, nur ehrlich im Bericht.
4. Kommentare der kopierten Dateien nennen "Probebefehl(e) der Test-Mod" (`Grow.lua:292`, `:596`, `Stats.lua:5`) -- gehen nach NPC Crew mit,
   keine Befehlsnamen, kein Cheat-Fund; mit A5 erledigt sich das.
5. `attrappe/pruef_b1b/run.lua` (die alte Fassung ohne `_nach`) passt zu keiner gespeicherten Ausgabe mehr ("Laufbefehle" je +1 seit B1c);
   massgeblich ist `run_nach.lua` == `ergebnis_b1c.txt`. Nur Ordnung.

## 4. Ohne Befund geprueft
- **Testbefehle nur in der Bench:** `NCBear_*`/`NCBearBench` im Code ausserhalb `S:client/NCBearBenchCub.lua`: 0 (eigener grep, xref,
  Skript). Die vier neuen Befehle `NCBear_CubGrow/_CubStats/_CubXp/_CubHurt` und die zwei Menue-Eintraege ("Cub: grow 5 days", "Cub: stats",
  Bench `:917-918`, `:934-935`) gehen alle ueber `ready()` (`Bench:69-90`, `B.IsSP()` = `not isClient() and not isServer()`,
  `S:shared/BanditsNPCBear.lua:167-169`) -> im MP "singleplayer only". Die Bench liest am Tier nur `getData():getSize()`/`getHealth()`
  (Fundstelle im Kommentar `Bench:866`). `mod_info_vorschlag.txt` nennt 25 Testhilfen = 25 `function NCBear_` in der Bench; LF, ASCII.
- **Alte NCBear*-Dateien:** das Staging enthaelt ausser der Bench des Jungen keine `NCBear*`-Lua; nichts an `T:shared/NCBearFight.lua` usw.
  Kein Wechsel auf die Art `bear` (`Grow.lua` nennt sie nur im Kommentar `:403`); `B.CFG.bodySwap = false`.
- **Namen und Kollisionen:** neue Dateien `BanditsNPCBearStats.lua`, `BanditsNPCBearGrow.lua`; in `NC:` 0 Dateien `BanditsNPCBear*`,
  0 Treffer `BanditsNPC.Bear`, `BearGrow|BearDodge|BearFight|BearHeal|BearStats|BearStage|BearSkill|UI_BN_Bear` in `NC 42/media` nur
  `UI_BN_Beard_None` (NPC Crews, anderer Schluessel); Landkarte `NC _docs/landkarte_index.txt` ohne Baer; Skript: v3.8.38-Probe 143 Funktionen
  gegen 162 Modultabellen, keine Kollision, 0 Vanilla-Treffer. Bench-Namen `NCBear_CubGrow/Stats/Xp/Hurt` kommen in der Test-Mod sonst nicht
  vor. Optionen-Ids `TagHealth`/`TagStamina`/`TagAge` auf der EIGENEN Seite `BanditsNPCBear` (NPC Crews Seite heisst `NPCCrew`).
- **Texte (7 Sprachen):** UI.json je 133, Sandbox.json je 60, Paritaet ja; Platzhalter je Schluessel in allen Sprachen gleich (KO stellt in
  `Tag_Age` `%3` vor `%2`, `getText` setzt nach Nummer ein, `B.T` -> `getText(key, s1, s2, s3)`, `S:shared/BanditsNPCBear.lua:325`); kein
  `<`/`>`, kein Testwort, Sandbox-Texte ohne nacktes `%` ("percent"); CN: 0 Zeichen, die Vanilla-CN nicht benutzt (gegen alle Dateien in
  `V:shared/Translate/CN/`); `U.EN` == EN/UI.json wortgleich (Skript). Die 24 neuen UI- und 10 Sandbox-Texte habe ich in allen 7 Sprachen
  gelesen: inhaltlich stimmig, Satzbau mit den eingesetzten Stufen-Namen in allen Sprachen lesbar. IG_UI.json EN hat 6 Schluessel (3 davon
  die bekannten Test-Tiernamen = Altlasten B5a), das Skript kopiert nur die 3 echten.
- **Sandbox:** 5 neue Optionen in `sandbox-options.txt` zwischen `BearCallCooldownMinutes` und `BearLog`, `page = BanditsNPC`, Zahlen textgleich
  mit `B.OPTS` (`S:shared/BanditsNPCBear.lua:149-153`, Doubles `1.0`/`15.0`, Skript `plan_sandbox`), `type = double` hat NPC Crew selbst
  (`NC 42/media/sandbox-options.txt:14`). Name + Tooltip je Option in allen 7 Sandbox.json. Benutzt: `BearGrowDays` (`B.GrowDays`, Stats.lua:148),
  `BearDodgeMax`/`BearFightBonusMax` (`B.StatsOf` :302, :305), `BearHealAwake`/`BearHealSleep` (`B.HealRate` :324-327); die drei ohne Wirkung
  sagen das im Tooltip (Auftrag Punkt 4/5 verlangt die Sandbox schon jetzt). `B.Opt` klemmt auf min/max (`S:shared/BanditsNPCBear.lua:180-199`).
- **Kevins Zahlen:** 0,35 / 0,75 / 1,0 / 1,35 an Tag 0 / 15 / 45 / 100 (`B.CFG.growCurve`), Traglast 10 / 40 / 100, Ausweichen 5 % .. 40 %,
  Kaempfen +70 %, Leben-Bonus +50 % (`ENT:21`), Heilen 1 / 15 %/h, Fischen erst ab Halbstark (`B.OnFish` Rang >= 1, Fang 0 darunter) -- alle
  so gebaut. Werte stetig aus der inneren Groesse -> steigen jeden Tag (Kevin `ENT:207`).
- **Uebernahme:** Bench nie kopiert (24 von 25 Lua); keine neue Naht, keine NPC-Crew-Lua beruehrt; NAEHTE-Zeilen 4, 5, 11, 14, 15, 19, 25
  gegen die Fundstellen gelesen (`NC shared/BanditsNPCLivestockSlaughter.lua:2016` `setHealth(0)` beim Schlachten, `:548-550`, `:1025-1026`
  `NOT_TENDED`; `NC client/BanditsNPCModOptions.lua:95-104`) -- stimmen (bis auf die gewanderte Zeile A8.1). Kein `.git` in der Probe.
- **SP/MP-Riegel:** Client-Probe der Groesse nur `isClient()` (Hud :441), im SP nie; `B.GrowFromMark` deckelt nur im MP (`B.IsSP()`);
  `B.Tell` im SP direkt, am Server `sendServerCommand`; kein neuer Client-Befehl (xref 3).
- **Lernen, nicht kopieren:** Erfahrungs-Eimer und "eine Zahl je Faehigkeit" nach `NC shared/BanditsNPCSkills.lua:52-59`, `:475-500` -- nur das
  Konzept, eigener Code (Felder, Namen, Aufbau verschieden).

## 5. Offen / ungeprueft (zusaetzlich zu Zusammenbau 7)
- Ob `setSizeForced` an der MP-Client-Kopie etwas ins Netz schickt oder den Anti-Cheat beruehrt: ungeprueft (NUR JAR) -- Pruefer B / MP-Test.
- Laufzeit aller B1d-Wege: ungespielt (Zusammenbau 7.1-7.3 gilt).

## 6. Fragen fuer Kevin (Kevin schlaeft -- nichts davon haelt den Einbau auf)
1. (A1) Die langsame Selbstheilung (1 %/h, die Spiel-Heilung wird zurueckgenommen) ist schon an, obwohl du "Heilen erst nach meinem B1c-Test"
   gesagt hast. So lassen? Empfehlung: ja, zusammen mit dem B1c-Test ansehen.
2. (A3) `setHealth` mit Werten zwischen 0 und 1 und `setSizeForced` am lebenden Tier: Vanilla benutzt beide nur am Haken-/toten Tier bzw. mit 0;
   gelten sie als belegt? Empfehlung: ja (gleicher Typ; `setSizeForced` hast du am lebenden Baeren schon benutzt).
3. (A4) Spieler und Autos koennen dein zahmes Junges verletzen, und das bleibt jetzt -- laut ENT:45 sollen sie keinen Schaden machen. Mit B5a
   abschalten? Empfehlung: ja, mit B5a.
4. (A5) Die Vorspul-/Setz-Wege der Testhilfe liegen im Kern (ohne Aufrufer). In die Testhilfe verlegen? Empfehlung: ja, beim naechsten Lauf.
5. (A6) Die Erklaerungen der Auswahlen Leben/Ausdauer zeigt das Optionen-Fenster nicht an. Reicht dir der Name? Empfehlung: ja.

Statisch geprueft, nicht gespielt.
