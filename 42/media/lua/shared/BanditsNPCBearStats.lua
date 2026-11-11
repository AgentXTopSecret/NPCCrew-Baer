--
-- NPC Crew -- Baer, Wachsen, Werte und Faehigkeiten als reine Formeln (B1d, PLAN_B1D.md 0.2, 0.6, 0.7, 0.10, 6.2).
--
-- Rein bis auf B.ApplySize: nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (Register-Eintrag) und beim
-- Client (Anzeige, Probebefehle der Test-Mod). Gelesen werden nur B.Opt (Sandbox) und B.CFG (Stellwerte, shared/BanditsNPCBear.lua) zur Laufzeit.
--
-- Die Wachstums-Uhr ist rec.g (0..1, gefuehrt beim Schreiber in server/BanditsNPCBearGrow.lua). Daraus wird gerechnet und nie
-- gespeichert (eine Wahrheit): die INNERE Groesse s (stueckweise gerade durch Kevins Tabelle 0,35 / 0,75 / 1,0 / 1,35 an den Tagen
-- 0 / 15 / 45 / 100 bei 100 Tagen, anteilig bei anderer Sandbox-Zahl), die Stufe, alle Werte (Leben, Ausdauer, Traglast, Schaden --
-- sie steigen mit s jeden Tag ein Stueck, Kevin 11.11.2026) und die GEZEIGTE Groesse sz = min(s, B.CFG.cubMaxSize): das
-- Junges-Modell waechst nur bis Halbstark und bleibt dort stehen; der Modellwechsel ist vorbereitet und abgeschaltet (B.BodyOf,
-- B.CFG.bodySwap = false; Kevins Wort offen, Frage F11).
-- Faehigkeiten: je Faehigkeit EINE Zahl (Erfahrung, Felder xAgi ... xNos), die Stufe 0..10 wird immer daraus gerechnet (Lehre aus
-- NPC Crew shared/BanditsNPCSkills.lua:52-59, gelesen, nicht kopiert: nie zwei Wahrheiten). Kurve B.CFG.xpNeed, hinten langsamer.
--
-- Einziger Engine-Weg dieser Datei: B.ApplySize (animal:getData():getSize() / :setSizeForced(Zahl), Belege dort).
-- Ladefolge: nach ...Bear / ...Crew / ...Defs / ...Food / ...Rules (alphabetisch); auf Dateiebene wird nichts Fremdes eingefangen,
-- B.CFG und B.Opt werden erst beim Aufruf gelesen (fehlen sie, gelten die Vorgaben unten).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- ---------------------------------------------------------------------------
-- Kleine Helfer (ohne math.min / math.max)
-- ---------------------------------------------------------------------------

-- Zahl oder nil (Text, NaN, Tabelle -> nil).
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

local function opt(name, def)
    local v = num(B.Opt(name))
    if v == nil then return def end
    return v
end

-- Vorgaben, falls B.CFG fehlt oder eine Tabelle unbrauchbar ist (gleiche Zahlen wie shared/BanditsNPCBear.lua).
local CURVE_DEF = { { 0, 0.35 }, { 0.15, 0.75 }, { 0.45, 1.0 }, { 1.0, 1.35 } }
local STAGE_AT_DEF = { 0.75, 1.0, 1.35 }
local STAGE_KEYS = { "half", "strong", "adult" }
local STAT_AT_DEF = { 0.35, 0.75, 1.35 }
local HP_DEF = { 40, 150, 400 }
local STA_DEF = { 50, 100, 160 }
local CARRY_DEF = { 10, 40, 100 }
local DMG_DEF = { 0, 0.35, 1.0 }
local NEED_DEF = { 100, 116, 135, 156, 181, 210, 244, 283, 328, 380 }

-- Kurve: Liste { x, Groesse } mit steigendem x, mindestens zwei Punkte, alles Zahlen -- sonst die Vorgabe.
local function curve()
    local c = B.CFG and B.CFG.growCurve
    if type(c) ~= "table" or #c < 2 then return CURVE_DEF end
    local lastX = nil
    for i = 1, #c do
        local p = c[i]
        if type(p) ~= "table" or num(p[1]) == nil or num(p[2]) == nil then return CURVE_DEF end
        if lastX ~= nil and p[1] < lastX then return CURVE_DEF end
        lastX = p[1]
    end
    return c
