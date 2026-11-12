--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Nur Einzelspieler (Konsole, Spiel
-- mit -debug). Lauf baer-gen-gross, 11.11.2026. Kevin 11.11. ~18:25 (Freigabe 3): "der Generator-Baer nur als Vergleich per Testbefehl
-- NCBear_GenLive() (braun + Fototon); Kevin waehlt spaeter".
-- F2 (Lauf baer-f2, PLAN_F2.md 1.1): der 2c-Baer ist jetzt die Test-Art "ncbear" (shared/NCBearBenchDefs.lua); die alte Kampf-Datei
-- shared/NCBearFight.lua ist ein Stummel. Den 2c-Baeren fuehrt jetzt der Clip-Spieler der Testhilfe NCBearBenchClip (client/NCBearBench.lua:
-- Play / Sit / Eat / Stand / Busy, nur Uhr aus B.CLIPS) -- also genau wie NCBear_Sit / NCBear_Eat / NCBear_AnimTest. Er hat keinen
-- Laerm-Riegel mehr (der alte kam aus NCBearFight): Laerm laesst jetzt auch ihn weglaufen.
--
-- Der neue grosse Baer E hat GENAU das Skelett und GENAU die 15 Clips des 2c-Baeren (Lauf baer-gen-gross, RIG.md); hier stehen beide Farben
-- lebend neben dem 2c-Baeren, damit Kevin Form UND Bewegung aus seiner Kamera vergleicht. Arten: shared/NCBearBenchGenDefs.lua.
--
-- Konsole:
--   NCBear_GenLive()              2c-Baer | E braun | E Fototon lebend in einer Reihe vor dir (quer ueber den Bildschirm, je ~3 Kacheln),
--                                 alle mit Blick zur Kamera. Gehen: wie beim 2c-Baeren laufen sie ab und zu von selbst ein Stueck.
--   NCBear_GenAct(name, sek)      einen Clip spielen: alle E-Baeren in 12 Kacheln UND der naechste 2c-Baer (ueber dieselbe Schnittstelle wie
--                                 NCBear_AnimTest/NCBear_Sit), alle drehen zur Kamera. Namen: sit, eat, rear, bite, maul, swipeL, swipeR, slam.
--                                 sit/eat mit sek Sekunden (Vorgabe 60/30): sit = hinsetzen, sitzen, aufstehen.
--   NCBear_GenStand()             aufstehen bzw. aufhoeren (alle E-Baeren in 12 Kacheln und der naechste 2c-Baer)
--   NCBear_GenStay() / (false)    E-Baeren in 12 Kacheln bleiben stehen (Blick zur Kamera) bzw. laufen mit false wieder frei
--   NCBear_GenRun()               E-Baeren in 12 Kacheln und der ruhende 2c-Baer rennen ~8 Kacheln quer ueber den Bildschirm (naechster
--                                 Aufruf: zurueck) -- zum Vergleich des Rennens von der Seite
--   NCBear_GenClean()             entfernt ALLE geladenen E-Baeren (der 2c-Baer bleibt; den entfernt "Remove living bears nearby")
--   NCBear_GenHelp()              diese Liste
--
-- GRENZEN (ehrlich): Laerm (Rennen, Schuesse, Zombies an Zaeunen) laesst alle drei weglaufen und bricht ihren Clip ab. Keiner kaempft
-- (der Kampf kennt nur den eigenen gezaehmten Baeren, F2).
-- SPIELSTAND: ein gespeicherter E-Baer braucht beim Laden diese Testhilfe (Art unbekannt = Laden bricht, shared/BanditsNPCBearDefs.lua Kopf;
-- eine Baerenleiche wirft ohne ihre Art ebenso, NCBearSpawn.lua:77-78). Vor dem Entfernen der Testhilfe NCBear_GenClean() ausfuehren und
-- speichern; E-Baeren dort nicht toeten (Leichen entfernt NCBear_GenClean nicht) -- oder gleich einen Wegwerf-Spielstand benutzen.
--
-- NCBearAct: je Tier genau EIN Schreiber -- diese Datei fuer die E-Arten, der Clip-Spieler NCBearBenchClip fuer den 2c-Baeren "ncbear" (hier
-- nur ueber seine Schnittstelle, wie client/NCBearBench.lua). Die Knoten AnimSets/buck/idle/NCBear_*.xml fragen nur die Variable NCBearAct.
--
-- Engine-Aufrufe (Fundstelle; "gespielt" = gespielte Testhilfe der Test-Mod):
--   getAllAnimalsDefinitions, def:getAnimalType, def:getBreeds, breeds:size/get: Vanilla client/DebugUIs/DebugContextMenu.lua:246-275
--   addAnimal(getCell(), x, y, z, typ, breed, false) + animal:addToWorld(): DebugContextMenu.lua:1460-1467 (gespielt NCBearSpawn.lua:51-56)
--   getSpecificPlayer(0): DebugContextMenu.lua:917; getCurrentSquare: :344; getCell():getGridSquare(x, y, z): :1432 und :899
--   square:getFloor() + floor:hasProperty(IsoFlagType.water): client/ISUI/ISWorldObjectContextMenu.lua:687-688 (gespielt NCBearSpawn.lua:30-32)
--   animal:setDir(IsoDirections.SE): shared/Definitions/animal/ButcheringUtil.lua:574 (NE), gespielt mit SE NCBearBench.lua:72
--   getCell():getObjectListForLua(), instanceof(x, "IsoAnimal"), animal:remove(): DebugContextMenu.lua:612-616 (rueckwaerts)
--   animal:getAnimalType(): client/ISUI/Animal/ISAnimalUI.lua:65; animal:getSquare(): client/ISUI/Animal/ISAnimalContextMenu.lua:90
--   animal:getX()/getY(): ButcheringUtil.lua:575-576; player:getX()/getY(): DebugContextMenu.lua:925/:921; square:getX/getY/getZ: :1461-1463
--   animal:isExistInTheWorld(): ISAnimalUI.lua:15; animal:isDead(): client/ISUI/Hutch/ISHutchUI.lua:427
--   animal:getBehavior():setBlockMovement(true/false): shared/TimedActions/Animals/ISPetAnimal.lua:36/:49
--   animal:setVariable("NCBearAct", s): ISPetAnimal.lua:43; animal:clearVariable(s): ISPetAnimal.lua:48
--   animal:getVariableString(s): ISWorldObjectContextMenu.lua:2660 (am Spieler; gleiche Methode am Tier gespielt in der alten NCBearFight.lua:1629;
--     NUR hier in der Testhilfe fuer die E-Arten -- der Kern und NCBearBenchClip fragen nie getVariableString)
--   animal:fleeTo(square): shared/TimedActions/Animals/ISMilkAnimal.lua:38; gespielt als Anrennen (alte NCBearFight.lua:1383). Er RENNT dabei
--     (Jar IsoAnimal.fleeTo Offset 48-65: animalRunning + pathToLocation; _arbeit/baer_laerm/forschung_laerm.md)
--   getGameTime():getMultiplier(): client/Foraging/ISAnimalTracksFinder.lua:28; Events.OnTick.Add: DebugContextMenu.lua:1487
-- Nichts Teures je Bild: der Takt tut nur etwas, solange ein E-Baer einen Clip spielt oder festgehalten wird (Deckel MAX_GEN).
--

