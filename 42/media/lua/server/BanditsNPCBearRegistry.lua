if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Register (B1a, PLAN_ZAEHMEN.md 4.1, 4.2, 6.2.3).
--
-- Die Wahrheit ueber jedes Junge steht NUR hier: globale ModData "TrueCompanionsBears" beim Schreiber. Sie wird nie
-- uebertragen (kein ModData.transmit, kein request): kein Client erfaehrt fremde Zeilen, kein Client kann sie ueberschreiben.
-- Am Tier liegt ein Spiegel zum Wiederfinden. B1c (PLAN_B1C.md 2): Register v2 mit Epoche ep, je Eintrag Kennzeichen u,
-- Koerper-Generation gen und Aenderungszaehler r; der Spiegel v2 traegt alles Wichtige (server/BanditsNPCBearHeal.lua). Besitz,
-- Balken und Zeiten kommen aus dem Spiegel NUR, wenn kein Eintrag da ist und kein Eintrag widerspricht (Heilung nach einem
-- Registerverlust, B.HealFromMark) -- sonst gewinnt immer das Register.
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
                                -- B1c: + calmUntil, ownUntil, walk, g (Zombie-Wache), ride (Mitfahren), vx, vy, vAt (Lage der Sicht)
                                -- B1d: + sta, breathAt, kx, ky, kAt, kAcc, staV, staVAt, xb, gDirty (Wachsen, Ausdauer)
                                -- B1e: + swapAt, swapTryAt, swapFailN (Koerper-Tausch), busyUntil (Fuettern/Streicheln laeuft)
                                -- Nachbesserung B1e: + swapWantAt (Wartezeit "move"), placedAt (Koerper erzeugt, "Call to me")
                                -- F1: + sat, satAt, backTried (Sitz), standUntil (Aufstehen), roam = { pauseUntil } (Frei), come
                                --     (Komm her), revN, revFail (C1), ldSent, busySent (Sicht nachschicken bei Wechsel)
B._healUntil = B._healUntil or 0    -- B1c: Echtzeit-Ende des Heil-Fensters nach InitRegistry (PLAN_B1C.md 1.1 Schritt 2)
B._healScanAt = B._healScanAt or nil
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
-- B1c: Kennzeichen u eines Jungen (PLAN_B1C.md 0.1): getTimestampMs() * 1000 + ZombRand(1000) (getTimestampMs: Vanilla
-- server/Foraging/forageServer.lua:456; ZombRand(n): shared/TimedActions/Animals/ISMilkAnimal.lua:25), bis zu 8 Versuche gegen
-- die Eintraege der Tabelle cubs; danach groesstes vorhandenes u + 1 (immer eindeutig). Zahlen bis ~2e15 < 2^53 (exakt als Double).
local function uTaken(cubs, u)
    for _, rec in pairs(cubs) do
        if type(rec) == "table" and rec.u == u then return true end
    end
    return false
end

local function newUIn(cubs)
    local base = getTimestampMs() * 1000
    for _ = 1, 8 do
        local u = base + ZombRand(1000)
        if not uTaken(cubs, u) then return u end
    end
    local top = base
    for _, rec in pairs(cubs) do
        local ru = type(rec) == "table" and tonumber(rec.u) or nil
        if ru ~= nil and ru > top then top = ru end
    end
    return top + 1
end

