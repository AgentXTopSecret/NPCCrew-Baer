if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Schlafen beim Schreiber (F3, PLAN_F3.md 6, 7 -- umgebaut nach Kevins Antworten vom 13.11.2026,
-- _arbeit/baer_zaehmen/f3/KEVIN_ANTWORTEN.md 2, 3, 6c-6e: sie gehen vor dem Plan).
--
-- Kevin 6c: "schlafen und aufstehen nach seinen mueidgkeitswert wie bei den npc crew's steigt es auf 100% schlaeft er solange bis er
-- auf 0% runter ist ansonsten kann man ihn per folgen wieder aufwecken mitten drinne". Also KEINE Uhrzeiten: kein Nachtfenster, kein
-- Mittagsschlaf, kein getGameTime():getHour(). Geschlafen wird nur
--   "tired": Muedigkeit bei tirCollapse (100) -- wo er steht, in jedem Modus, auch beim Folgen; bis tirWake (0);
--   "owner": sein Besitzer schlaeft (Kevin 6d) -- er geht 1-2 Kacheln neben ihn und legt sich; bis der Besitzer aufwacht.
--   K1 (Kevin 14.11. ~01:10, woertlich: "wenn ein spieler schlaeft schlaeft der baer immer mit legt sich neben dem spieler und wenn der spieler
--   vorspult das spiel dan legt er sich auch zum schlafen hin ausser gegner sind in der naehe dann kaempft er"): aus JEDEM Modus (Folgen,
--   Bleiben, Sitz, Frei), nicht nur beim Folgen. Hingehen nur bis sleepGoR (25) Kacheln auf derselben Ebene, sonst legt er sich, wo er ist;
--   der Weg hat sleepWalkMs (45 s) Frist. Vorspulen meldet der Client als "schlaeft" (Bitte "Sleep", nur Einzelspieler -- OBERFLAECHE).
--   Nach dem Aufwachen ("ownerup") gilt sein Modus wie vorher (Bleiben / Sitz / Frei rechnet wieder B.OrderStep).
-- Wecken (B.SleepStop, die EINE Weck-Stelle): jeder Befehl (B.SetMode: Mode / Come / Call; der Aussehen-Knopf ueber den neuen Koerper),
-- Fuettern / Traenken (Bitte "Wake" bzw. B.FeedComplete / B.DrinkComplete), Gefahr in sleepWakeR Kacheln, ein Treffer (B.BearHurt) oder
-- Laerm (B.CalmAnswer) -- die drei letzten als Aufschrecken. Streicheln und Passiv wecken nicht. Geweckt bleibt die Muedigkeit, wo sie ist.
-- Fuettern / Traenken wecken nur KURZ (Kevin 6e; Nachbesserung C2): schlief er aus Muedigkeit, bleibt die Marke rec.slpAt stehen, und er
-- legt sich nach der Sperre sleepRetryMs wieder hin (s.slpBack: mit Hinlege-Bild, ohne zweite Meldung) und schlaeft weiter bis tirWake
-- (Kevin 6c "schlaeft er solange bis er auf 0% runter ist"). Jeder ANDERE Weck-Grund loescht Marke und Rueckkehr -- auch eine Marke, die
-- nur wartet (nach dem Laden, in einer Sperre; Nachbesserung C3: "Folgen" weckt endgueltig).
-- Kevin 2: vom Zombie geweckt rennt er wokeFleeMs (5 s) schlaftrunken weg (B.FightDecide "woke"), dann kaempft er wie immer -- ausser er
-- ist zu muede (ab tirVery 90) oder weigert sich (Vertrauen).
--
-- Bild: der Schreiber haelt den Baeren nur still (B.Hold je Takt) und meldet slp in der Sicht; das Liege-Bild setzt jeder Client an
-- SEINER Kopie (client/BanditsNPCBearPose.lua, OBERFLAECHE) -- wie beim Sitzen (F1). F3 zeigt den Schlaf mit dem Ersatzbild Sitzen
-- (B.CFG.sleepClips false); F3b bringt die Clips. Der Zustand lebt in der Sitzung (s.slp = { ph "go" / "lie" / "sleep", why, at, hAt,
-- hrs = gezaehlte Stunden DIESES Schlafs }, s.wkUntil / s.wkSpan / s.wka Aufsteh-Halt, s.slpLock / s.slpLockSpan Sperre, s.wokeUntil /
-- s.wokeSpan schlaftrunken, s.slpBack = { x, y } kurz geweckt an dieser Stelle, legt sich wieder hin). Im Register nur rec.slpAt (Einschlafen
-- aus Muedigkeit): nach einem Laden schlaeft er damit weiter, solange die Muedigkeit ueber tirWake liegt -- jedes Wecken ausser Fuettern /
-- Traenken loescht die Marke, und sie verfaellt von selbst mit der Muedigkeit (Lehre NPC Crew "STALE SLEEP FLAG",
-- client/BanditsNPCGuardian.lua, nur gelesen: nie haengt ein Baer an einer alten Marke).
-- Jeder Halt hat eine Frist (nichts haengt): Hinlegen = Clip-Dauer, Aufsteh-Halt = Clip + Frist, Weg zum Besitzer sleepWalkMs, die
-- Schlaf-Meldung des Besitzers veraltet nach ownSleepStaleMs.
-- Mehrspieler: nur der Server entscheidet; ein Client meldet nur, dass SEIN Spieler schlaeft (Bitte "Sleep" -- einen belegten Lua-Weg,
-- auf dem der Server den Schlaf eines Spielers erfaehrt, hat Vanilla nur fuer das Schlafen im FAHRZEUG: der Client sendet
-- "onVehicleSleep", client/ISUI/ISWorldObjectContextMenu.lua:1098, der Server setzt otherPlayer:setAsleep(...),
-- server/ClientCommands.lua:658-661; fuer Bett und Boden gibt es das nicht), und bittet ums Wecken ("Wake"). Eine
-- falsche Meldung legt hoechstens den EIGENEN folgenden Baeren hin. MP ungespielt.
--
-- Engine-Aufrufe hier (Fundstelle am Aufruf): getX / getY am Tier, square:getX() / getY(), getTimestampMs(). Bewegung nur ueber
-- B.MoveTo / B.Hold (server/BanditsNPCBearWorld.lua), Platz ueber B.SpotNear.
-- Ladefolge: server/ alphabetisch nach ...Server, vor ...World; fremde Funktionen nur zur Laufzeit ueber B.X.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._ownSleep = B._ownSleep or {}     -- [Spielerschluessel] = { at }: dieser Spieler schlaeft (Bitte "Sleep"), nur Sitzung, Deckel 64

