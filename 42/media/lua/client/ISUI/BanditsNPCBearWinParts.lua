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
-- F2 = B5a (PLAN_F2.md 3.2, Nachtrag 11.4): Chip-Farben fuer "am Boden" (rot), "kaempft" (orange), "zieht sich zurueck / verschnauft"
-- (gelb); am Leben-Balken ein kleines Verband-Zeichen (gruenes Kreuz aus zwei Rechtecken) vor dem Wert, solange ein Verband wirkt; eine
-- Faehigkeit am Alters-Deckel ist AUSGEGRAUT (Segmente dunkler und entsaettigt, Stufe gedimmt) und rechts steht klein "max for its age"
-- (Kevin 12.11.2026 ~06:30: "oder der balken ist ausgegraut ... zusaetzlich"). Weiter nur Rechtecke und fertige Texte je Bild.
-- F3 (Lauf baer-f3, PLAN_F3.md 10.1; Kevin 13.11.2026: Fenster Variante B, "Hellblau"): Chip-Farbe stSleep = die EINE Schlaf-Farbe des
-- Kerns (B.CFG.sleepCol ueber U.SleepColor, client/BanditsNPCBearClient.lua -- dieselbe faerbt das z Z z und die Schild-Zeile
-- "sleeping"); Farbe warn (Fusszeile "zu muede zum Kaempfen" / "weigert sich zu kaempfen"); Verlaeufe "need" (Hunger / Durst / Muedigkeit
-- FUELLEN SICH MIT DEM DRUCK: leer = gruen, halb = gelb, ab 0,8 rot -- Lehre NPC Crew NC:client/ISUI/BanditsNPCDialogWindow.lua:6496-6497)
-- und "trust" (Vertrauen fuellt sich mit dem Guten, honig -> gold). Die vier Beduerfnis-Balken zeichnet der vorhandene drawBar. Der
-- Schalter U.WinTick kennt jetzt state "off" (grau, kein Klick: Platzhalter "Nose alerts" bis F5). Die Zeilenart "later" (Raster
-- "Coming later") ist weg -- die Beduerfnisse sind echte Zeilen.
-- F4 (Lauf baer-f4, PLAN_F4.md 8.1): eine Wert-Zeile kann ihren Wert in einer Farbe der Tabelle zeigen (e.col, z. B. "warn" fuer "Load" ueber
-- der Grenze); die Bausteine benutzt auch das Inventar-Fenster (client/ISUI/BanditsNPCBearInvWindow.lua).
-- K1 (Lauf baer-k1, PLAN_K1.md 2.3, 4 X; Kevin 13.11.2026 ~21:40 "bei negativ halt in einer negativen farbe und positiv eine positive = gruen ;D
-- und negativ rot", 14.11. ~00:20 "die damage zahl soll rot werden"): Vertrauens-Balken und -Zahl nach Ton (e.tone "pos" gruen / "neg" rot /
-- "zero" grau, U.WinTrustColor), Farbe "bad" (roter Wert: Schaden geschwaecht). Weiter nur Rechtecke und fertige Texte je Bild.
-- Lauf baer-talente (PLAN_TALENTE.md 5.1): Knopf-Stil "tab" (Reiter "Overview" / "Perks": gewaehlt = Kartengrund mit accent-Rahmen, Text in
-- Titelfarbe; Abzeichen mit der Zahl freier Talentpunkte als Honig-Kaestchen) und Farben fuer die Kacheln (client/ISUI/BanditsNPCBearTalentTab.lua).
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
    -- F2 (PLAN_F2.md 3.2): am Boden / kaempft / zieht sich zurueck oder verschnauft
    stDown = { 0.90, 0.30, 0.25, 1 }, stFight = { 1.00, 0.45, 0.15, 1 }, stBack = { 0.95, 0.70, 0.30, 1 },
    -- F2: Verband-Zeichen am Leben-Wert; Faehigkeit am Alters-Deckel (11.4) -- Segmente ausgegraut
    bandage = { 0.55, 0.85, 0.55, 1 }, pipCapGold = { 0.46, 0.43, 0.36, 1 }, pipCapNow = { 0.42, 0.36, 0.28, 1 },
    pipCapEmpty = { 0.15, 0.14, 0.13, 1 },
    -- F3: Chip "Sleeping" (Rueckfall; unten aus der EINEN Schlaf-Farbe des Kerns gesetzt) und Warnfarbe der Fusszeile
    stSleep = { 0.70, 0.85, 1.00, 1 }, warn = { 1.00, 0.58, 0.28, 1 },
    -- F4 Nachbesserung (Befund P2): ueber der Traglast -- kraeftiger als die Warnfarbe (der schlimmere Zustand darf nicht harmloser aussehen)
    over = { 0.92, 0.27, 0.20, 1 },
    -- K1: geschwaechter Schaden (rot wie "over"); Vertrauen: Balken gruen / rot / grau und die Zahl daneben in derselben Farbe (heller)
    bad = { 0.95, 0.36, 0.28, 1 },
    trustPos = { 0.45, 0.80, 0.35, 1 }, trustNeg = { 0.88, 0.25, 0.20, 1 }, trustZero = { 0.55, 0.53, 0.50, 1 },
    trustPosText = { 0.62, 0.92, 0.52, 1 }, trustNegText = { 1.00, 0.55, 0.48, 1 }, trustZeroText = { 0.78, 0.76, 0.72, 1 },
    -- Nachbesserung K1 P4 / P3: bei negativem Vertrauen ist auch der LEERE Teil dunkelrot (-100 = leer, aber rot -- Kevin "negativ rot");
    -- ein 1-Strich-Mittelzeichen bei 0 macht den Balken als -100..+100 kenntlich (der Lebensbalken hat keins)
    trustNegTrack = { 0.36, 0.11, 0.09, 1 }, trustMid = { 0.92, 0.90, 0.84, 0.85 },
    -- Lauf baer-talente (PLAN_TALENTE.md 5.1/5.2): Reiter (aktiv = Kartengrund mit accent-Rahmen), Abzeichen freie Punkte (Honig mit dunkler
    -- Zahl), Kachel aktiv (warmer Grund) und waehlbar (Honigrahmen); gesperrt nimmt btnOff*
    tabOnBg = { 0.115, 0.105, 0.095, 1 }, badgeBg = { 1.00, 0.72, 0.32, 1 }, badgeText = { 0.10, 0.06, 0.02, 1 },
    talOnBg = { 0.30, 0.18, 0.06, 1 }, talFreeBorder = { 0.80, 0.58, 0.26, 1 },
}
U.WIN_COL = COL
-- F3 (PLAN_F3.md 8, 10.1): die Schlaf-Farbe steht an EINER Stelle (B.CFG.sleepCol des Kerns, gelesen ueber U.SleepColor). Einmal beim
-- Laden dieser Datei (shared und client/BanditsNPCBearClient.lua laden vorher); fehlt der Helfer, bleibt der Rueckfall oben.
if U.SleepColor then
    local sr, sg, sb = U.SleepColor()
    COL.stSleep = { sr, sg, sb, 1 }
