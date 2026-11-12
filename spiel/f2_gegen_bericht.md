# Lauf baer-f2 (= B5a Kampf): GEGENPRUEFUNG nach der Nachbesserung

Stand 12.11.2026 nachmittags. Rolle GEGENPRUEFER (nichts davon gebaut, keinem Bericht geglaubt, alles selbst gelaufen bzw. am Code gelesen).
**Statisch geprueft, nicht gespielt.** Nichts im Staging, in der Test-Mod, in NPC Crew, Vanilla oder Bandits geaendert; kein git, kein Spielstart,
kein Download. Eigene Pruefskripte und Ausgaben: `_arbeit/baer_zaehmen/attrappe/gegen_f2/` (neu; Probe-Ordner nur im Scratchpad).

## 0. Urteil zuerst

- **Bereit fuer Kevins naechsten Einzelspieler-Test: JA.** Kein Blocker, keine rote Linie gerissen (Belege unten).
- **Alle 20 Befunde am heutigen Code nachgeprueft:** 18 geschlossen, 2 bewusst als Frage an Kevin offen (B6 Teil 2, B10 gebaut nach Empfehlung
  + Frage). **Kein Befund zu Unrecht abgelehnt** (die Nachbesserung hat keinen abgelehnt; die Begruendung fuer B6 Teil 2 traegt). **Die
  Nachbesserung hat nichts kaputt gemacht**, das ich finden konnte: alle Zahlen gleich wie im Nachbesserungs-Bericht, alte Attrappen byte-gleich.
- **Bekannt, kein Blocker:** der Trockenlauf meldet genau 1 Fehler "NPC Crew hat Sprachen, die das Skript nicht kennt: DE" (Kevins Wahl).
- **4 neue Kleinbefunde (R1-R4, alle minor, keiner verhindert den Test)**, Abschnitt 4.
- MP bleibt ungespielt und ehrlich offen (B9, Server-Fragen am Tier, Abschnitt 5).

## 1. Selbst gelaufen (Zahlen)

