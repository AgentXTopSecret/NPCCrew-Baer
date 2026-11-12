--
-- NPC Crew -- Baer, Kern (B1a "Junges finden und zaehmen", PLAN_ZAEHMEN.md 6.2.1 und 6.2.2).
--
-- Modul, Konstanten, Stellwerte, Sandbox, Meldungen, Text, Spielerschluessel, Zeit, Wald-Frage, Sicht des Clients und die
-- drei Wege zwischen Schreiber und Spieler (B.Ask, B.Tell, B.SendView).
-- B1c (PLAN_B1C.md 5): Spiegel-Fassung B.MARK_V, Stellwerte fuer Heilung, Laerm, Zombies, Mitfahren, Call to me, Gehen,
-- Markierung und Karte, zwei neue Sandbox-Optionen (BearRideDistance, BearCallCooldownMinutes).
-- B1d (PLAN_B1D.md 5): Stellwerte fuer Wachsen (Kurve, Stufen, Fuetter-Bonus), Werte (Stuetzwerte Leben / Ausdauer / Traglast /
-- Schaden), Faehigkeiten (Erfahrungs-Kurve, Eimer, Haken-Erfahrung), Ausdauer, Leben-Abgleich; fuenf neue Sandbox-Optionen
-- (BearGrowDays, BearDodgeMax, BearFightBonusMax, BearHealAwake, BearHealSleep). Formeln: shared/BanditsNPCBearStats.lua.
-- B1e (PLAN_B1E.md 0.1, 0.8, 3.1, 5): zwei Koerper fuer EINEN Register-Eintrag -- "cub" = Art B.CUB (Junges-Modell) und "big" = Art
-- B.BIG (grosses Modell, ab Halbstark bis 1,35). Die EINZIGE Art-Frage ist B.BodyKind (nie "bear", "bearstag", "ncbearcubalt");
-- B.NoteBd haengt bd = "big" an Meldungen, deren Text je Koerper anders ist. Stellwerte fuer den Tausch, Tempo und Abstaende je
-- Koerper, Schild-Faktor, Streichel-Haltung und die neue Markierung (OBERFLAECHE) stehen in B.CFG.
-- F1 (PLAN_F1.md 0.3, 5.1, 6): vier Modi B.MODES (follow / stay / sit / roam), Stellwerte fuer Bleiben, Sitz, Frei herumlaufen,
-- Komm her und die Rueckkehr eines Baeren ohne Koerper (C1) in B.CFG, neue Sandbox-Option BearRoamRadius (Vorgabe 12).
--
-- Laeuft ohne NPC Crew und ohne Bandits. Am Ende kopiert das Uebernahme-Skript diese Datei unveraendert nach NPC Crew.
-- Deshalb: auf Dateiebene wird kein fremdes Modul eingefangen; jeder Griff nach BanditsNPC.X passiert zur Laufzeit und
-- hinter einem Existenz-Riegel. Funktionen anderer Baer-Dateien werden nur zur Laufzeit ueber die Modul-Tabelle geholt.
--
-- "Schreiber" = der Rechner, der die Welt rechnet: im Einzelspieler das eine Programm, im Mehrspieler der Server.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- ---------------------------------------------------------------------------
-- Konstanten (Plan 6.2.1)
-- ---------------------------------------------------------------------------
B.KEY = "TrueCompanionsBears"   -- globale ModData des Registers, nur beim Schreiber
B.CMD = "BanditsNPCBear"        -- Modulname fuer sendClientCommand / sendServerCommand
B.CUB = "ncbearcub"             -- Tierart des Jungen
B.BIG = "ncbeargrown"           -- B1e: Tierart des grossen Koerpers (ab Halbstark; Artname ENDGUELTIG, shared/BanditsNPCBearDefs.lua)
B.BODY_TYPE = { cub = B.CUB, big = B.BIG }                -- B1e: Koerper -> Art
B.TYPE_BODY = { [B.CUB] = "cub", [B.BIG] = "big" }        -- B1e: Art -> Koerper (nie "bear", "bearstag", "ncbearcubalt")
B.BREED = "brown"
B.GROUP = "ncbear"
B.MARK = "tcBear"               -- Spiegel am Tier: animal:getModData().tcBear (B1c: Spiegel v2, server/BanditsNPCBearHeal.lua B.MarkOf)
B.MARK_V = 2                    -- B1c (PLAN_B1C.md 2.2): Fassung des Spiegels; fehlt mark.v, ist es ein B1a/B1b-Spiegel { id, st }
B.SP_KEY = "__sp"               -- Besitzerschluessel im Einzelspieler (nie der Charaktername)
B.ACT = "NCBearAct"             -- Anim-Variable am Tier (Knoten AnimSets/buck/idle)

