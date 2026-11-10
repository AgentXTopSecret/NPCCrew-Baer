export const meta = {
  name: 'baer-junges-bau',
  description: 'Baer-Junges hochwertig auf 2c-Stand, Etappe 1: Forschung (2), Spezifikation, Bau Koerper+Clips, Bau Kopf, Bau Textur (6 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Forschung', detail: 'echte Jungtiere + Kritik am Entwurf; Bestand 2c- und Baby-Kette' },
    { title: 'Spezifikation', detail: 'Ziele als Zahlen, Bauweg, Abnahme' },
    { title: 'Bau', detail: 'Koerper + Skelett + Clips, dann Kopf, dann Textur' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const C2 = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c'
const BB = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby'
const H = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/harness'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'

const CTX = `
PROJEKT: NC Bear, lebender Braunbaer (IsoAnimal) fuer Project Zomboid B42.21, gebaut FUER die Mod NPC Crew. Test-Mod NCBearTest
(${T}, NUR LESEN). Dort liegt seit 10.11.2026 10:37 der ERWACHSENE aus Lauf baer-2c (NCBear.glb MD5 08ec7806..., 19.806 Dreiecke, 26 Knochen,
15 Clips, Body-Textur 1024): Sitzen nach Kevins Vorlage, kurzer dunkler Hinterfuss, Beine ohne "Hose in Stiefeln", schmalerer Rumpf.
Dieser Lauf heisst "baer-junges" und baut das BAEREN-JUNGE neu und hochwertig, als eigenes Modell NCBearCub (Groessenstufe Jungtier, im Spiel
Groesse 0,35 bis 0,75; Kevin: Jungtier 0,35 = rund 70 cm lang, 40 cm Schulter).

KEVINS WUNSCH (10.11.2026 nachmittags, woertlich): "ja ich will das du jz das model richtig schoen machst hochwertig wie ein normales braun
baer baby soll das aussehen". Davor: "hast du den auch angepasst an das neue baeren model? wo die fuesse verbessert worden sind?" und "und die
sitz animation ist ja jz auch anders". Frueher zum Modellbau allgemein: "das model verkackst du leider immer". Nimm das ernst: Kevin sieht das
Tier aus der Spielkamera (schraeg von oben, az 0 el 30, von Lauf 2c gegen sein Spielbild geprueft) in Spielgroesse UND er zoomt nah heran.

BESTAND: Es gibt einen ENTWURF aus Lauf baer-baby (${BB}/entwurf/NCBearCub.glb MD5 6c3f0a96 + NCBearCub.png; Skripte
${B}/spiel/baer_{form,netz,textur,export}_baby.py; Berichte ${BB}/SPEZ_BABY.md, bau_baby.md, pruef_baby.md, fix_baby.md; Blatt
${B}/spiel/baby_entwurf.png). Er wurde VOR Lauf 2c auf dem alten Koerper gebaut. Was Claude am 10.11. auf dem Blatt neben Kevins Foto
gesehen hat (ehrlich, das ist der Ausgangspunkt, nicht das Ziel):
- Kopf von vorn: breites flaches Kissen mit sichtbarer Umrisskante wie eine aufgesetzte Maske; das Foto zeigt eine runde Kuppel mit
  flauschigem Umriss. Ohren: kleine Ringe mit dunklem Loch ("Donut", Teddy); das Foto zeigt GROSSE, runde, dicke, flauschige Ohren weit aussen.
- Augen klein und knopfartig; das Foto zeigt groessere runde dunkelbraune Augen mit Glanzpunkt, Fell darum dunkler.
- Fell: grobe, struppige Striche wie Stroh; das Foto zeigt dichtes, kurzes, weiches Flauschfell, schokoladenbraun mit hellen Spitzen.
- Koerper: langes Fass/Wurst, Beine als Saeulen mit "Hose in Stiefeln", Hinterfuss wie ein Menschenfuss mit grauer Sohle, alte Sitzhaltung
  (ein Bein steht mit der Sohle ab). Im Ton-Bild Beulen und Falten am Beinansatz. In Spielgroesse kaum als Junges zu erkennen.
- Gut und zu behalten: kurze helle Schnauze mit grosser schwarzer Nase, Kopf und Hals als EINE verschweisste Flaeche, Technik (26 Knochen,
  15 Clips per Skript umgerechnet, Importer laedt).

VORLAGEN (NUR ansehen; nie hochladen, nie in Modell oder Textur, kein Abpausen, keine Pixel oder Farbflaechen kopieren; gemessene Verhaeltnisse
und Farbtoene als Zielwerte sind erlaubt; Blaetter, auf denen eine Vorlage zu sehen ist, liegen nur unter ${W}/referenz/ und werden nie
weitergegeben): Gesicht ${B}/begleiter/kevin_babygesicht_vorlage.webp (Beschreibung ${B}/begleiter/ENTSCHEIDUNGEN.md Abschnitt "Gesicht des
Baby-Baeren"); Sitzen ${B}/begleiter/kevin_sitzvorlage.png; Fuss/Pfote ${B}/begleiter/kevin_baerenfuss_vorlage.png und kevin_pfotenvorlage.png.
Im Internet duerfen Fotos echter Braunbaeren-Jungen ANGESEHEN werden (nichts speichern, keine Downloads).

ZIEL: ein Junges, das jeder sofort als echtes Braunbaeren-Junges erkennt -- im TON-Bild (ohne Textur) UND mit Textur, nah UND in Spielgroesse
aus der Spielkamera. (1) Kopf gross und rund (Kuppel, Stirnabsatz), grosse runde flauschige Ohren weit aussen, kurze helle Schnauze, grosse
schwarze Nase, runde dunkle Augen mit Glanz, weiche Wangen, kein Maskenrand, kein Fellkragen ums Gesicht. (2) Koerper kurz, rund, kompakt mit
rundem Bauch und rundem Hintern -- kein Fass; kurze kraeftige Beine, die ohne Stufe in grosse weiche Pfoten uebergehen; Hinterfuss und Sohlen
in der Art von Lauf 2c (kurz, breit, dunkel, Zehenballen im Bogen, Fellkranz). (3) Fell dicht, kurz, weich, flauschig; Kopf und Koerper aus
einem Guss; Unterseite, Brust, Achseln, Innenseiten ausgearbeitet (man sieht sie im Sitzen). (4) Sitzen wie Kevins Sitzvorlage: aufrecht,
Hinterbeine eng nach vorn, Sohlen nach vorn/oben, Vorderbeine gerade dazwischen, Pranken flach am Boden; Kopf blickt GERADEAUS (beim
Erwachsenen blickt er im Sitzen noch nach oben, offener Punkt G3 -- beim Jungen gleich richtig). (5) Alle 15 Clips sehen am Jungen sauber aus:
nichts im Boden, nichts schwebt, keine Risse, keine Hautdehnung, Fuesse gleiten nicht.

FESTE REGELN (Technik, damit das Spiel es laedt und der Code-Lauf es benutzen kann):
- Dateien am Ende GENAU: ${W}/mod/42/media/models_X/Skinned/NCBearCub.glb und ${W}/mod/42/media/textures/Body/NCBearCub.png (1024 x 1024 RGB;
  Tiere haben keine Mipmaps, 2048 flimmert). Diese Namen sind fest (der Code-Lauf baut auf mesh Skinned/NCBearCub.glb, Textur NCBearCub).
- Dieselben 26 Knochen wie NCBear.glb (Namen, Eltern, Reihenfolge); eigene Knochenlaengen sind erlaubt und gewollt.
- Dieselben 15 Clip-Namen wie NCBear.glb (Stand 2c in ${T}), je Clip gleiche Dauer und gleiche Abtastzeiten (die Lua und die AnimSet-XMLs
  duerfen nichts merken). Drehungen kommen aus den Clips des ERWACHSENEN Stand 2c (auch die neuen NCBear_SitDown/Sit/StandUp); Lage-Schluessel
  werden fuer die Knochen des Jungen neu gerechnet (Beleg und Weg: ${BB}/SPEZ_BABY.md Abschnitt 3.3). Eine Drehung darf vom Erwachsenen
  abweichen, wo es das Junge nachweislich braucht (Bodenkontakt, Durchdringung, Sitzhaltung, Kopf geradeaus) -- je Clip und Knochen begruenden.
- Hoechstens 20.000 Dreiecke nach dem Spiel-Importer (${H}, Dump.java = so liest das Spiel das GLB), hoechstens 4 Einfluesse je Punkt, Summe 1,
  ein Netz, ein Material, keine offenen oder nicht-mannigfaltigen Kanten. Mundhoehle geschlossen (Kiefer oeffnet in Eat ~15, Bite/Maul ~34,
  Rear ~38 Grad).
- Dehnung je Clip: 99,5 % <= 2,6, Hoechstwert <= 4,0, Achsel/Brust <= 3,5 (Messweg wie Lauf 2c, ${C2}/pruef/gegen/werkzeug/). Boden: Stuetzpfoten
  je Bild hoechstens 1,5 cm ueber oder unter dem Boden (bei Groesse 1,0).
- Massstab: 0,544 Modelleinheiten je Meter; das GLB wird bei Groesse 1,0 gebaut und im Spiel auf 0,35 bis 0,75 verkleinert. Die Spezifikation
  legt die Laenge bei 1,0 fest (Entwurf: 1,857 m), so dass 0,35 zu Kevins "rund 70 cm lang, 40 cm Schulter" passt.
- Weg je Schritt (Translation_Data): mit dem Bein-Faktor des Jungen, so dass die Fuesse NICHT gleiten.
- Nichts aus fremden Mods oder dem Netz kopieren, keine Downloads. Der Erwachsene, die Test-Mod und alle fremden Ordner bleiben unangetastet.

ENTSCHEIDUNGEN FUER DIESEN LAUF (von Claude gesetzt, weil Kevin "wie ein normales Braunbaer-Baby" gesagt hat; er kann sie spaeter umwerfen):
Augen groesser als im Entwurf (Richtung Foto), Rumpf kuerzer und runder (echtes Junges), Unterlid dunkel, Ohrrand als Fell aber Ohren gross
und flauschig. Massstab ist Kevins Bild und das echte Tier aus der Spielkamera -- nicht Literaturmasse; eine Textur darf eine falsche Form
nie verdecken; jedes Ton-Bild kommt NEBEN die Vorlage, bevor jemand "fertig" sagt.

SKRIPTE: Originale in ${B}/spiel (*_2c.py, *_baby.py, *_pfote.py, ...) NIE aendern. Dieser Lauf arbeitet mit neuen Dateien baer_*_junges.py in
${B}/spiel (als Kopie aus *_baby.py und/oder *_2c.py, was die Spezifikation festlegt); Ausgaben nur unter ${W}. Kette, Werkzeuge und Lehren:
Lauf 2c ${C2}/ (SPEZ_2C.md, bau_koerper.md, bau_sitzen.md, bau_gebiss.md, bau_textur.md, fix1_bericht.md, gegen_bericht.md; Werkzeuge
${C2}/werkzeug/ und ${C2}/pruef/gegen/werkzeug/; Skripte ${B}/spiel/baer_{quelle,export,kampf,gewichte,textur,maul}_2c.py), Lauf baer-baby
${BB}/ (Werkzeuge ${BB}/werkzeug/, u. a. mensch.py = Spielfigur, render_baby.py, mess_baby.py, clip_schluessel.py, gpu_render.sh). Werkzeuge
nur KOPIEREN (nach ${W}/werkzeug/). Lehre aus baer-baby: eine kopierte ein.json zeigte auf den ALTEN Dump -- Clip-Posen immer aus dem NEUEN
Importer-Dump rendern.
GPU-REGELN: Renders nur RTX 4090 mit OPTIX (+ Entrauscher). Rendern ist AUCH erlaubt, wenn ProjectZomboid laeuft (nicht pruefen, nicht warten).
Sperre ${W}/gpu.lock (mkdir; existiert er, warten; nach dem Render rmdir; nie > 20 min). Laeuft ein FREMDES blender.exe mit Render (andere
Sitzungen arbeiten auf demselben PC; PowerShell Get-CimInstance Win32_Process), kurz warten -- nie zwei Renders gleichzeitig auf der GPU.
Blender 5.2.3: C:/Users/Kevin/Tools/blender/blender-5.2.3-windows-x64/blender.exe (--background --factory-startup --python s.py -- args).
JDK: C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin. Zwischenstaende klein rendern, Bilder gezielt.
SUCHORTE (nur diese): ${B}, C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_* (lesen; schreiben NUR ${W}), ${T} (lesen), Vanilla
C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media (+ projectzomboid.jar daneben, lesen). Nie rekursiv ueber C:/Users/Kevin
oder ein Laufwerk suchen, nie nach C:/Sandbox.
PARALLEL laeuft der Code-Lauf "baer-zaehmen" (${W}/../baer_zaehmen, Lua): dort NIE schreiben. NIE in die Test-Mod oder nach NPC Crew
schreiben, nichts committen, keine weiteren Agenten starten. Berichte Deutsch, ASCII (ae/oe/ue), mit Belegen (Datei:Zeile, Messwert,
Bildpfad). Statisch/offline heisst nicht gespielt -- so berichten. SIEH DIR DEINE BILDER WIRKLICH AN (Read auf die PNG) und sei ehrlich:
melde, was noch nicht nach einem echten Jungen aussieht.`

phase('Forschung')
const [fr, fb] = await parallel([
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Referenz + Kritik, nichts am Modell bauen): Schreibe ${W}/forschung_referenz.md, Bilder nach ${W}/forschung/referenz/.
1. ECHTE JUNGE: Fotos echter Braunbaeren-Jungen (etwa 3 bis 8 Monate) im Netz ansehen (nur ansehen): von vorn, Seite, 3/4, von hinten, von
   schraeg oben, sitzend, gehend, liegend. Daraus eine Masstabelle als VERHAELTNISSE (Quelle je Zeile, Schaetzung als Schaetzung): Kopflaenge und
   Kopfbreite zur Rumpflaenge, Ohr-Durchmesser und Ohr-Abstand zur Kopfbreite, Augengroesse und -abstand, Schnauzenlaenge, Rumpflaenge zu
   Schulterhoehe, Rumpfbreite, Beinlaenge und Beindicke (oben, am Gelenk), Pfotenbreite, Schulterbuckel, Schwanz, Fell-Laenge je Zone. Was macht
   ein Junges auf einen Blick erkennbar (und was laesst es wie einen verkleinerten Erwachsenen, Teddy, Hund oder Wombat wirken)? Eigene
   Skizzen (selbst gezeichnet) Seite / vorn / schraeg oben aus der Spielkamera.
2. KEVINS VORLAGEN ansehen und beschreiben (Gesicht, Sitzen, Fuss). Die fertige Foto-Vermessung steht in ${BB}/SPEZ_BABY.md Abschnitt 1 -- nicht
   wiederholen, nur pruefen und ergaenzen, was fuer "hochwertig" fehlt (Ohren, Wangen, Fellumriss, Augen).
3. KRITIK AM ENTWURF: ${B}/spiel/baby_entwurf.png und die Einzelbilder unter ${BB}/bilder/ ansehen; den Entwurf (${BB}/entwurf/NCBearCub.glb) selbst
   klein rendern (Ton UND Textur): von vorn, 3/4, Seite, hinten, Spielkamera az 0 el 30 in Spielgroesse neben der Spielfigur. Je Merkmal:
   Soll (echtes Junges, Kevins Foto) gegen Ist, mit Zahl und Bild. Ein Blatt Entwurf neben Vorlage nur unter ${W}/referenz/.
4. FELL: Wie wirkt flauschiges kurzes Jungtier-Fell auf einem 1024er-Bild und einem Netz mit hoechstens 20.000 Dreiecken (Umriss, Straehnen,
   helle Spitzen, weiche Schattierung)? Was hat bei baer-fell, 2c und baer-baby funktioniert, was nicht (${B}/spiel/fell_*.md, ${C2}/bau_textur.md,
   ${BB}/fix_baby.md M2)? Konkrete Empfehlung.
5. SPIELGROESSE: Was bleibt bei 0,35 aus der Spielkamera ueberhaupt lesbar (Kopf, Ohren, helle Schnauze, Umriss)? Daraus die drei wichtigsten
   Formmerkmale, die uebertrieben deutlich sein muessen.
Rueckgabe: Kurzfassung (Deutsch) mit der Masstabelle, den wichtigsten Kritikpunkten und allen Dateipfaden.`, { label: 'forschung:referenz', phase: 'Forschung' }),
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Bestand + Bauweg, nichts am Modell bauen): Schreibe ${W}/forschung_bestand.md, Bilder nach ${W}/forschung/bestand/.
1. LAUF 2c VERSTEHEN: Wie entstehen im Erwachsenen Stand 2c Rumpf, Beine, Hinterfuss, Sohlen, Fellhuelle, Gewichte, Sitz-Clips, Gebiss, Textur
   (${B}/spiel/baer_{quelle,export,kampf,gewichte,textur,maul}_2c.py; Datei:Zeile; Berichte unter ${C2}/)? Welche Befehle bilden die Kette, wie
   lange dauert jeder Schritt, welche Werkzeuge messen was?
2. LAUF baer-baby VERSTEHEN: Wie entstehen Kopf, Hals-Naht, Proportionen, Clip-Umrechnung, Bodenausgleich, Textur
   (${B}/spiel/baer_{form,netz,textur,export}_baby.py; ${BB}/bau_baby.md Abschnitt "Warum nicht die Pfoten-Kette" und fix_baby.md)? Was davon
   ist gut und wiederverwendbar, was ist die Ursache der sichtbaren Maengel (Maskenrand, kleine Ohren, Fass-Rumpf, Hautdehnung M6 durch
   ungleiche Faktoren Rumpf/Beine mit Erwachsenen-Gewichten)?
3. BAUWEG VERGLEICHEN (mit Aufwand, Risiko, erwarteter Guete; klare Empfehlung): (A) Koerper des Erwachsenen Stand 2c als Niedrig-Netz nehmen
   und verformen; (B) eigenes Hochmodell des Jungen in der 2c-Kette (eigene Proportionen, eigene Fellhuelle, eigene Gewichte); (C) Mischung.
   Ziel ist ein echtes Junges, kein verformter Erwachsener -- aber die Fuss-, Bein- und Sitz-Ergebnisse von 2c sollen nicht neu erfunden werden.
4. CLIPS: Die 15 Clips des Erwachsenen Stand 2c aus ${T}/42/media/models_X/Skinned/NCBear.glb mit dem Importer dumpen. Welche Lage-Schluessel
   sind konstant (Knochenlaengen), wie sieht die neue Sitzhaltung in Zahlen aus (Gelenkwinkel, Becken-Hoehe, Kopf gegen Hals bis 58 Grad = G3)?
   Was muss die Umrechnung fuer kuerzere, anders proportionierte Knochen leisten (Becken-Hoehe, Bodenausgleich je Stuetzpfote, Sitzen: Ferse
   liegt auf, Vorderpranken flach, Kopf geradeaus)? Pruefe am Entwurf mit den NEUEN Sitz-Clips probehalber, was passiert (Ton-Bild).
5. HAUSHALT: Dreiecke je Region im Entwurf und im Erwachsenen; Vorschlag fuer das Junge (mehr fuer Kopf, Ohren, Pfoten; Summe <= 20.000);
   Texturplatz je Region (Gesicht braucht Dichte).
6. STOLPERSTEINE aus den Berichten (Importer-Eigenheiten, GLB-Aufbau, Dump-Fallen, GPU-Sperre) als kurze Liste fuer die Bauer.
Rueckgabe: Kurzfassung (Deutsch) mit Empfehlung zum Bauweg, den wichtigsten Zahlen und allen Dateipfaden.`, { label: 'forschung:bestand', phase: 'Forschung' }),
])
log(`Forschung: Referenz ${fr ? 'ok' : 'FEHLT'}, Bestand ${fb ? 'ok' : 'FEHLT'}`)

