--
-- NPC Crew -- Baer, Daten des Inventar-Fensters (F4, Lauf baer-f4, PLAN_F4.md 7, 8.2, 16; Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md:
-- "alles was es gibt", hoechstens 1000 Dinge, ansehen ueberall, hineinlegen / herausnehmen nur daneben, nicht waehrend er mitfaehrt).
--
-- Diese Datei entscheidet NICHTS. Sie
--   * nimmt die Liste des Schreibers an: B.OnInv(seite) (Einzelspieler ruft der Kern direkt, Mehrspieler kommt sie als Befehl "Inv" an --
--     client/BanditsNPCBearClient.lua). Eine Liste = pn Seiten mit je hoechstens 100 Saetzen, alle gleich nacheinander gesendet
--     (f4/schnittstelle.md K4). Gesammelt wird je Baer und je Fassung r: kommt eine Seite mit anderem r, gilt nur noch die neue Fassung.
--     Fehlt it, ist die Seite leer (eine leere Tabelle kommt im Netz als nil an). Deckel: 8 Baeren, 64 Seiten, 1000 Zeilen.
--   * bittet um die Liste: U.InvAsk -> B.Ask(player, "InvList", { id }) (Einzelspieler B.Handle direkt, Mehrspieler sendClientCommand,
--     Rolle user genuegt). Drossel B.CFG.invListMs (500 ms); das Fenster fragt beim Oeffnen, bei neuer Fassung der Sicht (ivR) und alle
--     invKeepMs (30 s); ohne Antwort nach 2 s noch einmal, hoechstens 3 Mal, dann "No answer".
--   * liest das eigene Inventar (U.InvMine): Hauptinventar UND alle Taschen darin, gruppiert nach Typ + Name (Deckel 200 Gruppen); Angezogenes
--     und Versteckte wie Vanillas Tausch-Fenster (V:client/ISUI/ISTradingUI.lua:175, :181) -- Angezogenes steht grau ("Take it off first").
--   * stellt Zeitaktionen an (U.InvGive / U.InvTake / U.InvPacksOn / U.InvPacksOff): bei Bedarf erst aus der Tasche ins Hauptinventar
--     (ISWorldObjectContextMenu.transferIfNeeded, V:client/ISUI/ISWorldObjectContextMenu.lua:427), dann die Netz-Zeitaktion
--     (shared/TimedActions/BanditsNPCBear{Put,Take}Action.lua). Ob es gilt, entscheidet der Schreiber in complete() -- er nimmt erst, prueft
--     die Ankunft und schreibt dann gut (rote Linie: nichts verloren, nichts doppelt). Ein Stapel wird in Aktionen zu hoechstens
--     B.CFG.invTakeMax (50) Stueck genommen; "Alle geben" stellt hoechstens so viele Stuecke an, wie Gewicht, 1000-Deckel und 50 erlauben.
--   * prueft vor (U.InvWhy): nur fuer das Grau im Fenster, aus der Sicht (Abstand < 3 Kacheln wie die Zeitaktion, faehrt mit, du sitzt im
--     Auto, kaempft, nicht geladen) und der Verlustfrei-Regel des Kerns B.InvCanCarry(item) (shared/BanditsNPCBearInvRules.lua, Existenz-Riegel).
-- Namen und Symbole je Typ: getItemNameFromFullType(t) (V:client/Entity/ISUI/ISEntityBuildMenu.lua:176), ScriptManager.instance:getItem(t)
-- (V:client/ISUI/ISWorldObjectContextMenu.lua:1254) + getNormalTexture() (V:client/ISUI/ISInventoryItem.lua:26-27) -- Cache je Typ, Deckel 256.
-- Laeuft im Einzelspieler und auf jedem MP-Client; nie je Bild (das Fenster ruft hoechstens 1 x je Sekunde bzw. auf Klick).
-- K1 (Lauf baer-k1, PLAN_K1.md 1.4, 5; Kevin 13./14.11.2026: "nur die 1000 items einstellen zum gleichzeitig verschieben", Zahlenfeld beim Geben
-- UND Nehmen): kein 50er-Deckel mehr -- Grenzen nur Traglast und B.CFG.invMaxItems (1000). U.InvGive(player, v, g, n) stellt fuer n Stueck
-- EINE gebuendelte Put-Aktion an (k = n; vorher holt transferIfNeeded jedes der n Stuecke, das in einer Tasche liegt, ins Hauptinventar --
-- Frage K-F10), U.InvTake(player, v, row, k) EINE Take-Aktion fuer bis zu invTakeMax (1000) Stueck. U.InvGiveable(g) = die Stuecke, die
-- gebuendelt gehen (ohne Favoriten / Ausgeruestetes), U.InvFit(player, w) = wie viele Stuecke dieses Gewichts in DEIN Inventar passen
-- (Vorbelegung des Zahlenfelds beim Nehmen). Verlustfrei bleibt es beim Schreiber: er nimmt je Stueck, prueft die Ankunft, schreibt erst dann gut.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local INV_MAX = 8           -- so viele Baeren merkt sich der Client (einer je Spieler ist die Vorgabe)
local PAGE_MAX = 64         -- Seiten je Liste (1000 Saetze / 100 = 10; Deckel gegen Unsinn)
local ROW_MAX = 1000        -- Zeilen je Liste (Kevin: hoechstens 1000 Dinge)
local MINE_MAX = 1000       -- Gruppen des eigenen Inventars (PLAN_F4.md 8.2; Nachbesserung F4 P12: 200 -> 1000, greift der Deckel, sagt es der Fuss)
local NAME_MAX = 256        -- Cache Namen / Symbole je Typ
local RETRY_MS = 2000       -- ohne Antwort nach so vielen ms noch einmal fragen ...
local RETRY_N = 3           -- ... hoechstens so oft
local GIVE_MAX = 1000       -- K1: Rueckfall fuer B.CFG.invMaxItems -- so viele Stuecke hoechstens in EINER gebuendelten Aktion (vorher 50 Aktionen)
local BAG_TYPE = "NPCCrew.BearPacks"

