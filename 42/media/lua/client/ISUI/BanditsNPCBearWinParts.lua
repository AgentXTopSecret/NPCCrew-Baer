--
-- NPC Crew -- Baer, Bausteine des Baeren-Fensters (F1, PLAN_F1.md 1.1-1.3, 7.5, 7.7; Kevin 11.11.2026: "das schoene ui").
--
-- Hier stehen nur Bausteine, das Fenster selbst steht in client/ISUI/BanditsNPCBearWindow.lua, sein Inhalt (fertige Texte) in
-- client/BanditsNPCBearWinData.lua:
--   * Farben (U.WinColor) und Farbverlauf der Balken nach Wert (U.WinRamp) -- PLAN_F1.md 1.3.
--   * Schriftwahl (U.WinFonts) -- PLAN_F1.md 1.2: groesste von Small/Medium/Large mit Zeilenhoehe <= Ziel x 1,1; Name > Text > Klein.
--   * Drei kleine Klassen, alle von Vanillas ISButton abgeleitet (V:client/ISUI/ISResizeableButton.lua:1 -- dort genauso
--     ISButton:derive, :new wird geerbt; Aufrufer V:client/ISUI/ISInventoryPane.lua:63): so kommen Klick, Ton, enable und
--     Vanillas Tooltip (auch an grauen Knoepfen: onMouseMove setzt mouseOver ohne enable-Frage V:client/ISUI/ISButton.lua:18-20,
--     updateTooltip :316-346) mit. Gezeichnet wird in eigener prerender/render mit eigenen Farben; prerender ruft ZULETZT
--     ISButton.updateTooltip(self) (wie Vanillas ISButton:prerender :176).
--       U.WinBtn  -- Befehls-Knopf (Zustand normal / active / off) und kleine Knoepfe (Umbenennen, Pfeile).
--       U.WinRow  -- Zeile mit Tooltip, ohne Klick (onclick = nil, ISButton.lua:42-44): zeichnet Wert, Balken oder Faehigkeit.
--       U.WinTick -- Schalter: Kaestchen + Text, der Klick schaltet (das Fenster schickt die Bitte).
-- Je Bild wird nur aus fertigen Feldern gezeichnet (Modell des Fensters, hoechstens 1 x je Sekunde gebaut; Masse beim Legen):
-- keine Tabelle, kein getText, kein MeasureStringX je Bild.
-- Zeichen-Aufrufe (alle ISUIElement, Vanillas eigenes Lua): drawRect(x, y, w, h, a, r, g, b) V:client/ISUI/ISUIElement.lua:1191
-- (Aufrufer ISButton.lua:128), drawRectBorder(x, y, w, h, a, r, g, b) :1219 (ISButton.lua:141), drawText(text, x, y, r, g, b, a,
-- Schrift) :1293 (V:client/ISUI/Animal/ISAnimalUI.lua:58), drawTextRight :1306 (ISAnimalUI.lua:64), drawTextCentre :1280
-- (V:client/ISUI/ISToolTip.lua:120), drawTextureScaled(tex, x, y, w, h, a, r, g, b) :1032 (V:client/Chat/ISChat.lua:418).
-- Kein Engine-Aufruf ohne Vanilla-Fundstelle. Statisch geprueft, nicht gespielt.
--

