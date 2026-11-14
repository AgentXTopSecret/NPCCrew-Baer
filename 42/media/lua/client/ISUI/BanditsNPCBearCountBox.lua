--
-- NPC Crew -- Baer, Zahlenfeld "Wie viele?" fuer das Inventar-Fenster (K1, Lauf baer-k1, PLAN_K1.md 1.4, 5; Kevin 14.11.2026 ~00:10: "ich will
-- bei geben eine auswahl bkeommen wo ich eine zahl eintippe", ~00:15 "Ja, auch Nehmen").
--
-- Genau Vanillas Mengen-Feld (V:client/ISUI/Animal/ISAnimalContextMenu.lua:790-799, Wolle-Menge): ISTextBox mit setOnlyNumbers(true), dazu eine
-- eigene Pruefung wie unser Namensfeld (client/ISUI/BanditsNPCBearNameBox.lua): OK nur bei einer GANZEN Zahl von 1 bis max (sonst OK grau mit
-- Hinweis -- auch fuer "-", "." oder Leerzeichen, falls das Feld sie zulaesst, Pruef-Tor G-K3). Das Fenster entscheidet nichts: OK ruft nur
-- onOk(n) des Aufrufers (Inventar-Fenster), der die Gruppe / den Satz frisch holt, klemmt und genau EINE Zeitaktion anstellt -- ob es gilt,
-- entscheidet der Schreiber in complete(). Abbrechen tut nichts. Kein Warten auf den Server, nichts haengt.
-- ISTextBox wird erst beim Klick gebraucht (dann ist Vanillas client/ISUI/ISTextBox.lua laengst geladen): kein require.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local DIGITS_MAX = 7        -- mehr Ziffern sind immer Unsinn (Deckel 1000); schuetzt tonumber vor riesigen Zahlen

-- Ganze Zahl 1 .. max aus dem Text, sonst nil. Nur Ziffern (fuehrende / folgende Leerzeichen erlaubt). Reine Lua-Rechnung.
local function countOf(text, max)
    if type(text) ~= "string" then return nil end
    local d = string.match(text, "^%s*(%d+)%s*$")
    if d == nil or string.len(d) > DIGITS_MAX then return nil end
    local n = tonumber(d)
    if n == nil or n < 1 or n > max then return nil end
    return math.floor(n)
end
U.CountOf = countOf

-- Antwort des Fensters. ISTextBox ruft onclick(Ziel, Knopf, param1) (V:client/ISUI/ISTextBox.lua:133-134); Ziel ist der Spieler, param1 die
-- Tabelle { max, onOk }. button.internal == "OK" und button.parent.entry:getText(): V:client/ISUI/Animal/ISAnimalContextMenu.lua:802-804.
local function onCountClick(_playerObj, button, st)
    if not button or button.internal ~= "OK" then return end
    if type(st) ~= "table" or type(st.onOk) ~= "function" then return end
    local n = countOf(button.parent.entry:getText(), st.max)
    if n == nil then return end
    st.onOk(n)
end

-- U.AskCount(playerObj, title, bd, def, max, onOk): Fenster "Wie viele?" mit dem Text title (Schluessel; %1 = max; U.TB waehlt beim grossen
-- Koerper die Big-Fassung, wenn es sie gibt), vorbelegt mit def (auf 1 .. max geklemmt). Rueckgabe das Fenster oder nil (max < 1 / Unsinn).
-- ISTextBox:new(x, y, w, h, Titel, Vorgabe, Ziel, Rueckruf, Spielernummer, param1): Signatur V:client/ISUI/ISTextBox.lua:280; Masse 280 x 180
-- und initialise / addToUIManager / setOnlyNumbers(true) wie V:client/ISUI/Animal/ISAnimalContextMenu.lua:791-794; getPlayerNum():
-- V:client/ISUI/Animal/ISAnimalContextMenu.lua:1069; setValidateFunction(Ziel, f) / setValidateTooltipText(Text): V:client/ISUI/ISTextBox.lua:111-119
-- (gelesen in updateButtons :170-177), wie client/ISUI/BanditsNPCBearNameBox.lua. Joypad: getJoypadFocus / centerOnScreen / setJoypadFocus wie
-- V:client/ISUI/Animal/ISAnimalUI.lua:464-468.
function U.AskCount(playerObj, title, bd, def, max, onOk)
    if not playerObj or type(onOk) ~= "function" then return nil end
    max = math.floor(tonumber(max) or 0)
    if max < 1 then return nil end
    def = math.floor(tonumber(def) or max)
    if def ~= def or def < 1 then def = 1 end
    if def > max then def = max end
    local nr = playerObj:getPlayerNum()
    local st = { max = max, onOk = onOk }
    local modal = ISTextBox:new(0, 0, 280, 180, U.TB(title, bd, max), string.format("%d", def), playerObj, onCountClick, nr, st)
    modal:initialise()
    modal:addToUIManager()
    modal:setOnlyNumbers(true)
    modal:setValidateFunction(nil, function(_target, text) return countOf(text, max) ~= nil end)
    modal:setValidateTooltipText(U.T("UI_BN_Bear_Inv_CountBad", max))
    if getJoypadFocus(nr) then
        modal:centerOnScreen(nr)
        modal.prevFocus = getJoypadFocus(nr)
        setJoypadFocus(nr, modal)
    end
    return modal
end
