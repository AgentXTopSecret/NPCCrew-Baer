export const meta = {
  name: 'baer-b1b-folgen',
  description: 'Baer-Junges B1b: Folgen/Bleiben, Namensschild, Futter hinhalten, Waisen-Aufraeumen -- Forschung, Plan, Bau (2), Zusammenbau, Pruefer (2), Nachbesserung, Gegenpruefer (10 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Forschung', detail: 'Engine-Belege fuer Folgen, Namensschild, Umbenennen, Hinhalten, MP' },
    { title: 'Plan', detail: 'PLAN_B1B.md mit Schnittstelle Kern/Oberflaeche' },
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

const CTX = `Du arbeitest im Lauf "baer-b1b" fuer Kevins Mod NPC Crew (Project Zomboid, Spiel laut Forschung 42.22.2; Bandits laedt aus ${BAN}/42.22
und ${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: Version B1a (Baeren-Junges finden und zaehmen, Tierart ncbearcub) ist gebaut, geprueft und seit 10.11. in der Test-Mod ${T};
Kevin hat sie am 10.11. abends gespielt: Junges erscheint (nach Fix 1), flieht ohne Futter, Fuettern und Streicheln erhoehen den Zaehm-Balken,
Zaehmen klappt. Seine Rueckmeldungen woertlich ganz unten in ${B}/begleiter/ENTSCHEIDUNGEN.md (Abschnitt "Erster Spieltest B1a" und folgende),
die Befunde N5-N8 und Fix 1-3 ganz oben in ${B}/STAND.md -- beides ZUERST lesen. Nach dem Zaehmen kann das Junge noch nichts; Kevin
(woertlich): "kann jz nichtmehr mit dem machen also da steht auch nicht ueber den baeren das es meiner ist" und auf die Frage, was zuerst
kommen soll: "Folgen + Namensschild".

AUFTRAG B1b (Umfang fest):
1. FOLGEN / BLEIBEN: Am eigenen, gezaehmten Jungen Rechtsklick "Follow me" bzw. "Stay here" (Umschalter). Folgen: das Junge laeuft dem
   Besitzer hinterher (Abstand etwa 2-4 Kacheln, rennt mit, wenn er rennt), sucht sich neu den Weg, wenn er weiterzieht; ist der Besitzer im
   Auto, zu weit weg (Deckel als Sandbox-Option) oder ausser geladener Gegend, bleibt es stehen und wechselt mit Meldung auf "Bleiben".
   Bleiben: bleibt in der Gegend (kleiner Radius). Zustand ueberlebt Speichern/Laden und gilt im SP und im MP (Server rechnet).
2. NAMENSSCHILD: ueber dem eigenen Jungen ein Schild wie ein Namensschild: Zeile 1 der Name (Vorgabe, solange nicht benannt: z. B.
   "<Spielername>'s cub" in EN, je Sprache natuerlich), Zeile 2 klein der Zustand ("following" / "staying"). Fremde Junge im MP zeigen
   Name und Besitzer. Schild dicht ueber dem Kopf des Jungen (Kevin fand den Balken zu hoch ueber dem kleinen Jungen), Hoehe als
   Stellwert. Sichtbar in der Naehe, billig zu zeichnen (nichts Teures je Bild). Der Zaehm-Balken (vor dem Zaehmen) und das Schild
   (danach) sitzen an derselben Stelle.
3. UMBENENNEN: Rechtsklick "Name the cub" mit Texteingabe (Vanilla-Eingabefenster mit Beleg), Laenge begrenzt, nur druckbare Zeichen,
   im MP prueft der Server und verteilt.
4. FUTTER HINHALTEN (N6/N8): Weil Vanilla fuer Essen kein Ausruesten anbietet und der Rechtsklick am Tier nur aus der Naehe geht, musste
   Kevin das scheue Junge jagen. Neu: ein Weg, Futter in die Hand zu nehmen, ohne das Tier anzuklicken (z. B. Welt-Rechtsklick "Hold out
   food for the cub" mit Untermenue der Futtersorten, wenn ein eigenes oder scheues Junges in der Naehe ist; Vanilla
   ISWorldObjectContextMenu.equip wie client/BanditsNPCBearMenu.lua:79). Danach greift die bestehende Regel "Futter in der Hand ->
   Junges bleibt stehen / kommt naeher". Vanillas eigenes Locken ("ContextMenu_Lure", eatFromLured) NICHT verwenden: das liesse das Tier
   an Register und Balken vorbei fressen.
5. N5 WAISEN: ein ncbearcub ohne Spiegel und ohne passenden Register-Eintrag wird unbeobachtet entfernt (wie der stale-Zweig in
   B.ScanAnimals), damit Reste nach Fehlern/Abstuerzen nicht ewig herumstehen.
6. Fix 2 (Text-Warnungen, tHas-Zwischenspeicher in B.T) und Fix 3 (Streichel-Ton petting = PetAnimalCalf) sind SCHON im Staging -- nicht
   zurueckbauen. Das Streicheln selbst (Haltung, Abstand) bleibt wie es ist (Kevin: "lass das einfach so").
NICHT in B1b: Wachsen, Kampf/Gegenwehr, Inventar, Beduerfnisse, Schlafen, Baeren-Fenster (V-Taste), Mitfahren im Auto, Befehle an
NPC-Crew-Figuren, Umbenennen der alten NCBear*-Dateien.

ORTE: Staging (Pruefgegenstand und Bauort) ${W}/mod/ (spiegelt die Wurzel der Test-Mod; Liste ${W}/staging_dateien.txt). Plan, Berichte und
Forschung von B1a: ${W}/PLAN_ZAEHMEN.md, ${W}/forschung_engine.md (Abschnitte zu pathToLocation, respondToSound, Lure: Zeilen ~160-170,
~500-510, ~615-630), ${W}/forschung_bestand.md, ${W}/nachbesserung.md, ${W}/gegen_bericht.md, ${W}/schnittstelle_aenderungen.md.
Jar-Auszuege 42.22.2: ${W}/jar, ${W}/javap, ${W}/dec. Attrappen: ${W}/attrappe/ (kern/, ober/, gesamt/, pruef_b/; lua5.1:
C:/Users/Kevin/Tools/lua51/lua5.1.exe). Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py. Uebernahme-Skript ${B}/tools/baer_uebernahme.py, Naehte ${B}/NAEHTE.md.

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, Vanilla ${VAN} (nur lesen), Bandits ${BAN}/42.22 und
${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen; NPC Crew hat eigene Namensschilder
und Tier-Code -- zum Lernen lesen, nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Kevin spielt gerade mit der Test-Mod). Kein git, kein
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

DEINE ROLLE: FORSCHUNG (nur lesen und belegen, kein Code im Staging).
Belege fuer jeden Bedarf von B1b den Weg mit Fundstelle (Datei:Zeile, zitierte Zeile, Seite Client/Server/SP) in Vanilla bzw. Bandits:
a) Tier zu einem Punkt laufen lassen und wieder anhalten: pathToLocation (Kevins Ja 08.11. -- pruefe im Jar, ob es am SERVER wirkt und wie
   die Bewegung im MP zu den Clients kommt), Ankunft/Haengen erkennen, Gehen vs. Rennen (Variablen/Geschwindigkeit), stopAllMovementNow,
   setBlockMovement; was Vanilla mit angeleinten Tieren macht (Folgen am Seil) -- taugt der Weg als Vorbild? Was macht respondToSound /
   callOut (Q-Ruf) mit einem zahmen Jungen (Akzeptanz >= 40), stoert oder hilft es?
b) Besitzer im Fahrzeug, Treppen/Stockwerke (z), Tueren/Zaeune, entladene Gegend -- was passiert mit einem Tier, das dort hin soll?
c) Namensschild: wie zeichnet die Test-Mod heute den Balken (client/ISUI/BanditsNPCBearHud.lua) -- Weltposition -> Bildschirm, Kopfhoehe
   des Jungen; wie zeichnen Vanilla und NPC Crew Namen ueber Figuren/Tieren billig (TextDrawObject, drawText, Schrift); hat ein Tier schon
   einen Namen (getData():getName / setCustomName / getFullName) und zeigt Vanilla ihn irgendwo (ISAnimalUI)?
d) Umbenennen: Vanillas Texteingabe-Fenster (ISTextBox o. ae.) mit Fundstelle, wie Vanilla Tiere oder anderes umbenennt (ISAnimalUI?),
   Zeichenfilter, MP-Weg.
e) Futter hinhalten: Welt-Kontextmenue (OnFillWorldObjectContextMenu) mit Untermenue, ISWorldObjectContextMenu.equip mit Essen
   (Beleg Menue :79 nachpruefen), was die bestehende Server-Regel aus "Futter in der Hand" macht (BanditsNPCBearServer.lua playerInfo ~576
   und die Lock-Regel), und ob ein ausgeruestetes Essen beim Gehen/Rennen in der Hand bleibt.
f) N5: B.ScanAnimals (server/BanditsNPCBearWorld.lua) -- wie heute loose/stale behandelt werden, was fuer Waisen fehlt.
g) Sandbox-Optionen, die B1b braucht, und wie die bestehenden 19 aufgebaut sind.
Ergebnis: ${W}/forschung_b1b.md (Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil; was NUR mit Jar belegt ist, getrennt markiert;
offene Fragen). Rueckgabe: Kurzfassung mit den Kernbelegen und den Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung_b1b.md ganz, dazu PLAN_ZAEHMEN.md (Aufbau der Dateien, Register, Sicht/Sync, Zeitaktionen) und die
Staging-Dateien, die B1b beruehrt. Schreibe ${W}/PLAN_B1B.md:
1. Verhalten Schritt fuer Schritt (Folgen, Bleiben, Umschalten, Abbruchgruende mit Meldungen, Speichern/Laden, Tod, Besitzer offline im MP,
   zweiter Spieler), Zahlen als Stellwerte/Sandbox-Optionen mit Vorgaben.
2. Namensschild: Inhalt, Position (dicht ueber dem Kopf, Stellwert), Sichtweite, Deckel, Kosten je Bild; Balken vor dem Zaehmen an
   derselben Stelle.
3. Umbenennen und Futter hinhalten: Menuepunkte, Bedingungen, Grautoene mit Tooltip, Server-Pruefung.
4. N5 Waisen-Aufraeumen.
5. GENAUE SCHNITTSTELLE fuer zwei getrennte Bauer: KERN (shared/ und server/: Register-Felder, Befehle Client->Server mit Feldern und
   Pruefungen, Server-Takt fuer das Folgen, Sicht-Nutzlast an den Client mit neuen Feldern) und OBERFLAECHE (client/: Menue, Schild,
   Eingabefenster, Texte in sieben Sprachen, Sandbox-Texte, Bench-Erweiterung z. B. NCBear_CubFollowTest). Jede Funktion mit Name,
   Parametern, Rueckgabe, Datei. Wer welche Datei schreibt (keine Datei fuer beide).
6. Testfaelle fuer die Attrappen (SP und MP-Rundlauf) und Kevins Testschritte.
7. Belege: jeder geplante Engine-Aufruf mit Fundstelle aus forschung_b1b.md; Jar-only-Aufrufe ausser pathToLocation sind verboten.
Rueckgabe: Kurzfassung des Plans mit Dateiliste je Bauer.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua). Setze ${W}/PLAN_B1B.md fuer deinen Teil WOERTLICH um;
musst du von der Schnittstelle abweichen, sofort nach ${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "B1b KERN") und die Datei vor dem
Abschluss lesen. Client-Dateien (lua/client/, Translate, Bench) gehoeren dem anderen Bauer: nur lesen. Jeder Engine-Aufruf mit Fundstelle im
Kommentar (selbst nachgeprueft). Diagnose hinter dem bestehenden Schalter. Danach: vier Lua-Pruefer auf deine Dateien, Zeilenenden, die
bestehenden Attrappen (kern/, gesamt/) muessen weiter laufen (Attrappe nur anpassen, wenn der Code sich gewollt aendert, begruenden), neue
Attrappen-Faelle fuer Folgen/Bleiben/Umbenennen/Waisen unter ${W}/attrappe/b1b_kern/.
Ergebnis: ${W}/bau_b1b_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je
Vorgang, Pruefer-Ausgaben, Attrappen-Ergebnis, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/ und Bench NCBearBenchCub.lua, Translate in sieben Sprachen, Sandbox-Texte, im Staging
${W}/mod/42/media/lua). Setze ${W}/PLAN_B1B.md fuer deinen Teil WOERTLICH um; Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md
ANHAENGEN (Abschnitt "B1b OBERFLAECHE"), vor dem Abschluss lesen. shared/ und server/ gehoeren dem anderen Bauer: nur lesen. Das Schild
muss billig sein (nichts Teures je Bild, Liste selten erneuert). Texte natuerlich je Sprache, gleiche Platzhalter, JSON-Round-Trip
(json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende), sortiert, CN nur Vanilla-CN-Zeichen (pruefen). Danach: vier Lua-Pruefer,
Zeilenenden, bestehende Attrappen (ober/, gesamt/) weiter gruen, neue Faelle unter ${W}/attrappe/b1b_ober/.
Ergebnis: ${W}/bau_b1b_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt,
Pruefer-Ausgaben, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UEBERNAHME. Zwei Bauer haben getrennt gebaut (Berichte ${W}/bau_b1b_kern.md, ${W}/bau_b1b_oberflaeche.md,
Abweichungen ${W}/schnittstelle_aenderungen.md). 1. Pruefe das Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl
hat Empfaenger, Sicht-Felder passen, jeder Textschluessel in EN und allen Sprachen, Ersatztexte wortgleich) -- Werkzeug wie
${W}/attrappe/gesamt/xref.py; Luecken klein und belegt schliessen. 2. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um B1b erweitern (ein
gezaehmtes Junges: Folgen, Besitzer rennt, Auto, zu weit, Bleiben, Umbenennen, Speichern/Laden, MP-Rundlauf, Waise wird geraeumt, Futter
hinhalten am scheuen Jungen) und laufen lassen. 3. ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md nachziehen (neue Dateien/Texte/Optionen,
Cheat-Pruefung), Trockenlauf und --probe (mit --vor-b5a, Probe nur unter ${W}/probe_b1b/). 4. ${W}/staging_dateien.txt neu (Pfad | MD5 |
Bytes | neu/ueberschreibt gegen ${T}) und ${W}/mod_info_vorschlag.txt um B1b ergaenzen.
Ergebnis: ${W}/bau_b1b_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { fo, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in B1b
geaenderten oder neuen Dateien (Liste aus ${W}/bau_b1b_zusammenbau.md und staging_dateien.txt): jeder Engine-Aufruf gegen die genannte
Fundstelle im heutigen Vanilla/Bandits (Datei, Zeile, Argumenttypen, Seite), Jar-only ausser pathToLocation = Befund; keine Testbefehle
ausserhalb der Bench; Namen und Kollisionen gegen NPC Crew und Vanilla; Texte in sieben Sprachen (Schluessel, Platzhalter, Round-Trip, CN);
Sandbox-Optionen mit Texten und Benutzung; Uebernahme-Skript Trockenlauf/Probe selbst laufen lassen; vier Lua-Pruefer und alle Attrappen
selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_b1b_a.md. Rueckgabe strukturiert (id A1...).`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/pruef_b1b/. Lies den Code ganz und verfolge: Folgen (Weg, Neuplanen, Rennen, Haengenbleiben, Treppen, Auto, entladene Gegend,
Besitzer stirbt/geht offline, zwei Spieler mit je einem Jungen), Bleiben, Umbenennen (boese Eingaben, Laenge, MP-Pruefung), Schild (Kosten je
Bild, Deckel, nur eigene/nahe Junge), Futter hinhalten (kein Gegenstand verloren/verdoppelt, kein Kick, Hand-Zustand nach Abbruch), Waisen
(raeumt NIE ein Junges mit gueltigem Eintrag, nie eines in Sicht), Speichern/Laden, Zusammenspiel mit B1a (Zaehmen, Tod, Sperre, Koeder) --
alles im SP-Zweig und im MP-Zweig. Drei eigene Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_b1b_b.md. Rueckgabe
strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_b1b_a.md, ${W}/pruef_b1b_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine
neuen unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in ${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES
neu: vier Lua-Pruefer auf alle Lua-Dateien des Stagings, Zeilenenden/ASCII, JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe
(--vor-b5a), ${W}/staging_dateien.txt neu. Ergebnis ${W}/nachbesserung_b1b.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_b1b.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (--vor-b5a). staging_dateien.txt gegen
   die Platte nachzaehlen; nachweisen, welche bestehenden Dateien der Test-Mod ueberschrieben wuerden (nur gewollte).
3. Zwei eigene Stichproben (z. B. Folgen im MP-Zweig Zeile fuer Zeile; eine Sprache ganz gegengelesen).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; gezaehmtes Junges folgt, bleibt, traegt Namensschild,
   laesst sich umbenennen; Futter hinhalten am scheuen Jungen)? Blocker nur, was diesen Test verhindert oder eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_b1b.md und Testanleitung ${W}/anleitung_b1b_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit
Bench-Befehlen zum Eintippen; Achtung: Essen laesst sich in Vanilla nicht ausruesten -- nur ueber unseren Menuepunkt; Debug-"Tier Cheat"
vorher ausschalten). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, zus, pa, pb, fix, gegen }
