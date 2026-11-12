--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Nur Einzelspieler (Konsole, Spiel
-- mit -debug). Lauf baer-gen-junges-v2, 12.11.2026. Kevin 12.11.: "starte noch einen workflow fuer den anderen baby baeren mach da auch das
-- gesicht besser und vorallem die beine" -- und "laeuft das andere baby anders als das was jz standard ist?". Das neue Generator-Junge kommt
-- nur als Vergleich per Testbefehl zurueck; es ist nie dein gezaehmtes Junges.
--
-- Arten (shared/NCBearBenchCubGenDefs.lua): "ncbearcubgen" = neues Generator-Junges, "ncbearcubstd" = Standard-Junges der Test-Mod (gleiches
-- Modell wie jedes neue Junge). Beide haben dieselbe Definition und werden nur von der Engine bewegt (kein Baeren-Kern) -- so sieht man
-- Gesicht, Beine und Gang direkt nebeneinander. Dein eigenes Junges (Art ncbearcub) fasst diese Datei nie an.
--
-- Konsole:
--   NCBear_CubGen()                 links das Standard-Junge, rechts das neue Generator-Junge, lebend 2 Kacheln vor dir, Blick zur Kamera.
--                                   Sie gehen ab und zu von selbst ein Stueck (wie das alte Junge von NCBear_CubAlt()).
--   NCBear_CubGenSize(x)            beide Vergleichs-Arten in 20 Kacheln auf Groesse x (0,35 .. 0,75; Vorgabe nach dem Erscheinen 0,35)
--   NCBear_CubGenSize(x, s)         das neue auf x, das Standard-Junge auf s (z. B. gleich lang: das neue ist bei gleicher Groesse kuerzer)
--   NCBear_CubGenClean()            entfernt ALLE geladenen lebenden Vergleichs-Jungen beider Arten (vor dem Entfernen der Testhilfe: das und
--                                   speichern; Vergleichs-Junge nicht toeten -- Leichen entfernt der Befehl nicht)
--
-- Engine-Aufrufe (Fundstelle; "gespielt" = gespielte Testhilfe der Test-Mod):
--   getAllAnimalsDefinitions, defs:size/get, def:getAnimalType, def:getBreeds, breeds:size/get: Vanilla client/DebugUIs/DebugContextMenu.lua:246-275
--     (gespielt NCBearBenchVergleich.lua findBreed)
--   addAnimal(getCell(), x, y, z, Art, Rasse-Objekt, false) + animal:addToWorld(): DebugContextMenu.lua:1460-1467 (gespielt NCBearBenchVergleich.lua:45-47)
--   getSpecificPlayer(0): DebugContextMenu.lua:917; player:getCurrentSquare(): :344; getCell():getGridSquare(x, y, z): :1432 und :899;
--   square:getX/getY/getZ: :1455-1457
--   square:getFloor() + floor:hasProperty(IsoFlagType.water): client/ISUI/ISWorldObjectContextMenu.lua:687-688 (gespielt NCBearSpawn.lua:30-32)
--   animal:setDir(IsoDirections.SE): shared/Definitions/animal/ButcheringUtil.lua:574 (NE), gespielt mit SE (NCBearBench.lua:296)
--   getCell():getObjectListForLua(), :size(), :get(i), instanceof(x, "IsoAnimal"), animal:remove(): DebugContextMenu.lua:611-616 (rueckwaerts)
--   animal:getAnimalType(): client/ISUI/Animal/ISAnimalUI.lua:65; animal:isDead(): client/ISUI/Hutch/ISHutchUI.lua:427
--   animal:getX()/getY(): ButcheringUtil.lua:575-576; player:getX()/getY(): DebugContextMenu.lua:921/:925
--   animal:getData():setSizeForced(Zahl): ButcheringUtil.lua:569-571 (gespielt NCBearBenchVergleich.lua:79 NCBear_CubAltSize)
-- Kein Takt, kein Ereignis: jeder Befehl sucht nur einmal (Deckel MAX_CUBS beim Erscheinen). Statisch geprueft, nicht gespielt.
--

local GEN = "ncbearcubgen"
local STD = "ncbearcubstd"
local ARTEN = { ncbearcubgen = true, ncbearcubstd = true }
local RADIUS = 20             -- NCBear_CubGenSize: Vergleichs-Junge in so vielen Kacheln um dich (wie NCBear_CubAltSize)
local MAX_CUBS = 8            -- Deckel: hoechstens so viele lebende Vergleichs-Junge in RADIUS, sonst erst NCBear_CubGenClean()
local SIZE_MIN = 0.35
local SIZE_MAX = 0.75
local FRONT = 2               -- Mitte der Reihe: so viele Kacheln vor dir (Bildschirm unten = Welt +x/+y, NCBearBenchGen.lua NCBear_GenLive)

-- Vanillas eigener Test (ISEatFoodAction.lua:136, wie NCBearBench.lua / NCBearBenchGen.lua)
local function isSP()
    return not isClient() and not isServer()
end

local function say(s)
    print("[NCBear] cubgen: " .. s)
end

local function player()
    local p = getSpecificPlayer(0)
    if not p then say("no player yet") end
    return p
