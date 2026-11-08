# Baer kaempft - Nachbesserung (Fixer)

Stand 08.11.2026, PZ 42.21. Grundlage: `kampf_review_regeln.md` (7 Funde) und `kampf_review_technik.md` (7 Funde).
Gebaut unter `_arbeit/baer_kampf/mod` (nichts in `NCBearTest` kopiert, nichts unter NPC Crew `42`/`common`/`mod.info`
oder in einer fremden Mod geaendert). Kein toedlicher Fund; beide ernsten Funde der Regel-Pruefung und der ernste der
Technik-Pruefung sind behoben. **Statisch geprueft, nicht gespielt.**

## Was geaendert ist

| Fund | Stufe | Was jetzt gilt | Beleg |
|---|---|---|---|
| Regeln 1: Treffer durch Waende | ernst | Neues `canStrike(B, z)`: `a:CanSee(z)` und `not baerKachel:isSomethingTo(zielKachel)` (Wand, Tuer, Fenster an den Kanten). Gilt beim Treffer fuer **jedes** Ziel, Hauptziel eingeschlossen (in `hitList`, hoechstens 12 Pruefungen je Treffer), und bei der Ankunft: ein nahes Ziel hinter der Wand wird nicht angegriffen, er laeuft weiter bzw. drumherum; kommt er nicht hin, greift die Steckenbleib-Sperre. | Bandits `BanditUpdate.lua:1203-1206` (gleiche Form, IsoGridSquare/IsoGridSquare), Vanilla `ISBBQMenu.lua:108`; Jar `IsoGameCharacter.CanSee` 0-61 = `LosUtil.lineClear` (Sicht, Waende sperren), `IsoGridSquare.isSomethingTo` = isWallTo/isWindowTo/isDoorTo ueber `isEdgeElementTo` (prueft die Kanten beider Kacheln, auch zwei Kacheln in einer Reihe) |
| Regeln 2: Geist-Ziel bis 90 s | ernst | `targetOk`: `z:getCurrentSquare() == nil` -> kein Ziel. Dazu `dropVanished()` je Suchtakt (0,5 s): ein Durchlauf ueber `getZombieList` fuer alle Ziele; fehlt das Ziel dort, oder springt es zwischen zwei Takten ueber 8 Kacheln (dasselbe Objekt neu aus dem Pool), ist es weg. | Jar `IsoMovingObject.removeFromSquare` 38-45 (current/last null), `IsoZombie.removeFromWorld` 159-170 (`getZombieList().remove`); `getCurrentSquare` Bandits `BanditUpdate.lua:574` (Zombie), `ISAnimalContextMenu.lua:159` (Tier) |
| Regeln 3: Bandit im/unter Fahrzeug | klein | `F.IsTarget`: `z:getVehicle() ~= nil or z:isUnderVehicle()` -> nie Ziel. | Bandits `BanditMenu.lua:162-163` (am Zombie) |
| Regeln 4: frischer Koerper ohne Gehirn | klein | **verworfen.** Schaden faellt nur in `ApplyHit`, das jedes Ziel neu durch `F.IsTarget` schickt; der frueheste Treffer kommt 0,46 s nach der Wahl, das Gehirn schreibt Bandits beim ersten `OnZombieUpdate`. Uebrig bleibt hoechstens ein Bruellen (3 s) in Richtung eines frisch gespawnten Neutralen -- kein Angriff. Eine Marke im ModData fremder Zombies waere ein Schreibzugriff auf jeden Zombie fuer einen kosmetischen Fall. | `kampf_review_regeln.md` Fund 4, `NCBearFight.lua` `ApplyHit`/`hitList` |
| Regeln 5 / Technik 5: Baer verlaesst mitten im Kampf die Welt | klein | `scanBears`: verschwindet ein nicht toter Baer mit Marke oder Sperre, werden `NCBearAct`/Marken geloescht und die Sperre geloest, bevor er vergessen wird. `register` loescht die drei Variablen einmal (die Sperre absichtlich nicht: ein gerade gestreichelter Baer behielte sonst seine Vanilla-Sperre nicht). | `clearVariable` `ISPetAnimal.lua:48`; Jar `BaseAnimalBehavior.setBlockMovement` 14-24 (false schreibt nur zwei Felder) |
| Regeln 6 / Technik 4: Doppelschlag-Wahl mit alter Blickrichtung | klein | `face(B, ziel)` vor `F.ChooseAct` in `decide` und `updateApproach`. | `faceThisObject` `ISPetAnimal.lua:17` (wie bisher) |
| Regeln 7: Fehldiagnose "clips missing" | klein | Verfaellt ein Angriff, wird der Zustand gelesen; verliess der Baer `idle` (ab 0,5 s im Angriff gemerkt, oder beim Verfall nicht idle), heisst die Zeile "the bear left idle (Zustand)" und zaehlt nicht als fehlender Clip. Neuer Deckel: sechs abgebrochene Angriffe in Folge -> eine Zeile, 60 s Ruhe (sonst alle 2 s eine laute Zeile bis 90 s). | `getActionStateName` Bandits `ZASmack.lua:486` |
| Technik 1: Regel trifft weiter als der Clip | ernst | Weiten nach dem gemessenen Clip (Pranke 0,82, Schnauze 0,78, Doppelschlag 0,60 Kacheln vor der Mitte, `kampf_anim.md`): **Ankunft 1,1** (vorher 1,5), **Hieb 1,4** (1,8), **Doppelschlag 1,5** (2,0), **Biss 1,2** (1,7). Damit er am Gedraenge nicht haengt: kommt er in 3 s nicht 0,5 naeher, steht aber in Hiebweite und `canStrike` stimmt, schlaegt er von dort zu (Zeile "cannot get closer, strikes from x tiles") und bleibt fuer dieses Ziel bei der Hiebweite; sonst wie bisher 20 s Sperre. | `kampf_anim.md` Trefferstellen-Tabelle; Koerperkreis `collisionSize 0,42` (`NCBearDefs.lua:63`) |
| Technik 2: `pause` unter der Blendzeit | klein | `NCBear_Tune("pause", ...)` klemmt jetzt auf mindestens 0,3 (Vorgabe 0,35 unveraendert). | Jar `AnimLayer.findLiveNode` 36-59, `getOrCreateLiveNode` 6-15 (laut Pruefer) |
| Technik 3: Bruellen mit geschlossenem Maul | klein | `NCBear_Roar.wav` nur noch der erste Stoss mit Ausklang: Quelle 11,08-12,26 s statt -13,09 (1,18 s statt 2,01 s, Ausblenden 0,12 s, rms95 -11,0, Spitze -4,5). Im Clip endet der laute Teil (> -24 dBFS) bei 1,95 s, das Maul ist bis 2,07 s ueber 15 Grad offen. Blender nicht angefasst (weniger Risiko als den Kiefer im Clip zu verlaengern). | `sound/schnitt.py` (Eintrag Roar, Kommentar), `sound/schnitt.md` Tabelle; die fuenf anderen wav byte-gleich (MD5 vorher = nachher) |
| Technik 6: Abschluss-Kopie, `mod.info` "friedlich" | klein | `mod/42/mod.info` und `mod/mod.info` neu im Bau (nur die Beschreibung: kaempft im Einzelspieler gegen Zombies und feindliche Banditen, nie gegen Spieler, Crew, Neutrale, Tiere). Kopierregel unten. | `NCBearTest/mod.info` = `42/mod.info` (cmp), LF, ASCII |
| Technik 7: Netz an Brust/Achsel | klein | **nur notiert**, nicht geaendert: Gewichte zu aendern verschiebt Gang und Lauf, aus Spielhoehe kaum sichtbar (`kampf_anim.md` "Was unsicher bleibt" 2-4). | - |

