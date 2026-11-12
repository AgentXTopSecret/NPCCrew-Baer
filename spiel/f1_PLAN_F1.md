# Lauf baer-f1: PLAN -- Baeren-Fenster auf V, Befehle Sitz/Frei/Komm her/Passiv/Unstuck, Namensschild je Baer, B1e-Reste (F1)

Stand 11.11.2026 nachts (Nachtschicht). **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2. Verbindlich fuer zwei Bauer (KERN,
OBERFLAECHE, gleichzeitig, getrennte Dateien) und den ZUSAMMENBAU danach. Baut auf dem Staging `_arbeit/baer_zaehmen/mod/` (B1a-B1e inkl.
Nachbesserung, Liste `staging_dateien.txt`).
**Vorab nachgezaehlt (11.11. nachts):** Staging gegen Test-Mod `NCBearTest` (Git main 914ee79): **60 Dateien, alle 60 byte-gleich** (MD5). Die Bauer
zaehlen vor dem Bau noch einmal nach (aendert sich etwas, Abbruch und Meldung).
Kurzformen: `FF x.y` = `forschung_f1.md`; `PB1C/PB1D/PB1E x.y` = `PLAN_B1C.md`/`PLAN_B1D.md`/`PLAN_B1E.md`; `S:` = Staging `mod/42/media/lua/`;
`V:` = Vanilla `media/lua/` (42.22.2); `B:` = Bandits `42.22/media/lua/`; `NC:` = NPC Crew `42/media/lua/` (nur gelernt); `T:` = Test-Mod
`NCBearTest/42/media/`; `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`; `B` = `BanditsNPC.Bear`, `U` = `B.UI`. **NUR JAR** = Lesehilfe, kein Beleg.
Entwurfsbilder: `_arbeit/baer_zaehmen/f1_entwurf/fenster_1080.png`, `fenster_4k.png` (Skript `f1_entwurf/zeichne_fenster.py`, echte Spielschrift,
Kevins Spielbild als Hintergrund).

Kevins Worte, auf denen der Plan steht: *"ich wll noch spaeter eine richtige UI die aufgeht wenn ich V druecke (einstellbar in den keystings)"*
(ENT:259) -- *"alle funktionen einbauen ... die ganzen skills das schoene ui und alles"* (ENT:348) -- Befehle *"hinsetzen ... oder frei rum
wandern aber nie aus der base area geht ... ausser man stellt den auf passiv"* (ENT:63-66) -- Unstuck *"holt ihn auf eine freie, stehbare Kachel
neben dem Spieler ... nur auf Klick"* (ENT:68) -- *"Unstuck vorerst als Rechtsklick ('Call to me') ... spaeter ins V-Fenster"* (ENT:280) --
Namensschild *"je Baer; Vorgabe an"* und *"JE SPIELER (was ich sehe)"* (ENT:103, :106) -- Faehigkeiten ENT:209-230 -- B1e-Reste ENT:335-336
("bear" statt "cub"; Baer ohne Koerper erscheint von selbst wieder). Alles andere ist VORSCHLAG des Planers (Stellwert oder Frage in 12).

---

## 0. Entscheidungen des Planers (gelten fuer alle)

**0.1 Das Fenster ist ein eigenes `ISPanel` mit `moveWithMouse`** (Vanilla `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1`, `:243`, `:253`) --
NICHT `ISCollapsableWindow`: dessen Titelleiste nimmt fest `UIFont.Small` (`V:client/ISUI/ISCollapsableWindow.lua:398-399`) und waere bei 4K
winzig (FF 2.1 "Titelleiste bei 4K ungeprueft"). Alles waechst mit EINEM Faktor f (0.4); gezogen wird an jeder freien Stelle des Fensters.
Knoepfe, Schalter und Zeilen mit Tooltip sind Kinder, abgeleitet von `ISButton` (`ISButton:derive`, Vorbild `V:client/ISUI/ISResizeableButton.lua:1`,
Aufruf der Elternmethode `ISButton.onMouseDown(self, x, y)` `:15`) -- so kommen Klick, Ton und Vanillas Tooltip (auch an grauen Knoepfen,
`V:client/ISUI/ISButton.lua:18-20`, `:316-346`) mit; gezeichnet wird in eigener `prerender`/`render` (eigene Farben, 0.3 / 1.3).

**0.2 "Komm her" und "Unstuck" sind ZWEI verschiedene Knoepfe** (Frage F1): **Unstuck = "Call to me" aus B1c** (`B.HandleCall`, Versetzen neben
den Spieler, 5-min-Abklingzeit mit Restzeit am Knopf, geht auch fuer vermisste und nicht geladene Baeren -- Kevins Gleichsetzung ENT:280).
**Komm her = gehender Ruf** (neuer Befehl `Come`): der Baer LAEUFT zum Spieler (Folgen-Logik) und bleibt dort ("Bleiben"); kein Versetzen, keine
Abklingzeit; nur geladen und in `BearFollowMaxDistance` (Kevins eigener Befehl "Komm her" ENT:65, Ruf-Idee ENT:97). Der Auftrag schrieb
"Komm her (= Call to me)" -- dann waeren es zwei gleiche Knoepfe (FF 0.7, F-a).

**0.3 Vier Modi statt zwei** (`rec.mode`): `follow`, `stay`, `sit`, `roam`. **Bleiben = stehen bleiben** an der Stelle des Befehls (halten; ist er
weiter als `stayBack` 3 Kacheln weg -- Laerm, Verstecken --, geht er zurueck). **Frei = das bisherige Bleiben mit eigenem Radius** (Sandbox
`BearRoamRadius`, **Vorgabe 12**, 4..30) PLUS eigene Spaziergaenge (gehend) mit Pausen; zwischen den Wegen haelt er (kein Engine-Wandern -> er
verlaesst den Kreis nie von selbst). Vorgabe 12 statt der 8 aus dem Auftrag: Kevin hat "Bleiben-Radius 12" bestaetigt (ENT:284), und mit 8 rannte das
Junge in B1b staendig heim, weil die Engine +-8 je Achse wuerfelt (Nachbesserung B1b B7, `S:shared/BanditsNPCBear.lua:84-86`) (Frage F2).
Mittelpunkt von Bleiben/Sitz/Frei = die Kachel, auf der der Baer beim Befehl steht (wie B1b-Bleiben, `S:server/BanditsNPCBearFollow.lua:95-97`).
Alte Spielstaende: `mode` "stay" bleibt "stay" (steht jetzt still statt in 12 Kacheln zu bummeln -- in 12 erwaehnt).

**0.4 Masse, Schrift, Faktor.** f = `U.MarkerFactor(getCore():getScreenHeight(), idx)` (B1e, `S:client/ISUI/BanditsNPCBearMarker.lua:108-123`;
1080 -> 1,0, Kevins 2054 -> 2,0) mit eigener Option `WinSize` (Auto/100..300 %, 1.7). Alle Grundmasse in 1.1 sind Pixel bei f = 1 und werden mit f
mal genommen; **Zeilenhoehen kommen aus der echten Schrifthoehe** (`getTextManager():getFontHeight`), Breiten aus `MeasureStringX` -- so passt es bei
jeder Vanilla-Schriftgroesse (1x..4x). Schriftwahl 1.2.

**0.5 Sitzen wie die Test-Mod, aber ohne Lesen der Anim-Variable.** Der Schreiber haelt den Baeren an seiner Stelle und meldet in der Sicht
`sit = true`, sobald er dort ruhig steht; JEDER Client (im SP derselbe Rechner) setzt an SEINER Kopie `NCBearAct` = "sitdown" -> nach 1,7 s "sit"
-> beim Ende "standup" -> nach 1,4 s loeschen (Weg der Test-Mod `T:lua/shared/NCBearFight.lua:1491-1513`, Clips in beiden GLBs, FF 4.1/4.2; im MP
wird `NCBearAct` nicht uebertragen, FF 4.2 Nr. 2). **Nur nach der Uhr, nie `getVariableString`:** FF 4.2 nennt als Vanilla-Beleg am Tier
`V:client/DebugUIs/DebugMenu/Anims/ISAnimDebugMonitor.lua:289` -- dort ist es `getPlayer()`, also KEIN Tier (nachgelesen); am Tier gibt es den
Aufruf nur in der gespielten Test-Mod. Ohne Kevins Wort wird er nicht benutzt. Die drei Knoten `AnimSets/buck/idle/NCBear_SitDown|Sit|StandUp.xml`
liegen schon in der Test-Mod (unveraendert); das Uebernahme-Skript bekommt sie frei (11).

**0.6 Neue Datei fuer die neuen Befehle beim Schreiber:** `S:server/BanditsNPCBearOrder.lua` (Bleiben/Sitz/Frei-Takt, Komm her, Passiv, C1). Die
grossen Dateien (`Server.lua` 48 KB, `Follow.lua`, `Ride.lua`) bekommen nur die noetigen Einhaenger (localcount aktiv UND insgesamt < 180).

**0.7 Passiv** ist ein gespeicherter Schalter je Baer (`rec.passive`, Register + Spiegel + Sicht), wirkt erst mit B5a -- der Tooltip sagt das
ehrlich. **Namensschild je Baer** ist eine Einstellung JE SPIELER (ENT:106): Datei `BanditsNPCBear.ini` beim Client (Schluessel = `u` des Baeren als
Text, Deckel 64), der Server weiss nichts davon; die globale Option `TagShow` bleibt der Hauptschalter.

**0.8 C1 (Baer ohne Koerper kommt von selbst wieder)** laeuft im Suchlauf-Block des Hirn-Takts direkt nach `countMisses`: ein VERMISSTER Eintrag,
dessen Gegend geladen ist und dessen Besitzer online ist, bekommt nach 2 weiteren vergeblichen Suchlaeufen GENAU EINEN neuen Koerper an seiner
letzten Stelle (`B.SpotNear` + `B.PlaceCub` -- derselbe Weg wie Call to me, gen + 1, Spiegel sofort). **Und: ein zahmer Eintrag wird nie mehr
nach 24 Spielstunden als "lost" geschlossen** (rote Linie "der Baer geht nie verloren"; Unstuck und C1 holen ihn immer) (Frage F10).

**0.9 Taste:** eine Zeile in Vanillas `keyBinding`-Tabelle (Reiter Tastaturbelegung, `V:shared/keyBinding.lua:6-14`), Name **"Bear window"**,
Vorgabe V, eigener Abschnitt **"[NPC Crew Bear]"** (FF 1.1, F-h). Vorfahrt in 3.2: NPC-Gespraech > Fahrzeug-Radial > Radial eines FREMDEN Tiers >
Baeren-Fenster; am eigenen Baeren schliesst unser Fenster Vanillas Tier-Radial (FF 1.3 Weg b).

**0.10 Nichts Teures je Bild.** Das Fenster baut sein Modell (Texte, Zahlen, Knopf-Zustaende) nur bei neuer Sicht (`B.OnView`) und hoechstens
1 x je Sekunde (Restzeit Unstuck, Abstand); je Bild wird nur aus fertigen Feldern gezeichnet (~130 Zeichenaufrufe, nur solange es offen ist).

**0.11 Aufteilung:** KERN = `shared/` (ohne Translate) + `server/` + Kern-Attrappen; OBERFLAECHE = `client/` (mit `ISUI/`, Bench), alle Texte
(`UI.json`, `Sandbox.json`), `sandbox-options.txt`, Werkzeuge, Oberflaechen-Attrappen. Keine Datei fuer beide (7.1).

**0.12 Nicht in F1:** Kampf/Zombie-Angriffe (B5a; Passiv wirkt dann), Hunger/Durst/Muedigkeit/Vertrauen (F3; nur Platz "kommt spaeter"), Inventar
(F4), Spuernase/Fischen-Wirkung (F5), 3D-Bild des Baeren im Fenster (F-f), Modell-Dateien, alte `NCBear*`-Dateien, NPC-Crew-Beacon-Anbindung
(nur Naht in NAEHTE.md), Joypad-Bedienung des Fensters, geteilter Bildschirm (nur Spieler 0, wie `V:client/ISUI/Hutch/ISHutchUI.lua:884-893`).

---

## 1. Das Fenster (OBERFLAECHE)

Entwurf: `f1_entwurf/fenster_1080.png` (1920 x 1080, f 1,0, Vanilla-Schrift 1x) und `f1_entwurf/fenster_4k.png` (3840 x 2054, f 2,0, Schrift 2x --
so gross zeigt Kevins Spielbild `baer/begleiter/kevin_sitzen_gut_1111.webp` die Vanilla-Schrift: Inventar-Titel ~26 px). Je Bild links das Junge
Tag 12 (folgt, Maus ueber "Agility"), rechts derselbe Baer gross Tag 60 (sitzt, passiv, Unstuck wartet; Faehigkeiten dort Beispielwerte wie nach
Kaempfen). **Der Bau soll so aussehen.** Das Skript rechnet die Masse genau nach 1.1/1.2 (Grundlage fuer die Attrappe der OBERFLAECHE).

### 1.1 Aufbau und Masse (Pixel bei f = 1; jede Zahl x f; lb/ls/ln = Zeilenhoehe der Schrift Text/Klein/Name, 1.2)

