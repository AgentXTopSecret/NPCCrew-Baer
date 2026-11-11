if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Mitfahren und "Call to me" (B1c, PLAN_B1C.md 0.2, 0.3, 1.4, 1.5, 3).
--
-- Mitfahren wie NPC Crews Figuren (gelernt, nicht kopiert: NPC Crew client/BanditsNPCPersistence.lua P.BeginRide ~7948 ff.,
-- forschung_b1c.md 4.1): das Tier faehrt NIE wirklich mit. Steigt der Besitzer ein und folgt das gezaehmte Junge (hoechstens
-- BearRideDistance weg), wird sein Koerper entfernt (B.RemoveCub) und der Eintrag steht "ride" -- alles Wichtige bleibt im Register.
-- Steigt der Besitzer aus, entsteht neben ihm ein neuer Koerper (B.PlaceCub -> B.CreateCub, der bestehende, belegte Weg) mit
-- gleichem Eintrag (Name, Zaehmung, Modus follow). "Call to me" (Unstuck) holt ein gezaehmtes Junges auf demselben Weg neben den
-- Besitzer. Jedes Neu-Erzeugen und jedes Einsteigen zaehlt die Koerper-Generation rec.gen hoch; ein Koerper mit kleinerer gen ist
-- eine veraltete Kopie und wird nie gebunden (server/BanditsNPCBearHeal.lua) -- so gibt es nach Absturz oder Herholen kein Doppel.
-- Kein Teleport (setX/setY am Tier: kein Beleg), kein Vanilla-Tier-Anhaenger (nur Fahrzeuge mit Anhaenger).
-- Im Mehrspieler erzeugt und entfernt nur der Server; Clients bekommen das Tier ueber das Netz. Bitte "Call" pruefen Besitz und
-- Abklingzeit beim Schreiber (B.HandleCall); kein Kick (nur sendClientCommand mit LoginOnServer).
--
-- Engine-Aufrufe hier: player:getVehicle() (Vanilla server/Vehicles/VehicleCommands.lua:11), getX/getY am Spieler (Bandits
-- server/BanditServerSpawner.lua:179, getZ :191), square:getX()/getY()/getZ() (Vanilla client/DebugUIs/DebugContextMenu.lua:636),
-- animal:getAnimalID() (client/ISUI/Animal/ISAnimalUI.lua:53; am Server A3, offen), getTimestampMs (server/Foraging/forageServer.lua:456).
-- Ladefolge: nach ...Follow / ...Guard / ...Heal / ...Registry, vor ...Server / ...World -- fremde Funktionen nur zur Laufzeit.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._callAt = B._callAt or {}         -- [id] = Echtzeit des letzten erfolgreichen "Call to me" (nie gespeichert, Deckel 64)

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Naechster anwesender Spieler mit dem Schluessel des Besitzers (Eintrag aus B.Players()).
local function ownerEntry(rec, players)
    if rec.owner == nil then return nil end
    local best, bestD = nil, nil
    for i = 1, #players do
        local e = players[i]
        if e.key == rec.owner then
            local d = B.DistXY(rec.x, rec.y, e.x, e.y)
            if bestD == nil or d < bestD then best, bestD = e, d end
        end
    end
    return best
end

local function tellOwner(rec, players, n)
    local e = ownerEntry(rec, players or B.Players())
    if e and e.p then B.Tell(e.p, n) end
end

-- Sitzung leeren, die zu einem Koerper gehoert (Folgen, Gegenprobe, Halt, Zombie-Wache, Laerm-Uhren).
local function clearBodySession(s)
    s.f, s.chk, s.held, s.g = nil, nil, nil, nil
    s.calmUntil, s.ownUntil, s.walk = nil, nil, nil
    s.tx, s.ty, s.td0 = nil, nil, nil                 -- Nachbesserung B1c B5 (Ziel des eigenen Befehls)
end

