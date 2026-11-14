--
-- NUR TESTHILFE fuer die Lebensanzeige Vorlage B (Lauf baer-hp-b, 14.11.2026; client/ISUI/BanditsNPCBearHpBar.lua). Wird NIE nach NPC Crew kopiert
-- (NCBearBench*). Kein Kern-Code ruft diese Datei. Jeder Befehl nimmt den EIGENEN naechsten gezaehmten Baeren und geht ueber dieselben Wege wie
-- das Spiel: Treffer ueber B.BearHurt (die EINE Schadens-Stelle des Schreibers: Ausweichen, Fx "hurt" mit pts, Festschreiben), Leben ueber
-- B.GrowSetHp (wie NCBear_CubHurt), Hunger / Durst ueber den Probeweg B.NeedsSet (wie NCBear_CubNeeds). Die Anzeige sieht davon nur die Sicht und
-- das Fx-Ereignis -- genau wie im Spiel.
-- NUR EINZELSPIELER ("not isServer() and not isClient()"): im Mehrspieler sagt jeder Befehl "singleplayer only".
--
-- Konsole:
--   NCBear_HpHit(pts)        ein echter Treffer mit pts Lebenspunkten (Vorgabe 28) -- Wackeln, Blitz, rote "-28", Nachlauf. Weicht er aus,
--                            steht "DODGE" (dann noch einmal)
--   NCBear_HpHeal(pts)       Leben um pts Punkte hoeher (Vorgabe 12) -- gruene Kreuze, "+12" (die Zahl kommt in ganzen Prozent: bei 400 Leben
--                            in 4er-Schritten)
--   NCBear_HpSet(pct)        Leben auf pct Prozent (1..100): 100 / 60 / 30 / 10 fuer die vier Farbstufen (unter 16 % pulsiert er rot)
--   NCBear_HpHunger(on)      Hunger 100 (true, Vorgabe) bzw. 50 (false) -- Keule, oranger Puls, alle paar Spielminuten "-4"
--   NCBear_HpThirst(on)      dasselbe fuer Durst (Tropfen)
--   NCBear_HpShow()          nur Anzeige: der Treffer-Effekt mit 28 Punkten OHNE Schaden (derselbe Eingang wie das Fx-Ereignis, U.HpBarHurt);
--                            nach 6 s steht wieder das Leben der Sicht (Nachbesserung C3: Z.PRED_MS 6 s)
--   NCBear_HpInfo()          Zustand der Anzeige drucken (Sicht-Leben, Vorhersage, laufende Effekte, Bilder, Masse der Stufe)
--   Verband: wie im Spiel (Rechtsklick "Bandage the bear") -- das Pflaster steht, solange er wirkt.
--
-- Engine-Aufrufe (Fundstelle): getSpecificPlayer(0) V:client/Farming/CFarmingSystem.lua:45; player:Say(Text) V:client/Entity/ISEntityUI.lua:458;
-- player:getX() / getY() V:client/Fishing/TensionUI.lua:11; getTimestampMs() V:client/Foraging/ISBaseIcon.lua:485. Kern zur Laufzeit hinter
-- Existenz-Riegeln. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function out(text)
    print("[NCBear] " .. tostring(text))
end

local function say(text)
    out(text)
    local p = getSpecificPlayer(0)
    if p then p:Say(tostring(text)) end
end

local function f1(v)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%.1f", v)
end

-- mein naechster zahmer Baer (Register) -- oder nil mit einer Zeile
local function mine()
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return nil
    end
    if not B.Reg or not B.PlayerKey or not B.StatsOf then
        out("the bear core is not loaded")
        return nil
    end
    local p = getSpecificPlayer(0)
    local reg = B.Reg()
    if not p or not reg then
        out("no player or registry yet (load a game first)")
        return nil
    end
    local key = B.PlayerKey(p)
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        if rec.st == "tame" and rec.owner == key then
            local dx = (tonumber(rec.x) or 0) - p:getX()
            local dy = (tonumber(rec.y) or 0) - p:getY()
            local d = dx * dx + dy * dy
            if bestD == nil or d < bestD then best, bestD = rec, d end
        end
    end
    if not best then
        say("no tamed bear of yours (NCBear_CubTame(100) first)")
        return nil
    end
    return best, p
end

local function push(p)
    if B.PushView then B.PushView(p) end
end