end

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
    -- F3: ein Beduerfnis fuellt sich mit dem Druck (0 = satt / ausgeruht gruen, 0,5 gelb, ab 0,8 rot); Vertrauen honig, voll = gold
    need = { { 0, 0.45, 0.76, 0.32 }, { 0.5, 0.95, 0.66, 0.20 }, { 0.8, 0.82, 0.26, 0.20 }, { 1, 0.82, 0.26, 0.20 } },
    trust = { { 0, 0.62, 0.42, 0.20 }, { 1, 1.00, 0.78, 0.30 } },
    -- F4 Nachbesserung (Befund P2): Traglast gruen bis 0,6, gelb bei 0,85, voll orange (= warn); UEBER der Grenze zeichnet das Fenster "over" (rot)
    load = { { 0, 0.45, 0.76, 0.32 }, { 0.6, 0.45, 0.76, 0.32 }, { 0.85, 0.95, 0.66, 0.20 }, { 1, 1.00, 0.58, 0.28 } },
}

-- K1: Farbe des Vertrauens-Balkens nach Ton ("pos" / "neg" / "zero"): r, g, b. Unbekannt -> grau.
local TRUST_BAR = { pos = "trustPos", neg = "trustNeg", zero = "trustZero" }
local TRUST_TEXT = { pos = "trustPosText", neg = "trustNegText", zero = "trustZeroText" }
function U.WinTrustColor(tone)
    local c = COL[TRUST_BAR[tone] or "trustZero"]
    return c[1], c[2], c[3]