Keine neuen Engine-Aufrufe ausser diesen, jeder mit Fundstelle und gleichen Argumenttypen: `getCurrentSquare()` (Zombie, Tier),
`IsoGridSquare:isSomethingTo(IsoGridSquare)`, `getVehicle()`, `isUnderVehicle()`. Kein `pcall` neu, kein neuer Global
(`F._canStrike` wieder raus, ungenutzt). Mehrspieler unveraendert: nichts angemeldet, kein Schaden.

## Pruefungen

* **Lua-Pruefer** (beide Dateien): luacheck 0, scopecheck 0, localcount hoechstens 57 insgesamt / 42 aktiv,
  luacheck_pz (auch `--unused`) nur die 2 x W113 auf den eigenen Global `NCBearFight` wie vorher. LF, ASCII, ohne BOM, keine
  Steuerzeichen. `NCBearDefs.lua` unveraendert (gegen `NCBearTest` nur der Tonblock anders, wie gemeldet).
* **Attrappe** `_arbeit/baer_kampf/attrappe/test_fight.lua` (Engine-Nachbau um `getCurrentSquare`, `isSomethingTo`,
  `getVehicle`, `isUnderVehicle`, festsitzenden Baeren erweitert): **110 Pruefungen gruen** (vorher 79), auch mit `LOGLVL=2`.
  Neu 13-23: Geist ueber `removeFromWorld` und `removeFromSquare`, Pool-Sprung (kein Nachrennen), Neben- und Hauptziel hinter
  Wand/Fenster (0 Treffer, kein Hieb gegen die Wand), Baer verlaesst die Welt und kommt mit Marke zurueck, Fahrzeug, Angriff erst
  ab 1,27, Hieb trifft 1,3 und nicht 1,51, Zuschlagen aus 1,3 bei Steckenbleiben / Sperre bei 2,2, keine Fehldiagnose ausserhalb
  idle samt Deckel, `pause` >= 0,3, Doppelschlag bei Menge hinter der alten Blickrichtung. Die Pruefer-Proben P1-P5 stecken
  darin. **Gegenprobe:** 12 Mutationen (je eine Nachbesserung zurueckgenommen, dazu die alten Weiten): 11 fallen auf;
  nur `face` in `decide` allein nicht (die Probe kommt ueber das Anrennen, dort steht dasselbe `face`) -- beide `face` zusammen
  fallen auf. Probe 14 wurde dafuer verschaerft (Ziel weg bei der naechsten Entscheidung, nicht erst nach der Sperre).