| Bereich | Lage / Masse | Inhalt |
|---|---|---|
| Fenster | Breite W = max(640, Bedarf); P (Rand) = 16; Hoehe aus dem Inhalt (unten) | Hintergrund + 1-px-Rahmen + 3-px-Akzentlinie oben |
| Kopf | Hoehe headH = max(100, 14 + ln + 2 + lb + 2 + lb + 10) | links Scheibe 80 x 80 bei (P, 12), darin Kevins Symbol 72 x 72 bei (P+4, 16) |
| Name | x = P + 80 + 14, y = 14, Schrift Name, zweimal gezeichnet (+1 px, "fett") | Name aus der Sicht, sonst `U.CubName` |
| Umbenennen | rechts neben dem Namen, Abstand 12; Hoehe ls + 6, Breite Text + 16, senkrecht zur Namenszeile mittig | Knopf "Rename" |
| Zeile 2 | y = 14 + ln + 2, Schrift Text, Farbe text2 | "Bear cub - day 12" / "Bear - day 60" |
| Zeile 3 | y = Zeile 2 + lb + 2, Farbe honeyText | "half-grown in 3 days" / "full-grown" |
| Schliessen | 24 x 24 bei (W - P - 24, 12) | Vanillas Bild `media/ui/inventoryPanes/Button_Close.png`, auf 24 x f gezwungen |
| Baeren-Wahl (nur > 1 Baer) | links vom Schliessen: "<" 24 x 24, Text "1 / 2", ">" 24 x 24, Abstand 6 | blaettert (F-c) |
| Zustand-Chip | rechtsbuendig, y = 44, Hoehe lb + 8; Punkt 10 x 10 (eingefaerbte `BanditsNPCBearMarker_disc.png`) bei +10, Text bei +28 | 1.4 |
| Abstand | rechtsbuendig unter dem Chip, +4, Schrift Klein, Farbe dim | "3 tiles to the south-east" / "right next to you" / "last seen 52 tiles to the north" |
| Trennlinie | y = headH + 4, 1 px, von P bis W - P | |
| Karten | y1 = headH + 16; zwei Spalten CW = (W - 2P - 16) / 2; Hoehe cardH = max(links, rechts) | Hintergrund cardBg, Rahmen 1 px |
| Karte "Condition" (links) | Innenrand 12; Titel (Text, honey) + 8; Leben: Etikett links / "118 / 128" rechts, darunter Balken 10 hoch, Breite CW - 24, Zeile = lb + 4 + 10 + 10; Ausdauer gleich; "Can carry" / "up to 34" (Zeile lb + 10); Trennlinie + 9; "Coming later:" (Klein, dim) + 6; 2 x 2 Raster Hunger / Thirst / Tiredness / Trust (Klein, dim, Punkt 6 x 6), Zeile ls + 6 | 1.5 |
| Karte "Skills" (rechts) | Titel + 8; 6 Zeilen je lb + 4 + 8 + 8: Name links; rechts "Lv 3" (honey; Stufe 0 dim) und "32%" (Klein, text2; Stufe 10: "max"); darunter 10 Segmente, Luecke 3, Hoehe 8, Breite (CW - 24 - 27) / 10 | 1.5 |
| Karte "Orders" | y2 = y1 + cardH + 16; volle Breite W - 2P; Titel + 8; rechts im Titel ein Hinweis (Klein, dim; nur bei "Frei": "Roams within 12 tiles"); 2 Reihen x 3 Knoepfe, Breite bw = (W - 2P - 24 - 16) / 3, Hoehe bh = max(34, lb + 12), Abstand 8; Reihe 1 Follow / Stay / Sit, Reihe 2 Roam free / Come here / Unstuck; darunter 10 Abstand, Schalter-Reihe Hoehe th = max(30, lb + 10): Passive, Name tag (je bw breit), dritte Zelle frei | 1.6 |
| Fusszeile | y3 = y2 + ordH + 10, Schrift Klein, dim | Hinweis zum Zustand (1.4) |
| Gesamt | H = y3 + ls + 14 | bei 1080/1x: **640 x 615**; 4K/2x: **1280 x 1178** (57 % von 2054); 4K/1x: 1280 x 1149 |
Breite waechst nur, wenn ein Text nicht passt: jeder Knopf bw >= laengster Knopftext + 24 x f, jede Spalte CW >= Etikett + Wert + 36 x f
(gemessen mit `MeasureStringX`); dann W = 2 P + 3 bw + 40 x f bzw. 2 P + 2 CW + 16 x f. Passt das Fenster nicht auf den Bildschirm
(H > 0,92 x Bildhoehe), wird f eine Stufe kleiner gerechnet (bis 1,0).
**Lage:** beim ersten Oeffnen x = (Bildbreite - W) x 0,62, y = (Bildhoehe - H) x 0,30; danach die gemerkte (1.8); immer auf den Bildschirm
geklemmt (mindestens 40 x f px sichtbar). Kein Schliessen wegen Abstand (F-j).

### 1.2 Schrift (Regel, wie im Entwurf-Skript `pick_fonts`)
Kandidaten nur `UIFont.Small`, `UIFont.Medium`, `UIFont.Large` (Hoehe je `getTextManager():getFontHeight(font)`, einmal je Aufbau).
1. Wahl: die groesste Schrift mit Hoehe <= Ziel x 1,1, sonst Small. Ziele: **Name 29 x f, Text 19 x f, Klein 15 x f**.
2. Rangfolge: Text ist eine Stufe kleiner als Name, Klein eine Stufe kleiner als Text -- aber nur, solange die kleinere Schrift noch >= 0,75 x ihres
   Ziels ist (sonst dieselbe). Ergebnis (EN-Zeilenhoehen aus `media/fonts/EN/<n>x/*.fnt`): 1080/1x: Name Medium 29, Text Small 19, Klein Small 19;
   4K/2x: Large 40 / Medium 33 / Small 26; 4K/1x: Large 33 / Medium 29 / Medium 29; 1440/1x: Large 33 / Small 19 / Small 19.
3. Tooltips: Vanillas `ISToolTip` (eigene Schrift, wie jeder Vanilla-Tooltip). Kein `drawTextZoomed` (kein Vanilla-Aufrufer, PB1C 0.8).

### 1.3 Farben (r, g, b, a; 0..1)
| Name | Wert | wo |
|---|---|---|
| winBg | 0.075, 0.070, 0.065, 0.95 | Fenster |
| winBorder | 0.55, 0.38, 0.16, 0.85 | Rahmen |
| accent (Honig) | 1.00, 0.62, 0.18, 1 | Linie oben, aktiver Knopf (Rand + 4-px-Leiste links), Haken, laufendes Segment |
| cardBg / cardBorder | 0.115, 0.105, 0.095, 1 / 0.20, 0.18, 0.16, 1 | Karten |
| divider | 1, 1, 1, 0.08 | Trennlinien |
| title | 1.00, 0.70, 0.30, 1 | Kartentitel, Tooltip-Kopfzeile |
| name | 0.99, 0.93, 0.80, 1 | Name |
| text / text2 / dim | 0.93, 0.90, 0.85 / 0.70, 0.66, 0.60 / 0.50, 0.47, 0.43 (a 1) | Text / Nebentext / "kommt spaeter" |
| honeyText | 1.00, 0.72, 0.32, 1 | Zeile 3, "Lv n" |
| track / trackBorder / barHi | 0.20, 0.18, 0.16, 1 / 0, 0, 0, 0.35 / 1, 1, 1, 0.18 (1 px oben auf der Fuellung) | Balken |
| Leben (nach Wert v) | v >= 0,6 gruen 0.45, 0.76, 0.32; 0,3..0,6 Mischung gelb 0.95, 0.66, 0.20 -> gruen; < 0,3 rot 0.82, 0.26, 0.20 -> gelb | Leben-Balken |
| Ausdauer (nach Wert v) | v >= 0,35 blau 0.38, 0.64, 0.92; < 0,35 Mischung orange 0.90, 0.50, 0.20 -> blau | Ausdauer-Balken |
| pipGold / pipNow / pipEmpty / pipEdge | 1.00, 0.86, 0.40 / 1.00, 0.62, 0.18 / 0.22, 0.20, 0.18 / 0.30, 0.28, 0.25 | Faehigkeits-Segmente (Gold wie Vanillas Skill-Kaestchen 1/0,89/0,38, `V:client/XpSystem/ISUI/ISSkillProgressBar.lua:13-16`) |
| Knopf normal | bg 0.15, 0.14, 0.125 / Rand 0.34, 0.30, 0.25 / Text 0.92, 0.89, 0.84 | |
| Knopf Maus darueber | bg 0.22, 0.20, 0.17 / Rand 0.62, 0.46, 0.24 | |
| Knopf aktiv (laufender Befehl) | bg 0.40, 0.23, 0.07 / Rand accent doppelt (aussen a 1, innen a 0,45) / Text 1.00, 0.93, 0.78 / Leiste 4 px accent links | |
| Knopf grau | bg 0.10, 0.095, 0.09 / Rand 0.20, 0.19, 0.17 / Text 0.45, 0.42, 0.39 | |
| gedrueckt | bg x 0,8 | |
| Schalter-Kaestchen | 16 x 16, bg 0.10, 0.09, 0.085, Rand 0.55, 0.50, 0.44; an: Innenquadrat 10 x 10 accent | |
| Zustand-Farbe sc | folgt/kommt 0.45, 0.78, 0.40; bleibt/sitzt 0.95, 0.70, 0.30; frei 0.40, 0.75, 0.80; versteckt 0.95, 0.42, 0.30; faehrt mit 0.45, 0.62, 0.95; vermisst 0.90, 0.30, 0.25; ausser Reichweite 0.60, 0.58, 0.55 | Chip: bg sc x 0,20, Rand sc a 0,85, Punkt sc |
| Kopf-Scheibe | 0.24, 0.16, 0.08 (eingefaerbte Scheibe) | hinter dem Symbol |

### 1.4 Kopf: Zustand, Abstand, Fusszeile (Vorrang von oben nach unten)
| Zustand | aus der Sicht | Chip (EN) | Fusszeile |
|---|---|---|---|
| vermisst | `st == "missing"` | "Missing" | "Your bear has no body right now. Unstuck brings it back next to you." |
| faehrt mit | `ride == true` | "Riding with you" | "It rides with you and gets out when you stop." |
| ausser Reichweite | `ld ~= true` (tame) | "Out of reach" | "Too far away for orders. Unstuck brings it to you." |
| versteckt sich | `hide == true` | "Hiding" | normaler Hinweis |
| kommt | `cm == true` | "Coming to you" | normal |
| Modus | `mode` follow / stay / sit / roam | "Following you" / "Staying" / "Sitting" / "Roaming" | normal: "Drag to move.  V or Esc closes." |
Abstand: aus `v.x, v.y` (Sicht) und der Spielerkachel: < 2 "right next to you", sonst "%1 tiles to the %2" (Richtung `B.DirOf` + vorhandene
`UI_BN_Bear_Dir_*`); bei vermisst/ausser Reichweite "last seen %1 tiles to the %2". Zeile 2: Koerper ("Bear cub" bei `bd ~= "big"`, sonst "Bear")
+ " - day %2" (`v.day`); Zeile 3: `v.nst`/`v.nxt` -> Stufe (`U.StageName`) "in %2 day(s)", sonst "full-grown". Fehlen die Zahlen (alte Sicht),
faellt die Zeile weg -- nie geraten.

### 1.5 Werte und Faehigkeiten (Daten: Sicht, 5.3)
- **Leben** "now / max": now = round(hp/100 x hpMax), max = `hpMax`; Balken = hp/100. **Ausdauer** gleich aus `sta`/`staMax`. **Kann tragen**
  "up to %1" aus `carry` (gerundet). Fehlt ein Wert (missing ohne `hp`): Zeile "--" ohne Balken, nie 0.
- **Kommt spaeter:** Hunger, Durst, Muedigkeit, Vertrauen -- nur Etikett in dim, KEIN Balken (ein leerer Balken saehe aus wie 0). Tooltip der vier
  (eine Zeile mit Tooltip ueber die ganze Breite): "Hunger, thirst, tiredness and trust come with a later version. Nothing is counted yet."
- **Faehigkeiten:** je Schluessel `agi vit con fgt fsh nos` (`B.SKILLS`, `S:shared/BanditsNPCBearStats.lua:110-111`): `B.SkillProgress(v, key)` ->
  Stufe L, xp in der Stufe, Bedarf (rechnet direkt auf dem Sicht-Eintrag, gleiche Feldnamen `xAgi..xNos`, FF 3.2). Segmente: k < L Gold;
  k == L (L < 10) dunkel + Honig-Fuellung xp/Bedarf; Rest dunkel mit Rand. Text rechts "Lv L" und Prozent (ganzzahlig, abgerundet).
- **Tooltips** (Zeilen mit `" <LINE> "` verbunden wie `V:client/ISUI/ISGarmentUI.lua:136`; nie `<`/`>` in UI.json):
  Kopf "Agility - level 3" | Wirkung mit Zahl jetzt | woher die Erfahrung | "kommt spaeter"-Satz (nur wo es noch nicht wirkt) | "123 of 156 to level 4"
  bzw. "Level 10 - the highest level."
  | Faehigkeit | Wirkung (Zahl aus der Sicht) | waechst durch | ehrlich |
  |---|---|---|---|
  | Agility | Ausweichen `dodge` % jetzt, `BearDodgeMax` % auf 10 (ENT:221-222, :227) | jeden Treffer, den er einsteckt | wirkt erst mit dem Kampf (kommt spaeter) |
  | Toughness | + `vitPerLv` x L x 100 % Leben (ENT:223) | jeden Treffer, den er einsteckt | steigt erst mit dem Kampf; der Bonus wirkt schon |
  | Endurance | + `conPerLv` x L x 100 % Ausdauer, schnellere Erholung (ENT:226) | Rennen, ausser Puste kommen | wirkt jetzt |
  | Fighting | + `fgtB` % Schaden, + `BearFightBonusMax` % auf 10 (ENT:228, :230) | jeden Treffer, den er austeilt | wirkt erst mit dem Kampf |
  | Fishing | Fang-Chance `fish` % (ab Halbstark, ENT:213) | Fischen | Fischen kommt spaeter |
  | Keen nose | riecht Zombies frueher, warnt mit Brummen: Weite `nose` Kacheln (ENT:220) | Schnueffeln | kommt spaeter, abschaltbar |
- Leben- und Ausdauer-Zeile haben Tooltips ("Grows every day as your bear grows, and with Toughness. Heals slowly on its own." /
  "Drops while your bear runs and comes back while it rests. More with Endurance. It matters once bears fight (comes later).");
  "Can carry": "How much your bear could carry. Its own inventory and bags come later."

### 1.6 Befehls-Knoepfe: Zustaende (Vorpruefung aus der Sicht; entscheiden tut der Schreiber, 2)
Reihenfolge der Pruefung je Knopf, der erste Treffer gewinnt; grau = `enable = false` + Grund als Tooltip (Vanilla zeigt Tooltips auch grau,
`V:client/ISUI/ISButton.lua:18-20`, `:176`; Vorbild `V:client/ISUI/Hutch/ISHutchUI.lua:617-623`).
| Knopf | aktiv hervorgehoben, wenn | grau mit Grund, wenn (Schluessel) | sonst Tooltip |
|---|---|---|---|
| Follow | `mode == "follow"` und nicht `cm` | ride (`Why_Riding`+Big); missing oder `ld ~= true` (`Why_OutOfReach`+Big); Spieler im Fahrzeug (`Why_InCar`); Abstand > `BearFollowMaxDistance` (`Why_Far`) | `Menu_FollowTip` |
| Stay | `mode == "stay"` | ride; missing/`ld` | `Win_StayTip` |
| Sit | `mode == "sit"` | ride; missing/`ld` | `Win_SitTip` |
| Roam free | `mode == "roam"` | ride; missing/`ld` | `Win_RoamTip` (%1 = `B.Opt("BearRoamRadius")`) |
| Come here | `cm == true` | ride; missing/`ld`; im Fahrzeug; zu weit (`Why_Far`) | `Win_ComeTip` |
| Unstuck | nie | ride; im Fahrzeug; Abklingzeit (`Why_CallWait`+Big, Minuten wie `S:client/BanditsNPCBearMenu.lua:247-260`); Beschriftung dann "Unstuck  m:ss" (`Win_UnstuckWait`) | `Menu_CallTip`+Big |
| Rename | -- | nie grau (auch vermisst, wie `B.HandleRename`) | -- |
| Passive (Schalter) | Haken = `pas == true` | nie grau | `Win_PassiveTip` |
| Name tag (Schalter) | Haken = `U.TagOn(v)` | nie grau | `Win_TagTip` (+ Zeile `Win_TagOffAll`, wenn `TagShow` aus ist) |
Der aktive Knopf bleibt klickbar (nochmals "Sit" setzt nichts Neues; der Schreiber antwortet mit derselben Meldung, gedrosselt). Nach einem Klick
zeigt der Knopf bis zur naechsten Sicht keinen Zwischenstand (der Schreiber meldet; die neue Sicht faerbt um).

