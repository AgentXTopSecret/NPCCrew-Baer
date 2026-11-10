export const meta = {
  name: 'baer-2c',
  description: 'Baer Lauf 2c v2: Sitzen wie Kevins Vorlage, Hinterfuss wie Baer statt Mensch, Kopf passt, Beine eng und ohne Hose-in-Stiefeln, Gebiss + Zunge (Forschung fertig; Spezifikation, Bau Koerper, Bau Sitzen, Bau Gebiss, Textur, Pruefer, Nachbesserung, Gegenpruefer; 10 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Forschung', detail: 'Gebiss/Zunge und Beine (aus dem ersten Start, zwischengespeichert)' },
    { title: 'Spezifikation', detail: 'messen, Ziele als Zahlen, Haushalt' },
    { title: 'Bau', detail: 'Koerper, dann Sitzen, dann Gebiss, dann Textur' },
    { title: 'Pruefer', detail: 'Optik und Technik' },
    { title: 'Nachbesserung', detail: 'Befunde beheben' },
    { title: 'Gegenpruefer', detail: 'unabhaengige Abnahme' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const P = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote'
const F = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_fell'
const CTX = `
PROJEKT: NC Bear, lebender Braunbaer (IsoAnimal) fuer Project Zomboid B42.21, gebaut FUER die Mod NPC Crew. Test-Mod NCBearTest
(C:/Users/Kevin/Zomboid/mods/NCBearTest, NUR LESEN). Stand dort seit 10.11.2026 00:04: Lauf baer-pfoten (GLB MD5 5066fa67..., 19.426 Dreiecke,
15 Clips, Body-Textur 1024, WorldItems-Textur 2048). Dieser Lauf heisst "baer-2c" (Modell).

KEVINS WUNSCH (09.11.2026, woertlich): "hier guck dir mal die zaehne an wenn er schreit so sollen die auch aussehn die zaehne und zunge sieht auch
noch schlecht aus ;D und die beine must du auch noch realistischer machen die sehn aus bei baumstaemme ;D". Alles dazu steht in
${B}/begleiter/ENTSCHEIDUNGEN.md, Abschnitt "Gebiss, Zunge, Beine wie Baumstaemme" (ZUERST LESEN). Vorlage ${B}/begleiter/kevin_bruellen_vorlage.webp
(Bildschirmfoto einer Bildersuche, Stockfotos: NUR ansehen, nie in Modell/Textur/Mod, nie hochladen; eine PNG-Kopie zum Ansehen nur unter ${W}/referenz/).
ZIEL A (Beine): keine gleich dicken Rohre mehr. Vorn Schulterbuckel, Oberarm im Rumpf, kraeftiger Unterarm, der GLEICHMAESSIG zum Handgelenk schmaler
wird, Fell bricht die Kontur hinter dem Ellbogen; hinten breiter Oberschenkel, der in den Hintern uebergeht und zum Sprunggelenk schmaler wird, Ferse
sichtbar. Bekannte Schwaeche aus baer-pfoten, die hier weg muss: ueber dem Gelenk wird das Bein auf kurzer Strecke wieder dick ("Glocke", von hinten
wie Hose im Stiefel), weil dort nur unter z 0,36 gebaut werden durfte -- Bild ${P}/pruef/gegen/blaetter/w5_pranke.png, Text ${P}/gegen_bericht.md
und ${P}/fix1_bericht.md (fix1_form in baer_export_pfote.py). Die Pfoten selbst (Ferse, Sohle, Zehen, Ballen, Krallen) sind fertig und bleiben.
ZIEL B (Gebiss, Zunge): beim Bruellen (Clip NCBear_Rear, auch Bite/Maul) vier lange, gebogene, spitze Eckzaehne, oben und unten eine Reihe kleiner
Schneidezaehne, Backenzaehne angedeutet, Lefzen schwarz und zurueckgezogen, Zahnfleisch dunkel bis rosa, Gaumen; Zunge rosa, breit, flach, tief im
Unterkiefer, Raender leicht hochgewoelbt -- kein Klumpen, keine Rolle. Bei geschlossenem Maul darf kein Zahn durch Lippe oder Backe stechen.
Kevins Test: im TON-Bild (ohne Textur) UND mit Textur, nah UND in Spielgroesse. Eine Textur darf eine falsche Form nie verdecken. Jede neue Form kommt
als Ton-Bild NEBEN die Vorlage (Blatt nur unter ${W}, wird nie weitergegeben), bevor jemand "fertig" sagt.

FESTE REGELN: KOPF-AUSSENFORM BLEIBT (Kevin): Kopfpunkte, Kopf-UV und Kopf-Texel ausserhalb des Mauls bit-gleich; geaendert werden duerfen nur
Maul-Innenraum, Lefzen-Rand, Zaehne, Zunge (die Spezifikation legt die Maske fest). Alle 15 Clips bit-gleich (Abtastzeiten, Schluessel,
Knochen/Namen/Eltern, Offset- und Bind-Matrizen) -- was ohne Clip-Aenderung nachweislich nicht zu retten ist, wird als Vorschlag fuer die Clip-Runde
gemeldet, nicht geaendert. Pfoten unter dem Gelenk und Krallen bleiben wie baer-pfoten (hoechstens Nahtrand). Hoechstens 20.000 Dreiecke im GLB nach
dem Importer, hoechstens 4 Einfluesse je Punkt, Summe 1, ein Netz/Material. Liegehoehe Death/Dead wie bisher, kein Clip tiefer im Boden als heute.
Dehnung: 99,5 % je Clip <= 2,6, Hoechstwert <= 4,0, Achsel/Brust <= 3,5. Was baer-fell und baer-pfoten erreicht haben (helle Unterseite, Straehnen,
Ei-Form, Falten, Pfoten) darf nicht verloren gehen. Netz-Zotteln sind bei baer-fell verworfen worden (sahen aus wie Noppen, ${F}/bau_netz.md) --
Zotteln nur ueber Umriss-Form und Textur, ausser die Forschung belegt einen besseren Weg. Dateinamen/Pfade der Mod bleiben (models_X/Skinned/NCBear.glb,
models_X/Skinned/NCBearDeer.glb, models_X/WorldItems/NCBear.fbx, textures/Body/NCBear.png, textures/WorldItems/NCBear.png). Nichts aus fremden Mods
oder dem Netz kopieren, keine Downloads.
SKRIPTE: Originale in ${B}/spiel (*_anim.py, *_fell.py, *_pfote.py) NICHT aendern. Dieser Lauf arbeitet mit neuen Kopien der *_pfote.py:
baer_quelle_2c.py, baer_export_2c.py, baer_kampf_2c.py, baer_gewichte_2c.py, baer_textur_2c.py, alle in ${B}/spiel; Ausgaben nur unter ${W}
(Mod-Ergebnis ${W}/mod/42/media/, am Ende genau die 5 Dateien). Kette, Befehle und Lehren von baer-pfoten: ${P}/SPEZ_PFOTEN.md, ${P}/bau_netz.md,
${P}/bau_textur.md, ${P}/fix1_bericht.md, ${P}/gegen_bericht.md, ${P}/pruef_optik.md, ${P}/pruef_technik.md; Werkzeuge ${P}/werkzeug/,
${P}/textur/werkzeug/, ${P}/pruef/optik/werkzeug/, ${P}/pruef/technik/, ${P}/pruef/gegen/werkzeug/, ${P}/fix1/ (Bezug ${P}/fix1/bau4/textur/zw_fell_2048.png),
Importer-Harness C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness (Dump.java). Werkzeuge nur KOPIEREN (nach ${W}/werkzeug/), fremde
Ordner (baer_pfote, baer_fell, ...) nie beschreiben. Die ganze Kette dauert ~35-40 min; Form-Runden zuerst mit Formel-Gewichten und Ton-Bildern (~5 min).
GPU-REGELN: Renders nur RTX 4090 mit OPTIX (+ Entrauscher). Rendern ist AUCH erlaubt, wenn ProjectZomboid laeuft -- Kevin hat die alte Regel am
09.11.2026 geloescht (steht so in C:/Users/Kevin/NPCCrew-Nebenprojekte/CLAUDE.md Abschnitt 5): NICHT auf das Spiel pruefen, NICHT darauf warten.
Sperre ${W}/gpu.lock (mkdir; existiert er, warten; nach dem Render rmdir; nie > 20 min); laeuft ein fremdes blender.exe mit Render (PowerShell
Get-CimInstance Win32_Process), kurz warten. Vorlage fuer das Render-Skript: ${P}/werkzeug/gpu_render.sh (kopieren, Sperr-Pfad auf ${W} aendern).
Blender 5.2.3: C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe (--background --factory-startup --python s.py -- args).
JDK: C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin.
SUCHORTE (nur diese): ${B}, C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_* (lesen; schreiben nur ${W}), NCBearTest (lesen), Vanilla
C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (+ Jar, lesen); Internet nur wo die Aufgabe es sagt (nur ansehen, nichts speichern).
NIE in die Test-Mod oder nach NPC Crew schreiben, nichts committen. Kontingent schonen: fertige Messungen nicht wiederholen, Bilder gezielt rendern
und ansehen. Berichte Deutsch, ASCII (ae/oe/ue), mit Belegen (Datei:Zeile, Messwert, Bildpfad, URL). Statisch/offline heisst nicht gespielt -- so
berichten. SIEH DIR DEINE BILDER WIRKLICH AN (Read auf die PNG).`

phase('Forschung')
const [fg, fb] = await parallel([
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Gebiss + Zunge, nichts am Modell bauen): Schreibe ${W}/forschung_gebiss.md, Bilder nach ${W}/forschung/gebiss/.
1. VORLAGE: Kevins Vorlage ansehen. Dazu im Netz nachlesen und ansehen (nur ansehen): Gebiss des Braunbaeren (Zahnformel, Laenge und Kruemmung der
   Eckzaehne beim grossen Maennchen in cm, Luecke hinter dem Eckzahn, Schneidezaehne, Backenzaehne), Zunge, Lefzen, Gaumen. Masstabelle auf unsere
   Kopfgroesse umgerechnet (Groesse 1,0), Quelle je Zeile; Schaetzungen als Schaetzung kennzeichnen.
2. BESTAND: Wie sind Maul-Innenraum, Zaehne, Zunge, Lefzen heute gebaut (${B}/spiel/baer_quelle_pfote.py, baer_export_pfote.py,
   baer_kampf_pfote.py, baer_gewichte_pfote.py, baer_textur_pfote.py; Datei:Zeile)? Welche Punkte/Dreiecke/Texel gehoeren zum Maul, wie viele
   Dreiecke, welche Texel-Dichte? An welchen Knochen haengen sie? Wie weit oeffnet das Maul je Clip (Winkel und Spalt in cm ueber die Zeit: Rear,
   Bite, Maul, Eat, Slam, Idle/Walk/Run geschlossen)? Was deckt die heutige Kopf-Pruefung ab (Kopfprobe, Kopf-Texel) und wie laesst sich
   "Aussenform bleibt, Maul innen darf" als Maske fassen?
3. BILDER heute: Bruellen (Rear am weitesten offen) nah von vorn, schraeg, Seite, je Ton und Textur; geschlossenes Maul nah; Spielgroesse.
   Ein Blatt heute NEBEN Kevins Vorlage (nur unter ${W}). Was genau sieht schlecht aus (Zaehne, Zunge, Lefzen)?
4. MACHBARKEIT: Was geht ohne Clip-Aenderung, wo stechen Zaehne bei geschlossenem Maul durch, wie viele Dreiecke kostet ein gutes Gebiss
   (Vorschlag mit Zahlen), was muss in der Kette neu laufen. Offene Punkte klar benennen.
Rueckgabe: Kurzfassung (Deutsch) mit den wichtigsten Zahlen und allen Dateipfaden.`, { label: 'forschung:gebiss', phase: 'Forschung' }),
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Beine, nichts am Modell bauen): Schreibe ${W}/forschung_beine.md, Bilder nach ${W}/forschung/beine/.
1. VORLAGE: Im Netz nachlesen und ansehen (nur ansehen): Braunbaer stehend/gehend von Seite, vorn, hinten -- Schulterbuckel, Lage von Ellbogen und
   Knie am Rumpf, Unterarm und Unterschenkel (Dicke oben gegen Gelenk), Oberschenkel/Hintern, Fellbehang. Masstabelle als Verhaeltnisse
   (z. B. Unterarm oben : Handgelenk, Schenkelbreite : Rumpfbreite, Buckelhoehe ueber der Rueckenlinie), auf Groesse 1,0 umgerechnet, Quelle je Zeile.
   Eigene Skizzen (selbst gezeichnet) Seite/vorn/hinten.
2. BESTAND: Wie entstehen Schulter, Oberarm, Unterarm, Oberschenkel, Unterschenkel heute (Hochmodell baer_quelle_pfote.py, Fellhuelle und fix1_form in
   baer_export_pfote.py, Gewichte; Datei:Zeile)? Miss am heutigen GLB (Importer-Dump) je Bein die Querschnitte (Breite von der Seite und von vorn)
   in 5-cm-Schritten vom Boden bis in den Rumpf, in Stehen und in zwei Gang-Bildern; zeige, wo "Baumstamm" und wo "Glocke" entsteht (Zahlen + Ton-Bild).
   Wo liegen die Knochen (Schulter, Ellbogen, Handgelenk, Huefte, Knie, Sprunggelenk) -- die sind fest. Welche Zonen sind heute an der Dehnungs- oder
   Faltengrenze (${P}/pruef_technik.md, ${P}/gegen_bericht.md)?
3. ZOTTELN: Wege fuer Fellbehang an Ellbogen, Bauch, Hinterbein, die NICHT wie Noppen aussehen (Umriss-Form, Textur, wenige grosse Lappen?), mit
   Kosten in Dreiecken; kann der Tier-Shader des Spiels Ausschnitt/Alpha (nur statisch aus Vanilla/Jar belegen, sonst "ungeprueft")?
4. MACHBARKEIT + HAUSHALT: Was geht ohne Clip-Aenderung, welche Schritte der Kette muessen neu laufen, Dreiecke heute je Region und Vorschlag
   (Grenze 20.000, heute 19.426; wo laesst sich sparen). Bilder heute neben deinen Skizzen (Ton, Seite/vorn/hinten/Spielwinkel).
Rueckgabe: Kurzfassung (Deutsch) mit den wichtigsten Zahlen und allen Dateipfaden.`, { label: 'forschung:beine', phase: 'Forschung' }),
])
log(`Forschung: Gebiss ${fg ? 'ok' : 'FEHLT'}, Beine ${fb ? 'ok' : 'FEHLT'}`)

