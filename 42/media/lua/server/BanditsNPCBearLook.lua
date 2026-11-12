if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Aussehen-Knopf beim Schreiber (Lauf baer-aussehen, PLAN_AUSSEHEN.md 0, 3, 5, 7, 14).
--
-- Kevin 12.11.2026: "koennte man auch ingame einen knopf einbauen wo man das baeren model weckselt? also von einen getamed baeren?" --
-- "ja fuer spieler als knopf" -- "koennte man das model weckseln abused? z.b als unstuck funktion oder so? wird er dabei geheilt etc?".
-- Echte Spielmechanik (kein Probebefehl): der Knopf "Look" im Baerenfenster bittet B.Ask(player, "Look", { id, look }); getauscht wird
-- NUR hier beim Schreiber (Einzelspieler: dasselbe Programm; Mehrspieler: der Server), der Client setzt nie etwas selbst.
-- Jedes Aussehen ist eine eigene Tierart mit ENDGUELTIGEM Namen (B.LOOKS, shared/BanditsNPCBear.lua; Definitionen in
-- shared/BanditsNPCBearDefs.lua). Der Tausch ist derselbe Koerper-Tausch wie beim Wachsen: B.BodySwap (server/BanditsNPCBearGrow.lua) ->
-- B.PlaceCub (server/BanditsNPCBearRide.lua) -> B.CreateCub (server/BanditsNPCBearWorld.lua): erst der neue Koerper (gen + 1, Spiegel,
-- Groesse und Leben sofort), DANN der alte weg. Eintrag, Name, Zaehmung, Werte, Erfahrung, Modus, Leben (rec.hp), Ausdauer (s.sta), am
-- Boden, Verband bleiben.
--
-- Gegen Missbrauch (PLAN_AUSSEHEN.md 7, fest): kein Heilen (Leben/Ausdauer bleiben, siehe oben); getauscht wird nur, wenn B.BodySwapReady
-- ja sagt (kein Zombie / feindlicher Bandit naeher als zedSafe 9, nicht beim Fuettern/Streicheln/Verband/Aufhelfen, nicht im Kampf, nicht
-- am Boden) und kein Kampf-Nachlauf (B.FightState); die neue Kachel ist die eigene oder Ring 1-2 UM DAS TIER (B.SwapSpot, nie zum Spieler,
-- kein Wegzaubern); nur ein geladener Koerper; die Abklingzeit ist DIESELBE Uhr wie Unstuck ("Call to me", B.CallLeft lesen hier; starten
-- tut B.BodySwap mit look ueber B.CallStamp direkt vor dem neuen Koerper -- Nachbesserung Aussehen B1 --, server/BanditsNPCBearRide.lua --
-- B._callAt bleibt dort). Ablehnungen sind sofort zu Ende (keine Warteschlange), ohne Abklingzeit.
--
-- Kein neuer Engine-Aufruf: player:getVehicle() (Vanilla server/Vehicles/VehicleCommands.lua:11, wie B.HandleCall),
-- getTimestampMs (Vanilla server/Foraging/forageServer.lua:456); alles andere ueber vorhandene Baeren-Funktionen.
-- Ladefolge: nach ...Hurt, vor ...Mend / ...Registry / ...Ride / ...Server / ...World (alphabetisch) -- fremde Funktionen nur zur Laufzeit.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- ---------------------------------------------------------------------------
-- Aussehen JETZT (PLAN_AUSSEHEN.md 3): Familie des gebundenen Koerpers (B.LookKind des Tiers der Sitzung), sonst die des Wunsches fuer den
-- Koerper, den der Eintrag hat (B.LookFor(B.BodyNow(rec), rec.look)). Rueckgabe "std" / "gen" / "foto" (nie nil).
-- ---------------------------------------------------------------------------
function B.LookNow(rec)
    if type(rec) ~= "table" then return "std" end
    local s = B._s and B._s[rec.id] or nil
    local o = s and s.obj or nil
    if o ~= nil and B.LookKind then
        local lk = B.LookKind(o)
        if lk ~= nil then return lk end
    end
    local body = rec.body
    if B.BodyNow then
        local b0 = B.BodyNow(rec)
        body = b0
    end
    if B.LookFor == nil then return "std" end
    return B.LookFor(body, rec.look).k
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_AUSSEHEN.md 3; aus viewEntry, server/BanditsNPCBearRegistry.lua, nur tame/missing): lk = Familie des JETZIGEN Koerpers (fehlt =
-- "std", damit ein Eintrag ohne Aussehen genau die bisherige Sicht hat), lkg = true, wenn ein Wachs-Tausch wartet (Knopf grau). Schreibt
-- nur in t.
-- ---------------------------------------------------------------------------
function B.LookView(rec, t)
    if type(rec) ~= "table" or type(t) ~= "table" then return end
    if rec.st ~= "tame" and rec.st ~= "missing" then return end
    local lk = B.LookNow(rec)
    if lk ~= "std" then t.lk = lk end
    if rec.st == "tame" and (rec.body == "cub" or rec.body == "big") and B.BodyWant and B.BodyWant(rec) ~= rec.body then
        t.lkg = true
    end
