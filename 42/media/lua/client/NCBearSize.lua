-- NC Bear: Groesse der lebenden Baeren in der Naehe nachstellen. Konsole: NCBear_Size(1.5)
-- Kevin 08.11.: "der baer ist eher noch ein baby braunbaer ein echter waere viel groesser".
-- setSizeForced: Vanilla ButcheringUtil.lua:569 (animal:getData():setSizeForced(x)); gilt, bis der Baer einen Spieltag
-- aelter wird, dann setzt das Spiel die Groesse aus der Definition wieder (bau_lebend.md). Nur zum Ausprobieren.
-- Liste und Abfragen wie NCBearSpawn.lua (getObjectListForLua, instanceof IsoAnimal, getAnimalType, getSquare).
local RADIUS = 20

function NCBear_Size(x)
	x = tonumber(x)
	if not x or x <= 0 then
		print("[NCBear] use NCBear_Size(1.5)")
		return
	end
	local playerObj = getSpecificPlayer(0)
	if not playerObj then return end
	local here = playerObj:getCurrentSquare()
	if not here then return end
	local list = getCell():getObjectListForLua()
	local n = 0
	for i = list:size(), 1, -1 do
		local animal = list:get(i - 1)
		if instanceof(animal, "IsoAnimal") then
			local typ = animal:getAnimalType()
			if typ == "bear" or typ == "bearstag" then
				local sq = animal:getSquare()
				if sq and math.abs(sq:getX() - here:getX()) <= RADIUS and math.abs(sq:getY() - here:getY()) <= RADIUS then
					animal:getData():setSizeForced(x)
					n = n + 1
				end
			end
		end
	end
	print("[NCBear] size " .. x .. " set on " .. n .. " bear(s) within " .. RADIUS .. " tiles (until the bear is a day older)")
end
