# Lauf baer-talente -- Bericht GEGENPRUEFER (14.11.2026)

**Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und keinem Bericht geglaubt: jeden Befund am Code nachgesehen, alle Pruefer selbst
laufen lassen, eigene Stichproben am echten Kern und ein eigenes Fensterbild aus dem echten Code.
Geschrieben nur: `tal/GEGEN.md` (dieser Bericht), `tal/anleitung_entwurf.md` (berichtigt, Abschnitt 7), `tal/gegen_bild/` (Bild + Mal-Skript),
`tal/gegen_probe/` (Probe des Uebernahme-Skripts, 76 MB, darf weg), `attrappe/tal_gegen/` (Attrappen, Laeufe). Test-Mod, NPC Crew, Vanilla,
Bandits, `baer/tools`, `baer/NAEHTE.md` nur gelesen. Kein git, kein Download, kein Spielstart.
`S:` = `mod_tal/42/media/lua/`, `V:` = Vanilla `media/lua/`, `G:` = `attrappe/tal_gegen/`.

## 0. Ergebnis zuerst
- **Bereit fuer Kevins Einzelspieler-Test: JA.** Kein offener Blocker. Alle 17 Befunde sind geschlossen oder ehrlich als Frage an Kevin gefuehrt.
- Eigene Stichproben gruen (`G:gegen_kern.lua` 30 ok / 0): 3 Punkte durch Wachsen und Bitten vergeben -> Aussehen gewechselt -> "Absturz" (Register
  aelter als der Spiegel, Register ganz weg) -> geladen: **genau 3, alles andere gesperrt**, keine neue Punkt-Meldung; Dickes Fell bei
  **200/400 -> 325/650**, Reset zurueck 200/400; Krit-Zahl ueber den echten Client-Weg **Large, Gold (1, 0,84, 0,25), fett, "!"**.
- Nichts kaputt gemacht: alle alten Attrappen (K1, Kampf, Fix 1, F3 Schlaf, F4 Inventar, ...) geben gegen das Staging -- mit UND ohne Talent-Dateien --
  dieselben Ergebnisse wie gegen die Test-Mod, bis auf erklaerte Zaehler (Abschnitt 2).
- Testanleitung **berichtigt** (Schritt 7 war falsch, Schritte 2/3/5 ungenau -- Abschnitt 6).