-- Weck-Grund -> Bild: "wake" (ruhig aufstehen) / "alarm" (aufschrecken); ohne Eintrag kein Bild (Koerper weg / neu).
local WAKE_CLIP = { order = "wake", hand = "wake", rested = "wake", ownerup = "wake", alarm = "alarm", noise = "alarm" }

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------
local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function clamp(v, lo, hi)
    if v < lo then return lo end
    if v > hi then return hi end
    return v
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

-- Uhr u liegt noch vor ms und hoechstens span voraus? (Uhr rueckwaerts oder Unsinn = abgelaufen; haengt nie endlos.)
local function pending(u, ms, span)
    local t = num(u)
    if t == nil or ms == nil then return false end
    local left = t - ms
    return left > 0 and left <= span
end

local function tellOwner(rec, players, n)
    if rec.owner == nil then return end
    local p = B.PlayerByKey(rec.owner, players)
    if p then B.Tell(p, B.NoteBd(n, rec)) end
end

local function standMs()
    if B.StandMs then return B.StandMs() end
    return 2300
end

-- ---------------------------------------------------------------------------
-- Besitzer schlaeft? Aus der Bitte "Sleep" { on = <Wahrheitswert> } (der Client fragt player:isAsleep() und meldet Wechsel und je 30 s
-- neu, client/BanditsNPCBearPose.lua -- OBERFLAECHE). Veraltet nach ownSleepStaleMs ohne Auffrischung (Uhr rueckwaerts = veraltet).
-- ---------------------------------------------------------------------------
function B.OwnerAsleep(pkey, ms)
    if pkey == nil then return false end
    local e = B._ownSleep[pkey]
    if type(e) ~= "table" then return false end
    ms = num(ms) or getTimestampMs()                -- Vanilla server/Foraging/forageServer.lua:456
    local age = ms - (num(e.at) or 0)
    return age >= 0 and age <= cfg("ownSleepStaleMs", 90000)