function B.InitRegistry()
    local r = ModData.getOrCreate(B.KEY)
    if type(r) ~= "table" then
        B.Err("registry: ModData.getOrCreate gave no table")
        return
    end
    -- B1c (PLAN_B1C.md 2.1): Fassung 2; die Epoche ep nur beim ERSTEN Anlegen stempeln (fehlt sie, ist das Register neu --
    -- neu angelegt oder verloren; ein Spiegel mit anderer Epoche kommt dann aus einem frueheren Register)
    r.v = 2
    if tonumber(r.ep) == nil then
        r.ep = getTimestampMs()
        r.epAt = B.Now()
    end
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
    -- F1 (PLAN_F1.md 5.1): vier Modi (B.MODES); passive nur true an einem gezaehmten/vermissten Eintrag, sonst nil (Zeile nur bei Unsinn).
    local modes = B.MODES or { follow = true, stay = true, sit = true, roam = true }
    for id, rec in pairs(r.cubs) do
        if rec.mode ~= nil and (type(rec.mode) ~= "string" or modes[rec.mode] ~= true) then
            B.Err("registry: entry " .. tostring(id) .. " had an unknown mode, set to stay")
            rec.mode = nil
        end
        if rec.passive ~= nil then
            if rec.passive ~= true or (rec.st ~= "tame" and rec.st ~= "missing") then
                B.Err("registry: entry " .. tostring(id) .. " had an unusable passive switch, removed")
                rec.passive = nil
            end
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
    -- B1c (PLAN_B1C.md 2.1): u nachtragen (B1a/B1b-Eintraege haben keins), gen/r als Zahl, ride nur gueltig an einem gezaehmten
    -- Eintrag mit Besitzer (sonst ohne Koerper: "missing" nach den Fehlversuchen; es kommt beim Wiederfinden zurueck -- "Call to me" fuer
    -- ein Junges ohne anklickbaren Koerper erst spaeter ueber das Baeren-Fenster, Frage F4). Je Feld eine Zeile nur bei Unsinn.
    for id, rec in pairs(r.cubs) do
        if tonumber(rec.u) == nil then
            if rec.u ~= nil then B.Err("registry: entry " .. tostring(id) .. " had an unusable mark number, given a new one") end
            rec.u = nil
            rec.u = newUIn(r.cubs)
        end
        if rec.gen ~= nil and tonumber(rec.gen) == nil then
            B.Err("registry: entry " .. tostring(id) .. " had an unusable body generation, set to 0")
        end
        rec.gen = tonumber(rec.gen) or 0
        rec.r = tonumber(rec.r) or 0
        if rec.ride ~= nil then
            local okRide = type(rec.ride) == "table" and tonumber(rec.ride.at) ~= nil and rec.st == "tame" and rec.owner ~= nil
            if not okRide then
                B.Err("registry: entry " .. tostring(id) .. " had an unusable ride state, removed")
                rec.ride = nil
            end
        end
    end
    -- F2 (PLAN_F2.md 4.2, 11.5): am Boden (down: Spielstunde), Verband (bndH: Spielstunde bis, bndR: %/h 0..50), Kills (kZ, kB: ganze Zahlen
    -- 0..killTop) -- nur Zahlen an einem gezaehmten/vermissten Eintrag, sonst nil; je Feld eine Fehlerzeile nur bei Unsinn.
    local killTop = tonumber(B.CFG.killTop) or 999999
    for id, rec in pairs(r.cubs) do
        local tame = rec.st == "tame" or rec.st == "missing"
        local nums = { "down", "bndH", "bndR", "kZ", "kB" }
        for i = 1, #nums do
            local k = nums[i]
            local v = rec[k]
            if v ~= nil and (not tame or tonumber(v) == nil) then
                if tonumber(v) == nil then B.Err("registry: entry " .. tostring(id) .. " had an unusable " .. k .. ", removed") end
                rec[k] = nil
            end
        end
        if tonumber(rec.bndR) ~= nil then
            local b = tonumber(rec.bndR)
            if b < 0 then b = 0 end
            if b > 50 then b = 50 end
            rec.bndR = b
        end
        if (rec.bndH == nil) ~= (rec.bndR == nil) then rec.bndH, rec.bndR = nil, nil end
        local kk = { "kZ", "kB" }
        for i = 1, 2 do
            local v = tonumber(rec[kk[i]])
            if v ~= nil then
                v = math.floor(v)
                if v < 0 then v = 0 end
                if v > killTop then v = killTop end
                rec[kk[i]] = v
            end
        end
    end
    -- B1d (PLAN_B1D.md 2.2): Wachstum, Fuetter-Bonus, Leben, Erfahrung nachtragen / klemmen (server/BanditsNPCBearGrow.lua). Ein
    -- B1c-Eintrag ohne g bekommt es aus tamedAt (nur Diagnose-Zeile); Fehlerzeilen nur bei Unsinn. Wilde Eintraege: alle B1d-Felder nil.
    if B.GrowFix then
        local now = B.Now()
        for _, rec in pairs(r.cubs) do B.GrowFix(rec, now, true) end
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
    -- B1c (PLAN_B1C.md 1.1 Schritt 2): Heil-Fenster -- die ersten healWindowMs sucht der Hirn-Takt je healScanMs nach Jungen mit
    -- Spiegel (Zellen laden nach), und der Wald-Wurf wartet so lange. getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
    B._healUntil = getTimestampMs() + B.CFG.healWindowMs
    B._healScanAt = nil
    B.Touch()
    B.Log("registry ready: " .. tostring(B.CountRecs()) .. " entries, " .. tostring(B.CountBaits()) .. " bait spots, epoch "
        .. tostring(r.ep))
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

