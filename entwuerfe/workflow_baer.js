export const meta = {
  name: 'baer-kopf-krallen',
  description: 'Baer: Kopf und Krallen in drei Bauweisen neu, hartes Urteil, Zusammenbau, Kritik, Feinschliff (7 Agenten)',
  phases: [
    { title: 'Entwurf', detail: 'drei Bauweisen fuer Kopf und Krallen' },
    { title: 'Urteil', detail: 'Bilder hart bewerten, Sieger und Uebernahmen' },
    { title: 'Zusammenbau', detail: 'beste Teile in ein Skript' },
    { title: 'Kritik', detail: 'was sieht noch nach Stofftier aus' },
    { title: 'Feinschliff', detail: 'Maengel beheben, Endbilder, Skript sichern' },
  ],
}

const SP = 'C:/Users/Kevin/AppData/Local/Temp/claude/33ca7602a1c8491a/c3f66696-88e0-4da2-a026-3f8129d53368/_arbeit/blender_test/baer'
const BASE = 'C:/Users/Kevin/Zomboid/mods/NPCCrew/_docs/modelle/baer/baer.py'
const BLENDER = 'C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe'
const DOCS = 'C:/Users/Kevin/Zomboid/mods/NPCCrew/_docs/modelle/baer'

const REGELN = `
AUFTRAG UND RAHMEN
Das ist eine Blender-Nebenarbeit, KEINE NPC-Crew-Version: kein Lua anfassen, keine Version, kein Changelog, keine commit-meldung, kein workshop_sync, kein git, kein Spiel und keinen Server starten, keine Downloads, nichts im Netz veroeffentlichen.
Suchorte und Schreiborte: nur ${SP} und ${DOCS} (dort nur lesen, ausser es steht ausdruecklich anders in deinem Auftrag) und die Blender-Installation zum Nachschlagen der Python-API. Keine rekursive Suche ueber den Benutzerordner oder ein Laufwerk. Skripte mit dem Write-Werkzeug schreiben (Heredocs mit Python-Code gehen in dieser Shell oft schief).
Blender: "${BLENDER}" --background --factory-startup --python skript.py -- modus. Rendern nur auf der RTX 4090 (das Skript stellt OPTIX schon ein). VOR JEDEM RENDERN pruefen: tasklist | grep -i ProjectZomboid. Laeuft das Spiel, NICHT rendern (Kevin spielt, die Grafikkarte gehoert ihm), sofort aufhoeren und das im Ergebnis sagen. Die Grafikkarte teilen sich bis zu drei Agenten: fuer Zwischenbilder kleine Aufloesung und reduziertes Fell, Vollqualitaet erst am Ende; meldet OPTIX zu wenig Speicher, kurz spaeter nochmal. Foreground-Bash bis 600000 ms Timeout.
Du SIEHST deine Bilder mit dem Read-Werkzeug (PNG). Arbeite in Schleifen: rendern, ansehen, mit der Liste unten vergleichen, aendern. Hoer nicht beim ersten brauchbaren Bild auf, mindestens drei Runden. Beurteile ehrlich, nichts schoenreden.

KEVINS URTEIL UEBER DEN JETZIGEN STAND (woertlich)
"der kopf ist mega schlecht und die krallen auch nicht gut" und "du hast den einfach son kuscheltier knopfauge/nase verpasst statt einen echten". Vorher: "guck mal so sieht ein baer aus und so soll der auch in blender aussehn", mit Fotos aus der Google-Bildersuche 'braun baer'. Der KOERPER gefaellt inzwischen (hohe Beine, Schulterbuckel, Zottelfell) und bleibt im Wesentlichen wie er ist. Neu gebaut werden KOPF und KRALLEN (samt Zehen).

AUSGANGSSKRIPT
${BASE} (rund 950 Zeilen, Blender 5.2 Python). Koerper aus Metabaellen, Voxel-Remesh 0.052 (fuer ein Gesicht viel zu grob, das ist eine Hauptursache: es gibt keine Augenhoehle, keine Lippe, keinen Stirnabsatz), Skelett mit Knochen u. a. "kopf", "kiefer", "prankeR/L", "fussR/L", vier Fellsysteme ueber Gewichtsgruppen (d_koerper, d_bein, d_kopf, l_*), Hilfsfunktionen on_bone(o, knochen), sphere, cone, lz(z) (streckt die Beine), Walk-Zyklus und Aufrichten mit Krallenhieb ueber KF[...], Modi "still" und "anim". Nase, Augen, Lider sind heute Kugeln, Krallen gerade Kegel, Zaehne/Zunge/Gaumen/Kieferhaut kleine Teile am Knochen.
Das Skelett, der Lauf, der Hieb, das Aufreissen des Mauls (Knochen "kiefer", KF "hieb") und der Modus anim MUESSEN weiter funktionieren. Neue Teile haengen ueber on_bone am richtigen Knochen.

SO SIEHT DAS ZIEL AUS (Kevins Fotos, in Worten; das Modell ist rund 2,6 m lang)
Kopf von der Seite: Schaedel fast flach bis leicht gewoelbt, dann ein KLARER Stirnabsatz (konkave Kerbe, 'dish'), dann eine lange, gerade, kraeftige Schnauze mit STUMPF rechteckiger Spitze, darunter tiefer Unterkiefer. Keine Kugel, kein Fuchs, kein Biber. Kopf-Laenge Ohrbasis bis Nase rund 0,50 m; Schaedelbreite samt Fell rund 0,42 m; Schnauze rund 0,17 m breit, 0,16 m hoch, Stirnabsatz bis Nase rund 0,20 m.
Augen: KEINE Perlen, keine Knoepfe. Klein, mandelfoermig, tief unter einem Brauenwulst in der Augenhoehle, schauen nach vorn und sitzen nah an der Schnauzenwurzel, Abstand rund 0,13-0,15 m. Sichtbar ist ein schmaler Ausschnitt: dunkelbraune bis bernsteinfarbene Iris, schwarze Pupille, schwarzer Hautrand ringsum, Oberlid schneidet oben ab, nur ein kleiner Glanzpunkt. Eine ganze runde Kugel darf nie zu sehen sein.
Nase: KEIN glatter Ball. Breites, oben abgeflachtes Polster rund 0,085 m breit, 0,055 m hoch, in die Schnauzenspitze eingelassen, Mittelfurche nach unten (Philtrum), kommafoermige Nasenloecher, die nach aussen auslaufen. Dunkles Anthrazit, nicht rein schwarz, ledrig-feuchte feine Koernung. Darum herum kurzes dunkles Fell, das weich in die helle Schnauze uebergeht.
Maul geschlossen: schwarze Lippenlinie von der Mittelfurche seitlich nach hinten bis unter das Auge, Oberlippe haengt leicht ueber die Unterlippe. Das ist Form plus dunkle Haut, KEIN aufgelegter Draht. Offen (Hieb): dunkle Lippen, rosa-dunkles Zahnfleisch, Eckzaehne, Zunge, kein Loch im Netz, keine schwebenden Teile.
Ohren: klein, rund, weit aussen auf den oberen hinteren Schaedelecken. Eine SCHALE mit Oeffnung nach vorn-aussen, kein Ball: aussen dunkles kurzes Fell, innen helleres laengeres Haar.
Kopffell: Schnauze sehr kurz (1-1,5 cm), fein, OHNE Klumpen, Strich von der Nase nach hinten. Stirn 3-4 cm. Wangen 6-9 cm, nach hinten-unten in die Halskrause laufend. Farbe: Schnauze hell fawn/lohfarben (nahe der Nase dunkler), Stirn goldbraun, um die Augen dunkler, Ohren dunkel, Koerper Schokobraun mit goldenen Spitzen. Weniger Rot als jetzt. Weder Plueschklumpen noch Maske. Kein harter Farbrand zwischen Kopf und Hals.
Krallen und Pfote: FUENF Zehen im Bogen an der Pfotenvorderkante, jede mit eigenem Zehenballen und kurzem Fell. Krallen lang und GEBOGEN, vorn 7-10 cm, hinten 4-6 cm, an der Wurzel dick, seitlich leicht abgeflacht, laufen spitz zu, Bogen nach unten, die Spitze zielt zum Boden und geht nicht unter den Boden. Horn: dunkelbraune Wurzel, zur Spitze heller elfenbein-grau, matt mit etwas Glanz. Keine geraden Kegel, nichts waagerecht wie eine Gabel, keine glaenzenden Metallspitzen.

TECHNISCHE HINWEISE
- hair_length und normal_factor sind dasselbe Feld (hair_length = 4 x normal_factor). Wer beide setzt, verliert den ersten Wert.
- Ist object_align_factor staerker als normal_factor, waechst das Haar auf nach vorn zeigenden Flaechen IN den Koerper: kahle Flecken. Am Kopf also Normale deutlich groesser als Strich.
- Zu dichtes Fell in kleiner Flaeche wird fast schwarz (Selbstschatten), zu duennes laesst Haut durch. Dichte je Flaeche ausgleichen, Haut darunter in Fellfarbe.
- Cycles kann Haaren ueber den Attribute-Knoten eine Farbattribut-Schicht des Traegernetzes geben: das ist die beste Art, das Gesicht gezielt zu faerben. Pruefen, ob es im Bild ankommt, sonst Generated-Koordinaten des Traegers.
- Das Gesicht braucht ein viel feineres Netz. Ein Bildaufloesungs-Ziel gibt es nicht als Dreieckszahl: diese Fassung ist fuer Bilder, die Spielfassung wird spaeter getrennt reduziert. Gewichte werden je Punkt in Python gerechnet und duerfen nicht zu langsam werden.
- Kamera ueber camera(name, pos, ziel, lens=...) (faehrt mit dem Baeren mit), Standbilder ueber render_still.

JEDER LAUF LEGT IN SEINEM ORDNER AB
kopf_profil.png (reine Seitenansicht des Kopfes), kopf_34.png (Dreiviertel von vorn), kopf_front.png (von vorn), pfote.png (Vorderpfote nah, auf Hoehe des Bodens, Gras niedrig), ganz.png (ganzer Baer von der Seite), hieb.png (Hieb mit offenem Maul). Endbilder mindestens 1200x900 mit voller Felldichte, Hintergrund wie im Ausgangsskript.
`