end

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
    if self.style == "tab" and st == "active" then
        bg, bd = COL.tabOnBg, COL.accent                -- Lauf baer-talente: gewaehlter Reiter
    elseif st == "off" then
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
    if self.style == "tab" then
        -- Lauf baer-talente: Reiter -- gewaehlt in Titelfarbe; mit Abzeichen (freie Talentpunkte) Text + Honig-Kaestchen mittig. labelW / badgeW
        -- setzt das Fenster beim Legen bzw. im 1-s-Takt (kein MeasureStringX je Bild).
        c = COL.text2
        if self.state == "active" then c = COL.title elseif self.mouseOver then c = COL.text end
        local m = self.win and self.win.m
        if self.badge and self.labelW and self.badgeW and m then
            local x0 = math.floor((self.width - self.labelW - m.R6 - self.badgeW) / 2)
            local ty = math.floor((self.height - fh) / 2)
            self:drawText(label, x0, ty, c[1], c[2], c[3], c[4], self.font or UIFont.Small)
            local bx, bh = x0 + self.labelW + m.R6, m.ls + m.R2
            local by = math.floor((self.height - bh) / 2)
            rect(self, bx, by, self.badgeW, bh, COL.badgeBg)
            local bc = COL.badgeText
            self:drawTextCentre(self.badge, bx + self.badgeW / 2, by + math.floor((bh - m.ls) / 2), bc[1], bc[2], bc[3], bc[4], m.fSmall)
            return
        end
    end
    self:drawTextCentre(label, self.width / 2, math.floor((self.height - fh) / 2), c[1], c[2], c[3], c[4], self.font or UIFont.Small)
end

-- ---------------------------------------------------------------------------
-- Zeile mit Tooltip (PLAN_F1.md 1.1 Karten, 1.5). Felder: win, kind ("bar" / "val" / "skill"), key ("hp" / "sta" / F3: "hun" / "thr" /
-- "tir" / "tru" bzw. Faehigkeit 1..6). Inhalt aus dem Modell des Fensters (win.model), Masse aus win.m. Innenrand ox = 8 x f, oy = 3 x f (die Zeile
-- liegt 4 x f im Kartenrand und 3 x f ueber dem Text, so passt die Hervorhebung beim Ueberfahren).
-- ---------------------------------------------------------------------------
local Row = ISButton:derive("BanditsNPCBearWinRow")
U.WinRow = Row

