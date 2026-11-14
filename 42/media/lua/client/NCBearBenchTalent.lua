--
-- NUR TESTHILFE fuer die Talente (Lauf baer-talente, baer/plaene/PLAN_TALENTE.md 10). Wird NIE nach NPC Crew kopiert (NCBearBench*).
-- Kein Kern-Code ruft diese Datei; sie ruft dieselben Kern-Funktionen wie das echte Spiel (BanditsNPC.Bear: die Bitten "Talent" /
-- "TalentReset" ueber B.Ask, wie der Reiter "Talente" nach dem Ja) und die ZWEI Probewege des Kerns B.TalentForce / B.TalentWipe (im Spiel nie
-- gerufen, Tier-Regel "probeweg" des Uebernahme-Skripts).
-- NUR EINZELSPIELER ("not isServer() and not isClient()"): im Mehrspieler sagt jeder Befehl "singleplayer only".
--
-- Konsole:
--   NCBear_TalentInfo()        Punkte (verdient / gelernt / frei, Tage bis zum naechsten), je Talent der Zustand (B.TalentCan) und die Werte, die
--                              es aendert (Leben, Ausdauer, Traglast, Hunger-Anstieg, Heilen, Liegezeit, Wachsam-Weiten, Krit, Pranke), die Reset-
--                              Uhr und die Sandbox; vorher ein Langsam-Schritt der Talente (B.TalentSlow: eine faellige Punkt-Meldung kommt sofort)
--   NCBear_TalentLearn("crit") ein Talent lernen -- derselbe Weg wie Ja im Fenster (alle Pruefungen des Schreibers)
--   NCBear_TalentReset()       alle zuruecksetzen -- derselbe Weg wie der Knopf (Sandbox, Abstand)
--   NCBear_TalentForce("alert,paw")  Talente OHNE Punkte setzen (bereinigt, hoechstens 3) -- Probeweg B.TalentForce
--   NCBear_TalentWipe()        alle weg OHNE Sandbox und Uhr (auch die Reset-Uhr) -- Probeweg B.TalentWipe
--   Dazu: NCBear_CubGrow(tage) (client/NCBearBenchCub.lua) fuer die Punkte (10 % / halbstark / ausgewachsen), NCBear_FightLog(true)
--   (client/NCBearBenchFight.lua) fuer die Zeilen "critical hit".
--
-- Engine-Aufrufe (Fundstelle): getSpecificPlayer(0) V:client/Farming/CFarmingSystem.lua:45; player:Say(Text) V:client/Entity/ISEntityUI.lua:458;
-- player:getX() / getY() V:client/Fishing/TensionUI.lua:11. Kern zur Laufzeit hinter Existenz-Riegeln. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function out(text)
    print("[NCBear] " .. tostring(text))
end

local function say(text)
    out(text)
    local p = getSpecificPlayer(0)
    if p then p:Say(tostring(text)) end
end

local function f1(v)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%.1f", v)
end

-- Spieler, Schluessel, mein naechster zahmer Baer -- oder nil mit einer Zeile.
local function mine()
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return nil
    end
    if not B.Reg or not B.TalentList or not B.HandleTalent or not B.StatsOf then
        out("the bear core has no perks (BanditsNPCBearTalentRules.lua / BanditsNPCBearTalent.lua not loaded)")
        return nil
    end
    local p = getSpecificPlayer(0)
    local reg = B.Reg()
    if not p or not reg then
        out("no player or registry yet (load a game first)")
        return nil
    end
    local key = B.PlayerKey(p)
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        if rec.st == "tame" and rec.owner == key then
            local dx = (tonumber(rec.x) or 0) - p:getX()
            local dy = (tonumber(rec.y) or 0) - p:getY()
            local d = dx * dx + dy * dy
            if bestD == nil or d < bestD then best, bestD = rec, d end
        end
    end
    if not best then
        say("no tamed bear of yours (NCBear_CubTame(100) first)")
        return nil
    end
    return best, p
end

