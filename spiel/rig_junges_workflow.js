export const meta = {
  name: 'baer-rig-junges',
  description: 'Generator-Junges C spielfertig: Formrunde (Kopf gerade, Ohren), Skelett + Gewichte, 15 Clips (Gehen schneller), Pruefer Optik/Technik, Nachbesserung, Gegenpruefer -- 8 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Plan', detail: 'RIG_PLAN.md aus SPEZ_JUNGES, Baby-/2c-Kette und Harness' },
    { title: 'Bau', detail: 'Formrunde, Skelett+Gewichte, Clips+Export' },
    { title: 'Pruefung', detail: 'Optik (alle Clips aus der Spielkamera) und Technik (feste Regeln, Importer)' },
    { title: 'Nachbesserung', detail: 'bestaetigte Maengel beheben' },
    { title: 'Gegenpruefung', detail: 'Urteil: besser als der Platzhalter und bereit fuer die Test-Mod?' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const G = N + '/_arbeit/baer_gen'
const R = G + '/rig'
const J = N + '/_arbeit/baer_junges'
const BB = N + '/_arbeit/baer_baby'
const C2 = N + '/_arbeit/baer_2c'
const H = N + '/_arbeit/baer_spiel/harness'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const BL = 'C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe'

const CTX = `Du arbeitest im Lauf "baer-rig-junges" an Kevins Baeren-Mod (NPC Crew, Project Zomboid B42). Kevin schlaeft (Nachtschicht): keine
Fragen, offene Punkte als "Fragen fuer Kevin" in deinen Bericht. Berichte auf Deutsch. "Statisch geprueft, nicht gespielt."

ZIEL: Das neue Baeren-Junge aus dem Generator (${G}/aus/C_schoen.glb + C_schoen_textur.png, Berichte ${G}/C_ERZEUGEN.md, ${G}/C_FEIN.md,
Urteil ${G}/GEGEN_OPTIK.md, Blatt ${G}/bilder/KEVIN_junges.png) wird ein SPIELFERTIGES Tiermodell, das den heutigen Platzhalter
(${T}/42/media/models_X/Skinned/NCBearCub.glb + ${T}/42/media/textures/Body/NCBearCub.png, alter Entwurf aus ${BB}/entwurf/) unter
GENAU DENSELBEN Dateinamen ersetzt. Kevin (11.11.): "so schoen wie moeglich muss das model werden", "richtig schoen von allen seiten". Er hat
erlaubt, den Platzhalter zu ersetzen, WENN der Gegenpruefer das neue Junge besser findet. Ausserdem (Kevins Freigabe 11.11.): "Gehen schneller",
damit das Junge beim Folgen nicht immer rennen muss (heute geht der Platzhalter bei Groesse 0,35 nur ~0,52 Kacheln/s, ein Spieler ~2,27;
Messung ${N}/_arbeit/baer_zaehmen/forschung_b1b.md Befund 0.3).

WAS SCHON FESTSTEHT (lesen, nicht neu erfinden): ${J}/SPEZ_JUNGES.md -- besonders B.5 Skelett (Faktoren, Lage-Schluessel, Lehre M6),
D Clips (D.1 Grundsatz, D.2 Lagen/Becken, D.3 Boden, D.4 Sitzen S_J, D.5 erlaubte Abweichungen, D.6 Weg je Schritt), Messwerkzeuge
${J}/werkzeug/; Baby-Lauf ${BB}/SPEZ_BABY.md, ${BB}/bau_baby.md, ${BB}/fix_baby.md (Clip-Umrechnung per Skript: Drehungen vom
Erwachsenen, Lage-Schluessel neu); 2c-Kette ${B}/spiel/baer_{quelle,export,kampf,gewichte,textur,maul}_2c.py und ${C2}/ (SPEZ_2C.md, Berichte;
Ergebnis ${C2}/mod/42/media/); angefangene Skripte des abgebrochenen Laufs ${B}/spiel/baer_{form,export,gewichte,kampf}_junges.py (Teilstand,
nicht blind trauen); der gespielte Erwachsene ${T}/42/media/models_X/Skinned/NCBear.glb (26 Knochen, 15 Clips) und seine Skripte
${T}/42/media/scripts/nc_bear*.txt; das Junge ${T}/42/media/scripts/nc_bear_cub.txt und ${T}/42/media/lua/shared/BanditsNPCBearDefs.lua
(minSize = maxSize = 0,35, animset buck). Importer-Harness ${H} (Dump.java = so liest das Spiel das GLB; vor jedem "fertig" laufen lassen).

FESTE REGELN DES MODELLS: hoechstens 20.000 Dreiecke; EIN Netz, EIN Material; 26 Knochen mit GENAU den Namen des Erwachsenen; hoechstens
4 Einfluesse je Ecke, Summe 1; GENAU die 15 Clip-Namen des Erwachsenen mit gleicher Dauer und gleichen Abtastzeiten (Ausnahme nur mit
Begruendung nach SPEZ D.5); Textur 1024x1024 RGB (Tiere haben keine Mipmaps), Datei-/Modellnamen unveraendert (NCBearCub.glb,
NCBearCub.png, model NCBearCub_Body, animationsMesh NCBearCub); Massstab 0,544 Einheiten je Meter wie der Erwachsene, gebaut bei Groesse 1,0
(das Spiel skaliert auf 0,35); Dehnung 99,5 % <= 2,6, max <= 4,0, Achsel/Brust <= 3,5; Boden <= 1,5 cm in allen Clips; keine Risse an
Hals/Achsel/Leiste; Kevins Spielkamera Azimut 0 / Hoehe 30 Grad; jede Ansicht in Spielgroesse (~140 px) mit ansehen. Kopf-Aussenform des
Jungen bleibt die des Generators (nur gerade drehen und die Ohren richten). Kevins Bild ist der Massstab: rendern, neben Foto
${B}/begleiter/vorlage_C_junges_steht.jpg legen, SELBST ansehen, bevor du "fertig" sagst. Eine Textur darf eine falsche Form nie verdecken.

ORTE: Arbeit nur unter ${R}/ (Unterordner je Rolle) und neue Skripte ${B}/spiel/baer_*_rig.py (Originale nie aendern). Endergebnis GENAU:
${R}/out/42/media/models_X/Skinned/NCBearCub.glb und ${R}/out/42/media/textures/Body/NCBearCub.png (+ MD5 in ${R}/out/md5.txt). Nie in
Test-Mods (C:/Users/Kevin/Zomboid/mods), NPC Crew, das Spiel oder ${N}/_arbeit/baer_zaehmen/mod/ schreiben (das macht Claude danach). Kein
git, kein Download, nichts hochladen. SUCHORTE nur: ${N}/_arbeit/baer_*, ${B}, ${T} (lesen), Vanilla
C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (lesen); nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk.
WERKZEUGE: Blender 5.2.3 ${BL} (--background --factory-startup --python skript.py -- args), Python 3.12, JDK 25
C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin (Harness). GPU RTX 4090 OPTIX; Sperre ${G}/gpu.lock vor jedem Render (mkdir, danach rmdir;
existiert sie, warten); laeuft ein fremdes blender.exe mit Render, kurz warten. Rendern ist auch bei laufendem Spiel erlaubt. Befehle ueber
2 Minuten im Hintergrund starten.`

const MANGEL = {
  type: 'object',
  properties: {
    urteil: { type: 'string' },
    maengel: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] },
          wo: { type: 'string' },
          beschreibung: { type: 'string' },
          beleg: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['id', 'schwere', 'wo', 'beschreibung', 'beleg', 'vorschlag'],
      },
    },
  },
  required: ['urteil', 'maengel'],
}

