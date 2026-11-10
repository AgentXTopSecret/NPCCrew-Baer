--
-- NPC Crew -- Baer, Anzeige ueber der Welt (B1a, PLAN_ZAEHMEN.md 5.6, 6.8, 7): Zaehm-Balken ueber dem Jungen und das Schild
-- ueber dem eigenen Koederplatz.
--
-- Reine Anzeige: liest nur B.View (die Sicht, die der Schreiber diesem Spieler geschickt hat) und fragt nie den Server.
-- Einzelspieler und Mehrspieler laufen gleich; im Mehrspieler stammen alle Zahlen vom Server. Der dedizierte Server laedt client/ nicht.
--
-- Bauart (Vorbild: ein kleines Element, das weit daneben zeichnet; Vanilla ISButtonPrompt.lua:1244 haelt genauso ein 1 x 1-Element):
--   * EIN ISPanel, 1 x 1 Pixel in der Ecke oben links, angelegt bei OnGameStart. Es bleibt 1 x 1 (ein grosses Element frisst jeden
--     Weltklick) und wird NIE unsichtbar geschaltet (ein unsichtbares Element erreicht prerender nie wieder); Ein/Aus sitzt im
--     Zeichencode. Die drei Maus-Funktionen geben false zurueck.
--   * Die Liste der Balken wird hoechstens einmal je Sekunde neu gebaut (und sofort nach einer neuen Sicht): hoechstens
--     B.CFG.hudMax Junge in B.CFG.hudDist Kacheln, dazu fertige Texte. Die Objektliste der Zelle wird nur durchsucht, wenn ein
--     Junges aus der Sicht noch kein Objekt hat, und dann hoechstens einmal je Sekunde (nach fuenf vergeblichen Laeufen alle 5 s).
--   * Je Bild wird nur aus der fertigen Liste gezeichnet: je Balken zwei Umrechnungen, zwei Rechtecke, ein Rahmen, zwei Texte
--     (jeder mit Schatten). Keine Suche, kein getText, keine Tabelle je Bild.
--   * Bei mehr als einem lokalen Spieler (geteilter Bildschirm) wird nichts gezeichnet.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Die Klasse bleibt ein Local: sie muss nicht global sein (nur Zeitaktionen muessen das).
local Hud = ISPanel:derive("BanditsNPCBearHud")

local LIST_MS = 1000        -- Liste hoechstens so oft neu
local SCAN_FAST_MS = 1000   -- Suchlauf, solange ein Junges ohne Objekt ist
local SCAN_SLOW_MS = 5000   -- ... nach SCAN_FAST_N vergeblichen Laeufen
local SCAN_FAST_N = 5
-- Nach SCAN_SLOW_N vergeblichen Laeufen nur noch je SCAN_IDLE_MS (das eigene Junge steht in der Sicht, ist aber weit weg und
-- nicht geladen). Kommt der Spieler in seine Naehe, schickt der Schreiber eine neue Sicht (Server pushNewSights) und es geht
-- wieder schnell (S.scanMiss = 0 bei jeder neuen Sicht). Nachbesserung B6.
local SCAN_SLOW_N = 17
local SCAN_IDLE_MS = 30000
local FLASH_MS = 5000       -- so lange steht "Gezaehmt!"
local BAR_W = 64
local BAR_H = 7
local BAIT_DIST = 25        -- Kacheln: so nah steht das Schild ueber dem eigenen Koederplatz
local BAIT_Z = 0.3

local panel = nil
local fontH = nil

-- Alles, was die Anzeige sich merkt. Nichts davon wird gespeichert oder gesendet; die Tabellen sind durch die Sicht gedeckelt
-- (hoechstens so viele Kennungen, wie B.View.cubs traegt; verschwundene Kennungen fallen bei jeder neuen Sicht heraus).
local S = {
    dirty = true,   -- neue Sicht: Liste sofort neu
    listAt = 0,     -- ms, letzte Liste
    scanAt = 0,     -- ms, fruehestens naechster Suchlauf
    scanMiss = 0,   -- vergebliche Suchlaeufe in Folge
    list = {},      -- fertige Eintraege fuer den Zeichner
    n = 0,
    bait = nil,     -- fertiger Eintrag fuer das Koeder-Schild
    objs = {},      -- id -> IsoAnimal (nur in dieser Sitzung, jedes Mal gegengeprueft)
    prev = {},      -- id -> letzter gesehener Zustand (fuer "gerade gezaehmt")
    flash = {},     -- id -> ms, bis wann "Gezaehmt!" steht
}