phase('Spezifikation')
const spez = await agent(`${CTX}

FORSCHUNG REFERENZ (Kurzfassung, Langfassung ${W}/forschung_referenz.md):
${fr || 'FEHLT -- selbst aus Vorlagen, Netz-Fotos und dem Entwurf ableiten'}

FORSCHUNG BESTAND (Kurzfassung, Langfassung ${W}/forschung_bestand.md):
${fb || 'FEHLT -- selbst aus den Skripten und Berichten ableiten'}

DEINE AUFGABE (Spezifikation, nichts am Modell bauen): Schreibe ${W}/SPEZ_JUNGES.md -- messbar, damit alle Bauer und Pruefer dieselben Zahlen
benutzen. Sieh dir vorher die Vorlagen und den Entwurf selbst an.
A BAUWEG: entscheide A/B/C aus der Forschung, mit Begruendung; welche Skripte als baer_*_junges.py entstehen, woraus kopiert, wer sie anfasst.
B KOERPER: Laenge bei Groesse 1,0, Schulterhoehe, Rumpf (Laenge, Breite, Hoehe, Bauchlinie, Rueckenlinie, Hintern), Beine als Profil-Tabelle
  (Hoehe -> Breite von Seite und vorn, ohne Stufe), Pfoten (Breite, Laenge, Zehen, Krallen klein und dunkel-hell wie beim Jungen), Hinterfuss
  und Sohlen nach 2c, Schwanz; Knochenlaengen je Knochen (Faktor zum Erwachsenen) so gewaehlt, dass Rumpf- und Bein-Faktor die Gewichte nicht
  zerreissen (Lehre M6) -- mit Zahlen und Toleranz.
C KOPF: Kuppel, Stirnabsatz, Breite/Hoehe/Laenge, Ohren (Durchmesser, Dicke, Lage, Fellrand), Augen (Durchmesser, Abstand, Lider, Glanz),
  Schnauze, Nase, Wangen, Kiefer/Mundhoehle, Hals und Naht; als Zahlen mit Toleranz (Verhaeltnisse zur Kopfbreite W).
D CLIPS: Umrechnung je Knochen, Becken, Bodenausgleich, Weg je Schritt; Sitz-Clips: Soll-Pose des Jungen als Zahlen (Ferse liegt auf, Beine
  eng, Kopf geradeaus), welche Drehungen dafuer vom Erwachsenen abweichen duerfen.
E FELL + TEXTUR: Zonen, Farbtoene (sRGB), Straehnen (Laenge, Breite, Richtung), helle Spitzen, Schattierung, Umriss-Form fuer Flausch,
  Texturplatz je Region.
F HAUSHALT: Dreiecke je Region (Summe <= 20.000).
G REIHENFOLGE: (1) Bau Koerper = Hochmodell/Netz Koerper + Skelett + Gewichte + alle 15 Clips + GLB (Kopf darf Platzhalter sein),
  (2) Bau Kopf = Kopf, Ohren, Augen, Schnauze, Mundhoehle, Hals-Naht auf dem Koerper von (1), (3) Bau Textur = Fell, Gesicht, Sohlen, die zwei
  Mod-Dateien, alle Renders und das Blatt fuer Kevin.
H ABNAHME: Liste der Pruefbilder (Ton UND Textur; nah und Spielgroesse; vorn, 3/4, Seite, hinten, Spielkamera az 0 el 30; Sitzen aus der
  Spielkamera und von vorn neben der Sitzvorlage; Gehen, Rennen, Fressen, Liegen; neben Spielfigur und Erwachsenem bei 0,35 und 0,75; Entwurf
  alt neben neu) und der Messungen mit Grenzwerten.
Rueckgabe: Kurzfassung mit ALLEN Zahlen, die die Bauer brauchen, und dem Dateipfad.`, { label: 'spezifikation', phase: 'Spezifikation' })