### 1.7 Mod-Option (OBERFLAECHE, `client/BanditsNPCBearOptions.lua`, nach `MarkerSize`, KEIN pcall)
```
local ws = o:addComboBox("WinSize", "UI_BN_Bear_MO_WinSize", "UI_BN_Bear_MO_WinSizeTip")
ws:addItem("UI_BN_Bear_MO_Auto", true)  ws:addItem("UI_BN_Bear_MO_Pct100") ... ws:addItem("UI_BN_Bear_MO_Pct300")   -- 7 Eintraege wie MarkerSize
```
Gelesen `U.Opt("WinSize", 1)` -> `U.MarkerFactor(H, idx)`. Aenderung wirkt beim naechsten Oeffnen oder 1-s-Takt (Layout neu).

### 1.8 Oeffnen, Schliessen, Lage
- Ein Fenster-Objekt je Spielstart (beim ersten Oeffnen angelegt, bei `OnGameStart` vergessen/abgemeldet wie `S:client/ISUI/BanditsNPCBearHud.lua:770-777`).
  Oeffnen: `addToUIManager()`, `setVisible(true)`, `bringToTop()`; Schliessen: `setVisible(false)`, `removeFromUIManager()` (wie
  `V:client/ISUI/Crafting/ISHandcraftWindow.lua:293-295`). Tooltips der Kinder werden beim Schliessen mit abgemeldet (Kind-Tooltips schliessen sich in
  `updateTooltip`, sobald die Maus weg ist; zusaetzlich `btn.tooltipUI:setVisible(false)`/`removeFromUIManager()` wie `ISButton.lua:340-343`).
- Esc / eigene Taste: `o:setWantKeyEvents(true)`; `isKeyConsumed(key)` = `key == Keyboard.KEY_ESCAPE or getCore():isKey("Bear window", key)`;
  `onKeyRelease(key)` -> schliessen (`ISHandcraftWindow.lua:289-297`, `:386`). Merkt `U.winClosedAt` (ms), damit der OnKeyPressed-Weg im selben
  Loslassen nicht wieder oeffnet (250 ms; NUR JAR sagt, dass ein verbrauchter Druck ohnehin kein OnKeyPressed ausloest -- doppelt gesichert).
- **Lage merken:** `ISLayoutManager.RegisterWindow("BanditsNPCBearWindow", Win, win)` beim Anlegen (`V:client/ISUI/ISLayoutManager.lua:6-13`,
  Klasse mit eigenen Funktionen wie `V:client/Chat/ISChat.lua:1172`). `Win:SaveLayout(name, layout)` schreibt NUR `layout.x`, `layout.y` (kein
  `visible` -> nie automatisch offen nach dem Laden, FF 2.3); `Win:RestoreLayout(name, layout)` setzt x/y (tonumber) und klemmt aufs Bild. Vanilla
  schreibt `layout.ini` beim Spielspeichern (`:191-232`), je Aufloesung. Nur Spieler 0.
- Bildschirm-Aufloesung geaendert (`Events.OnResolutionChange`, `V:client/ISUI/PlayerData/ISPlayerData.lua:206`): Layout neu, klemmen.
- Spieler tot / kein Spieler 0: beim naechsten Takt schliessen.
- Kein eigener Baer (Sicht frisch, `me.bears == 0`): kein Fenster, `HaloTextHelper.addText(player, U.T("UI_BN_Bear_Win_NoBear"))`
  (`V:client/Foraging/forageClient.lua:73`). Sicht nicht frisch (`U.Fresh()` falsch): `U.AskHello(player)` + Hinweis `Win_NoData`.
- Waehrend es offen ist, verschwindet der gewaehlte Baer aus der Sicht (Tod, Eintrag weg): naechster eigener Baer, sonst schliessen.

---

## 2. Befehle Schritt fuer Schritt

Gemeinsam: Klick -> `B.Ask(player, Befehl, args)` (`S:shared/BanditsNPCBear.lua:541-550`; MP `sendClientCommand`, Rolle user genuegt; SP direkt
`B.Handle`). Nie eine leere Tabelle (`S:client/BanditsNPCBearClient.lua:381-383`). Schreiber: `B.Handle` (`S:server/BanditsNPCBearServer.lua:371-406`)
-> Handler prueft: Text-Kennung, Spielerschluessel (`B.PlayerKey`), Eintrag, Besitzer, Zustand; Drossel ueber `B.AskOk` je "Spieler|Befehl|ok/no"
500 ms (`S:server/BanditsNPCBearFollow.lua:53-82`). Antwort: Meldung `B.Tell` (mit `B.NoteBd`) + `B.FlushViews()`. Was der Client glaubt, zaehlt nie.

### 2.1 Folgen (`Mode` mode = "follow") -- B1b, erweitert
1. Ausloeser: Knopf Follow (oder Rechtsklick "Follow me", unveraendert).
2. Schreiber `B.HandleMode`: Kennung Text; mode in `B.MODES`; Eintrag fehlt oder `missing` -> `Why_Gone` (+NoteBd, A1); nicht Besitzer/nicht tame
   -> `Why_NotOwner`; `ride` -> `Why_Riding`; Koerper nicht geladen (`B.FindAnimal` nil) -> **`Why_OutOfReach`** (neu, statt Why_Gone); Spieler im
   Fahrzeug -> `Why_InCar`; Abstand > `BearFollowMaxDistance` -> `Why_Far`; Drossel; `B.SetMode(rec, "follow", "ask")`.
3. `B.SetMode` (4 Modi, 5.1): war der alte Modus "sit" und sass er (`s.sat`), dann `s.standUntil = ms + standMs` (Aufstehen 2,3 s halten); `s.come`
   weg; Meldung `Note_Follow`.
4. Wechselwirkungen: Mitfahren/Verstecken/Laerm/Tausch wie B1b-B1e (Folgen-Takt `B.FollowStep`). Speichern: `mode` im Register + Spiegel.
   Tod: Eintrag weg. Besitzer offline: haelt und wartet als follow (A7, unveraendert).

### 2.2 Bleiben (`Mode` "stay") -- neu: stehen bleiben
1. Pruefungen wie 2.1 Schritt 2 ohne Fahrzeug/Abstand. `B.SetMode(rec, "stay", "ask")`: Heimat = jetzige Kachel, Meldung `Note_Stay`.
2. Hirn-Takt (`liveRec` -> `B.OrderStep`, 5.4): Regel 6 (Besitzer haelt still Futter hin -> kommt bis `comeFed` 2, nimmt die Heimat mit) und Regel 7
   (Futter nah / Besitzer in Reichweite -> halten) wie heute; weiter als `stayBack` (3) von der Heimat -> zurueck (gehend bis `backRunDist` 8, sonst
   rennend, `B.MoveTo`); sonst `B.Hold` je Takt (keine Engine-Wanderung).
3. Wechselwirkungen: Zombie -> `B.GuardStep` geht vor (versteckt sich), danach zurueck; Laerm -> Laerm-Wache faengt die Flucht ab, danach zurueck;
   Tausch (Tag 15) -> neuer Koerper an derselben Stelle, Modus bleibt; Speichern/Laden -> Modus + Heimat aus Register/Spiegel; Besitzer offline -> bleibt.

### 2.3 Sitz (`Mode` "sit") -- neu
1. Pruefungen wie Bleiben. `B.SetMode(rec, "sit", "ask")`: Heimat = jetzige Kachel, `s.sat = nil`, Meldung `Note_Sit`.
2. Schreiber-Takt (`B.OrderStep`): kein Futter-Locken (er sitzt); weiter als `stayBack` -> zurueck gehen, `s.sat = nil`; sonst `B.Hold`; steht er
   `sitSettleMs` (800) lang in `stayNear` (1,5) -> `s.sat = true`, `B.Touch(rec)` (Sicht `sit = true`). Jede Bewegung (zurueck, Verstecken, Laerm,
   Locken) -> `s.sat = nil` + `B.Touch(rec)`.
3. Jeder Client (`U.PoseTick`, 250 ms, 5.6 / 6.6): Sicht `sit == true` und nicht `busy`/`hide`/`ride` -> an der eigenen Kopie "sitdown" -> nach
   `SIT_DOWN_MS` 1700 "sit" (Schleife); `sit` faellt weg -> "standup" -> nach `STAND_UP_MS` 1400 Variable loeschen. Waehrend `busy` (Fuettern/
   Streicheln laeuft, die Zeitaktion setzt "eat") schreibt der Treiber nichts und beginnt danach neu mit "sitdown".
4. Verlassen: jeder andere Modus -> `B.SetMode` setzt `s.standUntil = ms + standMs` (nur wenn `s.sat`); `B.StandStep` haelt bis dahin (ausser
   Zombie: `B.GuardStep` kommt vorher).
5. Wechselwirkungen: Fuettern/Streicheln im Sitzen geht (er steht dafuer kurz, setzt sich danach wieder); Tausch/Call/Aussteigen = neuer Koerper ohne
   Variable -> der Treiber sieht eine neue Kopie und setzt sich neu (`clearBodySession` loescht `s.sat`, `s.standUntil`); Speichern/Laden -> mode
   "sit" bleibt, setzt sich nach dem Laden wieder; MP: jeder Client in Sichtweite (Sicht `tellDist` 60) sieht ihn sitzen.

### 2.4 Frei herumlaufen (`Mode` "roam") -- neu
1. Pruefungen wie Bleiben. `B.SetMode(rec, "roam", "ask")`: Mittelpunkt (Heimat) = jetzige Kachel, `s.roam = nil`, Meldung `Note_Roam` (%1 Radius).
2. Schreiber-Takt (`B.OrderStep`): Regel 7 (Besitzer in Reichweite -> halten, damit Fuettern geht); KEIN Locken mit Heimat (sonst zoege Futter ihn aus
   dem Bereich); weiter als R (`BearRoamRadius`) vom Mittelpunkt -> zurueck gehen; eigener Weg laeuft (`ms < s.ownUntil`) -> weiter; Pause laeuft
   (`ms < s.roam.pauseUntil`) -> `B.Hold`; sonst neues Ziel `B.RoamSpot(rec, a, R)` (5.5) -> `B.MoveTo(..., { walk = true })`, danach Pause
   `ZombRand(roamPauseMin, roamPauseMax)` ms (8..20 s). Kein Ziel gefunden -> Pause und naechster Versuch.
3. Grenze "nie ausserhalb": nur eigene Ziele im Kreis UND im selben Raum-Zustand wie der Mittelpunkt (drinnen/draussen); die Engine wandert nie
   (Halten in den Pausen). Verschiebt ihn Laerm/Zombie hinaus, geht er zurueck.
4. NPC Crew (spaeter, nur Naht 9 in NAEHTE.md): statt Kreis die Basisflaeche des Beacons (`BanditsNPC.Base.Zone`, FF 4.3) -- nicht gebaut.
5. Wechselwirkungen wie Bleiben; `s.roam` ist nur Sitzung (Deckel: eine Tabelle je Eintrag), nach Laden neu.

### 2.5 Komm her (`Come` { id }) -- neu
1. Ausloeser: Knopf Come here.
2. Schreiber `B.HandleCome`: Kennung; Eintrag fehlt -> `Why_Gone`; nicht Besitzer/nicht tame -> `Why_NotOwner` (missing -> `Why_OutOfReach`);
   ride -> `Why_Riding`; Koerper nicht geladen -> `Why_OutOfReach`; Spieler im Fahrzeug -> `Why_InCar`; Abstand > `BearFollowMaxDistance` -> `Why_Far`;
   Drossel "Come"; `B.SetMode(rec, "follow", "come")` (Meldung `Note_Coming`), DANACH `s.come = ms`.
3. Takt: `B.FollowStep` laeuft wie Folgen; am Anfang `B.ComeCheck(rec, env, ms, players)`: Besitzer naeher als `comeNear` (3) + Koerper-Zuschlag
   (`B.BodyGap`) -> `B.SetMode(rec, "stay", "came")` (Meldung `Note_Came`, Heimat = hier); laenger als `comeMaxMs` (30 s) oder `f.stuck` ->
   `B.SetMode(rec, "stay", "comefail")` (`Note_ComeFail`). Steigt der Besitzer ins Auto -> wie Folgen (steigt mit ein, `s.come` weg).
4. Wechselwirkungen: aus "sit" -> erst aufstehen (2.3 Nr. 4); Zombie geht vor; Speichern mitten im Kommen -> `s.come` verloren, Modus follow bleibt
   (folgt dann einfach); Besitzer offline -> haelt (Folgen-Regel).

### 2.6 Passiv (`Passive` { id, on }) -- neu
1. Ausloeser: Schalter Passive. Client schickt `on = not v.pas` (Wahrheitswert).
2. Schreiber `B.HandlePassive`: Kennung; `type(args.on) == "boolean"` sonst still verwerfen; Eintrag -> `Why_Gone`; Besitzer und st tame/missing
   sonst `Why_NotOwner`; Drossel "Passive"; `rec.passive = true` bzw. nil; `B.Commit(rec)`; Meldung `Note_PassiveOn`/`Note_PassiveOff` (+NoteBd);
   `B.FlushViews()`.
3. Wirkung in F1: keine (Tooltip ehrlich, F-g). B5a liest `rec.passive`. Speichern: Register + Spiegel (`MARK_FIELDS`), Heilung uebernimmt es.
   Mitfahren/Vermisst: Schalter geht trotzdem.

