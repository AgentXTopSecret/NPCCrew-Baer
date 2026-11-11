if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Register (B1a, PLAN_ZAEHMEN.md 4.1, 4.2, 6.2.3).
--
-- Die Wahrheit ueber jedes Junge steht NUR hier: globale ModData "TrueCompanionsBears" beim Schreiber. Sie wird nie
-- uebertragen (kein ModData.transmit, kein request): kein Client erfaehrt fremde Zeilen, kein Client kann sie ueberschreiben.
-- Am Tier liegt nur ein Spiegel { id, st } zum Wiederfinden; Besitz, Balken und Zeiten kommen nie aus dem Spiegel.
-- Plaetze je Spieler werden gezaehlt (B.SlotsOf), nie doppelt gefuehrt.
--
-- Deckel: hoechstens B.CFG.maxRecs Eintraege, B.CFG.maxBaits Koederplaetze (einer je Spieler), Spieler-Eintraege nur mit
-- laufender Sperre. Tier-Objekte werden nur fuer die Sitzung gemerkt (B._s) und bei jedem Gebrauch gegengeprueft.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local reg = nil                 -- gesetzt in OnInitGlobalModData; vorher wartet alles

B._s = B._s or {}               -- Sitzung je Eintrag: [id] = { obj, held, moveAt, curiousAt, chk, f }
                                -- f (B1b) = { held, orderAt, tx, ty, bestD, bestAt, stuck, retryAt }: Folgen, nie gespeichert
B._rev = B._rev or 0            -- zaehlt jede Aenderung, die eine Sicht betrifft
-- Wen betrifft das Geaenderte? Der Takt schickt danach nur diesen Spielern eine neue Sicht (B.FlushViews).
B._dirty = B._dirty or { any = true, all = true, keys = {}, spots = {}, n = 0 }

function B.Reg()
    return reg
end

-- Sitzungs-Zustand eines Eintrags (wird nie gespeichert).
function B.Ses(id)
    local s = B._s[id]
    if s == nil then
        s = {}
        B._s[id] = s
    end
    return s
end

-- "Geaendert" merken: ohne Angabe fuer alle, sonst fuer die Spieler eines Eintrags (finder, bond, owner), fuer alle in
-- Reichweite seiner Kachel und / oder fuer einen Spielerschluessel. Deckel 32 Orte, danach gilt es fuer alle.
function B.Touch(rec, key)
    B._rev = (B._rev or 0) + 1
    local d = B._dirty
    d.any = true
    if rec == nil and key == nil then
        d.all = true
        return
    end
    if key ~= nil then d.keys[key] = true end
    if rec ~= nil then
        if rec.finder ~= nil then d.keys[rec.finder] = true end
        if rec.bond ~= nil then d.keys[rec.bond] = true end
        if rec.owner ~= nil then d.keys[rec.owner] = true end
        if d.n < 32 and tonumber(rec.x) ~= nil and tonumber(rec.y) ~= nil then
            d.n = d.n + 1
            d.spots[d.n] = { x = rec.x, y = rec.y }
        else
            d.all = true
        end
    end
end

