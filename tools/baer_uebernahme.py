# -*- coding: utf-8 -*-
"""baer_uebernahme.py -- den Baeren (heute B1a: Junges finden und zaehmen; B1b: Folgen/Bleiben, Namensschild, Umbenennen, Futter
hinhalten, Waisen raeumen; B1c: Register-Selbstheilung, Laerm- und Zombie-Wache, Mitfahren, Call to me, Gehen, Bildschirm-Markierung,
Karten-Symbol, Anzeige-Optionen; B1d: Wachsen in BearGrowDays Spieltagen, taeglich steigende Werte, Faehigkeiten als Daten, Leben am
Tier, Werte-Zeilen ueber dem Baeren; B1e: ab Halbstark zweiter Koerper "ncbeargrown" mit dem grossen Modell bis 1,35, groessere
Markierung als eigenes UI-Element; F1: Baeren-Fenster auf V, Befehle Sitz/Frei/Komm her/Passiv/Unstuck, Namensschild je Baer, Baer ohne
Koerper kommt von selbst wieder; F2 = B5a: Umbenennen der alten NCBear*-Dateien, Zombies und feindliche Banditen greifen den gezaehmten
Baeren an, er kaempft ab Halbstark, Faehigkeiten wirken, Fliehen, Tod oder am Boden, Verband) aus der Test-Mod NCBearTest nach NPC Crew
uebernehmen.

F2 (PLAN_F2.md 7.3, Lauf baer-f2 = B5a, Zusammenbau 12.11.2026): die Altlasten sind abgeloest -- ALT_EXPECTED und ALT_DEFS sind leer.
  * Stummel: eine alte NCBear*.lua (nicht NCBearBench*), die nur noch aus Kommentar-/Leerzeilen besteht ("umbenannt nach ..."), wird nie
    kopiert und ist kein Fehler (Zeile "Stummel" im Bericht). Steht darin Code, ist sie eine unbekannte Altlast (Fehler).
  * Grosses Modell und Toene werden kopiert (BIG_ASSET): models_X/Skinned/NCBear.glb, textures/Body/NCBear.png, scripts/nc_bear_tier.txt
    (seit F2 OHNE den Hirsch-Rueckfall NCBearStag_Body -- der steht in der Werkbank scripts/NCBearBenchStag.txt), scripts/nc_bear_sounds.txt,
    sound/NCBear_{Roar,Growl1,Growl2,Growl3,Huff,Pain}.wav. Jeder Ton-Name der Rasse (BanditsNPCBearDefs.lua name = "NCBear_*") hat seinen
    sound-Block in einem kopierten Skript, jede Ton-Datei liegt in der Uebernahme.
  * Werkbank-Dateien, nie kopiert (WERKBANK_ASSET, je mit Grund): NCBearDeer.glb, WorldItems/NCBear.fbx, Item_NCBear.png,
    WorldItems/NCBear.png, scripts/nc_bear.txt (der Generator-Baer NCBearGen.glb/.png/Foto.png ist seit dem Lauf baer-aussehen ein Aussehen
    und wird kopiert, siehe unten).
    Werkbank-Texte (BENCH_TEXT_KEYS): IGUI_AnimalType_ncbear / _bear / _bearstag, IGUI_Animal_Group_bear -- werden aus den Texten genommen.
  * Animations-Knoten: + die sechs Kampf-Knoten NCBear_(Bite|Maul|Rear|Slam|SwipeL|SwipeR).xml (Clip im GLB des grossen Baeren; Fressen und
    Sitzen in BEIDEN GLBs); jeder Angriff aus B.ATTACKS (shared/BanditsNPCBearFightRules.lua) braucht einen kopierten Knoten; ein unbekannter
    neuer Knoten der Test-Mod ist ein Fehler. Neu ZOMBIE_ANIM: 42/media/AnimSets/zombie/bumped/BanditsNPCBear*.xml (eigener Zombie-Biss-
    Knoten, PLAN_F2.md 0.3): genau eine Bedingung BumpType (STRING) = m_Name, Clip in Vanillas anims_X/Zombie, Ende BumpAnimFinished=true,
    m_Name von der Lua genannt (B.ZBITE / B.ZBITE_LOW) und in NPC Crew, Vanilla und Bandits frei.
  * Tier-Regeln: setHealth/getHealth zusaetzlich in B.BodyDie (Tod am Koerper) und B.FoeHurt (Leben am ZOMBIE, shared/BanditsNPCBearFoe.lua);
    neue Regel setIsInvincible nur in B.BodyShield / B.BodyHp / B.BodyDie (server/BanditsNPCBearGrow.lua); probeweg + FightForce (der
    naechste Angriff von Hand -- nur die Werkbank). Cheat-Ausnahmen: Regel engine fuer genau die zwei setIsInvincible-Zeilen (Kevin
    baer/STAND.md "Fragen fuer Kevin" B1d Nr. 9 + begleiter/ENTSCHEIDUNGEN.md "Kein Schaden am eigenen Baeren" -- "Spieler/Autos schaden dem
    Baeren nicht (mit B5a) -> ja", PLAN_F2.md 0.4 / 11.6), Regel befehl fuer die Ton-Namen der Rasse.
  * Kevins Jar-Ausnahmen (je Methode, sonst gilt die eiserne Regel): animal:pathToLocation(x, y, z) (08.11.) und
    setVariable("animalRunning", ...) am Tier (11.11.) -- je nur in B.MoveTo, Tier-Regeln unten --, dazu pcall(getTextOrNull, key, "%1"
    .. "%9") in B.T (shared/BanditsNPCBear.lua, Kevin 12.11. ~04:25 "Ja, wie NPC Crew", begleiter/ENTSCHEIDUNGEN.md). Nachbesserung F2:
    nur Kommentare/Texte hier (Fundstellen, Naht-Spanne 33-39).
    PZ_ALLOWED + die zwei neuen Aktionsklassen (Verband, Aufhelfen). --vor-b5a aendert seit F2 nichts mehr (keine Altlast).

Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1, Kevin 12.11.2026 "ja fuer spieler als knopf"; Sandbox "ja du hast komplett
uebertrieben da muss so einiges rausfliegen"):
  * Drei neue ENDGUELTIGE Arten ncbeargrowngen / ncbeargrowngenfoto / ncbearcubgen2 (shared/BanditsNPCBearDefs.lua). Neue Kopier-Klasse
    LOOK_ASSET: models_X/Skinned/NCBearGen.glb, NCBearCubGen.glb, textures/Body/NCBearGen.png, NCBearGenFoto.png, NCBearCubGen.png,
    scripts/nc_bear_look.txt (model-Skripte NCBearGen_Body / NCBearCubGen_Body). Die drei Generator-Eintraege sind aus WERKBANK_ASSET raus
    (F-G13 durch Kevins "Aussehen" erledigt). NCBear.* / NCBearGen.* teilen ihre Namen mit dem Maul-Lauf (NAEHTE.md "Aussehen-Modelle").
  * Form: NCBearGen.glb wie NCBear.glb, NCBearCubGen.glb wie NCBearCub.glb -- 1 Netz / 1 Haut, gleiche Knochen-Namen wie die Standard-GLB
    DESSELBEN Koerpers; Fressen/Sitzen-Clips in allen vier GLBs, Kampf-Clips in beiden grossen.
  * Cheat-Ausnahmen +2 (bodyModel "NCBearGen_Body" / "NCBearCubGen_Body", Regel befehl), IG_UI.json + drei Tiernamen.
  * Neue Tier-Regel BodySwap: B.BodySwap( nur aus B.GrowLive (Wachsen) und B.HandleLook (Aussehen-Knopf, server/BanditsNPCBearLook.lua).
  * Neue Pruefung "Optionsname": jedes Literal "Bear..." als erstes Argument von Opt( / opt( / optNum( in kopiertem Lua ist ein Schluessel
    von B.OPTS -- faengt eine vergessene Lesestelle der Sandbox-Kuerzung (39 -> 12 Optionen; die anderen sind feste Werte in B.CFG).
  * Nachbesserung (PRUEF_A.md A3/A4, 12.11. abends): JEDES String-Literal im Code-Teil, das einer der 29 entfernten Optionsnamen ist (auch
    "BanditsNPC.<Name>" / "..._<Name>"), ist ein Fehler (faengt auch local f = B.Opt; f("<alt>")); neue Tier-Regel SandboxVars: das Wort
    SandboxVars nur in B.Opt (shared/BanditsNPCBear.lua). Neue Pruefung "Aussehen-Arten": jede art = "..." in B.LOOKS steht als Literal in
    der kopierten shared/BanditsNPCBearDefs.lua, ist in keiner NCBearBench*Defs-Datei definiert und hat ihren Tiernamen
    IGUI_AnimalType_<art> in den kopierten IG_UI-Texten. Tier-Regel callAt: + B.CallStamp / B.CallUnstamp (Nachbesserung B1: die Uhr
    startet beim Aussehen-Knopf vor dem neuen Koerper und wird bei einem Fehlversuch zurueckgenommen).

F3 (Lauf baer-f3, PLAN_F3.md 17.1; Kevins Antworten 13.11.2026, _arbeit/baer_zaehmen/f3/KEVIN_ANTWORTEN.md): Beduerfnisse (Hunger, Durst,
Muedigkeit), Vertrauen, Traenken, Schlafen (ohne neue Clips: Ersatzbild Sitzen), z Z z, Kopf-Balken, Fenster Variante B, Herz.
  * Neue Dateien deckt LUA_BEAR von selbst: shared/BanditsNPCBearNeedRules.lua, server/BanditsNPCBearNeeds.lua, server/BanditsNPCBearSleep.lua,
    shared/TimedActions/BanditsNPCBearDrinkAction.lua, client/ISUI/BanditsNPCBearZz.lua; die Werkbank client/NCBearBenchNeeds.lua wird nie
    kopiert (BENCH_ANY). Das Herz (42/media/ui/BanditsNPCBearHeart*.png, eigene Zeichnung) deckt UI_ASSET.
  * Sandbox: EIN neuer Regler BearNeedsPercent (13 Optionen); plan_sandbox prueft ihn wie die anderen gegen B.OPTS und Sandbox.json, die
    Pruefung "Optionsname" deckt die Lesestellen.
  * Tier-Regel probeweg + NeedsSet (die vier Werte von Hand setzen -- nur die Werkbank), TIER_DEF + NeedsSet / BodyHurt.
  * Neue Tier-Regel BodyHurt: B.BodyHurt( nur aus B.BearHurt (Treffer) und B.NeedsSlow (Hunger / Durst 100) -- haelt Kevins "Schaden nur von
    Zombies, Banditen, Hunger, Durst" fest (begleiter/ENTSCHEIDUNGEN.md).
  * Neue Tier-Regeln removeFluid / sendSyncEntity: Wasser nehmen (jedes Vorkommen des Namens im Code-Teil) nur in B.DrinkComplete
    (server/BanditsNPCBearNeeds.lua) -- eine zweite Stelle (z. B. in der Zeitaktion) naehme Wasser doppelt (rote Linie "kein Gegenstand
    verloren").
  * Neue Tier-Regel getHour: nirgends (Kevin 13.11. Antwort 6c: KEINE Uhrzeiten -- kein Nachtfenster, kein Mittagsschlaf; geschlafen wird
    nur nach der Muedigkeit und neben dem schlafenden Besitzer).
  * Schlaf-Clips (F3b): die acht Werte liedown / sleep / wakeup / wakealarm / curlin / sleepcurl / curlout / wakecurl (SLEEP_KEYS) darf der
    Pose-Treiber nennen, OHNE dass es ihre Knoten gibt -- solange B.CFG.sleepClips = false in der kopierten shared/BanditsNPCBear.lua steht
    (dann setzt sie niemand). Steht dort true, braucht JEDER der acht Werte einen kopierten Knoten (sonst Fehler): Knoten, Clips in allen
    GLBs und der Schalter kommen zusammen mit F3b. Die Knoten selbst nimmt F3b in ANIMSET_OK / ANIMSET_BOTH auf.
  * Staging als volle Kopie der Test-Mod (mod_f3): eine mod.info im Staging, die BYTE-GLEICH mit der der Test-Mod ist, ist kein Fehler
    (wird wie die der Test-Mod nie kopiert); eine geaenderte bleibt ein Fehler (Vorschlag als eigene Datei).
  * Keine Naht in eine NPC-Crew-Datei, keine Laufzeit-Naht zu NPC Crew (kein Nachtfenster mehr); neu beruehrt wird nur Vanilla
    (Fluessigkeits-Behaelter wie ISGiveWaterToAnimal). NAEHTE.md: Kopf, Zeile 41 (gebaut), neu 44 (Traenken), 45 (Schlaf), "Sandbox-Seiten".
  * Nachbesserung F3 (13.11.2026 abends, _arbeit/baer_zaehmen/f3/NACHBESSERUNG.md, Befunde C1 und C5): PZ_ALLOWED + die neue
    Aktionsklasse BanditsNPCBearDrinkAction (ohne sie war die Probe rot: luacheck_pz W113 in client/BanditsNPCBearMenu.lua -- der
    Trockenlauf merkt das nicht, der Pruefer laeuft erst nach dem Schreiben; deshalb nach JEDER neuen Aktionsklasse --probe laufen lassen).
    Neue Tier-Regel getForwardDirection: Kevins VIERTE Jar-Ausnahme (13.11., Antwort 5 "Hellblau, ueber dem Kopf": Blickrichtung des
    Tiers fuer das z Z z) nur in aim (client/ISUI/BanditsNPCBearZz.lua); am Zombie (Lua-Beleg Bandits) nur in knock
    (shared/BanditsNPCBearFoe.lua). Eine zweite Stelle am Tier waere ein Fehler.

F4 (Lauf baer-f4, PLAN_F4.md 17.1; Kevins Antworten 13.11.2026 abends, _arbeit/baer_zaehmen/f4/KEVIN_ANTWORTEN.md): eigenes Inventar des
Baeren (Register-Inventar + Spieler-Kopie im Einzelspieler), Traglast, Packtaschen, frisst selbst aus dem Inventar.
  * Neue Lua-Dateien deckt LUA_BEAR von selbst: shared/BanditsNPCBearInvRules.lua, server/BanditsNPCBearInv.lua (KERN),
    shared/TimedActions/BanditsNPCBearPutAction.lua, ...TakeAction.lua, client/BanditsNPCBearInvClient.lua, client/ISUI/BanditsNPCBearInvWindow.lua
    (OBERFLAECHE); die Werkbank client/NCBearBenchInv.lua wird nie kopiert (BENCH_ANY).
  * Neue Klasse PACKS_ASSET: 42/media/scripts/nc_bear_packs.txt (Gegenstand NPCCrew.BearPacks in module NPCCrew + Schneider-Rezept SewBearPacks in
    module Base). packs_check: das Rezept-Ergebnis steht als item in DERSELBEN Datei (NPC-Crew-Lehre: ein Rezept mit unbekannter Ausgabe frisst die
    Zutaten), jede Zutat Base.X gibt es in Vanillas scripts/generated/items, der Gegenstand ist KEIN Behaelter (kein Inhalt im Inhalt).
  * TEXT_NS: ItemName.json (nur NPCCrew.BearPacks) und Recipes.json (nur SewBearPacks) -- NPC Crew hat beide Dateien (noch) nicht: die erste
    Uebernahme legt sie sortiert an, wer danach kommt (Zweihaender, Crew Backpack), fuehrt zusammen (NAEHTE.md "ItemName/Recipes").
  * Sandbox: EIN neuer Regler BearCarryPercent (14 Optionen); plan_sandbox prueft ihn wie die anderen.
  * Neue Tier-Regeln (rote Linie "kein Gegenstand verloren oder verdoppelt"): invWrite (rec.inv / rec.bag zuweisen nur in server/BanditsNPCBearInv.lua),
    invCopy (der Spieler-ModData-Schluessel BanditsNPCBearInv nur dort), AddWorldInventoryItem nur in K.dropAll (Tod / Abwurf-Liste), invAdd (AddItem /
    sendAddItemToContainer nur in K.give, Nehmen), invRemove (sendRemoveItemFromContainer nur in takeOne, server/BanditsNPCBearServer.lua -- Geben,
    Fuettern und Verband gehen alle durch takeOne). probeweg + InvSet / InvSnap (Absturz nachstellen -- nur die Werkbank). getHour: zusaetzlich
    INV.alarmRead (die WECKZEIT eines Weckers reist mit -- nie die Tageszeit).
  * Cheat-Regel "erzeugen": je Stelle einzeln freigegeben (CHEAT_ALLOWED): instanceItem in INV.refOf (Vergleichs-Stueck, kommt in keinen Behaelter),
    B.InvBuild (Neubau aus einem Satz) und dem Anbauteil einer Schusswaffe; inv:AddItem / sendAddItemToContainer in K.give -- jede Stelle baut nur
    aus einem Satz, der vorher als echter Gegenstand vom Spieler genommen wurde (kein Spawn-Weg).
  * Jar-Ausnahmen (Kevin 13.11.: "Ja, dieselben wie NPC Crew"): Liste im Kopf von shared/BanditsNPCBearInvRules.lua und in f4/JAR_LISTE.md;
    geprueft von _arbeit/baer_zaehmen/f4/werkzeug_kern/feldpruefer.py.
  * Keine Naht in eine NPC-Crew-Datei. NAEHTE.md: Kopf F4, Zeile 42 (gebaut), neu "Absturz-Schere", "Spieler-ModData", "ItemName/Recipes",
    "Sandbox-Seiten" + BearCarryPercent.
  * Nachbesserung F4 (13.11.2026 spaet, _arbeit/baer_zaehmen/f4/NACHBESSERUNG.md, Befund C1): PZ_ALLOWED + die zwei neuen Aktionsklassen
    BanditsNPCBearPutAction (Menue + InvClient) und BanditsNPCBearTakeAction (InvClient) -- ohne sie war die Probe rot (8 x W113), dieselbe
    Luecke wie F3 bei DrinkAction: nach JEDER neuen Aktionsklasse --probe laufen lassen.

K1 (Lauf baer-k1, Korrektur nach F4, _arbeit/baer_zaehmen/k1/PLAN_K1.md 12; Kevins Worte baer/begleiter/ENTSCHEIDUNGEN.md ab 13.11. ~21:40): Vertrauen
-100..+100 (Fassung trV im Register UND im Spiegel), Hunger/Durst nach Groesse, Einfrieren, Mitschlafen in jedem Modus, Geben gebuendelt / Nehmen 1000,
selbst trinken, Look-Sperre mit Restzeit; dazu (OBERFLAECHE) Schild folgt der Pose, Zahnrad, Zahlenfeld.
  * Neue Lua-Dateien deckt LUA_BEAR von selbst: shared/BanditsNPCBearTagPose.lua (erzeugte Daten), client/ISUI/BanditsNPCBearCountBox.lua.
    Neue Werkbank-Befehle NCBear_CubTrustDay, NCBear_InvItems (Gegenstaende fuer den Test grosser Stapel) leben nur in NCBearBench*.lua (BENCH_ANY).
  * Neue Tier-Regel k1entfallen: die alten Vertrauens- und Mengen-Regeln (B.TrustGain, B.TrustDayClose, B.MealsDay, B.BowlsDay und ihre
    Stellwerte needHunDay / needThrDay / mealsAt / bowlsAt / trHandDay / trMix / trFeed* / trPet / trDrink / trDay* / trSleepH) stehen in KEINER
    kopierten Code-Zeile mehr -- ein uebersehener Leser rechnete sonst still mit nil bzw. einem alten Rueckfall-Wert.
  * Keine Naht in eine NPC-Crew-Datei. NAEHTE.md: Absatz "K1" (Vertrauens-Skala v2 im Register, Liste hpoff in BanditsNPCBear.ini, Zahnrad-Bild
    aus Vanilla, erzeugte Daten-Datei TagPose).
  * Nachbesserung K1 (14.11.2026, _arbeit/baer_zaehmen/k1/NACHBESSERUNG.md): keine Aenderung an diesem Skript noetig -- Trockenlauf und
    --probe gruen. Lehre aus dem Trockenlauf: eine Vorab-Erklaerung "local f" + spaeter "function f(...)" meldet die Cheat-Pruefung als globale
    Funktion (Regel global) -- lokale Hilfen darum VOR ihrem ersten Aufrufer als "local function" schreiben (server/BanditsNPCBearNeeds.lua counts).
    TagPose (erzeugte Daten) kommt jetzt aus _arbeit/baer_zaehmen/k1/werkzeug_nach/tagpose_schirm.py (Bildschirm-Hoehe, Befund P2).

Lauf baer-kampf (K1-K8, _arbeit/baer_zaehmen/kampf/PLAN_KAMPF.md 4; Kevins Worte baer/begleiter/ENTSCHEIDUNGEN.md "Kevin 13.11. ~23:00, Kampf-Fehler"):
Bruellen beim ersten Kontakt, Liegende zerfleischen, Einholen (Vorhalt, Ausfallschritt), Sprint im Angriff, Zombies greifen den Baeren an, kein
Verstecken des grossen Baeren, Leine 25 mit Sprint zurueck, Kampf-Log.
  * Keine neue Datei, keine neuen Texte, keine Modell-/AnimSet-Datei. Neue Werkbank-Befehle NCBear_FightSpeed / NCBear_Lure leben nur in
    client/NCBearBenchFight.lua (BENCH_ANY).
  * Neue Tier-Regel setXY (wie die F3-Regel getForwardDirection): setX / setY am Baeren nur in moveBear (server/BanditsNPCBearFight.lua: a:setX/setY
    am Tier wie V:server/ClientCommands.lua:895-896, nur SP, Kachelwechsel nur mit B.FoeStepOk), am Zombie nur in B.FoePushTick (F2), sonst nur an
    UI-Elementen (Inventar-Fenster, Baeren-Fenster, Markierung -- je Funktion einzeln erlaubt). Blickrichtung des Baeren weiter nicht ueber
    getForwardDirection (Regel bleibt). NAEHTE.md: Absatz "Kampf-Lauf" (Haken Events.OnZombieUpdate nur waehrend des Lockens, SP).
  * Nachbesserung (_arbeit/baer_zaehmen/kampf/NACHBESSERUNG.md): nur Stellwerte und Logik in denselben vier Kern-Dateien (Fight, FightRules, Foe,
    BanditsNPCBear.lua) -- keine neue Datei, kein neuer Engine-Aufruf, keine neue Regel; Trockenlauf + --probe gruen.

Grundregel (Werkstatt-CLAUDE.md Abschnitt 0, Kevin 08.11.2026): alles wird FUER NPC Crew gebaut und soll am Ende "einfach copy paste"
hinueber; keine Cheat- oder Testmenues kommen mit. Plan: _arbeit/baer_zaehmen/PLAN_ZAEHMEN.md Abschnitt 12 (B1b: PLAN_B1B.md 7),
Naehte: baer/NAEHTE.md.
Vorbild (gelesen, nicht blind kopiert): turret/tools/turret_uebernahme.py.

Aufruf (aus C:/Users/Kevin/NPCCrew-Nebenprojekte):
  python baer/tools/baer_uebernahme.py                     Trockenlauf: liest alles, schreibt NICHTS, sagt, was passieren wuerde.
  python baer/tools/baer_uebernahme.py --probe <ordner>    baut <ordner>/quelle (Kopie der Test-Mod ohne .git, darueber --staging, falls
                                                           angegeben) und <ordner>/NPCCrew (Kopie der noetigen Teile von NPC Crew), spielt
                                                           die Uebernahme dort echt durch, danach die vier Lua-Pruefer.
  python baer/tools/baer_uebernahme.py --echt --ja-kevin-hat-es-gesagt
                                                           schreibt in NPC Crew. NUR auf Kevins Wort, nie waehrend das Spiel laeuft.
  Zusatz: --staging <ordner>  Staging ueber die Test-Mod legen (Trockenlauf: nur gedanklich, Probe: in <probe>/quelle kopiert);
                              Form wie _arbeit/baer_zaehmen/mod (spiegelt die Wurzel der Test-Mod). Mit --echt verboten.
          --vor-b5a           Altlasten (die alten, noch nicht umbenannten NCBear*-Dateien und die Art "bear") nur als Warnung.
                              Nur Trockenlauf/Probe; mit --echt verboten: bis B5a ist die echte Uebernahme deshalb immer rot.
          --erneut            eine Datei aus einer frueheren Uebernahme darf ueberschrieben werden (sonst ist jede vorhandene Kollision).

Was es tut (erst wenn ALLES geprueft ist, wird geschrieben; sonst Abbruch ohne Schreiben):
  1. Einordnen: Lua (42|common)/media/lua/(shared|client|server)/(ISUI/|TimedActions/)?BanditsNPCBear*.lua kopieren; jede Datei mit
     Basisnamen NCBearBench* (jede Endung, jeder Ordner) NICHT (Testhilfe); mod.info, .git, .gitattributes, .gitignore nie;
     Translate/<L>/*.json zusammenfuehren; sandbox-options.txt anhaengen (Naht); Modell/Textur/Skript des Jungen (NCBearCub*,
     nc_bear_cub*) und den Animations-Knoten 42/media/AnimSets/buck/idle/NCBear_Eat.xml kopieren (die Kampf-Knoten des Erwachsenen
     bleiben bis B5a in der Test-Mod). F1 (PLAN_F1.md 0.5, 11.3): dazu die drei Sitz-Knoten NCBear_SitDown/Sit/StandUp.xml (liegen in
     der Test-Mod; genau eine Bedingung NCBearAct, Clips im GLB des Jungen); die Werte, die der Sitz-Treiber
     (client/BanditsNPCBearPose.lua, phase(e, obj, "<wert>", now)) setzt, brauchen je einen kopierten Knoten.
     B1c: Bilder 42/media/ui/BanditsNPCBear*.png kopieren (Kevins Symbol fuer Markierung und Karte;
     PNG-Kopf geprueft, Name gegen NPC Crew, Vanilla und Bandits). Die ALTEN Dateien (NCBear*.lua
     ausser Bench, Modelle/Texturen/Skripte/Toene des Erwachsenen und des Test-Gegenstands, die drei Test-Tiernamen in EN/IG_UI.json)
     sind "noch umzubenennen (B5a)": Fehler, mit --vor-b5a Warnung, werden nie kopiert. Erwartet sind genau die in ALT_EXPECTED
     (NAEHTE.md 'Erlaubte Fundstellen des Trockenlaufs'); eine neue Altlast ist immer ein Fehler. Alles andere: Fehler.
  2. Form: Lua LF, reines ASCII, keine Zeile endet mit Backslash; JSON der Quelle UTF-8 ohne BOM, Round-Trip
     json.dumps(indent=4, ensure_ascii=False)+"\\n"; Animations-Knoten wohlgeformt, genau eine Bedingung NCBearAct (STRING) -- sonst
     spielte der Knoten fuer jedes Tier mit Animset buck, auch Vanillas Hirsche --, jeder Clip im GLB des Jungen; Clip-Namen der
     GLB-Datei gegen Vanillas buck-Animset (fehlende nur Warnung, der gespielte Erwachsene hat dieselben 15).
  3. Texte: neue Schluessel sortiert einfuegen, nie die ganze Datei neu sortieren; NPC Crews Datei muss den Round-Trip bestehen;
     Paritaet ueber acht Sprachen (DE seit NPC Crew v3.14.75); CN nur Zeichen, die Vanilla-CN benutzt; DE nur Zeichen der Sprech-
     blasen-Schrift (U+0020-007E, U+00A1-00FF ohne U+00A4/U+00AD); EN 'singleplayer'/'multiplayer' zusammen; %1/%2 gleich
     in allen Sprachen; Namensraum je Datei (UI_BN_Bear_*, Sandbox_BanditsNPC_Bear*, die drei Tiernamen); IG_UI.json hat NPC Crew
     nicht: wird sortiert neu angelegt (bzw. zusammengefuehrt, falls es sie inzwischen gibt); gleicher Schluessel mit gleichem Wert
     (Sandbox_BanditsNPC = "NPC Crew") ist kein Fehler. B1b: kein '<' oder '>' in einem UI.json-Text (Tooltips sind Rich-Text).
  4. Sandbox (Naht 4): die option BanditsNPC.Bear*-Bloecke an NPC Crews 42/media/sandbox-options.txt anhaengen (Zeilenenden der
     Zieldatei, nur C-Kommentare, VERSION nicht doppelt); Abbruch bei vorhandenem Namen; je Option page, translation, Grenzen gegen
     B.OPTS in shared/BanditsNPCBear.lua und die Texte in Sandbox.json.
  5. Kollisionen gegen NPC Crew und Vanilla: eigene Namen (OWN_NAME_RES) im Code von NPC Crew (Kommentar = Warnung), Dateien im
     eigenen Namensraum, gleiche Dateinamen in models_X/textures/scripts/AnimSets (NPC Crew UND Vanilla: gleicher Pfad verdeckte
     Vanillas Datei), Modell-/Skriptnamen in Vanilla-Skripten, BanditsNPC.Bear als Funktion UND Tabelle (v3.8.38), Texte aus der Lua
     fehlen in EN, englische Ersatztexte (U.EN) wortgleich mit EN/UI.json, mesh/Textur des Jungen liegt auf der Platte.
  6. Cheat-Pruefung (Kevin 08.11.2026, fest): kein Testbefehl (NC<Name>_*), keine Testhilfe/Bank/Cheat, kein 'debug' im Code, kein
     Admin-Recht, keine Taste/Maus, kein Engine-Cheat, kein _G, keine globale Funktion/Zuweisung (ausser BanditsNPC = ..., den drei
     Aktionsklassen = ISBaseTimedAction:derive(...) und AnimalDefinitions = AnimalDefinitions or {}), kein Gegenstand aus dem Nichts,
     kein fester Menuetext, kein Fingerabdruck der Werkbank (Texte, Funktionsnamen der NCBearBench*-Dateien). Tier-Regel (Plan 12.1
     Punkt 7): addAnimal( und :addToWorld( nur in B.CreateCub, B.CreateCub( nur aus B.AppearFor, B.AppearFor( nur aus forestRolls und
     baitAppear in server/BanditsNPCBearServer.lua, :remove() am Tier nur in B.RemoveCub. B1b: kein B.ScanAnimals(..., force) im
     kopierten Code (Waisen ohne Alters-Frist entfernen kann nur die Werkbank). B1c (PLAN_B1C.md 10): B.CreateCub( auch aus B.PlaceCub
     (server/BanditsNPCBearRide.lua: Aussteigen, Call to me); setVariable("animalRunning" und :pathToLocation( (Kevins Wort je Methode)
     nur in B.MoveTo (server/BanditsNPCBearWorld.lua) -- seit der Nachbesserung B1c A4 zaehlt JEDES Vorkommen der beiden Namen im
     Code-Teil (auch als String, ueber einen Namen oder ein Tabellenfeld); animalRunning darf zusaetzlich in der Laerm-Wache gelesen
     werden (calmTickBody); B._callAt (Abklingzeit von Call to me) nur in server/BanditsNPCBearRide.lua -- zuruecksetzen kann nur die
     Werkbank; die Seite unter Optionen -> Mods (PZAPI.ModOptions) nennt nur Textschluessel (kein anderes Literal, keine Verkettung,
     kein getText(...) als Argument: mo_text_hits).
     B1d (PLAN_B1D.md 10): Groesse am Tier (setSizeForced, getData) nur in B.ApplySize (shared/BanditsNPCBearStats.lua), Leben am Tier
     (setHealth, getHealth) nur in B.BodyHp (server/BanditsNPCBearGrow.lua) -- jedes Vorkommen des Namens im Code-Teil; die
     Probe-Wege B.GrowSetG / B.GrowSetHp / B.SkillSet (Vorspulen, Leben und Erfahrung setzen) ruft im kopierten Code NIEMAND (nur die
     Definition; aufrufen darf sie nur die Werkbank, spaeter ein Baeren-Fenster mit eigener begruendeter Ausnahme). Die neuen Dateien
     deckt LUA_BEAR, die fuenf neuen Optionen (zwei als double) plan_sandbox (Text der Zahlen gegen B.OPTS).
     B1e (PLAN_B1E.md 10.3): die Art-Frage animal:getAnimalType() steht nur in B.BodyKind (shared/BanditsNPCBear.lua) -- jedes
     Vorkommen des Namens im Code-Teil; kein Vergleich mit B.CUB (== / ~=) im kopierten Code (beide Koerper gehen ueber B.BodyKind).
     Der Koerper-Tausch geht ueber B.PlaceCub (Tier-Regeln unveraendert). Die Art ncbeargrown nennt bodyModel "NCBear_Body" und die
     Rassen-Textur "NCBear" -- beides Teile des grossen Modells, die bis B5a in der Test-Mod bleiben (ALT_DEFS: ohne --vor-b5a Fehler,
     mit Warnung; F9); "NCBear_Body" ist kein Testbefehl (CHEAT_ALLOWED). Neue Bilder ueber UI_ASSET; IG_UI.json + der Tiername
     IGUI_AnimalType_ncbeargrown.
     F1 (PLAN_F1.md 11.3): genau drei Ausnahmen der Regel "taste" (Baeren-Fenster auf Kevins Wunsch, Taste in Vanillas Belegung):
     client/BanditsNPCBearKey.lua Keyboard.KEY_V (Vorgabe der Zeile "Bear window") und Events.OnKeyPressed.Add(onKey),
     client/ISUI/BanditsNPCBearWindow.lua Keyboard.KEY_ESCAPE (Esc schliesst); jede andere Taste/Maus bleibt ein Fund. Nachbesserung
     F1 A1: die Regel sieht auch Fenster-Tasten (setWantKeyEvents, isKeyConsumed, onKeyPress/onKeyRelease/onKeyRepeat, :isKey(...),
     table.insert(keyBinding, rohe Tastencodes "key == 33"); die heutigen Stellen (Key.lua: Abschnitt, eigene Taste, Vorfahrt NPC/
     Fahrzeug/Tier, B9 Radial schliessen beim Druecken und Halten; Window.lua: setWantKeyEvents, isKeyConsumed, onKeyRelease)
     stehen einzeln mit Grund in CHEAT_ALLOWED (14 Tasten-Ausnahmen). TEXT_NS
     UI.json + genau die zwei Tasten-Schluessel "UI_optionscreen_binding_NPC Crew Bear" / "UI_optionscreen_binding_Bear window"
     (Vanilla liest sie selbst, client/OptionScreens/MainOptions.lua:2165/:2177). Neue Tier-Regel PlaceCub: B.PlaceCub( (neuer Koerper
     fuer einen bestehenden Eintrag) nur aus B.RideStep / B.HandleCall / B.BodySwap / B.ReviveMissing (C1). Das Fenster ist echte
     Spielmechanik (kein Wert-Setzen, keine Probe-Wege); die Bench (NCBearBench*) bleibt Bench.
     F1B (PLAN_F1B.md 8.1; Kevin 12.11.2026: Baeren-Fenster auf E in der Naehe, Fern-Taste in den Mod-Optionen): keine Zeile mehr in
     Vanillas keyBinding (die Ausnahmen KEY_V / Abschnitt / isKey(NAME) / Radial-Schliessen / "Esc oder eigene Taste" sind gestrichen),
     dafuer die Vorgaben U.KEY_DEF (Keyboard.KEY_E / KEY_NONE, client/BanditsNPCBearOptions.lua), OnKeyStartPressed (Haltezeit und
     Cursor beim Druecken) und die Interact-Frage isKey(KeybindId.INTERACT, key) in client/BanditsNPCBearKey.lua, "nur Esc" im Fenster.
     TEXT_NS UI.json: nur noch UI_BN_Bear_* (die zwei Tasten-Schluessel UI_optionscreen_binding_* sind weg). mo_text_hits: der NAME
     einer addKeyBind-Zeile darf genau getText("UI_BN_Bear_*") sein (Vanilla sucht die Zeile ueber ihren Beschriftungstext,
     client/OptionScreens/MainOptions.lua:2985, :2992, :3804 -- ein roher Schluessel liefe ins Leere); der Schluessel darin muss wie
     jeder benutzte Schluessel in EN/UI.json stehen. Jede andere Form bleibt ein Fund.
     Ausnahmen nur einzeln mit Grund (CHEAT_ALLOWED).
  7. (Probe/echt) schreiben, zuruecklesen, dann luacheck.py, scopecheck.py, localcount.py je kopierter Lua-Datei und luacheck_pz.py
     (W113 nur die einzeln erlaubten: die drei Aktionsklassen, die eine andere kopierte Datei setzt).

Statisch geprueft, nicht gespielt. Das Skript startet kein Spiel und keinen Server, schreibt nie in die Test-Mod, nie in Vanilla/Bandits,
committet nichts.
"""
import collections
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
NC_LIVE = os.path.normpath(r"C:/Users/Kevin/Zomboid/mods/NPCCrew")
TOOLS = os.path.join(NC_LIVE, "_docs", "tools")                     # Pruefwerkzeuge von NPC Crew (nur aufrufen)
ZOMBOID = os.path.normpath(os.path.join(NC_LIVE, "..", ".."))        # C:/Users/Kevin/Zomboid
TEST = os.path.join(ZOMBOID, "mods", "NCBearTest")
NAEHTE = os.path.normpath(os.path.join(HERE, "..", "NAEHTE.md"))
VANILLA_MEDIA = r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media"
VANILLA_CN = os.path.join(VANILLA_MEDIA, "lua", "shared", "Translate", "CN")
VANILLA_EN = os.path.join(VANILLA_MEDIA, "lua", "shared", "Translate", "EN")
VANILLA_BUCK = os.path.join(VANILLA_MEDIA, "AnimSets", "buck")
LUAC = r"C:/Users/Kevin/Tools/lua51/luac5.1.exe"
LANGS = ["EN", "PTBR", "RU", "KO", "ES", "CN", "FR", "DE"]   # DE seit NPC Crew v3.14.75 (Reihenfolge wie _docs/tools/langcheck.py CODES)
PROBE_MARK = ".baer_probe"

