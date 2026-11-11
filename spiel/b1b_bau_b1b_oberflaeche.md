# Lauf baer-b1b: Bau OBERFLAECHE (B1b Folgen + Namensschild, Futter hinhalten)

Stand 10.11.2026 ~23:50. **Statisch geprueft, nicht gespielt.** Gebaut nach `PLAN_B1B.md` (Abschnitte 1.1, 2, 3.1, 3.2, 5.4-5.6, 6, 8.2)
im Staging `_arbeit/baer_zaehmen/mod/42/media/`. Nichts in die Test-Mod, nach NPC Crew, Vanilla oder Bandits geschrieben; kein Spielstart,
kein Download. shared/ und server/ (KERN) nur gelesen. Abweichungen: `schnittstelle_aenderungen.md`, Abschnitt "B1b OBERFLAECHE".
Fix 2 und Fix 3 sind unberuehrt (liegen in shared/, nicht in meinen Dateien).

---

## 1. Dateien

| Datei (unter `mod/42/media/`) | neu/geaendert | Zeilen | MD5 | Was |
|---|---|---|---|---|
| `lua/client/BanditsNPCBearClient.lua` | geaendert | 324 | `f1396cef17c4f01163f8db0dc40179ed` | `U.EN` +20 Schluessel, `Note_Tamed` neu; `U.LocalName`, `U.CubName` |
| `lua/client/BanditsNPCBearMenu.lua` | geaendert | 434 | `f6d1b7093dad4baf395f28d1a20e48ea` | "Follow me"/"Stay here" (Umschalter), "Name the cub", Welt-Menue "Hold out food for the cub"; `foodLabel` (Futterzeile, von Feed und Hold geteilt) |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | geaendert | 479 | `f0f757b95049644a3b277da498ffce8e` | Namensschild, Anker `B.CFG.tagZ` fuer Balken UND Schild, `wanted` fuer alle Jungen mit Objekt, Schrift Zeile 2, `U.CubsNear` |
| `lua/client/ISUI/BanditsNPCBearNameBox.lua` | **neu** | 76 | `d7b9c92f16ce962e8a135b6a94d34660` | `U.AskName` (Eingabefenster wie Vanillas Tier-Umbenennen) |
| `lua/client/NCBearBenchCub.lua` | geaendert (Testhilfe, wird nie kopiert) | 557 | `0ccf87143d724dd52613f39f47959981` | `NCBear_CubFollow`, `_CubName`, `_CubFollowTest`, `_CubOrphan`, `_CubSweep`; `_CubInfo` mit mode/name; Hilfetext `tagZ`; 3 neue Rechtsklick-Eintraege (jetzt 8) |
| `lua/shared/Translate/<L>/UI.json` x 7 | geaendert | - | siehe 1.1 | 94 Schluessel je Sprache (74 + 20), `Note_Tamed` neu |
| `lua/shared/Translate/<L>/Sandbox.json` x 7 | geaendert | - | siehe 1.1 | + `Sandbox_BanditsNPC_BearFollowMaxDistance` (+ `_tooltip`) |
| `lua/shared/Translate/<L>/IG_UI.json` x 7 | unveraendert (byte-gleich neu geschrieben) | - | wie `staging_dateien.txt` | - |
| `sandbox-options.txt` | geaendert | - | `48e5520a82dd7d6371105f933a1568ad` | Block `option BanditsNPC.BearFollowMaxDistance` (integer 10..60, Vorgabe 40) vor `BearLog`, Form wie `BearCubMinDistance` |

### 1.1 MD5 der Texte
UI.json: CN `402215531c612b984420b134762a8a0d`, EN `1b84eeebcb8d2e4936586be3fa900201`, ES `8dc22eb1ccdd2fe055571485cf84587e`,
FR `a27f55f36add87137f14a8723fe0ed5d`, KO `f35c20b216aa2e2c8a6d0068518e4f28`, PTBR `e08bda84c0a7f9f0455aabf1042107e0`, RU `e88606df35029d9b2d117c010ea3a04c`.
Sandbox.json: CN `1494c5240aa6705c1948823a57fdcd11`, EN `5102e25bc94ad87c89bc6bf24d6c8de7`, ES `0bc4fdf6e0eeff0a664b7f9ee915b455`,
FR `f28ad0534169dcd420fabc650f4dec06`, KO `d5f93443bff87457fd9b23cc702ad888`, PTBR `7ccd0f989e1b067af103be0de7a42122`, RU `1f5534e63a0e28cd15d6db084d2ad3dd`.