-- Listen je Baer: [id] = { r, pn, got = { [pg] = Zeilen }, have, rows, n, cnt, cap, load, over, bag, at }; Bitten je Baer:
-- [id] = { at, n, since }. Nur diese Sitzung.
local INV = {}
local ASK = {}
local NAMES, NAMES_N = {}, 0
local ICONS, ICONS_N = {}, 0

local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

local function count(t)
    local n = 0
    for _ in pairs(t) do n = n + 1 end
    return n
end

local function isNum(v)
    return type(v) == "number" and v == v
end

-- ---------------------------------------------------------------------------
-- Namen und Symbole je Typ (nur Anzeige; nie ein Gegenstand)
-- ---------------------------------------------------------------------------

-- Name eines vollen Typs ("Base.Apple" -> "Apple"); unbekannt -> der Typ selbst.
function U.ItemName(t)
    if type(t) ~= "string" or t == "" then return "?" end
    local n = NAMES[t]
    if n ~= nil then return n end
    n = getItemNameFromFullType(t)                              -- V:client/Entity/ISUI/ISEntityBuildMenu.lua:176
    if type(n) ~= "string" or n == "" then n = t end
    if NAMES_N >= NAME_MAX then
        NAMES, NAMES_N = {}, 0
    end
    NAMES[t] = n
    NAMES_N = NAMES_N + 1
    return n
end

-- Symbol eines vollen Typs aus dem Skript-Gegenstand (kein Gegenstand wird gebaut). false = gibt es nicht (im Cache, damit nicht je
-- Sekunde neu gesucht wird).
function U.ItemIcon(t)
    if type(t) ~= "string" or t == "" then return nil end
    local tex = ICONS[t]
    if tex == nil then
        tex = false
        local si = ScriptManager.instance:getItem(t)            -- V:client/ISUI/ISWorldObjectContextMenu.lua:1254
        if si then tex = si:getNormalTexture() or false end     -- V:client/ISUI/ISInventoryItem.lua:26-27
        if ICONS_N >= NAME_MAX then
            ICONS, ICONS_N = {}, 0
        end
        ICONS[t] = tex
        ICONS_N = ICONS_N + 1
    end
    if tex == false then return nil end
    return tex
