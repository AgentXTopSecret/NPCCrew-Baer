# Lauf baer-k1 -- GEGENPRUEFER (nach der Nachbesserung)

Stand 14.11.2026 ~05:45, Rolle GEGENPRUEFER (nichts gebaut, keinem Bericht geglaubt). **Statisch geprueft, nicht gespielt.**
Geschrieben nur in `_arbeit/baer_zaehmen/k1/` (dieser Bericht, `gegen/` mit Laeufen, Bildern, Diffs, Probe-Ordner; `anleitung_entwurf.md`
berichtigt, Stand davor `gegen/anleitung_entwurf_vor_gegen.md`) und `attrappe/k1_gegen/` (eigene Attrappe `gegen.lua`, `bestand_testmod.lua`,
Mitschrift `zeichne_dump_gegen.lua`). Die Laeufer der alten Attrappen (`attrappe/k1_nach/*.py`) haben ihre eigenen Ausgaben in `attrappe/k1_nach/`
neu geschrieben (Inhalt gleich; Sicherung vorher `k1/gegen/sicherung_k1_nach/`). **Kein Byte in mod_k1, Test-Mod, NPC Crew, Vanilla, Bandits,
baer/tools, baer/NAEHTE.md**; kein git, kein Download, kein Spielstart.
Kuerzel: `S:` = `mod_k1/42/media/lua/`, `V:` = Vanilla `media/lua/`, `J:` = Jar 42.22, `E:` = `baer/begleiter/ENTSCHEIDUNGEN.md`.

## 0. Ergebnis zuerst

- **Urteil: bereit fuer Kevins Einzelspieler-Test.** Kein offener Blocker. Der eine major (C1) ist geschlossen; von den 16 minor sind 11 im Code
  geschlossen, C3 nur zum Teil, 4 bewusst ohne Code mit Frage an Kevin (C4, P1-Rest, P6, P8).
- **Nichts kaputt gefunden:** vier Lua-Pruefer 0 neu, alle K1-Attrappen gruen (153/0, 134/0 + 136/0, 40/0, 167/0 + 169/0, Pruefer 53/0), alte
  Attrappen genau wie im Bericht (Ausgaben byte-/zeilengleich), umgestellte F3/F4-Oberflaeche 261/0 + 251/0 + 172/0 + 172/0, langcheck 0 Fehler,
  Texte paritaetisch in acht Sprachen, Trockenlauf + `--probe` OK (0 Fehler, 2 Warnungen Bestand), Staging 185 Dateien gegen Platte und Liste
  0 Abweichungen, **keine Modell-Datei geaendert** (33 byte-gleich).
- **Drei eigene Stichproben** (`attrappe/k1_gegen/gegen.lua`, **50 / 0**): 37 von 94 Patronen gebuendelt + Absturz in allen vier Speicher-Lagen
  + Engine-Wurf mitten in der Schleife: Zaehl-Invariante haelt (mit Kopie beim Spieler); Vertrauen alt 44 -> **-12 genau einmal** (Register,
  Spiegel, zweimal neu laden), ein Spieltag Streicheln + satt fuettern + Hunger 90 % -> **-16**, je Quelle nur einmal; Einfrieren bei
  schlafendem Besitzer: 8 Spielstunden **nichts** steigt, kein Leben-, kein Vertrauens-Verlust, kein Nachholen.
- **Eigener Restbefund R1 (minor, Bestand F4, nicht durch K1 entstanden):** erstes Geben an einen LEEREN Baeren hat noch keine Kopie beim Spieler
  -- Absturz genau zwischen vollem Speichern (Register) und dem naechsten Spieler-Speichern (SP alle 10 s) laesst das Gegebene **doppelt**
  (`S:server/BanditsNPCBearInv.lua:281-284` "keine Kopie: das Register gilt"). In der Test-Mod genauso (1 Nagel, `attrappe/k1_gegen/bestand_testmod.lua`).
  Sekunden-Fenster, darum kein Blocker; Vorschlag fuer den naechsten Lauf in Abschnitt 7.
- Testanleitung berichtigt (Abschnitt 6): Selbst-Trinken am grossen Baeren (3 Flaschen = ~20 Punkte, nicht "bis 0"), Look-Sperre (der zweite
  Look-Klick trifft die Unstuck-Uhr, nicht die 60-s-Sperre), am Boden erst aufhelfen, Schritte fuer A, V4, E, H ergaenzt.

## 1. Die 17 Befunde -- geschlossen?