end

-- ---------------------------------------------------------------------------
-- Bitte "Look" { id = <Text>, look = <Familie> } (PLAN_AUSSEHEN.md 5.2). Reihenfolge wie B.HandleCall (server/BanditsNPCBearRide.lua).
-- Ablehnung ueber refuse: Drossel je "Spieler|Look|no" (B.AskOk, server/BanditsNPCBearFollow.lua), dann Meldung und frische Sicht.
-- "still" = ohne Meldung und ohne Abklingzeit (unsinnige Bitte, eben erzeugter Koerper, schon dieses Aussehen, Drossel).
-- ---------------------------------------------------------------------------
local function refuse(player, pkey, ms, n)
    if B.AskOk(pkey .. "|Look|no", ms) then
        B.Tell(player, n)
        B.PushView(player)
    end
end

-- Grund aus B.BodySwapReady -> Meldung (PLAN_AUSSEHEN.md 5.2 Nr. 16)
local READY_WHY = {
    guard = "UI_BN_Bear_Why_LookDanger",
    busy = "UI_BN_Bear_Why_LookBusy", calm = "UI_BN_Bear_Why_LookBusy", cool = "UI_BN_Bear_Why_LookBusy",
    retry = "UI_BN_Bear_Why_LookBusy", move = "UI_BN_Bear_Why_LookBusy",
    fight = "UI_BN_Bear_Why_LookFight",
    down = "UI_BN_Bear_Why_Down",
    ride = "UI_BN_Bear_Why_Riding",
    nodef = "UI_BN_Bear_Why_LookMissing",
    state = "UI_BN_Bear_Why_NotOwner",
}

