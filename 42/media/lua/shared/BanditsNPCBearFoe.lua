--
-- NPC Crew -- Baer, die Zombie- und Banditen-Seite des Kampfs (F2 = B5a, PLAN_F2.md 0.1-0.3, 2.1.2-2.1.4, 2.2.4, 4.3, 4.4).
--
-- Laeuft dort, wo der Zombie gerechnet wird: im Einzelspieler im einen Programm, im Mehrspieler auf dem Client mit Hoheit ueber den Zombie
-- (H, "not z:getVariableBoolean('bClient')", FG 4). Auf dem dedizierten Server tut die Datei nichts (kein Takt, B.OnFx kehrt sofort um).
-- Der Schreiber (server/BanditsNPCBearFight*.lua, ...Hurt.lua) ENTSCHEIDET alles, was zaehlt (wer beisst, Treffer, Schaden am Baeren);
-- diese Datei zeigt nur und wirkt am Zombie:
--   1 Locken (B.FoeLureTick, je lureMs): ein Zombie in lureR eines gezaehmten Baeren laeuft hin -- SP spotted/setTarget bzw. CanSee ->
--     pathToCharacter (Kevins Probe ENT:60 "laeuft hin"), MP pathToLocationF (das Ziel reist im MP als Spieler-Id, FG 0.3). Nur, wenn der Baer
--     dem Zombie NAEHER ist als jeder Spieler und jeder Bandit (keine NPC-Crew-Figur wird gestoert, FG 1.6).
--   2 Biss-Pose (Fx "zbite"): eigener Knoten AnimSets/zombie/bumped/BanditsNPCBearZBite*.xml ueber setBumpType (Weg der Bandits, ohne Bandits
--     mit eigenem Knoten, PLAN_F2.md 0.3).
--   3 Banditen-Hieb (Fx "smack"): eigene Bandits-Aufgabe ZombieActions.BNBearSmack (in OnGameBoot, nur mit Bandits).
--   4 Treffer des Baeren am Zombie (Fx "hit", B.FoeHurt): Leben, Blut, Ton, Umwerfen mit Zurueckfliegen, eigenes Schieben (B.FoePushTick).
-- Buchfuehrung nur in Lua-Listen dieser Datei (L Locken <= lureTrackMax, P Schieben <= pushMax), nie in z:getModData() (Bandits loescht
-- brain an Nicht-Banditen jedes Update, FG 1.5).
-- Jeder Engine-Aufruf mit Fundstelle am Aufruf (Vanilla 42.22 media/lua = V:, Bandits 42.22 media/lua = B:). Ohne Bandits laeuft alles (keine
-- Banditen, Zombies ueber die Zellenliste). Ladefolge: shared, nach ...Bear / ...Crew / ...Defs / ...FightRules; fremde Funktionen nur zur
-- Laufzeit ueber B.X.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B.ZBITE = "BNBearZBite"             -- Bump-Wert und Knoten-Name (Name ewig stabil, PLAN_F2.md 0.3)
B.ZBITE_LOW = "BNBearZBiteLow"      -- Biss gegen das kleine Junge (Clip Zombie_BiteLow_Success)
B.SMACK = "BNBearSmack"             -- Bandits-Aufgabe des Banditen-Hiebs

local L = {}            -- Locken: { z, id, obj, at, pAt, px, py } (Deckel lureTrackMax)
local P = {}            -- Schieben: { z, rx, ry, left, t0, zl } (Deckel pushMax)
local lureAt = nil      -- Echtzeit des letzten Locken-Takts
local lureFrom = 0      -- rollender Anfang in der Zellenliste

local FALL_PREFIX = { "falldown", "staggerback-knockeddown", "knockeddown", "onground", "getup", "getdown", "falling",
    "hitreaction-onfloor", "vehicleCollision-onground", "fakedead" }
-- nur aus diesen Zustaenden fliegt ein Zombie zurueck (forschung_f2_bestand.md 2.5; gespielt T:shared/NCBearFight.lua:303)
local FLY_FROM = { idle = true, walktoward = true, pathfind = true, attack = true, lunge = true }

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function cfg(key, def)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return def end
    return v
end

-- Hoheit ueber den Zombie: im Einzelspieler immer; im Mehrspieler nur der Client, der ihn rechnet.
-- z:getVariableBoolean(Text): B:client/BanditZombie.lua:74 (gleiche Methode, Text-Argument); Name bClient: V:media/actiongroups/zombie/idle/
-- to_attack.xml (<isFalse>bClient</isFalse>).
local function hasAuth(z)
    if B.IsSP() then return true end
    return z:getVariableBoolean("bClient") ~= true
end

