# Lauf baer-b1b: PLAN -- Folgen, Bleiben, Namensschild, Umbenennen, Futter hinhalten, Waisen (B1b)

Stand 10.11.2026 spaet. **Nur geplant: nichts gebaut, nichts gespielt.** Spiel 42.22.2. Verbindlich fuer zwei Bauer (KERN, OBERFLAECHE,
gleichzeitig, getrennte Dateien) und den ZUSAMMENBAU danach. Baut auf dem Staging `_arbeit/baer_zaehmen/mod/` (B1a + Fix 1-3) auf.
Kurzformen: `FB1B x.y` = `forschung_b1b.md` Abschnitt x.y; `PZ x.y` = `PLAN_ZAEHMEN.md`; `FE x.y` = `forschung_engine.md`;
`S:` = Staging `mod/42/media/lua/`; `V:` = Vanilla `media/lua/` (42.22.2); `ENT` = `baer/begleiter/ENTSCHEIDUNGEN.md`; `B` = `BanditsNPC.Bear`.

Kevins Worte, auf denen der Plan steht (ENT, "Erster Spieltest B1a", und Auftrag): *"kann jz nichtmehr mit dem machen also da steht auch
nicht ueber den baeren das es meiner ist"* -- auf die Frage, was zuerst kommt: *"Folgen + Namensschild"*. Dazu N5 (Waise des ersten
Versuchs), N6/N8 (*"man kann garkein essen in die hand nehmen?"*, Fuettern *"ging mit hinterherennen"*), der Balken *zu hoch* ueber dem
kleinen Jungen (STAND.md ~22:50), Streicheln bleibt (*"lass das einfach so"*). Alles andere hier ist VORSCHLAG (Stellwert, Sandbox oder Frage in 9).

**Nicht zurueckbauen:** Fix 2 (`tHas` in `B.T`, `S:shared/BanditsNPCBear.lua:238-261`), Fix 3 (Streichel-Ton `petting = PetAnimalCalf`,
`S:shared/BanditsNPCBearDefs.lua`, `S:shared/TimedActions/BanditsNPCBearPetAction.lua`). Streicheln (Haltung, Abstand) bleibt unveraendert.

---

## 0. Entscheidungen des Planers (gelten fuer alle)

**0.1 Bewegung nur ueber `animal:fleeTo(sq)` -- das Junge RENNT beim Folgen immer.** `fleeTo` ist laut Jar `animalRunning = true` +
`pathToLocation` (FB1B 0.2), in B1a gespielt (*"das rennt weg"*). Damit braucht B1b **keinen** neuen Engine-Weg: `pathToLocation` (Kevins
Ausnahme) wird NICHT gebraucht, `setVariable("animalRunning", false)` (Grenzfall, FB1B 1.1/1.3) wird NICHT benutzt. Grund zusaetzlich: das
Platzhalter-Junge geht nur ~0,5 Kacheln/s, rennt ~2,5 Kacheln/s, der Spieler geht ~2,3 (FB1B 0.3) -- zum Mitgehen muss es ohnehin rennen.
"Rennt mit, wenn er rennt" gilt also immer; einen sprintenden Besitzer verliert es (dann greift der Deckel 1.3). Gehen in der Naehe ist
Frage 1 (Kevins Wort je Methode, erst mit den Clips des neuen Modells sinnvoll).

**0.2 Folgen rechnet der SCHREIBER im Hirn-Takt** (SP: das eine Programm; MP: der Server), wie B1a die Flucht (FB1B 0.1). Kein Client
befiehlt dem Tier etwas. Der Client bittet nur ("Mode", "Rename") und zeigt an.

**0.3 Der Name lebt NUR im Register (Weg A aus FB1B 3).** Kein `setCustomName`, kein `getCustomName`. Grund: Vanillas "Animal info" darf
jeder nicht wilde Tier umbenennen und der Server-Befehl `animal.rename` prueft keinen Besitz (FB1B 0.6) -- die Wahrheit muss beim
Register bleiben; ein Spiegel am Tier braeuchte einen Rueckdreh-Takt und ueberschriebe Kevins eigene Vanilla-Umbenennung still. Folge
(bekannte Grenze): Vanillas Tier-Info und der Untermenue-Titel zeigen weiter den Vanilla-Namen ("Bear cub"); unser Schild zeigt den
echten Namen. Spiegeln ist Frage 2 (spaeter mit dem Baeren-Fenster).

**0.4 Nach dem Zaehmen steht das Junge auf "Bleiben"** (Feld `mode` fehlt = "stay"; alte Spielstaende passen ohne Umbau). "Follow me"
schaltet um. Die Zaehm-Meldung bekommt einen Satz dazu, der auf den Rechtsklick hinweist (6.2 Texte).

**0.5 Vanillas Locken bleibt aus** ("ContextMenu_Lure", `eatFromLured`, FB1B 4): "Futter hinhalten" nimmt das Stueck nur in die Hand
(`ISWorldObjectContextMenu.equip`, Beleg 8), alles Weitere macht die bestehende Regel des Schreibers (`B.Decide` Regeln 2/3/6/7).

**0.6 Waisen (N5) raeumt `B.ScanAnimals`**, plus ein seltener eigener Suchlauf. Drei Riegel gegen Fehlgriffe (4.2), weil ein frisch
erzeugtes Junges in B1a im ersten Bild noch KEINEN Spiegel bekommt (`B.Commit` schreibt ihn nur bei `isExistInTheWorld()`,
`S:server/BanditsNPCBearRegistry.lua:264`, und das ist direkt nach `addToWorld` falsch -- Lehre aus Fix 1) -- ohne Riegel waere es eine "Waise".

**0.7 Aufteilung:** KERN = `shared/` (ohne Translate) + `server/`; OBERFLAECHE = `client/` + alle Texte + `sandbox-options.txt`. Je eine
neue Datei je Bauer (5.1). Keine Datei fuer beide. Zeitaktionen, Defs, Food, Crew, Modell, Skript bleiben unberuehrt.

**0.8 Nicht in B1b:** Wachsen, Kampf/Gegenwehr, Inventar, Beduerfnisse, Schlafen, Baeren-Fenster (V), Ein/Aus des Schilds je Spieler
(ENT:103/106, gehoert ins Fenster), Mitfahren im Auto, Befehle an NPC-Crew-Figuren, Umbenennen der alten `NCBear*`-Dateien.

---

## 1. Verhalten Schritt fuer Schritt

### 1.1 Umschalten (Rechtsklick am eigenen, gezaehmten Jungen)
1. Rechtsklick aufs Junge -> im Untermenue (wie Fuettern/Streicheln, `S:client/BanditsNPCBearMenu.lua:172-194`) steht bei `mode` "stay"
   **"Follow me"**, bei "follow" **"Stay here"** (ein Umschalter, nie beide). Nur fuer den Besitzer und nur, wenn die Sicht das Junge kennt
   (`v.st == "tame"`, `v.owner == B.PlayerKey(playerObj)`); sonst fehlt der Punkt (kein grauer Muell fuer Fremde).
2. Klick -> `B.Ask(player, "Mode", { id = v.id, mode = "follow" | "stay" })`. SP: `B.Handle` direkt; MP: `sendClientCommand`.
3. Schreiber prueft (3.3) und setzt `rec.mode`; Meldung `Note_Follow` ("Your cub follows you.") bzw. `Note_Stay` ("Your cub stays here.");
   Sicht an alle in 60 Kacheln (Schild Zeile 2 wechselt sofort).
4. Grau mit Grund (Vorpruefung beim Client): Spieler sitzt im Fahrzeug -> "Follow me" grau, Tooltip `Why_InCar`. Alles andere entscheidet der Schreiber.

### 1.2 Folgen (Hirn-Takt des Schreibers, alle `brainMs` 1500 ms, nur fuer `st == "tame"` und `mode == "follow"`)
Der Besitzer `o` = naechster Spieler mit `key == rec.owner` aus `B.Players()` (SP geteilter Bildschirm: der naechste lokale Spieler).
`d` = Abstand Junges-Besitzer. Erste passende Regel gewinnt (`B.FollowDecide`, 5.3):

| Nr | Bedingung | Tut | Meldung an den Besitzer |
|---|---|---|---|
| 10 | Besitzer nicht da (offline, tot, MP noch nicht verbunden) | auf **Bleiben** wechseln (Heimat = Kachel des Jungen) | keine (er ist ja weg) |
| 11 | Besitzer sitzt in einem Fahrzeug (`p:getVehicle()`, Beleg 1) | auf **Bleiben** | `Note_StayCar` "Your cub cannot follow a vehicle. It waits here." |
| 12 | `d > BearFollowMaxDistance` (Sandbox, Vorgabe 40) | auf **Bleiben** | `Note_StayFar` "Your cub could not keep up. It waits to the %1." (Richtung vom Besitzer zum Jungen) |
| 13 | Besitzer auf anderer Ebene (`floor(o.z) ~= rec.z`) | **halten** (Sperre), kein Weg -- Treppen sind ungeprueft (FB1B 1.4) | keine |
| 14 | `d <= followNear` (3) oder (schon gehalten und `d <= followStart` 4,5) | **halten** (steht und wartet neben ihm) | keine |
| 15 | "steckt fest" (5.3) und Wiederholzeit noch nicht um | **nichts** (kein neuer Befehl, keine Sperre) | keine |
| 16 | sonst | **rennen** (`fleeTo`) zum Punkt `followGap` (2) Kacheln VOR dem Besitzer auf der Linie Besitzer->Junges; neuer Befehl nur, wenn der letzte >= `followMoveMs` (1200) alt ist UND (Ziel um >= `followRepath` 2,5 Kacheln gewandert ODER letzter Befehl >= `followRenewMs` 4000 alt ODER es war gehalten ODER Wiederholung nach "steckt fest") | keine |

