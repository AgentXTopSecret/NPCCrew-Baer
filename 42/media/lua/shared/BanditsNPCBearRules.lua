--
-- NPC Crew -- Baer, reine Regeln (B1a, PLAN_ZAEHMEN.md 2, 3.2, 6.2.2, 6.7).
--
-- Keine Engine in dieser Datei: nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (auf dem
-- Register-Eintrag) und beim Client (auf dem Sicht-Eintrag bzw. B.View.me) -- eine Antwort je Frage.
-- Gelesen wird nur B.Opt (Sandbox) und B.CFG (feste Stellwerte) aus shared/BanditsNPCBear.lua, zur Laufzeit.
--
-- Zustaende st: "new" (erschienen) -> "shy" (entdeckt) -> "fed" (angefuettert, an bond gebunden) -> "tame" (gezaehmt,
-- owner gesetzt); "missing" nur fuer gezaehmte. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function isTame(st)
    return st == "tame" or st == "missing"
end

-- Resttage einer Sperre, aufgerundet (mindestens 1).
local function lockDays(lockUntil, now)
    local d = math.ceil((lockUntil - now) / 24 - 0.000001)
    if d < 1 then d = 1 end
    return d
end

-- Laeuft fuer diesen Spieler eine Sperre nach dem Tod seines Baeren? Rueckgabe: boolean, Resttage.
local function locked(slots, now)
    local lock = tonumber(slots.lockUntil) or 0
    if lock > now then return true, lockDays(lock, now) end
    return false, nil
end

-- ---------------------------------------------------------------------------
-- Punkte (Plan 3.2): Grundpunkte x Futterfaktor x Mischfaktor
-- ---------------------------------------------------------------------------

-- kind = "feed" / "pet"; class = "fav" / "ok" / "snack" (nur beim Fuettern); last = vorige gewertete Handlung oder nil.
-- Rueckgabe: Punkte (eine Nachkommastelle), mixed (die vorige Handlung war die andere und es gibt dafuer mehr).
function B.Gain(kind, class, last)
    local base = 0
    local factor = 1
    if kind == "feed" then
        base = B.Opt("BearTameFeedPoints")
        if class == "fav" then
            factor = 1 + B.Opt("BearTameFavoriteBonus") / 100
        elseif class == "snack" then
            factor = B.CFG.snack
        end
    elseif kind == "pet" then
        base = B.Opt("BearTamePetPoints")
    else
        return 0, false
    end
    local mix = 1
    local mixed = false
    if (last == "feed" or last == "pet") and last ~= kind then
        local bonus = B.Opt("BearTameMixBonus")
        if bonus > 0 then
            mix = 1 + bonus / 100
            mixed = true
        end
    end
    return B.Round1(base * factor * mix), mixed
end

-- Ist der Balken voll UND oft genug gefuettert? Dann gezaehmt (owner = bond). Sonst haelt der Balken bei 99.
function B.TameCheck(rec, now)
    if not rec or isTame(rec.st) then return false end
    local tame = tonumber(rec.tame) or 0
    if tame >= 100 and rec.st == "fed" and rec.bond ~= nil and (tonumber(rec.fedN) or 0) >= B.Opt("BearTameMinFeedings") then
        rec.tame = 100
        rec.st = "tame"
        rec.owner = rec.bond
        rec.tamedAt = now
        return true
    end
    if tame > 99 then rec.tame = 99 end
    return false
end

