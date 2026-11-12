if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Laerm-Wache und Zombie-Wache (B1c, PLAN_B1C.md 0.4, 0.5, 1.2, 1.3).
--
-- LAERM: die Engine laesst jedes nicht wilde Tier vor Laerm (Schuss, Q-Ruf, Husten, Zombie am Zaun) "radius + 10" Kacheln
-- wegrennen (IsoAnimal.respondToSound, Jar _arbeit/baer_zaehmen/dec/IsoAnimal.java:764-806; nur beim Schreiber). Das GEZAEHMTE
-- Junge soll das nicht mehr: je Bild (OnTick) erkennt B.CalmTick eine fremde Flucht (Stress-Sprung -- die Engine gibt je Flucht
-- +radius x 0,05, dec/IsoAnimal.java:799 -- oder "laeuft rennend ohne eigenen Befehl") und ERSETZT sie im selben Bild durch einen
-- eigenen kurzen Weg (B.CalmAnswer). Die Engine laesst ein Tier, das einen Laerm gemerkt hat und sich bewegt, nicht neu fliehen
-- (das "Schild", dec/IsoAnimal.java:765-769) -- deshalb ein Ersatzweg statt eines Halts, und waehrend der Ruhefrist calmMs erneuert
-- B.Hold die Sperre nicht (sie loescht das Schild). Wild / scheu / angefuettert: nichts (sie erschrecken weiter).
-- Seite (Nachbesserung B1c A2): das Stress-Signal ist am Server belegt; "rennt ohne eigenen Befehl" fragt Methoden, die Bandits nur
-- clientseitig ruft -- es gilt deshalb nur im Einzelspieler; am Mehrspieler-Server traegt neben dem Stress-Sprung das Signal "weg vom
-- eigenen Ziel" (B5, nur getX/getY). Testpunkt im Mehrspieler: Server-Log auf "calm tick:" pruefen.
-- Vorbild und Unterschied: der grosse Baer (NCBearTest shared/NCBearFight.lua:28-38, fleeStop) haelt an, weil sein Angriffs-Clip
-- nicht neu starten darf; das Junge hat keinen solchen Clip (forschung_b1c.md 2.2). An NCBearFight wird nichts geaendert.
--
-- ZOMBIES: fleeZombies bleibt false (shared/BanditsNPCBearDefs.lua). Je Hirn-Takt EINE Suche fuer alle geladenen Jungen
-- (B.GuardScan -> B.ZedNear, server/BanditsNPCBearWorld.lua). Das gezaehmte Junge mit erreichbarem Besitzer VERSTECKT sich hinter
-- ihm (dem Zombie abgewandt), sonst und fuer wilde / scheue / angefuetterte: fliehen (B.GuardStep, Regeln B.GuardDecide in
-- shared/BanditsNPCBearRules.lua). Zombies greifen in B1c nicht an (B5a).
--
-- Engine-Aufrufe hier (Fundstelle je am Aufruf): getStress, getActionStateName, getVariableBoolean, getX/getY, isExistInTheWorld,
-- isDead, Events.OnTick.Add. Bewegung nur ueber B.MoveTo / B.Hold (World.lua). Ladefolge: diese Datei laedt nach ...Follow und vor
-- ...Heal / ...Registry / ...Ride / ...Server / ...World -- fremde Funktionen nur zur Laufzeit ueber B.X.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._calm = B._calm or {}             -- [id] = { a, seen, stress, side, hits = { ms, ... }, n, last = { why, kind, at, tx, ty } } (Deckel calmMax)
B._calmN = B._calmN or 0            -- Anzahl in B._calm
B._calmHits = B._calmHits or 0      -- Antworten gesamt (Diagnose, Bench)
B._zed = B._zed or {}               -- [id] = { x, y, d, at }: naechster Zombie je geladenem Jungen (aus B.GuardScan)
B._zedFrom = B._zedFrom or 0        -- rollender Anfang in der Zombie-Liste (B.ZedNear)
B._hot = B._hot or false            -- irgendein Junges hat einen Zombie in zedSense -> Hirn-Takt je zedTickMs

-- ---------------------------------------------------------------------------
-- Laerm-Wache
-- ---------------------------------------------------------------------------

-- Ein Junges aus der Wache nehmen (Einsteigen, Herholen, Schliessen).
function B.CalmDrop(id)
    if id == nil or B._calm[id] == nil then return end
    B._calm[id] = nil
    B._calmN = (B._calmN or 1) - 1
    if B._calmN < 0 then B._calmN = 0 end
