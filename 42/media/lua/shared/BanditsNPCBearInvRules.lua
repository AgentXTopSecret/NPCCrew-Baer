--
-- NPC Crew -- Baer, Inventar-Regeln (F4, PLAN_F4.md 3, 4, 5, 11; Kevins Antworten 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md).
--
-- Rein und auf BEIDEN Seiten: der Client fragt B.InvCanCarry nur zum Grauen im Fenster, entschieden wird beim Schreiber in complete()
-- (server/BanditsNPCBearInv.lua). Hier stehen: welcher Gegenstand verlustfrei als Datensatz ("Satz") reist, wie er gelesen und wieder
-- gebaut wird (Feld-Module), Stapel-Gleichheit, Traglast, Verderben unterwegs, die Zeile fuer das Fenster.
--
-- Kevin 13.11. Antwort 1: der Baer traegt ALLES ("alles was es gibt"), was ein Satz VOLLSTAENDIG zurueckbringt. Jar-Ausnahme "Ja, dieselben
-- wie NPC Crew": genau die Methoden aus f4/JAR_LISTE.md Abschnitt 0 (A2 gekocht/verbrannt/gefroren, A3 Schaerfe/Kopf, A4 Zutaten/Gewuerze,
-- A10 Farbton) -- jeder solche Aufruf mit Existenz-Riegel und der Kennung "JAR A<n>" im Kommentar (geprueft von f4/werkzeug_kern/feldpruefer.py).
-- Was selbst NPC Crew nicht verlustfrei kann, lehnt der Baer mit Grund ab (UI_BN_Bear_Why_InvLossy) oder es ist als "Rest" benannt
-- (BAU_KERN.md, Fragen fuer Kevin) -- nie still. Taschen nur LEER (UI_BN_Bear_Why_InvBagFirst, Vorschlag aus dem Auftrag, Frage fuer Kevin).
--
-- Ein Satz enthaelt nur Text, Zahl, Wahrheitswert und Tabelle (KahluaTableImpl.save speichert nichts anderes, f4/FORSCHUNG_F4.md 0.3).
-- Kennungen der Felder: siehe FELDER unten (jede Zeile "BELEG" nennt die Fundstelle mit gleicher Argument-Art).
-- Statisch geprueft, nicht gespielt.
--
-- JAR-AUSNAHMEN (Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md:5-6: "Ja, dieselben wie NPC Crew") -- NUR diese, je Aufruf-Zeile "JAR A<n>",
-- jeder hinter einem Existenz-Riegel (fehlt die Methode nach einem PZ-Update, lehnt der Baer das Stueck beim GEBEN ab, nie still ohne den Wert).
-- Jar 42.22, javap -c -p in f4/gates_javap/<Klasse>.txt (Zeile = Methodenkopf; Offsets aus f4/JAR_LISTE.md 0 / f4/GATES.md):
--   A2 InventoryItem.setCooked(Z)V        InventoryItem.txt:7548, Offset 0-29 (Feld + cookingTime auf getMinutesToCook; kein Paket)  NC:shared/BanditsNPC.lua:5021
--   A2 InventoryItem.setBurnt(Z)V         InventoryItem.txt:7573, Offset 0-29 (wie setCooked mit getMinutesToBurn)                   NC:shared/BanditsNPC.lua:5019
--   A2 InventoryItem.setCookingTime(F)V   InventoryItem.txt:7509, Offset 0-5 (putfield)                                               NC:shared/BanditsNPC.lua:5027
--   A2 InventoryItem.setOffAge(I)V        InventoryItem.txt:7598, Offset 0-5                                                          NC:shared/BanditsNPC.lua:5029
--   A2 InventoryItem.setOffAgeMax(I)V     InventoryItem.txt:7611, Offset 0-5                                                          NC:shared/BanditsNPC.lua:5030
--   A2 Food.setFreezingTime(F)V           Food.txt:6035, Offset 0-38 (klemmt 0..100, kippt frozen an den Raendern)                   NC:shared/BanditsNPC.lua:5035
--   A2 Food.setFrozen(Z)V                 Food.txt:6074, Offset 0-5                                                                   NC:shared/BanditsNPC.lua:5036
--      Kevins Wort fuer NC: NPC Crew CLAUDE.md:219-228 (19.09. "ja bau"); setCooked seit Bandits 42.22 auch Lua-belegt (B:shared/Bandit.lua:883).
--   A3 InventoryItem.getSharpness()F      InventoryItem.txt:11693, Offset 0-47 (42.22 klemmt per applyMaxSharpness, nur das Attribut)    NC:shared/BanditsNPC.lua:4538
--   A3 InventoryItem.setSharpness(F)V     InventoryItem.txt:11775, Offset 0-57 (klemmt gegen getMaxSharpness)                          NC:shared/BanditsNPC.lua:4587
--   A3 InventoryItem.getHeadCondition()I  InventoryItem.txt:12180, Offset 0-22                                                         NC:shared/BanditsNPC.lua:4539
--      Kevins Wort fuer NC: NPC Crew CLAUDE.md:230-237 (20.09. "dann bau das noch").
--   A4 InventoryItem.addExtraItem(Ljava/lang/String;)V  InventoryItem.txt:8700, Offset 0-27                                           NC:shared/BanditsNPC.lua:4993
--   A4 Food.setSpices(Ljava/util/ArrayList;)V           Food.txt:5732, Offset 0-64                                                    NC:shared/BanditsNPC.lua:5006
--      Kevins Wort fuer NC: NPC Crew CLAUDE.md:247-263 (30.09.); addExtraItem seit Bandits 42.22 auch Lua-belegt (B:shared/Bandit.lua:878).
--   A10 ItemVisual.getHue()F (ohne Argument)  ItemVisual.txt:249, Offset 0-4                                                          NC:client/BanditsNPCInteract.lua:6181
--   A10 ItemVisual.setHue(F)V                 ItemVisual.txt:234, Offset 0-18 (klemmt [-1, 1])                                      NC:client/BanditsNPCInteract.lua:6247
--      Kevins Wort fuer NC: NPC Crew CLAUDE.md:403-457 (25.10.).
-- NICHT gedeckt und NICHT benutzt: ItemVisual.getTint() ohne Argument (hier Vanillas Form getTint(ClothingItem)), get/setHaveBeenRepaired
-- (Reparatur-Zaehler reist nicht), getBoredomChange (Langeweile reist nicht), getMaxSharpness, Kartensymbole, Radio-Geraetedaten.
-- Geprueft von f4/werkzeug_kern/feldpruefer.py (jede Methode: Vanilla/Bandits-Zeile maschinell gegengelesen ODER diese Liste).
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local INV = {}                      -- interne Helfer (eine Tabelle statt vieler Locals)

local function cfg(k, d)
    local c = B.CFG
    local v = c and tonumber(c[k]) or nil
    if v == nil then return d end
    return v
end

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

-- ---------------------------------------------------------------------------
-- Tabellen: Kopie nur speicherbarer Werte, Groesse, Gleichheit
-- ---------------------------------------------------------------------------