-- Register holen. ModData.getOrCreate: Vanilla server/Foraging/forageServer.lua:26. Fruehestens in OnInitGlobalModData
-- (davor ist die gespeicherte Tabelle noch nicht geladen); eine frueher geholte Referenz wird nie behalten.
function B.InitRegistry()
    local r = ModData.getOrCreate(B.KEY)
    if type(r) ~= "table" then
        B.Err("registry: ModData.getOrCreate gave no table")
        return
    end
    r.v = 1
    r.n = tonumber(r.n) or 0
    r.nb = tonumber(r.nb) or 0
    if type(r.cubs) ~= "table" then r.cubs = {} end
    if type(r.players) ~= "table" then r.players = {} end
    if type(r.baits) ~= "table" then r.baits = {} end
    -- Unbrauchbare Zeilen raus (erst sammeln, dann loeschen).
    local bad = {}
    for id, rec in pairs(r.cubs) do
        if type(rec) ~= "table" or rec.id ~= id or type(rec.st) ~= "string" or tonumber(rec.x) == nil or tonumber(rec.y) == nil then
            bad[#bad + 1] = id
        end
    end
    for i = 1, #bad do
        B.Err("registry: dropped unreadable entry " .. tostring(bad[i]))
        r.cubs[bad[i]] = nil
    end
    -- B1b (PLAN_B1B.md 5.2): Folgen-Zustand und Name pruefen. Unbrauchbar -> nil (Vorgabe "stay" / Vorgabe-Name), je Feld eine Zeile.
    for id, rec in pairs(r.cubs) do
        if rec.mode ~= nil and rec.mode ~= "follow" and rec.mode ~= "stay" then
            B.Err("registry: entry " .. tostring(id) .. " had an unknown mode, set to stay")
            rec.mode = nil
        end
        if rec.name ~= nil then
            local clean = nil
            if type(rec.name) == "string" then clean = B.CleanName(rec.name) end
            if clean == nil or clean ~= rec.name then
                B.Err("registry: entry " .. tostring(id) .. " had an unusable name, removed")
                rec.name = nil
            end
        end
    end
    bad = {}
    for bid, bait in pairs(r.baits) do
        if type(bait) ~= "table" or bait.id ~= bid or bait.owner == nil or tonumber(bait.x) == nil or tonumber(bait.y) == nil then
            bad[#bad + 1] = bid
        end
    end
    for i = 1, #bad do
        B.Err("registry: dropped unreadable bait " .. tostring(bad[i]))
        r.baits[bad[i]] = nil
    end
    reg = r
    B._s = {}
    B.Touch()
    B.Log("registry ready: " .. tostring(B.CountRecs()) .. " entries, " .. tostring(B.CountBaits()) .. " bait spots")
end

-- Events.OnInitGlobalModData.Add: Vanilla server/Vehicles/ProfessionVehicles.lua:347 (server-Ordner).
Events.OnInitGlobalModData.Add(function() B.InitRegistry() end)

-- ---------------------------------------------------------------------------
-- Zaehlen
-- ---------------------------------------------------------------------------
function B.CountRecs()
    local n = 0
    if reg then
        for _, _ in pairs(reg.cubs) do n = n + 1 end
    end
    return n
end

-- Ungezaehmte Junge (fuer den Welt-Deckel BearCubWorldCap). online = { [Schluessel] = true } (wahlfrei): dann zaehlen nur Junge,
-- deren Uhr laeuft -- Finder (new/shy) bzw. bond (fed) ist da oder es gibt keinen. Die Uhren laufen nur, waehrend dieser Spieler
-- online ist (Plan 2); ohne diese Ausnahme fuellten Junge abwesender Spieler den Deckel fuer immer (Nachbesserung B2).
function B.CountWild(online)
    local n = 0
    if reg then
        for _, rec in pairs(reg.cubs) do
            if rec.st ~= "tame" and rec.st ~= "missing" and not rec.goneP then
                local key = rec.finder
                if rec.st == "fed" then key = rec.bond end
                if online == nil or key == nil or online[key] == true then n = n + 1 end
            end
        end
    end
    return n
end

function B.CountBaits()
    local n = 0
    if reg then
        for _, _ in pairs(reg.baits) do n = n + 1 end
    end
    return n
end

-- ---------------------------------------------------------------------------
-- Eintraege
-- ---------------------------------------------------------------------------

-- Neuer Eintrag fuer ein vorhandenes Tier. src = "forest" / "bait" / "found". Rueckgabe: rec oder nil, why.
-- getAnimalID: Vanilla client/ISUI/Animal/ISAnimalUI.lua:53 (nur Gegenprobe: die Zahl ist eine von 10000, nicht eindeutig).
function B.NewRec(src, pkey, animal, x, y, z, now)
    if not reg then return nil, "noreg" end
    if not animal then return nil, "noanimal" end
    if B.CountRecs() >= B.CFG.maxRecs then return nil, "full" end
    reg.n = reg.n + 1
    local id = "b" .. string.format("%d", reg.n)
    local rec = {
        id = id, nr = reg.n, kind = "cub",
        aid = animal:getAnimalID(),
        src = src, st = "new",
        finder = pkey, bond = nil, owner = nil,
        tame = 0, fedN = 0, petN = 0, last = nil,
        feedAt = nil, petAt = nil,
        born = now, tamedAt = nil,
        idleH = 0, goneP = nil, missN = 0, missAt = nil, missH = 0, hintAt = nil,
        x = x, y = y, z = z,
        hx = nil, hy = nil, hz = nil,
        mode = nil, name = nil,                       -- B1b: nil = "stay" / Vorgabe-Name beim Client
    }
    if src == "found" then
        -- ein Junges ohne Eintrag, das jemand anfasst: schon entdeckt, gehoert niemandes "wildem Jungen"
        rec.st = "shy"
        rec.finder = nil
    end
    reg.cubs[id] = rec
    B.Ses(id).obj = animal
    -- B1b (PLAN_B1B.md 4.4): Spiegel SOFORT schreiben, ohne die isExistInTheWorld-Frage von B.Commit -- die ist direkt nach
    -- addToWorld noch falsch (Fix 1); ohne Spiegel saehe der Waisen-Suchlauf das neue Junge sonst als Waise.
    -- Schreiben in die ModData eines Tiers: Vanilla client/ISUI/ISInventoryPaneContextMenu.lua:4127
    -- (animal:getModData()["skeleton"] = "true"); lesen am Tier shared/Definitions/animal/ButcheringUtil.lua:596.
    local md = animal:getModData()
    if md then md[B.MARK] = { id = id, st = rec.st } end
    B.Touch(rec)
    return rec, nil
end

local function objAlive(o)
    -- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; isDead am Tier: server/Traps/STrapGlobalObject.lua:238
    return o ~= nil and o:isExistInTheWorld() and not o:isDead()
end

-- Tier -> Eintrag. Erst die Objekte dieser Sitzung, dann der Spiegel mit Gegenprobe (Art, AnimalID, kein zweites lebendes
-- Tier unter derselben Kennung). Ein Junges ganz ohne Eintrag wird aufgenommen (src = "found"), wenn der Deckel es erlaubt.
-- getAnimalType: Vanilla shared/Definitions/animal/ButcheringUtil.lua:13; getModData am Tier: ButcheringUtil.lua:596/602;
-- getX/getY/getZ am Tier: shared/Definitions/animal/ButcheringUtil.lua:575-577.
function B.RecOf(animal)
    if not reg then return nil, "noreg" end
    if not animal then return nil, "noanimal" end
    if animal:getAnimalType() ~= B.CUB then return nil, "kind" end
    for id, s in pairs(B._s) do
        if s.obj == animal then
            local rec = reg.cubs[id]
            if rec then return rec, nil end
        end
    end
    local aid = animal:getAnimalID()
    local md = animal:getModData()            -- erst NACH der Art-Frage
    local mark = md and md[B.MARK]
    if type(mark) == "table" and mark.id ~= nil then
        local rec = reg.cubs[mark.id]
        if rec and rec.aid == aid then
            local s = B.Ses(rec.id)
            if s.obj == nil or not objAlive(s.obj) then
                s.obj = animal
                return rec, nil
            end
            -- ein anderes lebendes Tier traegt diesen Eintrag schon: dem Spiegel an DIESEM Tier wird nicht geglaubt
        end
    end
    local x, y, z = math.floor(animal:getX()), math.floor(animal:getY()), math.floor(animal:getZ())
    local rec, why = B.NewRec("found", nil, animal, x, y, z, B.Now())
    if not rec then return nil, why end
    B.Commit(rec)
    B.Log("found " .. rec.id .. " at " .. x .. "," .. y)
    return rec, nil
end

-- Plaetze eines Spielers, gezaehlt aus cubs / baits (Form von B.View.me, Plan 6.2.5).
function B.SlotsOf(pkey, now)
    local slots = {
        key = pkey,
        on = (B.Opt("BearCubsEnabled") == true),
        bears = 0,
        maxBears = B.Opt("BearMaxPerPlayer"),
        bonded = nil, wild = nil, bait = nil,
        lockUntil = 0,
    }
    if not reg or pkey == nil then return slots end
    for id, rec in pairs(reg.cubs) do
        if rec.owner == pkey then
            slots.bears = slots.bears + 1
        elseif rec.bond == pkey and rec.st == "fed" then
            slots.bonded = id
        elseif rec.finder == pkey and rec.bond == nil and (rec.st == "new" or rec.st == "shy") and not rec.goneP then
            -- ein faelliges ("zieht weiter", goneP) Junges belegt den Platz nicht mehr: es wartet nur noch auf einen
            -- unbeobachteten Moment, um zu verschwinden
            slots.wild = id
        end
    end
    for bid, bait in pairs(reg.baits) do
        if bait.owner == pkey then slots.bait = bid end
    end
    local prec = reg.players[pkey]
    if type(prec) == "table" then
        local lock = tonumber(prec.lockUntil)
        if lock and lock > now then slots.lockUntil = lock end
    end
    return slots
end

-- Aenderung festschreiben: Balken klemmen, Spiegel am Tier schreiben (nie transmitModData), "geaendert" merken --
-- die Sicht geht im selben oder im naechsten Takt hinaus.
function B.Commit(rec)
    if not reg or not rec then return end
    local tame = tonumber(rec.tame) or 0
    if tame < 0 then tame = 0 end
    if tame > 100 then tame = 100 end
    rec.tame = B.Round1(tame)
    local s = B._s[rec.id]
    local a = s and s.obj
    if a ~= nil and a:isExistInTheWorld() then
        local md = a:getModData()
        if md then
            local mark = md[B.MARK]
            if type(mark) ~= "table" then
                mark = {}
                md[B.MARK] = mark
            end
            mark.id = rec.id
            mark.st = rec.st
        end
    end
    B.Touch(rec)
end

-- Sperre nach dem Tod des eigenen Baeren.
local function setLock(pkey, now)
    local days = B.Opt("BearDeathLockDays")
    if pkey == nil or days <= 0 then return 0 end
    local prec = reg.players[pkey]
    if type(prec) ~= "table" then
        prec = { lockUntil = nil, tamedN = 0 }
        reg.players[pkey] = prec
    end
    prec.lockUntil = now + days * 24
    B.Touch(nil, pkey)
    return days
end

-- Abgelaufene Sperren raeumen (Langsam-Takt): players traegt nur Eintraege mit laufender Sperre.
function B.CleanLocks(now)
    if not reg then return end
    local old = {}
    for pkey, prec in pairs(reg.players) do
        local lock = type(prec) == "table" and tonumber(prec.lockUntil) or nil
        if lock == nil or lock <= now then old[#old + 1] = pkey end
    end
    for i = 1, #old do
        reg.players[old[i]] = nil
        B.Touch(nil, old[i])
    end
end

local function tellKey(pkey, note)
    if pkey == nil then return end
    local find = B.PlayerByKey
    local p = find and find(pkey)
    if p then B.Tell(p, note) end
end

-- Eintrag beenden. how = "vanish" (weitergezogen), "dead" (gesehen: isDead), "lost" (fehlt), "clean" (aufgeraeumt).
-- Loescht den Eintrag, setzt bei "dead" und gezaehmt die Sperre fuer den Besitzer, meldet. Das Tier selbst entfernt
-- nur B.RemoveCub (server/BanditsNPCBearWorld.lua).
function B.Close(rec, how)
    if not reg or not rec then return end
    local id = rec.id
    if reg.cubs[id] ~= rec then return end
    local wasTame = (rec.st == "tame" or rec.st == "missing") and rec.owner ~= nil
    reg.cubs[id] = nil
    B._s[id] = nil
    B.Touch(rec)
    if how == "dead" then
        if wasTame then
            local days = setLock(rec.owner, B.Now())
            if days > 0 then
                tellKey(rec.owner, { k = "UI_BN_Bear_Note_BearDead", t = "days", v = days, tone = "bad" })
            else
                tellKey(rec.owner, { k = "UI_BN_Bear_Note_Dead", tone = "bad" })
            end
        else
            tellKey(rec.bond or rec.finder, { k = "UI_BN_Bear_Note_Dead", tone = "bad" })
        end
    elseif how == "vanish" then
        tellKey(rec.bond or rec.finder, { k = "UI_BN_Bear_Note_Vanished" })
    elseif how == "lost" then
        tellKey(rec.owner or rec.bond, { k = "UI_BN_Bear_Why_Gone", tone = "bad" })
    end
    B.Log("close " .. tostring(id) .. " " .. tostring(how) .. " st " .. tostring(rec.st) .. " owner " .. tostring(rec.owner))
end

-- Naechster Eintrag zu einem Spieler (letzte bekannte Kachel), fuer Meldungen. Rueckgabe: rec, animal.
function B.NearestRec(player, radius)
    if not reg or not player then return nil, nil end
    local px, py = player:getX(), player:getY()
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        local d = B.DistXY(px, py, rec.x, rec.y)
        if (radius == nil or d <= radius) and (bestD == nil or d < bestD) then
            best = rec
            bestD = d
        end
    end
    if not best then return nil, nil end
    local find = B.FindAnimal
    return best, find and find(best) or nil
end

-- ---------------------------------------------------------------------------
-- Koederplaetze
-- ---------------------------------------------------------------------------
function B.BaitOf(pkey)
    if not reg or pkey == nil then return nil end
    for _, bait in pairs(reg.baits) do
        if bait.owner == pkey then return bait end
    end
    return nil
end

function B.NewBait(pkey, x, y, z, kind, now, night)
    if not reg then return nil end
    reg.nb = reg.nb + 1
    local bid = "k" .. string.format("%d", reg.nb)
    local bait = {
        id = bid, owner = pkey, x = x, y = y, z = z, kind = kind, t0 = now,
        nights = 0, miss = 0, wasNight = (night == true), ready = false, warnAt = nil,
    }
    reg.baits[bid] = bait
    B.Touch(nil, pkey)
    return bait
end

function B.DropBait(bait)
    if not reg or not bait then return end
    if reg.baits[bait.id] == bait then
        reg.baits[bait.id] = nil
        B.Touch(nil, bait.owner)
    end
end

-- ---------------------------------------------------------------------------
-- Sicht bauen (Plan 6.2.5): nur Zahlen, Texte, Wahrheitswerte, Tabellen -- nie ein Objekt, nie ein Register-Eintrag selbst.
-- Inhalt: eigene Plaetze, das eigene gebundene / gezaehmte Junge, die Jungen in B.CFG.tellDist Kacheln (naechste zuerst,
-- hoechstens B.CFG.viewMax), der eigene Koederplatz.
-- ---------------------------------------------------------------------------
local function viewEntry(rec)
    local oid = -1
    local s = B._s[rec.id]
    local a = s and s.obj
    if a ~= nil and a:isExistInTheWorld() then
        local got = a:getOnlineID()          -- Vanilla shared/Definitions/animal/ButcheringUtil.lua:614 (isServer-Zweig)
        if got ~= nil then oid = got end
    end
    -- B1b (PLAN_B1B.md 5.2): name (nil fehlt im Eintrag), mode nur bei "tame" (Schild Zeile 2)
    local mode = nil
    if rec.st == "tame" then mode = B.ModeOf(rec) end
    return {
        id = rec.id, oid = oid, st = rec.st, tame = rec.tame, fedN = rec.fedN, petN = rec.petN, last = rec.last,
        feedAt = rec.feedAt, petAt = rec.petAt, bond = rec.bond, owner = rec.owner, src = rec.src,
        name = rec.name, mode = mode,
    }
end

function B.BuildView(player)
    local now = B.Now()
    local pkey = B.PlayerKey(player)
    local payload = { me = B.SlotsOf(pkey, now), cubs = {}, bait = nil }
    if not reg or not player then return payload end
    local px, py = player:getX(), player:getY()
    local limit = B.CFG.viewMax
    local list = payload.cubs
    local near = {}
    for _, rec in pairs(reg.cubs) do
        if rec.owner == pkey or rec.bond == pkey then
            if #list < limit then list[#list + 1] = viewEntry(rec) end
        else
            local d = B.DistXY(px, py, rec.x, rec.y)
            if d <= B.CFG.tellDist then near[#near + 1] = { rec = rec, d = d } end
        end
    end
    if #near > 1 then
        table.sort(near, function(a, b) return a.d < b.d end)
    end
    for i = 1, #near do
        if #list >= limit then break end
        list[#list + 1] = viewEntry(near[i].rec)
    end
    local bait = B.BaitOf(pkey)
    if bait then
        payload.bait = {
            id = bait.id, x = bait.x, y = bait.y, z = bait.z, kind = bait.kind,
            nights = bait.nights, max = B.Opt("BearBaitNights"), ready = (bait.ready == true),
        }
    end
    return payload
end