| Pruefung | Ergebnis |
|---|---|
| `staging_dateien.txt` gegen die Platte (eigenes Skript `gegen_f2/zaehle.py`, MD5 + Bytes) | **95 / 95**, keine fehlt, keine zu viel, 0 Abweichungen |
| Status je Datei gegen die Test-Mod NCBearTest neu gerechnet | **17 neu, 50 ueberschreibt, 28 gleich** -- stimmt Zeile fuer Zeile mit der Liste |
| Form (83 Text-Dateien im Staging + Skript + NAEHTE) | alle LF, kein CR, LF am Ende; Lua/XML/TXT reines ASCII; 21 JSON: Round-Trip `json.dumps(indent=4, ensure_ascii=False) + "\n"` byte-gleich und sortiert |
| `luacheck.py` (56 Lua) | 56 geprueft, **0 failed** |
| `scopecheck.py` | **0 violations** |
| `localcount.py` | hoechstens **52 aktiv** (`ISUI/BanditsNPCBearHud.lua`), hoechstens **77 insgesamt** (`server/BanditsNPCBearWorld.lua:699`) -- alles unter 180 |
| `luacheck_pz.py` (56 Lua) | **46 x W113**, alle erklaert: 7 Zeitaktions-Klassen in `client/BanditsNPCBearMenu.lua` (global definiert in `shared/TimedActions/*.lua`, z. B. `BanditsNPCBearMendAction.lua:37`) + 39 Werkbank-Globale, je in einer anderen Werkbank-Datei definiert (stichprobenweise nachgesehen: `NCBear_FightNext` `NCBearBenchFight.lua:199`, `NCBearBenchClip` `NCBearBench.lua:81`, `NCBearMenu` u. a.) |
| `luac5.1 -p` | 56 / 0 |
| `attrappe/f2_kern/run.lua` | **166 / 0** |
| `attrappe/f2_ober/run.lua` | **291 / 0** (Kern-Attrappe), **292 / 0** (echter Kern) |
| `attrappe/gesamt/run.lua` | **3333 / 0** (nur die drei gewollten Heil-Zeilen 18c, 19f, 20e) |
| `attrappe/pruef_f2/run.lua` (Pruefer B) | **14 ok, 0 Befunde** |
| `attrappe/nach_f2/kern.lua` | **25 / 0** |
| `attrappe/nach_f2/ober.lua` | **23 / 0** mit Kern-Attrappe und mit echtem Kern |
| Alle alten Attrappen (Kopie von `f2_ober/alte_laufen_f2.py`, TMP im Scratchpad; 31 Laeufe) | **byte-gleich** mit `attrappe/nach_f2/alte_nach.txt`. Rot nur die gewollten: `b1d_kern` 161/1 (B6: jetzt ein getHealth je Hirn-Takt), `pruef_b1d` P1d (11.6), `pruef_b1e` 20/5 (seit nachbesserung_b1e bekannt), OBER-Attrappen b1c/b1d/b1e/f1/nach_f1/f1b (neue Option TagDodge in der Liste, Big-Zahl 39, Fensterhoehe 682/1281, "comes later" entfernt) -- alle selbst an den Fehlerzeilen gelesen (`gegen_f2/alte_attrappen.txt`) |
| `attrappe/gesamt/xref_f2.py` | **0 Luecken**; nach dem Einbau 61 Testbefehle (heute 55), **verloren 0, doppelt 0**, alle in `NCBearBench*` |
| `attrappe/gesamt/gegenprobe_f2.py` (TEMP im Scratchpad) | **18 von 18** Verderbnissen erkannt, unveraendert gruen |
| `attrappe/uebernahme_f2/probe_regeln_f2.py` (TEMP im Scratchpad) | **16 von 16** wie erwartet |
| `attrappe/nach_f2/texte_pruefen_nach_f2.py` | **OK** (345 Schluessel je Sprache; RU "Show damage" 153 px in der 189-px-Zelle) |
| Fundstellen (eigenes Skript `gegen_f2/refs.py`) | **294** `V:`/`B:`-Zeilenangaben in den 40 kopierten Lua-Dateien: jede Datei da, jede Zeile da (Bandits 42.22 + common, Vanilla) -- 0 fehlend; Inhalt stichprobenweise gelesen (A1-A3, Verband, Aufhelfen, Biss, Locken) |
| Trockenlauf `--staging _arbeit/baer_zaehmen/mod` | **1 Fehler (DE, bekannt), 2 Warnungen** (Junges-GLB ohne 10 buck-Clips; NPC-Crew-Kommentar `shared/BanditsNPC.lua:1410`), **"keine Altlasten mehr"**; 40 Lua + 35 Dateien zum Kopieren; 6 Stummel "wird nie kopiert" |
| Trockenlauf mit `--vor-b5a` | identisch bis auf die Kopfzeile |
| Trockenlauf Einbau-Stand (Staging ohne die 2 NICHT-KOPIEREN-Dateien) | 1 Fehler (DE), 2 Warnungen; nimmt `NCBearCub.glb` **d9931d32** aus der Test-Mod (15 Clips) |
| `--probe` Original | 1 Fehler (DE) -> **nicht geschrieben** (so gewollt) |
| `--probe` mit der DE-Warnungs-Kopie (`f2_werkzeug/baer_uebernahme_de_warnung.py`; per diff: **genau 1 Zeile** anders, Skript-Zeile 1057) | **0 Fehler, 3 Warnungen, 97 Dateien geschrieben**; luacheck/scopecheck/localcount je kopierter Datei ok (hoechstens 77); luacheck_pz 0 Treffer + 7 erlaubt |
| Gesamt-Attrappe gegen die geschriebene Probe (ohne Werkbank) | **3333 / 0** |
| geschriebene Probe auf Testhilfen durchsucht | kein `NCBearBench*`, kein Stummel, keine `function NCBear_*` / `NCBear_* =` in den kopierten Dateien |
| Kollisionsprobe der neuen Namen (FightUnmiss, Why_BandageOff, fxFoeDist, lureCandMax, foeCandZ/B, growlCdMs, fightMiss*, fightLeashPad, missBl) | 0 Treffer in NPC Crew `42/media/lua` und Landkarte |
| Eigene Stichproben `gegen_f2/stich.lua` (Abschnitt 3) | **27 / 0** |

