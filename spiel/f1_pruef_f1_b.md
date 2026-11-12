# Lauf baer-f1: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung, Optik (F1 Baeren-Fenster)

Stand 12.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Pruefgegenstand: Staging `_arbeit/baer_zaehmen/mod/` (67 Dateien laut
`staging_dateien.txt`), Berichte `bau_f1_kern.md`, `bau_f1_oberflaeche.md`, `bau_f1_zusammenbau.md`, Plan `PLAN_F1.md`. Nichts im Staging,
in der Test-Mod, in NPC Crew, Vanilla oder Bandits geaendert; kein git, kein Spielstart. Geschrieben nur dieser Bericht und
`attrappe/pruef_f1/` (drei Attrappen + Ergebnisse, Jar-Auszuege `jar/KahluaUtil.txt`, `jar/BaseVehicle.txt` per javap).
Abkuerzungen: S = Staging `mod/42/media/lua/`, V = Vanilla `media/lua/`.

## 0. Ergebnis in Kurzform

- **Keine rote Linie im Register verletzt**: kein Weg erzeugt einen zweiten Eintrag oder schliesst einen zahmen Baeren; jeder Fenster-Befehl
  geht als Bitte an den Schreiber, der Besitz, Zustand und Lage prueft (S:server/BanditsNPCBearFollow.lua:259-297,
  S:server/BanditsNPCBearOrder.lua:253-315, S:server/BanditsNPCBearRide.lua:303-385). Ein Client kann keinen fremden Baeren steuern.
  Nichts haengt endlos (alle Wartezeiten mit Deckel: comeMaxMs, standMs, ownMaxMs, Roam-Pause, Layout-Schleife 8, Tags 64).
- **Aber sichtbare Doppel sind moeglich** (Register bleibt einfach, eine "stale"-Kopie steht ohne Schild herum, bis niemand naeher als
  25 Kacheln ist): **B1** C1 feuert zu frueh (Wartefrist zaehlt Suchlaeufe, nicht geladene Zeit), **B2** Vanillas Tier-Anhaenger + C1.
- **B3** Sitz-Treiber: nach Streicheln/Fuettern im Sitzen falscher Anim-Zustand -- im schlimmsten Fall setzt sich ein FOLGENDER Baer bei
  jedem Halt hin (bleibt so bis zum naechsten Sitz-Zyklus).
- Optik: das gebaute Fenster entspricht dem Entwurf (Bilder `f1_entwurf/fenster_gebaut_*.png` gegen `fenster_*.png`); bei 1080/1x, 4K/2x,
  4K/4x, 24-Zeichen-Namen und RU/FR keine Ueberlappung im Kopf, nichts abgeschnitten (Breite waechst mit `MeasureStringX`). Kleinigkeiten B6, B8.
- 3 major, 7 minor. Die Attrappen: `c1_wartefrist.lua` (2 Befunde), `sitz_treiber.lua` (3 Befunde), `kopf_lage.lua` (1 Grenzfall, 1 px).

## 1. Befunde

### B1 (major) C1 kommt zu frueh: die Wartefrist zaehlt Suchlaeufe, nicht Zeit in geladener Gegend
- `B.ReviveMissing` zaehlt `s.revN` nur hoch, wenn der Eintrag "eligible" ist, setzt ihn aber **nie zurueck, wenn er es nicht ist**
  (Gegend entladen, Besitzer offline) -- S:server/BanditsNPCBearOrder.lua:344-361. Zurueckgesetzt wird nur beim Wechsel tame -> missing
  (S:server/BanditsNPCBearServer.lua:862-864) und nach Erfolg.
- Folge 1: ein Suchlauf in geladener Gegend (revN 1), Kevin geht weg (Gegend entladen), kommt zurueck -> **der erste Suchlauf nach dem
  Neuladen erzeugt sofort den Koerper**. Genau dann hat der Tier-Lader (Worker-Faden `AnimalManagerMain.fromWorker`, forschung_engine.md 1.4,
  Dauer ungeprueft) den alten Koerper vielleicht noch nicht geliefert -> dieser kommt danach als "stale" (kleinere gen), wird nie gebunden und
  steht ohne Schild herum, bis niemand naeher als 25 Kacheln ist (Plan 4b Nr. 5). Dasselbe im MP nach Abmelden/Anmelden des Besitzers.
