# Baer -- Uebergabe an den anderen Claude-Account (10.11.2026 ~11:00)

Kevin (10.11.2026, woertlich): *"du speicherst erstmal alles ab fuer meinen anderen claude account das er bescheid weiss wo wir sind und was als
naechstes dran kommt und was wir noch testen muessen"*. (Die alte Uebergabe vom 09.11. ist erledigt und steht im Git-Verlauf.)

**Lesereihenfolge:** `../CLAUDE.md` (Grundregeln, ganz) -> DIESE Datei -> `STAND.md` (Liste "Offen") -> `begleiter/ENTSCHEIDUNGEN.md` (ganz unten
stehen Kevins neueste Wuensche: Spieltest vom 10.11., Gebiss/Beine, Babygesicht). Kevin programmiert nicht: Deutsch, kurz, Ergebnis zuerst,
"statisch geprueft, nicht gespielt", nach jeder Mod-Aenderung sagen: Spiel neu starten.

## 1. Wo wir stehen (alles gesichert und hochgeladen, nichts laeuft)
- **Test-Mod `C:/Users/Kevin/Zomboid/mods/NCBearTest`**, Git `main` **b42435e** (GitHub `AgentXTopSecret/NPCCrew-Baer`). Darin seit 10.11. 10:37
  der Baer aus **Lauf baer-2c**: Sitzen nach Kevins Vorlage (aufrecht, Beine eng, Vorderbeine gerade), Hinterfuss kurz und dunkel (29 statt
  43 cm), Beine ohne "Hose in Stiefeln", Rumpf schmaler (0,79 statt 0,93 m), Gebiss mit 4 gebogenen Eckzaehnen + 6+6 Schneidezaehnen, flache
  rosa Zunge. 5 Dateien: GLB 08ec7806, Deer-GLB 91f0c60e, FBX da08d469, Body-Textur 4cfdb177, WorldItems a640e4cd. 12 Clips byte-gleich,
  NCBear_SitDown/Sit/StandUp neu (gleiche Dauer und Proben), Skelett gleich, Kopf von aussen gleich, 19.806 Dreiecke (alles von Claude
  nachgezaehlt). **Ungespielt.** Sicherungen `Zomboid/backups/NCBearTest/NCBearTest_vor_2c_2026-11-10_103718.zip` und `..._mit_2c_...`.
- **Unterlagen `baer/`**, Git-Zweig `unterlagen` (lokal `main`, `git push` landet richtig). Berichte von 2c: `spiel/2c_*.md`
  (zuerst `2c_gegen_bericht.md`), Bild `spiel/2c_vorher_nachher.png`.
- **Baer-Junges: nur ENTWURF, nicht im Spiel.** `../_arbeit/baer_baby/entwurf/NCBearCub.glb` (MD5 6c3f0a96) + `NCBearCub.png`, eigenes Gesicht
  nach Kevins Foto (runder Kopf, runde Ohren, kurze helle Schnauze), gleiche 26 Knochen und 15 Clip-Namen, Clips per Skript umgerechnet.
  Kevin hat das Blatt `spiel/baby_entwurf.png` gesehen, aber noch nicht geantwortet. Berichte `spiel/baby_*.md` (zuerst `baby_fix_baby.md`).
- **Kein Workflow offen.** Workflows lassen sich nur in der Sitzung fortsetzen, die sie gestartet hat -- es gibt nichts fortzusetzen.
- **Verbrauch bei der Uebergabe (alter Account):** Woche 93 %, Reset 15.11. 23 Uhr. Ein Modell-Lauf mit 10 Agenten kostete hier 15-25 % der Woche.
  Kevins Regel (10.11., ueber die NPC-Crew-Hauptsitzung): weiterarbeiten bis 98 % Woche, dann sofort anhalten, speichern, Uebergabe schreiben.

## 2. Was Kevin testen muss (vorher Spiel neu starten; rote Fehler? `C:/Users/Kevin/Zomboid/console.txt`)
1. **`spiel/anleitung_2c.md` -- zuerst.** `NCBear_SpawnLive()`, `NCBear_Sit(20)` aus der Spielkamera, Hinsetzen/Aufstehen, einmal um den
   stehenden Baeren laufen, Gehen/Rennen, `NCBear_AnimTest("rear")` fuer Zaehne und Zunge, Maul zu nah ansehen.