end

-- Bitte "Sleep" { on }: nur der Typ zaehlt (on muss ein Wahrheitswert sein, sonst still verworfen); dieselbe Meldung hoechstens je askMs.
-- Geglaubt wird nur "MEIN Spieler schlaeft" -- das legt hoechstens den eigenen Baeren hin.
-- Nachbesserung K1 C6 (Pruef-Tor G-K1; CLAUDE.md 4 "was der Server wissen muss, kommt nie aus einem Client-Glauben"): seit K1 friert die
-- Meldung auch Hunger, Durst und Muedigkeit ein -- im Mehrspieler glaubt der Server "on = true" darum nur, wenn ER den Spieler schlafen
-- sieht: player:isAsleep() (Aufruf wie V:shared/TimedActions/ISWakeOtherPlayer.lua:6, am anderen Spieler). Beleg, dass der Server es weiss
-- (Jar nur gelesen, k1/jar/nach/): PlayerPacket.processServer ruft NetworkPlayerAI.parse(PlayerPacket), das setzt ueber
-- NetworkPlayerVariables.setBooleanVariables die Flagge isAsleep (IsoPlayer.setAsleep) -- dieselbe Flagge, die der Client aus isAsleep()
-- schickt. Kommt die Bitte vor der Flagge an, gilt die naechste Auffrischung (je 30 s, client/ISUI/BanditsNPCBearZz.lua U.SleepReport).
-- Einzelspieler: ungeprueft geglaubt (dort zaehlt auch das Vorspulen, und es gibt keinen fremden Client).
function B.HandleSleep(player, args)
    if not player or not B.IsWriter() then return end
    if type(args) ~= "table" or type(args.on) ~= "boolean" then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    local t = B._ownSleep
    if args.on ~= true then
        t[pkey] = nil
        return
    end
    if isServer() and player:isAsleep() ~= true then
        B.Log("sleep: " .. tostring(pkey) .. " reports asleep, the server sees it awake -- ignored")
        return
    end
    local ms = getTimestampMs()
    local e = t[pkey]
    if type(e) == "table" then
        local age = ms - (num(e.at) or 0)
        if age >= 0 and age < (num(B.CFG.askMs) or 500) then return end
        e.at = ms
        return
    end
    local n = 0
    for _, _ in pairs(t) do n = n + 1 end
    if n >= 64 then
        t = {}
        B._ownSleep = t
    end
    t[pkey] = { at = ms }
end

-- ---------------------------------------------------------------------------
-- Zustand lesen
-- ---------------------------------------------------------------------------

-- Schlaeft er (Phase "sleep", nicht beim Hinlegen oder auf dem Weg)? Fuer das Heilen im Schlaf (B.GrowSlow).
function B.IsAsleep(rec)
    local s = type(rec) == "table" and B._s[rec.id] or nil
    local slp = s and s.slp or nil
    return type(slp) == "table" and slp.ph == "sleep"
end

-- Liegt er (Hinlegen oder Schlaf)? Fuer Tausch-Sperre und Sicht.
local function lying(s)
    local slp = s and s.slp or nil
    return type(slp) == "table" and (slp.ph == "lie" or slp.ph == "sleep")
end

function B.IsLying(rec)
    return lying(type(rec) == "table" and B._s[rec.id] or nil)
end

