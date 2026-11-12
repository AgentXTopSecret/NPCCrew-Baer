# Baer -- Uebergabe fuer Kevins anderen Claude-Account (Stand 12.11.2026 20:15, Sitzung d5933cc7; wird bei Lauf-Ende / Limit-Halt nachgezogen)

Kevin (12.11. ~20:10): *"so keinen neuen workflow mehr starten merk dir den stand schonmal und mach alels fuer die uebergabe an eine nanderen clausde
ascocunt berreit und wenn die workflows durch sind nochmal alles speichern, stell dir einen waechter ab 95% wochen limit stoppst du alles und machst es
berreit fuer die uebergabe und mach ein 5h std waechter an falls er beendet wird deswegen"*. **Statisch geprueft, nicht gespielt**, ausser wo "gespielt" steht.
Die vorige Uebergabe (12.11. frueh) ist hiermit ersetzt; ihr Inhalt ist erledigt (F1b, F2, Kopfnaht, Generator-Modelle).

## 0. Zuerst lesen (in dieser Reihenfolge)
1. `C:\Users\Kevin\.claude\CLAUDE.md` (global: max. 10 Agenten je Workflow, **UI-Bilder nur aus echtem Code**, neu 12.11.) und
   `C:\Users\Kevin\NPCCrew-Nebenprojekte\CLAUDE.md` (Werkstatt-Regeln: Deutsch/kurz, nie in NPC Crew schreiben, nur bei geschlossenem Spiel bzw. nicht
   geladener NCBearTest in die Test-Mod kopieren, Zip vorher/nachher, sichern.py + Commit + Push nach jeder Version).
2. Diese Datei, dann `baer\STAND.md` -- die Bloecke OBEN (neueste zuerst).
3. `baer\begleiter\ENTSCHEIDUNGEN.md` -- UNTEN stehen Kevins neueste Worte woertlich.
4. Feste Arbeitsweise (Gedaechtnis): eine Modell-Spur UND eine Funktionen-Spur; fertige Laeufe selbst pruefen, einbauen, committen, pushen; Modelle erst
   zeigen, wenn sie wirklich schoen sind; UI-Bilder per Zeichen-Mitschrift des echten Codes. **ABER: Kevin 20:10 "keinen neuen workflow mehr starten"** --
   neue Laeufe erst auf Kevins Wort im neuen Account.

