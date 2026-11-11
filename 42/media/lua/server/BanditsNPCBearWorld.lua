if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Engine-Seite des Schreibers (B1a, PLAN_ZAEHMEN.md 5.1, 6.2.3, 6.3, 6.7).
--
-- Hier stehen ALLE Griffe in die Welt: Spielerliste, Tier erzeugen / finden / entfernen, Kachel- und Waldpruefung, Halten
-- und Laufen. Die Takte und Regeln (server/BanditsNPCBearServer.lua) rufen nur diese Funktionen, deshalb kann eine
-- Attrappe sie ersetzen. Jeder Engine-Aufruf nennt seine Fundstelle (Vanilla-Lua oder Bandits 42.22).
--
-- Tier erzeugen NUR in B.CreateCub (einziger Aufrufer: B.AppearFor), Tier entfernen NUR in B.RemoveCub.
-- Im Mehrspieler ruft das nur der Server: ein Client, der an seiner Kopie entfernt, macht ein Geistertier.
-- Nicht benutzt (Plan 0.8): pathToLocation, setWild, die Engine-Akzeptanz als Balken, LosUtil, getCell():getAnimals().
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._orph = B._orph or {}             -- B1b: Waisen-Kandidaten { { o, at } } (Deckel B.CFG.orphanMax), nur fuer die Sitzung

-- ---------------------------------------------------------------------------
-- Spieler
-- ---------------------------------------------------------------------------

-- Liste { p, key, uid, nr, x, y, z } der lebenden Spieler. Server: getOnlinePlayers() mit :size() / :get(i)
-- (Vanilla server/Foraging/forageServer.lua:463-466). Einzelspieler: getNumActivePlayers() (Vanilla
-- client/Fishing/FishingHandler.lua:6) und getSpecificPlayer(i) (server/BuildingObjects/ISBuildingObject.lua:183).
-- isDead am Spieler (Server: getOnlinePlayers():get(i), Einzelspieler: getSpecificPlayer(i)): server/XpSystem/XpUpdate.lua:298
-- (Nachbesserung B1b A4: der vorige Beleg lag in auskommentiertem Vanilla-Code). getX/getY: Bandits server/BanditServerSpawner.lua:179.
-- uid trennt lokale Spieler, die sich im Einzelspieler den Schluessel "__sp" teilen; nr ist dort die Spielernummer.
-- car (B1b): sitzt der Spieler in einem Fahrzeug? player:getVehicle(): Vanilla server/Vehicles/VehicleCommands.lua:11 (Server,
-- Spieler eines Client-Befehls), client/ISUI/Hutch/ISHutchMenu.lua:8 (getSpecificPlayer(n):getVehicle(), Einzelspieler).
function B.Players()
    local list = {}
    if isServer() then
        local online = getOnlinePlayers()
        if online then
            for i = 0, online:size() - 1 do
                local p = online:get(i)
                if p and not p:isDead() then
                    local key = B.PlayerKey(p)
                    if key ~= nil then
                        list[#list + 1] = { p = p, key = key, uid = key, nr = nil, x = p:getX(), y = p:getY(), z = p:getZ(),
                                            car = (p:getVehicle() ~= nil) }
                    end
                end
            end
        end
        return list
    end
    for i = 0, getNumActivePlayers() - 1 do
        local p = getSpecificPlayer(i)
        if p and not p:isDead() then
            list[#list + 1] = { p = p, key = B.SP_KEY, uid = B.SP_KEY .. "#" .. string.format("%d", i), nr = i,
                                x = p:getX(), y = p:getY(), z = p:getZ(), car = (p:getVehicle() ~= nil) }
        end
    end
    return list
end

-- Spieler zu einem Schluessel, wenn er gerade da ist (fuer Meldungen).
function B.PlayerByKey(key, players)
    if key == nil then return nil end
    players = players or B.Players()
    for i = 1, #players do
        if players[i].key == key then return players[i].p, players[i] end
    end
    return nil, nil
end

