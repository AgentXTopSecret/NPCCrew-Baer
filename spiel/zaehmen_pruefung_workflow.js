export const meta = {
  name: 'baer-zaehmen-pruefung',
  description: 'Baer-Junges finden und zaehmen (B1a), Etappe 2: zwei Pruefer, Nachbesserung, Gegenpruefer (4 Agenten auf Opus; nichts in die Test-Mod)',
  phases: [
    { title: 'Pruefung', detail: 'Pruefer A (Engine-Belege, Regeln, Cheat-Trennung, Texte, Uebernahme-Skript) und Pruefer B (Logik, SP/MP, rote Linien)', model: 'opus' },
    { title: 'Nachbesserung', detail: 'bestaetigte Befunde im Staging beheben, alle Pruefer neu', model: 'opus' },
    { title: 'Gegenpruefung', detail: 'jeden Befund nachpruefen, Urteil bereit fuer den SP-Test', model: 'opus' },
  ],
}

const W = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen'
const B = 'C:/Users/Kevin/NPCCrew-Nebenprojekte/baer'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Du arbeitest im Lauf "baer-zaehmen" (B1a) fuer Kevins Mod NPC Crew (Project Zomboid B42; das Spiel ist laut Forschung inzwischen 42.22.2,
Bandits laedt aus ${BAN}/42.22 und ${BAN}/common). Gebaut wurde in Etappe 1: ein Baeren-Junges (Tierart ncbearcub) im Wald finden oder per
Koederplatz anlocken, aus der Hand fuettern und streicheln, Zaehm-Balken, Besitz je Spieler, Register am Server, Sandbox-Optionen, sieben
Sprachen, Bench-Datei, Uebernahme-Skript. NICHT Teil von B1a: Wachsen, Kampf, Befehle, Baeren-Fenster, Beduerfnisse, Inventar, Schlafen,
Umbenennen der alten NCBear*-Dateien.

LIES ZUERST (in dieser Reihenfolge, ganz): ${W}/PLAN_ZAEHMEN.md, ${W}/bau_uebernahme.md, ${W}/bau_kern.md, ${W}/bau_oberflaeche.md,
${W}/schnittstelle_aenderungen.md; nachschlagen in ${W}/forschung_engine.md und ${W}/forschung_bestand.md.
STAGING (der Pruefgegenstand): ${W}/mod/ (spiegelt die Wurzel der Test-Mod; Liste ${W}/staging_dateien.txt, 40 Dateien, davon 15 Lua).
Dazu ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md. Attrappen: ${W}/attrappe/ (gesamt/run.lua mit lua5.1:
C:/Users/Kevin/Tools/lua51/lua5.1.exe). Lua-Pruefer (nur aufrufen): python ${NC}/_docs/tools/luacheck.py, scopecheck.py, localcount.py,
luacheck_pz.py.

SUCHORTE (nur diese, nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk): ${W}, ${B}, Vanilla ${VAN} (nur lesen), Bandits ${BAN}/42.22 und
${BAN}/common (nur lesen), NPC Crew ${NC}/42/media/lua und ${NC}/_docs/landkarte_index.txt (nur lesen), Test-Mod ${T} (nur lesen),
Jar-Auszuege ${W}/jar, ${W}/javap, ${W}/dec.

FESTE REGELN: Nie in die Test-Mod, nach NPC Crew, Vanilla oder Bandits schreiben. Kein git, kein Spielstart, kein Download, nichts hochladen.
Eiserne Regel: jeder Engine-Aufruf braucht eine Fundstelle als echten Aufruf in Vanilla-Lua oder Bandits mit GLEICHEN Argumenttypen
(Jar allein reicht nicht; ein pcall um einen unbelegten Aufruf ist eine Tarnkappe). SP und MP muessen beide stimmen; SP-Test ist
"not isServer() and not isClient()"; was der Server wissen muss, kommt nie aus einem Client-Glauben. Kevins rote Linien: kein Gegenstand
verloren oder verdoppelt, kein Kick (Rolle user, AntiCheat), nichts haengt endlos, keine NPC-Crew-Figur wird gestoert. Testbefehle, Spawn-
und Debug-Menues nur in NCBearBench*.lua. Namen: BanditsNPCBear*.lua, Modul BanditsNPC.Bear, Texte UI_BN_Bear_* in EN, PTBR, RU, KO, ES,
CN, FR. Nichts Teures je Bild, Deckel fuer alles, was waechst. Kahlua ist kein echtes Lua 5.1 (kein next). Schreibe "statisch geprueft,
nicht gespielt"; keine Behauptung ohne Fundstelle (Datei:Zeile), sonst "ungeprueft".`

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

