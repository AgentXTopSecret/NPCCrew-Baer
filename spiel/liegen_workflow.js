export const meta = {
  name: 'baer-liegen',
  description: 'Baer liegend/tot: Dead/Death aller Baeren (gross 2c, Generator, Junges, Generator-Junges) ohne ineinander steckende Pfoten, liegt auf -- nur diese Clips, alles andere bit-gleich (bis 9 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Plan', detail: 'Bestand aller vier GLB, Pose, Weg' },
    { title: 'Bau', detail: 'grosse Baeren und Junge parallel' },
    { title: 'Pruefung', detail: 'Optik und Technik' },
    { title: 'Nachbesserung' },
    { title: 'Gegenpruefung' },
    { title: 'Zweite Runde', detail: 'nur wenn der Gegenpruefer noch nicht zufrieden ist' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const B = N + '/baer'
const R = N + '/_arbeit/baer_liegen'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const H = N + '/_arbeit/baer_spiel/harness'
const BL = 'C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe'

const CTX = `Du arbeitest im Lauf "baer-liegen" an Kevins Baeren-Mod (fuer NPC Crew, Project Zomboid 42.22). Keine Fragen an Kevin waehrend des Laufs,
offene Punkte als "Fragen fuer Kevin". Berichte Deutsch, ASCII. "Statisch geprueft, nicht gespielt."

KEVIN (12.11.2026, woertlich, zum Blatt ${N}/_arbeit/baer_junges_fuss/bilder/KEVIN_junges_liegen.png): "naja ich denk mal du siehst selbst das es
scheisse ist die beine stecken ineinander xD" -- "(die fuesse)". Auf die Frage, ob das Liegen beim grossen Baeren gleich mit soll (Render
${N}/_arbeit/baer_gross/fix1/render/end/p_dead_az50_tex.png: Beine uebereinander gestapelt): "Ja, beide Baeren". WOERTLICH und FEST in
${B}/begleiter/ENTSCHEIDUNGEN.md, Abschnitt "Junges liegend/tot: Pfoten stecken ineinander" (Zeile ~447) -- ZUERST lesen, dazu ${B}/STAND.md (Bloecke
oben) und ${B}/UEBERGABE_ACCOUNT2.md.
ZIEL: In den Clips **Death** (Sturz) und **Dead** (liegt tot) stecken Pfoten/Fuesse NICHT mehr ineinander oder uebereinander: Beine natuerlich
gestaffelt wie bei einem echten Baeren in Seitenlage (jede Pfote sichtbar und frei, auch aus Kevins Spielkamera), der Koerper LIEGT AUF (kein
Schweben -- bekannt: Variante "liegen_gesenkt" des Jungen 2,2 cm tiefer, grosser Baer schwebte 4 mm; nichts im Boden: hoechstens 1,5 cm). Das ist die
TOT-Pose (ausgestreckte Seitenlage) -- NICHT die spaetere Schlafpose (Sphinx/eingerollt, eigener Lauf). Der Sturz (Death) muss sauber in genau die
Dead-Pose enden (letztes Death-Bild = Dead-Pose), ohne Sprung, ohne dass Glieder durch den Koerper wandern.
GILT FUER ALLE VIER KOERPER (Kevin "beide Baeren"; seit dem Aussehen-Knopf gibt es je zwei Aussehen): gross 2c ${T}/42/media/models_X/Skinned/NCBear.glb
(MD5 08bfdbfd), Generator-Baer NCBearGen.glb (f58ea4c9; Clips laut STAND textgleich zum 2c -- pruefen), Junges NCBearCub.glb (d9931d32),
Generator-Junges NCBearCubGen.glb (989939f2) UND sein byte-gleicher Werkbank-Zwilling NCBearBenchCubGen.glb (beide immer als Paar ersetzen; beim
Generator-Jungen war offen "liegt auf dem Ruecken", ${N}/_arbeit/baer_gen_junges/v2/GEGEN.md M6 -- mit beheben). NCBearBenchCubAlt.glb und NCBearDeer.glb
bleiben unberuehrt. Die Test-Mod ist der Eingang und wird NUR GELESEN.
FESTE REGELN: NUR die Clips Death und Dead aendern sich. Netz, UV, Gewichte, Knochen (Namen/Eltern/Ruhelage), Texturen und ALLE anderen Clips bleiben
bit-gleich (gleiche Abtastzeiten, Schluessel, Matrizen; glb_pruef.py z. B. ${N}/_arbeit/baer_2c/werkzeug/pruef/glb_pruef.py, Importer des Spiels
${H}/Dump.java -- vor jedem "fertig" beide laufen lassen). Clip-Namen, Dauern, Bildzahl und Abtastzeiten von Death/Dead bleiben wie heute (Knoten-XML,
Ton-Momente und Lua haengen daran: im Plan belegen, wo Lua/XML Death/Dead benutzen, auch F2 "Am Boden"/Aufhelfen und der Leichnam). Kopf/Gesicht in
der Pose nicht verformen (Kevin: "KOPF BLEIBT SO"). Reicht "nur Clips" an einer Stelle nicht (z. B. Falten im Liegen nur ueber Gewichte): NICHT
aendern, sondern messen, zeigen und als Frage fuer Kevin melden. Kevin hat ausserdem gebeten, beim Jungen das Schweben beim Rennen ANZUSEHEN: nur
messen und berichten (Bild + Zahl), Run bleibt byte-gleich.
WIEDERHOLBAR: Die Aenderung ist je Koerper ein Skript-Schritt, der Death/Dead in einem vorhandenen GLB ersetzt bzw. die Kette mit neuen Spuren neu
baut -- der naechste Modell-Lauf (Maul-Nachbesserung) ersetzt NCBear.glb/NCBearGen.glb und muss das Liegen mit EINEM Befehl wieder aufsetzen koennen
(Befehl je Koerper in ${R}/WIEDERHOLEN.md).
KEVINS BILD IST DER MASSSTAB (Gedaechtnis-Regel): jede Pose als TON-Bild UND mit Textur aus Kevins Spielkamera (schraeg von oben, Hoehe 30 Grad,
Azimut 0, 50, 90, 180, 270) und von der Seite/von oben, in Spielgroesse (gross 1,35 / Junges 0,35 neben einer 1,8-m-Figur) und nah, ALT neben NEU
legen und SELBST ansehen, bevor jemand "fertig" sagt. Eine Textur darf eine falsche Form nie verdecken. Sturz als Bildfolge (mindestens 8 Bilder).
ERGEBNIS genau: ${R}/out/42/media/models_X/Skinned/{NCBear.glb, NCBearGen.glb, NCBearCub.glb, NCBearCubGen.glb, NCBearBenchCubGen.glb} + ${R}/out/md5.txt.
KETTE UND WERKZEUGE (selbst nachlesen, Originale NIE aendern -- neue Skripte ${B}/spiel/baer_*_liegen.py): grosser Baer ${B}/spiel/baer_kampf_gross.py
(Clips; Sterbe-Spuren, Liegehoehe boden_liege/liege_alt.json), ${N}/_arbeit/baer_gross, ${N}/_arbeit/baer_kopfnaht (heutiger Stand = mod/),
${N}/_arbeit/baer_2c (SPEZ_2C.md, werkzeug/); Generator-Baer ${N}/_arbeit/baer_gen_gross/v2 (out_schmal), ${B}/spiel/baer_*_gg2*.py; Junges
${N}/_arbeit/baer_junges_fuss (PLAN_JFUSS.md, CLIPS.md, clips/, werkzeug/), ${B}/spiel/baer_*_jfuss.py, ${N}/_arbeit/baer_baby; Generator-Junges
${N}/_arbeit/baer_gen_junges/v2, ${B}/spiel/baer_clips_gj2.py, baer_umrechnen_gj2.py. Einbau-Vorlagen (nur lesen) ${B}/tools/einbau_gross.py,
einbau_gg2s.py, einbau_gj2.py. Blender 5.2.3 ${BL} (--background --factory-startup --python s.py -- args); JDK C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin.
GPU nur RTX 4090 mit OPTIX (auch Entrauscher); Sperre ${R}/gpu.lock (mkdir = Sperre; existiert er, warten; danach rmdir; nie laenger als 20 min
halten); laeuft ein fremdes blender.exe (andere Sitzung rendert), kurz warten. Rendern ist auch bei laufendem Spiel erlaubt. Befehle ueber 2 Minuten
im Hintergrund.
ORTE: schreiben nur unter ${R}/ und neue Skripte ${B}/spiel/baer_*_liegen.py. Suchorte nur: ${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla
C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (lesen). Nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk. NIE in Test-Mods,
NPC Crew, das Spiel oder fremde Arbeitsordner schreiben. Kein git, kein Download, nichts hochladen, nichts aus fremden Mods kopieren.`

const MANGEL = {
  type: 'object',
  properties: {
    urteil: { type: 'string' },
    maengel: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, wo: { type: 'string' },
      beschreibung: { type: 'string' }, beleg: { type: 'string' }, vorschlag: { type: 'string' },
    }, required: ['id', 'schwere', 'wo', 'beschreibung', 'beleg', 'vorschlag'] } },
  },
  required: ['urteil', 'maengel'],
}
const VERDICT = {
  type: 'object',
  properties: {
    bereit_fuer_test_mod: { type: 'boolean' },
    pfoten_frei: { type: 'boolean' },
    liegt_auf: { type: 'boolean' },
    schoen_genug_fuer_kevin: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    offene_maengel: { type: 'array', items: { type: 'string' } },
    fragen_an_kevin: { type: 'array', items: { type: 'string' } },
    dateien: { type: 'array', items: { type: 'string' } },
    kevin_test: { type: 'string' },
  },
  required: ['bereit_fuer_test_mod', 'pfoten_frei', 'liegt_auf', 'schoen_genug_fuer_kevin', 'zusammenfassung', 'offene_maengel', 'fragen_an_kevin', 'dateien', 'kevin_test'],
}

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. (1) Bestand: wie entstehen Death/Dead in jedem der vier GLB (Skript, Funktion, Zeile), wie viele Bilder/Dauer, welche Knochen haben
Schluessel; wo benutzen Lua und Knoten-XML der Test-Mod diese Clips (Tod, Leichnam, F2 "Am Boden"/Aufhelfen) und was haengt an Dauer/Ereignissen.
(2) Die heutige Pose aller vier Koerper rendern (TON + Textur, Kevins Kamera und Seite/oben; GPU-Regeln) und messen: welche Pfoten ueberlappen
(Durchdringung in cm je Paar), wie hoch schwebt/wie tief sinkt er, wie liegt der Kopf. Blatt ${R}/bilder/bestand.png. (3) Die ZIEL-POSE festlegen:
Seitenlage eines echten Baeren -- untere Beine nach vorn/hinten ausgestreckt am Boden, obere Beine leicht versetzt davor/darueber, sodass aus Kevins
Kamera alle vier Pfoten frei zu sehen sind; als Winkel-/Lage-Tabelle je Knochen fuer den grossen Baeren und umgerechnet fuer die Junges-Skelette
(kuerzere Beine, groesserer Kopf), mit messbaren Abnahme-Zielen (kein Pfoten-/Bein-Paar durchdringt sich; Abstand je Pfotenpaar >= X cm; tiefster
Punkt -1,5..0 cm; Auflageflaeche; Dehnung nicht schlechter als heute). Eine schnelle Pose-Probe (ein Bild je Koerper, TON) beweist, dass die Tabelle
taugt. (4) Den Weg je Koerper: welches Skript wird kopiert/erweitert, wie wird "nur Death/Dead" bewiesen, WIEDERHOLEN-Befehl. (5) Aufteilung fuer zwei
Bauer mit getrennten Dateien: GROSS (2c + Generator) und JUNGE (Junges + Generator-Junges + Zwilling); gemeinsame Pose-Tabelle ${R}/POSE.md.
Schreibe ${R}/PLAN_LIEGEN.md. Rueckgabe: Kurzfassung (hoechstens 30 Zeilen) mit Zielen und Dateiliste.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const [gross, junge] = await parallel([
  () => agent(`${CTX}

Der Plan ist fertig: ${R}/PLAN_LIEGEN.md und ${R}/POSE.md (ganz lesen). Kurzfassung: ${plan}
DEINE ROLLE: BAUER GROSS -- 2c (NCBear.glb) und Generator-Baer (NCBearGen.glb). Arbeitsordner ${R}/gross/, Skripte ${B}/spiel/baer_*_liegen.py (nur
deine: Namen mit "gross"/"gg" kenntlich). Baue Death und Dead nach POSE.md, sieh dir JEDE Fassung selbst an (TON + Textur, Kevins Kamera Azimut
0/50/90/180/270, Seite, oben; Sturz als Bildfolge) und bessere nach, bis keine Pfote mehr in einer anderen steckt und er aufliegt -- erst dann fertig.
Beweise: alle anderen Clips bit-gleich, Netz/Gewichte/UV gleich (glb_pruef.py + Dump.java alt gegen neu), Dauern gleich. Ergebnis nach
${R}/out/42/media/models_X/Skinned/NCBear.glb und NCBearGen.glb, MD5 in ${R}/out/md5_gross.txt, WIEDERHOLEN-Befehle in ${R}/WIEDERHOLEN.md (Abschnitt
GROSS). Weicht die Pose von POSE.md ab: dort Abschnitt GROSS anhaengen (der andere Bauer liest ihn). Bericht ${R}/BAU_GROSS.md mit Bildern
${R}/bilder/gross_*.png (alt | neu). Rueckgabe: Kurzfassung (hoechstens 25 Zeilen).`, { label: 'bau:gross', phase: 'Bau' }),
  () => agent(`${CTX}

Der Plan ist fertig: ${R}/PLAN_LIEGEN.md und ${R}/POSE.md (ganz lesen). Kurzfassung: ${plan}
DEINE ROLLE: BAUER JUNGE -- Junges (NCBearCub.glb) und Generator-Junges (NCBearCubGen.glb + byte-gleicher Zwilling NCBearBenchCubGen.glb). Arbeitsordner
${R}/junge/, Skripte ${B}/spiel/baer_*_liegen.py (nur deine: Namen mit "junges"/"gj" kenntlich). Baue Death und Dead nach POSE.md fuer die
Junges-Skelette (kuerzere Beine, groesserer Kopf; beim Generator-Jungen das "liegt auf dem Ruecken" beheben), sieh dir JEDE Fassung selbst an (TON +
Textur, Kevins Kamera Azimut 0/50/90/180/270, Seite, oben, Spielgroesse 0,35 und nah; Sturz als Bildfolge) und bessere nach, bis keine Pfote mehr in
einer anderen steckt und es aufliegt -- erst dann fertig. Beweise: alle anderen Clips bit-gleich (Gang!), Netz/Gewichte/UV gleich (glb_pruef.py +
Dump.java alt gegen neu), Dauern gleich. Dazu der Mess-Auftrag "Schweben beim Rennen" (nur Bild + Zahl, nichts aendern). Ergebnis nach
${R}/out/42/media/models_X/Skinned/NCBearCub.glb, NCBearCubGen.glb, NCBearBenchCubGen.glb, MD5 in ${R}/out/md5_junge.txt, WIEDERHOLEN-Befehle in
${R}/WIEDERHOLEN.md (Abschnitt JUNGE). Abweichungen von POSE.md dort im Abschnitt JUNGE anhaengen. Bericht ${R}/BAU_JUNGE.md mit Bildern
${R}/bilder/junge_*.png (alt | neu). Rueckgabe: Kurzfassung (hoechstens 25 Zeilen).`, { label: 'bau:junge', phase: 'Bau' }),
])
if (!gross && !junge) { return { plan, abbruch: 'Bauer ohne Ergebnis' } }

