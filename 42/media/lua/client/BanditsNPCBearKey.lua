--
-- NPC Crew -- Baer, Taste fuer das Baeren-Fenster (F1, PLAN_F1.md 0.9, 3.1, 3.2; Kevin 11.11.2026: "eine richtige UI die aufgeht wenn
-- ich V druecke (einstellbar in den keystings)").
--
-- Eine Zeile in Vanillas Tastenbelegung (Optionen -> Tastaturbelegung), eigener Abschnitt "[NPC Crew Bear]", Name "Bear window",
-- Vorgabe V. Vanilla laedt und speichert die Taste selbst (MainOptions.loadKeys / saveKeys, keysB42.ini); der NAME ist dort fuer
-- immer die Kennung -- nie umbenennen (Lehre NPC Crew NC:client/BanditsNPCInteract.lua:19-34). Die Zeile muss auf Dateiebene
-- stehen: Mod-Dateien laden vor Vanillas loadKeys (Lehre NC:client/ISUI/BanditsNPCBeaconWindow.lua:166-172, gespielt).
-- Beschriftung: getText("UI_optionscreen_binding_" .. Name ohne Klammern) (V:client/OptionScreens/MainOptions.lua:2165, :2177) ->
-- Schluessel "UI_optionscreen_binding_NPC Crew Bear" und "UI_optionscreen_binding_Bear window" in allen sieben UI.json.
--
-- V liegt auch auf Vanillas Fahrzeug- und Tier-Radial (V:shared/keyBinding.lua:131-132, :186-187) und auf NPC Crews "Talk to NPC"
-- (NC:client/BanditsNPCInteract.lua:7462). Vorfahrt (PLAN_F1.md 3.2): NPC-Gespraech > Fahrzeug-Radial > Radial eines FREMDEN Tiers >
-- Baeren-Fenster. Am eigenen Baeren oeffnet das Fenster und schliesst Vanillas Tier-Radial, falls es aufging (FF 1.3 Weg b).
-- Nachbesserung F1 A2: "fremd" ist auch der gezaehmte Baer eines ANDEREN Spielers (Sicht: Besitzer nicht ich) -- dort bleibt Vanillas
-- Radial, das Fenster geht nicht auf. Eigene Baeren (jeder Zustand), Baeren ohne Besitzer und ungekannte unserer Art zaehlen als "unser".
-- Nachbesserung F1 B9: Vanillas Tier-Radial an UNSEREM Baeren (nicht wild; mit Waffe enthaelt es "Kill",
-- V:client/ISUI/Animal/ISAnimalContextMenu.lua:1170-1176) geht schon beim Druecken auf (V:client/ISUI/ISUIHandler.lua:35-57) -- es wird
-- sofort wieder geschlossen, solange die Taste gehalten wird (OnKeyStartPressed / OnKeyKeepPressed, unabhaengig von der Belegung
-- "Bear window"; wie im Rechtsklick-Menue kein "Kill" am Baeren, client/BanditsNPCBearMenu.lua). Nicht, wenn ein Fahrzeug Vorfahrt hat.
-- Liegt "Bear window" auf einer anderen Taste, greift keine Vorfahrt (die isKey-Fragen sind dann falsch).
-- Nur Spieler 0. Laeuft beim Loslassen der Taste (OnKeyPressed); waehrend die Radial-Taste gehalten wird, je Bild nur die Frage, ob ein
-- Radial offen ist (das Tier erst dann). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local NAME = "Bear window"          -- Kennung in keysB42.ini, fuer immer stabil
local HEAD = "[NPC Crew Bear]"      -- Abschnitt der Tastaturbelegung
local REOPEN_MS = 250               -- so lange nach dem Schliessen oeffnet dieselbe Taste nicht wieder (U.winClosedAt)

-- Gibt es die Zeile schon (zweites Laden, NPC Crew mit derselben Zeile)? Schleife ueber keyBinding wie
-- NC:client/ISUI/BanditsNPCFarmPanel.lua:1250-1255 (reines Lua).
local function has(value)
    for _, row in ipairs(keyBinding) do
        if type(row) == "table" and row.value == value then return true end
    end
    return false
end

-- Anlegen auf Dateiebene (V:shared/keyBinding.lua:6 Tabelle, Form :8-14; Keyboard.KEY_V :132). Doppel-Riegel: nur einmal.
if type(keyBinding) == "table" and not has(NAME) then
    if not has(HEAD) then table.insert(keyBinding, { value = HEAD }) end
    table.insert(keyBinding, { value = NAME, key = Keyboard.KEY_V })
end

-- Name der belegten Taste fuer die Fusszeile des Fensters ("V or Esc closes"), sonst nil (Taste nicht belegt).
-- getKeyName(getCore():getKey(Text)): V:client/Tutorial/Tutorial1.lua:177.
function U.WinKeyName()
    local k = getCore():getKey(NAME)
    if type(k) ~= "number" or k <= 0 then return nil end
    local n = getKeyName(k)
    if type(n) ~= "string" or n == "" then return nil end
    return n
end

-- Das Tier vor dem Spieler: "ours" (unsere Art, nicht fremd), "foreign" (Baer unserer Art eines anderen Spielers) oder nil (kein Baer
-- unserer Art). getAnimalToInteractWith: V:client/ISUI/ISUIHandler.lua:44; B.BodyKind / B.ViewOf (Kern, nur lesend); U.WinMine (WinData).
local function bearKind(p)
    local an = AnimalContextMenu.getAnimalToInteractWith(p)
    if not an or B.BodyKind == nil or B.BodyKind(an) == nil then return nil, an end
    local v = nil
    if B.ViewOf then v = B.ViewOf(an) end
    if v ~= nil and v.owner ~= nil and U.WinMine and not U.WinMine(v) then return "foreign", an end
    return "ours", an
end

-- Vanillas Tier-Radial schliessen, wenn es offen ist (getPlayerRadialMenu(0), isReallyVisible, undisplay:
-- V:client/ISUI/ISUIHandler.lua:91-92, V:client/ISUI/Animal/ISAnimalContextMenu.lua:1157-1164).
local function closeRadial()
    local menu = getPlayerRadialMenu(0)
    if menu and menu:isReallyVisible() then menu:undisplay() end
end

-- B9: Radial-Taste gedrueckt / gehalten (Form key wie V:client/ISUI/ISUIHandler.lua:35 bzw. V:client/Hotbar/ISHotbar.lua:782).
-- Erst die billigen Fragen (Taste, Radial offen), dann Fahrzeug und Tier.
local function onRadialKey(key)
    if not getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key) then return end    -- V:client/ISUI/ISUIHandler.lua:37
    local menu = getPlayerRadialMenu(0)                                          -- V:client/ISUI/ISUIHandler.lua:91
    if not menu or not menu:isReallyVisible() then return end                    -- :92
    local p = getSpecificPlayer(0)                                               -- V:client/Farming/CFarmingSystem.lua:45
    if not p or p:isDead() then return end                                       -- V:client/ISUI/ISUIHandler.lua:42
    if ISVehicleMenu.getVehicleToInteractWith(p) then return end                 -- :43 (dann ist es das Fahrzeug-Radial)
    local kind, _ = bearKind(p)
    if kind == "ours" then menu:undisplay() end                                  -- V:client/ISUI/Animal/ISAnimalContextMenu.lua:1164