const ERGEBNIS = {
  type: 'object',
  properties: {
    blocked: { type: 'boolean', description: 'true, wenn wegen laufendem Spiel oder Fehler keine Endbilder entstanden' },
    script: { type: 'string', description: 'voller Pfad des fertigen Skripts' },
    ordner: { type: 'string', description: 'voller Pfad des Ordners mit den Bildern' },
    bauweise: { type: 'string', description: 'was konkret gebaut wurde, kurz' },
    runden: { type: 'number' },
    schwaechen: { type: 'array', items: { type: 'string' }, description: 'ehrlich: was sieht noch falsch aus' },
  },
  required: ['blocked', 'script', 'ordner', 'bauweise', 'runden', 'schwaechen'],
}

const BAUWEISEN = [
  { key: 'a', titel: 'Schnittfolge', text: `Baue den Kopf als eigenes Netz aus einer SCHNITTFOLGE: 14-20 Querschnittsringe entlang der Blickachse vom Hals bis zur Nase, jeder Ring eine Superellipse mit Breite, Hoehe und Versatz aus einer Tabelle, die das Profil von oben (Stirnabsatz, Schnauzenruecken) und unten (Kiefer) exakt vorgibt. Danach Unterteilung und analytische Verschiebungsfunktionen fuer Brauenwulst, Augenhoehle, Nasenruecken, Lippenfalte. Verbinde es im Halsbereich mit dem Koerper.` },
  { key: 'b', titel: 'Kontrollkaefig', text: `Baue den Kopf als KONTROLLKAEFIG von Hand: mit bmesh rund 150-300 gesetzte Punkte (links/rechts gespiegelt), Quads, Subdivision Surface Stufe 3 mit Crease an Lippe, Nasenpolster und Augenrand; Augenhoehle und Lippenspalte sind echte Geometrie im Kaefig. Nasenpolster und Ohrschale genauso. Verbinde es im Halsbereich mit dem Koerper.` },
  { key: 'c', titel: 'Abstandsfeld', text: `Baue den Kopf aus einem eigenen ABSTANDSFELD (SDF) in Python: Ellipsoide und Kapseln mit weicher Vereinigung und weicher Subtraktion (Augenhoehlen, Stirnkerbe, Lippenspalte, Nasenfurche, Nasenloecher), dann ein dichtes Netz auf die Nullflaeche projizieren (z. B. feines Voxelnetz oder Kugelnetz entlang des Gradienten) und glaetten. Verbinde es im Halsbereich mit dem Koerper; die Nase darf ein eigenes Feld bekommen.` },
]

