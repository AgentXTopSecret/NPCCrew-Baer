# Lauf baer-b1d: Bau OBERFLAECHE (B1d Wachsen -- Anzeige, Optionen, Meldungen, Texte, Bench)

Stand 11.11.2026 Nachtschicht. **Statisch geprueft, nicht gespielt.** Gebaut nach `PLAN_B1D.md` 1.6, 1.7, 4, 5.1, 6.5-6.9, 7.2 im Staging
`_arbeit/baer_zaehmen/mod/42/media/` (nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein git, kein Spielstart).
Abweichungen und Zusaetze: `schnittstelle_aenderungen.md` Abschnitt "B1d OBERFLAECHE" (12 Punkte, vor dem Abschluss gelesen).

## Kurzfassung
- **Optionen -> Mods -> "NPC Crew: Bear"** bekommt nach "Namensschilder": *Leben* (Aus / Balken / Zahl, Vorgabe Balken), *Ausdauer*
  (Vorgabe Aus), *Alter und Wachstum* (an/aus, Vorgabe an); danach wie bisher die Groesse. Je Spieler, der Server kennt sie nicht.
- **Schild ueber jedem gezaehmten Jungen** (eigen und fremd): bis zu fuenf Zeilen, von unten Ausdauer -> Leben -> Alter -> Zustand -> Name;
  Balken rot (Leben) / gelb (Ausdauer) oder Zahl "Health 92/150"; Alter "Day 12 - half-grown in 3 day(s)" bzw. "Day 100 - full-grown".
  Alles aus -> kein Eintrag. Der Anker waechst mit der gezeigten Groesse (tagZ x sz / 0,35). Zahlen kommen fertig aus der Sicht des Kerns.
- **MP-Client:** setzt im Listenbau (hoechstens 1 x je Sekunde) die Groesse seiner Kopie aus der Sicht nach (B.ApplySize des Kerns);
  im Einzelspieler nie.
- **Meldungen:** "Your bear is half-grown now." (strong / full-grown) und "Your bear's endurance is now level 3." -- unbekannte Werte "?".
- **Texte:** 24 neue UI-Schluessel + 5 Sandbox-Optionen (Titel + Tooltip) in allen 7 Sprachen; `sandbox-options.txt` mit 5 neuen Bloecken
  (2 davon `type = double`), textgleich mit `B.OPTS` des KERNs.
- **Bench (nur SP, wird nie kopiert):** `NCBear_CubGrow(tage)`, `NCBear_CubStats()`, `NCBear_CubXp(key, xp)`, `NCBear_CubHurt(pct)`,
  Rechtsklick "Cub: grow 5 days" / "Cub: stats" (zwoelf Eintraege), CubInfo mit g/hp/hpB/Erfahrung, CubSet-Hilfe mit der B1d-Gruppe.
- Pruefer gruen: vier Lua-Pruefer, LF/ASCII, alle Attrappen (ober, b1b_ober, b1c_ober, b1d_ober je mit Kern-Attrappe und echtem Kern;
  kern, b1b_kern, b1c_kern, gesamt), Text-Pruefer, Belege, Trockenlauf des Uebernahme-Skripts (0 Fehler, 0 Cheat-Funde).

## Dateien