- Folge 2: der Suchlauf-Abstand haengt an ALLEN Eintraegen: gibt es irgendeinen zahmen/wilden Eintrag ohne Koerper in geladener Gegend
  (`need`), laeuft der Suchlauf je 5 s statt 30 s (S:server/BanditsNPCBearServer.lua:971-972) -> C1 nach **10 s** statt der geplanten ~60 s
  (PLAN_F1.md 4b Nr. 2). Typisch direkt nach dem Laden (alle Eintraege noch ungebunden) und im MP (fremde Junge).
- Beleg: Attrappe `attrappe/pruef_f1/c1_wartefrist.lua` laedt die echte Order.lua: A Sollfall 0/1 korrekt; **B** "nach dem ERSTEN Suchlauf
  nach dem Neuladen 1 Koerper (Soll 0)"; **C** "neuer Koerper 10000 ms nach missing" (`c1_wartefrist_ergebnis.txt`).
- Vorschlag (klein, nur Order.lua, kein Engine-Aufruf): (1) im Schleifenrumpf `if not eligible and s then s.revN, s.revAt = nil, nil end`
  (Wartefrist beginnt neu, sobald die Gegend nicht geladen / der Besitzer nicht da ist); (2) Frist zusaetzlich als Zeit:
  `s.revAt = s.revAt or ms` beim ersten eligible Suchlauf, PlaceCub erst bei `revN >= reviveScans` UND `ms - revAt >= reviveMs` (neuer
  Stellwert, z. B. 60000); (3) nicht im Heil-Fenster nach dem Laden (`ms < B._healUntil`, healWindowMs 120 s), dort lief bisher alles
  Laden-Heilen. Attrappe danach erneut laufen lassen (Soll: 0 Befunde).

### B2 (major) Vanillas Tier-Anhaenger + C1 = zweiter Baer (alte Luecke F7, durch C1 verschaerft)
- Jeder Spieler (im MP auch ein fremder) kann jedes Tier in 6 Kacheln um einen Tier-Anhaenger einladen, ohne Besitzfrage
  (V:client/Vehicles/ISUI/ISVehicleMenu.lua:777-800). Bedingung nur Platz: `canAddAnimalInTrailer` = Kapazitaet >= belegt +
  `animal:getAnimalTrailerSize()` (Jar 42.22.2, `attrappe/pruef_f1/jar/BaseVehicle.txt:37653-37667`), das ist `trailerBaseSize x Groesse`
  (dec/IsoAnimal.java:2794-2796). Junges 100 x Groesse, grosser Koerper 300 x 1,0..1,35 (S:shared/BanditsNPCBearDefs.lua:99, :185) --
  **beide passen** in Vanillas Viehanhaenger/Pferdeanhaenger (`animalTrailerSize = 500.0`, V:scripts/generated/vehicles/
  vehicle_trailer_livestock.txt:51, vehicle_trailer_horsebox.txt:51).
- Im Anhaenger ist der Koerper nicht in der Welt -> nach ~15 s "missing" -> C1 setzt nach 2 Suchlaeufen (B1: ggf. 10 s) einen NEUEN Koerper
  neben den Anhaenger. Wird der alte ausgeladen, ist er "stale" (kleinere gen) -> nie gebunden, zweiter Baer ohne Schild, Vanilla-KI.
  **Vor F1** kam der Baer beim Ausladen einfach zurueck (missing -> tame, gleicher Koerper); jetzt wird daraus ein Doppel.
