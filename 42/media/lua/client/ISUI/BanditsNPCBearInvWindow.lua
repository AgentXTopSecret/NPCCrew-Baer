--
-- NPC Crew -- Baer, das Inventar-Fenster (F4, Lauf baer-f4, PLAN_F4.md 7, 8.2; Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md: der Baer traegt
-- ALLES, hoechstens 1000 Dinge; ansehen ueberall -- auch mit der Fern-Taste --, hineinlegen / herausnehmen nur daneben (3 Kacheln), nicht
-- waehrend er im Auto mitfaehrt; Packtaschen "Bear Packs" +150 kg ab halbstark -- Kevins Aenderung waehrend des Laufs).
--
-- Ein eigenes ISPanel mit moveWithMouse wie das Baeren-Fenster (client/ISUI/BanditsNPCBearWindow.lua; Vanilla V:client/ISUI/AdminPanel/
-- ISAdminTicketsUI.lua:1, :243, :253) mit denselben Bausteinen, Farben und Schriften (client/ISUI/BanditsNPCBearWinParts.lua: U.WinBtn,
-- U.WinRect, U.WinFrame, U.WinFonts, U.WinRamp, U.WIN_COL) und demselben Massstab (U.MarkerFactor(Bildhoehe, Option WinSize)).
-- Aufbau:
--   Kopf     "Inventory: Bruno" (UI_BN_Bear_Inv_Title), Schliessen; Zeile "Load 18.5 / 62 kg" mit Balken (gruen, fast voll orange, UEBER der Grenze
--            rot -- Nachbesserung P2) und rechts "140 / 1000 things" (bei 1000 in Warnfarbe, P7); Zeile Packtaschen: "Packs: on (+150 kg)" mit
--            "Take off" bzw. "No packs" mit "Put on".
--   Spalten  links "Your bear" (Liste des Schreibers, am Client nach Anzeige-Namen geordnet, P4), rechts "You" (dein Inventar samt Taschen) --
--            je 10 Zeilen und Seiten "<  1 / 3  >"; Mausrad blaettert eine Seite, Umschalt + Pfeil zehn (P6).
--            Zeile: Symbol, Name (Anzahl), Gewicht, Knopf "Take" / "Give" und bei mehreren Stuecken "All". Tooltip: Gewicht, Zustand,
--            frisch / alt / verdorben, gekocht / verbrannt / gefroren, Fuellung, Rest, Favorit, Baerenfutter -- was die Zeile des Schreibers traegt.
--   Fuss     der Grund, warum Geben / Nehmen gerade grau ist (Warnfarbe), bei 1000 Dingen "already carries 1000 things" (P7), sonst ein Hinweis.
-- Ansehen geht immer (auch vermisst, mitfahrend, nicht geladen: die Liste kommt aus dem Register des Schreibers). Grau mit Grund nur aus der
-- Sicht (U.InvWhy, U.InvGiveWhy, U.InvPacksWhy -- client/BanditsNPCBearInvClient.lua); ein Klick stellt nur Zeitaktionen an, entscheiden tut
-- der Schreiber in complete(). Kein Klick laeuft von selbst hin (nur der Rechtsklick "Put packs on" tut das, PLAN_F4.md 7).
-- Takt: Modell hoechstens 1 x je Sekunde und bei neuer Liste / Seite / Klick; je Bild nur fertige Felder zeichnen. Liste: beim Oeffnen, bei
-- neuer Fassung der Sicht (ivR), alle invKeepMs (30 s) solange offen; ohne Antwort 3 Versuche (U.InvAskState), dann "No answer".
-- Nur Spieler 0. Esc schliesst. Lage in layout.ini wie das Baeren-Fenster (nur x / y).
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"
require "ISUI/ISButton"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local Inv = ISPanel:derive("BanditsNPCBearInvWindow")      -- V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1

local LAYOUT_NAME = "BanditsNPCBearInvWindow"
local MODEL_MS = 1000
local FIT = 0.92
local ROWS = 10                                             -- Zeilen je Spalte und Seite
local NONE_AGAIN_MS = 10000                                 -- nach "No answer" so lange warten, dann neu fragen
local CLOSE_FILE = "media/ui/inventoryPanes/Button_Close.png"
local TIP_HEAD = " <RGB:1,0.7,0.3> "                        -- Rich-Text wie client/BanditsNPCBearWinData.lua (ISRichTextPanel)
local TIP_BODY = " <LINE> <RGB:1,1,1> "
local TIP_LINE = " <LINE> "
local SIDES = { "bear", "you" }

local W = { win = nil, close = nil }
local ST = nil

local function col(key)
    local c = U.WIN_COL and U.WIN_COL[key]
    return c or { 1, 1, 1, 1 }
end

local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

local function isNum(v)
    return type(v) == "number" and v == v
end

local function tw(font, s)
    if s == nil or s == "" then return 0 end
    return getTextManager():MeasureStringX(font, s)        -- V:client/ISUI/ISButton.lua:450
end

local function screen()
    local core = getCore()
    return core:getScreenWidth(), core:getScreenHeight()   -- V:client/Challenge/WinterIsComing.lua:18
end

local function sizeIdx()
    local v = 1
    if U.Opt then v = tonumber(U.Opt("WinSize", 1)) or 1 end
    return math.floor(v)
end