2. **`spiel/anleitung_laerm.md`** (seit 08.11. ungespielt): flieht der Baer bei Zombie-Schlaegen an Zaun/Tuer oder Q-Rufen nicht mehr endlos?
3. **`spiel/anleitung_fell.md`** (Unterseite und Brust beim Aufrichten und Sitzen; die Pfoten-Teile sind durch 2c ueberholt).
4. `spiel/anleitung_pfote.md` ist durch 2c ueberholt (Kevin hat es am 10.11. ~01:00 gespielt; seine Kritik steckt in 2c).
Seine Antworten woertlich in `begleiter/ENTSCHEIDUNGEN.md` unten eintragen.

## 3. Offene Entscheidungen -- Kevin fragen, nicht selbst entscheiden
- **Aus 2c (Gegenpruefer: klar besser, aber nicht fertig):**
  - G1: Im Sitzen woelbt sich hinter dem Kopf noch ein Buckel ueber die Ohren (2,6-4,2 cm) -- 1,5-3 cm tiefer?
  - G2: Das Fell direkt um den Kopf ist 12 % dunkler als der Kopf (Kopf wirkt leicht aufgeklebt) -- Kopf-Randfarbe angleichen? (Kopf-Texel
    sind nach Kevins Regel tabu; die Form bleibt in jedem Fall.)
  - G3: Der Kopf schaut im Sitzen nach oben, die Vorlage geradeaus -- geradeaus drehen?
- **Baby:** Augen groesser? Rumpf kuerzer (wirkt wie ein Fass)? Schrittweite 0,777 oder 1,0 x Erwachsener? Halbstark mit Jungen- oder
  Erwachsenen-Modell? Zwei Abweichungen ok (Unterlid dunkel statt hellgrau, Ohrrand fellfarben)?
- **Reihenfolge (wichtig):** Kevin 10.11. ~01:20: *"ich wuerd ja gern auch mal baeren features machen das taming und so vom baby baeren aber
  das model verkackst du leider immer"*. Vorschlag an ihn (noch ohne Antwort): nach 2c direkt Features (Baby finden + zaehmen), das neue
  Aufrichten hinten anstellen. Bis er antwortet, gilt seine Reihenfolge vom 09.11. ("Reihenfolge lassen", Abschnitt 4).
- **Vorschlag Baby finden/zaehmen (ihm erklaert, nicht bestaetigt):** selten im Wald in Spielernaehe ausser Sicht (Sandbox-Haeufigkeit) oder
  Koeder (Honig/Fisch, 1-3 Naechte); Zaehm-Balken aus Fuettern und Streicheln; ungefuettert und 1-2 Spieltage ohne Kontakt -> verschwindet,
  einmal gefuettert -> bleibt; je Spieler hoechstens ein Baer und ein wildes Junges; nach Tod des eigenen Baeren neues Junges nach 7 Spieltagen;
  Zombies greifen nur den gezaehmten Baeren an.
- **Aeltere, weiter offen:** baer-laerm (`changeStress` nach Flucht? `setShouldFollowWall(false)` nur Jar-belegt -> braucht sein Wort;
  stoert clockHit?), baer-fell (Zotteln am Umriss, Kopf-Variante B), Schlafen (`begleiter/SCHLAF_PLAN.md` Fragen K1-K21).

## 4. Was als Naechstes dran ist (Kevins Reihenfolge vom 09.11., Einzelheiten `STAND.md` "Offen" 3-13)
1. Kevins Test von 2c abwarten, dann **G1-G3** nach seinem Wort beheben (klein; Nacken/Buckel, Kopfrand-Farbe, Kopfwinkel in den Sitz-Clips).
2. **Clip-Runde:** Aufrichten `NCBear_Rear` neu (ganzer Koerper, kein Kragen, bleibt 3,0 s); Lefzen beim Bruellen hochziehen (geht nur mit
   Clip/Knochen, `spiel/2c_forschung_gebiss.md`); `Toe0` abrollen; Pranke beim Aufrichten von vorn klotzig; Hinterfuss im Renn-Rueckschwung;
   Liegen schwebt. (Sitzen Richtung (b) ist mit 2c erledigt.)