end

-- Vorfahrt und Oeffnen (PLAN_F1.md 3.2). Jeder Weg nur lesend; keine NPC-Crew-Datei wird geaendert.
local function openKey(key)
    if not getCore():isKey(NAME, key) then return end                      -- V:client/ISUI/FPS.lua:9 (isKey mit Text)
    if ISChat and ISChat.focused then return end                            -- V:client/Chat/ISChat.lua:8
    -- B10: das Namensfeld des Fensters ist offen (auch ohne Fokus) -> die Taste schliesst das Fenster nicht (client/ISUI/...Window.lua)
    if U.WinTyping and U.WinTyping() then return end
    local p = getSpecificPlayer(0)                                          -- V:client/Farming/CFarmingSystem.lua:45
    if not p or p:isDead() then return end                                  -- V:client/ISUI/ISUIHandler.lua:42
    local closed = U.winClosedAt
    if type(closed) == "number" then
        local now = getTimestampMs()                                        -- V:client/Foraging/ISBaseIcon.lua:485
        if now >= closed and now - closed < REOPEN_MS then return end
    end
    -- 1. NPC Crew zuerst: liegt die Taste auch auf "Talk to NPC" und steht ein NPC vor dem Spieler, gewinnt das Gespraech
    -- (NC:client/BanditsNPCInteract.lua:35 KEYBIND, :41 FindTarget, nur lesend). Existenz-Riegel: ohne NPC Crew still.
    local ia = BanditsNPC.Interact
    if type(ia) == "table" and ia.KEYBIND and ia.FindTarget and getCore():isKey(ia.KEYBIND, key) and ia.FindTarget(p) then
        return
    end
    -- 2. Fahrzeug-Radial (V:client/ISUI/ISUIHandler.lua:36, :43): im oder am Auto gehoert V dem Fahrzeug.
    if getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU, key) and ISVehicleMenu.getVehicleToInteractWith(p) then return end
    -- 3. Tier-Radial eines FREMDEN Tiers (ISUIHandler.lua:37, :44; isWild V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171) -- auch
    -- eines fremden Baeren (A2). Unser Baer ist es, wenn B.BodyKind (Kern, einziger Art-Vergleich) "cub" oder "big" sagt.
    local ours = false
    if getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key) then
        local kind, an = bearKind(p)
        if kind == "foreign" then return end
        ours = kind == "ours"
        if an and not ours and not an:isWild() then return end
    end
    -- 4. Das Baeren-Fenster (auf / zu)
    if U.WinToggle then U.WinToggle(p) end
    -- Am eigenen Baeren ein offenes Tier-Radial schliessen
    if ours then closeRadial() end
end

-- Loslassen einer Taste: erst Fenster (eigene Taste), dann B9 (Radial-Taste, unabhaengig von der Belegung "Bear window").
local function onKey(key)
    openKey(key)
    onRadialKey(key)
end

-- Nur einmal anmelden (wird die Datei ein zweites Mal geladen, oeffnete und schloesse dieselbe Taste sonst sofort wieder).
if not U.keyHooked then
    U.keyHooked = true
    Events.OnKeyPressed.Add(onKey)                                          -- V:client/ISUI/FPS.lua:20
    -- B9: Vanillas Radial-Handler meldet sich erst in OnGameStart an (V:client/ISUI/ISUIHandler.lua:101-104) und laeuft damit NACH
    -- unserem OnKeyStartPressed -- das Radial geht danach auf; OnKeyKeepPressed schliesst es im naechsten Bild, onKey (oben) beim
    -- Loslassen (kurzer Tipp, Vanilla-Option "Radial-Menue per Taste umschalten", Taste "Bear window" anders belegt)
    Events.OnKeyStartPressed.Add(onRadialKey)                               -- V:client/ISUI/ISUIHandler.lua:102
    Events.OnKeyKeepPressed.Add(onRadialKey)                                -- V:client/Hotbar/ISHotbar.lua:890
end
