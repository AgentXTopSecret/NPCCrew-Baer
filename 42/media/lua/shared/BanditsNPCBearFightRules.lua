--
-- NPC Crew -- Baer, Kampf-Regeln als reine Formeln (F2 = B5a, PLAN_F2.md 0.7, 0.8, 2.1-2.5, 4.3).
--
-- Rein: keine Engine, nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (Kampf, Gegner, Verband) und beim Client
-- (Anzeige). Gelesen werden nur B.CFG (Stellwerte, shared/BanditsNPCBear.lua), B.Opt (Sandbox) und AnimalDefinitions.animals
-- (Lua-Tabelle unserer Arten, shared/BanditsNPCBearDefs.lua) zur Laufzeit.
--
-- B.CLIPS ist die EINE Tabelle der Clip-Zeiten (Kevins Wunsch, PLAN_F2.md 0.7): Sitz-Treiber, Aufstehen (B.StandMs) und Kampf-Uhr
-- lesen NUR daraus (B.ClipMs). Bezug: das GLB des grossen Koerpers (forschung_f2_bestand.md 2.3, Dauer aus dem glTF-Kopf, gleich den
-- Knoten-XML unter AnimSets/buck/idle). Nach dem Lauf baer-gross (neues Aufrichten/Bruellen) bzw. baer-junges-fuss (eigene Sitz-Clips des
-- Jungen: Feld cubDur) wird nur diese Tabelle nachgezogen. zbite / smack sind die Zombie- bzw. Banditen-Bilder (Treffer nach der Uhr beim
-- Schreiber; das Bild spielt der Zombie-Rechner).
--
-- Stufen (Kevin ENT:194-207, PLAN_F2.md 0.8): Junges (innere Groesse < 0,75) kaempft nie; Halbstark nur Prankenhieb gegen EIN Ziel, wirft
-- nicht um; ab 1,0 Biss, Zerfleischen am Boden, 1 Nebenziel, Umwerfen 30 % -> linear 100 % bei 1,35; ab 1,35 Doppelschlag, Aufrichten,
-- 3 Nebenziele.
-- NACHTRAG Kevin 12.11. (PLAN_F2.md 11): B.MeleeDamage (11.2, Schaden je Treffer fuer Fenster UND Kampf), B.SkillCapLv (11.4, Alters-Deckel
-- der Faehigkeiten), B.FleeHp (11.7, Fliehen "noch N Treffer vom Tod" statt Prozent).
-- Ladefolge: nach ...Bear / ...Crew / ...Defs (alphabetisch, ...FightRules < ...Foe < ...Food); nichts Fremdes auf Dateiebene.
-- Statisch geprueft, nicht gespielt.
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

local function opt(name, def)
    local f = B.Opt
    local v = f and num(f(name)) or nil
    if v == nil then return def end
    return v
end

-- ---------------------------------------------------------------------------
-- Clip-Tabelle (PLAN_F2.md 4.3). dur = Sekunden, hitPc = Treffer-Anteil der Dauer, loop = Schleife, cubDur (wahlfrei) = Dauer am Junges-GLB.
-- ---------------------------------------------------------------------------
B.CLIPS = B.CLIPS or {
    rear = { dur = 3.00 },
    swipeL = { dur = 1.50, hitPc = 0.40 },
    swipeR = { dur = 1.50, hitPc = 0.40 },
    slam = { dur = 2.40, hitPc = 0.54 },
    bite = { dur = 1.30, hitPc = 0.40 },
    maul = { dur = 1.60, hitPc = 0.34 },
    sitdown = { dur = 1.60 },
    sit = { dur = 4.00, loop = true },
    standup = { dur = 1.30 },
    eat = { dur = 3.20, loop = true },
    zbite = { dur = 1.60, hitPc = 0.30 },
    smack = { dur = 1.10, hitPc = 0.45 },
}

-- Angriffe des Baeren (nur diese waehlt B.FightChoose bzw. nimmt B.FightForce an).
B.ATTACKS = B.ATTACKS or { rear = true, swipeL = true, swipeR = true, slam = true, bite = true, maul = true }

-- Dauer eines Clips in ms plus Zuschlag padS (Sekunden, nil = 0). bd ~= "big" nimmt cubDur, wenn gesetzt. Unbekannt -> nil.
function B.ClipMs(key, padS, bd)
    local list = B.CLIPS
    local c = type(list) == "table" and list[key] or nil
    if type(c) ~= "table" then return nil end
    local dur = num(c.dur)
    if bd ~= "big" and num(c.cubDur) ~= nil then dur = num(c.cubDur) end
    if dur == nil then return nil end
    return math.floor((dur + (num(padS) or 0)) * 1000 + 0.5)