### 1.2 Werkzeuge und Tests (nicht im Spiel)
| Datei | Was |
|---|---|
| `ober_werkzeug/texte_b1b.py` (neu) | Quelle der B1b-Texte: laedt `texte.py` UNVERAENDERT, haengt die 20 Schluessel an, ersetzt `Note_Tamed`, fuegt die Sandbox-Option vor `BearLog` ein, schreibt mit `texte.py`s eigenem `build()` (sortiert, Round-Trip `json.dumps(..., indent=4, ensure_ascii=False) + "\n"`, UTF-8 ohne BOM, LF). Gegenprobe: `texte.py` allein erzeugt byte-gleich den B1a-Stand. |
| `attrappe/b1b_ober/run.lua` (neu) | Attrappe Plan 8.2 (Abschnitte 1-9), eigene Kern-Attrappe nach 5.3/5.5 oder mit `kern` die echten shared-Dateien |
| `attrappe/b1b_ober/texte_pruefen_b1b.py` (neu) | alle Pruefungen von `ober/texte_pruefen.py` + Dir-Satzbau je Sprache, `Note_Tamed` nennt `Menu_Follow`, kein `<`/`>` in Texten, Beispielsaetze |
| `attrappe/b1b_ober/belege_b1b.py` (neu) | jede neue Fundstelle der Kommentare gegen die heutigen Vanilla-Dateien |
| `attrappe/ober/run.lua`, `attrappe/ober/texte_pruefen.py` (geaendert, B1a-Attrappe der OBERFLAECHE) | auf das gewollte B1b-Verhalten gezogen (siehe 6) |

---

## 2. Was gebaut ist (Anteil OBERFLAECHE je Auftragspunkt)

1. **Folgen / Bleiben** (Plan 1.1): im Untermenue des eigenen gezaehmten Jungen (nur `v.st == "tame"` UND `v.owner == B.PlayerKey(p)`, nur mit
   Sicht-Eintrag) genau EIN Punkt: bei `B.ModeOf(v) == "stay"` "Follow me" (Tooltip `Menu_FollowTip`; im Fahrzeug grau mit `Why_InCar`), bei
   "follow" "Stay here" (Tooltip `Menu_StayTip`). Klick -> `B.Ask(p, "Mode", { id, mode })` (SP direkt `B.Handle`, MP `sendClientCommand`).
   Fremde, angefuetterte und unbekannte Junge bekommen keinen der neuen Punkte. Entscheiden tut der Schreiber.
2. **Namensschild** (Plan 2): jedes gezaehmte Junge mit Objekt in 20 Kacheln (Deckel 6, naechste zuerst, Balken mitgezaehlt). Zeile 1
   (`UIFont.Small`) Name aus dem Register oder Vorgabe `Tag_Name` ("<Vorname>'s cub" im SP, "<Konto>'s cub" im MP; `__sp` nie als Text);
   Zeile 2 klein und blasser: eigen `Tag_Follow`/`Tag_Stay`, fremd `Tag_Owner` ("belongs to <Konto>"); gerade gezaehmt 5 s gruen blinkend
   "Tamed!". Anker `a:getZ() + B.CFG.tagZ` (Vorgabe 0,18 beim KERN, Rueckfall 0,18), Block waechst nach oben, Zeile 2 sitzt mit der
   Unterkante am Anker, Zeile 1 1 px darueber; der Zaehm-Balken haengt am selben Anker (sonst unveraendert). Je Bild und Schild 2
   Umrechnungen + 4 `drawTextCentre`, kein `getText`, kein Suchlauf, keine neue Tabelle; Texte nur beim Listenbau (hoechstens 1 x/s).
   Kein Sichtfeld-Test. Zeile 2 nimmt `UIFont.NewSmall` nur, wenn sie niedriger ist als `Small` (einmal je Spielstart gefragt).
