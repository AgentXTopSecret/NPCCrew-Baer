--
-- NPC Crew -- Baer, Zeitaktion "Dem Baeren Wasser geben" (F3, Lauf baer-f3, PLAN_F3.md 5.2; Kevin ENT:14-19 "Wasser 1 / 2 / 3 Schalen").
--
-- Form der Fuetter-Aktion (shared/TimedActions/BanditsNPCBearFeedAction.lua) mit Vanillas Wasser-Behaelter statt Futter (Vorbild
-- V:shared/TimedActions/Animals/ISGiveWaterToAnimal.lua). Liegt in shared/, weil im Mehrspieler auch der Server die Klasse braucht: er baut
-- die Aktion aus den uebertragenen Werten neu (Spieler, Tier, Gegenstand) und ruft serverStart(), bei Abbruch serverStop(), am Ende
-- complete(). Bild und Ton spielt der Client bzw. der Einzelspieler; die Sperre am Tier setzt im Mehrspieler der Server (serverStart).
-- complete() ist eine Zeile und ruft den Schreiber-Kern (B.DrinkComplete, server/BanditsNPCBearNeeds.lua): dort stehen ALLE Pruefungen
-- (Besitzer, gezaehmt, nicht mitfahrend / am Boden, Behaelter im Inventar, durstig), dort wird das Wasser in EINEM Aufruf genommen und der
-- Durst gesenkt; eine Ablehnung nimmt nichts (rote Linie: kein Gegenstand verloren). Diese Datei nimmt kein Wasser und schreibt nichts gut.
-- Einzelspieler: complete() laeuft im selben Programm nach perform(). Auf einem MP-Client gibt es B.DrinkComplete nicht (nil), dort wird
-- complete() auch nie gerufen.
-- Schlaeft der Baer, hat das Menue vorher um sanftes Wecken gebeten (Bitte "Wake", client/BanditsNPCBearMenu.lua); waitToStart wartet
-- hoechstens 5 s darauf (U.WakeWait, nur Client / Einzelspieler). Kommt die Bitte nie an, weckt der Schreiber in complete() selbst
-- (f3/schnittstelle.md K3) -- nichts haengt.
-- Die Klasse ist eine GLOBALE Variable mit dem Namen ihres Typs und new() nennt seine Parameter wie die Felder: beides verlangt die
-- Engine fuer Netz-Aktionen (Form V:shared/TimedActions/Animals/ISGiveWaterToAnimal.lua:3 und :124-133).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearDrinkAction = ISBaseTimedAction:derive("BanditsNPCBearDrinkAction")

-- Nur Client und Einzelspieler, billig (der Server fragt isValid nie). Abstand und Tier wie die Fuetter-Aktion (ISPetAnimal.lua:5-7,
-- ISAnimalUI.lua:15, ISHutchUI.lua:427); Behaelter im Inventar und nicht leer: ISGiveWaterToAnimal.lua:6 (contains, getFluidContainer():isEmpty()).
function BanditsNPCBearDrinkAction:isValid()
    local a = self.animal
    if not a or not self.item then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    if here:DistTo(there) >= 3 then return false end
    if not self.character:getInventory():contains(self.item) then return false end
    local fc = self.item:getFluidContainer()
    return fc ~= nil and not fc:isEmpty()
end

-- Erst zum Tier drehen (ISGiveWaterToAnimal.lua:9-17); dann -- nur wenn er laut Sicht schlief -- kurz auf das Aufwachen warten.
function BanditsNPCBearDrinkAction:waitToStart()
    self.character:faceThisObject(self.animal)
    if self.character:shouldBeTurning() then return true end
    local ui = B.UI
    return ui ~= nil and ui.WakeWait ~= nil and ui.WakeWait(self) == true
end

-- Figur und Baer sehen sich an: ISPetAnimal.lua:16-17.
function BanditsNPCBearDrinkAction:update()
    self.character:faceThisObject(self.animal)
    self.animal:faceThisObject(self.character)
end

