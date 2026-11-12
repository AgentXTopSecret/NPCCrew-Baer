if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Engine-Seite des Schreibers (B1a, PLAN_ZAEHMEN.md 5.1, 6.2.3, 6.3, 6.7).
--
-- Hier stehen ALLE Griffe in die Welt: Spielerliste, Tier erzeugen / finden / entfernen, Kachel- und Waldpruefung, Halten
-- und Laufen. Die Takte und Regeln (server/BanditsNPCBearServer.lua) rufen nur diese Funktionen, deshalb kann eine
-- Attrappe sie ersetzen. Jeder Engine-Aufruf nennt seine Fundstelle (Vanilla-Lua oder Bandits 42.22).
--
-- Tier erzeugen NUR in B.CreateCub. CreateCub: AppearFor und PlaceCub (B1c, server/BanditsNPCBearRide.lua: Aussteigen, Call to me)
-- sind die einzigen Aufrufer. Tier entfernen NUR in B.RemoveCub.
-- Im Mehrspieler ruft das nur der Server: ein Client, der an seiner Kopie entfernt, macht ein Geistertier.
-- B1c: Gehen ueber animal:setVariable("animalRunning", false) + animal:pathToLocation(x, y, z) NUR in B.MoveTo mit opt.walk
-- (beide mit Kevins Wort: pathToLocation 08.11.2026, forschung_engine.md:627; setVariable("animalRunning", false) 11.11.2026,
-- baer/begleiter/ENTSCHEIDUNGEN.md). Zombies finden in B.ZedNear (Bandits-belegte Wege), freie Kachel in B.SpotNear.
-- Nicht benutzt (Plan 0.8): setWild, die Engine-Akzeptanz als Balken, LosUtil, getCell():getAnimals(), Teleport (setX/setY am Tier).
-- B1e (PLAN_B1E.md 3.2 Nr. 5-10, 6.2.3): zwei Koerper -- B.CreateCub(x, y, z, body) erzeugt die Art des Koerpers (Vorgabe Junges),
-- Entfernen / Finden / Suchlauf sehen beide Arten ueber B.BodyKind (shared/BanditsNPCBear.lua; nie "bear"). B.SwapSpot waehlt die
-- Kachel fuer den Tausch, B.MoveTo rechnet die Wegzeit mit dem Tempo des Koerpers (B.BodyNum).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._orph = B._orph or {}             -- B1b: Waisen-Kandidaten { { o, at } } (Deckel B.CFG.orphanMax), nur fuer die Sitzung

-- ---------------------------------------------------------------------------
-- Spieler
-- ---------------------------------------------------------------------------

-- Liste { p, key, uid, nr, x, y, z } der lebenden Spieler. Server: getOnlinePlayers() mit :size() / :get(i)
-- (Vanilla server/Foraging/forageServer.lua:463-466). Einzelspieler: getNumActivePlayers() (Vanilla
-- client/Fishing/FishingHandler.lua:6) und getSpecificPlayer(i) (server/BuildingObjects/ISBuildingObject.lua:183).
-- isDead am Spieler (Server: getOnlinePlayers():get(i), Einzelspieler: getSpecificPlayer(i)): server/XpSystem/XpUpdate.lua:298
-- (Nachbesserung B1b A4: der vorige Beleg lag in auskommentiertem Vanilla-Code). getX/getY: Bandits server/BanditServerSpawner.lua:179,
-- getZ :191.
-- uid trennt lokale Spieler, die sich im Einzelspieler den Schluessel "__sp" teilen; nr ist dort die Spielernummer.
-- car (B1b): sitzt der Spieler in einem Fahrzeug? player:getVehicle(): Vanilla server/Vehicles/VehicleCommands.lua:11 (Server,
-- Spieler eines Client-Befehls), client/ISUI/Hutch/ISHutchMenu.lua:8 (getSpecificPlayer(n):getVehicle(), Einzelspieler).
function B.Players()
    local list = {}
    if isServer() then
        local online = getOnlinePlayers()
        if online then
            for i = 0, online:size() - 1 do
                local p = online:get(i)
                if p and not p:isDead() then
                    local key = B.PlayerKey(p)
                    if key ~= nil then
                        list[#list + 1] = { p = p, key = key, uid = key, nr = nil, x = p:getX(), y = p:getY(), z = p:getZ(),
                                            car = (p:getVehicle() ~= nil) }
                    end
                end
            end
        end
        return list
    end
    for i = 0, getNumActivePlayers() - 1 do
        local p = getSpecificPlayer(i)
        if p and not p:isDead() then
            list[#list + 1] = { p = p, key = B.SP_KEY, uid = B.SP_KEY .. "#" .. string.format("%d", i), nr = i,
                                x = p:getX(), y = p:getY(), z = p:getZ(), car = (p:getVehicle() ~= nil) }
        end
    end
    return list
end

-- Spieler zu einem Schluessel, wenn er gerade da ist (fuer Meldungen).
function B.PlayerByKey(key, players)
    if key == nil then return nil end
    players = players or B.Players()
    for i = 1, #players do
        if players[i].key == key then return players[i].p, players[i] end
    end
    return nil, nil
end

-- Ist es Nacht? Form Vanilla shared/Foraging/forageSystem.lua:1944-1951 (getClimateManager():getSeason(), getDawn, getDusk,
-- getGameTime():getTimeOfDay()).
function B.IsNight()
    local season = getClimateManager():getSeason()
    local dawn = season:getDawn()
    local dusk = season:getDusk()
    local timeOfDay = getGameTime():getTimeOfDay()
    return (timeOfDay < dawn) or (timeOfDay > dusk)
end

-- ---------------------------------------------------------------------------
-- Kacheln
-- ---------------------------------------------------------------------------

-- Wasser: dort bleibt ein Tier halb gebaut. Vanilla client/ISUI/ISWorldObjectContextMenu.lua:687-688.
local function isWater(sq)
    local floor = sq:getFloor()
    return floor ~= nil and floor:hasProperty(IsoFlagType.water)
end

-- Kann hier ein Junges stehen (bzw. ein Koeder liegen)? Rueckgabe: boolean, why.
-- isOutside: Bandits server/BanditServerSpawner.lua:152. TreatAsSolidFloor: Bandits server/BuildingObjects/ZSGuardposts.lua:12,
-- Vanilla server/BuildingObjects/ISWalkToCursor.lua:35. HasTree: Vanilla server/Foraging/forageServer.lua:276.
-- isFree(false): Bandits server/BanditServerSpawner.lua:231, Vanilla client/ISUI/ISWorldObjectContextMenu.lua:2219.
-- isVehicleIntersecting: Vanilla server/BuildingObjects/ISBuildUtil.lua:34.
function B.SquareFits(sq)
    if sq == nil then return false, "unloaded" end
    if not sq:isOutside() then return false, "inside" end
    if not sq:TreatAsSolidFloor() then return false, "nofloor" end
    if isWater(sq) then return false, "water" end
    if sq:HasTree() then return false, "tree" end
    if not sq:isFree(false) then return false, "blocked" end
    if sq:isVehicleIntersecting() then return false, "vehicle" end
    return true, nil
end

