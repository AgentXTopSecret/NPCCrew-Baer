# Lauf baer-kampf -- GEGENPRUEFER

Stand 14.11.2026 ~08:00. **Statisch geprueft, nicht gespielt.** Keinem Bericht geglaubt: jeder Befund am Code, alle Pruefer, Attrappen, die Simulation,
langcheck, Trockenlauf und `--probe` selbst neu gelaufen. Kevins Worte: `baer/begleiter/ENTSCHEIDUNGEN.md:642-684` (Punkte 1-8). Kuerzel: `S:` =
`_arbeit/baer_zaehmen/mod_kampf/42/media/lua/`, `G:` = `_arbeit/baer_zaehmen/attrappe/kampf_gegen/` (meine Laeufe), `V:` = Vanilla `media/lua/`,
`B22:` = Bandits 42.22 `media/lua/`, `J:` = Jar 42.22 `kampf/jar/dec/zombie/`.
Geschrieben habe ich nur: diesen Bericht, `kampf/gegen/` (Trockenlauf, Probe), `attrappe/kampf_gegen/` (Laeufer-Kopien mit eigenem TMP, eigene
Simulation `sim_gegen.lua`, Ausgaben) und 7 kleine Berichtigungen in `kampf/anleitung_entwurf.md` (Abschnitt 7). Kein Byte in Staging-Code, Test-Mod,
NPC Crew, Vanilla, Bandits (Test-Mod und NPC Crew: keine Datei neuer als 05:21 heute). Kein Download, kein Spielstart. Ehrlich: ich habe lesend
`git log` / `git show` / `git diff` benutzt (Stand der Test-Mod, Aenderungen an `NAEHTE.md` / `baer_uebernahme.py`), nichts geschrieben.

## 0. Ergebnis zuerst

* **Bereit fuer Kevins Einzelspieler-Test: JA.** Kein Blocker. Alle 7 major (C1, C2, C3, S1, S2, S3, S4) am Code geschlossen und in Attrappe /
  Simulation nachgewiesen; C4, C6, C7, C8, C10, S6 geschlossen; C5, C9, S5, S7, S8 ehrlich als Frage / Testpunkt gefuehrt (kein Code, richtig so).
* **Nichts kaputt gefunden:** K1-Attrappen (k1_kern 153/0, k1_pruef 53/0, k1_nach 40/0, k1_gegen 50/0, K1-Kopien, OBERFLAECHE K1) **zeilengleich mit der
  Test-Mod** (`G:k1_testmod.txt` = `G:k1_nach.txt`, `G:oberk1_testmod.txt` = `G:oberk1_nach.txt`); alle 70 alten Laeufe gleich wie gegen die Test-Mod
  ausser genau den 3 F2-Dateien mit den begruendeten Erwartungen (Abschnitt 4). Schlaf, Inventar, Beduerfnisse, Vertrauen: Dateien unveraendert
  (nur 8 Lua-Dateien anders als die Test-Mod, `diff -rq`), Lesestellen von `B.FightState` (`S:server/BanditsNPCBearInv.lua:482`, `:1086`, `:1205`,
  `S:server/BanditsNPCBearSleep.lua:457`) liefern dieselben Werte wie vorher.
* **Eigene Szenarien** (Abschnitt 3): Zombie jagt Kevin am Baeren vorbei -> 10/10 auf den Baeren, Kevin 0 s gebissen (Test-Mod: G1b 14,1 s, G1c
  50,6 s). Sprinter quer / weg -> 0/10 Treffer (wie L6b; Grenze aus C3/S5, Frage).
* 6 neue minor-Restbefunde (G-R1 .. G-R6), keiner haelt den Test auf.

## 1. Befunde der Pruefer -- geschlossen?