-- Feste Stellwerte (Plan 3.3). Keine Sandbox; zur Laufzeit aenderbar.
B.CFG = B.CFG or {
    brainMs = 1500, idleMs = 10000, scanMs = 5000,       -- Hirn-Takt mit / ohne lebende Eintraege, Abstand zweier Suchlaeufe (Echtzeit)
    shyDist = 6, fleeDist = 12,                           -- Fluchtabstand eines scheuen Jungen / so weit laeuft es weg
    lureDist = 15, comeUnfed = 3, comeFed = 2,            -- Futter in der Hand wirkt bis / so nah kommt ein scheues / ein angefuettertes
    curiousMin = 12, curiousMax = 45, curiousStop = 9, curiousMs = 60000,   -- Neugier
    contactDist = 15,                                     -- Kontakt (haelt die Verschwinde-Uhr an), auch "entdeckt"
    homeR = 10,                                           -- Radius um die Heimat
    vanishKeep = 25,                                      -- Verschwinden nur, wenn kein Spieler naeher ist
    baitKeep = 20, baitAppear = 20, baitEdge = 8, baitApart = 10, baitExtra = 4,
    hintH = 1.0,                                          -- Hinweis "Wimmern" hoechstens je Spielstunde
    tellDist = 60,                                        -- so nah bekommt ein Spieler die Daten eines Jungen
    moveMs = 3000, tries = 8,                             -- fruehestens neuer Laufbefehl / Versuche bei der Platzsuche
    abandonH = 168, missScans = 3, missingH = 24,
    maxRecs = 64, maxBaits = 16,                          -- harte Deckel des Registers
    snackBelow = 0.05, snack = 0.5,                       -- Happen: getHungerChange() > -0.05; Faktor
    forestRate = { 0, 2, 5, 12, 30 },                     -- Prozent je Spielstunde zu Option BearCubForestRate
    feedTime = 150, petTime = 150, baitTime = 100,        -- Dauer der Zeitaktionen
    petAnim = "lamb",
    -- tagZ (B1b, PLAN_B1B.md 1.7/2.2): Anker von Zaehm-Balken UND Namensschild ueber dem Boden des Tiers (Ebenen); ersetzt barZ
    -- (0,55 war ~4,5 x zu hoch ueber dem kleinen Jungen). Stellwert: nach Kevins Blick im Spiel nachstellen.
    tagZ = 0.18, hudDist = 20, hudMax = 6, menuFoods = 12,
    -- Zusatz des Kerns (nicht in Plan 3.3, gleiche Tabelle, damit alles Stellbare an einem Ort liegt):
    reach = 3,                                            -- Fuettern/Streicheln: Abstand kleiner als (Vanilla ISPetAnimal.lua:6)
    baitReach = 3,                                        -- Koeder auslegen: Spieler hoechstens so weit von der Kachel
    baitRing = 2,                                         -- Koeder-Junges erscheint in diesem Umkreis um den Platz
    mateDist = 70,                                        -- Finder/Besitzer zaehlt als "da" bis hierhin
    hintDist = 80,                                        -- Wimmer-Hinweis nur, wenn der Finder so nah ist
    stillEps = 0.3,                                       -- Spieler "steht": weniger als so viel je Takt bewegt
    viewMax = 16,                                         -- hoechstens so viele Junge in einer Sicht
    loadRing = 12,                                        -- "Gegend geladen": Kachel und vier Punkte in diesem Abstand
    orphanMs = 10000,                                     -- verwaiste Bewegungssperre fruehestens so oft loesen
    maxDtH = 1.0,                                         -- Deckel fuer einen Schritt des Langsam-Takts (Spielstunden)
    fedMissH = 1.0,                                       -- angefuettertes Junges: so lange fehlen (Spielstunden), bevor es "verloren" ist
    missScanMul = 6,                                      -- vermisstes zahmes Junges: Suchlauf nur je scanMs x so viel
    -- B1b Folgen / Bleiben (PLAN_B1B.md 1.2, 1.4, 1.7). Abstaende in Kacheln, Zeiten in Echtzeit-ms.
    followNear = 3, followStart = 4.5, followGap = 2,     -- halten bis / losrennen ab (Haltespanne) / Ziel so weit vor dem Besitzer
    followLead = 1.5,                                     -- Vorhalt: so weit hoechstens rechnet das Ziel den Weg des Besitzers voraus
    followMoveMs = 1200, followRepath = 2.5, followRenewMs = 4000,   -- fruehester neuer Laufbefehl / Ziel-Wanderung / Auffrischen
    followStuckMs = 15000, followStuckGain = 1.0, followRetryMs = 10000,   -- "steckt fest" nach / Mindest-Fortschritt / ein Versuch je
    -- Bleiben-Radius des gezaehmten Jungen (homeR gilt weiter fuer "fed"). 12 statt 8 (Nachbesserung B1b B7): die Engine wuerfelt
    -- beim Wandern bis +-8 je Achse um das Tier (Jar BaseAnimalBehavior, forschung_b1b.md:120) -- mit 8 rannte es oft grundlos heim.
    stayR = 12,
    -- B1b Name, Bitten, Waisen (PLAN_B1B.md 1.7, 3.3, 4)
    nameMax = 24,                                         -- hoechstens so viele Zeichen im Namen
    askMs = 500,                                          -- Bitten "Mode"/"Rename" eines Spielers hoechstens so oft
    orphanScanMs = 120000, orphanAgeMs = 30000, orphanMax = 16,   -- eigener Waisen-Suchlauf je / Mindestalter einer Waise / Deckel
    -- B1c (PLAN_B1C.md 5.2). Abstaende in Kacheln, Zeiten in Echtzeit-ms, Tempo in Kacheln/s.
    healWindowMs = 120000, healScanMs = 15000,            -- Heil-Fenster nach InitRegistry / Suchlauf darin je
    calmMax = 8, calmMs = 2500, calmGap = 1.5,            -- Laerm-Wache: Deckel / Ruhefrist (keine Sperre) / Ersatzweg-Laenge
    noiseStressJump = 0.02, noiseAnswerMax = 4, noiseAnswerWinMs = 2000,   -- Stress-Sprung je Bild = Laerm / Antworten je Fenster
    ownSlackMs = 1500, ownMaxMs = 15000,                  -- eigener Befehl gilt Wegzeit + so viel, hoechstens so lange
    ownAway = 3, ownAwayQuietMs = 5000,                   -- Nachbesserung B5: so viel weiter vom eigenen Ziel = Flucht / danach Ruhe
    followFleeGrow = 2.0,                                 -- Rueckfall: Abstand zum Besitzer wuchs je Takt so viel -> sofort neu
    walkDist = 3, walkSpeed = 0.52, runSpeed = 2.47,      -- gehen bis Reststrecke / bis Besitzer-Tempo / Tempo fuer die Wegzeit
    zedSense = 12, zedHide = 6, zedSafe = 9, zedCalmMs = 3000,     -- Zombie: Suche / Gefahr ab / sicher ab / so lange sicher bis Ende
    zedFlee = 10, hideGap = 1.5, hideNear = 1.0, hideOwnerMax = 10,  -- Fluchtweite / Versteck hinter dem Besitzer / angekommen / Besitzer
    zedScanMax = 1500, zedTickMs = 750, zedKeepMs = 3000,  -- Zombies je Takt / Hirn-Takt bei Gefahr / letzte Sichtung gilt so lange
    guardMoveMs = 800, guardRepath = 1.5, guardRenewMs = 3000,     -- Wache: fruehester neuer Befehl / Ziel-Wanderung / Auffrischen
    rideOffMsSP = 1000, rideOffMsMP = 3000, rideSpeedMax = 4,      -- Aussteigen nach (SP / MP) / nur langsamer als
    rideRing = 3, rideLostMs = 5000, rideFailLog = 20,    -- Platz-Ringe / Besitzer tot so lange / Fehlerzeile ab Versuch
    callRing = 3,                                         -- Platz-Ringe fuer "Call to me"
    viewMoveTiles = 3, viewMoveMs = 5000,                 -- Lage in der Sicht nachschicken ab / hoechstens je
    markerMs = 400, markerAfterMs = 60000, markerDur = 1800, markerShift = 100,   -- Markierung (liest die OBERFLAECHE)
    mapMiniPx = 14, mapWorldMin = 18, mapWorldMax = 28, mapListMs = 500,          -- Karte (liest die OBERFLAECHE)
    -- B1d (PLAN_B1D.md 5.2). Wachstum g = 0..1 (Register), innere Groesse s, gezeigte Groesse sz. Tabellen nicht zur Laufzeit stellbar.
    growCurve = { { 0, 0.35 }, { 0.15, 0.75 }, { 0.45, 1.0 }, { 1.0, 1.35 } },   -- Kurve (x = g, Groesse) durch Kevins Tabelle
    stageAt = { 0.75, 1.0, 1.35 },                        -- Schwellen half / strong / adult (innere Groesse)
    -- B1e (PLAN_B1E.md 5): bodySwap true = Modellwechsel an (Kevin 11.11.2026 "Ab Tag 15 (halbstark)"); false = Not-Aus (B.BodyWant
    -- immer "cub": ein grosser Koerper wird wieder Junges). cubMaxSize = groesste gezeigte Groesse mit dem Junges-Modell UND Schwelle hin.
    cubMaxSize = 0.75, bodySwap = true,
    -- swapSize = gezeigte Groesse des grossen Koerpers beim Tausch; MUSS gleich minSize der Art B.BIG sein
    -- (shared/BanditsNPCBearDefs.lua). Gemessen: bei 0,72 ist das grosse Modell so gross wie das Junge bei 0,75 (Laenge +0,6 %,
    -- Oberkante +1,9 %, _arbeit/baer_zaehmen/mess_b1e/ausgabe.txt:60). swapBackSize = innere Groesse, unter der er zurueck wechselt.
    swapSize = 0.72, swapBackSize = 0.70,
    swapMinMs = 60000, swapRetryMs = 10000, swapFailLog = 6, swapRing = 2,   -- Abklingzeit / neuer Versuch / Fehlerzeile ab / Ringe
    swapFaceDist = 30,                                    -- neuer Koerper schaut zum Besitzer, wenn naeher (0 = aus)
    busyMs = 20000,                                       -- Fuettern/Streicheln sperren den Tausch hoechstens so lange
    swapMoveMaxMs = 10000,                                -- Nachbesserung B1e B2: Rennbefehl sperrt den Tausch hoechstens so lange
    callFreshMs = 2000,                                   -- Nachbesserung B1e B1: "Call to me" wartet auf einen eben erzeugten Koerper
    -- Tempo des grossen Koerpers (Kacheln/s; Clip-Weg / Dauer x MotionScale 1,6, forschung_b1e.md 4.4) und Abstand-Zuschlag mit der
    -- Koerperlaenge: max(0, (bodyLenBig x sz x tilesPerE - followRefLen) / 2), followRefLen = Laenge des Jungen bei 0,75 (Kacheln)
    walkSpeedBig = 0.67, runSpeedBig = 3.17,
    bodyLenBig = 1.0448, tilesPerE = 1.5, followRefLen = 1.12,
    tagBigK = 1.06,                                       -- Schild-Hoehe gross / Junges bei gleicher Groesse (OBERFLAECHE liest)
    petAnimBig = "cow",                                   -- Streichel-Haltung am grossen Koerper (Vanilla petanimal/petcow.xml)
    markerAngleAdd = 135, markerCloseTiles = 6.6,         -- Markierung: Pfeil-Ausrichtung / ab hier kein Pfeil (OBERFLAECHE liest)
    markerR = 1.0, markerG = 0.52, markerB = 0.09,        -- Markierung: Kreisfarbe (OBERFLAECHE liest)
    sizeEps = 0.002, tagBase = 0.35,                      -- Groessen-Probe ab Abweichung / Bezug des Schild-Ankers (OBERFLAECHE)
    growCommitH = 1.0,                                    -- Wachstum festschreiben hoechstens je (Spielstunden)
    feedGrowFav = 3, feedGrowOk = 2, feedGrowSnack = 1,   -- Fuetter-Bonus: Spielstunden Wachstum je Fuetterung (Klasse)
    feedGrowDay = 2, feedGrowMax = 0.10,                  -- hoechstens so viele Gutschriften je Spieltag / Summe als Anteil von g
    statAt = { 0.35, 0.75, 1.35 },                        -- Stuetzpunkte der Werte (innere Groesse)
    hpAt = { 40, 150, 400 }, staAt = { 50, 100, 160 },    -- Leben max (Punkte) / Ausdauer max an den Stuetzpunkten
    carryAt = { 10, 40, 100 }, dmgAt = { 0, 0.35, 1.0 },  -- Traglast (Kevin) / Schaden-Faktor (1,0 = heutiger Erwachsener)
    vitPerLv = 0.05, conPerLv = 0.05, dodgeBase = 5,      -- Leben- / Ausdauer-Bonus je Stufe / Ausweichen auf Stufe 0 (%)
    fishBase = 10, fishMax = 60, noseBase = 12, noseStep = 1.5,   -- Fang-Chance % / Warnweite Kacheln
    xpNeed = { 100, 116, 135, 156, 181, 210, 244, 283, 328, 380 },   -- Erfahrung je Stufe (x 1,16, Summe 2133)
    xpPerMin = 6, xpBucketMin = 3,                        -- Echtzeit-Deckel je Faehigkeit und Minute / so viele Minuten ansparen
    xpHitTaken = 10, xpHitDealt = 5, xpFishTry = 2, xpFishCatch = 10, xpSniff = 5,   -- Erfahrung je Ereignis (Haken)
    conTilesPerXp = 5, conBreathXp = 5, conBreathMs = 60000, conStepMax = 8,   -- Kondition: Kacheln je XP / ausser Puste / je / Weg-Deckel
    conStepMul = 4,                                       -- Sprung erst ab Weg > conStepMul x runSpeed x Taktdauer (Nachbesserung B1d B4)
    staRunCost = 0.4, staRegen = 2, staViewStep = 10,     -- Ausdauer: Punkte je Kachel Rennen / Punkte je s Erholung / Sicht ab
    hpEps = 0.005, hpCommit = 0.02,                       -- Leben: Abgleich-Schwelle (Anteil) / sofort festschreiben ab Verlust
    hpLossEps = 0.0001,                                   -- Leben: jeder Verlust darueber ist Schaden (Gleitkomma-Rest; Nachbesserung B1d B3)
    -- F1 (PLAN_F1.md 6.1). Abstaende in Kacheln (Tier-Mitte zu Kachel-Mitte der Heimat), Zeiten in Echtzeit-ms.
    stayNear = 1.5,                                       -- "an seiner Stelle" bis (Sitz: einmal nachruecken, wenn weiter weg)
    stayBack = 3,                                         -- Bleiben/Sitz: weiter weg -> zurueck
    backRunDist = 8,                                      -- zurueck gehend bis, sonst rennend
    sitSettleMs = 800,                                    -- so lange ruhig an der Stelle, dann "sitzt"
    standMs = 2300,                                       -- Aufstehen 1,3 s + 1 s Frist (Clip "StandUp", Animset buck/idle)
    roamMinStep = 3,                                      -- Frei: neues Ziel mindestens so weit vom Tier
    roamPauseMin = 8000, roamPauseMax = 20000,            -- Frei: Pause zwischen zwei Wegen (ms, Zufall)
    comeNear = 3, comeMaxMs = 30000,                      -- Komm her: angekommen bis / aufgeben nach
    reviveScans = 2, reviveFailLog = 3,                   -- C1: Wartefrist in Vermissten-Suchlaeufen / Fehlerzeile ab Versuch
    -- Nachbesserung F1 B1: C1 erst nach so viel Echtzeit in geladener Gegend mit Besitzer (seit dem ersten passenden Suchlauf) / eine
    -- groessere Luecke zwischen zwei passenden Suchlaeufen (Gegend entladen, Spiel angehalten) beginnt die Frist neu
    reviveMs = 60000, reviveGapMs = 50000,
}

