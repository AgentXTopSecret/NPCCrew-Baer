export const meta = {
  name: 'baer-kopfnaht',
  description: 'Grosser Baer: sauberer Uebergang Kopf -> Hals/Nacken (kein Rand, keine Stufe, Fell laeuft durch), geprueft aus Kevins Spielkamera -- 6 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'Ursache der Kopfnaht: UV-Inseln, Backen, Fell-Struktur, Netz-Stufe' },
    { title: 'Plan', detail: 'SPEZ_KOPFNAHT.md mit Messgroessen und Bild-Soll' },
    { title: 'Bau', detail: 'Textur (und falls noetig Netz) am Kopf-Hals-Uebergang' },
    { title: 'Pruefung', detail: 'Optik aus Kevins Kamera, alle Posen, nichts schlechter' },
    { title: 'Nachbesserung', detail: 'Befunde beheben' },
    { title: 'Gegenpruefung', detail: 'Urteil + Blatt fuer Kevin' },
  ],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const B = N + '/baer'
const G = N + '/_arbeit/baer_gross'
const W = N + '/_arbeit/baer_kopfnaht'
const C2 = N + '/_arbeit/baer_2c'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const BL = 'C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe'

const CTX = `Du arbeitest im Lauf "baer-kopfnaht" an Kevins Baeren-Mod (fuer NPC Crew, Project Zomboid B42). Kevin programmiert nicht, er spielt
und beurteilt mit den Augen. Berichte auf Deutsch.

KEVIN 12.11.2026 ~05:35 (im Spiel, Spielkamera von vorn-oben auf seinen grossen gezaehmten Baeren = das 2c-Modell der Test-Mod
${T}/42/media/models_X/Skinned/NCBear.glb + textures/Body/NCBear.png; Bilder ${B}/begleiter/kevin_kopfnaht_1112_a.png (rote Linie = Bogen hinter
Stirn und Ohren) und _b.png), woertlich: "guck mal die rote markierung da ist kein sauberer umergang zum kopf das regt mich noch auf da sieht man
richtig so eine spuhr das bis da gerendet wurde und dann der kopf einfach dran gebaut worden ist".
ZIEL: Der Kopf geht ohne sichtbaren Rand, Ring, Farb-/Helligkeitssprung, Wechsel der Fell-Struktur/Haarlaenge oder Stufe im Netz in Stirn-Hinterkopf,
Nacken, Hals und Wangen ueber -- aus Kevins Kamera, in allen Posen (Stehen, Gehen, Rennen, Sitzen, Aufrichten, Fressen, Hieb, Biss), bei Spielgroesse
und naeher. Gesicht (Augen, Nase, Schnauze, Lippen, Ohren) bleibt wie es ist; Koerperform, Clips und Skelett bleiben gleich (nur wenn die Stufe im Netz
nicht anders weggeht: kleinste Netz-Aenderung am Uebergang, Gewichte dort gleich behandeln, Rest bit-gleich).

GRUNDLAGE: der NEUESTE Stand des grossen Baeren aus Lauf "baer-gross" (${G}: SPEZ_GROSS.md, bau_netz.md, bau_textur.md, pruef_optik.md
Befund 4 "Kopf bleibt hellere, feiner behaarte Scheibe mit sichtbarem Rand", fix1_bericht.md, gegen_bericht.md (Urteil des Gegenpruefers samt
${G}/bilder/kopfnaht_vorher_nachher.png), Staging ${G}/mod/, Skripte ${B}/spiel/baer_*_gross.py (Textur baer_textur_gross.py, Netz/Export
baer_quelle_gross.py / baer_export_gross.py) und der 2c-Stand ${C2}. Was baer-gross schon an der Kopfnaht tat (G2-Band 3 cm, Farbsprung 18,8 -> 16,5)
lesen und darauf aufbauen. Fehlt ein baer-gross-Ergebnis, auf dem 2c-Stand der Test-Mod arbeiten und das im Bericht sagen.
EIGENER ORDNER ${W} (Werkzeuge ${W}/werkzeug/, Bilder ${W}/bilder/, Staging ${W}/mod/ als Kopie des Grundlage-Stagings; nie in ${G}/mod oder die
Test-Mod schreiben). Blender: ${BL} --background --factory-startup --python skript.py -- args; Renders nur auf der RTX 4090 (OPTIX, auch Denoiser),
vorher "tasklist | grep -i blender" pruefen und nicht gleichzeitig mit einem anderen grossen Render. Spielkamera wie Kevins Bilder (PZ-Isometrie von
vorn-oben, Spielgroesse ~101 px/m und 2x), dazu Seite und hinten. Regeln aus der Werkstatt-CLAUDE.md Abschnitt 8 (Kleidung/Tiere/Blender) gelten;
Texturdeckel 256 im Spiel bedenken (Uebergang muss auch bei 256er-Textur weich sein). Kein git, kein Spielstart, kein Download, nichts hochladen,
nichts aus fremden Mods; Kevins Bilder und fremde Fotos nur lokal ansehen. Schreibe "statisch geprueft, nicht gespielt"; keine Behauptung ohne
Messung oder Bild, sonst "ungeprueft".`

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
          wo: { type: 'string' },
          behauptung: { type: 'string' },
          beleg: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['id', 'schwere', 'wo', 'behauptung', 'beleg', 'vorschlag'],
      },
    },
  },
  required: ['zusammenfassung', 'findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    ready: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    offene_major: { type: 'array', items: { type: 'string' } },
    restbefunde: { type: 'array', items: { type: 'string' } },
    blatt_fuer_kevin: { type: 'string' },
    kevin_test: { type: 'string' },
  },
  required: ['ready', 'zusammenfassung', 'offene_major', 'blatt_fuer_kevin'],
}

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG (nur messen und rendern, nichts am Modell aendern). 1) Kevins zwei Bilder genau ansehen und dieselbe Kamera nachstellen
(Render heute 2c UND neuester baer-gross-Stand nebeneinander, Ton und Textur). 2) Ursache je Anteil belegen: UV-Inseln Kopf/Koerper (wo laeuft die
Naht im UV, Texel-Dichte beidseits), Backen/Malen der Textur (Helligkeit, Farbton, Haarlaenge/Struktur, Strichrichtung beidseits der Naht),
Normalen/Glaettung und Stufe im Netz an der Naht (Nacken von hinten "Stufe" laut pruef_optik), Mip-/256er-Verkleinerung. 3) Mass-Werkzeug fuer den
Uebergang aus Kevins Kamera (Profil quer ueber die rote Linie: Helligkeit, Farbton, Feinstruktur je cm; Sprungmass) unter ${W}/werkzeug/.
Ergebnis ${W}/forschung.md (Ursachen mit Bildern und Zahlen, Rangfolge, Wege). Rueckgabe: Kurzfassung.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const spez = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${W}/forschung.md. Schreibe ${W}/SPEZ_KOPFNAHT.md: Weg je Ursache (z. B. Uebergangsband beidseits der Naht 8-15 cm mit
Helligkeit/Farbton/Struktur-Angleich, Fell-Striche ueber die Naht durchmalen, UV-Naht-Raender auffuellen gegen Mip-Bluten, Normalen an der Naht
mitteln, Nacken-Stufe glaetten), was bit-gleich bleibt (Gesicht, Ohren, Schnauze, Koerper ausserhalb des Bandes, Skelett, Clips), harte Soll-Werte
(Sprungmass aus Kevins Kamera <= Wert X je 2-cm-Schritt, kein Ring in 8 Posen, Farbton +-5 Grad), Bild-Soll (welche Renders gegen Kevins Bild).
Rueckgabe: Kurzfassung.`, { label: 'plan', phase: 'Plan' })
if (!spez) { return { fo, abbruch: 'Plan ohne Ergebnis' } }

phase('Bau')
const bau = await agent(`${CTX}

