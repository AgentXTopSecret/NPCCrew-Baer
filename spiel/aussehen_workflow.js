export const meta = {
  name: 'baer-aussehen',
  description: 'Baer: Knopf "Aussehen" im Baerenfenster -- gezaehmter Baer wechselt sein Modell (gross: 2c / Generator braun / Generator Fototon; Junges: Standard / spaeter Generator-Junges) ueber den Koerper-Tausch, echte Spieler-Funktion, SP+MP (8 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Forschung' }, { title: 'Plan' }, { title: 'Bau' }, { title: 'Pruefung' }, { title: 'Nachbesserung' }, { title: 'Gegenpruefung' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const S = W + '/mod_look'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-aussehen" fuer Kevins Mod NPC Crew (Project Zomboid 42.22; Bandits ${BAN}/42.22 und ${BAN}/common). Kevin
programmiert nicht, er spielt und testet. Berichte auf Deutsch, "statisch geprueft, nicht gespielt", jede Behauptung mit Fundstelle (Datei:Zeile).

KEVIN (12.11.2026, woertlich): "koennte man auch ingame einen knopf einbauen wo man das baeren model weckselt? also von einen getamed baeren?" --
"ja fuer spieler als knopf" -- "koennte man das model weckseln abused? z.b als unstuck funktion oder so? wird er dabei geheilt etc?" -- (Start)
"Aussehen-Knopf". FEST (${B}/begleiter/ENTSCHEIDUNGEN.md unten, ${B}/STAND.md): ECHTE Spieler-Funktion (kein Bench), Knopf "Aussehen"/"Look" im
Baerenfenster (Taste E nah, F1/F1b/F2), grosser Baer 2c <-> Generator-Baer braun <-> Generator-Baer Fototon, Junges Standard <-> (spaeter)
Generator-Junges. Weg: derselbe Koerper-Tausch wie beim Wachsen (server/BanditsNPCBearGrow.lua B.BodySwap -> server/BanditsNPCBearRide.lua
B.PlaceCub -> B.CreateCub; Eintrag, Name, Zaehmung, Werte, Leben (rec.hp), Ausdauer (s.sta) bleiben). Jedes Aussehen ist eine eigene Tierart
(ggf. Rasse) mit ENDGUELTIGEM Namen (steht im Spielstand). GEGEN MISSBRAUCH (fest): kein Heilen (Leben/Ausdauer bleiben), Tausch nur wenn
B.BodySwapReady ja sagt (kein Zombie < 9 Kacheln, nicht fahren/fuettern/streicheln, nicht im Kampf/am Boden -- F2), neue Kachel = eigene oder
Ring 1-2 (B.SwapSpot, kein Wegzaubern), Abklingzeit GEMEINSAM mit Unstuck (F1 Unstuck = Call to me). F3 spaeter: Beduerfnisse im Register.
STAND: Test-Mod ${T} (Git main 8a22bf9 = F1 + F1b + F2 + DE) ist 1:1 nach ${S} kopiert = dein Staging (Bauort). Modelle heute in der Test-Mod
(NUR LESEN, nie aendern): 2c NCBear.glb/.png (Art ncbeargrown; parallel laeuft ein Kopfnaht-Lauf, der NCBear.* spaeter ersetzt -- gleiche Namen),
Generator NCBearGen.glb + NCBearGen.png (braun) + NCBearGenFoto.png (Fototon), heute nur ueber die Werkbank NCBear_GenLive (shared/
NCBearBenchGenDefs.lua, client/NCBearBenchGen.lua, scripts/...: dort nur lernen, die echte Funktion braucht eigene NICHT-Bench-Namen fuer Art,
model-Skript und Uebernahme), Junges NCBearCub.glb/.png (Art ncbearcub), altes Junges ncbearcubalt (nur Werkbank). Das Generator-Junge
(Lauf baer-gen-junges-v2, Bench-Name NCBearBenchCubGen.*) ist NOCH NICHT fertig: plane es als spaeteren Daten-Eintrag (eine Zeile + Dateien),
baue heute nur, was es gibt; mit nur einem Aussehen fuer das Junge ist der Knopf beim Jungen grau mit Grund oder unsichtbar (Plan entscheidet).
Kevins Texte: 8 Sprachen (EN, PTBR, RU, KO, ES, CN, FR, DE; DE-Regeln: ${B}/NAEHTE.md, NPC Crew CLAUDE.md "ACHT Sprachen", Pruefer ${NC}/_docs/tools/
langcheck.py, Begriffe: Faehigkeiten, Leben, Herholen, stark; Werkzeuge ${W}/../baer_de/werkzeug/). Uebernahme-Skript ${B}/tools/baer_uebernahme.py
(kennt acht Sprachen; Trockenlauf heute 0 Fehler) und ${B}/NAEHTE.md nachziehen (neue Modell-Dateien/Arten muessen mit nach NPC Crew, Bench nie).
ORTE: schreiben nur in ${S}/, ${W}/aussehen/ (Berichte, Attrappen, Werkzeuge), ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md (nur Rolle
Bau/Nachbesserung). Nie in die Test-Mod, NPC Crew, Vanilla, Bandits oder andere _arbeit-Ordner schreiben; kein git, kein Download, kein Spielstart.
Suchorte nur: ${W}, ${B}, ${T} (lesen), Vanilla ${VAN} (lesen), Bandits (lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs (lesen).
EISERNE REGEL: jeder Engine-Aufruf mit Fundstelle als echter Aufruf in Vanilla-Lua oder Bandits mit GLEICHEN Argumenttypen, im Kommentar; kein pcall
als Tarnkappe. SP UND MP: SP-Test "not isServer() and not isClient()"; der Tausch passiert nur beim Schreiber (Server/SP), der Client bittet nur;
der Server prueft Besitz, Zustand, Abklingzeit selbst. Kevins rote Linien: Baer nie verloren oder verdoppelt, kein Gegenstand verloren/verdoppelt,
kein Kick, nichts haengt endlos. Namen BanditsNPCBear*/UI_BN_Bear_*/BanditsNPC.Bear*, vor jedem neuen Namen in NPC Crew greppen. Testbefehle nur in
NCBearBench*.lua. Lua-Pruefer: python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py, luacheck_pz.py; Attrappen ${W}/attrappe/ (lua5.1
C:/Users/Kevin/Tools/lua51/lua5.1.exe) -- alle bestehenden bleiben gruen.`

const FIND = { type: 'object', properties: { zusammenfassung: { type: 'string' }, findings: { type: 'array', items: { type: 'object',
  properties: { id: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, datei: { type: 'string' }, zeile: { type: 'string' },
    behauptung: { type: 'string' }, beleg: { type: 'string' }, vorschlag: { type: 'string' } },
  required: ['id', 'schwere', 'datei', 'behauptung', 'beleg', 'vorschlag'] } } }, required: ['zusammenfassung', 'findings'] }
const VERDICT = { type: 'object', properties: { bereit_fuer_sp_test: { type: 'boolean' }, zusammenfassung: { type: 'string' },
  offene_blocker: { type: 'array', items: { type: 'string' } }, restbefunde: { type: 'array', items: { type: 'string' } },
  fragen_an_kevin: { type: 'array', items: { type: 'string' } }, staging_dateien: { type: 'integer' } },
  required: ['bereit_fuer_sp_test', 'zusammenfassung', 'offene_blocker', 'restbefunde', 'staging_dateien'] }

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG. Lies den Koerper-Tausch (Grow/Ride/World/Stats/Defs), B1e-Plan ${W}/PLAN_B1E.md, F1/F1b/F2-Fenster (client/ISUI/
BanditsNPCBearWindow.lua, WinParts, WinData) und die Werkbank NCBearBenchGen*. Klaere mit Belegen: wie eine neue Tierart/Rasse definiert wird (Form
wie ncbeargrown, copyOf), ob ein Aussehen besser Art oder Rasse ist (addAnimal mit Rasse belegt?), wie B.BodyKind/B.TYPE_BODY/B.BODY_TYPE erweitert
werden, wie Spiegel/Waisen/Selbstheilung (C1) mit mehreren Arten je Koerper umgehen, wie Unstuck seine Abklingzeit fuehrt, wie ein Client-Befehl im MP
zum Schreiber kommt (vorhandene Befehle des Fensters), was das Uebernahme-Skript fuer neue Modell-Dateien braucht. Ergebnis ${W}/aussehen/FORSCHUNG.md.
Rueckgabe: Kurzfassung mit Kernbelegen und Luecken.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/aussehen/FORSCHUNG.md. Schreibe ${W}/aussehen/PLAN_AUSSEHEN.md: endgueltige Art-/Rassen-Namen je Aussehen, Datentabelle
(ein Eintrag je Aussehen, Generator-Junges als spaetere Zeile), Register-Feld fuer das Aussehen, Tausch-Ablauf (Bitte vom Client, Pruefungen beim
Schreiber, gemeinsame Abklingzeit mit Unstuck, Meldungen), Wachsen bei Tag 15 behaelt das gewaehlte Aussehen (Junges->gross: passendes grosses
Aussehen?), Fenster (Knopf mit Name des Aussehens, Restzeit, grauer Grund), Rechtsklick ja/nein, Sandbox-Schalter ja/nein, Texte 8 Sprachen, Bench-
Befehle, Uebernahme/Naehte, Attrappen-Faelle, SP/MP. Zwei Bauer mit getrennten Dateien: KERN (shared/server, Defs, model-Skripte, Uebernahme) und
OBERFLAECHE (client, Fenster, Texte, Bench). Kleinfragen mit Empfehlung bauen und als "Fragen fuer Kevin" fuehren. Rueckgabe: Kurzfassung mit Dateiliste.`,
  { label: 'plan', phase: 'Plan' })
if (!plan) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN laut ${W}/aussehen/PLAN_AUSSEHEN.md (shared/, server/, scripts/, Defs; dazu ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md).
Client-Dateien gehoeren dem anderen Bauer (nur lesen). Abweichungen nach ${W}/aussehen/schnittstelle.md ANHAENGEN (Abschnitt KERN), vor Abschluss
lesen. Vier Lua-Pruefer, alle Attrappen gruen, neue Faelle unter ${W}/attrappe/aussehen_kern/, Trockenlauf (--staging ${S}). Bericht ${W}/aussehen/
BAU_KERN.md. Rueckgabe: Kurzfassung.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE laut ${W}/aussehen/PLAN_AUSSEHEN.md (client/ inkl. ISUI, Texte in 8 Sprachen, Bench NCBearBench*). shared/server
gehoeren dem anderen Bauer (nur lesen). Abweichungen nach ${W}/aussehen/schnittstelle.md ANHAENGEN (Abschnitt OBERFLAECHE), vor Abschluss lesen.
Fenster-Bild ${W}/aussehen/fenster_aussehen_1080.png (PIL, Masse/Farben wie im Code). Vier Lua-Pruefer, Texte-Pruefer (8 Sprachen, langcheck),
Attrappen gruen, neue Faelle unter ${W}/attrappe/aussehen_ober/. Bericht ${W}/aussehen/BAU_OBER.md. Rueckgabe: Kurzfassung.`,
    { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { fo, plan, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Texte, Uebernahme, Zusammenpassen ueber die Grenze (jede B.*-Benutzung definiert, jeder Befehl mit
Empfaenger, Textschluessel in 8 Sprachen). Du aenderst nichts ausser deinem Bericht. Pruefer und Attrappen selbst laufen lassen, Trockenlauf und
--probe (Probe nur unter ${W}/aussehen/probe/). Bericht ${W}/aussehen/PRUEF_A.md. Rueckgabe strukturiert (id A1...).`,
    { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, Missbrauch, SP/MP, rote Linien. Du aenderst nichts ausser deinem Bericht und eigenen Attrappen unter
${W}/attrappe/aussehen_pruef/. Verfolge: Wechsel bei vollem/halbem Leben (kein Heilen), mit Zombie in der Naehe, im Kampf/am Boden (F2), beim Fahren,
Fuettern, Streicheln, waehrend Unstuck-Abklingzeit, kurz vor Tag 15 (Wachsen), Speichern/Laden direkt danach, Absturz mitten im Tausch (C1-
Selbstheilung, nie zwei Koerper), Besitzer offline, fremder Spieler drueckt, MP-Bitte mit falschen Daten. Drei eigene Attrappen-Faelle fuer die
riskantesten Stellen. Bericht ${W}/aussehen/PRUEF_B.md. Rueckgabe strukturiert (id B1...).`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde: ${JSON.stringify(befunde, null, 1)}
Jeden selbst am Code nachpruefen, falsche mit Beleg ablehnen, blocker/major beheben, minor wenn klein und sicher; Texte immer in 8 Sprachen. Danach
alles neu: Pruefer, Attrappen, Trockenlauf/--probe, Liste ${W}/aussehen/staging_dateien_look.txt (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen
${T}; Modell-Dateien, die die Test-Mod inzwischen neuer hat, als "ueberschreibt (NICHT KOPIEREN: ...)"), mod.info-Vorschlag
${W}/aussehen/mod_info_vorschlag_look.txt. Bericht ${W}/aussehen/NACHBESSERUNG.md. Rueckgabe: je Befund-ID Kurzfassung.`,
  { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut und glaubst keinem Bericht. Befunde: ${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere,
datei: f.datei, behauptung: f.behauptung })), null, 1)}. Nachbesserung: ${W}/aussehen/NACHBESSERUNG.md. Je Befund geschlossen? Etwas kaputt gemacht?
Pruefer, Attrappen, Trockenlauf/--probe selbst laufen lassen, staging_dateien_look.txt gegen die Platte nachzaehlen, zwei eigene Stichproben
(Tausch mit halbem Leben; Absturz mitten im Tausch). Urteil bereit fuer Kevins Einzelspieler-Test? Bericht ${W}/aussehen/GEGEN.md und Testanleitung
${W}/aussehen/anleitung_entwurf.md (Deutsch, kurz, Schritt fuer Schritt mit Befehlen; Spiel mit -debug neu starten). Rueckgabe strukturiert.`,
  { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, plan, kern, ober, pa, pb, fix, gegen }