### 1.1 Was der Einbau in der Test-Mod tut (nur gewollt)

Aus `staging_dateien.txt`, gegen NCBearTest nachgerechnet (`gegen_f2/zaehle_ergebnis.txt`):
- **17 neu:** 2 Zombie-Knoten `AnimSets/zombie/bumped/BanditsNPCBearZBite*.xml`, `client/BanditsNPCBearFx.lua`, `server/BanditsNPCBear{Fight,FightFoes,Hurt,Mend}.lua`,
  `shared/BanditsNPCBear{FightRules,Foe}.lua`, `shared/TimedActions/BanditsNPCBear{Help,Mend}Action.lua`, 5 Werkbank-Lua
  (`NCBearBench{Adult,AttackProbe,Fight,Model}.lua`, `shared/NCBearBenchDefs.lua`), `scripts/NCBearBenchStag.txt`.
- **6 Stummel ersetzen alte Dateien** (je 2 Kommentarzeilen "Umbenannt nach ...", kein Code, selbst gelesen): `client/NCBearAttackProbe.lua` (alt 12914 B),
  `client/NCBearSize.lua` (1421 B), `client/NCBearSpawn.lua` (4714 B), `client/NCBearTest.lua` (5933 B), `shared/NCBearDefs.lua` (6171 B),
  `shared/NCBearFight.lua` (100260 B). Danach laedt nichts doppelt; die Uebernahme kopiert sie nie (Trockenlauf "Stummel ... wird nie kopiert").
- **44 weitere ueberschrieben, davon 41 wirklich kopiert:** 9 Client-Dateien des Baeren, 8 Server-Dateien, 3 shared (`BanditsNPCBear`, `...Crew`, `...Defs`),
  4 Werkbank-Lua + `NCBearBenchGenDefs.lua`, 7 x `Sandbox.json`, 7 x `UI.json`, `EN/IG_UI.json`, `sandbox-options.txt`, `scripts/nc_bear_tier.txt`
  (**bedingt**: Test-Mod heute 2a7c5ab1 -> ja). **NICHT KOPIEREN** (Test-Mod neuer): `models_X/Skinned/NCBearCub.glb` (Test-Mod d9931d32,
  Staging alt 6c3f0a96) und `textures/Body/NCBearCub.png` (Test-Mod 2e627a1b) -- in der Liste so gefuehrt.
- **Unberuehrt bleiben** alle Modelle, Texturen, Toene, Buck-Knoten, `scripts/nc_bear*.txt` ausser tier, die Generator-Werkbank (`NCBearGen*`) und
  `shared/NCBearBenchVergleichDefs.lua` (nicht im Staging; sie macht nur `require "BanditsNPCBearDefs"` und liest `ncbearcub` -- laedt weiter).

## 2. Befunde am heutigen Code