-- Diagnose (nur lesen): { ph, why, sleptMs, lockMs, wokeMs, wakeMs, ownerAsleep } -- alles flach.
function B.SleepInfo(rec, ms)
    local t = {}
    local s = type(rec) == "table" and B._s[rec.id] or nil
    if type(s) ~= "table" then return t end
    ms = num(ms) or getTimestampMs()
    local slp = s.slp
    if type(slp) == "table" then
        t.ph, t.why = slp.ph, slp.why
        t.sleptMs = ms - (num(slp.at) or ms)
    end
    if pending(s.slpLock, ms, num(s.slpLockSpan) or 60000) then t.lockMs = s.slpLock - ms end
    if pending(s.wokeUntil, ms, num(s.wokeSpan) or 10000) then t.wokeMs = s.wokeUntil - ms end
    if pending(s.wkUntil, ms, num(s.wkSpan) or 8000) then t.wakeMs = s.wkUntil - ms end
    t.ownerAsleep = B.OwnerAsleep(rec.owner, ms)
    return t
end

-- ---------------------------------------------------------------------------
-- Abbau der Muedigkeit im Schlaf: tirSleepGround (10,5) je Spielstunde seit dem letzten Abzug -- eigene Uhr slp.hAt in Weltstunden
-- (wie rt.sleepHour der NPC-Crew-Figuren, NPC Crew shared/BanditsNPCPrograms.lua, nur gelesen), je Aufruf hoechstens maxDtH (ein
-- entladener oder angehaltener Baer holt nichts nach). Zaehlt die Schlafstunden des Tages (nur noch Diagnose: K1 hat keinen Schlaf-Bonus). Der Regler BearNeedsPercent
-- skaliert den Abbau NICHT (wie bei der Crew: die Schlaflaenge ist bei jedem Tempo dieselbe). Rueckgabe: gezaehlte Stunden.
-- ---------------------------------------------------------------------------
function B.SleepDrain(rec, s, now)
    local slp = type(s) == "table" and s.slp or nil
    if type(rec) ~= "table" or type(slp) ~= "table" then return 0 end
    now = num(now) or B.Now()
    local at = num(slp.hAt)
    slp.hAt = now
    if at == nil or now <= at then return 0 end
    if slp.ph ~= "lie" and slp.ph ~= "sleep" then return 0 end
    local dt = now - at
    local cap = cfg("maxDtH", 1.0)
    if dt > cap then dt = cap end
    local f = num(rec.nF)
    if f ~= nil then rec.nF = clamp(f - cfg("tirSleepGround", 10.5) * dt, 0, 100) end
    local d = rec.nDay
    if type(d) == "table" then d.s = clamp((num(d.s) or 0) + dt, 0, 24) end
    -- Nachbesserung C9: die Stunden DIESES Schlafs -- laeuft er ueber Mitternacht, nimmt der Tageswechsel sie in den neuen Tag mit
    -- (dayRoll in server/BanditsNPCBearNeeds.lua), sonst gaebe ein Schlaf von 20 bis 4 Uhr nie den Bonus fuer 6 Stunden Schlaf
    slp.hrs = clamp((num(slp.hrs) or 0) + dt, 0, 24)
    return dt
end