| Datei (unter `_arbeit/baer_zaehmen/`) | Art | Bytes | MD5 | Inhalt |
|---|---|---|---|---|
| `mod/42/media/lua/client/BanditsNPCBearClient.lua` | geaendert (+52 / -2 Zeilen) | 20845 | 576b8e0cd14ac5522212d52c8ca93ebd | `U.EN` + 24 Schluessel, `STAGE_KEY`/`SKILL_KEY`, `U.StageName`, `U.NoteText` "stage"/"skill" |
| `mod/42/media/lua/client/BanditsNPCBearOptions.lua` | geaendert (+28 / -9) | 6918 | 0e4b5a8731c29b643163229e5c5afd99 | `TagHealth`, `TagStamina` (addComboBox + addItem), `TagAge` (addTickBox), Kommentar "spaeter" |
| `mod/42/media/lua/client/ISUI/BanditsNPCBearHud.lua` | geaendert (+189 / -14) | 34879 | 58dadbf1835e403ba4b4270549b9d2ff | Werte-Zeilen, Filter, Lagen, Balken, Anker x Groesse, MP-Client-Probe |
| `mod/42/media/lua/client/NCBearBenchCub.lua` | geaendert (+156 / -1), Testhilfe | 42668 | bd950dece7bd584208c3565e7197100a | Bench 1.7 |
| `mod/42/media/lua/shared/Translate/<L>/UI.json` x 7 | geaendert (+24 je Sprache) | EN 7963 | siehe `texte_pruefen_b1d.py` | Schild, Stufen, Faehigkeiten, Meldungen, Optionen |
| `mod/42/media/lua/shared/Translate/<L>/Sandbox.json` x 7 | geaendert (+10 je Sprache) | EN 6785 | | 5 Optionen + `_tooltip` |
| `mod/42/media/sandbox-options.txt` | geaendert (+40 Zeilen) | 7055 | 5b182174ddd23f8187b3c978ea061ba8 | 5 Bloecke nach BearCallCooldownMinutes, vor BearLog |
| `ober_werkzeug/texte_b1d.py` | **neu** | | | Text-Generator auf `texte_b1c.py`; `write_sbo()` mit `double`; `--basis` |
| `attrappe/b1d_ober/run.lua` | **neu** | | | Attrappe 7.2 (171 / 173 Pruefungen) |
| `attrappe/b1d_ober/texte_pruefen_b1d.py` | **neu** | | | Texte, Sandbox, Optionen-Argumente (mo_text_hits), Dateiform, Werkzeug-Gegenprobe |
| `attrappe/b1d_ober/belege_b1d.py` | **neu** | | | 23 neue Fundstellen gegen die Dateien |
| `attrappe/b1b_ober/run.lua`, `attrappe/b1c_ober/run.lua` | gewollt geaendert ("B1d") | | | 12 statt 10 Bench-Eintraege; 6 statt 3 Eintraege der Optionen-Seite |
| `attrappe/ober/texte_pruefen.py`, `attrappe/b1b_ober/texte_pruefen_b1b.py` | gewollt geaendert ("B1d") | | | Schluesselliste + 24 |
| `schnittstelle_aenderungen.md` | angehaengt | | | Abschnitt "B1d OBERFLAECHE" |

Unveraendert (byte-gleich, geprueft): `client/BanditsNPCBearMenu.lua`, `client/ISUI/BanditsNPCBearMap.lua`, `...Marker.lua`, `...NameBox.lua`,
`IG_UI.json` x 7. `shared/` und `server/` nur gelesen (KERN). `staging_dateien.txt` nicht angefasst (ZUSAMMENBAU).

## Was wie gebaut ist (Plan-Bezug)
- **Optionen (6.8):** auf Dateiebene im vorhandenen Riegel `if PZAPI and PZAPI.ModOptions and PZAPI.ModOptions.create`, kein pcall. Nur
  Schluessel als Text (Uebernahme-Regel `MO_TEXT_ARGS`: 13 Aufrufe, 0 Funde). `getValue` einer Auswahl = Index (1 Aus, 2 Balken, 3 Zahl).
  Gelesen nur ueber `U.Opt` (1 s Zwischenspeicher, Typpruefung); im Hud zusaetzlich auf 1..3 geklemmt (Unsinn in ModOptions.ini -> Vorgabe).
- **Hud (6.6):** im Listenbau einmal `md = { tags, hp, sta, age }`; ein zahmes Junges wird nur gelistet, wenn mindestens eine Zeile
  wirklich etwas zeigt (Zusatz 1). `describeValues` rechnet Fuellbreiten, Texte (U.T) und die Lage jeder Zeile (Pixel ueber dem Anker,
  von unten: Balken `barH + gap2`, Text `h2 + 1`); `drawTag` zeichnet nur noch aus dem Eintrag -- Name zuerst (Text-Reihenfolge wie B1c).
  Ohne Werte in der Sicht ist das Schild Pixel fuer Pixel das von B1c. Anker `a:getZ() + tagZ x e.zk`, `e.zk = sz / tagBase` (gedeckelt 5;
  wilde Junge 1). Je Schild hoechstens 12 Zeichenaufrufe (Plan: <= 14), je Bild kein U.T / U.Opt / B.StatsOf / keine Tabelle.
- **Client-Probe (0.4):** Schritt 1 des Listenbaus, nur `isClient()` und `B.ApplySize` vorhanden, nur gewollte (nicht `ride`), lebende,
  zahme Junge mit Zahl `sz`; einmal je Listenbau. Was geschrieben wird, entscheidet `B.ApplySize` (KERN, nur bei Abweichung > sizeEps).
