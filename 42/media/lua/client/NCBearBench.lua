--
-- NUR TESTHILFE (NCBearBench*: wird NIE nach NPC Crew kopiert, Kevin 08.11.: Testbefehle nur in Bench-Dateien). Konsole, Spiel mit -debug.
-- F2 (Lauf baer-f2, PLAN_F2.md 1.1, 4.6): die acht alten Befehle laufen jetzt ueber den Clip-Spieler NCBearBenchClip (Test-Arten) bzw.
-- ueber U.PoseAct am EIGENEN gezaehmten Baeren (client/BanditsNPCBearPose.lua). Die alte Kampf-Datei shared/NCBearFight.lua ist ein Stummel;
-- die Test-Art "ncbear" (shared/NCBearBenchDefs.lua) kaempft nicht mehr (Frage F-G5) -- gekaempft wird mit dem eigenen Baeren
-- (client/NCBearBenchFight.lua: NCBear_FightZed, NCBear_FightNext ...).
--
-- Nur Einzelspieler ("not isServer() and not isClient()"); im Mehrspieler sagt jeder Befehl "singleplayer only".
-- Baer = das Naechste in 12 Kacheln um die eigene Figur: ein Test-Baer (Art ncbear, alt bear / bearstag) oder dein gezaehmter Baer.
--   NCBear_Sit(sek)          Test-Baer: hinsetzen, sek Sekunden sitzen (Vorgabe 60), aufstehen. Eigener Baer: Befehl "Sit" (wie das Fenster)
--   NCBear_Stand()           Test-Baer: aufstehen bzw. aufhoeren. Eigener Baer: Befehl "Stay"
--   NCBear_Eat(sek)          Test-Baer: fressen (Vorgabe 30 s). Eigener Baer: der Fress-Clip einmal (U.PoseAct "eat")
--   NCBear_Huff()            leises Schnauben einmal (playBreedSound "huffsoft"; am Jungen gibt es die Stimme nicht)
--   NCBear_NextAttack(name)  = NCBear_FightNext(name) (client/NCBearBenchFight.lua): der naechste Angriff DEINES Baeren
--   NCBear_AnimTest(name)    einen Clip einmal spielen (Namen aus B.CLIPS; NCBear_AnimTest() listet sie). K1 (Claude 13.11. ~22:25): die acht
--                            Schlaf-Schluessel (liedown, sleep, wakeup, wakealarm, curlin, sleepcurl, curlout, wakecurl) nur bei
--                            B.CFG.sleepClips == true -- ihre Clips / Knoten bringt erst F3b; abgespielt stuende der Baer sonst stehend still
--   NCBear_TagPose(on)       K1 (PLAN_K1.md 10): Schild folgt der Pose an / aus (B.CFG.tagPoseOn; ohne Wert umschalten) und zeigt den
--                            Faktor U.PoseLift deines Baeren jetzt (client/BanditsNPCBearPose.lua)
--   NCBear_ZHealth(h, r)     Zombies und feindlichen Banditen (B.FoeIsTarget) in r Kacheln das Leben h geben (Deckel 50)
--   NCBear_KnockInfo()       Zombies in 6 Kacheln um deinen Baeren: Zustand, liegt, Leben (der Flug-Zaehler der alten Datei ist weg)
-- Sit, Eat und AnimTest drehen den Baeren beim Beginn zur Kamera (Kevin 08.11.: "in der position wo er zur kamera guckt");
-- setDir(IsoDirections.SE) an einem Tier: V:shared/Definitions/animal/ButcheringUtil.lua:574 (NE), gespielt mit SE (alte NCBearBench.lua).
--
-- Clip-Spieler NCBearBenchClip (global, nur Testhilfe; auch client/NCBearBenchGen.lua benutzt ihn fuer den 2c-Baeren "ncbear"):
-- setzt die Anim-Variable "NCBearAct" SELBST (der Kern fuehrt Test-Arten nie: B.BodyKind kennt nur ncbearcub / ncbeargrown) und
-- loescht sie NUR nach der Uhr aus B.CLIPS (B.ClipMs, shared/BanditsNPCBearFightRules.lua) -- kein getVariableString. Die Knoten liegen unter
-- AnimSets/buck/idle/NCBear_*.xml (Bedingung NCBearAct = Name). Haelt den Test-Baeren dabei fest (setBlockMovement, ISPetAnimal.lua:36/:49).
-- Takt nur, solange ein Clip laeuft (Deckel CLIP_MAX). Engine-Aufrufe:
--   animal:setVariable(Text, Text) / clearVariable(Text): V:shared/TimedActions/Animals/ISPetAnimal.lua:43 / :48
--   animal:getBehavior():setBlockMovement(b): ISPetAnimal.lua:36 / :49
--   getCell():getObjectListForLua(), instanceof(o, "IsoAnimal"): V:client/DebugUIs/DebugContextMenu.lua:612-615
--   animal:getAnimalType(): V:client/ISUI/Animal/ISAnimalUI.lua:65; isExistInTheWorld: :15; isDead: V:client/ISUI/Hutch/ISHutchUI.lua:427
--   animal:getX()/getY(): ButcheringUtil.lua:575-576; player:getX()/getY(): V:client/Fishing/TensionUI.lua:11
--   animal:playBreedSound(Text): V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19
--   getCell():getZombieList(), :size(), :get(i): B:client/BanditZombie.lua:110; z:getModData(): B:shared/BanditBrain.lua:4;
--   z:getVariableBoolean("Bandit"): B:client/BanditMenu.lua:153; z:isAlive(): B:client/BanditUpdate.lua:1087; z:getHealth(): :1203;
--   z:setHealth(h): B:client/BanditClientCommands.lua:36; z:getActionStateName(): B:client/BanditMenu.lua:161; z:isProne():
--   B:shared/ZombieActions/ZASmack.lua:486; z:isOnFloor(): B:shared/BanditUtils.lua:362
--   getTimestampMs(): V:client/Foraging/ISBaseIcon.lua:485; Events.OnTick.Add: V:client/Chat/ISChat.lua:943
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local NEAR = 12            -- Baer um die eigene Figur
local ZH_MAX = 50          -- NCBear_ZHealth: hoechstens so viele Zombies
local CLIP_MAX = 16        -- Clip-Spieler: hoechstens so viele Tiere zugleich
local LOOP_N = 3           -- NCBear_AnimTest mit einem Schleifen-Clip (sit, eat): so viele Durchlaeufe
local HOLD_RENEW_MS = 60000    -- Halt alle 60 s erneuern (die Sperre der Engine laeuft nach ~167 s ab, alte NCBearFight.lua:149)
local ACT = "NCBearAct"
local MARKS = { "NCBearHit", "NCBearDone" }
local TEST = { ncbear = true, bear = true, bearstag = true }