end

-- Aus liveRec je Hirn-Takt fuer ein geladenes, lebendes, gezaehmtes, nicht mitfahrendes Junges. Deckel calmMax.
function B.CalmWatch(rec, a, ms)
    if type(rec) ~= "table" or not a or rec.st ~= "tame" or rec.ride ~= nil then return end
    local w = B._calm[rec.id]
    if w == nil then
        if (B._calmN or 0) >= (tonumber(B.CFG.calmMax) or 8) then
            B.ErrEvery("calmfull", 60000, "calm: more than " .. tostring(B.CFG.calmMax) .. " tamed cubs loaded, "
                .. tostring(rec.id) .. " is not watched for noise")
            return
        end
        w = { hits = {}, side = 1, n = 0 }
        B._calm[rec.id] = w
        B._calmN = (B._calmN or 0) + 1
    end
    if w.a ~= a then
        w.a = a
        w.stress = nil
    end
    w.seen = ms
end

-- Punkt im Abstand d von P auf der Geraden P -> C (wie shared/BanditsNPCBearRules.lua toward).
local function toward(px, py, cx, cy, d)
    local dx, dy = cx - px, cy - py
    local len = math.sqrt(dx * dx + dy * dy)
    if len < 0.001 then return px + d, py end
    return px + dx / len * d, py + dy / len * d
end

-- Naechster anwesender Besitzer (Eintrag aus B.Players()).
local function ownerOf(rec, players)
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

