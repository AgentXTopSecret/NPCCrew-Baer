--
-- NPC Crew -- Baer, Tasten fuer das Baeren-Fenster (F1B, PLAN_F1B.md 0 E1-E8, 1.1-1.8; Kevin 12.11.2026: "das fenster geht auf V auf
-- aber das war eigtl so gemeint wenn man in der naehe ist wie bei den npc's ... deswegen schlag ich vor bei E das baeren ui zu oeffnen
-- und wenn man es aus der ferne oeffnen will dann kann man beim UI den hotkey festelegen ... die E taste fuer den baeren wenn man in
-- der naehe ist in sen mod settings zum aendern eintragen falls jemand nicht E nutzen will sondern einen anderen key").
--
-- Zwei Tasten auf der eigenen Seite Optionen -> Mods -> "NPC Crew: Bear" (client/BanditsNPCBearOptions.lua, Vorgaben U.KEY_DEF):
--   * Nah-Taste "KeyNear" (Vorgabe E): steht der Spieler nahe am EIGENEN zahmen Baeren -- wie NPC Crews V bei NPCs: 3,5 Kacheln (2D),
--     gleiche Etage, im Blick (unter 1,5 Kacheln egal), bei mehreren gewinnt das kleinste "Abstand - Blick"
--     (NC:client/BanditsNPCInteract.lua:36, :57, :61-65) --, oeffnet sie das Fenster mit DIESEM Baeren. Kein eigener Baer nah: NICHTS
--     (kein Hinweis, keine Frage an den Server; E bleibt Vanillas Interact, z. B. Tueren -- Lehre NC:client/BanditsNPCInteract.lua:120-139).
--   * Fern-Taste "KeyFar" (Vorgabe KEINE): oeffnet aus jeder Entfernung (das alte V-Verhalten: U.WinOpen ohne Kennung -> naechster
--     eigener Baer, "You do not have a bear yet.", vermisst / nicht geladen mit Zustand). Liegt sie auf Vanillas Interact (E), bleibt
--     sie ohne Sicht oder ohne eigenen Baeren STILL wie die Nah-Taste (Nachbesserung F1B B2: sonst ein Hinweis bei jedem E).
--   * Jede der beiden schliesst ein offenes Fenster immer (E7). Das Fenster selbst verbraucht nur noch Esc (E8,
--     client/ISUI/BanditsNPCBearWindow.lua) -- V gehoert wieder NPC Crew ("Talk to NPC") und Vanilla (Tier-/Fahrzeug-Radial).
-- E bleibt immer AUCH Vanillas Taste (Lua-Ereignisse haben keine Rueckgabe, Java liest den Tastenzustand selbst -- forschung_f1b.md 2.2).
-- Doppelte Wirkung vermeiden wir nur durch Zurueckhaltung: liegt unsere Taste gerade auf Vanillas Interact
-- (getCore():isKey(KeybindId.INTERACT, key), V:client/Farming/CFarming_Interact.lua:28), oeffnet sie NICHT bei Tuer/Fenster/Fensterrahmen
-- vor oder hinter dem Spieler, Zaun/Mauer zum Klettern, mitten im Klettern, im/am Fahrzeug, beim Zielen, mit Leiche,
-- schlafend/gesperrt, nach langem Druck (>= 0,5 s), mit Bau-/Moebel-Cursor beim Druecken oder wenn ein ANDERES Tier Vanillas E-Ziel ist
-- (PLAN_F1B.md 1.4 I). Kein
-- setIgnoreContextKey (bliebe es haengen, ginge keine Tuer mehr). Liegt etwas Fremdes auf DERSELBEN Taste (NC "Talk to NPC" mit NPC vor
-- dem Spieler, NC-Station mit "[E]"-Hinweis in 2,2 Kacheln, Vanillas Fahrzeug-Radial, Vanillas Tier-Radial an einem fremden Tier), geht
-- das vor (1.4 F) -- alles nur lesend, hinter Existenz-Riegeln, keine NPC-Crew-Datei wird geaendert.
-- Keine Zeile mehr in Vanillas keyBinding (die alte "Bear window"-Zeile in keysB42.ini ueberliest Vanilla still,
-- V:client/OptionScreens/MainOptions.lua:3545, :3577). Vanillas Tier-Radial am Baeren bleibt offen -- ohne "Kill" macht es
-- client/BanditsNPCBearMenu.lua (Huelle um AnimalContextMenu.showRadialMenu, E9). Nur wenn eine UNSERER Tasten selbst auf Vanillas
-- Tier-Radial-Taste liegt und am eigenen Baeren das Fenster oeffnet oder schliesst, geht das Radial mit zu (Nachbesserung F1B B1, wie
-- F1) -- sonst blieben im Umschalt-Modus Radial und Fenster zugleich offen.
-- Nur Spieler 0. Gerechnet wird nur beim Druecken (Zeitstempel, Cursor) und beim Loslassen (alles andere) -- nie je Bild. Keine
-- Fehler-Tarnkappe (pcall): jeder Engine-Aufruf hat eine Fundstelle (Kommentar daneben). Tasten sind reine Client-Sache; die Befehle
-- im Fenster gehen wie in F1 als Bitte an den Schreiber. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Stellwerte (PLAN_F1B.md 1.5): Nah-Radius, "egal wohin er schaut", Blick-Grenze (wie NC Interact.lua:36, :64), langer Druck (Javas
-- Kontext-Grenze 0,5 s, NUR JAR forschung_f1b.md 2.3), Sperre nach dem Schliessen (U.winClosedAt), Stations-Radius (NC
-- NC:client/ISUI/BanditsNPCBeaconPrompt.lua:23).
local NEAR_R, NEAR_ANY, DOT_MIN, HOLD_MS, REOPEN_MS = 3.5, 1.5, 0.2, 500, 250
local STATION_R = 2.2
local DIAG_K = 0.7071                -- 1 / Wurzel 2: schraeger Blick als Einheitsvektor

-- Nur der letzte Druck EINER unserer Tasten (gedeckelt: ein Eintrag): Taste, Zeitstempel, Cursor beim Druecken.
local K = { key = nil, at = 0, drag = false }
-- Vanillas "nutzbares Tier" je Loslassen hoechstens einmal (PLAN_F1B.md 1.3): gebraucht von Riegel I, Rueckfall 1.5 und Vorfahrt F.
local UA = { done = false, an = nil, p = nil }
-- Schraege Blickrichtungen: { Blick, vorn 1, vorn 2, hinten 1, hinten 2 } -- Zerlegung wie V:client/ISUI/ISButtonPrompt.lua:448-462
-- (vorn) und :468-481 (hinten). Einmal gebaut, nie je Druck; verglichen wird mit == wie Vanilla.
local DIAG = nil

-- ---------------------------------------------------------------------------
-- 1.1 Tasten lesen (je Druck). U.Opt (client/BanditsNPCBearOptions.lua, 1-s-Zwischenspeicher) liest
-- getOptions(Seite):getOption(id):getValue() -> Tastencode (V:client/PZAPI/ModOptions.lua:191; Lese-Form B:shared/BanditCompatibility.lua:96-101).
-- 0 (oder weniger) heisst "keine Taste" (Keyboard.KEY_NONE, V:shared/keyBinding.lua:143) -- anders als NPC Crew, das 0 als "Vorgabe" deutet.
-- Verglichen wird nur der rohe Code: die Mod-Optionen speichern keine Zusatztasten (V:client/PZAPI/ModOptions.lua:276-280).
-- ---------------------------------------------------------------------------
local function keyOf(id)
    local def = (U.KEY_DEF and U.KEY_DEF[id]) or 0
    local k = def
    if U.Opt then k = tonumber(U.Opt(id, def)) end
    if k == nil or k <= 0 then return nil end
    return math.floor(k)
end

-- -> near, far: Tastencode oder nil
function U.BearKeys()
    return keyOf("KeyNear"), keyOf("KeyFar")
end

-- Anzeige-Name einer Taste ("E", "F7") oder nil. getKeyName(Zahl): V:client/OptionScreens/MainOptions.lua:2991,
-- V:client/ISUI/ISDuplicateKeybindDialog.lua:17.
local function nameOf(code)
    if code == nil then return nil end
    local n = getKeyName(code)
    if type(n) ~= "string" or n == "" then return nil end
    return n
end

-- Fuer die Fusszeile des Fensters (client/BanditsNPCBearWinData.lua): -> nearName, farName (je Name oder nil).
function U.WinKeyName()
    local near, far = U.BearKeys()
    return nameOf(near), nameOf(far)
end

-- ---------------------------------------------------------------------------
-- Vanillas nutzbares Tier (AnimalContextMenu.getAnimalToInteractWith(p), V:client/ISUI/ISUIHandler.lua:44) -- je Loslassen einmal.
-- ---------------------------------------------------------------------------
local function useableReset(p)
    UA.done, UA.an, UA.p = false, nil, p
end

local function useable()
    if UA.done then return UA.an end
    UA.done = true
    local acm = AnimalContextMenu
    if UA.p ~= nil and type(acm) == "table" and type(acm.getAnimalToInteractWith) == "function" then
        UA.an = acm.getAnimalToInteractWith(UA.p)                           -- V:client/ISUI/ISUIHandler.lua:44
    end
    return UA.an
end

-- Das Tier: "ours" (unsere Art, nicht fremd), "foreign" (Baer unserer Art eines ANDEREN Spielers) oder nil (kein Baer unserer Art).
-- Wie F1 (Nachbesserung A2), aber mit uebergebenem Tier. B.BodyKind / B.ViewOf (Kern, nur lesend); U.WinMine (WinData).
local function bearKind(an)
    if not an or B.BodyKind == nil or B.BodyKind(an) == nil then return nil end
    local v = nil
    if B.ViewOf then v = B.ViewOf(an) end
    if v ~= nil and v.owner ~= nil and U.WinMine and not U.WinMine(v) then return "foreign" end
    return "ours"
end

-- ---------------------------------------------------------------------------
-- 1.4 G -- Grundriegel, jede unserer Tasten (auch zum Schliessen). Textfelder und Vanillas Tasten-Dialog brauchen keinen Riegel: dort
-- feuert die Engine gar kein OnKeyPressed (NUR JAR, forschung_f1b.md 2.3 -- Testpunkt im Spiel, Nachbesserung F1B A5).
-- ---------------------------------------------------------------------------
local function blockedBase(p)
    if p == nil or p:isDead() then return true end                         -- V:client/ISUI/ISUIHandler.lua:42
    if ISChat and ISChat.focused then return true end                       -- V:client/Chat/ISChat.lua:8
    if U.WinTyping and U.WinTyping() then return true end                   -- Namensfeld offen (client/ISUI/BanditsNPCBearWindow.lua)
    local ms = MainScreen and MainScreen.instance
    if ms and ms.inGame and ms:isReallyVisible() then return true end        -- V:client/ISUI/Gamepad/JoyPadSetup.lua:280
    return false
end

-- ---------------------------------------------------------------------------
-- 1.4 I -- Interact-Riegel (nur wenn unsere Taste gerade Vanillas Interact ist). Jeder Aufruf mit Vanilla-Fundstelle, gleiche Typen.
-- ---------------------------------------------------------------------------
local function diag()
    if DIAG then return DIAG end
    local D = IsoDirections                                                 -- V:client/ISUI/ISButtonPrompt.lua:448-481
    DIAG = { { D.NE, D.N, D.E, D.S, D.W }, { D.SE, D.S, D.E, D.N, D.W }, { D.SW, D.S, D.W, D.N, D.E },
        { D.NW, D.N, D.W, D.S, D.E } }
    return DIAG
end

-- Tuer / Fenster / Fensterrahmen in Richtung d: p:getContextDoorOrWindowOrWindowFrame(IsoDirections) V:client/ISUI/ISButtonPrompt.lua:513
-- (dahinter :487, :494).
local function doorAt(p, d)
    return d ~= nil and p:getContextDoorOrWindowOrWindowFrame(d) ~= nil
end

-- Zaun / Mauer zum Klettern in Richtung d: p:hopFence(d, true) (true = nur pruefen) V:client/ISUI/ISButtonPrompt.lua:846,
-- p:canClimbOverWall(d) :851.
local function climbAt(p, d)
    if d == nil then return false end
    if p:hopFence(d, true) then return true end
    return p:canClimbOverWall(d) == true
end

local function busy(p, held, drag, useableFn)
    if held >= HOLD_MS then return true end                                 -- langer Druck (Zeitstempel aus onKeyStart)
    if drag then return true end                                            -- Cursor beim Druecken (V:server/BuildingObjects/ISMoveableCursor.lua:44-57)
    if p:getVehicle() ~= nil or p:getUseableVehicle() ~= nil then return true end   -- V:client/Vehicles/ISUI/ISVehicleMenu.lua:245-247
    if p:isAiming() then return true end                                    -- V:client/Farming/CFarming_Interact.lua:37
    if p:isDraggingCorpse() or p:isGrappling() then return true end         -- V:client/ISUI/ISButtonPrompt.lua:695; V:shared/TimedActions/ISGrabCorpseAction.lua:140
    if p:isAsleep() or p:getIgnoreMovement() then return true end           -- V:client/ISUI/ISButtonPrompt.lua:440
    if p:isClimbing() then return true end                                  -- Klettern (Nachbesserung F1B B3): V:client/ISUI/ISFitnessUI.lua:260
    local dir = p:getDir()                                                  -- V:client/ISUI/ISButtonPrompt.lua:378
    if dir ~= nil then
        local f1, f2, b1, b2 = dir, nil, nil, nil
        local rows = diag()
        local slant = false
        for i = 1, #rows do
            local r = rows[i]
            if dir == r[1] then
                f1, f2, b1, b2 = r[2], r[3], r[4], r[5]
                slant = true
                break
            end
        end
        if not slant then b1 = dir:RotLeft(4) end                           -- V:client/ISUI/ISButtonPrompt.lua:483 (180 Grad)
        if doorAt(p, f1) or doorAt(p, f2) or doorAt(p, b1) or doorAt(p, b2) then return true end
        if climbAt(p, f1) or climbAt(p, f2) then return true end
    end
    -- Ein ANDERES Tier ist Vanillas E-Ziel (Kuh, Huhn ...: E streichelt/melkt dort, V:client/TimedActions/ISContextualActions.lua:99-133)
    local an = useableFn()
    if an ~= nil and (B.BodyKind == nil or B.BodyKind(an) == nil) then return true end
    return false
end

-- ---------------------------------------------------------------------------
-- 1.4 F -- Fremd-Vorfahrt auf DERSELBEN Taste (lesend, Existenz-Riegel)
-- ---------------------------------------------------------------------------
-- NC-Station mit "[E]"-Hinweis (Crew Beacon, Appearance Workstation) in STATION_R Kacheln, gleiche Etage, 5 x 5 Kacheln um den Spieler --
-- dieselbe Suche wie NC:client/ISUI/BanditsNPCBeaconPrompt.lua:45-71 (Stationen :31-38: NC:client/BanditsNPCBeacon.lua:655 OnSquare,
-- NC:client/BanditsNPCAppearance.lua:174 OnSquare). getCell():getGridSquare(ganze Zahlen) V:server/Animal/ISPickDungCursor.lua:104;
-- sq:getX()/getY() V:client/ISUI/ISWorldObjectContextMenu.lua:751. Erst der Abstand (reines Lua), dann die NC-Frage.
local function stationNear(p)
    local bc, ap = BanditsNPC.Beacon, BanditsNPC.Appearance
    local withBc = type(bc) == "table" and type(bc.OnSquare) == "function"
    local withAp = type(ap) == "table" and type(ap.OnSquare) == "function"
    if not withBc and not withAp then return false end
    local cell = getCell()
    if cell == nil then return false end
    local px, py = p:getX(), p:getY()                                       -- V:client/Fishing/TensionUI.lua:11
    local fx, fy, fz = math.floor(px), math.floor(py), math.floor(p:getZ())
    local r2 = STATION_R * STATION_R
    for dx = -2, 2 do
        for dy = -2, 2 do
            local sq = cell:getGridSquare(fx + dx, fy + dy, fz)
            if sq ~= nil then
                local ddx, ddy = sq:getX() + 0.5 - px, sq:getY() + 0.5 - py
                if ddx * ddx + ddy * ddy <= r2 then
                    if withBc and bc.OnSquare(sq) then return true end
                    if withAp and ap.OnSquare(sq) then return true end
                end
            end
        end
    end
    return false
end

local function othersFirst(p, key, useableFn)
    -- NPC Crew "Talk to NPC" auf derselben Taste und ein NPC vor dem Spieler (NC:client/BanditsNPCInteract.lua:35 KEYBIND, :41 FindTarget;
    -- isKey(Text, key) V:client/ISUI/FPS.lua:9). Ohne NPC Crew still.
    local ia = BanditsNPC.Interact
    if type(ia) == "table" and ia.KEYBIND and ia.FindTarget and getCore():isKey(ia.KEYBIND, key) and ia.FindTarget(p) then
        return true
    end
    -- NC-Station mit "[E]"-Hinweis: deren Taste ist NC:client/BanditsNPCBeacon.lua:1142 PromptKey() (Vanillas Interact)
    local bc = BanditsNPC.Beacon
    if type(bc) == "table" and type(bc.PromptKey) == "function" and key == bc.PromptKey() and stationNear(p) then
        return true
    end
    -- Vanillas Fahrzeug-Radial (V:client/ISUI/ISUIHandler.lua:36, :43)
    if getCore():isKey(KeybindId.VEHICLE_RADIAL_MENU, key) and ISVehicleMenu.getVehicleToInteractWith(p) then return true end
    -- Vanillas Tier-Radial an einem FREMDEN Tier (V:client/ISUI/ISUIHandler.lua:37, :44): nicht wild und nicht unserer Art, oder ein Baer
    -- unserer Art eines anderen Spielers. isWild: V:client/ISUI/Animal/ISAnimalContextMenu.lua:1171.
    if getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key) then
        local an = useableFn()
        if an ~= nil then
            local kind = bearKind(an)
            if kind == "foreign" then return true end
            if kind == nil and not an:isWild() then return true end
        end
    end
    return false
