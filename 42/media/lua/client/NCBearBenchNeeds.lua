--
-- NUR TESTHILFE fuer Beduerfnisse, Vertrauen und Schlafen (F3, Lauf baer-f3, PLAN_F3.md 13). Wird NIE nach NPC Crew kopiert (NCBearBench*).
-- Kein Kern-Code ruft diese Datei; sie ruft dieselben Kern-Funktionen wie das echte Spiel (BanditsNPC.Bear) und den EINEN Probeweg des
-- Kerns B.NeedsSet (im Spiel nie gerufen, Tier-Regel "probeweg" des Uebernahme-Skripts).
-- NUR EINZELSPIELER ("not isServer() and not isClient()"): im Mehrspieler sagt jeder Befehl "singleplayer only". Die zwei z Z z-Regler
-- sind reine Anzeige und gehen ueberall.
--
-- Konsole:
--   NCBear_CubNeeds(h, t, f, tr)  Hunger, Durst, Muedigkeit, Vertrauen meines naechsten zahmen Baeren setzen (je 0..100, nil = lassen),
--                                 z. B. NCBear_CubNeeds(85) = ausgehungert, NCBear_CubNeeds(nil, nil, 92) = zu muede zum Kaempfen,
--                                 NCBear_CubNeeds(nil, nil, nil, 100) = volles Vertrauen (Herz), NCBear_CubNeeds(nil, nil, nil, 10) =
--                                 er weigert sich zu kaempfen. Danach ein Hirn-Takt und eine Zeile.
--   NCBear_CubSleep()             Muedigkeit auf 100: er schlaeft nach den ECHTEN Regeln von selbst ein (nie bei Gefahr, im Kampf, in
--                                 einer Sperre -- dann sagt die Zeile, warum nicht) und dreht sich zur Kamera
--   NCBear_CubWake()              derselbe Modus noch einmal = ein Befehl weckt ihn (Bitte "Mode" wie der Knopf im Fenster)
--   NCBear_CubNeedsInfo()         Werte, Woerter, Faktoren (B.NeedK, B.TrustK), kaempft-nicht-Grund, Schlafzustand (B.SleepInfo),
--                                 Verlauf der Tage, dazu der Sicht-Eintrag (hun thr tir tru slp slpO wka fsy nof trM trW) und das
--                                 Ruhebild dieses Clients (U.PosePhase, U.PoseSleeping, z Z z)
--   NCBear_ZzLift(px)             z Z z um px Pixel hoeher (negativ: tiefer) ueber dem Schild-Stapel; ohne Wert: Vorgabe 4
--   NCBear_ZzHead(k)              Kopf-Vorlage des z Z z in Modell-Einheiten (0 = ueber der Tiermitte); ohne Wert: Wert des Kerns
--   Tempo testen: NCBear_CubSet("needHunDay", 500) (client/NCBearBenchCub.lua) bzw. den Sandbox-Regler "Bear: needs speed".
--   Leben setzen: NCBear_CubHurt(pct); Spielstunden ueberspringen: NCBear_CubSkip(h).
--
-- Engine-Aufrufe (Fundstelle): getSpecificPlayer(0) V:client/Farming/CFarmingSystem.lua:45; player:getX() / getY()
-- V:client/Fishing/TensionUI.lua:11; player:Say(Text) V:client/Entity/ISEntityUI.lua:458; animal:setDir(IsoDirections.SE) -- Form
-- V:shared/Definitions/animal/ButcheringUtil.lua:574 (dort IsoDirections.NE; gleiche Aufzaehlung); getTimestampMs()
-- V:client/Foraging/ISBaseIcon.lua:485.
-- Kern (zur Laufzeit, hinter Existenz-Riegeln): B.Reg, B.PlayerKey, B.IsSP, B.NeedsSet, B.NeedOf, B.NeedK, B.TrustK, B.NoFight,
-- B.NeedWord, B.TrustWord, B.SleepInfo, B.IsAsleep, B.BrainTick, B.PushView, B.FindAnimal, B.ModeOf, B.Ask, B.View; Oberflaeche:
-- B.UI.ZZ, B.UI.ZzPoke, B.UI.ZzInfo, B.UI.PosePhase, B.UI.PoseSleeping.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local KINDS = { "hun", "thr", "tir", "tru" }
local VIEW_FIELDS = { "hun", "thr", "tir", "tru", "slp", "slpO", "wka", "fst", "fsy", "nof", "trM", "trW", "meal", "bowl", "mdmgK" }

