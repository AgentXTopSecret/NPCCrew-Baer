--
-- NPC Crew -- Baer, Sitzen sichtbar machen (F1, PLAN_F1.md 0.5, 2.3 Nr. 3, 5.6): der Anim-Treiber auf JEDEM Client.
--
-- Der Schreiber haelt den Baeren beim Befehl "Sitz" an seiner Stelle und meldet in der Sicht sit = true, sobald er dort ruhig steht
-- (KERN, B.OrderStep). Jeder Client setzt dann an SEINER lebenden Kopie die Anim-Variable B.ACT ("NCBearAct"): "sitdown" -> nach
-- SIT_DOWN_MS "sit" (Schleife) -> faellt sit weg: "standup" -> nach STAND_UP_MS loeschen. Die drei Knoten (Hinsetzen, Sitzen,
-- Aufstehen) liegen schon im Animset buck/idle (Bedingung NCBearAct = sitdown / sit / standup, PLAN_F1.md 0.5, 11); derselbe Weg wie der
-- gespielte Kampf des grossen Baeren (Kevin 11.11.: "der sitz schonmal viel besser"; Marken loeschen, dann setVariable). Im Mehrspieler wird die
-- Variable nicht uebertragen (forschung_f1.md 4.2 Nr. 2) -- darum setzt jeder Client selbst; im Einzelspieler ist die Kopie das Tier
-- des Schreibers (dasselbe Objekt).
-- NUR nach der Uhr, nie getVariableString (kein Vanilla-Beleg am Tier, PLAN_F1.md 0.5). Waehrend busy (Fuettern/Streicheln) und
-- waehrend DIESES Spiel selbst fuettert (U.PoseHands aus shared/TimedActions/BanditsNPCBearFeedAction.lua, die Aktion setzt "eat")
-- schreibt der Treiber nichts, BEHAELT aber seinen Zustand (Nachbesserung F1 B3). Danach: hat die Fuetter-Aktion B.ACT geloescht, setzt
-- er sich neu hin (sonst fertig); nach dem Streicheln (B.ACT unberuehrt) sitzt er einfach weiter -- kein Hinsetz-Clip aus dem Sitzen;
-- will er nicht mehr sitzen (Befehl waehrenddessen), steht er auf. Im Sitzen setzt der Treiber "sit" alle SIT_RENEW_MS nach (gleicher
-- Wert; heilt ein fremdes clearVariable). Versteckt / faehrt mit -> aufstehen.
-- Aufrufe am Tier: animal:setVariable(Text, Text) V:shared/TimedActions/Animals/ISPetAnimal.lua:43, animal:clearVariable(Text) :48.
-- Takt je 250 ms aus Events.OnTick (V:client/Chat/ISChat.lua:943); Deckel: P nur fuer Kennungen der Sicht (viewMax 16).
-- F2 = B5a (PLAN_F2.md 0.6, 0.7, 4.4, 4.6): der Sitz-Treiber ist der EINZIGE Schreiber von B.ACT je Client und spielt jetzt auch die
-- Kampf-Clips: U.PoseAct(id, act) (aus U.FightFx "act", client/BanditsNPCBearFx.lua) setzt den Clip an der lebenden Kopie und loescht ihn
-- NUR nach der Uhr (B.ClipMs(act, 0,1, bd) aus der EINEN Clip-Tabelle B.CLIPS, shared/BanditsNPCBearFightRules.lua; der Treffer haengt an der
-- Uhr des Schreibers, nicht am Bild). Danach wie bisher: will er laut Sicht sitzen, setzt er sich hin. Sitzen will er bei sit ODER am Boden
-- (dn -- "Am Boden" sieht vorerst aus wie Sitzen, Frage F-G7), nie waehrend eines Kampfs (fst), versteckt, mitfahrend oder beschaeftigt.
-- Hinsetzen / Aufstehen dauern B.ClipMs("sitdown"/"standup", 0,1, bd) (Rueckfall 1700 / 1400 ms, wenn die Tabelle fehlt).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local TICK_MS = 250
local SIT_DOWN_MS = 1700        -- Rueckfall: Clip "Hinsetzen" 1,6 s + Frist (forschung_f1.md 4.1); sonst B.ClipMs("sitdown", 0.1, bd)
local STAND_UP_MS = 1400        -- Rueckfall: Clip "Aufstehen" 1,3 s + Frist; sonst B.ClipMs("standup", 0.1, bd)
local CLIP_PAD_S = 0.1          -- F2: Frist nach jedem Clip (Sekunden, PLAN_F2.md 4.6)
local SIT_RENEW_MS = 2000       -- im Sitzen "sit" so oft nachsetzen (Nachbesserung F1 B3)
local HANDS_MS = 30000          -- eine eigene Fuetter-Aktion sperrt den Treiber hoechstens so lange (falls ihr Ende nie kommt)
local HANDS_MAX = 8             -- Deckel der Liste H
local DONE = "NCBearDone"       -- Marke der Knoten (Ereignis SetVariable am Clip-Ende); vor jedem Wechsel loeschen

