--
-- NPC Crew -- Baer, Bildschirm-Markierung oben (B1c, PLAN_B1C.md 1.7, 4.3; Kevin: "wie beim npc crew", Symbol "ich will 1 haben").
--
-- Ein Pfeil oben am Bildschirm zeigt auf das WILDE Junge des Spielers (aus dem Wald oder vom Koeder), solange es noch nicht
-- entdeckt ist ("new") und noch eine Weile nach dem Entdecken (B.CFG.markerAfterMs, Vorgabe 60 s ab dem ersten "shy", das dieser
-- Client sieht). Weg ist er, sobald das Junge angefuettert/gezaehmt ist (B.View.me.wild faellt weg), der Eintrag fehlt, die Lage
-- fehlt oder die Frist um ist. Kevins Symbol (media/ui/BanditsNPCBearCub_marker.png), Farbe { r = 1.0, g = 0.72, b = 0.30 }
-- (im Spiel kraeftiges Orange, Kevin: so lassen), Text UI_BN_Bear_Marker_Cub.
--
-- Weg: Bandits' eigene Markierung. BanditEventMarkerHandler.set(id, symbol, dauer, x, y, farbe, text)
-- (B:client/BanditEventMarkerHandler.lua:6-38; Aufrufer derselben Form B:server/BanditServerSpawner.lua:1093 und
-- B:server/BanditServerWanderers.lua:697 -- dort mit getRandomUUID() statt einer festen Id). Mit IMMER DERSELBEN Id verschiebt ein
-- weiteres set() den vorhandenen Marker (:31-36), Dauer 0 blendet ihn aus (B:client/BanditEventMarkers.lua:135-140). So macht es
-- auch NPC Crew fuer seinen Ueberlebenden-Pfeil (NC client/BanditsNPCSpawn.lua:238-321, nur gelesen, nichts kopiert).
-- Nur wenn Bandits geladen ist (Existenz-Riegel); ohne Bandits tut diese Datei nichts.
--
-- Takt: Events.OnTick (Client, V:client/Chat/ISChat.lua:943), gedrosselt auf B.CFG.markerMs (400 ms) -- je Takt hoechstens ein set(),
-- dazu ggf. drei Aufrufe an der Client-Kopie (U.CubPos). Ein Marker, nie mehr (feste Id).
-- Mehrspieler: alles aus der Sicht DIESES Clients (B.View). Bandits zeigt immer fuer getSpecificPlayer(0) (Handler :8): bei
-- geteiltem Bildschirm nur Spieler 1 (Bandits-Grenze).
--
-- Drei Feinheiten:
--   * Doppelklick blendet aus (Bandits setzt die Dauer auf 0, B:client/BanditEventMarkers.lua:19-21). Sieht dieser Client UNSEREN
--     Marker mit Dauer 0, ohne dass wir 0 gesetzt haben, zeigt er ihn fuer DIESES Junge nicht wieder; ein neues Junges bekommt
--     wieder einen (Frage F6).
--   * Bandits legt alle Marker an EINE gemerkte Bildschirmstelle (Handler :17-23). Liegt beim Anlegen unseres Markers ein anderer
--     sichtbarer Marker genau dort (z. B. NPC Crews Ueberlebenden-Pfeil), wird unserer einmal um B.CFG.markerShift (100 px) nach
--     rechts geschoben (0 = aus; Frage F5). setX am Marker-Element: B:client/BanditEventMarkers.lua:81, :103.
--   * Bandits raeumt alte Marker nur aus SEINER Tabelle (RemoveOldMarkers, Handler :40-49); das unsichtbare Element bliebe im
--     UIManager liegen, und jede neue Dauer legte ein weiteres an. Deshalb nimmt diese Datei UNSER altes Element selbst aus dem
--     UIManager, sobald es nicht mehr in Bandits' Tabelle steht (removeFromUIManager: Vanilla-Lua V:client/ISUI/ISUIElement.lua:1373,
--     Aufrufer V:client/ISUI/Maps/ISMap.lua:116). Deckel: hoechstens ein lebendes Element von uns.
-- Fehler in Bandits' set() laufen nicht je Takt in die Konsole: pcall um den belegten Aufruf, Fehlerzeile hoechstens je Minute
-- (B.ErrEvery), nie stumm.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local ID = "BanditsNPCBearCub"
local ICON = "media/ui/BanditsNPCBearCub_marker.png"
local COLOR = { r = 1.0, g = 0.72, b = 0.30 }
local KEEP_MAX = 16         -- Deckel der Merk-Tabellen (shyAt, gone); voll -> geleert