3. **Umbenennen** (Plan 3.1): "Name the cub" -> `U.AskName`: `ISTextBox` 280 x 180, Titel `Name_Title`, vorbelegt mit dem aktuellen Namen,
   `maxChars = nameMax` (24), `noEmpty`, Pruefer `B.CleanName(text) ~= nil` (Hinweis `Why_NameBad` mit 24), `entry:setMaxTextLength(24)`,
   Joypad-Fokus wie Vanilla. OK -> `B.Ask(p, "Rename", { id, name = roher Text })`; Abbrechen -> nichts. Der Server prueft und verteilt.
4. **Futter hinhalten** (Plan 3.2): Welt-Rechtsklick "Hold out food for the cub" nur, wenn `U.CubsNear(p, lureDist 15)` ein passendes Junges
   kennt (new/shy: jeder; fed: nur gebunden an mich; tame: nur mein eigenes). Untermenue = Futterzeilen wie beim Fuettern; ohne Futter grau
   mit `Menu_NoFood`. Klick -> NUR `ISWorldObjectContextMenu.equip(p, p:getPrimaryHandItem(), food, true, false)` -- kein Hingehen, keine
   Warteschlange geleert, kein Gegenstand erzeugt/vernichtet. Steht vor dem Koeder-Riegel (gilt auch mit Koeder/Jungen aus); im Fahrzeug
   nichts (B1a-Riegel); `test` -> `setTest()`. Vanillas Locken ("ContextMenu_Lure", `eatFromLured`) wird nicht benutzt (Datei-Grep in der Attrappe).
5. **Waisen**: Oberflaeche nur Bench (`NCBear_CubOrphan(n)` = `B.CreateCub` OHNE Eintrag, `NCBear_CubSweep()` = `B.ScanAnimals(nil, true)`).
6. **Texte**: sieben Sprachen, 20 neue Schluessel, `Note_Tamed` mit Hinweis auf den Rechtsklick (nennt `Menu_Follow` der Sprache wortgleich),
   Sandbox-Option `BearFollowMaxDistance` (Name + Tooltip).

---

## 3. Engine-Aufrufe (neu oder an neuem Ort in B1b), je mit Fundstelle (gleiche Argumenttypen)

Alle Fundstellen per `attrappe/b1b_ober/belege_b1b.py` gegen die heutigen Vanilla-Dateien geprueft: **51 von 51 OK**. B1a-Fundstellen der
OBERFLAECHE weiter per `attrappe/ober/belege.py`: **112 von 112 OK**. Jar-only-Aufrufe: **keiner**. Kein `pcall`.

