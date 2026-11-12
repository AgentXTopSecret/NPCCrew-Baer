# Lauf baer-aussehen: GEGENPRUEFUNG der Nachbesserung (Befunde A1-A8, B1-B6)

Stand 12.11.2026 spaetabends. **Statisch geprueft, nicht gespielt.** Ich habe nichts gebaut und keinem Bericht geglaubt: jede Aussage unten habe
ich selbst am Code, mit eigenem Lauf oder eigener Attrappe nachgeprueft. Kurzformen wie in NACHBESSERUNG.md: `S:` = `mod_look/42/media/lua/`,
`V:` = Vanilla `media/lua/`, `UE` = `baer/tools/baer_uebernahme.py`. Alle Ausgaben dieser Pruefung liegen in `aussehen/gegen/`.

## 0. Urteil

**Bereit fuer Kevins Einzelspieler-Test**, sobald der Integrator in EINEM Zug in die Test-Mod kopiert hat (Liste `aussehen/staging_dateien_look.txt`,
beide `mod.info` = `aussehen/mod_info_vorschlag_look.txt`) und Kevin das Spiel mit `-debug` neu startet. Kein offener Blocker.
Alle 14 Befunde: **A1-A8, B1, B2 geschlossen; B3-B6 wie vorgeschlagen gelassen und ehrlich dokumentiert** (Text, Naht, Frage, Testpunkt).
Die Nachbesserung hat **nichts kaputt gemacht**: sie hat genau die 18 Dateien geaendert, die sie nennt, und nur an den Stellen der Befunde
(Vergleich mit der Probe-Kopie vor der Nachbesserung `aussehen/probe/quelle`, 19:58). Kein neuer Engine-Aufruf, kein neues `pcall` im Mod-Code.

## 1. Je Befund