### 2.7 Unstuck (`Call` { id }) -- B1c, unveraendert beim Schreiber
1. Knopf Unstuck -> `B.Ask(player, "Call", { id = v.id })` -- derselbe Weg wie Rechtsklick "Call to me" (`S:server/BanditsNPCBearRide.lua:300-375`):
   Besitz, tame ODER missing, nicht ride, nicht im Fahrzeug, Abklingzeit, freie stehbare Kachel 1..3 Ringe neben dem SPIELER (`B.SpotNear`, nie
   unstehbar, FF 5.1), frisch erzeugter Koerper wartet (`callFreshMs`), alter Koerper geladen-aber-ungebunden -> erst ein Suchlauf; neuer Koerper
   (`B.PlaceCub`, gen + 1), alter weg; Modus follow; Abklingzeit startet.
2. Geht fuer vermisste und nicht geladene Baeren (das ist der Unstuck-Fall). "Liegt am Boden" gibt es erst mit B5a.
3. Restzeit am Knopf aus `callWait` (Sicht, nur Besitzer) minus Zeit seit `U.viewAt`.

### 2.8 Name (`Rename` { id, name }) -- B1b, unveraendert
Knopf Rename -> `U.AskName(playerObj, v)` (`S:client/ISUI/BanditsNPCBearNameBox.lua:56-77`, Titel je Koerper). Schreiber `B.HandleRename`
(Besitzer, tame ODER missing, `B.CleanName`). Name im Register + Spiegel; Kopfzeile zeigt ihn nach der naechsten Sicht.

### 2.9 Namensschild an/aus (nur Client)
1. Schalter Name tag -> `U.TagSet(v, not U.TagOn(v))`. Schluessel = `tostring(v.u)` (Sicht-Feld `u`, 5.3; Text, damit nichts gerundet wird).
2. Datei `BanditsNPCBear.ini` beim Client (Lesen einmal je Spielstart, Schreiben bei jeder Aenderung; nur Zeilen fuer AUSGESCHALTETE Baeren
   "tagoff <u>"; Deckel 64 -- beim 65. die aelteste Zeile raus). `getFileReader(name, true)` / `getFileWriter(name, true, false)` wie
   `V:client/ISUI/ISLayoutManager.lua:127`, `:172`. Kein Server, keine ModData (MP-Clients speichern ihre globale ModData nicht, FF 9 Nr. 7).
3. Wirkung: `S:client/ISUI/BanditsNPCBearHud.lua` `describeTag` -- bei `U.TagOn(c) == false` keine Name/Zustand-Zeilen fuer diesen Baeren (die
   Werte-Zeilen folgen weiter ihren Optionen). `TagShow` aus = alle aus (Hauptschalter, unveraendert).
4. Gilt fuer jeden Baeren, den dieser Spieler sieht (auch fremde, wenn er sie im Fenster nicht oeffnen kann: nur eigene haben den Schalter).

### 2.10 Wechselwirkungen auf einen Blick
| | Mitfahren | Verstecken (Zombie) | Laerm | Tausch Tag 15 | Speichern/Laden | Tod | Besitzer offline |
|---|---|---|---|---|---|---|---|
| Folgen | steigt ein (B1c) | geht vor | Wache | neuer Koerper, folgt weiter | mode | Eintrag weg | haelt, wartet |
| Bleiben | nie | geht vor, dann zurueck | Wache, zurueck | gleiche Stelle | mode + Heimat | dto. | bleibt |
| Sitz | nie | steht auf, versteckt sich, setzt sich danach | steht auf, setzt sich wieder | setzt sich neu | sitzt wieder | dto. | sitzt |
| Frei | nie | dto., dann zurueck in den Kreis | dto. | weiter im Kreis | Mittelpunkt bleibt | dto. | laeuft weiter (nur solange geladen) |
| Komm her | steigt ein, wenn Besitzer im Auto | geht vor | Wache | geht weiter | wird "follow" | dto. | haelt |
| Passiv | Schalter geht | -- (B5a) | -- | bleibt | gespeichert | -- | -- |
| Unstuck | grau | geht | geht | neuer Koerper = Wunschkoerper (B1e 0.3) | Abklingzeit nur Sitzung | -- | nur Besitzer |
| Namensschild | -- | -- | -- | gleicher `u` -> bleibt | Client-Datei | Zeile bleibt (Deckel 64) | je Spieler |

---

## 3. Taste V und Rechtsklick (OBERFLAECHE, `client/BanditsNPCBearKey.lua`)

### 3.1 Anlegen (Dateiebene, Doppel-Riegel)
```
local NAME, HEAD = "Bear window", "[NPC Crew Bear]"
if type(keyBinding) == "table" and not has(NAME) then        -- has: ipairs-Schleife auf row.value (NC:client/ISUI/BanditsNPCFarmPanel.lua:1250-1255)
    table.insert(keyBinding, { value = HEAD })               -- V:shared/keyBinding.lua:8-10
    table.insert(keyBinding, { value = NAME, key = Keyboard.KEY_V })   -- V:shared/keyBinding.lua:131 (Keyboard.KEY_V)
end
Events.OnKeyPressed.Add(onKey)                                -- V:client/ISUI/FPS.lua:21
```
Der NAME ist fuer immer die Kennung in `keysB42.ini` (NC-Lehre `NC:client/BanditsNPCInteract.lua:19-34`). Beschriftung `UI_optionscreen_binding_NPC
Crew Bear` und `UI_optionscreen_binding_Bear window` (`V:client/OptionScreens/MainOptions.lua:2159-2177`) in 7 Sprachen. Vanilla laedt/speichert die
Taste selbst (FF 1.1).

### 3.2 `onKey(key)` -- Vorfahrt (je Weg nur Vanilla-/NC-Lua lesen)
1. `if not getCore():isKey(NAME, key) then return end` (`V:client/ISUI/FPS.lua:9`).
2. `if ISChat and ISChat.focused then return end` (`V:client/Chat/ISChat.lua:8`).
3. `p = getSpecificPlayer(0)`; nil oder `p:isDead()` -> return. `U.winClosedAt` juenger als 250 ms -> return.
4. **NPC Crew zuerst:** `local ia = BanditsNPC.Interact; if ia and ia.KEYBIND and ia.FindTarget and getCore():isKey(ia.KEYBIND, key) and
   ia.FindTarget(p) then return end` (NC `client/BanditsNPCInteract.lua:35-36`, `:40-...`; nur lesen, keine NC-Datei aendern).
5. **Fahrzeug-Radial:** `getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU, key) and ISVehicleMenu.getVehicleToInteractWith(p)` -> return
   (`V:client/ISUI/ISUIHandler.lua:36`, `:42`).
6. **Radial eines fremden Tiers:** `getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key)`, `an = AnimalContextMenu.getAnimalToInteractWith(p)`
   (`ISUIHandler.lua:43`), `an and not an:isWild() and not B.BodyKind(an)` (`V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171`) -> return.
7. Sonst `U.WinToggle(p)`; danach, wenn `an` UNSER Baer war: offenes Radial schliessen -- `local m = getPlayerRadialMenu(0); if m and
   m:isReallyVisible() then m:undisplay() end` (`ISUIHandler.lua:91-92`, `ISAnimalContextMenu.lua:1157-1164`).
Liegt "Bear window" auf einer anderen Taste, greifen 4-6 nicht (die `isKey`-Fragen sind dann falsch). Kollisionen (FF 1.2): Vanilla Animal-Radial
(V), Vehicle-Radial (V), Toggle UI (keine Vorgabe), NPC Crew "Talk to NPC" (V), Debug Shift+V; NPC Crew F6/F8 und Bandits G nicht.

### 3.3 Rechtsklick
`S:client/BanditsNPCBearMenu.lua` `cubMenu`: am eigenen gezaehmten Baeren (Block mit `addMode/addName/addCall`, `:307-312`) zusaetzlich
`menu:addOption(U.T("UI_BN_Bear_Menu_Window"), playerObj, onWindow, v.id)` mit Tooltip `Menu_WindowTip`; `onWindow` -> `U.WinOpen(playerObj, id)`.

---

## 4. B1e-Reste

**(a) A1/B6 "bear" statt "cub"** (FF 6.1): neue Big-Fassungen `Why_GoneBig` "The bear is gone.", `Note_DeadBig` "Your bear is dead.",
`Menu_HoldBig` "Hold out food for the bear", `Menu_HoldTipBig` "Takes it in your hand. Stand still and the bear comes closer." (7 Sprachen, `U.EN`).
KERN haengt `B.NoteBd` an, wo der Eintrag bekannt ist: `S:server/BanditsNPCBearFollow.lua:223` (nur wenn rec da), `:237`; `Ride.lua:365`;
`Registry.lua:492` (Note_Dead, zahm), `:500` (lost -- fuer zahm nicht mehr erreichbar, 0.8; bleibt fuer "fed"). Ohne Eintrag (Follow `:261`,
Ride `:310`, Server `:158`, `:169`) bleibt der Grundtext. OBERFLAECHE: `U.WhyText(whyKey, whyVal, bd)` waehlt ueber `U.TB` (Aufrufer im Menue
geben `v.bd`); `holdWanted` gibt das passende Junge `c` zurueck (statt true), `addHold` nimmt `U.TB(key, c.bd)`. Neue F1-Texte haben ihre Big-Fassung
gleich mit (7.6).

**(b) C1 Baer ohne Koerper** (0.8; FF 5.2): `B.ReviveMissing(missing, players, ms)` (Order.lua), Aufruf in `brainTickBody` direkt nach
`countMisses(missing, players, B.Now())` (nur wenn in diesem Takt ein Suchlauf lief):
1. je Eintrag der Liste `missing`: noch derselbe Eintrag (`reg.cubs[id] == rec`), `st == "missing"`, `ride == nil`, Besitzer unter `players`
   (online), `B.AreaLoaded(rec.x, rec.y)`, `B.FindAnimal(rec) == nil` (der Suchlauf dieses Takts hat einen geladenen alten Koerper schon gebunden
   = "erst suchen").
2. `s.revN = (s.revN or 0) + 1`; kleiner als `reviveScans` (2) -> weiter (Vermissten-Suchlauf je 30 s -> ~60 s nach "missing", ~75 s nach dem Verlust).
3. Kachel `B.SpotNear(rec.x, rec.y, rec.z, B.CFG.callRing, rec.gen)` (an SEINER Stelle, nicht beim Spieler, FF 5.2 Nr. 3); keine -> `s.revFail + 1`,
   ab `reviveFailLog` (3) `B.ErrEvery("revive:" .. id, 600000, ...)`, naechster Suchlauf.
4. `B.PlaceCub(rec, x, y, z, "revive")` -> gen + 1, st tame, Spiegel sofort, Groesse/Leben (Wunschkoerper). `s.revN = nil`. Meldung `Note_Back`
   ("Your bear is back."; passt fuer beide Koerper) an den Besitzer. `B.Log`.
5. Deckel: hoechstens EIN Eintrag je Takt. Kein Doppel: ein spaeter auftauchender alter Koerper hat kleinere Generation -> "stale" -> nie gebunden,
   unbeobachtet entfernt (`S:server/BanditsNPCBearWorld.lua:634-641`, `:729-736`, `:767-800`). Restrisiko wie Call (FF 5.2 Nr. 5): steht der Spieler
   naeher als 25 Kacheln, bleibt die alte Kopie bis dahin sichtbar ohne Schild.
6. `slowRec` (`S:server/BanditsNPCBearServer.lua:486-493`): `st == "missing"` zaehlt `missH` weiter (Diagnose), schliesst aber NIE mehr
   ("lost" nur noch fuer "fed" ueber `countMisses`). Unstuck wirkt fuer "missing" schon heute.

**(c) A5 288-px-Bilder:** erledigt, kein Handlungsbedarf (FF 6.2: UI-Bilder ueber `getTexture` werden nicht gedeckelt -- NUR JAR; Vanilla zeigt selbst
Bilder > 256 px, `V:client/XpSystem/ISUI/ISCharacterProtection.lua:182-191`). Das Fenster nutzt die 288er Datei fuer das Kopf-Symbol.

**(d) C3/B7 Klickflaeche der Markierung:** keine kleine sichere Aenderung (FF 6.3; `setWantMouseEvents(false)` nimmt Kevins Doppelklick weg). In F1
nichts aendern; Frage 6 aus `gegen_bericht_b1e.md` bleibt (Text dort: "bis du das Junge gefunden hast, plus ~1 Minute").

---

## 5. Register, Spiegel, Sicht, Sitzung (KERN)

### 5.1 Register
```
rec.mode    = "follow" | "stay" | "sit" | "roam" | nil (= stay)     -- nur tame; B.MODES
rec.passive = true | nil                                             -- nur tame/missing
B._s[id]   += { sat, satAt, standUntil, roam = { pauseUntil }, come, revN, revFail, ldSent, hideSent }   -- nur Sitzung
```
`B.InitRegistry` (`S:server/BanditsNPCBearRegistry.lua:131-135`): `mode` nicht in `B.MODES` -> nil + Fehlerzeile (wie heute); `passive` nicht `true`
-> nil (Fehlerzeile nur, wenn es etwas anderes als nil war). `clearBodySession` (`Ride.lua:53-58`) += `s.sat, s.satAt, s.standUntil, s.roam`
(nicht `come`, nicht `revN`).

### 5.2 Spiegel (Fassung bleibt `B.MARK_V = 2`)
`MARK_FIELDS` (`S:server/BanditsNPCBearHeal.lua:42-47`) += `"passive"`. `B.Restore` (`:228-229`) und `B.TakeNewerMark` (`:368-369`): `mode` in
`B.MODES` (sonst nil), `passive = (mark.passive == true) or nil` nur bei tame.

### 5.3 Sicht (`viewEntry`, `S:server/BanditsNPCBearRegistry.lua:563-590`; `B.GrowView`, `S:server/BanditsNPCBearGrow.lua:751-772`)
Neue flache Felder (Zahl/Text/Wahrheitswert, `copyFlat` nimmt sie von selbst):
| Feld | Wert | wann |
|---|---|---|
| `mode` | wie heute, jetzt auch "sit"/"roam" | tame |
| `pas` | true / fehlt | tame/missing, `rec.passive` |
| `u` | `rec.u` (Zahl) | tame/missing |
| `ld` | true / fehlt | `s.obj` existiert in der Welt (`isExistInTheWorld`, wie `oid` daneben) |
| `hide` | true / fehlt | `s.g.on == true` (Zombie-Wache) |
| `sit` | true / fehlt | `rec.mode == "sit" and s.sat == true` |
| `cm` | true / fehlt | `s.come ~= nil` |
| `busy` | true / fehlt | `s.busyUntil` > jetzt (Fuettern/Streicheln, B1e 0.7) |
| GrowView jetzt fuer **tame UND missing** | + `xAgi xVit xCon xFgt xFsh xNos` (Erfahrung, auf 0,1 gerundet), `carry` (ganz), `dodge` (%), `fgtB` (%), `fish` (%), `nose` (0,1) aus `B.StatsOf` | |
**Sicht nachschicken bei Wechsel** (`B.Touch(rec)`, die Sicht geht mit `B.FlushViews` am Ende des Takts): `s.sat` an/aus (Order.lua), Zombie-Wache
an/aus (`B.GuardStep`: `g.on` vorher/nachher verschieden), `ld` an/aus (Schritt 4 des Hirn-Takts: `(B.FindAnimal(rec) ~= nil) ~= s.ldSent`),
`busy` an/aus (`B.BodyBusy`), `s.come` gesetzt/geloescht (laeuft ueber `B.SetMode` -> Commit -> Touch). Kein Nachschicken je Takt ohne Wechsel.