-- "Gegend geladen": die Kachel und vier Punkte im Abstand B.CFG.loadRing, alle am Boden. Nur dann darf "Tier fehlt" zaehlen.
-- getCell():getGridSquare(x, y, z) (nil = nicht geladen): Vanilla server/Animal/ISPickDungCursor.lua:104.
function B.AreaLoaded(x, y)
    local cell = getCell()
    local r = B.CFG.loadRing
    x = math.floor(x)
    y = math.floor(y)
    if cell:getGridSquare(x, y, 0) == nil then return false end
    if cell:getGridSquare(x + r, y, 0) == nil then return false end
    if cell:getGridSquare(x - r, y, 0) == nil then return false end
    if cell:getGridSquare(x, y + r, 0) == nil then return false end
    if cell:getGridSquare(x, y - r, 0) == nil then return false end
    return true
end

-- Einzelspieler: sieht ein lokaler Spieler diese Kachel gerade? isCanSee(Spielernummer): Vanilla
-- client/Foraging/ISBaseIcon.lua:256. Auf dem Server gibt es kein Sichtfeld je Spieler: dort immer false (ehrliche Grenze,
-- "ausser Sicht" gilt im Mehrspieler nur ueber den Mindestabstand).
function B.SeenInSP(sq, players)
    if sq == nil or not B.IsSP() then return false end
    players = players or B.Players()
    for i = 1, #players do
        local nr = players[i].nr
        if nr ~= nil and sq:isCanSee(nr) then return true end
    end
    return false
end

local function nearestDist(x, y, players)
    local best = nil
    for i = 1, #players do
        local d = B.DistXY(x, y, players[i].x, players[i].y)
        if best == nil or d < best then best = d end
    end
    return best
end

-- Abstand des naechsten Spielers zu einem Punkt (nil = niemand da).
function B.NearestPlayerDist(x, y, players)
    return nearestDist(x, y, players or B.Players())
end

-- Platz im Wald fuer ein neues Junges (Plan 5.1): bis B.CFG.tries Zufallspunkte im Ring Min..Max um den Spieler.
-- Kachel geladen, am Boden, Waldzone, B.SquareFits, Abstand zu ALLEN Spielern mindestens Min; im Einzelspieler zusaetzlich
-- nicht im Blick. Kein Punkt -> nil (kein Nachholen). player: Eintrag aus B.Players() oder ein Spieler.
-- Ring-Form und ZombRandFloat(a, b): Bandits server/BanditServerSpawner.lua:216-222.
function B.PickForestSquare(player, players)
    if player == nil then return nil end
    local e = player
    if type(e) ~= "table" then
        e = { p = player, x = player:getX(), y = player:getY(), z = player:getZ() }
    end
    players = players or B.Players()
    local minD = B.Opt("BearCubMinDistance")
    local maxD = B.Opt("BearCubMaxDistance")
    if maxD < minD + 5 then maxD = minD + 5 end
    if maxD > 65 then maxD = 65 end                 -- geladen sind 76 Kacheln um den Spieler: nie weiter ansprechen
    if minD > maxD then minD = maxD end
    local cell = getCell()
    for _ = 1, B.CFG.tries do
        local theta = ZombRandFloat(0, 2 * math.pi)
        local d = ZombRandFloat(minD, maxD)
        local x = math.floor(e.x + d * math.cos(theta))
        local y = math.floor(e.y + d * math.sin(theta))
        local sq = cell:getGridSquare(x, y, 0)
        if sq ~= nil and B.IsForestAt(x, y, 0) then
            local fits, _ = B.SquareFits(sq)
            if fits then
                local nd = nearestDist(x + 0.5, y + 0.5, players)
                if (nd == nil or nd >= minD) and not B.SeenInSP(sq, players) then
                    return sq
                end
            end
        end
    end
    return nil
end

-- Freie Kachel im Umkreis r um einen Punkt (Koeder-Junges). Beginnt an einer Zufallsstelle, hoechstens (2r+1)^2 Fragen.
-- ZombRand(n): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:25.
function B.FreeSquareNear(x, y, z, r, players)
    local cell = getCell()
    local side = 2 * r + 1
    local total = side * side
    local start = ZombRand(total)
    for k = 0, total - 1 do
        local idx = start + k
        if idx >= total then idx = idx - total end
        local ox = idx - math.floor(idx / side) * side - r
        local oy = math.floor(idx / side) - r
        local sq = cell:getGridSquare(x + ox, y + oy, z)
        if sq ~= nil then
            local fits, _ = B.SquareFits(sq)
            if fits and not B.SeenInSP(sq, players) then return sq end
        end
    end
    return nil
end

-- B1c (PLAN_B1C.md 3.6): freie Kachel 1..r Ringe um (x, y) auf Ebene z, fuer Aussteigen und "Call to me". Je Ring 8, 16, 24 Kacheln,
-- hoechstens 48 Kacheln bei r = 3. Wie B.SquareFits (Belege dort), aber OHNE isOutside (im Haus erlaubt) und OHNE B.SeenInSP (das Junge
-- SOLL sichtbar neben dem Spieler stehen); nie unter einem Fahrzeug (isVehicleIntersecting: Vanilla server/BuildingObjects/ISBuildUtil.lua:34).
-- getCell():getGridSquare: server/Animal/ISPickDungCursor.lua:104; square:getX()/getY(): client/DebugUIs/DebugContextMenu.lua:636.
-- Nachbesserung B1c B2: (1) nur eine Kachel im SELBEN Raum wie die Kachel des Spielers (draussen beide nil): sq:getRoom() ==
-- ownerSq:getRoom() wie Vanilla shared/Util/AdjacentFreeTileFinder.lua:240 (playerSq:getRoom() == gridSquare:getRoom()); (2) der Weg
-- von der Kachel zum Spieler ohne Wand, Zaun, Fenster oder Tuer: Schritt fuer Schritt (hoechstens 3, je einer Richtung Spieler)
-- not cur:isBlockedTo(next) -- square:isBlockedTo(square) wie Vanilla shared/Foraging/ISForageAction.lua:7 und
-- shared/TimedActions/ISDropWorldItemAction.lua:7 (dort mit der Nachbarkachel; Jar dec/IsoGridSquare.java:954-963: Wand, Fenster, Tuer,
-- Treppe zwischen den beiden Kacheln). Ob Zaeune und Ecken so ganz erfasst sind, ist ungeprueft (Testpunkt). (3) Der Anfang im Ring
-- wandert mit turn (der Aufrufer gibt die Koerper-Generation, die jedes Herholen erhoeht): ein zweiter "Call to me" probiert zuerst
-- eine andere Kachel. Kein Engine-Zufall noetig.
local function spotOk(sq)
    if sq == nil then return false end
    if not sq:TreatAsSolidFloor() then return false end
    if isWater(sq) then return false end
    if sq:HasTree() then return false end
    if not sq:isFree(false) then return false end
    if sq:isVehicleIntersecting() then return false end
    return true
end

