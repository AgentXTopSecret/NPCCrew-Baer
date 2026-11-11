# Lauf baer-b1d: Bau KERN (Wachsen, Werte, Faehigkeiten, Leben, Sicht)

Stand 11.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Spiel 42.22.2. Rolle: BAUER KERN (shared/ ohne Translate, server/).
Umgesetzt: `PLAN_B1D.md` 0.1-0.13, 1.1-1.5, 2, 3, 4.1, 5, 6.1-6.4, 7.1, 8 fuer den KERN-Teil, woertlich; Zusaetze/Auslegungen stehen in
`schnittstelle_aenderungen.md` Abschnitt "B1d KERN" (14 Punkte, alle rueckwaertsvertraeglich). Nichts in die Test-Mod, nach NPC Crew,
Vanilla oder Bandits geschrieben; keine Client-Datei, kein Text, keine Bench, keine alte `NCBear*`-Datei angefasst.
Kurzformen: `S:` = Staging `mod/42/media/lua/`, `V:` = Vanilla `media/lua/`, `B:` = Bandits `42.22/media/lua/`, `T:` = NCBearTest.

---

## 1. Dateien

| Datei (`S:`) | Art | Zeilen | Inhalt |
|---|---|---|---|
| `shared/BanditsNPCBearStats.lua` | **neu** | 347 | reine Formeln (Kurve, Stufen, Werte, Faehigkeiten, Heilrate) + `B.ApplySize` (einzige Stelle mit `getData`/`setSizeForced`) |
| `server/BanditsNPCBearGrow.lua` | **neu** | 629 | Takte und Register-Seite: `B.GrowFix`, `B.BodyHp`, `B.SkillAdd`, `B.SkillSet`, Haken, Ausdauer, `B.GrowLive`, `B.GrowSlow`, `B.GrowBody`, `B.GrowFeed`, `B.GrowFromMark`, `B.GrowView`, `B.GrowSetG`, `B.GrowSetHp` |
| `shared/BanditsNPCBear.lua` | geaendert | | Kopf-Kommentar B1d (:8-10), `B.CFG` B1d-Block (:102-120), `B.OPTS` + 5 Optionen (:148-153) |
| `shared/BanditsNPCBearDefs.lua` | geaendert | | Weg B (F1): `maxSize = 1.35` (:84), `stages[CUB] = { ageToGrow = 36500 }` (:72-73), Kopf-/Gen-Kommentar (:13-20, :34-35) |
| `server/BanditsNPCBearServer.lua` | geaendert | | drei Haken: `B.FeedComplete` (:242-243), `slowTickBody` (:581-582), `liveRec` (:746-747) |
| `server/BanditsNPCBearRegistry.lua` | geaendert | | `B.InitRegistry` GrowFix-Schleife (:165-171), `viewEntry` Tabelle `t` + `B.GrowView` (:572-584), Kommentare (:28, :555) |
| `server/BanditsNPCBearHeal.lua` | geaendert | | `MARK_FIELDS` + 10 (:38-44), `B.Restore` Haken (:245-246), `B.TakeNewerMark` Haken (:361-362) |
| `server/BanditsNPCBearRide.lua` | geaendert | | `B.PlaceCub` -> `B.GrowBody` (:85-86) |
| `attrappe/kern/attrappen.lua` | geaendert | | A.FILES + Stats/Grow; Tier `getData()`/`getHealth()`/`setHealth()` mit Zaehlern; `ShowNote` mit `w` |
| `attrappe/b1d_kern/run.lua`, `ergebnis.txt` | **neu** | 942 | 19 Abschnitte, 147 Faelle |
| `schnittstelle_aenderungen.md` | angehaengt | | Abschnitt "B1d KERN" |

Ladefolge (alphabetisch, auf Dateiebene nichts Fremdes eingefangen): shared `...Bear < Crew < Defs < Food < Rules < Stats`; server
`Follow < Grow < Guard < Heal < Registry < Ride < Server < World`. `server/`-Datei beginnt mit `if isClient() then return end`. Alle
Haken in alten Dateien hinter `if B.X then` (fehlt eine B1d-Datei, laeuft B1c unveraendert).

## 2. Was gebaut ist (je Auftragspunkt)