-- F1 (PLAN_F1.md 0.3, 6.1): die vier Modi eines gezaehmten Baeren. Jeder andere Wert (auch nil) gilt als "stay" (B.ModeOf).
B.MODES = B.MODES or { follow = true, stay = true, sit = true, roam = true }

-- Sandbox-Optionen BanditsNPC.<Name> (Plan 3.1): Vorgabe und Bereich. Die Datei sandbox-options.txt nennt dieselben Zahlen.
B.OPTS = B.OPTS or {
    BearCubsEnabled = { def = true },
    BearCubForestRate = { def = 3, min = 1, max = 5 },
    BearCubMinDistance = { def = 30, min = 15, max = 60 },
    BearCubMaxDistance = { def = 50, min = 20, max = 65 },
    BearCubWorldCap = { def = 8, min = 1, max = 32 },
    BearMaxPerPlayer = { def = 1, min = 1, max = 4 },
    BearBaitEnabled = { def = true },
    BearBaitNights = { def = 3, min = 1, max = 7 },
    BearBaitFirstChance = { def = 40, min = 0, max = 100 },
    -- Kevin 11.11.2026 (begleiter/ENTSCHEIDUNGEN.md, Zaehm-Dauer): Abklingzeiten bleiben, weniger Punkte je Handlung -> ~12 Spielstunden
    BearTameFeedPoints = { def = 4, min = 1, max = 100 },
    BearTamePetPoints = { def = 3, min = 0, max = 100 },
    BearTameMixBonus = { def = 50, min = 0, max = 200 },
    BearTameFavoriteBonus = { def = 50, min = 0, max = 200 },
    BearTameMinFeedings = { def = 3, min = 0, max = 10 },
    BearFeedCooldownMinutes = { def = 120, min = 0, max = 2880 },
    BearPetCooldownMinutes = { def = 60, min = 0, max = 2880 },
    BearCubVanishHours = { def = 36, min = 0, max = 240 },
    BearDeathLockDays = { def = 7, min = 0, max = 60 },
    BearFollowMaxDistance = { def = 40, min = 10, max = 60 },   -- B1b: weiter weg -> ein folgendes Junges wartet (Max unter 76 geladenen Kacheln)
    -- B1c (PLAN_B1C.md 5.1, Kevin 11.11.2026: 15 Kacheln, 5 Minuten Echtzeit)
    BearRideDistance = { def = 15, min = 3, max = 40 },          -- so weit darf ein folgendes Junges beim Einsteigen weg sein
    BearCallCooldownMinutes = { def = 5, min = 0, max = 60 },    -- Echtzeit-Minuten zwischen zwei "Call to me" am selben Jungen
    -- B1d (PLAN_B1D.md 5.1; Kevin 11.11.2026: 100 Tage, Ausweichen 40 %, Kaempfen +70 %, Heilen wach ~1 %, im Schlaf ~15 %)
    BearGrowDays = { def = 100, min = 10, max = 365 },           -- Spieltage vom Zaehmen bis ausgewachsen
    BearDodgeMax = { def = 40, min = 5, max = 80 },              -- Ausweichen in Prozent auf Agilitaet 10
    BearFightBonusMax = { def = 70, min = 0, max = 200 },        -- Mehr-Schaden in Prozent auf Kaempfen 10
    BearHealAwake = { def = 1.0, min = 0.0, max = 10.0 },
    BearHealSleep = { def = 15.0, min = 0.0, max = 100.0 },
    -- F1 (PLAN_F1.md 6.2): so weit darf ein Baer auf "Frei herumlaufen" von der Stelle des Befehls weg (Kevin ENT:284 "Radius 12")
    BearRoamRadius = { def = 12, min = 4, max = 30 },
    BearLog = { def = false },
}

