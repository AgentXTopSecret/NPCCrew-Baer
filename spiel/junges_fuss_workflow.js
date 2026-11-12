export const meta = {
  name: 'baer-junges-fuss',
  description: 'Altes Baer-Junges: Baerenfuesse, Beine und Sitzen wie der grosse 2c-Baer, Gesicht und Gang bleiben -- 8 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Plan', detail: 'Bestand Junges + 2c, Weg, Ziele' },
    { title: 'Bau', detail: 'Form (Beine/Fuesse), Clips/Gewichte (Sitzen), Textur' },
    { title: 'Pruefung', detail: 'Optik und Technik' },
    { title: 'Nachbesserung', detail: 'Befunde beheben' },
    { title: 'Gegenpruefung', detail: 'unabhaengige Abnahme' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const B = N + '/baer'
const BB = N + '/_arbeit/baer_baby'
const C2 = N + '/_arbeit/baer_2c'
const R = N + '/_arbeit/baer_junges_fuss'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const H = N + '/_arbeit/baer_spiel/harness'
const BL = 'C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe'

const CTX = `Du arbeitest im Lauf "baer-junges-fuss" an Kevins Baeren-Mod (fuer NPC Crew, Project Zomboid B42). Keine Fragen an Kevin waehrend des
Laufs, offene Punkte als "Fragen fuer Kevin". Berichte Deutsch, ASCII. "Statisch geprueft, nicht gespielt."

KEVIN (11.11.2026, woertlich): "der neue baby baer laeuft auch wie eine giraffe oder so xD also das alte ist definitiv besser ^^" -- "nimm den
neuen baby baeren bitte raus aus der mod und benutz wieder den alten der gefaellt mir besser" -- dann: "und das baby hat echt so menschen fuesse
noch? wenn ja kannst du das auch noch abaendern das es beim sitzen nicht so scheisse aussieht dann? sondern wie unser grosser baer der schon fast
fertig ist? ;D" -- und: "genau das gesicht muss so bleiben das wirkt suess ;D das ist gut so und gang sieht ja auch normal aus ^^". Zum grossen
Baeren (Lauf baer-2c): "der sitz schonmal viel besser als frueher". Alles WOERTLICH ganz unten in ${B}/begleiter/ENTSCHEIDUNGEN.md -- ZUERST lesen.
HEUTE: Das alte Junge (Lauf baer-baby, ${BB}/; Modell ${T}/42/media/models_X/Skinned/NCBearCub.glb MD5 6c3f0a96 + textures/Body/NCBearCub.png
2ee25f24; Skripte ${B}/spiel/baer_{form,netz,textur,export}_baby.py) wurde aus dem grossen Baeren VOR dessen Umbau gebaut: Hinterfuss wie ein
Menschenfuss, im Sitzen Menschen-Sohle, alte breitbeinige Sitzhaltung, Pranken gross (${BB}/fix_baby.md, Abschnitt zum Koerper aus dem
Erwachsenen; Bilder ${BB}/bilder/fix1/R4_sitzen_*.png; Blatt ${B}/spiel/baby_entwurf.png).
ZIEL: (1) Hinterfuesse und Beine wie beim grossen 2c-Baeren (kurze, runde, dunkle Baerensohle mit Zehenballen, Bein ohne "Hose in Stiefeln"),
im Junges-Massstab; (2) Sitzen wie der grosse Baer nach Kevins Sitzvorlage ${B}/begleiter/kevin_sitzvorlage.png (aufrecht, Beine eng,
Vorderbeine gerade, Kopf oben): die drei Sitz-Clips NCBear_SitDown/Sit/StandUp aus den 2c-Clips per Skript umrechnen (Drehungen vom grossen
Baeren, Lage-Schluessel des Jungen, Weg wie im Lauf baer-baby, ${BB}/bau_baby.md Abschnitt Clips); (3) GESICHT UND KOPF des Jungen bleiben
bit-gleich (Punkte, UV, Texel) -- Kevin: "das wirkt suess"; (4) GANG bleibt: Gehen/Rennen und alle anderen Clips des Jungen byte-gleich zu heute
(Kevin: "gang sieht ja auch normal aus"; das Generator-Junge "lief wie eine Giraffe"). Pranken duerfen etwas kleiner werden, wenn das hilft.
Kevins Bild ist der Massstab: jede Form als TON-Bild und mit Textur aus Kevins Spielkamera (schraeg von oben, Azimut 0 / Hoehe 30 Grad) und von
der Seite, in Spielgroesse 0,35 und nah, neben das heutige Junge, den grossen 2c-Baeren und die Sitzvorlage legen und SELBST ansehen, bevor
jemand "fertig" sagt.
PARALLEL laufen: baer-gross (aendert NCBear_Rear und Hals/Kopf der Sitz-Clips des grossen Baeren, ${N}/_arbeit/baer_gross) -- deshalb die
Clip-Umrechnung als wiederholbares Skript bauen, damit neue Sitz-/Rear-Clips spaeter mit einem Befehl uebernommen werden koennen;
baer-gen-gross; baer-b1e (Code, misst das Junge fuer den Modellwechsel ab Tag 15 -- Ruhelage-Masse moeglichst gleich lassen, Aenderungen in
Zahlen berichten).
FESTE REGELN: hoechstens 20.000 Dreiecke; ein Netz, ein Material; 26 Knochen mit Namen/Eltern wie heute; hoechstens 4 Einfluesse, Summe 1; 15 Clips
mit gleichen Namen, Dauern und Abtastzeiten; Textur 1024 RGB; Dateinamen bleiben (NCBearCub.glb, NCBearCub.png, Modell-Skript unveraendert);
Dehnung je Clip 99,5 % <= 2,6, max <= 4,0, Achsel/Brust <= 3,5 (heute zu hoch: Run 3,67 / SwipeL 4,41 laut fix_baby.md M6 -- besser werden, nicht
schlechter); Boden <= 1,5 cm; Ferse liegt im Sitzen auf. Ergebnis GENAU ${R}/out/42/media/models_X/Skinned/NCBearCub.glb und
${R}/out/42/media/textures/Body/NCBearCub.png + ${R}/out/md5.txt.
KETTE UND WERKZEUGE: Junges ${B}/spiel/baer_*_baby.py, ${BB}/ (SPEZ_BABY.md, bau_baby.md, fix_baby.md, werkzeug/); grosser Baer ${B}/spiel/baer_*_2c.py,
${C2}/ (SPEZ_2C.md, bau_koerper.md, bau_sitzen.md, gegen_bericht.md, werkzeug/, pruef/gegen/werkzeug/). Neue Skripte ${B}/spiel/baer_*_jfuss.py
(Originale nie aendern); Arbeit nur unter ${R}/. Importer-Harness ${H} (Dump.java, vor jedem "fertig"). Blender 5.2.3 ${BL}; JDK
C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin. GPU nur RTX 4090 OPTIX; Sperre ${R}/gpu.lock (mkdir; existiert er, warten; danach rmdir); laeuft ein
fremdes blender.exe mit Render (andere Laeufe rendern parallel), warten; Rendern auch bei laufendem Spiel erlaubt. Befehle ueber 2 Minuten im Hintergrund.
SUCHORTE nur: ${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (lesen). Nie rekursiv
ueber C:/Users/Kevin oder ein Laufwerk. NIE in Test-Mods, NPC Crew, das Spiel oder fremde Arbeitsordner schreiben. Kein git, kein Download, nichts hochladen.`

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
    fuesse_wie_baer: { type: 'boolean' },
    sitzen_wie_grosser_baer: { type: 'boolean' },
    gesicht_und_gang_gleich: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    rest_maengel: { type: 'array', items: { type: 'string' } },
    zahlen: { type: 'string' },
    dateien: { type: 'array', items: { type: 'string' } },
    kevin_test: { type: 'string' },
    fragen_fuer_kevin: { type: 'array', items: { type: 'string' } },
  },
  required: ['bereit_fuer_test_mod', 'fuesse_wie_baer', 'sitzen_wie_grosser_baer', 'gesicht_und_gang_gleich', 'zusammenfassung', 'rest_maengel', 'zahlen', 'dateien', 'kevin_test'],
}

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN (nichts bauen). Miss das heutige Junge (Dump.java) und rendere es im Sitzen aus Kevins Spielkamera und von der Seite neben
dem 2c-Baeren (Ton und Textur, ansehen). Lies, wie das Junge gebaut wurde (baer_*_baby.py, bau_baby.md) und wie der 2c-Baer Fuesse/Beine/Sitzen
bekam (SPEZ_2C.md, bau_koerper.md, bau_sitzen.md). Schreibe ${R}/PLAN_JFUSS.md: Weg fuer Beine/Fuesse (2c-Formen im Junges-Massstab uebernehmen,
Naht am Rumpf, Kopf bit-gleich), Sitz-Clips (Umrechnungsskript, wiederholbar), Gewichte (mit den neuen Sitz-Clips, Dehnung besser), Textur (nur
Fuesse/Beine neu, Gesicht bit-gleich), Soll-Zahlen mit Toleranz, Abnahme-Bilder. Rueckgabe: Kurzfassung mit Zahlen und Weg je Bauer.`, { label: 'plan', phase: 'Plan' })

phase('Bau')
const form = await agent(`${CTX}

