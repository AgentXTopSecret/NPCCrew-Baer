
## OBERFLAECHE, Eintrag 1 (10.11.2026, vor dem Bau; ZUSATZ, keine Abweichung)

- **Eigener Unterraum `B.UI`** (`BanditsNPC.Bear.UI = BanditsNPC.Bear.UI or {}`): alle Helfer, die die OBERFLAECHE zwischen ihren
  eigenen Dateien teilt, liegen NUR dort (z. B. `B.UI.NoteText`, `B.UI.WhyText`, `B.UI.WaitText`, `B.UI.Fresh`, `B.UI.AskHello`,
  `B.UI.EN`). Grund: der KERN entsteht gleichzeitig; so kann kein Helfer der OBERFLAECHE einen Namen des KERNs ueberschreiben.
  Bitte an den KERN: `B.UI` nicht belegen. Der KERN braucht nichts daraus.
- Direkt an `B` legt die OBERFLAECHE nur die zwei Funktionen aus Plan 6.2.4: `B.ShowNote(player, note)` (Datei 13) und `B.OnView()`
  (Datei 15). Sonst nichts.
- Die Schnittstelle 6.2 wird woertlich benutzt (Stand dieses Eintrags: keine Abweichung).

## KERN, Eintrag 1 (10.11.2026 abends, nach dem Bau; Zusaetze und zwei kleine Abweichungen)

Die Schnittstelle 6.2 ist woertlich gebaut (Namen, Parameter, Rueckgaben, Befehle, Sicht, Note-Form). `B.UI` belegt der KERN nicht.
Zusaetze und Abweichungen, alle rueckwaertsvertraeglich:

1. **Wahlfreie Zusatz-Parameter:** `B.CheckBait(slots, now)` (fehlt `now`, nimmt sie `B.Now()`; die Sperre braucht die Zeit);
   `B.BaitDawn(bait, now, players)` (`players` wahlfrei); `B.ScanAnimals(players)` (wahlfrei). Aufrufe nach Plan bleiben gueltig.
2. **`B.Decide` gibt zusaetzlich `rule`** (Nummer der Regel 1..9) zurueck: der Hirn-Takt merkt sich damit die Neugier-Zeit, der Test prueft jede Regel.
3. **Weitere Kern-Funktionen an `B`** (nicht in 6.2, die OBERFLAECHE braucht sie nicht; die Bench darf sie im SP rufen):
   shared: `B.LogActive`, `B.DistXY`, `B.Round1`, `B.ReleaseBond`; server: `B.InitRegistry`, `B.Ses`, `B.Touch(rec, key)` (merkt "geaendert",
   die Bench ruft es schon), `B.NewRec`, `B.CountRecs`, `B.CountWild`, `B.CountBaits`, `B.CleanLocks`, `B.BaitOf`, `B.NewBait`, `B.DropBait`,
   `B.FlushViews(players, sent)`, `B.PlayerByKey`, `B.IsNight`, `B.AreaLoaded`, `B.SeenInSP`, `B.NearestPlayerDist`, `B.FreeSquareNear`,
   `B.ScanAnimals`, `B.MoveWatch`. Felder: `B._s`, `B._dirty`, `B._rev`, `B._brainAt`, `B._scanAt`, `B._live`, `B._pp`, `B._sig`, `B._errAt`.
   Mehr Felder in `B.CFG` (reach, baitReach, baitRing, mateDist, hintDist, stillEps, viewMax, loadRing, orphanMs, maxDtH), gleiche Tabelle.
4. **`B.OnCubDead(rec)` (Plan 5.5) gibt es nicht als eigene Funktion:** der Tod laeuft ueber `B.Close(rec, "dead")` (6.2.3), das die Sperre setzt.
5. **Faelliges Junges (`goneP`) belegt keinen Platz mehr** (Abweichung vom Wortlaut 4.1): `B.SlotsOf` zaehlt es nicht als `wild`,
   `B.CountWild` nicht fuer den Welt-Deckel. Grund: ein faelliges Junges, dessen Gegend nie wieder geladen wird, haette den Platz des
   Finders sonst fuer immer blockiert. Dazu: faellig UND Gegend nicht geladen -> Eintrag wird geschlossen ("vanish"); ein spaeter geladenes
   Tier, dessen Spiegel auf einen geschlossenen Eintrag zeigt und `st` new/shy traegt, entfernt `B.ScanAnimals` ueber `B.RemoveCub`, sobald
   niemand in 25 Kacheln ist und es keiner sieht. Fuer die OBERFLAECHE aendert sich nichts.