phase('Bau')
const koerper = await agent(`${CTX}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_JUNGES.md, ganz lesen; dazu ${W}/forschung_bestand.md und ${W}/forschung_referenz.md):
${spez || 'FEHLT -- lies die Forschungsberichte unter ' + W + ' und leite die Ziele selbst ab, schreibe sie zuerst auf'}

DEINE AUFGABE (Bau Koerper + Skelett + Clips): Lege die Skripte baer_*_junges.py an und baue Teil B und D der Spezifikation: Koerper des Jungen
(Rumpf, Beine, Pfoten, Hinterfuss, Sohlen, Fellhuelle), Skelett mit den Knochenlaengen des Jungen, Gewichte, alle 15 Clips umgerechnet aus dem
Erwachsenen Stand 2c (auch die neuen Sitz-Clips; Sitzhaltung des Jungen nach der Sitzvorlage, Kopf geradeaus), GLB. Der Kopf darf ein einfacher
Platzhalter sein (der naechste Bauer baut ihn), aber Hals-Ansatz und Nacken muessen stimmen. Arbeite in Runden: Form aendern, Ton-Bild rendern
(Seite, vorn, hinten, schraeg oben aus der Spielkamera), ANSEHEN, neben Skizzen und Vorlagen legen, messen -- erst wenn der Koerper im Ton nach
einem echten Jungen aussieht (kurz, rund, kompakt; kein Fass, keine Saeulen, keine Stufe am Bein), die teure Kette (Gewichte, Dehnung, Boden).
Dann je Clip pruefen und ansehen: Idle, Walk, Run, Eat, SitDown/Sit/StandUp (Sitzen aus der Spielkamera und von vorn neben der Sitzvorlage),
Rear, Death/Dead, Hiebe/Biss (das Junge kaempft nie, die Clips muessen trotzdem ohne Risse laufen). Feste Regeln nachmessen (Knochen, Clip-Namen,
Dauern, Abtastzeiten, Dreiecke, Einfluesse, Dehnung, Boden, Importer laedt).
Ergebnis: ${W}/bau_koerper.md (was gebaut, Datei:Zeile, Messwerte gegen SPEZ, Befehle der Kette zum Wiederholen, was nicht erreicht wurde),
Bilder ${W}/bilder/koerper_*.png, GLB-Stand unter ${W}/glb_koerper/. Ehrlich melden, wenn etwas noch nach Fass, Saeule, Menschenfuss oder
verkleinertem Erwachsenen aussieht.
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:koerper', phase: 'Bau' })

const kopf = await agent(`${CTX}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_JUNGES.md, ganz lesen; dazu ${W}/forschung_referenz.md):
${spez || 'FEHLT'}