-- Eine gewertete Handlung gutschreiben. Aendert rec. Rueckgabe { gain, mixed, first, tamed, need }:
-- first = erste Fuetterung (bond gesetzt, st = "fed"); tamed = jetzt gezaehmt; need = fehlende Fuetterungen, wenn der Balken
-- bei 99 haelt. Am zahmen Jungen gibt es keine Punkte, nur die Abklingzeit.
function B.ApplyGain(rec, pkey, kind, class, now)
    local res = { gain = 0, mixed = false, first = false, tamed = false, need = 0 }
    if not rec or (kind ~= "feed" and kind ~= "pet") then return res end
    local wasTame = isTame(rec.st)
    if not wasTame then
        local pts, mixed = B.Gain(kind, class, rec.last)
        res.gain = pts
        res.mixed = mixed
        if kind == "feed" then
            if rec.bond == nil then rec.bond = pkey end
            if rec.st == "new" or rec.st == "shy" then
                rec.st = "fed"
                res.first = true
            end
            rec.fedN = (tonumber(rec.fedN) or 0) + 1
        else
            rec.petN = (tonumber(rec.petN) or 0) + 1
        end
        rec.tame = B.Round1((tonumber(rec.tame) or 0) + pts)
    end
    rec.last = kind
    if kind == "feed" then rec.feedAt = now else rec.petAt = now end
    if not wasTame then
        local full = rec.tame >= 100
        res.tamed = B.TameCheck(rec, now)
        if full and not res.tamed then
            local need = B.Opt("BearTameMinFeedings") - (tonumber(rec.fedN) or 0)
            if need < 1 then need = 1 end
            res.need = need
        end
    end
    return res
end

-- Rest der Abklingzeit in Spielstunden (0 = bereit). kind = "feed" / "pet".
function B.WaitLeft(rec, kind, now)
    if not rec then return 0 end
    local at, mins
    if kind == "feed" then
        at = tonumber(rec.feedAt)
        mins = B.Opt("BearFeedCooldownMinutes")
    else
        at = tonumber(rec.petAt)
        mins = B.Opt("BearPetCooldownMinutes")
    end
    if at == nil or mins <= 0 then return 0 end
    local left = at + mins / 60 - now
    if left <= 0.0005 then return 0 end
    return left
end

-- ---------------------------------------------------------------------------
-- Pruefungen. Rueckgabe: ok, whyKey, whyVal (Reststunden bei Wartezeit, Resttage bei Sperre, sonst nil).
-- rec darf Register- oder Sicht-Eintrag sein; slots hat die Form von B.SlotsOf bzw. B.View.me.
-- ---------------------------------------------------------------------------

function B.CheckFeed(rec, pkey, slots, now)
    if not rec then return false, "UI_BN_Bear_Why_Gone", nil end
    slots = slots or {}
    if isTame(rec.st) then
        if rec.owner ~= pkey then return false, "UI_BN_Bear_Why_NotOwner", nil end
    elseif rec.bond ~= nil then
        if rec.bond ~= pkey then return false, "UI_BN_Bear_Why_Other", nil end
    else
        -- noch niemandes Junges: mit dieser Fuetterung bindet es sich an pkey -- dafuer braucht er einen freien Platz
        if (tonumber(slots.bears) or 0) >= (tonumber(slots.maxBears) or 1) then return false, "UI_BN_Bear_Why_HasBear", nil end
        if slots.bonded ~= nil and slots.bonded ~= rec.id then return false, "UI_BN_Bear_Why_HasCub", nil end
        local isLocked, days = locked(slots, now)
        if isLocked then return false, "UI_BN_Bear_Why_Locked", days end
    end
    local left = B.WaitLeft(rec, "feed", now)
    if left > 0 then return false, "UI_BN_Bear_Why_FeedWait", left end
    return true, nil, nil
end

function B.CheckPet(rec, pkey, slots, now)
    if not rec then return false, "UI_BN_Bear_Why_Gone", nil end
    if isTame(rec.st) then
        if rec.owner ~= pkey then return false, "UI_BN_Bear_Why_NotOwner", nil end
    elseif rec.bond == nil then
        return false, "UI_BN_Bear_Why_Shy", nil
    elseif rec.bond ~= pkey then
        return false, "UI_BN_Bear_Why_Other", nil
    end
    local left = B.WaitLeft(rec, "pet", now)
    if left > 0 then return false, "UI_BN_Bear_Why_PetWait", left end
    return true, nil, nil
end

