if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Wachsen, Leben, Ausdauer und Faehigkeiten beim Schreiber (B1d, PLAN_B1D.md 0.1, 0.4, 0.5, 0.7-0.11, 1-4, 6.3).
--
-- Die Wahrheit steht im Register-Eintrag (nur gezaehmt/vermisst, nur Zahlen): g (Wachstum 0..1), gF / gFd / gFn (Fuetter-Bonus),
-- gAt (letztes Wachstums-Commit), hp / hpB (Leben als Anteil / zuletzt am Koerper gesetzt oder gesehen), xAgi ... xNos (Erfahrung).
-- Groesse, Stufe und Werte rechnet shared/BanditsNPCBearStats.lua daraus. Nur in der Sitzung (B._s[id], nie gespeichert): Ausdauer
-- sta, Weg kx / ky / kAt / kAcc, Ausser-Puste-Uhr breathAt, Sicht-Drossel staV / staVAt, Erfahrungs-Eimer xb, gDirty.
-- B1e (PLAN_B1E.md 0.1-0.7, 1.1-1.3, 6.2.5): KOERPER-TAUSCH. Register-Feld body ("cub"/"big" = Koerper, den der Eintrag zuletzt hatte;
-- Wahrheit ist immer die Art des gebundenen Tiers, B.BodyKind). Erreicht das gezaehmte Junge Halbstark (innere Groesse >= cubMaxSize),
-- tauscht B.GrowLive den Koerper ueber den vorhandenen Weg: B.PlaceCub (neuer Koerper der Art B.BIG, gen + 1, Spiegel, Groesse und
-- Leben sofort) und DANN B.RemoveCub(alt) -- genau wie "Call to me". Genau EIN Koerper, Register-Eintrag bleibt derselbe. Nur, wenn es
-- sicher ist (B.BodySwapReady), sonst beim naechsten Hirn-Takt. Zurueck zum Jungen erst unter swapBackSize (nie flackern).
-- Sitzung dazu: swapAt, swapTryAt, swapFailN (Tausch), busyUntil (Fuettern/Streicheln laeuft, B.BodyBusy).
-- F1 (PLAN_F1.md 5.3): B.GrowView auch fuer "missing" (+ Erfahrung, Traglast, Ausweichen, Kampf-Bonus, Fang-Chance, Warnweite);
-- B.BodyBusy meldet den Wechsel der Marke an die Sicht (B.Touch, s.busySent).
-- F2 = B5a (PLAN_F2.md 0.4, 2.3, 2.4, 4.3, 11.4, 11.6): Schutz B.BodyShield (setIsInvincible am gezaehmten Koerper), fremder Lebensverlust
-- zaehlt nie (B.BodyHp stellt den Koerper zurueck), Schaden nur ueber B.BodyHurt (aus B.BearHurt), Tod B.BodyDie, Ausdauer im Kampf
-- (B.StaUse, keine Erholung im Kampf), Lerntempo und Alters-Deckel in B.SkillAdd, Tausch nie im Kampf / am Boden, Verband in B.GrowSlow.
--
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 3, 5.3): Register-Feld look (Familie des Wunsches, nil = "std", nur tame/missing; B.GrowFix
-- klemmt es), B.BodySwap / B.BodySwapReady nehmen wahlfrei das Aussehen (nur der Aussehen-Knopf, server/BanditsNPCBearLook.lua) -- ohne
-- es wie bisher (B.GrowLive: das Wachsen behaelt die Familie ueber B.PlaceCub). Kondition rechnet mit dem Tempo des Aussehens.
-- F3 (PLAN_F3.md 3.1, 3.2, 6.4): Hunger / Durst / Muedigkeit wirken hier an je EINER Stelle ueber B.NeedK (shared/
-- BanditsNPCBearNeedRules.lua): Ausdauer-Erholung (stamina), Wachsen und Selbstheilung (B.GrowSlow; im Schlaf B.HealRate(true)).
-- Verbrauchte Ausdauer zaehlt als Anstrengung in die Sitzung (s.tirAcc -> Muedigkeit, server/BanditsNPCBearNeeds.lua). Das Wachsen
-- tauscht den Koerper nicht, waehrend er liegt (B.BodySwapReady "sleep").
--
-- Takte (alle aus vorhandenen Takten, keine neuen Ereignisse; je eine EIGENE Schleife nach den B1a-B1c-Schritten, Nachbesserung B1d B2):
--   Langsam-Takt (10 Spielminuten, server/BanditsNPCBearServer.lua slowTickBody) -> B.GrowSlow: g waechst, Leben abgleichen und heilen,
--     hoechstens je Spielstunde ein Commit (sofort bei Stufenwechsel oder Schaden).
--   Hirn-Takt (1,5 s, brainTickBody, am Ende) -> B.GrowLive: Groesse nachsetzen, Ausdauer und Kondition.
--   Neuer Koerper (B.PlaceCub: Aussteigen, Call to me, Tod im Auto) -> B.GrowBody: Groesse und Leben SOFORT aus dem Register.
-- Alle Uhren laufen nur, solange der Besitzer im Spiel ist, nicht bei "missing" (PLAN_B1D.md 0.9, Fragen F4 / F8). Wilde, scheue,
-- angefuetterte Junge: nichts (Kevin "ab dem Zaehmen").
--
-- Engine-Aufrufe hier (je Fundstelle am Aufruf): animal:isDead(), animal:getHealth(), animal:setHealth(Zahl), F2: animal:setIsInvincible(
-- Wahrheitswert), animal:setAttackedBy(getFakeAttacker()) -- getHealth nur in B.BodyHp; setHealth nur in B.BodyHp und B.BodyDie;
-- setIsInvincible nur in B.BodyHp, B.BodyShield, B.BodyDie (B.BodyHurt geht ueber B.BodyHp). Groesse nur ueber B.ApplySize
-- (shared/BanditsNPCBearStats.lua). Zeit ueber B.Now() / getTimestampMs().
-- Ladefolge: diese Datei laedt nach ...Follow und vor ...Guard / ...Heal / ...Registry / ...Ride / ...Server / ...World
-- (alphabetisch); fremde Funktionen (B.Ses, B.Commit, B.FindAnimal, B.PlayerByKey ...) nur zur Laufzeit. Ohne
-- shared/BanditsNPCBearStats.lua tut jeder Weg hier nichts (statsOk, Nachbesserung B1d B5).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

-- Rang der Stufen (Meldung nur aufwaerts).
local RANK = { cub = 0, half = 1, strong = 2, adult = 3 }
-- Text der Stufen fuer die Diagnose-Zeile (die Meldung an den Spieler baut die OBERFLAECHE aus dem Schluessel).
local STAGE_LOG = { half = "half-grown", strong = "strong", adult = "full-grown" }

-- Alle B1d-Felder des Eintrags (an anderen Zustaenden nil). B1e: + body. Aussehen (PLAN_AUSSEHEN.md 3): + look.
-- Lauf baer-talente: + tal / talR / talN (gelernte Talente, Spieltag des letzten Resets, gemeldete Punkte; server/BanditsNPCBearTalent.lua).
local FIELDS = { "g", "gF", "gFd", "gFn", "gAt", "hp", "hpB", "xAgi", "xVit", "xCon", "xFgt", "xFsh", "xNos", "body", "look",
    "tal", "talR", "talN" }

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------
local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

local function clamp(v, lo, hi)
    if v < lo then return lo end
    if v > hi then return hi end
    return v
end

local function cfg(key, def)
    local c = B.CFG
    local v = c and num(c[key]) or nil
    if v == nil then return def end
    return v
end

local function r3(v)
    return math.floor((tonumber(v) or 0) * 1000 + 0.5) / 1000
end

local function isTame(st)
    return st == "tame" or st == "missing"
end

local function rankOf(g)
    return RANK[B.StageOf(B.GrowSize(g))] or 0
end

-- Nachbesserung B1d B5: diese Datei rechnet mit den Formeln aus shared/BanditsNPCBearStats.lua (B.GrowDays, B.XpCum, B.SKILLS,
-- B.StatsOf, B.HealRate, B.ApplySize ...). Fehlt jene Datei (Teilkopie) oder brach sie beim Laden ab, tut jeder Weg hier NICHTS --
-- sonst wuerfe schon B.InitRegistry (B.GrowFix), das Register bliebe nil und der ganze Baer stuende. B.ApplySize ist ihre letzte
-- Funktion. Nur Tabellen-Lesen, kein Engine-Aufruf.
local function statsOk()
    return type(B.SKILLS) == "table" and type(B.SKILL_FIELD) == "table" and B.XpCum ~= nil and B.GrowDays ~= nil
        and B.StatsOf ~= nil and B.HealRate ~= nil and B.ApplySize ~= nil
end

-- Wachstum aus der Zeit seit dem Zaehmen (Migration, Spiegel ohne g). Ohne tamedAt: 0.
local function gFromTamed(tamedAt, now, D)
    local t = num(tamedAt)
    local n = num(now)
    if t == nil or n == nil then return 0 end
    return clamp((n - t) / (D * 24), 0, 1)
