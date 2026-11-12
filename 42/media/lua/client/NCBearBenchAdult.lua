--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert). Lauf baer-f2, PLAN_F2.md 1.1, 1.4. Frueher client/NCBearSpawn.lua und
-- client/NCBearSize.lua (heute Stummel). Nur Einzelspieler ("singleplayer only"); nichts hier laeuft je Bild.
--
-- Konsole:
--   NCBear_SpawnLive(typ)   ein lebender Test-Baer zwei Kacheln neben dir: Vorgabe "ncbear" (neue Test-Art, shared/NCBearBenchDefs.lua);
--                           "bear" / "bearstag" gehen noch (ALT-Arten, nur damit alte Spielstaende laden). Der Test-Baer KAEMPFT NICHT
--                           (Frage F-G5): Clips zeigen NCBear_AnimTest / NCBear_Sit / NCBear_Eat (client/NCBearBench.lua).
--   NCBear_Size(x)          Groesse der Test-Baeren in 20 Kacheln (setSizeForced; gilt, bis er einen Spieltag aelter wird)
--   NCBear_OldClean()       entfernt die ALTEN Test-Baeren (Arten bear / bearstag) in 30 Kacheln; deinen gezaehmten Baeren und die neue
--                           Test-Art ncbear fasst es nie an
-- Rechtsklick (Untermenue "NC Bear", Wirt client/NCBearBenchModel.lua): "Spawn living test bear here", "Remove living test bears nearby".
--
-- Engine-Aufrufe (Fundstelle; "gespielt" = gespielte alte Testhilfe NCBearSpawn.lua / NCBearSize.lua):
--   getAllAnimalsDefinitions(), def:getAnimalType(), def:getBreeds(), :size(), :get(i): V:client/DebugUIs/DebugContextMenu.lua:246-275
--   addAnimal(getCell(), x, y, z, typ, breed, false) + animal:addToWorld(): V:client/DebugUIs/DebugContextMenu.lua:1460-1467
--   square:getFloor() + floor:hasProperty(IsoFlagType.water): V:client/ISUI/ISWorldObjectContextMenu.lua:687-688
--   getCell():getObjectListForLua(), instanceof(x, "IsoAnimal"), animal:remove(): V:client/DebugUIs/DebugContextMenu.lua:612-616
--   animal:getAnimalType(): V:client/ISUI/Animal/ISAnimalUI.lua:65; animal:getSquare(): V:client/ISUI/Animal/ISAnimalContextMenu.lua:90
--   animal:getData():setSizeForced(x): V:shared/Definitions/animal/ButcheringUtil.lua:569
--   getSpecificPlayer(0): V:client/DebugUIs/DebugContextMenu.lua:917; getCurrentSquare(): :344; getCell():getGridSquare(x, y, z): :1432
--   sub:addOption(Text, Ziel, Funktion): V:client/DebugUIs/AdminContextMenu.lua:46 (gespielt NCBearSpawn.lua:94-98)
-- Statisch geprueft, nicht gespielt.
--

local RADIUS = 12           -- Entfernen per Rechtsklick
local SIZE_RADIUS = 20      -- NCBear_Size
local OLD_RADIUS = 30       -- NCBear_OldClean
local ARTEN = { ncbear = true, bear = true, bearstag = true }
local OLD = { bear = true, bearstag = true }

-- Vanillas eigener Test: V:shared/TimedActions/ISEatFoodAction.lua:136
local function isSP()
    return not isClient() and not isServer()
end

local function say(s)
    print("[NCBear] " .. s)
end

-- Rasse einer Art aus der Liste, die auch das Debug-Menue liest (DebugContextMenu.lua:250-280)
local function findBreed(typ)
    local defs = getAllAnimalsDefinitions()
    for i = 0, defs:size() - 1 do
        local def = defs:get(i)
        if def:getAnimalType() == typ then
            local breeds = def:getBreeds()
            if breeds:size() > 0 then return breeds:get(0) end
        end
    end
    return nil
end

-- Wasser: dort bleibt ein Tier uninitialisiert (alte NCBearSpawn.lua). Form ISWorldObjectContextMenu.lua:683-689
local function isWater(square)
    local floor = square:getFloor()
    return floor ~= nil and floor:hasProperty(IsoFlagType.water)
end

local function spawnLive(square, typ)
    if not square then return nil end
    if not isSP() then
        say("singleplayer only")
        return nil
    end
    if isWater(square) then
        say("not on water")
        return nil
    end
    local breed = findBreed(typ)
    if not breed then
        say("animal definition not loaded: " .. typ .. " (shared/NCBearBenchDefs.lua)")
        return nil
    end
    -- Einzelspieler-Zweig von DebugContextMenu.AddAnimal (DebugContextMenu.lua:1460-1467)
    local animal = addAnimal(getCell(), square:getX(), square:getY(), square:getZ(), typ, breed, false)
    if not animal then
        say("addAnimal gave nothing for " .. typ)
        return nil
    end
    animal:addToWorld()
    say("living test bear " .. typ .. " at " .. square:getX() .. "," .. square:getY() .. "," .. square:getZ()
        .. " (it does not fight; your own bear does: NCBear_FightZed)")
    return animal
