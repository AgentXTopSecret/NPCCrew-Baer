# Baer -- Uebergabe fuer Kevins anderen Account (12.11.2026, ab ~07:20; wird beim Abschluss bzw. Limit-Halt nachgezogen)

Kevin (12.11. ~07:10): *"wenn die workflows durch sind alles speichern und berreit machen fuer meinen anderen account das er bescheid weiss wo es
weiter geht"*. Diese Datei sagt der neuen Sitzung, wo es weitergeht. **Statisch geprueft, nicht gespielt**, ausser wo "gespielt" steht.

## 0. Zuerst lesen (in dieser Reihenfolge)
1. `C:\Users\Kevin\NPCCrew-Nebenprojekte\CLAUDE.md` (Werkstatt-Regeln: Deutsch und kurz, hoechstens 10 Agenten je Workflow, nie in NPC Crew schreiben,
   nur bei geschlossenem Spiel in die Test-Mod kopieren, Zip vorher/nachher, sichern.py + Commit + Push nach jeder Version).
2. `baer\STAND.md` -- die Bloecke OBEN (neueste zuerst) bis "NACHTSCHICHT 11./12.11.2026".
3. `baer\begleiter\ENTSCHEIDUNGEN.md` -- UNTEN stehen Kevins neueste Wuensche woertlich (12.11.: E-Taste, Wachstums-Schalter, Show damage,
   Melee damage, Lerntempo, Kill-Zaehler, kein Schaden durch Freunde, Kopfnaht, Fischen-Balance).
4. Gedaechtnis-Regel (feste Arbeitsweise): immer eine Modell-Spur UND eine Funktionen-Spur; fertige Laeufe selbst pruefen, einbauen, wenn das Spiel zu
   ist, committen, pushen, naechsten Lauf starten. Modelle erst Kevin zeigen, wenn sie wirklich schoen sind (Kevins Bild + Spielkamera sind der Massstab).

## 1. Was im Spiel ist (Test-Mod `C:\Users\Kevin\Zomboid\mods\NCBearTest`, Git main cee4890 = F1 + Junges mit Baerenfuessen)
- B1a-B1e (finden, zaehmen, folgen, wachsen, ab Tag 15 grosser Koerper `ncbeargrown` = 2c-Modell), Generator-Baer nur als Vergleich (`NCBear_GenLive()`).
- **F1 Baerenfenster** (gespielt 12.11. frueh: Kevin "neues ui anzeige passt ... das ist top"): heute noch auf Taste **V** -- Kevin will **E in der
  Naehe** (F1b, siehe 2).
- Bekannt im Spiel (alles fuer F2 eingeplant, siehe 3): je Text eine harmlose Konsolen-Warnung "Missing arguments" (Fix 3 liegt im F2-Staging);
  der zahme Baer kann vom Spieler getoetet werden (Kevin hat es passiert, 11.6); Faehigkeiten lernen zu schnell (11.4). Nach einem Baeren-Tod sperrt
  die Trauerzeit neue Junge -- zum Testen `NCBear_CubClean()`.

## 2. Laeufe und ihr Stand (Arbeitsordner `C:\Users\Kevin\NPCCrew-Nebenprojekte\_arbeit\`)
WICHTIG: `resumeFromRunId` gilt NUR in der alten Sitzung. Eine neue Sitzung setzt fort, indem sie die fertigen Rollen aus ihren Berichten nimmt
(Vorbild: `baer\spiel\f2_fortsetzung.js` -- Forschung/Plan als Text-Konstanten, ab Bau echte Agenten).

