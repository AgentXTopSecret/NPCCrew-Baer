--
-- NPC Crew -- Baer, Inhalt des Reiters "Talente" im Baeren-Fenster (Lauf baer-talente, PLAN_TALENTE.md 5; Kevins Antworten 14.11.2026 ~10:20,
-- baer/begleiter/ENTSCHEIDUNGEN.md -- sie gehen vor dem Plan: FREIE WAHL, irgendwelche 3 von 9, keine Reihen).
--
-- Kevin 14.11.2026: "im skilltree auf einen extra tab kann man die skillpunkte aisgeben und per knopf altivieten dann leuchtet der skill hell
-- und ist permanent altiv" -- "skills vergeben muss bestaetigt werden beim klicken" -- "genau also am ende genau 3 punkte zum verteilen".
--
-- Hier steht nur das MODELL (fertige Texte, Zustaende, Tooltips) -- das Zeichnen und Klicken macht client/ISUI/BanditsNPCBearTalentTab.lua, die
-- Reiterleiste client/ISUI/BanditsNPCBearWindow.lua. Rein bis auf U.T (Texte) und B.* (Kern): keine Engine-Abfrage, kein Zeichnen. Gebaut nur im
-- 1-s-Takt des Fensters (U.WinModel, client/BanditsNPCBearWinData.lua), nie je Bild; die festen Texte einmal je Sitzung (Tabelle TS).
-- EINE Wahrheit: der Zustand jeder Kachel kommt aus den reinen Regeln des Kerns (shared/BanditsNPCBearTalentRules.lua) auf dem Sicht-Eintrag
-- (Felder tal / talE / talNx / talRo / talRw / talRd, tal/schnittstelle.md K3) -- dieselben Regeln, mit denen der Schreiber die Bitte prueft.
-- Graue Kacheln und eine Ablehnung des Schreibers laufen so nie auseinander; entscheiden tut immer der Schreiber.
--   aktiv        B.TalentOn(v, k) (zuerst: bei 3 gelernten liefert B.TalentCan fuer ein gelerntes "max")
--   waehlbar     B.TalentCan(v, k) ok
--   kommt spaeter "soon" (Angler bis F5) -- auch wenn "max" zuerst kommt, steht beim Angler "kommt spaeter" (nur Anzeige; er ist so oder so zu)
--   gesperrt     "max" / "point" / alles andere
-- Alle Zahlen der Texte liest das Fenster aus B.CFG (Block "Talente", Rueckfall = Kevins Werte) -- keine eigene Wahrheit.
-- Fehlt der Kern der Talente (B.TALENTS / B.TalentCan), gibt U.TalentModel nil und das Fenster hat keinen Reiter.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Rich-Text des Vanilla-Tooltips wie client/BanditsNPCBearWinData.lua (Formen V:client/ISUI/ISWorldObjectContextMenu.lua:376,
-- V:client/ISUI/ISGarmentUI.lua:136). Nie "<" oder ">" in UI.json: die Marken stehen nur hier.
local TIP_HEAD = " <RGB:1,0.7,0.3> "
local TIP_BODY = " <LINE> <RGB:1,1,1> "
local TIP_LINE = " <LINE> "

