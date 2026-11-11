export const meta = {
  name: 'baer-b1e',
  description: 'Baer-Junges B1e: ab Halbstark (Tag 15) Wechsel auf das grosse Modell, das bis Tag 100 auf 1,35 mitwaechst -- 9 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Tausch-Weg, Modellgroessen, Tempo, alle Stellen mit Art-Pruefung' },
    { title: 'Plan', detail: 'PLAN_B1E.md mit Schnittstelle Kern/Oberflaeche' },
    { title: 'Bau', detail: 'Kern und Oberflaeche getrennt, dann Zusammenbau + Uebernahme-Skript' },
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

const CTX = `Du arbeitest im Lauf "baer-b1e" fuer Kevins Mod NPC Crew (Project Zomboid, Spiel 42.22.2; Bandits laedt aus ${BAN}/42.22 und
${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: B1a (finden, zaehmen), B1b (folgen, Namensschild), B1c (Selbstheilung, Laerm, Verstecken, Mitfahren, Call to me, Gehen,
Markierung, Karten-Symbol, Optionen) und B1d (Wachsen 100 Tage, taeglich steigende Werte, Faehigkeiten-Daten, Heil-Formeln, Anzeige) sind
gebaut, geprueft und in der Test-Mod ${T} (Git main 401dd70). Seit 11.11. 14:39 traegt das Junge ein neues Modell aus dem Generator.
KEVINS SPIELTEST B1d (11.11.2026 ~15:10, console.txt): Werte stimmen (Tag 15 Leben 150, Tag 45 Leben 255, Tag 100 Leben 400 / Ausdauer 160 /
Traglast 100 / Schaden 1,0), keine roten Fehler -- aber woertlich: "der wird garnichtmehr groesser ab tag 15 oder so" und "und das model
aendert sich auch nicht". Beides war in B1d Absicht (${W}/PLAN_B1D.md 0.10 und 1.2: gezeigte Groesse haelt bei cubMaxSize 0,75, Modellwechsel
vorbereitet, B.CFG.bodySwap = false, Frage F11). KEVINS ENTSCHEIDUNG (11.11. ~15:20, woertlich): "Ab Tag 15 (halbstark)" -- auf Claudes
Vorschlag: "Ab Tag 15 wird das Junge zum grossen Baeren in klein, mit 0,75, und waechst bis Tag 100 auf die volle Groesse 1,35." Steht ganz
unten in ${B}/begleiter/ENTSCHEIDUNGEN.md -- ZUERST lesen, dazu die Groessen-Tabelle oben (Jungtier 0,35 / Halbstark 0,75 / Erwachsen 1,35).
Kevin testet gerade im Spiel: keine Fragen an ihn waehrend des Laufs, offene Punkte als "Fragen fuer Kevin" in den Bericht.

JUNGES-MODELL (Kevin 11.11. ~15:25, woertlich): "der neue baby baer laeuft auch wie eine giraffe oder so xD also das alte ist definitiv
besser ^^". Das Junge bekommt deshalb wieder das ALTE Modell (Entwurf baer-baby: C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/entwurf/
NCBearCub.glb MD5 6c3f0a96 + NCBearCub.png 2ee25f24 = Stand der Test-Mod vor Commit f10621f, Gehen 0,52 / Rennen 2,47 Kacheln/s). Claude stellt
es in der Test-Mod zurueck, sobald Kevins Spiel zu ist; byte-gleich liegt es schon als ${T}/42/media/models_X/Skinned/NCBearBenchCubAlt.glb.
Miss und plane mit DIESEM Modell, nicht mit dem Generator-Jungen, das heute noch als NCBearCub.glb in der Test-Mod liegt; die B1c-Folgen-Werte
(walkSpeed 0,52) passen wieder dazu.

AUFTRAG B1e MODELLWECHSEL (Kevins Wort oben):
1. TAUSCH: Erreicht das GEZAEHMTE Junge Halbstark (gezeigte Groesse erreicht cubMaxSize 0,75; bei Sandbox 100 Tage um Tag 15, bei anderer
   Zahl anteilig), wird der Koerper vom Junges-Modell (Art "ncbearcub", B.CUB) auf das GROSSE Modell getauscht -- das grosse Modell, das die
   Test-Mod heute fuer den erwachsenen Baeren nutzt (2c-Baer, models_X/Skinned/NCBear.glb mit seinem Modell-Skript). Als EIGENE neue Art
   (Name mit Kollisionsprobe gegen NPC Crew ${NC}/42/media/lua, Vanilla und die Test-Mod; Vorschlag im Plan), NIE die alte Art "bear" (deren
   Kampf in NCBearFight.lua greift sofort voll an -- das ist B5a), alte NCBear*-Dateien NICHT aendern. Tausch ueber den vorhandenen Weg
   (B.RemoveCub + B.PlaceCub mit gen + 1, PLAN_B1C 0.2/0.3; die Stelle steht als Kommentar in server/BanditsNPCBearGrow.lua B.GrowLive;
   B.CreateCub lernt den Koerper). Genau EIN Tier zu jeder Zeit: kein Doppel, kein Verlust, Register-Eintrag bleibt derselbe (Besitzer, Name,
   Zaehmung, Werte, Faehigkeiten, Leben-Anteil, Folgen/Bleiben, Lage/Richtung). Kein Tausch waehrend Mitfahren, Call to me oder anderer
   laufender Vorgaenge -- dann beim naechsten sicheren Takt. Ein Tausch je Stufenwechsel, nie hin und her flackern (Schwelle mit Abstand).
2. GROESSE: Der Sprung beim Tausch soll klein sein. MESSEN (GLB-Auszuege, Importer-Harness C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/
   baer_spiel/harness Dump.java oder Python-GLB-Leser): Hoehe/Laenge des Junges-Modells bei 0,75 gegen das grosse Modell; daraus die gezeigte
   Groesse des grossen Modells beim Tausch und die Abbildung s 0,75..1,35 -> gezeigte Groesse, so dass es am Ende (Tag 100) genau so gross ist
   wie der erwachsene Baer bei 1,35 (Kevins Tabelle). Zahlen als Stellwerte mit Fundstelle. Groesse wie bisher ueber den belegten Weg setzen.
3. ZURUECK: NCBear_CubGrow(-100) (Bench) bringt es wieder auf das Junges-Modell (Tausch zurueck). Speichern/Laden, Mitfahren, Call to me und die
   Register-Heilung (Spiegel v2 um den Koerper ergaenzen) behalten den Koerper; ein Spielstand von B1d (Junges ueber 0,75 im Junges-Modell)
   tauscht beim ersten sicheren Takt.
4. ALLES AUS B1a-B1d GILT AUCH FUER DEN GROSSEN KOERPER: jede Stelle, die heute auf die Art B.CUB prueft (Folgen, Bleiben, Namensschild und
   seine Hoehe, Rechtsklick-Menue, Fuettern/Hinhalten, Streicheln, Verstecken vor Zombies, Laerm-Flucht abfangen, Mitfahren, Call to me,
   Markierung, Karten-Symbol, Anzeige-Optionen, Spiegel, Bench) muss beide Koerper erkennen (ein Helfer statt verstreuter Vergleiche).
   Wilde Junge wachsen und tauschen nie; die alte Art "bear" bleibt unberuehrt.
5. TEMPO: Folgen/Gehen/Rennen beim grossen Modell so einstellen, dass die Fuesse nicht rutschen (Clip-Geschwindigkeit gegen gezeigte Groesse,
   Folgen-Abstaende mit der Koerperlaenge); belegen oder als "im Spiel ansehen" melden.
6. BENCH (nur NCBearBench*, nur SP): NCBear_CubStats() zeigt den Koerper; NCBear_CubGrow loest den Tausch aus.
7. MARKIERUNG GROESSER (Kevin 11.11. ~15:30 nach seinem Test mit Bandits, woertlich: "okay das geht schonmal aber waer cooler wenn das
   symbol was groesser waere zumindestens bei 4k aufloesung"; sein Bildschirm 3840x2054, das Symbol oben in der Mitte wirkt klein, der Kreis
   ist kaum zu sehen). Ursache: Bandits zeichnet Kreis, Pfeil und Symbol in fester Pixelgroesse 96 ohne Skalierung (Bandits 42.22
   client/BanditEventMarkers.lua:7, :174, :192-193; BanditEventMarkerHandler.lua:7-35). Ziel: die Markierung des wilden Jungen waechst mit der
   Bildschirmhoehe (Richtwert 1080 = 1,0 / 1440 = ~1,33 / 2160 = 2,0) und laesst sich in unseren Mod-Optionen (Seite aus B1c) einstellen
   (z. B. Auto oder 100-300 %). Weg mit Beleg waehlen: eigene Markierung als eigenes UI-Element nur mit Vanilla-UI-Aufrufen (Fundstelle je
   Aufruf; nichts aus Bandits kopieren; Bandits-Bilder hoechstens zur Laufzeit ueber getTexture nutzen, wenn Bandits geladen ist, sonst eigene
   Bilder) ODER ein belegter Weg, Bandits-Markierung zu skalieren, ohne Bandits-Dateien zu aendern. Aussehen und Verhalten wie heute (Kreis
   Honig-Orange, Pfeil zur Richtung, Text "Bear cub nearby", verschwindet etwa 1 Minute nachdem es dich sah), billig je Bild. Gehoert der
   OBERFLAECHE (Texte fuer die neue Option in 7 Sprachen).
NICHT in B1e: Kampf/Zombie-Angriffe (B5a), neue Modelle oder Aenderung an Modell-Dateien, Farbe/Kopf des grossen Baeren (Kevins offene Frage --
der Tausch nimmt das jeweils aktuelle grosse Modell), Schlafen, Fischen, Spuernase, Inventar, Baeren-Fenster.

ORTE: Staging (Pruefgegenstand und Bauort) ${W}/mod/ (spiegelt die Wurzel der Test-Mod fuer die B1-Dateien; Liste ${W}/staging_dateien.txt;
heute byte-gleich mit der Test-Mod -- vor dem Bau nachzaehlen). Plaene/Berichte: ${W}/PLAN_ZAEHMEN.md, PLAN_B1B.md, PLAN_B1C.md, PLAN_B1D.md,
forschung_b1c.md, forschung_b1d.md, schnittstelle_aenderungen.md, gegen_bericht_b1d.md, nachbesserung_b1d.md. Jar-Auszuege ${W}/jar,
${W}/javap, ${W}/dec. Attrappen: ${W}/attrappe/ (kern/, ober/, gesamt/, b1d_kern/, b1d_ober/; lua5.1: C:/Users/Kevin/Tools/lua51/lua5.1.exe).
Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py, luacheck_pz.py. Uebernahme-Skript
${B}/tools/baer_uebernahme.py, Naehte ${B}/NAEHTE.md. Modell-Berichte: ${B}/spiel/2c_*.md (grosser Baer), ${B}/spiel/rig_*.md (neues Junges).

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel,
Vanilla ${VAN} (nur lesen), Bandits ${BAN}/42.22 und ${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt
(nur lesen, nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Kevin spielt gerade). Kein git, kein Spielstart, kein
Download, nichts hochladen. EISERNE REGEL: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder Bandits mit
GLEICHEN Argumenttypen, im Kommentar genannt; Ausnahme nur mit Kevins Wort je Methode -- erteilt fuer animal:pathToLocation(x, y, z) und
setVariable("animalRunning", ...) am Tier. Ein pcall um einen unbelegten Aufruf ist eine Tarnkappe. SP UND MP: SP-Test "not isServer() and not
isClient()"; was der Server wissen muss, kommt nie aus einem Client-Glauben; im SP tut sendServerCommand nichts (direkt rufen). Kevins rote
Linien: kein Gegenstand verloren oder verdoppelt, kein Kick (Rolle user, AntiCheat), nichts haengt endlos, keine NPC-Crew-Figur wird gestoert --
hier zusaetzlich: das Junge geht beim Tausch nie verloren und wird nie verdoppelt. Testbefehle nur in NCBearBench*.lua (nur SP). Namen:
BanditsNPCBear*.lua, Modul BanditsNPC.Bear, Texte UI_BN_Bear_* in EN, PTBR, RU, KO, ES, CN, FR (CN nur Zeichen aus Vanilla-CN), Sandbox
BanditsNPC.Bear*. Nichts Teures je Bild, Deckel fuer alles, was waechst; Kahlua ist kein echtes Lua 5.1 (kein next). Dateien LF, ASCII in Lua.
Schreibe "statisch geprueft, nicht gespielt"; keine Behauptung ohne Fundstelle (Datei:Zeile), sonst "ungeprueft".`

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

