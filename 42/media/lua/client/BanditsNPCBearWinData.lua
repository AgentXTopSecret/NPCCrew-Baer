--
-- NPC Crew -- Baer, Inhalt des Baeren-Fensters (F1, PLAN_F1.md 1.4-1.6, 7.5): welche Baeren dem Spieler gehoeren (U.WinBears) und
-- das fertige Modell eines Baeren (U.WinModel) -- alle Texte, Zahlen, Knopf-Zustaende und Tooltips, die das Fenster zeichnet.
--
-- Rein bis auf U.T (Texte) und B.* (Kern): kein Zeichnen, keine Engine-Abfrage ausser player:getX/getY/getVehicle des uebergebenen
-- Spielers (V:client/Fishing/TensionUI.lua:11, V:client/ISUI/Hutch/ISHutchMenu.lua:8). Gebaut wird das Modell nur bei neuer Sicht
-- und hoechstens 1 x je Sekunde (client/ISUI/BanditsNPCBearWindow.lua), nie je Bild. Die festen Texte (Knoepfe, Titel, Zustaende,
-- Hinweise) holt U.T nur einmal je Sitzung (Tabelle ST, gedeckelt durch die feste Zahl der Schluessel).
-- Daten: der Sicht-Eintrag des Kerns (S:server/BanditsNPCBearRegistry.lua viewEntry, S:server/BanditsNPCBearGrow.lua B.GrowView;
-- Felder PLAN_F1.md 5.3: mode pas u ld hide sit cm busy, x* carry dodge fgtB fish nose, dazu B1b-B1e: name owner st x y ride callWait
-- bd sz hp hpMax sta staMax day nst nxt). Fehlt ein Wert, steht "--" bzw. die Zeile faellt weg -- nie geraten (PLAN_F1.md 1.4, 1.5).
-- Was der Spieler sieht, ist nur eine Vorpruefung: entscheiden tut immer der Schreiber (B.Handle; Einzelspieler: dasselbe Programm,
-- Mehrspieler: der Server).
-- F1B (PLAN_F1B.md 3.4, 5.3): die Fusszeile nennt die Tasten, die gelten ("E near your bear", die Fern-Taste, falls gesetzt; Namen aus
-- U.WinKeyName, client/BanditsNPCBearKey.lua); der dritte Schalter "Growth line" (U.AgeOn, client/BanditsNPCBearTags.lua) traegt
-- ageShow = der Baer waechst noch (Sicht mit day UND nst) -- ausgewachsen verschwindet er aus dem Fenster.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Rich-Text des Vanilla-Tooltips (ISToolTip -> ISRichTextPanel): Kopfzeile in der Titelfarbe, danach weiss, Zeilen ueber " <LINE> ".
-- Formen: " <LINE> <RGB:1,0,0> " V:client/ISUI/ISWorldObjectContextMenu.lua:376, " <LINE> " V:client/ISUI/ISGarmentUI.lua:136.
-- Nie "<" oder ">" in UI.json (Uebernahme-Regel): die Marken stehen nur hier.
local TIP_HEAD = " <RGB:1,0.7,0.3> "
local TIP_BODY = " <LINE> <RGB:1,1,1> "
local TIP_LINE = " <LINE> "

local CMDS = { "follow", "stay", "sit", "roam", "come", "unstuck" }
U.WIN_CMDS = CMDS

