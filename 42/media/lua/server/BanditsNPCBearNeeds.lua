if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Beduerfnisse und Vertrauen beim Schreiber (F3, PLAN_F3.md 2-5, 7; Kevins Antworten vom 13.11.2026,
-- _arbeit/baer_zaehmen/f3/KEVIN_ANTWORTEN.md -- sie gehen vor dem Plan).
--
-- Die Wahrheit steht im Register-Eintrag (nur gezaehmt/vermisst, Koerper-Tausch-fest): nH (Hunger), nT (Durst), nF (Muedigkeit) -- je
-- 0 = gut .. 100 = am Ende --, tr (Vertrauen 0..100, Start 50), nDay (laufender Spieltag: d Tag, h / t Hoechst-Hunger / -Durst, s
-- Schlafstunden, a Aufschrecken, c gezaehlte Stunden, p Hand-Punkte, l letzte Handlung), trD (Verlauf der letzten drei abgeschlossenen
-- Tage als Ziffern-Text, aeltester zuerst: 0 gut versorgt / 1 hungrig oder durstig / 2 ausgehungert oder ausgetrocknet), slpAt
-- (Weltstunde des Einschlafens aus Muedigkeit: mit dieser Marke schlaeft er nach einem Laden und nach dem Fuettern / Traenken weiter,
-- solange die Muedigkeit ueber tirWake liegt -- server/BanditsNPCBearSleep.lua).
-- Die Engine-Werte HUNGER / THIRST des Tiers bleiben unbenutzt (FORSCHUNG_F3.md 0.4). Formeln: shared/BanditsNPCBearNeedRules.lua.
--
-- Gezaehlt wird im Langsam-Takt (B.NeedsSlow, eigene Schleife NACH B.GrowSlow in server/BanditsNPCBearServer.lua): nur gezaehmt, Besitzer
-- im Spiel, und nur mit Koerper in der Welt oder mitfahrend -- ein entladener Baer ist eingefroren (er verhungert nie, waehrend du weg
-- bist). Sandbox BearNeedsPercent 0: Hunger, Durst, Muedigkeit stehen auf 0.
-- Folgen: B.NeedK (shared) an je EINER Stelle (Ausdauer-Erholung, Wachsen, Selbstheilung in server/BanditsNPCBearGrow.lua, Schaden in
-- shared/BanditsNPCBearFightRules.lua B.MeleeDamage); Leben bei Hunger / Durst 100 hier ueber B.BodyHurt -- Kevin 13.11.: "geht sein
-- leben auf 1% runter aber er stirbt nie daran" (needHpFloor 0,01; nie Tod, nie am Boden, kein B.OnHitTaken).
-- Fuettern senkt den Hunger (B.NeedEat aus B.FeedComplete), Traenken ist neu: B.DrinkComplete (aus BanditsNPCBearDrinkAction:complete(),
-- shared/TimedActions -- OBERFLAECHE). Wasser wird erst nach ALLEN Pruefungen in EINEM Aufruf genommen; eine Ablehnung nimmt nichts.
-- Mehrspieler: nur der Server rechnet und nimmt Wasser; Clients bitten nur (Netz-Zeitaktion) und zeigen aus der Sicht (B.NeedsView).
--
-- Engine-Aufrufe hier (Fundstelle am Aufruf): character:getInventory():contains(item), item:getFluidContainer(), :isEmpty(), :getAmount(),
-- :contains(Fluid.Water / Fluid.TaintedWater), :removeFluid(Zahl, false), item:sendSyncEntity(nil) (nur isServer()), getTimestampMs().
-- Ladefolge: server/ alphabetisch nach ...Mend, vor ...Order / ...Registry / ...Ride / ...Server / ...Sleep / ...World; fremde Funktionen
-- nur zur Laufzeit ueber B.X. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- Alle F3-Felder des Eintrags (an anderen Zustaenden nil).
local FIELDS = { "nH", "nT", "nF", "tr", "nDay", "trD", "slpAt" }
local HAND = { feed = true, pet = true, drink = true }
local CODE = { [0] = "0", [1] = "1", [2] = "2" }
local SET_FIELD = { hun = "nH", thr = "nT", tir = "nF", tru = "tr" }

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
-- ganze Baer stuende. B.SleepWakeMs ist ihre letzte Funktion. Nur Tabellen-Lesen.
local function rulesOk()
    return B.NeedOf ~= nil and B.NeedsPct ~= nil and B.MealPct ~= nil and B.TrustGain ~= nil and B.TrustDayClose ~= nil
        and B.SleepWakeMs ~= nil
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