end

-- Fluessigkeit (Typ-Name des Kerns, z. B. "Water") als Text des Spiels: Vanillas Fluids.json "Fluid_Name_<Typ>" (Schluessel zusammengesetzt
-- wie V:client/Foraging/ISSearchWindow.lua:165); fehlt er, der Name selbst.
function U.FluidName(fn)
    if type(fn) ~= "string" or fn == "" then return "?" end
    local s = getTextOrNull("Fluid_Name_" .. fn)                -- ISSearchWindow.lua:165
    if type(s) ~= "string" or s == "" then return fn end
    return s
end

-- ---------------------------------------------------------------------------
-- Liste des Schreibers
-- ---------------------------------------------------------------------------

-- Eine Zeile pruefen (nur Anzeige): nr Text, t Text, k >= 1. Felder, die das Fenster liest, werden uebernommen; Unsinn -> nil.
local function cleanRow(x)
    if type(x) ~= "table" then return nil end
    local nr, t, k = x.nr, x.t, tonumber(x.k)
    if type(nr) ~= "string" or nr == "" or type(t) ~= "string" or t == "" or k == nil or k < 1 then return nil end
    local r = { nr = nr, t = t, k = math.floor(k), w = tonumber(x.w) or 0 }
    if type(x.nm) == "string" and x.nm ~= "" then r.nm = x.nm end
    if isNum(tonumber(x.cp)) then r.cp = tonumber(x.cp) end
    if isNum(tonumber(x.fr)) then r.fr = math.floor(tonumber(x.fr)) end
    if isNum(tonumber(x.fl)) then r.fl = tonumber(x.fl) end
    if type(x.fn) == "string" then r.fn = x.fn end
    if isNum(tonumber(x.u)) then r.u = tonumber(x.u) end
    r.fv, r.ck, r.bu, r.fz, r.unk, r.ea = x.fv == true, x.ck == true, x.bu == true, x.fz == true, x.unk == true, x.ea == true
    return r
end

-- Aeltesten Eintrag vergessen, wenn mehr als INV_MAX Baeren gemerkt sind (Deckel).
local function trimInv()
    if count(INV) < INV_MAX then return end
    local oldId, oldAt = nil, nil
    for id, e in pairs(INV) do
        if oldAt == nil or (e.at or 0) < oldAt then oldId, oldAt = id, e.at or 0 end
    end
    if oldId ~= nil then INV[oldId] = nil end
end

-- Nachbesserung F4 (Befund P4): die fertige Liste nach dem ANZEIGE-Namen ordnen (eigener Name vor dem Namen des Typs, dann Satz-Nummer) -- wie die
-- rechte Spalte (byName). Nur Anzeige, einmal je neuer Fassung; der Schreiber sortiert nach Typ (er kennt die Sprache des Clients nicht).
local function nrNum(nr)
    return tonumber(string.sub(tostring(nr), 2)) or 0
end

function U.InvSortRows(rows)
    if type(rows) ~= "table" then return end
    local seen = {}
    for i = 1, #rows do
        local r = rows[i]
        r.sortName = r.nm or U.ItemName(r.t)
        if r.unk then r.sortName = U.T("UI_BN_Bear_Inv_Unknown") end      -- wie die Zeile es zeigt ("Unknown item")
        seen[r.sortName] = (seen[r.sortName] or 0) + 1
    end
    -- P6: gleicher Name mehrfach (z. B. Hemden in verschiedenem Zustand) -> das Fenster schreibt den Zustand in die Zeile
    for i = 1, #rows do
        local r = rows[i]
        r.dup = seen[r.sortName] > 1
    end
    table.sort(rows, function(a, b)
        if a.sortName ~= b.sortName then return a.sortName < b.sortName end
        return nrNum(a.nr) < nrNum(b.nr)
    end)
end