-- Faehigkeiten in der Reihenfolge von B.SKILLS (S:shared/BanditsNPCBearStats.lua:110). Jeder Schluessel ausgeschrieben.
-- later = ehrlicher Satz, wo die Faehigkeit noch nicht (ganz) wirkt (PLAN_F1.md 1.5; Toughness: der Bonus wirkt, Erfahrung gibt es
-- erst mit dem Kampf -> eigener Satz Win_LaterGrow, Zusatz der OBERFLAECHE).
local SKILL_ROWS = {
    { key = "agi", name = "UI_BN_Bear_Win_Sk_Agi", tip = "UI_BN_Bear_Win_SkTip_Agi", from = "UI_BN_Bear_Win_SkFrom_Agi",
        later = "UI_BN_Bear_Win_LaterFight" },
    { key = "vit", name = "UI_BN_Bear_Win_Sk_Vit", tip = "UI_BN_Bear_Win_SkTip_Vit", from = "UI_BN_Bear_Win_SkFrom_Vit",
        later = "UI_BN_Bear_Win_LaterGrow" },
    { key = "con", name = "UI_BN_Bear_Win_Sk_Con", tip = "UI_BN_Bear_Win_SkTip_Con", from = "UI_BN_Bear_Win_SkFrom_Con" },
    { key = "fgt", name = "UI_BN_Bear_Win_Sk_Fgt", tip = "UI_BN_Bear_Win_SkTip_Fgt", from = "UI_BN_Bear_Win_SkFrom_Fgt",
        later = "UI_BN_Bear_Win_LaterFight" },
    { key = "fsh", name = "UI_BN_Bear_Win_Sk_Fsh", tip = "UI_BN_Bear_Win_SkTip_Fsh", from = "UI_BN_Bear_Win_SkFrom_Fsh",
        later = "UI_BN_Bear_Win_LaterFish" },
    { key = "nos", name = "UI_BN_Bear_Win_Sk_Nos", tip = "UI_BN_Bear_Win_SkTip_Nos", from = "UI_BN_Bear_Win_SkFrom_Nos",
        later = "UI_BN_Bear_Win_LaterNose" },
}
local SKILL_FIELD = { agi = "xAgi", vit = "xVit", con = "xCon", fgt = "xFgt", fsh = "xFsh", nos = "xNos" }

-- Zustand -> Text und Farbe (PLAN_F1.md 1.4, Farben 1.3)
local STATE = {
    missing = { "UI_BN_Bear_Win_St_Missing", "stMissing" }, ride = { "UI_BN_Bear_Win_St_Ride", "stRide" },
    away = { "UI_BN_Bear_Win_St_Away", "stAway" }, hide = { "UI_BN_Bear_Win_St_Hide", "stHide" },
    come = { "UI_BN_Bear_Win_St_Come", "stCome" }, follow = { "UI_BN_Bear_Win_St_Follow", "stFollow" },
    stay = { "UI_BN_Bear_Win_St_Stay", "stStay" }, sit = { "UI_BN_Bear_Win_St_Sit", "stSit" },
    roam = { "UI_BN_Bear_Win_St_Roam", "stRoam" },
}
local STATE_ORDER = { "missing", "ride", "away", "hide", "come", "follow", "stay", "sit", "roam" }
local DIR_KEY = { N = "UI_BN_Bear_Dir_N", NE = "UI_BN_Bear_Dir_NE", E = "UI_BN_Bear_Dir_E", SE = "UI_BN_Bear_Dir_SE",
    S = "UI_BN_Bear_Dir_S", SW = "UI_BN_Bear_Dir_SW", W = "UI_BN_Bear_Dir_W", NW = "UI_BN_Bear_Dir_NW" }
local BTN_KEY = { follow = "UI_BN_Bear_Win_Follow", stay = "UI_BN_Bear_Win_Stay", sit = "UI_BN_Bear_Win_Sit",
    roam = "UI_BN_Bear_Win_Roam", come = "UI_BN_Bear_Win_Come", unstuck = "UI_BN_Bear_Win_Unstuck" }

local ST = nil      -- feste Texte dieser Sitzung (einmal ueber U.T geholt)