- Ergebnis fuer Kevin: das Junge laeuft (rennend) hinterher und bleibt etwa 2-4,5 Kacheln hinter ihm; bleibt er stehen, wartet es neben ihm.
- **Steckt fest** (Tuer zu, Zaun, Wasser): wird der Abstand in `followStuckMs` (15 s) nicht um mindestens `followStuckGain` (1 Kachel)
  kleiner, gibt es keinen neuen Laufbefehl mehr, nur noch je `followRetryMs` (10 s) EINEN Versuch. Ein Fortschritt hebt das auf, ebenso
  Regel 14 (Besitzer kommt zurueck). Folge: kein endloses Neu-Rechnen von Wegen; das Junge wartet vor der Tuer, bis der Besitzer
  wiederkommt, die Tuer aufmacht oder weiter als 40 Kacheln weggeht (dann Regel 12). Die Engine haengt laut Jar selbst nicht endlos
  (Wandfolge mit Zeitdeckel, FB1B 1.1 "Haengen erkennen").
- **Laerm / Q-Ruf** zieht das Junge weg (FB1B 0.4, `respondToSound`, die Sperre haelt nicht). Der naechste Takt sieht den grossen Abstand
  und schickt es zurueck (Regel 16, Ziel weit gewandert -> sofort). Nichts Eigenes noetig.
- Futter in der Hand spielt beim Folgen keine Rolle (die Folgen-Regeln stehen vor den B1a-Regeln 6/7).
- Gegenprobe "bewegt es sich": B1a `B.MoveWatch` meldet einen stillen Laufbefehl als ECHTEN Fehler (`B.ErrEvery`,
  `S:server/BanditsNPCBearWorld.lua:418-428`). Beim Folgen ist ein Halt vor einer Tuer kein Fehler -> Folgen-Befehle ohne diese Gegenprobe
  (`watch = false`, 5.3), dafuer eine `B.Log`-Zeile beim Wechsel auf "steckt fest" (Diagnose hinter dem Schalter).

### 1.3 Junges ausser geladener Gegend
Hirn-Takt: ein Eintrag mit `mode == "follow"` hat kein Objekt (`B.FindAnimal` nil) UND `B.AreaLoaded(rec.x, rec.y)` ist falsch -> auf
**Bleiben** (Heimat = letzte bekannte Kachel), Meldung `Note_StayBehind` "Your cub stayed behind to the %1." (Richtung vom Besitzer aus;
ist der Besitzer nicht da: ohne Meldung). Ist die Gegend geladen, das Tier aber weg: B1a-Weg (Suchlauf, `missN`, `missing`); beim Wechsel
nach `missing` wird `mode` still auf "stay" gesetzt.

### 1.4 Bleiben
- `mode == "stay"` (oder fehlt): B1a-Verhalten fuer `tame` mit kleinerem Radius: Regel 8 holt es zurueck, wenn es weiter als `stayR` (8)
  von der Heimat ist (B1a `homeR` 10 gilt weiter fuer `fed`). Dazwischen laesst die Engine es wandern (Regel 9). Regeln 6/7 (Besitzer haelt
  Futter -> kommt / haelt, Heimat wandert mit) bleiben -- das ist das gespielte "Mitlocken".
- Heimat = Kachel, an der das Junge beim Umschalten auf Bleiben stand (Befehl, Auto, zu weit, entladen, offline). Nach dem Zaehmen ist die
  Heimat der Ort der letzten Fuetterung (B1a, unveraendert).

### 1.5 Speichern / Laden
- `rec.mode` und `rec.name` stehen im Register (globale ModData beim Schreiber, `S:server/BanditsNPCBearRegistry.lua:65-107`), werden mit
  dem Spielstand gespeichert. Die Sitzungs-Tabelle (`B._s[id]`: Sperre, letzter Befehl, "steckt fest") wird nie gespeichert; die
  Bewegungssperre am Tier auch nicht (FB1B 1.6). Nach dem Laden setzt der erste Hirn-Takt sie neu.
- SP: Besitzer `__sp` ist nach dem Laden sofort da -> ein folgendes Junges folgt weiter (Regel 14/16).
- MP, Server-Neustart: der Besitzer ist beim ersten Takt noch nicht verbunden -> Regel 10 -> Bleiben (ehrlich, vorhersagbar; er schaltet nach
  dem Einloggen neu um). `InitRegistry` prueft die neuen Felder (5.2).

### 1.6 Tod, Besitzer tot, offline, zweiter Spieler
- **Junges stirbt:** B1a unveraendert (`B.Close(rec, "dead")`, Sperre 7 Tage, `Note_BearDead`); Schild verschwindet mit der Sicht.
- **Besitzer stirbt:** `B.Players()` filtert Tote (`S:server/BanditsNPCBearWorld.lua:36`, `:48`) -> Regel 10 -> Bleiben. SP: die neue Figur hat
  wieder den Schluessel `__sp` -> bleibt Besitzer. MP: gleicher Kontoname -> bleibt Besitzer.
- **Besitzer offline (MP):** Regel 10 sofort, ohne Meldung; nach dem Einloggen zeigt das Schild "staying". Das Junge steht im Register; ist
  seine Gegend entladen, wird es virtuell und kommt beim Laden zurueck (FB1B 1.4).
- **Zweiter Spieler (MP):** sieht ueber fremden gezaehmten Jungen Name + "belongs to <Besitzer>"; bekommt KEINE Punkte "Follow me" /
  "Stay here" / "Name the cub"; ein gebastelter Befehl wird vom Server abgelehnt (`Why_NotOwner`) und gedrosselt (3.3). Fuettern/Streicheln
  fremder Zahmer bleibt wie in B1a abgelehnt. "Futter hinhalten" erscheint fuer fremde Zahme nicht.

### 1.7 Zahlen (Stellwerte in `B.CFG`, KERN-Datei `shared/BanditsNPCBear.lua`; die Bench aendert sie mit `NCBear_CubSet`)
| Feld | Vorgabe | Bedeutung |
|---|---|---|
| `followNear` / `followStart` / `followGap` | 3 / 4,5 / 2 | halten bis / losrennen ab (Haltespanne) / Ziel so weit vor dem Besitzer |
| `followMoveMs` / `followRepath` / `followRenewMs` | 1200 / 2,5 / 4000 | fruehester neuer Laufbefehl / Ziel-Wanderung fuer neuen Befehl / Auffrischen |
| `followStuckMs` / `followStuckGain` / `followRetryMs` | 15000 / 1,0 / 10000 | "steckt fest" nach / Mindest-Fortschritt / dann ein Versuch je |
| `stayR` | 8 | Bleiben-Radius des gezaehmten Jungen (Engine-Wandern wuerfelt +-8, FB1B 1.4) |
| `tagZ` | 0,18 | Anker von Balken UND Schild ueber dem Boden des Tiers (Ebenen); **ersetzt `barZ`** (0,55 war ~4,5 x zu hoch, FB1B 2.2) |
| `nameMax` | 24 | hoechstens so viele Zeichen im Namen (Vanilla 30; 24 passt besser ueber das kleine Tier) |
| `askMs` | 500 | Bitten "Mode"/"Rename" eines Spielers hoechstens so oft (Rest still verworfen) |
| `orphanScanMs` / `orphanAgeMs` / `orphanMax` | 120000 / 30000 / 16 | eigener Waisen-Suchlauf je / Waise muss so lange schon Waise sein / Deckel der Kandidatenliste |

Sandbox (neu, Seite `BanditsNPC`): `BanditsNPC.BearFollowMaxDistance`, integer, min 10, max 60, Vorgabe 40 -- "zu weit weg". Max 60
bleibt unter der geladenen Flaeche (76 Kacheln, CLAUDE.md; B1a deckelt Platzsuchen bei 65). Name frei (FB1B 6: grep 0 in NPC Crew).

---

## 2. Namensschild

### 2.1 Inhalt
| Junges | Zeile 1 (Schrift `UIFont.Small`) | Zeile 2 (klein, blasser) |
|---|---|---|
| eigenes, gezaehmt, ohne Namen | Vorgabe-Name `Tag_Name` "%1's cub": SP der Vorname der Figur (`getDescriptor():getForename()`, Beleg 10), MP der Kontoname (`owner` der Sicht) | `Tag_Follow` "following" / `Tag_Stay` "staying" |
| eigenes, gezaehmt, benannt | der Name aus dem Register | wie oben |
| fremdes, gezaehmt (MP) | Name bzw. "%1's cub" mit dem Kontonamen des Besitzers | `Tag_Owner` "belongs to %1" |
| gerade gezaehmt (5 s, B1a `FLASH_MS`) | Vorgabe-Name | `Hud_Tamed` "Tamed!" gruen blinkend, danach der Zustand |
| ungezaehmt (`new`/`shy`/`fed`) | Zaehm-Balken wie B1a (`S:client/ISUI/BanditsNPCBearHud.lua:131-158`, `:306-325`), unveraendert bis auf den Anker | |
| `missing` | nichts (kein Objekt) | |

