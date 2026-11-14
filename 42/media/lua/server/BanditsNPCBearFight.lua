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
-- Lauf baer-kampf (PLAN_KAMPF.md 2.1-2.4, 2.7, 2.8; Kevin 13.11. ~23:00 Punkte 1-7, begleiter/ENTSCHEIDUNGEN.md):
--   K1 Aufrichten IMMER beim ersten Kontakt (EIN Entscheid je Kampf in begin, f.rearWant; Pause rearCdMs bleibt; Gegner schon bis rearDist
--      dran -> sofort Angriff). K2 Anlauf AUF die (vorhergesagte) Lage, Liegende und Fallende werden zerfleischt (B.FoePosture, Foe.lua),
--      "steckt fest" nur ausser Weite, die Sperre lebt in der Sitzung (s.fBlk). K3 Vorhalt, Laufbefehl nur bei Wanderung / Alter, Angriff
--      sobald der Abstand zum Trefferzeitpunkt in Weite ist, Ausfallschritt im Schlag, Zielwechsel mit Hysterese, Pause nach dem Kill.
--   K4 Sprint-Schub NUR im Anlauf und beim Leinen-Sprint (B.FightMoveTick, je Bild, nur Einzelspieler), danach ruhig zurueck (s.calmBack).
--   K7 Sicht fuer bis zu sightMax Kandidaten, Leine 25, Leinen-Abbruch -> Sprint zum Besitzer (s.leashRun, server/BanditsNPCBearFollow.lua).
--   K8 Kampf-Log je Entscheidung (B.LogEvery, nur mit dem Diagnose-Schalter B.LogActive).
--   Neu am Tier: a:setX(Zahl) / a:setY(Zahl) nur in moveBear (Vanilla server/ClientCommands.lua:895-896, shared/Definitions/animal/
--   ButcheringUtil.lua:575-576; Uebernahme-Regel setXY). Kachelwechsel nur mit B.FoeStepOk (shared/BanditsNPCBearFoe.lua, ZOMBIES).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._fightN = B._fightN or 0          -- kaempfende Baeren (jeder Kampf-Takt neu gezaehlt; Riegel des OnTick)
B._kp = B._kp or {}                 -- Kill-Zaehler (11.5): { { o, id, kind, at }, ... } getroffene Gegner (<= killMax)
B._ftAt = B._ftAt or nil            -- Echtzeit des letzten Kampf-Takts
B._mvOn = B._mvOn or false          -- Lauf baer-kampf: Bewegungs-Takt je Bild an (Kampf / Leinen-Sprint, nur SP; B.FightMoveTick)

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

-- Lauf baer-kampf (PLAN_KAMPF.md 2.8, K8): Kampf-Log hinter dem Diagnose-Schalter (B.LogActive), je Schluessel hoechstens je fightLogMs (B.LogEvery,
-- shared/BanditsNPCBear.lua). Wer eine Zeile baut, fragt vorher logOn() -- ohne Schalter kein Text, keine Uhr, nichts je Bild.
local function logOn()
    return B.LogActive ~= nil and B.LogActive() == true
end

local function logE(key, msg)
    if B.LogEvery then B.LogEvery(key, cfg("fightLogMs", 1500), msg) else B.Log(msg) end
end

local function r1(v)
    return math.floor((num(v) or 0) * 10 + 0.5) / 10
end

-- Lauftempo des Koerpers in Kacheln/s wie B.MoveTo (B.BodyNum mit dem Aussehen, shared/BanditsNPCBearStats.lua; grosser Koerper 3,17
-- gemessen, kampf/werkzeug_plan/tempo_ausgabe.txt). Nur je Kampf-Takt, nie je Bild (B.LookNow fragt das Tier).
local function runSpeedOf(rec)
    local look = nil
    if B.LookNow then look = B.LookNow(rec) end
    local v = nil
    if B.BodyNum then v = num(B.BodyNum(rec.body, "runSpeed", 1, look)) end
    if v == nil or v <= 0 then v = cfg("runSpeedBig", 3.17) end
    return v
end

-- Sprint-Faktor des Koerpers (K4): nur im Einzelspieler (PLAN_KAMPF.md 6), sonst 0 (B.FightSprintK, shared/BanditsNPCBearFightRules.lua).
local function sprintK(rec)
    if not B.IsSP() or B.FightSprintK == nil then return 0 end
    return B.FightSprintK(runSpeedOf(rec))
end

-- Tempo, mit dem der Baer im Anlauf rechnet (Vorhalt): Sprint, wenn an, sonst das Lauftempo.
local function chaseSpeed(rec, k)
    local v = runSpeedOf(rec)
    if (num(k) or 0) > 0 then v = v * (1 + k) end
    return v
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
    local leash = cfg("fightLeash", 25)                -- Nachbesserung C7: Rueckfall = Kevins Wert 25 (K7), nicht mehr 14
    local mode = B.ModeOf(rec)
    if mode == "follow" and rec.owner ~= nil then
        local _, e = B.PlayerByKey(rec.owner, players)
        if e ~= nil and math.floor(num(e.z) or 0) == math.floor(num(rec.z) or 0) then return e.x, e.y, leash end
    elseif (mode == "stay" or mode == "sit" or mode == "roam") and rec.hx ~= nil and rec.hy ~= nil then
        if mode == "roam" then
            local rr = cfg("roamRadius", 12) + cfg("fightLeashRoamPad", 2)   -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3): fester Wert
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
    return t ~= nil and t - ms > 0 and t - ms <= cfg("fightBlockLongMs", 120000)
end

-- Nachbesserung (kampf/NACHBESSERUNG.md C1): wird DASSELBE Ziel wieder gesperrt (Zaun, steckt fest), dauert die Sperre doppelt so lang wie die
-- letzte (Grundfrist x 2^(n-1), hoechstens fightBlockLongMs) -- sonst rannte er alle 8 s wieder an denselben Zaun. Nach fightBlockForgetMs ohne
-- Sperre zaehlt er neu; beisst ihn das Ziel (B.FightUnmiss), faellt alles weg. s.blkK[oid] = { n, at }, Deckel fightBlockMax wie s.missBl.
local function blockSpan(s, oid, base, ms)
    if type(s.blkK) ~= "table" then s.blkK, s.blkKN = {}, 0 end
    local e = s.blkK[oid]
    if e == nil then
        s.blkKN = (num(s.blkKN) or 0) + 1
        if s.blkKN > cfg("fightBlockMax", 32) then s.blkK, s.blkKN = {}, 1 end
        e = { n = 0, at = ms }
        s.blkK[oid] = e
    elseif ms - e.at < 0 or ms - e.at > cfg("fightBlockForgetMs", 300000) then
        e.n = 0
    end
    e.n = e.n + 1
    e.at = ms
    local cap = cfg("fightBlockLongMs", 120000)
    local span = base
    for _ = 2, e.n do
        span = span * 2
        if span >= cap then break end
    end
    if span > cap then span = cap end
    return span, e.n
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
    local span, rep = blockSpan(s, tgt.oid, cfg("fightMissBlockMs", 8000), ms)
    s.missBl[tgt.oid] = ms + span
    f.tgt, f.stuckAt, f.missOid, f.missN, f.missAt = nil, nil, nil, 0, nil
    B.Log("fight: target " .. tostring(tgt.oid) .. " is in reach but cannot be struck (wall, window, fence) -- ignored for "
        .. tostring(math.floor(span / 1000)) .. " s (" .. tostring(rep) .. ". time)")
    return true
end