-- Feste Texte einmal je Sitzung.
local function statics()
    if ST ~= nil then return ST end
    local s = {}
    s.load, s.give, s.take, s.all = U.T("UI_BN_Bear_Win_Load"), U.T("UI_BN_Bear_Inv_Give"), U.T("UI_BN_Bear_Inv_Take"),
        U.T("UI_BN_Bear_Inv_All")
    s.you, s.putOn, s.takeOff = U.T("UI_BN_Bear_Inv_You"), U.T("UI_BN_Bear_Inv_PutOn"), U.T("UI_BN_Bear_Inv_TakeOff")
    s.noPacks, s.empty, s.youEmpty = U.T("UI_BN_Bear_Win_LoadNoPacks"), U.T("UI_BN_Bear_Inv_Empty"), U.T("UI_BN_Bear_Inv_YouEmpty")
    s.wait, s.none, s.unknown = U.T("UI_BN_Bear_Inv_Wait"), U.T("UI_BN_Bear_Inv_NoAnswer"), U.T("UI_BN_Bear_Inv_Unknown")
    s.fresh = { [0] = U.T("UI_BN_Bear_Inv_TipFresh"), [1] = U.T("UI_BN_Bear_Inv_TipStale"), [2] = U.T("UI_BN_Bear_Inv_TipRotten") }
    s.cooked, s.burnt, s.frozen = U.T("UI_BN_Bear_Inv_TipCooked"), U.T("UI_BN_Bear_Inv_TipBurnt"), U.T("UI_BN_Bear_Inv_TipFrozen")
    s.fav, s.unkTip = U.T("UI_BN_Bear_Inv_TipFav"), U.T("UI_BN_Bear_Why_InvUnknown")     -- TipFood je Koerper in bearTip (P10)
    s.hint, s.over = U.T("UI_BN_Bear_Inv_Hint"), U.T("UI_BN_Bear_Win_LoadOver")
    s.putOnTip, s.takeOffTip = U.T("UI_BN_Bear_Inv_PutOnTip", math.floor(cfgNum("bagAdd", 150) + 0.5)), U.T("UI_BN_Bear_Inv_TakeOffTip")
    s.allTakeTip, s.allGiveTip = U.T("UI_BN_Bear_Inv_AllTakeTip"), U.T("UI_BN_Bear_Inv_AllGiveTip")
    s.wornTip = U.T("UI_BN_Bear_Why_InvWorn")
    s.giveTip, s.takeTip = U.T("UI_BN_Bear_Inv_GiveTip"), U.T("UI_BN_Bear_Inv_TakeTip")
    -- breiteste wechselnde Texte (die Breite waechst nur, wenn einer nicht passt)
    s.wideLoad = U.T("UI_BN_Bear_Win_LoadVal", "888.8", "888")
    s.wideThings = U.T("UI_BN_Bear_Inv_Things", 1000, 1000)
    s.widePacks = U.T("UI_BN_Bear_Win_LoadPacks", 888)
    s.wideKg = U.T("UI_BN_Bear_Inv_Kg", "888.8")
    s.widePage = U.T("UI_BN_Bear_Win_Count", 100, 100)
    ST = s
    return s
end

-- ---------------------------------------------------------------------------
-- Masse (Pixel bei f = 1, jede Zahl x f gerundet), wie das Baeren-Fenster
-- ---------------------------------------------------------------------------
local function metrics(f, sw, sh, idx)
    local m = { f = f, sw = sw, sh = sh, idx = idx }
    local function R(v) return math.floor(v * f + 0.5) end
    for _, v in ipairs({ 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 22, 24, 28, 40, 160, 180, 240, 860 }) do m["R" .. v] = R(v) end
    m.t = math.max(1, math.floor(f))
    m.bold = math.max(1, math.floor(f / 2))
    m.fName, m.fBody, m.fSmall, m.ln, m.lb, m.ls = U.WinFonts(f)
    local s = statics()
    local P = m.R16
    m.P = P
    m.ty = m.R12
    m.l2y = m.ty + m.ln + m.R8                              -- Zeile Load
    m.barH = m.R10
    m.l3y = m.l2y + m.lb + m.R4 + m.barH + m.R8             -- Zeile Packtaschen
    m.pbh = math.max(m.R24, m.ls + m.R8)                    -- Knopf "Put on" / "Take off"
    m.headH = m.l3y + math.max(m.lb, m.pbh) + m.R10
    m.rowH = math.max(m.R28, m.lb + m.R8)
    m.icon = m.R22
    m.btnH = m.rowH - m.R4
    m.pgH = m.R24
    m.cardTop = m.R10 + m.lb + m.R8                         -- Kartenrand + Titel bis zur ersten Zeile
    m.cardH = m.cardTop + ROWS * m.rowH + m.R8 + m.pgH + m.R10
    m.y1 = m.headH + m.R8
    m.y3 = m.y1 + m.cardH + m.R10
    m.H = m.y3 + m.ls + m.R14
    -- Breite: Spalte = Symbol + Name (mind. 160) + Gewicht + zwei Knoepfe; Kopf = Load-Zeile + Zaehler
    m.b1W = math.max(tw(m.fSmall, s.give), tw(m.fSmall, s.take)) + m.R16
    m.b2W = tw(m.fSmall, s.all) + m.R16
    m.kgW = tw(m.fSmall, s.wideKg)
    local cw = m.R4 + m.icon + m.R6 + m.R160 + m.R8 + m.kgW + m.R8 + m.b1W + m.R4 + m.b2W + m.R6
    local need = math.max(m.R860, 2 * P + 2 * cw + m.R16)
    m.loadLblW = tw(m.fBody, s.load)
    local head = 2 * P + m.loadLblW + m.R12 + tw(m.fBody, s.wideLoad) + m.R12 + m.R240 + m.R24 + tw(m.fBody, s.wideThings)
    if head > need then need = head end
    m.putW = math.max(tw(m.fSmall, s.putOn), tw(m.fSmall, s.takeOff)) + m.R16
    m.W = need
    m.CW = math.floor((m.W - 2 * P - m.R16) / 2)
    m.W = 2 * P + 2 * m.CW + m.R16
    m.lx, m.rx = P, P + m.CW + m.R16
    m.barX = P + m.loadLblW + m.R12
    m.barW = m.R240
    return m