-- Ist es Nacht? Form Vanilla shared/Foraging/forageSystem.lua:1944-1951 (getClimateManager():getSeason(), getDawn, getDusk,
-- getGameTime():getTimeOfDay()).
function B.IsNight()
    local season = getClimateManager():getSeason()
    local dawn = season:getDawn()
    local dusk = season:getDusk()
    local timeOfDay = getGameTime():getTimeOfDay()
    return (timeOfDay < dawn) or (timeOfDay > dusk)
end

-- ---------------------------------------------------------------------------
-- Kacheln
-- ---------------------------------------------------------------------------

-- Wasser: dort bleibt ein Tier halb gebaut. Vanilla client/ISUI/ISWorldObjectContextMenu.lua:687-688.
local function isWater(sq)
    local floor = sq:getFloor()
    return floor ~= nil and floor:hasProperty(IsoFlagType.water)
end

-- Kann hier ein Junges stehen (bzw. ein Koeder liegen)? Rueckgabe: boolean, why.
-- isOutside: Bandits server/BanditServerSpawner.lua:152. TreatAsSolidFloor: Bandits server/BuildingObjects/ZSGuardposts.lua:12,
-- Vanilla server/BuildingObjects/ISWalkToCursor.lua:35. HasTree: Vanilla server/Foraging/forageServer.lua:276.
-- isFree(false): Bandits server/BanditServerSpawner.lua:231, Vanilla client/ISUI/ISWorldObjectContextMenu.lua:2219.
-- isVehicleIntersecting: Vanilla server/BuildingObjects/ISBuildUtil.lua:34.
function B.SquareFits(sq)
    if sq == nil then return false, "unloaded" end
    if not sq:isOutside() then return false, "inside" end
    if not sq:TreatAsSolidFloor() then return false, "nofloor" end
    if isWater(sq) then return false, "water" end
    if sq:HasTree() then return false, "tree" end
    if not sq:isFree(false) then return false, "blocked" end
    if sq:isVehicleIntersecting() then return false, "vehicle" end
    return true, nil
end

-- "Gegend geladen": die Kachel und vier Punkte im Abstand B.CFG.loadRing, alle am Boden. Nur dann darf "Tier fehlt" zaehlen.
-- getCell():getGridSquare(x, y, z) (nil = nicht geladen): Vanilla server/Animal/ISPickDungCursor.lua:104.
function B.AreaLoaded(x, y)
    local cell = getCell()
    local r = B.CFG.loadRing
    x = math.floor(x)
    y = math.floor(y)
    if cell:getGridSquare(x, y, 0) == nil then return false end
    if cell:getGridSquare(x + r, y, 0) == nil then return false end
    if cell:getGridSquare(x - r, y, 0) == nil then return false end
    if cell:getGridSquare(x, y + r, 0) == nil then return false end
    if cell:getGridSquare(x, y - r, 0) == nil then return false end
    return true
end

-- Einzelspieler: sieht ein lokaler Spieler diese Kachel gerade? isCanSee(Spielernummer): Vanilla
-- client/Foraging/ISBaseIcon.lua:256. Auf dem Server gibt es kein Sichtfeld je Spieler: dort immer false (ehrliche Grenze,
-- "ausser Sicht" gilt im Mehrspieler nur ueber den Mindestabstand).
function B.SeenInSP(sq, players)
    if sq == nil or not B.IsSP() then return false end
    players = players or B.Players()
    for i = 1, #players do
        local nr = players[i].nr
        if nr ~= nil and sq:isCanSee(nr) then return true end
    end
    return false
end

local function nearestDist(x, y, players)
    local best = nil
    for i = 1, #players do
        local d = B.DistXY(x, y, players[i].x, players[i].y)
        if best == nil or d < best then best = d end
    end
    return best
end

-- Abstand des naechsten Spielers zu einem Punkt (nil = niemand da).
function B.NearestPlayerDist(x, y, players)
    return nearestDist(x, y, players or B.Players())
end

