--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert). Nur Einzelspieler.
-- Kevin 11.11.2026: "ich will das du die 2 baby varianten einbaust zum spawnen und beide grosse!"
--
-- Konsole (Debug):
--   NCBear_Vergleich()      alles nebeneinander: altes Junges (lebend), grosser 2c-Baer (lebend) und die zwei Standmodelle
--                           des grossen Generator-Baeren (braun und Fototon) ins Inventar zum Hinlegen
--   NCBear_CubAlt()         nur das alte Junge (lebend)
--   NCBear_GenE()           nur die zwei Standmodelle des Generator-Baeren ins Inventar
-- Das neue Junge ist dein gezaehmtes (gleiches Modell wie jedes neue Junge); ein weiteres holt NCBear_CubHere().
--
-- Engine-Aufrufe wie die gespielte Testhilfe client/NCBearSpawn.lua: getAllAnimalsDefinitions/getBreeds (Vanilla
-- client/DebugUIs/DebugContextMenu.lua:246-275), addAnimal + addToWorld (DebugContextMenu.lua:1462-1471),
-- getSpecificPlayer(0) (:24), getCurrentSquare (:348), getCell():getGridSquare (:1436),
-- getInventory():AddItem("Modul.Name") (Vanilla client/DebugUIs/Scenarios/AiteronScenario.lua:74 getPlayer():getInventory():AddItem("Base.FishingRod")).
--

local function sp()
    return not isServer() and not isClient()
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

local function spawnAt(dx, dy, typ)
    local p = getSpecificPlayer(0)
    if not p then print("[NCBear] no player yet"); return nil end
    local here = p:getCurrentSquare()
    if not here then print("[NCBear] player has no square"); return nil end
    local sq = getCell():getGridSquare(here:getX() + dx, here:getY() + dy, here:getZ()) or here
    local breed = findBreed(typ)
    if not breed then print("[NCBear] animal definition not loaded: " .. typ); return nil end
    local a = addAnimal(getCell(), sq:getX(), sq:getY(), sq:getZ(), typ, breed, false)
    if not a then print("[NCBear] addAnimal gave nothing for " .. typ); return nil end
    a:addToWorld()
    print("[NCBear] vergleich: " .. typ .. " at " .. sq:getX() .. "," .. sq:getY())
    return a
end

function NCBear_CubAlt()
    if not sp() then print("[NCBear] singleplayer only"); return end
    return spawnAt(2, -2, "ncbearcubalt")
end

function NCBear_GenE()
    if not sp() then print("[NCBear] singleplayer only"); return end
    local p = getSpecificPlayer(0)
    if not p then return end
    p:getInventory():AddItem("NCBear.BenchGenEBraun")
    p:getInventory():AddItem("NCBear.BenchGenEFototon")
    print("[NCBear] vergleich: 2 Standmodelle des Generator-Baeren im Inventar (brown, photo tone) -- auf den Boden legen")
end

function NCBear_Vergleich()
    if not sp() then print("[NCBear] singleplayer only"); return end
    NCBear_CubAlt()
    spawnAt(4, 2, "bear")
    NCBear_GenE()
    print("[NCBear] vergleich: altes Junges + grosser 2c-Baer stehen neben dir; das neue Junge ist dein eigenes (oder NCBear_CubHere())")
end