| ID | Urteil | Beleg am heutigen Code |
|---|---|---|
| A1 | **geschlossen** | `shared/TimedActions/BanditsNPCBearHelpAction.lua:13, :49-50` nennen jetzt `ISAddFuelAction.lua:41-42`; dort stehen `setActionAnim("Loot")` / `SetVariable("LootPosition", "Low")` (gelesen) |
| A2 | **geschlossen** | `shared/BanditsNPCBearFoe.lua:301` -> `B:client/BanditUpdate.lua:421`: `bandit:setTarget(nil)` an einem Zombie, nicht auskommentiert (gelesen; :1748-1751 ist weiter `--[[ ]]`) |
| A3 | **geschlossen** | 294 Zeilenangaben loesen auf (Abschnitt 1); MendAction `ISFeedAnimalFromHand.lua:6` / `:54`, `ISApplyBandage.lua:61-62/:70`, `ISAddFuelAction.lua:48`, `ISPetAnimal.lua:5-12` gelesen -- Methode und Argumenttyp gleich |
| A4 | **geschlossen** | Grow.lua:261-263, Skript `baer_uebernahme.py:29`, `:385`, `:479` und NAEHTE verweisen auf den Wortlaut `baer/STAND.md` "Fragen fuer Kevin" Nr. 9 (dort :246-247) + `begleiter/ENTSCHEIDUNGEN.md` "Kein Schaden am eigenen Baeren" (:400); keine Zeilennummer mehr |
| A5 | **geschlossen** (Text), Frage an Kevin | `UI_BN_Bear_Win_KillsTip` in 7 Sprachen ehrlich ("... even if someone else landed the last blow"); Code `server/BanditsNPCBearFight.lua:444-470` unveraendert |
| A6 | **geschlossen** | RU "Показ урона" 153 px < 189 px (Text-Pruefer selbst gelaufen); im Spiel ansehen |
| A7 | **geschlossen** (Herkunft offen benannt), Frage an Kevin | `shared/BanditsNPCBearFoe.lua:188-206`: eigene Namen `awayX/awayY/awayLen`, Kommentar "gelernt aus B:shared/ZombieActions/ZAPush.lua:33-39". Gegen ZAPush gelesen: es bleibt die Standard-Rechnung (Skalarprodukt / Laenge > 0,5), sonst eigener Ablauf (Zurueckfliegen, Schieben). Kevin entscheidet |
| A8 | **geschlossen** fuer die 6 genannten Stellen | Fight.lua (Probeweg :416-417), `shared/BanditsNPCBearCrew.lua:12-13`, `...FightRules.lua:1-12`, `...Defs.lua:191/:193` neutral; Trockenlauf-Warnung weg. Rest siehe **R1** |
| A9 | **geschlossen** | `baer/tools/baer_uebernahme.py:1856` "33-39" = `baer/NAEHTE.md:21` |
| A10 | **geschlossen** (Doku) | Skript-Kopf `baer_uebernahme.py:28-31` und NAEHTE-Kopf nennen alle drei Jar-Ausnahmen; `begleiter/ENTSCHEIDUNGEN.md:352` belegt getTextOrNull |
| B1 major | **geschlossen** | `server/BanditsNPCBearFight.lua:339-345`: kein Kampfbeginn, wenn der Baer weiter als `fightLeash - fightLeashPad` (12) vom Anker steht -> Zombie-Wache/Folgen holen ihn; Ende weiter erst bei > 14 (:688-690) -> kein Pendeln. Knurren je Baer hoechstens alle 10 s (:229-239). Attrappen pruef_f2 P1, nach_f2 N1 gruen. Rest-Verhalten siehe **R4** |
| B2 major | **geschlossen** | `server/BanditsNPCBearFightFoes.lua:122-221`: Rahmen nur Vorfilter, dann KREIS je Baer, je Baer die naechsten 24 Zombies und GETRENNT die naechsten 8 Banditen (`sortIn`), kein globaler 64er-Deckel mehr; Locken ebenso (`shared/BanditsNPCBearFoe.lua:399-458`, je Baer 12). P2, N7, N8 gruen. Rest siehe **R2** |
| B3 major | **geschlossen** | `server/BanditsNPCBearFight.lua:640-648` (in Weite, nicht treffbar -> kein Luftschlag, Fall zaehlen), :697-702 (Treffer 0 wegen Wand), :148-175 (nach 2 Faellen 8 s Sperre IN DER SITZUNG, Deckel 32), :201 (Ziel-Wahl beachtet die Sperre), `server/BanditsNPCBearHurt.lua:88` (Biss dieses Gegners hebt die Sperre auf). `CanSee` ist reine Sichtlinie (J:`dec_b1b/IsoGameCharacter.java:4854-4866`, selbst gelesen). P5 jetzt 0 Luftschlaege. Rest siehe **R3** |
| B4 major | **geschlossen** | `shared/BanditsNPCBearFoe.lua:678-689`: `pcall(ui.FightFx, ...)` um EIGENEN Code mit gedrosselter Meldung; Reihenfolge Fx vor `B.Close` begruendet und mit dem pcall unschaedlich. P6 jetzt Register zu, Koerper tot; eigene Stichprobe S1 (Tod) gruen |
| B5 | **geschlossen** | Fight.lua:382 (`B.FightState` am Boden nil), Hurt.lua:151 (`s.fstNow/fstSent` weg). Stichprobe S1b: am Boden fst nil |
| B6 | **Teil 1 geschlossen**, Teil 2 Frage an Kevin (Ablehnung **berechtigt**) | `server/BanditsNPCBearGrow.lua:689-694`: Abgleich Koerper <-> Register jeden Hirn-Takt (ein getHealth je geladenem zahmen Baeren, kein Bild-Takt). Teil 2 ("fremder Tod = Koerper weg") wuerde eine zerlegbare Leiche neben einem per C1 wiederkehrenden Baeren lassen -- das waere eine Verdopplung (rote Linie); erst im Spiel klaeren, ob ueberhaupt etwas am Schutz vorbei toetet |
| B7 | **geschlossen** | `server/BanditsNPCBearMend.lua:82` lehnt bei `BearBandageHeal <= 0` VOR jedem Verbrauch ab; `client/BanditsNPCBearMenu.lua:425` zeigt denselben Grund. Stichprobe S3 gruen |
| B8 | **geschlossen** | `client/BanditsNPCBearFx.lua:213-215`: DODGE nur bei `mine(id)` (Sicht: eigener zahmer Baer, :166-170) |
| B9 | **verbessert, MP offen** | `shared/BanditsNPCBear.lua:653-687`: hit/zbite/smack an Spieler bis 75 Kacheln (unter Ladeweite 76), Rest 40, hoechstens 32 Empfaenger. Ungespielt (MP) |
| B10 | **gebaut nach Empfehlung**, Frage an Kevin | Fight.lua:305-308: Pause "long" nur nach 90 s OHNE eigenen Treffer; Muedigkeit bleibt bei der Ausdauer (R7) |