local function drawBar(self, m, e)
    local ox, oy = m.ox, m.oy
    local tc = COL.text
    self:drawText(e.label or "", ox, oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    local vc = tc
    if e.tone and TRUST_TEXT[e.tone] then vc = COL[TRUST_TEXT[e.tone]] end     -- K1: Vertrauens-Zahl in der Farbe ihres Balkens
    self:drawTextRight(e.val or "", self.width - ox, oy, vc[1], vc[2], vc[3], vc[4], m.fBody)
    if e.bnd and e.valW then
        -- F2: Verband-Zeichen (Kreuz, Kantenlaenge = halbe Textzeile) links vor dem Wert; valW misst das Fenster im 1-s-Takt
        local sz = math.floor(m.lb / 2)
        local th = math.max(m.t, math.floor(sz / 3))
        local cx = self.width - ox - e.valW - m.R8 - sz
        local cy = oy + math.floor((m.lb - sz) / 2)
        rect(self, cx, cy + math.floor((sz - th) / 2), sz, th, COL.bandage)
        rect(self, cx + math.floor((sz - th) / 2), cy, th, sz, COL.bandage)
    end
    if e.frac == nil then return end                    -- Wert fehlt: "--" ohne Balken (PLAN_F1.md 1.5), nie ein leerer Balken
    local by = oy + m.lb + m.R4
    local bw = self.width - 2 * ox
    local bh = m.R10
    rect(self, ox, by, bw, bh, (e.tone == "neg") and COL.trustNegTrack or COL.track)      -- Nachbesserung K1 P4
    local fill = math.floor(bw * e.frac + 0.5)
    if fill > 0 then
        self:drawRect(ox, by, fill, bh, 1, e.r or 1, e.g or 1, e.b or 1)
        rect(self, ox, by, fill, m.t, COL.barHi)
    end
    if e.tone then rect(self, ox + math.floor(bw / 2), by, m.t, bh, COL.trustMid) end   -- Nachbesserung K1 P3: Mitte = 0
    frame(self, ox, by, bw, bh, m.t, COL.trackBorder)
end

local function drawVal(self, m, e)
    local tc = COL.text
    self:drawText(e.label or "", m.ox, m.oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    local vc = tc
    if e.col and COL[e.col] then vc = COL[e.col] end            -- F4: "Load" ueber der Grenze in Warnfarbe (e.col = "warn")
    self:drawTextRight(e.val or "", self.width - m.ox, m.oy, vc[1], vc[2], vc[3], vc[4], m.fBody)
end


-- Faehigkeit: Name links, rechts "Lv n" und Prozent, darunter 10 Segmente (Gold = erreicht, Honig = laufende Stufe anteilig, Rest
-- dunkel mit Rand). Vorbild Vanillas Faehigkeiten-Leiste (V:client/XpSystem/ISUI/ISSkillProgressBar.lua:128-210, Gold :13-16).
local function drawSkill(self, m, s)
    local ox, oy = m.ox, m.oy
    local tc = COL.text
    self:drawText(s.name or "", ox, oy, tc[1], tc[2], tc[3], tc[4], m.fBody)
    local right = self.width - ox
    local c2 = COL.text2
    if s.capped then c2 = COL.dim end                           -- F2 (11.4): "max for its age" klein und ruhig
    self:drawTextRight(s.pctTxt or "", right, oy + m.lb - m.ls, c2[1], c2[2], c2[3], c2[4], m.fSmall)
    local lc = COL.honeyText
    if (s.lv or 0) <= 0 or s.capped then lc = COL.dim end       -- F2 (11.4): Stufe gedimmt
    self:drawTextRight(s.lvTxt or "", right - (s.pctW or 0) - m.R8, oy, lc[1], lc[2], lc[3], lc[4], m.fBody)
    local gold, now, empty = COL.pipGold, COL.pipNow, COL.pipEmpty
    if s.capped then gold, now, empty = COL.pipCapGold, COL.pipCapNow, COL.pipCapEmpty end
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
            rect(self, x0, sy, sw, m.R8, gold)
        else
            rect(self, x0, sy, sw, m.R8, empty)
            if s.known and k == L and L < 10 then
                local fw = math.floor(sw * (s.frac or 0) + 0.5)
                if fw > 0 then rect(self, x0, sy, fw, m.R8, now) end
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
-- F3 (PLAN_F3.md 10.2): state "off" = grauer Platzhalter mit Grund im Tooltip (wie ein grauer Knopf; kein Klick, weil das Fenster
-- enable = false setzt, V:client/ISUI/ISButton.lua:45) -- "Nose alerts" steht so schon an seinem Platz, F5 schaltet es nur scharf.
-- ---------------------------------------------------------------------------
local Tick = ISButton:derive("BanditsNPCBearWinTick")
U.WinTick = Tick

function Tick:prerender()
    local m = self.win and self.win.m
    if m then
        local w, h = self.width, self.height
        local off = (self.state == "off")
        local bg, bd, edge = COL.btnBg, COL.btnBorder, COL.checkEdge
        if off then
            bg, bd, edge = COL.btnOffBg, COL.btnOffBorder, COL.btnOffBorder
        elseif self.mouseOver then
            bd = COL.btnHoverBorder
        end
        local mul = 1
        if self.pressed and not off then mul = 0.8 end
        rect(self, 0, 0, w, h, bg, mul)
        frame(self, 0, 0, w, h, m.t, bd)
        local box = m.R16
        local bx = m.R10
        local by = math.floor((h - box) / 2)
        rect(self, bx, by, box, box, COL.checkBg)
        frame(self, bx, by, box, box, m.t, edge)
        if self.on and not off then
            rect(self, bx + m.R3, by + m.R3, box - 2 * m.R3, box - 2 * m.R3, COL.accent)
        end
    end
    ISButton.updateTooltip(self)                        -- ISButton.lua:176, :316-346
end

function Tick:render()
    local m = self.win and self.win.m
    if not m then return end
    local c = COL.text2
    if self.state == "off" then
        c = COL.btnOffText
    elseif self.on then
        c = COL.text
    end
    self:drawText(self.label or "", m.R10 + m.R16 + m.R10, math.floor((self.height - m.lb) / 2), c[1], c[2], c[3], c[4], m.fBody)
end