| ID | geschlossen? | am Code (selbst gelesen) / Beleg selbst gelaufen |
|---|---|---|
| C1 major | **ja** | EINE Grenze `near = d <= rMax + 0.5` fuer "kein Luftschlag" (`S:server/BanditsNPCBearFight.lua:1123-1129`) und den Angriff aus dem Ausfall (`:1155`); Uhr "steckt fest" nur nach eigenem Treffer neu (`:1196-1199`); verfehlter Ausfall-Hieb -> fightLungeOffMs 3 s ohne Ausfall (`:1259-1263`, `:1135-1136`); Wiederholung doppelt (8/16/32 ... <= 120 s, `blockSpan :205-226`, `:241`, `:284`); Biss hebt alles auf (`B.FightUnmiss :251-257`, Aufrufer `S:server/BanditsNPCBearHurt.lua:90`). `G:neu_run_pruef.txt`: P1 SP **und** MP Ende nach 4,0 s statt 90,1 s. Rest "5 Kampfbeginne in 240 s" ist gewollt (Sperre waechst) -- kein Haengen |
| C2 major | **ja** | `lureBias = 99` (`S:shared/BanditsNPCBear.lua:384`, Rueckfall `S:shared/BanditsNPCBearFoe.lua:712`): Manhattan in lureR 10 ist hoechstens 14,2 -> jeder, der den Baeren sieht, geht auf ihn; nur Kevin bis 2 am Zombie (`Foe.lua:699-700`) oder ein Bandit (`:697-698`) behaelt ihn. `G:neu_kampf_zomb.txt` 73/0 (Z6b, Z13 seitlich -> Baer); eigene G1c (Baer BLEIBT 4 seitlich) 10/10 |
| C3 major | **ja** | `fightLungeChase = 0` (`BanditsNPCBear.lua:357`, Rueckfall `Fight.lua:1140`): Ausfall = 0,5 x 1,35 = 0,675. **Selbst gemessen** (Weg des Baeren je Angriff, `G:sim_gegen.lua`): hoechstens **0,68** in allen 19 Laeufen x 10 Wuerfen |
| C4 minor | **ja** | Schluessel "rear:" / "rearL:" / "rearC:" (`Fight.lua:499`, `:557`, `:961`); Beginn sagt "rear planned (looking)". P2 gruen ("rear no 1x") |
| C5 minor | Frage | kein Code (Bandits setzt bis 3 Kacheln selbst jedes Bild, `B22:client/BanditUpdate.lua:1745-1771` -- gelesen). FK6 |
| C6 minor | **ja** | `baer/NAEHTE.md:21-22` "nur Einzelspieler; der MP-Hoheits-Client lenkt wie bisher ohne Haken"; Zeile 51 direkt unter 50 (`NAEHTE.md:205-206`, keine Leerzeile) |
| C7 minor | **ja** | `cfg("fightLeash", 25)` (`Fight.lua:139`); `G:neu_nach.txt` N8 |
| C8 minor | **ja** | `G:kampfkopie_nach.txt`: f2_kern 164/1 (nur Bestand "3 BearDodgeMax", auch gegen die Test-Mod), pruef_f2 14/0, nach_f2 22/3 (Bestand N4) |
| C9 minor | Frage | MP ehrlich offen: Sprint `sprintK` nur SP (`Fight.lua:96-99`), Ausfall nur SP (`:1136`, `:905`), Bewegungs-Takt nur SP (`:1416-1419`); MP-Locken unveraendert (`Foe.lua` lureMP / steerMP, nur Zombies ohne Ziel). F5 |
| C10 minor | **ja** (mit S3) | |
| S1 major | **ja** | `rearCheck` (`Fight.lua:510-560`, Aufruf `:1298-1301`, Lagen `foeSnap :399-408`, Besitzer `ownerPt :383-389` je Takt `:1246`): 0,4 s schauen, kein Aufrichten, wenn ein Gegner bis 2,5 dran ist, das Ziel liegt, oder Baer / Besitzer in 3 s erreicht wird. Simulation: L2 Sprinter Kevin gebissen 3,7 -> **0 s**, rear 0/10; Schlurfer (L1, L4, L5b, L6a, L7, G1a) richten weiter auf |
| S2 major | **ja** | `standing()` (`Fight.lua:393-396`) beim Beginn (`:479-482`) und im Schauen (`:519-520`). L5a / L5c: Zerfleischen nach **1,1 s** auf den Liegenden |
| S3 major | **ja** | `lureBears` laesst `c.pas` / `c.fst == "retreat"` aus (`Foe.lua:932-933`); `pas` kommt aus `S:server/BanditsNPCBearRegistry.lua:667`, `fst` aus `B.FightView` (`Fight.lua:1456`). Junges: `FightDecide` "cub" -> act none -> fst nil (`S:shared/BanditsNPCBearFightRules.lua:470`) -> lockt wie bisher (F7). Passiv-Lauf selbst: schlechtestes Leben **0,62** (`G:sim_gegen_passiv_alle.txt`) |
| S4 major | **ja** | `ownerBonus` (`Fight.lua:296-302`) in `pickTarget :332` (erste Wahl mit `tmp.own :640`) und `switchMaybe :1026-1055`. L4 Kevin gebissen **25,4 s** [20,7-31,8] (selbst; vorher 50,5) |
| S5 minor | Frage | eigene G2a / G2b bestaetigen: fliehender / querender Sprinter 0/10 (FK4, F6) |
| S6 minor | **ja** | Maul zuerst, wenn liegend/fallend in Maul-Weite und nicht der letzte (`S:shared/BanditsNPCBearFightRules.lua:226-230`). Selbst: liegend **alle** Angriffe Zerfleischen (Summe Wurf 1: onground:maul 22, falldown:maul 1, andere 0) |
| S7 minor | Frage | Bestand B1e (`S:shared/BanditsNPCBearRules.lua:652`), L8: 5,8 s rennend / 1,5 s gehend (selbst). FK5 |
| S8 minor | Testpunkt | Variante pathfind selbst: alle G-Laeufe Kevin 0 s; L-Laeufe wie NACHBESSERUNG. Zombie-F6 |

