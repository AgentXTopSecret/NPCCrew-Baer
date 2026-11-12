export const meta = {
  name: 'baer-gen-junges-v2',
  description: 'Generator-Junges (Foto C) schoener: vor allem Beine/Gang (kein Giraffen-Gang, Baerenfuesse), Gesicht/Maul groesser -- Plan, 2 Bauer, 2 Pruefer + Bench-Staging, Nachbesserung, Gegenpruefer (8 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Plan' }, { title: 'Bau' }, { title: 'Pruefung' }, { title: 'Nachbesserung' }, { title: 'Gegenpruefung' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const GJ = N + '/_arbeit/baer_gen_junges'
const V2 = GJ + '/v2'
const RIG = N + '/_arbeit/baer_gen/rig'
const JF = N + '/_arbeit/baer_junges_fuss'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'

const CTX = `Du arbeitest im Lauf "baer-gen-junges-v2" an Kevins Baeren-Mod (NPC Crew, Project Zomboid). Berichte auf Deutsch, "statisch geprueft,
nicht gespielt". Kevin (12.11.2026, woertlich): "starte noch einen workflow fuer den anderen baby baeren mach da auch das gesicht besser und vorallem
die beine". Gemeint ist das GENERATOR-JUNGE (aus Foto C), NICHT das heutige Standard-Junge. Kevin 11.11. dazu: "besonders die gesichtsgroesse sieht zu
klein aus also das maul" und "der neue baby baer laeuft auch wie eine giraffe oder so xD also das alte ist definitiv besser" -- darum flog es 11.11.
aus der Mod (heute in keiner Test-Mod-Datei).

STAND (zuerst lesen): Generator-Junges = ${RIG}/out/42/media/models_X/Skinned/NCBearCub.glb (md5 ee7a0cce) + .../textures/Body/NCBearCub.png
(92a829fa); 26 Knochen, 15 Clips wie der Erwachsene, Gehen 1,60 Kacheln/s. Berichte ${RIG}/*.md (v. a. GEGEN.md: Kopf gesenkt, Gesicht aus Kevins
Kamera klein unten, Ohren von vorn wie Scheiben, Fressen ~18 cm ueber dem Boden, von hinten "Ei auf Stelzen", Pfoten rutschen ueber 0,35) und
${B}/spiel/rig_*.md, Skripte ${B}/spiel/baer_*_rig.py (nur lesen). Generator-Herkunft ${N}/_arbeit/baer_gen/ (C_FEIN.md, c_fein/).
Das Standard-Junge in der Test-Mod (${T}/42/media/models_X/Skinned/NCBearCub.glb d9931d32 = altes Junges + Baerenfuesse): Kevin findet sein Gesicht
suess und den Gang normal -- das ist die Messlatte. Wie die Baerenfuesse/Beine dort hinkamen (2c-Beine in den Junges-Massstab, Sitz-Clips aus den
2c-Clips umgerechnet + Korrektur-Schicht): ${JF}/PLAN_JFUSS.md, FORM.md, CLIPS.md, NACHBESSERUNG.md, GEGEN.md und ${JF}/werkzeug (nur lesen).
Grosser 2c-Baer ${T}/42/media/models_X/Skinned/NCBear.glb (08ec7806). Vorlagen ${B}/begleiter/: vorlage_C_junges_steht.jpg (Foto C),
vorlage_A_junges.jpg, kevin_babygesicht_vorlage.webp, kevin_baerenfuss_vorlage.png, kevin_pfotenvorlage.png, kevin_sitzvorlage.png.

ZIEL: VOR ALLEM DIE BEINE: kurze, kraeftige Junges-Beine statt Stelzen (Proportion wie Foto C / echte Baerenjunge, Bauch naeher am Boden), echte
Baerenfuesse (runde dunkle Sohlen, Krallen, wie das Standard-Junge), Gang wie ein tapsiges Junges statt Giraffe (Schrittlaenge/Tempo zum kurzen Bein,
Pfoten haften am Boden, nichts schwebt, kein Rutschen bei 0,35), von hinten kein Ei auf Stelzen. DAZU DAS GESICHT: Schnauze/Maul deutlich groesser,
Kopf aus Kevins Kamera nicht gesenkt (Gesicht gut sichtbar), Augen dunkel und sichtbar, Ohren rund statt Scheiben, suess (Babygesicht-Vorlage);
Fressen erreicht den Boden. Messlatte: Foto C, Kevins Kamera (Azimut 0, Hoehe 30 Grad) in Spielgroesse (Groesse 0,35), daneben das Standard-Junge.

FESTE REGELN: 26 Knochen mit denselben NAMEN und 15 Clips mit denselben NAMEN wie heute (AnimSet buck). Clip-INHALT darf neu sein (Umrechnung auf
die kurzen Beine wie in baer-junges-fuss, wiederholbar per Skript). <= 20.000 Dreiecke, 1 Netz, 1 Material, <= 4 Einfluesse, Textur 1024 RGB,
Dehnung 99,5 % <= 2,6 / max <= 4,0 / Achsel <= 3,5, Boden <= 1,5 cm, keine offenen Kanten/Risse in allen Bildern. Gang-Tempo (Gehen/Rennen in
Kacheln/s bei 0,35) messen und melden -- den Code (walkSpeed) NICHT aendern, nur die Zahl nennen. Importer-Harness ${N}/_arbeit/baer_spiel/harness
vor "fertig". Jedes Blatt SELBST ansehen; kein Schoenreden.
ORTE: arbeiten nur unter ${V2}/ (Unterordner je Rolle), neue Skripte ${B}/spiel/baer_*_gj2.py (Originale nie aendern). Ergebnis unter ${V2}/out/ mit
den BENCH-Namen 42/media/models_X/Skinned/NCBearBenchCubGen.glb und 42/media/textures/Body/NCBearBenchCubGen.png + md5.txt (das Generator-Junge kommt
nur als Vergleich per Testbefehl zurueck). Nie in Test-Mods, NPC Crew oder das Spiel schreiben; kein git, kein Download. Suchorte nur
${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla media (lesen), Bandits (lesen), NPC Crew 42/media/lua (nur greppen). Blender 5.2.3
C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe headless; GPU-Sperre ${N}/_arbeit/baer_gen/gpu.lock (mkdir/rmdir; existiert sie:
warten -- andere Laeufe rendern parallel). ComfyUI nur wenn noetig (lokal 127.0.0.1:8188, nur eigenen Prozess beenden). Befehle ueber 2 Minuten im
Hintergrund.`

const MANGEL = { type: 'object', properties: { urteil: { type: 'string' }, maengel: { type: 'array', items: { type: 'object',
  properties: { id: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, wo: { type: 'string' },
    beschreibung: { type: 'string' }, vorschlag: { type: 'string' } }, required: ['id', 'schwere', 'wo', 'beschreibung', 'vorschlag'] } } },
  required: ['urteil', 'maengel'] }
const VERDICT = { type: 'object', properties: { schoener_als_vorher: { type: 'boolean' }, kein_giraffen_gang: { type: 'boolean' },
  kevin_zeigen: { type: 'boolean' }, zusammenfassung: { type: 'string' }, gang_tempo: { type: 'string' },
  rest_maengel: { type: 'array', items: { type: 'string' } }, dateien: { type: 'array', items: { type: 'string' } } },
  required: ['schoener_als_vorher', 'kein_giraffen_gang', 'kevin_zeigen', 'zusammenfassung', 'gang_tempo', 'rest_maengel', 'dateien'] }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies den Stand, miss am Generator-Jungen, am Standard-Jungen und am Foto C: Beinlaenge/Rumpfhoehe/Bauchabstand relativ zur
Rumpflaenge, Fussgroesse, Schrittlaenge und Tempo, Kopf-/Schnauzen-/Nasengroesse relativ zum Kopf, Kopfneigung aus Kevins Kamera. Sieh die heutigen
Renders aus Kevins Kamera an (Gang als Streifen!) und schreibe ${V2}/PLAN.md: Soll-Masse (Zahlen), Weg fuer die Beine (Netz + Knochen-Ruhelage,
Baerenfuesse wie baer-junges-fuss, Gewichte), Weg fuer die Clips (alle 15 auf die neuen Beine umrechnen, Pfoten-Haftung, Tempo), Weg fuer das
Gesicht (Verformung mit glatten Uebergaengen, Kopfneigung, Textur), Pruefliste. Zwei Bauer nacheinander: BEINE (Form, Skelett-Ruhe, Clips) und
GESICHT (Kopf-Form, Textur, Export) -- getrennte Dateien, Uebergabe. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const beine = await agent(`${CTX}

DEINE ROLLE: BAUER BEINE laut ${V2}/PLAN.md (Ordner ${V2}/beine/). Kurze kraeftige Beine, Baerenfuesse, Skelett-Ruhe dazu, Gewichte, alle 15 Clips
umgerechnet (Gang tapsig, Pfoten haften, nichts schwebt, kein Rutschen bei 0,35); Zwischenstand ${V2}/beine/NCBearBenchCubGen_beine.glb, Harness.
Blatt ${V2}/bilder/beine.png (Seite/vorn/hinten gross, Gang-Streifen aus Kevins Kamera in Spielgroesse neben dem Standard-Jungen und dem alten
Generator-Jungen) SELBST ansehen und nachbessern. Bericht ${V2}/BEINE.md. Rueckgabe: Kurzfassung mit Zahlen (Beinlaenge, Tempo, Boden, Rutschen).`,
  { label: 'bau:beine', phase: 'Bau' })
if (!beine) { return { plan, abbruch: 'Beine ohne Ergebnis' } }
const gesicht = await agent(`${CTX}

DEINE ROLLE: BAUER GESICHT + EXPORT laut ${V2}/PLAN.md (Ordner ${V2}/gesicht/), auf dem Stand des Beine-Bauers (${V2}/BEINE.md). Schnauze/Maul
groesser, Kopf nicht gesenkt, Augen sichtbar, Ohren rund, suess; Gewichte am Kopf sauber; Fressen erreicht den Boden; Textur passend (Beine/Fuesse
mit). Export nach ${V2}/out/ (Bench-Namen), Harness, alle festen Regeln messen. Blatt ${V2}/bilder/gesicht.png (Kopf nah vorn/schraeg/Seite, aus
Kevins Kamera gross und in Spielgroesse, neben Foto C, Babygesicht-Vorlage, Standard-Jungem und altem Generator-Jungen) SELBST ansehen. Bericht
${V2}/GESICHT.md. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:gesicht', phase: 'Bau' })
if (!gesicht) { return { plan, beine, abbruch: 'Gesicht ohne Ergebnis' } }

phase('Pruefung')
const [po, pt, st] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER OPTIK. Du hast nichts gebaut. Rendere SELBST ${V2}/out gegen das alte Generator-Junge und das Standard-Junge: Gesicht nah,
8 Seiten, Spielgroesse, Gehen/Rennen als Streifen, Sitzen, Liegen, Fressen aus Kevins Kamera. Laeuft es noch wie eine Giraffe? Ist das Maul gross
genug? Urteile hart. Bericht ${V2}/PRUEF_OPTIK.md. Rueckgabe strukturiert.`, { label: 'pruef:optik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER TECHNIK. Du hast nichts gebaut. Miss SELBST alle festen Regeln an ${V2}/out, Harness, Knochen-/Clip-Namen wie heute, Boden je
Pfote und Bild, Rutschen bei 0,35, Tempo, Risse, Dehnung. Bericht ${V2}/PRUEF_TECHNIK.md. Rueckgabe strukturiert.`,
    { label: 'pruef:technik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${CTX}

DEINE ROLLE: BENCH-STAGING (nur Testhilfe, nie nach NPC Crew). Baue unter ${V2}/mod/ (gleiche relative Pfade wie ${T}) die Dateien, mit denen Kevin
das neue Generator-Junge lebend neben sich holt: shared/NCBearBenchCubGenDefs.lua (eigene Vergleichs-Art "ncbearcubgen", Form GENAU wie
${T}/42/media/lua/shared/NCBearBenchVergleichDefs.lua mit ncbearcubalt), scripts/NCBearBenchCubGen.txt (Form wie NCBearBenchVergleich.txt),
client/NCBearBenchCubGen.lua mit NCBear_CubGen() (lebend vor dir, neben einem Standard-Jungen zum Vergleich) und NCBear_CubGenSize(0.35..0.75), nur
Einzelspieler. Eiserne Regel: jeder Engine-Aufruf mit Fundstelle (die vorhandenen Bench-Dateien sind die Vorlage). Nur NCBearBench*/NCBear_*-Namen,
vorher in NPC Crew greppen; ${B}/tools/baer_uebernahme.py (nur lesen) muss sie als Bench erkennen. Lua-Pruefer luacheck.py, scopecheck.py,
localcount.py, luacheck_pz.py (C:/Users/Kevin/Zomboid/mods/NPCCrew/_docs/tools) laufen lassen. Liste ${V2}/staging_dateien.txt (Lua/Skript + die zwei
Modell-Dateien aus ${V2}/out), Testanleitung fuer Kevin ${V2}/anleitung_entwurf.md (Deutsch, kurz, eine Zeile zum Eintippen). Bericht ${V2}/STAGING.md.
Rueckgabe: Kurzfassung.`, { label: 'staging:bench', phase: 'Pruefung' }),
])
const maengel = [...((po && po.maengel) || []), ...((pt && pt.maengel) || [])]

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Maengel: ${JSON.stringify(maengel, null, 1)}
Selbst nachpruefen, blocker/major beheben (Skripte der Bauer), minor wenn klein; vorher ${V2}/out nach ${V2}/out_vor_fix sichern; neu exportieren,
Harness, Regeln messen, Blaetter neu, selbst ansehen. Bench-Staging (${V2}/STAGING.md) nur anfassen, wenn ein Mangel es betrifft. Bericht
${V2}/NACHBESSERUNG.md. Rueckgabe: Kurzfassung.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut. Rendere und miss SELBST ${V2}/out und lies ${V2}/mod (Bench-Staging, Pruefer-Skripte laufen
lassen). Je Mangel der Pruefer: geschlossen? Dann: schoener als vorher (schoener_als_vorher)? Kein Giraffen-Gang mehr (kein_giraffen_gang)? So schoen,
dass man es Kevin zeigen kann (kevin_zeigen)? Gang-Tempo bei 0,35 (gang_tempo). Blatt fuer Kevin ${V2}/bilder/KEVIN_gen_junges_v2.png (oben Foto C +
neu aus Kevins Kamera gross; Gesicht nah alt gegen neu gegen Standard-Junges; Gang-Streifen alt gegen neu gegen Standard in Spielgroesse; 8 Seiten;
Sitzen/Liegen). Testanleitung ${V2}/anleitung_entwurf.md pruefen und richtigstellen. Bericht ${V2}/GEGEN.md. Rueckgabe strukturiert.`,
  { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { plan, beine, gesicht, po, pt, st, fix, gegen }
