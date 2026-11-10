export const meta = {
  name: 'baer-zaehmen-bau',
  description: 'Baer-Junges finden und zaehmen (B1a), Etappe 1: Forschung (2), Plan, Bau Kern, Bau Oberflaeche, Uebernahme-Skript (6 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Forschung', detail: 'Engine-Belege; Bestand, Namen, Naehte' },
    { title: 'Plan', detail: 'Dateien, Schnittstellen, Zahlen, SP/MP' },
    { title: 'Bau', detail: 'Kern und Oberflaeche getrennt, dann Uebernahme-Skript und Staging' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const BB = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const N = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const V = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BA = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'
const TU = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/turret'

const CTX = `
PROJEKT: NC Bear, lebender Braunbaer (IsoAnimal) fuer Project Zomboid B42.21, gebaut FUER die Mod NPC Crew (auf der Mod Bandits). Test-Mod
NCBearTest (${T}, NUR LESEN): Erwachsener als Tierart "bear" (${T}/42/media/lua/shared/NCBearDefs.lua), Kampf im Einzelspieler
(shared/NCBearFight.lua, 100 KB), Testhilfen (client/NCBearBench.lua, NCBearSpawn.lua, NCBearSize.lua, NCBearAttackProbe.lua, NCBearTest.lua),
Skripte ${T}/42/media/scripts/nc_bear*.txt, AnimSets/buck/idle/NCBear_*.xml, Texte bisher nur EN/IG_UI.json. Es gibt noch keinen Ordner
lua/server, kein Wachsen, kein Junges im Spiel.
Dieser Lauf heisst "baer-zaehmen" (Version B1a) und baut den CODE, mit dem man im Spiel ein Baeren-Junges FINDET und ZAEHMT.

KEVINS WUNSCH (10.11.2026 nachmittags, woertlich): "nebenbei will ich das du schonmal den code programmierst das man das baby finden und
tamen kann". Seine frueheren Entscheidungen dazu stehen in ${B}/begleiter/ENTSCHEIDUNGEN.md (ZUERST GANZ LESEN; sie geht vor PLAN.md):
- Bekommen (08.11.): "Weg A (verwaistes Junges im Wald, 3-5 Mal aus der Hand fuettern) plus C (Koederplatz mit Honig oder Fisch)".
- Zaehmen (08.11.): "ich will das man den irgentwie mit futter tamed und den streicheln kann ;D so eine mischung aus beiden soll den
  fortschritt fuellen" und "wir brauchen einen taming balken mit vorschrit und so"; "der baer soll immer streichelbar sein mit cooldown".
- Jeder Spieler darf EINEN Baeren als Begleiter haben. Nach dem Tod des eigenen Baeren ein neues Junges nach 7 Spieltagen.
VORSCHLAG, DER KEVIN ERKLAERT WURDE (noch nicht im Einzelnen bestaetigt -- deshalb jede Zahl als Sandbox-Option mit dieser Vorgabe):
selten im Wald in Spielernaehe ausser Sicht (Sandbox-Haeufigkeit) ODER am Koederplatz (Honig oder Fisch, nach 1 bis 3 Naechten); Zaehm-Balken
aus Fuettern und Streicheln (die Mischung zaehlt mehr als nur eines); ungefuettert und 1 bis 2 Spieltage ohne Kontakt -> das Junge verschwindet,
einmal gefuettert -> es bleibt; je Spieler hoechstens ein Baer und ein wildes Junges. Weitere Vorschlaege: ${B}/begleiter/PLAN.md Abschnitte
3, 4, 9, 10 (und die Berichtigungen am Ende, ${B}/begleiter/KRITIK.md).

UMFANG B1a (genau das, nicht mehr): (1) eigene Tierart fuer das Junge mit eigenem Modell; (2) FINDEN: Weg A Wald und Weg C Koederplatz als
echte Spielmechanik; (3) ZAEHMEN: aus der Hand fuettern und streicheln, Zaehm-Balken mit sichtbarem Fortschritt, Abklingzeiten; (4) BESITZ:
wem das Junge gehoert (Register beim Server, Spiegel am Tier), Grenzen je Spieler, Verschwinde-Regel, Sperre nach Tod; (5) Sandbox-Optionen;
(6) Texte in sieben Sprachen; (7) Testhilfe nur in einer Bench-Datei; (8) Uebernahme-Skript und Naehte-Liste.
NICHT in diesem Lauf (nur so vorbereiten, dass es spaeter passt, und als offen auflisten): Wachsen zum Erwachsenen (Stufen, nextStage,
Weitergabe der Daten beim Wachsen -- deshalb liegt die Wahrheit im Register, nicht nur am Tier), Kampf und Gegenwehr, Befehle (Folgen,
Bleiben, Sitz), Baeren-Fenster mit V, Namensschild und Lebensbalken, Beduerfnisse, Inventar, Schlafen, das Umbenennen der ALTEN Dateien
NCBear* und der Art "bear" (Kevin: zu Beginn von B5a). Die alten Dateien werden in diesem Lauf NICHT geaendert.

FESTE NAMEN (schon wie spaeter in NPC Crew; vor jedem weiteren neuen Namen in ${N}/42/media/lua und in Vanilla greppen, ob er frei ist):
- Tierart des Jungen: "ncbearcub" (Gruppe laut Plan; der Erwachsene bleibt heute "bear").
- Neue Lua-Dateien: BanditsNPCBear*.lua, Modul-Tabelle BanditsNPC.Bear (BanditsNPC = BanditsNPC or {} hinter Existenz-Riegel; NPC Crew ist
  in der Test-Mod OPTIONAL: mit und ohne NPC Crew und Bandits darf nichts kaputtgehen).
- Texte: UI_BN_Bear_* in SIEBEN Sprachen (EN, PTBR, RU, KO, ES, CN, FR; CN nur Zeichen, die Vanilla-CN selbst benutzt), Ablage wie NPC Crew
  (Translate/<L>/UI.json, Round-Trip json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende). Tiernamen-Texte (IGUI_AnimalType_...)
  wie Vanilla sie verlangt.
- Sandbox: Seite/Optionen BanditsNPC.Bear* (Vorbild Turret-Test-Mod und NPC Crew).
- Modell des Jungen: Skript-Eintraege animationsMesh NCBearCub und model NCBearCub_Body (module Base, mesh Skinned/NCBearCub.glb, shader
  animalEffect, wie ${T}/42/media/scripts/nc_bear_tier.txt), Textur NCBearCub (textures/Body/NCBearCub.png), animset "buck" (das Junge traegt
  dieselben 15 Clip-Namen wie der Erwachsene). Das endgueltige Modell baut gerade der parallele Lauf "baer-junges" unter denselben Namen;
  bis dahin dient der Entwurf ${BB}/entwurf/NCBearCub.glb + NCBearCub.png als Platzhalter im Staging.
- Testhilfen (Junges herbeizaubern, Balken setzen, Zeit ueberspringen, Diagnose) NUR in NCBearBench*.lua -- die werden nie nach NPC Crew kopiert.
  In den BanditsNPCBear*-Dateien: kein Konsolenbefehl, kein Spawn-Menue, kein Debug-Rechtsklick, kein Cheat.

EISERNE REGELN:
- ENGINE-AUFRUFE: Rufe nie eine Engine-Methode auf, die du nicht als echten Aufruf in Vanilla-Lua (${V}/lua) oder Bandits (${BA}/42.21 und
  ${BA}/common) gesehen hast -- mit GLEICHEN Argumenttypen. Erst die Fundstelle, dann der Aufruf; Fundstelle (Datei:Zeile) im Kommentar. Nur im
  Jar belegte Methoden sind verboten (brauchen Kevins Wort je Methode) -- als offene Frage melden und einen belegten Weg nehmen. Schon erlaubt
  (Kevins Ja 08.11.): pathToLocation am Tier, mit Jar-Beleg, Existenz-Riegel, pcall und Gegenprobe. Ein pcall um einen unbelegten Aufruf ist
  eine Tarnkappe, keine Absicherung. Kahlua ist kein echtes Lua 5.1 (z. B. kein next); Mehrfachrueckgaben erst in Locals holen.
- EINZELSPIELER UND MEHRSPIELER: alles muss im SP und im MP laufen oder im MP ehrlich als aus/offen markiert sein (dann sagt es der Code dem
  Spieler). SP-Test ist "not isServer() and not isClient()". Tiere rechnet im MP der Server: was der Server wissen muss, kommt nie aus einem
  Client-Glauben (Client bittet, Server prueft und tut). Rote Linien: kein Gegenstand verloren oder verdoppelt (Futter!), kein Kick (Rolle
  user, AntiCheat 2 -- Spawnen ueber Client-Debug-Wege ist tabu), nichts haengt endlos, keine NPC-Crew-Figur wird gestoert.
- LEISTUNG: nichts Teures je Bild; Suchen und Wuerfeln in grossen Abstaenden; Deckel fuer alles, was waechst (Register, Koederplaetze, Junge);
  Diagnose-Zeilen hinter einem Schalter, echte Fehler immer melden. Das Spiel laedt 76 Kacheln um den Spieler: nichts weiter weg ansprechen.
- NICHTS aus fremden Mods kopieren (lesen, um zu lernen, ist erlaubt). Keine Downloads.

WERKZEUGE: Lua-Pruefer von NPC Crew (nur aufrufen): python ${N}/_docs/tools/luacheck.py, scopecheck.py, localcount.py (Grenze 200 Locals, ab 180
aufteilen), luacheck_pz.py (nil-Globals). Lua 5.1 fuer Attrappen: C:/Users/Kevin/Tools/lua51/lua5.1.exe. Jar lesen: Python zipfile nach einem
Ordner unter ${W}/jar, dann C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin/javap.exe -c -p (fertige Auszuege: ${BB}/jar/,
C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/dec/, _arbeit/baer_angriff/).
ABLAGE: Staging = ${W}/mod/ (spiegelt die Wurzel der Test-Mod: ${W}/mod/42/media/lua/{shared,server,client}/..., scripts, Translate, ...);
Berichte ${W}/*.md; Uebernahme-Skript ${B}/tools/baer_uebernahme.py, Naehte-Liste ${B}/NAEHTE.md.
SUCHORTE (nur diese): ${B}, C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_* (lesen; schreiben NUR ${W}), ${T} (lesen), ${TU} und
C:/Users/Kevin/Zomboid/mods/NCTurretTest (lesen, Vorbild), ${N} (NUR LESEN: Code 42/media/lua, Landkarte _docs/landkarte_index.txt greppen,
CLAUDE.md nur den Abschnitt, den du brauchst), Vanilla ${V} (+ projectzomboid.jar daneben, lesen), Bandits ${BA} (lesen). Nie rekursiv ueber
C:/Users/Kevin oder ein Laufwerk suchen, nie nach C:/Sandbox.
PARALLEL laeuft der Modell-Lauf "baer-junges" (C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges, Skripte ${B}/spiel/baer_*_junges.py):
dort NIE schreiben. NIE in die Test-Mod oder nach NPC Crew schreiben, nichts committen, keine weiteren Agenten starten, das Spiel nicht starten.
Berichte Deutsch, ASCII (ae/oe/ue), mit Belegen (Datei:Zeile). Statisch geprueft heisst nicht gespielt -- so berichten; jede
Laufzeit-Behauptung ohne Beleg ist "ungeprueft".`

phase('Forschung')
const [fe, fb] = await parallel([
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Engine-Belege, nichts bauen): Schreibe ${W}/forschung_engine.md. Fuer JEDEN Bedarf unten: der Aufruf, die Fundstelle
als echter Aufruf in Vanilla-Lua oder Bandits (Datei:Zeile, Zeile zitieren), Argumenttypen, auf welcher Seite er laeuft (SP / Server / Client),
Fallen. Wo es nur einen Jar-Beleg gibt: so kennzeichnen (verboten ohne Kevins Wort) und einen belegten Ersatzweg nennen. Wo du nichts findest:
"nicht gefunden" mit den Suchmustern.
1. TIER ERZEUGEN UND ENTFERNEN per Lua: wie ${T}/42/media/lua/client/NCBearSpawn.lua es heute im SP tut; wie der SERVER es im MP tut (Vanilla
   server/ClientCommands.lua rund um Zeile 754 und 964, Debug-Menue DebugContextMenu.lua); Rasse waehlen; sicher entfernen (kein Geistertier,
   keine Leiche). Bleibt ein per Lua erzeugtes Tier beim Speichern/Entladen der Kachel erhalten, und wie findet man es nach dem Laden wieder
   (AnimalID, Tierlisten der Zelle/Kachel, wie NCBearFight.lua ab Zeile 1766 sucht)?
2. TIER-DEFINITION des Jungen: Felder von AnimalDefinitions (Vorbild NCBearDefs.lua und DeerDefinitions.lua fawn/buck): wild, fleeZombies,
   alwaysFleeHumans, canBeDomesticated, canBePicked (Hochheben muss AUS sein), sitRandomly, Stufen ohne nextStage, minSize/maxSize 0,35; was
   bewirken wild/alwaysFleeHumans fuer ein scheues wildes Junges, das naeher kommt, wenn man Futter hat (BaseAnimalBehavior; Jar nur als Lesehilfe)?
3. WALD ERKENNEN und einen Platz ausser Sicht waehlen: Zonen-Abfrage (Forest, DeepForest u. a. -- wie Vanilla-Lua sie liest, z. B. Sammeln
   forageSystem/ISSearchManager, Zonen an der Kachel), freie stehbare Kachel, nicht im Wasser, nicht in Gebaeuden, Sichtpruefung (Bandits
   BanditUtils/LosUtil, Vanilla), Abstand zum Spieler innerhalb der geladenen Flaeche.
4. ZEIT: Spielstunden, Spieltage, Nacht erkennen; Ereignisse fuer seltene Arbeit (EveryTenMinutes, EveryHours, EveryDays, OnTick mit Zaehler).
5. DATEN HALTEN: globale ModData (anlegen, lesen, im MP zum Client schicken, Ereignisse), modData am Tier und ihr Abgleich im MP, Spielerkennung
   (Name/Steam-ID/OnlineID -- was ist stabil ueber Neustarts, wie NPC Crew und Bandits den Besitzer merken).
6. CLIENT <-> SERVER: sendClientCommand / OnClientCommand / sendServerCommand / OnServerCommand (Form, Argumente, wer sie im SP empfaengt),
   Tier ueber die Leitung benennen (ID).
7. RECHTSKLICK AUF EIN TIER: wie Vanilla das Tier-Menue fuellt (ISAnimalContextMenu, AnimalContextMenu, OnFillWorldObjectContextMenu /
   OnClickedAnimalForContext o. ae.) und wie eine Mod dort einen Eintrag fuer EINE Tierart anhaengt, ohne Vanilla-Dateien zu aendern.
8. ZEITAKTION: Vanilla-Streicheln ISPetAnimal.lua ganz lesen (petAnimal, Dauer, Animation) und eine Fuetter-Aktion als Vorbild
   (ISFeedAnimalFromHand o. ae.): Aufbau in B42 (isValid, start, perform, complete auf dem Server, getDuration), hingehen zum Tier, was im MP
   wo laeuft; wie ein Gegenstand dabei sicher verbraucht wird (genau einer, serverseitig, ohne Verlust oder Verdopplung).
9. FUTTER ERKENNEN: Honig und Fisch in B42 (Gegenstandsnamen, Tags, FoodType, Fisch-Erkennung im Vanilla-Angeln), allgemein essbar/verdorben;
   ein KOEDER am Boden: Bodengegenstaende einer Kachel lesen und entfernen (Server), ohne dass der Spieler etwas verliert, was er nicht hergab.
10. AKZEPTANZ: getPlayerAcceptance / petAnimal / Fuettern -- hebt ein ehrlicher Vanilla-Weg (kein Debug, NICHT setDebugAcceptance) die
   Akzeptanz, so dass das Tier bei einem Ruf (Q) zum Spieler kommt (ENTSCHEIDUNGEN.md "Baeren rufen")? Was ist belegt, was nur Jar?
11. BALKEN UND TEXT UEBER DEM TIER zeichnen, ohne Teures je Bild: wie Bandits und NPC Crew Namen/Balken ueber Figuren zeichnen (Fundstellen;
   ISCoordConversion.ToScreen, Text- und Rechteck-Zeichnen, welches Ereignis), dazu ein kleines Fenster/Fortschritt waehrend der Zeitaktion.
12. SANDBOX: Format sandbox-options.txt, Uebersetzungs-Schluessel, Lesen ueber SandboxVars (wie NPC Crew und die Turret-Test-Mod es tun).
13. STOERFAELLE: Was macht die Engine mit einem fremden Tier ohne Stall (Wandern, Stress, Hunger/Durst, Tod durch Verhungern in der
   Zaehm-Zeit, Zombies greifen Tiere nie an, Autos, Spieler-Schlag)? Was davon muss B1a abfangen?
Rueckgabe: Kurzfassung mit einer Tabelle Bedarf -> Aufruf -> Fundstelle -> Seite, den verbotenen/offenen Punkten und dem Dateipfad.`, { label: 'forschung:engine', phase: 'Forschung' }),
  () => agent(`${CTX}

DEINE AUFGABE (Forschung Bestand, Namen, Naehte; nichts bauen): Schreibe ${W}/forschung_bestand.md.
1. ANFORDERUNGEN: Aus ${B}/begleiter/ENTSCHEIDUNGEN.md, ${B}/begleiter/PLAN.md (Abschnitte 3, 4, 5, 9, 10 und "Berichtigt durch Kritik"),
   ${B}/begleiter/KRITIK.md, ${B}/STAND.md Punkt 5 und ${B}/UEBERGABE.md Abschnitt 3 eine nummerierte Liste ALLER Anforderungen an Finden,
   Zaehmen und Besitz -- je Zeile: Kevins Wort (woertlich, mit Fundstelle) ODER "Vorschlag, unbestaetigt". Widersprueche benennen
   (ENTSCHEIDUNGEN geht vor). Ideen aus ${B}/begleiter/recherche_*.md und spion_*.md nur als Idee (nichts kopieren).
2. BESTAND: Alle Lua-Dateien von ${T} lesen (NCBearFight.lua gezielt: wie Baeren gefunden, gemerkt, bewegt werden; welche Tierarten es
   anspricht; was mit einer NEUEN Tierart "ncbearcub" passiert -- darf das Junge vom Kampf-Code NICHT erfasst werden). Skripte, AnimSets, Texte,
   mod.info. Was muss fuer das Junge NEU angelegt werden (Skript-Datei fuer Modell, Tiernamen-Texte), ohne alte Dateien zu aendern?
   ${BB}/SPEZ_BABY.md Abschnitt 3 (Weg ins Spiel, Namen, isBaby, Wachsen) als Vorarbeit lesen und pruefen.
3. NAMEN: Kollisionsprobe fuer "ncbearcub", BanditsNPCBear*, BanditsNPC.Bear, UI_BN_Bear_, Sandbox BanditsNPC.Bear*, NCBearCub in
   ${N}/42/media/lua, Vanilla (lua + scripts) und Bandits. Wie heisst und liegt alles in NPC Crew (Ordner client/server/shared, ISUI,
   Translate/<L>/UI.json, sandbox-options.txt, Sandbox-Uebersetzungen) -- damit die relativen Pfade gleich sind.
4. VORBILD TURRET: ${TU}/tools/turret_uebernahme.py, turret_uebernahme_probe.py, ${TU}/NAEHTE.md und die Test-Mod NCTurretTest lesen: Aufbau
   des Uebernahme-Skripts (Trockenlauf, --probe <ordner>, --echt nur auf Kevins Wort; Cheat-Pruefung; Texte sortiert in sieben UI.json
   zusammenfuehren; erlaubte Fundstellen), Aufbau der Naehte-Liste, wie Bench-Dateien getrennt sind, wie Sandbox und Texte dort heissen.
5. NAEHTE ZU NPC CREW (nur lesen): BanditsNPCLivestockPanel.lua (liest AnimalDefinitions nach group, um Zeile 4079) -- was passiert mit einer
   neuen Tierart/Gruppe? Wie merkt sich NPC Crew Besitzer/Spieler im MP (Muster fuer das Register)? Wo zeichnet NPC Crew Namen/Balken ueber
   Figuren (Muster)? Welche Lehren aus ${N}/CLAUDE.md gelten hier (nur die Abschnitte zu MP-Regeln, Kahlua-Fallen, Zeichnen, Timed Actions
   greppen -- nicht die ganze Datei lesen)?
6. FALLEN: Liste der bekannten Fallen fuer die Bauer (Kahlua, Locals-Grenze, Ladereihenfolge shared/client/server, Zeilenenden je Datei,
   AnimalDefinitions wird erst in IsoWorld.init gelesen, usw.).
Rueckgabe: Kurzfassung mit der Anforderungsliste, der Namenstabelle, den Naehten und dem Dateipfad.`, { label: 'forschung:bestand', phase: 'Forschung' }),
])
log(`Forschung: Engine ${fe ? 'ok' : 'FEHLT'}, Bestand ${fb ? 'ok' : 'FEHLT'}`)

phase('Plan')
const plan = await agent(`${CTX}

FORSCHUNG ENGINE (Kurzfassung, Langfassung ${W}/forschung_engine.md -- ganz lesen):
${fe || 'FEHLT -- die Belege selbst suchen, bevor du planst'}

FORSCHUNG BESTAND (Kurzfassung, Langfassung ${W}/forschung_bestand.md -- ganz lesen):
${fb || 'FEHLT -- selbst aus den Unterlagen ableiten'}

DEINE AUFGABE (Plan, nichts bauen): Schreibe ${W}/PLAN_ZAEHMEN.md -- so genau, dass zwei Bauer mit GETRENNTEN Dateien gleichzeitig arbeiten
koennen und ein dritter danach das Uebernahme-Skript baut.
1. SPIELABLAUF aus Sicht des Spielers (Wald: Junges taucht auf, ist scheu, Futter in der Hand lockt, fuettern, streicheln, Balken, gezaehmt;
   Koederplatz: was der Spieler hinlegt, was nach 1-3 Naechten passiert; was er sieht, wenn etwas nicht geht) -- kurz, als Schritte.
2. ZUSTAENDE des wilden Jungen (erschienen, scheu, angefuettert, gezaehmt, verschwunden, tot) mit Uebergaengen, Zeiten und wer sie rechnet.
3. ZAHLEN: jede Zahl mit Vorgabe und Sandbox-Option (Name BanditsNPC.Bear..., Typ, Bereich): Haeufigkeit im Wald, Abstaende, Koeder-Naechte und
   -Chance, Zaehm-Punkte je Fuettern/Streicheln, Mischungs-Bonus, Abklingzeiten, Verschwinde-Frist, Sperre nach Tod, Deckel. Vorgaben nach
   Kevins Worten (3-5 Mal fuettern zusammen mit Streicheln fuellt den Balken).
4. DATEN: Register beim Server (globale ModData: Schluessel, Felder je Spieler und je Junges), Spiegel am Tier, was der Client weiss; so
   geschnitten, dass spaeter das Wachsen (neues Tier, gleiche AnimalID, modData geht verloren) und der Erwachsene dazupassen.
5. SP UND MP: je Vorgang (Erscheinen, Koeder, Fuettern, Streicheln, Verschwinden, Balken anzeigen) wer bittet, wer prueft, wer tut, welche
   Nachricht; SP-Zweig ausdruecklich. Rote Linien je Vorgang (Futter genau einmal verbraucht; nichts haengt, wenn das Tier weg ist; kein Kick).
   Was im MP nicht belegt werden kann: ehrlich als aus markieren (mit Text fuer den Spieler).
6. DATEIEN: vollstaendige Liste mit Pfad unter ${W}/mod/, Zweck, Besitzer (KERN = shared + server; OBERFLAECHE = client + Translate + Sandbox-
   Texte + Bench), Locals-Haushalt. SCHNITTSTELLE zwischen Kern und Oberflaeche als feste Liste: Funktionsnamen in BanditsNPC.Bear, Befehle
   (Modul, Name, Felder), Felder der Daten, Text-Schluessel UI_BN_Bear_*. Jeder Engine-Aufruf mit Verweis auf die Zeile in forschung_engine.md;
   was dort fehlt, wird NICHT benutzt.
7. LEISTUNG: was wie oft laeuft, Deckel, Schalter fuer Diagnose.
8. BENCH: welche Testbefehle Kevin braucht (Junges in der Naehe erscheinen lassen, Balken setzen, Frist/Nacht ueberspringen, Zustand
   ausgeben, alles aufraeumen) -- nur in NCBearBench*.lua, benutzen dieselben Wege wie das echte Spiel.
9. ATTRAPPEN-TEST: was mit lua5.1 ohne Spiel pruefbar ist (Zustandsmaschine, Register, Zahlen) und wie.
10. KEVINS TEST im Spiel (SP zuerst): 8 bis 12 kurze Schritte mit dem, was er sehen soll; dazu MP-Schritte.
11. OFFEN / NICHT GEBAUT: Liste mit Grund, Fragen an Kevin (hoechstens 5, jede mit Empfehlung).
Rueckgabe: Kurzfassung mit Dateiliste, Schnittstelle, Zahlen und Dateipfad.`, { label: 'plan', phase: 'Plan' })

phase('Bau')
const [kern, ober] = await parallel([
  () => agent(`${CTX}

PLAN (Kurzfassung; verbindlich ist ${W}/PLAN_ZAEHMEN.md, GANZ lesen; Belege ${W}/forschung_engine.md, Bestand ${W}/forschung_bestand.md):
${plan || 'FEHLT -- ohne Plan nicht bauen: schreibe zuerst selbst einen knappen Plan nach den Forschungsberichten'}

DEINE AUFGABE (Bau KERN): Baue genau die Dateien, die der Plan dem KERN zuweist (shared + server: Tierart "ncbearcub" samt Skript-Datei fuer
das Modell, Register, Finden im Wald, Koederplatz, Zaehm-Logik, Verschwinden, Befehle Server-Seite, SP-Zweig) unter ${W}/mod/. Gleichzeitig
baut ein zweiter Bauer die OBERFLAECHE (client, Texte, Sandbox-Texte, Bench): fasse seine Dateien NICHT an und halte die Schnittstelle aus dem
Plan WOERTLICH ein; musst du davon abweichen, schreibe es sofort nach ${W}/schnittstelle_aenderungen.md (und lies die Datei vor dem Abschluss).
Jeder Engine-Aufruf mit Fundstelle im Kommentar (aus forschung_engine.md -- pruefe die Stelle selbst nach, bevor du sie zitierst). Diagnose
hinter einem Schalter. Nach dem Bau: alle vier Lua-Pruefer auf deine Dateien, Zeilenenden pruefen, Attrappen-Test laut Plan mit lua5.1
(${W}/attrappe/kern/), Ergebnis ansehen.
Ergebnis: ${W}/bau_kern.md (Dateien, was jede tut, Engine-Aufrufe mit Fundstelle als Tabelle, SP- und MP-Zweig je Vorgang, Pruefer-Ausgaben,
Attrappen-Ergebnis, was nicht gebaut oder ungeprueft ist).
Rueckgabe: Kurzfassung mit Dateiliste, offenen Punkten und Abweichungen von der Schnittstelle.`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

PLAN (Kurzfassung; verbindlich ist ${W}/PLAN_ZAEHMEN.md, GANZ lesen; Belege ${W}/forschung_engine.md, Bestand ${W}/forschung_bestand.md):
${plan || 'FEHLT -- ohne Plan nicht bauen: schreibe zuerst selbst einen knappen Plan nach den Forschungsberichten'}

DEINE AUFGABE (Bau OBERFLAECHE): Baue genau die Dateien, die der Plan der OBERFLAECHE zuweist (client: Rechtsklick-Eintraege am Jungen fuer
Fuettern und Streicheln, Zeitaktionen, Zaehm-Balken ueber dem Tier und waehrend der Aktion, Meldungen an den Spieler, Koederplatz-Bedienung,
Befehle Client-Seite; Texte UI_BN_Bear_* und Tiernamen in SIEBEN Sprachen; Sandbox-Optionen samt Texten; die Bench-Datei NCBearBench*.lua mit
den Testbefehlen aus dem Plan) unter ${W}/mod/. Gleichzeitig baut ein zweiter Bauer den KERN (shared + server): fasse seine Dateien NICHT an
und halte die Schnittstelle aus dem Plan WOERTLICH ein; musst du davon abweichen, schreibe es sofort nach ${W}/schnittstelle_aenderungen.md (und
lies die Datei vor dem Abschluss). Jeder Engine-Aufruf mit Fundstelle im Kommentar (selbst nachpruefen). Nichts Teures je Bild: der Balken
zeichnet nur fuer Junge in der Naehe aus einer kleinen, selten erneuerten Liste. Kein Testbefehl, kein Debug-Eintrag ausserhalb der Bench-Datei.
Texte: natuerliche Saetze je Sprache, Crew-Figuren neutral, englisch singleplayer/multiplayer zusammengeschrieben; JSON-Round-Trip pruefen; CN
nur Zeichen, die in Vanilla-CN vorkommen (pruefen und belegen). Nach dem Bau: alle vier Lua-Pruefer, Zeilenenden, Attrappen-Test soweit
moeglich (${W}/attrappe/ober/).
Ergebnis: ${W}/bau_oberflaeche.md (Dateien, Engine-Aufrufe mit Fundstelle als Tabelle, Text-Schluessel je Sprache gezaehlt, Pruefer-Ausgaben,
was nicht gebaut oder ungeprueft ist).
Rueckgabe: Kurzfassung mit Dateiliste, offenen Punkten und Abweichungen von der Schnittstelle.`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
log(`Bau: Kern ${kern ? 'ok' : 'FEHLT'}, Oberflaeche ${ober ? 'ok' : 'FEHLT'}`)

const ueber = await agent(`${CTX}

PLAN: ${W}/PLAN_ZAEHMEN.md. BAU KERN (${W}/bau_kern.md): ${kern || 'FEHLT'}
BAU OBERFLAECHE (${W}/bau_oberflaeche.md): ${ober || 'FEHLT'}
Abweichungen: ${W}/schnittstelle_aenderungen.md (falls vorhanden, lesen).

DEINE AUFGABE (Zusammenbau + Uebernahme-Skript):
1. ZUSAMMENBAU PRUEFEN: Passen Kern und Oberflaeche zusammen (jede Funktion, jeder Befehl, jedes Datenfeld, jeder Text-Schluessel, den eine
   Seite benutzt, gibt es auf der anderen -- als Tabelle; Luecken BEHEBEN, kleinste Aenderung, im Bericht nennen)? Alle vier Lua-Pruefer ueber
   ALLE neuen Lua-Dateien, Zeilenenden, JSON-Round-Trip aller sieben Sprachen, gemeinsamer Attrappen-Lauf (Kern + Oberflaeche zusammen laden,
   ein Junges durch den ganzen Ablauf fuehren) unter ${W}/attrappe/gesamt/.
2. STAGING VOLLSTAENDIG: Platzhalter-Modell ${BB}/entwurf/NCBearCub.glb nach ${W}/mod/42/media/models_X/Skinned/NCBearCub.glb und
   NCBearCub.png nach ${W}/mod/42/media/textures/Body/NCBearCub.png kopieren (MD5 notieren; das endgueltige Modell ersetzt sie spaeter unter
   demselben Namen); Skript-Datei des Modells da und richtig; Vorschlag fuer den neuen Text von mod.info als ${W}/mod_info_vorschlag.txt
   (mod.info selbst NICHT ins Staging). Liste ${W}/staging_dateien.txt: jede Datei unter ${W}/mod/ mit MD5 und "neu" oder "ueberschreibt" gegen
   ${T} (es soll NUR neue Dateien geben; ueberschreibt etwas, begruenden).
3. UEBERNAHME-SKRIPT ${B}/tools/baer_uebernahme.py nach dem Vorbild ${TU}/tools/turret_uebernahme.py (lesen, Aufbau lernen, nicht blind
   kopieren): Trockenlauf (schreibt nichts), --probe <ordner> (echter Durchlauf an einer Kopie samt aller Pruefer), --echt nur mit
   ausdruecklichem Schalter (wird in diesem Lauf NIE ausgefuehrt). Es kopiert nur, was nach NPC Crew gehoert (BanditsNPCBear*-Lua, Modelle,
   Texturen, Toene, AnimSets, Skripte), NIE Bench-Dateien, .git oder .gitattributes; es prueft selbst: keine Bench-Datei, kein Testbefehl
   (NCBear_*), kein Testmenue, kein Debug-Rechtsklick in den kopierten Dateien, sonst Abbruch; Texte sortiert in alle sieben UI.json
   zusammenfuehren (Round-Trip); Sandbox-Optionen als Naht. Die ALTEN, noch nicht umbenannten Dateien (NCBear*.lua, Art "bear") sind heute
   NICHT uebernahmereif: das Skript meldet sie klar als "noch umzubenennen (B5a)" -- der Trockenlauf darf deshalb absichtlich rot sein, mit
   genau benannten erlaubten Fundstellen (wie beim Turret). Trockenlauf UND --probe an einer Kopie unter ${W}/probe/ wirklich ausfuehren
   (die Quelle fuer die Probe ist das Staging ueber einer Kopie der Test-Mod; NPC Crew selbst wird nur gelesen bzw. nach ${W}/probe/ kopiert,
   nur die noetigen Ordner), Ausgaben in den Bericht.
4. NAEHTE-LISTE ${B}/NAEHTE.md nach dem Vorbild ${TU}/NAEHTE.md: jede Beruehrung mit NPC Crew und Vanilla (AnimalDefinitions global,
   Livestock-Panel, Sandbox-Seite, UI.json, Tier-Menue, V-Taste spaeter), jeder Aufsatz in OnGameBoot, keine NPC-Crew-Datei wird geaendert;
   erlaubte Fundstellen des Trockenlaufs.
Ergebnis: ${W}/bau_uebernahme.md (Tabelle Zusammenbau, behobene Luecken, Pruefer-Ausgaben, Trockenlauf- und Probe-Ausgabe, offene Punkte).
Rueckgabe: Kurzfassung mit Dateiliste des Stagings (Anzahl, neu/ueberschreibt), Ergebnis von Trockenlauf und Probe, offenen Punkten.`, { label: 'bau:uebernahme', phase: 'Bau' })

return { fe, fb, plan, kern, ober, ueber }