Der Vorgabe-Name wird beim Client zusammengesetzt (der Server kennt den Vornamen nicht und muss ihn nicht kennen, FB1B 2.4); `__sp`
erscheint nie als Text. Je Sprache ein eigener Satz mit `%1` (6.2).

### 2.2 Position (dicht ueber dem Kopf, Stellwert)
- Anker = `isoToScreenX/Y(0, x, y, a:getZ() + B.CFG.tagZ)` (Beleg 13), Vorgabe **0,18** (Oberkante Junges ~0,12 Ebenen gerechnet, FB1B 2.2).
  Der Block waechst nach OBEN: Zeile 2 sitzt mit ihrer Unterkante am Anker, Zeile 1 darueber (1 px Abstand). Beim Balken wie B1a (Zeile 2,
  Balken, Zeile 1), nur derselbe Anker -> **Balken (vor dem Zaehmen) und Schild (danach) sitzen an derselben Stelle.**
- Einstellen im Spiel: `NCBear_CubSet("tagZ", 0.25)` (Bench, wirkt sofort, bis Spielende). Das neue Generator-Modell kann anders hoch sein
  -> Kevin stellt nach (Lehre NPC Crew "Regler gleich mitbauen", FB1B 2.2). Kein Zoom-Teilen (FB1B 2.2).
- Zeile 2 "klein": beim ersten Zeichnen beide Schrifthoehen holen (`getTextManager():getFontHeight(UIFont.Small)` / `(UIFont.NewSmall)`,
  Beleg 14); ist `NewSmall` niedriger, Zeile 2 in `NewSmall`, sonst in `Small` (ob `NewSmall` kleiner ist: ungeprueft, FB1B 2.3). Zeile 2
  immer blasser (Alpha 0,8, grau).

### 2.3 Sichtweite, Deckel, Kosten je Bild
- Sichtweite `B.CFG.hudDist` (20 Kacheln), hoechstens `B.CFG.hudMax` (6) Eintraege (Schilder + Balken zusammen, naechste zuerst). Kein
  Sichtfeld-Test (ein folgendes Junges laeuft HINTER dem Spieler, ausserhalb seines Blickkegels -- das Schild darf dort nicht verschwinden).
- Liste wie B1a hoechstens 1 x je Sekunde (sofort nach neuer Sicht); alle Texte (Name, Zustand, Besitzer) werden beim Listenbau fertig gemacht.
- Je Bild und Schild: 2 Umrechnungen, 4 `drawTextCentre` (2 Zeilen mit Schatten). Kein `getText`, kein Suchlauf, keine neue Tabelle je Bild.
  Balken unveraendert (2 Umrechnungen, 2 Rechtecke, 1 Rahmen, 4 Texte). Geteilter Bildschirm: nichts (B1a `:346`).
- `wanted` (B1a `:88-93`) gilt jetzt fuer ALLE Jungen der Sicht mit Objekt (auch gezaehmte); der B1a-Suchlauf mit Stufen 1 s / 5 s / 30 s
  (`:32-40`) deckelt die Kosten, wenn das eigene Junge weit weg und nicht geladen ist.

---

## 3. Umbenennen, Futter hinhalten, Server-Pruefungen

### 3.1 "Name the cub" (OBERFLAECHE, neue Datei `client/ISUI/BanditsNPCBearNameBox.lua`)
- Menuepunkt im Untermenue des eigenen gezaehmten Jungen (`Menu_Name`), nur Besitzer, nur mit Sicht-Eintrag. Kein Graufall (Fahrzeug egal).
- Fenster genau wie Vanillas Tier-Umbenennen (`V:client/ISUI/Animal/ISAnimalUI.lua:459-485`, Beleg 9): `ISTextBox:new(0, 0, 280, 180,
  U.T("UI_BN_Bear_Name_Title"), v.name or "", playerObj, onNameClick, playerObj:getPlayerNum(), v.id)`, `:initialise()`, `:addToUIManager()`,
  `modal.maxChars = B.CFG.nameMax` (OK grau + Vanilla-Tooltip `IGUI_TextBox_TooManyChar`, `V:client/ISUI/ISTextBox.lua:178-181`),
  `modal.noEmpty = true` (`:182-185`), `modal:setValidateFunction(nil, fn)` mit `fn(target, text)` = `B.CleanName(text) ~= nil`,
  `modal:setValidateTooltipText(U.T("UI_BN_Bear_Why_NameBad", B.CFG.nameMax))`, `modal.entry:setMaxTextLength(B.CFG.nameMax)`, Joypad wie
  `ISAnimalUI.lua:464-468`. Vorbelegt mit dem aktuellen Namen (leer, wenn keiner).
- `onNameClick(playerObj, button, id)`: nur bei `button.internal == "OK"`: `B.Ask(playerObj, "Rename", { id = id, name =
  button.parent.entry:getText() })`. Der Client prueft vor, entscheidet aber nichts.

### 3.2 "Hold out food for the cub" (Welt-Rechtsklick, OBERFLAECHE `client/BanditsNPCBearMenu.lua`)
- **Erscheint nur**, wenn ein passendes Junges mit Objekt in `B.CFG.lureDist` (15) Kacheln um den SPIELER steht: `new`/`shy` (jeder darf
  locken, wie B1a `keysOf`, `S:server/BanditsNPCBearServer.lua:598-602`), `fed` mit `bond == ich`, `tame` mit `owner == ich`. Quelle: die
  Objekte des Balkens (`U.CubsNear`, 5.4) -- live-Lage der Client-Kopie, kein Server-Weg, kein eigener Suchlauf. Sonst kein Eintrag (kein
  Menue-Muell in der Stadt). Spieler im Fahrzeug: kein Eintrag (B1a `onFillWorld` kehrt schon um, `:285`).
- Eintrag `Menu_Hold` mit Untermenue aus `B.FoodList(playerObj, B.CFG.menuFoods)` (Zeilen wie beim Fuettern: `Food_Fav`/`Food_Ok`/`Food_Snack`
  + Anzahl), Tooltip `Menu_HoldTip`. Keine Futterzeile: Eintrag grau mit `Menu_NoFood`.
- Klick: `ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)` (Beleg 8; holt das Stueck selbst aus
  Taschen, stellt `ISEquipWeaponAction` an). Kein Hingehen, kein Leeren der Warteschlange. Danach die bestehende Regel: Spieler steht still
  mit Futter -> scheues Junges kommt bis 3, angefuettertes/zahmes bis 2 Kacheln (`B.Decide` 2/3/6/7). Fuettern dann per Rechtsklick
  aufs Junge (Feed laeuft gehend hin, Regel 3/7 haelt es).
- `test`-Lauf (Controller): `ISWorldObjectContextMenu.setTest()` wie B1a, wenn der Eintrag erscheinen wuerde.
- Reihenfolge in `onFillWorld`: NACH "Koederplatz aufgeben", VOR dem fruehen `return` des Koeder-Teils (`:311`) -- sonst verschluckt der
  Koeder-Riegel den neuen Punkt.
- Ehrliche Grenzen: `ISEquipWeaponAction` bricht im Rennen ab (`stopOnRun`, FB1B 4); eine Waffe in der Hand wandert dabei ins Inventar
  (Vanilla-Verhalten). Kein Gegenstand wird erzeugt oder vernichtet (rote Linie).

### 3.3 Server-Pruefungen (KERN, neue Datei `server/BanditsNPCBearFollow.lua`; `B.Handle` leitet weiter)
Gemeinsam: `B.IsWriter()`; `pkey = B.PlayerKey(player)`; Drossel `B.AskOk(pkey, ms)` (`askMs`; Tabelle `B._askAt`, bei mehr als 64
Schluesseln geleert); `type(args.id) == "string"` und `reg.cubs[args.id]` vorhanden, sonst `Why_Gone`.

| Bitte | Pruefung (in dieser Reihenfolge) | Bei Erfolg |
|---|---|---|
| `Mode` `{ id, mode }` | `mode` ist "follow" oder "stay" (sonst still verwerfen); `rec.st == "missing"` -> `Why_Gone`; `rec.st ~= "tame"` oder `rec.owner ~= pkey` -> `Why_NotOwner`; `B.FindAnimal(rec)` nil -> `Why_Gone`; nur bei "follow": `player:getVehicle()` -> `Why_InCar`, Abstand Spieler-Tier > `BearFollowMaxDistance` -> `Why_Far` | `B.SetMode(rec, mode, "ask", players)`, `B.FlushViews()` |
| `Rename` `{ id, name }` | `type(name) == "string"` und `string.len(name) <= 4 * nameMax` (Vorab-Deckel, sonst `Why_NameBad`); `rec.owner ~= pkey` oder `st` nicht "tame"/"missing" -> `Why_NotOwner`; `B.CleanName(name)` nil -> `Why_NameBad` (Zahl `nameMax`) | `rec.name = sauber`, `B.Commit(rec)`, `Note_Renamed` (t = "name"), `B.FlushViews()` |

`B.CleanName(text)` (rein, shared, auch fuer das Eingabefenster): Text-Typ; fuehrende/abschliessende Leerzeichen (Byte 32) weg (eigene
Schleife, kein `string.trim`); leer -> nil; `string.len > nameMax` -> nil; jedes Zeichen per `string.byte`: < 32, = 127, `<`, `>`, `%` -> nil
(`<`/`>` gegen Rich-Text-Tags in Tooltips, `%` gegen Platzhalter in `getText`). Zeichencodes ueber 127 (Umlaute, Kyrillisch, Koreanisch,
Chinesisch) sind erlaubt -- unter Kahlua liefert `string.byte` dafuer Zeichencodes > 255 (ungeprueft im Spiel, FB1B 3). Kein Engine-Aufruf.

