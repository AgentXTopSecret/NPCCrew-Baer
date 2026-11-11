# Baer -- Uebergabe an den anderen Claude-Account (11.11.2026 ~15:00)

Kevin (11.11.2026, woertlich): *"workflow abbrechen (oder anlassen wenn der neue account ihn direkt fortfuehren kann) und stand merken fuer meinen
anderen account ich muss den account weckseln der andere account soll alles wissen was ich noch testen soll und wo es weiter geht!"*
(Die alte Uebergabe vom 10.11. steht im Git-Verlauf.)

**Lesereihenfolge:** `../CLAUDE.md` (Grundregeln, ganz) -> DIESE Datei -> `STAND.md` (oben "LIMIT-REGEL" und "Nachtschicht 11.11.2026") ->
`begleiter/ENTSCHEIDUNGEN.md` (ganz unten: alle Wuensche und Freigaben vom 10./11.11. WOERTLICH). Kevin programmiert nicht: Deutsch, kurz,
Ergebnis zuerst, "statisch geprueft, nicht gespielt", nach jeder Mod-Aenderung sagen: Spiel neu starten.

## 1. Wo wir stehen (alles gesichert und hochgeladen; KEIN Workflow laeuft)
- **Test-Mod `C:/Users/Kevin/Zomboid/mods/NCBearTest`**, Git `main` **401dd70** (GitHub `AgentXTopSecret/NPCCrew-Baer`). Unterlagen `baer/`
  Zweig `unterlagen` **e7dec28**. Sicherungen je Schritt in `Zomboid/backups/NCBearTest/` (`*_vor_*/_mit_*` vom 10./11.11.).
- **Baeren-Junges (Code, alle UNGESPIELT ausser B1a/B1b-Teilen):**
  - B1a finden + zaehmen (gespielt: klappt), B1b folgen/bleiben, Namensschild, Umbenennen, Futter hinhalten (Folgen gespielt: klappt),
  - B1c (seit 11.11. 08:12): Zaehmung ueberlebt Absturz (Spiegel v2), kein Fliehen vor Laerm, versteckt sich vor Zombies, Mitfahren im Auto,
    "Call to me" (Unstuck), Gehen, Bildschirm-Markierung mit Kevins Symbol 1, Baeren-Symbol auf Mini-/grosser Karte, Anzeige-Optionen,
  - B1d (seit 10:55): Wachsen ueber 100 Spieltage (Modell haelt bei 0,75), Werte steigen taeglich, Faehigkeiten-Daten, Heil-Formeln.
  - Staging/Arbeitsordner `../_arbeit/baer_zaehmen/` (mod/, PLAN_B1A..D, Berichte); Kopien der Berichte `spiel/b1b_*.md`, `b1c_*.md`, `b1d_*.md`.
- **Neues Junges-Modell aus dem Bild-zu-3D-Generator** (seit 14:39 statt des alten Platzhalters): 26 Knochen, 15 Clips, Gehen 1,6 Kacheln/s.
  Blatt `spiel/rig_KEVIN_junges_spielfertig.png` (nicht in Git), Berichte `spiel/rig_*.md`. **Kevin: "besonders die gesichtsgroesse sieht zu
  klein aus also das maul" und "ich find sogar unser altes baby model sieht besser aus"** -> siehe Abschnitt 3.
- **Vergleichs-Testhilfe** (14:55, nur NCBearBench*): `NCBear_Vergleich()` (altes Junges lebend als Art `ncbearcubalt` + grosser 2c-Baer +
  zwei Standmodelle des Generator-Baeren braun/Fototon ins Inventar), `NCBear_CubAlt()`, `NCBear_GenE()`.
- **Grosser Baer:** im Spiel weiter der 2c-Baer (`NCBear.glb`, Art `bear`). Der Generator-Baer E ist fertig geformt, aber OHNE Knochen/Clips
  (`../_arbeit/baer_gen/aus/E_schoen.glb`, `E_schoen_fototon.glb`; Blatt `spiel/gen_KEVIN_gross.png`).
- **Generator-Werkzeug:** ComfyUI v0.44.0 + TRELLIS.2 lokal (`C:/Users/Kevin/Tools/ComfyUI/ComfyUI_windows_portable/`, Start nur 127.0.0.1:8188),
  Startskript `tools/gen_trellis.py`, Wege/Lehren `spiel/gen_PROBELAUF.md`, `gen_STUFE2.md`, `../_arbeit/baer_gen/` (C_*.md, E_FEIN.md, rig/).
  Fotos `begleiter/vorlage_*.jpg`, `ref_*.jpg` (Wikimedia, nicht in Git).
- **Verbrauch beim Wechsel (dieses Konto):** 5 h 9 %, Woche 3 % (neue Woche). Workflows lassen sich NUR in der Sitzung fortsetzen, die sie
  gestartet hat -- es gibt nichts fortzusetzen (alle Laeufe fertig, siehe STAND.md).

## 2. Was Kevin testen muss (vorher Spiel neu starten, -debug; rote Fehler? `C:/Users/Kevin/Zomboid/console.txt`)
1. **`spiel/anleitung_b1c.md`** -- Mitfahren, Call to me, Laerm, Verstecken, Markierung oben, Karten-Symbol, Optionen (Optionen -> Mods).
   **Teil C (Auto) spaeter** (Kevin 11.11.: *"das mit dem auto muss ich spaeter mal testen irgentwann hab jz kein auto hier ;D"*). Auto im
   Debug: Rechtsklick Boden > Debug > Main > "Spawn Vehicle" (Vanilla `DebugContextMenu.lua:60`).
