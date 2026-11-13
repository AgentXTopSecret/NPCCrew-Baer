export const meta = {
  name: 'baer-f3',
  description: 'Baer F3: Hunger, Durst, Muedigkeit, Vertrauen, Schlafen (ohne neue Clips), Fenster Variante B, z Z z -- Bau nach PLAN_F3.md mit Kevins Antworten vom 13.11. (7 Agenten; nichts in die Test-Mod)',
  phases: [
    { title: 'Bau', detail: 'KERN und OBERFLAECHE parallel, danach Texte in 6 Sprachen' },
    { title: 'Pruefung', detail: 'Code und Bild' },
    { title: 'Nachbesserung' },
    { title: 'Gegenpruefung' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const F = W + '/f3'
const S = W + '/mod_f3'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-f3" fuer Kevins Mod NPC Crew (Project Zomboid 42.22; Bandits ${BAN}/42.22 und ${BAN}/common). Kevin
programmiert nicht, er spielt und testet. Berichte auf Deutsch, "statisch geprueft, nicht gespielt", jede Behauptung mit Fundstelle (Datei:Zeile).
Keine Fragen an Kevin waehrend des Laufs: Kleinfragen mit dem empfohlenen Weg bauen und als "Fragen fuer Kevin" im Bericht fuehren.

AUFTRAG: F3 = Beduerfnisse (Hunger, Durst, Muedigkeit), Vertrauen, Fuettern/Traenken, Schlafen (noch OHNE neue Clips: Ersatzbild Sitzen,
B.CFG.sleepClips = false), z Z z, Kopf-Balken, Baerenfenster Variante B, EIN neuer Sandbox-Regler. DER PLAN IST FERTIG UND GILT:
${F}/PLAN_F3.md (691 Zeilen, GANZ lesen; Forschung daneben ${F}/FORSCHUNG_F3.md). Fenster-Vorlage ${W}/ui_entwurf/proto/ (nur der "wide"-Zweig).
Fruehere Forschung zum Schlaf der NPC-Crew-Figuren: ${W}/../baer_schlaf/forschung_npcschlaf.md.

KEVINS ANTWORTEN VOM 13.11.2026 GEHEN VOR DEM PLAN (woertlich in ${F}/KEVIN_ANTWORTEN.md, ZUERST lesen; gleich in ${B}/begleiter/ENTSCHEIDUNGEN.md unten):
 1. Schlafhaltung: beide (Sphinx + eingerollt) -- betrifft erst den Modell-Lauf; hier nur die 8 Clip-Schluessel aus Plan 14.3 vorsehen.
 2. Vom Zombie geweckt: schlaftrunken wegrennen nur 5 SEKUNDEN (wokeFleeMs 5000, nicht 20 s), dann kaempfen wie immer; sehr muede -> rennt weiter weg.
 3. Muedigkeit steigt AUCH beim Folgen. Schwellen GEAENDERT: "zu muede zum Kaempfen" erst ab 90 % (Plan: 70) -- und er SAGT es (Meldung an den
    Besitzer + Zeile/Grund im Fenster); von selbst einschlafen erst bei 100 % (Plan: 90).
 4. Vertrauen: Balken + Wort; viel Vertrauen -> Hunger/Durst/Muedigkeit bis 20 % langsamer; NEU: wenig Vertrauen -> Beduerfnisse steigen im
    Gegenzug SCHNELLER (spiegelbildlich, Vorschlag bis +20 %, neutral bei 50); NEU: bei SEHR wenig Vertrauen WEIGERT er sich zu KAEMPFEN, und das
    steht sichtbar da (Fenster + Meldung). Alle anderen Befehle gehorcht er weiter. Schwelle vorschlagen (z. B. unter 15), als Stellwert in B.CFG,
    in "Fragen fuer Kevin" nennen. Ein frisch gezaehmter Baer (Start 50) darf davon nie betroffen sein.
 5. z Z z: Hellblau, UEBER DEM KOPF. Kevin hat Ja gesagt, dass der Code das Spiel fragt, wohin der Baer schaut. Ist der Aufruf in Vanilla-Lua/
    Bandits belegt: Fundstelle nennen. Ist er NUR im Jar belegt: genau dieser eine Aufruf ist durch Kevins Wort gedeckt -- Klasse.Methode + Offset
    im Kommentar UND im Bericht unter "Jar-Ausnahme (Kevins Wort 13.11.)" nennen. Buchstabe wechselt weich z -> Z -> z (kein drawTextZoomed).
 6a. Hunger/Durst ganz leer: Leben sinkt bis 1 % (Plan: 10 %), er stirbt NIE daran, geht nie deswegen zu Boden.
 6b. EIN neuer Sandbox-Regler BearNeedsPercent ("Beduerfnis-Tempo %", 0 = aus) -> 13 Regler.
 6c. KEINE UHRZEITEN: kein Nachtfenster 22-7, kein fester Mittagsschlaf des Jungen. Schlaf nur nach Muedigkeit "wie bei den NPC-Crew-Figuren": bei
     100 % schlaeft er von selbst ein und schlaeft, bis er bei 0 % ist; mittendrin weckt ihn "Folgen" (bzw. jeder Befehl, 6e) -- dann bleibt die
     Muedigkeit, wo sie ist. Den Abschnitt 6 des Plans (und 2.3, Kurzfassung Nr. 3 und 15) danach UMBAUEN: Uhrzeit-Zweige raus. Steig- und Sink-
     Tempo so waehlen, dass der Rhythmus zu den NPC-Crew-Figuren passt (dort NUR LESEN: ${NC}/42/media/lua, z. B. shared/BanditsNPCRoutine.lua und
     die Muedigkeits-Stellen; Fundstelle + deine Zahlen in den Bericht und in "Fragen fuer Kevin": wie viele Spielstunden wach bis 100 %, wie
     viele Stunden Schlaf bis 0 %, je Groesse).
 6d. Ausnahme vom 100-%-Schlaf: schlaeft der Besitzer und der Baer folgt ihm, legt er sich neben ihn und schlaeft mit (Plan 6, Zweig "Besitzer schlaeft").
 6e. Kein Schlaf-Knopf im Fenster. Jeder Befehl weckt ihn, Streicheln laesst ihn liegen, Fuettern/Traenken wecken kurz.
 6f. Kein Schlafton, kein Baerenbett, kein selbst Trinken am Wasser (alles spaeter).
 6g. Balken mit Prozent, das Wort (z. B. "Hungry") im Tooltip.
 7. HERZ (Kevin 13.11., nach den sechs Fragen): bei MAXIMALEM Vertrauen erscheint ein Herz UEBER dem Namensschild des Baeren. Es haengt am
    Namensschild: nur sichtbar, wenn die Namensanzeige des Baeren an ist -- KEIN eigener Schalter. "Maximal" = oberste Vertrauens-Stufe
    (Stellwert B.CFG, Vorschlag 100 %; in "Fragen fuer Kevin" nennen). Das Herz ist ein EIGENES, selbst gezeichnetes Bild (nichts kopieren,
    kein Download; z. B. mit Python/PIL in hoher Aufloesung gezeichnet und sauber verkleinert: weiche Form, Verlauf, Glanzlicht, dunkler
    Rand, auf hellem und dunklem Hintergrund gut lesbar, scharf in 1080p und 4K). Neue Bilddatei unter media/ui/ mit NPC-Crew-Namen
    (BanditsNPCBear*, vorher Kollision pruefen), ins Uebernahme-Skript und NAEHTE aufnehmen. Zeichnen nur mit belegten Aufrufen (wie das
    Namensschild/Hud heute zeichnet), nichts Teures je Bild.
Wo eine Antwort dem Plan widerspricht, gilt die Antwort; Plan 22.2 nennt je Frage die Stellwerte. Jede solche Abweichung in ${F}/schnittstelle.md
(Abschnitt deiner Rolle) festhalten, damit der andere Bauer sie sieht (z. B. neue Sicht-Felder/Meldungs-Schluessel fuer "zu muede", "kein
Vertrauen").

STAND: Test-Mod ${T} (Git main fda41e8 = F1 + F1b + F2 + DE + Aussehen-Knopf + Sandbox 12) ist heute 1:1 nach ${S} kopiert (145 Dateien, byte-gleich)
= dein Staging (Bauort; darin 42/, common/, mod.info). MODELL-DATEIEN (models_X, textures, AnimSets-XML fuer neue Clips) NIE im Staging aendern:
parallel laeuft der Modell-Lauf baer-liegen, spaeter Maul und Schlafpose (F3b bringt Clips + Knoten).
Texte in ACHT Sprachen (EN, PTBR, RU, KO, ES, CN, FR, DE; DE-Regeln ${B}/NAEHTE.md, NPC Crew CLAUDE.md "ACHT Sprachen", Pruefer
${NC}/_docs/tools/langcheck.py, Werkzeuge ${W}/../baer_de/werkzeug/; Begriffe: Faehigkeiten, Leben, Herholen, stark). Uebernahme-Skript
${B}/tools/baer_uebernahme.py (Trockenlauf heute 0 Fehler, 2 Warnungen) und ${B}/NAEHTE.md nachziehen (Bench nie nach NPC Crew).
UI-BILDER (Kevins feste Regel, globale CLAUDE.md "UI-Bilder fuer Kevin: aus dem echten Code"): jedes Fenster-/z Z z-Bild entsteht aus dem ECHTEN
Lua-Code per Zeichen-Mitschrift unter Lua 5.1 + echte Spielschriften ueber einem echten Spielbild (Vorbild ${W}/attrappe/f1_ober/zeichne_dump.lua,
${W}/f1_entwurf/zeichne_gebaut.py, ${W}/ui_entwurf/werkzeug/zeichne_entwurf.py), 1080p und 4K, EN und DE.
ORTE: schreiben nur in ${S}/, ${F}/ (Berichte, schnittstelle.md, Bilder), ${W}/attrappe/f3_*/ und -- nur KERN/Nachbesserung -- ${B}/tools/baer_uebernahme.py,
${B}/NAEHTE.md. Nie in die Test-Mod, NPC Crew, Vanilla, Bandits oder andere _arbeit-Ordner schreiben; kein git, kein Download, kein Spielstart.
Suchorte nur: ${W}, ${W}/../baer_schlaf, ${W}/../baer_de, ${B}, ${T} (lesen), Vanilla ${VAN} (lesen, Jar daneben), Bandits (lesen), NPC Crew
${NC}/42/media/lua und ${NC}/_docs (lesen). Nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk.
EISERNE REGEL: jeder Engine-Aufruf mit Fundstelle als echter Aufruf in Vanilla-Lua oder Bandits mit GLEICHEN Argumenttypen, im Kommentar (Liste Plan 15);
kein pcall als Tarnkappe; Jar-only nur die EINE Ausnahme aus Antwort 5. SP UND MP: SP-Test "not isServer() and not isClient()"; was der Server wissen
muss, kommt nie aus Client-Glauben. Kevins rote Linien: Baer nie verloren/verdoppelt, kein Gegenstand verloren/verdoppelt (Wasser/Futter!), kein Kick,
nichts haengt endlos, keine NPC-Crew-Figur gestoert. Namen BanditsNPCBear*/UI_BN_Bear_*/BanditsNPC.Bear*; vor jedem neuen Namen mit
${W}/aussehen/werkzeug/kollision.py pruefen. Testbefehle nur in NCBearBench*.lua. Lua-Pruefer auf jeder geaenderten Datei: python
${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py (aktiv UND insgesamt < 180), luacheck_pz.py. Attrappen ${W}/attrappe/ (lua5.1
C:/Users/Kevin/Tools/lua51/lua5.1.exe; Kahlua ist kein echtes 5.1, kein next) -- alle bestehenden bleiben gruen. Zeilenenden je Datei wie vorher;
keine Backslash-Escapes in Python-Heredocs. Befehle ueber 2 Minuten im Hintergrund.`

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
const [kern, ober] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: BAUER KERN laut ${F}/PLAN_F3.md Abschnitt 19 (Spalte KERN: shared/server, sandbox-options.txt, ${B}/tools/baer_uebernahme.py,
${B}/NAEHTE.md) -- mit Kevins Antworten. Client-Dateien, Zeitaktionen und Texte gehoeren dem anderen Bauer (nur lesen). ZUERST den Abschnitt KERN in
${F}/schnittstelle.md anlegen (Sicht-Felder, Bitten, Meldungs-Schluessel, B.CFG-Namen, Schwellen NACH Kevins Antworten: tirVery 90, tirCollapse 100,
wokeFleeMs 5000, Lebens-Untergrenze 1 %, Vertrauens-Schwellen, KEINE Uhrzeit-Felder) -- der andere Bauer liest ihn frueh; spaetere Abweichungen sofort
ANHAENGEN, vor Abschluss den Abschnitt OBERFLAECHE lesen. Vier Lua-Pruefer, alle Attrappen gruen, neue Faelle unter ${W}/attrappe/f3_kern/
(u. a.: 100 % -> schlaeft bis 0 %; Folgen weckt mittendrin; 90 % kaempft nicht + Meldung; wenig Vertrauen -> schnellere Beduerfnisse; sehr wenig ->
kaempft nicht + Meldung, Start 50 unberuehrt; maximales Vertrauen -> Sicht meldet es fuer das Herz (Antwort 7); leer -> Leben nie unter 1 %; BearNeedsPercent 0 = alles aus; Koerper-Tausch/Aussehen-Wechsel behaelt
die vier Werte; Wasser wird genau einmal genommen), Trockenlauf (--staging ${S}). Bericht ${F}/BAU_KERN.md (mit "Fragen fuer Kevin" und den
Rhythmus-Zahlen aus 6c). Rueckgabe: Kurzfassung (hoechstens 30 Zeilen).`, { label: 'bau:kern', phase: 'Bau' }),
  () => agent(`${CTX}

DEINE ROLLE: BAUER OBERFLAECHE laut ${F}/PLAN_F3.md Abschnitt 19 (Spalte OBERFLAECHE: client/ inkl. ISUI, Zeitaktionen, Bench NCBearBenchNeeds.lua,
Texte EN und DE in UI.json/Sandbox.json + U.EN-Block) -- mit Kevins Antworten (Fenster B, z Z z hellblau ueber dem Kopf, Prozent im Balken/Wort im
Tooltip, KEIN Schlaf-Knopf, sichtbare Gruende "zu muede zum Kaempfen" und "weigert sich zu kaempfen (kein Vertrauen)", keine Uhrzeit-Texte).
shared/server gehoeren dem anderen Bauer (nur lesen). ZUERST ${F}/schnittstelle.md lesen (der KERN-Bauer legt seinen Abschnitt frueh an; steht noch
nichts da, nach Plan 19 + Kevins Antworten bauen und nach 10 Minuten erneut lesen), eigene Abweichungen im Abschnitt OBERFLAECHE ANHAENGEN, vor
Abschluss den Abschnitt KERN lesen. Die sechs weiteren Sprachen macht danach ein eigener Texte-Bauer: schreibe ihm ${F}/texte_auftrag.md (alle neuen/
geaenderten Schluessel mit EN, DE, Platzhaltern und Zusammenhang). Bilder NUR aus dem echten Code (Regel oben): ${F}/bilder/KEVIN_fenster_f3_1080.png,
_4k.png, _DE_1080.png und ${F}/bilder/KEVIN_zzz.png (Hellblau ueber dem Kopf, auf echtem Spielbild). HERZ (Antwort 7, deine Aufgabe): mindestens vier eigene Herz-Entwuerfe zeichnen (Skript ${F}/herz/herz_zeichne.py),
Blatt ${F}/bilder/KEVIN_herz.png (jeder Entwurf gross, in Spielgroesse ueber einem Namensschild auf echtem Spielbild, hell und dunkel), den huebschesten
als Vorgabe einbauen (die anderen als Dateien unter ${F}/herz/ liegen lassen), im Hud ueber dem Namen zeichnen, wenn die Sicht "maximales
Vertrauen" meldet und die Namensanzeige an ist; Bild aus dem echten Code: ${F}/bilder/KEVIN_herz_im_spiel.png. Vier Lua-Pruefer, Texte-Pruefer fuer EN/DE,
Attrappen gruen, neue Faelle unter ${W}/attrappe/f3_ober/. Bericht ${F}/BAU_OBER.md. Rueckgabe: Kurzfassung (hoechstens 30 Zeilen).`,
    { label: 'bau:oberflaeche', phase: 'Bau' }),
])
if (!kern || !ober) { return { kern, ober, abbruch: 'Bauer ohne Ergebnis' } }

const texte = await agent(`${CTX}

DEINE ROLLE: TEXTE-BAUER. KERN und OBERFLAECHE sind fertig (${F}/BAU_KERN.md, ${F}/BAU_OBER.md, ${F}/schnittstelle.md, ${F}/texte_auftrag.md -- ganz
lesen). Du schreibst NUR in ${S}/42/media/lua/shared/Translate/<PTBR|RU|KO|ES|CN|FR>/UI.json und Sandbox.json: jeden neuen/geaenderten Schluessel aus
EN/DE in die sechs Sprachen (gleiche Schluessel, gleiche Platzhalter/Prozent wie EN; CN nur Zeichen, die Vanilla-CN selbst benutzt; Round-Trip
json.dumps(data, indent=4, ensure_ascii=False) + "\\n" bzw. das Format der Datei beibehalten -- vorher pruefen). Fehlt in EN/DE etwas, das der Code
benutzt (grep getText/UI_BN_Bear_ im Staging gegen die JSON): in ${F}/schnittstelle.md Abschnitt TEXTE melden und in allen ACHT Sprachen ergaenzen.
Pruefer: ${NC}/_docs/tools/langcheck.py und die Werkzeuge unter ${W}/../baer_de/werkzeug/ ueber alle acht Sprachen. Bericht ${F}/BAU_TEXTE.md.
Rueckgabe: Kurzfassung (hoechstens 15 Zeilen).`, { label: 'bau:texte', phase: 'Bau' })

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER CODE. Gebaut ist in ${S} (Berichte ${F}/BAU_KERN.md, BAU_OBER.md, BAU_TEXTE.md, schnittstelle.md). Du aenderst nichts ausser deinem
Bericht und eigenen Attrappen unter ${W}/attrappe/f3_pruef/. Glaube keinem Bericht. Pruefe: (1) Kevins Antworten 1-7 Punkt fuer Punkt im Code (90/100,
5 s, 1 %, keine Uhrzeiten, Vertrauen beide Richtungen + Kampf-Weigerung sichtbar, kein Schlaf-Knopf, Prozent/Tooltip, Herz nur bei maximalem Vertrauen UND Namensanzeige an, neue Bilddatei im Uebernahme-Skript); (2) jeden neuen Engine-Aufruf:
Fundstelle selbst oeffnen, gleiche Argumenttypen; Jar-Ausnahme nur die eine aus Antwort 5; (3) Zusammenpassen ueber die Grenze: jede B.*-Benutzung
definiert, jede Bitte mit Empfaenger, jedes Sicht-Feld gesetzt und gelesen, jeder Textschluessel in 8 Sprachen; (4) Logik und rote Linien: Koerper-
Tausch/Aussehen/Wachsen behalten die Werte, Speichern/Laden mitten im Schlaf, Kampf geht vor, Besitzer offline, MP-Bitte mit falschen Daten, Wasser
nie doppelt genommen oder verloren, nichts haengt endlos, F1/F1b/F2/Aussehen unveraendert bei BearNeedsPercent 0; (5) vier Lua-Pruefer, alle
Attrappen, Trockenlauf und --probe selbst (Probe nur unter ${F}/probe/). Bericht ${F}/PRUEF_CODE.md. Rueckgabe strukturiert (id C1...).`,
    { label: 'pruef:code', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER BILD UND OBERFLAECHE. Du aenderst nichts ausser deinem Bericht und eigenen Pruefbildern unter ${F}/pruef_bild/. Zeichne das
Fenster SELBST neu aus dem echten Staging-Code (Mitschrift-Kette, Regel oben) in 1080p, 4K, EN und DE, mit einem jungen und einem ausgewachsenen
Baeren, in den Zustaenden: normal, hungrig/durstig, "zu muede zum Kaempfen" (>= 90 %), schlafend, "weigert sich zu kaempfen (kein Vertrauen)",
BearNeedsPercent 0. Vergleiche mit ${W}/ui_entwurf/KEVIN_fenster_entwurf_B_klar_1080.png (Variante B: drei Karten Condition | Needs | Skills, Befehle
in 5 Spalten, graue Platzhalter Fish/Inventory/Nose alerts mit Grund, keine Loecher). Pruefe: nichts ueberlappt oder laeuft aus dem Fenster (auch DE
und RU-Laengen), Tooltips mit Wort, Prozent im Balken, kein Schlaf-Knopf, z Z z hellblau ueber dem Kopf (Bild aus dem echten Code), das HERZ (Antwort 7: selbst gezeichnet, huebsch, scharf in 1080p/4K, sitzt mittig ueber dem Namen, verschwindet mit der Namensanzeige und unter maximalem Vertrauen; Blatt KEVIN_herz.png ansehen und den besten Entwurf nennen), Kopf-Balken und
Optionen-Seite, Schild-Zeilen. Bericht ${F}/PRUEF_BILD.md mit Bildern. Rueckgabe strukturiert (id P1...).`,
    { label: 'pruef:bild', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log(befunde.length + ' Befunde (' + befunde.filter(f => f.schwere === 'blocker').length + ' blocker, ' + befunde.filter(f => f.schwere === 'major').length + ' major)')

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG (darf im ganzen Staging ${S}, in ${F}, ${W}/attrappe/f3_*, ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md schreiben).
Befunde: ${JSON.stringify(befunde, null, 1)}
Jeden selbst am Code nachpruefen, falsche mit Beleg ablehnen, blocker/major beheben, minor wenn klein und sicher; Texte immer in 8 Sprachen. Danach alles
neu: vier Lua-Pruefer, alle Attrappen, langcheck, Trockenlauf/--probe, Bilder neu aus dem Code (${F}/bilder/KEVIN_fenster_f3_*.png, KEVIN_zzz.png).
Schreibe ${F}/staging_dateien_f3.txt (Pfad | MD5 | Bytes | neu/ueberschreibt/gleich gegen ${T}; Modell-Dateien als "NICHT KOPIEREN"), den
mod.info-Vorschlag ${F}/mod_info_vorschlag_f3.txt und den Entwurf der Testanleitung ${F}/anleitung_entwurf.md (Deutsch, kurz, Schritt fuer Schritt mit
Bench-Befehlen; Spiel mit -debug neu starten). Bericht ${F}/NACHBESSERUNG.md. Rueckgabe: je Befund-ID eine Zeile.`,
  { label: 'nachbesserung', phase: 'Nachbesserung' })

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts gebaut und glaubst keinem Bericht. Befunde: ${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere,
datei: f.datei, behauptung: f.behauptung })), null, 1)}. Nachbesserung: ${F}/NACHBESSERUNG.md. Je Befund geschlossen? Etwas kaputt gemacht? Kevins
Antworten 1-7 noch einmal Punkt fuer Punkt am Code. Vier Lua-Pruefer, alle Attrappen, langcheck, Trockenlauf/--probe selbst laufen lassen,
staging_dateien_f3.txt gegen die Platte nachzaehlen (keine Modell-Datei geaendert), drei eigene Stichproben (100 % -> Schlaf bis 0 % und Wecken durch
Folgen; Wasser genau einmal genommen im MP-Weg; Aussehen-Wechsel behaelt Hunger/Durst/Muedigkeit/Vertrauen). Fenster-Bild einmal selbst aus dem Code
zeichnen und ansehen. Urteil: bereit fuer Kevins Einzelspieler-Test? Bericht ${F}/GEGEN.md; Testanleitung ${F}/anleitung_entwurf.md pruefen/berichtigen.
jar_ausnahmen = jede nur im Jar belegte Methode im Staging (mit Datei:Zeile), fragen_an_kevin = alle offenen Kleinfragen kurz auf Deutsch.`,
  { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })

return { kern, ober, texte, befunde: befunde.length, fix, gegen }