**Nachtrag Kevin 11.x (PLAN_F2.md 11) mitgeprueft:** 11.1 Show damage (Fx.lua: Zahl nur fuer den eigenen Baeren, Schalter), 11.2 Melee damage
(`B.MeleeDamage` `shared/BanditsNPCBearFightRules.lua:315`, vom Kampf selbst benutzt: Fight.lua:490), 11.4 Lerntempo (`xpPerMin = 2`,
`skillCapAt = {3,6,8,10}`, `shared/BanditsNPCBear.lua:148-149`; Sandbox `BearSkillXpPercent`/`BearSkillAgeCap`), 11.5 Kills (Fight.lua:432-470,
Tooltip ehrlich), 11.6 Schutz + Abgleich je Hirn-Takt (Grow.lua:688-694), 11.7 Fliehen nach Treffern (`B.FleeHp` FightRules.lua:295-307,
Vorgabe 3, Hysterese; Stichprobe S1: Rueckzug bei 14,2 < 21,6 Lebenspunkten). Alle Attrappen dazu gruen.

## 3. Eigene Stichproben (`attrappe/gegen_f2/stich.lua`, 27 / 0, echter Kern auf der Engine-Attrappe der Bauer)

**S1 Zombie beisst den grossen Baeren, er kaempft, flieht, stirbt (Vorgaben).** Zeile fuer Zeile gelesen und durchgespielt:
1. Hirn-Takt `server/BanditsNPCBearServer.lua:1027-1055`: der zahme, geladene, nicht mitfahrende Baer kommt in `B._fightLive`; `B.FoeScan(force)`
   (FightFoes.lua:243-308) legt `B._foes[id]` an (Kreis je Baer, `B.FoeIsTarget`).
