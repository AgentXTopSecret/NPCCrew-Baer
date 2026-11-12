--
-- NPC Crew -- Baer, Zeitaktion "Baeren aufhelfen" (F2 = B5a, PLAN_F2.md 0.10, 2.4, 2.5 Nr. 5; Kevin 08.11.2026 ENT:42: "Aufhelfen per
-- Rechtsklick (5 s, 45 % Leben)").
--
-- Gleiche Form wie die Verband-Aktion (shared/TimedActions/BanditsNPCBearMendAction.lua) und die gespielte Fuetter-Aktion. Liegt in shared/,
-- weil im Mehrspieler der Server die Klasse braucht (er baut die Aktion neu und ruft complete()). complete() ist eine Zeile und ruft den
-- Schreiber-Kern (B.HelpUpComplete, server/BanditsNPCBearHurt.lua, KERN): dort stehen alle Pruefungen (eigener, gezaehmter, geladener
-- Baer am Boden in Reichweite, sonst Why_NotOwner / Why_NotDown) und dort steht er auf. Diese Datei setzt nichts selbst; kein Gegenstand.
-- Kein Halt am Baeren: am Boden haelt ihn der Kern (B.DownStep / B.Hold).
-- Beschaeftigt-Marke (B.BodyBusy, nur beim Schreiber) wie beim Verbinden: SP start(), MP-Server serverStart(); weg in stop() / serverStop() /
-- complete().
-- Engine-Aufrufe (Fundstelle): wie die Verband-Aktion; Bild self:setActionAnim("Loot") + character:SetVariable("LootPosition", "Low")
-- V:shared/Camping/TimedActions/ISAddFuelAction.lua:41-42 (bodennah -- der Baer liegt/sitzt am Boden). Kein Ton. Dauer B.CFG.helpTime 250
-- (~5 s; im Spiel nachmessen, PLAN_F2.md 9).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearHelpAction = ISBaseTimedAction:derive("BanditsNPCBearHelpAction")

-- Nur Client und Einzelspieler, billig. Form: V:shared/TimedActions/Animals/ISPetAnimal.lua:5-7 (Abstand unter 3), ISAnimalUI.lua:15
-- (isExistInTheWorld), ISHutchUI.lua:427 (isDead).
function BanditsNPCBearHelpAction:isValid()
    local a = self.animal
    if not a then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    return here:DistTo(there) < 3
end

-- Erst zum Tier drehen: ISPetAnimal.lua:9-12.
function BanditsNPCBearHelpAction:waitToStart()
    self.character:faceThisObject(self.animal)
    return self.character:shouldBeTurning()
end

function BanditsNPCBearHelpAction:update()
    self.character:faceThisObject(self.animal)
end

function BanditsNPCBearHelpAction:start()
    self:setActionAnim("Loot")                                      -- ISAddFuelAction.lua:41
    self.character:SetVariable("LootPosition", "Low")               -- :42
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearHelpAction:forceStop()
    ISBaseTimedAction.forceStop(self)
end

function BanditsNPCBearHelpAction:stop()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end          -- im MP-Client fehlt die Funktion (nur Schreiber)
    ISBaseTimedAction.stop(self)
end

function BanditsNPCBearHelpAction:perform()
    ISBaseTimedAction.perform(self)                                 -- noetig, damit die Warteschlange weiterlaeuft
end

function BanditsNPCBearHelpAction:serverStart()
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearHelpAction:serverStop()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearHelpAction:complete()
    local f = BanditsNPC.Bear.HelpUpComplete
    local ok = false
    if f then ok = f(self.character, self.animal) end
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

-- Dauer: isTimedActionInstant wie V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:54.
function BanditsNPCBearHelpAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.helpTime) or 250
end

function BanditsNPCBearHelpAction:new(character, animal)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
