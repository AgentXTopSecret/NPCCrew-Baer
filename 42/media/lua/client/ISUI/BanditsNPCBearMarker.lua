--
-- NPC Crew -- Baer, Bildschirm-Markierung oben (B1c, PLAN_B1C.md 1.7, 4.3; B1e, PLAN_B1E.md 1.7, 6.5, 6.6 -- neu geschrieben).
--
-- Ein Kreis mit Pfeil oben am Bildschirm zeigt auf das WILDE Junge des Spielers (aus dem Wald oder vom Koeder), solange es noch
-- nicht entdeckt ist ("new") und noch eine Weile nach dem Entdecken (B.CFG.markerAfterMs, Vorgabe 60 s ab dem ersten "shy", das
-- dieser Client sieht). Weg ist er, sobald das Junge angefuettert/gezaehmt ist (B.View.me.wild faellt weg), der Eintrag fehlt, die
-- Lage fehlt oder die Frist um ist. Doppelklick blendet ihn fuer DIESES Junge aus; ein neues Junges bekommt wieder einen.
-- Aussehen wie bisher (Kevin: so lassen): Kreis Honig-Orange, Pfeil zum Jungen, Kevins Symbol, Text "Bear cub nearby".
--
-- B1e (Kevin 11.11.2026: "waer cooler wenn das symbol was groesser waere zumindestens bei 4k aufloesung"): bis B1d zeichnete Bandits
-- die Markierung in fester Groesse 96 px (B:client/BanditEventMarkers.lua:7, :174, :192-193). Jetzt ist sie ein EIGENES UI-Element
-- (PLAN_B1E.md 0.11, Weg A), nur mit Vanilla-UI-Aufrufen und eigenen Bildern (media/ui/BanditsNPCBearMarker_*.png,
-- BanditsNPCBearCub_marker288.png; nichts von Bandits kopiert). Die Groesse waechst mit der Bildschirmhoehe (Auto: 1080 = 100 %,
-- 2160 = 200 %, in Stufen 100/125/150/200/250/300 %) oder steht fest (Optionen -> Mods -> "NPC Crew: Bear" -> MarkerSize). Stufen,
-- weil DrawTextureAngle den Pfeil immer in Bildgroesse zeichnet (NUR JAR, forschung_b1e.md 8) -- ein Pfeil-Bild je Stufe.
-- Folge: die Markierung erscheint jetzt auch OHNE Bandits (Frage F11). Bandits wird nur noch GELESEN, je hinter einem Riegel:
-- die gemerkte Bildschirmstelle (player:getModData()["BanditEventMarkerPlacement"]) und fremde sichtbare Marker zum Ausweichen.
--
-- Takt: Events.OnTick (V:client/Chat/ISChat.lua:943), gedrosselt auf B.CFG.markerMs (400 ms): Ziel, Richtung, Abstand, Sichtbarkeit.
-- Je Bild (nur wenn sichtbar): 3 Bilder + 1 Text aus fertigen Feldern -- keine Tabelle, kein getText, keine Suche.
-- Genau EIN Element je Spielstart (OnGameStart: altes abmelden, neues anlegen). Mehrspieler: alles aus der Sicht DIESES Clients
-- (B.View), nur Spieler 1 (getSpecificPlayer(0)), wie bisher.
-- Kein pcall: alles Vanilla-Lua; Bandits-Felder werden mit type/tonumber geprueft.
-- Statisch geprueft, nicht gespielt.
--

require "ISUI/ISUIElement"                              -- wie V:client/Chat/ISAlert.lua:1

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Eigenes Element (Klasse bleibt ein Local). ISUIElement:derive: V:client/Chat/ISAlert.lua:3.
local Mk = ISUIElement:derive("BanditsNPCBearMarkerUI")

