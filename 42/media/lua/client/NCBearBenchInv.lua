--
-- NUR TESTHILFE fuer das Inventar des Baeren (F4, Lauf baer-f4, PLAN_F4.md 14). Wird NIE nach NPC Crew kopiert (NCBearBench*).
-- Kein Kern-Code ruft diese Datei. Sie ist KEIN Gegenstands-Drucker: kein Befehl legt einen Gegenstand an oder loescht einen -- sie liest,
-- oeffnet das Fenster und ruft die Werkbank-Wege des Kerns (f4/schnittstelle.md K8: B.InvInfo, B.InvSnap, B.InvSet; Abgleich B.InvHeal;
-- Kopie weg B.InvCopyOff), jeden hinter einem Existenz-Riegel. Kapazitaet testen: NCBear_CubSet("bagAdd", x) (client/NCBearBenchCub.lua)
-- und der Sandbox-Regler "Bear: carrying capacity"; Tod mit Inhalt: NCBear_CubKill(); Registerverlust: NCBear_CubForget().
-- NUR EINZELSPIELER ("not isServer() and not isClient()") fuer alles, was das Register beruehrt; im Mehrspieler sagt der Befehl
-- "singleplayer only". NCBear_InvOpen und NCBear_InvAsk gehen ueberall (sie sind dieselben Wege wie Knopf und Fenster).
--
-- Konsole:
--   NCBear_InvInfo()      Saetze, Stueck, Last / Kapazitaet, Fassung r im Register UND in der Kopie beim Spieler, Packtaschen, Waisen,
--                         invLost, invDrop (B.InvInfo des Kerns), dazu die Sicht (ivW ivC ivN ivK ivR ivX bag eat) und die Liste dieses Clients
--   NCBear_InvSnap()      Vorstand merken (B.InvSnap) -- danach etwas hineinlegen oder herausnehmen
--   NCBear_InvRollback()  ABSTURZ NACHSTELLEN: Register-Inventar auf den gemerkten Vorstand (B.InvSet(rec) ohne weitere Argumente), dann
--                         Abgleich sofort (B.InvHeal(player, true)) -> erwartet
--                         "inv: <id> restored from the owner's copy" in console.txt und denselben Inhalt wie vorher (die Kopie gewinnt)
--   NCBear_InvCopyOff()   Kopie beim Spieler fuer meinen Baeren entfernen (B.InvCopyOff) -> naechster Abgleich: "Register gewinnt, Kopie neu"
--   NCBear_InvOpen()      Inventar-Fenster meines naechsten Baeren oeffnen (wie der Knopf "Inventory")
--   NCBear_InvAsk()       die Liste neu anfordern (Bitte "InvList", wie das offene Fenster)
--
-- Engine-Aufrufe (Fundstelle): getSpecificPlayer(0) V:client/Farming/CFarmingSystem.lua:45; player:getX() / getY()
-- V:client/Fishing/TensionUI.lua:11; player:Say(Text) V:client/Entity/ISEntityUI.lua:458.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local VIEW_FIELDS = { "ivW", "ivC", "ivN", "ivK", "ivR", "ivX", "bag", "eat" }

local function out(text)
    print("[NCBear] " .. tostring(text))
end

local function say(text)
    out(text)
    local p = getSpecificPlayer(0)
    if p then p:Say(tostring(text)) end
end

-- Spieler, Schluessel, Register -- oder nil mit einer klaren Zeile (wie client/NCBearBenchNeeds.lua).
local function ready()
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

local function myTame(p, key, reg)
    local best, bestD = nil, nil
    for _, rec in pairs(reg.cubs) do
        if rec.st == "tame" and rec.owner == key then
            local dx = (tonumber(rec.x) or 0) - p:getX()
            local dy = (tonumber(rec.y) or 0) - p:getY()
            local d = dx * dx + dy * dy
            if bestD == nil or d < bestD then best, bestD = rec, d end
        end
    end
    return best
end

local function myRec()
    local p, key, reg = ready()
    if not p then return nil end
    local rec = myTame(p, key, reg)
    if not rec then
        say("no tamed bear of yours (NCBear_CubTame(100) first)")
        return nil
    end
    return rec, p