## 2. K1-K8 am Code gegen Kevins Worte (`ENTSCHEIDUNGEN.md:643-684`)

| Punkt | Kevin (woertlich, Auszug) | Code | Urteil |
|---|---|---|---|
| K1 | "der sollte das doch machen bevor er in den kampf stuermt das erste mal" | rearChance 100 (`BanditsNPCBear.lua:226`), EIN Entscheid je Kampf (`Fight.lua:469-492`), Pause 120 s ueber Kaempfe (`s.rearAt`, `:473`, `:917`), nur ausgewachsen (`allow.rear`, `FightRules.lua:153`), < 2,5 sofort Angriff (`:477`, `:956-964`) | **erfuellt fuer Schlurfer**; mit Sprintern meist KEIN Aufrichten (S1-Regel) -> Frage FK1 |
| K2 | "einen zombie der am boden lag nichtmehr angegrifen und gewartet bis er aufgestanden ist" | Ankunft AUF die Lage (`fightArrive 0`, `:1162-1167`), maulReach 1,4 (`FightRules.lua:166`), liegend/fallend -> Maul (`:226-230`, Haltung `Fight.lua:982-990`), kein "steckt fest" fuer Liegende in Weite nach eigenem Treffer (`:1196-1199`), nach dem Wegfliegen Anlauf auf die neue Lage | **erfuellt** (Simulation: maul 1,1 s, auch nach Umwerfen `maul at d 0.9-1.8 onground`) |
| K3 | "rennt langsam hinterher eher ein folgen und kommt nie zum zug" | Vorhalt `B.FightLeadPt` (`FightRules.lua:270-280`), Angriff nach Abstand zum Treffer (`B.FightHitD :284-296`, `Fight.lua:1150-1152`), Ausfall 0,675, Laufbefehl nur bei Abweichung / 2 s / Ankunft (`:1173-1187`; L4: 5 Befehle in 42 s) | **erfuellt fuer Zombies, die auf ihn / Kevin zulaufen** (L9a/L9b, G1a-c: Treffer 0,6-1,4 s); fliehende Sprinter nie (G-R1, FK4) |
| K4 | "schneller ... locker einholen", "nicht permanent rumrennen ... realtisch" | Sprint 4,6 nur Anlauf / Leinen-Sprint, nur SP (`Fight.lua:1400-1412`, `:96-99`); danach 8 s ruhig (`:696`, `Rules.lua:653-656`); nie Vanillas Reh (setX/setY nur am eigenen Baeren, `moveBear :1371-1376`). Messung nachgelesen (`kampf/werkzeug_plan/tempo_ausgabe.txt`: Baer 3,17, Sprinter 3,63, Kontrolle Reh 5,39 = tier_spez 2.8) | **SP erfuellt** (selbst: Anlauf 4,60 t/s in jedem Kampf-Lauf; ausserhalb Kampf 0 s Rennen nach Kaempfen bis 8 Kacheln); MP nicht (C9) |
| K5 | "die sind sehr fixiert auf mich ... ansonsten wird der total ignoriert" | Ziel-Sperre weg, `lureDecide` (`Foe.lua:681-714`), Lenken `steerSP :722-732` (setTarget vor spotted), Halten je Bild `holdZombie :401-431` ueber `Events.OnZombieUpdate` nur SP und nur solange gelenkt (`hookSync :436-455`); Bandits-Muster `B22:client/BanditUpdate.lua:1579-1786`, `:2588-2589` (Zeilen selbst gelesen) | **SP erfuellt** (selbst: G1a-c 10/10 Ziel Baer, Kevin 0 s; Test-Mod 0/10, Kevin bis 50,6 s); MP unveraendert (C9) |
| K6 | Log "b2 hides behind its owner from a zombie at 6" | grosser Koerper mit Kampf-Stufe versteckt sich nie (`S:server/BanditsNPCBearGuard.lua:318-342`), verletzt / schlaftrunken flieht (`:325`), Junges unveraendert | **erfuellt** ("hides behind" 0 in allen meinen 190 + 140 Laeufen) |
| K7 | "10 reichen aber er ist bei mir grad nie hingelaufen", "25 Kacheln", "in fullspeed zu mir sprinten" | Sicht bis sightMax 12 (`Fight.lua:342-350`), K6, Leine 25 (`BanditsNPCBear.lua:218`), Leinen-Sprint `s.leashRun` (`Fight.lua:1229-1244`, `S:server/BanditsNPCBearFollow.lua:202-221`) | **erfuellt** (L7: Leine bei 25,3, Sprint 4,3 t/s); Suchtakt mit Sprintern siehe G-R2 |
| K8 | Grund je "kein Angriff", Lenk-Zustand je Zombie | `B.LogEvery` (`BanditsNPCBear.lua:526-543`, nur mit Schalter, Deckel 64), Zeilen pick / no target (Gruende) / decide / rear planned-yes-no / act / hit-miss / run ... speed / skip / switch / ends / leash run / guard / lure ... (<= 8 je Takt) | **erfuellt**; nichts je Bild (Bewegungs-Takt `:1378-1441` ohne Log) |
| Nicht im Lauf | Sprung-Hieb, Clips, Modelle, Talente, Troege, Fischen | nichts davon gebaut; 33 Modell-Dateien byte-gleich (Abschnitt 5) | ok |

