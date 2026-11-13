if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, eigenes Inventar beim Schreiber (F4, PLAN_F4.md 2, 4, 6, 9, 10, 11, 16; Kevins Antworten 13.11.2026 abends).
--
-- Weg (PLAN_F4.md 2.3): REGISTER = Wahrheit (rec.inv / rec.bag im Baeren-Eintrag, globale ModData, nie uebertragen), SPIELER-KOPIE = Absturz-
-- Versicherung (besitzer:getModData().BanditsNPCBearInv[<u>], im selben Aufruf geschrieben, B.InvCommit), Geben / Nehmen nur in complete() der
-- zwei Netz-Zeitaktionen (B.InvPutComplete / B.InvTakeComplete), Tod -> alles auf den Boden (B.InvDrop aus B.Close).
-- Reihenfolge = Schutz: Geben "erst lesen, dann nehmen + Gegenprobe, dann gutschreiben"; Nehmen "erst bauen + Ankunft per contains, dann
-- austragen". Zwischen dem Nehmen/Ankommen und dem Festschreiben steht kein Engine-Aufruf, der scheitern koennte.
-- Kein Inhalt am Tier: Wachsen, Aussehen, Unstuck, Mitfahren, entladene Gegend, Besitzer offline -- es gibt nichts umzuziehen.
-- Kevin 13.11.: alles tragen (verlustfrei, shared/BanditsNPCBearInvRules.lua), hoechstens 1000 Stueck (B.CFG.invMaxItems) UND Gewicht, ansehen ueberall,
-- geben/nehmen nur daneben, Tod -> Boden, frisst selbst ab 50 % Hunger (B.InvEatStep), Sandbox BearCarryPercent.
-- Mehrspieler: nur der Server rechnet, nimmt, baut, wirft ab; der Client nennt nur Bezuege (Gegenstand der Zeitaktion, Satz-Nr) -> kein Kick
-- (sendRemove/sendAdd nur hier, NPC Crew CLAUDE.md:1606-1621). Pruef-Tor G1 NICHT bestanden (f4/GATES.md: jeder Client ersetzt die ModData seines
-- Spielers am Server per ObjectModData-Paket, Vanilla selbst bei jedem Hotbar-Wechsel): im MP wird die Kopie WEDER geschrieben NOCH gelesen
-- (B.CFG.invCopyMP = false); MP-Rest-Luecke = Server-Absturz zwischen Spieler-Speichern (alle 180 s) und Welt-Speichern (BAU_KERN.md, Frage fuer Kevin).
-- G6: der Spieler-Puffer fasst im SP hoechstens 2 MB -> Byte-Waage ueber alle Kopien eines Spielers (B.CFG.invCopyBytes).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local K = {}                        -- interne Helfer (eine Tabelle statt vieler Locals)

B._invWatch = B._invWatch or {}     -- [pkey] = { id, untilMs }: Fenster offen -> nach jeder Aenderung die Liste neu
B._invAskAt = B._invAskAt or {}     -- [pkey] = ms der letzten Bitte "InvList" (Drossel)
B._invPushAt = B._invPushAt or {}   -- [id] = ms der letzten gesendeten Liste
B._invPend = B._invPend or {}       -- [id] = true: Liste gedrosselt, geht im naechsten Hirn-Takt hinaus
B._invHealed = B._invHealed or {}   -- [pkey] = Spieler-Objekt, fuer das der Abgleich gelaufen ist (neues Objekt = neu einloggen / laden)
B._invSnap = B._invSnap or {}       -- [id] = { inv, bag } (nur Probe-Datei: Absturz nachstellen)
B._invEatShow = B._invEatShow or {} -- [id] = ms bis "eat" in der Sicht
B._invTypeOk = B._invTypeOk or {}   -- [typ] = true/false (gibt es den Typ? Sitzung, Deckel 256)
B._invTypeN = B._invTypeN or 0
B._invDropAt = B._invDropAt or nil  -- ms des letzten Blicks auf die Abwurf-Liste
B._invOrphRep = B._invOrphRep or {} -- [pkey] = true: Waisen dieser Sitzung gemeldet

B.INV_COPY = "BanditsNPCBearInv"    -- Schluessel der Kopie in der Spieler-ModData (grep 13.11.: frei in T, NC, Vanilla, Bandits)

local function cfg(k, d)
    local v = B.CFG and tonumber(B.CFG[k]) or nil
    if v == nil then return d end
    return v
end

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function isTame(st)
    return st == "tame" or st == "missing"
end

-- Meldung { k, t, v, tone } an einen Spieler; bd = "big" ueber B.NoteBd (Big-Fassung, wo es eine gibt).
function K.tell(player, rec, k, t, v, tone, extra)
    if not player then return end
    local n = { k = k, t = t, v = v, tone = tone }
    if type(extra) == "table" then
        for kk, vv in pairs(extra) do n[kk] = vv end
    end
    if rec ~= nil then B.NoteBd(n, rec) end
    B.Tell(player, n)
end

function K.why(player, rec, k, t, v)
    K.tell(player, rec, k, t, v, "bad", nil)
end

-- ---------------------------------------------------------------------------
-- Daten
-- ---------------------------------------------------------------------------
function K.inv(rec)
    local inv = rec.inv
    if type(inv) ~= "table" then
        inv = { v = 1, r = 0, n = 0, it = {} }
        rec.inv = inv
    end
    if type(inv.it) ~= "table" then inv.it = {} end
    inv.r = num(inv.r) or 0
    inv.n = num(inv.n) or 0
    return inv
end

function K.nrNum(nr)
    if type(nr) ~= "string" then return 0 end
    return tonumber(string.sub(nr, 2)) or 0
end

-- Last, Stueck, Saetze -- je Fassung r gemerkt (die Sicht fragt oft).
function K.sum(rec)
    local inv = rec.inv
    if type(inv) ~= "table" then return 0, 0, 0 end
    local s = B.Ses(rec.id)
    local c = s.invSum
    if type(c) == "table" and c.r == inv.r and c.inv == inv and c.bag == rec.bag then return c.kg, c.n, c.recs, c.bytes end
    local kg, n, recs = B.InvSum(inv)
    local bytes = B.InvBytes(inv) + B.InvBytes(rec.bag) + 64
    s.invSum = { r = inv.r, inv = inv, bag = rec.bag, kg = kg, n = n, recs = recs, bytes = bytes }
    return kg, n, recs, bytes
end

-- Bytes aller Kopien eines Spielers (alle seine Baeren; f4/GATES.md G6: Spieler-Puffer SP hoechstens 2 MB, darueber wird er NICHT gespeichert).
function K.ownerBytes(pkey)
    local reg = B.Reg()
    local n = 0
    if not reg or pkey == nil then return 0 end
    for _, rec in pairs(reg.cubs) do
        if rec.owner == pkey and type(rec.inv) == "table" then
            local _, _, _, b = K.sum(rec)
            n = n + (b or 0)
        end
    end
    return n
end

-- Passt ein neuer Satz noch in die Spieler-Kopie? (nur wenn die Kopie geschrieben wird -- Einzelspieler)
function K.copyRoom(rec, s)
    if not K.copyOn() then return true end
    return K.ownerBytes(rec.owner) + B.InvBytes(s) + 16 <= cfg("invCopyBytes", 524288)
end

-- Halbstark erreicht? (Packtaschen tragen ab hier; B.CFG.stageAt[1], innere Groesse aus B.StatsOf)
function K.half(rec)
    if B.StatsOf == nil then return false end
    local at = B.CFG.stageAt
    local edge = type(at) == "table" and num(at[1]) or 0.75
    return (num(B.StatsOf(rec).s) or 0) >= edge - 0.000001
