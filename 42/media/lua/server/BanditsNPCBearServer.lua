if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Schreiber (B1a, PLAN_ZAEHMEN.md 2, 5, 6.2.3, 7).
--
-- Takte (Langsam-Takt alle 10 Spielminuten, Hirn-Takt alle 1,5 s Echtzeit), Bitten der Clients (B.Handle), die drei
-- Abschluesse der Zeitaktionen (B.FeedComplete, B.PetComplete, B.BaitComplete), Erscheinen (B.AppearFor), Koeder-Morgen,
-- Verschwinden, Tod, Vermisst, Sicht verschicken.
--
-- Der Code ist im Einzelspieler und auf dem Server DERSELBE. Was der Schreiber tut, glaubt er nie einem Client: eine Bitte
-- benennt nur (welcher Koederplatz), Besitz / Balken / Zeiten stehen im Register (server/BanditsNPCBearRegistry.lua).
-- Engine-Griffe in die Welt stehen in server/BanditsNPCBearWorld.lua; hier nur die, die zu einem Vorgang gehoeren
-- (Futter nehmen, Streicheln zaehlen, Abstand, Hand und Tempo der Spieler), jeder mit Fundstelle.
-- F1 (PLAN_F1.md 4b, 5.3, 5.4): Bitten "Come"/"Passive", Aufstehen und Bleiben/Sitz/Frei im Hirn-Takt (server/BanditsNPCBearOrder.lua),
-- Rueckkehr eines vermissten Baeren (C1) nach dem Suchlauf, Sicht-Nachschub bei ld/busy-Wechsel, "missing" wird nie mehr geschlossen.
-- F2 = B5a (PLAN_F2.md 2.1, 2.2, 2.4, 4.1): im Hirn-Takt Liste B._fightLive und EINE Gegner-Suche (B.FoeScan) nach der Zombie-Suche; in
-- liveRec "am Boden" (B.DownStep) direkt nach der Laerm-Wache und der Kampf (B.FightStep) VOR der Zombie-Wache; im Langsam-Takt allein
-- aufstehen (B.DownSlow); handCheck / takeOne als B.HandCheck / B.TakeOne fuer Verband und Aufhelfen (server/BanditsNPCBearMend.lua,
-- ...Hurt.lua).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._brainAt = B._brainAt or nil      -- Echtzeit des letzten Hirn-Takts
B._scanAt = B._scanAt or nil        -- Echtzeit des letzten Suchlaufs
B._live = B._live or false          -- gab es beim letzten Hirn-Takt etwas zu tun (Eintraege, reife Koeder)?
B._pp = B._pp or {}                 -- [uid] = { x, y } Ort jedes Spielers beim letzten Hirn-Takt ("steht still")
B._sig = B._sig or {}               -- [uid] = Text: welche Jungen (mit OnlineID) der Spieler zuletzt in Reichweite hatte
B._orphAt = B._orphAt or nil        -- B1b: Echtzeit des letzten Suchlaufs, der die Waisen-Liste gefuehrt hat
B._ppAt = B._ppAt or nil            -- B1c: Echtzeit, zu der B._pp gemessen wurde (Tempo = Weg / echte Zeit, Takt ist bei Zombies schneller)

-- ---------------------------------------------------------------------------
-- Meldungen
-- ---------------------------------------------------------------------------
local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Welche Gruende eine Zahl tragen (Plan 6.2.6): Wartezeit in Stunden, Sperre in Tagen.
local WHY_T = {
    UI_BN_Bear_Why_FeedWait = "wait",
    UI_BN_Bear_Why_PetWait = "wait",
    UI_BN_Bear_Why_Locked = "days",
    UI_BN_Bear_Why_NameBad = "num",        -- B1b: Wert = B.CFG.nameMax (die Bitte "Rename" baut die Meldung selbst, Follow.lua)
    UI_BN_Bear_Why_CallWait = "num",       -- B1c: Wert = Minuten bis zum naechsten "Call to me" (die Bitte "Call" baut sie selbst, Ride.lua)
}

-- bd = "big" (wahlfrei): der grosse Koerper -- der Client zeigt dann die Big-Fassung ("bear" statt "cub", Nachbesserung F1 A3).
local function tellWhy(player, whyKey, whyVal, bd)
    if not player or whyKey == nil then return end
    local t = WHY_T[whyKey]
    local v = nil
    if t ~= nil then v = whyVal end
    local n = note(whyKey, t, v, "bad")
    if bd == "big" then n.bd = "big" end
    B.Tell(player, n)
end

local function tellKey(pkey, n, players)
    if pkey == nil then return end
    local p, _ = B.PlayerByKey(pkey, players)
    if p then B.Tell(p, n) end
end

local function isTame(st)
    return st == "tame" or st == "missing"
end

-- Schluessel der Spieler, die gerade da sind (Uhren des Langsam-Takts, Welt-Deckel B.CountWild).
local function onlineSet(players)
    local online = {}
    for i = 1, #players do online[players[i].key] = true end
    return online
end

-- Sicht eines Spielers bauen und schicken (Plan 5.6).
function B.PushView(player)
    if not player then return end
    B.SendView(player, B.BuildView(player))
end

-- Geaenderte Eintraege an die betroffenen Spieler: alle, die Schluessel finder / bond / owner, alle in B.CFG.tellDist um
-- einen geaenderten Ort. Hoechstens eine Sendung je Spieler und Takt (sent: schon bediente uid).
function B.FlushViews(players, sent)
    local d = B._dirty
    if not d or not d.any then return end
    players = players or B.Players()
    sent = sent or {}
    for i = 1, #players do
        local e = players[i]
        if not sent[e.uid] then
            local want = d.all or d.keys[e.key] == true
            if not want then
                for j = 1, d.n do
                    local sp = d.spots[j]
                    if B.DistXY(e.x, e.y, sp.x, sp.y) <= B.CFG.tellDist then
                        want = true
                        break
                    end
                end
            end
            if want then
                B.PushView(e.p)
                sent[e.uid] = true
            end
        end
    end
    B._dirty = { any = false, all = false, keys = {}, spots = {}, n = 0 }
end

-- ---------------------------------------------------------------------------
-- Erscheinen (Plan 5.1, 5.2): der EINE Weg, ein Junges in die Welt zu setzen. Rufer im Kern: Wald-Wurf und Koeder.
-- Rueckgabe: rec oder nil, why (Textschluessel oder ein kurzer Grund der Engine-Seite).
-- ---------------------------------------------------------------------------
function B.AppearFor(pkey, src, x, y, z)
    local reg = B.Reg()
    if not reg then return nil, "noreg" end
    if not B.IsWriter() then return nil, "nowriter" end
    if pkey == nil or x == nil or y == nil then return nil, "noargs" end
    local now = B.Now()
    local ok, why, _ = B.MayAppear(B.SlotsOf(pkey, now), now)
    if not ok then return nil, why end
    if B.CountWild(onlineSet(B.Players())) >= B.Opt("BearCubWorldCap") or B.CountRecs() >= B.CFG.maxRecs then
        return nil, "UI_BN_Bear_Why_Full"
    end
    x, y, z = math.floor(x), math.floor(y), math.floor(z or 0)
    local animal, cwhy = B.CreateCub(x, y, z)
    if not animal then return nil, cwhy end
    local rec, rwhy = B.NewRec(src, pkey, animal, x, y, z, now)
    if not rec then
        B.RemoveCub(animal)
        return nil, rwhy
    end
    if src == "bait" then
        rec.hx, rec.hy, rec.hz = x, y, z
    end
    B.Commit(rec)
    local players = B.Players()
    local p, e = B.PlayerByKey(pkey, players)
    if p then
        if src == "bait" then
            B.Tell(p, note("UI_BN_Bear_Bait_Came", nil, nil, "good"))
        else
            B.Tell(p, note("UI_BN_Bear_Note_Heard", "dir", B.DirOf(x - e.x, y - e.y), nil))
            rec.hintAt = now
        end
    end
    B.Log("appear " .. rec.id .. " " .. tostring(src) .. " for " .. tostring(pkey) .. " at " .. x .. "," .. y)
    B.FlushViews(players)
    return rec, nil