end

-- Tabelle mit n Zahlen, sonst die Vorgabe.
local function numList(t, def)
    if type(t) ~= "table" or #t ~= #def then return def end
    for i = 1, #def do
        if num(t[i]) == nil then return def end
    end
    return t
end

-- Stueckweise gerade durch (xs[i], ys[i]); ausserhalb die Randwerte.
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

-- ---------------------------------------------------------------------------
-- Faehigkeiten: Schluessel, Felder, Erfahrungs-Kurve
-- ---------------------------------------------------------------------------
B.SKILLS = { "agi", "vit", "con", "fgt", "fsh", "nos" }
B.SKILL_FIELD = { agi = "xAgi", vit = "xVit", con = "xCon", fgt = "xFgt", fsh = "xFsh", nos = "xNos" }

-- Summen der Erfahrung bis Stufe L: B.XP_CUM[0] = 0 ... B.XP_CUM[10] (Vorgabe 2133). Gerechnet aus B.CFG.xpNeed; geaendert jemand
-- xpNeed (neue Tabelle oder andere Zahlen), rechnet B.XpCum neu (Kennung = Tabelle + gewichtete Summe, 10 Additionen).
local cumOf, cumSig = nil, nil
local function needSig(need)
    if type(need) ~= "table" then return -1 end
    local s = 0
    for i = 1, 10 do s = s + i * (num(need[i]) or 0) end
    return s
end

function B.XpCum(L)
    local need = B.CFG and B.CFG.xpNeed
    local sig = needSig(need)
    if B.XP_CUM == nil or need ~= cumOf or sig ~= cumSig then
        local list = numList(need, NEED_DEF)
        local t = { [0] = 0 }
        local sum = 0
        for i = 1, 10 do
            local n = list[i]
            if n < 1 then n = 1 end
            sum = sum + n
            t[i] = sum
        end
        B.XP_CUM = t
        cumOf, cumSig = need, sig
    end
    if L == nil then return B.XP_CUM end
    local k = num(L) or 0
    k = clamp(math.floor(k), 0, 10)
    return B.XP_CUM[k]
end
B.XpCum()

-- ---------------------------------------------------------------------------
-- Wachsen
-- ---------------------------------------------------------------------------

-- Spieltage vom Zaehmen bis ausgewachsen (Sandbox BanditsNPC.BearGrowDays, B.Opt klemmt 10..365).
function B.GrowDays()
    local d = opt("BearGrowDays", 100)
    if d < 1 then d = 1 end
    return d
end

-- Innere Groesse s zu einem Wachstum g (0..1, geklemmt; nil/Text/NaN -> 0).
function B.GrowSize(g)
    local x = clamp(num(g) or 0, 0, 1)
    local c = curve()
    local p = c[1]
    if x <= p[1] then return p[2] end
    for i = 2, #c do
        local q = c[i]
        if x <= q[1] then
            local span = q[1] - p[1]
            if span <= 0 then return q[2] end
            return p[2] + (q[2] - p[2]) * (x - p[1]) / span
        end
        p = q
    end
    return p[2]
end

-- Umkehrung: Wachstum g, bei dem die innere Groesse s erreicht ist. s ausserhalb der Kurve -> nil.
function B.GrowXAt(s)
    local v = num(s)
    if v == nil then return nil end
    local c = curve()
    local p = c[1]
    if v < p[2] - 0.000000001 then return nil end
    if v <= p[2] then return p[1] end
    for i = 2, #c do
        local q = c[i]
        if v <= q[2] + 0.000000001 then
            local span = q[2] - p[2]
            if span <= 0 then return q[1] end
            return clamp(p[1] + (q[1] - p[1]) * (v - p[2]) / span, p[1], q[1])
        end
        p = q
    end
    return nil
end

local function stageAt()
    return numList(B.CFG and B.CFG.stageAt, STAGE_AT_DEF)
end

-- Stufe zur inneren Groesse: "cub" < 0,75 <= "half" < 1,0 <= "strong" < 1,35 <= "adult" (0,000001 Spiel).
function B.StageOf(s)
    local v = num(s) or 0
    local at = stageAt()
    local key = "cub"
    for i = 1, 3 do
        if v >= at[i] - 0.000001 then key = STAGE_KEYS[i] end
    end
    return key
