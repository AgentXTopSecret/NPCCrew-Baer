if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, der gezaehmte Baer kaempft (F2 = B5a, PLAN_F2.md 0.1, 0.5-0.9, 2.2, 2.3, 4.2, 4.3; Nachtrag 11.2, 11.5, 11.7).
--
-- Kevin ENT:63-66: "egal was er tut wenn ein zombies kommt soll der dann immer kaempfen ausser man stellt den auf passiv"; das Jungtier
-- kaempft nie (versteckt sich, B1c). Ab Halbstark (grosser Koerper) greift er Zombies und feindliche Banditen an (Ziele nur aus B._foes,
-- server/BanditsNPCBearFightFoes.lua -- nie Spieler, Crew, Neutrale, Tiere). Kampf hat Vorrang vor Folgen / Bleiben / Sitz / Frei / Komm
-- her; danach gilt der Befehl von selbst wieder (FollowStep / OrderStep fuehren zurueck). Passiv, wenig Leben (11.7: nur noch BearFleeHits
-- Treffer vom Tod), leere Ausdauer oder ein zu langer Kampf -> kein Kampf, die Zombie-Wache (B.GuardStep) versteckt ihn hinter dem
-- Besitzer bzw. laesst ihn fliehen (0.9).
-- Takte: Entscheid je Hirn-Takt (B.FightStep aus liveRec, VOR der Zombie-Wache); Phasen und Treffer im Kampf-Takt (B.FightTick, OnTick, je
-- fightTickMs 100 ms, nur wenn ein Baer kaempft, ein Gegner-Angriff laeuft oder Gegner nah sind). Treffer NUR nach der Uhr (B.CLIPS, nie das
-- Bild, 0.6); das Bild spielt jeder Client an seiner Kopie (Fx "act", OBERFLAECHE U.PoseAct); die Wirkung am Zombie rechnet der
-- Zombie-Rechner (Fx "hit", shared/BanditsNPCBearFoe.lua B.FoeHurt). Schaden je Treffer aus B.MeleeDamage (11.2, dieselbe Zahl wie im
-- Fenster). Kill-Zaehler (11.5): stirbt ein getroffener Gegner binnen killMs, zaehlt der Schreiber rec.kZ / rec.kB (ein Mal je Gegner).
-- Mehrspieler: Entscheid, Phasen, Lauf und Halt, Uhr, Erfahrung, Ausdauer beim Server; Sicht zum Ziel am Server nur ueber Kacheln (kein
-- CanSee), keine Drehung zum Ziel (faceThisObject nur SP, PLAN_B1E A2). MP ungespielt (F6).
-- Engine-Aufrufe hier (Fundstelle am Aufruf): getX/getY/getZ, isAlive, isProne, getCurrentSquare, isBlockedTo, isWindowTo, CanSee (SP),
-- faceThisObject (SP), isExistInTheWorld, isDead, ZombRand, getTimestampMs, Events.OnTick.Add; Bewegung nur ueber B.MoveTo / B.Hold
-- (server/BanditsNPCBearWorld.lua). Ladefolge: server/ alphabetisch (diese Datei zuerst); fremde Funktionen nur zur Laufzeit ueber B.X.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._fightN = B._fightN or 0          -- kaempfende Baeren (jeder Kampf-Takt neu gezaehlt; Riegel des OnTick)
B._kp = B._kp or {}                 -- Kill-Zaehler (11.5): { { o, id, kind, at }, ... } getroffene Gegner (<= killMax)
B._ftAt = B._ftAt or nil            -- Echtzeit des letzten Kampf-Takts

-- Treffer-Toene je Angriff (gespielt NCBearTest shared/NCBearFight.lua:170-172; Ton-Skripte Vanilla media/scripts/generated/sounds/
-- weapons/sounds_melee_bluntlong.txt, sounds_melee_bladelong.txt, zombies/sounds_zombie_foley.txt). Hoechstens 2 je Angriff.
local SND_MAIN = { swipeL = "SledgehammerHit", swipeR = "SledgehammerHit", slam = "SledgehammerHit", bite = "ZombieBite",
    maul = "ZombieBite" }
local SND_SIDE = "MacheteHit"
local DMG_MAIN = { swipeL = "swipe", swipeR = "swipe", bite = "bite", maul = "maul", slam = "slam" }
local DMG_SIDE = { swipeL = "swipeSide", swipeR = "swipeSide", slam = "slamSide" }
local ALLOW = { swipeL = "swipe", swipeR = "swipe", bite = "bite", maul = "maul", slam = "slam", rear = "rear" }

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function cfg(key, def)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return def end
    return v
end

local function r2(v)
    return math.floor((num(v) or 0) * 100 + 0.5) / 100
end

-- Laufende Kaempfe zaehlen (Sitzungen, hoechstens Zahl der Eintraege). Kein Zaehler, der weglaufen kann.
local function countFights()
    local n = 0
    for _, s in pairs(B._s) do
        if type(s) == "table" and type(s.fight) == "table" then n = n + 1 end
    end
    B._fightN = n
    return n
end

-- Sicht "fst" geaendert? -> EIN B.Touch (4.7).
local function touchFst(rec, s)
    local v = B.FightState(rec)
    if s.fstSent ~= v then
        s.fstSent = v
        B.Touch(rec)
    end
end

-- Halten im Kampf: die Sperre hoechstens je 1 s erneuern (B.Hold ruft setBlockMovement, server/BanditsNPCBearWorld.lua).
local function holdOn(rec, a, s, ms)
    if s.held and num(s.holdAt) ~= nil and ms - s.holdAt >= 0 and ms - s.holdAt < 1000 then return end
    B.Hold(rec, a, true)
    s.holdAt = ms