## 1. Befunde -- geschlossen?
| ID | Urteil Gegenpruefer | Beleg (selbst gesehen) |
|---|---|---|
| C1 | **geschlossen als Frage.** Kommentar stimmt jetzt (`S:client/BanditsNPCBearFx.lua:37-44`): Large = groesste Stufe der UI-Schrift (EN 1x lineHeight 33 / Medium 29, 2x 40 / 33, selbst aus `media/fonts/EN/*/zomboid*.fnt` gelesen); `NewLarge` ist dieselbe Datei (`fonts/EN/fonts.txt`); `drawTextZoomed` steht nur als Definition `V:client/ISUI/ISUIElement.lua:1260`, kein Aufruf in Vanilla. Randnotiz: SDF-Schriften (SdfBold lineHeight 45) gibt es auch, Vanilla setzt sie aber nur in Karten (`V:client/ISUI/Maps/ISMapDefinitions.lua:80`) und PZAPI ein -- kein drawText-Beleg, also richtig nicht benutzt | Kevins Frage 2 |
| C2 | **geschlossen.** Drossel `"|Talent|ok"` weg (`S:server/BanditsNPCBearTalent.lua:82-114`), Ablehnungen bleiben gedrosselt (`refuse` :52-57) | `G:gegen_kern.lua` G5: Server, 20 Bitten in 0 ms bei 2 verdienten -> genau 2; bei 3 verdienten -> genau 3 |
| C3 | **geschlossen.** `dropKey` streicht "fisher" vor `B.TalentFix` (`S:server/BanditsNPCBearTalent.lua:216-259`). `B.TalentFix` nimmt "fisher" weiter an -- harmlos, das Register ist nur beim Schreiber, nur die Werkbank `B.TalentForce` kaeme dorthin | G5: MP-Spiegel "fisher,fur,paw" -> wiederhergestellt "fur" (g gedeckelt 0,10 -> 1 Punkt) |
| C4 | **offen als Frage**, gebaut = Spieltag (`S:shared/BanditsNPCBearTalentRules.lua:249-262`); Sandbox-Text sagt ehrlich "hoechstens einmal je Spieltag" | Kevins Frage 3 |
| C5 | **geschlossen.** `local NL = "\n"` (`S:client/BanditsNPCBearTalentData.lua:276`), kein `string.char(` mehr. Vanillas `ISModalDialog.CalcSize` teilt per Java-Regex am echten Umbruch (`V:client/ISUI/ISModalDialog.lua:170`) | eigenes Bild: Ja/Nein mit 3 Zeilen |
| C6 | **geschlossen.** Tagesbedarf x `talFrugalK` nur in der Anzeige (`S:client/BanditsNPCBearWinData.lua:794-806`); Mahlzeit/Schale rechnen weiter mit der vollen Leiste | Rechnung: 16 Wachstunden x 6,25 x 2/3 = 66,7 % einer Leiste je Tag = 2/3 |
| C7 | **offen als Frage**, gebaut = Umwerfen ab halbstark + doppelter Flug (`S:server/BanditsNPCBearFight.lua:867-876`). Der Tooltip sagt es Kevin offen ("Ab halbstark werfen ... sie um (100%)"). Ohne Umwerfen wirkt das Talent bis "kraeftig" nicht: halbstark hat `knockPct 0` (`S:shared/BanditsNPCBearFightRules.lua:136-140`) | Kevins Frage 4 |
| C8 | **geschlossen.** `tal/werkzeug_kern/sandbox_texte.py`: 0 x 특성, 5 x 재능 | grep |
| P1 | **geschlossen (major).** Lastsack mit zugebundenem Hals, kein Buegel -- im Blatt klar vom Schloss zu trennen (`tal/bilder/KEVIN_icons_gross.png` selbst angesehen). Der kleine Flicken auf dem Sack liest sich als Aufnaeher, nicht als Schloss | Kevins Frage 1 |
| P2 | **geschlossen.** Eigene Messung (Median des Medaillon-Rands r 40-44 px, Lab): kleinster Abstand **11,5** (Fell/Angler), dann 13,6 (Fell/Wachsam), 14,7 (Genuegsam/Pranke) -- vorher 5,6; Bericht 11,8 an anderer Messstelle, gleiche Aussage | `G:icons_messung_gegen.py` -> `G:lauf/icons_messung_gegen.txt` |
| P3 | **geschlossen.** waehlbar mit Alpha 1 (`S:client/ISUI/BanditsNPCBearTalentTab.lua:262`) | eigenes Bild: waehlbar farbig hell, gesperrt grau + Schloss |
| P4 | **offen als Frage** (56 px in 1080p) | Kevins Frage 5 |
| P5 | **geschlossen.** DE "Später" (`S:shared/Translate/DE/UI.json`), DE-Fenster 802 x 644 wie EN-Hoehe | eigene Mitschrift: alle DE-Szenen 802 x 644, FR 862 x 644 |
| P6 | **so gelassen, einverstanden** (1280 x 720 mit Schrift 2x: 734 px, Fusszeile lesbar; seltene Einstellung) | Bericht-Messung, Code unveraendert |
| P7 | **geschlossen.** Die Bilder-Kette laedt Vanillas echtes `ISModalDialog.lua`; ich habe dieselbe Kette mit eigenen Szenen benutzt: mehrzeiliger Text als linksbuendiger Block, Knoepfe aus Vanilla | `tal/gegen_bild/GEGEN_talente_1080.png` |
| P8 | **geschlossen.** `SMALL_MAX = 64` (`S:client/ISUI/BanditsNPCBearTalentTab.lua:42`): 70 px bei 1,25 kommen aus der 128er | Code |
| P9 | **so gelassen, einverstanden** (Hof ausserhalb der Kachel hoechstens Deckkraft ~0,12) | Code `:257-259` |

## 2. Etwas kaputt gemacht? (K1, Kampf, Fix 1, Inventar, Schlaf)
- Alle alten Attrappen selbst laufen lassen (`G:alle_gegen.sh` = Kopie von `attrappe/tal_nach/alle_nach.sh`, eigene TMP-Ordner; MIT Talent-Dateien,
  OHNE, Test-Mod) -> `G:vergleich_lauf.txt`: **204 gleich**; meine Datei ist bis auf 2 Zeilen (gemessene Lua-Zeit in `pruef_f2`) gleich der der
  Nachbesserung. Die "ANDERS"-Zeilen selbst gelesen, alle erklaert: B.OPTS 14 -> 16 (`A14`, `K25` -- 2 neue Regler gewollt), U.EN-Big-Fassungen 84 -> 85
  (neuer Text `UI_BN_Bear_Note_TalentPointBig`), Pfadzeilen der Simulatoren, ein Absturz `isAsleep` in `f3_pruef` steht GLEICH auch gegen die Test-Mod.
  K1 (`k1_kern` 153/0, `k1_gegen` 50/0, `k1_ober` 134/136 ok), Kampf (`kampf_baer` 118/0, `kampf_zomb` 73/0, `kampf_nach` 41/0), Fix 1 (`fix1bau` 105/0,
  `oberfix1` 200/0), F4 Inventar (`f4_kern` 227, `f4_gegen` 31/0) gleich wie gegen die Test-Mod.
