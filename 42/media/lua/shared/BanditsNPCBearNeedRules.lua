--
-- NPC Crew -- Baer, Beduerfnisse, Vertrauen und Schlaf als reine Regeln (F3, PLAN_F3.md 2-4, 6, 19; Kevins Antworten vom 13.11.2026,
-- _arbeit/baer_zaehmen/f3/KEVIN_ANTWORTEN.md -- sie gehen vor dem Plan).
--
-- Rein: keine Engine, nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (Register-Eintrag: nH, nT, nF, tr) und beim
-- Client (Sicht-Eintrag: hun, thr, tir, tru) -- B.NeedOf liest beide. Gelesen werden nur B.CFG (Bloecke "F3" und "K1", shared/BanditsNPCBear.lua),
-- B.Opt (Sandbox BearNeedsPercent), B.GrowSize (shared/BanditsNPCBearStats.lua) und B.ClipMs (shared/BanditsNPCBearFightRules.lua) zur
-- Laufzeit.
--
-- Drei Werte 0..100: Hunger, Durst, Muedigkeit fuellen sich mit dem Druck (0 = gut). Vertrauen -100..+100 (K1, Kevin 13.11. ~21:40: "ich will bei
-- 0 starten und dann bis 100% und bis -100%"; Start 0).
--   K1 (Kevin 14.11. ~02:20 "nach 16std von 0 auf 100"): Hunger UND Durst steigen je GEZAEHLTER Wachstunde um needRiseH (6,25) -- bei jeder
--   Groesse in 16 Wachstunden von 0 auf 100. Die volle Leiste ist die Tagesmenge der Groesse (Kevin ~01:40 / ~01:55, gleitend an statAt
--   0,35 / 0,75 / 1,35, waechst bis Tag 100): Futter nach Saettigung B.HunDayPts = playerHunDay (55,3 Vanilla-Hungerpunkte) x 1,5 / 4 / 12,5
--   (83 / 221 / 691 Punkte), Wasser B.WaterDayL = 6 % von 25 / 80 / 250 kg (1,5 / 4,8 / 15 l). Jedes Futter saettigt nach seinem HungerChange.
--   Muedigkeit steigt wach 2,4 / 2,0 / 1,6 je Spielstunde (ausgewachsen wie die NPC-Crew-Figuren) plus Anstrengung, sinkt im Schlaf
--   10,5 je Stunde. Kevin 13.11.: ab 90 kaempft er nicht mehr und sagt es; bei 100 schlaeft er von selbst ein und schlaeft, bis er bei
--   0 ist; jeder Befehl weckt ihn mittendrin. KEINE Uhrzeiten (kein Nachtfenster, kein Mittagsschlaf). K1 (Kevin 14.11. ~01:10): schlaeft
--   der Besitzer (oder spult er vor), schlaeft der Baer IMMER mit -- aus jedem Modus.
--   Vertrauen (K1, Kevin ~02:50 "Nur Beduerfnisse"): +100 -> Beduerfnisse 25 % langsamer, -100 -> 25 % schneller (0 = neutral, gerade
--   dazwischen); UNTER trRefuse (-70) weigert er sich zu kaempfen; ab trHeart (100) meldet die Sicht trM (das Herz ueber dem Namensschild).
--   Gewinn / Verlust nur noch nach Kevins Regel vom 14.11. ~00:00 (B.TrustDelta; Buchfuehrung je Spieltag beim Schreiber).
-- Tempo: Sandbox BearNeedsPercent (0 = Hunger, Durst, Muedigkeit aus und auf 0 gehalten).
--
-- Ladefolge: shared/ alphabetisch nach ...Bear / ...Crew / ...Defs / ...FightRules / ...Foe / ...Food, vor ...Rules / ...Stats; nichts
-- Fremdes auf Dateiebene. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- ---------------------------------------------------------------------------
-- Kleine Helfer (ohne math.min / math.max)
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

-- Tabelle mit genau so vielen Zahlen wie die Vorgabe, sonst die Vorgabe.
local function numList(t, def)
    if type(t) ~= "table" or #t ~= #def then return def end
    for i = 1, #def do
        if num(t[i]) == nil then return def end
    end
    return t
end

-- Stueckweise gerade durch (xs[i], ys[i]); ausserhalb die Randwerte (wie shared/BanditsNPCBearStats.lua).
local function lerpList(v, xs, ys)
    local n = #xs
    if v <= xs[1] then return ys[1] end
    for i = 2, n do
        if v <= xs[i] then
            local span = xs[i] - xs[i - 1]
            if span <= 0 then return ys[i] end
            return ys[i - 1] + (ys[i] - ys[i - 1]) * (v - xs[i - 1]) / span
        end
    end
    return ys[n]
end

local STAT_AT_DEF = { 0.35, 0.75, 1.35 }
local FOOD_DEF = { 1.5, 4, 12.5 }           -- K1: Vielfaches des Spieler-Tagesbedarfs je Groesse (Kevin ~01:55 "Mitte")
local WEIGHT_DEF = { 25, 80, 250 }          -- K1: Koerpergewicht kg je Groesse (Kevin ~01:40, Claudes Annahme aus den Quellen)
local TIR_DEF = { 2.4, 2.0, 1.6 }
local TRWORD_DEF = { -70, -20, 20, 70 }

local function statAt()
    return numList(B.CFG and B.CFG.statAt, STAT_AT_DEF)
end

-- Innere Groesse eines REGISTER-Eintrags (rec.g); ohne g oder ohne shared/BanditsNPCBearStats.lua: Junges (0,35).
local function sizeOf(e)
    local g = 0
    if type(e) == "table" then g = num(e.g) or 0 end
    local f = B.GrowSize
    if f == nil then return STAT_AT_DEF[1] end
    return f(g)
end

-- ---------------------------------------------------------------------------
-- Tempo-Regler und Werte lesen
-- ---------------------------------------------------------------------------

-- Sandbox BearNeedsPercent als Zahl >= 0 (fehlt B.Opt oder die Option: 100).
function B.NeedsPct()
    local opts = B.OPTS
    if B.Opt == nil or type(opts) ~= "table" or opts.BearNeedsPercent == nil then return 100 end
    local v = num(B.Opt("BearNeedsPercent"))
    if v == nil then return 100 end
    if v < 0 then v = 0 end
    return v
end

-- false = Hunger, Durst und Muedigkeit sind aus (BearNeedsPercent 0): keine Folgen, kein Schlaf aus Muedigkeit.
function B.NeedsOn()
    return B.NeedsPct() > 0
end

-- Feldnamen je Wert: Register / Sicht.
local FIELD = { hun = { "nH", "hun" }, thr = { "nT", "thr" }, tir = { "nF", "tir" }, tru = { "tr", "tru" } }

-- Wert aus einem Register- ODER Sicht-Eintrag; fehlt er (oder ist Unsinn): nil. kind = "hun" / "thr" / "tir" (0..100) / "tru" (K1: -100..100).
function B.NeedOf(e, kind)
    local f = FIELD[kind]
    if type(e) ~= "table" or f == nil then return nil end
    local v = num(e[f[1]])
    if v == nil then v = num(e[f[2]]) end
    if v == nil then return nil end
    if kind == "tru" then return clamp(v, cfg("trMin", -100), cfg("trMax", 100)) end
    return clamp(v, 0, 100)
end

-- ---------------------------------------------------------------------------
-- Tagesmengen, Mahlzeit, Schale, Muedigkeits-Tempo (K1: PLAN_K1.md 1.1, 8; vorher PLAN_F3.md 2.1, 2.2)
-- ---------------------------------------------------------------------------

-- Vanilla-Hungerpunkte, die die VOLLE Leiste (0 -> 100 %) bei dieser Groesse fasst: playerHunDay x foodAt (Junges 83, halbstark 221, ausgewachsen
-- 691; gleitend). Register-Eintrag (Groesse aus rec.g); Sicht-Eintrag: dessen Feld hd.
function B.HunDayPts(e)
    if type(e) == "table" and num(e.hd) ~= nil and num(e.hd) > 0 then return num(e.hd) end
    local c = B.CFG or {}
    return cfg("playerHunDay", 55.3) * lerpList(sizeOf(e), statAt(), numList(c.foodAt, FOOD_DEF))
end

-- Liter Wasser, die die volle Leiste fasst: waterPct x Koerpergewicht weightAt (1,5 / 4,8 / 15 l; gleitend). Sicht-Eintrag: dessen Feld wl.
function B.WaterDayL(e)
    if type(e) == "table" and num(e.wl) ~= nil and num(e.wl) > 0 then return num(e.wl) end
    local c = B.CFG or {}
    return cfg("waterPct", 0.06) * lerpList(sizeOf(e), statAt(), numList(c.weightAt, WEIGHT_DEF))
end

-- So viele Punkte Hunger senkt EINE Mahlzeit (mealPts 20 Vanilla-Hungerpunkte; Junges 24,1, halbstark 9,0, ausgewachsen 2,9). Sicht: Feld meal.
function B.MealPct(e)
    if type(e) == "table" and num(e.meal) ~= nil then return num(e.meal) end
    local d = B.HunDayPts(e)
    if d <= 0 then return 0 end
    return cfg("mealPts", 20) / d * 100
end

-- So viele Punkte Durst senkt EINE Schale (bowlL 0,5 l; Junges 33,3, halbstark 10,4, ausgewachsen 3,3). Sicht-Eintrag: Feld bowl.
function B.BowlPct(e)
    if type(e) == "table" and num(e.bowl) ~= nil then return num(e.bowl) end
    local l = B.WaterDayL(e)
    if l <= 0 then return 0 end
    return cfg("bowlL", 0.5) / l * 100
end

-- Mahlzeiten eines Stuecks Futter: hungerChange = item:getHungerChange() (negativ, Skriptwert / 100: Honig -0,2 -> 1 Mahlzeit,
-- Beere -0,05 -> 0,25, Steak -0,4 -> 2, Wild -0,8 -> 4). Nicht negativ -> 0.
function B.MealsOf(hungerChange)
    local h = num(hungerChange) or 0
    if h >= 0 then return 0 end
    local pts = cfg("mealPts", 20)
    if pts <= 0 then pts = 20 end
    return -h * 100 / pts
end

-- Liter Wasser, die den Durst thr (Punkte) bei dieser Groesse ganz stillen (K1: Junges von 100: 1,5 l; ausgewachsen von 50: 7,5 l).
function B.DrinkNeedL(e, thr)
    local t = num(thr) or 0
    if t <= 0 then return 0 end
    return t / 100 * B.WaterDayL(e)
end

-- K1 (Kevin 14.11. ~02:05 / ~02:10): so viel Prozent seines Tagesbedarfs deckt EIN Stueck Futter (hungerChange = item:getHungerChange(),
-- negativ; Steak -0,4 -> Junges 48,2 %, ausgewachsen 5,8 %). Fuer den Tooltip "satt fuer ~x %" (Client: Sicht-Eintrag mit meal).
function B.FoodDayPct(e, hungerChange)
    return B.MealsOf(hungerChange) * B.MealPct(e)
end

-- Muedigkeit je Spielstunde wach bei dieser Groesse (Register-Eintrag), ohne Tempo-Regler und Vertrauen.
function B.TirRate(e)
    local c = B.CFG or {}
    return lerpList(sizeOf(e), statAt(), numList(c.tirAt, TIR_DEF))
end

-- ---------------------------------------------------------------------------
-- Vertrauen (K1, PLAN_K1.md 2.1; Kevin 13.11. ~21:40, 14.11. ~00:00 und ~02:50)
-- ---------------------------------------------------------------------------

-- Faktor auf das Steigen von Hunger, Durst, Muedigkeit: bei 0 genau 1; darueber gerade bis 1 - trBonus (0,75 bei +100), darunter
-- gerade bis 1 + trMalus (1,25 bei -100). Ohne Wert: 1.
function B.TrustK(e)
    local tr = B.NeedOf(e, "tru")
    if tr == nil then return 1 end
    if tr >= 0 then return 1 - cfg("trBonus", 0.25) * tr / 100 end
    return 1 + cfg("trMalus", 0.25) * (-tr) / 100
end

-- Aenderung des Vertrauens je Ereignis (Kevins endgueltige Regel 14.11. ~00:00 -- wie oft es zaehlt, entscheidet der Schreiber):
--   "pet" (gestreichelt) / "feedfull" (Hunger durch Fuettern aus der Hand auf 0 %) / "drinkfull" (Durst durch Traenken aus der Hand auf 0 %)
--     -> trGain (+0,5; je Quelle hoechstens 1x je Spieltag)
--   "hun90" / "thr90" (Hunger / Durst erreicht trLossAt 90 %) -> trLossNeed (-5; je Wert 1x je Spieltag)
--   "down" (am Boden, Todesschutz) -> trDown (-10, jedes Mal)
--   "weak" (Leben durch Hunger/Durst auf needHpFloor 1 %) -> trLossWeak (-10; 1x je Spieltag)
--   alles andere -> 0 (auch die alten Arten "feed" / "drink": Punkte je Futter gibt es nicht mehr)
local TR_DELTA = { pet = { "trGain", 0.5 }, feedfull = { "trGain", 0.5 }, drinkfull = { "trGain", 0.5 },
                   hun90 = { "trLossNeed", -5 }, thr90 = { "trLossNeed", -5 }, down = { "trDown", -10 }, weak = { "trLossWeak", -10 } }

function B.TrustDelta(kind)
    local d = TR_DELTA[kind]
    if d == nil then return 0 end
    return cfg(d[1], d[2])
end

-- V1 (Kevin 13.11. ~21:40 "Alte Spielstaende umrechnen: neu = (alt - 50) x 2"): alter Wert 0..100 -> neue Skala, geklemmt (44 -> -12,
-- 0 -> -100, 100 -> +100). Unsinn -> trStart. Einmal je Eintrag (die Marke trV fuehrt der Schreiber).
function B.TrustMigrate(old)
    local v = num(old)
    if v == nil then return cfg("trStart", 0) end
    return clamp((v - 50) * 2, cfg("trMin", -100), cfg("trMax", 100))
end

-- ---------------------------------------------------------------------------
-- Folgen (PLAN_F3.md 3.1): je Stufe der SCHLIMMERE der zwei Werte Hunger / Durst -- keine Multiplikation mehrerer Strafen.
-- e = Register- oder Sicht-Eintrag. Rueckgabe { sta, dmg, grow, heal } (Faktoren; alle 1 ohne Werte oder mit BearNeedsPercent 0):
--   ab needHungry (50): Ausdauer-Erholung x 0,5, Schaden x 0,85, Wachsen x 0,5
--   ab needStarve (80): Schaden x 0,7, kein Wachsen, keine Selbstheilung (der Verband wirkt weiter)
--   Muedigkeit ab tirHeavy (70): Ausdauer-Erholung x 0,5
-- ---------------------------------------------------------------------------
function B.NeedK(e)
    local r = { sta = 1, dmg = 1, grow = 1, heal = 1 }
    if not B.NeedsOn() then return r end
    local h = B.NeedOf(e, "hun") or 0
    local t = B.NeedOf(e, "thr") or 0
    local worst = h
    if t > worst then worst = t end
    if worst >= cfg("needStarve", 80) then
        r.sta, r.dmg, r.grow, r.heal = cfg("needStaK", 0.5), cfg("needDmgK2", 0.7), 0, 0
    elseif worst >= cfg("needHungry", 50) then
        r.sta, r.dmg, r.grow = cfg("needStaK", 0.5), cfg("needDmgK1", 0.85), cfg("needGrowK1", 0.5)
    end
    if (B.NeedOf(e, "tir") or 0) >= cfg("tirHeavy", 70) then r.sta = cfg("needStaK", 0.5) end
    return r
end

-- Kaempft er aus eigenem Zustand gerade NICHT? (Kevin 13.11. Antworten 3 und 4.) "trust" = Vertrauen unter trRefuse (weigert sich),
-- "tired" = Muedigkeit ab tirVery (zu muede), sonst nil. "trust" gewinnt. Ob er ueberhaupt kaempfen KANN (Groesse), fragt der Aufrufer.
function B.NoFight(e)
    local tr = B.NeedOf(e, "tru")
    if tr ~= nil and tr < cfg("trRefuse", -70) then return "trust" end
    if B.NeedsOn() then
        local f = B.NeedOf(e, "tir")
        if f ~= nil and f >= cfg("tirVery", 90) then return "tired" end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Woerter (Fenster-Tooltip; die Texte gehoeren der OBERFLAECHE)
-- ---------------------------------------------------------------------------

-- Stufe 1..4: Hunger / Durst ab needPeckish / needHungry / needStarve (25 / 50 / 80), Muedigkeit ab tirTired / tirHeavy / tirVery
-- (40 / 70 / 90). kind = "hun" / "thr" / "tir".
function B.NeedWord(kind, v)
    local x = num(v) or 0
    local a, b, c
    if kind == "tir" then
        a, b, c = cfg("tirTired", 40), cfg("tirHeavy", 70), cfg("tirVery", 90)
    else
        a, b, c = cfg("needPeckish", 25), cfg("needHungry", 50), cfg("needStarve", 80)
    end
    if x >= c then return 4 end
    if x >= b then return 3 end
    if x >= a then return 2 end
    return 1
end

-- Stufe 1..5 des Vertrauens (K1, Frage K-F4: unter -70 misstrauisch / -70..-20 scheu / -20..+20 neutral / +20..+70 vertraut / ab +70 ergeben;
-- B.CFG.trWordAt; die Grenze selbst gehoert zur hoeheren Stufe).
function B.TrustWord(v)
    local x = num(v) or 0
    local at = numList(B.CFG and B.CFG.trWordAt, TRWORD_DEF)
    local level = 1
    for i = 1, 4 do
        if x >= at[i] then level = i + 1 end
    end
    return level
end

-- ---------------------------------------------------------------------------
-- Schlaf (PLAN_F3.md 6, umgebaut nach Kevins Antworten 6c-6e vom 13.11.2026: KEINE Uhrzeiten)
-- ---------------------------------------------------------------------------

-- Soll ein WACHER Baer sich jetzt hinlegen? c = { st, mode, nF, needsOn, ownerAsleep, resume, down, ride, fight, guard, danger, come,
-- stand, busy, lock, calm } (alles Werte; die Wahrheitswerte sammelt der Schreiber aus Register und Sitzung, server/BanditsNPCBearSleep.lua).
-- Rueckgabe: "owner" (der Besitzer schlaeft oder spult vor -> neben ihn legen; K1, Kevin 14.11. ~01:10: "wenn ein spieler schlaeft schlaeft
-- der baer immer mit" -- in JEDEM Modus, nicht nur beim Folgen), "tired" (Muedigkeit ab tirCollapse 100 -> wo er steht;
-- in Bleiben / Sitz / Frei schon ab tirStaySleep, Vorgabe ebenfalls 100; mit resume -- er schlief schon aus Muedigkeit -- solange sie
-- ueber tirWake liegt) oder nil.
-- Nie: nicht gezaehmt, am Boden, mitfahrend, Kampf, Zombie-Wache an, Gefahr in sleepWakeR, Komm her, Aufstehen laeuft, Fuettern /
-- Streicheln laeuft, Sperre nach dem Wecken, Laerm-Antwort laeuft. Mit BearNeedsPercent 0 nur noch "owner".
function B.SleepWant(c)
    if type(c) ~= "table" or c.st ~= "tame" or c.down == true or c.ride == true then return nil end
    if c.fight == true or c.guard == true or c.danger == true or c.come == true or c.stand == true or c.busy == true
        or c.lock == true or c.calm == true then
        return nil
    end
    if c.ownerAsleep == true then return "owner" end
    if c.needsOn == false then return nil end
    local at = cfg("tirCollapse", 100)
    if c.mode ~= "follow" then
        local stay = cfg("tirStaySleep", at)
        if stay < at then at = stay end
    end
    local f = num(c.nF) or 0
    if f >= at then return "tired" end
    -- er schlief schon aus Muedigkeit (Register-Marke slpAt, z. B. vor dem Laden) und ist noch nicht ausgeschlafen: weiterschlafen
    if c.resume == true and f > cfg("tirWake", 0) then return "tired" end
    return nil
end

-- Soll ein SCHLAFENDER Baer aufwachen? c = { why ("tired" / "owner"), nF, needsOn, ownerAsleep, mode, danger }.
-- Rueckgabe: Weck-Grund oder nil, und (zweiter Wert) ein neuer Schlaf-Grund, wenn er aus einem anderen Grund weiterschlaeft:
--   Gefahr -> "alarm" (Aufschrecken).
--   "tired": bei Muedigkeit <= tirWake (0) -> "rested" -- ausser der Besitzer schlaeft noch: dann nil, "owner".
--            Mit BearNeedsPercent 0 (Muedigkeit aus) ebenso.
--   "owner": der Besitzer schlaeft noch -> nil (K1: in jedem Modus). Sonst: ist er selbst bei >= tirCollapse, schlaeft er weiter (nil,
--            "tired"), sonst "ownerup". c.mode wird nicht mehr gebraucht (bleibt erlaubt).
function B.SleepKeep(c)
    if type(c) ~= "table" then return "gone", nil end
    if c.danger == true then return "alarm", nil end
    local withOwner = c.ownerAsleep == true
    local nF = num(c.nF) or 0
    if c.why == "owner" then
        if withOwner then return nil, nil end
        if c.needsOn ~= false and nF >= cfg("tirCollapse", 100) then return nil, "tired" end
        return "ownerup", nil
    end
    if c.needsOn == false or nF <= cfg("tirWake", 0) then
        if withOwner then return nil, "owner" end
        return "rested", nil
    end
    return nil, nil
end

-- Clip-Schluessel (B.CLIPS, shared/BanditsNPCBearFightRules.lua) fuer das Schlafbild: kind = "lie" (hinlegen) / "loop" (Schleife) /
-- "wake" (ruhig aufstehen) / "alarm" (aufschrecken). Mit B.CFG.sleepClips == true die Schlaf-Clips (ab F3b), sonst das Ersatzbild Sitzen
-- (sitdown / sit / standup -- die drei Clips, die jedes GLB hat; kein neuer Wert an NCBearAct, nichts kann stehend erstarren).
local CLIP_SLEEP = { lie = "liedown", loop = "sleep", wake = "wakeup", alarm = "wakealarm" }
local CLIP_SIT = { lie = "sitdown", loop = "sit", wake = "standup", alarm = "standup" }

function B.SleepClip(kind)
    local c = B.CFG
    if c ~= nil and c.sleepClips == true then return CLIP_SLEEP[kind] end
    return CLIP_SIT[kind]
end

-- Liegt er nach sleptMs Schlaf (ab dem Hinlegen) schon eingerollt? Nur mit Schlaf-Clips: nach dem Hinlegen, curlAfterMs und dem Einrollen.
function B.SleepCurled(sleptMs, bd)
    local c = B.CFG
    if c == nil or c.sleepClips ~= true or B.ClipMs == nil then return false end
    local lie = B.ClipMs("liedown", 0, bd) or 2400
    local curl = B.ClipMs("curlin", 0, bd) or 2000
    return (num(sleptMs) or 0) >= lie + cfg("curlAfterMs", 90000) + curl
end

-- So lange haelt der Schreiber den Baeren fuer das Hinlegen still (Clip "lie").
function B.SleepLieMs(bd)
    local f = B.ClipMs
    local v = f and f(B.SleepClip("lie"), 0, bd) or nil
    return v or 1600
end

-- So lange haelt der Schreiber ihn nach dem Wecken still: kind = "wake" (Clip + standPadMs, wie B.StandMs) oder "alarm" (Clip +
-- sleepAlarmPadMs -- Gefahr geht vor). Aus der eingerollten Haltung (B.SleepCurled): ausrollen + aufstehen bzw. der eigene Aufschreck-Clip.
function B.SleepWakeMs(kind, sleptMs, bd)
    local f = B.ClipMs
    local pad = cfg("standPadMs", 1000)
    if kind == "alarm" then pad = cfg("sleepAlarmPadMs", 300) end
    if f == nil then return 1300 + pad end
    if B.SleepCurled(sleptMs, bd) then
        if kind == "alarm" then return (f("wakecurl", 0, bd) or 1400) + pad end
        return (f("curlout", 0, bd) or 2000) + (f("wakeup", 0, bd) or 2200) + pad
    end
    return (f(B.SleepClip(kind), 0, bd) or 1300) + pad
end
