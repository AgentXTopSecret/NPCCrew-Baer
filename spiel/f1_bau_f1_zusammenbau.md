# Lauf baer-f1: ZUSAMMENBAU + UEBERNAHME (F1 Baeren-Fenster auf V, Befehle Sitz/Frei/Komm her/Passiv/Unstuck, Namensschild je Baer, B1e-Reste)

Stand 11./12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (B1a-B1e +
F1 KERN + F1 OBERFLAECHE, Berichte `bau_f1_kern.md`, `bau_f1_oberflaeche.md`, Abweichungen `schnittstelle_aenderungen.md` "F1 KERN" /
"F1 OBERFLAECHE"). Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart, kein Download.
**Im Staging wurde nichts geaendert** (keine Luecke ueber die Grenze gefunden). Geschrieben: `attrappe/gesamt/run.lua` (Umgebung ergaenzt,
FILES + 7, 17d gewollt geaendert, neu Abschnitt 21), `attrappe/gesamt/xref_f1.py` + `xref_f1.txt`, `attrappe/gesamt/gegenprobe_f1.py` +
`gegenprobe_f1.txt`, `attrappe/gesamt/ergebnis.txt`, `ergebnis_probe.txt`, `attrappe/uebernahme_f1/probe_regeln_f1.py` + `.txt`,
`attrappe/pruef_b1b/ergebnis_f1.txt` (Vergleichsstand), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `staging_dateien.txt`,
`mod_info_vorschlag.txt`, Absatz "F1 ZUSAMMENBAU" in `schnittstelle_aenderungen.md`, Probe unter `probe_f1/`, Ausgaben `trockenlauf_f1.txt`,
`trockenlauf_f1_vor_b5a.txt`, `probe_f1_ausgabe.txt`. Nach dem Einbau muss Kevin das Spiel **neu starten** (neue Lua, neue Taste).

## 0. Ergebnis

