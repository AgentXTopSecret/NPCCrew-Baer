export const meta = {
  name: 'baer-f4',
  description: 'Baer F4: Traglast + eigenes Inventar (alles tragen, 1000 Gegenstaende, Jar-Ausnahmen wie NPC Crew) + Packtaschen-Gegenstand + selbst fressen -- Bau nach PLAN_F4.md mit Kevins Antworten (8 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Bau', detail: 'Pruef-Tore + Jar-Liste, KERN, OBERFLAECHE parallel; danach Texte' },
    { title: 'Pruefung', detail: 'Code (Verlust/Verdopplung) und Bild' },
    { title: 'Nachbesserung' },
    { title: 'Gegenpruefung' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const F = W + '/f4'
const S = W + '/mod_f4'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-f4" fuer Kevins Mod NPC Crew (Project Zomboid 42.22; Bandits ${BAN}/42.22 und ${BAN}/common). Kevin
programmiert nicht, er spielt und testet. Berichte auf Deutsch, "statisch geprueft, nicht gespielt", jede Behauptung mit Fundstelle (Datei:Zeile).
Keine Fragen an Kevin waehrend des Laufs: Kleinfragen mit dem empfohlenen Weg bauen und als "Fragen fuer Kevin" im Bericht fuehren.

AUFTRAG: F4 = Traglast + EIGENES INVENTAR des gezaehmten Baeren + Gegenstand Baeren-Packtaschen + selbst fressen aus dem Inventar. DER PLAN GILT:
${F}/PLAN_F4.md (660 Zeilen, GANZ lesen; Forschung ${F}/FORSCHUNG_F4.md). Weg: Register-Inventar (Saetze im Baeren-Eintrag) + Spieler-Kopie als
Absturz-Schutz (Plan 2), Geben/Nehmen ueber Netz-Zeitaktionen, Tod -> alles auf den Boden in B.Close, F5-Schnittstelle mitbauen.

KEVINS ANTWORTEN VOM 13.11. ABENDS GEHEN VOR DEM PLAN (woertlich ${F}/KEVIN_ANTWORTEN.md, ZUERST lesen; auch ${B}/begleiter/ENTSCHEIDUNGEN.md unten):
 1. ALLES TRAGEN ("alles was es gibt"): die "Packtier-Regel" des Plans (Abschnitt 5) wird ERSETZT -- er nimmt jeden Gegenstand, auch Kleidung,
    Taschen, gekochtes/verbranntes/gefrorenes Essen, Schusswaffen (geladen, mit Anbauteilen), Schluessel, Zettel/Karten, Elektronik, Klingen.
    JAR-AUSNAHME: Kevins Wort "Ja, dieselben wie NPC Crew" -- der Baer darf JEDE Jar-Methode nutzen, die NPC Crew fuer seine Inventar-Manifeste/
    Wiederherstellung schon mit Kevins Wort nutzt (NUR LESEN: ${NC}/42/media/lua, z. B. shared/BanditsNPC.lua ~4200-5100 Manifest-Felder, die
    Versionszeilen ab v3.10.15 "gekocht/verbrannt/gefroren nachgeholt", ${NC}/_docs und NPC Crews CLAUDE.md, Abschnitt zu Jar-Ausnahmen). Lerne, wie
    NPC Crew JEDE Art Gegenstand verlustfrei als Datensatz speichert und wiederherstellt (Feldliste je Art, Fundstellen), und baue das fuer den Baeren
    nach (eigener Code in BanditsNPCBear*-Dateien, nichts zur Laufzeit aus NPC Crew aufrufen; NPC Crew ist in der Test-Mod nicht da). Jede genutzte
    Jar-Methode: Klasse.Methode + javap-Offset + die NPC-Crew-Zeile, die Kevins Wort belegt, im Kommentar UND in ${F}/JAR_LISTE.md. Eine Methode, die
    NPC Crew NICHT nutzt, ist NICHT gedeckt: dann diesen Wert ehrlich weglassen bzw. den Gegenstand mit Grund ablehnen und als "Frage fuer Kevin"
    fuehren. Was selbst NPC Crew nicht verlustfrei kann (z. B. Inhalt einer Tasche, echte Flicken, Reparatur-Zaehler): genau benennen; Taschen mit
    Inhalt -- Vorschlag: nur leer annehmen ("erst ausraeumen"), als Frage fuehren. NIE still einen Wert verlieren.
 1b. HOECHSTENS 1000 GEGENSTAENDE (wie die NPC-Crew-Figuren), zusaetzlich zur Gewichtsgrenze; Stapel zaehlen je Stueck. Die Liste an den Client
    seitenweise (Plan: Deckel 100 je Paket) -- 1000 Saetze duerfen kein MP-Paket sprengen (nachweisen).
 2. Ansehen ueberall (auch Fern-Taste), hineinlegen/herausnehmen nur daneben (3 Kacheln), nicht waehrend er im Auto mitfaehrt.
 3. Tod: alles faellt an der Stelle auf den Boden (auch die Packtaschen).
 4. Packtaschen: eigener Gegenstand "Bear Packs" / "Baeren-Packtaschen" (Plan: NPCCrew.BearPacks; Name vorher mit Kollisions-Werkzeug pruefen), selbst
    naehen (Schneidern 3: Jute oder Stoff, Lederstreifen, Seil, Faden; Nadel und Schere bleiben), anlegen ab halbstark, +50 Traglast, OHNE Bild am
    Baeren (Modell-Lauf spaeter). Icon: vorhandenes Vanilla-Icon einer Tasche per Verweis im Skript (nichts kopieren).
 5. Sandbox-Regler "Traglast %" (BearCarryPercent) 50-250, Vorgabe 100, Packtaschen immer +50 -> 14 Regler.
 6. Selbst fressen: ja -- ab 50 % Hunger aus dem eigenen Inventar, nur Baerenfutter, nie Verdorbenes, Lieblingsfutter zuerst.
 Ohne Frage (Plan): nicht langsamer bei Last, nur der Besitzer kommt ran, hineinlegen weckt nicht, Absturz-Schutz ueber die Spieler-Kopie.
Kevins ROTE LINIEN mit hoechster Prioritaet: KEIN Gegenstand verloren oder verdoppelt -- bei Geben, Nehmen, Tod, Wachsen, Aussehen-Wechsel, Unstuck,
Mitfahren, entladener Gegend, Besitzer offline, Speichern/Laden, ABSTURZ (Spiel per Task-Manager beendet), Mehrspieler; kein Kick (AntiCheat 2, Rolle
user: der Client schickt nie Gegenstaende, nur Bezuege; nur der Server ruft sendAdd.../sendRemove...); nichts haengt endlos. Zaehl-Invariante: Spieler +
Baer + Boden bleibt in jedem Attrappen-Fall gleich (je Gegenstand UND je Feld).

STAND: Test-Mod ${T} (Git main 9b4ccca = F1..F3) ist heute 1:1 nach ${S} kopiert (159 Dateien) = dein Staging. MODELL-DATEIEN (models_X, textures,
AnimSets) NIE im Staging aendern (paralleler Modell-Lauf baer-liegen). Fenster Variante B steht seit F3 (Knopf Inventory grau an seinem Platz).
Texte in ACHT Sprachen (EN, PTBR, RU, KO, ES, CN, FR, DE; ${B}/NAEHTE.md, langcheck ${NC}/_docs/tools/langcheck.py, Werkzeuge ${W}/../baer_de/werkzeug/,
Vorbild F3 ${W}/f3/werkzeug_texte/). Uebernahme-Skript ${B}/tools/baer_uebernahme.py (heute 0 Fehler, 2 Warnungen) und ${B}/NAEHTE.md nachziehen.
UI-BILDER nur aus dem ECHTEN Code (globale CLAUDE.md; Vorbild ${W}/f3/ und ${W}/f1_entwurf/zeichne_gebaut.py): Fenster mit Load-Zeile, Inventar-Fenster
(leer, halb voll, voll/1000, Ablehnung), 1080p/4K, EN/DE.
ORTE: schreiben nur in ${S}/, ${F}/, ${W}/attrappe/f4_*/ und -- nur KERN/Nachbesserung -- ${B}/tools/baer_uebernahme.py, ${B}/NAEHTE.md. Nie in die
Test-Mod, NPC Crew, Vanilla, Bandits oder andere _arbeit-Ordner schreiben; kein git, kein Download, kein Spielstart. Suchorte nur: ${W}, ${B}, ${T}
(lesen), Vanilla ${VAN} (lesen; Jar daneben, Klassen nach ${F}/jar/ ziehen, javap C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin/javap.exe -c -p),
Bandits (lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs (lesen). Nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk.
EISERNE REGEL: jeder Engine-Aufruf mit Fundstelle als echter Aufruf in Vanilla-Lua oder Bandits mit GLEICHEN Argumenttypen, im Kommentar; Jar-only nur
die durch Antwort 1 gedeckten (JAR_LISTE.md); kein pcall als Tarnkappe. SP UND MP: SP-Test "not isServer() and not isClient()". Namen
BanditsNPCBear*/UI_BN_Bear_*/BanditsNPC.Bear*/NPCCrew.BearPacks; jeden neuen Namen mit ${W}/aussehen/werkzeug/kollision.py pruefen. Testbefehle nur in
NCBearBench*.lua. Vier Lua-Pruefer auf jeder geaenderten Datei: python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py (aktiv UND insgesamt
< 180), luacheck_pz.py. Attrappen ${W}/attrappe/ (lua5.1 C:/Users/Kevin/Tools/lua51/lua5.1.exe; Kahlua ist kein echtes 5.1, kein next) -- die F3-Attrappen
bleiben gruen. Zeilenenden je Datei wie vorher; keine Backslash-Escapes in Python-Heredocs; Shell-Befehle unter 6000 Zeichen (laengere scheiterten im
F3-Lauf mit "unexpected EOF"). Befehle ueber 2 Minuten im Hintergrund.`

const FIND = { type: 'object', properties: { zusammenfassung: { type: 'string' }, findings: { type: 'array', items: { type: 'object',
  properties: { id: { type: 'string' }, schwere: { type: 'string', enum: ['blocker', 'major', 'minor'] }, datei: { type: 'string' }, zeile: { type: 'string' },
    behauptung: { type: 'string' }, beleg: { type: 'string' }, vorschlag: { type: 'string' } },
  required: ['id', 'schwere', 'datei', 'behauptung', 'beleg', 'vorschlag'] } } }, required: ['zusammenfassung', 'findings'] }
const VERDICT = { type: 'object', properties: { bereit_fuer_sp_test: { type: 'boolean' }, zusammenfassung: { type: 'string' },
  offene_blocker: { type: 'array', items: { type: 'string' } }, restbefunde: { type: 'array', items: { type: 'string' } },
  fragen_an_kevin: { type: 'array', items: { type: 'string' } }, jar_ausnahmen: { type: 'array', items: { type: 'string' } },
  staging_dateien: { type: 'integer' } },
  required: ['bereit_fuer_sp_test', 'zusammenfassung', 'offene_blocker', 'restbefunde', 'fragen_an_kevin', 'jar_ausnahmen', 'staging_dateien'] }

phase('Bau')
const [gate, kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEF-TORE UND JAR-LISTE (du baust keinen Mod-Code). (1) Pruef-Tore G1-G4 aus ${F}/PLAN_F4.md im Jar klaeren (u. a. G1: kann ein Client
die Spieler-ModData am Server setzen -> traegt die Spieler-Kopie im MP?), Ergebnis ${F}/GATES.md mit Offsets und klarem Ja/Nein je Tor. (2) Fuer
Antwort 1 ("alles", Jar-Ausnahmen wie NPC Crew): lies NPC Crews Manifest-/Wiederherstellungs-Code (nur lesen) und schreibe ${F}/JAR_LISTE.md: je
Gegenstands-Art (Essen, Kleidung, Tasche/Behaelter, Schusswaffe + Magazin/Anbauteile, Nahkampf/Klinge, Fluessigkeits-Behaelter, Zettel/Buch/Karte,
Elektronik, Schluessel, Werkzeug, Material, sonstige) die Felder, die NPC Crew liest/setzt, die Methode, Vanilla-Fundstelle ODER Jar-Offset + NPC-Crew-
Zeile mit Kevins Wort, und was NICHT verlustfrei geht. Schreibe FRUEH einen ersten Stand (der KERN-Bauer liest ihn nach etwa 15 Minuten) und haenge
Nachtraege an. Rueckgabe: Kurzfassung (hoechstens 25 Zeilen).`, { label: 'bau:tore+jar', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN laut ${F}/PLAN_F4.md Abschnitt 19 (Spalte KERN) -- mit Kevins Antworten (ALLES tragen, 1000-Deckel, Regler 50-250, Tod -> Boden,
selbst fressen). Client-Dateien, Zeitaktionen und Texte gehoeren dem OBERFLAECHE-Bauer (nur lesen). Der Agent PRUEF-TORE schreibt parallel
${F}/GATES.md und ${F}/JAR_LISTE.md -- lies sie, sobald sie da sind (ab etwa 15 Minuten), und baue die Satz-Felder je Art danach; bis dahin den Teil
ohne Jar-Felder. ZUERST den Abschnitt KERN in ${F}/schnittstelle.md anlegen (Plan 19 + Aenderungen durch Kevins Antworten: Ablehnungs-Gruende nur noch
fuer "nicht verlustfrei"/"zu schwer"/"1000 voll"/"Tasche nicht leer"), spaetere Abweichungen sofort anhaengen, vor Abschluss den Abschnitt OBERFLAECHE
lesen. Pflicht: Feldpruefer-Skript ${F}/werkzeug_kern/feldpruefer.py (jedes Feld hat Lese- UND Schreib-Fundstelle), Attrappen ${W}/attrappe/f4_kern/ mit
Zaehl-Invariante je Gegenstand und Feld fuer: Geben/Nehmen jeder Art, 1000-Deckel, Gewicht, Tod (Boden), Wachsen/Aussehen/Unstuck/Mitfahren, Besitzer
offline, Speichern/Laden, ABSTURZ zwischen Geben und Speichern (Spieler-Kopie), MP-Bitte mit falschen Daten, selbst fressen. Trockenlauf
(--staging ${S}). Bericht ${F}/BAU_KERN.md ("Fragen fuer Kevin", Verweis auf JAR_LISTE.md). Rueckgabe: Kurzfassung (hoechstens 30 Zeilen).`,
    { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE laut ${F}/PLAN_F4.md Abschnitt 19 (Spalte OBERFLAECHE: Zeitaktionen Put/Take, client/BanditsNPCBearInvClient.lua,
ISUI-Inventar-Fenster, WinData/Window/Menu/Client/Pose, Bench NCBearBenchInv.lua, Texte EN + DE inkl. ItemName.json/Recipes.json fuer die Packtaschen).
ZUERST ${F}/schnittstelle.md lesen (der KERN-Bauer legt seinen Abschnitt frueh an; sonst nach Plan 19 + Kevins Antworten bauen und nach 10 Minuten
erneut lesen), eigene Abweichungen im Abschnitt OBERFLAECHE anhaengen, vor Abschluss den Abschnitt KERN lesen. Inventar-Fenster: zwei Spalten (du |
Baer), "Load x / y" und "n / 1000", Seiten oder Rollen fuer 1000 Gegenstaende, Geben/Nehmen (auch ganze Stapel), grauer Grund wenn zu weit/im Auto/voll;
ansehen auch aus der Ferne. Schreibe dem Texte-Bauer ${F}/texte_auftrag.md. Bilder NUR aus dem echten Code: ${F}/bilder/KEVIN_inventar_1080.png,
_4k.png, _DE_1080.png und KEVIN_fenster_f4_1080.png (Load-Zeile, Knopf scharf). Vier Lua-Pruefer, Texte-Pruefer EN/DE, Attrappen ${W}/attrappe/f4_ober/.
Bericht ${F}/BAU_OBER.md. Rueckgabe: Kurzfassung (hoechstens 30 Zeilen).`, { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { gate, kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const texte = await agent(`${CTX}

DEINE ROLLE: TEXTE-BAUER. KERN und OBERFLAECHE sind fertig (${F}/BAU_KERN.md, ${F}/BAU_OBER.md, ${F}/schnittstelle.md, ${F}/texte_auftrag.md -- ganz
lesen). Du schreibst NUR in ${S}/42/media/lua/shared/Translate/<PTBR|RU|KO|ES|CN|FR>/ (UI.json, Sandbox.json, ItemName.json, Recipes.json bzw. die
Dateien, die EN/DE neu bekommen haben): jeden neuen/geaenderten Schluessel aus EN/DE in die sechs Sprachen (gleiche Schluessel, gleiche Platzhalter;
CN nur Zeichen, die Vanilla-CN selbst benutzt; Dateiformat beibehalten -- vorher pruefen). Fehlt in EN/DE etwas, das der Code benutzt: in
${F}/schnittstelle.md Abschnitt TEXTE melden und in allen ACHT Sprachen ergaenzen. Pruefer: langcheck ueber alle acht + die Werkzeuge aus F3
(${W}/f3/werkzeug_texte/). Bericht ${F}/BAU_TEXTE.md. Rueckgabe: Kurzfassung (hoechstens 15 Zeilen).`, { label: 'bau:texte', phase: 'Bau' })

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER CODE. Gebaut ist in ${S} (Berichte ${F}/BAU_KERN.md, BAU_OBER.md, BAU_TEXTE.md, GATES.md, JAR_LISTE.md, schnittstelle.md). Du
aenderst nichts ausser deinem Bericht und eigenen Attrappen unter ${W}/attrappe/f4_pruef/. Glaube keinem Bericht. Pruefe: (1) Kevins Antworten 1-6
Punkt fuer Punkt im Code; (2) jede Jar-Methode: ist sie WIRKLICH in NPC Crew mit Kevins Wort benutzt (Zeile selbst oeffnen) -- sonst blocker; jeder
belegte Aufruf mit gleichen Argumenttypen; (3) VERLUST/VERDOPPLUNG: eigene Attrappen-Faelle fuer die gefaehrlichsten Wege (Geben + Absturz vor dem
Speichern; Nehmen + Absturz; Tod mitten im Geben; 1000-Grenze; zwei Clients nehmen denselben Satz; Aussehen-Wechsel mit vollem Inventar; Spieler-Kopie
aelter als Register) und zaehle je Gegenstand UND je Feld (Haltbarkeit, Kochzustand, Munition im Magazin, Fluessigkeit, Name, Farbe ...); (4) Kick:
schickt ein Client einen Gegenstand oder eine Zahl, die der Server glaubt?; (5) vier Lua-Pruefer, alle Attrappen (auch F3), Trockenlauf und --probe
selbst (Probe nur unter ${F}/probe/). Bericht ${F}/PRUEF_CODE.md. Rueckgabe strukturiert (id C1...).`,
    { label: 'pruef:code', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER BILD UND OBERFLAECHE. Du aenderst nichts ausser deinem Bericht und eigenen Pruefbildern unter ${F}/pruef_bild/. Zeichne
Baerenfenster und Inventar-Fenster SELBST neu aus dem echten Staging-Code (Mitschrift-Kette) in 1080p, 4K, EN und DE, Zustaende: leer, halb voll,
Gewicht voll, 1000 Stueck, Ablehnung mit Grund, aus der Ferne (nur ansehen), im Auto, Junges (10 kg), ausgewachsen mit Packtaschen. Pruefe: nichts
ueberlappt oder laeuft aus dem Fenster (auch DE/RU/FR-Laengen), Gewicht/Anzahl lesbar, Rollen/Seiten bei 1000, Knoepfe klar, passt zu Fenster B
(${W}/f3/bilder/KEVIN_fenster_f3_1080.png). Bericht ${F}/PRUEF_BILD.md mit Bildern. Rueckgabe strukturiert (id P1...).`,
    { label: 'pruef:bild', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log(befunde.length + ' Befunde (' + befunde.filter(f => f.schwere === 'blocker').length + ' blocker, ' + befunde.filter(f => f.schwere === 'major').length + ' major)')

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG (darf im ganzen Staging ${S}, in ${F}, ${W}/attrappe/f4_*, ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md schreiben).
Befunde: ${JSON.stringify(befunde, null, 1)}
Jeden selbst am Code nachpruefen, falsche mit Beleg ablehnen, blocker/major beheben, minor wenn klein und sicher; Texte immer in 8 Sprachen. Danach
alles neu: vier Lua-Pruefer, alle Attrappen, langcheck, Trockenlauf/--probe, Bilder neu aus dem Code. Schreibe ${F}/staging_dateien_f4.txt (Form wie
${W}/f3/staging_dateien_f3.txt: Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen ${T}; Modell-Dateien "NICHT KOPIEREN"; Skript nach dem Vorbild
${W}/f3/werkzeug_nach/staging_liste_f3.py als ${F}/werkzeug_nach/staging_liste_f4.py), den mod.info-Vorschlag ${F}/mod_info_vorschlag_f4.txt (F4-Absatz
anhaengen wie bei F3) und den Entwurf der Testanleitung ${F}/anleitung_entwurf.md (Deutsch, kurz, Schritt fuer Schritt mit Bench-Befehlen; darin T7:
etwas hineinlegen, Spiel per Task-Manager beenden, laden -- genau einmal da). Bericht ${F}/NACHBESSERUNG.md. Rueckgabe: je Befund-ID eine Zeile.`,
  { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut und glaubst keinem Bericht. Befunde: ${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere,
datei: f.datei, behauptung: f.behauptung })), null, 1)}. Nachbesserung: ${F}/NACHBESSERUNG.md. Lies ${F}/GATES.md zuerst. Je Befund geschlossen? Etwas
kaputt gemacht? Kevins Antworten 1-6 am Code. Schwerpunkt VERLUST/VERDOPPLUNG und KICK: drei eigene Stichproben mit Zaehl-Invariante (Absturz nach
Geben; Tod mit vollem Inventar -> Boden; Aussehen-Wechsel mit Packtaschen). Jede Jar-Methode gegen NPC Crews Zeile pruefen. Vier Lua-Pruefer, alle
Attrappen, langcheck, Trockenlauf/--probe selbst; staging_dateien_f4.txt gegen die Platte nachzaehlen (keine Modell-Datei geaendert). Ein Fensterbild
selbst aus dem Code zeichnen und ansehen. Urteil: bereit fuer Kevins Einzelspieler-Test? Bericht ${F}/GEGEN.md; Testanleitung ${F}/anleitung_entwurf.md
pruefen/berichtigen. jar_ausnahmen = jede nur im Jar belegte Methode im Staging (Datei:Zeile + NPC-Crew-Beleg), fragen_an_kevin = alle offenen
Kleinfragen kurz auf Deutsch.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { gate, kern, ober, texte, befunde: befunde.length, fix, gegen }