const NEU = `
NEU UND VORRANGIG -- KEVIN HAT AM 10.11.2026 ~01:00 IM SPIEL GETESTET (NCBearTest = Stand baer-pfoten, Befehl NCBear_Sit(20)).
Diese Punkte gehoeren JETZT in diesen Lauf und gehen den festen Regeln oben VOR, wo sie sich widersprechen. Woertlich:
"siehste das der fuss sieht aus wie vom menschen jz viel zu lang" -- "und wenn er da so sitzt sieht das aus als ob sein kopf nicht zum koerper
passen wuerde" -- "haste mal das bild gesehn wie es aussehn soll? die beine sind jz auch viel zu weit auseinander" -- "so sollte er da sitzend
aussehn wie auf dem bild" -- "und guck dir mal seine fuesse an und guck mal die fuesse die du gemacht hast" -- "der baer hat so eine fussform wie
menschen xD statt wie von einen braunbaeren".
DAS BILD = seine Sitzvorlage ${B}/begleiter/kevin_sitzvorlage.png (Stockfoto, NUR ansehen, nie in Modell/Textur/Mod, nie hochladen). Sein
Spielbild: ${B}/begleiter/kevin_sitzen_fuss_kopf.webp (2000x1088, Baer etwa bei x 1140-1400, y 400-620; Spielkamera schraeg von oben-vorn;
nur lokal, nie weitergeben). BEIDE BILDER ANSEHEN (Read), Ausschnitte vergroessern (PIL nach ${W}/referenz/).
Was das Spielbild zeigt (von Claude angesehen):
- Der Rumpf ist ein riesiger Fellball; die Fellhuelle steht als Kragen/Maehne RINGSUM um das Gesicht (oben und seitlich bis ueber die Ohren),
  der Kopf sitzt wie ein Gesicht in einer Kapuze darin. Der Kopf ist heller und glatter als das Koerperfell (wirkt aufgeklebt) und zu klein.
  Kein Hals.
- Die Hinterbeine liegen weit gespreizt zur Seite; die Hinterfuesse ragen senkrecht hoch als lange, schmale, HELLGRAUE Rechteck-Sohlen mit
  einer Krallenreihe oben -- wie Menschenfuesse oder Badelatschen.
- Die Vorderbeine sind zwei dunkle Saeulen eng in der Mitte mit weissen Krallen.
Was die Vorlage zeigt:
- Oberkoerper senkrecht, rund, Bauch vorn; Kopf aufrecht OBEN auf dem Koerper, klar ueber der Schulterlinie, im Verhaeltnis groesser, leicht
  zur Seite gedreht; Kopf- und Koerperfell gehen ohne Kante ineinander ueber.
- Vorderbeine gerade nach unten zwischen den Hinterbeinen, Vorderpranken flach am Boden, Krallen dunkel und kurz.
- Hinterbeine nach vorn, eng am Koerper, nur leicht gespreizt; die Hinterfuesse stehen auf der Ferse, Sohle nach vorn/oben.
- HINTERFUSS-FORM: kurze, breite, fast runde bis ovale Sohle (sichtbar etwa 1,1-1,4 mal so lang wie breit), DUNKELBRAUN bis schwarz und ledrig
  (nicht grau), ein grosser Sohlenballen, darueber fuenf grosse runde Zehenballen dicht im Bogen am oberen Rand, kurze dunkle Krallen, dicker
  Fellkranz rundum, der den Sohlenrand ueberdeckt und die Fussform rund macht. Keine schmale Ferse, kein Fussgewoelbe, keine langen Zehen.
DARAUS FOLGT FUER DIESEN LAUF (zusaetzlich zu Ziel A und B):
C1 HINTERFUSS WIE DER BRAUNBAER DER VORLAGE: deutlich kuerzer und breiter (Ziel als Zahl in der SPEZ; Richtwert Laenge etwa 28-30 cm mit Zehen
   statt heute 43, sichtbares Laengen-Breiten-Verhaeltnis im Sitzen 1,1-1,4), runde breite Ferse, Zehenballen gross und dicht im Bogen, Fellkranz
   ueber dem Rand, Sohle dunkelbraun-schwarz. Zehen und Krallen duerfen nach hinten wandern (Krallen-FORM bleibt). Die Literatur-Ziele aus
   baer-pfoten (spitze Ferse, L/B 1,7-1,9) gelten NICHT mehr -- Massstab ist Kevins Vorlage. Vorderpranken bleiben (Krallen hoechstens dunkler).
C2 SITZEN WIE DIE VORLAGE (Richtung (b), die Kevin am 08.11. schon gewaehlt hat, ${B}/begleiter/ENTSCHEIDUNGEN.md Zeilen 70 und 96):
   NCBear_SitDown, NCBear_Sit, NCBear_StandUp neu (Laenge, Abtastzeiten, Schleifen-Art und Ereignisse wie heute, damit die Lua nichts merkt);
   NCBear_SitB nur anpassen, wenn Fuss oder Beine es verlangen. Hinterbeine eng (Fussabstand wie in der Vorlage, als Zahl in der SPEZ),
   Sprunggelenk so tief, dass die KURZE Ferse aufliegt (C3 aus ${P}/SPEZ_PFOTEN.md 4.2 -- mit Kevins Saetzen jetzt freigegeben), Oberkoerper
   aufrecht, Kopf hoch ueber den Schultern, Vorderbeine gerade nach unten zwischen den Hinterbeinen, Pranken flach. Hinsetzen und Aufstehen
   fluessig, nichts im Boden, Gelenkgrenzen je Knochen. Vorbild fuer die Werkzeuge: Lauf baer-anim (${B}/spiel/anim_*.md,
   anim_sitzen_vergleich.png, anim_sitzen_vorschau.mp4); der Sitz-Clip steht heute in ${B}/spiel/baer_kampf_pfote.py (sp_sitzen ab Zeile 1361,
   Clip-Liste ab Zeile 1428). ALLE ANDEREN Clips bleiben bit-gleich, ausser einer ist nachweislich nur so zu retten (dann begruenden).
   Das neue Aufrichten bleibt fuer die Clip-Runde.
C3 KOPF PASST ZUM KOERPER: Kopf-AUSSENFORM bleibt (Kevin 08.11.: "das gesicht also der kopf vom baeren passt so"). Die Passung kommt aus
   (1) Fellhuelle steht nicht mehr als Kragen um das Gesicht -- Nacken, Hals und Schultern so, dass der Kopf OBEN auf dem Koerper sitzt;
   (2) Haltung (C2); (3) schmalerer Rumpf (C4); (4) Farbe und Fell am Uebergang: das Koerperfell an Hals, Nacken und Kehle laeuft in Farbe und
   Helligkeit des Kopfes aus (Koerper-Texel), so dass keine Kante bleibt. Kopf-Texel aendern nur als Vorschlag-Variante mit Bild (eigene Datei
   unter ${W}/vorschlag/, nicht in den 5 Mod-Dateien). Ein gleichmaessig groesserer Kopf (Form gleich) ebenfalls NUR als Vorschlag mit
   Vorher/Nachher-Bild. Erst MESSEN, heute gegen Vorlage: Kopfbreite zu Koerperbreite, Kopf-Oberkante ueber der Schulterlinie, im Sitzen von
   vorn und aus der Spielkamera.
C4 BEINE NICHT SO WEIT AUSEINANDER: Der Rumpf ist zu breit (forschung_beine.md: Gesamtbreite 0,93 m = 0,80 x Schulterhoehe, echt 0,5-0,65;
   eine senkrechte Rumpfwand kragt 13 cm je Seite ueber das Bein). Rumpf und Beinansatz schmaler (Ei-Form, helle Unterseite und Straehnen
   bleiben), Sitzen eng (C2). Im Stehen und Gehen sind die Knochen fest -- schmaler ueber das Netz; was nur per Clip ginge, als Vorschlag melden.
C5 KEIN "HOSE IN STIEFELN" (Kevin dazu, nach NCBear_AnimTest("rear"), im Stehen auf allen Vieren aus der Spielkamera, Baer seitlich nach
   links): "die beine sehn jz zwar besser aus also die fuesse unten aber der uebergang ist so als haette der seine hose in stiefeln gesteckt xD
   komplett krass". Gesehen im Spielbild (nicht gespeichert): die Unterschenkel und Unterarme sind kurze, duenne, dunkle Stiefel mit Pfote;
   gleich ueber Ellbogen/Knie beginnt schlagartig der dicke Rumpf wie ein weiter Sack, der tief ueber den Beinen haengt. Das ist die
   "Glocke" aus Ziel A -- sie ist Kevins WICHTIGSTER Punkt an den Beinen: ein durchgehender, gleichmaessiger Uebergang Pfote -> Unterarm/
   Unterschenkel -> Ellbogen/Knie -> Schulter/Oberschenkel -> Rumpf, in jeder Pose und aus der Spielkamera gesehen (seitlich und schraeg).
   Pfoten unten bleiben so (Kevin: "die fuesse unten" sehen besser aus) -- ausser der Hinterfuss-Form aus C1.
Abnahme zusaetzlich: Stehen auf allen Vieren aus der Spielkamera seitlich (wie Kevins Bild) alt neben neu. Sitzen aus GENAU der Spielkamera von Kevins Spielbild (Hoehe und Winkel nachstellen) -- alt, neu und Vorlage nebeneinander,
Ton und Textur; Hinterfuss nah neben dem Vorlagen-Fuss; Vorschau-Video Hinsetzen/Sitzen/Aufstehen. Blaetter mit Vorlage oder Spielbild nur
unter ${W}, nie weitergeben.`