end

local function put(el, x, y, w, h)
    el:setX(x)                                              -- V:client/ISUI/ISUIElement.lua:195-245
    el:setY(y)
    el:setWidth(w)
    el:setHeight(h)
end

-- Lage der Kinder.
local function place(win, m)
    local P = m.P
    win:setWidth(m.W)
    win:setHeight(m.H)
    put(win.closeB, m.W - P - m.R24, m.R12, m.R24, m.R24)
    win.closeB:forceImageSize(m.R24, m.R24)                 -- V:client/ISUI/ISInventoryPage.lua:1479
    win.packB.font, win.packB.fh = m.fSmall, m.ls
    for _, side in ipairs(SIDES) do
        local x0 = (side == "bear") and m.lx or m.rx
        local y = m.y1 + m.cardTop
        local rows = win.rows[side]
        for i = 1, ROWS do
            local r = rows[i]
            put(r, x0 + m.R4, y, m.CW - m.R8, m.rowH)
            local by = y + math.floor((m.rowH - m.btnH) / 2)
            local bx2 = x0 + m.CW - m.R6 - m.b2W
            put(r.b2, bx2, by, m.b2W, m.btnH)
            put(r.b1, bx2 - m.R4 - m.b1W, by, m.b1W, m.btnH)
            r.b1.font, r.b1.fh, r.b2.font, r.b2.fh = m.fSmall, m.ls, m.fSmall, m.ls
            y = y + m.rowH
        end
        local py = m.y1 + m.cardTop + ROWS * m.rowH + m.R8
        local cx = x0 + math.floor(m.CW / 2)
        local pw = math.max(tw(m.fSmall, statics().widePage), m.R40)
        put(win.prev[side], cx - math.floor(pw / 2) - m.R6 - m.R24, py, m.R24, m.pgH)
        put(win.next[side], cx + math.floor(pw / 2) + m.R6, py, m.R24, m.pgH)
        win.prev[side].font, win.prev[side].fh = m.fBody, m.lb
        win.next[side].font, win.next[side].fh = m.fBody, m.lb
        m["pgX_" .. side] = cx
        m.pgY = py + math.floor((m.pgH - m.ls) / 2)
    end
    put(win.packB, m.W - P - m.putW, m.l3y + math.floor((m.lb - m.pbh) / 2), m.putW, m.pbh)
end

local function clampPos(win)
    local m = win.m
    if not m then return end
    local sw, sh = screen()
    local keep = m.R40
    local x, y = win:getX(), win:getY()                     -- V:client/ISUI/ISLayoutManager.lua:55-56
    local nx = math.max(keep - m.W, math.min(x, sw - keep))
    local ny = math.max(0, math.min(y, sh - keep))
    if nx ~= x then win:setX(nx) end
    if ny ~= y then win:setY(ny) end
end

-- Faktor, Schriften, Masse; passt das Fenster nicht in 92 % der Bildhoehe, eine Stufe kleiner (wie U.WinLayout).
local function layout(win)
    local sw, sh = screen()
    local idx = sizeIdx()
    local f, k = 1, 1
    if U.MarkerFactor then f, k = U.MarkerFactor(sh, idx) end
    local m = nil
    for _ = 1, 8 do
        m = metrics(f, sw, sh, idx)
        if m.H <= FIT * sh or (k or 1) <= 1 or not U.MarkerFactor then break end
        f, k = U.MarkerFactor(sh, k)
    end
    win.m = m
    place(win, m)
    clampPos(win)
end

-- ---------------------------------------------------------------------------
-- Modell (hoechstens 1 x je Sekunde und bei neuer Liste / Seite / Klick)
-- ---------------------------------------------------------------------------

-- Text auf Breite kuerzen ("..." am Ende). Nur beim Modell-Bau, hoechstens 2 x ROWS Namen.
local function fit(font, s, maxW)
    if tw(font, s) <= maxW then return s end
    local n = string.len(s)
    while n > 1 do
        n = n - 1
        local t = string.sub(s, 1, n) .. "..."
        if tw(font, t) <= maxW then return t end
    end
    return "..."
end

-- Nachbesserung F4 (Befund P5): "Name<extra> (Anzahl)" -- gekuerzt wird nur der NAME, Zustand und Anzahl bleiben immer sichtbar (Form der Sprache
-- aus UI_BN_Bear_Inv_Many, auch wenn sie die Anzahl vorne hat).
local function fitLabel(font, name, extra, k, maxW)
    local function make(n)
        local t = n .. extra
        if k > 1 then t = U.T("UI_BN_Bear_Inv_Many", t, k) end
        return t
    end
    local full = make(name)
    if tw(font, full) <= maxW then return full end
    return make(fit(font, name, maxW - tw(font, make(""))))
end

local function btnOf(label, why, tip)
    local e = { label = label, state = "normal" }
    if why then
        e.state = "off"
        e.tip = TIP_HEAD .. label .. TIP_BODY .. why
    else
        e.tip = TIP_HEAD .. label .. TIP_BODY .. (tip or "")
    end
    return e
end