end

-- ---------------------------------------------------------------------------
-- Gemeinsame Pruefung von Fuettern und Streicheln (Plan 5.3 Schritt 1-2). Rueckgabe: rec oder nil (dann schon gemeldet).
-- Art-Frage: B.BodyKind (shared/BanditsNPCBear.lua; B1e: Junges UND grosser Koerper). isExistInTheWorld:
-- shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29. isDead am Tier:
-- server/Traps/STrapGlobalObject.lua:238. character:getSquare():DistTo(animal:getSquare()) < 3:
-- shared/TimedActions/Animals/ISPetAnimal.lua:6 (dieselbe Pruefung wie Vanillas Streicheln).
-- ---------------------------------------------------------------------------
local function handCheck(character, animal)
    if not B.IsWriter() or not character or not animal then return nil end
    local kind = B.BodyKind(animal)
    if not kind then return nil end
    if not animal:isExistInTheWorld() or animal:isDead() then
        tellWhy(character, "UI_BN_Bear_Why_Gone", nil, kind)
        return nil
    end
    local here = character:getSquare()
    local there = animal:getSquare()
    if not here or not there or here:DistTo(there) >= B.CFG.reach then
        tellWhy(character, "UI_BN_Bear_Why_Far")
        return nil
    end
    local rec, why = B.RecOf(animal)
    if not rec then
        if why == "full" then tellWhy(character, "UI_BN_Bear_Why_Full") else tellWhy(character, "UI_BN_Bear_Why_Gone", nil, kind) end
        return nil
    end
    return rec
end

-- Ein Stueck aus dem Inventar nehmen, genau so wie Vanilla in complete():
-- removeFromHands / getInventory():Remove / sendRemoveItemFromContainer: shared/Camping/TimedActions/ISAddFuelAction.lua:66-68.
-- contains: shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6. Rueckgabe true nur, wenn das Stueck danach WIRKLICH weg ist.
local function takeOne(character, food)
    local inv = character:getInventory()
    character:removeFromHands(food)
    inv:Remove(food)
    sendRemoveItemFromContainer(inv, food)
    if inv:contains(food) then
        B.Err("take: the item is still in the inventory after Remove, nothing credited")
        return false
    end
    return true
end

-- F2 (PLAN_F2.md 4.1, 4.3): dieselben Pruefungen fuer Verband (B.MendComplete) und Aufhelfen (B.HelpUpComplete) -- nur ausgefuehrt, nie
-- eingefangen (die Dateien rufen sie zur Laufzeit ueber B.X).
B.HandCheck = handCheck
B.TakeOne = takeOne

-- Ort des Tiers als ganze Kachel. getX/getY/getZ am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-577.
local function tileOf(animal)
    return math.floor(animal:getX()), math.floor(animal:getY()), math.floor(animal:getZ())
end

-- Meldungen nach einer Gutschrift (Plan 5.3 Schritt 7).
local function tellGain(character, res, class)
    local k = "UI_BN_Bear_Note_Gain"
    if res.mixed then
        k = "UI_BN_Bear_Note_GainMix"
    elseif class == "fav" then
        k = "UI_BN_Bear_Note_GainFav"
    end
    B.Tell(character, note(k, "num", math.floor(res.gain), "good"))
    if res.first then B.Tell(character, note("UI_BN_Bear_Note_FirstFed", nil, nil, "good")) end
    if res.tamed then B.Tell(character, note("UI_BN_Bear_Note_Tamed", nil, nil, "good")) end
    if res.need > 0 then B.Tell(character, note("UI_BN_Bear_Why_MoreFood", "num", res.need, nil)) end
end

-- ---------------------------------------------------------------------------
-- Fuettern (Plan 5.3). Gerufen aus BanditsNPCBearFeedAction:complete() -- im Mehrspieler auf dem Server mit dem Stueck
-- des SERVERS. Alle Pruefungen hier, nehmen und gutschreiben in EINEM Aufruf. Ablehnung: Meldung, false, nichts verbraucht.
-- ---------------------------------------------------------------------------
function B.FeedComplete(character, animal, food)
    if not food then return false end
    local rec = handCheck(character, animal)
    if not rec then return false end
    local pkey = B.PlayerKey(character)
    local now = B.Now()
    local ok, whyKey, whyVal = B.CheckFeed(rec, pkey, B.SlotsOf(pkey, now), now)
    if not ok then
        tellWhy(character, whyKey, whyVal, rec.body)    -- Big-Fassung, wo es eine gibt (F1 A3)
        return false
    end
    if not character:getInventory():contains(food) then
        tellWhy(character, "UI_BN_Bear_Why_NoItem")
        return false
    end
    local class, fwhy = B.FoodClass(food)
    if class == nil then
        tellWhy(character, fwhy or "UI_BN_Bear_Why_NotFood")
        return false
    end
    local wasTame = isTame(rec.st)
    if not takeOne(character, food) then return false end
    -- ab hier ist das Stueck weg: gutschreiben im selben Aufruf, ohne Engine-Wurf dazwischen
    local res = B.ApplyGain(rec, pkey, "feed", class, now)
    local x, y, z = tileOf(animal)
    rec.x, rec.y, rec.z = x, y, z
    -- F1 (PLAN_F1.md 2.3, 2.4; Zusatz "F1 KERN"): Sitz und Frei behalten ihren Mittelpunkt (die Stelle des Befehls) -- sonst wanderte der
    -- Kreis von "Frei" mit jeder Fuetterung; sonst wie bisher (Heimat = Stelle der Fuetterung)
    local keepHome = wasTame and (B.ModeOf(rec) == "sit" or B.ModeOf(rec) == "roam")
    if not keepHome then rec.hx, rec.hy, rec.hz = x, y, z end
    rec.idleH = 0
    rec.goneP = nil
    -- B1d (PLAN_B1D.md 1.1 Schritt 4): gutes Fuettern beschleunigt das Wachsen ein wenig (gedeckelt, server/BanditsNPCBearGrow.lua)
    if wasTame and B.GrowFeed then B.GrowFeed(rec, class, now) end
    B.Commit(rec)
    if wasTame then
        -- am zahmen Jungen nur Abklingzeit und Meldung (Plan 11), wie B.PetComplete (Nachbesserung B4)
        B.Tell(character, note("UI_BN_Bear_Note_Happy", nil, nil, "good"))
    else
        tellGain(character, res, class)
    end
    B.Log("feed " .. rec.id .. " " .. tostring(pkey) .. " +" .. tostring(res.gain) .. (res.mixed and " mix" or "")
        .. " " .. tostring(class) .. " tame " .. tostring(rec.tame) .. " st " .. tostring(rec.st))
    B.FlushViews()
    return true
end

-- ---------------------------------------------------------------------------
-- Streicheln (Plan 5.4). Kein Gegenstand im Spiel. Am gezaehmten Jungen nur Abklingzeit und "Es geniesst das".
-- animal:petAnimal(character): Vanilla shared/TimedActions/Animals/ISPetAnimal.lua:70 (in complete(), also Server / SP);
-- hebt die Engine-Akzeptanz (nicht der Balken), wirkt laut Jar nur bei abgelaufenem Vanilla-petTimer.
-- ---------------------------------------------------------------------------
function B.PetComplete(character, animal)
    local rec = handCheck(character, animal)
    if not rec then return false end
    local pkey = B.PlayerKey(character)
    local now = B.Now()
    local ok, whyKey, whyVal = B.CheckPet(rec, pkey, B.SlotsOf(pkey, now), now)
    if not ok then
        tellWhy(character, whyKey, whyVal, rec.body)    -- Big-Fassung, wo es eine gibt (F1 A3)
        return false
    end
    local wasTame = isTame(rec.st)
    local res = B.ApplyGain(rec, pkey, "pet", nil, now)
    animal:petAnimal(character)
    rec.idleH = 0
    rec.goneP = nil
    B.Commit(rec)
    if wasTame then
        B.Tell(character, note("UI_BN_Bear_Note_Happy", nil, nil, "good"))
    else
        tellGain(character, res, nil)
    end
    B.Log("pet " .. rec.id .. " " .. tostring(pkey) .. " +" .. tostring(res.gain) .. (res.mixed and " mix" or "")
        .. " tame " .. tostring(rec.tame) .. " st " .. tostring(rec.st))
    B.FlushViews()
    return true