end

-- Eigener Baer aus der Sicht (geht auch im Mehrspieler): naechster Eintrag aus U.WinBears.
local function myView()
    local U = B.UI
    if not U or not U.WinBears then return nil end
    local list = U.WinBears()
    local p = getSpecificPlayer(0)
    local best, bestD = nil, nil
    for i = 1, #list do
        local v = list[i]
        local dx = (tonumber(v.x) or 0) - (p and p:getX() or 0)
        local dy = (tonumber(v.y) or 0) - (p and p:getY() or 0)
        local d = dx * dx + dy * dy
        if bestD == nil or d < bestD then best, bestD = v, d end
    end
    return best, p
end

local function flat(t)
    if type(t) ~= "table" then return tostring(t) end
    local keys = {}
    for k, _ in pairs(t) do keys[#keys + 1] = tostring(k) end
    table.sort(keys)
    local parts = {}
    for i = 1, #keys do
        local k = keys[i]
        local v = t[k]
        if v == nil then v = t[tonumber(k)] end
        if type(v) == "table" then v = "{...}" end
        parts[#parts + 1] = k .. "=" .. tostring(v)
    end
    return table.concat(parts, " ")
end

function NCBear_InvInfo()
    local rec, p = myRec()
    if not rec then return end
    if B.InvInfo then
        out("inv: " .. flat(B.InvInfo(rec, p)))
    else
        out("inv: the core has no B.InvInfo (server/BanditsNPCBearInv.lua not loaded)")
    end
    local v = myView()
    if v then
        local parts = {}
        for i = 1, #VIEW_FIELDS do parts[#parts + 1] = VIEW_FIELDS[i] .. "=" .. tostring(v[VIEW_FIELDS[i]]) end
        out("view: " .. table.concat(parts, " "))
        local U = B.UI
        local e = U and U.InvList and U.InvList(v.id)
        if e then
            out("list: r=" .. tostring(e.r) .. " pages=" .. tostring(e.pn) .. " rows=" .. tostring(#e.rows) .. " things=" .. tostring(e.cnt)
                .. " load=" .. tostring(e.load) .. " cap=" .. tostring(e.cap))
        else
            out("list: none yet (NCBear_InvAsk())")
        end
    end
    say("inventory info -> console.txt")
end

function NCBear_InvSnap()
    local rec = myRec()
    if not rec then return end
    if not B.InvSnap then
        say("the core has no B.InvSnap")
        return
    end
    B.InvSnap(rec)
    say("snapshot of bear " .. tostring(rec.id) .. " kept -- now put something in or take something out, then NCBear_InvRollback()")
end

function NCBear_InvRollback()
    local rec, p = myRec()
    if not rec then return end
    if not B.InvSet or not B.InvHeal then
        say("the core has no B.InvSet / B.InvHeal")
        return
    end
    local ok = B.InvSet(rec)
    if ok == false then
        say("no snapshot (NCBear_InvSnap() first)")
        return
    end
    B.InvHeal(p, true)                                          -- force: der Abgleich laeuft sonst nur einmal je Sitzung
    say("register set back like after a crash -- check console.txt for 'restored from the owner's copy', then NCBear_InvInfo()")
end

function NCBear_InvCopyOff()
    local rec, p = myRec()
    if not rec then return end
    if not B.InvCopyOff then
        say("the core has no B.InvCopyOff")
        return
    end
    B.InvCopyOff(p, rec)
    say("owner's copy removed -- the next check writes it new from the register")
end

function NCBear_InvOpen()
    local v, p = myView()
    local U = B.UI
    if not v or not U or not U.InvOpen then
        say("no bear of yours in view (or the inventory window is not loaded)")
        return
    end
    U.InvOpen(p, v.id)
end

function NCBear_InvAsk()
    local v, p = myView()
    local U = B.UI
    if not v or not U or not U.InvAsk then
        say("no bear of yours in view")
        return
    end
    if U.InvAskReset then U.InvAskReset(v.id) end
    out("InvList asked: " .. tostring(U.InvAsk(p, v.id)))
end
