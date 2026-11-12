--
-- NUR TESTHILFE fuer den Kampf (F2 = B5a, Lauf baer-f2, PLAN_F2.md 4.6). Wird NIE nach NPC Crew kopiert (NCBearBench*, BENCH_ANY).
-- Frueher die Test-Teile von shared/NCBearFight.lua (NCBear_Fight / NCBear_Tune / NCBear_FightInfo, forceNext); die alte Datei ist ein Stummel.
-- NUR EINZELSPIELER ("not isServer() and not isClient()"): im Mehrspieler sagt jeder Befehl "singleplayer only". Gekaempft wird mit DEINEM
-- gezaehmten Baeren (die Test-Art ncbear kaempft nicht mehr, Frage F-G5); alles Laufen, Beissen und Schlagen macht der Kern selbst --
-- diese Datei stellt nur Zombies hin, druckt, stellt Stellwerte und erzwingt den naechsten Angriff (B.FightForce, nur Werkbank).
--
-- Konsole:
--   NCBear_FightZed(n, dist)  n Zombies (1..12, Vorgabe 1) dist Kacheln (2..20, Vorgabe 5) hinter DEINEM Baeren (von dir aus gesehen), damit
--                             sie ihm naeher sind als dir (sonst gehoeren sie Vanilla, PLAN_F2.md 2.1.2 Nr. 2)
--   NCBear_FightLog(on)       Kampf-/Diagnose-Zeilen [TC-BEAR] an/aus (B.LogOn)
--   NCBear_FightInfo()        Kampf deines Baeren: Phase, Ziel, gemerkte Gegner (B._foes), laufende Angriffe auf ihn (B._fa), Ausdauer,
--                             Leben, am Boden, Verband
--   NCBear_FightNext(name)    der naechste Angriff deines Baeren ist name (swipeL, swipeR, bite, maul, slam, rear), einmal (B.FightForce)
--   NCBear_FightDown()        deinen Baeren zu Boden werfen (B.BearDown) -- Aufhelfen / allein Aufstehen pruefen
--   NCBear_FightProbe()       15 s lang je 0,5 s: der naechste Zombie an deinem Baeren -- Abstand, Biss-Weite (B.FoeReach), Zustand,
--                             BumpType, Ziel, liegt, nutzlos (FG L1/L2). Ein zweiter Aufruf bricht ab.
--   NCBear_Fight()            sagt, wie man heute kaempft (der Test-Baer kaempft nicht mehr)
--   NCBear_Tune(feld, wert)   eine vorhandene ZAHL aus B.CFG setzen (z. B. "knockPush", "zBiteCdMs"); NCBear_Tune() listet die Kampf-Felder
--   Leben setzen: NCBear_CubHurt(pct) (client/NCBearBenchCub.lua). NCBear_ZHealth / NCBear_KnockInfo: client/NCBearBench.lua.
-- Rechtsklick (Untermenue "NC Bear"): "Fight: zombie next to my bear", "Fight: info", "Fight: knock my bear down".
--
-- Engine-Aufrufe (Fundstelle):
--   addZombiesInOutfit(x, y, z, n, nil, 50): V:client/DebugUIs/Scenarios/FenrisScenario.lua:544
--   getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45; player:getX()/getY()/getZ(): V:client/Fishing/TensionUI.lua:11
--   animal:getX()/getY()/getZ(): V:client/TimedActions/ISContextualActions.lua:100
--   getCell():getZombieList(), :size(), :get(i): B:client/BanditZombie.lua:110; z:getX()/getY(): B:client/BanditZombie.lua:69-71
--   z:getActionStateName(): B:client/BanditMenu.lua:161; z:getBumpType(): B:client/BanditUpdate.lua:1658; z:getTarget(): B:client/BanditMenu.lua:170
--   z:isOnFloor(): B:shared/BanditUtils.lua:362; z:isUseless(): B:client/BanditMenu.lua:152
--   getTimestampMs(): V:client/Foraging/ISBaseIcon.lua:485; Events.OnTick.Add: V:client/Chat/ISChat.lua:943
--   sub:addOption(Text, Ziel, Funktion): V:client/DebugUIs/AdminContextMenu.lua:46
-- Kern (zur Laufzeit, hinter Existenz-Riegeln): B.Reg, B._s, B._foes, B._fa, B.FindAnimal, B.StatsOf, B.FoeReach, B.FightForce, B.BearDown,
-- B.PushView, B.CFG, B.LogOn, B.PlayerKey, B.IsSP.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local PROBE_MS = 15000
local PROBE_STEP_MS = 500
local ZED_MAX = 12
local ATTACKS = { swipeL = true, swipeR = true, bite = true, maul = true, slam = true, rear = true }
-- Kampf-Felder fuer NCBear_Tune() (Anfang des Namens; B.CFG traegt sie, PLAN_F2.md 4.5)
local TUNE_HEAD = { "fight", "foe", "lure", "knock", "push", "swipe", "bite", "maul", "slam", "rear", "dmg", "w", "sta", "zBite", "bSmack",
    "down", "help", "mend", "flee", "huff", "hit", "side", "sight", "stand", "xpCon", "hpCommit" }