local function reset()
    S.dirty = true
    S.listAt = 0
    S.scanAt = 0
    S.scanMiss = 0
    S.list = {}
    S.n = 0
    S.bait = nil
    S.objs = {}
    S.prev = {}
    S.flash = {}
end

-- ---------------------------------------------------------------------------
-- Liste bauen (hoechstens einmal je Sekunde)
-- ---------------------------------------------------------------------------

-- Objekt noch da und lebendig? isExistInTheWorld: client/ISUI/Animal/ISAnimalUI.lua:15; isDead: client/ISUI/Hutch/ISHutchUI.lua:427.
local function alive(a)
    return a ~= nil and a:isExistInTheWorld() and not a:isDead()
end

-- Bekommt dieses Junge gerade eine Anzeige? Ungezaehmte immer, gezaehmte nur die 5 Sekunden nach dem Zaehmen.
local function wanted(c, now)
    local st = c.st
    if st == "new" or st == "shy" or st == "fed" then return true end
    local till = S.flash[c.id]
    return till ~= nil and now < till
end

-- Kennungen vergessen, die die Sicht nicht mehr traegt. Erst sammeln, dann loeschen (nie waehrend des Durchlaufs).
local function forget(t, cubs)
    local gone = nil
    for id, _ in pairs(t) do
        if cubs[id] == nil then
            gone = gone or {}
            gone[#gone + 1] = id
        end
    end
    if gone then
        for i = 1, #gone do t[gone[i]] = nil end
    end
end

-- Suchlauf: alle geladenen Jungen einmal ihrem Sicht-Eintrag zuordnen. Die Liste ist eine Kopie der Engine, deshalb selten.
-- getCell():getObjectListForLua(), size(), get(i): Vanilla FenrisScenario.lua:505-507; instanceof(o, "IsoAnimal"):
-- shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; getAnimalType(): client/ISUI/Animal/ISAnimalUI.lua:65.
local function scan()
    local objects = getCell():getObjectListForLua()
    for i = 0, objects:size() - 1 do
        local o = objects:get(i)
        if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB then
            local v = B.ViewOf(o)
            if v and v.id ~= nil then S.objs[v.id] = o end
        end
    end
end

-- "bereit" oder die Restzeit als Text.
local function waitWord(c, kind, nowH)
    local left = B.WaitLeft(c, kind, nowH)
    if type(left) ~= "number" or left <= 0 then return U.T("UI_BN_Bear_Hud_Ready") end
    return U.WaitText(left)
end

-- Die fertigen Texte eines Eintrags (einmal je Liste, nie je Bild).
local function describe(e, meKey, nowH)
    local c = e.c
    if c.st == "tame" or c.st == "missing" then
        e.flash = true
        e.till = S.flash[c.id] or 0
        e.line1 = U.T("UI_BN_Bear_Hud_Tamed")
        return
    end
    local pct = math.floor(tonumber(c.tame) or 0)
    if pct < 0 then pct = 0 end
    if pct > 100 then pct = 100 end
    e.fill = math.floor(BAR_W * pct / 100)
    local unfed = (c.st == "new" or c.st == "shy")
    e.unfed = unfed
    local line1 = U.T("UI_BN_Bear_Hud_Taming", pct)
    if unfed then line1 = line1 .. " - " .. U.T("UI_BN_Bear_Hud_Shy") end
    e.line1 = line1
    if c.bond ~= nil and c.bond ~= meKey then
        -- an jemand anderen gebunden
        e.line2 = U.T("UI_BN_Bear_Hud_Other", tostring(c.bond))
    elseif unfed then
        -- noch nie gefuettert: Streicheln geht noch nicht, also nur die Futter-Zeile
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH))
    else
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH)) .. "   "
            .. U.T("UI_BN_Bear_Hud_Pet", waitWord(c, "pet", nowH))
    end
end

local function byDist(a, b)
    return a.d2 < b.d2
end

-- Koeder-Schild: nur der eigene Platz (mehr traegt die Sicht nicht), nur in BAIT_DIST Kacheln.
local function baitEntry(view, px, py)
    local bait = view.bait
    if type(bait) ~= "table" or type(bait.x) ~= "number" or type(bait.y) ~= "number" then return nil end
    local dx = bait.x + 0.5 - px
    local dy = bait.y + 0.5 - py
    if dx * dx + dy * dy > BAIT_DIST * BAIT_DIST then return nil end
    local kindKey = "UI_BN_Bear_Bait_Fish"
    if bait.kind == "honey" then kindKey = "UI_BN_Bear_Bait_Honey" end
    local e = { x = bait.x + 0.5, y = bait.y + 0.5, z = (tonumber(bait.z) or 0) + BAIT_Z }
    e.line1 = U.T("UI_BN_Bear_Hud_Bait", U.T(kindKey))
    if bait.ready == true then
        e.line2 = U.T("UI_BN_Bear_Hud_BaitReady")
    else
        e.line2 = U.T("UI_BN_Bear_Hud_BaitNight", tonumber(bait.nights) or 0, tonumber(bait.max) or 0)
    end
    return e