end

-- Naechste Stufe: Schluessel und Schwelle (innere Groesse), ausgewachsen -> nil, nil.
function B.NextStage(s)
    local v = num(s) or 0
    local at = stageAt()
    for i = 1, 3 do
        if v < at[i] - 0.000001 then return STAGE_KEYS[i], at[i] end
    end
    return nil, nil
end

local function gOf(rec)
    if type(rec) ~= "table" then return 0 end
    return clamp(num(rec.g) or 0, 0, 1)
end

-- Koerper und GEZEIGTE Groesse (PLAN_B1D.md 0.10): in B1d immer das Junges-Modell, sz = min(s, cubMaxSize) auf 3 Nachkommastellen.
-- B.CFG.bodySwap bleibt aus; der spaetere Lauf entscheidet hier (Kevins Frage F11) -- server/BanditsNPCBearGrow.lua B.GrowLive
-- meldet einen eingeschalteten Schalter als Fehler, solange der Tausch nicht gebaut ist.
function B.BodyOf(rec)
    local sz = B.GrowSize(gOf(rec))
    local cap = cfg("cubMaxSize", 0.75)
    if sz > cap then sz = cap end
    return "cub", math.floor(sz * 1000 + 0.5) / 1000
end

-- Wachstumstag (Fuettern zieht ihn vor, Pausen halten ihn an; Frage F12).
function B.GrowDay(rec)
    return math.floor(gOf(rec) * B.GrowDays() + 0.000001)
end

-- ---------------------------------------------------------------------------
-- Faehigkeiten lesen
-- ---------------------------------------------------------------------------

-- Erfahrung 0..XP_CUM[10]; fehlt / Text / NaN / negativ -> 0.
function B.SkillXp(rec, key)
    local f = B.SKILL_FIELD[key]
    if type(rec) ~= "table" or f == nil then return 0 end
    local v = num(rec[f])
    if v == nil or v < 0 then return 0 end
    local top = B.XpCum(10)
    if v > top then return top end
    return v
end

-- Stufe 0..10: groesstes L mit Erfahrung >= XP_CUM[L].
function B.SkillLevel(rec, key)
    local xp = B.SkillXp(rec, key)
    local cum = B.XpCum()
    local L = 0
    for i = 1, 10 do
        if xp >= cum[i] then L = i else break end
    end
    return L
end

-- Stufe, Erfahrung in der Stufe, Bedarf der Stufe (Stufe 10: Bedarf 0).
function B.SkillProgress(rec, key)
    local xp = B.SkillXp(rec, key)
    local cum = B.XpCum()
    local L = B.SkillLevel(rec, key)
    if L >= 10 then return 10, xp - cum[10], 0 end
    return L, xp - cum[L], cum[L + 1] - cum[L]
end

-- ---------------------------------------------------------------------------
-- Alle Werte eines Eintrags (PLAN_B1D.md 0.6, 0.7). Neue Tabelle je Aufruf -- nie je Bild rufen. Werte ungerundet (so steigt jeder
-- auch an Tagen, an denen eine ganze Zahl gleich bliebe); die Sicht rundet (server/BanditsNPCBearGrow.lua B.GrowView).
-- ---------------------------------------------------------------------------
function B.StatsOf(rec)
    local c = B.CFG or {}
    local g = gOf(rec)
    local D = B.GrowDays()
    local s = B.GrowSize(g)
    local body, sz = B.BodyOf(rec)
    local stage = B.StageOf(s)
    local nst, nth = B.NextStage(s)
    local nextDays = nil
    if nst ~= nil then
        local gx = B.GrowXAt(nth)
        if gx ~= nil then
            local d = math.ceil((gx - g) * D - 0.000001)
            if d < 1 then d = 1 end
            nextDays = d
        end
    end
    local lv = {}
    for i = 1, #B.SKILLS do
        local k = B.SKILLS[i]
        lv[k] = B.SkillLevel(rec, k)
    end
    local xs = numList(c.statAt, STAT_AT_DEF)
    local hpMax = lerpList(s, xs, numList(c.hpAt, HP_DEF)) * (1 + cfg("vitPerLv", 0.05) * lv.vit)
    local staMax = lerpList(s, xs, numList(c.staAt, STA_DEF)) * (1 + cfg("conPerLv", 0.05) * lv.con)
    local carry = lerpList(s, xs, numList(c.carryAt, CARRY_DEF))
    local fightBonus = opt("BearFightBonusMax", 70) * lv.fgt / 10
    local dmg = lerpList(s, xs, numList(c.dmgAt, DMG_DEF)) * (1 + fightBonus / 100)
    local dodgeBase = cfg("dodgeBase", 5)
    local dodge = dodgeBase + (opt("BearDodgeMax", 40) - dodgeBase) * lv.agi / 10
    local at = stageAt()
    local fish = 0
    if s >= at[1] - 0.000001 then
        local grown = 1
        if at[3] > at[1] then grown = clamp((s - at[1]) / (at[3] - at[1]), 0, 1) end
        local fb = cfg("fishBase", 10)
        fish = fb + (cfg("fishMax", 60) - fb) * (0.5 * lv.fsh / 10 + 0.5 * grown)
    end
    local nose = cfg("noseBase", 12) + cfg("noseStep", 1.5) * lv.nos
    return {
        g = g, day = math.floor(g * D + 0.000001), s = s, sz = sz, body = body, stage = stage, next = nst, nextDays = nextDays,
        hpMax = hpMax, staMax = staMax, carry = carry, dmg = dmg, dodge = dodge, fightBonus = fightBonus, fish = fish, nose = nose,
        lv = lv,
    }