DEINE ROLLE: BAUER. Setze ${W}/SPEZ_KOPFNAHT.md um: Staging ${W}/mod/ (Kopie der Grundlage), eigene Skripte unter ${W}/werkzeug/ (die baer-gross-
Skripte nur lesen oder als Kopie aendern). Danach selbst messen und rendern (Kevins Kamera heute | Grundlage | neu; 8 Posen; Spielgroesse, 2x, nah;
256er-Textur) und ansehen; nachbessern, bis kein Rand mehr zu sehen ist. Dateien, die in die Test-Mod gingen, mit MD5 und Pfad in
${W}/staging_dateien.txt (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen ${T}). Ergebnis ${W}/bau.md (was geaendert, Messwerte vorher/nachher,
Bilder). Rueckgabe: Kurzfassung.`, { label: 'bau', phase: 'Bau' })
if (!bau) { return { fo, spez, abbruch: 'Bauer ohne Ergebnis' } }

phase('Pruefung')
const pr = await agent(`${CTX}

DEINE ROLLE: PRUEFER OPTIK + TECHNIK (aenderst nichts ausser eigenen Bildern unter ${W}/pruef/). Selbst rendern aus Kevins Kamera und 7 weiteren
Richtungen, 8 Posen, Spielgroesse und nah, 256er-Textur; Kevins Bild daneben. Ist der Rand weg? Ist irgendwo ein neuer Fleck, Ring, Farbstich,
Matsch (verwaschene Struktur) oder ein heller/dunkler Hof entstanden? Gesicht/Ohren/Schnauze bit-gleich? Skelett/Clips/Gewichte textgleich bzw. nur
im erlaubten Band? GLB-Regeln (Werkstatt-CLAUDE.md 8) eingehalten? Soll-Werte der SPEZ selbst messen. Ergebnis ${W}/pruef.md. Rueckgabe strukturiert
(id P1...).`, { label: 'pruef', phase: 'Pruefung', schema: FIND })

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde: ${JSON.stringify((pr && pr.findings) || [], null, 1)}
Jeden selbst nachpruefen, bestaetigte major/blocker beheben, minor wenn klein und sicher; danach alle Messungen und Renders neu,
${W}/staging_dateien.txt neu. Ergebnis ${W}/nachbesserung.md. Rueckgabe: je Befund Kurzfassung.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER (Bericht ${W}/gegen_bericht.md, du aenderst nichts). Glaube keinem Bericht: selbst rendern und messen, Kevins Bild
daneben. ready = true nur, wenn aus Kevins Kamera in allen 8 Posen KEIN Kopf-Rand mehr zu sehen ist UND nichts schlechter wurde. Sei streng --
Kevin regt sich zu Recht auf, wenn "fertig" kommt und es im Spiel anders aussieht. Baue ${W}/bilder/KEVIN_kopfnaht.png (Kevins Bild | heute |
neu, gleiche Kamera, Stehen + Sitzen + Gehen, Spielgroesse und 2x) ohne fremde Fotos. kevin_test: kurze Schritte im Spiel (grossen Baeren holen:
NCBear_CubClean(), NCBear_CubHere(4), NCBear_CubTame(100), NCBear_CubGrow(55); von vorn-oben ansehen). Rueckgabe strukturiert.`, { label: 'gegenpruefer', phase: 'Gegenpruefung', schema: VERDICT })

return { fo, spez, bau, pr, fix, gegen }