- Vorschlag: `trailerBaseSize` beider Arten so gross setzen, dass `canAddAnimalInTrailer` nie wahr ist (z. B. 100000 -> Vanilla graut
  die Zeile "zu gross" aus, ISVehicleMenu.lua:796-800). Reine Daten-Aenderung in Defs.lua, kein neuer Aufruf; Kevins Regel "faehrt wie die
  NPC-Crew-Figuren mit" (ENTSCHEIDUNGEN.md:244) braucht den Anhaenger nicht. Vorher pruefen, ob `getAnimalTrailerSize` sonst noch etwas
  steuert (Jar-Suche, ungeprueft). **Frage fuer Kevin** (unten).

### B3 (major, Optik/Zustand) Sitz-Treiber verliert seinen Zustand bei "busy" und setzt "sit" nur beim Phasenwechsel
- `step` verwirft bei `v.busy` den Eintrag, ohne die Variable aufzuraeumen (S:client/BanditsNPCBearPose.lua:53-56), und beginnt danach nur
  neu, wenn `want` gilt (:58-59); in Phase "sit" wird nie wieder geschrieben (:67-73).
- (a) **Streicheln im Sitzen**: die Streichel-Aktion laesst NCBearAct unberuehrt (S:shared/TimedActions/BanditsNPCBearPetAction.lua:82-90),
  setzt aber busy (:90, :136) -> danach schreibt der Treiber "sitdown" -> der Hinsetz-Clip startet aus dem Sitzen (sichtbares Aufspringen),
  **bei jedem Streicheln**.
- (b) **Streicheln und waehrenddessen Follow/Stay/Roam** im Fenster (der Schreiber nimmt Mode auch waehrend busy an): "sit" bleibt am Tier,
  der Treiber schreibt nie wieder -> **der folgende Baer setzt sich bei jedem Halt hin**, bis zum naechsten Sitz-Zyklus oder Neuladen.
  Im MP bei jedem Client (busy steht in jeder Sicht).
- (c) **Fuettern im Sitzen, sofort abgebrochen**: start() setzt "eat", release() loescht NCBearAct
  (S:shared/TimedActions/BanditsNPCBearFeedAction.lua:62, :73); busy an+aus im selben Hirn-Takt -> die Sicht traegt busy nie
  (S:server/BanditsNPCBearGrow.lua:485-496) -> der Treiber steht in "sit", schreibt nie wieder -> **Baer steht, Fenster und Schild sagen
  "Sitting"**.
- Beleg: `attrappe/pruef_f1/sitz_treiber.lua` (echte Pose.lua): Fall 3 NCBearAct nil, Fall 5 "set NCBearAct=sitdown" nach dem Streicheln,
  Fall 6 NCBearAct "sit" nach Follow; Gegenprobe 4 (normales Fuettern mit busy) korrekt (`sitz_treiber_ergebnis.txt`).
- Vorschlag (nur Pose.lua, nur vorhandene Aufrufe setVariable/clearVariable): bei busy den Eintrag BEHALTEN und nur nicht schreiben; nach
  busy: will er sitzen -> Phase "sit" direkt (nicht "sitdown"), sonst "standup" wie beim normalen Aufstehen; dazu in Phase "sit" alle ~2 s
  `setVariable(act(), "sit")` nachsetzen (idempotent, 1 Aufruf je 2 s und Baer) -- heilt jeden fremden clearVariable. Attrappe danach gruen.

### B4 (minor) Z2 bestaetigt: "Sit"/"Stay" mitten im Folgen-Lauf rennt erst bis 3 Kacheln weiter
- `B.SetMode` loescht `s.ownUntil`/`s.tx` nicht (S:server/BanditsNPCBearFollow.lua:101-123); der Folgen-Lauf hat sie gesetzt
  (`B.MoveTo` S:server/BanditsNPCBearWorld.lua:945, :949, bis ownMaxMs 15 s); `B.OrderDecide` laesst ihn laufen (Regel 32 / 36,
  S:shared/BanditsNPCBearRules.lua:381, :395), bis er weiter als stayBack 3 von der Befehlsstelle ist, dann zurueck (Regel 31/35).
