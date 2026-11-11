if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Folgen / Bleiben und Umbenennen (B1b, PLAN_B1B.md 1, 3.3, 5.3).
--
-- Folgen rechnet NUR der Schreiber im Hirn-Takt (Einzelspieler: das eine Programm; Mehrspieler: der Server). Kein Client
-- befiehlt dem Tier etwas: ein Client bittet nur ("Mode", "Rename"), der Schreiber prueft Besitz und Zustand im Register.
-- Bewegung nur ueber B.MoveTo (animal:fleeTo = rennen; B1c: auf kurze Strecke zu einem stehenden Besitzer gehen, opt.walk) und
-- B.Hold (setBlockMovement) aus server/BanditsNPCBearWorld.lua; B1c: Einsteigen ueber B.RideBoard (server/BanditsNPCBearRide.lua);
-- eigene Engine-Aufrufe hier nur player:getVehicle, getX/getY und getTimestampMs (Fundstelle je am Aufruf), sonst Register und Regeln.
-- Der Name lebt nur im Register (Plan 0.3): kein Vanilla-Tiername am Tier.
--
-- Ladefolge: diese Datei laedt VOR ...Registry / ...Server / ...World (alphabetisch). Deshalb wird auf Dateiebene nichts
-- eingefangen; jede fremde Funktion wird zur Laufzeit ueber B.X geholt.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._askAt = B._askAt or {}           -- ["Spieler|Befehl|ok/no"] = Echtzeit der letzten Wirkung einer Bitte "Mode"/"Rename" (B.AskOk)

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Naechster anwesender Spieler mit dem Schluessel des Besitzers (Einzelspieler mit geteiltem Bildschirm: der naechste lokale).
-- Rueckgabe: Spieler, Eintrag aus B.Players() oder nil, nil.
local function ownerNear(rec, players)
    if rec.owner == nil then return nil, nil end
    players = players or B.Players()
    local best, bestD = nil, nil
    for i = 1, #players do
        local e = players[i]
        if e.key == rec.owner then
            local d = B.DistXY(rec.x, rec.y, e.x, e.y)
            if bestD == nil or d < bestD then best, bestD = e, d end
        end
    end
    if best then return best.p, best end
    return nil, nil
end

-- ---------------------------------------------------------------------------
-- Drossel der Bitten (Plan 3.3): je Schluessel hoechstens eine Wirkung je B.CFG.askMs. Verworfene Bitten verschieben die Uhr
-- nicht. Deckel: mehr als 128 Schluessel -> Tabelle geleert.
-- Nachbesserung B1b B5: der Schluessel ist "Spieler|Befehl|Ausgang" (ok = angenommen, no = abgelehnt), und gezaehlt wird erst
-- NACH den Pruefungen (die sind billig: Register, Besitz, Abstand). Gedrosselt sind die Wirkungen (Zustand, Name, Meldung):
-- "Follow me" und gleich danach OK im Namensfenster gehen beide durch, und eine Ablehnung nimmt der naechsten angenommenen
-- Bitte nicht den Platz. Je Spieler hoechstens vier Schluessel (2 Befehle x 2 Ausgaenge).
-- ---------------------------------------------------------------------------
function B.AskOk(key, ms)
    if key == nil or ms == nil then return false end
    local t = B._askAt
    if type(t) ~= "table" then
        t = {}
        B._askAt = t
    end
    local last = t[key]
    if last ~= nil and ms - last >= 0 and ms - last < B.CFG.askMs then return false end
    if last == nil then
        local n = 0
        for _, _ in pairs(t) do n = n + 1 end
        if n >= 128 then
            t = {}
            B._askAt = t
        end
    end
    t[key] = ms
    return true
end

-- Wirkung einer Bitte jetzt erlaubt? getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
local function allow(pkey, command, outcome)
    return B.AskOk(pkey .. "|" .. command .. "|" .. outcome, getTimestampMs())
end