PLAN (verbindlich ${R}/PLAN_JFUSS.md): ${plan || 'FEHLT'}

DEINE ROLLE: BAU FORM. Lege ${B}/spiel/baer_*_jfuss.py an (Kopien der *_baby.py) und baue Beine und Fuesse nach dem Plan; Kopf bit-gleich.
Ton-Runden aus Spielkamera und Seite neben 2c-Baer und heutigem Jungen, ANSEHEN, messen. Ergebnis Netz unter ${R}/form/, Bericht ${R}/FORM.md,
Bilder ${R}/bilder/form_*.png. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:form', phase: 'Bau' })

const clips = await agent(`${CTX}

PLAN (${R}/PLAN_JFUSS.md): ${plan || 'FEHLT'}
FORM (vor dir fertig, ${R}/FORM.md): ${form || 'FEHLT'}

DEINE ROLLE: BAU SITZ-CLIPS + GEWICHTE + GLB. Wiederholbares Umrechnungsskript fuer NCBear_SitDown/Sit/StandUp aus den 2c-Clips (und vorbereitet
fuer Rear), alle anderen Clips des Jungen byte-gleich zu heute; Gewichte mit den neuen Clips; GLB bauen; Harness. Ton-Bilder Sitzen/Hinsetzen/
Aufstehen aus Spielkamera und Seite neben 2c-Baer und Sitzvorlage, Gehen/Rennen neben heute (Gang gleich?), ANSEHEN; Ferse liegt auf, Boden,
Dehnung je Clip. Ergebnis ${R}/out/42/media/models_X/Skinned/NCBearCub.glb (Textur-Bezug wie heute), Bericht ${R}/CLIPS.md, Bilder
${R}/bilder/clips_*.png, Video ${R}/bilder/sitzen_vorschau.mp4. Rueckgabe: Kurzfassung mit Zahlen. FORTSETZUNG nach Halt 11.11. 22:3x (5-h-Limit): der erste Agent dieses Schritts wurde angehalten; seine Zwischenstaende (Dateien, Logs, halbe GLB/PNG) zuerst pruefen, nur Vollstaendiges und Richtiges weiterverwenden, Halbes neu machen.`, { label: 'bau:clips', phase: 'Bau' })

