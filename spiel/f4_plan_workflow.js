export const meta = {
  name: 'baer-f4-plan',
  description: 'Baer F4 (Traglast + eigenes Inventar + Packtaschen) -- Forschung auf dem Stand nach F3 + Plan; Bau als eigener Lauf nach Kevins Antworten (2 Agenten; nur lesen + Plan schreiben)',
  phases: [{ title: 'Forschung' }, { title: 'Plan' }],
}

const N = 'C:/Users/Kevin/NPCCrew-Nebenprojekte'
const W = N + '/_arbeit/baer_zaehmen'
const F = W + '/f4'
const B = N + '/baer'
const T = 'C:/Users/Kevin/Zomboid/mods/NCBearTest'
const NC = 'C:/Users/Kevin/Zomboid/mods/NPCCrew'
const VAN = 'C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media'
const BAN = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits'

const CTX = `Lauf "baer-f4-plan" fuer Kevins Mod NPC Crew (Project Zomboid 42.22; Bandits ${BAN}/42.22, ${BAN}/common). Deutsch, "statisch geprueft,
nicht gespielt", jede Behauptung mit Fundstelle (Datei:Zeile). Keine Fragen an Kevin waehrend des Laufs -- am Ende EINE Frageliste.
F4 = TRAGLAST + EIGENES INVENTAR des gezaehmten Baeren (+ Packtaschen). KEVINS WORTE (ganz lesen, gehen vor): ${B}/begleiter/ENTSCHEIDUNGEN.md --
Abschnitt "Inventar und Fischen" (Zeile ~29-31: "Eigenes Inventar zum Oeffnen. Traglast: Jungtier 10, Halbstark 40, Erwachsen 100 (wie ein grosser
Kofferraum), Packtaschen als Ausruestung +50, Sandbox-Faktor fuer mehr (500 abgelehnt: dann braucht niemand ein Auto). Ob ein lebendes Tier ein
oeffenbares Inventar haben kann: ungeprueft."), Werte wachsen jeden Tag mit der Groesse (Zeile ~207, ~212, Traglast 10/40/100), Fenster-Tasten E/Fern
(Zeile ~362-370: Kevin will das Baeren-Inventar gut oeffnen koennen), Sandbox-Kuerzung 12.11. ("komplett uebertrieben" -> heute 13 Regler, F4 hoechstens
1 neuer), F5 spaeter: der Baer fischt und legt Fische in SEIN Inventar und frisst sie selbst (Zeile ~31, ~432-440) -- F4 muss das vorbereiten.
Fenster-Entwurf: ${W}/ui_entwurf/ENTWURF.md (Zeile ~17, ~47 "Load 18.5 / 62" + Knopf Inventory, ~85, ~100-101 offene Fragen) -- das Fenster Variante B
ist mit F3 GEBAUT (Knopf Inventory steht heute grau "Comes with a later version" an seinem Platz).
STAND: Test-Mod ${T} (Git main 9b4ccca = F1 + F1b + F2 Kampf + DE + Aussehen-Knopf + F3 Beduerfnisse/Schlaf/Vertrauen/Herz, alles UNGESPIELT seit F1b).
Berichte des F3-Baus: ${W}/f3/ (PLAN_F3.md, BAU_KERN.md, BAU_OBER.md, GEGEN.md, schnittstelle.md). Register/Hirn: lua/server/BanditsNPCBear*.lua,
Regeln lua/shared/BanditsNPCBear*.lua, Fenster lua/client/ISUI/BanditsNPCBearWindow.lua + WinData/WinParts, Uebernahme ${B}/tools/baer_uebernahme.py,
Naehte ${B}/NAEHTE.md. Kevins ROTE LINIEN (Werkstatt-CLAUDE.md Abschnitt 4): KEIN Gegenstand verloren oder verdoppelt (gerade bei Inventar, Tod,
Koerper-Tausch beim Wachsen/Aussehen/Unstuck, Absturz, Mehrspieler!), kein Kick (AntiCheat), nichts haengt endlos.
ORTE: schreiben NUR unter ${F}/. Lesen: ${W}, ${B}, ${T}, Vanilla ${VAN} (+ projectzomboid.jar daneben; Klassen mit Python zipfile nach ${F}/jar/ ziehen,
javap C:/Users/Kevin/Tools/jdk25/jdk-25.0.4.1+1/bin/javap.exe -c -p), Bandits, NPC Crew ${NC}/42/media/lua und ${NC}/_docs (wie NPC Crew Inventare
ihrer Figuren und Kisten fuehrt: nur lernen, nichts kopieren). Nie rekursiv ueber C:/Users/Kevin oder ein Laufwerk. Kein git, kein Download, nichts in
Test-Mod/NPC Crew. EISERNE REGEL fuer den spaeteren Bau: jeder Engine-Aufruf braucht eine Fundstelle in Vanilla-Lua oder Bandits mit gleichen
Argumenttypen -- die Forschung liefert sie oder sagt klar "nur im Jar" (dann braucht es Kevins Wort je Methode).`

