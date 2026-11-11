export const meta = {
  name: 'baer-gen-schoen',
  description: 'Generator-Baeren schoen machen: Junges neu aus Foto C (stehend), grosser Baer E nacharbeiten (Schwanz-Lappen, Kopf-Wulst, Augen, Krallen, Fell), Optik-Pruefer, Nachbesserung, Gegenpruefer (6 Agenten; ohne Knochen, nichts in die Test-Mod)',
  phases: [
    { title: 'Bau', detail: 'Junges aus C erzeugen und waehlen; grossen Baeren E nacharbeiten; dann Junges nacharbeiten' },
    { title: 'Pruefung', detail: 'strenger Optik-Pruefer gegen die Fotos aus Kevins Spielkamera' },
    { title: 'Nachbesserung', detail: 'bestaetigte Maengel beheben' },
    { title: 'Gegenpruefung', detail: 'Urteil und Blaetter fuer Kevin' },
  ],
}

const G = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const CU = 'C:/Users/Kevin/Tools/ComfyUI/ComfyUI_windows_portable'

const CTX = `Du arbeitest an Kevins Baeren-Modellen fuer seine Mod NPC Crew (Project Zomboid). Kevin programmiert nicht, er beurteilt Bilder. Schreibe
Berichte auf Deutsch. Kevins Massstab (woertlich): "mach das bitte richtig schoen von allen seiten das es immer gut aussieht" und
"so schoen wie moeglich muss das model werden". Zu den letzten Blaettern (woertlich): "fix noch den komischen schwanz hinten und das komische
dinge auf den kopf und so wie du selbst gesagt hast die punkte" und er wollte Fotos, "damit du es bauen kannst wie er grade steht".

STAND (zuerst lesen): ${G}/PROBELAUF.md und ${G}/STUFE2.md (Einrichtung ComfyUI + TRELLIS.2, Seeds, Werkzeuge, Glaett-Weg, Farb-Eichung,
Urteil). Werkzeuge unter ${G}/werkzeug/ (gen_var.py, vier.py, varblatt.py, spielnetz.py, spielblatt.py, gpu_lauf.sh, param_A.json,
param_E.json) und ${B}/tools/gen_trellis.py + trellis2_ablauf_api.json. ComfyUI: ${CU} (Start nur lokal 127.0.0.1:8188 ohne Browser wie im
PROBELAUF; am Ende nur den eigenen Prozess beenden; laeuft schon einer auf 8188, ihn mitbenutzen statt einen zweiten zu starten).
Bisherige Ergebnisse: ${G}/aus/A_spielnetz.glb (altes Junges aus Foto A, Schritt-Pose -- wird ERSETZT), ${G}/aus/E_spielnetz.glb (grosser Baer
aus Foto E, Versuch E_c2_form -- wird NACHGEARBEITET), Blaetter ${G}/bilder/*_spielnetz.png.
Fotos: ${B}/begleiter/vorlage_E_gross.jpg (grosser Baer, steht seitlich), NEU ${B}/begleiter/vorlage_C_junges_steht.jpg (Junges, 14 Monate,
steht ruhig auf allen vier Pfoten zwischen Steinen, schraeg von vorn, Gesicht gut zu sehen; Baer im Bild etwa x 0,33-0,86 und y 0,09-0,92;
hinten oben verschwommen ein zweiter Baer, der NICHT mit ins Netz darf). Lizenz C: CC BY-SA 4.0 (Wikimedia Commons, "Eurasian brown bear
(Ursus arctos arctos) cub 14 months.jpg").

REFERENZEN AUS ALLEN WINKELN (Kevin: "du brauchst bilder von jeden winkel", "hol dir auch ein bild vom hintern vom baeren damit du den
schwanz hinten fixxen kannst", "und vom stehenden baeren bilder damit das ROAR nicht komplett scheisse wieder aussieht"): alle Dateien
${B}/begleiter/ref_*.jpg -- von hinten: ref_hinten_grizzly.jpg (Hinterteil eines grossen Grizzly schraeg von hinten), ref_hinten_felsen.jpg
(oberer Baer ganz von hinten), ref_hinten_schraeg_laeuft.jpg; aufrecht auf den Hinterbeinen: ref_aufrecht_vorn.jpg (von vorn: Brust, Bauch,
Arme), ref_aufrecht_schraeg.jpg, ref_aufrecht_seite.jpg; evtl. noch ref_vorn_mutter.jpg (von vorn), ref_seite_geht.jpg (Seite); dazu
vorlage_A_junges.jpg (Junges schraeg vorn), vorlage_E_gross.jpg (Seite), vorlage_C_junges_steht.jpg (vorn). Sie sind zum ANSEHEN und
VERGLEICHEN (Form und Farbe je Blickwinkel) -- nicht als Textur aufkleben; der Generator nimmt nur EIN Bild. Wichtig daraus: das Hinterteil
ist rund, der Schwanz ist nur ein kurzer Stummel fast im Fell versteckt; Brust, Bauch und Innenseiten der Beine sieht man beim Aufrichten und
Bruellen -- sie muessen fellig und baerenhaft aussehen (keine glatte Flaeche, keine falsche Farbe).

ZIELE je Modell (Endstand): EIN zusammenhaengendes Netz, hoechstens 20.000 Dreiecke, keine Loecher, vier getrennte Beine, Kopf und Pfoten
dichter als der Rumpf, EINE Textur 1024x1024 RGB (Spiel hat fuer Tiere keine Normal-Map), Farbe am Foto geeicht (Render-Licht geeicht wie in
STUFE2). Schoen heisst: echte Braunbaer-Form von ALLEN acht Seiten, Gesicht mit dunklen Augen, dunkler Augenpartie/Unterlid und dunkler Nase,
Ohren rund und fellig, Pfoten mit angedeuteten dunklen Krallen (gemalt reicht), Fell-Eindruck durch ein gerichtetes Strichmuster in der
Textur (Fellrichtung vom Kopf nach hinten/unten), keine Fremdflecken, keine Lappen, keine Wuelste, kein Stachel- oder Pluesch-Eindruck.
Noch KEINE Knochen, Gewichte oder Clips -- die Pose bleibt die des Fotos (beide stehen); das kommt in einem spaeteren Lauf.

FESTE REGELN: KEINE Downloads (kein pip, kein git clone, keine Modelle nachladen, keine Custom Nodes); fehlt etwas: Name, Quelle, Groesse
melden und ohne es weitermachen. Nur ComfyUI (lokal) und Blender 5.2.3 (C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe,
headless) starten; keine Systemeinstellungen, kein Autostart; das Spiel nie starten oder beenden (laeuft es, darfst du trotzdem rendern; bei
Speichermangel kleiner stufen und melden). Grafikkarte RTX 4090, OPTIX; vor jedem Erzeugen/Rendern die Sperre ${G}/gpu.lock (mkdir, danach
rmdir; existiert sie, warten -- ein anderer Agent dieses Laufs rendert vielleicht gerade); rendert ein fremdes blender.exe, kurz warten.
Schreiben nur unter ${G}/ (neue Unterordner fuer deinen Teil) -- nie in Test-Mods (C:/Users/Kevin/Zomboid/mods), NPC Crew, das Spiel; kein
git; nichts hochladen; nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk suchen. Befehle ueber 2 Minuten im Hintergrund starten.
KAMERA fuer alle Blaetter: acht Ansichten rundum (alle 45 Grad), Hoehenwinkel 30 Grad (Kevins Spielkamera), orthografisch, neutrales Licht,
Farben nicht aufhellen; Reihe gross mit Textur, Reihe in SPIELGROESSE (Modell ca. 140 px hoch, unvergroessert), Reihe Ton ohne Textur, oben
das Foto; dazu je Blatt eine Zusatzreihe "wie beim Aufrichten": von vorn-unten (Kamera auf Bauchhoehe, 20 Grad von unten), von hinten und
von hinten-unten (Hinterteil/Schwanz), neben die passenden Referenzfotos gelegt. Sieh dir JEDES Blatt selbst an (Bild lesen) und urteile hart je Koerperteil -- kein Schoenreden; Kevin hat oft schlechte Modelle
bekommen.`

