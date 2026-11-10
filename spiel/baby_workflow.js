export const meta = {
  name: 'baer-baby',
  description: 'Baer-Junges Entwurf: eigenes Gesicht nach Kevins Babyfoto, Junges-Proportionen, Renders fuer Kevin (Spezifikation, Bau, Pruefer, Nachbesserung; 4 Agenten; parallel zu Lauf 2c; nichts in die Test-Mod)',
  phases: [
    { title: 'Spezifikation', detail: 'Foto vermessen, Bauweg ins Spiel, Ziele als Zahlen' },
    { title: 'Bau', detail: 'Kopf/Gesicht + Proportionen, Textur, Renders' },
    { title: 'Pruefer', detail: 'Optik und Technik' },
    { title: 'Nachbesserung', detail: 'Befunde beheben, Blatt fuer Kevin' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const P = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote'
const FB = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_fell/baby'
const CTX = `
PROJEKT: NC Bear, lebender Braunbaer (IsoAnimal) fuer Project Zomboid B42.21, gebaut FUER die Mod NPC Crew. Test-Mod NCBearTest
(C:/Users/Kevin/Zomboid/mods/NCBearTest, NUR LESEN; Stand baer-pfoten, GLB MD5 5066fa67...). Dieser Lauf heisst "baer-baby" und ist ein ENTWURF
des Baer-Jungen (Groessenstufe Jungtier 0,35) zum Ansehen fuer Kevin -- noch kein Einbau ins Spiel.

KEVINS WUNSCH (10.11.2026 ~01:40, woertlich): "kannst du nicht gleichzeitig noch den baby baeren rendern? hatte dir ja ein foto geschickt wie er
aussehen soll von vorne immerhin" -- und auf die Frage "jetzt parallel oder nach Lauf 2c": "Jetzt parallel". Am 09.11.: "guck mal das bild sollst
du nehmen als vorlage fuer das gesicht vom baby baeren wenn der noch klein ist ;D".
VORLAGE: ${B}/begleiter/kevin_babygesicht_vorlage.webp (Foto unbekannter Herkunft: NUR ansehen, nie hochladen, nie in Modell oder Textur -- kein
Abpausen, keine Pixel, keine Farbflaechen daraus kopieren; gemessene Verhaeltnisse und Farbtoene als Zielwerte sind erlaubt). Was es zeigt, steht in
${B}/begleiter/ENTSCHEIDUNGEN.md Abschnitt "Gesicht des Baby-Baeren" (ZUERST LESEN): grosser runder Kopf, breiter als lang, Stirn gewoelbt mit
deutlichem Absatz; grosse runde, dick bepelzte Ohren weit aussen oben, innen heller; kurze stumpfe Schnauze hell beige, nach oben ins dunklere
Gesicht verlaufend; grosse schwarze, glaenzende Nase; grosse runde dunkelbraune Augen weit vorn mit Glanzpunkt, um die Augen dunkler; Fell dicht,
kurz, flauschig, schokoladenbraun mit hellen Spitzen, Wangen leicht abstehend; Junges liegt flach, Kinn zwischen den Vorderpranken.
BESTAND: baer-fell hat ein Junges nur per Knochen-Skalierung probiert (${FB}/bericht.md, baby_vergleich.py, auftrag.json, baby_vergleich.png:
Kopf x1,45, Beine x0,64 lang, Rumpf x0,8-0,84 lang / x1,16 breit, Hals x0,5; Kopfnetz und Gesicht noch Erwachsenen-Form). Kevin hat dieses Bild
gesehen; sein Foto soll ein EIGENES Gesicht ergeben, nicht nur einen groesseren Erwachsenen-Kopf.
ZIEL: (1) Kopf und Gesicht des Jungen nach dem Foto, als echte Form im Netz (Ton-Bild muss das Junge zeigen) plus Textur; (2) Junges-Proportionen
am Koerper (kurze Beine, runder Rumpf, kurzer Hals, grosser Kopf), Kopf sitzt OBEN auf dem Koerper ohne Fellkragen ums Gesicht; (3) Renders fuer
Kevin: von vorn wie das Foto (eine liegende Standbild-Pose "Kinn zwischen den Pranken" nur fuer das Bild ist erlaubt), 3/4 von vorn, Seite, Sitzen,
und aus der Spielkamera in Spielgroesse neben der Spielfigur und dem verkleinerten Erwachsenen; Ton UND Textur; (4) den Weg ins Spiel vorbereiten
und empfehlen, aber NICHT einbauen.
WEG INS SPIEL (spaeter B1, muss leicht werden): gleiche Knochennamen wie der Erwachsene, <= 20.000 Dreiecke, <= 4 Einfluesse je Punkt, Summe 1, ein
Netz/Material, Body-Textur 1024; die 15 Clips des Erwachsenen muessen fuer das Junge nutzbar sein (mit Knochen-Skalierung: Uebersetzungs-Schluessel
der Clips passen nicht mehr zu kuerzeren Knochen -- untersuchen und belegen, ob umrechnen noetig ist). Wie Vanilla B42 Jungtiere macht (eigene
Tierart/Stufe mit eigenem Modell? Wachsen?), STATISCH in Vanilla-Lua/Skripten/Jar belegen (Datei:Zeile), dazu unsere Definition in NCBearTest.
Namen: Test-Mod NCBear*, spaeter in NPC Crew BanditsNPCBear*; jeden neuen Namen in NPC Crew (C:/Users/Kevin/Zomboid/mods/NPCCrew/42/media/lua,
nur lesen) auf Kollision greppen.
BEKANNTE BAUSTELLEN AM KOERPER (NICHT dieser Lauf, laufen gerade in Lauf 2c): Hinterfuss wirkt wie ein Menschenfuss, ueber dem Gelenk "Hose in
Stiefeln", Rumpf zu breit, Fellkragen ums Gesicht, Sitzhaltung. Der Entwurf nimmt den Koerper aus dem heutigen Stand (mit Junges-Proportionen),
sagt das offen und legt den Schwerpunkt auf Kopf und Gesicht; den Kragen ums Gesicht vermeidet er beim Jungen selbst.
PARALLEL LAEUFT LAUF 2c (Arbeitsordner C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c, Skripte ${B}/spiel/*_2c.py): dort NIE schreiben,
nichts davon aendern, nicht auf dessen Zwischenstaende bauen.
FESTE REGELN: Ton-Bild jeder Form neben die Vorlage, bevor jemand "fertig" sagt; eine Textur darf eine falsche Form nie verdecken. Erwachsenen-Modell,
Test-Mod und Lauf 2c bleiben unangetastet. Blaetter, auf denen die Vorlage zu sehen ist, liegen nur unter ${W} und werden nie weitergegeben.
SKRIPTE: Originale in ${B}/spiel NICHT aendern. Neue Kopien *_baby.py (aus *_pfote.py) in ${B}/spiel; Ausgaben nur unter ${W}. Lehren und
Werkzeuge: ${FB}/ (baby_vergleich.py, zusammen.py, mensch.py = Spielfigur), ${P}/werkzeug/ (u. a. gpu_render.sh), ${P}/bau_netz.md,
${P}/bau_textur.md, Importer-Harness C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness (Dump.java). Werkzeuge nur KOPIEREN (nach
${W}/werkzeug/), fremde Ordner nie beschreiben.
GPU-REGELN: Renders nur RTX 4090 mit OPTIX (+ Entrauscher). Rendern ist AUCH erlaubt, wenn ProjectZomboid laeuft (Kevin hat die alte Regel am
09.11.2026 geloescht, C:/Users/Kevin/NPCCrew-Nebenprojekte/CLAUDE.md Abschnitt 5): NICHT auf das Spiel pruefen oder warten. Sperre ${W}/gpu.lock
(mkdir; existiert er, warten; danach rmdir; nie > 20 min). Lauf 2c rendert gleichzeitig: laeuft ein fremdes blender.exe mit Render (PowerShell
Get-CimInstance Win32_Process), warten, bis es fertig ist -- nie zwei Renders gleichzeitig auf die GPU. Vorlage ${P}/werkzeug/gpu_render.sh
(kopieren, Sperr-Pfad auf ${W} aendern). Blender 5.2.3: C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe (--background
--factory-startup --python s.py -- args). JDK: C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin.
SUCHORTE (nur diese): ${B}, C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_* (lesen; schreiben nur ${W}), NCBearTest (lesen), Vanilla
C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (+ projectzomboid.jar daneben, lesen), NPC Crew 42/media/lua (nur lesen, nur
Namensprobe). Internet nur zum Ansehen echter Baerenjungen-Fotos (nichts speichern, keine Downloads).
NIE in die Test-Mod oder nach NPC Crew schreiben, nichts committen. Kontingent schonen (die Woche ist knapp): fertige Messungen nicht wiederholen,
Bilder gezielt rendern, kleine Aufloesung fuer Zwischenstaende. Berichte Deutsch, ASCII (ae/oe/ue), mit Belegen (Datei:Zeile, Messwert,
Bildpfad). Statisch/offline heisst nicht gespielt -- so berichten. SIEH DIR DEINE BILDER WIRKLICH AN (Read auf die PNG).`

phase('Spezifikation')
const spez = await agent(`${CTX}

DEINE AUFGABE (Spezifikation, nichts am Modell bauen): Schreibe ${W}/SPEZ_BABY.md.
1. FOTO VERMESSEN: Foto ansehen, Ausschnitte vergroessern (nur unter ${W}/referenz/). Verhaeltnisse als Zahlen: Kopfbreite zu Kopfhoehe, Ohr-Durchmesser
   und Ohr-Lage zur Kopfbreite, Augenabstand und Augengroesse, Schnauzenlaenge und -breite, Nasenbreite, Stirnabsatz (Winkel), Farbtoene als
   Zielwerte (Schnauze, Gesicht, Augenring, Ohr innen, Fellspitzen). Dazu selbst gezeichnete Skizze vorn/Seite (${W}/skizze_baby.png).
2. HEUTE: Erwachsenen-Kopf (Dump des NCBearTest-GLB) und das Junge aus baer-fell (${FB}) mit denselben Zahlen messen; Ton-Bild von vorn neben dem Foto.
3. WEG INS SPIEL: Vanilla-Jungtiere statisch belegen (AnimalDefinitions, Stufen, Modelle je Stufe, Wachsen; Datei:Zeile), unsere Definition in
   NCBearTest, Clips bei kuerzeren Knochen (Uebersetzungs-Schluessel) -- empfohlener Bauweg mit Begruendung (eigenes GLB vs. Knochen-Skalierung +
   eigener Kopf), Namen (Kollisionsprobe), was spaeter in B1 dazukommt.
4. SOLL: Kopf/Gesicht (Netz: Form, Ohren, Augenhoehlen/Lider, Schnauze, Nase -- als Zahlen mit Toleranz), Textur (Zonen und Farbtoene), Proportionen
   Koerper, Dreiecke, Texturplatz, Liste der Renders fuer Kevin (siehe ZIEL) und der Messungen, mit denen der Pruefer abnimmt.
Rueckgabe: Kurzfassung mit allen Zahlen, die der Bauer braucht, und Dateipfaden.`, { label: 'spezifikation', phase: 'Spezifikation' })

phase('Bau')
const bau = await agent(`${CTX}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_BABY.md, ganz lesen):
${spez || 'FEHLT -- leite die Ziele selbst aus Foto und ENTSCHEIDUNGEN.md ab und schreibe sie zuerst auf'}

DEINE AUFGABE (Bau Entwurf): Lege die Kopien *_baby.py an und baue das Junge nach der SPEZ: Kopf- und Gesichtsform im Netz, Junges-Proportionen,
Textur, GLB-Entwurf unter ${W}/entwurf/ (z. B. NCBearCub.glb + Textur; Name laut SPEZ) mit Knochen und Clips nach dem empfohlenen Weg. Arbeite in
Runden: Form aendern, Ton-Bild von vorn und 3/4 rendern, ANSEHEN, NEBEN das Foto legen (Blatt nur unter ${W}), messen gegen SPEZ -- erst wenn das
Ton-Bild nach dem Jungen aus dem Foto aussieht, die Textur. Danach alle Renders aus der SPEZ (Ton und Textur; vorn, liegend Kinn zwischen den Pranken
als Standbild, 3/4, Seite, Sitzen, Spielkamera in Spielgroesse neben Spielfigur und verkleinertem Erwachsenen) in ${W}/bilder/. Technik nachmessen:
Importer-Dump laedt, Knochennamen gleich, Dreiecke, Einfluesse, ein Netz, mindestens Idle, Walk, Sit sehen ohne Risse aus.
Ergebnis: ${W}/bau_baby.md (was gebaut, Datei:Zeile, Messwerte gegen SPEZ, Befehle zum Wiederholen, was nicht erreicht wurde).
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:baby', phase: 'Bau' })

phase('Pruefer')
const FIND = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
      title: { type: 'string' }, detail: { type: 'string' }, where: { type: 'string' },
    }, required: ['severity', 'title', 'detail'] } },
    gesicht_wie_foto: { type: 'string', description: 'Urteil: sieht das Gesicht im Ton-Bild UND mit Textur aus wie das Junge im Foto? je Merkmal, mit Bildpfad' },
    weg_ins_spiel: { type: 'string', description: 'Urteil zum empfohlenen Bauweg: belegt, machbar, Clips nutzbar?' },
    summary: { type: 'string' },
  },
  required: ['findings', 'gesicht_wie_foto', 'weg_ins_spiel', 'summary'],
}
const pruef = await agent(`${CTX}

Der Entwurf ist gebaut. Berichte: ${W}/SPEZ_BABY.md, ${W}/bau_baby.md. KURZFASSUNG BAUER: ${bau || 'FEHLT'}
Du bist PRUEFER (Optik UND Technik) und aenderst NICHTS am Bau (eigene Dateien nur unter ${W}/pruef/, Bericht ${W}/pruef_baby.md). Glaube keinem
Bericht: selbst rendern und ansehen, selbst messen. OPTIK: Ton UND Textur von vorn neben das Foto, 3/4, Seite, Sitzen, Spielgroesse: Ist es klar ein
Baerenjunges wie im Foto (runder breiter Kopf, Stirnabsatz, grosse runde Ohren weit aussen, kurze helle Schnauze, grosse Nase, grosse Augen mit
Glanz, flauschig)? Oder ein verkleinerter Erwachsener? Wirkt etwas gruselig, plump, verzogen, Kragen ums Gesicht? Lesbar in Spielgroesse? TECHNIK:
GLB mit Dump.java laden, Knochennamen gleich dem Erwachsenen, Dreiecke <= 20.000, <= 4 Einfluesse, Summe 1, ein Netz, offene Kanten, Risse oder
Dehnung in Idle/Walk/Run/Sit, Bodenkontakt, Textur 1024, keine Pixel aus dem Foto, der empfohlene Weg ins Spiel statisch belegt (Datei:Zeile
nachsehen), Namen kollisionsfrei. Schweregrade: blocker = Kevins Wunsch verfehlt oder Regel gebrochen; major = deutlich sichtbar oder SPEZ klar
verfehlt; minor = Rest. Jeder Befund mit Beleg und Vorschlag.`, { label: 'pruef:baby', phase: 'Pruefer', schema: FIND })
const all = (pruef && pruef.findings) || []
log(`Pruefer: ${pruef ? 'zurueck' : 'FEHLT'}, ${all.length} Befunde (${all.filter(f => f.severity === 'blocker').length} blocker, ${all.filter(f => f.severity === 'major').length} major)`)

phase('Nachbesserung')
const fix = await agent(`${CTX}

Berichte: ${W}/SPEZ_BABY.md, ${W}/bau_baby.md, ${W}/pruef_baby.md.
URTEIL GESICHT: ${pruef ? pruef.gesicht_wie_foto : 'FEHLT'}
URTEIL WEG INS SPIEL: ${pruef ? pruef.weg_ins_spiel : 'FEHLT'}
BEFUNDE: ${JSON.stringify(all)}

DEINE AUFGABE (Nachbesserung + Blatt fuer Kevin): Sichere zuerst den Stand (${W}/fix1/vorher/). Behebe alle blocker und major in den *_baby.py,
minor wenn billig; nach jeder Aenderung Ton-Bild neben dem Foto ansehen. Lehne einen Befund nur mit Beleg ab. Baue am Ende
${W}/bilder/kevin_baby_entwurf.png OHNE das Foto (nur unsere Renders): oben gross das Junge von vorn (Textur) und liegend Kinn zwischen den Pranken,
darunter 3/4, Seite, Sitzen (Textur und Ton), unten Spielgroesse neben Spielfigur und verkleinertem Erwachsenen; kurze Beschriftung (Deutsch,
ASCII). Pruefe das Blatt selbst (Read). Ein zweites Blatt mit Foto daneben nur unter ${W}/referenz/ (nie weitergeben). Schreibe
${W}/fix_baby.md (je Befund behoben/teilweise/abgelehnt mit Beleg; empfohlener Weg ins Spiel in 5 Saetzen; offene Fragen an Kevin; ehrliche
Liste, was am Koerper noch aus dem Erwachsenen kommt und in Lauf 2c behoben wird).
Rueckgabe: Kurzfassung, Pfad des Blatts fuer Kevin, offene Punkte.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

return { spez, bau, pruef, befunde: all, fix }
