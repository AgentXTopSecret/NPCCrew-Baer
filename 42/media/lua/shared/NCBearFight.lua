-- NC Bear Test: der Baer kaempft gegen Zombies und FEINDLICHE Banditen. Kein Teil von NPC Crew, nicht fuer den Workshop.
-- Bauplan: NPCCrew/_docs/modelle/baer/spiel/kampf_spez.md (Abschnitte genannt als "Spez x.y"). Bericht: kampf_lua.md.
--
-- NUR EINZELSPIELER (Spez 3.5): im Mehrspieler rechnet der Server die Baer-KI, der Client mit Hoheit den Zombie; Schaden
-- und Bild dort sind nicht belegt. Diese Datei tut im Mehrspieler nichts (kein OnTick, die Konsole sagt es).
--
-- HARTE REGEL (Kevin 08.11.): Ziele sind nur Zombies und feindliche Banditen. Die Liste ist getCell():getZombieList()
-- (Bandits BanditZombie.lua:110): Spieler, Tiere, Fahrzeuge, Kisten stehen nicht darin; F.IsTarget prueft dazu IsoZombie.
-- Banditen nach Bandits' eigener Regel (Bandit.IsHostile, Bandit.lua:600-605), NPC-Crew-Marken davor; im Zweifel kein Ziel.
-- NPC Crew und Bandits sind optional: nur Felder aus ModData, kein Aufruf in ihren Code.
--
-- Ablauf je Baer (Spez 5.2, anim_spez.md 4): Ruhe -> Aufrichten + Bruellen nur zu Kampfbeginn (50 %, alle 120 s, Ziel
-- weiter als 2,5 Kacheln) -> Anrennen -> Angriff nach Gewichten (Hieb L/R, Biss gegen Stehende, Doppelschlag, Biss am Boden;
-- nie zweimal derselbe Clip) -> Pause -> naechster Angriff; Ende -> zurueck zum Kampfbeginn -> Ruhe. Kein Scheinangriff.
-- Getroffene fliegen zurueck (anim_spez.md 2: Engine-Taumeln ueber setPlayerAttackPosition FRONT, Vorpruefung hinter ihm).
-- Ruhe: Sitzen (Hinsetzen, Sitzen-Schleife, Aufstehen) und Fressen (Phase "calm", anim_spez.md 6), Schnauben im Alltag (5).
-- Der Treffermoment kommt aus der Animation (SetVariable NCBearHit=true, Knoten unter AnimSets/buck/idle/NCBear_*.xml).
-- Beim Treffer neu geprueft: Regel, Ebene, Abstand, Kegel, Sicht und Wand (canStrike). Nachbesserung: kampf_fix.md.
-- NCBearAct schreibt NUR diese Datei (anim_spez.md 6.5); Testbefehle stehen in client/NCBearBench.lua und gehen ueber F.Calm.
-- Jeder Engine-Aufruf hat eine Fundstelle (Kommentar daneben). Nichts im render, Deckel auf allem, was waechst.
--
-- NUR TESTSCHNITTSTELLE (anim_review_technik.md Fund 9, Fixer 08.11.): F.forceNext, F.Calm.Play mit dem Unterzustand "play"
-- und PLAY_LOOP, F.knockLog, F._posture/_flyOk/_tickBody dienen nur NCBearBench.lua und der Attrappe. Sie sind KEIN Menue und
-- schreiben NCBearAct nur ueber diese Datei. Beim Uebernehmen nach NPC Crew (baer_uebernahme.py) nimmt das Skript sie heraus
-- (Marke "TESTSCHNITTSTELLE" an jeder Stelle) und legt "log" auf den Crew-Logging-Schalter (BanditsNPC.Log); hier druckt
-- die Flugsonde mit log = 1 (Vorgabe) in jedem Spiel.

NCBearFight = NCBearFight or {}
local F = NCBearFight

-- Clips (anim_spez.md 7). Der Animator baut parallel: Dauer und Treffermoment hier als Konstanten, gleich den Knoten-XML.
-- Weicht seine Messung ab, gilt sie, und F.ACTS und die m_TimePc ziehen nach.
-- hitPc nur fuer "Blick aufs Ziel bis zum Treffer"; den Treffer selbst meldet die Animation. loop = Schleifenknoten (keine
-- Frist auf das Ende, nur auf die Dauer des Befehls).
F.ACTS = {
	rear    = { clip = "NCBear_Rear",    dur = 3.00, hitPc = nil },
	swipeL  = { clip = "NCBear_SwipeL",  dur = 1.50, hitPc = 0.40 },
	swipeR  = { clip = "NCBear_SwipeR",  dur = 1.50, hitPc = 0.40 },
	slam    = { clip = "NCBear_Slam",    dur = 2.40, hitPc = 0.54 },
	bite    = { clip = "NCBear_Bite",    dur = 1.30, hitPc = 0.40 },
	maul    = { clip = "NCBear_Maul",    dur = 1.60, hitPc = 0.34 },
	sitdown = { clip = "NCBear_SitDown", dur = 1.60 },
	sit     = { clip = "NCBear_Sit",     dur = 4.00, loop = true },
	standup = { clip = "NCBear_StandUp", dur = 1.30 },
	eat     = { clip = "NCBear_Eat",     dur = 3.20, loop = true },
}
-- Angriffe, die ChooseAct waehlen bzw. NCBear_NextAttack erzwingen darf
F.ATTACKS = { rear = true, swipeL = true, swipeR = true, slam = true, bite = true, maul = true }
F.FRIST = 1.0              -- Netz (Spez 1.5): Clipdauer + 1 s, danach Angriff verwerfen, Treffer nie nachholen
F.REAR_FACE = 1.0          -- beim Aufrichten so lange dem Ziel zudrehen (Sekunden)

-- Stellschrauben (Konsole NCBear_Tune(feld, wert)). Weiten in Kacheln bei Baerengroesse 1,0 (wachsen mit getSize).
-- Schaden in Lebenspunkten: normaler Zombie 1,8-2,1, zaeh 3,5-3,8 (Spez 5.1); alles mal "dmg".
-- Weiten nach dem Clip (Formeln anim_spez.md 7, Masse aus dem Bau des Fixers baer-anim 08.11., anim_fix.md): im Treffermoment
-- ist die Pranke beim Hieb 0,90 Kacheln vor Bip01 (0,16 zur Schlagseite) -> 0,90 + 0,55 = rund 1,4; die Schnauze beim Biss
-- gegen Stehende 0,97 -> 0,97 + 0,45 = rund 1,4; beim Biss am Boden 0,68 -> 0,68 + 0,42 = rund 1,1; beide Pranken beim
-- Doppelschlag 0,58 -> 0,58 + 0,9 = rund 1,5. Mit 1,8/2,0/1,7 schlug er sichtbar in die Luft (kampf_review_technik.md Fund 1).
-- Ankunft 1,1 (Koerperkreis collisionSize 0,42, NCBearDefs.lua). Kommt er nicht naeher, schlaegt er aus der Hiebweite zu
-- (updateApproach, Steckenbleiben).
-- Schaden nach anim_spez.md 3.2: normaler Zombie (1,8-2,1) 2-3 Treffer, zaeher (3,5-3,8) 3-4. Debug-Spawn hat 1,0 Leben
-- (Schieber "Health", ISSpawnHordeUI.lua:110-111), dort toetet jeder Hieb: Schieber auf 2,0 stellen.
-- Angriffsgewichte (anim_spez.md 4.1): ganze Zahlen, ZombRand(summe); wSide kommt beim Hieb zur Seite des Ziels dazu.
-- Knockback (anim_spez.md 2): knock = umwerfen ueberhaupt; knockBack = Engine-Taumeln nach hinten (Hiebe, Doppelschlag);
-- knockKill = auch der toedliche Treffer taumelt (ungespielt); knockPush = eigenes Zurueckschieben in Kacheln, Rueckfall 2.8,
-- Vorgabe 0 (aus) -- nur einschalten, wenn knock: back im Spiel auf der Stelle faellt.
-- Ruhe: sitChance je 20 s Pruefung (Prozent); huff = Alltags-Schnauben an/aus, Abstand huffMin + ZombRand(huffSpread + 1) s.
F.T = {
	radius = 10, banditRadius = 12, nextRadius = 8,
	arrive = 1.1,
	swipeReach = 1.4, swipeHalf = 55, swipeShift = 15,
	slamReach = 1.5, slamHalf = 80,
	biteReach = 1.4, biteHalf = 30,
	maulReach = 1.1, maulHalf = 30,
	dmg = 1.0, dmgMain = 1.0, dmgSide = 0.6, dmgSlam = 0.9, dmgBite = 1.2, dmgMaul = 1.8,
	sideMax = 3, slamMax = 5, hitCap = 6, knock = 1,
	knockBack = 1, knockKill = 1, knockPush = 0,
	wSwipe = 25, wSide = 15, wBite = 30, wMaul = 70, wSlam = 40,
	roarCD = 120, rearChance = 50, rearDist = 2.5, slamCD = 10, pause = 0.35,
	leash = 25, fightMax = 90, restAfter = 20, noTarget = 3,
	stuckTime = 3, stuckGain = 0.5, blockTime = 20, home = 5,
	sitChance = 10, huff = 1, huffMin = 90, huffSpread = 150,
	noise = 0, log = 1,
}
F.RANGE = {
	radius = { 1, 30 }, banditRadius = { 1, 30 }, nextRadius = { 1, 30 }, arrive = { 0.5, 4 },
	swipeReach = { 0.5, 5 }, swipeHalf = { 5, 90 }, swipeShift = { 0, 45 },
	slamReach = { 0.5, 5 }, slamHalf = { 5, 90 }, biteReach = { 0.5, 4 }, biteHalf = { 5, 90 },
	maulReach = { 0.5, 4 }, maulHalf = { 5, 90 },
	dmg = { 0, 20 }, dmgMain = { 0, 20 }, dmgSide = { 0, 20 }, dmgSlam = { 0, 20 }, dmgBite = { 0, 20 }, dmgMaul = { 0, 20 },
	sideMax = { 0, 10 }, slamMax = { 1, 10 }, hitCap = { 1, 12 }, knock = { 0, 1 },
	knockBack = { 0, 1 }, knockKill = { 0, 1 }, knockPush = { 0, 2 },
	wSwipe = { 0, 100 }, wSide = { 0, 100 }, wBite = { 0, 100 }, wMaul = { 0, 100 }, wSlam = { 0, 100 },
	-- pause ab 0,3: ein noch ausblendender Knoten (m_BlendTime 0,15-0,25) wird von der Engine wieder genommen statt neu
	-- gestartet (AnimLayer.findLiveNode 36-59, getOrCreateLiveNode 6-15); derselbe Angriff zweimal kaeme dann ohne Ereignisse.
	roarCD = { 0, 600 }, rearChance = { 0, 100 }, rearDist = { 0, 10 }, slamCD = { 0, 120 }, pause = { 0.3, 5 },
	leash = { 5, 60 }, fightMax = { 10, 600 }, restAfter = { 0, 300 }, noTarget = { 1, 30 },
	stuckTime = { 1, 10 }, stuckGain = { 0.1, 3 }, blockTime = { 1, 120 }, home = { 2, 30 },
	sitChance = { 0, 100 }, huff = { 0, 1 }, huffMin = { 30, 900 }, huffSpread = { 0, 900 },
	noise = { 0, 60 }, log = { 0, 2 },
}

