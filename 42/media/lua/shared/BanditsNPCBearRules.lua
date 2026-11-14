--
-- NPC Crew -- Baer, reine Regeln (B1a, PLAN_ZAEHMEN.md 2, 3.2, 6.2.2, 6.7).
--
-- Keine Engine in dieser Datei: nur Zahlen, Texte, Tabellen. Dieselben Funktionen rechnen beim Schreiber (auf dem
-- Register-Eintrag) und beim Client (auf dem Sicht-Eintrag bzw. B.View.me) -- eine Antwort je Frage.
-- Gelesen wird nur B.Opt (Sandbox) und B.CFG (feste Stellwerte) aus shared/BanditsNPCBear.lua, zur Laufzeit.
-- Sandbox-Kuerzung (Kevin 12.11.2026, PLAN_AUSSEHEN.md 9): Zaehm-Punkte, Mindest-Fuetterungen, Abklingzeiten, Koeder-Naechte und
-- -Chance, Verschwinde-Frist, Mitfahr- und Folgen-Weite sind feste Werte (B.CFG, Block "Sandbox-Kuerzung"); neu das Zaehm-Tempo
-- BearTamePercent (Prozent auf die Punkte je Fuettern und Streicheln).
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

-- Fester Stellwert aus B.CFG (Sandbox-Kuerzung), sonst def (fehlender Schluessel, z. B. ein aelteres B.CFG nach Neuladen der Datei).
local function fixed(key, def)
    local c = B.CFG
    local v = c and tonumber(c[key]) or nil
    if v == nil or v ~= v then return def end
    return v
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
-- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.2): Grundpunkte = B.CFG.tameFeedPts / tamePetPts x Zaehm-Tempo BearTamePercent / 100 (bei 100 genau
-- die bisherigen 4 / 3), Lieblingsfutter und Abwechseln feste Prozent (B.CFG.tameFavBonus / tameMixBonus, je 50).
function B.Gain(kind, class, last)
    local base = 0
    local factor = 1
    local pct = tonumber(B.Opt("BearTamePercent")) or 100
    if kind == "feed" then
        base = fixed("tameFeedPts", 4) * pct / 100
        if class == "fav" then
            factor = 1 + fixed("tameFavBonus", 50) / 100
        elseif class == "snack" then
            factor = B.CFG.snack
        end
    elseif kind == "pet" then
        base = fixed("tamePetPts", 3) * pct / 100
    else
        return 0, false
    end
    local mix = 1
    local mixed = false
    if (last == "feed" or last == "pet") and last ~= kind then
        local bonus = fixed("tameMixBonus", 50)
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
    if tame >= 100 and rec.st == "fed" and rec.bond ~= nil and (tonumber(rec.fedN) or 0) >= fixed("tameMinFeeds", 3) then
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
            local need = fixed("tameMinFeeds", 3) - (tonumber(rec.fedN) or 0)
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
        mins = fixed("feedCoolMin", 120)
    else
        at = tonumber(rec.petAt)
        mins = fixed("petCoolMin", 60)
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
    -- F3 (PLAN_F3.md 5.1): am GEZAEHMTEN Baeren keine Abklingzeit mehr -- er frisst, solange er Hunger hat (K1: die volle Leiste eines
    -- Erwachsenen sind ~691 Vanilla-Hungerpunkte, ~17 Steaks); unter needFull (Nachbesserung K1 C1: 1 % -- die Sicht zeigt dann 0 %, abgerundet;
    -- Register und Sicht entscheiden darum gleich) ist er satt und lehnt ab (Vanilla bietet "Feed" auch nur bei Hunger an,
    -- client/ISUI/Animal/ISAnimalContextMenu.lua:30). Hunger aus dem Register (nH) oder der Sicht (hun), B.NeedOf. Ohne Wert (alte
    -- Sicht) oder mit BearNeedsPercent 0 (Hunger aus -- sonst waere er immer satt) gilt die bisherige Abklingzeit.
    if isTame(rec.st) and B.NeedOf ~= nil and B.NeedsOn ~= nil and B.NeedsOn() then
        local hun = B.NeedOf(rec, "hun")
        if hun ~= nil then
            if hun < fixed("needFull", 1) then return false, "UI_BN_Bear_Why_NotHungry", nil end
            return true, nil, nil
        end
    end
    local left = B.WaitLeft(rec, "feed", now)
    if left > 0 then return false, "UI_BN_Bear_Why_FeedWait", left end
    return true, nil, nil