-- ---------------------------------------------------------------------------
-- Migration und Klemmen (PLAN_F3.md 7). Nur gezaehmt/vermisst; an jedem anderen Zustand sind alle F3-Felder nil. Fehlt ein Wert
-- (eben gezaehmt, Baer von vor F3, Spiegel ohne F3-Felder), bekommt er den Erst-Wert: Hunger 20, Durst 20, Muedigkeit 10, Vertrauen 50
-- (kein Baer startet hungrig). Die Werte bleiben ungerundet (kleine Schritte je Takt), nur die Sicht rundet.
-- ---------------------------------------------------------------------------
local function fixVal(v, def)
    local n = num(v)
    if n == nil then n = def end
    return clamp(n, 0, 100)
end

local function fixHist(v)
    if type(v) ~= "string" then return nil end
    local n = string.len(v)
    if n == 0 then return nil end
    if n > 3 then
        v = string.sub(v, n - 2, n)
        n = 3
    end
    for i = 1, n do
        local ch = string.sub(v, i, i)
        if ch ~= "0" and ch ~= "1" and ch ~= "2" then return nil end
    end
    return v
end

function B.NeedsFix(rec, now)
    if type(rec) ~= "table" or not rulesOk() then return end
    if not isTame(rec.st) then
        for i = 1, #FIELDS do rec[FIELDS[i]] = nil end
        return
    end
    rec.nH = fixVal(rec.nH, cfg("needStartHun", 20))
    rec.nT = fixVal(rec.nT, cfg("needStartThr", 20))
    rec.nF = fixVal(rec.nF, cfg("needStartTir", 10))
    rec.tr = fixVal(rec.tr, cfg("trStart", 50))
    local d = rec.nDay
    if type(d) ~= "table" then
        d = {}
        rec.nDay = d
    end
    local day = math.floor((num(now) or B.Now()) / 24)
    d.d = math.floor(num(d.d) or day)
    d.h = clamp(num(d.h) or 0, 0, 100)
    d.t = clamp(num(d.t) or 0, 0, 100)
    d.s = clamp(num(d.s) or 0, 0, 24)
    d.a = clamp(math.floor(num(d.a) or 0), 0, 99)
    d.c = clamp(num(d.c) or 0, 0, 24)
    d.p = clamp(num(d.p) or 0, 0, 100)
    if not HAND[d.l] then d.l = nil end
    rec.trD = fixHist(rec.trD)
    rec.slpAt = num(rec.slpAt)
end

-- ---------------------------------------------------------------------------
-- Vertrauen setzen (die EINE Stelle): klemmen, Meldungen beim Ueberschreiten -- trHeart nach oben (das Herz erscheint, Kevin 13.11.
-- Antwort 7), trRefuse nach unten ("weigert sich zu kaempfen ... und das steht dann da auch", Antwort 4) bzw. wieder nach oben; die
-- zwei Kampf-Meldungen nur am kampffaehigen Baeren. Sicht bei jeder Aenderung.
-- ---------------------------------------------------------------------------
local function trustSet(rec, v, players)
    local old = num(rec.tr) or cfg("trStart", 50)
    local new = clamp(num(v) or old, 0, 100)
    rec.tr = new
    if new == old then return end
    local refuse, heart = cfg("trRefuse", 15), cfg("trHeart", 100)
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
end