-- Zustand je Kennung: { obj, ph = "sitdown" / "sit" / "standup" / "act", t0 = ms, busy, cleared, act, dur }. Nur diese Sitzung.
local P = {}
-- Tiere, die DIESES Spiel gerade selbst fuettert: { obj, t }. Nur diese Sitzung, Deckel HANDS_MAX.
local H = {}
local at = 0

local function act()
    return B.ACT or "NCBearAct"
end

local function phase(e, obj, ph, now)
    obj:clearVariable(DONE)                                     -- ISPetAnimal.lua:48
    obj:setVariable(act(), ph)                                  -- ISPetAnimal.lua:43
    e.ph, e.t0 = ph, now
end

-- F2: Dauer eines Clips in ms aus der EINEN Tabelle (B.ClipMs, KERN) fuer den Koerper bd; fehlt sie oder der Clip: def.
local function clipMs(key, bd, def)
    local f = B.ClipMs
    local v = nil
    if f then v = tonumber(f(key, CLIP_PAD_S, bd)) end
    if v == nil or v <= 0 then return def end
    return v
end

-- F2: Koerper eines Sicht-Eintrags ("cub" / "big"); fehlt bd: Junges.
local function bodyOf(v)
    if type(v) == "table" and v.bd == "big" then return "big" end
    return "cub"
end

-- Fuettert dieses Spiel das Tier gerade selbst (U.PoseHands)? Ein Eintrag ueber HANDS_MS zaehlt nicht mehr.
local function inHands(obj, now)
    for i = 1, #H do
        local h = H[i]
        if h.obj == obj and now - h.t >= 0 and now - h.t < HANDS_MS then return true end
    end
    return false
end