function BanditsNPCBearDrinkAction:start()
    local a = self.animal
    if a:isExistInTheWorld() then                               -- ISGiveWaterToAnimal.lua:48
        self:setActionAnim(a:getFeedByHandAnim())               -- :49
        self.character:faceThisObject(a)                        -- :50
        self:setOverrideHandModels(self.item:getStaticModel(), nil)     -- :51 (Text, nil)
    end
    a:getBehavior():setBlockMovement(true)                      -- :46
    -- Der Baer zeigt seinen Fress-Clip (Knoten "Eat" unter AnimSets/buck/idle, wie beim Fuettern). setVariable(Name, Text) an einem
    -- Tier: ISPetAnimal.lua:43. Im Mehrspieler nur an der Kopie dieses Clients sichtbar.
    if B.ACT then a:setVariable(B.ACT, "eat") end
    -- Der Ruhe-Treiber dieses Clients schreibt waehrenddessen nichts (client/BanditsNPCBearPose.lua; B.UI gibt es nur auf einem Client
    -- bzw. im Einzelspieler)
    if B.UI and B.UI.PoseHands then B.UI.PoseHands(a, true) end
    self.sound = self.character:playSound("GiveWaterAnimal")    -- :53
    -- Beschaeftigt-Marke beim Schreiber, nur im Einzelspieler (im Mehrspieler setzt sie serverStart am Server)
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(a, true) end
end

-- Jeder Ausgang loest die Sperre, loescht die Variable und stoppt den Ton.
function BanditsNPCBearDrinkAction:release()
    local a = self.animal
    if a then
        a:getBehavior():setBlockMovement(false)                 -- ISGiveWaterToAnimal.lua:57
        if B.ACT then a:clearVariable(B.ACT) end                -- ISPetAnimal.lua:48
        if B.UI and B.UI.PoseHands then B.UI.PoseHands(a, false) end    -- B.ACT ist weg, der Ruhe-Treiber setzt neu an
    end
    -- Ton: ISGiveWaterToAnimal.lua:118-122
    if self.sound and self.character:getEmitter():isPlaying(self.sound) then
        self.character:getEmitter():stopOrTriggerSound(self.sound)
    end
    self.sound = nil
end

function BanditsNPCBearDrinkAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)                           -- ISFeedAnimalFromHand.lua:29
end

function BanditsNPCBearDrinkAction:stop()
    self:release()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end       -- im MP-Client fehlt die Funktion (nur Schreiber)
    ISBaseTimedAction.stop(self)                                -- ISGiveWaterToAnimal.lua:64
end

function BanditsNPCBearDrinkAction:perform()
    self:release()
    -- noetig, damit die Warteschlange weiterlaeuft: ISGiveWaterToAnimal.lua:71-72
    ISBaseTimedAction.perform(self)
end

-- Einzelspieler und Server. Alle Pruefungen, das Nehmen des Wassers und das Senken des Dursts macht der Kern in EINEM Aufruf.
-- Im Mehrspieler haelt NUR die Sperre des Servers das Tier: serverStart setzt sie, serverStop (Abbruch) und complete() loesen sie --
-- wie die Fuetter-Aktion (Form V:shared/TimedActions/Animals/ISMilkAnimal.lua:212, :169, :196).
function BanditsNPCBearDrinkAction:serverStart()
    self.animal:getBehavior():setBlockMovement(true)
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearDrinkAction:serverStop()
    self.animal:getBehavior():setBlockMovement(false)
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearDrinkAction:complete()
    local f = BanditsNPC.Bear.DrinkComplete
    local ok = false
    if f then ok = f(self.character, self.animal, self.item) end
    if self.animal then self.animal:getBehavior():setBlockMovement(false) end      -- ISMilkAnimal.lua:196
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

-- Feste Dauer (B.CFG.drinkTime, Vorgabe 150 wie das Fuettern); isTimedActionInstant wie ISFeedAnimalFromHand.lua:53-58.
function BanditsNPCBearDrinkAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.drinkTime) or 150
end

function BanditsNPCBearDrinkAction:new(character, animal, item)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.item = item
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