-- B1e (PLAN_B1E.md 1.1 Schritt 4a, 6.2.3): Kachel fuer den Koerper-Tausch -- die eigene Kachel des Tiers, wenn sie die Platzregeln von
-- B.SpotNear erfuellt (spotOk), sonst Ring 1..swapRing um das Tier wie B.SpotNear (gleicher Raum, ohne Sperre erreichbar). nil = keine.
-- animal:getSquare(): Vanilla shared/TimedActions/Animals/ISPetAnimal.lua:6 (self.animal:getSquare()). getX/getY/getZ am Tier:
-- Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-577. Ob isFree(false) die eigene Kachel eines Tiers als belegt meldet, ist
-- ungeprueft -- dann nimmt der Tausch eine Kachel daneben.
function B.SwapSpot(a, turn)
    if a == nil then return nil end
    local sq = a:getSquare()
    if sq ~= nil and spotOk(sq) then return sq end
    return B.SpotNear(a:getX(), a:getY(), a:getZ(), tonumber(B.CFG.swapRing) or 2, turn)
end

local function sgn(v)
    if v > 0 then return 1 end
    if v < 0 then return -1 end
    return 0
end

-- Kommt man von sq Schritt fuer Schritt (hoechstens 3) zur Kachel (ox, oy), ohne dass etwas dazwischen sperrt?
local function reach(cell, sq, ox, oy, z)
    local cur = sq
    for _ = 1, 3 do
        local cx, cy = cur:getX(), cur:getY()
        if cx == ox and cy == oy then return true end
        local nxt = cell:getGridSquare(cx + sgn(ox - cx), cy + sgn(oy - cy), z)
        if nxt == nil or cur:isBlockedTo(nxt) then return false end
        cur = nxt
    end
    return cur:getX() == ox and cur:getY() == oy
end

-- Kachel i (0 .. 8k-1) des Rings k, im Uhrzeigersinn ab (-k, -k).
local function ringCell(k, i)
    local side = 2 * k
    if i < side then return -k + i, -k end
    i = i - side
    if i < side then return k, -k + i end
    i = i - side
    if i < side then return k - i, k end
    i = i - side
    return -k, k - i
end

function B.SpotNear(x, y, z, r, turn)
    if x == nil or y == nil then return nil end
    local cx, cy, cz = math.floor(x), math.floor(y), math.floor(z or 0)
    r = math.floor(tonumber(r) or 1)
    if r < 1 then r = 1 end
    if r > 3 then r = 3 end
    local t = math.floor(tonumber(turn) or 0)
    if t < 0 then t = -t end
    local cell = getCell()
    local osq = cell:getGridSquare(cx, cy, cz)
    if osq == nil then return nil end
    local room = osq:getRoom()
    for k = 1, r do
        local n = 8 * k
        local start = t * 3
        start = start - math.floor(start / n) * n
        for j = 0, n - 1 do
            local i = start + j
            if i >= n then i = i - n end
            local dx, dy = ringCell(k, i)
            local sq = cell:getGridSquare(cx + dx, cy + dy, cz)
            if spotOk(sq) and sq:getRoom() == room and reach(cell, sq, cx, cy, cz) then return sq end
        end
    end
    return nil
end

-- F1 (PLAN_F1.md 2.4, 5.5): Zufallsziel fuer "Frei herumlaufen". Mittelpunkt = Heimat rec.hx/hy/hz (fehlt: rec.x/y/z), Kachel-Mitte.
-- Bis B.CFG.tries Versuche: Winkel ZombRandFloat(0, 2 pi) und Abstand ZombRandFloat(0, r) (Form B.PickForestSquare oben, Bandits
-- server/BanditServerSpawner.lua:217; zwei Zahlen wie Vanilla server/Foraging/forageServer.lua:98), Kachel getCell():getGridSquare
-- (Vanilla server/Animal/ISPickDungCursor.lua:104). Gilt nur, wenn: Kachel-Mitte hoechstens r vom Mittelpunkt (nie hinaus), spotOk
-- (Platzregeln wie B.SpotNear: Boden, kein Wasser/Baum, frei, kein Fahrzeug), mindestens roamMinStep vom Tier, und drinnen/draussen wie
-- der Mittelpunkt: (sq:getRoom() == nil) == (Mitte:getRoom() == nil) -- getRoom wie Vanilla shared/Util/AdjacentFreeTileFinder.lua:240.
-- getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576. Rueckgabe: Kachel oder nil (dann Pause, neuer Versuch).
function B.RoamSpot(rec, a, r)
    if type(rec) ~= "table" or a == nil then return nil end
    r = tonumber(r)
    if r == nil or r <= 0 then return nil end
    local hx, hy, hz = tonumber(rec.hx), tonumber(rec.hy), tonumber(rec.hz)
    if hx == nil or hy == nil then hx, hy, hz = tonumber(rec.x), tonumber(rec.y), tonumber(rec.z) end
    if hx == nil or hy == nil then return nil end
    hx, hy, hz = math.floor(hx), math.floor(hy), math.floor(hz or 0)
    local cell = getCell()
    local center = cell:getGridSquare(hx, hy, hz)
    if center == nil then return nil end
    local inside = center:getRoom() ~= nil
    local mx, my = hx + 0.5, hy + 0.5
    local ax, ay = a:getX(), a:getY()
    local minStep = tonumber(B.CFG.roamMinStep) or 3
    for _ = 1, B.CFG.tries do
        local theta = ZombRandFloat(0, 2 * math.pi)
        local d = ZombRandFloat(0, r)
        local x = math.floor(mx + d * math.cos(theta))
        local y = math.floor(my + d * math.sin(theta))
        if B.DistXY(x + 0.5, y + 0.5, mx, my) <= r and B.DistXY(x + 0.5, y + 0.5, ax, ay) >= minStep then
            local sq = cell:getGridSquare(x, y, hz)
            if sq ~= nil and spotOk(sq) and (sq:getRoom() ~= nil) == inside then return sq end
        end
    end
    return nil
end

-- B1c (PLAN_B1C.md 3.4): Kachel eines TOTEN Spielers mit diesem Schluessel (Besitzer starb im Auto). Rueckgabe x, y, z oder nil.
-- Server: getOnlinePlayers() :size() / :get(i) (Vanilla server/Foraging/forageServer.lua:463-466); Einzelspieler:
-- getNumActivePlayers() (client/Fishing/FishingHandler.lua:6), getSpecificPlayer(i) (server/BuildingObjects/ISBuildingObject.lua:183).
-- isDead am Spieler: server/XpSystem/XpUpdate.lua:298; getX/getY am Spieler: Bandits server/BanditServerSpawner.lua:179, getZ :191.
-- Ob eine tote Figur dort noch steht, ist ungeprueft (PLAN_B1C.md 12) -- steht sie nicht, bleibt das Junge "ride" (F3).
function B.DeadAt(key)
    if key == nil then return nil end
    if isServer() then
        local online = getOnlinePlayers()
        if not online then return nil end
        for i = 0, online:size() - 1 do
            local p = online:get(i)
            if p and p:isDead() and B.PlayerKey(p) == key then
                return math.floor(p:getX()), math.floor(p:getY()), math.floor(p:getZ())
            end
        end
        return nil
    end
    if key ~= B.SP_KEY then return nil end
    for i = 0, getNumActivePlayers() - 1 do
        local p = getSpecificPlayer(i)
        if p and p:isDead() then
            return math.floor(p:getX()), math.floor(p:getY()), math.floor(p:getZ())
        end
    end
    return nil
end