end

-- Eine Fehlerzeile beim Laden, nur bei Unsinn (Text, NaN, ausserhalb).
local function badLine(log, id, what)
    if log == true then B.Err("registry: entry " .. tostring(id) .. " had an unusable " .. what .. ", repaired") end
end

-- Stufen-Meldung an den Besitzer (wenn da) und eine Diagnose-Zeile.
local function tellStage(rec, stage, players)
    if STAGE_LOG[stage] == nil then return end
    local p = B.PlayerByKey(rec.owner, players)
    if p then B.Tell(p, { k = "UI_BN_Bear_Note_Grown", t = "stage", v = stage, tone = "good" }) end
    B.Log("grow: " .. tostring(rec.id) .. " is " .. STAGE_LOG[stage] .. " (day " .. tostring(B.GrowDay(rec)) .. ")")
end

-- Wachstum festschreiben (r + 1, Spiegel, Sicht) und die Stunden-Uhr stellen.
local function commitGrow(rec, s, now)
    rec.gAt = now
    if s then s.gDirty = nil end
    B.Commit(rec)
end

-- ---------------------------------------------------------------------------
-- Migration und Klemmen (PLAN_B1D.md 2.2). log = true nur aus B.InitRegistry (Fehlerzeilen bei Unsinn); im Langsam-Takt still.
-- ---------------------------------------------------------------------------
function B.GrowFix(rec, now, log)
    if type(rec) ~= "table" or not statsOk() then return end
    if not isTame(rec.st) then
        for i = 1, #FIELDS do rec[FIELDS[i]] = nil end
        return
    end
    local id = rec.id
    local D = B.GrowDays()
    -- g
    local g = num(rec.g)
    if g == nil then
        local fromT = gFromTamed(rec.tamedAt, now, D)
        if rec.g ~= nil then
            badLine(log, id, "growth value")
        elseif log == true then
            B.Log("grow: " .. tostring(id) .. " had no growth value, day " .. tostring(math.floor(fromT * D + 0.000001))
                .. " from its taming time")
        end
        rec.g = fromT
    else
        if g < 0 or g > 1 then badLine(log, id, "growth value") end
        rec.g = clamp(g, 0, 1)
    end
    -- Fuetter-Bonus
    local fmax = cfg("feedGrowMax", 0.10)
    local gF = num(rec.gF)
    if gF == nil then
        if rec.gF ~= nil then badLine(log, id, "feeding bonus") end
        gF = 0
    elseif gF < 0 or gF > fmax then
        badLine(log, id, "feeding bonus")
    end
    rec.gF = clamp(gF, 0, fmax)
    local gFn = num(rec.gFn)
    if gFn == nil then
        if rec.gFn ~= nil then badLine(log, id, "feeding count") end
        gFn = 0
    end
    rec.gFn = clamp(math.floor(gFn), 0, math.floor(cfg("feedGrowDay", 2)))
    if rec.gFd ~= nil and num(rec.gFd) == nil then
        badLine(log, id, "feeding day")
        rec.gFd = nil
    elseif rec.gFd ~= nil then
        rec.gFd = num(rec.gFd)
    end
    rec.gAt = num(rec.gAt)
    -- Erfahrung
    local top = B.XpCum(10)
    for i = 1, #B.SKILLS do
        local f = B.SKILL_FIELD[B.SKILLS[i]]
        local x = num(rec[f])
        if x == nil then
            if rec[f] ~= nil then badLine(log, id, "skill value (" .. f .. ")") end
            x = 0
        elseif x < 0 or x > top then
            badLine(log, id, "skill value (" .. f .. ")")
        end
        rec[f] = clamp(x, 0, top)
    end
    -- Leben (Anteil 0..1; <= 0 -> nil: der naechste Abgleich holt es aus dem Koerper)
    local hp = num(rec.hp)
    if hp == nil then
        if rec.hp ~= nil then badLine(log, id, "health value") end
        rec.hp = nil
    elseif hp <= 0 then
        rec.hp = nil
    else
        if hp > 1 then badLine(log, id, "health value") end
        rec.hp = clamp(hp, 0, 1)
    end
    local hpB = num(rec.hpB)
    if hpB == nil or hpB <= 0 then
        rec.hpB = nil
    else
        rec.hpB = clamp(hpB, 0, 1)
    end
    -- B1e (PLAN_B1E.md 4.1): Koerper nur "cub" / "big"; fehlt er (B1d-Stand), setzt ihn das Binden bzw. der naechste Hirn-Takt
    if rec.body ~= nil and rec.body ~= "cub" and rec.body ~= "big" then
        badLine(log, id, "body")
        rec.body = nil
    end
    -- Aussehen (PLAN_AUSSEHEN.md 3): nur eine bekannte Familie ausser "std" (B.LOOK_KEYS, shared/BanditsNPCBear.lua); "std" wird nie
    -- gespeichert (nil); Unbekanntes -> nil (Standard) mit Fehlerzeile beim Laden
    if rec.look ~= nil then
        local keys = B.LOOK_KEYS
        if rec.look == "std" then
            rec.look = nil
        elseif type(rec.look) ~= "string" or type(keys) ~= "table" or keys[rec.look] ~= true then
            badLine(log, id, "look")
            rec.look = nil
        end
    end
    -- Lauf baer-talente (shared/BanditsNPCBearTalentRules.lua): gelernte Talente bereinigen (nur bekannte, keine Doppelten, hoechstens talMax --
    -- die ersten bleiben; eine Fehlerzeile bei Unsinn). Existenz-Riegel.
    if B.TalentFix ~= nil then B.TalentFix(rec) end
end

-- ---------------------------------------------------------------------------
-- Leben am Koerper abgleichen (PLAN_B1D.md 0.5; F2 = B5a PLAN_F2.md 0.4, 11.6). Die Wahrheit ist rec.hp (Anteil 0..1); rec.hpB ist der
-- Wert, den wir zuletzt am Koerper gesetzt bzw. gesehen haben.
-- F2 11.6 (Kevin 12.11. ~05:20, nachdem sein halbstarker Baer an einem eigenen Speerhieb starb): das Leben eines gezaehmten Baeren senkt
-- NUR B.BearHurt (server/BanditsNPCBearHurt.lua: Zombies und feindliche Banditen). Ein Verlust des Koerpers, der nicht dort herkam
-- (Spieler-Waffe, Auto, Turret, NPC-Crew-Figur, fremde Mod), zaehlt NIE mehr als Schaden: der Koerper wird auf rec.hp zurueckgestellt
-- (bis B1d zaehlte jeder Verlust ueber hpLossEps). Dazu ist der Koerper fuer die Engine unverwundbar (B.BodyShield, 0.4). Ein Anstieg
-- (Engine-Heilung, NUR JAR dec/AnimalData.java:377-398) wird wie bisher zurueckgenommen. Danach unsere Heilung add; weicht der Koerper um
-- mehr als hpEps ab (oder kam ein fremder Verlust), wird er gesetzt. Nie ueber 1,0 (MP-Byte, NUR JAR dec_b1b/NetworkPlayerAI.java:280),
-- nie 0 (das ist der Tod, nur B.BodyDie), nicht am toten Tier. a == nil (Fahrt, entladen): nur rec.hp heilt. Fehlt hp, wird es aus dem
-- Koerper uebernommen (erster Abgleich). getHealth nur hier, setHealth nur hier und in B.BodyDie. Rueckgabe: Schaden als Anteil --
-- seit F2 immer 0 (Schaden rechnet B.BearHurt selbst).
-- ---------------------------------------------------------------------------

-- Senken verweigert die Engine an einem unverwundbaren Tier (NUR JAR dec/IsoAnimal.java:1157 "if (!this.isInvincible() || !(health <
-- this.health))") -- deshalb setzt B.BodyHp beim gezaehmten Baeren Schutz aus -> setHealth -> Schutz an, im selben Lua-Aufruf (PLAN_F2.md
-- 0.4). animal:setIsInvincible(Wahrheitswert): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:563 (SP-Zweig), server/ClientCommands.lua:
-- 911 (Server). Diagnose: hurtNow markiert den Abgleich aus B.BodyHurt (eigener Schaden, kein "Engine-Anstieg").
local hurtNow = false