# ---------------------------------------------------------------------------------------------------------------------------------
# Namen (Plan 12.1 Punkt 4). Alles davon in NPC Crew (ausser erlaubten Fundstellen) ist eine Kollision.
# UI_BN_Bear_ MIT Unterstrich (UI_BN_Beard_None ist NPC Crews), tcBear mit Wortgrenze (nicht tcBeardColor).
# ---------------------------------------------------------------------------------------------------------------------------------
OWN_NAME_RES = [r"BanditsNPC\.Bear\b", r"BanditsNPCBear", r"TrueCompanionsBears", r"TC-BEAR", r"UI_BN_Bear_", r"\btcBear\b",
                r"ncbear", r"NCBear", r"nc_bear"]
LUA_BEAR = re.compile(r"^(42|common)/media/lua/(shared|client|server)/(ISUI/|TimedActions/)?BanditsNPCBear[A-Za-z0-9_]*\.lua$")
BENCH_ANY = re.compile(r"^NCBearBench", re.I)                    # jede Testhilfe, gleich welche Endung und welcher Ordner
TRANSLATE = re.compile(r"^42/media/lua/shared/Translate/([A-Za-z]+)/([^/]+\.json)$")
SANDBOX = "42/media/sandbox-options.txt"
# Neue Teile des Jungen (B1a) und der EINE Animations-Knoten, den das Junge braucht (NCBear_Eat, Plan 12.1 P. 10). Die uebrigen
# Knoten des Erwachsenen (Bite, Maul, Slam, Swipe ...) bleiben bis B5a in der Test-Mod (Nachbesserung A10): nie Kampf-Knoten vor
# dem Kampf nach NPC Crew, und was B5a umbenennt, muesste dort sonst geloescht werden.
CUB_ASSET = re.compile(r"^42/media/(models_X/Skinned/NCBearCub\.glb|textures/Body/NCBearCub\.png|scripts/nc_bear_cub\.txt)$")
# B1c (PLAN_B1C.md 10c): Bilder der Oberflaeche (Kevins Baeren-Symbol fuer Bildschirm-Markierung und Karte), nur im eigenen Namensraum
UI_ASSET = re.compile(r"^42/media/ui/BanditsNPCBear[A-Za-z0-9_]*\.png$")
UI_MAX_PX = 512                                                    # Deckel fuer ein Oberflaechen-Bild (Kevins Symbol: 96 x 96)
BANDITS_MEDIA = [os.path.normpath(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits/" + v
                                  + "/media") for v in ("42.22", "common")]   # nur lesen: gleicher ui-Dateiname verdeckte Bandits' Bild
# F1 (PLAN_F1.md 0.5, 11.3): + die drei Sitz-Knoten (Hinsetzen, Sitzen, Aufstehen; Bedingung NCBearAct = sitdown / sit / standup)
# F2 (PLAN_F2.md 7.3): + die sechs Kampf-Knoten des grossen Baeren (Bedingung NCBearAct = bite / maul / rear / slam / swipeL / swipeR).
# Fressen und Sitzen tragen BEIDE Koerper (Clip in beiden GLBs), die Kampf-Knoten nur der grosse (das Junge kaempft nie).
ANIMSET_OK = re.compile(r"^42/media/AnimSets/buck/idle/NCBear_(Eat|SitDown|Sit|StandUp|Bite|Maul|Rear|Slam|SwipeL|SwipeR)\.xml$")
ANIMSET_BOTH = re.compile(r"^42/media/AnimSets/buck/idle/NCBear_(Eat|SitDown|Sit|StandUp)\.xml$")
ANIMSET_ADULT = re.compile(r"^42/media/AnimSets/buck/idle/NCBear_[A-Za-z0-9]+\.xml$")
ANIMSET_ANY = re.compile(r"^(42|common)/media/AnimSets/")
CUB_GLB = "42/media/models_X/Skinned/NCBearCub.glb"
# F2 (PLAN_F2.md 7.3): das grosse Modell, sein model-Skript (ohne Hirsch-Rueckfall), die Toene der Rasse ncbeargrown -- bis F1 Altlasten
BIG_ASSET = re.compile(r"^42/media/(models_X/Skinned/NCBear\.glb|textures/Body/NCBear\.png|scripts/nc_bear_tier\.txt"
                       r"|scripts/nc_bear_sounds\.txt|sound/NCBear_(Roar|Growl1|Growl2|Growl3|Huff|Pain)\.wav)$")
BIG_GLB = "42/media/models_X/Skinned/NCBear.glb"
# Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1 Nr. 1): Modelle, Texturen und model-Skript der drei neuen Arten. Werden kopiert.
LOOK_ASSET = re.compile(r"^42/media/(models_X/Skinned/(NCBearGen|NCBearCubGen)\.glb|textures/Body/(NCBearGen|NCBearGenFoto|NCBearCubGen)\.png"
                        r"|scripts/nc_bear_look\.txt)$")
GEN_GLB = "42/media/models_X/Skinned/NCBearGen.glb"               # Generator-Baer gross (Koerper big, wie BIG_GLB)
# F4 (PLAN_F4.md 17.1 Nr. 2): Gegenstand NPCCrew.BearPacks + Schneider-Rezept SewBearPacks (packs_check). Wird kopiert.
PACKS_ASSET = re.compile(r"^42/media/scripts/nc_bear_packs\.txt$")
PACKS_ITEM = "NPCCrew.BearPacks"
VANILLA_ITEMS = os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media", "scripts", "generated", "items")
CUBGEN_GLB = "42/media/models_X/Skinned/NCBearCubGen.glb"         # Generator-Junges v2 (Koerper cub, wie CUB_GLB)
# F2 (PLAN_F2.md 0.3, 7.3): eigener Zombie-Biss-Knoten (Vanilla-Clip; Name ewig stabil). Kopiert; Form-Pruefung in form_check.
ZOMBIE_ANIM = re.compile(r"^42/media/AnimSets/zombie/bumped/BanditsNPCBear[A-Za-z0-9]*\.xml$")
VANILLA_ZOMBIE_ANIMS = os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media", "anims_X", "Zombie")
# F2 (PLAN_F2.md 7.3, Frage F-G13): Werkbank-Dateien der Test-Mod, die nie nach NPC Crew gehen (je mit Grund; ohne NCBearBench-Namen)
WERKBANK_ASSET = collections.OrderedDict([
    ("42/media/models_X/Skinned/NCBearDeer.glb", "Test-Modell der ALT-Art bearstag (Hirsch-Bewegung; scripts/NCBearBenchStag.txt)"),
    ("42/media/models_X/WorldItems/NCBear.fbx", "Test-Gegenstand 'Test Bear (model)' (NCBear_Spawn, Werkbank)"),
    ("42/media/textures/Item_NCBear.png", "Icon des Test-Gegenstands"),
    ("42/media/textures/WorldItems/NCBear.png", "Textur des Test-Gegenstands"),
    ("42/media/scripts/nc_bear.txt", "module NCBear mit dem Test-Gegenstand BearStatic ('Test Bear (model)')"),
    # Aussehen (PLAN_AUSSEHEN.md 12.1 Nr. 2): NCBearGen.glb / NCBearGen.png / NCBearGenFoto.png sind jetzt Aussehen (LOOK_ASSET) -- F-G13 erledigt
])
GIT_ROOT_FILES = (".git", ".gitattributes", ".gitignore")
ANIM_VAR = "NCBearAct"                                             # B.ACT
# F3 (PLAN_F3.md 14.3, 17.1): die acht Schlaf-Werte. Ihre Knoten und Clips bringt erst F3b; bis dahin (B.CFG.sleepClips = false) darf der
# Pose-Treiber sie nennen, ohne dass es einen kopierten Knoten gibt (form_check).
SLEEP_KEYS = ("liedown", "sleep", "wakeup", "wakealarm", "curlin", "sleepcurl", "curlout", "wakecurl")
SLEEP_SWITCH = re.compile(r"\bsleepClips\s*=\s*(true|false)\b")

# Namensraum der Texte je Datei.
TEXT_NS = {
    # F1 (PLAN_F1.md 3.1, 11.3) hatte hier die zwei Beschriftungen der Tasten-Zeile; F1B (PLAN_F1B.md 2.3, 8.1): keine Zeile mehr in
    # Vanillas keyBinding -> keine Ausnahme mehr (NAEHTE.md Zeile 27)
    "UI.json": (re.compile(r"^UI_BN_Bear_[A-Za-z0-9_]+$"), set()),
    "Sandbox.json": (re.compile(r"^Sandbox_BanditsNPC_Bear[A-Za-z0-9_]+$"), {"Sandbox_BanditsNPC"}),
    # F4 (PLAN_F4.md 13, 17.1 Nr. 3): Name des Gegenstands (voller Typ, ersetzt laut Jar den DisplayName) und des Rezepts
    "ItemName.json": (re.compile(r"^NPCCrew\.BearPacks$"), set()),
    "Recipes.json": (re.compile(r"^SewBearPacks$"), set()),
    "IG_UI.json": (re.compile(r"^$"), {"IGUI_AnimalType_ncbearcub", "IGUI_Animal_Group_ncbear", "IGUI_Breed_brown",
                                       "IGUI_AnimalType_ncbeargrown",                 # B1e: Tiername des grossen Koerpers
                                       # Aussehen (PLAN_AUSSEHEN.md 12.1 Nr. 5): Tiernamen der drei neuen Arten
                                       "IGUI_AnimalType_ncbeargrowngen", "IGUI_AnimalType_ncbeargrowngenfoto",
                                       "IGUI_AnimalType_ncbearcubgen2"}),
}

# ---------------------------------------------------------------------------------------------------------------------------------
# Altlasten bis B5a (Plan 12.1 Punkt 8; Kevin: Umbenennen zu Beginn von B5a). "Erlaubte Fundstellen des Trockenlaufs" (NAEHTE.md):
# genau diese machten den Trockenlauf ohne --vor-b5a absichtlich rot. Je Eintrag Pfad (bzw. "text:<datei>:<schluessel>") und Grund.
# F2 = B5a (PLAN_F2.md 1, 7.3, Lauf baer-f2): ALLE abgeloest -- die sechs alten Lua-Dateien sind Stummel (nie kopiert), das grosse Modell
# und die Toene werden kopiert (BIG_ASSET), die Test-Dateien sind Werkbank (WERKBANK_ASSET), die drei Tiernamen Werkbank-Texte
# (BENCH_TEXT_KEYS). Eine neue Altlast (NCBear*.lua mit Code, unbekannte NCBear*-Datei) ist weiter immer ein Fehler.
# ---------------------------------------------------------------------------------------------------------------------------------
ALT_EXPECTED = collections.OrderedDict()
OLD_ASSET = re.compile(r"^(NCBear|nc_bear|Item_NCBear)", re.I)
# F2 (PLAN_F2.md 1.4, 7.3): Tiernamen der Werkbank-Arten (Test-Art ncbear, ALT-Arten bear/bearstag) -- nie nach NPC Crew, kein Fehler
BENCH_TEXT_KEYS = {"IG_UI.json": {"IGUI_AnimalType_ncbear", "IGUI_AnimalType_bear", "IGUI_AnimalType_bearstag", "IGUI_Animal_Group_bear"}}
OLD_TEXT_KEYS = {}
# B1e (PLAN_B1E.md 0.13, 10.3, Frage F9) bis F1: die Art "ncbeargrown" nannte Teile des grossen Modells, die als Altlast in der Test-Mod
# blieben. F2 = B5a: nc_bear_tier.txt (ohne Hirsch-Rueckfall), NCBear.glb und NCBear.png werden kopiert -> keine Altlast mehr.
ALT_DEFS = collections.OrderedDict()

# Erlaubte Fundstellen in NPC Crew (NPC Crew nennt den Baeren SELBST im Code). Heute keine: der Baer beruehrt NPC Crew nur zur Laufzeit
# (NAEHTE.md). NPC Crew nennt 'NCBear' heute nur in einem Changelog-KOMMENTAR (shared/BanditsNPC.lua, v3.14.58): Warnung, keine Kollision.
NC_ALLOWED = []

