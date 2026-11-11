export const meta = {
  name: 'baer-b1c',
  description: 'Baer-Junges B1c: Selbstheilung, Laerm, Verstecken, Mitfahren, Unstuck, Gehen, Bildschirm- und Karten-Markierung, Anzeige-Optionen -- 9 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Engine-Belege fuer Folgen, Namensschild, Umbenennen, Hinhalten, MP' },
    { title: 'Plan', detail: 'PLAN_B1C.md mit Schnittstelle Kern/Oberflaeche' },
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

const CTX = `Du arbeitest im Lauf "baer-b1c" fuer Kevins Mod NPC Crew (Project Zomboid, Spiel laut Forschung 42.22.2; Bandits laedt aus ${BAN}/42.22
und ${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: B1a (Junges finden und zaehmen, Tierart ncbearcub) und B1b (Folgen/Bleiben, Namensschild, Umbenennen, Futter hinhalten,
Waisen) sind gebaut, geprueft und seit 11.11. 01:19 in der Test-Mod ${T}. Kevin hat gespielt: Zaehmen klappt, Folgen klappt. Seine neuen
Befunde und Wuensche stehen WOERTLICH ganz unten in ${B}/begleiter/ENTSCHEIDUNGEN.md (ab "Erster Spieltest B1a", besonders "Karten-Markierung
und Unstuck", "Mitfahren im Auto und Unstuck", "Laerm, Zombies und das Junge", "Markierung oben am Bildschirm", "Anzeige ueber dem Baeren",
"Nachtschicht 11.11.2026 -- Kevins Freigaben") und oben in ${B}/STAND.md (N9, Kevin ~01:50) -- ZUERST lesen. Kevin schlaeft: keine Fragen,
offene Punkte als "Fragen fuer Kevin" in den Bericht.

AUFTRAG B1c (Umfang fest, Kevins Freigaben vom 11.11. ~01:50):
1. N9 REGISTER-SELBSTHEILUNG: Nach Kevins Absturz war das Register leer, das Tier mit Spiegel aber da -> es wurde als neues "found" Junges
   gefuehrt, Zaehmung weg (Beleg STAND.md N9: Saves/Apocalypse/2026-11-10_22-12-12_crash/global_mod_data.bin hatte b1 tame 100). Neu: der
   Spiegel am Tier (B.MARK "tcBear", heute {id, st}) traegt alles Wichtige (st, owner, bond, finder, tame, fed, mode, name, src, Version);
   fehlt der Eintrag, wird er daraus WIEDERHERGESTELLT (gleicher Zustand, gleicher Besitzer), nie neu als found/shy. Ids bleiben eindeutig
   (Zaehler nachziehen). Zwei Tiere mit gleichem Spiegel / fremdes Konto / Fremdmanipulation im MP sauber behandeln (Server vertraut einem
   Spiegel nur, wenn kein Eintrag widerspricht; Deckel je Spieler gilt weiter).
2. LAERM: die Engine laesst jedes nicht wilde Tier vor jedem Nicht-Fahrzeug-Laerm "radius + 10" Kacheln wegrennen (respondToSound, Jar
   ${W}/dec/IsoAnimal.java:764-806; Befund 4 in ${W}/forschung_b1b.md). Das GEZAEHMTE Junge soll vor Laerm der Spieler (Rennen, Schuesse,
   Q-Ruf) NICHT mehr fliehen: Flucht sofort abfangen, Vorbild der grosse Baer (Lauf baer-laerm: ${T}/42/media/lua/shared/NCBearFight.lua:28-38
   und die fleeStop-Logik dort, Berichte C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_laerm/bau_bericht.md und fix_bericht.md -- lesen,
   nichts an NCBearFight aendern). Wilde/scheue/angefuetterte Junge duerfen weiter erschrecken.
3. ZOMBIES: das gezaehmte Junge kaempft nicht; kommt ein Zombie nahe, VERSTECKT es sich hinter seinem Besitzer (auf der dem Zombie
   abgewandten Seite, dicht dran); ist der Besitzer nicht da/zu weit, flieht es vom Zombie weg. Wilde/scheue/angefuetterte Junge fliehen vor
   Zombies. (Zombies greifen in B1c noch NICHT an -- das ist B5a.) Zombies finden: nur belegte, billige Wege (Bandits-Caches oder
   Zellenliste mit Deckel, selten erneuert).
4. MITFAHREN wie die NPC-Crew-Figuren (Kevin: "sowie unser npc crews", "der soll trotzdem in jedes auto passen"): steigt der Besitzer in ein
   Fahrzeug, folgt das gezaehmte Junge gerade (mode follow) und ist hoechstens 15 Kacheln weg, faehrt es mit (verschwindet aus der Welt,
   alles Wichtige bleibt im Register); steigt der Besitzer aus, steht es neben dem Fahrzeug wieder da (gleicher Name, gleiche Zaehmung,
   mode follow). Jede Fahrzeuggroesse. Speichern/Laden waehrend der Fahrt, Besitzer stirbt im Auto, Besitzer meldet sich im MP ab --
   sauber, nichts geht verloren, nichts verdoppelt. NPC Crew ansehen und LERNEN (nicht kopieren): ${NC}/42/media/lua/client/
   BanditsNPCPersistence.lua (P.BeginRide ~7948 ff.), client/ISUI/BanditsNPCVehiclePanel.lua. Ein Tier neu erzeugen nur ueber den
   bestehenden Weg B.CreateCub (addAnimal + addToWorld, belegt).
5. UNSTUCK: Rechtsklick am eigenen gezaehmten Jungen "Call to me": holt es neben den Besitzer (derselbe Weg wie Aussteigen), Abklingzeit
   5 Minuten Echtzeit, nicht im Fahrzeug, Zielkachel frei. Server prueft Besitz und Abklingzeit.
6. GEHEN: mit Kevins Wort (11.11.) ist animal:setVariable("animalRunning", false) am Tier erlaubt (Belege: Spieler V:ISMilkAnimal.lua:138,
   ISPetAnimal.lua:37; Zombie B:ZAMove.lua:31; am Tier nur ${T}/42/media/lua/shared/NCBearFight.lua:457/1064) -> beim Folgen auf kurze
   Strecke GEHEN, auf lange RENNEN (Schwelle als Stellwert). Das Platzhalter-Modell geht sehr langsam (0,52 Kacheln/s) -- das neue Modell
   kommt mit schnellerem Gehen; Schwelle so waehlen, dass es heute nicht zurueckfaellt.
7. BILDSCHIRM-MARKIERUNG oben (wie NPC Crews Ueberlebenden-Pfeil, ${NC}/42/media/lua/client/BanditsNPCSpawn.lua:238-319 lesen): Bandits'
   BanditEventMarkerHandler.set(feste Id, Symbol, Dauer, x, y, Farbe, Text) mit Kevins gewaehltem Symbol (Datei
   C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_icon/BanditsNPCBearCub_marker.png -> ins Staging nach 42/media/ui/BanditsNPCBearCub_marker.png
   kopieren), Farbe { r = 1.0, g = 0.72, b = 0.30 } (im Spiel orange, Kevin: so lassen), Text UI_BN_Bear_Marker_Cub "Bear cub nearby"
   (7 Sprachen). Zeigt auf das wilde Junge des Spielers (aus Wald oder Koeder), solange es noch nicht entdeckt ist bzw. eine Weile danach
   (Plan schlaegt vor), Pfeil alle ~0,4 s nachfuehren, ausblenden, wenn es weg, gezaehmt oder entdeckt ist. Nur wenn Bandits geladen ist
   (Riegel). MP: aus der Sicht des Clients.
8. KARTEN-SYMBOL: der eigene Baer (gezaehmt, auch das angefuetterte eigene Junge) als kleines Baeren-Symbol (gleiches Bild, klein) auf der
   Mini-Karte UND der grossen Karte. Weg wie NPC Crew ${NC}/42/media/lua/client/ISUI/BanditsNPCMiniMap.lua (Render von ISMiniMapInner und
   ISWorldMap umwickeln, mapAPI:worldToUIX/Y(x, y) mit ZWEI Argumenten, belegt in Vanilla ISWorldMapSymbols.lua und ISWorldMap.lua:478) --
   lernen, nicht kopieren; billig; Position aus der Sicht (auch wenn das Tier nicht geladen ist: letzte bekannte Stelle).
9. ANZEIGE-OPTIONEN je Spieler (Optionen -> Mods, wie NPC Crew ${NC}/42/media/lua/client/BanditsNPCModOptions.lua -- Belege dort lesen und
   in Vanilla nachpruefen): Namensschild ein/aus, Groesse des Schilds (Auswahl oder Schieber). Weitere Werte (Leben, Ausdauer ...) kommen
   spaeter -- die Einstellungsseite so anlegen, dass sie spaeter dazukommen koennen.
10. Kleinkram: ES "Caricias: lista" (Einzahl) richten; B1b-Restbefunde N1-N3 (${W}/gegen_bericht_b1b.md), wenn klein und sicher.
NICHT in B1c: Zombies greifen an, Kampf, Wachsen, Werte/Faehigkeiten, Heilen, Schlafen, Baeren-Fenster (V), Inventar, Fischen, neues Modell,
Umbenennen der alten NCBear*-Dateien.

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

DEINE ROLLE: FORSCHUNG (nur lesen und belegen, kein Code im Staging). Lies zuerst ${W}/forschung_b1b.md und ${W}/PLAN_B1B.md (vieles ist
dort schon belegt). Belege fuer jeden Punkt 1-10 des Auftrags den Weg mit Fundstelle (Datei:Zeile, zitierte Zeile, Seite Client/Server/SP) in
Vanilla bzw. Bandits; NPC Crew nur als Lernquelle. Besonders: Laerm-Abfangen beim grossen Baeren verstehen und auf das Junge uebertragen;
Zombies in der Naehe billig finden; NPC Crews Mitfahren (wie verschwindet/erscheint die Figur, was passiert bei Speichern, Tod, Abmelden)
und was davon fuer ein Tier mit unseren belegten Aufrufen machbar ist; Bandits-Markierung (BanditEventMarkerHandler.set: Parameter, Dauer 0 =
ausblenden, Texturpfad); Karten-Render-Wrapper (ISMiniMapInner/ISWorldMap) inkl. Symbolgroesse; Mod-Optionen-API von B42 (wie NPC Crew sie
benutzt, Beleg in Vanilla).
Ergebnis: ${W}/forschung_b1c.md (Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil; was NUR mit Jar belegt ist, getrennt markiert;
offene Fragen). Rueckgabe: Kurzfassung mit den Kernbelegen und den Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung_b1c.md ganz, dazu ${W}/PLAN_ZAEHMEN.md und ${W}/PLAN_B1B.md (Aufbau der Dateien, Register,
Sicht/Sync, Zeitaktionen, Folgen) und die Staging-Dateien, die B1c beruehrt. Schreibe ${W}/PLAN_B1C.md:
1. Je Auftragspunkt 1-10 das Verhalten Schritt fuer Schritt mit Meldungen, Speichern/Laden, Tod, Besitzer offline im MP, zweiter Spieler;
   Zahlen als Stellwerte/Sandbox-Optionen mit Vorgaben (Kevins Vorgaben aus dem Auftrag woertlich uebernehmen: 15 Kacheln Mitfahren,
   5 min Unstuck, Farbe der Markierung, ...).
2. Register-Selbstheilung: Felder des Spiegels, Version, Wiederherstellungs-Regeln, Konflikte (zwei Tiere/ein Eintrag, Eintrag/fremdes Tier).
3. Mitfahren und Unstuck: Zustandsmaschine (follow -> riding -> zurueck), was im Register steht, welche Tier-Daten verloren gehen und warum
   das ok ist; was passiert bei Speichern waehrend der Fahrt, Tod des Besitzers im Auto, Absturz.
4. Markierung, Karten-Symbol, Anzeige-Optionen: Daten aus der Sicht, Kosten je Bild, Deckel, Bandits-Riegel.
5. GENAUE SCHNITTSTELLE fuer zwei getrennte Bauer: KERN (shared/ und server/) und OBERFLAECHE (client/, Translate in 7 Sprachen,
   Sandbox-Texte, Bench-Erweiterung, Bild 42/media/ui/BanditsNPCBearCub_marker.png). Jede Funktion mit Name, Parametern, Rueckgabe, Datei.
   Wer welche Datei schreibt (keine Datei fuer beide).
6. Testfaelle fuer die Attrappen (SP und MP-Rundlauf) und Kevins Testschritte.
7. Belege: jeder geplante Engine-Aufruf mit Fundstelle aus forschung_b1c.md; Jar-only-Aufrufe sind verboten, ausser den von Kevin
   freigegebenen (pathToLocation, setVariable("animalRunning", ...) am Tier).
Rueckgabe: Kurzfassung des Plans mit Dateiliste je Bauer.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua). Setze ${W}/PLAN_B1C.md fuer deinen Teil WOERTLICH um;
musst du von der Schnittstelle abweichen, sofort nach ${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "B1c KERN") und die Datei vor dem
Abschluss lesen. Client-Dateien (lua/client/, Translate, Bench) gehoeren dem anderen Bauer: nur lesen. Jeder Engine-Aufruf mit Fundstelle im
Kommentar (selbst nachgeprueft). Diagnose hinter dem bestehenden Schalter. Danach: vier Lua-Pruefer auf deine Dateien, Zeilenenden, die
bestehenden Attrappen (kern/, gesamt/) muessen weiter laufen (Attrappe nur anpassen, wenn der Code sich gewollt aendert, begruenden), neue
Attrappen-Faelle fuer Folgen/Bleiben/Umbenennen/Waisen unter ${W}/attrappe/b1c_kern/.
Ergebnis: ${W}/bau_b1c_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je
Vorgang, Pruefer-Ausgaben, Attrappen-Ergebnis, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/ und Bench NCBearBenchCub.lua, Translate in sieben Sprachen, Sandbox-Texte, im Staging
${W}/mod/42/media/lua). Setze ${W}/PLAN_B1C.md fuer deinen Teil WOERTLICH um; Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md
ANHAENGEN (Abschnitt "B1c OBERFLAECHE"), vor dem Abschluss lesen. shared/ und server/ gehoeren dem anderen Bauer: nur lesen. Das Schild
muss billig sein (nichts Teures je Bild, Liste selten erneuert). Texte natuerlich je Sprache, gleiche Platzhalter, JSON-Round-Trip
(json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende), sortiert, CN nur Vanilla-CN-Zeichen (pruefen). Danach: vier Lua-Pruefer,
Zeilenenden, bestehende Attrappen (ober/, gesamt/) weiter gruen, neue Faelle unter ${W}/attrappe/b1c_ober/.
Ergebnis: ${W}/bau_b1c_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt,
Pruefer-Ausgaben, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UEBERNAHME. Zwei Bauer haben getrennt gebaut (Berichte ${W}/bau_b1c_kern.md, ${W}/bau_b1c_oberflaeche.md,
Abweichungen ${W}/schnittstelle_aenderungen.md). 1. Pruefe das Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl
hat Empfaenger, Sicht-Felder passen, jeder Textschluessel in EN und allen Sprachen, Ersatztexte wortgleich) -- Werkzeug wie
${W}/attrappe/gesamt/xref.py; Luecken klein und belegt schliessen. 2. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um B1c erweitern (Register leer + Tier mit Spiegel -> Wiederherstellung; Laerm am
gezaehmten Jungen wird abgefangen, am scheuen nicht; Zombie naht -> versteckt sich hinter dem Besitzer / flieht; Besitzer steigt ein ->
faehrt mit, steigt aus -> steht daneben; Speichern waehrend der Fahrt; Unstuck mit Abklingzeit; Gehen/Rennen; Markierung an/aus;
Karten-Symbol; Optionen) und laufen lassen; die bestehenden B1a/B1b-Faelle muessen gruen bleiben. 3. ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md nachziehen (neue Dateien/Texte/Optionen,
Cheat-Pruefung), Trockenlauf und --probe (mit --vor-b5a, Probe nur unter ${W}/probe_b1c/). 4. ${W}/staging_dateien.txt neu (Pfad | MD5 |
Bytes | neu/ueberschreibt gegen ${T}) und ${W}/mod_info_vorschlag.txt um B1c ergaenzen.
Ergebnis: ${W}/bau_b1c_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { fo, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in B1c
geaenderten oder neuen Dateien (Liste aus ${W}/bau_b1c_zusammenbau.md und staging_dateien.txt): jeder Engine-Aufruf gegen die genannte
Fundstelle im heutigen Vanilla/Bandits (Datei, Zeile, Argumenttypen, Seite), Jar-only ausser pathToLocation = Befund; keine Testbefehle
ausserhalb der Bench; Namen und Kollisionen gegen NPC Crew und Vanilla; Texte in sieben Sprachen (Schluessel, Platzhalter, Round-Trip, CN);
Sandbox-Optionen mit Texten und Benutzung; Uebernahme-Skript Trockenlauf/Probe selbst laufen lassen; vier Lua-Pruefer und alle Attrappen
selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_b1c_a.md. Rueckgabe strukturiert (id A1...).`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/pruef_b1c/. Lies den Code ganz und verfolge: Register-Selbstheilung (leeres Register, doppelter Spiegel, manipulierter Spiegel im MP,
fremdes Konto, Zaehler), Laerm-Abfangen (nur gezaehmt; nichts haengt; Zusammenspiel mit Folgen/Bleiben/Verstecken), Verstecken/Fliehen vor
Zombies (Kosten der Zombiesuche, kein Endlos-Hin-und-Her), Mitfahren (einsteigen, aussteigen, Speichern/Laden waehrend der Fahrt, Tod im
Auto, Abmelden im MP, zwei Spieler -- kein Junges verloren oder verdoppelt), Unstuck (Abklingzeit am Server, Zielkachel, Missbrauch im MP),
Gehen/Rennen (animalRunning wird immer wieder richtig gesetzt), Markierung/Karte/Optionen (Kosten je Bild, Bandits fehlt, NPC Crew fehlt),
Zusammenspiel mit B1a/B1b -- alles im SP-Zweig und im MP-Zweig. Drei eigene Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_b1c_b.md. Rueckgabe
strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_b1c_a.md, ${W}/pruef_b1c_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine
neuen unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in ${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES
neu: vier Lua-Pruefer auf alle Lua-Dateien des Stagings, Zeilenenden/ASCII, JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe
(--vor-b5a), ${W}/staging_dateien.txt neu. Ergebnis ${W}/nachbesserung_b1c.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_b1c.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (--vor-b5a). staging_dateien.txt gegen
   die Platte nachzaehlen; nachweisen, welche bestehenden Dateien der Test-Mod ueberschrieben wuerden (nur gewollte).
3. Zwei eigene Stichproben (z. B. Folgen im MP-Zweig Zeile fuer Zeile; eine Sprache ganz gegengelesen).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; Zaehmung ueberlebt ein geleertes Register; gezaehmtes
   Junges flieht nicht vor Laerm, versteckt sich hinter ihm vor Zombies, faehrt im Auto mit, Unstuck holt es, geht auf kurze Strecken;
   Markierung oben zeigt auf ein wildes Junges; Symbol auf Mini- und grosser Karte; Optionen wirken)? Blocker nur, was diesen Test verhindert
   oder eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_b1c.md und Testanleitung ${W}/anleitung_b1c_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit
Bench-Befehlen zum Eintippen; Debug-"Tier Cheat" vorher ausschalten; Bandits muss fuer die Markierung geladen sein). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, zus, pa, pb, fix, gegen }