end

-- F3 (PLAN_F3.md 5.2): darf dieser Spieler diesen Baeren traenken? Rein (Register- ODER Sicht-Eintrag; das Menue graut damit aus). Den
-- Behaelter und den Abstand prueft der Schreiber (B.DrinkComplete, server/BanditsNPCBearNeeds.lua). Rueckgabe ok, whyKey.
function B.CheckDrink(rec, pkey)
    if not rec then return false, "UI_BN_Bear_Why_Gone" end
    if rec.st ~= "tame" or rec.owner == nil or rec.owner ~= pkey then return false, "UI_BN_Bear_Why_NotOwner" end
    if rec.ride ~= nil and rec.ride ~= false then return false, "UI_BN_Bear_Why_Riding" end
    if (rec.down ~= nil and rec.down ~= false) or rec.dn == true then return false, "UI_BN_Bear_Why_Down" end
    local thr = nil
    if B.NeedOf ~= nil then thr = B.NeedOf(rec, "thr") end
    if thr == nil or thr < fixed("needFull", 1) then return false, "UI_BN_Bear_Why_NotThirsty" end
    return true, nil
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

-- Koeder-Chance in Prozent nach der n-ten gezaehlten Nacht: steigt gleichmaessig von B.CFG.baitFirstChance auf 100 in der
-- letzten (40 / 70 / 100; Sandbox-Kuerzung: feste Werte, vorher BearBaitNights / BearBaitFirstChance).
function B.BaitChance(night)
    local nights = fixed("baitMaxNights", 3)
    local first = fixed("baitFirstChance", 40)
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
    local limit = fixed("cubVanishH", 36)
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

-- Radius: c.homeR (B1b: der Schreiber gibt einem gezaehmten Jungen B.CFG.stayR mit), sonst B.CFG.homeR wie in B1a.
local function farFromHome(c)
    if c.hx == nil or c.hy == nil then return false end
    local dx, dy = c.x - c.hx, c.y - c.hy
    local r = tonumber(c.homeR) or B.CFG.homeR
    return math.sqrt(dx * dx + dy * dy) > r
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

-- ---------------------------------------------------------------------------
-- B1b: Folgen / Bleiben und Name (PLAN_B1B.md 1.2, 3.3, 5.3). Rein: keine Engine, auch der Client darf rufen.
-- ---------------------------------------------------------------------------

-- Zustand eines gezaehmten Jungen: "follow" oder "stay". Fehlt das Feld (alte Spielstaende) oder steht Unsinn darin: "stay".
-- F1 (PLAN_F1.md 0.3, 7.2): vier Modi "follow" / "stay" / "sit" / "roam" (B.MODES, shared/BanditsNPCBear.lua); Register- ODER
-- Sicht-Eintrag (gleiches Feld mode), auch der Client ruft. Fehlt B.MODES (Teilkopie), gilt dieselbe Liste hier.
local MODES_DEF = { follow = true, stay = true, sit = true, roam = true }

function B.ModeOf(rec)
    if type(rec) ~= "table" or type(rec.mode) ~= "string" then return "stay" end
    local modes = B.MODES
    if type(modes) ~= "table" then modes = MODES_DEF end
    if modes[rec.mode] == true then return rec.mode end
    return "stay"
end