-- ---------------------------------------------------------------------------
-- Neuer Koerper fuer einen bestehenden Eintrag (PLAN_B1C.md 3.5). Neben B.AppearFor der einzige Aufrufer von B.CreateCub
-- (server/BanditsNPCBearWorld.lua; addAnimal + addToWorld, Vanilla server/ClientCommands.lua:809-810). Die Kachel hat der Aufrufer
-- mit B.SpotNear geprueft. Spiegel SOFORT (isExistInTheWorld ist im selben Bild noch falsch, Fix 1). Rueckgabe: IsoAnimal oder nil, why.
-- Im selben Takt findet B.FindAnimal das neue Tier noch nicht (nicht in der Welt): ein harmloser Fehlversuch (3 noetig), der
-- naechste Takt bindet ueber das Objekt der Sitzung.
-- ---------------------------------------------------------------------------
function B.PlaceCub(rec, x, y, z, why)
    if type(rec) ~= "table" or x == nil or y == nil then return nil, "noargs" end
    local a, cwhy = B.CreateCub(x, y, z or 0)
    if not a then return nil, cwhy end
    local s = B.Ses(rec.id)
    rec.gen = (tonumber(rec.gen) or 0) + 1
    rec.aid = a:getAnimalID()
    s.obj = a
    clearBodySession(s)
    rec.x, rec.y, rec.z = math.floor(x), math.floor(y), math.floor(z or 0)
    rec.missN = 0
    rec.missAt = nil
    if rec.st == "missing" then
        rec.st = "tame"
        rec.missH = 0
    end
    B.Commit(rec)                       -- r + 1 (der Spiegel folgt gleich, mit diesem r)
    B.WriteMark(rec, a)
    -- B1d (PLAN_B1D.md 3.1): Groesse und Leben SOFORT aus dem Register an den neuen Koerper (server/BanditsNPCBearGrow.lua)
    if B.GrowBody then B.GrowBody(rec, a) end
    if B.CalmDrop then B.CalmDrop(rec.id) end
    if B._zed then B._zed[rec.id] = nil end
    B.Log("place " .. tostring(rec.id) .. " (" .. tostring(why) .. ") at " .. tostring(rec.x) .. "," .. tostring(rec.y)
        .. " gen " .. tostring(rec.gen))
    return a, nil
end

-- ---------------------------------------------------------------------------
-- Einsteigen (PLAN_B1C.md 3.1). Aus B.FollowStep (Regel 11 "ride"). o = env.owner { key, x, y, z, dist, car }.
-- Rueckgabe false -> der Aufrufer setzt "stay" "car" (Definition fehlt: es kaeme beim Aussteigen kein Koerper zurueck).
-- Erst die Sitzung loesen (B.Commit schreibt dann keinen Spiegel an den Koerper, der gleich verschwindet), dann festschreiben,
-- dann entfernen (B.RemoveCub: setBlockMovement(false), remove(), am Server removeAnimal(getOnlineID()) -- Belege dort).
-- ---------------------------------------------------------------------------
function B.RideBoard(rec, a, o, players)
    if type(rec) ~= "table" or not a or rec.st ~= "tame" or rec.owner == nil then return false end
    if not B.CubDefOk() then
        B.ErrEvery("ridedef", 600000, "ride: animal definition " .. tostring(B.CUB) .. " is not loaded, "
            .. tostring(rec.id) .. " waits instead of getting in")
        return false
    end
    local s = B.Ses(rec.id)
    s.obj = nil
    clearBodySession(s)
    s.ride = { offMs = nil, lostMs = nil, failN = 0 }
    rec.ride = { at = B.Now() }
    rec.gen = (tonumber(rec.gen) or 0) + 1
    if o ~= nil and tonumber(o.x) ~= nil and tonumber(o.y) ~= nil then
        rec.x, rec.y, rec.z = math.floor(o.x), math.floor(o.y), math.floor(tonumber(o.z) or 0)
    end
    B.Commit(rec)
    B.RemoveCub(a)
    if B.CalmDrop then B.CalmDrop(rec.id) end
    if B._zed then B._zed[rec.id] = nil end
    tellOwner(rec, players, note("UI_BN_Bear_Note_RideOn", nil, nil, "good"))
    B.Log("ride: " .. tostring(rec.id) .. " gets in with " .. tostring(rec.owner) .. " (gen " .. tostring(rec.gen) .. ")")
    return true
end

-- Tempo eines Spielers seit dem letzten Hirn-Takt (Kacheln/s) aus B._pp / B._ppAt (server/BanditsNPCBearServer.lua). nil = unbekannt.
local function speedOf(e, ms)
    local pp = B._pp
    local last = pp and pp[e.uid]
    local at = tonumber(B._ppAt)
    if last == nil or at == nil then return nil end
    local dt = ms - at
    if dt <= 0 then return nil end
    return B.DistXY(last.x, last.y, e.x, e.y) / (dt / 1000)
end

local function placeFail(rec, r, what)
    r.failN = (tonumber(r.failN) or 0) + 1
    if r.failN >= (tonumber(B.CFG.rideFailLog) or 20) then
        B.ErrEvery("ride:" .. tostring(rec.id), 60000, "ride: " .. tostring(rec.id) .. " could not get out (" .. tostring(what)
            .. ", " .. tostring(r.failN) .. " tries), it stays with its owner")
    end