* **Probe.java** auf `NCBear.glb`: unveraendert (MD5 `2e9a6d17b7f6...` = `kampf_anim.md`), 10 Clips, Dauern 3,0/1,1/1,1/2,2/1,6 =
  `F.ACTS`, `ohne_keys` ueberall leer; Ausgabe `_arbeit/baer_kampf/probe_fix.txt`. Knoten-XML: Clipnamen und Treffer-`m_TimePc`
  0,42/0,57/0,34 = `F.ACTS`. Textur MD5 `58a4ea416596...` unveraendert.
* **Ton:** Roar neu gemessen (mono, 44,1 kHz, 16 Bit, 1,180 s, erster/letzter Wert 0/1 LSB, DC -0,16 LSB), Spektrogramm
  `sound/schnitt_NCBear_Roar.png` neu und angesehen; die fuenf anderen wav und Bilder byte-gleich.
* Gerendert wurde nichts (kein Clip geaendert); das Spiel lief beim Abschluss nicht.

## Abschluss-Kopie (fuer den Integrator)

Nur **hinzufuegen und ueberschreiben, nie spiegeln oder loeschen** -- in `NCBearTest/42` liegen Dateien, die nicht aus diesem Lauf
stammen (`client/NCBearSpawn.lua`, `NCBearTest.lua`, `NCBearSize.lua`, `NCBearAttackProbe.lua`, `Translate/EN/IG_UI.json`,
`scripts/nc_bear.txt`, `nc_bear_tier.txt`, `NCBearDeer.glb`, `WorldItems/*`, `Item_NCBear.png`).

| aus `_arbeit/baer_kampf/mod/` | nach `C:/Users/Kevin/Zomboid/mods/NCBearTest/` |
|---|---|
| `42/media/AnimSets/buck/idle/NCBear_{Rear,SwipeL,SwipeR,Slam,Maul}.xml` | neu |
| `42/media/lua/shared/NCBearFight.lua` | neu |
| `42/media/lua/shared/NCBearDefs.lua` | ueberschreiben (Tonblock) |
| `42/media/models_X/Skinned/NCBear.glb`, `42/media/textures/Body/NCBear.png` | ueberschreiben |
| `42/media/scripts/nc_bear_sounds.txt`, `42/media/sound/NCBear_*.wav` (6) | neu |
| `42/mod.info`, `mod.info` | ueberschreiben (nur Beschreibung) |

## Was nur Kevins Test entscheidet

* Kommt er mit Ankunft 1,1 an den Zombie heran, oder steht oft "stuck on the way" / "cannot get closer" in der Konsole?
  Dann `NCBear_Tune("arrive", 1.3)`. Sieht die Pranke jetzt am Zombie aus statt in der Luft?
* Haelt die Wand-Regel ohne Fehlschlaege an Zaeunen und Moebeln (ein niedriger Zaun zaehlt je nach Kachel als Kante)?
* Klingt das kuerzere Bruellen (1,18 s) noch kraeftig genug?
* Alles weitere wie in `kampf_lua.md` "Was nur Kevins Test entscheidet". Mehrspieler bleibt offen.

Statisch geprueft, nicht gespielt.

## Integrator 08.11. (nach kampf_review_gegen.md)

* Gegenpruefung Fund 1 behoben: `canStrike` fragt `isBlockedTo(zsq)` oder `isWindowTo(zsq)` statt `isSomethingTo` (Vanilla
  `ISInventoryTransferAction.lua:598`, gleiche Typen; Jar `IsoGridSquare.isBlockedTo` 0-40). Offene Tuer frei, sonst wie vorher.
* Fund 2 behoben: `B.stucks` je Kampf, beim dritten unerreichbaren Ziel `endFight("targets unreachable", restAfter)`.
* Attrappe 118/0 (neu 24/25: offene Tuer, Fenster, Pendel-Deckel); alter Stand faellt dort 5x durch, zwei Mutationen fallen auf.
  Pruefer: luacheck 0, scopecheck 0, localcount max 58, luacheck_pz nur die 2 x W113 auf `NCBearFight`. LF, ASCII.
* Offen (klein, nicht gebaut): 3 Suchkosten bei vielen Baeren, 4 Leine/Baum, 5 Biss selten, 7 Engine-Sperre im Schlaf.
* Kopiert nach `NCBearTest` (18 Dateien, MD5 gleich), Spiel lief nicht. Sicherungen `backups/NCBearTest/NCBearTest_vor_kampf_*.zip`
  und `..._mit_kampf_*.zip`. Statisch geprueft, nicht gespielt.
