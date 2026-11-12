if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Befehle aus dem Baeren-Fenster (F1, PLAN_F1.md 0.3, 0.6-0.8, 2.2-2.6, 4b, 5.4, 7.2):
-- Bleiben (steht still an der Stelle), Sitz (setzt sich und bleibt sitzen), Frei herumlaufen (bummelt im Kreis um die Stelle des
-- Befehls, nie hinaus), Komm her (laeuft zum Besitzer und wartet dort), Passiv (Schalter je Baer, wirkt erst mit dem Kampf B5a) und
-- C1: ein zahmer Baer ohne Koerper in geladener Gegend bekommt von selbst wieder genau EINEN Koerper.
--
-- Nur der Schreiber rechnet (Einzelspieler: das eine Programm; Mehrspieler: der Server). Ein Client bittet nur ("Mode", "Come",
-- "Passive"); Besitz, Zustand und Lage stehen im Register. Bewegung nur ueber B.MoveTo (rennen = fleeTo, gehen = pathToLocation mit
-- Kevins Wort) und B.Hold (setBlockMovement) aus server/BanditsNPCBearWorld.lua; ein neuer Koerper nur ueber B.PlaceCub
-- (server/BanditsNPCBearRide.lua -> B.CreateCub). Das Sitzen selbst (Anim-Variable an der Kopie jedes Clients) zeichnet die
-- OBERFLAECHE nach der Sicht (sit = true); der Schreiber haelt den Baeren nur still und meldet, wann er ruhig an seiner Stelle steht.
-- Eigene Engine-Aufrufe hier: getX/getY am Tier (Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576), player:getVehicle()
-- (Vanilla server/Vehicles/VehicleCommands.lua:11), getX/getY am Spieler (Bandits server/BanditServerSpawner.lua:179),
-- square:getX()/getY()/getZ() (Vanilla server/Map/SGlobalObjectSystem.lua:89, am Server; Nachbesserung F1 A6), ZombRand(n) (Vanilla
-- shared/TimedActions/Animals/ISMilkAnimal.lua:25), getTimestampMs (Vanilla server/Foraging/forageServer.lua:456).
--
-- Ladefolge: nach ...Follow / ...Grow / ...Guard / ...Heal, vor ...Registry / ...Ride / ...Server / ...World (alphabetisch). Auf
-- Dateiebene wird nichts eingefangen; jede fremde Funktion wird zur Laufzeit ueber B.X geholt.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

local function cfgNum(key, def)
    local c = B.CFG
    local v = c and tonumber(c[key]) or nil
    if v == nil then return def end
    return v
end

-- Uhr u liegt noch vor ms und hoechstens span voraus? (Uhr rueckwaerts oder Unsinn = abgelaufen; haengt nie endlos.)
local function pending(u, ms, span)
    local t = tonumber(u)
    if t == nil or ms == nil then return false end
    local left = t - ms
    return left > 0 and left <= span
end

-- Laeuft ein eigener Laufbefehl noch, der NICHT beim letzten Wechsel auf Bleiben/Sitz/Frei abgeschnitten wurde? B.SetMode merkt dann
-- s.ownCut = s.ownUntil (Nachbesserung F1 B4): sonst liefe ein eben noch folgender Baer bis stayBack weiter und kehrte erst dann um.
-- s.ownUntil selbst bleibt stehen (die Laerm-Wache haelt einen Lauf ohne eigenen Befehl fuer eine Flucht, server/BanditsNPCBearGuard.lua).
-- Ein neuer Befehl (B.MoveTo) setzt ein neues s.ownUntil und gilt wieder.
local function ownLive(s, ms)
    if not pending(s.ownUntil, ms, cfgNum("ownMaxMs", 15000)) then return false end
    return s.ownCut == nil or s.ownCut ~= s.ownUntil
end

-- Zuschlag mit der Koerperlaenge (nur grosser Koerper; shared/BanditsNPCBearStats.lua). Mehrfachrueckgabe erst in Locals.
local function gapOf(rec)
    if not (B.BodyGap and B.BodyNow) then return 0 end
    local bd, bsz = B.BodyNow(rec)
    return B.BodyGap(bd, bsz)
end