phase('Pruefung')
const [pa, pb] = await parallel([
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER A -- Belege, Regeln, Trennung, Texte, Uebernahme. Du aenderst KEINE Datei ausser deinem Bericht.
1. Eiserne Regel: Gehe ALLE 15 Lua-Dateien des Stagings Zeile fuer Zeile durch. Fuer JEDEN Engine-Aufruf (Methoden auf Java-Objekten,
   globale Engine-Funktionen, Events, ISBaseTimedAction-Felder, Kontextmenue-Aufrufe): schlage die im Kommentar genannte Fundstelle im
   heutigen Vanilla bzw. Bandits 42.22 selbst nach. Stimmt Datei und ungefaehr die Zeile? Gleiche Argumentzahl und -typen? Gleiche Seite
   (Client/Server)? Aufrufe ohne Fundstelle, mit falscher Fundstelle oder nur mit Jar-Beleg sind Befunde (blocker, wenn der Aufruf im
   normalen Ablauf liegt).
2. Trennung: kein Testbefehl, Spawn-/Debug-Menue, isDebugEnabled, Konsolenbefehl ausserhalb von NCBearBenchCub.lua; die Bench laeuft nur im
   SP. Die Bench darf vom echten Code nie gebraucht werden.
3. Namen und Kollisionen: jede neue globale Tabelle, Funktion, Datei, Textschluessel, Sandbox-Option, Skriptname gegen NPC Crew
   (${NC}/42/media/lua) und Vanilla greppen. Alte Dateien der Test-Mod duerfen nicht veraendert sein (einzige Ausnahme laut Plan:
   Translate/EN/IG_UI.json -- pruefe, dass die 4 alten Schluessel wortgleich sind).
4. Texte: alle Schluessel in allen sieben Sprachen vorhanden, gleiche Platzhalter (%1 usw.) je Sprache, natuerliche Saetze, Crew-Figuren
   neutral, CN nur Zeichen aus Vanilla-CN, JSON-Round-Trip (json.dumps(data, indent=4, ensure_ascii=False) + Zeilenende). Sandbox:
   jede Option in sandbox-options.txt hat Texte und wird im Code gelesen (und umgekehrt), Wertebereiche sinnvoll.
5. Tier-Definition und Skript: ${W}/mod/42/media/lua/shared/BanditsNPCBearDefs.lua und scripts/nc_bear_cub.txt gegen die gespielte
   Definition des Erwachsenen (${T}/42/media/lua/shared/NCBearDefs.lua, ${T}/42/media/scripts/nc_bear_tier.txt) und Vanilla (Kitz,
   Waschbaer): fehlt ein Pflichtfeld, das beim Erwachsenen steht? animset, Clips, Rasse, Textur, Stufen.
6. Uebernahme-Skript und NAEHTE.md: Trockenlauf und --probe selbst laufen lassen (wie in bau_uebernahme.md 4.1/4.2), Ergebnis vergleichen;
   stichprobenartig pruefen, dass die Cheat-Pruefung wirklich anschlaegt (eigene verdorbene Kopie NUR im Probe-Ordner oder Scratchpad).
7. Alle vier Lua-Pruefer und die Gesamt-Attrappe selbst laufen lassen und die Zahlen nennen.
Ergebnis: ${W}/pruef_a.md (Tabelle aller geprueften Engine-Aufrufe mit Urteil, Befunde mit Datei:Zeile und Beleg). Rueckgabe: die Befunde
strukturiert (id A1, A2, ...). Nur echte, belegte Befunde; Geschmack als minor.`, { label: 'pruef:belege', phase: 'Pruefung', model: 'opus', schema: FIND }),
  () => agent(`${CTX}

DEINE ROLLE: PRUEFER B -- Logik, Einzelspieler/Mehrspieler, rote Linien, Leistung. Du aenderst KEINE Datei ausser deinem Bericht.
Lies den Code der 15 Lua-Dateien ganz (nicht nur die Berichte) und verfolge jeden Vorgang von der Auswahl im Menue bis zum Register:
Erscheinen im Wald, Koeder legen / aufgeben / Nacht / Morgen, Entdecken, Fuettern, Streicheln, Zaehmen, Verschwinden, Tod, Sperre, Sicht
zum Client, Hello/Sync, Speichern/Laden, Gegend entladen/neu laden, Spieler verlaesst den Server, zweiter Spieler.
Suche gezielt nach:
1. Gegenstand verloren oder verdoppelt: Futter/Koeder wird genau einmal und nur vom Schreiber (SP bzw. Server) genommen; was passiert bei
   Abbruch der Zeitaktion, bei vollem Tier, wenn das Tier waehrenddessen verschwindet, bei zwei Spielern gleichzeitig, wenn der Server
   ablehnt, nachdem der Client angefangen hat?
2. Kick-Gefahr im MP: entfernt oder erzeugt der Client je selbst etwas? Befehle mit Client-Glauben (Positionen, IDs, Mengen), die der
   Server ungeprueft uebernimmt? Zu grosse oder zu haeufige Sendungen?
3. Endlos-Haenger und Lecks: Schleifen ohne Deckel, Tabellen, die wachsen, Timer, die nie enden, Tier bleibt fuer immer gesperrt
   (setBlockMovement), Variable bleibt gesetzt, Register-Eintraege, die nie schliessen, Zustaende ohne Ausgang.
4. SP-Zweig: laeuft wirklich alles mit "not isServer() and not isClient()"? sendServerCommand tut im SP nichts -- wird ueberall direkt
   gerufen? Datei-Riegel (if isClient() then return end) richtig herum? Dedizierter Server: nichts Client-Eigenes (UI, getPlayer) im
   Server-Pfad.
5. Zustandsmaschine und Zahlen: Zaehm-Balken, Wartezeiten, Deckel je Spieler und Welt, Verschwinde-Regel, Sperre nach Tod -- stimmt der
   Code mit ${W}/PLAN_ZAEHMEN.md und Kevins Entscheidungen (${B}/begleiter/ENTSCHEIDUNGEN.md, Abschnitte zum Bekommen/Zaehmen und der letzte
   vom 10.11.) ueberein? Randfaelle: Werte 0, sehr gross, Sandbox-Option aus.
6. Stoerung anderer: beruehrt etwas den erwachsenen Baeren der Test-Mod (Art bear), NPC-Crew-Figuren, Vanilla-Tiere, Vanillas Tier-Menue
   fuer andere Tiere? Laeuft alles mit UND ohne NPC Crew (Existenz-Riegel)?
7. Leistung: nichts Teures je Bild (OnTick, Render), Listen selten erneuert, Suchen gedeckelt.
8. Schreibe drei eigene Attrappen-Faelle fuer die riskantesten Stellen (unter ${W}/attrappe/pruef_b/, bestehende Attrappen nur benutzen,
   nicht aendern) und lass sie laufen.
Ergebnis: ${W}/pruef_b.md (je Vorgang der Weg durch den Code mit Datei:Zeile, SP- und MP-Zweig, Befunde mit Beleg und Gegenbeispiel).
Rueckgabe: die Befunde strukturiert (id B1, B2, ...). Nur echte, belegte Befunde; Geschmack als minor.`, { label: 'pruef:logik', phase: 'Pruefung', model: 'opus', schema: FIND }),
])
const befunde = [...((pa && pa.findings) || []), ...((pb && pb.findings) || [])]
log('Pruefung: A ' + (pa ? pa.findings.length : 'FEHLT') + ' Befunde, B ' + (pb ? pb.findings.length : 'FEHLT') + ' Befunde')
if (!pa && !pb) {
  return { pa, pb, fix: null, gegen: null, abbruch: 'beide Pruefer ohne Ergebnis' }
}

phase('Nachbesserung')
const fix = await agent(`${CTX}

DEINE ROLLE: NACHBESSERUNG. Zwei Pruefer haben das Staging geprueft (Berichte ${W}/pruef_a.md und ${W}/pruef_b.md). Ihre Befunde:
${JSON.stringify(befunde, null, 1)}

1. Pruefe JEDEN Befund selbst am Code nach (Datei:Zeile lesen, Fundstellen nachschlagen). Ein Befund, der nicht stimmt, wird mit Beleg
   abgelehnt, nicht "vorsichtshalber" umgebaut.
2. Behebe alle bestaetigten blocker und major im Staging (${W}/mod/), minor, wenn es klein und sicher ist. Kleinste Aenderung, die den
   Fehler wirklich schliesst; keine neuen unbelegten Engine-Aufrufe (neue Aufrufe mit Fundstelle im Kommentar); Schnittstelle zwischen
   Kern und Oberflaeche nur aendern, wenn noetig, dann beide Seiten und ${W}/schnittstelle_aenderungen.md (anhaengen).
   Texte immer in allen sieben Sprachen. Falls noetig auch ${B}/tools/baer_uebernahme.py und ${B}/NAEHTE.md.
3. Danach ALLES neu: vier Lua-Pruefer auf alle 15 Lua-Dateien, Zeilenenden/ASCII, JSON-Round-Trip, Gesamt-Attrappe
   (${W}/attrappe/gesamt/run.lua; Attrappe nur anpassen, wenn der Code sich gewollt geaendert hat, und das begruenden), Trockenlauf und
   --probe des Uebernahme-Skripts wie in ${W}/bau_uebernahme.md 4.1/4.2. ${W}/staging_dateien.txt neu erzeugen (Pfad | MD5 | Bytes |
   neu/ueberschreibt).
Ergebnis: ${W}/nachbesserung.md (je Befund: bestaetigt/abgelehnt mit Beleg, was geaendert wurde mit Datei:Zeile vorher/nachher, alle
Pruefer-Ausgaben, was offen bleibt). Rueckgabe: Kurzfassung je Befund-ID und die neuen Zahlen der Pruefer.`, { label: 'nachbesserung', phase: 'Nachbesserung', model: 'opus' })
if (!fix) {
  return { pa, pb, fix: null, gegen: null, abbruch: 'Nachbesserung ohne Ergebnis' }
}

phase('Gegenpruefung')
const gegen = await agent(`${CTX}

DEINE ROLLE: GEGENPRUEFER. Du hast nichts davon gebaut und glaubst keinem Bericht. Die Pruefer meldeten diese Befunde:
${JSON.stringify(befunde.map(f => ({ id: f.id, schwere: f.schwere, datei: f.datei, zeile: f.zeile, behauptung: f.behauptung })), null, 1)}
Die Nachbesserung berichtet in ${W}/nachbesserung.md.

1. Je Befund: ist er im HEUTIGEN Staging wirklich geschlossen (Code lesen, nicht den Bericht)? Wurde ein Befund zu Unrecht abgelehnt?
   Hat die Nachbesserung etwas Neues kaputt gemacht (jede geaenderte Stelle samt Umgebung lesen; neue Engine-Aufrufe ohne Fundstelle)?
2. Selbst laufen lassen und Zahlen nennen: vier Lua-Pruefer auf alle 15 Lua-Dateien, Gesamt-Attrappe, Trockenlauf und --probe des
   Uebernahme-Skripts (mit --vor-b5a wie in ${W}/bau_uebernahme.md). ${W}/staging_dateien.txt gegen die Platte nachzaehlen (MD5, Anzahl);
   nachweisen, dass keine bestehende Datei der Test-Mod ausser Translate/EN/IG_UI.json ueberschrieben wuerde.
3. Zwei eigene Stichproben, die bisher niemand gemacht hat (z. B. ein ganzer Vorgang im MP-Zweig Zeile fuer Zeile; eine Sprache
   vollstaendig gegengelesen; Verhalten bei abgeschalteter Sandbox-Option).
4. Urteil: Ist das Staging bereit fuer Kevins ERSTEN Einzelspieler-Test in der Test-Mod (laedt ohne rote Fehler, Junges per Bench-Befehl
   holbar, fuettern, streicheln, zaehmen)? Blocker sind nur Dinge, die diesen Test verhindern oder eine rote Linie reissen; alles
   andere als Restbefund. Nenne ehrlich, was nur das Spiel zeigen kann.
Ergebnis: ${W}/gegen_bericht.md und ein Entwurf der Testanleitung fuer Kevin ${W}/anleitung_zaehmen_entwurf.md (Deutsch, kurz, Schritt
fuer Schritt, mit den Bench-Befehlen zum Eintippen, was er sehen soll, und wo rote Fehler stehen). Rueckgabe: das Urteil strukturiert.`, { label: 'gegenpruefung', phase: 'Gegenpruefung', model: 'opus', schema: VERDICT })

return { pa, pb, fix, gegen }