phase('Spezifikation')
const spez = await agent(`${CTX}
${NEU}

FORSCHUNG GEBISS (Kurzfassung, Langfassung ${W}/forschung_gebiss.md):
${fg || 'FEHLT -- selbst aus den Skripten und der Vorlage ableiten'}

FORSCHUNG BEINE (Kurzfassung, Langfassung ${W}/forschung_beine.md):
${fb || 'FEHLT -- selbst aus den Skripten und dem GLB ableiten'}

Hinweis: Ein erster Spezifikations-Agent wurde nach Kevins neuen Saetzen abgebrochen; liegt schon eine halbe ${W}/SPEZ_2C.md da, darfst du sie
lesen, schreibst sie aber neu.

DEINE AUFGABE (Spezifikation, nichts am Modell bauen): Zuerst die Punkte C1-C4 MESSEN und ANSEHEN: heutiges GLB (NCBearTest) im Sitzen aus
Kevins Spielkamera und von vorn rendern (Ton und Textur), neben Spielbild und Vorlage legen; Hinterfuss-Masse, Fussabstand, Kopf zu Koerper,
Kragenhoehe, Rumpfbreite als Zahlen. Dann schreibe ${W}/SPEZ_2C.md -- messbar, damit alle Bauer und Pruefer dieselben Zahlen benutzen:
A BEINE: je Bein Profil-Tabelle (Hoehe -> Breite von der Seite und von vorn, mit Toleranz) vom Gelenk bis in den Rumpf, ohne Glocke (groesste
  Breitenaenderung je 5 cm als Zahl); Schulterbuckel (aber KEIN Kragen um den Kopf, C3); Uebergang Oberschenkel-Hintern; Fellbehang (Weg, Ort,
  Groesse); Rumpfbreite (C4) als Tabelle.
B GEBISS + ZUNGE: Zaehne einzeln (Anzahl, Laenge, Dicke, Kruemmung, Lage, starr an welchem Knochen), Abstand bei geschlossenem Maul, Zunge,
  Lefzen/Zahnfleisch/Gaumen, Texel-Bedarf, MASKE "Kopf-Aussenform bleibt" (welche Punkte/Texel sich aendern duerfen, wie geprueft).
C HINTERFUSS (C1): Soll-Masse und Form nach der Vorlage (Laenge, Breite, Ferse, Zehenballen, Fellkranz, Farbe der Sohle), Lage zum Sprunggelenk.
D SITZEN (C2): Soll-Pose als Zahlen (Knochenwinkel oder Gelenkhoehen: Becken, Ruecken aufrecht, Kopf ueber Schulterlinie, Sprunggelenk-Hoehe,
  Fussabstand, Lage der Vorderpranken), Clip-Laengen/Abtastzeiten/Ereignisse unveraendert, Uebergaenge, Gelenkgrenzen.
E KOPF-PASSUNG (C3): Soll-Werte Kragen/Nacken, Farbuebergang, Messgroessen.
F HAUSHALT + REIHENFOLGE: Dreiecke je Region (Summe <= 20.000; Gebiss braucht laut Forschung 700-874), woher gespart wird. Kette und Zustaendigkeit:
  (1) Bau Koerper = Beine, Rumpfbreite, Nacken/Kragen, Hinterfuss (Netz + Gewichte; alter Sitz-Clip darf dabei schweben),
  (2) Bau Sitzen = neue Sitz-Clips auf dem Netz von (1), (3) Bau Gebiss, (4) Textur + die 5 Mod-Dateien.
G ABNAHME: Pruefbilder (alle Posen; Ton und Textur; nah und Spielgroesse; alt neben neu; Sitzen aus Kevins Spielkamera neben Vorlage; Gebiss neben
  der Bruell-Vorlage) und Messungen mit Grenzwerten; was ausdruecklich in die Clip-Runde gehoert.
Rueckgabe: Kurzfassung (alle Zahlen, die die Bauer brauchen) und Dateipfad.`, { label: 'spezifikation', phase: 'Spezifikation' })