-- Stellwerte aus B.CFG (KERN, PLAN_B1C.md 5.2) mit eigenem Rueckfall.
local function cfg(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Alles, was die Markierung sich merkt (nur diese Sitzung, nie gespeichert, nie gesendet).
local M = {
    at = 0,         -- ms, letzter Takt
    on = false,     -- wir haben zuletzt eine Dauer > 0 gesetzt
    cid = nil,      -- Kennung des Jungen, auf das der Marker zeigt
    obj = nil,      -- unser Marker-Element, wie wir es zuletzt in Bandits' Tabelle sahen
    x = 0, y = 0,   -- letzte Lage (fuer das Ausblenden)
    text = nil,     -- Text, einmal je Sitzung gebaut (Bandits nimmt ihn nur beim Anlegen, Handler :26)
    shyAt = {}, shyN = 0,   -- id -> ms: erstes "shy", das dieser Client sah
    gone = {}, goneN = 0,   -- id -> true: per Doppelklick ausgeblendet, fuer dieses Junge nicht wieder
    made = 0,       -- so viele Marker-Elemente hat Bandits fuer uns angelegt (Diagnose)
}

local function wipe(t)
    local keys = {}
    for k, _ in pairs(t) do keys[#keys + 1] = k end
    for i = 1, #keys do t[keys[i]] = nil end
end

-- Bandits geladen? set() braucht BanditUtils.DistTo (Handler :12) und BanditEventMarker (Handler :13, :26).
local function bandits()
    local h = BanditEventMarkerHandler
    return h ~= nil and h.set ~= nil and type(h.markers) == "table" and BanditEventMarker ~= nil
        and BanditUtils ~= nil and BanditUtils.DistTo ~= nil
end

local function errLine(what, e)
    local f = B.ErrEvery
    if f then f("marker", 60000, "marker: " .. what .. " failed: " .. tostring(e)) end
end

local function log(msg)
    local f = B.Log
    if f then f(msg) end
end

-- Der belegte Aufruf (Handler :6), geschuetzt gegen eine Fehlerflut, nie stumm.
local function setMarker(dur, x, y, text)
    local ok, e = pcall(BanditEventMarkerHandler.set, ID, ICON, dur, x, y, COLOR, text)
    if not ok then errLine("BanditEventMarkerHandler.set", e) end
    return ok
end

-- Ausblenden: genau einmal set(..., 0, ...) (PLAN_B1C.md 1.7 Punkt 4). Ohne vorhandenen Marker tut set mit Dauer 0 nichts (Handler :11).
local function hide()
    if not M.on then return end
    M.on = false
    setMarker(0, M.x, M.y, "")
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

-- Unser altes Element liegt nicht mehr in Bandits' Tabelle (weggeraeumt): aus dem UIManager nehmen. removeFromUIManager tut nichts,
-- wenn es schon weg ist (V:client/ISUI/ISUIElement.lua:1373-1376).
local function dropOld(old)
    if old == nil or type(old) ~= "table" or old.removeFromUIManager == nil then return end
    local ok, e = pcall(old.removeFromUIManager, old)
    if not ok then errLine("removeFromUIManager", e) end
end

-- Beim Anlegen: liegt ein anderer sichtbarer Marker auf derselben Bildschirmstelle, unseren nach rechts schieben.
-- marker.x / .y: B:client/BanditEventMarkers.lua:235-236; getDuration :142; getIsVisible (ISUIElement, gerufen :28); setX :81.
local function shiftIfOverlap(mine)
    local shift = cfg("markerShift", 100)
    if shift == 0 then return end
    local mx, my = tonumber(mine.x), tonumber(mine.y)
    if mx == nil or my == nil then return end
    for eid, other in pairs(BanditEventMarkerHandler.markers) do
        if eid ~= ID and type(other) == "table" and other ~= mine then
            local ox, oy = tonumber(other.x), tonumber(other.y)
            if ox ~= nil and oy ~= nil and math.abs(ox - mx) < 1 and math.abs(oy - my) < 1
                and other:getDuration() > 0 and other:getIsVisible() then
                mine:setX(mx + shift)
                log("marker: moved " .. shift .. " px to the right (another marker sits on the same spot)")
                return
            end
        end
    end
end

-- Ziel: Kennung und Lage des wilden Jungen dieses Spielers, oder nil.
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

-- Rumpf des Takts. getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485; getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45;
-- isDead() am Spieler: V:client/Context/ISMenuContextWorld.lua:37.
function U.MarkerTick()
    local now = getTimestampMs()
    if now >= M.at and now - M.at < cfg("markerMs", 400) then return end
    M.at = now
    if not bandits() or not B.View or not B.CFG or not U.T then return end
    local markers = BanditEventMarkerHandler.markers
    local mk = markers[ID]

    -- 1. Bandits hat unser altes Element aus seiner Tabelle genommen: auch aus dem UIManager.
    if M.obj ~= nil and mk ~= M.obj then
        dropOld(M.obj)
        M.obj = mk
    end

    -- 2. Doppelklick: unser Marker hat Dauer 0, ohne dass wir sie gesetzt haben.
    if M.on and mk ~= nil and mk:getDuration() <= 0 then
        M.on = false
        if M.cid ~= nil then
            keep(M.gone, "goneN", M.cid, true)
            log("marker: hidden by double-click, cub " .. tostring(M.cid) .. " gets no marker again")
        end
    end

    -- 3. Ziel
    local p = getSpecificPlayer(0)
    local id, x, y = nil, nil, nil
    if p and not p:isDead() then id, x, y = target(now) end
    if id == nil then
        hide()
        return
    end

    -- 4. Zeigen / nachfuehren (gleiche Id = verschieben, Handler :31-36)
    M.cid, M.x, M.y = id, x, y
    if M.text == nil then M.text = U.T("UI_BN_Bear_Marker_Cub") end
    local before = markers[ID]
    if setMarker(cfg("markerDur", 1800), x, y, M.text) then M.on = true end
    local after = markers[ID]
    if after ~= nil and after ~= before then
        -- set() hat ein neues Element angelegt (nur moeglich, wenn vorher keins in der Tabelle stand, Handler :11)
        M.made = M.made + 1
        shiftIfOverlap(after)
    end
    M.obj = after
end

-- Je Spielstart frisch (Hauptmenue und neu laden).
local function onGameStart()
    M.at = 0
    M.on = false
    M.cid = nil
    M.obj = nil
    M.text = nil
    wipe(M.shyAt)
    M.shyN = 0
    wipe(M.gone)
    M.goneN = 0
end

Events.OnTick.Add(function() U.MarkerTick() end)    -- V:client/Chat/ISChat.lua:943
Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