- **Meldungen (6.5):** `U.NoteText` `t == "stage"` -> `U.T(k, U.StageName(v))`; `t == "skill"` -> `U.T(k, Faehigkeit, floor(w))`; feste
  Listen mit ganzen Schluesseln (Zusatz 2), sonst "?".
- **Bench (1.7):** ueber `ready()` (MP: "singleplayer only") und `myTame`; `NCBear_CubGrow(t)`: `g + t / B.GrowDays()` auf 0..1 geklemmt ->
  `B.GrowSetG`, `B.BrainTick(true)`, `B.PushView`, eine Zeile (Tag, innen/gezeigt, Stufe, naechste Stufe, Leben); `NCBear_CubStats()` druckt
  alle Punkte aus 1.7 (Engine `getSize`/`getHealth` nur, wenn `B.FindAnimal` ein lebendes Tier gibt); `NCBear_CubXp` prueft den Schluessel
  vor dem Jungen (falsch -> Liste "agi vit con fgt fsh nos"); `NCBear_CubHurt(pct)` 1..100 -> `B.GrowSetHp(rec, pct / 100)`.

## Engine-Aufrufe mit Fundstelle (neu in B1d; alle Zeilen per `attrappe/b1d_ober/belege_b1d.py` gegen die Dateien geprueft: 23/23 OK)

| Datei | Aufruf | Fundstelle (gleiche Argumenttypen) | Seite |
|---|---|---|---|
| Options | `o:addComboBox(id, Schluessel, Schluessel)` | Definition `V:client/PZAPI/ModOptions.lua:121` (reines Lua, Tabellen); gespielt in NPC Crew `NC:client/BanditsNPCModOptions.lua:97` (gelernt, nicht kopiert). In Vanilla/Bandits KEIN Aufrufer -- gleiche Lage wie B1c `addTickBox`/`addSlider` (Regel-Frage an Kevin, unten) | Client |
| Options | `opt:addItem(Schluessel[, true])` | `ModOptions.lua:131-136` (ruft `getText(name)` :132 sofort); NC `BanditsNPCModOptions.lua:102` | Client |
| Options | `o:addTickBox("TagAge", Schluessel, true, Schluessel)` | `ModOptions.lua:64` (wie B1c `TagShow`) | Client |
| Options (U.Opt) | `option:getValue()` einer Auswahl -> Index | `ModOptions.lua:137`; gespeichert :272-273, geladen :319-320; Fenster `V:client/OptionScreens/MainOptions.lua:2910-2926` | Client |
| Hud | `isClient()` | `V:client/ISUI/ISWorldObjectContextMenu.lua:1435` | Client |
| Hud | `self:drawRect(x, y, w, h, a, r, g, b)` / `drawRectBorder(...)` / `drawTextCentre(text, x, y, r, g, b, a, UIFont)` | `V:client/ISUI/ISUIElement.lua:1191` / `:1219` / `:1280` (wie B1b/B1c im selben Hud) | Client |
| Hud | `B.ApplySize(obj, sz)` (Kern: `getData():getSize()`/`setSizeForced`) | Belege beim KERN (`shared/BanditsNPCBearStats.lua:330-347`; Client `V:client/ISUI/Animal/ISAnimalUI.lua:31`, `ISButcherHookUI.lua:520`) | MP-Client |
| Bench | `a:getData():getSize()` | `V:client/ISUI/Animal/ISAnimalUI.lua:31` | SP |
| Bench | `a:getHealth()` | `V:client/ISUI/Animal/ISAnimalUI.lua:15` | SP |
| Bench | `p:Say(text)` | `V:client/Entity/ISEntityUI.lua:458` (schon B1a) | SP |
| - | `math.floor`, `tonumber`, `string.format("%.Nf")`, `table.concat` | Lua-Grundbibliothek | - |

Kein `setSizeForced`, `getData`, `setHealth`, `getHealth`, `B.StatsOf`, `pcall(` in Client/Options/Hud (Attrappe und Text-Pruefer
suchen danach). Keine Jar-only-Aufrufe.

## Text-Schluessel je Sprache (gezaehlt von `attrappe/b1d_ober/texte_pruefen_b1d.py`)

| Sprache | UI neu | Sandbox neu (5 x Titel + Tooltip) | UI gesamt | Sandbox gesamt | IG_UI |
|---|---|---|---|---|---|
| EN | 24 | 10 | 133 | 60 | 6 |
| PTBR | 24 | 10 | 133 | 60 | 3 |
| RU | 24 | 10 | 133 | 60 | 3 |
| KO | 24 | 10 | 133 | 60 | 3 |
| ES | 24 | 10 | 133 | 60 | 3 |
| CN | 24 | 10 | 133 | 60 | 3 |
| FR | 24 | 10 | 133 | 60 | 3 |