local KEEP_MAX = 16         -- Deckel der Merk-Tabellen (shyAt, gone); voll -> geleert
local BASE_PX = 96          -- Kreis und Symbol bei 100 % (wie Bandits' iconSize, B:client/BanditEventMarkers.lua:7)
local CLICK_PX = 45         -- Klickflaeche bei 100 % (wie Bandits' clickableSize, :8)
local TEXT_DY = 25          -- Text unter der Kreismitte bei 100 % (wie Bandits, :176)
local REF_H = 1080          -- Bildschirmhoehe fuer 100 % (Auto)
local STEPS = { 1.0, 1.25, 1.5, 2.0, 2.5, 3.0 }        -- Groessen-Stufen; Option MarkerSize Index 2..7 = Stufe 1..6, Index 1 = Auto
local ARROW_FILES = {
    "media/ui/BanditsNPCBearMarker_arrow096.png", "media/ui/BanditsNPCBearMarker_arrow120.png",
    "media/ui/BanditsNPCBearMarker_arrow144.png", "media/ui/BanditsNPCBearMarker_arrow192.png",
    "media/ui/BanditsNPCBearMarker_arrow240.png", "media/ui/BanditsNPCBearMarker_arrow288.png",
}
local DISC_FILE = "media/ui/BanditsNPCBearMarker_disc.png"
local RING_FILE = "media/ui/BanditsNPCBearMarker_ring.png"
local ICON_FILE = "media/ui/BanditsNPCBearCub_marker288.png"

-- Stellwerte aus B.CFG (KERN, PLAN_B1E.md 5) mit eigenem Rueckfall.
local function cfg(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Alles, was die Markierung sich merkt (nur diese Sitzung, nie gespeichert, nie gesendet).
local M = {
    at = 0,         -- ms, letzter Takt
    shown = false,  -- Element sichtbar
    cid = nil,      -- Kennung des Jungen, auf das die Markierung zeigt
    el = nil,       -- unser Element (genau eins)
    idx = nil,      -- Optionswert MarkerSize, mit dem zuletzt gelegt wurde
    text = nil,     -- Text, einmal je Sitzung gebaut
    tex = nil,      -- Bilder dieser Sitzung (einmal geholt)
    shyAt = {}, shyN = 0,   -- id -> ms: erstes "shy", das dieser Client sah
    gone = {}, goneN = 0,   -- id -> true: per Doppelklick ausgeblendet, fuer dieses Junge nicht wieder
}

local function wipe(t)
    local keys = {}
    for k, _ in pairs(t) do keys[#keys + 1] = k end
    for i = 1, #keys do t[keys[i]] = nil end
end

local function log(msg)
    local f = B.Log
    if f then f(msg) end
end

local function errLine(msg)
    local f = B.ErrEvery
    if f then f("marker", 600000, "marker: " .. msg) end
end

local function keep(t, field, id, value)
    if t[id] == nil then
        M[field] = M[field] + 1
        if M[field] > KEEP_MAX then
            wipe(t)
            M[field] = 1
        end
    end
    t[id] = value
end

-- ---------------------------------------------------------------------------
-- Groesse (rein, ohne Engine; PLAN_B1E.md 1.7.3, 6.5)
-- ---------------------------------------------------------------------------

-- Faktor f aus der Bildschirmhoehe h und dem Optionswert idx (Index der Auswahl): idx 2..7 -> feste Stufe 100 ... 300 %; sonst Auto =
-- die Stufe, die h / 1080 am naechsten liegt (geklemmt 1..3; Gleichstand -> die groessere). 1080 -> 1,0; 1440 -> 1,25; 2054 -> 2,0;
-- 2160 -> 2,0; 3240 -> 3,0. Gibt f und die Stufe k (1..6, waehlt das Pfeil-Bild).
function U.MarkerFactor(h, idx)
    local i = tonumber(idx)
    if i ~= nil then
        i = math.floor(i)
        if i >= 2 and i <= #STEPS + 1 then return STEPS[i - 1], i - 1 end
    end
    local r = (tonumber(h) or REF_H) / REF_H
    if r ~= r or r < STEPS[1] then r = STEPS[1] end
    if r > STEPS[#STEPS] then r = STEPS[#STEPS] end
    local best, bestD = 1, nil
    for k = 1, #STEPS do
        local d = math.abs(STEPS[k] - r)
        if bestD == nil or d <= bestD + 1e-9 then best, bestD = k, d end
    end
    return STEPS[best], best
end

-- ---------------------------------------------------------------------------
-- Das Element
-- ---------------------------------------------------------------------------

-- ISUIElement.new(self, x, y, w, h): V:client/ISUI/ISUISprite.lua:71, V:client/ISUI/Maps/ISMiniMap.lua:345. Felder nur Zahlen,
-- Wahrheitswerte, Bilder und der fertige Text.
function Mk:new(x, y, w, h)
    local o = ISUIElement.new(self, x, y, w, h)
    o.on = false        -- zeichnen?
    o.c = CLICK_PX / 2  -- Kreismitte relativ zum Element (x = y)
    o.s = BASE_PX       -- Kantenlaenge von Kreis und Symbol
    o.hs = BASE_PX / 2  -- halbe Kantenlaenge
    o.ty = TEXT_DY      -- Text unter der Mitte
    o.font = UIFont.Small
    o.ang = 0           -- Pfeil in Grad (Bandits-Ausrichtung)
    o.close = false     -- nah: Ring ohne Spitze statt Pfeil
    o.cr, o.cg, o.cb = 1.0, 0.52, 0.09
    o.disc, o.ring, o.icon, o.arrow = nil, nil, nil, nil
    o.text = nil
    return o
end

-- Je Bild, nur wenn sichtbar (der UIManager ruft render nur fuer sichtbare Elemente). Reihenfolge wie Bandits
-- (B:client/BanditEventMarkers.lua:174-193): Kreis, Text, Pfeil (bzw. Ring), Symbol.
-- drawTextureScaled(tex, x, y, w, h, a, r, g, b): V:client/Chat/ISChat.lua:418, V:client/DebugUIs/ISSpawnVehicleUI.lua:171;
-- drawTextCentre(text, x, y, r, g, b, a, Schrift): Small B:client/BanditEventMarkers.lua:176, Medium V:client/DebugUIs/StashDebug.lua:86,
-- Large V:client/Chat/ISAlert.lua:35; DrawTextureAngle(tex, mitteX, mitteY, Grad): V:client/Fishing/TensionUI.lua:21,
-- V:client/ISUI/Fireplace/ISKnob.lua:24 (zeichnet in Bildgroesse, Mitte relativ zum Element -- NUR JAR, forschung_b1e.md 8).
function Mk:render()
    if not self.on then return end
    local c, hs, s = self.c, self.hs, self.s
    if self.disc then
        self:drawTextureScaled(self.disc, c - hs, c - hs, s, s, 1, self.cr, self.cg, self.cb)
    end
    if self.text then
        self:drawTextCentre(self.text, c, c + self.ty, 1, 1, 1, 1, self.font)
    end
    if self.close then
        if self.ring then self:drawTextureScaled(self.ring, c - hs, c - hs, s, s, 1, 1, 1, 1) end
    elseif self.arrow then
        self:DrawTextureAngle(self.arrow, c, c, self.ang)
    end
    if self.icon then
        self:drawTextureScaled(self.icon, c - hs, c - hs, s, s, 1, 1, 1, 1)
    end
end

local function hide()
    if not M.shown then return end
    M.shown = false
    local el = M.el
    if el then
        el.on = false
        el:setVisible(false)                            -- V:client/ISUI/ISCollapsableWindow.lua:70
    end
end

-- Doppelklick: fuer DIESES Junge nicht wieder (Rueckruf der Engine, Form V:client/ISUI/ISButton.lua:66; wie Bandits
-- B:client/BanditEventMarkers.lua:19-21). Keine Ziehen-Funktion (Frage F7).
function Mk:onMouseDoubleClick(_x, _y)
    if M.cid ~= nil then
        keep(M.gone, "goneN", M.cid, true)
        log("marker: hidden by double-click, cub " .. tostring(M.cid) .. " gets no marker again")
    end
    hide()
    return true
end

-- ---------------------------------------------------------------------------
-- Lage (PLAN_B1E.md 1.7.4)
-- ---------------------------------------------------------------------------

-- Bandits' gemerkte Bildschirmstelle (nur LESEN, nur wenn Bandits geladen): { x, y } der oberen linken Ecke seines Markers
-- (B:client/BanditEventMarkerHandler.lua:17-21, geschrieben B:client/BanditEventMarkers.lua:88). player:getModData():
-- V:client/Entity/ISUI/BuildRecipe/ISBuildRecipePanel.lua:48.
local function banditsPlacement()
    if BanditEventMarker == nil then return nil end
    local p = getSpecificPlayer(0)                      -- V:client/Farming/CFarmingSystem.lua:45
    if not p then return nil end
    local md = p:getModData()
    local pl = md and md["BanditEventMarkerPlacement"]
    if type(pl) ~= "table" then return nil end
    local x, y = tonumber(pl[1]), tonumber(pl[2])
    if x == nil or y == nil then return nil end
    return x, y
end

-- Liegt ein sichtbarer Bandits-/NPC-Crew-Marker (BanditEventMarkerHandler.markers, nur LESEN) mit seiner Kreismitte (m.x + 22,5,
-- m.y + 22,5; Felder B:client/BanditEventMarkers.lua:235-236, Klickflaeche 45 :8) naeher als 48 + 48 f an unserer, rutscht unsere um
-- markerShift x f nach rechts (0 = aus). getDuration: B:client/BanditEventMarkers.lua:142; getIsVisible: V:client/ISUI/ISUIElement.lua:676.
local function overlapShift(x, y, f)
    local shift = cfg("markerShift", 100)
    if shift == 0 then return x end
    local h = BanditEventMarkerHandler
    if h == nil or type(h.markers) ~= "table" then return x end
    local half = CLICK_PX / 2
    local mx, my = x + half * f, y + half * f
    local lim = BASE_PX / 2 + (BASE_PX / 2) * f
    for _, m in pairs(h.markers) do
        if type(m) == "table" and m.getDuration ~= nil and m.getIsVisible ~= nil then
            local ox, oy = tonumber(m.x), tonumber(m.y)
            if ox ~= nil and oy ~= nil then
                local dx, dy = ox + half - mx, oy + half - my
                if dx * dx + dy * dy < lim * lim then
                    local dur = tonumber(m:getDuration())
                    if dur ~= nil and dur > 0 and m:getIsVisible() then
                        log("marker: moved " .. tostring(shift * f) .. " px to the right (another marker sits there)")
                        return x + shift * f
                    end
                end
            end
        end
    end
    return x
end

-- Kreismitte so klemmen, dass der Kreis (Radius r) ganz auf dem Bild bleibt.
local function clampCenter(cx, cy, r, W, H)
    if W > 2 * r then
        if cx < r then cx = r end
        if cx > W - r then cx = W - r end
    else
        cx = W / 2
    end
    if H > 2 * r then
        if cy < r then cy = r end
        if cy > H - r then cy = H - r end
    else
        cy = H / 2
    end
    return cx, cy
end

-- Faktor, Groessen, Farbe, Pfeil-Bild und Lage neu (Spielstart, Einblenden, Aufloesung, Optionswert). Nie je Bild.
-- getCore():getScreenWidth()/getScreenHeight(): V:client/Challenge/WinterIsComing.lua:18; setX/setY/setWidth/setHeight(Zahl):
-- V:client/ISUI/ISToolTip.lua:78-79, :173-174.
function U.MarkerLayout()
    local el = M.el
    if el == nil then return end
    local core = getCore()
    local W, H = core:getScreenWidth(), core:getScreenHeight()
    local idx = 1
    if U.Opt then idx = tonumber(U.Opt("MarkerSize", 1)) or 1 end
    local f, k = U.MarkerFactor(H, idx)
    M.idx = idx
    el.s = BASE_PX * f
    el.hs = el.s / 2
    local cw = CLICK_PX * f
    el.c = cw / 2
    el.ty = TEXT_DY * f
    if f < 1.25 then
        el.font = UIFont.Small
    elseif f < 1.75 then
        el.font = UIFont.Medium
    else
        el.font = UIFont.Large
    end
    el.cr, el.cg, el.cb = cfg("markerR", 1.0), cfg("markerG", 0.52), cfg("markerB", 0.09)
    local tex = M.tex
    if tex then el.arrow = tex.arrow[k] end
    -- Lage wie Bandits mal f (B:client/BanditEventMarkerHandler.lua:22-23), oder dessen gemerkte Stelle
    local x, y = W / 2 - (BASE_PX / 2) * f, (BASE_PX / 2) * f
    local px, py = banditsPlacement()
    if px ~= nil then x, y = px, py end
    if M.shown then x = overlapShift(x, y, f) end
    local cx, cy = clampCenter(x + el.c, y + el.c, el.hs, W, H)
    el:setWidth(cw)
    el:setHeight(cw)
    el:setX(cx - el.c)
    el:setY(cy - el.c)
end

-- ---------------------------------------------------------------------------
-- Ziel und Takt
-- ---------------------------------------------------------------------------

-- Ziel: Kennung und Lage des wilden Jungen dieses Spielers, oder nil (unveraendert seit B1c).
local function target(now)
    if not U.Fresh or not U.Fresh() then return nil end
    local view = B.View
    local me = view.me
    local id = me and me.wild
    if id == nil then return nil end
    if M.gone[id] then return nil end
    local c = view.cubs and view.cubs[id]
    if type(c) ~= "table" then return nil end
    if c.st == "shy" then
        local t = M.shyAt[id]
        if t == nil or now < t then
            t = now
            keep(M.shyAt, "shyN", id, t)
        end
        if now - t >= cfg("markerAfterMs", 60000) then return nil end
    elseif c.st ~= "new" then
        return nil
    end
    local x, y = nil, nil
    if U.CubPos then x, y = U.CubPos(id) end
    if x == nil then
        if type(c.x) ~= "number" or type(c.y) ~= "number" then return nil end
        x, y = c.x + 0.5, c.y + 0.5
    end
    return id, x, y
end

-- Einblenden: Text (einmal je Sitzung), Lage mit Ueberdeckung (einmal beim Einblenden), sichtbar.
-- setVisible(true): V:client/Chat/ISAlert.lua:54-55 (dort ISAlert.alert:setVisible(true)).
local function show()
    local el = M.el
    if M.text == nil then M.text = U.T("UI_BN_Bear_Marker_Cub") end
    el.text = M.text
    M.shown = true
    U.MarkerLayout()
    el.on = true
    el:setVisible(true)
end

-- Rumpf des Takts. getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485; getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45;
-- isDead() am Spieler: V:client/Context/ISMenuContextWorld.lua:37; getX/getY am Spieler: V:client/Fishing/TensionUI.lua:11.
-- Richtung wie Bandits' gespielter Pfeil (Form B:client/BanditEventMarkers.lua:118-121: atan2 der Welt-Differenz + 135 Grad, Pfeil-Bild
-- mit der Spitze nach oben); math.atan2: V:client/ISUI/Fireplace/ISKnob.lua:137, math.deg: V:client/Foraging/ISBaseIcon.lua:212.
function U.MarkerTick()
    local now = getTimestampMs()
    if now >= M.at and now - M.at < cfg("markerMs", 400) then return end
    M.at = now
    local el = M.el
    if el == nil or not B.View or not B.CFG or not U.T then return end
    local p = getSpecificPlayer(0)
    local id, x, y = nil, nil, nil
    if p and not p:isDead() then id, x, y = target(now) end
    if id == nil then
        hide()
        return
    end
    M.cid = id
    local px, py = p:getX(), p:getY()
    local dx, dy = x - px, y - py
    el.ang = (math.deg(math.atan2(dy, dx)) + cfg("markerAngleAdd", 135) + 360) % 360
    local d
    if B.DistXY then d = B.DistXY(px, py, x, y) else d = math.sqrt(dx * dx + dy * dy) end
    el.close = d <= cfg("markerCloseTiles", 6.6)
    if not M.shown then
        show()
    elseif U.Opt then
        -- Optionswert geaendert (U.Opt: hoechstens 1 x je Sekunde gelesen): neu legen
        local idx = tonumber(U.Opt("MarkerSize", 1)) or 1
        if idx ~= M.idx then U.MarkerLayout() end
    end
end

-- Bilder einmal je Sitzung. getTexture("media/ui/<datei>.png"): V:client/Chat/ISChat.lua:921. Fehlt eins: eine Fehlerzeile, das Bild
-- wird nicht gezeichnet (der Rest schon).
local function loadTextures()
    local t = { arrow = {} }
    local missing = nil
    t.disc = getTexture(DISC_FILE)
    if not t.disc then missing = DISC_FILE end
    t.ring = getTexture(RING_FILE)
    if not t.ring then missing = RING_FILE end
    t.icon = getTexture(ICON_FILE)
    if not t.icon then missing = ICON_FILE end
    for k = 1, #ARROW_FILES do
        t.arrow[k] = getTexture(ARROW_FILES[k])
        if not t.arrow[k] then missing = ARROW_FILES[k] end
    end
    if missing then errLine("image not found: " .. missing) end
    return t
end

-- Je Spielstart ein frisches Element (Hauptmenue und neu laden): altes abmelden (removeFromUIManager: V:client/ISUI/ISUIElement.lua:1373,
-- tut nichts, wenn es schon weg ist; Aufrufer V:client/ISUI/Maps/ISMap.lua:116), neues anlegen, unsichtbar.
-- initialise / addToUIManager: V:client/ISUI/Animal/ISAnimalContextMenu.lua:746-747.
local function onGameStart()
    if M.el then M.el:removeFromUIManager() end
    M.el = nil
    M.at = 0
    M.shown = false
    M.cid = nil
    M.idx = nil
    M.text = nil
    wipe(M.shyAt)
    M.shyN = 0
    wipe(M.gone)
    M.goneN = 0
    M.tex = loadTextures()
    local el = Mk:new(0, 0, CLICK_PX, CLICK_PX)
    el:initialise()
    el:addToUIManager()
    el:setVisible(false)
    el.disc, el.ring, el.icon = M.tex.disc, M.tex.ring, M.tex.icon
    M.el = el
    U.MarkerLayout()
end

-- Aufloesung geaendert: neu legen. Form V:client/ISUI/PlayerData/ISPlayerData.lua:185, :206.
local function onResolutionChange(_oldw, _oldh, _neww, _newh)
    U.MarkerLayout()
end

Events.OnTick.Add(function() U.MarkerTick() end)    -- V:client/Chat/ISChat.lua:943
Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
Events.OnResolutionChange.Add(onResolutionChange)   -- V:client/ISUI/PlayerData/ISPlayerData.lua:206