end

-- Kapazitaet in kg (PLAN_F4.md 3): Groessen-Traglast x Sandbox BearCarryPercent / 100, +bagAdd mit Packtaschen ab halbstark.
function B.InvCap(rec)
    if type(rec) ~= "table" or B.StatsOf == nil then return 0 end
    local carry = num(B.StatsOf(rec).carry) or 0
    return B.InvCapOf(carry, B.Opt("BearCarryPercent"), rec.bag ~= nil, K.half(rec))
end

function B.InvLoad(rec)
    local kg, _, _ = K.sum(rec)
    return kg
end

function B.InvCount(rec)
    local _, n, _ = K.sum(rec)
    return n
end

-- Ist der Besitzer im Spiel? Nur dann aendert sich das Inventar (die Kopie liegt bei ihm, PLAN_F4.md 2.4).
function B.InvCan(rec)
    if type(rec) ~= "table" or rec.owner == nil or not isTame(rec.st) then return false end
    local p, _ = B.PlayerByKey(rec.owner)
    return p ~= nil
end

-- Platz fuer ein Stueck mit Gewicht w (kg)?
function B.InvRoom(rec, w)
    local kg, n, _ = K.sum(rec)
    if n + 1 > cfg("invMaxItems", 1000) then return false end
    return kg + (num(w) or 0) <= B.InvCap(rec) + 0.000001
end

-- Gibt es den Typ (noch)? ScriptManager.instance:getItem(Text): Vanilla client/ContextMenuCode.lua:67 (Pruef-Tor G4: am Server). Je Typ gemerkt.
function K.typeOk(t)
    local ok = B._invTypeOk[t]
    if ok ~= nil then return ok end
    if B._invTypeN >= 256 then
        B._invTypeOk = {}
        B._invTypeN = 0
    end
    ok = ScriptManager.instance:getItem(t) ~= nil
    B._invTypeOk[t] = ok
    B._invTypeN = B._invTypeN + 1
    return ok
end

-- ---------------------------------------------------------------------------
-- Spieler-Kopie (PLAN_F4.md 2.4). player:getModData(): Vanilla server/XpSystem/XpUpdate.lua:333 (Schreiber),
-- shared/TimedActions/Fishing/TimedActions/ISPickupFishAction.lua:43. Schluessel "u<Kennzeichen>" (Text; string.format "%.0f" -- ganze Zahl
-- ohne Exponent, wie die Kennzeichen-Anzeige der Test-Mod).
-- ---------------------------------------------------------------------------
function K.ukey(u)
    local n = num(u)
    if n == nil then return nil end
    return "u" .. string.format("%.0f", n)
end

function K.copyRoot(player, create)
    if not player then return nil end
    local md = player:getModData()
    if type(md) ~= "table" then return nil end
    local root = md[B.INV_COPY]
    if type(root) ~= "table" then
        if not create then return nil end
        root = {}
        md[B.INV_COPY] = root
    end
    return root
end

-- Liest der Abgleich die Kopie? Einzelspieler immer; Mehrspieler nur nach Pruef-Tor G1 (B.CFG.invCopyMP).
function K.copyOn()
    if B.IsSP() then return true end
    return B.CFG.invCopyMP == true
end

-- Kopie (neu) verknuepfen: dieselben Tabellen wie im Register (kein Kopieren je Aenderung; beim Speichern schreibt die Engine je Wurzel
-- eine eigene Fassung -- der Spieler-Puffer also immer den Stand, der zu SEINEM Inventar passt, PLAN_F4.md 2.2).
function K.link(rec, player)
    if not K.copyOn() then return end
    local key = K.ukey(rec.u)
    if key == nil then return end
    local root = K.copyRoot(player, true)
    if root == nil then return end
    local inv = K.inv(rec)
    root[key] = { u = rec.u, id = rec.id, r = inv.r, inv = inv, bag = rec.bag, at = B.Now() }
end

-- Nachbesserung F4 (Befund C3, f4/NACHBESSERUNG.md): ERST abgleichen, DANN aendern. Nach dem Laden kann die Kopie beim Besitzer neuer sein als das
-- Register (Absturz nach dem Spieler-Speichern); K.link wuerde sie durch das alte Register ersetzen -> Gegenstand weg. Jeder Weg, der das
-- Inventar aendert (Geben/Nehmen ueber K.check, Fressen, F5, Tod), ruft das VOR seiner Aenderung; B.InvCommit ruft es noch einmal als Netz
-- (dann ist es ein Leerlauf). owner = Spieler-Objekt des Besitzers oder nil (B.PlayerByKey: im Einzelspieler der erste lokale Spieler).
function K.healFirst(rec, owner)
    if not K.copyOn() or type(rec) ~= "table" or rec.owner == nil then return end
    if owner == nil then owner = B.PlayerByKey(rec.owner) end
    if owner == nil then return end
    if B._invHealed[rec.owner] ~= owner then B.InvHeal(owner) end
end

-- Nachbesserung F4 (Befund C7): Fassung + 1 und Kopie neu verknuepfen, BEVOR ein Weg Stueck fuer Stueck baut und austraegt (Nehmen, Tod). Wirft
-- die Engine mitten in der Schleife, tragen Register und Kopie schon die NEUE Fassung mit dem Teilstand (die Tabellen sind geteilt) -- beim
-- Laden gewinnt dann die Kopie, die zum Spieler-Inventar passt, statt das alte Register mit gleicher Fassung (sonst doppelt).
function K.bump(rec, owner)
    local inv = K.inv(rec)
    inv.r = inv.r + 1
    if owner == nil and rec.owner ~= nil then owner = B.PlayerByKey(rec.owner) end
    if owner ~= nil then K.link(rec, owner) end
end

-- Die EINE Schreibstelle (PLAN_F4.md 2.4): Fassung + 1, Kopie beim Besitzer, Register festschreiben, Liste an ein offenes Fenster.
-- owner = Spieler-Objekt des Besitzers (nil: B.PlayerByKey). Ohne Besitzer im Spiel: nur Register (der Aufrufer hat B.InvCan gefragt;
-- einzige Ausnahme ist der Tod, B.InvDrop).
function B.InvCommit(rec, owner)
    if type(rec) ~= "table" then return end
    if owner == nil and rec.owner ~= nil then owner = B.PlayerByKey(rec.owner) end
    K.healFirst(rec, owner)         -- Netz (C3); die Aufrufer haben vor ihrer Aenderung schon abgeglichen
    local inv = K.inv(rec)
    inv.r = inv.r + 1
    if owner ~= nil then K.link(rec, owner) end
    B.Commit(rec)
    B.InvPushSoon(rec)
end

-- ---------------------------------------------------------------------------
-- Abgleich nach dem Laden / Einloggen (PLAN_F4.md 2.4). force = Probe-Datei (laeuft auch ein zweites Mal).
-- ---------------------------------------------------------------------------
function K.hasStuff(rec)
    if rec.bag ~= nil then return true end
    local inv = rec.inv
    if type(inv) ~= "table" or type(inv.it) ~= "table" then return false end
    for _, _ in pairs(inv.it) do return true end
    return false
end

