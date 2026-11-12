-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert). Lauf baer-f2, PLAN_F2.md 1.1: frueher client/NCBearAttackProbe.lua (heute ein
-- Stummel). Geaendert nur die Arten (ncbear, ncbeargrown, ncbearcub statt bear, bearstag) und dieser Kopf. Seit F2 lockt der Kern selbst
-- Zombies zum GEZAEHMTEN Baeren (shared/BanditsNPCBearFoe.lua B.FoeLureTick, Weg 2 nachgebaut); diese Sonde misst weiter nur Weg 1 (ENT
-- "Probe im Spiel") -- am eigenen Baeren laufen dann beide Anstoesse gleichzeitig (Messung verfaelscht). Fuer F2 lieber NCBear_FightProbe()
-- (client/NCBearBenchFight.lua). Die pcall-Huellen sind die der gespielten alten Sonde (nur Testhilfe, keine Spielmechanik).
-- Alter Kopf:
-- NC Bear Test: Sonde "Koennen Zombies den Baeren angreifen?" (Weg 1). Kein Teil von NPC Crew, nicht fuer den Workshop.
-- Laeuft NUR auf Zuruf in der Lua-Konsole (Spiel mit -debug), NUR im Einzelspieler, hoechstens 15 s, dann meldet sie
-- sich selbst ab. Bericht: NPCCrew/_docs/modelle/baer/begleiter/angriff_fazit.md (Belege: angriff_zombie.md).
--
--   NCBear_AttackProbe()      sucht den naechsten lebenden Baeren (Art bear oder bearstag, bis 30 Kacheln um den Spieler)
--                             und den naechsten Zombie bis 15 Kacheln um den Baeren, druckt Klassen und Werte, hetzt den
--                             Zombie auf den Baeren (Weg 1) und druckt 15 s lang alle 0,5 s: Zustand, Ziel, Abstand,
--                             bAttack/isFacingTarget (die zwei Bedingungen von actiongroups/zombie/idle/to_attack.xml),
--                             Leben des Baeren. Am Ende eine Zusammenfassung mit Lesart.
--   NCBear_AttackProbeStop()  bricht ab und nimmt dem Zombie das Ziel, wenn es noch der Baer ist.
--
-- Weg 1 = Bandits' Form fuer seine Banditen (BanditUpdate.lua:1812-1813 und :1832-1835): zombie:spotted(baer, true) +
-- zombie:setTarget(baer), aus mehr als 3 Kacheln zombie:CanSee(baer) -> zombie:pathToCharacter(baer); alle 0,5 s erneut,
-- weil ein Ziel ohne neues spotted nach 'memory' verfaellt (IsoZombie.updateInternal Offset 1496-1518) und die Engine es
-- im Biss loescht. Diese vier Aufrufe sind Lua-belegt nur mit einem IsoZombie-Banditen als Argument (Java-Parameter
-- IsoMovingObject/IsoGameCharacter, ein IsoAnimal passt), deshalb je im eigenen pcall: ein Fehler wird einmal gedruckt und
-- der Teil fuer den Lauf abgeschaltet.
--
-- Erwartung laut Code: er laeuft hin, geht in den Zustand "attack" und spielt den Vanilla-Biss; im Treffer-Bild loescht die
-- Engine das Ziel (AttackState.triggerPlayerReaction Offset 20-33: Ziel instanceof IsoAnimal -> target = null, return --
-- VOR setAttackedBy und AddRandomDamageFromZombie), das Leben bleibt gleich.
--
-- Was sie veraendert: nur das Ziel EINES Zombies (und sein spottedLast). Hatte er kurz vorher den Spieler gesehen, kann er
-- nach dem Ende noch einige Sekunden den Baeren nachfassen (bonusSpotTime, IsoZombie.updateInternal Offset 957-991), danach
-- verfaellt das Ziel. Kein Schaden von uns, kein ModData, keine Datei, nichts Gespeichertes.
-- Testaufbau: Spieler weiter vom Zombie weg als der Baer (sonst behaelt er den naeheren Spieler, IsoZombie.spottedNew
-- Offset 1042-1113), keine Bandits-NPCs in 20 Kacheln (Bandits zieht Zombies zu ihnen, BanditUpdate.lua:1769-1835),
-- Spiel nicht pausieren.