end

-- Treffer-Zeitpunkt eines Clips in ms nach dem Start (nil = der Clip trifft nicht).
function B.ClipHitMs(key, bd)
    local list = B.CLIPS
    local c = type(list) == "table" and list[key] or nil
    local pc = type(c) == "table" and num(c.hitPc) or nil
    local dur = B.ClipMs(key, 0, bd)
    if pc == nil or dur == nil then return nil end
    return math.floor(dur * pc + 0.5)
end

-- Aufstehen: Clip "standup" + Frist standPadMs (= 1300 + 1000 = 2300; ersetzt B.CFG.standMs, PLAN_F2.md 0.7).
function B.StandMs()
    return (B.ClipMs("standup", 0) or 1300) + cfg("standPadMs", 1000)
end

-- ---------------------------------------------------------------------------
-- Stufen-Freischaltung (0.8). st = B.StatsOf(rec) (st.s = innere Groesse). Rueckgabe { swipe, bite, maul, slam, rear, side, knockPct, stage }.
-- ---------------------------------------------------------------------------
local STAGE_AT_DEF = { 0.75, 1.0, 1.35 }

local function stageAt()
    local t = B.CFG and B.CFG.stageAt
    if type(t) ~= "table" or #t ~= 3 then return STAGE_AT_DEF end
    for i = 1, 3 do
        if num(t[i]) == nil then return STAGE_AT_DEF end
    end
    return t
end

function B.FightStageOf(st)
    local s = 0
    if type(st) == "table" then s = num(st.s) or 0 end
    local at = stageAt()
    local eps = 0.000001
    local r = { swipe = false, bite = false, maul = false, slam = false, rear = false, side = 0, knockPct = 0, stage = "cub" }
    if s < at[1] - eps then return r end
    r.swipe = true
    r.stage = "half"
    if s < at[2] - eps then return r end
    r.bite, r.maul = true, true
    r.side = 1
    r.stage = "strong"
    local kmin = cfg("knockMinPct", 30)
    if s < at[3] - eps then
        local span = at[3] - at[2]
        local f = 0
        if span > 0 then f = clamp((s - at[2]) / span, 0, 1) end
        r.knockPct = kmin + (100 - kmin) * f
        return r
    end
    r.slam, r.rear = true, true
    r.side = math.floor(cfg("sideMax", 3))
    r.knockPct = 100
    r.stage = "adult"
    return r
end

-- ---------------------------------------------------------------------------
-- Weiten, Kegel, Schaden des Baeren (2.2.4)
-- ---------------------------------------------------------------------------
local REACH_KEY = { swipeL = "swipeReach", swipeR = "swipeReach", bite = "biteReach", maul = "maulReach", slam = "slamReach" }
local HALF_KEY = { swipeL = "swipeHalf", swipeR = "swipeHalf", bite = "biteHalf", maul = "maulHalf", slam = "slamHalf" }
local REACH_DEF = { swipeReach = 1.4, biteReach = 1.4, maulReach = 1.1, slamReach = 1.5 }
local HALF_DEF = { swipeHalf = 55, biteHalf = 30, maulHalf = 30, slamHalf = 80 }

-- Weite eines Angriffs in Kacheln bei gezeigter Groesse sz (rear / unbekannt: 0).
function B.FightReach(act, sz)
    local k = REACH_KEY[act]
    if k == nil then return 0 end
    return cfg(k, REACH_DEF[k]) * (num(sz) or 1)
end

-- Halber Kegel in Grad um die Linie Baer -> Hauptziel (rear / unbekannt: 0).
function B.FightHalf(act)
    local k = HALF_KEY[act]
    if k == nil then return 0 end
    return cfg(k, HALF_DEF[k])
end

-- Schaden am Zombie (Zombie-Leben): Grundwert x st.dmg x BearDamagePercent / 100. main = Hauptziel (sonst Nebenziel).
function B.FightDamage(act, main, st)
    local base = 0
    if act == "swipeL" or act == "swipeR" then
        if main then base = cfg("dmgMain", 1.0) else base = cfg("dmgSide", 0.6) end
    elseif act == "slam" then
        if main then base = cfg("dmgSlam", 0.9) else base = cfg("dmgSide", 0.6) end
    elseif act == "bite" then
        base = cfg("dmgBite", 1.2)
    elseif act == "maul" then
        base = cfg("dmgMaul", 1.8)
    end
    local dmg = 0
    if type(st) == "table" then dmg = num(st.dmg) or 0 end
    return base * dmg * opt("BearDamagePercent", 100) / 100