# ---------------------------------------------------------------------------------------------------------------------------------
# Cheat-Pruefung (Kevin 08.11.2026: "achte darauf das keine cheat menues davon rueber kommen am ende"). Geprueft wird der CODE-Teil jeder
# kopierten Lua-Zeile (Strings zaehlen zum Code, Kommentare nicht). (Kennung, Muster, Grund)
# ---------------------------------------------------------------------------------------------------------------------------------
CHEAT_RULES = [
    ("befehl", r"\bNC[A-Z][A-Za-z]*_[A-Za-z]\w*", "Testbefehl der Werkbank (NCBear_*, NCTurret_* ...)"),
    ("testhilfe", r"(?i)\w*(bench|cheat|godmode|testmod[eu]s?|testhilfe|testmenue?)\w*", "Bank-, Test- oder Cheat-Name"),
    ("bank", r"(?i)\bbank\b", "Bank-Modus (gehoert in NCBearBench*)"),
    ("debug", r"\bisDebugEnabled\b|\bgetDebug\s*\(|\bgetDebugOptions\b|\bDebugOptions\b|\baddDebugOption\b|\bDebugContextMenu\b"
              r"|\bISDebugMenu\b|(?i:debug)", "Debug-Schalter, Debug-Menue oder 'debug' im Code"),
    ("admin", r"\bCapability\.\w+|\bisAdmin\b|\bgetAccessLevel\b|\bIsStaff\b|\bhasAdminPower\b|\bhasAdminTool\b"
              r"|:getRole\s*\(\s*\)\s*:\s*getName\s*\(|\bisCoopHost\b|(?i:[\"']admin)", "Admin-/Staff-Recht (ein Admin-Weg ist ein Spawn-Weg)"),
    ("taste", r"\bEvents\.(OnKeyPressed|OnKeyStartPressed|OnKeyKeepPressed|OnCustomUIKey\w*|OnContextKey|OnMouseDown|OnMouseUp"
              r"|OnRightMouseDown|OnRightMouseUp|OnMouseWheel|OnObject(?:Left|Right)MouseButton(?:Down|Up)|OnJoypad\w*|OnGamepad\w*"
              r"|OnPressReloadButton|OnPressRackButton)\b|\bisKeyDown\s*\(|\bisKeyPressed\s*\(|\bGameKeyboard\.|\bKeyboard\.KEY_\w+"
              # Nachbesserung F1 A1: Tasten in UI-Fenstern und Vanillas Tastentabelle
              r"|\bsetWantKeyEvents\s*\(|:isKey\s*\(|[:.]isKeyConsumed\b|[:.]onKey(?:Press|Release|Repeat)\b"
              r"|\btable\.insert\s*\(\s*keyBinding\b|\bkey\s*[=~]=\s*\d",
     "Taste oder Maus abgefragt (Debug-Taste? Erlaubt sind nur die einzeln begruendeten Stellen des Baeren-Fensters, CHEAT_ALLOWED / "
     "NAEHTE.md 27-28)"),
    ("engine", r"\b(setGodMod|setGhostMode|setInvisible|setInvincible|setIsInvincible|setNoClip|setUnlimitedCarry|setUnlimitedEndurance"
               r"|setUnlimitedAmmo|setBuildCheat|setFarmingCheat|setHealthCheat|setMechanicsCheat|setMovablesCheat"
               r"|setTimedActionInstantCheat|setFastMoveCheat|setCanSeeAll|setCanHearAll|setZombiesDontAttack|setKnowAllRecipes"
               r"|setSeeNonPvpZone|setCanUseBrushTool|setDebug\w*|addAcceptance|setWild)\b", "Cheat-Aufruf der Engine (Plan 0.8: nicht benutzt)"),
    ("_G", r"(?<!rawget\()\b_G\b", "Zugriff auf _G (Konsolenbefehl?)"),
    ("erzeugen", r"\binstanceItem\s*\(|\bInventoryItemFactory\.CreateItem\s*\(|:AddItems?\s*\(|\bsendAddItemToContainer\s*\(",
     "Gegenstand erzeugen (aus dem Nichts = Spawn; jede Stelle einzeln mit Grund freigeben)"),
    ("bankspur", r"\[NCBear\]|(?i:[\"'][^\"'\n]*\busage:)", "Fingerabdruck der Werkbank (Praefix [NCBear] oder 'usage:'-Hilfe)"),
    ("altmenue", r"\bNCBearMenu\b|\bNCBearBench\w*", "Haken ins alte Testmenue der Test-Mod (NCBearMenu.extra) oder in die Testhilfe"),
    # B1b (PLAN_B1B.md 4.3): B.ScanAnimals(players, force) -- force ueberspringt die Alters-Frist der Waisen (Riegel 3). Nur die Werkbank
    # (NCBear_CubSweep) darf das. Seit der Nachbesserung B1b A5 keine Zeilen-Regex mehr, sondern scan_force_hits (zerlegt die Klammer).
]
SCAN_NAME = re.compile(r"\bScanAnimals\b")
SCAN_DEF = re.compile(r"\bfunction\s+(?:[\w.]+[.:])?ScanAnimals\s*\(")
SCAN_WHY = "Waisen-Suchlauf mit force (ohne Alters-Frist) gibt es nur in der Werkbank"


def scan_force_hits(code_text):
    """Nachbesserung B1b A5: jede Erwaehnung von ScanAnimals im Code-Teil einer Datei (Zeilen mit "\\n" verbunden, Kommentare schon
    weg, Strings noch da). Erlaubt sind nur die Definition und Aufrufe mit hoechstens EINEM Argument auf oberster Ebene (mit
    ':' zaehlt das versteckte self mit). Fund: ein zweites Argument in jeder Form (true, not false, 1 == 1, B.Players(), ...), ein
    Aufruf ueber mehrere Zeilen eingeschlossen, und ScanAnimals ohne folgende Klammer (Zuweisung an einen Namen, Tabellenfeld,
    Text "ScanAnimals"). Rueckgabe: Liste (Zeichen-Offset, Kurztext)."""
    defs = set()
    for d in SCAN_DEF.finditer(code_text):
        defs.add(d.start() + d.group(0).index("ScanAnimals"))
    hits = []
    for m in SCAN_NAME.finditer(code_text):
        if m.start() in defs:
            continue
        j = m.end()
        while j < len(code_text) and code_text[j] in " \t\r\n":
            j += 1
        if j >= len(code_text) or code_text[j] != "(":
            hits.append((m.start(), "ScanAnimals ohne Aufruf-Klammer (an einen Namen gebunden?)"))
            continue
        k = m.start() - 1
        while k >= 0 and code_text[k] in " \t":
            k -= 1
        args = call_args(code_text, j + 1)
        n = len(args)
        if n == 1 and not args[0].strip():
            n = 0
        if k >= 0 and code_text[k] == ":":
            n += 1
        if n > 1:
            hits.append((m.start(), "Aufruf mit %d Argumenten" % n))
    return hits
CHEAT_GLOBAL_FN = re.compile(r"(?<![\w.:])function\s+([A-Za-z_]\w*)\s*\(")
CHEAT_GLOBAL_SET = re.compile(r"^([A-Za-z_]\w*)\s*=(?!=)")
CHEAT_STRING = re.compile(r"(?i)(?<!de)spawn|debug")
CHEAT_NAME = re.compile(r"(?i:bench|cheat|debug|spawn)|Dbg|Test|TEST|(?<![A-Za-z])test")
CHEAT_FILE_REST = re.compile(r"(?i:dev|tools|admin|console|tweak|tune)(?![a-z])")
CHEAT_TEXT = re.compile(r"(?i)\b(bench|cheat|debug|spawn|test)")
XML_CHEAT = re.compile(r"(?i)bench|cheat|debug|test|NCBear_Cub")
LUA_STRING = re.compile(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'')
LONG_STRING = re.compile(r"\[(=*)\[(.*?)\]\1\]", re.S)
BTN_CALL = re.compile(r"\bISButton\s*:\s*new\s*\(|[:.]addSlice\s*\(")
MENU_CALL = re.compile(r"[:.](addOption|addOptionOnTop|addGetUpOption|addColorBoxOption|addActionsOption|insertOptionAfter"
                       r"|insertOptionBefore)\s*\(")
