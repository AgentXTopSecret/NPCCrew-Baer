export const meta = {
  name: 'baer-f1',
  description: 'Baer F1: Baeren-Fenster auf V (schoenes UI: Werte, Faehigkeiten, Befehle Folgen/Bleiben/Sitz/Frei/Komm her/Passiv, Unstuck) + B1e-Reste -- 9 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Tasten, Fenster-Bausteine, Sitzen, Frei-Bereich, Unstuck, B1e-Reste' },
    { title: 'Plan', detail: 'PLAN_F1.md + Fenster-Entwurf als Bild, Schnittstelle Kern/Oberflaeche' },
    { title: 'Bau', detail: 'Kern und Oberflaeche getrennt, dann Zusammenbau + Uebernahme-Skript' },
    { title: 'Pruefung', detail: 'Pruefer A Belege/Regeln/Texte, Pruefer B Logik/SP-MP/Optik' },
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

const CTX = `Du arbeitest im Lauf "baer-f1" fuer Kevins Mod NPC Crew (Project Zomboid, Spiel 42.22.2; Bandits laedt aus ${BAN}/42.22 und
${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: B1a (finden, zaehmen), B1b (folgen, Namensschild), B1c (Selbstheilung, Laerm, Verstecken, Mitfahren, Call to me, Gehen,
Markierung, Karten-Symbol, Optionen), B1d (Wachsen 100 Tage, Werte, Faehigkeiten-Daten, Heil-Formeln, Anzeige) und B1e (ab Tag 15 Wechsel auf
den grossen Koerper, Art "ncbeargrown", Helfer B.BodyKind; Markierung skaliert) sind gebaut, geprueft und in der Test-Mod ${T} (Git main 914ee79,
11.11.2026 18:22; Staging ${W}/mod/ ist damit byte-gleich -- vor dem Bau nachzaehlen). Berichte: ${W}/PLAN_B1B.md .. PLAN_B1E.md,
forschung_b1c.md .. forschung_b1e.md, gegen_bericht_b1e.md (Restbefunde C1-C3, A1/B6, A5, B7 und 9 Fragen).
NACHTSCHICHT: Kevin schlaeft. Keine Fragen an ihn waehrend des Laufs; offene Kleinfragen mit dem EMPFOHLENEN Weg bauen und als "Fragen fuer
Kevin" (mit dem gewaehlten Weg) in den Bericht. Kevin woertlich (11.11. ~18:40): "alle funktionen einbauen noch vom baeren du weisst ja bescheid
was ich alels wollte die ganzen skills das schoene ui und alles". Seine Wuensche stehen in ${B}/begleiter/ENTSCHEIDUNGEN.md -- ZUERST lesen, vor
allem "Befehle, Sitzen, Fressen (08.11.)", "Baeren-Fenster mit V (08.11. ~19:45)", "Balken ueber dem Baeren", "Werte und Faehigkeiten
(11.11. ~00:30)", "B1b gespielt + Baeren-Fenster (11.11. ~01:45)", "Heilen", "Nachtschicht 11./12.11." mit den Nachtraegen; dazu ${B}/PLAN.md.

AUFTRAG F1 BAEREN-FENSTER (Kevin 11.11. ~01:45 woertlich: "ich wll noch spaeter eine richtige UI die aufgeht wenn ich V druecke (einstellbar in
den keystings)"; Kevin ~18:40: "das schoene ui"):
1. TASTE: V oeffnet/schliesst das Fenster des EIGENEN Baeren; Taste in den Tastenbelegungen des Spiels einstellbar (Weg wie NPC Crew
   ${NC}/42/media/lua/client/BanditsNPCModOptions.lua crewKey/OnKeyPressed :138-155 -- lernen, nicht kopieren; Kollision mit NPC Crews eigener
   Taste und Vanilla-Belegungen pruefen und im Bericht nennen). Kein eigener Baer: kurzer Hinweis statt Fenster. Dazu Eintrag "Bear window" im
   Rechtsklick-Menue am eigenen Baeren.
2. INHALT (alles, was es heute schon gibt; alles mit Fundstelle der Daten im Staging):
   - Kopf: Baeren-Symbol (Kevins Symbol 1, schon im Staging), Name (Umbenennen-Knopf, B1b-Weg), Koerper Junges/grosser Baer, Alter "Tag 12 --
     halbstark in 3 Tagen" (B1d), Zustand (folgt/bleibt/sitzt/frei/versteckt/faehrt mit/nicht geladen).
   - Balken mit Zahl: Leben, Ausdauer, Zaehmung/Vertrauen (falls Daten da), Traglast als Wert. Hunger/Durst/Muedigkeit gibt es noch nicht (F3):
     Platz vorsehen, aber NICHTS Falsches anzeigen.
   - Faehigkeiten (B1d-Daten): Agilitaet, Leben, Kondition, Kaempfen, Fischen, Spuernase -- je Stufe 0-10, Fortschritt zur naechsten Stufe als
     Balken, Tooltip, was sie bewirkt (Kevins Saetze aus ENTSCHEIDUNGEN; was erst mit B5a/F5 wirkt, im Tooltip ehrlich "kommt spaeter").
   - Befehle als Knoepfe: Folgen, Bleiben (B1b), **Sitz** (setzt sich hin und bleibt sitzen; Sitz-Clips gibt es fuer beide Koerper -- Weg, den die
     Test-Mod heute schon fuer das Sitzen benutzt, belegt suchen), **Frei herumlaufen** (Kevin 08.11.: "nie ausserhalb der Basisflaeche: in NPC
     Crew die gezeichnete Basisflaeche des Beacons, in der Test-Mod ein vom Spieler gesetzter Bereich" -- in F1: Bereich = Kreis um die Stelle des
     Befehls, Radius einstellbar, Vorgabe 8 Kacheln; Beacon-Naht nur dokumentieren in NAEHTE.md, nicht bauen), **Komm her** (= Call to me aus
     B1c, gleiche Abklingzeit, Restzeit am Knopf), **Passiv** (Schalter je Baer, gespeichert und angezeigt; wirkt erst mit B5a Kampf -- ehrlich im
     Tooltip), **Unstuck** (Kevin 08.11.: holt ihn auf eine freie, stehbare Kachel neben dem Spieler, nie auf eine unstehbare, auch wenn er liegt
     oder nicht geladen ist; nur auf Klick; im MP versetzt der Server; bestehende Call-to-me-/PlaceCub-Wege nutzen), Namensschild an/aus je Baer.
   - Der aktive Befehl ist sichtbar hervorgehoben; Knoepfe, die gerade nicht gehen (Mitfahren, Abklingzeit, zu weit), sind grau mit Grund.
3. SCHOEN: Vanilla-Fenster-Bausteine (ISCollapsableWindow/ISPanel/ISButton/ISTickBox o. ae., je Aufruf mit Fundstelle), ruhige dunkle
   Flaeche, Honig-Orange als Akzent wie die Markierung, klare Abstaende, Balken mit Farbverlauf nach Wert, Schrift lesbar; skaliert mit der
   Bildschirmhoehe/Schriftgroesse (Kevin spielt 3840x2054 -- 4K darf nicht winzig sein, B1e-Faktor wiederverwenden); Lage merken; Fenster
   verschiebbar, Esc/V schliesst. Nichts Teures je Bild (Werte hoechstens ein paar Mal je Sekunde neu lesen).
4. B1e-RESTE: (a) A1/B6: Why_Gone, Note_Dead, Menu_Hold, Menu_HoldTip sagen beim grossen Koerper "bear" statt "cub" (7 Sprachen).
   (b) C1: ein zahmer Eintrag ohne Koerper ("missing") in geladener Gegend bekommt von selbst wieder genau EINEN Koerper (nie ein Doppel: erst
   suchen, dann PlaceCub; Absturz-/Lade-Faelle wie B1c-Spiegel), und der Unstuck-Knopf im Fenster wirkt auch fuer ihn. (c) A5: 288-px-Bilder
   gegen den Texturdeckel 256 pruefen und sicher loesen. (d) C3/B7 Klickflaeche der Markierung: nur wenn klein und sicher.
5. BENCH (nur NCBearBench*, nur SP): NCBear_CubWin() oeffnet das Fenster; was Kevin sonst zum Testen braucht.
NICHT in F1: Kampf/Zombie-Angriffe (B5a), Hunger/Durst/Schlaf (F3), Inventar (F4), Spuernase/Fischen-Wirkung (F5), Modell-Dateien, alte
NCBear*-Dateien (nur lesen), NPC-Crew-Beacon-Anbindung.

ORTE: Staging (Pruefgegenstand und Bauort) ${W}/mod/ (Liste ${W}/staging_dateien.txt). Jar-Auszuege ${W}/jar, ${W}/javap, ${W}/dec. Attrappen:
${W}/attrappe/ (kern/, ober/, gesamt/, b1b_* .. b1e_*; lua5.1: C:/Users/Kevin/Tools/lua51/lua5.1.exe). Lua-Pruefer (nur aufrufen): python
${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py, luacheck_pz.py. Uebernahme-Skript ${B}/tools/baer_uebernahme.py (Trockenlauf und
--probe mit --vor-b5a), Naehte ${B}/NAEHTE.md.

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, Vanilla ${VAN} (nur lesen), Bandits ${BAN}/42.22 und
${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen, nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Claude baut nach der Pruefung selbst ein). Kein git, kein
Spielstart, kein Download, nichts hochladen. EISERNE REGEL: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder
Bandits mit GLEICHEN Argumenttypen, im Kommentar genannt; Ausnahme nur mit Kevins Wort je Methode -- erteilt fuer animal:pathToLocation(x, y, z)
und setVariable("animalRunning", ...) am Tier. Ein pcall um einen unbelegten Aufruf ist eine Tarnkappe. SP UND MP: SP-Test "not isServer() and
not isClient()"; was der Server wissen muss, kommt nie aus einem Client-Glauben (Befehle aus dem Fenster gehen als Client-Befehl zum Server, der
Besitz und Lage prueft; im SP direkt rufen). Kevins rote Linien: kein Gegenstand verloren oder verdoppelt, kein Kick (Rolle user, AntiCheat),
nichts haengt endlos, keine NPC-Crew-Figur wird gestoert -- hier zusaetzlich: der Baer geht nie verloren und wird nie verdoppelt. Testbefehle nur
in NCBearBench*.lua (nur SP); das Fenster selbst ist echte Spielmechanik (kein Cheat: keine Knoepfe, die Werte setzen). Namen: BanditsNPCBear*.lua,
Modul BanditsNPC.Bear, Texte UI_BN_Bear_* in EN, PTBR, RU, KO, ES, CN, FR (CN nur Zeichen aus Vanilla-CN), Sandbox BanditsNPC.Bear*; vor jedem
neuen Namen in NPC Crew greppen. Nichts Teures je Bild, Deckel fuer alles, was waechst; Kahlua ist kein echtes Lua 5.1 (kein next). Dateien LF,
ASCII in Lua; localcount aktiv UND insgesamt unter 180 (sonst Datei teilen). Schreibe "statisch geprueft, nicht gespielt"; keine Behauptung ohne
Fundstelle (Datei:Zeile), sonst "ungeprueft".`

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