-- Waldzonen (Vanilla shared/Foraging/forageZones.lua:3,27,72,79,91,98,110,122,129,140).
B.FOREST = B.FOREST or {
    Forest = true, DeepForest = true, PHForest = true, PHMixForest = true, PRForest = true,
    FarmMixForest = true, FarmForest = true, BirchForest = true, BirchMixForest = true, OrganicForest = true,
}

-- ---------------------------------------------------------------------------
-- Modus. Beide Negationen ausgeschrieben (Vanilla shared/TimedActions/ISEatFoodAction.lua:136).
-- B.IsWriter gilt NUR fuer Weltschreiben, nie fuer Rechte.
-- ---------------------------------------------------------------------------
function B.IsSP()
    return not isClient() and not isServer()
end

function B.IsWriter()
    return not isClient()
end

-- ---------------------------------------------------------------------------
-- Sandbox lesen (Plan 3.1): nil-Rueckfall auf die Vorgabe, Typ pruefen, auf den Bereich klemmen.
-- Mit NPC Crew ueber BanditsNPC.Opt (dessen Weltregel-Speicher geht vor), sonst SandboxVars.BanditsNPC
-- (Form Bandits client/BanditUpdate.lua:495 SandboxVars.Bandits...). Im Mehrspieler gelten die Werte des Servers.
-- ---------------------------------------------------------------------------
function B.Opt(name)
    local o = B.OPTS[name]
    if not o then return nil end
    local v = nil
    local crewOpt = BanditsNPC.Opt
    if crewOpt then
        v = crewOpt(name, o.def)
    else
        local sv = SandboxVars and SandboxVars.BanditsNPC
        if sv then v = sv[name] end
    end
    if type(o.def) == "boolean" then
        if type(v) ~= "boolean" then return o.def end
        return v
    end
    if type(v) ~= "number" then return o.def end
    if o.min ~= nil and v < o.min then v = o.min end
    if o.max ~= nil and v > o.max then v = o.max end
    return v
