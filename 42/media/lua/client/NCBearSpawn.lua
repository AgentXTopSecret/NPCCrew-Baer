-- NC Bear Test: das lebende Tier spawnen und wieder entfernen. Kein Teil von NPC Crew, nicht fuer den Workshop.
-- Haengt sich mit drei Eintraegen in das Untermenue "NC Bear" (NCBearTest.lua). Nur Einzelspieler; im Mehrspieler
-- spawnt das Debug-Menue (Tiere, "Bear (NC test)"), dort fragt der Server die Rolle (ClientCommands.lua:754).
-- Nichts hier laeuft je Bild. Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben).

local RADIUS = 12
local ARTEN = { bear = true, bearstag = true }

-- Vanillas eigener Test: ISEatFoodAction.lua:136
local function isSingleplayer()
	return not isClient() and not isServer()
end

-- Rasse eines Tiers aus der Liste, die auch das Debug-Menue liest: DebugContextMenu.lua:250-280
local function findBreed(typ)
	local defs = getAllAnimalsDefinitions()
	for i = 0, defs:size() - 1 do
		local def = defs:get(i)
		if def:getAnimalType() == typ then
			local breeds = def:getBreeds()
			if breeds:size() > 0 then
				return breeds:get(0)
			end
		end
	end
	return nil
end

-- Wasser: dort bleibt ein Tier uninitialisiert (tier_spez.md 4.1). Form: ISWorldObjectContextMenu.lua:683-689
local function isWater(square)
	local floor = square:getFloor()
	return floor ~= nil and floor:hasProperty(IsoFlagType.water)
end

local function spawnLive(square, typ)
	if not square then return nil end
	if not isSingleplayer() then
		print("[NCBear] singleplayer only, in multiplayer use the debug menu: Animals, Bear (NC test)")
		return nil
	end
	if isWater(square) then
		print("[NCBear] not on water")
		return nil
	end
	local breed = findBreed(typ)
	if not breed then
		print("[NCBear] animal definition not loaded: " .. typ .. " (NCBearDefs.lua)")
		return nil
	end
	-- Einzelspieler-Zweig von DebugContextMenu.AddAnimal, DebugContextMenu.lua:1462-1471
	local animal = addAnimal(getCell(), square:getX(), square:getY(), square:getZ(), typ, breed, false)
	if not animal then
		print("[NCBear] addAnimal gave nothing for " .. typ)
		return nil
	end
	animal:addToWorld()
	print("[NCBear] living " .. typ .. " at " .. square:getX() .. "," .. square:getY() .. "," .. square:getZ())
	return animal
end

local function removeLive(square)
	if not square then return end
	local cx, cy, cz = square:getX(), square:getY(), square:getZ() -- DebugContextMenu.lua:640
	-- Liste und Entfernen wie DebugContextMenu.OnRemoveAllAnimals, DebugContextMenu.lua:615-623 (rueckwaerts)
	local list = getCell():getObjectListForLua()
	local n = 0
	for i = list:size(), 1, -1 do
		local animal = list:get(i - 1)
		if instanceof(animal, "IsoAnimal") and ARTEN[animal:getAnimalType()] then -- ISAnimalUI.lua:65
			local sq = animal:getSquare() -- ISAnimalContextMenu.lua:90
			if sq and sq:getZ() == cz and math.abs(sq:getX() - cx) <= RADIUS and math.abs(sq:getY() - cy) <= RADIUS then
				animal:remove()
				n = n + 1
			end
		end
	end
	-- Nur lebende und geladene Baeren in RADIUS: Leichen und weggelaufene bleiben. Ein gespeicherter Baer oder eine
	-- Baerenleiche ohne diese Mod wirft beim Laden bzw. Zeichnen (pruefung_lebend.md Fund 1), also Wegwerf-Spielstand.
	print("[NCBear] removed " .. n .. " living bear(s) within " .. RADIUS .. " tiles; corpses and bears further away stay")
end

local function onSpawnBear(square)
	spawnLive(square, "bear")
end

local function onSpawnStag(square)
	spawnLive(square, "bearstag")
end

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}
table.insert(NCBearMenu.extra, function(sub, square, player)
	-- addOption(Text, Ziel, Funktion): AdminContextMenu.lua:46
	sub:addOption("Spawn living bear here", square, onSpawnBear)
	-- "Spawn living bear (deer motion)" ist seit 07.11. aus dem Menue (Kevin: sieht schlechter aus). Die Art bearstag
	-- bleibt definiert, sonst wirft ein Spielstand, in dem schon einer steht; Konsole NCBear_SpawnLive("bearstag") geht weiter.
	local _ = onSpawnStag
	sub:addOption("Remove living bears nearby", square, removeLive)
end)

-- Konsole: NCBear_SpawnLive() stellt einen lebenden Baeren zwei Kacheln neben die eigene Figur,
-- NCBear_SpawnLive("bearstag") den Rueckfall mit Reh-Bewegung.
function NCBear_SpawnLive(typ)
	typ = typ or "bear"
	if not ARTEN[typ] then
		print("[NCBear] unknown type " .. tostring(typ) .. ", use bear or bearstag")
		return nil
	end
	local playerObj = getSpecificPlayer(0) -- DebugContextMenu.lua:24
	if not playerObj then
		print("[NCBear] no player yet")
		return nil
	end
	local here = playerObj:getCurrentSquare() -- DebugContextMenu.lua:348
	if not here then
		print("[NCBear] player has no square")
		return nil
	end
	local target = getCell():getGridSquare(here:getX() + 2, here:getY(), here:getZ()) or here -- DebugContextMenu.lua:1436
	return spawnLive(target, typ)
end