DEINE ROLLE: FORSCHUNG (nur lesen und belegen, kein Code im Staging). Belege mit Fundstelle (Datei:Zeile, zitierte Zeile, Seite Client/Server/SP):
a) Tasten: wie NPC Crew und Vanilla eine einstellbare Taste anlegen und abfragen (Tastenbelegungs-Liste, OnKeyPressed, Speichern), welche
   Belegungen V schon nutzen (Vanilla keyBinding/Optionen, NPC Crew).
b) Fenster-Bausteine in Vanilla: Fenster mit Titelleiste/Schliessen/Verschieben, Knopf mit Tooltip und grau, Ankreuzfeld, Fortschrittsbalken
   oder selbst gezeichnete Balken (drawRect/drawRectBorder/drawTextureScaled), Schrift-Hoehen je UIFont, Lage merken; ein schoenes Vanilla-Fenster
   als Vorbild (z. B. Tier-Info ISAnimalUI, Charakter-Fenster) mit Fundstellen.
c) Daten im Staging, die das Fenster zeigt: Register/Sicht (B.ViewOf, rec-Felder), Werte (B1d Stats), Faehigkeiten (Stufe + Fortschritt), Alter/
   Stufe, Zaehmung/Vertrauen, Koerper (B1e), Zustand; Befehle Folgen/Bleiben/Call to me/Name und ihr Client->Server-Weg; Abklingzeiten.