end

-- ---------------------------------------------------------------------------
-- Je Hirn-Takt fuer jeden Eintrag mit rec.ride (PLAN_B1C.md 3.4), vor resolve. ms = Echtzeit.
-- 1 Besitzer fehlt: tot (B.DeadAt) seit rideLostMs und Gegend geladen -> neben der Leiche aussteigen und dort warten ("stay");
--   sonst warten (abgemeldet, Server-Neustart, Gegend entladen: die neue Figur bekommt es beim ersten Schritt zu Fuss).
-- 2 letzte bekannte Stelle = Kachel des Besitzers (ohne B.Touch: kein Karten-Symbol fuer Mitfahrende).
-- 3 im Fahrzeug -> weiter. 4 zu Fuss seit rideOffMsSP (SP) / rideOffMsMP (MP; getVehicle liefert dort waehrend der Fahrt
--   sekundenlang nil, NC-Lehre) und im MP langsamer als rideSpeedMax. 5 freie Kachel (B.SpotNear) -> 6 B.PlaceCub, "follow".
-- ---------------------------------------------------------------------------
function B.RideStep(rec, players, ms)
    if type(rec) ~= "table" or rec.ride == nil then return end
    local cfg = B.CFG
    local s = B.Ses(rec.id)
    local r = s.ride
    if type(r) ~= "table" then
        r = { offMs = nil, lostMs = nil, failN = 0 }
        s.ride = r
    end
    players = players or B.Players()
    local e = ownerEntry(rec, players)
    if e == nil then
        r.offMs = nil
        if r.lostMs == nil or ms - r.lostMs < 0 then r.lostMs = ms end
        local x, y, z = B.DeadAt(rec.owner)
        if x ~= nil and ms - r.lostMs >= cfg.rideLostMs and B.AreaLoaded(x, y) then
            local sq = B.SpotNear(x, y, z, cfg.rideRing, rec.gen)
            if sq == nil then
                placeFail(rec, r, "no free spot at the owner's body")
                return
            end
            local a, why = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "dead")
            if not a then
                placeFail(rec, r, why)
                return
            end
            rec.ride = nil
            s.ride = nil
            B.SetMode(rec, "stay", "dead", players)
            B.Log("ride: " .. tostring(rec.id) .. " got out where its owner died and waits there")
        end
        return
    end
    r.lostMs = nil
    rec.x, rec.y, rec.z = math.floor(e.x), math.floor(e.y), math.floor(tonumber(e.z) or 0)
    if e.car == true then
        r.offMs = nil
        return
    end
    if r.offMs == nil or ms - r.offMs < 0 then
        r.offMs = ms
        return
    end
    local need = cfg.rideOffMsSP
    if isServer() then need = cfg.rideOffMsMP end
    if ms - r.offMs < need then return end
    if isServer() then
        local v = speedOf(e, ms)
        if v ~= nil and v > cfg.rideSpeedMax then return end
    end
    local sq = B.SpotNear(e.x, e.y, e.z, cfg.rideRing, rec.gen)
    if sq == nil then
        placeFail(rec, r, "no free spot next to the owner")
        return
    end
    local a, why = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "ride")
    if not a then
        placeFail(rec, r, why)
        return
    end
    rec.ride = nil
    s.ride = nil
    B.SetMode(rec, "follow", "ride", players)
    if e.p then B.Tell(e.p, note("UI_BN_Bear_Note_RideOff", nil, nil, "good")) end
    B.Log("ride: " .. tostring(rec.id) .. " got out next to " .. tostring(rec.owner))
end

-- ---------------------------------------------------------------------------
-- "Call to me" (PLAN_B1C.md 1.5). Abklingzeit in Echtzeit je Junges (Sandbox BearCallCooldownMinutes, Vorgabe 5; 0 = keine).
-- Rueckgabe: Rest in ms (0 = bereit). Uhr rueckwaerts = abgelaufen. Speichern/Laden setzt sie zurueck (Sitzung, ehrlich).
-- ---------------------------------------------------------------------------
function B.CallLeft(rec, ms)
    if type(rec) ~= "table" or rec.id == nil then return 0 end
    local at = tonumber(B._callAt[rec.id])
    if at == nil then return 0 end
    ms = tonumber(ms) or getTimestampMs()
    if ms - at < 0 then return 0 end
    local mins = B.Opt("BearCallCooldownMinutes")
    if mins <= 0 then return 0 end
    local left = at + mins * 60000 - ms
    if left <= 0 then return 0 end
    return left