-- ---------------------------------------------------------------------------
-- F1 (PLAN_F1.md 2.2-2.4, 7.2): Bleiben / Sitz / Frei herumlaufen. Rein: keine Engine, auch der Client darf rufen.
-- c   = { mode, st, x, y, hx, hy, r, gap, ownBusy, pauseOver, backTried }: Tier-Mitte x/y, Heimat-Kachel hx/hy (Mittelpunkt = Kachel-Mitte
--       hx + 0,5 / hy + 0,5; fehlt sie: die Stelle des Tiers), r = Radius von "Frei" (BearRoamRadius), gap = Zuschlag mit der
--       Koerperlaenge (B.BodyGap), ownBusy = ein eigener Laufbefehl laeuft noch (s.ownUntil), pauseOver = die Frei-Pause ist um,
--       backTried = beim Sitz wurde nach dem letzten Versatz schon einmal nachgerueckt (Zusatz, schnittstelle_aenderungen.md "F1 KERN").
-- env = wie B.Decide (lure, mate; P = { key, x, y, dist, food, fast, still }).
-- Rueckgabe { act, tx, ty, walk, lead, rule }: act "hold" (stehen/sitzen), "back" (zurueck zur Heimat bzw. in den Kreis; walk =
-- Weg bis zum Ziel <= backRunDist), "stroll" (Frei: neues eigenes Ziel suchen, der Schreiber waehlt es mit B.RoamSpot), "keep" (eigener
-- Weg laeuft weiter), "come" (Regel 6: Besitzer haelt still Futter hin, lead = die Heimat wandert mit), "none" (kein Fall fuer diese
-- Regeln: follow, nicht gezaehmt). Erste passende Regel gewinnt.
--   S1 sit : weiter als stayBack -> back (31) / eigener Weg -> keep (32) / weiter als stayNear und noch nicht nachgerueckt -> back (33)
--            / hold (34). Kein Futter-Locken (er sitzt).
--   S2 stay: Regel 6 come (6) / Regel 7 hold (7) / weiter als stayBack -> back (35) / eigener Weg -> keep (36) / hold (37)
--   S3 roam: Regel 7 hold (7) / weiter als r -> back in den Kreis (38) / eigener Weg -> keep (39) / Pause laeuft -> hold (40) /
--            stroll (41). Kein Locken mit Heimat (sonst zoege Futter ihn aus dem Bereich).
-- Ziel "back": Bleiben/Sitz die Mitte der Heimat-Kachel; Frei der Punkt r - stayBack vom Mittelpunkt auf der Linie zum Tier (zurueck
-- IN den Kreis, nicht bis zur Mitte -- so geht er von 15 Kacheln aus, Plan 8.1 Nr. 6).
-- ---------------------------------------------------------------------------
local function backTo(c, tx, ty, rule)
    local walk = B.DistXY(c.x, c.y, tx, ty) <= (tonumber(B.CFG.backRunDist) or 8)
    return { act = "back", tx = tx, ty = ty, walk = walk, lead = false, rule = rule }
end

function B.OrderDecide(c, env)
    local cfg = B.CFG
    env = env or {}
    local mode = nil
    if type(c) == "table" then mode = c.mode end
    if mode ~= "sit" and mode ~= "stay" and mode ~= "roam" then return { act = "none", rule = 0 } end
    if c.st ~= "tame" then return { act = "none", rule = 0 } end
    local lure, mate = env.lure, env.mate
    local cx, cy = c.x, c.y
    local hx, hy = tonumber(c.hx), tonumber(c.hy)
    if hx ~= nil and hy ~= nil then cx, cy = hx + 0.5, hy + 0.5 end
    local dist = B.DistXY(c.x, c.y, cx, cy)
    local stayBack = tonumber(cfg.stayBack) or 3
    if mode == "sit" then
        if dist > stayBack then return backTo(c, cx, cy, 31) end
        if c.ownBusy == true then return { act = "keep", lead = false, rule = 32 } end
        if dist > (tonumber(cfg.stayNear) or 1.5) and c.backTried ~= true then return backTo(c, cx, cy, 33) end
        return { act = "hold", lead = false, rule = 34 }
    end
    if mode == "stay" then
        local gap = tonumber(c.gap) or 0
        if lure and lure.still and lure.dist > cfg.comeFed + gap then
            local tx, ty = toward(lure.x, lure.y, c.x, c.y, cfg.comeFed + gap)
            return { act = "come", tx = tx, ty = ty, walk = false, lead = true, rule = 6 }
        end
        if (lure and lure.dist <= cfg.shyDist) or (mate and mate.dist < cfg.reach) then
            return { act = "hold", lead = false, rule = 7 }
        end
        if dist > stayBack then return backTo(c, cx, cy, 35) end
        if c.ownBusy == true then return { act = "keep", lead = false, rule = 36 } end
        return { act = "hold", lead = false, rule = 37 }
    end
    -- roam
    if (lure and lure.dist <= cfg.shyDist) or (mate and mate.dist < cfg.reach) then
        return { act = "hold", lead = false, rule = 7 }
    end
    local r = tonumber(c.r) or 12
    if dist > r then
        local inner = r - stayBack
        if inner < 0 then inner = 0 end
        local tx, ty = toward(cx, cy, c.x, c.y, inner)
        return backTo(c, tx, ty, 38)
    end
    if c.ownBusy == true then return { act = "keep", lead = false, rule = 39 } end
    if c.pauseOver ~= true then return { act = "hold", lead = false, rule = 40 } end
    return { act = "stroll", lead = false, rule = 41 }
