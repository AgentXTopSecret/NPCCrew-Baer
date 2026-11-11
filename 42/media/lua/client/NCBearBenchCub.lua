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
--   NCBear_CubSet(feld, wert) einen Stellwert aus B.CFG aendern (z. B. "tagZ" = Hoehe von Balken und Namensschild ueber dem
--                            Jungen, "petAnim", "shyDist"); gilt bis zum Spielende
-- B1b (PLAN_B1B.md 5.6):
--   NCBear_CubFollow(on)     meinem naechsten zahmen Jungen Folgen an (true) / aus (false) / umschalten (nil) -- ueber dieselbe
--                            Bitte "Mode" wie der Rechtsklick, also mit denselben Pruefungen des Schreibers
--   NCBear_CubName(text)     mein naechstes zahmes Junges umbenennen (Bitte "Rename", dieselben Pruefungen)
--   NCBear_CubFollowTest()   Folgen-Zustand drucken: Modus, Abstand zum Besitzer, Ebenen, Fahrzeug, Sitzung (gehalten, fest,
--                            Alter des letzten Laufbefehls), Heimat, tagZ
--   NCBear_CubOrphan(n)      eine Waise n Kacheln (Vorgabe 8) neben mir: ein Junges OHNE Eintrag (fuer den N5-Test)
--   NCBear_CubSweep()        Suchlauf mit Waisen sofort (B.ScanAnimals(nil, true): nur die Alters-Frist entfaellt; Abstand
--                            25 Kacheln und "keiner sieht hin" gelten weiter)
-- B1c (PLAN_B1C.md 6.9):
--   NCBear_CubForget()       den Register-Eintrag meines naechsten zahmen Jungen loeschen, der Spiegel am Tier BLEIBT (Kevins
--                            Absturz N9 nachstellen); danach heilt der Kern ihn innerhalb von 2 min (oder sofort mit NCBear_CubSweep())
--   NCBear_CubMark()         Spiegel des naechsten geladenen Jungen drucken (alle Felder) und ob er zum Eintrag passt (B.MarkFresh)
--   NCBear_CubCalm()         Laerm-Wache: beobachtete Junge, je Junges die Felder der Wache (Stress, Antworten ...)
--   NCBear_CubGuard()        Zombie-Wache: naechster Zombie je Junges, Wache an/aus, Modus, "heiss" (schneller Hirn-Takt)
--   NCBear_CubRide()         Mitfahren: ride, gen, Sitzung (offMs, lostMs, failN), ich im Fahrzeug
--   NCBear_CubCallReset()    Abklingzeit von "Call to me" fuer alle Jungen zuruecksetzen
--   NCBear_CubInfo()         druckt zusaetzlich u, gen, r, ride, healed je Eintrag und v/ep des Registers
-- B1d (PLAN_B1D.md 1.7):
--   NCBear_CubGrow(tage)     mein naechstes zahmes Junges um so viele Wachstumstage weiter (Vorgabe 5; negativ = zurueck, geklemmt
--                            auf 0 .. ausgewachsen) -- ueber B.GrowSetG (Stufen-Meldung, Commit, Groesse sofort), danach eine Zeile
--   NCBear_CubStats()        alles zum Wachsen drucken: Tag, Groesse innen / gezeigt, Stufe, Leben, Ausdauer, Schaden, Traglast,
--                            Faehigkeiten (XP / Stufe), Ausweichen, Kampf-Bonus, Fang-Chance, Warnweite, Fuetter-Bonus, Engine-Werte
--   NCBear_CubXp(key, xp)    Erfahrung einer Faehigkeit absolut setzen (agi vit con fgt fsh nos; B.SkillSet)
--   NCBear_CubHurt(pct)      Leben auf pct Prozent setzen (1..100; B.GrowSetHp) -- Heilen und Balken pruefen
--   NCBear_CubInfo()         druckt zusaetzlich g, hp, hpB und die Erfahrung je Eintrag
-- B1e (PLAN_B1E.md 1.6): ab Halbstark (innere Groesse 0,75, bei 100 Tagen Tag 15) traegt das zahme Junge den grossen Koerper (Art
--   B.BIG); NCBear_CubGrow(-100) bringt es zurueck zum Jungen.
--   NCBear_CubGrow(tage)     wie B1d; der Tausch kommt im selben Aufruf (B.BrainTick(true)), die Zeile nennt den Koerper danach
--                            ("body big (swapped)" / "body cub, swap waits: calm")
--   NCBear_CubStats()        druckt zusaetzlich body / want / engine type, ob der Tausch bereit ist (sonst warum nicht), letzter
--                            Tausch, Fehlversuche
--   NCBear_CubClean(), NCBear_CubMark()   sehen beide Koerper (B.BodyKind des Kerns), nie den Test-Baeren "bear"
-- Rechtsklick auf eine Kachel, Untermenue "NC Bear": zwoelf Eintraege "Cub: ...". Texte hier sind englische Literale.
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

