--
-- NPC Crew -- Baer, Namensschild je Baer an/aus (F1, PLAN_F1.md 0.7, 2.9; Kevin 08.11.2026: Namensschild "je Baer; Vorgabe an" und
-- "das kann jeder frei entscheiden im baeren menue was er haben will" = JE SPIELER, was ich sehe -- ENT:103, :106).
-- F1B (PLAN_F1B.md 0 E11, 5.1; Kevin 12.11.2026: "ich will auch im ui einen schalter haben das die anzeige aus geht wann der waechst"):
-- dazu die Wachstums-Zeile UEBER dem Baeren je Baer an/aus (U.AgeOn / U.AgeSet, Schalter "Growth line" im Baeren-Fenster). Die globale
-- Option "TagAge" (Optionen -> Mods) bleibt der Hauptschalter; ein ausgewachsener Baer zeigt die Zeile ohnehin nicht mehr
-- (client/ISUI/BanditsNPCBearHud.lua), sein gespeicherter Schalter gilt weiter, falls er wieder klein wird (Testbefehl).
--
-- Eine Einstellung dieses Rechners, der Server weiss nichts davon (keine ModData: MP-Clients speichern ihre globale ModData nicht,
-- forschung_f1.md 9 Nr. 7). Datei "BanditsNPCBear.ini" im Lua-Ordner des Spielers (wie Vanillas layout.ini): nur Zeilen fuer
-- AUSGESCHALTETE Baeren, "tagoff <u>" (Namensschild aus) und -- F1B -- "ageoff <u>" (Wachstums-Zeile aus); u = Kennzeichen des
-- Eintrags aus der Sicht, als Text (so wird nichts gerundet). Deckel je Liste 64 Zeilen (beim 65. faellt die aelteste DIESER Liste
-- heraus). Gelesen einmal je Spielstart (beim ersten Bedarf), geschrieben je Klick -- und zwar IMMER BEIDE Listen (erst tag, dann age),
-- sonst loeschte ein Klick am einen Schalter die andere Liste. Fremde Zeilen werden ueberlesen; eine alte Datei (nur tagoff) laedt
-- unveraendert.
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
local MAX = 64

-- Zwei Listen in derselben Datei. off = Kennzeichen -> true, order = Reihenfolge (fuer den Deckel und das Schreiben).
local L = {
    tag = { pre = "tagoff ", off = {}, order = {} },
    age = { pre = "ageoff ", off = {}, order = {} },
}
local LISTS = { L.tag, L.age }                      -- Lese- und Schreib-Reihenfolge
local T = { loaded = false }

local function keyOf(c)
    if type(c) ~= "table" or c.u == nil then return nil end
    return tostring(c.u)
end

local function remember(list, k)
    if list.off[k] then return end
    list.off[k] = true
    list.order[#list.order + 1] = k
    while #list.order > MAX do
        local old = table.remove(list.order, 1)
        list.off[old] = nil
    end
end

local function forgetKey(list, k)
    if not list.off[k] then return end
    list.off[k] = nil
    for i = #list.order, 1, -1 do
        if list.order[i] == k then table.remove(list.order, i) end
    end
end

local function clearAll()
    for i = 1, #LISTS do
        LISTS[i].off = {}
        LISTS[i].order = {}
    end
end

-- Datei lesen (einmal je Spielstart). Fehlt sie, legt Vanilla sie leer an (zweites Argument true, ISLayoutManager.lua:127).
function U.TagLoad()
    T.loaded = true
    clearAll()
    local r = getFileReader(FILE, true)
    if not r then return end
    while true do
        local line = r:readLine()
        if line == nil then break end
        line = string.trim(line)
        for i = 1, #LISTS do
            local list = LISTS[i]
            local pre = list.pre
            if string.sub(line, 1, string.len(pre)) == pre then
                local k = string.trim(string.sub(line, string.len(pre) + 1))
                if k ~= "" then remember(list, k) end
                break
            end
        end
    end
    r:close()
end

-- Beide Listen schreiben (erst tag, dann age).
local function save()
    local w = getFileWriter(FILE, true, false)
    if not w then
        if B.ErrEvery then B.ErrEvery("tags:write", 600000, "tags: " .. FILE .. " could not be written") end
        return
    end
    for i = 1, #LISTS do
        local list = LISTS[i]
        for j = 1, #list.order do
            w:write(list.pre .. list.order[j] .. "\n")
        end
    end
    w:close()
end

-- Ist der Schalter dieser Liste fuer diesen Baeren an? Ohne Kennzeichen u (alte Sicht): immer an.
local function isOn(list, c)
    local k = keyOf(c)
    if k == nil then return true end
    if not T.loaded then U.TagLoad() end
    return list.off[k] ~= true
end

-- Schalter setzen; schreibt nur bei einer Aenderung.
local function setOn(list, c, on)
    local k = keyOf(c)
    if k == nil then return end
    if not T.loaded then U.TagLoad() end
    if on then
        if not list.off[k] then return end
        forgetKey(list, k)
    else
        if list.off[k] then return end
        remember(list, k)
    end
    save()
end

-- Namensschild dieses Baeren an? (F1)
function U.TagOn(c)
    return isOn(L.tag, c)
end

function U.TagSet(c, on)
    setOn(L.tag, c, on)
end

-- F1B: Wachstums-Zeile ueber diesem Baeren an? (ohne Kennzeichen: an)
function U.AgeOn(c)
    return isOn(L.age, c)
end

function U.AgeSet(c, on)
    setOn(L.age, c, on)
end

local function onGameStart()
    T.loaded = false
    clearAll()
end

Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