const STAND = `Gebaut ist in ${R}: PLAN_LIEGEN.md, POSE.md, BAU_GROSS.md, BAU_JUNGE.md, WIEDERHOLEN.md, out/42/media/models_X/Skinned/ (5 GLB), bilder/.
Kurzfassungen -- GROSS: ${gross || '(fehlt -- Bericht lesen)'} --- JUNGE: ${junge || '(fehlt -- Bericht lesen)'}`

async function pruefen(runde) {
  const res = await parallel([
    () => agent(`${CTX}

${STAND}
DEINE ROLLE: PRUEFER OPTIK (Runde ${runde}). Du aenderst nichts ausser deinem Bericht und eigenen Bildern unter ${R}/pruef_optik_${runde}/. Glaube keinem
Bericht. Rendere SELBST alle fuenf neuen GLB (Zwilling genuegt per MD5) in Dead und als Death-Bildfolge: TON und Textur, Kevins Kamera (Hoehe 30 Grad,
Azimut 0/50/90/180/270), Seite, von oben, Spielgroesse und nah, je ALT (Test-Mod) neben NEU, neben Kevins Blatt KEVIN_junges_liegen.png und dem alten
Render p_dead_az50_tex.png. Urteile streng wie Kevin: Steckt irgendwo eine Pfote/ein Bein in einem anderen oder im Rumpf? Sind alle vier Pfoten frei
und als Pfoten erkennbar? Liegt er auf (kein Spalt, kein Versinken)? Sieht die Lage nach einem liegenden Baeren aus oder verdreht/gebrochen/steif?
Kopf und Hals natuerlich? Sturz ohne Sprung, endet genau in Dead? Sehen grosse Baeren und Junge wie dieselbe Art zu liegen aus? Bericht
${R}/PRUEF_OPTIK_${runde}.md mit Bildern. Rueckgabe strukturiert (id O1...).`, { label: 'pruef:optik' + (runde > 1 ? ':' + runde : ''), phase: runde > 1 ? 'Zweite Runde' : 'Pruefung', schema: MANGEL }),
    () => agent(`${CTX}

${STAND}
DEINE ROLLE: PRUEFER TECHNIK (Runde ${runde}). Du aenderst nichts ausser deinem Bericht und eigenen Messungen unter ${R}/pruef_technik_${runde}/. Glaube
keinem Bericht. Lies alle fuenf neuen GLB mit dem Importer des Spiels (${H}/Dump.java) und vergleiche je mit der Test-Mod: (1) NUR Death und Dead
geaendert -- alle anderen Clips, Netz, UV, Gewichte, Knochen bit-gleich (glb_pruef.py + eigener Vergleich); (2) Death/Dead: Namen, Dauer, Bildzahl,
Abtastzeiten wie vorher, alle Knochen mit Schluesseln, letztes Death-Bild = Dead-Pose (Abweichung in Grad/cm), kein Sprung je Bild ueber den Grenzen
der Kette; (3) Geometrie messen statt schaetzen: Durchdringung je Glied-Paar (Pfote/Pfote, Bein/Bein, Bein/Rumpf) in cm ueber alle Dead-Bilder und das
Death-Ende, tiefster/hoechster Auflagepunkt gegen den Boden, Dehnung je Dreieck in Dead gegen heute; (4) Zwilling byte-gleich, Dateinamen wie in der
Mod, md5.txt stimmt, keine weitere Datei im out/; (5) WIEDERHOLEN.md: jeden Befehl einmal ausfuehren -> byte-gleiches GLB; (6) Lua/XML der Test-Mod,
die Death/Dead benutzen (Tod, Am Boden/Aufhelfen): passt alles weiter (Dauern, Ereignisse)? Bericht ${R}/PRUEF_TECHNIK_${runde}.md. Rueckgabe
strukturiert (id T1...).`, { label: 'pruef:technik' + (runde > 1 ? ':' + runde : ''), phase: runde > 1 ? 'Zweite Runde' : 'Pruefung', schema: MANGEL }),
  ])
  return res.filter(Boolean).flatMap(r => r.maengel || [])
}