end

-- Abklingzeit merken (Deckel 64: zuerst abgelaufene raus, sonst alles leeren).
local function callMark(rec, ms)
    local t = B._callAt
    if t[rec.id] == nil then
        local n = 0
        for _, _ in pairs(t) do n = n + 1 end
        if n >= 64 then
            local keep = {}
            for id, at in pairs(t) do
                local left = B.CallLeft({ id = id }, ms)
                if left > 0 then keep[id] = at end
            end
            B._callAt = keep
            t = keep
            n = 0
            for _, _ in pairs(t) do n = n + 1 end
            if n >= 64 then
                t = {}
                B._callAt = t
            end
        end
    end
    t[rec.id] = ms
end

-- Drossel wie die Bitten "Mode"/"Rename" (server/BanditsNPCBearFollow.lua B.AskOk): Wirkung je "Spieler|Call|ok/no".
local function allow(pkey, outcome, ms)
    return B.AskOk(pkey .. "|Call|" .. outcome, ms)
end

local function refuse(player, pkey, ms, n)
    if allow(pkey, "no", ms) then
        B.Tell(player, n)
        B.PushView(player)
    end
end

-- Bitte "Call" { id }. Reihenfolge der Pruefungen: Eintrag (Why_Gone), Besitzer und st tame/missing (Why_NotOwner), nicht
-- mitfahrend (Why_Riding), Spieler nicht im Fahrzeug (Why_InCar), Abklingzeit (Why_CallWait, Minuten aufgerundet, mindestens 1),
-- freie Kachel 1..callRing neben dem Spieler (Why_NoRoom). Erfolg: neuer Koerper neben ihm (gen + 1), DANN das alte Tier weg (falls
-- geladen; ein nicht geladenes taucht spaeter als veraltete Kopie auf und wird entfernt), "follow", Note_Called, Abklingzeit startet.
-- Kein Text als Kennung -> still verworfen (wie Mode/Rename).
function B.HandleCall(player, args)
    if not player or not B.IsWriter() then return end
    local reg = B.Reg()
    if not reg then return end
    if type(args) ~= "table" or type(args.id) ~= "string" then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    local ms = getTimestampMs()
    local rec = reg.cubs[args.id]
    if rec == nil then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    if rec.owner ~= pkey or (rec.st ~= "tame" and rec.st ~= "missing") then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return
    end
    if rec.ride ~= nil then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_Riding", nil, nil, "bad"))
        return
    end
    if player:getVehicle() ~= nil then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_InCar", nil, nil, "bad"))
        return
    end
    local left = B.CallLeft(rec, ms)
    if left > 0 then
        local mins = math.ceil(left / 60000 - 0.000001)
        if mins < 1 then mins = 1 end
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_CallWait", "num", mins, "bad"))
        return
    end
    local sq = B.SpotNear(player:getX(), player:getY(), player:getZ(), B.CFG.callRing, rec.gen)
    if sq == nil then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_NoRoom", nil, nil, "bad"))
        return
    end
    if not allow(pkey, "ok", ms) then return end
    local old = B.FindAnimal(rec)
    -- Nachbesserung B1c B9: ist der alte Koerper geladen, aber noch nicht gebunden (Sekunden nach dem Laden, bis zum naechsten
    -- Suchlauf), bliebe er sonst als zweites Junges ohne Schild stehen: erst EIN Suchlauf (bindet ihn), dann wie immer entfernen.
    -- Hoechstens je scanMs (B._callScanAt), damit auch Abklingzeit 0 keine Suchlauf-Flut macht. Ein Argument (ohne force).
    if old == nil and B.AreaLoaded(rec.x, rec.y) then
        local at = tonumber(B._callScanAt)
        if at == nil or ms - at < 0 or ms - at >= B.CFG.scanMs then
            B._callScanAt = ms
            B.ScanAnimals(nil)
            old = B.FindAnimal(rec)
        end
    end
    local a, why = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "call")
    if not a then
        B.Err("call: no new body for " .. tostring(rec.id) .. " (" .. tostring(why) .. "), nothing changed")
        B.Tell(player, note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        B.PushView(player)
        return
    end
    if old ~= nil and old ~= a then B.RemoveCub(old) end
    B.SetMode(rec, "follow", "call", nil)
    callMark(rec, ms)
    B.Tell(player, note("UI_BN_Bear_Note_Called", nil, nil, "good"))
    B.Log("call: " .. tostring(rec.id) .. " brought next to " .. tostring(pkey))
    B.FlushViews()
end