end

-- ---------------------------------------------------------------------------
-- Leine (2.2.2): Anker und Laenge. follow mit Besitzer auf gleicher Ebene -> der Besitzer; stay/sit -> Heimat; roam -> Heimat mit
-- max(fightLeash, BearRoamRadius + fightLeashRoamPad); sonst die Stelle des Kampfbeginns. players = B.Players() (Server-Liste).
-- ---------------------------------------------------------------------------
local function anchorOf(rec, f, players)
    local leash = cfg("fightLeash", 14)
    local mode = B.ModeOf(rec)
    if mode == "follow" and rec.owner ~= nil then
        local _, e = B.PlayerByKey(rec.owner, players)
        if e ~= nil and math.floor(num(e.z) or 0) == math.floor(num(rec.z) or 0) then return e.x, e.y, leash end
    elseif (mode == "stay" or mode == "sit" or mode == "roam") and rec.hx ~= nil and rec.hy ~= nil then
        if mode == "roam" then
            local rr = B.Opt("BearRoamRadius") + cfg("fightLeashRoamPad", 2)
            if rr > leash then leash = rr end
        end
        return rec.hx + 0.5, rec.hy + 0.5, leash
    end
    return f.sx, f.sy, leash
end

-- Erreicht ihn die Pranke (Treffer, Ankunft)? Wie gespielt (NCBearTest shared/NCBearFight.lua:363-375 canStrike): SP CanSee
-- (a:CanSee(z): Bandits client/BanditUpdate.lua:1203, Empfaenger dort ein Bandit -- am Tier gespielt, GRENZFALL -> nur SP) und Vanillas
-- Kanten-Frage isBlockedTo / isWindowTo (Vanilla client/TimedActions/ISInventoryTransferAction.lua:598; am Server GRENZFALL).
-- a:getCurrentSquare(): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:159; z:getCurrentSquare(): Bandits client/BanditUpdate.lua:574.
local function canStrike(a, o)
    local bs = a:getCurrentSquare()
    local zs = o:getCurrentSquare()
    if bs == nil or zs == nil then return false end
    if B.IsSP() and not a:CanSee(o) then return false end
    if bs ~= zs and (bs:isBlockedTo(zs) or bs:isWindowTo(zs)) then return false end
    return true
end

-- Ist das Ziel noch gueltig? lebt (Bandits server/BanditSave.lua:52), steht in der frischen Gegnerliste (B._foes, je foeScanMs neu -- so
-- fallen auch Banditen heraus, die nicht mehr feindlich sind), gleiche Ebene, innerhalb der Leine. getX/getY/getZ: Bandits
-- client/BanditZombie.lua:69-71.
local function inFoes(id, o)
    local list = B._foes and B._foes[id] or nil
    if type(list) ~= "table" then return false end
    for i = 1, #list do
        if list[i].o == o then return true end
    end
    return false
end

local function tgtOk(rec, a, tgt, ax, ay, leash)
    if type(tgt) ~= "table" or tgt.o == nil then return false end
    local o = tgt.o
    if not o:isAlive() or not inFoes(rec.id, o) then return false end
    if math.floor(o:getZ()) ~= math.floor(a:getZ()) then return false end
    return B.DistXY(ax, ay, o:getX(), o:getY()) <= leash
end

-- Gesperrtes Ziel (steckt fest, ausserhalb der Leine)? f.blocked[oid] = Echtzeit bis (<= fightBlockMax).
local function blockedNow(f, oid, ms)
    local t = f.blocked and num(f.blocked[oid]) or nil
    return t ~= nil and t - ms > 0 and t - ms <= cfg("fightBlockMs", 20000)
end

-- Nachbesserung F2 B3: Ziel in Weite, aber nicht treffbar (Wand, Fenster, Zaun dazwischen -- canStrike falsch) -> nach fightMissMax
-- solchen Faellen (je hoechstens einer je fightMissGapMs) fuer fightMissBlockMs gesperrt. Die Sperre lebt in der Sitzung (s.missBl, ueber
-- diesen Kampf hinaus, Deckel fightBlockMax), sonst finge der naechste Hirn-Takt denselben Kampf neu an. Trifft der Gegner den Baeren
-- (dann steht nichts mehr dazwischen), hebt B.FightUnmiss die Sperre sofort auf (server/BanditsNPCBearHurt.lua).
local function missedNow(s, oid, ms)
    local t = s and s.missBl and num(s.missBl[oid]) or nil
    return t ~= nil and t - ms > 0 and t - ms <= cfg("fightMissBlockMs", 8000)
end

local function missNote(s, f, tgt, ms)
    if type(tgt) ~= "table" or tgt.oid == nil then return false end
    if f.missOid ~= tgt.oid then f.missOid, f.missN, f.missAt = tgt.oid, 0, nil end
    local at = num(f.missAt)
    if at ~= nil and ms - at >= 0 and ms - at < cfg("fightMissGapMs", 750) then return false end
    f.missAt = ms
    f.missN = (num(f.missN) or 0) + 1
    if f.missN < cfg("fightMissMax", 2) then return false end
    if type(s.missBl) ~= "table" then s.missBl, s.missBlN = {}, 0 end
    if s.missBl[tgt.oid] == nil then
        s.missBlN = (num(s.missBlN) or 0) + 1
        if s.missBlN > cfg("fightBlockMax", 32) then s.missBl, s.missBlN = {}, 1 end
    end
    s.missBl[tgt.oid] = ms + cfg("fightMissBlockMs", 8000)
    f.tgt, f.stuckAt, f.missOid, f.missN, f.missAt = nil, nil, nil, 0, nil
    B.Log("fight: target " .. tostring(tgt.oid) .. " is in reach but cannot be struck (wall, window, fence) -- ignored for a while")
    return true
