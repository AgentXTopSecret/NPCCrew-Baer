# Lauf baer-hp-b -- GEGENPRUEFER: Lebensanzeige Vorlage B (14.11.2026)

Grundlage: `hp/BAU.md`, `hp/PRUEF_CODE.md` (C1-C4), `hp/PRUEF_BILD.md` (P1-P7), `hp/NACHBESSERUNG.md`. Staging `_arbeit/baer_zaehmen/mod_hp`.
**Statisch geprueft, nicht gespielt.** Nach dem Einbau: Spiel neu starten (Lua laedt nur beim Start).
Kuerzel: `S:` = `mod_hp/42/media/lua/`, `A:` = `_arbeit/baer_zaehmen/attrappe/`, `G:` = `A:hp_gegen/`.

## Ergebnis

- **Sieht aus wie der Entwurf (Kevins Wahl B): ja.** Eigene Mitschrift des echten Codes, 4K / Schrift 4x neben dem Entwurf gemalt: der Lebens-Block
  (Plakette, Rahmen, Segmente, Zahl, Farben, Kreuze, "+12", "-28", Nachlauf, Keule, Tropfen, Pflaster, Puls, Schein) ist in **allen 16 Vergleichs-Bildern
  pixelgleich** mit dem Entwurf (Abweichungen nur im Text darueber, hoechstens 12/255 Helligkeit; und die bekannte Zeile "Hunger 100%", F2).
- **Befunde:** C1, C3, C4, P1, P2 **geschlossen**. **C2 nur teilweise** (Restbefund R1). P3-P7 begruendet nicht geaendert, als Fragen gefuehrt (P4 mit Bild).
- **Nichts kaputt gemacht:** vier Lua-Pruefer gruen, alle alten Attrappen 62/62 gleich + 25/25 OBERFLAECHE ohne neue FEHLER, Rueckfall ohne die neue
  Datei 18/18, langcheck 0 Fehler, Trockenlauf und Probe OK, Staging-Liste stimmt (279 Dateien, 0 Abweichungen).
- **Neu gefunden (minor):** R1 (Rest von C2) und R2 (Rundung bei der Bestaetigung). Beide behebt EINE Zeile je Stelle in `S:client/ISUI/BanditsNPCBearHpBar.lua`
  (:332 und :404) -- in einer Kopie im Scratchpad geprueft: alle hp-Attrappen gruen, 0 Befunde (`G:vorschlag_r1_r2.diff`). **Nicht** ins Staging geschrieben.
- **Bereit fuer Kevins SP-Test: ja** (R1/R2 sind kosmetisch und beim Standard-Baeren mit 400 Leben selten; Empfehlung: die zwei Zeilen vorher einsetzen).

## Je Befund