BAU KOERPER (vor dir fertig, Bericht ${W}/bau_koerper.md ZUERST LESEN; du arbeitest auf diesem Stand und denselben baer_*_junges.py weiter):
${koerper || 'FEHLT -- pruefe selbst, was unter ' + W + ' und in ' + B + '/spiel/baer_*_junges.py liegt'}

DEINE AUFGABE (Bau Kopf, Teil C der Spezifikation): Kopf, Ohren, Augen, Lider, Schnauze, Nase, Wangen, Kiefer mit geschlossener Mundhoehle,
Hals und Naht -- als echte FORM im Netz, auf dem Koerper des Bauers vor dir. Das Gute aus dem Entwurf darf uebernommen werden (Schnauze, Nase,
verschweisste Hals-Naht; ${B}/spiel/baer_form_baby.py, baer_netz_baby.py), die Maengel muessen weg: kein Kissen mit Maskenrand sondern runde
Kuppel; GROSSE runde dicke Ohren weit aussen mit Fellrand statt Donut-Ringen; groessere runde Augen mit sauberem Lidrand; weiche Wangen.
Runden: Form aendern, Ton-Bild von vorn, 3/4, Seite und aus der Spielkamera rendern, ANSEHEN, NEBEN Kevins Foto legen (Blatt nur unter
${W}/referenz/), gegen die SPEZ messen. Erst wenn das TON-Bild nach dem Jungen aus dem Foto aussieht, ist der Kopf fertig. Kiefer-Gewichte so,
dass beim Fressen und Bruellen nur der Mund oeffnet (kein Entenschnabel, keine Zacken), Kopf und Hals in jedem Clip ohne Kante oder Kerbe.
Die Arbeit des Koerper-Bauers darf nicht verloren gehen: seine Messwerte am Ende nachmessen, ganze Kette bis zum GLB, feste Regeln nachmessen.
Ergebnis: ${W}/bau_kopf.md, Bilder ${W}/bilder/kopf_*.png, GLB-Stand unter ${W}/glb_kopf/.
Rueckgabe: Kurzfassung mit Messwerten, offenen Punkten und Dateipfaden.`, { label: 'bau:kopf', phase: 'Bau' })

const textur = await agent(`${CTX}

