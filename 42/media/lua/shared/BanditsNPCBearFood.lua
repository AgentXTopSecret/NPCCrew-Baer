--
-- NPC Crew -- Baer, Futter erkennen (B1a, PLAN_ZAEHMEN.md 6.6).
--
-- Klassen: "fav" (Lieblingsfutter: Honig, Fisch), "ok" (Fleisch, Obst, Beeren, Eier, Nuesse, Insekten ...), "snack" (Klasse ok,
-- aber ein Happen: Naehrwert kleiner als 5). Alles andere frisst ein Baer nicht. Verdorbenes und Verbranntes wird abgelehnt.
-- Honig ist in Vanilla ein Gewuerz: hier gibt es deshalb KEINEN Gewuerz-Filter. Ein angebrochenes Stueck zaehlt als ganzes.
--
-- B.FoodClass und B.IsBaitFood laufen ueberall (auch beim Schreiber, der sie in complete() fragt); B.FoodList nur beim Client.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local WHY_NOT = "UI_BN_Bear_Why_NotFood"
local WHY_ROTTEN = "UI_BN_Bear_Why_Rotten"

-- getFoodType()-Werte der Klasse "ok" (am 10.11.2026 in media/scripts gegen FoodType = ... nachgezaehlt; "Fish" ist "fav").
local OK_TYPES = {
    Meat = true, Beef = true, Poultry = true, Game = true, Venison = true, Bacon = true, Sausage = true, Seafood = true,
    Egg = true, Fruits = true, Citrus = true, Berry = true, Nut = true, Insect = true, Roe = true,
}

-- Gefangene Fische haben im Skript keinen FoodType: Vanillas eigene Liste Fishing.fishes (reine Lua-Tabelle,
-- shared/Fishing/fishing_properties.lua:216-237, je Eintrag .itemType wie "Base.LargemouthBass", gesetzt in :94).
-- Einmal beim ersten Gebrauch in eine Menge umgefuellt; solange Fishing fehlt, wird nichts gemerkt.
local fishSet = nil
local function fishTypes()
    if fishSet then return fishSet end
    local set = {}
    if Fishing and type(Fishing.fishes) == "table" then
        for _, cfg in pairs(Fishing.fishes) do
            if type(cfg) == "table" and type(cfg.itemType) == "string" then set[cfg.itemType] = true end
        end
        fishSet = set
    end
    return set
end

-- Klasse eines Gegenstands: "fav" / "ok" / "snack", sonst nil und der Grund als Textschluessel.
-- instanceof(item, "Food"), getFoodType, getHungerChange, isRotten: Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:37;
-- getFullType: ebenda :55; isBurnt: client/ISUI/ISInventoryPane.lua:990.
-- getHungerChange() ist der Skriptwert / 100 (Honig -20 -> -0.2; Jar Food.java:1413 rechnet fuer die Anzeige mal 100).
function B.FoodClass(item)
    if item == nil or not instanceof(item, "Food") then return nil, WHY_NOT end
    local hunger = item:getHungerChange()
    if hunger == nil or hunger >= 0 then return nil, WHY_NOT end
    local full = item:getFullType()
    local kind = item:getFoodType()
    local class = nil
    if full == "Base.Honey" or kind == "Fish" or fishTypes()[full] == true then
        class = "fav"
    elseif kind ~= nil and OK_TYPES[kind] == true then
        class = "ok"
    end
    if class == nil then return nil, WHY_NOT end
    if item:isRotten() or item:isBurnt() then return nil, WHY_ROTTEN end
    if class == "ok" and hunger > -B.CFG.snackBelow then class = "snack" end
    return class, nil
end

-- Koeder-Futter: nur Klasse "fav" (Honig oder Fisch), nicht verdorben. Rueckgabe: boolean, "honey" / "fish".
function B.IsBaitFood(item)
    local class, _ = B.FoodClass(item)
    if class ~= "fav" then return false, nil end
    if item:getFullType() == "Base.Honey" then return true, "honey" end
    return true, "fish"
end

local RANK = { fav = 1, ok = 2, snack = 3 }

-- Futterliste fuer das Menue (nur Client): je Anzeigename eine Zeile { item, class, name, count }, Lieblingsfutter zuerst,
-- hoechstens max Zeilen. getAllEvalRecurse(fn), :size(), :get(i): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:33-53;
-- getDisplayName: shared/Definitions/animal/ButcheringUtil.lua:334.
function B.FoodList(player, max)
    local rows = {}
    if not player then return rows end
    local inv = player:getInventory()
    if not inv then return rows end
    local found = inv:getAllEvalRecurse(function(item)
        local class, _ = B.FoodClass(item)
        return class ~= nil
    end)
    if not found then return rows end
    local byName = {}
    for i = 0, found:size() - 1 do
        local item = found:get(i)
        local class, _ = B.FoodClass(item)
        if class ~= nil then
            local name = item:getDisplayName()
            local row = byName[name]
            if row == nil then
                row = { item = item, class = class, name = name, count = 0 }
                byName[name] = row
                rows[#rows + 1] = row
            elseif RANK[class] < RANK[row.class] then
                -- gleicher Name, bessere Klasse (z. B. ein ganzes Stueck neben einem Happen): das bessere Stueck zeigen
                row.item = item
                row.class = class
            end
            row.count = row.count + 1
        end
    end
    -- Nach Klasse ordnen, innerhalb der Klasse in Fundfolge (kleine Liste: Einfuegen, kein Zeichenketten-Vergleich).
    local sorted = {}
    for rank = 1, 3 do
        for i = 1, #rows do
            if RANK[rows[i].class] == rank then sorted[#sorted + 1] = rows[i] end
        end
    end
    max = tonumber(max) or #sorted
    local out = {}
    for i = 1, #sorted do
        if i > max then break end
        out[i] = sorted[i]
    end
    return out
end
