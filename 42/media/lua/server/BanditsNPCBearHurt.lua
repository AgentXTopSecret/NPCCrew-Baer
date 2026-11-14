if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Treffer am Baeren, Am Boden, Tod (F2 = B5a, PLAN_F2.md 0.1, 0.10, 0.11, 2.4, 4.3; Nachtrag 11.7).
--
-- B.BearHurt ist die EINE Stelle fuer Schaden am gezaehmten Baeren (Zombie-Biss, Hieb eines feindlichen Banditen; gerufen nur aus dem
-- Gegner-Takt server/BanditsNPCBearFightFoes.lua). Der Schreiber entscheidet alles (Ausweichen, Schaden, Tod, Am Boden); die Clients zeigen
-- nur (Fx "hurt" / "down" / "dead", shared/BanditsNPCBear.lua B.Fx). Kevin ENT:23-24: er kann sterben; Sandbox BearCannotDie (Vorgabe AUS)
-- -> "am Boden" statt Tod, der Besitzer hilft ihm auf (5 s, 45 %) oder er steht nach BearDownedHours (12) mit 15 % allein auf (ENT:42).
-- Ist der Besitzer nicht da (Mehrspieler offline), stirbt der Baer nie, er geht hoechstens zu Boden (PLAN_F2.md 0.10, rote Linie "der Baer
-- geht nie verloren"). Tod: Register ZUERST (B.Close, Sperre, Meldung), DANN der Koerper (B.BodyDie) -- so kann der Eintrag nie als
-- "missing" in die C1-Wiederkehr laufen (kein zweiter Baer, forschung_f2_gegner.md 2.2). Inventar gibt es noch nicht (F4): nichts verloren.
-- Am Boden ist unser eigener Zustand (rec.down = Spielstunde des Falls, gespeichert; die Engine kennt fuer Tiere kein "downed"): er haelt
-- still in der Sitz-Pose (Sicht dn), Zombies und Banditen lassen ihn in Ruhe, kein Kampf, kein Verstecken, kein Folgen, kein Einsteigen,
-- keine Selbstheilung (nur ein Verband wirkt).
-- Fliehen (11.7, Kevin 12.11. ~07:30): reicht das Leben nur noch fuer BearFleeHits Treffer (B.FleeHp), meldet der Schreiber es einmal
-- (Note_Flee); den Rueckzug selbst entscheidet B.FightDecide (R6) im Hirn-Takt.
-- Engine-Aufrufe hier (Fundstelle am Aufruf): getX/getY am Tier und am Gegner, ZombRand, getTimestampMs. Leben und Tod am Koerper nur
-- ueber B.BodyHurt / B.BodyHp / B.BodyDie (server/BanditsNPCBearGrow.lua). Ladefolge: server/ alphabetisch; fremde Funktionen nur zur
-- Laufzeit ueber B.X. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

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

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Besitzer gerade im Spiel? Rueckgabe: Spieler-Objekt oder nil (B.PlayerByKey, server/BanditsNPCBearWorld.lua).
local function ownerP(rec, players)
    if rec.owner == nil then return nil end
    local p = B.PlayerByKey(rec.owner, players)
    return p
end

local function tellOwner(rec, players, n)
    local p = ownerP(rec, players)
    if p then B.Tell(p, B.NoteBd(n, rec)) end
end

-- Arten der Gegner, die dem Baeren gerade nah sind (B._foes, server/BanditsNPCBearFightFoes.lua) -- fuer B.FleeHp (11.7).
function B.FoeKinds(id)
    local k = {}
    local list = B._foes and B._foes[id] or nil
    if type(list) == "table" then
        for i = 1, #list do
            if list[i].kind == "b" then k.b = true else k.z = true end
        end
    end
    return k
end

-- ---------------------------------------------------------------------------
-- Treffer (2.4). rec = gezaehmter Eintrag, a = sein Koerper, pts = Lebenspunkte (B.FoePts), src = "z" / "b", foe = Angriffs-Eintrag
-- { o, oid } oder nil. Rueckgabe "dodge" / "hit" / "down" / "dead" / nil (nicht gerechnet). getTimestampMs: Vanilla
-- server/Foraging/forageServer.lua:456; ZombRand(n): shared/TimedActions/Animals/ISMilkAnimal.lua:25; getX/getY am Tier: Vanilla
-- shared/Definitions/animal/ButcheringUtil.lua:575-576; am Zombie/Banditen: Bandits client/BanditZombie.lua:69-70.
-- ---------------------------------------------------------------------------
function B.BearHurt(rec, a, pts, src, foe)
    if type(rec) ~= "table" or a == nil or rec.st ~= "tame" or rec.down ~= nil or rec.ride ~= nil then return nil end
    local reg = B.Reg and B.Reg() or nil
    if not reg or reg.cubs[rec.id] ~= rec then return nil end
    local ms = getTimestampMs()
    -- F3 (PLAN_F3.md 6.3): ein Treffer weckt sofort (Aufschrecken; server/BanditsNPCBearSleep.lua) -- auch wenn er ausweicht
    if B.SleepStop then B.SleepStop(rec, "alarm", ms) end
    local st = B.StatsOf(rec)
    local s = B.Ses(rec.id)
    local bx, by = a:getX(), a:getY()
    local fx = { id = rec.id, bx = bx, by = by, src = src, big = rec.body == "big" }
    if type(foe) == "table" then
        fx.oid = foe.oid
        local o = foe.o
        if o ~= nil then fx.zx, fx.zy = o:getX(), o:getY() end
        -- Nachbesserung F2 B3: der Angriff kam an (nichts dazwischen) -> eine Luftschlag-Sperre auf diesen Gegner faellt weg
        if B.FightUnmiss then B.FightUnmiss(rec.id, foe.oid) end
    end
    if B.DodgeHit(st.dodge, ZombRand(100)) then
        fx.dodge = true
        B.Fx("hurt", fx, bx, by)
        B.Log("hurt: " .. tostring(rec.id) .. " dodged a " .. tostring(src) .. " attack (" .. tostring(B.Round1(st.dodge)) .. " %)")
        return "dodge"
    end
    pts = num(pts) or 0
    if pts < 0 then pts = 0 end
    local hpMax = num(st.hpMax) or 1
    if hpMax <= 0 then hpMax = 1 end
    local hp1 = B.BodyHurt(rec, a, pts / hpMax)
    B.OnHitTaken(rec, pts, ms)
    fx.dodge = false
    B.Fx("hurt", fx, bx, by)
    local players = B.Players()
    local fleeHp = B.FleeHp(B.FoeKinds(rec.id))
    local low = fleeHp > 0 and hp1 * hpMax < fleeHp
    if low and hp1 > 0 and s.fleeSaid ~= true then
        s.fleeSaid = true
        tellOwner(rec, players, note("UI_BN_Bear_Note_Flee", nil, nil, "bad"))
    end
    if B.LogActive() then
        B.Log("hurt: " .. tostring(rec.id) .. " -" .. tostring(B.Round1(pts)) .. " (" .. tostring(src) .. ") -> "
            .. tostring(math.floor(hp1 * hpMax + 0.5)) .. " / " .. tostring(math.floor(hpMax + 0.5)) .. " health")
    end
    if hp1 <= 0 then
        if B.Opt("BearCannotDie") == true or ownerP(rec, players) == nil then
            B.BearDown(rec, a, src, players)
            return "down"
        end
        B.BearDie(rec, a, src)
        return "dead"
    end
    -- festschreiben hoechstens je hpCommitMs, sofort unter der Flucht-Schwelle (2.3)
    local at = num(s.hpComAt)
    if low or at == nil or ms - at < 0 or ms - at >= cfg("hpCommitMs", 2000) then
        s.hpComAt = ms
        B.Commit(rec)
    else
        B.Touch(rec)
    end
    return "hit"
end

-- ---------------------------------------------------------------------------
-- Am Boden (0.10, 2.4). Leben auf downFloor (5 %), Kampf und Angriffe weg, Abklingzeit von Call/Unstuck startet jetzt (Lehre NPC Crew
-- client/BanditsNPCCombat.lua:91-104, nur gelesen), festschreiben, still halten, Fx "down", Meldung. Rueckgabe: true, wenn neu am Boden.
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
-- ---------------------------------------------------------------------------
function B.BearDown(rec, a, why, players)
    if type(rec) ~= "table" or rec.st ~= "tame" or rec.down ~= nil then return false end
    local ms = getTimestampMs()
    rec.down = B.Now()
    rec.hp = cfg("downFloor", 0.05)
    if a ~= nil then B.BodyHp(rec, a, 0) end
    if B.FightDrop then B.FightDrop(rec.id, "down") end
    if B.FoeDrop then B.FoeDrop(rec.id) end
    if B.CallStamp then B.CallStamp(rec, ms) end
    local s = B.Ses(rec.id)
    if type(s.g) == "table" then s.g.on = nil end
    s.fleeSaid = nil
    s.fstNow, s.fstSent = nil, nil              -- Nachbesserung F2 B5: Sicht fst weg (dn hat Vorrang, Sitz-Pose am Boden)
    -- F3 (PLAN_F3.md 4.1, 6.3): am Boden gibt es keinen Schlaf (ohne Bild), und ein Mal am Boden kostet Vertrauen (trDown; K1, Kevin 14.11.
    -- ~00:00: -10 jedes Mal, mit Meldung UI_BN_Bear_Note_TrustDown aus B.TrustAdd)
    if B.SleepStop then B.SleepStop(rec, "gone", ms, players) end
    if B.TrustAdd then B.TrustAdd(rec, "down", nil, nil, players) end
    B.Commit(rec)
    local bx, by = rec.x, rec.y
    if a ~= nil then
        B.Hold(rec, a, true)
        bx, by = a:getX(), a:getY()               -- Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576
    end
    B.Fx("down", { id = rec.id, bx = bx, by = by }, bx, by)
    tellOwner(rec, players or B.Players(), note("UI_BN_Bear_Note_Down", nil, nil, "bad"))
    B.Log("down: " .. tostring(rec.id) .. " is down (" .. tostring(why) .. ")")
    return true
end

-- Aus liveRec direkt nach der Laerm-Wache (server/BanditsNPCBearServer.lua): am Boden haelt er still, sonst nichts. Rueckgabe true = haelt.
function B.DownStep(rec, a, ms)
    if type(rec) ~= "table" or rec.down == nil or a == nil then return false end
    B.Hold(rec, a, true)
    return true
end

-- Aus slowRec (Langsam-Takt, 10 Spielminuten): nach BearDownedHours steht er allein mit downSelfHp (15 %) auf. Uhr rueckwaerts -> neu.
function B.DownSlow(rec, now, players)
    if type(rec) ~= "table" or rec.down == nil then return end
    if rec.st ~= "tame" and rec.st ~= "missing" then
        rec.down = nil
        return
    end
    local t = num(rec.down)
    now = num(now) or B.Now()
    if t == nil or now < t then
        rec.down = now
        return
    end
    if now - t < cfg("downedHours", 12) then return end           -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3): fester Wert
    rec.down = nil
    local alone = cfg("downSelfHp", 0.15)
    if (num(rec.hp) or 0) < alone then rec.hp = alone end
    local a = B.FindAnimal(rec)
    if a ~= nil then
        B.BodyHp(rec, a, 0)
        B.Hold(rec, a, false)
    end
    B.Commit(rec)
    tellOwner(rec, players or B.Players(), note("UI_BN_Bear_Note_GotUp", nil, nil, "good"))
    B.Log("down: " .. tostring(rec.id) .. " got up on its own")