end

-- Nachbesserung F1B B1 (Pruefer A1/B1): liegt die gedrueckte Taste AUCH auf Vanillas Tier-Radial (Vorgabe V) und ist Vanillas nutzbares
-- Tier ein Baer unserer Art (nicht fremd), hat Vanilla das Radial schon beim DRUECKEN geoeffnet (V:client/ISUI/ISUIHandler.lua:35-57)
-- und schliesst es beim Loslassen nur ohne getOptionRadialMenuKeyToggle (:87-96). Damit nicht Radial UND Fenster offen bleiben, geht ein
-- offenes Radial hier mit zu -- wie in F1 (closeRadial / onRadialKey). getPlayerRadialMenu(0), isReallyVisible:
-- V:client/ISUI/ISUIHandler.lua:91-92; undisplay V:client/ISUI/Animal/ISAnimalContextMenu.lua:1164. Am Fahrzeug gehoert das Radial dem
-- Fahrzeug (V:client/ISUI/ISUIHandler.lua:43, :49-54) -- dann nichts. Mit den Vorgaben (E nah, keine Fern-Taste) greift das nie.
local function closeBearRadial(p, key)
    if getCore():isKey(KeybindId.ANIMAL_RADIAL_MENU, key) then                      -- V:client/ISUI/ISUIHandler.lua:37
        local menu = getPlayerRadialMenu(0)                                          -- V:client/ISUI/ISUIHandler.lua:91
        if menu and menu:isReallyVisible() and not ISVehicleMenu.getVehicleToInteractWith(p)   -- :92, :43
            and bearKind(useable()) == "ours" then
            menu:undisplay()                                                         -- V:client/ISUI/Animal/ISAnimalContextMenu.lua:1164
        end
    end