const VERDICT = {
  type: 'object',
  properties: {
    ersetzt_platzhalter: { type: 'boolean' },
    bereit_fuer_test_mod: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    rest_maengel: { type: 'array', items: { type: 'string' } },
    zahlen: { type: 'string' },
    dateien: { type: 'array', items: { type: 'string' } },
    fragen_fuer_kevin: { type: 'array', items: { type: 'string' } },
  },
  required: ['ersetzt_platzhalter', 'bereit_fuer_test_mod', 'zusammenfassung', 'rest_maengel', 'zahlen', 'dateien'],
}

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies die genannten Unterlagen (SPEZ_JUNGES B.5 und D ganz, Baby-Berichte, GEGEN_OPTIK.md Restmaengel C-01/C-06/C-04/C-05,
2c-Export-Kette, Harness) und miss das Generator-Junge selbst (Lage von Kopf, Hals, Schultern, Ellbogen, Handgelenk, Huefte, Knie, Sprunggelenk,
Pfoten, Rueckenlinie, Schwanzansatz; Pose des Fotos: Kopf ~43 Grad zur Seite gedreht, Beine fast in Ruhe). Schreibe ${R}/RIG_PLAN.md:
1. Formrunde vor dem Skelett: Kopf gerade (um den Hals drehen, Naht unsichtbar), Ohren nach GEGEN_OPTIK C-01 (Basis breiter, kein Hals, etwas
   groesser wie im Foto), Stirn-Kratzer, Sohlenkanten rund; Beine, falls noetig, in die Ruhelage des Skeletts bringen.