-- ---------------------------------------------------------------------------
-- Wecken: die EINE Stelle. why = "order" (Befehl), "hand" (Fuettern / Traenken), "rested" (Muedigkeit 0), "ownerup" (Besitzer wach),
-- "alarm" (Gefahr / Treffer), "noise" (Laerm) -- und ohne Bild: "swap" / "ride" (Koerper weg oder neu), "gone" (am Boden, nicht mehr
-- gezaehmt). Rest-Abbau bis jetzt, Zustand und Register-Marke weg, Aufsteh-Halt (Clip-Dauer aus B.SleepWakeMs; nur wenn er schon lag),
-- Sperre (Gefahr / Laerm sleepDangerLockMs, Befehl / Hand sleepRetryMs), schlaftrunken nach dem Aufschrecken (wokeFleeMs nach dem
-- Halt), Sicht. Doppelte Rufe sind harmlos (ohne Schlaf: false). Rueckgabe: true, wenn er schlief (oder auf dem Weg zum Schlafplatz war).
-- Nachbesserung C2 (Kevin 6e "Fuettern/Traenken weckt kurz", 6c "bis er auf 0% runter ist"): "hand" beendet einen Schlaf aus Muedigkeit
-- nur fuer die Sperre sleepRetryMs -- die Marke rec.slpAt bleibt, s.slpBack merkt die Rueckkehr (B.SleepStep legt ihn danach wieder hin,
-- mit Hinlege-Bild und ohne zweite Meldung). Nachbesserung C3: ohne laufenden Schlaf loescht jeder Grund ausser "hand" eine WARTENDE
-- Marke (und die Rueckkehr) -- ein Befehl nach dem Laden oder in einer Sperre weckt endgueltig.
-- ---------------------------------------------------------------------------
function B.SleepStop(rec, why, ms, players)
    if type(rec) ~= "table" or rec.id == nil then return false end
    local s = B._s[rec.id]
    if type(s) ~= "table" or type(s.slp) ~= "table" then
        if why ~= "hand" then
            rec.slpAt = nil
            if type(s) == "table" then s.slpBack = nil end
        end
        return false
    end
    ms = num(ms) or getTimestampMs()
    local slp = s.slp
    local now = B.Now()
    B.SleepDrain(rec, s, now)
    local lay = slp.ph == "lie" or slp.ph == "sleep"
    s.slp = nil
    if why == "hand" and slp.why == "tired" and lay then
        if rec.slpAt == nil then rec.slpAt = now end
        s.slpBack = { x = rec.x, y = rec.y }
    else
        rec.slpAt = nil
        s.slpBack = nil
    end
    s.wkUntil, s.wkSpan, s.wka = nil, nil, nil
    local clip = WAKE_CLIP[why]
    local hold = 0
    if clip ~= nil and lay and B.SleepWakeMs ~= nil then
        hold = B.SleepWakeMs(clip, ms - (num(slp.at) or ms), rec.body)
        s.wkUntil, s.wkSpan = ms + hold, hold
        if clip == "alarm" then s.wka = true end
    end
    if why == "alarm" or why == "noise" then
        local lock = cfg("sleepDangerLockMs", 30000)
        s.slpLock, s.slpLockSpan = ms + lock, lock
        local woke = hold + cfg("wokeFleeMs", 5000)
        s.wokeUntil, s.wokeSpan = ms + woke, woke
        local d = rec.nDay
        if type(d) == "table" and lay then d.a = (num(d.a) or 0) + 1 end
    elseif why == "order" or why == "hand" then
        local lock = cfg("sleepRetryMs", 60000)
        s.slpLock, s.slpLockSpan = ms + lock, lock
    end
    B.Touch(rec)
    if why == "rested" and lay then tellOwner(rec, players, note("UI_BN_Bear_Note_Rested", nil, nil, "good")) end
    B.Log("sleep: " .. tostring(rec.id) .. " wakes (" .. tostring(why) .. ", was " .. tostring(slp.why) .. "/" .. tostring(slp.ph)
        .. "), tiredness " .. tostring(B.Round1(num(rec.nF) or 0)))
    return true
end

-- Bitte "Wake" { id }: vor dem Fuettern / Traenken eines schlafenden Baeren (aus dem Menue). Nur der Besitzer am eigenen gezaehmten,
-- schlafenden Baeren -- alles andere wird still verworfen (keine Meldung: es gibt nichts zu erklaeren). Drossel wie die anderen Bitten.
function B.HandleWake(player, args)
    if not player or not B.IsWriter() then return end
    local reg = B.Reg()
    if not reg then return end
    if type(args) ~= "table" or type(args.id) ~= "string" then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    local rec = reg.cubs[args.id]
    if rec == nil or rec.st ~= "tame" or rec.owner ~= pkey then return end
    local s = B._s[rec.id]
    if type(s) ~= "table" or type(s.slp) ~= "table" then return end
    local ms = getTimestampMs()
    if not B.AskOk(pkey .. "|Wake|ok", ms) then return end
    B.SleepStop(rec, "hand", ms)
    B.FlushViews()
end