-- Text-Schluessel je Talent, ausgeschrieben (jeder im Code zu finden). Name / kurze Wirkung / Tooltip.
local KEY = {
    frugal = { "UI_BN_Bear_Talent_Frugal", "UI_BN_Bear_Talent_Frugal_Short", "UI_BN_Bear_Talent_Frugal_Tip" },
    fur = { "UI_BN_Bear_Talent_Fur", "UI_BN_Bear_Talent_Fur_Short", "UI_BN_Bear_Talent_Fur_Tip" },
    stamina = { "UI_BN_Bear_Talent_Stamina", "UI_BN_Bear_Talent_Stamina_Short", "UI_BN_Bear_Talent_Stamina_Tip" },
    paw = { "UI_BN_Bear_Talent_Paw", "UI_BN_Bear_Talent_Paw_Short", "UI_BN_Bear_Talent_Paw_Tip" },
    mule = { "UI_BN_Bear_Talent_Mule", "UI_BN_Bear_Talent_Mule_Short", "UI_BN_Bear_Talent_Mule_Tip" },
    alert = { "UI_BN_Bear_Talent_Alert", "UI_BN_Bear_Talent_Alert_Short", "UI_BN_Bear_Talent_Alert_Tip" },
    tough = { "UI_BN_Bear_Talent_Tough", "UI_BN_Bear_Talent_Tough_Short", "UI_BN_Bear_Talent_Tough_Tip" },
    crit = { "UI_BN_Bear_Talent_Crit", "UI_BN_Bear_Talent_Crit_Short", "UI_BN_Bear_Talent_Crit_Tip" },
    fisher = { "UI_BN_Bear_Talent_Fisher", "UI_BN_Bear_Talent_Fisher_Short", "UI_BN_Bear_Talent_Fisher_Tip" },
}
-- Zustand -> Text-Schluessel und Farbe der Zustandszeile (Farben: client/ISUI/BanditsNPCBearWinParts.lua)
local ST_KEY = { on = "UI_BN_Bear_Talent_StOn", free = "UI_BN_Bear_Talent_StFree", locked = "UI_BN_Bear_Talent_StLocked",
    soon = "UI_BN_Bear_Talent_StSoon" }
local ST_ORDER = { "on", "free", "locked", "soon" }
-- In welchen Tooltip des Uebersicht-Reiters die Zusatzzeile "Perk x: ..." eines gelernten Talents kommt (PLAN_TALENTE.md 5.4)
local LINE_AT = { fur = { "hp" }, stamina = { "sta" }, mule = { "carry" }, paw = { "melee" }, crit = { "melee" }, frugal = { "hun", "thr" },
    tough = { "hp" }, alert = { "melee" } }

local TS = nil      -- feste Texte dieser Sitzung

-- Fester Wert des Kerns (B.CFG) als Zahl, sonst def (Rueckfall = Kevins Werte, tal/schnittstelle.md K7).
local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil or v ~= v then return def end
    return v
end

-- Zahl fuer einen Text: auf eine Nachkommastelle (24.000000001 -> 24, 1.5 bleibt); B.T setzt das Dezimalzeichen der Sprache (B.DecText).
local function nice(v)
    return math.floor(v * 10 + 0.5) / 10
end

local function maxN()
    local m = math.floor(cfgNum("talMax", 3))
    if m < 0 then m = 0 end
    if m > 3 then m = 3 end             -- harter Deckel 3 wie der Kern (shared/BanditsNPCBearTalentRules.lua maxN; Nachbesserung, nur Anzeige)
    return m
end

-- Zahlen je Talent fuer kurze Wirkung und Tooltip (bis zu drei, wie die Platzhalter in texte_tal_daten.py).
local function argsOf(k)
    if k == "frugal" then
        local base = 100 / cfgNum("needRiseH", 6.25)                       -- 0 -> 100 % in 16 Wachstunden (K1, B.CFG.needRiseH)
        local with = base / cfgNum("talFrugalK", 16 / 24)
        return nice(with), nice(base)
    elseif k == "fur" then
        return nice(cfgNum("talFurHp", 250))
    elseif k == "stamina" then
        return nice(cfgNum("talStaPct", 0.30) * 100), nice(cfgNum("talStaRegK", 1.5))
    elseif k == "paw" then
        return nice(cfgNum("talPawPush", 2.0)), nice(cfgNum("talPawKnock", 100))
    elseif k == "mule" then
        return nice(cfgNum("talMuleKg", 50))
    elseif k == "alert" then
        return nice((cfgNum("talAlertK", 1.5) - 1) * 100)
    elseif k == "tough" then
        local h = cfgNum("downedHours", 12)
        return nice(cfgNum("talHealK", 2.0)), nice(h * cfgNum("talDownK", 0.5)), nice(h)
    elseif k == "crit" then
        return nice(cfgNum("talCritPct", 25)), nice(cfgNum("talCritK", 2.0))
    end
    return nice(cfgNum("talFishK", 2))
