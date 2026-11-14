--
-- NPC Crew -- Baer, Reiter "Talente" im Baeren-Fenster: Kacheln, Karte, Ja/Nein-Fenster (Lauf baer-talente, PLAN_TALENTE.md 5; Kevins Antworten
-- 14.11.2026 ~10:20, baer/begleiter/ENTSCHEIDUNGEN.md -- gehen vor: FREIE WAHL, 9 Kacheln in 3 x 3, 3 Punkte frei verteilbar).
--
-- Kevin 14.11.2026: "per knopf altivieten dann leuchtet der skill hell und ist permanent altiv" -- "skills vergeben muss bestaetigt werden beim
-- klicken" -- Icons "recht gut sichtbar ... wie in anderen spielen wo man skills vergeben kann", "hochaufloesend und huebsch".
--
-- Aufbau (Fenster-Masse m aus client/ISUI/BanditsNPCBearWindow.lua, alles x f): EINE Karte "Perks" ueber die ganze Breite und dieselbe Hoehe wie
-- die drei Karten + Befehle des Uebersicht-Reiters (beide Reiter gleich hoch: nichts springt beim Wechsel). Kopfzeile Titel + rechts "1 perk
-- point(s) free - 2 of 3 used"; darunter 3 x 3 Kacheln in der Reihenfolge B.TALENTS; Fusszeile links der Hinweis, rechts Knopf "Reset" mit
-- kleinem Grund davor ("off (sandbox)" / "in 14 hours").
-- Kachel (U.WinTalent, von Vanillas ISButton abgeleitet wie U.WinRow -- Klick nur bei enable, Tooltip auch grau, V:client/ISUI/ISButton.lua:18-23,
-- :45, :316-346): oben links der Zustand klein, mittig das Symbol 56 x f (bis 64 px die 64er-Bilder, darueber die 128er), darunter Name und
-- kurze Wirkung. Zustaende:
--   aktiv          warmer Grund, Rahmen accent doppelt, goldener Hof hinter dem Symbol (Leuchten, eine Welle je talGlowMs), Symbol _on, Name gold
--   waehlbar       Knopf-Grund, Honigrahmen, Symbol voll hell (Nachbesserung P3: nicht mehr 0,8 gedimmt -- sonst so dunkel wie gesperrt);
--                  Maus darueber: Grund heller, Rahmen accent -- Klick oeffnet das Ja/Nein-Fenster
--   gesperrt       grauer Grund, Symbol _off (grau) + Schloss unten rechts
--   kommt spaeter  wie gesperrt, Sanduhr statt Schloss (Angler bis F5)
-- Je Bild NUR Rechtecke, Bilder und fertige Texte (Modell U.TalentModel im 1-s-Takt, Masse beim Legen); einzig die Helligkeit des Hofs wird je
-- Bild gerechnet (math.sin wie V:client/ISUI/ISEquippedItem.lua:391).
-- Bestaetigung (Kevin E:815): Vanillas ISModalDialog mit Ja/Nein -- Form V:client/ISUI/ISWorldObjectContextMenu.lua:953 (x 0, y 0 = an der Maus,
-- Breite/Hoehe, Text, yesno true, Ziel, Rueckruf, Spieler 0, zwei Werte), initialise + addToUIManager V:client/ISUI/Animal/ISAnimalContextMenu.lua:
-- 1085-1086; Rueckruf onclick(Ziel, Knopf, Wert1, Wert2) V:client/ISUI/ISModalDialog.lua:58-63, Ja = button.internal == "YES"
-- (V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:219). Erst nach "Ja" geht GENAU EINE Bitte an den Schreiber (B.Ask "Talent" { id, k } bzw.
-- "TalentReset" { id }, tal/schnittstelle.md K4) -- der prueft alles noch einmal (Besitz, Punkte, Hoechstzahl) und glaubt keine Zahl. Hoechstens
-- ein offenes Fenster. Nebenwirkung Vanilla: ISModalDialog:destroy setzt im Spiel das Tempo auf 1 (ISModalDialog.lua:47-49) -- wie beim Schlafen.
-- Zeichen-Aufrufe wie client/ISUI/BanditsNPCBearWinParts.lua (Belege dort): drawRect / drawRectBorder (ueber U.WinRect / U.WinFrame), drawText /
-- drawTextRight / drawTextCentre, drawTextureScaled(tex, x, y, w, h, a, r, g, b) V:client/ISUI/ISUIElement.lua:1032 (V:client/Chat/ISChat.lua:418).
-- getTexture("media/textures/...png") V:client/Chat/ISChat.lua:424. Kein Engine-Aufruf ohne Vanilla-Fundstelle. Statisch geprueft, nicht gespielt.
--