-- Darf dieser Spieler einen Koeder auslegen? now ist wahlfrei (fehlt es, die Weltstunden von jetzt): nur fuer die Sperre.
function B.CheckBait(slots, now)
    slots = slots or {}
    if B.Opt("BearBaitEnabled") ~= true then return false, "UI_BN_Bear_Bait_Off", nil end
    if slots.on == false then return false, "UI_BN_Bear_Why_Off", nil end
    if (tonumber(slots.bears) or 0) >= (tonumber(slots.maxBears) or 1) then return false, "UI_BN_Bear_Why_HasBear", nil end
    if slots.bonded ~= nil or slots.wild ~= nil then return false, "UI_BN_Bear_Why_HasCub", nil end
    if now == nil then now = B.Now() end
    local isLocked, days = locked(slots, now)
    if isLocked then return false, "UI_BN_Bear_Why_Locked", days end
    if slots.bait ~= nil then return false, "UI_BN_Bear_Bait_HasOne", nil end
    return true, nil, nil
end

-- Darf fuer diesen Spieler ein neues Junges erscheinen (Wald oder Koeder)? Den Welt-Deckel prueft der Schreiber dazu.
function B.MayAppear(slots, now)
    slots = slots or {}
    if slots.on == false then return false, "UI_BN_Bear_Why_Off", nil end
    if (tonumber(slots.bears) or 0) >= (tonumber(slots.maxBears) or 1) then return false, "UI_BN_Bear_Why_HasBear", nil end
    if slots.bonded ~= nil or slots.wild ~= nil then return false, "UI_BN_Bear_Why_HasCub", nil end
    local isLocked, days = locked(slots, now)
    if isLocked then return false, "UI_BN_Bear_Why_Locked", days end
    return true, nil, nil
end

-- Koeder-Chance in Prozent nach der n-ten gezaehlten Nacht: steigt gleichmaessig von BearBaitFirstChance auf 100 in der
-- letzten (Vorgabe 40 / 70 / 100).
function B.BaitChance(night)
    local nights = B.Opt("BearBaitNights")
    local first = B.Opt("BearBaitFirstChance")
    local n = tonumber(night) or 1
    if n < 1 then n = 1 end
    if nights <= 1 or n >= nights then return 100 end
    return first + (100 - first) * (n - 1) / (nights - 1)
end

-- ---------------------------------------------------------------------------
-- Verschwinden und Aufgabe (Plan 2)
-- ---------------------------------------------------------------------------

-- Ein Schritt der Uhr "ohne Kontakt". Fuehrt rec.idleH. contact = jemand ist nah (bei "fed": bond);
-- relevantOnline = der Finder bzw. bond ist online (nur dann laeuft die Uhr).
-- "go" = Verschwinde-Frist um (nur new / shy), "release" = Aufgabe-Frist um (nur fed), sonst "keep".
function B.VanishStep(rec, dtH, contact, relevantOnline)
    if not rec then return "keep" end
    local st = rec.st
    if st ~= "new" and st ~= "shy" and st ~= "fed" then return "keep" end
    if contact then
        rec.idleH = 0
        return "keep"
    end
    local idle = tonumber(rec.idleH) or 0
    dtH = tonumber(dtH) or 0
    if relevantOnline and dtH > 0 then idle = idle + dtH end
    rec.idleH = idle
    if st == "fed" then
        if idle >= B.CFG.abandonH then return "release" end
        return "keep"
    end
    local limit = B.Opt("BearCubVanishHours")
    if limit > 0 and idle >= limit then return "go" end
    return "keep"
end

-- "fed" -> "shy" nach der Aufgabe-Frist: bond weg, Balken halbiert, Uhr auf null. Gibt den alten bond zurueck.
function B.ReleaseBond(rec)
    if not rec or rec.st ~= "fed" then return nil end
    local old = rec.bond
    rec.bond = nil
    rec.st = "shy"
    rec.tame = B.Round1((tonumber(rec.tame) or 0) / 2)
    rec.idleH = 0
    rec.goneP = nil
    return old
end