const textur = await agent(`${CTX}

PLAN (${R}/PLAN_JFUSS.md): ${plan || 'FEHLT'}
FORM (${R}/FORM.md): ${form || 'FEHLT'}
CLIPS (${R}/CLIPS.md): ${clips || 'FEHLT'}

DEINE ROLLE: BAU TEXTUR. Neue Fuesse/Beine im Junges-Fell, Sohlen dunkel mit Zehenballen wie beim 2c-Baeren, Gesicht/Kopf-Texel bit-gleich.
Ergebnis ${R}/out/42/media/textures/Body/NCBearCub.png (1024), md5.txt fuer beide Dateien, Bericht ${R}/TEXTUR.md, Kontroll-Renders Ton und Textur
alt neben neu (Sitzen Spielkamera, Seite, Stehen, Gehen; nah und Spielgroesse) ANSEHEN. Rueckgabe: Kurzfassung mit MD5.`, { label: 'bau:textur', phase: 'Bau' })

phase('Pruefung')
const PB = `${CTX}

Gebaut: ${R}/PLAN_JFUSS.md, FORM.md, CLIPS.md, TEXTUR.md, Ergebnis ${R}/out/. Du aenderst NICHTS. Glaube keinem Bericht: selbst rendern/messen/ansehen.
Schweregrad blocker = Kevins Wunsch verfehlt oder Regel gebrochen; major = deutlich sichtbar; minor = Rest. Jeder Mangel mit Beleg und Vorschlag.`
const [po, pt] = await parallel([
  () => agent(`${PB}

PRUEFER OPTIK (Ordner ${R}/pruef/optik/, Bericht ${R}/PRUEF_OPTIK.md): Sitzen wie der grosse Baer und die Sitzvorlage? Baerenfuesse statt
Menschenfuesse (nah und Spielgroesse)? Gesicht unveraendert? Gang wie heute (keine Giraffe)? Ton UND Textur, alt neben neu.`, { label: 'pruef:optik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${PB}

PRUEFER TECHNIK (Ordner ${R}/pruef/technik/, Bericht ${R}/PRUEF_TECHNIK.md): Dump.java; Skelett gleich; nur die drei Sitz-Clips geaendert, Rest
byte-gleich; Dauern/Abtastzeiten; Kopf bit-gleich (Punkte, UV, Texel); Dreiecke, Einfluesse, Summe, ein Netz, offene Kanten; Dehnung/Boden je
Clip; Textur 1024; md5.txt gegen die Platte; Umrechnungsskript wiederholbar (zweimal laufen = byte-gleich).`, { label: 'pruef:technik', phase: 'Pruefung', schema: MANGEL }),
])
const maengel = [...((po && po.maengel) || []), ...((pt && pt.maengel) || [])]
log('Pruefung: ' + maengel.length + ' Maengel')

phase('Nachbesserung')
const fix = await agent(`${CTX}

Berichte: ${R}/*.md. URTEILE: Optik ${JSON.stringify(po ? po.urteil : 'FEHLT')} | Technik ${JSON.stringify(pt ? pt.urteil : 'FEHLT')}
MAENGEL: ${JSON.stringify(maengel)}

DEINE ROLLE: NACHBESSERUNG. Stand sichern (${R}/fix1/vorher/), blocker und major beheben (minor wenn billig), nach jeder Aenderung Ton-Bild ansehen,
alles neu messen, md5.txt neu. Mangel nur mit Beleg ablehnen. Bericht ${R}/NACHBESSERUNG.md. Rueckgabe: je Mangel-ID Kurzfassung. FORTSETZUNG nach Halt 04:12 (5-h-Limit): Zwischenstaende pruefen, nur Vollstaendiges weiterverwenden.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

Berichte: ${R}/*.md. KURZFASSUNG NACHBESSERUNG: ${fix || 'FEHLT'}

DEINE ROLLE: GEGENPRUEFER (Ordner ${R}/gegen/, Bericht ${R}/GEGEN.md), du aenderst NICHTS. Unabhaengig messen und rendern; streng: Baerenfuesse,
Sitzen wie der grosse Baer, Gesicht und Gang unveraendert, keine Regel gebrochen? Baue ${R}/bilder/KEVIN_junges_vorher_nachher.png (alt links, neu
rechts; Sitzen Spielkamera und Seite, Hinterfuss nah, Stehen, Gehen, Spielgroesse) OHNE fremde Fotos. kevin_test: kurze Schritte (Spiel neu
starten, NCBear_CubHere(8), NCBear_CubTame(100), Sitzen wie in anleitung_b1b/b1c). Rueckgabe strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { plan, form, clips, textur, po, pt, maengel, fix, gegen }