| ID | Urteil | Beleg |
|---|---|---|
| C1 major | **geschlossen** | `HpBar.lua:402`: Hunger/Durst nach ALTER oder NEUER Sicht, ohne `pct > 1`. `A:hp_nach/nach.lua` (von mir neu gerechnet, 4 Arten je 56 ok / 0): 2 -> 1 % Hunger und Durst, Abzug + Fressen im selben Takt -> orange "-4", kein Wackeln. Gegenprobe ohne Hunger bleibt Treffer. Original-Attrappe des Pruefers: P10/P11 jetzt "ok-kein-Befund" (`G:pruef_orig_kern.txt`). |
| C2 major | **teilweise** | Fuer Treffer bis 0,5 % der Leiste geschlossen (`HpBar.lua:404`, `nach.lua` "351/400 steht 9 s"). Fuer Treffer **zwischen 0,5 und 1 %** -- genau der Fall des Befunds (Zombie 4,8-7,2 Punkte bei 600-850 Leben) -- **nicht**: die Bedingung `st.vp - st.pred <= 0,5` greift dort nicht, nach 6 s gilt wieder die Sicht. `G:gegen.lua` (echter Code, Schreiber-Modell Sicht = floor(hp x 100 + 0,5) wie `S:server/BanditsNPCBearGrow.lua:976`): G1 ein Treffer 3 von 400 (0,75 %) -> "349/400", **nach 6000 ms "352/400"** ohne Heilen; G3 Kampf 850 Leben, letzter Treffer -> nach 6 s **717 -> 723**. -> Restbefund R1. |
| C3 minor | **geschlossen** | `onDrop` (`HpBar.lua:327`). `nach.lua` C3a (Fuellung 50/50/50, zwei Zahlen), C3b (Sicht 4,5 s spaet: ein Effekt), C3c (Hunger 2 s nach Treffer: orange "-4"). Pruefer-Original P2/P4/P6 "ok-kein-Befund". Grenze (ehrlich im Bericht): Sicht spaeter als 6 s nach dem Fx gibt weiter einen zweiten Effekt. |
| C4 minor | **geschlossen** (Empfehlung gebaut, Frage F5) | `HpBar.lua:414-422`, `own` aus `Hud.lua:534` (`ownOf`, gleich wie die K1-Auto-Zeilen). `nach.lua` C4: fremd ohne Sinken keine Keule, nach Sinken Keule, nach 1,25 h ohne Sinken aus, eigener Baer sofort. Weltstunden `B.Now()` = `getGameTime():getWorldAgeHours()` (Client-Fundstelle Vanilla `client/Challenge/WinterIsComing.lua:8` geprueft). |
| P1 major | **geschlossen** | `client/BanditsNPCBearFx.lua:141-148`: Unterkante 2 px ueber dem Stapel (`U.TagTop`), gleicher Anker wie das Schild (Fx: `U.TagLift x U.PoseLift`, Hud :1017: `tagZ x zk x PoseLift`, `U.TagLift` = `tagZ x zkOf`). `nach.lua` P1 in 1x und 4x. **Bild:** "AUSGEWICHEN" steht ueber "Bär von Dee" (Blatt, Teil "Nur GEBAUT"). `getFontHeight(UIFont.Medium/Large)`: Vanilla `ISAddSafeZoneUI.lua:8` / `ISAdminTicketsUI.lua:6` geprueft. |
| P2 minor | **geschlossen** | `Hud.lua:638-649` misst die Zeile ueber dem Block einmal je Liste (`MeasureStringX(Schrift, Text)`, Vanilla `ISButton.lua:450` geprueft); `HpBar.lua:721` / `:744-748`. **Bild:** "-28" steht rechts neben "zu müde -- weicht zurück" mit Abstand; kurze Texte pixelgleich wie der Entwurf. Nebenwirkung siehe H1. |
| P3 minor | Frage F7 | Bestand (Schilder an Weltankern); nicht geaendert -- nachvollziehbar. |
| P4 minor | Frage F10 | Bild mit Code-Anker `hp/nach/bild/aufrichten_4k_4x.png` angesehen: Block 157-174 px ueber dem Kopf. Mein Blatt sagt das in der Kopfzeile. |
| P5 minor | Frage F8 | Bestand (Vorgabe "Aus"); nicht geaendert. |
| P6 minor | Frage F9 | wie der Entwurf; nicht geaendert. |
| P7 Hinweis | Frage F2 | im Blatt sichtbar ("Hunger 100%" / "Durst 100%" ueber dem Block). |

## Restbefunde (neu)

- **R1 (minor, Rest von C2):** Ein Treffer zwischen 0,5 und 1 % der Leiste, der die ganzen Prozent der Sicht nicht aendert, springt nach `Z.PRED_MS`
  (6 s) zurueck: Zahl und Fuellung steigen um 3-6 Punkte ohne Heil-Effekt. Betrifft starke Baeren (ab ~480 Leben: Vitalitaet, Dickes Fell) bei
  Zombie-Treffern -- einzeln oder als letzter Treffer eines Kampfs. Grund: die Sicht rundet den WAHREN Wert (+-0,5), die Vorhersage geht vom
  GERUNDETEN aus (+-0,5); mit gleicher Sicht ist die Vorhersage stimmig, solange `vp - pred < 1`. **Vorschlag** `HpBar.lua:404`:
  `st.vp - st.pred < 1 - Z.EPS` statt `<= 0.5 + Z.EPS`.
- **R2 (minor):** Bestaetigt eine Sicht die Vorhersage und liegt bis 0,5 % DARUEBER, loescht `onDrop` (`:332`) die Vorhersage und zeigt die gerundete
  Sicht. Im Einzelspieler (Sicht im selben Bild) sinkt die Zahl dann bei einem kleinen Treffer gar nicht oder einmal um 1 % mehr (G2, 650 Leben, 10 x 3:
  `572 569 566 563 559 559 556 ...` -- Treffer 5 aendert die Zahl nicht, obwohl "-3" schwebt); im Mehrspieler (Sicht ~0,3 s spaeter) steigt sie kurz nach
  dem Treffer um 1-4 Punkte (G4: 3 von 10 Treffern +1). **Vorschlag** `:332`: `if dn or to <= p + Z.EPS then st.pred = nil end` (Vorhersage behalten,
  solange die Sicht sie nicht unterschreitet).
  Mit BEIDEN Zeilen (Kopie im Scratchpad, `G:gegen_mit_beiden_fixes_kern.txt`): G1-G5 0 Befunde, G2 `572 569 566 563 559 556 553 550 547 544 541`,
  `nach.lua` 56/0 (1x, 4x), `hp_bau/run.lua` 116 ok + 1 Fehler (nur "Bild fehlt" -- die Kopie hatte keine Bilder), Pruefer-Kopie 12/0/0.
  Nebenwirkung: die Zahl im Balken kann bis 1 % unter der Zahl im Baeren-Fenster stehen (die Vorhersage ist genauer als die gerundete Sicht).