phase('Pruefung')
const maengel1 = await pruefen(1)
log(maengel1.length + ' Maengel (' + maengel1.filter(m => m.schwere === 'blocker').length + ' blocker, ' + maengel1.filter(m => m.schwere === 'major').length + ' major)')

phase('Nachbesserung')
const fix1 = await agent(`${CTX}

${STAND}
DEINE ROLLE: NACHBESSERUNG (darf alle Skripte ${B}/spiel/baer_*_liegen.py und alles unter ${R}/ aendern). Pruefberichte ${R}/PRUEF_OPTIK_1.md,
${R}/PRUEF_TECHNIK_1.md. Maengel: ${JSON.stringify(maengel1, null, 1)}
Jeden selbst nachpruefen (Bild ansehen, messen), falsche mit Beleg ablehnen, blocker/major beheben, minor wenn klein und sicher. Nach jeder Aenderung
SELBST rendern und ansehen (TON + Textur, Kevins Kamera) und die Beweise neu fuehren (nur Death/Dead geaendert, Zwilling, md5.txt, WIEDERHOLEN). Bericht
${R}/NACHBESSERUNG_1.md (je Mangel behoben/abgelehnt). Rueckgabe: je Mangel-ID eine Zeile.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegenPrompt = (runde, fixText) => `${CTX}

${STAND}
DEINE ROLLE: GEGENPRUEFER (Runde ${runde}). Du hast nichts gebaut und glaubst keinem Bericht. Nachbesserung sagt: ${fixText || '(fehlt -- Bericht lesen)'}
Pruefe selbst und streng: (1) alle fuenf GLB mit Dump.java/glb_pruef.py -- nur Death/Dead geaendert, Zwilling byte-gleich, md5.txt; (2) rendere Dead und
das Death-Ende aller vier Koerper selbst (TON + Textur, Kevins Kamera Azimut 0/50/90/180/270 und Seite) und sieh sie an: Pfoten frei? liegt auf?
natuerlich? Miss die Durchdringung je Glied-Paar; (3) sind die blocker/major der Pruefer wirklich behoben, ist nichts Neues kaputt? Urteile, ob das
SCHOEN GENUG ist, um es Kevin zu zeigen (er entscheidet nach dem Bild aus seiner Kamera) -- wenn nicht, offene_maengel genau nennen.
Baue das Blatt fuer Kevin ${R}/bilder/KEVIN_liegen.png: je Koerper ALT links, NEU rechts, aus Kevins Kamera in Spielgroesse und nah, mit Textur
(deutsche Beschriftung, kurz), unten eine Reihe TON. Schreibe ${R}/GEGEN_${runde}.md. dateien = Pfade relativ zu ${R}/out (nur Mod-Dateien),
kevin_test = hoechstens 6 kurze deutsche Zeilen (Spiel neu starten; wie er einen toten/am Boden liegenden Baeren je Aussehen mit den Bench-Befehlen
der Test-Mod zu sehen bekommt -- Befehle in ${T}/42/media/lua/client/NCBearBench*.lua nachlesen).`

const gegen1 = await agent(gegenPrompt(1, fix1), { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

let gegen = gegen1
let fix2 = null
if (gegen1 && !(gegen1.bereit_fuer_test_mod && gegen1.schoen_genug_fuer_kevin)) {
  phase('Zweite Runde')
  log('Gegenpruefer noch nicht zufrieden -> zweite Runde (Nachbesserung + Gegenpruefung)')
  fix2 = await agent(`${CTX}

${STAND}
DEINE ROLLE: NACHBESSERUNG, ZWEITE RUNDE (darf alle Skripte ${B}/spiel/baer_*_liegen.py und alles unter ${R}/ aendern). Der Gegenpruefer
(${R}/GEGEN_1.md, ganz lesen) ist noch nicht zufrieden: ${JSON.stringify({ zusammenfassung: gegen1.zusammenfassung, offene_maengel: gegen1.offene_maengel }, null, 1)}
Behebe jeden offenen Mangel, sieh dir jede Aenderung SELBST an (TON + Textur, Kevins Kamera), fuehre alle Beweise neu (nur Death/Dead geaendert,
Zwilling, md5.txt, WIEDERHOLEN). Bericht ${R}/NACHBESSERUNG_2.md. Rueckgabe: je Mangel eine Zeile.`, { label: 'nachbesserung:2', phase: 'Zweite Runde' })
  gegen = await agent(gegenPrompt(2, fix2), { label: 'gegenpruefung:2', phase: 'Zweite Runde', schema: VERDICT })
}

return { plan, gross, junge, maengel: maengel1.length, fix1, gegen1, fix2, gegen }