function B.HandleLook(player, args)
    if not player or not B.IsWriter() then return end
    local reg = B.Reg()
    if not reg then return end
    if type(args) ~= "table" or type(args.id) ~= "string" then return end
    local want = args.look
    local keys = B.LOOK_KEYS
    if type(want) ~= "string" or type(keys) ~= "table" or keys[want] ~= true then return end
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
    if rec.st == "missing" then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_OutOfReach", nil, nil, "bad"), rec))
        return
    end
    if rec.ride ~= nil then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_Riding", nil, nil, "bad"), rec))
        return
    end
    if player:getVehicle() ~= nil then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_InCar", nil, nil, "bad"))
        return
    end
    if rec.down ~= nil then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_Down", nil, nil, "bad"), rec))
        return
    end
    -- GEMEINSAME Uhr mit Unstuck (Kevin: "abused? z.b als unstuck funktion")
    local left = B.CallLeft(rec, ms)
    if left > 0 then
        local mins = math.ceil(left / 60000 - 0.000001)
        if mins < 1 then mins = 1 end
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_LookWait", "num", mins, "bad"), rec))
        return
    end
    -- Ein eben erzeugter Koerper (Tausch, Aussteigen, Call) haengt erst im naechsten Bild in der Welt (wie B.HandleCall, Nachbesserung
    -- B1e B1): bis dahin nichts tun (still) -- sonst bliebe er als ungebundene Kopie neben dem neuen stehen.
    local s0 = B._s[rec.id]
    local placed = s0 and tonumber(s0.placedAt) or nil
    if placed ~= nil and s0.obj ~= nil and ms - placed >= 0 and ms - placed < (tonumber(B.CFG.callFreshMs) or 2000)
        and B.FindAnimal(rec) == nil then
        B.Log("look: " .. tostring(rec.id) .. " got its body " .. tostring(ms - placed) .. " ms ago, not in the world yet -- nothing done")
        return
    end
    local a = B.FindAnimal(rec)
    if a == nil then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_OutOfReach", nil, nil, "bad"), rec))
        return
    end
    local have, cur = B.BodyKind(a)
    if have == nil then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_OutOfReach", nil, nil, "bad"), rec))
        return
    end
    if want == cur then return end
    local entry = B.LookEntry(have, want)
    if entry == nil or entry.hide == true then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_LookMissing", nil, nil, "bad"))
        return
    end
    if B.BodyWant(rec) ~= have then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_LookGrow", nil, nil, "bad"), rec))
        return
    end
    if not B.CubDefOk(have, want) then
        refuse(player, pkey, ms, note("UI_BN_Bear_Why_LookMissing", nil, nil, "bad"))
        return
    end
    -- Kampf-Nachlauf (retreat / rest) hat kein s.fight mehr -- B.BodySwapReady saehe ihn nicht (server/BanditsNPCBearFight.lua)
    if B.FightState and B.FightState(rec) ~= nil then
        refuse(player, pkey, ms, B.NoteBd(note("UI_BN_Bear_Why_LookFight", nil, nil, "bad"), rec))
        return
    end
    local s = B.Ses(rec.id)
    local ok, why = B.BodySwapReady(rec, s, ms, have, want)
    if not ok then
        local k = READY_WHY[why] or "UI_BN_Bear_Why_LookBusy"
        if k == "UI_BN_Bear_Why_NotOwner" or k == "UI_BN_Bear_Why_LookMissing" then
            refuse(player, pkey, ms, note(k, nil, nil, "bad"))
        else
            refuse(player, pkey, ms, B.NoteBd(note(k, nil, nil, "bad"), rec))
        end
        return
    end
    if not B.AskOk(pkey .. "|Look|ok", ms) then return end
    local from = cur
    -- Die gemeinsame Uhr startet IN B.BodySwap direkt vor dem neuen Koerper (Nachbesserung Aussehen B1, server/BanditsNPCBearGrow.lua):
    -- bricht ein Engine-Aufruf mitten im Tausch ab, laeuft sie schon -- kein weiterer Koerper je Klick.
    local n, nwhy = B.BodySwap(rec, a, have, ms, want)
    if n == nil then
        -- Nichts geaendert (B.BodySwap: erst der neue Koerper, dann der alte weg), KEINE Abklingzeit (B.BodySwap nahm den Stempel zurueck)
        if nwhy == "nospot" then
            B.Tell(player, B.NoteBd(note("UI_BN_Bear_Why_LookNoRoom", nil, nil, "bad"), rec))
        else
            B.Err("look: no new body for " .. tostring(rec.id) .. " (" .. tostring(nwhy) .. "), nothing changed")
            B.Tell(player, note("UI_BN_Bear_Why_LookMissing", nil, nil, "bad"))
        end
        B.PushView(player)
        return
    end
    B.Tell(player, B.NoteBd(note("UI_BN_Bear_Note_Look", nil, nil, "good"), rec))
    B.Log("look: " .. tostring(rec.id) .. " " .. tostring(have) .. " " .. tostring(from) .. " -> " .. tostring(want) .. " for "
        .. tostring(pkey))
    B.FlushViews()
end
