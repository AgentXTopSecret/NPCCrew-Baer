if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Heilen von Hand mit einem Verband (F2 = B5a, PLAN_F2.md 0.12, 2.5, 4.3; Kevin ENT:267-272 "wir koennen den baeren
-- manuel heilen").
--
-- Vierte Zeitaktion nach dem gespielten Fuetter-Weg: BanditsNPCBearMendAction:complete() (shared/TimedActions, OBERFLAECHE) ruft EINEN
-- Schreiber-Kern B.MendComplete, der alles prueft und GENAU EIN Stueck nimmt (B.TakeOne = takeOne in server/BanditsNPCBearServer.lua, Form
-- Vanilla shared/Camping/TimedActions/ISAddFuelAction.lua:66-68) und im selben Aufruf gutschreibt. Abbruch der Aktion = nichts verbraucht
-- (stop/forceStop rufen den Kern nie). Kein zweiter Verband, solange einer wirkt (Why_Bandaged) -- so nimmt auch ein zweites complete()
-- nichts. Im Mehrspieler baut der Server die Aktion mit SEINEM Gegenstand neu und ruft complete(); der Client glaubt nichts.
-- Wirkung: rec.bndH = jetzt + BearBandageHours (Spielstunden), rec.bndR = BearBandageHeal x B.MendPower(Staerke) (%/h, geklemmt 0..50);
-- B.GrowSlow (server/BanditsNPCBearGrow.lua) heilt zusaetzlich B.MendRateOf -- auch am Boden (dort nur das). Gespeichert in Register und
-- Spiegel. Name "Mend" (nicht "Heal": server/BanditsNPCBearHeal.lua ist die Register-Selbstheilung C1). NPC-Heiler: nur eine Naht
-- (NAEHTE.md, spaeter B.MendBy derselben Form mit NPC Crews Heiler-Job).
-- Engine-Aufrufe hier (Fundstelle am Aufruf): item:getType(), item:isCanBandage(), item:getBandagePower(), character:getInventory(),
-- inv:contains(item). Ladefolge: server/ alphabetisch; fremde Funktionen nur zur Laufzeit ueber B.X. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function cfg(key, def)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return def end
    return v
end

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Welche Gruende eine Zahl tragen (Stunden Rest des wirkenden Verbands).
local WHY_NUM = { UI_BN_Bear_Why_Bandaged = true }

local function tellWhy(character, rec, whyKey, whyVal)
    local n = note(whyKey, nil, nil, "bad")
    if WHY_NUM[whyKey] then
        n.t = "num"
        n.v = whyVal
    end
    B.Tell(character, B.NoteBd(n, rec))
end

-- Zusatz-Heilung des wirkenden Verbands in Prozent je Spielstunde (0 ohne / abgelaufen).
function B.MendRateOf(rec, now)
    if type(rec) ~= "table" then return 0 end
    local h, r = num(rec.bndH), num(rec.bndR)
    if h == nil or r == nil or r <= 0 then return 0 end
    now = num(now) or B.Now()
    if now >= h then return 0 end
    return r
end

-- Sicht (4.7): bnd = Stunden Verband uebrig (0,1; mindestens 0,1, solange er wirkt) -- aus viewEntry.
function B.MendView(rec, t, now)
    if type(t) ~= "table" then return end
    now = num(now) or B.Now()
    if B.MendRateOf(rec, now) <= 0 then return end
    local left = B.Round1(num(rec.bndH) - now)
    if left < 0.1 then left = 0.1 end
    t.bnd = left
end

-- Pruefung ohne Wirkung (rein bis auf die Gegenstands-Fragen). Rueckgabe ok, whyKey, whyVal.
-- item:getType() + string.match(..., "Dirty"): Vanilla shared/TimedActions/ISApplyBandage.lua:113 (schmutziger Verband);
-- item:isCanBandage(): client/ISUI/ISInventoryPaneContextMenu.lua:169; item:getBandagePower() > 0: client/XpSystem/ISUI/ISHealthPanel.lua:1154.
function B.MendCheck(rec, pkey, item, now)
    if type(rec) ~= "table" or rec.st ~= "tame" or pkey == nil or rec.owner ~= pkey then
        return false, "UI_BN_Bear_Why_NotOwner", nil
    end
    if item == nil then return false, "UI_BN_Bear_Why_NoBandage", nil end
    -- Nachbesserung F2 B7: Sandbox BearBandageHeal 0 -> ein Verband wirkt nicht -> ablehnen, nichts wird verbraucht (rote Linie)
    if cfg("bandageHeal", 6) <= 0 then return false, "UI_BN_Bear_Why_BandageOff", nil end    -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3): fester Wert 6 (Text unerreichbar)
    local kind = item:getType()
    if type(kind) == "string" and string.match(kind, "Dirty") then return false, "UI_BN_Bear_Why_Dirty", nil end
    if not item:isCanBandage() or (num(item:getBandagePower()) or 0) <= 0 then return false, "UI_BN_Bear_Why_NoBandage", nil end
    if (num(rec.hp) or 1) >= cfg("mendRefuseFull", 0.995) then return false, "UI_BN_Bear_Why_Healthy", nil end
    now = num(now) or B.Now()
    if B.MendRateOf(rec, now) > 0 then
        local h = math.ceil(num(rec.bndH) - now - 0.000001)
        if h < 1 then h = 1 end
        return false, "UI_BN_Bear_Why_Bandaged", h
    end
    return true, nil, nil