-- Antwort auf eine fremde Flucht, SOFORT im selben Bild (PLAN_B1C.md 1.2 Schritt 3). Deckel noiseAnswerMax je noiseAnswerWinMs.
-- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; isDead am Tier:
-- server/Traps/STrapGlobalObject.lua:238; getX/getY am Tier: shared/Definitions/animal/ButcheringUtil.lua:575-576.
-- Rueckgabe: true, wenn ein Befehl hinausging.
function B.CalmAnswer(rec, a, w, ms, why)
    local cfg = B.CFG
    local keep = {}
    local hits = w.hits or {}
    for i = 1, #hits do
        local h = hits[i]
        if ms - h >= 0 and ms - h < cfg.noiseAnswerWinMs then keep[#keep + 1] = h end
    end
    w.hits = keep
    if #keep >= cfg.noiseAnswerMax then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local s = B.Ses(rec.id)
    local cx, cy = a:getX(), a:getY()
    local kind, tx, ty
    local walk = false
    local g = s.g
    if type(g) == "table" and g.on == true and g.tx ~= nil and g.ty ~= nil then
        -- die Zombie-Wache laeuft: deren Ziel neu (rennen)
        kind, tx, ty = "guard", g.tx, g.ty
    else
        local players = B.Players()
        local o = ownerOf(rec, players)
        local follow = B.ModeOf(rec) == "follow"
        local sameLevel = o ~= nil and math.floor(o.z or 0) == math.floor(rec.z or 0)
        -- Nachbesserung B1e B5 (Z2): Zuschlag mit der Koerperlaenge wie B.FollowDecide (followStart + gap, followGap + gap; nur der
        -- grosse Koerper, beim Jungen 0). Nur Tabellen-Lesen (shared/BanditsNPCBearStats.lua).
        local gap = 0
        if rec.st == "tame" and B.BodyGap and B.BodyNow then
            local bd, bsz = B.BodyNow(rec)
            gap = B.BodyGap(bd, bsz)
        end
        if follow and o ~= nil and o.car ~= true and sameLevel and B.DistXY(cx, cy, o.x, o.y) > cfg.followStart + gap then
            -- folgt und der Besitzer ist da: der Folgen-Laufbefehl (rennen, wie Regel 16)
            kind = "follow"
            tx, ty = toward(o.x, o.y, cx, cy, cfg.followGap + gap)
        else
            -- gehender Ersatzweg calmGap Kacheln: Richtung Besitzer (folgt) bzw. Heimat (bleibt), nah dran seitlich
            local ax, ay = nil, nil
            if follow then
                if o ~= nil and sameLevel then ax, ay = o.x, o.y end
            elseif rec.hx ~= nil and rec.hy ~= nil then
                ax, ay = rec.hx + 0.5, rec.hy + 0.5
            end
            local side = 1
            if w.side == 1 then side = -1 end
            w.side = side
            kind, walk = "walk", true
            tx, ty = B.CalmSpot(cx, cy, ax, ay, cfg.calmGap, side)
        end
    end
    local moved = B.MoveTo(rec, a, tx, ty, rec.z, { force = true, walk = walk, watch = false })
    if not moved then return false end
    s.calmUntil = ms + cfg.calmMs
    keep[#keep + 1] = ms
    w.n = (tonumber(w.n) or 0) + 1
    w.last = { why = why, kind = kind, at = ms, tx = tx, ty = ty }
    B._calmHits = (B._calmHits or 0) + 1
    B.Log("calm: " .. tostring(rec.id) .. " noise answered (" .. tostring(why) .. ", " .. tostring(kind) .. ")")
    return true
end

-- Rumpf des OnTick (PLAN_B1C.md 1.2 Schritt 2-3). Je Bild und beobachtetem Jungen hoechstens 4 Engine-Aufrufe:
-- a:getStress() (Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:17; am Server erreicht ueber update() :127 -> milk() :60);
-- ohne Sprung dann JE NACH LAGE:
-- (a) eigener Befehl laeuft (Nachbesserung B1c B5): beim FOLGEN und einem RENN-Befehl a:getX()/getY() (Vanilla
--     shared/Definitions/animal/ButcheringUtil.lua:575-576) -- ist das Tier um mehr als ownAway Kacheln weiter vom eigenen Ziel weg als
--     beim Befehl (s.td0 aus B.MoveTo), flieht es ("away"). Das faengt die Flucht auch, wenn der Engine-Stress am Deckel 100 steht und
--     keinen Sprung mehr macht (dec/IsoAnimal.java:2367-2368). Nach einer solchen Antwort ownAwayQuietMs Ruhe (ein Umweg um ein
--     Hindernis loest hoechstens eine Antwort aus; die neue Antwort misst ab dort neu). Beim Bleiben und beim Gehen nicht (Umwege
--     zur Heimat sollen nie eine Schleife bauen).
-- (b) kein eigener Befehl, NUR IM EINZELSPIELER (Nachbesserung B1c A2: Bandits ruft beide Methoden nur clientseitig, am Tier ist
--     nur der gespielte Einzelspieler belegt): a:getActionStateName() (Bandits shared/ZombieActions/ZASmack.lua:486, Methode des
--     Charakters; am Tier NCBearTest shared/NCBearFight.lua:1099), im idle-Bild a:getVariableBoolean("bPathfind") (Bandits
--     shared/ZombieActions/ZAMove.lua:61) und nur, wenn es sich bewegt, a:getVariableBoolean("animalRunning") (gleiche Methode,
--     gleiche Argumenttypen; dass der Name den Engine-Merker trifft, steht nur im Jar -- deshalb nur Zusatzsignal neben dem belegten
--     Stress-Sprung, forschung_b1c.md 2.3). Am Mehrspieler-Server gelten der Stress-Sprung und (a); Testpunkt "calm tick:" im Log.
-- Wandern geht (animalRunning false, Jar dec/BaseAnimalBehavior.java:167), Flucht rennt. Der Q-Ruf mit Akzeptanz >= 40 ruft in der
-- Engine NUR pathToLocation zum Spieler (dec/IsoAnimal.java:783-784, kein Stress-Sprung) und laesst animalRunning, wie es ist -- nach
-- einem eigenen Rennbefehl (fleeTo setzt true, dec/IsoAnimal.java:2525) kommt es also RENNEND und gilt im Einzelspieler als (b)
-- "rennt ohne eigenen Befehl": beim Folgen harmlos (die Antwort laeuft ohnehin zum Besitzer), ein BLEIBENDES Junges kommt auf Q dann
-- nicht (Nachbesserung B1c B6; Kevins Wort offen). Eintraege mit seen aelter als 3 x brainMs, ohne Eintrag, nicht mehr gezaehmt oder
-- mitfahrend fallen heraus (Lebend-Frage nur in der seltenen Antwort).
local function calmTickBody()
    if (B._calmN or 0) <= 0 then return end
    local reg = B.Reg()
    if not reg then return end
    local cfg = B.CFG
    local ms = getTimestampMs()                 -- Vanilla server/Foraging/forageServer.lua:456
    local old = (tonumber(cfg.brainMs) or 1500) * 3
    local drop = nil
    for id, w in pairs(B._calm) do
        local rec = reg.cubs[id]
        local seen = tonumber(w.seen)
        if rec == nil or rec.st ~= "tame" or rec.ride ~= nil or w.a == nil or seen == nil or ms - seen > old or ms - seen < 0 then
            drop = drop or {}
            drop[#drop + 1] = id
        else
            local a = w.a
            local stress = a:getStress()
            local why = nil
            if w.stress ~= nil and stress - w.stress >= cfg.noiseStressJump then why = "jump" end
            w.stress = stress
            if why == nil then
                local s = B._s[id]
                local own = false
                if s ~= nil and s.ownUntil ~= nil then
                    local left = s.ownUntil - ms
                    own = left > 0 and left <= cfg.ownMaxMs
                end
                if own then
                    -- (a) B5: weg vom eigenen Ziel? (nur Folgen + Rennbefehl, Ruhe nach einer solchen Antwort)
                    local d0 = tonumber(s.td0)
                    local quiet = w.awayAt ~= nil and ms - w.awayAt >= 0 and ms - w.awayAt < cfg.ownAwayQuietMs
                    if d0 ~= nil and s.walk ~= true and not quiet and s.tx ~= nil and s.ty ~= nil and B.ModeOf(rec) == "follow" then
                        if B.DistXY(a:getX(), a:getY(), s.tx, s.ty) > d0 + cfg.ownAway then
                            why = "away"
                            w.awayAt = ms
                        end
                    end
                elseif B.IsSP() then
                    -- (b) A2: nur im Einzelspieler
                    local st = a:getActionStateName()
                    local moving = st == "walk" or st == "pathfind" or st == "followwall"
                    if not moving and st == "idle" then moving = a:getVariableBoolean("bPathfind") == true end
                    if moving and a:getVariableBoolean("animalRunning") == true then why = "run" end
                end
            end
            if why ~= nil then B.CalmAnswer(rec, a, w, ms, why) end
        end
    end
    if drop then
        for i = 1, #drop do B.CalmDrop(drop[i]) end
    end
end

-- pcall um EIGENEN Code wie B.BrainTick (server/BanditsNPCBearServer.lua): ein Fehler je Bild kommt laut, aber gedrosselt
-- (B.ErrEvery), nie verschluckt. pcall ist eine Lua-Grundfunktion, keine Engine-Methode.
function B.CalmTick()
    local ok, err = pcall(calmTickBody)
    if not ok then B.ErrEvery("calm", 60000, "calm tick: " .. tostring(err)) end
end

-- Events.OnTick.Add: Vanilla server/Foraging/forageServer.lua:502 (Server-Ordner). Ueber eine kleine Huelle, damit eine spaeter
-- ersetzte B.CalmTick gilt.
Events.OnTick.Add(function() B.CalmTick() end)

-- ---------------------------------------------------------------------------
-- Zombie-Wache
-- ---------------------------------------------------------------------------

-- Eine Zombie-Suche fuer alle geladenen Jungen dieses Hirn-Takts. live = { { rec, a, x, y, z }, ... }. Ergebnis B._zed[id] und
-- B._hot. War die Zellenliste laenger als zedScanMax (rollender Anfang), gilt die letzte Sichtung eines Jungen noch zedKeepMs.
-- Eintraege ohne lebendes Objekt fallen aus B._zed.
function B.GuardScan(live, ms)
    local cfg = B.CFG
    local old = B._zed or {}
    local new = {}
    local hot = false
    local n = type(live) == "table" and #live or 0
    if n > 0 then
        local points = {}
        for i = 1, n do points[i] = { x = live[i].x, y = live[i].y, z = live[i].z } end
        local res, _, partial = B.ZedNear(points, cfg.zedSense, cfg.zedScanMax)
        for i = 1, n do
            local e = live[i]
            local id = e.rec.id
            local z = res[i]
            if z then
                new[id] = { x = z.x, y = z.y, d = z.d, at = ms }
            elseif partial then
                local o = old[id]
                local at = o and tonumber(o.at) or nil
                if at ~= nil and ms - at >= 0 and ms - at < cfg.zedKeepMs then
                    local d = B.DistXY(e.x, e.y, o.x, o.y)
                    if d <= cfg.zedSense then new[id] = { x = o.x, y = o.y, d = d, at = at } end
                end
            end
            if new[id] then hot = true end
        end
    end
    B._zed = new
    B._hot = hot
end

-- Ein Hirn-Takt der Zombie-Wache fuer ein geladenes, lebendes Junges (aus liveRec, VOR Folgen und B.Decide).
-- env = buildEnv (env.owner = naechster Besitzer { key, x, y, z, dist, car, ... } nur bei st "tame"). Rueckgabe true = dieser Takt ist
-- erledigt (liveRec ruft dann weder B.FollowStep noch B.Decide). Ausnahme (Zusatz, schnittstelle_aenderungen.md "B1c KERN"): ein
-- folgendes gezaehmtes Junges, dessen Besitzer im Fahrzeug sitzt und nah genug zum Einsteigen ist, steigt ein (false) -- das Auto
-- ist das beste Versteck. getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576.
-- B1e (PLAN_B1E.md 1.5, 6.3): beim gezaehmten Eintrag traegt c.gap den Zuschlag mit der Koerperlaenge (B.BodyGap mit Koerper und
-- Groesse aus B.BodyNow(rec), nur grosser Koerper) -- das Versteck liegt dann weiter hinter dem Besitzer; sonst 0.
function B.GuardStep(rec, a, env, ms, players)
    if type(rec) ~= "table" or not a then return false end
    local cfg = B.CFG
    local s = B.Ses(rec.id)
    local g = s.g
    local z = B._zed and B._zed[rec.id] or nil
    if z == nil and (type(g) ~= "table" or g.on ~= true) then return false end
    if type(g) ~= "table" then
        g = {}
        s.g = g
    end
    local o = nil
    if rec.st == "tame" and env then o = env.owner end
    if o ~= nil and o.car == true and B.ModeOf(rec) == "follow" and (tonumber(o.dist) or 999) <= B.Opt("BearRideDistance") then
        return false
    end
    local cx, cy = a:getX(), a:getY()
    local zz = nil
    if z then zz = { x = z.x, y = z.y, d = B.DistXY(cx, cy, z.x, z.y) } end
    local wasOn = g.on == true
    local prevMode = g.mode
    local gap = 0
    if rec.st == "tame" and B.BodyGap and B.BodyNow then
        local bd, bsz = B.BodyNow(rec)          -- Nachbesserung B1e A3: Mehrfachrueckgabe erst in Locals (CLAUDE.md 5)
        gap = B.BodyGap(bd, bsz)
    end
    local d = B.GuardDecide({ x = cx, y = cy, z = rec.z, st = rec.st, gap = gap }, o, zz, g, ms)
    -- F1 (PLAN_F1.md 5.3): Wache an/aus -> die Sicht (hide) geht neu hinaus; ein sitzender Baer steht dafuer auf (Sitz-Treiber der Clients)
    if (g.on == true) ~= wasOn then B.Touch(rec) end
    if d.act == "none" then
        if wasOn then B.Log("guard: " .. tostring(rec.id) .. " is safe again") end
        g.tx, g.ty, g.orderAt = nil, nil, nil
        return false
    end
    if not wasOn or prevMode ~= d.mode then
        if d.mode == "hide" then
            B.Log("guard: " .. tostring(rec.id) .. " hides behind its owner from a zombie at " .. tostring(B.Round1(zz and zz.d or -1)))
        elseif d.mode == "flee" then
            B.Log("guard: " .. tostring(rec.id) .. " flees from a zombie at " .. tostring(B.Round1(zz and zz.d or -1)))
        end
    end
    if d.act == "keep" then return true end
    if d.act == "hold" then
        B.Hold(rec, a, true)
        return true
    end
    -- hide / flee: rennen; neuer Befehl nur, wenn das Ziel um guardRepath wanderte, der letzte guardRenewMs alt ist oder die Art wechselte
    local wandered = g.tx == nil or g.ty == nil or B.DistXY(g.tx, g.ty, d.tx, d.ty) >= cfg.guardRepath
    local age = nil
    if g.orderAt ~= nil and ms - g.orderAt >= 0 then age = ms - g.orderAt end
    local renew = age == nil or age >= cfg.guardRenewMs
    if wandered or renew or prevMode ~= d.mode then
        local moved = B.MoveTo(rec, a, d.tx, d.ty, rec.z, { minMs = cfg.guardMoveMs, watch = false })
        if moved then
            g.tx, g.ty, g.orderAt = d.tx, d.ty, ms
        end
    end
    return true
end