d) Sitzen: wie die Test-Mod heute einen Baeren sitzen laesst (NCBear_Sit, AnimSet-Variablen, Clips beider Koerper) -- belegter Weg fuer das
   gezaehmte Tier; Aufstehen. Frei herumlaufen: belegter Weg fuer ziellose Wege in einem Kreis (pathToLocation erlaubt), Takt, Deckel.
e) Unstuck/C1: freie stehbare Kachel finden (wie NPC Crew/Bandits es tun, Fundstellen), PlaceCub/RemoveCub, was bei "nicht geladen" geht.
f) B1e-Reste A1/B6, A5 (Texturdeckel 256: belegt, was mit 288-px-UI-Bildern passiert), C3/B7.
Ergebnis: ${W}/forschung_f1.md (Tabellen Bedarf -> Aufruf -> Fundstelle -> Seite -> Urteil; was NUR mit Jar belegt ist, getrennt; offene Fragen).
Rueckgabe: Kurzfassung mit Kernbelegen und Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung_f1.md ganz, dazu PLAN_B1C.md .. PLAN_B1E.md (Aufbau, Register, Spiegel, Sicht/Sync, Takte) und die
Staging-Dateien, die F1 beruehrt. Schreibe ${W}/PLAN_F1.md:
1. Fenster: Aufbau mit Massen in Pixeln bei 1080 und Faktor fuer 4K, Farben (Zahlen), Schrift je Element, Reihenfolge der Bereiche, Tooltips,
   Zustaende der Knoepfe. Zeichne dazu einen ENTWURF als Bild (Python mit PIL, nur Werkzeug unter ${W}/f1_entwurf/, kein Spiel): ${W}/f1_entwurf/
   fenster_1080.png und fenster_4k.png mit Beispielwerten (Junges Tag 12 und grosser Baer Tag 60), so wie es im Spiel aussehen soll -- schoen,
   ruhig, lesbar; selbst ansehen und verbessern, bis es dir gefaellt.