-- B1c (PLAN_B1C.md 6.3): Kennzeichen, Kennung, Zaehler.
function B.RecByU(u)
    if not reg or u == nil then return nil end
    for _, rec in pairs(reg.cubs) do
        if rec.u == u then return rec end
    end
    return nil
end

function B.NewU()
    if not reg then return newUIn({}) end
    return newUIn(reg.cubs)
end

-- Naechste freie Kennung "b<n>" ab reg.n + 1 (ueberspringt belegte; hoechstens maxRecs Eintraege). Rueckgabe: id, nr.
function B.NewId()
    if not reg then return nil, nil end
    local nr = reg.n + 1
    while reg.cubs["b" .. string.format("%d", nr)] ~= nil do nr = nr + 1 end
    reg.n = nr
    return "b" .. string.format("%d", nr), nr
end

-- Zaehler nachziehen (nur ganze Zahlen ueber dem Stand).
function B.BumpN(nr)
    if not reg then return end
    local v = tonumber(nr)
    if v == nil then return end
    v = math.floor(v)
    if v > reg.n then reg.n = v end
end

-- Spiegel schreiben ueber B.WriteMark (server/BanditsNPCBearHeal.lua, laedt VOR dieser Datei; zur Laufzeit geholt). Fehlt die
-- Datei, der B1b-Spiegel { id, st }. Schreiben in die ModData eines Tiers: Vanilla client/ISUI/ISInventoryPaneContextMenu.lua:4127.
local function writeMark(rec, a)
    local wm = B.WriteMark
    if wm then
        wm(rec, a)
        return
    end
    local md = a:getModData()
    if md then md[B.MARK] = { id = rec.id, st = rec.st } end
end

-- Einen fertigen Eintrag einfuegen (Heilung, PLAN_B1C.md 2.4): Register, Objekt der Sitzung, Spiegel sofort, "geaendert".
function B.InsertRec(rec, a)
    if not reg or type(rec) ~= "table" or rec.id == nil then return nil end
    reg.cubs[rec.id] = rec
    B.Ses(rec.id).obj = a
    if a then writeMark(rec, a) end
    B.Touch(rec)
    return rec
end