local function statics()
    if ST ~= nil then return ST end
    local s = {}
    s.bodyCub = U.T("UI_BN_Bear_Win_BodyCub")
    s.bodyBig = U.T("UI_BN_Bear_Win_BodyBear")
    s.grown = U.T("UI_BN_Bear_Win_Grown")
    s.here = U.T("UI_BN_Bear_Win_Here")
    s.none = U.T("UI_BN_Bear_Win_None")
    s.rename = U.T("UI_BN_Bear_Win_Rename")
    s.tCond, s.tSkills, s.tOrders = U.T("UI_BN_Bear_Win_Cond"), U.T("UI_BN_Bear_Win_Skills"), U.T("UI_BN_Bear_Win_Orders")
    s.tHealth, s.tStamina, s.tCarry = U.T("UI_BN_Bear_Win_Health"), U.T("UI_BN_Bear_Win_Stamina"), U.T("UI_BN_Bear_Win_Carry")
    s.tLater = U.T("UI_BN_Bear_Win_Later")
    s.needs = { U.T("UI_BN_Bear_Win_Hunger"), U.T("UI_BN_Bear_Win_Thirst"), U.T("UI_BN_Bear_Win_Tired"), U.T("UI_BN_Bear_Win_Trust") }
    s.tipHealth = TIP_HEAD .. s.tHealth .. TIP_BODY .. U.T("UI_BN_Bear_Win_HealthTip")
    s.tipStamina = TIP_HEAD .. s.tStamina .. TIP_BODY .. U.T("UI_BN_Bear_Win_StaminaTip")
    s.tipCarry = TIP_HEAD .. s.tCarry .. TIP_BODY .. U.T("UI_BN_Bear_Win_CarryTip")
    s.tipLater = TIP_HEAD .. s.tLater .. TIP_BODY .. U.T("UI_BN_Bear_Win_LaterTip")
    s.state = {}
    for i = 1, #STATE_ORDER do
        local k = STATE_ORDER[i]
        s.state[k] = U.T(STATE[k][1])
    end
    s.btn = {}
    for i = 1, #CMDS do s.btn[CMDS[i]] = U.T(BTN_KEY[CMDS[i]]) end
    s.passive, s.tag = U.T("UI_BN_Bear_Win_Passive"), U.T("UI_BN_Bear_Win_Tag")
    s.tipStay, s.tipSit = U.T("UI_BN_Bear_Win_StayTip"), U.T("UI_BN_Bear_Win_SitTip")
    s.tipFollow, s.tipCome = U.T("UI_BN_Bear_Menu_FollowTip"), U.T("UI_BN_Bear_Win_ComeTip")
    s.tipPassive, s.tipTag = U.T("UI_BN_Bear_Win_PassiveTip"), U.T("UI_BN_Bear_Win_TagTip")
    s.tagOffAll, s.active = U.T("UI_BN_Bear_Win_TagOffAll"), U.T("UI_BN_Bear_Win_Active")
    -- F1B: Wachstums-Schalter (Text, Tooltip, Hinweis auf den Hauptschalter TagAge in Optionen -> Mods)
    s.growth, s.tipGrowth = U.T("UI_BN_Bear_Win_Growth"), U.T("UI_BN_Bear_Win_GrowthTip")
    s.growthOffAll = U.T("UI_BN_Bear_Win_GrowthOffAll")
    s.whyCar, s.whyFar = U.T("UI_BN_Bear_Why_InCar"), U.T("UI_BN_Bear_Why_Far")
    s.hintMissing, s.hintRide, s.hintAway = U.T("UI_BN_Bear_Win_HintMissing"), U.T("UI_BN_Bear_Win_HintRide"),
        U.T("UI_BN_Bear_Win_HintAway")
    s.hintEsc = U.T("UI_BN_Bear_Win_HintEsc")
    s.skName, s.skFrom, s.skLater = {}, {}, {}
    for i = 1, #SKILL_ROWS do
        local r = SKILL_ROWS[i]
        s.skName[i] = U.T(r.name)
        s.skFrom[i] = U.T(r.from)
        if r.later then s.skLater[i] = U.T(r.later) end
    end
    s.skTop = U.T("UI_BN_Bear_Win_SkTop")
    s.max = U.T("UI_BN_Bear_Win_Max")
    -- Breiteste Texte fuer das Legen des Fensters (Breite waechst nur, wenn ein Text nicht passt, PLAN_F1.md 1.1)
    s.wideVal = U.T("UI_BN_Bear_Win_Count", 888, 888)
    s.wideCarry = U.T("UI_BN_Bear_Win_CarryVal", 888)
    s.wideLv = U.T("UI_BN_Bear_Win_Lv", 10)
    s.widePct = U.T("UI_BN_Bear_Win_Pct", 100)
    s.wideUnstuck = U.T("UI_BN_Bear_Win_UnstuckWait", "9:59")
    s.wideDist = U.T("UI_BN_Bear_Win_LastSeen", 888, U.T("UI_BN_Bear_Dir_NW"))
    s.wideDist2 = U.T("UI_BN_Bear_Win_Dist", 888, U.T("UI_BN_Bear_Dir_NW"))
    ST = s
    return s