end

local NAME_BAD = "UI_BN_Bear_Why_NameBad"

-- Zeichenklassen fuer Namen (Nachbesserung B1b A1/A2/B4: ohne string.byte, das weder Vanilla noch Bandits aufrufen).
-- Unter Kahlua schneidet string.sub Java-Zeichen (UTF-16), keine Bytes (Jar se/krka/kahlua/stdlib/StringLib.sub: String.substring),
-- und string.len zaehlt dieselben Einheiten (Vanilla verlaesst sich darauf: shared/luautils.lua:5
-- string.sub(String, 1, string.len(Start))). "<" / "<=" zwischen zwei Texten vergleicht mit String.compareTo (Jar
-- se/krka/kahlua/vm/KahluaThread, Befehle LT/LE; Texte vergleicht Vanilla so z. B.
-- client/DebugUIs/DebugMenu/Entity/ISEntityScriptsPanel.lua:149). Grenzen ueber 127 stehen als UTF-8-Bytefolge im Text
-- ("\226\128\139" = U+200B): der Kahlua-Lader macht daraus EIN Zeichen (Jar org/luaj/kahluafork/compiler/LexState.newstring:
-- new String(bytes, "UTF-8")). Die Datei bleibt reines ASCII. Laese der Lader die Folge anders, fiele nur diese Grenze aus (keine
-- falsche Ablehnung: ein Zeichen ist dann kleiner als die Folge, die mit ihm beginnt).
-- NAME_BADR: nicht druckbar -> Name abgelehnt. C0 (< " ") prueft der Code selbst.
local NAME_BADR = {
    { "\127", "\127" },                         -- DEL
    { "\194\128", "\194\159" },                 -- U+0080-U+009F C1-Steuerzeichen (z. B. U+0085 NEXT LINE)
    { "\194\173", "\194\173" },                 -- U+00AD weiches Trennzeichen (unsichtbar)
    { "\216\156", "\216\156" },                 -- U+061C arabische Richtungsmarke
    { "\225\133\159", "\225\133\160" },         -- U+115F-U+1160 Hangul-Fueller (unsichtbar)
    { "\225\160\142", "\225\160\142" },         -- U+180E mongolischer Vokaltrenner
    { "\226\128\139", "\226\128\143" },         -- U+200B-U+200F Null-Breite-Zeichen, Richtungsmarken
    { "\226\128\168", "\226\128\174" },         -- U+2028-U+202E Zeilen-/Absatztrenner, Richtungs-Umschalter (U+202E)
    { "\226\129\160", "\226\129\175" },         -- U+2060-U+206F Wortverbinder, Richtungs-Isolate (U+2066-U+2069)
    { "\227\133\164", "\227\133\164" },         -- U+3164 Hangul-Fueller
    { "\239\187\191", "\239\187\191" },         -- U+FEFF Null-Breite-Leerzeichen / BOM
    { "\239\190\160", "\239\190\160" },         -- U+FFA0 Hangul-Fueller halbbreit
    { "\239\191\185", "\239\191\187" },         -- U+FFF9-U+FFFB Anmerkungs-Steuerzeichen
    -- B1c N2 (PLAN_B1C.md 1.10, gegen_bericht_b1b.md N2)
    { "\238\128\128", "\239\163\191" },         -- U+E000-U+F8FF Privatbereich (ohne Schrift: leere Kaestchen)
    { "\239\191\188", "\239\191\189" },         -- U+FFFC-U+FFFD Objekt-Ersatz, Ersatzzeichen
}
-- B1c N2: Ersatzzeichen-Haelften U+D800-U+DFFF (Kahlua liefert ein Zeichen ueber U+FFFF als ZWEI solche Haelften, Jar
-- String.substring). Eine Haelfte allein hat kein gueltiges UTF-8-Literal -> als ECHTE Ungleichungen zwischen U+D7FF und U+E000.
local SURR_LO = "\237\159\191"                  -- U+D7FF (letztes Zeichen davor)
local SURR_HI = "\238\128\128"                  -- U+E000 (erstes Zeichen danach)
-- B1c N2: Kombinationszeichen U+0300-U+036F. Ein Name, dessen sichtbare Zeichen ALLE solche sind, zeigt nichts Lesbares.
local COMB_LO = "\204\128"                      -- U+0300
local COMB_HI = "\205\175"                      -- U+036F
-- NAME_SPACE: Leerraum -> am Rand weg, zaehlt nicht als sichtbar (ein Name nur daraus ist leer); in der Mitte erlaubt.
local NAME_SPACE = {
    { " ", " " },
    { "\194\160", "\194\160" },                 -- U+00A0 geschuetztes Leerzeichen
    { "\225\154\128", "\225\154\128" },         -- U+1680 Ogham-Leerzeichen
    { "\226\128\128", "\226\128\138" },         -- U+2000-U+200A Leerzeichen verschiedener Breite
    { "\226\128\175", "\226\128\175" },         -- U+202F schmales geschuetztes Leerzeichen
    { "\226\129\159", "\226\129\159" },         -- U+205F mittleres mathematisches Leerzeichen
    { "\227\128\128", "\227\128\128" },         -- U+3000 ideografisches Leerzeichen
}

