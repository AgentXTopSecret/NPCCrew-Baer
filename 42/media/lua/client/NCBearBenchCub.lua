--
-- TESTHILFE fuer das Baeren-Junge (B1a, PLAN_ZAEHMEN.md Abschnitt 8). Wird NICHT nach NPC Crew kopiert. Kein Kern-Code ruft
-- diese Datei; sie ruft dieselben Kern-Funktionen wie das echte Spiel (BanditsNPC.Bear) und aendert sonst nur Register-Felder.
--
-- NUR EINZELSPIELER: im Mehrspieler druckt jeder Befehl "singleplayer only" (dort testet man ueber die Sandbox-Werte).
--
-- Konsole:
--   NCBear_CubHere(n)        Junges n Kacheln (Vorgabe 8) neben mir erscheinen lassen -- ueber B.AppearFor, also mit denselben
--                            Regeln wie im Spiel (habe ich schon einen Baeren, lehnt es mit Grund ab)
--   NCBear_CubFood()         2 Honig, 3 Barsche, 3 Steaks ins Inventar
--   NCBear_CubTame(x)        Balken des naechsten Jungen auf x (0..100); bei 100 gilt es als fertig gezaehmt
--   NCBear_CubSkip(h)        h Spielstunden ueberspringen: Abklingzeiten, Verschwinde-Uhr, Sperre, Vermisst-Uhr.
--                            ACHTUNG: stehe ich naeher als 15 Kacheln am Jungen, setzt der Kontakt die Verschwinde-Uhr sofort
--                            wieder auf 0 -- zum Testen des Verschwindens ERST weggehen, DANN ueberspringen
--   NCBear_CubNight(force)   ein Morgen fuer meinen Koederplatz; NCBear_CubNight(true) macht ihn sofort reif
--   NCBear_CubInfo()         Zustand drucken (Sandbox-Werte, meine Plaetze, alle Eintraege mit Abstand, Koeder, Sicht)
--   NCBear_CubKill()         naechstes Junges toeten (Tod und Sperre pruefen)
--   NCBear_CubClean()        alle Jungen in der geladenen Gegend entfernen, Register leeren (auch Koeder und Sperren)
--   NCBear_CubLog(on)        Diagnose-Zeilen [TC-BEAR] an/aus
--   NCBear_CubSet(feld, wert) einen Stellwert aus B.CFG aendern (z. B. "barZ", "petAnim", "shyDist"); gilt bis zum Spielende
-- Rechtsklick auf eine Kachel, Untermenue "NC Bear": fuenf Eintraege "Cub: ...". Texte hier sind englische Literale.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function out(text)
    print("[NCBear] " .. tostring(text))
end

-- Kurze Rueckmeldung: Konsole und ueber der Figur. getSpecificPlayer(0): client/Farming/CFarmingSystem.lua:45;
-- player:Say(Text): client/Entity/ISEntityUI.lua:458.
local function say(text)
    out(text)
    local p = getSpecificPlayer(0)
    if p then p:Say(tostring(text)) end
end

-- Spieler, Schluessel und Register -- oder nil mit einer klaren Zeile.
local function ready()
    -- Erst der Modus: auf einem MP-Client gibt es die Schreiber-Funktionen (B.Reg ...) gar nicht.
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return nil
    end
    if not B.IsSP or not B.Reg then
        out("the bear core is not loaded (BanditsNPCBear*.lua)")
        return nil
    end
    local p = getSpecificPlayer(0)
    if not p then
        out("no player yet")
        return nil
    end
    local reg = B.Reg()
    if not reg then
        out("registry not ready yet (load a game first)")
        return nil
    end
    return p, B.PlayerKey(p), reg
end

local function push(p)
    if B.PushView then B.PushView(p) end
end

-- Grund als Text: Textschluessel werden uebersetzt, kurze Codes bleiben, wie sie sind.
local function whyText(why, val)
    if type(why) == "string" and string.sub(why, 1, 3) == "UI_" and B.UI and B.UI.WhyText then
        return B.UI.WhyText(why, val)
    end
    return tostring(why)
end

local function num(v)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%.1f", v)
end

-- ---------------------------------------------------------------------------
-- Befehle
-- ---------------------------------------------------------------------------

