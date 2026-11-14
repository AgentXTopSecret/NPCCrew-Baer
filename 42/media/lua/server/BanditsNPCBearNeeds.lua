if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Beduerfnisse und Vertrauen beim Schreiber (F3, PLAN_F3.md 2-5, 7; Kevins Antworten vom 13.11.2026,
-- _arbeit/baer_zaehmen/f3/KEVIN_ANTWORTEN.md -- sie gehen vor dem Plan). K1 (Korrektur-Lauf nach F4, PLAN_K1.md 2, 6, 8; Kevins Worte in
-- baer/begleiter/ENTSCHEIDUNGEN.md ab 13.11. ~21:40 gehen vor): Vertrauen -100..+100, Gewinn / Verlust nach Kevins Regel vom 14.11. ~00:00,
-- Hunger / Durst nach Groesse, Einfrieren.
--
-- Die Wahrheit steht im Register-Eintrag (nur gezaehmt/vermisst, Koerper-Tausch-fest): nH (Hunger), nT (Durst), nF (Muedigkeit) -- je
-- 0 = gut .. 100 = am Ende --, tr (Vertrauen -100..+100, Start 0), trV (Fassung der Vertrauens-Skala: 2 = K1; fehlt sie, ist tr ein alter Wert
-- 0..100 und wird EINMAL umgerechnet: neu = (alt - 50) x 2), nDay (laufender Spieltag: d Tag, h / t Hoechst-Hunger / -Durst, s Schlafstunden,
-- a Aufschrecken, c gezaehlte Stunden und die sechs Tages-Marken 0/1: gp gestreichelt, gf satt gefuettert, gd satt getraenkt -- je +0,5 --,
-- lh Hunger 90, lt Durst 90 -- je -5 --, lw Leben 1 % -- -10), slpAt (Weltstunde des Einschlafens aus Muedigkeit: mit dieser Marke schlaeft
-- er nach einem Laden und nach dem Fuettern / Traenken weiter, solange die Muedigkeit ueber tirWake liegt -- server/BanditsNPCBearSleep.lua).
-- Der alte Verlauf trD (Tagesabschluss) entfaellt mit K1 und wird beim Klemmen geloescht.
-- Die Engine-Werte HUNGER / THIRST des Tiers bleiben unbenutzt (FORSCHUNG_F3.md 0.4). Formeln: shared/BanditsNPCBearNeedRules.lua.
--
-- Gezaehlt wird im Langsam-Takt (B.NeedsSlow, eigene Schleife NACH B.GrowSlow in server/BanditsNPCBearServer.lua): nur gezaehmt, Besitzer
-- im Spiel, und nur mit Koerper in der Welt oder mitfahrend -- ein entladener Baer ist eingefroren (er verhungert nie, waehrend du weg
-- bist). K1 (Kevin 14.11. ~01:05 "beim schlafen/ausgelogt/nicht geladen in der welt weit out of range duerfen seine beduerfnisse nie
-- steigen", ~01:15 MP-Vorschlag bestaetigt): AUCH eingefroren, solange er liegt (nur die Muedigkeit sinkt weiter), sein Besitzer schlaeft
-- bzw. vorspult (Bitte "Sleep") oder er weiter als needFreezeR (70) Kacheln vom Besitzer ist. Eingefroren: kein Anstieg, kein Leben-Abzug,
-- kein Vertrauens-Verlust aus Hunger / Durst (am Boden kostet es trotzdem -10, fix1 R3), keine gezaehlte Stunde; kein Nachholen (dt je Takt,
-- gedeckelt auf maxDtH).
-- Sandbox BearNeedsPercent 0: Hunger, Durst, Muedigkeit stehen auf 0.
-- Folgen: B.NeedK (shared) an je EINER Stelle (Ausdauer-Erholung, Wachsen, Selbstheilung in server/BanditsNPCBearGrow.lua, Schaden in
-- shared/BanditsNPCBearFightRules.lua B.MeleeDamage); Leben bei Hunger / Durst 100 hier ueber B.BodyHurt -- Kevin 13.11.: "geht sein
-- leben auf 1% runter aber er stirbt nie daran" (needHpFloor 0,01; nie Tod, nie am Boden, kein B.OnHitTaken).
-- Fuettern senkt den Hunger (B.NeedEat aus B.FeedComplete), Traenken ist neu: B.DrinkComplete (aus BanditsNPCBearDrinkAction:complete(),
-- shared/TimedActions -- OBERFLAECHE). Wasser wird erst nach ALLEN Pruefungen in EINEM Aufruf genommen; eine Ablehnung nimmt nichts.
-- Mehrspieler: nur der Server rechnet und nimmt Wasser; Clients bitten nur (Netz-Zeitaktion) und zeigen aus der Sicht (B.NeedsView).
--
-- Engine-Aufrufe hier (Fundstelle am Aufruf): character:getInventory():contains(item), item:getFluidContainer(), :isEmpty(), :getAmount(),
-- :contains(Fluid.Water / Fluid.TaintedWater), :removeFluid(Zahl, false), item:sendSyncEntity(nil) (nur isServer()), getTimestampMs(),
-- getX / getY am Tier (Abstand zum Besitzer).
-- Ladefolge: server/ alphabetisch nach ...Mend, vor ...Order / ...Registry / ...Ride / ...Server / ...Sleep / ...World; fremde Funktionen
-- nur zur Laufzeit ueber B.X. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- Alle F3/K1-Felder des Eintrags (an anderen Zustaenden nil). trD nur, damit ein alter Verlauf mit verschwindet.
local FIELDS = { "nH", "nT", "nF", "tr", "trV", "nDay", "trD", "slpAt" }
local SET_FIELD = { hun = "nH", thr = "nT", tir = "nF", tru = "tr" }
local TRUST_V = 2                   -- K1: Fassung der Vertrauens-Skala -100..+100 (Register UND Spiegel)
-- Tages-Marken (0/1) im Tagesbuch nDay; die drei Gewinn-Quellen mit ihrer Meldung
local MARKS = { "gp", "gf", "gd", "lh", "lt", "lw" }
local GAIN = { pet = { "gp", "UI_BN_Bear_Note_TrustUpPet" }, feedfull = { "gf", "UI_BN_Bear_Note_TrustUpFed" },
               drinkfull = { "gd", "UI_BN_Bear_Note_TrustUpDrank" } }

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------
local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function clamp(v, lo, hi)
    if v < lo then return lo end
    if v > hi then return hi end
    return v
end

local function cfg(key, def)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return def end
    return v
end

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

local function isTame(st)
    return st == "tame" or st == "missing"
end

-- Diese Datei rechnet mit den Regeln aus shared/BanditsNPCBearNeedRules.lua. Fehlt jene Datei (Teilkopie) oder brach sie beim Laden ab,
-- tut jeder Weg hier NICHTS (wie statsOk in server/BanditsNPCBearGrow.lua) -- sonst wuerfe schon B.InitRegistry (B.NeedsFix) und der
-- ganze Baer stuende. B.SleepWakeMs ist ihre letzte Funktion; K1: B.TrustDelta / B.TrustMigrate / B.HunDayPts sind neu (eine alte
-- Regel-Datei ohne sie gilt als fehlend). Nur Tabellen-Lesen.
local function rulesOk()
    return B.NeedOf ~= nil and B.NeedsPct ~= nil and B.MealPct ~= nil and B.TrustDelta ~= nil and B.TrustMigrate ~= nil
        and B.HunDayPts ~= nil and B.SleepWakeMs ~= nil
end

-- Ganze Zahl fuer die Sicht: abgerundet (99,9 zeigt 99 -- 100 steht erst da, wenn es wirklich 100 ist).
local function whole(v)
    return math.floor((num(v) or 0) + 0.000001)
end

local function tellOwner(rec, players, n)
    if rec.owner == nil then return end
    local p = B.PlayerByKey(rec.owner, players)
    if p then B.Tell(p, B.NoteBd(n, rec)) end
end

local function tellWhy(character, rec, whyKey)
    B.Tell(character, B.NoteBd(note(whyKey, nil, nil, "bad"), rec))
end

-- Kann dieser Eintrag ueberhaupt kaempfen (grosser Koerper ab Halbstark, wie B.FightDecide)? Das Junge nie.
local function fights(rec)
    if rec.body ~= "big" or B.StatsOf == nil or B.FightStageOf == nil then return false end
    return B.FightStageOf(B.StatsOf(rec)).swipe == true
end

-- Spieltag einer Weltstunde
local function dayOf(now)
    return math.floor(now / 24)
end

-- ---------------------------------------------------------------------------
-- Migration und Klemmen (PLAN_F3.md 7; K1 PLAN_K1.md 2.2). Nur gezaehmt/vermisst; an jedem anderen Zustand sind alle F3/K1-Felder nil. Fehlt
-- ein Wert (eben gezaehmt, Baer von vor F3, Spiegel ohne F3-Felder), bekommt er den Erst-Wert: Hunger 20, Durst 20, Muedigkeit 10, Vertrauen 0
-- (kein Baer startet hungrig). Die Werte bleiben ungerundet (kleine Schritte je Takt), nur die Sicht rundet.
-- V1 (Kevin 13.11. ~21:40): ein Vertrauen OHNE die Marke trV = 2 ist ein alter Wert 0..100 -> EINMAL neu = (alt - 50) x 2 (B.TrustMigrate), die
-- Marke steht im selben Schritt (nie zweimal); fehlt das Vertrauen ganz, Start trStart (0). Eine hoehere (spaetere) Fassung bleibt unberuehrt.
-- ---------------------------------------------------------------------------
local function fixVal(v, def, lo, hi)
    local n = num(v)
    if n == nil then n = def end
    return clamp(n, lo, hi)
end

local function fixMark(v)
    if num(v) == 1 then return 1 end
    return 0
end

function B.NeedsFix(rec, now)
    if type(rec) ~= "table" or not rulesOk() then return end
    if not isTame(rec.st) then
        for i = 1, #FIELDS do rec[FIELDS[i]] = nil end
        return
    end
    rec.nH = fixVal(rec.nH, cfg("needStartHun", 20), 0, 100)
    rec.nT = fixVal(rec.nT, cfg("needStartThr", 20), 0, 100)
    rec.nF = fixVal(rec.nF, cfg("needStartTir", 10), 0, 100)
    local lo, hi = cfg("trMin", -100), cfg("trMax", 100)
    local tv = num(rec.trV)
    if tv == nil or tv < TRUST_V then
        local old = num(rec.tr)
        if old ~= nil then
            rec.tr = B.TrustMigrate(old)
            B.Log("trust: " .. tostring(rec.id) .. " scale v2 " .. tostring(B.Round1(old)) .. " -> " .. tostring(B.Round1(rec.tr)))
        else
            rec.tr = nil
        end
        rec.trV = TRUST_V
    end
    rec.tr = fixVal(rec.tr, cfg("trStart", 0), lo, hi)
    local d = rec.nDay
    if type(d) ~= "table" then
        d = {}
        rec.nDay = d
    end
    local day = dayOf(num(now) or B.Now())
    d.d = math.floor(num(d.d) or day)
    d.h = clamp(num(d.h) or 0, 0, 100)
    d.t = clamp(num(d.t) or 0, 0, 100)
    d.s = clamp(num(d.s) or 0, 0, 24)
    d.a = clamp(math.floor(num(d.a) or 0), 0, 99)
    d.c = clamp(num(d.c) or 0, 0, 24)
    for i = 1, #MARKS do d[MARKS[i]] = fixMark(d[MARKS[i]]) end
    d.p, d.l = nil, nil             -- F3: Hand-Punkte / letzte Handlung (Tages-Hand-Deckel, Wechsel-Bonus) gibt es nicht mehr
    rec.trD = nil                   -- F3: Verlauf des Tagesabschlusses gibt es nicht mehr
    rec.slpAt = num(rec.slpAt)
end

-- ---------------------------------------------------------------------------
-- Vertrauen setzen (die EINE Stelle): klemmen auf -100..+100, Meldungen beim Ueberschreiten -- trHeart nach oben (das Herz erscheint, Kevin
-- 13.11. Antwort 7), trRefuse (-70) nach unten ("weigert sich zu kaempfen ... und das steht dann da auch", Antwort 4) bzw. wieder nach oben;
-- die zwei Kampf-Meldungen nur am kampffaehigen Baeren. Sicht bei jeder Aenderung. Rueckgabe: die wirkliche Aenderung (0 an der Grenze).
-- ---------------------------------------------------------------------------
local function trustSet(rec, v, players)
    local old = num(rec.tr) or cfg("trStart", 0)
    local new = clamp(num(v) or old, cfg("trMin", -100), cfg("trMax", 100))
    rec.tr = new
    if new == old then return 0 end
    local refuse, heart = cfg("trRefuse", -70), cfg("trHeart", 100)
    if old < heart and new >= heart then
        tellOwner(rec, players, note("UI_BN_Bear_Note_TrustTop", nil, nil, "good"))
    end
    if rec.st == "tame" and fights(rec) then
        if old >= refuse and new < refuse then
            local s = B.Ses(rec.id)
            if type(s.refAt) ~= "table" then s.refAt = {} end
            s.refAt.trust = getTimestampMs()            -- Vanilla server/Foraging/forageServer.lua:456
            tellOwner(rec, players, note("UI_BN_Bear_Note_NoTrust", nil, nil, "bad"))
        elseif old < refuse and new >= refuse then
            tellOwner(rec, players, note("UI_BN_Bear_Note_TrustBack", nil, nil, "good"))
        end
    end
    B.Touch(rec)
    B.Log("trust: " .. tostring(rec.id) .. " " .. tostring(B.Round1(old)) .. " -> " .. tostring(B.Round1(new)))
    return new - old
end

-- Neuer Spieltag? Dann beginnt das Tagesbuch neu: alle sechs Marken auf 0 (K1: kein Tagesabschluss mehr -- Kevin 14.11. ~00:00 "Kein
-- Tagesabschluss-Verlust mehr"). Auch eine rueckwaerts gestellte Uhr beginnt neu.
local function dayRoll(rec, now)
    local d = rec.nDay
    local day = dayOf(now)
    if type(d) == "table" and d.d == day then return end
    local nd = { d = day, h = 0, t = 0, s = 0, a = 0, c = 0 }
    for i = 1, #MARKS do nd[MARKS[i]] = 0 end
    rec.nDay = nd
end

-- Ein Verlust nach Kevins Regel (V3): Aenderung B.TrustDelta(kind), Meldung k an den Besitzer mit dem Betrag (nur, wenn sich wirklich etwas
-- aenderte -- bei -100 bleibt es still). Rueckgabe: die wirkliche Aenderung.
local function trustLoss(rec, kind, k, players)
    local want = B.TrustDelta(kind)
    local got = trustSet(rec, rec.tr + want, players)
    if got ~= 0 then tellOwner(rec, players, note(k, "num", -want, "bad")) end
    B.Log("trust: " .. tostring(rec.id) .. " loses (" .. tostring(kind) .. ") " .. tostring(B.Round1(got)))
    return got
end

-- ---------------------------------------------------------------------------
-- Zaehlen die Beduerfnisse dieses Eintrags gerade? (PLAN_F3.md 2.1; K1 PLAN_K1.md 6) Rueckgabe: zaehlt, grund.
-- Nein ohne Grund (wie F3): nicht gezaehmt (vermisst), Besitzer nicht im Spiel.
-- Nein MIT Grund (K1, Kevin 14.11. ~01:05 / ~01:15; Grund fuer die Sicht nfz): "sleep" -- er liegt (Hinlegen oder Schlaf; nur die Muedigkeit
-- sinkt weiter), "owner" -- sein Besitzer schlaeft bzw. spult vor (Bitte "Sleep", B.OwnerAsleep in server/BanditsNPCBearSleep.lua), "far" --
-- weiter als needFreezeR (70) Kacheln vom naechsten seiner Spieler (im Mehrspieler kann ihn ein ANDERER Spieler geladen halten).
-- fix1 (R5, k1/GEGEN.md 7): auch "far", wenn sein Koerper nicht in der Welt ist und er nicht mitfaehrt (nicht geladen = weiter weg als die
-- geladene Gegend um jeden Spieler; das Fenster zeigt dann "ausser Reichweite") -- vorher ohne Grund, der Satz "ruhen" fehlte.
-- Mitfahrend zaehlt der Abstand nicht (er sitzt beim Besitzer). getX / getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576;
-- die Spieler-Lage kommt fertig aus B.Players() (e.x / e.y, server/BanditsNPCBearWorld.lua). fix1 (R3): "am Boden" folgt dieser Sperre NICHT
-- mehr (B.TrustAdd).
-- ---------------------------------------------------------------------------
local function ownerDist(rec, a, players)
    players = players or B.Players()
    local ax, ay = a:getX(), a:getY()
    local best = nil
    for i = 1, #players do
        local e = players[i]
        if e.key == rec.owner and num(e.x) ~= nil and num(e.y) ~= nil then
            local d = B.DistXY(ax, ay, e.x, e.y)
            if best == nil or d < best then best = d end
        end
    end
    return best
end

local function counts(rec, online, players)
    if rec.st ~= "tame" or rec.owner == nil then return false, nil end
    if type(online) ~= "table" or online[rec.owner] ~= true then return false, nil end
    local a = nil
    if rec.ride == nil then
        a = B.FindAnimal(rec)
        if a == nil then return false, "far" end        -- fix1 (R5): nicht geladen -> Grund fuer die Sicht
    end
    if B.IsLying ~= nil and B.IsLying(rec) then return false, "sleep" end
    if B.OwnerAsleep ~= nil and B.OwnerAsleep(rec.owner) then return false, "owner" end
    if a ~= nil then
        local d = ownerDist(rec, a, players)
        if d ~= nil and d > cfg("needFreezeR", 70) then return false, "far" end
    end
    return true, nil
end

-- ---------------------------------------------------------------------------
-- Vertrauen aus der Hand und aus Ereignissen (K1, PLAN_K1.md 2.2; Kevins endgueltige Regel 14.11. ~00:00). kind =
--   "pet" (gestreichelt) / "feedfull" (Hunger durch Fuettern aus der Hand auf 0 %) / "drinkfull" (Durst durch Traenken aus der Hand auf 0 %):
--     je Quelle hoechstens 1x je Spieltag +trGain (0,5) -- die Marke gp / gf / gd im Tagesbuch; Meldung UI_BN_Bear_Note_TrustUp*.
--     Den Fall "auf 0 gebracht" entscheidet der Aufrufer (B.FeedComplete, B.DrinkComplete); selbst gefressen / getrunken ruft nie.
--   "down": am Boden (Todesschutz), JEDES Mal trDown (-10), Meldung UI_BN_Bear_Note_TrustDown. fix1 (R3; Kevin 14.11. ~00:00 woertlich
--     "wenn der baer down (todesschutz) geht verliert er -10"): auch, wenn seine Beduerfnisse gerade ruhen -- die Sperre der Nachbesserung
--     K1 C2 (nur solange er zaehlt) ist zurueckgenommen; so stimmt der Tooltip "jedes Mal".
--   jede andere Art (auch die alten "feed" / "drink"): nichts.
-- Das dritte Argument (frueher die Futterklasse) wird nicht mehr gebraucht. Rueckgabe: die wirkliche Aenderung. Festschreiben: der Aufrufer.
-- ---------------------------------------------------------------------------
function B.TrustAdd(rec, kind, _, now, players)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return 0 end
    now = num(now) or B.Now()
    B.NeedsFix(rec, now)
    if kind == "down" then
        return trustLoss(rec, "down", "UI_BN_Bear_Note_TrustDown", players)     -- fix1 (R3): jedes Mal, ohne Einfrier-Sperre
    end
    local g = GAIN[kind]
    if g == nil then return 0 end
    dayRoll(rec, now)
    local d = rec.nDay
    if d[g[1]] == 1 then return 0 end
    d[g[1]] = 1
    B.Touch(rec)                    -- die Sicht traegt die erledigten Quellen (trT)
    local got = trustSet(rec, rec.tr + B.TrustDelta(kind), players)
    if got ~= 0 then tellOwner(rec, players, note(g[2], nil, nil, "good")) end
    B.Log("trust: " .. tostring(rec.id) .. " gains (" .. tostring(kind) .. ") " .. tostring(B.Round1(got)))
    return got
end

-- ---------------------------------------------------------------------------
-- Fressen und Trinken: die Schnittstelle fuer F4 / F5 (frisst aus dem Inventar, Fische, trinkt selbst). meals = Mahlzeiten (B.MealsOf),
-- bowls = Schalen (Liter / bowlL). Was unter 0 ginge, verfaellt (kein Vorrat). Rueckgabe: der neue Wert. Festschreiben: der Aufrufer.
-- K1: ein Rest unter 0,0005 (Rundung beim Trinken genau "bis 0") gilt als 0 -- sonst zaehlte "satt" nie.
-- Nachbesserung K1 C1: aus der HAND (why "hand") gilt schon ein Rest unter needFull (1 %) als 0 -- die Sicht zeigt dann 0 %, das naechste
-- Fuettern / Traenken lehnt B.CheckFeed / B.CheckDrink ab; so bringt das letzte Stueck den Hunger immer auf 0 ("satt gefuettert"). Hoechstens
-- 1 % der Tagesmenge geschenkt; selbst gefressen / getrunken ("inv") bleibt genau.
-- ---------------------------------------------------------------------------
local ZERO = 0.0005

local function restOf(v, why)
    if v < ZERO then return 0 end
    if why == "hand" and v < cfg("needFull", 1) then return 0 end
    return v
end

function B.NeedEat(rec, meals, why)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return nil end
    B.NeedsFix(rec, B.Now())
    local m = num(meals) or 0
    if m < 0 then m = 0 end
    local was = rec.nH
    local v = restOf(clamp(was - m * B.MealPct(rec), 0, 100), why)
    rec.nH = v
    B.Touch(rec)
    B.Log("needs: " .. tostring(rec.id) .. " eats " .. tostring(B.Round1(m)) .. " meal(s) (" .. tostring(why) .. "), hunger "
        .. tostring(B.Round1(was)) .. " -> " .. tostring(B.Round1(rec.nH)))
    return rec.nH
end

function B.NeedDrink(rec, bowls, why)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return nil end
    B.NeedsFix(rec, B.Now())
    local b = num(bowls) or 0
    if b < 0 then b = 0 end
    local was = rec.nT
    local v = restOf(clamp(was - b * B.BowlPct(rec), 0, 100), why)
    rec.nT = v
    B.Touch(rec)
    B.Log("needs: " .. tostring(rec.id) .. " drinks " .. tostring(B.Round1(b)) .. " bowl(s) (" .. tostring(why) .. "), thirst "
        .. tostring(B.Round1(was)) .. " -> " .. tostring(B.Round1(rec.nT)))
    return rec.nT
end

-- ---------------------------------------------------------------------------
-- Traenken (PLAN_F3.md 5.2). Gerufen aus BanditsNPCBearDrinkAction:complete() -- im Mehrspieler auf dem Server mit dem Behaelter des
-- SERVERS. Reihenfolge der Ablehnungen (jede mit Meldung, OHNE dass etwas genommen wird): Why_Gone / Why_Far (B.HandCheck),
-- Why_NotOwner / Why_Riding / Why_Down / Why_NotThirsty (B.CheckDrink, shared/BanditsNPCBearRules.lua), Why_NoItem, Why_NoWater.
-- Dann GENAU EIN removeFluid mit der Menge, die den Durst stillt (hoechstens was im Behaelter ist, mindestens drinkMinL), und im selben
-- Lua-Aufruf gutschreiben. Ein schlafender Baer wird dafuer geweckt (Kevin 13.11. 6e "Fuettern/Traenken wecken kurz").
-- K1: die Menge ist so viel, wie bis 0 % fehlt (B.DrinkNeedL nach Groesse, ausgewachsen bis 15 l); bringt sie den Durst auf 0, ist er "satt
-- getraenkt" (+0,5 Vertrauen, 1x je Spieltag, B.TrustAdd "drinkfull").
-- Nachbesserung C8: zwischen Nehmen und Gutschrift steht KEIN Engine-Aufruf mehr -- der Abgleich des Behaelters am Server
-- (sendSyncEntity) kommt als Letztes, nach Gutschrift, Spiegel, Meldung und Sicht. Wuerfe er, waere das Wasser trotzdem angerechnet.
-- character:getInventory():contains(item): Vanilla shared/TimedActions/Animals/ISGiveWaterToAnimal.lua:6.
-- item:getFluidContainer() als Vorfrage (nil ohne Behaelter): Vanilla shared/Vehicles/TimedActions/ISWashVehicle.lua:6,
--   shared/Camping/ISCampingMenu.lua:37. :isEmpty(): ISGiveWaterToAnimal.lua:6. :getAmount(): ISWashVehicle.lua:6 (Liter).
-- :contains(Fluid.Water) / :contains(Fluid.TaintedWater): ISWashVehicle.lua:6 -- der Schreiber glaubt dem Client nicht, dass es Wasser ist
--   (das Menue bietet wie Vanilla getAllWaterFluidSources(true) an, auch ungereinigtes Wasser).
-- :removeFluid(Zahl, false): ISGiveWaterToAnimal.lua:34 (Einzelspieler-Zweig "if not isClient()" in update), :86 (Server).
-- item:sendSyncEntity(nil): ISGiveWaterToAnimal.lua:87 -- dort nur im isServer()-Zweig, hier ebenso.
-- Ehrlich offen (Testpunkt T6): Vanilla nimmt je Schritt 0,05 l; ob EIN groesserer Abzug am Server sauber bei allen ankommt, ist ungespielt.
-- Rueckgabe: true, wenn getrunken.
-- ---------------------------------------------------------------------------
function B.DrinkComplete(character, animal, item)
    if character == nil or animal == nil or item == nil then return false end
    local hc = B.HandCheck
    if hc == nil or B.CheckDrink == nil or not rulesOk() then return false end
    local rec = hc(character, animal)
    if not rec then return false end
    local pkey = B.PlayerKey(character)
    local now = B.Now()
    B.NeedsFix(rec, now)
    local ok, whyKey = B.CheckDrink(rec, pkey)
    if not ok then
        tellWhy(character, rec, whyKey)
        return false
    end
    if not character:getInventory():contains(item) then
        tellWhy(character, rec, "UI_BN_Bear_Why_NoItem")
        return false
    end
    local fc = item:getFluidContainer()
    if fc == nil or fc:isEmpty() or not (fc:contains(Fluid.Water) or fc:contains(Fluid.TaintedWater)) then
        tellWhy(character, rec, "UI_BN_Bear_Why_NoWater")
        return false
    end
    local have = num(fc:getAmount()) or 0
    if have <= 0 then
        tellWhy(character, rec, "UI_BN_Bear_Why_NoWater")
        return false
    end
    local bowlL = cfg("bowlL", 0.5)
    if bowlL <= 0 then bowlL = 0.5 end
    local take = B.DrinkNeedL(rec, rec.nT)
    local minL = cfg("drinkMinL", 0.05)
    if take < minL then take = minL end
    if take > have then take = have end
    local thr0 = rec.nT
    -- ab hier wird genommen: EIN Aufruf, danach im selben Lua-Aufruf gutschreiben, ohne Engine-Aufruf dazwischen
    fc:removeFluid(take, false)
    if B.SleepStop then B.SleepStop(rec, "hand") end
    B.NeedDrink(rec, take / bowlL, "hand")
    if thr0 > 0 and rec.nT <= 0 then B.TrustAdd(rec, "drinkfull", nil, now) end
    B.Commit(rec)
    B.Tell(character, B.NoteBd(note("UI_BN_Bear_Note_Drank", "num", whole(rec.nT), "good"), rec))
    B.Log("drink " .. tostring(rec.id) .. " " .. tostring(pkey) .. " took " .. tostring(math.floor(take * 1000 + 0.5)) .. " mL of "
        .. tostring(math.floor(have * 1000 + 0.5)) .. " mL, thirst " .. tostring(B.Round1(rec.nT)))
    B.FlushViews()
    -- der Behaelter-Abgleich fuer die Clients zuletzt (Vanilla ISGiveWaterToAnimal.lua:87, dort ebenfalls nur im isServer()-Zweig)
    if isServer() then item:sendSyncEntity(nil) end
    return true
end

-- ---------------------------------------------------------------------------
-- Meldungen an den Besitzer (PLAN_F3.md 3.3): hungrig / durstig (ab 50) bzw. ausgehungert / ausgetrocknet (ab 80) -- beim Erreichen der
-- Stufe und danach als Erinnerung, je Art hoechstens alle needNoteH Spielstunden (Uhr in der Sitzung -- nach dem Laden einmal neu).
-- "Zu muede" (ab 90) einmal beim Ueberschreiten; dazu "zu muede" / "kein Vertrauen" beim verweigerten Kampf: B.NeedRefuseSay.
-- ---------------------------------------------------------------------------
local function say(rec, s, k, tone, now, players)
    if type(s.noteAt) ~= "table" then s.noteAt = {} end
    local at = num(s.noteAt[k])
    if at ~= nil and now - at >= 0 and now - at < cfg("needNoteH", 6) then return end
    s.noteAt[k] = now
    tellOwner(rec, players, note(k, nil, nil, tone))
end

local function bandOf(v)
    if v >= cfg("needStarve", 80) then return 2 end
    if v >= cfg("needHungry", 50) then return 1 end
    return 0
end

-- Rueckgabe: true, wenn eine Stufe wechselte (dann sofort festschreiben und Sicht).
local function bands(rec, s, now, players)
    local nb = s.nb
    if type(nb) ~= "table" then
        nb = {}
        s.nb = nb
    end
    local changed = false
    local bh, bt = bandOf(rec.nH), bandOf(rec.nT)
    -- solange die Stufe gilt, erinnert die Meldung (say drosselt je Art auf needNoteH; beim Ueberschreiten kommt sie sofort, weil die
    -- hoehere Stufe einen eigenen Schluessel hat)
    if bh == 2 then
        say(rec, s, "UI_BN_Bear_Note_Starving", "bad", now, players)
    elseif bh == 1 then
        say(rec, s, "UI_BN_Bear_Note_Hungry", nil, now, players)
    end
    if bt == 2 then
        say(rec, s, "UI_BN_Bear_Note_Parched", "bad", now, players)
    elseif bt == 1 then
        say(rec, s, "UI_BN_Bear_Note_Thirsty", nil, now, players)
    end
    if bh ~= nb.h then
        changed = nb.h ~= nil
        nb.h = bh
    end
    if bt ~= nb.t then
        changed = changed or nb.t ~= nil
        nb.t = bt
    end
    -- Kevin 13.11. Antwort 3: "ab 90% sagt das er zu muede ist zum kaempfen"
    local tired = rec.nF >= cfg("tirVery", 90)
    if tired ~= (nb.f == true) then
        if tired then
            if type(s.refAt) ~= "table" then s.refAt = {} end
            s.refAt.tired = getTimestampMs()            -- Vanilla server/Foraging/forageServer.lua:456
            say(rec, s, "UI_BN_Bear_Note_Tired", "bad", now, players)
        end
        changed = true
        nb.f = tired
    end
    return changed
end

-- Aus B.FightStep (server/BanditsNPCBearFight.lua), wenn er einen Kampf verweigert: why = "tired" / "trust". Meldung an den Besitzer,
-- je Grund hoechstens alle refuseSayMs (Echtzeit) -- Kevin: "sagt das er zu muede ist" / "weigert er sich zu kaempfen und das steht dann da".
function B.NeedRefuseSay(rec, why, ms, players)
    if type(rec) ~= "table" then return end
    local k = nil
    if why == "tired" then
        k = "UI_BN_Bear_Note_Tired"
    elseif why == "trust" then
        k = "UI_BN_Bear_Note_NoTrust"
    end
    if k == nil then return end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    if type(s.refAt) ~= "table" then s.refAt = {} end
    local at = num(s.refAt[why])
    if at ~= nil and ms - at >= 0 and ms - at < cfg("refuseSayMs", 60000) then return end
    s.refAt[why] = ms
    tellOwner(rec, players, note(k, nil, nil, "bad"))
end


-- ---------------------------------------------------------------------------
-- Je Langsam-Takt (10 Spielminuten; dt = Spielstunden seit dem letzten Takt, vom Aufrufer auf maxDtH gedeckelt). Eigene Schleife NACH
-- B.GrowSlow (ein Fehler hier reisst Wachsen und Heilen nicht mit). Schritte: klemmen -> zaehlt er? (Grund des Einfrierens in die Sicht) ->
-- neuer Spieltag (Marken auf 0) -> Anstieg Hunger / Durst (needRiseH 6,25 je Stunde x Tempo x Vertrauens-Faktor) -> Muedigkeit (wach: Tempo
-- der Groesse + Anstrengung aus der Sitzung s.tirAcc) -> V3: Hunger / Durst erreicht trLossAt -> -5 (je 1x am Tag) -> Leben bei 100 und V3
-- Leben 1 % -> -10 (1x am Tag) -> Meldungen -> Sicht (ab needViewStep Punkten oder bei einem Stufenwechsel) -> Spiegel (ueber s.gDirty mit dem
-- naechsten Wachstums-Commit, sofort bei einem Stufenwechsel oder einer Vertrauens-Aenderung) -> selbst fressen / trinken (F4 / K1 E).
-- Eingefroren wegen Liegen ("sleep"): nur der Schlaf-Abbau der Muedigkeit (B.SleepDrain), Meldungen, Sicht und Spiegel laufen weiter.
-- ---------------------------------------------------------------------------
function B.NeedsSlow(rec, dt, online, now, players)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return end
    now = num(now) or B.Now()
    B.NeedsFix(rec, now)
    local go, why = counts(rec, online, players)
    -- Sicht nfz: der Grund, solange er eingefroren ist (Wechsel -> neue Sicht); eine Sitzung wird dafuer nur angelegt, wenn es einen Grund gibt
    local s0 = B._s and B._s[rec.id] or nil
    if s0 ~= nil or why ~= nil then
        s0 = B.Ses(rec.id)
        if s0.nfz ~= why then
            s0.nfz = why
            B.Touch(rec)
        end
    end
    if not go and why ~= "sleep" then
        if s0 ~= nil then s0.tirAcc = nil end   -- keine Anstrengung sammeln, waehrend nichts zaehlt (kein Nachholen)
        return
    end
    dt = num(dt) or 0
    if dt < 0 then dt = 0 end
    local s = B.Ses(rec.id)
    local pct = B.NeedsPct()
    local on = pct > 0
    local hp0 = rec.hp
    local tr0 = rec.tr
    if not on then
        -- Sandbox 0: alle drei aus und auf 0 gehalten (Muster NPC Crew shared/BanditsNPCNeeds.lua, NeedsRateMult 0)
        rec.nH, rec.nT, rec.nF = 0, 0, 0
    elseif not go then
        -- er liegt: Hunger und Durst stehen, die Muedigkeit sinkt (der Abbau ist ihre ganze Uhr, wie bei den NPC-Crew-Figuren)
        if B.SleepDrain then B.SleepDrain(rec, s, now) end
    else
        dayRoll(rec, now)
        local d = rec.nDay
        d.c = clamp(d.c + dt, 0, 24)
        local k = pct / 100 * B.TrustK(rec)
        local rise = cfg("needRiseH", 6.25) * k * dt
        rec.nH = clamp(rec.nH + rise, 0, 100)
        rec.nT = clamp(rec.nT + rise, 0, 100)
        local add = B.TirRate(rec) * k * dt
        local acc = num(s.tirAcc) or 0
        if acc > 0 and B.StatsOf ~= nil then
            local staMax = num(B.StatsOf(rec).staMax) or 1
            if staMax <= 0 then staMax = 1 end
            add = add + acc / staMax * cfg("tirPerBar", 3) * k
        end
        rec.nF = clamp(rec.nF + add, 0, 100)
        if rec.nH > d.h then d.h = rec.nH end
        if rec.nT > d.t then d.t = rec.nT end
        -- V3 (Kevin 14.11. ~00:00 "trinken/essen bei 90% direkt - 5"): je Wert hoechstens 1x je Spieltag (Frage K-F2: steht er am neuen Tag
        -- noch darueber, kostet auch der neue Tag -5)
        local lossAt = cfg("trLossAt", 90)
        if rec.nH >= lossAt and d.lh ~= 1 then
            d.lh = 1
            trustLoss(rec, "hun90", "UI_BN_Bear_Note_TrustHungry", players)
        end
        if rec.nT >= lossAt and d.lt ~= 1 then
            d.lt = 1
            trustLoss(rec, "thr90", "UI_BN_Bear_Note_TrustThirsty", players)
        end
        -- Leben bei Hunger / Durst 100 (Kevin 13.11. Antwort 6a): bis needHpFloor (1 %), nie Tod, nie am Boden. Nicht am Boden (er ist
        -- schon hilflos) und nicht, solange das Leben noch nie abgeglichen wurde (mitfahrend seit dem Laden). B.BodyHurt ist die EINE
        -- Stelle, an der das Register-Leben sinkt (server/BanditsNPCBearGrow.lua; geht auch ohne Koerper) -- kein B.OnHitTaken.
        local rate = 0
        if rec.nH >= 100 then rate = rate + cfg("needHpHun", 2) end
        if rec.nT >= 100 then rate = rate + cfg("needHpThr", 3) end
        local floor = cfg("needHpFloor", 0.01)
        if rate > 0 and dt > 0 and rec.down == nil and B.BodyHurt ~= nil then
            local a = B.FindAnimal(rec)
            if a ~= nil and B.BodyHp ~= nil then B.BodyHp(rec, a, 0) end
            local hp = num(rec.hp)
            if hp ~= nil then
                local frac = rate / 100 * dt
                local room = hp - floor
                if frac > room then frac = room end
                if frac > 0 then B.BodyHurt(rec, a, frac) end
            end
        end
        -- V3 (Kevin ~00:00 "ab 1% hp (durch hunger/durst) auch -10"): Leben steht durch Hunger / Durst auf needHpFloor -> -10, 1x je Spieltag
        local hpNow = num(rec.hp)
        if rate > 0 and rec.down == nil and hpNow ~= nil and hpNow <= floor + 0.000001 and d.lw ~= 1 then
            d.lw = 1
            trustLoss(rec, "weak", "UI_BN_Bear_Note_TrustWeak", players)
        end
    end
    s.tirAcc = nil
    local stepped = bands(rec, s, now, players)
    -- Sicht: nur bei sichtbarer Aenderung
    local nv = s.nv
    local h, t, f = whole(rec.nH), whole(rec.nT), whole(rec.nF)
    local step = cfg("needViewStep", 2)
    local edge = type(nv) == "table" and ((h == 0) ~= (nv.h == 0) or (t == 0) ~= (nv.t == 0) or (f == 0) ~= (nv.f == 0)
        or (h == 100) ~= (nv.h == 100) or (t == 100) ~= (nv.t == 100) or (f == 100) ~= (nv.f == 100))
    if type(nv) ~= "table" or stepped or edge or rec.hp ~= hp0 or math.abs(h - nv.h) >= step or math.abs(t - nv.t) >= step
        or math.abs(f - nv.f) >= step then
        s.nv = { h = h, t = t, f = f }
        B.Touch(rec)
    end
    s.gDirty = true                 -- der naechste Wachstums-Commit (B.GrowSlow, hoechstens je growCommitH) schreibt den Spiegel
    if stepped or rec.tr ~= tr0 then B.Commit(rec) end
    -- F4 / K1 (Kevin 14.11. ~00:30 / ~00:50): ab 50 % frisst und trinkt er selbst aus seinem Inventar, bis 0 % (server/BanditsNPCBearInv.lua)
    -- -- nur, solange gezaehlt wird
    if go and on then
        if B.InvEatStep then B.InvEatStep(rec, now, players) end
        if B.InvDrinkStep then B.InvDrinkStep(rec, now, players) end
    end
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_F3.md 7; K1 k1/schnittstelle.md K3) -- aus viewEntry, nur gezaehmt/vermisst, fuer eigene UND fremde Baeren; schreibt nur in t:
-- hun / thr / tir (ganze Zahlen 0..100, abgerundet), tru (K1: -100..+100 mit EINER Nachkommastelle, B.Round1 -- nie abrunden, -0,5 bleibt
-- -0,5), trM (Vertrauen ab trHeart: das Herz ueber dem Namensschild, Kevin 13.11. Antwort 7), nof ("trust" / "tired": er kaempft gerade nicht
-- -- nur am kampffaehigen Baeren), trT (K1: heute schon erledigte Gewinn-Quellen "p" gestreichelt / "f" satt gefuettert / "d" satt getraenkt,
-- in dieser Reihenfolge; fehlt = keine), meal / bowl (so viele Punkte senkt eine Mahlzeit / eine Schale bei dieser Groesse, auf 0,1), hd / wl
-- (K1: Vanilla-Hungerpunkte bzw. Liter der vollen Leiste, ganze Zahl / 0,1), nfz (K1: "sleep" / "owner" / "far", nur waehrend eingefroren).
-- trW (Verlauf der Tage) entfaellt mit K1.
-- ---------------------------------------------------------------------------
function B.NeedsView(rec, t)
    if type(rec) ~= "table" or type(t) ~= "table" or not isTame(rec.st) or not rulesOk() then return end
    local h, th, f, tr = B.NeedOf(rec, "hun"), B.NeedOf(rec, "thr"), B.NeedOf(rec, "tir"), B.NeedOf(rec, "tru")
    if h ~= nil then t.hun = whole(h) end
    if th ~= nil then t.thr = whole(th) end
    if f ~= nil then t.tir = whole(f) end
    if tr ~= nil then
        t.tru = B.Round1(tr)
        if tr >= cfg("trHeart", 100) then t.trM = true end
    end
    if rec.st == "tame" and fights(rec) then t.nof = B.NoFight(rec) end
    local d = rec.nDay
    if type(d) == "table" and d.d == dayOf(B.Now()) then
        local txt = ""
        if d.gp == 1 then txt = txt .. "p" end
        if d.gf == 1 then txt = txt .. "f" end
        if d.gd == 1 then txt = txt .. "d" end
        if txt ~= "" then t.trT = txt end
    end
    t.meal = B.Round1(B.MealPct(rec))
    t.bowl = B.Round1(B.BowlPct(rec))
    t.hd = math.floor(B.HunDayPts(rec) + 0.5)
    t.wl = B.Round1(B.WaterDayL(rec))
    local s = B._s and B._s[rec.id] or nil
    if type(s) == "table" and type(s.nfz) == "string" then t.nfz = s.nfz end
end

-- ---------------------------------------------------------------------------
-- Aus dem Spiegel (server/BanditsNPCBearHeal.lua B.Restore / B.TakeNewerMark, nur fuer einen gezaehmten Eintrag): die vier Werte
-- geklemmt uebernehmen (Unsinn -> Erst-Wert), dazu die Fassung trV (K1: ein Spiegel OHNE trV traegt den alten Wert 0..100 -> B.NeedsFix
-- rechnet ihn einmal um; ein Spiegel mit trV 2 nie). Tagesbuch beginnt neu (nicht im Spiegel -- harmlos).
-- Nachbesserung K1 C5: die sechs Tages-Marken (gp gf gd lh lt lw) reisen flach mit (mark.nDd = Spieltag, mark.nDm = Bitmaske 1/2/4/8/16/32,
-- B.NeedsDayMark; geschrieben in B.MarkOf, server/BanditsNPCBearHeal.lua) -- sonst gaebe es nach B.Restore / B.TakeNewerMark am selben Tag
-- noch einmal -5 bzw. +0,5 je Quelle ("1x pro tag" gebrochen). Gilt nur fuer den LAUFENDEN Tag; ein eigenes Tagesbuch desselben Tages
-- (B.TakeNewerMark: der Eintrag lebt weiter) wird vereinigt -- eine Marke geht am Tag nur von 0 auf 1, also nie zweimal. Ein Spiegel ohne
-- die zwei Felder (von vor der Nachbesserung): wie bisher.
-- ---------------------------------------------------------------------------
function B.NeedsDayMark(rec)
    local d = type(rec) == "table" and rec.nDay or nil
    if type(d) ~= "table" or num(d.d) == nil then return nil, nil end
    local m, bit = 0, 1
    for i = 1, #MARKS do
        if num(d[MARKS[i]]) == 1 then m = m + bit end
        bit = bit * 2
    end
    return math.floor(d.d), m
end

local function dayFromMark(mark, own, day)
    local nd = nil
    local md, mm = num(mark.nDd), num(mark.nDm)
    if md ~= nil and mm ~= nil and math.floor(md) == day and mm >= 0 then
        nd = { d = day, h = 0, t = 0, s = 0, a = 0, c = 0 }
        local m, bit = math.floor(mm), 1
        for i = 1, #MARKS do
            nd[MARKS[i]] = 0
            if math.floor(m / bit) % 2 == 1 then nd[MARKS[i]] = 1 end
            bit = bit * 2
        end
    end
    if type(own) == "table" and num(own.d) == day then
        if nd == nil then return own end
        for i = 1, #MARKS do
            if num(own[MARKS[i]]) == 1 then nd[MARKS[i]] = 1 end
        end
        nd.h, nd.t, nd.s, nd.a, nd.c = own.h, own.t, own.s, own.a, own.c
    end
    return nd
end

function B.NeedsFromMark(rec, mark, now)
    if type(rec) ~= "table" or type(mark) ~= "table" then return end
    local own = rec.nDay
    rec.nH, rec.nT, rec.nF, rec.tr, rec.trV = mark.nH, mark.nT, mark.nF, mark.tr, mark.trV
    rec.nDay, rec.trD, rec.slpAt = nil, nil, nil
    rec.nDay = dayFromMark(mark, own, dayOf(num(now) or B.Now()))
    B.NeedsFix(rec, now)
end

-- ---------------------------------------------------------------------------
-- Von Hand (Probeweg der Test-Mod zum Setzen der vier Werte -- im Spiel nie gerufen, das Uebernahme-Skript prueft das: Regel probeweg).
-- k = "hun" / "thr" / "tir" (0..100) / "tru" (K1: -100..+100). Vertrauen ueber die EINE Setz-Stelle (Meldungen wie im Spiel).
-- Rueckgabe: der gesetzte Wert oder nil.
-- ---------------------------------------------------------------------------
function B.NeedsSet(rec, k, v)
    local field = SET_FIELD[k]
    local n = num(v)
    if type(rec) ~= "table" or not isTame(rec.st) or field == nil or n == nil or not rulesOk() then return nil end
    B.NeedsFix(rec, B.Now())
    if field == "tr" then
        n = clamp(n, cfg("trMin", -100), cfg("trMax", 100))
        trustSet(rec, n, nil)
    else
        n = clamp(n, 0, 100)
        rec[field] = n
    end
    B.Commit(rec)
    return n
end