-- Tiefe Kopie mit Groessen-Schaetzung (Zeichen). Rueckgabe: kopie, ok, groesse. ok = false, wenn ein Wert nicht speicherbar ist (Funktion,
-- Java-Objekt) oder die Tiefe 8 ueberschreitet -- der Aufrufer lehnt dann ab (nie still weglassen).
function INV.copy(v, depth)
    local tv = type(v)
    if tv == "string" then return v, true, string.len(v) + 2 end
    if tv == "number" then
        if v ~= v then return nil, false, 0 end
        return v, true, 9
    end
    if tv == "boolean" then return v, true, 2 end
    if tv ~= "table" then return nil, false, 0 end
    depth = depth or 0
    if depth > 8 then return nil, false, 0 end
    local out = {}
    local size = 4
    for k, x in pairs(v) do
        local tk = type(k)
        if tk ~= "string" and tk ~= "number" then return nil, false, 0 end
        local cx, ok, sx = INV.copy(x, depth + 1)
        if not ok then return nil, false, 0 end
        out[k] = cx
        if tk == "string" then size = size + string.len(k) + 2 else size = size + 9 end
        size = size + sx
    end
    return out, true, size
end

-- Bytes eines Werts in der Form der Engine (KahluaTableImpl.save / TableNetworkUtils.save; Formel wie NPC Crew R.ByteSize laut f4/GATES.md G5):
-- Tabelle 4 + je Paar (Schluessel + Wert), Text 1 + 2 + Zeichen (x 3 fuer Nicht-ASCII, obere Schranke), Zahl 1 + 8, Wahrheitswert 1 + 1.
function INV.bytes(v)
    local tv = type(v)
    if tv == "string" then return 3 + string.len(v) * 3 end
    if tv == "number" then return 9 end
    if tv == "boolean" then return 2 end
    if tv ~= "table" then return 0 end
    local n = 4
    for k, x in pairs(v) do n = n + INV.bytes(k) + INV.bytes(x) end
    return n
end

function B.InvBytes(v)
    return INV.bytes(v)
end

function B.InvCopy(v)
    local c, ok, _ = INV.copy(v, 0)
    if not ok then return nil end
    return c
end

-- Gleichheit zweier Werte (Tabellen tief; Zahlen mit 1e-6 Spiel, damit gespeicherte Doubles nicht an der letzten Stelle trennen).
function INV.same(a, b)
    local ta, tb = type(a), type(b)
    if ta ~= tb then return false end
    if ta == "number" then return math.abs(a - b) < 0.000001 end
    if ta ~= "table" then return a == b end
    for k, x in pairs(a) do
        if not INV.same(x, b[k]) then return false end
    end
    for k, _ in pairs(b) do
        if a[k] == nil then return false end
    end
    return true
end

-- ---------------------------------------------------------------------------
-- Was nie reist (Ablehnung "nicht verlustfrei"). Gruende nur fuer Log und Bericht; im Fenster steht UI_BN_Bear_Why_InvLossy.
-- ---------------------------------------------------------------------------
-- Leichen-Gegenstaende (VS:generated/items/normal.txt:8560, :8573, food.txt:1331): ihr Koerper steckt in Engine-Daten ohne Lua-Weg.
INV.NEVER = { ["Base.CorpseMale"] = "corpse", ["Base.CorpseFemale"] = "corpse", ["Base.CorpseAnimal"] = "corpse" }

-- Anbau-Plaetze einer Schusswaffe (NPC Crew NC:shared/BanditsNPC.lua:4436, Platz-Namen aus scripts weaponpart.txt).
INV.PARTS = { "Scope", "Sling", "RecoilPad", "Canon", "Stock", "Clip" }
INV.XI_MAX = 16                     -- Zutaten / Gewuerze je Gericht (NC:shared/BanditsNPC.lua:4265 XI_MAX)
INV.NEVER_ROTS = 1000000000         -- Food.updateAge: OffAgeMax ab hier verdirbt nie (PLAN_F4.md 4.1, J:Food.updateAge Offset 301/338)

-- Vergleichs-Stueck je Typ (nur fuer die Anbauteile einer neu gebauten Waffe). instanceItem(Text): V:server/Fishing/BuildingObjects/FishingNet.lua:125
-- (Schreiber), V:client/ISUI/Animal/ISAnimalContextMenu.lua:1023 (Client). Kommt in keinen Behaelter. Deckel 64 Typen.
INV.ref = {}
INV.refN = 0
function INV.refOf(t)
    local r = INV.ref[t]
    if r ~= nil then return r end
    if INV.refN >= 64 then
        INV.ref = {}
        INV.refN = 0
    end
    r = instanceItem(t)
    if r == nil then return nil end
    INV.ref[t] = r
    INV.refN = INV.refN + 1
    return r
end

-- Nachbesserung F4 (Befund C9): gibt es den Typ einer Zutat / eines Gewuerzes? ScriptManager.instance:getItem(Text): V:client/ContextMenuCode.lua:67
-- (wie K.typeOk im Kern, server/BanditsNPCBearInv.lua). Die Engine speichert Zutaten und Gewuerze als Registry-Id -- ein unbekannter Typ wird -1
-- und kommt nach dem Laden als nil zurueck (NPC Crew CLAUDE.md:258 "Zwei Fallen, beide im Code beachtet"; NC:shared/BanditsNPC.lua:4993/:5003
-- pruefen FindItem). Darum: beim Geben nur Gerichte, deren Zutaten es alle gibt; beim Bauen fehlt eine -> kein Gericht mit kaputter Liste.
function INV.typeOk(t)
    if type(t) ~= "string" or t == "" then return false end
    return ScriptManager.instance:getItem(t) ~= nil
end

function INV.allKnown(list)
    if type(list) ~= "table" then return true end
    for i = 1, #list do
        if not INV.typeOk(list[i]) then return false end
    end
    return true
end