local function out(text)
    print("[NCBear] " .. tostring(text))
end

-- Kurze Rueckmeldung: Konsole und ueber der Figur.
local function say(text)
    out(text)
    local p = getSpecificPlayer(0)
    if p then p:Say(tostring(text)) end
end

-- Spieler, Schluessel, Register -- oder nil mit einer klaren Zeile (wie client/NCBearBenchCub.lua).
local function ready()
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return nil
    end
    if not B.IsSP or not B.Reg then
        out("the bear core is not loaded (BanditsNPCBear*.lua)")
        return nil
    end
    if not B.NeedsSet or not B.NeedOf then
        out("the bear core has no needs (BanditsNPCBearNeedRules.lua / BanditsNPCBearNeeds.lua not loaded)")
        return nil
    end
    local p = getSpecificPlayer(0)
    if not p then
        out("no player yet")
        return nil
    end
    local reg = B.Reg()
    if not reg then
        out("registry not ready yet (load a game first)")
        return nil
    end
    return p, B.PlayerKey(p), reg
end

-- Mein naechster gezaehmter Baer (Eintrag im Register), gleich wie weit weg.
local function myTame(p, key, reg)
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        if rec.st == "tame" and rec.owner == key then
            local dx = (tonumber(rec.x) or 0) - p:getX()
            local dy = (tonumber(rec.y) or 0) - p:getY()
            local d = dx * dx + dy * dy
            if bestD == nil or d < bestD then best, bestD = rec, d end
        end
    end
    return best
end

local function myRec()
    local p, key, reg = ready()
    if not p then return nil end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed bear of yours (NCBear_CubTame(100) first)")
        return nil
    end
    return rec, p
end

local function fix(v, d)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%." .. tostring(d or 1) .. "f", v)
end

-- Eine Zeile: die vier Werte, der Grund "kaempft nicht" und ob er schlaeft.
local function needsLine(rec)
    local parts = {}
    for i = 1, #KINDS do parts[#parts + 1] = KINDS[i] .. " " .. fix(B.NeedOf(rec, KINDS[i])) end
    local line = "bear " .. tostring(rec.id) .. ": " .. table.concat(parts, ", ")
    if B.NoFight then line = line .. ", no-fight " .. tostring(B.NoFight(rec)) end
    if B.SleepInfo then
        local si = B.SleepInfo(rec, getTimestampMs())
        line = line .. ", sleep " .. tostring(si.ph)
        if si.lockMs then line = line .. " (locked " .. fix(si.lockMs / 1000, 0) .. " s)" end
    end
    return line
end

local function tick(p)
    if B.BrainTick then B.BrainTick(true) end
    if B.PushView then B.PushView(p) end
end

-- ---------------------------------------------------------------------------
-- Befehle
-- ---------------------------------------------------------------------------

function NCBear_CubNeeds(h, t, f, tr)
    local rec, p = myRec()
    if not rec then return end
    local vals = { h, t, f, tr }
    for i = 1, #KINDS do
        if vals[i] ~= nil then
            local got = B.NeedsSet(rec, KINDS[i], tonumber(vals[i]))
            if got == nil then out("could not set " .. KINDS[i] .. " to " .. tostring(vals[i])) end
        end
    end
    tick(p)
    say(needsLine(rec))
end

function NCBear_CubSleep()
    local rec, p = myRec()
    if not rec then return end
    B.NeedsSet(rec, "tir", 100)
    tick(p)
    -- zur Kamera drehen, damit man das Schlafbild von vorn sieht (nur, wenn der Koerper geladen ist)
    local a = nil
    if B.FindAnimal then a = B.FindAnimal(rec) end
    if a then a:setDir(IsoDirections.SE) end
    local asleep = B.IsLying and B.IsLying(rec)
    if asleep then
        say(needsLine(rec) .. " -- lying down")
    else
        say(needsLine(rec) .. " -- NOT asleep yet (danger near, fight, riding, down or a lock; it lies down as soon as the rules allow)")
    end
end