end

-- ---------------------------------------------------------------------------
-- Koeder auslegen (Plan 5.2). Gerufen aus BanditsNPCBearBaitAction:complete(). Der Platz ist unsichtbar (Plan 0.4):
-- das Stueck wird verbraucht, der Platz steht nur im Register.
-- getCell():getGridSquare(x, y, z): Vanilla server/Animal/ISPickDungCursor.lua:104. square:DistTo(square): ISPetAnimal.lua:6.
-- ---------------------------------------------------------------------------
local function baitSpotWhy(character, x, y, z)
    local sq = getCell():getGridSquare(x, y, z)
    local here = character:getSquare()
    if sq == nil or here == nil or here:DistTo(sq) > B.CFG.baitReach then return "UI_BN_Bear_Why_Far" end
    local fits, _ = B.SquareFits(sq)
    if not fits then return "UI_BN_Bear_Bait_Inside" end
    if not B.NearForest(x, y, z, B.CFG.baitEdge) then return "UI_BN_Bear_Bait_NotForest" end
    return nil
end

local function baitTooClose(reg, x, y)
    for _, bait in pairs(reg.baits) do
        if B.DistXY(x, y, bait.x, bait.y) < B.CFG.baitApart then return true end
    end
    return false
end

function B.BaitComplete(character, food, x, y, z)
    local reg = B.Reg()
    if not reg or not B.IsWriter() or not character or not food then return false end
    x, y, z = tonumber(x), tonumber(y), tonumber(z)
    if x == nil or y == nil then return false end
    x, y, z = math.floor(x), math.floor(y), math.floor(z or 0)
    if B.Opt("BearBaitEnabled") ~= true then
        tellWhy(character, "UI_BN_Bear_Bait_Off")
        return false
    end
    local spotWhy = baitSpotWhy(character, x, y, z)
    if spotWhy then
        tellWhy(character, spotWhy)
        return false
    end
    local pkey = B.PlayerKey(character)
    local now = B.Now()
    local ok, whyKey, whyVal = B.CheckBait(B.SlotsOf(pkey, now), now)
    if not ok then
        tellWhy(character, whyKey, whyVal)
        return false
    end
    if B.CountBaits() >= B.CFG.maxBaits then
        tellWhy(character, "UI_BN_Bear_Why_Full")
        return false
    end
    if baitTooClose(reg, x, y) then
        tellWhy(character, "UI_BN_Bear_Bait_TooClose")
        return false
    end
    if not character:getInventory():contains(food) then
        tellWhy(character, "UI_BN_Bear_Why_NoItem")
        return false
    end
    local class, fwhy = B.FoodClass(food)
    if class == nil and fwhy == "UI_BN_Bear_Why_Rotten" then
        tellWhy(character, fwhy)
        return false
    end
    local isBait, kind = B.IsBaitFood(food)
    if not isBait then
        tellWhy(character, "UI_BN_Bear_Bait_BadFood")
        return false
    end
    if not takeOne(character, food) then return false end
    local bait = B.NewBait(pkey, x, y, z, kind, now, B.IsNight())
    if not bait then
        -- kann nur ohne Register passieren, das oben geprueft ist; trotzdem laut melden (Stueck ist weg)
        B.Err("bait: could not enter the spot after taking the food")
        return false
    end
    B.Tell(character, note("UI_BN_Bear_Bait_Placed", nil, nil, "good"))
    B.Log("bait " .. bait.id .. " " .. tostring(pkey) .. " " .. tostring(kind) .. " at " .. x .. "," .. y)
    B.FlushViews()
    return true
end

-- ---------------------------------------------------------------------------
-- Bitten der Clients (Plan 6.2.6). Im Einzelspieler ruft B.Ask diese Funktion direkt.
-- ---------------------------------------------------------------------------
function B.Handle(player, command, args)
    if not player or not B.IsWriter() then return end
    if type(args) ~= "table" then return end
    if command == "Hello" then
        B.PushView(player)
        return
    end
    if command == "BaitDrop" then
        local reg = B.Reg()
        if not reg then return end
        local pkey = B.PlayerKey(player)
        local bait = nil
        if type(args.id) == "string" then bait = reg.baits[args.id] end
        if bait and bait.owner == pkey then
            B.DropBait(bait)
            B.Tell(player, note("UI_BN_Bear_Bait_Dropped", nil, nil, nil))
            B.Log("bait " .. tostring(bait.id) .. " given up by " .. tostring(pkey))
        end
        B.PushView(player)
        return
    end
    -- B1b (PLAN_B1B.md 5.3): Folgen / Bleiben und Umbenennen pruefen die Bitten selbst (server/BanditsNPCBearFollow.lua)
    if command == "Mode" then
        if B.HandleMode then B.HandleMode(player, args) end
        return
    end
    if command == "Rename" then
        if B.HandleRename then B.HandleRename(player, args) end
        return
    end
    -- B1c (PLAN_B1C.md 1.5, 6.5): "Call to me" prueft die Bitte selbst (server/BanditsNPCBearRide.lua)
    if command == "Call" then
        if B.HandleCall then B.HandleCall(player, args) end
        return
    end
    -- F1 (PLAN_F1.md 2.5, 2.6, 7.3): "Komm her" und "Passiv" pruefen die Bitten selbst (server/BanditsNPCBearOrder.lua)
    if command == "Come" then
        if B.HandleCome then B.HandleCome(player, args) end
        return
    end
    if command == "Passive" then
        if B.HandlePassive then B.HandlePassive(player, args) end
        return
    end
end

-- Events.OnClientCommand.Add(function(module, command, player, args)): Vanilla server/ClientCommands.lua:1357; Filter auf das
-- eigene Modul zuerst wie server/Foraging/forageServer.lua:56-57.
-- Eine leer gesendete Tabelle kommt als nil an (Vanilla server/ClientCommands.lua:1349 "if args then", client/ServerCommands.lua:211);
-- deshalb nil wie {} behandeln (Nachbesserung B1). Jede Bitte prueft ihre Felder selbst.
local function onClientCommand(module, command, player, args)
    if module ~= B.CMD then return end
    if isClient() then return end
    if args == nil then args = {} end
    if type(args) ~= "table" then return end
    B.Handle(player, command, args)
end

-- ---------------------------------------------------------------------------
-- Koeder: ein Morgen (Plan 5.2). Steht jemand naeher als baitKeep, zaehlt die Nacht nicht. ZombRand(n): Vanilla
-- shared/TimedActions/Animals/ISMilkAnimal.lua:25.
-- ---------------------------------------------------------------------------
function B.BaitDawn(bait, now, players)
    if not bait or bait.ready then return end
    players = players or B.Players()
    local nd = B.NearestPlayerDist(bait.x, bait.y, players)
    if nd ~= nil and nd < B.CFG.baitKeep then
        bait.miss = (tonumber(bait.miss) or 0) + 1
        if bait.miss >= B.CFG.baitExtra then
            B.DropBait(bait)
            tellKey(bait.owner, note("UI_BN_Bear_Bait_Expired", nil, nil, "bad"), players)
            B.Log("bait " .. tostring(bait.id) .. " expired after " .. tostring(bait.miss) .. " disturbed mornings")
            return
        end
        if bait.warnAt == nil or now - bait.warnAt >= 24 then
            bait.warnAt = now
            tellKey(bait.owner, note("UI_BN_Bear_Bait_Near", nil, nil, nil), players)
        end
        B.Touch(nil, bait.owner)
        return
    end
    bait.nights = (tonumber(bait.nights) or 0) + 1
    local chance = B.BaitChance(bait.nights)
    if ZombRand(100) < chance then bait.ready = true end
    B.Touch(nil, bait.owner)
    B.Log("bait " .. tostring(bait.id) .. " night " .. tostring(bait.nights) .. " chance " .. tostring(chance)
        .. " ready " .. tostring(bait.ready))