local BEAR_RADIUS = 30     -- Baer um den Spieler
local Z_RADIUS = 15        -- Zombie um den Baeren
local RUN_MS = 15000
local STEP_MS = 500
local ARTEN = { ncbear = true, ncbeargrown = true, ncbearcub = true } -- F2: Test-Art und die zwei Koerper des eigenen Baeren

local P = nil              -- laufender Lauf, nil = aus
local tickFn = nil

-- Vanillas eigener Test: ISEatFoodAction.lua:136 (wie NCBearSpawn.lua)
local function isSingleplayer()
	return not isClient() and not isServer()
end

local function say(s)
	print("[NCBear-ATK] " .. s)
end

-- Ein Aufruf im eigenen pcall; beim ersten Fehler eine Zeile, danach ist der Teil fuer diesen Lauf aus.
local function try(key, fn)
	if not P then return nil end
	if P.off[key] then return nil end
	local ok, res = pcall(fn)
	if not ok then
		P.off[key] = true
		say("*** " .. key .. " warf: " .. tostring(res) .. " -- fuer diesen Lauf aus")
		return nil
	end
	return res
end

local function dist(a, b)
	local dx, dy = a:getX() - b:getX(), a:getY() - b:getY()
	return math.sqrt(dx * dx + dy * dy)
end

local function f3(v)
	if type(v) ~= "number" then return tostring(v) end
	return string.format("%.3f", v)
end

-- Naechster lebender Baer um den Spieler. Liste wie DebugContextMenu.lua:601/615-623, Art ISAnimalUI.lua:65.
local function findBear(playerObj)
	local list = getCell():getObjectListForLua()
	local best, bestD = nil, nil
	for i = 0, list:size() - 1 do
		local o = list:get(i)
		if instanceof(o, "IsoAnimal") and ARTEN[o:getAnimalType()] and not o:isDead() then
			local d = dist(o, playerObj)
			if math.abs(o:getZ() - playerObj:getZ()) < 0.5 and d <= BEAR_RADIUS and (not bestD or d < bestD) then
				best, bestD = o, d
			end
		end
	end
	return best
end

-- Naechster lebender Zombie um den Baeren, gleiche Ebene. getZombieList: Bandits BanditZombie.lua:110.
local function findZombie(bear)
	local list = getCell():getZombieList()
	local best, bestD = nil, nil
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		if z and not z:isDead() and math.abs(z:getZ() - bear:getZ()) < 0.5 then
			local d = dist(z, bear)
			if d <= Z_RADIUS and (not bestD or d < bestD) then
				best, bestD = z, d
			end
		end
	end
	return best
end

local function bearHealth()
	return try("bear:getHealth", function() return P.bear:getHealth() end) -- ISAnimalUI.lua:15
end

local function targetName(t)
	if t == nil then return "keins" end
	if t == P.bear then return "BAER" end
	if t == P.player then return "Spieler" end
	if instanceof(t, "IsoZombie") then return "Zombie/Bandit" end
	return "anderes"
end

local function stateOf(z)
	-- getActionStateName: Bandits BanditUpdate.lua:414; getCurrentState an einem Zombie: Tutorial/Steps.lua:925
	local asn = try("z:getActionStateName", function() return z:getActionStateName() end) or "?"
	local cs = try("z:getCurrentState", function() return tostring(z:getCurrentState()) end) or "?"
	cs = string.gsub(cs, "^zombie%.ai%.states%.", "")
	cs = string.gsub(cs, "@.*$", "")
	return asn, cs
end

-- Die zwei Bedingungen des Uebergangs nach "attack" (to_attack.xml); getVariableBoolean: ISFitnessUI.lua:245.
local function attackVars(z)
	local a = try("z:getVariableBoolean bAttack", function() return z:getVariableBoolean("bAttack") end)
	local f = try("z:getVariableBoolean isFacingTarget", function() return z:getVariableBoolean("isFacingTarget") end)
	return tostring(a), tostring(f)
end