function B.BodyHp(rec, a, add)
    if type(rec) ~= "table" then return 0 end
    add = num(add) or 0
    if add < 0 then add = 0 end
    if a == nil then
        local hp = num(rec.hp)
        if hp ~= nil and add > 0 then rec.hp = clamp(hp + add, 0.01, 1) end
        return 0
    end
    -- isDead am Tier: Vanilla server/Traps/STrapGlobalObject.lua:238
    if a:isDead() then return 0 end
    -- animal:getHealth(): Vanilla client/ISUI/Animal/ISAnimalUI.lua:15 (am Tier, Client); am Schreiber dieselbe geerbte Methode an
    -- IsoZombie: Bandits server/BanditServerSync.lua:11, server/BanditSave.lua:52 (Vererbung NUR JAR); im SP gespielt am Erwachsenen
    -- NCBearTest client/NCBearAttackProbe.lua:104 (ENTSCHEIDUNGEN.md:60). Am MP-Server am Tier ehrlich offen (PLAN_B1D.md 8 Nr. 4).
    local h = num(a:getHealth())
    if h == nil or h <= 0 then return 0 end
    local eps = cfg("hpEps", 0.005)
    local hp = num(rec.hp)
    local hp0 = hp
    local foreign, back = 0, 0
    if hp == nil then
        hp = clamp(h, 0.01, 1)
    elseif h < hp - cfg("hpLossEps", 0.0001) then
        foreign = hp - h                       -- F2 11.6: nicht ueber B.BearHurt -> kein Schaden, der Koerper wird zurueckgestellt
    elseif h > hp + eps then
        back = h - hp
    end
    hp = clamp(hp + add, 0.01, 1)
    rec.hp = hp
    local set = false
    if foreign > 0 or math.abs(h - hp) > eps then
        -- animal:setHealth(Zahl): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:545 (SP-Zweig), server/ClientCommands.lua:932
        -- (Server); Zwischenwerte ERLAUBT (Kevin: baer/STAND.md "Fragen fuer Kevin" B1d Nr. 9 "setHealth 0..1 ... als belegt zaehlen? ->
        -- ja", dazu baer/begleiter/ENTSCHEIDUNGEN.md "Kein Schaden am eigenen Baeren", 11.6), Werte 0..1 ohne Klemme NUR JAR
        -- dec/IsoAnimal.java:1156-1163.
        if hp < h and (rec.st == "tame" or rec.st == "missing") then
            a:setIsInvincible(false)
            a:setHealth(hp)
            a:setIsInvincible(true)
            local s = B._s and B._s[rec.id] or nil
            if s ~= nil and s.obj == a then s.shieldObj = a end
        else
            a:setHealth(hp)
        end
        rec.hpB = hp
        set = true
    else
        rec.hpB = h
    end
    if (foreign > 0 or back > 0 or set) and B.LogActive() then
        local what = " heal, engine +" .. tostring(r3(back)) .. " taken back, engine -" .. tostring(r3(foreign)) .. " ignored)"
        if hurtNow then what = " heal, hurt by a foe)" end
        B.Log("hp: " .. tostring(rec.id) .. " " .. tostring(r3(hp0)) .. " -> " .. tostring(r3(hp)) .. " (+" .. tostring(r3(add)) .. what)
    end
    return 0
end

-- F2 (PLAN_F2.md 0.4, 4.3; 11.6): Schutz -- der gezaehmte Koerper ist fuer die Engine unverwundbar (Spieler-Waffen, Autos, Vanillas "Kill",
-- Turret, NPC-Crew-Figuren). Wird nicht gespeichert (NUR JAR dec/IsoAnimal.java:147, :2181-2191) -> je Sitzung und Koerper EINMAL
-- (s.shieldObj); gerufen aus B.GrowBody (jeder neue Koerper: Tausch Tag 15, C1, Unstuck, Aussteigen -- im selben Aufruf, keine Luecke) und
-- B.GrowLive (jeder Hirn-Takt, ein Vergleich). animal:setIsInvincible(true): Vanilla client/ISUI/Animal/ISAnimalContextMenu.lua:563,
-- server/ClientCommands.lua:911. Nur gezaehmt/vermisst (wilde Junge bleiben verwundbar).
function B.BodyShield(rec, a)
    if type(rec) ~= "table" or a == nil or (rec.st ~= "tame" and rec.st ~= "missing") then return end
    local s = B.Ses(rec.id)
    if s.shieldObj == a then return end
    a:setIsInvincible(true)
    s.shieldObj = a
end

-- F2 (PLAN_F2.md 2.4, 4.3): der Schaden eines Gegner-Treffers am Koerper. Erst der ausstehende Abgleich (B.BodyHp), dann hp1 = rec.hp - frac
-- (Rueckgabe, darf <= 0 sein); rec.hp = max(hp1, 0,01) und der Koerper ueber B.BodyHp (Schutz kurz aus). Bei hp1 <= 0 entscheidet der
-- Aufrufer (B.BearDown setzt downFloor, B.BearDie toetet). Die EINE Stelle, an der Schaden das Register-Leben senkt.
function B.BodyHurt(rec, a, frac)
    if type(rec) ~= "table" then return nil end
    frac = num(frac) or 0
    if frac < 0 then frac = 0 end
    if a ~= nil then B.BodyHp(rec, a, 0) end
    local hp1 = (num(rec.hp) or 1) - frac
    rec.hp = clamp(hp1, 0.01, 1)
    if a ~= nil then
        hurtNow = true
        B.BodyHp(rec, a, 0)
        hurtNow = false
    end
    return hp1
end

-- F2 (PLAN_F2.md 0.11): Tod wie Vanilla (Register ZUERST, das macht B.BearDie): Schutz aus, Angreifer = der Ersatz-Angreifer der Engine
-- (nie ein Spieler -> kein PVP-Log), Leben 0. animal:setAttackedBy(getFakeAttacker()), animal:setHealth(0): Vanilla server/ClientCommands.lua:
-- 931-932 (Server), client/ISUI/Animal/ISAnimalContextMenu.lua:544-545 (SP); setIsInvincible: :563 / server/ClientCommands.lua:911.
-- Rueckgabe: true, wenn gesetzt.
function B.BodyDie(rec, a)
    if a == nil or a:isDead() then return false end
    a:setIsInvincible(false)
    a:setAttackedBy(getFakeAttacker())
    a:setHealth(0)
    return true
end

-- ---------------------------------------------------------------------------
-- Faehigkeiten: der EINE Weg, Erfahrung gutzuschreiben (PLAN_B1D.md 0.7, 1.4). Echtzeit-Eimer je Junges und Faehigkeit nur in der
-- Sitzung (startet voll mit xpPerMin x xpBucketMin, fuellt xpPerMin je Echtzeit-Minute, Uhr rueckwaerts = voll; Lehre NPC Crew
-- shared/BanditsNPCSkills.lua:475-565). Nur gezaehmt. Stufenaufstieg -> Commit und Meldung an den Besitzer.
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456. Rueckgabe: gutgeschrieben, hochgestuft (boolean).
-- F2 (PLAN_F2.md 11.4, Kevin 12.11. ~05:10): langsamer und durch das Alter gedeckelt -- Grundtempo xpPerMin 2 (vorher 6); Sandbox
-- BearSkillXpPercent (Prozent) multipliziert jede Gutschrift UND den Minuten-Deckel; Erfahrung ueber dem Alters-Deckel (B.SkillCapLv,
-- shared/BanditsNPCBearFightRules.lua: Junges 3, halbstark 6, kraeftig 8, ausgewachsen 10) wird NICHT gutgeschrieben -- was ein Spielstand
-- schon darueber hat, bleibt stehen (nichts wird weggenommen). Nur hier (die EINE Stelle aller Gutschriften).
-- ---------------------------------------------------------------------------
function B.SkillAdd(rec, key, xp, ms)
    if type(rec) ~= "table" or rec.st ~= "tame" or not statsOk() then return 0, false end
    local f = B.SKILL_FIELD[key]
    if f == nil then return 0, false end
    local pct = num(B.Opt("BearSkillXpPercent")) or 100
    if pct < 0 then pct = 0 end
    xp = (num(xp) or 0) * pct / 100
    if xp <= 0 then return 0, false end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    if type(s.xb) ~= "table" then s.xb = {} end
    local per = cfg("xpPerMin", 2) * pct / 100
    if per < 0 then per = 0 end
    local cap = per * cfg("xpBucketMin", 3)
    local b = s.xb[key]
    if type(b) ~= "table" or num(b.at) == nil or ms - b.at < 0 then
        b = { t = cap, at = ms }
        s.xb[key] = b
    else
        b.t = clamp((num(b.t) or 0) + (ms - b.at) / 60000 * per, 0, cap)
        b.at = ms
    end
    local give = xp
    if give > b.t then give = b.t end
    local old = B.SkillXp(rec, key)
    local capL = 10
    if B.SkillCapLv then capL = B.SkillCapLv(rec) end
    local top = B.XpCum(capL)
    if old + give > top then give = top - old end
    if give <= 0 then return 0, false end
    b.t = b.t - give
    local L0 = B.SkillLevel(rec, key)
    rec[f] = old + give
    local L1 = B.SkillLevel(rec, key)
    if L1 <= L0 then return give, false end
    B.Commit(rec)
    local p = B.PlayerByKey(rec.owner)
    if p then B.Tell(p, { k = "UI_BN_Bear_Note_SkillUp", t = "skill", v = key, w = L1, tone = "good" }) end
    B.Log("skill: " .. tostring(rec.id) .. " " .. tostring(key) .. " is now level " .. tostring(L1))
    return give, true
end

-- Erfahrung absolut setzen (Probebefehl der Test-Mod; spaeter Baeren-Fenster): geklemmt, ohne Eimer, Commit. Rueckgabe: neue Stufe (nil bei falschem
-- Schluessel oder nicht gezaehmt).
function B.SkillSet(rec, key, xp)
    if type(rec) ~= "table" or not isTame(rec.st) or not statsOk() then return nil end
    local f = B.SKILL_FIELD[key]
    if f == nil then return nil end
    rec[f] = clamp(num(xp) or 0, 0, B.XpCum(10))
    B.Commit(rec)
    return B.SkillLevel(rec, key)
end

-- Haken ohne Aufrufer in B1d (Kampf B5a, Fischen, Spuernase): nur Erfahrung, kein Verhalten (PLAN_B1D.md 1.4.4).
-- _dmg: Schaden des Treffers (fuer B5a; die Erfahrung haengt in B1d nicht davon ab).
function B.OnHitTaken(rec, _dmg, ms)
    local xp = cfg("xpHitTaken", 10)
    B.SkillAdd(rec, "agi", xp, ms)
    B.SkillAdd(rec, "vit", xp, ms)
end

function B.OnHitDealt(rec, ms)
    B.SkillAdd(rec, "fgt", cfg("xpHitDealt", 5), ms)
end

-- Fischen erst ab Halbstark (Kevin, ENTSCHEIDUNGEN.md:213).
function B.OnFish(rec, caught, ms)
    if type(rec) ~= "table" or not statsOk() or rankOf(rec.g) < 1 then return end
    local xp = cfg("xpFishTry", 2)
    if caught == true then xp = xp + cfg("xpFishCatch", 10) end
    B.SkillAdd(rec, "fsh", xp, ms)
end

function B.OnSniff(rec, ms)
    B.SkillAdd(rec, "nos", cfg("xpSniff", 5), ms)
end

-- ---------------------------------------------------------------------------
-- Ausdauer und Kondition je Hirn-Takt (PLAN_B1D.md 0.8). Nur in der Sitzung, ohne Wirkung. Sinkt NUR bei unserem Rennbefehl (s.walk
-- == false und ms < s.ownUntil, beides setzt B.MoveTo, server/BanditsNPCBearWorld.lua); Gehen, Laerm-Ersatzweg (gehend) und eine
-- Engine-Flucht zaehlen nicht. Weg aus den Lagen, die der Hirn-Takt ohnehin liest. Sprung (Neu-Erzeugen ausserhalb B.GrowBody) -> 0,
-- aber erst ab mehr als conStepMax Kacheln UND mehr als conStepMul x runSpeed x Taktdauer (Nachbesserung B1d B4: bei Ruckeln oder
-- Vorspulen bis etwa x4 ist ein langer Weg kein Sprung). Erholung in Echtzeit (auch in der Pause; nur Anzeige, ohne Wirkung).
-- Sicht nur an den Besitzer, gedrosselt (staViewStep Punkte UND viewMoveMs; Rand leer/voll ab einem halben Punkt).
-- ---------------------------------------------------------------------------
-- F2 (PLAN_F2.md 2.3, 4.3): Sicht der Ausdauer an den Besitzer, gedrosselt -- im Kampf (s.fight) je staViewMsFight 1 s und ab 1 Punkt,
-- sonst je viewMoveMs ab staViewStep Punkten; Rand leer/voll ab einem halben Punkt. Aus stamina und B.StaUse.
local function staView(rec, s, sta, staMax, ms)
    local pts = sta * staMax
    local v, vAt = num(s.staV), num(s.staVAt)
    if v == nil or vAt == nil or ms - vAt < 0 then
        s.staV, s.staVAt = pts, ms
        return
    end
    local every, step = cfg("viewMoveMs", 5000), cfg("staViewStep", 10)
    if type(s.fight) == "table" then every, step = cfg("staViewMsFight", 1000), 1 end
    if ms - vAt < every then return end
    local d = math.abs(pts - v)
    local edge = (sta <= 0 or sta >= 1) and d >= 0.5
    if d >= step or edge then
        s.staV, s.staVAt = pts, ms
        if rec.owner ~= nil then B.Touch(nil, rec.owner) end
    end
end

-- Ausser Puste (Kondition +conBreathXp, hoechstens je conBreathMs) -- Rennen (stamina) und seit F2 auch der Kampf (B.StaUse).
local function outOfBreath(rec, s, ms)
    local b = num(s.breathAt)
    if b == nil or ms - b < 0 or ms - b >= cfg("conBreathMs", 60000) then
        s.breathAt = ms
        B.SkillAdd(rec, "con", cfg("conBreathXp", 5), ms)
    end
end

-- F3 (PLAN_F3.md 3.2): Anstrengung -> Muedigkeit. Verbrauchte Ausdauer-Punkte (Rennen, Angriffe) sammeln sich in der Sitzung
-- (s.tirAcc); B.NeedsSlow (server/BanditsNPCBearNeeds.lua) macht daraus tirPerBar Punkte Muedigkeit je verbrauchte Leiste und leert den
-- Zaehler. Deckel tirAccBars Leisten: ein Baer, dessen Beduerfnisse gerade nicht zaehlen, sammelt nicht endlos.
local function tire(s, pts, staMax)
    local p = num(pts) or 0
    if p <= 0 then return end
    local acc = (num(s.tirAcc) or 0) + p
    local cap = (num(staMax) or 1) * cfg("tirAccBars", 10)
    if acc > cap then acc = cap end
    s.tirAcc = acc
end

-- F2 (PLAN_F2.md 2.2.3, 2.3): ein Angriff kostet Ausdauer (pts Punkte, staAttackCost 3) -- aus dem Kampf-Takt (server/BanditsNPCBearFight.lua).
-- Leer -> ausser Puste. Rueckgabe: Ausdauer danach (Anteil 0..1).
function B.StaUse(rec, pts, ms)
    if type(rec) ~= "table" or rec.st ~= "tame" or not statsOk() then return 1 end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    local staMax = B.StatsOf(rec).staMax
    if staMax <= 0 then staMax = 1 end
    tire(s, pts, staMax)                               -- F3: ein Angriff macht auch ein wenig muede
    local sta = (num(s.sta) or 1) - (num(pts) or 0) / staMax
    if sta <= 0 then
        sta = 0
        outOfBreath(rec, s, ms)
    end
    if sta > 1 then sta = 1 end
    s.sta = sta
    staView(rec, s, sta, staMax, ms)
    return sta
end

local function stamina(rec, s, cx, cy, ms)
    cx, cy = num(cx), num(cy)
    if cx == nil or cy == nil then return end
    local lastAt = num(s.kAt)
    local px, py = num(s.kx), num(s.ky)
    s.kx, s.ky, s.kAt = cx, cy, ms
    if lastAt == nil or px == nil or py == nil or ms - lastAt <= 0 then return end
    local dts = (ms - lastAt) / 1000
    if dts > 10 then dts = 10 end
    local way = B.DistXY(px, py, cx, cy)
    -- B1e: Sprungdeckel mit dem Tempo des Koerpers (grosser Koerper: runSpeedBig); Aussehen: Tempo des Aussehens (B.LookNow,
    -- server/BanditsNPCBearLook.lua)
    local look = nil
    if B.LookNow then look = B.LookNow(rec) end
    local run0 = B.BodyNum(rec.body, "runSpeed", 2.47, look)
    if way > cfg("conStepMax", 8) and way > cfg("conStepMul", 4) * run0 * dts then way = 0 end
    local st = B.StatsOf(rec)
    local staMax = st.staMax
    if staMax <= 0 then staMax = 1 end
    local sta = num(s.sta) or 1
    local until_ = num(s.ownUntil)
    local run = s.walk == false and until_ ~= nil and ms < until_
    if run then
        if way > 0 then
            sta = sta - way * cfg("staRunCost", 0.4) / staMax
            tire(s, way * cfg("staRunCost", 0.4), staMax)      -- F3: Rennen macht auch ein wenig muede (gemuetliches Gehen nicht)
            local per = cfg("conTilesPerXp", 5)
            if per <= 0 then per = 5 end
            local acc = (num(s.kAcc) or 0) + way
            local n = math.floor(acc / per)
            s.kAcc = acc - n * per
            if n > 0 then B.SkillAdd(rec, "con", n, ms) end
        end
    elseif type(s.fight) ~= "table" then
        -- F2 (PLAN_F2.md 2.3): im Kampf keine Erholung (sonst glichen 2 Punkte/s die Angriffe aus und er waere nie ausser Puste)
        -- F3 (PLAN_F3.md 3.1; Kevin ENT:21 "erst langsamer"): hungrig / durstig (ab 50) oder sehr muede (ab tirHeavy) erholt er sich halb
        -- so schnell (B.NeedK, shared/BanditsNPCBearNeedRules.lua); ohne jene Datei wie vor F3
        local needK = 1
        if B.NeedK then needK = num(B.NeedK(rec).sta) or 1 end
        -- Lauf baer-talente (Talent Ausdauernd): Erholung x talStaRegK (1,5); das Maximum staMax ist schon x 1,3 (B.StatsOf). Existenz-Riegel.
        local regK = 1
        if B.TalentK ~= nil then regK = B.TalentK(rec, "stamina", "talStaRegK", 1) end
        sta = sta + cfg("staRegen", 2) * dts * (1 + cfg("conPerLv", 0.05) * st.lv.con) * needK * regK / staMax
    end
    if sta <= 0 then
        sta = 0
        -- ausser Puste (Kevin: "vor allem Ausser-Puste-Kommen", ENTSCHEIDUNGEN.md:226), hoechstens je conBreathMs
        if run then outOfBreath(rec, s, ms) end
    end
    if sta > 1 then sta = 1 end
    s.sta = sta
    staView(rec, s, sta, staMax, ms)
end

-- ---------------------------------------------------------------------------
-- B1e: Koerper-Tausch (PLAN_B1E.md 0.4, 0.6, 0.7, 1.1 Schritt 3-4, 6.2.5)
-- ---------------------------------------------------------------------------

-- Laeuft eine Frist noch? until_ = Zeitpunkt (Echtzeit-ms), span = ihre Hoechstdauer. Uhr rueckwaerts (Rest > span) = abgelaufen.
local function pending(until_, ms, span)
    local u = num(until_)
    if u == nil then return false end
    local left = u - ms
    return left > 0 and left <= span
end

-- Seit at weniger als span vergangen? Uhr rueckwaerts (ms < at) = abgelaufen.
local function within(at, ms, span)
    local t = num(at)
    if t == nil then return false end
    return ms - t >= 0 and ms - t < span
end

-- Ist ein Tausch JETZT sicher? (0.6) Sonst beim naechsten Hirn-Takt; der alte Koerper bleibt solange voll benutzbar.
-- Das lebende Objekt der Sitzung prueft der Aufrufer (brainTickBody Schritt 7, server/BanditsNPCBearServer.lua).
-- Rueckgabe ok, why: "state" (nicht gezaehmt), "ride" (faehrt mit), "cool" (swapMinMs seit dem letzten Tausch), "retry"
-- (swapRetryMs seit dem letzten Fehlversuch), F2: "fight" (Kampf laeuft), "down" (am Boden), "calm" (Laerm-Antwort laeuft), "guard"
-- (Zombie-Wache an oder Zombie / feindlicher Bandit naeher als
-- zedSafe), "busy" (Fuettern/Streicheln laeuft), "move" (eigener Rennbefehl laeuft, hoechstens swapMoveMaxMs), "nodef" (Definition
-- des Ziel-Koerpers fehlt). Liest nur (auch die Bench fragt hier).
-- Aussehen (PLAN_AUSSEHEN.md 5.2 Nr. 16, 5.3): body / look wahlfrei (der Aussehen-Knopf: Ziel = der JETZIGE Koerper in einem anderen
-- Aussehen) -- dann prueft "nodef" genau diese Art. Ohne beide wie bisher (Ziel B.BodyWant, Standard-Art; die Bench ruft mit drei).
function B.BodySwapReady(rec, s, ms, body, look)
    if type(rec) ~= "table" or rec.st ~= "tame" then return false, "state" end
    if rec.ride ~= nil then return false, "ride" end
    if type(s) ~= "table" then s = B.Ses(rec.id) end
    ms = num(ms) or getTimestampMs()
    -- F2 (PLAN_F2.md 2.2.8, 4.3): nie waehrend eines Kampfs (s.fight) und nie am Boden (rec.down)
    if type(s.fight) == "table" then return false, "fight" end
    if rec.down ~= nil then return false, "down" end
    -- F3 (PLAN_F3.md 6.8): das WACHSEN (weder body noch look gegeben) tauscht den Koerper nicht, waehrend er liegt -- er stuende mitten im
    -- Schlaf auf; nach dem Aufwachen kommt der Tausch von selbst. Der Aussehen-Knopf ist ein Befehl und weckt ihn (B.PlaceCub).
    if body == nil and look == nil and B.IsLying ~= nil and B.IsLying(rec) then return false, "sleep" end
    if within(s.swapAt, ms, cfg("swapMinMs", 60000)) then return false, "cool" end
    if within(s.swapTryAt, ms, cfg("swapRetryMs", 10000)) then return false, "retry" end
    if pending(s.calmUntil, ms, cfg("calmMs", 2500)) then return false, "calm" end
    local g = s.g
    if type(g) == "table" and g.on == true then return false, "guard" end
    local z = B._zed and B._zed[rec.id] or nil
    if type(z) == "table" and num(z.d) ~= nil and num(z.d) < cfg("zedSafe", 9) then return false, "guard" end
    if pending(s.busyUntil, ms, cfg("busyMs", 20000)) then return false, "busy" end
    -- Nachbesserung B1e B2: unser eigener Rennbefehl laeuft noch (B.MoveTo, server/BanditsNPCBearWorld.lua: s.walk == false und
    -- ms < s.ownUntil, das hoechstens ownMaxMs voraus liegt) -> warten, sonst stuende der neue Koerper bis zum naechsten Hirn-Takt
    -- still. Aber hoechstens swapMoveMaxMs seit dem ersten Takt mit want ~= have (s.swapWantAt, setzt B.GrowLive): ein staendig
    -- rennender Baer wartet nie endlos. Ohne s.swapWantAt (Bench-Abfrage vor dem ersten Takt) keine Sperre.
    if s.walk == false and pending(s.ownUntil, ms, cfg("ownMaxMs", 15000))
        and within(s.swapWantAt, ms, cfg("swapMoveMaxMs", 10000)) then
        return false, "move"
    end
    local want = body or B.BodyWant(rec)
    if B.CubDefOk == nil or not B.CubDefOk(want, look) then return false, "nodef" end
    return true, nil
end

-- Beschaeftigt-Marke (0.7) aus den Zeitaktionen Fuettern / Streicheln (shared/TimedActions, SP start() / MP serverStart(); loeschen in
-- complete() / stop() / serverStop()). Sucht den Eintrag mit s.obj == animal (hoechstens 64 Sitzungen). on -> busyUntil = jetzt +
-- busyMs (Deckel: eine nie beendete Aktion sperrt hoechstens so lange), sonst nil. Rueckgabe: true, wenn gefunden.
-- getTimestampMs: Vanilla server/Foraging/forageServer.lua:456.
-- F1 (PLAN_F1.md 5.3): wechselt die Marke (an/aus), geht die Sicht neu hinaus (busy; der Sitz-Treiber der Clients wartet so lange) --
-- B.Touch des Eintrags, s.busySent merkt den gemeldeten Stand (laeuft die Marke von selbst ab, meldet es der Hirn-Takt).
function B.BodyBusy(animal, on)
    if animal == nil or type(B._s) ~= "table" then return false end
    local n = 0
    for id, s in pairs(B._s) do
        n = n + 1
        if n > 64 then break end
        if type(s) == "table" and s.obj == animal then
            local busy = on == true
            if busy then
                s.busyUntil = getTimestampMs() + cfg("busyMs", 20000)
            else
                s.busyUntil = nil
            end
            if (s.busySent == true) ~= busy then
                s.busySent = busy or nil
                local reg = B.Reg and B.Reg()
                local rec = reg and reg.cubs[id] or nil
                if rec ~= nil and B.Touch then B.Touch(rec) end
            end
            return true
        end
    end
    return false
end

local function swapFail(rec, s, ms, why)
    s.swapTryAt = ms
    s.swapFailN = (num(s.swapFailN) or 0) + 1
    if s.swapFailN >= cfg("swapFailLog", 6) then
        B.ErrEvery("swap:" .. tostring(rec.id), 60000, "body: " .. tostring(rec.id) .. " could not change its body (" .. tostring(why)
            .. ", " .. tostring(s.swapFailN) .. " tries), it keeps the old one")
    end
    return nil, why
end

-- Der Tausch (1.1 Schritt 4), alles in EINEM Lua-Aufruf (dazwischen speichert die Welt nicht):
--   a Kachel (B.SwapSpot: eigene Kachel, sonst Ring 1..swapRing) -- keine: Fehlversuch "nospot"
--   b noch nicht verbuchter Schaden am alten Koerper ins Register (B.BodyHp, sonst verloren)
--   c neuer Koerper ueber B.PlaceCub(..., want) (der vorhandene Weg: B.CreateCub, gen + 1, aid, rec.body, Sitzung leer, Commit, Spiegel
--     sofort, Groesse und Leben sofort ueber B.GrowBody) -- misslingt er: Fehlversuch, der alte Koerper bleibt unberuehrt
--   d DANN der alte Koerper weg (B.RemoveCub: Sperre los, remove(), am Server removeAnimal(OnlineID)); Abklingzeit; NUR IM
--     EINZELSPIELER (B.IsSP) schaut der neue Koerper zum Besitzer (animal:faceThisObject(Spieler): Vanilla
--     shared/TimedActions/Animals/ISPetAnimal.lua:17, Tier -> Spielfigur), wenn der Besitzer da und naeher als swapFaceDist ist.
--     Nachbesserung B1e A2: jenes Vorbild steht in update() einer Zeitaktion; am MP-Server ruft weder Vanilla noch Bandits
--     faceThisObject -- im Mehrspieler behaelt der neue Koerper die Richtung, die addAnimal ihm gibt (offen, nur Optik).
--   Eine Diagnose-Zeile. square:getX()/getY()/getZ() an der Kachel: Vanilla client/DebugUIs/DebugContextMenu.lua:636
--   (Nachbesserung B1e A6; derselbe Beleg wie server/BanditsNPCBearWorld.lua und server/BanditsNPCBearRide.lua).
-- Keine eigene Meldung (die Stufen-Meldung "half-grown" kommt mit derselben Schwelle). Rueckgabe: neues Tier oder nil, why.
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 5.3): look gegeben (nur der Aussehen-Knopf, B.HandleLook) -> derselbe Weg mit genau
-- diesem Aussehen (B.PlaceCub(..., want, look) setzt rec.look), Grund "look". Leben (b), Ausdauer (Sitzung), am Boden, Verband, Erfahrung
-- bleiben -- kein Heilen (Kevin 12.11.: "wird er dabei geheilt etc?" -> nein). Ohne look wie bisher (Wachsen: Familie aus rec.look).
function B.BodySwap(rec, a, want, ms, look)
    if type(rec) ~= "table" or a == nil then return nil, "noargs" end
    if want ~= "big" then want = "cub" end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    local from, fromLook = B.BodyKind(a)
    if from == nil then from = "cub" end
    local sq = B.SwapSpot(a, rec.gen)
    if sq == nil then return swapFail(rec, s, ms, "nospot") end
    B.BodyHp(rec, a, 0)
    local why = "shrink"
    if want == "big" then why = "grow" end
    if look ~= nil then why = "look" end
    -- Nachbesserung Aussehen B1 (PRUEF_B.md): beim Aussehen-Knopf (look gegeben) startet die gemeinsame Uhr mit Unstuck HIER, direkt vor
    -- dem neuen Koerper (B.CallStamp, server/BanditsNPCBearRide.lua -- B._callAt bleibt dort). Bricht danach ein Engine-Aufruf ab (neuer
    -- Koerper da, alter noch nicht weg), laeuft die Uhr schon: jede weitere Bitte wird abgelehnt, hoechstens EIN Extra-Koerper je
    -- Abklingzeit (die Selbstheilung raeumt ihn weg) statt einer mehr je Klick. Ohne neuen Koerper (n == nil) Stempel zurueck: ein
    -- Fehlversuch kostet weiter keine Abklingzeit. Ein Fehler davor (Kachel, B.BodyHp) startet keine Uhr. Wachsen (look nil) unveraendert.
    local was = nil
    if look ~= nil and B.CallStamp then was = B.CallStamp(rec, ms) end
    local n, pwhy = B.PlaceCub(rec, sq:getX(), sq:getY(), sq:getZ(), why, want, look)
    if n == nil then
        if look ~= nil and B.CallUnstamp then B.CallUnstamp(rec, was) end
        return swapFail(rec, s, ms, pwhy)
    end
    if n ~= a then B.RemoveCub(a) end
    s = B.Ses(rec.id)
    s.swapAt = ms
    s.swapTryAt = nil
    s.swapFailN = 0
    s.swapWantAt = nil                  -- Nachbesserung B1e B2: die Wartezeit "move" beginnt beim naechsten Wunsch neu
    local fd = cfg("swapFaceDist", 30)
    if fd > 0 and rec.owner ~= nil and B.IsSP() then
        local p, e = B.PlayerByKey(rec.owner)
        if p and e and B.DistXY(e.x, e.y, sq:getX() + 0.5, sq:getY() + 0.5) < fd then n:faceThisObject(p) end
    end
    if B.LogActive() then
        local toLook = B.LookKind and B.LookKind(n) or nil
        B.Log("body: " .. tostring(rec.id) .. " " .. from .. " -> " .. want .. " (" .. why .. ") at " .. tostring(sq:getX()) .. ","
            .. tostring(sq:getY()) .. " gen " .. tostring(rec.gen) .. ", inner " .. tostring(r3(B.GrowSize(rec.g))) .. " shown "
            .. tostring(B.BodySize(rec, want)) .. ", look " .. tostring(fromLook) .. " -> " .. tostring(toLook))
    end
    return n, nil
