--
-- NPC Crew -- Baer, Anzeige-Optionen je Spieler (B1c, PLAN_B1C.md 1.9, 6.8): eine eigene Seite "BanditsNPCBear" unter
-- Optionen -> Mods ("NPC Crew: Bear"). Heute zwei Werte: Namensschilder ueber gezaehmten Baeren an/aus und die Groesse der
-- Anzeige ueber den Baeren (100 / 150 / 200 = Schrift Small / Medium / Large). Der Zaehm-Balken bleibt immer (Kevin).
--
-- Warum hier und nicht in der Sandbox: das ist eine Anzeige-Frage des eigenen Rechners, keine Weltregel. Vanilla speichert die
-- Seite selbst je Rechner in ModOptions.ini (V:client/PZAPI/ModOptions.lua:259-290, geladen V:client/OptionScreens/MainOptions.lua:2791);
-- im Mehrspieler gilt sie je Client, der Server kennt sie nicht und braucht sie nicht.
--
-- Bausteine: alles reines Vanilla-Lua (Tabellen, kein Engine-Aufruf) aus V:client/PZAPI/ModOptions.lua -- create :247-253,
-- addTitle :28-30, addTickBox :64-86, addSlider :206-228, getOptions :255-257, getOption :24-26, getValue :67 / :215. Aufrufer
-- derselben Form in Bandits: B:client/BanditModOptions.lua:12-13 (create, addTitle), B:shared/BanditCompatibility.lua:98-99
-- (getOptions, getOption, getValue). EHRLICH (Nachbesserung B1c A3): addTickBox und addSlider haben in Vanilla, Bandits und NPC
-- Crew KEINEN Aufrufer -- nur ihre Definition ist gelesen (ganz; reines Lua, legt nur Tabellen an). Gezeichnet werden sie von
-- Vanillas eigenen Bausteinen (V:client/OptionScreens/MainOptions.lua:2809-2830 addYesNo, :3019-3036 MainOptions:addSlider, den
-- Vanilla selbst bei :1090 benutzt). Ob das als Beleg zaehlt, ist eine Regel-Frage an Kevin. Namen und Tooltips gehen beim Bau des
-- Fensters durch getText (V:client/OptionScreens/MainOptions.lua:2801, :2804, :2810-2812, :3020) -- deshalb stehen hier SCHLUESSEL,
-- nie fertige Saetze.
-- Der Schieber zeigt im Fenster keinen Tooltip (MainOptions.lua:3019-3036); der Schluessel steht trotzdem fuer spaeter.
--
-- KEIN pcall um das Anlegen (sonst fehlte die Seite lautlos): Existenz-Riegel, im Fehlerfall eine Fehlerzeile, U.Opt gibt dann
-- die Vorgaben. Gelesen wird nur ueber U.Opt (hoechstens 1 x je Sekunde und Wert, zwischengespeichert).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local PAGE = "BanditsNPCBear"
local CACHE_MS = 1000

-- Zwischenspeicher je Wert: { v = Wert oder nil, at = ms }. Gedeckelt durch die festen Ids dieser Seite (heute 2).
local cache = {}

local function err(msg)
    local f = B.Err
    if f then
        f(msg)
    else
        print("[TC-BEAR] *** " .. tostring(msg))
    end
end

-- ---------------------------------------------------------------------------
-- Die Seite (auf Dateiebene, wie Bandits B:client/BanditModOptions.lua:12-14)
-- ---------------------------------------------------------------------------
if PZAPI and PZAPI.ModOptions and PZAPI.ModOptions.create then
    local o = PZAPI.ModOptions:create(PAGE, "UI_BN_Bear_MO_Page")
    o:addTitle("UI_BN_Bear_MO_Title")
    -- Namensschild (Name und Zustand) ueber JEDEM gezaehmten Baeren, eigenen und fremden; der Zaehm-Balken ungezaehmter Junge bleibt.
    o:addTickBox("TagShow", "UI_BN_Bear_MO_TagShow", true, "UI_BN_Bear_MO_TagShowTip")
    -- Groesse von Schild UND Balken: 100 = Small (Stand B1b), 150 = Medium, 200 = Large. Stufen statt stufenlos, weil
    -- drawTextZoomed keinen Vanilla-Aufrufer hat (PLAN_B1C.md 0.8, Frage F8).
    o:addSlider("TagSize", "UI_BN_Bear_MO_TagSize", 100, 200, 50, 100, "UI_BN_Bear_MO_TagSizeTip")
    -- Spaeter (PLAN_B1C.md 1.9 Punkt 5, NICHT jetzt anlegen): je Wert des Baeren eine Auswahl aus / Balken / Zahl, z. B.
    --   local hp = o:addComboBox("ShowHealth", <Schluessel ..._MO_Health>, <..._MO_HealthTip>)      -- ModOptions.lua:121
    --   hp:addItem(<..._MO_Off>, true)  hp:addItem(<..._MO_Bar>)  hp:addItem(<..._MO_Number>)      -- :131 (addItem ruft getText)
    -- ebenso Ausdauer, Hunger, Durst, Muedigkeit; dazu "DODGE" als addTickBox. Gelesen wird alles ueber U.Opt(id, vorgabe); jeder
    -- neue Schluessel in allen sieben UI.json.
else
    err("PZAPI.ModOptions is not available -- the bear display page (Options > Mods) was not created; the defaults apply")
end

-- ---------------------------------------------------------------------------
-- Lesen. id = Wert-Id der Seite, def = Vorgabe (auch der Typ, den der Aufrufer erwartet). Fehlt die Seite, der Wert oder passt
-- der Typ nicht: def. getTimestampMs: V:server/Foraging/forageServer.lua:456 (auf dem Client: V:client/Foraging/ISBaseIcon.lua:485).
-- ---------------------------------------------------------------------------
function U.Opt(id, def)
    local now = getTimestampMs()
    local c = cache[id]
    if c ~= nil and now >= c.at and now - c.at < CACHE_MS then
        if c.v == nil then return def end
        return c.v
    end
    local v = nil
    local api = PZAPI and PZAPI.ModOptions
    local page = nil
    if api and api.getOptions then page = api:getOptions(PAGE) end
    local opt = nil
    if page and page.getOption then opt = page:getOption(id) end
    if opt and opt.getValue then v = opt:getValue() end
    if v ~= nil and def ~= nil and type(v) ~= type(def) then v = nil end
    if c == nil then
        cache[id] = { v = v, at = now }
    else
        c.v = v
        c.at = now
    end
    if v == nil then return def end
    return v
end