2. Kampf-Takt (Fight.lua:790-792, 728-761): `B.FoeAttackTick` (FightFoes.lua:421-462) beginnt je Zombie in `B.FoeReach` einen Biss (Fx `zbite`
   -> `onBite` Foe.lua: eigener Bump-Knoten), Deckel 4 Angreifer am grossen Koerper; nach der Uhr `lands` (Ebene, Weite + 0,25, liegt nicht,
   `isSomethingTo`) -> `B.BearHurt` (Hurt.lua:74-132): Ausweichen-Wurf, `B.BodyHurt` (Schutz kurz aus, Grow.lua:302-315), Erfahrung
   Agilitaet/Zaehigkeit, Fx `hurt`, Flucht-Meldung.
3. `liveRec` (Server.lua:812) -> `B.FightStep` (Fight.lua:289-353): `B.FightDecide` (FightRules.lua:369-388) "fight" -> Leine ok -> `pickTarget`
   -> `begin` (Knurren). Kampf-Takt `tickBear` -> `approach` -> `choose` -> `enterAct` (Ausdauer, Kondition) -> `strike` nach der Uhr -> Fx `hit`
   -> `B.FoeHurt` (Foe.lua:236-260) am Zombie.
4. Leben unter `B.FleeHp` -> R6 "retreat": `B.FightDrop`, `s.fleeOn`, Rueckgabe false -> `B.GuardStep` versteckt ihn hinter dem Besitzer
   (`B.GuardDecide` Rules.lua:668-712). **Ergebnis:** 14 eigene Treffer, 43 Bisse; Rueckzug bei 14,2 Leben (Schwelle 3 x 7,2 = 21,6);
   Meldung "Note_Flee"; **danach kein eigener Angriff mehr**.
5. Weitere Bisse -> Leben <= 0, Besitzer da, `BearCannotDie` aus -> `B.BearDie` (Hurt.lua:232-242): Fx `dead` **genau einmal**, Kampf und
   Angriffe weg, `B.Close(rec, "dead")` (Register ZUERST), dann `B.BodyDie` (Schutz aus, Ersatz-Angreifer, Leben 0). **Ergebnis:** Eintrag zu,
   Koerper tot, Meldung "Note_BearDead", 0 laufende Bisse, **kein zweiter Baer**, 5 weitere Takte ruhig.
- **S1b mit `BearCannotDie`:** am Boden statt Tod, Koerper lebt, **keine weiteren Bisse**, Sicht fst nil (B5), `B.HelpUpComplete` -> steht mit 45 %.
- **S2 Mitfahren:** waehrend `rec.ride` rechnet `B.BearHurt` nichts (Hurt.lua:75), laufende Bisse fallen weg (FightFoes.lua:436), kein Kampf
  (Fight.lua:750), Eintrag bleibt. Einsteigen am Boden ist gesperrt (`server/BanditsNPCBearRide.lua:130`), "Come" am Boden ebenso (`Order.lua:278`).
- **S3 Verband:** `complete` nimmt **genau 1** (`B.TakeOne` Server.lua:188-198 prueft danach, dass er weg ist), ein zweiter `complete` waehrend
  der Verband wirkt nimmt **nichts** (Why_Bandaged), ein schon verbrauchtes Stueck nimmt nichts (Why_NoItem), Heilung 0 nimmt nichts (B7).
  Abbruch: `stop()`/`forceStop()` (MendAction.lua:74-83) rufen den Kern nie -- nichts weg; der vorher aus der Tasche geholte Verband liegt dann
  im Hauptinventar (nicht verloren).