end

-- Feste Texte einmal je Sitzung (Sprache wechselt nur mit Neustart). Nur B.TALENTS-Schluessel mit Text-Schluessel oben.
local function statics()
    if TS ~= nil then return TS end
    local s = { name = {}, short = {}, tip = {}, st = {}, keys = {} }
    local list = B.TALENTS
    if type(list) == "table" then
        for i = 1, #list do
            local k = list[i]
            local key = KEY[k]
            if key then
                local a1, a2, a3 = argsOf(k)
                s.keys[#s.keys + 1] = k
                s.name[k] = U.T(key[1])
                s.short[k] = U.T(key[2], a1, a2, a3)
                s.tip[k] = U.T(key[3], a1, a2, a3)
            end
        end
    end
    for i = 1, #ST_ORDER do s.st[ST_ORDER[i]] = U.T(ST_KEY[ST_ORDER[i]]) end
    s.tabMain, s.tabTal = U.T("UI_BN_Bear_Win_TabMain"), U.T("UI_BN_Bear_Win_TabTalents")
    s.tabTip = TIP_HEAD .. s.tabTal .. TIP_BODY .. U.T("UI_BN_Bear_Win_TabTalentsTip")
    s.hintFree, s.hintDone, s.hintWait = U.T("UI_BN_Bear_Talent_HintFree"), U.T("UI_BN_Bear_Talent_HintDone"), U.T("UI_BN_Bear_Talent_HintWait")
    s.tipLearn, s.tipOn, s.tipPoint, s.tipSoon = U.T("UI_BN_Bear_Talent_TipLearn"), U.T("UI_BN_Bear_Talent_TipOn"),
        U.T("UI_BN_Bear_Talent_TipPoint"), U.T("UI_BN_Bear_Talent_TipSoon")
    s.tipMax = U.T("UI_BN_Bear_Talent_TipMax", maxN())
    s.reset, s.resetOff = U.T("UI_BN_Bear_Talent_Reset"), U.T("UI_BN_Bear_Talent_ResetOff")
    s.resetTip = U.T("UI_BN_Bear_Talent_ResetTip")
    s.whyOff, s.whyNone = U.T("UI_BN_Bear_Why_TalentResetOff"), U.T("UI_BN_Bear_Why_TalentNone")
    s.pointsAll = U.T("UI_BN_Bear_Talent_PointsAll", maxN())
    -- Breiteste Texte fuer das Legen (das Fenster misst sie einmal je Legen; Breite waechst nur, wenn ein Text nicht passt)
    s.widePoints = U.T("UI_BN_Bear_Talent_Points", maxN(), maxN(), maxN())
    s.wideNext = U.T("UI_BN_Bear_Talent_HintNext", 88)
    s.wideWait = U.T("UI_BN_Bear_Talent_ResetWait", U.WaitText and U.WaitText(88) or "88")
    TS = s
    return s
end
U.TalentStatics = statics

-- Gibt es die Talente? (Kern mit den reinen Regeln geladen.)
function U.TalentOn()
    return type(B.TALENTS) == "table" and B.TalentCan ~= nil and B.TalentOn ~= nil and B.TalentFree ~= nil and B.TalentN ~= nil
end

local function isNum(v)
    return type(v) == "number" and v == v
end

-- Zustand einer Kachel (siehe Kopf).
local function stateOf(v, k)
    if B.TalentOn(v, k) then return "on" end
    local ok, why = B.TalentCan(v, k)
    if ok then return "free" end
    if why == "soon" or (k == "fisher" and not (B.CFG and B.CFG.talFishOn == true)) then return "soon" end
    return "locked", why
end

-- Zeile "naechster Punkt" aus der Sicht (talNx, ganze Spieltage) oder nil.
local function nextLine(v)
    if isNum(v.talNx) and v.talNx >= 1 then return U.T("UI_BN_Bear_Talent_HintNext", math.floor(v.talNx)) end
    return nil
end

-- Kachel-Tooltip: Kopf (Name), Wirkung mit Zahlen, dann was der Zustand bedeutet.
local function tileTip(s, v, k, st, why)
    local t = TIP_HEAD .. s.name[k] .. TIP_BODY .. s.tip[k]
    if k == "fur" and st ~= "on" and isNum(v.hpMax) and v.hpMax > 0 then
        t = t .. TIP_LINE .. U.T("UI_BN_Bear_Talent_FurNow", math.floor(v.hpMax + 0.5), math.floor(v.hpMax + cfgNum("talFurHp", 250) + 0.5))
    end
    if st == "on" then
        t = t .. TIP_LINE .. s.tipOn
    elseif st == "free" then
        t = t .. TIP_LINE .. s.tipLearn
    elseif st == "soon" then
        t = t .. TIP_LINE .. s.tipSoon
    elseif why == "max" then
        t = t .. TIP_LINE .. s.tipMax
    else
        t = t .. TIP_LINE .. s.tipPoint
        local nx = nextLine(v)
        if nx then t = t .. TIP_LINE .. nx end
    end
    return t
end

-- Knopf "Zuruecksetzen": grau mit Grund (Sandbox aus / nichts gelernt / Wartezeit) -- dieselben Gruende, die der Schreiber meldet
-- (tal/schnittstelle.md K5); note = kleiner Text links daneben.
local function resetOf(s, v, used)
    local e = { label = s.reset, state = "normal", note = "" }
    local why = nil
    if v.talRo ~= true then
        why, e.note = s.whyOff, s.resetOff
    elseif used <= 0 then
        why = s.whyNone
    elseif isNum(v.talRw) and v.talRw > 0 then
        local w = U.WaitText and U.WaitText(v.talRw) or tostring(math.ceil(v.talRw))
        why = U.T("UI_BN_Bear_Why_TalentResetWait", w)
        e.note = U.T("UI_BN_Bear_Talent_ResetWait", w)
    end
    if why then
        e.state = "off"
        e.tip = TIP_HEAD .. s.reset .. TIP_BODY .. why .. TIP_LINE .. s.resetTip
    else
        e.tip = TIP_HEAD .. s.reset .. TIP_BODY .. s.resetTip
    end
    return e
end

-- ---------------------------------------------------------------------------
-- U.TalentModel(v): Modell des Reiters fuer den Sicht-Eintrag v (eigener Baer). nil ohne Kern der Talente. Neue Tabelle je Aufruf (1-s-Takt).
--   free / used / max / earned     Zahlen (aus den Regeln des Kerns)
--   badge                          freie Punkte fuer das Abzeichen am Reiter (nil bei 0)
--   head                           rechts in der Kopfzeile der Karte
--   hint, hintCol                  Fusszeile der Karte links (Farbe "honeyText" wenn ein Punkt frei ist)
--   tiles[i] = { k, state, name, short, stTxt, tip }   in der Reihenfolge von B.TALENTS
--   reset = { label, state, tip, note }
-- ---------------------------------------------------------------------------
function U.TalentModel(v)
    if not U.TalentOn() or type(v) ~= "table" then return nil end
    local s = statics()
    local t = { tiles = {}, title = s.tabTal }
    t.max = maxN()
    t.used = B.TalentN(v)
    t.free = B.TalentFree(v)
    t.earned = (B.TalentEarned and B.TalentEarned(v)) or 0
    if t.free > 0 then t.badge = t.free end
    if t.used >= t.max then
        t.head = s.pointsAll
    else
        t.head = U.T("UI_BN_Bear_Talent_Points", t.free, t.used, t.max)
    end
    if t.used >= t.max then
        t.hint, t.hintCol = s.hintDone, "dim"
    elseif t.free > 0 then
        t.hint, t.hintCol = s.hintFree, "honeyText"
    else
        t.hint, t.hintCol = nextLine(v) or s.hintWait, "dim"
    end
    for i = 1, #s.keys do
        local k = s.keys[i]
        local st, why = stateOf(v, k)
        t.tiles[i] = { k = k, state = st, name = s.name[k], short = s.short[k], stTxt = s.st[st], tip = tileTip(s, v, k, st, why) }
    end
    t.reset = resetOf(s, v, t.used)
    return t
end

-- ---------------------------------------------------------------------------
-- U.TalentLines(v): Zusatzzeilen fuer die Tooltips des Uebersicht-Reiters (PLAN_TALENTE.md 5.4) -- je gelerntem Talent "Perk <Name>: <Wirkung>"
-- an Leben / Ausdauer / Last / Nahkampfschaden / Hunger / Durst. Rueckgabe { hp = "...", ... } (Zeilen mit TIP_LINE verbunden) oder nil.
-- ---------------------------------------------------------------------------
function U.TalentLines(v)
    if not U.TalentOn() or type(v) ~= "table" or v.tal == nil then return nil end
    local s = statics()
    local list = B.TalentList and B.TalentList(v) or {}
    if #list == 0 then return nil end
    local out = {}
    for i = 1, #list do
        local k = list[i]
        local at = LINE_AT[k]
        if at and s.name[k] then
            local line = U.T("UI_BN_Bear_Win_TalentLine", s.name[k], s.short[k])
            for j = 1, #at do
                local a = at[j]
                if out[a] then out[a] = out[a] .. TIP_LINE .. line else out[a] = line end
            end
        end
    end
    return out
end

-- Text der Bestaetigung (Kevin E:815 "skills vergeben muss bestaetigt werden beim klicken"): Zeilen mit echtem Zeilenumbruch -- Vanillas
-- ISModalDialog misst und zeichnet Zeile fuer Zeile (V:client/ISUI/ISModalDialog.lua:166-174 CalcSize teilt am Umbruch; :188 macht aus "\n" im
-- Text auch einen). bearName = Name des Baeren (U.CubName), k = Talent. Nachbesserung C5: der Umbruch als Lua-Zeichenfolge "\n" wie in Vanilla
-- (Text .. "\n" .. Text: V:client/ISUI/ISWorldObjectContextMenu.lua:1167) statt string.char(10) -- gleiches Zeichen, keine Bibliotheks-Funktion.
local NL = "\n"
function U.TalentAskText(bearName, k, usedAfter)
    local s = statics()
    if not s.name[k] then return nil end
    return U.T("UI_BN_Bear_Talent_LearnAsk", bearName or "", s.name[k]) .. NL .. s.short[k] .. NL
        .. U.T("UI_BN_Bear_Talent_LearnAsk2", usedAfter, maxN())
end

function U.TalentResetText(bearName, earned, days)
    local t = U.T("UI_BN_Bear_Talent_ResetAsk", bearName or "") .. NL .. U.T("UI_BN_Bear_Talent_ResetAsk2", earned)
    local d = tonumber(days)
    if d ~= nil and d >= 1 then
        t = t .. NL .. U.T("UI_BN_Bear_Talent_ResetAskDays", math.floor(d))
    else
        t = t .. NL .. U.T("UI_BN_Bear_Talent_ResetAskAny")
    end
    return t
end

-- Je Spielstart frisch (feste Texte neu lesen; Events.OnGameStart: V:client/Chat/ISChat.lua:1186).
local function onGameStart()
    TS = nil
end
Events.OnGameStart.Add(onGameStart)
