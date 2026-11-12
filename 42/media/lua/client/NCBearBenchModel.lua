--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert). Lauf baer-f2, PLAN_F2.md 1.1: frueher client/NCBearTest.lua (heute ein Stummel),
-- Inhalt unveraendert bis auf diesen Kopf. Nur Einzelspieler; nichts hier laeuft je Bild.
-- Stellt das stehende Baeren-Modell als Bodengegenstand in die Welt (Gegenstand NCBear.BearStatic, scripts/nc_bear.txt = Werkbank-Asset)
-- und ist der WIRT des Rechtsklick-Untermenues "NC Bear": jede Bench-Datei haengt dort Eintraege an (Tabelle NCBearMenu.extra, je eine
-- Funktion(Untermenue, Kachel, Spielernummer); client/NCBearBenchAdult.lua, ...Cub.lua, ...Fight.lua). client/ laedt alphabetisch,
-- deshalb legt jede Datei die Tabelle mit "or {}" an; gelesen wird sie erst beim Rechtsklick.
-- Konsole: NCBear_Spawn() stellt ein Modell zwei Kacheln neben die eigene Figur.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben; Zeilen der alten gespielten Datei, Lauf baer-kampf).
-- Statisch geprueft, nicht gespielt.
--

local ITEM = "NCBear.BearStatic"
local RADIUS = 8

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}

-- Vanillas eigener Test: ISEatFoodAction.lua:136
local function isSingleplayer()
	return not isClient() and not isServer()
end

local function spawnBear(square)
	if not square then return nil end
	-- instanceItem(typ): FenrisScenario.lua:8. Ohne geladenes Skript kommt nil, und nil trifft in AddWorldInventoryItem
	-- keine eindeutige Fassung (es gibt sie fuer String, ItemKey und InventoryItem): lieber eine klare Zeile.
	local fresh = instanceItem(ITEM)
	if not fresh then
		print("[NCBear] spawn failed: item script not loaded: " .. ITEM)
		return nil
	end
	-- square:AddWorldInventoryItem(instanceItem(typ), x, y, z): FenrisScenario.lua:8; Kachelmitte, auf dem Boden
	local item = square:AddWorldInventoryItem(fresh, 0.5, 0.5, 0)
	if not item then
		print("[NCBear] spawn failed: no item came back for " .. ITEM)
		return nil
	end
	-- item:setWorldZRotation(zahl): FenrisScenario.lua:39, ISDropWorldItemAction.lua:83
	item:setWorldZRotation(0)
	-- Nicht vom Sandbox-Aufraeumer weggeraeumt: ISDropWorldItemAction.lua:84-85
	if item:getWorldItem() then
		item:getWorldItem():setIgnoreRemoveSandbox(true)
	end
	print("[NCBear] spawned at " .. square:getX() .. "," .. square:getY() .. "," .. square:getZ())
	return item
end

-- Alle Baeren-Modelle um eine Kachel: erst sammeln, dann handeln. Rueckgabe je Eintrag: Weltobjekt und Abstand^2.
local function findBears(square)
	local found = {}
	local cx, cy, cz = square:getX(), square:getY(), square:getZ() -- DebugContextMenu.lua:640
	for dy = -RADIUS, RADIUS do
		for dx = -RADIUS, RADIUS do
			local sq = getCell():getGridSquare(cx + dx, cy + dy, cz) -- DebugContextMenu.lua:1432
			if sq then
				local objs = sq:getWorldObjects() -- ISWorldObjectContextMenu.lua:2978
				for i = 0, objs:size() - 1 do
					local obj = objs:get(i)
					local item = obj:getItem() -- ISWorldObjectContextMenu.lua:2980
					if item and item:getFullType() == ITEM then -- ISInventoryPaneContextMenu.lua:4290
						table.insert(found, { obj = obj, dist = dx * dx + dy * dy })
					end
				end
			end
		end
	end
	return found