end

-- ---------------------------------------------------------------------------
-- Je Hirn-Takt fuer jedes geladene, lebende, gezaehmte Junge (PLAN_B1D.md 1.1 Schritt 3; seit der Nachbesserung B1d B2 in einer
-- eigenen Schleife am ENDE von brainTickBody, server/BanditsNPCBearServer.lua -- ein Fehler hier reisst B1a-B1c nicht mehr mit):
-- Groesse nachsetzen (faengt Laden, Tierzone, Debug-Alter der Engine und Weg A ab; 2 Java-Aufrufe, geschrieben nur bei Abweichung),
-- fehlendes Leben aus dem Koerper, Ausdauer/Kondition. Kein Commit (ausser beim Stufenaufstieg einer Faehigkeit).
-- B1e (PLAN_B1E.md 1.1 Schritt 1-3): have = Koerper des Tiers (B.BodyKind; weicht rec.body ab -> rec.body = have, ohne Commit), want =
-- B.BodyWant. Gleich -> Groesse des VORHANDENEN Koerpers. Verschieden und sicher (B.BodySwapReady) -> B.BodySwap (der neue Koerper hat
-- Groesse und Leben schon). Sonst bleibt der alte Koerper (das Junge bei 0,75) bis zum naechsten Takt; fehlt die Definition des
-- Ziel-Koerpers, eine Fehlerzeile je 10 Minuten.
-- ---------------------------------------------------------------------------
function B.GrowLive(rec, a, cx, cy, ms)
    if type(rec) ~= "table" or rec.st ~= "tame" or a == nil or not statsOk() then return end
    ms = num(ms) or getTimestampMs()
    local s = B.Ses(rec.id)
    local have = B.BodyKind(a) or "cub"
    if rec.body ~= have then rec.body = have end
    local want = B.BodyWant(rec)
    if want ~= have then
        -- Nachbesserung B1e B2: erster Takt mit want ~= have (Beginn der hoechstens swapMoveMaxMs langen Wartezeit "move")
        if num(s.swapWantAt) == nil then s.swapWantAt = ms end
        local ready, why = B.BodySwapReady(rec, s, ms)
        if ready then
            local n = B.BodySwap(rec, a, want, ms)
            if n ~= nil then return end
        elseif why == "nodef" then
            B.ErrEvery("swapdef", 600000, "body: animal definition " .. tostring(B.BODY_TYPE[want]) .. " is not loaded, "
                .. tostring(rec.id) .. " keeps its " .. have .. " body")
        end
    else
        s.swapWantAt = nil
    end
    B.ApplySize(a, B.BodySize(rec, have))
    B.BodyShield(rec, a)                         -- F2 (PLAN_F2.md 0.4, 11.6): Schutz am gebundenen Koerper (einmal je Objekt)
    -- Nachbesserung F2 B6 (Befund Z3): der Abgleich Koerper <-> Register laeuft JEDEN Hirn-Takt (ein getHealth je Baer), nicht erst im
    -- Langsam-Takt -- ein fremder Verlust am Schutz vorbei (11.6) steht so hoechstens einen Hirn-Takt am Koerper und kann sich nicht ueber
    -- 10 Spielminuten bis zum Tod aufsummieren. Neu bekanntes Leben -> in die Sicht (sie geht mit dem naechsten Takt hinaus).
    local hpKnown = rec.hp ~= nil
    B.BodyHp(rec, a, 0)
    if not hpKnown and rec.hp ~= nil then B.Touch(rec) end
    stamina(rec, s, cx, cy, ms)