Gleiche Platzhalter je Schluessel (KO stellt %3 vor %2), kein `<`/`>`, kein Testwort, kein einzelnes `%` in Sandbox-Texten; sortiert,
UTF-8 ohne BOM, LF, Round-Trip `json.dumps(data, indent=4, ensure_ascii=False) + "\n"`; `U.EN` == EN/UI.json (133); CN: 398 verschiedene
Zeichen, alle in Vanilla-CN (ein Vollbreiten-Semikolon wurde durch ein Komma ersetzt). EN wortgleich mit Plan 6.7; Sandbox-EN mit dem
Zusatz "Has no effect until bears can fight." bei BearDodgeMax/BearFightBonusMax (Abweichung 7).

## Pruefer-Ausgaben (alle im Staging, 11.11.2026)
- `luacheck.py` (4 Dateien): 0 failed. `scopecheck.py`: 0 violation(s). `localcount.py`: groesster Wert 48 aktiv / 59 insgesamt (Hud,
  Dateiebene) -- weit unter 180.
- `luacheck_pz.py`: 15 x W113, alle in der Bench (eigene Globale `NCBear_Cub*` in den Menue-Huellen + `NCBearMenu`; B1c-Stand 13, die 2 neuen
  sind `NCBear_CubGrow`/`NCBear_CubStats` in `menuGrow`/`menuStats`). `--unused`: nur die alten `self` der drei Maus-Funktionen und `player`
  der Bench-Huelle (unveraendert seit B1b/B1c).
- Zeilenenden/Form: alle geaenderten und neuen Dateien LF, kein BOM; Lua ASCII, ohne Leerzeichen am Zeilenende, kein `next(`, kein `%a`.
- Attrappen: `ober` 116 / 117 ok, `b1b_ober` 144 / 134, `b1c_ober` 193 / 180, **`b1d_ober` 171 (Kern-Attrappe) / 173 (echter Kern shared,
  inkl. echter `B.ApplySize`, `B.StatsOf`)**, je 0 Fehler; `kern` 136, `b1b_kern` 204, `b1c_kern` 192, `gesamt` 812 bestanden, 0 Fehler.
- `texte_pruefen.py`, `texte_pruefen_b1b.py`, `texte_pruefen_b1c.py`, `texte_pruefen_b1d.py --tmp <ordner>`: je FEHLER gesamt 0 (inkl.
  `texte_b1d.py` byte-gleich mit dem Staging, `--basis` byte-gleich mit `texte_b1c.py`).
- `belege_b1d.py`: abweichend 0 von 23.
- Trockenlauf `python -I baer/tools/baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a` (schreibt nichts): ERGEBNIS OK, 0 Fehler,
  26 Warnungen (alle Altlasten bis B5a + GLB-Clips, wie B1c); Cheat-Funde 0; Ersatztexte 133 wortgleich; 27 Sandbox-Optionen.

## Was die Attrappe b1d_ober beweist (Logik, nicht Engine)
Optionen: Reihenfolge TagShow, TagHealth, TagStamina, TagAge, TagSize; Auswahl-Werte sind Schluessel, Vorgabe-Index 2 / 1, TickBox an;
`addItem` ruft beim Laden genau 6 x `getText` mit Schluesseln; `U.Opt` liefert den Index, Zwischenspeicher 1 s, Seite fehlt -> Vorgaben.
Hud: Balken-Fuellung `floor(64 x 0,61)`, "Health 92/150", "Stamina 40/50", Alter mit/ohne naechste Stufe, nxt 0 -> 1, Reihenfolge und
Pixel-Lagen von unten, TagShow aus + Leben-Balken -> nur der Balken (3 Aufrufe), alles aus -> nicht gelistet (wildes Junges dahinter
bekommt den Platz bei hudMax 1), ohne Werte = B1c-Schild, Anker x 2,14 bei sz 0,75 / Deckel 5 / tagBase-Stellwert, wilde Junge Faktor 1,
Index 7 -> Vorgabe, je Bild 0 U.T/getText/U.Opt, Hud ruft B.StatsOf nie. Probe: SP nie; MP eine je Liste, nie bei ride / ohne sz / wild /
totem Objekt; echter Kern schreibt nur bei Abweichung. Meldungen: alle 6 Faehigkeiten, 3 Stufen, "?" bei Unbekanntem. Bench: MP-Sperre,
Grow(15) -> g 0,15, Grow(-200) -> 0, Grow(500) -> 1, Menue +0,05, D 50 anteilig, Hurt 50/0/150 -> 0,5/0,01/1, Xp-Schluesselliste, Stats-Zeilen,
ohne Tier kein Engine-Aufruf, Info-Zeile, Kern ohne B1d -> klare Zeile.