| ID | geschlossen? | selbst nachgeprueft (Fundstelle / Lauf) |
|---|---|---|
| **C1** major | **ja** | `needFull = 1` (`S:shared/BanditsNPCBear.lua:266`), `restOf` "hand" unter 1 % -> 0 (`S:server/BanditsNPCBearNeeds.lua:315-319`), gelesen in `B.CheckFeed`/`B.CheckDrink` (`S:shared/BanditsNPCBearRules.lua:177`, `:195`). Eigene G2: Hunger 3 + Steak (-40) am ausgewachsenen -> 0 -> +0,5. Register == Sicht (N1, 401 Werte). |
| C2 | **ja, wie gebaut** -- aber Kevins Wort offen | `B.TrustAdd` "down" fragt `counts()` (`S:server/BanditsNPCBearNeeds.lua:281-291`). Kevin 14.11. ~00:00 woertlich: *"wenn der baer down (todesschutz) geht verliert er -10"*; die Sperre in `E:752` nennt "Leben-Abzug bei 100 und Tagesabschluss/Vertrauen (nur gezaehlte Stunden)". Ich lese "am Boden" eher als Kampf-Ereignis (immer -10) -- Frage 2 bleibt richtig; der Tooltip sagt heute "jedes Mal" (R3). |
| C3 | **teilweise** | Farbe/Fuellung jetzt nach dem ungerundeten Wert (`S:client/ISUI/BanditsNPCBearHud.lua:562-578`): -0,5 rot statt grau. **Die Zahl weicht weiter ab:** +0,5 -> Kopf "+1", Fenster "+0.5%" (`:566-568` rundet halbe auf). Da JEDE Vertrauens-Aenderung 0,5 ist, steht jeder zweite Wert im Kopf anders als im Fenster (R2, Frage). |
| C4 | **nein, bewusst** (Frage) | `dayOf = floor(Weltstunden / 24)` (`S:server/BanditsNPCBearNeeds.lua:113-115`); eigene G2: Wechsel bei Weltstunde 1008. Beleg 07:00 aus `J:GameTime` laut Nachbesserung, nicht selbst nachgelesen. |
| C5 | **ja** | `B.NeedsDayMark` / `dayFromMark` / `B.NeedsFromMark` (`:665-705`), geschrieben in `B.MarkOf` (`S:server/BanditsNPCBearHeal.lua:118-121`). N4 gruen; eigene G2: Spiegel zurueck traegt -12 (nie -100). |
| C6 | **ja** | `if isServer() and player:isAsleep() ~= true` (`S:server/BanditsNPCBearSleep.lua:135`); Aufruf-Form `V:shared/TimedActions/ISWakeOtherPlayer.lua:6` (am anderen Spieler, `isAsleep()` ohne Argument) selbst gelesen. Jar-Weg (PlayerPacket -> setAsleep) nicht selbst nachgelesen. |
| C7 | **ja** | `retry = "UI_BN_Bear_Why_LookRetry"` (`S:server/BanditsNPCBearLook.lua:107`), Text in acht Sprachen (EN `:361-362`). |
| C8 | **ja** | Sandbox-Tooltip nennt nur Hunger und Durst fuer 16 h (`S:shared/Translate/EN/Sandbox.json:29`, DE ebenso). |
| C9 | **ja** (fuer die K1-Kopien) | K1-Kopien f1_ober 335/7, f1b 200/11, aussehen_ober 190/1 + 191/1 = Test-Mod-Stand; die ORIGINALE von f1_ober, f1b, aussehen_ober, f3_ober, f4_ober brechen gegen mod_k1 weiter ab (gewollt: K1 aendert die Regeln; die umgestellten F3/F4-Kopien sind gruen). Bilder `k1/bilder/KEVIN_fenster_k1_DE_4k.png` und `KEVIN_inventar_zahlenfeld_1080.png` da. |
| P1 | **teilweise, bewusst** (Frage 4) | Aufrichten gross x1,63 statt x1,89 (`S:shared/BanditsNPCBearTagPose.lua:50`). |
| P2 | **ja** (Rechnung nachvollzogen) | Tabelle neu nach Bildschirm-Hoehe; die Schranke "Abstand nie kleiner als im Stehen" folgt aus k = S(t)/S0 und A0 >= S0 (NACHBESSERUNG 2) -- stimmt. Die Iso-Faktoren 0,612 / 0,354 habe ich aus dem Pruefer-Werkzeug uebernommen, **nicht selbst nachgemessen**. Dauern der Tabelle = `B.CLIPS` (rear 3,0 / slam 2,4 / bite 1,3 / sit 4,0, `S:shared/BanditsNPCBearFightRules.lua:63-71`). |
| P3 | **ja** | Mittelstrich Fenster (`S:client/ISUI/BanditsNPCBearWinParts.lua:274`) und Kopf (`trustBar`, Hud `:876`); im eigenen Bild gesehen. |
| P4 | **ja** | Dunkelroter leerer Teil bei negativ (WinParts `:268`, Hud `TRUST_NEG_BG`); im eigenen Bild bei -0,5 gesehen. |
| P5 | **ja** (Frage 6) | `needMode` gibt bei "Aus" ab 75 % `SHOW_NUM` (Hud `:348-356`) -> "Hunger 80%". |
| P6 | **nein, bewusst** (Frage 7) | Nasen-Warnung im Zahnrad rot (Vanillas `notAvailable`), im eigenen Bild gesehen. |
| P7 | **ja** | `UI_BN_Bear_Win_TrustTip` nennt "Hunger oder Durst" und "je hoechstens einmal am Tag" (EN `:567`, DE im eigenen Bild gelesen). |
| P8 | **nein, bewusst** (Frage 8) | -- |