### 5.4 Takt (`S:server/BanditsNPCBearServer.lua` `liveRec`)
Reihenfolge nach `B.GuardStep` (unveraendert zuerst): `if rec.st == "tame" and B.StandStep and B.StandStep(rec, a, ms) then return end` ->
Folgen-Zweig (unveraendert, darin `B.ComeCheck`) -> **neu** `if rec.st == "tame" and B.OrderStep and B.OrderStep(rec, a, env, ms, players) then
return end` -> `B.Decide` (wild/scheu/angefuettert und Rueckfall wie heute). `B.OrderStep` gibt false fuer follow und fuer fremde Zustaende.

### 5.5 Zufallsziel im Kreis (`S:server/BanditsNPCBearWorld.lua`, neu `B.RoamSpot(rec, a, r)`)
Mittelpunkt `rec.hx, rec.hy, rec.hz` (fehlt -> rec.x/y/z); bis `B.CFG.tries` (8) Versuche: Winkel `ZombRandFloat(0, 2 * math.pi)`, Abstand
`ZombRandFloat(0, r)` (Form `World.lua:175-179`); Kachel `getCell():getGridSquare`; muss `spotOk` (lokal, `:227-235`), mindestens `roamMinStep` (3)
vom Tier, und `(sq:getRoom() == nil) == (center:getRoom() == nil)` (`V:shared/Util/AdjacentFreeTileFinder.lua:240`); sonst nil.

### 5.6 Anim-Treiber (OBERFLAECHE, `client/BanditsNPCBearPose.lua`, `U.PoseTick` je 250 ms aus `Events.OnTick`)
Je Sicht-Eintrag mit `st == "tame"`: `obj = U.CubObj(id)` (lebende Kopie aus der Balken-Tabelle, kein Suchlauf); Zustand `P[id] = { obj, ph, t0 }`:
- `obj` nil oder anders als `P[id].obj` -> `P[id] = nil`.
- `want = v.sit == true and not v.busy and not v.hide and not v.ride`.
- `v.busy` -> `P[id] = nil` (nichts schreiben; die Zeitaktion steuert "eat").
- want und kein P -> `obj:clearVariable("NCBearDone")`, `obj:setVariable(B.ACT, "sitdown")`, ph "sitdown".
- ph "sitdown" und want und `ms - t0 >= 1700` -> `setVariable(B.ACT, "sit")`, ph "sit".
- nicht want und ph "sitdown"/"sit" -> `clearVariable("NCBearDone")`, `setVariable(B.ACT, "standup")`, ph "standup".
- ph "standup" und `ms - t0 >= 1400` -> `clearVariable(B.ACT)`, `clearVariable("NCBearDone")`, P nil.
- Deckel: `P` nur fuer Kennungen der Sicht (bei jeder neuen Sicht `forget`). Nie `getVariableString` (0.5). Im SP ist die Kopie das Tier des
  Schreibers -- dasselbe. Belege 9.

---

## 6. Stellwerte und Sandbox (KERN `S:shared/BanditsNPCBear.lua`)

### 6.1 `B.CFG` neu (flach, zur Laufzeit per `NCBear_CubSet`)
| Feld | Vorgabe | Bedeutung |
|---|---|---|
| `stayNear` | 1.5 | "an seiner Stelle" bis (Kacheln) |
| `stayBack` | 3 | Bleiben/Sitz: weiter weg -> zurueck |
| `backRunDist` | 8 | zurueck gehend bis, sonst rennend |
| `sitSettleMs` | 800 | so lange ruhig an der Stelle, dann "sitzt" |
| `standMs` | 2300 | Aufstehen 1,3 s + 1 s Frist (Clip `NCBear_StandUp`, FF 4.1) |
| `roamMinStep` | 3 | Frei: neues Ziel mindestens so weit |
| `roamPauseMin` / `roamPauseMax` | 8000 / 20000 | Frei: Pause zwischen zwei Wegen (ms, Zufall) |
| `comeNear` / `comeMaxMs` | 3 / 30000 | Komm her: angekommen bis / aufgeben nach |
| `reviveScans` / `reviveFailLog` | 2 / 3 | C1: Wartefrist in Vermissten-Suchlaeufen / Fehlerzeile ab Versuch |
`B.MODES = { follow = true, stay = true, sit = true, roam = true }`.

### 6.2 Sandbox (KERN `B.OPTS`; OBERFLAECHE `sandbox-options.txt` + 7 x `Sandbox.json`, Zahlen TEXTGLEICH)
`BearRoamRadius = { def = 12, min = 4, max = 30 }` -- integer, page BanditsNPC, translation `BanditsNPC_BearRoamRadius`.
EN: "Bear: roaming radius (tiles)" / Tooltip "How far a bear on Roam free may stray from the spot where you gave the order."

---

## 7. GENAUE SCHNITTSTELLE (WOERTLICH einhalten; Abweichung sofort nach `schnittstelle_aenderungen.md`, Abschnitt "F1 KERN" / "F1 OBERFLAECHE")

### 7.1 Wer schreibt welche Datei (unter `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | Bauer | Was |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | KERN | `B.MODES`, `B.CFG` (6.1), `B.OPTS.BearRoamRadius`, Kopf-Kommentar |
| `lua/shared/BanditsNPCBearRules.lua` | KERN | `B.ModeOf` (4 Modi), `B.OrderDecide` (neu, rein) |
| `lua/server/BanditsNPCBearOrder.lua` (**neu**) | KERN | `B.OrderStep`, `B.StandStep`, `B.ComeCheck`, `B.HandleCome`, `B.HandlePassive`, `B.ReviveMissing` |
| `lua/server/BanditsNPCBearFollow.lua` | KERN | `B.SetMode` (4 Modi, neue why), `B.HandleMode` (4 Modi, `Why_OutOfReach`), `B.FollowStep` ruft `B.ComeCheck`, NoteBd an Why_Gone |
| `lua/server/BanditsNPCBearServer.lua` | KERN | `B.Handle` ("Come", "Passive"), `liveRec` (5.4), `brainTickBody` (C1, `ld`-Wechsel), `slowRec` (4b Nr. 6) |
| `lua/server/BanditsNPCBearRegistry.lua` | KERN | `B.InitRegistry` (mode/passive), `viewEntry` (5.3), `B.Close` NoteBd |
| `lua/server/BanditsNPCBearHeal.lua` | KERN | `MARK_FIELDS`, `B.Restore`, `B.TakeNewerMark` (5.2) |
| `lua/server/BanditsNPCBearGrow.lua` | KERN | `B.GrowView` (tame + missing, 5.3), `B.BodyBusy` -> `B.Touch` |
| `lua/server/BanditsNPCBearGuard.lua` | KERN | `B.GuardStep`: Touch bei Wechsel von `g.on` |
| `lua/server/BanditsNPCBearRide.lua` | KERN | `clearBodySession` (5.1), NoteBd an Why_Gone `:365` |
| `lua/server/BanditsNPCBearWorld.lua` | KERN | `B.RoamSpot` (5.5) |
| `attrappe/kern/attrappen.lua` (Zufall, Raum), `attrappe/f1_kern/run.lua` (**neu**) | KERN | 8.1 |
| `lua/client/BanditsNPCBearKey.lua` (**neu**) | OBERFLAECHE | Taste (3.1, 3.2) |
| `lua/client/BanditsNPCBearWinData.lua` (**neu**) | OBERFLAECHE | Modell des Fensters (rein bis auf `U.T`/`B.*`, testbar ohne UI) |
| `lua/client/ISUI/BanditsNPCBearWinParts.lua` (**neu**) | OBERFLAECHE | Knopf-/Zeilen-/Schalter-Klassen, Farben, Schriftwahl, Farbverlauf |
| `lua/client/ISUI/BanditsNPCBearWindow.lua` (**neu**) | OBERFLAECHE | Fenster (ISPanel), Aufbau, Zeichnen, Takt, Lage |
| `lua/client/BanditsNPCBearPose.lua` (**neu**) | OBERFLAECHE | Anim-Treiber Sitzen (5.6) |
| `lua/client/BanditsNPCBearTags.lua` (**neu**) | OBERFLAECHE | Namensschild je Baer (2.9) |
| `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `U.EN` (+ alle neuen Schluessel, wortgleich EN), `U.WhyText(..., bd)` |
| `lua/client/BanditsNPCBearMenu.lua` | OBERFLAECHE | "Bear window" (3.3), `holdWanted`/`addHold` (4a), `modeOf` fuer 4 Modi (Umschalter: bei follow "Stay here", sonst "Follow me") |
| `lua/client/BanditsNPCBearOptions.lua` | OBERFLAECHE | `WinSize` (1.7) |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | Zeile 2: `Tag_Sit`/`Tag_Roam`; `U.TagOn`; `B.OnView` ruft zusaetzlich `U.WinOnView` und `U.PoseOnView` (je hinter Riegel) |
| `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | 7.8 -- wird nie kopiert |
| `lua/shared/Translate/<L>/UI.json` x 7, `.../Sandbox.json` x 7, `sandbox-options.txt` | OBERFLAECHE | 7.6, 6.2 |
| `ober_werkzeug/texte_f1.py` (**neu**), `attrappe/f1_ober/` (**neu**: `run.lua`, `texte_pruefen_f1.py`) | OBERFLAECHE | 8.2 |
| `staging_dateien.txt`, `attrappe/gesamt/` ("21 F1", `xref_f1.py`), `baer/tools/baer_uebernahme.py`, `baer/NAEHTE.md`, `mod_info_vorschlag.txt` | ZUSAMMENBAU | 11 |
Unveraendert: `BanditsNPCBearDefs.lua`, `...Stats.lua`, `...Food.lua`, `...Crew.lua`, alle `TimedActions/`, `ISUI/BanditsNPCBearMap.lua`,
`ISUI/BanditsNPCBearMarker.lua`, `ISUI/BanditsNPCBearNameBox.lua`, `IG_UI.json`, Bilder, Modelle, AnimSets.
Ladefolge: Client-Dateien rufen sich nur zur Laufzeit ueber `U.*` (nie auf Dateiebene); `BanditsNPCBearKey.lua` legt die Tasten-Zeile auf Dateiebene an
(muss VOR Vanillas `loadKeys` laufen -- Mod-Dateien laden vorher, NC-Lehre `NC:client/ISUI/BanditsNPCBeaconWindow.lua:166-172`). Lua LF, ASCII; kein
`next(`, kein `%a`; keine Namen/Texte mit spawn/debug/test/bench/cheat ausser in der Bench (auch keine Bezeichner mit "Test"/"test" -- Regel
`CHEAT_NAME` des Uebernahme-Skripts); Klassen nur `local` (keine globale Funktion/Zuweisung); `ISButton:new`-Titel nie als fester Text (nur `""` oder
`U.T(...)`); localcount < 180.

### 7.2 KERN: neue Funktionen
| Funktion | Datei | Parameter | Rueckgabe | Bemerkung |
|---|---|---|---|---|
| `B.ModeOf(rec)` | Rules | Register- oder Sicht-Eintrag | "follow"/"stay"/"sit"/"roam" | unbekannt/nil -> "stay"; auch Client |
| `B.OrderDecide(c, env)` | Rules | c = { mode, st, x, y, hx, hy, r, gap, ownBusy, pauseOver }; env wie `B.Decide` (lure, mate) | { act, tx, ty, walk, lead, rule } | act: "hold" / "back" / "stroll" / "keep" / "come"; Regeln: S1 sit: weiter als stayBack -> back, sonst hold; S2 stay: Regel 6 (come, lead) / 7 (hold) / weiter als stayBack -> back / hold; S3 roam: 7 (hold) / weiter als r -> back / ownBusy -> keep / nicht pauseOver -> hold / stroll. back.walk = Abstand <= backRunDist |
| `B.OrderStep(rec, a, env, ms, players)` | Order | | true = erledigt | nur tame und mode stay/sit/roam; fuehrt `B.OrderDecide` aus (`B.Hold`, `B.MoveTo`, `B.RoamSpot`); Sitz-Ruhe (`s.sat`) + Touch; Roam-Pause |
| `B.StandStep(rec, a, ms)` | Order | | true = haelt (Aufstehen laeuft) | `s.standUntil > ms` (Uhr rueckwaerts = abgelaufen) -> `B.Hold`, true |
| `B.ComeCheck(rec, env, ms, players)` | Order | | true = SetMode lief | 2.5 Nr. 3; ohne `s.come` sofort false |
| `B.HandleCome(player, args)` | Order | { id } | - | 2.5 Nr. 2 |
| `B.HandlePassive(player, args)` | Order | { id, on } | - | 2.6 |
| `B.ReviveMissing(missing, players, ms)` | Order | Liste aus `resolve` | Zahl erzeugter Koerper (0/1) | 4b |
| `B.RoamSpot(rec, a, r)` | World | | Kachel oder nil | 5.5 |
Geaendert: `B.SetMode(rec, mode, why, players)` -- mode in `B.MODES`; why += "come" (`Note_Coming`), "came" (`Note_Came`), "comefail"
(`Note_ComeFail`), bei "ask": follow `Note_Follow`, stay `Note_Stay`, sit `Note_Sit`, roam `Note_Roam` (t "num", v Radius); stay/sit/roam setzen die
Heimat; immer `s.come = nil`, `s.roam = nil`; Wechsel weg von "sit" mit `s.sat` -> `s.standUntil`; alle Noten ueber `B.NoteBd`.

### 7.3 Befehle (Modul `BanditsNPCBear`, Client -> Schreiber)
`Mode { id, mode }` (mode: follow/stay/sit/roam), `Come { id }`, `Passive { id, on }`, dazu unveraendert `Rename`, `Call`, `Hello`, `BaitDrop`.