_TS = r'"(?:[^"\\\n]|\\.)*"|' + r"'(?:[^'\\\n]|\\.)*'"
_TL0 = r"(?:%s|[^()\"'])*" % _TS
_TL1 = r"(?:%s|[^()\"']|\(%s\))*" % (_TS, _TL0)
_TL2 = r"(?:%s|[^()\"']|\(%s\))*" % (_TS, _TL1)
TEXT_CALL = re.compile(r"\b(?:getText|getTextOrNull)\s*\(%s\)|\b[\w.:]+\s*\(\s*([\"'])UI_[^\"']*\1%s\)" % (_TL2, _TL2))
FN_HEAD = re.compile(r"^(?:local\s+)?function\s+([\w.:]+)\s*\(|^(?:local\s+)?([\w.:]+)\s*=\s*function\b")
# Erlaubte Globale (Plan 12.1 Punkt 6): Aktionsklassen sind in Vanilla und NPC Crew global (die Engine baut Netz-Aktionen ueber den Namen).
GLOBAL_OK = {"BanditsNPC"}
GLOBAL_SAME = {"AnimalDefinitions"}                                # nur die Form "X = X or {}" (Vanillas Tabelle, DeerDefinitions.lua:1)
# Tier-Regel (Plan 12.1 Punkt 7): Muster -> erlaubte (Datei, Funktion). Die Definition selbst zaehlt nicht.
TIER_RULES = [
    ("addAnimal", re.compile(r"(?<![\w.:])addAnimal\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.CreateCub")},
     "Tier erzeugen nur in B.CreateCub"),
    ("addToWorld", re.compile(r":addToWorld\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.CreateCub")},
     "Tier in die Welt setzen nur in B.CreateCub"),
    ("CreateCub", re.compile(r"\bB\.CreateCub\s*\("), {("42/media/lua/server/BanditsNPCBearServer.lua", "B.AppearFor"),
                                                         ("42/media/lua/server/BanditsNPCBearRide.lua", "B.PlaceCub")},
     "B.CreateCub nur aus B.AppearFor und (B1c) B.PlaceCub (Aussteigen, Call to me)"),
    ("AppearFor", re.compile(r"\bB\.AppearFor\s*\("), {("42/media/lua/server/BanditsNPCBearServer.lua", "forestRolls"),
                                                         ("42/media/lua/server/BanditsNPCBearServer.lua", "baitAppear")},
     "B.AppearFor (der EINE Weg, ein Junges in die Welt zu setzen) nur aus Wald-Wurf und Koeder"),
    ("remove", re.compile(r":remove\s*\(\s*\)"), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.RemoveCub")},
     "Tier entfernen nur in B.RemoveCub"),
    ("removeAnimal", re.compile(r"(?<![\w.:])removeAnimal\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.RemoveCub")},
     "Tier bei den Clients entfernen (Server) nur in B.RemoveCub"),
    # B1c (PLAN_B1C.md 10b): die zwei Engine-Aufrufe mit Kevins Wort (pathToLocation 08.11.2026, setVariable("animalRunning", false)
    # 11.11.2026) an genau EINER Stelle. Nachbesserung B1c A4: nicht mehr nur die Aufruf-Form, sondern JEDES Vorkommen des Namens im
    # Code-Teil (Strings zaehlen mit, Gross/Klein egal) -- so fallen auch local V = "animalRunning"; a.setVariable(a, V, false),
    # a["setVariable"](...), a.pathToLocation(a, ...), a["pathToLocation"](...) und local f = a.pathToLocation auf. Zweite erlaubte
    # Stelle fuer den Namen animalRunning: das LESEN in der Laerm-Wache (getVariableBoolean, calmTickBody, nur Einzelspieler).
    ("animalRunning", re.compile(r"(?i)\banimalRunning\b"),
     {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.MoveTo"), ("42/media/lua/server/BanditsNPCBearGuard.lua", "calmTickBody")},
     "Name animalRunning (Gehen setzen nur in B.MoveTo, lesen nur in der Laerm-Wache)"),
    ("pathToLocation", re.compile(r"(?i)\bpathToLocation\b"), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.MoveTo")},
     "pathToLocation (jede Form) nur in B.MoveTo"),
    # B1c: die Abklingzeit von "Call to me" lebt nur in Ride.lua (Dateiebene, B.CallLeft, callMark); sie zuruecksetzen kann nur die
    # Werkbank (NCBear_CubCallReset). Nachbesserung Aussehen B1: + B.CallStamp (gibt den Stempel davor zurueck) und B.CallUnstamp (nimmt
    # einen Stempel zurueck, nur nach einem Aussehen-Tausch ohne neuen Koerper) -- beide in Ride.lua
    ("callAt", re.compile(r"\bB\._callAt\b"), {("42/media/lua/server/BanditsNPCBearRide.lua", None),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "B.CallLeft"),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "callMark"),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "B.CallStamp"),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "B.CallUnstamp")},
     "Abklingzeit von Call to me (B._callAt) nur in server/BanditsNPCBearRide.lua"),
    # B1d (PLAN_B1D.md 10, 7.1 Nr. 18): Groesse und Leben am Tier je an EINER Stelle -- jedes Vorkommen des Namens im Code-Teil (auch als
    # String oder Tabellenfeld), wie die B1c-Regeln animalRunning/pathToLocation. Belege der Aufrufe stehen dort im Kommentar
    # (setSizeForced: Vanilla ButcheringUtil.lua:569/:571/:586; getHealth: ISAnimalUI.lua:15; setHealth: ISAnimalContextMenu.lua:545).
    ("setSizeForced", re.compile(r"(?i)\bsetSizeForced\b"), {("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")},
     "Groesse am Tier setzen (setSizeForced) nur in B.ApplySize"),
    ("getData", re.compile(r"\bgetData\b"), {("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")},
     "Datenteil des Tiers (getData) nur in B.ApplySize"),
    # F2 (PLAN_F2.md 0.11, 5.1 Nr. 26): + B.BodyDie (Tod am Koerper: setHealth(0), V:server/ClientCommands.lua:932) und B.FoeHurt (die
    # EINE Stelle fuer Leben am ZOMBIE beim Zombie-Rechner, shared/BanditsNPCBearFoe.lua; B:client/BanditUpdate.lua:2386, :2391-2397)
    ("setHealth", re.compile(r"(?i)\bsetHealth\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp"),
                                                    ("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyDie"),
                                                    ("42/media/lua/shared/BanditsNPCBearFoe.lua", "B.FoeHurt")},
     "Leben setzen (setHealth) nur in B.BodyHp / B.BodyDie (Tier) und B.FoeHurt (Zombie)"),
    ("getHealth", re.compile(r"(?i)\bgetHealth\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp"),
                                                    ("42/media/lua/shared/BanditsNPCBearFoe.lua", "B.FoeHurt")},
     "Leben lesen (getHealth) nur in B.BodyHp (Tier) und B.FoeHurt (Zombie)"),
    # B1d: Vorspulen / Leben / Erfahrung von Hand setzen -- im kopierten Code gibt es keinen erlaubten Aufrufer (leere Menge); die
    # Definitionen zaehlen nicht (TIER_DEF). Ein Aufrufer waere ein Spieler-Weg ohne Spielmechanik (Cheat-Pfad).
    # F2 (PLAN_F2.md 4.3, 7.3): + B.FightForce (der naechste Angriff von Hand, NCBear_FightNext) -- ebenfalls nur die Werkbank
    # F3 (PLAN_F3.md 13, 17.1): + B.NeedsSet (Hunger / Durst / Muedigkeit / Vertrauen von Hand setzen) -- ebenfalls nur die Werkbank
    # F4 (PLAN_F4.md 14, 17.1 Nr. 4): + B.InvSet / B.InvSnap (Register-Inventar zuruecksetzen = Absturz nachstellen) -- nur die Werkbank
    ("probeweg", re.compile(r"\bGrowSetG\b|\bGrowSetHp\b|\bSkillSet\b|\bFightForce\b|\bNeedsSet\b|\bInvSet\b|\bInvSnap\b"), set(),
     "B.GrowSetG / B.GrowSetHp / B.SkillSet / B.FightForce / B.NeedsSet / B.InvSet / B.InvSnap nur aus der Werkbank (im kopierten Code nur "
     "die Definition)"),
    # F3 (PLAN_F3.md 3.1, 17.1; Kevin ENT "Schaden nur von Zombies, Banditen, Hunger, Durst"): das Register-Leben senkt nur B.BodyHurt, und
    # das rufen nur der Treffer (B.BearHurt) und der Langsam-Takt der Beduerfnisse (B.NeedsSlow: Hunger / Durst 100, bis 1 %, nie Tod)
    # K1 (PLAN_K1.md 2.1, 8, 9): die alten Vertrauens- und Mengen-Regeln sind ENTFALLEN -- wer sie noch ruft oder ihre Stellwerte liest, rechnet
    # mit nil bzw. einem Rueckfall auf die alten Zahlen (still falsch). Im kopierten Code nirgends erlaubt (es gibt auch keine Definition mehr).
    ("k1entfallen", re.compile(r"\bTrustGain\b|\bTrustDayClose\b|\bMealsDay\b|\bBowlsDay\b|\bneedHunDay\b|\bneedThrDay\b|\bmealsAt\b"
                               r"|\bbowlsAt\b|\btrHandDay\b|\btrMix\b|\btrFeed(?:Fav|Ok|Snack)\b|\btrPet\b|\btrDrink\b"
                               r"|\btrDay(?:Good|Bad|Worst|Sleep|MinH)\b|\btrSleepH\b"), set(),
     "alte Vertrauens-/Mengen-Regel (K1 entfallen: B.TrustGain / B.TrustDayClose / B.MealsDay / B.BowlsDay und ihre Stellwerte)"),
    ("BodyHurt", re.compile(r"\bB\.BodyHurt\s*\("), {("42/media/lua/server/BanditsNPCBearHurt.lua", "B.BearHurt"),
                                                       ("42/media/lua/server/BanditsNPCBearNeeds.lua", "B.NeedsSlow")},
     "Register-Leben sinkt (B.BodyHurt) nur durch Treffer (B.BearHurt) und Hunger / Durst (B.NeedsSlow)"),
    # F3 (PLAN_F3.md 5.2; rote Linie "kein Gegenstand verloren oder verdoppelt"): Wasser nehmen an EINER Stelle -- jedes Vorkommen der
    # zwei Namen im Code-Teil (auch als String), nur in B.DrinkComplete (Vanilla shared/TimedActions/Animals/ISGiveWaterToAnimal.lua:34/:86-87)
    ("removeFluid", re.compile(r"(?i)\bremoveFluid\b"), {("42/media/lua/server/BanditsNPCBearNeeds.lua", "B.DrinkComplete")},
     "Wasser nehmen (removeFluid) nur in B.DrinkComplete"),
    ("sendSyncEntity", re.compile(r"(?i)\bsendSyncEntity\b"), {("42/media/lua/server/BanditsNPCBearNeeds.lua", "B.DrinkComplete")},
     "Behaelter abgleichen (sendSyncEntity) nur in B.DrinkComplete"),
    # F3-Nachbesserung C5 (Kevins Wort 13.11.2026, Antwort 5: "Hellblau, ueber dem Kopf" -- der Code darf das Spiel fragen, wohin der Baer
    # schaut): animal:getForwardDirection() am TIER ist nur im Jar belegt (zombie.characters.IsoGameCharacter.getForwardDirection(),
    # javap -c 42.22 Offset 0 aload_0 / 1 getfield forwardDirection / 4 areturn; IsoAnimal ueberschreibt sie nicht) -- genau EINE Stelle:
    # aim in client/ISUI/BanditsNPCBearZz.lua (z Z z). Die zweite erlaubte Stelle ist alt (F2) und am ZOMBIE mit Lua-Beleg
    # (B:shared/ZombieActions/ZAPush.lua:36-37): knock in shared/BanditsNPCBearFoe.lua. Jedes Vorkommen des Namens im Code-Teil zaehlt.
    ("getForwardDirection", re.compile(r"(?i)\bgetForwardDirection\b"),
     {("42/media/lua/client/ISUI/BanditsNPCBearZz.lua", "aim"), ("42/media/lua/shared/BanditsNPCBearFoe.lua", "knock")},
     "Blickrichtung (getForwardDirection) nur in aim (z Z z, Kevins Jar-Ausnahme 13.11.) und knock (am Zombie)"),
    # Lauf baer-kampf (_arbeit/baer_zaehmen/kampf/PLAN_KAMPF.md 4; Kevin 13.11. ~23:00 Punkte 3/4): die Lage eines KOERPERS setzt nur, wer es
    # darf -- am Baeren moveBear (Ausfallschritt / Sprint-Schub, server/BanditsNPCBearFight.lua; a:setX/setY am Tier wie V:server/
    # ClientCommands.lua:895-896, nur SP, Kachelwechsel nur mit B.FoeStepOk), am Zombie B.FoePushTick (F2, Zurueckfliegen; B:shared/
    # ZombieActions/ZAMove.lua:11/:17). Die uebrigen Treffer sind UI-Elemente (ISUIElement:setX/setY, V:client/ISUI/ISUIElement.lua:195-245):
    # Inventar-Fenster und Bildschirm-Markierung. Jedes Vorkommen von setX / setY im Code-Teil zaehlt; eine neue Stelle ist ein Fehler.
    ("setXY", re.compile(r"\bset[XY]\b"),
     {("42/media/lua/server/BanditsNPCBearFight.lua", "moveBear"), ("42/media/lua/shared/BanditsNPCBearFoe.lua", "B.FoePushTick"),
      ("42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "put"), ("42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "clampPos"),
      ("42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "Inv:RestoreLayout"),
      ("42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "U.InvOpen"),
      ("42/media/lua/client/ISUI/BanditsNPCBearMarker.lua", "U.MarkerLayout"),
      ("42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "put"), ("42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "clampPos"),
      ("42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "Win:RestoreLayout"),
      ("42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "U.WinOpen")},
     "Lage setzen (setX / setY) am Baeren nur in moveBear (Kampf-Lauf), am Zombie nur in B.FoePushTick, sonst nur an UI-Elementen"),
    # F3 (Kevin 13.11.2026, Antwort 6c: KEINE Uhrzeiten -- kein Nachtfenster, kein Mittagsschlaf): die Tagesstunde fragt niemand
    # F4: einzige Ausnahme ist die WECKZEIT eines Weckers, der im Baeren-Inventar reist (INV.alarmRead, shared/BanditsNPCBearInvRules.lua)
    ("getHour", re.compile(r"\bgetHour\b"), {("42/media/lua/shared/BanditsNPCBearInvRules.lua", "INV.alarmRead")},
     "Uhrzeit (getHour) nirgends -- geschlafen wird nur nach der Muedigkeit und neben dem schlafenden Besitzer (Kevin 13.11.); nur die "
     "Weckzeit eines Weckers im Baeren-Inventar (INV.alarmRead)"),
    # F2 (PLAN_F2.md 0.4, 5.1 Nr. 26; Kevin baer/STAND.md "Fragen fuer Kevin" B1d Nr. 9 + begleiter/ENTSCHEIDUNGEN.md "Kein Schaden am eigenen Baeren", 11.6): der gezaehmte Koerper ist fuer die
    # Engine unverwundbar -- den Schutz
    # setzen/loesen nur diese drei Stellen (jedes Vorkommen des Namens im Code-Teil). Die Cheat-Regel "engine" meldet den Namen ausserdem;
    # die zwei Zeilen stehen einzeln in CHEAT_ALLOWED.
    ("setIsInvincible", re.compile(r"(?i)\bsetIsInvincible\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyShield"),
                                                                 ("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp"),
                                                                 ("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyDie")},
     "Schutz am Tier (setIsInvincible) nur in B.BodyShield / B.BodyHp / B.BodyDie"),
    # B1e (PLAN_B1E.md 0.8, 10.3): EINE Art-Frage fuer beide Koerper -- getAnimalType (jede Form, auch als String) nur in B.BodyKind,
    # und kein Vergleich mit B.CUB (eine Stelle, die nur das Junge kennt, verloere den grossen Koerper ab Halbstark)
    ("getAnimalType", re.compile(r"(?i)\bgetAnimalType\b"), {("42/media/lua/shared/BanditsNPCBear.lua", "B.BodyKind")},
     "Art-Frage (getAnimalType) nur in B.BodyKind"),
    ("artvergleich", re.compile(r"(?:==|~=)\s*B\.CUB\b|\bB\.CUB\s*(?:==|~=)"), set(),
     "Vergleich mit B.CUB (nur das Junge) -- beide Koerper ueber B.BodyKind"),
    # F1 (PLAN_F1.md 4b, 8.1 Nr. 16): B.PlaceCub erzeugt einen neuen Koerper fuer einen BESTEHENDEN Eintrag (gen + 1). Erlaubt nur aus
    # Aussteigen (B.RideStep), Call to me / Unstuck (B.HandleCall), Koerper-Tausch (B.BodySwap) und C1 (B.ReviveMissing) -- ein weiterer
    # Aufrufer (z. B. aus einem Fenster-Knopf) waere ein Spawn-Weg.
    ("PlaceCub", re.compile(r"\bB\.PlaceCub\s*\("), {("42/media/lua/server/BanditsNPCBearRide.lua", "B.RideStep"),
                                                       ("42/media/lua/server/BanditsNPCBearRide.lua", "B.HandleCall"),
                                                       ("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodySwap"),
                                                       ("42/media/lua/server/BanditsNPCBearOrder.lua", "B.ReviveMissing")},
     "neuer Koerper fuer einen bestehenden Eintrag (B.PlaceCub) nur aus Aussteigen, Call to me, Koerper-Tausch und C1"),
    # Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1 Nr. 6): der Koerper-Tausch (neuer Koerper, dann der alte weg) nur aus dem Wachsen
    # (B.GrowLive) und dem Aussehen-Knopf (B.HandleLook, prueft Besitz, Uhr, Kampf, Zombies selbst) -- ein weiterer Aufrufer waere ein
    # Herhol- oder Heil-Weg ohne diese Pruefungen
    ("BodySwap", re.compile(r"\bB\.BodySwap\s*\("), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.GrowLive"),
                                                       ("42/media/lua/server/BanditsNPCBearLook.lua", "B.HandleLook")},
     "Koerper-Tausch (B.BodySwap) nur aus dem Wachsen und dem Aussehen-Knopf"),
    # Nachbesserung Aussehen A3 (PRUEF_A.md; PLAN_AUSSEHEN.md 9.4 "SandboxVars liest nur B.Opt"): jedes Vorkommen des Wortes SandboxVars im
    # Code-Teil nur in B.Opt -- jede Option geht ueber B.OPTS (Vorgabe, Bereich), eine entfernte Option wird nie gelesen
    ("SandboxVars", re.compile(r"\bSandboxVars\b"), {("42/media/lua/shared/BanditsNPCBear.lua", "B.Opt")},
     "Sandbox lesen (SandboxVars) nur in B.Opt"),
    # Nachbesserung Aussehen B1: B.CallUnstamp nimmt die gemeinsame Uhr (Unstuck/Aussehen) zurueck -- nur im Koerper-Tausch selbst, wenn
    # KEIN neuer Koerper entstand (B.BodySwap, server/BanditsNPCBearGrow.lua). Ein weiterer Aufrufer waere ein Weg an der Abklingzeit
    # vorbei (im Einzelspieler teilen Client und Schreiber dieselben Lua-Tabellen). Die Definition zaehlt nicht (TIER_DEF).
    ("CallUnstamp", re.compile(r"\bCallUnstamp\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodySwap")},
     "Abklingzeit zuruecknehmen (B.CallUnstamp) nur in B.BodySwap nach einem Fehlversuch ohne neuen Koerper"),
    # F4 (PLAN_F4.md 10, 17.1 Nr. 4; rote Linie "kein Gegenstand verloren oder verdoppelt"): das Inventar des Baeren (rec.inv / rec.bag) wird nur in
    # server/BanditsNPCBearInv.lua zugewiesen -- an EINER Stelle je Vorgang (Geben, Nehmen, Tod, Abgleich, Laden, Werkbank)
    ("invWrite", re.compile(r"\brec\.(?:inv|bag)\s*=(?!=)"), {
        ("42/media/lua/server/BanditsNPCBearInv.lua", "K.inv"), ("42/media/lua/server/BanditsNPCBearInv.lua", "B.InvHealRec"), ("42/media/lua/server/BanditsNPCBearInv.lua", "K.fixInv"), ("42/media/lua/server/BanditsNPCBearInv.lua", "B.InvPutComplete"),
        ("42/media/lua/server/BanditsNPCBearInv.lua", "B.InvTakeComplete"), ("42/media/lua/server/BanditsNPCBearInv.lua", "B.InvDrop"), ("42/media/lua/server/BanditsNPCBearInv.lua", "B.InvSet")},
     "Baeren-Inventar (rec.inv / rec.bag) zuweisen nur in server/BanditsNPCBearInv.lua"),
    ("invCopy", re.compile(r"\bBanditsNPCBearInv\b"), {("42/media/lua/server/BanditsNPCBearInv.lua", None)},
     "Spieler-Kopie (ModData-Schluessel BanditsNPCBearInv) nur in server/BanditsNPCBearInv.lua (B.INV_COPY)"),
    ("AddWorldInventoryItem", re.compile(r"(?i)\bAddWorldInventoryItem\b"), {("42/media/lua/server/BanditsNPCBearInv.lua", "K.dropAll")},
     "Gegenstaende auf den Boden (AddWorldInventoryItem) nur in K.dropAll (Tod / Abwurf-Liste)"),
    ("invAdd", re.compile(r":AddItems?\s*\(|(?i:\bsendAddItemToContainer\b)"), {("42/media/lua/server/BanditsNPCBearInv.lua", "K.give")},
     "Gegenstand ins Spieler-Inventar (AddItem / sendAddItemToContainer) nur in K.give (Nehmen)"),
    ("invRemove", re.compile(r"(?i)\bsendRemoveItemFromContainer\b"), {("42/media/lua/server/BanditsNPCBearServer.lua", "takeOne")},
     "Gegenstand vom Spieler nehmen (sendRemoveItemFromContainer) nur in takeOne (Fuettern, Verband, Geben)"),
]
# B1c (PLAN_B1C.md 6.8): die Seite unter Optionen -> Mods bekommt nur Textschluessel (Vanilla ruft getText,
# client/OptionScreens/MainOptions.lua:2801-2812). Methode -> Stellen der Text-Argumente (0 = erstes Argument).
MO_CALL = re.compile(r"\bModOptions\s*:\s*create\s*\(|[:.](addTitle|addDescription|addTickBox|addSlider|addComboBox|addItem|addTextEntry"
                     r"|addButton|addKeyBind|addMultipleTickBox|addColorPicker)\s*\(")
MO_TEXT_ARGS = {None: (1,), "addTitle": (0,), "addDescription": (0,), "addTickBox": (1, 3), "addSlider": (1, 6), "addComboBox": (1, 2),
                "addItem": (0,), "addTextEntry": (1, 3), "addButton": (1, 2), "addKeyBind": (1, 3), "addMultipleTickBox": (1, 2),
                "addColorPicker": (1, 6)}
# (Vanilla client/PZAPI/ModOptions.lua :28-247; option:addTickBox(name, value) einer Mehrfach-Auswahl :96 hat den Text vorn -- mit
# hoechstens zwei Argumenten zaehlt deshalb das erste)
MO_KEY = re.compile(r"^UI_BN_Bear_[A-Za-z0-9_]+$")
MO_NAME = re.compile(r"^[A-Za-z_]\w*$")
# F1B (PLAN_F1B.md 0 E2, 8.1): Name einer Tasten-Zeile schon uebersetzt -- genau diese Form, nur fuer addKeyBind Argument 1
MO_KEYBIND_NAME = re.compile(r"^getText\(\s*\"UI_BN_Bear_[A-Za-z0-9_]+\"\s*\)$")


def mo_text_hits(code_text):
    """Nachbesserung B1c A4: Text-Argumente der Optionen-Seite (PZAPI.ModOptions) im Code-Teil einer Datei (Zeilen mit "\\n"
    verbunden, Kommentare weg). Erlaubt: genau EIN String-Literal, das ein Schluessel UI_BN_Bear_* ist, oder ein blosser Name, hinter
    dem kein lokaler Satz steht (local x = "..."). Alles andere ist ein Fund: ein anderes Literal, ein Literal in einer Verkettung
    ("Text" .. x), ein Aufruf als Argument (getText(...), U.T(...) -- schon uebersetzt statt Schluessel), jeder andere Ausdruck.
    Rueckgabe: Liste (Zeilennummer, Kurztext, Grund)."""
    local_str = set(m.group(1) for m in re.finditer(r"\blocal\s+(\w+)\s*=\s*[\"'][^\"'\n]*[A-Za-z][^\"'\n]*[A-Za-z]", code_text))
    hits = []
    for m in MO_CALL.finditer(code_text):
        args = call_args(code_text, m.end())
        idx = MO_TEXT_ARGS.get(m.group(1), ())
        if m.group(1) == "addTickBox" and len(args) <= 2:
            idx = (0,)
        no = code_text.count("\n", 0, m.start()) + 1
        for i in idx:
            if i >= len(args):
                continue
            a = args[i].strip()
            if a in ("", "nil"):
                continue
            if m.group(1) == "addKeyBind" and i == 1 and MO_KEYBIND_NAME.match(a):
                continue        # F1B: Name der Tasten-Zeile = getText("UI_BN_Bear_*") (Schluessel prueft die Text-Pruefung)
            lit = re.match(r"^([\"'])([^\"'\n]*)\1$", a)
            if lit:
                if not MO_KEY.match(lit.group(2)):
                    hits.append((no, a[:40], "Optionen-Seite mit festem Text statt Textschluessel"))
            elif MO_NAME.match(a):
                if a in local_str:
                    hits.append((no, a[:40], "Optionen-Seite mit festem Text (lokaler Satz) statt Textschluessel"))
            else:
                hits.append((no, a[:40], "Optionen-Seite mit einem Ausdruck (Verkettung, Aufruf ...) statt eines Textschluessels"))
    return hits


TIER_DEF = re.compile(r"^function\s+B\.(CreateCub|AppearFor|RemoveCub|GrowSetG|GrowSetHp|SkillSet|PlaceCub|FightForce|BodySwap"
                      r"|CallUnstamp|NeedsSet|BodyHurt|InvSet|InvSnap)\s*\(")   # F4: + InvSet, InvSnap; B1d:
# + die drei Probe-Wege; F1: + PlaceCub; F2: + FightForce; Aussehen: + BodySwap; Nachbesserung Aussehen B1: + CallUnstamp;
# F3: + NeedsSet, BodyHurt
# Ausnahmen einzeln mit Grund: Datei, Regel, ein Text im Code-Teil der Zeile. Greift eine nicht mehr, warnt das Skript.
CHEAT_ALLOWED = [
    # F4 (PLAN_F4.md 5, 6.3, 10): Neubau aus einem Satz, der vorher als ECHTER Gegenstand vom Spieler genommen wurde (B.InvPutComplete) bzw. den
    # F5 aus einem Fang baut (B.InvAddItem) -- kein Spawn-Weg; Zaehl-Invariante Spieler + Baer + Boden in attrappe/f4_kern (Kevins rote Linie)
    {"file": "42/media/lua/shared/BanditsNPCBearInvRules.lua", "rule": "erzeugen", "code": "r = instanceItem(t)", "exact": True,
     "why": "F4: Vergleichs-Stueck je Typ (INV.refOf) fuer die Anbauteile einer Waffe -- kommt in keinen Behaelter"},
    {"file": "42/media/lua/shared/BanditsNPCBearInvRules.lua", "rule": "erzeugen", "code": "local item = instanceItem(s.t)", "exact": True,
     "why": "F4: B.InvBuild -- Neubau eines Satzes (Nehmen, Tod), der Satz stammt von einem genommenen Gegenstand"},
    {"file": "42/media/lua/shared/BanditsNPCBearInvRules.lua", "rule": "erzeugen", "code": "part = instanceItem(e.t)", "exact": True,
     "why": "F4: Anbauteil einer Schusswaffe aus deren Satz (das Teil hing am genommenen Original)"},
    {"file": "42/media/lua/server/BanditsNPCBearInv.lua", "rule": "erzeugen", "code": "inv:AddItem(item)", "exact": True,
     "why": "F4: K.give -- der gebaute Satz in das Inventar des Besitzers (Ankunft per contains, erst danach ausgetragen)"},
    {"file": "42/media/lua/server/BanditsNPCBearInv.lua", "rule": "erzeugen", "code": "sendAddItemToContainer(inv, item)", "exact": True,
     "why": "F4: K.give -- der Server meldet den angekommenen Gegenstand dem Client (Vanilla FishingNet.lua:152-153)"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'bodyModel = "NCBearCub_Body"',
     "why": "Name des model-Skripts (scripts/nc_bear_cub.txt), kein Befehl (Plan 12.1 Punkt 5)"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'bodyModel = "NCBear_Body"',
     "why": "B1e: model-Skript des grossen Koerpers (scripts/nc_bear_tier.txt, seit F2 kopiert, ohne Hirsch-Rueckfall), kein Befehl"},
    # Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1 Nr. 4): model-Skripte der neuen Arten (scripts/nc_bear_look.txt), kein Befehl
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'bodyModel = "NCBearGen_Body"',
     "why": "Aussehen: model-Skript des Generator-Baeren (ncbeargrowngen / ncbeargrowngenfoto, scripts/nc_bear_look.txt), kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'bodyModel = "NCBearCubGen_Body"',
     "why": "Aussehen: model-Skript des Generator-Jungen (ncbearcubgen2, scripts/nc_bear_look.txt), kein Befehl"},
    # F2 (PLAN_F2.md 1.1, 7.3): Stimmen der Rasse von ncbeargrown -- Namen der Ton-Skripte (scripts/nc_bear_sounds.txt, sound-Bloecke), kein
    # Befehl; gespielt ueber animal:playBreedSound(Schluessel) (V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19, :41)
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_Pain"',
     "why": "F2: Ton-Skript NCBear_Pain (scripts/nc_bear_sounds.txt) fuer pain und death der Rasse, kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_Huff"',
     "why": "F2: Ton-Skript NCBear_Huff (scripts/nc_bear_sounds.txt), kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_HuffSoft"',
     "why": "F2: Ton-Skript NCBear_HuffSoft (scripts/nc_bear_sounds.txt), kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_Growl1"',
     "why": "F2: Ton-Skript NCBear_Growl1 (scripts/nc_bear_sounds.txt), kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_Growl2"',
     "why": "F2: Ton-Skript NCBear_Growl2 (scripts/nc_bear_sounds.txt), kein Befehl"},
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'name = "NCBear_Growl3"',
     "why": "F2: Ton-Skript NCBear_Growl3 (scripts/nc_bear_sounds.txt), kein Befehl"},
    # F2 (PLAN_F2.md 0.4, 11.6; Kevin baer/STAND.md "Fragen fuer Kevin" B1d Nr. 9 + begleiter/ENTSCHEIDUNGEN.md "Kein Schaden am eigenen Baeren": "Spieler/Autos schaden dem Baeren
    # nicht (mit B5a) -> ja"; Kevin 12.11. ~05:20 "der darf kein schaden
    # bekommen von mir oder meinen turrets ... und von meinen npc's nicht"): Schutz am gezaehmten Koerper. Genau diese zwei Zeilen (exakt),
    # dazu die Tier-Regel setIsInvincible (nur B.BodyShield / B.BodyHp / B.BodyDie). Belege: V:client/ISUI/Animal/ISAnimalContextMenu.lua:563,
    # V:server/ClientCommands.lua:911.
    {"file": "42/media/lua/server/BanditsNPCBearGrow.lua", "rule": "engine", "code": "a:setIsInvincible(true)", "exact": True,
     "why": "F2: Schutz an (B.BodyShield je Koerper; B.BodyHp nach dem eigenen Senken) -- nur unser Weg senkt das Leben (Kevin: ENTSCHEIDUNGEN 'Kein Schaden am eigenen Baeren', 11.6)"},
    {"file": "42/media/lua/server/BanditsNPCBearGrow.lua", "rule": "engine", "code": "a:setIsInvincible(false)", "exact": True,
     "why": "F2: Schutz kurz aus, damit B.BodyHp das Leben senken kann bzw. B.BodyDie (Tod wie Vanilla, PLAN_F2.md 0.11) toeten kann"},
    # F1 (PLAN_F1.md 11.3) / Nachbesserung F1 A1: Baeren-Fenster mit Taste. F1B (PLAN_F1B.md 8.1; Kevin 12.11.2026: "bei E das baeren ui
    # zu oeffnen und wenn man es aus der ferne oeffnen will dann kann man ... den hotkey festelegen ... in sen mod settings"): zwei
    # Tasten auf der eigenen Mod-Optionen-Seite (Nah-Taste E, Fern-Taste ohne Vorgabe), keine Zeile mehr in Vanillas keyBinding, kein
    # Radial-Schliessen beim Druecken/Halten mehr (Tier-Radial ohne "Kill" jetzt als Huelle in client/BanditsNPCBearMenu.lua; nur wenn
    # eine UNSERER Tasten selbst auf V liegt, geht das Radial am eigenen Baeren beim Loslassen mit zu -- Nachbesserung F1B B1), das
    # Fenster verbraucht nur Esc. Genau diese Stellen, je mit Grund.
    {"file": "42/media/lua/client/BanditsNPCBearOptions.lua", "rule": "taste",
     "code": "U.KEY_DEF = { KeyNear = Keyboard.KEY_E, KeyFar = Keyboard.KEY_NONE }", "exact": True,
     "why": "F1B, Kevin 12.11.: E am Baeren, Fern-Taste in den Mod-Optionen -- Vorgaben der zwei addKeyBind-Zeilen (V:shared/keyBinding.lua:33, :57)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste", "code": "Events.OnKeyStartPressed.Add(onKeyStart)",
     "why": "F1B, Kevin 12.11.: E am Baeren -- Haltezeit und Cursor beim Druecken merken (V:client/Farming/CFarming_Interact.lua:289)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste", "code": "Events.OnKeyPressed.Add(onKey)",
     "why": "F1B, Kevin 12.11.: E am Baeren / Fern-Taste oeffnen und schliessen das Fenster (V:client/ISUI/FPS.lua:20)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste", "code": "getCore():isKey(KeybindId.INTERACT, key)",
     "why": "F1B, Kevin 12.11.: E am Baeren -- Tuer/Fahrzeug/Zielen/Kletter-Riegel und die stille Fern-Taste ohne Baeren "
            "(Nachbesserung F1B B2/B3) nur, wenn die Taste gerade Vanillas Interact ist (V:client/Farming/CFarming_Interact.lua:28)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste", "code": "getCore():isKey(ia.KEYBIND, key) and ia.FindTarget(p)",
     "why": "F1B: Vorfahrt NPC-Gespraech auf derselben Taste -- NPC Crews Taste nur gelesen (NAEHTE.md 28)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste",
     "code": "getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU, key) and ISVehicleMenu.getVehicleToInteractWith(p)",
     "why": "F1B: Vorfahrt Fahrzeug-Radial, falls eine unserer Tasten darauf liegt (V:client/ISUI/ISUIHandler.lua:36, :43)"},
    {"file": "42/media/lua/client/BanditsNPCBearKey.lua", "rule": "taste", "code": "if getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key) then",
     "why": "F1B: Vorfahrt Tier-Radial eines fremden Tiers, falls eine unserer Tasten darauf liegt (V:client/ISUI/ISUIHandler.lua:37, :44); "
            "Nachbesserung F1B B1 (zweite Stelle, closeBearRadial): liegt sie darauf, geht Vanillas Radial am eigenen Baeren mit dem "
            "Fenster zu (V:client/ISUI/ISUIHandler.lua:91-92, V:client/ISUI/Animal/ISAnimalContextMenu.lua:1164)"},
    # F4 (OBERFLAECHE, schnittstelle.md O1): das Inventar-Fenster schliesst wie das Baerenfenster nur mit Esc (V:client/ISUI/Crafting/
    # ISHandcraftWindow.lua:289-297, :386); nicht, solange der Chat tippt
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "rule": "taste", "code": "o:setWantKeyEvents(true)",
     "why": "F4: das Inventar-Fenster bekommt Tasten (nur Esc schliesst; V:client/ISUI/Crafting/ISHandcraftWindow.lua:386)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "rule": "taste", "code": "function Inv:isKeyConsumed(key)",
     "why": "F4: nur Esc gehoert dem offenen Inventar-Fenster (V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-292)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "rule": "taste", "code": "return key == Keyboard.KEY_ESCAPE", "exact": True,
     "why": "F4: nur Esc (V:client/ISUI/Crafting/ISHandcraftWindow.lua:290)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "rule": "taste", "code": "function Inv:onKeyRelease(key)",
     "why": "F4: Esc schliesst das Inventar-Fenster (V:client/ISUI/Crafting/ISHandcraftWindow.lua:294-297)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearInvWindow.lua", "rule": "taste", "code": "if self:isVisible() and key == Keyboard.KEY_ESCAPE then U.InvClose() end", "exact": True,
     "why": "F4: Esc schliesst das Inventar-Fenster (V:client/ISUI/Crafting/ISHandcraftWindow.lua:294-297)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "rule": "taste", "code": "o:setWantKeyEvents(true)",
     "why": "F1: das Fenster bekommt Tasten (F1B: nur Esc schliesst; V:client/ISUI/Crafting/ISHandcraftWindow.lua:386)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "rule": "taste", "code": "function Win:isKeyConsumed(key)",
     "why": "F1B: nur Esc gehoert dem offenen Fenster (V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-292)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "rule": "taste", "code": "function Win:onKeyRelease(key)",
     "why": "F1B: Esc schliesst das Fenster (V:client/ISUI/Crafting/ISHandcraftWindow.lua:294-297)"},
    {"file": "42/media/lua/client/ISUI/BanditsNPCBearWindow.lua", "rule": "taste", "code": "return key == Keyboard.KEY_ESCAPE",
     "exact": True,
     "why": "F1B: nur Esc schliesst (V:client/ISUI/Crafting/ISHandcraftWindow.lua:290); E / Fern-Taste schliessen ueber OnKeyPressed"},
]
# luacheck_pz W113, die eine ANDERE kopierte Datei setzt (luacheck_pz liest je Datei, nicht ueber Dateien): (Datei, Name).
PZ_ALLOWED = {
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearFeedAction"),
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearPetAction"),
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearBaitAction"),
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearMendAction"),         # F2: Verband (shared/TimedActions/BanditsNPCBearMendAction.lua)
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearHelpAction"),         # F2: Aufhelfen (shared/TimedActions/BanditsNPCBearHelpAction.lua)
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearDrinkAction"),        # F3: Traenken (shared/TimedActions/BanditsNPCBearDrinkAction.lua)
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearPutAction"),          # F4: Packtaschen anlegen (shared/TimedActions/BanditsNPCBearPutAction.lua)
    ("BanditsNPCBearInvClient.lua", "BanditsNPCBearPutAction"),     # F4: Geben (Nachbesserung F4, Befund C1)
    ("BanditsNPCBearInvClient.lua", "BanditsNPCBearTakeAction"),    # F4: Nehmen (shared/TimedActions/BanditsNPCBearTakeAction.lua)
}

ARGS = {"erneut": False, "vor_b5a": False, "echt": False}


