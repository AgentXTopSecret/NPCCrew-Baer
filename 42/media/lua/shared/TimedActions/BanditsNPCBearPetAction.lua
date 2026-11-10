--
-- NPC Crew -- Baer, Zeitaktion "Junges streicheln" (B1a, PLAN_ZAEHMEN.md 5.4 und 6.2.7).
--
-- Liegt in shared/, weil im Mehrspieler auch der Server die Klasse braucht (serverStart, serverStop, complete). Das Bild spielt der
-- Client bzw. der Einzelspieler, die Sperre am Tier im Mehrspieler der Server (serverStart). complete() ist eine Zeile und ruft den Schreiber-Kern (B.PetComplete): dort stehen
-- alle Pruefungen (zu scheu, fremd gebunden, Besitzer, Abklingzeit), die Gutschrift und Vanillas petAnimal.
--
-- Anders als Vanillas Streicheln (shared/TimedActions/Animals/ISPetAnimal.lua): feste Dauer, KEIN Anim-Ereignis -- gewertet wird
-- genau einmal in complete(). Die Groesse fuer die Haltung der Figur ist FEST (Vanilla teilt durch maxSize - minSize, das ist beim
-- Jungen 0). Welche Haltung die Figur einnimmt, sagt der Stellwert B.CFG.petAnim (Vorgabe "lamb" = Knoten petlamb der Figur;
-- "loot" = einfach buecken).
-- Die Klasse ist global und new() nennt seine Parameter wie die Felder (Engine-Pflicht fuer Netz-Aktionen, ISPetAnimal.lua:3, :95-102).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearPetAction = ISBaseTimedAction:derive("BanditsNPCBearPetAction")

-- Nur Client und Einzelspieler, billig. Abstand: ISPetAnimal.lua:5-7; da und lebendig: ISAnimalUI.lua:15, ISHutchUI.lua:427.
function BanditsNPCBearPetAction:isValid()
    local a = self.animal
    if not a then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    return here:DistTo(there) < 3
end

-- ISPetAnimal.lua:9-12
function BanditsNPCBearPetAction:waitToStart()
    self.character:faceThisObject(self.animal)
    return self.character:shouldBeTurning()
end

-- ISPetAnimal.lua:14-18
function BanditsNPCBearPetAction:update()
    self.character:setIsAiming(false)
    self.character:faceThisObject(self.animal)
    self.animal:faceThisObject(self.character)
end

function BanditsNPCBearPetAction:start()
    local cfg = B.CFG
    local pose = (cfg and cfg.petAnim) or "lamb"
    self:setOverrideHandModels(nil, nil)                            -- ISPetAnimal.lua:25
    if pose == "loot" then
        -- Rueckfall: buecken wie beim Nachlegen am Lagerfeuer, shared/Camping/TimedActions/ISAddFuelAction.lua:41-42
        self:setActionAnim("Loot")
        self.character:SetVariable("LootPosition", "Low")
    else
        self.character:setVariable("AnimalSizeX", 0.01)             -- ISPetAnimal.lua:26
        self.character:setVariable("AnimalSizeY", 0.5)              -- :32 (dort gerechnet, hier fest)
        self.character:setVariable("petanimal", true)               -- :37
        self.character:setVariable("animal", pose)                  -- :39 und :41 (Text)
        self.petPose = true
    end
    self.animal:getBehavior():setBlockMovement(true)                -- :36
end

-- Jeder Ausgang: Haltung beenden, Sperre loesen (ISPetAnimal.lua:46-67).
function BanditsNPCBearPetAction:release()
    if self.petPose then
        self.character:setVariable("petanimal", false)              -- :47
        self.petPose = nil
    end
    local a = self.animal
    if a then
        a:getBehavior():setBlockMovement(false)                     -- :49
    end
end

function BanditsNPCBearPetAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)
end

function BanditsNPCBearPetAction:stop()
    self:release()
    ISBaseTimedAction.stop(self)                                    -- :57
end

function BanditsNPCBearPetAction:perform()
    self:release()
    -- noetig, damit die Warteschlange weiterlaeuft: ISPetAnimal.lua:65-66
    ISBaseTimedAction.perform(self)
end

-- Einzelspieler und Server. Pruefen, gutschreiben und Vanillas petAnimal macht der Kern in EINEM Aufruf.
-- Im Mehrspieler haelt NUR die Sperre des Servers das Tier: serverStart setzt sie, serverStop (Abbruch) und complete() loesen sie
-- -- Form Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:212 (serverStart), :169 (serverStop), :196 (complete).
-- Nachbesserung A2. Der Client setzt seine eigene Kopie in start() (nur Bild).
function BanditsNPCBearPetAction:serverStart()
    self.animal:getBehavior():setBlockMovement(true)
end

function BanditsNPCBearPetAction:serverStop()
    self.animal:getBehavior():setBlockMovement(false)
end

function BanditsNPCBearPetAction:complete()
    local f = BanditsNPC.Bear.PetComplete
    local ok = false
    if f then ok = f(self.character, self.animal) end
    if self.animal then self.animal:getBehavior():setBlockMovement(false) end      -- ISMilkAnimal.lua:196
    return ok
end

-- Feste Dauer (Stellwert); die Sofort-Frage wie ISFeedAnimalFromHand.lua:53-58.
function BanditsNPCBearPetAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.petTime) or 150
end

function BanditsNPCBearPetAction:new(character, animal)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    o.stopOnAim = false                                             -- ISPetAnimal.lua:100
    return o
end