- Inventar: Lasttier aendert nur die Kapazitaet (`S:shared/BanditsNPCBearInvRules.lua:882-886`, beide Aufrufer `S:server/BanditsNPCBearInv.lua:153`,
  :820), kein Gegenstand wird angefasst. Schlaf: nur mit Wachsam `s.wokeUntil = nil` und Weckweite x 1,5 bis `zedSense` (`S:server/BanditsNPCBearSleep.lua:269-271`, :338-345).
- Dickes Fell: das Leben am Tier ist ein Anteil (`B.BodyHp` gleicht `rec.hp` mit `a:getHealth()` ab, `S:server/BanditsNPCBearGrow.lua:253-283`) --
  mehr hpMax aendert den Koerper nicht, "Prozent bleibt" stimmt auch an der Engine.

## 3. Kevins Antworten am Code
| Kevin | Code |
|---|---|
| Freie Wahl, 3 von 9, keine Reihen | `B.TalentCan` ohne Reihen (`S:shared/BanditsNPCBearTalentRules.lua:189-199`) |
| genau 3 Punkte (10 % / halbstark / ausgewachsen), nie mehr | `B.TalentEarned` aus g, drei Schwellen, Deckel `maxN` hart 3 (:52-57, :153-175); selbst gerechnet: Tag 10 -> 1, Tag 15 -> 2, Tag 100 -> 3 |
| nach 3 aktiven gesperrt, auch wenn ein Fehler mehr gaebe | "max" ZUERST (:192) |
| Reiter "Talente" / "Perks", "Talentpunkt" / "Perk point" | DE/EN UI.json |
| Vergeben per Knopf mit Vanilla-Ja/Nein | `ISModalDialog:new(0, 0, 350, 150, text, true, win, fn, 0, k, id)` (`S:client/ISUI/BanditsNPCBearTalentTab.lua:333`) wie `V:client/ISUI/ISWorldObjectContextMenu.lua:953`; Bitte erst bei `button.internal == "YES"` |
| aktiv leuchtet hell | Hof + `_on`-Bild + Goldrahmen (:256-260) |
| Reset nur Sandbox (aus), alle auf einmal, 0-30 Tage (1) | `BearTalentReset` / `BearTalentResetDays` (`S:shared/BanditsNPCBear.lua` B.OPTS, `sandbox-options.txt`), `B.HandleTalentReset` setzt `rec.tal = nil` |
| Werte "so wie besprochen" | B.CFG-Block: 16/24, +250, +30 % / x1,5, Flug x2, +50 kg, x1,5 + nie schlaftrunken, x2 / 6 h, 25 % x2, Angler 2 und gesperrt |
| Krit-Zahl gross in Gold mit "!" | eigene Mitschrift ueber `U.FightFx("hit", { crit = true })`: Large, Gold, zweimal 1 px versetzt, "-120!" |
| Icons 128 px, klar, Zustaende | 60 Bilder 64/128 + glow/lock/soon, Blatt angesehen |

## 4. Eigene Stichproben (`G:gegen_kern.lua`, 30 ok / 0 Fehler, Ausgabe `G:lauf/gegen_kern.txt`)
- **G1** SP, echter Weg (`B.Ask` -> `B.Handle`, `B.SlowTick`): Tag 0 Bitte -> "kein freier Punkt"; Tag 10 / 15 / 100 je GENAU eine Punkt-Meldung;
  fur, paw, crit gelernt; viertes (mule) -> "max"; alle uebrigen gesperrt.