-- B1c (PLAN_B1C.md 1.3, 6.3): naechster lebender Nicht-Bandit-Zombie auf gleicher Ebene in r Kacheln je Punkt.
-- points = { { x, y, z }, ... }. Rueckgabe: Liste (gleich lang wie points) aus { x, y, d } oder false; hot (irgendeiner gefunden);
-- partial (die Zellenliste war laenger als maxN: nur ein Teil angesehen, rollender Anfang B._zedFrom).
-- Wege (alle Bandits-belegt, Vanilla-Lua ruft getZombieList nicht):
--   SP mit Bandits: BanditZombie.CacheLightZ (Lua-Tabelle id -> { x, y, z, ... }, nur Zombies OHNE Banditen, je OnZombieUpdate frisch:
--     Bandits client/BanditZombie.lua:12, :60-87). Kein Engine-Aufruf. Leer -> Zellenliste.
--   sonst: getCell():getZombieList(), :size(), :get(i) (Bandits server/BanditSave.lua:15-18, :46-47; SP + Server); je Zombie
--     getX/getY (Bandits client/BanditZombie.lua:69-71); nur in r eines Punktes zusaetzlich getZ (gleiche ganze Ebene), isAlive
--     (Bandits server/BanditSave.lua:52), BanditCompatibility.IsReanimatedForGrappleOnly (Bandits shared/BanditCompatibility.lua:187,
--     gerufen client/BanditZombie.lua:118; Riegel: nur mit Bandits und -- Nachbesserung B1c A2 -- nur im Einzelspieler, denn Bandits
--     ruft es nur clientseitig; am Server zaehlt isAlive) und "kein Bandit": SP getVariableBoolean("Bandit") (Bandits
--     client/BanditZombie.lua:74), Server GetBanditClusterData(BanditUtils.GetZombieID(z))[id] (Bandits server/BanditSave.lua:55-57;
--     Riegel). Ohne Bandits gibt es keine Banditen (und NPC-Crew-Figuren sind Banditen).
-- Nachbesserung B1c B8 (Kosten): einmal je Aufruf der Rahmen aller Punkte +- r; je Zombie zuerst vier Vergleiche, nur im Rahmen die
-- Punktschleife (vorher jeder Zombie gegen jedes Junge).
local function isBanditZ(zb)
    if B.IsSP() then return zb:getVariableBoolean("Bandit") == true end
    local bu = BanditUtils
    local gcd = GetBanditClusterData
    if bu and bu.GetZombieID and gcd then
        local id = bu.GetZombieID(zb)
        local gmd = gcd(id)
        if gmd and gmd[id] then return true end
    end
    return false
end

local function zedTake(res, points, n, zx, zy, zz, r2)
    local hit = false
    for i = 1, n do
        local p = points[i]
        local dx, dy = zx - p.x, zy - p.y
        local d2 = dx * dx + dy * dy
        if d2 <= r2 and math.floor(zz) == math.floor(p.z or 0) then
            local d = math.sqrt(d2)
            local cur = res[i]
            if cur == false or d < cur.d then res[i] = { x = zx, y = zy, d = d } end
            hit = true
        end
    end
    return hit
end

local function anyNear(points, n, zx, zy, r2)
    for i = 1, n do
        local p = points[i]
        local dx, dy = zx - p.x, zy - p.y
        if dx * dx + dy * dy <= r2 then return true end
    end
    return false
end

function B.ZedNear(points, r, maxN)
    local res = {}
    local n = type(points) == "table" and #points or 0
    for i = 1, n do res[i] = false end
    if n == 0 then return res, false, false end
    r = tonumber(r) or 12
    maxN = math.floor(tonumber(maxN) or 1500)
    local r2 = r * r
    local hot = false
    -- B8: Rahmen aller Punkte +- r
    local x0, x1, y0, y1 = points[1].x - r, points[1].x + r, points[1].y - r, points[1].y + r
    for i = 2, n do
        local p = points[i]
        if p.x - r < x0 then x0 = p.x - r end
        if p.x + r > x1 then x1 = p.x + r end
        if p.y - r < y0 then y0 = p.y - r end
        if p.y + r > y1 then y1 = p.y + r end
    end
    -- SP mit Bandits: Lua-Tabelle (hoechstens 4 x maxN Eintraege ansehen)
    local bz = BanditZombie
    local cache = B.IsSP() and bz and bz.CacheLightZ or nil
    if type(cache) == "table" then
        local seen = 0
        for _, light in pairs(cache) do
            seen = seen + 1
            if seen > 4 * maxN then break end
            if type(light) == "table" then
                local zx, zy, zz = tonumber(light.x), tonumber(light.y), tonumber(light.z)
                if zx ~= nil and zy ~= nil and zz ~= nil and zx >= x0 and zx <= x1 and zy >= y0 and zy <= y1
                    and zedTake(res, points, n, zx, zy, zz, r2) then
                    hot = true
                end
            end
        end
        if seen > 0 then return res, hot, false end
    end
    local cell = getCell()
    local list = cell and cell:getZombieList()
    if not list then return res, false, false end
    local size = list:size()
    if size <= 0 then
        B._zedFrom = 0
        return res, false, false
    end
    local start = math.floor(tonumber(B._zedFrom) or 0)
    if start < 0 or start >= size then start = 0 end
    local count = size
    if count > maxN then count = maxN end
    local bc = BanditCompatibility
    local grapple = nil
    if B.IsSP() and bc then grapple = bc.IsReanimatedForGrappleOnly end      -- A2: nur im Einzelspieler (siehe Kopf)
    for k = 0, count - 1 do
        local idx = start + k
        if idx >= size then idx = idx - size end
        local zb = list:get(idx)
        if zb then
            local zx, zy = zb:getX(), zb:getY()
            if zx >= x0 and zx <= x1 and zy >= y0 and zy <= y1 and anyNear(points, n, zx, zy, r2) then
                local zz = zb:getZ()
                if zb:isAlive() and not (grapple and grapple(zb)) and not isBanditZ(zb) then
                    if zedTake(res, points, n, zx, zy, zz, r2) then hot = true end
                end
            end
        end
    end
    local nextFrom = start + count
    if nextFrom >= size then nextFrom = nextFrom - size end
    B._zedFrom = nextFrom
    return res, hot, size > maxN
end

-- ---------------------------------------------------------------------------
-- Tier erzeugen, entfernen, finden
-- ---------------------------------------------------------------------------

-- Rasse-Objekt zur Art. AnimalDefinitions.getDef(Artname-Text) und def:getBreedByName(Rasse-Text): Vanilla
-- server/ClientCommands.lua:808 (Server, direkt vor addAnimal) und shared/Definitions/animal/ButcheringUtil.lua:79/85 (mit
-- nil-Pruefung). Nachbesserung A3: vorher getAllAnimalsDefinitions/getBreeds, das nur Client-Belege hatte.
-- B1e (PLAN_B1E.md 6.2.3): je Koerper die Art (B.BODY_TYPE; unbekannt/nil -> Junges).
local function findBreed(body)
    local def = AnimalDefinitions.getDef(B.BODY_TYPE[body] or B.CUB)
    if def == nil then return nil end
    return def:getBreedByName(B.BREED)
end

-- B1c (PLAN_B1C.md 3.1): kann ein Koerper erzeugt werden? (Definition und Rasse geladen; sonst nicht einsteigen.)
-- B1e: body = "cub" / "big" (nil = "cub").
function B.CubDefOk(body)
    return findBreed(body) ~= nil