## 2. Jeder Punkt der K1-Liste am Code gegen Kevins Worte

| Punkt | Kevins Wort (woertlich, `E:`) | Code (Fundstelle) | Urteil |
|---|---|---|---|
| V1 | *"ich will bei 0 starten und dann bis 100% und bis -100%"* (21:40) | `trStart 0`, `trMin/trMax` (`S:shared/BanditsNPCBear.lua:287-290`); einmal `(alt-50)x2` mit Marke `trV` (`S:server/BanditsNPCBearNeeds.lua:145-156`, `S:shared/BanditsNPCBearNeedRules.lua:225-229`); Spiegel traegt `trV` (`S:server/BanditsNPCBearHeal.lua:59`) | ok (G2) |
| V2 | *"gewinnen soll er immer nur beim streicheln und wenn das essen und trinken 100 erreicht ... um 0,5 aber immer nur 1x pro tag"* (23:55) | `B.TrustAdd` pet/feedfull/drinkfull je Marke (`Needs:277-303`); Aufrufer `S:server/BanditsNPCBearServer.lua:282` (nur wenn DIESES Stueck auf 0 brachte), `:325-326`, `Needs:408`; alte Stellwerte weg (Tier-Regel `k1entfallen` im Probe-Lauf 0 Funde) | ok (G2) |
| V3 | *"bei 90% direkt - 5 ... down (todesschutz) ... -10 und ab 1% hp (durch hunger/durst) auch -10"* (00:00) | `Needs:562-570` (90 %, je Marke lh/lt), `S:server/BanditsNPCBearHurt.lua:157` -> `Needs:281-291` (-10, mit Einfrier-Sperre, C2), `Needs:590-594` (1 %, Marke lw) | ok; Sperre am Boden = Frage 2 |
| V4 | *"Nur Beduerfnisse"* (+-25 %, 02:50); *"Unter -70 %"* | `B.TrustK` (`NeedRules:200-205`) auf Hunger, Durst UND Muedigkeit (`Needs:546-550`); `B.NoFight` `tr < -70` (`NeedRules:256-264`); Herz `trM` ab 100 (`Needs:636`) | ok |
| V5 | *"normaler Balken mit Zahl"*, *"negativ rot ... positiv ... gruen"* | Fenster `trustRow` (`S:client/BanditsNPCBearWinData.lua:713-735`), Kopf Hud `:562-578`, Woerter `{-70,-20,20,70}`; acht Sprachen | ok; Zahl Kopf/Fenster R2 |
| S | *"beim roar geht der text nicht hoeher"*, *"der hp balken geht auch nicht hoeher"* | `U.PoseLift` (`S:client/BanditsNPCBearPose.lua:492`), Tabelle aus den GLB (offline), Anker Hud `:981`, z Z z (`Zz.lua`), schwebende Zeilen (`Fx.lua`); kein Engine-Aufruf | ok statisch; im Spiel ansehen |
| Z | *"zahnrad menue einbauen in baeren ui ... fuer unnoetige ausblendungknoepfe"*; *"hp balken auch gern ausblenden ... durch einen botton"* | Zahnrad `Window.lua:79`, `:600-655` (Vanilla-Form `V:client/Chat/ISChat.lua:130-140` selbst gelesen); Punkte `d.gear` (WinData `:1082`); `hpoff` je Spieler (`Tags.lua`); Passiv bleibt; Liste erweiterbar | ok |
| D | *"Verbinden ... ireefuehren ... wie 'Heilen'"* | DE `:131-132` "Junges heilen" / "Baeren heilen", `:389` "Heilen"; kein "verbind" mehr in DE | ok |
| L | *"da steht immer dein baer ist beschaeftigt"* | Grund + Restzeit (`Look.lua:85-112`, `:198-210`); Testbefehl loescht `swapAt/swapTryAt` (`NCBearBenchCub.lua:1204`) | ok |
| A | (Claude 22:25) | `SLEEP_KEYS` nur mit `sleepClips == true` (`NCBearBench.lua:373-405`) | ok |
| I | *"nur die 1000 items einstellen"*; *"bei geben eine auswahl ... wo ich eine zahl eintippe"*; *"Ja, auch Nehmen"* | `GIVE_MAX`/`invTakeMax` 1000 (InvClient `:47`, `S:shared/BanditsNPCBear.lua:309`); Server klemmt (`K.putCount` `Inv:530-539`, `K.putRoom` `:543-553`); EINE Put-Aktion mit k (`InvClient:467-490`, `PutAction.lua:141-168`); Zahlenfeld `ISTextBox` + `setOnlyNumbers` (`CountBox.lua:50-71`, Form `V:client/ISUI/Animal/ISAnimalContextMenu.lua:791-794` selbst gelesen); Geben UND Nehmen (InvWindow `:662-702`); Fusszeile ohne 50 | ok (G1); Taschen-Stuecke K-F10 |
| X | *"die damage zahl soll rot werden"*, *"mit info dann im screen"*, Muedigkeit *"Nein, so lassen"* | `weakOf`/`meleeRow` (WinData `:450-495`): rot, Grund mit Stand, normal -> jetzt je Angriff; `B.NeedK` unveraendert (Muedigkeit nur Ausdauer) | ok (eigenes Bild) |
| E | *"Ja, ab 50 % Durst"*, *"bis er 0% erreicht"*, *"auch dreckiges wasser"* | `B.InvEatStep` bis `invEatStop 0`, kleinstes deckendes Stueck (`Inv:1074-1125`); `K.drinkPick` Water vor TaintedWater, kleinste Fuellung zuerst (`:1141-1158`), `K.sip` nur was fehlt, Behaelter bleibt (q 0, ohne Stoff) (`:1160-1191`), `B.InvDrinkStep` (`:1193-1233`); "inv" zaehlt nie fuer V2 | ok |
| F | *"beim schlafen/ausgelogt/nicht geladen in der welt weit out of range duerfen seine beduerfnisse nie steigen"*; *"dann nimm dein vorschlag fuer den mp"* | `counts()` (`Needs:249-264`): liegt / Besitzer schlaeft / > 70 Kacheln / offline / nicht geladen; Leben-Abzug und V3 nur bei `go` (`:525-595`); dt je Takt gedeckelt | ok (G3) |
| SL | *"wenn ein spieler schlaeft schlaeft der baer immer mit ... und wenn der spieler vorspult ... ausser gegner sind in der naehe"* | `B.SleepWant` "owner" vor dem Modus (`NeedRules:316`), Weg nur bis `sleepGoR` 25 (`Sleep.lua:348-360`), Vorspulen `getCurrentGameSpeed() > 1` nur SP (`Zz.lua:321-329`, Form `V:client/TimedActions/ISTimedActionQueue.lua:302` selbst gelesen), Gefahr weckt (unveraendert) | ok |
| U | *"anzeige automatisch auf wenn seine beduerfnisse auf +75% steigen ... verschwinden wieder wenn es unter 75 ist"* | `needMode` (Hud `:348-356`), nur eigener Baer, auch bei "Aus" | ok |
| H | *"nach 16std von 0 auf 100"*, *"Mitte, ~6 %"*, *"Nach Saettigung"*, *"dynamisch steigen pro groesse"* | `needRiseH 6,25` x Tempo x `TrustK` (`Needs:546-549`); `B.HunDayPts` = 55,3 x {1,5; 4; 12,5} (`NeedRules:136-140`), `B.WaterDayL` = 6 % von {25; 80; 250} kg (`:143-147`), gleitend an statAt; Tooltip "satt fuer ~x %" in Fuettern-Menue (`Menu.lua`) und Inventar (InvWindow). **55,3 selbst nachgerechnet** am Jar-Text `k1/jar/dec/IsoGameCharacter.java:9958-9984` und `GameTime.java:439-441`, `:526`: 9,6e-6 x (30/mpd) x M je Bild bei M/(120 mpd) Stunden je Bild = 0,03456 je Stunde = 3,456 Punkte x 16 = **55,3** | ok |

