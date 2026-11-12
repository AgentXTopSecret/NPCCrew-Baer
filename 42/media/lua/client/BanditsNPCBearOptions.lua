--
-- NPC Crew -- Baer, Anzeige-Optionen je Spieler (B1c, PLAN_B1C.md 1.9, 6.8): eine eigene Seite "BanditsNPCBear" unter
-- Optionen -> Mods ("NPC Crew: Bear"). B1c: Namensschilder ueber gezaehmten Baeren an/aus und die Groesse der Anzeige ueber den
-- Baeren (100 / 150 / 200 = Schrift Small / Medium / Large). Der Zaehm-Balken bleibt immer (Kevin).
-- B1d (PLAN_B1D.md 1.6, 6.8; Kevin 11.11.2026: "jeden wert einzelnd ... im balken oder als zahl frei auswaehlbar"): Leben und
-- Ausdauer je als Auswahl Aus / Balken / Zahl (Vorgabe Leben = Balken, Ausdauer = Aus), dazu die Alter-Zeile an/aus (Vorgabe an).
-- Reihenfolge auf der Seite: TagShow, TagHealth, TagStamina, TagAge, TagSize.
-- B1e (PLAN_B1E.md 1.7.9, 6.7): danach MarkerSize -- Groesse der Markierung oben am Bildschirm (Auto / 100 ... 300 %, Vorgabe Auto).
-- F1 (PLAN_F1.md 1.7): danach WinSize -- Groesse des Baeren-Fensters (Auto / 100 ... 300 %, Vorgabe Auto; gleiche Stufen wie MarkerSize,
-- gelesen ueber U.Opt("WinSize", 1) -> U.MarkerFactor). Wirkt beim naechsten Oeffnen oder im 1-s-Takt des offenen Fensters.
-- F1B (PLAN_F1B.md 0 E1/E2, 1.1, 3.1; Kevin 12.11.2026: "bei E das baeren ui zu oeffnen und wenn man es aus der ferne oeffnen will dann
-- kann man ... den hotkey festelegen ... die E taste fuer den baeren wenn man in der naehe ist in sen mod settings zum aendern
-- eintragen"): danach ein Titel "Bear window keys" und ZWEI Tasten -- KeyNear (Vorgabe E, oeffnet/schliesst nahe am eigenen Baeren)
-- und KeyFar (Vorgabe KEINE Taste, oeffnet/schliesst aus jeder Entfernung). Reihenfolge jetzt: TagShow, TagHealth, TagStamina, TagAge,
-- TagSize, MarkerSize, WinSize, Titel Keys, KeyNear, KeyFar. Keine Zeile mehr in Vanillas Tastaturbelegung (keyBinding).
-- F2 (PLAN_F2.md 3.2; Kevin ENT:237 '"DODGE" ein/aus'): nach WinSize die Schaltbox TagDodge (Vorgabe an) -- "DODGE" schwebt ueber dem
-- eigenen Baeren, wenn ein Angriff ihn verfehlt (client/BanditsNPCBearFx.lua U.HudFloat). Reihenfolge: ..., WinSize, TagDodge, Titel Keys, ...
-- addKeyBind(id, Name, Taste, Tooltip): V:client/PZAPI/ModOptions.lua:182-204 (getValue :191 = Tastencode), Aufrufer derselben Form
-- B:client/BanditModOptions.lua:14. AUSNAHME von der Regel "hier stehen Schluessel": der NAME einer Tasten-Zeile ist schon
-- uebersetzt (getText auf Dateiebene wie Bandits :12-14) -- Vanilla beschriftet die Zeile mit getText(option.name)
-- (V:client/OptionScreens/MainOptions.lua:2985), merkt sich aber btn.internal = option.name (:2992) und sucht die Zeile beim
-- Tastendruck im Dialog ueber den Beschriftungstext (:3804, :3818) -- mit einem rohen Schluessel liefe das ins Leere (Lua-Fehler).
-- Der Tooltip bleibt Schluessel (btn:setTooltip(getText(option.tooltip)) :2996-2998). Kein %1 in diesen Namen.
-- 0 (Keyboard.KEY_NONE, V:shared/keyBinding.lua:143 "-- 0") heisst "keine Taste" (der Dialog "Loeschen" setzt 0,
-- V:client/ISUI/ISSetKeybindDialog.lua:85-96). Nur eine einfache Taste: save schreibt nur den Code (V:client/PZAPI/ModOptions.lua:276-280),
-- getValue gibt nur ihn (:191) -- Shift/Strg/Alt waeren nach dem Neustart weg. Gespeichert wird von Vanilla selbst
-- ("keybind|BanditsNPCBear|KeyNear|18" in ModOptions.ini, :276-282, geladen :326-327). Die Vorgaben stehen in U.KEY_DEF (unten, auf
-- Dateiebene AUSSERHALB des Riegels), damit client/BanditsNPCBearKey.lua sie auch ohne die Seite kennt.
--
-- Warum hier und nicht in der Sandbox: das ist eine Anzeige-Frage des eigenen Rechners, keine Weltregel. Vanilla speichert die
-- Seite selbst je Rechner in ModOptions.ini (V:client/PZAPI/ModOptions.lua:259-290, geladen V:client/OptionScreens/MainOptions.lua:2791);
-- im Mehrspieler gilt sie je Client, der Server kennt sie nicht und braucht sie nicht.
--
-- Bausteine: alles reines Vanilla-Lua (Tabellen, kein Engine-Aufruf) aus V:client/PZAPI/ModOptions.lua -- create :247-253,
-- addTitle :28-30, addTickBox :64-86, addSlider :206-228, getOptions :255-257, getOption :24-26, getValue :67 / :215; B1d:
-- addComboBox :121-156 (option.addItem :131-136 ruft getText(name) SOFORT beim Anlegen :132 -- also Schluessel; getValue :137 gibt
-- den INDEX 1..n der Auswahl, gespeichert als "combobox|Seite|Id|Index" :272-273, geladen :319-320). Gezeichnet von Vanillas
-- MainOptions.lua:2910-2933 (addCombo mit getText(option.name); den Tooltip einer Auswahl zeigt das Fenster nicht -- der
-- Schluessel steht trotzdem). Gelernt (nicht kopiert): NPC Crew benutzt addComboBox/addItem gespielt (NC:client/
-- BanditsNPCModOptions.lua:97-103). Aufrufer
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

-- Zwischenspeicher je Wert: { v = Wert oder nil, at = ms }. Gedeckelt durch die festen Ids dieser Seite (B1d: 5, B1e: 6, F1: 7, F1B: 9, F2: 10).
local cache = {}

local function err(msg)
    local f = B.Err
    if f then
        f(msg)
    else
        print("[TC-BEAR] *** " .. tostring(msg))
    end
end

-- F1B (PLAN_F1B.md 1.1, 3.1): Vorgabe-Tasten der zwei Zeilen unten -- Nah-Taste E (Vanillas Interact-Vorgabe, V:shared/keyBinding.lua:33
-- Keyboard.KEY_E), Fern-Taste keine (Keyboard.KEY_NONE, V:shared/keyBinding.lua:57 / :143 "-- 0"). Gelesen von U.BearKeys
-- (client/BanditsNPCBearKey.lua), auch wenn die Seite fehlt. Einziger Ort dieser zwei Zahlen.
U.KEY_DEF = { KeyNear = Keyboard.KEY_E, KeyFar = Keyboard.KEY_NONE }

-- ---------------------------------------------------------------------------
-- Die Seite (auf Dateiebene, wie Bandits B:client/BanditModOptions.lua:12-14)
-- ---------------------------------------------------------------------------
if PZAPI and PZAPI.ModOptions and PZAPI.ModOptions.create then
    local o = PZAPI.ModOptions:create(PAGE, "UI_BN_Bear_MO_Page")
    o:addTitle("UI_BN_Bear_MO_Title")
    -- Namensschild (Name und Zustand) ueber JEDEM gezaehmten Baeren, eigenen und fremden; der Zaehm-Balken ungezaehmter Junge bleibt.
    o:addTickBox("TagShow", "UI_BN_Bear_MO_TagShow", true, "UI_BN_Bear_MO_TagShowTip")
    -- B1d: Leben ueber jedem gezaehmten Baeren -- Index 1 Aus, 2 Balken (Vorgabe), 3 Zahl ("Health 92/150"). addComboBox :121,
    -- addItem :131 (zweites Argument true = Vorgabe, :133-135).
    local hp = o:addComboBox("TagHealth", "UI_BN_Bear_MO_Health", "UI_BN_Bear_MO_HealthTip")
    hp:addItem("UI_BN_Bear_MO_Off")
    hp:addItem("UI_BN_Bear_MO_Bar", true)
    hp:addItem("UI_BN_Bear_MO_Number")
    -- B1d: Ausdauer -- Index 1 Aus (Vorgabe), 2 Balken, 3 Zahl ("Stamina 40/50").
    local st = o:addComboBox("TagStamina", "UI_BN_Bear_MO_Stamina", "UI_BN_Bear_MO_StaminaTip")
    st:addItem("UI_BN_Bear_MO_Off", true)
    st:addItem("UI_BN_Bear_MO_Bar")
    st:addItem("UI_BN_Bear_MO_Number")
    -- B1d: Alter-Zeile ("Day 12 - half-grown in 3 day(s)"), Vorgabe an.
    o:addTickBox("TagAge", "UI_BN_Bear_MO_Age", true, "UI_BN_Bear_MO_AgeTip")
    -- Groesse von Schild UND Balken: 100 = Small (Stand B1b), 150 = Medium, 200 = Large. Stufen statt stufenlos, weil
    -- drawTextZoomed keinen Vanilla-Aufrufer hat (PLAN_B1C.md 0.8, Frage F8).
    o:addSlider("TagSize", "UI_BN_Bear_MO_TagSize", 100, 200, 50, 100, "UI_BN_Bear_MO_TagSizeTip")
    -- B1e (PLAN_B1E.md 1.7.9, 6.7; Kevin 11.11.2026: "waer cooler wenn das symbol was groesser waere zumindestens bei 4k aufloesung"):
    -- Groesse der Markierung oben am Bildschirm (client/ISUI/BanditsNPCBearMarker.lua). Index 1 Auto (Vorgabe: waechst mit der
    -- Bildschirmhoehe, 1080 = 100 %, 4K = 200 %), 2..7 = 100 / 125 / 150 / 200 / 250 / 300 %. addComboBox :121, addItem :131.
    local mk = o:addComboBox("MarkerSize", "UI_BN_Bear_MO_MarkerSize", "UI_BN_Bear_MO_MarkerSizeTip")
    mk:addItem("UI_BN_Bear_MO_Auto", true)
    mk:addItem("UI_BN_Bear_MO_Pct100")
    mk:addItem("UI_BN_Bear_MO_Pct125")
    mk:addItem("UI_BN_Bear_MO_Pct150")
    mk:addItem("UI_BN_Bear_MO_Pct200")
    mk:addItem("UI_BN_Bear_MO_Pct250")
    mk:addItem("UI_BN_Bear_MO_Pct300")
    -- F1 (PLAN_F1.md 1.7; Kevin 11.11.2026: "das schoene ui", 4K darf nicht winzig sein): Groesse des Baeren-Fensters, Index 1 Auto
    -- (Vorgabe: 1080 = 100 %, 4K = 200 %), 2..7 = 100 / 125 / 150 / 200 / 250 / 300 %. addComboBox :121, addItem :131.
    local ws = o:addComboBox("WinSize", "UI_BN_Bear_MO_WinSize", "UI_BN_Bear_MO_WinSizeTip")
    ws:addItem("UI_BN_Bear_MO_Auto", true)
    ws:addItem("UI_BN_Bear_MO_Pct100")
    ws:addItem("UI_BN_Bear_MO_Pct125")
    ws:addItem("UI_BN_Bear_MO_Pct150")
    ws:addItem("UI_BN_Bear_MO_Pct200")
    ws:addItem("UI_BN_Bear_MO_Pct250")
    ws:addItem("UI_BN_Bear_MO_Pct300")
    -- F2 (PLAN_F2.md 3.2): "DODGE" ueber dem eigenen Baeren an/aus (Vorgabe an). addTickBox :64-86 wie TagShow oben.
    o:addTickBox("TagDodge", "UI_BN_Bear_MO_Dodge", true, "UI_BN_Bear_MO_DodgeTip")
    -- F1B (PLAN_F1B.md 3.1; Kevin 12.11.2026, Kopf dieser Datei): die zwei Tasten des Baeren-Fensters. addTitle :28-30 (gezeichnet mit
    -- getText, V:client/OptionScreens/MainOptions.lua:2803-2804); addKeyBind :182-204 mit SCHON UEBERSETZTEM Namen (getText wie
    -- B:client/BanditModOptions.lua:14 -- Grund im Kopf), Tooltip als Schluessel. Vorgaben aus U.KEY_DEF (oben).
    o:addTitle("UI_BN_Bear_MO_Keys")
    o:addKeyBind("KeyNear", getText("UI_BN_Bear_MO_KeyNear"), U.KEY_DEF.KeyNear, "UI_BN_Bear_MO_KeyNearTip")
    o:addKeyBind("KeyFar", getText("UI_BN_Bear_MO_KeyFar"), U.KEY_DEF.KeyFar, "UI_BN_Bear_MO_KeyFarTip")
    -- Spaeter (NICHT jetzt anlegen; ENTSCHEIDUNGEN.md "Anzeige ueber dem Baeren"): Hunger, Durst, Muedigkeit je als Auswahl
    -- Aus / Balken / Zahl wie TagHealth, sobald es die Werte gibt (Beduerfnisse, Schlafen). "DODGE" steht seit F2 oben (TagDodge).
    -- Gelesen wird alles ueber U.Opt(id, vorgabe); jeder neue Schluessel in allen sieben UI.json.
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
