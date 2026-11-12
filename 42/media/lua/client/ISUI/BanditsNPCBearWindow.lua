--
-- NPC Crew -- Baer, das Baeren-Fenster (F1, PLAN_F1.md 0.1, 0.4, 0.10, 1.1, 1.8; Kevin 11.11.2026: "ich wll noch spaeter eine richtige
-- UI die aufgeht wenn ich V druecke (einstellbar in den keystings)" -- "das schoene ui").
--
-- Ein eigenes ISPanel mit moveWithMouse (Vanilla V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1, :243, :253; Ziehen
-- V:client/ISUI/ISPanel.lua:49-95), NICHT ISCollapsableWindow (dessen Titelleiste nimmt fest UIFont.Small, ISCollapsableWindow.lua:398-399,
-- bei 4K winzig). Alles waechst mit EINEM Faktor f = U.MarkerFactor(Bildschirmhoehe, Option WinSize) (B1e, 1080 -> 1,0, Kevins
-- 2054 -> 2,0); Zeilenhoehen aus der echten Schrifthoehe, Breiten aus MeasureStringX -- so passt es bei jeder Vanilla-Schriftgroesse.
-- Aufbau (PLAN_F1.md 1.1): Kopf (Kevins Symbol 1, Name + Umbenennen, Koerper/Tag, naechste Stufe, Zustand-Chip, Abstand, Pfeile bei
-- mehreren Baeren, Schliessen), Karte "Condition" (Leben, Ausdauer, Traglast, "kommt spaeter"), Karte "Skills" (6 Faehigkeiten),
-- Karte "Orders" (6 Befehle, Passiv, Namensschild), Fusszeile. Bausteine: client/ISUI/BanditsNPCBearWinParts.lua; Inhalt:
-- client/BanditsNPCBearWinData.lua (U.WinModel).
-- Takt (nichts Teures je Bild, PLAN_F1.md 0.10): das Modell entsteht nur bei neuer Sicht (U.WinOnView) und hoechstens 1 x je Sekunde,
-- nur solange das Fenster offen ist; je Bild wird nur aus fertigen Feldern gezeichnet. Geschlossen: kein Bau, kein Zeichnen.
-- Befehle gehen als Bitte an den Schreiber (B.Ask: Einzelspieler B.Handle direkt, Mehrspieler sendClientCommand, Rolle user genuegt);
-- Besitz, Lage und Abklingzeit prueft der Schreiber. Das Fenster setzt nie einen Wert selbst (kein Cheat).
-- Nur Spieler 0 (wie V:client/ISUI/Hutch/ISHutchUI.lua:884-893). Kein Schliessen wegen Abstand (F-j).
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"
require "ISUI/ISButton"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Klasse bleibt ein Local. ISPanel:derive: V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1.
local Win = ISPanel:derive("BanditsNPCBearWindow")

local KEY_NAME = "Bear window"                  -- Kennung der Taste in keysB42.ini (client/BanditsNPCBearKey.lua, fuer immer stabil)
local LAYOUT_NAME = "BanditsNPCBearWindow"      -- Name in Vanillas layout.ini (eindeutig, Kollisionsprobe forschung_f1.md 8)
local MODEL_MS = 1000
local FIT = 0.92                                -- passt das Fenster nicht in 92 % der Bildhoehe, wird f eine Stufe kleiner
local ICON_FILE = "media/ui/BanditsNPCBearCub_marker288.png"
local DISC_FILE = "media/ui/BanditsNPCBearMarker_disc.png"
local CLOSE_FILE = "media/ui/inventoryPanes/Button_Close.png"
local CMDS = { "follow", "stay", "sit", "roam", "come", "unstuck" }

-- Alles, was das Fenster sich merkt (nur diese Sitzung): genau EIN Fenster-Objekt je Spielstart.
local W = { win = nil, tex = nil }

local function col(key)
    local c = U.WIN_COL and U.WIN_COL[key]
    return c or { 1, 1, 1, 1 }
end

-- Textbreite. getTextManager():MeasureStringX(Schrift, Text): V:client/ISUI/ISButton.lua:450, :233.
local function tw(font, s)
    if s == nil or s == "" then return 0 end
    return getTextManager():MeasureStringX(font, s)
end

local function screen()
    local core = getCore()
    return core:getScreenWidth(), core:getScreenHeight()   -- V:client/Challenge/WinterIsComing.lua:18
end

-- Optionswert WinSize (Index der Auswahl, client/BanditsNPCBearOptions.lua): 1 = Auto. Fehlt die Seite: Auto.
local function sizeIdx()
    local v = 1
    if U.Opt then v = tonumber(U.Opt("WinSize", 1)) or 1 end
    return math.floor(v)
end

local function factor(h, idx)
    if U.MarkerFactor then return U.MarkerFactor(h, idx) end
    return 1, 1
end

-- ---------------------------------------------------------------------------
-- Masse (PLAN_F1.md 1.1, Pixel bei f = 1, jede Zahl x f gerundet; lb / ls / ln = Zeilenhoehe Text / Klein / Name). Dieselbe Rechnung wie
-- f1_entwurf/zeichne_fenster.py window(). Gibt die Tabelle m mit allen Massen und Lagen; misst die festen Texte (Breite waechst nur,
-- wenn ein Text nicht passt). Nur beim Legen.
-- ---------------------------------------------------------------------------
-- Breite, die die wechselnden Texte brauchen (Name + Umbenennen + Pfeile, Koerper/Stufe neben dem Chip, Hinweis der Befehle,
-- Fusszeile). Mit den Schriften und festen Breiten aus m; im 1-s-Takt nur diese wenigen Messungen (layoutStale).
local function dynNeed(m, d, n)
    local P = m.P
    local need = 0
    local function grow(v) if v > need then need = v end end
    local right = m.R24
    local countW = 0
    if n > 1 then
        countW = math.max(tw(m.fSmall, d and d.count), m.R28)
        right = right + m.R6 + m.R24 + m.R6 + countW + m.R6 + m.R24
    end
    local nameW = tw(m.fName, d and d.name)
    grow(m.tx + nameW + m.bold + m.R12 + m.renameW + m.R16 + right + P)
    local subW = math.max(tw(m.fBody, d and d.sub), tw(m.fBody, d and d.next))
    grow(m.tx + subW + m.R16 + math.max(m.chipMax, m.distW) + P)
    grow(2 * P + m.R24 + m.ordTitleW + m.R16 + tw(m.fSmall, d and d.ordersInfo))
    grow(2 * P + tw(m.fSmall, d and d.footer))
    return need, nameW, countW
end

local function metrics(f, d, n, sw, sh, idx)
    local m = { f = f, n = n, sw = sw, sh = sh, idx = idx }
    local function R(v) return math.floor(v * f + 0.5) end
    for _, v in ipairs({ 2, 3, 4, 6, 8, 9, 10, 12, 14, 16, 24, 28, 36, 40, 44, 46, 72, 80, 94, 100 }) do m["R" .. v] = R(v) end
    m.t = math.max(1, math.floor(f))
    m.bar = R(4)
    m.bold = math.max(1, math.floor(f / 2))
    m.ox, m.oy = R(8), R(3)
    m.fName, m.fBody, m.fSmall, m.ln, m.lb, m.ls = U.WinFonts(f)
    local P = R(16)
    m.P = P
    local lb, ls, ln = m.lb, m.ls, m.ln
    m.headH = math.max(R(100), R(14) + ln + R(2) + lb + R(2) + lb + R(10))
    m.rowBar = lb + R(4) + R(10) + R(10)
    m.rowVal = lb + R(10)
    m.needGrid = 2 * (ls + R(6))
    local leftH = R(10) + lb + R(8) + 2 * m.rowBar + m.rowVal + R(9) + ls + R(6) + m.needGrid + R(10)
    m.rowSk = lb + R(4) + R(8) + R(8)
    local rightH = R(10) + lb + R(8) + 6 * m.rowSk + R(4)
    m.cardH = math.max(leftH, rightH)
    m.bh = math.max(R(34), lb + R(12))
    m.th = math.max(R(30), lb + R(10))
    m.ordH = R(10) + lb + R(8) + m.bh + R(8) + m.bh + R(10) + m.th + R(12)
    m.y1 = m.headH + R(16)
    m.y2 = m.y1 + m.cardH + R(16)
    m.y3 = m.y2 + m.ordH + R(10)
    m.H = m.y3 + ls + R(14)
    m.chipH = lb + R(8)
    m.tx = P + R(94)
    m.ty = R(14)
    m.l2y = m.ty + ln + R(2)
    m.l3y = m.l2y + lb + R(2)
    m.rbh = ls + R(6)
    -- Breite: mindestens 640 x f; mehr nur, wenn ein Text nicht passt (PLAN_F1.md 1.1). Feste Texte hier (einmal je Legen),
    -- wechselnde in dynNeed.
    local s = (d and d.wide) or {}
    local need = R(640)
    local function grow(v) if v > need then need = v end end
    m.renameW = tw(m.fSmall, d and d.rename) + R(16)
    local chipMax = 0
    if type(s.state) == "table" then
        for _, txt in pairs(s.state) do chipMax = math.max(chipMax, tw(m.fBody, txt)) end
    end
    m.chipMax = R(28) + chipMax + R(12)
    m.distW = math.max(tw(m.fSmall, s.wideDist), tw(m.fSmall, s.wideDist2))
    m.ordTitleW = tw(m.fBody, s.tOrders)
    -- Karten: jede Spalte CW >= Etikett + Wert + 36 x f
    local cw = 0
    local function col2(a, b, extra) cw = math.max(cw, a + b + (extra or R(36))) end
    col2(tw(m.fBody, s.tHealth), tw(m.fBody, s.wideVal))
    col2(tw(m.fBody, s.tStamina), tw(m.fBody, s.wideVal))
    col2(tw(m.fBody, s.tCarry), tw(m.fBody, s.wideCarry))
    local lvW, pctW = tw(m.fBody, s.wideLv), math.max(tw(m.fSmall, s.widePct), tw(m.fSmall, s.max))
    if type(s.skName) == "table" then
        for i = 1, #s.skName do col2(tw(m.fBody, s.skName[i]), lvW + R(8) + pctW, R(44)) end
    end
    if type(s.needs) == "table" then
        local wMax = 0
        for i = 1, #s.needs do wMax = math.max(wMax, tw(m.fSmall, s.needs[i])) end
        cw = math.max(cw, 2 * (R(12) + wMax + R(8)) + R(24))
    end
    cw = math.max(cw, tw(m.fSmall, s.tLater) + R(24))
    grow(2 * P + 2 * cw + R(16))
    -- Befehle: jeder Knopf bw >= laengster Knopftext + 24 x f; Schalter: Kaestchen + Abstaende + Text
    local bwNeed = 0
    if type(s.btn) == "table" then
        for _, txt in pairs(s.btn) do bwNeed = math.max(bwNeed, tw(m.fBody, txt) + R(24)) end
    end
    bwNeed = math.max(bwNeed, tw(m.fBody, s.wideUnstuck) + R(24))
    bwNeed = math.max(bwNeed, tw(m.fBody, s.passive) + R(46), tw(m.fBody, s.tag) + R(46))
    grow(2 * P + 3 * bwNeed + R(40))
    local footW = 0
    for _, txt in ipairs({ s.hintMissing, s.hintRide, s.hintAway, s.hintEsc }) do footW = math.max(footW, tw(m.fSmall, txt)) end
    grow(2 * P + footW)
    m.needStatic = need
    local dyn, nameW, countW = dynNeed(m, d, n)
    m.nameW, m.countW = nameW, countW
    if dyn > need then need = dyn end
    m.need = need
    -- Spaltenbreite ganzzahlig, Fensterbreite exakt daraus (keine Rundungsluecke am rechten Rand)
    m.CW = math.floor((need - 2 * P - R(16)) / 2 + 0.999)
    m.W = 2 * P + 2 * m.CW + R(16)
    m.ow = m.W - 2 * P
    m.bw = math.floor((m.ow - R(24) - 2 * R(8)) / 3)
    m.lx, m.rx = P, P + m.CW + R(16)
    return m
end

-- Lage der Kinder (Knoepfe, Zeilen, Schalter) nach den Massen m. setX/setY/setWidth/setHeight: V:client/ISUI/ISUIElement.lua:195-245
-- (Vanilla ruft sie an Knoepfen, z. B. V:client/ISUI/ISCollapsableWindow.lua; Aufrufer V:client/ISUI/ISToolTip.lua:78-79).
local function put(el, x, y, w, h)
    el:setX(x)
    el:setY(y)
    el:setWidth(w)
    el:setHeight(h)
end

local function place(win, m)
    local P = m.P
    win:setWidth(m.W)
    win:setHeight(m.H)
    -- Kopf
    put(win.closeB, m.W - P - m.R24, m.R12, m.R24, m.R24)
    win.closeB:forceImageSize(m.R24, m.R24)          -- V:client/ISUI/ISInventoryPage.lua:1479
    put(win.rename, m.tx + m.nameW + m.bold + m.R12, m.ty + math.floor((m.ln - m.rbh) / 2), m.renameW, m.rbh)
    win.rename.font, win.rename.fh = m.fSmall, m.ls
    local nx = m.W - P - m.R24 - m.R6 - m.R24
    put(win.nextB, nx, m.R12, m.R24, m.R24)
    m.countX = nx - m.R6 - math.floor(m.countW / 2)
    put(win.prevB, nx - m.R6 - m.countW - m.R6 - m.R24, m.R12, m.R24, m.R24)
    win.prevB.font, win.prevB.fh = m.fBody, m.lb
    win.nextB.font, win.nextB.fh = m.fBody, m.lb
    win.prevB:setVisible(m.n > 1)                   -- ISButton:setVisible V:client/ISUI/ISButton.lua:9
    win.nextB:setVisible(m.n > 1)
    -- Karte links: Leben, Ausdauer, Traglast, "kommt spaeter"
    local yy = m.y1 + m.R10 + m.lb + m.R8
    put(win.rows.hp, m.lx + m.R4, yy - m.R3, m.CW - m.R8, m.rowBar - m.R2)
    yy = yy + m.rowBar
    put(win.rows.sta, m.lx + m.R4, yy - m.R3, m.CW - m.R8, m.rowBar - m.R2)
    yy = yy + m.rowBar
    put(win.rows.carry, m.lx + m.R4, yy - m.R3, m.CW - m.R8, m.rowVal - m.R2)
    yy = yy + m.rowVal
    m.divY = yy
    yy = yy + m.R9
    put(win.rows.later, m.lx + m.R4, yy - m.R3, m.CW - m.R8, 3 * (m.ls + m.R6))
    -- Karte rechts: sechs Faehigkeiten
    yy = m.y1 + m.R10 + m.lb + m.R8
    for i = 1, 6 do
        put(win.rows[i], m.rx + m.R4, yy - m.R3, m.CW - m.R8, m.rowSk - m.R2)
        yy = yy + m.rowSk
    end
    -- Befehle: 2 Reihen x 3 Knoepfe, darunter die Schalter
    local by0 = m.y2 + m.R10 + m.lb + m.R8
    for i = 1, #CMDS do
        local b = win.btn[CMDS[i]]
        put(b, P + m.R12 + ((i - 1) % 3) * (m.bw + m.R8), by0 + math.floor((i - 1) / 3) * (m.bh + m.R8), m.bw, m.bh)
        b.font, b.fh = m.fBody, m.lb
    end
    local ty0 = by0 + 2 * (m.bh + m.R8) + m.R2
    put(win.tick.pas, P + m.R12, ty0, m.bw, m.th)
    put(win.tick.tag, P + m.R12 + m.bw + m.R8, ty0, m.bw, m.th)
end

-- Auf den Bildschirm klemmen: mindestens 40 x f px sichtbar, Oberkante nie ueber dem Bild (PLAN_F1.md 1.1 "Lage").
local function clampPos(win)
    local m = win.m
    if not m then return end
    local sw, sh = screen()
    local keep = m.R40
    local x, y = win:getX(), win:getY()             -- V:client/ISUI/ISLayoutManager.lua:55-56
    local nx = math.max(keep - m.W, math.min(x, sw - keep))
    local ny = math.max(0, math.min(y, sh - keep))
    if nx ~= x then win:setX(nx) end
    if ny ~= y then win:setY(ny) end
end

-- ---------------------------------------------------------------------------
-- U.WinLayout(): Faktor, Schrift, Masse, Kinder neu legen (PLAN_F1.md 1.1, 1.7). Passt das Fenster nicht (H > 0,92 x Bildhoehe), eine
-- Stufe kleiner (U.MarkerFactor(h, k): Index k = Stufe k-1, bis 1,0).
-- ---------------------------------------------------------------------------
function U.WinLayout()
    local win = W.win
    if not win then return end
    local sw, sh = screen()
    local idx = sizeIdx()
    local f, k = factor(sh, idx)
    local m = nil
    for _ = 1, 8 do
        m = metrics(f, win.model, win.n or 1, sw, sh, idx)
        if m.H <= FIT * sh or (k or 1) <= 1 then break end
        f, k = factor(sh, k)
    end
    m.disc = W.tex and W.tex.disc
    win.m = m
    place(win, m)
    clampPos(win)
end

-- ---------------------------------------------------------------------------
-- Das Fenster
-- ---------------------------------------------------------------------------

-- ISPanel:new + eigene Felder (Form V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:243-253); Tasten wie
-- V:client/ISUI/Crafting/ISHandcraftWindow.lua:386 (setWantKeyEvents vor dem Anlegen speichert nur das Feld, ISUIElement.lua:1828-1831).
function Win:new(x, y, w, h)
    local o = ISPanel:new(x, y, w, h)
    setmetatable(o, self)
    self.__index = self
    o.moveWithMouse = true
    o.background = false                            -- eigener Hintergrund (Feld wie ISPanel:noBackground, V:client/ISUI/ISPanel.lua:9-11)
    o:setWantKeyEvents(true)
    o.dirty = true
    o.modelAt = 0
    o.n = 0
    o.idx = 1
    o.isOpen = false
    return o
end

-- Kinder einmal anlegen. ISButton:new(x, y, w, h, Titel, Ziel, Rueckruf) + initialise + addChild: V:client/ISUI/ISCollapsableWindow.lua:55-61
-- (dort auch das Bild am Schliessen-Knopf, setImage :60, Hintergrund-Alpha :57-59). Abgeleitete Klassen erben :new
-- (V:client/ISUI/ISResizeableButton.lua:1; Aufrufer V:client/ISUI/ISInventoryPane.lua:63). Titel immer "" -- die Texte zeichnen die
-- Klassen selbst aus fertigen Feldern.
local function kid(win, cls, cmd, style)
    local b = cls:new(0, 0, 10, 10, "", win, Win.onCmd)
    b:initialise()
    b.win, b.cmd, b.style, b.state = win, cmd, style, "normal"
    win:addChild(b)
    win.kids[#win.kids + 1] = b
    return b
end

function Win:build()
    self.kids = {}
    self.btn = {}
    for i = 1, #CMDS do self.btn[CMDS[i]] = kid(self, U.WinBtn, CMDS[i], "cmd") end
    self.rename = kid(self, U.WinBtn, "rename", "small")
    self.prevB = kid(self, U.WinBtn, "prev", "small")
    self.nextB = kid(self, U.WinBtn, "next", "small")
    self.prevB.label, self.nextB.label = "<", ">"
    self.tick = { pas = kid(self, U.WinTick, "passive"), tag = kid(self, U.WinTick, "tag") }
    self.rows = {
        hp = kid(self, U.WinRow, nil), sta = kid(self, U.WinRow, nil), carry = kid(self, U.WinRow, nil),
        later = kid(self, U.WinRow, nil),
    }
    self.rows.hp.kind, self.rows.hp.key = "bar", "hp"
    self.rows.sta.kind, self.rows.sta.key = "bar", "sta"
    self.rows.carry.kind, self.rows.carry.key = "val", "carry"
    self.rows.later.kind = "later"
    for i = 1, 6 do
        local r = kid(self, U.WinRow, nil)
        r.kind, r.key = "skill", i
        self.rows[i] = r
    end
    for _, r in pairs(self.rows) do r.onclick = nil end   -- Zeilen klicken nicht (ISButton.lua:42-44)
    -- Schliessen: Vanillas Knopf mit Vanillas Bild (wie ISCollapsableWindow.lua:55-61)
    local c = ISButton:new(0, 0, 10, 10, "", self, Win.onClose)
    c:initialise()
    c.borderColor.a = 0.0                           -- ISCollapsableWindow.lua:57
    local bg, hv = col("closeBg"), col("closeHover")
    c.backgroundColor = { r = bg[1], g = bg[2], b = bg[3], a = bg[4] }
    c.backgroundColorMouseOver = { r = hv[1], g = hv[2], b = hv[3], a = hv[4] }
    if W.tex and W.tex.close then c:setImage(W.tex.close) end   -- ISCollapsableWindow.lua:60
    self:addChild(c)
    self.kids[#self.kids + 1] = c
    self.closeB = c                                 -- nicht "close": das ist ISPanel:close (V:client/ISUI/ISPanel.lua:14)
end

-- Offene Tooltips der Kinder abmelden (wie ISButton:updateTooltip selbst: V:client/ISUI/ISButton.lua:341-343).
local function hideTips(win)
    if not win.kids then return end
    for i = 1, #win.kids do
        local tip = win.kids[i].tooltipUI
        if tip and tip:getIsVisible() then
            tip:setVisible(false)
            tip:removeFromUIManager()
        end
    end
end

-- Modell anwenden: Texte, Zustaende, Tooltips der Kinder; Breiten, die je Sekunde wechseln (Chip, Prozent). Nur im 1-s-Takt.
local function apply(win, d)
    local m = win.m
    if not m then return end
    d.chipW = m.R28 + tw(m.fBody, d.chipText) + m.R12
    for i = 1, #d.skills do
        local s = d.skills[i]
        s.pctW = tw(m.fSmall, s.pctTxt)
        win.rows[i].tooltip = s.tip
    end
    for i = 1, #CMDS do
        local key = CMDS[i]
        local b, e = win.btn[key], d.buttons[key]
        b.label, b.state, b.tooltip = e.label, e.state, e.tip
        b.enable = (e.state ~= "off")               -- ISButton.lua:45; Felder wie V:client/ISUI/Hutch/ISHutchUI.lua:617-623
    end
    win.rename.label = d.rename
    local t = d.toggles
    win.tick.pas.on, win.tick.pas.label, win.tick.pas.tooltip = t.pas, t.pasLabel, t.pasTip
    win.tick.tag.on, win.tick.tag.label, win.tick.tag.tooltip = t.tag, t.tagLabel, t.tagTip
    win.rows.hp.tooltip, win.rows.sta.tooltip = d.tips.hp, d.tips.sta
    win.rows.carry.tooltip, win.rows.later.tooltip = d.tips.carry, d.tips.later
end

-- Neu legen noetig? Option, Bildschirm, Zahl der Baeren, Name (Lage des Umbenennen-Knopfs) oder ein Text, der nicht mehr passt.
local function layoutStale(win, d)
    local m = win.m
    if not m then return true end
    local sw, sh = screen()
    if sw ~= m.sw or sh ~= m.sh or sizeIdx() ~= m.idx then return true end
    if (win.n > 1) ~= (m.n > 1) then return true end
    local dyn, nameW, countW = dynNeed(m, d, win.n)
    if nameW ~= m.nameW or countW ~= m.countW then return true end
    return math.max(m.needStatic, dyn) ~= m.need
end

-- Modell neu bauen (bei neuer Sicht oder je MODEL_MS). Gibt false, wenn das Fenster dabei geschlossen wurde.
function Win:refresh(now)
    self.dirty = false
    self.modelAt = now
    local player = getSpecificPlayer(0)             -- V:client/Farming/CFarmingSystem.lua:45
    if not player or player:isDead() then           -- V:client/ISUI/ISUIHandler.lua:42
        U.WinClose()
        return false
    end
    local list = U.WinBears()
    if #list == 0 then
        U.WinClose()
        return false
    end
    local idx = nil
    for i = 1, #list do
        if list[i].id == self.sel then idx = i end
    end
    if idx == nil then idx = math.min(math.max(self.idx or 1, 1), #list) end   -- der gewaehlte ist weg: naechster eigener Baer
    local v = list[idx]
    self.idx, self.sel, self.n, self.v = idx, v.id, #list, v
    local d = U.WinModel(v, player, now)
    if #list > 1 then d.count = U.T("UI_BN_Bear_Win_Count", idx, #list) end
    self.model = d
    if layoutStale(self, d) then U.WinLayout() end
    apply(self, d)
    return true
end

-- Klick auf einen Knopf / Schalter (ISButton ruft onclick(Ziel, Knopf), V:client/ISUI/ISButton.lua:47). Nur Bitten an den Schreiber;
-- nie eine leere Tabelle (S:client/BanditsNPCBearClient.lua sendHello).
function Win:onCmd(button)
    if not button or button.state == "off" then return end
    local cmd = button.cmd
    local player = getSpecificPlayer(0)
    if not player then return end
    if cmd == "prev" or cmd == "next" then
        local n = self.n or 1
        if n > 1 then
            local i = (self.idx or 1) + ((cmd == "next") and 1 or -1)
            if i < 1 then i = n end
            if i > n then i = 1 end
            local list = U.WinBears()
            if list[i] then self.sel, self.idx = list[i].id, i end
            self.dirty = true
        end
        return
    end
    local v = self.v
    if not v or v.id == nil then return end
    if cmd == "follow" or cmd == "stay" or cmd == "sit" or cmd == "roam" then
        B.Ask(player, "Mode", { id = v.id, mode = cmd })
    elseif cmd == "come" then
        B.Ask(player, "Come", { id = v.id })
    elseif cmd == "unstuck" then
        B.Ask(player, "Call", { id = v.id })
    elseif cmd == "passive" then
        B.Ask(player, "Passive", { id = v.id, on = not (v.pas == true) })
    elseif cmd == "tag" then
        if U.TagSet and U.TagOn then U.TagSet(v, not U.TagOn(v)) end
        self.dirty = true
    elseif cmd == "rename" then
        if U.AskName then self.nameBox = U.AskName(player, v) end
    end
end

function Win:onClose()
    U.WinClose()
end

-- Zeichnen je Bild: nur Rechtecke, Bilder und fertige Texte (PLAN_F1.md 0.10). drawRect / drawRectBorder / drawText / drawTextRight /
-- drawTextCentre / drawTextureScaled wie client/ISUI/BanditsNPCBearWinParts.lua (Belege dort); Bild-Zeichnen V:client/Chat/ISChat.lua:418.
local function drawHead(self, m, d)
    local P = m.P
    local tex = W.tex or {}
    local disc = col("iconDisc")
    if tex.disc then self:drawTextureScaled(tex.disc, P, m.R12, m.R80, m.R80, 1, disc[1], disc[2], disc[3]) end
    if tex.icon then self:drawTextureScaled(tex.icon, P + m.R4, m.R16, m.R72, m.R72, 1, 1, 1, 1) end
    local c = col("name")
    self:drawText(d.name or "", m.tx, m.ty, c[1], c[2], c[3], c[4], m.fName)
    self:drawText(d.name or "", m.tx + m.bold, m.ty, c[1], c[2], c[3], c[4], m.fName)   -- zweimal = "fett" (PLAN_F1.md 1.1)
    c = col("text2")
    self:drawText(d.sub or "", m.tx, m.l2y, c[1], c[2], c[3], c[4], m.fBody)
    if d.next then
        c = col("honeyText")
        self:drawText(d.next, m.tx, m.l3y, c[1], c[2], c[3], c[4], m.fBody)
    end
    if d.count and m.n > 1 then
        c = col("text2")
        self:drawTextCentre(d.count, m.countX, m.R12 + math.floor((m.R24 - m.ls) / 2), c[1], c[2], c[3], c[4], m.fSmall)
    end
    -- Zustand-Chip (rechtsbuendig) und Abstand darunter
    local cw = d.chipW or 0
    local chx, chy = m.W - P - cw, m.R44
    local r, g, b = d.cr or 1, d.cg or 1, d.cb or 1
    self:drawRect(chx, chy, cw, m.chipH, 1, r * 0.2, g * 0.2, b * 0.2)
    for i = 0, m.t - 1 do self:drawRectBorder(chx + i, chy + i, cw - 2 * i, m.chipH - 2 * i, 0.85, r, g, b) end
    if tex.disc then self:drawTextureScaled(tex.disc, chx + m.R10, chy + math.floor((m.chipH - m.R10) / 2), m.R10, m.R10, 1, r, g, b) end
    c = col("text")
    self:drawText(d.chipText or "", chx + m.R28, chy + m.R4, c[1], c[2], c[3], c[4], m.fBody)
    if d.dist then
        c = col("dim")
        self:drawTextRight(d.dist, m.W - P, chy + m.chipH + m.R4, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

local function card(self, m, x, y, w, h, title, info)
    U.WinRect(self, x, y, w, h, col("cardBg"))
    U.WinFrame(self, x, y, w, h, m.t, col("cardBorder"))
    local c = col("title")
    self:drawText(title or "", x + m.R12, y + m.R10, c[1], c[2], c[3], c[4], m.fBody)
    if info and info ~= "" then
        c = col("dim")
        self:drawTextRight(info, x + w - m.R12, y + m.R10, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

function Win:prerender()
    local now = getTimestampMs()                    -- V:client/Foraging/ISBaseIcon.lua:485
    if self.dirty or now - self.modelAt >= MODEL_MS or now < self.modelAt then
        if not self:refresh(now) then return end
    end
    local m, d = self.m, self.model
    if not m or not d then return end
    U.WinRect(self, 0, 0, m.W, m.H, col("winBg"))
    U.WinFrame(self, 0, 0, m.W, m.H, m.t, col("winBorder"))
    U.WinRect(self, 0, 0, m.W, m.R3, col("accent"))
    drawHead(self, m, d)
    U.WinRect(self, m.P, m.headH + m.R4, m.W - 2 * m.P, m.t, col("divider"))
    card(self, m, m.lx, m.y1, m.CW, m.cardH, d.tCond)
    U.WinRect(self, m.lx + m.R12, m.divY, m.CW - m.R24, m.t, col("divider"))
    card(self, m, m.rx, m.y1, m.CW, m.cardH, d.tSkills)
    card(self, m, m.P, m.y2, m.ow, m.ordH, d.tOrders, d.ordersInfo)
    local c = col("dim")
    self:drawText(d.footer or "", m.P, m.y3, c[1], c[2], c[3], c[4], m.fSmall)
end

-- Esc oder die eigene Taste schliessen (V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-297; Esc nur Spieler 0 wie
-- V:client/ISUI/Hutch/ISHutchUI.lua:884-893). Nicht, solange der Spieler tippt: Chat (ISChat.focused, V:client/Chat/ISChat.lua:8)
-- oder das Namensfeld dieses Fensters (isReallyVisible, V:client/ISUI/ISUIElement.lua:690) -- sonst schloesse ein "v" im Namen das Fenster.
local function typing(self)
    if ISChat and ISChat.focused then return true end
    local box = self.nameBox
    return box ~= nil and box:isReallyVisible()
end

-- Schliess-Taste: Esc oder die eigene Belegung (isKey(Text, key): V:client/ISUI/FPS.lua:9). Die einzige Tastenabfrage dieser Datei.
local function closeKey(key)
    return key == Keyboard.KEY_ESCAPE or getCore():isKey(KEY_NAME, key)
end

function Win:isKeyConsumed(key)
    if typing(self) then return false end
    return closeKey(key)
end

function Win:onKeyRelease(key)
    if typing(self) then return end
    if self:isVisible() and closeKey(key) then
        U.WinClose()
    end
end

-- Lage merken (V:client/ISUI/ISLayoutManager.lua:6-13 RegisterWindow mit eigener Klasse wie V:client/Chat/ISChat.lua:1172; gerufen
-- :103 / :111). NUR x und y -- kein "visible", sonst oeffnete Vanillas DefaultRestoreWindow das Fenster nach dem Laden von selbst
-- (:45-50). Geschrieben in layout.ini beim Spielspeichern (:191-232), je Aufloesung.
function Win:SaveLayout(_name, layout)
    layout.x = self:getX()
    layout.y = self:getY()
    layout.visible, layout.width, layout.height = nil, nil, nil
end

function Win:RestoreLayout(_name, layout)
    local x = tonumber(layout.x)                    -- ISLayoutManager.lua:17-18
    local y = tonumber(layout.y)
    if x ~= nil and y ~= nil then
        self:setX(x)
        self:setY(y)
        clampPos(self)
    end
end

-- ---------------------------------------------------------------------------
-- Oeffnen / Schliessen (PLAN_F1.md 1.8)
-- ---------------------------------------------------------------------------

-- Bilder einmal je Spielstart. getTexture(Pfad): V:client/Chat/ISChat.lua:137; Vanillas Schliessen-Bild:
-- V:client/ISUI/ISCollapsableWindow.lua:386; eigene Bilder wie S:client/ISUI/BanditsNPCBearMarker.lua (288-px-Symbol, Scheibe).
local function textures()
    if W.tex then return W.tex end
    W.tex = { icon = getTexture(ICON_FILE), disc = getTexture(DISC_FILE), close = getTexture(CLOSE_FILE) }
    return W.tex
end

-- Der naechste eigene Baer (Sicht-Lage) -- beim Oeffnen ohne Kennung (Frage F6).
local function nearest(list, player)
    local best, bestD = list[1], nil
    local px, py = player:getX(), player:getY()     -- V:client/Fishing/TensionUI.lua:11
    for i = 1, #list do
        local v = list[i]
        if type(v.x) == "number" and type(v.y) == "number" then
            local dx, dy = v.x + 0.5 - px, v.y + 0.5 - py
            local dd = dx * dx + dy * dy
            if bestD == nil or dd < bestD then best, bestD = v, dd end
        end
    end
    return best
end

-- Hinweis ueber der Figur. HaloTextHelper.addText(Spieler, Text): V:client/Foraging/forageClient.lua:73.
local function halo(player, key)
    HaloTextHelper.addText(player, U.T(key))
end

function U.WinOpen(player, id)
    player = player or getSpecificPlayer(0)
    if not player then return false end
    if not U.Fresh or not U.Fresh() then
        if U.AskHello then U.AskHello(player) end
        halo(player, "UI_BN_Bear_Win_NoData")
        return false
    end
    local list = U.WinBears()
    if #list == 0 then
        halo(player, "UI_BN_Bear_Win_NoBear")
        return false
    end
    local pick = nil
    if id ~= nil then
        for i = 1, #list do
            if list[i].id == id then pick = list[i] end
        end
    end
    if pick == nil then pick = nearest(list, player) end
    local win = W.win
    local first = (win == nil)
    if first then
        textures()
        win = Win:new(0, 0, 640, 480)
        win:initialise()                            -- V:client/ISUI/Animal/ISAnimalContextMenu.lua:746
        win:build()
        W.win = win
    end
    win.sel = pick.id
    win.dirty = true
    if not win:refresh(getTimestampMs()) then return false end
    if first then
        local sw, sh = screen()
        local m = win.m
        win:setX(math.floor((sw - m.W) * 0.62))
        win:setY(math.floor((sh - m.H) * 0.30))
        ISLayoutManager.RegisterWindow(LAYOUT_NAME, Win, win)   -- stellt eine gemerkte Lage sofort her (ISLayoutManager.lua:12)
        clampPos(win)
    end
    win.isOpen = true
    win:addToUIManager()                            -- V:client/ISUI/ISUIElement.lua:1365
    win:setVisible(true)                            -- :657
    win:bringToTop()                                -- :1548
    return true
end

function U.WinClose()
    U.winClosedAt = getTimestampMs()
    local win = W.win
    if not win then return end
    win.isOpen = false
    hideTips(win)
    win:setVisible(false)                           -- wie V:client/ISUI/Crafting/ISHandcraftWindow.lua:295-296 (close + removeFromUIManager)
    win:removeFromUIManager()
end

function U.WinIsOpen()
    return W.win ~= nil and W.win.isOpen == true
end

-- Nachbesserung F1 B10: tippt der Spieler gerade (Chat oder das Namensfeld dieses Fensters ist offen, auch ohne Fokus)? Dann schliesst die
-- Taste das Fenster auch ueber client/BanditsNPCBearKey.lua nicht (isKeyConsumed gibt die Taste dann frei).
function U.WinTyping()
    local win = W.win
    return win ~= nil and win.isOpen == true and typing(win)
end

function U.WinToggle(player)
    if U.WinIsOpen() then
        U.WinClose()
    else
        U.WinOpen(player)
    end
end

-- Naht zur Sicht: B.OnView (client/ISUI/BanditsNPCBearHud.lua) ruft das nach jeder neuen Sicht -> Modell im naechsten Bild neu.
function U.WinOnView()
    if W.win then W.win.dirty = true end
end

-- Je Spielstart ein frisches Fenster: ein altes (Hauptmenue und neu laden) wird geschlossen, abgemeldet und vergessen (wie
-- S:client/ISUI/BanditsNPCBearHud.lua onGameStart).
local function onGameStart()
    if W.win then U.WinClose() end
    W.win = nil
    W.tex = nil
end

-- Bildschirm-Aufloesung geaendert: neu legen und klemmen. Events.OnResolutionChange: V:client/ISUI/PlayerData/ISPlayerData.lua:206.
local function onResolution()
    if W.win then U.WinLayout() end
end

Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
Events.OnResolutionChange.Add(onResolution)