end

-- ---------------------------------------------------------------------------
-- Langsam-Takt (Plan 7): alle 10 Spielminuten.
-- ---------------------------------------------------------------------------

-- Ist jemand (bei "fed": nur bond) innerhalb contactDist? Und ist der Spieler online, fuer den die Uhr laeuft?
local function contactOf(rec, players, online)
    local onlyKey = nil
    if rec.st == "fed" then onlyKey = rec.bond end
    local contact = false
    for i = 1, #players do
        local e = players[i]
        if (onlyKey == nil or e.key == onlyKey) and B.DistXY(rec.x, rec.y, e.x, e.y) <= B.CFG.contactDist then
            contact = true
            break
        end
    end
    local key = rec.finder
    if rec.st == "fed" then key = rec.bond end
    local relevant
    if key ~= nil then relevant = online[key] == true else relevant = #players > 0 end
    return contact, relevant
end

-- Wimmer-Hinweis an den Finder eines noch nicht entdeckten Jungen (hoechstens je B.CFG.hintH).
local function hint(rec, players, now)
    if rec.st ~= "new" or rec.finder == nil then return end
    if rec.hintAt ~= nil and now - rec.hintAt < B.CFG.hintH then return end
    local p, e = B.PlayerByKey(rec.finder, players)
    if not p then return end
    local d = B.DistXY(e.x, e.y, rec.x, rec.y)
    if d <= B.CFG.contactDist or d > B.CFG.hintDist then return end
    rec.hintAt = now
    B.Tell(p, note("UI_BN_Bear_Note_Heard", "dir", B.DirOf(rec.x - e.x, rec.y - e.y), nil))
end

