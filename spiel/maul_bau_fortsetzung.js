export const meta = {
  name: 'baer-maul-bau-fortsetzung',
  description: 'FORTSETZUNG ohne Lauf-Cache (ab Gegenpruefung): Offenes Maul beider grossen Baeren (2c + Generator) nach PLAN_MAUL.md bauen: gerollte Lefze, Mundwinkel bis unters Auge, Gebiss/Zunge/Gaumen neu -- W, G||T, PT||PO, N, GP, I (8 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Rahmen' }, { title: 'Bau' }, { title: 'Pruefung' }, { title: 'Nachbesserung' }, { title: 'Gegenpruefung' }, { title: 'Integrator' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const M = N + '/_arbeit/baer_maul'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'

const CTX = `Lauf "baer-maul-bau" an Kevins Baeren-Mod (Project Zomboid). Deutsch, "statisch geprueft, nicht gespielt".
Kevin (12.11.2026): "und bei beiden baeren sieht der mund schonn scheisse aus das muss besser werden guck dir dazu vllt bilder an wie nen baeren maul
aussieht wenn er das maul offen hat". Forschung ${M}/FORSCHUNG.md (Maengel 1-16, Soll-Zahlen) und Plan ${M}/PLAN_MAUL.md sind FERTIG -- ganz lesen,
der Plan gilt WOERTLICH (Abschnitt 5 = deine Rolle, Schnittstellen fest).
KEVINS ANTWORTEN (12.11., zu PLAN 7): K2 Mundwinkel 1,5-2,5 cm weiter nach hinten bis unter das Auge: JA. K4 dunkle Lippenlinie auch bei
geschlossenem Maul (2c neu): JA. K1 Generator-Baer bekommt das neue Aufrichten/Bruellen: "erstmal so lassen und angucken" -> NICHT in diesem Lauf
(Maul-Proben trotzdem gegen beide Clip-Saetze, PLAN 1.3). K3 Kinn: nicht in diesem Lauf. K5: drei freie Fotos liegen jetzt auf der Platte (nur
ansehen, nie in Modell/Textur): ${B}/begleiter/ref_maul/ref_maul_1.jpg (Kodiak, offen von vorn, gemeinfrei USFWS), ref_maul_2.jpg (zwei Baeren,
offen von der Seite, gemeinfrei USFWS), ref_maul_3.jpg (Seite zu, schwarze Lippenlinie bis unters Auge, CC BY-SA Malene Thyssen); dazu Kevins
Vorlage ${B}/begleiter/kevin_bruellen_vorlage.webp (nur ansehen).
EINGANG (PLAN 1.1): 2c = ${N}/_arbeit/baer_kopfnaht/mod/42/media/ (Abgabe des fertigen Kopfnaht-Laufs; MD5 im Eingangs-Tor neu festhalten -- sie
koennen von den Zahlen im Plan abweichen, wenn die Nachbesserung des Kopfnaht-Laufs noch etwas geaendert hat: dann Tor-Regel 1.2 anwenden), Gen =
${N}/_arbeit/baer_gen_gross/v2/out_schmal/42/media/ (Kevins schmale Nase, in NCBearTest eingebaut; f58ea4c9 / 1fe9c54b / 29c3c7d7).
ORTE: schreiben nur unter ${M}/bau/ (Unterordner je Rolle) und ${M}/bilder/. Nie in Test-Mods, NPC Crew, das Spiel, baer_kopfnaht oder
baer_gen_gross schreiben; kein git, kein Download. Suchorte nur ${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla media (lesen). Blender 5.2.3
C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe headless, GPU-Sperre ${N}/_arbeit/baer_gen/gpu.lock (mkdir/rmdir; besteht sie:
warten -- andere Laeufe rendern parallel), Harness ${N}/_arbeit/baer_spiel/harness. Befehle ueber 2 Minuten im Hintergrund. Jedes Bild SELBST
ansehen; erst Form im Ton richtig, dann Textur; kein Schoenreden.`

const MANGEL = { type: 'object', properties: { urteil: { type: 'string' }, maengel: { type: 'array', items: { type: 'object',
  properties: { id: { type: 'string' }, baer: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, wo: { type: 'string' },
    beschreibung: { type: 'string' }, vorschlag: { type: 'string' } }, required: ['id', 'schwere', 'wo', 'beschreibung', 'vorschlag'] } } },
  required: ['urteil', 'maengel'] }
const VERDICT = { type: 'object', properties: { c2_empfohlen: { type: 'boolean' }, gen_empfohlen: { type: 'boolean' }, kevin_zeigen: { type: 'boolean' },
  zusammenfassung: { type: 'string' }, rest_maengel: { type: 'array', items: { type: 'string' } } },
  required: ['c2_empfohlen', 'gen_empfohlen', 'kevin_zeigen', 'zusammenfassung', 'rest_maengel'] }

// FORTSETZUNG (13.11.2026, ohne Lauf-Cache): W, G, T, PT, PO und N liefen im Lauf wf_a876c805-e76 (Sitzung d5933cc7) und liegen als Berichte vor.
log('Fortsetzung ab Gegenpruefung: W/G/T/PT/PO/N aus Dateien')
const w = `Rahmen ist fertig: ${M}/bau/w/BAU_RAHMEN.md (ganz lesen).`
const g = `Gebiss ist fertig: ${M}/bau/g/BAU_GEBISS.md (ganz lesen).`
const t = `Textur ist fertig: ${M}/bau/t/BAU_TEXTUR.md (ganz lesen).`
const pt = `Pruefer Technik ist fertig: ${M}/bau/pt/PRUEF_TECHNIK.md (ganz lesen).`
const po = `Pruefer Optik ist fertig: ${M}/bau/po/PRUEF_OPTIK.md (ganz lesen).`
const fix = `Nachbesserung ist fertig: ${M}/bau/NACHBESSERUNG.md (ganz lesen). FORTSETZUNG: Zwischenstaende pruefen, nur Vollstaendiges weiterverwenden; liegt schon ein ${M}/bau/GEGEN.md vom abgebrochenen Gegenpruefer, nur als Hinweis lesen und selbst neu pruefen.`

phase('Gegenpruefung')
const gp = await agent(`${CTX}

DEINE ROLLE: GP -- GEGENPRUEFER (PLAN 5 Zeile 7). Du hast nichts gebaut. Unabhaengig: Regeln, Bilder, Kevins Kamera; je Mangel der Pruefer
geschlossen? Ist das Maul beider Baeren klar besser und nah an Vorlage/Fotos? Empfehlung je Baer (c2_empfohlen, gen_empfohlen) und ob man es Kevin
zeigen kann. Bericht ${M}/bau/GEGEN.md. Rueckgabe strukturiert.`, { label: 'GP:gegen', phase: 'Gegenpruefung', schema: VERDICT })
if (!gp) { return { w, g, t, pt, po, fix, abbruch: 'Gegenpruefung ohne Ergebnis' } }

phase('Integrator')
const integ = await agent(`${CTX}

DEINE ROLLE: I -- INTEGRATOR (PLAN 5 Zeile 8; NICHT in die Test-Mod). Urteil des Gegenpruefers: ${JSON.stringify(gp)}. Staging je empfohlenem Baer
${M}/bau/out_c2/ (5 Dateien) und ${M}/bau/out_gen/ (3 Dateien) mit md5.txt und gleichen relativen Pfaden wie in ${T}; Blatt fuer Kevin
${M}/bilder/KEVIN_maul.png (oben ref_maul_1 + neu aus Kevins Kamera gross beim Bruellen; Maul nah alt gegen neu je Baer: Bruellen, Biss, Fressen,
zu; Seite; Spielgroesse) -- Kevins Stockfoto-Vorlage NICHT ins Blatt; Bericht ${M}/BAU_MAUL.md (Dateien, MD5, Wiederhol-Befehle, SP/MP: nur
Modell-Dateien, Naht-Text-Vorschlag). Rueckgabe: Kurzfassung mit MD5 je Datei.`, { label: 'I:integrator', phase: 'Integrator' })

return { w, g, t, pt, po, fix, gp, integ }