end

-- Heilung in Prozent des Hoechstwerts je Spielstunde (Kevin 11.11.2026: wach ~1 %, im Schlaf ~15 %). In B1d gibt es keinen Schlaf:
-- der Schreiber ruft immer B.HealRate(false).
function B.HealRate(asleep)
    if asleep == true then return opt("BearHealSleep", 15) end
    return opt("BearHealAwake", 1)
end

-- ---------------------------------------------------------------------------
-- Groesse am Tier setzen (PLAN_B1D.md 0.4). Die EINZIGE Stelle mit setSizeForced und mit getData. Nur bei Abweichung > sizeEps.
-- animal:getData(): Vanilla shared/Definitions/animal/ButcheringUtil.lua:566 (setWeight), :569, :586.
-- animal:getData():getSize(): ButcheringUtil.lua:570; client/ISUI/Animal/ISAnimalUI.lua:31; shared/TimedActions/Animals/ISPetAnimal.lua:28.
-- animal:getData():setSizeForced(Zahl): ButcheringUtil.lua:569 / :571 (createAnimalForHook, gerufen aus onAddedCorpseOnHook :535 --
-- Schreiber shared/TimedActions/Animals/ISPutAnimalOnHook.lua:88, Client client/ISUI/Animal/ISButcherHookUI.lua:520), :586
-- (onRemoveCorpseFromHook -- Server :674 im isServer-Zweig, shared/TimedActions/Animals/ISRemoveAnimalFromHook.lua:70, Client
-- ISButcherHookUI.lua:530), :242 (an einem frisch gebauten IsoAnimal). Grenzfall ehrlich: Vanilla setzt es nur an Haken-Tieren und
-- dort entstehenden Tieren; an einem lebenden Tier in der Welt nur NCBearTest client/NCBearSize.lua:27 und Kevins Anleitung
-- baer/spiel/anleitung_lebend.md:6 (b:getData():setSizeForced(1.2) am lebenden Erwachsenen). Kevins 1,35
-- (baer/begleiter/ENTSCHEIDUNGEN.md:10) war die Antwort auf die Groessen-Frage "nach dem Test" mit jenem Groessen-Befehl der Test-Mod
-- (baer/begleiter/PLAN.md:297) -- gespielt also sehr wahrscheinlich, belegt nicht; Regel-Frage an Kevin (Nachbesserung B1d A3).
-- Kein setSize (klemmt), kein pcall. Rueckgabe: true, wenn geschrieben wurde.
-- ---------------------------------------------------------------------------
function B.ApplySize(a, sz)
    if a == nil or type(sz) ~= "number" or sz ~= sz or sz <= 0 then return false end
    local d = a:getData()
    if d == nil then return false end
    if math.abs(d:getSize() - sz) <= cfg("sizeEps", 0.002) then return false end
    d:setSizeForced(sz)
    return true
end