-- Neuer Spieltag? Dann den alten abschliessen (B.TrustDayClose: Aenderung und Kennziffer fuer den Verlauf, hoechstens drei Tage) und
-- neu beginnen. Die letzte Handlung (Mischbonus) bleibt.
-- Nachbesserung C9: laeuft gerade ein Schlaf ueber Mitternacht, nimmt der neue Tag dessen bisherige Stunden mit (slp.hrs,
-- server/BanditsNPCBearSleep.lua B.SleepDrain) -- aber nur, wenn der alte Tag den Schlaf-Bonus (trSleepH, 6 Stunden) nicht schon selbst
-- erreicht hat (kein Bonus zweimal fuer denselben Schlaf). So gibt ein Schlaf von 20 bis 4 Uhr den Bonus am zweiten Tag.
local function dayRoll(rec, now, needsOn, players)
    local d = rec.nDay
    local day = math.floor(now / 24)
    if d.d == day then return end
    local keep = 0
    if day == d.d + 1 and (num(d.s) or 0) < cfg("trSleepH", 6) then
        local s = B._s and B._s[rec.id] or nil
        local slp = type(s) == "table" and s.slp or nil
        if type(slp) == "table" and (slp.ph == "lie" or slp.ph == "sleep") then
            keep = num(slp.hrs) or 0
            if keep > (num(d.s) or 0) then keep = num(d.s) or 0 end
        end
    end
    if day > d.d then
        local delta, code = B.TrustDayClose(d, needsOn)
        if delta ~= nil then
            local hist = (rec.trD or "") .. (CODE[code] or "0")
            local n = string.len(hist)
            if n > 3 then hist = string.sub(hist, n - 2, n) end
            rec.trD = hist
            B.Log("trust: " .. tostring(rec.id) .. " day " .. tostring(d.d) .. " closed (hunger " .. tostring(B.Round1(d.h))
                .. ", thirst " .. tostring(B.Round1(d.t)) .. ", slept " .. tostring(B.Round1(d.s)) .. " h) -> "
                .. tostring(delta))
            if delta ~= 0 then trustSet(rec, rec.tr + delta, players) end
            B.Touch(rec)
        end
    end
    rec.nDay = { d = day, h = 0, t = 0, s = keep, a = 0, c = 0, p = 0, l = d.l }
end

-- ---------------------------------------------------------------------------
-- Vertrauen aus der Hand und aus Ereignissen (PLAN_F3.md 4.1). kind = "feed" (class = Futterklasse) / "pet" / "drink": Punkte nach
-- B.TrustGain (Mischbonus im Wechsel, Tagesdeckel trHandDay); kind = "down": am Boden, sofort trDown (-5). Rueckgabe: Aenderung.
-- Festschreiben tut der Aufrufer (B.Commit).
-- ---------------------------------------------------------------------------
function B.TrustAdd(rec, kind, class, now, players)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return 0 end
    now = num(now) or B.Now()
    B.NeedsFix(rec, now)
    if kind == "down" then
        local delta = cfg("trDown", -5)
        trustSet(rec, rec.tr + delta, players)
        return delta
    end
    if not HAND[kind] then return 0 end
    dayRoll(rec, now, B.NeedsOn(), players)
    local d = rec.nDay
    local pts, _ = B.TrustGain(kind, class, d.l, d.p)
    d.l = kind
    if pts > 0 then
        d.p = d.p + pts
        trustSet(rec, rec.tr + pts, players)
    end
    return pts
end

-- ---------------------------------------------------------------------------
-- Fressen und Trinken: die Schnittstelle fuer F4 / F5 (frisst aus dem Inventar, Fische, trinkt selbst). meals = Mahlzeiten (B.MealsOf),
-- bowls = Schalen (Liter / bowlL). Was unter 0 ginge, verfaellt (kein Vorrat). Rueckgabe: der neue Wert. Festschreiben: der Aufrufer.
-- ---------------------------------------------------------------------------
function B.NeedEat(rec, meals, why)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return nil end
    B.NeedsFix(rec, B.Now())
    local m = num(meals) or 0
    if m < 0 then m = 0 end
    local was = rec.nH
    rec.nH = clamp(was - m * B.MealPct(rec), 0, 100)
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
    rec.nT = clamp(was - b * B.BowlPct(rec), 0, 100)
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
    -- ab hier wird genommen: EIN Aufruf, danach im selben Lua-Aufruf gutschreiben, ohne Engine-Aufruf dazwischen
    fc:removeFluid(take, false)
    if B.SleepStop then B.SleepStop(rec, "hand") end
    B.NeedDrink(rec, take / bowlL, "hand")
    B.TrustAdd(rec, "drink", nil, now)
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
-- Zaehlen die Beduerfnisse dieses Eintrags gerade? (PLAN_F3.md 2.1) Nur gezaehmt, Besitzer im Spiel, und mit Koerper in der Welt oder
-- mitfahrend. Vermisst / entladen / Besitzer abgemeldet: eingefroren (Kevins Wahl "Einfrieren" bei der Crew, 11.10.).
-- ---------------------------------------------------------------------------
local function counts(rec, online)
    if rec.st ~= "tame" or rec.owner == nil then return false end
    if type(online) ~= "table" or online[rec.owner] ~= true then return false end
    if rec.ride ~= nil then return true end
    return B.FindAnimal(rec) ~= nil