## 3. Eigene Stichproben (`attrappe/k1_gegen/gegen.lua`, Lauf `k1/gegen/lauf/`, 50 bestanden / 0 Fehler)

- **G1 Zahlenfeld-Geben 37 von 94 Patronen** (Put k = 37): 37 beim Baeren, 57 beim Spieler, EINE Meldung "37", Zaehl-Invariante je Feld live.
  Absturz (Register und Spieler zu verschiedenen Zeiten gespeichert, Form `f4_gegen`): **G1K mit Kopie beim Spieler -- alle vier Lagen gruen**
  (Register alt/neu x Spieler alt/neu, dazu zweiter Absturz direkt danach). **Ohne Kopie** (Baer war leer, erste Aenderung) und "Register neu,
  Spieler alt": 37 doppelt -> R1 (Bestand F4, Test-Mod gleich).
- **G1W Engine-Wurf mitten in der Schleife** (am 20. Stueck): vor dem Herausnehmen -> 19 drueben, 75 beim Spieler, Invariante live und nach
  Absturz (mit Kopie / gleiche Lage) gruen; nach dem Herausnehmen (`sendRemoveItemFromContainer` wirft) -> genau 1 Stueck weg (Bestand F4
  `takeOne`, wie der K1-Pruefer P1). Kein pcall im Kern: der Wurf kommt durch, nichts haengt.