function NCBear_CubWake()
    local rec, p = myRec()
    if not rec then return end
    local mode = "stay"
    if B.ModeOf then mode = B.ModeOf(rec) end
    B.Ask(p, "Mode", { id = rec.id, mode = mode })
    tick(p)
    say(needsLine(rec) .. " -- order '" .. tostring(mode) .. "' sent again (any order wakes it)")
end

function NCBear_CubNeedsInfo()
    local rec, p = myRec()
    if not rec then return end
    out(needsLine(rec))
    local words = {}
    for i = 1, 3 do
        local v = B.NeedOf(rec, KINDS[i])
        if v ~= nil and B.NeedWord then words[#words + 1] = KINDS[i] .. " level " .. tostring(B.NeedWord(KINDS[i], v)) end
    end
    local tr = B.NeedOf(rec, "tru")
    if tr ~= nil and B.TrustWord then words[#words + 1] = "tru level " .. tostring(B.TrustWord(tr)) end
    out("  words: " .. table.concat(words, ", "))
    if B.NeedK then
        local k = B.NeedK(rec)
        out("  factors: stamina x" .. fix(k.sta, 2) .. ", damage x" .. fix(k.dmg, 2) .. ", growth x" .. fix(k.grow, 2) .. ", healing x"
            .. fix(k.heal, 2) .. "; needs speed from trust x" .. fix(B.TrustK and B.TrustK(rec) or nil, 2)
            .. "; needs on: " .. tostring(B.NeedsOn and B.NeedsOn()))
    end
    if B.SleepInfo then
        local si = B.SleepInfo(rec, getTimestampMs())
        out("  sleep: phase " .. tostring(si.ph) .. ", why " .. tostring(si.why) .. ", slept ms " .. tostring(si.sleptMs) .. ", lock ms "
            .. tostring(si.lockMs) .. ", drowsy ms " .. tostring(si.wokeMs) .. ", getting up ms " .. tostring(si.wakeMs) .. ", owner asleep "
            .. tostring(si.ownerAsleep))
    end
    out("  history (oldest day first, 0 good / 1 hungry or thirsty / 2 starving or parched): " .. tostring(rec.trD))
    -- Sicht-Eintrag (was das Fenster und die Anzeige ueber dem Baeren lesen) und das Ruhebild dieses Clients
    local v = B.View and B.View.cubs and B.View.cubs[rec.id] or nil
    if type(v) == "table" then
        local parts = {}
        for i = 1, #VIEW_FIELDS do
            local f = VIEW_FIELDS[i]
            if v[f] ~= nil then parts[#parts + 1] = f .. "=" .. tostring(v[f]) end
        end
        out("  view: " .. table.concat(parts, " "))
    else
        out("  view: no entry yet")
    end
    local U = B.UI
    if U then
        local n = nil
        if U.ZzInfo then n = U.ZzInfo() end                     -- Mehrfachrueckgabe: nur der erste Wert
        out("  pose: phase " .. tostring(U.PosePhase and U.PosePhase(rec.id)) .. ", sleep loop "
            .. tostring(U.PoseSleeping and U.PoseSleeping(rec.id)) .. ", z Z z drawn for " .. tostring(n) .. " bear(s); z Z z lift "
            .. tostring(U.ZZ and U.ZZ.lift) .. ", head " .. tostring(U.ZZ and U.ZZ.head))
    end
    say("needs info printed to the console")
end

-- z Z z-Regler (reine Anzeige dieses Rechners; gilt bis zum Spielende). Ohne Wert: zurueck auf die Vorgabe.
function NCBear_ZzLift(px)
    local U = B.UI
    if not U or not U.ZZ then
        out("the z Z z display is not loaded (client/ISUI/BanditsNPCBearZz.lua)")
        return
    end
    U.ZZ.lift = tonumber(px) or 4
    if U.ZzPoke then U.ZzPoke() end
    say("z Z z lift " .. tostring(U.ZZ.lift) .. " px above the name tag stack")
end

function NCBear_ZzHead(k)
    local U = B.UI
    if not U or not U.ZZ then
        out("the z Z z display is not loaded (client/ISUI/BanditsNPCBearZz.lua)")
        return
    end
    U.ZZ.head = tonumber(k)
    if U.ZzPoke then U.ZzPoke() end
    say("z Z z head offset " .. tostring(U.ZZ.head) .. " (nil = core value, 0 = above the middle of the bear)")
end