-- Platz im Wald fuer ein neues Junges (Plan 5.1): bis B.CFG.tries Zufallspunkte im Ring Min..Max um den Spieler.
-- Kachel geladen, am Boden, Waldzone, B.SquareFits, Abstand zu ALLEN Spielern mindestens Min; im Einzelspieler zusaetzlich
-- nicht im Blick. Kein Punkt -> nil (kein Nachholen). player: Eintrag aus B.Players() oder ein Spieler.
-- Ring-Form und ZombRandFloat(a, b): Bandits server/BanditServerSpawner.lua:216-222.
function B.PickForestSquare(player, players)
    if player == nil then return nil end
    local e = player
    if type(e) ~= "table" then
        e = { p = player, x = player:getX(), y = player:getY(), z = player:getZ() }
    end
    players = players or B.Players()
    local minD = B.Opt("BearCubMinDistance")
    local maxD = B.Opt("BearCubMaxDistance")
    if maxD < minD + 5 then maxD = minD + 5 end
    if maxD > 65 then maxD = 65 end                 -- geladen sind 76 Kacheln um den Spieler: nie weiter ansprechen
    if minD > maxD then minD = maxD end
    local cell = getCell()
    for _ = 1, B.CFG.tries do
        local theta = ZombRandFloat(0, 2 * math.pi)
        local d = ZombRandFloat(minD, maxD)
        local x = math.floor(e.x + d * math.cos(theta))
        local y = math.floor(e.y + d * math.sin(theta))
        local sq = cell:getGridSquare(x, y, 0)
        if sq ~= nil and B.IsForestAt(x, y, 0) then
            local fits, _ = B.SquareFits(sq)
            if fits then
                local nd = nearestDist(x + 0.5, y + 0.5, players)
                if (nd == nil or nd >= minD) and not B.SeenInSP(sq, players) then
                    return sq
                end
            end
        end
    end
    return nil
end

-- Freie Kachel im Umkreis r um einen Punkt (Koeder-Junges). Beginnt an einer Zufallsstelle, hoechstens (2r+1)^2 Fragen.
-- ZombRand(n): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:25.
function B.FreeSquareNear(x, y, z, r, players)
    local cell = getCell()
    local side = 2 * r + 1
    local total = side * side
    local start = ZombRand(total)
    for k = 0, total - 1 do
        local idx = start + k
        if idx >= total then idx = idx - total end
        local ox = idx - math.floor(idx / side) * side - r
        local oy = math.floor(idx / side) - r
        local sq = cell:getGridSquare(x + ox, y + oy, z)
        if sq ~= nil then
            local fits, _ = B.SquareFits(sq)
            if fits and not B.SeenInSP(sq, players) then return sq end
        end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- Tier erzeugen, entfernen, finden
-- ---------------------------------------------------------------------------

-- Rasse-Objekt zur Art. AnimalDefinitions.getDef(Artname-Text) und def:getBreedByName(Rasse-Text): Vanilla
-- server/ClientCommands.lua:808 (Server, direkt vor addAnimal) und shared/Definitions/animal/ButcheringUtil.lua:79/85 (mit
-- nil-Pruefung). Nachbesserung A3: vorher getAllAnimalsDefinitions/getBreeds, das nur Client-Belege hatte.
local function findBreed()
    local def = AnimalDefinitions.getDef(B.CUB)
    if def == nil then return nil end
    return def:getBreedByName(B.BREED)
end