| Aufruf | Datei (Staging) | Fundstelle Vanilla 42.22.2 |
|---|---|---|
| `getSpecificPlayer(0):getDescriptor():getForename()` | Client.lua `U.LocalName` | `client/XpSystem/ISUI/ISCharacterScreen.lua:84` (`self.char:getDescriptor():getForename()`); `getSpecificPlayer(0)` `client/Farming/CFarmingSystem.lua:45` |
| `playerObj:getVehicle()` | Menu.lua `addMode`, Bench | `client/ISUI/Hutch/ISHutchMenu.lua:8` |
| `ISWorldObjectContextMenu.equip(p, p:getPrimaryHandItem(), food, true, false)` | Menu.lua `onHold` | `client/ISUI/Animal/ISAnimalContextMenu.lua:93`; Funktion `client/ISUI/ISWorldObjectContextMenu.lua:2594-2622` |
| `context:addOption`, `ISContextMenu:getNew(context)`, `context:addSubMenu(opt, sub)`, Tooltip/`notAvailable` | Menu.lua `addMode`/`addName`/`addHold` | wie B1a: `ISAnimalContextMenu.lua:48-49`, `:160-163`, `:272-280`; `ISWorldObjectContextMenu.lua:271-273` |
| `ISWorldObjectContextMenu.setTest()` | Menu.lua (Probelauf) | wie B1a `client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81` |
| `getTextManager():getFontHeight(UIFont.NewSmall)` | Hud.lua prerender (einmal) | `client/Entity/ISUI/Controls/ISWidgetTitleHeader.lua:4`; `(UIFont.Small)` `client/ISUI/Animal/ISAnimalUI.lua:4` |
| `self:drawTextCentre(text, x, y, r, g, b, a, UIFont.NewSmall)` | Hud.lua `drawTag` | `client/Foraging/ISSearchManager.lua:148`; mit `UIFont.Small` `client/ISUI/ISUIElement.lua:1280` |
| `isoToScreenX/Y(0, x, y, z)` mit `z = a:getZ() + tagZ` | Hud.lua `draw` | `client/Fishing/TensionUI.lua:11-12` (dort `getZ() + 0.6`) |
| `a:getX()/getY()`, `a:isExistInTheWorld()`, `a:isDead()` | Hud.lua `U.CubsNear` | `client/TimedActions/ISContextualActions.lua:100`; `client/ISUI/Animal/ISAnimalUI.lua:15`; `client/ISUI/Hutch/ISHutchUI.lua:427` |
| `ISTextBox:new(0, 0, 280, 180, Titel, Vorgabe, Ziel, Rueckruf, Spielernummer, param1)` | NameBox.lua | Signatur `client/ISUI/ISTextBox.lua:280`; so mit Spielernummer + param1 `client/ISUI/ISInventoryPage.lua:1912`; Masse `client/ISUI/Animal/ISAnimalUI.lua:460` |
| `modal:initialise()`, `:addToUIManager()`, `.maxChars` | NameBox.lua | `client/ISUI/Animal/ISAnimalUI.lua:461-463`; Wirkung maxChars `client/ISUI/ISTextBox.lua:178-181` |
| `.noEmpty = true` | NameBox.lua | `client/ISUI/Maps/ISWorldMapSymbols.lua:203`; Wirkung `ISTextBox.lua:182-185` |
| `:setValidateFunction(ziel, f)` | NameBox.lua | `client/OptionScreens/CharacterCreationProfession.lua:1297`; Wirkung `ISTextBox.lua:173-177` |
| `:setValidateTooltipText(text)` | NameBox.lua | Vanilla-Lua `ISTextBox.lua:117-119` (setzt nur das Feld, gelesen `:176`), kein Engine-Aufruf |
| `.entry:setMaxTextLength(n)` | NameBox.lua | `client/ISUI/ISMPEditAccount.lua:19` (`ISTextEntryBox`, `client/ISUI/ISTextEntryBox.lua:170-171`; Feld entsteht `ISTextBox.lua:20`) |
| `button.internal`, `button.parent.entry:getText()`, Rueckruf `onclick(ziel, knopf, param1)` | NameBox.lua `onNameClick` | `client/ISUI/Animal/ISAnimalUI.lua:471-473`; `ISTextBox.lua:133-134` |
| `getJoypadFocus(n)`, `modal:centerOnScreen(n)`, `modal.prevFocus`, `setJoypadFocus(n, modal)` | NameBox.lua | `client/ISUI/Animal/ISAnimalUI.lua:464-468` |
| `playerObj:getPlayerNum()` | NameBox.lua | `client/ISUI/Animal/ISAnimalContextMenu.lua:1069` |
| `sendClientCommand` / `B.Ask` (Mode, Rename) | Menu.lua, NameBox.lua | wie B1a (`B.Ask`, `shared/BanditsNPCBear.lua`; Vanilla `client/DebugUIs/DebugContextMenu.lua:956`) |
| Bench: `p:getZ()`, `a:getZ()`, `getCell():getGridSquare(x, y, z)`, `p:getCurrentSquare()`, `getTimestampMs()` | NCBearBenchCub.lua | `client/Fishing/TensionUI.lua:11`; `client/TimedActions/ISContextualActions.lua:100`; `server/Animal/ISPickDungCursor.lua:104`; `client/ISUI/ISWorldObjectContextMenu.lua:112`; `server/Foraging/forageServer.lua:456` |
| `string.byte/sub/len` | (nur im KERN `B.CleanName`) | Lua-Grundbibliothek |