-- Der Gegner traf den Baeren (server/BanditsNPCBearHurt.lua): nichts steht mehr dazwischen -> Sperren "kein Luftschlag" UND (Nachbesserung C1)
-- "steckt fest" fallen weg, die Wiederholungs-Zaehlung auch -- er wehrt sich sofort.
function B.FightUnmiss(id, oid)
    local s = id ~= nil and B._s and B._s[id] or nil
    if type(s) ~= "table" or oid == nil then return end
    if type(s.missBl) == "table" then s.missBl[oid] = nil end
    if type(s.fBlk) == "table" then s.fBlk[oid] = nil end
    if type(s.blkK) == "table" then s.blkK[oid] = nil end
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

-- Lauf baer-kampf (PLAN_KAMPF.md 2.2, K2): "steckt fest" sperrt das Ziel in der SITZUNG (s.fBlk, Deckel fightBlockMax, wie s.missBl) -- sonst
-- naehme der naechste Kampf (leere Sperrliste) dasselbe haengende Ziel sofort wieder (genau Kevins Bild: er wartet, bis es aufsteht).
local function stuckNow(s, oid, ms)
    local t = s and s.fBlk and num(s.fBlk[oid]) or nil
    return t ~= nil and t - ms > 0 and t - ms <= cfg("fightBlockLongMs", 120000)
end

local function stuckBlock(s, oid, ms)
    if type(s.fBlk) ~= "table" then s.fBlk, s.fBlkN = {}, 0 end
    if s.fBlk[oid] == nil then
        s.fBlkN = (num(s.fBlkN) or 0) + 1
        if s.fBlkN > cfg("fightBlockMax", 32) then s.fBlk, s.fBlkN = {}, 1 end
    end
    local span = blockSpan(s, oid, cfg("fightBlockMs", 20000), ms)      -- Nachbesserung C1: Wiederholung laenger
    s.fBlk[oid] = ms + span
    return span
end

-- Ziel waehlen (2.2.2): aus B._foes[id] nach Abstand, Banditen um fightBanditBias bevorzugt, nicht gesperrt, innerhalb der Leine; Sicht
-- (SP CanSee, Bandits client/BanditUpdate.lua:1087 / :1203; am Server ohne Sicht-Frage). Rueckgabe { o, kind, oid } / nil.
-- Lauf baer-kampf (PLAN_KAMPF.md 2.7, K7): Sicht fuer bis zu sightMax Kandidaten (vorher nur die drei naechsten -- standen die hinter einem
-- Zaun, ging er nicht los, auch wenn ein vierter frei stand); why (wahlfrei, nur mit Log) zaehlt je verworfenem Kandidaten den Grund
-- (out-of-leash, blocked, stuck, missblocked, level, no-sight). Die Gegnerliste ist ohnehin hoechstens foeListMax lang.
-- Nachbesserung (kampf/NACHBESSERUNG.md S4, Frage FK3): steht ein Gegner bis fightOwnerNear am Besitzer (f.own = { x, y }, gleiche Ebene, aus
-- B.Players() wie anchorOf), zaehlt er fightOwnerBias Kacheln naeher -- der Baer hilft zuerst dem, der beisst. Nur Abstaende.
local function ownerBonus(f, ox, oy)
    local own = f and f.own or nil
    local b = cfg("fightOwnerBias", 3)
    if own == nil or b <= 0 then return 0 end
    if B.DistXY(own.x, own.y, ox, oy) <= cfg("fightOwnerNear", 2.0) then return b end
    return 0
end