function NCBear_CubHere(n)
    local p, key = ready()
    if not p then return nil end
    n = math.floor(tonumber(n) or 8)
    if n < 1 then n = 1 end
    if n > 40 then n = 40 end
    local here = p:getCurrentSquare()                   -- client/ISUI/ISWorldObjectContextMenu.lua:112
    if not here then
        out("player has no square")
        return nil
    end
    local cx, cy, cz = here:getX(), here:getY(), here:getZ()
    local ring = { { n, 0 }, { 0, n }, { -n, 0 }, { 0, -n }, { n, n }, { -n, n }, { n, -n }, { -n, -n } }
    local lastWhy = "unloaded"
    for i = 1, #ring do
        -- getCell():getGridSquare(x, y, z), nil = nicht geladen: server/Animal/ISPickDungCursor.lua:104
        local sq = getCell():getGridSquare(cx + ring[i][1], cy + ring[i][2], cz)
        local fits, why = B.SquareFits(sq)
        if fits then
            local rec, refused = B.AppearFor(key, "forest", sq:getX(), sq:getY(), sq:getZ())
            if not rec then
                say("no cub: " .. whyText(refused))
                return nil
            end
            push(p)
            say("cub " .. tostring(rec.id) .. " appeared " .. n .. " tiles away")
            return rec
        end
        lastWhy = why
    end
    say("no free outdoor square " .. n .. " tiles around you (" .. tostring(lastWhy) .. ")")
    return nil
end

function NCBear_CubFood()
    local p = ready()
    if not p then return end
    local inv = p:getInventory()
    -- inv:AddItem("Base.X"): client/Tests/RecipeTests.lua:317. Namen: scripts/generated/items/food.txt (Honey, LargemouthBass, Steak).
    for _ = 1, 2 do inv:AddItem("Base.Honey") end
    for _ = 1, 3 do inv:AddItem("Base.LargemouthBass") end
    for _ = 1, 3 do inv:AddItem("Base.Steak") end
    say("food added: 2 honey, 3 bass, 3 steaks")
end

function NCBear_CubTame(x)
    local p, key = ready()
    if not p then return end
    x = tonumber(x) or 100
    if x < 0 then x = 0 end
    if x > 100 then x = 100 end
    local rec = B.NearestRec(p, 60)
    if not rec then
        say("no cub entry within 60 tiles")
        return
    end
    local now = B.Now()
    if x >= 100 and rec.owner ~= key then
        local slots = B.SlotsOf(key, now)
        if slots.bears >= slots.maxBears then
            say("refused: you already have a bear (NCBear_CubClean() or raise the sandbox value)")
            return
        end
        if slots.bonded ~= nil and slots.bonded ~= rec.id then
            say("refused: you are already taming cub " .. tostring(slots.bonded))
            return
        end
    end
    rec.tame = x
    if x >= 100 then
        rec.bond = key
        if rec.st ~= "tame" then rec.st = "fed" end
        local minFeed = B.Opt("BearTameMinFeedings") or 0
        if (tonumber(rec.fedN) or 0) < minFeed then rec.fedN = minFeed end
        -- wie nach einer echten ersten Fuetterung: Heimat = letzte bekannte Kachel
        if rec.hx == nil then
            rec.hx, rec.hy, rec.hz = rec.x, rec.y, rec.z
        end
    end
    local tamed = B.TameCheck(rec, now)
    B.Commit(rec)
    push(p)
    say("cub " .. tostring(rec.id) .. ": bar " .. num(rec.tame) .. ", state " .. tostring(rec.st) .. ", tamed " .. tostring(tamed))
end

function NCBear_CubSkip(h)
    local p, _, reg = ready()
    if not p then return end
    h = tonumber(h) or 2
    if h <= 0 then
        out("NCBear_CubSkip(h): h must be above 0")
        return
    end
    local n = 0
    for _, rec in pairs(reg.cubs) do
        if rec.feedAt ~= nil then rec.feedAt = rec.feedAt - h end
        if rec.petAt ~= nil then rec.petAt = rec.petAt - h end
        if rec.hintAt ~= nil then rec.hintAt = rec.hintAt - h end
        rec.idleH = (tonumber(rec.idleH) or 0) + h
        if rec.st == "missing" then rec.missH = (tonumber(rec.missH) or 0) + h end
        B.Commit(rec)
        n = n + 1
    end
    for _, prec in pairs(reg.players) do
        if type(prec) == "table" and prec.lockUntil ~= nil then prec.lockUntil = prec.lockUntil - h end
    end
    for _, bait in pairs(reg.baits) do
        if type(bait) == "table" and bait.warnAt ~= nil then bait.warnAt = bait.warnAt - h end
    end
    B.SlowTick()
    B.BrainTick(true)
    push(p)
    say("skipped " .. num(h) .. " h for " .. n .. " cub entr" .. ((n == 1) and "y" or "ies"))
    for _, rec in pairs(reg.cubs) do
        if rec.st == "new" or rec.st == "shy" then
            out("  " .. tostring(rec.id) .. " " .. tostring(rec.st) .. ": idle " .. num(rec.idleH) .. " h, leaving " .. tostring(rec.goneP == true)
                .. " (contact within 15 tiles resets the clock: step away first, then skip)")
        end
    end