end

local function onSpawn(square)
	spawnBear(square)
end

local function onTurn(square)
	local found = findBears(square)
	local best = nil
	for _, e in ipairs(found) do
		if not best or e.dist < best.dist then best = e end
	end
	if not best then
		print("[NCBear] no bear model within " .. RADIUS .. " tiles")
		return
	end
	local item = best.obj:getItem()
	-- Lesen: ISExtendedPlacementUI.lua:160; Schreiben: ISExtendedPlacementUI.lua:186; "% 360": ISKnob.lua:139
	item:setWorldZRotation((item:getWorldZRotation() + 45) % 360)
	print("[NCBear] turned to " .. item:getWorldZRotation())
end

local function onRemove(square)
	local found = findBears(square)
	for _, e in ipairs(found) do
		-- Einzelspieler-Form aus ISGrabItemAction.lua:129-134
		local obj = e.obj
		local item = obj:getItem()
		obj:getSquare():transmitRemoveItemFromSquare(obj)
		obj:removeFromWorld()
		obj:removeFromSquare()
		obj:setSquare(nil)
		item:setWorldItem(nil)
	end
	print("[NCBear] removed " .. #found .. " bear model(s)")
end

local function onFillWorldObjectContextMenu(player, context, worldobjects, test)
	-- Dieselbe Tuer wie Vanillas Menues: DebugContextMenu.lua:34-40
	if test and ISWorldObjectContextMenu.Test then return true end
	local square = nil
	for _, v in ipairs(worldobjects) do
		square = v:getSquare()
		break
	end
	if not square then return end
	-- Probelauf fuer Controller: nur melden, dass es Eintraege gibt, nichts bauen.
	-- Regel: ISWorldObjectContextMenu.lua:122-128, Form: DebugContextMenu.lua:350
	if test then return ISWorldObjectContextMenu.setTest() end

	if not isSingleplayer() then
		-- Grau mit Hinweis: ISWorldObjectContextMenu.lua:271-275
		local opt = context:addOption("NC Bear", worldobjects, nil)
		opt.notAvailable = true
		local toolTip = ISWorldObjectContextMenu.addToolTip()
		toolTip.description = "singleplayer only. Living bear in multiplayer: debug menu, Animals, Bear (NC test)."
		opt.toolTip = toolTip
		return
	end

	-- Untermenue: ISWorldObjectContextMenu.lua:585, DebugContextMenu.lua:54-56
	local main = context:addOption("NC Bear", worldobjects, nil)
	local sub = ISContextMenu:getNew(context)
	context:addSubMenu(main, sub)
	-- addOption(Text, Ziel, Funktion): AdminContextMenu.lua:46
	sub:addOption("Spawn bear model here", square, onSpawn)
	sub:addOption("Turn nearest bear model 45 degrees", square, onTurn)
	sub:addOption("Remove bear models nearby", square, onRemove)
	-- Eintraege anderer Dateien, je einer Funktion(Untermenue, Kachel, Spielernummer)
	for _, fn in ipairs(NCBearMenu.extra) do
		fn(sub, square, player)
	end
end

Events.OnFillWorldObjectContextMenu.Add(onFillWorldObjectContextMenu) -- ISHutchMenu.lua:115

-- Konsole: NCBear_Spawn() stellt ein Modell zwei Kacheln neben die eigene Figur.
function NCBear_Spawn()
	if not isSingleplayer() then
		print("[NCBear] singleplayer only")
		return
	end
	local playerObj = getSpecificPlayer(0) -- DebugContextMenu.lua:24
	if not playerObj then
		print("[NCBear] no player yet")
		return
	end
	local here = playerObj:getCurrentSquare() -- DebugContextMenu.lua:344
	if not here then
		print("[NCBear] player has no square")
		return
	end
	local target = getCell():getGridSquare(here:getX() + 2, here:getY(), here:getZ()) or here
	return spawnBear(target)
end