end

local function isWater(square)
    local floor = square:getFloor()
    return floor ~= nil and floor:hasProperty(IsoFlagType.water)
end

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

-- Groesse in [SIZE_MIN, SIZE_MAX] oder nil
local function clampSize(v)
    v = tonumber(v)
    if v == nil then return nil end
    if v < SIZE_MIN then v = SIZE_MIN end
    if v > SIZE_MAX then v = SIZE_MAX end
    return v
end

-- Lebende Vergleichs-Junge (beide Arten) in RADIUS Kacheln um p. Rueckwaerts wie DebugContextMenu.lua:612-614.
local function cubsNear(p)
    local px, py = p:getX(), p:getY()
    local out = {}
    local list = getCell():getObjectListForLua()
    for i = list:size(), 1, -1 do
        local a = list:get(i - 1)
        if instanceof(a, "IsoAnimal") and ARTEN[a:getAnimalType()] and not a:isDead() then
            if math.abs(a:getX() - px) <= RADIUS and math.abs(a:getY() - py) <= RADIUS then
                out[#out + 1] = a
            end
        end
    end
    return out
end

-- Ein lebendes Tier an here + (dx, dy), Blick zur Kamera (wie NCBearBenchGen.lua spawnAt)
local function spawnAt(here, dx, dy, typ)
    local sq = getCell():getGridSquare(here:getX() + dx, here:getY() + dy, here:getZ())
    if not sq then
        say(typ .. ": square " .. dx .. "," .. dy .. " not loaded, skipped")
        return nil
    end
    if isWater(sq) then
        say(typ .. ": square " .. dx .. "," .. dy .. " is water, skipped (stand on open ground)")
        return nil
    end
    local breed = findBreed(typ)
    if not breed then
        say("animal definition not loaded: " .. typ .. " (shared/NCBearBenchCubGenDefs.lua)")
        return nil
    end
    local a = addAnimal(getCell(), sq:getX(), sq:getY(), sq:getZ(), typ, breed, false)
    if not a then
        say("addAnimal gave nothing for " .. typ)
        return nil
    end
    a:addToWorld()
    a:setDir(IsoDirections.SE)
    return a
end

-------------------------------------------------------------------------------------------------------------------------------

function NCBear_CubGen()
    if not isSP() then say("singleplayer only"); return end
    local p = player()
    if not p then return end
    local here = p:getCurrentSquare()
    if not here then say("player has no square"); return end
    local have = #cubsNear(p)
    if have + 2 > MAX_CUBS then
        say(have .. " comparison cubs within " .. RADIUS .. " tiles already (limit " .. MAX_CUBS .. ") -- NCBear_CubGenClean() first")
        return
    end
    -- Reihe quer ueber den Bildschirm (Bildschirm rechts = Welt +x/-y), FRONT Kacheln vor dir: links Standard, rechts neu
    local aStd = spawnAt(here, FRONT - 1, FRONT + 1, STD)
    local aGen = spawnAt(here, FRONT + 1, FRONT - 1, GEN)
    say("in front of you (left to right): standard cub " .. (aStd and "ok" or "MISSING") .. " | new generator cub "
        .. (aGen and "ok" or "MISSING") .. ", both size 0.35, facing the camera; they walk now and then by themselves")
    say("NCBear_CubGenSize(0.5) both to 0.5 (0.35 .. 0.75) | NCBear_CubGenSize(0.43, 0.35) new 0.43, standard 0.35 (about the same length)")
    say("SAVE WARNING: a saved comparison cub needs this test helper on load -- NCBear_CubGenClean() and save before removing it")
end

function NCBear_CubGenSize(x, s)
    if not isSP() then say("singleplayer only"); return end
    local xg = clampSize(x)
    if not xg then
        say("use NCBear_CubGenSize(0.5) or NCBear_CubGenSize(0.43, 0.35) -- new cub, standard cub (" .. SIZE_MIN .. " .. " .. SIZE_MAX .. ")")
        return
    end
    local xs = clampSize(s) or xg
    local p = player()
    if not p then return end
    local cubs = cubsNear(p)
    local nG, nS = 0, 0
    for _, a in ipairs(cubs) do
        if a:getAnimalType() == GEN then
            a:getData():setSizeForced(xg)
            nG = nG + 1
        elseif a:getAnimalType() == STD then
            a:getData():setSizeForced(xs)
            nS = nS + 1
        end
    end
    say("size new " .. xg .. " on " .. nG .. ", standard " .. xs .. " on " .. nS .. " comparison cub(s) within " .. RADIUS .. " tiles"
        .. ((nG + nS == 0) and " -- spawn them first: NCBear_CubGen()" or ""))
end

function NCBear_CubGenClean()
    if not isSP() then say("singleplayer only"); return end
    local list = getCell():getObjectListForLua()
    local n = 0
    for i = list:size(), 1, -1 do
        local a = list:get(i - 1)
        if instanceof(a, "IsoAnimal") and ARTEN[a:getAnimalType()] then
            a:remove()
            n = n + 1
        end
    end
    say("removed " .. n .. " living comparison cub(s); cubs further away (not loaded) and corpses stay -- your own cub stays")
end