local function inRanges(ch, list)
    for i = 1, #list do
        local r = list[i]
        if ch >= r[1] and ch <= r[2] then return true end
    end
    return false
end

-- Name pruefen und saeubern. Rueckgabe: sauberer Text oder nil, whyKey (immer "UI_BN_Bear_Why_NameBad").
-- Laenger als 4 x nameMax -> nil, bevor ein Zeichen einzeln angesehen wird (Deckel). Jedes Zeichen per string.sub: unter " ", die
-- Bereiche NAME_BADR, "<", ">" und "%" -> nil ("<"/">" gegen Rich-Text in Tooltips, "%" gegen Platzhalter in getText). Leerraum
-- (NAME_SPACE) vorn und hinten weg; nichts Sichtbares -> nil; danach laenger als B.CFG.nameMax -> nil. Druckbare Zeichen ueber 127
-- (Umlaute, Kyrillisch, Koreanisch, Chinesisch) sind erlaubt. Gedruckte ASCII-Zeichen gehen den kurzen Weg (das Namensfenster ruft
-- das je Bild). Nur string.len, string.sub und Textvergleiche.
function B.CleanName(text)
    if type(text) ~= "string" then return nil, NAME_BAD end
    local max = tonumber(B.CFG.nameMax) or 24
    local n = string.len(text)
    if n > 4 * max then return nil, NAME_BAD end
    local first, last = nil, nil
    local allComb = true                        -- B1c N2: bisher nur Kombinationszeichen gesehen (sichtbar)
    for k = 1, n do
        local ch = string.sub(text, k, k)
        local space
        if ch >= " " and ch <= "~" then
            if ch == "<" or ch == ">" or ch == "%" then return nil, NAME_BAD end
            space = (ch == " ")
            if not space then allComb = false end
        else
            if ch < " " or inRanges(ch, NAME_BADR) then return nil, NAME_BAD end
            if ch > SURR_LO and ch < SURR_HI then return nil, NAME_BAD end
            space = inRanges(ch, NAME_SPACE)
            if not space and not (ch >= COMB_LO and ch <= COMB_HI) then allComb = false end
        end
        if not space then
            if first == nil then first = k end
            last = k
        end
    end
    if first == nil then return nil, NAME_BAD end
    if allComb then return nil, NAME_BAD end
    if last - first + 1 > max then return nil, NAME_BAD end
    return string.sub(text, first, last), nil
end

