--
-- NPC Crew -- Baer, Namensschild je Baer an/aus (F1, PLAN_F1.md 0.7, 2.9; Kevin 08.11.2026: Namensschild "je Baer; Vorgabe an" und
-- "das kann jeder frei entscheiden im baeren menue was er haben will" = JE SPIELER, was ich sehe -- ENT:103, :106).
--
-- Eine Einstellung dieses Rechners, der Server weiss nichts davon (keine ModData: MP-Clients speichern ihre globale ModData nicht,
-- forschung_f1.md 9 Nr. 7). Datei "BanditsNPCBear.ini" im Lua-Ordner des Spielers (wie Vanillas layout.ini): nur Zeilen fuer
-- AUSGESCHALTETE Baeren, "tagoff <u>" (u = Kennzeichen des Eintrags aus der Sicht, als Text -- so wird nichts gerundet). Deckel 64
-- Zeilen (beim 65. faellt die aelteste heraus). Gelesen einmal je Spielstart (beim ersten Bedarf), geschrieben je Klick.
-- Die globale Option "TagShow" (Optionen -> Mods) bleibt der Hauptschalter: ist sie aus, sind alle Schilder aus.
-- Dateizugriff: getFileReader(Name, true) / readLine / close und getFileWriter(Name, true, false) / write / close wie
-- V:client/ISUI/ISLayoutManager.lua:127-135, :172-185; string.trim :136.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local FILE = "BanditsNPCBear.ini"
local PREFIX = "tagoff "
local MAX = 64

local T = { loaded = false, off = {}, order = {} }

local function keyOf(c)
    if type(c) ~= "table" or c.u == nil then return nil end
    return tostring(c.u)
end

local function remember(k)
    if T.off[k] then return end
    T.off[k] = true
    T.order[#T.order + 1] = k
    while #T.order > MAX do
        local old = table.remove(T.order, 1)
        T.off[old] = nil
    end
end

-- Datei lesen (einmal je Spielstart). Fehlt sie, legt Vanilla sie leer an (zweites Argument true, ISLayoutManager.lua:127).
function U.TagLoad()
    T.loaded = true
    T.off = {}
    T.order = {}
    local r = getFileReader(FILE, true)
    if not r then return end
    while true do
        local line = r:readLine()
        if line == nil then break end
        line = string.trim(line)
        if string.sub(line, 1, string.len(PREFIX)) == PREFIX then
            local k = string.trim(string.sub(line, string.len(PREFIX) + 1))
            if k ~= "" then remember(k) end
        end
    end
    r:close()
end

local function save()
    local w = getFileWriter(FILE, true, false)
    if not w then
        if B.ErrEvery then B.ErrEvery("tags:write", 600000, "tags: " .. FILE .. " could not be written") end
        return
    end
    for i = 1, #T.order do
        w:write(PREFIX .. T.order[i] .. "\n")
    end
    w:close()
end

-- Schild dieses Baeren an? Ohne Kennzeichen u (alte Sicht): immer an.
function U.TagOn(c)
    local k = keyOf(c)
    if k == nil then return true end
    if not T.loaded then U.TagLoad() end
    return T.off[k] ~= true
end

function U.TagSet(c, on)
    local k = keyOf(c)
    if k == nil then return end
    if not T.loaded then U.TagLoad() end
    if on then
        if not T.off[k] then return end
        T.off[k] = nil
        for i = #T.order, 1, -1 do
            if T.order[i] == k then table.remove(T.order, i) end
        end
    else
        if T.off[k] then return end
        remember(k)
    end
    save()
end

local function onGameStart()
    T.loaded = false
    T.off = {}
    T.order = {}
end

Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