- **G2 Vertrauen alt 44 -> -12** genau einmal (NeedsFix dreimal, Spiegel zurueck, alter Spiegel ohne `trV`, zweimal neu laden); dann ein
  Spieltag: Streicheln -11,5 (zweimal: bleibt), satt fuettern -11 (zweites Mal: bleibt; Fuettern ohne satt: nichts), Hunger erreicht 90 -> -16
  (zweites Mal am selben Tag: bleibt); naechster Spieltag Streicheln wieder -15,5.
- **G3 Einfrieren bei schlafendem Besitzer:** Hunger 85, Durst 99,9, Muedigkeit 50, Leben 0,5, 48 Langsam-Takte (8 h) mit Bitte "Sleep":
  nichts steigt, Durst erreicht nie 100/kein -5, Leben gleich, Sicht `nfz` owner/sleep; nach dem Aufwachen nur EIN Takt (kein Nachholen);
  75 Kacheln weg eingefroren, 60 Kacheln zaehlt wieder.

## 4. Pruefungen (alles selbst gelaufen, Ausgaben `k1/gegen/lauf/`)

| Pruefung | Ergebnis |
|---|---|
| vier Lua-Pruefer auf allen 31 gegen die Test-Mod geaenderten Lua-Dateien (`pruefer4.txt`) | luacheck 0, scopecheck 0, localcount hoechstens 73 aktiv / 90 insgesamt (< 180), luacheck_pz 40 x W113 = genau die Test-Mod (Aktionsklassen, Bench) |
| K1-Kern / K1-Oberflaeche (Kern-Attrappe + echter Kern) / Nachbesserung Kern / Nachbesserung Oberflaeche / Pruefer | 153/0; 134/0 + 136/0; 40/0; 167/0 + 169/0; 53/0 (1 Befund = Bestand takeOne) |
| alte Attrappen (`alte_laufen_kern.py`, `alte_k1_kern.py`, `alte_laufen_ober.py`, `alte_ober_k1.py`) | Ausgaben inhaltlich gleich wie in NACHBESSERUNG 3 (Kern-Liste und K1-Kopien zeichengleich, Oberflaeche nur Zeilenenden anders) |
| umgestellte F3/F4-Oberflaeche (`attrappe/k1_ober/alt_umgestellt/`) | F3 261/0 + 251/0, F4 172/0 + 172/0; jede Umstellung nennt ihren K1-Grund (`attrappe/k1_ober/alt_umgestellt.txt`, 22 Zeilen) |
| NPC Crews `langcheck.py` ueber die acht Staging-Ordner (`langcheck_acht.txt`) | 0 Fehler, 3 Hinweise (CN-Blasenschrift, DE breiter, DE-gleich) |
| eigene Text-Pruefung (`k1/gegen/texte_paritaet.py`) | UI 586 / Sandbox 34 Schluessel je Sprache, 0 fehlen, 0 zuviel, Platzhalter gleich, ohne BOM, LF, Round-Trip `json.dumps(indent=4, ensure_ascii=False)+"\n"` gleich, sortiert; 604 Schluessel-Bezuege im Code, 0 fehlen; 40 neue EN-Schluessel, alle benutzt |
| Skript-Dateien `scripts/*.txt` | **keine geaendert** (10 byte-gleich mit der Test-Mod; Rezept-Fix vom 13.11. von Kevin gespielt) |
| Uebernahme Trockenlauf / `--probe k1/gegen/probe` (`ue_trocken.txt`, `ue_probe.txt`) | OK 0 Fehler, 2 Warnungen (Bestand: Clips buck im Jungen-GLB, Baeren-Namen in NPC-Crew-Kommentar); Probe: langcheck 0 Fehler, luacheck_pz 0 + 17 erlaubt, Bench nie kopiert, Tier-Regel `k1entfallen` 0 Funde |
| Staging gegen `staging_dateien_k1.txt` und Platte (`k1/gegen/zaehle_staging.py`) | 185 = 185, MD5/Bytes 0 Abweichungen, 2 neu + 45 ueberschreibt + 138 gleich (darin 33 Modell-Dateien, alle byte-gleich), nichts nur in der Test-Mod |
| Engine-Aufrufe neu in K1 (Stichprobe selbst gelesen) | `isAsleep` (`V:shared/TimedActions/ISWakeOtherPlayer.lua:6`), `getCurrentGameSpeed` (`V:client/TimedActions/ISTimedActionQueue.lua:302`), Zahnrad-Knopf/-Bild (`V:client/Chat/ISChat.lua:130-140`), `notAvailable` + Tooltip (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:160-163`), `ISTextBox`/`setOnlyNumbers` (`:791-794`), `getItemsFromFullType` + `size/get` (`V:shared/TimedActions/Animals/ISMilkAnimal.lua:83-85`), `isFavorite/isEquipped` (`V:shared/Camping/ISCampingMenu.lua:33`), `getEffectiveCapacity(chr)` (`V:client/Foraging/ISBaseIcon.lua:105`), `AddItems` (Bench, `V:client/DebugUIs/Scenarios/AiteronScenario.lua:79`), Stoffnamen (`V:client/Farming/ISUI/ISFarmingMenu.lua:80`) -- gleiche Argument-Arten; **keine neue Jar-only-Methode, kein pcall** |

## 5. Eigenes Fensterbild aus dem echten Code (angesehen)

`k1/gegen/bilder/GEGEN_fenster_DE.png` (1080p), `_EN.png`, `_DE4k.png` -- Kette: `attrappe/k1_gegen/zeichne_dump_gegen.lua` (Kopie der K1-Mitschrift,
eigene Szenen) -> `k1/gegen/zeichne_gegen.py` (Kopie des Mal-Skripts, echte Spielschriften), Lupen `lupe_tru_plus.png`, `lupe_tru_minus.png`.
Gesehen: Vertrauen +0,5 gruen halb gefuellt mit Mittelstrich; -0,5 rot mit dunkelrotem Rest; Tooltip "Jetzt: Neutral (+0.5%)", Regeltext mit
"je hoechstens einmal am Tag", "Heute noch moeglich: satt fuettern, satt traenken"; Hunger-Tooltip "Seine Beduerfnisse ruhen: du schlaefst",
"Tagesbedarf bei seiner Groesse: 446 Hungerpunkte (etwa 11 Steaks) und 9.6 l Wasser", Honig 4.5 %; "57 je Treffer" rot, Tooltip "Durst 92%: 70%
des normalen Schadens. Sonst 81 je Treffer, jetzt 57.", je Angriff "(sonst ...)"; Zahnrad offen: Namensschild, Lebensbalken, Schaden zeigen,
Wachstumszeile (Haken), Nasen-Warnung rot; unten nur "Passiv". Auffaellig: im selben DE-Tooltip "+0,5" (Text) neben "+0.5%" (Zahl vom Code) -- R4.

## 6. Testanleitung berichtigt (`k1/anleitung_entwurf.md`)

- Schritt Selbst-Trinken: ein grosser Baer braucht 15 l fuer die volle Leiste -- 3 Flaschen (je 1 l, `Base.WaterBottle` Capacity 1.0) senken den
  Durst um ~20 Punkte, nicht "bis 0"; Wartezeit (eine Flasche je 10 Spielminuten) genannt.
- Look-Sperre: zweimal Look trifft zuerst die gemeinsame Unstuck/Look-Uhr (`S:server/BanditsNPCBearLook.lua:152-157`, Meldung in Minuten) -- der
  60-s-Grund kommt nur nach Wachsen; Schritt jetzt wie Kevins Fall vom 13.11. (neues Junges, `NCBear_CubGrow(55)`, sofort Look).
- Am Boden: vor dem zweiten `NCBear_FightDown()` aufhelfen; Hinweis auf die Einfrier-Sperre (Frage 2).
- Weiter als 70 Kacheln: vorher "Bleiben" (folgt er, kommt man nicht weg); ab ~76 Kacheln fehlt der "ruhen"-Satz (R5).
- `NCBear_CubNeedsInfo()` schreibt englisch "needs frozen: owner/sleep".
- Ergaenzt: Selbst fressen bis 0 (E), "satt fuer ~x %" im Fuettern-Menue (H), Kampf-Weigerung unter -70 und Herz bei +100 (V4), AnimTest ohne
  Schlaf-Schluessel (A), zu grosse Zahl im Zahlenfeld, Fusszeile ohne 50.

## 7. Restbefunde (eigene, alle minor, kein Blocker)

- **R1 (Bestand F4):** erstes Geben an einen leeren Baeren ohne Kopie + Absturz zwischen `GameWindow.save` (Register) und dem naechsten
  Spieler-Speichern -> doppelt (G1b; Test-Mod: 1 Nagel). Ursache `S:server/BanditsNPCBearInv.lua:281-284` (keine Kopie -> Register gilt) und
  `K.link` nur bei Inhalt (`:283`). K1 vergroessert nur die Menge je Aktion (bis 1000 statt 1). Vorschlag naechster Lauf: beim Abgleich IMMER
  verknuepfen (auch leerer Baer), dann liegt nach dem Laden binnen 10 s eine leere Kopie mit Fassung beim Spieler und "Register neu, Spieler
  alt" faellt auf die Kopie zurueck (Attrappe G1K zeigt, dass das mit Kopie haelt).
- **R2 (C3-Rest):** Kopf-Balken zeigt +-0,5 als "+1"/"-1", +1,5 als "+2" (`S:client/ISUI/BanditsNPCBearHud.lua:566-568`), das Fenster "+0.5%"/"+1.5%".
  Weil jede Vertrauens-Aenderung 0,5 ist, sieht Kevin in der Haelfte der Faelle zwei verschiedene Zahlen. Vorschlag: im Kopf dasselbe Format wie
  das Fenster (eine Nachkommastelle, wenn nicht ganz).
- **R3:** Vertrauens-Tooltip "jedes Mal um 10, wenn er zu Boden geht" (EN `UI.json:567`, alle Sprachen) -- seit C2 kostet es eingefroren nichts.
  Je nach Kevins Antwort (Frage 2) Text oder Code angleichen.
- **R4:** DE / FR / ES / PTBR / RU schreiben im Text "+0,5", der Code setzt Zahlen mit Punkt ein ("+0.5%", "4.5%", "9.6 l") -- im selben Tooltip
  gemischt (eigenes Bild). Schon Frage BAU_TEXTE 1.
- **R5:** Der Satz "Seine Beduerfnisse ruhen: ..." fehlt, wenn er nicht geladen ist (`counts` gibt dann keinen Grund, `S:server/BanditsNPCBearNeeds.lua:254-255`,
  `:518-523` setzt `nfz` auf nil) -- die Werte ruhen trotzdem (G3, F4-Bestand), nur die Anzeige sagt es nicht.
- **R6 (Bestand F3):** Hunger-/Durst-Tooltip "Ausgehungert: ... verliert Leben bis auf 1%" -- Leben sinkt erst bei 100 %, ab 80 % nur Schaden /
  Wachsen / Heilen (`S:server/BanditsNPCBearNeeds.lua:575-576`).

## 8. Jar-Ausnahmen im Staging (nur im Jar belegt) -- alle vor K1, keine neue

- `S:client/ISUI/BanditsNPCBearZz.lua:124` `a:getForwardDirection()` am Tier -- Kevins Wort 13.11.2026 Antwort 5 (F3; am Zombie/Spieler Lua-belegt,
  am Tier nicht). (`S:shared/BanditsNPCBearFoe.lua:201` am ZOMBIE ist Bandits-belegt, keine Ausnahme.)
- `S:shared/BanditsNPCBearInvRules.lua:243` getHeadCondition, `:248` getSharpness, `:256` setSharpness (A3); `:519` addExtraItem, `:527` setSpices (A4;
  addExtraItem inzwischen auch Bandits-belegt); `:529` setBurnt, `:530` setCooked (inzwischen Bandits-belegt), `:531` setCookingTime, `:533` setOffAge,
  `:534` setOffAgeMax, `:538` setFreezingTime, `:540` setFrozen (A2); `:660` getHue(), `:681` setHue (A10) -- Kevins Wort 13.11.2026
  `f4/KEVIN_ANTWORTEN.md:5-6` *"Ja, dieselben wie NPC Crew"*, Liste `f4/JAR_LISTE.md` Abschnitt 0 (Farbton im MP gesperrt bis "auch am Server").

## 9. Fragen fuer Kevin (kurz; gebaut ist jeweils die Empfehlung)

1. Satt = unter 1 % (du siehst 0 %); ein Rest unter 1 % aus der Hand zaehlt als 0. Gut so?
2. Am Boden -10: nur, solange seine Beduerfnisse zaehlen (du wach, nah, online) -- oder immer (dein Wort "jedes Mal")? Mein Rat: immer.
3. Der "Tag" fuer 1x-pro-Tag wechselt um 7 Uhr morgens (wie Vanillas Tageszaehler). Lieber Mitternacht?
4. Schild beim Aufrichten noch naeher an den Kopf (fester Abstand)?
5. Vertrauens-Balken negativ dunkelrot mit Mittelstrich -- passt der Rot-Ton?
6. Anzeige ab 75 % als "Hunger 80%" (Zahl mit Wort) statt bunter Balken -- so lassen?
7. Nasen-Warnung im Zahnrad rot (Vanilla "geht noch nicht") -- so lassen oder bis F5 ausblenden?
8. Zahlenfeld Geben "(1 - 93)": Grund dazuschreiben (Traglast bzw. 1000-Deckel)?
9. Vertrauen ueber dem Kopf als ganze Zahl ("+1" bei +0,5) -- oder genau wie im Fenster ("+0.5")? Mein Rat: wie im Fenster.
10. Dezimalzeichen: Text "+0,5", Zahlen vom Spiel "+0.5%" -- vereinheitlichen?
11. Geben aus einer Tasche: das Spiel holt jedes Stueck einzeln ins Hauptinventar (Vanilla), dann EINE Baeren-Aktion. Ok?
12. Spieler-Tagesbedarf 55 Hungerpunkte (ausgewachsen ~17 Steaks je volle Leiste) -- passt?
13. Bleibt er ueber 90 % bzw. auf 1 % Leben in den naechsten Tag, kostet auch der neue Tag wieder -5 / -10. So lassen?
14. Vorspulen im Einzelspieler friert seine Beduerfnisse ein (er schlaeft mit) -- wer viel vorspult, haelt ihn so satt. Ok?
15. Mit Beduerfnis-Tempo 0 bringt nur Streicheln Vertrauen. Ok?
16. Selbst trinken zeigt das Fress-Bild (echte Trink-Animation kommt mit "Wasser in der Welt"). Ok?
17. Worte des Vertrauens: Misstrauisch (unter -70) / Scheu / Neutral / Vertraut / Ergeben (ab +70) -- passen sie?
18. Fehler R1 (sehr seltenes Doppel nach Absturz beim ersten Geben an einen leeren Baeren) im naechsten Lauf beheben?

## 10. Dateien

- Bericht `k1/GEGEN.md`; berichtigte Anleitung `k1/anleitung_entwurf.md` (alt: `k1/gegen/anleitung_entwurf_vor_gegen.md`).
- `attrappe/k1_gegen/gegen.lua` (G1, G1K, G1W, G2, G3; Aufruf `lua5.1.exe gegen.lua`), `attrappe/k1_gegen/bestand_testmod.lua` (R1 an der Test-Mod),
  `attrappe/k1_gegen/zeichne_dump_gegen.lua` + `zeichnung_gegen.txt`.
- `k1/gegen/`: `lauf/` (alle Ausgaben), `diff/` (Unified-Diffs Test-Mod -> mod_k1), `bilder/` (eigene Fensterbilder + Lupen), `zaehle_staging.py`,
  `texte_paritaet.py`, `zeichne_gegen.py`, `alle_alten.sh`, `probe/` (Uebernahme-Probe, 74 MB, darf weg), `sicherung_k1_nach/`.

Statisch geprueft, nicht gespielt. Nach dem Einbau muss Kevin das Spiel neu starten (Lua laedt nur beim Start).