end
U.WinStatics = statics

local function isNum(v)
    return type(v) == "number" and v == v
end

local function clamp(v, lo, hi)
    if v < lo then return lo end
    if v > hi then return hi end
    return v
end

-- Sandbox-Zahl ueber den Kern (B.Opt klemmt und faellt selbst auf die Vorgabe zurueck); fehlt der Kern: def.
local function optNum(name, def)
    local v = nil
    if B.Opt then v = tonumber(B.Opt(name)) end
    if v == nil then return def end
    return v
end

local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Modus nach der Regel des Kerns (B.ModeOf, F1: follow / stay / sit / roam; nil und Unsinn = stay). Fehlt der Kern: dieselbe Regel.
local function modeOf(v)
    if B.ModeOf then return B.ModeOf(v) end
    local m = v.mode
    if m == "follow" or m == "sit" or m == "roam" then return m end
    return "stay"
end

-- Prozent als ganze Zahl oder "?" (fehlt der Wert in der Sicht, wird nichts geraten).
local function pctOf(v)
    if not isNum(v) then return "?" end
    return math.floor(v + 0.5)
end

-- Eigener Spieler-Schluessel: aus der Sicht (B.View.me.key, S:server/BanditsNPCBearRegistry.lua B.SlotsOf), sonst ueber den Kern.
local function myKey()
    local me = B.View and B.View.me
    if type(me) == "table" and me.key ~= nil then return me.key end
    local p = getSpecificPlayer(0)                      -- V:client/Farming/CFarmingSystem.lua:45
    if p and B.PlayerKey then return B.PlayerKey(p) end
    return nil
end

local function byId(a, b)
    if type(a.id) == type(b.id) then return a.id < b.id end
    return tostring(a.id) < tostring(b.id)
end