end

-- ---------------------------------------------------------------------------
-- 1.5 Welcher eigene Baer ist nah? Nur beim Druck; Quelle ist die lebende Kopie der Anzeige (U.CubsNear,
-- client/ISUI/BanditsNPCBearHud.lua: frische Sicht, lebende Objekte, 2D-Abstand; kein Suchlauf), hoechstens viewMax Eintraege.
-- ---------------------------------------------------------------------------
-- Traegt die Sicht einen eigenen zahmen, geladenen, nicht mitfahrenden Baeren? (Riegel fuer den Rueckfall -- sonst keine Engine-Frage)
local function loadedOwn()
    if not U.WinBears then return false end
    local list = U.WinBears()
    for i = 1, #list do
        local v = list[i]
        if v.st == "tame" and v.ld == true and v.ride ~= true then return true end
    end
    return false
end

-- Traegt die frische Sicht ueberhaupt einen eigenen Baeren (zahm oder vermisst, U.WinBears -- dieselben Fragen wie U.WinOpen)?
local function hasOwn()
    if not U.Fresh or not U.Fresh() or not U.WinBears then return false end
    return #U.WinBears() > 0
end

local function nearBear(p, useableFn)
    if not U.Fresh or not U.Fresh() or not U.CubsNear or not U.WinMine then return nil end
    local px, py, pz = p:getX(), p:getY(), p:getZ()                         -- V:client/Fishing/TensionUI.lua:11
    local fx, fy = 0, 0
    local dir = p:getDir()                                                  -- V:client/ISUI/ISButtonPrompt.lua:378
    if dir ~= nil then fx, fy = dir:dx(), dir:dy() end                      -- V:server/BuildingObjects/ISMoveableCursor.lua:450-451
    if fx ~= 0 and fy ~= 0 then fx, fy = fx * DIAG_K, fy * DIAG_K end
    local list = U.CubsNear(p, NEAR_R)
    local best, bestScore = nil, nil
    for i = 1, #list do
        local e = list[i]
        local c, a = e.c, e.a
        if type(c) == "table" and c.st == "tame" and c.ride ~= true and U.WinMine(c)
            and math.abs(a:getZ() - pz) < 1 then                            -- a:getZ(): V:client/TimedActions/ISContextualActions.lua:100
            local d = e.d
            local dot = 1
            if d > 0 then dot = (fx * (a:getX() - px) + fy * (a:getY() - py)) / d end
            if d < NEAR_ANY or dot > DOT_MIN then
                local score = d - dot                                       -- naeher UND mehr vorn gewinnt (NC Interact.lua:65)
                if bestScore == nil or score < bestScore then best, bestScore = c.id, score end
            end
        end
    end
    if best ~= nil then return best end
    -- Rueckfall E12 (b): die Anzeige hat (noch) kein Objekt -- Vanillas nutzbares Tier dicht vor dem Spieler ist unser eigener zahmer Baer.
    if not loadedOwn() then return nil end
    local an = useableFn()
    if an == nil or B.BodyKind == nil or B.BodyKind(an) == nil or not B.ViewOf then return nil end
    local v = B.ViewOf(an)
    if type(v) ~= "table" or v.id == nil or v.st ~= "tame" or v.ride == true or not U.WinMine(v) then return nil end
    if math.abs(an:getZ() - pz) >= 1 then return nil end
    return v.id