end

-- ---------------------------------------------------------------------------
-- Je Langsam-Takt (PLAN_B1D.md 1.1 Schritt 2; seit der Nachbesserung B1d B2 in einer eigenen Schleife nach den B1a-B1c-Schritten von
-- slowTickBody): nur gezaehmt, Besitzer im Spiel. g waechst um dt / (D x 24); Leben abgleichen und mit BearHealAwake heilen (Koerper
-- nur, wenn geladen; Fahrt/entladen: nur das Register); Commit hoechstens je growCommitH, sofort bei Stufenwechsel (mit Meldung) oder
-- einem Verlust ab hpCommit. Kein Schlaf in B1d -> immer B.HealRate(false). F2: am Boden ohne Selbstheilung, + Verband (B.MendRateOf).
-- F3 (PLAN_F3.md 3.1, 6.4): Wachsen x B.NeedK.grow (Hunger/Durst ab 50 halb, ab 80 gar nicht), Selbstheilung im Schlaf mit
-- B.HealRate(true) (15 %/h x Heil-Tempo) und x B.NeedK.heal (ab 80 keine); der Verband wirkt immer.
-- ---------------------------------------------------------------------------
function B.GrowSlow(rec, dt, online, now, players)
    if type(rec) ~= "table" or rec.st ~= "tame" or rec.owner == nil or not statsOk() then return end
    if type(online) ~= "table" or online[rec.owner] ~= true then return end
    now = num(now) or B.Now()
    -- frisch gezaehmt (g fehlt noch): B.GrowFix rechnet g aus tamedAt bis jetzt -- dieser Schritt darf dt nicht noch einmal geben
    local fresh = rec.g == nil
    B.GrowFix(rec, now, false)
    local s = B.Ses(rec.id)
    dt = num(dt) or 0
    if dt < 0 then dt = 0 end
    local g0 = rec.g
    local rank0 = rankOf(g0)
    if fresh then s.gDirty = true end
    -- F3 (PLAN_F3.md 3.1; Kevin ENT:12 "Hunger bremst", ENT:21 "waechst nicht, heilt nicht"): Faktoren aus Hunger / Durst (B.NeedK,
    -- shared/BanditsNPCBearNeedRules.lua); ohne jene Datei alle 1 (wie vor F3)
    local needK = nil
    if B.NeedK then needK = B.NeedK(rec) end
    local growK = needK and num(needK.grow) or 1
    if dt > 0 and g0 < 1 and not fresh and growK > 0 then
        rec.g = clamp(g0 + dt * growK / (B.GrowDays() * 24), 0, 1)
        s.gDirty = true
    end
    local hp0 = rec.hp
    -- F2 (PLAN_F2.md 2.4, 2.5): am Boden keine Selbstheilung, nur ein Verband; ein Verband heilt zusaetzlich (B.MendRateOf,
    -- server/BanditsNPCBearMend.lua, %/h). Abgelaufen -> Felder weg (festgeschrieben mit dem naechsten Wachstums-Commit).
    local rate = 0
    if rec.down == nil then
        -- F3 (PLAN_F3.md 6.4; Kevin ENT:272 "im Schlaf ~15 %"): schlaeft er (B.IsAsleep, server/BanditsNPCBearSleep.lua), heilt er mit dem
        -- Schlaf-Wert; ausgehungert / ausgetrocknet (ab 80) heilt er nicht von selbst
        -- Nachbesserung C4: der Schlaf-Wert gilt nur mit Koerper in der Welt -- die Sitzung (s.slp) ueberlebt das Entladen, waehrend
        -- Hunger, Durst und Muedigkeit ohne Koerper eingefroren sind (server/BanditsNPCBearNeeds.lua counts); sonst heilte ein
        -- "schlafender", entladener Baer 15-mal so schnell wie wach und wachte nie auf
        local asleep = B.IsAsleep ~= nil and B.IsAsleep(rec) and B.FindAnimal(rec) ~= nil
        rate = B.HealRate(asleep) * (needK and num(needK.heal) or 1)
        -- Lauf baer-talente (Talent Zaeh, Kevin 02:50 "heilt doppelt so schnell"): Selbstheilung x talHealK (wach 2 %/h, Schlaf 30 %/h bei 100 %
        -- Heil-Tempo); der Verband unten bleibt gleich. Existenz-Riegel.
        if B.TalentK ~= nil then rate = rate * B.TalentK(rec, "tough", "talHealK", 1) end
    end
    if B.MendRateOf then
        local mend = B.MendRateOf(rec, now)
        rate = rate + mend
        if rec.bndH ~= nil and mend <= 0 then
            rec.bndH, rec.bndR = nil, nil
            s.gDirty = true
            B.Touch(rec)
        end
    end
    local loss = B.BodyHp(rec, B.FindAnimal(rec), rate / 100 * dt)
    if rec.hp ~= hp0 then s.gDirty = true end
    local stage1 = B.StageOf(B.GrowSize(rec.g))
    local up = (RANK[stage1] or 0) > rank0
    -- 0,001 h Spiel: sechs Schritte zu 1/6 h ergeben in Gleitkomma auch 0,99999... (sonst kaeme das Commit erst nach 70 Minuten)
    local at = num(rec.gAt)
    local due = at == nil or now - at < 0 or now - at >= cfg("growCommitH", 1) - 0.001
    if up or loss >= cfg("hpCommit", 0.02) or (s.gDirty == true and due) then commitGrow(rec, s, now) end
    if up then tellStage(rec, stage1, players) end