2. Je Befehl (Folgen, Bleiben, Sitz, Frei, Komm her, Passiv, Unstuck, Name, Namensschild) das Verhalten Schritt fuer Schritt: Ausloeser, Weg
   Client->Server, Pruefungen am Server, Wechselwirkung mit Mitfahren/Verstecken/Laerm/Wachsen-Tausch/Speichern/Laden/Tod/Besitzer offline.
3. B1e-Reste (a)-(d) mit Weg.
4. GENAUE SCHNITTSTELLE fuer zwei getrennte Bauer: KERN (shared/ und server/: Befehle, Zustaende, Sicht-Felder, C1) und OBERFLAECHE (client/
   inkl. ISUI/ Fenster und Taste, Translate in 7 Sprachen, Bench). Jede Funktion mit Name, Parametern, Rueckgabe, Datei; keine Datei fuer beide.
5. Testfaelle fuer die Attrappen (SP und MP-Rundlauf je Befehl, C1 ohne Doppel, Unstuck) und Kevins Testschritte.
6. Belege: jeder geplante Engine-Aufruf mit Fundstelle aus forschung_f1.md; Jar-only ist verboten (ausser pathToLocation, animalRunning).
Rueckgabe: Kurzfassung des Plans mit Dateiliste je Bauer und Pfaden der Entwurfsbilder.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN (shared/ und server/ im Staging ${W}/mod/42/media/lua). Zuerst Staging gegen die Test-Mod nachzaehlen
(staging_dateien.txt, MD5). Setze ${W}/PLAN_F1.md fuer deinen Teil WOERTLICH um; musst du von der Schnittstelle abweichen, sofort nach
${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "F1 KERN") und die Datei vor dem Abschluss lesen. Client-Dateien (lua/client/, Translate,
Bench) gehoeren dem anderen Bauer: nur lesen. Jeder Engine-Aufruf mit Fundstelle im Kommentar (selbst nachgeprueft). Diagnose hinter dem
bestehenden Schalter. Danach: vier Lua-Pruefer auf deine Dateien, Zeilenenden, die bestehenden Attrappen (kern/, gesamt/, b1b_kern .. b1e_kern)
muessen weiter laufen (nur gewollt anpassen, begruenden), neue Faelle je Befehl, C1 ohne Doppel, Unstuck unter ${W}/attrappe/f1_kern/.
Ergebnis: ${W}/bau_f1_kern.md (Dateien, Aenderungen mit Datei:Zeile, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je Befehl,
Pruefer-Ausgaben, Attrappen-Ergebnis, offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE (lua/client/ inkl. ISUI/: das Baeren-Fenster, die Taste, der Menue-Eintrag; Bench NCBearBenchCub.lua; Translate
in sieben Sprachen; im Staging ${W}/mod/42/media/lua; neue Bilder unter ${W}/mod/42/media/ui/ nur wenn noetig, hoechstens 256 px). Setze
${W}/PLAN_F1.md fuer deinen Teil WOERTLICH um und halte dich an den Entwurf ${W}/f1_entwurf/ (Aussehen ist Kevins Hauptwunsch: "das schoene
ui"). Abweichungen sofort nach ${W}/schnittstelle_aenderungen.md ANHAENGEN (Abschnitt "F1 OBERFLAECHE"), vor dem Abschluss lesen. shared/ und
server/ gehoeren dem anderen Bauer: nur lesen. Nichts Teures je Bild. Texte natuerlich je Sprache, gleiche Platzhalter, JSON-Round-Trip
(json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende), sortiert, CN nur Vanilla-CN-Zeichen (pruefen). Danach: vier Lua-Pruefer,
Zeilenenden, bestehende Attrappen (ober/, gesamt/, b1b_ober .. b1e_ober) weiter gruen, neue Faelle unter ${W}/attrappe/f1_ober/ (Fenster baut
sich mit Attrappen-UI auf, alle Knoepfe senden den richtigen Befehl, Texte vorhanden). Zeichne am Ende das Fenster so, wie DEIN Code es
anordnet, noch einmal als ${W}/f1_entwurf/fenster_gebaut_1080.png und _4k.png (gleiche Masse/Farben wie im Code, PIL).
Ergebnis: ${W}/bau_f1_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt, Pruefer-Ausgaben,
offen/ungeprueft). Rueckgabe: Kurzfassung.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const zus = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENBAU + UEBERNAHME. Zwei Bauer haben getrennt gebaut (Berichte ${W}/bau_f1_kern.md, ${W}/bau_f1_oberflaeche.md,
Abweichungen ${W}/schnittstelle_aenderungen.md). 1. Pruefe das Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl hat
Empfaenger am Server, Sicht-Felder passen, jeder Textschluessel in EN und allen Sprachen, Ersatztexte wortgleich) -- Werkzeug wie
${W}/attrappe/gesamt/xref.py; Luecken klein und belegt schliessen. 2. Gesamt-Attrappe ${W}/attrappe/gesamt/run.lua um F1 erweitern (Zaehmen ->
Fenster mit V; jeder Befehl SP und MP-Rundlauf; Sitz/Frei/Folgen wechseln; Passiv gespeichert; Unstuck auch "nicht geladen"; C1: koerperloser
Eintrag bekommt genau einen Koerper, nie zwei; Tausch Tag 15 mit offenem Fenster; Speichern/Laden) und laufen lassen; alle B1a-B1e-Faelle bleiben
gruen. 3. ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md nachziehen (neue Dateien, Texte, Taste, Cheat-Pruefung: Fenster ist keine
Testhilfe, Bench bleibt Bench; Beacon-Naht fuer "Frei" dokumentieren), Trockenlauf und --probe (mit --vor-b5a, Probe nur unter
${W}/probe_f1/). 4. ${W}/staging_dateien.txt neu (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen ${T}) und ${W}/mod_info_vorschlag.txt um F1.
Ergebnis: ${W}/bau_f1_zusammenbau.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:zusammenbau', phase: 'Bau' })
if (!zus) { return { fo, plan, kern, ober, abbruch: 'Zusammenbau ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in F1
geaenderten oder neuen Dateien (Liste aus ${W}/bau_f1_zusammenbau.md und staging_dateien.txt): jeder Engine-Aufruf gegen die genannte Fundstelle
im heutigen Vanilla/Bandits (Datei, Zeile, Argumenttypen, Seite), Jar-only = Befund (ausser pathToLocation/animalRunning); Taste kollisionsfrei
und einstellbar; alte NCBear*-Dateien unveraendert; keine Testbefehle und keine Werte-setzenden Knoepfe ausserhalb der Bench; Texte in sieben
Sprachen (Schluessel, Platzhalter, Round-Trip, CN); Bildgroessen <= 256; Uebernahme-Skript Trockenlauf/Probe selbst laufen lassen; vier
Lua-Pruefer und alle Attrappen selbst laufen lassen und Zahlen nennen. Ergebnis ${W}/pruef_f1_a.md. Rueckgabe strukturiert (id A1...).`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, SP/MP, rote Linien, Leistung UND OPTIK. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen
unter ${W}/attrappe/pruef_f1/. Verfolge jeden Befehl in jedem Zustand (folgt, bleibt, sitzt, frei, versteckt, flieht vor Laerm, faehrt mit,
Call to me/Abklingzeit, Tausch Tag 15, Besitzer offline, zweiter Spieler mit eigenem Baeren, Speichern/Laden, Absturz, koerperloser Eintrag):
kann der Baer verloren gehen oder doppelt entstehen, haengt etwas, kann ein Client fremde Baeren steuern? Kosten je Bild? OPTIK: vergleiche den
Code (Masse, Farben, Schriften, Skalierung bei 3840x2054) mit ${W}/f1_entwurf/fenster_*.png und fenster_gebaut_*.png -- ueberlappt etwas,
wird Text abgeschnitten (laengste Sprache RU/PTBR), ist es bei 4K lesbar, wirkt es schoen und aufgeraeumt? Drei eigene Attrappen-Faelle fuer die
riskantesten Stellen. Ergebnis ${W}/pruef_f1_b.md. Rueckgabe strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, kern, ober, zus, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_f1_a.md, ${W}/pruef_f1_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher (Optik-Befunde
ernst nehmen: Kevin will ein schoenes Fenster); keine neuen unbelegten Aufrufe; Texte immer in sieben Sprachen; Schnittstellen-Aenderung in
${W}/schnittstelle_aenderungen.md anhaengen. Danach ALLES neu: vier Lua-Pruefer auf alle Lua-Dateien des Stagings, Zeilenenden/ASCII,
JSON-Round-Trip, alle Attrappen, Trockenlauf und --probe (--vor-b5a), ${W}/staging_dateien.txt neu, fenster_gebaut_*.png neu, falls sich das
Fenster aenderte. Ergebnis ${W}/nachbesserung_f1.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, kern, ober, zus, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_f1.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (--vor-b5a). staging_dateien.txt gegen die
   Platte nachzaehlen; nachweisen, welche bestehenden Dateien der Test-Mod ueberschrieben wuerden (nur gewollte; alte NCBear*-Dateien nie).
3. Zwei eigene Stichproben (z. B. Unstuck eines nicht geladenen Baeren Zeile fuer Zeile; C1 nach Laden ohne Doppel; Sitz -> Folgen -> Mitfahren).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; V oeffnet das Fenster, Taste umstellbar; Werte und
   Faehigkeiten stimmen mit NCBear_CubStats() ueberein; jeder Befehl wirkt sichtbar; Fenster bei 4K lesbar und schoen; B1a-B1e unveraendert)?
   Blocker nur, was diesen Test verhindert oder eine rote Linie reisst.
Ergebnis ${W}/gegen_bericht_f1.md und Testanleitung ${W}/anleitung_f1_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin, mit Bench-
Befehlen zum Eintippen; Spiel mit -debug neu starten; nur NCBearTest noetig; Hinweis, wo die Taste umgestellt wird; Bild des Fensters
${W}/f1_entwurf/fenster_gebaut_4k.png nennen). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, zus, pa, pb, fix, gegen }
