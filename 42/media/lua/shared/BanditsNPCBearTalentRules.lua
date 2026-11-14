--
-- NPC Crew -- Baer, Talente als reine Regeln (Lauf baer-talente, baer/plaene/PLAN_TALENTE.md 2-3; Kevins Antworten 14.11.2026 ~10:20,
-- baer/begleiter/ENTSCHEIDUNGEN.md -- sie gehen vor dem Plan).
--
-- Kevin 14.11.2026: "am ende genau 3 punkte zum verteilen" -- Punkt 1 bei 10 % Wachstum, Punkt 2 bei halbstark, Punkt 3 bei ausgewachsen;
-- "das aktivieren ... sperrt es einen neuen skill zu lernen selbst wenn man durch bugs mehr haette"; ~10:20 "Freie Wahl" (irgendwelche 3 von 9,
-- KEINE Reihen), Reset "Alle auf einmal", Dickes Fell "Prozent bleibt".
--
-- Eine Wahrheit: die VERDIENTEN Punkte werden nie gespeichert, sondern aus dem Wachstum rec.g gerechnet (drei Schwellen -> hoechstens 3).
-- Gespeichert wird nur, WAS gelernt ist: rec.tal = Text "alert,paw" (Lern-Reihenfolge, hoechstens talMax 3) -- im Register und im Spiegel.
-- Kein Aussehen-Wechsel, Unstuck, Koerper-Tausch, Absturz oder eine Bitte mit falschen Werten erzeugt einen 4. Punkt; ab 3 gelernten ist
-- immer Schluss (B.TalentCan prueft "max" ZUERST).
--
-- Rein: keine Engine, nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (Register-Eintrag: g, tal, talR) und beim
-- Client (Sicht-Eintrag: tal, talE) -- graue Kacheln und Server-Ablehnung laufen so nie auseinander. Gelesen werden nur B.CFG (Block
-- "Talente", shared/BanditsNPCBear.lua), B.GrowSize / B.StageOf / B.GrowXAt / B.GrowDays (shared/BanditsNPCBearStats.lua) und B.Err zur
-- Laufzeit. Jede Wirkung der 9 Talente sitzt an GENAU einer Stelle des uebrigen Codes und fragt dort B.TalentK (mit Existenz-Riegel).
--
-- Ladefolge: shared/ alphabetisch nach ...Stats / ...TagPose; nichts Fremdes auf Dateiebene. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------
local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

-- Vorgaben, falls B.CFG fehlt (gleiche Zahlen wie der Block "Talente" in shared/BanditsNPCBear.lua).
local DEF = {
    talG1 = 0.10, talMax = 3,
    talFrugalK = 16 / 24, talFurHp = 250, talStaPct = 0.30, talStaRegK = 1.5, talPawKnock = 100, talPawPush = 2.0, talMuleKg = 50,
    talAlertK = 1.5, talHealK = 2.0, talDownK = 0.5, talCritPct = 25, talCritK = 2.0, talFishK = 2,
    downedHours = 12,
}

local function cfg(key)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return DEF[key] end
    return v
end

-- Hoechstzahl gelernter Talente (talMax, ganze Zahl 0..3). Kevin 14.11.2026: "genau 3 punkte", "niemals mehr" -- darum ist 3 ein harter Deckel,
-- auch ein hoeher gestellter Stellwert bringt keinen 4. Punkt und kein 4. Talent.
local function maxN()
    local m = math.floor(cfg("talMax") or 3)
    if m < 0 then m = 0 end
    if m > 3 then m = 3 end
    return m
end

-- ---------------------------------------------------------------------------
-- Die 9 Talente (Kevin 14.11.2026 ~02:50 / ~05:05). Reihenfolge = Fenster (Kevins Nummern 1-9, Angler ans Ende, solange er "kommt spaeter").
-- Schluessel ENDGUELTIG (stehen im Spielstand); Name = Text-Kern fuer UI_BN_Bear_Talent_<Name> / _<Name>_Short / _<Name>_Tip.
-- ---------------------------------------------------------------------------
B.TALENTS = { "frugal", "fur", "stamina", "paw", "mule", "alert", "tough", "crit", "fisher" }
B.TALENT_IX = {}
local NAME = {
    frugal = "Frugal", fur = "Fur", stamina = "Stamina", paw = "Paw", mule = "Mule", alert = "Alert", tough = "Tough", crit = "Crit",
    fisher = "Fisher",
}
for i = 1, #B.TALENTS do B.TALENT_IX[B.TALENTS[i]] = i end

function B.TalentName(k)
    if type(k) ~= "string" then return nil end
    return NAME[k]
end