phase('Bau')
const koerper = await agent(`${CTX}
${NEU}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_2C.md, ganz lesen):
${spez || 'FEHLT -- lies ' + W + '/forschung_beine.md und leite die Ziele selbst ab'}

DEINE AUFGABE (Bau Koerper): Lege die Kopien *_2c.py an (aus *_pfote.py) und baue Teil A, C (Hinterfuss), C3-Kragen/Nacken und C4 (Rumpfbreite)
der Spezifikation: Hochmodell, Fellhuelle/Export, Gewichte, GLB mit allen Clips (Clips noch unveraendert). Das Maul und die Clips fasst du NICHT
an (machen spaetere Bauer). Der alte Sitz-Clip darf mit dem kurzen Fuss schweben (der neue kommt danach). Arbeite in Runden: Form mit
Formel-Gewichten, Ton-Bild rendern, ANSEHEN, neben Vorlage und Spielbild legen, messen (Profil-Tabelle, Glocke weg? Fuss rund und kurz? Kragen
weg? Rumpf schmaler?), erst dann die teure Kette (Gewichte, Dehnung, Falten, Boden). Feste Regeln nachmessen (Clips bit-gleich, Kopf bit-gleich,
Dreiecke, Dehnung, Boden ausser Sitzen). Ergebnis: ${W}/bau_koerper.md (was geaendert, Datei:Zeile, Messwerte gegen SPEZ, Befehle der Kette
zum Wiederholen, was nicht erreicht wurde), Ton-Bilder alt neben neu in ${W}/bilder/ (koerper_*_ton.png: Stehen Seite/vorn/hinten/Spielwinkel,
Gehen, Sitzen alt, Aufrichten, Hinterfuss nah neben Vorlagen-Fuss), GLB-Stand unter ${W}/glb_koerper/. Ehrlich melden, wenn etwas noch nach
Rohr, Glocke, Menschenfuss oder Kragen aussieht.
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:koerper', phase: 'Bau' })

const sitzen = await agent(`${CTX}
${NEU}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_2C.md, ganz lesen):
${spez || 'FEHLT'}