| Pruefung | Ergebnis |
|---|---|
| Vorab: Test-Mod gegen die B1e-Liste (MD5) | **60 von 60 gleich** (Test-Mod unveraendert seit 914ee79); Staging jetzt 67 Dateien = 60 + 7 neue F1-Dateien; jede MD5, die die Bauer in ihren Berichten nennen, stimmt mit dem Staging |
| Grenze KERN <-> OBERFLAECHE (`attrappe/gesamt/xref_f1.py`, neu) | **0 Luecken**, 3 Hinweise (die bekannten Rueckfallwerte in Rules.lua) -- `xref_f1.txt` |
| Gegenprobe (`gegenprobe_f1.py`, Temp-Kopie, je eine Verderbnis) | **27 von 27 erkannt** (15 x xref, 12 x Gesamt-Attrappe) -- `gegenprobe_f1.txt` |
| Gesamt-Attrappe `attrappe/gesamt/run.lua` | **2329 bestanden, 0 Fehler** (vorher 1672): +266 Lade-Pruefungen (7 neue Dateien x 38 Ladevorgaenge in 1-20), Abschnitt 21 neu mit 391 Pruefungen (231 Ablauf + 160 Lade); 17d gewollt geaendert; `***`-Zeilen weiter nur die drei gewollten Heilungen 18c, 19f, 20e; in 21 keine |
| dieselbe gegen die Probe (`probe_f1/NPCCrew/42/media/lua/`) | **2329 / 0**, `ergebnis_probe.txt` **byte-gleich** mit `ergebnis.txt` |
| Attrappen der Bauer auf dem Endstand | kern 136/0, b1b_kern 204/0, b1c_kern 192/0, b1d_kern 162/0, b1e_kern 153/0, **f1_kern 188/0** (alle wortgleich mit ihrem `ergebnis_f1.txt` bzw. `ergebnis.txt`; b1d_kern nur der Pfad-Vorsatz der Fehlerzeile anders); ober 116 + 117, b1b_ober 144 + 134, b1c_ober 155 + 142, b1d_ober 174 + 176, b1e_ober 230 + 230, **f1_ober 359 + 359** (Kern-Attrappe + echter Kern), je 0 Fehler |
| Pruef-/Nachbesserungs-Attrappen | pruef_b = `ergebnis_b1b_nach.txt`; pruef_b1b `run_nach` = `ergebnis_b1c.txt` + genau die eine erwartete Zeile des AnimalID-Riegels (KERN Nr. 13; neu gespeichert als `ergebnis_f1.txt`); pruef_b1c, pruef_b1d (10/0, 3 Befunde), pruef_b1e `run_nach` 25/0, nach_b1e 31/0 je wortgleich; pruef_b1e `run.lua` 20/5 wie seit `nachbesserung_b1e.md` :96 dokumentiert |
| Text-/Beleg-Pruefer | `texte_pruefen*.py` (ober, b1b, b1c, b1d, b1e, f1) je **FEHLER gesamt: 0**; `belege.py` 0/112, `_b1b` 0/51, `_b1c` 0/89, `_b1d` 0/23, `_b1e` 0/53, `belege_f1.py` 0 Fehler (85 Belege); `bilder_pruefen_b1e.py` lief hier nicht (numpy fehlt in diesem Python) -- die Bilder sind MD5-gleich mit B1e |
| Lua-Pruefer (32 Lua-Dateien des Stagings) | luacheck 32 / 0 failed, scopecheck 0, localcount hoechstens **51 aktiv** (Hud) / **77 insgesamt** (World.lua, unveraendert), luacheck_pz 20 x W113 = die bekannten (17 Bench, 3 Aktionsklassen); luac5.1 -p alle ohne Fehler; alle LF, reines ASCII, LF am Dateiende |
| Trockenlauf `--staging ... --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen** (24 Altlasten + 2 `ALT_DEFS` + 1 Clip-Warnung GLB + 1 NPC-Crew-Kommentar; vorher bei den Bauern 5 Fehler = die geplanten Naehte) |
| Trockenlauf ohne `--vor-b5a` | **26 Fehler = genau die 24 Altlasten + 2 `ALT_DEFS`** ("Erwartet rot ... sonst nichts") |
| Gegenprobe der Skript-Regeln | `probe_regeln_f1.py` **10 von 10 wie erwartet** (9 Verderbnisse erkannt, unveraendertes Staging gruen); `probe_regeln_b1e.py` weiter 8 von 8 |
| Probe `--probe probe_f1 --staging ... --vor-b5a` | **OK -- 0 Fehler, 28 Warnungen**; 70 Dateien geschrieben (31 Lua, 17 Modell/Textur/Skript/Knoten/Bild, 21 Texte, `sandbox-options.txt`); luacheck/scopecheck/localcount je kopierter Datei gruen (hoechstens 77), luacheck_pz 0 Treffer + 3 erlaubt |
| `staging_dateien.txt` neu | **67 Dateien: 7 neu, 30 ueberschreibt, 30 gleich** (gegen NCBearTest 914ee79); gegen die B1e-Liste: 7 neu, 30 geaendert, 30 unveraendert |

## 1. Grenze KERN <-> OBERFLAECHE

### 1.1 Werkzeug `attrappe/gesamt/xref_f1.py` (neu; `xref_b1e.py` prueft den B1e-Plan und meldet F1 als 29 Luecken)
Aufruf `python -I xref_f1.py [lua-Ordner]` (Vorgabe Staging), Exit 1 bei einer Luecke. Alles aus `xref_b1e.py` (Abschnitte 1-9) plus:
1. **B.*/U.***: 217 / 217 Namen definiert, U.* 52 / 52; **130 Funktionen** je in ihrer Datei (neu: Order.lua OrderStep/StandStep/ComeCheck/
   HandleCome/HandlePassive/ReviveMissing, Rules.lua ModeOf/OrderDecide, World.lua RoamSpot, Follow.lua HandleMode; Key WinKeyName, WinData
   WinBears/WinModel/WinStatics, WinParts WinFonts/WinColor/WinRamp/WinBtn/WinRow/WinTick/WinFrame/WinRect, Window WinOpen/WinClose/WinToggle/
   WinIsOpen/WinOnView/WinLayout, Pose PoseTick/PoseOnView/PosePhase, Tags TagOn/TagSet/TagLoad, Client WhyText, Hud CubObj). Die OBERFLAECHE
   ruft vom KERN nur die Liste aus Plan 7.5 (neu `ACT`, `DirOf`); Bench (Plan 7.8) ruft FindAnimal/RemoveCub/_s, alle definiert. Ladefolge:
   0 Aufrufe auf Dateiebene vor ihrer Definition.
2. **B.CFG** (192 Felder, 190 gelesen; nie: `markerDur`, `orphanMs` wie bisher): die 12 Stellwerte aus Plan 6.1 **mit ihren Zahlen**, alle
   gelesen (neu erkannt: die lokalen Leser `cfgNum("feld", vorgabe)` in Order.lua/WinData.lua, Rueckfall = B.CFG); `B.MODES` =
   follow/stay/sit/roam. **Sandbox**: 28 Optionen, `BearRoamRadius` integer 12 (4..30) direkt vor `BearLog`, B.OPTS textgleich.
   **Optionen-Seite**: `WinSize` (7 Eintraege Auto/100..300 %, Vorgabe Auto) nach `MarkerSize`; der Leser `U.Opt("WinSize", 1)` hat dieselbe
   Vorgabe.
3. **Befehle**: Come `{ id }`, Passive `{ id, on }` haben ihren Empfaenger (`B.Handle` -> `B.HandleCome` / `B.HandlePassive`); `on` ist im
   Fenster `not (v.pas == true)` (Wahrheitswert), der Schreiber verwirft alles andere still; die Mode-Werte des Fensters (`CMDS`) liegen alle in
   `B.MODES`; Unstuck ist die B1c-Bitte `Call { id }`. Schreiber liest `args.id`/`mode`/`name`/`on` -- jedes schickt ein Client.
4. **Sicht**: viewEntry baut `mode pas u ld hide sit cm busy` (auch als `t.<feld> = ...`), B.GrowView fuer tame UND missing mit
   `x* carry dodge fgtB fish nose` (die Erfahrungs-Felder ueber `VIEW_X`); jedes `c.`/`v.`-Feld der OBERFLAECHE ist gebaut (ausgenommen die
   Farb-Felder des Schliessen-Knopfs in Window.lua, dort heisst der Knopf `c`).
5. **Texte**: UI.json 274 je Sprache (272 `UI_BN_Bear_*` + 2 Tasten-Schluessel), Sandbox.json 62, IG_UI.json 4; Paritaet, Platzhalter, `%%`,
   sortiert, Round-Trip, BOM/CR in 7 Sprachen; die **106 F1-Schluessel mit Plan-Text + 9 ohne** x 7 Sprachen vorhanden, **EN wortgleich mit
   Plan 7.6** (mit den dokumentierten Abweichungen Win_BodyBear, Win_Hint mit %1); die zwei Tasten-Schluessel gebaut aus `NAME`/`HEAD` in Key.lua
   wie Vanilla (MainOptions.lua:2159-2177) und in allen 7 Sprachen; kein anderer Schluessel ausserhalb `UI_BN_Bear_*`; `U.EN` == EN fuer alle
   `UI_BN_Bear_*`; 0 EN-Schluessel unbenutzt (Big-Fassungen auch ueber `B.NoteBd({ k = ... })` und `note(k, ...)` mit Variable k erkannt).
6. **Meldungen**: die 8 Meldungen aus Plan 7.4 + `Why_Gone` / `Note_Dead` (4a) gehen im KERN durch `B.NoteBd`, je mit Big-Fassung (21 Meldungen
   mit bd insgesamt).
10. **Neu -- Taste, Fenster, Sitz**: genau drei Tasten-Stellen im Mod-Code (Key.lua:41 `Keyboard.KEY_V`, Key.lua:96 `Events.OnKeyPressed`,
   Window.lua:543 `Keyboard.KEY_ESCAPE`); Name "Bear window" in Key.lua = Window.lua; layout.ini-Name `BanditsNPCBearWindow`, Datei
   `BanditsNPCBear.ini`; Sitz-Treiber setzt `sit`/`sitdown`/`standup` an `NCBearAct` = m_Value der drei Knoten der Test-Mod (je genau eine
   STRING-Bedingung), Marke `NCBearDone` = Ereignis der Knoten; **Clips in BEIDEN GLBs gemessen**: Junges (Staging) und grosser Koerper
   (`NCBear.glb` der Test-Mod) je `NCBear_SitDown` 1,6 s, `NCBear_Sit` 4,0 s, `NCBear_StandUp` 1,3 s -- `SIT_DOWN_MS` 1700, `STAND_UP_MS` 1400,
   `standMs` 2300 sind laenger (Plan 13 nannte die Laengen "angenommen": jetzt belegt); `B.PlaceCub(` nur aus BodySwap / ReviveMissing /
   RideStep (2x) / HandleCall; kein pcall, kein `next(`, kein Testwort in den 7 neuen Dateien; kein `getVariableString` im Mod-Code;
   `B.SKILL_FIELD` (Stats) == `SKILL_FIELD` (WinData) == `VIEW_X` (Grow).

**Gegenprobe** (`gegenprobe_f1.py`): xref -- viewEntry ohne sit, GrowView nur fuer tame, Passiv-Meldung ohne B.NoteBd, Come ohne Empfaenger,
Passive.on als Text, RU ohne Win_St_Sit, EN Note_Sit anders, CN ohne Tasten-Schluessel, standMs 1000, SIT_DOWN_MS 1000, Treiber setzt
"sitting", zweite Taste im Fenster, BearRoamRadius Vorgabe 8, Erfahrungs-Feld falsch, PlaceCub aus dem Fenster -> **15 von 15 erkannt**.
Gesamt-Attrappe -- Sitz setzt sich nie (17 Fehler), Treiber schreibt nichts (9), Passive immer verworfen (13), C1 aus (11 + Abbruch), Unstuck
grau fuer Vermisste (7 + Abbruch), Komm her kommt nie an (1), Taste ohne Doppel-Riegel (2), Esc schliesst nicht (4), Bleiben ohne OrderStep
(2, in 17d), Namensschild nicht gespeichert (3), Lage mit visible (1), Passive-Klick sendet immer an (4) -> **12 von 12 rot**.

### 1.2 Von Hand nachgesehen (was ein Grep nicht sieht)
- **Ladefolge Client**: Window.lua und WinParts.lua leiten auf Dateiebene von `ISPanel`/`ISButton` ab (Vanilla laedt beide vorher); Key.lua
  legt die Tasten-Zeile auf Dateiebene an; alle U.*-Aufrufe zwischen den Dateien laufen erst zur Laufzeit (Gesamt-Attrappe laedt in
  Spielreihenfolge, `client/B*` < `client/ISUI/*` < `client/NCBearBench*`).
- **Sicht und Fenster im 1-s-Takt**: `B.OnView` (Hud) -> `U.WinOnView` (dirty) und `U.PoseOnView` (vergessen), je hinter Riegel; das Fenster
  liest `self.v` beim naechsten Bild neu -- zwei Klicks auf "Passive" zwischen zwei Bildern gibt es im Spiel nicht (21g prueft mit Bild).
- **Sitz-Treiber und Hud**: `U.CubObj` nimmt nur die Objekte, die der Hud ohnehin bindet; der Hud-Suchlauf bindet jeden unserer Baeren der
  Sicht (unabhaengig von den Anzeige-Optionen), also findet der Treiber den Koerper auch bei "Name tag aus" und allen Werte-Zeilen aus.
- **Mehrspieler**: jeder Fenster-Knopf ist ein `sendClientCommand` (Mode/Come/Passive/Call; Rename ueber das Namensfenster wie B1b); kein neuer
  Server->Client-Befehl; im MP kann ein neuer Koerper beim Client erst ueber die Online-ID der neuen Sicht gebunden werden -> der Treiber
  sieht am Client nie eine veraltete `sit`-Sicht am neuen Koerper (Z1 ist nur Einzelspieler).
- **NPC Crew** (nur gelesen, v3.14.74): `Bear window`, `NPC Crew Bear`, `BanditsNPCBearWindow`, `BanditsNPCBear.ini`, `BearRoamRadius` 0 Treffer
  in `42/media/lua` und `_docs/landkarte_index.txt`; "Talk to NPC" liegt auf V (NC `client/BanditsNPCInteract.lua:7462`, Abschnitt
  `[NPC Crew]` :7451), `KEYBIND` :35, `FindTarget` :41; Beacon-Flaeche `hasBaseArea` NC `shared/BanditsNPCForestZones.lua:687-692` ("ohne das
  Modul, z. B. auf dem dedizierten Server, nein"); `BanditsNPC.Opt` jetzt :6108.

### 1.3 Luecken geschlossen
**Keine Luecke ueber die Grenze; kein Lua im Staging geaendert.** Die drei Sitz-Knoten bleiben (wie geplant, PLAN_F1.md 11.1) in der Test-Mod;
das Uebernahme-Skript nimmt sie von dort (3).

## 2. Gesamt-Attrappe `attrappe/gesamt/run.lua`

### 2.1 Umgebung (ERGAENZT, kein bisheriges Verhalten geaendert)
Seit F1 laden **alle** Abschnitte die sieben neuen Dateien (vorher lud die Attrappe keine davon -- die Bauer konnten das nicht pruefen).
Dafuer: weitere ISUIElement-Methoden (addChild, isReallyVisible, getAbsoluteX ...), `ISPanel` erbt sie, darauf **Vanillas echtes
`client/ISUI/ISButton.lua`** (Klick nur bei `enable`, `onclick(Ziel, Knopf)` wie im Spiel); `getCore()` mit `isKey`/`getKey` (Taste 47 = V),
`getKeyName`, Vanillas `keyBinding` (gekuerzt), `Keyboard`, `KeybindId`, Radiale, `ISChat`, `ISLayoutManager` (gemerkte Lage ueberlebt das
Laden), `getFileReader`/`getFileWriter` im Speicher (ueberleben das Laden wie die Platte), `MeasureStringX`, `UITransition`, `getSoundManager`,
`ISToolTip`, `string.trim`. Alles in EINER lokalen Tabelle `FE` (der Hauptteil steht bei 200 lokalen Namen, Lua 5.1).
Gewollt geaendert: **17d** (Bleiben steht jetzt still: 11 Kacheln -> zurueck rennend zur Heimat, 2 Kacheln -> haelt ohne Lauf; KERN Nr. 12),
`hud()`/`lastTagDraws()`/zwei Stellen in 19 nehmen den Hud ueber seine Klasse (`FE.hudPanel()`; das Fenster ist auch ein ISPanel), fake
`ISPanel:new` traegt Breite/Hoehe/Sichtbarkeit/leere Zeichenlisten, `ISTextBox:isReallyVisible` (zu nach OK), die Schluss-Schleife ohne lokalen
Namen. Mit diesen Aenderungen und den neuen Dateien liefen 1-20 sofort gruen (1938 / 0, nur die zwei 17d-Pruefungen rot -- genau wie vom KERN
angekuendigt); danach 17d angepasst.

### 2.2 Abschnitt 21 (neu, Plan 8.3 + Auftrag), Messwerte aus `ergebnis.txt` ("info 21")
- **21a** Tasten-Zeile nach ZWEIMAL Laden genau einmal (Abschnitt `[NPC Crew Bear]` direkt darueber, Vorgabe V), OnKeyPressed einmal; vor der
  ersten Sicht V -> "The bear window is still loading..."; ohne Baer V -> "You do not have a bear yet.", kein Fenster-Objekt.
- **21b** zaehmen ueber Menue + Zeitaktion; Rechtsklick "Bear window" mit Tooltip; V -> Fenster: "Kate's cub", "Bear cub - day 0",
  "half-grown in 15 day(s)", Zustand "Staying", Abstand aus der lebenden Kopie, Fusszeile "Drag to move.  V or Esc closes.", Leben/Ausdauer
  "n / m" mit Balken, "up to N", 6 Faehigkeiten "Lv 0", ehrliche "comes later"-Tooltips (Kaempfen, Fischen), Stay aktiv, Masse 640 x 602 bei 1080
  (Attrappen-Schrift; die echten Masse 640 x 615 prueft f1_ober), Lage auf dem Bild, ein Bild zeichnet Fenster + Kinder; Esc / V (verbraucht,
  dasselbe Loslassen oeffnet nicht wieder) / X / Rechtsklick / `NCBear_CubWin()`; Chat-Fokus sperrt die Taste; Rename oeffnet das Namensfenster,
  waehrenddessen schliessen V/Esc nicht, Name kommt im Fenster an.
- **21c** Sit: Modus sit, Meldung, Heimat = Kachel; nach zwei Hirn-Takten Sicht `sit`, Treiber "sitdown", nach 1,8 s "sit"; Fenster
  "Sitting", Sit aktiv; Besitzer 10 Kacheln weg -> sitzt weiter, haelt still.
- **21d** Follow aus dem Sitz: steht 1,6 s still ("standup"), Variable nach 1,4 s geloescht, danach folgt er; Fenster "Following you".
- **21e** Roam: Meldung "(up to 12 tiles)"; 200 Takte (320 s) mit festem Zufall: groesster Abstand **10,44** Kacheln vom Mittelpunkt, **0** Takte
  in einem Raum (Haus neben dem Mittelpunkt), **11** eigene Wege mit Pausen; Fenster "Roaming", "Roams within 12 tiles".
- **21f** Come here aus 10 Kacheln: folgt mit `s.come`, Fenster "Coming to you" (Come aktiv, Follow nicht), kommt an -> Bleiben,
  "waits here", beim Besitzer.
- **21g** Passive an/aus/an: Register, Spiegel am Tier, Sicht `pas`, Meldungen, Schalter, ehrlicher Tooltip; Name tag aus: Datei
  `BanditsNPCBear.ini` "tagoff <u>", Schild ohne Namen.
- **21h** Unstuck aus 15 Kacheln: gen + 1, genau ein addAnimal, alter Koerper weg, neuer neben dem Besitzer, Folgen; Knopf grau "Unstuck  m:ss"
  mit Grund. **Nicht geladen**: Sicht ohne `ld`, Fenster "Out of reach", alle Befehle grau mit "out of reach. Use Unstuck.", grauer Knopf
  schickt nichts, direkte Bitte -> Why_OutOfReach; nach der Abklingzeit Unstuck frei -> neuer Koerper neben dem Besitzer; die alte Kopie laedt
  spaeter wieder, wird **nie gebunden** und nach **75 Hirn-Takten (120 s, Waisen-/Kopien-Suchlauf)** unbeobachtet entfernt (Z3); danach genau
  ein Koerper.
- **21i** Tag 15 im Sitz mit offenem Fenster: Tausch (gen + 1, Modus bleibt sit), setzt sich wieder, Treiber am NEUEN Koerper endet in "sit"
  (Folge **sitdown > standup > sitdown > sit** -- Z1), Fenster "Bear - day 15", "Sitting".
- **21j** `NCBear_CubBodyGone()`: Koerper weg, Eintrag bleibt; vermisst nach **9 Hirn-Takten (14 s)**, "You have lost track of your bear.";
  Fenster "Missing", Fusszeile Win_HintMissing, Befehle grau mit "Your bear is out of reach..." (bd big), **Unstuck frei**, Werte und
  Faehigkeiten auch vermisst; **C1** nach weiteren **20 Hirn-Takten (32 s)**: genau EIN addAnimal, gen + 1, "Your bear is back.", Modus sit
  bleibt; 30 Takte danach kein weiterer Koerper.
- **21k** Speichern/Laden: Modus sit, passive, sitzt wieder, ein Koerper, Fenster NICHT von selbst offen, Name tag bleibt aus (Datei), Lage
  gemerkt ohne `visible`; V oeffnet ein neues Fenster an (123, 77); Schalter und aktiver Befehl stimmen.
- **21l** 3840 x 2054: Faktor 2, **1280 x 1104 px**, auf dem Bild; zurueck auf 1080: Faktor 1; Tod -> Eintrag weg, Meldung, **Fenster zu**,
  danach V -> "kein Baer".
- **21m MP** (Server + A Besitzer + B fremd): A oeffnet mit V; jeder Knopf Sit/Roam/Follow/Stay -> genau ein `sendClientCommand Mode` mit dem
  Wert -> Server setzt, Meldung nur an A, aktiver Knopf aus der neuen Sicht; Sit: Server sitzt (nach dem eigenen Laufbefehl), Sicht an A UND B
  `sit`, Bs Sitz-Treiber setzt "sitdown" an SEINER Kopie (ohne Spiegel, ueber die Online-ID); B: V -> "kein Baer", Bs Mode an As Baeren ->
  Why_NotOwner, nichts geaendert; A: Passive `{ on = true }` -> Server, Sicht `pas`; Come (aus dem Sitz) -> angekommen -> Bleiben; Unstuck ->
  gen + 1, `removeAnimal(alte OnlineID)`; **C1 am Server** (Suchlauf hat Baeren gesehen, `B._scanSeen`): genau EIN addAnimal, passive bleibt;
  Server-Neustart: passive bleibt, ein Koerper; Client-Befehle nur Mode/Come/Passive/Call/Hello (Rename/Hello erlaubt).

**Grenze der Attrappe** (wie B1a-B1e): ein Lua-Zustand fuer Server und alle Clients (darum schliesst 21m As Fenster, bevor B dran ist);
Laufbefehle setzen das Tier sofort ans Ziel; Clip-Laengen, Bildwechsel, Fenster-Ziehen und Tooltips beweist sie nicht.

## 3. Uebernahme-Skript `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md` (Plan 11.3/11.4)

### 3.1 Was sich aenderte
- `ANIMSET_OK` + `NCBear_SitDown|Sit|StandUp.xml` (aus der Test-Mod; Pruefungen "genau eine Bedingung NCBearAct (STRING)" und "Clip im GLB des
  Jungen" gelten mit, im Trockenlauf nachgewiesen); die 6 Kampf-Knoten bleiben "NICHT" (Text jetzt "Kampf-Knoten").
- Neue Form-Pruefung: jeder Wert, den der Sitz-Treiber ueber `phase(e, obj, "<wert>", now)` an B.ACT setzt, braucht einen kopierten Knoten
  (sit / sitdown / standup gruen).
- `TEXT_NS["UI.json"]` + genau die zwei Schluessel `UI_optionscreen_binding_NPC Crew Bear` / `UI_optionscreen_binding_Bear window` (kein
  Muster; NPC Crew und Vanilla-EN kennen sie nicht -- das Skript prueft je Lauf).
- `CHEAT_ALLOWED` + drei Ausnahmen der Regel `taste`, je mit Grund (ENT:259): Key.lua `{ value = NAME, key = Keyboard.KEY_V }`,
  `Events.OnKeyPressed.Add(onKey)`, Window.lua `return key == Keyboard.KEY_ESCAPE or`. Jede andere Taste/Maus/Joypad-Abfrage bleibt ein Fund.
- **Neue Tier-Regel `PlaceCub`**: `B.PlaceCub(` (neuer Koerper fuer einen bestehenden Eintrag) nur aus `B.RideStep`, `B.HandleCall`,
  `B.BodySwap`, `B.ReviveMissing`; `TIER_DEF` + PlaceCub (die Definition zaehlt nicht). Ein Fenster-Knopf mit `B.PlaceCub` waere ein Spawn-Weg.
- Kopftext (F1 im Ueberblick, Punkt 1 und 6), Text der Regel `taste`, Naehte-Zeile des Plan-Ausdrucks (Zeilen 27-30). Die Bench-Pruefung
  ("Fingerabdruck der Werkbank") greift weiter: die neuen Bench-Texte ("bear window opened", "Cub: bear window" ...) stehen nur in der Bench.
- `NAEHTE.md`: Kopf (F1, NPC Crew v3.14.74), Zeilen 4 (BearRoamRadius, 28 Optionen), 5 (274 Texte, die zwei Tasten-Schluessel ausserhalb des
  Namensraums, NPC Crew 3815/92), 6 (Rechtsklick "Bear window", vier Modi, Hold nur bei Bleiben), 9 (drei Sitz-Knoten, Clip-Laengen), 11 (Come,
  Passive, Register/Spiegel/Sicht/Sitzung, nie mehr "lost"), 14 (Taste/Fenster gebaut, Namensschild je Baer), 17 (C1 mit beiden Riegeln), 19
  (WinSize), **neu 27** (Tasten-Zeile in Vanillas `keyBinding`), **28** (Vorfahrt V: NPC Crew nur gelesen), **29** (`layout.ini`-Name,
  `BanditsNPCBear.ini`), **30** ("Frei" in NPC Crew = Beacon-Basisflaeche -- NUR dokumentiert, Rueckfall Kreis am dedizierten Server);
  Laufzeit-Aufsaetze, Animations-Knoten, Cheat-Ausnahmen + 3, Absatz "F1, vom Skript erzwungen", B5a-Abhaengigkeiten (Sitz-Werte ziehen mit).

### 3.2 Laeufe (Ausgaben im Ordner `_arbeit/baer_zaehmen/`)
- `trockenlauf_f1_vor_b5a.txt`: **OK, 0 Fehler, 28 Warnungen**. Kopieren: 31 Lua, 17 Modell/Textur/Skript/Knoten/Bild (3,1 MB), Knoten 4 (Werte
  eat, sit, sitdown, standup). Texte: UI.json 274 neu (NPC Crew 3815 -> 4089), Sandbox.json 61 neu (92 -> 153), IG_UI.json 4 (neu). Sandbox 28
  Optionen (NPC Crew vorher 42). Cheat-Pruefung: 31 Lua, 9238 Codezeilen, **Funde 0**, 5 Ausnahmen greifen (2 `befehl` + 3 `taste`);
  Tier-Regeln je an ihrem Ort, PlaceCub: Grow.lua:537 BodySwap, Order.lua:366 ReviveMissing, Ride.lua:198/:232 RideStep, Ride.lua:365
  HandleCall. "Texte aus der Lua: 245 benutzt, fehlen in EN: 0; Ersatztexte 272, wortgleich: ja". Kollisionen 0.
- `trockenlauf_f1.txt` (ohne `--vor-b5a`): 26 Fehler, alle "noch umzubenennen (B5a)", 0 andere.
- `probe_f1_ausgabe.txt` (nur unter `_arbeit/baer_zaehmen/probe_f1/`): OK, 0 Fehler, 28 Warnungen, 70 Dateien; Pruefer je kopierter Datei gruen.

### 3.3 Gegenprobe der Skript-Regeln (`attrappe/uebernahme_f1/probe_regeln_f1.py`, Temp-Kopie, Trockenlauf `--vor-b5a`)
Unveraendert: 0 Fehler. Zweite Taste (`Keyboard.KEY_F`) im Fenster, `Events.OnKeyPressed` im Fenster, `Events.OnMouseDown` im Fenster,
`B.PlaceCub` aus `B.HandleCome`, `B.GrowSetG` aus dem Fenster, Fenster-Knopf mit festem Text, Testbefehl `NCBear_CubWin` im Fenster, Treiber
setzt "liedown" (kein Knoten), dritter Tasten-Schluessel in EN -> **je erkannt (10 von 10 wie erwartet)**.

## 4. `staging_dateien.txt` und `mod_info_vorschlag.txt`
- `staging_dateien.txt` (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen NCBearTest 914ee79): **67 Dateien, 7 neu** (`server/
  BanditsNPCBearOrder.lua`, `client/BanditsNPCBearKey.lua`, `...Pose.lua`, `...Tags.lua`, `...WinData.lua`, `client/ISUI/BanditsNPCBearWinParts.lua`,
  `...Window.lua`), **30 ueberschreibt** (10 Kern-Lua, 4 Client-Lua, Bench, 7 UI.json, 7 Sandbox.json, `sandbox-options.txt`), **30 gleich**.
  Kopfzeile nennt die drei Sitz-Knoten (liegen schon in der Test-Mod, nicht im Staging).
- `mod_info_vorschlag.txt`: Beschreibung um F1 (Fenster auf V mit allem Inhalt, die Befehle, Passive, Name tag je Baer, Groessen-Option,
  "kommt spaeter" ohne Balken, Baer ohne Koerper kommt wieder, nie mehr verloren, "bear" statt "cub"), B1e nicht mehr "NEU"; Testhilfen-Liste
  28 (gegen die Bench gezaehlt: `NCBear_CubWin`, `_CubBodyGone`, `_CubView` neu); ASCII, LF, fuer `mod.info` UND `42/mod.info`.

## 5. Einzelspieler und Mehrspieler
| Vorgang | SP (`not isServer() and not isClient()`) | MP |
|---|---|---|
| Taste / Fenster | Spieler 0, Sicht des einen Programms (21a-21l) | nur Client; Server laedt `client/` nicht; je Client eigene Sicht (21m) |
| Befehle aus dem Fenster | `B.Ask` -> `B.Handle` direkt (21c-21h) | `sendClientCommand` Mode/Come/Passive/Call, Server prueft Besitz/Lage/Abklingzeit; Meldung nur an den Bittenden (21m) |
| Sitzen sichtbar | Treiber an der Kopie = Tier des Schreibers (21c, 21i) | jeder Client an SEINER Kopie (B sieht A sitzen, 21m) |
| Passiv / Name tag | Register + Spiegel / Client-Datei (21g, 21k) | Register am Server, Sicht `pas` (21m) / Datei je Client |
| Unstuck / C1 | 21h (auch nicht geladen), 21j | 21m (Unstuck, C1 nach dem Beweis des Suchlaufs) |
| Bench | `NCBear_CubWin`, `NCBear_CubBodyGone` (21b, 21j) | lehnt ab ("singleplayer only", f1_ober) |
Rote Linien: kein Gegenstand erzeugt oder vernichtet (das Fenster fasst keinen an); **nie zwei Koerper und nie keiner** (21h, 21i, 21j, 21k, 21m
zaehlen die lebenden Koerper je Eintrag; die alte Kopie nach Unstuck aus entladener Gegend wird nie gebunden, Z3); kein neuer Server->Client-Befehl,
die neuen Client-Befehle brauchen nur Rolle user; nichts haengt (Abklingzeiten, Deckel 64 Zeilen, Fenster-Takt 1 s nur offen); keine
NPC-Crew-Figur beruehrt (Vorfahrt V liest NPC Crew nur).

## 6. Befunde des Zusammenbaus (kein Lua geaendert; fuer die Pruefer/Nachbesserung)
- **Z1 (Sicht, klein, nur SP): Treiber flackert nach dem Tausch im Sitz.** Tauscht der Koerper (Tag 15), waehrend der Baer sitzt, bindet der Hud
  den neuen Koerper sofort ueber den Spiegel, die Sicht traegt aber noch `sit = true` bis zum naechsten Hirn-Takt: `B.GrowLive` (darin der
  Tausch) laeuft NACH `B.FlushViews` (`S:server/BanditsNPCBearServer.lua:1043` Flush, `:1075` GrowLive -- so seit B1d B2). Folge am neuen
  Koerper: sitdown > standup > sitdown > sit (21i, gemessen), ~5 s. Im MP nicht (Bindung erst ueber die neue Online-ID). Vorschlag (klein, nur
  Client): `client/BanditsNPCBearPose.lua` beginnt an einer NEUEN Kopie erst mit der naechsten Sicht (`U.syncN` merken); f1_ober Fall 9
  ("neue Kopie -> neu") nachziehen.
- **Z2 (Verhalten, ungeprueft, aus dem Code gelesen): "Sit"/"Stay" waehrend eines laufenden eigenen Wegs.** `B.SetMode` leert `s.f`/`s.come`/
  `s.roam` (`S:server/BanditsNPCBearFollow.lua:120-123`), aber nicht `s.ownUntil`/`s.tx`; `B.OrderDecide` laesst einen laufenden Weg weiter
  laufen (Regel 32 "keep" fuer Sitz, 36 fuer Bleiben, `S:shared/BanditsNPCBearRules.lua:381`), bis er weiter als `stayBack` 3 von der Stelle des
  Befehls ist -- dann geht er zurueck (Regel 31/35). Drueckt Kevin "Sit", waehrend der Baer ihm hinterherrennt, laeuft er seinen Schritt zu Ende
  und kommt dann an die Stelle zurueck, wo der Knopf gedrueckt wurde. Die Attrappe sieht das nicht (Laufbefehle setzen das Tier sofort ans
  Ziel). Vorschlag: beim Wechsel auf stay/sit den eigenen Weg beenden (`s.ownUntil = nil` + `B.Hold`), oder die Stelle des Befehls = Ende des
  laufenden Wegs -- Kevins Wahl (Frage Z2 unten).
- **Z3 (bekannt, Plan 4b Nr. 5): alte Kopie nach Unstuck aus entladener Gegend.** Laedt die Gegend spaeter, steht die alte Kopie (kleinere gen,
  ohne Schild, nie gebunden) bis zum naechsten Waisen-/Kopien-Suchlauf: gemessen 120 s (`orphanScanMs`), und nur, wenn niemand naeher als 25
  Kacheln steht. Kein Doppel im Register; sichtbar ja.
- **Z4 (Werkzeug)**: `xref_f1.py` prueft nur das Staging (im Probe-Ordner liest es NPC Crews eigene Dateien mit: 4808 Fremd-"Luecken");
  `xref_b1e.py` ist durch F1 ueberholt. `bilder_pruefen_b1e.py` braucht numpy (hier nicht da) -- Bilder unveraendert.
- **Taste V (Kollisionen, nachgelesen)**: V liegt in Vanilla auf "Vehicle Radial Menu" (`V:shared/keyBinding.lua:130-132`) und "Animal Radial
  Menu" (`:185-187`), in NPC Crew auf "Talk to NPC" (`NC:client/BanditsNPCInteract.lua:7462`); Bandits benutzt `Keyboard.KEY_V` nirgends
  (grep 42.22). Vorfahrt im Code wie Plan F4 (NPC > Fahrzeug > fremdes Tier > Baeren-Fenster); legt Kevin "Bear window" auf eine eigene Taste,
  greift keine Vorfahrt.

## 7. Offen / ungeprueft (Testpunkte; PLAN_F1.md 8.4 ist Kevins Testliste)
1. **Alles Laufzeit-Verhalten ungespielt**: Ziehen/Klicken des ISPanel mit ISButton-Kindern, Esc oeffnet das Spielmenue NICHT (isKeyConsumed),
   verbrauchtes V loest kein OnKeyPressed aus (NUR JAR, dazu 250-ms-Sperre), Tier-Radial blitzt am eigenen Baeren hoechstens kurz, die Zeile
   erscheint unter Optionen -> Tastaturbelegung "NPC Crew: Bear", Tooltip-Schrift bei 4K, lange RU/FR-Texte.
2. Sitzen: ob `setBlockMovement(true)` je Takt den sitzenden Baeren ruhig haelt, ohne den Clip zu stoeren; `setVariable` an der Client-Kopie
   im MP (ob ein Tierpaket sie ueberschreibt); Z1/Z2 im Spiel ansehen.
3. Frei: Fussgleiten beim gehenden Bummeln; ob `pathToLocation` die Zielkachel erreicht.
4. Komm her: `comeMaxMs` 30 s / "steckt fest" -- gibt er vor Tueren zu frueh auf?
5. MP: `getObjectListForLua` am Server (A3) -- solange der Suchlauf dort nichts sieht, kommt ein Baer ohne Koerper NICHT von selbst wieder
   (Fehlerzeile "revive: ... has not seen any bear on this server yet"), Unstuck geht. Server-Log nach `[TC-BEAR] ***` durchsehen.
6. NPC Crew wird parallel weitergebaut (v3.14.74): Trockenlauf und Probe vor einer echten Uebernahme (erst nach B5a) neu laufen lassen.

## 8. Fragen fuer Kevin (Nachtschicht: nichts davon haelt den Einbau auf; gebaut ist jeweils der heutige Stand)
Die Plan-Fragen F1-F15 (`PLAN_F1.md` 12), K1-K4 (`bau_f1_kern.md` 9) und O1-O5 (`bau_f1_oberflaeche.md` 9) sind wie empfohlen gebaut. Neu aus
dem Zusammenbau:
1. **Z2**: Wenn du "Sit" oder "Stay" drueckst, waehrend der Baer dir hinterherlaeuft -- soll er sofort stehen bleiben (Empfehlung) statt seinen
   Schritt zu Ende zu laufen und zurueckzukommen? Gebaut: heutiger Stand (laeuft zu Ende); Empfehlung fuer die Nachbesserung: sofort anhalten.
2. **Z1**: Beim Wechsel an Tag 15 im Sitzen steht der neue Baer einmal kurz auf und setzt sich wieder (nur Einzelspieler). Glaetten (Empfehlung,
   kleine Aenderung im Sitz-Treiber)? Gebaut: heutiger Stand.
3. **Z3**: Holst du den Baeren mit Unstuck aus einer weit entfernten Gegend, kann dort spaeter eine alte Kopie ohne Schild stehen, bis der
   naechste Suchlauf sie entfernt (bis 2 Minuten, und nur, wenn niemand naeher als 25 Kacheln steht; nie doppelt im Register, nie
   gebunden). Reicht das? Empfehlung: ja (so gebaut seit B1c).

## 9. Einbau (NICHT gemacht -- nur wenn Kevin nicht spielt)
`tasklist | grep -i ProjectZomboid` leer -> Zip der Test-Mod nach `Zomboid/backups/NCBearTest/`, die **37 Dateien** mit Zustand neu/ueberschreibt aus
`staging_dateien.txt` in EINEM Zug kopieren (die 30 "gleich" aendern nichts), byte-gleich nachzaehlen (MD5-Spalte), Beschreibung aus
`mod_info_vorschlag.txt` in `mod.info` und `42/mod.info`, zweites Zip. Danach **Spiel neu starten** (neue Lua, neue Taste), `bugwatch.py`
mitlaufen lassen, Test nach PLAN_F1.md 8.4 (Debug-"Tier Cheat" AUS, `NCBear_CubLog(true)`).

Statisch geprueft, nicht gespielt.