function NCBear_TalentInfo()
    local rec = mine()
    if not rec then return end
    if B.TalentSlow and B.Players then B.TalentSlow(rec, B.Now(), B.Players()) end
    local list = B.TalentList(rec)
    out("perks of " .. tostring(rec.id) .. ": learned " .. tostring(table.concat(list, ",")) .. " (" .. tostring(#list) .. "), earned "
        .. tostring(B.TalentEarned(rec)) .. ", free " .. tostring(B.TalentFree(rec)) .. ", g " .. f1((tonumber(rec.g) or 0) * 100)
        .. " %, next point in " .. tostring(B.TalentNextDays and B.TalentNextDays(rec)) .. " day(s), told " .. tostring(rec.talN))
    for i = 1, #B.TALENTS do
        local k = B.TALENTS[i]
        local ok, why = B.TalentCan(rec, k)
        local st = "free"
        if not ok then st = tostring(why) end
        if B.TalentOn(rec, k) then st = "ACTIVE" end
        out("  " .. tostring(i) .. " " .. k .. ": " .. st)
    end
    local s = B.StatsOf(rec)
    local c = B.CFG or {}
    out("  health max " .. f1(s.hpMax) .. ", stamina max " .. f1(s.staMax) .. ", carry cap " .. f1(B.InvCap and B.InvCap(rec)) .. " kg")
    out("  hunger/thirst rise x " .. f1(B.TalentK(rec, "frugal", "talFrugalK", 1) * 100) .. " %, stamina regen x "
        .. f1(B.TalentK(rec, "stamina", "talStaRegK", 1)) .. ", self-heal x " .. f1(B.TalentK(rec, "tough", "talHealK", 1))
        .. ", down hours " .. f1(B.DownHours(rec)))
    local ak = B.TalentK(rec, "alert", "talAlertK", 1)
    out("  alert x " .. f1(ak) .. ": fight " .. f1((tonumber(c.fightRadius) or 10) * ak) .. " / " .. f1((tonumber(c.fightBanditRadius) or 12) * ak)
        .. ", wake " .. f1((tonumber(c.sleepWakeR) or 8) * ak) .. ", hide " .. f1((tonumber(c.zedHide) or 6) * ak) .. " (capped at zedSense "
        .. tostring(c.zedSense) .. "), never groggy " .. tostring(B.TalentOn(rec, "alert")))
    out("  crit " .. tostring(B.TalentOn(rec, "crit")) .. " (" .. tostring(c.talCritPct) .. " % x " .. tostring(c.talCritK) .. "), paw knock "
        .. f1(B.TalentK(rec, "paw", "talPawKnock", 0)) .. " %, fly x " .. f1(B.TalentK(rec, "paw", "talPawPush", 1)) .. ", fish x "
        .. f1(B.TalentK(rec, "fisher", "talFishK", 1)) .. " (open " .. tostring(c.talFishOn) .. ")")
    local days = B.Opt("BearTalentResetDays")
    out("  reset allowed " .. tostring(B.Opt("BearTalentReset")) .. ", days " .. tostring(days) .. ", last reset day " .. tostring(rec.talR)
        .. ", wait " .. f1(B.TalentResetLeft(rec, B.Now(), days)) .. " h (today " .. tostring(math.floor(B.Now() / 24)) .. ")")
    say("perks: " .. tostring(#list) .. " learned, " .. tostring(B.TalentFree(rec)) .. " free (console)")
end

function NCBear_TalentLearn(k)
    local rec, p = mine()
    if not rec then return end
    B.Ask(p, "Talent", { id = rec.id, k = tostring(k) })
    say("perk request " .. tostring(k) .. " -> learned now: " .. tostring(table.concat(B.TalentList(rec), ",")))
end

function NCBear_TalentReset()
    local rec, p = mine()
    if not rec then return end
    B.Ask(p, "TalentReset", { id = rec.id })
    say("perk reset request -> learned now: " .. tostring(table.concat(B.TalentList(rec), ",")))
end

function NCBear_TalentForce(text)
    local rec, p = mine()
    if not rec or not B.TalentForce then return end
    local got = B.TalentForce(rec, text)
    if B.PushView then B.PushView(p) end
    say("perks forced: " .. tostring(got))
end

function NCBear_TalentWipe()
    local rec, p = mine()
    if not rec or not B.TalentWipe then return end
    B.TalentWipe(rec)
    if B.PushView then B.PushView(p) end
    say("perks wiped (no sandbox, no clock)")
end