-- Ablehnung mit Meldung (gedrosselt ueber den Ausgang "no").
local function refuse(player, pkey, command, n)
    if allow(pkey, command, "no") then B.Tell(player, n) end
end

-- ---------------------------------------------------------------------------
-- Zustand setzen (Plan 5.3). mode = "follow" / "stay"; why = "ask" / "car" / "far" / "lost" / "offline" / "missing"; B1c auch
-- "call" / "ride" / "dead" (ohne Meldung: Ride.lua meldet selbst).
-- Bei "stay" wird die Heimat die Kachel, an der das Junge jetzt steht (Plan 1.4). Leert die Folgen-Sitzung B._s[id].f und die
-- alte Lauf-Gegenprobe (sonst meldete B.MoveWatch nach dem Wechsel einen Folgen-Befehl als "bewegt sich nicht").
-- Meldung an den Besitzer nach why; die Richtung ist die vom Besitzer zum Jungen. Rueckgabe: true, wenn gesetzt.
-- B1e (PLAN_B1E.md 6.4): die Meldungen tragen bd = "big", wenn der Eintrag den grossen Koerper hat (B.NoteBd).
-- ---------------------------------------------------------------------------
function B.SetMode(rec, mode, why, players)
    if type(rec) ~= "table" or (mode ~= "follow" and mode ~= "stay") then return false end
    rec.mode = mode
    if mode == "stay" then
        rec.hx, rec.hy, rec.hz = rec.x, rec.y, rec.z
    end
    local s = B.Ses(rec.id)
    s.f = nil
    s.chk = nil
    B.Commit(rec)
    local p, e = ownerNear(rec, players)
    if p then
        local n = nil
        if why == "ask" then
            if mode == "follow" then
                n = note("UI_BN_Bear_Note_Follow", nil, nil, "good")
            else
                n = note("UI_BN_Bear_Note_Stay", nil, nil, nil)
            end
        elseif why == "car" then
            n = note("UI_BN_Bear_Note_StayCar", nil, nil, "bad")
        elseif why == "far" then
            n = note("UI_BN_Bear_Note_StayFar", "dir", B.DirOf(rec.x - e.x, rec.y - e.y), "bad")
        elseif why == "lost" then
            n = note("UI_BN_Bear_Note_StayBehind", "dir", B.DirOf(rec.x - e.x, rec.y - e.y), "bad")
        end
        if n then B.Tell(p, B.NoteBd(n, rec)) end
    end
    B.Log("mode " .. tostring(rec.id) .. " " .. mode .. " (" .. tostring(why) .. ") at " .. tostring(rec.x) .. "," .. tostring(rec.y))
    return true
end

