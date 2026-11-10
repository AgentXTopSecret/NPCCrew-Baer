# Gegenpruefung B1a "baer-zaehmen" (10.11.2026)

Rolle: Gegenpruefer. Nichts davon gebaut, keinem Bericht geglaubt: jede geaenderte Stelle samt Umgebung im heutigen Staging gelesen,
alle Pruefer selbst laufen lassen. **Statisch geprueft, nicht gespielt.** Nichts geschrieben ausser dieser Datei und
`anleitung_zaehmen_entwurf.md`; Probe in einen eigenen Scratchpad-Ordner (nicht `_arbeit/.../probe`). Kein git, kein Spiel.

## 1. Urteil

**Bereit fuer Kevins ersten Einzelspieler-Test.** Kein Blocker gefunden. Alle 17 Befunde gelesen: 15 im Code geschlossen bzw. zu
Recht unveraendert (A8), 2 teils offen (A3, B2 -- beide nur Mehrspieler, ehrlich als offen markiert). Die Nachbesserung hat nichts
kaputt gemacht, was den SP-Test stoert; drei neue kleine Restbefunde (N1-N3), alle nicht SP-relevant oder nur Anzeige-Verzoegerung.

## 2. Je Befund (Code gelesen, Zeilen = Staging `mod/42/media/lua/...`)

| ID | Urteil | Beleg im heutigen Code |
|---|---|---|
| B1 | geschlossen | `client/BanditsNPCBearClient.lua:212` sendet `{ v = 1 }`; `server/BanditsNPCBearServer.lua:395` `args == nil -> {}`; `:800` pusht auch beim ersten Takt (`B._sig[uid] ~= sig`). Vanilla-Beleg fuer "leer = nil": `server/ClientCommands.lua:1349` (`if args then`). Keine neue Engine-Methode. |
| A1 | geschlossen | `server/BanditsNPCBearWorld.lua:252-255` `animal:remove()` dann `if isServer() then removeAnimal(animal:getOnlineID()) end` -- selbst nachgelesen: genau so `shared/Definitions/animal/ButcheringUtil.lua:609-614` (Zahl als Argument). MP ungespielt. |
| A2 | geschlossen | Feed `:98-112`, Pet `:98-112`: `serverStart` sperrt, `serverStop` loest, `complete()` ruft den Kern und loest danach; Form `ISMilkAnimal.lua:168-169, :195-196, :211-212` (selbst gelesen). SP: `perform` loest wie vorher, `complete` loest noch einmal (harmlos). |
| A3 | teils offen (zu Recht) | `findBreed` jetzt `AnimalDefinitions.getDef(B.CUB)` + `def:getBreedByName(B.BREED)` (`World.lua:208-212`) -- selbst nachgelesen `server/ClientCommands.lua:808` (Server, direkt vor `addAnimal`) und `ButcheringUtil.lua:79/85` (mit nil-Pruefung). `getObjectListForLua`, `getAnimalID`, `isRotten`/`isBurnt` am Server: kein Server-Beleg, im Kommentar `World.lua:275-276` als MP OFFEN markiert. Die Ablehnung "eiserne Regel verlangt keine gleiche Seite" ist vertretbar (Werkstatt-CLAUDE.md 3 nennt Argumenttypen, nicht Seite); das MP-Risiko bleibt Testpunkt. |
| A4 | geschlossen | Kommentare `Registry.lua:150, :181, :187, :403`, `Server.lua:145-148, :832` nennen jetzt shared-Fundstellen. |
| A5 | geschlossen | `client/NCBearBenchCub.lua:340-343`, `:350-353` pruefen `B.IsSP()` zuerst. |
| A6 | geschlossen | `baer_uebernahme.py:178` Regel `altmenue` (`\bNCBearMenu\b|\bNCBearBench\w*`). Echtes Staging trifft sie nicht (Trockenlauf 0 Funde). Gegenprobe des Bauers nicht wiederholt. |
| A7 | geschlossen | selbst gegreppt: NC `42/media/lua` `NOT_TENDED` = 24 Treffer in 9 Dateien -- stimmt mit `BanditsNPCBearCrew.lua:10` und `NAEHTE.md:24`. |
| A8 | zu Recht unveraendert | gewollt (Plan 6.5); Testpunkt im SP: Junges treffen/toeten, Konsole auf Ton-Warnungen. |
| A9 | geschlossen | grep "werkbank/bench/spawn/debug/cheat" in den 14 echten Dateien: nur noch Fundstellen-Pfade (`BanditServerSpawner.lua`, `DebugContextMenu.lua`) in Kommentaren, vom Skript erlaubt; Trockenlauf 2 statt 3 Warnungen. |
| A10 | geschlossen | `baer_uebernahme.py:103-104`; Probe schreibt 40 Dateien (nur `NCBear_Eat.xml` als Knoten). |
| B2 | teils offen | `Registry.lua:123-135` `B.CountWild(online)`; `Server.lua:113`, `:511` uebergeben die Online-Menge. Der Welt-Deckel ist damit frei. Offen (Kevin-Frage, s. N3): Eintraege Abwesender bleiben fuer immer. |
| B3 | geschlossen, mit Schwaeche N1 | `Server.lua:720-741`: `fed` erst nach `missScans` UND `fedMissH` (1 h); `liveRec` setzt `missAt = nil` (`:655`). |
| B4 | geschlossen | `Server.lua:229, :239-244`: am zahmen Jungen `Note_Happy`, Stueck weiter genau einmal (`takeOne` vor der Gutschrift). |
| B5 | geschlossen | `Server.lua:749-761`: reifer Platz verfaellt nach (Naechte + 4 + 1) x 24 h ab `t0` (`t0` gesetzt in `Registry.lua:377`). Abweichung vom Plan-Wortlaut, in `nachbesserung.md` genannt. |
| B6 | geschlossen, mit Schwaeche N2 | Server `:696-715`, `:817-823` (vermisste Zahme nur je 30 s); HUD `:226-245` dritte Stufe 30 s. |
| B7 | geschlossen | `Rules.lua:311-313`: fed/tame mit `mate.dist < reach` -> `hold`. `mate` ist nur bond/Besitzer (`Server.lua:598-601, :619`). Folge: steht der Besitzer naeher als 3 Kacheln, wandert das Junge nie -- gewollt, unschaedlich. |