-- Tooltip einer Zeile des Baeren aus den Feldern des Schreibers (f4/schnittstelle.md K4).
local function bearTip(s, r, name, bd)
    local t = TIP_HEAD .. name .. TIP_BODY
    if r.unk then return t .. s.unkTip end
    local kg = U.Kg(r.w)
    if r.k > 1 then
        t = t .. U.T("UI_BN_Bear_Inv_TipEach", kg, U.Kg(r.w * r.k))
    else
        t = t .. U.T("UI_BN_Bear_Inv_Kg", kg)
    end
    if r.cp then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Inv_TipCond", math.floor(r.cp + 0.5)) end
    if r.fr and s.fresh[r.fr] then t = t .. TIP_LINE .. s.fresh[r.fr] end
    if r.ck then t = t .. TIP_LINE .. s.cooked end
    if r.bu then t = t .. TIP_LINE .. s.burnt end
    if r.fz then t = t .. TIP_LINE .. s.frozen end
    if r.fl and r.fl > 0 then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Inv_TipFluid", U.Kg(r.fl), U.FluidName(r.fn)) end
    if r.u then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Inv_TipUses", math.floor(r.u + 0.5)) end
    if r.fv then t = t .. TIP_LINE .. s.fav end
    -- Nachbesserung F4 (Befund P3): nur, was der Kern wirklich frisst -- nie verdorben (fr 2), nie verbrannt (S:server/BanditsNPCBearInv.lua
    -- B.InvEatStep); Text je Koerper (P10)
    if r.ea and r.fr ~= 2 and not r.bu then t = t .. TIP_LINE .. U.TB("UI_BN_Bear_Inv_TipFood", bd) end
    return t
end

-- Seite klemmen: 1 .. Seiten (mindestens 1).
local function pages(n)
    local p = math.floor((n + ROWS - 1) / ROWS)
    if p < 1 then p = 1 end
    return p
end

local function clampPage(pg, n)
    local p = pages(n)
    pg = math.floor(tonumber(pg) or 1)
    if pg < 1 then pg = 1 end
    if pg > p then pg = p end
    return pg, p
end