BAU KOERPER (vor dir fertig, Bericht ${W}/bau_koerper.md -- ZUERST LESEN, du arbeitest auf diesem Netz und denselben *_2c.py weiter):
${koerper || 'FEHLT -- pruefe selbst, was unter ' + W + ' und in ' + B + '/spiel/*_2c.py liegt'}

ACHTUNG NEUSTART: Ein erster Sitzen-Bauer lief 10.11. 04:01-04:35 und wurde wegen des Nutzungslimits angehalten (nicht wegen eines Fehlers). Seine Zwischenstaende: ${W}/sitzen/ (blatt, render, probe, log, werkzeug), ${W}/pruef_sitzen/ (s1, s2) und eine HALB fertige Aenderung an ${B}/spiel/baer_kampf_2c.py (heute MD5 7a23aa83; Kopie ${W}/sitzen/abgebrochen_baer_kampf_2c_0431.py). Der Koerper-Bauer hatte die Datei mit MD5 11c7f3c4 hinterlassen (nur Pfade geaendert, bau_koerper.md Abschnitt 1). Sieh dir die Zwischenstaende an und uebernimm, was gut ist; bevor du baust, stelle sicher, dass die Kette ohne deine Sitz-Aenderung das Netz und alle Nicht-Sitz-Clips des Koerper-Bauers byte-gleich ergibt (${W}/glb_koerper/), sonst halbe Aenderungen zuruecknehmen.