end

-- Lebende Test-Baeren der Arten in kinds um die Kachel (gleiche Ebene, Quadrat r), rueckwaerts entfernt (DebugContextMenu.lua:612-616).
local function removeAround(cx, cy, cz, r, kinds)
    local list = getCell():getObjectListForLua()
    local n = 0
    for i = list:size(), 1, -1 do
        local animal = list:get(i - 1)
        if instanceof(animal, "IsoAnimal") and kinds[animal:getAnimalType()] then
            local sq = animal:getSquare()
            if sq and sq:getZ() == cz and math.abs(sq:getX() - cx) <= r and math.abs(sq:getY() - cy) <= r then
                animal:remove()
                n = n + 1
            end
        end
    end
    return n
end

local function removeLive(square)
    if not square then return end
    if not isSP() then
        say("singleplayer only")
        return
    end
    local n = removeAround(square:getX(), square:getY(), square:getZ(), RADIUS, ARTEN)
    -- Nur lebende und geladene Test-Baeren: Leichen und weggelaufene bleiben (alte NCBearSpawn.lua:76-78).
    say("removed " .. n .. " living test bear(s) within " .. RADIUS .. " tiles; corpses and bears further away stay")
end

local function onSpawn(square)
    spawnLive(square, "ncbear")
end

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}
table.insert(NCBearMenu.extra, function(sub, square, _player)
    sub:addOption("Spawn living test bear here", square, onSpawn)       -- AdminContextMenu.lua:46
    sub:addOption("Remove living test bears nearby", square, removeLive)
end)

-- Konsole: zwei Kacheln neben die eigene Figur.
function NCBear_SpawnLive(typ)
    typ = typ or "ncbear"
    if not ARTEN[typ] then
        say("unknown type " .. tostring(typ) .. ", use ncbear (old saves: bear or bearstag)")
        return nil
    end
    local p = getSpecificPlayer(0)                      -- DebugContextMenu.lua:917
    if not p then
        say("no player yet")
        return nil
    end
    local here = p:getCurrentSquare()                   -- DebugContextMenu.lua:344
    if not here then
        say("player has no square")
        return nil
    end
    local sq = getCell():getGridSquare(here:getX() + 2, here:getY(), here:getZ()) or here   -- DebugContextMenu.lua:1432
    return spawnLive(sq, typ)
end

-- Groesse nachstellen (alte NCBearSize.lua, Kevin 08.11.: "ein echter waere viel groesser"). Nur Test-Arten, nie der eigene Baer.
function NCBear_Size(x)
    if not isSP() then
        say("singleplayer only")
        return
    end
    x = tonumber(x)
    if not x or x <= 0 then
        say("use NCBear_Size(1.5)")
        return
    end
    local p = getSpecificPlayer(0)
    if not p then return end
    local here = p:getCurrentSquare()
    if not here then return end
    local list = getCell():getObjectListForLua()
    local n = 0
    for i = list:size(), 1, -1 do
        local animal = list:get(i - 1)
        if instanceof(animal, "IsoAnimal") and ARTEN[animal:getAnimalType()] then
            local sq = animal:getSquare()
            if sq and math.abs(sq:getX() - here:getX()) <= SIZE_RADIUS and math.abs(sq:getY() - here:getY()) <= SIZE_RADIUS then
                animal:getData():setSizeForced(x)       -- V:shared/Definitions/animal/ButcheringUtil.lua:569
                n = n + 1
            end
        end
    end
    say("size " .. x .. " set on " .. n .. " test bear(s) within " .. SIZE_RADIUS .. " tiles (until the bear is a day older)")
end

-- Alte Test-Baeren (bear / bearstag) wegraeumen: danach speichern, dann braucht der Stand die ALT-Arten nicht mehr.
function NCBear_OldClean()
    if not isSP() then
        say("singleplayer only")
        return
    end
    local p = getSpecificPlayer(0)
    if not p then
        say("no player yet")
        return
    end
    local here = p:getCurrentSquare()
    if not here then
        say("player has no square")
        return
    end
    local n = removeAround(here:getX(), here:getY(), here:getZ(), OLD_RADIUS, OLD)
    say("removed " .. n .. " old test bear(s) (bear / bearstag) within " .. OLD_RADIUS .. " tiles -- your tamed bear and ncbear stay;"
        .. " save the game afterwards")
end