end

function NCBear_CubNight(force)
    local p, key, reg = ready()
    if not p then return end
    local bait = nil
    for _, b in pairs(reg.baits) do
        if type(b) == "table" and b.owner == key then bait = b end
    end
    if not bait then
        say("you have no bait spot")
        return
    end
    local bid = bait.id
    if force then
        bait.ready = true
        if B.Touch then B.Touch() end
    else
        B.BaitDawn(bait, B.Now())
    end
    B.BrainTick(true)
    push(p)
    local left = reg.baits[bid]
    if left then
        say("bait " .. tostring(bid) .. ": nights " .. tostring(left.nights) .. ", missed " .. tostring(left.miss) .. ", ready "
            .. tostring(left.ready == true) .. (left.ready and " (a cub appears once you are 20+ tiles away and not looking)" or ""))
    else
        say("bait " .. tostring(bid) .. " is used up (cub appeared or bait expired)")
    end
end

local function infoRec(p, rec, now)
    local dx = (tonumber(rec.x) or 0) - p:getX()        -- client/Fishing/TensionUI.lua:11
    local dy = (tonumber(rec.y) or 0) - p:getY()
    local d = math.sqrt(dx * dx + dy * dy)
    local a = B.FindAnimal(rec)
    out("  " .. tostring(rec.id) .. " " .. tostring(rec.st) .. " src " .. tostring(rec.src) .. " bar " .. num(rec.tame)
        .. " fed " .. tostring(rec.fedN) .. " pet " .. tostring(rec.petN) .. " last " .. tostring(rec.last)
        .. " finder " .. tostring(rec.finder) .. " bond " .. tostring(rec.bond) .. " owner " .. tostring(rec.owner))
    out("     dist " .. num(d) .. " at " .. tostring(rec.x) .. "," .. tostring(rec.y) .. " home " .. tostring(rec.hx) .. "," .. tostring(rec.hy)
        .. " object " .. tostring(a ~= nil) .. " idle " .. num(rec.idleH) .. " h leaving " .. tostring(rec.goneP == true)
        .. " missed " .. tostring(rec.missN) .. " feed in " .. num(B.WaitLeft(rec, "feed", now)) .. " h pet in "
        .. num(B.WaitLeft(rec, "pet", now)) .. " h")
end