-- Neuer Eintrag fuer ein vorhandenes Tier. src = "forest" / "bait" / "found". Rueckgabe: rec oder nil, why.
-- getAnimalID: Vanilla client/ISUI/Animal/ISAnimalUI.lua:53 (nur Gegenprobe: die Zahl ist eine von 10000, nicht eindeutig).
-- B1c: Kennung ueber B.NewId (ueberspringt belegte), Kennzeichen u, gen 0, r 0, Spiegel v2 ueber B.WriteMark.
function B.NewRec(src, pkey, animal, x, y, z, now)
    if not reg then return nil, "noreg" end
    if not animal then return nil, "noanimal" end
    if B.CountRecs() >= B.CFG.maxRecs then return nil, "full" end
    local id, nr = B.NewId()
    local rec = {
        id = id, nr = nr, kind = "cub",
        u = B.NewU(), gen = 0, r = 0,
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
    writeMark(rec, animal)
    B.Touch(rec)
    return rec, nil
end

local function objAlive(o)
    -- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; isDead am Tier: server/Traps/STrapGlobalObject.lua:238
    return o ~= nil and o:isExistInTheWorld() and not o:isDead()
end

-- Tier -> Eintrag. Erst die Objekte dieser Sitzung (Riegel 1), dann der Spiegel ueber B.HealFromMark (PLAN_B1C.md 2.6): binden,
-- wiederherstellen oder ablehnen ("stale"/"dup": ein Doppel oder eine veraltete Kopie wird NIE ein neuer Eintrag; "heal": ein
-- zahmer Spiegel, der gerade nicht herstellbar ist, wird es auch nie -- Nachbesserung B1c A1). Ein Junges ganz ohne Eintrag (kein
-- Spiegel, oder ein wilder Spiegel, den die Heilung nicht nimmt) wird aufgenommen (src = "found"), wenn der Deckel es erlaubt.
-- Art-Frage ueber B.BodyKind (shared/BanditsNPCBear.lua; B1e: beide Koerper); getModData am Tier: ButcheringUtil.lua:596/602;
-- getX/getY/getZ am Tier: shared/Definitions/animal/ButcheringUtil.lua:575-577.
-- B1e (PLAN_B1E.md 1.3 Nr. 5, 3.2 Nr. 4): ein GROSSER Koerper ohne Eintrag ist nie ein neuer Fund ("found" gibt es nur fuer das
-- Junge): nil, "kind" -- er bleibt unberuehrt (Menue: Why_Gone) bzw. faellt als Waise / Kopie unter die B1b/B1c-Riegel.
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 3): ebenso ein Junges in einem Nicht-Standard-Aussehen (das erzeugt nur der Aussehen-
-- Knopf an einem gezaehmten Baeren) -- nie ein WILDES Generator-Junges als neuer Fund.
function B.RecOf(animal)
    if not reg then return nil, "noreg" end
    if not animal then return nil, "noanimal" end
    local body, look = B.BodyKind(animal)
    if not body then return nil, "kind" end
    for id, s in pairs(B._s) do
        if s.obj == animal then
            local rec = reg.cubs[id]
            if rec then return rec, nil end
        end
    end
    local md = animal:getModData()            -- erst NACH der Art-Frage
    local mark = md and md[B.MARK]
    if type(mark) == "table" and mark.id ~= nil then
        local heal = B.HealFromMark
        if heal then
            local got = heal(animal, mark, nil)
            if type(got) == "table" then return got, nil end
            if got == "stale" or got == "dup" then return nil, "stale" end
            -- Nachbesserung B1c A1/B4 (Auftrag 1: "nie neu als found/shy", "Deckel je Spieler gilt weiter"): meldet der Spiegel ein
            -- gezaehmtes, vermisstes oder (v2) angefuettertes Junges und konnte es gerade nicht hergestellt werden (Deckel voll,
            -- Mehrspieler-Spiegel ohne Konto, v1-Spiegel "tame" im Mehrspieler), wird es KEIN neuer Fund: es bleibt unberuehrt (das
            -- Menue sagt Why_Gone), der Spiegel bleibt, und der Suchlauf stellt es her, sobald ein Platz frei ist.
            local st = mark.st
            local v2 = (tonumber(mark.v) or 1) >= 2
            if st == "tame" or st == "missing" or (v2 and st == "fed") then return nil, "heal" end
        else
            -- ohne server/BanditsNPCBearHeal.lua: der B1b-Weg (gleiche Kennung, gleiche AnimalID, kein anderes lebendes Objekt)
            local rec = reg.cubs[mark.id]
            if rec and rec.aid == animal:getAnimalID() then
                local s = B.Ses(rec.id)
                if s.obj == nil or not objAlive(s.obj) then
                    s.obj = animal
                    return rec, nil
                end
            end
        end
    end
    if body == "big" then return nil, "kind" end
    if look ~= nil and look ~= "std" then return nil, "kind" end
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

-- Aenderung festschreiben: Balken klemmen, Aenderungszaehler r + 1 (B1c, fuer die Spiegel-Probe), Spiegel am Tier schreiben
-- (nie transmitModData), "geaendert" merken -- die Sicht geht im selben oder im naechsten Takt hinaus.
-- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29 (ein Tier ausserhalb der Welt -- entfernt,
-- mitfahrend -- bekommt keinen Spiegel; die Spiegel-Probe im Hirn-Takt holt das nach, sobald es wieder da ist).
function B.Commit(rec)
    if not reg or not rec then return end
    local tame = tonumber(rec.tame) or 0
    if tame < 0 then tame = 0 end
    if tame > 100 then tame = 100 end
    rec.tame = B.Round1(tame)
    rec.r = (tonumber(rec.r) or 0) + 1
    local s = B._s[rec.id]
    local a = s and s.obj
    if a ~= nil and a:isExistInTheWorld() then writeMark(rec, a) end
    B.Touch(rec)