DEINE AUFGABE (Bau Sitzen, C2 + Teil D der SPEZ): Baue NCBear_SitDown, NCBear_Sit und NCBear_StandUp neu nach Kevins Sitzvorlage (SitB nur,
wenn noetig) -- in baer_kampf_2c.py (bzw. einer neuen *_2c.py-Kopie jeder weiteren Datei, die du aendern musst; Originale nie). Laenge,
Abtastzeiten, Schleifen-Art und Ereignisse wie heute (nachmessen und belegen). Runden: Pose setzen, Ton-Bild aus Kevins Spielkamera, von vorn und
von der Seite rendern, ANSEHEN, NEBEN Vorlage und Spielbild legen (Blatt nur unter ${W}), messen (Ferse liegt auf, nichts im Boden, Fussabstand,
Kopf ueber Schulterlinie, Gelenkgrenzen, Dehnung/Falten in den neuen Clips). Danach Vorschau-Video Hinsetzen-Sitzen-Aufstehen (${W}/bilder/
sitzen_vorschau.mp4, Ton, Spielkamera und Seite) und die ganze Kette bis zum GLB. Alle anderen Clips bit-gleich nachmessen, die Messwerte des
Koerper-Bauers duerfen nicht schlechter werden. Ergebnis: ${W}/bau_sitzen.md (wie bau_koerper.md), Bilder ${W}/bilder/sitzen_*.png, GLB-Stand
unter ${W}/glb_sitzen/.
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:sitzen', phase: 'Bau' })

const gebiss = await agent(`${CTX}
${NEU}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_2C.md, ganz lesen):
${spez || 'FEHLT -- lies ' + W + '/forschung_gebiss.md und leite die Ziele selbst ab'}

VOR DIR FERTIG (Berichte ZUERST LESEN, du arbeitest auf diesem Stand und denselben *_2c.py weiter):
Bau Koerper (${W}/bau_koerper.md): ${koerper || 'FEHLT'}
Bau Sitzen (${W}/bau_sitzen.md): ${sitzen || 'FEHLT'}

DEINE AUFGABE (Bau Gebiss + Zunge, Teil B der SPEZ): Zaehne, Zunge, Maul-Innenraum, Lefzen-Rand in dieselben *_2c.py; starr an den richtigen
Knochen; nur innerhalb der Maske. Die Arbeit der beiden Bauer vor dir darf nicht verloren gehen (ihre Messwerte am Ende nachmessen). Runden:
Ton-Bild Bruellen nah (vorn, schraeg, Seite) rendern, ANSEHEN, NEBEN Kevins Bruell-Vorlage legen (Blatt nur unter ${W}), geschlossenes Maul in
jedem Clip pruefen (kein Zahn sticht durch, auch bei kleinen Kieferwinkeln 3-14 Grad), Spielgroesse ansehen (Eckzaehne lesbar?). Danach die
ganze Kette bis zum GLB. Feste Regeln nachmessen. Ergebnis: ${W}/bau_gebiss.md, Bilder ${W}/bilder/gebiss_*_ton.png, GLB-Stand unter ${W}/glb_2c/.
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:gebiss', phase: 'Bau' })

const textur = await agent(`${CTX}
${NEU}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_2C.md): ${spez || 'FEHLT'}
BAU KOERPER (${W}/bau_koerper.md): ${koerper || 'FEHLT'}
BAU SITZEN (${W}/bau_sitzen.md): ${sitzen || 'FEHLT'}
BAU GEBISS (${W}/bau_gebiss.md): ${gebiss || 'FEHLT'}