-- Folgen: was soll ein folgendes Junges in diesem Hirn-Takt tun? Erste passende Regel gewinnt (Plan 1.2, Regeln 10-16).
-- c = { x, y, z } (z ganze Ebene); o = nil | { key, x, y, z, dist, car, mx, my } (naechster Besitzer; mx/my = sein Weg seit dem
-- letzten Hirn-Takt, fehlt -> 0); f = Sitzungs-Tabelle { held, orderAt, tx, ty, bestD, bestAt, bx, by, stuck, retryAt }: hier
-- fortgeschrieben werden NUR bestD, bestAt, bx, by, stuck, retryAt (orderAt / tx / ty / held setzt B.FollowStep nach dem
-- Ausfuehren). ms = Echtzeit.
-- Rueckgabe { act, why, tx, ty, rule }: act "stay" / "hold" / "run" / "keep"; why "offline" / "car" / "far" / "level" / "near" /
-- "stuck" / nil.
-- Regel 10 (Nachbesserung B1b A7): ist der Besitzer nicht da (abgemeldet, tot, nach einem Server-Neustart noch nicht verbunden),
-- WARTET das Junge (halten) und bleibt "follow" -- der Zustand ueberlebt so auch im Mehrspieler Abmelden und Neustart.
-- Vorhalt (Nachbesserung B2): Halten (Regel 14) und Ziel (Regel 16) rechnen mit dem Ort, an dem der Besitzer im naechsten Takt
-- etwa ist: sein Weg seit dem letzten Takt, gedeckelt auf followLead Kacheln. Steht er, ist das sein Ort.
-- "Steckt fest" (Nachbesserung B1): bewegt sich das Junge in followStuckMs nicht um followStuckGain AUF DEN BESITZER ZU (gemessen
-- ab seinem Ort beim letzten Fortschritt, bx/by) und wird auch der Abstand nicht um followStuckGain kleiner, gibt es nur noch je
-- followRetryMs einen Laufbefehl. Ein Junges, das frei hinter einem gehenden Besitzer herrennt, ist so nie "fest"; eines vor einer
-- geschlossenen Tuer oder an einer Wand entlang (seitlich, ohne Weg zum Besitzer) schon. Der Fortschritt wird vor Regel 15
-- gerechnet (gilt auch waehrend des Wartens); jedes Halten (Regel 10/13/14) setzt ihn zurueck.
local function resetProgress(f)
    f.bestD = nil
    f.bestAt = nil
    f.bx = nil
    f.by = nil
    f.stuck = nil
    f.retryAt = nil
end

-- Weg des Jungen seit dem letzten Fortschritt (f.bx, f.by), projiziert auf die Richtung zum Besitzer.
local function gainToward(f, c, o)
    if f.bx == nil or f.by == nil then return 0 end
    local ux, uy = o.x - f.bx, o.y - f.by
    local len = math.sqrt(ux * ux + uy * uy)
    if len < 0.001 then return 0 end
    return ((c.x - f.bx) * ux + (c.y - f.by) * uy) / len
end