- **G2** Aussehen-Knopf (`B.HandleLook`, neuer Koerper ncbeargrowngen): tal gleich, keine Meldung, Spiegel am neuen Koerper traegt "fur,paw,crit".
- **G3 Absturz:** (a) Register-Stand von "nach 2 Talenten" zurueckgesetzt, Sitzung weg, Koerper mit neuerem Spiegel -> Hirn-Takt bindet, der neuere
  Spiegel gewinnt -> **fur,paw,crit, frei 0, viertes max**, keine Meldung, Bitte "alert" -> max. (b) Register-Eintrag ganz weg -> `B.HealFromMark`
  stellt wieder her -> genau 3, gesperrt. (c) aelterer Spiegel ("fur") -> das Register bleibt bei 3.
- **G4 Dickes Fell:** Tag 100, Anteil 0,5: Sicht 50 % von 400 = **200/400**; lernen -> **325/650**, Anteil 0,5; Reset -> 200/400; zweiter Reset am selben
  Spieltag -> "Wartezeit".
- **G5 Mehrspieler** (Server-Attrappe): fremder Spieler -> "nicht dein Baer"; Bitte mit erfundenen Feldern (n, earned, tal) -> nur k zaehlt; 20 Bitten
  in 0 ms -> nie mehr als verdient; Angler gesperrt; veraenderter Spiegel mit Angler -> kein Angler.

## 5. Pruefer selbst gelaufen
- **4 Lua-Pruefer** auf allen 26 geaenderten/neuen Lua-Dateien (`G:lauf/pruefer4.txt`): luacheck 26 x 0 failed, scopecheck 26 x 0, luacheck_pz 26 x 0;
  localcount hoechstens **61 aktiv** (WinData) und **71 insgesamt** (`server/BanditsNPCBearRegistry.lua` Funktion ab :105; Foe-Datei 70) -- alle < 180.
  (Die Nachbesserung schrieb "63 insgesamt" -- nur eine falsche Zahl im Bericht.)
- **Attrappen dieses Laufs** selbst: `tal_kern/run.lua` 106/0, `tal_ober/run.lua` 127/0, `tal_pruef/pruef.lua` 40/0, `tal_nach/nach_kern.lua` 20/0,
  `nach_ober.lua` 16/0.
- **langcheck** acht Staging-Ordner: 0 Fehler, 3 Hinweise (`G:lauf/langcheck_acht.txt`). `texte_pruefen_tal.py` 0 Fehler (EN = DE = U.EN 655),
  `texte_pruefen_tal_acht_nach.py` 0 Fehler (CN-Zeichen alle in Vanilla-CN).
- **Uebernahme** selbst: Trockenlauf `--staging mod_tal` OK, 0 Fehler, 2 Warnungen (Bestand), 209 Dateien (`G:lauf/ue_trocken.txt`); `--probe tal/gegen_probe`
  OK, 0 Fehler, 2 Warnungen, Pruefer auf 58 kopierten Dateien gruen, langcheck des geschriebenen Stands 0 Fehler (`G:lauf/ue_probe.txt`). NPC Crew `git status` leer.
- **Staging nachgezaehlt** (eigenes Skript, MD5 je Datei): 250 Dateien auf der Platte = 250 in `tal/staging_dateien_tal.txt`, MD5/Bytes/Status alle
  gleich; 65 neu, 38 ueberschreibt, 147 gleich (davon 33 Modell-Dateien, **alle byte-gleich mit der Test-Mod -- keine Baeren-Modell-Datei geaendert**);
  60 Talent-Bilder; nichts nur in der Test-Mod. Test-Mod steht auf main 93ba693, sauber. Zeilenenden: alle geaenderten Dateien LF wie vorher, kein BOM.
- **Namen** (`aussehen/werkzeug/kollision.py`): BanditsNPCBearTalent, BanditsNPCBear_Talent, UI_BN_Bear_Talent/_Why_Talent/_Note_Talent, BearTalentReset,
  NCBearBenchTalent, BanditsNPCBearWinTalent, NCBear_Talent -- 0 Treffer in NPC Crew, Vanilla, Bandits.
- **Eiserne Regel:** neue Engine-Aufrufe der Talent-Dateien je mit Vanilla-Fundstelle selbst nachgesehen (getTimestampMs `V:server/Foraging/forageServer.lua:456`,
  ZombRand(100) `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25`, getSpecificPlayer(0) `V:client/Farming/CFarmingSystem.lua:45`, MeasureStringX
  `V:client/ISUI/ISButton.lua:450`, Events.OnGameStart `V:client/Chat/ISChat.lua:1186`, ISModalDialog s.o.). Keine Jar-only-Methode, kein pcall als Tarnkappe.