| ID | Geschlossen? | Beleg (selbst geprueft) |
|---|---|---|
| A1 | ja | `S:client/BanditsNPCBearWinData.lua:549-578` zaehlt `others` (Angebote AUSSER dem jetzigen); Grau "only one look" nur bei `others < 1`; `S:client/ISUI/BanditsNPCBearWindow.lua:535-543` oeffnet das Menue nach `e.others`. Traegt der Baer ein `hide`-Aussehen, liefert `B.LookFor` (`S:shared/BanditsNPCBear.lua:646-660`, `B.LookEntry` sieht `hide` nicht) genau diesen Eintrag als `cur`, also zaehlt Classic als Angebot. Klick nur bei hellem Knopf (`Window.lua` `onCmd`: `button.state == "off"` -> return). `ober_nach.lua` selbst gelaufen: 212/0, mit echtem Kern 213/0 |
| A2 | ja | `W/naehte_tabelle.py baer/NAEHTE.md --pruefen`: 0 Mangel; mein eigener Tabellen-Zaehler: alle 5 Tabellen mit gleicher Zellenzahl je Zeile, Leerzeile nach jeder Tabelle; Wort-Vergleich gegen `W/NAEHTE_vor_nachbesserung.md`: NUR Einfuegungen (Kopfzeile, Zeile 43, Absatz "Nachbesserung Aussehen, vom Skript erzwungen"), kein Wort veraendert oder verloren. LF, ASCII |
| A3 | ja | eigene Verderbnisse an einer Kopie (`gegen/ue_eigene_verderbnis.txt`): E1 `local f = B.Opt; f("BearRoamRadius")` -> FEHLER "entfernte Sandbox-Option"; E2 `SandboxVars.BanditsNPC.BearRoamRadius` -> FEHLER Tier-Regel `SandboxVars`; E6 `SandboxVars["BanditsNPC"]` -> FEHLER. Restluecke siehe R2 |
| A4 | ja | E4 Werkbank-Art `ncbeargenfoto` in `B.LOOKS` -> 3 FEHLER (nicht in der kopierten Defs-Datei, in `NCBearBench*Defs.lua` definiert, Tiername fehlt). Unveraendert: "B.LOOKS: 5 Arten ... Fehler: 0" |
| A5 | ja | `W/xref_aussehen.py` selbst gelaufen (`gegen/xref_aussehen.txt`): 104/104 Luecken von `xref_f2.py` einer gewollten Aenderung zugeordnet, AX-1..AX-8 gruen, 0 Luecken. `xref_f2.py` allein weiter rc 1 / 104 (gewollt; steht in NACHBESSERUNG 2) |
| A6 | ja | `aussehen/mod_info_vorschlag_look.txt`: ASCII, 4 Zeilen; nennt nur noch die 12 Optionen (Namen stimmen mit `EN/Sandbox.json`, z. B. "Bear: healing speed", "Taming: speed"); Satz zum Look-Knopf und zur Kuerzung, `NCBear_CubLook(Info)` in den Testhilfen. Achtung Integrator: der alte Ordner `aussehen/mod_info_vorschlag/` ist nur die QUELLE (= Test-Mod heute) |
| A7 | ja | `UI_BN_Bear_Why_BandageOff` in allen 8 `UI.json` ohne Klammerzusatz, `S:client/BanditsNPCBearClient.lua:342` gleich; die uebrigen EN-Texte mit "sandbox" nennen nur Optionen, die bleiben (Bait, Cubs, FleeHits, DamagePercent). `texte_pruefen_nach.py` selbst gelaufen: OK (372 je Sprache) |
| A8 | ja | (a) `BAU_KERN.md:95` verweist fuer die Zeilen jetzt auf `trockenlauf_nach.txt` (dort Grow.lua:714 -- stimmt, `S:server/BanditsNPCBearGrow.lua:714`); (b) beide Werkbank-Kommentare nennen die 5 Arten; (c) Window-Kommentar: `V:client/ISUI/ISContextMenu.lua:70` (onSelect mit param1..10), `:873` (addOption), `V:client/ISUI/Animal/ISAnimalContextMenu.lua:75` / `:377` (zwei Werte) -- selbst nachgelesen, stimmt |
| B1 | ja | `S:server/BanditsNPCBearGrow.lua:666-671`: Stempel (`B.CallStamp`) direkt VOR `B.PlaceCub`, bei `n == nil` zurueck (`B.CallUnstamp`, `S:server/BanditsNPCBearRide.lua:329-332`); `S:server/BanditsNPCBearLook.lua` stempelt nicht mehr. Meine Stichprobe S2a (Fehler in `B.RemoveCub`): 2 Koerper, Uhr laeuft, weitere Look- UND Unstuck-Bitten abgelehnt, kein dritter Koerper; Besitzer 36 Kacheln weg -> genau EIN Koerper. Tier-Regel `CallUnstamp` greift (E5) |
| B2 | ja | `B.LookFromBody` (`S:server/BanditsNPCBearHeal.lua:134-143`) aus `bind` (`:158`) und dem AnimalID-Weg (`S:server/BanditsNPCBearWorld.lua:816-817`); Art nur ueber `B.BodyKind` -> `getAnimalType` (Beleg `V:client/ISUI/Animal/ISAnimalUI.lua:65`). Standard-Koerper aendert den Wunsch nie, `LOOK_NEAR` bleibt. `kern_nach.lua` selbst: 27/0 (K5, K6a-c) |
| B3 | gelassen (ok) | nur Text fuer Kevin; NAEHTE Zeile 41 (Regel fuer F3) |
| B4 | gelassen (ok) | vorbestehend; NAEHTE Zeile 43; meine Stichprobe S2c zeigt es genau so: Register neu + Zelle alt (MP) -> 2 Koerper, solange der Besitzer nah ist, danach EINER, Leben 0,5 bleibt |
| B5 | gelassen (ok) | `S:server/BanditsNPCBearRide.lua:28` (`B._callAt` nie gespeichert); Frage an Kevin; steht auch ehrlich im mod.info-Vorschlag ("nach dem Laden ist sie frei") |
| B6 | gelassen (ok) | Testpunkt; der Schreiber entscheidet richtig (`S:server/BanditsNPCBearGrow.lua:569-575`) |

## 2. Selbst gelaufen (nach der letzten Aenderung)