Nicht benutzt: `setCustomName`/`getCustomName`, `pathToLocation`, `setVariable("animalRunning", ...)`, Vanillas Locken, `require "ISUI/ISTextBox"`
(ISTextBox wird erst beim Klick gebraucht; kein Vanilla-Beleg fuer genau dieses `require`, deshalb weggelassen).

---

## 4. Texte je Sprache gezaehlt

| Sprache | UI.json | davon neu B1b | Sandbox.json | IG_UI.json |
|---|---|---|---|---|
| EN | 94 | 20 (+ Note_Tamed geaendert) | 46 (+2) | 6 (unveraendert) |
| PTBR | 94 | 20 (+1) | 46 (+2) | 3 |
| RU | 94 | 20 (+1) | 46 (+2) | 3 |
| KO | 94 | 20 (+1) | 46 (+2) | 3 |
| ES | 94 | 20 (+1) | 46 (+2) | 3 |
| CN | 94 | 20 (+1) | 46 (+2) | 3 |
| FR | 94 | 20 (+1) | 46 (+2) | 3 |

Neu: `Why_NameBad Why_InCar Note_Follow Note_Stay Note_StayCar Note_StayFar Note_StayBehind Note_Renamed Menu_Follow Menu_Stay
Menu_FollowTip Menu_StayTip Menu_Name Name_Title Menu_Hold Menu_HoldTip Tag_Name Tag_Follow Tag_Stay Tag_Owner` (alle `UI_BN_Bear_*`).
Gleiche Schluessel und gleiche Platzhalter in allen sieben Sprachen, sortiert, Round-Trip, UTF-8 ohne BOM, LF. CN: 330 verschiedene
Nicht-ASCII-Zeichen, **alle** in Vanilla-CN (auch `“ ”`). `U.EN` == EN/UI.json (94). Keine Woerter spawn/debug/bench/cheat/test.

Dir-Satzbau (Sichtpruefung, `Dir_NE` eingesetzt; aus `texte_pruefen_b1b.py`):
- EN "Your cub could not keep up. It waits to the north-east." / "Your cub stayed behind to the north-east."
- PTBR "Seu filhote não conseguiu acompanhar. Ele espera ao nordeste." / "Seu filhote ficou para trás, ao nordeste."
- RU "Ваш медвежонок не поспевал за вами. Он ждёт на северо-востоке." / "Ваш медвежонок остался позади, на северо-востоке."
- KO "새끼 곰이 따라오지 못했습니다. 북동쪽에서 기다립니다." / "새끼 곰이 북동쪽에 남았습니다."
- ES "Tu cría no pudo seguirte el ritmo. Te espera al noreste." / "Tu cría se ha quedado atrás, al noreste."
- CN "你的小熊跟不上了。它在东北边等你。" / "你的小熊留在了东北边。"
- FR "Votre ourson n'a pas pu suivre. Il vous attend au nord-est." / "Votre ourson est resté en arrière, au nord-est."
Schild-Beispiele mit "Bruno": EN "Bruno's cub" / "belongs to Bruno"; PTBR "Filhote de Bruno" / "pertence a Bruno"; RU "Медвежонок (Bruno)" /
"хозяин: Bruno"; KO "Bruno의 새끼 곰" / "주인: Bruno"; ES "Cría de Bruno" / "pertenece a Bruno"; CN "Bruno的小熊" / "主人: Bruno";
FR "Ourson de Bruno" / "appartient à Bruno".

---

## 5. Pruefer-Ausgaben (10.11.2026 ~23:45, auf dem Staging)