- Vorschlag (Empfehlung des Zusammenbaus, Frage Z2): in `B.SetMode` fuer `mode ~= "follow"` zusaetzlich `s.ownUntil, s.tx, s.ty = nil, nil,
  nil`; in `B.HandleMode` nach dem SetMode `B.Hold(rec, a, true)` (a ist dort gebunden, :279). Dann bleibt er sofort stehen bzw. geht
  den kurzen Rest zur Stelle zurueck.

### B5 (minor) Zwei Texte versprechen mehr als gebaut
- `UI_BN_Bear_Win_HintMissing` "It comes back soon, or use Unstuck." (S:client/BanditsNPCBearClient.lua:280): im MP erst, wenn der
  Suchlauf einen Baeren gesehen hat (S:server/BanditsNPCBearOrder.lua:341-349, A3 offen), nie bei `_aidSeen` (:351-357), im SP nur solange
  die Gegend geladen ist und der Besitzer da ist (:345). Vorschlag: "It can come back by itself while you are near its last spot. Unstuck
  brings it now."
- `UI_BN_Bear_Note_PassiveOn` "Your cub is passive now: it stays out of fights." (:301): wirkt erst mit B5a (der Tooltip :273 sagt es
  ehrlich, die Meldung nicht). Vorschlag: "...is passive now. It keeps out of fights once bears fight (comes later)." Beide in 7 Sprachen.

### B6 (minor, Optik) Unstuck: Knopf "3:12", Tooltip "about 4 min"
- Knopf zeigt `m:ss` (S:client/BanditsNPCBearWinData.lua:434), Tooltip `Why_CallWait` mit aufgerundeten Minuten (:429) -- im Bild
  `fenster_gebaut_1080.png` rechts direkt nebeneinander. Vorschlag: im Tooltip des grauen Unstuck-Knopfs nur den Satz ohne Zahl (oder
  "in %1" mit derselben m:ss-Uhr), Menue-Text bleibt.

### B7 (minor) Im Auto oeffnet V das Fenster nie; offenes Fenster schluckt V
- Fahrzeug-Radial hat Vorfahrt (S:client/BanditsNPCBearKey.lua:72); Rechtsklick geht ohne Koerper nicht. Den Zustand "Riding with you"
  (grau mit Grund, Auftrag 2) sieht Kevin nur, wenn das Fenster schon vor dem Einsteigen offen war oder die Taste umgelegt ist. Umgekehrt
  verbraucht das offene Fenster V (isKeyConsumed, S:client/ISUI/BanditsNPCBearWindow.lua:546-549; Engine:
  `UIManager.onKeyPress/onKeyRelease` vor OnKeyStartPressed/OnKeyPressed, jar_f1/GameKeyboard.txt:157-173, :369-385): im Auto schliesst der
  erste V-Druck das Fenster, erst der zweite oeffnet das Fahrzeug-Radial. Empfehlung: so lassen, in Kevins Testliste aufnehmen (Frage).

### B8 (minor, Leistung) ~300 Zeichenaufrufe je Bild bei 4K statt der geplanten ~130
- Mitschrift des echten Codes `attrappe/f1_ober/zeichnung.txt`: 1080 224 / 214, 4K **301 / 277** je Bild (davon 127 drawRectBorder:
  jeder Rahmen t-fach, t = 2 bei 4K, und je Faehigkeits-Segment ein Rahmen, S:client/ISUI/BanditsNPCBearWinParts.lua:128-133, :256-270).
  Nur bei offenem Fenster, Modell 1 x je Sekunde -- vertretbar. Optional: Segment als zwei Rechtecke (Rand-Rechteck + Innen) statt
  Rechteck + t Rahmen (~-100 Aufrufe).