function B.InvHealRec(rec, player)
    if type(rec) ~= "table" or not isTame(rec.st) or rec.owner == nil then return end
    if player == nil then player = B.PlayerByKey(rec.owner) end
    if player == nil then return end
    local key = K.ukey(rec.u)
    if key == nil then return end
    local root = K.copyRoot(player, false)
    local c = root and root[key] or nil
    local inv = K.inv(rec)
    if not K.copyOn() then return end
    if type(c) ~= "table" then
        -- keine Kopie (neuer Charakter, erste Aenderung nach F4): das Register gilt, Kopie (neu) schreiben
        if K.hasStuff(rec) then K.link(rec, player) end
        return
    end
    local cr = num(c.r) or 0
    if c.dead == true then
        -- Grabstein: der Baer ist gestorben, seine Sachen liegen schon am Boden; das Register ist von davor
        if K.hasStuff(rec) then
            B.Err("inv: " .. tostring(rec.id) .. " has a grave mark in the owner's copy -- its things already lie on the ground, cleared")
        end
        rec.inv = { v = 1, r = cr, n = inv.n, it = {} }
        rec.bag = nil
        K.link(rec, player)
        B.Commit(rec)
        return
    end
    if cr ~= inv.r then
        local it2 = B.InvCopy(type(c.inv) == "table" and c.inv.it or {})
        local bag2 = nil
        if c.bag ~= nil then bag2 = B.InvCopy(c.bag) end
        if it2 == nil or (c.bag ~= nil and bag2 == nil) then
            B.Err("inv: " .. tostring(rec.id) .. " owner's copy is unreadable -- the register stays (r " .. tostring(inv.r) .. ")")
            return
        end
        local n2 = math.max(num(type(c.inv) == "table" and c.inv.n or nil) or 0, inv.n)
        B.Err("inv: " .. tostring(rec.id) .. " restored from the owner's copy (r " .. tostring(inv.r) .. " -> " .. tostring(cr) .. ")")
        rec.inv = { v = 1, r = cr, n = n2, it = it2 }
        rec.bag = bag2
        K.fixInv(rec, B.Reg())
        K.link(rec, player)
        B.Commit(rec)
        B.InvPushSoon(rec)
        return
    end
    K.link(rec, player)
end