3. **B5a Gegenwehr** -- vorher umbenennen auf NPC-Crew-Namen (`BanditsNPCBear*`, `BanditsNPC.Bear`, `UI_BN_Bear_*`, Testhilfen nur in
   `NCBearBench*`).
4. **B1 + Baby finden und zaehmen:** Weg aus `spiel/baby_spez_baby.md` Abschnitt 3 -- eigene Tierart `bearcub` mit `NCBearCub.glb`, Stufe ->
   `bear` wie Vanilla Kitz -> Hirsch (`DeerDefinitions.lua:7-11`); beim Wachsen baut die Engine ein NEUES Tier (`AnimalData.grow`), modData geht
   NICHT mit -> Besitzer, Zaehm-Balken, Inventar selbst weiterreichen; Clips fuer das Junge per Skript umrechnen (Drehungen gleich,
   Lage-Schluessel neu). Spaetestens hier `baer_uebernahme.py` mit Cheat-Pruefung (Vorbild `../turret/tools/turret_uebernahme.py`).
5. Danach Befehle + Fenster (V-Taste, Namensschild, Balken), Beduerfnisse, Inventar, Fischen, Mehrspieler, Schlafen.

## 5. Lehren aus diesen Tagen (bitte ernst nehmen)
- **Kevins Bild ist der Massstab, nicht die Literatur.** Der "anatomisch richtige" Hinterfuss (29 cm, spitze Ferse, L/B 1,9) sah im Spiel
  aus wie ein Menschenfuss. Immer: Renders aus GENAU seiner Spielkamera (schraeg von oben, auch seitlich), Ton UND Textur, neben sein Bild
  legen und selbst ansehen, BEVOR "fertig" gesagt wird. Eine Textur darf eine falsche Form nie verdecken.
- **Kopf-Aussenform bleibt** (Kevin 08.11.: "das gesicht also der kopf vom baeren passt so"). **Clips bit-gleich**, ausser ein Bein laesst
  sich nachweislich nur mit neuer Pose retten.
- Modell-Laeufe: Plan -> Bau -> Pruefer -> Nachbesserung -> Gegenpruefer, hoechstens 10 Agenten; vorher Verbrauch pruefen und Kevin die
  Agentenzahl nennen. Vorlage fuer einen neuen Lauf: `spiel/2c_workflow.js` (gemeinsamer Kontext CTX mit allen festen Regeln, Suchorten,
  GPU-Sperre je Arbeitsordner; Rendern auch bei laufendem Spiel erlaubt) bzw. `spiel/baby_workflow.js`.
- Modell-Kette: neueste Skripte `spiel/baer_{quelle,export,kampf,gewichte,textur,maul}_2c.py`; fuer einen neuen Lauf KOPIEREN
  (`*_<lauf>.py`), Originale nie aendern. Arbeitsdaten und Werkzeuge `../_arbeit/baer_2c/` (Mod-Ergebnis `mod/42/media/`, Pruefwerkzeuge
  `pruef/gegen/werkzeug/`), Importer-Harness `../_arbeit/baer_spiel/harness` (Dump.java = so liest das Spiel das GLB).
- Einbau: nur wenn Kevin NICHT spielt (`tasklist | grep -i ProjectZomboid`), Zip vorher und nachher nach `Zomboid/backups/NCBearTest/`,
  MD5 nachzaehlen; dann `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, Commit + Push in beiden Repos.
- Kevins Vorlagebilder in `begleiter/` (`kevin_sitzvorlage.png`, `kevin_bruellen_vorlage.webp`, `kevin_babygesicht_vorlage.webp`,
  `kevin_baerenfuss_vorlage.png`, `kevin_pfotenvorlage.png`) sind Stockfotos: NUR ansehen, nie hochladen, nie in Modell/Textur
  (stehen in `.gitignore`); sein Spielbild `kevin_sitzen_fuss_kopf.webp` bleibt ebenfalls lokal (zeigt ein Steam-Overlay).