## 3. Simulation selbst + zwei eigene Szenarien

`G:sim_gegen.lua` = Kopie von `attrappe/kampf_nach/sim_nach.lua` (gebaut von `G:baue_sim_gegen.py`, Original unveraendert) + Szenarien
`G:szenarien_gegen.lua.txt` + Messung "Weg des Baeren je Angriff" (Ausfall). 10 Wuerfe je Lauf, Engine-MODELL (kein Spiel; ohne Waende, ohne
Kollision, Kevin wehrt sich nicht).
* **Alle L-Laeufe gegen das Staging zeilengleich mit der NACHBESSERUNG** (`G:sim_gegen_std.txt`; z. B. L4 Kevin 25,4 s, L2 0 s, L5a/c 1,1 s, L6b nie,
  haengt 0, hides 0). Passiv (`G:sim_gegen_passiv_alle.txt`): schlechtestes Leben 0,62 -- wie berichtet.
* **G1 "Zombie jagt Kevin am Baeren vorbei"**:

  | Lauf | Staging | Test-Mod (`G:sim_gegen_testmod.txt`) |
  |---|---|---|
  | G1a Schlurfer, Weg 3 Kacheln am folgenden Baeren vorbei | Ziel Baer ab d 9,7; rear; Treffer 5,5 s nach Beginn; Kevin 0 s | Ziel Baer 0/10; Kevin 0 s (der Baer ging trotzdem hin) |
  | G1b Sprinter jagt den rennenden Kevin seitlich vorbei | Ziel Baer ab d 7,5 (sofort); bite bei d 2,2, Kill; Kevin 0 s | Ziel Baer 0/10; Kevin **14,1 s** [4,9-46,0] |
  | G1c Baer BLEIBT 4 seitlich, Sprinter jagt Kevin vorbei | Ziel Baer ab d 9,0; "rear no (foe reaches the bear (5.9 at 3.6 t/s))"; Kill; Kevin 0 s | Ziel Baer 0/10; **nie getroffen; Kevin 50,6 s** |

  Das ist genau Kevins Bild ("beissen ihn nur wenn ... der weg zu mir am baeren vorbei fuehrt") -- im Modell behoben. pathfind-Variante: gleich (0 s).