require "ISUI/ISButton"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local TEX_DIR = "media/textures/BanditsNPCBear_Talent_"
local SMALL_MAX = 64            -- bis zu dieser Zeichengroesse (px) die 64er-Bilder, darueber die 128er (Nachbesserung P8: nie hochskaliert,
                                -- 1,25 x = 70 px kommt aus der 128er; vorher 80 = 70 aus 64)
local GLOW_K = 1.5              -- Hof = 1,5 x Symbol (weich auslaufend, sichtbar etwa bis 1,3 x)
local GLOW_MS = 2000            -- Rueckfall fuer B.CFG.talGlowMs

local T = { tex = nil, dlg = nil }

local function col(key)
    local c = U.WIN_COL and U.WIN_COL[key]
    return c or { 1, 1, 1, 1 }
end

local function tw(font, s)
    if s == nil or s == "" then return 0 end
    return getTextManager():MeasureStringX(font, s)    -- V:client/ISUI/ISButton.lua:450
end

-- Bilder einmal je Spielstart: je Talent normal / _on / _off in 64 und 128, Hof, Schloss, Sanduhr. getTexture: V:client/Chat/ISChat.lua:424.
local function textures()
    if T.tex then return T.tex end
    local t = { k = {} }
    local list = B.TALENTS
    if type(list) == "table" then
        for i = 1, #list do
            local k = list[i]
            local e = {}
            for _, st in ipairs({ "", "_on", "_off" }) do
                e[st .. "64"] = getTexture(TEX_DIR .. k .. st .. "_64.png")
                e[st .. "128"] = getTexture(TEX_DIR .. k .. st .. "_128.png")
            end
            t.k[k] = e
        end
    end
    t.glow64, t.glow128 = getTexture(TEX_DIR .. "glow_64.png"), getTexture(TEX_DIR .. "glow_128.png")
    t.lock32, t.lock64 = getTexture(TEX_DIR .. "lock_32.png"), getTexture(TEX_DIR .. "lock_64.png")
    t.soon32, t.soon64 = getTexture(TEX_DIR .. "soon_32.png"), getTexture(TEX_DIR .. "soon_64.png")
    T.tex = t
    return t
end

-- ---------------------------------------------------------------------------
-- Masse (aus client/ISUI/BanditsNPCBearWindow.lua metrics, nur beim Legen)
-- ---------------------------------------------------------------------------
-- Breite, die der Reiter braucht (Kacheln mit dem breitesten Namen / der breitesten Wirkung, Kopfzeile, Fusszeile, Reiterleiste).
function U.TalentNeedW(m)
    local s = U.TalentStatics and U.TalentStatics()
    if not s then return 0 end
    local R = function(v) return math.floor(v * m.f + 0.5) end
    local tile = R(56) + 2 * R(16)
    for i = 1, #s.keys do
        local k = s.keys[i]
        tile = math.max(tile, tw(m.fBody, s.name[k]) + 2 * R(8), tw(m.fSmall, s.short[k]) + 2 * R(8))
    end
    local need = 2 * m.P + 2 * R(12) + 3 * tile + 2 * R(8)
    local head = 2 * m.P + 2 * R(12) + tw(m.fBody, s.tabTal) + R(24) + math.max(tw(m.fSmall, s.widePoints), tw(m.fSmall, s.pointsAll))
    local hint = math.max(tw(m.fSmall, s.hintFree), tw(m.fSmall, s.hintDone), tw(m.fSmall, s.hintWait), tw(m.fSmall, s.wideNext))
    local note = math.max(tw(m.fSmall, s.resetOff), tw(m.fSmall, s.wideWait))
    local foot = 2 * m.P + 2 * R(12) + hint + R(16) + note + R(10) + tw(m.fBody, s.reset) + R(24)
    m.tabW = math.max(tw(m.fBody, s.tabMain) + R(24), tw(m.fBody, s.tabTal) + R(24) + R(6) + R(20))
    local tabs = 2 * m.P + 2 * m.tabW + R(6)
    return math.max(need, head, foot, tabs)
end