phase('Entwurf')
const entwuerfe = await parallel(BAUWEISEN.map(b => () => agent(`${REGELN}

DEIN AUFTRAG: Bauweise ${b.key.toUpperCase()} (${b.titel}).
${b.text}
Krallen und Zehen baust du ebenfalls neu: jede Kralle als Rohrform entlang einer gebogenen Mittellinie mit abnehmendem, leicht ovalem Querschnitt, Zehenballen im Netz, Hornfarbe als Verlauf.
Arbeitsordner: ${SP}/run_${b.key} (anlegen). Kopiere ${BASE} dorthin nach baer_${b.key}.py, stelle OUT auf diesen Ordner, baue dort. Ergaenze einen Modus "kopf", der fuer die Schleifen schnell die Nahbilder rendert (700x525, wenig Samples, reduziertes Fell), und einen Modus "ende" fuer alle sechs Endbilder. Die anderen zwei Laeufe arbeiten parallel an anderen Bauweisen: fremde Ordner nicht anfassen.
Gib das Ergebnis als Struktur zurueck.`, { label: `entwurf:${b.titel}`, phase: 'Entwurf', schema: ERGEBNIS, effort: 'xhigh' }).then(r => r ? { ...r, key: b.key, titel: b.titel } : null)))
const brauchbar = entwuerfe.filter(Boolean).filter(r => !r.blocked)
log(`Entwuerfe fertig: ${brauchbar.length} von ${BAUWEISEN.length} mit Endbildern`)
if (!brauchbar.length) return { abbruch: 'kein Entwurf mit Endbildern', entwuerfe }