### B9 (minor) Vanillas Tier-Radial blitzt bei V am eigenen Baeren auf -- mit "Kill"
- Unser Baer ist `wild = false` (S:shared/BanditsNPCBearDefs.lua:100) -> beim DRUECKEN von V oeffnet Vanilla das Tier-Radial
  (V:client/ISUI/ISUIHandler.lua:35-57); mit einer Waffe mit Tag KILL_ANIMAL enthaelt es "Kill" (V:client/ISUI/Animal/
  ISAnimalContextMenu.lua:1173-1176). Im Rechtsklick-Menue blendet B1 "Kill" aus (S:client/BanditsNPCBearMenu.lua:310), im Radial nicht.
  Unser onKey schliesst es erst beim LOSLASSEN (Key.lua:87-90). Ein Klick waehrend V gehalten wird, toetet den Baeren. Seit F1 ist "V am
  Baeren" der Normalfall. Vorschlag: eigener `Events.OnKeyStartPressed`-Handler, angemeldet in OnGameStart (laeuft dann nach Vanillas,
  V:client/ISUI/ISUIHandler.lua:101-104), der das Radial sofort schliesst, wenn `getUseableAnimal` unser Baer ist (dieselben Aufrufe wie
  Key.lua:76-89, alle belegt).

### B10 (minor) Namensfeld offen ohne Fokus: V schliesst das Fenster doch
- `typing()` sperrt nur `isKeyConsumed`/`onKeyRelease` des Fensters (S:client/ISUI/BanditsNPCBearWindow.lua:535-556); ist V dann nicht
  verbraucht, laeuft OnKeyPressed -> `onKey` (Key.lua:55-91, kein Namensfeld-Riegel) -> WinToggle schliesst. Mit Fokus im Feld unterdrueckt
  die Engine ohnehin alle Tasten (Core.currentTextEntryBox, jar_f1/GameKeyboard.txt:53-75). Harmlos (Umbenennen geht weiter), widerspricht
  nur 21b im Zusammenbau-Bericht. Vorschlag: in `onKey` nichts tun, solange das Namensfenster des Baeren-Fensters sichtbar ist (U-Helfer).

## 2. Jeder Befehl in jedem Zustand (Schreiber-Sicht; "ok" = Bitte wird angenommen, Ergebnis eindeutig)

| Zustand | Follow | Stay | Sit | Roam | Come | Passive | Unstuck | Risiko |
|---|---|---|---|---|---|---|---|---|
| folgt | aktiv | ok (B4) | ok (B4) | ok | ok, `s.come` | ok | ok, Abklingzeit | B4 |
| bleibt | ok | aktiv | ok | ok | ok | ok | ok | -- |
| sitzt (`s.sat`) | ok, standMs 2,3 s halten | ok, aufstehen | gleiche Meldung, sitzt weiter (`stillSat` Follow.lua:107) | ok, aufstehen | ok, aufstehen + kommen | ok | ok, neuer Koerper, `sat` weg (Ride.lua:60) | B3 bei Streicheln/Fuettern |
| frei | ok | ok | ok | aktiv, Mittelpunkt neu | ok | ok | ok | Mittelpunkt bleibt beim Fuettern (Server.lua:241-244, keepHome :243) |
| versteckt (Wache) | Wache geht vor (Server.lua:794) | dito | dito, Treiber steht auf (hide) | dito | Uhr laeuft, nach 30 s "comefail" -> bleibt | ok | ok | keins |
| flieht vor Laerm | CalmAnswer laeuft, danach OrderStep zurueck | dito | dito | dito | dito | ok | ok | keins (kurz "sit" bis Regel 33) |
| faehrt mit | grau / Why_Riding | grau | grau | grau | grau | ok | grau / Why_Riding | keins |
| Komm her laeuft | ok, `come` weg | ok | ok | ok | aktiv | ok | ok, `come` weg | Besitzer im Auto -> steigt ein (Regel 11) |
| Abklingzeit Unstuck | -- | -- | -- | -- | -- | -- | grau "m:ss" (B6) | -- |
| Tausch Tag 15 | -- | -- | Z1 (SP-Flackern, bekannt) | Pause neu | `come` bleibt | bleibt | `placedAt`-Riegel 2 s | Z1 |
| Besitzer offline (MP) | -- | -- | -- | Baer bummelt weiter, wenn geladen | 30 s -> bleibt | -- | -- | C1 nur mit Besitzer online (B1) |
| 2. Spieler, eigener Baer | nur eigene Liste (WinData.lua:180-194); fremde Bitte -> Why_NotOwner | | | | | | | keins |
| Speichern/Laden | mode/passive im Register, `sat`/`come`/`roam` Sitzung (setzt sich neu hin) | | | | | | | B1 (Heil-Fenster) |
| Absturz | Register = letzter Stand; neuerer Spiegel heilt (B1c); C1-Koerper ohne Spiegel-Sicherung wird beim naechsten Suchlauf ersetzt | | | | | | | B1 |
| koerperlos (missing) | grau Why_OutOfReach | grau | grau | grau | grau | ok | **frei** (Auftrag 4b) | B1, B2 |