* **G2 "Sprinter flieht quer"** (eigener Weg nach Osten, 3,63 t/s, reagiert nicht auf den Baeren = schlimmster Fall):
  G2a kreuzt 3 vor dem Baeren: Beginn d 4,0, "rear no (foe reaches ...)", swipeL bei d 2,6 verfehlt, dann `skip 7000: stuck at d 6.2` -> **0/10 Treffer**.
  G2b startet 2,4 vor ihm: Beginn erst nach 1,5 s bei d 5,9 (Suchtakt, G-R2), **0/10**. Auch mit `fightLungeChase 1` 0/10 (`G:sim_gegen_chase1.txt`).
  Ausfall in allen Laeufen <= 0,68 (C3 ok).

## 4. Pruefer, Attrappen, Uebernahme (alle selbst)

| Pruefung | Ergebnis |
|---|---|
| vier Lua-Pruefer auf den 8 geaenderten Dateien | luacheck 8 x ok, scopecheck 0, localcount hoechstens **40 aktiv / 70 insgesamt** (< 180), luacheck_pz 0 ausser 6 x W113 `NCBearMenu` in der Bench (Bestand) |
| Zeilenenden / BOM / Zeichen | alle 8 + `baer_uebernahme.py` + `NAEHTE.md`: LF, ohne BOM, nur ASCII -- wie in der Test-Mod bzw. HEAD |
| `kampf_baer/run.lua` / `run_echt_foe.lua` | **118 / 0**, **12 / 0** |
| `kampf_zomb/run.lua` | **73 / 0** |
| `kampf_pruef/run_pruef.lua` | 8 ok, 1 Befund (P1 "hoechstens EIN Kampf in 240 s": 5 -- gewollt, C1) |
| `kampf_nach/nach.lua` / `nach_zomb.lua` | **41 / 0**, **10 / 0** |
| alte Attrappen, Staging gegen Test-Mod (`G:alte_nach.txt` vs `G:alte_testmod.txt`) | 67 von 70 Zeilen gleich; anders nur f2_kern (1 rear rnd 60, 9 Passiv versteckt sich, 16 / 16 Leine, 20 Fall 20), pruef_f2 P1 (Leine 25), nach_f2 N1 + N2 x3 -- genau die begruendeten Erwartungen (BAU_KAMPF.md 5, BAU_ZOMBIES.md 6); KAMPF-Kopien gruen bis auf den Bestand (C8) |
| K1 / OBERFLAECHE K1 / OBERFLAECHE alle | zeilengleich mit der Test-Mod; `G:ober_vergleich_lauf.txt`: 0 NEU / 0 WEG |
| Uebernahme Trockenlauf `--staging mod_kampf` (`kampf/gegen/ue_trocken_gegen.txt`) | **OK, 0 Fehler, 2 Warnungen** (Bestand: Clips buck im Jungen-GLB, Baeren-Namen in NPC-Crew-Kommentar), 145 Dateien |
| `--probe kampf/gegen/probe --staging mod_kampf` (`kampf/gegen/ue_probe_gegen.txt`) | **OK, 0 Fehler, 2 Warnungen**; langcheck 8 Sprachen **0 Fehler / 12 Hinweise**; luacheck_pz 0 + 17 erlaubt; Tier-Regel setXY nur moveBear (`Fight.lua:1373-1374`), B.FoePushTick und UI |
| Engine-Aufrufe | gegen die Test-Mod neu nur `setX/setY` am Tier (V:`server/ClientCommands.lua:895-896`, V:`shared/Definitions/animal/ButcheringUtil.lua:575-576`, Zahl -- gelesen) und `instanceof(x, "IsoAnimal")` (V:`server/BuildingObjects/ISAnimalPickMateCursor.lua:14`); `Events.OnZombieUpdate.Add/Remove` B22:`client/BanditUpdate.lua:2588-2589`; alle Bandits-Zeilen 1584/1585/1593/1595/1659/1749/1750/1769/1771 selbst gelesen. Die Nachbesserung bringt **keinen** neuen Aufruf (Vergleich der Methoden-Namen gegen `kampf/vor_nach`). Kein pcall um Engine-Aufrufe (nur um `tickBody` / `moveTickBody`, eigener Code) |