local NEAR = 12            -- Baeren um die eigene Figur (wie NCBearBench.lua NEAR)
local MAX_GEN = 16         -- Deckel: so viele E-Baeren fuehrt der Takt hoechstens
local STEP = 2             -- Reihe: Abstand je Baer in Kacheln diagonal (2 x 2 = ~2,8 Kacheln)
local RUN = 6              -- NCBear_GenRun: so weit quer (6 x 6 diagonal = ~8,5 Kacheln)
local FRIST = 1.0          -- Clipdauer + 1 s, dann gilt der Clip als zu Ende (wie die alte NCBearFight F.FRIST)
local DT_MAX = 0.5         -- je Bild hoechstens so viel Uhr (Pause, Ladebild), wie NCBearFight DT_MAX
local BLOCK_REFRESH = 4000 -- Sperre der Engine laeuft bei 8000 ab (rohe getMultiplier-Summe, ~167 s): bei 4000 erneuern (NCBearFight.lua:149)
local SIT_DEFAULT, EAT_DEFAULT = 60, 30   -- wie NCBearFight SIT_DEFAULT / EAT_DEFAULT

local GEN = { ncbeargen = true, ncbeargenfoto = true }

-- Clip-Dauer (Sekunden) NUR aus der EINEN Tabelle B.CLIPS (shared/BanditsNPCBearFightRules.lua, F2 PLAN_F2.md 0.7) -- nach baer-gross wird nur
-- sie nachgezogen. Knoten AnimSets/buck/idle/NCBear_*.xml, Bedingung NCBearAct = Name. Das Ende eines Einmal-Clips meldet die Animation
-- (SetVariable NCBearDone=true am Ende); die Dauer + FRIST ist nur das Netz. Fehlt die Tabelle (Kern nicht geladen): Netz 3 s.
local NET_DUR = 3.0
local function durOf(key)
    local bear = BanditsNPC and BanditsNPC.Bear
    local c = bear and bear.CLIPS and bear.CLIPS[key]
    local d = c and tonumber(c.dur)
    if d == nil then return NET_DUR end
    return d