-- Die EINZIGE Stelle, die ein Tier in die Welt setzt. Gerufen nur von B.AppearFor. Rueckgabe: IsoAnimal oder nil, why.
-- addAnimal(getCell(), x, y, z, Art, Rasse-Objekt, false) und animal:addToWorld(): Vanilla server/ClientCommands.lua:809-810
-- (Server) und client/DebugUIs/DebugContextMenu.lua:1460-1467 (Einzelspieler). Derselbe Aufruf, aber von sich aus beim
-- Schreiber -- kein Client-Weg, kein Recht noetig, kein Kick. Koordinaten als ganze Zahlen; die Kachel hat der Aufrufer
-- mit B.SquareFits geprueft (kein Wasser).
function B.CreateCub(x, y, z)
    if not B.IsWriter() then return nil, "nowriter" end
    local breed = findBreed()
    if not breed then
        B.ErrEvery("nodef", 600000, "create: animal definition " .. tostring(B.CUB) .. " is not loaded")
        return nil, "nodef"
    end
    local animal = addAnimal(getCell(), math.floor(x), math.floor(y), math.floor(z), B.CUB, breed, false)
    if not animal then
        B.Err("create: addAnimal gave nothing at " .. tostring(x) .. "," .. tostring(y))
        return nil, "noanimal"
    end
    animal:addToWorld()
    -- KEINE Pruefung mit isExistInTheWorld direkt nach addToWorld (Kevins Test 10.11.2026: "no cub: notinworld", console.txt
    -- "[TC-BEAR] *** create: the new cub is not in the world"): die Engine haengt ein neues Tier erst beim naechsten Update in die
    -- Liste seiner Kachel (Jar 42.22.2 IsoAnimal.isExistInTheWorld = square.getMovingObjects().contains(this)); im selben Bild ist
    -- die Antwort deshalb immer falsch. Vanilla prueft hier auch nicht (server/ClientCommands.lua:809-810,
    -- client/DebugUIs/DebugContextMenu.lua:1466-1467), ebenso der gespielte Erwachsene (NCBearTest client/NCBearSpawn.lua:56).
    -- Fehlt das Tier wirklich, findet es der Suchlauf nicht und der Eintrag wird als verloren geschlossen.
    return animal, nil
end

-- Die EINZIGE Stelle, die ein Tier entfernt (Verschwinde-Regel, Aufraeumen). Nur unsere Art, nur beim Schreiber.
-- Erst die Bewegungssperre loesen (getBehavior():setBlockMovement(false): Vanilla
-- shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:28), dann animal:remove(): Vanilla
-- shared/Definitions/animal/ButcheringUtil.lua:609 (shared, laeuft auch auf dem Server), client/DebugUIs/DebugContextMenu.lua:616.
-- Auf dem Server zusaetzlich removeAnimal(animal:getOnlineID()), damit die Clients ihre Kopie verlieren -- genau wie
-- ButcheringUtil.lua:612-614 (isServer-Zweig nach remove(); Server-Befehl server/ClientCommands.lua:841). Im Einzelspieler
-- nur remove() (DebugContextMenu.lua:231-235 -> :616). Nachbesserung A1. remove() hinterlaesst keine Leiche.
function B.RemoveCub(animal)
    if not animal or not B.IsWriter() then return end
    if animal:getAnimalType() ~= B.CUB then return end
    animal:getBehavior():setBlockMovement(false)
    animal:remove()
    if isServer() then
        removeAnimal(animal:getOnlineID())
    end
end

-- Das in dieser Sitzung gemerkte Objekt eines Eintrags, mit Gegenprobe (in der Welt, lebt, Art, AnimalID). Sonst nil:
-- der naechste Suchlauf findet es. Raeumt nichts weg -- den Tod muss der Hirn-Takt am gemerkten Objekt noch sehen koennen.
-- isDead am Tier: Vanilla server/Traps/STrapGlobalObject.lua:238.
function B.FindAnimal(rec)
    if not rec then return nil end
    local s = B._s[rec.id]
    local a = s and s.obj
    if a == nil then return nil end
    if not a:isExistInTheWorld() or a:isDead() then return nil end
    if a:getAnimalType() ~= B.CUB then return nil end
    if rec.aid ~= nil and a:getAnimalID() ~= rec.aid then return nil end
    return a
end

