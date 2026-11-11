--
-- NPC Crew -- Baer, Zeitaktion "Junges aus der Hand fuettern" (B1a, PLAN_ZAEHMEN.md 5.3 und 6.2.7).
--
-- Liegt in shared/, weil im Mehrspieler auch der Server die Klasse braucht: er baut die Aktion aus den uebertragenen Werten neu
-- (Spieler, Tier, Gegenstand) und ruft serverStart(), bei Abbruch serverStop(), am Ende complete(). Bild und Ton spielt der
-- Client bzw. der Einzelspieler; die Sperre am Tier setzt im Mehrspieler der Server (serverStart).
-- complete() ist eine Zeile und ruft den Schreiber-Kern (B.FeedComplete, server/BanditsNPCBearServer.lua): dort stehen ALLE
-- Pruefungen, dort wird genau ein Stueck genommen und gutgeschrieben. Diese Datei nimmt nichts und schreibt nichts gut.
-- Einzelspieler: complete() laeuft im selben Programm nach perform(). Auf einem MP-Client gibt es B.FeedComplete nicht (nil),
-- dort wird complete() auch nie gerufen.
--
-- B1e (PLAN_B1E.md 0.7, 6.3): Beschaeftigt-Marke -- der Schreiber tauscht den Koerper nicht, solange gefuettert wird (B.BodyBusy,
-- server/BanditsNPCBearGrow.lua; SP in start(), MP-Server in serverStart(); geloescht in complete()/stop()/serverStop(), Deckel busyMs).
-- Die Klasse ist eine GLOBALE Variable mit dem Namen ihres Typs und new() nennt seine Parameter wie die Felder: beides verlangt
-- die Engine fuer Netz-Aktionen (Form Vanilla shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3 und :66-74).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearFeedAction = ISBaseTimedAction:derive("BanditsNPCBearFeedAction")

-- Nur Client und Einzelspieler, billig (der Server fragt isValid nie). Form: ISFeedAnimalFromHand.lua:5-7 (contains),
-- ISPetAnimal.lua:5-7 (Abstand unter 3), ISAnimalUI.lua:15 (isExistInTheWorld), ISHutchUI.lua:427 (isDead).
function BanditsNPCBearFeedAction:isValid()
    local a = self.animal
    if not a or not self.food then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    if here:DistTo(there) >= 3 then return false end
    return self.character:getInventory():contains(self.food)
end

-- Erst zum Tier drehen: ISPetAnimal.lua:9-12.
function BanditsNPCBearFeedAction:waitToStart()
    self.character:faceThisObject(self.animal)
    return self.character:shouldBeTurning()
end

-- Figur und Junges sehen sich an: ISPetAnimal.lua:16-17.
function BanditsNPCBearFeedAction:update()
    self.character:faceThisObject(self.animal)
    self.animal:faceThisObject(self.character)
end

function BanditsNPCBearFeedAction:start()
    local a = self.animal
    if a:isExistInTheWorld() then                           -- ISFeedAnimalFromHand.lua:14
        self:setActionAnim(a:getFeedByHandAnim())           -- :15 (Junges "AnimalLureLow", gross "AnimalLureHigh": Defs.lua)
        self:setOverrideHandModels(self.food, nil)          -- :16
        self.character:faceThisObject(a)                    -- :17
    end
    a:getBehavior():setBlockMovement(true)                  -- :19
    -- Fress-Clip des Jungen ueber die Text-Variable des Animsets (B.ACT; der Knoten "Eat" liegt unter AnimSets/buck/idle).
    -- setVariable(Name, Text) an einem Tier: ISPetAnimal.lua:43. Im Mehrspieler nur an der Kopie dieses Clients sichtbar.
    if B.ACT then a:setVariable(B.ACT, "eat") end
    self.sound = self.character:playSound("GiveFoodAnimal") -- :23
    -- B1e: Beschaeftigt-Marke beim Schreiber, nur im Einzelspieler (im Mehrspieler setzt sie serverStart am Server)
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(a, true) end
end

-- Jeder Ausgang loest die Sperre, loescht die Variable und stoppt den Ton.
function BanditsNPCBearFeedAction:release()
    local a = self.animal
    if a then
        a:getBehavior():setBlockMovement(false)             -- ISFeedAnimalFromHand.lua:28
        if B.ACT then a:clearVariable(B.ACT) end            -- ISPetAnimal.lua:48
    end
    -- Ton: ISFeedAnimalFromHand.lua:60-64
    if self.sound and self.character:getEmitter():isPlaying(self.sound) then
        self.character:getEmitter():stopOrTriggerSound(self.sound)
    end
    self.sound = nil
end

function BanditsNPCBearFeedAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)                       -- ISFeedAnimalFromHand.lua:29
end

function BanditsNPCBearFeedAction:stop()
    self:release()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end  -- B1e: im MP-Client fehlt die Funktion (nur Schreiber)
    ISBaseTimedAction.stop(self)                            -- :35
end

function BanditsNPCBearFeedAction:perform()
    self:release()
    -- noetig, damit die Warteschlange weiterlaeuft: ISFeedAnimalFromHand.lua:41-42
    ISBaseTimedAction.perform(self)
end

-- Einzelspieler und Server. Alle Pruefungen, das Nehmen des einen Stuecks und die Gutschrift macht der Kern in EINEM Aufruf.
-- Im Mehrspieler haelt NUR die Sperre des Servers das Tier: serverStart setzt sie, serverStop (Abbruch) und complete() loesen sie
-- -- Form Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:212 (serverStart), :169 (serverStop), :196 (complete).
-- Nachbesserung A2. Der Client setzt seine eigene Kopie in start() (nur Bild).
-- B1e: Beschaeftigt-Marke (B.BodyBusy, nur beim Schreiber vorhanden) in serverStart setzen, in serverStop / complete loeschen.
function BanditsNPCBearFeedAction:serverStart()
    self.animal:getBehavior():setBlockMovement(true)
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearFeedAction:serverStop()
    self.animal:getBehavior():setBlockMovement(false)
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearFeedAction:complete()
    local f = BanditsNPC.Bear.FeedComplete
    local ok = false
    if f then ok = f(self.character, self.animal, self.food) end
    if self.animal then self.animal:getBehavior():setBlockMovement(false) end      -- ISMilkAnimal.lua:196
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

-- Dauer wie Vanillas Fuettern: ISFeedAnimalFromHand.lua:53-58.
function BanditsNPCBearFeedAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.feedTime) or 150
end

function BanditsNPCBearFeedAction:new(character, animal, food)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.food = food
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