DEINE AUFGABE (Textur + Mod-Dateien): Mit baer_textur_2c.py die Texturen fuer das neue Netz bauen: Fell an den neuen Beinen und am schmaleren
Rumpf (Straehnen folgen der Form, Behang laut SPEZ, helle Unterseite bleibt); Hinterfuss-Sohle dunkelbraun-schwarz und ledrig mit grossen
Zehenballen und Fellkranz wie in der Vorlage (nicht grau); Uebergang Hals/Nacken/Kehle laeuft in Farbe und Helligkeit des Kopfes aus (C3, nur
Koerper-Texel); Maul: Zaehne elfenbein mit hellerer Spitze, Zahnfleisch, schwarze Lefzen, Gaumen mit Querrillen, rosa Zunge. Kopf-Texel
ausserhalb der Maske bit-gleich (eine Kopf-Variante nur als Vorschlag unter ${W}/vorschlag/). Body bleibt 1024, WorldItems 2048 (Lehren
${P}/bau_textur.md). Am Ende liegen genau die 5 Mod-Dateien unter ${W}/mod/42/media/ (GLB, Deer-GLB, FBX, zwei Texturen), das GLB byte-gleich zum
Stand des Gebiss-Bauers. Kontroll-Renders mit Textur UND Ton, alt (NCBearTest) neben neu, ANSEHEN; Sitzen aus Kevins Spielkamera neben Spielbild
und Vorlage; Gebiss mit Textur neben der Bruell-Vorlage (Blaetter nur unter ${W}). Ergebnis: ${W}/bau_textur.md (Schritte, Befehle, Messwerte, MD5
der 5 Dateien, offene Punkte), Bilder ${W}/bilder/textur_*.png.
Rueckgabe: Kurzfassung mit MD5, offenen Punkten und Dateipfaden.`, { label: 'bau:textur', phase: 'Bau' })

phase('Pruefer')
const FIND = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
      title: { type: 'string' }, detail: { type: 'string' }, where: { type: 'string' },
    }, required: ['severity', 'title', 'detail'] } },
    sitzen: { type: 'string', description: 'Urteil Sitzen aus Kevins Spielkamera gegen die Vorlage: Kopf oben, Beine eng, Fuss rund und kurz, mit Bildpfad' },
    baumstamm: { type: 'string', description: 'je Pose und Bein: Bein mit Form oder noch Rohr/Glocke, mit Bildpfad' },
    gebiss: { type: 'string', description: 'Urteil Zaehne/Zunge/Lefzen gegen die Bruell-Vorlage, nah und Spielgroesse, mit Bildpfad' },
    summary: { type: 'string' },
  },
  required: ['findings', 'sitzen', 'baumstamm', 'gebiss', 'summary'],
}
const pruef = await agent(`${CTX}
${NEU}

Der Bau ist fertig. Berichte: ${W}/SPEZ_2C.md, ${W}/bau_koerper.md, ${W}/bau_sitzen.md, ${W}/bau_gebiss.md, ${W}/bau_textur.md. Ergebnis:
${W}/mod/42/media/ (5 Dateien). KURZFASSUNG TEXTUR-BAUER: ${textur || 'FEHLT'}
Du bist PRUEFER (Optik UND Technik) und aenderst NICHTS am Bau (eigene Dateien nur unter ${W}/pruef/, Bericht ${W}/pruef_bericht.md). Glaube
keinem Bericht: selbst messen, selbst rendern, Bilder ansehen. Werkzeuge der frueheren Pruefer duerfen kopiert werden (${P}/pruef/...).
OPTIK: GLB mit dem Importer (Dump.java) lesen, rendern alt (NCBearTest) neben neu, Ton UND Textur: Sitzen aus GENAU Kevins Spielkamera neben
Spielbild und Vorlage (sitzt er wie die Vorlage? Kopf oben ohne Kragen? Beine eng? Hinterfuss rund, kurz, dunkel, wie ein Baerenfuss?),
Hinsetzen/Aufstehen (Video oder Bildfolge), Stehen (Seite, vorn, hinten, Spielwinkel), Gehen, Rennen, Aufrichten/Bruellen, Liegen, Hieb, Biss;
Beine nah (Schulter, Ellbogen, Handgelenk, Knie, Sprunggelenk, Hintern); Maul nah offen und geschlossen; alles auch in Spielgroesse. Ist am Kopf
aussen, an den Vorderpranken, an Unterseite/Straehnen etwas schlechter geworden?
TECHNIK: alle Clips ausser SitDown/Sit/StandUp (und SitB, falls begruendet geaendert) bit-gleich gegen NCBearTest (Abtastzeiten, Schluessel,
Knochen, Offset/Bind); die neuen Sitz-Clips: gleiche Laenge, Abtastzeiten, Ereignisse, Gelenkgrenzen, nichts im Boden, Ferse liegt auf; Kopf
ausserhalb der Maske bit-gleich (Punkte, UV, Texel); Dreiecke <= 20.000, <= 4 Einfluesse, Summe 1, ein Netz, offene Kanten; Zaehne/Zunge starr
am richtigen Knochen, Abstand bei geschlossenem Maul in jedem Clip-Bild; Boden je Clip, Liegehoehe; Dehnung und Falten je Clip gegen die Grenzen;
Profil-Tabelle der Beine und Rumpfbreite gegen SPEZ; Hinterfuss-Masse gegen SPEZ; FBX und Deer-GLB (laden, Skelett, Dreiecke); Texturgroessen;
genau 5 Dateien ohne Test- oder Cheat-Inhalt; MD5.
Schweregrade: blocker = Kevins Wunsch verfehlt oder feste Regel gebrochen; major = deutlich sichtbar oder SPEZ klar verfehlt; minor = Rest.
Jeder Befund mit Beleg (Bildpfad, Messwert, Datei:Zeile) und einem Vorschlag.`, { label: 'pruef:optik+technik', phase: 'Pruefer', schema: FIND })
const all = (pruef && pruef.findings) || []
log(`Pruefer: ${pruef ? 'zurueck' : 'FEHLT'}, ${all.length} Befunde (${all.filter(f => f.severity === 'blocker').length} blocker, ${all.filter(f => f.severity === 'major').length} major)`)

phase('Nachbesserung')
const fix = await agent(`${CTX}
${NEU}