### 7.4 Meldungen (KERN schickt `{ k, t, v, tone, bd }`, OBERFLAECHE zeigt)
Neu: `Note_Sit` (good), `Note_Roam` (t "num", v Radius), `Note_Coming` (good), `Note_Came` (good), `Note_ComeFail` (bad), `Note_PassiveOn`,
`Note_PassiveOff`, `Why_OutOfReach` (bad). Jede mit Big-Fassung; `bd` ueber `B.NoteBd`.

### 7.5 OBERFLAECHE: Funktionen (nur unter `U`; an `B` nichts Neues ausser `B.OnView` wie heute)
| Funktion | Datei | Rueckgabe | Bemerkung |
|---|---|---|---|
| `U.WinBears()` | WinData | Liste eigener Sicht-Eintraege (tame/missing, owner == me.key bzw. SP-Schluessel), nach `id` sortiert | rein |
| `U.WinModel(v, player, nowMs)` | WinData | Tabelle: name, sub, next, chip { key, text, r, g, b }, dist, footer, hp/sta { now, max, frac } oder nil, carry, skills[6] { name, lv, pct, frac, tip }, buttons[key] = { label, state = "normal"/"active"/"off", tip }, toggles { pas, tag }, ordersInfo | alle Texte fertig; nur hier `U.T` |
| `U.WinFonts(f)` | WinParts | fName, fBody, fSmall, hName, hBody, hSmall | Regel 1.2 |
| `U.WinColor(key)` / `U.WinRamp(kind, v)` | WinParts | r, g, b, a / r, g, b | 1.3 |
| `U.WinBtn`, `U.WinRow`, `U.WinTick` (Klassen) | WinParts | Klassen-Tabellen (lokal abgeleitet, ueber U erreichbar) | `ISButton:derive`, eigene prerender/render, `ISButton.updateTooltip(self)` |
| `U.WinOpen(player, id)` / `U.WinClose()` / `U.WinToggle(player)` / `U.WinIsOpen()` | Window | - / - / - / boolean | 1.8 |
| `U.WinOnView()` | Window | - | merkt "neu bauen" |
| `U.WinLayout()` | Window | - | f, Schrift, Masse, Kinder neu legen |
| `U.PoseTick()` / `U.PoseOnView()` | Pose | - | 5.6 |
| `U.TagOn(c)` / `U.TagSet(c, on)` / `U.TagLoad()` | Tags | boolean / - / - | 2.9; ohne `c.u` -> immer an |
| `U.WhyText(whyKey, whyVal, bd)` | Client | Text | + bd (4a) |
Was die OBERFLAECHE vom KERN ruft: `B.View`, `B.ViewOf`, `B.BodyKind`, `B.ModeOf`, `B.SkillProgress`, `B.SKILLS`, `B.Opt`, `B.DirOf`, `B.DistXY`,
`B.Ask`, `B.ACT`, `B.CFG` (lesen, mit eigenem Rueckfall), `B.T`, `B.IsSP`, `B.PlayerKey`, `B.Log`/`B.ErrEvery`; Bench (nur SP) zusaetzlich `B.Reg`,
`B._s`, `B.FindAnimal`, `B.RemoveCub`, `B.BrainTick`.

### 7.6 Texte (OBERFLAECHE, alle sieben Sprachen; sortiert, Round-Trip `json.dumps(indent=4, ensure_ascii=False) + "\n"`, UTF-8 ohne BOM, LF, CN nur
Vanilla-CN-Zeichen, `U.EN` wortgleich mit EN, Platzhalter je Big gleich dem Grundschluessel, kein `<`/`>`, `%%` fuer Prozent)
EN-Vorschlag (Praefix `UI_BN_Bear_` weggelassen):
- Kopf/Zustand: `Win_BodyCub` "Bear cub", `Win_BodyBig` "Bear", `Win_Sub` "%1 - day %2", `Win_Next` "%1 in %2 day(s)", `Win_Grown` "full-grown",
  `Win_St_Follow` "Following you", `Win_St_Stay` "Staying", `Win_St_Sit` "Sitting", `Win_St_Roam` "Roaming", `Win_St_Come` "Coming to you",
  `Win_St_Hide` "Hiding", `Win_St_Ride` "Riding with you", `Win_St_Missing` "Missing", `Win_St_Away` "Out of reach", `Win_Here` "right next to you",
  `Win_Dist` "%1 tiles to the %2", `Win_LastSeen` "last seen %1 tiles to the %2", `Win_Count` "%1 / %2", `Win_Rename` "Rename".
- Karten: `Win_Cond` "Condition", `Win_Skills` "Skills", `Win_Orders` "Orders", `Win_Health` "Health", `Win_Stamina` "Stamina", `Win_Carry` "Can carry",
  `Win_CarryVal` "up to %1", `Win_None` "--", `Win_Later` "Coming later:", `Win_Hunger` "Hunger", `Win_Thirst` "Thirst", `Win_Tired` "Tiredness",
  `Win_Trust` "Trust", `Win_HealthTip`, `Win_StaminaTip`, `Win_CarryTip`, `Win_LaterTip` (Saetze 1.5).
- Faehigkeiten: `Win_Sk_Agi` "Agility", `Win_Sk_Vit` "Toughness", `Win_Sk_Con` "Endurance", `Win_Sk_Fgt` "Fighting", `Win_Sk_Fsh` "Fishing",
  `Win_Sk_Nos` "Keen nose", `Win_Lv` "Lv %1", `Win_Pct` "%1%%", `Win_Max` "max", `Win_SkHead` "%1 - level %2", `Win_SkProg` "%1 of %2 to level %3",
  `Win_SkTop` "Level 10 - the highest level.", `Win_SkTip_Agi` "A hit misses your bear completely: %1%% now, %2%% at level 10.",
  `Win_SkFrom_Agi` "Grows with every hit your bear takes.", `Win_SkTip_Vit` "Adds +%1%% health on top of the daily growth.",
  `Win_SkFrom_Vit` "Grows with every hit your bear takes.", `Win_SkTip_Con` "Bigger stamina bar (+%1%%) and faster rest.",
  `Win_SkFrom_Con` "Grows when your bear runs and gets out of breath.", `Win_SkTip_Fgt` "+%1%% damage now, +%2%% at level 10, on top of the daily growth.",
  `Win_SkFrom_Fgt` "Grows with every hit your bear lands.", `Win_SkTip_Fsh` "Catch chance %1%% (from half-grown; clumsy at first, much better later).",
  `Win_SkFrom_Fsh` "Grows while your bear fishes.", `Win_SkTip_Nos` "Smells zombies earlier and warns you with a growl: %1 tiles.",
  `Win_SkFrom_Nos` "Grows when it sniffs out zombies.", `Win_LaterFight` "Works once bears fight - comes later.",
  `Win_LaterFish` "Fishing comes later.", `Win_LaterNose` "Comes later and can be switched off.".
- Knoepfe: `Win_Follow` "Follow", `Win_Stay` "Stay", `Win_Sit` "Sit", `Win_Roam` "Roam free", `Win_Come` "Come here", `Win_Unstuck` "Unstuck",
  `Win_UnstuckWait` "Unstuck  %1", `Win_Passive` "Passive", `Win_Tag` "Name tag", `Win_StayTip` "It stays right at this spot and waits.",
  `Win_SitTip` "It sits down right here and stays sitting until you give another order.",
  `Win_RoamTip` "It strolls around freely, but never further than %1 tiles from this spot.",
  `Win_ComeTip` "It walks over to you and waits there. If it is stuck, use Unstuck.",
  `Win_PassiveTip` "Your bear stays out of fights and keeps to its order or comes back to you. No effect yet: fighting comes with a later version. A cub never fights anyway.",
  `Win_TagTip` "Shows the name above this bear - only on your screen.", `Win_TagOffAll` "All name tags are switched off in Options - Mods.",
  `Win_RoamInfo` "Roams within %1 tiles", `Win_Active` "This is its current order.".
- Fusszeile/Hinweise: `Win_Hint` "Drag to move.  V or Esc closes.", `Win_HintMissing`, `Win_HintRide`, `Win_HintAway` (1.4), `Win_NoBear`
  "You do not have a bear yet.", `Win_NoData` "The bear window is still loading. Try again in a moment.".
- Menue/Optionen/Schild: `Menu_Window` "Bear window", `Menu_WindowTip` "Also opens with a key - Options, Key bindings, NPC Crew: Bear.",
  `MO_WinSize` "Size of the bear window", `MO_WinSizeTip` "Auto grows with the screen height (1080p = 100%%, 4K = 200%%).", `Tag_Sit` "sitting",
  `Tag_Roam` "roaming".
- Meldungen (KERN) + Big: `Note_Sit` "Your cub sits down." / "Your bear sits down.", `Note_Roam` "Your cub roams around here (up to %1 tiles)." /
  bear, `Note_Coming` "Your cub is coming to you." / bear, `Note_Came` "Your cub is with you and waits here." / bear, `Note_ComeFail` "Your cub could
  not get to you. It waits where it is." / bear, `Note_PassiveOn` "Your cub is passive now: it stays out of fights." / bear, `Note_PassiveOff` "Your
  cub is no longer passive." / bear, `Why_OutOfReach` "Your cub is out of reach. Use Unstuck." / bear.
- B1e-Reste (4a): `Why_GoneBig`, `Note_DeadBig`, `Menu_HoldBig`, `Menu_HoldTipBig`.
- **Ausserhalb `UI_BN_Bear_`** (Vanilla liest sie selbst): `UI_optionscreen_binding_NPC Crew Bear` "NPC Crew: Bear",
  `UI_optionscreen_binding_Bear window` "Bear window" (Uebernahme-Ausnahme, 11).
- `Sandbox.json`: `Sandbox_BanditsNPC_BearRoamRadius`, `..._tooltip` (6.2).
Uebersetzungen schreibt `ober_werkzeug/texte_f1.py` (Muster `texte_b1e.py`); Woerter spawn/debug/bench/cheat/test nie.

### 7.7 Klassen-Gerippe (OBERFLAECHE, Form verbindlich)
```
-- WinParts.lua
local Btn = ISButton:derive("BanditsNPCBearWinBtn")          -- V:client/ISUI/ISResizeableButton.lua:1
function Btn:prerender()  -- eigener Hintergrund/Rand nach state + mouseOver + pressed; ZULETZT ISButton.updateTooltip(self) (ISButton.lua:176, :316)
function Btn:render()     -- Titel zentriert in eigener Farbe (drawTextCentre), aktive Leiste
-- Btn.state = "normal" | "active" | "off"; Btn.enable = (state ~= "off") -- ISButton:onMouseUp klickt nur bei enable (ISButton.lua:45)
local Row = ISButton:derive("BanditsNPCBearWinRow")          -- Zeile mit Tooltip, onclick = nil (ISButton.lua:42-44), zeichnet Wert/Balken/Segmente
local Tick = ISButton:derive("BanditsNPCBearWinTick")        -- Schalter: Kaestchen + Text, onclick schaltet
-- Window.lua
local Win = ISPanel:derive("BanditsNPCBearWindow")           -- V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1
function Win:new(x, y, w, h)  local o = ISPanel:new(x, y, w, h); setmetatable(o, self); self.__index = self
    o.moveWithMouse = true; o:setWantKeyEvents(true); ... return o end      -- ISAdminTicketsUI.lua:243-253; ISHandcraftWindow.lua:386
function Win:prerender()  -- Hintergrund, Rahmen, Akzent, Kopf, Karten (nur fertige Felder), dann ISPanel nicht noetig
function Win:isKeyConsumed(key) / Win:onKeyRelease(key) / Win:SaveLayout(name, layout) / Win:RestoreLayout(name, layout)
```

### 7.8 Bench (`client/NCBearBenchCub.lua`, nur SP wie die anderen, "singleplayer only")
- `NCBear_CubWin()` -- oeffnet das Fenster des eigenen Baeren (`U.WinOpen(getSpecificPlayer(0))`).
- `NCBear_CubBodyGone()` -- Koerper des eigenen Baeren weg, Eintrag bleibt (`B.RemoveCub(B.FindAnimal(rec))`, `s.obj = nil`) -> C1 testen.
- `NCBear_CubView()` -- druckt den eigenen Sicht-Eintrag (mode, pas, ld, hide, sit, cm, busy, u, x*, carry, dodge ...).
- `NCBear_CubStats()` druckt zusaetzlich mode, passive, s.sat, s.standUntil, s.roam, s.come, s.revN.
Schnell-C1: `NCBear_CubSet("reviveScans", 0)` (vorhandener Stellwert-Befehl).

---

## 8. Tests

### 8.1 KERN-Attrappe (`attrappe/f1_kern/run.lua`, neu; `kern/`, `b1b_kern/` ... `b1e_kern/`, `gesamt/` bleiben gruen -- gewollte Aenderungen einzeln
begruendet: Bleiben haelt statt "free", `missing` schliesst nicht mehr, GrowView auch fuer missing)
1. **ModeOf:** nil/"x"/"stay"/"sit"/"roam"/"follow" -> stay/stay/stay/sit/roam/follow; `InitRegistry` mit mode "dance" -> nil + Fehlerzeile; passive
   "yes" -> nil.
2. **Mode SP:** Besitzer, geladen: je sit/roam/stay -> rec.mode, Heimat = Kachel, Meldung (k, bd), Sicht `mode`; fremder Spieler -> Why_NotOwner;
   ride -> Why_Riding(+bd); nicht geladen -> Why_OutOfReach; missing -> Why_Gone(+bd).
3. **Mode MP-Rundlauf:** Server + Client A (Besitzer) + Client B: A `sendClientCommand("Mode", {id, "sit"})` -> Server setzt, Sichten A und B tragen
   `mode sit`; B schickt "Mode" -> Why_NotOwner an B, nichts geaendert; leere Tabelle -> still.
4. **Bleiben:** Tier 5 Kacheln weg -> MoveTo walk zur Heimat; in 1 Kachel -> Hold je Takt, nie "free"; Futter hinhalten -> Regel 6 (Heimat wandert).
5. **Sitz:** nach Befehl hold; nach 800 ms an der Stelle `s.sat` -> Touch -> Sicht `sit = true` (genau eine Sicht mehr); Laerm-Versatz 4 Kacheln ->
   `sat` nil + Touch, zurueck, wieder sat; Wechsel auf follow -> `standUntil = ms + 2300`, `B.StandStep` haelt 2,3 s, Zombie (GuardStep) trotzdem vorher.