-- ---------------------------------------------------------------------------
-- Sitz-Ruhe (PLAN_F1.md 2.3 Nr. 2): jede Bewegung (zurueck, eigener Weg, Locken) loescht s.sat; wechselt es, geht die Sicht neu hinaus
-- (B.Touch -> B.FlushViews am Ende des Takts).
-- ---------------------------------------------------------------------------
local function unsit(rec, s)
    s.satAt = nil
    if s.sat == true then
        s.sat = nil
        B.Touch(rec)
        B.Log("order: " .. tostring(rec.id) .. " gets up (moves)")
    end
end

-- Steht er lange genug ruhig an seiner Stelle -> s.sat = true (Sicht sit). Gerufen nur im Sitz und beim Halten.
local function settle(rec, s, ms)
    if s.sat == true then return end
    local at = tonumber(s.satAt)
    if at == nil or ms - at < 0 then
        s.satAt = ms
        return
    end
    if ms - at < cfgNum("sitSettleMs", 800) then return end
    s.sat = true
    s.satAt = nil
    B.Touch(rec)
    B.Log("order: " .. tostring(rec.id) .. " sits down at " .. tostring(rec.x) .. "," .. tostring(rec.y))
end

-- Laufbefehl zur Heimat bzw. in den Kreis (gehend oder rennend nach d.walk), ohne Gegenprobe (ein Halt vor einer Tuer ist kein
-- Fehler). Laeuft schon ein eigener Weg zu (fast) demselben Ziel, kein neuer Befehl -- sonst begaenne der Weg je moveMs von vorn.
local function goBack(rec, a, s, d, ms)
    if ownLive(s, ms) and s.tx ~= nil and s.ty ~= nil and B.DistXY(s.tx, s.ty, d.tx, d.ty) < 1.5 then
        return false
    end
    return B.MoveTo(rec, a, d.tx, d.ty, rec.z, { walk = d.walk == true, watch = false })
end