## 5. Staging nachgezaehlt

`kampf/staging_dateien_kampf.txt` gegen die Platte (MD5 + Bytes je Datei, eigenes Skript): **185 Eintraege = 185 Dateien im Staging = 185 in der
Test-Mod** (ohne .git), 0 Abweichungen bei MD5 / Bytes / Status: **8 ueberschreibt, 0 neu, 177 gleich** (darunter **33 Modell-Dateien** models_X /
textures / AnimSets, **alle byte-gleich** mit der Test-Mod -- keine Modell-Datei geaendert). mod.info / 42/mod.info im Staging byte-gleich, neuer Text
`kampf/mod_info_vorschlag_kampf.txt` (ASCII, LF).

## 6. Restbefunde (neu vom Gegenpruefer, alle minor)

* **G-R1 Fliehender / querender Sprinter wird nie getroffen** (G2a, G2b, L6b je 0/10; auch mit `fightLungeChase 1`). Kurzer Ausfall 0,675 + Ausholzeit
  0,6 s (der Sprinter laeuft 2,2 Kacheln) + Sprint nur 1,27 x Sprinter (`BanditsNPCBear.lua:375`). Kevins "locker einholen und weg klatschen" gilt
  damit nur fuer Zombies, die auf den Baeren / Kevin zulaufen (dank K5 die meisten: G1 10/10). Weg: Sprung-Hieb (Punkt 8). Frage FK4 / F6.
* **G-R2 Suchtakt mit Sprintern:** war vorher kein Zombie in 12 Kacheln, kommt der naechste Hirn-Takt erst nach brainMs 1,5 s (`S:server/
  BanditsNPCBearServer.lua:1189-1191`, `BanditsNPCBear.lua:97`, `:152`) -- ein Sprinter legt in der Zeit 5,4 Kacheln zurueck, Kampfbeginn also bei
  ~6,6-10 (L3 7,4; G2b 1,5 s nach dem Auftauchen). Schlurfer unberuehrt (0,8 Kacheln). PLAN_KAMPF.md 1 K7 ("kein Hauptgrund") stimmt nur fuer
  Schlurfer. Frage.
* **G-R3 "steckt fest" zaehlt die Ausholzeit mit:** nach einem verfehlten Hieb gegen ein fliehendes Ziel kommt die Sperre (20 s) kurz nach dem Hieb
  (G2a `skip 7000: stuck at d 6.2`), obwohl er mit 4,6 gegen 3,63 aufholen wuerde. Die Uhr wird beim Angriff nicht neu gesetzt (`Fight.lua:1196-1214`;
  `enterAct :896-930` fasst `f.stuckAt` nicht an). Ein fliehender Zombie ist keine Gefahr -- vertretbar, nur zur Kenntnis.
* **G-R4 Schlafender Baer lockt:** waehrend `B.SleepStep` true gibt, laeuft `B.FightStep` nicht (`BanditsNPCBearServer.lua:879-880`), `fst` bleibt nil,
  `lureBears` laesst ihn drin (`Foe.lua:932-933`). Zombies in 10 Kacheln, die ihn sehen, gehen auf ihn, wecken ihn bei 8 (sleepWakeR), dann F3-Regel
  5 s schlaftrunkene Flucht ("woke" -> retreat -> Locken aus, die Zombies sind wieder frei). Nicht neu, mit lureBias 99 + Haken staerker. Testpunkt,
  Frage F9.
