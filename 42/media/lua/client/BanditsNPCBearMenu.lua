--
-- NPC Crew -- Baer, Rechtsklick (B1a, PLAN_ZAEHMEN.md 5.2-5.4, 5.7, 6.8).
--
-- Tier-Menue: am Jungen (Art B.CUB) "Fuettern" (Untermenue mit dem Futter aus dem Inventar) und "Streicheln"; Vanillas "Kill"
-- wird am Jungen ausgeblendet (Menue-Hygiene, kein Schutz). Welt-Menue: "Baeren-Koeder auslegen" und "Koederplatz aufgeben".
-- B1b (PLAN_B1B.md 1.1, 3.1, 3.2): am eigenen gezaehmten Jungen der Umschalter "Follow me" / "Stay here" und "Name the cub"
-- (nur der Besitzer, nur mit Sicht-Eintrag); im Welt-Menue "Hold out food for the cub" (Futter nur in die Hand nehmen, ohne das
-- Tier anzuklicken), wenn ein passendes Junges in B.CFG.lureDist Kacheln steht.
--
-- Das Menue BIETET nur AN. Es stellt Zeitaktionen an (Fuettern, Streicheln, Koeder) bzw. schickt eine Bitte (Koederplatz
-- aufgeben); ob etwas gilt, entscheidet der Schreiber in complete() bzw. in B.Handle (Einzelspieler: dasselbe Programm,
-- Mehrspieler: der Server). Die grauen Punkte sind nur eine Vorpruefung mit denselben Regel-Funktionen des Kerns
-- (B.CheckFeed, B.CheckPet, B.CheckBait) auf der Sicht des Spielers; lehnt der Schreiber trotzdem ab, kommt seine Meldung.
-- Nichts hier nimmt oder gibt einen Gegenstand. Laeuft nur beim Rechtsklick, nie je Bild.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local DROP_RANGE = 3    -- Kacheln: so nah am eigenen Koederplatz gibt es "Koederplatz aufgeben" (Plan 6.8)

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------

-- Tooltip an einem Menuepunkt. Form: client/ISUI/Animal/ISAnimalContextMenu.lua:161-163 (addToolTip :161, setName :162),
-- client/ISUI/ISWorldObjectContextMenu.lua:271-273 (description).
local function setTip(option, name, text)
    local tip = ISWorldObjectContextMenu.addToolTip()
    if name then tip:setName(name) end
    if text then tip.description = text end
    option.toolTip = tip
    return tip
end

-- Grauer Punkt mit Grund: ISAnimalContextMenu.lua:160-163.
local function setGray(option, text)
    option.notAvailable = true
    setTip(option, nil, text)
end

-- Die Sicht des Spielers, wenn sie von diesem Spiel ist (sonst nil: dann wird nichts vorgeprueft, der Schreiber entscheidet).
local function viewMe()
    if not U.Fresh or not U.Fresh() then return nil end
    return B.View.me
end

-- Der n-te Menuepunkt mit diesem Namen. Vanilla legt je angeklicktem Tier einen Punkt mit animal:getFullName() an
-- (ISAnimalContextMenu.lua:140-141); zwei Junge heissen gleich. Der erste geht ueber Vanillas eigene Suche
-- (context:getOptionFromName, client/Tutorial/Tutorial1.lua:131), ab dem zweiten dieselbe Schleife mit Zaehler
-- (context.options ist eine Lua-Tabelle, client/ISUI/ISContextMenu.lua:889-895).
local function nthOption(context, name, n)
    if n <= 1 then return context:getOptionFromName(name) end
    local seen = 0
    for _, opt in ipairs(context.options) do
        if opt.name == name then
            seen = seen + 1
            if seen == n then return opt end
        end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Klick-Handler: stellen nur Aktionen an
-- ---------------------------------------------------------------------------

-- Fuettern (Plan 5.3). Reihenfolge ist Absicht: ZUERST das Futter in die Hand, DANN hingehen -- mit Futter in der Hand haelt der
-- Takt des Schreibers das Junge fest. luautils.walkAdj leert ohne drittes Argument die Warteschlange
-- (shared/luautils.lua:119-122) und wuerde das Anlegen wieder streichen; deshalb erst selbst leeren, dann mit keepActions gehen.
local function onFeed(playerObj, animal, food)
    if not playerObj or not animal or not food then return end
    if not animal:isExistInTheWorld() then return end               -- ISAnimalContextMenu.lua:88
    local sq = animal:getSquare()                                   -- :90
    if not sq then return end
    ISTimedActionQueue.clear(playerObj)                             -- client/ISUI/ISWorldObjectContextMenu.lua:1056
    -- equip holt das Stueck bei Bedarf selbst aus der Tasche (transferIfNeeded, ISWorldObjectContextMenu.lua:2606-2612)
    ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)    -- ISAnimalContextMenu.lua:93
    if luautils.walkAdj(playerObj, sq, true) then                   -- ISWorldObjectContextMenu.lua:2564 (keepActions)
        ISTimedActionQueue.add(BanditsNPCBearFeedAction:new(playerObj, animal, food))   -- ISAnimalContextMenu.lua:94
    end