-- Vanillas eigener Test: V:shared/TimedActions/ISEatFoodAction.lua:136
local function isSP()
    return not isClient() and not isServer()
end

local function say(s)
    print("[NCBear] " .. s)
end

local function player()
    local p = getSpecificPlayer(0)                      -- V:client/Farming/CFarmingSystem.lua:45
    if not p then say("no player yet") end
    return p
end

local function gone(a)
    return a == nil or not a:isExistInTheWorld() or a:isDead()
end

-- Clip-Laenge in ms aus der EINEN Tabelle (B.ClipMs, KERN). Fehlt sie: nil (dann spielt nichts).
local function clipMs(key)
    if not B.ClipMs then return nil end
    return B.ClipMs(key, 0.1, "big")
end

-- ---------------------------------------------------------------------------
-- NCBearBenchClip: Clip-Spieler fuer Test-Arten
-- ---------------------------------------------------------------------------
NCBearBenchClip = NCBearBenchClip or {}
local C = NCBearBenchClip
C.list = C.list or {}       -- { a, sub ("play" / "sitdown" / "sit" / "standup" / "eat"), act, t0, dur, sek, standNow, holdAt }
local hooked = false

function C.IsTest(a)
    if a == nil or not instanceof(a, "IsoAnimal") then return false end
    return TEST[a:getAnimalType()] == true
end

local function entryOf(a)
    for i = 1, #C.list do
        if C.list[i].a == a then return C.list[i] end
    end
    return nil
end

local function marks(a)
    for i = 1, #MARKS do a:clearVariable(MARKS[i]) end
end