Meldungen bei Ablehnung: Server -> `B.Tell` an den Bittenden (SP direkt). Neu in `WHY_T` (`S:server/BanditsNPCBearServer.lua:35-39`):
`UI_BN_Bear_Why_NameBad = "num"` (Wert `nameMax`). Kick-Gefahr: keine (nur `sendClientCommand`, Recht LoginOnServer, FB1B 1.6).

---

## 4. N5 Waisen aufraeumen

### 4.1 Was eine Waise ist
Ein lebendes `ncbearcub` in der geladenen Zelle **ohne Spiegel** (`getModData().tcBear` fehlt) und **ohne passenden Register-Eintrag**. Nur
diese Art, nie der Erwachsene `bear`, nie fremde Tiere. Tiere MIT Spiegel bleiben wie B1a (geschlossener Eintrag + `new`/`shy` -> `stale`,
sonst bleiben sie und werden beim Anfassen `found`).

### 4.2 Riegel (alle drei Pflicht, im Kern-Test je ein Fall)
1. **Identitaet:** ein Tier, das als `B._s[id].obj` eines Eintrags gemerkt ist, ist nie Waise -- es wird gebunden, und fehlt sein Spiegel,
   wird er sofort geschrieben (`B.Commit(rec)`, "Spiegel-Reparatur"). Schuetzt das gerade erzeugte Junge (0.6).
2. **Mehrdeutig:** passt die AnimalID der Waise zu einem Eintrag OHNE Objekt (gleiche AnimalID, <= 40 Kacheln, wie B1a `:323-345`), aber
   der Rueckfall konnte nicht binden (mehrere Kandidaten), wird keiner entfernt (nie raten), `B.Log`-Zeile.
3. **Alter und Beobachter:** entfernt wird erst, wenn dasselbe Objekt schon bei einem frueheren Suchlauf vor mindestens `orphanAgeMs` (30 s)
   Waise war (Kandidatenliste `B._orph = { { o, at } }`, Deckel `orphanMax` 16, Vergleich mit `==` wie `S:...Registry.lua:194`), UND
   niemand naeher als `vanishKeep` (25) steht, UND es im SP keiner sieht (`B.SeenInSP`). Dann `B.RemoveCub(o)` (einzige Entfern-Stelle,
   im MP mit `removeAnimal`, `S:server/BanditsNPCBearWorld.lua:248-256`), `B.Log("scan: removed an orphan cub ...")`.
   Kandidaten, die nicht mehr da sind oder inzwischen einen Spiegel haben, fallen bei jedem Lauf aus der Liste.

### 4.3 Wann gesucht wird
- Jeder B1a-Suchlauf (`B.ScanAnimals`, nur bei vermissten Eintraegen, je 5 s) fuehrt die Waisen-Liste mit.
- NEU: ein eigener seltener Lauf im Hirn-Takt je `orphanScanMs` (120 s), auch ohne Eintraege und ohne Vermisste (FB1B 0.5 b). Kosten: eine
  Kopie der Objektliste je 2 min (FE 1.2). Im MP unbelegt auf dem Server wie B1a (A3, `getObjectListForLua`/`getAnimalID`) -- MP-Testpunkt.
- Bench `NCBear_CubSweep()` ruft `B.ScanAnimals(nil, true)`: `force` ueberspringt NUR Riegel 3 "Alter" (nie Identitaet, Mehrdeutig,
  Beobachter).

### 4.4 Dazu: Spiegel gleich beim Erzeugen
`B.NewRec` schreibt den Spiegel `{ id, st }` sofort ueber `animal:getModData()` (ohne die `isExistInTheWorld`-Frage, die direkt nach
`addToWorld` immer falsch ist); `B.Commit` bleibt wie es ist. `liveRec` prueft je Takt billig, ob der Spiegel noch zu `rec.id` passt, sonst
`B.Commit(rec)`. Damit hat jedes Junge mit Eintrag spaetestens nach einem Takt seinen Spiegel.

---

## 5. Genaue Schnittstelle (WOERTLICH einhalten; Abweichung sofort nach `schnittstelle_aenderungen.md`, Abschnitt "B1b")

### 5.1 Wer schreibt welche Datei (alles unter `_arbeit/baer_zaehmen/mod/42/media/`)
| Datei | Bauer | Was |
|---|---|---|
| `lua/shared/BanditsNPCBear.lua` | KERN | `B.CFG` neue Felder (1.7), `barZ` raus, `tagZ` rein; `B.OPTS.BearFollowMaxDistance = { def = 40, min = 10, max = 60 }` |
| `lua/shared/BanditsNPCBearRules.lua` | KERN | `B.ModeOf`, `B.FollowDecide`, `B.CleanName`; `B.Decide` Regel 8 mit `c.homeR` |
| `lua/server/BanditsNPCBearRegistry.lua` | KERN | Felder `mode`/`name`, `InitRegistry` prueft sie, `NewRec` stempelt sofort, Sicht-Eintrag mit `name`/`mode` |
| `lua/server/BanditsNPCBearServer.lua` | KERN | `B.Handle` leitet "Mode"/"Rename" weiter, `WHY_T`, `buildEnv` mit `env.owner`, `liveRec` Folgen-Zweig + Spiegel-Probe, Hirn-Takt: Folgen-Verloren-Pass, Waisen-Takt, `countMisses` setzt `mode` |
| `lua/server/BanditsNPCBearWorld.lua` | KERN | `B.Players` mit `car`, `B.MoveTo` mit `opt`, `B.ScanAnimals(players, force)` mit Waisen |
| `lua/server/BanditsNPCBearFollow.lua` (**neu**) | KERN | `B.SetMode`, `B.FollowStep`, `B.FollowLost`, `B.HandleMode`, `B.HandleRename`, `B.AskOk` |
| `lua/client/BanditsNPCBearClient.lua` | OBERFLAECHE | `U.EN` neue Schluessel (wortgleich mit EN/UI.json), `U.LocalName`, `U.CubName` |
| `lua/client/BanditsNPCBearMenu.lua` | OBERFLAECHE | Follow/Stay, Name, "Hold out food" |
| `lua/client/ISUI/BanditsNPCBearNameBox.lua` (**neu**) | OBERFLAECHE | `U.AskName` (Eingabefenster) |
| `lua/client/ISUI/BanditsNPCBearHud.lua` | OBERFLAECHE | Schild, Anker `tagZ`, `wanted` fuer alle, `U.CubsNear` |
| `lua/client/NCBearBenchCub.lua` | OBERFLAECHE | Bench-Erweiterung (5.6) -- wird nie kopiert |
| `lua/shared/Translate/<L>/UI.json` x 7 | OBERFLAECHE | neue Schluessel (6.2), `Note_Tamed` erweitert |
| `lua/shared/Translate/<L>/Sandbox.json` x 7 | OBERFLAECHE | `Sandbox_BanditsNPC_BearFollowMaxDistance` + `_tooltip` |
| `sandbox-options.txt` | OBERFLAECHE | Block `option BanditsNPC.BearFollowMaxDistance` (Form wie `BearCubMinDistance`, `:24-31`), vor `BearLog` |
| `staging_dateien.txt`, `attrappe/gesamt/`, `baer/NAEHTE.md`, Trockenlauf/Probe `baer/tools/baer_uebernahme.py` | ZUSAMMENBAU | 7 |
Unveraendert: `shared/BanditsNPCBearDefs.lua`, `...Food.lua`, `...Crew.lua`, `shared/TimedActions/*`, `IG_UI.json` x 7, Modell, Textur, `nc_bear_cub.txt`.
Kopf jeder neuen Lua-Datei wie PZ 6.1 (`BanditsNPC = BanditsNPC or {}` ...); `server/`-Datei beginnt mit `if isClient() then return end`.
Kein Einfangen fremder Funktionen auf Dateiebene (Ladefolge `shared` < `client` < `server`, darin alphabetisch: `...Follow` laedt VOR
`...Registry`/`...Server`/`...World` -- nur zur Laufzeit ueber `B.X` greifen).

### 5.2 Register und Sicht (KERN)
```
rec = { ... B1a-Felder (PZ 4.1 + schnittstelle_aenderungen) ...,
        mode = nil | "follow" | "stay",      -- nil heisst "stay"; nur bei st "tame" wirksam
        name = nil | Text }                  -- schon durch B.CleanName; nil = Vorgabe-Name beim Client
B._s[id].f = { held, orderAt, tx, ty, bestD, bestAt, stuck, retryAt }   -- Sitzung, nie gespeichert; B.SetMode leert sie
viewEntry(rec) = { ... B1a-Felder ..., name = rec.name, mode = (st "tame": B.ModeOf(rec), sonst nil) }
```
`InitRegistry`: `mode` nicht "follow"/"stay" -> nil; `name` kein Text oder `B.CleanName(name) ~= name` -> nil (mit `B.Err`-Zeile je Eintrag).
`B.View.cubs[id]` traegt `name` und `mode` automatisch (`copyFlat`, `S:shared/BanditsNPCBear.lua:358-364`). `me` unveraendert.