end

-- Sperre nach dem Tod des eigenen Baeren.
local function setLock(pkey, now)
    local days = tonumber(B.CFG.deathLockDays) or 7          -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3): fester Wert
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
    -- F2 (PLAN_F2.md 4.1): Kampf und laufende Gegner-Angriffe weg, BEVOR die Sitzung geht (server/BanditsNPCBearFight*.lua)
    if B.FightDrop then B.FightDrop(id, how) end
    if B.FoeDrop then B.FoeDrop(id) end
    reg.cubs[id] = nil
    B._s[id] = nil
    if B.CalmDrop then B.CalmDrop(id) end          -- B1c: Laerm-Wache (server/BanditsNPCBearGuard.lua)
    B.Touch(rec)
    -- F1 (PLAN_F1.md 4a, A1/B6): Note_Dead und Why_Gone tragen bd = "big" beim grossen Koerper (B.NoteBd, Text "bear" statt "cub").
    -- "lost" erreicht einen zahmen Eintrag nicht mehr (F1 0.8: missing schliesst nie); es bleibt fuer "fed".
    if how == "dead" then
        if wasTame then
            local days = setLock(rec.owner, B.Now())
            if days > 0 then
                tellKey(rec.owner, { k = "UI_BN_Bear_Note_BearDead", t = "days", v = days, tone = "bad" })
            else
                tellKey(rec.owner, B.NoteBd({ k = "UI_BN_Bear_Note_Dead", tone = "bad" }, rec))
            end
        else
            tellKey(rec.bond or rec.finder, { k = "UI_BN_Bear_Note_Dead", tone = "bad" })
        end
    elseif how == "vanish" then
        tellKey(rec.bond or rec.finder, { k = "UI_BN_Bear_Note_Vanished" })
    elseif how == "lost" then
        tellKey(rec.owner or rec.bond, B.NoteBd({ k = "UI_BN_Bear_Why_Gone", tone = "bad" }, rec))
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
-- B1c (PLAN_B1C.md 4.1): je Eintrag x, y (ganze Kacheln, letzte bekannte Stelle), ride (true = faehrt mit) und fuer den Besitzer
-- callWait (Sekunden Rest der "Call to me"-Abklingzeit, aufgerundet; fehlt = bereit). Das wilde Junge des Finders steht IMMER in
-- seiner Sicht (Bildschirm-Markierung). N3: ein Konto ohne Schluessel bekommt nur Junge in tellDist.
-- B1d (PLAN_B1D.md 4.1): je gezaehmtem Eintrag zusaetzlich sz, hp, hpMax, sta, staMax, day, stg, nst, nxt (B.GrowView).
-- F1 (PLAN_F1.md 5.3): flache Felder fuer das Baeren-Fenster -- mode (tame; jetzt auch "sit"/"roam"), pas (tame/missing, rec.passive),
-- u (tame/missing, Kennzeichen als Zahl), ld (Koerper in der Welt, wie oid), hide (Zombie-Wache an), sit (Modus "sit" UND er sitzt
-- schon, s.sat), cm (Komm her laeuft), busy (Fuettern/Streicheln laeuft, s.busyUntil); fehlt ein Feld, ist es falsch. B.GrowView jetzt
-- fuer tame UND missing (Werte, Faehigkeiten, Traglast).
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 3): lk (Familie des JETZIGEN Koerpers, fehlt = "std") und lkg (true = ein Wachs-Tausch
-- wartet, der Knopf ist grau) ueber B.LookView (server/BanditsNPCBearLook.lua) -- fuer alle tame/missing-Eintraege (das Namensschild
-- braucht lk auch bei fremden Baeren).
-- ---------------------------------------------------------------------------
local function viewEntry(rec, pkey, ms)
    local oid = -1
    local s = B._s[rec.id]
    local a = s and s.obj
    local ld = nil
    if a ~= nil and a:isExistInTheWorld() then
        local got = a:getOnlineID()          -- Vanilla shared/Definitions/animal/ButcheringUtil.lua:614 (isServer-Zweig)
        if got ~= nil then oid = got end
        ld = true
    end
    -- B1b (PLAN_B1B.md 5.2): name (nil fehlt im Eintrag), mode nur bei "tame" (Schild Zeile 2)
    local mode = nil
    if rec.st == "tame" then mode = B.ModeOf(rec) end
    local callWait = nil
    if pkey ~= nil and rec.owner == pkey and B.CallLeft then
        local left = B.CallLeft(rec, ms)
        if left > 0 then callWait = math.ceil(left / 1000) end
    end
    local ride = nil
    if rec.ride ~= nil then ride = true end
    local t = {
        id = rec.id, oid = oid, st = rec.st, tame = rec.tame, fedN = rec.fedN, petN = rec.petN, last = rec.last,
        feedAt = rec.feedAt, petAt = rec.petAt, bond = rec.bond, owner = rec.owner, src = rec.src,
        name = rec.name, mode = mode,
        x = math.floor(tonumber(rec.x) or 0), y = math.floor(tonumber(rec.y) or 0), ride = ride, callWait = callWait,
        ld = ld,
    }
    local tameOrMissing = rec.st == "tame" or rec.st == "missing"
    if tameOrMissing then
        if rec.passive == true then t.pas = true end
        t.u = tonumber(rec.u)
    end
    if s ~= nil then
        if type(s.g) == "table" and s.g.on == true then t.hide = true end
        if rec.st == "tame" and mode == "sit" and s.sat == true then t.sit = true end
        if s.come ~= nil then t.cm = true end
        local left = (tonumber(s.busyUntil) or 0) - ms
        if left > 0 and left <= (tonumber(B.CFG.busyMs) or 20000) then t.busy = true end
    end
    -- B1d (PLAN_B1D.md 4.1): fertige Zahlen sz hp hpMax sta staMax day stg nst nxt (server/BanditsNPCBearGrow.lua); F1: auch missing
    if tameOrMissing and B.GrowView then B.GrowView(rec, t) end
    if tameOrMissing and B.LookView then B.LookView(rec, t) end
    -- F2 (PLAN_F2.md 4.7, 11.2, 11.5, 11.7): fst, mdmg*, kZ, kB, fleeP (server/BanditsNPCBearFight.lua), dn / dnH (...Hurt.lua),
    -- bnd (...Mend.lua) -- flach, nur gezaehmt/vermisst
    if tameOrMissing then
        local now = B.Now()
        if B.FightView then B.FightView(rec, t, ms) end
        if B.DownView then B.DownView(rec, t, now) end
        if B.MendView then B.MendView(rec, t, now) end
    end
    return t