local function out(s)
    print("[NCBear] " .. tostring(s))
end

local function say(s)
    out(s)
    local p = getSpecificPlayer(0)                      -- V:client/Farming/CFarmingSystem.lua:45
    if p then p:Say(tostring(s)) end                    -- V:client/Entity/ISEntityUI.lua:458
end

local function sp()
    return not isServer() and not isClient()
end

-- Spieler, mein gezaehmter Eintrag (der naechste), sein Tier (oder nil) -- oder nil mit einer Zeile.
local function mine()
    if not sp() then
        out("singleplayer only")
        return nil
    end
    if not B.Reg or not B.PlayerKey then
        out("the bear core is not loaded (BanditsNPCBear*.lua)")
        return nil
    end
    local p = getSpecificPlayer(0)
    if not p then
        out("no player yet")
        return nil
    end
    local reg = B.Reg()
    if not reg or type(reg.cubs) ~= "table" then
        out("registry not ready yet (load a game first)")
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
        say("no tamed bear of yours (NCBear_CubHere() + NCBear_CubTame(100) first)")
        return nil
    end
    local a = B.FindAnimal and B.FindAnimal(best) or nil
    return p, best, a
end

local function fix(v, d)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%." .. tostring(d or 1) .. "f", v)
end

-- ---------------------------------------------------------------------------
-- Zombies hinstellen
-- ---------------------------------------------------------------------------
function NCBear_FightZed(n, dist)
    local p, rec, a = mine()
    if not p then return end
    if not a then
        say("your bear has no living body right now (riding, not loaded or missing)")
        return
    end
    n = math.floor(tonumber(n) or 1)
    if n < 1 then n = 1 end
    if n > ZED_MAX then n = ZED_MAX end
    dist = tonumber(dist) or 5
    if dist < 2 then dist = 2 end
    if dist > 20 then dist = 20 end
    local bx, by, bz = a:getX(), a:getY(), a:getZ()     -- V:client/TimedActions/ISContextualActions.lua:100
    local dx, dy = bx - p:getX(), by - p:getY()
    local len = math.sqrt(dx * dx + dy * dy)
    if len < 0.5 then dx, dy, len = 1, 0, 1 end         -- du stehst auf ihm: einfach nach Osten
    local zx = math.floor(bx + dx / len * dist)
    local zy = math.floor(by + dy / len * dist)
    addZombiesInOutfit(zx, zy, math.floor(bz), n, nil, 50)      -- V:client/DebugUIs/Scenarios/FenrisScenario.lua:544
    say(n .. " zombie(s) " .. fix(dist, 0) .. " tiles behind your bear (" .. zx .. "," .. zy .. ") -- they should walk to it and bite;"
        .. " NCBear_FightInfo() shows the fight")
end

function NCBear_FightLog(on)
    if not sp() then
        out("singleplayer only")
        return
    end
    if on == nil then on = not B.LogOn end
    B.LogOn = (on == true)
    out("fight / diagnosis lines [TC-BEAR] " .. (B.LogOn and "on" or "off"))
end

-- ---------------------------------------------------------------------------
-- Drucken
-- ---------------------------------------------------------------------------
local function foeLine(f)
    local o = f.o
    local alive = (o ~= nil) and o:isAlive()            -- B:client/BanditUpdate.lua:1087
    return tostring(f.kind) .. " oid " .. tostring(f.oid) .. " at " .. fix(f.d, 1) .. (alive and "" or " (dead)")
end