- **H1 (Hinweis, Folge von P2):** Unter einem langen Zustand ("streift umher", "zu müde -- weicht zurück") bleiben 6-7 der 8 Heil-Kreuze an der
  Rahmen-Oberkante stehen (sie starten schon unter `top + arm` und werden dort festgehalten) und blinken an Ort und Stelle; sie decken keinen Text,
  liegen aber auf der Bronze-Kante. Bei kurzen Zustaenden ("folgt", "kämpft", "schläft") wie der Entwurf. Im Blatt: "langer Zustand + Heilen".
- **H2 (Testanleitung):** berichtigt (unten).

## Bilder (Regel "aus dem echten Code")

- **Kette:** `G:zeichne_dump_gegen.lua` (eigene Mitschrift: Staging mod_hp ueber `A:hp_bau/hp_welt.lua` + Vanillas ISPanel-Attrappe mit echten Schriftmassen,
  echter Kern, deutsche Texte; zwischen den Aufnahmen laeuft die Anzeige wie im Spiel alle 50 ms weiter) -> `hp/gegen/tmp/zeichnung_gegen_<1x|4x>.txt` ->
  `hp/gegen/zeichne_gegen.py` (eigener Maler; echte Spielschriften `media/fonts/EN/<1x|4x>/zomboid*.fnt` ueber den BMFont-Leser `f1_entwurf/zeichne_fenster.py`,
  Bilder des Stagings 1:1, Kevins Spielbild `baer/begleiter/kevin_rear_bauch_1113.webp`). Entwurf-Spalte: `baer_hp_entwurf/B/zeichne.py` (nur gelesen,
  ohne .pyc; Entwurfs-Ordner danach unveraendert).
- **`hp/bilder/KEVIN_hp_B_gebaut.png`** (1876 x 8412): 4K / Schrift 4x 1:1, ENTWURF | GEBAUT in 16 Zeilen (Stufen 100/60/30/10; Heilen +0,12/+0,55/+1,10 s;
  Treffer +0,06/+0,20/+0,45 s; Hunger 0,8/1,3/1,9 s; Hunger + Durst; fast leer Puls oben/unten), darunter "Nur GEBAUT" (nur Durst, AUSGEWICHEN zweimal,
  am Boden, langer Zustand + Treffer, langer Zustand + Heilen) und 1080p / Schrift 1x (8 Zeilen).
- **`hp/bilder/KEVIN_hp_B_gebaut.gif`** (1286 x 380, 20 Bilder/s, 9,6 s Schleife): links Entwurf, rechts Gebaut -- Heilen, Treffer, Hunger, fast leer.
- **Angesehen** (Ausschnitte `hp/gegen/tmp/blatt_*.png`, Lupen, GIF-Mitten): gleich bis auf "Hunger 100%" (F2). **Gemessen** (`hp/gegen/vergleich_gegen.py` ->
  `hp/gegen/tmp/vergleich_gegen.txt`): 4x Abweichung nur im Text ueber dem Block (12-133 px, hoechstens 12/255), Block und Effekte 0 px; Hunger-Zeilen
  wegen der Auto-Zeile verschoben; 1x zusaetzlich 1 px Abstand Zustand -> Block (Bauer-Unterschied 2, gewollt).

## Pruefungen (Ausgaben unter `G:`, `hp/gegen/`)

- **Vier Lua-Pruefer** (`G:pruefer4.txt`, 5 Dateien): luacheck 0, scopecheck 0, luacheck_pz 0; localcount hoechstens 80 aktiv / 106 insgesamt (`U.HpBarDraw`).
  Zeilenenden LF, nur ASCII (wie die Test-Mod). Kein `pcall`; jeder Engine-Aufruf mit Vanilla-Fundstelle, alle neun Fundstellen nachgelesen.
- **hp-Attrappen** neu gerechnet: `hp_nach/nach.lua` 56/0 in allen 4 Arten; `hp_bau/run.lua` 116/0 bzw. 117/0, 4x je 19/0; `server_pts.lua` 7/0;
  Pruefer-Original 11 ok / 1 Fehler / 1 Befund (gewollt, siehe NACHBESSERUNG), Pruefer-Kopie 12/0/0.