-- Lage der Karte und der Kacheln (nach der Breite W). Braucht der Reiter mehr Hoehe als Karten + Befehle, wird die Befehls-Karte so viel
-- hoeher (beide Reiter bleiben gleich hoch). Setzt m.tal* Felder; gibt nichts.
function U.TalentLayout(m)
    local s = U.TalentStatics and U.TalentStatics()
    local R = function(v) return math.floor(v * m.f + 0.5) end
    m.talX, m.talY, m.talW = m.P, m.y1, m.ow
    m.talIc = R(56)
    m.talSmall = (m.talIc <= SMALL_MAX)
    m.talBadge = R(22)
    m.talTileW = math.floor((m.talW - 2 * R(12) - 2 * R(8)) / 3)
    m.talGx = m.talX + R(12)
    m.talGy = m.talY + R(10) + m.lb + R(8)
    -- Zustand oben links neben dem Symbol: passt er nicht daneben, rutscht das Symbol unter ihn
    local stW = 0
    if s then
        for _, txt in pairs(s.st) do stW = math.max(stW, tw(m.fSmall, txt)) end
    end
    m.talStX, m.talStY = R(8), R(5)
    m.talIy = R(6)
    if R(8) + stW + R(4) > math.floor((m.talTileW - m.talIc) / 2) then m.talIy = R(5) + m.ls + R(2) end
    m.talNameY = m.talIy + m.talIc + R(4)
    m.talShortY = m.talNameY + m.lb + R(2)
    local tileNeed = m.talShortY + m.ls + R(8)
    local footH = R(8) + m.bh + R(10)
    local have = m.cardH + R(16) + m.ordH
    local th = math.floor((have - (m.talGy - m.talY) - 2 * R(8) - footH) / 3)
    if th < tileNeed then
        m.ordH = m.ordH + 3 * (tileNeed - th)
        th = tileNeed
    end
    m.talTileH = th
    m.talH = m.cardH + R(16) + m.ordH
    m.talFootY = m.talGy + 3 * th + 2 * R(8) + R(8)
    m.talResetW = tw(m.fBody, s and s.reset or "") + R(24)
end

local function put(el, x, y, w, h)
    el:setX(x)                                          -- V:client/ISUI/ISUIElement.lua:195-245 (wie BanditsNPCBearWindow.lua put)
    el:setY(y)
    el:setWidth(w)
    el:setHeight(h)
end

-- Kacheln, Reset-Knopf und Reiter-Knoepfe an ihre Stelle (aus BanditsNPCBearWindow.lua place).
function U.TalentPlace(win, m)
    if not win.talTiles then return end
    local R = function(v) return math.floor(v * m.f + 0.5) end
    for i = 1, #win.talTiles do
        local c = (i - 1) % 3
        local r = math.floor((i - 1) / 3)
        put(win.talTiles[i], m.talGx + c * (m.talTileW + R(8)), m.talGy + r * (m.talTileH + R(8)), m.talTileW, m.talTileH)
    end
    local rb = win.talReset
    put(rb, m.talX + m.talW - R(12) - m.talResetW, m.talFootY, m.talResetW, m.bh)
    rb.font, rb.fh = m.fBody, m.lb
    for i, tb in ipairs({ win.tabMainB, win.tabTalB }) do
        put(tb, m.P + (i - 1) * (m.tabW + R(6)), m.tabY, m.tabW, m.tabH)
        tb.font, tb.fh = m.fBody, m.lb
        tb.badgeW = R(20)
    end
end

-- Modell anwenden (1-s-Takt): Kachel-Felder, Tooltips, Klick nur bei "waehlbar"; Reset-Knopf; Reiter-Texte und Abzeichen.
function U.TalentApply(win, d)
    local t = d and d.tal
    if not t or not win.talTiles then return end
    local m = win.m
    for i = 1, #win.talTiles do
        local b = win.talTiles[i]
        local e = t.tiles[i]
        b.e = e
        b.k = e and e.k
        b.tooltip = e and e.tip
        b.enable = (e ~= nil and e.state == "free")     -- ISButton.lua:45 (Felder wie V:client/ISUI/Hutch/ISHutchUI.lua:617-623)
    end
    local r = t.reset
    win.talReset.label, win.talReset.state, win.talReset.tooltip = r.label, r.state, r.tip
    win.talReset.enable = (r.state ~= "off")
    local s = U.TalentStatics()
    win.tabMainB.label, win.tabTalB.label = s.tabMain, s.tabTal
    win.tabTalB.tooltip = s.tabTip
    win.tabTalB.badge = t.badge and string.format("%d", t.badge) or nil
    if m then
        win.tabMainB.labelW, win.tabTalB.labelW = tw(m.fBody, s.tabMain), tw(m.fBody, s.tabTal)
    end
    local tal = (win.tab == "tal")
    win.tabMainB.state = tal and "normal" or "active"
    win.tabTalB.state = tal and "active" or "normal"