- Ehrliche Grenze der Attrappe: sie teleportiert den Baeren beim Laufbefehl; meine Zombies "laufen" ihm im Fall S1 nach (im Spiel macht das
  das Locken, Foe.lua:553-594). Kein Engine-Verhalten bewiesen.

## 4. Neue Kleinbefunde (alle minor, keiner verhindert den Test)

- **R1 (Rest von A8):** 25 Kommentare in kopierten Dateien belegen "gespielt" mit Dateien, die nach dem Einbau Stummel sind
  (`NCBearTest shared/NCBearFight.lua:...` z. B. Fight.lua:33, :105, :226, :553, FightFoes.lua:86, Guard.lua:16, :175, Foe.lua:38, :139, :154,
  :188, :235, :302, :485-486; `NCBearDefs.lua` Defs.lua:6, :22, :37, :51, :174, :227; `NCBearAttackProbe.lua` Grow.lua:242; `NCBearSpawn.lua`
  World.lua:539; `NCBearSize.lua` Stats.lua:412). Kein Code, keine Cheat-Spur; der Inhalt steht weiter im Git der Test-Mod (main db80ad6).
  Vorschlag bei Gelegenheit: "(Git NCBearTest db80ad6)" dazuschreiben.
- **R2 (Rest von B2):** die 8 Banditen-Plaetze je Baer werden VOR `B.FoeIsTarget` vergeben (FightFoes.lua:149-150, Filter erst :269-270).
  Stehen mehr als 8 freundliche Banditen/Crew-Figuren naeher am Baeren als ein feindlicher, sieht er den feindlichen erst, wenn der naeher kommt.
  Nur mit NPC Crew/Bandits (nicht in Kevins Test). Vorschlag: Freund-Pruefung (Gehirn-Felder) vor `sortIn` oder foeCandB groesser.
- **R3 (Rest von B3):** steht ein Zombie dauerhaft hinter einem Fenster/Zaun in Leinen-Weite, laeuft ein Kreis: nach 8 s Sperre neuer Kampf,
  zwei Fehlfaelle (~1-2 s), dann 3 s "seek" mit Halt (Fight.lua:712-718), Knurren hoechstens alle 10 s. Kein endloses Haengen, aber beim Folgen
  bleibt er so je ~12 s etwa 4-5 s stehen, bis der Zombie aus der Leine faellt. Vorschlag: nach einer Sperre ohne weiteres Ziel sofort
  `FightDrop` statt "seek".
- **R4 (B1-Umfeld, alte B1c-Wache):** Besitzer mehr als 12 Kacheln weg (kein Kampfbeginn) UND mehr als 10 (`hideOwnerMax`, kein Verstecken),
  Zombie <= 6 am Baeren -> die Wache laesst ihn VOM Zombie weg rennen statt zum Besitzer (`shared/BanditsNPCBearRules.lua:691-711`); er kommt erst
  nach "sicher" (9 Kacheln, 3 s) per Folgen zurueck. Erholt sich, kein Haengen. Dazu passt die alte offene Frage B1c Nr. 5
  (`baer/spiel/b1c_gegen_bericht_b1c.md:141-142`, "lieber stehen bleiben? Empfehlung: ja, zusammen mit B5a") -- in F2 nicht gebaut.

## 5. Offen / ehrlich (kein Blocker fuer den SP-Test)

- **MP ungespielt:** Fx-Weite 75 (B9), `CanSee`/`faceThisObject` nur SP, Kachel-/`isProne`-Fragen und `getHealth` am Tier beim Server (GRENZFAELLE
  laut Plan), Verband-/Aufhelfen-Netzaktion. Im Bericht als offen gefuehrt.