## 3. Selbst laufen lassen (Zahlen)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (15 Lua) | 15 file(s) checked, 0 failed |
| `scopecheck.py` (15 Lua) | 15 file(s), 0 violation(s) |
| `luacheck_pz.py` (15 Lua) | 11 x W113, alle erwartet: 3 Aktionsklassen `BanditsNPCBearMenu.lua:81/92/102`, 8 in der Bench (`NCBear_Cub*` :380-384, `NCBearMenu` :386-388) |
| `localcount.py` (je Datei) | hoechstens 39 aktiv (`NCBearBenchCub.lua` Fkt. ab :308) / 42 insgesamt (`ISUI/BanditsNPCBearHud.lua` Fkt. ab :183); Grenze 200 |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` | **261 bestanden, 0 Fehler** |
| Kern- / Oberflaechen-Attrappe | 133/0 / 113 ok, 0 Fehler |
| Pruefer-B-Attrappe | 1a 1b 1c 2b 3a 3b 3c OK, 2a BEFUND (gewollt: Eintraege Abwesender bleiben, B2) -- die Fall-Texte beschreiben noch den alten Fehler, die Ergebnisse den neuen Stand |
| Trockenlauf ohne Schalter | NICHT OK -- 24 Fehler (genau die 24 Altlasten), 2 Warnungen (erwartet rot) |
| Trockenlauf `--vor-b5a` | OK -- 0 Fehler, 26 Warnungen |
| Probe `--probe <scratchpad>/probe --staging ... --vor-b5a` | OK -- 0 Fehler, 26 Warnungen; 40 Dateien geschrieben; 14 Lua luacheck/scopecheck/localcount ok (hoechstens 42); luacheck_pz 0 Treffer + 3 erlaubt; Sandbox 42 + 19 Optionen |
| `staging_dateien.txt` gegen Platte | 40 Eintraege = 40 Dateien, 0 MD5-/Groessen-Abweichungen, keine Datei nur auf einer Seite |
| Ueberschreiben in der Test-Mod | gegen `Zomboid/mods/NCBearTest` (ohne `.git`, auch ohne Gross/Klein): **nur** `42/media/lua/shared/Translate/EN/IG_UI.json` existiert schon; neue Datei behaelt die 4 alten Schluessel wortgleich (selbst verglichen), dazu 2 neue sortiert. Die Test-Mod hat kein `sandbox-options.txt` und keine anderen Translate-Dateien. |
| Texte | 7 Sprachen: UI 74 / Sandbox 44 Schluessel je Sprache gleich, Platzhalter `%1 %2 %%` je Schluessel gleich, Round-Trip gleich, kein BOM, LF. `%%` ist Vanilla-Form (`IG_UI.json:439` "Fuel: %1%%"). |

Hinweis Trockenlauf: die NPC-Crew-Kommentarstelle wanderte von `BanditsNPC.lua:1356` auf `:1357` (NPC Crew wird parallel gebaut) -- keine Kollision.

## 4. Eigene Stichproben (bisher von niemandem gemacht)

**S1 -- Fuettern im Mehrspieler Zeile fuer Zeile.** Client: `Menu.lua:72-83` (Queue leeren, `equip`, `walkAdj(..., true)`, Aktion) ->
Server baut die Aktion aus `character/animal/food` -> `serverStart` sperrt (`FeedAction.lua:98`) -> `complete` -> `B.FeedComplete`
(`Server.lua:209`): `handCheck` (Art, `isExistInTheWorld`, `isDead`, `DistTo < 3`, `B.RecOf` ueber Sitzungs-Objekt/Spiegel/`aid`) ->
`B.CheckFeed` mit `B.SlotsOf(Benutzername)` -> `contains(food)` am Server-Inventar -> `B.FoodClass` (hier `isRotten`/`isBurnt` am Server:
A3 offen) -> `takeOne` (drei Vanilla-Aufrufe, danach `contains` muss falsch sein) -> `ApplyGain` -> `Commit` (Spiegel nur am Server-Tier,
nie uebertragen) -> `B.Tell` = `sendServerCommand(...,"Note")` -> `FlushViews` -> `Sync` an alle in 60 Kacheln -> `complete` loest die
Sperre. Client: `ApplySync`, Balken ueber `byOid[getOnlineID()]` (Spiegel fehlt am Client-Tier, das ist gewollt). Kein Weg, auf dem ein
Gegenstand doppelt oder ohne Gutschrift verschwindet; jede Ablehnung vor `takeOne` laesst das Stueck liegen. Kein Befehl braucht ein Recht
ausser `LoginOnServer` (Fuettern ist eine Zeitaktion, kein Befehl). Ergebnis: stimmig; Laufzeit (Neubau der Aktion mit IsoAnimal-Feld) ungeprueft.

**S2 -- Spanisch (ES/UI.json) ganz gegengelesen**, 74 Zeilen: alle sinnvoll und vollstaendig, Platzhalter an der richtigen Stelle,
Genus passt zu "cria" (timida, lista, domada), "al %1" passt zu allen acht Richtungen (al norte / al noreste ...). Kein Fehler.

**S3 -- Sandbox-Option `BearCubsEnabled = false`** (Code durchgerechnet): Wald-Wurf endet sofort (`Server.lua:502`); Bench
`NCBear_CubHere` -> `B.AppearFor` -> `B.MayAppear` lehnt mit `Why_Off` ab (`Rules.lua:191`) und sagt "no cub: Bear cubs are switched off
...". Vorhandene Junge bleiben fuetter- und streichelbar (`CheckFeed`/`CheckPet` fragen den Schalter nicht -- wie Plan 3.1 Nr. 1).
Koeder auslegen: `Why_Off` (`Rules.lua:178`), Welt-Menue zeigt den Punkt gar nicht (`Menu.lua:311`). Reifer Koeder: verfaellt mit
`Bait_Expired` (`Server.lua:765-768`). Nichts haengt, nichts geht verloren. Nebenbefund: `BearTamePetPoints = 0` meldet "+0 trust".

## 5. Neue Restbefunde der Gegenpruefung

- **N1 (minor, ungeprueft):** `missAt`/`missN` werden nur in `liveRec` zurueckgesetzt (`Server.lua:654-655`), nicht, wenn die Gegend
  entladen ist. Zaehlt ein Suchlauf beim Weggehen 1-2 Fehlversuche (Tier schon weg, Kacheln noch da), steht `missAt` Tage spaeter noch
  -- beim Wiederkommen greift die 1-h-Frist von B3 dann nicht, das angefuetterte Junge kann nach 1-2 Suchlaeufen wieder "lost" sein.
  Ob Tiere und Kacheln beim Entladen getrennt gehen, ist ungeprueft. Abhilfe: in `countMisses`/`resolve` bei nicht geladener Gegend
  `missN = 0, missAt = nil`.
- **N2 (minor, nur Anzeige):** HUD setzt bei neuer Sicht `scanMiss = 0`, aber nicht `S.scanAt` (`Hud.lua:195-200`). War schon die
  30-s-Stufe erreicht, erscheint der Balken nach dem Zurueckkommen bis zu 30 s spaeter. Der Kommentar `:36-38` ("geht wieder schnell")
  stimmt so nicht ganz. Abhilfe: bei `wasDirty` auch `S.scanAt = 0`.
- **N3 (minor, nur MP, Kevin-Frage B2):** Eintraege Abwesender bleiben; der harte Deckel `B.CountRecs() >= maxRecs` (64) in
  `B.AppearFor` (`Server.lua:113`) zaehlt sie weiter. Je Spieler hoechstens ein wildes/gebundenes + seine zahmen, also erst bei rund
  30+ verschiedenen, nie wiederkehrenden Spielern -- dann erscheint fuer niemanden mehr ein Junges.
- **N4 (Doku):** `PLAN_ZAEHMEN.md` nicht nachgezogen (6.2.6 "Hello {}", 6.2.7/FE 8.2 "Server ruft nur complete()", B3 1 h, B5-Frist,
  B2-Deckel). Steht in `nachbesserung.md` und `schnittstelle_aenderungen.md`; vor B1b in den Plan uebernehmen.

## 6. Was nur das Spiel zeigen kann

Laedt die neue Art (GLB-Platzhalter, `NCBearCub_Body`, Textur) ohne rote Zeile; erscheint unser Rechtsklick am Jungen und ist "Kill"
weg; sieht die Streichel-Haltung `"lamb"` bei Groesse 0,35 brauchbar aus; haelt `setBlockMovement` das nicht wilde Junge waehrend der
Aktion; rennt `fleeTo` wie gedacht (Flucht, Neugier, Mitlocken); `%%` in "Taming 21%"; Balkenhoehe `barZ`; steht das Junge nach
Speichern/Laden wieder da und findet der Suchlauf es (Spiegel/`aid`); `setHealth(0)` (Bench) wird als Tod erkannt; Konsole bei Tod
(A8, fehlende Toene). Im MP zusaetzlich: A1 (kein Geistertier), A2 (Junges steht am Server), A3 (vier Server-Aufrufe), B1 (Neuverbinden),
Neubau der Zeitaktionen am Server, OnlineID nach Neuladen.

Statisch geprueft, nicht gespielt.