* **G-R5 Kollisions-Forschung ungenau ("Kuh genauso"):** Vanilla haelt Tiere nur waehrend einer Spieler-Aktion fest (`V:client/ISUI/Animal/
  ISAnimalContextMenu.lua:89`, `:495`, `:751`, `:776`, `:843`); eine stehende Kuh schiebt den Spieler also weich weg (Kreis `collisionSize` 0,5 x Groesse,
  `V:shared/Definitions/animal/CowDefinitions.lua:232`; Wirkung `J:characters/animals/IsoAnimal.java:424`, `:437`, `separate`). Unser Baer wird bei
  Sitz / Bleiben / Kampf festgehalten (`B.Hold` -> `setBlockMovement(true)`, `S:server/BanditsNPCBearWorld.lua:891`) und schiebt dann gar nicht
  (`J:iso/IsoMovingObject.java:1170-1173`); beim Laufen nur ein Kreis 0,30 x 1,35 = 0,41 (`S:shared/BanditsNPCBearDefs.lua:195`). Frage an Kevin
  berichtigt (Abschnitt 8).
* **G-R6 Schauen kostet 0,4 s auch ohne Aufrichten:** ist das Aufrichten geplant und faellt dann weg (Sprinter), stand er trotzdem 0,4 s still (G2a:
  Beginn 1,5 s, Hieb 2,0 s). Teil von FK1.

## 7. Testanleitung `kampf/anleitung_entwurf.md` -- geprueft und berichtigt

Alle Befehle gibt es (`S:client/NCBearBenchFight.lua:112` FightZed, `:136` FightLog, `:212` FightSpeed, `:234` Lure, `:310` Tune; `NCBearBenchCub.lua`
CubHere/CubTame/CubGrow/CubClean); die Log-Texte passen zum Code (`pick z`, `rear planned (looking)`, `rear yes`, `rear no (...)`, `act ... (hit-d,
down, lunge 0.7)`, `leash run, owner at`, `follow: ... leash run over`, `big body does not hide`). Berichtigt (7 Stellen):
1. Kopf: Hinweis auf diese Pruefung.
2. Punkt 4: frisch hingestellte Zombies zeigen auch `target was none` (sie haben Kevin evtl. noch nicht gesehen; `Foe.lua:690-694`).
3. Punkt 5: danach den Baeren wieder auf **Folgen** (Teil D braucht es; Leinen-Sprint nur beim Folgen, `Fight.lua:1233`).
4. Punkt 7: mindestens 2 Minuten nach dem letzten Aufrichten -- sonst steht nur `rear no (cooldown ...)`, weil die Pause vor "target down" geprueft
   wird (`Fight.lua:473-482`).
5. Punkt 10: ehrlich, dass ein quer / weg rennender Sprinter meist nicht erwischt wird (G-R1) und er mit Sprintern manchmal erst bei ~7 losgeht (G-R2).
6. Punkt 12: "Baer auf Folgen".
7. Punkt 15: nur die Zaun-Sperre in Schlagweite schreibt `... ignored for 8 s (1. time)` (`Fight.lua:244-245`); "steckt fest" schreibt nur
   `skip <z>: stuck at d ...` (Sperre 20 s, dann 40 s, `:284`, `:1204`).

## 8. Fragen fuer Kevin (gebaut ist jeweils die Empfehlung)

1. **FK1 Bruellen:** er richtet sich nur auf, wenn in 3 s kein Zombie ihn oder dich erreicht und das Ziel nicht am Boden liegt -- mit Sprintern also
   fast nie (dann knurrt er und greift sofort an). Gut so? (Aus: `NCBear_Tune("rearSafeS", 0)`)
2. **FK2 Passiv / zu muede / ohne Vertrauen:** lockt keine Zombies mehr, folgt dir, weicht nicht aus. Oder soll er Zombies ausweichen?
3. **FK3:** Zombies bis 2 Kacheln an dir greift er zuerst an. Ok?
4. **F3 Baer-Magnet voll:** jeder Zombie, der ihn in 10 Kacheln sieht, geht auf ihn (ausser er ist bis 2 an dir). Ok, oder weniger (`lureBias` 4)?
5. **FK4 / F6:** einen weg- oder querrennenden Sprinter erwischt er nicht. Sprung-Hieb abwarten (Empfehlung), Sprint 5,5 statt 4,6, oder im Hieb mitgleiten
   (bis 2,8 Kacheln Rutschen)?