## 6. Fensterbild aus dem Code und Testanleitung
- **Eigenes Bild** `tal/gegen_bild/GEGEN_talente_1080.png` (Mitschrift `G:zeichne_gegen.lua` -> `G:zeichnung_gegen.txt`, gemalt mit den Funktionen von
  `tal/werkzeug_ober/zeichne_tal.py`, echte Spielschriften, echte Talent-Bilder, Vanillas ISModalDialog). Eigene Szenen: Junges Tag 3 (alles gesperrt,
  Angler "Später", "Nächster Talentpunkt in etwa 7 Tag(en)"), Junges Tag 12 (1 frei, Ja/Nein auf Genügsam), Übersicht mit Dickes Fell bei 50 %
  (**325 / 650**, Tooltip-Zeile "Talent Dickes Fell: +250 Leben"), "nach dem Laden" fur/paw/crit (Tooltip "Alle 3 Talentpunkte sind vergeben"),
  Französisch (längste Texte, 862 px breit, Ja/Nein "Oui"/"Non"), Krit-Zahl. Angesehen: kein Text über Text, nichts ragt aus dem Fenster.
- **Testanleitung berichtigt** (`tal/anleitung_entwurf.md`): Schritt 7 war falsch -- direkt nach dem Reset ist der Knopf grau, weil NICHTS gelernt ist
  (`resetOf`, `S:client/BanditsNPCBearTalentData.lua:188-207`), "in ... Std." kommt erst, wenn wieder ein Talent gelernt ist. Schritt 2/3: die
  Punkt-Meldung kommt mit dem 10-Minuten-Takt (`Events.EveryTenMinutes`, `S:server/BanditsNPCBearServer.lua:1222`), der Punkt am Reiter sofort; "fliegen
  weiter als vorher" stimmte am Halbstarken nicht (ohne Talent wirft er gar nicht um). Schritt 4: Angler mit Sanduhr. Schritt 5: + Speichern/Laden.

## 7. Restbefunde (klein, kein Blocker)
1. `NACHBESSERUNG.md` 3: localcount "63 insgesamt" -- richtig 71 (Registry), weiterhin weit unter 180.
2. `tal/bilder/KEVIN_icons_gross.png`: Zeilen-Titel "Kommt später / Coming later", im Spiel steht seit P5 "Später" -- nur die Beschriftung des Blatts.
3. C1-Kommentar nennt als groessere Schriften nur Zierschriften und drawTextZoomed; die SDF-Schriften fehlen in der Aufzaehlung (ohne drawText-Beleg, also ohne Folge).
4. P6 (1280 x 720 mit 2x: 734 px) und P9 (Hof 8 px ueber der Kachel, kaum sichtbar) bleiben bewusst.
5. Mehrspieler nur als Server-Attrappe; das Ja/Nein-Fenster setzt beim Schliessen das Spieltempo auf 1 (Vanilla `ISModalDialog.lua:47-49`) -- wie beim Schlafen.

## 8. Fragen fuer Kevin (gebaut ist jeweils die Empfehlung; "Ja, alle so" nimmt jede)
1. Lasttier als **Lastsack** (Magenta) -- passt?
2. Krit-Zahl: Large + Gold + fett + "!" genug, oder noch groesser (nur mit `drawTextZoomed`, ohne Vanilla-Aufruf -> braucht dein Wort)?
3. Reset "1 Tag": ab dem naechsten **Spieltag** (gebaut) oder volle 24 Stunden?
4. Schwere Pranke: doppelt so weit **und** Umwerfen schon ab halbstark (gebaut) oder nur doppelt so weit (wirkt dann erst ab "kraeftig")?
5. Symbolgroesse 1080p: 56 px (gebaut) oder 72 px (Fenster ~100 px hoeher)?
6. DE "Später" statt "Kommt später" -- ok?
7. Wachsam beim Verstecken/Wecken hoechstens 12 Kacheln; Angler als letzte Kachel -- ok?

## 9. Urteil
**Bereit fuer Kevins Einzelspieler-Test.** Nach dem Einbau (Integrator: Staging-Liste direkt vorher neu erzeugen, Sicherung vorher/nachher, nicht
waehrend Kevin spielt) muss Kevin das Spiel **neu starten**. Ungeprueft bleibt alles, was nur das Spiel zeigt: wie scharf die Symbole skaliert
werden, wie das Magenta wirkt, ob die Krit-Zahl im Getuemmel auffaellt, und der echte Mehrspieler.