- **Eigene Attrappe** `G:gegen.lua`: 3 Befunde (G1, G3 = R1; G4 = R2), Gegenprobe G5 gruen; mit Vorschlag 0 Befunde.
- **Alle alten Attrappen** (`G:alle_alt_hp.sh`, Kopie mit eigenem TMP, 5 min): **62 von 62** gleich Staging/Test-Mod (`G:vergleich_hp.txt`), OBERFLAECHE 25 von 25
  ohne neue FEHLER (`G:ober_alte_vergleich.txt`) -- beides byte-gleich mit dem Ergebnis der Nachbesserung.
- **Rueckfall** (`G:ohne_aus/vergleich.txt`): ohne die neue Datei 18/18 wie die Test-Mod, Aus/Zahl 12/12 gleich, Balken 6/6 anders -- je Attrappe und Kern.
- **langcheck** (8 Staging-Sprachen, `G:langcheck_acht.txt`): 0 Fehler, 3 Hinweise (Bestand); `shared/Translate` byte-gleich mit der Test-Mod (keine Texte).
- **Uebernahme** `baer/tools/baer_uebernahme.py --staging mod_hp`: Trockenlauf **OK, 0 Fehler, 2 Warnungen** (Bestand), 237 Dateien (`hp/gegen/ue_trocken.txt`);
  `--probe hp/gegen/probe`: **OK, 0 Fehler** (`hp/gegen/ue_probe.txt`); im Ziel HpBar/Hud/Fx/Hurt byte-gleich, 27 Bilder byte-gleich, keine Werkbank, kein `NCBear_Hp`.
- **Staging-Liste** (`hp/gegen/zaehle_staging.py` -> `hp/gegen/tmp/zaehle_staging.txt`): 279 Zeilen = 279 Dateien, MD5/Bytes/Status 0 Abweichungen; zu kopieren
  **32** (neu 29: HpBar.lua, NCBearBenchHp.lua, 27 Bilder; ueberschreibt 3: Fx, Hud, Hurt), 93 Modell-Dateien NICHT KOPIEREN (alle byte-gleich mit der
  Test-Mod), nichts nur in der Test-Mod. `mod_info_vorschlag_hp.txt`: haengt nur den hp-b-Satz an, LF, ASCII.
- NAEHTE.md / Uebernahme-Skript: nur Kopf-Absaetze, Zeile 53, `UI_ASSET` + "genannt"-Regel um `textures/BanditsNPCBear_Hp_` (gegen die Sicherungen
  `hp/NAEHTE_vor_hp.md.txt`, `hp/baer_uebernahme_vor_hp.py.txt` verglichen) -- stimmig.

## Testanleitung (`hp/anleitung_entwurf.md`, Stand vorher `hp/gegen/anleitung_entwurf_vor_gegen.md.txt`)

Berichtigt: Bild-Hinweis auf `KEVIN_hp_B_gebaut.png/.gif` (+ Schild steht im Spiel hoeher); Punkt 2 Menue heisst beim grossen Baeren "Bären heilen"
(`S:shared/Translate/DE/UI.json:132`, nicht "Junges heilen"); Punkt 4 "sinkt jedes Mal um 3" stimmt so nicht (R2) -- jetzt "springt nicht hoch", dazu R1 als
bekannter Fall; Punkt 5 / 6 Futter in SEINEM Inventar (ab Hunger 50 frisst er selbst); Punkt 8 Kreuze unter langem Text (H1); Schlusszeile Frage F7 -> F5.

## Fragen fuer Kevin (kurz)

1. R1/R2: die zwei Zeilen vor dem Einbau noch einsetzen? (Empfehlung ja -- dann springt die Zahl bei starken Baeren nie mehr hoch und sinkt immer genau um den Treffer.)
2. F10/P4: Im Spiel steht das Schild beim Aufrichten deutlich hoeher als in den Bildern. Fester Abstand (K1-Frage 4)?
3. F2/P7: "Hunger 100%" steht zusaetzlich zur Keule. So lassen?
4. H1: Bei langem Zustand blinken die Heil-Kreuze auf der Rahmenkante statt aufzusteigen. Ok so?
5. F7/P3, F8/P5, F9/P6, F5/C4, F1: wie in `hp/NACHBESSERUNG.md` (Empfehlung jeweils: so lassen bzw. erst spielen).

## Grenzen

Alles Attrappe unter Lua 5.1, kein Spiel. Das Schreiber-Modell in `G:gegen.lua` (wahres Leben, Rundung wie Grow.lua:976, Sicht sofort bzw. 300 ms nach dem Fx)
ist eine Vereinfachung; die echte MP-Verzoegerung ist ungemessen. Die Bilder zeigen den Anker des Entwurfs, nicht den Code-Anker (F10).