-- Liegt / faellt der Zombie? z:isProne(), z:getActionStateName(): B:shared/ZombieActions/ZASmack.lua:486.
local function posture(z)
    if z:isProne() then return "down", "onground" end
    local st = z:getActionStateName()
    if type(st) ~= "string" then return "up", "" end
    if st == "onground" then return "down", st end
    for i = 1, #FALL_PREFIX do
        local pre = FALL_PREFIX[i]
        if string.sub(st, 1, string.len(pre)) == pre then return "falling", st end
    end
    return "up", st
end

-- ---------------------------------------------------------------------------
-- Zombie zu einer Outfit-Kennung finden (4.3): in 1,5 Kacheln um (x, y), gleiche z:getPersistentOutfitID() (B:shared/BanditUtils.lua:621).
-- Erst die eigene Locken-Liste, dann (SP mit Bandits) BanditZombie.CacheLightZ/CacheLightB + BanditZombie.GetInstanceById(id)
-- (B:client/BanditZombie.lua:11-16, :177-186; prueft Identitaet und Welt), sonst die Zellenliste getCell():getZombieList() (B:server/
-- BanditSave.lua:15-18), gedeckelt foeScanMax. getX/getY am Zombie: B:client/BanditZombie.lua:69-71.
-- ---------------------------------------------------------------------------
local function near15(z, x, y)
    local dx, dy = z:getX() - x, z:getY() - y
    return dx * dx + dy * dy <= 2.25
end

local function lightFind(tab, oid, x, y, cap)
    if type(tab) ~= "table" then return nil, 0 end
    local bz = BanditZombie
    local seen = 0
    for id, light in pairs(tab) do
        seen = seen + 1
        if seen > cap then break end
        if type(light) == "table" then
            local lx, ly = num(light.x), num(light.y)
            if lx ~= nil and ly ~= nil and (lx - x) * (lx - x) + (ly - y) * (ly - y) <= 2.25 then
                local z = bz.GetInstanceById(id)
                if z ~= nil and z:getPersistentOutfitID() == oid then return z, seen end
            end
        end
    end
    return nil, seen
end

function B.FoeFind(oid, x, y)
    oid, x, y = num(oid), num(x), num(y)
    if oid == nil or x == nil or y == nil then return nil end
    for i = 1, #L do
        local z = L[i].z
        if z ~= nil and near15(z, x, y) and z:getPersistentOutfitID() == oid then return z end
    end
    local cap = math.floor(cfg("foeScanMax", 1500))
    local bz = BanditZombie
    if B.IsSP() and type(bz) == "table" and bz.GetInstanceById then
        local z, n1 = lightFind(bz.CacheLightZ, oid, x, y, 4 * cap)
        if z ~= nil then return z end
        local zb, n2 = lightFind(bz.CacheLightB, oid, x, y, 4 * cap)
        if zb ~= nil then return zb end
        if n1 + n2 > 0 then return nil end
    end
    local cell = getCell()
    local list = cell and cell:getZombieList()
    if not list then return nil end
    local size = list:size()
    if size > cap then size = cap end
    for i = 0, size - 1 do
        local z = list:get(i)
        if z ~= nil and near15(z, x, y) and z:getPersistentOutfitID() == oid then return z end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Treffer am Zombie (2.2.4, 4.3): die EINE Stelle mit getHealth / setHealth / Kill am Zombie. Nur wo der Zombie gerechnet wird (hasAuth).
-- ---------------------------------------------------------------------------

-- Darf ein Zombie von Kachel a nach Kachel b fliegen / geschoben werden? Vanillas Frage "kann man hier ablegen":
-- V:client/TimedActions/ISInventoryTransferAction.lua:590 (TreatAsSolidFloor), :593 (isSolid/isSolidTrans), :598 (isBlockedTo/isWindowTo),
-- :601 (HasStairs); Wasser V:client/ISUI/ISWorldObjectContextMenu.lua:687-688 (getFloor, hasProperty(IsoFlagType.water)); isFree(false)
-- V:client/Farming/ISUI/ISFarmingMenu.lua:530. Gespielt T:shared/NCBearFight.lua:707-718.
local function flyOk(a, b)
    if b == nil then return false, "unloaded" end
    if not b:TreatAsSolidFloor() then return false, "no floor" end
    if b:HasStairs() then return false, "stairs" end
    local floor = b:getFloor()
    if floor ~= nil and floor:hasProperty(IsoFlagType.water) then return false, "water" end
    if b:isSolid() or b:isSolidTrans() then return false, "solid" end
    if not b:isFree(false) then return false, "furniture" end
    if a:isBlockedTo(b) then return false, "wall or door" end
    if a:isWindowTo(b) then return false, "window" end
    return true, nil
end