2. Skelett: 26 Knochen des Erwachsenen mit den Faktoren aus SPEZ B.5 oder neu aus den Messungen am Generator-Netz -- begruende; Ruhelage so,
   dass die Clips des Erwachsenen (Drehungen) ohne Risse wirken; Lage-Schluessel neu (Lehre M6).
3. Gewichte: Verfahren (Blender-Automatik + Nacharbeit, oder Uebernahme der Gewichte der 2c-Kette per Naehe), Grenzen (4 Einfluesse, Summe 1),
   heikle Zonen (Hals, Achsel, Leiste, Schwanz, Ohren).
4. Clips: alle 15 aus dem Erwachsenen umrechnen (SPEZ D.1-D.5), Sitzen S_J, Boden, und D.6 Weg je Schritt: Zielgeschwindigkeit fuer Gehen bei
   Groesse 0,35 so hoch wie ohne Fussgleiten moeglich (Ziel ~1,6-2,3 Kacheln/s; wie das Spiel die Geschwindigkeit aus dem Clip nimmt, aus den
   Unterlagen belegen) -- Zahl und Weg festlegen; Rennen entsprechend.
5. Export und Pruefung: Export-Weg (2c-Kette als Vorbild), Harness-Lauf, Messskripte, Renderliste (alle 15 Clips aus Kevins Kamera,
   Spielgroesse, Sitzen von vorn neben der Sitzvorlage ${B}/begleiter/kevin_sitzvorlage.png), Abnahmekriterien.
6. Wer was baut: FORM (Netz + Textur), SKELETT+GEWICHTE, CLIPS+EXPORT -- getrennte Ordner/Skripte, klare Uebergabedateien.
Rueckgabe: Kurzfassung mit den Kernzahlen und den Uebergabedateien.`, { label: 'plan', phase: 'Plan' })
if (!plan) { return { abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const form = await agent(`${CTX}

DEINE ROLLE: FORM. Setze RIG_PLAN.md Abschnitt 1 um (Arbeitsordner ${R}/form/, Skript ${B}/spiel/baer_form_rig.py). Kopf gerade, Ohren richten
(von ALLEN Seiten runde, fellige Baerenohren -- von hinten keine Pilze, von vorn kein dunkler Fleck im Kopfumriss), Stirn-Kratzer weg,
Sohlenkanten rund, Beine in Ruhelage falls der Plan das sagt; Textur nachziehen (Augen, Nase, Fell, Farbe wie in C_FEIN geeicht). Danach
Blatt ${R}/bilder/form.png (8 Seiten gross + Spielgroesse + Ton + Kopf nah) und SELBST ansehen. Ergebnis: Netz ${R}/form/C_rig_basis.glb
(+ Textur), Bericht ${R}/FORM.md. Rueckgabe: Kurzfassung mit Zahlen und ehrlichem Urteil.`, { label: 'bau:form', phase: 'Bau' })
if (!form) { return { plan, abbruch: 'Form ohne Ergebnis' } }

const skel = await agent(`${CTX}

DEINE ROLLE: SKELETT + GEWICHTE. Setze RIG_PLAN.md Abschnitte 2-3 um auf ${R}/form/C_rig_basis.glb (Arbeitsordner ${R}/skelett/, Skripte
${B}/spiel/baer_skelett_rig.py, baer_gewichte_rig.py). 26 Knochen mit den Namen des Erwachsenen, Ruhelage, Gewichte (<= 4, Summe 1),
Probe-Posen (Kopf nach unten/oben/seitlich, Bein vor/zurueck, Aufrichten) rendern und ansehen: keine Risse, keine Beulen, Ohren und
Schwanz folgen richtig. Ergebnis: ${R}/skelett/C_rig.blend und Uebergabe fuer die Clips laut Plan, Bericht ${R}/SKELETT.md.
Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:skelett', phase: 'Bau' })
if (!skel) { return { plan, form, abbruch: 'Skelett ohne Ergebnis' } }

