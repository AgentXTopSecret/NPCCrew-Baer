export const meta = {
  name: 'baer-f3-plan',
  description: 'Baer F3 (Beduerfnisse + Schlafen) -- Forschung auf heutigem Stand + Plan inkl. Fenster-Variante B; Bau als eigener Lauf nach dem Aussehen-Lauf (2 Agenten; nur lesen + Plan schreiben)',
  phases: [{ title: 'Forschung' }, { title: 'Plan' }],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const W = N + '/_arbeit/baer_zaehmen'
const F = W + '/f3'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Lauf "baer-f3-plan" fuer Kevins Mod NPC Crew (Project Zomboid 42.22; Bandits ${BAN}/42.22, ${BAN}/common). Deutsch, "statisch geprueft,
nicht gespielt", jede Behauptung mit Fundstelle (Datei:Zeile). F3 = BEDUERFNISSE (Hunger, Durst, Muedigkeit, Vertrauen) + SCHLAFEN des gezaehmten Baeren.
QUELLEN (ganz lesen): ${B}/begleiter/SCHLAF_PLAN.md (09.11., Fragen K1-K21) + Forschung ${N}/_arbeit/baer_schlaf/forschung_*.md;
${B}/begleiter/ENTSCHEIDUNGEN.md (geht vor; u. a. Heilen: "beim schlafen soll er viel schneller geheilt werden das er quasi immer voll ist nach dem er
paar ingame std geschlafen hat"; Schlafpose nach Kevins Bild ${B}/begleiter/kevin_schlafen_vorlage_1112.png (eingerollt auf der Seite, Pfoten frei) mit
Vorrang, dazu 5 Commons-Fotos (Liste unten in ENTSCHEIDUNGEN, Download erst nach Kevins Ja je Datei); z Z z ueber dem Kopf in eigener Schlaf-Farbe
(Vorschlag Hellblau, Kevin waehlt); Hunger-/Durst-Balken ueber dem Kopf (ENTSCHEIDUNGEN ~105-109); Fenster Variante B FEST (Kevin 12.11. "B (breit)"):
drei Karten Condition | Needs | Skills, Befehle in 5 Spalten -- Vorlage Prototyp ${W}/ui_entwurf/proto/ und ${W}/ui_entwurf/ENTWURF.md (Fragen F1-F9);
Sandbox: Kevin kuerzte am 12.11. von 39 auf 12 Regler ("komplett uebertrieben") -- F3 bringt hoechstens 1-2 neue Regler, sonst feste Werte; Seiten-
Schema ${B}/NAEHTE.md "Sandbox-Seiten"; Aussehen-Knopf (Lauf baer-aussehen laeuft, ${W}/aussehen/): Beduerfnisse muessen im Register liegen (Koerper-
Tausch). STAND: Test-Mod ${T} (F1, F1b, F2 Kampf, DE, grosser Baer neu). Laufend: baer-aussehen (Staging ${W}/mod_look, nicht anfassen), baer-maul-bau.
Die Schlaf-POSE (Clip) ist Modell-Arbeit: im Plan als eigenen Modell-Lauf beschreiben (Clip-Name im AnimSet, Laenge, Haltungen), nicht hier bauen.
ORTE: schreiben NUR unter ${F}/. Lesen: ${W}, ${B}, ${T}, ${N}/_arbeit/baer_schlaf, ${N}/_arbeit/baer_de, Vanilla ${VAN}, Bandits, NPC Crew ${NC}/42/media/lua
und ${NC}/_docs (Beduerfnisse/Schlaf der Crew: nur lernen, nichts kopieren). Kein git, kein Download, nichts in Test-Mod/Staging/NPC Crew.
EISERNE REGEL fuer den spaeteren Bau: jeder Engine-Aufruf braucht eine Fundstelle mit gleichen Argumenttypen -- die Forschung liefert sie.`

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG. Bringe SCHLAF_PLAN.md auf den heutigen Code-Stand (F1-F2 haben Register, Hirn-Takt, Heilen, Kampf, Fenster veraendert): welche
Annahmen gelten noch, welche Fundstellen haben sich verschoben, was fehlt. Dazu: Wie fressen/trinken Tiere in Vanilla (AnimalData Hunger/Durst, Futter-
Trog, Wasser) -- nur belegte Lua-Wege; wie macht NPC Crew Hunger/Muedigkeit/Zuneigung ihrer Figuren (lernen); was bedeutet "Trust" fuer den Baeren
(Kevins Worte suchen, sonst Frage); wie wirken Beduerfnisse auf Faehigkeiten/Heilen/Kampf; MP-Weg. Ergebnis ${F}/FORSCHUNG_F3.md. Rueckgabe: Kurzfassung
mit Kernbelegen, Luecken und Fragen.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${F}/FORSCHUNG_F3.md und schreibe ${F}/PLAN_F3.md fuer den Bau-Lauf (nach baer-aussehen): Werte und Regeln je Beduerfnis
(steigen wie schnell, was senkt sie, Folgen bei hoch: Leben, Ausdauer, Lernen, Kampf, Weglaufen?), Schlafen (wann, wo, aufwachen, Heilen im Schlaf,
z Z z mit Farbe, Kampf geht vor), Fenster Variante B (aus dem Prototyp uebernehmen, inkl. Umbau der heutigen Karten), Balken ueber dem Kopf, Texte in
8 Sprachen, Sandbox (hoechstens 1-2 neue Regler, Gruppe), Register-Felder, Bench-Befehle, Attrappen, SP/MP, Uebernahme/Naehte, Schlafpose als eigener
Modell-Lauf. Bauer-Aufteilung KERN/OBERFLAECHE mit getrennten Dateien. Am Ende EINE kurze Frageliste fuer Kevin (hoechstens 6, je mit Empfehlung), die
SCHLAF_PLAN K1-K21 und ENTWURF F1-F9 zusammenfasst, soweit noch offen. Rueckgabe: Kurzfassung + die Frageliste.`, { label: 'plan', phase: 'Plan' })

return { fo, plan }
