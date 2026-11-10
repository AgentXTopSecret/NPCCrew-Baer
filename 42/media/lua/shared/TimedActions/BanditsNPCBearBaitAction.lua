--
-- NPC Crew -- Baer, Zeitaktion "Baeren-Koeder auslegen" (B1a, PLAN_ZAEHMEN.md 5.2 und 6.2.7).
--
-- Liegt in shared/, weil im Mehrspieler auch der Server die Klasse braucht (er ruft NUR complete()). complete() ist eine Zeile und
-- ruft den Schreiber-Kern (B.BaitComplete): dort stehen alle Pruefungen (Wald, draussen, Plaetze, Abstand, Stueck noch da und
-- Honig oder Fisch), dort wird das EINE Stueck genommen und der Koederplatz im selben Aufruf eingetragen. Lehnt der Kern ab, ist
-- nichts verbraucht. Der Koederplatz ist unsichtbar: es entsteht kein Bodengegenstand.
-- x, y, z sind die Kachel des Koederplatzes (ganze Zahlen). Die Klasse ist global und new() nennt seine Parameter wie die Felder
-- (Engine-Pflicht fuer Netz-Aktionen; Form Vanilla shared/Camping/TimedActions/ISAddFuelAction.lua:3 und :84-94).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearBaitAction = ISBaseTimedAction:derive("BanditsNPCBearBaitAction")

-- Nur Client und Einzelspieler, billig: das Stueck ist noch im Inventar (Form ISFeedAnimalFromHand.lua:5-7).
function BanditsNPCBearBaitAction:isValid()
    if not self.food then return false end
    return self.character:getInventory():contains(self.food)
end

-- Buecken wie beim Nachlegen am Lagerfeuer: ISAddFuelAction.lua:41-43.
function BanditsNPCBearBaitAction:start()
    self:setActionAnim("Loot")
    self.character:SetVariable("LootPosition", "Low")
    self.character:reportEvent("EventLootItem")
end

function BanditsNPCBearBaitAction:stop()
    ISBaseTimedAction.stop(self)                                    -- ISAddFuelAction.lua:50
end

function BanditsNPCBearBaitAction:perform()
    -- noetig, damit die Warteschlange weiterlaeuft: ISAddFuelAction.lua:58-59
    ISBaseTimedAction.perform(self)
end

-- Einzelspieler und Server. Pruefen, das eine Stueck nehmen und den Platz eintragen macht der Kern in EINEM Aufruf.
function BanditsNPCBearBaitAction:complete()
    local f = BanditsNPC.Bear.BaitComplete
    if not f then return false end
    return f(self.character, self.food, self.x, self.y, self.z)
end

-- Dauer: ISAddFuelAction.lua:77-82 (dort 100).
function BanditsNPCBearBaitAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.baitTime) or 100
end

function BanditsNPCBearBaitAction:new(character, food, x, y, z)
    local o = ISBaseTimedAction.new(self, character)
    o.food = food
    o.x = x
    o.y = y
    o.z = z
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