end

local function rebuild(now)
    local wasDirty = S.dirty
    S.dirty = false
    S.listAt = now
    S.n = 0
    S.bait = nil
    -- Nur eine Sicht von DIESEM Spiel zeigen (B.UI.Fresh, client/BanditsNPCBearClient.lua).
    if not U.Fresh or not U.Fresh() then return end
    local view = B.View
    local cubs = view.cubs
    if type(cubs) ~= "table" then return end

    if wasDirty then
        forget(S.objs, cubs)
        forget(S.prev, cubs)
        forget(S.flash, cubs)
        S.scanMiss = 0
    end

    -- 1. Zustandswechsel merken; fehlt einem gewuenschten Jungen das Objekt?
    local need = false
    local any = false
    for id, c in pairs(cubs) do
        any = true
        local was = S.prev[id]
        if c.st == "tame" and (was == "fed" or was == "shy" or was == "new") then
            S.flash[id] = now + FLASH_MS
        end
        S.prev[id] = c.st
        if wanted(c, now) and not alive(S.objs[id]) then
            S.objs[id] = nil
            need = true
        end
    end
    -- Die Sicht kennt weder ein Junges noch einen Koederplatz: nichts zu tun, kein Engine-Aufruf.
    if not any and view.bait == nil then return end

    local player = getSpecificPlayer(0)                 -- client/Farming/CFarmingSystem.lua:45
    if not player then return end
    local px = player:getX()                            -- client/Fishing/TensionUI.lua:11
    local py = player:getY()

    -- 2. Suchlauf, nur bei Bedarf und gedrosselt (now < scanAt - SCAN_IDLE_MS: die Uhr lief rueckwaerts).
    if need and (now >= S.scanAt or now < S.scanAt - SCAN_IDLE_MS) then
        scan()
        local still = false
        for id, c in pairs(cubs) do
            if wanted(c, now) and S.objs[id] == nil then still = true end
        end
        if still then
            S.scanMiss = S.scanMiss + 1
            local wait = SCAN_IDLE_MS
            if S.scanMiss <= SCAN_FAST_N then
                wait = SCAN_FAST_MS
            elseif S.scanMiss <= SCAN_SLOW_N then
                wait = SCAN_SLOW_MS
            end
            S.scanAt = now + wait
        else
            S.scanMiss = 0
            S.scanAt = now + SCAN_FAST_MS
        end
    end

    -- 3. Eintraege: die naechsten hudMax in hudDist Kacheln.
    local cfg = B.CFG
    local reach = cfg.hudDist or 20
    local max = cfg.hudMax or 6
    local found = {}
    for id, c in pairs(cubs) do
        local a = S.objs[id]
        if a ~= nil and wanted(c, now) and alive(a) then
            local dx = a:getX() - px                    -- client/TimedActions/ISContextualActions.lua:100
            local dy = a:getY() - py
            local d2 = dx * dx + dy * dy
            if d2 <= reach * reach then
                found[#found + 1] = { a = a, c = c, d2 = d2 }
            end
        end
    end
    if #found > 1 then table.sort(found, byDist) end
    local n = #found
    if n > max then n = max end
    if n > 0 then
        local meKey = view.me and view.me.key
        local nowH = B.Now()
        for i = 1, n do
            describe(found[i], meKey, nowH)
        end
    end
    S.list = found
    S.n = n

    -- 4. Koeder-Schild
    S.bait = baitEntry(view, px, py)
end

-- ---------------------------------------------------------------------------
-- Zeichnen (je Bild, nur aus der fertigen Liste)
-- ---------------------------------------------------------------------------

-- Text mit Schatten, sonst ist heller Text auf Sand oder Beton unlesbar. drawTextCentre: client/ISUI/ISUIElement.lua:1280.
local function text(self, str, x, y, r, g, b, a)
    self:drawTextCentre(str, x + 1, y + 1, 0, 0, 0, 0.7, UIFont.Small)
    self:drawTextCentre(str, x, y, r, g, b, a, UIFont.Small)
end

-- Das Element liegt bei 0,0 und wird nie verschoben: seine Koordinaten sind Bildschirm-Koordinaten.
-- isoToScreenX/Y(Spielernummer, x, y, z): client/Fishing/TensionUI.lua:11-12 (erstes Argument eine Zahl).
-- drawRect / drawRectBorder (x, y, w, h, a, r, g, b): client/ISUI/ISUIElement.lua:1191 / :1219.
local function draw(self, now)
    local cfg = B.CFG
    local lift = cfg.barZ or 0.55
    local fh = fontH
    for i = 1, S.n do
        local e = S.list[i]
        local a = e.a
        if a:isExistInTheWorld() then
            local x = a:getX()
            local y = a:getY()
            local z = a:getZ() + lift
            local sx = math.floor(isoToScreenX(0, x, y, z))
            local sy = math.floor(isoToScreenY(0, x, y, z))
            if e.flash then
                -- gerade gezaehmt: blinkt, bis die Frist um ist
                if now < e.till and (now % 700) < 450 then
                    text(self, e.line1, sx, sy - fh, 0.55, 1.0, 0.55, 1.0)
                end
            else
                local bx = sx - BAR_W / 2
                local by = sy - fh - BAR_H - 4
                text(self, e.line1, sx, by - fh - 2, 0.96, 0.96, 0.90, 0.95)
                self:drawRect(bx - 1, by - 1, BAR_W + 2, BAR_H + 2, 0.65, 0, 0, 0)
                if e.fill > 0 then
                    if e.unfed then
                        self:drawRect(bx, by, e.fill, BAR_H, 0.95, 0.95, 0.70, 0.25)
                    else
                        self:drawRect(bx, by, e.fill, BAR_H, 0.95, 0.45, 0.85, 0.35)
                    end
                end
                self:drawRectBorder(bx - 1, by - 1, BAR_W + 2, BAR_H + 2, 0.9, 0.85, 0.85, 0.80)
                text(self, e.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80)
            end
        end
    end
    local bait = S.bait
    if bait then
        local sx = math.floor(isoToScreenX(0, bait.x, bait.y, bait.z))
        local sy = math.floor(isoToScreenY(0, bait.x, bait.y, bait.z))
        text(self, bait.line1, sx, sy - fh * 2 - 2, 0.98, 0.85, 0.45, 0.95)
        text(self, bait.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80)
    end
end

-- Ein Panel sagt zu jedem Klick ja, wenn man es laesst: ausdruecklich nein.
function Hud:onMouseDown() return false end
function Hud:onMouseUp() return false end
function Hud:onRightMouseDown() return false end

function Hud:prerender()
    ISPanel.prerender(self)
    if not B.View or not B.CFG or not B.T then return end
    -- Geteilter Bildschirm: lieber nichts als auf der falschen Haelfte. getNumActivePlayers: client/Fishing/FishingHandler.lua:6.
    if getNumActivePlayers() > 1 then return end
    local now = getTimestampMs()                        -- client/Foraging/ISBaseIcon.lua:485
    if S.dirty or now - S.listAt >= LIST_MS or now < S.listAt then
        if not fontH then
            fontH = getTextManager():getFontHeight(UIFont.Small)    -- client/ISUI/Animal/ISAnimalUI.lua:4
        end
        rebuild(now)
    end
    if S.n > 0 or S.bait then
        draw(self, now)
    end
end

-- ---------------------------------------------------------------------------
-- Naht zum Kern (Plan 6.2.4): B.ApplySync ruft das nach jeder neuen Sicht.
-- ---------------------------------------------------------------------------
function B.OnView()
    S.dirty = true
    if U.NoteSync then U.NoteSync() end
end

-- Je Spielstart ein frisches Element. Ein altes (Hauptmenue und neu laden) wird vorher abgemeldet und vergessen:
-- removeFromUIManager ist Vanillas eigenes Lua (client/ISUI/ISUIElement.lua:1373) und tut nichts, wenn es schon weg ist.
local function onGameStart()
    if panel then panel:removeFromUIManager() end
    reset()
    panel = Hud:new(0, 0, 1, 1)
    panel:initialise()                                  -- client/ISUI/Animal/ISAnimalContextMenu.lua:746
    panel:noBackground()                                -- client/ISUI/ISPanel.lua:9
    panel:addToUIManager()                              -- client/ISUI/Animal/ISAnimalContextMenu.lua:747
end

Events.OnGameStart.Add(onGameStart)                     -- client/Chat/ISChat.lua:1186