## Fuer den ZUSAMMENBAU
- `attrappe/gesamt/run.lua` laedt `shared/BanditsNPCBearStats.lua` und `server/BanditsNPCBearGrow.lua` noch nicht. Mit beiden (Probe nur im
  Sitzungs-Ordner, nichts geaendert) fallen 5 alte B1b-Erwartungen, alle gewollt (Vorgabe Alter-Zeile an): `gesamt/run.lua:480`, `:873`
  ("4 Texte" -> 6), `:879`, `:881` (Zustand 12 px hoeher), `:1210` (`#tb == 4`). Vorschlag: in diesen Abschnitten `TagAge` aus und `TagHealth`
  = 1 setzen; die Werte-Zeilen in "19 B1d" pruefen (schnittstelle_aenderungen.md B1d OBERFLAECHE Punkt 11).
- `staging_dateien.txt`: die vier Client-Dateien, 14 JSON, `sandbox-options.txt` geaendert (MD5 oben); Bench weiter "nur Testhilfe".
- xref: alle B1d-Schluessel stehen woertlich im Code (auch `UI_BN_Bear_Skill_*`, `Stage_*`); `Note_Grown`/`Note_SkillUp` kommen vom KERN.

## Offen / ungeprueft (Testpunkte)
- Alles ungespielt. Wie Schild, Balken und Abstaende im Spiel wirken (Groesse 100/150/200), ob der Anker bei 0,75 ueber dem Kopf sitzt
  (Kevins Test 7.4 SP 2-3).
- `addComboBox`/`addItem` haben in Vanilla und Bandits keinen Aufrufer (nur Definition, reines Lua); NPC Crew nutzt sie gespielt. Gleiche
  Regel-Frage wie B1c A3.
- Das Optionen-Fenster zeigt fuer eine Auswahl keinen Tooltip (MainOptions.lua:2910-2933 liest `option.tooltip` nicht) -- die Tip-Texte
  stehen trotzdem in 7 Sprachen.
- `addItem` uebersetzt beim Laden der Datei: nach einem Sprachwechsel im Hauptmenue stehen Aus/Balken/Zahl bis zum Neustart in der alten
  Sprache (Plan 12).
- MP-Client-Probe: ob `setSizeForced` an der Client-Kopie haelt, bis das Tier verloren geht, und keinen Kick ausloest -- ungeprueft (Testpunkt
  PLAN_B1D.md 12, MP 2-3). Geteilter Bildschirm: weiterhin keine Anzeige.
- `type = double` in `sandbox-options.txt`: Beleg laut Plan 5.1 NPC Crew `42/media/sandbox-options.txt:14` (gespielt) -- die Datei liegt
  ausserhalb meiner Suchorte, nicht selbst nachgelesen.
- Ausdauer kommt in der Sicht nur, solange der Kern eine Sitzung hat; nach dem Laden voll (F13).

## Fragen fuer Kevin (Kevin schlaeft; gebaut ist jeweils die Empfehlung)
1. Vorgaben der Anzeige: Leben als Balken an, Ausdauer aus, Alter-Zeile an (F9)? Empfehlung: ja.
2. Namen in den Meldungen: agility, toughness (Leben-Bonus), endurance (Kondition), fighting, fishing, keen nose; Stufen half-grown /
   strong / full-grown (F6, F15)? Empfehlung: ja.
3. Sandbox-Hinweis "Has no effect until bears can fight." bei Ausweichen und Kampf-Bonus, solange es keinen Kampf gibt? Empfehlung: ja.
4. Farben: Leben-Balken rot, Ausdauer gelb, Zahlen leicht getoent, Alter blass wie der Zustand -- ok? Empfehlung: im Spiel ansehen.
5. Regel-Frage wie B1c: zaehlt `addComboBox`/`addItem` (nur Definition in Vanilla, in NPC Crew gespielt) als Beleg? Empfehlung: ja.

Statisch geprueft, nicht gespielt. Lua laedt nur beim Spielstart: nach dem Einbau das Spiel neu starten.