require "ISUI/ISButton"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- ---------------------------------------------------------------------------
-- Farben (PLAN_F1.md 1.3), r, g, b, a in 0..1. Werte wie im Entwurf f1_entwurf/zeichne_fenster.py.
-- ---------------------------------------------------------------------------
local COL = {
    winBg = { 0.075, 0.070, 0.065, 0.95 }, winBorder = { 0.55, 0.38, 0.16, 0.85 }, accent = { 1.00, 0.62, 0.18, 1 },
    cardBg = { 0.115, 0.105, 0.095, 1 }, cardBorder = { 0.20, 0.18, 0.16, 1 }, divider = { 1, 1, 1, 0.08 },
    title = { 1.00, 0.70, 0.30, 1 }, name = { 0.99, 0.93, 0.80, 1 }, text = { 0.93, 0.90, 0.85, 1 },
    text2 = { 0.70, 0.66, 0.60, 1 }, dim = { 0.50, 0.47, 0.43, 1 }, honeyText = { 1.00, 0.72, 0.32, 1 },
    track = { 0.20, 0.18, 0.16, 1 }, trackBorder = { 0, 0, 0, 0.35 }, barHi = { 1, 1, 1, 0.18 },
    pipGold = { 1.00, 0.86, 0.40, 1 }, pipNow = { 1.00, 0.62, 0.18, 1 }, pipEmpty = { 0.22, 0.20, 0.18, 1 },
    pipEdge = { 0.30, 0.28, 0.25, 1 },
    btnBg = { 0.15, 0.14, 0.125, 1 }, btnBorder = { 0.34, 0.30, 0.25, 1 }, btnText = { 0.92, 0.89, 0.84, 1 },
    btnHoverBg = { 0.22, 0.20, 0.17, 1 }, btnHoverBorder = { 0.62, 0.46, 0.24, 1 },
    btnActBg = { 0.40, 0.23, 0.07, 1 }, btnActText = { 1.00, 0.93, 0.78, 1 },
    btnOffBg = { 0.10, 0.095, 0.09, 1 }, btnOffBorder = { 0.20, 0.19, 0.17, 1 }, btnOffText = { 0.45, 0.42, 0.39, 1 },
    checkBg = { 0.10, 0.09, 0.085, 1 }, checkEdge = { 0.55, 0.50, 0.44, 1 },
    closeBg = { 0.18, 0.16, 0.14, 1 }, closeHover = { 0.30, 0.26, 0.22, 1 }, rowHover = { 1, 1, 1, 0.05 },
    iconDisc = { 0.24, 0.16, 0.08, 1 },
    -- Zustand-Farben des Chips (PLAN_F1.md 1.3 "Zustand-Farbe sc", 1.4)
    stFollow = { 0.45, 0.78, 0.40, 1 }, stCome = { 0.45, 0.78, 0.40, 1 }, stStay = { 0.95, 0.70, 0.30, 1 },
    stSit = { 0.95, 0.70, 0.30, 1 }, stRoam = { 0.40, 0.75, 0.80, 1 }, stHide = { 0.95, 0.42, 0.30, 1 },
    stRide = { 0.45, 0.62, 0.95, 1 }, stMissing = { 0.90, 0.30, 0.25, 1 }, stAway = { 0.60, 0.58, 0.55, 1 },
}
U.WIN_COL = COL

-- Farbe nach Name: r, g, b, a. Unbekannter Name -> weiss (nie nil, damit kein Zeichenaufruf mit nil laeuft).
function U.WinColor(key)
    local c = COL[key]
    if c == nil then return 1, 1, 1, 1 end
    return c[1], c[2], c[3], c[4] or 1
end

-- Farbverlauf nach Wert v (0..1), PLAN_F1.md 1.3: Leben gruen ab 0,6, gelb bei 0,3, rot bei 0; Ausdauer blau ab 0,35, orange bei 0.
-- Stuetzpunkte { x, r, g, b }, dazwischen gerade gemischt (Form wie Vanillas Mischung V:client/XpSystem/ISUI/ISSkillProgressBar.lua:150-160).
local RAMP = {
    hp = { { 0, 0.82, 0.26, 0.20 }, { 0.3, 0.95, 0.66, 0.20 }, { 0.6, 0.45, 0.76, 0.32 }, { 1, 0.45, 0.76, 0.32 } },
    sta = { { 0, 0.90, 0.50, 0.20 }, { 0.35, 0.38, 0.64, 0.92 }, { 1, 0.38, 0.64, 0.92 } },
}

