export const meta = {
  name: 'baer-gen-gross-v2',
  description: 'Generator-Baer (grosser Vergleichsbaer) schoener: Gesicht/Nase breiter und kraeftiger, schwarze Unterarme weg, Fell -- Plan, 2 Bauer, 2 Pruefer, Nachbesserung, Gegenpruefer (7 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Plan' }, { title: 'Bau' }, { title: 'Pruefung' }, { title: 'Nachbesserung' }, { title: 'Gegenpruefung' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const GG = N + '/_arbeit/baer_gen_gross'
const V2 = GG + '/v2'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'

const CTX = `Du arbeitest im Lauf "baer-gen-gross-v2" an Kevins Baeren-Mod (NPC Crew, Project Zomboid). Berichte auf Deutsch, "statisch geprueft,
nicht gespielt". Kevin (12.11.2026, woertlich): "ja mach den eignen model lauf wo du den verbesserst besonders sein gesicht (nase) die ist voll
schmall und so". Gemeint ist der GROSSE GENERATOR-BAER (aus Foto E), der als Vergleich per NCBear_GenLive() in der Test-Mod steht.

STAND (zuerst lesen): der Lauf baer-gen-gross (${GG}/: Skript workflow_baer_gen_gross.js, Berichte *.md, Ergebnis out/, fix1/) hat ihn auf das
2c-Skelett gesetzt (alle 15 2c-Clips byte-gleich, braun + Fototon); Urteil des Gegenpruefers: technisch sauber, aber "insgesamt NICHT schoener
als der 2c" (u. a. schwarze Unterarme). Generator-Herkunft ${N}/_arbeit/baer_gen/ (E_FEIN.md, GEGEN_OPTIK.md: helles Gesicht/Maske, Fell wie
Filz). Foto ${B}/begleiter/vorlage_E_gross.jpg, Referenzen ${B}/begleiter/ref_*.jpg (u. a. aufrecht/hinten). Der 2c-Baer
(${T}/42/media/models_X/Skinned/NCBear.glb) ist der Vergleich, dessen Kopf Kevin gut fand.

ZIEL: Der Generator-Baer wird SCHOENER, vor allem das GESICHT: Nase/Schnauze deutlich BREITER und kraeftiger wie bei einem echten Braunbaeren
(breiter Nasenruecken, grosse dunkle Nase mit Nasenloechern, kraeftige helle Schnauze, Augen dunkel und sichtbar), Kopf nicht zu hell
(keine Maske), Uebergang Kopf->Hals ohne Rand; schwarze Unterarme in Fellfarbe (dunkle Beine wie im Foto, aber kein Schwarz-Block); Fell mit
gerichtetem Strichmuster statt Filz. Form am Foto und an Kevins Spielkamera (Azimut 0, Hoehe 30 Grad, Spielgroesse ~140 px) messen.

FESTE REGELN: gleiche 26 Knochen und 15 Clips wie der 2c-Baer (byte-gleich, nur Netz/Gewichte/Textur aendern), <= 20.000 Dreiecke, 1 Netz,
1 Material, <= 4 Einfluesse, Textur 1024 RGB, Dehnung 99,5 % <= 2,6 / max <= 4,0 / Achsel <= 3,5, Boden <= 1,5 cm, gleiche Dateinamen wie heute
(beide Farbvarianten). Importer-Harness ${N}/_arbeit/baer_spiel/harness vor "fertig". Jedes Blatt SELBST ansehen; kein Schoenreden.
ORTE: arbeiten nur unter ${V2}/ (Unterordner je Rolle), neue Skripte ${B}/spiel/baer_*_gg2.py (Originale nie aendern). Ergebnis unter ${V2}/out/
mit GENAU den Pfaden/Namen, die das Vergleichs-Modell heute in der Test-Mod hat (aus den gen-gross-Berichten bzw. ${T} ermitteln) + md5.txt.
Nie in Test-Mods, NPC Crew oder das Spiel schreiben; kein git, kein Download. Suchorte nur ${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla
media (lesen). Blender 5.2.3 C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe headless; GPU-Sperre ${N}/_arbeit/baer_gen/gpu.lock
(mkdir/rmdir, existiert sie: warten -- ein anderer Lauf rendert parallel); ComfyUI nur wenn noetig, lokal 127.0.0.1:8188, nur eigenen Prozess beenden.
Befehle ueber 2 Minuten im Hintergrund.`

const MANGEL = { type: 'object', properties: { urteil: { type: 'string' }, maengel: { type: 'array', items: { type: 'object',
  properties: { id: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, wo: { type: 'string' },
    beschreibung: { type: 'string' }, vorschlag: { type: 'string' } }, required: ['id', 'schwere', 'wo', 'beschreibung', 'vorschlag'] } } },
  required: ['urteil', 'maengel'] }
const VERDICT = { type: 'object', properties: { schoener_als_vorher: { type: 'boolean' }, kevin_zeigen: { type: 'boolean' },
  zusammenfassung: { type: 'string' }, rest_maengel: { type: 'array', items: { type: 'string' } }, dateien: { type: 'array', items: { type: 'string' } } },
  required: ['schoener_als_vorher', 'kevin_zeigen', 'zusammenfassung', 'rest_maengel', 'dateien'] }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies den Stand, miss Kopf/Schnauze/Nase am heutigen Modell und am Foto (Breite Nasenruecken/Schnauze relativ zur Kopfbreite,
Nasengroesse, Augenlage), sieh die heutigen Renders aus Kevins Kamera an und schreibe ${V2}/PLAN.md: Soll-Masse fuer Gesicht/Nase (Zahlen),
Weg fuer die Form (Netz-Verformung am Kopf mit glatten Uebergaengen, Gewichte am Kopf mitfuehren), Textur-Weg (Unterarme, Gesicht-Helligkeit,
Fellstriche), Pruefliste. Zwei Bauer: GESICHT (Form + Gesichts-Textur) und FELL (Unterarme, Fell, Farbvarianten) -- getrennte Dateien,
Uebergabe-Reihenfolge. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const gesicht = await agent(`${CTX}

DEINE ROLLE: BAUER GESICHT laut ${V2}/PLAN.md (Ordner ${V2}/gesicht/). Nase/Schnauze breiter und kraeftiger, Nase gross und dunkel, Augen sichtbar,
Kopf nicht hell, Uebergang zum Hals glatt; Gewichte am Kopf weiter sauber; Blatt ${V2}/bilder/gesicht.png (Kopf nah von vorn, schraeg, Seite,
aus Kevins Kamera gross und in Spielgroesse, neben dem Foto und dem 2c-Kopf) SELBST ansehen und nachbessern. Bericht ${V2}/GESICHT.md.
Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:gesicht', phase: 'Bau' })
if (!gesicht) { return { plan, abbruch: 'Gesicht ohne Ergebnis' } }
const fell = await agent(`${CTX}

DEINE ROLLE: BAUER FELL + EXPORT laut ${V2}/PLAN.md (Ordner ${V2}/fell/), auf dem Stand des Gesichts-Bauers (${V2}/GESICHT.md). Unterarme in
Fellfarbe statt Schwarz-Block, Fell mit gerichtetem Strichmuster, beide Farbvarianten; Export nach ${V2}/out/ (gleiche Namen wie heute), Harness,
alle festen Regeln messen, Blatt ${V2}/bilder/fell.png (8 Seiten gross + Spielgroesse, Aufrichten, Gehen) SELBST ansehen. Bericht ${V2}/FELL.md.
Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:fell', phase: 'Bau' })
if (!fell) { return { plan, gesicht, abbruch: 'Fell ohne Ergebnis' } }

phase('Pruefung')
const [po, pt] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER OPTIK. Du hast nichts gebaut. Rendere SELBST ${V2}/out (beide Farben) gegen das heutige Vergleichs-Modell und den 2c-Baeren:
Gesicht nah, 8 Seiten, Spielgroesse, Gehen/Aufrichten/Sitzen aus Kevins Kamera. Ist die Nase jetzt breit und kraeftig wie im Foto? Urteile hart.
Bericht ${V2}/PRUEF_OPTIK.md. Rueckgabe strukturiert.`, { label: 'pruef:optik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER TECHNIK. Du hast nichts gebaut. Miss SELBST alle festen Regeln an ${V2}/out (beide Farben), Harness, Clips byte-gleich mit dem
2c-Baeren, Namen/Pfade wie das heutige Vergleichs-Modell. Bericht ${V2}/PRUEF_TECHNIK.md. Rueckgabe strukturiert.`, { label: 'pruef:technik', phase: 'Pruefung', schema: MANGEL }),
])
const maengel = [...((po && po.maengel) || []), ...((pt && pt.maengel) || [])]

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Maengel: ${JSON.stringify(maengel, null, 1)}
Selbst nachpruefen, blocker/major beheben (Skripte der Bauer), minor wenn klein; vorher ${V2}/out nach ${V2}/out_vor_fix sichern; neu exportieren,
Harness, Regeln messen, Blaetter neu, selbst ansehen. Bericht ${V2}/NACHBESSERUNG.md. Rueckgabe: Kurzfassung.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut. Rendere und miss SELBST ${V2}/out. Je Mangel der Pruefer: geschlossen? Dann: ist der Baer
schoener als vorher (schoener_als_vorher) und so schoen, dass man ihn Kevin zeigen kann (kevin_zeigen)? Blatt fuer Kevin
${V2}/bilder/KEVIN_gen_gross_v2.png (oben Foto + neu aus Kevins Kamera gross; Gesicht nah alt gegen neu gegen 2c; 8 Seiten Spielgroesse;
Gehen/Aufrichten). Bericht ${V2}/GEGEN.md. Rueckgabe strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { plan, gesicht, fell, po, pt, fix, gegen }