-- ---------------------------------------------------------------------------
-- Ein Hirn-Takt eines FOLGENDEN, geladenen, lebenden Jungen (Plan 1.2). Gerufen aus liveRec (server/BanditsNPCBearServer.lua)
-- statt B.Decide. env.owner = { key, x, y, z, dist, car, mx, my } oder nil (buildEnv). Ohne Gegenprobe B.MoveWatch (Plan 1.2).
-- Ist der Besitzer nicht da, haelt es und bleibt "follow" (Regel 10, Nachbesserung B1b A7).
-- B1e (PLAN_B1E.md 1.5, 6.3): c.gap = Zuschlag mit der Koerperlaenge (B.BodyGap, nur grosser Koerper) und c.walkSpeed = Tempo des
-- Koerpers (B.BodyNum) fuer B.FollowDecide; fehlt shared/BanditsNPCBearStats.lua: Junges, Zuschlag 0, Tempo aus B.CFG (wie B1c).
-- ---------------------------------------------------------------------------
function B.FollowStep(rec, a, env, ms, players)
    if type(rec) ~= "table" or not a then return end
    local s = B.Ses(rec.id)
    local f = s.f
    if type(f) ~= "table" then
        f = {}
        s.f = f
    end
    local body, sz = "cub", 0
    if B.BodyNow then body, sz = B.BodyNow(rec) end
    local gap, walkSpeed = 0, nil
    if B.BodyGap then gap = B.BodyGap(body, sz) end
    if B.BodyNum then walkSpeed = B.BodyNum(body, "walkSpeed", 0.52) end
    -- getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576
    local c = { x = a:getX(), y = a:getY(), z = rec.z, gap = gap, walkSpeed = walkSpeed }
    local wasStuck = f.stuck == true
    local d = B.FollowDecide(c, env and env.owner or nil, f, ms)
    if d.act == "ride" then
        -- B1c (PLAN_B1C.md 1.4, 6.3): Besitzer im Fahrzeug und nah genug -> einsteigen (Koerper verschwindet); geht das nicht
        -- (Definition fehlt), wie B1b "Bleiben" mit Meldung
        local board = B.RideBoard
        if not (board and board(rec, a, env and env.owner or nil, players)) then B.SetMode(rec, "stay", "car", players) end
        return
    elseif d.act == "stay" then
        B.SetMode(rec, "stay", d.why, players)
        return
    elseif d.act == "hold" then
        B.Hold(rec, a, true)
        f.held = true
    elseif d.act == "run" then
        -- B1c Gehen (1.6): d.walk -> B.MoveTo geht (setVariable + pathToLocation), sonst rennt es (fleeTo)
        local walk = d.walk == true
        local moved = B.MoveTo(rec, a, d.tx, d.ty, rec.z, { minMs = B.CFG.followMoveMs, watch = false, walk = walk })
        if moved then
            f.orderAt = ms
            f.tx, f.ty = d.tx, d.ty
            f.held = nil
            f.walk = walk
        end
    end
    if f.stuck == true and not wasStuck then
        B.Log("follow: " .. tostring(rec.id) .. " gets no closer to its owner (stuck?), one try every "
            .. tostring(B.CFG.followRetryMs) .. " ms now")
    elseif wasStuck and f.stuck ~= true then
        B.Log("follow: " .. tostring(rec.id) .. " moves on again")
    end
end

-- ---------------------------------------------------------------------------
-- Ein folgendes Junges ohne Objekt (Plan 1.3). Gerufen aus dem Hirn-Takt fuer jeden Eintrag ohne Objekt. Ist die Gegend seiner
-- letzten Kachel NICHT geladen, wartet es dort ("Bleiben", Heimat = letzte Kachel, Meldung mit Richtung). Ist die Gegend geladen,
-- gilt der B1a-Weg (Suchlauf, Fehlversuche, "missing").
-- Nur fuer ein Junges, das in DIESER Sitzung schon ein Objekt hatte (Nachbesserung B1b B3): nach dem Laden ist jedes Junge
-- "ohne Objekt", bis der Suchlauf es bindet -- das ist kein Zurueckbleiben. Und nur, wenn der Besitzer da ist (Nachbesserung B1b
-- A7): ist er abgemeldet, entlaedt seine Gegend mit ihm, und das Junge wartet als "follow" auf ihn.
-- ---------------------------------------------------------------------------
-- B1c: ein mitfahrendes Junges (rec.ride) hat absichtlich kein Objekt -- nie "zurueckgeblieben" (PLAN_B1C.md 3.3).
function B.FollowLost(rec, players)
    if type(rec) ~= "table" or rec.st ~= "tame" or B.ModeOf(rec) ~= "follow" then return end
    if rec.ride ~= nil then return end
    local s = B._s[rec.id]
    if s == nil or s.obj == nil then return end
    if ownerNear(rec, players) == nil then return end
    if B.FindAnimal(rec) ~= nil then return end
    if B.AreaLoaded(rec.x, rec.y) then return end
    B.SetMode(rec, "stay", "lost", players)
end