2. **`spiel/anleitung_b1d.md`** -- `NCBear_CubGrow(tage)`, `NCBear_CubStats()`; Achtung: ueber 0,35 rutschen die Pfoten (bekannt, M3).
3. **Junges-Modell im Spiel ansehen** (sein gezaehmtes Junges traegt das neue Modell) und mit `NCBear_Vergleich()` neben das alte Junge,
   den 2c-Baeren und die Generator-Standmodelle stellen -> Kevin entscheidet altes oder neues Junges und Farbe des grossen Baeren.
4. Aeltere, weiter offen: `spiel/anleitung_2c.md`, `anleitung_laerm.md`, `anleitung_fell.md` (siehe alte Uebergabe im Git-Verlauf).
Seine Antworten woertlich in `begleiter/ENTSCHEIDUNGEN.md` unten eintragen.

## 3. Offene Entscheidungen (Kevin fragen, nicht selbst entscheiden) -- Einzelheiten STAND.md "Fragen fuer Kevin"
- **Junges-Modell:** neues (Generator) behalten und Gesicht/Maul groesser + Kopf hoeher machen, ODER zurueck zum alten Entwurf
  (`../_arbeit/baer_baby/entwurf/NCBearCub.glb` 6c3f0a96 + png; Sicherung `NCBearTest_vor_junges_neu_2026-11-11_143915.zip`) und dessen Clips
  auf das schnellere Gehen umrechnen.
- **Grosser Baer:** Farbe braun oder Fototon; Kopf: 2c-Kopf behalten oder Generator-Kopf? Erst danach Knochen/Clips fuer den grossen Baeren.
- Modellwechsel bei Halbstark (Jungen- oder Erwachsenen-Modell?); B1c/B1d-Fragen (A3 Belege ohne Aufrufer, MP nach Server-Absturz, Q-Ruf beim
  Bleiben, Zombie zwischen Besitzer und Junges, Gehen oefter, FR-Text, Tier-Anhaenger-Luecke F7, Selbstheilung schon an, Leben/Ausdauer-Zahlen).

## 4. Was als Naechstes dran ist (Reihenfolge nach Kevins Woertern vom 10./11.11.)
1. Kevins Tests oben abwarten; Junges-Modell nach seiner Wahl verbessern (Gesicht/Maul) bzw. zurueck; Folgen-Schwelle `walkSpeed` (B1c 0,52) auf
   das Tempo des gewaehlten Modells stellen; M3 (Pfoten rutschen beim Wachsen) loesen.
2. Grosser Baer aus dem Generator spielfertig (Vorlage `spiel/rig_junges_workflow.js`), erst nach Kevins Farb-/Kopf-Wort.
3. **B5a Kampf** (vorher NPC-Crew-Namen fuer die alten NCBear*-Dateien): Zombies greifen GEZAEHMTE Baeren an (auch das Junge; ungezaehmte
   nicht), Faehigkeiten Agilitaet (5-40 %), Leben, Kondition, Kaempfen (+70 % auf Stufe 10), Ausdauer mit Verschnaufen, Heilen (wach ~1 %/h,
   Schlaf ~15 %/h, von Hand; NPC-Heiler spaeter), Fliehen statt Sterben?
4. Schlafen (Muedigkeit; schlaeft selbst, wacht bei Zombies auf und flieht; `begleiter/SCHLAF_PLAN.md` K1-K21), Spuernase (abschaltbar),
   Fischen (ab Halbstark), Baeren-Fenster auf V (Taste einstellbar), Unstuck-Symbol im Spiel, Traglast/Inventar, Mehrspieler-Test.

## 5. Lehren (bitte ernst nehmen)
- **Kevins Bild ist der Massstab** (Gedaechtnis `kevin-vorlage-ist-massstab`). Der Generator-Weg macht NICHT von selbst ein schoeneres Modell --
  Kevin fand das alte Junge schoener. Immer Blatt aus seiner Spielkamera + Spielgroesse neben das Foto, selbst ansehen, bevor "fertig".
- Die Stockfoto-Einschraenkung ist NICHT von Kevin (Gedaechtnis `stockfoto-regel-nicht-von-kevin`).
- Workflows: hoechstens 10 Agenten je Workflow; Skript-Vorlagen `spiel/*_workflow.js` (b1c/b1d fuer Code, rig_junges fuer Modelle).
  Limit-Regel oben in STAND.md (resumeFromRunId, nichts von vorn). Modell-Laeufe dauern viele Stunden (Rig: ~6 h Rechenzeit).
- Einbau: nur bei geschlossenem Spiel (`tasklist | grep -i ProjectZomboid`), Zip vorher/nachher, MD5 nachzaehlen, nur Bench-/eigene Namen
  ueberschreiben; dann `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`, Commit + Push in beiden Repos.
- Absturz-Falle: PZ schreibt beim Absturz in `Saves/.../<save>_crash/`; der normale Ordner behaelt den alten Stand (so ging die erste
  Zaehmung verloren; seit B1c heilt der Spiegel am Tier das).