end

function B.FightUnmiss(id, oid)
    local s = id ~= nil and B._s and B._s[id] or nil
    if type(s) == "table" and type(s.missBl) == "table" and oid ~= nil then s.missBl[oid] = nil end
end

local function block(f, oid, ms)
    if type(f.blocked) ~= "table" then f.blocked = {} end
    if f.blocked[oid] == nil then
        f.blockN = (f.blockN or 0) + 1
        if f.blockN > cfg("fightBlockMax", 32) then
            f.blocked = {}
            f.blockN = 1
        end
    end
    f.blocked[oid] = ms + cfg("fightBlockMs", 20000)
end

-- Ziel waehlen (2.2.2): aus B._foes[id] nach Abstand, Banditen um fightBanditBias bevorzugt, nicht gesperrt, innerhalb der Leine; Sicht nur
-- fuer die drei besten (SP CanSee, Bandits client/BanditUpdate.lua:1087 / :1203; am Server ohne Sicht-Frage). Rueckgabe { o, kind, oid } / nil.
local function pickTarget(rec, a, f, ms, ax, ay, leash)
    local list = B._foes and B._foes[rec.id] or nil
    if type(list) ~= "table" or #list == 0 then return nil end
    local bx, by, bz = a:getX(), a:getY(), math.floor(a:getZ())
    local bias = cfg("fightBanditBias", 3)
    local ses = B._s and B._s[rec.id] or nil
    local best = {}
    for i = 1, #list do
        local fo = list[i]
        local o = fo.o
        if o ~= nil and not blockedNow(f, fo.oid, ms) and not missedNow(ses, fo.oid, ms) and o:isAlive()
            and math.floor(o:getZ()) == bz then
            local ox, oy = o:getX(), o:getY()
            if B.DistXY(ax, ay, ox, oy) <= leash then
                local sc = B.DistXY(bx, by, ox, oy)
                if fo.kind == "b" then sc = sc - bias end
                best[#best + 1] = { fo = fo, s = sc }
            elseif fo.oid ~= nil then
                block(f, fo.oid, ms)
            end
        end
    end
    if #best == 0 then return nil end
    if #best > 1 then table.sort(best, function(p, q) return p.s < q.s end) end
    local n = #best
    if n > 3 then n = 3 end
    for i = 1, n do
        local o = best[i].fo.o
        if not B.IsSP() or a:CanSee(o) then return { o = o, kind = best[i].fo.kind, oid = best[i].fo.oid } end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Laute: Knurren zu Kampfbeginn (Halbstark/kraeftig; ausgewachsen, wenn kein Aufrichten kommt), Alltags-Schnauben (Kevin ENT:78, alte
-- Werte NCBearTest shared/NCBearFight.lua:1459-1489). Nur Fx -- den Ton spielt jeder Client an seiner Kopie (playBreedSound, OBERFLAECHE).
-- ZombRand(n): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:25. getX/getY am Tier: Vanilla ButcheringUtil.lua:575-576.
-- ---------------------------------------------------------------------------
-- Nachbesserung F2 B1: hoechstens ein Knurren je growlCdMs und Baer (s.growlAt), auch wenn Kaempfe kurz hintereinander beginnen.
local function growl(rec, a, ms)
    local s = B._s and B._s[rec.id] or nil
    if type(s) == "table" then
        local at = num(s.growlAt)
        if at ~= nil and ms - at >= 0 and ms - at < cfg("growlCdMs", 10000) then return end
        s.growlAt = ms
    end
    local bx, by = a:getX(), a:getY()
    B.Fx("growl", { id = rec.id, n = 1 + ZombRand(3), bx = bx, by = by }, bx, by)
end

local function huff(rec, a, s, ms)
    if rec.body ~= "big" or rec.down ~= nil or type(s.fight) == "table" then return end
    local span = (cfg("huffMinS", 90) + cfg("huffSpreadS", 150)) * 1000
    local at = num(s.huffAt)
    if at == nil or at - ms > span then
        s.huffAt = ms + cfg("huffMinS", 90) * 1000          -- erster Abstand fest (kein Wurf), danach mit Zufall
        return
    end
    if ms < at then return end
    s.huffAt = ms + (cfg("huffMinS", 90) + ZombRand(math.floor(cfg("huffSpreadS", 150)) + 1)) * 1000
    local bx, by = a:getX(), a:getY()
    B.Fx("huff", { id = rec.id, soft = true, bx = bx, by = by }, bx, by)
end

-- ---------------------------------------------------------------------------
-- Kampfbeginn (2.2.2). Zombie-Wache aus (Sicht hide), Sitz aus (erst aufstehen: f.readyAt = jetzt + B.StandMs), Laut. Rueckgabe: true.
-- ---------------------------------------------------------------------------
local function begin(rec, a, s, st, tgt, ms)
    local f = { ph = "approach", t0 = ms, startAt = ms, tgt = tgt, first = true, blocked = {}, blockN = 0, stuckN = 0,
                sx = a:getX(), sy = a:getY() }
    if type(s.g) == "table" and s.g.on == true then s.g.on = nil end
    local stand = nil
    if s.sat == true then
        s.sat, s.satAt = nil, nil
        stand = ms + B.StandMs()
    end
    local su = num(s.standUntil)
    if su ~= nil and su - ms > 0 and su - ms <= B.StandMs() and (stand == nil or su > stand) then stand = su end
    s.standUntil = nil
    f.readyAt = stand
    s.fight = f
    countFights()
    local allow = B.FightStageOf(st)
    local rearReady = allow.rear and (s.rearAt == nil or ms - s.rearAt < 0 or ms - s.rearAt >= cfg("rearCdMs", 120000))
    if not rearReady then
        growl(rec, a, ms)
        f.growled = true
    end
    touchFst(rec, s)
    B.Log("fight: " .. tostring(rec.id) .. " (" .. tostring(allow.stage) .. ") attacks a " .. tostring(tgt.kind) .. " (outfit "
        .. tostring(tgt.oid) .. ")")
    return true
end

-- ---------------------------------------------------------------------------
-- Kampf-Entscheid je Hirn-Takt (2.2.1, R1-R10; aus liveRec, server/BanditsNPCBearServer.lua, VOR B.GuardStep). Rueckgabe true = dieser
-- Takt ist erledigt (der Kampf-Takt fuehrt). false -> Zombie-Wache / Befehl wie bisher (Verstecken, Fliehen, Folgen ...).
-- ---------------------------------------------------------------------------
function B.FightStep(rec, a, env, ms, players)
    if type(rec) ~= "table" or a == nil or rec.st ~= "tame" then return false end
    ms = num(ms) or getTimestampMs()             -- Vanilla server/Foraging/forageServer.lua:456
    local s = B.Ses(rec.id)
    local st = B.StatsOf(rec)
    local f = s.fight
    local foes = B._foes and B._foes[rec.id] or nil
    local hpMax = num(st.hpMax) or 1
    local hpPts = (num(rec.hp) or 1) * hpMax
    local fleeHp, hys = B.FleeHp(B.FoeKinds(rec.id))
    if fleeHp <= 0 or hpPts >= fleeHp + hys then
        s.fleeOn = nil
        s.fleeSaid = nil
    end
    local restOver = num(s.restAt) ~= nil and (ms - s.restAt < 0 or ms - s.restAt >= cfg("fightRestMaxMs", 30000))
    local ru = num(s.restUntil)
    -- R8 (Nachbesserung F2 B10, gebaut nach Empfehlung -- Frage an Kevin): die Pause kommt nur nach fightMaxMs OHNE eigenen Treffer
    -- (f.hitLast, sonst seit Kampfbeginn); wer trifft, kaempft weiter (Muedigkeit regelt R7 ueber die Ausdauer)
    local longOver = (ru ~= nil and ru - ms > 0 and ru - ms <= cfg("fightRestMs", 20000))
        or (type(f) == "table" and ms - (num(f.hitLast) or f.startAt) >= cfg("fightMaxMs", 90000))
    local o = env and env.owner or nil
    local carNear = o ~= nil and o.car == true and (num(o.dist) or 999) <= B.Opt("BearRideDistance")
    local d = B.FightDecide({
        st = rec.st, body = B.BodyKind(a) or rec.body, s = st.s, passive = rec.passive == true, down = rec.down ~= nil,
        ride = rec.ride ~= nil, hpPts = hpPts, fleeHp = fleeHp, fleeHys = hys, fleeOn = s.fleeOn == true, sta = num(s.sta) or 1,
        resting = s.resting == true, restOver = restOver, longOver = longOver, foe = type(foes) == "table" and #foes > 0,
        ownerCarNear = carNear, follow = B.ModeOf(rec) == "follow", capFull = type(f) ~= "table" and countFights() >= cfg("fightMax", 4),
    })
    if d.why == "hurt" then s.fleeOn = true end
    if d.why == "breath" then
        if s.resting ~= true then s.resting, s.restAt = true, ms end
    else
        s.resting, s.restAt = nil, nil
    end
    if d.act ~= "fight" then
        if type(f) == "table" then B.FightDrop(rec.id, d.why) end
        s.fstNow = nil
        if d.act == "retreat" or d.act == "rest" then s.fstNow = d.act end
        touchFst(rec, s)
        huff(rec, a, s, ms)
        return false
    end
    s.fstNow = nil
    if type(f) == "table" then
        touchFst(rec, s)
        return true
    end
    local ax, ay = a:getX(), a:getY()
    local tmp = { sx = ax, sy = ay, blocked = {} }
    local bx, by, leash = anchorOf(rec, tmp, players or B.Players())
    -- Nachbesserung F2 B1: steht der Baer selbst nicht mindestens fightLeashPad innerhalb der Leine, beginnt kein Kampf (der Kampf-Takt
    -- beendete ihn sofort mit "leash", und Folgen kaeme nie an die Reihe) -- erst holen ihn Folgen bzw. die Zombie-Wache zurueck
    if B.DistXY(bx, by, ax, ay) > leash - cfg("fightLeashPad", 2) then
        touchFst(rec, s)
        huff(rec, a, s, ms)
        return false
    end
    local tgt = pickTarget(rec, a, tmp, ms, bx, by, leash)
    if tgt == nil then
        touchFst(rec, s)
        huff(rec, a, s, ms)
        return false
    end
    return begin(rec, a, s, st, tgt, ms)
end

-- ---------------------------------------------------------------------------
-- Kampfende (Hold los, Zaehler, Sicht). why "long" -> Pause fightRestMs (R8). Kills seit dem Beginn -> EIN Commit (Spiegel).
-- ---------------------------------------------------------------------------
function B.FightDrop(id, why)
    if id == nil then return end
    local s = B._s and B._s[id] or nil
    if type(s) ~= "table" or type(s.fight) ~= "table" then return end
    s.fight = nil
    local ms = getTimestampMs()
    if why == "long" then s.restUntil = ms + cfg("fightRestMs", 20000) end
    local reg = B.Reg and B.Reg() or nil
    local rec = reg and reg.cubs[id] or nil
    local a = s.obj
    if rec ~= nil and a ~= nil and s.held then B.Hold(rec, a, false) end
    countFights()
    if rec ~= nil then
        if s.killDirty then
            s.killDirty = nil
            B.Commit(rec)
        end
        touchFst(rec, s)
    end
    B.Log("fight: " .. tostring(id) .. " ends (" .. tostring(why) .. ")")
end

-- Zustand fuer die Sicht (4.7): "fight" (Kampf laeuft), "retreat" (passiv / zu wenig Leben / Deckel), "rest" (verschnauft) oder nil.
function B.FightState(rec)
    if type(rec) ~= "table" or rec.down ~= nil then return nil end      -- Nachbesserung F2 B5: am Boden zaehlt nur dn
    local s = B._s and B._s[rec.id] or nil
    if type(s) ~= "table" then return nil end
    if type(s.fight) == "table" then return "fight" end
    return s.fstNow
end

-- Haelt der Kampf ihn gerade still (Angriff, Pause, Suchen, Aufstehen)?
function B.FightHolds(rec, ms)
    local s = type(rec) == "table" and B._s[rec.id] or nil
    local f = s and s.fight or nil
    if type(f) ~= "table" then return false end
    return f.ph ~= "approach" or f.readyAt ~= nil
end

-- Laerm im Kampf (2.2.5): aus B.CalmAnswer (server/BanditsNPCBearGuard.lua) VOR dessen Ersatzweg. Am Boden oder Angriff/Pause/Suchen ->
-- nur halten (keine Ruhefrist); Anlauf -> den Kampf-Laufbefehl sofort neu. Rueckgabe true = erledigt.
function B.FightCalm(rec, a, ms)
    if type(rec) ~= "table" or a == nil then return false end
    if rec.down ~= nil then
        B.Hold(rec, a, true)
        return true
    end
    local s = B._s[rec.id]
    local f = s and s.fight or nil
    if type(f) ~= "table" then return false end
    if f.ph == "approach" and f.readyAt == nil and f.mx ~= nil and f.my ~= nil then
        B.MoveTo(rec, a, f.mx, f.my, rec.z, { force = true, watch = false })
        return true
    end
    B.Hold(rec, a, true)
    return true
end

-- Probeweg (im Spiel nie gerufen, das Uebernahme-Skript prueft das: Regel probeweg): der naechste Angriff ist act, einmal -- wenn die
-- Stufe ihn kann.
function B.FightForce(rec, act)
    if type(rec) ~= "table" or rec.st ~= "tame" or type(act) ~= "string" or ALLOW[act] == nil then return false end
    local allow = B.FightStageOf(B.StatsOf(rec))
    if allow[ALLOW[act]] ~= true then return false end
    B.Ses(rec.id).force = act
    return true
end

-- ---------------------------------------------------------------------------
-- Kill-Zaehler (11.5): getroffene Gegner merken; stirbt einer binnen killMs (isAlive falsch: Bandits server/BanditSave.lua:52), zaehlt der
-- Eintrag rec.kZ (Zombie) bzw. rec.kB (Bandit) EINMAL (Deckel killTop). Im Einzelspieler stirbt der Zombie schon im selben Aufruf
-- (B.Fx -> B.FoeHurt -> Kill), im Mehrspieler sieht der Server den Tod an seinem Zombie-Objekt. Nie NPC-Crew-Figuren oder Neutrale (nur
-- Ziele aus B._foes werden getroffen). Ein Tod durch jemand anderen binnen killMs zaehlt mit (ehrliche Grenze, Testpunkt).
-- ---------------------------------------------------------------------------
local function killNote(o, id, kind, ms)
    local kp = B._kp
    for i = 1, #kp do
        if kp[i].o == o then
            kp[i].id, kp[i].kind, kp[i].at = id, kind, ms
            return
        end
    end
    if #kp >= cfg("killMax", 32) then table.remove(kp, 1) end
    kp[#kp + 1] = { o = o, id = id, kind = kind, at = ms }
end

local function killTick(ms)
    local kp = B._kp
    if #kp == 0 then return end
    local reg = B.Reg and B.Reg() or nil
    local keep = {}
    for i = 1, #kp do
        local e = kp[i]
        if not e.o:isAlive() then
            local rec = reg and reg.cubs[e.id] or nil
            if rec ~= nil and (rec.st == "tame" or rec.st == "missing") then
                local key = "kZ"
                if e.kind == "b" then key = "kB" end
                local v = math.floor(num(rec[key]) or 0) + 1
                local top = cfg("killTop", 999999)
                if v > top then v = top end
                rec[key] = v
                local s = B._s[e.id]
                if s ~= nil then s.killDirty = true end
                B.Touch(rec)
                B.Log("fight: " .. tostring(e.id) .. " killed a " .. tostring(e.kind) .. " (" .. key .. " " .. tostring(v) .. ")")
            end
        elseif ms - e.at >= 0 and ms - e.at < cfg("killMs", 2000) then
            keep[#keep + 1] = e
        end
    end
    B._kp = keep
end

-- ---------------------------------------------------------------------------
-- Treffer (2.2.4) bei hitAt, genau einmal. Hauptziel (Weite + 0,25) und Nebenziele im Kegel um die Linie Baer -> Hauptziel (Hiebe:
-- stage.side, Doppelschlag: slamMax), hoechstens hitCap Ziele und sightMax Sicht-Pruefungen. Umwerfen mit st.knockPct (ZombRand beim
-- Schreiber), toedliche Treffer werden vorher umgeworfen (kk, knockKill). Je Ziel Fx "hit" (die Wirkung macht der Zombie-Rechner), einmal
-- je Angriff mit Treffer B.OnHitDealt (Kaempfen +xpHitDealt). Schaden aus B.MeleeDamage (11.2).
-- ---------------------------------------------------------------------------
-- Liegt (dx, dy) im Kegel +-half Grad um (mx, my)? Ueber den Kosinus (math.cos / math.pi wie server/BanditsNPCBearWorld.lua B.MoveTo).
local function inCone(mx, my, dx, dy, half)
    local lm = math.sqrt(mx * mx + my * my)
    local ld = math.sqrt(dx * dx + dy * dy)
    if lm < 0.001 or ld < 0.001 then return true end
    return (mx * dx + my * dy) / (lm * ld) >= math.cos(half * math.pi / 180) - 0.000001
end

local function strike(rec, a, f, st, ms)
    local act = f.act
    local tgt = f.tgt
    if DMG_MAIN[act] == nil or type(tgt) ~= "table" or tgt.o == nil then return 0 end
    local md = B.MeleeDamage(rec, st)
    if md == nil then return 0 end
    local allow = B.FightStageOf(st)
    local sz = num(st.sz) or 1
    local reach = B.FightReach(act, sz)
    local half = B.FightHalf(act)
    local bx, by, bz = a:getX(), a:getY(), math.floor(a:getZ())
    local main = tgt.o
    local mx, my = main:getX() - bx, main:getY() - by
    local hits, checks = {}, 0
    local sightMax = cfg("sightMax", 12)
    local cap = cfg("hitCap", 6)
    local wall = false
    if main:isAlive() and math.floor(main:getZ()) == bz and math.sqrt(mx * mx + my * my) <= reach + 0.25 then
        checks = checks + 1
        if canStrike(a, main) then hits[1] = { o = main, kind = tgt.kind, oid = tgt.oid, main = true } else wall = true end
    end
    local side = 0
    if act == "swipeL" or act == "swipeR" then side = allow.side elseif act == "slam" then side = cfg("slamMax", 5) end
    local list = B._foes and B._foes[rec.id] or nil
    if side > 0 and type(list) == "table" then
        local n = 0
        for i = 1, #list do
            if n >= side or #hits >= cap or checks >= sightMax then break end
            local o = list[i].o
            if o ~= nil and o ~= main and o:isAlive() and math.floor(o:getZ()) == bz then
                local dx, dy = o:getX() - bx, o:getY() - by
                if math.sqrt(dx * dx + dy * dy) <= reach and inCone(mx, my, dx, dy, half) then
                    checks = checks + 1
                    if canStrike(a, o) then
                        hits[#hits + 1] = { o = o, kind = list[i].kind, oid = list[i].oid, main = false }
                        n = n + 1
                    end
                end
            end
        end
    end
    if #hits == 0 then return 0, wall end
    local kmode = B.FightKnockMode(act)
    local kpct = num(allow.knockPct) or 0
    local kk = nil
    if kmode ~= nil and kpct > 0 then kk = kmode end
    for i = 1, #hits do
        local h = hits[i]
        local dmg = md[DMG_MAIN[act]]
        if not h.main then dmg = md[DMG_SIDE[act] or DMG_MAIN[act]] end
        local knock = nil
        if kk ~= nil and ZombRand(100) < kpct then knock = kk end
        local snd = nil
        if i <= 2 then
            snd = SND_MAIN[act]
            if not h.main and DMG_SIDE[act] ~= nil then snd = SND_SIDE end
        end
        B.Fx("hit", { id = rec.id, oid = h.oid, zx = h.o:getX(), zy = h.o:getY(), zz = bz, bx = bx, by = by, dmg = r2(num(dmg) or 0),
                      knock = knock, kk = kk, main = h.main, snd = snd, kind = h.kind }, bx, by)
        killNote(h.o, rec.id, h.kind, ms)
    end
    B.OnHitDealt(rec, ms)
    return #hits, wall
end

-- ---------------------------------------------------------------------------
-- Ein Angriff beginnt (2.2.3 "act"): halten, SP zum Ziel drehen (a:faceThisObject(z): Vanilla shared/TimedActions/Animals/ISPetAnimal.lua:17,
-- Tier -> Figur; gespielt NCBearTest shared/NCBearFight.lua:428; im MP keine Drehung), Fx "act" (Bild an jeder Kopie), Ausdauer -
-- staAttackCost (B.StaUse), Kondition +xpConFight. Uhr: hitAt = Dauer x hitPc, endAt = Dauer (B.ClipMs / B.ClipHitMs, Koerper "big").
-- ---------------------------------------------------------------------------
local function enterAct(rec, a, s, f, act, ms)
    local dur = B.ClipMs(act, 0, "big") or 1500
    local hit = B.ClipHitMs(act, "big")
    f.ph, f.act, f.t0, f.endAt, f.hitDone = "act", act, ms, ms + dur, false
    f.hitAt = nil
    if hit ~= nil then f.hitAt = ms + hit end
    f.last = act
    if act == "slam" then f.slamAt = ms end
    if act == "rear" then s.rearAt = ms end
    if f.first and not f.growled and act ~= "rear" then growl(rec, a, ms) end
    f.first, f.growled = false, true
    s.held = nil
    holdOn(rec, a, s, ms)
    local o = f.tgt and f.tgt.o or nil
    if B.IsSP() and o ~= nil then a:faceThisObject(o) end
    local bx, by = a:getX(), a:getY()
    B.Fx("act", { id = rec.id, act = act, bx = bx, by = by }, bx, by)
    if act ~= "rear" then
        B.StaUse(rec, cfg("staAttackCost", 3), ms)
        B.SkillAdd(rec, "con", cfg("xpConFight", 1), ms)
    end
end

-- Welcher Angriff jetzt? B.FightForce (Probeweg) geht vor, sobald er in Weite ist. Sonst B.FightChoose (nur in Weite bzw. als erster
-- Angriff fuer das Aufrichten; die Wuerfe nur dann). Nachbarn fuer den Doppelschlag: weitere Gegner in slamReach x sz im Kegel.
local function choose(rec, s, f, st, o, d, ms)
    local allow = B.FightStageOf(st)
    local sz = num(st.sz) or 1
    local force = s.force
    if force ~= nil then
        if allow[ALLOW[force] or ""] ~= true then
            s.force = nil
        elseif force == "rear" or d <= B.FightReach(force, sz) then
            s.force = nil
            return force
        else
            return nil
        end
    end
    local maxR = B.FightReach("slam", sz)
    local r1 = B.FightReach("swipeL", sz)
    if r1 > maxR then maxR = r1 end
    local rearTry = allow.rear and f.first == true
    if d > maxR and not rearTry then return nil end
    local slamN = 0
    local list = B._foes and B._foes[rec.id] or nil
    if allow.slam and type(list) == "table" then
        local a = s.obj
        local bx, by = a:getX(), a:getY()
        local mx, my = o:getX() - bx, o:getY() - by
        for i = 1, #list do
            local x = list[i].o
            if x ~= nil and x ~= o then
                local dx, dy = x:getX() - bx, x:getY() - by
                if math.sqrt(dx * dx + dy * dy) <= maxR and inCone(mx, my, dx, dy, B.FightHalf("slam")) then slamN = slamN + 1 end
            end
        end
    end
    return B.FightChoose({
        allow = allow, last = f.last, prone = o:isProne(), d = d, sz = sz,
        slamReady = f.slamAt == nil or ms - f.slamAt < 0 or ms - f.slamAt >= cfg("slamCdMs", 10000), slamN = slamN,
        rearReady = rearTry and (s.rearAt == nil or ms - s.rearAt < 0 or ms - s.rearAt >= cfg("rearCdMs", 120000)),
        first = f.first, rnd = ZombRand(100), rnd2 = ZombRand(100),
    })
end

-- Anlauf (2.2.3 "approach"): bis fightArrive x sz vor das Ziel rennen (B.MoveTo, Drossel fightRepathMs); kein Fortschritt in fightStuckMs ->
-- Ziel sperren, naechstes; fightStuckMax Sperren -> Ende.
local function approach(rec, a, s, f, st, ms, ax, ay, leash)
    local tgt = f.tgt
    if not tgtOk(rec, a, tgt, ax, ay, leash) then
        tgt = pickTarget(rec, a, f, ms, ax, ay, leash)
        f.tgt, f.stuckAt = tgt, nil
        if tgt == nil then
            f.ph, f.t0 = "seek", ms
            s.held = nil
            holdOn(rec, a, s, ms)
            return
        end
    end
    local o = tgt.o
    local bx, by = a:getX(), a:getY()
    local ox, oy = o:getX(), o:getY()
    local d = B.DistXY(bx, by, ox, oy)
    -- Nachbesserung F2 B3: in Weite, aber nicht treffbar (Wand, Fenster, Zaun) -> kein Luftschlag; nach fightMissMax Faellen gesperrt
    local sz = num(st.sz) or 1
    local rMax = B.FightReach("slam", sz)
    local r1 = B.FightReach("swipeL", sz)
    if r1 > rMax then rMax = r1 end
    if d <= rMax + 0.25 and not canStrike(a, o) then
        missNote(s, f, tgt, ms)
        return
    end
    local act = choose(rec, s, f, st, o, d, ms)
    if act ~= nil then
        enterAct(rec, a, s, f, act, ms)
        return
    end
    local tx, ty = ox, oy
    if d > 0.001 then
        local back = cfg("fightArrive", 1.1) * (num(st.sz) or 1)
        tx, ty = ox - (ox - bx) / d * back, oy - (oy - by) / d * back
    end
    f.mx, f.my = tx, ty
    B.MoveTo(rec, a, tx, ty, rec.z, { minMs = cfg("fightRepathMs", 750), watch = false })
    if f.stuckAt == nil or ms - f.stuckAt < 0 then
        f.stuckAt, f.stuckD = ms, d
    elseif ms - f.stuckAt >= cfg("fightStuckMs", 3000) then
        if (num(f.stuckD) or d) - d < cfg("fightStuckGain", 0.5) then
            if tgt.oid ~= nil then block(f, tgt.oid, ms) end
            f.stuckN = (f.stuckN or 0) + 1
            f.tgt = nil
            if f.stuckN >= cfg("fightStuckMax", 3) then
                B.FightDrop(rec.id, "stuck")
                return
            end
        end
        f.stuckAt, f.stuckD = ms, d
    end
end

-- Ein Kampf-Takt eines Baeren (2.2.3).
local function tickBear(rec, a, s, f, ms, players)
    local ra = num(f.readyAt)
    if ra ~= nil then
        if ra - ms > 0 and ra - ms <= 10000 then
            holdOn(rec, a, s, ms)
            return
        end
        f.readyAt = nil
    end
    local ax, ay, leash = anchorOf(rec, f, players)
    if B.DistXY(ax, ay, a:getX(), a:getY()) > leash then
        B.FightDrop(rec.id, "leash")
        return
    end
    local st = B.StatsOf(rec)
    if f.ph == "act" then
        holdOn(rec, a, s, ms)
        if not f.hitDone and f.hitAt ~= nil and ms >= f.hitAt then
            f.hitDone = true
            local n, wall = strike(rec, a, f, st, ms)
            if n > 0 then
                f.hitLast, f.missOid, f.missN, f.missAt = ms, nil, 0, nil
            elseif wall then
                missNote(s, f, f.tgt, ms)
            end
        end
        if ms >= f.endAt or ms - f.t0 < 0 then f.ph, f.t0 = "pause", ms end
        return
    end
    if f.ph == "pause" then
        holdOn(rec, a, s, ms)
        if ms - f.t0 >= 0 and ms - f.t0 < cfg("fightPauseMs", 350) then return end
        f.ph, f.t0 = "approach", ms
    end
    if f.ph == "seek" then
        holdOn(rec, a, s, ms)
        local tgt = pickTarget(rec, a, f, ms, ax, ay, leash)
        if tgt == nil then
            if ms - f.t0 < 0 or ms - f.t0 >= cfg("fightSeekMs", 3000) then B.FightDrop(rec.id, "seek") end
            return
        end
        f.tgt, f.ph, f.t0, f.stuckAt = tgt, "approach", ms, nil
    end
    approach(rec, a, s, f, st, ms, ax, ay, leash)
end

-- ---------------------------------------------------------------------------
-- Kampf-Takt (0.5): je fightTickMs. Suche (gedrosselt foeScanMs), Gegner-Angriffe, die Phasen jedes kaempfenden Baeren, Kill-Zaehler.
-- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; isDead am Tier: server/Traps/STrapGlobalObject.lua:238.
-- ---------------------------------------------------------------------------
local function tickBody()
    local ms = getTimestampMs()
    if B._ftAt ~= nil and ms - B._ftAt >= 0 and ms - B._ftAt < cfg("fightTickMs", 100) then return end
    B._ftAt = ms
    local reg = B.Reg and B.Reg() or nil
    if not reg then return end
    local n = countFights()
    if n > 0 or (B._foeN or 0) > 0 then B.FoeScan(B._fightLive, ms, false) end
    if B.FoeAttackTick then B.FoeAttackTick(ms) end
    if n > 0 then
        local ids = {}
        for id, s in pairs(B._s) do
            if type(s) == "table" and type(s.fight) == "table" then ids[#ids + 1] = id end
        end
        local players = nil
        for i = 1, #ids do
            local id = ids[i]
            local s = B._s[id]
            local f = s and s.fight or nil
            if type(f) == "table" then
                local rec = reg.cubs[id]
                local a = s.obj
                if rec == nil or rec.st ~= "tame" or rec.ride ~= nil or rec.down ~= nil or a == nil or not a:isExistInTheWorld()
                    or a:isDead() then
                    B.FightDrop(id, "gone")
                else
                    if players == nil then players = B.Players() end
                    tickBear(rec, a, s, f, ms, players)
                end
            end
        end
    end
    killTick(ms)
end

-- pcall um EIGENEN Code (wie B.BrainTick): ein Fehler kommt laut, aber gedrosselt (B.ErrEvery). pcall ist eine Lua-Grundfunktion.
function B.FightTick()
    local ok, err = pcall(tickBody)
    if not ok then B.ErrEvery("fight", 60000, "fight tick: " .. tostring(err)) end
end

-- Sicht (4.7, 11.2, 11.5, 11.7) -- aus viewEntry, nur gezaehmt/vermisst: fst (Kampfzustand), mdmg / mdmgB / mdmgM / mdmgS / mdmgF (Schaden
-- je Treffer, Groessen-Anteil, Kaempfen-Bonus %), kZ / kB (Kills), fleeP (Flucht-Schwelle in Lebenspunkten, aufgerundet; fehlt = nie).
function B.FightView(rec, t, ms)
    if type(rec) ~= "table" or type(t) ~= "table" then return end
    if rec.st == "tame" then t.fst = B.FightState(rec) end
    local md = B.MeleeDamage(rec)
    if md ~= nil then
        t.mdmg = r2(md.swipe)
        if md.bite ~= nil then t.mdmgB = r2(md.bite) end
        if md.maul ~= nil then t.mdmgM = r2(md.maul) end
        t.mdmgS = r2(md.size)
        t.mdmgF = B.Round1(md.fgt)
    end
    t.kZ = math.floor(num(rec.kZ) or 0)
    t.kB = math.floor(num(rec.kB) or 0)
    local fleeHp = B.FleeHp(B.FoeKinds(rec.id))
    if fleeHp > 0 then t.fleeP = math.ceil(fleeHp - 0.000001) end
end

-- Events.OnTick.Add: Vanilla server/Foraging/forageServer.lua:502. Je Bild nur ein paar Zahlenvergleiche; Arbeit nur mit Kampf, Gegnern
-- in der Naehe, laufenden Gegner-Angriffen oder offenen Kill-Pruefungen. Ueber eine kleine Huelle (spaeter ersetzte B.FightTick gilt).
Events.OnTick.Add(function()
    if (B._fightN or 0) > 0 or (B._foeN or 0) > 0 or #(B._fa or {}) > 0 or #B._kp > 0 then B.FightTick() end
end)