6. **Gruende ausserhalb der Liste 6.2.8 gibt es in Notes nicht.** `B.AppearFor` gibt als `why` ausser Textschluesseln auch kurze
   Engine-Gruende zurueck (`"noreg"`, `"nodef"`, `"noanimal"`, `"notinworld"`, `"full"`, `"noargs"`, `"nowriter"`) -- nur fuer Bench und Log.
   Koeder: zu weit / Kachel nicht geladen -> `Why_Far`; Koeder-Deckel 16 voll -> `Why_Full`.
7. **`Bait_Came`** geht an den Besitzer in dem Moment, in dem das Junge am Platz erscheint (falls er online ist), danach `Note_Seen`, wenn er in 15 Kacheln kommt.
8. **`B.Players()`-Eintraege** tragen zusaetzlich `uid` (trennt lokale Spieler im geteilten Bildschirm, `"__sp#0"`) und `nr` (Spielernummer, nur SP).
9. **Register-Eintrag** traegt zusaetzlich `nr` (laufende Nummer, wie in `id`). Sonst wie 4.1.

## OBERFLAECHE, Eintrag 2 (10.11.2026 ~20:40, nach dem Bau; keine Abweichung, zwei Hinweise)

- Gebaut gegen 6.2 woertlich; die Zusaetze aus "KERN, Eintrag 1" sind vertraeglich (`B.CheckBait(me)` ohne `now` im Menue,
  `B.Touch()` ohne Argumente in der Bench = "alles geaendert", `B.AppearFor`-Kurzgruende zeigt die Bench als Text).
- Hinweis 1: die Texte `UI_BN_Bear_Dir_*` sind NUR fuer `Note_Heard` gebaut (RU im Praepositiv, "severe", FR mit Praeposition
  "au nord"/"a l'est", der Satz in `Note_Heard` traegt sie nicht mehr). Wer `Dir_*` spaeter anderswo einsetzt, braucht eigene Schluessel.
- Hinweis 2: die Bench prueft zuerst `B.IsSP()` (MP-Client: "singleplayer only"), erst dann `B.Reg`.

## NACHBESSERUNG, Eintrag 3 (10.11.2026, nach Pruefer A und B; beide Seiten geaendert)

- **Hello traegt eine nicht leere Tabelle** `{ v = 1 }` (OBERFLAECHE `client/BanditsNPCBearClient.lua` sendHello). Grund: die Engine
  schickt eine LEERE Tabelle als nil (Befund B1). Der KERN nimmt bei jeder Bitte `args == nil` wie `{}` (`onClientCommand`) und
  schickt einem Spieler im ersten Hirn-Takt, in dem er da ist, von sich aus eine Sicht (`pushNewSights`). Hello liest weiter kein Feld.
- **`B.CountWild(online)`** hat ein wahlfreies Argument (Satz `{ [Schluessel] = true }`, nur Kern-intern; ohne Argument wie bisher).
- **Zeitaktionen Fuettern/Streicheln** haben `serverStart()` / `serverStop()` (Sperre am Tier am Server); `complete()` loest die Sperre
  nach dem Kern-Aufruf und gibt dessen Ergebnis zurueck (Befund A2).
- **Neue Stellwerte** in `B.CFG`: `fedMissH = 1.0` (Spielstunden, B3), `missScanMul = 6` (B6). Register-Eintrag traegt zusaetzlich
  `missAt` (Weltstunde des ersten Fehlversuchs, nil = keiner).
- **B.Decide Regel 7** haelt ein angefuettertes / zahmes Junges auch, wenn bond / Besitzer naeher als `B.CFG.reach` steht (B7).
- HUD (OBERFLAECHE): dritte Suchlauf-Stufe `SCAN_IDLE_MS = 30000` nach `SCAN_SLOW_N = 17` vergeblichen Laeufen (B6). Keine neuen Texte.