DEINE ROLLE: FORSCHUNG (nur lesen, messen und belegen, kein Code im Staging). Lies zuerst ${W}/PLAN_B1D.md (0.10, 1.2), ${W}/PLAN_B1C.md
(0.2/0.3 Tausch-Weg), forschung_b1d.md. Belege mit Fundstelle (Datei:Zeile, zitierte Zeile, Seite Client/Server/SP):
a) Wie die Test-Mod Arten und Modelle anlegt (BanditsNPCBearDefs.lua, NCBearDefs.lua, NCBearBenchVergleichDefs.lua, media/scripts/*,
   AnimalDefinitions in Vanilla): was eine neue Art mit dem grossen Modell braucht (Definition, Modell-Skript, Animset, Geschwindigkeiten,
   Groessen-Felder), welche Felder der alten Art "bear" Kampf/Verhalten ausloesen (NCBearFight.lua: woran erkennt es "seine" Baeren?).
b) Jede Stelle im Staging, die auf die Art des Jungen prueft (B.CUB, "ncbearcub", getAnimalType o. ae.) -- vollstaendige Liste mit Datei:Zeile.
c) Der Tausch-Weg B.RemoveCub/B.PlaceCub/B.CreateCub und der Kommentar in B.GrowLive: was heute schon geht, was fehlt.
d) MESSEN: Hoehe, Laenge, Breite des ALTEN Junges-Modells (siehe JUNGES-MODELL oben) und des grossen Modells (NCBear.glb) in
   Spiel-Einheiten bei Groesse 1,0 (Ruhelage aus dem GLB bzw. Dump.java), daraus: gezeigte Groesse des grossen Modells, die beim Tausch so gross
   wirkt wie das Junge bei 0,75, und Vorschlag fuer die Abbildung bis 1,35. Gehgeschwindigkeit je Modell (Weg je Clip-Zyklus, Translation_Data)
   gegen das Folgen-Tempo (B1c walkSpeed u. ae.), damit die Fuesse nicht rutschen.
e) Was die Engine beim Entfernen/Neuanlegen eines Tiers mit Daten tut (modData, Leben, Groesse; forschung_b1c.md/b1d.md weiter nutzen).
f) Auftragspunkt 7: wie unsere Markierung heute gesetzt wird (Staging client/, B1c), wie Bandits sie zeichnet, welche Vanilla-UI-Aufrufe ein
   skaliertes Zeichnen inkl. gedrehtem Pfeil erlauben (Fundstellen), Bildschirmhoehe lesen (Fundstelle), Optionen-Seite aus B1c erweitern.
Ergebnis: ${W}/forschung_b1e.md (Tabellen Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil; Messwerte mit Werkzeug und Befehl; was NUR mit
Jar belegt ist, getrennt; offene Fragen). Rueckgabe: Kurzfassung mit Kernbelegen, Messzahlen und Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung_b1e.md ganz, dazu ${W}/PLAN_B1D.md und ${W}/PLAN_B1C.md (Aufbau, Register, Spiegel v2, Sicht/Sync,
Takte, Tausch-Weg) und die Staging-Dateien, die B1e beruehrt. Schreibe ${W}/PLAN_B1E.md:
1. Je Auftragspunkt 1-7 das Verhalten Schritt fuer Schritt: Ausloeser, sicherer Zeitpunkt, Ablauf des Tauschs (alte Kennung, neue Kennung,
   gen), Meldung an den Besitzer (falls eine, Text in 7 Sprachen), Speichern/Laden, Tod, Besitzer offline im MP, zweiter Spieler, Absturz
   mitten im Tausch (was steht im Register, was heilt der Spiegel), zurueck auf das Junge.
2. Die neue Art: Name (Kollisionsprobe), Definition, Modell-Skript, Groessen-Abbildung mit den gemessenen Zahlen, Tempo/Abstaende je Koerper.
3. Der eine Helfer fuer "ist unser Baer" und die Liste ALLER Stellen aus forschung_b1e.md b), die ihn benutzen.
4. GENAUE SCHNITTSTELLE fuer zwei getrennte Bauer: KERN (shared/ und server/) und OBERFLAECHE (client/, Translate in 7 Sprachen, Sandbox-Texte,
   Bench). Jede Funktion mit Name, Parametern, Rueckgabe, Datei. Wer welche Datei schreibt (keine Datei fuer beide).
5. Testfaelle fuer die Attrappen (SP und MP-Rundlauf; Tausch hin und zurueck; Speichern im Tausch; Mitfahren/Call to me waehrend der Schwelle)
   und Kevins Testschritte.
6. Belege: jeder geplante Engine-Aufruf mit Fundstelle aus forschung_b1e.md; Jar-only ist verboten (ausser pathToLocation, animalRunning).
Rueckgabe: Kurzfassung des Plans mit Dateiliste je Bauer.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua, dazu Art-Definition/Modell-Skript, falls der Plan sie dem Kern
gibt). Zuerst Staging gegen die Test-Mod nachzaehlen (staging_dateien.txt, MD5). Setze ${W}/PLAN_B1E.md fuer deinen Teil WOERTLICH um;
musst du von der Schnittstelle abweichen, sofort nach ${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "B1e KERN") und die Datei vor dem
Abschluss lesen. Client-Dateien (lua/client/, Translate, Bench) gehoeren dem anderen Bauer: nur lesen. Jeder Engine-Aufruf mit Fundstelle im
Kommentar (selbst nachgeprueft). Diagnose hinter dem bestehenden Schalter. Danach: vier Lua-Pruefer auf deine Dateien, Zeilenenden, die
bestehenden Attrappen (kern/, gesamt/, b1d_kern/) muessen weiter laufen (nur gewollt anpassen, begruenden), neue Faelle fuer Tausch hin/zurueck,
Speichern im Tausch, Spiegel-Heilung mit Koerper, kein Doppel unter ${W}/attrappe/b1e_kern/.
Ergebnis: ${W}/bau_b1e_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je
Vorgang, Pruefer-Ausgaben, Attrappen-Ergebnis, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/ und Bench NCBearBenchCub.lua, Translate in sieben Sprachen, Sandbox-Texte, im Staging
${W}/mod/42/media/lua). Setze ${W}/PLAN_B1E.md fuer deinen Teil WOERTLICH um (u. a. alle Client-Stellen mit Art-Pruefung auf den Helfer,
Namensschild-Hoehe fuer den grossen Koerper, Menue, Markierung, Karten-Symbol, Bench); Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md
ANHAENGEN (Abschnitt "B1e OBERFLAECHE"), vor dem Abschluss lesen. shared/ und server/ gehoeren dem anderen Bauer: nur lesen. Nichts Teures je
Bild. Texte natuerlich je Sprache, gleiche Platzhalter, JSON-Round-Trip (json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende),
sortiert, CN nur Vanilla-CN-Zeichen (pruefen). Danach: vier Lua-Pruefer, Zeilenenden, bestehende Attrappen (ober/, gesamt/, b1d_ober/) weiter
gruen, neue Faelle unter ${W}/attrappe/b1e_ober/.
Ergebnis: ${W}/bau_b1e_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt,
Pruefer-Ausgaben, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UEBERNAHME. Zwei Bauer haben getrennt gebaut (Berichte ${W}/bau_b1e_kern.md, ${W}/bau_b1e_oberflaeche.md,
Abweichungen ${W}/schnittstelle_aenderungen.md). 1. Pruefe das Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl
hat Empfaenger, Sicht-Felder passen, jeder Textschluessel in EN und allen Sprachen, Ersatztexte wortgleich, keine Stelle prueft mehr nur auf
B.CUB) -- Werkzeug wie ${W}/attrappe/gesamt/xref.py; Luecken klein und belegt schliessen. 2. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um B1e
erweitern (Zaehmen -> 14 Tage: Junges-Modell; 15 Tage: Tausch auf den grossen Koerper, genau ein Tier, gleicher Eintrag/Name/Werte;
45/100 Tage: gezeigte Groesse nach Abbildung bis zum Endwert; -100: zurueck; Speichern/Laden, Mitfahren und Call to me um die Schwelle;
Spiegel-Heilung mit Koerper; Sandbox-Tage 30 und 365) und laufen lassen; alle B1a-B1d-Faelle bleiben gruen. 3. ${B}/tools/baer_uebernahme.py
und ${B}/NAEHTE.md nachziehen (neue Art, Dateien, Texte, Cheat-Pruefung), Trockenlauf und --probe (mit --vor-b5a, Probe nur unter
${W}/probe_b1e/). 4. ${W}/staging_dateien.txt neu (Pfad | MD5 | Bytes | neu/ueberschreibt gegen ${T}) und ${W}/mod_info_vorschlag.txt um B1e.
Ergebnis: ${W}/bau_b1e_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { fo, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in B1e
geaenderten oder neuen Dateien (Liste aus ${W}/bau_b1e_zusammenbau.md und staging_dateien.txt): jeder Engine-Aufruf gegen die genannte
Fundstelle im heutigen Vanilla/Bandits (Datei, Zeile, Argumenttypen, Seite), Jar-only = Befund (ausser pathToLocation/animalRunning); neue Art
und Modell-Skript richtig angelegt und kollisionsfrei; alte NCBear*-Dateien unveraendert; keine Testbefehle ausserhalb der Bench; Texte in
sieben Sprachen (Schluessel, Platzhalter, Round-Trip, CN); Uebernahme-Skript Trockenlauf/Probe selbst laufen lassen; vier Lua-Pruefer und alle
Attrappen selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_b1e_a.md. Rueckgabe strukturiert (id A1...).`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/pruef_b1e/. Lies den Code ganz und verfolge den Tausch hin und zurueck in jedem Zustand (folgt, bleibt, versteckt, flieht vor
Laerm, faehrt mit, Call to me, wird gefuettert/gestreichelt, Besitzer offline, zweiter Spieler, Speichern/Laden, Absturz mitten im Tausch,
Register leer + Spiegel): kann das Tier verloren gehen oder doppelt entstehen? Flackert der Tausch an der Schwelle? Stimmt die Groessen-Abbildung
(Zahlen nachrechnen gegen forschung_b1e.md)? Erkennt jede Stelle beide Koerper (Liste aus forschung_b1e.md b) abhaken)? Tempo/Fussrutschen?
Kosten je Bild? Alles im SP- und MP-Zweig. Drei eigene Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_b1e_b.md.
Rueckgabe strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_b1e_a.md, ${W}/pruef_b1e_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine
neuen unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in ${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES
neu: vier Lua-Pruefer auf alle Lua-Dateien des Stagings, Zeilenenden/ASCII, JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe
(--vor-b5a), ${W}/staging_dateien.txt neu. Ergebnis ${W}/nachbesserung_b1e.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_b1e.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (--vor-b5a). staging_dateien.txt gegen
   die Platte nachzaehlen; nachweisen, welche bestehenden Dateien der Test-Mod ueberschrieben wuerden (nur gewollte; alte NCBear*-Dateien nie).
3. Zwei eigene Stichproben (z. B. Tausch waehrend Mitfahren Zeile fuer Zeile; Speichern genau im Tausch).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; NCBear_CubGrow(15) tauscht sichtbar auf den grossen Koerper,
   genau ein Tier, Name/Werte bleiben, er folgt weiter; NCBear_CubGrow bis 100 laesst ihn bis zum Endwert wachsen; -100 zurueck; NCBear_CubHere(30) zeigt die Markierung bei 4K deutlich groesser,
   Groesse in den Optionen einstellbar; B1a-B1d
   unveraendert)? Blocker nur, was diesen Test verhindert oder eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_b1e.md und Testanleitung ${W}/anleitung_b1e_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit
Bench-Befehlen zum Eintippen; Spiel mit -debug neu starten; Debug-"Tier Cheat" vorher ausschalten; Bandits muss geladen sein; Mitfahren nur
optional -- Kevin hat gerade kein Auto, Hinweis: Rechtsklick Boden > Debug > Main > "Spawn Vehicle"). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, zus, pa, pb, fix, gegen }