-- ---------------------------------------------------------------------------
-- Hinlegen. resume = er schlief schon vor dem Laden (rec.slpAt): gleich in die Schlaf-Phase, die Sicht meldet sofort slpO (der
-- Pose-Treiber springt in die Schleife statt das Hinlegen noch einmal zu zeigen), keine Meldung. quiet = er war nur kurz geweckt
-- (Fuettern / Traenken, Nachbesserung C2): normales Hinlegen mit Bild, aber keine zweite Meldung "schlaeft ein".
-- ---------------------------------------------------------------------------
local function lie(rec, a, s, why, ms, now, resume, players, quiet)
    local slp = { ph = "lie", why = why, at = ms, hAt = now }
    if resume then
        slp.ph = "sleep"
        slp.at = ms - cfg("sleepOldMs", 5000) - B.SleepLieMs(rec.body)
    end
    s.slp = slp
    s.slpBack = nil
    if why == "tired" then
        if rec.slpAt == nil then rec.slpAt = now end
    else
        rec.slpAt = nil
    end
    s.wkUntil, s.wkSpan, s.wka = nil, nil, nil
    B.Hold(rec, a, true)
    B.Touch(rec)
    -- Kevin kann mit einem folgenden Baeren unterwegs sein, wenn der bei 100 % einschlaeft: ohne Meldung liefe er weiter
    if why == "tired" and not resume and not quiet then tellOwner(rec, players, note("UI_BN_Bear_Note_Collapse", nil, nil, "bad")) end
    B.Log("sleep: " .. tostring(rec.id) .. " lies down (" .. tostring(why) .. (resume and ", resumed" or "")
        .. (quiet and ", back to sleep" or "") .. ") at "
        .. tostring(rec.x) .. "," .. tostring(rec.y) .. ", tiredness " .. tostring(B.Round1(num(rec.nF) or 0)))
end

-- Gefahr nah? Der naechste Zombie bzw. feindliche Bandit aus der EINEN Suche des Hirn-Takts (B._zed, server/BanditsNPCBearGuard.lua
-- B.GuardScan + server/BanditsNPCBearFightFoes.lua B.FoeScan), Abstand von jetzt. getX/getY am Tier: Vanilla
-- shared/Definitions/animal/ButcheringUtil.lua:575-576.
local function dangerNear(rec, a)
    local z = B._zed and B._zed[rec.id] or nil
    if type(z) ~= "table" or num(z.x) == nil or num(z.y) == nil then return false end
    return B.DistXY(a:getX(), a:getY(), z.x, z.y) <= cfg("sleepWakeR", 8)
end

-- Zuschlag mit der Koerperlaenge (nur grosser Koerper; shared/BanditsNPCBearStats.lua). Mehrfachrueckgabe erst in Locals.
local function gapOf(rec)
    if not (B.BodyGap and B.BodyNow) then return 0 end
    local bd, bsz = B.BodyNow(rec)
    return B.BodyGap(bd, bsz)
end

