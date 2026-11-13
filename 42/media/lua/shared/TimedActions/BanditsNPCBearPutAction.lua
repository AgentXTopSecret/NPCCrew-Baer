--
-- NPC Crew -- Baer, Zeitaktion "Etwas in das Inventar des Baeren legen" bzw. "Packtaschen anlegen" (F4, Lauf baer-f4, PLAN_F4.md 6.1;
-- Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md: er traegt alles, hineinlegen nur daneben, hineinlegen weckt nicht).
--
-- Form der Fuetter-Aktion (shared/TimedActions/BanditsNPCBearFeedAction.lua). Liegt in shared/, weil im Mehrspieler auch der Server die Klasse
-- braucht: er baut die Aktion aus den uebertragenen Werten neu (Spieler, Tier, Gegenstand, Text) und ruft serverStart(), bei Abbruch
-- serverStop(), am Ende complete(). Bild und Ton spielt der Client bzw. der Einzelspieler; die Sperre am Tier setzt im Mehrspieler der Server.
-- complete() ist EINE Zeile Kern (f4/schnittstelle.md K2): B.InvPutComplete(character, animal, item, mode) im Schreiber
-- (server/BanditsNPCBearInv.lua) prueft alles (Besitzer, gezaehmt, Abstand, Kampf, Mitfahren, Gegenstand im SERVER-Inventar, Verlustfrei-Regel,
-- Gewicht, 1000 Stueck), nimmt den Gegenstand, prueft die Ankunft und schreibt erst DANN gut -- in EINEM Aufruf. Diese Datei nimmt nichts und
-- schreibt nichts gut. Der Client schickt nie einen Gegenstand selbst: die Engine uebertraegt nur den BEZUG der Zeitaktion (kein Kick,
-- NCC:1612-1621). Auf einem MP-Client gibt es B.InvPutComplete nicht (nil), dort wird complete() auch nie gerufen.
-- mode = "inv" (in das Inventar) oder "bag" (Packtaschen NPCCrew.BearPacks anlegen; Stufe, Taschen schon an: der Kern).
-- KEIN Wecken (Kevin, PLAN_F4.md 23 "ohne Frage"): ein schlafender Baer schlaeft weiter -- waitToStart dreht nur zum Tier.
-- Bild: Vanillas Griff in einen Behaelter (V:client/TimedActions/ISInventoryTransferAction.lua:193-209: setActionAnim("Loot"), LootPosition,
-- setOverrideHandModels(nil, nil), reportEvent("EventLootItem")) -- beim Jungen "Low" wie ein Behaelter am Boden (:204), beim grossen Baeren
-- "Mid" (Form V:shared/TimedActions/ISApplyBandage.lua:61-63: Griff an einer anderen Figur). Ton "PutItemInBag" (Vanillas Taschen-Ton,
-- V:shared/TimedActions/ISDropWorldItemAction.lua:31 / :36).
-- Die Klasse ist eine GLOBALE Variable mit dem Namen ihres Typs und new() nennt seine Parameter wie die Felder: beides verlangt die Engine fuer
-- Netz-Aktionen (Form V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3 und :66-74). Nur Spieler, Tier, Gegenstand und Text als
-- Parameter -- kein nil (F 4.2: PZNetKahluaTableImpl traegt STRING, DOUBLE, InventoryItem, IsoAnimal).
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearPutAction = ISBaseTimedAction:derive("BanditsNPCBearPutAction")

local PUT_SOUND = "PutItemInBag"

-- Fester Wert des Kerns (B.CFG, Block "F4", f4/schnittstelle.md K9) als Zahl, sonst def.
local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Nur Client und Einzelspieler, billig (der Server fragt isValid nie). Form wie die Fuetter-Aktion: ISFeedAnimalFromHand.lua:5-7 (contains),
-- ISPetAnimal.lua:5-7 (Abstand unter 3), ISAnimalUI.lua:15 (isExistInTheWorld), ISHutchUI.lua:427 (isDead).
function BanditsNPCBearPutAction:isValid()
    local a = self.animal
    if not a or not self.item then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    if here:DistTo(there) >= 3 then return false end
    return self.character:getInventory():contains(self.item)
end

-- Zum Tier drehen (ISPetAnimal.lua:9-12). Kein Warten auf Wecken: hineinlegen weckt nicht.
function BanditsNPCBearPutAction:waitToStart()
    self.character:faceThisObject(self.animal)
    return self.character:shouldBeTurning()