end

-- Streicheln (Plan 5.4): hingehen, dann die Aktion.
local function onPet(playerObj, animal)
    if not playerObj or not animal then return end
    if not animal:isExistInTheWorld() then return end
    local sq = animal:getSquare()
    if not sq then return end
    if luautils.walkAdj(playerObj, sq) then                         -- ISAnimalContextMenu.lua:90
        ISTimedActionQueue.add(BanditsNPCBearPetAction:new(playerObj, animal))
    end
end

-- Koeder auslegen (Plan 5.2): hingehen, Stueck bei Bedarf aus der Tasche holen, dann die Aktion. Reihenfolge wie Vanillas
-- Fuettern (ISAnimalContextMenu.lua:90-94): walkAdj leert die Warteschlange, alles Weitere kommt danach hinein.
local function onBait(playerObj, food, sq)
    if not playerObj or not food or not sq then return end
    if luautils.walkAdj(playerObj, sq) then
        ISWorldObjectContextMenu.transferIfNeeded(playerObj, food)  -- ISAnimalContextMenu.lua:577
        ISTimedActionQueue.add(BanditsNPCBearBaitAction:new(playerObj, food, sq:getX(), sq:getY(), sq:getZ()))
    end
end

-- Koederplatz aufgeben: eine Bitte an den Schreiber, der den Besitz selbst prueft.
local function onBaitDrop(playerObj, baitId)
    if not playerObj or baitId == nil then return end
    B.Ask(playerObj, "BaitDrop", { id = baitId })
end

-- Folgen / Bleiben (B1b, Plan 1.1): nur eine Bitte. Ob sie gilt (Besitz, Fahrzeug, Abstand), entscheidet der Schreiber
-- (Einzelspieler: B.Handle direkt; Mehrspieler: sendClientCommand). Die Tabelle ist nie leer (Plan 5.5).
local function onMode(playerObj, id, mode)
    if not playerObj or id == nil then return end
    if mode ~= "follow" and mode ~= "stay" then return end
    B.Ask(playerObj, "Mode", { id = id, mode = mode })
end

-- Umbenennen (B1b, Plan 3.1): das Eingabefenster (client/ISUI/BanditsNPCBearNameBox.lua) schickt die Bitte "Rename".
local function onName(playerObj, v)
    if not playerObj or not v or not U.AskName then return end
    U.AskName(playerObj, v)
end

-- Futter hinhalten (B1b, Plan 3.2): das Stueck NUR in die Hand nehmen -- kein Hingehen, die Warteschlange bleibt. equip holt es
-- bei Bedarf selbst aus der Tasche (transferIfNeeded) und stellt ISEquipWeaponAction an (client/ISUI/ISWorldObjectContextMenu.lua:2594-2622);
-- derselbe Aufruf mit Futter: client/ISUI/Animal/ISAnimalContextMenu.lua:93. Danach greift die Regel des Schreibers "Futter in
-- der Hand und stillstehen -> das Junge kommt naeher". Kein Gegenstand wird erzeugt oder vernichtet.
local function onHold(playerObj, food)
    if not playerObj or not food then return end
    ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)
end

-- ---------------------------------------------------------------------------
-- Tier-Menue
-- ---------------------------------------------------------------------------

-- Tooltip der freien Punkte: Stand des Balkens und der Hinweis auf die Mischung.
local function tipStatus(option, v)
    local name = nil
    if v and type(v.tame) == "number" and v.st ~= "tame" then
        name = U.T("UI_BN_Bear_Hud_Taming", math.floor(v.tame))
    end
    setTip(option, name, U.T("UI_BN_Bear_Tip_Mix"))
end

-- Text einer Futterzeile (Fuettern und Futter hinhalten): Lieblingsfutter / normal / nur ein Happen, dazu die Anzahl.
local function foodLabel(row)
    local label
    if row.class == "fav" then
        label = U.T("UI_BN_Bear_Food_Fav", row.name)
    elseif row.class == "snack" then
        label = U.T("UI_BN_Bear_Food_Snack", row.name)
    else
        label = U.T("UI_BN_Bear_Food_Ok", row.name)
    end
    if type(row.count) == "number" and row.count > 1 then
        label = label .. " (" .. tostring(row.count) .. ")"
    end
    return label