-- Suchlauf: alle geladenen Jungen ansehen und den Eintraegen ihre Objekte geben. Teuer (die Engine kopiert die ganze
-- Objektliste), deshalb nur bei Bedarf und fruehestens alle B.CFG.scanMs (das regelt der Hirn-Takt).
-- getCell():getObjectListForLua(), :size(), :get(i), instanceof(o, "IsoAnimal"): Vanilla
-- client/DebugUIs/DebugContextMenu.lua:612-615. Ein Server-Beleg fehlt (Vanilla server/, shared/ und Bandits: 0 Treffer):
-- im Mehrspieler OFFEN, Testpunkt (Plan 6.3; Nachbesserung A3). getAnimalID ebenso (nur Client-Belege, ISAnimalUI.lua:53).
-- Zuordnung ueber den Spiegel am Tier (id) mit Gegenprobe AnimalID. Rueckfall, wenn der Spiegel fehlt oder nicht passt
-- (jeder Client kann Tier-ModData ueberschreiben): gleiche AnimalID, genau EIN Kandidat, hoechstens 40 Kacheln von der
-- letzten bekannten Kachel -- dann wird neu gestempelt. Mehrere Kandidaten: nichts (nie raten).
--
-- Ein Junges, dessen Spiegel auf einen GESCHLOSSENEN Eintrag zeigt und das dabei noch ungefuettert war (mark.st new/shy),
-- ist ein schon "weitergezogenes" Tier aus einer damals nicht geladenen Gegend (server/BanditsNPCBearServer.lua slowRec):
-- es wird ueber B.RemoveCub entfernt, sobald niemand naeher als B.CFG.vanishKeep steht und es keiner sieht. Angefuetterte
-- oder zahme Tiere ohne Eintrag bleiben (sie werden beim Anfassen ueber B.RecOf neu aufgenommen).
--
-- B1b (PLAN_B1B.md 4, N5): WAISEN. Eine Waise ist ein lebendes ncbearcub OHNE Spiegel und ohne passenden Eintrag (Rest nach einem
-- Fehler oder Absturz). Nie der Erwachsene, nie fremde Tiere (Art-Frage oben). Drei Riegel, alle Pflicht:
--   1 Identitaet: das in dieser Sitzung gemerkte Objekt eines Eintrags (B._s[id].obj) ist nie Waise; fehlt sein Spiegel, wird er
--     sofort ueber B.Commit geschrieben (Spiegel-Reparatur).
--   2 Mehrdeutig: gleiche AnimalID wie ein Eintrag ohne lebendes Objekt -> nie entfernt (nie raten; strenger als der Rueckfall,
--     der nur bis 40 Kacheln bindet), eine Diagnose-Zeile, wenn der Rueckfall mehrere Kandidaten hatte.
--   3 Alter und Beobachter: entfernt erst, wenn dasselbe Objekt schon bei einem frueheren Suchlauf vor mindestens
--     B.CFG.orphanAgeMs Waise war (Liste B._orph, Deckel B.CFG.orphanMax, Vergleich mit ==), UND niemand naeher als
--     B.CFG.vanishKeep steht, UND es im Einzelspieler keiner sieht. force ueberspringt NUR das Alter (der Spielcode ruft nie mit force).
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456. B.ScanAnimals gibt n (gebunden), removed (entfernte Waisen).

-- Eine Waise entfernen, wenn niemand naeher als vanishKeep steht und sie (SP) keiner sieht. Rueckgabe: true, wenn entfernt.
-- Nur ueber B.RemoveCub (einzige Entfern-Stelle; im MP mit removeAnimal).
local function dropOrphan(o, players)
    local nd = nearestDist(o:getX(), o:getY(), players)
    if (nd ~= nil and nd < B.CFG.vanishKeep) or B.SeenInSP(o:getSquare(), players) then return false end
    local x, y = math.floor(o:getX()), math.floor(o:getY())
    B.RemoveCub(o)
    B.Log("scan: removed an orphan cub (no mark, no entry) at " .. x .. "," .. y)
    return true
end