end
-- Befehlsnamen fuer NCBear_GenAct (sitdown/sit/standup laufen als Folge "sit")
local ORDER = { "sit", "eat", "rear", "bite", "maul", "swipeL", "swipeR", "slam" }
local PLAYS = { rear = true, bite = true, maul = true, swipeL = true, swipeR = true, slam = true }

-- Zustand: S.list = gefuehrte E-Baeren { a, stay, blocked, raw, sub, act, t, sek, standNow }
local S = { list = {}, hooked = false, runSign = 1, failed = false }

-- Vanillas eigener Test (ISEatFoodAction.lua:136, wie NCBearBench.lua)
local function isSP()
    return not isClient() and not isServer()
end

local function say(s)
    print("[NCBear] gen: " .. s)
end

local function player()
    local p = getSpecificPlayer(0)
    if not p then say("no player yet") end
    return p
end

local function gone(a)
    return not a:isExistInTheWorld() or a:isDead()
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

local function clampSec(sek, def)
    local v = tonumber(sek) or def
    if v < 5 then v = 5 end
    if v > 3600 then v = 3600 end
    return v
end

-- Ein lebendes Tier an here + (dx, dy), Blick zur Kamera (Bildschirm unten = Welt +x/+y = SE, NCBearBench.lua:69-72)
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
        say("animal definition not loaded: " .. typ .. " (shared/NCBearBenchGenDefs.lua / NCBearDefs.lua)")
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