end

-- ---------------------------------------------------------------------------
-- Neuer Koerper (PLAN_B1D.md 3.1; aus B.PlaceCub direkt nach B.WriteMark): Groesse und Leben SOFORT aus dem Register, sonst heilte jede
-- Autofahrt voll (der neue Koerper hat 0,35 und 1,0, NUR JAR dec/AnimalData.java:1353-1358, dec_b1b/IsoGameCharacter.java:574). Ob
-- setSizeForced direkt nach addToWorld im selben Bild wirkt: ungeprueft -- der naechste Hirn-Takt setzt sicher nach.
-- ---------------------------------------------------------------------------
-- B1e (PLAN_B1E.md 6.2.5): Groesse des VORHANDENEN Koerpers (B.BodyKind; nie bekommt ein Junges-Koerper Erwachsenen-Groesse oder
-- umgekehrt), rec.body = dieser Koerper.
function B.GrowBody(rec, a)
    if type(rec) ~= "table" or a == nil or not isTame(rec.st) or not statsOk() then return end
    local have = B.BodyKind(a) or "cub"
    rec.body = have
    B.ApplySize(a, B.BodySize(rec, have))
    -- F2 (PLAN_F2.md 11.6.1): Schutz SOFORT am neuen Koerper (Tausch Tag 15, C1, Unstuck, Aussteigen) -- keine Luecke von einem Takt
    B.BodyShield(rec, a)
    B.BodyHp(rec, a, 0)
    local s = B.Ses(rec.id)
    s.kx, s.ky, s.kAt, s.kAcc = nil, nil, nil, nil
