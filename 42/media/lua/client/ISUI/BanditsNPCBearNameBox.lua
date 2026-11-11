--
-- NPC Crew -- Baer, Eingabefenster "Name the cub" (B1b, PLAN_B1B.md 3.1, 5.4).
--
-- Genau wie Vanillas Tier-Umbenennen (client/ISUI/Animal/ISAnimalUI.lua:459-485): ISTextBox mit Laengengrenze, leer gesperrt,
-- eigene Zeichenpruefung (B.CleanName des Kerns, dieselbe Regel wie beim Schreiber), Joypad-Fokus. Das Fenster PRUEFT nur vor;
-- es schickt den rohen Text als Bitte "Rename" (B.Ask). Ob und wie der Name gilt, entscheidet der Schreiber (Einzelspieler:
-- dasselbe Programm; Mehrspieler: der Server, der dann allen in der Naehe die neue Sicht schickt). Der Name lebt nur im
-- Register (Plan 0.3) -- kein Vanilla-Tiername am Tier, Vanillas Tier-Info zeigt weiter "Bear cub".
-- Laeuft nur auf Klick. Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
-- ISTextBox wird erst beim Klick gebraucht (dann ist Vanillas client/ISUI/ISTextBox.lua laengst geladen): kein require.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local NAME_MAX = 24     -- Rueckfall fuer B.CFG.nameMax (Plan 1.7)

local function nameMax()
    local n = B.CFG and tonumber(B.CFG.nameMax)
    if not n or n < 1 then return NAME_MAX end
    return math.floor(n)
end

-- Pruefer des Fensters: ISTextBox ruft ihn in updateButtons (bei jedem Zeichnen, solange das Fenster offen ist) mit (Ziel, Text)
-- (client/ISUI/ISTextBox.lua:173-177; falsch -> OK grau mit dem Hinweis aus setValidateTooltipText). Reine Regel des Kerns
-- (shared, kein Engine-Aufruf, hoechstens nameMax Zeichen). Fehlt die Kern-Datei, entscheidet allein der Schreiber.
local function validName(_target, text)
    local clean = B.CleanName
    if not clean then return true end
    return clean(text) ~= nil
end

-- Antwort des Fensters. ISTextBox ruft onclick(Ziel, Knopf, param1) (client/ISUI/ISTextBox.lua:133-134); Ziel ist der Spieler,
-- param1 die Kennung des Jungen. button.internal == "OK" und button.parent.entry:getText(): client/ISUI/Animal/ISAnimalUI.lua:471-473.
-- Abbrechen tut nichts.
local function onNameClick(playerObj, button, id)
    if not button or button.internal ~= "OK" then return end
    if not playerObj or id == nil then return end
    local text = button.parent.entry:getText()
    if type(text) ~= "string" then return end
    B.Ask(playerObj, "Rename", { id = id, name = text })
end

-- Fenster oeffnen, vorbelegt mit dem aktuellen Namen (leer, wenn das Junge noch keinen hat).
-- ISTextBox:new(x, y, w, h, Titel, Vorgabe, Ziel, Rueckruf, Spielernummer, param1): Signatur client/ISUI/ISTextBox.lua:280;
-- so mit Spielernummer und param1 client/ISUI/ISInventoryPage.lua:1912; Masse 280 x 180 wie ISAnimalUI.lua:460.
-- getPlayerNum(): client/ISUI/Animal/ISAnimalContextMenu.lua:1069. initialise / addToUIManager / maxChars: ISAnimalUI.lua:461-463.
-- noEmpty: client/ISUI/Maps/ISWorldMapSymbols.lua:203. setValidateFunction(Ziel, f): client/OptionScreens/CharacterCreationProfession.lua:1297.
-- setValidateTooltipText(Text): Vanillas eigenes Lua (client/ISUI/ISTextBox.lua:117-119, setzt nur das Feld, gelesen :176).
-- maxChars wirkt ueber ISTextBox.lua:178-181 (OK grau, Vanilla-Hinweis IGUI_TextBox_TooManyChar), noEmpty ueber :182-185.
-- entry:setMaxTextLength(n): client/ISUI/ISMPEditAccount.lua:19 (ISTextEntryBox, client/ISUI/ISTextEntryBox.lua:170-171; das Feld
-- entsteht in ISTextBox:initialise, ISTextBox.lua:20). Joypad: getJoypadFocus / centerOnScreen / setJoypadFocus wie ISAnimalUI.lua:464-468.
function U.AskName(playerObj, v)
    if not playerObj or type(v) ~= "table" or v.id == nil then return nil end
    local max = nameMax()
    local nr = playerObj:getPlayerNum()
    local current = ""
    if type(v.name) == "string" then current = v.name end
    local modal = ISTextBox:new(0, 0, 280, 180, U.T("UI_BN_Bear_Name_Title"), current, playerObj, onNameClick, nr, v.id)
    modal:initialise()
    modal:addToUIManager()
    modal.maxChars = max
    modal.noEmpty = true
    modal:setValidateFunction(nil, validName)
    modal:setValidateTooltipText(U.T("UI_BN_Bear_Why_NameBad", max))
    if modal.entry then modal.entry:setMaxTextLength(max) end
    if getJoypadFocus(nr) then
        modal:centerOnScreen(nr)
        modal.prevFocus = getJoypadFocus(nr)
        setJoypadFocus(nr, modal)
    end
    return modal
end