-- Einschlafen (aus B.SleepStep). "owner": steht er weiter als sleepNear vom schlafenden Besitzer (gleiche Ebene, K1: hoechstens sleepGoR), geht
-- er erst auf eine freie Kachel 1-2 neben ihm (B.SpotNear: nie die Kachel des Besitzers, gleicher Raum, ohne Sperre erreichbar) -- Phase "go",
-- hoechstens sleepWalkMs; sonst legt er sich, wo er ist. square:getX()/getY(): Vanilla client/DebugUIs/DebugContextMenu.lua:636.
local function begin(rec, a, s, why, env, ms, players)
    local now = B.Now()
    if why == "owner" then
        local o = env and env.owner or nil
        -- K1: nur hingehen, wenn er erreichbar ist (gleiche Ebene, hoechstens sleepGoR Kacheln) -- sonst legt er sich, wo er ist
        if o ~= nil and (num(o.dist) or 0) > cfg("sleepNear", 2.5) + gapOf(rec) and (num(o.dist) or 0) <= cfg("sleepGoR", 25)
            and math.floor(num(o.z) or 0) == math.floor(num(rec.z) or 0) then
            local sq = B.SpotNear(o.x, o.y, o.z, 2, rec.gen)
            if sq ~= nil then
                local tx, ty = sq:getX() + 0.5, sq:getY() + 0.5
                s.slp = { ph = "go", why = "owner", at = ms, hAt = now, tx = tx, ty = ty }
                B.MoveTo(rec, a, tx, ty, rec.z, { walk = true, watch = false })
                B.Log("sleep: " .. tostring(rec.id) .. " walks next to its sleeping owner")
                return
            end
        end
        lie(rec, a, s, why, ms, now, false, players)
        return
    end
    -- Marke ohne Sitzung (nach dem Laden): gleich in die Schlaf-Phase. Marke MIT s.slpBack (kurz geweckt zum Fuettern / Traenken,
    -- Nachbesserung C2): er legt sich sichtbar wieder hin -- ohne zweite Meldung, solange er noch an der Stelle des Weckens ist
    -- (sleepBackNear Kacheln). Ist er inzwischen mit dem Spieler weitergezogen (Folgen), sagt er es noch einmal: sonst liefe der
    -- Spieler weiter, ohne zu merken, dass der Baer sich wieder hinlegt.
    local resume = rec.slpAt ~= nil
    local bk = s.slpBack
    local back = resume and type(bk) == "table"
    local quiet = back and num(bk.x) ~= nil and num(bk.y) ~= nil and num(rec.x) ~= nil and num(rec.y) ~= nil
        and B.DistXY(rec.x, rec.y, bk.x, bk.y) <= cfg("sleepBackNear", 3)
    lie(rec, a, s, why, ms, now, resume and not back, players, quiet)
end