## 1. Was im Spiel ist (Test-Mod `C:\Users\Kevin\Zomboid\mods\NCBearTest`, Git main 99e0368, alles UNGESPIELT seit F1b)
| Commit | Was | Kevins Test |
|---|---|---|
| db80ad6 | F1b: Baerenfenster mit **E** nah am Baeren, Fern-Taste in Optionen > Mods, V wieder Vanilla, Schalter Growth line | `baer\spiel\anleitung_f1b.md` |
| 8a22bf9 | **F2 Kampf** (Zombies/feindliche Banditen greifen an, Baer kaempft ab halbstark, flieht 3 Treffer vor dem Tod, Am Boden/Aufhelfen, Verband, Schadenszahlen, Melee damage, Kills, Lerntempo + Alters-Deckel, kein Schaden durch Freunde) + **alle Texte auf Deutsch** (8. Sprache) | `baer\spiel\anleitung_f2.md`; offene Kevin-Fragen in STAND.md Block "15:08" |
| 71ce40a, 59973dc | Generator-Baer v2 (nur Vergleich `NCBear_GenLive()`), Kevins **schmale Nase** | Blatt `_arbeit\baer_gen_gross\v2\bilder\KEVIN_gen_gross_schmal.png` |
| d5ab258 | **Grosser Baer** neu: Aufrichten/Bruellen wie ein echter Baer, Kevins roter Bogen am Nacken weg (Rest: ~0,1 s Kopfumriss am Ende des Aufrichtens, Nackenfell nah knittrig) | Blatt `_arbeit\baer_kopfnaht\bilder\KEVIN_kopfnaht.png`; Test in `_arbeit\baer_kopfnaht\gegen_bericht.md` (kevin_test) |
| 99e0368 | **Generator-Junges v2** (nur Vergleich `NCBear_CubGen()`): kurze Beine, Baerenfuesse, Baerenschritt, groesseres Gesicht | `baer\spiel\anleitung_gen_junges_v2.md`; Fragen: Gehen 0,34 statt 0,52 Kacheln/s (Trippel-Variante 0,51 liegt in `_arbeit\baer_gen_junges\v2\beine\var_gehen3\`), gleich gross wie Standard? |

## 2. Laufende Laeufe (gestartet in Sitzung d5933cc7 -- `resumeFromRunId` gilt NUR dort)
Transkripte: `C:\Users\Kevin\.claude\projects\C--Users-Kevin-NPCCrew-Nebenprojekte-baer\d5933cc7-7f9d-46b2-a3a8-0929595b654b\subagents\workflows\<Lauf-ID>\journal.jsonl`
(eine Zeile `{"type":"result",...}` je FERTIGEM Agenten).
| Lauf | Lauf-ID / Task | Skript | fertig (20:13) | danach |
|---|---|---|---|---|
| **baer-aussehen** (Funktion: Aussehen-Knopf + Sandbox 39 -> 12) | `wf_34a802e5-6f8` / wbvwbx4bx | `baer\spiel\aussehen_workflow.js` | forschung, plan, bau:kern, bau:oberflaeche, pruef:logik | pruef:belege, nachbesserung, gegenpruefung |
| **baer-maul-bau** (Modell: Maul beider grosser Baeren) | `wf_a876c805-e76` / w8qe5etel | `baer\spiel\maul_bau_workflow.js` | W:rahmen, T:textur | G:gebiss, PT+PO, N, GP, I |
| **baer-f3-plan** (Funktion: F3 Forschung + Plan, nur lesen) | `wf_881b0108-ad0` / whr8tzmw4 | `baer\spiel\f3_plan_workflow.js` | forschung | plan |

**Fortsetzen in einem NEUEN Account/einer neuen Sitzung** (kein Lauf-Cache): wie `baer\spiel\f2_fortsetzung.js` -- fertige Rollen werden
Text-Konstanten ("X ist fertig: <Bericht>, ganz lesen"), ab der ersten nicht fertigen Rolle echte Agenten mit dem Zusatz "FORTSETZUNG: Zwischenstaende
pruefen, nur Vollstaendiges weiterverwenden". Welche Rollen fertig sind: journal.jsonl (oben) bzw. die Berichte in den Ordnern:
- Aussehen: `_arbeit\baer_zaehmen\aussehen\` (FORSCHUNG.md, PLAN_AUSSEHEN.md, BAU_KERN.md, BAU_OBER.md, PRUEF_A.md, PRUEF_B.md, NACHBESSERUNG.md,
  GEGEN.md, anleitung_entwurf.md, staging_dateien_look.txt, mod_info_vorschlag_look.txt), Staging `_arbeit\baer_zaehmen\mod_look\` (= Test-Mod 99e0368 + Bau).
- Maul: `_arbeit\baer_maul\` (FORSCHUNG.md, PLAN_MAUL.md, bau\w|g|t|pt|po\..., bau\NACHBESSERUNG.md, bau\GEGEN.md, BAU_MAUL.md, Staging bau\out_c2\, bau\out_gen\).
- F3-Plan: `_arbeit\baer_zaehmen\f3\` (FORSCHUNG_F3.md, PLAN_F3.md mit hoechstens 6 Fragen an Kevin).
Die Stand-Zeile oben in `baer\STAND.md` sagt, ob ein Lauf inzwischen fertig/eingebaut ist (die alte Sitzung zieht sie nach).

## 3. Was nach den Laeufen zu tun ist (Reihenfolge; NEUE Laeufe nur auf Kevins Wort)
1. **Aussehen einbauen** (Spiel zu oder NCBearTest nicht im geladenen Spielstand): Liste `_arbeit\baer_zaehmen\aussehen\staging_dateien_look.txt`
   (Modell-Dateien, die die Test-Mod neuer hat = "NICHT KOPIEREN"), Werkzeug-Vorlage `baer\tools\einbau_f2.py` (kennt neu/ueberschreibt/gleich/NICHT KOPIEREN/
   bedingt), mod.info aus `mod_info_vorschlag_look.txt`, Trockenlauf `python baer\tools\baer_uebernahme.py` (0 Fehler erwartet), sichern, Commit, Push.
2. **Maul einbauen**, wenn der Gegenpruefer je Baer empfiehlt (`_arbeit\baer_maul\bau\GEGEN.md`): 2c 5 Dateien aus bau\out_c2, Gen 3 aus bau\out_gen
   (Vorlage `baer\tools\einbau_gross.py` / `einbau_gg2s.py`); Kevin das Blatt `_arbeit\baer_maul\bilder\KEVIN_maul.png` zeigen.
3. **F3-Fragen** (PLAN_F3.md, Ende) Kevin stellen; danach F3-Bau (Fenster-Variante B, Kevin 12.11. "B (breit)", Vorlage `_arbeit\baer_zaehmen\ui_entwurf\proto\`).
4. Spaeter (Kevins Wuensche, ENTSCHEIDUNGEN.md): Liegen/Tot beider Baeren (Pfoten frei), Schlafpose nach Kevins Bild (Modell-Lauf), F4 Traglast/Inventar,
   F5 Spuernase (abschaltbar) + Fischen, F6 Mehrspieler, Sandbox-Seiten nach NPC-Crew-Schema (Vorschlag `baer\NAEHTE.md` "Sandbox-Seiten"; page-Namen
   meldet die NPC-Crew-Sitzung), Restpunkte Kopfnaht (Ende Aufrichten, Nackenfell), Generator-Baer bekommt das neue Aufrichten (Kevin: "erstmal so lassen
   und angucken").

## 4. Kevins Entscheidungen von heute (Kurzfassung; woertlich in ENTSCHEIDUNGEN.md)
- Aussehen-Knopf als echte Spieler-Funktion; kein Heilen beim Wechsel, Abklingzeit mit Unstuck geteilt.
- Deutsch als achte Sprache; Begriffe: Faehigkeiten, Leben, Herholen, stark (Vitality = Zaehigkeit).
- Sandbox nur noch **12 Regler** (Junge an/aus, Haeufigkeit, Baeren je Spieler, Koederplatz, Zaehm-Tempo %, Tage bis ausgewachsen, Lerntempo %,
  Faehigkeiten nach Alter, kann nicht sterben, Flucht-Schwelle, Schaden %, Heil-Tempo %); Zombies/Banditen greifen IMMER an.
- Maul: Mundwinkel bis unters Auge, dunkle Lippenlinie auch zu; drei Commons-Fotos in `baer\begleiter\ref_maul\` (nur ansehen, .gitignore).
- Fenster-Variante **B (breit)**.
- Generator-Baer: schmale Nase.

## 5. Werkzeuge
- Einbau: `baer\tools\einbau_f2.py` (Liste mit Arten), `einbau_gross.py`, `einbau_gg2s.py`, `einbau_gj2.py` (je mit `--baer-nicht-geladen`, wenn das Spiel
  ohne NCBearTest laeuft -- vorher die zweite "Loading Mods"-Liste in `Zomboid\console.txt` lesen).
- Uebernahme-Trockenlauf: `python baer\tools\baer_uebernahme.py` (kennt 8 Sprachen; heute 0 Fehler, 2 Warnungen).
- Lua-Pruefer: `python C:\Users\Kevin\Zomboid\mods\NPCCrew\_docs\tools\luacheck.py|scopecheck.py|localcount.py|luacheck_pz.py <datei>`.
- UI-Bild aus echtem Code: `_arbeit\baer_zaehmen\ui_entwurf\werkzeug\zeichne_entwurf.py` (Vorbild), F1/F2: `_arbeit\baer_zaehmen\f1_entwurf\`.
- Gedaechtnis sichern: `python C:/Users/Kevin/Claude-Gedaechtnis/sichern.py`; dann Commit + Push in Test-Mod (main) und `baer\` (Zweig unterlagen, einfaches `git push`).

## 6. Verbrauch und Waechter (alte Sitzung)
12.11. 20:13: Woche 75 % (Reset Sa 14.11. 04:00), 5 h 63 % (Reset 23:40). In der alten Sitzung laeuft ein Waechter (CronCreate, alle 10 min):
Woche >= 95 % -> alle Laeufe anhalten (TaskStop), diese Datei mit dem Halt-Stand nachziehen, Commit/Push; 5-h-Limit -> nach dem Reset haengende
Laeufe mit `resumeFromRunId` fortsetzen (nur in der alten Sitzung moeglich).
