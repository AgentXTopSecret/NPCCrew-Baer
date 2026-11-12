export const meta = {
  name: 'baer-f1b-fortsetzung',
  description: 'Baer F1b FORTSETZUNG ohne Lauf-Cache: Forschung, Plan und Bau sind fertig auf der Platte (forschung_f1b.md, PLAN_F1B.md, bau_f1b.md, Staging mod_f1b), es geht ab Pruefung weiter -- 5 Agenten; nichts in die Test-Mod',
  phases: [
    { title: 'Forschung', detail: 'E/V in Vanilla und NPC Crew, ModOptions-Tasten, Naehe wie NPC Crew' },
    { title: 'Plan', detail: 'PLAN_F1B.md: Tastenweg, Abstand, Optionen-Seite, Wachstums-Schalter, Texte, Tests' },
    { title: 'Bau', detail: 'ein Bauer, nur Client-Dateien + Texte im Staging mod_f1b' },
    { title: 'Pruefung', detail: 'Pruefer A Belege/Regeln/Texte, Pruefer B Logik/Kollisionen/SP-MP' },
    { title: 'Nachbesserung', detail: 'bestaetigte Befunde beheben, alles neu pruefen' },
    { title: 'Gegenpruefung', detail: 'Urteil bereit fuer Kevins Test + Testanleitung' },
    { title: 'Zusammenfuehren', detail: 'F1b-Aenderungen in das F2-Staging mod/ uebertragen (F2 angehalten)' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const S = W + '/mod_f1b'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-f1b" fuer Kevins Mod NPC Crew (Project Zomboid 42; Bandits laedt aus ${BAN}/42.21 bzw. 42.22 und
${BAN}/common). Kevin programmiert nicht, er spielt und testet. Schreibe Berichte auf Deutsch.

VORGESCHICHTE: F1 (Baeren-Fenster, Befehle Follow/Stay/Sit/Roam free/Come here/Unstuck, Passive, Name tag) ist gebaut, geprueft und seit 12.11.
04:04 in der Test-Mod ${T} (Git main 455ced2). Berichte: ${W}/PLAN_F1.md, forschung_f1.md, bau_f1_*.md, pruef_f1_a/b.md, nachbesserung_f1.md,
gegen_bericht_f1.md, Testanleitung ${B}/spiel/anleitung_f1.md. Die Taste steckt in ${S}/42/media/lua/client/BanditsNPCBearKey.lua (Zeile in
Vanillas keyBinding "Bear window" = V, Vorfahrt vor Vanillas Tier-Radial, Rad am eigenen Baeren geschlossen), Mod-Optionen in
BanditsNPCBearOptions.lua (Seite "NPC Crew: Bear"), Fenster ISUI/BanditsNPCBearWindow.lua, Rechtsklick "Bear window" in BanditsNPCBearMenu.lua.

KEVINS WUNSCH (12.11.2026 ~04:40, woertlich): "also folgendes problem das fenster geht auf V auf aber das war eigtl so gemeint wenn man in der
naehe ist wie bei den npc's ich wuerde vorschlagen aber jz weil wenn man mit npc's unterwegs ist die auf v auf gehn dann ist es schwer das baeren
inventar zu oeffnen deswegen schlag ich vor bei E das baeren ui zu oeffnen und wenn man es aus der ferne oeffnen will dann kann man beim UI den
hotkey festelegen um es aus der ferne aufzurufen und em die E taste fuer den baeren wenn man in der naehe ist in sen mod settings zum aendern
eintragen falls jemand nicht E nutzen will sondern einen anderen key".
Daraus AUFTRAG F1B (Kevin ist wach, aber waehrend des Laufs keine Fragen; offene Kleinfragen mit dem EMPFOHLENEN Weg bauen und als "Fragen fuer
Kevin" mit dem gewaehlten Weg in den Bericht):
1. NAH-TASTE: steht der Spieler nahe am EIGENEN Baeren (Abstand wie NPC Crews V bei NPCs -- belegt ermitteln, sonst begruendet ~2-3 Kacheln,
   gleiche Etage), oeffnet/schliesst Taste E das Baeren-Fenster. Vorgabe E, einstellbar in Optionen > Mods > "NPC Crew: Bear" (Vanillas
   PZAPI-ModOptions-Taste, ${VAN}/lua/client/PZAPI/ModOptions.lua:182 Options:addKeyBind -- Abfrage und Speichern belegen). Ist kein eigener Baer
   nah: NICHTS tun und nichts melden (E bleibt fuer Vanillas Interact, z. B. Tueren). E ist Vanillas INTERACT (${VAN}/lua/shared/keyBinding.lua:32-33):
   pruefen, was Vanilla auf E in Baeren-Naehe sonst tut (Tuer, Fenster, Fahrzeug, Gegenstand, Tier) und eine belegte Regel waehlen, damit nicht zwei
   Dinge auf einmal passieren, wo es vermeidbar ist (z. B. nicht oeffnen, wenn der Spieler im Fahrzeug sitzt, zielt, im Menue/Chat tippt, ein
   anderes Fenster den Fokus hat) -- was nicht vermeidbar ist, ehrlich als Frage an Kevin.
2. FERN-TASTE: eine zweite Taste in derselben Mod-Optionen-Seite, oeffnet/schliesst das Fenster aus jeder Entfernung (heutiges V-Verhalten mit
   "You do not have a bear yet." und vermisstem/nicht geladenem Baeren). VORGABE: KEINE Taste (Kevin: "kann man ... den hotkey festlegen").
   Belegen, wie ModOptions "keine Taste" darstellt (Keyboard.KEY_NONE o. ae.).
3. V GEHOERT WIEDER NPC CREW UND VANILLA: die Zeile "Bear window" in Vanillas keyBinding und die V-Vorfahrt entfallen; pruefen, was mit einer
   gespeicherten alten Belegung in Kevins Optionen passiert (belegt). Vanillas Tier-Radial am eigenen Baeren: darf wieder aufgehen, aber ohne
   "Kill" (wenn belegt moeglich, sonst bleibt es zu -- begruenden); der Rechtsklick "Bear window" bleibt. Sitzt NPC Crews "Talk to NPC" auf V,
   darf nichts davon gestoert werden (nur lesen: ${NC}/42/media/lua/client/BanditsNPCInteract.lua um :7462-7480).
4. Kleiner Hinweis im Fenster (unten, klein, 7 Sprachen), welche Tasten gelten ("E near your bear", Fern-Taste falls gesetzt) -- nur wenn es das
   ruhige Aussehen nicht stoert (Kevin mag das Fenster so, wie es ist: "ui anzeige passt ... das ist top").
5. WACHSTUMS-ZEILE JE BAER (Kevin 12.11. ~04:50 woertlich: "ich will auch im ui einen schalter haben das die anzeige aus geht wann der
   waechst und wenn er bei 100% ist soll der knopf ganz verschwinden aus dem ui weil er dann unnoetig waere wenn das geht ;D also ueber den baeren
   die anzeige"): im Baeren-Fenster ein Schalter "Growth line" (Name nach Plan, 7 Sprachen) je Baer, der die Alter-/Wachstums-Zeile UEBER dem
   Baeren ("Day 12 - half-grown in 3 day(s)", ${S}/42/media/lua/client/ISUI/BanditsNPCBearHud.lua um :343-353) an/aus schaltet -- gespeichert wie
   der Namensschild-Schalter je Baer in der Client-Datei (BanditsNPCBearTags.lua, "tagoff <u>"; eigenes Praefix, gleicher Deckel). Die globale
   Option TagAge (Optionen > Mods) bleibt Hauptschalter. Ist der Baer AUSGEWACHSEN (keine naechste Stufe, c.nst == nil): die Wachstums-Zeile ueber
   dem Baeren entfaellt von selbst (heute steht dort dauerhaft "Day N - full-grown", UI_BN_Bear_Tag_AgeDone) UND der Schalter verschwindet ganz
   aus dem Fenster (Platz schliesst sich ruhig, nichts springt unschoen). Wird er wieder klein (Testbefehl NCBear_CubGrow(-100)), kommt beides
   wieder (gespeicherter Schalter gilt dann weiter).
NICHT in F1B: alles aus F2 (Kampf), Modelle, server/ und shared/ (nur lesen; braucht der Weg dort etwas, als Befund melden statt bauen),
NPC-Crew-Dateien.

ORTE: Staging (Pruefgegenstand und Bauort) ${S}/ -- Kopie des F1-Schnappschusses ${W}/mod_f1_fertig/, byte-gleich mit der Test-Mod (Liste
${W}/staging_dateien_f1.txt, Spalten Pfad | MD5 | Bytes | neu/ueberschreibt/gleich). NICHT anfassen: ${W}/mod/ (Staging des angehaltenen F2-Laufs,
nur die letzte Rolle "Zusammenfuehren" schreibt dort) und ${W}/mod_f1_fertig/. Attrappen ${W}/attrappe/ (lua5.1: C:/Users/Kevin/Tools/lua51/lua5.1.exe;
eigene F1b-Faelle unter ${W}/attrappe/f1b/). Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py. Uebernahme-Skript ${B}/tools/baer_uebernahme.py (Trockenlauf und --probe mit --vor-b5a; es prueft die TEST-MOD -- fuer das
Staging eine Kopie des Skripts unter ${W}/f1b_werkzeug/ mit auf ${S} gebogenem Pfad nutzen, das Original nicht aendern ausser in der Rolle
Zusammenbau/Nachbesserung, wenn F1b neue Dateien oder Texte bringt), Naehte ${B}/NAEHTE.md (Zeilen 27-29 Taste/Fenster).

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, Vanilla ${VAN} (nur lesen), Bandits ${BAN} (nur lesen),
NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen, nichts kopieren), Test-Mod ${T} (nur lesen).

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben (Claude baut nach der Pruefung selbst ein). Kein git, kein
Spielstart, kein Download, nichts hochladen. EISERNE REGEL: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder
Bandits mit GLEICHEN Argumenttypen, im Kommentar genannt; Ausnahme nur mit Kevins Wort je Methode -- erteilt fuer animal:pathToLocation(x, y, z),
setVariable("animalRunning", ...) am Tier und (12.11.) getTextOrNull(key, "%1".."%9") nur fuer die Existenzfrage in B.T. Ein pcall um einen
unbelegten Aufruf ist eine Tarnkappe. SP UND MP: Tasten sind reine Client-Sache; Befehle aus dem Fenster gehen wie in F1 zum Server, der
Besitz und Lage prueft. SP-Test "not isServer() and not isClient()". Kevins rote Linien: kein Gegenstand verloren oder verdoppelt, kein Kick,
nichts haengt endlos, keine NPC-Crew-Figur wird gestoert, der Baer geht nie verloren und wird nie verdoppelt. Keine Testbefehle ausserhalb
NCBearBench*.lua. Namen: BanditsNPCBear*.lua, Texte UI_BN_Bear_* in EN, PTBR, RU, KO, ES, CN, FR (CN nur Zeichen aus Vanilla-CN), Optionen-IDs
mit Praefix wie die bestehenden in BanditsNPCBearOptions.lua; vor jedem neuen Namen in NPC Crew greppen. Nichts Teures je Bild (Taste nur in
OnKeyPressed; Abstand nur beim Druck rechnen). Dateien LF, ASCII in Lua; localcount aktiv UND insgesamt unter 180. JSON-Round-Trip
json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende, sortiert. Schreibe "statisch geprueft, nicht gespielt"; keine Behauptung ohne
Fundstelle (Datei:Zeile), sonst "ungeprueft".`

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
          datei: { type: 'string' },
          zeile: { type: 'string' },
          behauptung: { type: 'string' },
          beleg: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['id', 'schwere', 'datei', 'behauptung', 'beleg', 'vorschlag'],
      },
    },
  },
  required: ['zusammenfassung', 'findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    bereit_fuer_sp_test: { type: 'boolean' },
    zusammenfassung: { type: 'string' },
    offene_blocker: { type: 'array', items: { type: 'string' } },
    restbefunde: { type: 'array', items: { type: 'string' } },
    befunde_geschlossen: { type: 'integer' },
    befunde_offen: { type: 'integer' },
    staging_dateien: { type: 'integer' },
    pruefer_ausgaben: { type: 'string' },
    fragen_an_kevin: { type: 'array', items: { type: 'string' } },
  },
  required: ['bereit_fuer_sp_test', 'zusammenfassung', 'offene_blocker', 'restbefunde', 'staging_dateien', 'pruefer_ausgaben'],
}

// FORTSETZUNG (12.11.2026 08:13, Wochenlimit): Forschung, Plan und Bau liefen im Lauf wf_217a0733-3d7 (alte Sitzung) und liegen als Dateien vor.
// Der Lauf-Cache gilt nur in der alten Sitzung -- deshalb ohne diese drei Agenten; die Pruefer lesen die Berichte selbst.
const fo = `Forschung ist fertig: ${W}/forschung_f1b.md.`
const plan = `Plan ist fertig: ${W}/PLAN_F1B.md.`
const bau = `Bau ist fertig: ${W}/bau_f1b.md, Staging ${S}/, Liste ${W}/staging_dateien_f1b.txt, mod.info-Vorschlag ${W}/mod_info_vorschlag_f1b.txt.`
log('Fortsetzung ab Pruefung: Forschung, Plan, Bau aus Dateien')

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht. Pruefe alle in F1B geaenderten
Dateien (Liste ${W}/bau_f1b.md und ${W}/staging_dateien_f1b.txt): jeder Engine-Aufruf gegen die Fundstelle im heutigen Vanilla/Bandits
(Datei, Zeile, Argumenttypen, Seite), Jar-only = Befund; ModOptions-Tasten richtig angelegt und gelesen; keine Testbefehle ausserhalb der
Bench; nur client/ und Translate/ geaendert (sonst Befund); Texte in sieben Sprachen (Schluessel, Platzhalter, Round-Trip, CN-Zeichen);
Uebernahme-Kopie Trockenlauf/--probe selbst laufen lassen; vier Lua-Pruefer und alle Attrappen selbst laufen lassen, Zahlen nennen.
Ergebnis ${W}/pruef_f1b_a.md. Rueckgabe strukturiert (id A1...). FORTSETZUNG nach Halt 08:13 (Wochenlimit 97 %): Zwischenstaende pruefen, nur Vollstaendiges weiterverwenden.`, { label: 'pruef:belege', phase: 'Pruefung', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, Tasten-Kollisionen, SP/MP, rote Linien. Du aenderst KEINE Datei ausser deinem Bericht und eigenen Attrappen
unter ${W}/attrappe/pruef_f1b/. Verfolge jeden Tastendruck: E nah am eigenen Baeren / nah an fremdem Baeren / nah an Tuer + Baer / im Fahrzeug /
beim Tippen im Chat / bei offenem anderem Fenster / Baer auf anderer Etage / Baer vermisst oder nicht geladen; Fern-Taste nicht gesetzt (darf
nie ausloesen, auch nicht bei Tastencode 0) und gesetzt (auch auf E oder V -- was dann?); V neben NPC und Baer (nur noch NPC Crew bzw.
Vanilla); Tier-Radial am eigenen Baeren (kein Kill); Wachstums-Schalter je Baer (zwei Baeren, ausgewachsen, zurueck, Deckel der Datei). Kann ein Druck den Baeren verlieren, verdoppeln, fremde Baeren steuern, NPC Crew
stoeren oder Vanilla-E kaputtmachen? Kosten je Druck. Drei eigene Attrappen-Faelle fuer die riskantesten Stellen. Ergebnis ${W}/pruef_f1b_b.md.
Rueckgabe strukturiert (id B1...). FORTSETZUNG nach Halt 08:13 (Wochenlimit 97 %): Zwischenstaende pruefen, nur Vollstaendiges weiterverwenden.`, { label: 'pruef:logik', phase: 'Pruefung', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: ' + befunde.length + ' Befunde')
if (!pa && !pb) { return { fo, plan, bau, abbruch: 'beide Pruefer ohne Ergebnis' } }

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Befunde der Pruefer (Berichte ${W}/pruef_f1b_a.md, ${W}/pruef_f1b_b.md):
${JSON.stringify(befunde, null, 1)}
Jeden Befund selbst am Code nachpruefen; falsche mit Beleg ablehnen. Bestaetigte blocker/major beheben, minor wenn klein und sicher; keine
neuen unbelegten Aufrufe; Texte immer in sieben Sprachen. Danach ALLES neu: vier Lua-Pruefer, Zeilenenden/ASCII, JSON-Round-Trip, alle
Attrappen, Trockenlauf und --probe (Kopie unter ${W}/f1b_werkzeug/, --vor-b5a), ${W}/staging_dateien_f1b.txt neu. Ergebnis
${W}/nachbesserung_f1b.md. Rueckgabe: je Befund-ID Kurzfassung und die neuen Zahlen.`, { label: 'nachbesserung', phase: 'Nachbesserung' })
if (!fix) { return { fo, plan, bau, pa, pb, abbruch: 'Nachbesserung ohne Ergebnis' } }

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Befunde der Pruefer:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Bericht der Nachbesserung: ${W}/nachbesserung_f1b.md.
1. Je Befund am HEUTIGEN Code: geschlossen? Zu Unrecht abgelehnt? Hat die Nachbesserung etwas kaputt gemacht?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer, alle Attrappen, Trockenlauf und --probe (Kopie, --vor-b5a). staging_dateien_f1b.txt
   gegen die Platte nachzaehlen; nachweisen, welche Dateien der Test-Mod ueberschrieben wuerden (nur client/ und Translate/; alte NCBear*-Dateien
   ausser NCBearBench* nie).
3. Zwei eigene Stichproben (z. B. E neben Tuer und Baer Zeile fuer Zeile; Fern-Taste "keine" bei Tastencode 0).
4. Urteil: bereit fuer Kevins naechsten Einzelspieler-Test (laedt ohne rote Fehler; E nah oeffnet, fern nicht; Fern-Taste einstellbar; V
   oeffnet das Baeren-Fenster nicht mehr; NPC Crews V unberuehrt; Wachstums-Schalter wirkt, ausgewachsen ist er samt Zeile weg; F1 sonst
   unveraendert)? Blocker nur, was diesen Test verhindert oder eine rote
   Linie reisst.
Ergebnis ${W}/gegen_bericht_f1b.md und Testanleitung ${W}/anleitung_f1b_entwurf.md (Deutsch, kurz, Schritt fuer Schritt fuer Kevin; Spiel mit
-debug neu starten; nur NCBearTest noetig, fuer den V-Test zusaetzlich NPC Crew; wo die Tasten eingestellt werden). Rueckgabe: das Urteil
strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', schema: VERDICT })
if (!gegen || !gegen.bereit_fuer_sp_test) { return { fo, plan, bau, pa, pb, fix, gegen, abbruch: 'Gegenpruefung nicht bereit -- kein Zusammenfuehren' } }

phase('Zusammenfuehren')
const merge = await agent(`${CTX}

DEINE ROLLE: ZUSAMMENFUEHREN in das F2-Staging. Der Lauf F2 (B5a Kampf) ist angehalten und baut in ${W}/mod/ auf F1 auf; dort liegen halbe
F2-Aenderungen (nicht pruefen, nicht aendern, nur erhalten). Basis = ${W}/mod_f1_fertig/ (F1), F1B = ${S}/, F2 = ${W}/mod/. Fuer JEDE Datei,
die F1B gegenueber der Basis aendert oder neu bringt (Liste aus staging_dateien_f1b.txt bzw. MD5-Vergleich Basis/F1B):
- F2 hat sie nicht angefasst (MD5 F2 = Basis): F1B-Datei nach ${W}/mod/ kopieren.
- F2 hat sie auch geaendert: Drei-Wege-Zusammenfuehrung je Stelle (Lua per diff Basis->F1B auf die F2-Fassung anwenden; UI.json je Schluessel
  zusammenfuehren, sortiert, Round-Trip). Kollidiert eine Stelle wirklich, F2-Fassung behalten, F1B-Stelle daneben einsetzen und in den Bericht.
Vorher ${W}/mod/ als Zip nach ${W}/mod_vor_f1b_merge.zip sichern. Danach vier Lua-Pruefer auf die beruehrten Dateien in ${W}/mod/ und
Lua-5.1-Syntax (loadfile). Ergebnis ${W}/f1b_merge.md (je Datei: kopiert / zusammengefuehrt / Kollision; Pruefer-Ausgaben), damit der F2-Lauf
beim Fortsetzen weiss, dass diese F1B-Stellen gewollt sind. Rueckgabe: Kurzfassung mit Zahlen.`, { label: 'zusammenfuehren', phase: 'Zusammenfuehren' })

return { fo, plan, bau, pa, pb, fix, gegen, merge }
