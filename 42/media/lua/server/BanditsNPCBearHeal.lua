if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Spiegel v2 und Register-Selbstheilung (B1c, PLAN_B1C.md 1.1, 2).
--
-- Kevins Fall (baer/STAND.md N9): nach einem Absturz war das Register leer, das gezaehmte Junge mit seinem Spiegel aber da -- es
-- wurde als neues "found" Junges gefuehrt, die Zaehmung war weg. Ab B1c traegt der Spiegel am Tier (animal:getModData().tcBear)
-- alles Wichtige (B.MarkOf). Fehlt der Eintrag, wird er daraus WIEDERHERGESTELLT (gleicher Zustand, gleicher Besitzer), nie neu
-- als found/shy -- solange die Regeln es erlauben (B.HealFromMark, B.Restore).
--
-- Vertrauen (PLAN_B1C.md 2.5): im Mehrspieler kann ein veraenderter Client die ModData eines Tiers am Server ueberschreiben (Jar
-- dec/ObjectModDataPacket.java, forschung_b1c.md 0.1). Deshalb gewinnt IMMER das Register: ein Spiegel zaehlt nur, wenn kein
-- Eintrag widerspricht (Kennzeichen u, Koerper-Generation gen, AnimalID), der Deckel je Spieler (BearMaxPerPlayer) gilt, ein Spiegel
-- mit Besitzer nil oder "__sp" ist im Mehrspieler nicht als gezaehmt herstellbar, und jede Heilung schreibt eine Fehlerzeile.
-- Nachbesserung B1c: (B1) im EINZELSPIELER gewinnt ein Spiegel, der nachweislich NEUER ist als sein Eintrag (Register aelter als die
-- Zelle nach einem Absturz; B.TakeNewerMark) -- im Mehrspieler bleibt das Register; (B3) ein spaeter gefundener neuerer Koerper loest
-- eine zuerst geheilte alte Kopie ab; (B10) im Mehrspieler bindet ein Spiegel gleicher Generation nur am Tier mit der AnimalID des
-- Eintrags. B.RecOf macht aus einem nicht herstellbaren zahmen Spiegel nie einen neuen Fund (server/BanditsNPCBearRegistry.lua, A1).
--
-- Engine-Aufrufe hier: animal:getModData() (lesen/schreiben, Vanilla client/ISUI/ISInventoryPaneContextMenu.lua:4127,
-- shared/Definitions/animal/ButcheringUtil.lua:596), animal:getAnimalID() (client/ISUI/Animal/ISAnimalUI.lua:53; am Server nur
-- Client-belegt, A3 aus B1a, offen), getX/getY/getZ am Tier (ButcheringUtil.lua:575-577), isExistInTheWorld
-- (shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29), isDead am Tier (server/Traps/STrapGlobalObject.lua:238).
-- Ladefolge: diese Datei laedt VOR ...Registry / ...Ride / ...Server / ...World (alphabetisch); fremde Funktionen nur zur Laufzeit.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