local function sweepOrphans(found, players, force, ms)
    local old = B._orph
    if type(old) ~= "table" then old = {} end
    local cap = tonumber(B.CFG.orphanMax) or 16
    local keep = {}
    local taken = {}
    local removed = 0
    -- zuerst die schon bekannten Waisen (sie sind der Entfernung naeher)
    for i = 1, #found do
        local o = found[i]
        for k = 1, #old do
            local e = old[k]
            if type(e) == "table" and e.o == o then
                taken[i] = true
                local at = tonumber(e.at)
                if at == nil or ms - at < 0 then at = ms end          -- Uhr rueckwaerts: Messung neu beginnen
                if (force == true or ms - at >= B.CFG.orphanAgeMs) and dropOrphan(o, players) then
                    removed = removed + 1
                elseif #keep < cap then
                    keep[#keep + 1] = { o = o, at = at }
                end
                break
            end
        end
    end
    -- dann neue, solange der Deckel Platz hat (auch Plaetze, die eben frei wurden); force entfernt sie gleich
    for i = 1, #found do
        if not taken[i] then
            local o = found[i]
            if force == true and dropOrphan(o, players) then
                removed = removed + 1
            elseif #keep < cap then
                keep[#keep + 1] = { o = o, at = ms }
            end
        end
    end
    B._orph = keep
    return removed
end

function B.ScanAnimals(players, force)
    local reg = B.Reg()
    if not reg then return 0, 0 end
    local list = getCell():getObjectListForLua()
    if not list then return 0, 0 end
    players = players or B.Players()
    local n = 0
    local loose = nil
    local looseMark = nil                       -- [j] = true: dieses lose Tier traegt einen Spiegel (dann nie Waise)
    local stale = nil
    for i = 0, list:size() - 1 do
        local o = list:get(i)
        if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB and not o:isDead() then
            local md = o:getModData()
            local mark = md and md[B.MARK]
            local hasMark = type(mark) == "table" and mark.id ~= nil
            local rec = nil
            local bound = false
            -- Riegel 1 (Identitaet + Spiegel-Reparatur)
            for id, s in pairs(B._s) do
                if s.obj == o then
                    local own = reg.cubs[id]
                    if own then
                        bound = true
                        n = n + 1
                        if not hasMark or mark.id ~= id then
                            B.Commit(own)
                            B.Log("scan: mark of " .. tostring(id) .. " written anew (the animal is the one of this session)")
                        end
                    end
                    break
                end
            end
            if not bound and hasMark then
                rec = reg.cubs[mark.id]
                if rec == nil and (mark.st == "new" or mark.st == "shy") then
                    stale = stale or {}
                    stale[#stale + 1] = o
                    bound = true                    -- nicht zuordnen: dieses Tier hat keinen Eintrag mehr
                end
            end
            if not bound and rec and rec.aid == o:getAnimalID() then
                local s = B.Ses(rec.id)
                if s.obj == nil or s.obj == o or not s.obj:isExistInTheWorld() or s.obj:isDead() then
                    s.obj = o
                    n = n + 1
                    bound = true
                end
            end
            if not bound then
                loose = loose or {}
                looseMark = looseMark or {}
                loose[#loose + 1] = o
                looseMark[#loose] = hasMark
            end
        end
    end
    -- Rueckfall ueber die AnimalID fuer jeden Eintrag OHNE lebendes Objekt (B1b: auch, wenn das gemerkte Objekt nicht mehr in
    -- der Welt ist -- wie der Spiegel-Weg oben; B1a nahm nur Eintraege ganz ohne Objekt).
    local guard = nil                           -- Riegel 2: [j] = true -> dieses lose Tier wird nie entfernt
    if loose then
        for id, rec in pairs(reg.cubs) do
            local s = B._s[id]
            local live = s ~= nil and s.obj ~= nil and s.obj:isExistInTheWorld() and not s.obj:isDead()
            if not live then
                local hit, hitAt, hits = nil, 0, 0
                for j = 1, #loose do
                    local o = loose[j]
                    if o and o:getAnimalID() == rec.aid then
                        guard = guard or {}
                        guard[j] = true
                        if B.DistXY(o:getX(), o:getY(), rec.x, rec.y) <= 40 then
                            hit = o
                            hitAt = j
                            hits = hits + 1
                        end
                    end
                end
                if hits == 1 then
                    B.Ses(id).obj = hit
                    loose[hitAt] = false
                    n = n + 1
                    B.Commit(rec)
                    B.Log("scan: " .. id .. " found again by its animal id, mark written anew")
                elseif hits > 1 then
                    B.Log("scan: " .. id .. " has " .. hits .. " animals with its animal id nearby: none bound, none removed")
                end
            end
        end
    end
    if stale then
        -- erst nach dem Durchlauf entfernen (die Liste ist eine Kopie, trotzdem nie waehrend des Lesens aendern)
        for j = 1, #stale do
            local o = stale[j]
            local nd = nearestDist(o:getX(), o:getY(), players)
            if (nd == nil or nd >= B.CFG.vanishKeep) and not B.SeenInSP(o:getSquare(), players) then
                B.RemoveCub(o)
                B.Log("scan: removed a cub whose entry had wandered off")
            end
        end
    end
    local found = {}
    if loose then
        for j = 1, #loose do
            local o = loose[j]
            if o and not looseMark[j] and not (guard and guard[j]) then found[#found + 1] = o end
        end
    end
    local removed = sweepOrphans(found, players, force, getTimestampMs())
    return n, removed
end

-- ---------------------------------------------------------------------------
-- Halten und Laufen (Plan 6.7)
-- ---------------------------------------------------------------------------

-- Stehenbleiben. getBehavior():setBlockMovement(b): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:89,
-- shared/TimedActions/Animals/ISPetAnimal.lua:36. Die Engine loest die Sperre nach einer Weile von selbst (haengt nie
-- endlos); deshalb setzt der Hirn-Takt sie jeden Takt neu, solange sie gelten soll.
function B.Hold(rec, animal, on)
    if not rec or not animal then return end
    animal:getBehavior():setBlockMovement(on == true)
    local s = B.Ses(rec.id)
    if on == true then
        s.held = true
        s.chk = nil
    else
        s.held = nil
    end
end

-- Die Zielkachel und bis zu vier gedrehte Ersatzpunkte (Bogenmass).
local TURN = { 0, 0.6, -0.6, 1.2, -1.2 }

-- Zu einem Punkt rennen. animal:fleeTo(square): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:38 (laeuft dort auch auf
-- dem Server). Derselbe Befehl fruehestens nach B.CFG.moveMs. Zielkachel nicht geladen oder Wasser: Ersatzpunkte, dann nichts.
-- opt (B1b, wahlfrei): opt.minMs ersetzt B.CFG.moveMs; opt.watch == false -> keine Gegenprobe (B.MoveWatch), weil beim Folgen
-- ein Halt vor einer Tuer kein Fehler ist. Ohne opt wie B1a.
-- Rueckgabe: true, wenn ein Befehl hinausging.
function B.MoveTo(rec, animal, x, y, z, opt)
    if not rec or not animal or x == nil or y == nil then return false end
    local ms = getTimestampMs()
    local s = B.Ses(rec.id)
    local minMs = B.CFG.moveMs
    if type(opt) == "table" and tonumber(opt.minMs) ~= nil then minMs = tonumber(opt.minMs) end
    if s.moveAt ~= nil and ms - s.moveAt >= 0 and ms - s.moveAt < minMs then return false end
    local ax, ay = animal:getX(), animal:getY()
    local dx, dy = x - ax, y - ay
    z = math.floor(z or 0)
    local cell = getCell()
    local sq = nil
    for i = 1, #TURN do
        local cs, sn = math.cos(TURN[i]), math.sin(TURN[i])
        local cand = cell:getGridSquare(math.floor(ax + dx * cs - dy * sn), math.floor(ay + dx * sn + dy * cs), z)
        if cand ~= nil and not isWater(cand) then
            sq = cand
            break
        end
    end
    if sq == nil then return false end
    if s.held then B.Hold(rec, animal, false) end
    animal:fleeTo(sq)
    s.moveAt = ms
    -- Gegenprobe nur fuer Wege, die lang genug sind, um sie zu sehen
    if type(opt) == "table" and opt.watch == false then
        s.chk = nil
    elseif dx * dx + dy * dy >= 2.25 then
        s.chk = { x = ax, y = ay, n = 0 }
    else
        s.chk = nil
    end
    return true
end

-- Gegenprobe zum Laufbefehl, je Hirn-Takt: hat sich das Tier 3 Takte danach nicht bewegt, eine gedrosselte Zeile
-- (Diagnose, kein Abbruch).
function B.MoveWatch(rec, animal)
    local s = B._s[rec.id]
    local chk = s and s.chk
    if not chk then return end
    chk.n = chk.n + 1
    if chk.n < 3 then return end
    s.chk = nil
    if B.DistXY(chk.x, chk.y, animal:getX(), animal:getY()) < 0.3 then
        B.ErrEvery("still:" .. tostring(rec.id), 60000, "move: " .. tostring(rec.id) .. " did not move after a run order (fleeTo)")
    end
end