## 3. Einzelspieler / Mehrspieler
- SP (`not isServer() and not isClient()`): `B.Ask` ruft `B.Handle` direkt (S:shared/BanditsNPCBear.lua:558-567); der Treiber schreibt am
  Tier des Schreibers; Sicht sofort.
- MP: jeder Knopf ein `sendClientCommand` (Mode/Come/Passive/Call/Rename), Server prueft Besitzer, Zustand, Lage, Abklingzeit, Drossel askMs
  500 (S:server/BanditsNPCBearOrder.lua:231-247); kein neuer Server->Client-Befehl; NCBearAct wird nicht uebertragen (nur vier Bits
  `AnimalStateVariables`, dec_b1b/AnimalStateVariables.java:8-19) -> jeder Client setzt an seiner Kopie, keine Pakete -> kein Kick-Risiko.
  C1 im MP erst nach `_scanSeen` (A3 offen) -- ehrlich als Fehlerzeile.
- Rote Linien: kein Gegenstand beruehrt; Baer nie geschlossen (missing schliesst nie, Server.lua:500-510); Doppel nur sichtbar, nie im
  Register (B1, B2, Z3); nichts haengt; keine NPC-Crew-Figur gestoert (Vorfahrt liest nur `BanditsNPC.Interact.FindTarget`,
  NC:client/BanditsNPCInteract.lua:41-70, reines Lesen der Zombie-Liste).

## 4. Kosten je Bild
- Geschlossen: nichts (nicht im UI-Manager). Offen: Modell nur bei neuer Sicht und hoechstens 1 x je Sekunde (Window.lua:512-516); je Bild
  ~220 (1080) bis ~300 (4K) Zeichenaufrufe (B8), keine Tabelle, kein getText. Sitz-Treiber 4 x je Sekunde, nur Sicht-Eintraege (<= 16).
  Je Sekunde ~6 MeasureStringX (dynNeed). In Ordnung.

## 5. Optik (Code gegen `f1_entwurf/fenster_*.png` und `fenster_gebaut_*.png`, 4K-Ausschnitte nachgesehen)
- Gebaut = Entwurf: Kopf mit Symbol auf Scheibe, Name "fett", Zeile 2/3, Chip rechts, Abstand darunter; zwei Karten, Befehle 2 x 3 + 2
  Schalter; Honig-Akzent oben, aktiver Knopf mit Leiste; Balken mit Verlauf (gruen/blau); Segmente Gold/Honig. Ruhig, aufgeraeumt.
- 4K (2054, f 2, Vanilla-Schrift 2x): Fenster 1280 x 1178 (`kopf_lage`), Name Large 40, Text Medium 33, Klein Small 26 -- gut lesbar,
  Klein entspricht Vanillas eigener 2x-Schrift. Relativ zur Bildhoehe ist "Klein" bei 4K eine Stufe kleiner als bei 1080 (dort ist Klein =
  Text = Small 19, Plan-Regel 1.2) -- gewollt, im Bild unauffaellig.
- Ueberlappung/Abschneiden (`attrappe/pruef_f1/kopf_lage.lua`, echter Fenster-Code mit echten EN-Schriftmassen): 9 Faelle (1080/1x kurz,
  24 Zeichen, 24 x "W"; 4K/2x lang und "W"; 1080/4x; 4K/4x; vermisst 1489 Kacheln) -- **keine Ueberlappung** ausser 1 px zwischen
  Umbenennen-Knopf und Zeile 2 bei Vanilla-Schrift 4x auf 1080 (ungewoehnliche Einstellung, unsichtbar). Breite waechst mit jedem Text
  (Window.lua:80-183): RU-Fusszeile ~640 px -> Fenster ~670 px bei 1080 (grob gemessen), PTBR/FR/ES/KO/CN unter 640. Nichts abgeschnitten.