- **Laufzeit-Vermutungen:** ob der eigene Zombie-Biss-Knoten im Spiel sauber endet (`BumpAnimFinished`), ob `playBreedSound` die Stimmen der Rasse
  spielt, ob "DODGE" und die Schadenszahl gut sitzen, ob die Balance (Bisse vs. Hiebe) passt -- nur im Spiel zu sehen.
- **Lerntempo:** mit Vorgabe 100 % und `xpPerMin` 2 bewegen sich die Faehigkeits-Balken im Test nur wenig (Absicht, Kevin 11.4). Fuer den Test die
  Sandbox "Bear: skill learning speed" hoch stellen oder `NCBear_CubXp` nehmen (Anleitung).

## 6. Fragen fuer Kevin (gebaut ist jeweils die Empfehlung)

1. **B10:** Pause nach 90 s Kampf nur, wenn er so lange nichts getroffen hat? (Empfehlung ja, gebaut.)
2. **B6 Teil 2:** Tod am Schutz vorbei (Feuer? Explosion? ungeprueft) zaehlt heute als Tod mit Trauer-Sperre -- so lassen, bis im Spiel klar ist,
   ob es das ueberhaupt gibt? (Empfehlung ja.)
3. **A5:** Kill-Zaehler zaehlt auch, wenn du/eine Figur den vom Baeren getroffenen Zombie in den 2 s danach erledigst -- so lassen? (Empfehlung ja.)
4. **A7:** Die 5-Zeilen-Rechnung "von hinten getroffen" ist dieselbe Mathematik wie in Bandits, mit eigenen Namen und Herkunft im Kommentar -- ok?
5. **B7:** Verband-Heilung 0 in der Sandbox -> Verband wird abgelehnt (bleibt im Inventar) -- ok? (Empfehlung ja.)
6. **R4 / B1c Nr. 5:** Wenn du weit weg bist (> 10 Kacheln) und ein Zombie am Baeren steht: lieber stehen bleiben (bzw. zu dir laufen) statt
   wegrennen? (Empfehlung: zu dir laufen, naechste Version.)
7. **F-G5:** Der alte Test-Baer (`NCBear_SpawnLive`) kaempft nicht mehr; gekaempft wird mit deinem gezaehmten Baeren -- ok?
8. **DE:** Bekommt der Baer Deutsch als achte Sprache? Bis dahin meldet der Trockenlauf genau diesen einen Fehler.

## 7. Fuer den Einbau

Wie `nachbesserung_f2.md` 7: Spiel zu (`tasklist`), Zip vor/nach nach `Zomboid/backups/NCBearTest/`, aus `staging_dateien.txt` alle "neu" und
"ueberschreibt" kopieren **ausser** `NCBearCub.glb`/`.png`; `nc_bear_tier.txt` nur, solange die Test-Mod-Datei 2a7c5ab1 hat; nichts loeschen;
byte-gleich nachzaehlen (65 Dateien geschrieben); `mod.info`/`42/mod.info` aus `mod_info_vorschlag.txt`. Direkt davor Trockenlauf (1 Fehler DE)
und Gesamt-Attrappe (3333/0). Kevin: Spiel **neu starten** (mit -debug), `bugwatch.py` mitlaufen lassen. Testanleitung: `anleitung_f2_entwurf.md`.

## 8. Dateien

- Bericht: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/gegen_bericht_f2.md`
- Testanleitung: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/anleitung_f2_entwurf.md`
- Eigene Pruefungen: `C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/attrappe/gegen_f2/` (`stich.lua` + `stich_ergebnis.txt`, `zaehle.py`
  + `zaehle_ergebnis.txt`, `refs.py` + `refs_ergebnis.txt`, `alte_attrappen.txt`, `trockenlauf*.txt`, `probe_original.txt`, `probe_de_kopie.txt`,
  `gesamt_gegen_probe.txt`)