end

-- Figur und Baer sehen sich an: ISPetAnimal.lua:16-17.
function BanditsNPCBearPutAction:update()
    self.character:faceThisObject(self.animal)
    self.animal:faceThisObject(self.character)
end

-- Griff-Hoehe: beim Jungen unten (wie ein Behaelter am Boden), sonst Mitte. Koerper ueber den Kern (B.BodyKind, einziger Art-Vergleich).
local function lootPos(a)
    if B.BodyKind and B.BodyKind(a) == "big" then return "Mid" end
    return "Low"
end

function BanditsNPCBearPutAction:start()
    local a = self.animal
    self:setActionAnim("Loot")                                  -- ISInventoryTransferAction.lua:193
    self:setAnimVariable("LootPosition", lootPos(a))            -- :198 / :204
    self:setOverrideHandModels(nil, nil)                        -- :195
    self.character:reportEvent("EventLootItem")                 -- :209
    a:getBehavior():setBlockMovement(true)                      -- ISFeedAnimalFromHand.lua:19
    self.sound = self.character:playSound(PUT_SOUND)            -- ISDropWorldItemAction.lua:36
    -- Beschaeftigt-Marke beim Schreiber, nur im Einzelspieler (im Mehrspieler setzt sie serverStart am Server): kein Koerper-Tausch
    -- (Wachsen, Aussehen, Unstuck), solange die Aktion laeuft (B.BodyBusy, server/BanditsNPCBearGrow.lua)
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(a, true) end
end

-- Jeder Ausgang loest die Sperre und stoppt den Ton (ISFeedAnimalFromHand.lua:28, :60-64).
function BanditsNPCBearPutAction:release()
    local a = self.animal
    if a then a:getBehavior():setBlockMovement(false) end
    if self.sound and self.character:getEmitter():isPlaying(self.sound) then
        self.character:getEmitter():stopOrTriggerSound(self.sound)
    end
    self.sound = nil
end

function BanditsNPCBearPutAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)                           -- ISFeedAnimalFromHand.lua:29
end

function BanditsNPCBearPutAction:stop()
    self:release()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end      -- im MP-Client fehlt die Funktion (nur Schreiber)
    ISBaseTimedAction.stop(self)                                -- ISFeedAnimalFromHand.lua:35
end

function BanditsNPCBearPutAction:perform()
    self:release()
    ISBaseTimedAction.perform(self)                             -- ISFeedAnimalFromHand.lua:41-42
end

-- Einzelspieler und Server: Sperre und Beschaeftigt-Marke (Form V:shared/TimedActions/Animals/ISMilkAnimal.lua:212 / :169 / :196, wie die
-- Fuetter-Aktion). Alles andere -- Pruefen, Nehmen, Gutschreiben -- macht der Kern in complete() in EINEM Aufruf.
function BanditsNPCBearPutAction:serverStart()
    self.animal:getBehavior():setBlockMovement(true)
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearPutAction:serverStop()
    self.animal:getBehavior():setBlockMovement(false)
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearPutAction:complete()
    local f = BanditsNPC.Bear.InvPutComplete
    local ok = false
    if f then ok = f(self.character, self.animal, self.item, self.mode) end
    if self.animal then self.animal:getBehavior():setBlockMovement(false) end      -- ISMilkAnimal.lua:196
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

-- Dauer (f4/schnittstelle.md K2): Packtaschen anlegen bagOnTime; sonst invPutTime + invPutPerKg x kg, hoechstens invPutMax. Gewicht wie der
-- Kern: item:getUnequippedWeight() (V:client/Hotbar/ISHotbar.lua:573). Sofort-Modus wie ISFeedAnimalFromHand.lua:53-58.
function BanditsNPCBearPutAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    if self.mode == "bag" then return cfgNum("bagOnTime", 300) end
    local kg = 0
    if self.item then kg = tonumber(self.item:getUnequippedWeight()) or 0 end
    local t = cfgNum("invPutTime", 40) + cfgNum("invPutPerKg", 8) * kg
    local most = cfgNum("invPutMax", 150)
    if t > most then t = most end
    return math.floor(t + 0.5)
end

function BanditsNPCBearPutAction:new(character, animal, item, mode)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.item = item
    if mode ~= "bag" then mode = "inv" end                      -- nur diese zwei; ein Unsinn-Wert legt in das Inventar
    o.mode = mode
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