6. **F1:** im Sprint gleitet der Koerper ~45 % schneller als die Beine laufen -- ok bis zu einem eigenen Sprint-Clip?
7. **FK5:** beim Folgen rennt er stossweise hinter dir her (sein Gehen ist langsamer als deins) -- im naechsten Modell-Lauf ein Trab?
8. **FK6:** steht eine NPC-Crew-Figur bis 3,5 Kacheln am Zombie, lenkt der Baer ihn nicht (sonst zoegen beide) -- so lassen?
9. **F5 Mehrspieler:** Sprint, Ausfall und das Festhalten der Zombies gibt es nur im Einzelspieler -- eigener MP-Lauf?
10. **F7:** waehrend des Leinen-Sprints zu dir (hoechstens 20 s) beginnt er keinen neuen Kampf -- ok?
11. **F9 Schlaf:** ein schlafender Baer zieht Zombies an, wacht erst bei 8 Kacheln auf und flieht dann 5 s schlaftrunken. Weck-Abstand 10, und soll er
    neben dir sofort kaempfen statt 5 s zu fliehen?
12. **Suchtakt (G-R2):** mit Sprintern geht er manchmal erst bei ~7 Kacheln los. Schneller nachschauen (etwas mehr Rechenzeit)?
13. **Zombie-F6:** ein Zombie, der schon einen Weg zu dir hat, laeuft dem bis ~8 s weiter nach. Weg abbrechen bauen, falls dein Log viele
    `flipped back` zeigt?
14. **Zombie-F7:** soll das Junge Zombies ueberhaupt anziehen (heute ja; es versteckt sich dann hinter dir)?
15. **Kollision (nur Forschung):** man laeuft durch den Baeren, weil er beim Sitzen / Bleiben / Kaempfen festgehalten wird -- dann schiebt die Engine
    niemanden. Vanilla haelt Tiere nur beim Streicheln / Melken fest, eine stehende Kuh schiebt dich weich weg (Kreis um ihre Mitte); auch beim Laufen hat
    der Baer nur einen Kreis von 0,41 Kacheln um die Mitte, Kopf und Hinterteil sind frei. Eigener Lauf dafuer (anders festhalten / groesserer Kreis)?

## 9. Jar-Ausnahmen im Staging (nur im Jar belegt) -- alle vor dem Kampf-Lauf, keine neue

* `S:client/ISUI/BanditsNPCBearZz.lua:124` `a:getForwardDirection()` am Tier (Kevins Wort 13.11., F3 Antwort 5). (`S:shared/BanditsNPCBearFoe.lua:248`
  am ZOMBIE ist Bandits-belegt.)
* `S:shared/BanditsNPCBearInvRules.lua:243` getHeadCondition, `:248` getSharpness, `:256` setSharpness (A3); `:519` addExtraItem, `:527` setSpices (A4);
  `:529` setBurnt, `:530` setCooked, `:531` setCookingTime, `:533` setOffAge, `:534` setOffAgeMax, `:538` setFreezingTime, `:540` setFrozen (A2);
  `:660` getHue(), `:681` setHue (A10) -- Kevins Wort `f4/KEVIN_ANTWORTEN.md:5-6` "Ja, dieselben wie NPC Crew", Liste `f4/JAR_LISTE.md` Abschnitt 0.

## 10. Dateien

* Dieser Bericht; `kampf/gegen/ue_trocken_gegen.txt`, `kampf/gegen/ue_probe_gegen.txt`, `kampf/gegen/probe/`.
* `attrappe/kampf_gegen/`: `alle_gegen.sh` (alle Attrappen), Laeufer-Kopien `alte_*.py` (TMP `kampf_gegen/tmp_*`), Ausgaben `neu_*.txt`, `alte_nach.txt`,
  `alte_testmod.txt`, `k1_*.txt`, `oberk1_*.txt`, `kampfkopie_nach.txt`, `ober_vergleich_lauf.txt`; Simulation `sim_gegen.lua` (aus `baue_sim_gegen.py`
  + `szenarien_gegen.lua.txt`), Ausgaben `sim_gegen_std.txt`, `sim_gegen_testmod.txt`, `sim_gegen_vornach.txt`, `sim_gegen_passiv*.txt`,
  `sim_gegen_pathfind.txt`, `sim_gegen_chase1.txt`.
* Berichtigt: `kampf/anleitung_entwurf.md` (Abschnitt 7). Kevin muss nach dem Einbau das Spiel neu starten (Lua laedt nur beim Spielstart).