local function setSub(e, sub, act, dur, now)
    marks(e.a)
    e.a:setVariable(ACT, act or sub)
    e.sub, e.act, e.t0, e.dur = sub, act, now, dur
end

local function release(e)
    if gone(e.a) then return end
    marks(e.a)
    e.a:clearVariable(ACT)
    e.a:getBehavior():setBlockMovement(false)
end

local function step(e, now)
    if now - e.holdAt >= HOLD_RENEW_MS or now < e.holdAt then
        local bh = e.a:getBehavior()
        bh:setBlockMovement(false)
        bh:setBlockMovement(true)
        e.holdAt = now
    end
    local dt = now - e.t0
    if dt < 0 then dt = 0 end
    if e.sub == "sitdown" then
        if dt >= e.dur then
            if e.standNow then
                setSub(e, "standup", nil, clipMs("standup") or 1400, now)
            else
                setSub(e, "sit", nil, e.sek, now)
            end
        end
    elseif e.sub == "sit" then
        if dt >= e.dur then setSub(e, "standup", nil, clipMs("standup") or 1400, now) end
    elseif dt >= e.dur then
        return true                                     -- standup / eat / play fertig
    end
    return false
end

local function onTick()
    if #C.list == 0 then return end
    local now = getTimestampMs()
    local keep = {}
    for i = 1, #C.list do
        local e = C.list[i]
        if gone(e.a) then
            local _ = e                                 -- entladen oder tot: nichts mehr anfassen
        elseif step(e, now) then
            release(e)
        else
            keep[#keep + 1] = e
        end
    end
    C.list = keep
end

local function hook()
    if hooked then return end
    hooked = true
    Events.OnTick.Add(onTick)
end

local function start(a, sub, act, dur, sek)
    local e = entryOf(a)
    if e == nil then
        if #C.list >= CLIP_MAX then return nil end
        e = { a = a }
        C.list[#C.list + 1] = e
        a:getBehavior():setBlockMovement(true)
    end
    e.sek, e.standNow, e.holdAt = sek, nil, getTimestampMs()
    setSub(e, sub, act, dur, e.holdAt)
    hook()
    return e
end

function C.Busy(a)
    local e = entryOf(a)
    return e ~= nil and e.sub ~= nil
end

-- Einen Clip einmal (Schleifen-Clips LOOP_N mal). Rueckgabe ok, Text.
function C.Play(a, act)
    if not C.IsTest(a) or gone(a) then return false, "not a test bear" end
    local spec = B.CLIPS and B.CLIPS[act]
    local ms = clipMs(act)
    if type(spec) ~= "table" or not ms then return false, "unknown clip " .. tostring(act) .. " (B.CLIPS)" end
    local e = entryOf(a)
    if e and (e.sub == "sitdown" or e.sub == "sit" or e.sub == "standup") then return false, "is sitting (NCBear_Stand() first)" end
    if spec.loop then ms = ms * LOOP_N end
    if not start(a, "play", act, ms) then return false, "too many test bears busy" end
    return true, "plays " .. act .. " (" .. string.format("%.1f", ms / 1000) .. " s)"
end

function C.Sit(a, sek)
    if not C.IsTest(a) or gone(a) then return false, "not a test bear" end
    local down = clipMs("sitdown")
    if not down then return false, "no clip table (B.CLIPS) loaded" end
    local ms = (tonumber(sek) or 60) * 1000
    local e = entryOf(a)
    if e and e.sub == "sit" then
        e.t0, e.dur = getTimestampMs(), ms
        return true, "sits longer"
    end
    if e and e.sub == "sitdown" then
        e.sek, e.standNow = ms, nil
        return true, "is sitting down"
    end
    if e and e.sub == "standup" then return false, "is standing up" end
    if not start(a, "sitdown", nil, down, ms) then return false, "too many test bears busy" end
    return true, "sits down for " .. math.floor(ms / 1000) .. " s"
end

function C.Eat(a, sek)
    if not C.IsTest(a) or gone(a) then return false, "not a test bear" end
    if not clipMs("eat") then return false, "no clip table (B.CLIPS) loaded" end
    local e = entryOf(a)
    if e and (e.sub == "sitdown" or e.sub == "sit" or e.sub == "standup") then return false, "is sitting (NCBear_Stand() first)" end
    local ms = (tonumber(sek) or 30) * 1000
    if not start(a, "eat", nil, ms) then return false, "too many test bears busy" end
    return true, "eats for " .. math.floor(ms / 1000) .. " s"
end

function C.Stand(a)
    local e = entryOf(a)
    if e == nil or e.sub == nil then return false, "not sitting or eating" end
    if e.sub == "sitdown" then
        e.standNow = true                               -- erst zu Ende hinsetzen, dann sofort aufstehen
        return true, "stands up after sitting down"
    elseif e.sub == "sit" then
        setSub(e, "standup", nil, clipMs("standup") or 1400, getTimestampMs())
        return true, "stands up"
    elseif e.sub == "standup" then
        return true, "is already standing up"
    end
    e.dur = 0                                           -- Fressen / Clip: im naechsten Takt fertig
    return true, "stops"
end

-- Naechster Test-Baer in r Kacheln um x, y (Suchlauf nur auf Befehl, nie je Bild). Rueckgabe Tier, Abstand^2.
function C.Nearest(x, y, r)
    local best, bd = nil, r * r
    local list = getCell():getObjectListForLua()
    for i = 0, list:size() - 1 do
        local a = list:get(i)
        if C.IsTest(a) and not gone(a) then
            local dx, dy = a:getX() - x, a:getY() - y
            local d = dx * dx + dy * dy
            if d <= bd then best, bd = a, d end
        end
    end
    return best, bd
end

-- ---------------------------------------------------------------------------
-- Welcher Baer ist gemeint? Der naechste Test-Baer oder der eigene gezaehmte Baer (Sicht + lebende Kopie), je naeher.
-- ---------------------------------------------------------------------------
local function own(p)
    local U = B.UI
    if not U or not U.WinBears or not U.CubObj then return nil, nil, nil end
    local best, bv, bd = nil, nil, NEAR * NEAR
    local list = U.WinBears()
    for i = 1, #list do
        local v = list[i]
        local a = (v.st == "tame") and U.CubObj(v.id) or nil
        if a then
            local dx, dy = a:getX() - p:getX(), a:getY() - p:getY()
            local d = dx * dx + dy * dy
            if d <= bd then best, bv, bd = a, v, d end
        end
    end
    return best, bv, bd
end

-- Rueckgabe: kind ("test" / "own"), Tier, Sicht-Eintrag (nur "own") -- oder nil mit einer Zeile.
local function target()
    if not isSP() then
        say("singleplayer only")
        return nil
    end
    local p = player()
    if not p then return nil end
    local t, td = C.Nearest(p:getX(), p:getY(), NEAR)
    local o, ov, od = own(p)
    if t and (not o or td <= od) then return "test", t, nil end
    if o then return "own", o, ov end
    say("no bear within " .. NEAR .. " tiles (NCBear_SpawnLive() puts a test bear next to you; your own bear needs a fresh view)")
    return nil
end

local function report(ok, why)
    say((ok and "bear " or "bear refuses: ") .. tostring(why))
end

local function turn(a)
    a:setDir(IsoDirections.SE)                          -- V:shared/Definitions/animal/ButcheringUtil.lua:574 (NE); gespielt mit SE
end

local function poseAct(v, act)
    local U = B.UI
    if not U or not U.PoseAct then
        say("the pose driver is not loaded (client/BanditsNPCBearPose.lua)")
        return false
    end
    return U.PoseAct(v.id, act) == true
end

-- ---------------------------------------------------------------------------
-- Befehle
-- ---------------------------------------------------------------------------
function NCBear_Sit(sek)
    local kind, a, v = target()
    if not kind then return end
    if kind == "own" then
        B.Ask(getSpecificPlayer(0), "Mode", { id = v.id, mode = "sit" })
        say("your bear: order Sit sent (same as the bear window)")
        return
    end
    local busy = C.Busy(a)
    local ok, why = C.Sit(a, sek)
    if ok and not busy then turn(a) end
    report(ok, why)
end

function NCBear_Stand()
    local kind, a, v = target()
    if not kind then return end
    if kind == "own" then
        B.Ask(getSpecificPlayer(0), "Mode", { id = v.id, mode = "stay" })
        say("your bear: order Stay sent (stands up)")
        return
    end
    report(C.Stand(a))
end

function NCBear_Eat(sek)
    local kind, a, v = target()
    if not kind then return end
    if kind == "own" then
        say("your bear: " .. (poseAct(v, "eat") and "eat clip once" or "eat clip refused (no clip table or no body)"))
        return
    end
    local busy = C.Busy(a)
    local ok, why = C.Eat(a, sek)
    if ok and not busy then turn(a) end
    report(ok, why)
end

function NCBear_Huff()
    local kind, a = target()
    if not kind then return end
    if kind == "own" and B.BodyKind and B.BodyKind(a) ~= "big" then
        say("a cub has no huff voice (only the big body, shared/BanditsNPCBearDefs.lua)")
        return
    end
    a:playBreedSound("huffsoft")                        -- V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19
    say("huff (soft)")
end

function NCBear_NextAttack(name)
    if NCBear_FightNext then
        NCBear_FightNext(name)
    else
        say("client/NCBearBenchFight.lua is not loaded")
    end
end

-- K1: die acht Schlaf-Schluessel von B.CLIPS (shared/BanditsNPCBearFightRules.lua:77-84) -- nur mit Schlaf-Clips (B.CFG.sleepClips, erst F3b)
local SLEEP_KEYS = { liedown = true, sleep = true, wakeup = true, wakealarm = true, curlin = true, sleepcurl = true, curlout = true,
    wakecurl = true }

local function sleepClipsOn()
    return B.CFG ~= nil and B.CFG.sleepClips == true
end

function NCBear_AnimTest(name)
    if not isSP() then
        say("singleplayer only")
        return
    end
    local clips = B.CLIPS
    if type(clips) ~= "table" then
        say("no clip table B.CLIPS (shared/BanditsNPCBearFightRules.lua not loaded)")
        return
    end
    -- K1: ohne Schlaf-Clips gibt es die acht Schlaf-Schluessel weder in der Liste noch zum Abspielen
    local hideSleep = not sleepClipsOn()
    if name ~= nil and hideSleep and SLEEP_KEYS[name] then
        say("'" .. tostring(name) .. "' is a sleep clip -- the sleep clips come with F3b (B.CFG.sleepClips is off), nothing played")
        return
    end
    if name == nil or clips[name] == nil or name == "zbite" or name == "smack" then
        local keys = {}
        for k in pairs(clips) do
            -- zbite / smack sind Zombie-/Banditen-Clips; K1: Schlaf-Schluessel nur mit Schlaf-Clips
            if k ~= "zbite" and k ~= "smack" and not (hideSleep and SLEEP_KEYS[k]) then keys[#keys + 1] = k end
        end
        table.sort(keys)
        local tail = ""
        if hideSleep then tail = " (sleep clips come with F3b)" end
        say("use NCBear_AnimTest(name), names: " .. table.concat(keys, ", ") .. tail)
        return
    end
    local kind, a, v = target()
    if not kind then return end
    if kind == "own" then
        local ok = poseAct(v, name)
        if ok then turn(a) end
        say("your bear: " .. (ok and ("plays " .. name) or "refused (no body or no clip time)"))
        return
    end
    local ok, why = C.Play(a, name)
    if ok then turn(a) end
    report(ok, why)
end

-- K1 (PLAN_K1.md 10): Schild folgt der Pose an / aus (B.CFG.tagPoseOn, nur diese Sitzung) und den Faktor deines Baeren zeigen. Ohne Wert
-- umschalten. Nur Einzelspieler (wie alle Befehle hier).
function NCBear_TagPose(on)
    if not isSP() then
        say("singleplayer only")
        return
    end
    if type(B.CFG) ~= "table" then
        say("no B.CFG")
        return
    end
    if on == nil then on = (B.CFG.tagPoseOn == false) end
    B.CFG.tagPoseOn = (on == true)
    local U = B.UI
    local msg = "tag follows the pose: " .. ((B.CFG.tagPoseOn ~= false) and "on" or "off")
    local p = player()
    if p and U and U.PoseLift then
        local _, _, v = own(p)
        if v then
            local k = U.PoseLift(v.id, getTimestampMs())                -- V:client/Foraging/ISBaseIcon.lua:485
            msg = msg .. ", your bear now x" .. string.format("%.2f", tonumber(k) or 1) .. " (phase " .. tostring(U.PosePhase(v.id)) .. ")"
        end
    end
    say(msg)
end

-- Ziel nach der Regel des Kerns (B.FoeIsTarget, shared/BanditsNPCBearFightRules.lua): Zombies und feindliche Banditen, nie Spieler,
-- Crew, Neutrale, Tiere (die Zombieliste traegt nur Zombies). Die Merkmale liest diese Testhilfe selbst (nur Lesen, Fundstellen oben).
local function foeFacts(z)
    local f = { alive = z:isAlive() and z:getHealth() > 0 }
    local md = z:getModData()
    if md and md.tcUid ~= nil then f.tcUid = md.tcUid end
    local brain = md and md.brain
    f.bandit = z:getVariableBoolean("Bandit") or brain ~= nil
    if type(brain) == "table" then
        f.recruited, f.npcNeutral, f.npcUid = brain.recruited, brain.npcNeutral, brain.npcUid
        f.fallback, f.loyal, f.hostile, f.hostileP = brain.programFallback, brain.loyal, brain.hostile, brain.hostileP
        local prog = brain.program
        if type(prog) == "table" then f.program = prog.name end
    elseif f.bandit then
        f.noBrain = true
    end
    return f
end

local function isTarget(z)
    if not B.FoeIsTarget then return false end
    local f = foeFacts(z)
    if f.noBrain then return false end                  -- Marke ohne Gehirn: im Zweifel nicht
    return B.FoeIsTarget(f) == true
end

function NCBear_ZHealth(h, r)
    if not isSP() then
        say("singleplayer only")
        return
    end
    h = tonumber(h)
    r = tonumber(r) or 10
    if not h or h <= 0 or h > 20 then
        say("use NCBear_ZHealth(h, r): h 0.1..20 (normal zombie 1.8-2.1, tough 3.5-3.8), r tiles (default 10)")
        return
    end
    if r < 1 then r = 1 end
    if r > 40 then r = 40 end
    if not B.FoeIsTarget then
        say("B.FoeIsTarget is missing (shared/BanditsNPCBearFightRules.lua not loaded)")
        return
    end
    local p = player()
    if not p then return end
    local px, py = p:getX(), p:getY()
    local list = getCell():getZombieList()
    local n, skipped = 0, 0
    for i = 0, list:size() - 1 do
        local z = list:get(i)
        local dx, dy = z:getX() - px, z:getY() - py
        if dx * dx + dy * dy <= r * r then
            if n >= ZH_MAX then
                skipped = skipped + 1
            elseif isTarget(z) then
                z:setHealth(h)                          -- B:client/BanditClientCommands.lua:36
                n = n + 1
            end
        end
    end
    say("health " .. h .. " set on " .. n .. " target(s) within " .. r .. " tiles"
        .. (skipped > 0 and (", " .. skipped .. " more skipped (cap " .. ZH_MAX .. ")") or ""))
end

-- Zombies in 6 Kacheln um den eigenen Baeren (sonst um die Figur): Aktionszustand, liegt, Leben. Hoechstens 12 Zeilen.
function NCBear_KnockInfo()
    if not isSP() then
        say("singleplayer only")
        return
    end
    local p = player()
    if not p then return end
    local cx, cy = p:getX(), p:getY()
    local a = own(p)
    if a then cx, cy = a:getX(), a:getY() end
    local list = getCell():getZombieList()
    local n = 0
    for i = 0, list:size() - 1 do
        local z = list:get(i)
        local dx, dy = z:getX() - cx, z:getY() - cy
        if dx * dx + dy * dy <= 36 and n < 12 then
            n = n + 1
            say(string.format("  zombie %.1f tiles: state %s, prone %s, on floor %s, health %.2f", math.sqrt(dx * dx + dy * dy),
                tostring(z:getActionStateName()), tostring(z:isProne()), tostring(z:isOnFloor()), z:getHealth()))
        end
    end
    local cfg = B.CFG or {}
    say("knock info: " .. n .. " zombie(s) within 6 tiles of " .. (a and "your bear" or "you")
        .. " (knockPush " .. tostring(cfg.knockPush) .. ", knockMinPct " .. tostring(cfg.knockMinPct) .. ")")
end