end

-- Die EINZIGE Stelle, die ein Tier in die Welt setzt. Gerufen nur von B.AppearFor und (B1c) B.PlaceCub. Rueckgabe: IsoAnimal oder nil, why.
-- addAnimal(getCell(), x, y, z, Art, Rasse-Objekt, false) und animal:addToWorld(): Vanilla server/ClientCommands.lua:809-810
-- (Server) und client/DebugUIs/DebugContextMenu.lua:1460-1467 (Einzelspieler). Derselbe Aufruf, aber von sich aus beim
-- Schreiber -- kein Client-Weg, kein Recht noetig, kein Kick. Koordinaten als ganze Zahlen; die Kachel hat der Aufrufer
-- mit B.SquareFits geprueft (kein Wasser).
-- B1e (PLAN_B1E.md 6.2.3): body = "cub" (Vorgabe, auch nil/unbekannt; wilde Junge) oder "big" -> Art B.BIG. Gleicher Aufruf, nur ein
-- anderer Artname (Text) -- wie Vanilla ClientCommands.lua:809 (args.type ist ein Text).
function B.CreateCub(x, y, z, body)
    if not B.IsWriter() then return nil, "nowriter" end
    if body ~= "big" then body = "cub" end
    local kind = B.BODY_TYPE[body] or B.CUB
    local breed = findBreed(body)
    if not breed then
        B.ErrEvery("nodef:" .. kind, 600000, "create: animal definition " .. tostring(kind) .. " is not loaded")
        return nil, "nodef"
    end
    local animal = addAnimal(getCell(), math.floor(x), math.floor(y), math.floor(z), kind, breed, false)
    if not animal then
        B.Err("create: addAnimal gave nothing at " .. tostring(x) .. "," .. tostring(y))
        return nil, "noanimal"
    end
    animal:addToWorld()
    -- KEINE Pruefung mit isExistInTheWorld direkt nach addToWorld (Kevins Test 10.11.2026: "no cub: notinworld", console.txt
    -- "[TC-BEAR] *** create: the new cub is not in the world"): die Engine haengt ein neues Tier erst beim naechsten Update in die
    -- Liste seiner Kachel (Jar 42.22.2 IsoAnimal.isExistInTheWorld = square.getMovingObjects().contains(this)); im selben Bild ist
    -- die Antwort deshalb immer falsch. Vanilla prueft hier auch nicht (server/ClientCommands.lua:809-810,
    -- client/DebugUIs/DebugContextMenu.lua:1466-1467), ebenso der gespielte Erwachsene (NCBearTest client/NCBearSpawn.lua:56).
    -- Fehlt das Tier wirklich, findet es der Suchlauf nicht und der Eintrag wird als verloren geschlossen.
    return animal, nil
end

-- Die EINZIGE Stelle, die ein Tier entfernt (Verschwinde-Regel, Aufraeumen). Nur unsere Art, nur beim Schreiber.
-- Erst die Bewegungssperre loesen (getBehavior():setBlockMovement(false): Vanilla
-- shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:28), dann animal:remove(): Vanilla
-- shared/Definitions/animal/ButcheringUtil.lua:609 (shared, laeuft auch auf dem Server), client/DebugUIs/DebugContextMenu.lua:616.
-- Auf dem Server zusaetzlich removeAnimal(animal:getOnlineID()), damit die Clients ihre Kopie verlieren -- genau wie
-- ButcheringUtil.lua:612-614 (isServer-Zweig nach remove(); Server-Befehl server/ClientCommands.lua:841). Im Einzelspieler
-- nur remove() (DebugContextMenu.lua:231-235 -> :616). Nachbesserung A1. remove() hinterlaesst keine Leiche.
-- B1e: beide Koerper (B.BodyKind), nie ein fremdes Tier ("bear", "bearstag", "ncbearcubalt").
function B.RemoveCub(animal)
    if not animal or not B.IsWriter() then return end
    if not B.BodyKind(animal) then return end
    animal:getBehavior():setBlockMovement(false)
    animal:remove()
    if isServer() then
        removeAnimal(animal:getOnlineID())
    end
end

-- Das in dieser Sitzung gemerkte Objekt eines Eintrags, mit Gegenprobe (in der Welt, lebt, Art, AnimalID). Sonst nil:
-- der naechste Suchlauf findet es. Raeumt nichts weg -- den Tod muss der Hirn-Takt am gemerkten Objekt noch sehen koennen.
-- isDead am Tier: Vanilla server/Traps/STrapGlobalObject.lua:238.
function B.FindAnimal(rec)
    if not rec then return nil end
    local s = B._s[rec.id]
    local a = s and s.obj
    if a == nil then return nil end
    if not a:isExistInTheWorld() or a:isDead() then return nil end
    if not B.BodyKind(a) then return nil end                -- B1e: beide Koerper
    if rec.aid ~= nil and a:getAnimalID() ~= rec.aid then return nil end
    return a
end

-- Suchlauf: alle geladenen Jungen ansehen und den Eintraegen ihre Objekte geben. Teuer (die Engine kopiert die ganze
-- Objektliste), deshalb nur bei Bedarf und fruehestens alle B.CFG.scanMs (das regelt der Hirn-Takt).
-- getCell():getObjectListForLua(), :size(), :get(i), instanceof(o, "IsoAnimal"): Vanilla
-- client/DebugUIs/DebugContextMenu.lua:612-615. Ein Server-Beleg fehlt (Vanilla server/, shared/ und Bandits: 0 Treffer):
-- im Mehrspieler OFFEN, Testpunkt (Plan 6.3; Nachbesserung A3). getAnimalID ebenso (nur Client-Belege, ISAnimalUI.lua:53).
-- Zuordnung ueber den Spiegel am Tier (id) mit Gegenprobe AnimalID. Rueckfall, wenn der Spiegel fehlt oder nicht passt
-- (jeder Client kann Tier-ModData ueberschreiben): gleiche AnimalID, genau EIN Kandidat, hoechstens 40 Kacheln von der
-- letzten bekannten Kachel -- dann wird neu gestempelt. Mehrere Kandidaten: nichts (nie raten).
--
-- Ein Junges, dessen Spiegel auf einen GESCHLOSSENEN Eintrag zeigt und das dabei noch ungefuettert war (mark.st new/shy),
-- ist ein schon "weitergezogenes" Tier aus einer damals nicht geladenen Gegend (server/BanditsNPCBearServer.lua slowRec):
-- es wird ueber B.RemoveCub entfernt, sobald niemand naeher als B.CFG.vanishKeep steht und es keiner sieht.
-- B1c (PLAN_B1C.md 2): Tiere mit Spiegel ohne passenden Eintrag gehen durch B.HealFromMark (server/BanditsNPCBearHeal.lua):
-- binden, wiederherstellen (Registerverlust), oder als veraltete Kopie / Doppel unbeobachtet entfernen; "nil" bleibt stehen.
--
-- B1b (PLAN_B1B.md 4, N5): WAISEN. Eine Waise ist ein lebendes ncbearcub (B1e: oder ncbeargrown) OHNE Spiegel und ohne passenden
-- Eintrag (Rest nach einem Fehler oder Absturz). Nie der Erwachsene, nie fremde Tiere (Art-Frage oben). Drei Riegel, alle Pflicht:
--   1 Identitaet: das in dieser Sitzung gemerkte Objekt eines Eintrags (B._s[id].obj) ist nie Waise; fehlt sein Spiegel, wird er
--     sofort ueber B.Commit geschrieben (Spiegel-Reparatur).
--   2 Mehrdeutig: gleiche AnimalID wie ein Eintrag ohne lebendes Objekt -> nie entfernt (nie raten; strenger als der Rueckfall,
--     der nur bis 40 Kacheln bindet), eine Diagnose-Zeile, wenn der Rueckfall mehrere Kandidaten hatte.
--   3 Alter und Beobachter: entfernt erst, wenn dasselbe Objekt schon bei einem frueheren Suchlauf vor mindestens
--     B.CFG.orphanAgeMs Waise war (Liste B._orph, Deckel B.CFG.orphanMax, Vergleich mit ==), UND niemand naeher als
--     B.CFG.vanishKeep steht, UND es im Einzelspieler keiner sieht. force ueberspringt NUR das Alter (der Spielcode ruft nie mit force).
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456. B.ScanAnimals gibt n (gebunden), removed (entfernte Waisen).

