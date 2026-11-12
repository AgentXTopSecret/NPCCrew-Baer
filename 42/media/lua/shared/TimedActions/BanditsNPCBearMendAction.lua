--
-- NPC Crew -- Baer, Zeitaktion "Baeren verbinden" (F2 = B5a, PLAN_F2.md 0.12, 2.5; Kevin 11.11.2026: "wir koennen den baeren manuel heilen").
--
-- Vierte Zeitaktion nach dem gespielten Fuetter-Weg (shared/TimedActions/BanditsNPCBearFeedAction.lua, gleiche Form). Liegt in shared/,
-- weil im Mehrspieler auch der Server die Klasse braucht: er baut die Aktion aus den uebertragenen Werten neu (Spieler, Tier, Gegenstand
-- -- SEIN Gegenstand) und ruft serverStart(), bei Abbruch serverStop(), am Ende complete(). Bild und Ton spielt der Client bzw. der
-- Einzelspieler.
-- complete() ist eine Zeile und ruft den Schreiber-Kern (B.MendComplete, server/BanditsNPCBearMend.lua, KERN): dort stehen ALLE Pruefungen
-- (Besitzer, gezaehmt, geladen, Abstand, Gegenstand im Inventar, sauber, ist ein Verband, nicht gesund, nicht schon verbunden), dort wird
-- GENAU EIN Stueck genommen (B.TakeOne) und im selben Aufruf gutgeschrieben. Diese Datei nimmt nichts und schreibt nichts gut: ein Abbruch
-- (Weglaufen, Esc, Tier weg) verbraucht nichts; ein zweites complete() lehnt der Kern ab (Why_Bandaged).
-- Kein Halt am Baeren (anders als das Fuettern): seinen Halt fuehrt allein der Kern (B.Hold -- Kampf, Am Boden); laeuft er weg, wird die
-- Aktion ungueltig (Abstand) und bricht ab.
-- Beschaeftigt-Marke (B.BodyBusy, server/BanditsNPCBearGrow.lua, nur beim Schreiber): der Koerper wird nicht getauscht, solange verbunden
-- wird -- SP in start(), MP-Server in serverStart(); geloescht in stop() / serverStop() / complete() (Deckel busyMs beim Kern).
-- Die Klasse ist eine GLOBALE Variable mit dem Namen ihres Typs und new() nennt seine Parameter wie die Felder: beides verlangt die Engine
-- fuer Netz-Aktionen (Form Vanilla shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:3 und :66-74).
-- Engine-Aufrufe (Fundstelle):
--   isValid: inv:contains(item) V:shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6; sq:DistTo(sq2) >= 3 V:shared/TimedActions/
--     Animals/ISPetAnimal.lua:5-7; animal:isExistInTheWorld() V:client/ISUI/Animal/ISAnimalUI.lua:15; animal:isDead()
--     V:client/ISUI/Hutch/ISHutchUI.lua:427; character:getSquare() / animal:getSquare() ISPetAnimal.lua:6
--   Drehen: character:faceThisObject(animal), character:shouldBeTurning() ISPetAnimal.lua:9-12
--   Bild/Ton: self:setActionAnim("Loot"), character:SetVariable("LootPosition", "Mid"), character:playSound("FirstAidApplyBandage")
--     V:shared/TimedActions/ISApplyBandage.lua:61-62, :70 (Verband an einer ANDEREN Figur); Ton stoppen character:stopOrTriggerSound(ton)
--     V:shared/Camping/TimedActions/ISAddFuelAction.lua:48
--   Dauer: character:isTimedActionInstant() ISFeedAnimalFromHand.lua:54; ISBaseTimedAction.new / stop / forceStop / perform wie die
--     Fuetter-Aktion (S:shared/TimedActions/BanditsNPCBearFeedAction.lua, gespielt)
-- Statisch geprueft, nicht gespielt.
--

require "TimedActions/ISBaseTimedAction"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

BanditsNPCBearMendAction = ISBaseTimedAction:derive("BanditsNPCBearMendAction")

-- Nur Client und Einzelspieler, billig (der Server fragt isValid nie).
function BanditsNPCBearMendAction:isValid()
    local a = self.animal
    if not a or not self.item then return false end
    if not a:isExistInTheWorld() or a:isDead() then return false end
    local here = self.character:getSquare()
    local there = a:getSquare()
    if not here or not there then return false end
    if here:DistTo(there) >= 3 then return false end
    return self.character:getInventory():contains(self.item)
end

function BanditsNPCBearMendAction:waitToStart()
    self.character:faceThisObject(self.animal)
    return self.character:shouldBeTurning()
end

function BanditsNPCBearMendAction:update()
    self.character:faceThisObject(self.animal)
end

function BanditsNPCBearMendAction:start()
    self:setActionAnim("Loot")                                      -- ISApplyBandage.lua:61
    self.character:SetVariable("LootPosition", "Mid")               -- :62
    self.sound = self.character:playSound("FirstAidApplyBandage")   -- :70
    -- Beschaeftigt-Marke beim Schreiber, nur im Einzelspieler (im Mehrspieler setzt sie serverStart am Server)
    if not isClient() and not isServer() and B.BodyBusy then B.BodyBusy(self.animal, true) end
end

-- Jeder Ausgang stoppt nur den Ton -- nie ein Gegenstand.
function BanditsNPCBearMendAction:release()
    if self.sound then self.character:stopOrTriggerSound(self.sound) end    -- ISAddFuelAction.lua:48
    self.sound = nil
end

function BanditsNPCBearMendAction:forceStop()
    self:release()
    ISBaseTimedAction.forceStop(self)
end

function BanditsNPCBearMendAction:stop()
    self:release()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end          -- im MP-Client fehlt die Funktion (nur Schreiber)
    ISBaseTimedAction.stop(self)
end

function BanditsNPCBearMendAction:perform()
    self:release()
    ISBaseTimedAction.perform(self)                                 -- noetig, damit die Warteschlange weiterlaeuft
end

-- Einzelspieler und Server. Form wie die Fuetter-Aktion (Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:212 / :169 / :196).
function BanditsNPCBearMendAction:serverStart()
    if B.BodyBusy then B.BodyBusy(self.animal, true) end
end

function BanditsNPCBearMendAction:serverStop()
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
end

function BanditsNPCBearMendAction:complete()
    local f = BanditsNPC.Bear.MendComplete
    local ok = false
    if f then ok = f(self.character, self.animal, self.item) end
    if B.BodyBusy then B.BodyBusy(self.animal, false) end
    return ok
end

function BanditsNPCBearMendAction:getDuration()
    if self.character:isTimedActionInstant() then
        return 1
    end
    local cfg = B.CFG
    return (cfg and cfg.mendTime) or 200
end

function BanditsNPCBearMendAction:new(character, animal, item)
    local o = ISBaseTimedAction.new(self, character)
    o.animal = animal
    o.item = item
    o.maxTime = o:getDuration()
    o.stopOnWalk = true
    o.stopOnRun = true
    return o
end