phase('Urteil')
const URTEIL = {
  type: 'object',
  properties: {
    bewertung: { type: 'array', items: { type: 'object', properties: {
      key: { type: 'string' }, kopf: { type: 'number', description: '0-10, 10 = kaum von einem Foto zu unterscheiden, 5 = klar Baer aber Spielzeug' }, krallen: { type: 'number' }, begruendung: { type: 'string' },
    }, required: ['key', 'kopf', 'krallen', 'begruendung'] } },
    sieger_kopf: { type: 'string' },
    sieger_krallen: { type: 'string' },
    uebernahmen: { type: 'array', items: { type: 'string' }, description: 'konkrete Einzelteile aus den anderen Laeufen, die in den Sieger sollen, mit Datei und Funktionsname' },
    pflicht: { type: 'array', items: { type: 'string' }, description: 'was beim Zusammenbau zwingend besser werden muss' },
  },
  required: ['bewertung', 'sieger_kopf', 'sieger_krallen', 'uebernahmen', 'pflicht'],
}
const urteil = await agent(`${REGELN}

DEIN AUFTRAG: Du bist Preisrichter und baust nichts. Sieh dir ALLE Bilder (kopf_profil, kopf_34, kopf_front, pfote, ganz, hieb) dieser Laeufe mit dem Read-Werkzeug an und bewerte sie streng gegen die Zielbeschreibung. Kevin hat den Vorgaenger 'mega schlecht' und 'Kuscheltier' genannt; ein Bild, das auch nur entfernt nach Stofftier, Knopfauge, Plastiknase, Biber oder Fuchs aussieht, bekommt hoechstens 4.
Laeufe: ${JSON.stringify(brauchbar.map(r => ({ key: r.key, titel: r.titel, ordner: r.ordner, script: r.script, schwaechen: r.schwaechen })))}
Waehle je den besten Kopf und die besten Krallen, nenne was aus den anderen Laeufen uebernommen werden soll (Datei + Funktion, nachlesen), und was zwingend besser werden muss. Rendere nicht.`, { label: 'urteil', phase: 'Urteil', schema: URTEIL, effort: 'xhigh' })
if (!urteil) return { abbruch: 'Urteil fehlgeschlagen', entwuerfe: brauchbar }

phase('Zusammenbau')
const zusammen = await agent(`${REGELN}

DEIN AUFTRAG: Baue aus den Laeufen EIN Skript mit dem besten Kopf und den besten Krallen und setze die Pflichtpunkte um.
Laeufe: ${JSON.stringify(brauchbar.map(r => ({ key: r.key, titel: r.titel, script: r.script, ordner: r.ordner })))}
Urteil: ${JSON.stringify(urteil)}
Arbeitsordner: ${SP}/run_final (anlegen), Skript baer_final.py, ausgehend vom Skript des Kopf-Siegers. Weiter in Schleifen mit Ansehen der Bilder, bis du die Pflichtpunkte in den Bildern siehst. Am Ende alle sechs Endbilder in Vollqualitaet im Ordner. Gib das Ergebnis als Struktur zurueck.`, { label: 'zusammenbau', phase: 'Zusammenbau', schema: ERGEBNIS, effort: 'xhigh' })
if (!zusammen || zusammen.blocked) return { abbruch: 'Zusammenbau ohne Endbilder', zusammen, urteil }

