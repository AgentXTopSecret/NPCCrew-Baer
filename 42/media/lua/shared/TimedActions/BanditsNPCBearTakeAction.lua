--
-- NPC Crew -- Baer, Zeitaktion "Etwas aus dem Inventar des Baeren nehmen" bzw. "Packtaschen abnehmen" (F4, Lauf baer-f4, PLAN_F4.md 6.1, 6.3;
-- Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md: herausnehmen nur daneben, nicht waehrend er mitfaehrt).
--
-- Gegenstueck zu shared/TimedActions/BanditsNPCBearPutAction.lua (dieselbe Form wie die Fuetter-Aktion). Der Client nennt nur BEZUEGE: die
-- Satz-Nummer nr (Text, z. B. "s12", oder "bag" = Packtaschen abnehmen) und die Anzahl k -- nie einen Steckbrief eines Gegenstands
-- (PLAN_F4.md 16). complete() ist EINE Zeile Kern (f4/schnittstelle.md K2): B.InvTakeComplete(character, animal, nr, k) im Schreiber baut je
-- Stueck den Gegenstand aus dem Datensatz, legt ihn in das Inventar des Spielers, prueft die ANKUNFT und traegt erst DANN aus -- hoechstens
-- B.CFG.invTakeMax (50) Stueck je Aktion; groessere Stapel stellt die Oberflaeche als mehrere Aktionen an (client/BanditsNPCBearInvClient.lua).
-- Diese Datei baut nichts und traegt nichts aus. Auf einem MP-Client gibt es B.InvTakeComplete nicht (nil), dort wird complete() nie gerufen.
-- kg = Gewicht, das die Oberflaeche aus der Liste kennt (Stueckgewicht x k): NUR fuer die Dauer auf dem MP-Client; beim Schreiber rechnet
-- getDuration das Gewicht aus dem Register (B.InvTakeKg, Nachbesserung F4 Befund C12) -- die Zahl des Clients bestimmt dort nichts.
-- KEIN Wecken (herausnehmen weckt so wenig wie hineinlegen). Bild und Ton wie die Put-Aktion (Vanillas Griff in einen Behaelter,
-- V:client/TimedActions/ISInventoryTransferAction.lua:193-209; Ton "PutItemInBag" V:shared/TimedActions/ISDropWorldItemAction.lua:31 / :36).
-- GLOBALE Klasse mit dem Namen ihres Typs, new() nennt die Parameter wie die Felder (Netz-Aktion, Form
-- V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3 und :66-74); nur Spieler, Tier, Text, Zahl -- kein nil.
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearTakeAction = ISBaseTimedAction:derive("BanditsNPCBearTakeAction")

local TAKE_SOUND = "PutItemInBag"

local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Nur Client und Einzelspieler, billig (der Server fragt isValid nie): Tier in der Welt, nicht tot, Abstand unter 3 (ISPetAnimal.lua:5-7,
-- ISAnimalUI.lua:15, ISHutchUI.lua:427). Ob der Satz noch da ist und ob es passt, prueft der Kern in complete().
function BanditsNPCBearTakeAction:isValid()
    local a = self.animal
    if not a then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    return here:DistTo(there) < 3
end

function BanditsNPCBearTakeAction:waitToStart()
    self.character:faceThisObject(self.animal)                  -- ISPetAnimal.lua:9-12
    return self.character:shouldBeTurning()
end

function BanditsNPCBearTakeAction:update()
    self.character:faceThisObject(self.animal)                  -- ISPetAnimal.lua:16-17
    self.animal:faceThisObject(self.character)
end

local function lootPos(a)
    if B.BodyKind and B.BodyKind(a) == "big" then return "Mid" end
    return "Low"
end

function BanditsNPCBearTakeAction:start()
    local a = self.animal
    self:setActionAnim("Loot")                                  -- ISInventoryTransferAction.lua:193
    self:setAnimVariable("LootPosition", lootPos(a))            -- :198 / :204
    self:setOverrideHandModels(nil, nil)                        -- :195
    self.character:reportEvent("EventLootItem")                 -- :209
    a:getBehavior():setBlockMovement(true)                      -- ISFeedAnimalFromHand.lua:19
    self.sound = self.character:playSound(TAKE_SOUND)           -- ISDropWorldItemAction.lua:36
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(a, true) end
end

function BanditsNPCBearTakeAction:release()
    local a = self.animal
    if a then a:getBehavior():setBlockMovement(false) end      -- ISFeedAnimalFromHand.lua:28
    if self.sound and self.character:getEmitter():isPlaying(self.sound) then
        self.character:getEmitter():stopOrTriggerSound(self.sound)     -- :60-64
    end
    self.sound = nil
end

function BanditsNPCBearTakeAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)
end

function BanditsNPCBearTakeAction:stop()
    self:release()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    ISBaseTimedAction.stop(self)
end

function BanditsNPCBearTakeAction:perform()
    self:release()
    ISBaseTimedAction.perform(self)
end

-- Einzelspieler und Server (Form V:shared/TimedActions/Animals/ISMilkAnimal.lua:212 / :169 / :196).
function BanditsNPCBearTakeAction:serverStart()
    self.animal:getBehavior():setBlockMovement(true)
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearTakeAction:serverStop()
    self.animal:getBehavior():setBlockMovement(false)
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearTakeAction:complete()
    local f = BanditsNPC.Bear.InvTakeComplete
    local ok = false
    if f then ok = f(self.character, self.animal, self.nr, self.k) end
    if self.animal then self.animal:getBehavior():setBlockMovement(false) end      -- ISMilkAnimal.lua:196
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

-- Dauer (f4/schnittstelle.md K2): Packtaschen abnehmen bagOffTime; sonst wie Hineinlegen mit dem Gewicht des Satzes x k.
function BanditsNPCBearTakeAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    if self.nr == "bag" then return cfgNum("bagOffTime", 200) end
    local kg = tonumber(self.kg) or 0
    -- Nachbesserung F4 (Befund C12): beim Schreiber (Einzelspieler, Server) zaehlt das Gewicht aus dem Register (server/BanditsNPCBearInv.lua
    -- B.InvTakeKg, gleiche Rundung wie die Zeile des Fensters -> ein ehrlicher Client rechnet dieselbe Dauer); auf dem MP-Client gibt es die
    -- Funktion nicht (nil), dort gilt die Zahl aus der Liste.
    local f = B.InvTakeKg
    if f then
        local srv = f(self.animal, self.nr, self.k)
        if srv ~= nil then kg = srv end
    end
    if kg ~= kg or kg < 0 then kg = 0 end
    local t = cfgNum("invPutTime", 40) + cfgNum("invPutPerKg", 8) * kg
    local most = cfgNum("invPutMax", 150)
    if t > most then t = most end
    return math.floor(t + 0.5)
end

function BanditsNPCBearTakeAction:new(character, animal, nr, k, kg)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.nr = tostring(nr)
    k = math.floor(tonumber(k) or 1)
    if k < 1 then k = 1 end
    o.k = k
    o.kg = tonumber(kg) or 0
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