local MAX_BEARS = 8        -- gemerkt (Spez 5.4)
local MAX_FIGHTING = 4     -- gleichzeitig im Kampf
local MAX_BLOCKED = 32     -- gesperrte Ziele
local SCAN_EVERY = 5.0     -- getObjectListForLua kopiert die ganze Menge (IsoCell.getObjectListForLua 0-14), darum selten
local SEARCH_EVERY = 0.5
local REISSUE = 0.75       -- Anrennen neu, wenn das Ziel weiterzog oder der Weg endete
local DT_MAX = 0.5         -- je Bild hoechstens so viel Kampfuhr (Pause, Ladebild)
local FRIST_STRIKES = 3    -- so viele verfallene Angriffe in Folge: Clips fehlen vermutlich, Kampf aus
local JUMP = 8             -- springt das Ziel zwischen zwei Suchtakten weiter: ein anderes Objekt (Pool), Ziel weg
local SIGHT_MAX = 12       -- Sichtpruefungen je Treffer hoechstens
local STUCK_MAX = 3        -- so viele unerreichbare Ziele je Kampf, dann Kampf aus (Ruhe restAfter)

-- Knockback (anim_spez.md 2.7/2.8): Pruefpunkte hinter dem Zombie alle KNOCK_STEP Kacheln bis KNOCK_LEN (Zombie_StaggerBackFall
-- fliegt rund 1,7 Kacheln); eigene Schiebe-Eintraege hoechstens MAX_PUSH, je Bild hoechstens PUSH_STEP, hoechstens PUSH_TIME s.
local KNOCK_STEP = 0.45
local KNOCK_SAMPLES = 4
local MAX_PUSH = 8
local PUSH_STEP = 0.05
local PUSH_TIME = 0.6
-- Sonde "wie weit flog er": je umgeworfenem Zombie ein Eintrag, nach WATCH_TIME s eine Zeile; hoechstens MAX_WATCH, die
-- letzten MAX_KLOG Ergebnisse fuer NCBear_KnockInfo (Testdatei)
local MAX_WATCH = 8
local WATCH_TIME = 2.3
local WATCH_DEAD = 4.0     -- toedlich: bis die Leiche liegt (Leiche erst am Boden, anim_spez.md 2.9), hoechstens so lange
local MAX_KLOG = 8

-- Ruhe (anim_spez.md 6.2/6.3): Sperre der Engine loest bei 8000 (BaseAnimalBehavior.wanderIdle 0-39), wir erneuern bei 4000
local BLOCK_REFRESH = 4000
local SIT_EVERY = 20       -- von selbst sitzen: Pruefung je Baer alle 20 s
local SIT_MIN, SIT_SPREAD = 45, 105   -- Dauer 45 + ZombRand(106) s
local SIT_QUIET = 3        -- so viele Suchtakte ohne Ziel vorher
local SIT_AFTER_HIT = 20   -- nicht in den 20 s nach einem Treffer
local SIT_AFTER_STAND = 180
local CALM_FAILS = 3       -- verfallene Hinsetz-/Aufsteh-Clips in Folge, dann eine laute Zeile
local EAT_DEFAULT = 30
local SIT_DEFAULT = 60
local PLAY_LOOP = 2        -- TESTSCHNITTSTELLE: NCBear_AnimTest spielt Schleifenclips so oft ab

-- Alltags-Schnauben (anim_spez.md 5)
local HUFF_GAP = 60        -- zwischen zwei Alltags-Schnauben mindestens
local HUFF_SIT_MUL = 3     -- im Sitzen der Abstand mal 3
local HUFF_NEAR, HUFF_FAR = 3, 6   -- Spieler unter 3 Kacheln: einmal; scharf erst wieder ueber 6
local HUFF_NEAR_GAP = 60
local HUFF_AFTER_FIGHT = 20
local HUFF_LOUD_GAP = 18   -- lautes Schnauben beim Anrennen: mit dem Knockback rennt er fast nach jedem Hieb neu an (Pruefer
                           -- Fund 5); vorher 6 s, das waere den ganzen Kampf lang alle 6 s gewesen

local SND_HIT_MAIN = "SledgehammerHit"   -- weapons/sounds_melee_bluntlong.txt:939
local SND_HIT_SIDE = "MacheteHit"        -- weapons/sounds_melee_bladelong.txt:39
local SND_BITE = "ZombieBite"            -- zombies/sounds_zombie_foley.txt:210
local SND_KILL = "HeadSmash"             -- zombies/sounds_zombie_foley.txt:12
local SND_MAX = 2                        -- Treffertoene je Angriff (mehr klingt nach Brei)

F.enabled = (F.enabled ~= false)
F.clock = F.clock or 0
F.bears = F.bears or {}
F.byObj = F.byObj or {}
F.blocked = F.blocked or {}
F.blockedN = F.blockedN or 0
F.nextScan = F.nextScan or 0
F.nextSearch = F.nextSearch or 0
F.stats = F.stats or { fights = 0, acts = 0, hits = 0, kills = 0, expired = 0, fleeStops = 0, calmExpired = 0 }
F.knockStats = F.knockStats or { back = 0, down = 0, vetoed = 0, side = 0, pushed = 0, killFly = 0 }
F.knockWatch = F.knockWatch or {}
F.knockLog = F.knockLog or {}
F.pushes = F.pushes or {}
F.forceNext = nil          -- TESTSCHNITTSTELLE: NCBear_NextAttack (Testdatei) erzwingt den naechsten Angriff, einmal
F.rawMult = 0              -- ungedeckelter getMultiplier dieses Bildes (Sperre der Engine, anim_spez.md 6.2)
F.Calm = F.Calm or {}

-- Vanillas eigener Test: ISEatFoodAction.lua:136
local function isSP()
	return not isClient() and not isServer()
end

local function say(msg)
	if F.T.log >= 1 then print("[NCBear] " .. msg) end
end

local function sayMore(msg)
	if F.T.log >= 2 then print("[NCBear] " .. msg) end
end

local function fmt(x)
	return string.format("%.2f", x)
end

-- Groesse des Baeren (NCBear_Size): animal:getData():getSize(), ISPetAnimal.lua:31
local function sizeOf(a)
	local s = a:getData():getSize()
	if type(s) ~= "number" or s < 0.5 then return 0.5 end
	if s > 3 then return 3 end
	return s
end

-- Winkel des Ziels zur Blickrichtung, positiv = links vom Baeren (Iso: x Ost, y Sued; links von (fx,fy) ist (fy,-fx)).
function F.AngleLeft(fx, fy, dx, dy)
	local dot = fx * dx + fy * dy
	local left = fy * dx - fx * dy
	return math.deg(math.atan2(left, dot))   -- math.atan2: ISBaseIcon.lua:210
end

function F.InCone(fx, fy, dx, dy, lo, hi)
	if dx * dx + dy * dy < 0.0001 then return true end
	local ang = F.AngleLeft(fx, fy, dx, dy)
	return ang >= lo and ang <= hi
end

-- Die harte Regel (Spez 3.4). Rueckgabe: darf getroffen werden, ist ein Bandit. Reihenfolge: NPC-Crew-Marken vor hostileP
-- (NPC Crew setzt hostileP kurz auf Crew und Neutrale, BanditsNPCCompat.lua:171-195).
function F.IsTarget(z)
	if not z or not instanceof(z, "IsoZombie") then return false, false end         -- DebugContextMenu.lua:604
	if z:isOnKillDone() then return false, false end                               -- Bandits ZASmack.lua:357
	if not z:isAlive() or z:getHealth() <= 0 then return false, false end          -- Bandits BanditUpdate.lua:1203
	if z:isReanimatedForGrappleOnly() then return false, false end                 -- Bandits BanditCompatibility.lua:189
	if z:isFakeDead() then return false, false end                                 -- DebugContextMenu.lua:662
	-- im oder unter einem Fahrzeug: nie (Banditen sitzen in Autos, Bandits BanditUpdate.lua:270)
	if z:getVehicle() ~= nil or z:isUnderVehicle() then return false, false end      -- Bandits BanditMenu.lua:162-163
	local md = z:getModData()                                                       -- Bandits BanditBrain.lua:4
	if md.tcUid ~= nil then return false, true end    -- NPC-Crew-Marke am Koerper (Guardian firstCompanionSight): nie
	local brain = md.brain                                                          -- Bandits BanditBrain.lua:5
	local isBandit = z:getVariableBoolean("Bandit")                                 -- Bandits BanditZombie.lua:137
	if not isBandit and brain == nil then return true, false end                    -- gewoehnlicher Zombie
	if type(brain) ~= "table" then return false, true end                           -- Marke ohne Gehirn: im Zweifel nicht
	if brain.recruited or brain.npcNeutral or brain.npcUid ~= nil then return false, true end   -- NPC Crew (Interact.lua:1055, Compat.lua:32-43)
	if brain.programFallback == "NPCNeutral" then return false, true end                        -- NPC Crew (Compat.lua:40)
	local prog = brain.program
	local pname = (type(prog) == "table") and prog.name or nil
	if type(pname) == "string" and string.sub(pname, 1, 3) == "NPC" then return false, true end  -- NPC-Crew-Programme
	if brain.loyal then return false, true end                                      -- Bandits "babe" (BanditUtils.lua:785-786)
	if brain.hostile or brain.hostileP then return true, true end                   -- Bandit.IsHostile (Bandit.lua:600-605)
	return false, true                                                              -- Zivilist, Begleiter, neutral
end

-- Haltung eines Ziels (anim_spez.md 2.2): "down" = liegt (Bandits ZASmack.lua:486: isProne oder onground), "falling" = faellt,
-- fliegt, steht auf (Aktionszustand mit diesem Anfang, Ordner media/actiongroups/zombie/), sonst "up". Dazu der Zustandsname.
-- Ein fallender Zombie wird nicht noch einmal umgeworfen (faceLocationF wuerde ihn mitten im Flug drehen: StaggerBackState
-- dreht den Clip nach seinem Blick) und nicht im Stehen gebissen.
local FALL_PREFIX = { "falldown", "staggerback-knockeddown", "knockeddown", "onground", "getup", "getdown", "falling",
	"hitreaction-onfloor", "vehicleCollision-onground", "fakedead" }