end

-- Karte des Reiters (aus BanditsNPCBearWindow.lua prerender): Rahmen, Titel, Punkte, Fusszeile, kleiner Grund am Reset-Knopf.
function U.TalentDraw(el, m, d)
    local t = d and d.tal
    if not t or not m.talW then return end
    local R = function(v) return math.floor(v * m.f + 0.5) end
    local x, y, w, h = m.talX, m.talY, m.talW, m.talH
    U.WinRect(el, x, y, w, h, col("cardBg"))
    U.WinFrame(el, x, y, w, h, m.t, col("cardBorder"))
    local c = col("title")
    el:drawText(t.title or "", x + R(12), y + R(10), c[1], c[2], c[3], c[4], m.fBody)
    c = col((t.free or 0) > 0 and "honeyText" or "dim")
    el:drawTextRight(t.head or "", x + w - R(12), y + R(10) + m.lb - m.ls, c[1], c[2], c[3], c[4], m.fSmall)
    local fy = m.talFootY + math.floor((m.bh - m.ls) / 2)
    c = col(t.hintCol or "dim")
    el:drawText(t.hint or "", x + R(12), fy, c[1], c[2], c[3], c[4], m.fSmall)
    local note = t.reset and t.reset.note
    if note and note ~= "" then
        c = col("dim")
        el:drawTextRight(note, x + w - R(12) - m.talResetW - R(10), fy, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

-- ---------------------------------------------------------------------------
-- Kachel
-- ---------------------------------------------------------------------------
local Tile = ISButton:derive("BanditsNPCBearWinTalent")
U.WinTalent = Tile

-- Helligkeit des Hofs (0,55 .. 0,85), eine Welle je talGlowMs. getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485; math.sin wie
-- V:client/ISUI/ISEquippedItem.lua:391.
local function glowA()
    local ms = GLOW_MS
    if B.CFG and tonumber(B.CFG.talGlowMs) and tonumber(B.CFG.talGlowMs) > 0 then ms = tonumber(B.CFG.talGlowMs) end
    local ph = (getTimestampMs() % ms) / ms
    return 0.70 + 0.15 * math.sin(ph * 2 * math.pi)
end

function Tile:prerender()
    local m = self.win and self.win.m
    local e = self.e
    if m and e then
        local w, h = self.width, self.height
        local st = e.state
        local bg, bd, tt = col("btnBg"), col("talFreeBorder"), m.t
        if st == "on" then
            bg, bd, tt = col("talOnBg"), col("accent"), 2 * m.t
        elseif st == "locked" or st == "soon" then
            bg, bd = col("btnOffBg"), col("btnOffBorder")
        elseif self.mouseOver then                      -- mouseOver: ISButton.lua:18-20 / :22-23
            bg, bd = col("btnHoverBg"), col("accent")
        end
        local mul = 1
        if self.pressed and self.enable then mul = 0.8 end      -- ISButton.lua:59 / :41
        U.WinRect(self, 0, 0, w, h, bg, mul)
        U.WinFrame(self, 0, 0, w, h, tt, bd)
        local tex = textures()
        local te = tex.k[e.k]
        local ic = m.talIc
        local ix, iy = math.floor((w - ic) / 2), m.talIy
        local sz = m.talSmall and "64" or "128"
        if te then
            if st == "on" then
                local gs = math.floor(ic * GLOW_K + 0.5)
                local g = m.talSmall and tex.glow64 or tex.glow128
                if g then self:drawTextureScaled(g, ix - math.floor((gs - ic) / 2), iy - math.floor((gs - ic) / 2), gs, gs, glowA(), 1, 1, 1) end
                if te["_on" .. sz] then self:drawTextureScaled(te["_on" .. sz], ix, iy, ic, ic, 1, 1, 1, 1) end
            elseif st == "free" then
                if te[sz] then self:drawTextureScaled(te[sz], ix, iy, ic, ic, 1, 1, 1, 1) end      -- Nachbesserung P3: voll hell
            else
                if te["_off" .. sz] then self:drawTextureScaled(te["_off" .. sz], ix, iy, ic, ic, 1, 1, 1, 1) end
                local bs = m.talBadge
                local b = (st == "soon") and (bs <= 32 and tex.soon32 or tex.soon64) or (bs <= 32 and tex.lock32 or tex.lock64)
                if b then self:drawTextureScaled(b, ix + ic - math.floor(bs * 0.8), iy + ic - math.floor(bs * 0.8), bs, bs, 1, 1, 1, 1) end
            end
        end
    end
    ISButton.updateTooltip(self)                        -- ISButton.lua:176, :316-346
end

function Tile:render()
    local m = self.win and self.win.m
    local e = self.e
    if not m or not e then return end
    local st = e.state
    local stc, nc, sc = col("honeyText"), col("text"), col("text2")
    if st == "on" then
        stc, nc, sc = col("pipGold"), col("pipGold"), col("honeyText")
    elseif st == "locked" or st == "soon" then
        stc, nc, sc = col("dim"), col("btnOffText"), col("btnOffText")
    end
    self:drawText(e.stTxt or "", m.talStX, m.talStY, stc[1], stc[2], stc[3], stc[4], m.fSmall)
    local cx = self.width / 2
    self:drawTextCentre(e.name or "", cx, m.talNameY, nc[1], nc[2], nc[3], nc[4], m.fBody)
    self:drawTextCentre(e.short or "", cx, m.talShortY, sc[1], sc[2], sc[3], sc[4], m.fSmall)
end

-- ---------------------------------------------------------------------------
-- Ja/Nein-Fenster und Bitten
-- ---------------------------------------------------------------------------
local function dlgOpen()
    return T.dlg ~= nil and T.dlg:getIsVisible()        -- ISUIElement getIsVisible (wie BanditsNPCBearWindow.lua hideTip)
end

-- Gehoert der Baer id laut Sicht noch mir? (U.WinBears, client/BanditsNPCBearWinData.lua)
local function mine(id)
    if id == nil or not U.WinBears then return false end
    local list = U.WinBears()
    for i = 1, #list do
        if list[i].id == id then return true end
    end
    return false
end

-- Rueckruf "Talent lernen" (ISModalDialog.lua:62: onclick(Ziel, Knopf, Wert1, Wert2)); Ziel = Fenster, k = Talent, id = Baer.
function U.TalentYes(win, button, k, id)
    T.dlg = nil
    if not button or button.internal ~= "YES" then return end      -- V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:219
    if type(k) ~= "string" or not mine(id) then return end
    local player = getSpecificPlayer(0)                 -- V:client/Farming/CFarmingSystem.lua:45
    if not player then return end
    B.Ask(player, "Talent", { id = id, k = k })
    if win then win.dirty = true end
end

-- Rueckruf "alle zuruecksetzen".
function U.TalentResetYes(win, button, id)
    T.dlg = nil
    if not button or button.internal ~= "YES" then return end      -- ISAdminTicketsUI.lua:219
    if not mine(id) then return end
    local player = getSpecificPlayer(0)
    if not player then return end
    B.Ask(player, "TalentReset", { id = id })
    if win then win.dirty = true end
end

-- Vanillas Ja/Nein-Fenster an der Maus (ISWorldObjectContextMenu.lua:953; initialise + addToUIManager ISAnimalContextMenu.lua:1085-1086).
local function ask(win, text, fn, p1, p2)
    if dlgOpen() or not text then return false end
    local modal = ISModalDialog:new(0, 0, 350, 150, text, true, win, fn, 0, p1, p2)
    modal:initialise()
    modal:addToUIManager()
    T.dlg = modal
    return true
end

-- Klick auf eine waehlbare Kachel (Fenster: Win:onCmd "talent"). Nur, wenn das Modell sie gerade waehlbar zeigt.
function U.TalentAsk(win, button)
    local v = win and win.v
    local t = win and win.model and win.model.tal
    local e = button and button.e
    if not v or v.id == nil or not t or not e or e.state ~= "free" then return false end
    return ask(win, U.TalentAskText(win.model.name, e.k, (t.used or 0) + 1), U.TalentYes, e.k, v.id)
end

-- Klick auf "Reset" (nur, wenn der Knopf nicht grau ist).
function U.TalentResetAsk(win)
    local v = win and win.v
    local t = win and win.model and win.model.tal
    if not v or v.id == nil or not t or not t.reset or t.reset.state == "off" then return false end
    return ask(win, U.TalentResetText(win.model.name, t.earned or 0, v.talRd), U.TalentResetYes, v.id, nil)
end

-- Je Spielstart frisch: Bilder neu holen, ein altes Fenster vergessen (Events.OnGameStart: V:client/Chat/ISChat.lua:1186).
local function onGameStart()
    T.tex = nil
    T.dlg = nil
end
Events.OnGameStart.Add(onGameStart)