- Kleines: Karte "Condition" hat unten freien Raum (hoehe = Skills-Karte) -- Platz fuer F3, ok. Unstuck-Zahl B6.

## 6. Auftrags-Abweichungen (vom Planer begruendet, nur zur Kenntnis)
- "Frei" Vorgabe 12 statt 8 Kacheln (PLAN_F1.md 0.3, Frage F2: Kevins "Bleiben-Radius 12").
- "Komm her" und "Unstuck" sind zwei Knoepfe (Komm her laeuft ohne Abklingzeit, Unstuck = Call to me mit Abklingzeit; PLAN_F1.md 0.2,
  Frage F1). Der Auftrag schrieb "Komm her (= Call to me)".
- A5: die 288-px-Bilder zeichnet das Fenster auf 72 x f / 80 x f px -- ein Deckel auf 256 wuerde nichts zeigen (Texture-Deckel nur ueber
  `Core.getMaxTextureSizeFromFlags`, jar_f1/TextureID.txt:1136; NUR JAR, unkritisch).
- Taste "Bear window" als Text-Kennung: `tostring(u)` fuer das Namensschild ist in Kahlua exakt (`KahluaUtil.numberToString`: ab 1e14
  `Double.toString`, kuerzeste eindeutige Form; `attrappe/pruef_f1/jar/KahluaUtil.txt:416-453`) -- die Kommentar-Aussage "nichts gerundet"
  stimmt im Spiel (in lua5.1 nicht).

## 7. Attrappen (alle lesen das Staging nur)
| Datei | Aufruf | Ergebnis |
|---|---|---|
| `attrappe/pruef_f1/c1_wartefrist.lua` | `lua5.1.exe c1_wartefrist.lua` (im Ordner pruef_f1) | A korrekt; B und C rot (B1) -> `c1_wartefrist_ergebnis.txt` |
| `attrappe/pruef_f1/sitz_treiber.lua` | `lua5.1.exe sitz_treiber.lua` | 1 und 4 korrekt; 3, 5, 6 rot (B3) -> `sitz_treiber_ergebnis.txt` |
| `attrappe/pruef_f1/kopf_lage.lua` | im Ordner `attrappe/f1_ober`: `lua5.1.exe ../pruef_f1/kopf_lage.lua` | 9 Faelle, 1 Grenzfall 1 px -> `kopf_lage_ergebnis.txt` |
Grenze: Engine-Verhalten (Tier-Lader-Dauer, Anhaenger-Ablauf, Clip-Uebergaenge) beweisen sie nicht -- nur die Lua-Logik.

## 8. Fragen fuer Kevin (Nachtschicht: Empfehlung zuerst)
1. **Anhaenger (B2):** Soll man den Baeren in Vanillas Tier-Anhaenger laden koennen? Empfehlung: **nein** (er faehrt wie die Crew in jedem
   Auto mit); dann "zu gross" fuer jeden Anhaenger -- sonst entsteht nach einer Minute ein zweiter Baer.
2. **C1-Frist (B1):** Baer ohne Koerper kommt von selbst wieder -- erst nach **1 Minute in geladener Gegend** (Empfehlung) und nicht in den
   ersten 2 Minuten nach dem Laden?
3. **Im Auto (B7):** V gehoert dort dem Fahrzeug-Radial; das Baeren-Fenster im Auto nur, wenn es vorher offen war oder mit eigener Taste.
   Empfehlung: so lassen.
4. **Kill im Radial (B9):** Vanillas Tier-Radial am eigenen Baeren sofort wieder schliessen (Empfehlung) -- dann gibt es dort auch kein
   "Kill" mehr.

Statisch geprueft, nicht gespielt.