-- Grosse ganze Zahl (Kennzeichen u, Epoche ep: Millisekunden x 1000) ohne Exponent.
local function big(v)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%.0f", v)
end

-- Flache Felder einer Tabelle als Text, Schluessel sortiert (Zahlen, Texte, Wahrheitswerte; Tabellen als "{...}").
-- skip = Felder, die nicht gedruckt werden. Felder, die auf "At" enden oder "seen" heissen, kommen mit Alter in ms dazu.
local function flat(t, skip)
    if type(t) ~= "table" then return " " .. tostring(t) end
    local keys = {}
    for k, _ in pairs(t) do
        if not (skip and skip[k]) then keys[#keys + 1] = tostring(k) end
    end
    table.sort(keys)
    local now = getTimestampMs()                        -- server/Foraging/forageServer.lua:456
    local parts = {}
    for i = 1, #keys do
        local k = keys[i]
        local v = t[k]
        if v == nil then v = t[tonumber(k)] end
        local tv = type(v)
        if tv == "table" then
            parts[#parts + 1] = k .. "={...}"
        elseif tv == "number" and (k == "seen" or (string.len(k) > 2 and string.sub(k, string.len(k) - 1) == "At")) and v > 1000000 then
            parts[#parts + 1] = k .. "=" .. tostring(v) .. " (" .. tostring(now - v) .. " ms ago)"
        else
            parts[#parts + 1] = k .. "=" .. tostring(v)
        end
    end
    if #parts == 0 then return " (empty)" end
    return " " .. table.concat(parts, " ")
end

local function infoRec(p, rec, now)
    local dx = (tonumber(rec.x) or 0) - p:getX()        -- client/Fishing/TensionUI.lua:11
    local dy = (tonumber(rec.y) or 0) - p:getY()
    local d = math.sqrt(dx * dx + dy * dy)
    local a = B.FindAnimal(rec)
    out("  " .. tostring(rec.id) .. " " .. tostring(rec.st) .. " src " .. tostring(rec.src) .. " bar " .. num(rec.tame)
        .. " fed " .. tostring(rec.fedN) .. " pet " .. tostring(rec.petN) .. " last " .. tostring(rec.last)
        .. " finder " .. tostring(rec.finder) .. " bond " .. tostring(rec.bond) .. " owner " .. tostring(rec.owner)
        .. " mode " .. tostring(rec.mode) .. " name " .. tostring(rec.name))
    out("     dist " .. num(d) .. " at " .. tostring(rec.x) .. "," .. tostring(rec.y) .. " home " .. tostring(rec.hx) .. "," .. tostring(rec.hy)
        .. " object " .. tostring(a ~= nil) .. " idle " .. num(rec.idleH) .. " h leaving " .. tostring(rec.goneP == true)
        .. " missed " .. tostring(rec.missN) .. " feed in " .. num(B.WaitLeft(rec, "feed", now)) .. " h pet in "
        .. num(B.WaitLeft(rec, "pet", now)) .. " h")
    -- B1c: Kennzeichen, Koerper-Generation, Aenderungszaehler, Mitfahren, Heilung
    local healed = "-"
    if type(rec.healed) == "table" then healed = "at " .. num(rec.healed.at) .. " h, epoch " .. tostring(rec.healed.ep) end
    local ride = "-"
    if type(rec.ride) == "table" then ride = "since " .. num(rec.ride.at) .. " h" end
    out("     u " .. big(rec.u) .. " gen " .. tostring(rec.gen) .. " r " .. tostring(rec.r) .. " ride " .. ride
        .. " healed " .. healed .. " body " .. tostring(rec.body))
    -- B1d: Wachstum, Leben, Erfahrung (nur Register-Felder, roh)
    if rec.g ~= nil or rec.hp ~= nil or rec.xCon ~= nil then
        out("     g " .. tostring(rec.g) .. " hp " .. tostring(rec.hp) .. " hpB " .. tostring(rec.hpB) .. " xp agi " .. tostring(rec.xAgi)
            .. " vit " .. tostring(rec.xVit) .. " con " .. tostring(rec.xCon) .. " fgt " .. tostring(rec.xFgt) .. " fsh "
            .. tostring(rec.xFsh) .. " nos " .. tostring(rec.xNos) .. " feed bonus " .. tostring(rec.gF) .. " (" .. tostring(rec.gFn)
            .. " on day " .. tostring(rec.gFd) .. ")")
    end
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
    out("entries: " .. n .. " (registry v " .. tostring(reg.v) .. ", epoch " .. big(reg.ep) .. ", next number " .. tostring(reg.n) .. ")")
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
    -- B1e: beide Koerper (Junges und grosser Koerper) ueber B.BodyKind des Kerns; der Test-Baer "bear" bleibt.
    local objects = getCell():getObjectListForLua()
    local gone = 0
    for i = objects:size(), 1, -1 do
        local o = objects:get(i - 1)
        if instanceof(o, "IsoAnimal") and B.BodyKind and B.BodyKind(o) ~= nil then
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
        out("B1c groups: heal (healWindowMs healScanMs), noise (calmMax calmMs calmGap noiseStressJump noiseAnswerMax"
            .. " noiseAnswerWinMs ownSlackMs ownMaxMs followFleeGrow), walk (walkDist walkSpeed runSpeed), zombies (zedSense zedHide"
            .. " zedSafe zedCalmMs zedFlee hideGap hideNear hideOwnerMax zedScanMax zedTickMs zedKeepMs guardMoveMs guardRepath"
            .. " guardRenewMs), ride (rideOffMsSP rideOffMsMP rideSpeedMax rideRing rideLostMs rideFailLog callRing viewMoveTiles"
            .. " viewMoveMs), marker (markerMs markerAfterMs markerDur markerShift), map (mapMiniPx mapWorldMin mapWorldMax mapListMs)")
        out("B1d groups: growth (cubMaxSize bodySwap sizeEps tagBase growCommitH feedGrowFav feedGrowOk feedGrowSnack feedGrowDay"
            .. " feedGrowMax), values (vitPerLv conPerLv dodgeBase fishBase fishMax noseBase noseStep), skills (xpPerMin xpBucketMin"
            .. " xpHitTaken xpHitDealt xpFishTry xpFishCatch xpSniff conTilesPerXp conBreathXp conBreathMs conStepMax), stamina and"
            .. " health (staRunCost staRegen staViewStep hpEps hpCommit); the tables growCurve stageAt statAt hpAt staAt carryAt"
            .. " dmgAt xpNeed are not settable here")
        out("B1e groups: body swap (bodySwap swapSize swapBackSize swapMinMs swapRetryMs swapFailLog swapRing swapFaceDist busyMs),"
            .. " big body (walkSpeedBig runSpeedBig bodyLenBig tilesPerE followRefLen tagBigK petAnimBig), marker (markerAngleAdd"
            .. " markerCloseTiles markerR markerG markerB; the size is in Options > Mods)")
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
-- B1b: Folgen, Name, Waisen (PLAN_B1B.md 5.6). Alles geht ueber dieselben Wege wie das Spiel (B.Ask -> Schreiber-Pruefungen).
-- ---------------------------------------------------------------------------

-- Folgen-Zustand nach der Regel des Kerns (B.ModeOf, nil = "stay").
local function modeOf(rec)
    if B.ModeOf then return B.ModeOf(rec) end
    if rec.mode == "follow" then return "follow" end
    return "stay"
end

-- Mein naechstes gezaehmtes Junges (Eintrag im Register), gleich wie weit weg.
local function myTame(p, key, reg)
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        if rec.st == "tame" and rec.owner == key then
            local dx = (tonumber(rec.x) or 0) - p:getX()    -- client/Fishing/TensionUI.lua:11
            local dy = (tonumber(rec.y) or 0) - p:getY()
            local d = dx * dx + dy * dy
            if bestD == nil or d < bestD then
                best, bestD = rec, d
            end
        end
    end
    return best
end

function NCBear_CubFollow(on)
    local p, key, reg = ready()
    if not p then return end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed cub of yours (NCBear_CubTame(100) first)")
        return
    end
    local mode = "follow"
    if on == nil then
        if modeOf(rec) == "follow" then mode = "stay" end
    elseif on == false then
        mode = "stay"
    end
    B.Ask(p, "Mode", { id = rec.id, mode = mode })
    push(p)
    say("cub " .. tostring(rec.id) .. ": asked " .. mode .. ", now " .. modeOf(rec))
end

function NCBear_CubName(text)
    local p, key, reg = ready()
    if not p then return end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed cub of yours (NCBear_CubTame(100) first)")
        return
    end
    B.Ask(p, "Rename", { id = rec.id, name = tostring(text or "") })
    push(p)
    say("cub " .. tostring(rec.id) .. ": name now " .. tostring(rec.name))
end

function NCBear_CubFollowTest()
    local p, key, reg = ready()
    if not p then return end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed cub of yours (NCBear_CubTame(100) first)")
        return
    end
    local a = B.FindAnimal(rec)
    local cx, cy, cz = tonumber(rec.x) or 0, tonumber(rec.y) or 0, tonumber(rec.z) or 0
    if a then
        cx, cy, cz = a:getX(), a:getY(), a:getZ()       -- client/TimedActions/ISContextualActions.lua:100
    end
    local dx = cx - p:getX()
    local dy = cy - p:getY()
    local pz = p:getZ()                                 -- client/Fishing/TensionUI.lua:11
    local car = p:getVehicle() ~= nil                   -- client/ISUI/Hutch/ISHutchMenu.lua:8
    out("--- follow test, cub " .. tostring(rec.id) .. " ---")
    out("mode " .. modeOf(rec) .. " (field " .. tostring(rec.mode) .. ") name " .. tostring(rec.name) .. " object " .. tostring(a ~= nil))
    out("distance to me " .. num(math.sqrt(dx * dx + dy * dy)) .. " levels cub " .. num(cz) .. " / me " .. num(pz)
        .. " in vehicle " .. tostring(car) .. " limit " .. tostring(B.Opt("BearFollowMaxDistance")))
    out("home " .. tostring(rec.hx) .. "," .. tostring(rec.hy) .. "," .. tostring(rec.hz) .. " tagZ " .. tostring(B.CFG.tagZ))
    local s = B._s and B._s[rec.id]
    local f = s and s.f
    if type(f) ~= "table" then
        out("session: none yet (first brain tick after load or after a mode change)")
        return
    end
    local now = getTimestampMs()                        -- server/Foraging/forageServer.lua:456
    local age = "-"
    if type(f.orderAt) == "number" then age = tostring(now - f.orderAt) .. " ms" end
    local retry = "-"
    if type(f.retryAt) == "number" then retry = tostring(f.retryAt - now) .. " ms" end
    out("session: held " .. tostring(f.held == true) .. " stuck " .. tostring(f.stuck == true) .. " last order " .. age
        .. " target " .. tostring(f.tx) .. "," .. tostring(f.ty) .. " best " .. num(f.bestD) .. " retry in " .. retry)
end

function NCBear_CubOrphan(n)
    local p = ready()
    if not p then return nil end
    if not B.CreateCub then
        out("the bear core is not loaded (BanditsNPCBearWorld.lua)")
        return nil
    end
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
        local sq = getCell():getGridSquare(cx + ring[i][1], cy + ring[i][2], cz)    -- server/Animal/ISPickDungCursor.lua:104
        local fits, why = B.SquareFits(sq)
        if fits then
            -- Absichtlich OHNE Register-Eintrag: genau so bleibt nach einem Fehler eine Waise zurueck (N5).
            local animal, refused = B.CreateCub(sq:getX(), sq:getY(), sq:getZ())
            if not animal then
                say("no orphan: " .. tostring(refused))
                return nil
            end
            say("orphan cub " .. n .. " tiles away (no entry); walk 25+ tiles off, look away, wait or NCBear_CubSweep()")
            return animal
        end
        lastWhy = why
    end
    say("no free outdoor square " .. n .. " tiles around you (" .. tostring(lastWhy) .. ")")
    return nil
end

function NCBear_CubSweep()
    local p = ready()
    if not p then return end
    if not B.ScanAnimals then
        out("the bear core is not loaded (BanditsNPCBearWorld.lua)")
        return
    end
    local n, removed = B.ScanAnimals(nil, true)
    push(p)
    say("sweep: " .. tostring(n) .. " cub(s) seen, " .. tostring(removed or 0) .. " orphan(s) removed (nobody within 25 tiles, not seen)")
end

-- ---------------------------------------------------------------------------
-- B1c: Selbstheilung, Laerm, Zombies, Mitfahren, Call to me (PLAN_B1C.md 6.9). Nur lesen und die zwei Testgriffe (Eintrag loeschen,
-- Abklingzeit leeren); alles andere geht ueber die Wege des Spiels.
-- ---------------------------------------------------------------------------

function NCBear_CubForget()
    local p, key, reg = ready()
    if not p then return end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed cub of yours (NCBear_CubTame(100) first)")
        return
    end
    local id = rec.id
    local loaded = B.FindAnimal ~= nil and B.FindAnimal(rec) ~= nil
    -- Absichtlich OHNE B.Close (keine Meldung, keine Sperre): genau so fehlt der Eintrag nach Kevins Absturz (N9).
    reg.cubs[id] = nil
    if B._s then B._s[id] = nil end
    if B.Touch then B.Touch(nil, key) end
    push(p)
    say("entry " .. tostring(id) .. " removed, mark kept -- wait up to 2 min or NCBear_CubSweep()")
    if not loaded then out("  note: the cub is not loaded right now; it heals once it is loaded again") end
end

-- Naechstes geladenes Junges (mit oder ohne Eintrag) in r Kacheln. Liste: FenrisScenario.lua:505-507; instanceof(o, "IsoAnimal"):
-- shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; B1e: beide Koerper ueber B.BodyKind des Kerns (darin getAnimalType(),
-- client/ISUI/Animal/ISAnimalUI.lua:65); getX/getY am Tier: client/TimedActions/ISContextualActions.lua:100.
local function nearestCubObject(p, r)
    if not B.BodyKind then return nil, nil end
    local objects = getCell():getObjectListForLua()
    local px, py = p:getX(), p:getY()
    local best, bestD = nil, nil
    for i = 0, objects:size() - 1 do
        local o = objects:get(i)
        if instanceof(o, "IsoAnimal") and B.BodyKind(o) ~= nil then
            local dx, dy = o:getX() - px, o:getY() - py
            local d = math.sqrt(dx * dx + dy * dy)
            if d <= r and (bestD == nil or d < bestD) then
                best, bestD = o, d
            end
        end
    end
    return best, bestD
end

function NCBear_CubMark()
    local p, _, reg = ready()
    if not p then return end
    local a, d = nearestCubObject(p, 60)
    if not a then
        say("no loaded cub within 60 tiles")
        return
    end
    -- getModData am Tier: client/ISUI/ISInventoryPaneContextMenu.lua:4127
    local md = a:getModData()
    local mark = md and md[B.MARK]
    out("--- mark of the nearest loaded cub (" .. num(d) .. " tiles) ---")
    if type(mark) ~= "table" then
        out("no mark (" .. tostring(B.MARK) .. " missing): an orphan without entry")
        return
    end
    out("mark:" .. flat(mark))
    out("  u " .. big(mark.u) .. " epoch " .. big(mark.ep) .. " (registry epoch " .. big(reg.ep) .. ")")
    local rec = nil
    if mark.id ~= nil then rec = reg.cubs[mark.id] end
    if not rec then
        out("entry " .. tostring(mark.id) .. ": none in the registry (the core heals it on its next search)")
        return
    end
    local s = B._s and B._s[rec.id]
    local bound = (s ~= nil and s.obj == a)
    local fresh = "n/a (core without B.MarkFresh)"
    if B.MarkFresh then fresh = tostring(B.MarkFresh(rec, mark) == true) end
    out("entry " .. tostring(rec.id) .. ": st " .. tostring(rec.st) .. " u " .. big(rec.u) .. " gen " .. tostring(rec.gen)
        .. " r " .. tostring(rec.r) .. " | bound to this animal " .. tostring(bound) .. " | mark fresh " .. fresh)
    if B.MarkOf then out("mark as the core would write it:" .. flat(B.MarkOf(rec))) end
end

-- Nur lesen: Einzelspieler und Kern da? (ohne Spieler-Pflicht)
local function readyCore()
    if B.IsSP and not B.IsSP() then
        out("singleplayer only")
        return false
    end
    if not B.IsSP or not B.Reg then
        out("the bear core is not loaded (BanditsNPCBear*.lua)")
        return false
    end
    return true
end

function NCBear_CubCalm()
    if not readyCore() then return end
    local calm = B._calm
    out("--- noise watch: watched " .. tostring(B._calmN) .. " ---")
    if type(calm) ~= "table" then
        out("no noise watch in this core (B._calm missing)")
        return
    end
    local ids = {}
    for id, _ in pairs(calm) do ids[#ids + 1] = tostring(id) end
    table.sort(ids)
    if #ids == 0 then out("no tamed cub is watched right now (none loaded, riding or not tame)") end
    for i = 1, #ids do
        local w = calm[ids[i]]
        local hits = 0
        if type(w) == "table" and type(w.hits) == "table" then hits = #w.hits end
        out("  " .. ids[i] .. ":" .. flat(w, { a = true, hits = true }) .. " | answers in the window " .. hits)
    end
end

function NCBear_CubGuard()
    if not readyCore() then return end
    local tick = B.CFG.brainMs
    if B._hot then tick = B.CFG.zedTickMs end
    out("--- zombie watch: hot " .. tostring(B._hot) .. " (brain tick " .. tostring(tick) .. " ms) ---")
    local zed = B._zed
    if type(zed) ~= "table" then
        out("no zombie watch in this core (B._zed missing)")
        return
    end
    local ids = {}
    for id, _ in pairs(zed) do ids[#ids + 1] = tostring(id) end
    table.sort(ids)
    if #ids == 0 then out("no loaded cub has a zombie listed") end
    for i = 1, #ids do
        local z = zed[ids[i]]
        local s = B._s and B._s[ids[i]]
        out("  " .. ids[i] .. ": nearest zombie" .. flat(z) .. " | watch" .. flat(s and s.g))
    end
end

function NCBear_CubRide()
    local p, key, reg = ready()
    if not p then return end
    local car = p:getVehicle() ~= nil                   -- client/ISUI/Hutch/ISHutchMenu.lua:8
    out("--- ride: me in a vehicle " .. tostring(car) .. ", distance limit " .. tostring(B.Opt("BearRideDistance")) .. " ---")
    local n = 0
    for _, rec in pairs(reg.cubs) do
        if rec.owner == key then
            n = n + 1
            local ride = "-"
            if type(rec.ride) == "table" then ride = "since " .. num(rec.ride.at) .. " h" end
            local s = B._s and B._s[rec.id]
            out("  " .. tostring(rec.id) .. " st " .. tostring(rec.st) .. " mode " .. modeOf(rec) .. " ride " .. ride .. " gen "
                .. tostring(rec.gen) .. " at " .. tostring(rec.x) .. "," .. tostring(rec.y) .. " | session" .. flat(s and s.ride))
        end
    end
    if n == 0 then out("no cub of yours") end
end

function NCBear_CubCallReset()
    if not readyCore() then return end
    local t = B._callAt
    if type(t) ~= "table" then
        out("no call cooldown in this core (B._callAt missing)")
        return
    end
    local keys = {}
    for k, _ in pairs(t) do keys[#keys + 1] = k end
    for i = 1, #keys do t[keys[i]] = nil end
    local p = getSpecificPlayer(0)
    if p then push(p) end
    say("call cooldown reset (" .. #keys .. " cub(s))")
end

-- ---------------------------------------------------------------------------
-- B1d: Wachsen, Werte, Faehigkeiten, Leben (PLAN_B1D.md 1.7). Alles ueber die Kern-Wege (B.GrowSetG, B.SkillSet, B.GrowSetHp: Stufen-
-- Meldung, Commit, Groesse/Leben am Tier sofort); gelesen wird mit B.StatsOf / B.SkillProgress (rein, shared).
-- ---------------------------------------------------------------------------

-- Zahl mit d Nachkommastellen (sonst als Text).
local function fix(v, d)
    if type(v) ~= "number" then return tostring(v) end
    return string.format("%." .. tostring(d or 2) .. "f", v)
end

-- Kern mit B1d geladen? (shared/BanditsNPCBearStats.lua + server/BanditsNPCBearGrow.lua)
local function growReady()
    if not B.StatsOf or not B.GrowSetG or not B.GrowSetHp or not B.SkillSet or not B.SkillProgress or not B.SKILLS then
        out("the bear core has no growth (BanditsNPCBearStats.lua / BanditsNPCBearGrow.lua not loaded)")
        return false
    end
    return true
end

-- Mein naechstes zahmes Junges oder nil mit einer Zeile.
local function myGrowRec()
    local p, key, reg = ready()
    if not p then return nil end
    if not growReady() then return nil end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed cub of yours (NCBear_CubTame(100) first)")
        return nil
    end
    return rec, p
end

-- Eine kurze Zeile: Tag, Groesse innen / gezeigt, Stufe, Leben.
local function growLine(rec)
    local st = B.StatsOf(rec)
    local hp = tonumber(rec.hp)
    local life = "health unknown (first check of the body pending) / " .. fix(st.hpMax, 0)
    if hp then life = "health " .. fix(hp * 100, 0) .. "% = " .. fix(hp * st.hpMax, 0) .. " / " .. fix(st.hpMax, 0) end
    local nxt = "full-grown"
    if st.next ~= nil then nxt = tostring(st.next) .. " in " .. tostring(st.nextDays) .. " day(s)" end
    return "cub " .. tostring(rec.id) .. ": day " .. tostring(st.day) .. ", size inner " .. fix(st.s, 3) .. " / shown " .. fix(st.sz, 3)
        .. ", stage " .. tostring(st.stage) .. " (next " .. nxt .. "), " .. life
end

-- B1e (PLAN_B1E.md 1.6): Koerper des Eintrags -- zuerst das lebende Tier (B.BodyKind des Kerns), sonst das Register-Feld rec.body.
-- Gibt body (oder nil), Tier (oder nil).
local function bodyNow(rec)
    local a = nil
    if B.FindAnimal then a = B.FindAnimal(rec) end
    local have = nil
    if a and B.BodyKind then have = B.BodyKind(a) end
    if have == nil and (rec.body == "cub" or rec.body == "big") then have = rec.body end
    return have, a
end

-- B1e: ist der Tausch jetzt erlaubt? B.BodySwapReady(rec, Sitzung, ms) des Kerns (nur lesen). Gibt ok, Grund.
local function swapReady(rec)
    if not B.BodySwapReady then return false, "core without B1e" end
    local s = B._s and B._s[rec.id]
    if type(s) ~= "table" then return false, "no session yet" end
    local ok, why = B.BodySwapReady(rec, s, getTimestampMs())     -- getTimestampMs: server/Foraging/forageServer.lua:456
    if ok then return true, nil end
    return false, tostring(why)
end

-- B1e: Zusatz fuer die Zeile von NCBear_CubGrow: Koerper danach, getauscht oder warum (noch) nicht. before = Koerper vor dem Aufruf.
local function bodyNote(rec, before)
    if not B.BodyWant then return "" end
    local have = bodyNow(rec)
    local want = B.BodyWant(rec)
    if have == nil then return ", body " .. tostring(want) .. " (no living animal: riding, not loaded or missing)" end
    if before ~= nil and have ~= before then return ", body " .. have .. " (swapped)" end
    if want ~= have then
        local ok, why = swapReady(rec)
        if ok then return ", body " .. have .. ", swap on the next brain tick" end
        return ", body " .. have .. ", swap waits: " .. tostring(why)
    end
    return ", body " .. have
end

function NCBear_CubGrow(days)
    local rec, p = myGrowRec()
    if not rec then return end
    days = tonumber(days) or 5
    local D = B.GrowDays()
    local g = tonumber(rec.g) or 0
    local want = g + days / D
    if want < 0 then want = 0 end
    if want > 1 then want = 1 end
    local before = bodyNow(rec)
    B.GrowSetG(rec, want)
    B.BrainTick(true)
    push(p)
    say(growLine(rec) .. bodyNote(rec, before))
end

function NCBear_CubStats()
    local rec = myGrowRec()
    if not rec then return end
    local st = B.StatsOf(rec)
    local D = B.GrowDays()
    out("--- cub stats " .. tostring(rec.id) .. " (" .. tostring(rec.name) .. "), owner " .. tostring(rec.owner) .. " ---")
    local cal = "-"
    if type(rec.tamedAt) == "number" then cal = fix((B.Now() - rec.tamedAt) / 24, 1) end
    out("growth g " .. fix(st.g, 4) .. " = day " .. tostring(st.day) .. " of " .. tostring(D) .. " (calendar days since taming " .. cal
        .. ") | size inner " .. fix(st.s, 3) .. " / shown " .. fix(st.sz, 3) .. " (body " .. tostring(st.body) .. ")")
    local nxt = "none (full-grown)"
    if st.next ~= nil then nxt = tostring(st.next) .. " in " .. tostring(st.nextDays) .. " day(s)" end
    out("stage " .. tostring(st.stage) .. ", next " .. nxt)
    -- B1e (PLAN_B1E.md 1.6): Koerper -- Register, Wunsch, Art des lebenden Tiers (animal:getAnimalType(): V:client/ISUI/Animal/
    -- ISAnimalUI.lua:65, nur gedruckt), Tausch bereit oder warum nicht, letzter Tausch, Fehlversuche (Sitzung des Kerns, nur lesen)
    if B.BodyWant then
        local _, a0 = bodyNow(rec)
        local etype = "- (no living animal)"
        if a0 then etype = tostring(a0:getAnimalType()) end
        out("body " .. tostring(rec.body) .. " / want " .. tostring(B.BodyWant(rec)) .. " / engine type " .. etype)
        local ok, why = swapReady(rec)
        local ready = "swap ready"
        if not ok then ready = "swap waits (" .. tostring(why) .. ")" end
        local s = B._s and B._s[rec.id]
        local last = "never (this session)"
        if type(s) == "table" and type(s.swapAt) == "number" then
            last = fix((getTimestampMs() - s.swapAt) / 1000, 0) .. " s ago"
        end
        local fails = 0
        if type(s) == "table" then fails = tonumber(s.swapFailN) or 0 end
        out(ready .. " | last swap " .. last .. " | fails " .. tostring(fails))
    else
        out("body: the core has no body swap (B1e) loaded")
    end
    local hp = tonumber(rec.hp)
    local life = "health unknown (taken from the body on the next check)"
    if hp then life = "health " .. fix(hp, 3) .. " = " .. fix(hp * st.hpMax, 1) .. " / " .. fix(st.hpMax, 1) end
    out(life .. " | hpB " .. tostring(rec.hpB))
    local s = B._s and B._s[rec.id]
    local sta = s and tonumber(s.sta)
    local stam = "stamina full (no session yet) " .. fix(st.staMax, 1) .. " / " .. fix(st.staMax, 1)
    if sta then stam = "stamina " .. fix(sta, 3) .. " = " .. fix(sta * st.staMax, 1) .. " / " .. fix(st.staMax, 1) .. " (session)" end
    out(stam .. " | damage factor " .. fix(st.dmg, 3) .. " | carry " .. fix(st.carry, 1))
    for i = 1, #B.SKILLS do
        local k = B.SKILLS[i]
        local L, xpIn, need = B.SkillProgress(rec, k)
        local f = B.SKILL_FIELD and B.SKILL_FIELD[k]
        out("  skill " .. k .. ": xp " .. fix(f and tonumber(rec[f]) or 0, 1) .. ", level " .. tostring(L) .. ", "
            .. fix(xpIn, 1) .. " / " .. tostring(need) .. " in this level")
    end
    out("dodge " .. fix(st.dodge, 1) .. "% | fight bonus +" .. fix(st.fightBonus, 1) .. "% | catch chance " .. fix(st.fish, 1)
        .. "% | warning range " .. fix(st.nose, 1) .. " tiles")
    out("feed bonus gF " .. tostring(rec.gF) .. " (" .. tostring(rec.gFn) .. " on day " .. tostring(rec.gFd) .. ")")
    local a = B.FindAnimal(rec)
    if a then
        -- animal:getData():getSize(): V:client/ISUI/Animal/ISAnimalUI.lua:31; animal:getHealth(): V:client/ISUI/Animal/ISAnimalUI.lua:15
        out("engine: size " .. fix(a:getData():getSize(), 3) .. " health " .. fix(a:getHealth(), 3) .. " (living animal)")
    else
        out("engine: no living animal (riding, not loaded or missing)")
    end
end

function NCBear_CubXp(key, xp)
    if not ready() or not growReady() then return end
    if type(key) ~= "string" or not (B.SKILL_FIELD and B.SKILL_FIELD[key]) then
        out("NCBear_CubXp(key, xp). Keys: " .. table.concat(B.SKILLS, " ") .. " (xp 0 .. " .. tostring(B.XpCum and B.XpCum(10)) .. ")")
        return
    end
    local v = tonumber(xp)
    if v == nil then
        out("NCBear_CubXp: xp must be a number")
        return
    end
    local rec, p = myGrowRec()
    if not rec then return end
    local L = B.SkillSet(rec, key, v)
    push(p)
    say("cub " .. tostring(rec.id) .. ": " .. key .. " xp " .. fix(B.SkillXp and B.SkillXp(rec, key) or v, 1) .. ", level " .. tostring(L))
end

function NCBear_CubHurt(pct)
    local rec, p = myGrowRec()
    if not rec then return end
    local v = tonumber(pct) or 50
    v = math.floor(v)
    if v < 1 then v = 1 end
    if v > 100 then v = 100 end
    B.GrowSetHp(rec, v / 100)
    push(p)
    say(growLine(rec))
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
local function menuFollow() NCBear_CubFollow() end
local function menuOrphan() NCBear_CubOrphan() end
local function menuSweep() NCBear_CubSweep() end
local function menuForget() NCBear_CubForget() end
local function menuCallReset() NCBear_CubCallReset() end
local function menuGrow() NCBear_CubGrow(5) end
local function menuStats() NCBear_CubStats() end

NCBearMenu = NCBearMenu or {}
NCBearMenu.extra = NCBearMenu.extra or {}
table.insert(NCBearMenu.extra, function(sub, square, player)
    -- addOption(Text, Ziel, Funktion): client/ISUI/Animal/ISAnimalContextMenu.lua:287
    sub:addOption("Cub: appear near me", square, menuHere)
    sub:addOption("Cub: give food", square, menuFood)
    sub:addOption("Cub: skip 2 hours", square, menuSkip)
    sub:addOption("Cub: info", square, menuInfo)
    sub:addOption("Cub: clean up", square, menuClean)
    sub:addOption("Cub: follow / stay", square, menuFollow)
    sub:addOption("Cub: make an orphan", square, menuOrphan)
    sub:addOption("Cub: remove orphans now", square, menuSweep)
    sub:addOption("Cub: forget entry (keep mark)", square, menuForget)
    sub:addOption("Cub: reset call cooldown", square, menuCallReset)
    sub:addOption("Cub: grow 5 days", square, menuGrow)
    sub:addOption("Cub: stats", square, menuStats)
end)