### 5.3 Funktionen des KERNs
shared (`BanditsNPCBearRules.lua`, rein, auch der Client darf sie rufen):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.ModeOf(rec)` | "follow" / "stay" | nil und alles andere -> "stay" |
| `B.CleanName(text)` | Text oder nil, whyKey | 3.3; whyKey immer `"UI_BN_Bear_Why_NameBad"` |
| `B.FollowDecide(c, o, f, ms)` | `{ act, why, tx, ty, rule }` | `c = { x, y, z }` (z ganze Ebene); `o = nil \| { key, x, y, z, dist, car }`; `f` = Sitzungs-Tabelle, wird fortgeschrieben (nur `bestD`, `bestAt`, `stuck`, `retryAt`; `orderAt`/`tx`/`ty` setzt `B.FollowStep` NACH einem gelungenen Befehl); `act` = "stay" / "hold" / "run" / "keep"; `why` = "offline" / "car" / "far" / "level" / "near" / "stuck" / nil; `rule` 10..16 (1.2). Fortschritt wird VOR Regel 15 gerechnet (gilt auch waehrend des Wartens) |
| `B.Decide(c, env)` | wie B1a | einzige Aenderung: Regel 4/8 fragen `c.homeR or B.CFG.homeR` |

server (`BanditsNPCBearFollow.lua`, neu):
| Funktion | Rueckgabe | Bemerkung |
|---|---|---|
| `B.SetMode(rec, mode, why, players)` | boolean | setzt `rec.mode`; bei "stay" Heimat = `rec.x/y/z`; leert `B._s[id].f`; `B.Commit`; Meldung an den Besitzer nach `why`: "ask" + follow -> `Note_Follow`, "ask" + stay -> `Note_Stay`, "car" -> `Note_StayCar`, "far" -> `Note_StayFar` (t "dir"), "lost" -> `Note_StayBehind` (t "dir"), "offline"/"missing" -> keine; Richtung `B.DirOf(rec.x - e.x, rec.y - e.y)`; `B.Log` |
| `B.FollowStep(rec, a, env, ms, players)` | - | baut `c`, ruft `B.FollowDecide(c, env.owner, f, ms)`, fuehrt aus: stay -> `B.SetMode(rec, "stay", why, players)`; hold -> `B.Hold(rec, a, true)`; run -> `B.MoveTo(rec, a, tx, ty, rec.z, { minMs = followMoveMs, watch = false })`, bei true `f.orderAt/tx/ty`; keep -> nichts. Wechsel nach "steckt fest" -> `B.Log` |
| `B.FollowLost(rec, players)` | - | 1.3 (Junges ohne Objekt, `mode` follow, Gegend nicht geladen) |
| `B.HandleMode(player, args)` / `B.HandleRename(player, args)` | - | 3.3; schicken selbst Meldung und Sicht |
| `B.AskOk(pkey, ms)` | boolean | Drossel 3.3 |

server (Aenderungen in vorhandenen Dateien):
| Stelle | Aenderung |
|---|---|
| `B.Handle` (`...Server.lua:365-386`) | `if command == "Mode" then if B.HandleMode then B.HandleMode(player, args) end return end`, ebenso "Rename" |
| `buildEnv` (`:605-632`) | bei `st == "tame"`: `env.owner` = naechster Eintrag aus `players` mit `key == rec.owner`, `{ key, x, y, z, dist, car = e.car }` |
| `liveRec` (`:651-692`) | Spiegel-Probe (4.4); `c.homeR = B.CFG.stayR` bei `tame`; bei `tame` und `B.ModeOf(rec) == "follow"`: `B.FollowStep(...)` statt `B.Decide`/`steer`/`B.MoveWatch` |
| `brainTickBody` (`:810-850`) | nach `resolve`: fuer jeden Eintrag aus `missing` `B.FollowLost(rec, players)`; Waisen-Takt: `B._orphAt` nil/rueckwaerts/>= `orphanScanMs` und in diesem Takt noch kein Suchlauf -> `B.ScanAnimals(players)` |
| `countMisses` (`:720-741`) | beim Wechsel `tame` -> `missing` zusaetzlich `rec.mode = "stay"` |
| `WHY_T` (`:35-39`) | `UI_BN_Bear_Why_NameBad = "num"` |
| `B.Players` (`...World.lua:29-54`) | je Eintrag `car = (p:getVehicle() ~= nil)` (Beleg 1) |
| `B.MoveTo(rec, animal, x, y, z, opt)` (`...World.lua:385-414`) | `opt` wahlfrei: `opt.minMs` ersetzt `B.CFG.moveMs`; `opt.watch == false` -> keine Gegenprobe (`s.chk = nil`). Ohne `opt` wie B1a |
| `B.ScanAnimals(players, force)` (`...World.lua:285-358`) | Riegel 1 (Identitaet + Spiegel-Reparatur) im ersten Durchgang; nach dem AnimalID-Rueckfall Waisen sammeln (Riegel 2), Liste `B._orph` fuehren, entfernen (Riegel 3, `force`); Rueckgabe `n, removed` |
| `B.NewRec` (`...Registry.lua:151-178`) | `mode = nil, name = nil`; Spiegel sofort (4.4) |
| `viewEntry` (`...Registry.lua:398-410`) | `name`, `mode` (5.2) |

Neue KERN-Felder an `B` (nur Kern-intern, die Bench darf lesen): `B._askAt`, `B._orph`, `B._orphAt`.

### 5.4 Funktionen der OBERFLAECHE (nur unter `B.UI` = `U`, wie B1a; an `B` nichts Neues)
| Funktion | Datei | Rueckgabe / Bemerkung |
|---|---|---|
| `U.LocalName()` | Client.lua | Vorname der Figur `getSpecificPlayer(0):getDescriptor():getForename()` (Beleg 10), leer -> "?" |
| `U.CubName(c, meKey)` | Client.lua | `c.name` (nicht leer) oder `U.T("UI_BN_Bear_Tag_Name", wer)` mit `wer` = `U.LocalName()` bei `c.owner == B.SP_KEY`, sonst `tostring(c.owner)` |
| `U.CubsNear(playerObj, radius)` | Hud.lua | Liste `{ id, c, a, d }` der Jungen mit lebendem Objekt aus der Balken-Liste (`S.objs`), Abstand zum Spieler <= radius, naechste zuerst; kein Suchlauf, keine Engine ausser `getX/getY`/`isExistInTheWorld`/`isDead` |
| `U.AskName(playerObj, v)` | NameBox.lua | 3.1 |
| Menue (lokal) `addMode`, `addName`, `addHold`, `onMode`, `onHold` | Menu.lua | 1.1, 3.1, 3.2; `onMode` -> `B.Ask(playerObj, "Mode", { id = v.id, mode = ... })` |
| Hud `describe` / `draw` | Hud.lua | 2.1-2.3; Schrift-Wahl einmal (2.2) |

Die OBERFLAECHE ruft vom KERN nur: `B.Ask`, `B.ModeOf`, `B.CleanName`, `B.FoodList`, `B.ViewOf`, `B.PlayerKey`, `B.View`, `B.CFG`, `B.SP_KEY`
und (nur Bench, SP) `B.CreateCub`, `B.ScanAnimals`, `B.FindAnimal`, `B.NearestRec`, `B._s`.

### 5.5 Befehle (Modul `BanditsNPCBear`, Ergaenzung zu PZ 6.2.6)
| Richtung | Befehl | Felder | Antwort |
|---|---|---|---|
| Client -> Schreiber | `Mode` | `{ id = Text, mode = "follow" \| "stay" }` | `Note` + `Sync` (an alle in 60 Kacheln und den Besitzer) |
| Client -> Schreiber | `Rename` | `{ id = Text, name = Text }` | `Note` (`Note_Renamed`, t "name") + `Sync` |
Nie eine leere Tabelle schicken (B1a-Befund B1); `args == nil` behandelt der Server wie `{}` und verwirft dann mangels `id`.

### 5.6 Bench (`client/NCBearBenchCub.lua`, OBERFLAECHE, nur SP, wird nie kopiert)
| Befehl | Tut |
|---|---|
| `NCBear_CubFollow(on)` | meinem naechsten zahmen Jungen Folgen an/aus (nil = umschalten) -- ueber `B.Ask(p, "Mode", ...)`, also dieselben Pruefungen |
| `NCBear_CubName(text)` | umbenennen ueber `B.Ask(p, "Rename", ...)` |
| `NCBear_CubFollowTest()` | Folgen-Zustand drucken: `mode`, Abstand zum Besitzer, Ebenen, `car`, `f.held/stuck/orderAt` (Alter), Heimat, `tagZ` |
| `NCBear_CubOrphan(n)` | eine Waise n Kacheln (Vorgabe 8) neben mir: `B.CreateCub` OHNE Eintrag (fuer den N5-Test) |
| `NCBear_CubSweep()` | `B.ScanAnimals(nil, true)`, druckt `n` und `removed` |
| `NCBear_CubInfo()` | zusaetzlich `mode` und `name` je Eintrag |
| `NCBear_CubSet` | Hilfetext nennt `tagZ` statt `barZ` |
Rechtsklick "NC Bear" (englische Literale, nur Bench): "Cub: follow / stay", "Cub: make an orphan", "Cub: remove orphans now".

---

## 6. Texte (OBERFLAECHE schreibt alle sieben Sprachen; KERN benutzt nur diese Schluessel)

### 6.1 Vom KERN benutzt (Note / whyKey)
`Note_Follow` (Your cub follows you.) - `Note_Stay` (Your cub stays here.) - `Note_StayCar` (Your cub cannot follow a vehicle. It waits
here.) - `Note_StayFar` (Your cub could not keep up. It waits to the %1.) - `Note_StayBehind` (Your cub stayed behind to the %1.) -
`Note_Renamed` (Your cub is now called %1.) - `Why_NameBad` (That name does not work. Use up to %1 letters, without < > or %%.) -
`Why_InCar` (Not while you are in a vehicle.). Vorhandene weiter benutzt: `Why_Gone`, `Why_NotOwner`, `Why_Far`.
**`%1` bei `Note_StayFar`/`Note_StayBehind` ist ein `Dir_*`-Text** (t = "dir"). Die `Dir_*` sind fuer den Satzbau von `Note_Heard` gebaut
(schnittstelle_aenderungen.md, OBERFLAECHE Eintrag 2: RU im Praepositiv, FR mit Praeposition "au nord-est", KO/CN ohne "-쪽"/"边", PTBR/ES
nach "ao"/"al"). Jeder neue Satz muss in seiner Sprache genau diese Form tragen (EN "to the %1", PTBR "ao %1", RU "на %1", KO "%1쪽에",
ES "al %1", CN "%1边", FR "%1"). Keine neuen `Dir_*`.

### 6.2 Nur OBERFLAECHE
`Menu_Follow` (Follow me) - `Menu_Stay` (Stay here) - `Menu_FollowTip` (It runs after you. In a vehicle or when you get too far ahead,
it waits.) - `Menu_StayTip` (It stays around this spot.) - `Menu_Name` (Name the cub) - `Name_Title` (Name for your cub:) - `Menu_Hold` (Hold
out food for the cub) - `Menu_HoldTip` (Takes it in your hand. Stand still and the cub comes closer.) - `Tag_Name` (%1's cub) - `Tag_Follow`
(following) - `Tag_Stay` (staying) - `Tag_Owner` (belongs to %1).
Geaendert: `Note_Tamed` -> "The cub trusts you. It is yours now! Right-click it and choose Follow me." (alle sieben Sprachen).
Sandbox: `Sandbox_BanditsNPC_BearFollowMaxDistance` (Bear: follow distance limit), `..._tooltip` (Tiles. If the owner gets farther away
than this, a following cub stops and waits there.).
Regeln wie PZ 6.2.8: alle Schluessel `UI_BN_Bear_*` in allen sieben `UI.json`, gleiche Platzhalter, sortiert, Round-Trip
`json.dumps(data, indent=4, ensure_ascii=False) + "\n"`, UTF-8 ohne BOM, LF; CN nur Zeichen aus Vanilla-CN (Werkzeug `ober_werkzeug/texte.py`);
`U.EN` in `client/BanditsNPCBearClient.lua` wortgleich mit EN/UI.json (das Uebernahme-Skript prueft das, `baer/tools/baer_uebernahme.py:968-981`);
keine Woerter spawn/debug/bench/cheat/test; Menue-Eintraege nur ueber `U.T(...)` (sonst meldet das Skript "Testmenue").

---

## 7. Fuer den ZUSAMMENBAU
- `staging_dateien.txt` neu (2 neue Lua-Dateien, geaenderte MD5).
- `attrappe/gesamt/run.lua` Abschnitt "17 B1b" (8.3); beide Attrappen-Laeufe der Bauer gegen die echten Dateien wiederholen.
- `baer/tools/baer_uebernahme.py`: erwartet keine Aenderung (Muster `BanditsNPCBear[A-Za-z0-9_]*\.lua` deckt beide neuen Dateien,
  `:95`; `B.RemoveCub` bleibt einzige `:remove()`-Stelle, `B.CreateCub` wird im kopierten Code weiter nur aus `B.AppearFor` gerufen,
  `:203-214`; neue Sandbox-Option muss in `B.OPTS` UND `sandbox-options.txt` stehen, `:779`). Trockenlauf mit `--vor-b5a`, Probe.
- `baer/NAEHTE.md` Naht 8: Namensschilder -- NPC Crews `client/ISUI/BanditsNPCNameTags.lua` zeichnet keine Tiere (grep `IsoAnimal`/
  `getAnimalType` dort: 0 Treffer, 10.11.), NPC Crew setzt keinen Tiernamen (`setCustomName` nur an Gegenstaenden,
  `NC:shared/BanditsNPCLivestockButcher.lua:1760`) -> keine neue Naht. Taste V bleibt spaeter.
- Einbau in NCBearTest nur, wenn Kevin nicht spielt (CLAUDE.md 5); vorher und nachher sichern.

---

## 8. Tests

### 8.1 KERN-Attrappe (`attrappe/kern/run.lua`, neuer Abschnitt "13 B1b"; Tier-Attrappe zaehlt `fleeTo`, `setBlockMovement`, `getModData`)
1. `B.FollowDecide` jede Regel 10-16 mit treffendem und knapp nicht treffendem Fall: offline; Auto; `dist` 40,1 / 40,0 bei Max 40; andere
   Ebene; 2,9 halten / 3,1 nicht; gehalten 4,4 halten / 4,6 rennen; Ziel genau 2 Kacheln vor dem Besitzer; zweiter Befehl nach 1100 ms ->
   keep, nach 1300 ms und Wanderung 2,6 -> run; Wanderung 2,4 und Alter 3900 -> keep, 4100 -> run; 15 s ohne 1 Kachel Fortschritt ->
   stuck/keep; nach 10 s genau ein run; Fortschritt -> stuck weg; Regel 14 hebt stuck auf; `f` waechst nicht (feste Felder).
2. `Mode`: Besitzer follow -> `rec.mode`, `Note_Follow`, Sicht traegt `mode`; Fremder -> `Why_NotOwner`, nichts geaendert; `fed` ->
   `Why_NotOwner`; `missing` -> `Why_Gone`; Tier nicht geladen -> `Why_Gone`; im Auto -> `Why_InCar`; 41 Kacheln -> `Why_Far`; `mode = "fly"`,
   `id` Zahl, `args` nil -> still nichts; zwei Bitten in 400 ms -> zweite verworfen, nach 600 ms angenommen; `B._askAt` > 64 -> geleert.
3. Bleiben: `SetMode stay` setzt Heimat = Kachel; `tame` 8,1 von der Heimat -> Regel 8 "home", 7,9 -> "free"; `fed` weiter mit 10.
4. Wechsel im Hirn-Takt: Besitzer fehlt in `players` -> stay ohne Meldung; `car` -> `Note_StayCar`; 45 Kacheln -> `Note_StayFar` mit
   Richtung; Objekt weg + Gegend nicht geladen -> `Note_StayBehind`; Objekt weg + geladen -> kein Wechsel, nach `missScans` `missing` + `mode` stay.
5. Umbenennen: `B.CleanName` "Bruno" ok, "  Bruno  " -> "Bruno", "" / "   " nil, 24 Zeichen ok, 25 nil, "<b>", "a%1", Steuerzeichen (Byte 7),
   Byte 127 je nil, UTF-8-Bytes > 127 ok; Server: Besitzer -> `rec.name`, `Note_Renamed` mit Name, Sicht-Eintrag `name`; Fremder abgelehnt;
   Name als Zahl / 200 Zeichen -> `Why_NameBad` ohne Schleife ueber alle Zeichen.
6. Speichern/Laden: Register-Tabelle behalten, `B._s` leeren, `InitRegistry`: `mode`/`name` bleiben; "fly" -> nil, 99 Zeichen -> nil (je
   eine `B.Err`-Zeile); erster Takt mit Besitzer in 2 Kacheln -> halten (Sperre neu gesetzt).
7. Waisen: (a) Waise ohne Spiegel, niemand in 25 -> 1. Lauf Kandidat, 2. Lauf nach 30 s entfernt (`RemoveCub` genau 1 x); (b) Spieler in 24 ->
   bleibt; (c) SP `isCanSee` wahr -> bleibt; (d) frisch ueber `B.AppearFor` erzeugt, Attrappe `isExistInTheWorld` falsch -> Spiegel trotzdem
   geschrieben, nie Kandidat; (e) Spiegel geloescht, Objekt = `s.obj` -> gebunden, Spiegel repariert; (f) Eintrag ohne Objekt + zwei Kandidaten
   gleicher AnimalID -> keiner entfernt; (g) `force` -> im ersten Lauf entfernt, Riegel b/c gelten weiter; (h) 20 Waisen -> Liste hoechstens 16;
   (i) Waisen-Takt laeuft ohne Eintraege je 120 s (Uhr stellen); (j) Erwachsener `bear` ohne Spiegel -> nie angefasst.
8. MP-Rundlauf (`isServer = true`, Client-Attrappe): "Mode" ueber `sendClientCommand`-Liste -> `onClientCommand` -> Sync an Besitzer UND an
   Spieler B in 30 Kacheln mit `mode`/`name`; Note nur an den Besitzer; Spieler B "Rename" -> abgelehnt. SP (`isClient = isServer = false`):
   `B.Ask` ruft `B.Handle` direkt, keine Sende-Eintraege.
9. Nutzlast: nur Zahl/Text/Wahrheitswert/Tabelle; `name` nil fehlt im Eintrag.
10. Dateien: kein `next(`, kein `%a`, kein `pathToLocation`, kein `setCustomName`/`getCustomName`, kein `setVariable("animalRunning"` in
    `BanditsNPCBear*` (grep im Testlauf).

### 8.2 OBERFLAECHE-Attrappe (`attrappe/ober/run.lua`, neue Abschnitte; eigene Kern-Attrappe nach 5.3/5.5, nicht auf den KERN warten)
1. Tier-Menue: eigenes Zahmes `mode` stay -> Feed, Pet, "Follow me", "Name the cub"; `mode` follow -> "Stay here"; fremdes Zahmes -> keines der
   neuen; `v` nil -> keines + Hello; im Fahrzeug -> "Follow me" grau mit `Why_InCar`.
2. Klick "Follow me" / "Stay here" -> genau ein `B.Ask("Mode", { id, mode })`.
3. Namensfenster (ISTextBox-Attrappe): `maxChars == nameMax`, `noEmpty`, Pruefer nimmt `B.CleanName`, `entry:setMaxTextLength(nameMax)`;
   OK -> `B.Ask("Rename", { id, name })`; Abbrechen -> nichts.
4. "Hold out food": scheues Junges in 10 Kacheln -> Punkt mit Futter-Untermenue; Klick -> `equip(p, hand, food, true, false)` genau 1 x, keine
   Warteschlange geleert; kein Futter -> grau `Menu_NoFood`; Junges in 16 Kacheln -> kein Punkt; fremd gezaehmt / fremd gebunden -> kein Punkt;
   Koeder ausgeschaltet -> Punkt trotzdem da; `test` -> `setTest`.
5. Schild-Texte: SP eigen ohne Namen "<Vorname>'s cub" / "staying", nach Sync follow "following"; benannt "Bruno"; MP fremd "Bruno" bzw.
   "<Konto>'s cub" / "belongs to <Konto>"; `__sp` erscheint nie; gerade gezaehmt: Zeile 2 "Tamed!" 5 s, dann Zustand.
6. Anker: Balken und Schild benutzen `a:getZ() + tagZ` (gleiches `sy` bei gleichem Tier); `tagZ` aendern verschiebt beide.
7. Kosten: waehrend `draw` 0 Aufrufe von `U.T`/`getText`/`getObjectListForLua`; je Schild 2 Umrechnungen, 4 `drawTextCentre`; > 6 Junge -> 6.
8. Texte: sieben Sprachen, gleiche Schluessel, gleiche Platzhalter, `U.EN` == EN, Round-Trip, CN-Zeichen aus Vanilla, `Note_StayFar`/
   `Note_StayBehind` je Sprache mit dem `Dir_*`-Satzbau (Sichtpruefung im Bericht: je Sprache ein ausgefuellter Beispielsatz).
9. Bench: neue Befehle im MP "singleplayer only"; keine neue Bench-Funktion ausserhalb `NCBearBenchCub.lua`.

### 8.3 GESAMT (`attrappe/gesamt/run.lua` Abschnitt "17 B1b", Zusammenbau)
Ein Junges erscheint -> gezaehmt -> "Follow me" -> Besitzer geht 10 Kacheln (Lagen stellen) -> `fleeTo` -> nah -> `setBlockMovement(true)`
-> Register "speichern", `B._s` leeren, `InitRegistry` -> folgt weiter -> Besitzer ins Auto -> Bleiben + `Note_StayCar` -> "Name the cub" ->
Sicht traegt den Namen -> Waise erzeugen -> nach 30 s und weit weg entfernt. Einmal SP, einmal Server + zwei Client-Attrappen (A Besitzer, B fremd).

### 8.4 Kevins Test im Spiel (nach dem Einbau: Spiel neu starten, `bugwatch.py` mitlaufen lassen; Wegwerf-Spielstand, `-debug`)
Einzelspieler:
1. Spielstand mit gezaehmtem Jungen aus B1a laden (oder `NCBear_CubClean()`, `NCBear_CubHere()`, `NCBear_CubTame(100)`). Erwartet: ueber dem
   Jungen "<Vorname>'s cub" / "staying", **dicht ueber dem Kopf**. Zu hoch/tief: `NCBear_CubSet("tagZ", 0.25)` probieren, Zahl melden.
2. Rechtsklick aufs Junge -> "Follow me". Erwartet: "Your cub follows you.", Zeile 2 "following". 15 Kacheln weggehen: es rennt hinterher und
   bleibt 2-4 Kacheln hinter dir; stehenbleiben: es wartet neben dir. **Dazu (Nachbesserung B1): 30 s geradeaus gehen** -- es bleibt
   die ganze Zeit etwa 3-4 Kacheln hinter dir und bleibt NICHT immer wieder stehen.
3. Lange die Strasse entlang sprinten. Erwartet: es faellt zurueck; ab 40 Kacheln "could not keep up ... to the <Richtung>", "staying".
   Zurueckgehen, Rechtsklick "Follow me".
4. In ein Auto steigen. Erwartet: "cannot follow a vehicle", "staying".
5. In ein Haus gehen, Tuer hinter dir zu. Erwartet: es wartet draussen (ruhig, kein Hin-und-her-Rennen); Tuer auf -> es kommt nach. Treppe hoch:
   es wartet unten (ansehen und melden, ob es mitkommt).
6. Mit Q rufen. Erwartet: es kann kurz wegrennen, kommt aber sofort zurueck.
7. Speichern, Hauptmenue, laden. Erwartet: Junges da, folgt weiter, Schild "following".
8. Rechtsklick -> "Name the cub" -> "Bruno". Erwartet: Schild "Bruno", Meldung "Your cub is now called Bruno.". Mehr als 24 Zeichen oder "<" ->
   OK grau mit Hinweis.
9. "Stay here". Erwartet: es bleibt in der Gegend (wandert hoechstens ~12 Kacheln, Nachbesserung B7), Schild "staying".
10. Futter hinhalten: `NCBear_CubClean()`, `NCBear_CubFood()`, `NCBear_CubHere(12)` (scheues Junges, Balken dicht ueber dem Kopf). Rechtsklick auf
    den Boden -> "Hold out food for the cub" -> Fisch. Erwartet: Fisch in der Hand ohne Hingehen; stillstehen -> das Junge kommt bis ~3
    Kacheln; Rechtsklick aufs Junge -> Feed klappt **ohne Hinterherrennen**.
11. Waise: `NCBear_CubOrphan(8)` -> ein zweites Junges ohne Balken/Schild. 30+ Kacheln weggehen, nicht hinsehen, 3 Minuten warten (oder
    `NCBear_CubSweep()` zweimal mit 30 s Abstand von weit weg). Erwartet: es ist weg; `NCBear_CubLog(true)` zeigt "removed an orphan cub".
    Dein eigenes Junges bleibt.
12. `NCBear_CubKill()` am folgenden Jungen. Erwartet: "Your bear is dead ... 7 day(s)", Schild weg, keine roten Fehler.
Mehrspieler (dedizierter Server, Rolle user, zwei Spieler A und B; Sandbox Abklingzeiten 0):
1. Server startet ohne Fehler, beide verbinden, kein Kick.
2. A zaehmt (`NCBear_*` geht im MP nicht -- ueber Sandbox schnell), "Follow me", laeuft: beide sehen das Junge hinter A herlaufen (ruckelt es bei B?).
3. B sieht "<A>'s cub" / "belongs to A"; B hat im Rechtsklick kein "Follow me"/"Name the cub".
4. A nennt es "Bruno": B sieht "Bruno".
5. A trennt die Verbindung: das Junge bleibt stehen und wartet. A kommt wieder: "following", es folgt weiter (Nachbesserung A7).
6. Server neu starten: Name bleibt, Zustand "following"; nach dem Einloggen folgt es weiter (Nachbesserung A7). Kein Kick in keinem Schritt.
7. Waise im MP (A3 offen: `getObjectListForLua` am Server): eine Waise entsteht nur nach Fehlern -- Server-Log auf `[TC-BEAR] ***` pruefen.
   **Dazu (Nachbesserung A6):** den Server 3 Minuten OHNE Junges laufen lassen (der Waisen-Suchlauf kommt alle 2 min, auch ohne Junges)
   und im Server-Log nach `brain tick:` und `slow tick:` suchen. Keine solche Zeile = `getObjectListForLua` laeuft am Server.

---

## 9. Belege: jeder geplante Engine-Aufruf (Lesen: FB1B; "Nachbeleg" = vom Planer am 10.11. in den 42.22.2-Dateien gelesen)
| Nr | Aufruf | Beleg (gleiche Argumenttypen) | Seite | neu in B1b? |
|---|---|---|---|---|
| 1 | `p:getVehicle()` (Spieler) | `V:server/Vehicles/VehicleCommands.lua:11` `local vehicle = player:getVehicle()`; `V:client/ISUI/Hutch/ISHutchMenu.lua:8` (FB1B 1.1) | Schreiber, Client | Server: neu |
| 2 | `animal:fleeTo(square)` | `V:shared/TimedActions/Animals/ISMilkAnimal.lua:38` (FB1B 1.1), B1a gespielt | Schreiber | nein |
| 3 | `animal:getBehavior():setBlockMovement(b)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:89`, `V:shared/TimedActions/Animals/ISPetAnimal.lua:36` (FB1B 1.1) | Schreiber | nein |
| 4 | `animal:getX/getY/getZ`, `p:getX/getY/getZ` | `V:shared/Definitions/animal/ButcheringUtil.lua:575-577`; `B:server/BanditServerSpawner.lua:179` (FB1B 1.1) | Schreiber | nein |
| 5 | `getCell():getGridSquare(x, y, z)` | `V:server/Animal/ISPickDungCursor.lua:104` (FB1B 1.1) | Schreiber | nein |
| 6 | `animal:getModData()` (sofort nach dem Erzeugen) | `V:shared/Definitions/animal/ButcheringUtil.lua:596/602` (PZ 6.3, FE 5.2) | Schreiber | Ort neu |
| 7 | `getCell():getObjectListForLua()`, `:size()`, `:get(i)`, `instanceof(o, "IsoAnimal")`, `getAnimalType`, `getAnimalID`, `isDead`, `isExistInTheWorld`, `getSquare`, `isCanSee(nr)`, `animal:remove()`, `removeAnimal(id)`, `getOnlineID` | wie B1a `S:server/BanditsNPCBearWorld.lua:120-128`, `:248-256`, `:274-276` (MP-Server unbelegt, A3) | Schreiber | nein |
| 8 | `ISWorldObjectContextMenu.equip(p, p:getPrimaryHandItem(), food, true, false)` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:93` (Nachbeleg: in `onFeedAnimalFood` `:87-95`), FB1B 4 | Client | Ort neu |
| 9 | `ISTextBox:new(0, 0, 280, 180, titel, vorgabe, ziel, rueckruf, spielerNr, p1)`, `:initialise()`, `:addToUIManager()`, `.maxChars`, `.noEmpty`, `:setValidateFunction(t, f)`, `:setValidateTooltipText(text)`, `.entry:setMaxTextLength(n)`, `button.internal`, `button.parent.entry:getText()`, `getJoypadFocus(n)`, `:centerOnScreen(n)`, `setJoypadFocus(n, m)` | `V:client/ISUI/Animal/ISAnimalUI.lua:459-485`; Signatur und Rueckruf `V:client/ISUI/ISTextBox.lua:280`, `:127-137` (`onclick(target, button, param1, ...)`); `noEmpty` `V:client/ISUI/Maps/ISWorldMapSymbols.lua:203`; Pruefer `V:client/OptionScreens/CharacterCreationProfession.lua:1297`; `setValidateTooltipText` ist reines Vanilla-Lua (`ISTextBox.lua:117`, setzt nur `validateTooltipText`, gelesen `:176`), kein Engine-Aufruf; `setMaxTextLength` `V:client/ISUI/ISMPEditAccount.lua:19` (ISTextEntryBox, `ISTextEntryBox.lua:170-171`) (FB1B 3) | Client | neu |
| 10 | `getSpecificPlayer(0):getDescriptor():getForename()` | `V:client/XpSystem/ISUI/ISCharacterScreen.lua:84` (FB1B 2.4) | Client | neu |
| 11 | `playerObj:getPlayerNum()` | `V:client/ISUI/Animal/ISAnimalContextMenu.lua:1069` (Nachbeleg) | Client | neu |
| 12 | `Events.OnFillWorldObjectContextMenu`, `context:addOption`, `ISContextMenu:getNew`, `addSubMenu`, `notAvailable`, `addToolTip`, `setTest` | wie B1a (FB1B 4, PZ 6.3) | Client | nein |
| 13 | `isoToScreenX/Y(0, x, y, z)`, `drawTextCentre(text, x, y, r, g, b, a, UIFont.Small)` | `V:client/Fishing/TensionUI.lua:11-12`, `V:client/ISUI/ISUIElement.lua:1280` (FB1B 2.1) | Client | nein |
| 14 | `getTextManager():getFontHeight(UIFont.NewSmall)`, `drawTextCentre(..., UIFont.NewSmall)` | `V:client/Entity/ISUI/Controls/ISWidgetTitleHeader.lua:4`, `V:client/Foraging/ISSearchManager.lua:148` (Nachbeleg; FB1B 2.3 nennt `drawText` mit NewSmall `V:client/ISUI/Animal/ISAddDesignationAnimalZoneUI.lua:261`) | Client | neu |
| 15 | `sendClientCommand` / `OnClientCommand` / `sendServerCommand` / `OnServerCommand`, `getTimestampMs`, `B.Tell`/`B.SendView`/`B.Ask` | wie B1a (FE 6, PZ 6.3) | je Seite | nein |
| - | `string.byte`, `string.sub`, `string.len` | Lua-Grundbibliothek, kein Engine-Aufruf (FB1B 3) | beide | - |

**Nicht benutzt (auch nicht hinter pcall):** `pathToLocation` (erlaubt, aber unnoetig, 0.1), `setVariable("animalRunning", ...)` am Tier
(Grenzfall -> Frage 1), `setCustomName`/`getCustomName` (0.3), `isAnimalMoving`, `pathToCharacter`, `getData():setAttachedPlayer`,
`setShouldFollowWall`, `TextDrawObject:AddBatchedDraw`, `getAttachmentWorldPos` (kein `attachment head`), Vanillas Locken (`tryLure`,
`eatFromLured`, "ContextMenu_Lure"), `setDebugAcceptance`, `string.trim` (eigene Schleife). **Jar-only-Aufrufe in B1b: keiner.**

---

## 10. Fragen an Kevin (jede mit Empfehlung; nichts davon haelt den Bau auf)
1. **Gehen statt Rennen in der Naehe:** braucht `animal:setVariable("animalRunning", false)` -- dieselbe Methode wie am Spieler/Zombie, am
   Tier aber nur in der eigenen Test-Mod gesehen (FB1B 1.1, Grenzfall). Empfehlung: jetzt NICHT; mit dem neuen Modell (eigene, schnellere
   Clips) entscheiden. Bis dahin rennt das Junge beim Folgen immer.
2. **Name auch in Vanillas "Tier-Info"?** Ginge mit `setCustomName` (Vanilla-belegt), aber dort darf jeder Spieler jedes zahme Tier
   umbenennen -- wir muessten es im Takt zurueckdrehen. Empfehlung: spaeter mit dem Baeren-Fenster; jetzt nur unser Schild.
3. **Folgen-Deckel 40 Kacheln** (Sandbox 10-60) und **Bleiben-Radius 8** -- ok? Empfehlung: so lassen, im Test fuehlen.
4. **Treppen:** das Junge wartet unten, wenn du auf eine andere Ebene gehst (ob es Treppen kann, ist ungeprueft). Empfehlung: so lassen.
5. **Nach dem Zaehmen gleich "Folgen"?** Empfehlung: nein (steht auf "Bleiben", die Zaehm-Meldung sagt, wo man umschaltet).

---

## 11. Leistung (Ergaenzung zu PZ 7)
| Was | Wie oft | Deckel |
|---|---|---|
| Folgen je zahmem Jungen | je Hirn-Takt (1,5 s), reine Rechnung; Laufbefehl hoechstens je 1,2 s und nur bei Bedarf, festgesteckt nur je 10 s | Baeren je Spieler (Sandbox 1..4) |
| Spiegel-Probe | je Takt und Junges ein `getModData()` | - |
| Waisen-Suchlauf | je 120 s eine Objektliste (plus die B1a-Laeufe bei Bedarf) | Kandidaten 16 |
| Bitten Mode/Rename | hoechstens je 500 ms und Spieler | Drossel-Tabelle 64 |
| Client Schild | Liste 1 x/s, je Bild 2 Umrechnungen + 4 Texte je Schild | 6 Eintraege, 20 Kacheln |

Statisch geplant, nichts gebaut, nichts gespielt.

---

## 12. Nachbesserung B1b (11.11.2026, `nachbesserung_b1b.md`) -- aendert 1.2, 1.5, 1.6, 1.7, 3.3, 8.4, 9
- **1.2 Regel 10:** Besitzer nicht da -> das Junge **haelt und bleibt "follow"** (vorher: Bleiben). Damit ueberlebt der Zustand auch im
  MP Abmelden und Server-Neustart (Auftrag 1). `B.FollowLost` greift nur, wenn der Besitzer da ist und das Junge in dieser Sitzung schon
  ein Objekt hatte (nach dem Laden kein falsches "stayed behind").
- **1.2 "steckt fest":** gemessen am Weg des JUNGEN auf den Besitzer zu (`f.bx`/`f.by`), nicht am Abstand. Frei hinter einem gehenden
  Besitzer ist es nie fest; vor einer Tuer oder seitlich an einer Wand schon.
- **1.2 Regel 14/16 Vorhalt:** Halten und Ziel rechnen mit dem Ort, an dem der Besitzer im naechsten Takt etwa ist (sein Weg seit dem
  letzten Takt, hoechstens `followLead` 1,5 Kacheln). Abstand beim Gehen je Takt ~3,7-4,4 statt 5,3-5,9 (Attrappe). Bleibt er abrupt
  stehen, kommt das Junge bis auf ~0,5 Kacheln heran.
- **1.7:** `stayR` 12 (statt 8), neu `followLead` 1,5. Sandbox `BearTameFeedPoints` 4 / `BearTamePetPoints` 3 (Kevin 11.11.).
- **3.3 Drossel:** je "Spieler|Befehl|Ausgang", gezaehlt erst nach den Pruefungen; Deckel 128.
- **5.3 `B.CleanName`:** ohne `string.byte`; lehnt zusaetzlich unsichtbare/Steuer-/Richtungszeichen ab, Leerraum wie U+00A0/U+3000 am Rand weg.
- **9:** `string.byte` ist nicht mehr im Code (hatte keinen Vanilla-/Bandits-Aufruf). Jar-only-Aufrufe in B1b damit wirklich keiner.
- **10 Frage 3** gilt jetzt fuer `stayR` 12; neue Fragen an Kevin stehen in `nachbesserung_b1b.md` Abschnitt "Fragen an Kevin".