phase('Forschung')
const fo = await agent(`${CTX}

DEINE ROLLE: FORSCHUNG. Klaere mit Belegen:
1. KANN ein lebendes IsoAnimal ein oeffenbares Inventar haben (getInventory/ItemContainer am Tier, wie Vanilla tote Tiere/Schlachtkoerper, Anhaenger,
   Pferde-/Tier-Mods zeigen das?), und wie sieht Vanillas Loot-Fenster einen fremden Container (ISInventoryPage, getContainers, Container in der Naehe,
   "Kofferraum"-Weg der Fahrzeuge)? Welche Wege gibt es, wenn nicht direkt: (a) unsichtbarer Welt-Container, der dem Baeren folgt; (b) Container im
   Register/ModData mit eigenem Fenster (ISInventoryPage mit eigenem ItemContainer, wie NPC Crew es macht?); (c) Vanillas Tier-Inventar (falls es eins
   gibt, z. B. fuer Milch/Wolle/Eier). Je Weg: belegte Aufrufe, Gewichtsgrenze (setCapacity/getCapacityWeight), Speichern/Laden, MP-Sync
   (sendItemsInContainer, Server-Pruefung, AntiCheat-Risiko), Absturz, Koerper-Tausch (heute B.BodySwap/B.PlaceCub erschaffen einen NEUEN Koerper!).
2. Wie macht NPC Crew das Inventar seiner Figuren und Begleiter (wo, wie oeffnet der Spieler es, wie bleibt es beim Tod)? Nur lernen.
3. Was passiert mit dem Inhalt bei Tod des Baeren (Leiche als Container? fallen lassen? im Register halten?), bei "Am Boden", beim Wachsen
   (Junges -> grosser Baer = neue Art), Aussehen-Wechsel, Unstuck, Besitzer offline, Mitfahren im Auto, entladene Gegend?
4. Packtaschen: gibt es in Vanilla/NPC Crew/Bandits Taschen-Gegenstaende, die man einem Tier anlegen koennte (Animal-Attachment, Saettel, Halsband
   in B42?), oder braucht es einen eigenen Gegenstand + Modell (dann Modell-Lauf) -- und wie zeigt man ihn am Tier (Attachment-Punkte des Skeletts)?
5. Traglast heute: wo steht B.CFG.carry / "Can carry up to" (F1/F2) und wie waechst sie; wie zeigt Vanilla Gewicht/Last im Inventar-Kopf.
6. F5-Vorbereitung: wie legt der Server spaeter Fische ins Inventar und wie frisst der Baer daraus (Fuettern-Weg aus F3)?
Ergebnis ${F}/FORSCHUNG_F4.md (mit einer Tabelle "Weg | belegt mit | Risiko fuer rote Linien | Aufwand"). Rueckgabe: Kurzfassung mit Kernbelegen,
klarer Empfehlung fuer EINEN Weg, Luecken und Fragen.`, { label: 'forschung', phase: 'Forschung' })
if (!fo) { return { abbruch: 'Forschung ohne Ergebnis' } }

phase('Plan')
const plan = await agent(`${CTX}

DEINE ROLLE: PLAN. Lies ${F}/FORSCHUNG_F4.md (ganz) und schreibe ${F}/PLAN_F4.md fuer den Bau-Lauf baer-f4 (Form wie ${W}/f3/PLAN_F3.md): gewaehlter Weg mit
Belegen; Traglast je Groesse (taeglich, 10/40/100) + Packtaschen +50 (als eigener Gegenstand? Rezept/Fundort? Modell als eigener spaeterer Modell-Lauf
beschreiben, nicht hier); Oeffnen (Knopf Inventory im Fenster, E-Naehe, Rechtsklick, aus der Ferne ja/nein -- Empfehlung mit Grund); Gewicht ueber der
Grenze (was passiert: kann nichts mehr hineinlegen; wird er langsamer?); Inhalt bei Tod, Am Boden, Wachsen, Aussehen, Unstuck, Absturz, offline, Auto,
entladener Gegend -- jede Stelle mit "kein Gegenstand verloren oder verdoppelt"-Beweis; Fenster ("Load x / y", Knopf Inventory aktiv, Grund wenn grau);
Sandbox (hoechstens 1 neuer Regler "Traglast %", Gruppe; Empfehlung); Texte 8 Sprachen; Bench-Befehle (NCBearBench*); Attrappen-Faelle (vor allem
Verlust/Verdopplung); SP/MP mit Server-Pruefung; Uebernahme/Naehte; F5-Schnittstelle (Fische ablegen, selbst fressen). Bauer-Aufteilung KERN/OBERFLAECHE
mit getrennten Dateien, Workflow-Groesse (hoechstens 10 Agenten). Am Ende EINE kurze Frageliste fuer Kevin (hoechstens 6, je mit Empfehlung, in
einfachen Worten -- er programmiert nicht) plus eine Tabelle "was eine andere Antwort am Bau aendert". Rueckgabe: Kurzfassung + die Frageliste.`,
  { label: 'plan', phase: 'Plan' })

return { fo, plan }
