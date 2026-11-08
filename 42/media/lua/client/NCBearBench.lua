-- NC Bear Test: REINE TESTHILFEN fuer den Baeren (Konsole, Spiel mit -debug). Wird NIE nach NPC Crew kopiert (Kevin 08.11.,
-- Copy-Paste-Regel: Testbefehle nur in Bench-Dateien). Kein Teil von NPC Crew, nicht fuer den Workshop.
-- Bauplan: NPCCrew/_docs/modelle/baer/spiel/anim_spez.md 6.6. Bericht: anim_lua.md.
--
-- Nur Einzelspieler (Vanillas Test ISEatFoodAction.lua:136); im Mehrspieler sagt jeder Befehl "singleplayer only".
-- Baer = der naechste gemerkte Baer (Art "bear") in 12 Kacheln um die eigene Figur. Baeren werden alle 5 s gesucht: einen
-- frisch gespawnten Baeren erst nach ein paar Sekunden ansprechen.
-- NCBearAct schreibt diese Datei NICHT: alles geht ueber die Schnittstelle in NCBearFight.lua (F.Calm, F.forceNext).
-- Nichts hier laeuft je Bild.
--
--   NCBear_Sit(sek)          hinsetzen, sek Sekunden sitzen (Vorgabe 60), dann aufstehen
--   NCBear_Stand()           aufstehen (aus Sitzen) bzw. aufhoeren (Fressen, Testclip)
--   NCBear_Eat(sek)          fressen (Vorgabe 30 s)
--   NCBear_Huff()            leises Alltags-Schnauben einmal abspielen
--   NCBear_NextAttack(name)  der naechste Angriff ist name (swipeL, swipeR, bite, maul, slam, rear), einmal
--   NCBear_AnimTest(name)    einen Clip einmal abspielen ohne Kampf (Namen: NCBear_AnimTest() listet sie)
--   NCBear_ZHealth(h, r)     allen Zielen (nur Zombies und feindliche Banditen) in r Kacheln das Leben h geben (Deckel 50)
--   NCBear_KnockInfo()       Knockback-Zaehler und die letzten Flug-Messungen

local NEAR = 12            -- Baer um die eigene Figur
local ZH_MAX = 50          -- NCBear_ZHealth: hoechstens so viele Zombies

-- Vanillas eigener Test: ISEatFoodAction.lua:136
local function isSP()
	return not isClient() and not isServer()
end

local function say(s)
	print("[NCBear] " .. s)
end

local function fight()
	if not isSP() then
		say("singleplayer only")
		return nil
	end
	if not NCBearFight or not NCBearFight.Calm then
		say("*** NCBearFight.lua not loaded")
		return nil
	end
	return NCBearFight
end

local function player()
	local p = getSpecificPlayer(0)                                                   -- DebugContextMenu.lua:921
	if not p then say("no player yet") end
	return p
end

-- Naechster gemerkter Baer um die eigene Figur
local function bear()
	local F = fight()
	if not F then return nil, nil end
	local p = player()
	if not p then return nil, nil end
	local B = F.NearestBear(p:getX(), p:getY(), NEAR)
	if not B then
		say("no bear within " .. NEAR .. " tiles (bears are picked up every 5 s; fight must be ON: NCBear_Fight())")
		return nil, nil
	end
	return F, B
end

local function report(ok, why)
	say((ok and "bear " or "bear refuses: ") .. tostring(why))
end

function NCBear_Sit(sek)
	local F, B = bear()
	if not B then return end
	report(F.Calm.Sit(B, sek))
end

function NCBear_Stand()
	local F, B = bear()
	if not B then return end
	report(F.Calm.Stand(B))
end

function NCBear_Eat(sek)
	local F, B = bear()
	if not B then return end
	report(F.Calm.Eat(B, sek))
end

function NCBear_Huff()
	local _, B = bear()
	if not B then return end
	B.a:playBreedSound("huffsoft")                                                   -- ISHutchGrabAnimal.lua:31
	say("huff (soft)")
end

function NCBear_NextAttack(name)
	local F = fight()
	if not F then return end
	if name == nil or not F.ATTACKS[name] then
		say("use NCBear_NextAttack(name) with swipeL, swipeR, bite, maul, slam or rear")
		return
	end
	F.forceNext = name
	say("next attack: " .. name .. " (once, for the next bear that attacks)")
end

function NCBear_AnimTest(name)
	local F = fight()
	if not F then return end
	if name == nil or not F.ACTS[name] then
		local keys = {}
		for k in pairs(F.ACTS) do keys[#keys + 1] = k end
		table.sort(keys)
		say("use NCBear_AnimTest(name), names: " .. table.concat(keys, ", "))
		return
	end
	local _, B = bear()
	if not B then return end
	report(F.Calm.Play(B, name))
end

-- Leben setzen: z:setHealth(h) wie Bandits BanditClientCommands.lua:36. Nur Ziele nach der harten Regel (F.IsTarget):
-- Zombies und feindliche Banditen, nie Spieler, Crew, Neutrale, Tiere.
function NCBear_ZHealth(h, r)
	local F = fight()
	if not F then return end
	h = tonumber(h)
	r = tonumber(r) or 10
	if not h or h <= 0 or h > 20 then
		say("use NCBear_ZHealth(h, r): h 0.1..20 (normal zombie 1.8-2.1, tough 3.5-3.8), r tiles (default 10)")
		return
	end
	if r < 1 then r = 1 end
	if r > 40 then r = 40 end
	local p = player()
	if not p then return end
	local px, py = p:getX(), p:getY()
	local list = getCell():getZombieList()                                         -- Bandits BanditZombie.lua:110
	local n, skipped = 0, 0
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		local dx, dy = z:getX() - px, z:getY() - py
		if dx * dx + dy * dy <= r * r then
			if n >= ZH_MAX then
				skipped = skipped + 1
			elseif F.IsTarget(z) then
				z:setHealth(h)                                                       -- Bandits BanditClientCommands.lua:36
				n = n + 1
			end
		end
	end
	say("health " .. h .. " set on " .. n .. " target(s) within " .. r .. " tiles" .. (skipped > 0 and (", " .. skipped .. " more skipped (cap " .. ZH_MAX .. ")") or ""))
end

function NCBear_KnockInfo()
	local F = fight()
	if not F then return end
	local K = F.knockStats
	say("knock: back " .. K.back .. " (killing blows " .. K.killFly .. "), down " .. K.down
		.. " (bear at his side " .. (K.side or 0) .. "), back vetoed " .. K.vetoed .. " (side, behind him, check behind), pushed " .. K.pushed
		.. " | knockBack " .. tostring(F.T.knockBack) .. ", knockKill " .. tostring(F.T.knockKill) .. ", knockPush " .. tostring(F.T.knockPush))
	if #F.knockLog == 0 then
		say("  no flight measured yet (a line comes 2.3 s after each knock)")
	end
	for _, line in ipairs(F.knockLog) do
		say("  " .. line)
	end
	if #F.knockWatch > 0 then say("  " .. #F.knockWatch .. " flight(s) still being measured") end
end