-- Hinter dem Zombie (Richtung rx, ry) frei? knockSamples Punkte je knockStep. getCell():getGridSquare(x, y, z): V:server/Animal/
-- ISPickDungCursor.lua:104. getZ am Zombie: B:server/BanditSave.lua (Zombieliste), gespielt T:shared/NCBearFight.lua:723-742.
local function clearBehind(z, rx, ry)
    local cell = getCell()
    local zx, zy = z:getX(), z:getY()
    local zl = math.floor(z:getZ())
    local lx, ly = math.floor(zx), math.floor(zy)
    local prev = cell:getGridSquare(lx, ly, zl)
    if prev == nil then return false, "unloaded" end
    if prev:HasStairs() then return false, "stairs" end
    local step = cfg("knockStep", 0.45)
    for k = 1, math.floor(cfg("knockSamples", 4)) do
        local px = math.floor(zx + rx * step * k)
        local py = math.floor(zy + ry * step * k)
        if px ~= lx or py ~= ly then
            local sq = cell:getGridSquare(px, py, zl)
            local ok, why = flyOk(prev, sq)
            if not ok then return false, why end
            prev, lx, ly = sq, px, py
        end
    end
    return true, nil
end

local function addPush(z, rx, ry, ms)
    for i = 1, #P do
        if P[i].z == z then
            table.remove(P, i)
            break
        end
    end
    if #P >= math.floor(cfg("pushMax", 8)) then table.remove(P, 1) end
    P[#P + 1] = { z = z, rx = rx, ry = ry, left = cfg("knockPush", 0.7), t0 = ms, zl = math.floor(z:getZ()) }
end

-- Umwerfen (gespielt T:shared/NCBearFight.lua:845-905, Kevin 08.11. "umwerfen hat geklappt"). mode "back" / "down". bear = Baer-Kopie
-- dieses Rechners (U.CubObj) oder nil (dann faellt er auf der Stelle). Reihenfolge Pflicht: setPlayerAttackPosition NACH knockDown.
-- "Von hinten getroffen" (Richtung Baer -> Zombie gegen die Blickrichtung des Zombies, Skalarprodukt > 0,5): die Rechnung ist gelernt aus
-- B:shared/ZombieActions/ZAPush.lua:33-39 (Standard-Vektorrechnung, eigene Namen; Nachbesserung F2 A7).
-- z:getForwardDirection() + :getX()/:getY(): B:shared/ZombieActions/ZAPush.lua:36-37; z:testDotSide(Figur): ZAPush.lua:42 (IsoGameCharacter
-- als Argument; der Baer ist IsoPlayer); z:setHitFromBehind(b): ZAPush.lua:41; z:knockDown(b): V:client/DebugUIs/DebugContextMenu.lua:664;
-- z:setPlayerAttackPosition(Text): ZAPush.lua:42.
local function knock(z, mode, bear, bx, by, ms)
    local awayX, awayY = z:getX() - bx, z:getY() - by
    local awayLen = math.sqrt(awayX * awayX + awayY * awayY)
    local behind = false
    local fx, fy = 0, 0
    if awayLen > 0 then
        local fwd = z:getForwardDirection()
        fx, fy = fwd:getX(), fwd:getY()
        behind = (awayX * fx + awayY * fy) / awayLen > 0.5
    end
    local side = nil
    if bear ~= nil then side = z:testDotSide(bear) end
    local fromBehind = behind or side == "BEHIND"
    local _, st = posture(z)
    local rx, ry = 0, 0
    if mode == "back" then
        if bear == nil or not FLY_FROM[st or ""] or fromBehind or awayLen < 0.05 or side ~= "FRONT" then
            mode = "down"
        else
            rx, ry = awayX / awayLen, awayY / awayLen
            local ok = clearBehind(z, rx, ry)
            local fl = math.sqrt(fx * fx + fy * fy)
            if ok and fl > 0.001 then ok = clearBehind(z, -fx / fl, -fy / fl) end
            if not ok then mode = "down" end
        end
    end
    local fly = mode == "back"
    z:setHitFromBehind(fromBehind and not fly)
    z:knockDown(fromBehind)
    if fly then
        z:setPlayerAttackPosition(side)
        if cfg("knockPush", 0.7) > 0 then addPush(z, rx, ry, ms) end
    end
    return mode
end

-- Treffer: dmg Zombie-Leben, knock "back"/"down"/nil (vom Schreiber gewuerfelt), kk = Umwerf-Art auch fuer den toedlichen Treffer
-- (knockKill, nur wo die Stufe umwerfen darf), snd = Treffer-Ton oder nil. Rueckgabe "kill" / "hit" / nil (nicht gerechnet).
-- z:isAlive(): B:server/BanditSave.lua:52; z:getHealth()/z:setHealth(Zahl): B:client/BanditUpdate.lua:2392/:2397; z:Kill(nil): :2386;
-- z:splatBlood(3, 0.3), z:splatBloodFloorBig(): B:shared/BanditCompatibility.lua:130/:132; z:playSound(Text): B:client/BanditUpdate.lua:1665,
-- Ton "HeadSmash" V:media/scripts/generated/sounds/zombies/sounds_zombie_foley.txt (gespielt T:shared/NCBearFight.lua:910-927).
function B.FoeHurt(z, dmg, knockMode, bx, by, id, snd, kk)
    if z == nil or not hasAuth(z) or not z:isAlive() then return nil end
    dmg = num(dmg) or 0
    bx, by = num(bx), num(by)
    if bx == nil or by == nil then bx, by = z:getX(), z:getY() end
    local ms = getTimestampMs()                  -- V:server/Foraging/forageServer.lua:456
    local bear = nil
    local ui = B.UI
    if ui and ui.CubObj and id ~= nil then bear = ui.CubObj(id) end
    local h = z:getHealth() - dmg
    z:splatBlood(3, 0.3)
    z:splatBlood(3, 0.3)
    local pst = posture(z)
    local standing = pst == "up"
    if h <= 0 then
        z:splatBloodFloorBig()
        if snd ~= nil then z:playSound("HeadSmash") end
        if cfg("knockKill", 1) >= 1 and standing and (kk == "back" or kk == "down") then knock(z, kk, bear, bx, by, ms) end
        z:Kill(nil)
        return "kill"
    end
    z:setHealth(h)
    if type(snd) == "string" then z:playSound(snd) end
    if standing and (knockMode == "back" or knockMode == "down") then knock(z, knockMode, bear, bx, by, ms) end
    return "hit"
end

-- Eigenes Schieben je Bild (Kevin ENT:90 knockPush 0,7): je Bild hoechstens pushStep, hoechstens pushMs, jede neue Kachel wie im Flug.
-- z:setX/setY: B:shared/ZombieActions/ZAMove.lua:11/:17; z:getCurrentSquare(): B:client/BanditUpdate.lua:574.
function B.FoePushTick()
    if #P == 0 then return end
    local ms = getTimestampMs()
    local stepMax = cfg("pushStep", 0.05)
    local span = cfg("pushMs", 600)
    local i = 1
    while i <= #P do
        local p = P[i]
        local z = p.z
        local drop = p.left <= 0 or ms - p.t0 > span or ms - p.t0 < 0 or z:getCurrentSquare() == nil or math.floor(z:getZ()) ~= p.zl
        if not drop then
            local step = p.left
            if step > stepMax then step = stepMax end
            local x, y = z:getX(), z:getY()
            local nx, ny = x + p.rx * step, y + p.ry * step
            local ox, oy, kx, ky = math.floor(x), math.floor(y), math.floor(nx), math.floor(ny)
            if ox ~= kx or oy ~= ky then
                local cell = getCell()
                local sa = cell:getGridSquare(ox, oy, p.zl)
                if sa == nil or not flyOk(sa, cell:getGridSquare(kx, ky, p.zl)) then drop = true end
            end
            if not drop then
                z:setX(nx)
                z:setY(ny)
                p.left = p.left - step
            end
        end
        if drop then table.remove(P, i) else i = i + 1 end
    end
end

-- ---------------------------------------------------------------------------
-- Locken (2.1.2): je lureMs, nur auf SP / MP-Client. Baeren aus der Sicht (B.View.cubs: tame, ld, nicht ride, nicht dn), Objekt ueber
-- U.CubObj (F1-Hud; ohne OBERFLAECHE nichts).
-- ---------------------------------------------------------------------------

-- Ziel freigeben, wenn es noch dieser Baer ist. z:getTarget(): B:client/BanditUpdate.lua:1647; z:setTarget(nil): :421 (IsoZombie, nil;
-- gespielt am Baeren T:client/NCBearAttackProbe.lua:170-172).
local function letGo(e)
    local z = e.z
    if z ~= nil and e.obj ~= nil and z:getTarget() == e.obj then z:setTarget(nil) end
end

function B.FoeRelease(id)
    if id == nil then return end
    local i = 1
    while i <= #L do
        if L[i].id == id then
            letGo(L[i])
            table.remove(L, i)
        else
            i = i + 1
        end
    end
end

-- Spieler dieses Rechners bzw. des Spiels. SP: getNumActivePlayers() (V:client/Fishing/FishingHandler.lua:6) + getSpecificPlayer(i)
-- (V:server/BuildingObjects/ISBuildingObject.lua:183); MP-Client: getOnlinePlayers() :size() / :get(i) (B:client/BanditPlayer.lua:24).
-- getX/getY am Spieler: B:server/BanditServerSpawner.lua:179. isDead am Spieler: V:server/XpSystem/XpUpdate.lua:298.
local function playerSpots()
    local out = {}
    if isClient() then
        local online = getOnlinePlayers()
        if online then
            for i = 0, online:size() - 1 do
                local p = online:get(i)
                if p and not p:isDead() and #out < 64 then out[#out + 1] = { x = p:getX(), y = p:getY() } end
            end
        end
        return out
    end
    for i = 0, getNumActivePlayers() - 1 do
        local p = getSpecificPlayer(i)
        if p and not p:isDead() then out[#out + 1] = { x = p:getX(), y = p:getY() } end
    end
    return out
end

-- Lagen der Banditen (nur mit Bandits): BanditZombie.CacheLightB (B:client/BanditZombie.lua:16, Felder x / y aus :68-69), Deckel 64.
local function banditSpots()
    local out = {}
    local bz = BanditZombie
    local tab = type(bz) == "table" and bz.CacheLightB or nil
    if type(tab) ~= "table" then return out end
    for _, light in pairs(tab) do
        if #out >= 64 then break end
        if type(light) == "table" and num(light.x) ~= nil and num(light.y) ~= nil then out[#out + 1] = { x = light.x, y = light.y } end
    end
    return out
end

-- Ist der Baer (Abstand d) dem Zombie naeher als jeder Spieler / Bandit?
local function nearestIsBear(zx, zy, d, spots)
    for i = 1, #spots do
        local s = spots[i]
        local dx, dy = s.x - zx, s.y - zy
        if dx * dx + dy * dy <= d * d then return false end
    end
    return true
end

local function tracked(z)
    for i = 1, #L do
        if L[i].z == z then return L[i] end
    end
    return nil
end

local function countFor(id)
    local n = 0
    for i = 1, #L do
        if L[i].id == id then n = n + 1 end
    end
    return n
end

-- Kandidaten (keine Banditen) in r um einen der Baeren (Nachbesserung F2 B2, wie server/BanditsNPCBearFightFoes.lua cands): Rahmen aller
-- Baeren nur als Vorfilter, dann der KREIS um jeden Baeren (gleiche Ebene) und je Baer die NAECHSTEN lureCandMax -- kein globaler Deckel,
-- der naechste Zombie fehlt nie. Quellen: SP mit Bandits CacheLightZ + GetInstanceById, sonst die Zellenliste (rollend, hoechstens
-- foeScanMax). Rueckgabe Liste { z, x, y, zl } (je Zombie einmal; Baer fuer Baer, der naechste zuerst). isAlive: B:server/BanditSave.lua:52;
-- "Bandit": B:client/BanditZombie.lua:74; getZ: Zombieliste.
local function sortIn(t, e, cap)
    local n = #t
    if n >= cap and e.d >= t[n].d then return end
    t[n + 1] = e
    local i = n + 1
    while i > 1 and t[i - 1].d > e.d do
        t[i], t[i - 1] = t[i - 1], t[i]
        i = i - 1
    end
    if #t > cap then t[#t] = nil end
end

-- In welchen Baeren-Kreisen steht er? isAlive und (nur Zellenliste, checkBandit) "Bandit" erst, wenn er in einem Kreis steht.
local function lurePut(per, bears, r, z, x, y, zl, checkBandit)
    local c = nil
    local capN = math.floor(cfg("lureCandMax", 12))
    for i = 1, #bears do
        local b = bears[i]
        if math.floor(zl) == math.floor(b.z) then
            local dx, dy = x - b.x, y - b.y
            local d2 = dx * dx + dy * dy
            if d2 <= r * r then
                if c == nil then
                    if not z:isAlive() then return end
                    if checkBandit and z:getVariableBoolean("Bandit") == true then return end
                    c = { z = z, x = x, y = y, zl = zl }
                end
                sortIn(per[i], { c = c, d = math.sqrt(d2) }, capN)
            end
        end
    end
end

local function lureCands(bears, r)
    local per = {}
    for i = 1, #bears do per[i] = {} end
    local x0, x1, y0, y1 = bears[1].x - r, bears[1].x + r, bears[1].y - r, bears[1].y + r
    for i = 2, #bears do
        local b = bears[i]
        if b.x - r < x0 then x0 = b.x - r end
        if b.x + r > x1 then x1 = b.x + r end
        if b.y - r < y0 then y0 = b.y - r end
        if b.y + r > y1 then y1 = b.y + r end
    end
    local cap = math.floor(cfg("foeScanMax", 1500))
    local bz = BanditZombie
    local tab = (B.IsSP() and type(bz) == "table" and bz.GetInstanceById) and bz.CacheLightZ or nil
    local done = false
    if type(tab) == "table" then
        local seen = 0
        for id, light in pairs(tab) do
            seen = seen + 1
            if seen > 4 * cap then break end
            local lx, ly = type(light) == "table" and num(light.x) or nil, type(light) == "table" and num(light.y) or nil
            if lx ~= nil and ly ~= nil and lx >= x0 and lx <= x1 and ly >= y0 and ly <= y1 then
                local z = bz.GetInstanceById(id)
                if z ~= nil then lurePut(per, bears, r, z, lx, ly, num(light.z) or 0, false) end
            end
        end
        done = seen > 0
    end
    if not done then
        local cell = getCell()
        local list = cell and cell:getZombieList()
        local size = list and list:size() or 0
        if size > 0 then
            local start = lureFrom
            if start < 0 or start >= size then start = 0 end
            local count = size
            if count > cap then count = cap end
            for k = 0, count - 1 do
                local idx = start + k
                if idx >= size then idx = idx - size end
                local z = list:get(idx)
                if z ~= nil then
                    local zx, zy = z:getX(), z:getY()
                    if zx >= x0 and zx <= x1 and zy >= y0 and zy <= y1 then lurePut(per, bears, r, z, zx, zy, z:getZ(), true) end
                end
            end
            local nxt = start + count
            if nxt >= size then nxt = nxt - size end
            lureFrom = nxt
        end
    end
    local out = {}
    for i = 1, #per do
        local q = per[i]
        for j = 1, #q do
            local c = q[j].c
            if c.taken ~= true then
                c.taken = true
                out[#out + 1] = c
            end
        end
    end
    return out
end

-- Einen Zombie zum Baeren schicken. SP: Ziel nil oder schon dieser Baer -> fern (d > lureNear) z:CanSee(Baer) -> z:pathToCharacter(Baer)
-- (B:client/BanditUpdate.lua:1812-1813, Argument IsoGameCharacter; am Baeren gespielt T:client/NCBearAttackProbe.lua:137-138), nah
-- z:spotted(Baer, true) + z:setTarget(Baer) (:1832, :1834; gespielt T:client/NCBearAttackProbe.lua:134-135; nie spotted(.., false), FG 1.1).
-- MP (nur H): nur Zombies OHNE Ziel, z:pathToLocationF(x, y, z) (B:shared/ZombieActions/ZAGoTo.lua:42), hoechstens je lureRepathMs oder
-- wenn der Baer weiter als 1,5 Kacheln zog. Waehrend unseres Bisses (Bump-Wert) nichts: bumped/to_pathfind.xml bricht sonst den Biss ab.
local function steerZombie(e, b, d, ms)
    local z = e.z
    local bt = z:getBumpType()                   -- B:client/BanditUpdate.lua:1890
    if bt == B.ZBITE or bt == B.ZBITE_LOW then return end
    local obj = b.obj
    if B.IsSP() then
        local tgt = z:getTarget()
        if tgt ~= nil and tgt ~= obj then return end
        if d > cfg("lureNear", 3) then
            if z:CanSee(obj) then z:pathToCharacter(obj) end
        else
            z:spotted(obj, true)
            z:setTarget(obj)
        end
        return
    end
    if not hasAuth(z) or z:getTarget() ~= nil then return end
    local moved = e.px == nil or e.py == nil or B.DistXY(e.px, e.py, b.x, b.y) > 1.5
    if e.pAt ~= nil and ms - e.pAt >= 0 and ms - e.pAt < cfg("lureRepathMs", 1000) and not moved then return end
    z:pathToLocationF(b.x, b.y, b.z)
    e.pAt, e.px, e.py = ms, b.x, b.y
end

-- Eintraege loslassen: Baer weg aus der Sicht, am Boden, faehrt mit, neue Kopie, Zombie tot oder weiter als 2 x lureR.
local function sweep(byId)
    local far = 2 * cfg("lureR", 10)
    local i = 1
    while i <= #L do
        local e = L[i]
        local b = byId[e.id]
        local drop = b == nil or b.obj ~= e.obj or e.z == nil or not e.z:isAlive()
        if not drop then
            local dx, dy = e.z:getX() - b.x, e.z:getY() - b.y
            drop = dx * dx + dy * dy > far * far
        end
        if drop then
            letGo(e)
            table.remove(L, i)
        else
            i = i + 1
        end
    end
end

-- Baeren dieses Rechners: Sicht-Eintraege tame, ld, nicht ride, nicht dn, mit lebender Kopie (U.CubObj). getX/getY/getZ am Tier:
-- V:client/TimedActions/ISContextualActions.lua:100.
local function lureBears()
    local out, byId = {}, {}
    local v = B.View
    local ui = B.UI
    if type(v) ~= "table" or type(v.cubs) ~= "table" or not (ui and ui.CubObj) then return out, byId end
    for id, c in pairs(v.cubs) do
        if type(c) == "table" and c.st == "tame" and c.ld == true and c.ride ~= true and c.dn ~= true and #out < 16 then
            local obj = ui.CubObj(id)
            if obj ~= nil then
                local b = { id = id, obj = obj, x = obj:getX(), y = obj:getY(), z = obj:getZ() }
                out[#out + 1] = b
                byId[id] = b
            end
        end
    end
    return out, byId
end

local function lureBody(ms)
    local bears, byId = lureBears()
    if B.Opt("BearZombiesAttack") ~= true then bears, byId = {}, {} end
    sweep(byId)
    if #bears == 0 then return end
    local r = cfg("lureR", 10)
    local cands = lureCands(bears, r)
    if #cands == 0 then return end
    local spots = playerSpots()
    local bandits = banditSpots()
    for j = 1, #bandits do spots[#spots + 1] = bandits[j] end
    local perMax = math.floor(cfg("lureMax", 6))
    local allMax = math.floor(cfg("lureTrackMax", 32))
    for i = 1, #cands do
        local c = cands[i]
        local best, bestD = nil, nil
        for k = 1, #bears do
            local b = bears[k]
            local d = B.DistXY(c.x, c.y, b.x, b.y)
            if d <= r and math.floor(c.zl) == math.floor(b.z) and (bestD == nil or d < bestD) then best, bestD = b, d end
        end
        if best ~= nil and nearestIsBear(c.x, c.y, bestD, spots) then
            local e = tracked(c.z)
            if e ~= nil and e.id ~= best.id then
                letGo(e)
                e.id, e.obj, e.pAt = best.id, best.obj, nil
            elseif e == nil and #L < allMax and countFor(best.id) < perMax then
                e = { z = c.z, id = best.id, obj = best.obj, at = ms }
                L[#L + 1] = e
            end
            if e ~= nil and e.id == best.id then steerZombie(e, best, bestD, ms) end
        end
    end
end

function B.FoeLureTick()
    if isServer() then return end
    local ms = getTimestampMs()
    if lureAt ~= nil and ms - lureAt >= 0 and ms - lureAt < cfg("lureMs", 500) then return end
    lureAt = ms
    lureBody(ms)
end

-- ---------------------------------------------------------------------------
-- Kampf-Ereignisse (4.4, Spalte KERN). Danach die Baeren-Seite der OBERFLAECHE (B.UI.FightFx). Dedizierter Server: nichts.
-- ---------------------------------------------------------------------------

-- Bild des Banditen-Hiebs aus seiner Nahkampfwaffe (brain.weapons.melee, B:client/BanditUpdate.lua:657 / :734):
-- WeaponType.getWeaponType(BanditCompatibility.InstanceItem(Name)) (B:shared/ZombieActions/ZASmack.lua:488-489); Werte = Bedingungen der
-- Bandits-Knoten BC:AnimSets/zombie/bumped/zsattackbarehands1.xml / zsattack2h1.xml / zsattack1h1.xml.
local function smackAnim(brain)
    local w = type(brain) == "table" and type(brain.weapons) == "table" and brain.weapons.melee or nil
    if type(w) ~= "string" or w == "Base.BareHands" then return "AttackBareHands1" end
    local bc, wt = BanditCompatibility, WeaponType
    if type(bc) ~= "table" or not bc.InstanceItem or wt == nil then return "AttackBareHands1" end
    local item = bc.InstanceItem(w)
    if item == nil then return "AttackBareHands1" end
    local kind = wt.getWeaponType(item)
    if kind == wt.UNARMED then return "AttackBareHands1" end
    if kind == wt.TWO_HANDED then return "Attack2H1" end
    return "Attack1H1"
end

local function onBite(t)
    local z = B.FoeFind(t.oid, t.zx, t.zy)
    if z == nil or not hasAuth(z) then return end
    local bt = B.ZBITE
    if t.low == true then bt = B.ZBITE_LOW end
    if z:getBumpType() == bt then return end        -- B:shared/ZombieActions/ZASmack.lua:601 (Vergleich des Bump-Werts)
    local bx, by = num(t.bx), num(t.by)
    if bx ~= nil and by ~= nil then z:faceLocationF(bx, by) end     -- B:shared/ZombieActions/ZASmack.lua:599
    z:setBumpType(bt)                                -- B:client/BanditUpdate.lua:1895
end

-- Bandit.HasTaskType(bandit, Name) B:shared/Bandit.lua:334; BanditBrain.Get(bandit) B:shared/BanditBrain.lua:3-6; Bandit.AddTask(bandit,
-- Aufgabe) B:shared/Bandit.lua:289-301 (ab 10 Aufgaben leert Bandits die ganze Liste -> wir reihen nur unter 8 ein; lock = true ueberlebt
-- Bandit.ClearTasks :372-381). Muster eigene Aufgabe: NPC Crew shared/BanditsNPCActions.lua:336-411 (gelernt, nicht kopiert).
local function onSmack(t)
    local bn, za, br = Bandit, ZombieActions, BanditBrain
    if type(bn) ~= "table" or type(za) ~= "table" or type(za[B.SMACK]) ~= "table" or type(br) ~= "table" then return end
    local z = B.FoeFind(t.oid, t.zx, t.zy)
    if z == nil then return end
    if bn.HasTaskType(z, B.SMACK) then return end
    local brain = br.Get(z)
    if type(brain) ~= "table" or type(brain.tasks) ~= "table" or #brain.tasks >= 8 then return end
    bn.AddTask(z, { action = B.SMACK, anim = smackAnim(brain), time = 65, lock = true, x = num(t.bx), y = num(t.by) })
end

-- Biss-/Kratz-Ton: z:playSound("ZombieBite") (1 von 4), sonst "ZombieScratch" (B:client/BanditUpdate.lua:1664-1668). ZombRand(n):
-- V:shared/TimedActions/Animals/ISMilkAnimal.lua:25.
local function onHurt(t)
    if t.dodge == true or t.src ~= "z" then return end
    local z = B.FoeFind(t.oid, t.zx, t.zy)
    if z == nil then return end
    if ZombRand(4) == 0 then z:playSound("ZombieBite") else z:playSound("ZombieScratch") end
end

local function onHit(t)
    local z = B.FoeFind(t.oid, t.zx, t.zy)
    if z == nil then return end
    if hasAuth(z) then
        B.FoeHurt(z, t.dmg, t.knock, t.bx, t.by, t.id, t.snd, t.kk)
    elseif type(t.snd) == "string" then
        z:playSound(t.snd)                           -- B:client/BanditUpdate.lua:1665
    end
end

local function foeSide(kind, t)
    if kind == "zbite" then
        onBite(t)
    elseif kind == "smack" then
        onSmack(t)
    elseif kind == "hurt" then
        onHurt(t)
    elseif kind == "hit" then
        onHit(t)
    elseif kind == "down" or kind == "dead" then
        B.FoeRelease(t.id)
    end
end

-- pcall nur um EIGENEN Code (wie B.BrainTick, server/BanditsNPCBearServer.lua): ein Fehler auf der Zombie-Seite kommt laut, aber gedrosselt
-- (B.ErrEvery), und die Baeren-Seite (Bild, Ton) laeuft trotzdem. Nachbesserung F2 B4: ebenso die Baeren-Seite (U.FightFx, OBERFLAECHE) --
-- im Einzelspieler laeuft B.OnFx mitten im Schreiber (B.Fx aus B.BearHurt / B.BearDie), ein Fehler der Anzeige darf dort weder Tod noch Am
-- Boden noch B.Close ueberspringen. pcall ist eine Lua-Grundfunktion, keine Engine-Methode.
function B.OnFx(kind, t)
    if isServer() then return end
    if type(t) ~= "table" or type(kind) ~= "string" then return end
    local ok, err = pcall(foeSide, kind, t)
    if not ok then B.ErrEvery("fx:" .. kind, 60000, "fight fx (" .. kind .. "): " .. tostring(err)) end
    local ui = B.UI
    if ui and ui.FightFx then
        local ok2, err2 = pcall(ui.FightFx, kind, t)
        if not ok2 then B.ErrEvery("fxui:" .. kind, 60000, "fight fx bear side (" .. kind .. "): " .. tostring(err2)) end
    end
end

-- ---------------------------------------------------------------------------
-- Bandits-Aufgabe des Banditen-Hiebs (2.1.4). Bandits ruft onStart / onWorking / onComplete (B:client/BanditUpdate.lua:1957-1999; die Pose
-- task.anim setzt Bandits im Zustand NEW selbst, :1956-1958). Nur Bild und Ton -- den Schaden rechnet der Schreiber nach B.CLIPS.smack.
-- bandit:faceLocationF(x, y): B:shared/ZombieActions/ZASmack.lua:599; bandit:isFemale(): :487; bandit:playSound(Stimme): :573 (Stimmen :496);
-- bandit:getBumpType(): :589, Ende wie :601.
-- ---------------------------------------------------------------------------
local function smackStart(bandit, task)
    local x, y = num(task.x), num(task.y)
    if x ~= nil and y ~= nil then bandit:faceLocationF(x, y) end
    if bandit:isFemale() then bandit:playSound("VoiceFemaleMeleeAttack") else bandit:playSound("VoiceMaleMeleeAttack") end
    return true
end

local function smackWork(bandit, task)
    local x, y = num(task.x), num(task.y)
    if x ~= nil and y ~= nil then bandit:faceLocationF(x, y) end
    if bandit:getBumpType() ~= task.anim then return true end
    return false
end

local function smackDone(bandit, task)
    return true
end

local installed = false
local function install()
    if installed then return end
    installed = true
    local za = ZombieActions
    if type(za) ~= "table" or type(Bandit) ~= "table" then return end
    if za[B.SMACK] == nil then za[B.SMACK] = { onStart = smackStart, onWorking = smackWork, onComplete = smackDone } end
end

-- Events.OnGameBoot.Add: V:client/Foraging/ISSearchManager.lua:1481. Events.OnTick.Add: V:server/Foraging/forageServer.lua:502 (Takt mit
-- Echtzeit-Drossel). Ueber kleine Huellen, damit spaeter ersetzte Funktionen gelten. Nur, wo Zombies gerechnet werden (nicht der
-- dedizierte Server).
Events.OnGameBoot.Add(install)
if not isServer() then
    Events.OnTick.Add(function()
        if #P > 0 then B.FoePushTick() end
        B.FoeLureTick()
    end)
end