function U.WinRamp(kind, v)
    local r = RAMP[kind] or RAMP.hp
    v = tonumber(v) or 0
    if v ~= v or v < 0 then v = 0 end
    if v > 1 then v = 1 end
    for i = 2, #r do
        local a, b = r[i - 1], r[i]
        if v <= b[1] then
            local t = 0
            if b[1] > a[1] then t = (v - a[1]) / (b[1] - a[1]) end
            return a[2] + (b[2] - a[2]) * t, a[3] + (b[3] - a[3]) * t, a[4] + (b[4] - a[4]) * t
        end
    end
    local e = r[#r]
    return e[2], e[3], e[4]
end

-- ---------------------------------------------------------------------------
-- Schriftwahl (PLAN_F1.md 1.2, wie pick_fonts im Entwurf-Skript). f = Faktor des Fensters (1080 -> 1,0, Kevins 2054 -> 2,0).
-- Hoehe je Schrift: getTextManager():getFontHeight(UIFont.Small) V:client/ISUI/Animal/ISAnimalUI.lua:4, UIFont.Medium
-- V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8, UIFont.Large V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6.
-- Rueckgabe: Schrift Name, Text, Klein und ihre Hoehen. Nur beim Legen (nie je Bild).
-- ---------------------------------------------------------------------------
local NAME_T, BODY_T, SMALL_T = 29, 19, 15   -- Ziel-Zeilenhoehen bei f = 1
local LOWER_OK = 0.75                         -- eine Stufe kleiner nur, solange die kleinere Schrift >= 0,75 x ihres Ziels ist

function U.WinFonts(f)
    f = tonumber(f) or 1
    local fonts = { UIFont.Small, UIFont.Medium, UIFont.Large }
    local tm = getTextManager()                         -- V:client/ISUI/Animal/ISAnimalUI.lua:4
    local h = {}
    for i = 1, 3 do
        local v = tm:getFontHeight(fonts[i])
        if type(v) ~= "number" or v <= 0 then v = 19 * i end
        h[i] = v
    end
    local function pick(target, cap)
        local best = 1
        for i = 1, cap do
            if h[i] <= target * 1.1 then best = i end
        end
        return best
    end
    local n = pick(NAME_T * f, 3)
    local b = pick(BODY_T * f, n)
    if b == n and n > 1 and h[n - 1] >= LOWER_OK * BODY_T * f then b = n - 1 end
    local s = pick(SMALL_T * f, b)
    if s == b and b > 1 and h[b - 1] >= LOWER_OK * SMALL_T * f then s = b - 1 end
    return fonts[n], fonts[b], fonts[s], h[n], h[b], h[s]
end

-- ---------------------------------------------------------------------------
-- Kleine Zeichen-Helfer (je Aufruf nur Rechnen und drawRect / drawRectBorder)
-- ---------------------------------------------------------------------------

-- Rahmen der Dicke t (t ineinander liegende 1-px-Rahmen; drawRectBorder zeichnet 1 px, ISUIElement.lua:1219).
local function frame(el, x, y, w, h, t, c, aMul)
    local a = c[4] * (aMul or 1)
    for i = 0, t - 1 do
        el:drawRectBorder(x + i, y + i, w - 2 * i, h - 2 * i, a, c[1], c[2], c[3])
    end
end
U.WinFrame = frame

local function rect(el, x, y, w, h, c, mul)
    local m = mul or 1
    el:drawRect(x, y, w, h, c[4], c[1] * m, c[2] * m, c[3] * m)
end
U.WinRect = rect

-- ---------------------------------------------------------------------------
-- Befehls-Knopf (PLAN_F1.md 1.3 Knopf normal / Maus darueber / aktiv / grau / gedrueckt, 7.7)
-- Felder (setzt das Fenster): win (Fenster, traegt die Masse m), label (fertiger Text), state ("normal" / "active" / "off"),
-- style ("cmd" = Befehl, sonst klein: Umbenennen, Pfeile), font / fh (Schrift und ihre Hoehe), cmd (Befehl beim Klick).
-- enable = (state ~= "off"): ISButton:onMouseUp klickt nur bei enable (V:client/ISUI/ISButton.lua:45).
-- ---------------------------------------------------------------------------
local Btn = ISButton:derive("BanditsNPCBearWinBtn")
U.WinBtn = Btn

function Btn:prerender()
    local m = self.win and self.win.m
    local t = (m and m.t) or 1
    local w, h = self.width, self.height
    local st = self.state
    local bg, bd = COL.btnBg, COL.btnBorder
    if st == "off" then
        bg, bd = COL.btnOffBg, COL.btnOffBorder
    elseif st == "active" then
        bg, bd = COL.btnActBg, COL.accent
    elseif self.mouseOver then                          -- mouseOver: ISButton.lua:18-20 / :22-23
        bg, bd = COL.btnHoverBg, COL.btnHoverBorder
    end
    local mul = 1
    if self.pressed and self.enable then mul = 0.8 end  -- pressed: ISButton.lua:59 / :41
    rect(self, 0, 0, w, h, bg, mul)
    frame(self, 0, 0, w, h, t, bd)
    if st == "active" and self.style == "cmd" then
        frame(self, t, t, w - 2 * t, h - 2 * t, t, COL.accent, 0.45)
        rect(self, t, t, (m and m.bar) or 4, h - 2 * t, COL.accent)
    end
    ISButton.updateTooltip(self)                        -- ISButton.lua:176, :316-346
end

function Btn:render()
    local label = self.label
    if label == nil or label == "" then return end
    local c = COL.btnText
    if self.style ~= "cmd" then c = COL.text2 end
    if self.state == "off" then
        c = COL.btnOffText
    elseif self.state == "active" then
        c = COL.btnActText
    end
    local fh = self.fh or 0
    self:drawTextCentre(label, self.width / 2, math.floor((self.height - fh) / 2), c[1], c[2], c[3], c[4], self.font or UIFont.Small)
end

-- ---------------------------------------------------------------------------
-- Zeile mit Tooltip (PLAN_F1.md 1.1 Karten, 1.5). Felder: win, kind ("bar" / "val" / "later" / "skill"), key ("hp" / "sta" bzw.
-- Faehigkeit 1..6). Inhalt aus dem Modell des Fensters (win.model), Masse aus win.m. Innenrand ox = 8 x f, oy = 3 x f (die Zeile
-- liegt 4 x f im Kartenrand und 3 x f ueber dem Text, so passt die Hervorhebung beim Ueberfahren).
-- ---------------------------------------------------------------------------
local Row = ISButton:derive("BanditsNPCBearWinRow")
U.WinRow = Row

local function drawBar(self, m, e)
    local ox, oy = m.ox, m.oy
    local tc = COL.text
    self:drawText(e.label or "", ox, oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    self:drawTextRight(e.val or "", self.width - ox, oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    if e.frac == nil then return end                    -- Wert fehlt: "--" ohne Balken (PLAN_F1.md 1.5), nie ein leerer Balken
    local by = oy + m.lb + m.R4
    local bw = self.width - 2 * ox
    local bh = m.R10
    rect(self, ox, by, bw, bh, COL.track)
    local fill = math.floor(bw * e.frac + 0.5)
    if fill > 0 then
        self:drawRect(ox, by, fill, bh, 1, e.r or 1, e.g or 1, e.b or 1)
        rect(self, ox, by, fill, m.t, COL.barHi)
    end
    frame(self, ox, by, bw, bh, m.t, COL.trackBorder)
end

local function drawVal(self, m, e)
    local tc = COL.text
    self:drawText(e.label or "", m.ox, m.oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    self:drawTextRight(e.val or "", self.width - m.ox, m.oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
end

-- "Kommt spaeter": Etikett und 2 x 2 Raster, nur in dim, KEIN Balken (PLAN_F1.md 1.5).
local function drawLater(self, m, d)
    local c = COL.dim
    self:drawText(d.tLater or "", m.ox, m.oy, c[1], c[2], c[3], c[4], m.fSmall)
    local words = d.needs
    if type(words) ~= "table" then return end
    local half = math.floor((self.width - 2 * m.ox) / 2)
    local y0 = m.oy + m.ls + m.R6
    for i = 1, 4 do
        local gx = m.ox + ((i - 1) % 2) * half
        local gy = y0 + math.floor((i - 1) / 2) * (m.ls + m.R6)
        if m.disc then
            self:drawTextureScaled(m.disc, gx, gy + math.floor((m.ls - m.R6) / 2), m.R6, m.R6, 1, c[1], c[2], c[3])
        end
        self:drawText(words[i] or "", gx + m.R12, gy, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

-- Faehigkeit: Name links, rechts "Lv n" und Prozent, darunter 10 Segmente (Gold = erreicht, Honig = laufende Stufe anteilig, Rest
-- dunkel mit Rand). Vorbild Vanillas Faehigkeiten-Leiste (V:client/XpSystem/ISUI/ISSkillProgressBar.lua:128-210, Gold :13-16).
local function drawSkill(self, m, s)
    local ox, oy = m.ox, m.oy
    local tc = COL.text
    self:drawText(s.name or "", ox, oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    local right = self.width - ox
    local c2 = COL.text2
    self:drawTextRight(s.pctTxt or "", right, oy + m.lb - m.ls, c2[1], c2[2], c2[3], c2[4], m.fSmall)
    local lc = COL.honeyText
    if (s.lv or 0) <= 0 then lc = COL.dim end
    self:drawTextRight(s.lvTxt or "", right - (s.pctW or 0) - m.R8, oy, lc[1], lc[2], lc[3], lc[4], m.fBody)
    local sy = oy + m.lb + m.R4
    local gap = m.R3
    local span = self.width - 2 * ox
    local segW = (span - 9 * gap) / 10
    local L = s.lv or 0
    for k = 0, 9 do
        local x0 = math.floor(ox + k * (segW + gap) + 0.5)
        local x1 = math.floor(ox + k * (segW + gap) + segW + 0.5)
        local sw = x1 - x0
        if s.known and k < L then
            rect(self, x0, sy, sw, m.R8, COL.pipGold)
        else
            rect(self, x0, sy, sw, m.R8, COL.pipEmpty)
            if s.known and k == L and L < 10 then
                local fw = math.floor(sw * (s.frac or 0) + 0.5)
                if fw > 0 then rect(self, x0, sy, fw, m.R8, COL.pipNow) end
            end
            frame(self, x0, sy, sw, m.R8, m.t, COL.pipEdge)
        end
    end
end

function Row:prerender()
    local win = self.win
    local m = win and win.m
    local d = win and win.model
    if m and d then
        if self.mouseOver then rect(self, 0, 0, self.width, self.height, COL.rowHover) end
        local kind = self.kind
        if kind == "bar" then
            local e = d[self.key]
            if e then drawBar(self, m, e) end
        elseif kind == "val" then
            local e = d[self.key]
            if e then drawVal(self, m, e) end
        elseif kind == "later" then
            drawLater(self, m, d)
        elseif kind == "skill" then
            local s = d.skills and d.skills[self.key]
            if s then drawSkill(self, m, s) end
        end
    end
    ISButton.updateTooltip(self)                        -- ISButton.lua:176, :316-346
end

-- Kein Titel, kein Bild: nichts zu zeichnen (ISButton:render wuerde nur den leeren Titel messen).
function Row:render()
end

-- ---------------------------------------------------------------------------
-- Schalter (PLAN_F1.md 1.3 "Schalter-Kaestchen" 16 x 16, an: Innenquadrat accent). Felder: win, label, on, cmd.
-- ---------------------------------------------------------------------------
local Tick = ISButton:derive("BanditsNPCBearWinTick")
U.WinTick = Tick

function Tick:prerender()
    local m = self.win and self.win.m
    if m then
        local w, h = self.width, self.height
        local bd = COL.btnBorder
        if self.mouseOver then bd = COL.btnHoverBorder end
        local mul = 1
        if self.pressed then mul = 0.8 end
        rect(self, 0, 0, w, h, COL.btnBg, mul)
        frame(self, 0, 0, w, h, m.t, bd)
        local box = m.R16
        local bx = m.R10
        local by = math.floor((h - box) / 2)
        rect(self, bx, by, box, box, COL.checkBg)
        frame(self, bx, by, box, box, m.t, COL.checkEdge)
        if self.on then
            rect(self, bx + m.R3, by + m.R3, box - 2 * m.R3, box - 2 * m.R3, COL.accent)
        end
    end
    ISButton.updateTooltip(self)                        -- ISButton.lua:176, :316-346
end

function Tick:render()
    local m = self.win and self.win.m
    if not m then return end
    local c = COL.text2
    if self.on then c = COL.text end
    self:drawText(self.label or "", m.R10 + m.R16 + m.R10, math.floor((self.height - m.lb) / 2), c[1], c[2], c[3], c[4], m.fBody)
end