phase('Kritik')
const KRITIK = {
  type: 'object',
  properties: {
    stofftier_grad: { type: 'number', description: '0 = echtes Tier, 10 = Pluschtier' },
    kopf_note: { type: 'number' },
    krallen_note: { type: 'number' },
    maengel: { type: 'array', items: { type: 'object', properties: {
      was: { type: 'string' }, bild: { type: 'string' }, wie_beheben: { type: 'string', description: 'konkret, mit Stelle im Skript' }, wichtig: { type: 'number', description: '1 = am wichtigsten' },
    }, required: ['was', 'bild', 'wie_beheben', 'wichtig'] } },
  },
  required: ['stofftier_grad', 'kopf_note', 'krallen_note', 'maengel'],
}
const kritik = await agent(`${REGELN}

DEIN AUFTRAG: Du bist der schaerfste Kritiker und baust nichts. Stell dir ein Naturfoto eines Braunbaeren daneben vor. Sieh dir alle sechs Bilder in ${zusammen.ordner} mit dem Read-Werkzeug an, lies das Skript ${zusammen.script} und nenne, was das Bild verraet: wo Stofftier, Knopfauge, Plastik, Spielzeugkralle, falsche Proportion, falsche Farbe, kahle Stelle, Naht am Hals, schwebende Teile. Im Zweifel ist es ein Mangel. Hoechstens die 8 wichtigsten Punkte, je mit konkretem Weg zur Behebung und Stelle im Skript. Rendere nicht.`, { label: 'kritik', phase: 'Kritik', schema: KRITIK, effort: 'xhigh' })

phase('Feinschliff')
const FINAL = {
  type: 'object',
  properties: {
    blocked: { type: 'boolean' },
    skript_im_docs: { type: 'string' },
    bilder: { type: 'array', items: { type: 'string' }, description: 'volle Pfade der Endbilder unter _docs/modelle/baer' },
    anim_geprueft: { type: 'boolean', description: 'Modus anim lief auf einer Kopie mit 2 Bildern durch' },
    behoben: { type: 'array', items: { type: 'string' } },
    offen: { type: 'array', items: { type: 'string' }, description: 'ehrlich, was weiter nach Spielzeug aussieht' },
    zustand: { type: 'string', description: 'ein bis zwei Saetze fuer Kevin auf Deutsch, ohne Beschoenigung' },
  },
  required: ['blocked', 'skript_im_docs', 'bilder', 'anim_geprueft', 'behoben', 'offen', 'zustand'],
}
const final = await agent(`${REGELN}

DEIN AUFTRAG: Behebe die Maengel in ${zusammen.script}, die wichtigsten zuerst, in Schleifen mit Ansehen der Bilder. Arbeite im selben Ordner.
Maengel: ${JSON.stringify(kritik ? kritik.maengel : [])}
Pruefe danach den Modus anim auf einer Kopie mit scene.frame_end auf 2 Bildern und kleiner Aufloesung, nur ob er ohne Fehler durchlaeuft (Python-Fehler und fehlende Dateien). Ein Fehler dort wird behoben.
Danach, und NUR hier darfst du nach ${DOCS} schreiben: vorhandene ${DOCS}/baer.py nach baer_alt_v14.py kopieren, das fertige Skript als ${DOCS}/baer.py ablegen (OUT darf auf den Arbeitsordner zeigen), die Endbilder als baer_kopf_profil.png, baer_kopf_34.png, baer_kopf_front.png, baer_pfote.png, baer_ganz.png, baer_hieb.png. Alte Dateien baer_seite.png, baer_kopf.png, baer_hieb.png duerfen ueberschrieben oder liegen bleiben, nichts anderes im Ordner loeschen.
Gib das Ergebnis als Struktur zurueck.`, { label: 'feinschliff', phase: 'Feinschliff', schema: FINAL, effort: 'xhigh' })

return { urteil, kritik_vorher: kritik, final, entwuerfe: brauchbar.map(r => ({ key: r.key, titel: r.titel, ordner: r.ordner, schwaechen: r.schwaechen })) }