-- Weg 1 (Bandits' Form). Kein Schaden.
local function lure()
	local z, bear = P.z, P.bear
	try("z:spotted(baer,true)", function() z:spotted(bear, true) end)
	try("z:setTarget(baer)", function() z:setTarget(bear) end)
	if dist(z, bear) > 3 then
		try("z:pathToCharacter(baer)", function()
			if z:CanSee(bear) then z:pathToCharacter(bear) end
		end)
	end
	P.lures = P.lures + 1
end

local function printStart()
	local bear, z, pl = P.bear, P.z, P.player
	say(string.format("Baer: Art %s, instanceof IsoAnimal=%s IsoPlayer=%s IsoZombie=%s, Leben %s, unsterblich=%s, liegt=%s",
		tostring(try("bear:getAnimalType", function() return bear:getAnimalType() end)),
		tostring(instanceof(bear, "IsoAnimal")), tostring(instanceof(bear, "IsoPlayer")), tostring(instanceof(bear, "IsoZombie")),
		f3(P.h0),
		tostring(try("bear:isInvincible", function() return bear:isInvincible() end)), -- ISAnimalContextMenu.lua:565
		tostring(try("bear:isOnFloor", function() return bear:isOnFloor() end))))      -- BanditUtils.lua:362
	local asn, cs = stateOf(z)
	local a, f = attackVars(z)
	say(string.format("Zombie: instanceof IsoZombie=%s, Zustand %s / %s, Ziel %s, useless=%s, kriecht=%s, bAttack=%s, isFacingTarget=%s",
		tostring(instanceof(z, "IsoZombie")), asn, cs,
		targetName(try("z:getTarget", function() return z:getTarget() end)), -- Bandits BanditMenu.lua:170
		tostring(try("z:isUseless", function() return z:isUseless() end)),   -- Bandits BanditMenu.lua:152
		tostring(try("z:isCrawling", function() return z:isCrawling() end)), -- DebugContextMenu.lua:503
		a, f))
	local dzb, dzp = dist(z, bear), dist(z, pl)
	say(string.format("Abstaende: Zombie-Baer %.2f, Zombie-Spieler %.2f, Spieler-Baer %.2f", dzb, dzp, dist(pl, bear)))
	if dzp <= dzb then
		say("ACHTUNG: der Spieler steht naeher am Zombie als der Baer -- er nimmt dann eher den Spieler (spottedNew 1042-1113)")
	end
end

local function finish(why)
	if not P then return end
	local run = P
	-- Ziel freigeben, nur wenn es noch der Baer ist (getTarget: Bandits BanditMenu.lua:170; setTarget(nil): BanditUpdate.lua:421)
	pcall(function()
		if run.z:getTarget() == run.bear then run.z:setTarget(nil) end
	end)
	local h1 = nil
	pcall(function() h1 = run.bear:getHealth() end)
	Events.OnTick.Remove(tickFn) -- ISFastTeleportMove.lua:24
	P = nil
	say("=== Ende (" .. why .. ") nach " .. string.format("%.1f", (getTimestampMs() - run.t0) / 1000) .. " s")
	say("Baer: Leben " .. f3(run.h0) .. " -> " .. f3(h1) .. ", niedrigster Wert " .. f3(run.hMin))
	say(string.format("Zombie: naechster Abstand %.2f, Zustaende [%s], Weg-1-Anstoesse %d", run.minD,
		table.concat(run.states, " "), run.lures))
	say(string.format("Biss-Momente (Zustand attack, Ziel Baer verschwindet im selben Bild): %d, davon mit Lebensverlust %d",
		run.bites, run.bitesHurt))
	say("Lesart: 'attack' in den Zustaenden = er hat zum Biss angesetzt. Biss-Momente > 0 ohne Lebensverlust = genau die")
	say("Code-Stelle AttackState.triggerPlayerReaction 20-33 (Tier -> Ziel null, kein Schaden). Kein 'attack' und naechster")
	say("Abstand > 0,72 = er kam nicht nah genug (IsoZombie.getShouldAttack). Eine '***'-Zeile = ein Aufruf warf, siehe dort.")
	if run.hMin and run.h0 and run.hMin < run.h0 then
		say("!!! Der Baer hat Leben verloren -- das widerspricht dem Code-Befund, bitte die Konsole an Claude geben")
	end
end

local function step()
	local z, bear = P.z, P.bear
	local asn, cs = stateOf(z)
	local a, f = attackVars(z)
	local h = bearHealth()
	local d = dist(z, bear)
	local tgt = try("z:getTarget", function() return z:getTarget() end)
	local dh = ""
	if h and P.hLast and h < P.hLast then dh = string.format(" (-%.3f)", P.hLast - h) end
	P.hLast = h or P.hLast
	say(string.format("t=%.1f s | Zustand %s / %s | Ziel %s | Abstand %.2f | bAttack=%s facing=%s | Baer-Leben %s%s",
		(getTimestampMs() - P.t0) / 1000, asn, cs, targetName(tgt), d, a, f, f3(h), dh))
	lure()
end

tickFn = function()
	if not P then return end
	local now = getTimestampMs()
	if now - P.t0 > RUN_MS then
		finish("15 s um")
		return
	end
	local z, bear = P.z, P.bear
	local alive = false
	pcall(function() alive = not bear:isDead() and not z:isDead() end)
	if not alive then
		finish("Baer oder Zombie tot bzw. weg")
		return
	end
	-- Jedes Bild: Abstand, Zustandsfolge, Biss-Moment (Ziel Baer -> weg, waehrend Zustand attack).
	local d = dist(z, bear)
	if d < P.minD then P.minD = d end
	local asn = try("z:getActionStateName", function() return z:getActionStateName() end) or "?"
	if asn ~= P.lastAsn then
		P.lastAsn = asn
		if #P.states < 16 then P.states[#P.states + 1] = asn end
	end
	local tgt = try("z:getTarget", function() return z:getTarget() end)
	local onBear = (tgt == bear)
	local h = bearHealth()
	if h and (not P.hMin or h < P.hMin) then P.hMin = h end
	if P.wasOnBear and not onBear and asn == "attack" then
		P.bites = P.bites + 1
		P.biteAt = now
		P.biteH = h
		say(string.format("Biss-Moment: Zustand attack, Ziel Baer geloescht, Abstand %.2f, Baer-Leben %s", d, f3(h)))
	end
	-- eine halbe Sekunde nach dem Biss-Moment nachsehen, ob Leben fehlt
	if P.biteAt and now - P.biteAt >= STEP_MS then
		if h and P.biteH and h < P.biteH then P.bitesHurt = P.bitesHurt + 1 end
		P.biteAt = nil
	end
	P.wasOnBear = onBear
	if now - P.lastStep >= STEP_MS then
		P.lastStep = now
		step()
	end
end

function NCBear_AttackProbeStop()
	if not P then
		say("laeuft nicht")
		return
	end
	finish("abgebrochen")
end

function NCBear_AttackProbe()
	if not isSingleplayer() then
		say("nur Einzelspieler: im Mehrspieler rechnet der Rechner mit Hoheit den Zombie und der Server das Tier")
		return
	end
	if P then finish("neu gestartet") end
	local playerObj = getSpecificPlayer(0) -- DebugContextMenu.lua:900
	if not playerObj then say("kein Spieler") return end
	local bear = findBear(playerObj)
	if not bear then
		say("kein lebender Baer in " .. BEAR_RADIUS .. " Kacheln (NCBear_SpawnLive() stellt einen Test-Baeren hin)")
		return
	end
	local z = findZombie(bear)
	if not z then
		say("kein lebender Zombie in " .. Z_RADIUS .. " Kacheln um den Baeren auf derselben Ebene")
		return
	end
	local now = getTimestampMs()
	P = {
		bear = bear, z = z, player = playerObj, t0 = now, lastStep = now, off = {},
		states = {}, lures = 0, bites = 0, bitesHurt = 0, minD = dist(z, bear),
	}
	P.h0 = bearHealth()
	P.hMin, P.hLast = P.h0, P.h0
	say("=== Start Weg 1, 15 s, eine Zeile je 0,5 s. Abbruch: NCBear_AttackProbeStop()")
	printStart()
	lure()
	P.wasOnBear = (try("z:getTarget", function() return z:getTarget() end) == bear)
	say("Weg 1 angestossen: Ziel jetzt " .. targetName(try("z:getTarget", function() return z:getTarget() end)))
	Events.OnTick.Add(tickFn) -- DebugContextMenu.lua:1491
end