-- E-Baeren (lebend, geladen) in NEAR Kacheln um die eigene Figur, hoechstens MAX_GEN
local function genNear(p)
    local px, py = p:getX(), p:getY()
    local out = {}
    local list = getCell():getObjectListForLua()
    for i = list:size(), 1, -1 do
        local a = list:get(i - 1)
        if instanceof(a, "IsoAnimal") and GEN[a:getAnimalType()] and not gone(a) then
            if math.abs(a:getX() - px) <= NEAR and math.abs(a:getY() - py) <= NEAR and #out < MAX_GEN then
                out[#out + 1] = a
            end
        end
    end
    return out
end

local function entryOf(a, create)
    for _, G in ipairs(S.list) do
        if G.a == a then return G end
    end
    if not create or #S.list >= MAX_GEN then return nil end
    local G = { a = a, stay = false, blocked = false, raw = 0 }
    S.list[#S.list + 1] = G
    return G
end

-- Sperre wie NCBearFight setBlock: true stoppt ihn selbst (Jar BaseAnimalBehavior.setBlockMovement 0-8); der Zaehler der Engine laeuft nur
-- bei false zurueck, darum G.raw nur beim Wechsel neu
local function block(G, on)
    G.a:getBehavior():setBlockMovement(on)
    if not on or not G.blocked then G.raw = 0 end
    G.blocked = on
end

local function clearMarks(a)
    a:clearVariable("NCBearHit")
    a:clearVariable("NCBearDone")
end

local function setAct(G, sub, act)
    clearMarks(G.a)
    G.a:setVariable("NCBearAct", act or sub)
    G.sub, G.act, G.t = sub, act, 0
end

local function endAct(G)
    clearMarks(G.a)
    G.a:clearVariable("NCBearAct")
    G.sub, G.act, G.standNow = nil, nil, nil
    if not G.stay and G.blocked then block(G, false) end
end

-- Nicht mehr in der Welt (entladen, Anhaenger) aber nicht tot: Marke und Sperre loesen, sonst kaeme er gesperrt bzw. im letzten Clipbild
-- zurueck (wie NCBearFight scanBears, :1771-1777)
local function drop(G)
    if not G.a:isDead() and (G.sub or G.blocked) then
        clearMarks(G.a)
        G.a:clearVariable("NCBearAct")
        if G.blocked then G.a:getBehavior():setBlockMovement(false) end
    end
end

local function step(G, dt, raw)
    if G.blocked then
        G.raw = G.raw + raw
        if G.raw >= BLOCK_REFRESH then
            local bh = G.a:getBehavior()
            bh:setBlockMovement(false)
            bh:setBlockMovement(true)
            G.raw = 0
        end
    end
    local sub = G.sub
    if not sub then return end
    G.t = G.t + dt
    local done = G.a:getVariableString("NCBearDone") == "true"
    if sub == "sitdown" then
        if done or G.t > durOf("sitdown") + FRIST then
            if G.standNow then setAct(G, "standup") else setAct(G, "sit") end
        end
    elseif sub == "sit" then
        if G.t >= G.sek then setAct(G, "standup") end
    elseif sub == "standup" then
        if done or G.t > durOf("standup") + FRIST then endAct(G) end
    elseif sub == "eat" then
        if G.t >= G.sek then endAct(G) end
    elseif sub == "play" then
        if done or G.t > durOf(G.act) + FRIST then endAct(G) end
    end
end

local function releaseAll()
    for _, G in ipairs(S.list) do
        if not gone(G.a) then
            G.stay = false
            endAct(G)
            if G.blocked then block(G, false) end
        end
    end
    S.list = {}
end

local function tickBody(dt, raw)
    local keep = {}
    for _, G in ipairs(S.list) do
        if gone(G.a) then
            drop(G)
        else
            step(G, dt, raw)
            if G.sub or G.stay or G.blocked then keep[#keep + 1] = G end
        end
    end
    S.list = keep
end

-- Uhr in Animationssekunden wie NCBearFight onTick (:1869-1875): getMultiplier / 48, je Bild hoechstens DT_MAX
local function onTick()
    if #S.list == 0 or S.failed or not isSP() then return end
    local raw = getGameTime():getMultiplier()
    if raw < 0 then raw = 0 end
    local dt = raw / 48
    if dt > DT_MAX then dt = DT_MAX end
    -- Kein pcall als Tarnkappe: ein Fehler wird EINMAL laut gemeldet, die E-Baeren werden losgelassen, der Takt schweigt bis zum naechsten
    -- Befehl (hook).
    local ok, err = pcall(tickBody, dt, raw)
    if not ok then
        S.failed = true
        print("[NCBear] *** gen: error in the comparison tick, gen bears released: " .. tostring(err))
        local ok2, err2 = pcall(releaseAll)
        if not ok2 then print("[NCBear] *** gen: release after error failed too: " .. tostring(err2)) end
    end
end

-- Nach einem Fehler schweigt der Takt; der naechste Befehl startet ihn neu (meldet er wieder einen Fehler, dann wieder EINMAL laut).
local function hook()
    if S.failed then
        S.failed = false
        say("tick restarted after an error")
    end
    if S.hooked then return end
    Events.OnTick.Add(onTick)
    S.hooked = true
end

-- Der naechste 2c-Baer (Test-Art ncbear, auch ALT bear / bearstag) ueber den Clip-Spieler der Testhilfe (client/NCBearBench.lua)
local function twoC(p)
    local C = NCBearBenchClip
    if not C or not C.Nearest or not C.Play then return nil, "client/NCBearBench.lua (NCBearBenchClip) not loaded" end
    local a = C.Nearest(p:getX(), p:getY(), NEAR)
    if not a then
        return nil, "no 2c test bear within " .. NEAR .. " tiles (NCBear_GenLive() or NCBear_SpawnLive() first)"
    end
    return a, nil
end

-- E-Baer: Befehl beginnen. Aus dem Sitzen nie in einen Stehclip springen (wie NCBearFight F.Calm.Play/Eat: "is sitting").
local function startAct(G, name, sek)
    local sub = G.sub
    if sub == "sitdown" or sub == "sit" or sub == "standup" then
        if name == "sit" and sub == "sit" then
            G.sek = G.t + sek          -- wie NCBearFight F.Calm.Sit: ab jetzt noch sek Sekunden
            return true, "sits " .. sek .. " s from now"
        end
        if name == "sit" and sub == "sitdown" then
            G.sek, G.standNow = sek, nil
            return true, "is sitting down"
        end
        if sub == "standup" then return false, "is standing up" end
        return false, "is sitting (NCBear_GenStand() first)"
    end
    if not G.blocked then block(G, true) end
    G.a:setDir(IsoDirections.SE)
    if name == "sit" then
        setAct(G, "sitdown")
        G.sek = sek
        return true, "sits down for " .. sek .. " s"
    elseif name == "eat" then
        setAct(G, "eat")
        G.sek = sek
        return true, "eats for " .. sek .. " s"
    end
    setAct(G, "play", name)
    return true, "plays " .. name
end

local function countLine(n, total, why)
    if total == 0 then return "no E bear within " .. NEAR .. " tiles (NCBear_GenLive() first)" end
    return n .. " of " .. total .. " E bear(s): " .. tostring(why)
end

-------------------------------------------------------------------------------------------------------------------------------

function NCBear_GenHelp()
    say("NCBear_GenLive()            2c bear | E brown | E photo tone, living, in a row in front of you, facing the camera")
    say("NCBear_GenAct(name, sek)    play on all E bears within " .. NEAR .. " tiles AND the nearest 2c bear: " .. table.concat(ORDER, ", "))
    say("NCBear_GenStand()           stand up / stop (E bears and the nearest 2c test bear ncbear)")
    say("NCBear_GenStay() / (false)  hold the E bears still facing the camera / let them walk again")
    say("NCBear_GenRun()             E bears and the resting 2c bear run ~8 tiles across the screen (next call: back)")
    say("NCBear_GenClean()           remove ALL loaded living E bears (do this and save before removing the test helper; no E corpses either)")
    say("noise (running, shots) makes all three run off (no noise guard since F2)")
end

function NCBear_GenLive()
    if not isSP() then say("singleplayer only"); return end
    local p = player()
    if not p then return end
    local here = p:getCurrentSquare()
    if not here then say("player has no square"); return end
    -- Reihe quer ueber den Bildschirm (Bildschirm rechts = Welt +x/-y), STEP*2 Kacheln vor dir (Bildschirm unten = +x/+y):
    -- links der 2c-Baer, Mitte E braun, rechts E Fototon -- wie das Blatt KEVIN_gross_vergleich (2c | braun | Fototon)
    local c = STEP
    local a2c = spawnAt(here, c - STEP, c + STEP, "ncbear")
    local aBr = spawnAt(here, c, c, "ncbeargen")
    local aFo = spawnAt(here, c + STEP, c - STEP, "ncbeargenfoto")
    say("row in front of you (left to right): 2c " .. (a2c and "ok" or "MISSING") .. " | E brown " .. (aBr and "ok" or "MISSING")
        .. " | E photo tone " .. (aFo and "ok" or "MISSING"))
    say("they walk now and then by themselves like the 2c bear; NCBear_GenStay() holds the E bears, NCBear_GenAct(\"sit\") lets all three sit")
    say("SAVE WARNING: a saved E bear needs this test helper on load -- NCBear_GenClean() and save before removing it")
end

function NCBear_GenAct(name, sek)
    if not isSP() then say("singleplayer only"); return end
    if name == nil or not (name == "sit" or name == "eat" or PLAYS[name]) then
        say("use NCBear_GenAct(name, sek), names: " .. table.concat(ORDER, ", ") .. " (sek only for sit and eat)")
        return
    end
    local p = player()
    if not p then return end
    if name == "sit" then sek = clampSec(sek, SIT_DEFAULT) elseif name == "eat" then sek = clampSec(sek, EAT_DEFAULT) end
    hook()
    local gens = genNear(p)
    local n, why = 0, nil
    for _, a in ipairs(gens) do
        local G = entryOf(a, true)
        if G then
            local ok, w = startAct(G, name, sek)
            if ok then n = n + 1 end
            why = w
        end
    end
    say(countLine(n, #gens, why))
    -- 2c-Baer ueber den Clip-Spieler der Testhilfe, genau wie NCBear_Sit / NCBear_Eat / NCBear_AnimTest (client/NCBearBench.lua)
    local a2, miss = twoC(p)
    if not a2 then say("2c: " .. miss); return end
    local C = NCBearBenchClip
    local turn = not C.Busy(a2)
    local ok, w
    if name == "sit" then
        ok, w = C.Sit(a2, sek)
    elseif name == "eat" then
        ok, w = C.Eat(a2, sek)
    else
        turn = true
        ok, w = C.Play(a2, name)
    end
    if ok and turn then a2:setDir(IsoDirections.SE) end
    say("2c: " .. (ok and "bear " or "bear refuses: ") .. tostring(w))
end

function NCBear_GenStand()
    if not isSP() then say("singleplayer only"); return end
    local p = player()
    if not p then return end
    local gens = genNear(p)
    local n = 0
    for _, a in ipairs(gens) do
        local G = entryOf(a, false)
        if G and G.sub then
            if G.sub == "sitdown" then
                G.standNow = true          -- erst zu Ende hinsetzen (StandUp beginnt in der Sitzpose), dann sofort aufstehen
            elseif G.sub == "sit" then
                setAct(G, "standup")
            elseif G.sub ~= "standup" then
                endAct(G)
            end
            n = n + 1
        end
    end
    say(countLine(n, #gens, "stand up / stop"))
    local a2, miss = twoC(p)
    if not a2 then say("2c: " .. miss); return end
    local ok, w = NCBearBenchClip.Stand(a2)
    say("2c: " .. (ok and "bear " or "bear refuses: ") .. tostring(w))
end

function NCBear_GenStay(on)
    if not isSP() then say("singleplayer only"); return end
    local want = not (on == false or on == 0 or on == "off")
    local p = player()
    if not p then return end
    if want then hook() end
    local gens = genNear(p)
    local n = 0
    for _, a in ipairs(gens) do
        local G = entryOf(a, want)
        if G then
            G.stay = want
            if want then
                if not G.blocked then block(G, true) end
                if not G.sub then a:setDir(IsoDirections.SE) end
            elseif not G.sub and G.blocked then
                block(G, false)
            end
            n = n + 1
        end
    end
    say(countLine(n, #gens, want and "hold still (the hold is renewed every ~80 s)" or "walk freely again"))
end

function NCBear_GenRun()
    if not isSP() then say("singleplayer only"); return end
    local p = player()
    if not p then return end
    -- quer ueber den Bildschirm: rechts = Welt +x/-y; jeder Aufruf wechselt die Richtung
    local dx, dy = RUN * S.runSign, -RUN * S.runSign
    S.runSign = -S.runSign
    local function target(a)
        local sq = a:getSquare()
        if not sq then return nil end
        local t = getCell():getGridSquare(sq:getX() + dx, sq:getY() + dy, sq:getZ())
        if not t or isWater(t) then return nil end
        return t
    end
    local gens = genNear(p)
    local n, busy, nosq = 0, 0, 0
    for _, a in ipairs(gens) do
        local G = entryOf(a, false)
        if G and G.sub then
            busy = busy + 1
        else
            local t = target(a)
            if not t then
                nosq = nosq + 1
            else
                if G then
                    G.stay = false
                    if G.blocked then block(G, false) end
                end
                a:fleeTo(t)
                n = n + 1
            end
        end
    end
    local why = "run " .. ((dx > 0) and "right" or "left")
    if busy > 0 then why = why .. ", " .. busy .. " busy (NCBear_GenStand() first)" end
    if nosq > 0 then why = why .. ", " .. nosq .. " without a free target square" end
    say(countLine(n, #gens, why))
    -- 2c-Baer nur, wenn der Clip-Spieler ihn gerade nicht fuehrt (sonst haelt ihn dessen Sperre fest)
    local a2, miss = twoC(p)
    if not a2 then say("2c: " .. miss); return end
    if NCBearBenchClip.Busy(a2) then
        say("2c: busy (plays a clip), not sent -- NCBear_GenStand() first")
        return
    end
    local t = target(a2)
    if not t then say("2c: no free target square"); return end
    a2:fleeTo(t)
    say("2c: run " .. ((dx > 0) and "right" or "left"))
end

function NCBear_GenClean()
    if not isSP() then say("singleplayer only"); return end
    local list = getCell():getObjectListForLua()
    local n = 0
    for i = list:size(), 1, -1 do
        local a = list:get(i - 1)
        if instanceof(a, "IsoAnimal") and GEN[a:getAnimalType()] then
            a:remove()
            n = n + 1
        end
    end
    S.list = {}
    say("removed " .. n .. " living E bear(s); E bears further away (not loaded) and E bear corpses stay -- the 2c test bear stays")
end