-- Naht zur Fuetter-Aktion (shared/TimedActions/BanditsNPCBearFeedAction.lua start / release, nur auf dem Client, der fuettert; reines
-- Lua): on = true -> der Treiber schreibt an diesem Tier nichts (die Aktion setzt "eat"); sonst hat die Aktion B.ACT geloescht -> ein
-- Eintrag dieses Tiers beginnt neu (setzt sich wieder hin bzw. ist fertig).
function U.PoseHands(obj, on)
    if obj == nil then return end
    local now = getTimestampMs()                                -- V:client/Foraging/ISBaseIcon.lua:485
    local keep = {}
    for i = 1, #H do
        local h = H[i]
        if h.obj ~= obj and now - h.t >= 0 and now - h.t < HANDS_MS then keep[#keep + 1] = h end
    end
    if on == true and #keep < HANDS_MAX then keep[#keep + 1] = { obj = obj, t = now } end
    H = keep
    if on ~= true then
        for _, e in pairs(P) do
            if e.obj == obj then e.cleared = true end
        end
    end
end

-- Ein Eintrag der Sicht, je Takt.
local function step(id, v, now)
    local obj = nil
    if U.CubObj then obj = U.CubObj(id) end                     -- lebende Kopie aus der Balken-Tabelle (kein Suchlauf)
    local e = P[id]
    if obj == nil or (e ~= nil and e.obj ~= obj) then
        P[id] = nil                                             -- keine Kopie oder eine neue (Tausch, Call, Aussteigen): neu beginnen
        e = nil
        if obj == nil then return end
    end
    if v.busy == true or inHands(obj, now) then
        if e ~= nil then e.busy = true end                      -- die Zeitaktion laeuft: nichts schreiben, Zustand behalten
        return
    end
    -- F2 (PLAN_F2.md 4.6): sitzen bei Befehl Sitz ODER am Boden (dn), nie im Kampf (fst), versteckt oder mitfahrend
    local want = (v.sit == true or v.dn == true) and v.hide ~= true and v.ride ~= true and v.fst == nil
    local bd = bodyOf(v)
    if e ~= nil and e.ph == "act" then
        -- F2: ein Kampf-Clip laeuft -- nur nach der Uhr beenden (nie getVariableString); danach wie bisher (setzt sich ggf. wieder hin)
        local dt0 = now - e.t0
        if dt0 >= 0 and dt0 < (e.dur or 0) then return end
        obj:clearVariable(act())                                -- ISPetAnimal.lua:48
        obj:clearVariable(DONE)
        e.act, e.dur, e.busy, e.cleared = nil, nil, nil, nil
        if want then
            phase(e, obj, "sitdown", now)
        else
            P[id] = nil
        end
        return
    end
    if e == nil then
        if not want then return end
        e = { obj = obj }
        P[id] = e
        phase(e, obj, "sitdown", now)
        return
    end
    if e.cleared then
        -- die Fuetter-Aktion hat B.ACT geloescht: er steht -> neu hinsetzen, sonst fertig
        e.cleared, e.busy = nil, nil
        if want then
            phase(e, obj, "sitdown", now)
        else
            obj:clearVariable(DONE)                             -- ISPetAnimal.lua:48
            P[id] = nil
        end
        return
    end
    if e.busy then
        -- nach dem Streicheln (B.ACT unberuehrt): er sass und sitzt weiter, kein Hinsetz-Clip aus dem Sitzen
        e.busy = nil
        if want and e.ph == "sit" then
            obj:setVariable(act(), "sit")                       -- ISPetAnimal.lua:43
            e.t0 = now
            return
        end
    end
    local dt = now - e.t0
    if dt < 0 then dt = 0 end
    if want then
        if e.ph == "sitdown" and dt >= clipMs("sitdown", bd, SIT_DOWN_MS) then
            phase(e, obj, "sit", now)
        elseif e.ph == "standup" then
            phase(e, obj, "sitdown", now)                       -- wieder hinsetzen (Befehl kam erneut)
        elseif e.ph == "sit" and dt >= SIT_RENEW_MS then
            obj:setVariable(act(), "sit")                       -- gleicher Wert; heilt ein fremdes clearVariable (ISPetAnimal.lua:43)
            e.t0 = now
        end
        return
    end
    if e.ph == "sitdown" or e.ph == "sit" then
        phase(e, obj, "standup", now)
    elseif e.ph == "standup" and dt >= clipMs("standup", bd, STAND_UP_MS) then
        obj:clearVariable(act())                                -- ISPetAnimal.lua:48
        obj:clearVariable(DONE)
        P[id] = nil
    end
end

-- Je 250 ms (gedrosselt im OnTick). Nur Eintraege der Sicht dieses Spiels (U.Fresh); gezaehmt.
function U.PoseTick()
    local now = getTimestampMs()                                -- V:client/Foraging/ISBaseIcon.lua:485
    if now - at < TICK_MS and now >= at then return end
    at = now
    if not U.Fresh or not U.Fresh() then return end
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return end
    for id, v in pairs(cubs) do
        if type(v) == "table" and v.st == "tame" then step(id, v, now) end
    end
end

-- Neue Sicht: Kennungen vergessen, die sie nicht mehr traegt (erst sammeln, dann loeschen). Deckel P <= Sicht.
function U.PoseOnView()
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return end
    local gone = nil
    for id, _ in pairs(P) do
        local v = cubs[id]
        if v == nil or v.st ~= "tame" then
            gone = gone or {}
            gone[#gone + 1] = id
        end
    end
    if gone then
        for i = 1, #gone do P[gone[i]] = nil end
    end
end

-- F2 (PLAN_F2.md 4.4, 4.6): einen Kampf-Clip (oder einen anderen Clip der Tabelle, z. B. "eat") an der lebenden Kopie
-- dieses Clients spielen: Marke NCBearDone loeschen, B.ACT = act setzen, nach B.ClipMs(act, 0,1, bd) wieder loeschen (step). Ein zweiter
-- Clip ersetzt den ersten. Kein Objekt (zu weit, nicht geladen) oder kein Clip in der Tabelle: nichts, Rueckgabe false. Der Treffer haengt
-- nie an diesem Bild (Uhr des Schreibers, PLAN_F2.md 0.6). Aufrufe am Tier wie phase(): ISPetAnimal.lua:43 / :48.
function U.PoseAct(id, actName)
    if id == nil or type(actName) ~= "string" or actName == "" then return false end
    local obj = nil
    if U.CubObj then obj = U.CubObj(id) end
    if obj == nil then return false end
    local cubs = B.View and B.View.cubs
    local v = type(cubs) == "table" and cubs[id] or nil
    local dur = clipMs(actName, bodyOf(v), nil)
    if dur == nil then return false end
    local now = getTimestampMs()                                -- V:client/Foraging/ISBaseIcon.lua:485
    local e = P[id]
    if e == nil or e.obj ~= obj then
        e = { obj = obj }
        P[id] = e
    end
    e.busy, e.cleared = nil, nil
    obj:clearVariable(DONE)                                     -- ISPetAnimal.lua:48
    obj:setVariable(act(), actName)                             -- ISPetAnimal.lua:43
    e.ph, e.t0, e.act, e.dur = "act", now, actName, dur
    return true
end

-- Zum Pruefen (Bench, Attrappe): Phase einer Kennung oder nil.
function U.PosePhase(id)
    local e = P[id]
    return e and e.ph or nil
end

local function onGameStart()
    P = {}
    H = {}
    at = 0
end

Events.OnTick.Add(U.PoseTick)                                   -- V:client/Chat/ISChat.lua:943
Events.OnGameStart.Add(onGameStart)                             -- V:client/Chat/ISChat.lua:1186