end

-- Aufhelfen (2.4): aus BanditsNPCBearHelpAction:complete() (shared/TimedActions, OBERFLAECHE) -- im Mehrspieler auf dem Server. Nur der
-- Besitzer (Kevin F-G19), nur am gezaehmten, geladenen Baeren in Reichweite (B.HandCheck meldet Why_Gone / Why_Far selbst).
-- Rueckgabe: true, wenn er steht.
function B.HelpUpComplete(character, animal)
    local hc = B.HandCheck
    if hc == nil then return false end
    local rec = hc(character, animal)
    if not rec then return false end
    local pkey = B.PlayerKey(character)
    if rec.st ~= "tame" or rec.owner == nil or rec.owner ~= pkey then
        B.Tell(character, note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return false
    end
    if rec.down == nil then
        B.Tell(character, B.NoteBd(note("UI_BN_Bear_Why_NotDown", nil, nil, "bad"), rec))
        return false
    end
    rec.down = nil
    local up = cfg("helpUpHp", 0.45)
    if (num(rec.hp) or 0) < up then rec.hp = up end
    B.BodyHp(rec, animal, 0)
    B.Hold(rec, animal, false)
    B.Commit(rec)
    B.Tell(character, B.NoteBd(note("UI_BN_Bear_Note_HelpedUp", nil, nil, "good"), rec))
    B.Log("down: " .. tostring(rec.id) .. " helped up by " .. tostring(pkey))
    B.FlushViews()
    return true
end

-- ---------------------------------------------------------------------------
-- Tod (0.11, 2.4): Fx "dead" (Clients: Todeslaut, Zombies loslassen) -> Kampf und Angriffe weg -> B.Close(rec, "dead") (Sperre
-- BearDeathLockDays, Note_BearDead / Note_Dead, Sitzung, Laerm-Wache; server/BanditsNPCBearRegistry.lua) -> B.BodyDie (Schutz aus,
-- Ersatz-Angreifer, Leben 0; server/BanditsNPCBearGrow.lua). Angreifer nie ein Spieler.
-- ---------------------------------------------------------------------------
function B.BearDie(rec, a, why)
    if type(rec) ~= "table" then return end
    local bx, by = rec.x, rec.y
    if a ~= nil then bx, by = a:getX(), a:getY() end      -- Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576
    B.Fx("dead", { id = rec.id, bx = bx, by = by, big = rec.body == "big" }, bx, by)
    if B.FightDrop then B.FightDrop(rec.id, "dead") end
    if B.FoeDrop then B.FoeDrop(rec.id) end
    B.Close(rec, "dead")
    if a ~= nil then B.BodyDie(rec, a) end
    B.Log("dead: " .. tostring(rec.id) .. " was killed (" .. tostring(why) .. ")")
end

-- Sicht (4.7): dn (am Boden) und dnH (Stunden bis allein aufstehen, 0,1) -- aus viewEntry (server/BanditsNPCBearRegistry.lua).
function B.DownView(rec, t, now)
    if type(rec) ~= "table" or type(t) ~= "table" or rec.down == nil then return end
    local d = num(rec.down)
    if d == nil then return end
    now = num(now) or B.Now()
    t.dn = true
    local left = cfg("downedHours", 12) - (now - d)
    if left < 0 then left = 0 end
    t.dnH = B.Round1(left)
end