end

-- ---------------------------------------------------------------------------
-- Fuetter-Bonus (PLAN_B1D.md 1.1 Schritt 4, Kevin 08.11.: "Fuettern beschleunigt", Frage F7). Aus B.FeedComplete am zahmen Jungen,
-- VOR dessen Commit (Abklingzeit und "nur der Besitzer" prueft B.CheckFeed). Je Fuetterung feedGrowFav / Ok / Snack Spielstunden
-- Wachstum, hoechstens feedGrowDay Gutschriften je Spieltag, Summe gF <= feedGrowMax, nie ueber g = 1. Rueckgabe: Zuwachs an g.
-- ---------------------------------------------------------------------------
function B.GrowFeed(rec, class, now)
    if type(rec) ~= "table" or not isTame(rec.st) or not statsOk() then return 0 end
    now = num(now) or B.Now()
    B.GrowFix(rec, now, false)
    local g = rec.g
    if g >= 1 then return 0 end
    local h = 0
    if class == "fav" then
        h = cfg("feedGrowFav", 3)
    elseif class == "ok" then
        h = cfg("feedGrowOk", 2)
    elseif class == "snack" then
        h = cfg("feedGrowSnack", 1)
    end
    if h <= 0 then return 0 end
    local day = math.floor(now / 24)
    if num(rec.gFd) ~= day then
        rec.gFd = day
        rec.gFn = 0
    end
    if rec.gFn >= cfg("feedGrowDay", 2) then return 0 end
    local add = h / (B.GrowDays() * 24)
    local room = cfg("feedGrowMax", 0.10) - rec.gF
    if add > room then add = room end
    if add > 1 - g then add = 1 - g end
    if add <= 0 then return 0 end
    local rank0 = rankOf(g)
    rec.g = g + add
    rec.gF = rec.gF + add
    rec.gFn = rec.gFn + 1
    B.Ses(rec.id).gDirty = true
    B.Log("grow: " .. tostring(rec.id) .. " fed (" .. tostring(class) .. "), " .. tostring(h) .. " h of growth")
    local stage1 = B.StageOf(B.GrowSize(rec.g))
    if (RANK[stage1] or 0) > rank0 then tellStage(rec, stage1, nil) end
    return add
end