end

-- ---------------------------------------------------------------------------
-- Meldungen (Form NCTurretTest shared/BanditsNPCTurret.lua:90-133)
-- ---------------------------------------------------------------------------
B.LogOn = B.LogOn or false

-- Diagnose erlaubt? Eigener Schalter, Sandbox-Option BearLog oder NPC Crews Crew logging ab Stufe 2 (BanditsNPC.DIAG).
function B.LogActive()
    if B.LogOn == true or BanditsNPC.DIAG == true then return true end
    return B.Opt("BearLog") == true
end

-- Diagnose-Zeile: nie nackt, immer hinter dem Schalter.
function B.Log(msg)
    if not B.LogActive() then return end
    print("[TC-BEAR] " .. tostring(msg))
end

-- Fehler laufen immer.
function B.Err(msg)
    local crewErr = BanditsNPC.Err
    if crewErr then
        crewErr("[TC-BEAR] *** " .. tostring(msg))
    else
        print("[TC-BEAR] *** " .. tostring(msg))
    end
end

-- Fehler an einer Stelle, die wiederholt laeuft: je Schluessel hoechstens einmal je ms. Deckel 64 Schluessel.
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
B._errAt = B._errAt or {}
B._errN = B._errN or 0
function B.ErrEvery(key, ms, msg)
    local now = getTimestampMs()
    local last = B._errAt[key]
    if last and now - last >= 0 and now - last < ms then return end
    if last == nil then
        B._errN = B._errN + 1
        if B._errN > 64 then
            B._errAt = {}
            B._errN = 1
        end
    end
    B._errAt[key] = now
    B.Err(msg)