end

-- ---------------------------------------------------------------------------
-- Je Langsam-Takt (10 Spielminuten; dt = Spielstunden seit dem letzten Takt, vom Aufrufer auf maxDtH gedeckelt). Eigene Schleife NACH
-- B.GrowSlow (ein Fehler hier reisst Wachsen und Heilen nicht mit). Schritte: klemmen -> zaehlt er? -> Tagesabschluss (Vertrauen) ->
-- Anstieg Hunger / Durst (x Tempo x Vertrauens-Faktor; auch im Schlaf) -> Muedigkeit (wach: Tempo der Groesse + Anstrengung aus der
-- Sitzung s.tirAcc; im Schlaf der Abbau, B.SleepDrain) -> Leben bei 100 -> Meldungen -> Sicht (ab needViewStep Punkten oder bei einem
-- Stufenwechsel) -> Spiegel (ueber s.gDirty mit dem naechsten Wachstums-Commit, sofort bei einem Stufenwechsel).
-- ---------------------------------------------------------------------------
function B.NeedsSlow(rec, dt, online, now, players)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return end
    now = num(now) or B.Now()
    B.NeedsFix(rec, now)
    if not counts(rec, online) then return end
    dt = num(dt) or 0
    if dt < 0 then dt = 0 end
    local s = B.Ses(rec.id)
    local pct = B.NeedsPct()
    local on = pct > 0
    dayRoll(rec, now, on, players)
    local d = rec.nDay
    d.c = clamp(d.c + dt, 0, 24)
    local hp0 = rec.hp
    if not on then
        -- Sandbox 0: alle drei aus und auf 0 gehalten (Muster NPC Crew shared/BanditsNPCNeeds.lua, NeedsRateMult 0)
        rec.nH, rec.nT, rec.nF = 0, 0, 0
        s.tirAcc = nil
    else
        local k = pct / 100 * B.TrustK(rec)
        rec.nH = clamp(rec.nH + cfg("needHunDay", 50) / 24 * k * dt, 0, 100)
        rec.nT = clamp(rec.nT + cfg("needThrDay", 75) / 24 * k * dt, 0, 100)
        local slp = s.slp
        if type(slp) == "table" and (slp.ph == "lie" or slp.ph == "sleep") then
            -- im Schlaf steigt die Muedigkeit nicht -- der Abbau ist ihre ganze Uhr (wie bei den NPC-Crew-Figuren)
            if B.SleepDrain then B.SleepDrain(rec, s, now) end
        else
            local add = B.TirRate(rec) * k * dt
            local acc = num(s.tirAcc) or 0
            if acc > 0 and B.StatsOf ~= nil then
                local staMax = num(B.StatsOf(rec).staMax) or 1
                if staMax <= 0 then staMax = 1 end
                add = add + acc / staMax * cfg("tirPerBar", 3) * k
            end
            rec.nF = clamp(rec.nF + add, 0, 100)
        end
        s.tirAcc = nil
        if rec.nH > d.h then d.h = rec.nH end
        if rec.nT > d.t then d.t = rec.nT end
        -- Leben bei Hunger / Durst 100 (Kevin 13.11. Antwort 6a): bis needHpFloor (1 %), nie Tod, nie am Boden. Nicht am Boden (er ist
        -- schon hilflos) und nicht, solange das Leben noch nie abgeglichen wurde (mitfahrend seit dem Laden). B.BodyHurt ist die EINE
        -- Stelle, an der das Register-Leben sinkt (server/BanditsNPCBearGrow.lua; geht auch ohne Koerper) -- kein B.OnHitTaken.
        local rate = 0
        if rec.nH >= 100 then rate = rate + cfg("needHpHun", 2) end
        if rec.nT >= 100 then rate = rate + cfg("needHpThr", 3) end
        if rate > 0 and dt > 0 and rec.down == nil and B.BodyHurt ~= nil then
            local a = B.FindAnimal(rec)
            if a ~= nil and B.BodyHp ~= nil then B.BodyHp(rec, a, 0) end
            local hp = num(rec.hp)
            if hp ~= nil then
                local frac = rate / 100 * dt
                local room = hp - cfg("needHpFloor", 0.01)
                if frac > room then frac = room end
                if frac > 0 then B.BodyHurt(rec, a, frac) end
            end
        end
    end
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
    if stepped then B.Commit(rec) end
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_F3.md 7; schnittstelle.md K2) -- aus viewEntry, nur gezaehmt/vermisst, fuer eigene UND fremde Baeren; schreibt nur in t:
-- hun / thr / tir / tru (ganze Zahlen 0..100, abgerundet), trM (Vertrauen ab trHeart: das Herz ueber dem Namensschild, Kevin 13.11.
-- Antwort 7), nof ("trust" / "tired": er kaempft gerade nicht -- nur am kampffaehigen Baeren), trW (Verlauf der letzten drei Tage als
-- Ziffern-Text), meal / bowl (so viele Punkte senkt eine Mahlzeit / eine Schale bei dieser Groesse, auf 0,1).
-- ---------------------------------------------------------------------------
function B.NeedsView(rec, t)
    if type(rec) ~= "table" or type(t) ~= "table" or not isTame(rec.st) or not rulesOk() then return end
    local h, th, f, tr = B.NeedOf(rec, "hun"), B.NeedOf(rec, "thr"), B.NeedOf(rec, "tir"), B.NeedOf(rec, "tru")
    if h ~= nil then t.hun = whole(h) end
    if th ~= nil then t.thr = whole(th) end
    if f ~= nil then t.tir = whole(f) end
    if tr ~= nil then
        t.tru = whole(tr)
        if tr >= cfg("trHeart", 100) then t.trM = true end
    end
    if rec.st == "tame" and fights(rec) then t.nof = B.NoFight(rec) end
    if type(rec.trD) == "string" and rec.trD ~= "" then t.trW = rec.trD end
    t.meal = B.Round1(B.MealPct(rec))
    t.bowl = B.Round1(B.BowlPct(rec))