-- B1c (PLAN_B1C.md 1.4, 1.6, 6.3):
--   Regel 11: Besitzer im Fahrzeug und hoechstens BearRideDistance weg -> { act = "ride" } (der Schreiber laesst es einsteigen,
--   server/BanditsNPCBearRide.lua B.RideBoard); weiter weg -> "stay" "car" wie B1b.
--   Regel 16 traegt walk: GEHEN, wenn die Reststrecke Junges -> Ziel hoechstens walkDist ist UND der Besitzer langsamer als
--   walkSpeed ist (o.dt = ms seit dem letzten Takt, fehlt -> brainMs); sonst rennen. Wechselt walk, geht sofort ein neuer Befehl.
--   Rueckfall Laerm (1.2 Schritt 5): wuchs der Abstand zum Besitzer seit dem letzten Aufruf um followFleeGrow, sofort neu (ohne
--   followMoveMs). f.lastD = Abstand dieses Aufrufs; f.walk setzt B.FollowStep nach einem Befehl.
-- B1e (PLAN_B1E.md 0.9, 1.5, 6.3): c.gap (Zuschlag mit der Koerperlaenge, B.BodyGap) kommt auf followNear, followStart und followGap;
--   c.walkSpeed (Tempo des Koerpers, B.BodyNum) ersetzt cfg.walkSpeed in der Gehen-Regel. Fehlen beide: Zahlen wie B1c.
function B.FollowDecide(c, o, f, ms)
    local cfg = B.CFG
    f = f or {}
    local gap = tonumber(c.gap) or 0
    local walkSpeed = tonumber(c.walkSpeed) or tonumber(cfg.walkSpeed) or 0
    if o == nil then
        resetProgress(f)
        f.lastD = nil
        return { act = "hold", why = "offline", rule = 10 }
    end
    local d = tonumber(o.dist) or 0
    if o.car then
        f.lastD = nil
        if d <= fixed("rideDist", 15) then return { act = "ride", rule = 11 } end
        return { act = "stay", why = "car", rule = 11 }
    end
    local lastD = f.lastD
    f.lastD = d
    if d > fixed("followMaxDist", 40) then return { act = "stay", why = "far", rule = 12 } end
    if math.floor(tonumber(o.z) or 0) ~= math.floor(tonumber(c.z) or 0) then
        resetProgress(f)
        return { act = "hold", why = "level", rule = 13 }
    end
    local px, py = o.x, o.y
    local mx, my = tonumber(o.mx) or 0, tonumber(o.my) or 0
    local ml = math.sqrt(mx * mx + my * my)
    local lead = tonumber(cfg.followLead) or 0
    if ml > 0.001 and lead > 0 then
        local k = 1
        if ml > lead then k = lead / ml end
        px, py = o.x + mx * k, o.y + my * k
    end
    local dp = B.DistXY(c.x, c.y, px, py)
    if dp <= cfg.followNear + gap or (f.held == true and dp <= cfg.followStart + gap) then
        resetProgress(f)
        return { act = "hold", why = "near", rule = 14 }
    end
    -- Fortschritt (vor Regel 15). Uhr rueckwaerts: Messung neu beginnen.
    if f.bestD == nil or f.bestAt == nil or ms - f.bestAt < 0 or d <= f.bestD - cfg.followStuckGain
        or gainToward(f, c, o) >= cfg.followStuckGain then
        f.bestD = d
        f.bestAt = ms
        f.bx, f.by = c.x, c.y
        f.stuck = nil
        f.retryAt = nil
    elseif not f.stuck and ms - f.bestAt >= cfg.followStuckMs then
        f.stuck = true
        f.retryAt = ms
    end
    local retry = false
    if f.stuck then
        local since = (f.retryAt ~= nil) and (ms - f.retryAt) or cfg.followRetryMs
        if since >= 0 and since < cfg.followRetryMs then
            return { act = "keep", why = "stuck", rule = 15 }
        end
        retry = true
    end
    -- 16: laufen zu einem Punkt followGap Kacheln vor dem (vorausberechneten) Besitzer auf der Linie Besitzer -> Junges
    local tx, ty = toward(px, py, c.x, c.y, cfg.followGap + gap)
    -- B1c Gehen (1.6): Reststrecke und Tempo des Besitzers (Weg seit dem letzten Takt / echte Zeit seitdem)
    local dt = tonumber(o.dt)
    if dt == nil or dt <= 0 then dt = tonumber(cfg.brainMs) or 1500 end
    local speed = ml / (dt / 1000)
    local walk = B.DistXY(c.x, c.y, tx, ty) <= (tonumber(cfg.walkDist) or 0) and speed <= walkSpeed
    -- Lauf baer-kampf (PLAN_KAMPF.md 2.4, 2.7; Kevin 13.11. ~23:00 Punkte 4 und 7): c.calm = eben aus dem Kampf -> ruhig zurueck (gehen bis
    -- fightCalmWalkMax Kacheln Reststrecke, weiter weg rennen); c.sprint = Leinen-Sprint zum Besitzer -> nie gehen. Fehlen beide: wie B1e.
    if c.calm == true and B.DistXY(c.x, c.y, tx, ty) <= (tonumber(cfg.fightCalmWalkMax) or 8) then walk = true end
    if c.sprint == true then walk = false end
    local grow = lastD ~= nil and d - lastD >= (tonumber(cfg.followFleeGrow) or 2)
    local age = nil
    if f.orderAt ~= nil and ms - f.orderAt >= 0 then age = ms - f.orderAt end
    if grow then
        -- B1c Rueckfall (1.2 Schritt 5): das Junge entfernte sich (Engine-Flucht bei Stress am Deckel) -> sofort neu
        if retry then f.retryAt = ms end
        return { act = "run", tx = tx, ty = ty, rule = 16, walk = walk }
    end
    if age ~= nil and age < cfg.followMoveMs then
        return { act = "keep", tx = tx, ty = ty, rule = 16, walk = walk }
    end
    local wandered = f.tx == nil or f.ty == nil or B.DistXY(f.tx, f.ty, tx, ty) >= cfg.followRepath
    local renew = age == nil or age >= cfg.followRenewMs
    local switched = f.orderAt ~= nil and (f.walk == true) ~= walk
    if wandered or renew or switched or f.held == true or retry then
        if retry then f.retryAt = ms end
        return { act = "run", tx = tx, ty = ty, rule = 16, walk = walk }
    end
    return { act = "keep", tx = tx, ty = ty, rule = 16, walk = walk }
end

-- ---------------------------------------------------------------------------
-- B1c: Zombie-Wache, Verstecken, Laerm-Ersatzweg (PLAN_B1C.md 1.2, 1.3, 6.3). Rein: keine Engine, auch der Client darf rufen.
-- ---------------------------------------------------------------------------