end

local function addFeed(menu, playerObj, animal, v, me, key)
    local feedOpt = menu:addOption(U.T("UI_BN_Bear_Menu_Feed"), nil, nil)       -- ISAnimalContextMenu.lua:272 (Punkt mit Untermenue)
    if v and me then
        local ok, whyKey, whyVal = B.CheckFeed(v, key, me, B.Now())
        if not ok then
            setGray(feedOpt, U.WhyText(whyKey, whyVal))
            return
        end
    end
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    if not rows or #rows == 0 then
        setGray(feedOpt, U.T("UI_BN_Bear_Menu_NoFood"))
        return
    end
    tipStatus(feedOpt, v)
    local sub = ISContextMenu:getNew(menu)                                      -- ISAnimalContextMenu.lua:273
    menu:addSubMenu(feedOpt, sub)                                               -- :274
    for _, row in ipairs(rows) do
        sub:addOption(foodLabel(row), playerObj, onFeed, animal, row.item)      -- ISAnimalContextMenu.lua:280
    end
end

local function addPet(menu, playerObj, animal, v, me, key)
    local petOpt = menu:addOption(U.T("UI_BN_Bear_Menu_Pet"), playerObj, onPet, animal)     -- ISAnimalContextMenu.lua:287
    petOpt.iconTexture = getTexture("media/ui/AnimalActions_Pet.png")                       -- :288
    if v and me then
        local ok, whyKey, whyVal = B.CheckPet(v, key, me, B.Now())
        if not ok then
            setGray(petOpt, U.WhyText(whyKey, whyVal))
            return
        end
    end
    tipStatus(petOpt, v)
end

-- Zustand des Jungen laut Sicht (Regel des Kerns B.ModeOf, Plan 5.3: nil und alles andere heisst "stay").
local function modeOf(v)
    local f = B.ModeOf
    if f then return f(v) end
    if v.mode == "follow" then return "follow" end
    return "stay"
end

-- Umschalter (Plan 1.1): bei "stay" steht "Follow me", bei "follow" "Stay here" -- nie beide. Grau nur mit Grund: im Fahrzeug
-- kann das Junge nicht folgen (Vorpruefung; alles andere entscheidet der Schreiber). getVehicle() am Spieler:
-- client/ISUI/Hutch/ISHutchMenu.lua:8.
local function addMode(menu, playerObj, v)
    if modeOf(v) == "follow" then
        local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Stay"), playerObj, onMode, v.id, "stay")
        setTip(opt, nil, U.T("UI_BN_Bear_Menu_StayTip"))
        return
    end
    local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Follow"), playerObj, onMode, v.id, "follow")
    if playerObj:getVehicle() then
        setGray(opt, U.T("UI_BN_Bear_Why_InCar"))
        return
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_FollowTip"))
end

-- "Name the cub" (Plan 3.1): kein Graufall.
local function addName(menu, playerObj, v)
    menu:addOption(U.T("UI_BN_Bear_Menu_Name"), playerObj, onName, v)
end

-- Ein Junges: Vanillas Untermenue suchen (fehlt es, auf die oberste Ebene), "Kill" entfernen, eigene Punkte anhaengen.
local function cubMenu(context, playerObj, animal, name, nth)
    local menu = context
    local opt = nthOption(context, name, nth)
    if opt and opt.subOption then
        local sub = context:getSubMenu(opt.subOption)       -- client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:41
        if sub then
            menu = sub
            -- Vanilla bietet "Kill" fuer jedes nicht wilde Tier an (ISAnimalContextMenu.lua:307-324); am Jungen blenden wir es
            -- aus. removeOptionByName ist reines Lua (client/ISUI/ISContextMenu.lua:1016).
            sub:removeOptionByName(getText("ContextMenu_KillAnimal"))           -- Text: ISAnimalContextMenu.lua:310
        end
    end
    local me = viewMe()
    local v = nil
    if me then v = B.ViewOf(animal) end
    if not v then
        -- Der Client kennt dieses Junge (noch) nicht: Punkte bleiben frei, der Schreiber entscheidet; Sicht nachfragen.
        if U.AskHello then U.AskHello(playerObj) end
    end
    local key = B.PlayerKey(playerObj)
    addFeed(menu, playerObj, animal, v, me, key)
    addPet(menu, playerObj, animal, v, me, key)
    -- B1b: nur am eigenen gezaehmten Jungen und nur, wenn die Sicht es kennt (Fremde sehen die Punkte gar nicht, Plan 1.1, 1.6).
    if v and v.id ~= nil and v.st == "tame" and key ~= nil and v.owner == key then
        addMode(menu, playerObj, v)
        addName(menu, playerObj, v)
    end