-- ---------------------------------------------------------------------------
-- Verhalten (Plan 6.7). Erste passende Regel gewinnt.
-- c   = { st, src, x, y, hx, hy, held, sinceMoveMs, sinceCuriousMs }
-- env = { near = P|nil, lure = P|nil, mate = P|nil }, P = { key, x, y, dist, food, fast, still }
-- Rueckgabe { act, tx, ty, lead, rule }: act = "flee" / "come" / "hold" / "home" / "free"; rule = Nummer der Regel (Zusatz).
-- ---------------------------------------------------------------------------

-- Punkt im Abstand d von P auf der Geraden P -> C.
local function toward(px, py, cx, cy, d)
    local dx, dy = cx - px, cy - py
    local len = math.sqrt(dx * dx + dy * dy)
    if len < 0.001 then return px + d, py end
    return px + dx / len * d, py + dy / len * d
end

local function farFromHome(c)
    if c.hx == nil or c.hy == nil then return false end
    local dx, dy = c.x - c.hx, c.y - c.hy
    return math.sqrt(dx * dx + dy * dy) > B.CFG.homeR
end

function B.Decide(c, env)
    local cfg = B.CFG
    local near, lure, mate = env.near, env.lure, env.mate
    local st = c.st
    if st == "new" or st == "shy" then
        -- 1: jemand ohne Futter in der Hand oder im Lauf kommt zu nah -> weg, fleeDist vom Spieler fort
        if near and near.dist <= cfg.shyDist and ((not near.food) or near.fast) then
            local tx, ty = toward(c.x, c.y, c.x + (c.x - near.x), c.y + (c.y - near.y), cfg.fleeDist)
            return { act = "flee", tx = tx, ty = ty, lead = false, rule = 1 }
        end
        -- 2: jemand steht ruhig mit Futter -> heran bis comeUnfed
        if lure and lure.still and lure.dist > cfg.comeUnfed then
            local tx, ty = toward(lure.x, lure.y, c.x, c.y, cfg.comeUnfed)
            return { act = "come", tx = tx, ty = ty, lead = false, rule = 2 }
        end
        -- 3: Futter in der Naehe -> stehen bleiben und schauen
        if lure then
            return { act = "hold", lead = false, rule = 3 }
        end
        -- 4: Koeder-Junges bleibt bei seinem Platz
        if farFromHome(c) then
            return { act = "home", tx = c.hx, ty = c.hy, lead = false, rule = 4 }
        end
        -- 5: Neugier: naehert sich dem Finder bis curiousStop
        if c.hx == nil and mate and mate.dist > cfg.curiousMin and mate.dist <= cfg.curiousMax
            and (tonumber(c.sinceCuriousMs) or 0) >= cfg.curiousMs then
            local tx, ty = toward(mate.x, mate.y, c.x, c.y, cfg.curiousStop)
            return { act = "come", tx = tx, ty = ty, lead = false, rule = 5 }
        end
    elseif st == "fed" or st == "tame" then
        -- 6: bond / Besitzer steht ruhig mit Futter -> heran bis comeFed; das zahme Junge nimmt seine Heimat mit
        if lure and lure.still and lure.dist > cfg.comeFed then
            local tx, ty = toward(lure.x, lure.y, c.x, c.y, cfg.comeFed)
            return { act = "come", tx = tx, ty = ty, lead = (st == "tame"), rule = 6 }
        end
        -- 7: Futter ganz nah -> stehen bleiben; ebenso, wenn bond / Besitzer in Reichweite zum Fuettern oder Streicheln steht --
        -- sonst loeste dieser Takt die Sperre einer laufenden Zeitaktion (Nachbesserung B7)
        if lure and lure.dist <= cfg.shyDist then
            return { act = "hold", lead = false, rule = 7 }
        end
        if mate and mate.dist < cfg.reach then
            return { act = "hold", lead = false, rule = 7 }
        end
        -- 8: zurueck in die Gegend der Heimat
        if farFromHome(c) then
            return { act = "home", tx = c.hx, ty = c.hy, lead = false, rule = 8 }
        end
    end
    -- 9: nichts zu tun; eine eigene Sperre wird geloest, die Engine laesst das Tier wandern
    return { act = "free", lead = false, rule = 9 }
end