end

-- ---------------------------------------------------------------------------
-- 1.2 / 1.3 Ereignisse
-- ---------------------------------------------------------------------------
-- Druecken: ist es eine unserer Tasten, Zeitstempel und Cursor-Zustand merken. Der Cursor wird schon beim Druecken festgehalten, weil
-- Vanillas Moebel-Cursor auf Interact beim Loslassen/Halten selbst endet (V:server/BuildingObjects/ISMoveableCursor.lua:43-58, :69-70)
-- und die Reihenfolge der Hoerer an der Ladefolge haengt (ungeprueft). getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485;
-- getCell():getDrag(0): V:server/BuildingObjects/ISMoveableCursor.lua:44 (im Hauptmenue gibt es keine Zelle).
local function onKeyStart(key)
    local near, far = U.BearKeys()
    if key ~= near and key ~= far then return end
    K.key, K.at = key, getTimestampMs()
    local cell = getCell()
    K.drag = (cell ~= nil and cell:getDrag(0) ~= nil)
end

-- Der Rest von 1.3 ab Schritt 5 (Fenster ist zu): -> true + Kennung (nil = naechster eigener Baer) oder false. Reihenfolge so, dass die
-- teuren Fragen (NC FindTarget, Stationen) nur kommen, wenn wirklich ein Fenster aufginge. Abweichung vom Plan-Ablauf (bau_f1b.md):
-- der Nah-Baer (6.) wird VOR dem Interact-Riegel (5.) gesucht -- gleiches Ergebnis, aber ohne Baeren in der Naehe fragt ein E-Druck
-- die Engine nie nach dem nutzbaren Tier (PLAN_F1B.md 6.1 T29).
local function decide(p, key, isFar, held, drag)
    local target = nil
    if not isFar then
        target = nearBear(p, useable)
        if target == nil then return false end                              -- E5: kein eigener Baer nah -> still
    end
    local interact = getCore():isKey(KeybindId.INTERACT, key)               -- V:client/Farming/CFarming_Interact.lua:28
    -- Nachbesserung F1B B2: die Fern-Taste auf Vanillas Interact bleibt ohne Sicht oder ohne eigenen Baeren STILL wie die Nah-Taste (sonst
    -- "You do not have a bear yet." / "still loading" bei jedem E an jeder Ecke; um die Sicht bittet helloTick ohnehin,
    -- client/BanditsNPCBearClient.lua). Mit Sicht und eigenem (auch vermisstem) Baeren: das alte Fern-Verhalten.
    if isFar and interact and not hasOwn() then return false end
    if interact and busy(p, held, drag, useable) then return false end
    if othersFirst(p, key, useable) then return false end
    return true, target