end

-- Wie ein Treffer umwirft (Rueckstoss, forschung_f2_bestand.md 2.5): "back" (taumelt zurueck), "down" (faellt auf der Stelle) oder nil.
function B.FightKnockMode(act)
    if act == "swipeL" or act == "swipeR" or act == "slam" then return "back" end
    if act == "bite" then return "down" end
    return nil
end

-- Angriff waehlen (2.2.4). c = { allow (B.FightStageOf), last, prone, d, sz, slamReady, slamN, rearReady, first, rnd, rnd2 }; rnd 0..99 vom
-- Aufrufer (Aufrichten), rnd2 0..99 (wahlfrei, Zusatz schnittstelle_aenderungen.md "F2 KERN": Gewichts-Wurf; fehlt er, gilt rnd).
-- Aufrichten nur als erster Angriff (first), frei (rearReady), Ziel weiter als rearDist und rnd < rearChance. Sonst gewichteter Zufall
-- aus den Angriffen in Weite: nie last; liegt das Ziel (prone), Zerfleischen statt Biss. Alle Gewichte 0: Hiebe im Wechsel. Rueckgabe: Name / nil.
function B.FightChoose(c)
    if type(c) ~= "table" then return nil end
    local allow = c.allow
    if type(allow) ~= "table" then return nil end
    local d = num(c.d) or 999
    local sz = num(c.sz) or 1
    local rnd = num(c.rnd) or 0
    if allow.rear and c.first == true and c.rearReady == true and d > cfg("rearDist", 2.5) and rnd < cfg("rearChance", 50)
        and c.last ~= "rear" then
        return "rear"
    end
    local list = {}
    local sum = 0
    local function add(name, w)
        w = math.floor((num(w) or 0) + 0.5)
        if name ~= c.last and w > 0 then
            list[#list + 1] = { name, w }
            sum = sum + w
        end
    end
    if allow.maul and c.prone == true and d <= B.FightReach("maul", sz) then add("maul", cfg("wMaul", 70)) end
    if allow.bite and c.prone ~= true and d <= B.FightReach("bite", sz) then add("bite", cfg("wBite", 30)) end
    local swipeIn = allow.swipe and d <= B.FightReach("swipeL", sz)
    if swipeIn then
        add("swipeL", cfg("wSwipe", 25))
        add("swipeR", cfg("wSwipe", 25))
    end
    if allow.slam and c.slamReady == true and (num(c.slamN) or 0) >= 1 and d <= B.FightReach("slam", sz) then
        add("slam", cfg("wSlam", 40))
    end
    if sum <= 0 then
        if not swipeIn then return nil end
        if c.last == "swipeL" then return "swipeR" end
        return "swipeL"
    end
    local r2 = num(c.rnd2)
    if r2 == nil then r2 = rnd end
    local r = math.floor(clamp(r2, 0, 99) * sum / 100)
    for i = 1, #list do
        if r < list[i][2] then return list[i][1] end
        r = r - list[i][2]
    end
    return list[#list][1]
end

-- ---------------------------------------------------------------------------
-- Gegner (2.1.3-2.1.5)
-- ---------------------------------------------------------------------------
local COLL_DEF = { cub = 0.24, big = 0.30 }

-- Reichweite eines Gegners zum Baeren in Kacheln: Zombie 0,3 + w + foeReachPad, Bandit foeBanditReach + w; w = collisionSize der Art des
-- Koerpers x gezeigte Groesse (FG 1.2: Zombie-Breite 0,3 + Tier-Breite = Stand-Abstand). collisionSize aus unserer eigenen Definition
-- (Lua-Tabelle AnimalDefinitions.animals, shared/BanditsNPCBearDefs.lua:90, :181), Rueckfall 0,24 / 0,30.
function B.FoeReach(kind, bd, sz)
    if bd ~= "big" then bd = "cub" end
    local coll = nil
    local defs = AnimalDefinitions and AnimalDefinitions.animals
    local types = B.BODY_TYPE
    local def = type(defs) == "table" and type(types) == "table" and defs[types[bd]] or nil
    if type(def) == "table" then coll = num(def.collisionSize) end
    if coll == nil then coll = COLL_DEF[bd] end
    local w = coll * (num(sz) or 1)
    if kind == "b" then return cfg("foeBanditReach", 1.2) + w end
    return 0.3 + w + cfg("foeReachPad", 0.35)
end

-- Lebenspunkte eines Gegner-Treffers: Sandbox BearZombieDamage / BearBanditDamage x (0,8 + 0,4 x r01); r01 0..1 vom Aufrufer.
function B.FoePts(kind, r01)
    local base
    if kind == "b" then base = opt("BearBanditDamage", 12) else base = opt("BearZombieDamage", 6) end
    return base * (0.8 + 0.4 * clamp(num(r01) or 0.5, 0, 1))
end

-- Darf dieser Gegner den Baeren angreifen / vom Baeren angegriffen werden? (Reihenfolge wie die gespielte Regel T:shared/NCBearFight.lua:271-293;
-- NPC-Crew-Marken VOR hostile, FG 3.2.) f = { alive, fakeDead, killDone, inCar, grapple, bandit, tcUid, recruited, npcNeutral, npcUid,
-- fallback, program, loyal, stance, downed, hostile, hostileP } -- nur Werte (der Aufrufer liest sie aus Engine und Gehirn). Ein
-- gewoehnlicher Zombie (bandit falsch) ist Gegner; ein Bandit nur bei hostile oder hostileP (Bandits B:shared/Bandit.lua:607-612
-- Bandit.IsHostile). Im Zweifel false.
function B.FoeIsTarget(f)
    if type(f) ~= "table" then return false end
    if f.alive ~= true then return false end
    if f.fakeDead == true or f.killDone == true or f.inCar == true or f.grapple == true then return false end
    if f.tcUid ~= nil then return false end
    if f.bandit ~= true then return true end
    if f.recruited or f.npcNeutral or f.npcUid ~= nil then return false end
    if f.fallback == "NPCNeutral" then return false end
    if type(f.program) == "string" and string.sub(f.program, 1, 3) == "NPC" then return false end
    if f.loyal then return false end
    if f.stance == "passive" then return false end
    if f.downed then return false end
    if f.hostile or f.hostileP then return true end
    return false
end

-- ---------------------------------------------------------------------------
-- Fliehen kurz vor dem Tod (PLAN_F2.md 11.7, Kevin 12.11. ~07:30 "nach 2-3 hits sterben wuerde"; ERSETZT BearFleeHealth 20 %).
-- kinds = { z = true / b = true } (Gegner, die ihn gerade angreifen bzw. in Reichweite sind; nil/leer = unbekannt). Groesster erwarteter
-- Einzeltreffer = Sandbox-Schaden x 1,2 (die obere Grenze von B.FoePts, Ausweichen NICHT abgezogen); ohne bekannten Gegner der
-- Banditen-Hieb (sichere Seite). Rueckgabe: Schwelle in Lebenspunkten (BearFleeHits x Treffer; 0 = flieht nie), Hysterese (1 Treffer).
-- ---------------------------------------------------------------------------
function B.FleeHp(kinds)
    local n = math.floor(opt("BearFleeHits", 3))
    if n <= 0 then return 0, 0 end
    local hz = opt("BearZombieDamage", 6) * 1.2
    local hb = opt("BearBanditDamage", 12) * 1.2
    local hit = nil
    if type(kinds) == "table" then
        if kinds.b == true then hit = hb end
        if kinds.z == true and (hit == nil or hz > hit) then hit = hz end
    end
    if hit == nil then hit = hb end
    return n * hit, hit
end

-- ---------------------------------------------------------------------------
-- Schaden JE TREFFER, den der Baer JETZT machen wuerde (PLAN_F2.md 11.2): dieselbe Rechnung wie der Kampf (B.FightDamage mit B.StatsOf) --
-- der Kampf (server/BanditsNPCBearFight.lua) holt seine Zahlen genau hier, Anzeige und Kampf laufen so nie auseinander. st wahlfrei
-- (sonst B.StatsOf(rec)). Junges (kaempft nie) -> nil. Rueckgabe { swipe, swipeSide, bite, maul, slam, slamSide (nur freigeschaltete),
-- size (Anteil aus der Groesse), fgt (Kaempfen-Bonus in Prozent), pct (BearDamagePercent) } -- Einheit Zombie-Leben (wie Fx "hit" dmg).
-- ---------------------------------------------------------------------------
function B.MeleeDamage(rec, st)
    if type(st) ~= "table" then
        local f = B.StatsOf
        if f == nil or type(rec) ~= "table" then return nil end
        st = f(rec)
    end
    if type(st) ~= "table" then return nil end
    local allow = B.FightStageOf(st)
    if not allow.swipe then return nil end
    local fgt = num(st.fightBonus) or 0
    local r = {
        swipe = B.FightDamage("swipeL", true, st), swipeSide = B.FightDamage("swipeL", false, st),
        size = (num(st.dmg) or 0) / (1 + fgt / 100), fgt = fgt, pct = opt("BearDamagePercent", 100),
    }
    if allow.bite then
        r.bite = B.FightDamage("bite", true, st)
        r.maul = B.FightDamage("maul", true, st)
    end
    if allow.slam then
        r.slam = B.FightDamage("slam", true, st)
        r.slamSide = B.FightDamage("slam", false, st)
    end
    return r
end

-- ---------------------------------------------------------------------------
-- Lerntempo: Alters-Deckel der Faehigkeiten (PLAN_F2.md 11.4, Kevin 12.11. ~05:10 "nicht schon alles auf max level ... bevor er
-- ueberhaupt voll ausgewachsen ist"). Hoechste Stufe, die der Eintrag in seiner Wachstums-Stufe lernen kann: B.CFG.skillCapAt
-- { Junges, halbstark, kraeftig, ausgewachsen } = { 3, 6, 8, 10 }; Sandbox BearSkillAgeCap aus -> 10. Stufe aus B.StageOf(B.GrowSize(g))
-- (shared/BanditsNPCBearStats.lua, zur Laufzeit; dieselbe Stufe wie die Alter-Zeile). Schreiber (B.SkillAdd) und Fenster lesen hier.
-- ---------------------------------------------------------------------------
local CAP_DEF = { 3, 6, 8, 10 }
local CAP_IDX = { cub = 1, half = 2, strong = 3, adult = 4 }

function B.SkillCapLv(rec)
    local f = B.Opt
    if f == nil or f("BearSkillAgeCap") ~= true then return 10 end
    if B.StageOf == nil or B.GrowSize == nil then return 10 end
    local g = 0
    if type(rec) == "table" then g = num(rec.g) or 0 end
    local idx = CAP_IDX[B.StageOf(B.GrowSize(g))] or 4
    local t = B.CFG and B.CFG.skillCapAt
    local v = nil
    if type(t) == "table" then v = num(t[idx]) end
    if v == nil then v = CAP_DEF[idx] end
    return clamp(math.floor(v), 0, 10)
end

-- ---------------------------------------------------------------------------
-- Kampf-Entscheid je Hirn-Takt (2.2.1, R1-R10). c = { st, body, s, passive, down, ride, hpPts, fleeHp, fleeHys, fleeOn, sta, resting,
-- restOver, longOver, foe, ownerCarNear, follow, capFull }. R6 (PLAN_F2.md 11.7): hpPts = Leben in Punkten, fleeHp / fleeHys aus B.FleeHp
-- (0 = flieht nie), fleeOn = zieht sich schon wegen Leben zurueck (dann erst ab fleeHp + fleeHys wieder kampfbereit). sta Anteil 0..1.
-- Rueckgabe { act = "none" / "fight" / "retreat" / "rest", why }.
-- ---------------------------------------------------------------------------
function B.FightDecide(c)
    if type(c) ~= "table" then return { act = "none", why = "args" } end
    if c.st ~= "tame" or c.ride == true or c.down == true then return { act = "none", why = "state" } end
    if c.body ~= "big" or (num(c.s) or 0) < (stageAt()[1] - 0.000001) then return { act = "none", why = "cub" } end
    if c.foe ~= true then return { act = "none", why = "nofoe" } end
    if c.follow == true and c.ownerCarNear == true then return { act = "none", why = "car" } end
    if c.passive == true then return { act = "retreat", why = "passive" } end
    local flee = num(c.fleeHp) or 0
    if flee > 0 then
        local edge = flee
        if c.fleeOn == true then edge = flee + (num(c.fleeHys) or 0) end
        if (num(c.hpPts) or 0) < edge then return { act = "retreat", why = "hurt" } end
    end
    local sta = num(c.sta) or 1
    if sta <= cfg("staRestBelow", 0.05) then return { act = "rest", why = "breath" } end
    if c.resting == true and sta < cfg("staResume", 0.30) and c.restOver ~= true then return { act = "rest", why = "breath" } end
    if c.longOver == true then return { act = "rest", why = "long" } end
    if c.capFull == true then return { act = "retreat", why = "cap" } end
    return { act = "fight", why = nil }
end

-- Ausweichen (2.3): roll 0..99 vom Aufrufer, pct = B.StatsOf(rec).dodge.
function B.DodgeHit(pct, roll)
    return (num(roll) or 100) < (num(pct) or 0)
end

-- Verband-Staerke -> Faktor der Heilung (2.5 Nr. 2): power / 4, geklemmt 0,25 .. 1,5 (Bandage 4,0 -> 1; Stoffstreifen 2,0 -> 0,5).
function B.MendPower(power)
    return clamp((num(power) or 0) / 4, 0.25, 1.5)
end