function NCBear_CubInfo()
    local p, key, reg = ready()
    if not p then return end
    local now = B.Now()
    out("--- bear cub info, world hours " .. num(now) .. " ---")
    local names = {}
    for name, _ in pairs(B.OPTS) do names[#names + 1] = name end
    table.sort(names)
    local line = "sandbox:"
    for i = 1, #names do
        line = line .. " " .. names[i] .. "=" .. tostring(B.Opt(names[i]))
        if i % 5 == 0 and i < #names then
            out(line)
            line = "        "
        end
    end
    out(line)
    local s = B.SlotsOf(key, now)
    local lock = (tonumber(s.lockUntil) or 0) - now
    if lock < 0 then lock = 0 end
    out("me: key " .. tostring(s.key) .. " cubs on " .. tostring(s.on) .. " bears " .. tostring(s.bears) .. "/" .. tostring(s.maxBears)
        .. " taming " .. tostring(s.bonded) .. " wild " .. tostring(s.wild) .. " bait " .. tostring(s.bait) .. " lock " .. num(lock) .. " h")
    local n = 0
    for _, rec in pairs(reg.cubs) do
        infoRec(p, rec, now)
        n = n + 1
    end
    out("entries: " .. n)
    for _, bait in pairs(reg.baits) do
        out("  bait " .. tostring(bait.id) .. " owner " .. tostring(bait.owner) .. " " .. tostring(bait.kind) .. " at " .. tostring(bait.x) .. ","
            .. tostring(bait.y) .. " nights " .. tostring(bait.nights) .. " missed " .. tostring(bait.miss) .. " ready " .. tostring(bait.ready == true))
    end
    local view = B.View
    local vn = 0
    if view and type(view.cubs) == "table" then
        for _, _ in pairs(view.cubs) do vn = vn + 1 end
    end
    local fresh = B.UI and B.UI.Fresh and B.UI.Fresh()
    out("view: ready " .. tostring(view and view.ready) .. " fresh " .. tostring(fresh) .. " cubs " .. vn .. " bait "
        .. tostring(view and view.bait and view.bait.id) .. " log " .. tostring(B.LogOn))
end

function NCBear_CubKill()
    local p = ready()
    if not p then return end
    local rec, animal = B.NearestRec(p, 60)
    if not rec then
        say("no cub entry within 60 tiles")
        return
    end
    if not animal then
        say("cub " .. tostring(rec.id) .. " is not loaded (walk closer)")
        return
    end
    animal:setHealth(0)                                 -- shared/TimedActions/Animals/ISKillAnimal.lua:58
    say("cub " .. tostring(rec.id) .. " (" .. tostring(rec.st) .. ") set to 0 health; the next brain tick books the death")
end

function NCBear_CubClean()
    local p, _, reg = ready()
    if not p then return end
    -- Erst sammeln, dann handeln (nie waehrend des Durchlaufs loeschen).
    local recs = {}
    for _, rec in pairs(reg.cubs) do recs[#recs + 1] = rec end
    for i = 1, #recs do B.Close(recs[i], "clean") end
    -- Alle geladenen Jungen entfernen, mit und ohne Eintrag. Liste und Rueckwaerts-Schleife: FenrisScenario.lua:505-507;
    -- instanceof(o, "IsoAnimal"): shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; entfernt wird nur ueber den Kern.
    local objects = getCell():getObjectListForLua()
    local gone = 0
    for i = objects:size(), 1, -1 do
        local o = objects:get(i - 1)
        if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB then
            B.RemoveCub(o)
            gone = gone + 1
        end
    end
    local keys = {}
    for bid, _ in pairs(reg.baits) do keys[#keys + 1] = bid end
    for i = 1, #keys do reg.baits[keys[i]] = nil end
    local baits = #keys
    keys = {}
    for pk, _ in pairs(reg.players) do keys[#keys + 1] = pk end
    for i = 1, #keys do reg.players[keys[i]] = nil end
    if B.Touch then B.Touch() end
    push(p)
    say("cleaned: " .. #recs .. " entr" .. ((#recs == 1) and "y" or "ies") .. ", " .. gone .. " loaded cub(s), " .. baits
        .. " bait spot(s), " .. #keys .. " lock(s); cubs that are not loaded stay in the world")
end

function NCBear_CubLog(on)
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return
    end
    if on == nil then on = not B.LogOn end
    B.LogOn = (on == true)
    out("diagnosis lines [TC-BEAR] " .. (B.LogOn and "on" or "off"))
end

function NCBear_CubSet(field, value)
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return
    end
    local cfg = B.CFG
    if not cfg then
        out("the bear core is not loaded")
        return
    end
    if field == nil or cfg[field] == nil then
        local names = {}
        for name, v in pairs(cfg) do
            if type(v) ~= "table" then names[#names + 1] = name .. "=" .. tostring(v) end
        end
        table.sort(names)
        out("NCBear_CubSet(field, value). Fields: " .. table.concat(names, " "))
        return
    end
    if type(value) ~= type(cfg[field]) or type(value) == "table" then
        out("NCBear_CubSet: " .. tostring(field) .. " needs a " .. type(cfg[field]) .. " (now " .. tostring(cfg[field]) .. ")")
        return
    end
    cfg[field] = value
    out(tostring(field) .. " = " .. tostring(value) .. " (until the game is closed)")
end

-- ---------------------------------------------------------------------------
-- Rechtsklick: Eintraege im vorhandenen Untermenue "NC Bear" (NCBearTest.lua nimmt Funktionen aus NCBearMenu.extra an und
-- ruft sie nur im Einzelspieler). Keine alte Datei wird geaendert.
-- ---------------------------------------------------------------------------
local function menuHere() NCBear_CubHere() end
local function menuFood() NCBear_CubFood() end
local function menuSkip() NCBear_CubSkip(2) end
local function menuInfo() NCBear_CubInfo() end
local function menuClean() NCBear_CubClean() end

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}
table.insert(NCBearMenu.extra, function(sub, square, player)
    -- addOption(Text, Ziel, Funktion): client/ISUI/Animal/ISAnimalContextMenu.lua:287
    sub:addOption("Cub: appear near me", square, menuHere)
    sub:addOption("Cub: give food", square, menuFood)
    sub:addOption("Cub: skip 2 hours", square, menuSkip)
    sub:addOption("Cub: info", square, menuInfo)
    sub:addOption("Cub: clean up", square, menuClean)
end)