function B.InvHeal(player, force)
    if not player or not B.IsWriter() then return end
    local reg = B.Reg()
    if not reg then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    -- im Einzelspieler mit mehreren lokalen Spielern liegt die Kopie nur beim ersten (B.PlayerByKey) -- die anderen gleichen nicht ab
    local main, _ = B.PlayerByKey(pkey)
    if main ~= player then return end
    if not force and B._invHealed[pkey] == player then return end
    B._invHealed[pkey] = player
    local live = {}
    for _, rec in pairs(reg.cubs) do
        if rec.owner == pkey and isTame(rec.st) then
            B.InvHealRec(rec, player)
            local k = K.ukey(rec.u)
            if k ~= nil then live[k] = true end
        end
    end
    local root = K.copyRoot(player, false)
    if root == nil then return end
    local gone = {}
    for k, c in pairs(root) do
        if not live[k] and type(c) == "table" and c.dead == true then gone[#gone + 1] = k end
        if type(c) ~= "table" then gone[#gone + 1] = k end
    end
    for i = 1, #gone do root[gone[i]] = nil end
end

-- Waisen (Kopie ohne Eintrag, nicht Grabstein): nie Gegenstaende erzeugen (eine Waise kann ein Doppel sein, PLAN_F4.md 2.4); nach dem
-- Heil-Fenster EINE Fehlerzeile je Spieler und Sitzung; Deckel invWaifMax (die aelteste faellt mit Fehlerzeile).
function K.orphans(player, pkey)
    local root = K.copyRoot(player, false)
    local reg = B.Reg()
    if root == nil or reg == nil then return end
    local live = {}
    for _, rec in pairs(reg.cubs) do
        local k = K.ukey(rec.u)
        if k ~= nil then live[k] = true end
    end
    local list = {}
    for k, c in pairs(root) do
        if not live[k] and type(c) == "table" and c.dead ~= true then list[#list + 1] = { k = k, at = num(c.at) or 0 } end
    end
    if #list == 0 then return end
    if not B._invOrphRep[pkey] then
        B._invOrphRep[pkey] = true
        B.Err("inv: " .. tostring(#list) .. " copy/copies of bear packs without a bear for " .. tostring(pkey)
            .. " (kept as data, nothing created)")
    end
    if #list > cfg("invWaifMax", 8) then
        table.sort(list, function(a, b) return a.at < b.at end)
        for i = 1, #list - cfg("invWaifMax", 8) do
            B.Err("inv: dropped the oldest orphan copy " .. tostring(list[i].k) .. " of " .. tostring(pkey))
            root[list[i].k] = nil
        end
    end
end

-- ---------------------------------------------------------------------------
-- Laden: Register pruefen (aus B.InitRegistry). Nie still loeschen: ein kaputter Satz kommt nach reg.invLost.
-- ---------------------------------------------------------------------------
function K.lost(reg, key, it, bag, why)
    if reg == nil then return end
    if type(reg.invLost) ~= "table" then reg.invLost = {} end
    local lost = reg.invLost
    local k = tostring(key) .. "@" .. string.format("%.0f", getTimestampMs())   -- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456
    lost[k] = { it = it, bag = bag, at = B.Now(), why = tostring(why) }
    B.Err("inv: kept unusable bear packs data as " .. k .. " (" .. tostring(why) .. ")")
    local list = {}
    for kk, e in pairs(lost) do list[#list + 1] = { k = kk, at = type(e) == "table" and num(e.at) or 0 } end
    if #list > cfg("invLostMax", 8) then
        table.sort(list, function(a, b) return a.at < b.at end)
        for i = 1, #list - cfg("invLostMax", 8) do
            B.Err("inv: dropped the oldest lost data " .. tostring(list[i].k))
            lost[list[i].k] = nil
        end
    end
end

function K.fixInv(rec, reg)
    if rec.inv == nil and rec.bag == nil then return end
    if rec.inv ~= nil and type(rec.inv) ~= "table" then
        K.lost(reg, rec.u or rec.id, rec.inv, nil, "inventory of " .. tostring(rec.id) .. " was no table")
        rec.inv = nil
    end
    if rec.inv ~= nil then
        local inv = K.inv(rec)
        local bad = {}
        local top = inv.n
        for nr, s in pairs(inv.it) do
            local ok = type(nr) == "string" and type(s) == "table" and type(s.t) == "string" and num(s.k) ~= nil and s.k >= 1
                and num(s.w) ~= nil and s.w >= 0
            if ok then
                s.k = math.floor(s.k)
                if K.nrNum(nr) > top then top = K.nrNum(nr) end
            else
                bad[#bad + 1] = nr
            end
        end
        for i = 1, #bad do
            K.lost(reg, rec.u or rec.id, { [tostring(bad[i])] = inv.it[bad[i]] }, nil, "broken record in " .. tostring(rec.id))
            inv.it[bad[i]] = nil
        end
        inv.n = top
    end
    if rec.bag ~= nil and (type(rec.bag) ~= "table" or type(rec.bag.t) ~= "string") then
        K.lost(reg, rec.u or rec.id, nil, rec.bag, "packs of " .. tostring(rec.id) .. " unreadable")
        rec.bag = nil
    end
end

-- Aus B.InitRegistry (server/BanditsNPCBearRegistry.lua): je Eintrag; Listen des Registers klemmen.
function B.InvFix(rec, reg)
    if type(reg) == "table" then
        if reg.invLost ~= nil and type(reg.invLost) ~= "table" then reg.invLost = nil end
        if reg.invDrop ~= nil and type(reg.invDrop) ~= "table" then reg.invDrop = nil end
    end
    if type(rec) ~= "table" then return end
    K.fixInv(rec, reg)
end

-- Aus B.InitRegistry, BEVOR ein unlesbarer Eintrag geht: sein Inhalt wird aufbewahrt (nie still geloescht, nie gedruckt).
function B.InvLostAdd(reg, id, rec)
    if type(rec) ~= "table" then return end
    if rec.inv == nil and rec.bag == nil then return end
    local it = type(rec.inv) == "table" and rec.inv.it or rec.inv
    K.lost(reg, rec.u or id, it, rec.bag, "unreadable entry " .. tostring(id))
end

-- ---------------------------------------------------------------------------
-- Pruefungen fuer Geben und Nehmen (PLAN_F4.md 6.2 Schritt 1-2). Rueckgabe: rec oder nil (dann schon gemeldet).
-- B.HandCheck: server/BanditsNPCBearServer.lua (Schreiber, Art, in der Welt, lebt, Abstand < reach, Eintrag).
-- character:getVehicle(): Vanilla server/Vehicles/VehicleCommands.lua:11.
-- ---------------------------------------------------------------------------
function K.check(character, animal)
    local hc = B.HandCheck
    if hc == nil then return nil end
    local rec = hc(character, animal)
    if not rec then return nil end
    local pkey = B.PlayerKey(character)
    if pkey == nil or rec.owner ~= pkey or rec.st ~= "tame" then
        K.why(character, nil, "UI_BN_Bear_Why_NotOwner")
        return nil
    end
    -- Nachbesserung F4 (Befund C6): im Einzelspieler teilen sich alle lokalen Spieler den Schluessel B.SP_KEY; die Kopie (und ihr Abgleich nach
    -- einem Absturz) liegt nur beim ERSTEN (B.PlayerByKey, wie B.InvHeal). Gaebe der zweite etwas, laege die Kopie in SEINER ModData und ginge
    -- nach einem Absturz verloren -> nur der erste lokale Spieler gibt und nimmt (ansehen duerfen alle). Mehrspieler: Schluessel = Konto.
    if B.IsSP() then
        local main, _ = B.PlayerByKey(pkey)
        if main ~= character then
            K.why(character, rec, "UI_BN_Bear_Why_InvMain")
            return nil
        end
    end
    if rec.ride ~= nil then
        K.why(character, rec, "UI_BN_Bear_Why_Riding")
        return nil
    end
    if character:getVehicle() ~= nil then
        K.why(character, nil, "UI_BN_Bear_Why_InCar")
        return nil
    end
    local fs = B.FightState and B.FightState(rec) or nil
    if fs == "fight" or fs == "retreat" then
        K.why(character, rec, "UI_BN_Bear_Why_InvFight")
        return nil
    end
    if not B.InvCan(rec) then
        K.why(character, rec, "UI_BN_Bear_Why_NotOwner")
        return nil
    end
    B.InvHeal(character)            -- vor jeder Aenderung: ist der Abgleich nach dem Laden schon gelaufen?
    return rec
end

-- Ein Stueck vom Spieler nehmen (Form takeOne, server/BanditsNPCBearServer.lua; Vanilla shared/Camping/TimedActions/ISAddFuelAction.lua:66-68).
-- removeAttachedItem(item): Vanilla shared/TimedActions/ISTransferAction.lua:87 (Hotbar). Rueckgabe true nur, wenn es danach WIRKLICH weg ist.
function K.takeFrom(character, item)
    character:removeAttachedItem(item)
    local tk = B.TakeOne
    if tk == nil then return false end
    return tk(character, item)
end

-- Angezogen? isEquipped(item): Vanilla shared/TimedActions/ISTransferAction.lua:88; getPrimaryHandItem: server/BuildingObjects/ISEmptyGraves.lua:18;
-- getSecondaryHandItem: client/Farming/CFarming_Interact.lua:265. In der Hand ist nicht "angezogen" (removeFromHands loest es).
function K.worn(character, item)
    if not character:isEquipped(item) then return false end
    if character:getPrimaryHandItem() == item or character:getSecondaryHandItem() == item then return false end
    return true
end

-- Satz eintragen (stapeln oder neue Nr). Rueckgabe: nr.
function K.insert(rec, s)
    local inv = K.inv(rec)
    for nr, e in pairs(inv.it) do
        if B.InvSame(e, s) then
            e.k = (num(e.k) or 0) + 1
            return nr
        end
    end
    inv.n = inv.n + 1
    local nr = "s" .. string.format("%d", inv.n)
    s.k = 1
    inv.it[nr] = s
    return nr
end

-- ---------------------------------------------------------------------------
-- Geben (PLAN_F4.md 6.2). Aus BanditsNPCBearPutAction:complete() -- im MP am Server mit dem Gegenstand des SERVERS. mode "inv" | "bag".
-- ---------------------------------------------------------------------------
function B.InvPutComplete(character, animal, item, mode)
    if not B.IsWriter() or not character or not item then return false end
    local rec = K.check(character, animal)
    if not rec then return false end
    if not character:getInventory():contains(item) then        -- Vanilla shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6
        K.why(character, nil, "UI_BN_Bear_Why_NoItem")
        return false
    end
    if K.worn(character, item) then
        K.why(character, nil, "UI_BN_Bear_Why_InvWorn")
        return false
    end
    local s, whyKey, detail = B.InvRead(item)
    if s == nil then
        B.Log("inv: " .. tostring(rec.id) .. " refuses " .. tostring(item:getFullType()) .. " (" .. tostring(detail) .. ")")
        K.why(character, rec, whyKey or B.INV_LOSSY)       -- rec: Big-Fassung beim grossen Koerper (Nachbesserung P10)
        return false
    end
    if mode == "bag" then
        if s.t ~= (B.CFG.bagType or "NPCCrew.BearPacks") then
            K.why(character, nil, "UI_BN_Bear_Why_NoItem")
            return false
        end
        if rec.bag ~= nil then
            K.why(character, rec, "UI_BN_Bear_Why_InvHasPacks")
            return false
        end
        if not K.half(rec) then
            K.why(character, nil, "UI_BN_Bear_Why_InvCub")
            return false
        end
    else
        local kg, n, _ = K.sum(rec)
        if n + 1 > cfg("invMaxItems", 1000) then
            K.why(character, rec, "UI_BN_Bear_Why_InvCap", "num", cfg("invMaxItems", 1000))
            return false
        end
        local cap = B.InvCap(rec)
        if kg + (num(s.w) or 0) > cap + 0.000001 then
            local left = cap - kg
            if left < 0 then left = 0 end
            K.why(character, rec, "UI_BN_Bear_Why_InvFull", "name", string.format("%.1f", math.floor(left * 10) / 10))
            return false
        end
        if not K.copyRoom(rec, s) then
            K.why(character, rec, "UI_BN_Bear_Why_InvData")
            return false
        end
    end
    -- Schritt 6: nehmen + Gegenprobe. Scheitert es, wird NICHTS gutgeschrieben.
    if not K.takeFrom(character, item) then return false end
    -- Schritt 7: ab hier ist das Stueck weg -- im selben Aufruf eintragen und festschreiben, ohne Engine-Wurf dazwischen
    if mode == "bag" then
        s.k = 1
        rec.bag = s
        B.InvCommit(rec, character)
        K.tell(character, rec, "UI_BN_Bear_Note_PacksOn", nil, nil, "good", nil)
    else
        K.insert(rec, s)
        B.InvCommit(rec, character)
        K.tell(character, nil, "UI_BN_Bear_Note_InvPut", "item", s.t, nil, { w = 1, nm = s.nm })
    end
    B.Log("inv: " .. tostring(rec.id) .. " got " .. tostring(s.t) .. " (" .. tostring(mode) .. ")")
    return true
end

-- ---------------------------------------------------------------------------
-- Nehmen (PLAN_F4.md 6.3). nr = Satz-Nr oder "bag", k = Anzahl (hoechstens invTakeMax je Aktion).
-- hasRoomFor(Spieler, Gegenstand): Vanilla client/Foraging/ISBaseIcon.lua:127. AddItem(Gegenstand) + sendAddItemToContainer(inv, Gegenstand):
-- Vanilla server/Fishing/BuildingObjects/FishingNet.lua:152-153. Ankunft per contains (nie am Rueckgabewert, NPC Crew CLAUDE.md:1685-1690).
-- ---------------------------------------------------------------------------
-- arrived(): traegt das angekommene Stueck aus dem Register aus -- VOR sendAddItemToContainer, damit auch ein Wurf beim Senden nie ein Stueck
-- doppelt laesst (es liegt dann im Server-Inventar und ist schon ausgetragen).
-- Grund, warum ein Satz nicht zurueckgebaut wurde: "room" -> deine Tasche ist voll; "field <Modul>" -> ein Feld laesst sich hier nicht
-- verlustfrei setzen (z. B. Farbton im Mehrspieler, Nachbesserung C4; eine Zutat fehlt, C9) -> "nicht ohne Verlust"; sonst Typ fehlt.
function K.whyBuild(character, rec, why)
    if why == "room" then
        K.why(character, nil, "UI_BN_Bear_Why_InvRoom")
    elseif type(why) == "string" and string.sub(why, 1, 6) == "field " then
        K.why(character, rec, B.INV_LOSSY)
    else
        K.why(character, nil, "UI_BN_Bear_Why_InvUnknown")
    end
end

function K.give(character, s, arrived)
    local item, why = B.InvBuild(s)
    if item == nil then return nil, why end
    local inv = character:getInventory()
    if not inv:hasRoomFor(character, item) then return nil, "room" end
    inv:AddItem(item)
    if not inv:contains(item) then
        B.Err("inv: built " .. tostring(s.t) .. " did not arrive in the inventory, nothing taken out")
        return nil, "arrive"
    end
    arrived()
    sendAddItemToContainer(inv, item)
    return item, nil
end

-- Dauer der Take-Aktion beim Schreiber (Nachbesserung F4, Befund C12): kg aus dem Satz im Register statt aus der Zahl des Clients -- mit DERSELBEN
-- Rundung wie die Fenster-Zeile (B.InvRow w, 2 Nachkommastellen) x Stueck, damit ein ehrlicher Client genau dieselbe Dauer rechnet. Nur lesen,
-- keine Nebenwirkung (B.RecOf heilt aus dem Spiegel -- deshalb hier nur die Sitzungs-Tabelle B._s). nil = kein Satz / kein Eintrag (dann gilt
-- die Zahl der Aktion; complete() lehnt in dem Fall ohnehin ab).
function B.InvTakeKg(animal, nr, k)
    if not B.IsWriter() or animal == nil or type(nr) ~= "string" or nr == "bag" then return nil end
    local reg = B.Reg()
    if not reg then return nil end
    local rec = nil
    for id, ss in pairs(B._s) do
        if ss.obj == animal then
            rec = reg.cubs[id]
            break
        end
    end
    if type(rec) ~= "table" or type(rec.inv) ~= "table" or type(rec.inv.it) ~= "table" then return nil end
    local s = rec.inv.it[nr]
    if type(s) ~= "table" then return nil end
    local n = math.floor(num(k) or 1)
    local have = math.floor(num(s.k) or 0)
    if n > have then n = have end
    if n > cfg("invTakeMax", 50) then n = cfg("invTakeMax", 50) end
    if n < 1 then return nil end
    return (math.floor((num(s.w) or 0) * 100 + 0.5) / 100) * n
end

function B.InvTakeComplete(character, animal, nr, k)
    if not B.IsWriter() or not character or type(nr) ~= "string" then return false end
    local rec = K.check(character, animal)
    if not rec then return false end
    if nr == "bag" then
        local bag = rec.bag
        if type(bag) ~= "table" then
            K.why(character, nil, "UI_BN_Bear_Why_InvGone")
            return false
        end
        local kg, _, _ = K.sum(rec)
        local capNo = B.InvCapOf(num(B.StatsOf(rec).carry) or 0, B.Opt("BearCarryPercent"), false, false)
        if kg > capNo + 0.000001 then
            K.why(character, rec, "UI_BN_Bear_Why_InvPacks")
            return false
        end
        if not K.typeOk(bag.t) then
            K.why(character, nil, "UI_BN_Bear_Why_InvUnknown")
            return false
        end
        -- C7: neue Fassung VOR dem Bauen; bei Ankunft die Kopie OHNE Taschen neu verknuepfen (rec.bag ist kein geteiltes Feld der Kopie)
        K.bump(rec, character)
        local item, why = K.give(character, bag, function()
            rec.bag = nil
            K.link(rec, character)
        end)
        if item == nil then
            K.whyBuild(character, rec, why)
            return false
        end
        B.InvCommit(rec, character)
        K.tell(character, rec, "UI_BN_Bear_Note_PacksOff", nil, nil, nil, nil)
        return true
    end
    local inv = K.inv(rec)
    local s = inv.it[nr]
    local want = math.floor(num(k) or 0)
    local have = math.floor(num(type(s) == "table" and s.k or nil) or 0)
    if type(s) ~= "table" or want < 1 or have < 1 then
        K.why(character, nil, "UI_BN_Bear_Why_InvGone")
        return false
    end
    -- Nachbesserung F4 (Befund C15): ist der Satz inzwischen kleiner (der Baer hat gefressen), nimmt die Aktion den Rest statt ganz abzulehnen
    if want > have then want = have end
    if want > cfg("invTakeMax", 50) then want = cfg("invTakeMax", 50) end
    if not K.typeOk(s.t) then
        K.why(character, nil, "UI_BN_Bear_Why_InvUnknown")
        return false
    end
    K.bump(rec, character)          -- C7: neue Fassung VOR dem ersten AddItem (jeder Teilstand traegt sie)
    local got, stop = 0, nil
    -- je angekommenem Stueck SOFORT austragen (genau so viele, wie angekommen sind; auch ein Wurf mitten in der Schleife laesst nichts doppelt)
    local function arrived()
        got = got + 1
        s.k = s.k - 1
        if s.k <= 0 then inv.it[nr] = nil end
    end
    for _ = 1, want do
        local item, why = K.give(character, s, arrived)
        if item == nil then
            stop = why
            break
        end
    end
    if got == 0 then
        K.whyBuild(character, rec, stop)
        return false
    end
    B.InvCommit(rec, character)
    if got < want then
        K.tell(character, nil, "UI_BN_Bear_Note_InvTookSome", "item", s.t, "bad", { w = got, x = want, nm = s.nm })
    else
        K.tell(character, nil, "UI_BN_Bear_Note_InvTook", "item", s.t, nil, { w = got, nm = s.nm })
    end
    B.Log("inv: " .. tostring(rec.id) .. " gave " .. tostring(got) .. " x " .. tostring(s.t))
    return true
end

-- ---------------------------------------------------------------------------
-- Tod / Ende (PLAN_F4.md 10, Kevin Antwort 3): aus B.Close VOR dem Loeschen des Eintrags. Alles als echte Gegenstaende auf die Kachel des Tiers
-- (sonst rec.x/y/z), Packtaschen mit. Kachel nicht geladen -> reg.invDrop (abwerfen, sobald geladen). Typ fehlt -> reg.invLost (nie geloescht).
-- square:AddWorldInventoryItem(Gegenstand, Zahl, Zahl, Zahl) (Objekt-Form, sendet selbst): Vanilla shared/TimedActions/Animals/ISMilkAnimal.lua:46
-- (animal:getSquare()), server/Camping/SCampfireGlobalObject.lua:143; Lage-Zufall ZombRandFloat(Zahl, Zahl): shared/TimedActions/ISTransferAction.lua:68;
-- getCell():getGridSquare(x, y, z): server/Animal/ISPickDungCursor.lua:104 (wie server/BanditsNPCBearWorld.lua B.AreaLoaded).
-- ---------------------------------------------------------------------------
function K.dropAll(sq, it, bag, key)
    local n = 0
    local reg = B.Reg()
    local list = {}
    if type(it) == "table" then
        for nr, s in pairs(it) do list[#list + 1] = { nr = nr, s = s } end
    end
    if type(bag) == "table" then list[#list + 1] = { nr = "bag", s = bag } end
    for i = 1, #list do
        local s = list[i].s
        local left = math.floor(num(s.k) or 1)
        while left > 0 do
            local item, _ = B.InvBuild(s)
            if item == nil then break end
            -- erst austragen, dann ablegen: ein Wurf der Engine NACH dem Ablegen (Senden) laesst nichts doppelt; liegt das Stueck danach nicht am
            -- Boden (getWorldItem(): V:client/ISUI/ISInventoryPane.lua:2337), kommt es in den Satz zurueck. Rest (BAU_KERN.md): ein Wurf VOR dem
            -- Ablegen kostet hoechstens dieses eine Stueck.
            left = left - 1
            s.k = left
            sq:AddWorldInventoryItem(item, ZombRandFloat(0.1, 0.9), ZombRandFloat(0.1, 0.9), 0)
            if item:getWorldItem() == nil then
                left = left + 1
                s.k = left
                B.Err("inv: " .. tostring(s.t) .. " did not land on the ground, kept in its record")
                break
            end
            n = n + 1
        end
        if left > 0 then
            local keep = B.InvCopy(s)
            if keep ~= nil then keep.k = left end
            K.lost(reg, key, { [tostring(list[i].nr)] = keep }, nil, "could not rebuild " .. tostring(s.t) .. " at the drop")
        end
    end
    return n
end

function B.InvDrop(rec, how)
    if type(rec) ~= "table" then return end
    -- C3: erst abgleichen (eine neuere Kopie beim Besitzer gehoert mit auf den Boden; sonst schriebe der Grabstein sie weg)
    if isTame(rec.st) then K.healFirst(rec, nil) end
    if not K.hasStuff(rec) then return end
    local reg = B.Reg()
    local s = B._s[rec.id]
    local a = s and s.obj or nil
    local sq = nil
    if a ~= nil and a:isExistInTheWorld() then sq = a:getSquare() end
    if sq == nil then sq = getCell():getGridSquare(math.floor(num(rec.x) or 0), math.floor(num(rec.y) or 0), math.floor(num(rec.z) or 0)) end
    local inv = K.inv(rec)
    local it, bag = inv.it, rec.bag
    local key = rec.u or rec.id
    local n = 0
    if sq ~= nil then
        n = K.dropAll(sq, it, bag, key)
    elseif reg ~= nil then
        if type(reg.invDrop) ~= "table" then reg.invDrop = {} end
        reg.invDrop[#reg.invDrop + 1] = { x = math.floor(num(rec.x) or 0), y = math.floor(num(rec.y) or 0), z = math.floor(num(rec.z) or 0),
            it = it, bag = bag, at = B.Now(), key = tostring(key) }
        if #reg.invDrop > cfg("invDropMax", 16) then
            B.Err("inv: " .. tostring(#reg.invDrop) .. " drops wait for unloaded ground (nothing is deleted)")
        end
    end
    -- Inhalt ist jetzt am Boden bzw. in der Abwurf-Liste: Register leer, Kopie wird Grabstein (ein Absturz danach bringt nichts zurueck)
    rec.inv = { v = 1, r = inv.r + 1, n = inv.n, it = {} }
    rec.bag = nil
    local owner = rec.owner and B.PlayerByKey(rec.owner) or nil
    local root = (owner and K.copyOn()) and K.copyRoot(owner, true) or nil
    local ukey = K.ukey(rec.u)
    if root ~= nil and ukey ~= nil then root[ukey] = { u = rec.u, id = rec.id, dead = true, r = rec.inv.r, at = B.Now() } end
    if owner ~= nil and (n > 0 or sq == nil) then K.tell(owner, rec, "UI_BN_Bear_Note_InvDrop", nil, nil, "bad", nil) end
    B.Log("inv: " .. tostring(rec.id) .. " (" .. tostring(how) .. ") dropped " .. tostring(n) .. " thing(s)" .. (sq == nil and " -- ground not loaded, kept in the drop list" or ""))
end

-- Abwurf-Liste (Langsam): sobald die Kachel geladen ist.
function K.dropPending()
    local reg = B.Reg()
    if not reg or type(reg.invDrop) ~= "table" or #reg.invDrop == 0 then return end
    local keep = {}
    for i = 1, #reg.invDrop do
        local e = reg.invDrop[i]
        local sq = type(e) == "table" and getCell():getGridSquare(e.x, e.y, e.z) or nil
        if sq ~= nil then
            local n = K.dropAll(sq, e.it, e.bag, e.key)
            B.Log("inv: dropped " .. tostring(n) .. " waiting thing(s) at " .. tostring(e.x) .. "," .. tostring(e.y))
        elseif type(e) == "table" then
            keep[#keep + 1] = e
        end
    end
    reg.invDrop = keep
end

-- ---------------------------------------------------------------------------
-- Liste fuer das Fenster (PLAN_F4.md 4.4, 16; schnittstelle.md K4): seitenweise, sortiert nach Typ, dann Satz-Nr; NUR an den Besitzer.
-- sendServerCommand(Spieler, Modul, Befehl, Tabelle): Vanilla server/BuildingObjects/ISBuildUtil.lua:291. Einzelspieler: B.OnInv (Client) direkt.
-- Groesse: eine Seite mit invPageMax (100) Zeilen ist hoechstens ~45 KB (Rechnung f4/BAU_KERN.md 6; Puffer je Verbindung 1.000.000 Bytes,
-- J:UdpConnection.<init> Offset 16 "ldc 1000000" -> ByteBuffer.allocate, ohne Wachsen).
-- ---------------------------------------------------------------------------
function K.sendList(player, rec)
    local inv = K.inv(rec)
    local now = B.Now()
    local order = {}
    for nr, s in pairs(inv.it) do
        if type(s) == "table" then order[#order + 1] = { nr = nr, t = tostring(s.t), n = K.nrNum(nr), s = s } end
    end
    table.sort(order, function(a, b)
        if a.t ~= b.t then return a.t < b.t end
        return a.n < b.n
    end)
    local kg, cnt, recs = K.sum(rec)
    local cap = B.InvCap(rec)
    local per = math.floor(cfg("invPageMax", 100))
    if per < 1 then per = 100 end
    local maxB = cfg("invPageBytes", 200000)
    local bag = nil
    if type(rec.bag) == "table" then bag = B.InvRow("bag", rec.bag, now, K.typeOk(rec.bag.t)) end
    -- erst in Seiten teilen (hoechstens per Zeilen UND maxB Bytes je Seite), dann senden (pn steht vorher fest)
    local pages = { {} }
    local pb = 0
    for i = 1, #order do
        local e = order[i]
        local row = B.InvRow(e.nr, e.s, now, K.typeOk(e.t))
        local rb = B.InvBytes(row) + 9
        local cur = pages[#pages]
        if #cur >= per or (#cur > 0 and pb + rb > maxB) then
            cur = {}
            pages[#pages + 1] = cur
            pb = 0
        end
        cur[#cur + 1] = row
        pb = pb + rb
    end
    local pn = #pages
    for pg = 1, pn do
        local it = pages[pg]
        local page = { id = rec.id, r = inv.r, pg = pg, pn = pn, n = recs, cnt = cnt, cap = math.floor(cap + 0.000001),
            load = math.floor(kg * 10 + 0.5) / 10, bag = bag }
        if kg > cap + 0.000001 then page.over = true end
        if #it > 0 then page.it = it end
        if isServer() then
            sendServerCommand(player, B.CMD, "Inv", page)
        elseif not isClient() then
            local f = B.OnInv
            if f then f(page, player) end
        end
    end
    B._invPushAt[rec.id] = getTimestampMs()
    B._invPend[rec.id] = nil
end

-- Bitte "InvList" { id } (B.Handle). Nur der Besitzer, Drossel invListMs; zugleich "Fenster offen" bis invWatchMs. Fremder Baer: still nichts.
-- Kevin Antwort 2: ansehen von ueberall -- auch vermisst, mitfahrend, nicht geladen.
function B.HandleInvList(player, args)
    if not player or not B.IsWriter() or type(args) ~= "table" or type(args.id) ~= "string" then return end
    local reg = B.Reg()
    if not reg then return end
    local rec = reg.cubs[args.id]
    local pkey = B.PlayerKey(player)
    if type(rec) ~= "table" or pkey == nil or rec.owner ~= pkey or not isTame(rec.st) then return end
    local ms = getTimestampMs()
    local last = B._invAskAt[pkey]
    if last ~= nil and ms - last >= 0 and ms - last < cfg("invListMs", 500) then return end
    B._invAskAt[pkey] = ms
    B._invWatch[pkey] = { id = rec.id, untilMs = ms + cfg("invWatchMs", 60000) }
    B.InvHeal(player)
    K.sendList(player, rec)
end

-- Nach einer Aenderung: ist das Fenster des Besitzers offen, die Liste neu (gedrosselt; Rest im Hirn-Takt).
function B.InvPushSoon(rec)
    if type(rec) ~= "table" or rec.owner == nil then return end
    local w = B._invWatch[rec.owner]
    local ms = getTimestampMs()
    if type(w) ~= "table" or w.id ~= rec.id or ms > (num(w.untilMs) or 0) then return end
    local last = B._invPushAt[rec.id]
    if last ~= nil and ms - last >= 0 and ms - last < cfg("invListMs", 500) then
        B._invPend[rec.id] = true
        return
    end
    local p, _ = B.PlayerByKey(rec.owner)
    if p then K.sendList(p, rec) end
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_F4.md 4.3; schnittstelle.md K3) -- aus viewEntry. Besitzer: ivW ivC ivN ivK ivR ivX bag; alle: eat.
-- ---------------------------------------------------------------------------
function B.InvView(rec, t, pkey, ms)
    if type(rec) ~= "table" or type(t) ~= "table" or not isTame(rec.st) then return end
    ms = num(ms) or getTimestampMs()
    local show = B._invEatShow[rec.id]
    if show ~= nil and ms < show then t.eat = true end
    if pkey == nil or rec.owner ~= pkey then return end
    local kg, n, recs = K.sum(rec)
    local cap = B.InvCap(rec)
    t.ivW = math.floor(kg * 10 + 0.5) / 10
    t.ivC = math.floor(cap + 0.000001)
    t.ivN = recs
    t.ivK = n
    t.ivR = type(rec.inv) == "table" and (num(rec.inv.r) or 0) or 0
    if kg > cap + 0.000001 then t.ivX = true end
    if rec.bag ~= nil then t.bag = true end
end

-- ---------------------------------------------------------------------------
-- Kern-Aufrufe fuer F5 (PLAN_F4.md 11) -- nur Schreiber.
-- ---------------------------------------------------------------------------
function B.InvFind(rec, test)
    local out = {}
    if type(rec) ~= "table" or type(rec.inv) ~= "table" or type(rec.inv.it) ~= "table" then return out end
    for nr, s in pairs(rec.inv.it) do
        if type(s) == "table" and (test == nil or test(s, nr)) then out[#out + 1] = nr end
    end
    table.sort(out, function(a, b) return K.nrNum(a) < K.nrNum(b) end)
    return out
end

-- Bis zu k Stueck eines Satzes austragen (gefressen o. ae.; baut KEINEN Gegenstand). Rueckgabe: ausgetragen. Festschreiben: der Aufrufer (B.InvCommit).
function B.InvTakeUnits(rec, nr, k, why)
    if type(rec) ~= "table" then return 0 end
    K.healFirst(rec, nil)           -- C3: erst abgleichen, dann austragen (sonst ueberschriebe das Festschreiben eine neuere Kopie)
    if type(rec.inv) ~= "table" or type(rec.inv.it) ~= "table" then return 0 end
    local s = rec.inv.it[nr]
    if type(s) ~= "table" then return 0 end
    local want = math.floor(num(k) or 0)
    local have = math.floor(num(s.k) or 0)
    if want > have then want = have end
    if want <= 0 then return 0 end
    s.k = have - want
    if s.k <= 0 then rec.inv.it[nr] = nil end
    B.Log("inv: " .. tostring(rec.id) .. " -" .. tostring(want) .. " " .. tostring(s.t) .. " (" .. tostring(why) .. ")")
    return want
end

-- Ein Gegenstand, der in KEINEM Behaelter liegt (F5: ein wie Vanillas Fischnetz gebauter Fisch), wird ein Satz. Rueckgabe: bool.
function B.InvAddItem(rec, item, why)
    if not B.IsWriter() or type(rec) ~= "table" or item == nil or not B.InvCan(rec) then return false end
    K.healFirst(rec, nil)           -- C3: erst abgleichen, dann eintragen (ein Abgleich NACH dem Eintragen koennte den Satz verdraengen)
    local s, _, detail = B.InvRead(item)
    if s == nil then
        B.Log("inv: " .. tostring(rec.id) .. " cannot keep " .. tostring(item:getFullType()) .. " (" .. tostring(detail) .. ")")
        return false
    end
    if not B.InvRoom(rec, s.w) or not K.copyRoom(rec, s) then return false end
    K.insert(rec, s)
    B.InvCommit(rec, nil)
    B.Log("inv: " .. tostring(rec.id) .. " +" .. tostring(s.t) .. " (" .. tostring(why) .. ")")
    return true
end

-- ---------------------------------------------------------------------------
-- Frisst selbst aus dem Inventar (Kevin Antwort 6; PLAN_F4.md 11): aus B.NeedsSlow je Langsam-Takt. Ab needHungry (50) bis unter needPeckish (25),
-- hoechstens ein Stueck je invEatGapMin Spielminuten; nur Baerenfutter (fc beim Geben, B.FoodClass), nie Verdorbenes (Alter jetzt), Lieblingsfutter zuerst.
-- ---------------------------------------------------------------------------
local RANK = { fav = 1, ok = 2, snack = 3 }

function B.InvEatStep(rec, now, players)
    if type(rec) ~= "table" or rec.st ~= "tame" or rec.ride ~= nil or rec.down ~= nil then return end
    if type(rec.inv) ~= "table" or B.NeedEat == nil or not (B.NeedsOn and B.NeedsOn()) then return end
    local s = B.Ses(rec.id)
    local hun = num(rec.nH) or 0
    if hun >= cfg("needHungry", 50) then s.invEat = true end
    if hun < cfg("needPeckish", 25) then s.invEat = nil end
    if not s.invEat then return end
    if not B.InvCan(rec) or B.FindAnimal(rec) == nil then return end
    if B.IsLying and B.IsLying(rec) then return end
    K.healFirst(rec, nil)           -- C3: erst abgleichen (eine neuere Kopie nach dem Laden), dann waehlen und fressen
    if type(rec.inv) ~= "table" or type(rec.inv.it) ~= "table" then return end
    local fs = B.FightState and B.FightState(rec) or nil
    if fs == "fight" or fs == "retreat" then return end
    now = num(now) or B.Now()
    local lastAt = num(s.invEatAt)
    if lastAt ~= nil and now >= lastAt and now - lastAt < cfg("invEatGapMin", 10) / 60 - 0.0001 then return end
    local best, bestR, bestN = nil, 99, 0
    for nr, x in pairs(rec.inv.it) do
        local r = type(x) == "table" and RANK[x.fc] or nil
        if r ~= nil and (num(x.k) or 0) >= 1 and B.InvFresh(x, now) ~= 2 and x.bu ~= 1 then
            local nn = K.nrNum(nr)
            if r < bestR or (r == bestR and nn < bestN) then best, bestR, bestN = nr, r, nn end
        end
    end
    if best == nil then return end
    local x = rec.inv.it[best]
    local meals = num(x.ml) or 0
    local t, nm = x.t, x.nm
    if B.InvTakeUnits(rec, best, 1, "eat") ~= 1 then return end
    s.invEatAt = now
    B.NeedEat(rec, meals, "inv")
    B.InvCommit(rec, nil)
    B._invEatShow[rec.id] = getTimestampMs() + cfg("invEatShowMs", 4000)
    B.Touch(rec)
    local noteAt = num(s.invEatNoteAt)
    if noteAt == nil or now < noteAt or now - noteAt >= cfg("needNoteH", 6) then
        s.invEatNoteAt = now
        local p, _ = B.PlayerByKey(rec.owner, players)
        if p then K.tell(p, rec, "UI_BN_Bear_Note_InvAte", "item", t, nil, { w = 1, nm = nm }) end
    end
end

-- ---------------------------------------------------------------------------
-- Hirn-Takt (aus brainTickBody, server/BanditsNPCBearServer.lua): Abgleich je Spieler-Objekt, gedrosselte Listen, Ende des Fress-Bilds,
-- Abwurf-Liste (je 5 s), Waisen-Meldung nach dem Heil-Fenster.
-- ---------------------------------------------------------------------------
function B.InvBrain(ms, players)
    local reg = B.Reg()
    if not reg then return end
    ms = num(ms) or getTimestampMs()
    players = players or B.Players()
    for i = 1, #players do
        local e = players[i]
        if B._invHealed[e.key] ~= e.p then B.InvHeal(e.p) end
        if ms >= (B._healUntil or 0) and not B._invOrphRep[e.key] and K.copyOn() then
            local main, _ = B.PlayerByKey(e.key, players)
            if main == e.p then K.orphans(e.p, e.key) end
        end
    end
    local pend = {}
    for id, _ in pairs(B._invPend) do pend[#pend + 1] = id end
    for i = 1, #pend do
        local rec = reg.cubs[pend[i]]
        if type(rec) == "table" then
            B._invPushAt[pend[i]] = nil
            B.InvPushSoon(rec)
        end
        B._invPend[pend[i]] = nil
    end
    local done = {}
    for id, untilMs in pairs(B._invEatShow) do
        if ms >= untilMs then done[#done + 1] = id end
    end
    for i = 1, #done do
        B._invEatShow[done[i]] = nil
        local rec = reg.cubs[done[i]]
        if type(rec) == "table" then B.Touch(rec) end
    end
    if B._invDropAt == nil or ms - B._invDropAt < 0 or ms - B._invDropAt >= 5000 then
        B._invDropAt = ms
        K.dropPending()
    end
end

-- ---------------------------------------------------------------------------
-- Probe-Datei der Test-Mod (nie kopiert, nie im Spielcode benutzt). Tier-Regel "probeweg": B.InvSet / B.InvSnap nur dort.
-- ---------------------------------------------------------------------------
function B.InvSnap(rec)
    if type(rec) ~= "table" then return false end
    B._invSnap[rec.id] = { inv = B.InvCopy(rec.inv), bag = B.InvCopy(rec.bag) }
    return true
end

-- Absturz nachstellen (nur Einzelspieler): das Register-Inventar auf den gemerkten Vorstand -- die Kopie beim Spieler bleibt (kein B.InvCommit).
function B.InvSet(rec, inv, bag)
    if type(rec) ~= "table" or not B.IsSP() then return false end
    if inv == nil then
        local snap = B._invSnap[rec.id]
        if type(snap) ~= "table" then return false end
        inv, bag = B.InvCopy(snap.inv), B.InvCopy(snap.bag)
    end
    rec.inv = inv
    rec.bag = bag
    B.Commit(rec)
    return true
end

-- Kopie des Baeren beim Spieler entfernen (nur Einzelspieler): der naechste Abgleich findet keine und schreibt sie aus dem Register neu
-- ("Register gewinnt"). Den Schluessel nennt nur diese Datei (Tier-Regel invCopy).
function B.InvCopyOff(player, rec)
    if not B.IsSP() or type(rec) ~= "table" then return false end
    local root = K.copyRoot(player, false)
    local key = K.ukey(rec.u)
    if root == nil or key == nil or root[key] == nil then return false end
    root[key] = nil
    return true
end

function B.InvInfo(rec, player)
    local t = {}
    if type(rec) ~= "table" then return t end
    local kg, n, recs = K.sum(rec)
    t.id, t.recs, t.items, t.load, t.cap = rec.id, recs, n, B.Round1(kg), B.Round1(B.InvCap(rec))
    t.r = type(rec.inv) == "table" and rec.inv.r or nil
    t.bag = type(rec.bag) == "table" and rec.bag.t or nil
    local root = K.copyRoot(player, false)
    local key = K.ukey(rec.u)
    local c = root and key and root[key] or nil
    if type(c) == "table" then
        t.copyR = c.r
        t.copyDead = c.dead == true
    end
    local orph = 0
    if root ~= nil then
        local reg = B.Reg()
        for k, cc in pairs(root) do
            local found = false
            for _, r2 in pairs(reg and reg.cubs or {}) do
                if K.ukey(r2.u) == k then found = true end
            end
            if not found and type(cc) == "table" and cc.dead ~= true then orph = orph + 1 end
        end
    end
    t.orphans = orph
    local reg = B.Reg()
    local lost = 0
    if reg and type(reg.invLost) == "table" then
        for _, _ in pairs(reg.invLost) do lost = lost + 1 end
    end
    t.lost = lost
    t.drops = reg and type(reg.invDrop) == "table" and #reg.invDrop or 0
    t.snap = B._invSnap[rec.id] ~= nil
    return t
end

B.InvKern = K                       -- nur fuer die Attrappen (attrappe/f4_kern); kein Spielcode liest es