end

-- Vanillas eigenes Tier-Menue haengt am selben Ereignis (ISAnimalContextMenu.lua:1013-1017, :1235) und laedt vor uns: sein
-- Untermenue je Tier steht schon, wenn wir drankommen.
local function onClickedAnimals(player, context, animals, test)
    if not B.CUB or not B.T or not B.View then return end
    local cubs = nil
    for _, a in ipairs(animals) do                                              -- ISAnimalContextMenu.lua:1014
        if a:getAnimalType() == B.CUB then                                      -- client/ISUI/Animal/ISAnimalUI.lua:65
            cubs = cubs or {}
            cubs[#cubs + 1] = a
        end
    end
    if not cubs then return end
    -- Probelauf fuer Controller: nur melden, dass es Eintraege gibt (client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81).
    if test then return ISWorldObjectContextMenu.setTest() end
    local playerObj = getSpecificPlayer(player)                                 -- ISAnimalContextMenu.lua:134
    if not playerObj then return end
    -- Je Name mitzaehlen: das zweite Junge gleichen Namens gehoert zum zweiten Vanilla-Punkt dieses Namens.
    local seen = {}
    for _, a in ipairs(cubs) do
        local name = a:getFullName()                                            -- ISAnimalContextMenu.lua:140
        seen[name] = (seen[name] or 0) + 1
        cubMenu(context, playerObj, a, name, seen[name])
    end
end

-- ---------------------------------------------------------------------------
-- Welt-Menue: Koeder
-- ---------------------------------------------------------------------------

-- Koeder-Futter im Inventar: die Zeilen der Futterliste des Kerns, die Koeder sein duerfen (Honig oder Fisch).
local function baitRows(playerObj)
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    local out = {}
    if not rows then return out end
    for _, row in ipairs(rows) do
        local ok, kind = B.IsBaitFood(row.item)
        if ok then
            row.kind = kind
            out[#out + 1] = row
        end
    end
    return out
end

local function addBaitDrop(context, playerObj, sq, view)
    local bait = view.bait
    if not bait or bait.id == nil then return false end
    if sq:getZ() ~= bait.z then return false end
    if math.abs(sq:getX() - bait.x) > DROP_RANGE or math.abs(sq:getY() - bait.y) > DROP_RANGE then return false end
    local opt = context:addOption(U.T("UI_BN_Bear_Menu_BaitDrop"), playerObj, onBaitDrop, bait.id)
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_BaitDropTip"))
    return true
end

local function addBait(context, playerObj, sq, me, rows, near)
    local opt = context:addOption(U.T("UI_BN_Bear_Menu_Bait"), nil, nil)
    if not near then
        setGray(opt, U.T("UI_BN_Bear_Bait_NotForest"))
        return
    end
    if not sq:isOutside() then                                  -- client/Foraging/ISZoneDisplay.lua:400
        setGray(opt, U.T("UI_BN_Bear_Bait_Inside"))
        return
    end
    if me then
        local ok, whyKey, whyVal = B.CheckBait(me)
        if not ok then
            setGray(opt, U.WhyText(whyKey, whyVal))
            return
        end
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_BaitTip"))
    local sub = ISContextMenu:getNew(context)                   -- client/ISUI/Animal/ISAnimalContextMenu.lua:48
    context:addSubMenu(opt, sub)                                -- :49
    for _, row in ipairs(rows) do
        local label = U.T("UI_BN_Bear_Food_Ok", row.name)
        if type(row.count) == "number" and row.count > 1 then
            label = label .. " (" .. tostring(row.count) .. ")"
        end
        local rowOpt = sub:addOption(label, playerObj, onBait, row.item, sq)
        setTip(rowOpt, nil, U.T("UI_BN_Bear_Menu_BaitTip"))
    end
end

-- ---------------------------------------------------------------------------
-- Welt-Menue: Futter hinhalten (B1b, Plan 3.2)
-- ---------------------------------------------------------------------------

-- Steht ein Junges mit Objekt in B.CFG.lureDist Kacheln um den Spieler, das auf sein Futter reagiert? Wie die Regel des
-- Schreibers (server keysOf): scheue (new/shy) jeder, angefuetterte nur der Gebundene, gezaehmte nur der Besitzer -- und nur,
-- solange es bleibt: ein folgendes Junges rechnet B.FollowDecide, dort spielt Futter keine Rolle (Nachbesserung B1b B6).
local function holdWanted(playerObj, key)
    if not U.CubsNear or key == nil then return false end
    local near = U.CubsNear(playerObj, B.CFG.lureDist or 15)
    for i = 1, #near do
        local c = near[i].c
        local st = c.st
        if st == "new" or st == "shy" then return true end
        if st == "fed" and c.bond == key then return true end
        if st == "tame" and c.owner == key and modeOf(c) ~= "follow" then return true end
    end
    return false
end

local function addHold(context, playerObj)
    local opt = context:addOption(U.T("UI_BN_Bear_Menu_Hold"), nil, nil)
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    if not rows or #rows == 0 then
        setGray(opt, U.T("UI_BN_Bear_Menu_NoFood"))
        return
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_HoldTip"))
    local sub = ISContextMenu:getNew(context)                   -- client/ISUI/Animal/ISAnimalContextMenu.lua:48
    context:addSubMenu(opt, sub)                                -- :49
    for _, row in ipairs(rows) do
        sub:addOption(foodLabel(row), playerObj, onHold, row.item)
    end
end

local function onFillWorld(player, context, worldobjects, test)
    -- Dieselbe Tuer wie Vanillas Menues: client/ISUI/Hutch/ISHutchMenu.lua:4
    if test and ISWorldObjectContextMenu.Test then return true end
    if not B.CUB or not B.T or not B.View or not B.Opt then return end
    local playerObj = getSpecificPlayer(player)                 -- ISHutchMenu.lua:6
    if not playerObj or playerObj:getVehicle() then return end  -- ISHutchMenu.lua:8
    local sq = nil
    for _, o in ipairs(worldobjects) do                         -- ISHutchMenu.lua:11
        sq = o:getSquare()                                      -- client/ISUI/ISWorldObjectContextMenu.lua:2571
        if sq then break end
    end
    if not sq then return end

    -- Die alte Sicht eines anderen Spielstands wird nicht benutzt (U.Fresh); ohne Sicht kein Koeder-Punkt.
    local me = viewMe()
    if not me then return end
    local view = B.View

    -- Aufgeben geht immer am eigenen Platz, auch ohne Koeder in der Tasche.
    if view.bait and view.bait.id ~= nil then
        if test then
            if sq:getZ() == view.bait.z and math.abs(sq:getX() - view.bait.x) <= DROP_RANGE
                and math.abs(sq:getY() - view.bait.y) <= DROP_RANGE then
                return ISWorldObjectContextMenu.setTest()       -- client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81
            end
        else
            addBaitDrop(context, playerObj, sq, view)
        end
    end

    -- B1b: Futter hinhalten -- nur wenn ein passendes Junges nah ist (sonst kein Menue-Muell in der Stadt). Steht VOR dem Riegel
    -- des Koeder-Teils: auch mit ausgeschaltetem Koeder oder ausgeschalteten neuen Jungen bleibt das eigene Junge lockbar.
    if holdWanted(playerObj, B.PlayerKey(playerObj)) then
        if test then return ISWorldObjectContextMenu.setTest() end
        addHold(context, playerObj)
    end

    -- Auslegen: nur wenn Junge und Koeder eingeschaltet sind (sonst kein Menue-Muell).
    if me.on == false or B.Opt("BearBaitEnabled") == false then return end
    local rows = baitRows(playerObj)
    if #rows == 0 then return end
    local near = B.NearForest(sq:getX(), sq:getY(), sq:getZ(), B.CFG.baitEdge)
    if not near then
        -- Ausserhalb des Waldes nur dann ein (grauer) Punkt, wenn der Spieler Honig oder Fisch in der Hand haelt.
        local hand = playerObj:getPrimaryHandItem()             -- ISAnimalContextMenu.lua:93
        if not hand then return end
        local inHand = B.IsBaitFood(hand)
        if not inHand then return end
    end
    if test then return ISWorldObjectContextMenu.setTest() end
    addBait(context, playerObj, sq, me, rows, near)
end

Events.OnClickedAnimalForContext.Add(onClickedAnimals)          -- client/ISUI/Animal/ISAnimalContextMenu.lua:1235
Events.OnFillWorldObjectContextMenu.Add(onFillWorld)            -- client/ISUI/Hutch/ISHutchMenu.lua:115