-- Versteck hinter dem Besitzer O, vom Zombie Z abgewandt: O + (O - Z) / |O - Z| x gap. Fallen O und Z zusammen: O + (gap, 0).
function B.HideSpot(ox, oy, zx, zy, gap)
    local dx, dy = ox - zx, oy - zy
    local len = math.sqrt(dx * dx + dy * dy)
    if len < 0.001 then return ox + gap, oy end
    return ox + dx / len * gap, oy + dy / len * gap
end

-- Laerm-Ersatzweg von C: ist der Anker A weiter als gap + 1, gap Kacheln Richtung A; sonst gap Kacheln quer zur Linie C -> A
-- (side 1 / -1; nie die eigene Kachel: Ankunft = Schild weg, PLAN_B1C.md 0.4). A fehlt (oder liegt auf C): quer zur x-Achse.
function B.CalmSpot(cx, cy, ax, ay, gap, side)
    local sd = 1
    if side == -1 then sd = -1 end
    if ax == nil or ay == nil then return cx, cy + gap * sd end
    local dx, dy = ax - cx, ay - cy
    local len = math.sqrt(dx * dx + dy * dy)
    if len < 0.001 then return cx, cy + gap * sd end
    local ux, uy = dx / len, dy / len
    if len > gap + 1 then return cx + ux * gap, cy + uy * gap end
    return cx - uy * gap * sd, cy + ux * gap * sd
end

-- Was soll ein Junges wegen eines Zombies tun? (Regeln 20-24, PLAN_B1C.md 1.3)
-- c = { x, y, z, st }; o = naechster Besitzer { x, y, z, dist, car } (nur bei st "tame") oder nil; z = naechster Zombie
-- { x, y, d } oder nil; g = Sitzungs-Tabelle der Wache, hier fortgeschrieben: on, mode, safeAt, zx, zy. ms = Echtzeit.
-- Rueckgabe { act, tx, ty, rule, mode }: act "none" (20, keine Gefahr / Ende), "hide" (21, rennen zum Versteck), "hold" (22, am
-- Versteck halten), "flee" (23, vom Zombie weg), "keep" (24, Nachlauf: war gefaehrdet, jetzt weiter als zedSafe, noch nicht
-- zedCalmMs lang). Gefahr beginnt bei z.d <= zedHide und haelt, solange z.d <= zedSafe (Hysterese).
-- B1e (PLAN_B1E.md 1.5, 6.3): c.gap (Zuschlag mit der Koerperlaenge, nur grosser Koerper) kommt auf hideGap; fehlt er: 0.
function B.GuardDecide(c, o, z, g, ms)
    local cfg = B.CFG
    g = g or {}
    local zd = z and tonumber(z.d) or nil
    local danger
    if g.on == true then
        danger = zd ~= nil and zd <= cfg.zedSafe
    else
        danger = zd ~= nil and zd <= cfg.zedHide
    end
    if not danger then
        if g.on ~= true then return { act = "none", rule = 20 } end
        if g.safeAt == nil or ms - g.safeAt < 0 then g.safeAt = ms end
        if ms - g.safeAt < cfg.zedCalmMs then return { act = "keep", rule = 24, mode = g.mode } end
        g.on = nil
        g.mode = nil
        g.safeAt = nil
        g.zx, g.zy = nil, nil
        return { act = "none", rule = 20 }
    end
    g.on = true
    g.safeAt = nil
    g.zx, g.zy = z.x, z.y
    local canHide = c.st == "tame" and o ~= nil and o.car ~= true
        and math.floor(tonumber(o.z) or 0) == math.floor(tonumber(c.z) or 0)
        and (tonumber(o.dist) or 999) <= cfg.hideOwnerMax
    if canHide then
        g.mode = "hide"
        local hx, hy = B.HideSpot(o.x, o.y, z.x, z.y, cfg.hideGap + (tonumber(c.gap) or 0))
        if B.DistXY(c.x, c.y, hx, hy) <= cfg.hideNear then
            return { act = "hold", tx = hx, ty = hy, rule = 22, mode = "hide" }
        end
        return { act = "hide", tx = hx, ty = hy, rule = 21, mode = "hide" }
    end
    g.mode = "flee"
    local dx, dy = c.x - z.x, c.y - z.y
    local len = math.sqrt(dx * dx + dy * dy)
    local tx, ty
    if len < 0.001 then
        tx, ty = c.x + cfg.zedFlee, c.y
    else
        tx, ty = c.x + dx / len * cfg.zedFlee, c.y + dy / len * cfg.zedFlee
    end
    return { act = "flee", tx = tx, ty = ty, rule = 23, mode = "flee" }
end