6. **Frei:** R 12 (Sandbox), 200 Takte mit Zufall: jedes Ziel <= 12 vom Mittelpunkt, >= 3 vom Tier, Raum gleich (Attrappe: Mittelpunkt draussen,
   Kacheln mit Raum werden nie gewaehlt); Pausen 8..20 s mit Hold; Tier bei 15 -> zurueck gehend; Futter zieht den Mittelpunkt nie.
7. **Komm her:** geladen, 10 Kacheln -> mode follow + `s.come` + Note_Coming; Besitzer bei 2,5 -> stay "came", Heimat dort, `s.come` nil; 31 s ohne
   Ankunft -> stay "comefail"; zu weit (45) -> Why_Far; im Fahrzeug -> Why_InCar; nicht geladen -> Why_OutOfReach; aus "sit" -> zuerst StandStep.
8. **Passiv:** on true -> rec.passive true, Spiegel `passive`, Sicht `pas`; on false -> nil; on "true" (Text) -> still verworfen; missing-Besitzer geht;
   Restore/TakeNewerMark uebernehmen es; Drossel 500 ms.
9. **Unstuck/Call unveraendert:** missing -> neuer Koerper neben dem Spieler, ein Koerper, Abklingzeit; 2. Call -> Why_CallWait(+bd).
10. **C1:** Koerper weg (gen N) -> 3 Suchlaeufe -> missing + Note_Missing -> 2 weitere Suchlaeufe -> GENAU EIN `addAnimal`, gen N+1, st tame, Note_Back,
    Spiegel gen N+1; alter Koerper taucht danach auf (Spiegel gen N) -> "stale", nie gebunden, unbeobachtet entfernt; Gegend nicht geladen -> kein
    Versuch; Besitzer offline -> kein Versuch; keine freie Kachel -> kein Koerper, Fehlerzeile ab 3, kein Absturz; zwei Vermisste -> je Takt hoechstens
    einer; ride -> nie; der alte Koerper geladen-aber-ungebunden -> der Suchlauf bindet ihn VORHER, kein neuer.
11. **Nie verloren:** missing 48 Spielstunden mit Besitzer online -> Eintrag bleibt (missH steigt, kein Close); "fed" fehlt -> Close "lost" wie B1a.
12. **Sicht:** Felder 5.3 vorhanden/fehlend je Lage; `ld` faellt beim Entladen -> genau ein Touch; `hide` an/aus -> je ein Touch; `busy` (FeedAction
    serverStart/complete) -> Touch; GrowView fuer missing mit `x*`, `carry`, `dodge`, `fgtB`, `fish`, `nose`; Gleitkomma gerundet.
13. **Noten bd:** alle neuen + Why_Gone (Follow :223/:237, Ride :365) + Note_Dead (Registry :492) tragen `bd = "big"` nur beim grossen Koerper.
14. **Tausch waehrend Sitz/Frei:** neuer Koerper, `s.sat`/`s.roam` geleert, Modus bleibt, setzt sich wieder.
15. **Speichern/Laden:** sit/roam/passive bleiben (Register und, nach Register-Verlust, Spiegel-Heilung); `s.come` weg -> follow.
16. **Dateien:** `B.CreateCub(` weiter nur aus `B.AppearFor`/`B.PlaceCub`; `B.PlaceCub(` neu auch aus `B.ReviveMissing` (keine Tier-Regel betrifft es);
    `pathToLocation`/`animalRunning` nur in `B.MoveTo`; kein `next(`, kein `%a`, LF, ASCII; localcount.

### 8.2 OBERFLAECHE-Attrappe (`attrappe/f1_ober/run.lua`, neu; eigene Kern-Attrappe nach 7.2-7.4; `ober/`, `b1b_ober/` ... `b1e_ober/` bleiben gruen)
1. **Schriftwahl:** Hoehen (1x 19/29/33, 2x 26/33/40, 4x 38/45/50): f 1/1x -> Medium/Small/Small; f 2/2x -> Large/Medium/Small; f 2/1x ->
   Large/Medium/Medium; f 1/4x -> Small/Small/Small.
2. **Masse:** `U.WinLayout` bei 1080/1x -> 640 x 615 (+-2), bei 2054/2x -> 1280 x 1178 (+-2) (dieselben Zahlen wie `zeichne_fenster.py`); langer
   RU-Knopftext -> bw waechst; H > 0,92 x Bild -> f eine Stufe kleiner.
3. **Modell:** Junges Tag 12 -> sub "Bear cub - day 12", next "half-grown in 3 day(s)", hp "118 / 128", Faehigkeit con Stufe 2 / 54 % (Sicht x
   290); grosser Baer `bd big` -> "Bear - day 60"; missing -> Chip Missing, alle Befehle grau mit Why_OutOfReach(+bd), Unstuck frei; ride -> grau
   Why_Riding, Unstuck grau; `ld` fehlt -> Chip Away, Unstuck frei; im Fahrzeug -> Follow/Come/Unstuck grau Why_InCar; callWait 192 -> "Unstuck  3:12",
   grau, Tooltip Why_CallWait "4 min"; aktiver Knopf = mode; `cm` -> Come aktiv; hp fehlt -> "--" ohne Balken.
4. **Farbverlauf:** Leben 0,9 gruen, 0,45 Mischung, 0,1 rot-gelb; Ausdauer 0,6 blau, 0,1 orange-blau.
5. **Taste:** `keyBinding` bekommt Kopf + Zeile genau einmal (zweites Laden der Datei / NPC-Crew-Kopie -> kein Doppel); `isKey("Bear window")` und
   ISChat.focused -> nichts; NC-Attrappe mit FindTarget-Treffer -> nichts; Fahrzeug -> nichts; fremde Kuh (nicht wild) -> nichts; eigener Baer ->
   Fenster auf + Radial `undisplay`; kein Baer -> HaloText Win_NoBear; Sicht nicht frisch -> AskHello + Win_NoData; offen + V -> zu (onKeyRelease),
   gleiches Loslassen oeffnet nicht wieder (winClosedAt).
6. **Klicks:** Follow/Stay/Sit/Roam -> `B.Ask("Mode", { id, mode })`; Come -> "Come"; Passive -> "Passive" mit `on = not pas`; Unstuck -> "Call";
   Rename -> `U.AskName`; grauer Knopf -> kein Ask; nie leere Tabelle.
7. **Lage:** SaveLayout schreibt nur x, y (kein visible); RestoreLayout klemmt (-500, 9000) aufs Bild; OnResolutionChange -> neu.
8. **Takt/Kosten:** offen: Modell nur bei OnView oder je 1 s neu (Zaehler `U.T`-Aufrufe je Bild = 0); geschlossen: kein Bau, kein Zeichnen.
9. **Pose:** Sicht sit -> setVariable "sitdown", nach 1,7 s "sit"; sit weg -> "standup", nach 1,4 s clearVariable; busy -> keine Schreibzugriffe, danach
   neu "sitdown"; neue Kopie -> neu; kein `getVariableString`-Aufruf; Deckel P <= Sicht.
10. **Tags:** an (Vorgabe); aus -> Datei "tagoff <u>"; neu laden -> aus; 65 Baeren -> 64 Zeilen; `c.u` fehlt -> an; Hud zeigt bei aus keine Name-Zeile,
    Werte-Zeilen bleiben.
11. **Menue:** "Bear window" nur am eigenen zahmen Baeren; Hold-Texte mit bd big -> "...for the bear"; `U.WhyText` mit bd.
12. **Texte-Pruefer:** alle neuen Schluessel in 7 Sprachen, Platzhalter gleich, Big je Grundschluessel, CN-Zeichen, Round-Trip, `U.EN` == EN, kein `<`/`>`,
    die zwei Binding-Schluessel in allen 7, Sandbox 2 Schluessel x 7, `sandbox-options.txt` = `B.OPTS`.
13. **Bench:** `NCBear_CubWin`, `NCBear_CubBodyGone`, `NCBear_CubView`; MP -> "singleplayer only".

### 8.3 GESAMT (`attrappe/gesamt/run.lua` Abschnitt "21 F1", ZUSAMMENBAU)
SP: zaehmen -> V -> Fenster -> Sit (Sicht sit, Pose sitdown/sit) -> Follow (Aufstehen) -> Roam 200 Takte im Kreis -> Come -> Passive -> Name tag ->
Unstuck -> Tag 15 Tausch (sitzt wieder) -> BodyGone -> C1 (ein Koerper) -> Speichern/Laden (Modus, passive, Tag, Lage) -> Tod -> Fenster zu.
MP: dedizierter Server + A + B: A sit -> B sieht sit; B V -> Win_NoBear; A Unstuck; C1 am Server; kein `sendClientCommand` ausser Mode/Come/Passive/Call/
Rename/Hello. `xref_f1.py`: jede `B.*`/`U.*`-Benutzung definiert, Sicht-Felder 5.3, alle Schluessel aus Lua in EN.

### 8.4 Kevins Test im Spiel (nach dem Einbau: Spiel NEU starten; `bugwatch.py` mitlaufen lassen; Wegwerf-Spielstand, `-debug`; Debug-"Tier Cheat" AUS;
`NCBear_CubLog(true)`)
Einzelspieler:
1. Optionen -> Tastaturbelegung: Abschnitt "NPC Crew: Bear", Zeile "Bear window" = V.
2. Spielstand mit gezaehmtem Baeren (sonst `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`). Frei stehen (kein Auto, keine Kuh), V:
   Fenster geht auf. **Bei 4K: gross genug? Schoen?** Ziehen, mit V, Esc und X schliessen, wieder oeffnen: gleiche Stelle. Rechtsklick am Baeren ->
   "Bear window". `NCBear_CubWin()` geht auch.
3. Maus ueber Leben, Ausdauer und jede Faehigkeit: Tooltips lesen ("kommt spaeter" ehrlich?).
4. Befehle: **Sit** (setzt sich, bleibt sitzen, du gehst 10 Kacheln weg: sitzt weiter), **Stay** (steht still an der Stelle), **Roam free** (bummelt
   gemuetlich, nie weiter als 12 Kacheln), **Follow**, **Come here** aus 15 Kacheln (laeuft zu dir und wartet), **Unstuck** (steht neben dir, Knopf
   5 min grau mit Restzeit). Der aktive Knopf leuchtet Honig-Orange.
5. Passive an -> Meldung; Name tag aus -> Name ueber dem Baeren weg (Leben-Balken bleibt); speichern, Hauptmenue, laden: beides gemerkt, Fenster
   nicht von selbst offen, Lage gemerkt.
6. Ins Auto: Follow/Come/Unstuck grau "Not while you are in a vehicle". Mitfahren: Chip "Riding with you". (Im Auto gehoert V dem Fahrzeug-Radial.)
7. `NCBear_CubBodyGone()`: nach ~15 s "You have lost track of your bear.", Fenster zeigt "Missing", Unstuck geht; ohne Klick nach ~1 min "Your bear is
   back." an der alten Stelle, nur EIN Baer.
8. `NCBear_CubGrow(48)` (Tag 60): Fenster "Bear - day 60", Sitz mit dem grossen Baeren.
9. Mit NPC Crew: V vor einer Crew-Figur -> das NPC-Gespraech, nicht das Baeren-Fenster. V neben einer Kuh -> Vanillas Tier-Radial, kein Baeren-Fenster.
   V neben dem eigenen Baeren -> Baeren-Fenster (das Tier-Radial blitzt hoechstens kurz).
Mehrspieler (dedizierter Server, Rolle user, A und B): 1. Server startet ohne Fehler, kein Kick. 2. A: Fenster, Sit -> B sieht ihn sitzen. 3. B: V ->
"You do not have a bear yet."; B kann A's Baeren nicht befehligen. 4. A Unstuck, Passive; Server neu starten -> passive noch an. 5. Server-Log nach
`[TC-BEAR] ***` durchsehen.

---