local function pickTarget(rec, a, f, ms, ax, ay, leash, why)
    local list = B._foes and B._foes[rec.id] or nil
    if type(list) ~= "table" or #list == 0 then return nil end
    local bx, by, bz = a:getX(), a:getY(), math.floor(a:getZ())
    local bias = cfg("fightBanditBias", 3)
    local ses = B._s and B._s[rec.id] or nil
    local best = {}
    local function note(k)
        if why then why[k] = (why[k] or 0) + 1 end
    end
    for i = 1, #list do
        local fo = list[i]
        local o = fo.o
        if o == nil or not o:isAlive() then
            note("dead")
        elseif blockedNow(f, fo.oid, ms) then
            note("blocked")
        elseif stuckNow(ses, fo.oid, ms) then
            note("stuck")
        elseif missedNow(ses, fo.oid, ms) then
            note("missblocked")
        elseif math.floor(o:getZ()) ~= bz then
            note("level")
        else
            local ox, oy = o:getX(), o:getY()
            if B.DistXY(ax, ay, ox, oy) <= leash then
                local sc = B.DistXY(bx, by, ox, oy)
                if fo.kind == "b" then sc = sc - bias end
                sc = sc - ownerBonus(f, ox, oy)
                best[#best + 1] = { fo = fo, s = sc }
            else
                note("out-of-leash")
                if fo.oid ~= nil then block(f, fo.oid, ms) end
            end
        end
    end
    if #best == 0 then return nil end
    if #best > 1 then table.sort(best, function(p, q) return p.s < q.s end) end
    local n = #best
    local sm = math.floor(cfg("sightMax", 12))
    if n > sm then n = sm end
    for i = 1, n do
        local o = best[i].fo.o
        if not B.IsSP() or a:CanSee(o) then return { o = o, kind = best[i].fo.kind, oid = best[i].fo.oid } end
        note("no-sight")
    end
    return nil
end

-- Gruende als Text fuer das Log ("no-sight 2, stuck 1"; feste Reihenfolge).
local WHY_ORDER = { "out-of-leash", "blocked", "stuck", "missblocked", "level", "no-sight", "dead" }
local function whyText(why)
    local t = {}
    for i = 1, #WHY_ORDER do
        local k = WHY_ORDER[i]
        if why[k] then t[#t + 1] = k .. " " .. tostring(why[k]) end
    end
    if #t == 0 then return "none" end
    return table.concat(t, ", ")
end

-- Naechster Gegner jetzt (lebendige Lage, hoechstens foeListMax Eintraege; je Kampfbeginn einmal). Rueckgabe Abstand oder nil.
local function nearestFoeD(rec, a)
    local list = B._foes and B._foes[rec.id] or nil
    if type(list) ~= "table" then return nil end
    local bx, by = a:getX(), a:getY()
    local best = nil
    for i = 1, #list do
        local o = list[i].o
        if o ~= nil and o:isAlive() then
            local d = B.DistXY(bx, by, o:getX(), o:getY())
            if best == nil or d < best then best = d end
        end
    end
    return best
end

-- Nachbesserung (S1/S2, S4): Lage des Besitzers (gleiche Ebene wie der Baer) aus der Spieler-Liste B.Players() (Felder x / y / z, wie anchorOf)
-- -- oder nil. Nur Zahlen.
local function ownerPt(rec, a, players)
    if rec.owner == nil or players == nil then return nil end
    local _, e = B.PlayerByKey(rec.owner, players)
    if e == nil or num(e.x) == nil or num(e.y) == nil then return nil end
    if math.floor(num(e.z) or 0) ~= math.floor(a:getZ()) then return nil end
    return { x = e.x, y = e.y }
end

-- Steht das Ziel? SP B.FoePosture (shared/BanditsNPCBearFoe.lua, Fundstellen dort), am MP-Server nur isProne (Bandits
-- client/BanditUpdate.lua:275) -- wie choose.
local function standing(o)
    if B.IsSP() and B.FoePosture then return (B.FoePosture(o) or "up") == "up" end
    return not o:isProne()
end

-- Nachbesserung (S1/S2, Frage FK1): Lagen aller Gegner beim Kampfbeginn (hoechstens foeListMax, B._foes), fuer das Tempo in rearCheck.
local function foeSnap(rec)
    local list = B._foes and B._foes[rec.id] or nil
    local t = {}
    if type(list) ~= "table" then return t end
    for i = 1, #list do
        local o = list[i].o
        if o ~= nil and o:isAlive() then t[#t + 1] = { o = o, x = o:getX(), y = o:getY() } end
    end
    return t
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
    s.calmBack = nil
    s.leashRun = nil
    s.mvX, s.mvY = nil, nil
    f.sprK = sprintK(rec)
    f.hitN = 0
    countFights()
    if B.IsSP() then B._mvOn = true end
    local allow = B.FightStageOf(st)
    -- Lauf baer-kampf (PLAN_KAMPF.md 2.1, K1; Kevin 13.11. ~23:00 Punkt 1 "das erste mal ... bevor er in den kampf stuermt"): EIN Entscheid je
    -- Kampf -- ausgewachsen, Pause rearCdMs frei und kein Gegner schon bis rearDist dran -> er richtet sich auf (der erste Angriff, choose);
    -- sonst Knurren und sofort Angriff. Kein Wurf je Takt mehr (rearChance 100).
    local cd = num(s.rearAt)
    local rearWhy = nil
    if not allow.rear then
        rearWhy = "stage " .. tostring(allow.stage)
    elseif cd ~= nil and ms - cd >= 0 and ms - cd < cfg("rearCdMs", 120000) then
        rearWhy = "cooldown " .. tostring(math.ceil((cfg("rearCdMs", 120000) - (ms - cd)) / 1000)) .. " s"
    else
        local near = nearestFoeD(rec, a)
        if near ~= nil and near <= cfg("rearDist", 2.5) then
            rearWhy = "foe at " .. tostring(r1(near)) .. " <= " .. tostring(cfg("rearDist", 2.5))
        elseif tgt.o ~= nil and not standing(tgt.o) then
            -- Nachbesserung S2: liegt / faellt das erste Ziel, zerfleischt er es sofort (sonst steht es waehrend der 3 s wieder auf)
            rearWhy = "target down"
        end
    end
    f.rearWant = rearWhy == nil
    if f.rearWant then
        -- Nachbesserung S1: erst schauen (rearCheck im Kampf-Takt), dann aufrichten oder nicht
        f.rearLook = ms
        f.rearSnap = foeSnap(rec)
    else
        growl(rec, a, ms)
        f.growled = true
    end
    touchFst(rec, s)
    B.Log("fight: " .. tostring(rec.id) .. " (" .. tostring(allow.stage) .. ") attacks a " .. tostring(tgt.kind) .. " (outfit "
        .. tostring(tgt.oid) .. ")")
    if logOn() then
        local rw = "planned (looking)"
        if rearWhy ~= nil then rw = "no (" .. rearWhy .. ")" end
        logE("rear:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " rear " .. rw)
    end
    return true
end

-- Nachbesserung (kampf/NACHBESSERUNG.md S1/S2, Frage FK1; Kevin Punkt 1 "bevor er in den kampf stuermt", "steht ein Zombie schon direkt dran
-- greift er sofort an"): nach dem Kampfbeginn haelt er rearLookMs still und schaut. Dann richtet er sich NICHT auf, wenn ein Gegner schon bis
-- rearDist dran ist, das erste Ziel liegt / faellt, oder ein Gegner ihn (bis rearDist) bzw. den Besitzer (bis rearOwnerPad) schneller erreicht
-- als der Aufricht-Clip dauert (rearSafeS; Tempo = Weg seit dem Kampfbeginn / Zeit, je Gegner aus foeSnap -- ohne Richtung, also eher
-- vorsichtig). Rueckgabe true = er schaut noch (der Aufrufer haelt ihn). Das Log sagt "rear yes" bzw. "rear no (Grund)" (eigener Schluessel,
-- C4). Nur Zahlen (getX/getY, isAlive wie oben).
local function rearCheck(rec, a, f, ms)
    local why = nil
    local rd = cfg("rearDist", 2.5)
    local near = nearestFoeD(rec, a)
    local o = f.tgt and f.tgt.o or nil
    local t0 = num(f.rearLook) or ms
    local dt = ms - t0
    if near ~= nil and near <= rd then
        why = "foe at " .. tostring(r1(near)) .. " <= " .. tostring(rd)
    elseif o ~= nil and not standing(o) then
        why = "target down"
    elseif dt >= 0 and dt < cfg("rearLookMs", 400) then
        return true
    else
        local T = cfg("rearSafeS", 3.0)
        local snap = f.rearSnap
        if T > 0 and dt > 0 and type(snap) == "table" then
            local bx, by = a:getX(), a:getY()
            local own = f.own
            local pad = cfg("rearOwnerPad", 2.0)
            for i = 1, #snap do
                local e = snap[i]
                local z = e.o
                if z ~= nil and z:isAlive() then
                    local zx, zy = z:getX(), z:getY()
                    local v = B.DistXY(e.x, e.y, zx, zy) / dt * 1000
                    local dB = B.DistXY(bx, by, zx, zy)
                    if dB - rd <= v * T then
                        why = "foe reaches the bear (" .. tostring(r1(dB)) .. " at " .. tostring(r1(v)) .. " t/s)"
                        break
                    end
                    if own ~= nil then
                        local dO = B.DistXY(own.x, own.y, zx, zy)
                        if dO - pad <= v * T then
                            why = "foe reaches the owner (" .. tostring(r1(dO)) .. " at " .. tostring(r1(v)) .. " t/s)"
                            break
                        end
                    end
                end
            end
        end
    end
    f.rearLook, f.rearSnap = nil, nil
    if why ~= nil then f.rearWant = false end
    if logOn() then
        local rw = "yes"
        if why ~= nil then rw = "no (" .. why .. ")" end
        logE("rearL:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " rear " .. rw)
    end
    return false
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
    local carNear = o ~= nil and o.car == true and (num(o.dist) or 999) <= cfg("rideDist", 15)
    -- F3 (Kevins Antworten 13.11.2026, 2 / 3 / 4): schlaftrunken nach dem Aufschrecken (s.wokeUntil, server/BanditsNPCBearSleep.lua), ohne
    -- Vertrauen (unter trRefuse) oder zu muede (Muedigkeit ab tirVery) kaempft er nicht (B.NoFight, shared/BanditsNPCBearNeedRules.lua)
    local wu = num(s.wokeUntil)
    local woke = wu ~= nil and wu - ms > 0 and wu - ms <= (num(s.wokeSpan) or 10000)
    local noFight = nil
    if B.NoFight then noFight = B.NoFight(rec) end
    local d = B.FightDecide({
        st = rec.st, body = B.BodyKind(a) or rec.body, s = st.s, passive = rec.passive == true, down = rec.down ~= nil,
        ride = rec.ride ~= nil, hpPts = hpPts, fleeHp = fleeHp, fleeHys = hys, fleeOn = s.fleeOn == true, sta = num(s.sta) or 1,
        resting = s.resting == true, restOver = restOver, longOver = longOver, foe = type(foes) == "table" and #foes > 0,
        ownerCarNear = carNear, follow = B.ModeOf(rec) == "follow", capFull = type(f) ~= "table" and countFights() >= cfg("fightMax", 4),
        woke = woke, noTrust = noFight == "trust", tired = noFight == "tired",
    })
    if d.why == "hurt" then s.fleeOn = true end
    -- Lauf baer-kampf (K6): auch passiv / ohne Vertrauen / zu muede / Pause -- wer unter der Flucht-Schwelle ist, flieht (B.GuardStep fragt
    -- s.fleeOn; der grosse Baer versteckt sich nie mehr hinter dem Besitzer)
    if d.act ~= "fight" and fleeHp > 0 and hpPts < fleeHp then s.fleeOn = true end
    -- F3: Grund des Rueckzugs fuer die Sicht (fsy) und die Meldung an den Besitzer (Kevin: "sagt das er zu muede ist" / "weigert er sich
    -- zu kaempfen und das steht dann da auch") -- gedrosselt in B.NeedRefuseSay (server/BanditsNPCBearNeeds.lua)
    local fsy = nil
    if d.act == "retreat" and (d.why == "woke" or d.why == "trust" or d.why == "tired") then fsy = d.why end
    if s.fsy ~= fsy then
        s.fsy = fsy
        B.Touch(rec)
    end
    if (fsy == "tired" or fsy == "trust") and B.NeedRefuseSay then B.NeedRefuseSay(rec, fsy, ms, players) end
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
        -- K8: Entscheid mit Gegner in der Liste, aber kein Kampf (passiv, verschnauft, zu muede, Junges ...)
        if logOn() and type(foes) == "table" and #foes > 0 then
            logE("fd:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " decide " .. tostring(d.act) .. " (" .. tostring(d.why)
                .. ") with foe at " .. tostring(r1(foes[1].d)))
        end
        return false
    end
    s.fstNow = nil
    if type(f) == "table" then
        touchFst(rec, s)
        return true
    end
    local ax, ay = a:getX(), a:getY()
    local pl = players or B.Players()
    local tmp = { sx = ax, sy = ay, blocked = {} }
    tmp.own = ownerPt(rec, a, pl)                   -- Nachbesserung S4: Besitzer-Bonus schon bei der ersten Zielwahl
    local bx, by, leash = anchorOf(rec, tmp, pl)
    -- Nachbesserung F2 B1: steht der Baer selbst nicht mindestens fightLeashPad innerhalb der Leine, beginnt kein Kampf (der Kampf-Takt
    -- beendete ihn sofort mit "leash", und Folgen kaeme nie an die Reihe) -- erst holen ihn Folgen bzw. die Zombie-Wache zurueck
    local ld = B.DistXY(bx, by, ax, ay)
    -- Lauf baer-kampf (K7, Kevin Punkt 7): waehrend des Leinen-Sprints ("bis er wieder in normaler Folge-Naehe ist") kein neuer Kampf --
    -- B.FollowStep beendet den Sprint in Folge-Naehe (s.leashRun weg), Frist fightLeashRunMs
    local lr = num(s.leashRun)
    if lr ~= nil and lr - ms > 0 and lr - ms <= cfg("fightLeashRunMs", 20000) and B.ModeOf(rec) == "follow" then
        touchFst(rec, s)
        if logOn() then
            logE("nt:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " no target: leash run (owner at " .. tostring(r1(ld)) .. ")")
        end
        return false
    end
    if ld > leash - cfg("fightLeashPad", 2) then
        touchFst(rec, s)
        huff(rec, a, s, ms)
        if logOn() then
            logE("nt:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " no target: leash (anchor at " .. tostring(r1(ld)) .. " > "
                .. tostring(leash - cfg("fightLeashPad", 2)) .. ")")
        end
        return false
    end
    local why = nil
    if logOn() then why = {} end
    local tgt = pickTarget(rec, a, tmp, ms, bx, by, leash, why)
    if tgt == nil then
        touchFst(rec, s)
        huff(rec, a, s, ms)
        if why then
            logE("nt:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " no target: " .. whyText(why) .. " (" .. tostring(#foes)
                .. " foes)")
        end
        return false
    end
    if why then
        logE("pk:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " pick " .. tostring(tgt.kind) .. " " .. tostring(tgt.oid) .. " at "
            .. tostring(r1(B.DistXY(ax, ay, tgt.o:getX(), tgt.o:getY()))) .. " (" .. tostring(#foes) .. " foes)")
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
    local f = s.fight
    s.fight = nil
    local ms = getTimestampMs()
    if why == "long" then s.restUntil = ms + cfg("fightRestMs", 20000) end
    -- Lauf baer-kampf (PLAN_KAMPF.md 2.4, K4; Kevin Punkt 4 "nach dem Kampf ruhig zurueck"): fightCalmBackMs lang geht er beim Folgen bis
    -- fightCalmWalkMax Kacheln (B.FollowDecide c.calm). Leine: stattdessen der Sprint zum Besitzer (s.leashRun, tickBear).
    if why ~= "leash" then s.calmBack = ms + cfg("fightCalmBackMs", 8000) end
    s.mvX, s.mvY = nil, nil
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
    local took = ""
    if num(f.startAt) ~= nil and ms - f.startAt >= 0 then
        took = " after " .. tostring(r1((ms - f.startAt) / 1000)) .. " s, " .. tostring(math.floor(num(f.hitN) or 0)) .. " hits"
    end
    B.Log("fight: " .. tostring(id) .. " ends (" .. tostring(why) .. ")" .. took)
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
-- Lauf baer-kampf (PLAN_KAMPF.md 2.3, K3 "kurzer Ausfallschritt im Schlag"): steht das Ziel weiter als 0,6 x Weite, schiebt sich der Baer bis
-- zum Treffer um bis zu f.lgMax heran (approach: fightLunge x Groesse, bei einem fliehenden Ziel mehr -- je Bild in B.FightMoveTick, nur
-- Einzelspieler). sz = gezeigte Groesse, d = Abstand jetzt.
local function enterAct(rec, a, s, f, act, ms, sz, d)
    local dur = B.ClipMs(act, 0, "big") or 1500
    local hit = B.ClipHitMs(act, "big")
    f.ph, f.act, f.t0, f.endAt, f.hitDone = "act", act, ms, ms + dur, false
    f.hitAt = nil
    if hit ~= nil then f.hitAt = ms + hit end
    f.lgLeft = 0
    local reach = B.FightReach(act, sz)
    f.lgStop = 0.6 * reach
    if B.IsSP() and f.hitAt ~= nil and reach > 0 and (num(d) or 0) > 0.6 * reach and (num(f.lgMax) or 0) > 0 then
        f.lgLeft = f.lgMax
        B._mvOn = true
    end
    f.lgUsed = (num(f.lgLeft) or 0) > 0             -- Nachbesserung C1: verfehlt dieser Hieb, Ausfall eine Weile aus (tickBear)
    f.ordAt, f.spAt = nil, nil
    -- fix1 (G-R3, kampf/GEGEN.md 6): Abstand beim Ausholen merken -- der erste Lauf-Takt danach (approach) laesst die Uhr "steckt fest" neu
    -- beginnen, wenn das Ziel waehrend des Hiebs weggelaufen ist (siehe dort)
    f.actD = d
    if logOn() then
        logE("act:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " act " .. tostring(act) .. " at d " .. tostring(r1(d)) .. " (hit-d "
            .. tostring(r1(f.lastDH)) .. ", " .. tostring(f.lastPst or "up") .. ", lunge " .. tostring(r1(f.lgLeft)) .. ")")
    end
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
-- Lauf baer-kampf (PLAN_KAMPF.md 2.1-2.3): d = Abstand jetzt (Aufricht-Frage), dh = Abstand zum Trefferzeitpunkt (Weiten, K3); Aufrichten nur
-- beim ersten Angriff UND f.rearWant (begin) -- ist der Gegner jetzt schon bis rearDist dran, entfaellt es (sofort Angriff), und nach dem
-- ersten Versuch gilt es nie wieder in diesem Kampf (ein Entscheid, kein Wurf je Takt). Liegt ODER faellt das Ziel (SP B.FoePosture,
-- shared/BanditsNPCBearFoe.lua; sonst o:isProne()), zerfleischt er (K2).
local function choose(rec, s, f, st, o, d, dh, ms)
    local allow = B.FightStageOf(st)
    local sz = num(st.sz) or 1
    local force = s.force
    if force ~= nil then
        if allow[ALLOW[force] or ""] ~= true then
            s.force = nil
        elseif force == "rear" or dh <= B.FightReach(force, sz) then
            s.force = nil
            return force
        else
            return nil
        end
    end
    local maxR = B.FightReach("slam", sz)
    local rs = B.FightReach("swipeL", sz)
    if rs > maxR then maxR = rs end
    local rearTry = allow.rear and f.first == true and f.rearWant == true
    if rearTry and d <= cfg("rearDist", 2.5) then
        rearTry = false
        f.rearWant = false
        -- Nachbesserung C4: eigener Schluessel -- sonst drosselt die Zeile von begin ("rear:") dieses Nein weg
        if logOn() then
            logE("rearC:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " rear no (foe at " .. tostring(r1(d)) .. " <= "
                .. tostring(cfg("rearDist", 2.5)) .. ")")
        end
    end
    if dh > maxR and not rearTry then return nil end
    if rearTry then f.rearWant = false end
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
    -- Haltung: Einzelspieler B.FoePosture (isProne + getActionStateName, Fundstellen dort) -- am MP-Server nur isProne (schnittstelle.md)
    local pst = "up"
    if B.IsSP() and B.FoePosture then
        pst = B.FoePosture(o) or "up"
    elseif o:isProne() then
        pst = "down"
    end
    f.lastPst = pst
    return B.FightChoose({
        allow = allow, last = f.last, prone = pst ~= "up", d = dh, dRear = d, sz = sz,
        slamReady = f.slamAt == nil or ms - f.slamAt < 0 or ms - f.slamAt >= cfg("slamCdMs", 10000), slamN = slamN,
        rearReady = rearTry,
        first = f.first, rnd = ZombRand(100), rnd2 = ZombRand(100),
    })
end

-- Lauf baer-kampf (PLAN_KAMPF.md 2.3, K3): Tempo des Ziels aus zwei Lagen im Abstand >= 300 ms (Kacheln/s; Deckel VMAX gegen das
-- Wegfliegen beim Umwerfen, ~1,6 x Sprinter); neues Ziel / alte Messung (> 2 s) -> neu, Tempo 0. Nur Zahlen (getX/getY kommen vom Aufrufer).
local VMAX = 6
local function trackFoe(f, o, ox, oy, ms)
    local tp = f.tp
    if type(tp) ~= "table" or tp.o ~= o or ms - tp.at < 0 or ms - tp.at > 2000 then
        f.tp = { o = o, x = ox, y = oy, at = ms }
        f.tvx, f.tvy = 0, 0
        return
    end
    local dt = ms - tp.at
    if dt < 300 then return end
    local vx, vy = (ox - tp.x) / dt * 1000, (oy - tp.y) / dt * 1000
    local v = math.sqrt(vx * vx + vy * vy)
    if v > VMAX then vx, vy = vx / v * VMAX, vy / v * VMAX end
    f.tvx, f.tvy = vx, vy
    tp.x, tp.y, tp.at = ox, oy, ms
end

-- Neues Ziel: Messungen und Laufbefehl neu.
local function setTarget(f, tgt)
    f.tgt, f.stuckAt, f.tp, f.tvx, f.tvy, f.ox, f.oy, f.ordAt = tgt, nil, nil, 0, 0, nil, nil, nil
    f.ozx, f.ozy, f.ovx, f.ovy = nil, nil, nil, nil
end

-- K3 "kein Hin- und Herrennen": ein anderer Gegner nimmt das Ziel nur, wenn er fightSwitchGain Kacheln naeher ist (frische Liste B._foes,
-- lebende Lage, gleiche Ebene, in der Leine, nicht gesperrt, SP mit Sicht wie pickTarget).
-- Nachbesserung (S4, Frage FK3): Abstand mit Besitzer-Bonus (ownerBonus) fuer das Ziel UND die Kandidaten; der beste der Liste (hoechstens
-- foeListMax, nur Zahlen), CanSee nur fuer ihn (hoechstens einmal je Takt).
local function switchMaybe(rec, a, s, f, ms, ax, ay, leash, d)
    local list = B._foes and B._foes[rec.id] or nil
    if type(list) ~= "table" or #list == 0 or type(f.tgt) ~= "table" or f.tgt.o == nil then return end
    local cur = f.tgt.o
    local bx, by, bz = a:getX(), a:getY(), math.floor(a:getZ())
    local curS = d - ownerBonus(f, cur:getX(), cur:getY())
    local best, bestS, bestD = nil, nil, nil
    for i = 1, #list do
        local fo = list[i]
        local o = fo.o
        if o ~= nil and o ~= cur and o:isAlive() and math.floor(o:getZ()) == bz and not blockedNow(f, fo.oid, ms)
            and not stuckNow(s, fo.oid, ms) and not missedNow(s, fo.oid, ms) then
            local ox, oy = o:getX(), o:getY()
            if B.DistXY(ax, ay, ox, oy) <= leash then
                local d2 = B.DistXY(bx, by, ox, oy)
                local sc = d2 - ownerBonus(f, ox, oy)
                if bestS == nil or sc < bestS then best, bestS, bestD = fo, sc, d2 end
            end
        end
    end
    if best == nil or bestS + cfg("fightSwitchGain", 2.0) > curS then return end
    if B.IsSP() and not a:CanSee(best.o) then return end
    if logOn() then
        local tag = ""
        if ownerBonus(f, best.o:getX(), best.o:getY()) > 0 then tag = ", at the owner" end
        logE("sw:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " switch to " .. tostring(best.oid) .. " at " .. tostring(r1(bestD))
            .. tag .. " (target was at " .. tostring(r1(d)) .. ")")
    end
    setTarget(f, { o = best.o, kind = best.kind, oid = best.oid })
end

-- K4/K8: gemessenes Tempo im Anlauf (Weg je >= 1 s, nur zusammenhaengender Anlauf; der Angriff setzt f.spAt zurueck). Letzte 8 fuer die
-- Diagnose (B._spd).
B._spd = B._spd or {}
local function speedNote(rec, f, bx, by, ms)
    local at = num(f.spAt)
    if at == nil or ms - at < 0 or ms - at > 3000 then
        f.spX, f.spY, f.spAt = bx, by, ms
        return
    end
    if ms - at < 1000 then return end
    local v = B.DistXY(f.spX, f.spY, bx, by) / (ms - at) * 1000
    f.spV = v
    f.spX, f.spY, f.spAt = bx, by, ms
    local t = B._spd
    if #t >= 8 then table.remove(t, 1) end
    t[#t + 1] = { id = rec.id, v = v, at = ms, k = num(f.sprK) or 0 }
end

-- Anlauf (2.2.3 "approach"): zum Ziel rennen (B.MoveTo); kein Fortschritt in fightStuckMs -> Ziel sperren, naechstes; fightStuckMax
-- Sperren -> Ende.
-- Lauf baer-kampf (PLAN_KAMPF.md 2.2, 2.3; Kevin Punkte 2 und 3): Ziel tot -> fightKillPauseMs verschnaufen; sonst ggf. Zielwechsel
-- (Hysterese). Vorhalt: Ziel = Lage + Tempo x min(d / Tempo des Baeren, fightLeadMs), fightArrive x sz davor (Vorgabe 0 = AUF die Lage).
-- Angriff, sobald der Abstand zum TREFFERZEITPUNKT (B.FightHitD: Ziel nach der Ausholzeit, Ausfallschritt abgezogen) in Weite ist. Neuer
-- Laufbefehl nur, wenn der Zielpunkt um fightRepathDist wanderte, der letzte fightRenewMs alt ist oder er still gehalten wurde (vorher je
-- 750 ms neu -- jede neue Wegsuche liess ihn stocken). "Steckt fest" nur ausserhalb der Weite (rMax + 0,5): ein Liegender in Weite wird nie
-- gesperrt; die Sperre lebt in der Sitzung (stuckBlock).
local function approach(rec, a, s, f, st, ms, ax, ay, leash)
    local tgt = f.tgt
    if not tgtOk(rec, a, tgt, ax, ay, leash) then
        if type(tgt) == "table" and tgt.o ~= nil and not tgt.o:isAlive() and cfg("fightKillPauseMs", 800) > 0 then
            setTarget(f, nil)
            f.ph, f.t0, f.pauseMs = "pause", ms, cfg("fightKillPauseMs", 800)
            s.held = nil
            holdOn(rec, a, s, ms)
            return
        end
        local why = nil
        if logOn() then why = {} end
        tgt = pickTarget(rec, a, f, ms, ax, ay, leash, why)
        setTarget(f, tgt)
        if tgt == nil then
            f.ph, f.t0 = "seek", ms
            s.held = nil
            holdOn(rec, a, s, ms)
            if why then logE("nt:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " no target: " .. whyText(why) .. " (seek)") end
            return
        end
    end
    local bx, by = a:getX(), a:getY()
    local d = B.DistXY(bx, by, tgt.o:getX(), tgt.o:getY())
    switchMaybe(rec, a, s, f, ms, ax, ay, leash, d)
    tgt = f.tgt
    local o = tgt.o
    local ox, oy = o:getX(), o:getY()
    d = B.DistXY(bx, by, ox, oy)
    trackFoe(f, o, ox, oy, ms)
    -- Liegt er (am MP-Server nur so belegt), bewegt er sich nicht von selbst: kein Vorhalt (das Wegfliegen schiebt ihn hoechstens knockPush)
    local vx, vy = num(f.tvx) or 0, num(f.tvy) or 0
    if o:isProne() then vx, vy = 0, 0 end
    -- Nachbesserung F2 B3: in Weite, aber nicht treffbar (Wand, Fenster, Zaun) -> kein Luftschlag; nach fightMissMax Faellen gesperrt
    local sz = num(st.sz) or 1
    local rMax = B.FightReach("slam", sz)
    local rs = B.FightReach("swipeL", sz)
    if rs > rMax then rMax = rs end
    -- Nachbesserung C1: EINE Grenze "in Weite" (rMax + 0,5) fuer "kein Luftschlag" und fuer den Angriff aus dem Ausfall -- vorher sperrte
    -- "kein Luftschlag" nur bis rMax + 0,25 und "steckt fest" galt erst ab rMax + 0,5: dazwischen stand er vor einem Zaun bis fightMaxMs
    local near = d <= rMax + 0.5
    if near and not canStrike(a, o) then
        if missNote(s, f, tgt, ms) and logOn() then
            logE("sk:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " skip " .. tostring(tgt.oid) .. ": wall")
        end
        return
    end
    -- Ausfallschritt (nur SP): fightLunge x Groesse; flieht das Ziel (Tempo-Anteil vom Baeren weg), folgt der Ausfall ihm in der Ausholzeit
    -- mit fightLungeChase x diesem Anteil, hoechstens so weit, wie der Baer in der Ausholzeit rennt (chaseSpeed). Nachbesserung C3: Vorgabe
    -- fightLungeChase 0 = nur der kurze Ausfall (Frage F6). Nachbesserung C1: nach einem verfehlten Hieb aus dem Ausfall kein Ausfall bis f.lgOff.
    local hitS = (B.ClipHitMs("swipeL", "big") or 600) / 1000
    local lunge, lgV = 0, 0
    local lgOff = num(f.lgOff)
    if B.IsSP() and (lgOff == nil or ms - lgOff >= 0 or lgOff - ms > cfg("fightLungeOffMs", 3000)) then
        lunge = cfg("fightLunge", 0.5) * sz
        local away = 0
        if d > 0.001 then away = (vx * (ox - bx) + vy * (oy - by)) / d end
        if away > 0 and cfg("fightLungeChase", 0) > 0 then
            local vc = chaseSpeed(rec, f.sprK)
            local cap = vc * hitS
            if cap < lunge then cap = lunge end
            lunge = lunge + away * hitS * cfg("fightLungeChase", 0)
            if lunge > cap then lunge = cap end
            lgV = vc
        end
    end
    f.lgMax, f.lgV = lunge, lgV
    local dh = B.FightHitD(bx, by, ox, oy, vx, vy, hitS, lunge, rs)
    f.lastDH = dh
    local act = choose(rec, s, f, st, o, d, dh, ms)
    -- Angriff aus dem Ausfall (noch ausser Weite rMax + 0,5): nur, wenn nichts dazwischen ist (canStrike) -- sonst weiter anlaufen, ohne Sperre
    -- (in Weite sperrt "kein Luftschlag" oben; weiter weg greift "steckt fest" unten, wenn er nicht naeher kommt)
    if act ~= nil and act ~= "rear" and not near and not canStrike(a, o) then act = nil end
    if act ~= nil then
        enterAct(rec, a, s, f, act, ms, sz, d)
        return
    end
    -- K3 Vorhalt und Laufbefehl
    local tx, ty, lead = B.FightLeadPt(ox, oy, vx, vy, d, chaseSpeed(rec, f.sprK), cfg("fightLeadMs", 800) / 1000)
    local back = cfg("fightArrive", 0) * sz
    local dt = B.DistXY(bx, by, tx, ty)
    if back > 0 and dt > 0.001 then
        if back > dt then back = dt end
        tx, ty = tx - (tx - bx) / dt * back, ty - (ty - by) / dt * back
    end
    f.mx, f.my = tx, ty
    -- Neuer Laufbefehl (K3 "Wegsuche nicht alle 750 ms neu starten"): der alte gilt, solange das Ziel dort ist, wo es beim Befehl hinlief
    -- (Lage + Tempo x Alter; Abweichung < fightRepathDist), er juenger als fightRenewMs ist und der Baer seinen Laufpunkt noch nicht erreicht hat
    -- (bis rMax dran und mindestens fightRepathMs alt -> neuer Punkt). Ein gerade fliehender Zombie bekommt so hoechstens alle ~1,5-2 s einen
    -- neuen Weg statt bei jeder Kachel; ein haken schlagender sofort.
    local age = nil
    if num(f.ordAt) ~= nil and ms - f.ordAt >= 0 then age = ms - f.ordAt end
    local dev = 0
    if age ~= nil and f.ozx ~= nil then
        dev = B.DistXY(f.ozx + (num(f.ovx) or 0) * age / 1000, f.ozy + (num(f.ovy) or 0) * age / 1000, ox, oy)
    end
    local reached = age ~= nil and f.ox ~= nil and age >= cfg("fightRepathMs", 750) and B.DistXY(bx, by, f.ox, f.oy) <= rMax
    local order = "kept"
    if s.held or f.ox == nil or age == nil or age >= cfg("fightRenewMs", 2000) or dev >= cfg("fightRepathDist", 1.0) or reached then
        if B.MoveTo(rec, a, tx, ty, rec.z, { force = true, watch = false }) then
            f.ox, f.oy, f.ordAt = tx, ty, ms
            f.ozx, f.ozy, f.ovx, f.ovy = ox, oy, vx, vy
            order = "new"
        end
    end
    speedNote(rec, f, bx, by, ms)
    if logOn() then
        logE("run:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " run to " .. tostring(r1(tx)) .. "," .. tostring(r1(ty)) .. " (lead "
            .. tostring(r1(vx * lead)) .. "," .. tostring(r1(vy * lead)) .. ", order " .. order .. ", d " .. tostring(r1(d)) .. ") speed "
            .. tostring(r1(f.spV)) .. " t/s")
    end
    -- Nachbesserung C1: die Uhr "steckt fest" beginnt neu nach einem eigenen TREFFER (f.hitLast juenger als fightStuckMs; z. B. das Ziel flog
    -- nach dem Hieb weg), nicht mehr allein, weil er in Weite steht -- in Weite ohne Treffer und ohne Fortschritt wird das Ziel gesperrt.
    local hl = num(f.hitLast)
    local hitRecent = hl ~= nil and ms - hl >= 0 and ms - hl < cfg("fightStuckMs", 3000)
    -- fix1 (G-R3, kampf/GEGEN.md 6): erster Lauf-Takt nach einem Hieb. Ist das Ziel waehrend des Ausholens um mindestens fightStuckGain weiter
    -- weg (es floh, waehrend er stand), beginnt die Uhr neu -- der Hieb war kein Lauf ohne Fortschritt; sonst kam nach einem verfehlten Hieb
    -- gegen ein fliehendes Ziel sofort die Sperre, obwohl er aufholt. Blieb das Ziel, wo es war (Ausfall am Hindernis gestoppt), laeuft die Uhr
    -- weiter wie bisher (Nachbesserung C1: sonst Hieb um Hieb in die Luft, jeder Hieb setzte die Uhr zurueck -- attrappe/kampf_nach N1d).
    local actD = num(f.actD)
    if actD ~= nil then
        f.actD = nil
        if d - actD >= cfg("fightStuckGain", 0.5) then f.stuckAt = nil end
    end
    if f.stuckAt == nil or ms - f.stuckAt < 0 or hitRecent then
        f.stuckAt, f.stuckD = ms, d
    elseif ms - f.stuckAt >= cfg("fightStuckMs", 3000) then
        if (num(f.stuckD) or d) - d < cfg("fightStuckGain", 0.5) then
            if tgt.oid ~= nil then stuckBlock(s, tgt.oid, ms) end
            if logOn() then
                logE("sk:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " skip " .. tostring(tgt.oid) .. ": stuck at d " .. tostring(r1(d)))
            end
            f.stuckN = (f.stuckN or 0) + 1
            setTarget(f, nil)
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
    local ld = B.DistXY(ax, ay, a:getX(), a:getY())
    if ld > leash then
        -- Lauf baer-kampf (PLAN_KAMPF.md 2.7, K7; Kevin Punkt 7 "wenn ich 25 kacheln weg bin in fullspeed zu mir sprinten"): beim Folgen
        -- sprintet er zum Besitzer, bis er in Folge-Naehe ist (server/BanditsNPCBearFollow.lua; Sprint-Schub B.FightMoveTick, nur SP),
        -- hoechstens fightLeashRunMs
        if B.ModeOf(rec) == "follow" then
            s.leashRun = ms + cfg("fightLeashRunMs", 20000)
            s.leashK = sprintK(rec)
            s.mvX, s.mvY = nil, nil
            if B.IsSP() then B._mvOn = true end
            if logOn() then
                logE("lr:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " leash run, owner at " .. tostring(r1(ld)) .. " > "
                    .. tostring(leash))
            end
        end
        B.FightDrop(rec.id, "leash")
        return
    end
    f.own = ownerPt(rec, a, players)                -- Nachbesserung S1/S4: Besitzer-Lage je Takt (B.Players(), schon geholt)
    local st = B.StatsOf(rec)
    if f.ph == "act" then
        holdOn(rec, a, s, ms)
        if not f.hitDone and f.hitAt ~= nil and ms >= f.hitAt then
            f.hitDone = true
            f.lgLeft = 0
            local n, wall = strike(rec, a, f, st, ms)
            if n > 0 then
                f.hitLast, f.missOid, f.missN, f.missAt = ms, nil, 0, nil
                f.hitN = (num(f.hitN) or 0) + 1
            elseif wall then
                missNote(s, f, f.tgt, ms)
            elseif f.lgUsed == true and f.act ~= "rear" then
                -- Nachbesserung C1: Hieb aus dem Ausfall ins Leere (Ziel nicht erreicht, z. B. Ausfall an einem Hindernis gestoppt) -> eine Weile
                -- ohne Ausfall: er laeuft hin (dann greift "steckt fest", wenn er nicht naeher kommt) statt Hieb um Hieb in die Luft
                f.lgOff = ms + cfg("fightLungeOffMs", 3000)
            end
            -- K8: Treffer oder Fehlschlag (Abstand beim Treffer zur Weite + 0,25 wie strike)
            if logOn() and f.act ~= "rear" then
                local o = f.tgt and f.tgt.o or nil
                local hd = -1
                if o ~= nil then hd = B.DistXY(a:getX(), a:getY(), o:getX(), o:getY()) end
                local res = "hit " .. tostring(n)
                if n == 0 then
                    res = "miss (d " .. tostring(r1(hd)) .. " > " .. tostring(r1(B.FightReach(f.act, num(st.sz) or 1) + 0.25)) .. ")"
                    if wall then res = "miss (wall, d " .. tostring(r1(hd)) .. ")" end
                end
                logE("hit:" .. tostring(rec.id), "fight: " .. tostring(rec.id) .. " " .. tostring(f.act) .. " " .. res)
            end
        end
        if ms >= f.endAt or ms - f.t0 < 0 then f.ph, f.t0 = "pause", ms end
        return
    end
    if f.ph == "pause" then
        holdOn(rec, a, s, ms)
        -- K3: nach dem Kill f.pauseMs (fightKillPauseMs), sonst fightPauseMs
        local pm = num(f.pauseMs) or cfg("fightPauseMs", 350)
        if ms - f.t0 >= 0 and ms - f.t0 < pm then return end
        f.ph, f.t0, f.pauseMs = "approach", ms, nil
    end
    if f.ph == "seek" then
        holdOn(rec, a, s, ms)
        local tgt = pickTarget(rec, a, f, ms, ax, ay, leash)
        if tgt == nil then
            if ms - f.t0 < 0 or ms - f.t0 >= cfg("fightSeekMs", 3000) then B.FightDrop(rec.id, "seek") end
            return
        end
        setTarget(f, tgt)
        f.ph, f.t0 = "approach", ms
    end
    -- Nachbesserung S1/S2: vor dem ersten Angriff kurz schauen, ob das Aufrichten jetzt passt (rearCheck); solange haelt er still
    if f.first == true and f.rearWant == true and f.rearLook ~= nil and type(f.tgt) == "table" and rearCheck(rec, a, f, ms) then
        holdOn(rec, a, s, ms)
        return
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

-- ---------------------------------------------------------------------------
-- Lauf baer-kampf (PLAN_KAMPF.md 2.3, 2.4; K3 Ausfallschritt, K4 Sprint): je BILD, nur Einzelspieler, nur solange ein Baer kaempft oder zum
-- Besitzer sprintet (B._mvOn; sonst kein Aufruf). Je Baer hoechstens getX/getY/getZ, isDead, setX/setY und bei einem Kachelwechsel
-- B.FoeStepOk. Sprint: Zusatzweg = eigene Bewegung dieses Bildes x k (B.FightSprintStep, Deckel sprintStepMax) -- nur im Anlauf (nicht
-- gehalten) bzw. beim Leinen-Sprint (rennend, nicht gehend), nur bei echter Laufbewegung (mindestens halbes Lauftempo: kein Schieben durch
-- Zombies, kein Gehen; hoechstens 3 x fightSprint: kein Versetzen) und nur, wenn das Bild <= 50 ms dauerte (Ruckler / Pause schieben nicht).
-- Gemerkt wird die Lage NACH dem eigenen Schritt (sonst schaukelte sich der Schub auf). Ausfallschritt: im Angriff bis zum Treffer je Bild
-- fightLungeStep Richtung Ziel, zusammen hoechstens f.lgLeft, nie naeher als 0,6 x Weite (f.lgStop).
-- Ehrlich (Frage F1 fuer Kevin): die Beine laufen im Takt des Renn-Clips, der Koerper gleitet im Sprint ~45 % schneller.
-- ---------------------------------------------------------------------------
-- Darf der Koerper von (x0, y0) nach (x1, y1)? Gleiche Kachel ja; sonst nur mit B.FoeStepOk (Wand, Tuer, Fenster, Zaun, Wasser, Treppe --
-- shared/BanditsNPCBearFoe.lua, ZOMBIES); fehlt die Funktion, kein Kachelwechsel.
local function stepOk(x0, y0, x1, y1, zl)
    if math.floor(x0) == math.floor(x1) and math.floor(y0) == math.floor(y1) then return true end
    if B.FoeStepOk == nil then return false end
    return B.FoeStepOk(x0, y0, x1, y1, zl) == true
end

-- Die EINE Stelle, die die Lage des Baeren setzt (Uebernahme-Regel setXY): a:setX(Zahl) / a:setY(Zahl) am Tier wie Vanilla
-- server/ClientCommands.lua:895-896 und shared/Definitions/animal/ButcheringUtil.lua:575-576; a:getZ() am Tier: Vanilla
-- client/TimedActions/ISContextualActions.lua:100. Rueckgabe true, wenn gesetzt.
local function moveBear(a, x, y, nx, ny)
    if not stepOk(x, y, nx, ny, math.floor(a:getZ())) then return false end
    a:setX(nx)
    a:setY(ny)
    return true
end

local function moveOne(s, f, a, run, okDt, dtS, ms)
    local x, y = a:getX(), a:getY()
    local px, py = num(s.mvX), num(s.mvY)
    s.mvX, s.mvY = x, y
    if type(f) == "table" and f.ph == "act" then
        local left = num(f.lgLeft) or 0
        local o = f.tgt and f.tgt.o or nil
        if left > 0 and o ~= nil and okDt and num(f.hitAt) ~= nil and ms < f.hitAt then
            -- je Bild fightLungeStep; folgt er einem fliehenden Ziel, mindestens sein Renntempo (f.lgV) x Bilddauer
            local step = cfg("fightLungeStep", 0.06)
            local fast = (num(f.lgV) or 0) * dtS
            if fast > step then step = fast end
            local ex, ey, l = B.FightLungeStep(x, y, o:getX(), o:getY(), left, step, num(f.lgStop) or 0)
            if l > 0 and moveBear(a, x, y, x + ex, y + ey) then
                f.lgLeft = left - l
                s.mvX, s.mvY = x + ex, y + ey
            else
                f.lgLeft = 0
            end
        end
        return
    end
    local k = 0
    if type(f) == "table" then
        if f.ph == "approach" and f.readyAt == nil and not s.held then k = num(f.sprK) or 0 end
    elseif run and s.walk ~= true and not s.held then
        k = num(s.leashK) or 0
    end
    if k <= 0 or px == nil or py == nil or not okDt or dtS <= 0 then return end
    local dx, dy = x - px, y - py
    local v = math.sqrt(dx * dx + dy * dy) / dtS
    local fs = cfg("fightSprint", 4.6)
    if v < 0.5 * fs / (1 + k) or v > 3 * fs then return end
    local ex, ey = B.FightSprintStep(dx, dy, k, cfg("sprintStepMax", 0.08))
    if (ex ~= 0 or ey ~= 0) and moveBear(a, x, y, x + ex, y + ey) then s.mvX, s.mvY = x + ex, y + ey end
end

local function moveTickBody()
    if not B.IsSP() then
        B._mvOn = false
        return
    end
    local ms = getTimestampMs()                 -- Vanilla server/Foraging/forageServer.lua:456
    local last = num(B._mvAt)
    B._mvAt = ms
    local okDt = last ~= nil and ms - last > 0 and ms - last <= 50
    local dtS = 0
    if okDt then dtS = (ms - last) / 1000 end
    local busy = false
    for _, s in pairs(B._s) do
        if type(s) == "table" then
            local f = s.fight
            local lr = num(s.leashRun)
            local run = lr ~= nil and lr - ms > 0 and lr - ms <= cfg("fightLeashRunMs", 20000)
            if lr ~= nil and not run then s.leashRun = nil end
            local a = s.obj
            if a ~= nil and (type(f) == "table" or run) and not a:isDead() then
                busy = true
                moveOne(s, f, a, run, okDt, dtS, ms)
            end
        end
    end
    if not busy then B._mvOn = false end
end

function B.FightMoveTick()
    local ok, err = pcall(moveTickBody)
    if not ok then
        B._mvOn = false
        B.ErrEvery("fightmove", 60000, "fight move tick: " .. tostring(err))
    end
end

-- F3: + fsy (Grund des Rueckzugs), mdmgK (Schaden-Faktor durch Hunger / Durst).
-- Sicht (4.7, 11.2, 11.5, 11.7) -- aus viewEntry, nur gezaehmt/vermisst: fst (Kampfzustand), mdmg / mdmgB / mdmgM / mdmgS / mdmgF (Schaden
-- je Treffer, Groessen-Anteil, Kaempfen-Bonus %), kZ / kB (Kills), fleeP (Flucht-Schwelle in Lebenspunkten, aufgerundet; fehlt = nie).
function B.FightView(rec, t, ms)
    if type(rec) ~= "table" or type(t) ~= "table" then return end
    if rec.st == "tame" then t.fst = B.FightState(rec) end
    -- F3: fsy = Grund des Rueckzugs ("tired" zu muede / "trust" weigert sich / "woke" schlaftrunken), nur neben fst "retreat"
    if t.fst == "retreat" then
        local s = B._s and B._s[rec.id] or nil
        if type(s) == "table" then t.fsy = s.fsy end
    end
    local md = B.MeleeDamage(rec)
    if md ~= nil then
        -- F3: mdmgK = Schaden-Faktor durch Hunger / Durst (nur wenn unter 1; in mdmg* schon eingerechnet)
        if (num(md.need) or 1) < 1 then t.mdmgK = r2(md.need) end
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
-- Lauf baer-kampf: + B.FightMoveTick je Bild, nur solange B._mvOn (Kampf oder Leinen-Sprint im Einzelspieler).
Events.OnTick.Add(function()
    if (B._fightN or 0) > 0 or (B._foeN or 0) > 0 or #(B._fa or {}) > 0 or #B._kp > 0 then B.FightTick() end
    if B._mvOn then B.FightMoveTick() end
end)