**Wachsen (Auftrag 1, Plan 0.1-0.4, 1.1).** Register-Feld `rec.g` (0..1) nur fuer `tame`/`missing`; je Langsam-Takt (`B.GrowSlow`,
Grow.lua:422) `g += dt / (D x 24)`, `D = BearGrowDays` (Vorgabe 100, 10..365). Kurve `B.GrowSize` (Stats.lua:155) stueckweise gerade
`(0, 0,35) (0,15, 0,75) (0,45, 1,0) (1, 1,35)` -> D 100: Tag 15/45/100 = 0,75/1,0/1,35; anteilig bei anderem D; ein D-Wechsel aendert nur
das Tempo. Commit hoechstens je Spielstunde (nur wenn sich `g` oder `hp` geaendert hat), sofort bei Stufenwechsel (+ `Note_Grown` an den
Besitzer) oder Verlust >= 2 %. Uhren nur mit Besitzer im Spiel, nie bei `missing`, nie wild/scheu/angefuettert; mitfahrend waechst es.
Fuetter-Bonus `B.GrowFeed` (Grow.lua:470) aus `B.FeedComplete` Zweig `wasTame`: 3/2/1 Spielstunden (Lieblingsfutter/normal/Happen),
hoechstens 2 je Spieltag, Summe `gF <= 0,10`. Groesse nur ueber `B.ApplySize` (Stats.lua:340): je Hirn-Takt (`B.GrowLive`, Grow.lua:396),
sofort am neuen Koerper (`B.GrowBody`, Grow.lua:456), nach `B.GrowSetG`. Speichern/Laden: `g`, `gF`, `gFd`, `gFn`, `gAt` im Register,
`g`/`gF`/`gFd`/`gFn` + Erfahrung im Spiegel; Migration `B.GrowFix` (Grow.lua:103) in `B.InitRegistry` -- Kevins B1c-Junges bekommt `g` aus
`tamedAt` (nur Diagnose-Zeile).

**Modellwechsel vorbereitet (Auftrag 2, Plan 0.10).** `B.BodyOf` (Stats.lua:225) gibt immer `"cub"` und `sz = min(s, cubMaxSize 0,75)`;
`B.CFG.bodySwap = false`. Steht er auf true, bleibt es beim Junges-Modell und `B.GrowLive` schreibt je Junges eine Fehlerzeile je
10 Minuten; der Kommentar dort beschreibt den spaeteren Tausch (B.RemoveCub + B.PlaceCub mit gen + 1; nie Art "bear"). Kein Engine-Aufruf.

**Werte (Auftrag 3, Plan 0.5, 0.6).** `B.StatsOf` (Stats.lua:276): Leben 40/150/400, Ausdauer 50/100/160, Traglast 10/40/100 (Kevin),
Schaden-Faktor 0/0,35/1,0 an 0,35/0,75/1,35, dazwischen gerade -> jeder Wert steigt JEDEN Spieltag (Attrappe 4: Tag 0..100 streng
steigend). Leben am Tier ueber den belegten Weg (`B.BodyHp`, Grow.lua:191): Anteil `rec.hp` ist die Wahrheit, `rec.hpB` der zuletzt
gesetzte/gesehene Koerperwert; Engine-Schaden zaehlt, Engine-Heilung wird zurueckgenommen, nie 0, nie > 1, nicht am toten Tier.

**Faehigkeiten (Auftrag 4, Plan 0.7, 0.8).** Je Faehigkeit EINE Zahl (`xAgi xVit xCon xFgt xFsh xNos`), Stufe 0..10 daraus
(`B.SkillLevel`, Bedarf 100 x 1,16^n, Summe 2133). Wirkung: Ausweichen 5..`BearDodgeMax` (40) %, Leben/Ausdauer +5 % je Stufe, Kampf-Bonus
bis `BearFightBonusMax` (70) %, Fang-Chance ab Halbstark, Warnweite. Ein Weg fuer Erfahrung `B.SkillAdd` (Grow.lua:254) mit Echtzeit-Eimer
(18 voll, +6/min). Verdrahtet ist nur Kondition: unser Rennbefehl (`s.walk == false`, `ms < s.ownUntil`) -> 1 XP je 5 Kacheln, ausser
Puste +5 (je 60 s). Haken ohne Aufrufer: `B.OnHitTaken`, `B.OnHitDealt`, `B.OnFish` (ab Halbstark), `B.OnSniff`. Ausdauer nur Sitzung, ohne
Wirkung, sinkt nur beim eigenen Rennen.