## 9. Belege: jeder geplante Engine-Aufruf (der Bauer liest die Stelle selbst nach und nennt sie im Kommentar)
| Nr | Aufruf | Beleg (gleiche Argumenttypen) | Seite | Wer |
|---|---|---|---|---|
| 1 | `table.insert(keyBinding, { value = T })`, `{ value = T, key = Keyboard.KEY_V }` | `V:shared/keyBinding.lua:6-14`, `:131`; NC gespielt `client/BanditsNPCInteract.lua:7451`, `:7462` | C | OBER |
| 2 | `Events.OnKeyPressed.Add(fn)`, `getCore():isKey(Text, key)` | `V:client/ISUI/FPS.lua:9`, `:21` | C | OBER |
| 3 | `getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU / ANIMAL_RADIAL_MENU, key)`, `ISVehicleMenu.getVehicleToInteractWith(p)`, `AnimalContextMenu.getAnimalToInteractWith(p)` | `V:client/ISUI/ISUIHandler.lua:36-43` | C | OBER |
| 4 | `animal:isWild()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171` | C | OBER |
| 5 | `getPlayerRadialMenu(0)`, `m:isReallyVisible()`, `m:undisplay()` | `ISUIHandler.lua:91-92`; `ISAnimalContextMenu.lua:1157-1164` | C | OBER |
| 6 | `ISChat.focused` (lesen) | `V:client/Chat/ISChat.lua:8` | C | OBER |
| 7 | `ISPanel:derive(T)`, `ISPanel:new(x, y, w, h)`, `o.moveWithMouse = true` | `V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1`, `:243`, `:253`; Ziehen `V:client/ISUI/ISPanel.lua:49-95` | C | OBER |
| 8 | `ISButton:derive(T)`, `X:new(...)` geerbt, `ISButton.onMouseDown(self, x, y)` | `V:client/ISUI/ISResizeableButton.lua:1`, `:15`; Aufrufer `V:client/ISUI/ISInventoryPane.lua:63` | C | OBER |
| 9 | `ISButton:new(x, y, w, h, "", target, fn)`, `:initialise()`, `parent:addChild(b)`, `b:setImage(tex)`, `b:forceImageSize(w, h)`, Felder `borderColor`/`backgroundColor` | `V:client/ISUI/ISCollapsableWindow.lua:55-61`; `V:client/ISUI/ISInventoryPage.lua:1479` | C | OBER |
| 10 | `b:setTooltip(text)`, `b.enable`, `ISButton.updateTooltip(self)` | `V:client/ISUI/ISButton.lua:445`, `:45`, `:176`, `:316-346`; Grund-Tooltip grau `V:client/ISUI/Hutch/ISHutchUI.lua:617-623` | C | OBER |
| 11 | `" <LINE> "` im Tooltip-Text | `V:client/ISUI/ISGarmentUI.lua:136` | C | OBER |
| 12 | `self:drawRect(x,y,w,h,a,r,g,b)`, `drawRectBorder`, `drawText`, `drawTextRight`, `drawTextCentre`, `drawTextureScaled(tex,x,y,w,h,a,r,g,b)` | `V:client/ISUI/ISUIElement.lua:1191-1198`, `:1219-1227`, `:1280`, `:1293`, `:1306`; `V:client/Chat/ISChat.lua:418` | C | OBER |
| 13 | `getTexture("media/ui/<datei>.png")` (eigene 288er, Scheibe; Vanilla `media/ui/inventoryPanes/Button_Close.png`) | `V:client/Chat/ISChat.lua:921`; `ISCollapsableWindow.lua:386` | C | OBER |
| 14 | `getTextManager():getFontHeight(UIFont.X)`, `MeasureStringX(UIFont.X, s)` | `V:client/ISUI/Animal/ISAnimalUI.lua:4-5`; `V:client/ISUI/ISButton.lua:450` | C | OBER |
| 15 | `getCore():getScreenWidth()/getScreenHeight()` | `V:client/Challenge/WinterIsComing.lua:18` | C | OBER |
| 16 | `addToUIManager()`, `removeFromUIManager()`, `setVisible(b)`, `bringToTop()`, `getIsVisible()`, `setX/setY/setWidth/setHeight` | `ISUIElement.lua:1365`, `:1373`, `:657`, `:1548`; `V:client/ISUI/ISToolTip.lua:78-79`, `:173-174` | C | OBER |
| 17 | `o:setWantKeyEvents(true)`, `X:isKeyConsumed(key)`, `X:onKeyRelease(key)`, `Keyboard.KEY_ESCAPE` | `V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-297`, `:386` | C | OBER |
| 18 | `ISLayoutManager.RegisterWindow(name, Klasse, obj)`; `layout.x/y` | `V:client/ISUI/ISLayoutManager.lua:6-13`, `:97-110`; `V:client/Chat/ISChat.lua:1172` | C | OBER |
| 19 | `getFileReader(name, true)`, `r:readLine()`, `r:close()`, `getFileWriter(name, true, false)`, `w:write(s)`, `w:close()`, `string.trim` | `V:client/ISUI/ISLayoutManager.lua:127-135`, `:172-186` | C | OBER |
| 20 | `Events.OnResolutionChange`, `OnGameStart`, `OnTick` | `V:client/ISUI/PlayerData/ISPlayerData.lua:206`; `V:client/Chat/ISChat.lua:1186`, `:943` | C | OBER |
| 21 | `HaloTextHelper.addText(p, t)`, `getSpecificPlayer(0)`, `p:isDead()`, `p:getVehicle()`, `p:getX()/getY()` | `V:client/Foraging/forageClient.lua:73`; `V:client/Farming/CFarmingSystem.lua:45`; `V:client/Context/ISMenuContextWorld.lua:37`; `V:client/ISUI/Hutch/ISHutchMenu.lua:8`; `V:client/Fishing/TensionUI.lua:11` | C | OBER |
| 22 | `animal:setVariable(Text, Text)`, `animal:clearVariable(Text)` (am Tier) | `V:shared/TimedActions/Animals/ISPetAnimal.lua:43`, `:48` | C | OBER (Pose) |
| 23 | `menu:addOption(text, p, fn, arg)` | `S:client/BanditsNPCBearMenu.lua:241` (wie heute) | C | OBER |
| 24 | `PZAPI.ModOptions` `addComboBox`/`addItem`/`getValue` | wie B1e (PB1E 8 Nr. 23) | C | OBER |
| 25 | `ZombRandFloat(a, b)`, `ZombRand(n)` | `S:server/BanditsNPCBearWorld.lua:175-179` (Form `B:server/BanditServerSpawner.lua:216-222`); `V:shared/TimedActions/Animals/ISMilkAnimal.lua:25` | S | KERN |
| 26 | `getCell():getGridSquare(x, y, z)`, `sq:getRoom()` | `V:server/Animal/ISPickDungCursor.lua:104`; `V:shared/Util/AdjacentFreeTileFinder.lua:240` | S | KERN |
| 27 | `animal:getBehavior():setBlockMovement(b)` (ueber `B.Hold`), `B.MoveTo` (darin `fleeTo`, `setVariable("animalRunning", false)`, `pathToLocation` -- Kevins Wort, unveraendert NUR dort) | wie B1c (`S:server/BanditsNPCBearWorld.lua:823-917`) | S | KERN |
| 28 | `isExistInTheWorld`, `getOnlineID`, `getModData`, `getX/getY` am Tier; `sendClientCommand`/`sendServerCommand` | wie B1a-B1e (unveraendert) | beide | KERN |
**Jar-only-Aufrufe in F1: keine.** **Nicht benutzt:** `getVariableString` am Tier (kein Vanilla-Beleg am Tier, 0.5), `ISCollapsableWindow`-Titelleiste,
`ISTickBox` (eigener Schalter aus `ISButton`), `drawTextZoomed`, `drawProgressBar`, `ISCharacterScreenAvatar` (F-f), `setWantMouseEvents` an der
Markierung (4d), `setDebugAcceptance`, `idleAction` (FF 4.2 Nr. 3).

---

## 10. Leistung
| Was | Wie oft | Deckel |
|---|---|---|
| Fenster zeichnen | nur offen; je Bild ~130 Zeichenaufrufe aus fertigen Feldern, kein `getText`, keine neue Tabelle | ein Fenster |
| Fenster-Modell | bei neuer Sicht oder je 1 s (nur offen) | 6 Faehigkeiten, 6 Knoepfe, 2 Schalter |
| Pose-Treiber | je 250 ms, je zahmem Eintrag der Sicht 1 Tabellen-Blick + hoechstens 2 `setVariable`/`clearVariable` beim Wechsel | `viewMax` 16 |
| Taste | nur beim Loslassen von "Bear window" | - |
| Schreiber Order-Takt | je Hirn-Takt und geladenem zahmem Baeren: Lua-Rechnung, 1 Hold oder MoveTo; RoamSpot hoechstens 8 Kachel-Fragen je neuem Ziel (alle 8-20 s) | Eintraege 64 |
| C1 | nur im Vermissten-Suchlauf (je 30 s), hoechstens 1 PlaceCub je Takt | ein Koerper je Eintrag |
| Sicht nachschicken | nur bei Wechsel (sat, hide, ld, busy) | wie B1c |
| Tags-Datei | lesen 1 x je Spielstart, schreiben je Klick | 64 Zeilen |

---

## 11. Fuer den ZUSAMMENBAU
1. Staging nachzaehlen (60 Dateien gegen Test-Mod 914ee79), dann `staging_dateien.txt` neu (6 neue Client-/ISUI-Dateien, 1 neue Server-Datei, geaenderte
   MD5; Bench als Testhilfe). Die drei Sitz-Knoten liegen schon in der Test-Mod (nicht ins Staging; unveraendert).
2. `attrappe/gesamt/run.lua` "21 F1" (8.3), beide Bauer-Attrappen gegen die echten Dateien, `xref_f1.py`; die Masse aus `f1_entwurf/zeichne_fenster.py`
   gegen `U.WinLayout` (8.2 Nr. 2) vergleichen.
3. `baer/tools/baer_uebernahme.py`:
   - `ANIMSET_OK` += `NCBear_SitDown.xml`, `NCBear_Sit.xml`, `NCBear_StandUp.xml` (Kampf-Knoten bleiben gesperrt); Pruefungen "genau eine Bedingung
     NCBearAct" und "Clip im GLB des Jungen" gelten mit (die Clips liegen im Junges-GLB, FF 4.1 -- im Trockenlauf nachweisen).
   - `CHEAT_ALLOWED` += genau drei Ausnahmen der Regel `taste`: `42/media/lua/client/BanditsNPCBearKey.lua` `Events.OnKeyPressed` und `Keyboard.KEY_V`,
     `42/media/lua/client/ISUI/BanditsNPCBearWindow.lua` `Keyboard.KEY_ESCAPE` -- je mit Grund "Baeren-Fenster auf Kevins Wunsch (ENT:259), Taste in
     Vanillas Belegung"; jede andere Taste/Maus bleibt ein Fund.
   - `TEXT_NS["UI.json"]` += die zwei exakten Schluessel `UI_optionscreen_binding_NPC Crew Bear`, `UI_optionscreen_binding_Bear window`; Kollisionsprobe
     gegen NPC Crews UI.json (heute 0 Treffer).
   - Neue Sandbox-Option `BearRoamRadius` laeuft ueber die vorhandene Naht 4 (Name frei, 0 Treffer am 11.11. nachts).
   - Trockenlauf mit `--vor-b5a`, Probe nur unter `_arbeit/baer_zaehmen/probe_f1/`.
4. `baer/NAEHTE.md` neue Zeilen: (27) Tasten-Zeile in Vanillas `keyBinding`, eigener Abschnitt "[NPC Crew Bear]" (in NPC Crew evtl. unter "[NPC Crew]",
   Frage F9), Name ewig stabil; (28) Vorfahrt V: liest `BanditsNPC.Interact.KEYBIND`/`FindTarget` (Existenz-Riegel, keine NC-Datei), Vanilla-Radiale;
   (29) `layout.ini`-Name `BanditsNPCBearWindow`, Client-Datei `BanditsNPCBear.ini`; (30) "Frei herumlaufen" in NPC Crew: Basisflaeche des Beacons
   (`BanditsNPC.Base.Zone`/`SiteNear`, NC `shared/BanditsNPCForestZones.lua:687-694`; am dedizierten Server fraglich -> Rueckfall Kreis) -- NUR
   dokumentiert; Zeile 9 (AnimSet): + drei Sitz-Knoten; Zeile 14 (Taste V): erledigt mit F1; Zeile 11: Befehle Come/Passive, Register `passive`,
   Spiegel `passive`, Sicht-Felder 5.3.
5. `mod_info_vorschlag.txt` um F1 (Baeren-Fenster auf V, Befehle Sitz/Frei/Komm her/Passiv/Unstuck, Namensschild je Baer, Baer kommt von selbst wieder).
6. Einbau in NCBearTest nur, wenn Kevin nicht spielt; vorher/nachher Zip; Kevin muss das Spiel NEU starten (Taste, neue Lua).

---

## 12. Fragen fuer Kevin (Nachtschicht -- gebaut wird die Empfehlung; morgens als Liste zeigen)
| # | Frage | gebaut (Empfehlung) |
|---|---|---|
| F1 | "Komm her" und "Unstuck" als zwei Knoepfe: Komm her = er LAEUFT zu dir und wartet (keine Abklingzeit); Unstuck = Call to me (versetzt, 5 min)? | ja, zwei Knoepfe |
| F2 | "Bleiben" = steht still an der Stelle; "Frei herumlaufen" = bummelt im Kreis, Vorgabe **12** Kacheln (Sandbox 4-30) statt 8 -- mit 8 rannte das Junge in B1b dauernd heim. Ok? | ja |
| F3 | Mittelpunkt von Frei/Bleiben/Sitz = wo der Baer beim Befehl steht (nicht wo du stehst)? | ja |
| F4 | V: das NPC-Gespraech (NPC Crew) geht vor, im/am Auto Vanillas Fahrzeug-Radial, an einer fremden Kuh Vanillas Tier-Radial; nur sonst das Baeren-Fenster. Im Auto also kein Fenster auf V. Ok? | ja |
| F5 | Am eigenen Baeren schliesst unser Fenster Vanillas Tier-Radial (darin steht "Toeten", wenn du eine Waffe traegst). Sollen wir das Radial am eigenen Baeren ganz unterdruecken (Vanilla-Funktion umwickeln)? | nein (nur schliessen) |
| F6 | Mehrere eigene Baeren (Sandbox bis 4): Pfeile "< 1/2 >" im Kopf, beim Oeffnen der naechste? | ja |
| F7 | Namensschild je Baer: gespeichert auf deinem Rechner (wie "was ich sehe"), die Option "Namensschilder" bleibt der Hauptschalter? | ja |
| F8 | Passiv beim Jungen zeigen (Tooltip: Jungtier kaempft nie, wirkt mit dem Kampf)? | ja |
| F9 | Tastenbelegung: eigener Abschnitt "NPC Crew: Bear" (in NPC Crew spaeter unter "NPC Crew"?) | eigener Abschnitt |
| F10 | Baer ohne Koerper: kommt ~1 Minute nach "lost track" von selbst an seiner Stelle wieder; und ein zahmer Baer wird NIE mehr nach 24 Spielstunden als verloren geloescht? | ja, beides |
| F11 | Fenster bleibt offen, egal wie weit der Baer weg ist (fuer Unstuck)? | ja |
| F12 | Fenstergroesse "Auto" = 200 % bei deinem 4K (1280 x 1180 px); Option "Size of the bear window" 100-300 %. Lage merkt sich das Spiel beim Speichern. | ja |
| F13 | Ein 3D-Bild des Baeren im Fenster (wie Vanillas Tier-Info)? Absturz-Risiko laut NPC-Crew-Lehre -> spaeter. | nein (Symbol) |
| F14 | Fuettern im Sitzen: er steht dafuer kurz auf und setzt sich danach wieder. Ok? | ja |
| F15 | Vertrauen/Hunger/Durst/Muedigkeit stehen als "Coming later" ohne Balken im Fenster (nichts Falsches). Ok? | ja |

---

## 13. Offen / ungeprueft (Testpunkte)
Alles Laufzeit-Verhalten. Besonders: ob `ISPanel` mit `moveWithMouse` und `ISButton`-Kindern sauber zieht und klickt; ob Esc mit `isKeyConsumed` das
Spielmenue NICHT oeffnet; ob ein V im Chat-Textfeld das offene Fenster schliesst (das Fenster will Tasten; Vanillas Handwerks-Fenster hat dieselbe
Lage); Vanillas Tier-Radial-Blitz am eigenen Baeren; Sitz-Clips am grossen Koerper und am Jungen nach dem laufenden Modell-Lauf baer-junges-fuss
(gleiche Clip-Namen, Laengen 1,6/4,0/1,3 s angenommen -- aendern sie sich, nur `SIT_DOWN_MS`/`STAND_UP_MS`/`standMs` nachziehen); `setVariable` an
der Client-Kopie im MP (ob ein Tierpaket sie ueberschreibt); Fussgleiten beim Bummeln (gehend); `layout.ini` im MP-Client; Tooltip-Schrift bei 4K;
lange Texte in RU/FR in den Knoepfen; `getAnimalID`/`getObjectListForLua` am MP-Server (A3, offen seit B1a).

Statisch geplant, nichts gebaut, nichts gespielt.