class Report:
    def __init__(self):
        self.errors, self.warns, self.lines = [], [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def say(self, msg=""):
        self.lines.append(msg)
        print(msg)


def rd(path):
    with open(path, "rb") as f:
        return f.read()


def rel_of(root, full):
    return os.path.relpath(full, root).replace(os.sep, "/")


def md5(data):
    return hashlib.md5(data).hexdigest()


_LONG_OPEN = re.compile(r"\[(=*)\[")


def lua_split_lines(text):
    """Je Zeile (Code, Kommentar). Kennt "..." und '...' mit Escapes, [[...]] und --[[...]] auch ueber Zeilen. Nur zum Pruefen.
    Was es nicht erkennt, zaehlt als Code (die strengere Seite). Form wie turret_uebernahme.py."""
    out = []
    state = None
    for raw in text.split("\n"):
        line = raw[:-1] if raw.endswith("\r") else raw
        code, com = [], []
        i, n = 0, len(line)
        while i < n:
            if state is not None:
                close = "]" + "=" * state[0] + "]"
                j = line.find(close, i)
                end = n if j < 0 else j + len(close)
                (com if state[1] else code).append(line[i:end])
                if j >= 0:
                    if state[1] and "".join(code).strip():
                        code.append(" ")
                    state = None
                i = end
                continue
            c = line[i]
            if c == "-" and line.startswith("--", i):
                m = _LONG_OPEN.match(line, i + 2)
                if m:
                    state = (len(m.group(1)), True)
                    com.append(line[i:m.end()])
                    i = m.end()
                    continue
                com.append(line[i:])
                break
            if c == "[":
                m = _LONG_OPEN.match(line, i)
                if m:
                    state = (len(m.group(1)), False)
                    code.append(line[i:m.end()])
                    i = m.end()
                    continue
            if c == '"' or c == "'":
                j = i + 1
                while j < n and line[j] != c:
                    j += 2 if line[j] == "\\" else 1
                code.append(line[i:j + 1])
                i = j + 1
                continue
            code.append(c)
            i += 1
        out.append(("".join(code), "".join(com)))
    return out


def eol_of(data, label, rep):
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    if crlf and lf:
        rep.err("%s: gemischte Zeilenenden (%d CRLF, %d LF) -- nicht anfassen, von Hand klaeren" % (label, crlf, lf))
    return b"\r\n" if crlf > lf else b"\n"


# ---------------------------------------------------------------------------------------------------------------------------------
# 0. Quelle: Test-Mod (ohne .git), wahlweise mit Staging darueber
# ---------------------------------------------------------------------------------------------------------------------------------
def source_map(base, staging, rep):
    """{rel: absoluter Pfad} und Liste der uebersprungenen Git-Teile. Staging gewinnt (gleicher Pfad)."""
    files, skipped = {}, []
    for root, tag in ((base, "test"), (staging, "staging")):
        if not root:
            continue
        if not os.path.isdir(root):
            rep.err("Quelle fehlt: %s" % root)
            continue
        for dirpath, dirs, fs in os.walk(root):
            if os.path.normcase(dirpath) == os.path.normcase(root) and ".git" in dirs:
                dirs.remove(".git")
                skipped.append((".git/", "Git-Sicherung der Test-Mod (Ordner), wird nicht kopiert"))
            for fn in fs:
                full = os.path.join(dirpath, fn)
                rel = rel_of(root, full)
                if tag == "staging" and rel in ("mod.info", "42/mod.info"):
                    # F3: ein Staging als volle Kopie der Test-Mod (mod_f3) traegt deren mod.info byte-gleich mit -- kein Fehler
                    # (kopiert wird mod.info ohnehin nie); eine GEAENDERTE mod.info bleibt ein Fehler
                    twin = os.path.join(base, rel.replace("/", os.sep)) if base else None
                    if twin and os.path.isfile(twin) and rd(twin) == rd(full):
                        continue
                    rep.err("Staging enthaelt %s (anders als die der Test-Mod) -- mod.info gehoert nicht ins Staging (Vorschlag als "
                            "eigene Datei)" % rel)
                    continue
                files[rel] = full
    return files, skipped


# ---------------------------------------------------------------------------------------------------------------------------------
# 1. Einordnen
# ---------------------------------------------------------------------------------------------------------------------------------
def is_stub(data):
    """F2 (PLAN_F2.md 1.2): Stummel = Lua nur aus Kommentar- und Leerzeilen (kein Code-Teil, lua_split_lines) und mit dem Satz
    "Umbenannt nach". Jede Zeile Code -> kein Stummel (dann ist die Datei eine unbekannte Altlast)."""
    text = data.decode("latin-1")
    if "Umbenannt nach" not in text:
        return False
    return all(not code.strip() for code, _com in lua_split_lines(text))


def collect_source(src, rep):
    copy_lua, copy_asset, merge, skipped, alt, sandbox = [], [], [], [], [], None
    for rel in sorted(src):
        base = os.path.basename(rel)
        if rel in ("mod.info", "42/mod.info"):
            skipped.append((rel, "mod.info der Test-Mod"))
        elif rel in GIT_ROOT_FILES:
            skipped.append((rel, "Git-Sicherung der Test-Mod, wird nicht kopiert"))
        elif BENCH_ANY.match(base):
            skipped.append((rel, "Testhilfe NCBearBench*, wird nie kopiert"))
        elif TRANSLATE.match(rel):
            merge.append(rel)
        elif LUA_BEAR.match(rel):
            copy_lua.append(rel)
        elif rel == SANDBOX:
            sandbox = rel
        elif (CUB_ASSET.match(rel) or ANIMSET_OK.match(rel) or UI_ASSET.match(rel) or BIG_ASSET.match(rel)
              or ZOMBIE_ANIM.match(rel) or LOOK_ASSET.match(rel) or PACKS_ASSET.match(rel)):   # F2: + grosses Modell/Toene
                                                                  # (BIG_ASSET), Zombie-Biss-Knoten (ZOMBIE_ANIM); Aussehen: + LOOK_ASSET;
                                                                  # F4: + PACKS_ASSET (Packtaschen + Rezept)
            copy_asset.append(rel)
        elif rel in WERKBANK_ASSET:                         # F2: Werkbank-Dateien ohne NCBearBench-Namen (je mit Grund)
            skipped.append((rel, "Werkbank, wird nie kopiert: " + WERKBANK_ASSET[rel]))
        elif ANIMSET_ADULT.match(rel):
            # F2: alle bekannten Knoten werden kopiert (ANIMSET_OK); ein NEUER Knoten (z. B. aus einem Modell-Lauf) muss erst eingeordnet werden
            rep.err("%s: unbekannter Animations-Knoten des Baeren -- in ANIMSET_OK aufnehmen (Clip im GLB, Bedingung NCBearAct, NAEHTE.md "
                    "Naht 9) oder in die Werkbank (NCBearBench*)" % rel)
        elif rel.endswith(".lua") and re.match(r"BanditsNPCBear", base):
            rep.err("%s: Unterordner nicht freigegeben (bekannt: shared|client|server, darin ISUI/ oder TimedActions/)" % rel)
        elif rel.endswith(".lua") and base.startswith("NCBear") and is_stub(rd(src[rel])):
            # F2 (PLAN_F2.md 0.13, 1.2): umbenannte alte Datei, nur noch Kommentar ("umbenannt nach ..."), damit die Test-Mod beim Einbau
            # nichts loeschen muss -- wird nie kopiert, kein Fehler
            skipped.append((rel, "Stummel (umbenannt, nur Kommentar), wird nie kopiert"))
        elif rel in ALT_EXPECTED or (rel.endswith(".lua") and base.startswith("NCBear")) or (
                rel.startswith(("42/media/", "common/media/")) and OLD_ASSET.match(base)):
            alt.append(rel)
        elif ANIMSET_ANY.match(rel):
            rep.err("%s: Animations-Datei nur als 42/media/AnimSets/buck/idle/NCBear_*.xml oder (F2) "
                    "42/media/AnimSets/zombie/bumped/BanditsNPCBear*.xml" % rel)
        elif rel.endswith(".lua"):
            rep.err("%s: Lua-Datei ohne den Namen BanditsNPCBear* (Kopierregel a) -- umbenennen; Testhilfe nach NCBearBench*" % rel)
        else:
            rep.err("%s: Datei ohne Baeren-Namen -- wuerde eine NPC-Crew-Datei treffen koennen" % rel)
    return copy_lua, copy_asset, merge, skipped, alt, sandbox


def alt_report(alt, text_alt, rep):
    """Altlasten bis B5a melden. Ohne --vor-b5a Fehler (erwartet rot), mit Warnung; eine nicht erwartete ist immer ein Fehler."""
    rep.say("")
    rep.say("== Altlasten bis B5a (noch umzubenennen; Erlaubte Fundstellen des Trockenlaufs, NAEHTE.md)")
    found = list(alt) + list(text_alt)
    for item in found:
        why = ALT_EXPECTED.get(item)
        if why is None:
            rep.err("unbekannte Altlast %s -- nicht in ALT_EXPECTED: umbenennen (BanditsNPCBear*/NCBearCub*) oder nach NCBearBench*" % item)
            continue
        msg = "noch umzubenennen (B5a): %s -- %s" % (item, why)
        rep.say("  " + msg)
        if ARGS["vor_b5a"]:
            rep.warn(msg)
        else:
            rep.err(msg)
    for item in ALT_EXPECTED:
        if item not in found:
            rep.warn("Altlast %s ist weg (in B5a erledigt?) -- aus ALT_EXPECTED und NAEHTE.md streichen" % item)
    if not found and not ALT_EXPECTED:
        rep.say("  keine Altlasten mehr (F2 = B5a: Stummel, kopiertes grosses Modell, Werkbank-Dateien und -Texte; --vor-b5a aendert nichts)")
        return 0
    rep.say("  %d Altlasten (%s)" % (len(found), "--vor-b5a: nur Warnung" if ARGS["vor_b5a"] else "Fehler: Trockenlauf absichtlich rot"))
    return len(found)


# ---------------------------------------------------------------------------------------------------------------------------------
# 2. Form: Lua, Animations-Knoten, GLB
# ---------------------------------------------------------------------------------------------------------------------------------
def glb_json(data, label, rep):
    if len(data) < 20 or data[:4] != b"glTF":
        rep.err("%s: keine GLB-Datei (Kopf)" % label)
        return None
    _magic, ver, length = struct.unpack("<4sII", data[:12])
    clen, ctype = struct.unpack("<I4s", data[12:20])
    if ver != 2 or ctype != b"JSON" or length != len(data):
        rep.err("%s: GLB-Kopf unstimmig (Version %s, Laenge %s/%s)" % (label, ver, length, len(data)))
        return None
    try:
        return json.loads(data[20:20 + clen].decode("utf-8"))
    except ValueError as ex:
        rep.err("%s: GLB-JSON unlesbar (%s)" % (label, ex))
        return None


def vanilla_buck_clips():
    clips = set()
    for dp, _d, fs in os.walk(VANILLA_BUCK):
        for fn in fs:
            if fn.endswith(".xml"):
                try:
                    t = rd(os.path.join(dp, fn)).decode("utf-8", errors="ignore")
                except OSError:
                    continue
                clips.update(re.findall(r"<m_AnimName>\s*([^<\s]+)\s*</m_AnimName>", t))
    return clips


def zombie_knot(rel, final, copy_lua, rep):
    """F2 (PLAN_F2.md 0.3, 7.3): eigener Zombie-Biss-Knoten. Form wie Vanilla media/AnimSets/zombie/bumped/left.xml: genau eine Bedingung
    BumpType (STRING) = m_Name, Clip in Vanillas anims_X/Zombie, am Ende SetVariable BumpAnimFinished=true (sonst bliebe der Zombie im
    Zustand bumped haengen, V:media/actiongroups/zombie/bumped/to_idle.xml); der Name steht in der kopierten Lua (B.ZBITE / B.ZBITE_LOW) und
    ist in NPC Crew (42 + common), Vanilla und Bandits frei (ein gleicher Knoten-Name spielte sonst fremde Bump-Werte mit)."""
    data = final[rel]
    if data.startswith(b"\xef\xbb\xbf"):
        rep.err("%s: BOM" % rel)
        return
    eol_of(data, rel, rep)
    try:
        root = ET.fromstring(data)
    except ET.ParseError as ex:
        rep.err("%s: kein wohlgeformtes XML (%s)" % (rel, ex))
        return
    if root.tag != "animNode":
        rep.err("%s: Wurzel <%s>, erwartet <animNode>" % (rel, root.tag))
    name = (root.findtext("m_Name") or "").strip()
    conds = list(root.iter("m_Conditions"))
    ok = (len(conds) == 1 and (conds[0].findtext("m_Name") or "").strip() == "BumpType"
          and (conds[0].findtext("m_Type") or "").strip() == "STRING" and (conds[0].findtext("m_Value") or "").strip() == name and name)
    if not ok:
        rep.err("%s: genau eine Bedingung BumpType (STRING) = m_Name erwartet -- sonst spielte der Knoten fuer fremde Bump-Werte" % rel)
    anims = [(a.text or "").strip() for a in root.iter("m_AnimName")]
    for a in anims:
        if not (os.path.isfile(os.path.join(VANILLA_ZOMBIE_ANIMS, a + ".X")) or os.path.isfile(os.path.join(VANILLA_ZOMBIE_ANIMS, a + ".x"))):
            rep.err("%s: Clip '%s' liegt nicht in Vanillas anims_X/Zombie" % (rel, a))
    if not anims:
        rep.err("%s: kein m_AnimName" % rel)
    ends = [e for e in root.iter("m_Events") if (e.findtext("m_EventName") or "").strip() == "SetVariable"
            and (e.findtext("m_Time") or "").strip() == "End" and (e.findtext("m_ParameterValue") or "").strip() == "BumpAnimFinished=true"]
    if len(ends) != 1:
        rep.err("%s: am Ende genau ein SetVariable BumpAnimFinished=true erwartet (sonst haengt der Zombie in bumped)" % rel)
    named = any(('"%s"' % name) in "\n".join(c for c, _ in lua_split_lines(final[r].decode("latin-1"))) for r in copy_lua) if name else False
    if not named:
        rep.err("%s: der Knoten-Name %s steht in keiner kopierten Lua-Datei (B.ZBITE / B.ZBITE_LOW)" % (rel, name))
    for no, ln in enumerate(data.decode("latin-1").split("\n"), 1):
        m = XML_CHEAT.search(ln)
        if m:
            rep.err("%s:%d: Wort einer Testhilfe/Debug/Cheat im Animations-Knoten (%s)" % (rel, no, m.group(0)))
    hits = []
    roots = [os.path.join(VANILLA_MEDIA, "AnimSets"), os.path.join(NC_LIVE, "42", "media", "AnimSets"),
             os.path.join(NC_LIVE, "common", "media", "AnimSets")] + [os.path.join(b, "AnimSets") for b in BANDITS_MEDIA]
    pat = re.compile(r"<m_Name>\s*%s\s*</m_Name>|<m_Value>\s*%s\s*</m_Value>" % (re.escape(name), re.escape(name)))
    for base in roots:
        for dp, _d, fs in os.walk(base):
            for fn in fs:
                if fn.endswith(".xml") and pat.search(rd(os.path.join(dp, fn)).decode("latin-1", errors="ignore")):
                    hits.append(os.path.join(dp, fn))
    for h in hits:
        rep.err("Kollision: Zombie-Knoten-Name %s gibt es schon in %s" % (name, h))
    rep.say("  %s: Knoten %s, Clip %s, Ende BumpAnimFinished=true: %s, in der Lua: %s, Kollision (Vanilla/NPC Crew/Bandits): %d" % (
        rel, name, ", ".join(anims), "ja" if len(ends) == 1 else "NEIN", "ja" if named else "NEIN", len(hits)))


def packs_check(final, rep):
    """F4 (PLAN_F4.md 17.1 Nr. 2): scripts/nc_bear_packs.txt -- jedes craftRecipe-Ergebnis steht als item in DIESER Datei (sonst frisst das Rezept die
    Zutaten), jede Zutat Base.X gibt es in Vanillas scripts/generated/items, der Packtaschen-Gegenstand ist kein Behaelter (Capacity/container)."""
    rels = [r for r in final if PACKS_ASSET.match(r)]
    if not rels:
        return
    van = set()
    if os.path.isdir(VANILLA_ITEMS):
        for fn in os.listdir(VANILLA_ITEMS):
            if fn.endswith(".txt"):
                van.update(re.findall(r"^\s*item\s+(\w+)", rd(os.path.join(VANILLA_ITEMS, fn)).decode("latin-1"), re.M))
    for rel in rels:
        text = final[rel].decode("latin-1")
        mods = re.findall(r"^\s*module\s+(\w+)", text, re.M)
        items = {}
        cur = None
        for line in text.split("\n"):
            m = re.match(r"^\s*module\s+(\w+)", line)
            if m:
                cur = m.group(1)
            m = re.match(r"^\s*item\s+(\w+)\s*$", line)
            if m and cur:
                items["%s.%s" % (cur, m.group(1))] = True
        if PACKS_ITEM not in items:
            rep.err("%s: Gegenstand %s fehlt" % (rel, PACKS_ITEM))
        blk = re.search(r"item\s+BearPacks\s*\{(.*?)\}", text, re.S)
        if blk and re.search(r"(?i)\b(Capacity|ItemType\s*=\s*base:container)\b", blk.group(1)):
            rep.err("%s: %s ist ein Behaelter -- die Packtaschen sind eine Zahl im Register (kein Inhalt im Inhalt)" % (rel, PACKS_ITEM))
        n_out = 0
        for m in re.finditer(r"outputs\s*\{(.*?)\}", text, re.S):
            for o in re.findall(r"item\s+\d+\s+([\w.]+)", m.group(1)):
                n_out += 1
                if o not in items:
                    rep.err("%s: Rezept-Ergebnis %s steht nicht als item in dieser Datei" % (rel, o))
        for m in re.finditer(r"inputs\s*\{(.*?)\}", text, re.S):
            for line in m.group(1).split("\n"):
                for name in re.findall(r"Base\.(\w+)", line):
                    if van and name not in van:
                        rep.err("%s: Zutat Base.%s gibt es in Vanillas scripts/generated/items nicht" % (rel, name))
        rep.say("Packtaschen %s: Module %s, Gegenstaende %s, %d Rezept-Ergebnis(se) geprueft" % (rel, ", ".join(mods), ", ".join(sorted(items)), n_out))


def form_check(final, copy_lua, copy_asset, rep):
    for rel in copy_lua:
        data = final[rel]
        if b"\r" in data:
            rep.err("%s: CR in einer neuen Datei (Regel: LF)" % rel)
        if any(c > 126 or (c < 32 and c not in (9, 10)) for c in data):
            rep.err("%s: nicht reines ASCII oder Steuerzeichen" % rel)
        if data.startswith(b"\xef\xbb\xbf"):
            rep.err("%s: BOM" % rel)
        if not data.endswith(b"\n"):
            rep.warn("%s: kein Zeilenende am Schluss" % rel)
        for no, ln in enumerate(data.split(b"\n"), 1):
            if ln.endswith(b"\\"):
                rep.err("%s:%d: Zeile endet mit Backslash (String ueber das Zeilenende)" % (rel, no))
        code = "\n".join(c for c, _ in lua_split_lines(data.decode("latin-1")))
        if re.search(r"(?<![\w.:])next\s*\(", code):
            rep.err("%s: next( -- Kahlua kennt kein next" % rel)
    # GLB des Jungen
    rep.say("")
    rep.say("== Modell und Animations-Knoten")
    glb = final.get(CUB_GLB)
    cub_clips = set()
    if glb is None:
        rep.err("%s fehlt in der Quelle (Platzhalter aus _arbeit/baer_baby/entwurf/ oder Modell aus baer-junges)" % CUB_GLB)
    else:
        j = glb_json(glb, CUB_GLB, rep)
        if j is not None:
            cub_clips = set(a.get("name") for a in j.get("animations", []))
            nm, ns = len(j.get("meshes", [])), len(j.get("skins", []))
            joints = len(j["skins"][0].get("joints", [])) if ns else 0
            rep.say("  %s: MD5 %s, %d KB, %d Netz(e), %d Haut, %d Knochen, %d Clips" % (CUB_GLB, md5(glb), len(glb) // 1024, nm, ns,
                                                                                          joints, len(cub_clips)))
            if nm != 1 or ns != 1:
                rep.err("%s: erwartet genau ein Netz und eine Haut (Werkstatt-CLAUDE.md 8)" % CUB_GLB)
            miss = sorted(vanilla_buck_clips() - cub_clips)
            if miss:
                rep.warn("%s: %d Clips aus Vanillas Animset buck fehlen im GLB (%s) -- der gespielte Erwachsene hat dieselben 15 "
                         "Clips; ob ein Zustand mit fehlendem Clip einfriert, ist ungespielt" % (CUB_GLB, len(miss), ", ".join(miss)))
    # F2 (PLAN_F2.md 7.3): GLB des grossen Baeren (seit F2 kopiert; Form wie beim Jungen)
    big_clips = set()
    bglb = final.get(BIG_GLB)
    if bglb is not None:
        j = glb_json(bglb, BIG_GLB, rep)
        if j is not None:
            big_clips = set(a.get("name") for a in j.get("animations", []))
            nm, ns = len(j.get("meshes", [])), len(j.get("skins", []))
            joints = len(j["skins"][0].get("joints", [])) if ns else 0
            rep.say("  %s: MD5 %s, %d KB, %d Netz(e), %d Haut, %d Knochen, %d Clips" % (BIG_GLB, md5(bglb), len(bglb) // 1024, nm, ns,
                                                                                          joints, len(big_clips)))
            if nm != 1 or ns != 1:
                rep.err("%s: erwartet genau ein Netz und eine Haut (Werkstatt-CLAUDE.md 8)" % BIG_GLB)
    elif any(BIG_ASSET.match(r) for r in copy_asset):
        rep.err("%s fehlt, aber Teile des grossen Modells werden kopiert" % BIG_GLB)
    # Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1 Nr. 3): NCBearCubGen.glb wie NCBearCub.glb, NCBearGen.glb wie NCBear.glb -- 1 Netz,
    # 1 Haut, dieselben Knochen-Namen wie die Standard-GLB DESSELBEN Koerpers (ein Animations-Knoten spielt fuer jede Art mit Animset buck
    # denselben Clip-Namen). Clips: unten (Fressen/Sitzen in allen vier GLBs, Kampf in beiden grossen).
    def glb_bones(jj):
        if not jj or not jj.get("skins"):
            return []
        nodes = jj.get("nodes", [])
        return sorted(str(nodes[i].get("name")) if 0 <= i < len(nodes) else "?" for i in jj["skins"][0].get("joints", []))
    look_clips = {}
    for look_rel, std_rel in ((CUBGEN_GLB, CUB_GLB), (GEN_GLB, BIG_GLB)):
        ldata = final.get(look_rel)
        if ldata is None:
            if any(LOOK_ASSET.match(r) for r in copy_asset):
                rep.err("%s fehlt, aber Teile der Aussehen werden kopiert (LOOK_ASSET)" % look_rel)
            continue
        lj = glb_json(ldata, look_rel, rep)
        if lj is None:
            continue
        sdata = final.get(std_rel)
        sj = glb_json(sdata, std_rel, Report()) if sdata is not None else None      # Fehler der Standard-GLB meldet ihr eigener Block
        clips = set(x.get("name") for x in lj.get("animations", []))
        look_clips[look_rel] = clips
        nm, ns = len(lj.get("meshes", [])), len(lj.get("skins", []))
        lb, sb = glb_bones(lj), glb_bones(sj)
        rep.say("  %s: MD5 %s, %d KB, %d Netz(e), %d Haut, %d Knochen, %d Clips; Knochen-Namen wie %s: %s" % (
            look_rel, md5(ldata), len(ldata) // 1024, nm, ns, len(lb), len(clips), os.path.basename(std_rel),
            "ja" if (sb and lb == sb) else "NEIN"))
        if nm != 1 or ns != 1:
            rep.err("%s: erwartet genau ein Netz und eine Haut (Werkstatt-CLAUDE.md 8)" % look_rel)
        if not sb or lb != sb:
            rep.err("%s: Knochen-Namen weichen von %s ab (gleicher Koerper, gleiche Animations-Knoten) -- %d gegen %d" % (
                look_rel, std_rel, len(lb), len(sb)))
    used_values = set()
    for rel in copy_asset:
        if ZOMBIE_ANIM.match(rel):
            zombie_knot(rel, final, copy_lua, rep)
            continue
        if not ANIMSET_OK.match(rel):
            continue
        data = final[rel]
        if data.startswith(b"\xef\xbb\xbf"):
            rep.err("%s: BOM" % rel)
            continue
        eol_of(data, rel, rep)
        try:
            root = ET.fromstring(data)
        except ET.ParseError as ex:
            rep.err("%s: kein wohlgeformtes XML (%s)" % (rel, ex))
            continue
        if root.tag != "animNode":
            rep.err("%s: Wurzel <%s>, erwartet <animNode>" % (rel, root.tag))
        anims = [(a.text or "").strip() for a in root.iter("m_AnimName")]
        if not anims or not all(anims):
            rep.err("%s: kein m_AnimName" % rel)
        for a in anims:
            # F2: Fressen/Sitzen tragen beide Koerper (Clip in BEIDEN GLBs); die Kampf-Knoten nur der grosse (das Junge kaempft nie --
            # fehlt der Clip im Jungen-GLB, nur Warnung)
            if ANIMSET_BOTH.match(rel):
                if cub_clips and a not in cub_clips:
                    rep.err("%s: Clip '%s' fehlt im GLB des Jungen -- ein Name ohne Clip friert das Tier ein" % (rel, a))
                if big_clips and a not in big_clips:
                    rep.err("%s: Clip '%s' fehlt im GLB des grossen Baeren -- ein Name ohne Clip friert das Tier ein" % (rel, a))
                for lr in sorted(look_clips):            # Aussehen: Fressen/Sitzen in allen vier GLBs
                    if a not in look_clips[lr]:
                        rep.err("%s: Clip '%s' fehlt im GLB des Aussehens %s -- ein Name ohne Clip friert das Tier ein" % (rel, a, lr))
            else:
                if not big_clips or a not in big_clips:
                    rep.err("%s: Clip '%s' fehlt im GLB des grossen Baeren (%s) -- Kampf-Knoten ohne Clip" % (rel, a, BIG_GLB))
                if cub_clips and a not in cub_clips:
                    rep.warn("%s: Clip '%s' nicht im GLB des Jungen (das Junge kaempft nie; nur Hinweis)" % (rel, a))
                if GEN_GLB in look_clips and a not in look_clips[GEN_GLB]:          # Aussehen: Kampf in beiden grossen GLBs
                    rep.err("%s: Clip '%s' fehlt im GLB des Aussehens %s -- Kampf-Knoten ohne Clip" % (rel, a, GEN_GLB))
                if CUBGEN_GLB in look_clips and a not in look_clips[CUBGEN_GLB]:
                    rep.warn("%s: Clip '%s' nicht im GLB des Aussehens %s (das Junge kaempft nie; nur Hinweis)" % (rel, a, CUBGEN_GLB))
        conds = list(root.iter("m_Conditions"))
        mine = [c for c in conds if (c.findtext("m_Name") or "").strip() == ANIM_VAR]
        if len(conds) != 1 or len(mine) != 1:
            rep.err("%s: genau eine Bedingung %s erwartet (%d Bedingungen) -- sonst spielte der Knoten fuer jedes Tier mit Animset "
                    "buck, auch Vanillas Hirsche" % (rel, ANIM_VAR, len(conds)))
        for c in mine:
            if (c.findtext("m_Type") or "").strip() != "STRING":
                rep.err("%s: Bedingung %s nicht vom Typ STRING" % (rel, ANIM_VAR))
            used_values.add((c.findtext("m_Value") or "").strip())
        for no, ln in enumerate(data.decode("latin-1").split("\n"), 1):
            m = XML_CHEAT.search(ln)
            if m:
                rep.err("%s:%d: Wort einer Testhilfe/Debug/Cheat im Animations-Knoten (%s)" % (rel, no, m.group(0)))
    # Jeder Wert, den die Lua an B.ACT setzt, hat einen Knoten.
    for rel in copy_lua:
        code = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        for m in re.finditer(r"setVariable\s*\(\s*B\.ACT\s*,\s*\"(\w+)\"", code):
            if m.group(1) not in used_values:
                rep.err("%s: setzt %s = '%s', dafuer gibt es keinen kopierten Animations-Knoten" % (rel, ANIM_VAR, m.group(1)))
            else:
                rep.say("  %s = '%s' (%s) hat seinen Knoten" % (ANIM_VAR, m.group(1), os.path.basename(rel)))
    # F3 (PLAN_F3.md 6.7, 14.6, 17.1): der Schalter B.CFG.sleepClips in der kopierten shared/BanditsNPCBear.lua. false (F3, Ersatzbild
    # Sitzen): die acht Schlaf-Werte setzt niemand -> sie brauchen noch keinen Knoten. true (ab F3b): JEDER der acht braucht einen
    # kopierten Knoten (Knoten, Clips in allen GLBs und der Schalter kommen zusammen).
    sleep_on = None
    core = final.get("42/media/lua/shared/BanditsNPCBear.lua")
    if core is not None:
        ccode = "\n".join(c for c, _ in lua_split_lines(core.decode("latin-1")))
        sw = SLEEP_SWITCH.findall(ccode)
        if len(sw) == 1:
            sleep_on = sw[0] == "true"
        elif len(sw) > 1:
            rep.err("shared/BanditsNPCBear.lua: sleepClips steht %d-mal im Code -- genau EINE Stelle (B.CFG) erwartet" % len(sw))
    if sleep_on is True:
        missing = [k for k in SLEEP_KEYS if k not in used_values]
        if missing:
            rep.err("B.CFG.sleepClips = true, aber fuer %s gibt es keinen kopierten Animations-Knoten -- der Baer erstarrte stehend "
                    "(Knoten, Clips in allen GLBs und der Schalter kommen zusammen, F3b)" % ", ".join(missing))
        else:
            rep.say("  B.CFG.sleepClips = true: alle acht Schlaf-Werte haben ihren Knoten")
    elif sleep_on is False:
        early = [k for k in SLEEP_KEYS if k in used_values]
        if early:
            rep.warn("Schlaf-Knoten fuer %s werden kopiert, aber B.CFG.sleepClips = false -- sie spielen noch nicht (F3b schaltet um)"
                     % ", ".join(early))
        else:
            rep.say("  B.CFG.sleepClips = false: Ersatzbild Sitzen, die acht Schlaf-Werte brauchen noch keinen Knoten (F3b)")
    # F1 (PLAN_F1.md 5.6): der Sitz-Treiber setzt B.ACT ueber phase(e, obj, "<wert>", now) (client/BanditsNPCBearPose.lua)
    for rel in copy_lua:
        code = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        for val in sorted(set(re.findall(r"\bphase\(\s*\w+\s*,\s*\w+\s*,\s*\"(\w+)\"", code))):
            if val not in used_values:
                if val in SLEEP_KEYS and sleep_on is False:
                    rep.say("  %s = '%s' (%s, Pose-Treiber) wartet auf F3b (sleepClips = false, kein Knoten noetig)"
                            % (ANIM_VAR, val, os.path.basename(rel)))
                else:
                    rep.err("%s: Sitz-Treiber setzt %s = '%s', dafuer gibt es keinen kopierten Animations-Knoten" % (rel, ANIM_VAR, val))
            else:
                rep.say("  %s = '%s' (%s, Sitz-Treiber) hat seinen Knoten" % (ANIM_VAR, val, os.path.basename(rel)))
    # F2 (PLAN_F2.md 0.6, 4.4): die Kampf-Clips setzt U.PoseAct(id, act) mit einer Variablen -- jeder Angriff aus B.ATTACKS
    # (shared/BanditsNPCBearFightRules.lua) braucht deshalb einen kopierten Knoten
    rules = final.get("42/media/lua/shared/BanditsNPCBearFightRules.lua")
    if rules is not None:
        rcode = "\n".join(c for c, _ in lua_split_lines(rules.decode("latin-1")))
        am = re.search(r"\bB\.ATTACKS\s*=\s*B\.ATTACKS\s+or\s+\{([^}]*)\}", rcode)
        if not am:
            rep.err("shared/BanditsNPCBearFightRules.lua: B.ATTACKS nicht gefunden (Liste der Angriffe fuer die Knoten-Pruefung)")
        else:
            for val in sorted(re.findall(r"(\w+)\s*=\s*true", am.group(1))):
                if val not in used_values:
                    rep.err("Angriff '%s' (B.ATTACKS): kein kopierter Animations-Knoten mit %s = '%s'" % (val, ANIM_VAR, val))
                else:
                    rep.say("  %s = '%s' (Angriff, U.PoseAct) hat seinen Knoten" % (ANIM_VAR, val))
    rep.say("  Animations-Knoten: %d, Werte %s; Zombie-Knoten: %d" % (len([r for r in copy_asset if ANIMSET_OK.match(r)]),
                                                                     ", ".join(sorted(used_values)),
                                                                     len([r for r in copy_asset if ZOMBIE_ANIM.match(r)])))
    # B1c: Bilder der Oberflaeche (PNG-Kopf, IHDR-Groesse, gedeckelt); jedes Bild, das die kopierte Lua als media/ui/... nennt, wird
    # mitkopiert -- und jedes kopierte Bild nennt die Lua auch (sonst toter Ballast)
    rep.say("")
    rep.say("== Bilder der Oberflaeche (B1c)")
    named = set()
    for rel in copy_lua:
        code = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        named.update("42/" + m for m in re.findall(r"[\"'](media/ui/BanditsNPCBear[A-Za-z0-9_]*\.png)[\"']", code))
    ui = [r for r in copy_asset if UI_ASSET.match(r)]
    for rel in ui:
        data = final[rel]
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            rep.err("%s: kein PNG (Kopf/IHDR)" % rel)
            continue
        w, h = struct.unpack(">II", data[16:24])
        rep.say("  %s: %d x %d, %d Bytes, MD5 %s" % (rel, w, h, len(data), md5(data)))
        if not (0 < w <= UI_MAX_PX and 0 < h <= UI_MAX_PX):
            rep.err("%s: %d x %d -- erwartet hoechstens %d x %d" % (rel, w, h, UI_MAX_PX, UI_MAX_PX))
        if rel not in named:
            rep.warn("%s wird kopiert, aber keine kopierte Lua-Datei nennt es" % rel)
    for rel in sorted(named - set(ui)):
        rep.err("die Lua nennt %s, das Bild ist nicht in der Uebernahme (fehlt in Test-Mod/Staging)" % rel[3:])
    if not ui and not named:
        rep.say("  keine")


# ---------------------------------------------------------------------------------------------------------------------------------
# 3. Texte
# ---------------------------------------------------------------------------------------------------------------------------------
_cn_chars = None


def vanilla_cn_chars(rep):
    global _cn_chars
    if _cn_chars is not None:
        return _cn_chars
    chars = set()
    if not os.path.isdir(VANILLA_CN):
        rep.err("Vanilla-CN fehlt (%s)" % VANILLA_CN)
    else:
        for fn in os.listdir(VANILLA_CN):
            p = os.path.join(VANILLA_CN, fn)
            if os.path.isfile(p):
                chars.update(rd(p).decode("utf-8", errors="ignore"))
    _cn_chars = chars
    return chars


def dump_json(d):
    return (json.dumps(d, indent=4, ensure_ascii=False) + "\n").encode("utf-8")


def load_json(data, label, rep):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        rep.err("%s: kein UTF-8" % label)
        return None
    if text.startswith("\ufeff"):
        rep.err("%s: BOM am Anfang" % label)
        return None
    try:
        return json.loads(text, object_pairs_hook=collections.OrderedDict)
    except ValueError as ex:
        rep.err("%s: kein gueltiges JSON (%s)" % (label, ex))
        return None


PLACE = re.compile(r"%\d|<LINE>|<BR>")


# DE (NPC Crew v3.14.75, NPC-Crew-CLAUDE.md "JSON-Paritaet"; dort geprueft von _docs/tools/langcheck.py, Art "de-zeichen"): nur Zeichen
# der Sprechblasen-Schrift zomboidDialogue -- U+0020-007E, U+00A1-00A3, U+00A5-00AC, U+00AE-00FF und Zeilenumbruch. Kein U+00A0,
# U+00A4, U+00AD, keine typografischen Anfuehrungszeichen oder Gedankenstriche (in DE als " und --).
def de_char_ok(c):
    o = ord(c)
    return c == "\n" or 0x20 <= o <= 0x7E or 0xA1 <= o <= 0xA3 or 0xA5 <= o <= 0xAC or 0xAE <= o <= 0xFF


def plan_texts(tgt, src, merge, rep):
    """{rel_ziel: neue bytes}, Zusammenfassung, by_file (ohne Altschluessel), Altschluessel. Schreibt nichts."""
    out, summary, text_alt = {}, [], []
    by_file = collections.defaultdict(dict)
    for rel in merge:
        lang, fname = TRANSLATE.match(rel).groups()
        raw = rd(src[rel])
        d = load_json(raw, "Quelle " + rel, rep)
        if d is None:
            continue
        if dump_json(d) != raw:
            rep.err("Quelle %s: nicht im Round-Trip-Format (json.dumps(indent=4, ensure_ascii=False)+'\\n')" % rel)
        ks = list(d)
        if any(a > b for a, b in zip(ks, ks[1:])):
            rep.warn("Quelle %s: nicht sortiert" % rel)
        old = OLD_TEXT_KEYS.get(fname, set())
        bench = BENCH_TEXT_KEYS.get(fname, set())
        for k in list(d):
            if k in old:
                if lang == "EN":
                    text_alt.append("text:%s:%s" % (fname, k))
                del d[k]
            elif k in bench:
                # F2 (PLAN_F2.md 1.4, 7.3): Tiername einer Werkbank-Art -- nie nach NPC Crew, kein Fehler
                if lang == "EN":
                    rep.say("  Werkbank-Text, nie kopiert: %s %s" % (fname, k))
                del d[k]
        by_file[fname][lang] = d
    tdir = os.path.join(tgt, "42", "media", "lua", "shared", "Translate")
    if os.path.isdir(tdir):
        other = [x for x in os.listdir(tdir) if os.path.isdir(os.path.join(tdir, x)) and x not in LANGS]
        if other:
            rep.err("NPC Crew hat Sprachen, die das Skript nicht kennt: %s -- LANGS erweitern" % ", ".join(other))
    # Eine Sprache der Quelle, die LANGS nicht kennt, fiele sonst STILL weg (die Schleifen unten laufen nur ueber LANGS).
    src_unknown = sorted(set(l for d in by_file.values() for l in d) - set(LANGS))
    if src_unknown:
        rep.err("Quelle hat Sprachen, die das Skript nicht kennt: %s -- LANGS erweitern" % ", ".join(src_unknown))
    cn = None
    for fname, langs in sorted(by_file.items()):
        ns = TEXT_NS.get(fname)
        if ns is None:
            rep.err("Texte %s: unbekannte Datei (erlaubt: %s)" % (fname, ", ".join(sorted(TEXT_NS))))
            continue
        missing = [l for l in LANGS if l not in langs]
        if missing:
            rep.err("Texte %s: es fehlen Sprachen %s (alle acht, immer)" % (fname, ",".join(missing)))
        keyset = None
        for l in LANGS:
            if l in langs:
                ks = set(langs[l])
                if keyset is None:
                    keyset = ks
                elif ks != keyset:
                    rep.err("Texte %s: Sprache %s hat andere Schluessel als EN (%s)" % (fname, l, ", ".join(sorted(ks ^ keyset))[:200]))
        en = langs.get("EN", {})
        for k, v in en.items():
            if not (ns[0].match(k) or k in ns[1]):
                rep.err("Texte %s: Schluessel %s liegt nicht im Baeren-Namensraum" % (fname, k))
            if re.search(r"single[ -]player|multi[ -]player", str(v), re.I):
                rep.err("Texte %s %s: EN schreibt 'singleplayer'/'multiplayer' zusammen" % (fname, k))
            # B1b (schnittstelle_aenderungen.md, B1b OBERFLAECHE 1): Tooltips sind Rich-Text (Vanilla client/ISUI/ISButton.lua:317-334 ->
            # ISToolTip.lua:192, :358) -- ein "<" oder ">" in einem UI-Text wuerde dort als Formatbefehl verschluckt.
            if fname == "UI.json":
                for l in LANGS:
                    lv = langs.get(l, {}).get(k)
                    if lv is not None and re.search(r"[<>]", PLACE.sub("", str(lv))):
                        rep.err("Texte UI.json %s %s: '<' oder '>' im Text (Tooltip ist Rich-Text)" % (l, k))
            want = sorted(PLACE.findall(str(v)))
            for l in LANGS:
                if l in langs and k in langs[l] and sorted(PLACE.findall(str(langs[l][k]))) != want:
                    rep.err("Texte %s %s: Platzhalter in %s weichen von EN ab" % (fname, k, l))
        if "CN" in langs:
            cn = cn or vanilla_cn_chars(rep)
            for k, v in langs["CN"].items():
                bad = sorted(set(c for c in str(v) if ord(c) > 127 and c not in cn))
                if bad:
                    rep.err("Texte %s %s: CN-Zeichen, die Vanilla-CN nicht benutzt: %s" % (fname, k, " ".join("U+%04X" % ord(c) for c in bad)))
        if "DE" in langs:
            for k, v in langs["DE"].items():
                bad = sorted(set(c for c in str(v) if not de_char_ok(c)))
                if bad:
                    rep.err("Texte %s %s: DE-Zeichen ausserhalb der Sprechblasen-Schrift: %s" % (fname, k, " ".join("U+%04X" % ord(c) for c in bad)))
        # Vanilla verdecken? (gleicher Schluessel in Vanillas gleichnamiger Datei)
        vp = os.path.join(VANILLA_EN, fname)
        if os.path.isfile(vp):
            try:
                van = json.loads(rd(vp).decode("utf-8", errors="replace"))
            except ValueError:
                van = {}
            for k in en:
                if k in van:
                    rep.err("Texte %s: Schluessel %s gibt es in Vanilla -- unser Text verdeckte Vanillas" % (fname, k))
        counts = {}
        for l in LANGS:
            if l not in langs:
                continue
            rel_t = "42/media/lua/shared/Translate/%s/%s" % (l, fname)
            full_t = os.path.join(tgt, rel_t)
            new = langs[l]
            if os.path.isfile(full_t):
                raw = rd(full_t)
                old = load_json(raw, "NPC Crew " + rel_t, rep)
                if old is None:
                    continue
                if dump_json(old) != raw:
                    rep.err("NPC Crew %s: Round-Trip stimmt nicht -- Abbruch, sonst wuerde die ganze Datei umformatiert" % rel_t)
                    continue
                ks = list(old)
                if any(a > b for a, b in zip(ks, ks[1:])):
                    rep.warn("NPC Crew %s: nicht sortiert, neue Schluessel kommen vor den ersten groesseren" % rel_t)
                add = []
                for k in sorted(new):
                    if k in old:
                        if old[k] != new[k]:
                            rep.err("Texte %s: Schluessel %s gibt es in NPC Crew schon mit anderem Wert -- Kollision" % (rel_t, k))
                    else:
                        add.append(k)
                merged = collections.OrderedDict()
                i = 0
                for k in ks:
                    while i < len(add) and add[i] < k:
                        merged[add[i]] = new[add[i]]
                        i += 1
                    merged[k] = old[k]
                while i < len(add):
                    merged[add[i]] = new[add[i]]
                    i += 1
                data = dump_json(merged)
                again = json.loads(data.decode("utf-8"), object_pairs_hook=collections.OrderedDict)
                if dump_json(again) != data or list(again) != list(merged):
                    rep.err("Texte %s: Round-Trip nach dem Einfuegen stimmt nicht" % rel_t)
                if add:
                    out[rel_t] = data
                counts[l] = (len(old), len(merged), len(add))
            else:
                merged = collections.OrderedDict((k, new[k]) for k in sorted(new))
                out[rel_t] = dump_json(merged)
                counts[l] = (0, len(merged), len(merged))
        totals = set(c[1] for c in counts.values())
        if len(totals) > 1:
            rep.err("Texte %s: nach dem Zusammenfuehren ungleich viele Schluessel je Sprache: %s" % (fname, counts))
        else:
            ref = None
            for l in LANGS:
                rel_t = "42/media/lua/shared/Translate/%s/%s" % (l, fname)
                data = out.get(rel_t)
                if data is None and os.path.isfile(os.path.join(tgt, rel_t)):
                    data = rd(os.path.join(tgt, rel_t))
                if data is None:
                    continue
                ks = set(json.loads(data.decode("utf-8")))
                if ref is None:
                    ref = ks
                elif ks != ref:
                    rep.err("Texte %s: Sprache %s hat nach dem Zusammenfuehren andere Schluessel als EN" % (fname, l))
        if counts:
            c = counts.get("EN") or list(counts.values())[0]
            summary.append("%s: %d neu, %d -> %d je Sprache, %d Sprachen%s" % (fname, c[2], c[0], c[1], len(counts),
                                                                             "" if c[0] else " (Datei neu)"))
    return out, summary, by_file, text_alt


# ---------------------------------------------------------------------------------------------------------------------------------
# 4. Sandbox (Naht 4)
# ---------------------------------------------------------------------------------------------------------------------------------
OPT_BLOCK = re.compile(r"^option\s+(BanditsNPC\.\w+)\s*\{(.*?)^\}", re.M | re.S)


def opts_of_lua(final):
    """B.OPTS aus shared/BanditsNPCBear.lua: Name -> (def, min, max) als Text."""
    data = final.get("42/media/lua/shared/BanditsNPCBear.lua")
    out = {}
    if data is None:
        return out
    for m in re.finditer(r"^\s*(Bear\w+)\s*=\s*\{\s*def\s*=\s*([^,}\s]+)\s*(?:,\s*min\s*=\s*([-\d.]+)\s*,\s*max\s*=\s*([-\d.]+))?\s*\}",
                         data.decode("latin-1"), re.M):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out


def plan_sandbox(tgt, src, rel, final, en_sandbox, rep):
    """{rel: neue bytes} fuer NPC Crews sandbox-options.txt, Zahl der Optionen. Schreibt nichts."""
    rep.say("")
    rep.say("== Sandbox-Optionen (Naht 4: an NPC Crews 42/media/sandbox-options.txt anhaengen)")
    if rel is None:
        rep.say("  keine sandbox-options.txt in der Quelle")
        return {}, 0
    raw = rd(src[rel])
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        rep.err("%s: nicht reines ASCII" % rel)
        return {}, 0
    if "\r" in text:
        rep.err("%s: CR (Regel: LF)" % rel)
    lines = text.split("\n")
    if not lines or lines[0].strip() != "VERSION = 1,":
        rep.err("%s: erste Zeile ist nicht 'VERSION = 1,'" % rel)
        return {}, 0
    body = "\n".join(lines[1:]).strip("\n") + "\n"
    if "VERSION" in body:
        rep.err("%s: VERSION steht noch einmal im Anhang" % rel)
    if re.search(r"^\s*--", body, re.M):
        rep.err("%s: '--'-Kommentar (nur C-Kommentare: ein unlesbarer Kommentar kostet die ganze Seite)" % rel)
    blocks = OPT_BLOCK.findall(body)
    stripped = re.sub(r"/\*.*?\*/", "", OPT_BLOCK.sub("", body), flags=re.S).strip()
    if stripped:
        rep.err("%s: ausser Optionen und C-Kommentaren steht noch etwas da: %r" % (rel, stripped[:80]))
    lua_opts = opts_of_lua(final)
    names = []
    for name, inner in blocks:
        names.append(name)
        short = name[len("BanditsNPC."):]
        if not short.startswith("Bear"):
            rep.err("Sandbox %s: nicht im Namensraum BanditsNPC.Bear*" % name)
        kv = dict((k.strip(), v.strip()) for k, v in re.findall(r"(\w+)\s*=\s*([^,\n]+)", inner))
        if kv.get("page") != "BanditsNPC":
            rep.err("Sandbox %s: page ist nicht BanditsNPC" % name)
        if kv.get("translation") != "BanditsNPC_" + short:
            rep.err("Sandbox %s: translation ist nicht BanditsNPC_%s" % (name, short))
        for key in ("Sandbox_BanditsNPC_" + short, "Sandbox_BanditsNPC_" + short + "_tooltip"):
            if key not in en_sandbox:
                rep.err("Sandbox %s: Text %s fehlt in EN/Sandbox.json" % (name, key))
        if kv.get("type") == "enum":
            n = int(kv.get("numValues", "0"))
            vt = kv.get("valueTranslation", "")
            for i in range(1, n + 1):
                if "Sandbox_%s_option%d" % (vt, i) not in en_sandbox:
                    rep.err("Sandbox %s: Text Sandbox_%s_option%d fehlt" % (name, vt, i))
        lo = lua_opts.get(short)
        if lo is None:
            rep.err("Sandbox %s: fehlt in B.OPTS (shared/BanditsNPCBear.lua)" % name)
        else:
            d, mn, mx = lo
            if kv.get("default") != d:
                rep.err("Sandbox %s: default %s, B.OPTS %s" % (name, kv.get("default"), d))
            if kv.get("type") == "enum":
                # enum: Werte 1..numValues (Vanilla-Form); B.OPTS klemmt auf min..max
                if mn is not None and (mn != "1" or kv.get("numValues") != mx):
                    rep.err("Sandbox %s: enum 1..%s, B.OPTS %s..%s" % (name, kv.get("numValues"), mn, mx))
            elif mn is not None and (kv.get("min") != mn or kv.get("max") != mx):
                rep.err("Sandbox %s: Bereich %s..%s, B.OPTS %s..%s" % (name, kv.get("min"), kv.get("max"), mn, mx))
    for short in lua_opts:
        if "BanditsNPC." + short not in names:
            rep.err("B.OPTS %s hat keine Sandbox-Option" % short)
    tfull = os.path.join(tgt, SANDBOX)
    if not os.path.isfile(tfull):
        rep.err("NPC Crew hat keine %s" % SANDBOX)
        return {}, len(names)
    traw = rd(tfull)
    eol = eol_of(traw, "NPC Crew " + SANDBOX, rep)
    ttext = traw.decode("latin-1").replace("\r\n", "\n")
    nc_names = set(re.findall(r"^option\s+(BanditsNPC\.\w+)", ttext, re.M))
    if body.strip() in ttext:
        if ARGS["erneut"]:
            rep.say("  %d Optionen stehen schon da (--erneut), uebersprungen" % len(names))
            return {}, len(names)
    for name in names:
        if name in nc_names:
            rep.err("Sandbox %s gibt es in NPC Crew schon -- Kollision" % name)
    new = ttext.rstrip("\n") + "\n\n" + body
    data = new.replace("\n", "\r\n").encode("ascii") if eol == b"\r\n" else new.encode("ascii")
    rep.say("  %d Optionen (%s ... %s), NPC Crew vorher %d Optionen, Zeilenenden %s" % (
        len(names), names[0] if names else "-", names[-1] if names else "-", len(nc_names), "CRLF" if eol == b"\r\n" else "LF"))
    return {SANDBOX: data}, len(names)


# ---------------------------------------------------------------------------------------------------------------------------------
# 5. Kollisionen
# ---------------------------------------------------------------------------------------------------------------------------------
def walk_rel(root, sub):
    out = []
    for top in ("42", "common"):
        base = os.path.join(root, top, "media", sub)
        for dp, _d, fs in os.walk(base):
            for fn in fs:
                out.append(rel_of(root, os.path.join(dp, fn)))
    return out


def is_own(rel):
    b = os.path.basename(rel)
    return bool(LUA_BEAR.match(rel) or UI_ASSET.match(rel) or re.match(r"^(NCBear|nc_bear|Item_NCBear)", b, re.I))


def collisions(tgt, final, copy_lua, copy_asset, rep):
    rep.say("")
    rep.say("== Kollisionsbericht (NPC Crew vor der Uebernahme, Vanilla)")
    nc_lua = [r for r in walk_rel(tgt, "lua") if r.endswith(".lua") and not is_own(r)]
    nc_scripts = [r for r in walk_rel(tgt, "scripts") if not is_own(r)]
    nc_anims = [r for r in walk_rel(tgt, "AnimSets") if not is_own(r)]
    pat = re.compile("|".join(OWN_NAME_RES))
    hard, in_comment = [], []
    for rel in nc_lua + nc_scripts + nc_anims:
        try:
            text = rd(os.path.join(tgt, rel)).decode("latin-1")
        except OSError:
            continue
        parts = lua_split_lines(text) if rel.endswith(".lua") else [(ln.rstrip("\r"), "") for ln in text.split("\n")]
        for no, (code, com) in enumerate(parts, 1):
            if pat.search(code):
                if not any(a["file"] == rel and a["line"] == code.strip() for a in NC_ALLOWED):
                    hard.append("%s:%d: %s" % (rel, no, (code + com).strip()[:100]))
            elif pat.search(com):
                in_comment.append("%s:%d" % (rel, no))
    rep.say("Baeren-Namen in NPC Crew (%d Muster): %d im Code, %d nur im Kommentar" % (len(OWN_NAME_RES), len(hard), len(in_comment)))
    for h in hard[:20]:
        rep.err("Kollision: " + h)
    if in_comment:
        rep.warn("Baeren-Namen nur in NPC-Crew-Kommentaren (keine Kollision): %s" % ", ".join(in_comment[:10]))
    for r in sorted(set(walk_rel(tgt, "lua")) | set(walk_rel(tgt, "scripts")) | set(walk_rel(tgt, "AnimSets"))
                    | set(walk_rel(tgt, "models_X")) | set(walk_rel(tgt, "textures")) | set(walk_rel(tgt, "ui"))):
        if is_own(r) and not ARGS["erneut"]:
            rep.err("Kollision: NPC Crew hat schon eine Datei im Baeren-Namensraum: %s" % r)
    for rel in sorted(final):
        if rel.startswith("42/media/lua/shared/Translate/") or rel == SANDBOX:
            continue
        full = os.path.join(tgt, rel)
        if os.path.exists(full) and rd(full) != final[rel] and not ARGS["erneut"]:
            rep.err("Kollision: %s gibt es in NPC Crew schon mit anderem Inhalt" % rel)
    # Gleicher Dateiname: NPC Crew (Ziel und echter Baum) und Vanilla (gleicher relativer Pfad verdeckte Vanillas Datei).
    names = collections.defaultdict(list)
    for root in sorted(set([tgt, NC_LIVE])):
        for sub in ("models_X", "textures", "scripts", "AnimSets", "sound", "ui"):      # B1c: + ui
            for rel in walk_rel(root, sub):
                names[os.path.basename(rel).lower()].append(rel)
    n_van = 0
    n_ban = 0
    for rel in sorted(copy_asset):
        b = os.path.basename(rel).lower()
        others = [o for o in names.get(b, []) if o != rel]
        if others:
            rep.err("Kollision: %s, gleicher Dateiname liegt in NPC Crew unter %s" % (rel, ", ".join(sorted(set(others)))))
        vp = os.path.join(VANILLA_MEDIA, rel[len("42/media/"):])
        if os.path.exists(vp):
            n_van += 1
            rep.err("Kollision: %s verdeckte Vanillas Datei %s" % (rel, vp))
        # B1c: Bandits ist Pflicht-Mod von NPC Crew; ein gleicher media/ui-Pfad verdeckte Bandits' Bild (oder umgekehrt)
        if UI_ASSET.match(rel):
            for bm in BANDITS_MEDIA:
                bp = os.path.join(bm, rel[len("42/media/"):])
                if os.path.exists(bp):
                    n_ban += 1
                    rep.err("Kollision: %s liegt auch in Bandits (%s)" % (rel, bp))
    rep.say("Dateinamen gegen NPC Crew, Vanilla und Bandits (media/ui): %d Vanilla-Treffer, %d Bandits-Treffer" % (n_van, n_ban))
    # Modell-/Skriptnamen und Tierart gegen Vanilla.
    van_scripts = os.path.join(VANILLA_MEDIA, "scripts")
    own_models = set()
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        # F4: nur echte Namen (Buchstabe zuerst, allein auf der Zeile) -- Rezept-Zeilen "item 4 [Base.X] ..." (scripts/nc_bear_packs.txt) sind keine
        own_models.update(re.findall(r"^\s*(?:model|animationsMesh|item|sound)\s+([A-Za-z_]\w*)\s*$", final[rel].decode("latin-1"), re.M))
    hits = []
    for dp, _d, fs in os.walk(van_scripts):
        for fn in fs:
            t = rd(os.path.join(dp, fn)).decode("latin-1")
            for nm in own_models:
                if re.search(r"^\s*(?:model|animationsMesh|item|sound)\s+%s\b" % re.escape(nm), t, re.M):
                    hits.append("%s in %s" % (nm, fn))
    for nc in nc_scripts:
        t = rd(os.path.join(tgt, nc)).decode("latin-1")
        for nm in own_models:
            if re.search(r"^\s*(?:model|animationsMesh|item|sound)\s+%s\b" % re.escape(nm), t, re.M):
                hits.append("%s in NPC Crew %s" % (nm, nc))
    for h in hits:
        rep.err("Kollision Skriptname: " + h)
    rep.say("Skriptnamen %s gegen Vanilla und NPC Crew: %d Treffer" % (", ".join(sorted(own_models)) or "-", len(hits)))
    van_lua = os.path.join(VANILLA_MEDIA, "lua")
    vhits = 0
    for dp, _d, fs in os.walk(van_lua):
        for fn in fs:
            if fn.endswith(".lua") and re.search(r"ncbear|NCBear|BanditsNPCBear", rd(os.path.join(dp, fn)).decode("latin-1")):
                vhits += 1
                rep.err("Kollision: Vanilla %s nennt einen Baeren-Namen" % os.path.join(dp, fn))
    rep.say("Baeren-Namen in Vanilla-Lua: %d" % vhits)
    # Globale der kopierten Dateien gegen NPC Crew; v3.8.38 (Funktion gegen Modultabelle).
    own_globals = set()
    for rel in copy_lua:
        text = final[rel].decode("latin-1")
        for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)", text, re.M):
            if m.group(1) not in GLOBAL_OK and m.group(1) not in GLOBAL_SAME:
                own_globals.add(m.group(1))
    for g in sorted(own_globals):
        for rel in nc_lua:
            t = rd(os.path.join(tgt, rel)).decode("latin-1")
            if re.search(r"(^|[^.\w])%s\s*=|function %s\s*\(" % (re.escape(g), re.escape(g)), t, re.M):
                rep.err("Kollision: Global %s wird auch in NPC Crew %s gesetzt" % (g, rel))
                break
    fn, mod = set(), set()
    for rel in set(nc_lua) | set(copy_lua):
        text = final[rel].decode("latin-1") if rel in final else rd(os.path.join(tgt, rel)).decode("latin-1")
        fn.update(re.findall(r"^function BanditsNPC\.([A-Za-z_]*)\(", text, re.M))
        mod.update(m.group(1) for m in re.finditer(r"BanditsNPC\.([A-Za-z_]*) = BanditsNPC\.\1 or \{\}", text))
    both = sorted(fn & mod)
    rep.say("Globale der Baeren-Dateien: %s; v3.8.38-Probe: %d Funktionen gegen %d Modultabellen, Kollision: %s" % (
        ", ".join(sorted(own_globals)) or "-", len(fn), len(mod), ", ".join(both) or "keine"))
    for b in both:
        rep.err("Kollision v3.8.38: BanditsNPC.%s ist Funktion UND Modultabelle" % b)
    # Skript des Jungen: mesh liegt auf der Platte, Textur der Rasse liegt auf der Platte.
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        text = final[rel].decode("latin-1")
        for kind, val in re.findall(r"^\s*(mesh|meshFile)\s*=\s*([^,\s]+)", text, re.M):
            p = "42/media/models_X/" + val
            if p not in final:
                rep.err("%s: %s = %s liegt nicht in der Uebernahme (%s)" % (rel, kind, val, p))
        rep.say("Skript %s: Module %s, Namen %s" % (rel, ", ".join(re.findall(r"^\s*module\s+(\w+)", text, re.M)),
                                                  ", ".join(re.findall(r"^\s*(?:model|animationsMesh|sound)\s+(\w+)", text, re.M))))
        # F2 (PLAN_F2.md 7.3): jede Ton-Datei eines sound-Blocks liegt in der Uebernahme (sonst spielte die Rasse einen leeren Ton)
        for val in re.findall(r"^\s*file\s*=\s*media/(sound/[^,\s]+)", text, re.M):
            if "42/media/" + val not in final:
                rep.err("%s: file = media/%s liegt nicht in der Uebernahme" % (rel, val))
    defs = final.get("42/media/lua/shared/BanditsNPCBearDefs.lua")
    if defs:
        dtext = defs.decode("latin-1")
        # F2 (PLAN_F2.md 1.1): jeder Ton-Name der Rasse (sounds.<schluessel> = { name = "NCBear_*" ... }) hat seinen sound-Block in einem
        # kopierten Skript (scripts/nc_bear_sounds.txt); playBreedSound spielt sonst nichts
        snd_def = set()
        for r in [x for x in final if x.startswith("42/media/scripts/")]:
            snd_def.update(re.findall(r"^\s*sound\s+(\w+)", final[r].decode("latin-1"), re.M))
        snd_used = sorted(set(re.findall(r"\bname\s*=\s*\"(NCBear_\w+)\"", "\n".join(c for c, _ in lua_split_lines(dtext)))))
        for s in snd_used:
            if s not in snd_def:
                rep.err("Defs: Ton %s der Rasse hat keinen sound-Block in einem kopierten Skript" % s)
        rep.say("Toene der Rasse: %s -- je ein sound-Block: %s" % (", ".join(snd_used) or "-",
                                                                   "ja" if all(s in snd_def for s in snd_used) else "NEIN"))
        # B1e: Fehlt ein Teil, das ALT_DEFS als Altlast bis B5a fuehrt, gilt dieselbe Regel wie fuer ALT_EXPECTED (alt_report): ohne
        # --vor-b5a Fehler, mit Warnung. Ist es inzwischen da (B5a), meldet das Skript, dass der Eintrag zu streichen ist.
        def defs_missing(kind, val, msg):
            why = ALT_DEFS.get((kind, val))
            if why is None:
                rep.err(msg)
                return
            line = "noch umzubenennen (B5a): Defs %s %s -- %s" % (kind, val, why)
            rep.say("  " + line)
            if ARGS["vor_b5a"]:
                rep.warn(line)
            else:
                rep.err(line)
        seen_defs = set()
        for val in sorted(set(re.findall(r"\btexture(?:Male|Baby)?\s*=\s*\"(\w+)\"", dtext))):
            seen_defs.add(("texture", val))
            if "42/media/textures/Body/%s.png" % val not in final:
                defs_missing("texture", val, "Defs: Rassen-Textur %s liegt nicht als 42/media/textures/Body/%s.png in der Uebernahme" % (val, val))
            elif ("texture", val) in ALT_DEFS:
                rep.warn("ALT_DEFS: Rassen-Textur %s liegt jetzt in der Uebernahme (B5a erledigt?) -- aus ALT_DEFS und NAEHTE.md streichen" % val)
        for val in re.findall(r"\bbodyModel\s*=\s*\"(\w+)\"", dtext):
            seen_defs.add(("bodyModel", val))
            if not any(re.search(r"^\s*model\s+%s\b" % re.escape(val), final[r].decode("latin-1"), re.M)
                       for r in final if r.startswith("42/media/scripts/")):
                defs_missing("bodyModel", val, "Defs: bodyModel %s hat kein model-Skript in der Uebernahme" % val)
            elif ("bodyModel", val) in ALT_DEFS:
                rep.warn("ALT_DEFS: bodyModel %s hat jetzt ein model-Skript in der Uebernahme (B5a erledigt?) -- aus ALT_DEFS streichen" % val)
        for key in ALT_DEFS:
            if key not in seen_defs:
                rep.warn("ALT_DEFS %s %s steht nicht mehr in BanditsNPCBearDefs.lua -- aus ALT_DEFS und NAEHTE.md streichen" % key)
    # Texte: jeder Schluessel aus der Lua steht in EN; englische Ersatztexte (U.EN) wortgleich.
    rel_en = "42/media/lua/shared/Translate/EN/UI.json"
    data = final.get(rel_en)
    if data is None and os.path.isfile(os.path.join(tgt, rel_en)):
        data = rd(os.path.join(tgt, rel_en))
    en_final = json.loads(data.decode("utf-8")) if data else {}
    used = set()
    fallback = {}
    for rel in copy_lua:
        t = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        for k in re.findall(r'"(UI_BN_[A-Za-z0-9_]+)"', t):
            if not k.endswith("_"):
                used.add(k)
        # englische Ersatztexte: nur der Block "U.EN = { ... }" (client/BanditsNPCBearClient.lua); andere Tabellen mit
        # Textschluesseln als Feldnamen (WHY_T im Server) sind keine Ersatztexte
        blk = re.search(r"^U\.EN\s*=\s*\{\s*$(.*?)^\}", t, re.M | re.S)
        if blk:
            for k, v in re.findall(r'^\s*(UI_BN_Bear_[A-Za-z0-9_]+)\s*=\s*"((?:[^"\\]|\\.)*)"\s*,', blk.group(1), re.M):
                fallback[k] = v
    miss = sorted(k for k in used if k not in en_final)
    for k in miss:
        rep.err("Text %s wird in der Baeren-Lua benutzt, steht aber nicht in EN/UI.json" % k)
    own_en = dict((k, v) for k, v in en_final.items() if k.startswith("UI_BN_Bear_"))
    for k, v in sorted(fallback.items()):
        if own_en.get(k) != v:
            rep.err("Ersatztext %s weicht von EN/UI.json ab" % k)
    for k in sorted(set(own_en) - set(fallback)):
        rep.warn("EN-Schluessel %s hat keinen englischen Ersatztext im Code" % k)
    rep.say("Texte aus der Lua: %d benutzt, fehlen in EN: %d; Ersatztexte %d, wortgleich: %s" % (
        len(used), len(miss), len(fallback), "ja" if all(own_en.get(k) == v for k, v in fallback.items()) else "NEIN"))