**Heilen-Vorbereitung (Auftrag 5).** `B.HealRate(asleep)` (Stats.lua:324): `BearHealAwake` 1,0 / `BearHealSleep` 15,0 % je Spielstunde
(Sandbox, Doubles textgleich). Angewandt wird in B1d nur wach (kein Schlaf), mit Koerper am Tier, ohne Koerper nur im Register.

**Anzeige (Auftrag 6, KERN-Seite).** `B.GrowView` (Grow.lua:573) aus `viewEntry`: `sz hp hpMax sta staMax day stg nst nxt` nur bei
`tame`. Ausdauer-Sicht gedrosselt nur an den Besitzer (`B.Touch(nil, owner)`).

**Bench (Auftrag 7, KERN-Seite).** Wege fuer die Probebefehle: `B.GrowSetG`, `B.GrowSetHp`, `B.SkillSet` (Grow.lua:600, :619, :294).

## 3. Engine-Aufrufe mit Fundstelle (selbst nachgelesen)

| Aufruf | Wo (`S:`) | Beleg (gleiche Argumenttypen) | Seite |
|---|---|---|---|
| `animal:getData()` | Stats.lua:342 `B.ApplySize` (einzige Stelle) | `V:shared/Definitions/animal/ButcheringUtil.lua:566`, `:569`, `:586` | SP, Server, MP-Client (Hud) |
| `animal:getData():getSize()` | Stats.lua:344 | `ButcheringUtil.lua:570`; `V:client/ISUI/Animal/ISAnimalUI.lua:31`; `V:shared/TimedActions/Animals/ISPetAnimal.lua:28` | beide |
| `animal:getData():setSizeForced(Zahl)` | Stats.lua:345 (einzige Stelle) | `ButcheringUtil.lua:569`/`:571` (createAnimalForHook <- `:535`; Schreiber `V:shared/TimedActions/Animals/ISPutAnimalOnHook.lua:88`, Client `V:client/ISUI/Animal/ISButcherHookUI.lua:520`), `:586` (Server `:674` isServer-Zweig, `V:shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70`, Client `ISButcherHookUI.lua:530`), `:242` (frisch gebautes IsoAnimal). **Grenzfall:** am lebenden Tier in der Welt nur `T:client/NCBearSize.lua:27` | SP, Server, MP-Client |
| `animal:isDead()` | Grow.lua:201 `B.BodyHp` | `V:server/Traps/STrapGlobalObject.lua:238` | Schreiber |
| `animal:getHealth()` | Grow.lua:205 `B.BodyHp` (einzige Stelle) | `V:client/ISUI/Animal/ISAnimalUI.lua:15` (am Tier, Client); geerbte Methode am Zombie am Server `B:server/BanditServerSync.lua:11`, `B:server/BanditSave.lua:52`; im SP gespielt `T:client/NCBearAttackProbe.lua:104`. **Am MP-Server am Tier offen** (Plan 8 Nr. 4) | SP + Server |
| `animal:setHealth(Zahl)` | Grow.lua:237 `B.BodyHp` (einzige Stelle) | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:545` (SP), `V:server/ClientCommands.lua:932` (Server), `V:shared/TimedActions/Animals/ISKillAnimal.lua:58` -- Vanilla setzt nur 0; eine Zahl > 0 setzt `B:server/BanditServerSync.lua:12` am Zombie (geerbt). Werte 0..1 ohne Klemme NUR JAR `dec/IsoAnimal.java:1156-1163` | SP + Server |
| `getTimestampMs()` | Grow.lua (Eimer, Uhren) | `V:server/Foraging/forageServer.lua:456` | Schreiber |
| `getGameTime():getWorldAgeHours()` | ueber `B.Now()` | `V:server/Traps/STrapSystem.lua:77` | Schreiber |
| Takte | vorhandene `EveryTenMinutes` / `OnTick` (keine neuen) | `V:server/Traps/STrapSystem.lua:134`, `V:server/Foraging/forageServer.lua:502` | Schreiber |
| `math.floor/ceil/abs`, `tonumber`, Tabellen | -- | Lua-Grundbibliothek (kein `math.min/max`, kein `next`, kein `%a`) | beide |

**Nicht benutzt** (auch nicht hinter pcall): `getData():setSize` (Klemme), `setWeight`, Engine-Alter/-Stufen, `setIsInvincible`,
`healthLossMultiplier`, `getMinSize/getMaxSize`, `transmitModData`. **Jar-only-Aufrufe in B1d: keine.** Kein neues pcall (die Takte laufen
weiter im vorhandenen, lauten pcall von `B.SlowTick`/`B.BrainTick`).

## 4. SP- und MP-Zweig je Vorgang

| Vorgang | Einzelspieler (`not isServer() and not isClient()`) | Mehrspieler |
|---|---|---|
| Wachsen je Langsam-Takt | `B.SlowTick` -> `B.GrowSlow`, Besitzer `__sp` in `B.Players()` | Server; nur wenn das Konto des Besitzers online ist (F4); Clients rechnen nie |
| Groesse am Tier | Schreiber-Objekt = gezeigtes Objekt, `B.GrowLive` setzt je Hirn-Takt nach | Server setzt seine Kopie; Clients bekommen sie nur bei der Erstuebertragung (NUR JAR) -> MP-Client-Probe im Hud (OBERFLAECHE) mit `sz` aus der Sicht; Weg B laesst die Groesse Laden/Erstuebertragung ueberstehen |
| Leben | `B.BodyHp` liest/setzt am Schreiber | Server (getHealth am Tier am Server: Testpunkt); Clients sehen die Engine-Kopie (Tierpaket) und `hp` aus der Sicht |
| Fuetter-Bonus | `B.FeedComplete` direkt | `complete()` am Server; Fremde scheitern an `B.CheckFeed` (`Why_NotOwner`), kein Bonus (Attrappe 17) |
| Stufe/Faehigkeit-Meldung | `B.Tell` -> `B.ShowNote` direkt (sendServerCommand tut im SP nichts) | `sendServerCommand(Note)` mit `w`, nur an den Besitzer, wenn online |
| Sicht | `B.SendView` -> `B.ApplySync` direkt | `sendServerCommand(Sync)`; Ausdauer-Touch nur an den Besitzer (Attrappe 17: Kevin 1, Bob 0) |
| Spiegel-Heilung | `"restore"` voll, `"newer"` = max | `"restore"` mit Deckel `g <= Tage seit tamedAt + 0,10` und Fehlerzeile; `"newer"` gibt es im MP nicht (Register gewinnt, B1c) |
| Mitfahren / Call / Tod im Auto | `B.PlaceCub` -> `B.GrowBody` sofort | gleich, am Server |
| Probebefehle | `B.GrowSetG/GrowSetHp/SkillSet` von der Bench (nur SP) | Bench lehnt ab; die Funktionen liegen in einer Server-Datei (kein Client-Weg) |

Kein Kick (kein neuer Client-Befehl), nichts haengt (alles in vorhandenen Takten, Deckel: Eintraege, 6 Eimer je Junges), kein Gegenstand
entsteht oder verschwindet (Fuetter-Bonus haengt am vorhandenen, gepruefte `takeOne`), keine NPC-Crew-Figur beruehrt.

## 5. Pruefer-Ausgaben (acht KERN-Dateien)

```
luacheck.py      8 file(s) checked, 0 failed
scopecheck.py    8 file(s), 0 violation(s)
localcount.py    hoechstens 37 aktiv / 51 insgesamt (Server.lua brainTickBody :915); neue Dateien: Stats.lua B.StatsOf 28/32,
                 Grow.lua 24 (Grenze 200, ab 180 aufteilen)