-- ---------------------------------------------------------------------------
-- Aus dem Spiegel (PLAN_B1D.md 2.4; gerufen aus server/BanditsNPCBearHeal.lua, nur fuer einen gezaehmten Eintrag).
-- "restore": B.Restore, VOR B.InsertRec -- Felder aus dem Spiegel geklemmt; fehlt g, aus mark.tamedAt. Nur Mehrspieler: g hoechstens
--   (now - tamedAt) / (D x 24) + feedGrowMax (ohne tamedAt hoechstens feedGrowMax). Ehrlich (Nachbesserung B1d B1): rec.tamedAt kommt
--   selbst aus dem Spiegel; B.Restore klemmt es auf [0, now] (Weltstunden sind nie negativ). Der Deckel haelt also nur ein zu hohes g
--   bei ehrlichem tamedAt auf -- ein veraenderter Spiegel mit tamedAt nahe 0 bekommt hoechstens die Zeit seit Weltbeginn. Erfahrung
--   ist dort gar nicht pruefbar (beides Frage F18). hp / hpB bleiben nil -> der erste Abgleich holt das Leben vom Koerper.
-- "newer": B.TakeNewerMark (nur Einzelspieler), VOR B.Touch -- g und Erfahrung = das Groessere (nie schrumpfen), Fuetter-Bonus aus dem
--   Spiegel.
-- ---------------------------------------------------------------------------
local function markFeed(rec, mark)
    local fmax = cfg("feedGrowMax", 0.10)
    rec.gF = clamp(num(mark.gF) or 0, 0, fmax)
    rec.gFn = clamp(math.floor(num(mark.gFn) or 0), 0, math.floor(cfg("feedGrowDay", 2)))
    rec.gFd = num(mark.gFd)
end

function B.GrowFromMark(rec, mark, how)
    if type(rec) ~= "table" or type(mark) ~= "table" or not statsOk() then return end
    local now = B.Now()
    local D = B.GrowDays()
    local top = B.XpCum(10)
    if how == "restore" then
        local g = num(mark.g)
        if g == nil then g = gFromTamed(mark.tamedAt, now, D) end
        g = clamp(g, 0, 1)
        if not B.IsSP() then
            local cap = cfg("feedGrowMax", 0.10)
            local t = num(rec.tamedAt)
            if t ~= nil then cap = cap + (now - t) / (D * 24) end
            cap = clamp(cap, 0, 1)
            if g > cap then
                B.Err("heal: growth of " .. tostring(rec.id) .. " from the mark was capped to " .. tostring(r3(cap))
                    .. " (multiplayer: the mark is not trusted)")
                g = cap
            end
        end
        rec.g = g
        markFeed(rec, mark)
        for i = 1, #B.SKILLS do
            local f = B.SKILL_FIELD[B.SKILLS[i]]
            rec[f] = clamp(num(mark[f]) or 0, 0, top)
        end
        rec.hp, rec.hpB, rec.gAt = nil, nil, nil
    elseif how == "newer" then
        B.GrowFix(rec, now, false)
        local mg = num(mark.g)
        if mg ~= nil then
            mg = clamp(mg, 0, 1)
            if mg > rec.g then rec.g = mg end
        end
        for i = 1, #B.SKILLS do
            local f = B.SKILL_FIELD[B.SKILLS[i]]
            local mx = num(mark[f])
            if mx ~= nil then
                mx = clamp(mx, 0, top)
                if mx > rec[f] then rec[f] = mx end
            end
        end
        markFeed(rec, mark)
    end
end

-- ---------------------------------------------------------------------------
-- Sicht (PLAN_B1D.md 4.1): fertige Zahlen fuer den Client, nur fuer einen gezaehmten Eintrag; schreibt nur in t (aus viewEntry).
-- sz (gezeigte Groesse), hp (Prozent 0..100, fehlt solange rec.hp fehlt), hpMax, sta (Prozent, Sitzung; ohne Sitzung 100), staMax,
-- day, stg, nst / nxt (fehlen, wenn ausgewachsen).
-- B1e (PLAN_B1E.md 4.2): bd = Koerper, den der Eintrag JETZT hat ("cub"/"big"), sz = dessen gezeigte Groesse (B.BodyNow ueber
-- B.StatsOf). Ein Junges, dessen Tausch noch wartet, zeigt also bd "cub" und 0,75.
-- F1 (PLAN_F1.md 5.3): fuer tame UND missing (das Baeren-Fenster zeigt auch einen vermissten Baeren); dazu die Erfahrung je Faehigkeit
-- xAgi .. xNos (auf 0,1), carry (ganze Zahl), dodge / fgtB / fish (Prozent, auf 0,1) und nose (Kacheln, auf 0,1) aus B.StatsOf.
-- Fehlt rec.hp (noch nie abgeglichen), fehlt hp -- nie 0.
-- ---------------------------------------------------------------------------
local VIEW_X = { "xAgi", "xVit", "xCon", "xFgt", "xFsh", "xNos" }

function B.GrowView(rec, t)
    if type(rec) ~= "table" or type(t) ~= "table" or not isTame(rec.st) or not statsOk() then return end
    local st = B.StatsOf(rec)
    t.sz = st.sz
    t.bd = st.body
    local hp = num(rec.hp)
    if hp ~= nil then
        local p = math.floor(hp * 100 + 0.5)
        if p < 1 and hp > 0 then p = 1 end
        t.hp = clamp(p, 0, 100)
    end
    t.hpMax = math.floor(st.hpMax + 0.5)
    local s = B._s[rec.id]
    local sta = 1
    if s ~= nil and num(s.sta) ~= nil then sta = num(s.sta) end
    t.sta = clamp(math.floor(sta * 100 + 0.5), 0, 100)
    t.staMax = math.floor(st.staMax + 0.5)
    t.day = st.day
    t.stg = st.stage
    t.nst = st.next
    t.nxt = st.nextDays
    -- F1: Faehigkeiten (Erfahrung; Stufe und Fortschritt rechnet der Client mit B.SkillProgress auf demselben Feldnamen) und Werte.
    -- Erfahrung ABGERUNDET auf 0,1: so zeigt der Client nie eine hoehere Stufe als der Schreiber rechnet (99,96 bliebe Stufe 0).
    for i = 1, #VIEW_X do
        local k = VIEW_X[i]
        local v = num(rec[k])
        if v ~= nil and v > 0 then t[k] = math.floor(v * 10 + 0.000001) / 10 end
    end
    -- F2 (PLAN_F2.md 11.4): Alters-Deckel der Faehigkeiten (nur, wenn unter 10) -- das Fenster graut Balken an der Grenze aus
    if B.SkillCapLv then
        local capL = B.SkillCapLv(rec)
        if capL < 10 then t.skCap = capL end
    end
    t.carry = math.floor((num(st.carry) or 0) + 0.5)
    t.dodge = B.Round1(num(st.dodge) or 0)
    t.fgtB = B.Round1(num(st.fightBonus) or 0)
    t.fish = B.Round1(num(st.fish) or 0)
    t.nose = B.Round1(num(st.nose) or 0)
end

-- ---------------------------------------------------------------------------
-- Von Hand (Probebefehle der Test-Mod zum Vorspulen und Verletzen; spaeter Baeren-Fenster und Von-Hand-Heilen). Nur gezaehmt/vermisst.
-- ---------------------------------------------------------------------------

-- Wachstum setzen (geklemmt 0..1), Stufen-Meldung nur aufwaerts, Commit, Groesse sofort. Rueckgabe: neues g.
-- B1e (PLAN_B1E.md 1.3 Nr. 1, 6.2.5): von Hand gibt es keine Abklingzeit des Tauschs (swapAt / swapTryAt geleert) -- der naechste
-- Hirn-Takt tauscht, wenn noetig; die Groesse hier nur fuer den VORHANDENEN Koerper.
function B.GrowSetG(rec, g, players)
    if type(rec) ~= "table" or not isTame(rec.st) or not statsOk() then return nil end
    local now = B.Now()
    B.GrowFix(rec, now, false)
    local v = clamp(num(g) or rec.g, 0, 1)
    local rank0 = rankOf(rec.g)
    rec.g = v
    local s = B.Ses(rec.id)
    s.swapAt, s.swapTryAt = nil, nil
    commitGrow(rec, s, now)
    local a = B.FindAnimal(rec)
    if a ~= nil then
        B.ApplySize(a, B.BodySize(rec, B.BodyKind(a) or "cub"))
    end
    local stage1 = B.StageOf(B.GrowSize(v))
    if (RANK[stage1] or 0) > rank0 then tellStage(rec, stage1, players) end
    return v
end

-- Leben setzen (Anteil 0,01..1): erst den Koerper abgleichen (ausstehender Schaden zaehlt), dann den neuen Wert setzen, Commit.
function B.GrowSetHp(rec, frac)
    if type(rec) ~= "table" or not isTame(rec.st) or not statsOk() then return end
    local v = num(frac)
    if v == nil then return end
    v = clamp(v, 0.01, 1)
    local a = B.FindAnimal(rec)
    if a ~= nil then B.BodyHp(rec, a, 0) end
    rec.hp = v
    B.BodyHp(rec, a, 0)
    B.Commit(rec)
end