Berichte: ${W}/SPEZ_2C.md, ${W}/bau_koerper.md, ${W}/bau_sitzen.md, ${W}/bau_gebiss.md, ${W}/bau_textur.md, ${W}/pruef_bericht.md.
URTEILE DES PRUEFERS -- Sitzen: ${pruef ? pruef.sitzen : 'FEHLT'}
Beine: ${pruef ? pruef.baumstamm : 'FEHLT'}
Gebiss: ${pruef ? pruef.gebiss : 'FEHLT'}
BEFUNDE: ${JSON.stringify(all)}

DEINE AUFGABE (Nachbesserung): Sichere zuerst den Stand (${W}/fix1/vorher/). Behebe alle blocker und major in den *_2c.py, minor wenn billig; was
nur per Clip-Runde geht, als Vorschlag melden. Nach jeder Aenderung Ton-Bild ansehen (Sitzen immer auch aus Kevins Spielkamera neben der
Vorlage) und die festen Regeln neu messen; am Ende wieder genau 5 Dateien unter ${W}/mod/42/media/. Lehne einen Befund nur mit Beleg ab.
Ergebnis: ${W}/fix1_bericht.md (je Befund: behoben/teilweise/abgelehnt mit Beleg, Messwerte, neue MD5), Bilder ${W}/fix1/bilder/. Gibt es keine
blocker und major, nur pruefen und kurz berichten.
Rueckgabe: Kurzfassung mit MD5 und offenen Punkten.`, { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefer')
const VERDICT = {
  type: 'object',
  properties: {
    ready: { type: 'boolean' },
    sitzen_wie_vorlage: { type: 'boolean' },
    fuss_wie_baer: { type: 'boolean' },
    kopf_passt: { type: 'boolean' },
    baumstamm_irgendwo: { type: 'boolean' },
    gebiss_wie_vorlage: { type: 'boolean' },
    open: { type: 'array', items: { type: 'string' } },
    blocker_left: { type: 'array', items: { type: 'string' } },
    kevin_test: { type: 'string' },
    files_to_copy: { type: 'array', items: { type: 'string' } },
    md5: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['ready', 'sitzen_wie_vorlage', 'fuss_wie_baer', 'kopf_passt', 'baumstamm_irgendwo', 'gebiss_wie_vorlage', 'open', 'blocker_left', 'kevin_test', 'files_to_copy', 'md5', 'summary'],
}
const gegen = await agent(`${CTX}
${NEU}

Berichte: ${W}/SPEZ_2C.md, ${W}/bau_*.md, ${W}/pruef_bericht.md, ${W}/fix1_bericht.md. Ergebnis: ${W}/mod/42/media/.
KURZFASSUNG NACHBESSERUNG: ${fix || 'FEHLT'}

Du bist GEGENPRUEFER (eigener Ordner ${W}/pruef/gegen/, Bericht ${W}/gegen_bericht.md) und aenderst NICHTS am Bau. Unabhaengig von allen
Berichten: GLB mit Dump.java lesen, selbst rendern (alt = NCBearTest neben neu; Ton und Textur; nah und Spielgroesse; alle Posen; Sitzen aus
GENAU Kevins Spielkamera neben Spielbild und Vorlage), ansehen, die festen Regeln selbst messen (Clips: nur die Sitz-Clips duerfen anders sein;
Kopf ausserhalb der Maske; Dreiecke; Einfluesse; Dehnung; Boden; Ferse liegt im Sitzen auf; Maul geschlossen; 5 Dateien; MD5).
ready = true nur, wenn keine feste Regel gebrochen ist UND er sitzt wie die Vorlage (Kopf oben ohne Kragen, Beine eng, Fuss kurz, rund, dunkel --
kein Menschenfuss) UND die Beine in keiner Pose mehr Rohr oder Glocke sind UND das Gebiss beim Bruellen klar besser und der Vorlage aehnlich ist.
Sei streng: Kevin hat bei den Pfoten und jetzt beim Sitzen zu Recht geschimpft, als "fertig" gemeldet wurde, was im Spiel falsch aussah.
Baue ${W}/bilder/kevin_vorher_nachher.png (alt links, neu rechts, Ton und Textur: Sitzen aus Kevins Spielkamera, Sitzen von vorn, Hinterfuss nah,
Bruellen nah, Bruellen Spielgroesse, Stehen Seite, Stehen hinten, Gehen) OHNE Vorlage, Spielbild oder andere Stockfotos. kevin_test: kurze
Schritte fuer Kevin im Spiel (Befehle aus ${B}/spiel/anleitung_pfote.md als Muster).`, { label: 'gegenpruefer', phase: 'Gegenpruefer', schema: VERDICT })

return { fg, fb, spez, koerper, sitzen, gebiss, textur, pruef, befunde: all, fix, gegen }