-- ---------------------------------------------------------------------------
-- U.WinBears(): eigene Eintraege der Sicht (gezaehmt oder vermisst), nach Kennung sortiert. Eigen = Besitzer ist mein Schluessel --
-- im Einzelspieler auch der feste Einzelspieler-Schluessel (wie S:client/ISUI/BanditsNPCBearHud.lua describeTag). Die Frische der
-- Sicht (U.Fresh) prueft der Aufrufer.
-- ---------------------------------------------------------------------------
function U.WinBears()
    local out = {}
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return out end
    local key = myKey()
    local sp = B.IsSP ~= nil and B.IsSP()
    for _, c in pairs(cubs) do
        if type(c) == "table" and c.id ~= nil and (c.st == "tame" or c.st == "missing") and c.owner ~= nil
            and (c.owner == key or (sp and c.owner == B.SP_KEY)) then
            out[#out + 1] = c
        end
    end
    if #out > 1 then table.sort(out, byId) end
    return out
end

-- U.WinMine(v): gehoert dieser Sicht-Eintrag mir (jeder Zustand, auch das Junge im Zaehmen)? Fuer die Taste (Nachbesserung F1 A2,
-- client/BanditsNPCBearKey.lua): an einem FREMDEN Baeren bleibt Vanillas Tier-Radial.
function U.WinMine(v)
    if type(v) ~= "table" or v.owner == nil then return false end
    if v.owner == myKey() then return true end
    return B.IsSP ~= nil and B.IsSP() and v.owner == B.SP_KEY
end

-- Rest der Call-Abklingzeit in ms (0 = bereit). Die Sicht traegt den Rest in Sekunden (callWait, nur fuer den Besitzer) zum
-- Zeitpunkt ihres Baus; abgezogen wird die Zeit seit ihrer Ankunft (U.viewAt) -- wie S:client/BanditsNPCBearMenu.lua callWaitMinutes.
local function callWaitMs(v, nowMs)
    local left = tonumber(v.callWait)
    if left == nil or left <= 0 then return 0 end
    local ms = left * 1000
    local at = U.viewAt
    if type(at) == "number" and type(nowMs) == "number" and nowMs >= at then ms = ms - (nowMs - at) end
    if ms <= 0 then return 0 end
    return ms
end

-- "m:ss" aus ms (aufgerundet auf ganze Sekunden). string.format("%d"): S:shared/BanditsNPCBear.lua argText.
local function clock(ms)
    local s = math.ceil(ms / 1000)
    local m = math.floor(s / 60)
    s = s - m * 60
    local ss = string.format("%d", s)
    if s < 10 then ss = "0" .. ss end
    return string.format("%d", m) .. ":" .. ss
end

-- Knopf-Eintrag (PLAN_F1.md 1.6): grau mit Grund (why) vor aktiv; Tooltip = Kopf (Knopftext) + Grund bzw. Erklaerung (+ "aktueller
-- Befehl").
local function cmdBtn(label, active, why, tip)
    local e = { label = label, state = "normal" }
    if why then
        e.state = "off"
        e.tip = TIP_HEAD .. label .. TIP_BODY .. why
        return e
    end
    if active then e.state = "active" end
    local t = TIP_HEAD .. label .. TIP_BODY .. (tip or "")
    if active then t = t .. TIP_LINE .. statics().active end
    e.tip = t
    return e
end

local function firstOf(a, b, c, d)
    if a then return a end
    if b then return b end
    if c then return c end
    if d then return d end
    return nil
end

-- Wirkung einer Faehigkeit mit der Zahl von jetzt (PLAN_F1.md 1.5 Tabelle; Zahlen aus der Sicht bzw. Kevins Formeln ENT:221-230).
local function skillEffect(key, v, L)
    if key == "agi" then
        return U.T("UI_BN_Bear_Win_SkTip_Agi", pctOf(v.dodge), math.floor(optNum("BearDodgeMax", 40) + 0.5))
    elseif key == "vit" then
        return U.T("UI_BN_Bear_Win_SkTip_Vit", math.floor(cfgNum("vitPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "con" then
        return U.T("UI_BN_Bear_Win_SkTip_Con", math.floor(cfgNum("conPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "fgt" then
        return U.T("UI_BN_Bear_Win_SkTip_Fgt", pctOf(v.fgtB), math.floor(optNum("BearFightBonusMax", 70) + 0.5))
    elseif key == "fsh" then
        return U.T("UI_BN_Bear_Win_SkTip_Fsh", pctOf(v.fish))
    end
    local nose = "?"
    if isNum(v.nose) then nose = math.floor(v.nose * 10 + 0.5) / 10 end
    return U.T("UI_BN_Bear_Win_SkTip_Nos", nose)
end

-- Faehigkeiten (PLAN_F1.md 1.5): Stufe, Fortschritt, Texte, Tooltip. known = die Sicht ist eine F1-Sicht: B.GrowView schickt ab F1 fuer
-- tame und missing IMMER carry / dodge / fgtB / fish / nose, die Erfahrung x* aber nur, wenn sie > 0 ist (fehlt = 0,
-- S:server/BanditsNPCBearGrow.lua B.GrowView). Traegt die Sicht nichts davon, ist es eine alte Sicht -> "--" statt einer geratenen 0.
local function skillsOf(v, s)
    local known = isNum(v.dodge) or isNum(v.carry)
    for i = 1, #SKILL_ROWS do
        if isNum(v[SKILL_FIELD[SKILL_ROWS[i].key]]) then known = true end
    end
    if not B.SkillProgress then known = false end
    local out = {}
    for i = 1, #SKILL_ROWS do
        local r = SKILL_ROWS[i]
        local e = { key = r.key, name = s.skName[i], known = known, lv = 0, frac = 0, pct = 0 }
        local head, prog
        if known then
            local L, xpIn, need = B.SkillProgress(v, r.key)
            L = tonumber(L) or 0
            xpIn = tonumber(xpIn) or 0
            need = tonumber(need) or 0
            e.lv = L
            e.lvTxt = U.T("UI_BN_Bear_Win_Lv", L)
            if L >= 10 or need <= 0 then
                e.frac, e.pct, e.pctTxt = 1, 100, s.max
                prog = s.skTop
            else
                e.frac = clamp(xpIn / need, 0, 1)
                e.pct = math.floor(e.frac * 100)
                e.pctTxt = U.T("UI_BN_Bear_Win_Pct", e.pct)
                prog = U.T("UI_BN_Bear_Win_SkProg", math.floor(xpIn), math.floor(need + 0.5), L + 1)
            end
            head = U.T("UI_BN_Bear_Win_SkHead", e.name, L)
        else
            e.lvTxt = s.none
            e.pctTxt = ""
            head = e.name
        end
        local t = TIP_HEAD .. head .. TIP_BODY .. skillEffect(r.key, v, e.lv) .. TIP_LINE .. s.skFrom[i]
        if s.skLater[i] then t = t .. TIP_LINE .. s.skLater[i] end
        if prog then t = t .. TIP_LINE .. prog end
        e.tip = t
        out[i] = e
    end
    return out
end

-- Wert-Zeile Leben / Ausdauer (PLAN_F1.md 1.5): "jetzt / hoechst" und Balken aus Prozent (0..100) und Hoechstwert; fehlt einer:
-- "--" ohne Balken (frac nil), nie 0.
local function valueRow(label, pct, most, kind, s)
    local e = { label = label, val = s.none }
    if isNum(pct) and isNum(most) then
        local frac = clamp(pct / 100, 0, 1)
        local mx = math.floor(most + 0.5)
        if mx < 0 then mx = 0 end
        e.now = math.floor(frac * mx + 0.5)
        e.max = mx
        e.frac = frac
        e.val = U.T("UI_BN_Bear_Win_Count", e.now, mx)
        if U.WinRamp then e.r, e.g, e.b = U.WinRamp(kind, frac) end
    end
    return e
end

-- Zustand nach Vorrang (PLAN_F1.md 1.4): vermisst > faehrt mit > ausser Reichweite > versteckt > kommt > Modus.
local function stateOf(v, mode)
    if v.st == "missing" then return "missing" end
    if v.ride == true then return "ride" end
    if v.ld ~= true then return "away" end
    if v.hide == true then return "hide" end
    if v.cm == true then return "come" end
    return mode
end

-- ---------------------------------------------------------------------------
-- U.WinModel(v, player, nowMs): das fertige Modell eines Baeren (v = Eintrag aus U.WinBears). Neue Tabelle je Aufruf (1 x je Sekunde).
-- ---------------------------------------------------------------------------
function U.WinModel(v, player, nowMs)
    local s = statics()
    local d = { id = v.id, tCond = s.tCond, tSkills = s.tSkills, tOrders = s.tOrders, tLater = s.tLater, needs = s.needs,
        rename = s.rename, wide = s }
    local bd = v.bd
    d.name = U.CubName(v)
    -- Kopf: Koerper und Tag, naechste Stufe (Zahlen aus B.GrowView; fehlen sie, faellt die Zeile weg)
    local body = s.bodyCub
    if bd == "big" then body = s.bodyBig end
    if isNum(v.day) then
        d.sub = U.T("UI_BN_Bear_Win_Sub", body, math.floor(v.day))
    else
        d.sub = body
    end
    if v.nst ~= nil and isNum(v.nxt) then
        local left = math.floor(v.nxt)
        if left < 1 then left = 1 end
        d.next = U.T("UI_BN_Bear_Win_Next", U.StageName(v.nst), left)
    elseif isNum(v.day) then
        d.next = s.grown
    end
    -- Zustand, Chip-Farbe, Fusszeile
    local tame = (v.st == "tame")
    local mode = modeOf(v)
    local st = stateOf(v, mode)
    d.state = st
    d.chipText = s.state[st] or ""
    if U.WinColor then
        d.cr, d.cg, d.cb = U.WinColor(STATE[st][2])
    else
        d.cr, d.cg, d.cb = 1, 1, 1
    end
    if st == "missing" then
        d.footer = s.hintMissing
    elseif st == "ride" then
        d.footer = s.hintRide
    elseif st == "away" then
        d.footer = s.hintAway
    else
        -- F1B (PLAN_F1B.md 3.4): welche Tasten gelten. Liegen beide auf derselben Taste, gilt sie als Fern-Taste (oeffnet ueberall).
        local nn, fn = nil, nil
        if U.WinKeyName then nn, fn = U.WinKeyName() end
        if nn and fn and nn == fn then nn = nil end
        if nn and fn then
            d.footer = U.T("UI_BN_Bear_Win_HintBoth", nn, fn)
        elseif nn then
            d.footer = U.T("UI_BN_Bear_Win_HintNear", nn)
        elseif fn then
            d.footer = U.T("UI_BN_Bear_Win_Hint", fn)
        else
            d.footer = s.hintEsc
        end
    end
    -- Abstand: lebende Kopie (U.CubPos, S:client/ISUI/BanditsNPCBearHud.lua), sonst die letzte Stelle der Sicht (ganze Kacheln)
    local px, py = player:getX(), player:getY()         -- V:client/Fishing/TensionUI.lua:11
    local bx, by = nil, nil
    if isNum(v.x) and isNum(v.y) then bx, by = v.x + 0.5, v.y + 0.5 end
    if U.CubPos and v.ride ~= true then
        local lx, ly = U.CubPos(v.id)
        if lx ~= nil then bx, by = lx, ly end
    end
    if bx ~= nil then
        local dist = B.DistXY(px, py, bx, by)
        d.distN = dist
        local dirTxt = U.T(DIR_KEY[B.DirOf(bx - px, by - py)] or "UI_BN_Bear_Dir_N")
        local n = math.floor(dist + 0.5)
        if st == "missing" or st == "away" then
            if n < 1 then n = 1 end
            d.dist = U.T("UI_BN_Bear_Win_LastSeen", n, dirTxt)
        elseif dist < 2 then
            d.dist = s.here
        else
            d.dist = U.T("UI_BN_Bear_Win_Dist", n, dirTxt)
        end
    end
    -- Werte
    d.hp = valueRow(s.tHealth, v.hp, v.hpMax, "hp", s)
    d.sta = valueRow(s.tStamina, v.sta, v.staMax, "sta", s)
    d.carry = { label = s.tCarry, val = s.none }
    if isNum(v.carry) then d.carry.val = U.T("UI_BN_Bear_Win_CarryVal", math.floor(v.carry + 0.5)) end
    d.tips = { hp = s.tipHealth, sta = s.tipStamina, carry = s.tipCarry, later = s.tipLater }
    d.skills = skillsOf(v, s)
    -- Befehle (PLAN_F1.md 1.6): Vorpruefung aus der Sicht, entscheiden tut der Schreiber
    local ride = (v.ride == true)
    local gone = (v.st == "missing") or (v.ld ~= true)
    local inCar = player:getVehicle() ~= nil            -- V:client/ISUI/Hutch/ISHutchMenu.lua:8
    local far = (not gone) and d.distN ~= nil and d.distN > optNum("BearFollowMaxDistance", 40)
    local cm = tame and v.cm == true
    local whyRide = ride and U.TB("UI_BN_Bear_Why_Riding", bd)
    local whyAway = gone and U.TB("UI_BN_Bear_Why_OutOfReach", bd)
    local whyCar = inCar and s.whyCar
    local whyFar = far and s.whyFar
    local act = nil
    if tame then act = mode end
    local radius = math.floor(optNum("BearRoamRadius", 12) + 0.5)
    local b = {}
    b.follow = cmdBtn(s.btn.follow, act == "follow" and not cm, firstOf(whyRide, whyAway, whyCar, whyFar), s.tipFollow)
    b.stay = cmdBtn(s.btn.stay, act == "stay", firstOf(whyRide, whyAway), s.tipStay)
    b.sit = cmdBtn(s.btn.sit, act == "sit", firstOf(whyRide, whyAway), s.tipSit)
    b.roam = cmdBtn(s.btn.roam, act == "roam", firstOf(whyRide, whyAway), U.T("UI_BN_Bear_Win_RoamTip", radius))
    b.come = cmdBtn(s.btn.come, cm, firstOf(whyRide, whyAway, whyCar, whyFar), s.tipCome)
    -- Unstuck = "Call to me" (B1c): geht auch fuer vermisste und nicht geladene; grau beim Mitfahren, im Fahrzeug, in der Abklingzeit
    local waitMs = callWaitMs(v, nowMs)
    local whyWait = nil
    if waitMs > 0 then
        -- Nachbesserung F1 B6: dieselbe m:ss-Uhr wie auf dem Knopf (nicht "about 4 min" neben "3:12"); das Menue behaelt Why_CallWait
        whyWait = U.TB("UI_BN_Bear_Win_CallWaitClock", bd, clock(waitMs))
    end
    local uLabel = s.btn.unstuck
    if waitMs > 0 then uLabel = U.T("UI_BN_Bear_Win_UnstuckWait", clock(waitMs)) end
    local cool = math.floor(optNum("BearCallCooldownMinutes", 5) + 0.5)
    b.unstuck = cmdBtn(uLabel, false, firstOf(whyRide, whyCar, whyWait), U.TB("UI_BN_Bear_Menu_CallTip", bd, cool))
    d.buttons = b
    d.ordersInfo = ""
    if act == "roam" then d.ordersInfo = U.T("UI_BN_Bear_Win_RoamInfo", radius) end
    -- Schalter: Passiv (Register, Sicht pas) und Namensschild (je Spieler, client/BanditsNPCBearTags.lua)
    local tagOn = true
    if U.TagOn then tagOn = U.TagOn(v) ~= false end
    local tagTip = TIP_HEAD .. s.tag .. TIP_BODY .. s.tipTag
    if U.Opt and U.Opt("TagShow", true) == false then tagTip = tagTip .. TIP_LINE .. s.tagOffAll end
    -- F1B (PLAN_F1B.md 5.3): Wachstums-Schalter -- an/aus je Baer (U.AgeOn, je Spieler), sichtbar nur, solange er waechst (nst fehlt,
    -- wenn er ausgewachsen ist: S:server/BanditsNPCBearGrow.lua:758, :786-787). TagAge aus (Hauptschalter): Hinweis im Tooltip.
    local ageOn = true
    if U.AgeOn then ageOn = U.AgeOn(v) ~= false end
    local ageTip = TIP_HEAD .. s.growth .. TIP_BODY .. s.tipGrowth
    if U.Opt and U.Opt("TagAge", true) == false then ageTip = ageTip .. TIP_LINE .. s.growthOffAll end
    d.toggles = { pas = (v.pas == true), tag = tagOn, pasLabel = s.passive, tagLabel = s.tag,
        pasTip = TIP_HEAD .. s.passive .. TIP_BODY .. s.tipPassive, tagTip = tagTip,
        age = ageOn, ageShow = isNum(v.day) and v.nst ~= nil, ageLabel = s.growth, ageTip = ageTip }
    return d
end