-- B.OnInv(seite): eine Seite der Liste (f4/schnittstelle.md K4). Einzelspieler: der Kern ruft das direkt; Mehrspieler: Befehl "Inv".
function B.OnInv(page)
    if type(page) ~= "table" or page.id == nil then return end
    local r, pg, pn = tonumber(page.r), tonumber(page.pg), tonumber(page.pn)
    if r == nil or pg == nil or pn == nil then return end
    pg, pn = math.floor(pg), math.floor(pn)
    if pn < 1 or pn > PAGE_MAX or pg < 1 or pg > pn then return end
    local id = page.id
    local e = INV[id]
    if e == nil or e.r ~= r or e.pn ~= pn then
        if e == nil then trimInv() end
        e = { r = r, pn = pn, got = {}, have = 0 }
        INV[id] = e
    end
    if e.got[pg] == nil then e.have = e.have + 1 end
    local rows = {}
    if type(page.it) == "table" then
        for i = 1, #page.it do
            local x = cleanRow(page.it[i])
            if x then rows[#rows + 1] = x end
        end
    end
    e.got[pg] = rows
    -- Kopfwerte stehen auf jeder Seite gleich; die letzte gilt
    e.n, e.cnt = tonumber(page.n), tonumber(page.cnt)
    e.cap, e.load = tonumber(page.cap), tonumber(page.load)
    e.over = page.over == true
    e.bag = nil
    -- Packtaschen: eine Zeile wie in it (nr = "bag", f4/schnittstelle.md K-Nachtrag 1 Nr. 7) -- nur Typ und Zustand werden gelesen
    if type(page.bag) == "table" and type(page.bag.t) == "string" then e.bag = { t = page.bag.t, cp = tonumber(page.bag.cp) } end
    e.at = getTimestampMs()                                     -- V:client/Foraging/ISBaseIcon.lua:485
    if e.have >= e.pn then
        local all = {}
        for i = 1, e.pn do
            local list = e.got[i] or {}
            for j = 1, #list do
                if #all < ROW_MAX then all[#all + 1] = list[j] end
            end
        end
        U.InvSortRows(all)
        e.rows = all
        ASK[id] = nil                                           -- beantwortet: Wiederholen aus
    end
    if U.InvOnList then U.InvOnList(id) end
end

-- Fertige Liste eines Baeren (alle Seiten derselben Fassung da) oder nil.
function U.InvList(id)
    local e = INV[id]
    if e == nil or e.rows == nil then return nil end
    return e
end

-- Fassung der fertigen Liste (oder nil).
function U.InvListR(id)
    local e = INV[id]
    if e == nil or e.rows == nil then return nil end
    return e.r
end

-- Um die Liste bitten (Drossel invListMs). force = auch innerhalb der Drossel nicht (nie schneller als die Drossel). Rueckgabe true = gefragt.
function U.InvAsk(player, id)
    if not player or id == nil or not B.Ask then return false end
    local now = getTimestampMs()
    local a = ASK[id]
    if a and now >= a.at and now - a.at < cfgNum("invListMs", 500) then return false end
    if a == nil then
        a = { n = 0, since = now }
        ASK[id] = a
    end
    a.at = now
    a.n = a.n + 1
    B.Ask(player, "InvList", { id = id })
    return true
end

-- Zustand der Bitte: "wait" (gefragt, noch keine Antwort), "none" (3 Mal ohne Antwort) oder nil. Stellt selbst die Wiederholung an.
function U.InvAskState(player, id)
    local a = ASK[id]
    if a == nil then return nil end
    local now = getTimestampMs()
    if now < a.at then a.at = now end
    if now - a.at < RETRY_MS then return "wait" end
    if a.n < RETRY_N then
        U.InvAsk(player, id)
        return "wait"
    end
    return "none"
end

-- Neu fragen lassen (Knopf / neue Sicht): die Zaehlung der Wiederholungen beginnt neu.
function U.InvAskReset(id)
    ASK[id] = nil
end

-- Wann zuletzt gefragt (ms) -- fuer das Keep-alive des Fensters.
function U.InvAskedAt(id)
    local a = ASK[id]
    return a and a.at or nil
end

-- ---------------------------------------------------------------------------
-- Eigenes Inventar (rechte Spalte)
-- ---------------------------------------------------------------------------

-- Gruppen { key, t, name, items = { ... }, w, kg, worn, fav, tex } nach Name sortiert. Hauptinventar und alle Taschen darin
-- (getAllEvalRecurse mit Lua-Funktion: V:client/ISUI/Animal/ISAnimalContextMenu.lua:32, :52-54). Versteckte nie (ISTradingUI.lua:181).
-- Angezogenes eigene Gruppe "worn" (ISTradingUI.lua:175). Gewicht wie der Kern: getUnequippedWeight (V:client/Hotbar/ISHotbar.lua:573).
local function shown(item)
    return not item:isHidden()                                  -- ISTradingUI.lua:181
end

local function byName(a, b)
    if a.name ~= b.name then return a.name < b.name end
    return a.key < b.key
end

function U.InvMine(player)
    local out = {}
    if not player then return out end
    local inv = player:getInventory()
    if not inv then return out end
    local found = inv:getAllEvalRecurse(shown)
    if not found then return out end
    local groups = {}
    for i = 0, found:size() - 1 do
        local item = found:get(i)
        local worn = player:isEquippedClothing(item)           -- ISTradingUI.lua:175
        local name = item:getName()                             -- ISTradingUI.lua:390 (C10: :379 war setHistoryMessage)
        local t = item:getFullType()                            -- ISAnimalContextMenu.lua:54
        local key = t .. "|" .. tostring(name)
        if worn then key = key .. "|w" end
        local g = groups[key]
        if g == nil and #out >= MINE_MAX then out.more = true end
        if g == nil and #out < MINE_MAX then
            g = { key = key, t = t, name = tostring(name), items = {}, kg = 0, worn = worn, tex = item:getTex() }   -- ISInventoryItem.lua:4-5
            g.w = tonumber(item:getUnequippedWeight()) or 0     -- ISHotbar.lua:573
            groups[key] = g
            out[#out + 1] = g
        end
        if g ~= nil then
            g.items[#g.items + 1] = item
            g.kg = g.kg + (tonumber(item:getUnequippedWeight()) or 0)
            if item:isFavorite() then g.fav = true end          -- V:client/ISUI/ISTradingUI.lua:178
        end
    end
    table.sort(out, byName)
    return out
end

-- Erste Packtasche (B.CFG.bagType) im Inventar oder nil (auch in Taschen; transferIfNeeded holt sie).
function U.InvPacksItem(player)
    if not player then return nil end
    local inv = player:getInventory()
    if not inv then return nil end
    local want = (B.CFG and B.CFG.bagType) or BAG_TYPE
    local found = inv:getAllEvalRecurse(function(item) return item:getFullType() == want end)   -- ISAnimalContextMenu.lua:32, :54
    if found and found:size() > 0 then return found:get(0) end
    return nil
end

-- ---------------------------------------------------------------------------
-- Vorpruefung (nur Grau; entscheiden tut der Schreiber in complete())
-- ---------------------------------------------------------------------------

-- Abstand in ganzen Kacheln wie die Zeitaktion (square:DistTo, shared/TimedActions/BanditsNPCBearPutAction.lua isValid) aus der lebenden
-- Kopie (U.CubPos, client/ISUI/BanditsNPCBearHud.lua). nil = keine lebende Kopie.
function U.InvDist(player, v)
    if not player or type(v) ~= "table" or not U.CubPos then return nil end
    local bx, by = U.CubPos(v.id)
    if bx == nil then return nil end
    local dx = math.floor(bx) - math.floor(player:getX())       -- V:client/Fishing/TensionUI.lua:11
    local dy = math.floor(by) - math.floor(player:getY())
    return math.sqrt(dx * dx + dy * dy)
end

-- Grund, warum Geben / Nehmen gerade nicht geht (fertiger Text), sonst nil. Reihenfolge wie das Baeren-Fenster (client/BanditsNPCBearWinData.lua):
-- vermisst / nicht geladen > faehrt mit > du im Auto > zu weit (3 Kacheln) > kaempft.
function U.InvWhy(player, v)
    if type(v) ~= "table" then return U.T("UI_BN_Bear_Why_Gone") end
    local bd = v.bd
    if v.ride == true then return U.TB("UI_BN_Bear_Why_Riding", bd) end
    if v.st ~= "tame" or v.ld ~= true then return U.TB("UI_BN_Bear_Why_OutOfReach", bd) end
    if player and player:getVehicle() ~= nil then return U.T("UI_BN_Bear_Why_InCar") end     -- V:client/ISUI/Hutch/ISHutchMenu.lua:8
    local d = U.InvDist(player, v)
    if d == nil then return U.TB("UI_BN_Bear_Why_OutOfReach", bd) end
    if d >= 3 then return U.TB("UI_BN_Bear_Why_InvFar", bd) end
    if v.fst == "fight" or v.fst == "retreat" then return U.TB("UI_BN_Bear_Why_InvFight", bd) end
    return nil
end

-- Freies Gewicht (kg) und freie Stueck aus der Sicht (f4/schnittstelle.md K5); fehlt die Sicht: nil.
function U.InvRoom(v)
    if type(v) ~= "table" or not isNum(v.ivW) or not isNum(v.ivC) then return nil, nil end
    local free = v.ivC - v.ivW
    local things = nil
    if isNum(v.ivK) then things = cfgNum("invMaxItems", 1000) - v.ivK end
    return free, things
end

-- kg als Text mit einer Nachkommastelle (string.format: S:shared/BanditsNPCBear.lua argText); Nachbesserung F4 (Befund P8): leichte Dinge unter
-- 0,1 kg mit zwei Stellen (eine Patrone "0.01 kg" statt "0.0 kg"; Vanilla rundet Gewichte auf 2 Stellen, V:client/ISUI/ISInventoryPage.lua:632).
function U.Kg(v)
    v = tonumber(v) or 0
    if v < 0 then v = 0 end
    if v > 0 and v < 0.095 then return string.format("%.2f", math.floor(v * 100 + 0.5) / 100) end
    return string.format("%.1f", math.floor(v * 10 + 0.5) / 10)
end

-- Grund, warum DIESE Gruppe nicht gegeben werden kann (Text), sonst nil, dazu wie viele Stuecke "Alle" anstellen darf. Gewicht und
-- 1000-Deckel aus der Sicht; Verlustfrei-Regel des Kerns am ersten Stueck (B.InvCanCarry, Existenz-Riegel).
function U.InvGiveWhy(v, g)
    local bd = v and v.bd
    if g.worn then return U.T("UI_BN_Bear_Why_InvWorn"), 0 end
    local item = g.items[1]
    if B.InvCanCarry and item then
        local ok, why = B.InvCanCarry(item)
        if not ok then return U.TB(type(why) == "string" and why or "UI_BN_Bear_Why_InvLossy", bd), 0 end     -- TB: Nachbesserung P10
    end
    local free, things = U.InvRoom(v)
    if things ~= nil and things < 1 then return U.TB("UI_BN_Bear_Why_InvCap", bd, cfgNum("invMaxItems", 1000)), 0 end
    if free ~= nil and g.w > free + 0.0001 then return U.TB("UI_BN_Bear_Why_InvFull", bd, U.Kg(free)), 0 end
    -- Nachbesserung F4 (Befund P9): "Alle" zaehlt nur, was U.InvGive auch anstellt -- Favoriten und Ausgeruestetes bleiben (TransferSameType.lua:61)
    local n = 0
    for i = 1, #g.items do
        local it = g.items[i]
        if not it:isFavorite() and not it:isEquipped() then n = n + 1 end
    end
    if things ~= nil and n > things then n = things end
    if free ~= nil and g.w > 0 then n = math.min(n, math.floor((free + 0.0001) / g.w)) end
    local most = math.floor(cfgNum("invMaxItems", GIVE_MAX))         -- K1: 1000 statt 50
    if n > most then n = most end
    return nil, n
end

-- K1: die Stuecke einer Gruppe, die gebuendelt gegeben werden (ohne Favoriten / Ausgeruestetes wie Vanillas "alle dieser Art",
-- V:client/ISUI/InventoryWindow/Handlers/TransferSameType.lua:61). Neue Liste, nur auf Klick.
function U.InvGiveable(g)
    local out = {}
    if type(g) ~= "table" or type(g.items) ~= "table" then return out end
    for i = 1, #g.items do
        local it = g.items[i]
        if not it:isFavorite() and not it:isEquipped() then out[#out + 1] = it end
    end
    return out
end

-- K1: wie viele Stuecke des Gewichts w passen noch in DEIN Inventar (Vorbelegung "Nehmen"; entscheiden tut der Schreiber mit hasRoomFor).
-- inv:getCapacityWeight() / inv:getEffectiveCapacity(Spieler): V:client/Foraging/ISBaseIcon.lua:105. nil = unbekannt / gewichtslos.
function U.InvFit(player, w)
    w = tonumber(w) or 0
    if not player or w <= 0 then return nil end
    local inv = player:getInventory()
    if not inv then return nil end
    local free = (tonumber(inv:getEffectiveCapacity(player)) or 0) - (tonumber(inv:getCapacityWeight()) or 0)
    if free ~= free or free < 0 then free = 0 end
    return math.floor((free + 0.0001) / w)
end

-- ---------------------------------------------------------------------------
-- Zeitaktionen anstellen (nehmen nichts selbst)
-- ---------------------------------------------------------------------------

local function bad(player, text)
    HaloTextHelper.addBadText(player, text)                     -- V:client/ISUI/ISWorldObjectContextMenu.lua:1038
end

-- Lebende Kopie des eigenen gezaehmten Baeren oder nil (mit Hinweis).
local function bearObj(player, v)
    local a = nil
    if U.CubObj and type(v) == "table" then a = U.CubObj(v.id) end
    if a == nil or v.ride == true then
        bad(player, U.TB("UI_BN_Bear_Why_OutOfReach", v and v.bd))
        return nil
    end
    return a
end

-- EIN Stueck (k = 1) bzw. EIN Buendel geben (Put "inv"): erst ins Hauptinventar, dann die Zeitaktion. Reihenfolge wie U.MendAsk
-- (client/BanditsNPCBearMenu.lua) ohne Hingehen -- das Fenster laeuft nicht von selbst hin (PLAN_F4.md 7). transferIfNeeded:
-- V:client/ISUI/ISWorldObjectContextMenu.lua:427; ISTimedActionQueue.add: :428 / V:client/ISUI/Animal/ISAnimalContextMenu.lua:94.
local function queuePut(player, a, item, mode, k)
    ISWorldObjectContextMenu.transferIfNeeded(player, item)
    ISTimedActionQueue.add(BanditsNPCBearPutAction:new(player, a, item, mode, k or 1))
end

-- Gruppe geben (K1): n = Anzahl (Zahl; true = so viele wie gehen, wie "Alle"; nil / false / 1 = ein Stueck). Ein Stueck = das erste der Gruppe
-- (einzeln geben geht immer, wie bisher). Mehr als eins: n wird auf das geklemmt, was U.InvGiveWhy erlaubt (Gewicht, 1000); es zaehlen nur
-- Stuecke ohne Favorit / Ausgeruestetes (U.InvGiveable); jedes davon, das in einer Tasche liegt, holt transferIfNeeded vorher ins Hauptinventar,
-- dann EINE Put-Aktion mit k = n am ersten (der Kern sucht die anderen selbst). Rueckgabe: Zahl der Stuecke, die die Aktion geben SOLL.
function U.InvGive(player, v, g, n)
    if not player or type(g) ~= "table" or BanditsNPCBearPutAction == nil then return 0 end
    local why, most = U.InvGiveWhy(v, g)
    if why then
        bad(player, why)
        return 0
    end
    local a = bearObj(player, v)
    if a == nil then return 0 end
    local want = 1
    if n == true then want = most else want = math.floor(tonumber(n) or 1) end
    if want ~= want then want = 1 end
    local list = U.InvGiveable(g)
    if want > most then want = most end
    if want > #list then want = #list end
    if want <= 1 then
        if g.items[1] == nil then return 0 end
        queuePut(player, a, g.items[1], "inv", 1)
        return 1
    end
    for i = 2, want do ISWorldObjectContextMenu.transferIfNeeded(player, list[i]) end    -- ISWorldObjectContextMenu.lua:427
    queuePut(player, a, list[1], "inv", want)
    return want
end

-- Satz nehmen (K1): k Stueck in EINER Aktion (Deckel invTakeMax, jetzt 1000; ein Rest darueber -- kann es nach dem 1000-Deckel der Liste nicht
-- geben -- bekaeme eine zweite). kg je Aktion nur fuer die Dauer. Rueckgabe: Zahl der Aktionen.
function U.InvTake(player, v, row, k)
    if not player or type(row) ~= "table" or BanditsNPCBearTakeAction == nil then return 0 end
    if row.unk then
        bad(player, U.T("UI_BN_Bear_Why_InvUnknown"))
        return 0
    end
    local a = bearObj(player, v)
    if a == nil then return 0 end
    k = math.floor(tonumber(k) or 1)
    if k > row.k then k = row.k end
    if k < 1 then return 0 end
    local step = math.floor(cfgNum("invTakeMax", 1000))              -- K1: 1000 statt 50
    if step < 1 then step = 1 end
    local n = 0
    while k > 0 do
        local part = math.min(k, step)
        ISTimedActionQueue.add(BanditsNPCBearTakeAction:new(player, a, row.nr, part, (row.w or 0) * part))
        k = k - part
        n = n + 1
    end
    return n
end

-- Packtaschen anlegen (Put "bag"); walk = true: erst hingehen (Rechtsklick; luautils.walkAdj leert die Warteschlange,
-- V:client/ISUI/ISWorldObjectContextMenu.lua:426-428, Form U.MendAsk). Grund kommt aus U.InvPacksWhy.
function U.InvPacksOn(player, v, walk)
    if not player or BanditsNPCBearPutAction == nil then return false end
    local why = U.InvPacksWhy(player, v, true, walk)
    if why then
        bad(player, why)
        return false
    end
    local a = bearObj(player, v)
    local item = U.InvPacksItem(player)
    if a == nil or item == nil then return false end
    if walk then
        local sq = a:getSquare()                                -- ISAnimalContextMenu.lua:90
        if not sq or not luautils.walkAdj(player, sq) then return false end     -- ISWorldObjectContextMenu.lua:426
    end
    queuePut(player, a, item, "bag")
    return true
end

-- Packtaschen abnehmen (Take "bag").
function U.InvPacksOff(player, v)
    if not player or BanditsNPCBearTakeAction == nil then return false end
    local why = U.InvPacksWhy(player, v, false)
    if why then
        bad(player, why)
        return false
    end
    local a = bearObj(player, v)
    if a == nil then return false end
    ISTimedActionQueue.add(BanditsNPCBearTakeAction:new(player, a, "bag", 1, 0))
    return true
end

-- Grund, warum die Packtaschen gerade nicht an- bzw. abgehen (Text), sonst nil. on = anlegen. walk = der Rechtsklick geht hin (dann
-- zaehlt der Abstand nicht).
function U.InvPacksWhy(player, v, on, walk)
    if type(v) ~= "table" then return U.T("UI_BN_Bear_Why_Gone") end
    local bd = v.bd
    if on then
        if bd ~= "big" then return U.T("UI_BN_Bear_Why_InvCub") end
        if v.bag == true then return U.TB("UI_BN_Bear_Why_InvHasPacks", bd) end
        if U.InvPacksItem(player) == nil then return U.T("UI_BN_Bear_Why_InvNoPacks") end
    else
        if v.bag ~= true then return U.T("UI_BN_Bear_Why_InvGone") end
        local free = U.InvRoom(v)
        if free ~= nil and free < cfgNum("bagAdd", 150) - 0.0001 then return U.TB("UI_BN_Bear_Why_InvPacks", bd) end     -- 150: Kevin 13.11.
    end
    if walk then
        if v.ride == true then return U.TB("UI_BN_Bear_Why_Riding", bd) end
        if v.st ~= "tame" or v.ld ~= true then return U.TB("UI_BN_Bear_Why_OutOfReach", bd) end
        return nil
    end
    return U.InvWhy(player, v)
end

local function onGameStart()
    INV, ASK = {}, {}
    NAMES, NAMES_N, ICONS, ICONS_N = {}, 0, {}, 0
end

Events.OnGameStart.Add(onGameStart)                             -- V:client/Chat/ISChat.lua:1186