local function hpLine(rec)
    local st = B.StatsOf(rec)
    local hp = tonumber(rec.hp)
    if hp == nil then return "health unknown / " .. f1(st.hpMax) end
    return "health " .. f1(hp * 100) .. "% = " .. f1(hp * st.hpMax) .. " / " .. f1(st.hpMax)
end

function NCBear_HpHit(pts)
    local rec, p = mine()
    if not rec then return end
    if not B.BearHurt or not B.FindAnimal then
        out("B.BearHurt / B.FindAnimal missing (server/BanditsNPCBearHurt.lua not loaded)")
        return
    end
    local a = B.FindAnimal(rec)
    if a == nil then
        say("your bear has no body near you (walk closer)")
        return
    end
    local v = tonumber(pts) or 28
    if v < 1 then v = 1 end
    if v > 500 then v = 500 end
    local r = B.BearHurt(rec, a, v, "z", nil)
    push(p)
    say("hit " .. f1(v) .. " -> " .. tostring(r) .. ", " .. hpLine(rec))
end

function NCBear_HpHeal(pts)
    local rec, p = mine()
    if not rec or not B.GrowSetHp then return end
    local st = B.StatsOf(rec)
    local most = tonumber(st.hpMax) or 0
    local hp = tonumber(rec.hp)
    if most <= 0 or hp == nil then
        say("health not known yet")
        return
    end
    local v = tonumber(pts) or 12
    B.GrowSetHp(rec, (hp * most + v) / most)
    push(p)
    say("heal +" .. f1(v) .. " -> " .. hpLine(rec))
end

function NCBear_HpSet(pct)
    local rec, p = mine()
    if not rec or not B.GrowSetHp then return end
    local v = math.floor(tonumber(pct) or 50)
    if v < 1 then v = 1 end
    if v > 100 then v = 100 end
    B.GrowSetHp(rec, v / 100)
    push(p)
    say(hpLine(rec))
end

local function need(kind, on)
    local rec, p = mine()
    if not rec then return end
    if not B.NeedsSet then
        out("B.NeedsSet missing (server/BanditsNPCBearNeeds.lua not loaded)")
        return
    end
    local v = 100
    if on == false then v = 50 end
    local got = B.NeedsSet(rec, kind, v)
    push(p)
    say(kind .. " " .. tostring(v) .. " -> " .. tostring(got) .. ", " .. hpLine(rec))
end

function NCBear_HpHunger(on)
    need("hun", on)
end

function NCBear_HpThirst(on)
    need("thr", on)
end

function NCBear_HpShow()
    local rec = mine()
    if not rec then return end
    local U = B.UI
    if not U or not U.HpBarHurt then
        out("the health bar file is not loaded (client/ISUI/BanditsNPCBearHpBar.lua)")
        return
    end
    local ok = U.HpBarHurt(rec.id, 28)
    say("display only: hit effect -28 -> " .. tostring(ok) .. " (false = the bar is not shown right now)")
end

function NCBear_HpInfo()
    local rec = mine()
    if not rec then return end
    local U = B.UI
    out(tostring(rec.id) .. ": " .. hpLine(rec))
    local st = U and U.HpBarState and U.HpBarState(rec.id)
    if not st then
        say("health bar: no display state (option Bar? health bar switch on? bear in view?)")
        return
    end
    local now = getTimestampMs()
    local function ago(t)
        if t == nil then return "-" end
        return tostring(now - t) .. " ms ago"
    end
    out("  view " .. tostring(st.vp) .. "% of " .. tostring(st.most) .. ", seen " .. ago(st.seenAt) .. ", predicted " .. tostring(st.pred)
        .. " (until " .. tostring(st.predUntil and (st.predUntil - now)) .. " ms)")
    out("  hit " .. ago(st.hitAt) .. " (no pts " .. tostring(st.hitNoPts) .. "), heal " .. ago(st.healAt) .. " from " .. tostring(st.healFrom)
        .. ", ghost " .. ago(st.gAt) .. " " .. tostring(st.gFrom) .. " -> " .. tostring(st.gTo))
    out("  hunger " .. tostring(st.hun) .. ", thirst " .. tostring(st.thr) .. ", bandage " .. tostring(st.bnd) .. ", floating numbers " .. tostring(#st.fl)
        .. ", number text " .. tostring(st.numTxt))
    say("health bar: " .. tostring(st.vp) .. "% (console)")
end