end

-- Abschluss (2.5 Nr. 3, 6). Reihenfolge der Ablehnungen: Why_Gone / Why_Far (B.HandCheck), Why_NotOwner, Why_NoItem, Why_BandageOff,
-- Why_Dirty, Why_NoBandage, Why_Healthy, Why_Bandaged -- jede mit Meldung und OHNE Verbrauch. Dann GENAU ein Stueck (B.TakeOne prueft danach, dass
-- es wirklich weg ist) und im selben Aufruf gutschreiben. character:getInventory():contains(item): Vanilla
-- shared/TimedActions/Animals/ISFeedAnimalFromHand.lua:6. Rueckgabe: true, wenn verbunden.
function B.MendComplete(character, animal, item)
    if character == nil or animal == nil or item == nil then return false end
    local hc = B.HandCheck
    if hc == nil then return false end
    local rec = hc(character, animal)
    if not rec then return false end
    local pkey = B.PlayerKey(character)
    if rec.st ~= "tame" or rec.owner == nil or rec.owner ~= pkey then
        tellWhy(character, rec, "UI_BN_Bear_Why_NotOwner", nil)
        return false
    end
    if not character:getInventory():contains(item) then
        tellWhy(character, rec, "UI_BN_Bear_Why_NoItem", nil)
        return false
    end
    B.BodyHp(rec, animal, 0)                      -- Leben aktuell (fehlt es, aus dem Koerper)
    local now = B.Now()
    local ok, whyKey, whyVal = B.MendCheck(rec, pkey, item, now)
    if not ok then
        tellWhy(character, rec, whyKey, whyVal)
        return false
    end
    local power = num(item:getBandagePower()) or 0
    local take = B.TakeOne
    if take == nil or not take(character, item) then return false end
    -- ab hier ist das Stueck weg: gutschreiben im selben Aufruf, ohne Engine-Wurf dazwischen
    local hours = cfg("bandageHours", 8)
    local rate = cfg("bandageHeal", 6) * B.MendPower(power)
    if rate < 0 then rate = 0 end
    if rate > 50 then rate = 50 end
    rec.bndH = now + hours
    rec.bndR = rate
    B.Commit(rec)
    B.Tell(character, B.NoteBd(note("UI_BN_Bear_Note_Bandaged", "num", hours, "good"), rec))
    B.Log("mend: " .. tostring(rec.id) .. " bandaged by " .. tostring(pkey) .. " (strength " .. tostring(power) .. ", +"
        .. tostring(B.Round1(rate)) .. " %/h for " .. tostring(hours) .. " h)")
    B.FlushViews()
    return true
end