-- Felder des Spiegels v2 (PLAN_B1C.md 2.2) ausser v / ep (die setzt B.MarkOf). Nur Zahlen, Texte, Wahrheitswerte.
-- Nicht im Spiegel: Lage (das Tier IST die Lage), aid (das Tier kennt sie selbst), Sitzungs-Uhren, ride, idleH, goneP, miss*, hintAt.
-- B1d (PLAN_B1D.md 2.3): + Wachstum, Fuetter-Bonus, Erfahrung (Fassung bleibt B.MARK_V = 2; Leser nehmen fehlende Felder als "nicht
-- da"). Nicht im Spiegel: hp / hpB (das Tier traegt sein Leben selbst, NUR JAR dec/IsoAnimal.java:1340), gAt, Sitzung.
-- B1e (PLAN_B1E.md 4.2): + body (Koerper "cub"/"big"; nur Diagnose -- beim Binden und Wiederherstellen gilt die Art des Tiers,
-- B.BodyKind). Fassung bleibt B.MARK_V = 2.
local MARK_FIELDS = {
    "u", "id", "nr", "gen", "r", "kind", "src", "st", "finder", "bond", "owner", "tame", "fedN", "petN", "last",
    "feedAt", "petAt", "born", "tamedAt", "mode", "name", "hx", "hy", "hz",
    "g", "gF", "gFd", "gFn", "xAgi", "xVit", "xCon", "xFgt", "xFsh", "xNos",
    "body",
}

local function plain(v)
    local t = type(v)
    return t == "number" or t == "string" or t == "boolean"
end

local function objAlive(o)
    -- isExistInTheWorld: Vanilla shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; isDead: server/Traps/STrapGlobalObject.lua:238
    return o ~= nil and o:isExistInTheWorld() and not o:isDead()
end

-- Spiegel v2 eines Eintrags als neue Tabelle.
function B.MarkOf(rec)
    local reg = B.Reg()
    local mark = { v = B.MARK_V }
    if reg and tonumber(reg.ep) ~= nil then mark.ep = reg.ep end
    if type(rec) ~= "table" then return mark end
    for i = 1, #MARK_FIELDS do
        local k = MARK_FIELDS[i]
        local v = rec[k]
        if v ~= nil and plain(v) then mark[k] = v end
    end
    return mark
end

-- Spiegel ganz ersetzen (kein isExistInTheWorld-Riegel: direkt nach addToWorld ist die Antwort noch falsch, Fix 1).
-- getModData am Tier: Vanilla client/ISUI/ISInventoryPaneContextMenu.lua:4127 (schreiben).
function B.WriteMark(rec, a)
    if type(rec) ~= "table" or not a then return end
    local md = a:getModData()
    if md then md[B.MARK] = B.MarkOf(rec) end
end

-- Passt der Spiegel noch zum Eintrag? Billig: Fassung, Kennung, Kennzeichen, Aenderungszaehler.
function B.MarkFresh(rec, mark)
    return type(rec) == "table" and type(mark) == "table" and mark.v == B.MARK_V and mark.id == rec.id and mark.u == rec.u
        and mark.r == rec.r
end

-- Ein Eintrag bekommt dieses Tier (Heilung 2.3 1a / 1b / 2a): Objekt der Sitzung, AnimalID, Generation, kein ride mehr (ein Koerper
-- ist da), vermisst -> gezaehmt mit Meldung, Spiegel neu, festschreiben.
-- Nachbesserung B1c B1: ist der Spiegel NEUER als der Eintrag (B.TakeNewerMark, weiter unten), gewinnt im Einzelspieler zuerst der
-- Spiegel -- sonst schriebe B.Commit den alten Stand des Registers ueber die neuere Zaehmung (N9 in anderer Form).
-- B1e (PLAN_B1E.md 1.3 Nr. 5, 6.3): rec.body = Koerper des Tiers (B.BodyKind; nur gezaehmt/vermisst, sonst nil); weicht der Spiegel ab,
-- nur eine Diagnose-Zeile.
local function bind(rec, o, mark, players)
    if mark ~= nil and B.TakeNewerMark then B.TakeNewerMark(rec, mark) end
    local s = B.Ses(rec.id)
    s.obj = o
    s.ride = nil
    rec.aid = o:getAnimalID()
    local body = B.BodyKind(o)
    if rec.st == "tame" or rec.st == "missing" then rec.body = body else rec.body = nil end
    if type(mark) == "table" and mark.body ~= nil and mark.body ~= body then
        B.Log("heal: " .. tostring(rec.id) .. " mark says body " .. tostring(mark.body) .. ", the animal is " .. tostring(body))
    end
    local mg = mark and tonumber(mark.gen) or nil
    local rg = tonumber(rec.gen) or 0
    if mg ~= nil and mg > rg then rg = mg end
    rec.gen = rg
    rec.ride = nil
    rec.x, rec.y, rec.z = math.floor(o:getX()), math.floor(o:getY()), math.floor(o:getZ())
    rec.missN = 0
    rec.missAt = nil
    local back = false
    if rec.st == "missing" then
        rec.st = "tame"
        rec.missH = 0
        back = true
    end
    B.Commit(rec)                      -- r + 1, Spiegel (das Tier ist in der Welt)
    B.WriteMark(rec, o)                -- auch, falls isExistInTheWorld gerade falsch ist
    if back and rec.owner ~= nil then
        local p = B.PlayerByKey(rec.owner, players)
        if p then B.Tell(p, note("UI_BN_Bear_Note_Back", nil, nil, "good")) end
    end
    return rec
end

local function isNewShy(st)
    return st == "new" or st == "shy"
end

-- Kennzeichen u als Zahl (oder nil).
local function markU(mark)
    return tonumber(mark.u)
end

local function isV2(mark)
    local v = tonumber(mark.v)
    return v ~= nil and v >= 2 and markU(mark) ~= nil
end

-- Lebt ein ANDERES Objekt dieses Eintrags (gemerkt in der Sitzung)?
local function otherAlive(rec, o)
    local s = B._s[rec.id]
    local other = s and s.obj
    return other ~= nil and other ~= o and objAlive(other)
end

-- Widerspruch per AnimalID (2.3 1b): genau EIN Eintrag ohne lebendes Objekt mit aid == AnimalID von o und hoechstens 40 Kacheln
-- von seiner letzten Kachel. Mehrere -> nil (nie raten).
local function byAnimalId(reg, o)
    local aid = o:getAnimalID()
    local hit, hits = nil, 0
    for id, rec in pairs(reg.cubs) do
        local s = B._s[id]
        local live = s ~= nil and objAlive(s.obj)
        if not live and rec.ride == nil and rec.aid == aid and B.DistXY(o:getX(), o:getY(), rec.x, rec.y) <= 40 then
            hit = rec
            hits = hits + 1
        end
    end
    if hits == 1 then return hit end
    return nil
end

-- ---------------------------------------------------------------------------
-- Wiederherstellen (PLAN_B1C.md 2.4). o = lebendes ncbearcub (B1e: oder ncbeargrown) ohne Eintrag; mark = Spiegel (v2 oder die
-- v1-Ersatztabelle aus 2.3 2c).
-- Rueckgabe: rec oder nil, why ("full" / "state" / "nokey" / "cap").
-- ---------------------------------------------------------------------------
local function num(v, lo, hi)
    local n = tonumber(v)
    if n == nil then return nil end
    if lo ~= nil and n < lo then n = lo end
    if hi ~= nil and n > hi then n = hi end
    return n
end

-- Schluessel aus dem Spiegel: SP -> jeder gesetzte wird "__sp" (es gibt nur einen Spieler); MP -> nur Texte ungleich "__sp".
local function keyOf(v)
    if v == nil then return nil end
    if B.IsSP() then return B.SP_KEY end
    if type(v) ~= "string" or v == B.SP_KEY or v == "" then return nil end
    return v
end

-- B1e (PLAN_B1E.md 1.3 Nr. 5, 4.3, 6.3): ein GROSSER Koerper gehoert nur zu einem gezaehmten Eintrag -- mit einem Spiegel new/shy/fed
-- (nur als Faelschung moeglich) wird er nie hergestellt (nil, "body"; der Aufrufer schreibt die Fehlerzeile). Der neue Eintrag traegt
-- den Koerper des Tiers (body, nur bei tame).
function B.Restore(o, mark, players)
    local reg = B.Reg()
    if not reg or not o or type(mark) ~= "table" then return nil, "state" end
    if B.CountRecs() >= B.CFG.maxRecs then return nil, "full" end
    local st = mark.st
    if st == "missing" then st = "tame" end
    if st ~= "new" and st ~= "shy" and st ~= "fed" and st ~= "tame" then return nil, "state" end
    local body = B.BodyKind(o) or "cub"
    if body == "big" and st ~= "tame" then return nil, "body" end
    local now = B.Now()
    local owner, bond, finder = keyOf(mark.owner), keyOf(mark.bond), keyOf(mark.finder)
    local max = B.Opt("BearMaxPerPlayer")
    if st == "tame" then
        if owner == nil then return nil, "nokey" end
        if B.SlotsOf(owner, now).bears >= max then return nil, "cap" end
        if bond == nil then bond = owner end
    elseif st == "fed" then
        if bond == nil then return nil, "nokey" end
        local slots = B.SlotsOf(bond, now)
        if slots.bonded ~= nil or slots.bears >= max then return nil, "cap" end
        owner = nil
    else
        -- new/shy (nur aus einer fremden Epoche, 2.3 1c): kommt als scheues Junges zurueck; der Finder nur, wenn sein Platz frei ist
        st = "shy"
        owner, bond = nil, nil
        if finder ~= nil and B.SlotsOf(finder, now).wild ~= nil then finder = nil end
    end
    -- Kennung: die alte, wenn frei und lesbar ("b<nr>"; ein v1-Spiegel kennt nr nicht -> aus der Kennung), sonst eine neue.
    local id, nr = nil, nil
    if type(mark.id) == "string" and reg.cubs[mark.id] == nil then
        nr = num(mark.nr)
        if nr == nil and string.sub(mark.id, 1, 1) == "b" then nr = tonumber(string.sub(mark.id, 2)) end
        if nr ~= nil and nr >= 1 and mark.id == "b" .. string.format("%d", math.floor(nr)) then
            id = mark.id
            nr = math.floor(nr)
            B.BumpN(nr)
        end
    end
    if id == nil then id, nr = B.NewId() end
    local mode = nil
    if mark.mode == "follow" or mark.mode == "stay" then mode = mark.mode end
    local name = nil
    if type(mark.name) == "string" then name = B.CleanName(mark.name) end
    local hx, hy, hz = num(mark.hx), num(mark.hy), num(mark.hz)
    if hx == nil or hy == nil or hz == nil then hx, hy, hz = nil, nil, nil end
    local last = nil
    if mark.last == "feed" or mark.last == "pet" then last = mark.last end
    local u = markU(mark)
    if u == nil or B.RecByU(u) ~= nil then u = B.NewU() end
    local src = mark.src
    if src ~= "forest" and src ~= "bait" and src ~= "found" then src = "found" end
    local x, y, z = math.floor(o:getX()), math.floor(o:getY()), math.floor(o:getZ())
    local rec = {
        id = id, nr = nr, kind = "cub",
        u = u, gen = math.floor(num(mark.gen, 0) or 0), r = 0,
        aid = o:getAnimalID(),
        src = src, st = st,
        finder = finder, bond = bond, owner = owner,
        tame = B.Round1(num(mark.tame, 0, 100) or 0), fedN = math.floor(num(mark.fedN, 0) or 0),
        petN = math.floor(num(mark.petN, 0) or 0), last = last,
        feedAt = num(mark.feedAt), petAt = num(mark.petAt),
        -- Nachbesserung B1d B1: Weltstunden sind nie negativ und nie spaeter als jetzt -- geklemmt, denn tamedAt traegt im
        -- Mehrspieler den Wachstums-Deckel (server/BanditsNPCBearGrow.lua B.GrowFromMark "restore")
        born = num(mark.born, 0, now) or now, tamedAt = num(mark.tamedAt, 0, now),
        idleH = 0, goneP = nil, missN = 0, missAt = nil, missH = 0, hintAt = nil,
        x = x, y = y, z = z,
        hx = hx, hy = hy, hz = hz,
        mode = mode, name = name,
        -- Nachbesserung B1c B3: r und gen des Quell-Spiegels merken -- ein spaeter gefundener Koerper derselben Quell-Epoche mit
        -- hoeherem r ist neuer (B.TakeNewerMark, Heil-Regel 1a)
        healed = { at = now, ep = num(mark.ep), r = num(mark.r), gen = num(mark.gen) },
    }
    if st == "tame" then
        rec.tame = 100
        rec.body = body                    -- B1e
    end
    if st ~= "tame" then rec.mode = nil end
    -- B1d (PLAN_B1D.md 2.4 "restore"): Wachstum und Erfahrung aus dem Spiegel, geklemmt; im Mehrspieler g gedeckelt (Grow.lua)
    if st == "tame" and B.GrowFromMark then B.GrowFromMark(rec, mark, "restore") end
    B.InsertRec(rec, o)
    B.Err("heal: entry " .. tostring(id) .. " (" .. st .. ", owner " .. tostring(owner) .. ") restored from the mark on the animal")
    local key = owner or bond
    if key ~= nil then
        local p = B.PlayerByKey(key, players)
        if p then B.Tell(p, note("UI_BN_Bear_Note_Back", nil, nil, "good")) end
    end
    return rec, nil
end

-- ---------------------------------------------------------------------------
-- Heil-Regeln (PLAN_B1C.md 2.3). o = lebendes ncbearcub (B1e: oder ncbeargrown), das in dieser Sitzung KEINEM Eintrag als Objekt
-- gehoert; mark = sein Spiegel.
-- Rueckgabe: rec (gebunden bzw. wiederhergestellt), "stale" (veraltete Kopie), "dup" (Doppel) oder nil (nichts).
-- ---------------------------------------------------------------------------
local function capLine(mark, why)
    B.ErrEvery("heal:" .. tostring(mark.u or mark.id), 600000, "heal: the cub with mark " .. tostring(mark.id) .. " ("
        .. tostring(mark.st) .. ", owner " .. tostring(mark.owner) .. ") was not restored: " .. tostring(why))
end

-- ---------------------------------------------------------------------------
-- Nachbesserung B1c B1 / B3: ein Spiegel, der NEUER ist als sein Eintrag.
-- Das gibt es nur, wenn das Register aelter ist als die Zelle des Tiers: nach einem Absturz kann die Zelle beim Entladen gespeichert
-- worden sein, die globale ModData aber nicht (baer/STAND.md N9 zeigt genau diese Mischung; dass Zellen beim Entladen geschrieben
-- werden, ist eine Annahme). Im laufenden Spiel ist mark.r nie groesser als rec.r: jede Aenderung zaehlt rec.r hoch (B.Commit), der
-- Spiegel bekommt hoechstens denselben Wert.
-- Vergleichbar ist r nur in EINER Epoche: der des Registers (mark.r > rec.r) oder der Quell-Epoche des Spiegels, aus dem der Eintrag
-- wiederhergestellt wurde (rec.healed.ep, mark.r > rec.healed.r -- B3: erst die alte Kopie geheilt, dann der echte Koerper gefunden).
-- Gleiches Kennzeichen u ist Pflicht.
-- ---------------------------------------------------------------------------
local function markAhead(rec, mark, reg)
    if type(rec) ~= "table" or type(mark) ~= "table" or not isV2(mark) or markU(mark) ~= rec.u then return false end
    local mr = tonumber(mark.r)
    if mr == nil or mark.ep == nil then return false end
    if mark.ep == reg.ep then return mr > (tonumber(rec.r) or 0) end
    local h = rec.healed
    if type(h) == "table" and tonumber(h.ep) ~= nil and tonumber(h.ep) == tonumber(mark.ep) then
        local hr = tonumber(h.r)
        return hr ~= nil and mr > hr
    end
    return false
end

-- Die Felder eines NEUEREN Spiegels uebernehmen, geklemmt wie B.Restore. Einzelspieler: voll vertrauen (es gibt keinen Fremden,
-- forschung_b1c.md 0.1). Mehrspieler: das Register gewinnt -- ein Client kann die ModData eines Tiers am Server schreiben (Jar
-- dec/ObjectModDataPacket.java), "neuer" ist dort nicht pruefbar; nur eine Fehlerzeile je Junges und 10 Minuten. Nie zurueck aus
-- "tame"/"missing" (ein gezaehmtes Junges wird nie wieder wild), Deckel je Spieler (BearMaxPerPlayer) wie B.Restore. Kennung, u,
-- Herkunft und Generation bleiben die des Eintrags. Rueckgabe true, wenn uebernommen (eine Fehlerzeile).
function B.TakeNewerMark(rec, mark)
    local reg = B.Reg()
    if not reg or not markAhead(rec, mark, reg) then return false end
    local id = tostring(rec.id)
    if not B.IsSP() then
        B.ErrEvery("newer:" .. id, 600000, "heal: the mark on " .. id .. " is newer than its entry (multiplayer: the entry wins)")
        return false
    end
    local st = mark.st
    if st == "missing" then st = "tame" end
    if st ~= "new" and st ~= "shy" and st ~= "fed" and st ~= "tame" then return false end
    local was = rec.st
    if (was == "tame" or was == "missing") and st ~= "tame" then
        B.ErrEvery("newer:" .. id, 600000, "heal: the newer mark on " .. id .. " says " .. tostring(mark.st) .. ", the entry stays tame")
        return false
    end
    local now = B.Now()
    local max = B.Opt("BearMaxPerPlayer")
    local owner, bond, finder = keyOf(mark.owner), keyOf(mark.bond), keyOf(mark.finder)
    if st == "tame" then
        if owner == nil then return false end
        local mine = 0
        if rec.owner == owner then mine = 1 end          -- B.SlotsOf zaehlt diesen Eintrag schon mit
        if B.SlotsOf(owner, now).bears - mine >= max then
            capLine(mark, "cap (newer mark)")
            return false
        end
        if bond == nil then bond = owner end
    elseif st == "fed" then
        if bond == nil then return false end
        local slots = B.SlotsOf(bond, now)
        if (slots.bonded ~= nil and slots.bonded ~= rec.id) or slots.bears >= max then
            capLine(mark, "cap (newer mark)")
            return false
        end
        owner = nil
    else
        owner, bond = nil, nil
        if finder ~= nil then
            local w = B.SlotsOf(finder, now).wild
            if w ~= nil and w ~= rec.id then finder = nil end
        end
    end
    rec.st = st
    rec.owner, rec.bond, rec.finder = owner, bond, finder
    rec.tame = B.Round1(num(mark.tame, 0, 100) or 0)
    if st == "tame" then rec.tame = 100 end
    rec.fedN = math.floor(num(mark.fedN, 0) or 0)
    rec.petN = math.floor(num(mark.petN, 0) or 0)
    rec.last = nil
    if mark.last == "feed" or mark.last == "pet" then rec.last = mark.last end
    rec.feedAt, rec.petAt, rec.tamedAt = num(mark.feedAt), num(mark.petAt), num(mark.tamedAt, 0, now)   -- tamedAt: wie B.Restore (B1d B1)
    rec.mode = nil
    if st == "tame" and (mark.mode == "follow" or mark.mode == "stay") then rec.mode = mark.mode end
    rec.name = nil
    if type(mark.name) == "string" then rec.name = B.CleanName(mark.name) end
    local hx, hy, hz = num(mark.hx), num(mark.hy), num(mark.hz)
    if hx == nil or hy == nil or hz == nil then hx, hy, hz = nil, nil, nil end
    rec.hx, rec.hy, rec.hz = hx, hy, hz
    if st ~= "new" and st ~= "shy" then rec.goneP = nil end
    local mr = tonumber(mark.r) or 0
    if mark.ep == reg.ep then
        if mr > (tonumber(rec.r) or 0) then rec.r = mr end          -- B.Commit danach: r = mark.r + 1
    else
        rec.healed.r = mr                                           -- eine noch aeltere Kopie ist danach nie "neuer"
    end
    B.Err("heal: entry " .. id .. " updated from a newer mark on the animal (" .. tostring(was) .. " -> " .. st .. ")")
    -- B1d (PLAN_B1D.md 2.4 "newer"): g und Erfahrung = das Groessere, Fuetter-Bonus aus dem Spiegel (Grow.lua)
    if st == "tame" and B.GrowFromMark then B.GrowFromMark(rec, mark, "newer") end
    B.Touch(rec)
    return true
end

function B.HealFromMark(o, mark, players)
    local reg = B.Reg()
    if not reg or not o or type(mark) ~= "table" then return nil end
    if isV2(mark) then
        local u = markU(mark)
        -- 3: Zaehler nachziehen (auch, wenn gebunden), nur fuer Spiegel aus DIESEM Register
        if mark.ep == reg.ep then B.BumpN(mark.nr) end
        local mg = tonumber(mark.gen) or 0
        -- 1a: ein Eintrag mit diesem Kennzeichen
        local rec = B.RecByU(u)
        if rec ~= nil then
            local rg = tonumber(rec.gen) or 0
            if otherAlive(rec, o) then
                if mg < rg then return "stale" end
                -- Nachbesserung B1c B3 (nur Einzelspieler): der Eintrag kam aus dem Spiegel einer ALTEN Kopie (Register verloren, die
                -- alte Kopie wurde zuerst gefunden), dieses Tier hat die hoehere Generation und den neueren Spiegel derselben
                -- Quell-Epoche -> es ist der echte Koerper: binden (B.TakeNewerMark holt Name, Modus ...); die alte Kopie ist danach
                -- ungebunden und wird beim naechsten Suchlauf "stale".
                if mg > rg and B.IsSP() and markAhead(rec, mark, reg) then
                    B.Log("heal: " .. tostring(rec.id) .. " moved to its newer body (gen " .. tostring(mg) .. " > " .. tostring(rg) .. ")")
                    return bind(rec, o, mark, players)
                end
                -- Doppel -- es sei denn, das Register kennt dieses Tier per AnimalID als einen ANDEREN Eintrag ohne Koerper (ein
                -- fremder Spiegel wurde auf ein Junges mit eigenem Eintrag kopiert, MP): dann gewinnt das Register (PLAN_B1C.md 2.5)
                local own = byAnimalId(reg, o)
                if own ~= nil and own ~= rec then
                    B.Log("heal: mark of " .. tostring(mark.id) .. " belongs to a living cub, bound to entry " .. tostring(own.id)
                        .. " by animal id")
                    return bind(own, o, nil, players)
                end
                return "dup"
            end
            if mg < rg then return "stale" end
            -- Nachbesserung B1c B10 (Mehrspieler): gleiche Generation = derselbe Koerper, und den kennt das Register an seiner
            -- AnimalID (die Engine speichert sie mit dem Tier: Jar dec/IsoAnimal.java:1279 / :1391). Traegt ein ANDERES Tier diesen
            -- Spiegel (ein veraenderter Client kann ModData am Server schreiben), wird nicht gebunden und nichts entfernt (nil).
            if mg == rg and not B.IsSP() and rec.aid ~= nil and rec.aid ~= o:getAnimalID() then
                capLine(mark, "same body generation, other animal id (copied mark?)")
                return nil
            end
            return bind(rec, o, mark, players)
        end
        -- 1b: das Register widerspricht per AnimalID
        local hit = byAnimalId(reg, o)
        if hit ~= nil then
            B.Log("heal: mark of " .. tostring(mark.id) .. " did not match, bound to its entry " .. tostring(hit.id) .. " by animal id")
            return bind(hit, o, nil, players)
        end
        -- 1c: in DIESEM Register weitergezogen (B1a-Regel)
        if mark.ep == reg.ep and isNewShy(mark.st) then return "stale" end
        -- 1d: wiederherstellen
        local got, why = B.Restore(o, mark, players)
        if got == nil then capLine(mark, why) end
        return got
    end
    -- 2: v1 (B1a/B1b { id, st })
    local rec = reg.cubs[mark.id]
    if rec ~= nil then
        if rec.aid == o:getAnimalID() then
            if otherAlive(rec, o) then return "dup" end
            return bind(rec, o, nil, players)          -- Migration: der Spiegel wird v2
        end
        return nil
    end
    if isNewShy(mark.st) then return "stale" end
    if mark.st == "tame" and B.IsSP() then
        local fake = {
            st = "tame", owner = B.SP_KEY, tame = 100, fedN = B.Opt("BearTameMinFeedings"), src = "found", id = mark.id,
        }
        local got, why = B.Restore(o, fake, players)
        if got == nil then capLine(mark, why) end
        return got
    end
    return nil
end