| Pruefer | Ergebnis |
|---|---|
| `luacheck.py` (Syntax), 5 Client-Dateien | 5 x "1 file(s) checked, 0 failed" |
| `scopecheck.py` | 5 x "0 violation(s)" |
| `localcount.py` (Grenze 200, ab 180 aufteilen) | hoechstens 39 aktiv (Bench `NCBear_CubClean`, B1a), Hud 36 (`rebuild`), Menu 18, Client 13, NameBox 6; insgesamt hoechstens 42 |
| `luacheck_pz.py` (nil-Globals) | 14 x W113, alle erwartet: 3 Aktionsklassen (`Menu.lua:84/95/105`, globale Klassen aus shared/TimedActions, Uebernahme `PZ_ALLOWED`) + 11 in der Bench (eigene `NCBear_*` und `NCBearMenu`; B1a: 8) |
| `luacheck_pz.py --unused` | zusaetzlich 3 x W212 `self` (Maus-Funktionen des Balkens, Absicht, wie B1a), 1 x W212 `player` (Bench-Menue, wie B1a); NameBox, Client: 0 |
| Zeilenenden / Form | alle 5 Lua-Dateien LF, reines ASCII, kein BOM, keine Zeile mit `\` am Ende; 21 JSON LF ohne BOM; `sandbox-options.txt` ASCII/LF |
| `attrappe/b1b_ober/run.lua` | **141 ok, 0 Fehler** (Kern-Attrappe); **131 ok, 0 Fehler** (mit echtem Kern shared, B1b-Stand des KERN-Bauers) |
| `attrappe/ober/run.lua` (B1a) | **116 ok, 0 Fehler** / **117 ok, 0 Fehler** (nach den 4 B1b-Anpassungen, Abschnitt 6) |
| `attrappe/ober/texte_pruefen.py` / `b1b_ober/texte_pruefen_b1b.py` | je **FEHLER gesamt: 0** (94 Schluessel, 20 Sandbox-Optionen == `B.OPTS`) |
| `attrappe/ober/belege.py` / `b1b_ober/belege_b1b.py` | 0 von 112 / 0 von 51 abweichend |
| `attrappe/gesamt/run.lua` (ZUSAMMENBAU) | **260 bestanden, 1 Fehler** -- gewollt, siehe 6 |
| `attrappe/kern/run.lua` (KERN, nur laufen lassen) | 133 bestanden, 0 Fehler |
| `baer/tools/baer_uebernahme.py --staging _arbeit/baer_zaehmen/mod --vor-b5a` (Trockenlauf, schreibt nichts) | **OK -- 0 Fehler, 27 Warnungen**; NameBox als `lua` erkannt; Cheat-Pruefung "Funde: 0"; "Texte aus der Lua: 86 benutzt, fehlen in EN: 0; Ersatztexte 94, wortgleich: ja". Die einzige neue Warnung (Kommentar nennt Testbefehl) betrifft KERN-Dateien (`server/BanditsNPCBearWorld.lua:299`, `shared/BanditsNPCBear.lua:51`) |

Abgedeckt in `b1b_ober/run.lua` (Plan 8.2): 1 Tier-Menue (eigen stay/follow, fremd, angefuettert, v nil + Hello, Fahrzeug grau, MP-Konto);
2 Klick -> genau eine `Mode`-Bitte (SP direkt, MP `sendClientCommand`); 3 Namensfenster (Masse, Spielernummer, param1, maxChars, noEmpty,
setMaxTextLength, Hinweis, Pruefer: Bruno / Leerzeichen / `<b>` / `a%1` / leer / 24 / 25 / Steuerzeichen, OK -> Rename, Abbrechen -> nichts,
Vorbelegung, Joypad, MP); 4 Hold out food (10 Kacheln, Untermenue, equip genau 1 x mit `(p, hand, food, true, false)`, 0 x Warteschlange,
kein Futter grau, 16 / 14,9 Kacheln, fremd zahm / fremd gebunden / eigen gebunden / eigen zahm, Koeder und Junge aus, `test`, Fahrzeug, tot);
5 Schild-Texte (SP Vorname, staying/following sofort nach Sync, benannt, MP fremd/benannt/eigen, Tamed! 5 s, `__sp` in keinem Text);
6 Anker (Unterkante Zeile 2 von Balken und Schild = `isoToScreenY(z + tagZ)`, Zeile 1 1 px darueber, tagZ 0,30 verschiebt beide);
7 Kosten (je Bild 0 x U.T/getText/getCell, 2 Umrechnungen, 4 Texte; 8 Junge -> 6 Schilder); 9 Bench (8 Rechtsklick-Eintraege, MP
"singleplayer only" fuer alle 5 neuen Befehle, SP-Abläufe Follow/Name/FollowTest/Orphan/Sweep, kein `NCBear_` / `setCustomName` /
Vanilla-Locken / `next(` in den Spiel-Dateien). 8 Texte: Python-Pruefer.

---

## 6. Geaenderte Erwartungen (gewollt) und Hinweis fuer den ZUSAMMENBAU

- `attrappe/ober/run.lua` (B1a-Attrappe der OBERFLAECHE, meine Datei): Spieler-Attrappe `getDescriptor`/`getPlayerNum`; "Note ohne t"
  erwartet den neuen `Note_Tamed`-Text; "gerade gezaehmt": Zeile 1 Name, Zeile 2 "Tamed!"; "nach 5 s" jetzt Namensschild (4 Texte,
  "Kate's cub" / "staying") statt 0. `attrappe/ober/texte_pruefen.py`: Plan-Liste +20, NameBox in der Dateiliste.
- **`attrappe/gesamt/run.lua:355`** (ZUSAMMENBAU, nicht von mir geaendert): `eq(#t, 0, "nach 5 s kein Balken mehr am zahmen Jungen")` ist
  durch B1b absichtlich falsch -- dort stehen jetzt 4 Texte (Name + "staying"). Vorschlag: `eq(#t, 4, ...)` und `t[2]`/`t[4]` pruefen.
  Sonst laeuft die Gesamt-Attrappe mit den neuen Client-Dateien durch (260 bestanden).

---

## 7. Offen / ungeprueft

- **Alles ungespielt.** Hoehe des Schilds: `tagZ 0,18` ist gerechnet (FB1B 2.2), nicht gesehen -- Kevin stellt mit `NCBear_CubSet("tagZ", x)` nach.
- Ob `UIFont.NewSmall` im Spiel niedriger ist als `Small`: ungeprueft (der Code vergleicht und faellt sonst auf `Small` zurueck).
  **[Nachbesserung B1b A3, 11.11.: statisch entschieden -- NICHT kleiner. In jeder Vanilla-Sprache laden `font NewSmall` und
  `font Small` dieselbe Datei (`media/fonts/EN/fonts.txt:75-79` und `:93-97`, ebenso CN/CH/JP/KO/PL/RU/TH). Zeile 2 ist gleich
  gross, nur blasser; siehe `nachbesserung_b1b.md`.]**
- `ISTextBox` mit Spielernummer: Lage des Fensters (Maus bzw. Joypad-Mitte) wie Vanillas Container-Umbenennen; ungespielt.
- Namen mit Umlauten/Kyrillisch/Koreanisch/Chinesisch: Pruefer und Laengengrenze haengen an Kahluas `string.len`/`string.byte` (KERN
  `B.CleanName`) und an `entry:getInternalText():len()` (Vanilla) -- ungeprueft im Spiel (FB1B 3).
- "Hold out food" und das Schild kennen nur Junge, deren Objekt der Balken gefunden hat (`S.objs`). Bei geteiltem Bildschirm zeichnet der
  Balken nichts (B1a) und sucht deshalb auch nicht -> dort erscheint "Hold out food" nicht (bekannte Grenze, wie B1a "geteilter Bildschirm: nichts").
- MP: fremde Schilder, `Rename`/`Mode` ueber `sendClientCommand` nur in der Attrappe; MP-Testpunkte in Plan 8.4.
- `Note_Tamed` nennt in RU den Menuenamen in «», in KO in '', in CN in “” -- wortgleich mit `Menu_Follow` (geprueft), Satzwirkung ungespielt.
- Nebenbei: ein versehentlicher, wirkungsloser Lese-Aufruf `git diff --no-index /dev/null /dev/null` lief einmal (schreibt nichts, kein Repo
  beruehrt). Sonst kein git.

Statisch geprueft, nicht gespielt.