end

-- Loslassen (OnKeyPressed): der ganze Weg PLAN_F1B.md 1.3.
local function onKey(key)
    local near, far = U.BearKeys()
    local isNear = near ~= nil and key == near
    local isFar = far ~= nil and key == far                                 -- hat Vorrang, falls near == far
    local held, drag = 0, false
    if K.key == key then
        held = getTimestampMs() - K.at
        if held < 0 then held = 0 end
        drag = K.drag
        K.key = nil
    end
    if not isNear and not isFar then return end
    local p = getSpecificPlayer(0)                                          -- V:client/Farming/CFarmingSystem.lua:45
    if blockedBase(p) then return end
    local closed = U.winClosedAt
    if type(closed) == "number" then
        local now = getTimestampMs()
        if now >= closed and now - closed < REOPEN_MS then return end
    end
    useableReset(p)
    if U.WinIsOpen and U.WinIsOpen() then                                   -- E7: jede unserer Tasten schliesst
        U.WinClose()
        closeBearRadial(p, key)                                             -- B1: liegt sie auch auf V, geht Vanillas Radial am Baeren mit zu
    else
        local go, target = decide(p, key, isFar, held, drag)
        if go and U.WinOpen and U.WinOpen(p, target) then                   -- client/ISUI/BanditsNPCBearWindow.lua
            closeBearRadial(p, key)
        end
    end
    useableReset(nil)                                                       -- keine Engine-Objekte ueber den Druck hinaus halten
end

-- Nur einmal anmelden (wird die Datei ein zweites Mal geladen, oeffnete und schloesse dieselbe Taste sonst sofort wieder).
if not U.keyHooked then
    U.keyHooked = true
    Events.OnKeyStartPressed.Add(onKeyStart)                                -- V:client/Farming/CFarming_Interact.lua:289
    Events.OnKeyPressed.Add(onKey)                                          -- V:client/ISUI/FPS.lua:20
end