# ---------------------------------------------------------------------------------------------------------------------------------
# 6. Cheat-Pruefung und Tier-Regel
# ---------------------------------------------------------------------------------------------------------------------------------
def call_args(text, start):
    args, cur, depth, i, n = [], [], 0, start, len(text)
    while i < n:
        c = text[i]
        if c == '"' or c == "'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            cur.append(text[i:j + 1])
            i = j + 1
            continue
        if c in "({[":
            depth += 1
        elif c in ")}]":
            if depth == 0:
                args.append("".join(cur))
                return args
            depth -= 1
        elif c == "," and depth == 0:
            args.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    args.append("".join(cur))
    return args


def lua_setglobals(data):
    if not os.path.isfile(LUAC):
        return None
    fd, tmp = tempfile.mkstemp(suffix=".lua", prefix="baer_luac_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        p = subprocess.run([LUAC, "-p", "-l", tmp], capture_output=True, text=True, errors="replace")
        if p.returncode != 0:
            return None
        return [(int(m.group(1)), m.group(2)) for m in re.finditer(r"\[(\d+)\]\s+SETGLOBAL\s+[^;\n]*;\s*([A-Za-z_]\w*)", p.stdout)]
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def global_ok(name, code):
    if name in GLOBAL_OK:
        return True
    if name in GLOBAL_SAME:
        return re.match(r"^\s*%s\s*=\s*%s\s+or\s+\{\s*\}\s*$" % (re.escape(name), re.escape(name)), code) is not None
    # Aktionsklassen: BanditsNPCBear*Action = ISBaseTimedAction:derive("gleicher Name")
    return name.startswith("BanditsNPCBear") and re.match(
        r"^\s*%s\s*=\s*ISBaseTimedAction:derive\s*\(\s*[\"']%s[\"']\s*\)\s*;?\s*$" % (re.escape(name), re.escape(name)), code) is not None


def _strings_of(code):
    out = [s.group(1) if s.group(1) is not None else s.group(2) for s in LUA_STRING.finditer(code)]
    out += [s.group(2) for s in LONG_STRING.finditer(code)]
    return out


def _norm_text(s):
    return s.strip().rstrip(".").strip().casefold()


def bench_marks(plan, src, copy_fn_names):
    """Texte (addOption/say/print-Helfer) und Funktionsnamen der NCBearBench*-Dateien. Namen, die auch eine kopierte Datei als
    Funktion definiert, zaehlen nicht als Fingerabdruck (sonst meldete die Pruefung den Kern)."""
    texts, funcs, shared = set(), set(), set()
    for rel, _why in plan["skipped"]:
        if not (rel.endswith(".lua") and BENCH_ANY.match(os.path.basename(rel))):
            continue
        for code, _com in lua_split_lines(rd(src[rel]).decode("latin-1")):
            m = re.match(r"^\s*(?:local\s+)?function\s+([A-Za-z_]\w*)\s*\(", code)
            if m:
                (shared if m.group(1) in copy_fn_names else funcs).add(m.group(1))
            plain = re.search(r"\baddOption\w*\s*\(|\bsay\s*\(", code)
            helper = (not plain) and re.search(r"\b\w*[Ss]ay\s*\(|\bline\s*\(", code)
            if plain or helper:
                for s in _strings_of(code):
                    t = _norm_text(s)
                    # nur Saetze und Menuetexte (zwei Woerter oder lang): einzelne Woerter wie "bait", "cub", "bear" sind
                    # Fachwoerter, die der echte Code auch braucht (sonst meldete die Pruefung den Kern)
                    if re.search(r"[a-z].*[a-z]", t) and (" " in t or len(t) >= 10):
                        texts.add(t)
    return texts, funcs, shared


def cheat_check(plan, src, rep):
    rep.say("")
    rep.say("== Cheat-Pruefung (Kevin 08.11.: keine Cheat- oder Testmenues nach NPC Crew) und Tier-Regel (Plan 12.1 Punkt 7)")
    final = plan["final"]
    rules = [(rid, re.compile(rx), why) for rid, rx, why in CHEAT_RULES]
    found, comments, seen = [], [], set()
    used = [[] for _ in CHEAT_ALLOWED]
    tier_used = collections.defaultdict(list)
    copy_fn = set()
    for rel in plan["copy_lua"]:
        copy_fn.update(re.findall(r"^\s*(?:local\s+)?function\s+(?:[\w.:]*[.:])?([A-Za-z_]\w*)\s*\(", final[rel].decode("latin-1"), re.M))
    prints, bfuncs, bshared = bench_marks(plan, src, copy_fn)

    def add(rel, no, rid, code, why, what):
        key = (rel, no, rid, what)
        if key in seen:
            return
        seen.add(key)
        for i, a in enumerate(CHEAT_ALLOWED):
            # F1B: "exact" -- die Ausnahme gilt nur fuer genau diese Zeile (Code-Teil ohne Rand), nie fuer eine verlaengerte
            hit = (a["code"] == code.strip()) if a.get("exact") else (a["code"] in code)
            if a["file"] == rel and a["rule"] == rid and hit:
                used[i].append("%s:%s" % (rel, no) if no else rel)
                return
        found.append("%s: %s [%s: %s]" % ("%s:%d" % (rel, no) if no else rel, why, rid, what))

    def check_code(rel, no, code):
        for rid, rx, why in rules:
            m = rx.search(code)
            if m:
                add(rel, no, rid, code, why, m.group(0))
        for body in _strings_of(code):
            m = CHEAT_STRING.search(body)
            if m:
                add(rel, no, "wort", code, "Cheat-/Spawn-/Debug-Wort in einem String im Code", body[:40])
            if _norm_text(body) in prints:
                add(rel, no, "bankspur", code, "Text aus dem Werkbank-Menue", body[:40])
        for m in CHEAT_GLOBAL_FN.finditer(code):
            if not re.search(r"\blocal\s+$", code[:m.start()]):
                add(rel, no, "global", code, "globale Funktion (in der Konsole aufrufbar: Konsolenbefehl)", m.group(1))
        m = CHEAT_GLOBAL_SET.match(code)
        if m and not global_ok(m.group(1), code):
            add(rel, no, "global", code, "globale Zuweisung (in der Konsole aufrufbar)", m.group(1))
        m = re.match(r"^\s*(?:local\s+)?function\s+(\w+)\s*\(", code)
        if m and m.group(1) in bfuncs:
            add(rel, no, "bankspur", code, "Funktionsname aus der Werkbank", m.group(1))

    def menu_check(rel, codes):
        code_text = "\n".join(codes)
        local_str = set(m.group(1) for m in re.finditer(r"\blocal\s+(\w+)\s*=\s*[\"'][^\"'\n]*[A-Za-z][^\"'\n]*[A-Za-z]", code_text))
        for rx in (MENU_CALL, BTN_CALL):
            for m in rx.finditer(code_text):
                args = call_args(code_text, m.end())
                if rx is BTN_CALL:
                    texts = args[4:5] if "ISButton" in m.group(0) else args[:1]
                else:
                    texts = args[:2] if m.group(1).startswith("insert") else args[:1]
                no = code_text.count("\n", 0, m.start()) + 1
                for a in texts:
                    lits = _strings_of(TEXT_CALL.sub("", a))
                    if any(re.search(r"[A-Za-z].*[A-Za-z]", x) for x in lits) or a.strip() in local_str:
                        add(rel, no, "menue", codes[no - 1], "Menue-Eintrag mit festem Text statt Textschluessel (Testmenue?)", a.strip()[:40])
        # B1c: Optionen-Seite (PZAPI.ModOptions) -- jedes Text-Argument ist ein Schluessel UI_BN_Bear_* (Vanilla ruft getText), nie
        # ein fester Satz, nie ein Ausdruck (Nachbesserung B1c A4: mo_text_hits)
        for no, what, why in mo_text_hits(code_text):
            add(rel, no, "menue", codes[no - 1], why, what)

    n_lines = 0
    for rel in plan["copy_lua"]:
        rest = os.path.basename(rel)[len("BanditsNPCBear"):]
        if CHEAT_NAME.search(rest) or CHEAT_FILE_REST.match(rest):
            add(rel, 0, "dateiname", os.path.basename(rel), "Dateiname nach Testhilfe/Debug/Cheat/Werkzeug", os.path.basename(rel))
        parts = lua_split_lines(final[rel].decode("latin-1"))
        cur_fn = None
        for no, (code, com) in enumerate(parts, 1):
            head = FN_HEAD.match(code)
            if head:
                cur_fn = head.group(1) or head.group(2)
            elif code[:1] not in ("", " ", "\t"):
                cur_fn = None
            if code.strip():
                n_lines += 1
                check_code(rel, no, code)
                if not TIER_DEF.match(code):
                    for tid, rx, allowed, why in TIER_RULES:
                        if rx.search(code):
                            if (rel, cur_fn) in allowed:
                                tier_used[tid].append("%s:%d (%s)" % (os.path.basename(rel), no, cur_fn or "Dateiebene"))
                            else:
                                add(rel, no, "tier", code, "%s -- Aufruf aus %s" % (why, cur_fn or "Dateiebene"), tid)
            if re.search(r"\bNC[A-Z][A-Za-z]*_[A-Za-z]|\bNC[A-Za-z]*Bench|(?i:\btesthilfe\b|\bwerkbank\b)", com):
                comments.append("%s:%d" % (rel, no))
        code_lines = [c for c, _ in parts]
        menu_check(rel, code_lines)
        code_text = "\n".join(code_lines)
        for off, what in scan_force_hits(code_text):
            no = code_text.count("\n", 0, off) + 1
            add(rel, no, "force", code_lines[no - 1], SCAN_WHY, what)
        sg = lua_setglobals(final[rel])
        if sg is None:
            rep.warn("%s: luac5.1 lief nicht (%s) -- globale Zuweisungen nur per Regex geprueft" % (rel, LUAC))
        else:
            for ln, name in sg:
                gcode = parts[ln - 1][0] if 0 < ln <= len(parts) else ""
                if not global_ok(name, gcode):
                    add(rel, ln, "global", gcode, "globale Zuweisung laut luac", name)
    for rel in plan["copy_asset"]:
        b = os.path.basename(rel)
        if CHEAT_NAME.search(b):
            add(rel, 0, "dateiname", b, "Dateiname nach Testhilfe/Debug/Cheat/Spawn", b)
    n_text = 0
    for fname, langs in sorted(plan["by_file"].items()):
        for l, d in sorted(langs.items()):
            for k, v in d.items():
                n_text += 1
                kk = k[len("UI_BN_"):] if k.startswith("UI_BN_") else k
                if CHEAT_NAME.search(kk):
                    add("Translate/" + fname, 0, "text", k, "Textschluessel nach Testhilfe/Debug/Cheat/Spawn", k)
                if l == "EN":
                    if CHEAT_TEXT.search(str(v)):
                        add("Translate/" + fname, 0, "text", k, "EN-Text klingt nach Test-/Cheat-Menue", "%s = '%s'" % (k, str(v)[:50]))
                    if _norm_text(str(v)) in prints:
                        add("Translate/" + fname, 0, "bankspur", k, "EN-Text aus dem Werkbank-Menue", k)
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        text = final[rel].decode("latin-1")
        for m in re.finditer(r"^\s*(?:item|model|animationsMesh)\s+(\w+)", text, re.M):
            if re.search(r"(?i)bench|cheat|debug|spawn|test", m.group(1)):
                add(rel, 0, "skript", m.group(1), "Skriptname nach Testhilfe/Debug/Cheat/Spawn", m.group(1))
    if SANDBOX in final:
        for name in re.findall(r"^option\s+(BanditsNPC\.\w+)", plan["sandbox_body"], re.M):
            if CHEAT_NAME.search(name):
                add(SANDBOX, 0, "sandbox", name, "Sandbox-Option nach Testhilfe/Debug/Cheat/Spawn", name)
    rep.say("geprueft: %d Lua-Dateien (%d Codezeilen), %d Texte, %d Dateinamen; %d Zeilenregeln + wort, global, menue, tier, force, "
            "bankspur (%d Werkbank-Texte, %d Werkbank-Funktionsnamen; %d gemeinsame Namen nicht gewertet: %s); %d Ausnahmen" % (
                len(plan["copy_lua"]), n_lines, n_text, len(plan["copy_lua"]) + len(plan["copy_asset"]), len(CHEAT_RULES),
                len(prints), len(bfuncs), len(bshared), ", ".join(sorted(bshared)) or "-", len(CHEAT_ALLOWED)))
    for a, hits in zip(CHEAT_ALLOWED, used):
        if hits:
            rep.say("  erlaubt %s [%s] (%s)" % (", ".join(hits), a["rule"], a["why"]))
        else:
            rep.warn("Cheat-Ausnahme greift nicht mehr (streichen?): %s [%s] %s" % (a["file"], a["rule"], a["code"]))
    for tid, _rx, allowed, why in TIER_RULES:
        hits = tier_used.get(tid, [])
        rep.say("  Tier-Regel %s: %s -- %s" % (tid, ", ".join(hits) or ("kein Aufruf" if allowed else "kein Aufruf (erlaubt: nirgends)"), why))
        if not hits and allowed:              # B1d: eine Regel ohne erlaubten Aufrufer (probeweg) erwartet keinen
            rep.warn("Tier-Regel %s: kein erlaubter Aufruf gefunden (Code umgebaut? TIER_RULES nachziehen)" % tid)
    if comments:
        rep.warn("Kommentare in Baeren-Dateien nennen Testbefehle oder die Testhilfe (kein Cheat): %s" % ", ".join(comments[:12]))
    rep.say("Funde: %d" % len(found))
    for f in found:
        rep.err("Cheat-Pruefung: " + f)
    return len(found)


# ---------------------------------------------------------------------------------------------------------------------------------
# 6b. Optionsnamen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 12.1 Nr. 7; Sandbox-Kuerzung Kevin 12.11.2026: 39 -> 12)
# ---------------------------------------------------------------------------------------------------------------------------------
OPT_CALL = re.compile(r"\b(?:Opt|opt|optNum)\s*\(\s*\"(Bear\w+)\"")
# Nachbesserung Aussehen A3 (PRUEF_A.md): die 29 Optionen, die die Sandbox-Kuerzung (Kevin 12.11.2026) zu festen Werten in B.CFG gemacht
# hat (Test-Mod 99e0368, 42/media/sandbox-options.txt: 39 Optionen; es bleiben 10 + 2 neue). Ihr Name darf im Code-Teil der kopierten Lua
# nie mehr als String stehen -- auch nicht ueber einen Umweg (local f = B.Opt; f("BearRoamRadius")) oder als "BanditsNPC.<Name>" /
# "..._<Name>" (Sandbox-Textschluessel). Kommentare zaehlen nicht.
REMOVED_OPTS = (
    "BearCubMinDistance", "BearCubMaxDistance", "BearCubWorldCap", "BearBaitNights", "BearBaitFirstChance", "BearTameFeedPoints",
    "BearTamePetPoints", "BearTameMixBonus", "BearTameFavoriteBonus", "BearTameMinFeedings", "BearFeedCooldownMinutes",
    "BearPetCooldownMinutes", "BearCubVanishHours", "BearDeathLockDays", "BearFollowMaxDistance", "BearRideDistance",
    "BearCallCooldownMinutes", "BearDodgeMax", "BearFightBonusMax", "BearHealAwake", "BearHealSleep", "BearRoamRadius",
    "BearZombiesAttack", "BearZombieDamage", "BearBanditDamage", "BearBandageHeal", "BearBandageHours", "BearDownedHours", "BearLog",
)
REMOVED_LIT = re.compile(r"(?:^|[._])(%s)$" % "|".join(REMOVED_OPTS))


def opt_name_check(plan, rep):
    """Jedes Literal "Bear..." als erstes Argument von Opt( / opt( / optNum( im Code-Teil einer kopierten Lua-Datei muss ein Schluessel von
    B.OPTS sein (shared/BanditsNPCBear.lua, opts_of_lua). Eine Option, die die Sandbox-Kuerzung zu einem festen Wert in B.CFG gemacht hat,
    liefert ueber B.Opt nur noch nil (plus Fehlerzeile) -- eine vergessene Lesestelle rechnete dann falsch. Kommentare zaehlen nicht.
    Nachbesserung Aussehen A3: dazu JEDES String-Literal im Code-Teil, das einer der 29 entfernten Optionsnamen ist (REMOVED_LIT) --
    gleich, wie es gelesen wuerde (Umweg ueber einen Namen, SandboxVars-Feld, Textschluessel). SandboxVars selbst: Tier-Regel."""
    rep.say("")
    rep.say("== Optionsnamen (Sandbox-Kuerzung: jede Lesestelle nennt eine Option aus B.OPTS; kein entfernter Name als String)")
    final = plan["final"]
    known = opts_of_lua(final)
    if not known:
        rep.err("B.OPTS nicht gefunden (shared/BanditsNPCBear.lua) -- Optionsnamen nicht pruefbar")
        return 0
    both = sorted(set(REMOVED_OPTS) & set(known))
    if both:
        rep.err("REMOVED_OPTS und B.OPTS ueberschneiden sich: %s -- Liste nachziehen" % ", ".join(both))
    n, bad, n_lit = 0, 0, 0
    for rel in plan["copy_lua"]:
        parts = lua_split_lines(final[rel].decode("latin-1"))
        for no, (code, _com) in enumerate(parts, 1):
            for m in OPT_CALL.finditer(code):
                n += 1
                if m.group(1) not in known:
                    bad += 1
                    rep.err("%s:%d: Option %s steht nicht in B.OPTS (shared/BanditsNPCBear.lua) -- vergessene Lesestelle einer festen "
                            "Option? Den Wert aus B.CFG lesen" % (rel, no, m.group(1)))
            for s in _strings_of(code):
                mm = REMOVED_LIT.search(s)
                if mm:
                    n_lit += 1
                    bad += 1
                    rep.err("%s:%d: der Code nennt die entfernte Sandbox-Option %s (\"%s\") -- seit der Sandbox-Kuerzung ein fester Wert "
                            "in B.CFG" % (rel, no, mm.group(1), s[:60]))
    rep.say("  %d Lesestellen mit Optionsnamen; B.OPTS %d Optionen (%s); unbekannt: %d; entfernte Namen als String: %d (Liste %d)" % (
        n, len(known), ", ".join(sorted(known)), bad - n_lit, n_lit, len(REMOVED_OPTS)))
    return bad


# ---------------------------------------------------------------------------------------------------------------------------------
# 6c. Aussehen-Arten (Nachbesserung Aussehen A4, PRUEF_A.md): B.LOOKS nennt nur echte, kopierte Arten
# ---------------------------------------------------------------------------------------------------------------------------------
LOOKS_HEAD = re.compile(r"\bB\.LOOKS\s*=\s*B\.LOOKS\s+or\s*\{")
ART_LIT = re.compile(r"\bart\s*=\s*\"([^\"]+)\"")
BENCH_ART = re.compile(r"\banimals\s*\[\s*\"(\w+)\"\s*\]\s*=(?!=)|\bname\s*=\s*\"(\w+)\"")
BENCH_DEFS = re.compile(r"^NCBearBench\w*Defs\.lua$", re.I)


def looks_check(plan, src, rep):
    """Jede Art in B.LOOKS (shared/BanditsNPCBear.lua, Code-Teil) muss (1) als String-Literal im Code-Teil der kopierten
    shared/BanditsNPCBearDefs.lua stehen (dort wird sie definiert), (2) darf in keiner Werkbank-Datei NCBearBench*Defs.lua definiert sein
    (animals["<art>"] = ... / name = "<art>") und (3) braucht ihren Tiernamen IGUI_AnimalType_<art> in den kopierten IG_UI-Texten (EN).
    Sonst gaebe es in NPC Crew ein Aussehen ohne Definition (Knopf grau / Why_LookMissing), und in der Test-Mod zaehlte eine Werkbank-Art
    als unser Baer (B.TYPE_BODY wird aus B.LOOKS gebaut). Rueckgabe: Zahl der Fehler."""
    rep.say("")
    rep.say("== Aussehen-Arten (B.LOOKS: nur echte, kopierte Arten, nie eine Werkbank-Art)")
    final = plan["final"]
    main = final.get("42/media/lua/shared/BanditsNPCBear.lua")
    defs = final.get("42/media/lua/shared/BanditsNPCBearDefs.lua")
    if main is None or defs is None:
        rep.err("Aussehen-Arten: shared/BanditsNPCBear.lua oder shared/BanditsNPCBearDefs.lua wird nicht kopiert")
        return 1
    code = "\n".join(c for c, _ in lua_split_lines(main.decode("latin-1")))
    m = LOOKS_HEAD.search(code)
    if not m:
        rep.err("B.LOOKS nicht gefunden (shared/BanditsNPCBear.lua) -- Aussehen-Arten nicht pruefbar")
        return 1
    depth, i = 1, m.end()
    while i < len(code) and depth > 0:
        if code[i] == "{":
            depth += 1
        elif code[i] == "}":
            depth -= 1
        i += 1
    arts = ART_LIT.findall(code[m.end():i])
    if not arts:
        rep.err("B.LOOKS ohne art = \"...\" -- Aussehen-Arten nicht pruefbar")
        return 1
    def_lits = set()
    for c, _ in lua_split_lines(defs.decode("latin-1")):
        def_lits.update(_strings_of(c))
    bench = {}
    for rel, _why in plan["skipped"]:
        if not (rel.endswith(".lua") and BENCH_DEFS.match(os.path.basename(rel))):
            continue
        for c, _ in lua_split_lines(rd(src[rel]).decode("latin-1")):
            for bm in BENCH_ART.finditer(c):
                nm = bm.group(1) or bm.group(2)
                if re.match(r"^[a-z][a-z0-9]*$", nm):          # Artnamen sind klein (Ton-Namen wie NCBear_Pain zaehlen nicht)
                    bench.setdefault(nm, os.path.basename(rel))
    ig_en = plan["by_file"].get("IG_UI.json", {}).get("EN", {})
    bad = 0
    for art in arts:
        if art not in def_lits:
            bad += 1
            rep.err("B.LOOKS nennt die Art %s, aber die kopierte shared/BanditsNPCBearDefs.lua definiert sie nicht (Werkbank-Art? In NPC "
                    "Crew gaebe es dieses Aussehen nie)" % art)
        if art in bench:
            bad += 1
            rep.err("B.LOOKS nennt die Art %s, die die Werkbank-Datei %s definiert -- ein Aussehen braucht eine eigene, kopierte Art"
                    % (art, bench[art]))
        if ("IGUI_AnimalType_" + art) not in ig_en:
            bad += 1
            rep.err("B.LOOKS nennt die Art %s, aber IG_UI.json (EN) hat keinen Tiernamen IGUI_AnimalType_%s" % (art, art))
    rep.say("  B.LOOKS: %d Arten (%s); in der kopierten Defs-Datei: %d; Werkbank-Arten (nie in B.LOOKS): %s; Fehler: %d" % (
        len(arts), ", ".join(arts), sum(1 for a in arts if a in def_lits), ", ".join(sorted(bench)) or "-", bad))
    return bad


# ---------------------------------------------------------------------------------------------------------------------------------
# 7. Pruefer
# ---------------------------------------------------------------------------------------------------------------------------------
def run_tool(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=NC_LIVE)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def checkers(root, lua_rels, final, rep):
    rep.say("")
    rep.say("== Pruefer auf dem geschriebenen Stand (%s)" % root)
    bad = 0
    for rel in lua_rels:
        p = os.path.join(root, rel)
        res = []
        for tool in ("luacheck.py", "scopecheck.py", "localcount.py"):
            rc, out = run_tool([os.path.join(TOOLS, tool), p])
            if rc != 0:
                bad += 1
                rep.err("%s: %s meldet einen Fehler:\n%s" % (rel, tool, "\n".join(out.strip().splitlines()[-6:])))
                res.append(tool + " FEHLER")
            else:
                if tool == "localcount.py":
                    nums = [int(x) for x in re.findall(r"^\s*(\d+) (?:locals|declared in total)", out, re.M)]
                    if nums and max(nums) >= 180:
                        rep.err("%s: localcount %d (ab 180 aufteilen)" % (rel, max(nums)))
                    res.append("localcount ok (hoechstens %d)" % (max(nums) if nums else 0))
                else:
                    res.append(tool.replace(".py", "") + " ok")
        rep.say("  %s: %s" % (rel, ", ".join(res)))
    # DE (NPC Crew v3.14.75): NPC Crews Sprachpruefer auf den ZUSAMMENGEFUEHRTEN Texten des geschriebenen Stands (alle LANGS ueber
    # --extra; prueft UI/Sandbox/Tooltip.json: Paritaet, Platzhalter, Round-Trip, NFC, DE-Zeichen, Schrift-Matrix; IG_UI.json nicht).
    tr = os.path.join(root, "42", "media", "lua", "shared", "Translate")
    lc = [os.path.join(TOOLS, "langcheck.py")]
    for l in LANGS:
        lc += ["--extra", "%s=%s" % (l, os.path.join(tr, l))]
    rc, out = run_tool(lc)
    tail = out.strip().splitlines()
    if rc != 0:
        rep.err("langcheck.py meldet Fehler auf dem geschriebenen Stand:\n" + "\n".join(tail[-12:]))
    else:
        rep.say("  langcheck.py (%d Sprachen, geschriebener Stand): %s" % (len(LANGS), tail[-1] if tail else "?"))
    rc, out = run_tool([os.path.join(TOOLS, "luacheck_pz.py")] + [os.path.join(root, r) for r in lua_rels])
    if "luacheck_pz:" not in out:
        rep.err("luacheck_pz lief nicht:\n" + out[-400:])
        return bad
    hits, allowed = [], []
    classes = set()
    for rel in lua_rels:
        classes.update(re.findall(r"^(BanditsNPCBear\w+)\s*=\s*ISBaseTimedAction:derive", final[rel].decode("latin-1"), re.M))
    for ln in out.splitlines():
        m = re.match(r"^(.*?):(\d+): \((\w\d+)\) .*'(\w+)'", ln)
        if not m:
            continue
        key = (os.path.basename(m.group(1)), m.group(4))
        if m.group(3) == "W113" and key in PZ_ALLOWED and m.group(4) in classes:
            allowed.append("%s:%s %s" % (key[0], m.group(2), key[1]))
        else:
            hits.append(ln.strip())
    for h in hits:
        rep.err("luacheck_pz: " + h)
    rep.say("  luacheck_pz auf %d kopierten Dateien: %d Treffer, %d erlaubt (Aktionsklasse aus einer anderen kopierten Datei: %s)"
            % (len(lua_rels), len(hits), len(allowed), ", ".join(allowed) or "-"))
    return bad


# ---------------------------------------------------------------------------------------------------------------------------------
# Ablauf
# ---------------------------------------------------------------------------------------------------------------------------------
def build_plan(tgt, src, rep):
    copy_lua, copy_asset, merge, skipped, alt, sandbox = collect_source(src, rep)
    final = {}
    for rel in copy_lua + copy_asset:
        final[rel] = rd(src[rel])
    form_check(final, copy_lua, copy_asset, rep)
    packs_check(final, rep)                                    # F4 (PLAN_F4.md 17.1 Nr. 2)
    texts, tsum, by_file, text_alt = plan_texts(tgt, src, merge, rep)
    final.update(texts)
    en_sb = {}
    rel_sb = "42/media/lua/shared/Translate/EN/Sandbox.json"
    data = final.get(rel_sb)
    if data is None and os.path.isfile(os.path.join(tgt, rel_sb)):
        data = rd(os.path.join(tgt, rel_sb))
    if data:
        en_sb = json.loads(data.decode("utf-8"))
    sb, n_opt = plan_sandbox(tgt, src, sandbox, final, en_sb, rep)
    final.update(sb)
    body = ""
    if sandbox:
        body = "\n".join(rd(src[sandbox]).decode("latin-1").split("\n")[1:])
    return {"copy_lua": copy_lua, "copy_asset": copy_asset, "merge": merge, "skipped": skipped, "alt": alt, "text_alt": text_alt,
            "final": final, "texts": tsum, "by_file": by_file, "n_opt": n_opt, "sandbox_body": body}


def print_plan(plan, rep):
    rep.say("")
    rep.say("== Dateien")
    size = sum(len(plan["final"][r]) for r in plan["copy_lua"] + plan["copy_asset"])
    rep.say("kopieren: %d Lua, %d Modell/Textur/Skript/Animations-Knoten, zusammen %.1f MB" % (
        len(plan["copy_lua"]), len(plan["copy_asset"]), size / 1048576.0))
    for rel in plan["copy_lua"]:
        rep.say("  lua    %s" % rel)
    for rel in plan["copy_asset"]:
        rep.say("  datei  %s (%d KB, MD5 %s)" % (rel, len(plan["final"][rel]) // 1024, md5(plan["final"][rel])))
    for rel, why in plan["skipped"]:
        rep.say("  NICHT  %s (%s)" % (rel, why))
    for rel in plan["alt"]:
        rep.say("  ALT    %s (noch umzubenennen, B5a)" % rel)
    rep.say("")
    rep.say("== Texte")
    for s in plan["texts"]:
        rep.say("  " + s)
    rep.say("")
    rep.say("== Naehte (NAEHTE.md): keine Zeile in einer NPC-Crew-Lua-Datei. Laufzeit-Aufsaetze auf NPC Crew in OnGameBoot stehen in den "
            "kopierten Dateien (B1c: dazu ein Aufsatz auf VANILLAS Kartenklassen, Datei-Ende + OnGameStart, NAEHTE.md Zeile 18; B1d: "
            "keine neue Naht, NAEHTE.md Zeile 25; B1e: keine neue Naht, die Art ncbeargrown haengt bis B5a am grossen Modell der "
            "Test-Mod, NAEHTE.md Zeilen 15 und 26; F1/F1B: zwei Tasten auf der eigenen Mod-Optionen-Seite (keine Zeile in Vanillas "
            "keyBinding mehr), Vorfahrt vor NPC Crews 'Talk to NPC' und NC-Stationen nur lesend, layout.ini-Name und Client-Datei "
            "BanditsNPCBear.ini (tagoff/ageoff), Beacon-Basisflaeche fuer 'Frei' nur dokumentiert, Huelle um Vanillas "
            "AnimalContextMenu.showRadialMenu (ohne Kill), NAEHTE.md Zeilen 27-32; F2 = B5a: eigener Zombie-Biss-Knoten, Bandits-Aufgabe "
            "ZombieActions.BNBearSmack in OnGameBoot hinter Riegel, Schutz setIsInvincible am zahmen Baeren, neuer Server->Client-Befehl Fx, "
            "Naht 1 nur noch ncbear, Turret <-> Baer und NPC-Heiler nur dokumentiert, NAEHTE.md Zeilen 1, 9, 13, 21, 23, 33-39; Aussehen: "
            "keine neue Naht -- drei neue Arten, eine neue Lua-Datei und Modelle nur im eigenen Namensraum, Sandbox 39 -> 12, NAEHTE.md Kopf); "
            "geaendert werden nur NPC Crews Texte (zusammenfuehren) und sandbox-options.txt (anhaengen).")


def write_all(root, final, rep):
    n = 0
    for rel, data in sorted(final.items()):
        full = os.path.join(root, rel)
        if os.path.isfile(full) and rd(full) == data:
            continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        if rd(full) != data:
            rep.err("%s: nach dem Schreiben nicht gleich -- Platte pruefen" % rel)
        n += 1
    return n


def game_running():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, errors="replace").stdout
    except OSError:
        return None
    return "projectzomboid" in out.lower()


def under(path, bad):
    a, b = os.path.abspath(path).lower(), os.path.abspath(bad).lower()
    return a == b or a.startswith(b + os.sep)


def make_probe(probe_dir, staging, rep):
    probe_dir = os.path.abspath(probe_dir)
    for bad in (ZOMBOID, NC_LIVE, TEST):
        if under(probe_dir, bad):
            rep.err("Probe-Ordner liegt unter %s -- dort laedt das Spiel Kopien als Mod oder es traefe echte Dateien" % bad)
            return None, None
    if os.path.exists(probe_dir) and os.listdir(probe_dir) and not os.path.isfile(os.path.join(probe_dir, PROBE_MARK)):
        rep.err("%s ist nicht leer und keine Probe dieses Skripts (Marke %s fehlt) -- nichts geloescht, Abbruch" % (probe_dir, PROBE_MARK))
        return None, None
    for sub in ("quelle", "NPCCrew"):
        p = os.path.join(probe_dir, sub)
        if os.path.exists(p):
            shutil.rmtree(p)
    os.makedirs(probe_dir, exist_ok=True)
    with open(os.path.join(probe_dir, PROBE_MARK), "w", encoding="ascii") as f:
        f.write("Probe von baer_uebernahme.py, darf geloescht werden.\n")
    # Quelle: Kopie der Test-Mod ohne Git-Teile, darueber das Staging.
    qroot = os.path.join(probe_dir, "quelle")
    src, _sk = source_map(TEST, staging, rep)
    for rel, full in sorted(src.items()):
        if rel in GIT_ROOT_FILES:
            continue
        dst = os.path.join(qroot, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(full, dst)
        if rd(dst) != rd(full):
            rep.err("Probe-Quelle %s: Kopie nicht byte-gleich" % rel)
    # Ziel: nur die noetigen Teile von NPC Crew (Lua, Skripte, AnimSets, Sandbox, mod.info); Texturen/Modelle liest das Skript im echten Baum.
    root = os.path.join(probe_dir, "NPCCrew")
    os.makedirs(root)
    for sub in ("42/media/lua", "42/media/scripts", "common/media/AnimSets", "42/media/AnimSets"):
        s = os.path.join(NC_LIVE, sub)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(root, sub))
    for one in (SANDBOX, "42/mod.info", "mod.info"):
        s = os.path.join(NC_LIVE, one)
        if os.path.isfile(s):
            os.makedirs(os.path.dirname(os.path.join(root, one)), exist_ok=True)
            shutil.copy2(s, os.path.join(root, one))
    return qroot, root


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    rep = Report()
    probe, staging = None, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--probe", "--staging"):
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                print("%s braucht einen Ordner" % a)
                return 2
            if a == "--probe":
                probe = argv[i + 1]
            else:
                staging = os.path.abspath(argv[i + 1])
            i += 1
        elif a == "--echt":
            ARGS["echt"] = True
        elif a == "--ja-kevin-hat-es-gesagt":
            pass
        elif a == "--erneut":
            ARGS["erneut"] = True
        elif a == "--vor-b5a":
            ARGS["vor_b5a"] = True
        else:
            print("unbekannt: %s (Hilfe: -h)" % a)
            return 2
        i += 1
    echt = ARGS["echt"]
    if probe and echt:
        print("--probe und --echt zusammen geht nicht")
        return 2
    if echt and "--ja-kevin-hat-es-gesagt" not in argv:
        print("--echt schreibt in NPC Crew und verlangt ausdruecklich --ja-kevin-hat-es-gesagt (nur auf Kevins Wort).")
        return 2
    if echt and (ARGS["vor_b5a"] or staging):
        print("--echt geht nicht mit --vor-b5a oder --staging: die echte Uebernahme liest nur die Test-Mod und prueft streng.")
        return 2
    if not os.path.isdir(TEST):
        print("Test-Mod fehlt: %s" % TEST)
        return 1
    if staging:
        for bad in (NC_LIVE, TEST):
            if under(staging, bad):
                print("--staging darf nicht in %s liegen" % bad)
                return 2

    if probe:
        mode = "PROBE"
        qroot, tgt = make_probe(probe, staging, rep)
        if tgt is None:
            for e in rep.errors:
                print("FEHLER: " + e)
            return 1
        src, git_sk = source_map(qroot, None, rep)
        src_label = "%s (Kopie der Test-Mod ohne .git%s)" % (qroot, ", darueber " + staging if staging else "")
    else:
        src, git_sk = source_map(TEST, staging, rep)
        src_label = TEST + ("  +  Staging " + staging if staging else "")
        if echt:
            mode, tgt = "ECHT", NC_LIVE
            running = game_running()
            if running is None:
                rep.err("tasklist lief nicht: ob das Spiel laeuft, ist unbekannt -- Abbruch")
            elif running:
                rep.err("Project Zomboid laeuft: erst das Spiel beenden.")
        else:
            mode, tgt = "TROCKENLAUF", NC_LIVE

    rep.say("baer_uebernahme.py -- %s%s" % (mode, " --vor-b5a" if ARGS["vor_b5a"] else ""))
    rep.say("Quelle: %s" % src_label)
    rep.say("Ziel:   %s%s" % (tgt, "  (nur lesen)" if mode == "TROCKENLAUF" else ""))
    plan = build_plan(tgt, src, rep)
    plan["skipped"] = sorted(set(git_sk)) + plan["skipped"]
    print_plan(plan, rep)
    alt_report(plan["alt"], plan["text_alt"], rep)
    collisions(tgt, plan["final"], plan["copy_lua"], plan["copy_asset"], rep)
    cheat_check(plan, src, rep)
    opt_name_check(plan, rep)                     # Aussehen: Sandbox-Kuerzung (PLAN_AUSSEHEN.md 12.1 Nr. 7)
    looks_check(plan, src, rep)                   # Nachbesserung Aussehen A4: B.LOOKS nur mit echten, kopierten Arten

    if rep.errors:
        rep.say("")
        rep.say("NICHT geschrieben: %d Fehler." % len(rep.errors))
    elif mode == "TROCKENLAUF":
        rep.say("")
        rep.say("Trockenlauf: nichts geschrieben. Wuerde %d Datei(en) schreiben." % len(plan["final"]))
    else:
        written = write_all(tgt, plan["final"], rep)
        rep.say("")
        rep.say("geschrieben: %d Datei(en) nach %s" % (written, tgt))
        checkers(tgt, plan["copy_lua"], plan["final"], rep)

    rep.say("")
    for w in rep.warns:
        rep.say("WARNUNG: " + w)
    for e in rep.errors:
        rep.say("FEHLER: " + e)
    rep.say("")
    rep.say("ERGEBNIS: %s -- %d Fehler, %d Warnungen (%s). Statisch geprueft, nicht gespielt." % (
        "OK" if not rep.errors else "NICHT OK", len(rep.errors), len(rep.warns), mode))
    n_defs = sum(1 for e in rep.errors if e.startswith("noch umzubenennen (B5a): Defs "))    # B1e: ALT_DEFS
    n_alt = len(plan["alt"]) + len(plan["text_alt"]) + n_defs
    if not ARGS["vor_b5a"] and n_alt and len(rep.errors) == n_alt and all(e.startswith("noch umzubenennen (B5a)") for e in rep.errors):
        rep.say("Erwartet rot: genau die %d Altlasten aus ALT_EXPECTED und %d aus ALT_DEFS (NAEHTE.md 'Erlaubte Fundstellen des "
                "Trockenlaufs'), sonst nichts." % (n_alt - n_defs, n_defs))
    if mode == "ECHT" and not rep.errors:
        rep.say("Danach von Hand: Version + Changelog in NPC Crew, Test-Mod aus Kevins Liste UND ihre Lua leeren (zwei Mods mit denselben "
                "Pfaden), Spiel neu starten.")
    if mode == "PROBE":
        try:
            with open(os.path.join(tgt, "bericht.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(rep.lines) + "\n")
        except OSError:
            pass
    return 0 if not rep.errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
