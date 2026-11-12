export const meta = {
  name: 'baer-maul-bau',
  description: 'Offenes Maul beider grossen Baeren (2c + Generator) nach PLAN_MAUL.md bauen: gerollte Lefze, Mundwinkel bis unters Auge, Gebiss/Zunge/Gaumen neu -- W, G||T, PT||PO, N, GP, I (8 Agenten; nichts in die Test-Mod)',
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

phase('Rahmen')
const w = await agent(`${CTX}

DEINE ROLLE: W -- RAHMEN + AUSSENHAUT (PLAN 5 Zeile 1, Abschnitte 1.2, 3.1-3.3, 3.5, 3.6, 2.2/2.3 Aussenhaut-Teil). Eingangs-Tor zuerst; dann Profile,
fleck_karte.json, "leeres" GLB je Baer (Loch + neuer Mundwinkel bis unters Auge + Eck-Gewichte) mit Dehnungs- und Ruhe-Beweis, Zusammenbau-Kette
mt_bau.sh mit Platzhalter-Teilen. Bericht ${M}/bau/w/BAU_RAHMEN.md. Rueckgabe: Kurzfassung mit Zahlen (Tor-MD5, Dreieck-Haushalt je Baer).`,
  { label: 'W:rahmen', phase: 'Rahmen' })
if (!w) { return { abbruch: 'Rahmen ohne Ergebnis' } }

phase('Bau')
const [g, t] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: G -- GEBISS-BAUSTEIN (PLAN 5 Zeile 2, Abschnitte 2.2-2.8, 3.4, 3.6) auf dem Rahmen von W (${M}/bau/w/BAU_RAHMEN.md). In Runden: Lefze +
Winkel im Ton gegen Vorlage/Fotos, dann Zaehne, dann Zunge/Gaumen; nach jeder Runde Probe und Ton-Render (Kevins Kamera, vorn, Seite) neben
ref_maul_1/2 und Kevins Vorlage. Bericht ${M}/bau/g/BAU_GEBISS.md. Rueckgabe: Kurzfassung mit Zahlen (Masse 2.1 je Baer, Proben).`,
    { label: 'G:gebiss', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: T -- TEXTUR (PLAN 5 Zeile 3, Abschnitt 3.7, dazu K4: dunkle Lippenlinie auch bei geschlossenem Maul beim 2c) auf dem Rahmen von W
(${M}/bau/w/BAU_RAHMEN.md, fleck_karte.json). 2c Body + WorldItems, Gen braun + Fototon; nur die Zonen Z4/Z5 aendern (Texel-Diff-Beweis).
Bericht ${M}/bau/t/BAU_TEXTUR.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'T:textur', phase: 'Bau' }),
])
if (!g || !t) { return { w, g, t, abbruch: 'Bauer ohne Ergebnis' } }

phase('Pruefung')
const [pt, po] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PT -- PRUEFER TECHNIK (PLAN 5 Zeile 4, Regeln Abschnitt 4 R1-R12). Du hast nichts gebaut. Baue den Ausgang mit mt_bau.sh selbst,
miss alle Regeln je Baer unabhaengig (eigene Proben, eigener Harness-Lauf, Durchstiche bei geschlossenem Maul in allen 15 Clips beider Clip-Saetze).
Bericht ${M}/bau/pt/PRUEF_TECHNIK.md. Rueckgabe strukturiert.`, { label: 'PT:technik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${CTX}

DEINE ROLLE: PO -- PRUEFER OPTIK (PLAN 5 Zeile 5, Pruefliste Abschnitt 6). Du hast nichts gebaut. Rendere selbst beide Baeren (Bruellen-Hoehepunkt,
Biss, Fressen, Maul zu; Kevins Kamera gross + Spielgroesse, vorn, schraeg, Seite) neben ref_maul_1/2/3 und Kevins Vorlage; Urteil je Mangel 1-16 der
FORSCHUNG. Urteile hart. Bericht ${M}/bau/po/PRUEF_OPTIK.md. Rueckgabe strukturiert.`, { label: 'PO:optik', phase: 'Pruefung', schema: MANGEL }),
])
const maengel = [...((pt && pt.maengel) || []), ...((po && po.maengel) || [])]

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: N -- NACHBESSERUNG (PLAN 5 Zeile 6). Maengel: ${JSON.stringify(maengel, null, 1)}
Selbst nachpruefen, blocker/major beheben (nur in ${M}/bau/w|g|t/), minor wenn klein; mt_bau.sh neu, Regeln messen, Bilder neu, selbst ansehen.
Bericht ${M}/bau/NACHBESSERUNG.md. Rueckgabe: Kurzfassung je Mangel-ID.`, { label: 'N:nachbesserung', phase: 'Nachbesserung' })

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