SPEZIFIKATION (Kurzfassung; verbindlich ist ${W}/SPEZ_JUNGES.md): ${spez || 'FEHLT'}
BAU KOERPER (${W}/bau_koerper.md): ${koerper || 'FEHLT'}
BAU KOPF (${W}/bau_kopf.md): ${kopf || 'FEHLT'}

DEINE AUFGABE (Bau Textur + Mod-Dateien + Blatt, Teil E der Spezifikation): Baue mit baer_textur_junges.py die Textur fuer das neue Netz:
dichtes, kurzes, weiches Flauschfell (keine groben Stroh-Striche), schokoladenbraun mit hellen Spitzen, Kopf und Koerper aus einem Guss;
Schnauze hell beige, nach oben ins dunklere Gesicht verlaufend; Nase schwarz, feucht glaenzend; Augen dunkelbraun mit Glanzpunkt, Fell darum
dunkler; Ohren innen heller; Sohlen dunkel und ledrig mit Zehenballen und Fellkranz; Krallen; helle, ausgearbeitete Unterseite, Brust, Achseln,
Innenseiten. Die Textur darf keine Formfehler verdecken -- findest du einen, melde ihn und behebe ihn in der Form, wenn es klein ist.
Am Ende liegen GENAU die zwei Mod-Dateien unter ${W}/mod/42/media/ (GLB byte-gleich zum Stand des Kopf-Bauers, sofern du die Form nicht
aendern musstest). Alle Renders der SPEZ Abschnitt H (Ton UND Textur) nach ${W}/bilder/, jedes ANSEHEN. Baue ${W}/bilder/kevin_junges.png
OHNE Vorlagen oder Fotos (nur unsere Renders, kurze Beschriftung Deutsch ASCII): oben gross von vorn und 3/4, darunter Seite, hinten, Sitzen aus
der Spielkamera und von vorn, Gehen, Liegen, je Ton daneben; unten Spielgroesse aus der Spielkamera neben Spielfigur und Erwachsenem bei 0,35 und
0,75; dazu ein Streifen "Entwurf alt | neu". Pruefe das Blatt selbst (Read). Ein zweites Blatt mit Kevins Foto und der Sitzvorlage daneben nur
unter ${W}/referenz/.
Ergebnis: ${W}/bau_textur.md (Schritte, Befehle, Messwerte, MD5 der zwei Dateien, ehrliche Liste: was sieht noch nicht nach einem echten
Jungen aus).
Rueckgabe: Kurzfassung mit MD5, Pfad des Blatts, offenen Punkten.`, { label: 'bau:textur', phase: 'Bau' })

return { fr, fb, spez, koerper, kopf, textur }
