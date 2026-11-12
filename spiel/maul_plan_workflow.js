export const meta = {
  name: 'baer-maul-plan',
  description: 'Offenes Maul beider grossen Baeren (2c + Generator) schoener -- Forschung (Vorlagen, Anatomie, heutige Renders) + Plan; Bau folgt als eigener Lauf, wenn kopfnaht und gen-gross-schmal fertig sind (2 Agenten; nichts in die Test-Mod)',
  phases: [{ title: 'Forschung' }, { title: 'Plan' }],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const M = N + '/_arbeit/baer_maul'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'

const CTX = `Lauf "baer-maul" an Kevins Baeren-Mod (Project Zomboid). Deutsch, "statisch geprueft, nicht gespielt".
Kevin (12.11.2026, woertlich, nach dem Blatt mit dem Bruellen/Aufrichten): "und bei beiden baeren sieht der mund schonn scheisse aus das muss besser
werden guck dir dazu vllt bilder an wie nen baeren maul aussieht wenn er das maul offen hat". Gemeint: das OFFENE MAUL (Bruellen/Aufrichten, Biss,
Fressen) der beiden GROSSEN Baeren: 2c-Baer (${T}/42/media/models_X/Skinned/NCBear.glb 08ec7806; verbesserte Fassung mit neuem Aufrichten/Bruellen
in ${N}/_arbeit/baer_gross/mod, Kopfnaht-Lauf darauf in ${N}/_arbeit/baer_kopfnaht -- LAEUFT NOCH, nur lesen) und Generator-Baer (${T}/42/media/
models_X/Skinned/NCBearGen.glb; v2 in ${N}/_arbeit/baer_gen_gross/v2/, Kevin waehlte die schmale Nase, Lauf out_schmal LAEUFT NOCH, nur lesen).
Beide teilen das 2c-Skelett (26 Knochen) und die 15 Clips.
FRUEHER: Kevin 09.11. (ENTSCHEIDUNGEN.md "Gebiss, Zunge, Beine wie Baumstaemme", ${B}/begleiter/ENTSCHEIDUNGEN.md Zeilen ~128-137): Zaehne beim
Schreien sollen aussehen wie in seiner Vorlage ${B}/begleiter/kevin_bruellen_vorlage.webp (Bildschirmfoto einer Bildersuche: NUR ANSEHEN, nie in
Modell/Textur, nie hochladen); Zunge sah schlecht aus. Was schon gebaut wurde: ${N}/_arbeit/baer_2c/forschung_gebiss.md, bau_gebiss.md, SPEZ_2C.md,
gegen_bericht.md; ${N}/_arbeit/baer_gross/SPEZ_GROSS.md (Bruellen-Clip). Weitere Vorlagen ${B}/begleiter/ref_*.jpg (Wikimedia), vorlage_E_gross.jpg.
Bilder im Netz: du darfst mit WebSearch suchen und Seiten ansehen, aber NICHTS herunterladen. Willst du ein freies Foto (Wikimedia Commons) als
Vorlage auf der Platte, liste es (Dateiname, Link, Pixel, MB, Lizenz) -- Kevin sagt je Datei ja.
ORTE: schreiben nur unter ${M}/. Lesen: ${N}/_arbeit/baer_*, ${B}, ${T}, Vanilla media. Nie in Test-Mods, NPC Crew, das Spiel oder die laufenden
Arbeitsordner (baer_kopfnaht, baer_gen_gross/v2) schreiben; kein git, kein Download. Blender 5.2.3 headless
C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe, GPU-Sperre ${N}/_arbeit/baer_gen/gpu.lock (mkdir/rmdir, besteht sie: warten),
Harness ${N}/_arbeit/baer_spiel/harness. Befehle ueber 2 Minuten im Hintergrund. Jedes Bild SELBST ansehen, kein Schoenreden.`

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG. 1) Rendere beide Baeren mit offenem Maul (Bruellen-Hoehepunkt, Biss, Fressen; Kevins Kamera az 0 / el 30 gross und
Spielgroesse, dazu nah vorn/schraeg/seitlich) und lege sie neben Kevins Vorlage -> ${M}/bilder/heute.png. Schreibe hart auf, WAS genau schlecht
aussieht (Zaehne: Zahl/Form/Groesse/Farbe der Eckzaehne und Schneidezaehne, Backenzaehne; Zahnfleisch; Lefzen/Lippenrand; Mundwinkel/Maulspalte
wie tief; Zunge; Gaumen; Rachen; Kieferwinkel/Oeffnung im Clip; Naht/Loecher/Durchstiche). 2) Anatomie eines offenen Braunbaeren-Mauls (Gebiss
3/3 1/1 4/4 2/3, lange gebogene Eckzaehne, dunkles/pigmentiertes Zahnfleisch und schwarze Lefzen, Maulspalte reicht weit nach hinten, Zunge breit/flach,
Gaumen mit Querrillen) aus Vorlagen und Netzbildern (nur ansehen) mit Zahlen relativ zur Kopflaenge. 3) Bestand: Wie sind Mundinneres, Zaehne und
Zunge heute gebaut (Netzteile, Gewichte am Kiefer, Textur-Bereiche, Skripte), was ist in beiden Modellen gleich, was anders. Ergebnis ${M}/FORSCHUNG.md.
Rueckgabe: Kurzfassung der Maengel und Soll-Zahlen.`, { label: 'forschung:maul', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${M}/FORSCHUNG.md und schreibe ${M}/PLAN_MAUL.md fuer den BAU-Lauf (startet erst, wenn kopfnaht und gen-gross-schmal
fertig sind; Grundlage dann deren Ergebnis): Soll je Teil (Zaehne, Zahnfleisch, Lefzen, Mundwinkel, Zunge, Gaumen, Rachen, ggf. Kieferoeffnung im
Bruellen-/Biss-Clip) mit Zahlen; Weg (Netz-Teile ersetzen/neu im Mundinneren, Gewichte Kiefer/Kopf, Textur-Bereiche, gleiche Kopf-Aussenform, Clips
nur wenn noetig und begruendet); EIN Gebiss-Baustein fuer BEIDE Baeren (gleiches Skelett) oder getrennt -- mit Grund; Regeln (<= 20.000 Dreiecke je
Modell, 1 Netz, 1 Material, <= 4 Einfluesse, Textur 1024 RGB, keine Durchstiche bei geschlossenem Maul in allen 15 Clips, Harness); Bauer-Aufteilung
mit getrennten Dateien; Pruefliste mit Bildern neben Kevins Vorlage aus Kevins Kamera. Optional: Liste freier Commons-Fotos fuer Kevins Ja.
Rueckgabe: Kurzfassung mit Zahlen und der Agentenzahl fuer den Bau-Lauf (hoechstens 8).`, { label: 'plan:maul', phase: 'Plan' })

return { fo, plan }