| Pruefung | Ergebnis | Datei in `aussehen/gegen/` |
|---|---|---|
| `attrappe/aussehen_kern/run.lua` | 148 / 0 | `kern.txt` |
| `attrappe/aussehen_ober/run.lua` ohne / mit Kern | 191 / 0, 192 / 0 | `ober.txt`, `ober_kern.txt` |
| `attrappe/aussehen_pruef/run.lua` | 32 / 0, 5 Befunde (die gewollten) | `pruef.txt` |
| `aussehen/attrappe_nach/kern_nach.lua`, `ober_nach.lua` (+ Kern) | 27 / 0; 212 / 0, 213 / 0 | `kern_nach.txt`, `ober_nach*.txt` |
| Alle alten Attrappen gegen `mod_look` (Kopie des Laeufers, nur Temp-Ordner gebogen) | Zusammenfassung **zeilengleich** mit der der Bauer (`attrappe/aussehen_kern/alte_nach.txt`) und der Nachbesserung | `alte.txt`, `alte/` |
| Dieselben mit Bruecke SandboxVars -> B.CFG (`alt_umgestellt` KERN / OBERFLAECHE) | KERN wie `alte_vorher.txt` (gesamt **3333 / 0**); OBERFLAECHE alle 10 "wie vorher" | `alt_umgestellt_kern*`, `alt_umgestellt_ober*` |
| luacheck / scopecheck / localcount / luacheck_pz / luac -p (60 Lua) | 0 failed / 0 / Spitze 52 aktiv, 77 insgesamt / 48 W113 = 41 Werkbank + 7 erlaubte Aktionsklassen / 0 | `pruefer.txt` |
| `UE --staging mod_look` (Trockenlauf) | 0 Fehler, 2 Warnungen; **identisch** mit `aussehen/trockenlauf_nach.txt` | `trockenlauf.txt` |
| `UE --probe aussehen/gegen/probe --staging mod_look` | 0 Fehler, 2 Warnungen, langcheck 0 Fehler / 12 Hinweise; NPC-Crew-Seite ohne jede Werkbank-Datei; Ausgabe gleich `probe_nach_ausgabe.txt` | `probe_ausgabe.txt`, `probe/` (73 MB, darf weg) |
| Alte UE-Regelprobe F2 (`probe_regeln_nach.py`) | 16 / 16 | `probe_regeln.txt` |
| Eigene UE-Verderbnisse E1-E6 | 5 / 5 erkannt, E3 = Restluecke R2 | `ue_eigene_verderbnis.py/.txt` |
| `W/xref_aussehen.py` | 0 Luecken | `xref_aussehen.txt` |
| `staging_dateien_look.txt` gegen die Platte (eigenes Skript, MD5 + Bytes je Datei, Status gegen die Test-Mod heute) | 143 Zeilen = 143 Dateien, **4 neu, 55 ueberschreibt, 84 gleich, 0 Abweichungen**; die Modell-Dateien `NCBear.*`, `NCBearGen.*`, `NCBearGenFoto.png`, `NCBearCub.*` sind heute byte-gleich mit der Test-Mod | `zaehle_staging.py/.txt` |

## 3. Zwei eigene Stichproben (`gegen/stichproben.lua`, 25 / 0)

**S1 Tausch mit halbem Leben** (SP UND MP-Server, grosser Baer, Leben 0,5, Ausdauer 0,3, Verband laeuft, 7 Kills, Name):
Look "Natural" -> Art `ncbeargrowngenfoto`, EIN Koerper, Register und Koerper 0,5, Ausdauer 0,3, Verband/Kills/Name/Besitzer/Zaehmung/
Faehigkeiten gleich, gen + 1, neue AnimalID, neue Kachel = die eigene. **Vier Spielstunden danach ist das Leben auf die Stelle genau wie bei
einem Baeren ohne Tausch (0,615 = Kontrolle).** Engine-Heilung am alten Koerper (0,9) wird zurueckgenommen, ein fremder Verlust (0,2) nicht
uebernommen: der neue Koerper hat 0,5. Kein Heilen ueber den Knopf.

**S2 Absturz mitten im Tausch:**
- S2a Lua-Fehler in `B.RemoveCub` (neuer Koerper da, alter noch da): Uhr laeuft, Look und Unstuck abgelehnt, kein dritter Koerper; neuer Koerper
  0,5. Solange Kevin daneben steht, sind es zwei Baeren (dokumentiert, NAEHTE 43); 36 Kacheln weg -> genau EINER (der neue), Eintrag heil.
- S2b Lua-Fehler in `B.GrowBody` (der neue Koerper behaelt das frische Engine-Leben 1,0): **ein Hirn-Takt spaeter steht er wieder auf 0,5
  (`B.BodyHp` nimmt den Anstieg zurueck), das Register wird nicht geheilt** -- auch ein Absturz heilt nicht.