-- ---------------------------------------------------------------------------
-- Ein Hirn-Takt (aus liveRec in server/BanditsNPCBearServer.lua, nach der Laerm-Wache und "am Boden", direkt VOR B.FightStep): der
-- Schlaf haelt den Baeren, solange keine Gefahr nah ist -- Gefahr weckt, und der Kampf-Entscheid laeuft danach wie immer.
-- env = buildEnv (env.owner = naechster anwesender Besitzer { key, x, y, z, dist, ... } oder nil). Rueckgabe true = dieser Takt ist erledigt.
-- ---------------------------------------------------------------------------
function B.SleepStep(rec, a, env, ms, players)
    -- ohne die Regeln (shared/BanditsNPCBearNeedRules.lua fehlt: Teilkopie) gibt es keinen Schlaf -- der Takt laeuft wie vor F3
    if type(rec) ~= "table" or a == nil or B.SleepWant == nil or B.SleepKeep == nil or B.SleepWakeMs == nil then return false end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    if rec.st ~= "tame" or rec.ride ~= nil or rec.down ~= nil then
        if type(s.slp) == "table" then B.SleepStop(rec, "gone", ms, players) end
        return false
    end
    -- Aufsteh-Halt nach dem Wecken (das Bild "aufstehen" / "aufschrecken" laeuft bei jedem Client)
    if s.wkUntil ~= nil then
        if pending(s.wkUntil, ms, num(s.wkSpan) or 8000) then
            B.Hold(rec, a, true)
            return true
        end
        s.wkUntil, s.wkSpan, s.wka = nil, nil, nil
    end
    local o = env and env.owner or nil
    local mode = B.ModeOf(rec)
    local ownerAsleep = o ~= nil and B.OwnerAsleep(o.key, ms)
    local needsOn = B.NeedsOn()
    local danger = dangerNear(rec, a)
    local slp = s.slp
    if type(slp) == "table" then
        local now = B.Now()
        -- der Abbau zaehlt nur, solange der Besitzer im Spiel ist (wie alle Uhren des Baeren); sonst nur die Uhr nachstellen
        if o ~= nil then B.SleepDrain(rec, s, now) else slp.hAt = now end
        if slp.ph == "go" then
            -- K1: der Weg gilt in jedem Modus (frueher nur beim Folgen)
            if danger or not ownerAsleep then
                s.slp = nil
                return false
            end
            local span = cfg("sleepWalkMs", 45000)
            local late = not pending((num(slp.at) or ms) + span, ms, span)
            if late or B.DistXY(a:getX(), a:getY(), slp.tx, slp.ty) <= cfg("sleepArrive", 1.2) then
                lie(rec, a, s, "owner", ms, now, false, players)
            else
                B.MoveTo(rec, a, slp.tx, slp.ty, rec.z, { walk = true, watch = false, minMs = 4000 })
            end
            return true
        end
        local wake, newWhy = B.SleepKeep({ why = slp.why, nF = rec.nF, needsOn = needsOn, ownerAsleep = ownerAsleep, mode = mode,
                                           danger = danger })
        if wake ~= nil then
            B.SleepStop(rec, wake, ms, players)
            if s.wkUntil ~= nil then
                B.Hold(rec, a, true)
                return true
            end
            return false
        end
        if newWhy ~= nil and newWhy ~= slp.why then
            slp.why = newWhy
            if newWhy == "tired" then rec.slpAt = now else rec.slpAt = nil end
        end
        if slp.ph == "lie" then
            local age = ms - (num(slp.at) or ms)
            if age < 0 or age >= B.SleepLieMs(rec.body) then slp.ph = "sleep" end
        end
        -- die Engine loest die Sperre nach einer Weile von selbst -> je Takt neu (server/BanditsNPCBearWorld.lua B.Hold)
        B.Hold(rec, a, true)
        return true
    end
    -- wach: nach der letzten Gefahr sleepDangerLockMs lang nicht (wieder) hinlegen
    if danger then
        local lock = cfg("sleepDangerLockMs", 30000)
        s.slpLock, s.slpLockSpan = ms + lock, lock
    end
    local g = s.g
    local why = B.SleepWant({
        st = rec.st, mode = mode, nF = rec.nF, needsOn = needsOn, ownerAsleep = ownerAsleep, resume = rec.slpAt ~= nil,
        down = rec.down ~= nil, ride = rec.ride ~= nil,
        fight = type(s.fight) == "table" or s.fstNow ~= nil,
        guard = type(g) == "table" and g.on == true,
        danger = danger,
        come = s.come ~= nil,
        stand = pending(s.standUntil, ms, standMs()),
        busy = pending(s.busyUntil, ms, cfg("busyMs", 20000)),
        lock = pending(s.slpLock, ms, num(s.slpLockSpan) or 60000),
        calm = pending(s.calmUntil, ms, cfg("calmMs", 2500)),
    })
    if why == nil then
        -- eine Register-Marke ohne Grund (ausgeschlafen, waehrend er nicht geladen war; Sandbox 0) verfaellt hier
        if rec.slpAt ~= nil and (not needsOn or (num(rec.nF) or 0) <= cfg("tirWake", 0)) then rec.slpAt = nil end
        if rec.slpAt == nil then s.slpBack = nil end
        return false
    end
    begin(rec, a, s, why, env, ms, players)
    return true
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_F3.md 7; schnittstelle.md K2) -- aus viewEntry, nur gezaehmt und nur mit Sitzung; schreibt nur in t:
-- slp (liegt: ab dem Hinlegen bis zum Wecken; nicht auf dem Weg zum Besitzer), slpO (liegt seit mehr als sleepOldMs -- ein Client, der
-- die Sicht zum ersten Mal bekommt, springt direkt in die Schleife), wka (Aufschrecken laeuft, solange der Aufsteh-Halt haelt).
-- ---------------------------------------------------------------------------
function B.SleepView(rec, t, ms)
    if type(rec) ~= "table" or type(t) ~= "table" or rec.st ~= "tame" then return end
    local s = B._s[rec.id]
    if type(s) ~= "table" then return end
    ms = num(ms) or getTimestampMs()
    if lying(s) then
        t.slp = true
        local age = ms - (num(s.slp.at) or ms)
        if age < 0 or age >= cfg("sleepOldMs", 5000) then t.slpO = true end
    end
    if s.wka == true and pending(s.wkUntil, ms, num(s.wkSpan) or 8000) then t.wka = true end
end