-- F1 (PLAN_F1.md 0.8, 4b Nr. 6): ein VERMISSTER zahmer Baer wird nie mehr nach missingH als "lost" geschlossen (rote Linie "der Baer geht
-- nie verloren"; Unstuck und die Rueckkehr C1 holen ihn). missH zaehlt weiter (Diagnose, eine Zeile beim Ueberschreiten von missingH).
local function slowRec(rec, dt, players, online, now)
    -- F2 (PLAN_F2.md 2.4): am Boden -- nach BearDownedHours steht er allein auf (server/BanditsNPCBearHurt.lua)
    if rec.down ~= nil and B.DownSlow then B.DownSlow(rec, now, players) end
    if rec.st == "missing" then
        if rec.owner ~= nil and online[rec.owner] then
            local was = tonumber(rec.missH) or 0
            rec.missH = was + dt
            if was < B.CFG.missingH and rec.missH >= B.CFG.missingH then
                B.Log("missing " .. tostring(rec.id) .. " for " .. tostring(B.Round1(rec.missH))
                    .. " h -- kept (a tame bear is never lost)")
            end
        end
        return
    end
    local contact, relevant = contactOf(rec, players, online)
    if contact and rec.goneP then
        rec.goneP = nil
        B.Touch(rec)
    end
    local step = B.VanishStep(rec, dt, contact, relevant)
    if step == "go" and not rec.goneP then
        rec.goneP = true
        B.Touch(rec)
        B.Log("vanish due " .. rec.id .. " idle " .. tostring(rec.idleH) .. " h")
    elseif step == "release" then
        local old = B.ReleaseBond(rec)
        B.Commit(rec)
        tellKey(old, note("UI_BN_Bear_Note_Abandoned", nil, nil, "bad"), players)
        B.Log("abandoned " .. rec.id .. " by " .. tostring(old))
    end
    -- ein faelliges Junges in einer nicht geladenen Gegend ist ausser Sicht und weit weg: Eintrag schliessen. Das Tier
    -- (falls es im gespeicherten Gebiet steht) traegt dann einen Spiegel ohne Eintrag; B.ScanAnimals entfernt es, sobald
    -- es geladen und unbeobachtet ist.
    if rec.goneP and not B.AreaLoaded(rec.x, rec.y) then
        B.Close(rec, "vanish")
        return
    end
    hint(rec, players, now)
end

-- Wald-Wurf je Spielerschluessel (Plan 5.1): erst wuerfeln, nur bei Erfolg einen Platz suchen.
local function forestRolls(players, now)
    if B.Opt("BearCubsEnabled") ~= true then return end
    -- B1c (PLAN_B1C.md 1.1 Schritt 2): im Heil-Fenster nach dem Laden kein Wald-Wurf -- sonst bekaeme ein Spieler ein neues wildes
    -- Junges, bevor sein zahmes aus dem Spiegel zurueck ist. getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
    if getTimestampMs() < (B._healUntil or 0) then return end
    local pct = B.CFG.forestRate[B.Opt("BearCubForestRate")] or 0
    if pct <= 0 then return end
    local done = {}
    for i = 1, #players do
        local e = players[i]
        if not done[e.key] then
            done[e.key] = true
            local ok, _, _ = B.MayAppear(B.SlotsOf(e.key, now), now)
            if ok and B.CountWild(onlineSet(players)) < B.Opt("BearCubWorldCap") and ZombRand(10000) < pct * 100 / 6 then
                local sq = B.PickForestSquare(e, players)
                if sq then
                    -- square:getX(): Vanilla shared/Traps/TrapSystem.lua:12
                    B.AppearFor(e.key, "forest", sq:getX(), sq:getY(), sq:getZ())
                else
                    B.Log("forest roll for " .. tostring(e.key) .. " found no square")
                end
            end
        end
    end
end

-- Koeder: Nacht merken, beim Morgengrauen einen Morgen zaehlen.
local function baitNights(reg, players, now)
    local night = B.IsNight()
    local list = {}
    for _, bait in pairs(reg.baits) do list[#list + 1] = bait end
    for i = 1, #list do
        local bait = list[i]
        if night then
            bait.wasNight = true
        elseif bait.wasNight then
            bait.wasNight = false
            B.BaitDawn(bait, now, players)
        end
    end
end

local function slowTickBody()
    local reg = B.Reg()
    if not reg then return end
    local now = B.Now()
    local at = tonumber(reg.at)
    local dt = 0
    if at ~= nil then dt = now - at end
    if dt < 0 then dt = 0 end
    if dt > B.CFG.maxDtH then dt = B.CFG.maxDtH end
    reg.at = now
    local players = B.Players()
    local online = onlineSet(players)
    B.CleanLocks(now)
    local list = {}
    for _, rec in pairs(reg.cubs) do list[#list + 1] = rec end
    for i = 1, #list do
        local rec = list[i]
        if reg.cubs[rec.id] == rec then slowRec(rec, dt, players, online, now) end
    end
    forestRolls(players, now)
    baitNights(reg, players, now)
    -- B1d (PLAN_B1D.md 1.1 Schritt 2): Wachsen und Leben der gezaehmten Jungen (server/BanditsNPCBearGrow.lua). Nachbesserung B1d B2:
    -- eigene Schleife NACH den B1a-B1c-Schritten -- wirft ein B1d-Schritt (animal:getHealth() ist am Tier am MP-Server unbelegt,
    -- PLAN_B1D.md 8 Nr. 4), sind sie in diesem Takt schon durch; die Sicht bleibt in B._dirty und geht mit dem naechsten Hirn-Takt hinaus.
    if B.GrowSlow then
        for i = 1, #list do
            local rec = list[i]
            if reg.cubs[rec.id] == rec then B.GrowSlow(rec, dt, online, now, players) end
        end
    end
    B.FlushViews(players)
end

function B.SlowTick()
    -- pcall um EIGENEN Code (gilt auch fuer B.BrainTick): ein Fehler soll laut, aber gedrosselt kommen (B.ErrEvery) -- er wird
    -- nie verschluckt. Alle Engine-Aufrufe darin haben einen Vanilla-/Bandits-Beleg, mit EINER ehrlich offenen Ausnahme fuer den
    -- Mehrspieler-Server (A3 aus B1a): getCell():getObjectListForLua() im Suchlauf B.ScanAnimals und animal:getAnimalID()
    -- (B.FindAnimal, B.NewRec, Suchlauf) haben nur Client-Belege (Kommentar ueber B.ScanAnimals in server/BanditsNPCBearWorld.lua).
    -- Scheitert einer am Server, steht das im Log ("slow tick: ..." / "brain tick: ...") -- Testpunkt in Kevins MP-Test (PLAN_B1B.md
    -- 8.4 MP 7). Nachbesserung B1b A6. B1c haengt mehr daran (Nachbesserung B1c A2): der Suchlauf im Heil-Fenster (je healScanMs fuer
    -- healWindowMs nach jedem Laden), die Heilung, das Aussteigen und "Call to me" (getAnimalID beim Binden) -- PLAN_B1C.md 7.4 MP 8.
    -- pcall ist eine Lua-Grundfunktion (keine Engine-Methode; Vanilla und Bandits benutzen sie nicht),
    -- im gespielten NCTurretTest shared/BanditsNPCTurretCrew.lua:128 unter Kahlua in Gebrauch.
    local ok, err = pcall(slowTickBody)
    if not ok then B.ErrEvery("slow", 60000, "slow tick: " .. tostring(err)) end
end

-- ---------------------------------------------------------------------------
-- Hirn-Takt (Plan 6.7, 7): Verhalten, Kontakt, Tod, Verschwinden vollziehen, reife Koeder, Sicht.
-- ---------------------------------------------------------------------------

-- Hand und Tempo eines Spielers, je Takt einmal. getPrimaryHandItem: Vanilla server/BuildingObjects/ISEmptyGraves.lua:18.
-- isRunning / isSprinting: Vanilla client/Foraging/ISBaseIcon.lua:702, Bandits shared/PlayerDamageModel.lua:81.
local function playerInfo(e, cache)
    local info = cache[e.uid]
    if info then return info end
    local p = e.p
    local item = p:getPrimaryHandItem()
    local food = false
    if item ~= nil then food = (B.FoodClass(item) ~= nil) end
    local fast = p:isRunning() or p:isSprinting()
    local last = B._pp[e.uid]
    local still = last ~= nil and B.DistXY(last.x, last.y, e.x, e.y) < B.CFG.stillEps
    info = { key = e.key, x = e.x, y = e.y, food = food, fast = fast == true, still = still }
    cache[e.uid] = info
    return info
end

local function asP(info, d)
    return { key = info.key, x = info.x, y = info.y, dist = d, food = info.food, fast = info.fast, still = info.still }
end

-- Wer zaehlt als "Lock-Spieler" (Futter in der Hand), wer als "mate" (Finder / bond / Besitzer)?
local function keysOf(rec)
    if rec.st == "fed" then return rec.bond, rec.bond end
    if isTame(rec.st) then return rec.owner, rec.owner end
    return nil, rec.finder
end

-- Umgebung eines Jungen fuer B.Decide. Rueckgabe: env, Abstand des naechsten Spielers, dessen Eintrag.
-- B1b: beim gezaehmten Jungen zusaetzlich env.owner = naechster anwesender Besitzer { key, x, y, z, dist, car } (ohne
-- Abstandsgrenze; B.FollowDecide braucht den echten Abstand fuer "zu weit weg").
-- B1c (PLAN_B1C.md 1.6, 6.3): env.owner.dt = echte ms seit dem letzten Hirn-Takt (B._ppAt; 0 -> nil), fuer das Tempo des Besitzers.
local function buildEnv(rec, cx, cy, players, cache, ms)
    local cfg = B.CFG
    local lureKey, mateKey = keysOf(rec)
    local nearD, nearE = nil, nil
    local lureD, lureI = nil, nil
    local mateD, mateE = nil, nil
    local ownD, ownE = nil, nil
    local ownKey = nil
    if rec.st == "tame" then ownKey = rec.owner end
    for i = 1, #players do
        local e = players[i]
        local d = B.DistXY(cx, cy, e.x, e.y)
        if nearD == nil or d < nearD then nearD, nearE = d, e end
        if d <= cfg.lureDist and (lureKey == nil or e.key == lureKey) then
            local info = playerInfo(e, cache)
            if info.food and not info.fast and (lureD == nil or d < lureD) then lureD, lureI = d, info end
        end
        if mateKey ~= nil and e.key == mateKey and d <= cfg.mateDist and (mateD == nil or d < mateD) then mateD, mateE = d, e end
        if ownKey ~= nil and e.key == ownKey and (ownD == nil or d < ownD) then ownD, ownE = d, e end
    end
    local env = {}
    if nearE then
        if nearD <= cfg.contactDist then
            env.near = asP(playerInfo(nearE, cache), nearD)
        else
            env.near = { key = nearE.key, x = nearE.x, y = nearE.y, dist = nearD, food = false, fast = false, still = false }
        end
    end
    if lureI then env.lure = asP(lureI, lureD) end
    if mateE then env.mate = { key = mateE.key, x = mateE.x, y = mateE.y, dist = mateD, food = false, fast = false, still = false } end
    if ownE then
        -- mx/my (Nachbesserung B1b B2): Weg des Besitzers seit dem letzten Hirn-Takt (B._pp), fuer den Vorhalt in B.FollowDecide
        local last = B._pp[ownE.uid]
        local mx, my = 0, 0
        if last ~= nil then mx, my = ownE.x - last.x, ownE.y - last.y end
        local dt = nil
        if ms ~= nil and B._ppAt ~= nil and ms - B._ppAt > 0 then dt = ms - B._ppAt end
        env.owner = { key = ownE.key, x = ownE.x, y = ownE.y, z = ownE.z, dist = ownD, car = (ownE.car == true), mx = mx, my = my,
                      dt = dt }
    end
    return env, nearD, nearE
end

-- Entscheidung ausfuehren (Plan 6.7 "Ausfuehren").
local function steer(rec, a, d, ms)
    local s = B.Ses(rec.id)
    if d.act == "hold" then
        B.Hold(rec, a, true)
    elseif d.act == "flee" or d.act == "come" or d.act == "home" then
        local moved = B.MoveTo(rec, a, d.tx, d.ty, rec.z)
        if moved and d.rule == 5 then s.curiousAt = ms end
        if moved and d.lead then
            rec.hx, rec.hy = math.floor(d.tx), math.floor(d.ty)
        end
    elseif s.held then
        B.Hold(rec, a, false)
    end
end

-- Spiegel-Probe (B1b, PLAN_B1B.md 4.4): passt der Spiegel am Tier nicht mehr zum Eintrag, neu schreiben. Ein getModData je Takt.
-- getModData am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:596.
-- B1c (PLAN_B1C.md 2.2, 6.3): billig ueber B.MarkFresh (v, id, u, r); schreibt nur bei Abweichung (B.WriteMark), ein alter
-- B1a/B1b-Spiegel { id, st } wird so beim ersten Takt v2. Ohne server/BanditsNPCBearHeal.lua der B1b-Weg.
local function markProbe(rec, a)
    local md = a:getModData()
    local mark = md and md[B.MARK]
    local fresh = B.MarkFresh
    if fresh then
        if not fresh(rec, mark) then B.WriteMark(rec, a) end
        return
    end
    if type(mark) ~= "table" or mark.id ~= rec.id or mark.st ~= rec.st then B.Commit(rec) end
end

-- B1c (PLAN_B1C.md 0.7, 4.1): die Lage in der Sicht nachschicken, wenn sie sich um viewMoveTiles geaendert hat, hoechstens je
-- viewMoveMs -- nur an finder / bond / owner (Karte, Markierung). Mitfahrend: nie (kein Koerper, kein Symbol).
local function pushMoved(rec, ms)
    local s = B.Ses(rec.id)
    if s.vx == nil or s.vy == nil or s.vAt == nil or ms - s.vAt < 0 then
        s.vx, s.vy, s.vAt = rec.x, rec.y, ms
        return
    end
    if ms - s.vAt < B.CFG.viewMoveMs then return end
    if B.DistXY(s.vx, s.vy, rec.x, rec.y) < B.CFG.viewMoveTiles then return end
    s.vx, s.vy, s.vAt = rec.x, rec.y, ms
    if rec.finder ~= nil then B.Touch(nil, rec.finder) end
    if rec.bond ~= nil then B.Touch(nil, rec.bond) end
    if rec.owner ~= nil then B.Touch(nil, rec.owner) end
end

-- Ein geladenes, lebendes Junges.
local function liveRec(rec, a, players, cache, ms)
    local x, y, z = tileOf(a)
    rec.x, rec.y, rec.z = x, y, z
    rec.missN = 0
    rec.missAt = nil
    if rec.st == "missing" then
        rec.st = "tame"
        rec.missH = 0
        B.Commit(rec)
        tellKey(rec.owner, note("UI_BN_Bear_Note_Back", nil, nil, "good"), players)
    end
    markProbe(rec, a)
    pushMoved(rec, ms)
    -- B1c (PLAN_B1C.md 1.2 Schritt 1): gezaehmte Junge stehen auf der Laerm-Wache (server/BanditsNPCBearGuard.lua)
    if rec.st == "tame" and B.CalmWatch then B.CalmWatch(rec, a, ms) end
    -- F2 (PLAN_F2.md 2.4): am Boden haelt er still -- vor allem anderen (kein Kampf, kein Verstecken, kein Folgen, kein Befehl)
    if rec.st == "tame" and B.DownStep and B.DownStep(rec, a, ms) then return end
    local cx, cy = a:getX(), a:getY()
    -- B1d (B.GrowLive: Groesse, Leben, Ausdauer/Kondition) laeuft seit der Nachbesserung B1d B2 am Ende von brainTickBody
    local env, nearD, nearE = buildEnv(rec, cx, cy, players, cache, ms)
    local contact = nearD ~= nil and nearD <= B.CFG.contactDist
    if rec.goneP and contact then
        rec.goneP = nil
        B.Touch(rec)
    end
    if rec.goneP and (rec.st == "new" or rec.st == "shy") then
        if (nearD == nil or nearD >= B.CFG.vanishKeep) and not B.SeenInSP(a:getSquare(), players) then
            B.RemoveCub(a)
            B.Close(rec, "vanish")
            return
        end
    end
    if rec.st == "new" and contact then
        rec.st = "shy"
        B.Commit(rec)
        B.Tell(nearE.p, note("UI_BN_Bear_Note_Seen", nil, nil, "good"))
        B.Log("seen " .. rec.id .. " by " .. tostring(nearE.key))
    end
    -- F2 (PLAN_F2.md 2.2.1): der Kampf geht vor jedem Befehl und vor der Zombie-Wache (server/BanditsNPCBearFight.lua); false = kein Kampf
    -- (passiv, zu wenig Leben, verschnaufen, Junges ...) -> die Zombie-Wache versteckt ihn bzw. der Befehl gilt
    if rec.st == "tame" and B.FightStep and B.FightStep(rec, a, env, ms, players) then return end
    -- B1c (PLAN_B1C.md 1.3 Schritt 5): die Zombie-Wache geht vor Folgen und B.Decide (verstecken bzw. fliehen)
    if B.GuardStep and B.GuardStep(rec, a, env, ms, players) then return end
    -- F1 (PLAN_F1.md 2.3 Nr. 4, 5.4): verlaesst er einen Sitz, haelt er fuer das Aufstehen still (server/BanditsNPCBearOrder.lua)
    if rec.st == "tame" and B.StandStep and B.StandStep(rec, a, ms) then return end
    -- B1b (PLAN_B1B.md 1.2): ein folgendes gezaehmtes Junges rechnet B.FollowDecide statt B.Decide, ohne Gegenprobe B.MoveWatch
    if rec.st == "tame" and B.ModeOf(rec) == "follow" and B.FollowStep then
        B.FollowStep(rec, a, env, ms, players)
        return
    end
    -- F1 (PLAN_F1.md 5.4): Bleiben / Sitz / Frei rechnet B.OrderStep (server/BanditsNPCBearOrder.lua) statt B.Decide; fehlt die Datei,
    -- gilt der B1b-Weg darunter (Bleiben im Radius stayR)
    if rec.st == "tame" and B.OrderStep and B.OrderStep(rec, a, env, ms, players) then return end
    local s = B.Ses(rec.id)
    local big = B.CFG.curiousMs + 1
    local c = {
        st = rec.st, src = rec.src, x = cx, y = cy, hx = rec.hx, hy = rec.hy, held = s.held,
        sinceMoveMs = (s.moveAt ~= nil) and (ms - s.moveAt) or big,
        sinceCuriousMs = (s.curiousAt ~= nil) and (ms - s.curiousAt) or big,
    }
    -- B1b (PLAN_B1B.md 1.4): Bleiben -- das gezaehmte Junge bleibt in B.CFG.stayR um die Heimat ("fed" weiter B.CFG.homeR)
    if rec.st == "tame" then c.homeR = B.CFG.stayR end
    local d = B.Decide(c, env)
    steer(rec, a, d, ms)
    B.MoveWatch(rec, a)
end

-- Erster Durchgang: Tod sehen, Objekte holen, entscheiden, ob ein Suchlauf noetig ist. Rueckgabe: Liste ohne Objekt, Suchlauf
-- (je B.CFG.scanMs), Suchlauf nur fuer vermisste Zahme (seltener, je scanMs x B.CFG.missScanMul; Nachbesserung B6).
-- B1c (PLAN_B1C.md 3.3): ein mitfahrendes Junges (rec.ride) hat absichtlich kein Objekt -- nie "fehlt", nie "missing".
local function resolve(list)
    local missing = {}
    local need = false
    local needSlow = false
    for i = 1, #list do
        local rec = list[i]
        local s = B._s[rec.id]
        local o = s and s.obj
        if rec.ride ~= nil then
            -- faehrt mit: nichts zu suchen (B.RideStep lief vorher)
        elseif o ~= nil and o:isDead() then
            -- Tod nur am in dieser Sitzung gemerkten Objekt (Plan 0.8); "fehlt" ist nie "tot"
            B.Close(rec, "dead")
        elseif B.FindAnimal(rec) == nil then
            missing[#missing + 1] = rec
            if B.AreaLoaded(rec.x, rec.y) then
                if rec.st == "missing" then needSlow = true else need = true end
            elseif rec.st == "missing" and s ~= nil and s.revAt ~= nil and B.ReviveForget then
                -- Nachbesserung F1 B1: Gegend nicht geladen -> die C1-Wartefrist beginnt beim naechsten geladenen Suchlauf neu
                B.ReviveForget(rec)
            end
        end
    end
    return missing, need, needSlow
end

-- Nach einem Suchlauf: wer immer noch fehlt und dessen Gegend geladen ist, bekommt einen Fehlversuch. Ein angefuettertes
-- Junges ("fed", bond und Balken haengen daran) wird erst geschlossen, wenn es AUCH seit B.CFG.fedMissH Spielstunden fehlt:
-- Tiere kommen nach den Kacheln ueber einen eigenen Lader zurueck (FE 1.4, Dauer ungeprueft). Nachbesserung B3.
local function countMisses(missing, players, now)
    for i = 1, #missing do
        local rec = missing[i]
        if B.Reg().cubs[rec.id] == rec and rec.ride == nil and B.FindAnimal(rec) == nil and rec.st ~= "missing"
            and B.AreaLoaded(rec.x, rec.y) then
            rec.missN = (tonumber(rec.missN) or 0) + 1
            if tonumber(rec.missAt) == nil then rec.missAt = now end
            local longEnough = rec.st ~= "fed" or now - tonumber(rec.missAt) >= B.CFG.fedMissH
            if rec.missN >= B.CFG.missScans and longEnough then
                if rec.st == "tame" then
                    rec.st = "missing"
                    rec.missH = 0
                    rec.missN = 0
                    rec.missAt = nil
                    -- F1 (PLAN_F1.md 4b): die Wartefrist der Rueckkehr (C1) beginnt hier neu
                    local s = B._s[rec.id]
                    if s ~= nil then s.revN, s.revFail = nil, nil end
                    -- B1b (PLAN_B1B.md 1.3): ein vermisstes Junges folgt nicht mehr -- still auf "Bleiben", Heimat = letzte Kachel
                    if B.ModeOf(rec) == "follow" then
                        if B.SetMode then B.SetMode(rec, "stay", "missing", players) else rec.mode = "stay" end
                    end
                    B.Commit(rec)
                    tellKey(rec.owner, note("UI_BN_Bear_Note_Missing", nil, nil, "bad"), players)
                else
                    B.Close(rec, "lost")
                end
            end
        end
    end
end

-- Reife Koeder: Junges erscheinen lassen, wenn die Kachel geladen ist und niemand nah ist / hinsieht.
local function baitAppear(reg, players)
    local list = {}
    for _, bait in pairs(reg.baits) do
        if bait.ready then list[#list + 1] = bait end
    end
    local due = (B.Opt("BearBaitNights") + B.CFG.baitExtra + 1) * 24      -- Spielstunden ab dem Auslegen (Nachbesserung B5)
    local nowH = B.Now()
    for i = 1, #list do
        local bait = list[i]
        local sq = getCell():getGridSquare(bait.x, bait.y, bait.z)
        local nd = B.NearestPlayerDist(bait.x, bait.y, players)
        local t0 = tonumber(bait.t0)
        if t0 ~= nil and nowH - t0 >= due then
            -- ein reifer Platz haengt nicht still (Plan 5.2): kam das Junge in dieser Frist nicht (Kachel nie geladen, Besitzer
            -- hat noch ein Junges ...), verfaellt der Platz mit Meldung -- auch fuer abwesende Besitzer (Deckel maxBaits)
            B.DropBait(bait)
            tellKey(bait.owner, note("UI_BN_Bear_Bait_Expired", nil, nil, "bad"), players)
            B.Log("bait " .. tostring(bait.id) .. " expired while ready")
        elseif sq ~= nil and (nd == nil or nd >= B.CFG.baitAppear) and not B.SeenInSP(sq, players) then
            local now = B.Now()
            local ok, why, _ = B.MayAppear(B.SlotsOf(bait.owner, now), now)
            if not ok and why ~= "UI_BN_Bear_Why_HasCub" then
                -- Besitzer nicht mehr berechtigt (Baer, Sperre, ausgeschaltet): Platz verfaellt mit Meldung
                B.DropBait(bait)
                tellKey(bait.owner, note("UI_BN_Bear_Bait_Expired", nil, nil, "bad"), players)
            elseif ok then
                local spot = B.FreeSquareNear(bait.x, bait.y, bait.z, B.CFG.baitRing, players)
                if spot then
                    local rec, _ = B.AppearFor(bait.owner, "bait", spot:getX(), spot:getY(), spot:getZ())
                    if rec then
                        rec.hx, rec.hy, rec.hz = bait.x, bait.y, bait.z
                        B.Commit(rec)
                        B.DropBait(bait)
                    end
                end
            end
        end
    end
end

-- Eine Sicht nachschicken, wenn ein Spieler neu in die Reichweite eines Jungen kommt oder sich dessen OnlineID aendert.
local function pushNewSights(reg, players, oids)
    local sent = {}
    local sigs = {}
    for i = 1, #players do
        local e = players[i]
        local parts = {}
        for id, rec in pairs(reg.cubs) do
            if B.DistXY(e.x, e.y, rec.x, rec.y) <= B.CFG.tellDist then
                parts[#parts + 1] = id .. "@" .. tostring(oids[id] or -1)
            end
        end
        if #parts > 1 then table.sort(parts) end
        local sig = table.concat(parts, ",")
        -- auch beim ERSTEN Takt eines Spielers (B._sig[uid] nil): ein neu verbundener Spieler bekommt so seine Sicht, selbst wenn
        -- sein "Hello" verloren ging (Nachbesserung B1)
        if B._sig[e.uid] ~= sig then
            B.PushView(e.p)
            sent[e.uid] = true
        end
        sigs[e.uid] = sig
    end
    B._sig = sigs                      -- nur die Spieler von jetzt: waechst nicht
    return sent
end

-- B1c-Reihenfolge (PLAN_B1C.md 6.3): 1 Mitfahrende (B.RideStep), 2 resolve / Folgen ohne Objekt / B1a-Suchlauf, 3 Heil-Fenster-
-- Suchlauf, 4 Liste der geladenen Jungen -> EINE Zombie-Suche (B.GuardScan), 5 liveRec je Junges, 6 Spieler-Orte und deren Zeit
-- (B._pp, B._ppAt). Restliche Schritte wie B1b. B1d: 7 B.GrowLive je Junges als allerletzter Schritt (Nachbesserung B1d B2).
local function brainTickBody(ms)
    local reg = B.Reg()
    if not reg then return end
    local players = B.Players()
    local list = {}
    for _, rec in pairs(reg.cubs) do list[#list + 1] = rec end
    -- 1: mitfahrende Junge (server/BanditsNPCBearRide.lua)
    if B.RideStep then
        for i = 1, #list do
            local rec = list[i]
            if reg.cubs[rec.id] == rec and rec.ride ~= nil then B.RideStep(rec, players, ms) end
        end
    end
    local missing, need, needSlow = resolve(list)
    -- B1b (PLAN_B1B.md 1.3): ein folgendes Junges ohne Objekt in nicht geladener Gegend wartet dort
    if B.FollowLost then
        for i = 1, #missing do
            local rec = missing[i]
            if reg.cubs[rec.id] == rec then B.FollowLost(rec, players) end
        end
    end
    local scanned = false
    local every = B.CFG.scanMs
    if not need then every = B.CFG.scanMs * B.CFG.missScanMul end
    if (need or needSlow) and (B._scanAt == nil or ms - B._scanAt < 0 or ms - B._scanAt >= every) then
        B._scanAt = ms
        B._orphAt = ms                 -- dieser Suchlauf fuehrt die Waisen-Liste mit (B.ScanAnimals)
        scanned = true
        -- F1 (PLAN_F1.md 4b): wer schon VOR diesem Suchlauf vermisst war (der Suchlauf, der "missing" setzt, zaehlt nicht mit)
        local wasMissing = {}
        for i = 1, #missing do
            if missing[i].st == "missing" then wasMissing[#wasMissing + 1] = missing[i] end
        end
        B.ScanAnimals(players)
        countMisses(missing, players, B.Now())
        -- F1 C1 (PLAN_F1.md 0.8, 4b): ein vermisster Baer in geladener Gegend bekommt nach reviveScans vergeblichen Suchlaeufen genau EINEN
        -- neuen Koerper (server/BanditsNPCBearOrder.lua; hoechstens einer je Takt)
        if B.ReviveMissing and #wasMissing > 0 then B.ReviveMissing(wasMissing, players, ms) end
    end
    -- 3: Heil-Fenster nach InitRegistry (PLAN_B1C.md 1.1 Schritt 2, 2.6): je healScanMs ein Suchlauf, auch ohne Vermisste -- die
    -- Zellen laden nach, und ein Junges mit Spiegel ohne Eintrag kommt so zurueck. Fuehrt die Waisen-Liste mit (B._orphAt).
    if not scanned and ms < (B._healUntil or 0)
        and (B._healScanAt == nil or ms - B._healScanAt < 0 or ms - B._healScanAt >= B.CFG.healScanMs) then
        B._healScanAt = ms
        B._orphAt = ms
        scanned = true
        B.ScanAnimals(players)
    end
    -- 4: geladene, lebende Junge dieses Takts; EINE Zombie-Suche fuer alle (server/BanditsNPCBearGuard.lua)
    -- getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576
    -- F1 (PLAN_F1.md 5.3): Sicht nachschicken, wenn ein Baer geladen/entladen wird (ld) oder seine Beschaeftigt-Marke von selbst ablief
    -- (busy; B.BodyBusy meldet An/Aus selbst) -- je Wechsel EIN B.Touch, nie je Takt ohne Wechsel.
    local busySpan = tonumber(B.CFG.busyMs) or 20000
    local loaded = {}
    local fightLive = {}
    for i = 1, #list do
        local rec = list[i]
        if reg.cubs[rec.id] == rec then
            local a = B.FindAnimal(rec)
            if a then
                loaded[#loaded + 1] = { rec = rec, a = a, x = a:getX(), y = a:getY(), z = rec.z }
                -- F2 (PLAN_F2.md 2.1.1, 4.2): gezaehmt, geladen, nicht mitfahrend -> Gegner-Suche und Kampf-Takt (Deckel 64)
                if rec.st == "tame" and rec.ride == nil and #fightLive < 64 then fightLive[#fightLive + 1] = loaded[#loaded] end
            end
            local s = B._s[rec.id]
            local ld = a ~= nil
            if (s ~= nil and s.ldSent == true) ~= ld then
                B.Ses(rec.id).ldSent = ld
                B.Touch(rec)
            end
            if s ~= nil and s.busySent == true then
                local left = (tonumber(s.busyUntil) or 0) - ms
                if not (left > 0 and left <= busySpan) then
                    s.busySent = nil
                    B.Touch(rec)
                end
            end
        end
    end
    if B.GuardScan then B.GuardScan(loaded, ms) end
    -- F2 (PLAN_F2.md 2.1.1): EINE Gegner-Suche fuer alle gezaehmten Baeren direkt nach der Zombie-Suche (mischt feindliche Banditen in
    -- B._zed, server/BanditsNPCBearFightFoes.lua)
    B._fightLive = fightLive
    if B.FoeScan then B.FoeScan(fightLive, ms, true) end
    -- 5: je Junges
    local cache = {}
    local oids = {}
    for i = 1, #loaded do
        local e = loaded[i]
        local rec = e.rec
        if reg.cubs[rec.id] == rec then
            liveRec(rec, e.a, players, cache, ms)
            -- getOnlineID am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:614 (isServer-Zweig); eingestiegen: kein Tier mehr
            if reg.cubs[rec.id] == rec and rec.ride == nil then oids[rec.id] = e.a:getOnlineID() end
        end
    end
    baitAppear(reg, players)
    -- 6: Spieler-Orte und ihre Echtzeit (Tempo des Besitzers fuer Gehen und Aussteigen)
    local pp = {}
    for i = 1, #players do pp[players[i].uid] = { x = players[i].x, y = players[i].y } end
    B._pp = pp
    B._ppAt = ms
    local sent = pushNewSights(reg, players, oids)
    B.FlushViews(players, sent)
    local live = B.CountRecs() > 0
    if not live then
        for _, bait in pairs(reg.baits) do
            if bait.ready then live = true end
        end
    end
    -- B1c: im Heil-Fenster laeuft der Takt je brainMs (sonst idleMs 10 s -> Suchlauf nur je 20 s statt healScanMs 15 s, gerade im
    -- Fall "Register leer"); das Fenster ist nach healWindowMs zu
    if not live and ms < (B._healUntil or 0) then live = true end
    B._live = live
    -- B1b (PLAN_B1B.md 4.3, N5): eigener seltener Waisen-Suchlauf je B.CFG.orphanScanMs, auch ohne Eintraege und ohne Vermisste --
    -- nur, wenn in diesem Takt noch kein Suchlauf war. Am ENDE des Takts und mit vorher gestellter Uhr. Mehrspieler-Server:
    -- getObjectListForLua hat dort keinen Vanilla-/Bandits-Beleg (A3 aus B1a, offen). Der pcall in B.BrainTick versteckt einen
    -- Fehler NICHT: er steht je 60 s als "brain tick: ..." im Log (B.ErrEvery) und ist Kevins MP-Testpunkt (PLAN_B1B.md 8.4 MP 7:
    -- Server 3 min ohne Junges laufen lassen). Weil dieser Lauf auch ohne Junges kommt, zeigt sich A3 dort spaetestens nach 2 min.
    -- Nachbesserung B1b A6.
    if not scanned and (B._orphAt == nil or ms - B._orphAt < 0 or ms - B._orphAt >= B.CFG.orphanScanMs) then
        B._orphAt = ms
        B.ScanAnimals(players)
    end
    -- 7 (B1d, PLAN_B1D.md 1.1 Schritt 3): je geladenem, gezaehmtem Jungen B.GrowLive (server/BanditsNPCBearGrow.lua) -- Groesse
    -- nachsetzen, fehlendes Leben holen, Ausdauer/Kondition. Nachbesserung B1d B2: als LETZTER Schritt, damit ein B1d-Fehler
    -- (animal:getHealth() ist am Tier am MP-Server unbelegt, PLAN_B1D.md 8 Nr. 4) Folgen, Verstecken, Koeder, Sichten und Suchlaeufe nicht
    -- mitreisst; was GrowLive in die Sicht legt, geht mit dem naechsten Takt hinaus. Nur, wer noch derselbe Eintrag mit demselben Objekt
    -- ist (nicht geschlossen, nicht eingestiegen, nicht an einen anderen Koerper gebunden); Ort aus Schritt 4 (e.x, e.y, dieser Takt).
    if B.GrowLive then
        for i = 1, #loaded do
            local e = loaded[i]
            local rec = e.rec
            local s = B._s[rec.id]
            if reg.cubs[rec.id] == rec and rec.st == "tame" and rec.ride == nil and s ~= nil and s.obj == e.a then
                B.GrowLive(rec, e.a, e.x, e.y, ms)
            end
        end
    end
end

-- force ueberspringt nur die Echtzeit-Drossel. getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
function B.BrainTick(force)
    local ms = getTimestampMs()
    if not force and B._brainAt ~= nil and ms - B._brainAt >= 0 then
        local every = B.CFG.idleMs
        if B._live then every = B.CFG.brainMs end
        -- B1c (PLAN_B1C.md 0.5, 1.3 Schritt 6): steht ein Zombie in zedSense eines Jungen, rechnet der Takt schneller
        if B._hot then every = B.CFG.zedTickMs end
        if ms - B._brainAt < every then return end
    end
    B._brainAt = ms
    local ok, err = pcall(brainTickBody, ms)          -- pcall: siehe B.SlowTick
    if not ok then B.ErrEvery("brain", 60000, "brain tick: " .. tostring(err)) end
end

-- ---------------------------------------------------------------------------
-- Takte einhaengen. Events.EveryTenMinutes.Add: Vanilla server/Traps/STrapSystem.lua:134. Events.OnTick.Add: Vanilla
-- server/Foraging/forageServer.lua:502 (mit Echtzeit-Drossel :455-461). Ueber kleine Huellen, damit spaeter ersetzte
-- Funktionen (B.SlowTick, B.BrainTick) gelten.
-- ---------------------------------------------------------------------------
Events.EveryTenMinutes.Add(function() B.SlowTick() end)
Events.OnTick.Add(function() B.BrainTick(false) end)
Events.OnClientCommand.Add(onClientCommand)