- S2c MP, Register NACH dem Tausch gespeichert, Zelle VOR dem Tausch: Eintrag da, Leben 0,5, Wunsch "gen"; zwei Koerper solange Kevin nah ist
  (B4, vorbestehend), danach EINER (der neue, gen 3). Kein Baer verloren.

## 4. Restbefunde (alle klein, keiner blockiert)

- **R1** (Kommentar, Werkbank, nie kopiert): `S:shared/NCBearBenchGenDefs.lua:11` sagt noch "eigenem Modell (scripts/NCBearBenchGen.txt,
  NCBearGen_Body)" -- der Block steht seit diesem Lauf in `scripts/nc_bear_look.txt` (`scripts/NCBearBenchGen.txt:9` sagt es richtig).
- **R2** (Pruefer-Luecke, klein): ein zusammengesetzter Optionsname (`B.Opt("Bear" .. "RoamRadius")`, E3) geht durch das Uebernahme-Skript.
  Zur Laufzeit faengt ihn `B.Opt` (`S:shared/BanditsNPCBear.lua:309-314`: Fehlerzeile + nil) -- er liest also nie einen alten Wert.
- **R3** (vorbestehend seit HEAD, Darstellung): die Tabelle "Sandbox-Seiten" (`baer/NAEHTE.md:372`) beginnt direkt nach einer Textzeile ohne
  Leerzeile; `naehte_tabelle.py` prueft das nicht. GitHub zeigt sie trotzdem als Tabelle (ungeprueft fuer andere Anzeigen).
- **R4** (bekannt, NAEHTE 43): `B.HandleCall` (Unstuck) stempelt seine Uhr weiter erst nach dem neuen Koerper -- bei einem Lua-Fehler mitten
  in Unstuck koennte jeder Klick einen weiteren Koerper machen (altes, gespieltes F1-Muster; der Look-Knopf ist jetzt sicher).
- **R5** (Hinweis): die alten Attrappen sind ROH gegen `mod_look` an mehreren Stellen rot (z. B. `kern_run` 24, `gesamt_run` bricht ab); das sind
  alles Faelle, die entfernte Optionen ueber SandboxVars setzen -- mit der Bruecke `alt_umgestellt` sind es genau die Ergebnisse von vorher.
  Wer nur die rohe Liste liest, sieht rot: immer `alt_umgestellt` daneben lesen.
- **R6** (Hinweis): beim Lesen von `W/mod_info_look.py` habe ich es versehentlich einmal ausgefuehrt; es schrieb `aussehen/mod_info_vorschlag_look.txt`
  neu (21:11). Das Werkzeug ist deterministisch, seine Quelle ist unveraendert (= Test-Mod `mod.info`, MD5 46e0f18d), Groesse gleich 11064 --
  der Inhalt ist derselbe.

## 5. Fragen an Kevin (aus PLAN 18 / NACHBESSERUNG 4, weiter offen)

- **K2** Generator-Junges ("Brown" beim Jungen) schon waehlbar lassen? Es geht etwa ein Drittel langsamer und du hast es noch nie gesehen.
  Gefaellt es dir nicht: vor dem ersten echten Spielstand streichen, danach nur noch verstecken (`hide`).
- **B5** Die gemeinsame Wartezeit von Look und Unstuck ist nach Speichern + Laden sofort frei (kein Heilen, kein Wegzaubern, nur Zeit). So lassen?
- **K1** Namen der Aussehen: EN Classic / Brown / Natural, DE Klassisch / Braun / Natur -- passt das?

## 6. Was ich geschrieben habe

Nur in `aussehen/`: dieser Bericht, `anleitung_entwurf.md`, Ordner `gegen/` (Ausgaben, `stichproben.lua`, `zaehle_staging.py`,
`ue_eigene_verderbnis.py`, Kopien der Laeufer mit gebogenem Temp-Ordner, `probe/`, `NAEHTE_head.md` = `git show HEAD:NAEHTE.md` zum Vergleich).
Dazu R6. Nichts in `mod_look/`, Test-Mod, NPC Crew, Vanilla, Bandits, `attrappe/`, `UE` oder `baer/NAEHTE.md`. Kein Commit, kein Download,
kein Spielstart; git nur lesend (`status`, `show HEAD:NAEHTE.md`).