function NCBear_FightInfo()
    local p, rec, a = mine()
    if not p then return end
    local s = (B._s and B._s[rec.id]) or {}
    local st = B.StatsOf and B.StatsOf(rec) or {}
    local hp = tonumber(rec.hp)
    out("bear " .. tostring(rec.id) .. " (" .. tostring(rec.body) .. ", day " .. tostring(st.day) .. ", size " .. fix(st.s, 2) .. "): health "
        .. (hp and (fix(hp * 100, 0) .. "% = " .. fix(hp * (st.hpMax or 0), 0) .. " / " .. fix(st.hpMax, 0)) or "?")
        .. ", stamina " .. fix((tonumber(s.sta) or 1) * 100, 0) .. "%, passive " .. tostring(rec.passive == true)
        .. ", mode " .. tostring(rec.mode) .. ", body " .. (a and "loaded" or "none"))
    if rec.down ~= nil then
        out("  DOWN since hour " .. fix(rec.down, 1) .. " (now " .. fix(B.Now and B.Now() or 0, 1) .. ")")
    end
    if rec.bndH ~= nil then
        out("  bandaged until hour " .. fix(rec.bndH, 1) .. ", +" .. fix(rec.bndR, 1) .. " %/h")
    end
    local f = s.fight
    if type(f) == "table" then
        local t = f.tgt
        out("  fight: phase " .. tostring(f.ph) .. ", act " .. tostring(f.act) .. ", last " .. tostring(f.last)
            .. ", target " .. (type(t) == "table" and (tostring(t.kind) .. " oid " .. tostring(t.oid)) or "none")
            .. (f.resting and ", resting" or ""))
    else
        out("  no fight running" .. (B.FightState and (" (state " .. tostring(B.FightState(rec)) .. ")") or ""))
    end
    local foes = B._foes and B._foes[rec.id]
    if type(foes) == "table" and #foes > 0 then
        local parts = {}
        for i = 1, #foes do parts[#parts + 1] = foeLine(foes[i]) end
        out("  foes (" .. #foes .. "): " .. table.concat(parts, "; "))
    else
        out("  foes: none in range")
    end
    local fa = B._fa
    local n = 0
    if type(fa) == "table" then
        for i = 1, #fa do
            local e = fa[i]
            if e.id == rec.id then
                n = n + 1
                out("  attack on it: " .. tostring(e.kind) .. " oid " .. tostring(e.oid))
            end
        end
    end
    if n == 0 then out("  no attack on it running") end
end

function NCBear_FightNext(name)
    local p, rec = mine()
    if not p then return end
    if name == nil or not ATTACKS[name] then
        out("use NCBear_FightNext(name) with swipeL, swipeR, bite, maul, slam or rear")
        return
    end
    if not B.FightForce then
        out("B.FightForce is missing (server/BanditsNPCBearFight.lua not loaded)")
        return
    end
    local ok = B.FightForce(rec, name)
    say("next attack of your bear: " .. name .. (ok and " (once)" or " -- refused (not unlocked at this stage?)"))
end

function NCBear_FightDown()
    local p, rec, a = mine()
    if not p then return end
    if not B.BearDown then
        out("B.BearDown is missing (server/BanditsNPCBearHurt.lua not loaded)")
        return
    end
    if not a then
        say("your bear has no living body right now")
        return
    end
    B.BearDown(rec, a, "bench")
    if B.PushView then B.PushView(p) end
    -- Sandbox-Kuerzung (Lauf baer-aussehen): die Liegezeit ist der feste Wert B.CFG.downedHours (vorher Option BearDownedHours)
    say("your bear is down: right-click it \"Help up\" or wait (gets up alone after " .. tostring(B.CFG and B.CFG.downedHours)
        .. " in-game hours, NCBear_CubSet('downedHours', n))")
end

function NCBear_Fight()
    out("the test bear (NCBear_SpawnLive) no longer fights; use your tamed bear (NCBear_CubGrow(15) or more) and NCBear_FightZed(n, dist)")
end

-- ---------------------------------------------------------------------------
-- Stellwerte
-- ---------------------------------------------------------------------------
local function tuneWanted(name)
    for i = 1, #TUNE_HEAD do
        local h = TUNE_HEAD[i]
        if string.sub(name, 1, string.len(h)) == h then return true end
    end
    return false
end

function NCBear_Tune(field, value)
    if not sp() then
        out("singleplayer only")
        return
    end
    local cfg = B.CFG
    if type(cfg) ~= "table" then
        out("the bear core is not loaded")
        return
    end
    if field == nil then
        local names = {}
        for k, v in pairs(cfg) do
            if type(v) == "number" and tuneWanted(k) then names[#names + 1] = k .. "=" .. tostring(v) end
        end
        table.sort(names)
        local line = {}
        for i = 1, #names do
            line[#line + 1] = names[i]
            if #line >= 8 then
                out(table.concat(line, "  "))
                line = {}
            end
        end
        if #line > 0 then out(table.concat(line, "  ")) end
        out("NCBear_Tune(field, value) sets one of these numbers (every number of B.CFG works) until the game is closed")
        return
    end
    if type(cfg[field]) ~= "number" then
        out("NCBear_Tune: " .. tostring(field) .. " is not a number field of B.CFG (NCBear_Tune() lists them)")
        return
    end
    local v = tonumber(value)
    if v == nil then
        out(tostring(field) .. " = " .. tostring(cfg[field]))
        return
    end
    cfg[field] = v
    out(tostring(field) .. " = " .. tostring(v) .. " (until the game is closed)")
end

-- ---------------------------------------------------------------------------
-- Sonde: der naechste Zombie an deinem Baeren, 15 s
-- ---------------------------------------------------------------------------
local P = nil
local hooked = false

local function nearestZed(a)
    local list = getCell():getZombieList()              -- B:client/BanditZombie.lua:110
    local best, bd = nil, 15 * 15
    local ax, ay = a:getX(), a:getY()
    for i = 0, list:size() - 1 do
        local z = list:get(i)
        local dx, dy = z:getX() - ax, z:getY() - ay
        local d = dx * dx + dy * dy
        if d < bd then best, bd = z, d end
    end
    return best, math.sqrt(bd)
end

local function probeTick()
    if not P then return end
    local now = getTimestampMs()
    if now - P.t0 > PROBE_MS or now < P.t0 then
        out("probe: end (15 s)")
        P = nil
        return
    end
    if now - P.last < PROBE_STEP_MS then return end
    P.last = now
    local a = B.FindAnimal and B.FindAnimal(P.rec) or nil
    if not a then
        out("probe: your bear has no body any more -- end")
        P = nil
        return
    end
    local z, d = nearestZed(a)
    if not z then
        out(string.format("probe t=%.1f s: no zombie within 15 tiles", (now - P.t0) / 1000))
        return
    end
    local tgt = z:getTarget()                           -- B:client/BanditMenu.lua:170
    local who = "none"
    if tgt == a then who = "BEAR" elseif tgt ~= nil then who = "other" end
    out(string.format("probe t=%.1f s: dist %.2f / bite reach %s | state %s | bump %s | target %s | on floor %s | useless %s",
        (now - P.t0) / 1000, d, fix(P.reach, 2), tostring(z:getActionStateName()), tostring(z:getBumpType()), who,
        tostring(z:isOnFloor()), tostring(z:isUseless())))
end

function NCBear_FightProbe()
    if P then
        P = nil
        out("probe stopped")
        return
    end
    local p, rec, a = mine()
    if not p then return end
    if not a then
        say("your bear has no living body right now")
        return
    end
    local reach = nil
    if B.FoeReach and B.StatsOf then
        local st = B.StatsOf(rec)
        reach = B.FoeReach("z", rec.body, st and st.sz)
    end
    local now = getTimestampMs()
    P = { rec = rec, t0 = now, last = 0, reach = reach }
    if not hooked then
        hooked = true
        Events.OnTick.Add(probeTick)                    -- V:client/Chat/ISChat.lua:943
    end
    out("probe: 15 s, one line every 0.5 s (NCBear_FightProbe() again stops it). Bring a zombie: NCBear_FightZed(1, 6)")
end

-- ---------------------------------------------------------------------------
-- Rechtsklick (Wirt: client/NCBearBenchModel.lua)
-- ---------------------------------------------------------------------------
local function menuZed() NCBear_FightZed(1, 6) end
local function menuInfo() NCBear_FightInfo() end
local function menuDown() NCBear_FightDown() end

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}
table.insert(NCBearMenu.extra, function(sub, square, _player)
    sub:addOption("Fight: zombie next to my bear", square, menuZed)     -- V:client/DebugUIs/AdminContextMenu.lua:46
    sub:addOption("Fight: info", square, menuInfo)
    sub:addOption("Fight: knock my bear down", square, menuDown)
end)