-- Spalte "Your bear": Zeilen der fertigen Liste auf dieser Seite.
local function bearSide(win, d, m, s, v, e, whyAll)
    local rows = (e and e.rows) or {}
    local pg, pn = clampPage(win.page.bear, #rows)
    win.page.bear = pg
    d.pg.bear, d.pn.bear = pg, pn
    local nameW = m.CW - m.R8 - (m.R4 + m.icon + m.R6) - m.R8 - m.kgW - m.R8 - m.b1W - m.R4 - m.b2W - m.R6
    local out = {}
    for i = 1, ROWS do
        local r = rows[(pg - 1) * ROWS + i]
        if r then
            local name = r.nm or U.ItemName(r.t)
            if r.unk then name = s.unknown end
            -- P6: gibt es den Namen mehrfach (U.InvSortRows setzt dup), steht der Zustand in der Zeile ("T-Shirt 70%")
            local extra = ""
            if r.dup and r.cp and not r.unk then extra = " " .. string.format("%d", math.floor(r.cp + 0.5)) .. "%" end
            local why = whyAll
            if not why and r.unk then why = s.unkTip end
            local x = { name = fitLabel(m.fBody, name, extra, r.k, nameW), kg = U.T("UI_BN_Bear_Inv_Kg", U.Kg(r.w * r.k)), dim = r.unk,
                tip = bearTip(s, r, name, v.bd), ref = r, tex = (not r.unk) and U.ItemIcon(r.t) or nil, rot = (r.fr == 2) }
            x.b1 = btnOf(s.take, why, s.takeTip)
            if r.k > 1 then x.b2 = btnOf(s.all, why, U.T("UI_BN_Bear_Inv_AllTake", r.k) .. TIP_LINE .. s.allTakeTip) end
            out[i] = x
        end
    end
    d.rows.bear = out
    if e == nil then
        local st = U.InvAskState(getSpecificPlayer(0), v.id)   -- V:client/Farming/CFarmingSystem.lua:45
        d.info.bear = (st == "none") and s.none or s.wait
    elseif #rows == 0 then
        d.info.bear = s.empty
    end
end

-- Spalte "You": eigene Gruppen auf dieser Seite.
local function youSide(win, d, m, s, v, player, whyAll)
    local groups = U.InvMine(player)
    local pg, pn = clampPage(win.page.you, #groups)
    win.page.you = pg
    d.pg.you, d.pn.you = pg, pn
    local nameW = m.CW - m.R8 - (m.R4 + m.icon + m.R6) - m.R8 - m.kgW - m.R8 - m.b1W - m.R4 - m.b2W - m.R6
    local out = {}
    for i = 1, ROWS do
        local g = groups[(pg - 1) * ROWS + i]
        if g then
            local n = #g.items
            local why, many = whyAll, 0
            if not why then why, many = U.InvGiveWhy(v, g) end
            local tip = TIP_HEAD .. g.name .. TIP_BODY
            if n > 1 then
                tip = tip .. U.T("UI_BN_Bear_Inv_TipEach", U.Kg(g.w), U.Kg(g.kg))
            else
                tip = tip .. U.T("UI_BN_Bear_Inv_Kg", U.Kg(g.w))
            end
            if g.fav then tip = tip .. TIP_LINE .. s.fav end
            if g.worn then tip = tip .. TIP_LINE .. s.wornTip end
            local x = { name = fitLabel(m.fBody, g.name, "", n, nameW), kg = U.T("UI_BN_Bear_Inv_Kg", U.Kg(g.kg)), dim = (why ~= nil), tip = tip,
                ref = g, tex = g.tex }
            x.b1 = btnOf(s.give, why, s.giveTip)
            if n > 1 then
                local w2 = why
                if not w2 and many < 1 then w2 = s.allGiveTip end      -- P9: alle Stuecke Favorit / ausgeruestet -> All grau mit Grund
                x.b2 = btnOf(s.all, w2, U.T("UI_BN_Bear_Inv_AllGive", math.max(many, 0)) .. TIP_LINE .. s.allGiveTip)
            end
            out[i] = x
        end
    end
    d.rows.you = out
    if #groups == 0 then d.info.you = s.youEmpty end
    d.mineMore = groups.more == true                             -- P12: Deckel der Gruppen gegriffen
end

-- Kopf: Load-Zeile, Zaehler, Packtaschen.
local function headModel(d, s, v, e, player)
    local bd = v.bd
    d.title = U.T("UI_BN_Bear_Inv_Title", U.CubName and U.CubName(v) or "?")
    d.bearTitle = U.TB("UI_BN_Bear_Inv_Bear", bd)
    local w, c = tonumber(v.ivW), tonumber(v.ivC)
    if (w == nil or c == nil) and e then w, c = e.load, e.cap end
    d.loadVal = "--"
    if w ~= nil and c ~= nil then
        d.loadVal = U.T("UI_BN_Bear_Win_LoadVal", U.Kg(w), math.floor(c + 0.5))
        local frac = 0
        if c > 0 then frac = w / c end
        if frac > 1 then frac = 1 end
        if frac < 0 then frac = 0 end
        d.loadFrac = frac
        if U.WinRamp then d.lr, d.lg, d.lb = U.WinRamp("load", frac) end     -- P2: gruen, fast voll orange; ueber der Grenze rot (prerender)
    end
    d.over = v.ivX == true or (e ~= nil and e.over == true)
    local k = tonumber(v.ivK)
    if k == nil and e then k = e.cnt end
    d.things = (k ~= nil) and U.T("UI_BN_Bear_Inv_Things", math.floor(k), math.floor(cfgNum("invMaxItems", 1000))) or ""
    d.thingsFull = (k ~= nil) and k >= cfgNum("invMaxItems", 1000)        -- P7
    local on = v.bag == true
    if on then
        d.packs = U.T("UI_BN_Bear_Win_LoadPacks", math.floor(cfgNum("bagAdd", 150) + 0.5))
        d.packB = btnOf(s.takeOff, U.InvPacksWhy(player, v, false), s.takeOffTip)
        d.packB.kind = "off"
    else
        d.packs = s.noPacks
        d.packB = btnOf(s.putOn, U.InvPacksWhy(player, v, true), s.putOnTip)
        d.packB.kind = "on"
    end
end

-- Eigenen Baeren mit dieser Kennung aus der Sicht (U.WinBears: gezaehmt oder vermisst, gehoert mir) oder nil.
local function myBear(id)
    if not U.WinBears then return nil end
    local list = U.WinBears()
    for i = 1, #list do
        if list[i].id == id then return list[i] end
    end
    return nil
end

-- Liste anfordern, wenn noetig: keine fertige Liste, neue Fassung in der Sicht, Keep-alive faellig, oder lange "No answer".
local function askIfNeeded(win, player, v, now)
    local have = U.InvListR(v.id)
    local st = U.InvAskState(player, v.id)
    local stale = have == nil or (isNum(v.ivR) and v.ivR ~= have)
    local keep = now - (win.askAt or 0) >= cfgNum("invKeepMs", 30000) or now < (win.askAt or 0)
    if st == "none" and now - (win.askAt or 0) >= NONE_AGAIN_MS then
        U.InvAskReset(v.id)
        st = nil
    end
    if (stale and st == nil) or (keep and st ~= "wait") then
        if U.InvAsk(player, v.id) then win.askAt = now end
    end
end

function Inv:refresh(now)
    self.dirty = false
    self.modelAt = now
    local player = getSpecificPlayer(0)                     -- V:client/Farming/CFarmingSystem.lua:45
    if not player or player:isDead() then                   -- V:client/ISUI/ISUIHandler.lua:42
        U.InvClose()
        return false
    end
    local v = myBear(self.id)
    if v == nil then
        U.InvClose()
        return false
    end
    self.v = v
    askIfNeeded(self, player, v, now)
    local m = self.m
    local sw, sh = screen()
    if not m or m.sw ~= sw or m.sh ~= sh or m.idx ~= sizeIdx() then
        layout(self)
        m = self.m
    end
    local s = statics()
    local e = U.InvList(v.id)
    local d = { rows = {}, info = {}, pg = {}, pn = {}, pgTxt = {} }
    headModel(d, s, v, e, player)
    local whyAll = U.InvWhy(player, v)
    bearSide(self, d, m, s, v, e, whyAll)
    youSide(self, d, m, s, v, player, whyAll)
    if whyAll then
        d.footer, d.footerCol = whyAll, "warn"
    elseif d.over then
        d.footer, d.footerCol = s.over, "warn"
    elseif d.thingsFull then
        d.footer, d.footerCol = U.TB("UI_BN_Bear_Why_InvCap", v.bd, math.floor(cfgNum("invMaxItems", 1000))), "warn"     -- P7
    elseif d.mineMore then
        d.footer = U.T("UI_BN_Bear_Inv_MineMore", 1000)                                                            -- P12
    else
        d.footer = s.hint
    end
    self.model = d
    -- Kinder: Texte, Zustaende, Tooltips; Knoepfe ohne Zeile verschwinden (nur bei einem Wechsel; offenen Tooltip vorher abmelden)
    for _, side in ipairs(SIDES) do
        local rows = self.rows[side]
        for i = 1, ROWS do
            local r = rows[i]
            local x = d.rows[side][i]
            r.tooltip = x and x.tip or nil
            U.InvSetBtn(r.b1, x and x.b1)
            U.InvSetBtn(r.b2, x and x.b2)
        end
        self.prev[side].state = (d.pg[side] > 1) and "normal" or "off"
        self.next[side].state = (d.pg[side] < d.pn[side]) and "normal" or "off"
        self.prev[side].enable = self.prev[side].state ~= "off"     -- ISButton.lua:45
        self.next[side].enable = self.next[side].state ~= "off"
        if d.pn[side] > 1 then d.pgTxt[side] = U.T("UI_BN_Bear_Win_Count", d.pg[side], d.pn[side]) end
    end
    local pb = self.packB
    pb.label, pb.state, pb.tooltip, pb.kind = d.packB.label, d.packB.state, d.packB.tip, d.packB.kind
    pb.enable = (pb.state ~= "off")
    return true
end

-- Offenen Tooltip EINES Kindes abmelden (V:client/ISUI/ISButton.lua:341-343), wie das Baeren-Fenster.
local function hideTip(el)
    local tip = el and el.tooltipUI
    if tip and tip:getIsVisible() then
        tip:setVisible(false)
        tip:removeFromUIManager()
    end
end

-- Knopf einer Zeile setzen: e = nil -> unsichtbar (ISButton:setVisible V:client/ISUI/ISButton.lua:9, getIsVisible :34).
function U.InvSetBtn(b, e)
    if e then
        b.label, b.state, b.tooltip = e.label, e.state, e.tip
        b.enable = (e.state ~= "off")                       -- ISButton.lua:45
    end
    local show = (e ~= nil)
    if b:getIsVisible() ~= show then
        if not show then hideTip(b) end
        b:setVisible(show)
    end
end

-- ---------------------------------------------------------------------------
-- Zeile (von ISButton, wie U.WinRow: Tooltip ohne Klick)
-- ---------------------------------------------------------------------------
local Row = ISButton:derive("BanditsNPCBearInvRow")

function Row:prerender()
    local win = self.win
    local m = win and win.m
    local d = win and win.model
    local x = d and d.rows[self.side] and d.rows[self.side][self.idx]
    if m and x then
        if self.mouseOver then U.WinRect(self, 0, 0, self.width, self.height, col("rowHover")) end
        local iy = math.floor((self.height - m.icon) / 2)
        if x.tex then
            self:drawTextureScaledAspect(x.tex, m.R4, iy, m.icon, m.icon, x.dim and 0.45 or 1, 1, 1, 1)    -- V:client/ISUI/ISButton.lua:226
        else
            U.WinRect(self, m.R4, iy, m.icon, m.icon, col("pipEmpty"))
            U.WinFrame(self, m.R4, iy, m.icon, m.icon, m.t, col("pipEdge"))
        end
        local c = col("text")
        if x.dim then c = col("btnOffText") end
        if x.rot then c = col("warn") end
        local ty = math.floor((self.height - m.lb) / 2)
        self:drawText(x.name or "", m.R4 + m.icon + m.R6, ty, c[1], c[2], c[3], c[4], m.fBody)
        local c2 = col("text2")
        local right = self.width - (m.R6 + m.b2W + m.R4 + m.b1W) - m.R8 + m.R4
        self:drawTextRight(x.kg or "", right, math.floor((self.height - m.ls) / 2), c2[1], c2[2], c2[3], c2[4], m.fSmall)
    end
    ISButton.updateTooltip(self)                            -- ISButton.lua:176, :316-346
end

function Row:render()
end

-- ---------------------------------------------------------------------------
-- Das Fenster
-- ---------------------------------------------------------------------------
function Inv:new(x, y, w, h)
    local o = ISPanel:new(x, y, w, h)                       -- ISAdminTicketsUI.lua:243-253
    setmetatable(o, self)
    self.__index = self
    o.moveWithMouse = true
    o.background = false                                    -- V:client/ISUI/ISPanel.lua:9-11
    o:setWantKeyEvents(true)                                -- V:client/ISUI/Crafting/ISHandcraftWindow.lua:386
    o.dirty = true
    o.modelAt = 0
    o.page = { bear = 1, you = 1 }
    o.isOpen = false
    return o
end

local function kid(win, cls, cmd, style)
    local b = cls:new(0, 0, 10, 10, "", win, Inv.onCmd)     -- V:client/ISUI/ISCollapsableWindow.lua:55-61
    b:initialise()
    b.win, b.cmd, b.style, b.state = win, cmd, style, "normal"
    win:addChild(b)
    win.kids[#win.kids + 1] = b
    return b
end

function Inv:build()
    self.kids = {}
    self.rows, self.prev, self.next = {}, {}, {}
    for _, side in ipairs(SIDES) do
        local list = {}
        for i = 1, ROWS do
            local r = kid(self, Row, nil)
            r.side, r.idx = side, i
            r.onclick = nil                                 -- Zeilen klicken nicht (ISButton.lua:42-44)
            r.b1 = kid(self, U.WinBtn, side == "bear" and "take1" or "give1", "cmd")
            r.b2 = kid(self, U.WinBtn, side == "bear" and "takeAll" or "giveAll", "cmd")
            r.b1.side, r.b1.idx, r.b2.side, r.b2.idx = side, i, side, i
            list[i] = r
        end
        self.rows[side] = list
        self.prev[side] = kid(self, U.WinBtn, "prev", "small")
        self.next[side] = kid(self, U.WinBtn, "next", "small")
        self.prev[side].label, self.next[side].label = "<", ">"
        self.prev[side].side, self.next[side].side = side, side
    end
    self.packB = kid(self, U.WinBtn, "packs", "cmd")
    local c = ISButton:new(0, 0, 10, 10, "", self, Inv.onClose)
    c:initialise()
    c.borderColor.a = 0.0                                   -- ISCollapsableWindow.lua:57
    local bg, hv = col("closeBg"), col("closeHover")
    c.backgroundColor = { r = bg[1], g = bg[2], b = bg[3], a = bg[4] }
    c.backgroundColorMouseOver = { r = hv[1], g = hv[2], b = hv[3], a = hv[4] }
    if W.close then c:setImage(W.close) end                 -- ISCollapsableWindow.lua:60
    self:addChild(c)
    self.kids[#self.kids + 1] = c
    self.closeB = c
end

-- Klick (ISButton ruft onclick(Ziel, Knopf), V:client/ISUI/ISButton.lua:47): nur Zeitaktionen anstellen bzw. blaettern.
function Inv:onCmd(button)
    if not button or button.state == "off" then return end
    local player = getSpecificPlayer(0)
    local d, v = self.model, self.v
    if not player or not d or not v then return end
    local cmd = button.cmd
    if cmd == "prev" or cmd == "next" then
        -- P6: Umschalt + Pfeil = zehn Seiten (isShiftKeyDown: V:client/ISUI/ISInventoryPane.lua:1163); das Modell klemmt die Seite
        local step = isShiftKeyDown() and 10 or 1
        self:flip(button.side, (cmd == "next") and step or -step)
    elseif cmd == "packs" then
        if button.kind == "off" then U.InvPacksOff(player, v) else U.InvPacksOn(player, v, false) end
    else
        local x = d.rows[button.side] and d.rows[button.side][button.idx]
        if not x then return end
        if cmd == "take1" then
            U.InvTake(player, v, x.ref, 1)
        elseif cmd == "takeAll" then
            U.InvTake(player, v, x.ref, x.ref.k)
        elseif cmd == "give1" then
            U.InvGive(player, v, x.ref, false)
        elseif cmd == "giveAll" then
            U.InvGive(player, v, x.ref, true)
        end
    end
    self.dirty = true
end

function Inv:onClose()
    U.InvClose()
end

-- Zeichnen je Bild: nur Rechtecke und fertige Texte (Belege der Zeichen-Aufrufe: client/ISUI/BanditsNPCBearWinParts.lua Kopf).
local function card(self, m, x, title, info)
    U.WinRect(self, x, m.y1, m.CW, m.cardH, col("cardBg"))
    U.WinFrame(self, x, m.y1, m.CW, m.cardH, m.t, col("cardBorder"))
    local c = col("title")
    self:drawText(title or "", x + m.R12, m.y1 + m.R10, c[1], c[2], c[3], c[4], m.fBody)
    if info then
        c = col("dim")
        self:drawTextCentre(info, x + math.floor(m.CW / 2), m.y1 + m.cardTop + 2 * m.rowH, c[1], c[2], c[3], c[4], m.fBody)
    end
end

function Inv:prerender()
    local now = getTimestampMs()                            -- V:client/Foraging/ISBaseIcon.lua:485
    if self.dirty or now - self.modelAt >= MODEL_MS or now < self.modelAt then
        if not self:refresh(now) then return end
    end
    local m, d = self.m, self.model
    if not m or not d then return end
    local P = m.P
    U.WinRect(self, 0, 0, m.W, m.H, col("winBg"))
    U.WinFrame(self, 0, 0, m.W, m.H, m.t, col("winBorder"))
    U.WinRect(self, 0, 0, m.W, m.R3, col("accent"))
    local c = col("name")
    self:drawText(d.title or "", P, m.ty, c[1], c[2], c[3], c[4], m.fName)
    self:drawText(d.title or "", P + m.bold, m.ty, c[1], c[2], c[3], c[4], m.fName)        -- zweimal = "fett"
    -- Load: Etikett, Balken, Wert; rechts der Zaehler
    c = col("text2")
    self:drawText(statics().load, P, m.l2y, c[1], c[2], c[3], c[4], m.fBody)
    local by = m.l2y + math.floor((m.lb - m.barH) / 2)
    U.WinRect(self, m.barX, by, m.barW, m.barH, col("track"))
    if d.loadFrac then
        local fill = math.floor(m.barW * d.loadFrac + 0.5)
        if fill > 0 then
            if d.over then
                local w = col("over")                               -- P2: ueber der Grenze kraeftig rot
                self:drawRect(m.barX, by, fill, m.barH, 1, w[1], w[2], w[3])
            else
                self:drawRect(m.barX, by, fill, m.barH, 1, d.lr or 1, d.lg or 1, d.lb or 1)
            end
        end
    end
    U.WinFrame(self, m.barX, by, m.barW, m.barH, m.t, col("trackBorder"))
    c = col(d.over and "over" or "text")
    self:drawText(d.loadVal or "--", m.barX + m.barW + m.R12, m.l2y, c[1], c[2], c[3], c[4], m.fBody)
    c = col(d.thingsFull and "warn" or "text2")                 -- P7
    self:drawTextRight(d.things or "", m.W - P, m.l2y, c[1], c[2], c[3], c[4], m.fBody)
    c = col("text")
    self:drawText(d.packs or "", P, m.l3y, c[1], c[2], c[3], c[4], m.fBody)
    U.WinRect(self, P, m.headH, m.W - 2 * P, m.t, col("divider"))
    card(self, m, m.lx, d.bearTitle, d.info.bear)
    card(self, m, m.rx, statics().you, d.info.you)
    c = col("text2")
    for _, side in ipairs(SIDES) do
        if d.pgTxt[side] then
            self:drawTextCentre(d.pgTxt[side], m["pgX_" .. side], m.pgY, c[1], c[2], c[3], c[4], m.fSmall)
        end
    end
    c = col(d.footerCol or "dim")
    self:drawText(d.footer or "", P, m.y3, c[1], c[2], c[3], c[4], m.fSmall)
end

-- Nachbesserung F4 (Befund P6): blaettern. step > 0 = weiter; die Seite klemmt das Modell (clampPage). Mausrad: eine Seite je Raste ueber der Spalte
-- unter der Maus (onMouseWheel(del), del > 0 = weiter: V:client/ISUI/ISScrollingListBox.lua:347-353; getMouseX: V:client/ISUI/ISInventoryPage.lua:1303).
-- Die Zeilen fangen das Rad selbst (Row:onMouseWheel), ueber Knoepfen und leerer Flaeche das Fenster.
function Inv:flip(side, step)
    if side ~= "bear" and side ~= "you" then return false end
    self.page[side] = (self.page[side] or 1) + step
    self.dirty = true
    return true
end

function Inv:onMouseWheel(del)
    local m = self.m
    if not m then return false end
    local side = (self:getMouseX() < m.rx) and "bear" or "you"
    return self:flip(side, (del > 0) and 1 or -1)
end

function Row:onMouseWheel(del)
    local win = self.win
    if not win or not win.flip then return false end
    return win:flip(self.side, (del > 0) and 1 or -1)
end

-- Esc schliesst (V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-297); nicht, solange der Chat tippt (ISChat.focused, V:client/Chat/ISChat.lua:8).
function Inv:isKeyConsumed(key)
    if ISChat and ISChat.focused then return false end
    return key == Keyboard.KEY_ESCAPE
end

function Inv:onKeyRelease(key)
    if ISChat and ISChat.focused then return end
    if self:isVisible() and key == Keyboard.KEY_ESCAPE then U.InvClose() end
end

-- Lage merken: nur x / y (V:client/ISUI/ISLayoutManager.lua:6-13, :103, :111; wie client/ISUI/BanditsNPCBearWindow.lua).
function Inv:SaveLayout(_name, layout)
    layout.x = self:getX()
    layout.y = self:getY()
    layout.visible, layout.width, layout.height = nil, nil, nil
end

function Inv:RestoreLayout(_name, layout)
    local x = tonumber(layout.x)                            -- ISLayoutManager.lua:17-18
    local y = tonumber(layout.y)
    if x ~= nil and y ~= nil then
        self:setX(x)
        self:setY(y)
        clampPos(self)
    end
end

-- ---------------------------------------------------------------------------
-- Oeffnen / Schliessen
-- ---------------------------------------------------------------------------

-- Neue Liste angekommen (B.OnInv, client/BanditsNPCBearInvClient.lua): Modell im naechsten Bild neu.
function U.InvOnList(id)
    local win = W.win
    if win and win.isOpen and win.id == id then win.dirty = true end
end

-- Inventar-Fenster eines eigenen Baeren oeffnen (Knopf "Inventory" im Baeren-Fenster, Rechtsklick "Open its inventory"). Ansehen geht
-- immer -- auch von weitem, vermisst oder mitfahrend (Kevin Antwort 2). Rueckgabe true = offen.
function U.InvOpen(player, id)
    player = player or getSpecificPlayer(0)
    if not player or id == nil then return false end
    if myBear(id) == nil then
        HaloTextHelper.addText(player, U.T("UI_BN_Bear_Win_NoBear"))     -- V:client/Foraging/forageClient.lua:73
        return false
    end
    local win = W.win
    local first = (win == nil)
    if first then
        W.close = getTexture(CLOSE_FILE)                    -- V:client/Chat/ISChat.lua:137; Bild ISCollapsableWindow.lua:386
        win = Inv:new(0, 0, 860, 600)
        win:initialise()                                    -- V:client/ISUI/Animal/ISAnimalContextMenu.lua:746
        win:build()
        W.win = win
    end
    if win.id ~= id then win.page = { bear = 1, you = 1 } end
    win.id = id
    win.dirty = true
    win.askAt = nil
    U.InvAskReset(id)
    layout(win)
    if not win:refresh(getTimestampMs()) then return false end
    if first then
        local sw, sh = screen()
        local m = win.m
        win:setX(math.floor((sw - m.W) * 0.30))
        win:setY(math.floor((sh - m.H) * 0.35))
        ISLayoutManager.RegisterWindow(LAYOUT_NAME, Inv, win)  -- V:client/ISUI/ISLayoutManager.lua:12
        clampPos(win)
    end
    win.isOpen = true
    win:addToUIManager()                                    -- V:client/ISUI/ISUIElement.lua:1365
    win:setVisible(true)                                    -- :657
    win:bringToTop()                                        -- :1548
    return true
end

function U.InvClose()
    local win = W.win
    if not win then return end
    win.isOpen = false
    if win.kids then
        for i = 1, #win.kids do hideTip(win.kids[i]) end
    end
    win:setVisible(false)                                   -- V:client/ISUI/Crafting/ISHandcraftWindow.lua:295-296
    win:removeFromUIManager()
end

function U.InvIsOpen()
    return W.win ~= nil and W.win.isOpen == true
end

local function onGameStart()
    if W.win then U.InvClose() end
    W.win = nil
    ST = nil
end

local function onResolution()
    if W.win then layout(W.win) end
end

Events.OnGameStart.Add(onGameStart)                         -- V:client/Chat/ISChat.lua:1186
Events.OnResolutionChange.Add(onResolution)                 -- V:client/ISUI/PlayerData/ISPlayerData.lua:206