const MANGEL = {
  type: 'object',
  properties: {
    urteil_junges: { type: 'string' },
    urteil_gross: { type: 'string' },
    maengel: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          modell: { type: 'string', enum: ['junges', 'gross'] },
          schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] },
          koerperteil: { type: 'string' },
          ansicht: { type: 'string' },
          beschreibung: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['id', 'modell', 'schwere', 'koerperteil', 'beschreibung', 'vorschlag'],
      },
    },
  },
  required: ['urteil_junges', 'urteil_gross', 'maengel'],
}

const VERDICT = {
  type: 'object',
  properties: {
    junges_kevin_zeigen: { type: 'boolean' },
    gross_kevin_zeigen: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    rest_maengel: { type: 'array', items: { type: 'string' } },
    blaetter: { type: 'array', items: { type: 'string' } },
    glb: { type: 'array', items: { type: 'string' } },
    zahlen: { type: 'string' },
    naechster_schritt: { type: 'string' },
  },
  required: ['junges_kevin_zeigen', 'gross_kevin_zeigen', 'zusammenfassung', 'rest_maengel', 'blaetter', 'glb', 'zahlen'],
}

phase('Bau')
const [jungesBau, gross] = await parallel([
  async () => {
    const gen = await agent(`${CTX}

DEINE ROLLE: JUNGES NEU ERZEUGEN aus ${B}/begleiter/vorlage_C_junges_steht.jpg (Arbeitsordner ${G}/c/).
1. Zuschnitt mit Rand, Hintergrund-Entfernung pruefen (Maske ansehen: zweiter Baer hinten, Steine zwischen den Pfoten muessen RAUS, alle vier
   Pfoten und beide Ohren DRIN); notfalls Maske selbst nachbessern (PIL) und den Entferner ueberspringen.
2. Mindestens 10 Versuche mit verschiedenen Seeds (laut STUFE2: Knoten 3 grobe Masse, 18 Form/Oberflaeche, 23 Feindetail, 12 Farbe), je vier
   schnelle Ansichten; Vergleichsblatt ${G}/bilder/C_varianten.png. Waehle den besten nach: Gesicht/Kopf auch von der Seite und hinten
   stimmig, Ohren beidseitig, vier saubere Beine mit Pfoten (keine Flossen, keine Menschenzehen), kein Fremdfleck/Lappen, wenig Stacheln,
   Farbe nah am Foto. Begruende am Bild.
3. Aus dem besten Versuch das Spielnetz wie in STUFE2 (spielnetz.py): Stacheln weg, Form bleibt, <= 20.000 Dreiecke, Textur 1024 backen,
   Farbe eichen. Ergebnis ${G}/aus/C_spielnetz.glb (+ Textur-PNG, Messung) und Blatt ${G}/bilder/C_spielnetz.png.
Bericht ${G}/C_ERZEUGEN.md. Rueckgabe: Kurzfassung (gewaehlter Versuch, Seeds, Zahlen, ehrliches Urteil je Koerperteil).`, { label: 'bau:junges-erzeugen', phase: 'Bau' })
    if (!gen) return null
    const fein = await agent(`${CTX}

DEINE ROLLE: JUNGES NACHARBEITEN. Ausgangspunkt ${G}/aus/C_spielnetz.glb (Bericht ${G}/C_ERZEUGEN.md, Blatt ${G}/bilder/C_spielnetz.png) --
zuerst das Blatt selbst ansehen und die Maengel je Koerperteil aufschreiben. Dann beheben (Arbeitsordner ${G}/c_fein/, Skripte dort):
Form (Wuelste/Lappen/Beulen gezielt mit Kugel-Masken glaetten oder abtragen, Ohren rund, Schnauze und Pfoten sauber, ggf. dichtes Rohnetz
als Quelle fuer Details), Gesicht in der Textur (dunkle Augen an den 3D-Augenpositionen, dunkles Unterlid/Augenpartie, dunkle Nase, helle
Schnauze wie im Foto C), Krallen dunkel an den Zehen, Fell als gerichtetes Strichmuster, einheitliche Fellfarbe ohne Flecken (am Foto
geeicht). Nach jeder groesseren Aenderung ein Blatt rendern und selbst ansehen. Endstand ${G}/aus/C_schoen.glb + C_schoen_textur.png +
Messung, Blatt ${G}/bilder/C_schoen.png. Bericht ${G}/C_FEIN.md (was geaendert, vorher/nachher, Zahlen, hartes Urteil). Rueckgabe: Kurzfassung.`, { label: 'bau:junges-fein', phase: 'Bau' })
    return { gen, fein }
  },
  () => agent(`${CTX}

DEINE ROLLE: GROSSEN BAEREN E NACHARBEITEN. Ausgangspunkt ${G}/aus/E_spielnetz.glb (Blatt ${G}/bilder/E_spielnetz.png, dichtes Rohnetz des
Versuchs E_c2_form unter ${G}/aus/varianten/). Zuerst das Blatt selbst ansehen. Kevins Punkte: der "komische Schwanz hinten" (der Lappen am
Hinterteil -- Braunbaeren haben nur ein kurzes Stummelschwaenzchen, fast im Fell versteckt) und "das komische Ding auf dem Kopf" (Wulst/Beule
hinter dem Kopf, frueher der weisse Fleck) MUESSEN weg; dazu Augen, dunkle Augenpartie und Nase in die Textur, Krallen an den Pfoten,
flossenartige Hinterpfoten zu Baerenpfoten (breit, kurz, dicke Zehenballen), Fell als gerichtetes Strichmuster, Schulterbuckel behalten.
Arbeitsordner ${G}/e_fein/ (Skripte dort). Nach jeder groesseren Aenderung ein Blatt rendern und selbst ansehen. Endstand
${G}/aus/E_schoen.glb + E_schoen_textur.png + Messung, Blatt ${G}/bilder/E_schoen.png. Bericht ${G}/E_FEIN.md (vorher/nachher, Zahlen, hartes
Urteil je Koerperteil). Rueckgabe: Kurzfassung.`, { label: 'bau:gross-fein', phase: 'Bau' }),
])
if (!jungesBau && !gross) { return { abbruch: 'Bau ohne Ergebnis' } }