const clips = await agent(`${CTX}

DEINE ROLLE: CLIPS + EXPORT. Setze RIG_PLAN.md Abschnitte 4-5 um (Arbeitsordner ${R}/clips/, Skripte ${B}/spiel/baer_clips_rig.py,
baer_export_rig.py). Alle 15 Clips umrechnen (gleiche Namen, Dauern, Abtastzeiten), Sitzen S_J, Boden <= 1,5 cm, Gehen schneller laut Plan
ohne Fussgleiten (Geschwindigkeit nachmessen und nennen), Export in GENAU ${R}/out/42/media/models_X/Skinned/NCBearCub.glb und
${R}/out/42/media/textures/Body/NCBearCub.png, Harness ${H} laufen lassen (laedt das Spiel es?), alle festen Regeln nachmessen, Clip-Blatt
${R}/bilder/clips.png (je Clip 3-4 Bilder aus Kevins Kamera in Spielgroesse und gross) und SELBST ansehen. Bericht ${R}/CLIPS.md (Zahlen je
Regel, Geschwindigkeiten, Harness-Ausgabe, Befehle zum Wiederholen). Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'bau:clips', phase: 'Bau' })
if (!clips) { return { plan, form, skel, abbruch: 'Clips ohne Ergebnis' } }

phase('Pruefung')
const [po, pt] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER OPTIK. Du hast nichts gebaut. Lade ${R}/out/.../NCBearCub.glb so, wie das Spiel es bekommt, rendere SELBST: Ruhe 8 Seiten in
Spielgroesse und gross, jeden der 15 Clips in 4 Phasen aus Kevins Kamera, Sitzen von vorn neben ${B}/begleiter/kevin_sitzvorlage.png, Kopf nah,
Pfoten, Hinterteil; dazu den alten Platzhalter ${T}/42/media/models_X/Skinned/NCBearCub.glb gleich gerendert daneben. Urteile hart je Clip und
Koerperteil (Risse, Beulen, Fussgleiten, schwebend/im Boden, Ohren, Schwanz, Gesicht, Gangbild). Bericht ${R}/PRUEF_OPTIK.md mit Blaettern.
Rueckgabe strukturiert.`, { label: 'pruef:optik', phase: 'Pruefung', schema: MANGEL }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER TECHNIK. Du hast nichts gebaut. Miss SELBST alle festen Regeln am Endergebnis (Dreiecke, Netze/Materialien, 26 Knochennamen
gegen den Erwachsenen, Einfluesse, 15 Clipnamen/Dauern/Abtastzeiten gegen den Erwachsenen, Textur 1024 RGB, Massstab, Dehnung, Boden je Clip,
Geschwindigkeit Gehen/Rennen bei 0,35), lass den Harness ${H} laufen, vergleiche mit dem, was ${T}/42/media/scripts/nc_bear_cub.txt und
BanditsNPCBearDefs.lua erwarten. Bericht ${R}/PRUEF_TECHNIK.md. Rueckgabe strukturiert.`, { label: 'pruef:technik', phase: 'Pruefung', schema: MANGEL }),
])
const maengel = [...((po && po.maengel) || []), ...((pt && pt.maengel) || [])]
log('Pruefung: ' + maengel.length + ' Maengel')

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Maengel der Pruefer (Berichte ${R}/PRUEF_OPTIK.md, ${R}/PRUEF_TECHNIK.md):
${JSON.stringify(maengel, null, 1)}
Jeden selbst nachpruefen; blocker und major beheben (mit den Skripten der Bauer unter ${B}/spiel/baer_*_rig.py und ${R}/), minor wenn klein und
sicher. Vorher Sicherung von ${R}/out/ nach ${R}/out_vor_fix/. Danach neu exportieren, Harness, alle Regeln nachmessen, Blaetter neu, selbst
ansehen. Bericht ${R}/NACHBESSERUNG.md. Rueckgabe: je Mangel-ID Kurzfassung und neue Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut und glaubst keinem Bericht. Maengel der Pruefer:
${JSON.stringify(maengel.map(m => ({ id: m.id, schwere: m.schwere, wo: m.wo, beschreibung: m.beschreibung })), null, 1)}
Nachbesserung: ${R}/NACHBESSERUNG.md.
1. Rendere und miss SELBST am heutigen ${R}/out/ (Harness, feste Regeln, alle Clips aus Kevins Kamera, Spielgroesse). Je Mangel: geschlossen?
2. Lege das neue Junge und den alten Platzhalter nebeneinander (Ruhe, Gehen, Sitzen, Fressen aus Kevins Kamera, Spielgroesse und gross).
3. Urteil: (a) ersetzt_platzhalter = ist das neue Junge klar besser als der Platzhalter? (b) bereit_fuer_test_mod = laedt es laut Harness, halten
   alle festen Regeln, keine Risse/Schweben/Fussgleiten, die das Spiel kaputt aussehen lassen?
4. Blatt fuer Kevin ${R}/bilder/KEVIN_junges_spielfertig.png (oben Foto + neues Junges aus Kevins Kamera gross; Reihe Ruhe 8 Seiten Spielgroesse;
   Reihe je wichtiger Clip; Reihe alt gegen neu) und SELBST ansehen.
Bericht ${R}/GEGEN.md. Rueckgabe strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { plan, form, skel, clips, po, pt, fix, gegen }