end

-- ---------------------------------------------------------------------------
-- Kleine reine Helfer
-- ---------------------------------------------------------------------------
function B.DistXY(x1, y1, x2, y2)
    local dx, dy = x2 - x1, y2 - y1
    return math.sqrt(dx * dx + dy * dy)
end

-- Eine Nachkommastelle (Balken).
function B.Round1(v)
    return math.floor(v * 10 + 0.5) / 10
end

-- Zahl als Text ohne ".0" (Java formatiert 21.0 sonst als "21.0").
local function argText(a)
    if a == nil then return "" end
    if type(a) == "number" then
        if a == math.floor(a) then return string.format("%d", a) end
        return tostring(a)
    end
    return tostring(a)
end

-- Ersatztext fuellen: %1..%3 einsetzen, %% wird %. Zeichenweise, ohne Muster (Kahlua ist kein echtes Lua 5.1).
local function fill(text, a1, a2, a3)
    local out = {}
    local n = string.len(text)
    local i = 1
    while i <= n do
        local ch = string.sub(text, i, i)
        if ch == "%" and i < n then
            local nx = string.sub(text, i + 1, i + 1)
            if nx == "%" then
                out[#out + 1] = "%"
                i = i + 2
            elseif nx == "1" then
                out[#out + 1] = a1
                i = i + 2
            elseif nx == "2" then
                out[#out + 1] = a2
                i = i + 2
            elseif nx == "3" then
                out[#out + 1] = a3
                i = i + 2
            else
                out[#out + 1] = ch
                i = i + 1
            end
        else
            out[#out + 1] = ch
            i = i + 1
        end
    end
    return table.concat(out)
end

-- Text mit bis zu drei Einsetzungen. Fehlt der Schluessel, der englische Ersatztext (Form BanditsNPC.T).
-- getTextOrNull(key): Vanilla shared/TimedActions/ISReadABook.lua:220. getText(key, a, b): Vanilla
-- shared/Definitions/animal/ButcheringUtil.lua:394 (zwei Einsetzungen), client/Vehicles/ISUI/ISVehicleMenu.lua:403 (vier).
-- Fix 2 (Kevins Test 10.11.2026, console.txt: ~900 x "Translator.reportMissingArgumentsFromPastAbuse ... Missing arguments for
-- UI_BN_Bear_Hud_Taming" usw. in wenigen Minuten): getTextOrNull(key) OHNE Argumente formatiert eine Vorlage mit %1 ohne Werte und
-- wirft dabei jedes Mal eine Ausnahme (Warnung + Stacktrace). Die Existenzfrage deshalb nur EINMAL je Schluessel und Sitzung stellen
-- (Zwischenspeicher tHas, gedeckelt durch die feste Zahl unserer Schluessel); formatiert wird wie bisher mit getText(key, Werte).
-- Restwarnung: hoechstens eine je Schluessel mit Platzhalter und Sitzung (wie NPC Crew vor v3.11.19, shared/BanditsNPC.lua:2853-2856).
local tHas = {}
function B.T(key, fallback, a1, a2, a3)
    local s1, s2, s3 = argText(a1), argText(a2), argText(a3)
    if type(key) ~= "string" then
        return fill(tostring(fallback or ""), s1, s2, s3)
    end
    local has = tHas[key]
    if has == nil then
        has = getTextOrNull(key) ~= nil
        tHas[key] = has
    end
    if not has then
        return fill(tostring(fallback or key), s1, s2, s3)
    end
    if a3 ~= nil then return getText(key, s1, s2, s3) end
    if a2 ~= nil then return getText(key, s1, s2) end
    if a1 ~= nil then return getText(key, s1) end
    return getText(key)
end

-- Spielerschluessel (Plan 4.1): im Mehrspieler der Kontoname, im Einzelspieler ein fester Text.
-- getUsername: Vanilla shared/Traps/TrapSystem.lua:45 (so merkt Vanilla den Fallensteller).
-- Ein Mehrspieler-Konto, das woertlich wie der Einzelspieler-Schluessel heisst, bekommt keinen Schluessel (Nachbesserung B1b B8):
-- sonst waere es Besitzer aller Jungen eines frueheren Einzelspieler-Stands. Seine Bitten verfallen, es zaehlt nicht als Spieler.
function B.PlayerKey(player)
    if not player then return nil end
    if isClient() or isServer() then
        local name = player:getUsername()
        if name == B.SP_KEY then return nil end
        return name
    end
    return B.SP_KEY
end

-- Weltstunden. Vanilla server/Traps/STrapSystem.lua:77.
function B.Now()
    return getGameTime():getWorldAgeHours()
end

-- Restzeit fuer die Anzeige: unter 1 h Minuten (aufgerundet auf 5), sonst Stunden (aufgerundet).
function B.WaitParts(hours)
    local h = tonumber(hours) or 0
    if h <= 0 then return 0, "UI_BN_Bear_Time_Minutes" end
    if h < 1 then
        local m = math.ceil(h * 12 - 0.000001) * 5
        if m < 5 then m = 5 end
        if m < 60 then return m, "UI_BN_Bear_Time_Minutes" end
        return 1, "UI_BN_Bear_Time_Hours"
    end
    return math.ceil(h - 0.000001), "UI_BN_Bear_Time_Hours"
end

-- Himmelsrichtung eines Versatzes. Welt-Achsen: -y = Norden, +x = Osten. 0.41421356 = tan(22,5 Grad).
function B.DirOf(dx, dy)
    local ax, ay = math.abs(dx), math.abs(dy)
    if ax == 0 and ay == 0 then return "N" end
    local ns = "S"
    if dy < 0 then ns = "N" end
    local ew = "W"
    if dx > 0 then ew = "E" end
    if ax <= ay * 0.41421356 then return ns end
    if ay <= ax * 0.41421356 then return ew end
    return ns .. ew
end

-- ---------------------------------------------------------------------------
-- Wald (Plan 6.2.2). Auch der Client darf fragen (Vorpruefung im Koeder-Menue).
-- getZonesAt / zone:getType(): Vanilla shared/Traps/TrapSystem.lua:12-16 (shared: Einzelspieler, Server, Client).
-- ---------------------------------------------------------------------------
function B.IsForestAt(x, y, z)
    local zones = getWorld():getMetaGrid():getZonesAt(math.floor(x), math.floor(y), math.floor(z or 0))
    if not zones then return false end
    for i = 0, zones:size() - 1 do
        local zone = zones:get(i)
        local kind = zone and zone:getType()
        if kind and B.FOREST[kind] then return true end
    end
    return false
end

-- 0.7071 = cos(45 Grad): die acht Richtungen eines Rings.
local RING = {
    { 1, 0 }, { 0.7071, 0.7071 }, { 0, 1 }, { -0.7071, 0.7071 },
    { -1, 0 }, { -0.7071, -0.7071 }, { 0, -1 }, { 0.7071, -0.7071 },
}

-- Wald auf der Kachel oder in der Naehe: die Kachel, acht Punkte im Abstand r und (ab r > 4) acht im halben Abstand,
-- damit ein schmaler Waldstreifen zwischen Kachel und Ring nicht durchfaellt. Hoechstens 17 Zonen-Fragen, nur auf Klick.
function B.NearForest(x, y, z, r)
    if B.IsForestAt(x, y, z) then return true end
    r = tonumber(r) or 0
    if r <= 0 then return false end
    for i = 1, 8 do
        local d = RING[i]
        if B.IsForestAt(x + d[1] * r, y + d[2] * r, z) then return true end
    end
    if r > 4 then
        local h = r / 2
        for i = 1, 8 do
            local d = RING[i]
            if B.IsForestAt(x + d[1] * h, y + d[2] * h, z) then return true end
        end
    end
    return false
end

-- ---------------------------------------------------------------------------
-- Sicht des Clients (Plan 6.2.5). Der Schreiber schickt jedem Spieler nur SEINE Sicht; im Einzelspieler dieselbe Tabelle
-- direkt. B.View und seine Untertabellen cubs / byOid / me bleiben dieselben Tabellen (an Ort und Stelle gefuellt).
-- ---------------------------------------------------------------------------
B.View = B.View or { ready = false, me = {}, cubs = {}, byOid = {}, bait = nil }

-- Tabelle leeren, ohne waehrend des Durchlaufs zu loeschen.
local function wipe(t)
    local keys = {}
    for k, _ in pairs(t) do keys[#keys + 1] = k end
    for i = 1, #keys do t[keys[i]] = nil end
end

local function copyFlat(src, dst)
    for k, v in pairs(src) do
        local tv = type(v)
        if tv == "number" or tv == "string" or tv == "boolean" then dst[k] = v end
    end
    return dst
end

function B.ApplySync(payload)
    if type(payload) ~= "table" then return end
    local v = B.View
    if type(v.me) ~= "table" then v.me = {} end
    if type(v.cubs) ~= "table" then v.cubs = {} end
    if type(v.byOid) ~= "table" then v.byOid = {} end
    wipe(v.me)
    wipe(v.cubs)
    wipe(v.byOid)
    if type(payload.me) == "table" then copyFlat(payload.me, v.me) end
    if type(payload.cubs) == "table" then
        for _, c in pairs(payload.cubs) do
            if type(c) == "table" and c.id ~= nil then
                local e = copyFlat(c, {})
                v.cubs[e.id] = e
                local oid = tonumber(e.oid)
                if oid and oid >= 0 then v.byOid[oid] = e.id end
            end
        end
    end
    if type(payload.bait) == "table" and payload.bait.id ~= nil then
        v.bait = copyFlat(payload.bait, {})
    else
        v.bait = nil
    end
    v.ready = true
    local onView = B.OnView
    if onView then onView() end
end

-- B1e (PLAN_B1E.md 3.1, 6.2.1): welcher unserer Koerper ist dieses Tier? "cub" (Art B.CUB) / "big" (Art B.BIG) / nil (jedes andere
-- Tier, auch "bear", "bearstag", "ncbearcubalt"). Die EINZIGE Art-Frage des Baeren-Codes; Schreiber und Client.
-- animal:getAnimalType(): Vanilla client/ISUI/Animal/ISAnimalUI.lua:65 (Client), shared/Definitions/animal/ButcheringUtil.lua:13 (shared).
function B.BodyKind(animal)
    if animal == nil then return nil end
    local kind = animal:getAnimalType()
    if kind == nil then return nil end
    return B.TYPE_BODY[kind]
end

-- B1e (PLAN_B1E.md 0.10, 6.4): Meldung eines Eintrags mit grossem Koerper bekommt bd = "big" (der Client waehlt dann den
-- Big-Text). Sonst unveraendert. Nur Tabellen-Lesen.
function B.NoteBd(note, rec)
    if type(note) == "table" and type(rec) == "table" and rec.body == "big" then note.bd = "big" end
    return note
end

-- Tier -> Sicht-Eintrag (Plan 5.6): zuerst der Spiegel am Tier (im Einzelspieler immer da), sonst die OnlineID.
-- Erst die Art fragen (B1e: B.BodyKind, beide Koerper), dann getModData (legt sonst an jedem fremden Tier eine Tabelle an).
-- getModData am Tier: client/ISUI/ISInventoryPaneContextMenu.lua:4127. getOnlineID am Tier: client/ISUI/Animal/ISAnimalContextMenu.lua:432.
function B.ViewOf(animal)
    if not animal then return nil end
    if not B.BodyKind(animal) then return nil end
    local v = B.View
    local md = animal:getModData()
    local mark = md and md[B.MARK]
    if type(mark) == "table" and mark.id ~= nil then
        local e = v.cubs[mark.id]
        if e then return e end
    end
    local oid = animal:getOnlineID()
    if oid ~= nil then
        local id = v.byOid[oid]
        if id ~= nil then return v.cubs[id] end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Wege zwischen Spieler und Schreiber (Plan 5, 6.2.6)
-- ---------------------------------------------------------------------------

-- Spieler -> Schreiber. Mehrspieler-Client: sendClientCommand(player, modul, befehl, args), Vanilla
-- client/DebugUIs/DebugContextMenu.lua:956 (nur LoginOnServer noetig). Einzelspieler: B.Handle direkt
-- (server/BanditsNPCBearServer.lua). Der Schreiber glaubt aus einer Bitte nichts ausser der Benennung.
function B.Ask(player, command, args)
    if type(args) ~= "table" then args = {} end
    if isClient() then
        sendClientCommand(player, B.CMD, command, args)
        return
    end
    if isServer() then return end
    local handle = B.Handle
    if handle then handle(player, command, args) end
end

-- Schreiber -> Spieler, eine Meldung { k, t, v, tone } (Plan 6.2.6). Server: sendServerCommand(player, modul, befehl, args),
-- Vanilla server/BuildingObjects/ISBuildUtil.lua:291. Einzelspieler: B.ShowNote direkt (sendServerCommand tut dort nichts).
-- Ruft nur der Kern.
function B.Tell(player, note)
    if not player or type(note) ~= "table" then return end
    if isServer() then
        sendServerCommand(player, B.CMD, "Note", note)
        return
    end
    if isClient() then return end
    local show = B.ShowNote
    if show then show(player, note) end
end

-- Schreiber -> Spieler, die Sicht (Plan 6.2.5). Ruft nur der Kern.
function B.SendView(player, payload)
    if not player or type(payload) ~= "table" then return end
    if isServer() then
        sendServerCommand(player, B.CMD, "Sync", payload)
        return
    end
    if isClient() then return end
    B.ApplySync(payload)
end
