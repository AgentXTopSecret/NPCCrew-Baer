--
-- NPC Crew -- Baer, Symbol auf Mini-Karte und grosser Karte (B1c, PLAN_B1C.md 1.8, 4.2, 4.3; Kevin: "ich brauch nen map marker
-- mit unseren baeren icon").
--
-- Je EIGENEM Baeren ein kleines Baeren-Symbol (dasselbe Bild wie die Bildschirm-Markierung): eigen = Besitzer bin ich und Zustand
-- "tame"/"missing", oder gebunden an mich und "fed" (Kevin: auch das angefuetterte eigene Junge). "ich" wie beim Namensschild:
-- me.key der Sicht; im Einzelspieler zaehlt der feste Schluessel B.SP_KEY als eigen, im Mehrspieler nie. Fremde Baeren nie.
-- Ein mitfahrendes Junges ("ride") bekommt kein Symbol -- es ist ja beim Spieler (Frage F14).
-- Lage: live von der Client-Kopie (Alpha 1,0), sonst die letzte bekannte Kachel aus der Sicht (Alpha 0,55, "letzte bekannte Stelle";
-- ein vermisstes Junges ebenso). Ausserhalb des Kartenfensters: nicht zeichnen (lieber nichts als ein Symbol am Rand).
--
-- Einhaengen: die render-Methoden von ISMiniMapInner (erbt ISUIElement.render, V:client/ISUI/Maps/ISMiniMap.lua:4,
-- V:client/ISUI/ISUIElement.lua:1618) und ISWorldMap (eigene Methode, V:client/ISUI/Maps/ISWorldMap.lua:384) werden umwickelt: erst
-- die vorige Methode, dann unsere Symbole darueber (die Karte selbst malt in prerender, ISMiniMap.lua:206-212). Keine Vanilla-Datei
-- wird geaendert. EINMAL je Klasse (Merker), am Datei-Ende und noch einmal bei OnGameStart, falls eine Klasse beim Laden fehlte --
-- NIE erneut ueber einen fremden Aufsatz. Diese LEHRE stammt aus NPC Crew (v3.9.55: ein Identitaets-Neuversuch baute dort eine
-- Endlosschleife, NC client/ISUI/BanditsNPCMiniMap.lua:249-276); die Form hier ist eigene (eine Hilfsfunktion hook je Klasse,
-- Nachbesserung B1c A5 -- vorher stand der Einhaengeblock fast wortgleich wie in NPC Crew). NPC Crew umwickelt dieselben zwei Methoden;
-- beide merken die vorige Methode, die Kette haelt in jeder Ladefolge (baer/NAEHTE.md Zeile 18).
--
-- Engine-Aufrufe (je Fundstelle mit gleichen Argumenttypen):
--   self.mapAPI:worldToUIX(x, y) / worldToUIY(x, y), IMMER zwei Zahlen: V:client/ISUI/Maps/ISWorldMap.lua:478-479,
--     V:client/ISUI/Maps/ISWorldMapSymbols.lua:347; mapAPI am Element: ISMiniMap.lua:192, ISWorldMap.lua:395.
--   self.mapAPI:getZoomF(): V:client/ISUI/Maps/ISWorldMap.lua:447 (Groesse auf der grossen Karte wie Vanillas Druckmedien :446-449).
--   self:drawTextureScaledAspect(tex, x, y, w, h, a, r, g, b): V:client/ISUI/Maps/ISWorldMap.lua:482; Reihenfolge a, r, g, b laut
--     V:client/ISUI/ISUIElement.lua:1065.
--   self:getWidth() / self:getHeight() (Vanilla-Lua, ISUIElement.lua:259-271): V:client/ISUI/Maps/ISMiniMap.lua:356.
--   getTexture(pfad): V:client/ISUI/Maps/ISMap.lua:573.
--   a:isExistInTheWorld(): V:client/ISUI/Animal/ISAnimalUI.lua:15; a:getX()/getY(): V:client/TimedActions/ISContextualActions.lua:100.
-- Kosten: die Liste "wer" wird hoechstens je B.CFG.mapListMs (500 ms) neu gebaut (Sicht lesen, U.CubObj); je Bild und Symbol nur
-- 1 Existenzfrage + 2 Lage-Fragen an der Kopie + 2 Umrechnungen + 1 Bild; je Bild und Karte getWidth/getHeight (+ getZoomF auf der
-- grossen Karte). Deckel: hoechstens SYMBOL_MAX Symbole. Nur wenn eine Karte offen ist (sonst ruft niemand render).
-- Fehler beim Zeichnen: pcall nur um unseren Teil (lauter belegte Aufrufe), Fehlerzeile hoechstens je Minute (B.ErrEvery "map"),
-- nie stumm; die vorige render-Methode laeuft AUSSERHALB davon (ihre Fehler bleiben, wie sie sind).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local ICON = "media/ui/BanditsNPCBearCub_marker.png"
local A_LIVE = 1.0          -- geladen, Lage live
local A_AWAY = 0.55         -- letzte bekannte Stelle
local SYMBOL_MAX = 5        -- BearMaxPerPlayer (hoechstens 4) + 1 angefuettertes
local TEX_RETRY_MS = 10000  -- fehlt das Bild: so selten erneut fragen

local function cfg(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Die Liste "wer und wo zuletzt" (nur diese Sitzung). Eintraege werden wiederverwendet: keine Tabelle je Bild.
local L = { at = 0, n = 0, list = {}, tex = nil, texAt = nil }

-- Eigen? (siehe Kopf)
local function mine(c, meKey, sp)
    if c.ride == true then return false end
    local st = c.st
    local who
    if st == "tame" or st == "missing" then
        who = c.owner
    elseif st == "fed" then
        who = c.bond
    else
        return false
    end
    if who == nil then return false end
    return who == meKey or (sp and who == B.SP_KEY)
end

local function rebuild(now)
    L.at = now
    L.n = 0
    if L.tex == nil and (L.texAt == nil or now < L.texAt or now - L.texAt >= TEX_RETRY_MS) then
        L.texAt = now
        L.tex = getTexture(ICON)
        if L.tex == nil and B.ErrEvery then B.ErrEvery("maptex", 600000, "map: texture " .. ICON .. " not found") end
    end
    if not U.Fresh or not U.Fresh() then return end
    local view = B.View
    local cubs = view and view.cubs
    if type(cubs) ~= "table" then return end
    local meKey = view.me and view.me.key
    local sp = (B.IsSP ~= nil and B.IsSP()) and true or false
    for id, c in pairs(cubs) do
        if L.n >= SYMBOL_MAX then break end
        if type(c) == "table" and mine(c, meKey, sp) then
            local a = nil
            if U.CubObj then a = U.CubObj(id) end
            local x, y = nil, nil
            if type(c.x) == "number" and type(c.y) == "number" then
                x, y = c.x + 0.5, c.y + 0.5
            end
            if a ~= nil or x ~= nil then
                L.n = L.n + 1
                local e = L.list[L.n]
                if e == nil then
                    e = {}
                    L.list[L.n] = e
                end
                e.a, e.x, e.y = a, x, y
            end
        end
    end
    -- alte Objekt-Verweise hinter dem Ende loslassen (die Liste waechst nie ueber SYMBOL_MAX)
    for i = L.n + 1, #L.list do L.list[i].a = nil end
end

-- Unser Teil von render (self = das Kartenelement). mini = true auf der Mini-Karte.
local function drawSymbols(self, mini)
    -- Geteilter Bildschirm: die Sicht gehoert Spieler 1 (Nummer 0); playerNum am Kartenelement: ISMiniMap.lua:346, ISWorldMap.lua:401.
    local pn = self.playerNum
    if type(pn) == "number" and pn ~= 0 then return end
    local now = getTimestampMs()                        -- V:client/Foraging/ISBaseIcon.lua:485
    if now < L.at or now - L.at >= cfg("mapListMs", 500) then rebuild(now) end
    if L.n == 0 or L.tex == nil then return end
    local api = self.mapAPI
    if not api then return end
    local size
    if mini then
        size = cfg("mapMiniPx", 14)
    else
        -- wie V:client/ISUI/Maps/ISWorldMap.lua:446-449 (lerp ueber Zoom 12..15), nur kleiner; ohne PZMath, reines Lua
        local lo, hi = cfg("mapWorldMin", 18), cfg("mapWorldMax", 28)
        local zoom = api:getZoomF()
        local t = (zoom - 12) / 3
        if t < 0 then t = 0 end
        if t > 1 then t = 1 end
        size = lo + (hi - lo) * t
    end
    local half = size / 2
    local w = self:getWidth()
    local h = self:getHeight()
    local tex = L.tex
    for i = 1, L.n do
        local e = L.list[i]
        local x, y, alpha = e.x, e.y, A_AWAY
        local a = e.a
        if a ~= nil and a:isExistInTheWorld() then
            x = a:getX()
            y = a:getY()
            alpha = A_LIVE
        end
        if x ~= nil then
            local ux = api:worldToUIX(x, y)
            local uy = api:worldToUIY(x, y)
            if ux - half >= 0 and uy - half >= 0 and ux + half <= w and uy + half <= h then
                self:drawTextureScaledAspect(tex, ux - half, uy - half, size, size, alpha, 1, 1, 1)
            end
        end
    end
end

local function draw(self, mini)
    local ok, e = pcall(drawSymbols, self, mini)
    if not ok and B.ErrEvery then B.ErrEvery("map", 60000, "map symbol failed: " .. tostring(e)) end
end

-- ---------------------------------------------------------------------------
-- Einhaengen (einmal je Klasse). hooked[Schluessel] = die vorige render-Methode; einmal gesetzt, nie wieder angefasst -- auch nicht,
-- wenn spaeter ein fremder Aufsatz ueber uns liegt (sonst liefe unsere Huelle ueber sich selbst im Kreis).
-- ---------------------------------------------------------------------------
local hooked = {}

local function hook(key, cls, mini)
    if hooked[key] ~= nil or cls == nil then return end
    local before = cls.render
    if before == nil then return end
    hooked[key] = before
    cls.render = function(self)
        before(self)
        draw(self, mini)
    end
end

function U.MapInstall()
    hook("mini", ISMiniMapInner, true)
    hook("world", ISWorldMap, false)
end

U.MapInstall()
Events.OnGameStart.Add(function() U.MapInstall() end)  -- V:client/Chat/ISChat.lua:1186