-- ---------------------------------------------------------------------------
-- Gelernt (rec.tal / Sicht tal): Text, Schluessel durch Komma. Zeichenweise zerlegt, ohne Muster (Kahlua ist kein echtes Lua 5.1, wie fill in
-- shared/BanditsNPCBear.lua). Hoechstens 200 Zeichen werden gelesen (Deckel gegen einen veraenderten Spiegel).
-- Rueckgabe: Liste (nur bekannte, keine Doppelten, hoechstens talMax, in Lern-Reihenfolge) und die Zahl verworfener Teile.
-- ---------------------------------------------------------------------------
local function parse(text)
    local out, seen, bad = {}, {}, 0
    if text == nil then return out, 0 end
    if type(text) ~= "string" then return out, 1 end
    local n = string.len(text)
    if n > 200 then
        n = 200
        bad = bad + 1
    end
    local m = maxN()
    local start = 1
    for i = 1, n + 1 do
        local ch = ""
        if i <= n then ch = string.sub(text, i, i) end
        if i > n or ch == "," then
            local part = string.sub(text, start, i - 1)
            start = i + 1
            if part ~= "" then
                if B.TALENT_IX[part] == nil or seen[part] then
                    bad = bad + 1
                elseif #out >= m then
                    bad = bad + 1
                else
                    seen[part] = true
                    out[#out + 1] = part
                end
            end
        end
    end
    return out, bad
end

-- Liste -> Text ("" -> nil).
local function join(list)
    if type(list) ~= "table" or #list == 0 then return nil end
    return table.concat(list, ",")
end

function B.TalentList(e)
    if type(e) ~= "table" then return {} end
    local list, _ = parse(e.tal)
    return list
end

function B.TalentN(e)
    return #B.TalentList(e)
end

function B.TalentOn(e, k)
    if type(e) ~= "table" or type(k) ~= "string" or B.TALENT_IX[k] == nil then return false end
    local list = B.TalentList(e)
    for i = 1, #list do
        if list[i] == k then return true end
    end
    return false
end

-- Wert eines Talents: Zahl B.CFG[key] (Rueckfall DEF), wenn k gelernt -- sonst off. Die EINE Frage jeder Wirkungs-Stelle.
function B.TalentK(e, k, key, off)
    if not B.TalentOn(e, k) then return off end
    local v = cfg(key)
    if v == nil then return off end
    return v
end

-- ---------------------------------------------------------------------------
-- Verdiente Punkte 0..talMax (nie gespeichert). Sicht-Eintrag: Feld talE (der Schreiber rechnet). Register-Eintrag: drei Schwellen aus g --
-- g >= talG1 (Kevin "10 % Wachstum"; 100 Tage -> Tag 10), Stufe >= halbstark (B.StageOf, innere Groesse >= stageAt[1]), Stufe ausgewachsen.
-- Ohne shared/BanditsNPCBearStats.lua nur die erste Schwelle.
-- ---------------------------------------------------------------------------
local RANK = { cub = 0, half = 1, strong = 2, adult = 3 }

function B.TalentEarned(e)
    if type(e) ~= "table" then return 0 end
    local m = maxN()
    local te = num(e.talE)
    if te ~= nil then
        te = math.floor(te)
        if te < 0 then te = 0 end
        if te > m then te = m end
        return te
    end
    local g = num(e.g) or 0
    if g < 0 then g = 0 end
    if g > 1 then g = 1 end
    local n = 0
    if g >= (cfg("talG1") or 0.10) - 0.000001 then n = n + 1 end
    if B.GrowSize ~= nil and B.StageOf ~= nil then
        local r = RANK[B.StageOf(B.GrowSize(g))] or 0
        if r >= 1 then n = n + 1 end
        if r >= 3 then n = n + 1 end
    end
    if n > m then n = m end
    return n
end

function B.TalentFree(e)
    local have = B.TalentN(e)
    if have >= maxN() then return 0 end
    local f = B.TalentEarned(e) - have
    if f < 0 then f = 0 end
    return f
end

-- ---------------------------------------------------------------------------
-- Darf er k lernen? ok, why. Reihenfolge: unknown -> max (ZUERST nach unknown: Kevin "selbst wenn man durch bugs mehr haette") -> have ->
-- soon (Angler bis F5: B.CFG.talFishOn ~= true) -> point (kein freier Punkt). Freie Wahl (Kevin ~10:20): keine Reihen.
-- ---------------------------------------------------------------------------
function B.TalentCan(e, k)
    if type(k) ~= "string" or B.TALENT_IX[k] == nil then return false, "unknown" end
    local list = B.TalentList(e)
    if #list >= maxN() then return false, "max" end
    for i = 1, #list do
        if list[i] == k then return false, "have" end
    end
    if k == "fisher" and not (B.CFG and B.CFG.talFishOn == true) then return false, "soon" end
    if #list >= B.TalentEarned(e) then return false, "point" end
    return true, nil
end

-- ---------------------------------------------------------------------------
-- Bereinigen (rein; beim Laden ueber B.GrowFix, vor jedem Schreiben, nach dem Spiegel). rec.tal: nur bekannte, keine Doppelten, hoechstens
-- talMax (die ERSTEN bleiben -- R3), leer -> nil. rec.talR: ganzer Spieltag >= 0 oder nil. rec.talN: ganze Zahl 0..talMax oder nil.
-- Verworfenes -> EINE Fehlerzeile je Aufruf (B.Err). Rueckgabe: Zahl verworfener Teile.
-- ---------------------------------------------------------------------------
function B.TalentFix(rec)
    if type(rec) ~= "table" then return 0 end
    local list, bad = parse(rec.tal)
    local text = join(list)
    rec.tal = text
    local r = num(rec.talR)
    if r ~= nil then
        r = math.floor(r)
        if r < 0 then r = nil end
    end
    if rec.talR ~= nil and r == nil then bad = bad + 1 end
    rec.talR = r
    local n = num(rec.talN)
    if n ~= nil then
        n = math.floor(n)
        if n < 0 then n = 0 end
        if n > maxN() then n = maxN() end
    end
    rec.talN = n
    if bad > 0 and B.Err then
        B.Err("talent: entry " .. tostring(rec.id) .. " had " .. tostring(bad) .. " unusable perk value(s), kept " .. tostring(text or "none"))
    end
    return bad
end

-- Auf die verdienten Punkte kuerzen (Spiegel: Wiederherstellen / neuerer Spiegel -- R2: ein veraenderter Spiegel bringt hoechstens so viele
-- Talente, wie das ehrliche Wachstum erlaubt). Die ersten bleiben. Rueckgabe: Zahl gestrichener Talente.
function B.TalentCut(rec)
    if type(rec) ~= "table" then return 0 end
    local list = B.TalentList(rec)
    local keep = B.TalentEarned(rec)
    if #list <= keep then return 0 end
    local out = {}
    for i = 1, keep do out[i] = list[i] end
    rec.tal = join(out)
    return #list - keep
end

-- ---------------------------------------------------------------------------
-- Reset (Kevin ~10:20 "Alle auf einmal"; Sandbox BearTalentReset / BearTalentResetDays, die Werte gibt der Aufrufer). Stunden bis ein Reset
-- wieder geht: 0 = jetzt. Spieltag = floor(Weltstunden / 24) (wie server/BanditsNPCBearNeeds.lua dayRoll); der naechste geht ab Beginn von
-- Spieltag talR + days. days 0 = jederzeit. Ein talR in der Zukunft (fremder Spiegel) gilt als heute.
-- ---------------------------------------------------------------------------
function B.TalentResetLeft(e, nowH, days)
    if type(e) ~= "table" then return 0 end
    local d = math.floor(num(days) or 1)
    if d <= 0 then return 0 end
    local r = num(e.talR)
    if r == nil then return 0 end
    local now = num(nowH) or 0
    local today = math.floor(now / 24)
    r = math.floor(r)
    if r > today then r = today end
    local left = (r + d) * 24 - now
    if left < 0 then left = 0 end
    return left
end

-- ---------------------------------------------------------------------------
-- Zaeh (Kevin "steht vom Boden schneller auf", ~10:20 "So wie besprochen": 6 statt 12 h): Stunden am Boden bis allein aufstehen.
-- Die EINE Funktion fuer server/BanditsNPCBearHurt.lua B.DownSlow UND B.DownView.
-- ---------------------------------------------------------------------------
function B.DownHours(rec)
    local h = cfg("downedHours") or 12
    return h * B.TalentK(rec, "tough", "talDownK", 1)
end

-- Kritischer Treffer (Kevin 14.11. ~05:05: "+25% krit chance fuegt doppelten schaden aus"): Faktor zu einem Wurf roll 0..99 (der Aufrufer
-- wuerfelt beim Schreiber mit ZombRand). Nicht gelernt -> 1.
function B.TalentCrit(rec, roll)
    if not B.TalentOn(rec, "crit") then return 1 end
    local r = num(roll)
    if r == nil then return 1 end
    if r < (cfg("talCritPct") or 25) then return cfg("talCritK") or 2 end
    return 1
end

-- ---------------------------------------------------------------------------
-- Spieltage bis zum naechsten Punkt (nur Register-Eintrag; die Sicht traegt das Ergebnis als talNx). nil bei talMax verdienten.
-- Schwellen in g: talG1, B.GrowXAt(stageAt[1]), B.GrowXAt(stageAt[3]); Tage = ceil((gx - g) x BearGrowDays), mindestens 1 (wie nextDays in
-- shared/BanditsNPCBearStats.lua B.StatsOf).
-- ---------------------------------------------------------------------------
function B.TalentNextDays(rec)
    if type(rec) ~= "table" or B.GrowXAt == nil or B.GrowDays == nil then return nil end
    local n = B.TalentEarned(rec)
    if n >= maxN() then return nil end
    local g = num(rec.g) or 0
    local at = B.CFG and B.CFG.stageAt
    local s1 = type(at) == "table" and num(at[1]) or 0.75
    local s3 = type(at) == "table" and num(at[3]) or 1.35
    local marks = { cfg("talG1") or 0.10, B.GrowXAt(s1), B.GrowXAt(s3) }
    local best = nil
    for i = 1, 3 do
        local gx = num(marks[i])
        if gx ~= nil and gx > g + 0.000001 and (best == nil or gx < best) then best = gx end
    end
    if best == nil then return nil end
    local d = math.ceil((best - g) * B.GrowDays() - 0.000001)
    if d < 1 then d = 1 end
    return d
end