-- ---------------------------------------------------------------------------
-- Bitten (Plan 3.3). Gemeinsam: Schreiber, Register, Kennung als Text, Spielerschluessel. Eine Kennung, die kein Text ist (auch:
-- args leer oder nil), wird still verworfen (Plan 5.5); ein Text ohne Eintrag bekommt Why_Gone. Rueckgabe: pkey, rec (rec nil =
-- kein Eintrag) oder nil (still verwerfen). Die Drossel kommt erst nach den Pruefungen (allow / refuse, Nachbesserung B1b B5).
-- ---------------------------------------------------------------------------
local function askRec(player, args)
    if not player or not B.IsWriter() then return nil, nil end
    local reg = B.Reg()
    if not reg then return nil, nil end
    if type(args) ~= "table" or type(args.id) ~= "string" then return nil, nil end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return nil, nil end
    return pkey, reg.cubs[args.id]
end

-- "Mode" { id, mode }: nur der Besitzer, nur am gezaehmten, geladenen Jungen; "follow" nicht aus dem Fahrzeug und nicht weiter
-- als BearFollowMaxDistance. player:getVehicle(): Vanilla server/Vehicles/VehicleCommands.lua:11 (Spieler eines Client-Befehls).
-- getX/getY am Spieler: Bandits server/BanditServerSpawner.lua:179; am Tier: Vanilla ButcheringUtil.lua:575-576.
function B.HandleMode(player, args)
    local pkey, rec = askRec(player, args)
    if pkey == nil then return end
    local mode = args.mode
    if mode ~= "follow" and mode ~= "stay" then return end
    if rec == nil or rec.st == "missing" then
        refuse(player, pkey, "Mode", note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    if rec.st ~= "tame" or rec.owner ~= pkey then
        refuse(player, pkey, "Mode", note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return
    end
    if rec.ride ~= nil then
        -- B1c: es faehrt mit (kein Koerper); wie NPC Crews "parked" (forschung_b1c.md 4.1)
        refuse(player, pkey, "Mode", B.NoteBd(note("UI_BN_Bear_Why_Riding", nil, nil, "bad"), rec))
        return
    end
    local a = B.FindAnimal(rec)
    if a == nil then
        refuse(player, pkey, "Mode", note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    if mode == "follow" then
        if player:getVehicle() ~= nil then
            refuse(player, pkey, "Mode", note("UI_BN_Bear_Why_InCar", nil, nil, "bad"))
            return
        end
        if B.DistXY(player:getX(), player:getY(), a:getX(), a:getY()) > B.Opt("BearFollowMaxDistance") then
            refuse(player, pkey, "Mode", note("UI_BN_Bear_Why_Far", nil, nil, "bad"))
            return
        end
    end
    if not allow(pkey, "Mode", "ok") then return end
    B.SetMode(rec, mode, "ask", nil)
    B.FlushViews()
end

-- "Rename" { id, name }: nur der Besitzer (auch am vermissten Jungen). Vorab-Deckel 4 x nameMax Zeichen, bevor ein Zeichen
-- einzeln angesehen wird (B.CleanName prueft ihn auch selbst); dann B.CleanName (shared/BanditsNPCBearRules.lua).
function B.HandleRename(player, args)
    local pkey, rec = askRec(player, args)
    if pkey == nil then return end
    if rec == nil then
        refuse(player, pkey, "Rename", note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    local nameMax = tonumber(B.CFG.nameMax) or 24
    local name = args.name
    local bad = note("UI_BN_Bear_Why_NameBad", "num", nameMax, "bad")
    if type(name) ~= "string" or string.len(name) > 4 * nameMax then
        refuse(player, pkey, "Rename", bad)
        return
    end
    if rec.owner ~= pkey or (rec.st ~= "tame" and rec.st ~= "missing") then
        refuse(player, pkey, "Rename", note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return
    end
    local clean = B.CleanName(name)
    if clean == nil then
        refuse(player, pkey, "Rename", bad)
        return
    end
    if not allow(pkey, "Rename", "ok") then return end
    rec.name = clean
    B.Commit(rec)
    B.Tell(player, B.NoteBd(note("UI_BN_Bear_Note_Renamed", "name", clean, "good"), rec))
    B.Log("rename " .. tostring(rec.id) .. " by " .. tostring(pkey))
    B.FlushViews()
end