phase('Pruefung')
const pruef = await agent(`${CTX}

DEINE ROLLE: OPTIK-PRUEFER. Du hast nichts davon gebaut. Sieh dir die Blaetter ${G}/bilder/C_schoen.png und ${G}/bilder/E_schoen.png an (falls
eines fehlt, das letzte vorhandene des Modells und das melden) und rendere SELBST zusaetzlich: je Modell 8 Ansichten in Spielgroesse und die
Kopf-Nahansicht von vorn, von der Seite und schraeg hinten, dazu die Pfoten von unten-schraeg. Vergleiche mit den Fotos
(${B}/begleiter/vorlage_C_junges_steht.jpg bzw. vorlage_E_gross.jpg). Pruefe Kevins Punkte (Schwanz-Lappen, Kopf-Ding bei E) ausdruecklich.
Liste JEDEN Mangel je Koerperteil und Ansicht mit Schwere (blocker = Kevin wuerde es sofort sehen und hassen). Miss auch: Dreiecke, Teile,
Loecher, Textur 1024 RGB. Bericht ${G}/OPTIK_PRUEFUNG.md. Rueckgabe strukturiert.`, { label: 'pruef:optik', phase: 'Pruefung', schema: MANGEL })

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Der Optik-Pruefer fand (Bericht ${G}/OPTIK_PRUEFUNG.md):
${JSON.stringify(pruef ? pruef.maengel : [], null, 1)}
Pruefe jeden Mangel selbst am Bild; behebe alle blocker und major an ${G}/aus/C_schoen.glb und ${G}/aus/E_schoen.glb (Skripte und Werkzeuge der
Bauer unter ${G}/c_fein/ und ${G}/e_fein/ nutzen; Berichte ${G}/C_FEIN.md, ${G}/E_FEIN.md). Vorher Sicherungskopie (*_vor_fix.glb). Nach
jeder Aenderung neu rendern und ansehen. Danach Blaetter ${G}/bilder/C_schoen.png und E_schoen.png neu, Messungen neu. Bericht
${G}/NACHBESSERUNG_OPTIK.md (je Mangel: behoben/abgelehnt mit Bild-Beleg). Rueckgabe: Kurzfassung.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut und glaubst keinem Bericht. Maengel des Pruefers:
${JSON.stringify(pruef ? pruef.maengel.map(m => ({ id: m.id, modell: m.modell, schwere: m.schwere, koerperteil: m.koerperteil, beschreibung: m.beschreibung })) : [], null, 1)}
Bericht der Nachbesserung: ${G}/NACHBESSERUNG_OPTIK.md.
1. Rendere beide Endstaende selbst (acht Seiten, Spielgroesse, Kopf nah, Pfoten) und pruefe jeden Mangel: wirklich weg? Neues kaputt?
2. Messe nach: Dreiecke <= 20.000, ein Teil, keine Loecher, vier Beine getrennt, Textur 1024 RGB, Farbe gegen Foto.
3. Erstelle je Modell das Blatt fuer Kevin (${G}/bilder/KEVIN_junges.png, ${G}/bilder/KEVIN_gross.png): oben links das Foto, daneben gross die
   Ansicht aus Kevins Spielkamera schraeg von vorn, darunter acht Seiten in Spielgroesse und eine Reihe gross; hoechstens ca. 2400 px breit.
4. Urteil: Ist das jeweilige Modell gut genug, um es Kevin als "schoen von allen Seiten" zu zeigen? Nenne ehrlich die Restmaengel und den
   naechsten Schritt (Knochen/Clips oder weitere Formarbeit).
Bericht ${G}/GEGEN_OPTIK.md. Rueckgabe strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { jungesBau, gross, pruef, fix, gegen }