end

-- ---------------------------------------------------------------------------
-- Aus dem Spiegel (server/BanditsNPCBearHeal.lua B.Restore / B.TakeNewerMark, nur fuer einen gezaehmten Eintrag): die vier Werte
-- geklemmt uebernehmen (Unsinn -> Erst-Wert), Verlauf und Tagesbuch beginnen neu (nicht im Spiegel -- harmlos).
-- ---------------------------------------------------------------------------
function B.NeedsFromMark(rec, mark, now)
    if type(rec) ~= "table" or type(mark) ~= "table" then return end
    rec.nH, rec.nT, rec.nF, rec.tr = mark.nH, mark.nT, mark.nF, mark.tr
    rec.nDay, rec.trD, rec.slpAt = nil, nil, nil
    B.NeedsFix(rec, now)
end

-- ---------------------------------------------------------------------------
-- Von Hand (Probeweg der Test-Mod zum Setzen der vier Werte -- im Spiel nie gerufen, das Uebernahme-Skript prueft das: Regel probeweg).
-- k = "hun" / "thr" / "tir" / "tru", v = 0..100. Vertrauen ueber die EINE Setz-Stelle (Meldungen wie im Spiel).
-- Rueckgabe: der gesetzte Wert oder nil.
-- ---------------------------------------------------------------------------
function B.NeedsSet(rec, k, v)
    local field = SET_FIELD[k]
    local n = num(v)
    if type(rec) ~= "table" or not isTame(rec.st) or field == nil or n == nil or not rulesOk() then return nil end
    B.NeedsFix(rec, B.Now())
    n = clamp(n, 0, 100)
    if field == "tr" then
        trustSet(rec, n, nil)
    else
        rec[field] = n
    end
    B.Commit(rec)
    return n
end
