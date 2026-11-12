# Lauf baer-f1b: GEGENPRUEFUNG nach der Nachbesserung (Befunde A1-A5, B1-B5)

Stand 12.11.2026 ~09:35-10:15. **Statisch geprueft, nicht gespielt.** Geprueft wurde der HEUTIGE Stand im Staging
`_arbeit/baer_zaehmen/mod_f1b/` (67 Dateien), `baer/tools/baer_uebernahme.py`, die Kopie `f1b_werkzeug/baer_uebernahme.py` und
`mod_info_vorschlag_f1b.txt`. Keinem Bericht geglaubt, alles selbst gelaufen. Geschrieben nur diese Datei, `anleitung_f1b_entwurf.md` und
Wegwerf-Dateien im Scratchpad (`C:\Users\Kevin\AppData\Local\Temp\claude\086a7114045651dc\d5933cc7-7f9d-46b2-a3a8-0929595b654b\scratchpad\gegen\`:
`zaehlen.py`, `stich/run.lua`, Probe-Ordner `probe/` und `probe_de/`, Ausgaben `*.txt`). Nichts in der Test-Mod, NPC Crew, Vanilla, Bandits,
`mod/` (F2) oder `mod_f1_fertig/`; kein git, kein Spielstart.

## 0. Urteil

**Bereit fuer Kevins naechsten Einzelspieler-Test.** Kein Blocker. 7 Befunde geschlossen (A1, A2, A3, A4, B1, B2, B3), 3 bewusst offen
(A5, B5: Testpunkte; B4: Einbau-Regel "nur die 16 F1B-Dateien"). Keiner zu Unrecht abgelehnt. Die Nachbesserung hat nichts kaputt gemacht,
das ich finden konnte: geaendert ist nur `client/BanditsNPCBearKey.lua`; alle alten Attrappen geben dieselbe Ausgabe wie nach dem Bau, die
zwei roten Faelle der Prueferin B (P1b, P1g) sind genau die behobenen Befunde.
Einzige rote Zeile der Werkzeuge: das Uebernahme-Skript meldet **1 Fehler "NPC Crew hat Sprachen, die das Skript nicht kennt: DE"** -- kommt
aus NPC Crew (Ordner `shared/Translate/DE` seit 12.11. 09:26, anderer Lauf), nicht aus F1B; haelt nur ein spaeteres `--echt` auf, nicht den Test.

## 1. Je Befund am heutigen Code

S: = Staging `mod_f1b/42/media/lua/`, V: = Vanilla `media/lua/`.

| ID | heute | Beleg |
|---|---|---|
| A1 minor (= B1) | **geschlossen** | `S:client/BanditsNPCBearKey.lua:252-260` `closeBearRadial`: nur wenn die gedrueckte Taste Vanillas Tier-Radial-Taste ist, das Radial offen ist, kein Fahrzeug nutzbar ist und Vanillas nutzbares Tier ein Baer unserer Art (nicht fremd) ist -> `menu:undisplay()`; gerufen nach `U.WinClose` (`:375`) und nach erfolgreichem `U.WinOpen` (`:379`). Zeile fuer Zeile mit Vanilla nachgelesen: Radial geht beim DRUECKEN auf (`V:client/ISUI/ISUIHandler.lua:35-57`), Vanilla meldet sich erst in OnGameStart an (`:101-106`), schliesst beim Loslassen nur ohne Umschalt-Option (`:87-96`) -- unser Hoerer (Datei-Ebene, `Key.lua:388-389`) laeuft vorher. Belege der neuen Aufrufe echt: `getPlayerRadialMenu(0)`/`isReallyVisible()` `ISUIHandler.lua:91-92`, `undisplay()` `ISAnimalContextMenu.lua:1164`. Attrappe `nach_f1b` N1 (mit Vanillas echtem ISUIHandler, Halte- und Umschalt-Modus) 73/0; Pruefer-B-Fall P1b ("Radial UND Fenster offen") ist jetzt rot = behoben. Kuh/fremder Baer/Auto: Radial bleibt (`othersFirst` `:219-246` unveraendert). Mit den Vorgaben (E nah, keine Fern-Taste) greift die neue Stelle nie. |
| A2 minor | **geschlossen (Doku)** | Selbst gelaufen (`alte_pruefer.py`, F1B-Stand): `xref_b1d` 52 / `xref_b1e` 35 Luecken gegen 46 / 29 am F1-Stand. Diff der Ausgaben: **+8** Luecken `UI_BN_Bear_Tag_AgeDone` (7 Sprachen + EN-Wert, gewollt gestrichen), **-2** Luecken der entfernten Tasten-Schluessel `UI_optionscreen_binding_*` = netto +6. Massgeblich `xref_f1`: 0 Luecken, 3 Hinweise (an beiden Staenden). Kleine Ungenauigkeit im Nachbesserungs-Bericht (nennt nur die +6 als AgeDone), kein Fehler. |
| A3 minor | **geschlossen (Prozess-Hinweis, nicht zurueckgebaut)** | Selbst gelaufen: Original `baer_uebernahme.py --vor-b5a` gegen die Test-Mod allein **10 Fehler** (1 DE + 2 alte Tasten-Schluessel + 7 Tasten-Stellen der F1-Key.lua/Window.lua), mit `--staging _arbeit/baer_zaehmen/mod_f1b` **1 Fehler** (nur DE). Inhalt richtig; Folge nur, dass Original und `baer/NAEHTE.md` mit dem Einbau zusammen committet werden muessen (beide ungespeichert im baer-Repo, `git diff --stat`: NAEHTE.md 59, tools/baer_uebernahme.py 82 Zeilen). Vertretbar. |
| A4 minor | **geschlossen** | `mod_info_vorschlag_f1b.txt`: "... auch Rechtsklick am eigenen Baeren Bear window. Es zeigt Kevins Baeren-Symbol, ..." -- Satz vollstaendig; ASCII, 4 Zeilen; alles vor "NEU (F1)" und ab "Modell 12.11." wortgleich mit der heutigen `mod.info` der Test-Mod (beide `mod.info` dort gleich). |
| A5 minor | **offen (Testpunkt), vertretbar** | Kein Aufruf, kein Regelverstoss: Riegel nur Chat und eigenes Namensfeld (`Key.lua:122-130`); dass die Engine bei fokussiertem fremdem Textfeld gar kein OnKeyPressed schickt, steht nur im Jar (`jar_f1/GameKeyboard.txt:53-75`, `Core.currentTextEntryBox.isDoingTextEntry`). Testpunkt in der Anleitung. |
| B1 minor | **geschlossen** | wie A1. |
| B2 minor | **geschlossen** | `Key.lua:346`: Fern-Taste auf Vanillas Interact ohne frische Sicht oder ohne eigenen Baeren (`hasOwn` `:278-281`, dieselben Fragen wie `U.WinOpen` `S:client/ISUI/BanditsNPCBearWindow.lua:640-650`) -> still, kein Halo, kein Hello. Danach gilt der Interact-Riegel auch fuer die Fern-Taste (`:347`). Fern-Taste auf anderer Taste: altes Verhalten (Halo). Pruefer-B-Fall P1g ("3 Halos") jetzt 0 = behoben; eigene Stichprobe G1d (Fern-Taste E: Tuer vorn -> nichts, ohne Tuer -> auf, kein Halo) gruen. Teil (b) (Bett/Stall/Haken ... auf der ganzen Karte) ist nicht vermeidbar -> Frage an Kevin, Empfehlung "Fern-Taste nicht auf E". |
| B3 minor | **geschlossen (Laufzeit ungeprueft)** | `Key.lua:163` `if p:isClimbing() then return true end` im Interact-Riegel; Beleg echt: `self.player:isClimbing()` `V:client/ISUI/ISFitnessUI.lua:260` (IsoPlayer, ohne Argument; auch `V:shared/TimedActions/ISFitnessAction.lua:33`). Ob `isClimbing()` im Loslass-Bild schon wahr ist: ungeprueft -> Testpunkt. |
| B4 major | **offen = Einbau-Regel (kein Code-Fehler), richtig markiert** | Selbst nachgezaehlt: Test-Mod `42/media/models_X/Skinned/NCBearCub.glb` MD5 `d9931d32578f0fec0d5268db71874e5c` (1.221.556 B) und `42/media/textures/Body/NCBearCub.png` `2e627a1babca2df9e79cc484a9f24225` (1.071.919 B), beide 12.11. 07:28:45 = Test-Mod-Commit `cee4890` (baer-junges-fuss: nur GLB, PNG, 2 x mod.info); Staging hat die alten `6c3f0a96...`/`2ee25f24...` (= `mod_f1_fertig`). In `staging_dateien_f1b.txt` als "NICHT KOPIEREN" markiert. Beim Einbau nur die 16 F1B-Dateien kopieren und danach beide MD5 in der Test-Mod gegenpruefen. |
| B5 minor | **offen (Testpunkt), vertretbar** | `S:client/ISUI/BanditsNPCBearHud.lua:714` baut bei geteiltem Bildschirm im Einzelspieler nicht -> Nah-Taste nur ueber den Rueckfall (Vanillas nutzbares Tier, `Key.lua:307-315`). Kevin spielt nicht geteilt; nichts geht verloren, Fern-Taste und Rechtsklick gehen weiter. |

Zu Unrecht abgelehnt: **keiner**. Durch die Nachbesserung kaputt: **nichts gefunden** (Abschnitt 2).

## 2. Selbst gelaufen (Zahlen)

| Pruefung | Ergebnis |
|---|---|
| `luacheck.py` (32 Lua des Stagings) | 32 / 0 failed |
| `scopecheck.py` | 0 violations |
| `localcount.py` | hoechstens **53 aktiv** (Hud Dateiebene), **77 insgesamt** (World :699); Key.lua 31 Dateiebene -- alles unter 180 |
| `luacheck_pz.py` (alle 32) | 20 x W113 = 17 Bench-Befehle (`NCBearBenchCub.lua:1067-1084`, wird nie kopiert) + 3 bekannte Aktionsklassen `Menu.lua:98/:109/:119`. `--unused` auf die 8 geaenderten Spieldateien: nur die 3 W113 + 4 bekannte `self`-W212 (Hud :703-705, Window :487) |
| `luac5.1 -p` | 32 Lua, 0 Fehler |
| Form | 32 Lua ASCII, LF, LF am Ende, kein BOM; 21 JSON byte-gleich mit `json.dumps(sortiert, indent=4, ensure_ascii=False) + "\n"` -- 0 Abweichungen |
| `attrappe/f1b/run.lua` | **216 / 0** (Kern-Attrappe) und **216 / 0** (echter Kern) |
| `attrappe/nach_f1b/run.lua` | **73 / 0** beide Modi |
| `attrappe/pruef_f1b/pruef_b.lua` (Prueferin B, unveraendert) | 73 / 2 beide Modi -- rot nur P1b und P1g, deren Erwartung der alte Fehler ist (`pruef_b.lua:222-223`, `:266-267`) = behoben |
| `alte_laufen.py` am F1B-Stand | 31 Laeufe; Uebersicht und **jede Einzelausgabe byte-gleich** mit `alte_ergebnis_f1b_nach/`; gesamt **2327 / 0** |
| dieselben am F1-Stand (`mod_f1_fertig`) | Unterschiede nur dort, wo F1B gewollt anders ist: `f1_ober` 359 -> 341, `nach_f1_ober` 33 -> 20 (V-Abschnitte am F1B-Stand durch `attrappe/f1b` T11, T20-T22 ersetzt, `f1_ober/run.lua:31-42`, `nach_f1/ober.lua:44-58`), gesamt 2329 -> 2327; alles andere byte-gleich, je 0 Fehler |
| `alte_pruefer.py` | Uebersicht byte-gleich mit dem Nachbesserungs-Stand: alle texte_pruefen* 0, belege* 0 abweichend, `xref_f1` 0 Luecken / 3 Hinweise; `xref_b1b`/`xref_b1c` brechen wie am F1-Stand ab (historisch, unveraendert) |
| `texte_pruefen_f1b.py --tmp` | 0 Fehler: 283 Schluessel je Sprache, U.EN == EN, CN nur Vanilla-Zeichen, Fusszeile hoechstens 575 px (RU) bei Grenze 608 |
| `belege_f1b.py` | **55 / 55**, 209 Fundstellen, 0 ungueltig; dazu 22 Belege selbst in Vanilla nachgelesen (u. a. `ISButtonPrompt.lua:378, :440, :448-494, :513, :695, :846, :851`, `ISVehicleMenu.lua:244-247`, `ModOptions.lua:182-204, :276-282, :326-327`, `MainOptions.lua:2985-2998, :3014, :3545, :3804-3818`, `ISSetKeybindDialog.lua:85-96`, `keyBinding.lua:33, :57, :143`) |
| Kopie-Trockenlauf ohne Schalter | 30 Fehler = 27 Altlasten + 2 ALT_DEFS + **1 DE** |
| Kopie-Trockenlauf `--vor-b5a` | **1 Fehler (DE), 31 Warnungen** |
| Kopie `--probe <scratchpad>/probe --vor-b5a` | 1 Fehler (DE), 31 Warnungen, "NICHT geschrieben" (das Skript schreibt bei Fehler nichts) |
| dieselbe Probe mit einer Scratchpad-Kopie, in der NUR die DE-Zeile Warnung ist | **0 Fehler, 32 Warnungen, 70 Dateien geschrieben**; luacheck/scopecheck/localcount je kopierter Datei ok (31 Lua, Key.lua 31), luacheck_pz 0 + 3 erlaubt; Cheat-Pruefung 9650 Codezeilen, 11 Tasten-Ausnahmen alle benutzt, "Funde: 0"; Texte UI.json 283 neu (3823 -> 4106 je Sprache) |
| `probe_regeln_f1b.py` (Original-Skript) | **20 von 21** -- rot nur "unveraendert" mit genau 1 Fehler = DE; alle 20 Verderbnisse erkannt. (Der Nachbesserungs-Bericht nennt 21/21; die gespeicherte Ausgabe lief offenbar vor 09:26.) |
| Original-Skript | gegen Test-Mod allein 10 Fehler, gegen `mod_f1b` 1 Fehler (DE) -- wie im Bericht |
| `staging_dateien_f1b.txt` gegen die Platte (`zaehlen.py`) | **67 = 67** Dateien, MD5 und Bytes 0 Abweichungen; Status neu nachgerechnet gegen die Test-Mod: **0 neu, 18 ueberschreibt, 49 gleich** -- stimmt. Test-Mod seit Listenstand unveraendert (`find -newer`: nichts). `mod_f1_fertig` != Test-Mod nur in GLB/PNG. Kopfzeile nennt noch "Git main 455ced2"; heute ist es `cee4890` (nur GLB/PNG/mod.info, siehe B4) -- harmlos |

**Welche Test-Mod-Dateien der Einbau ueberschreibt (nachgewiesen):** genau 16, alle mit Test-Mod-MD5 == `mod_f1_fertig`:
`42/media/lua/client/` BanditsNPCBearClient, -Key, -Menu, -Options, -Tags, -WinData, `ISUI/`BanditsNPCBearHud, `ISUI/`BanditsNPCBearWindow
(je `.lua`), `NCBearBenchCub.lua` (Testhilfe, nur Kommentar) und `42/media/lua/shared/Translate/{CN,EN,ES,FR,KO,PTBR,RU}/UI.json`; dazu
`mod.info` + `42/mod.info` aus dem Vorschlag. Keine neue Datei, nichts in `server/`, `shared/*.lua`, Modelle oder Bilder. Einzige `NCBear*`-Datei
darunter ist `NCBearBenchCub.lua` (Bench). Die zwei weiteren "ueberschreibt"-Zeilen (`NCBearCub.glb`, `NCBearCub.png`) NIE kopieren (B4).

## 3. Eigene Stichproben (Attrappe `scratchpad/gegen/stich/run.lua`: Gerippe `attrappe/f1b/run.lua:1-174` woertlich + eigene Faelle)

Ergebnis: **58 ok, 0 Fehler** in beiden Modi (Kern-Attrappe und echter Kern); davon 24 eigene Faelle.

**S1 -- E neben Tuer und Baer, Zeile fuer Zeile** (Vorgabe: Nah-Taste 18 = E, Fern-Taste keine):
`onKey(18)` (`Key.lua:353`): `U.BearKeys` -> 18, nil (`:63-74`) -> isNear; Grundriegel (`:122-130`) frei; keine Sperre nach Schliessen;
`useableReset(p)`; Fenster zu -> `decide` (`:336`): `nearBear` findet den Baeren 2 Kacheln vorn (`:283-316`, 3,5 Kacheln, Blick > 0,2);
`interact = isKey(INTERACT, 18)` wahr (`:341`, V:client/Farming/CFarming_Interact.lua:28); `busy` (`:156-185`): Haltezeit < 0,5 s, kein Cursor,
kein Auto, zielt nicht, keine Leiche, wach, klettert nicht; Blick N nicht schraeg -> f1 = N, b1 = `dir:RotLeft(4)` = S (wie
V:client/ISUI/ISButtonPrompt.lua:483); `doorAt(p, N)` -> `getContextDoorOrWindowOrWindowFrame(N) ~= nil` -> **true -> still**. Vanilla oeffnet die
Tuer allein. Schraege Blicke: meine Tabelle gegen `ISButtonPrompt.lua:448-462` (vorn) und `:468-481` (hinten) verglichen -- alle vier gleich.
Attrappe: G1a Tuer vorn -> kein Fenster, kein Halo, Tuer gefragt; G1b Tuer weg -> auf; G1c Fenster offen + Tuer vorn -> E schliesst (E7, dann
geht zugleich die Tuer auf -- Plan-Frage 9.7); G1d Fern-Taste E, Baer 60 Kacheln weg: mit Tuer nichts, ohne Tuer auf, nie Halo; G1e gar kein Baer:
nichts, **keine** Tuer-Frage an die Engine (nichts Teures ohne Baeren). Alles gruen.

**S2 -- Fern-Taste "keine" bei Tastencode 0:** ModOptions speichert `keybind|BanditsNPCBear|KeyFar|0` (V:client/PZAPI/ModOptions.lua:276-282),
laedt mit `tonumber` (:326-327; "0" ist in Lua wahr, also Wert 0), `getValue` gibt 0 (:191); "Clear" im Tasten-Dialog setzt 0
(V:client/ISUI/ISSetKeybindDialog.lua:85-96); `keyOf` macht aus `k <= 0` nil (`Key.lua:67`), `onKeyStart`/`onKey` vergleichen dann nie.
Attrappe mit Vanillas ECHTEM `PZAPI.ModOptions:load` (und Vanillas `luautils.split`, V:shared/luautils.lua:608-619): Vorgabe -> near 18, far nil;
254 andere Tasten mit Baer 60 Kacheln weg -> 0 Fenster, 0 Halos; ini "KeyNear|0" + "KeyFar|0" -> beide nil, E am Baeren oeffnet nicht, Taste 0
selbst nichts, Fusszeile ohne Taste; ini "KeyFar|65" -> F7 oeffnet/schliesst aus 60 Kacheln. Alles gruen.

## 4. Restbefunde (neu, alle klein, keiner rot)

- **R1** Uebernahme-Skript 1 Fehler DE (NPC Crew `shared/Translate/DE`, 12.11. 09:26, `baer/tools/baer_uebernahme.py:868-873`) -- nicht F1B;
  vor jedem `--echt` klaeren (Frage an Kevin). Mit DE als Warnung ist die Probe gruen (Abschnitt 2).
- **R2** `probe_regeln_f1b` heute 20/21 statt 21/21 (Bericht) -- einziger Grund DE. Doku-Ungenauigkeit.
- **R3** A2-Erklaerung im Nachbesserungs-Bericht ungenau (+8 AgeDone, -2 Tasten-Schluessel = +6). Doku.
- **R4** Fusszeile "E near your bear or Esc closes" (`UI_BN_Bear_Win_HintNear`): E schliesst ein offenes Fenster aus jeder Entfernung (E7), z. B.
  nach Rechtsklick-Oeffnen aus der Ferne. Wortlaut harmlos ungenau.
- **R5** Plan 6.4 Punkt 10 sagt `NCBear_CubGrow(48)` fuer "ausgewachsen"; ab Tag 12 sind das erst Tag 60 (Bench klemmt bei 1,0:
  `S:client/NCBearBenchCub.lua:873-881`). In der Anleitung steht deshalb `NCBear_CubGrow(100)`.
- **R6** Plan 6.4 Punkt 6 schlaegt F7 als Fern-Taste vor -- F7 ist NPC Crews Zonen-Legende (`NC:client/ISUI/BanditsNPCZoneLegend.lua:93`);
  mit NPC Crew an gaebe es zwei Wirkungen. Anleitung nimmt **K** (in Vanilla-`keyBinding.lua`, NPC Crew und Bandits 42.21 nicht belegt).
- **R7** Kopfzeile `staging_dateien_f1b.txt` nennt "Git main 455ced2", die Test-Mod steht auf `cee4890`. Harmlos (Vergleich per MD5).

## 5. Fragen fuer Kevin (gebaut ist jeweils die Empfehlung)

1. **(B1/A1)** Legst du eine Baeren-Taste selbst auf V: am eigenen Baeren geht Vanillas Tier-Radial zu, sobald das Fenster auf- oder zugeht
   (solange du V haeltst, siehst du es kurz). An Kuh, fremdem Baeren und Auto bleibt Vanilla. Mit den Vorgaben passiert das nie. **Gebaut: so.**
2. **(B2)** Fern-Taste auf E: ohne Baeren tut E nichts (keine Meldung); mit Baeren gilt sie ueberall, und vor Bett, Stall, Haken, Vorhang, Seil,
   Leiter passiert beides. **Empfehlung: Fern-Taste nicht auf E legen.**
3. **(neu, DE)** NPC Crew hat seit heute Deutsch. Sollen die Baeren-Texte eine achte Sprache bekommen (eigener kleiner Lauf, Werkstatt-Regel
   "sieben Sprachen" erweitern) oder bleibt DE fuer Baeren-Texte englisch? Bis dahin meldet das Uebernahme-Skript 1 Fehler. Deine Wahl.
4. **(B5)** Geteilter Bildschirm: E findet den Baeren dort nur direkt vor dir. Hinnehmen? **Empfehlung: ja.**
5. **(E7, Plan 9.7)** Ist das Fenster offen, schliesst E es immer -- auch an einer Tuer (dann geht zugleich die Tuer auf). **Gebaut: so.**

## 6. Fuer den Integrator

- Nur die **16** Dateien aus Abschnitt 2 kopieren (+ `mod.info` und `42/mod.info` aus `mod_info_vorschlag_f1b.txt`), nicht waehrend Kevin
  spielt; Zip vorher/nachher; nachzaehlen; danach in der Test-Mod `NCBearCub.glb` = `d9931d32...` und `NCBearCub.png` = `2e627a1b...` pruefen.
- Direkt davor Trockenlauf/Probe wiederholen: erwartet 1 Fehler (DE), sonst 0 / 31.
- `baer/tools/baer_uebernahme.py` und `baer/NAEHTE.md` mit dem Einbau committen; F2-Zusammenfuehren muss die neue Key.lua mitnehmen.
- Anleitung `anleitung_f1b_entwurf.md` nach `baer/spiel/anleitung_f1b.md`; Kevin muss das Spiel NEU starten.

Statisch geprueft, nicht gespielt.
