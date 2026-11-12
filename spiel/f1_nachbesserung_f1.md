# Lauf baer-f1: NACHBESSERUNG (Befunde pruef_f1_a.md A1-A8, pruef_f1_b.md B1-B10)

Stand 12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Geaendert nur im Staging `_arbeit/baer_zaehmen/mod/` (19 Dateien:
12 Lua, 7 UI.json), im Werkzeug `ober_werkzeug/texte_f1.py`, in `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, in Attrappen/Pruefern
unter `attrappe/` (gewollte Erwartungen, neue `attrappe/nach_f1/`), `f1_entwurf/fenster_gebaut_*.png`, `staging_dateien.txt`,
`schnittstelle_aenderungen.md` (Abschnitt "F1 NACHBESSERUNG"). Nichts in der Test-Mod, NPC Crew, Vanilla, Bandits; kein git, kein Spiel.
Stand VOR der Nachbesserung als Kopie fuer die Gegenproben: Scratchpad `.../scratchpad/vor/` (mod, attrappe, Werkzeuge).

## 1. Je Befund

| ID | nachgeprueft | Entscheidung / Aenderung |
|---|---|---|
| **B1** major | bestaetigt: `revN` zaehlte nur Suchlaeufe und wurde beim Entladen nie zurueckgesetzt (Order.lua alt :358-361); mit `need` Suchlauf je 5 s (Server.lua :971-972). Pruefer-Attrappe `pruef_f1/c1_wartefrist.lua`: alt 2 Befunde | **behoben.** Frist = Zeit: neuer Koerper erst bei `revN >= reviveScans` UND `ms - revAt >= reviveMs` (60 s) UND nicht im Heil-Fenster (`B._healUntil`) -- `S:server/BanditsNPCBearOrder.lua:354-424` (Zeile 394). Frist neu bei: Eintrag passt nicht (Gegend entladen, Besitzer offline, AnimalID gesehen), Luecke > `reviveGapMs` 50 s, Uhr rueckwaerts; `resolve` vergisst die Frist je Takt, wenn die Gegend NICHT geladen ist (`S:server/BanditsNPCBearServer.lua:845`, neu `B.ReviveForget`, Order.lua:349). Deckel "ein Koerper je Takt" ueber `made` (die anderen Vermissten zaehlen weiter -- sonst begaenne ihre Frist durch die Luecke neu). Kein Engine-Aufruf. `c1_wartefrist.lua` jetzt 0 Befunde (`pruef_f1/c1_wartefrist_ergebnis_nach.txt`); `nach_f1/kern.lua` N1a-f gruen (mit need: 60-75 s statt 10 s; erster Suchlauf nach dem Neuladen: kein Koerper, erst >= 60 s danach; Heil-Fenster; offline; Luecke; zwei Vermisste). Gesamt-Attrappe 21j: C1 jetzt 62,4 s statt 32 s nach "vermisst". |
| **B2** major | bestaetigt: `V:client/Vehicles/ISUI/ISVehicleMenu.lua:777-800` (jedes Tier in 6 Kacheln, nur Platzfrage); `canAddAnimalInTrailer` = Kapazitaet >= belegt + `getAnimalTrailerSize` (Jar `attrappe/pruef_f1/jar/BaseVehicle.txt:37653-37667`), `= trailerBaseSize x Groesse` (`dec/IsoAnimal.java:2794-2796`); Anhaenger hoechstens 500 (`V:scripts/generated/vehicles/vehicle_trailer_livestock.txt:51`, `..._horsebox.txt:51`, keine anderen). Selbst gesucht (ganzes Jar, Python zipfile): `IsoAnimal.getAnimalTrailerSize` rufen nur `BaseVehicle` (canAdd, Summe im Anhaenger) und `AnimalCommandPacket` (Ein-/Ausladen); Lua nur `ISVehicleMenu` (Anzeige) und `ButcheringUtil.lua:45` (Leiche) | **behoben (reine Daten):** `trailerBaseSize = 100000` fuer beide Arten (`S:shared/BanditsNPCBearDefs.lua:104`, `:190`). Vanilla graut "zu gross" aus (ISVehicleMenu.lua:796-800). Nebenwirkung: auch eine Baeren-LEICHE passt in keinen Anhaenger (gewollt). NPC Crew/Bandits nennen trailerBaseSize nicht (grep 0). **Kevin-Frage** (Empfehlung gebaut: kein Anhaenger, er faehrt wie die Crew im Auto mit). |
| **B3** major | bestaetigt mit `pruef_f1/sitz_treiber.lua` (alt 3 Befunde): Treiber verwarf bei busy den Eintrag (Pose.lua alt :53-56), schrieb in Phase "sit" nie wieder | **behoben** (`S:client/BanditsNPCBearPose.lua`): bei busy UND waehrend DIESES Spiel selbst fuettert (`U.PoseHands`, :64, gerufen aus `S:shared/TimedActions/BanditsNPCBearFeedAction.lua:65/:77` hinter `B.UI and B.UI.PoseHands` -- nur Client/SP) Eintrag behalten, nichts schreiben; danach: Fuetter-Aktion hat `B.ACT` geloescht -> neu "sitdown" (bzw. fertig, wenn er nicht mehr sitzen soll, :103); nach dem Streicheln direkt "sit" (kein Hinsetz-Clip, :114); in Phase "sit" alle 2 s `setVariable(B.ACT, "sit")` (:130, heilt fremdes clearVariable). Nur belegte Aufrufe (ISPetAnimal.lua:43/:48). Deckel H <= 8, je Eintrag hoechstens 30 s. `sitz_treiber.lua` jetzt 0 Befunde; `nach_f1/ober.lua` B3 (inkl. ECHTER Fuetter-Aktion start/release) gruen. |
| **B4** minor | bestaetigt (Z2): SetMode liess `s.ownUntil` laufen, Regel 32/36 "keep" | **behoben**, aber NICHT mit dem Vorschlag "s.ownUntil = nil": dann haelt die Laerm-Wache im SP einen noch rennenden Baeren ohne eigenen Befehl fuer eine Flucht (`S:server/BanditsNPCBearGuard.lua:203-227`, Fall b "run") und antwortet mit einem Ersatzweg. Stattdessen merkt `B.SetMode` fuer stay/sit/roam `s.ownCut = s.ownUntil` (Follow.lua:127); `ownLive` in Order.lua:51 zaehlt nur nicht abgeschnittene Wege (ein neuer `B.MoveTo` gilt wieder). `B.HandleMode` setzt die Heimat auf die Kachel von JETZT (`floor(a:getX/getY)`, Follow.lua:301; sonst bis 1,5 s alt -> bis ~4 Kacheln zurueck) und haelt sofort an (`B.Hold`, :305). `nach_f1/kern.lua` N3 gruen (vorher "back 35"/"keep 36"). |
| **B5** minor | bestaetigt (Order.lua:341-357; Win_PassiveTip ehrlich) | **behoben**, 7 Sprachen (`texte_f1.py`, U.EN): `Win_HintMissing` "No body now. It can come back while you are near, or use Unstuck." (bewusst NICHT der laengere Vorschlag: die Fusszeile bestimmt die Fensterbreite mit -- `Window.lua:171`; so bleibt das Fenster gleich breit, `pruef_f1/kopf_lage_ergebnis_nach.txt`: 1x/2x unveraendert, 4x-Schrift auf 1080 sogar 34 px schmaler); `Note_PassiveOn`/`Big` "... is passive now. It keeps out of fights once bears can fight (comes later)." CN nur Vanilla-Zeichen (Pruefer 0 fremde). |
| **B6** minor | bestaetigt (WinData alt :429/:434; im Bild sichtbar) | **behoben:** Tooltip des grauen Unstuck-Knopfs mit derselben m:ss-Uhr: neu `UI_BN_Bear_Win_CallWaitClock` (+Big) "You can call your cub/bear again in %1." in 7 Sprachen (`S:client/BanditsNPCBearWinData.lua:438`); das Rechtsklick-Menue behaelt `Why_CallWait`. `fenster_gebaut_1080.png` / `_4k.png` neu gemalt (nur die Tooltip-Zeile anders, `attrappe/f1_ober/zeichnung.txt` sonst gleich). |
| **B7** minor | bestaetigt (Key.lua:112; isKeyConsumed) | **so gelassen** (Empfehlung beider Pruefer) -> Kevins Testliste + Frage. |
| **B8** minor | bestaetigt (`f1_ober/zeichnung.txt`: 4K ~300 Zeichenaufrufe, nur bei offenem Fenster) | **nicht umgesetzt:** optional, keine Optik-Wirkung, spart je Bild hoechstens ~50 Aufrufe (nur leere Segmente bei t = 2); Risiko einer sichtbaren Aenderung an den Faehigkeits-Segmenten ohne Nutzen fuer Kevin. Vertretbar laut Pruefer B. |
| **B9** minor | bestaetigt: `V:client/ISUI/ISUIHandler.lua:35-57` oeffnet das Radial beim DRUECKEN; `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1170-1176` "Kill" fuer jedes nicht wilde Tier mit Waffe; unser Rechtsklick blendet es aus, das Radial nicht | **behoben** (`S:client/BanditsNPCBearKey.lua:81` `onRadialKey`): an `Events.OnKeyStartPressed` (Form `ISUIHandler.lua:35/:102`), `Events.OnKeyKeepPressed` (Form `V:client/Hotbar/ISHotbar.lua:782/:890`) und im `onKey` (Loslassen) -- nur die Radial-Taste, nur wenn ein Radial offen ist, nicht am Auto, nur an UNSEREM Baeren (eigen / ohne Besitzer / unbekannt) -> `menu:undisplay()`. Gilt auch, wenn "Bear window" umgelegt ist. Unser StartPressed laeuft VOR Vanillas (das meldet sich erst in OnGameStart an) -- darum KeepPressed: hoechstens ein Bild sichtbar. Weiter genau EIN OnKeyPressed-Haken. Kosten: je Bild nur, solange die Taste gehalten wird, zwei billige Fragen. |
| **B10** minor | bestaetigt (Key.lua ohne Riegel; Window typing nur in isKeyConsumed) | **behoben:** neu `U.WinTyping()` (`S:client/ISUI/BanditsNPCBearWindow.lua:672`), `onKey` tut nichts, solange Chat oder das Namensfeld offen ist (Key.lua:97). |
| **A1** minor | bestaetigt (Regel sah `setWantKeyEvents`, `onKeyRelease`, `isKey("Name")`, rohe Codes nicht) | **behoben** (`baer/tools/baer_uebernahme.py` Regel `taste`): + `setWantKeyEvents(`, `[:.]isKeyConsumed`, `[:.]onKey(Press|Release|Repeat)`, `:isKey(`, `table.insert(keyBinding`, `key == <Zahl>`. `CHEAT_ALLOWED` 3 -> 14 Tasten-Stellen (je Datei/Regel/Code/Grund; alle greifen, keine Warnung "greift nicht"). Gegenprobe `attrappe/uebernahme_f1/probe_regeln_f1.py` + 5 Faelle (setWantKeyEvents in Tags.lua, onKeyPress mit Code, isKey mit fremdem Namen, roher Code, neue keyBinding-Zeile): **15 von 15**. NAEHTE.md Ausnahmen-Tabelle + Absatz. |
| **A2** minor | bestaetigt (`ours = B.BodyKind(an) ~= nil`) | **behoben:** `bearKind` (Key.lua:63): Sicht kennt das Tier und der Besitzer ist gesetzt und nicht ich (`U.WinMine`, WinData.lua:198) -> "foreign": wie ein fremdes Tier (Vanillas Radial bleibt, kein Fenster, Key.lua:118). Eigener Baer (jeder Zustand, auch das Junge im Zaehmen -> Hinweis "no bear yet"), Baer ohne Besitzer und unbekannte unserer Art -> wie bisher (Radial zu, Fenster). Nebenpunkt (offenes Fenster verbraucht V) -> Testliste. |
| **A3** minor | bestaetigt (handCheck ohne bd) | **behoben:** `tellWhy(..., bd)` (Server.lua:48); `handCheck` gibt `B.BodyKind(animal)` mit (:164, :175); zusaetzlich geben `B.FeedComplete`/`B.PetComplete` `rec.body` an die Absagen aus CheckFeed/CheckPet (:227, :278; der Client nimmt Big nur, wo es eine Fassung gibt). `nach_f1/kern.lua` N4 gruen. |
| **A4** minor | Abweichungen sind begruendet (PLAN_F1.md 0.2/0.3) | **nichts geaendert**; Kevin-Fragen F1/F2 ganz oben (Abschnitt 4). |
| **A5** minor | bestaetigt (WinData.lua:187 nur tame/missing) | **nicht gebaut** (Auftrag); Kevin-Frage mit Empfehlung. |
| **A6** minor | bestaetigt | **behoben:** Kommentare Order.lua :16 / :172 / :398 jetzt `V:server/Map/SGlobalObjectSystem.lua:89` (`square:getX(), square:getY(), square:getZ()` in einem Server-System). |
| **A7** minor | bestaetigt (6 Gen-Dateien in NCBearTest seit 12.11. 01:02) | **erledigt:** Trockenlauf und Probe nach der Nachbesserung neu: `trockenlauf_f1_nach.txt`, `trockenlauf_f1_nach_vor_b5a.txt`, `probe_f1_nach_ausgabe.txt`; Kopf von `staging_dateien.txt` vermerkt das. Direkt vor dem Einbau noch einmal laufen lassen (Test-Mod kann sich wieder aendern). |
| **A8** minor | Begruendung nachgelesen (Pruefer A) | **so gelassen**; Testliste (4K mit "Max. Texturgroesse 256"). |

## 2. Pruefungen nach der Nachbesserung (alle selbst gelaufen)

| Pruefung | Ergebnis |
|---|---|
| Vier Lua-Pruefer, 32 Lua-Dateien | luacheck 32 / 0 failed; scopecheck 0; localcount hoechstens **51 aktiv** (Hud :1) / **77 insgesamt** (World :699) -- unveraendert; luacheck_pz **20 x W113** = die bekannten (17 Bench, 3 Aktionsklassen Menu.lua :93/:104/:114); luac5.1 -p 0 Fehler |
| Form | 32 Lua LF/ASCII/LF am Ende/kein BOM; 21 JSON Round-Trip, sortiert, kein BOM/CR; 2 txt ASCII/LF -- 0 Abweichungen |
| Texte | UI.json **276** je Sprache (+2), Big-Fassungen EN 28; `texte_pruefen.py`/`_b1b`/`_b1c`/`_b1d`/`_b1e` je 0, `texte_pruefen_f1.py --tmp` **0** (Werkzeug == Staging, 22 Dateien), CN 0 Zeichen ausserhalb Vanilla-CN; Belege `belege.py` 0/112, `_b1b` 0/51, `_b1c` 0/89, `_b1d` 0/23, `_b1e` 0/53, `belege_f1.py` 0 (97 V:-Fundstellen); `bilder_pruefen_b1e.py --tmp` 0 |
| Attrappen | kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1e_kern 153/0 (je byte-gleich `ergebnis_f1.txt`), b1d_kern 162/0 (nur Pfad-Vorsatz, bekannt); **f1_kern 189/0** (neu gespeichert, +1 Pruefung); ober 116/117, b1b_ober 144/134, b1c_ober 155/142, b1d_ober 174/176, **b1e_ober 231/231**, **f1_ober 359/359** -- je 0 Fehler; **gesamt 2329/0** (neu gespeichert; einzige Zeile anders: "C1 wieder da 39 Hirn-Takte (62,4 s)" statt 20 (32 s)); nach_b1e 31/0, pruef_b/b1b/b1c/b1d wie gespeichert; pruef_b1e `run_nach` 25/0, `run` 20/5 (bekannt seit B1e) |
| **neu `attrappe/nach_f1/kern.lua`** (B1, B2, B4, A3) | **28 / 0**; gegen den Stand VOR der Nachbesserung **11 / 17** (`ergebnis_kern_vor.txt`, jeder Fall rot) |
| **neu `attrappe/nach_f1/ober.lua`** (A2, B9, B10, B6, B5, B3 mit echter Fuetter-Aktion; aus `attrappe/f1_ober`) | **33 / 0**; vorher **14 / 19** (`ergebnis_ober_vor.txt`) |
| Pruefer-B-Attrappen | `c1_wartefrist` 0 Befunde, `sitz_treiber` 0 Befunde (`*_ergebnis_nach.txt`; die Originale der Pruefer bleiben), `kopf_lage` weiter 1 Grenzfall 1 px (1080, Schrift 4x), 1x/2x byte-gleich |
| `xref_f1.py` | **0 Luecken**, 3 Hinweise (bekannt); 194 CFG-Felder (+2), U.* 55 (+3), B.* 218 (+1) -> `xref_f1.txt` neu |
| `gegenprobe_f1.py` | **27 von 27** erkannt (`gegenprobe_f1.txt` neu) |
| `probe_regeln_f1.py` / `probe_regeln_b1e.py` | **15 von 15** (neu 5 Tasten-Faelle) / 8 von 8 (byte-gleich) |
| Trockenlauf `--staging mod --vor-b5a` | **OK -- 0 Fehler, 31 Warnungen** (27 Altlasten + 2 ALT_DEFS + Clip-Warnung + NC-Kommentar); Cheat-Pruefung Funde 0, 14 Tasten-Ausnahmen alle benutzt |
| Trockenlauf ohne `--vor-b5a` | **29 Fehler = 27 Altlasten + 2 ALT_DEFS**, sonst nichts |
| Probe `--probe probe_f1 --staging mod --vor-b5a` | **OK -- 0 Fehler, 31 Warnungen**, 70 Dateien; Pruefer je kopierter Datei gruen (localcount hoechstens 77), luacheck_pz 0 + 3 erlaubt; Gesamt-Attrappe gegen die Probe **2329 / 0, byte-gleich** mit dem Staging-Lauf (`ergebnis_probe.txt` neu) |
| `staging_dateien.txt` neu | **67 Dateien: 7 neu, 32 ueberschreibt, 28 gleich** (gegen NCBearTest); in der Nachbesserung geaendert 19 (Lua: Client, Key, Pose, WinData, Window, Bench, Follow, Order, Server, BanditsNPCBear, Defs, FeedAction; 7 x UI.json) |
| Fenster-Bilder | `f1_entwurf/fenster_gebaut_1080.png` / `_4k.png` neu (Tooltip "You can call your bear again in 3:12."); Masse unveraendert (640 x 615 / 1280 x 1178) |
| Namen | neue Namen (`ReviveForget`, `reviveMs`, `reviveGapMs`, `ownCut`, `PoseHands`, `WinTyping`, `WinMine`, `CallWaitClock`) in NPC Crew `42/media/lua` und Landkarte: 0 Treffer |

## 3. Neue Zahlen
| Feld | Wert | Wofuer |
|---|---|---|
| `B.CFG.reviveMs` | 60000 | C1 erst nach 60 s Echtzeit in geladener Gegend mit Besitzer (B1) |
| `B.CFG.reviveGapMs` | 50000 | groessere Luecke zwischen zwei passenden Suchlaeufen -> Frist neu (B1) |
| C1 im Spiel (geplant) | ~60-90 s nach "vermisst", nie in den ersten 2 min nach dem Laden | vorher 10-60 s |
| `trailerBaseSize` | 100000 (beide Arten; vorher 100 / 300) | nie in den Tier-Anhaenger (B2) |
| Sitz-Treiber | `SIT_RENEW_MS` 2000, `HANDS_MS` 30000, `HANDS_MAX` 8 | "sit" nachsetzen / Deckel der eigenen Fuetter-Aktion (B3) |
| Tasten-Ausnahmen | 3 -> 14 | Uebernahme-Regel sieht Fenster-Tasten (A1) |

## 4. Fragen fuer Kevin (Nachtschicht -- gebaut ist jeweils die Empfehlung)
1. **(A4/F1)** "Komm her" und "Unstuck" sind zwei Knoepfe: Komm her geht ohne Abklingzeit zu dir, Unstuck (= Call to me) hat die 5 min mit
   Restzeit. So lassen? (Empfehlung: ja.)
2. **(A4/F2)** "Frei herumlaufen" Vorgabe 12 Kacheln statt 8 (dein Bleiben-Radius 12; mit 8 rannte das Junge in B1b grundlos heim). Ok?
3. **(B2)** Baer in Vanillas Tier-Anhaenger? Gebaut: **nein** ("zu gross"), er faehrt wie die Crew im Auto mit -- sonst gaebe es nach dem
   Ausladen einen zweiten Baeren.
4. **(B1)** Baer ohne Koerper kommt von selbst wieder: jetzt nach ~1-1,5 min in deiner Naehe, nie in den ersten 2 min nach dem Laden. Ok?
5. **(A5)** Zaehm-Fortschritt im V-Fenster, solange du das Junge noch zaehmst? (Empfehlung: ja, spaeter als kleiner Hinweis "Taming: 40%"
   statt "You do not have a bear yet." -- nicht in F1.)
6. **(A2)** V an einem FREMDEN Baeren (Mehrspieler): gebaut wie bei jedem fremden Tier -- Vanillas Radial, nicht dein Fenster. Ok?
7. **(B9)** Vanillas Tier-Radial (V) an deinem Baeren geht sofort wieder zu (dort gab es "Kill"). Dafuer fehlt dort Vanillas "Animal info"
   -- im Rechtsklick-Menue ist es weiter da. Ok?
8. **(B7)** Im Auto gehoert V dem Fahrzeug-Radial: das Baeren-Fenster im Auto nur, wenn es vorher offen war (oder mit anderer Taste). So lassen?

## 5. Kevins Testliste (zusaetzlich zu PLAN_F1.md 8.4)
- Sitzenden Baeren streicheln: bleibt sitzen (kein erneutes Hinsetzen). Sitzenden Baeren fuettern: frisst, setzt sich danach wieder hin.
- Folgenden Baeren mitten im Lauf "Sit"/"Stay": bleibt sofort stehen bzw. setzt sich, kein Weiterrennen.
- V neben dem eigenen Baeren mit Waffe in der Hand: kein Tier-Radial (hoechstens ein Bild), Fenster geht auf.
- Fenster offen, im Auto V druecken: erster Druck schliesst das Fenster, zweiter oeffnet das Fahrzeug-Radial (B7, gewollt).
- Namensfeld im Fenster offen, daneben klicken, V: Fenster bleibt offen.
- 4K mit "Max. Texturgroesse 256": Kopf-Symbol und Markierungs-Pfeil scharf? (A8)
- Koerper weg (`NCBear_CubBodyGone()`): ~1-1,5 min spaeter genau EIN Baer; weggehen und wiederkommen: kein zweiter. Tier-Anhaenger: Baer ist
  "zu gross".

## 6. Ungeprueft
Alles Laufzeit-Verhalten: ob `setVariable(B.ACT, "sit")` mit gleichem Wert den Clip wirklich NICHT neu startet (Lesart: gleiche Bedingung,
kein Uebergang -- im Spiel ansehen), ob OnKeyKeepPressed im Bild nach dem Druecken kommt (Vorbild ISHotbar/ISFastTeleportMove), ob
`setBlockMovement(true)` einen laufenden `fleeTo` sofort stoppt (Vorbild Fuettern/Streicheln), die Dauer des Tier-Laders nach dem Neuladen
(die 60 s-Frist ist eine Annahme), Anhaenger-Menue mit "zu gross". Nach dem Einbau (erst wenn Kevins Spiel zu ist) das Spiel neu starten.
Statisch geprueft, nicht gespielt.