| Lauf | Stand | Ergebnis / was als Naechstes |
|---|---|---|
| baer-gross (grosser Baer schoener) | FERTIG 06:45 | Aufrichten/Bruellen wie echte Baeren, Sitzen ok; **Kopfnaht wie heute** (Kevins Bilder `baer\begleiter\kevin_kopfnaht_1112_*.png`, nur lokal) -> NICHT eingebaut. Staging `baer_gross\mod\`, Blatt `baer_gross\bilder\kevin_vorher_nachher.png`, Urteil `baer_gross\gegen_bericht.md`. |
| baer-kopfnaht | VORBEREITET, nicht gestartet | `baer\spiel\kopfnaht_workflow.js` (6 Agenten, baut auf baer_gross\mod auf). Danach grossen Baeren einbauen (Kevin-Freigabe 2: ersetzt 2c) und Kevin zeigen. |
| baer-junges-fuss (Junges mit Baerenfuessen) | FERTIG + EINGEBAUT 07:28 (NCBearTest cee4890) | Kevins Test und Fragen: `baer/spiel/anleitung_jfuss.md` (Sitzhaltung, Liegen tiefer -- Variante fertig, Schweben beim Rennen). |
| F1b (E-Taste, Fern-Taste, Wachstums-Schalter) | lief 07:20 beim Bauer (von 8 Agenten: forschung, plan fertig) | Staging `baer_zaehmen\mod_f1b\`, Plan `baer_zaehmen\PLAN_F1B.md`; letzte Rolle fuehrt in das F2-Staging zusammen (`f1b_merge.md`). Siehe Abschnitt 5. |
| F2 (Kampf B5a + Nachtraege) | ANGEHALTEN 03:58 im Bau | Forschung + Plan fertig (`baer_zaehmen\forschung_f2_*.md`, `PLAN_F2.md` mit Abschnitt 11). Fortsetzen mit **`baer\spiel\f2_fortsetzung.js`** (7 Agenten, ab Bau), ERST wenn F1b in der Test-Mod ist und `f1b_merge.md` keine Kollision meldet. |

Dazu Modell-Aufgabe **Junges UND grosser Baer liegend/tot** (Kevin 07:50 "Ja, beide Baeren") (Kevin 07:40: "die beine stecken ineinander (die fuesse)"): Dead/Death neu, Pfoten frei, liegt auf
(Variante liegen_gesenkt 7005099d in `baer_junges_fuss`), Blatt `baer_junges_fuss/bilder/KEVIN_junges_liegen.png`; eigener kleiner Modell-Lauf.

## 3. F2-Inhalt (Kevins Wuensche 12.11., alle in `PLAN_F2.md` Abschnitt 11)
Kampf: Zombies und feindliche Banditen greifen den gezaehmten Baeren an, er kaempft ab halbstark mit; Faehigkeiten wirken; Fliehen/Tod/Am Boden;
Verband. Dazu: 11.1 Schalter "Show damage" (Zahlen ueber Zombies wie Kevins Mod CombatText, nur gelesen), 11.2 Zeile "Melee damage" unter Condition
(Groesse + Kaempfen, `B.MeleeDamage`), 11.4 Lerntempo 2 statt 6 XP/min, Alters-Deckel 3/6/8/10 (Balken ausgegraut UND "max for its age"),
Sandbox-Prozent 25-1000 und an/aus, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Autos/Turrets/NPCs + Bench-Meldung "%1$s" reparieren.
11.7 Fliehen erst, wenn das Leben nur noch fuer 3 Treffer reicht (Kevin: "nur noch fliehen wenn er low hp ist sodas er nach 2-3 hits sterben
wuerde"), Sandbox 1-10, Vorgabe 3; ersetzt die 20-%-Schwelle.

## 3b. Schlaf-Pose (Kevin 07:50: "das er darauss eine schlafpose macht fuer unsere baeren ... baby und ganz gross")
Nach 5 Wikimedia-Commons-Fotos (Liste mit Links, Groessen, Lizenzen: `baer/begleiter/ENTSCHEIDUNGEN.md` ganz unten), fuer Junges UND grossen Baeren
(am grossen Baeren entwerfen, mit dem Sitz-Umrechner auf das Junge uebertragen). Gehoert zu F3 (Schlafen, `baer/begleiter/SCHLAF_PLAN.md`).
Download erst nach Kevins Ja je Datei (noch nicht gegeben).
Dazu Kevins eigenes Bild `baer/begleiter/kevin_schlafen_vorlage_1112.png` (eingerollt auf der Seite, Pfoten frei) -- Vorrang als Vorlage, ggf. zweite
Haltung "eingerollt" neben der Sphinx (Kevin entscheidet im F3-Plan).
Beim Schlafen steigt ein z Z z ueber dem Kopf auf (SCHLAF_PLAN.md Abschnitt 2) -- Kevin will dafuer eine passende Farbe (Vorschlag sanftes Hellblau,
im Plan als Bild zeigen).

## 4. Spaeter (Funktionen-Liste, STAND.md "NACHTSCHICHT")
F3 Beduerfnisse + Schlafen (`baer\SCHLAF_PLAN.md`), F4 Traglast/Inventar, F5 Spuernase + Fischen (Balance fest: Ertrag = NPC-Angler gleicher Stufe x
0,5 halbstark .. 1,0 ausgewachsen, jedes Wasser; offene Fragen: von selbst/Befehl, Fische bringen, Zusehen), F6 Mehrspieler-Pruefung.

## 5. Abschluss-Stand (wird beim Ende/Halt eingetragen)
- (noch offen)

## 6. Werkzeuge
- Einbau in die Test-Mod: `baer\tools\einbau_f1.py` (Vorlage; SRC/LISTE/Zip-Namen anpassen), danach mod.info + 42/mod.info `description=` ersetzen,
  Trockenlauf `python baer\tools\baer_uebernahme.py --vor-b5a` (0 Fehler erwartet), `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`,
  Commit + Push in Test-Mod (Zweig main) und `baer\` (Zweig unterlagen; ein einfaches `git push` landet richtig).
- Lua-Pruefer: `python C:\Users\Kevin\Zomboid\mods\NPCCrew\_docs\tools\luacheck.py|scopecheck.py|localcount.py|luacheck_pz.py <datei>`.
- Fehlerwaechter bei Kevins Tests: `python C:\Users\Kevin\Zomboid\mods\NPCCrew\_docs\tools\bugwatch.py` als Monitor (30 min).
- Erinnerungen der alten Sitzung: `C:\Users\Kevin\AppData\Local\ClaudeErinnerungen\baer.md`.

## 7. Verbrauch
Woche 91 % am 12.11. 07:15 (Reset So 15.11. 23:00). Kevin 06:50: *"erstmal merken ich glaub unser limit laesst das garnichtmehr zu"* -- neue Laeufe
erst nach dem Reset bzw. mit dem anderen Account; Reihenfolge danach: F2 fortsetzen, dann baer-kopfnaht (Kevin vorher kurz fragen).