luacheck_pz.py   0 Treffer (W113); --unused auf Stats.lua + Grow.lua: 0 Treffer (W113, W211, W212, W213, W311)
Zeilenenden      alle LF, reines ASCII (file: "ASCII text", 0 x CR)
Trockenlauf      baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a: OK -- 0 Fehler, 26 Warnungen (wie B1c; alles Altlasten
                 B5a + GLB-Clips + ein NPC-Crew-Kommentar). Grow.lua und Stats.lua in der Kopierliste, 27 Sandbox-Optionen passen zu B.OPTS.
```

## 6. Attrappen

| Lauf | Ergebnis |
|---|---|
| `attrappe/b1d_kern/run.lua` (**neu**) | **147 bestanden, 0 Fehler** (`b1d_kern/ergebnis.txt`) |
| `attrappe/kern/run.lua` | 136 bestanden, 0 Fehler -- Ausgabe byte-gleich mit `kern/ergebnis.txt` (jetzt MIT B1d geladen) |
| `attrappe/b1b_kern/run.lua` | 204 bestanden, 0 Fehler -- byte-gleich mit `ergebnis.txt` |
| `attrappe/b1c_kern/run.lua` | 192 bestanden, 0 Fehler -- byte-gleich mit `ergebnis.txt` |
| `attrappe/gesamt/run.lua` | 812 bestanden, 0 Fehler -- gleich (FILES ohne B1d; gehoert dem ZUSAMMENBAU) |
| `attrappe/pruef_b`, `pruef_b1b`, `pruef_b1c` | Ausgabe mit und ohne B1d-Dateien identisch (Vergleich ueber einen Lader ohne Stats/Grow) |
| `ober`, `b1b_ober`, `b1c_ober`, `b1d_ober` mit echtem Kern (shared) | 117 / 134 / 180 / 173 ok, 0 Fehler |

Gewollt geaenderte alte Erwartungen: **keine**. Erweitert (nur Zusatz) wurde `attrappe/kern/attrappen.lua` (Grund: Kern ruft neu
`getData`/`getHealth`/`setHealth`; die zwei neuen Dateien in `A.FILES`; `ShowNote` schreibt `w` mit).

b1d_kern deckt Plan 7.1 Punkt 1-18 und die im Auftrag genannten Faelle Folgen/Bleiben/Umbenennen/Waisen (Abschnitt 19):
1 Kurve (Meilensteine 1e-9, streng steigend, 0,55, Umkehrung, Klemmen) - 2 Tage (D 100/50/365 ueber echte `B.GrowSlow`-Schritte,
D-Wechsel 100 -> 200) - 3 Stufen (0,12 -> cub, half in 3 Tagen ...) - 4 Werte (Stuetzwerte, Tag 5 Leben 77, Tag 0..100 streng steigend) -
5 Faehigkeiten (Kurve 2133, Klemmen, Fortschritt, 5/22,5/40 %, DodgeMax 80, +70 %, +50 %, Fischen) - 6 Langsam-Takt (online/offline/
missing/wild/Fahrt, g <= 1, 1 Commit je Stunde, Stufen-Meldung genau einmal, Ruecksetzen ohne Meldung, voller Baer ohne Commit) -
7 Migration (Tag 2 aus tamedAt nur mit Diagnose-Zeile, "x" -> eine Fehlerzeile, wild -> nil, hp 0 -> nil, Klemmen) - 8 Groessen-Probe
(genau ein setSizeForced(0.75), 2 Getter je Takt, cubMaxSize, Engine-Ruecksetzen, wild nie, bodySwap eine Zeile je 10 min) - 9 Leben
(Engine-Heilung zurueck, Verlust + sofort Commit, +1,67 % in 10 Takten, nie 0/nie > 1, tot, ohne Koerper, Entladen, hp nil) -
10 Fuetter-Bonus (3/2/1 h, 2 je Tag, Summe 0,10, g = 1, wild nie) - 11 Kondition/Ausdauer (1/50 je 2,5 Kacheln, 1 XP je 5, Gehen, 12er-Sprung,
Eimer <= 24 in 1 min, ausser Puste +5/60 s, Aufstieg + Note_SkillUp w 1, Sicht-Touch nur Besitzer, ab 10 Punkten, nicht unter 5 s) -
12 Spiegel (10 Felder, Restore, B1c-Spiegel ohne g, MP-Deckel 0,12, newer = max) - 13 Mitfahren/Call/Tod im Auto (keine Engine-Aufrufe
in der Fahrt, neuer Koerper bekommt setSizeForced(sz) und setHealth(hp), Uhr steht bei totem Besitzer) - 14 Sicht (Felder, gerundet, wild
ohne, hp nil, ausgewachsen, flach, ApplySync) - 15 Speichern/Laden - 16 Tod - 17 MP-Rundlauf (Server, Kevin offline -> Uhr steht, Bob sieht
dieselben Zahlen, Bob fuettert -> Why_NotOwner, Sync an beide, Ausdauer-Touch nur an Kevin) - 18 Dateiregeln (setSizeForced/getData nur
in B.ApplySize, setHealth/getHealth nur in B.BodyHp -- ueber alle Nicht-Bench-Dateien inkl. Client --, CreateCub unveraendert, LF/ASCII,
kein next(/%a, kein spawn/debug/bench/cheat/test im Code der neuen Dateien) - 19 Folgen (rennt hinterher: Ausdauer sinkt, Kondition steigt),
Bleiben (nichts), Umbenennen (Werte bleiben, Spiegel traegt Name + g + xCon), Waise (entfernt, nie eine Groessen-/Leben-Abfrage).

**Fuer den ZUSAMMENBAU:** eine Probe der Gesamt-Attrappe MIT Stats/Grow in FILES (Kopie im Arbeitsordner der Sitzung, nichts geaendert)
ergibt 841 ok, 5 Fehler -- alle Schild-Erwartungen der OBERFLAECHE (Alter-Zeile und Leben-Balken sind jetzt Vorgabe, F9); deckt sich mit
OBERFLAECHE-Hinweis 11 in `schnittstelle_aenderungen.md`. Fuer TIER_RULES (Plan 10): `setSizeForced`/`getData` nur
`("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")`, `setHealth`/`getHealth` nur `("42/media/lua/server/BanditsNPCBearGrow.lua",
"B.BodyHp")` -- Attrappe 18 bestaetigt, dass es heute so ist (Bench ausgenommen).

## 7. Offen / ungeprueft (Testpunkte, nichts davon gespielt)

- `setSizeForced` an einem LEBENDEN Tier in der Welt (Vanilla nur Haken-/neu gebaute Tiere): sieht man den Wechsel, ruckt es, wirkt es
  direkt nach `addToWorld` (B.GrowBody; der naechste Hirn-Takt setzt sicher nach).
- `setHealth` mit Werten zwischen 0 und 1 an einem lebenden Tier (Vanilla setzt nur 0; Bandits setzt am Zombie beliebige Zahlen).
- `getHealth()` am Tier am **MP-Server** (Plan 8 Nr. 4): scheitert es, steht "slow tick: ..." bzw. "brain tick: ..." im Log (B.ErrEvery).
- Engine-Heilung ~1,5-2,2 %/h (NUR JAR): wie oft sie im Spiel kommt; zurueckgenommen wird sie, sobald der Koerper > 0,5 % vor `hpB` liegt
  (bis zu 10 Spielminuten sichtbar).
- Weg B der Definition (F1): ob die Engine eine gespeicherte Groesse > 0,35 beim Laden wirklich behaelt (NUR JAR: Klemme auf [min, max]).
  Bestehende Junge laden als 0,35 und werden im ersten Hirn-Takt gesetzt. **Kevin muss das Spiel neu starten** (Definition und Lua).
- Fussgleiten, Streichel-Haltung, Schild-Hoehe bei 0,5-0,75 (F2, OBERFLAECHE/Kevins Blick).
- Wie viel Rennen in 100 Tagen zusammenkommt (F14); ob `EveryTenMinutes` beim Schlafen/Vorspulen jede Stufe feuert (Deckel 1 h je Schritt
  kann Wachstum kosten, nie doppelt geben).
- MP: Erfahrung aus einem gefaelschten Spiegel nach Registerverlust nicht pruefbar (F18, wie B1c F1); Wachstum ist gedeckelt.

## 8. Fragen fuer Kevin (aus dem Plan, so gebaut wie empfohlen)

F1 Definition 0,35..1,35 (gebaut: ja) - F3 Zahlen 40/150/400, 50/100/160, 0/0,35/1,0 (gebaut) - F4 kein Wachsen ohne eingeloggten Besitzer
(gebaut) - F5 Engine-Heilung zuruecknehmen (gebaut), Definition-Weg erst mit B5a - F7 Fuetter-Bonus 3/2/1 h, 2 je Tag, max 10 Tage (gebaut)
- F8 Wachsen beim Vermisstsein anhalten (gebaut) - F12 "Tag" = Wachstumstag (gebaut) - F13 Ausdauer nur beim Rennen, nach dem Laden voll
(gebaut) - F14 Kondition-Tempo (Stellwerte) - F16 Meldungen Stufe/Faehigkeit (gebaut) - F18 MP-Spiegel (so gelassen).
Neu aus dem Bau: keine weitere Frage.

Statisch geprueft, nicht gespielt.