-- Eine Waise entfernen, wenn niemand naeher als vanishKeep steht und sie (SP) keiner sieht. Rueckgabe: true, wenn entfernt.
-- Nur ueber B.RemoveCub (einzige Entfern-Stelle; im MP mit removeAnimal).
local function dropOrphan(o, players)
    local nd = nearestDist(o:getX(), o:getY(), players)
    if (nd ~= nil and nd < B.CFG.vanishKeep) or B.SeenInSP(o:getSquare(), players) then return false end
    local x, y = math.floor(o:getX()), math.floor(o:getY())
    B.RemoveCub(o)
    B.Log("scan: removed an orphan cub (no mark, no entry) at " .. x .. "," .. y)
    return true
end

local function sweepOrphans(found, players, force, ms)
    local old = B._orph
    if type(old) ~= "table" then old = {} end
    local cap = tonumber(B.CFG.orphanMax) or 16
    local keep = {}
    local taken = {}
    local removed = 0
    -- zuerst die schon bekannten Waisen (sie sind der Entfernung naeher)
    for i = 1, #found do
        local o = found[i]
        for k = 1, #old do
            local e = old[k]
            if type(e) == "table" and e.o == o then
                taken[i] = true
                local at = tonumber(e.at)
                if at == nil or ms - at < 0 then at = ms end          -- Uhr rueckwaerts: Messung neu beginnen
                if (force == true or ms - at >= B.CFG.orphanAgeMs) and dropOrphan(o, players) then
                    removed = removed + 1
                elseif #keep < cap then
                    keep[#keep + 1] = { o = o, at = at }
                end
                break
            end
        end
    end
    -- dann neue, solange der Deckel Platz hat (auch Plaetze, die eben frei wurden); force entfernt sie gleich
    for i = 1, #found do
        if not taken[i] then
            local o = found[i]
            if force == true and dropOrphan(o, players) then
                removed = removed + 1
            elseif #keep < cap then
                keep[#keep + 1] = { o = o, at = ms }
            end
        end
    end
    B._orph = keep
    return removed
end

-- B1c (PLAN_B1C.md 2.6): Spiegel reparieren (Riegel 1) ueber B.WriteMark, wenn er nicht mehr frisch ist (B.MarkFresh); ohne
-- server/BanditsNPCBearHeal.lua der B1b-Weg ueber B.Commit.
local function repairMark(own, mark, hasMark, id, o)
    local fresh = B.MarkFresh
    if fresh then
        if fresh(own, mark) then return end
        B.WriteMark(own, o)
    else
        if hasMark and mark.id == id then return end
        B.Commit(own)
    end
    B.Log("scan: mark of " .. tostring(id) .. " written anew (the animal is the one of this session)")
end

-- Eine veraltete Kopie / ein Doppel entfernen, wenn niemand naeher als vanishKeep steht und es (SP) keiner sieht (wie Waisen
-- Riegel 3, ohne Alters-Frist; PLAN_B1C.md 2.5). Sonst bleibt es ungebunden stehen (kein Schild, das Menue lehnt ab).
local function dropCopy(o, players, why)
    local nd = nearestDist(o:getX(), o:getY(), players)
    if (nd ~= nil and nd < B.CFG.vanishKeep) or B.SeenInSP(o:getSquare(), players) then return false end
    local x, y = math.floor(o:getX()), math.floor(o:getY())
    B.RemoveCub(o)
    B.Log("scan: removed a cub copy (" .. tostring(why) .. ") at " .. x .. "," .. y)
    return true
end

-- Nachbesserung B1c B3: Reihenfolge der Heilung -- hoehere Koerper-Generation zuerst, dann hoeheres r, sonst die Listen-Reihenfolge
-- (e.i), damit table.sort (nicht stabil) bei Gleichstand immer gleich entscheidet. Eine strenge Ordnung (nie "a vor a").
local function newerFirst(p, q)
    local gp, gq = tonumber(p.mark.gen) or 0, tonumber(q.mark.gen) or 0
    if gp ~= gq then return gp > gq end
    local rp, rq = tonumber(p.mark.r) or 0, tonumber(q.mark.r) or 0
    if rp ~= rq then return rp > rq end
    return p.i < q.i
end

-- B1c-Reihenfolge je Suchlauf (PLAN_B1C.md 2.6):
--   1 je lebendes ncbearcub / ncbeargrown (B1e): Riegel 1 (Objekt der Sitzung) -> gebunden, Spiegel reparieren; sonst mit Spiegel ->
--     marked (v2 aus DIESEM Register: Zaehler nachziehen), ohne Spiegel -> loose
--   2 AnimalID-Rueckfall (B1b) fuer Eintraege ohne lebendes Objekt und ohne ride, ueber loose UND marked; ein marked mit anderem
--     Kennzeichen u oder kleinerer Generation gen ist KEIN Kandidat
--   3 je verbliebenem marked: B.HealFromMark -> rec (gebunden / wiederhergestellt) / "stale" / "dup" / nil (bleibt, nie entfernt)
--   4 "stale"/"dup" unbeobachtet entfernen
--   5 Waisen (ohne Spiegel) wie B1b
-- Rueckgabe n (gebunden + wiederhergestellt), removed (Waisen + veraltete Kopien + Doppel).
-- B1e (PLAN_B1E.md 3.2 Nr. 10, 4.3): der Suchlauf sieht BEIDE Koerper (B.BodyKind) -- sonst bliebe eine veraltete grosse Kopie nach
-- einem Absturz fuer immer stehen (Doppel). Der AnimalID-Rueckfall setzt rec.body nach dem gefundenen Tier (nur gezaehmt/vermisst).
function B.ScanAnimals(players, force)
    local reg = B.Reg()
    if not reg then return 0, 0 end
    local list = getCell():getObjectListForLua()
    if not list then return 0, 0 end
    players = players or B.Players()
    B._aidSeen = {}                             -- F1: [id] = true, je Suchlauf neu (Deckel: Zahl der Eintraege); liest B.ReviveMissing
    local n = 0
    local loose = nil                           -- Tiere ohne Spiegel (Waisen-Kandidaten)
    local marked = nil                          -- { o, mark } mit Spiegel, ungebunden
    for i = 0, list:size() - 1 do
        local o = list:get(i)
        if instanceof(o, "IsoAnimal") and B.BodyKind(o) ~= nil and not o:isDead() then
            -- F1 (Zusatz "F1 KERN"): der Suchlauf hat in dieser Sitzung einen unserer Baeren gesehen -- erst dann darf die Rueckkehr C1
            -- im Mehrspieler einen neuen Koerper erzeugen (A3: getObjectListForLua am MP-Server unbelegt; ohne Beweis kein Doppel)
            B._scanSeen = true
            local md = o:getModData()
            local mark = md and md[B.MARK]
            local hasMark = type(mark) == "table" and mark.id ~= nil
            local bound = false
            -- Riegel 1 (Identitaet + Spiegel-Reparatur)
            for id, s in pairs(B._s) do
                if s.obj == o then
                    local own = reg.cubs[id]
                    if own then
                        bound = true
                        n = n + 1
                        repairMark(own, mark, hasMark, id, o)
                    end
                    break
                end
            end
            if not bound then
                if hasMark then
                    marked = marked or {}
                    marked[#marked + 1] = { o = o, mark = mark }
                    local v = tonumber(mark.v)
                    if v ~= nil and v >= 2 and mark.ep == reg.ep then B.BumpN(mark.nr) end
                else
                    loose = loose or {}
                    loose[#loose + 1] = o
                end
            end
        end
    end
    -- 2: Rueckfall ueber die AnimalID fuer jeden Eintrag OHNE lebendes Objekt (B1b: auch, wenn das gemerkte Objekt nicht mehr in der
    -- Welt ist). Ein mitfahrender Eintrag (ride) hat keinen Koerper und ist nie Kandidat.
    local guard = nil                           -- Riegel 2: [j] = true -> dieses lose Tier wird nie entfernt
    if loose or marked then
        local nl, nm = 0, 0
        if loose then nl = #loose end
        if marked then nm = #marked end
        for id, rec in pairs(reg.cubs) do
            local s = B._s[id]
            local live = s ~= nil and s.obj ~= nil and s.obj:isExistInTheWorld() and not s.obj:isDead()
            if not live and rec.ride == nil then
                local hit, hitL, hitM, hits = nil, nil, nil, 0
                for j = 1, nl do
                    local o = loose[j]
                    if o and o:getAnimalID() == rec.aid then
                        guard = guard or {}
                        guard[j] = true
                        -- F1 (Zusatz "F1 KERN"): ein ungebundenes Tier mit der AnimalID dieses Eintrags ist geladen (auch
                        -- weiter als 40 oder mehrdeutig) -- die Rueckkehr C1 erzeugt dann KEINEN neuen Koerper (der echte
                        -- Koerper bliebe sonst als Waise zurueck)
                        B._aidSeen[id] = true
                        if B.DistXY(o:getX(), o:getY(), rec.x, rec.y) <= 40 then
                            hit, hitL, hitM = o, j, nil
                            hits = hits + 1
                        end
                    end
                end
                for j = 1, nm do
                    local e = marked[j]
                    if e then
                        local mu = tonumber(e.mark.u)
                        local mg = tonumber(e.mark.gen) or 0
                        local sameBody = mu == nil or (mu == rec.u and mg >= (tonumber(rec.gen) or 0))
                        if sameBody and e.o:getAnimalID() == rec.aid and B.DistXY(e.o:getX(), e.o:getY(), rec.x, rec.y) <= 40 then
                            hit, hitL, hitM = e.o, nil, j
                            hits = hits + 1
                        end
                    end
                end
                if hits == 1 then
                    B.Ses(id).obj = hit
                    if hitL then loose[hitL] = false end
                    local newer = nil
                    if hitM then
                        newer = marked[hitM].mark
                        marked[hitM] = false
                    end
                    -- Nachbesserung B1c B1: traegt das Tier einen NEUEREN Spiegel als der Eintrag (Register aelter als die Zelle nach
                    -- einem Absturz), gewinnt im Einzelspieler der Spiegel (server/BanditsNPCBearHeal.lua B.TakeNewerMark) -- sonst
                    -- schriebe B.Commit den alten Stand ueber die Zaehmung
                    if newer ~= nil and B.TakeNewerMark then
                        B.TakeNewerMark(rec, newer)
                        local ng = tonumber(newer.gen)
                        if ng ~= nil and ng > (tonumber(rec.gen) or 0) then rec.gen = ng end
                    end
                    -- B1e (PLAN_B1E.md 4.1): Koerper = Art des gefundenen Tiers (vor dem Commit, damit der Spiegel ihn traegt)
                    if rec.st == "tame" or rec.st == "missing" then rec.body = B.BodyKind(hit) end
                    n = n + 1
                    B.Commit(rec)
                    B.Log("scan: " .. id .. " found again by its animal id, mark written anew")
                elseif hits > 1 then
                    B.Log("scan: " .. id .. " has " .. hits .. " animals with its animal id nearby: none bound, none removed")
                end
            end
        end
    end
    -- 3: Heilung je verbliebenem Tier mit Spiegel (server/BanditsNPCBearHeal.lua); fehlt die Datei, bleiben sie unberuehrt.
    -- Nachbesserung B1c B3: zuerst die NEUESTEN Koerper (gen absteigend, dann r absteigend, sonst die Reihenfolge der Liste) -- sonst
    -- wird bei verlorenem Register eine alte Kopie zuerst hergestellt und der echte Koerper als Doppel entfernt.
    -- table.sort mit Vergleichsfunktion (Lua-Bibliothek): Vanilla shared/NPCs/MainCreationMethods.lua:127, wie B.BuildView.
    local copies = nil
    local heal = B.HealFromMark
    if marked and heal then
        local rest = {}
        for j = 1, #marked do
            local e = marked[j]
            if e then
                e.i = j
                rest[#rest + 1] = e
            end
        end
        if #rest > 1 then table.sort(rest, newerFirst) end
        for j = 1, #rest do
            local e = rest[j]
            local got = heal(e.o, e.mark, players)
            if type(got) == "table" then
                n = n + 1
            elseif got == "stale" or got == "dup" then
                copies = copies or {}
                copies[#copies + 1] = { o = e.o, why = got }
            end
        end
    end
    -- 4: erst nach dem Durchlauf entfernen (die Liste ist eine Kopie, trotzdem nie waehrend des Lesens aendern)
    local removed = 0
    if copies then
        for j = 1, #copies do
            if dropCopy(copies[j].o, players, copies[j].why) then removed = removed + 1 end
        end
    end
    -- 5: Waisen
    local found = {}
    if loose then
        for j = 1, #loose do
            local o = loose[j]
            if o and not (guard and guard[j]) then found[#found + 1] = o end
        end
    end
    removed = removed + sweepOrphans(found, players, force, getTimestampMs())
    return n, removed
end

-- ---------------------------------------------------------------------------
-- Halten und Laufen (Plan 6.7)
-- ---------------------------------------------------------------------------

-- Stehenbleiben. getBehavior():setBlockMovement(b): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:89,
-- shared/TimedActions/Animals/ISPetAnimal.lua:36. Die Engine loest die Sperre nach einer Weile von selbst (haengt nie
-- endlos); deshalb setzt der Hirn-Takt sie jeden Takt neu, solange sie gelten soll.
-- B1c Ruhefrist (PLAN_B1C.md 0.4, 1.2 Schritt 3): nach einer Laerm-Antwort (s.calmUntil) wird die Sperre NICHT erneuert --
-- setBlockMovement(true) ruft in der Engine stopAllMovementNow (Jar dec/BaseAnimalBehavior.java:1739-1747) und loescht damit das
-- "Schild", das den Ersatzweg vor einer neuen Flucht schuetzt. Kein Engine-Aufruf, s.held bleibt, wie es ist.
function B.Hold(rec, animal, on)
    if not rec or not animal then return end
    local s = B.Ses(rec.id)
    if on == true and s.calmUntil ~= nil then
        local ms = getTimestampMs()                 -- Vanilla server/Foraging/forageServer.lua:456
        local left = s.calmUntil - ms
        if left > 0 and left <= (tonumber(B.CFG.calmMs) or 2500) then return end
    end
    animal:getBehavior():setBlockMovement(on == true)
    if on == true then
        s.held = true
        s.chk = nil
    else
        s.held = nil
    end
end

-- Die Zielkachel und bis zu vier gedrehte Ersatzpunkte (Bogenmass).
local TURN = { 0, 0.6, -0.6, 1.2, -1.2 }

-- Zu einem Punkt rennen. animal:fleeTo(square): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:38 (laeuft dort auch auf
-- dem Server). Derselbe Befehl fruehestens nach B.CFG.moveMs. Zielkachel nicht geladen oder Wasser: Ersatzpunkte, dann nichts.
-- opt (B1b, wahlfrei): opt.minMs ersetzt B.CFG.moveMs; opt.watch == false -> keine Gegenprobe (B.MoveWatch), weil beim Folgen
-- ein Halt vor einer Tuer kein Fehler ist. Ohne opt wie B1a.
-- B1c (PLAN_B1C.md 0.6, 6.3): opt.force == true ueberspringt die Drossel (Laerm-Antwort im selben Bild). opt.walk == true: GEHEN
-- statt rennen -- animal:setVariable("animalRunning", false) DANN animal:pathToLocation(x, y, z) mit den ganzen Zahlen der gewaehlten
-- Kachel (gleiche TURN-/Wasser-Wahl). Beide mit Kevins Wort (pathToLocation: 08.11.2026, forschung_engine.md:627;
-- setVariable("animalRunning", false): 11.11.2026, baer/begleiter/ENTSCHEIDUNGEN.md). setVariable(Text, Wahrheitswert) als Methode:
-- Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:139 (Spieler), Bandits shared/ZombieActions/ZAMove.lua:32 (Zombie);
-- pathToLocation(x, y, z) mit square:getX()/getY()/getZ(): Vanilla client/DebugUIs/DebugContextMenu.lua:636 (am Zombie). Reihenfolge
-- wie das Vanilla-Wandern (Jar dec/BaseAnimalBehavior.java:167, :224). Dies ist die EINZIGE Stelle mit beiden Aufrufen.
-- Jeder Befehl merkt s.ownUntil (eigener Befehl laeuft: Wegzeit + ownSlackMs, hoechstens ownMaxMs), s.walk und (B5) s.tx, s.ty, s.td0
-- (Zielkachel-Mitte, Abstand beim Befehl) fuer die Laerm-Wache.
-- Rueckgabe: true, wenn ein Befehl hinausging.
function B.MoveTo(rec, animal, x, y, z, opt)
    if not rec or not animal or x == nil or y == nil then return false end
    local ms = getTimestampMs()
    local s = B.Ses(rec.id)
    local minMs = B.CFG.moveMs
    local force, walk = false, false
    if type(opt) == "table" then
        if tonumber(opt.minMs) ~= nil then minMs = tonumber(opt.minMs) end
        force = opt.force == true
        walk = opt.walk == true
    end
    if not force and s.moveAt ~= nil and ms - s.moveAt >= 0 and ms - s.moveAt < minMs then return false end
    local ax, ay = animal:getX(), animal:getY()
    local dx, dy = x - ax, y - ay
    z = math.floor(z or 0)
    local cell = getCell()
    local sq = nil
    for i = 1, #TURN do
        local cs, sn = math.cos(TURN[i]), math.sin(TURN[i])
        local cand = cell:getGridSquare(math.floor(ax + dx * cs - dy * sn), math.floor(ay + dx * sn + dy * cs), z)
        if cand ~= nil and not isWater(cand) then
            sq = cand
            break
        end
    end
    if sq == nil then return false end
    if s.held then B.Hold(rec, animal, false) end
    if walk then
        animal:setVariable("animalRunning", false)
        animal:pathToLocation(sq:getX(), sq:getY(), sq:getZ())
    else
        animal:fleeTo(sq)
    end
    s.moveAt = ms
    local way = math.sqrt(dx * dx + dy * dy)
    -- B1e (PLAN_B1E.md 1.5, 6.2.3): Tempo des Koerpers (grosser Koerper: runSpeedBig / walkSpeedBig, shared/BanditsNPCBearStats.lua)
    local key = "runSpeed"
    if walk then key = "walkSpeed" end
    local speed = B.CFG[key]
    if B.BodyNum then speed = B.BodyNum(rec.body, key, 1) end
    speed = tonumber(speed) or 1
    if speed <= 0 then speed = 1 end
    local own = way / speed * 1000 + (tonumber(B.CFG.ownSlackMs) or 1500)
    local cap = tonumber(B.CFG.ownMaxMs) or 15000
    if own > cap then own = cap end
    s.ownUntil = ms + own
    s.walk = walk
    -- Nachbesserung B1c B5: Ziel und Abstand beim Befehl merken -- entfernt sich das Tier waehrend des eigenen Befehls deutlich davon,
    -- flieht es (B.CalmTick, server/BanditsNPCBearGuard.lua). Nur Zahlen, kein Engine-Aufruf mehr.
    s.tx, s.ty = sq:getX() + 0.5, sq:getY() + 0.5
    s.td0 = B.DistXY(ax, ay, s.tx, s.ty)
    -- Gegenprobe nur fuer Wege, die lang genug sind, um sie zu sehen
    if type(opt) == "table" and opt.watch == false then
        s.chk = nil
    elseif dx * dx + dy * dy >= 2.25 then
        s.chk = { x = ax, y = ay, n = 0 }
    else
        s.chk = nil
    end
    return true
end

-- Gegenprobe zum Laufbefehl, je Hirn-Takt: hat sich das Tier 3 Takte danach nicht bewegt, eine gedrosselte Zeile
-- (Diagnose, kein Abbruch).
function B.MoveWatch(rec, animal)
    local s = B._s[rec.id]
    local chk = s and s.chk
    if not chk then return end
    chk.n = chk.n + 1
    if chk.n < 3 then return end
    s.chk = nil
    if B.DistXY(chk.x, chk.y, animal:getX(), animal:getY()) < 0.3 then
        B.ErrEvery("still:" .. tostring(rec.id), 60000, "move: " .. tostring(rec.id) .. " did not move after a run order (fleeTo)")
    end
end
