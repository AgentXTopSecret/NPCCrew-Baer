export const meta = {
  name: 'baer-b1d',
  description: 'Baer-Junges B1d: Wachsen 100 Tage, taeglich steigende Werte, Faehigkeiten-Daten, Heil-Formeln, Anzeige -- 9 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Engine-Belege fuer Folgen, Namensschild, Umbenennen, Hinhalten, MP' },
    { title: 'Plan', detail: 'PLAN_B1D.md mit Schnittstelle Kern/Oberflaeche' },
    { title: 'Bau', detail: 'Kern (Server/shared) und Oberflaeche (Client, Texte) getrennt, dann Zusammenbau + Uebernahme-Skript' },
    { title: 'Pruefung', detail: 'Pruefer A Belege/Regeln/Texte, Pruefer B Logik/SP-MP/rote Linien' },
    { title: 'Nachbesserung', detail: 'bestaetigte Befunde beheben, alles neu pruefen' },
    { title: 'Gegenpruefung', detail: 'Urteil bereit fuer Kevins Test + Testanleitung' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-b1d" fuer Kevins Mod NPC Crew (Project Zomboid, Spiel laut Forschung 42.22.2; Bandits laedt aus ${BAN}/42.22
und ${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: B1a (finden, zaehmen), B1b (folgen, Namensschild) und B1c (Selbstheilung, Laerm, Verstecken, Mitfahren, Call to me, Gehen,
Markierung, Karten-Symbol, Optionen) sind gebaut, geprueft und seit 11.11. 08:12 in der Test-Mod ${T} (B1c ungespielt). Kevin hat B1a/B1b
gespielt (Zaehmen und Folgen klappen). Kevin schlaeft (Nachtschicht): keine Fragen, offene Punkte als "Fragen fuer Kevin" in den Bericht.
Kevins Entscheidungen WOERTLICH ganz unten in ${B}/begleiter/ENTSCHEIDUNGEN.md -- fuer diesen Lauf massgeblich: "Wachsen und Kampfkraft bis
ganz gross (Kevin 11.11.2026 ~00:20)", "Werte und Faehigkeiten des Baeren", "Muedigkeit und Schlafen", "Heilen", "Anzeige ueber dem Baeren",
dazu die alten Abschnitte zu Groessen/Stufen (Tabelle ganz oben: Jungtier 0,35 / Halbstark 0,75 / Erwachsen 1,35). ZUERST lesen.

AUFTRAG B1d WACHSEN (Kevins Freigabe Nachtschicht Punkt 4: "Wachsen 100 Tage + taeglich steigende Werte, Plan + Bau"):
1. WACHSEN: das GEZAEHMTE Junge waechst ab dem Zaehmen ueber Spieltage (Sandbox BanditsNPC.BearGrowDays, Vorgabe 100, 10..365) von 0,35 auf
   1,35; Kurve vorne schneller, hinten langsamer, Meilensteine bei Vorgabe ~Tag 15 = 0,75 (Halbstark), ~Tag 45 = 1,0, Tag 100 = 1,35 (bei
   anderer Sandbox-Zahl anteilig). Gutes Fuettern beschleunigt etwas (Kevin 08.11.), Hunger gibt es noch nicht -> Fuetter-Bonus klein und
   gedeckelt. Wilde Junge wachsen nicht. Groesse ueber den belegten Weg (setSizeForced, Vanilla ButcheringUtil.lua ~586 -- Seite pruefen) am
   Schreiber setzen; selten (z. B. je Spielstunde), nicht je Bild; ueberlebt Speichern/Laden, Mitfahren, Call to me, Register-Heilung (Spiegel v2
   um Alter/Groesse ergaenzen).
2. MODELLWECHSEL: das Junge-Modell wirkt nur bis etwa Halbstark richtig. Der Wechsel auf das Erwachsenen-Modell ist eine OFFENE Frage an Kevin
   (Junges- oder Erwachsenen-Modell fuer Halbstark?). In B1d deshalb: das Junge waechst mit seinem Modell bis zum Schwellwert (Stellwert,
   Vorgabe 0,75) und bleibt dort stehen (Groesse und Werte laufen intern weiter), Wechsel nur VORBEREITET (sauberer Haken, abgeschaltet), damit
   der spaetere Lauf ihn einschaltet. NICHT auf die alte Art "bear" wechseln (deren Kampf in NCBearFight.lua greift sofort voll an -- das ist
   B5a). Alte NCBear*-Dateien NICHT aendern.
3. WERTE, die JEDEN TAG mit der Groesse steigen (Kevin: "die werte von baeren muessen pro tag steigen"): Leben (max), Schaden (Faktor fuer
   spaeter), Ausdauer (max), Traglast (10 / 40 / 100 an den Stufen, dazwischen fliessend). Im Register fuehren, als Zahlen berechenbar
   (B.StatsOf o. ae.); Leben am Tier ueber einen belegten Weg setzen, falls es einen gibt (sonst nur fuehren und als Frage melden).
4. FAEHIGKEITEN (Stufe 0-10, Erfahrung durch Uebung, hinten langsamer): Agilitaet (eingesteckte Treffer -> Ausweichen 5 % .. 40 %),
   Leben-Bonus (eingesteckte Treffer), Kondition (Anstrengung: Rennen), Kaempfen (ausgeteilte Treffer -> +70 % Schaden auf Stufe 10), Fischen
   (ab Halbstark), Spuernase (Warnung, abschaltbar). In B1d nur DATEN, Formeln, Erfahrungs-Kurve und Haken bauen (Kondition kann schon durch
   Rennen beim Folgen steigen); Treffer/Kampf/Fischen/Spuernase-Verhalten kommen spaeter. Sandbox fuer Hoechstwerte (Ausweichen 40 %, Kaempfen
   70 %).
5. HEILEN-Vorbereitung: langsame Selbstheilung wach ~1 %/Spielstunde, im Schlaf ~15 %/Spielstunde (Kevin) als Formel + Sandbox; Schlaf gibt
   es noch nicht -> nur wach anwenden, wenn ein belegter Leben-Weg existiert.
6. ANZEIGE: in der vorhandenen Optionen-Seite (B1c) und im Namensschild die neuen Werte als waehlbare Zeilen anbieten (je Wert aus/Balken/Zahl,
   Kevin 11.11.) -- mindestens Leben und Ausdauer (wenn gefuehrt), dazu Alter/Groesse (z. B. "Tag 12 - halbstark in 3 Tagen") als Zeile.
7. BENCH: NCBear_CubGrow(tage) zum Vorspulen des Wachsens, NCBear_CubStats() zum Ausgeben (nur SP, nur Bench-Datei).
NICHT in B1d: Kampf, Zombie-Angriffe auf den Baeren, Schlafen, Fischen, Spuernase-Verhalten, Beduerfnisse, Inventar, Baeren-Fenster (V),
Modellwechsel einschalten, neues Modell, Aenderungen an alten NCBear*-Dateien.

ORTE: Staging (Pruefgegenstand und Bauort) ${W}/mod/ (spiegelt die Wurzel der Test-Mod; Liste ${W}/staging_dateien.txt). Plan, Berichte und
Forschung von B1a: ${W}/PLAN_ZAEHMEN.md, ${W}/forschung_engine.md (Abschnitte zu pathToLocation, respondToSound, Lure: Zeilen ~160-170,
~500-510, ~615-630), ${W}/forschung_bestand.md, ${W}/nachbesserung.md, ${W}/gegen_bericht.md, ${W}/schnittstelle_aenderungen.md.
Jar-Auszuege 42.22.2: ${W}/jar, ${W}/javap, ${W}/dec. Attrappen: ${W}/attrappe/ (kern/, ober/, gesamt/, pruef_b/; lua5.1:
C:/Users/Kevin/Tools/lua51/lua5.1.exe). Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py. Uebernahme-Skript ${B}/tools/baer_uebernahme.py, Naehte ${B}/NAEHTE.md.

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, Vanilla ${VAN} (nur lesen), Bandits ${BAN}/42.22 und
${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen; NPC Crew hat eigene Namensschilder
und Tier-Code -- zum Lernen lesen, nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Kevin kann jederzeit spielen). Kein git, kein
Spielstart, kein Download, nichts hochladen. EISERNE REGEL: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder
Bandits mit GLEICHEN Argumenttypen, im Kommentar genannt; Ausnahme nur mit Kevins Wort je Methode -- schon erteilt (08.11.) fuer
animal:pathToLocation(x, y, z) (siehe forschung_engine.md ~Zeile 627). Ein pcall um einen unbelegten Aufruf ist eine Tarnkappe. SP UND MP:
SP-Test "not isServer() and not isClient()"; was der Server wissen muss, kommt nie aus einem Client-Glauben; im SP tut sendServerCommand
nichts (direkt rufen). Kevins rote Linien: kein Gegenstand verloren oder verdoppelt, kein Kick (Rolle user, AntiCheat), nichts haengt endlos,
keine NPC-Crew-Figur wird gestoert. Testbefehle nur in NCBearBench*.lua (nur SP). Namen: BanditsNPCBear*.lua, Modul BanditsNPC.Bear, Texte
UI_BN_Bear_* in EN, PTBR, RU, KO, ES, CN, FR (CN nur Zeichen aus Vanilla-CN), Sandbox BanditsNPC.Bear*. Nichts Teures je Bild, Deckel fuer
alles, was waechst; Kahlua ist kein echtes Lua 5.1 (kein next). Dateien LF, ASCII in Lua. Schreibe "statisch geprueft, nicht gespielt";
keine Behauptung ohne Fundstelle (Datei:Zeile), sonst "ungeprueft".`

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

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG (nur lesen und belegen, kein Code im Staging). Lies zuerst ${W}/PLAN_B1C.md und ${W}/forschung_b1c.md (Register,
Spiegel v2, Takte). Belege fuer jeden Punkt 1-7 den Weg mit Fundstelle (Datei:Zeile, zitierte Zeile, Seite Client/Server/SP) in Vanilla bzw.
Bandits: Groesse eines lebenden Tiers aendern (setSizeForced/setSize, wo und auf welcher Seite; was die Engine dabei mit Modell, Geschwindigkeit,
Kollision, Futterbedarf macht; Jar-Auszuege ${W}/dec und ${W}/jar), Alter/Stufen der Engine (AnimalData, ageToGrow, grow -- warum wir NICHT die
Engine-Stufen nutzen), Leben eines Tiers lesen/setzen (getHealth/setHealth am IsoAnimal mit Beleg?), Traglast-Begriff (spaeter Inventar),
wie NPC Crew Skill-Erfahrung und -Stufen fuehrt (${NC}/42/media/lua/shared/BanditsNPCSkills.lua -- lernen, nicht kopieren), Optionen-Seite
aus B1c erweitern.
Ergebnis: ${W}/forschung_b1d.md (Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil; was NUR mit Jar belegt ist, getrennt markiert;
offene Fragen). Rueckgabe: Kurzfassung mit den Kernbelegen und den Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung_b1d.md ganz, dazu ${W}/PLAN_ZAEHMEN.md, ${W}/PLAN_B1B.md und ${W}/PLAN_B1C.md (Aufbau der Dateien, Register,
Sicht/Sync, Zeitaktionen, Folgen) und die Staging-Dateien, die B1c beruehrt. Schreibe ${W}/PLAN_B1D.md:
1. Je Auftragspunkt 1-7 das Verhalten Schritt fuer Schritt mit Meldungen, Speichern/Laden, Tod, Besitzer offline im MP, zweiter Spieler;
   Zahlen als Stellwerte/Sandbox-Optionen mit Vorgaben (Kevins Vorgaben aus dem Auftrag woertlich uebernehmen: 100 Tage, Meilensteine 15/45/100,
   Ausweichen 5-40 %, Kaempfen +70 %, Heilen 1 %/15 %, Traglast 10/40/100, ...).
2. Register-Selbstheilung: Felder des Spiegels, Version, Wiederherstellungs-Regeln, Konflikte (zwei Tiere/ein Eintrag, Eintrag/fremdes Tier).
3. Mitfahren und Unstuck: Zustandsmaschine (follow -> riding -> zurueck), was im Register steht, welche Tier-Daten verloren gehen und warum
   das ok ist; was passiert bei Speichern waehrend der Fahrt, Tod des Besitzers im Auto, Absturz.
4. Markierung, Karten-Symbol, Anzeige-Optionen: Daten aus der Sicht, Kosten je Bild, Deckel, Bandits-Riegel.
5. GENAUE SCHNITTSTELLE fuer zwei getrennte Bauer: KERN (shared/ und server/) und OBERFLAECHE (client/, Translate in 7 Sprachen,
   Sandbox-Texte, Bench-Erweiterung, Bild 42/media/ui/BanditsNPCBearCub_marker.png). Jede Funktion mit Name, Parametern, Rueckgabe, Datei.
   Wer welche Datei schreibt (keine Datei fuer beide).
6. Testfaelle fuer die Attrappen (SP und MP-Rundlauf) und Kevins Testschritte.
7. Belege: jeder geplante Engine-Aufruf mit Fundstelle aus forschung_b1d.md; Jar-only-Aufrufe sind verboten, ausser den von Kevin
   freigegebenen (pathToLocation, setVariable("animalRunning", ...) am Tier).
Rueckgabe: Kurzfassung des Plans mit Dateiliste je Bauer.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua). Setze ${W}/PLAN_B1D.md fuer deinen Teil WOERTLICH um;
musst du von der Schnittstelle abweichen, sofort nach ${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "B1d KERN") und die Datei vor dem
Abschluss lesen. Client-Dateien (lua/client/, Translate, Bench) gehoeren dem anderen Bauer: nur lesen. Jeder Engine-Aufruf mit Fundstelle im
Kommentar (selbst nachgeprueft). Diagnose hinter dem bestehenden Schalter. Danach: vier Lua-Pruefer auf deine Dateien, Zeilenenden, die
bestehenden Attrappen (kern/, gesamt/) muessen weiter laufen (Attrappe nur anpassen, wenn der Code sich gewollt aendert, begruenden), neue
Attrappen-Faelle fuer Folgen/Bleiben/Umbenennen/Waisen unter ${W}/attrappe/b1d_kern/.
Ergebnis: ${W}/bau_b1d_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je
Vorgang, Pruefer-Ausgaben, Attrappen-Ergebnis, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/ und Bench NCBearBenchCub.lua, Translate in sieben Sprachen, Sandbox-Texte, im Staging
${W}/mod/42/media/lua). Setze ${W}/PLAN_B1D.md fuer deinen Teil WOERTLICH um; Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md
ANHAENGEN (Abschnitt "B1d OBERFLAECHE"), vor dem Abschluss lesen. shared/ und server/ gehoeren dem anderen Bauer: nur lesen. Das Schild
muss billig sein (nichts Teures je Bild, Liste selten erneuert). Texte natuerlich je Sprache, gleiche Platzhalter, JSON-Round-Trip
(json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende), sortiert, CN nur Vanilla-CN-Zeichen (pruefen). Danach: vier Lua-Pruefer,
Zeilenenden, bestehende Attrappen (ober/, gesamt/) weiter gruen, neue Faelle unter ${W}/attrappe/b1d_ober/.
Ergebnis: ${W}/bau_b1d_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt,
Pruefer-Ausgaben, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UEBERNAHME. Zwei Bauer haben getrennt gebaut (Berichte ${W}/bau_b1d_kern.md, ${W}/bau_b1d_oberflaeche.md,
Abweichungen ${W}/schnittstelle_aenderungen.md). 1. Pruefe das Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl
hat Empfaenger, Sicht-Felder passen, jeder Textschluessel in EN und allen Sprachen, Ersatztexte wortgleich) -- Werkzeug wie
${W}/attrappe/gesamt/xref.py; Luecken klein und belegt schliessen. 2. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um B1d erweitern (Zaehmen -> Tag 0; 15/45/100 Tage vorspulen -> Groesse und Werte an den
Meilensteinen; Schwellwert 0,75 haelt das Modell; Speichern/Laden, Mitfahren, Call to me und Register-Heilung behalten Alter/Groesse/Werte;
Sandbox-Tage 30 und 365; Kondition durch Rennen; Anzeige-Zeilen) und laufen lassen; die bestehenden B1a/B1b-Faelle muessen gruen bleiben. 3. ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md nachziehen (neue Dateien/Texte/Optionen,
Cheat-Pruefung), Trockenlauf und --probe (mit --vor-b5a, Probe nur unter ${W}/probe_b1d/). 4. ${W}/staging_dateien.txt neu (Pfad | MD5 |
Bytes | neu/ueberschreibt gegen ${T}) und ${W}/mod_info_vorschlag.txt um B1d ergaenzen.
Ergebnis: ${W}/bau_b1d_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { fo, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in B1d
geaenderten oder neuen Dateien (Liste aus ${W}/bau_b1d_zusammenbau.md und staging_dateien.txt): jeder Engine-Aufruf gegen die genannte
Fundstelle im heutigen Vanilla/Bandits (Datei, Zeile, Argumenttypen, Seite), Jar-only ausser pathToLocation = Befund; keine Testbefehle
ausserhalb der Bench; Namen und Kollisionen gegen NPC Crew und Vanilla; Texte in sieben Sprachen (Schluessel, Platzhalter, Round-Trip, CN);
Sandbox-Optionen mit Texten und Benutzung; Uebernahme-Skript Trockenlauf/Probe selbst laufen lassen; vier Lua-Pruefer und alle Attrappen
selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_b1d_a.md. Rueckgabe strukturiert (id A1...).`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/pruef_b1d/. Lies den Code ganz und verfolge: Wachsen (Kurve, Meilensteine, andere Sandbox-Tage, Rundung, Zeitspruenge durch Schlafen/Vorspulen,
Speichern/Laden, Mitfahren, Call to me, Heilung aus dem Spiegel), Groesse setzen (Seite, Haeufigkeit, Wirkung auf Kollision/Geschwindigkeit/
Folgen), Werte und Faehigkeiten (Formeln, Deckel, Erfahrungskurve, nichts waechst ohne Grenze), Anzeige (Kosten je Bild), Zusammenspiel mit
B1a-B1c -- alles im SP-Zweig und im MP-Zweig. Drei eigene Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_b1d_b.md. Rueckgabe
strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_b1d_a.md, ${W}/pruef_b1d_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine
neuen unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in ${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES
neu: vier Lua-Pruefer auf alle Lua-Dateien des Stagings, Zeilenenden/ASCII, JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe
(--vor-b5a), ${W}/staging_dateien.txt neu. Ergebnis ${W}/nachbesserung_b1d.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_b1d.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (--vor-b5a). staging_dateien.txt gegen
   die Platte nachzaehlen; nachweisen, welche bestehenden Dateien der Test-Mod ueberschrieben wuerden (nur gewollte).
3. Zwei eigene Stichproben (z. B. Folgen im MP-Zweig Zeile fuer Zeile; eine Sprache ganz gegengelesen).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; gezaehmtes Junges waechst mit NCBear_CubGrow sichtbar bis
   zum Schwellwert, Werte steigen, Anzeige zeigt Alter/Leben/Ausdauer; B1a-B1c unveraendert)? Blocker nur, was diesen Test verhindert oder
   eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_b1d.md und Testanleitung ${W}/anleitung_b1d_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit
Bench-Befehlen zum Eintippen; Debug-"Tier Cheat" vorher ausschalten; Bandits muss fuer die Markierung geladen sein). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, zus, pa, pb, fix, gegen }