-- Koerperstellen fuer Blut/Schmutz/Loecher: BloodClothingType.getCoveredParts(item:getBloodClothingType())
-- BELEG getCoveredParts V:shared/TimedActions/ISWashClothing.lua:130 (Clothing ODER InventoryContainer); getBloodClothingType ebd.
function INV.parts(item)
    local out = {}
    local list = BloodClothingType.getCoveredParts(item:getBloodClothingType())
    if list == nil then return out end
    for i = 0, list:size() - 1 do
        local p = list:get(i)
        if p ~= nil then out[#out + 1] = p end
    end
    return out
end

-- Schluessel einer Koerperstelle als Text (ModData mischt nie Zahl- und Text-Schluessel). part:index(): V:client/DebugUIs/DebugMenu/General/
-- ISDebugBlood.lua:26 (BloodBodyPartType.MAX:index()); zurueck BloodBodyPartType.FromIndex(i): ebd. :27.
function INV.partKey(p)
    return "p" .. string.format("%d", p:index())
end

function INV.partOf(key)
    if type(key) ~= "string" or string.sub(key, 1, 1) ~= "p" then return nil end
    local i = tonumber(string.sub(key, 2))
    if i == nil then return nil end
    return BloodBodyPartType.FromIndex(i)
end

-- Zahl auf 4 Nachkommastellen (Stapel-Gleichheit; reicht fuer Zustand, Gewicht, Naehrwerte).
local function r4(v)
    local n = num(v)
    if n == nil then return nil end
    return math.floor(n * 10000 + 0.5) / 10000
end

-- ---------------------------------------------------------------------------
-- FELD-MODULE. Je Modul: id, read(item, s, x) -> nil oder Verlust-Grund (Text), write(item, s) -> true / false.
-- x = Lese-Kontext (Art-Merker). Reihenfolge der Liste = Reihenfolge beim Bauen (PLAN_F4.md 5 "Reihenfolge beim Bauen"; NC ApplyFood/ApplyExtra).
-- ---------------------------------------------------------------------------
INV.F = {}

-- Zustand. BELEG getConditionMax/getCondition V:client/ISUI/ISInventoryPane.lua:2666; setCondition(Zahl) V:shared/TimedActions/ISClothingExtraAction.lua:105.
INV.F[#INV.F + 1] = {
    id = "cond",
    read = function(item, s, x)
        local cm = item:getConditionMax()
        if cm > 0 then
            s.c = item:getCondition()
            s.cm = cm                                                                   -- nur Anzeige (Prozent im Fenster), Skriptwert
        end
        return nil
    end,
    write = function(item, s)
        if s.c ~= nil then item:setCondition(s.c) end
        return true
    end,
}

-- Kopfzustand und Schaerfe (Klingen, Reihenfolge c -> hc -> sh wie NC:shared/BanditsNPC.lua:4575-4589).
-- BELEG hasHeadCondition V:shared/Items/OnBreak.lua:106; hasSharpness V:shared/Items/OnBreak.lua:42;
-- BELEG setHeadCondition(Zahl), getHeadConditionMax B:shared/BanditCompatibility.lua:82.
-- JAR A3 getHeadCondition, getSharpness, setSharpness (Kevin 13.11. "Ja, dieselben wie NPC Crew"; f4/JAR_LISTE.md A3, NC:shared/BanditsNPC.lua:4538-4539).
INV.F[#INV.F + 1] = {
    id = "blade",
    read = function(item, s, x)
        if item:hasHeadCondition() then
            if item.getHeadCondition == nil or item.setHeadCondition == nil then return "headCondition (method missing)" end
            local hc = item:getHeadCondition()                                         -- JAR A3
            if hc ~= nil and hc > 0 and hc < item:getHeadConditionMax() then s.hc = hc end
        end
        if item:hasSharpness() then
            if item.getSharpness == nil or item.setSharpness == nil then return "sharpness (method missing)" end
            s.sh = item:getSharpness()                                                  -- JAR A3
        end
        return nil
    end,
    write = function(item, s)
        if s.hc ~= nil and item:hasHeadCondition() and s.hc < item:getHeadConditionMax() then item:setHeadCondition(s.hc) end
        if s.sh ~= nil then
            if item.setSharpness == nil then return false end
            item:setSharpness(s.sh)                                                     -- JAR A3
        end
        return true
    end,
}

-- Fuellstand von Verbrauchbarem (Batterie, Klebeband ...). BELEG instanceof(item, "Drainable") V:client/FeedingTrough/ISUI/ISFeedingTroughMenu.lua:202;
-- getCurrentUsesFloat V:client/ContextMenuCode.lua:55; setUsedDelta(Zahl) V:server/ClientCommands.lua:243 (gleiche Skala laut NC).
INV.F[#INV.F + 1] = {
    id = "uses",
    read = function(item, s, x)
        if x.drain then s.u = item:getCurrentUsesFloat() end
        return nil
    end,
    write = function(item, s)
        if s.u ~= nil then item:setUsedDelta(s.u) end
        return true
    end,
}

-- Schusswaffe / Magazin: Munition, Patrone im Lauf, Magazin drin, Ladehemmung, Feuermodus, Anbauteile.
-- BELEG getMaxAmmo/getCurrentAmmoCount V:client/ISUI/ISFirearmRadialMenu.lua:36; isRoundChambered :61; isContainsClip :30;
-- BELEG setRoundChambered(bool) setContainsClip(bool) setCurrentAmmoCount(Zahl) V:shared/Items/SpawnItems.lua:96-98 (Reihenfolge wie dort);
-- BELEG isJammed V:client/ISUI/ISFirearmRadialMenu.lua:200; setJammed(bool) V:shared/TimedActions/ISRackFirearm.lua:61;
-- BELEG getFireModePossibilities/getFireMode/setFireMode(Text)/setAmmoPerShoot(3) V:client/ISUI/ISInventoryPaneContextMenu.lua:1797-1809;
-- BELEG getWeaponPart(Text) V:shared/TimedActions/ISRemoveWeaponUpgrade.lua:17; attachWeaponPart(Teil) B:shared/BanditUtils.lua:804.
INV.F[#INV.F + 1] = {
    id = "gun",
    read = function(item, s, x)
        if item:getMaxAmmo() > 0 then
            s.a = item:getCurrentAmmoCount()
            if x.weapon then
                s.rc = item:isRoundChambered() and 1 or 0
                s.kc = item:isContainsClip() and 1 or 0
            end
        end
        if not x.weapon then return nil end
        if item:isRanged() then
            if item:isJammed() then s.jm = 1 end
            local poss = item:getFireModePossibilities()
            if poss ~= nil and poss:size() > 1 then s.fm = item:getFireMode() end
            -- Anbauteile: jedes Teil reist als Typ + Zustand + Batterie; ein Platz, den ein NEU gebautes Stueck schon belegt, das
            -- Original aber nicht (oder anders), ist nicht herstellbar -> Ablehnung (sonst ein Gratis-Teil).
            local ref = INV.refOf(s.t)
            local wp = nil
            for i = 1, #INV.PARTS do
                local k = INV.PARTS[i]
                local part = item:getWeaponPart(k)
                local rp = ref and ref:getWeaponPart(k) or nil
                if rp ~= nil and (part == nil or part:getFullType() ~= rp:getFullType()) then return "weapon part " .. k end
                if part ~= nil and rp == nil then
                    local e = { k = k, t = part:getFullType() }
                    if part:getConditionMax() > 0 then e.c = part:getCondition() end
                    if instanceof(part, "Drainable") then e.u = part:getCurrentUsesFloat() end
                    wp = wp or {}
                    wp[#wp + 1] = e
                elseif part ~= nil and rp ~= nil then
                    -- gleiches Teil wie im Neubau: nur dessen Zustand / Batterie reisen
                    local e = { k = k, t = part:getFullType(), keep = true }
                    if part:getConditionMax() > 0 then e.c = part:getCondition() end
                    if instanceof(part, "Drainable") then e.u = part:getCurrentUsesFloat() end
                    wp = wp or {}
                    wp[#wp + 1] = e
                end
            end
            s.wp = wp
        end
        return nil
    end,
    write = function(item, s)
        if s.rc ~= nil then item:setRoundChambered(s.rc == 1) end
        if s.kc ~= nil then item:setContainsClip(s.kc == 1) end
        if s.a ~= nil then item:setCurrentAmmoCount(s.a) end
        if s.jm == 1 then item:setJammed(true) end
        if s.fm ~= nil then
            item:setFireMode(s.fm)
            if s.fm == "Burst" then item:setAmmoPerShoot(3) end
        end
        if type(s.wp) == "table" then
            for i = 1, #s.wp do
                local e = s.wp[i]
                local part = nil
                if e.keep then
                    part = item:getWeaponPart(e.k)
                    if part == nil then return false end
                else
                    part = instanceItem(e.t)
                    if part == nil then return false end
                end
                if e.c ~= nil then part:setCondition(e.c) end
                if e.u ~= nil then part:setUsedDelta(e.u) end
                if not e.keep then item:attachWeaponPart(part) end
            end
        end
        return true
    end,
}

-- Blut an Waffen und sonstigem (Kleidung/Taschen fuehren Blut je Koerperstelle, Modul "cloth").
-- BELEG getBloodLevel V:shared/TimedActions/ISWashClothing.lua:69; setBloodLevel(Zahl) B:shared/Bandit.lua:890.
INV.F[#INV.F + 1] = {
    id = "blood",
    read = function(item, s, x)
        if x.cloth or x.bag then return nil end
        local b = item:getBloodLevel()
        if b ~= nil and b > 0 then s.bl = b end
        return nil
    end,
    write = function(item, s)
        if s.bl ~= nil then item:setBloodLevel(s.bl) end
        return true
    end,
}

-- Fluessigkeit (Flasche, Kanister, Eimer ...): nur leer oder EIN Stoff; Mischungen kommen in NPC Crew als Hauptstoff zurueck
-- (NC:shared/BanditsNPCBearWater.lua:206-245 Kopf) -> hier Ablehnung. q wird IMMER geschrieben (auch 0), sonst kaeme die Skript-Fuellung.
-- BELEG getFluidContainer/isEmpty/isMixture V:client/ISUI/ISInventoryPaneContextMenu.lua:3113; getAmount V:shared/Farming/TimedActions/ISWaterPlantAction.lua:118;
-- BELEG getPrimaryFluid/getFluidTypeString V:client/Farming/ISUI/ISFarmingMenu.lua:79; FluidType.FromNameLower(Text) V:server/ClientCommands.lua:1186;
-- BELEG adjustAmount(Zahl) V:shared/Fluids/ISFluidEmptyAction.lua:62; addFluid(FluidType, Zahl) V:client/ISUI/ISFluidContainerMenu.lua:76.
INV.F[#INV.F + 1] = {
    id = "fluid",
    read = function(item, s, x)
        local fc = item:getFluidContainer()
        if fc == nil then return nil end
        if fc:isEmpty() then
            s.q = 0
            return nil
        end
        if fc:isMixture() then return "fluid mixture" end
        local pf = fc:getPrimaryFluid()
        local ft = pf and pf:getFluidTypeString() or nil
        if type(ft) ~= "string" or ft == "" then return "fluid type" end
        if FluidType.FromNameLower(string.lower(ft)) == nil then return "fluid type " .. ft end
        s.q = fc:getAmount()
        s.ft = ft
        return nil
    end,
    write = function(item, s)
        if s.q == nil then return true end
        local fc = item:getFluidContainer()
        if fc == nil then return false end
        local want = num(s.q) or 0
        if fc:getAmount() > 0 then fc:adjustAmount(0) end
        if want > 0 then
            local ty = FluidType.FromNameLower(string.lower(tostring(s.ft)))
            if ty == nil then return false end
            fc:addFluid(ty, want)
        end
        return math.abs(fc:getAmount() - want) <= 0.01
    end,
}

-- Essen (NC CaptureFood / ApplyFood, NC:shared/BanditsNPC.lua:4266-4352, :4951-5040; f4/JAR_LISTE.md 2.1). Alter in TAGEN + Weltstunde at;
-- beim Bauen wird das Alter mit der Zeit im Rucksack hochgerechnet (B.InvAgeNow, kein Kuehlschrank).
-- BELEG getAge V:shared/Traps/TimedActions/ISAddBaitAction.lua:47; setAge(Zahl) V:shared/Definitions/animal/ButcheringUtil.lua:124;
-- BELEG getOffAge V:shared/Foraging/forageSystem.lua:2247; getOffAgeMax V:shared/Definitions/animal/ButcheringUtil.lua:124;
-- BELEG getHungChange V:client/ISUI/ISInventoryPane.lua:990; setHungChange(Zahl) V:client/ISUI/AdminPanel/ISItemEditPanel.lua:204;
-- BELEG getBaseHunger V:client/Farming/CFarming_Interact.lua:12; setBaseHunger(Zahl) V:server/Fishing/BuildingObjects/FishingNet.lua:137;
-- BELEG get/setCalories :127, get/setLipids :128, get/setCarbohydrates :129, get/setProteins :130 (V:server/Fishing/BuildingObjects/FishingNet.lua);
-- BELEG getPoisonPower/getPoisonDetectionLevel V:client/Foraging/ISForageIcon.lua:24-25; setPoisonPower/setPoisonDetectionLevel(Zahl) V:shared/Foraging/forageSystem.lua:2232-2233;
-- BELEG getHeat V:client/ISUI/ISInventoryPane.lua:2406; setHeat(Zahl) V:shared/TimedActions/ISAddItemInRecipe.lua:94;
-- BELEG getActualWeight V:client/Foraging/ISSearchManager.lua:474; getWeight NC-Regel; setActualWeight(Zahl)/setCustomWeight(true) V:server/Fishing/BuildingObjects/FishingNet.lua:145-146;
-- BELEG haveExtraItems V:server/Traps/ISUI/ISTrapMenu.lua:13; getExtraItems/getSpices V:shared/TimedActions/ISAddItemInRecipe.lua:105;
-- BELEG isCooked/isBurnt V:client/Farming/CFarming_Interact.lua:7; getCookingTime V:client/ISUI/ISInventoryPane.lua:2675;
-- BELEG isFrozen V:client/ISUI/ISInventoryPane.lua:2328; getFreezingTime :2693;
-- BELEG getUnhappyChange V:client/ISUI/ISInventoryPaneContextMenu.lua:2079; getThirstChange :2074; setUnhappyChange/setThirstChange(Zahl) B:shared/Bandit.lua:871/:868;
-- JAR A2 setCooked, setBurnt, setCookingTime, setOffAge, setOffAgeMax, setFreezingTime, setFrozen; JAR A4 addExtraItem, setSpices
-- (f4/JAR_LISTE.md 0; NC:shared/BanditsNPC.lua:4993-5036). ArrayList.new(): V:client/Challenge/AReallyCDDAy.lua:19.
-- Rest (benannt, BAU_KERN.md): Langeweile-Aenderung (getBoredomChange nur per Namens-Dispatch, NC fuehrt sie nicht), Fischgroesse am Boden
-- (setWorldScale nur beim Fang; das Gewicht reist), befruchtetes Ei (Merker nur Jar).
INV.F[#INV.F + 1] = {
    id = "food",
    read = function(item, s, x)
        if not x.food then return nil end
        s.rr = item:getOffAgeMax()
        s.rf = item:getOffAge()
        if num(s.rr) == nil or s.rr < INV.NEVER_ROTS then
            s.ag = item:getAge()
            s.at = B.Now()
        end
        s.h = item:getHungChange()
        s.bh = item:getBaseHunger()
        s.cal, s.lip, s.car, s.pro = item:getCalories(), item:getLipids(), item:getCarbohydrates(), item:getProteins()
        local pp = item:getPoisonPower()
        if pp ~= nil and pp > 0 then
            s.pp = pp
            s.pd = item:getPoisonDetectionLevel()
        end
        local ht = item:getHeat()
        if ht ~= nil and math.abs(ht - 1) > 0.001 then s.ht = ht end
        s.uh = item:getUnhappyChange()
        s.th = item:getThirstChange()
        if item:haveExtraItems() then
            local l = item:getExtraItems()
            local xi = {}
            for i = 0, l:size() - 1 do xi[#xi + 1] = tostring(l:get(i)) end
            if #xi > INV.XI_MAX then return "too many ingredients" end
            if #xi > 0 then
                if item.addExtraItem == nil then return "ingredients (method missing)" end
                if not INV.allKnown(xi) then return "ingredient of an unknown type" end        -- C9
                s.xi = xi
            end
        end
        local sl = item:getSpices()
        if sl ~= nil and sl:size() > 0 then
            local spc = {}
            for i = 0, sl:size() - 1 do spc[#spc + 1] = tostring(sl:get(i)) end
            if #spc > INV.XI_MAX then return "too many spices" end
            if item.setSpices == nil then return "spices (method missing)" end
            if not INV.allKnown(spc) then return "spice of an unknown type" end              -- C9
            s.spc = spc
        end
        -- Eigengewicht nur unangebissen, ohne Zutatenliste und abweichend (NC v3.10.13 / v3.12.33: sonst doppelt gewogen bzw. eingefroren)
        local aw, w = item:getActualWeight(), item:getWeight()
        local h, bh = num(s.h) or 0, num(s.bh) or 0
        if aw ~= nil and w ~= nil and math.abs(aw - w) > 0.001 and math.abs(h - bh) < 0.001 and s.xi == nil then s.aw = aw end
        s.ck = item:isCooked() and 1 or 0
        s.bu = item:isBurnt() and 1 or 0
        local ct = item:getCookingTime()
        if ct ~= nil and ct > 0 then s.ct = ct end
        if s.ck == 1 or s.bu == 1 then
            s.oa = item:getOffAge()
            s.om = item:getOffAgeMax()
        end
        local fzt = item:getFreezingTime()
        if fzt ~= nil and fzt > 0 then s.fzt = fzt end
        s.fz = item:isFrozen() and 1 or 0
        if (s.ck == 1 and item.setCooked == nil) or (s.bu == 1 and item.setBurnt == nil) or (s.ct ~= nil and item.setCookingTime == nil)
            or (s.oa ~= nil and (item.setOffAge == nil or item.setOffAgeMax == nil))
            or (s.fzt ~= nil and item.setFreezingTime == nil) or (s.fz == 1 and item.setFrozen == nil) then
            return "cooked/frozen state (method missing)"
        end
        -- Baerenfutter? Klasse beim Geben (nil = frisst er nicht, auch verdorben/verbrannt), Mahlzeiten je Stueck (F3: B.FoodClass, B.MealsOf)
        if B.FoodClass ~= nil then
            local cl, _ = B.FoodClass(item)
            s.fc = cl
        end
        if s.fc ~= nil and B.MealsOf ~= nil then s.ml = B.MealsOf(s.h) end
        return nil
    end,
    write = function(item, s)
        if s.h == nil then return true end
        local age, fz, fzt = B.InvAgeNow(s, B.Now())
        if s.ag ~= nil then item:setAge(age) end
        item:setBaseHunger(s.bh)
        item:setHungChange(s.h)
        item:setCalories(s.cal)
        item:setLipids(s.lip)
        item:setCarbohydrates(s.car)
        item:setProteins(s.pro)
        if s.pp ~= nil then
            item:setPoisonPower(s.pp)
            item:setPoisonDetectionLevel(s.pd or 0)
        end
        if s.ht ~= nil then item:setHeat(s.ht) end
        if s.aw ~= nil then
            item:setActualWeight(s.aw)
            item:setCustomWeight(true)
        end
        -- C9 (wie NC:shared/BanditsNPC.lua:4988-5005): nur bekannte Typen und nur auf ein frisches Stueck OHNE Liste; sonst wird das Stueck nicht
        -- gebaut (der Satz bleibt bzw. kommt beim Tod nach invLost) -- nie ein Gericht mit kaputter oder doppelter Liste.
        if type(s.xi) == "table" then
            if not INV.allKnown(s.xi) or item:haveExtraItems() then return false end
            for i = 1, #s.xi do item:addExtraItem(s.xi[i]) end                    -- JAR A4
        end
        if type(s.spc) == "table" then
            if not INV.allKnown(s.spc) then return false end
            local cur = item:getSpices()
            if cur ~= nil and cur:size() > 0 then return false end
            local l = ArrayList.new()
            for i = 1, #s.spc do l:add(s.spc[i]) end
            item:setSpices(l)                                                       -- JAR A4
        end
        if s.bu == 1 then item:setBurnt(true) end                                   -- JAR A2
        if s.ck == 1 then item:setCooked(true) end                                  -- JAR A2
        if s.ct ~= nil then item:setCookingTime(s.ct) end                           -- JAR A2
        if s.oa ~= nil then
            item:setOffAge(s.oa)                                                    -- JAR A2
            item:setOffAgeMax(s.om)                                                 -- JAR A2
        end
        if fzt ~= nil and fzt > 0 then
            if fz ~= 1 and fzt >= 100 then fzt = 99.9 end
            item:setFreezingTime(fzt)                                               -- JAR A2
        end
        if fz == 1 then item:setFrozen(true) end                                    -- JAR A2
        if s.uh ~= nil then item:setUnhappyChange(s.uh) end
        if s.th ~= nil then item:setThirstChange(s.th) end
        return true
    end,
}

-- Kleidung und Taschen: Naesse, Blut / Schmutz / Loecher je Koerperstelle; Flicken -> Ablehnung (NC braucht dafuer eine naehende Figur und
-- naehert die Schutzwerte, NC:shared/BanditsNPC.lua:4601-4648 -- nicht verlustfrei; Frage fuer Kevin).
-- BELEG getWetness V:client/ISUI/ISInventoryPaneContextMenu.lua:858; setWetness(Zahl) V:shared/TimedActions/ISClothingExtraAction.lua:90;
-- BELEG getBlood(Stelle) V:shared/TimedActions/ISWashClothing.lua:63; getDirt(Stelle) :84; setBlood(Stelle, Zahl) / setDirt(Stelle, Zahl) :136-137;
-- BELEG getVisual():getHole(Stelle) V:client/ISUI/ISGarmentUI.lua:78; setHole(Stelle) B:shared/BanditUtils.lua:199 (ItemVisual aus getItemVisuals, BloodBodyPartType; Nachbesserung F4 C10 -- ZASmack.lua:307 war die Waffe);
-- BELEG getPatchType(Stelle) V:client/ISUI/ISGarmentUI.lua:84; synchWithVisual V:shared/TimedActions/ISClothingExtraAction.lua:110.
INV.F[#INV.F + 1] = {
    id = "cloth",
    read = function(item, s, x)
        if not (x.cloth or x.bag) then return nil end
        if x.cloth then
            local w = item:getWetness()
            if w ~= nil and w > 0 then s.we = w end
        end
        local iv = item:getVisual()
        local list = INV.parts(item)
        local bp, dp, ho = nil, nil, nil
        for i = 1, #list do
            local p = list[i]
            local k = INV.partKey(p)
            local b = item:getBlood(p)
            if b ~= nil and b > 0 then
                bp = bp or {}
                bp[k] = b
            end
            if x.cloth then
                local d = item:getDirt(p)
                if d ~= nil and d > 0 then
                    dp = dp or {}
                    dp[k] = d
                end
                if item:getPatchType(p) ~= nil then return "patch" end
                if iv ~= nil and iv:getHole(p) > 0 then
                    ho = ho or {}
                    ho[k] = 1
                end
            end
        end
        s.bp, s.dp, s.ho = bp, dp, ho
        return nil
    end,
    write = function(item, s)
        if s.ho == nil and s.bp == nil and s.dp == nil and s.we == nil then return true end
        local iv = item:getVisual()
        if type(s.ho) == "table" then
            if iv == nil then return false end
            for k, _ in pairs(s.ho) do
                local p = INV.partOf(k)
                if p == nil then return false end
                iv:setHole(p)
            end
        end
        if type(s.bp) == "table" then
            for k, v in pairs(s.bp) do
                local p = INV.partOf(k)
                if p == nil then return false end
                item:setBlood(p, v)
            end
        end
        if type(s.dp) == "table" then
            for k, v in pairs(s.dp) do
                local p = INV.partOf(k)
                if p == nil then return false end
                item:setDirt(p, v)
            end
        end
        item:synchWithVisual()
        if s.we ~= nil then item:setWetness(s.we) end
        return true
    end,
}

-- Aussehen (ItemVisual): Grundtextur, Textur-Wahl, Aufdruck, Toenung (Vanillas eigene Kopie-Form mit dem ClothingItem), Farbton.
-- BELEG getVisual/getClothingItem/getTint(ClothingItem) + getRedFloat/getGreenFloat/getBlueFloat V:client/ISUI/ISInventoryPage.lua:1575-1577;
-- BELEG setTint(ImmutableColor.new(r, g, b, 1)) V:client/DebugUIs/Scenarios/FenrisScenario.lua:69;
-- BELEG getBaseTexture/getTextureChoice V:client/OptionScreens/CharacterCreationMain.lua:1489; setBaseTexture(Zahl) :983; setTextureChoice(Zahl)
-- V:client/DebugUIs/Scenarios/Trailer1Scenario.lua:113; getDecal(ClothingItem)/setDecal(Text) V:shared/TimedActions/ISClothingExtraAction.lua:73.
-- JAR A10 getHue(), setHue(Zahl) (f4/JAR_LISTE.md A10; NC:client/BanditsNPCInteract.lua:6181, :6247).
-- Eigene Farbe (NC fuehrt sie nicht, Lua-belegt, f4/GATES.md Nachtrag): BELEG isCustomColor V:client/ISUI/AdminPanel/ISItemEditPanel.lua:231;
-- getColorRed/Green/Blue V:client/ISUI/ISInventoryPaneContextMenu.lua:3371-3373; setColorRed/Green/Blue(Zahl) V:shared/TimedActions/ISTransferWaterAction.lua:26-28;
-- setCustomColor(true) V:client/ISUI/AdminPanel/ISItemEditPanel.lua:227.
-- x.probe (Grauen im Fenster, B.InvCanCarry): getTint(ClothingItem) schreibt an einem Stueck OHNE Zufallstoenung Weiss in dessen Feld (J:ItemVisual.getTint
-- Offset 68-76, f4/GATES.md) -- die Probe liest die Toenung deshalb nicht (sie kann ohnehin nicht ablehnen); gelesen wird nur beim Geben.
INV.F[#INV.F + 1] = {
    id = "look",
    read = function(item, s, x)
        if item:isCustomColor() then
            s.cc = { r = item:getColorRed(), g = item:getColorGreen(), b = item:getColorBlue() }
        end
        local iv = item:getVisual()
        if iv == nil then return nil end
        -- Nachbesserung F4 (Befund C4/C14): Kevins Jar-Wort fuer getHue/setHue (A10) gilt bei NPC Crew nur im Einzelspieler und auf dem MP-Client,
        -- NIE auf dem dedizierten Server (NPC Crew CLAUDE.md:444-447 "Server-Muenze ... braucht ein neues Wort"). Im Mehrspieler liest und baut der
        -- SERVER -> ein Stueck mit Aussehen (Farbton moeglich) wird dort mit Grund abgelehnt, bis Kevin "auch am Server" sagt (B.CFG.invHueMP).
        -- Damit laeuft im MP auch getTint(ClothingItem) nie am Server (C14: ungeladenes ClothingItem schriebe Weiss ins Feld). Der Client grauert
        -- gleich (dieselbe Regel, not B.IsSP()). Einzelspieler unveraendert.
        if not B.IsSP() and not (B.CFG and B.CFG.invHueMP == true) then return "look/hue in multiplayer (Kevin's word open)" end
        if iv.getHue == nil or iv.setHue == nil then return "hue (method missing)" end
        if x.probe then return nil end
        local v = {}
        local ci = item:getClothingItem()
        if ci ~= nil then
            local tint = iv:getTint(ci)
            if tint ~= nil then
                v.tr, v.tg, v.tb = tint:getRedFloat(), tint:getGreenFloat(), tint:getBlueFloat()
            end
            local dc = iv:getDecal(ci)
            if type(dc) == "string" and dc ~= "" then v.dc = dc end
        end
        local bt = iv:getBaseTexture()
        if type(bt) == "number" and bt >= 0 then v.bt = bt end
        local tc = iv:getTextureChoice()
        if type(tc) == "number" and tc >= 0 then v.tc = tc end
        local hue = iv:getHue()                                                     -- JAR A10
        if type(hue) == "number" and hue == hue and hue < math.huge then v.hue = hue end
        s.v = v
        return nil
    end,
    write = function(item, s)
        if type(s.cc) == "table" then
            item:setColorRed(s.cc.r)
            item:setColorGreen(s.cc.g)
            item:setColorBlue(s.cc.b)
            item:setCustomColor(true)
        end
        local v = s.v
        if type(v) ~= "table" then return true end
        -- C4: einen Farbton setzt im Mehrspieler nur, wer Kevins Wort hat (B.CFG.invHueMP); sonst baut der Server das Stueck NICHT (der Satz
        -- bleibt im Register bzw. kommt beim Tod nach invLost -- nie ohne seinen Farbton). Betrifft nur Saetze aus einem Einzelspieler-Stand.
        if v.hue ~= nil and not B.IsSP() and not (B.CFG and B.CFG.invHueMP == true) then return false end
        local iv = item:getVisual()
        if iv == nil then return false end
        if v.bt ~= nil then iv:setBaseTexture(v.bt) end
        if v.tc ~= nil then iv:setTextureChoice(v.tc) end
        if v.hue ~= nil then iv:setHue(v.hue) end                                   -- JAR A10
        if v.dc ~= nil then iv:setDecal(v.dc) end
        if v.tr ~= nil then iv:setTint(ImmutableColor.new(v.tr, v.tg, v.tb, 1)) end
        return true
    end,
}

-- Schluessel, Moebel, Wecker.
-- BELEG instanceof(item, "Key") V:client/ISUI/AdminPanel/ISItemEditPanel.lua:528; getKeyId V:shared/TimedActions/ISPadlockAction.lua:43 (keyToUse, ein Schluessel); setKeyId(Zahl)
-- V:shared/TimedActions/ISPadlockAction.lua:30 (Schluessel), V:client/DebugUIs/AdminContextMenu.lua:152 (instanceItem "Base.Key1") -- Nachbesserung F4 C10 (:128/:134 waren eine Tuer);
-- BELEG instanceof(item, "Moveable") + getWorldSprite V:client/ISUI/ISInventoryPaneContextMenu.lua (Moveable getWorldSprite); ReadFromWorldSprite(Text)
-- V:server/ClientCommands.lua:767; getActualWeight/setActualWeight wie Essen;
-- BELEG isAlarmSet/getHour/getMinute/setAlarmSet(bool)/setHour(Zahl)/setMinute(Zahl) V:shared/TimedActions/ISClothingExtraAction.lua:92-95.
-- Wecker in eigenen Funktionen: die Tier-Regel getHour (Kevin 13.11.: KEINE Uhrzeiten) erlaubt getHour nur in INV.alarmRead -- dort ist es die
-- WECKZEIT des Gegenstands, nie die Tageszeit (baer/tools/baer_uebernahme.py TIER_RULES).
function INV.alarmRead(item, s)
    s.al = { s = item:isAlarmSet() and 1 or 0, h = item:getHour(), m = item:getMinute() }
end

function INV.alarmWrite(item, s)
    item:setHour(s.al.h)
    item:setMinute(s.al.m)
    item:setAlarmSet(s.al.s == 1)
end

INV.F[#INV.F + 1] = {
    id = "misc",
    read = function(item, s, x)
        if x.key then s.kid = item:getKeyId() end
        if x.moveable then
            local ws = item:getWorldSprite()
            if type(ws) ~= "string" or ws == "" then return "furniture without sprite" end
            s.ws = ws
            s.aw = item:getActualWeight()
        end
        if x.alarm then INV.alarmRead(item, s) end
        return nil
    end,
    write = function(item, s)
        if s.kid ~= nil then item:setKeyId(s.kid) end
        if s.ws ~= nil then
            item:ReadFromWorldSprite(s.ws)
            if s.aw ~= nil then item:setActualWeight(s.aw) end
        end
        if type(s.al) == "table" then INV.alarmWrite(item, s) end
        return true
    end,
}

-- Eigener Name, ModData, Favorit (zuletzt -- ReadFromWorldSprite/Essen setzen Namen selbst).
-- BELEG getDisplayName V:client/ContextMenuCode.lua:69; getScriptItem():getDisplayName() V:shared/TimedActions/ISClothingExtraAction.lua:77 (getScriptItem);
-- BELEG isCustomName V:shared/TimedActions/ISAddItemInRecipe.lua:74; setName(Text) V:client/ServerCommands.lua:17; setCustomName(true) V:client/ISUI/ISInventoryPaneContextMenu.lua:2699;
-- BELEG hasModData/getModData/copyModData(Tabelle) V:shared/TimedActions/ISClothingExtraAction.lua:107-108;
-- BELEG isFavorite / setFavorite(bool) V:shared/TimedActions/ISClothingExtraAction.lua:106.
INV.F[#INV.F + 1] = {
    id = "tag",
    read = function(item, s, x)
        if not x.moveable then
            local dn = item:getDisplayName()
            local si = item:getScriptItem()
            local sd = si and si:getDisplayName() or nil
            if type(dn) == "string" and dn ~= "" and dn ~= sd then
                s.nm = dn
                s.cn = item:isCustomName() and 1 or 0
            end
        end
        if item:hasModData() then
            local md, ok, size = INV.copy(item:getModData(), 0)
            if not ok then return "item data (not storable)" end
            if size > cfg("invMdMax", 2048) then return "item data (too large)" end
            local any = false
            for _, _ in pairs(md) do
                any = true
                break
            end
            if any then s.md = md end
        end
        if item:isFavorite() then s.fv = true end
        return nil
    end,
    write = function(item, s)
        if type(s.nm) == "string" then
            item:setName(s.nm)
            if s.cn == 1 then item:setCustomName(true) end
        end
        if type(s.md) == "table" or item:hasModData() then
            local want = s.md or {}
            if type(s.md) == "table" then item:copyModData(s.md) end
            -- Schluessel, die das neue Stueck beim Bauen selbst bekam (OnCreate), das Original aber nicht hatte: weg (sonst ein Gratis-Wert)
            local live = item:getModData()
            local extra = {}
            for k, _ in pairs(live) do
                if want[k] == nil then extra[#extra + 1] = k end
            end
            for i = 1, #extra do live[extra[i]] = nil end
        end
        if s.fv then item:setFavorite(true) end
        return true
    end,
}

-- ---------------------------------------------------------------------------
-- Art-Merker eines Gegenstands (einmal je Lesen).
-- BELEG instanceof(item, "Food") V:client/Foraging/ISForageIcon.lua:23; "Clothing" V:client/ISUI/ISInventoryPaneContextMenu.lua (instanceof Clothing, 7 Stellen);
-- BELEG "InventoryContainer" + getInventory():getItems():isEmpty() V:server/BuildingObjects/ISBuildUtil.lua:111; "HandWeapon" V:client/ISUI/ISFirearmRadialMenu.lua
-- (instanceof HandWeapon); "Radio" V:client/ISUI/ISInventoryPaneContextMenu.lua (instanceof Radio); "AnimalInventoryItem" V:client/ISUI/Animal/ISAnimalContextMenu.lua:1081;
-- BELEG "AlarmClock" / "AlarmClockClothing" V:shared/TimedActions/ISClothingExtraAction.lua:91; IsMap V:client/ISUI/ISInventoryPane.lua:1107;
-- BELEG instanceof(item, "Literature") V:client/ISUI/ISInventoryPaneContextMenu.lua:329; getCustomPages V:client/ISUI/ISUIWriteJournal.lua:317; getLockedBy :56.
-- ---------------------------------------------------------------------------
function INV.kind(item)
    return {
        food = instanceof(item, "Food"),
        cloth = instanceof(item, "Clothing"),
        bag = instanceof(item, "InventoryContainer"),
        weapon = instanceof(item, "HandWeapon"),
        drain = instanceof(item, "Drainable"),
        key = instanceof(item, "Key"),
        moveable = instanceof(item, "Moveable"),
        alarm = instanceof(item, "AlarmClock") or instanceof(item, "AlarmClockClothing"),
        radio = instanceof(item, "Radio"),
        animal = instanceof(item, "AnimalInventoryItem"),
        lit = instanceof(item, "Literature"),
    }
end

-- ---------------------------------------------------------------------------
-- Gegenstand -> Satz. Rueckgabe: satz oder nil, whyKey, grund (Text fuer Log/Bericht). Liest nur (nimmt nichts, aendert nichts).
-- Stueckgewicht: BELEG getUnequippedWeight V:client/Hotbar/ISHotbar.lua:573. Typ: BELEG getFullType V:shared/Traps/TimedActions/ISAddBaitAction.lua:47.
-- ---------------------------------------------------------------------------
B.INV_LOSSY = "UI_BN_Bear_Why_InvLossy"
B.INV_BAGFIRST = "UI_BN_Bear_Why_InvBagFirst"

function B.InvRead(item, probe)
    if item == nil then return nil, B.INV_LOSSY, "no item" end
    local t = item:getFullType()
    if type(t) ~= "string" or t == "" then return nil, B.INV_LOSSY, "no type" end
    if INV.NEVER[t] then return nil, B.INV_LOSSY, INV.NEVER[t] end
    local x = INV.kind(item)
    x.probe = probe == true
    if x.animal then return nil, B.INV_LOSSY, "animal" end
    if x.radio then return nil, B.INV_LOSSY, "radio settings" end
    if item:IsMap() then return nil, B.INV_LOSSY, "map marks" end
    if x.lit then
        local pages = item:getCustomPages()
        if pages ~= nil and pages:size() > 0 then return nil, B.INV_LOSSY, "written pages" end
        if item:getLockedBy() ~= nil then return nil, B.INV_LOSSY, "locked journal" end
    end
    if x.bag and not item:getInventory():getItems():isEmpty() then return nil, B.INV_BAGFIRST, "bag not empty" end
    local s = { t = t, w = r4(item:getUnequippedWeight()) or 0 }
    for i = 1, #INV.F do
        local m = INV.F[i]
        local why = m.read(item, s, x)
        if why ~= nil then return nil, B.INV_LOSSY, m.id .. ": " .. tostring(why) end
    end
    return s, nil, nil
end

-- Verlustfrei tragbar? (Client: Grauen im Fenster; Schreiber: complete()). Rueckgabe: ok, whyKey.
function B.InvCanCarry(item)
    local s, whyKey, _ = B.InvRead(item, true)
    if s == nil then return false, whyKey end
    return true, nil
end

-- Satz -> neuer Gegenstand (nur Schreiber; liegt danach in KEINEM Behaelter). Rueckgabe: item oder nil, grund ("unknown" = Typ fehlt).
-- instanceItem(Text): V:server/Fishing/BuildingObjects/FishingNet.lua:125. Alle Felder VOR AddItem / AddWorldInventoryItem (der Schreiber sendet
-- den fertigen Zustand, PLAN_F4.md 5 "Reihenfolge beim Bauen").
function B.InvBuild(s)
    if type(s) ~= "table" or type(s.t) ~= "string" then return nil, "bad record" end
    local item = instanceItem(s.t)
    if item == nil then return nil, "unknown" end
    for i = 1, #INV.F do
        local m = INV.F[i]
        if not m.write(item, s) then return nil, "field " .. m.id end
    end
    return item, nil
end

-- ---------------------------------------------------------------------------
-- Stapel: gleicher Typ UND alle Felder gleich UND kein md / nm / fv (PLAN_F4.md 4.1). Weltstunde at zaehlt nur ueber das Alter (zwei Fische,
-- die gleich alt SIND, stapeln nicht, weil at verschieden ist -- ehrlich, aber selten gleich; Dosen ohne Alter stapeln).
-- ---------------------------------------------------------------------------
function B.InvSame(a, b)
    if type(a) ~= "table" or type(b) ~= "table" then return false end
    if a.md ~= nil or b.md ~= nil or a.nm ~= nil or b.nm ~= nil or a.fv or b.fv then return false end
    for k, v in pairs(a) do
        if k ~= "k" and not INV.same(v, b[k]) then return false end
    end
    for k, _ in pairs(b) do
        if k ~= "k" and a[k] == nil then return false end
    end
    return true
end

-- ---------------------------------------------------------------------------
-- Traglast (PLAN_F4.md 3; Kevin Antwort 4 + 5 und die Aenderung waehrend des Laufs): carry (Groesse, B.StatsOf) x BearCarryPercent / 100, Packtaschen
-- +bagAdd (150 kg, NICHT mit dem Regler multipliziert) ab halbstark -- ausgewachsen 100 + 150 = 250 kg, hoechstens 250 + 150 = 400.
-- Rein: carry, pct, bagOn (Taschen an), half (Stufe >= halbstark).
-- ---------------------------------------------------------------------------
function B.InvCapOf(carry, pct, bagOn, half)
    local c = (num(carry) or 0) * (num(pct) or 100) / 100
    if bagOn and half then c = c + cfg("bagAdd", 150) end
    if c < 0 then c = 0 end
    return c
end

-- Last und Stueckzahl eines Inventars (rec.inv). Rueckgabe: kg, stueck, saetze.
function B.InvSum(inv)
    local kg, n, recs = 0, 0, 0
    if type(inv) ~= "table" or type(inv.it) ~= "table" then return 0, 0, 0 end
    for _, s in pairs(inv.it) do
        if type(s) == "table" then
            local k = math.floor(num(s.k) or 0)
            kg = kg + (num(s.w) or 0) * k
            n = n + k
            recs = recs + 1
        end
    end
    return kg, n, recs
end

-- ---------------------------------------------------------------------------
-- Verderben unterwegs (NC ProjectedAge, NC:shared/BanditsNPC.lua:4365-4395; Food.updateAge laut PLAN_F4.md 5): Alter + Stunden / 24 x Tempo,
-- Gefrorenes taut zuerst (100 % in 1,5 Stunden), nie rueckwaerts. Tempo je Sandbox-Stufe FoodRotSpeed 1..5, gelesen wie Vanilla
-- getSandboxOptions():getOptionByName(Text):getValue() (V:shared/TimedActions/ISReadABook.lua:488; SandboxVars liest im Baeren nur B.Opt),
-- Faktoren {1.7, 1.4, 1.0, 0.7, 0.4} aus Food.getFoodRotSpeed (Pruef-Tor G3, f4/GATES.md: tableswitch Offset 44-68) in B.CFG.invRotK.
-- Rueckgabe: alter (Tage), fz (1/0), fzt.
-- ---------------------------------------------------------------------------
function B.InvRotK()
    local list = B.CFG and B.CFG.invRotK
    local opt = getSandboxOptions():getOptionByName("FoodRotSpeed")
    local lv = opt and num(opt:getValue()) or 3
    local k = type(list) == "table" and num(list[math.floor(lv)]) or nil
    if k == nil then k = 1 end
    return k
end

function B.InvAgeNow(s, nowH)
    local g = num(s and s.ag) or 0
    local fzt = num(s and s.fzt) or 0
    local fz = 0
    if s and s.fz == 1 and fzt > 0 then fz = 1 end
    local at = num(s and s.at)
    nowH = num(nowH)
    if at == nil or nowH == nil or nowH <= at then return g, fz, fzt end
    local elapsed = nowH - at
    if fz == 1 then
        local thawH = fzt / 100 * 1.5
        if elapsed < thawH then
            fzt = fzt - elapsed / 1.5 * 100
            elapsed = 0
        else
            elapsed = elapsed - thawH
            fzt = 0
            fz = 0
        end
    elseif fzt > 0 then
        fzt = math.max(0, fzt - elapsed / 1.5 * 100)
    end
    return g + elapsed / 24 * B.InvRotK(), fz, fzt
end

-- Frische JETZT: 0 frisch, 1 alt, 2 verdorben, nil (verdirbt nie / kein Essen).
function B.InvFresh(s, nowH)
    if type(s) ~= "table" or s.h == nil or s.ag == nil then return nil end
    local age, _, _ = B.InvAgeNow(s, nowH)
    local rr = num(s.om) or num(s.rr)
    local rf = num(s.oa) or num(s.rf)
    if rr ~= nil and rr < INV.NEVER_ROTS and age >= rr then return 2 end
    if rf ~= nil and age >= rf then return 1 end
    return 0
end

-- ---------------------------------------------------------------------------
-- Zeile fuer das Fenster (schnittstelle.md K4): nur Anzeige, nie zurueckgeschickt. nm hoechstens 100 Zeichen (die Daten behalten den ganzen Namen).
-- ---------------------------------------------------------------------------
function B.InvRow(nr, s, nowH, typeOk)
    local row = { nr = nr, t = s.t, k = math.floor(num(s.k) or 1), w = math.floor((num(s.w) or 0) * 100 + 0.5) / 100 }
    if type(s.nm) == "string" then row.nm = string.sub(s.nm, 1, 100) end
    if s.c ~= nil then
        local cm = num(s.cm)
        if cm ~= nil and cm > 0 then row.cp = math.floor((num(s.c) or 0) / cm * 100 + 0.5) end
    end
    if s.fv then row.fv = true end
    local fr = B.InvFresh(s, nowH)
    if fr ~= nil then row.fr = fr end
    if s.ck == 1 then row.ck = true end
    if s.bu == 1 then row.bu = true end
    if s.fz == 1 then
        local _, fz, _ = B.InvAgeNow(s, nowH)
        if fz == 1 then row.fz = true end
    end
    if num(s.q) ~= nil and s.q > 0 then
        row.fl = math.floor(s.q * 100 + 0.5) / 100
        row.fn = s.ft
    end
    if num(s.u) ~= nil then row.u = math.floor(s.u * 100 + 0.5) end
    if typeOk == false then row.unk = true end
    if s.fc ~= nil then row.ea = true end
    return row
end

B.InvInternal = INV                 -- nur fuer die Attrappen (attrappe/f4_kern) und den Feldpruefer; kein Spielcode liest es