end

-- Das wilde Junge des Finders (Form B.SlotsOf "wild"): ungebunden, new/shy, nicht faellig.
local function wildOf(rec, pkey)
    return pkey ~= nil and rec.finder == pkey and rec.bond == nil and (rec.st == "new" or rec.st == "shy") and not rec.goneP
end

function B.BuildView(player)
    local now = B.Now()
    local pkey = B.PlayerKey(player)
    local payload = { me = B.SlotsOf(pkey, now), cubs = {}, bait = nil }
    if not reg or not player then return payload end
    local ms = getTimestampMs()              -- Vanilla server/Foraging/forageServer.lua:456
    local px, py = player:getX(), player:getY()
    local limit = B.CFG.viewMax
    local list = payload.cubs
    local near = {}
    for _, rec in pairs(reg.cubs) do
        if pkey ~= nil and (rec.owner == pkey or rec.bond == pkey or wildOf(rec, pkey)) then
            if #list < limit then list[#list + 1] = viewEntry(rec, pkey, ms) end
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
        list[#list + 1] = viewEntry(near[i].rec, pkey, ms)
    end
    local bait = B.BaitOf(pkey)
    if bait then
        payload.bait = {
            id = bait.id, x = bait.x, y = bait.y, z = bait.z, kind = bait.kind,
            nights = bait.nights, max = tonumber(B.CFG.baitMaxNights) or 3, ready = (bait.ready == true),
        }
    end
    return payload
end