-- ---------------------------------------------------------------------------
-- Ein Hirn-Takt eines geladenen, lebenden, gezaehmten Baeren im Modus Bleiben / Sitz / Frei (PLAN_F1.md 5.4). Gerufen aus liveRec
-- (server/BanditsNPCBearServer.lua) nach der Zombie-Wache und dem Aufstehen, statt B.Decide. env = buildEnv (lure, mate, owner).
-- Rueckgabe true = erledigt; false fuer "follow" und jeden anderen Zustand (dann B.Decide wie B1a).
-- ---------------------------------------------------------------------------
function B.OrderStep(rec, a, env, ms, players)
    if type(rec) ~= "table" or a == nil or rec.st ~= "tame" then return false end
    local mode = B.ModeOf(rec)
    if mode ~= "stay" and mode ~= "sit" and mode ~= "roam" then return false end
    ms = tonumber(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    -- ein alter Eintrag ohne Heimat (vor B1b gezaehmt): die Stelle von jetzt (rec.x/y/z setzt liveRec aus dem Tier)
    if tonumber(rec.hx) == nil or tonumber(rec.hy) == nil then
        rec.hx, rec.hy, rec.hz = rec.x, rec.y, rec.z
        B.Commit(rec)
    end
    local ownMax = cfgNum("ownMaxMs", 15000)
    local ownBusy = ownLive(s, ms)
    local pauseOver = true
    if mode == "roam" and type(s.roam) == "table" then
        pauseOver = not pending(s.roam.pauseUntil, ms, cfgNum("roamPauseMax", 20000) + ownMax)
    end
    -- getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576
    local c = {
        mode = mode, st = rec.st, x = a:getX(), y = a:getY(), hx = rec.hx, hy = rec.hy, r = tonumber(B.CFG.roamRadius) or 12,
        gap = gapOf(rec), ownBusy = ownBusy, pauseOver = pauseOver, backTried = s.backTried == true,
    }
    local d = B.OrderDecide(c, env)
    if d.act == "none" then return false end
    -- Sitz: an der Stelle angekommen -> das naechste kleine Verruecken darf wieder einmal nachruecken (sonst bleibt der Merker stehen,
    -- und er setzt sich, wo er steht -- auch nach dem Hinsetzen, damit er nicht zwischen Sitzen und Nachruecken pendelt)
    if mode == "sit" and B.DistXY(c.x, c.y, rec.hx + 0.5, rec.hy + 0.5) <= cfgNum("stayNear", 1.5) then s.backTried = nil end
    if d.act == "hold" then
        B.Hold(rec, a, true)
        if mode == "sit" then settle(rec, s, ms) end
        return true
    end
    if mode == "sit" then unsit(rec, s) end
    if d.act == "keep" then return true end
    if d.act == "back" then
        if d.rule == 31 then s.backTried = nil end
        if d.rule == 33 then
            -- einmal nachruecken; danach setzt er sich, wo er steht (sonst stuende er vor einer belegten Kachel fuer immer)
            local throttled = s.moveAt ~= nil and ms - s.moveAt >= 0 and ms - s.moveAt < cfgNum("moveMs", 3000)
            if not throttled then s.backTried = true end
        end
        goBack(rec, a, s, d, ms)
        return true
    end
    if d.act == "come" then
        -- Regel 6 (wie B1a/B1b steer): rennen bis comeFed vor den Besitzer; die Heimat wandert mit (lead)
        local moved = B.MoveTo(rec, a, d.tx, d.ty, rec.z, { watch = false })
        if moved and d.lead then
            rec.hx, rec.hy = math.floor(d.tx), math.floor(d.ty)
            B.Commit(rec)
        end
        return true
    end
    if d.act == "stroll" then
        local roam = s.roam
        if type(roam) ~= "table" then
            roam = {}
            s.roam = roam
        end
        local pMin = cfgNum("roamPauseMin", 8000)
        local pMax = cfgNum("roamPauseMax", 20000)
        if pMax < pMin then pMax = pMin end
        -- ZombRand(n): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:25 (eine Zahl, 0 .. n-1)
        local pause = pMin + ZombRand(math.floor(pMax - pMin) + 1)
        local sq = B.RoamSpot(rec, a, c.r)
        local moved = false
        if sq ~= nil then
            -- square:getX()/getY()/getZ(): Vanilla server/Map/SGlobalObjectSystem.lua:89 (am Server)
            moved = B.MoveTo(rec, a, sq:getX() + 0.5, sq:getY() + 0.5, sq:getZ(), { walk = true, watch = false })
        end
        if moved then
            local own = tonumber(s.ownUntil) or ms
            roam.pauseUntil = own + pause
            B.Log("order: " .. tostring(rec.id) .. " strolls to " .. tostring(sq:getX()) .. "," .. tostring(sq:getY()))
        else
            roam.pauseUntil = ms + pause
            B.Hold(rec, a, true)
        end
        return true
    end
    return false
end

-- ---------------------------------------------------------------------------
-- Aufstehen (PLAN_F1.md 2.3 Nr. 4): nach dem Wechsel weg von einem SITZENDEN Baeren haelt der Schreiber ihn standMs still (der Clip
-- "StandUp" im Animset buck/idle laeuft bei jedem Client). Gerufen aus liveRec nach der Zombie-Wache (ein Zombie geht vor).
-- Rueckgabe true = haelt.
-- ---------------------------------------------------------------------------
function B.StandStep(rec, a, ms)
    if type(rec) ~= "table" or a == nil then return false end
    local s = B._s[rec.id]
    if s == nil or s.standUntil == nil then return false end
    ms = tonumber(ms) or getTimestampMs()
    local stand = 2300
    if B.StandMs then stand = B.StandMs() end         -- F2 (PLAN_F2.md 0.7): aus der Clip-Tabelle B.CLIPS
    if pending(s.standUntil, ms, stand) then
        B.Hold(rec, a, true)
        return true
    end
    s.standUntil = nil
    return false
end

-- ---------------------------------------------------------------------------
-- Komm her, Ankunft (PLAN_F1.md 2.5 Nr. 3): am Anfang von B.FollowStep (server/BanditsNPCBearFollow.lua). Ohne s.come sofort false.
-- Besitzer (nicht im Fahrzeug) naeher als comeNear + Koerper-Zuschlag -> "Bleiben" hier (came); laenger als comeMaxMs oder steckt fest
-- (s.f.stuck aus B.FollowDecide) -> "Bleiben" wo er ist (comefail). Rueckgabe true = B.SetMode lief.
-- ---------------------------------------------------------------------------
function B.ComeCheck(rec, env, ms, players)
    if type(rec) ~= "table" then return false end
    local s = B._s[rec.id]
    local at = s and tonumber(s.come) or nil
    if at == nil then return false end
    ms = tonumber(ms) or getTimestampMs()
    if ms - at < 0 then
        s.come = ms                     -- Uhr rueckwaerts: Messung neu beginnen
        return false
    end
    local o = env and env.owner or nil
    if o ~= nil and o.car ~= true and (tonumber(o.dist) or 999) <= cfgNum("comeNear", 3) + gapOf(rec) then
        B.SetMode(rec, "stay", "came", players)
        return true
    end
    local f = s.f
    if ms - at > cfgNum("comeMaxMs", 30000) or (type(f) == "table" and f.stuck == true) then
        B.SetMode(rec, "stay", "comefail", players)
        return true
    end
    return false
end

-- ---------------------------------------------------------------------------
-- Bitten (PLAN_F1.md 2.5, 2.6). Gemeinsam: Schreiber, Register, Kennung als Text (sonst still verwerfen), Spielerschluessel.
-- Drossel wie "Mode"/"Rename" (B.AskOk, server/BanditsNPCBearFollow.lua): Wirkung je "Spieler|Befehl|ok/no" hoechstens je askMs,
-- gezaehlt erst NACH den Pruefungen. getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
-- ---------------------------------------------------------------------------
local function allow(pkey, command, outcome)
    return B.AskOk(pkey .. "|" .. command .. "|" .. outcome, getTimestampMs())
end

local function refuse(player, pkey, command, n)
    if allow(pkey, command, "no") then B.Tell(player, n) end
end

local function askRec(player, args)
    if not player or not B.IsWriter() then return nil, nil end
    local reg = B.Reg()
    if not reg then return nil, nil end
    if type(args) ~= "table" or type(args.id) ~= "string" then return nil, nil end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return nil, nil end
    return pkey, reg.cubs[args.id]
end

-- "Come" { id }: nur der Besitzer, nur am gezaehmten, geladenen, nicht mitfahrenden Baeren; nicht aus dem Fahrzeug; hoechstens
-- BearFollowMaxDistance weit. Wirkung: Folgen (B.FollowStep) mit s.come = jetzt -> B.ComeCheck macht daraus "Bleiben" beim Besitzer.
-- player:getVehicle(): Vanilla server/Vehicles/VehicleCommands.lua:11; getX/getY am Spieler: Bandits server/BanditServerSpawner.lua:179;
-- am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576.
function B.HandleCome(player, args)
    local pkey, rec = askRec(player, args)
    if pkey == nil then return end
    if rec == nil then
        refuse(player, pkey, "Come", note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    if rec.owner ~= pkey or (rec.st ~= "tame" and rec.st ~= "missing") then
        refuse(player, pkey, "Come", note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return
    end
    if rec.ride ~= nil then
        refuse(player, pkey, "Come", B.NoteBd(note("UI_BN_Bear_Why_Riding", nil, nil, "bad"), rec))
        return
    end
    if rec.down ~= nil then
        -- F2 (PLAN_F2.md 2.4): am Boden erst aufhelfen
        refuse(player, pkey, "Come", B.NoteBd(note("UI_BN_Bear_Why_Down", nil, nil, "bad"), rec))
        return
    end
    local a = nil
    if rec.st == "tame" then a = B.FindAnimal(rec) end
    if a == nil then
        refuse(player, pkey, "Come", B.NoteBd(note("UI_BN_Bear_Why_OutOfReach", nil, nil, "bad"), rec))
        return
    end
    if player:getVehicle() ~= nil then
        refuse(player, pkey, "Come", note("UI_BN_Bear_Why_InCar", nil, nil, "bad"))
        return
    end
    if B.DistXY(player:getX(), player:getY(), a:getX(), a:getY()) > (tonumber(B.CFG.followMaxDist) or 40) then     -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3)
        refuse(player, pkey, "Come", note("UI_BN_Bear_Why_Far", nil, nil, "bad"))
        return
    end
    if not allow(pkey, "Come", "ok") then return end
    B.SetMode(rec, "follow", "come", nil)
    B.Ses(rec.id).come = getTimestampMs()     -- NACH B.SetMode (das loescht s.come); die Sicht traegt cm = true
    B.Touch(rec)
    B.FlushViews()
end

-- "Passive" { id, on }: on muss ein Wahrheitswert sein (sonst still verwerfen). Nur der Besitzer, tame ODER missing (auch mitfahrend).
-- Wirkung in F1: nur gespeichert (Register + Spiegel) und angezeigt; B5a (Kampf) liest rec.passive.
function B.HandlePassive(player, args)
    local pkey, rec = askRec(player, args)
    if pkey == nil then return end
    if type(args.on) ~= "boolean" then return end
    if rec == nil then
        refuse(player, pkey, "Passive", note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return
    end
    if rec.owner ~= pkey or (rec.st ~= "tame" and rec.st ~= "missing") then
        refuse(player, pkey, "Passive", note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return
    end
    if not allow(pkey, "Passive", "ok") then return end
    local k = "UI_BN_Bear_Note_PassiveOff"
    if args.on == true then
        rec.passive = true
        k = "UI_BN_Bear_Note_PassiveOn"
    else
        rec.passive = nil
    end
    B.Commit(rec)
    B.Tell(player, B.NoteBd(note(k, nil, nil, nil), rec))
    B.Log("passive " .. tostring(rec.id) .. " " .. tostring(args.on) .. " by " .. tostring(pkey))
    B.FlushViews()
end

-- ---------------------------------------------------------------------------
-- C1 (PLAN_F1.md 0.8, 4b): ein VERMISSTER Eintrag bekommt von selbst wieder genau EINEN Koerper an seiner letzten Stelle. Gerufen aus
-- brainTickBody direkt nach countMisses, nur wenn in diesem Takt ein Suchlauf lief (B.ScanAnimals hat einen geladenen alten Koerper dann
-- schon gebunden = "erst suchen"). missing = Eintraege aus resolve, die schon VOR diesem Suchlauf "missing" waren.
-- Riegel je Eintrag: noch derselbe Eintrag, st "missing", nicht mitfahrend, Besitzer online, Gegend geladen, kein Koerper gebunden; erst
-- nach reviveScans weiteren vergeblichen Suchlaeufen. Kachel B.SpotNear um SEINE letzte Stelle (nie unstehbar); keine -> Fehlversuch
-- (Fehlerzeile ab reviveFailLog, gedrosselt). Dann B.PlaceCub (gen + 1, st tame, Spiegel sofort, Groesse/Leben, Wunschkoerper).
-- Deckel: hoechstens EIN neuer Koerper je Takt. Ein spaeter auftauchender alter Koerper hat die kleinere Generation -> "stale", wird
-- nie gebunden und unbeobachtet entfernt (server/BanditsNPCBearHeal.lua / ...World.lua). Rueckgabe: Zahl erzeugter Koerper (0/1).
-- Zusatz (schnittstelle_aenderungen.md "F1 KERN"): im MEHRSPIELER erst, wenn der Suchlauf in dieser Sitzung schon einmal einen unserer
-- Baeren in der Objektliste gesehen hat (B._scanSeen, server/BanditsNPCBearWorld.lua B.ScanAnimals) -- getObjectListForLua hat am
-- MP-Server keinen Beleg (A3, offen seit B1a). Saehe der Suchlauf dort nichts, stuende der alte Koerper ungebunden neben dem neuen
-- (Doppel). Bis dahin wartet der Baer auf "Unstuck"; eine gedrosselte Fehlerzeile macht es in Kevins MP-Test sichtbar.
-- Zusatz 2: sah DIESER Suchlauf ein ungebundenes Tier mit der AnimalID des Eintrags (B.ScanAnimals setzt B._aidSeen[id]; weiter als
-- 40 Kacheln oder mehrdeutig, B1b-Riegel 2 "nie raten"), ist das wohl sein echter Koerper: kein neuer Koerper (sonst bliebe der echte als
-- Waise zurueck und wuerde entfernt), gedrosselte Fehlerzeile, Unstuck holt ihn.
-- Nachbesserung F1 B1: die Wartefrist ist ZEIT in geladener Gegend mit anwesendem Besitzer, nicht nur eine Zahl von Suchlaeufen (mit
-- einem zweiten Eintrag ohne Koerper laeuft der Suchlauf je 5 s statt 30 s). s.revAt = erster passender Suchlauf, s.revLast = letzter;
-- ein Suchlauf, in dem der Eintrag nicht passt (Gegend entladen, Besitzer weg, AnimalID gesehen), oder eine Luecke ueber reviveGapMs
-- (Gegend war dazwischen entladen, Spiel angehalten) beginnt die Frist neu -- so bekommt der Tier-Lader nach dem Neuladen Zeit, den alten
-- Koerper zu liefern. Ein neuer Koerper erst nach reviveScans Suchlaeufen UND reviveMs seit revAt, nie im Heil-Fenster nach dem Laden
-- (B._healUntil, server/BanditsNPCBearRegistry.lua). Die Gegend "nicht geladen" setzt auch resolve (server/BanditsNPCBearServer.lua) je
-- Takt zurueck (B.ReviveForget).
-- ---------------------------------------------------------------------------
function B.ReviveForget(rec)
    local s = type(rec) == "table" and B._s[rec.id] or nil
    if s ~= nil then s.revN, s.revAt, s.revLast = nil, nil, nil end
end

function B.ReviveMissing(missing, players, ms)
    local reg = B.Reg()
    if not reg or type(missing) ~= "table" then return 0 end
    players = players or B.Players()
    ms = tonumber(ms) or getTimestampMs()
    local online = {}
    for i = 1, #players do online[players[i].key] = true end
    local need = cfgNum("reviveScans", 2)
    local waitMs = cfgNum("reviveMs", 60000)
    local gapMs = cfgNum("reviveGapMs", 50000)
    local healOpen = ms < (tonumber(B._healUntil) or 0)
    local proven = B.IsSP() or B._scanSeen == true
    local made = 0                       -- Deckel: hoechstens EIN neuer Koerper je Takt; die anderen zaehlen trotzdem weiter (Luecke!)
    for i = 1, #missing do
        local rec = missing[i]
        local eligible = type(rec) == "table" and reg.cubs[rec.id] == rec and rec.st == "missing" and rec.ride == nil
            and rec.owner ~= nil and online[rec.owner] == true and B.AreaLoaded(rec.x, rec.y) and B.FindAnimal(rec) == nil
        if eligible and not proven then
            B.ErrEvery("revive:noscan", 600000, "revive: " .. tostring(rec.id) .. " has no body, but the scan has not seen any bear on"
                .. " this server yet (getObjectListForLua?) -- no new body, Unstuck brings it")
            return 0
        end
        if eligible and type(B._aidSeen) == "table" and B._aidSeen[rec.id] == true then
            -- der Suchlauf sah ein ungebundenes Tier mit seiner AnimalID (weiter als 40 Kacheln oder mehrdeutig, B1b-Riegel 2 "nie raten"):
            -- das ist wohl sein echter Koerper -- kein neuer, keine Waise; Unstuck holt ihn
            eligible = false
            B.ErrEvery("revive:aid:" .. tostring(rec.id), 600000, "revive: " .. tostring(rec.id) .. " has no bound body, but an unbound"
                .. " animal with its animal id is loaded -- no new body, Unstuck brings it")
        end
        if not eligible then
            B.ReviveForget(rec)
        else
            local s = B.Ses(rec.id)
            local last, since = tonumber(s.revLast), tonumber(s.revAt)
            if last == nil or since == nil or ms - last < 0 or ms - last > gapMs or ms - since < 0 then
                s.revN, s.revAt = 0, ms
                since = ms
            end
            s.revLast = ms
            s.revN = (tonumber(s.revN) or 0) + 1
            if made == 0 and s.revN >= need and ms - since >= waitMs and not healOpen then
                local sq = B.SpotNear(rec.x, rec.y, rec.z, B.CFG.callRing, rec.gen)
                local a, why = nil, "nospot"
                if sq ~= nil then
                    -- square:getX()/getY()/getZ(): Vanilla server/Map/SGlobalObjectSystem.lua:89 (am Server)
                    a, why = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), "revive")
                end
                if a ~= nil then
                    B.ReviveForget(rec)
                    s = B.Ses(rec.id)
                    s.revFail = nil
                    local p = B.PlayerByKey(rec.owner, players)
                    if p then B.Tell(p, note("UI_BN_Bear_Note_Back", nil, nil, "good")) end
                    B.Log("revive: " .. tostring(rec.id) .. " has a body again at " .. tostring(rec.x) .. "," .. tostring(rec.y)
                        .. " gen " .. tostring(rec.gen))
                    made = 1
                else
                    s.revFail = (tonumber(s.revFail) or 0) + 1
                    if s.revFail >= cfgNum("reviveFailLog", 3) then
                        B.ErrEvery("revive:" .. tostring(rec.id), 600000, "revive: " .. tostring(rec.id) .. " found no spot for a new"
                            .. " body (" .. tostring(why) .. ", " .. tostring(s.revFail) .. " tries), Unstuck brings it to its owner")
                    end
                end
            end
        end
    end
    return made
end
