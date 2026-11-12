export const meta = {
  name: 'baer-f2-fortsetzung',
  description: 'Baer F2 FORTSETZUNG ohne Lauf-Cache (fuer einen neuen Account/eine neue Sitzung): Forschung und Plan sind fertig auf der Platte (forschung_f2_*.md, PLAN_F2.md mit Abschnitt 11), es geht ab Bau weiter -- 7 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Gegner-Weg (Biss nachbauen, Banditen), Bestand NCBearFight + Umbenennen' },
    { title: 'Plan', detail: 'PLAN_F2.md mit Schnittstelle Kern/Oberflaeche' },
    { title: 'Bau', detail: 'Kern und Oberflaeche getrennt, dann Zusammenbau + Umbenennen + Uebernahme-Skript' },
    { title: 'Pruefung', detail: 'Pruefer A Belege/Regeln/Texte, Pruefer B Logik/SP-MP/rote Linien' },
    { title: 'Nachbesserung', detail: 'bestaetigte Befunde beheben, alles neu pruefen' },
    { title: 'Gegenpruefung', detail: 'Urteil bereit fuer Kevins Test + Testanleitung' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const A = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-f2" (= B5a Kampf) fuer Kevins Mod NPC Crew (Project Zomboid, Spiel 42.22.2; Bandits laedt aus ${BAN}/42.22
und ${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: Das gezaehmte Junge (Art "ncbearcub") und ab Tag 15 der grosse Koerper (Art "ncbeargrown", Helfer B.BodyKind) sind in
B1a-B1e gebaut; F1 (Baeren-Fenster auf V mit Werten, Faehigkeiten, Befehlen Folgen/Bleiben/Sitz/Frei/Komm her/Passiv/Unstuck, C1-Wiederkehr)
ist gebaut und geprueft und liegt im Staging ${W}/mod/ (67 Dateien, Liste ${W}/staging_dateien.txt; Berichte PLAN_F1.md, gegen_bericht_f1.md).
ACHTUNG: Die Test-Mod ${T} hat F1 NOCH NICHT (Claude baut F1 ein, sobald Kevins Spiel zu ist) -- dein Bezugsstand ist das STAGING; vergleiche
gegen die Test-Mod nur fuer die alten NCBear*-Dateien. Daneben gibt es in der Test-Mod den alten Kampf-Test: Art "bear" mit NCBearFight.lua
(Prankenhieb links/rechts, Biss, Biss am Boden, Doppelschlag, Rueckstoss, Schnauben, Sitzen/Fressen; Testbefehle NCBear_*; Lehren in
${B}/spiel/*.md und ${B}/STAND.md). Der grosse Baer bekommt parallel im Lauf baer-gross neue Clips (Aufrichten/Bruellen) -- Modell-, Textur-,
Ton- und AnimSet-Dateien fasst F2 NICHT an; Clip-Zeiten nur aus EINER Tabelle lesen, damit sie nach baer-gross nachgezogen werden koennen.
NACHTSCHICHT: keine Fragen an Kevin waehrend des Laufs; offene Kleinfragen mit dem EMPFOHLENEN Weg bauen und als "Fragen fuer Kevin" in den
Bericht. Kevin (11.11. ~18:40): "alle funktionen einbauen noch vom baeren du weisst ja bescheid was ich alels wollte die ganzen skills das
schoene ui und alles". Seine Wuensche: ${B}/begleiter/ENTSCHEIDUNGEN.md -- ZUERST lesen: "Tod", "Gegner wehren sich", "Probe im Spiel
(08.11. ~01:20)" (Weg 1 echt geht NICHT -> Weg 2 Biss nachbauen), "Befehle, Sitzen, Fressen (08.11.)" (Kampf hat Vorrang, Passiv, Jungtier
kaempft nie), Umbenennen (Zeile ~101), "Werte und Faehigkeiten (11.11. ~00:30)" mit Agilitaet/Leben/Kondition/Kaempfen (+70 % auf Stufe 10),
"Laerm, Zombies und das Junge (11.11. ~01:50)" ("ja nur ungetamte greifen die nicht an"), "Heilen (11.11. ~01:55)", Nachtschicht-Freigaben.

AUFTRAG F2:
1. UMBENENNEN zuerst (Kevins Ja): die alten Lua-Dateien NCBear*.lua (ausser NCBearBench*) bekommen NPC-Crew-Namen BanditsNPCBear*, Modul
   BanditsNPC.Bear, Texte UI_BN_Bear_* (7 Sprachen), Sandbox BanditsNPC.Bear*; die Test-Art "bear" wird "ncbear" (Kollisionsprobe). Modell-,
   Textur-, Ton-, AnimSet- und Modell-Skript-Dateinamen bleiben (gleiche relative Pfade). Testbefehle wandern in NCBearBench*.lua. In der
   Test-Mod wird beim Einbau nur hinzugefuegt/ueberschrieben, nie geloescht: eine alte Datei, die umbenannt wurde, wird im Staging als
   Stummel gleichen Namens gefuehrt (nur Kommentar "umbenannt nach ...", kein Code), damit nichts doppelt laedt. Die Uebernahme nach NPC Crew
   kopiert Stummel nie.
2. GEGNER: Zombies greifen JEDEN gezaehmten Baeren an (Junges und grosser Koerper), ungezaehmte nie; Weg 2 "nachgebaut": Zombie in der Naehe
   laeuft hin (spotted/setTarget-Annaeherung aus der Probe), Biss/Schlag selbst gerechnet mit belegter Zombie-Angriffs-Animation (Fundstelle!),
   Ton, Blut, Schaden per eigenem Code; mehrere Zombies gleichzeitig mit Deckel. Feindliche Banditen (nur hostile, Bandits' eigene Liste, belegt)
   greifen ihn ebenfalls an, Schaden selbst rechnen. Crew, Neutrale und Spieler greifen ihn nie an. Ohne Bandits muss alles laufen.
3. DER BAER KAEMPFT: ab Halbstark (grosser Koerper) mit dem Kampf-Werkzeug aus NCBearFight (umbenannt), Kampf hat Vorrang vor jedem Befehl,
   danach zurueck zum Befehl (Folgen/Bleiben/Sitz/Frei); Passiv (F1-Schalter): kaempft nicht, zieht sich zum Besitzer zurueck; das Junge kaempft
   nie (versteckt sich, B1c). Nie gegen Spieler, Crew, Neutrale oder Tiere. Mitfahren/Call to me/Unstuck/Tausch Tag 15 bleiben sicher.
4. FAEHIGKEITEN WIRKEN (B1d-Daten, Formeln aus ENTSCHEIDUNGEN): Agilitaet = Ausweich-Chance 5-40 % (steigt mit eingesteckten Treffern), Leben =
   Bonus aus eingesteckten Treffern, Kondition = mehr Ausdauer/schneller verschnaufen (steigt beim Rennen/Kaempfen/ausser Puste), Kaempfen = +70 %
   Schaden auf Stufe 10 (steigt mit ausgeteilten Treffern). Ausdauer sinkt im Kampf; leer -> kurz verschnaufen/zurueckziehen. Werte im
   F1-Fenster zeigen den Kampfzustand.
5. TOD UND FLIEHEN: er kann sterben (Kevin); Sandbox "Bear cannot die" (Vorgabe AUS): dann "downed" und der Besitzer hilft ihm auf (wie die
   NPC-Crew-Figuren, Weg dort nur lesen). Empfohlen (Claudes Vorschlag, Kevins Wort fehlt): bei wenig Leben (Sandbox, Vorgabe 20 %) flieht er
   zum Besitzer statt weiterzukaempfen. Tod: Register sauber, Meldung, nichts verdoppelt/verloren (Inventar gibt es noch nicht).
6. HEILEN VON HAND (Kevin: "wir koennen den baeren manuel heilen"): Vorschlag bauen -- Verband (Vanilla-Gegenstaende, belegt) am Baeren anlegen
   per Rechtsklick und im F1-Fenster: verbraucht genau einen Gegenstand (nie doppelt, nie verloren bei Abbruch), heilt deutlich schneller als die
   Selbstheilung; Werte als Sandbox. NPC-Heiler nur als Naht dokumentieren.
7. BENCH (nur NCBearBench*, nur SP): Zombie neben den Baeren holen, Kampf-Log, Leben setzen -- nur Testhilfe.
NICHT in F2: Hunger/Durst/Schlaf (F3), Inventar (F4), Spuernase/Fischen (F5), Modell-/Clip-Dateien, NPC-Heiler-Job.

ORTE: Staging ${W}/mod/ (Bauort). Frueheres Wissen: ${A}/baer_angriff/ (Jar-Auszuege zu AttackState, IsoZombie, Pakete, bandit_tools),
${A}/baer_kampf/, ${B}/spiel/*.md, Jar-Auszuege ${W}/jar, ${W}/javap, ${W}/dec, ${W}/jar_f1. Attrappen ${W}/attrappe/ (lua5.1:
C:/Users/Kevin/Tools/lua51/lua5.1.exe). Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py. Uebernahme-Skript ${B}/tools/baer_uebernahme.py (Trockenlauf/--probe mit --vor-b5a; F2 ist B5a: am Ende soll der Trockenlauf
OHNE --vor-b5a gruen sein, soweit nur Altlasten betroffen sind, die F2 ersetzt), Naehte ${B}/NAEHTE.md.

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${A}/baer_angriff, ${A}/baer_kampf, ${B}, Vanilla ${VAN}
(nur lesen), Bandits ${BAN}/42.22 und ${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen,
nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Claude baut nach der Pruefung selbst ein). Kein git, kein
Spielstart, kein Download, nichts hochladen. EISERNE REGEL: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder
Bandits mit GLEICHEN Argumenttypen, im Kommentar genannt; Ausnahme nur mit Kevins Wort je Methode -- erteilt fuer animal:pathToLocation(x, y, z)
und setVariable("animalRunning", ...) am Tier. Ein pcall um einen unbelegten Aufruf ist eine Tarnkappe. Nichts aus Bandits oder NPC Crew
kopieren (lernen ja). SP UND MP: SP-Test "not isServer() and not isClient()"; Schaden und Tod rechnet der Server; was der Server wissen muss,
kommt nie aus einem Client-Glauben; MP ehrlich als offen markieren, wo es nicht geht. Kevins rote Linien: kein Gegenstand verloren oder
verdoppelt, kein Kick (Rolle user, AntiCheat), nichts haengt endlos, keine NPC-Crew-Figur wird gestoert; der Baer geht nie verloren und wird nie
verdoppelt (ausser durch echten Tod). Testbefehle nur in NCBearBench*.lua (nur SP). Namen wie oben; vor jedem neuen Namen in NPC Crew greppen.
Nichts Teures je Bild (Zombie-Suche gedrosselt, Deckel); Kahlua ist kein echtes Lua 5.1 (kein next). Dateien LF, ASCII in Lua; localcount aktiv
UND insgesamt unter 180 (sonst teilen). Schreibe "statisch geprueft, nicht gespielt"; keine Behauptung ohne Fundstelle (Datei:Zeile).`

const FIND = {
  type: 'object',
  properties: {
    zusammenfassung: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] },
          datei: { type: 'string' },
          zeile: { type: 'string' },
          behauptung: { type: 'string' },
          beleg: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['id', 'schwere', 'datei', 'behauptung', 'beleg', 'vorschlag'],
      },
    },
  },
  required: ['zusammenfassung', 'findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    bereit_fuer_sp_test: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    offene_blocker: { type: 'array', items: { type: 'string' } },
    restbefunde: { type: 'array', items: { type: 'string' } },
    befunde_geschlossen: { type: 'integer' },
    befunde_offen: { type: 'integer' },
    staging_dateien: { type: 'integer' },
    pruefer_ausgaben: { type: 'string' },
    fragen_an_kevin: { type: 'array', items: { type: 'string' } },
  },
  required: ['bereit_fuer_sp_test', 'zusammenfassung', 'offene_blocker', 'restbefunde', 'staging_dateien', 'pruefer_ausgaben'],
}

// FORTSETZUNG (12.11.2026): Forschung A/B und Plan liefen im Lauf wf_6651b1ca-2f2 (alte Sitzung) und liegen als Dateien vor.
// Der Lauf-Cache gilt nur in der alten Sitzung -- deshalb hier ohne diese drei Agenten, die Bauer lesen die Berichte selbst.
const foA = `Forschung Gegner ist fertig: ${W}/forschung_f2_gegner.md (ganz lesen).`
const foB = `Forschung Bestand ist fertig: ${W}/forschung_f2_bestand.md (ganz lesen).`
const plan = `Plan ist fertig: ${W}/PLAN_F2.md (ganz lesen, inkl. Abschnitt 11 Nachtraege Kevin 12.11.).`
log('Fortsetzung ab Bau: Forschung und Plan aus Dateien')

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua, dazu Defs/Sandbox-Optionen, falls der Plan sie dem Kern gibt).
Zuerst Staging gegen staging_dateien.txt nachzaehlen (MD5). Setze ${W}/PLAN_F2.md fuer deinen Teil WOERTLICH um; Abweichungen sofort nach
${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "F2 KERN"), vor dem Abschluss lesen. Client-Dateien gehoeren dem anderen Bauer: nur lesen.
Jeder Engine-Aufruf mit Fundstelle im Kommentar (selbst nachgeprueft). Diagnose hinter dem bestehenden Schalter. Danach: vier Lua-Pruefer,
Zeilenenden, alle bestehenden Attrappen bleiben gruen (nur gewollt anpassen, begruenden), neue Faelle unter ${W}/attrappe/f2_kern/.
Ergebnis: ${W}/bau_f2_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle, SP-/MP-Zweig, Pruefer-Ausgaben, offen).
Rueckgabe: Kurzfassung. FORTSETZUNG nach Halt 03:58 (5-h-Limit): Zwischenstaende im Staging und in ${W} pruefen, nur Vollstaendiges weiterverwenden. Dazu 12.11. ~04:30 (Kevin: 'Ja, wie NPC Crew'): in shared/BanditsNPCBear.lua steht in B.T 'Fix 3' (Existenzfrage per pcall(getTextOrNull, key, "%1".."%9"), Jar-Ausnahme begleiter/ENTSCHEIDUNGEN.md) -- NICHT zuruecknehmen, mit uebernehmen. Dazu (12.11. ~04:45, Kevin: E in der Naehe statt V): der Lauf baer-f1b hat seine Aenderungen (nur client/ und Translate/: Nah-Taste E, Fern-Taste, V-Rueckbau) in dieses Staging zusammengefuehrt -- Liste ${W}/f1b_merge.md; diese Stellen sind gewollt, NICHT zuruecknehmen, und F2 legt KEINE eigene V-Taste an. NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/, Bench NCBearBench*.lua, Translate in sieben Sprachen, Sandbox-Texte; Staging
${W}/mod/42/media/lua). Setze ${W}/PLAN_F2.md fuer deinen Teil WOERTLICH um (Fenster-Ergaenzungen im Stil von F1, Entwurf
${W}/f1_entwurf/fenster_gebaut_*.png; Rechtsklick; Heilen-Aktion; Meldungen; Bench). Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md
ANHAENGEN (Abschnitt "F2 OBERFLAECHE"), vor dem Abschluss lesen. shared/ und server/ gehoeren dem anderen Bauer: nur lesen. Texte natuerlich je
Sprache, gleiche Platzhalter, JSON-Round-Trip (json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende), sortiert, CN nur Vanilla-CN-Zeichen.
Danach: vier Lua-Pruefer, Zeilenenden, alle bestehenden Attrappen gruen, neue Faelle unter ${W}/attrappe/f2_ober/; geaendertes Fenster als
${W}/f1_entwurf/fenster_f2_1080.png neu zeichnen (PIL, Masse/Farben wie im Code). Ergebnis: ${W}/bau_f2_oberflaeche.md. Rueckgabe: Kurzfassung. FORTSETZUNG nach Halt 03:58 (5-h-Limit): Zwischenstaende im Staging und in ${W} pruefen, nur Vollstaendiges weiterverwenden. Dazu 12.11. ~04:30 (Kevin: 'Ja, wie NPC Crew'): in shared/BanditsNPCBear.lua steht in B.T 'Fix 3' (Existenzfrage per pcall(getTextOrNull, key, "%1".."%9"), Jar-Ausnahme begleiter/ENTSCHEIDUNGEN.md) -- NICHT zuruecknehmen, mit uebernehmen. Dazu (12.11. ~04:45, Kevin: E in der Naehe statt V): der Lauf baer-f1b hat seine Aenderungen (nur client/ und Translate/: Nah-Taste E, Fern-Taste, V-Rueckbau) in dieses Staging zusammengefuehrt -- Liste ${W}/f1b_merge.md; diese Stellen sind gewollt, NICHT zuruecknehmen, und F2 legt KEINE eigene V-Taste an. NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { foA, foB, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UMBENENNEN + UEBERNAHME. Berichte ${W}/bau_f2_kern.md, ${W}/bau_f2_oberflaeche.md, Abweichungen
${W}/schnittstelle_aenderungen.md. 1. Zusammenpassen ueber die Grenze pruefen (xref wie ${W}/attrappe/gesamt/xref.py; jede B.*-Benutzung
definiert, jeder Befehl mit Empfaenger, Textschluessel in allen Sprachen) und Luecken klein und belegt schliessen. 2. Umbenennen abschliessen:
umbenannte Dateien im Staging, Stummel fuer die alten Namen, keine Datei laedt doppelt, Bench-Befehle nur in NCBearBench*; die alten NCBear*-
Testbefehle, die Kevin kennt (NCBear_SpawnLive, NCBear_Fight, NCBear_Sit, NCBear_Stand, NCBear_AnimTest, NCBear_Huff, NCBear_Vergleich,
NCBear_GenLive ...), laufen weiter. 3. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um F2 erweitern und laufen lassen; alle B1a-F1-Faelle bleiben
gruen. 4. ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md nachziehen (Umbenennen, Stummel nie kopieren, Altlasten, die F2 abloest, aus der
--vor-b5a-Liste; Cheat-Pruefung), Trockenlauf und --probe (mit und ohne --vor-b5a, Probe nur unter ${W}/probe_f2/).
5. ${W}/staging_dateien.txt neu (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen ${T} -- Achtung: F1 ist dort noch nicht eingebaut, Spalte
gilt gegen die heutige Test-Mod) und ${W}/mod_info_vorschlag.txt um F1 und F2. Ergebnis: ${W}/bau_f2_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen. NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { foA, foB, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme, Umbenennen. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle
in F2 geaenderten/neuen Dateien: jeder Engine-Aufruf gegen die genannte Fundstelle (Datei, Zeile, Argumenttypen, Seite), Jar-only = Befund
(ausser pathToLocation/animalRunning); nichts aus Bandits/NPC Crew kopiert; Umbenenn-Tabelle vollstaendig, kein doppeltes Laden, Stummel ohne
Code; keine Testbefehle ausserhalb der Bench; Texte in sieben Sprachen; Sandbox-Optionen vollstaendig; Uebernahme-Skript Trockenlauf/Probe selbst
laufen lassen; vier Lua-Pruefer und alle Attrappen selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_f2_a.md. Rueckgabe strukturiert (id A1...). NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/pruef_f2/. Verfolge: Zombie(s) gegen Junges und grossen Baeren (versteckt, folgt, bleibt, sitzt, frei, faehrt mit, Call/Unstuck,
Tausch Tag 15 mitten im Kampf, Besitzer offline/tot, Speichern/Laden im Kampf); wilde Baeren werden nie angegriffen; der Baer greift nie Spieler/
Crew/Neutrale/Tiere an; Passiv; Fliehen; Tod/downed/aufhelfen (kann er verloren gehen oder doppelt entstehen?); Verband genau einmal verbraucht,
auch bei Abbruch; Formeln (Ausweichen 5-40 %, +70 % auf Stufe 10) nachrechnen; Kosten je Bild mit 50 Zombies in der Naehe; MP-Zweig. Drei eigene
Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_f2_b.md. Rueckgabe strukturiert (id B1...). NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { foA, foB, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_f2_a.md, ${W}/pruef_f2_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine neuen
unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in ${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES neu:
vier Lua-Pruefer, Zeilenenden/ASCII, JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe, ${W}/staging_dateien.txt neu.
Ergebnis ${W}/nachbesserung_f2.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen. NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { foA, foB, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_f2.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe. staging_dateien.txt gegen die Platte
   nachzaehlen; nachweisen, welche Dateien der Test-Mod ueberschrieben und welche durch Stummel ersetzt wuerden (nur gewollte).
3. Zwei eigene Stichproben (z. B. Zombie beisst den grossen Baeren, der kaempft, flieht bei wenig Leben -- Zeile fuer Zeile; Tod waehrend
   Mitfahren; Verband abgebrochen).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; Zombies greifen den gezaehmten Baeren an, er wehrt sich,
   Junges versteckt sich, Passiv wirkt, Werte/Faehigkeiten steigen sichtbar im V-Fenster, Verband heilt, Tod bzw. downed sauber; alte Testbefehle
   laufen weiter; B1a-F1 unveraendert)? Blocker nur, was diesen Test verhindert oder eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_f2.md und Testanleitung ${W}/anleitung_f2_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit Bench-
Befehlen zum Eintippen; Spiel mit -debug neu starten; Wegwerf-Spielstand; F1 muss vorher eingebaut sein). Rueckgabe: das Urteil strukturiert. NACHTRAG KEVIN 12.11. ~05:00: ${W}/PLAN_F2.md Abschnitt 11 (11.1 Schalter 'Show damage' mit schwebenden Schadenszahlen ueber Zombies/Banditen, 11.2 Zeile 'Melee damage' unter Condition mit B.MeleeDamage, 11.4 Lerntempo langsamer + Alters-Deckel + Sandbox-Prozent, 11.5 Kill-Zaehler, 11.6 kein Schaden durch Spieler/Turrets/NPCs + Bench-Fehler %1$s, 11.7 Fliehen erst N=3 Treffer vor dem Tod statt 20 %) gehoert zum Auftrag -- umsetzen bzw. mitpruefen.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { foA, foB, plan, kern, ober, zus, pa, pb, fix, gegen }