-- nur aus diesen Zustaenden hat to_staggerback-knockeddown (Lage FRONT) Vorrang (anim_spez.md 2.2: idle, walktoward,
-- pathfind, attack, lunge haben dieselben fuenf Uebergaenge)
local FLY_FROM = { idle = true, walktoward = true, pathfind = true, attack = true, lunge = true }

local function posture(z)
	if z:isProne() then return "down", "onground" end                               -- Bandits ZASmack.lua:486
	local st = z:getActionStateName()                                                -- Bandits ZASmack.lua:486
	if st == "onground" then return "down", st end
	for _, pre in ipairs(FALL_PREFIX) do
		if string.sub(st, 1, #pre) == pre then return "falling", st end
	end
	return "up", st
end
F._posture = posture       -- TESTSCHNITTSTELLE: fuer die Attrappe

local function isBlocked(z)
	local t = F.blocked[z]
	return t ~= nil and t > F.clock
end

local function block(z)
	if F.blockedN >= MAX_BLOCKED then
		local keep, n = {}, 0
		for k, t in pairs(F.blocked) do
			if t > F.clock then keep[k] = t; n = n + 1 end
		end
		F.blocked, F.blockedN = keep, n
		if n >= MAX_BLOCKED then F.blocked, F.blockedN = {}, 0 end
	end
	if F.blocked[z] == nil then F.blockedN = F.blockedN + 1 end
	F.blocked[z] = F.clock + F.T.blockTime
end

local function distTo(a, x, y)
	local dx, dy = x - a:getX(), y - a:getY()
	return math.sqrt(dx * dx + dy * dy)
end

-- Ziel noch gueltig (jedes Mal neu: das Objekt kann seit der Wahl wiederverwendet sein, CLAUDE.md v3.9.35)
local function targetOk(B, z)
	if not z then return false end
	-- lebend entfernt (removeFromSquare setzt current auf null, Jar IsoMovingObject.removeFromSquare 38-45; getSquare taugt
	-- dafuer nicht, es behaelt IsoObject.square): kein Ziel. removeFromWorld allein faengt dropVanished (Zombieliste).
	if z:getCurrentSquare() == nil then return false end                           -- Bandits BanditUpdate.lua:574
	local ok = F.IsTarget(z)
	if not ok then return false end
	if math.abs(z:getZ() - B.a:getZ()) >= 0.5 then return false end
	if isBlocked(z) then return false end
	return distTo(B.a, z:getX(), z:getY()) <= F.T.leash
end

-- Erreicht ihn die Pranke? CanSee (LosUtil.lineClear, Waende und geschlossene Tueren sperren; Bandits BanditUpdate.lua:1203)
-- und Vanillas eigene Greif-Frage zwischen zwei Kacheln: isBlockedTo (Wand/Zaun, geschlossene oder verbarrikadierte Tuer,
-- Treppenkante) oder isWindowTo (jedes Fenster). Integrator 08.11. (kampf_review_gegen.md Fund 1): isSomethingTo fragte nur
-- das Tuer-FLAG der Kante, eine OFFENE Tuer sperrte also auch -- genau der Engpass, durch den Zombies ins Haus kommen.
-- Jar IsoGridSquare.isBlockedTo 0-40 (isWallTo/isWindowBlockedTo/isDoorBlockedTo/isStairBlockedTo ueber isEdgeElementTo).
-- Nur fuer nahe Ziele gedacht (Treffer, Ankunft).
local function canStrike(B, z)
	local bsq = B.a:getCurrentSquare()                                               -- ISAnimalContextMenu.lua:159
	local zsq = z:getCurrentSquare()                                                 -- Bandits BanditUpdate.lua:574
	if bsq == nil or zsq == nil then return false end
	if not B.a:CanSee(z) then return false end                                       -- Bandits BanditUpdate.lua:1203
	if bsq:isBlockedTo(zsq) then return false end                                    -- ISInventoryTransferAction.lua:598
	return not bsq:isWindowTo(zsq)                                                   -- ISInventoryTransferAction.lua:598
end

-- Ein Ziel wechselt nur hier (Merker, die am Ziel haengen, gehen mit).
local function setTarget(B, z)
	B.target = z
	B.nearOk = false          -- "kommt nicht naeher, schlaegt aus der Hiebweite" gilt nur fuer dieses Ziel
	B.trk = nil               -- Sprungpruefung (dropVanished) beginnt neu
end

-- Naechstes Ziel (Spez 5.2 Punkt 1): gleiche Ebene, Zombies bis "radius", feindliche Banditen bis "banditRadius" und 3 Kacheln
-- bevorzugt; die drei besten nach Abstand, Sicht (CanSee, Bandits BanditUpdate.lua:1087/:1203) nur fuer diese.
local function pickTarget(B, radius)
	local a = B.a
	local ax, ay, az = a:getX(), a:getY(), a:getZ()
	local rb = math.max(radius, radius + F.T.banditRadius - F.T.radius)
	local rmax2 = rb * rb
	local best = {}
	local list = getCell():getZombieList()                                         -- Bandits BanditZombie.lua:110
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		local dx, dy = z:getX() - ax, z:getY() - ay
		local d2 = dx * dx + dy * dy
		if d2 <= rmax2 and math.abs(z:getZ() - az) < 0.5 and not isBlocked(z) then
			local ok, isBandit = F.IsTarget(z)
			if ok then
				local d = math.sqrt(d2)
				if d <= radius or (isBandit and d <= rb) then
					local score = d - (isBandit and 3 or 0)
					best[#best + 1] = { z = z, s = score }
				end
			end
		end
	end
	if #best == 0 then return nil end
	table.sort(best, function(p, q) return p.s < q.s end)
	for i = 1, math.min(3, #best) do
		if a:CanSee(best[i].z) then return best[i].z end
	end
	return nil
end

local function fightingCount()
	local n = 0
	for _, B in ipairs(F.bears) do
		if B.phase == "act" or B.phase == "pause" or B.phase == "seek" or B.phase == "approach" then n = n + 1 end
	end
	return n
end

-- Marken loeschen: ISPetAnimal.lua:48 (clearVariable)
local function clearMarks(a)
	a:clearVariable("NCBearHit")
	a:clearVariable("NCBearDone")
end

local function clearAct(B)
	clearMarks(B.a)
	B.a:clearVariable("NCBearAct")
	B.act = nil
end

local function face(B, z)
	local a = B.a
	a:faceThisObject(z)                                                              -- ISPetAnimal.lua:17
	local dx, dy = z:getX() - a:getX(), z:getY() - a:getY()
	local l = math.sqrt(dx * dx + dy * dy)
	if l > 0.001 then B.fx, B.fy = dx / l, dy / l end
end

-- Die Engine zaehlt blockedFor nur hoch und setzt es nur bei false zurueck (Jar BaseAnimalBehavior.setBlockMovement 0-24,
-- wanderIdle 0-39); B.blockRaw spiegelt diesen Zaehler (refreshBlock).
local function setBlock(B, on)
	B.a:getBehavior():setBlockMovement(on)                                           -- ISPetAnimal.lua:36/:49
	if not on or not B.blocked then B.blockRaw = 0 end
	B.blocked = on
end

-- Die Sperre der Engine laeuft bei blockedFor >= 8000 ab (Summe des rohen getMultiplier, bei Tempo 1 rund 167 s, im Schlaf nach
-- Bildern; kampf_review_gegen.md Fund 7). Bei 4000 im selben Bild false und wieder true: false setzt den Zaehler zurueck.
local function refreshBlock(B)
	if not B.blocked then return end
	B.blockRaw = (B.blockRaw or 0) + F.rawMult
	if B.blockRaw >= BLOCK_REFRESH then
		local bh = B.a:getBehavior()
		bh:setBlockMovement(false)                                                   -- ISPetAnimal.lua:49
		bh:setBlockMovement(true)                                                    -- ISPetAnimal.lua:36
		B.blockRaw = 0
		sayMore("movement block renewed")
	end
end

local function beginAct(B, act)
	local a = B.a
	clearMarks(a)
	setBlock(B, true)          -- ruft selbst stopAllMovementNow (BaseAnimalBehavior.setBlockMovement 0-8)
	if B.target and targetOk(B, B.target) then face(B, B.target) end
	a:setVariable("NCBearAct", act)                                                  -- ISPetAnimal.lua:43
	B.act, B.actT, B.hitDone, B.phase = act, 0, false, "act"
	B.actLeft = nil
	B.lastAct = act            -- nie zweimal derselbe Clip hintereinander (ChooseAct)
	F.stats.acts = F.stats.acts + 1
	if act == "rear" then B.lastRoar = F.clock end
	if act == "slam" then B.lastSlam = F.clock end
	if (act == "swipeL" or act == "swipeR") and ZombRand(100) < 50 then             -- ZombRand(100): ISMilkAnimal.lua:25
		a:playBreedSound("growl" .. tostring(ZombRand(3) + 1))                         -- ISHutchGrabAnimal.lua:31, Rasse NCBearDefs.lua
	end
	sayMore(act .. " starts")
end

local function goApproach(B)
	setBlock(B, false)
	B.phase = "approach"
	B.issueT = -1000
	B.chkT = F.clock
	B.chkD = B.target and distTo(B.a, B.target:getX(), B.target:getY()) or 0
	if F.clock - (B.lastHuff or -1000) > HUFF_LOUD_GAP then
		B.a:playBreedSound("huff")                                                     -- ISHutchGrabAnimal.lua:31
		B.lastHuff = F.clock
	end
end

local function goSeek(B)
	setTarget(B, nil)
	setBlock(B, true)
	B.phase = "seek"
	B.seekT0 = F.clock
end

local function endFight(B, why, rest)
	local a = B.a
	clearAct(B)
	setBlock(B, false)
	setTarget(B, nil)
	B.restUntil = F.clock + (rest or 0)
	B.phase = "rest"
	B.huffQuiet = F.clock + HUFF_AFTER_FIGHT     -- nach dem Kampf 20 s kein Alltags-Schnauben (anim_spez.md 5)
	B.quietTicks = 0
	if why ~= "hurt" and B.sx and distTo(a, B.sx, B.sy) > F.T.home then
		local sq = getCell():getGridSquare(math.floor(B.sx), math.floor(B.sy), math.floor(B.sz))   -- DebugContextMenu.lua:1436
		if sq then
			a:fleeTo(sq)                                                                 -- ISMilkAnimal.lua:38
			B.phase = "return"
			B.retT0 = F.clock
		end
	end
	say("fight over (" .. why .. ")" .. (B.phase == "return" and ", going back" or ""))
end

local function startFight(B, z)
	local a = B.a
	setTarget(B, z)
	B.fightT0 = F.clock
	B.sx, B.sy, B.sz = a:getX(), a:getY(), a:getZ()
	B.strikes, B.fails = 0, 0
	B.stucks = 0               -- Ziele, an die er in diesem Kampf nicht herankam (kampf_review_gegen.md Fund 2)
	B.lastAct = nil
	F.stats.fights = F.stats.fights + 1
	local _, isBandit = F.IsTarget(z)
	local d = distTo(a, z:getX(), z:getY())
	say("fight: " .. (isBandit and "hostile bandit" or "zombie") .. " at " .. fmt(d) .. " tiles")
	-- Aufrichten + Bruellen nur hier (anim_spez.md 4.2): Abklingzeit frei, Zufall rearChance, Ziel weiter als rearDist.
	-- Steht der Zombie schon an ihm, greift er sofort an (Kevin: "unser baer soll immer angreifen").
	local rear = false
	if F.forceNext == "rear" then
		F.forceNext = nil
		rear = true
	elseif F.clock - B.lastRoar >= F.T.roarCD and d > F.T.rearDist and ZombRand(100) < F.T.rearChance then   -- ISMilkAnimal.lua:25
		rear = true
	end
	if rear then
		beginAct(B, "rear")
	else
		goApproach(B)
	end
end

-- Zaehlt gueltige Gegner ausser dem Ziel im Umkreis, optional nur im vorderen Halbkreis.
local function countFoes(B, radius, frontOnly)
	local a = B.a
	local ax, ay, az = a:getX(), a:getY(), a:getZ()
	local r2 = radius * radius
	local n = 0
	local list = getCell():getZombieList()
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		if z ~= B.target and math.abs(z:getZ() - az) < 0.5 then
			local dx, dy = z:getX() - ax, z:getY() - ay
			if dx * dx + dy * dy <= r2 and (not frontOnly or F.InCone(B.fx, B.fy, dx, dy, -90, 90)) then
				local ok = F.IsTarget(z)
				if ok then n = n + 1 end
			end
		end
	end
	return n
end

local function weight(w)
	w = math.floor((tonumber(w) or 0) + 0.5)
	if w < 0 then return 0 end
	return w
end

-- Kandidaten mit Gewicht (anim_spez.md 4.1), nach face(): B.fx/fy schaut aufs Ziel. Rueckgabe { { name, gewicht }, ... }.
function F.Candidates(B)
	local T = F.T
	local a, z = B.a, B.target
	local s = sizeOf(a)
	local dx, dy = z:getX() - a:getX(), z:getY() - a:getY()
	local d = math.sqrt(dx * dx + dy * dy)
	local ang = (d > 0.001) and F.AngleLeft(B.fx, B.fy, dx, dy) or 0
	local down = (posture(z) ~= "up")
	local c = {}
	if down and d <= T.maulReach * s and math.abs(ang) <= T.maulHalf then c[#c + 1] = { "maul", weight(T.wMaul) } end
	if not down and d <= T.biteReach * s and math.abs(ang) <= T.biteHalf then c[#c + 1] = { "bite", weight(T.wBite) } end
	c[#c + 1] = { "swipeL", weight(T.wSwipe) + ((ang > 12) and weight(T.wSide) or 0) }
	c[#c + 1] = { "swipeR", weight(T.wSwipe) + ((ang < -12) and weight(T.wSide) or 0) }
	-- Doppelschlag: Abklingzeit frei und mindestens ein weiterer Gegner vorn in der Weite (zwei vorn insgesamt)
	if F.clock - B.lastSlam >= T.slamCD and countFoes(B, T.slamReach * s, true) >= 1 then
		c[#c + 1] = { "slam", weight(T.wSlam) }
	end
	return c
end

-- Angriff waehlen: der zuletzt gespielte Clip faellt raus, dann gewichteter Zufall (ZombRand(summe), ISMilkAnimal.lua:25).
-- NCBear_NextAttack (Testdatei) erzwingt einmal einen Namen.
function F.ChooseAct(B)
	if F.forceNext then
		local f = F.forceNext
		F.forceNext = nil
		sayMore("forced attack " .. f)
		return f
	end
	local list, sum = {}, 0
	for _, e in ipairs(F.Candidates(B)) do
		if e[1] ~= B.lastAct and e[2] > 0 then
			list[#list + 1] = e
			sum = sum + e[2]
		end
	end
	if sum <= 0 then
		-- alle Gewichte 0 (Tune): Hiebe im Wechsel
		return (B.lastAct == "swipeL") and "swipeR" or "swipeL"
	end
	local r = ZombRand(sum)
	for _, e in ipairs(list) do
		if r < e[2] then return e[1] end
		r = r - e[2]
	end
	return list[#list][1]
end

-- ---------------------------------------------------------------------------------------------------------------- Knockback
-- Wie wird ein Treffer umgeworfen (anim_spez.md 2.6)? "back" = taumelt zurueck und faellt, "down" = faellt auf der Stelle,
-- "none" = nicht umwerfen. Biss stehend zieht statt zu stossen (down), Biss am Boden wirft nicht.
function F.KnockMode(act)
	if F.T.knock < 1 then return "none" end
	if act == "swipeL" or act == "swipeR" or act == "slam" then return "back" end
	if act == "bite" then return "down" end
	return "none"
end

-- Darf ein Zombie von Kachel a nach Kachel b fliegen? Vanillas eigene Frage "kann ich von hier auf diese Kachel ablegen"
-- (ISInventoryTransferAction.lua:585-608: TreatAsSolidFloor, isSolid/isSolidTrans, isBlockedTo/isWindowTo, HasStairs) plus
-- Wasser (ISWorldObjectContextMenu.lua:686-688) und isFree(false) (ISFarmingMenu.lua:463: Moebel, Baeume, kein Boden).
-- isBlockedTo = Wand, Zaun, geschlossene oder verbarrikadierte Tuer, Treppenkante (Jar IsoGridSquare.isBlockedTo 0-40);
-- eine OFFENE Tuer laesst ihn durch. Treppen gar nicht (eine Ebenenkante mitten im Flug sieht schlimmer aus als ein Fall).
local function flyOk(a, b)
	if b == nil then return false, "unloaded" end                                    -- getGridSquare nil: nicht geladen
	if not b:TreatAsSolidFloor() then return false, "no floor" end                   -- ISInventoryTransferAction.lua:590
	if b:HasStairs() then return false, "stairs" end                                -- ISInventoryTransferAction.lua:601
	local floor = b:getFloor()                                                       -- ISWorldObjectContextMenu.lua:687
	if floor ~= nil and floor:hasProperty(IsoFlagType.water) then return false, "water" end   -- ISWorldObjectContextMenu.lua:688
	if b:isSolid() or b:isSolidTrans() then return false, "solid" end               -- ISInventoryTransferAction.lua:593
	if not b:isFree(false) then return false, "furniture" end                        -- ISFarmingMenu.lua:463
	if a:isBlockedTo(b) then return false, "wall or door" end                        -- ISInventoryTransferAction.lua:598
	if a:isWindowTo(b) then return false, "window" end                               -- ISInventoryTransferAction.lua:598
	return true
end
F._flyOk = flyOk           -- TESTSCHNITTSTELLE: fuer die Attrappe

-- Ist hinter dem Zombie (Richtung rx, ry = vom Baeren weg) bis KNOCK_LEN frei? Pruefpunkte alle KNOCK_STEP Kacheln, jede neue
-- Kachel einmal, gegen die vorige (anim_spez.md 2.7). Gleiche Ebene: floor(getZ) des Zombies.
function F.ClearBehind(z, rx, ry)
	local cell = getCell()
	local zx, zy = z:getX(), z:getY()
	local zl = math.floor(z:getZ())
	local lx, ly = math.floor(zx), math.floor(zy)
	local prev = cell:getGridSquare(lx, ly, zl)                                       -- DebugContextMenu.lua:1436
	if prev == nil then return false, "unloaded" end
	if prev:HasStairs() then return false, "stairs" end                             -- ISInventoryTransferAction.lua:601
	for k = 1, KNOCK_SAMPLES do
		local px = math.floor(zx + rx * KNOCK_STEP * k)
		local py = math.floor(zy + ry * KNOCK_STEP * k)
		if px ~= lx or py ~= ly then
			local sq = cell:getGridSquare(px, py, zl)                                  -- DebugContextMenu.lua:1436
			local ok, why = flyOk(prev, sq)
			if not ok then return false, why end
			prev, lx, ly = sq, px, py
		end
	end
	return true
end

-- Sonde: je umgeworfenem Zombie Startpunkt merken, nach WATCH_TIME s eine Zeile (anim_spez.md 9 Punkt 1 und 3).
local function watchKnock(z, mode, why, dead)
	local W = F.knockWatch
	for i, e in ipairs(W) do
		if e.z == z then table.remove(W, i) break end
	end
	if #W >= MAX_WATCH then table.remove(W, 1) end
	W[#W + 1] = { z = z, mode = mode, why = why, dead = dead, x0 = z:getX(), y0 = z:getY(), t0 = F.clock, frames = 0 }
end

local function logKnock(e, st2, gone)
	local moved = math.sqrt((e.lx - e.x0) ^ 2 + (e.ly - e.y0) ^ 2)
	local line = "knock: " .. e.mode .. (e.why and (" (" .. e.why .. ")") or "") .. (e.dead and ", killing blow" or "")
		.. " | 1 frame later " .. tostring(e.st1) .. " | after " .. fmt(F.clock - e.t0) .. " s moved " .. fmt(moved)
		.. " tiles, " .. (gone and "body gone (corpse or removed)" or ("state " .. tostring(st2)))
	say(line)
	local L = F.knockLog
	if #L >= MAX_KLOG then table.remove(L, 1) end
	L[#L + 1] = line
end

-- Einmal je Bild, vor den Baeren: hoechstens MAX_WATCH Eintraege, je Eintrag ein Zustand oder eine Position.
local function stepKnockWatch()
	local W = F.knockWatch
	local i = 1
	while i <= #W do
		local e = W[i]
		local z = e.z
		local done, gone = false, false
		e.frames = e.frames + 1
		if z:getCurrentSquare() == nil then                                          -- Bandits BanditUpdate.lua:574
			-- zur Leiche geworden oder entfernt: x/y bleiben stehen (Jar IsoMovingObject.removeFromSquare 38-45)
			done, gone = true, true
		elseif math.abs(z:getX() - e.x0) + math.abs(z:getY() - e.y0) > JUMP then
			-- dasselbe Objekt weit weg: aus dem Pool als neuer Zombie (CLAUDE.md v3.9.35), nicht mehr unser Treffer
			done, gone = true, true
		else
			if e.frames == 1 then e.st1 = z:getActionStateName() end                 -- Bandits ZASmack.lua:486
			if F.clock - e.t0 >= (e.dead and WATCH_DEAD or WATCH_TIME) then done = true end
		end
		if not (gone and e.lx) then e.lx, e.ly = z:getX(), z:getY() end
		if done then
			logKnock(e, (not gone) and z:getActionStateName() or nil, gone)
			table.remove(W, i)
		else
			i = i + 1
		end
	end
end

-- Rueckfall 2.8 (Vorgabe aus, knockPush 0): je Bild hoechstens PUSH_STEP Kacheln vom Baeren weg, jede neue Kachel geprueft wie
-- im Flug. Form Bandits ZAMove.lua:11-19 (zombie:setX/setY je Bild um 0,05) und ZASmack.lua:590-596.
local function addPush(z, rx, ry)
	local P = F.pushes
	for i, p in ipairs(P) do
		if p.z == z then table.remove(P, i) break end
	end
	if #P >= MAX_PUSH then table.remove(P, 1) end
	P[#P + 1] = { z = z, rx = rx, ry = ry, left = F.T.knockPush, t0 = F.clock, zl = math.floor(z:getZ()) }
	F.knockStats.pushed = F.knockStats.pushed + 1
end

local function stepPushes()
	local P = F.pushes
	local i = 1
	while i <= #P do
		local p = P[i]
		local z = p.z
		local drop = p.left <= 0 or F.clock - p.t0 > PUSH_TIME or z:getCurrentSquare() == nil
			or math.floor(z:getZ()) ~= p.zl
		if not drop then
			local step = math.min(p.left, PUSH_STEP)
			local x, y = z:getX(), z:getY()
			local nx, ny = x + p.rx * step, y + p.ry * step
			local ox, oy, kx, ky = math.floor(x), math.floor(y), math.floor(nx), math.floor(ny)
			if ox ~= kx or oy ~= ky then
				local cell = getCell()
				local sa = cell:getGridSquare(ox, oy, p.zl)                            -- DebugContextMenu.lua:1436
				if sa == nil or not flyOk(sa, cell:getGridSquare(kx, ky, p.zl)) then drop = true end
			end
			if not drop then
				z:setX(nx)                                                             -- Bandits ZAMove.lua:12
				z:setY(ny)                                                             -- Bandits ZAMove.lua:17
				p.left = p.left - step
			end
		end
		if drop then table.remove(P, i) else i = i + 1 end
	end
end

-- Umwerfen vorbereiten und ausfuehren (anim_spez.md 2.6). Reihenfolge ist Pflicht: setPlayerAttackPosition NACH knockDown
-- (knockDown schreibt "BEHIND"/nil in die Lage, Jar IsoZombie.knockDown 0-43). Rueckgabe: tatsaechlicher Modus.
-- Bei "back" mit knockBack fliegt er NUR, wenn der Baer VOR ihm steht (testDotSide FRONT): dann gewinnt
-- to_staggerback-knockeddown (Lage FRONT): Zombie_StaggerBackFall, rund 1,7 Kacheln nach seinem eigenen Hinten.
-- Seitlich (LEFT/RIGHT) faellt er auf der Stelle (why "side"). KEIN Drehen mehr (Fixer 08.11., anim_review_technik.md Fund 1):
-- testDotSide liest den KOERPERwinkel (Jar IsoGameCharacter.getLookAngleRadians 0-53 = animPlayer.getAngle + Twist),
-- faceLocationF setzt nur forwardDirection (Jar 51-58 -> setForwardDirection 0-52); der Koerper dreht erst spaeter nach
-- (interpolateBodyAngle, hoechstens 0,15 rad je Bild). Nach einem Drehen stand also weiter LEFT/RIGHT in der Lage, und er fiel
-- verdreht auf der Stelle, waehrend die Zaehler "back" sagten. Geprueft werden BEIDE Bahnen: Baer -> Zombie und sein eigenes
-- Hinten (-getForwardDirection, Bandits ZAPush.lua:36), denn FRONT laesst bis rund 45 Grad Abweichung zu (Fund 2).
-- Ein Zombie mit dem Baeren hinter sich faellt mit frombehind nach vorn, also auch vom Baeren weg (falldown/frombehind).
local function knockSetup(B, z, act, dead, st)
	local mode = F.KnockMode(act)
	if mode == "none" then return "none" end
	local a = B.a
	-- von hinten wie Bandits ZAPush.lua:32-39
	local hdx, hdy = z:getX() - a:getX(), z:getY() - a:getY()
	local hlen = math.sqrt(hdx * hdx + hdy * hdy)
	local behind = false
	local fx, fy = 0, 0
	if hlen > 0 then
		local fwd = z:getForwardDirection()                                          -- Bandits ZAPush.lua:36
		fx, fy = fwd:getX(), fwd:getY()
		behind = (hdx * fx + hdy * fy) / hlen > 0.5
	end
	local side = z:testDotSide(a)                                                    -- Bandits ZAPush.lua:42 (Arg IsoMovingObject)
	-- zwei Masse fuer "von hinten" (Blick und Koerper, mitten in einer Drehung verschieden): eines genuegt (Pruefer Fund 4)
	local fromBehind = behind or side == "BEHIND"
	local why = nil
	local rx, ry = 0, 0
	if mode == "back" then
		if F.T.knockBack < 1 and F.T.knockPush <= 0 then
			mode, why = "down", "knockBack off"
		elseif not FLY_FROM[st or ""] then
			mode, why = "down", "state " .. tostring(st)
		elseif fromBehind then
			mode, why = "down", "bear behind him"
		elseif hlen < 0.05 then
			mode, why = "down", "too close"
		elseif F.T.knockBack >= 1 and side ~= "FRONT" then
			mode, why = "down", "side"
			F.knockStats.side = (F.knockStats.side or 0) + 1
		else
			rx, ry = hdx / hlen, hdy / hlen
			local ok, w = F.ClearBehind(z, rx, ry)
			if ok and F.T.knockBack >= 1 then
				-- sein eigenes Hinten: dorthin fliegt er (StaggerBackState haelt den Koerperwinkel)
				local fl = math.sqrt(fx * fx + fy * fy)
				if fl > 0.001 then
					ok, w = F.ClearBehind(z, -fx / fl, -fy / fl)
				end
			end
			if not ok then mode, why = "down", w end
		end
		if mode == "down" and why ~= "knockBack off" then F.knockStats.vetoed = F.knockStats.vetoed + 1 end
	end
	local fly = (mode == "back" and F.T.knockBack >= 1)
	z:setHitFromBehind(fromBehind and not fly)                                       -- Bandits ZAPush.lua:41
	z:knockDown(fromBehind)                                                          -- DebugContextMenu.lua:668
	if fly then
		z:setPlayerAttackPosition(side)                                              -- Bandits ZAPush.lua:42 (nach knockDown; side ist FRONT)
	end
	if mode == "back" then
		F.knockStats.back = F.knockStats.back + 1
		if dead then F.knockStats.killFly = F.knockStats.killFly + 1 end
		if F.T.knockPush > 0 then addPush(z, rx, ry) end
	else
		F.knockStats.down = F.knockStats.down + 1
	end
	watchKnock(z, mode, why, dead)
	return mode
end

-- Treffer nach Bandits' Weg (Spez 3.2): Leben setzen, toedlich Kill(nil), sonst umwerfen; Blut wie BanditCompatibility.Splash.
-- knockKill (anim_spez.md 2.9): auch der toedliche Treffer wird VOR Kill(nil) umgeworfen; to_staggerback-knockeddown hat in
-- idle/walktoward/pathfind/attack/lunge keinen Riegel auf bDead, die Leiche entsteht erst am Boden (ungespielt).
local function damage(B, z, amount, act, sound)
	local h = z:getHealth() - amount * F.T.dmg                                      -- Bandits BanditUpdate.lua:2391
	z:splatBlood(3, 0.3)                                                             -- Bandits BanditCompatibility.lua:130
	z:splatBlood(3, 0.3)
	local pst, st = posture(z)
	local standing = (pst == "up")
	if h <= 0 then
		z:splatBloodFloorBig()                                                       -- Bandits BanditCompatibility.lua:132
		if sound then z:playSound(SND_KILL) end                                      -- Bandits ZASmack.lua:444
		if F.T.knockKill >= 1 and standing then knockSetup(B, z, act, true, st) end
		z:Kill(nil)                                                                  -- Bandits BanditUpdate.lua:2386
		return true
	end
	z:setHealth(h)                                                                   -- Bandits BanditUpdate.lua:2397
	if sound then z:playSound(sound) end
	if standing then knockSetup(B, z, act, false, st) end
	return false
end

-- Wer im Kegel steht: Hauptziel zuerst, dann nach Abstand; hoechstens maxN.
local function hitList(B, reach, lo, hi, maxN, mainOnly)
	local a = B.a
	local ax, ay, az = a:getX(), a:getY(), a:getZ()
	local r2 = reach * reach
	local out = {}
	local list = getCell():getZombieList()
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		if (not mainOnly or z == B.target) and math.abs(z:getZ() - az) < 0.5 then
			local dx, dy = z:getX() - ax, z:getY() - ay
			local d2 = dx * dx + dy * dy
			if d2 <= r2 and F.InCone(B.fx, B.fy, dx, dy, lo, hi) then
				local ok = F.IsTarget(z)
				if ok then out[#out + 1] = { z = z, d = math.sqrt(d2), main = (z == B.target) } end
			end
		end
	end
	table.sort(out, function(p, q)
		if p.main ~= q.main then return p.main end
		return p.d < q.d
	end)
	-- Kein Treffer durch Wand, geschlossene Tuer oder Fenster, auch nicht fuer das Hauptziel (kampf_review_regeln.md Fund 1).
	-- In Reihenfolge pruefen, bis maxN getroffen sind; hoechstens SIGHT_MAX Pruefungen je Treffer.
	local hit, tests = {}, 0
	for _, e in ipairs(out) do
		if #hit >= maxN or tests >= SIGHT_MAX then break end
		tests = tests + 1
		if canStrike(B, e.z) then hit[#hit + 1] = e end
	end
	return hit
end

function F.ApplyHit(B, act)
	local T = F.T
	local s = sizeOf(B.a)
	local list
	if act == "swipeL" then
		list = hitList(B, T.swipeReach * s, -(T.swipeHalf - T.swipeShift), T.swipeHalf + T.swipeShift, math.min(T.hitCap, 1 + T.sideMax), false)
	elseif act == "swipeR" then
		list = hitList(B, T.swipeReach * s, -(T.swipeHalf + T.swipeShift), T.swipeHalf - T.swipeShift, math.min(T.hitCap, 1 + T.sideMax), false)
	elseif act == "slam" then
		list = hitList(B, T.slamReach * s, -T.slamHalf, T.slamHalf, math.min(T.hitCap, T.slamMax), false)
	elseif act == "maul" then
		list = hitList(B, T.maulReach * s, -T.maulHalf, T.maulHalf, 1, true)
		if list[1] and posture(list[1].z) == "up" then list = {} end    -- liegt oder faellt gerade
	elseif act == "bite" then
		-- Biss gegen Stehende: nur das Hauptziel, Kiefer im Treffer rund 0,9 m hoch (Bauchhoehe, anim_review_gegen.md 8); liegt es inzwischen, geht der Biss ins Leere
		list = hitList(B, T.biteReach * s, -T.biteHalf, T.biteHalf, 1, true)
		if list[1] and posture(list[1].z) ~= "up" then list = {} end
	else
		return 0, 0
	end
	local hits, kills = 0, 0
	for i, e in ipairs(list) do
		local amount, snd
		if act == "maul" then
			amount, snd = T.dmgMaul, SND_BITE
		elseif act == "bite" then
			amount, snd = T.dmgBite, SND_BITE
		elseif act == "slam" then
			-- anim_spez.md 3.2: dmgSide gilt fuer Nebenziele von Hieb UND Doppelschlag
			amount, snd = e.main and T.dmgSlam or T.dmgSide, SND_HIT_MAIN
		elseif e.main then
			amount, snd = T.dmgMain, SND_HIT_MAIN
		else
			amount, snd = T.dmgSide, SND_HIT_SIDE
		end
		if i > SND_MAX then snd = nil end
		if damage(B, e.z, amount, act, snd) then kills = kills + 1 end
		hits = hits + 1
	end
	if hits > 0 then B.lastHitT = F.clock end
	if hits > 0 and T.noise > 0 and list[1] then
		-- Laerm am Ort des Hauptziels (nie am Baeren: respondToSound rechnet die Flucht als Baer minus Laerm, Spez 4.4).
		-- addSound(Quelle, x, y, z, Radius, Lautstaerke): ISBuildAction.lua:103, AdminContextMenu.lua:260
		local z = list[1].z
		addSound(B.a, math.floor(z:getX()), math.floor(z:getY()), math.floor(z:getZ()), T.noise, T.noise)
	end
	F.stats.hits = F.stats.hits + hits
	F.stats.kills = F.stats.kills + kills
	say(act .. ": " .. hits .. " hit, " .. kills .. " killed")
	return hits, kills
end

-- Flucht vor Laerm (IsoAnimal.respondToSound) hat keinen Schalter: im Nahkampf jede fremde Bewegung sofort beenden (Spez 2).
local function fleeStop(B)
	local st = B.a:getActionStateName()                                              -- Bandits ZASmack.lua:486 (Charakter)
	if st == "walk" or st == "pathfind" then
		B.a:stopAllMovementNow()                                                     -- ISAnimalContextMenu.lua:760
		F.stats.fleeStops = F.stats.fleeStops + 1
		sayMore("stopped a move we did not order (" .. st .. ")")
	end
	return st
end

-- Kampf zu Ende? (Spez 5.2 Punkt 5) Rueckgabe true, wenn beendet.
local function fightOver(B)
	if B.sx and distTo(B.a, B.sx, B.sy) > F.T.leash then endFight(B, "too far from start"); return true end
	if F.clock - B.fightT0 > F.T.fightMax then endFight(B, "fought long enough", F.T.restAfter); return true end
	return false
end

local function decide(B)
	if fightOver(B) then return end
	local z = B.target
	if not targetOk(B, z) then goSeek(B); return end
	local s = sizeOf(B.a)
	local d = distTo(B.a, z:getX(), z:getY())
	local lim = F.T.arrive * s * 1.15
	if B.nearOk then lim = math.max(lim, F.T.swipeReach * s) end
	-- nah genug UND erreichbar (nicht durch die Wand); sonst hin bzw. drumherum
	if d > lim or not canStrike(B, z) then goApproach(B); return end
	face(B, z)                 -- Blick vor der Wahl: countFoes "vorn" rechnet mit B.fx/fy (Pruefer Fund 6 / Technik 4)
	beginAct(B, F.ChooseAct(B))
end

local function updateAct(B, dt)
	local a = B.a
	local spec = F.ACTS[B.act]
	B.actT = B.actT + dt
	local faceUntil = spec.hitPc and (spec.hitPc * spec.dur) or F.REAR_FACE
	if B.actT < faceUntil and not B.hitDone and B.target and targetOk(B, B.target) then face(B, B.target) end
	-- getVariableString: ISWorldObjectContextMenu.lua:2624 (gelesen wird die Marke aus SetVariable, Spez 1.5)
	if a:getVariableString("NCBearHit") == "true" then
		a:clearVariable("NCBearHit")
		if spec.hitPc and not B.hitDone then
			B.hitDone = true
			F.ApplyHit(B, B.act)
		end
	end
	local done = a:getVariableString("NCBearDone") == "true"
	if done or B.actT > spec.dur + F.FRIST then
		if done then
			B.strikes, B.fails = 0, 0
		else
			F.stats.expired = F.stats.expired + 1
			B.fails = (B.fails or 0) + 1
			local st = a:getActionStateName()                                        -- Bandits ZASmack.lua:486
			if B.actLeft or st ~= "idle" then
				-- er hat den Zustand idle verlassen (Flucht, Schreck): das sagt nichts ueber die Clips (Pruefer Fund 7)
				print("[NCBear] *** " .. B.act .. " did not finish in " .. fmt(spec.dur + F.FRIST) .. " s: the bear left idle (" .. tostring(B.actLeft or st) .. "); hit dropped")
			else
				B.strikes = (B.strikes or 0) + 1
				print("[NCBear] *** " .. B.act .. " did not finish in " .. fmt(spec.dur + F.FRIST) .. " s while idle (clip " .. spec.clip .. " missing in NCBear.glb?); hit dropped")
			end
		end
		clearAct(B)
		B.phase = "pause"
		B.pauseT0 = F.clock
		if B.strikes >= FRIST_STRIKES then
			print("[NCBear] *** " .. FRIST_STRIKES .. " attacks in a row never finished - fight clips probably missing. Bear rests 60 s.")
			endFight(B, "clips missing?", 60)
		elseif B.fails >= 2 * FRIST_STRIKES then
			-- Deckel fuer die Zeile oben: bricht jeder Angriff ab, hoechstens sechs Zeilen, dann Ruhe
			print("[NCBear] *** " .. B.fails .. " attacks in a row broke off (bear not idle). Bear rests 60 s.")
			endFight(B, "attacks keep breaking off", 60)
		end
	end
end

local function updateApproach(B)
	local a, z = B.a, B.target
	if fightOver(B) then return end
	if not targetOk(B, z) then goSeek(B); return end
	local s = sizeOf(a)
	local d = distTo(a, z:getX(), z:getY())
	local near = F.T.arrive * s
	if B.nearOk then near = math.max(near, F.T.swipeReach * s) end
	if d <= near and canStrike(B, z) then
		face(B, z)
		beginAct(B, F.ChooseAct(B))
		return
	end
	local st = a:getActionStateName()
	local moved = B.ix and distTo(z, B.ix, B.iy) or 999
	if F.clock - B.issueT >= REISSUE and (B.issueT < 0 or st == "idle" or moved > 1) then
		local sq = z:getSquare()
		if sq then
			a:fleeTo(sq)                                                                 -- ISMilkAnimal.lua:38
			B.issueT = F.clock
			B.ix, B.iy = z:getX(), z:getY()
		end
	end
	if F.clock - B.chkT >= F.T.stuckTime then
		if B.chkD - d < F.T.stuckGain then
			-- kommt nicht naeher (Gedraenge, Moebel), steht aber in Hiebweite und erreicht ihn: von hier zuschlagen
			if d <= F.T.swipeReach * s and canStrike(B, z) then
				B.nearOk = true
				say("cannot get closer, strikes from " .. fmt(d) .. " tiles")
				face(B, z)
				beginAct(B, F.ChooseAct(B))
				return
			end
			block(z)
			-- Deckel: hinter Zaun oder Fenster sieht er sie, kommt aber nicht hin; beim dritten Mal Kampf aus statt Pendeln
			B.stucks = (B.stucks or 0) + 1
			if B.stucks >= STUCK_MAX then
				endFight(B, "targets unreachable", F.T.restAfter)
				return
			end
			say("stuck on the way, target skipped for " .. F.T.blockTime .. " s")
			goSeek(B)
			return
		end
		B.chkT, B.chkD = F.clock, d
	end
end

-- ------------------------------------------------------------------------------------------- Ruhe: Schnauben, Sitzen, Fressen
-- Alltags-Schnauben (anim_spez.md 5): leiser Rassenton "huffsoft" (NCBearDefs.lua), ueber den Emitter, kein WorldSound.
local function huffGap(mul)
	return (F.T.huffMin + ZombRand(math.floor(F.T.huffSpread) + 1)) * (mul or 1)      -- ISMilkAnimal.lua:25
end

-- Im Suchtakt (0,5 s): Termin je Baer, dazu einmal, wenn der Spieler unter HUFF_NEAR kommt (scharf erst wieder ueber HUFF_FAR).
local function dailyHuff(B, pl, sitting)
	if F.T.huff < 1 then return end
	local c = F.clock
	local a = B.a
	local near = false
	if pl then
		local d = distTo(a, pl:getX(), pl:getY())
		if d > HUFF_FAR or math.abs(pl:getZ() - a:getZ()) >= 0.5 then
			B.huffArmed = true
		elseif d < HUFF_NEAR and B.huffArmed and c - (B.lastNearHuff or -1000) >= HUFF_NEAR_GAP then
			near = true
		end
	end
	if B.nextHuff == nil then B.nextHuff = c + huffGap(sitting and HUFF_SIT_MUL or 1) end
	if not near and c < B.nextHuff then return end
	-- nach dem Kampf still, und zwei Alltags-Schnauben nie dichter als HUFF_GAP (auch wenn beide Regeln zusammenfallen)
	if c < (B.huffQuiet or 0) or c - (B.lastSoftHuff or -1000) < HUFF_GAP then return end
	a:playBreedSound("huffsoft")                                                     -- ISHutchGrabAnimal.lua:31
	B.lastSoftHuff = c
	if near then
		B.huffArmed = false
		B.lastNearHuff = c
	end
	B.nextHuff = c + huffGap(sitting and HUFF_SIT_MUL or 1)
	sayMore("huff (" .. (near and "player close" or "now and then") .. ")")
end

-- Unterzustand wechseln: Marken weg, NCBearAct setzen (ISPetAnimal.lua:43). act nur fuer "play" (NCBear_AnimTest).
local function calmTo(B, sub, act)
	clearMarks(B.a)
	B.a:setVariable("NCBearAct", act or sub)                                         -- ISPetAnimal.lua:43
	B.calm, B.calmT = sub, 0
	if sub == "sit" then B.nextHuff = F.clock + huffGap(HUFF_SIT_MUL) end
end

local function calmStart(B, sub, dur, act)
	setTarget(B, nil)
	setBlock(B, true)          -- ruft selbst stopAllMovementNow (BaseAnimalBehavior.setBlockMovement 0-8)
	B.phase = "calm"
	B.calmNext, B.calmDur, B.playAct = nil, dur, act
	calmTo(B, sub, act)
	if sub == "sit" or sub == "eat" then B.calmUntil = F.clock + dur end
end

local function calmEnd(B, why)
	local was = B.calm
	clearAct(B)
	setBlock(B, false)
	B.phase = "rest"
	B.calm, B.calmNext, B.playAct = nil, nil, nil
	if was == "standup" then B.lastStandT = F.clock end
	B.nextHuff = F.clock + huffGap(1)
	sayMore("calm over (" .. why .. ")")
end

-- Frist eines Hinsetz-/Aufsteh-Clips: eine laute Zeile bei CALM_FAILS Verfaellen in Folge, dann still bis zum naechsten Erfolg
local function calmNote(B, done, sub)
	if done then
		B.calmFails = 0
		return
	end
	F.stats.calmExpired = (F.stats.calmExpired or 0) + 1
	B.calmFails = (B.calmFails or 0) + 1
	if B.calmFails == CALM_FAILS then
		print("[NCBear] *** " .. sub .. " did not finish " .. CALM_FAILS .. " times in a row (clip " .. F.ACTS[sub].clip
			.. " missing in NCBear.glb?)")
	end
end

-- Von selbst sitzen (anim_spez.md 6.3): alle SIT_EVERY s, nur in Ruhe und im Stehen, ohne Ziel in den letzten Suchtakten,
-- nicht kurz nach einem Treffer, einem Schmerz oder dem letzten Aufstehen; Chance sitChance.
local function autoSit(B)
	local c = F.clock
	if c < (B.nextSitCheck or 0) then return end
	B.nextSitCheck = c + SIT_EVERY
	if (B.quietTicks or 0) < SIT_QUIET then return end
	if c - (B.lastHitT or -1000) < SIT_AFTER_HIT or c - (B.lastHurtT or -1000) < SIT_AFTER_HIT then return end
	if c - (B.lastStandT or -1000) < SIT_AFTER_STAND then return end
	if ZombRand(100) >= F.T.sitChance then return end                                -- ISMilkAnimal.lua:25
	calmStart(B, "sitdown", SIT_MIN + ZombRand(SIT_SPREAD + 1))
	say("sits down by itself")
end

-- Phase calm. Kampf geht vor (anim_spez.md 6.4): sitzend erst aufstehen, fressend sofort los.
local function updateCalm(B, dt, searchNow, pl)
	local a = B.a
	fleeStop(B)
	B.calmT = B.calmT + dt
	local sub = B.calm
	if searchNow and B.calmNext == nil and F.clock >= B.restUntil and fightingCount() < MAX_FIGHTING then
		local z = pickTarget(B, F.T.radius)
		if z then
			B.quietTicks = 0
			if sub == "eat" or sub == "play" then
				calmEnd(B, "target")
				startFight(B, z)
				return
			end
			B.calmNext = z
			-- aus halbem Hinsetzen nicht springen: StandUp beginnt in der Sitzpose (Pruefer Fund 6); sitdown spielt zu Ende
			-- (hoechstens 1,6 s), dann direkt standup (Zweig sitdown unten)
			if sub == "sit" then
				calmTo(B, "standup")
				sub = "standup"
			end
			say("stands up to fight")
		else
			B.quietTicks = (B.quietTicks or 0) + 1
		end
	end
	if searchNow and sub == "sit" then dailyHuff(B, pl, true) end
	local done = a:getVariableString("NCBearDone") == "true"                         -- ISWorldObjectContextMenu.lua:2624
	local spec = F.ACTS[(sub == "play") and B.playAct or sub]
	if sub == "sitdown" then
		if done or B.calmT > spec.dur + F.FRIST then
			calmNote(B, done, sub)
			if B.calmNext then
				calmTo(B, "standup")
			else
				calmTo(B, "sit")
				B.calmUntil = F.clock + B.calmDur
			end
		end
	elseif sub == "sit" then
		if F.clock >= B.calmUntil then calmTo(B, "standup") end
	elseif sub == "eat" then
		if F.clock >= B.calmUntil then calmEnd(B, "done eating") end
	elseif sub == "standup" then
		if done or B.calmT > spec.dur + F.FRIST then
			calmNote(B, done, sub)
			local z = B.calmNext
			calmEnd(B, "stood up")
			if z and targetOk(B, z) then startFight(B, z) end
		end
	elseif sub == "play" then
		if spec.loop then
			if B.calmT >= spec.dur * PLAY_LOOP then calmEnd(B, "test clip played") end
		elseif done or B.calmT > spec.dur + F.FRIST then
			if not done then
				print("[NCBear] *** test clip " .. spec.clip .. " did not finish in " .. fmt(spec.dur + F.FRIST) .. " s (missing in NCBear.glb?)")
			end
			calmEnd(B, "test clip played")
		end
	end
end

local function updateBear(B, dt, searchNow, pl)
	local a = B.a
	local h = a:getHealth()                                                          -- ISAnimalUI.lua:15
	local hurt = B.lastHealth ~= nil and h < B.lastHealth - 0.005
	B.lastHealth = h
	if hurt then
		-- Getroffen (nur Spieler koennen das, Spez 3.6): Kampf bzw. Ruhe ab, die Engine laesst ihn fliehen (fleeFromAttacker).
		B.lastHurtT = F.clock
		if B.phase == "calm" then
			calmEnd(B, "hurt")
		elseif B.phase ~= "rest" or B.blocked then
			endFight(B, "hurt", F.T.restAfter)
		end
		B.restUntil = F.clock + F.T.restAfter
		return
	end
	refreshBlock(B)
	local p = B.phase
	if p == "act" then
		local st = fleeStop(B)
		if st ~= "idle" and B.actT > 0.5 then B.actLeft = st end   -- erst nach 0,5 s: das Anhalten beim Ankommen braucht Bilder
		updateAct(B, dt)
	elseif p == "pause" then
		fleeStop(B)
		if F.clock - B.pauseT0 >= F.T.pause then decide(B) end
	elseif p == "approach" then
		updateApproach(B)
	elseif p == "seek" then
		fleeStop(B)
		if fightOver(B) then return end
		if searchNow then
			local z = pickTarget(B, F.T.nextRadius)
			if z then
				setTarget(B, z)
				decide(B)
				return
			end
		end
		if F.clock - B.seekT0 > F.T.noTarget then endFight(B, "no target") end
	elseif p == "calm" then
		updateCalm(B, dt, searchNow, pl)
	elseif p == "return" or p == "rest" then
		if p == "return" and (distTo(a, B.sx, B.sy) < 2 or F.clock - B.retT0 > 20) then B.phase = "rest" end
		if not searchNow then return end
		if F.clock >= B.restUntil and fightingCount() < MAX_FIGHTING then
			local z = pickTarget(B, F.T.radius)
			if z then
				B.quietTicks = 0
				startFight(B, z)
				return
			end
			B.quietTicks = (B.quietTicks or 0) + 1
		end
		local st = a:getActionStateName()                                            -- Bandits ZASmack.lua:486
		if st == "idle" or st == "walk" or st == "pathfind" then dailyHuff(B, pl, false) end
		if B.phase == "rest" and st == "idle" then autoSit(B) end
	end
end

local function register(a)
	if F.byObj[a] then return end
	if #F.bears >= MAX_BEARS then
		if not F.fullSaid then print("[NCBear] more than " .. MAX_BEARS .. " bears loaded, extra ones do not fight"); F.fullSaid = true end
		return
	end
	local B = { a = a, phase = "rest", restUntil = 0, lastRoar = -1000, lastSlam = -1000, fx = 1, fy = 0, blocked = false }
	B.lastHealth = a:getHealth()
	-- Ruhe und Schnauben: erste Pruefungen nicht sofort nach dem Laden
	B.nextSitCheck = F.clock + SIT_EVERY
	B.nextHuff = F.clock + huffGap(1)
	B.huffArmed = true
	B.quietTicks = 0
	-- ein Objekt, das mit gesetzter Marke zurueckkommt, stuende sonst im letzten Clipbild (Knoten Prioritaet 10, Technik Fund 5)
	clearMarks(a)
	a:clearVariable("NCBearAct")                                                     -- ISPetAnimal.lua:48
	F.bears[#F.bears + 1] = B
	F.byObj[a] = B
	sayMore("bear registered (" .. #F.bears .. ")")
end

local function gone(a)
	return not a:isExistInTheWorld() or a:isDead()                                   -- ISAnimalUI.lua:15, ISHutchUI.lua:427
end

-- Baeren finden: Liste und Abfragen wie NCBearSpawn.lua (DebugContextMenu.lua:615-623, ISAnimalUI.lua:65). Nur "bear",
-- nie "bearstag" (der Rueckfall hat die Kampf-Clips nicht, Spez 1.2).
local function scanBears()
	local keep = {}
	for _, B in ipairs(F.bears) do
		if gone(B.a) then
			-- nicht tot (Anhaenger, entladen): Marke und Sperre loesen, sonst kaeme er gesperrt zurueck (Pruefer Fund 5).
			-- setBlockMovement(false) schreibt nur zwei Felder (Jar BaseAnimalBehavior.setBlockMovement 14-24).
			if not B.a:isDead() and (B.act or B.blocked) then
				clearAct(B)
				if B.blocked then setBlock(B, false) end
			end
			F.byObj[B.a] = nil
		else
			keep[#keep + 1] = B
		end
	end
	F.bears = keep
	local list = getCell():getObjectListForLua()
	for i = 0, list:size() - 1 do
		local o = list:get(i)
		if instanceof(o, "IsoAnimal") and o:getAnimalType() == "bear" and not gone(o) then register(o) end
	end
end

local function releaseAll()
	for _, B in ipairs(F.bears) do
		if not gone(B.a) then
			clearAct(B)
			if B.blocked then setBlock(B, false) end
		end
		B.phase = "rest"
		B.calm, B.calmNext, B.playAct = nil, nil, nil
		setTarget(B, nil)
	end
	F.pushes = {}
end

-- Ziel noch in der Welt? IsoZombie.removeFromWorld nimmt ihn aus getZombieList (Jar Offset 159-170), laesst aber isAlive,
-- Leben und x/y stehen; aus dem Pool kommt dasselbe Objekt als neuer Zombie zurueck (CLAUDE.md v3.9.35). Einmal je Suchtakt
-- ein Durchlauf fuer alle Ziele (hoechstens MAX_BEARS); dazu: springt das Ziel ueber JUMP Kacheln, ist es ein anderes.
local function dropVanished()
	local want, n = nil, 0
	for _, B in ipairs(F.bears) do
		local z = B.target
		if z then
			if want == nil then want = {} end
			if want[z] == nil then want[z] = false; n = n + 1 end
		end
	end
	if n == 0 then return end
	local list = getCell():getZombieList()                                         -- Bandits BanditZombie.lua:110
	local found = 0
	for i = 0, list:size() - 1 do
		local z = list:get(i)
		if want[z] == false then
			want[z] = true
			found = found + 1
			if found >= n then break end
		end
	end
	for _, B in ipairs(F.bears) do
		local z = B.target
		if z then
			local lost = (want[z] ~= true)
			if not lost and B.trk == z and distTo(z, B.tx, B.ty) > JUMP then lost = true end
			if lost then
				sayMore("target left the world")
				setTarget(B, nil)
			else
				B.trk, B.tx, B.ty = z, z:getX(), z:getY()
			end
		end
	end
end

local function tickBody(dt)
	F.clock = F.clock + dt
	if F.clock >= F.nextScan then
		F.nextScan = F.clock + SCAN_EVERY
		scanBears()
	end
	local searchNow = false
	local pl = nil
	if F.clock >= F.nextSearch then
		F.nextSearch = F.clock + SEARCH_EVERY
		searchNow = true
		dropVanished()
		pl = getSpecificPlayer(0)                                                    -- DebugContextMenu.lua:921 (Alltags-Schnauben)
	end
	-- je hoechstens 8 Eintraege: Sonde "wie weit flog er" vor den Baeren (Zustand ein Bild nach dem Treffer), Rueckfall-Schieben
	if #F.knockWatch > 0 then stepKnockWatch() end
	if #F.pushes > 0 then stepPushes() end
	for _, B in ipairs(F.bears) do
		if not gone(B.a) then updateBear(B, dt, searchNow, pl) end
	end
end
F._tickBody = tickBody     -- TESTSCHNITTSTELLE: fuer die Attrappe

-- Kampfuhr in Animationssekunden: die Animation laeuft mit getTimeDelta = getMultiplier / 0,8 / 60 (Jar GameTime
-- getTimeDeltaFromMultiplier, IsoGameCharacter.getAnimationTimeDelta). getMultiplier: ISAnimalTracksFinder.lua:28.
-- F.rawMult ist der UNGEDECKELTE Wert fuer die Sperre der Engine (refreshBlock); die Kampfuhr taugt dafuer nicht.
local function onTick()
	if not F.enabled or not isSP() then return end
	local raw = getGameTime():getMultiplier()
	if raw < 0 then raw = 0 end
	F.rawMult = raw
	local dt = raw / 48
	if dt > DT_MAX then dt = DT_MAX end
	-- Kein pcall als Tarnkappe: ein Fehler wird EINMAL laut gemeldet und schaltet den Kampf ab (sonst je Bild ein Stacktrace).
	local ok, err = pcall(tickBody, dt)
	if not ok then
		F.enabled = false
		print("[NCBear] *** fight error, fight switched OFF (NCBear_Fight(true) to try again): " .. tostring(err))
		local ok2, err2 = pcall(releaseAll)
		if not ok2 then print("[NCBear] *** release after error failed too: " .. tostring(err2)) end
	end
end

local function hook()
	if F.hooked then return end
	Events.OnTick.Add(onTick)                                                        -- DebugContextMenu.lua:1491
	F.hooked = true
end

local function onGameStart()
	if isSP() then hook() end
end
Events.OnGameStart.Add(onGameStart)                                                -- ISChat.lua:1186

-- Schnittstelle fuer Befehle (anim_spez.md 6.5): NCBearAct schreibt weiter nur diese Datei. Heute ruft sie nur die Testdatei
-- client/NCBearBench.lua, spaeter die Befehle (B2b). Rueckgabe je Aufruf: ok (true/false) und ein kurzer Grund.
local function calmReady(B)
	if not F.enabled then return false, "bear fight is OFF (NCBear_Fight(true))" end
	if not isSP() then return false, "singleplayer only" end
	if not B or gone(B.a) then return false, "no bear" end
	return true
end

local function clampSec(sek, def)
	local v = tonumber(sek) or def
	if v < 5 then v = 5 end
	if v > 3600 then v = 3600 end
	return v
end

-- Naechster gemerkter Baer in r Kacheln um x/y (Baeren werden alle SCAN_EVERY s gesucht).
function F.NearestBear(x, y, r)
	local best, bd = nil, r
	for _, B in ipairs(F.bears) do
		if not gone(B.a) then
			local d = distTo(B.a, x, y)
			if d <= bd then best, bd = B, d end
		end
	end
	return best, bd
end

function F.Calm.Sit(B, sek)
	local ok, why = calmReady(B)
	if not ok then return false, why end
	sek = clampSec(sek, SIT_DEFAULT)
	if B.phase == "calm" then
		if B.calm == "sit" then
			B.calmUntil = F.clock + sek
			return true, "sits longer"
		elseif B.calm == "sitdown" then
			B.calmDur = sek
			return true, "is sitting down"
		elseif B.calm == "standup" then
			return false, "is standing up"
		end
		calmEnd(B, "new order")
	elseif B.phase ~= "rest" and B.phase ~= "return" then
		return false, "fighting (" .. B.phase .. ")"
	end
	calmStart(B, "sitdown", sek)
	return true, "sits down for " .. sek .. " s"
end

function F.Calm.Stand(B)
	local ok, why = calmReady(B)
	if not ok then return false, why end
	if B.phase ~= "calm" then return false, "not sitting or eating (" .. B.phase .. ")" end
	if B.calm == "sitdown" then
		B.calmDur = 0          -- erst zu Ende hinsetzen (StandUp beginnt in der Sitzpose), dann sofort aufstehen
		return true, "stands up after sitting down"
	elseif B.calm == "sit" then
		calmTo(B, "standup")
		return true, "stands up"
	elseif B.calm == "standup" then
		return true, "is already standing up"
	end
	calmEnd(B, "order")
	return true, "stops"
end

function F.Calm.Eat(B, sek)
	local ok, why = calmReady(B)
	if not ok then return false, why end
	sek = clampSec(sek, EAT_DEFAULT)
	if B.phase == "calm" then
		if B.calm == "eat" then
			B.calmUntil = F.clock + sek
			return true, "eats longer"
		elseif B.calm ~= "play" then
			return false, "is sitting (NCBear_Stand() first)"
		end
		calmEnd(B, "new order")
	elseif B.phase ~= "rest" and B.phase ~= "return" then
		return false, "fighting (" .. B.phase .. ")"
	end
	calmStart(B, "eat", sek)
	return true, "eats for " .. sek .. " s"
end

-- Einen Clip einmal abspielen (NCBear_AnimTest), ohne Kampf und ohne Schaden: ein Treffer-Ereignis wird nicht gelesen.
-- TESTSCHNITTSTELLE (NCBear_AnimTest)
function F.Calm.Play(B, act)
	local ok, why = calmReady(B)
	if not ok then return false, why end
	local spec = F.ACTS[act]
	if not spec then return false, "unknown clip name " .. tostring(act) end
	if B.phase == "calm" then
		if B.calm ~= "play" and B.calm ~= "eat" then return false, "is sitting (NCBear_Stand() first)" end
		calmEnd(B, "new order")
	elseif B.phase ~= "rest" and B.phase ~= "return" then
		return false, "fighting (" .. B.phase .. ")"
	end
	calmStart(B, "play", 0, act)
	return true, "plays " .. spec.clip .. (spec.loop and (" (loop, " .. fmt(spec.dur * PLAY_LOOP) .. " s)") or "")
end

-- Konsole -------------------------------------------------------------------------------------------------------------

function NCBear_Fight(on)
	if on == nil then
		print("[NCBear] fight is " .. (F.enabled and "ON" or "OFF") .. (isSP() and "" or " (multiplayer: does nothing)") .. ", bears " .. #F.bears)
		return
	end
	if not isSP() then
		print("[NCBear] bear fight is singleplayer only for now (multiplayer is open, see kampf_lua.md)")
		return
	end
	local want = (on == true or on == 1 or on == "on")
	if want then
		F.enabled = true
		hook()
		print("[NCBear] bear fight ON")
	else
		F.enabled = false
		releaseAll()
		print("[NCBear] bear fight OFF, bears released")
	end
end

function NCBear_Tune(field, value)
	if field == nil then
		local keys = {}
		for k in pairs(F.T) do keys[#keys + 1] = k end
		table.sort(keys)
		for _, k in ipairs(keys) do
			local r = F.RANGE[k]
			print("[NCBear] " .. k .. " = " .. tostring(F.T[k]) .. (r and ("   (" .. r[1] .. " .. " .. r[2] .. ")") or ""))
		end
		return
	end
	local r = F.RANGE[field]
	if F.T[field] == nil or not r then
		print("[NCBear] unknown field " .. tostring(field) .. ", NCBear_Tune() lists all")
		return
	end
	if value == nil then
		print("[NCBear] " .. field .. " = " .. tostring(F.T[field]))
		return
	end
	local v = tonumber(value)
	if v == nil then
		print("[NCBear] " .. field .. ": not a number: " .. tostring(value))
		return
	end
	if v < r[1] then v = r[1] end
	if v > r[2] then v = r[2] end
	F.T[field] = v
	print("[NCBear] " .. field .. " = " .. tostring(v) .. " (until the game is restarted)")
end

function NCBear_FightInfo()
	local S = F.stats
	print("[NCBear] fight " .. (F.enabled and "ON" or "OFF") .. ", clock " .. fmt(F.clock) .. " s, bears " .. #F.bears
		.. " | fights " .. S.fights .. ", attacks " .. S.acts .. ", hits " .. S.hits .. ", kills " .. S.kills
		.. ", expired " .. S.expired .. ", flee stops " .. S.fleeStops)
	local K = F.knockStats
	print("[NCBear] knock: back " .. K.back .. " (killing blows " .. K.killFly .. "), down " .. K.down .. " (bear at his side " .. (K.side or 0) .. ")"
		.. ", back vetoed " .. K.vetoed .. ", pushed " .. K.pushed .. " | calm clips expired " .. (S.calmExpired or 0))
	for i, B in ipairs(F.bears) do
		local line = "  bear " .. i .. ": " .. B.phase .. (B.act and (" " .. B.act) or "") .. (B.calm and (" " .. B.calm) or "")
		if B.target then line = line .. ", target at " .. fmt(distTo(B.a, B.target:getX(), B.target:getY())) end
		line = line .. ", roar in " .. fmt(math.max(0, F.T.roarCD - (F.clock - B.lastRoar)))
			.. " s, slam in " .. fmt(math.max(0, F.T.slamCD - (F.clock - B.lastSlam))) .. " s"
		if F.clock < B.restUntil then line = line .. ", resting " .. fmt(B.restUntil - F.clock) .. " s" end
		print(line)
	end
end
