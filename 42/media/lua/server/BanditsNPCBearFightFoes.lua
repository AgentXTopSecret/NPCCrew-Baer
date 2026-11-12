if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Gegner beim Schreiber: Suche und Angriffe AUF den Baeren (F2 = B5a, PLAN_F2.md 0.1, 0.2, 0.5, 0.16, 2.1, 4.2, 4.3).
--
-- Kevin ENT:261-266 ("ja nur ungetamte greifen die nicht an"): Zombies greifen JEDEN gezaehmten Baeren an (Junges und grosser Koerper, auch
-- passiv, sitzend, bleibend, frei), wilde / scheue / angefuetterte nie, am Boden und mitfahrend nie. Feindliche Banditen (nur hostile /
-- hostileP, Bandits' eigene Felder) ebenso. Crew, Neutrale, Begleiter, "babe", passive und niedergeschlagene NPC-Crew-Figuren, Spieler und
-- Tiere nie (B.FoeIsTarget, shared/BanditsNPCBearFightRules.lua; Ziele nur aus der Zombieliste). Sandbox BearZombiesAttack aus -> niemand
-- greift an (die Suche laeuft weiter, der Baer selbst kaempft dann trotzdem).
-- Weg 2 "nachgebaut" (ENT:60, die echte Engine-Attacke auf ein Tier geht nicht): das Hinlaufen macht der Zombie-Rechner
-- (shared/BanditsNPCBearFoe.lua B.FoeLureTick), hier ENTSCHEIDET der Schreiber: wer in Reichweite ist, beginnt einen Biss (Zombie) bzw.
-- Hieb (Bandit) -- Fx "zbite" / "smack" an die Clients (Bild am Zombie) -- und nach der Uhr (B.CLIPS zbite / smack, nie das Bild) zaehlt der
-- Treffer, wenn der Gegner noch in Reichweite + 0,25 steht, auf derselben Ebene und ohne Wand dazwischen: B.BearHurt
-- (server/BanditsNPCBearHurt.lua; Ausweichen, Schaden, Tod). Deckel: Junges 2, grosser Koerper 4 gleichzeitige Angreifer, 64 laufende
-- Angriffe, 128 Abklingzeiten, je Baer 8 gemerkte Gegner (aus den naechsten 24 Zombies und getrennt 8 Banditen, Nachbesserung F2 B2),
-- 1500 Zombies je Suche.
-- Ohne Bandits: keine Banditen, Zombies aus der Zellenliste, kein Fehler. Im Mehrspieler rechnet der Server aus SEINEN Zombie-Objekten
-- (Lage aus den Paketen des Hoheits-Clients, forschung_f2_gegner.md 4); Banditen-Gehirn ueber Bandits' Cluster (nie BanditBrain.Get am
-- Server). Kachel-Fragen (isSomethingTo) und Zustands-Fragen (isProne ...) am Server: GRENZFALL (Methoden des Charakters; am Server gibt es
-- dafuer nur die Zombieliste-Belege) -- Testpunkt im MP.
-- Ladefolge: server/ alphabetisch (...Fight < ...FightFoes < ...Follow ...); fremde Funktionen nur zur Laufzeit ueber B.X.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

B._foes = B._foes or {}             -- [id] = { { o, kind = "z"/"b", oid, x, y, z, d }, ... } (<= foeListMax, nach Abstand), je Suche neu
B._foeN = B._foeN or 0              -- Zahl aller gemerkten Gegner (Riegel des Kampf-Takts, server/BanditsNPCBearFight.lua)
B._fa = B._fa or {}                 -- laufende Gegner-Angriffe { id, a, o, kind, oid, t0, hitAt, clipEnd, endAt, done } (<= foePendMax)
B._fcd = B._fcd or {}               -- [oid] = Echtzeit, bis zu der dieser Gegner nicht neu angreift (<= 128)
B._fcdN = B._fcdN or 0
B._fightLive = B._fightLive or {}   -- { { rec, a, x, y, z }, ... } aus brainTickBody Schritt 4 (gezaehmt, geladen, nicht mitfahrend)
B._foeAt = B._foeAt or nil          -- Echtzeit der letzten Suche

local scanFrom = 0                  -- rollender Anfang in der Zellenliste

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

-- ---------------------------------------------------------------------------
-- Gegner erkennen (2.1.1, 4.3 B.FoeIsTarget). Gehirn eines Banditen: SP aus Bandits' Lichttabelle (light.brain, Bandits
-- client/BanditZombie.lua:79) bzw. BanditBrain.Get(z) (Bandits shared/BanditBrain.lua:3-6); Server: GetBanditClusterData(BanditUtils.
-- GetZombieID(z))[id] (Bandits server/BanditSave.lua:19-21; Staging-Weg server/BanditsNPCBearWorld.lua isBanditZ). Ohne Bandits: nil.
-- ---------------------------------------------------------------------------
local function brainOf(z, light)
    if type(light) == "table" and type(light.brain) == "table" then return light.brain end
    if B.IsSP() then
        local bb = BanditBrain
        if type(bb) == "table" and bb.Get then return bb.Get(z) end
        return nil
    end
    local bu, gcd = BanditUtils, GetBanditClusterData
    if type(bu) == "table" and bu.GetZombieID and gcd then
        local id = bu.GetZombieID(z)
        local gmd = gcd(id)
        if type(gmd) == "table" then return gmd[id] end
    end
    return nil
end

-- Bandit? SP: z:getVariableBoolean("Bandit") (Bandits client/BanditZombie.lua:74); Server: Gehirn im Cluster (wie isBanditZ).
local function isBandit(z, light)
    if type(light) == "table" then return light.isBandit == true end
    if B.IsSP() then return z:getVariableBoolean("Bandit") == true end
    return brainOf(z, nil) ~= nil
end

-- Werte fuer B.FoeIsTarget (nur lesen). z:isAlive(): Bandits server/BanditSave.lua:52; z:isFakeDead(): Vanilla
-- client/DebugUIs/DebugContextMenu.lua:556; z:isOnKillDone(): Bandits client/BanditUpdate.lua:1679; z:getVehicle() / z:isUnderVehicle():
-- Bandits client/BanditMenu.lua:163 / :162; BanditCompatibility.IsReanimatedForGrappleOnly(z): Bandits shared/BanditCompatibility.lua:187
-- (gerufen client/BanditZombie.lua:118; nur SP wie B.ZedNear); z:getModData().tcUid (NPC-Crew-Marke am Koerper): getModData am Zombie
-- Bandits server/BanditSave.lua:52 (Server), shared/BanditBrain.lua:4 (SP) -- nur LESEN. Gehirn-Felder wie die gespielte Regel
-- NCBearTest shared/NCBearFight.lua:271-293 und Bandits shared/Bandit.lua:607-612 (Bandit.IsHostile).
local function facts(z, bandit, light)
    local f = { alive = z:isAlive(), bandit = bandit }
    if not f.alive then return f end
    f.fakeDead = z:isFakeDead()
    f.killDone = z:isOnKillDone()
    f.inCar = z:getVehicle() ~= nil or z:isUnderVehicle()
    local bc = BanditCompatibility
    if B.IsSP() and type(bc) == "table" and bc.IsReanimatedForGrappleOnly then f.grapple = bc.IsReanimatedForGrappleOnly(z) == true end
    local md = z:getModData()
    if md ~= nil then f.tcUid = md.tcUid end
    if bandit then
        local brain = brainOf(z, light)
        if type(brain) ~= "table" then return f end
        f.recruited, f.npcNeutral, f.npcUid = brain.recruited, brain.npcNeutral, brain.npcUid
        f.fallback = brain.programFallback
        local prog = brain.program
        if type(prog) == "table" then f.program = prog.name end
        f.loyal, f.stance, f.downed = brain.loyal, brain.npcStance, brain.downed
        f.hostile, f.hostileP = brain.hostile, brain.hostileP
    end
    return f
end

-- ---------------------------------------------------------------------------
-- Kandidaten je Baer (Nachbesserung F2 B2; vorher EIN Rahmen um alle Baeren mit den ersten 64 Treffern -- bei zwei weit getrennten Baeren
-- oder einer Horde im Rahmen blieb der Zombie direkt am Baeren unentdeckt). Rahmen aller Baeren +- r nur als billiger Vorfilter, dann der
-- KREIS um jeden Baeren (gleiche Ebene; wie B.ZedNear, server/BanditsNPCBearWorld.lua anyNear) und je Baer die NAECHSTEN foeCandZ Zombies
-- (innerhalb fightRadius) und getrennt die naechsten foeCandB Banditen (innerhalb fightBanditRadius) -- kein globaler Deckel mehr, der
-- naechste Gegner fehlt nie. Quellen: SP mit Bandits die Lua-Tabellen BanditZombie.CacheLightZ / CacheLightB + BanditZombie.
-- GetInstanceById(id) (Bandits client/BanditZombie.lua:12, :16, :176-186; prueft Identitaet und Welt), sonst getCell():getZombieList()
-- :size() :get(i) (Bandits server/BanditSave.lua:15-18; rollender Anfang, hoechstens foeScanMax). getX/getY/getZ am Zombie: Bandits
-- client/BanditZombie.lua:69-71. Rueckgabe per[i] = { z = { e, ... }, b = { e, ... } } je Punkt i, e = { c = Kandidat, d = Abstand },
-- Kandidat c = { z, x, y, zl, light, bandit } (je Zombie EINMAL, auch wenn er bei zwei Baeren steht).
-- ---------------------------------------------------------------------------
-- In eine nach Abstand sortierte Liste einsortieren, hoechstens cap Eintraege (der weiteste faellt hinten heraus).
local function sortIn(t, e, cap)
    local n = #t
    if n >= cap and e.d >= t[n].d then return end
    t[n + 1] = e
    local i = n + 1
    while i > 1 and t[i - 1].d > e.d do
        t[i], t[i - 1] = t[i - 1], t[i]
        i = i - 1
    end
    if #t > cap then t[#t] = nil end
end

-- Einen Zombie / Banditen an (x, y, zl) den Baeren zuordnen, in deren Kreis er steht. Bandit? erst, wenn er in einem Kreis steht (isBandit).
local function take(per, points, rz, rb, z, x, y, zl, light)
    local c = nil
    local capZ = math.floor(cfg("foeCandZ", 24))
    local capB = math.floor(cfg("foeCandB", 8))
    local rr = rz
    if rb > rr then rr = rb end
    for i = 1, #points do
        local p = points[i]
        if math.floor(zl) == p.z then
            local dx, dy = x - p.x, y - p.y
            local d2 = dx * dx + dy * dy
            if d2 <= rr * rr then
                if c == nil then c = { z = z, x = x, y = y, zl = zl, light = light, bandit = isBandit(z, light) } end
                local d = math.sqrt(d2)
                if c.bandit then
                    if d <= rb then sortIn(per[i].b, { c = c, d = d }, capB) end
                elseif d <= rz then
                    sortIn(per[i].z, { c = c, d = d }, capZ)
                end
            end
        end
    end
end

local function lightCands(per, points, rz, rb, tab, x0, x1, y0, y1, cap)
    local bz = BanditZombie
    local seen = 0
    for id, light in pairs(tab) do
        seen = seen + 1
        if seen > cap then break end
        if type(light) == "table" then
            local lx, ly = num(light.x), num(light.y)
            if lx ~= nil and ly ~= nil and lx >= x0 and lx <= x1 and ly >= y0 and ly <= y1 then
                local z = bz.GetInstanceById(id)
                if z ~= nil then take(per, points, rz, rb, z, lx, ly, num(light.z) or 0, light) end
            end
        end
    end
    return seen
end

local function cands(points, rz, rb)
    local per = {}
    for i = 1, #points do per[i] = { z = {}, b = {} } end
    local r = rz
    if rb > r then r = rb end
    local x0, x1, y0, y1 = points[1].x - r, points[1].x + r, points[1].y - r, points[1].y + r
    for i = 2, #points do
        local p = points[i]
        if p.x - r < x0 then x0 = p.x - r end
        if p.x + r > x1 then x1 = p.x + r end
        if p.y - r < y0 then y0 = p.y - r end
        if p.y + r > y1 then y1 = p.y + r end
    end
    local cap = math.floor(cfg("foeScanMax", 1500))
    local bz = BanditZombie
    if B.IsSP() and type(bz) == "table" and bz.GetInstanceById and type(bz.CacheLightZ) == "table" then
        local n = lightCands(per, points, rz, rb, bz.CacheLightZ, x0, x1, y0, y1, 4 * cap)
        if type(bz.CacheLightB) == "table" then n = n + lightCands(per, points, rz, rb, bz.CacheLightB, x0, x1, y0, y1, 4 * cap) end
        if n > 0 then return per end
    end
    local cell = getCell()
    local list = cell and cell:getZombieList()
    if not list then return per end
    local size = list:size()
    if size <= 0 then
        scanFrom = 0
        return per
    end
    local start = scanFrom
    if start < 0 or start >= size then start = 0 end
    local count = size
    if count > cap then count = cap end
    for k = 0, count - 1 do
        local idx = start + k
        if idx >= size then idx = idx - size end
        local z = list:get(idx)
        if z ~= nil then
            local zx, zy = z:getX(), z:getY()
            if zx >= x0 and zx <= x1 and zy >= y0 and zy <= y1 then take(per, points, rz, rb, z, zx, zy, z:getZ(), nil) end
        end
    end
    local nxt = start + count
    if nxt >= size then nxt = nxt - size end
    scanFrom = nxt
    return per
end

-- Abgelaufene Abklingzeiten raus; ueber 128 -> alles leeren (Deckel).
local function cdClean(ms)
    local keep, n = {}, 0
    for oid, t in pairs(B._fcd) do
        if num(t) ~= nil and t - ms > 0 and t - ms <= 60000 then
            keep[oid] = t
            n = n + 1
        end
    end
    if n > 128 then keep, n = {}, 0 end
    B._fcd, B._fcdN = keep, n
end

-- ---------------------------------------------------------------------------
-- Suche (2.1.1): live = B._fightLive. Ohne force hoechstens je foeScanMs. Ergebnis B._foes[id] (Ziele nach Abstand, <= foeListMax) und
-- B._foeN. Der naechste feindliche Bandit eines Baeren wird in B._zed[id] eingemischt (wenn naeher als der Zombie dort) und setzt B._hot:
-- so sehen Verstecken, Passiv und die Tausch-Sperre Banditen als Gefahr (0.9). Die Lage jedes Baeren kommt frisch vom Koerper
-- (getX/getY am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:575-576). z:getPersistentOutfitID(): Bandits
-- server/BanditServerSpawner.lua:442 (Server), shared/BanditUtils.lua:621.
-- ---------------------------------------------------------------------------
function B.FoeScan(live, ms, force)
    ms = num(ms) or getTimestampMs()          -- Vanilla server/Foraging/forageServer.lua:456
    if not force and B._foeAt ~= nil and ms - B._foeAt >= 0 and ms - B._foeAt < cfg("foeScanMs", 500) then return end
    B._foeAt = ms
    cdClean(ms)
    local out, total = {}, 0
    local points = {}
    local n = type(live) == "table" and #live or 0
    for i = 1, n do
        local e = live[i]
        local rec, a = e.rec, e.a
        local s = B._s[rec.id]
        if rec.st == "tame" and rec.ride == nil and s ~= nil and s.obj == a and a:isExistInTheWorld() and not a:isDead() then
            points[#points + 1] = { id = rec.id, x = a:getX(), y = a:getY(), z = math.floor(a:getZ()) }
        end
    end
    if #points > 0 then
        local rz, rb = cfg("fightRadius", 10), cfg("fightBanditRadius", 12)
        local per = cands(points, rz, rb)
        for i = 1, #points do
            local p = points[i]
            for pass = 1, 2 do
                local q = per[i].z
                if pass == 2 then q = per[i].b end
                for j = 1, #q do
                    local c, d = q[j].c, q[j].d
                    if c.f == nil then c.f = facts(c.z, c.bandit, c.light) end
                    if B.FoeIsTarget(c.f) then
                        local t = out[p.id]
                        if t == nil then
                            t = {}
                            out[p.id] = t
                        end
                        local kind = "z"
                        if c.bandit then kind = "b" end
                        if c.oid == nil then c.oid = c.z:getPersistentOutfitID() end
                        t[#t + 1] = { o = c.z, kind = kind, oid = c.oid, x = c.x, y = c.y, z = c.zl, d = d }
                    end
                end
            end
        end
    end
    local keep = math.floor(cfg("foeListMax", 8))
    for id, t in pairs(out) do
        if #t > 1 then table.sort(t, function(p, q) return p.d < q.d end) end
        while #t > keep do table.remove(t) end
        total = total + #t
        -- Banditen als Gefahr fuer Verstecken / Passiv / Tausch (B._zed, server/BanditsNPCBearGuard.lua)
        local zed = B._zed
        if type(zed) == "table" then
            for j = 1, #t do
                local f = t[j]
                if f.kind == "b" then
                    local cur = zed[id]
                    if cur == nil or (num(cur.d) or 999) > f.d then
                        zed[id] = { x = f.x, y = f.y, d = f.d, at = ms }
                        B._hot = true
                    end
                    break
                end
            end
        end
    end
    B._foes = out
    B._foeN = total
end

-- ---------------------------------------------------------------------------
-- Angriffe der Gegner (2.1.3, 2.1.4). Je Kampf-Takt (100 ms, server/BanditsNPCBearFight.lua).
-- ---------------------------------------------------------------------------

-- Laufende Angriffe auf einen Baeren weg (Tod, Am Boden, Close, Tausch). In der Liste an Ort und Stelle (der Takt haengt an.)
function B.FoeDrop(id)
    if id == nil then return end
    local fa = B._fa
    for i = #fa, 1, -1 do
        if fa[i].id == id then table.remove(fa, i) end
    end
    if B._foes then B._foes[id] = nil end
end

local function clipRunning(o, ms)
    local fa = B._fa
    for i = 1, #fa do
        if fa[i].o == o and ms < fa[i].clipEnd then return true end
    end
    return false
end

local function attackersOn(id, ms)
    local n = 0
    local fa = B._fa
    for i = 1, #fa do
        if fa[i].id == id and ms < fa[i].clipEnd then n = n + 1 end
    end
    return n
end

-- Steht ein Spieler naeher als foePlayerNear am Banditen? Dann kaempft er mit dem Spieler (Bandits' Sache, 2.1.4).
local function playerNear(players, x, y)
    local r = cfg("foePlayerNear", 1.5)
    for i = 1, #players do
        if B.DistXY(players[i].x, players[i].y, x, y) <= r then return true end
    end
    return false
end

-- Trifft der Angriff jetzt noch? Reichweite + 0,25, gleiche Ebene, Zombie steht noch, keine Wand. z:getSquare(): Bandits
-- client/BanditUpdate.lua:1852; animal:getSquare(): Vanilla shared/TimedActions/Animals/ISPetAnimal.lua:6; zSq:isSomethingTo(bSq): Bandits
-- client/BanditUpdate.lua:1855 (die Wand-Frage, mit der Bandits einen Zombie-Biss an einem Banditen zulaesst); z:isProne(): Bandits
-- client/BanditUpdate.lua:275. getZ am Tier: Vanilla shared/Definitions/animal/ButcheringUtil.lua:577.
local function lands(e, rec)
    local o, a = e.o, e.a
    if math.floor(o:getZ()) ~= math.floor(a:getZ()) then return false end
    local bd, sz = B.BodyNow(rec)
    if B.DistXY(o:getX(), o:getY(), a:getX(), a:getY()) > B.FoeReach(e.kind, bd, sz) + 0.25 then return false end
    if e.kind == "z" and o:isProne() then return false end
    local zs, bs = o:getSquare(), a:getSquare()
    if zs ~= nil and bs ~= nil and zs ~= bs and zs:isSomethingTo(bs) then return false end
    return true
end

-- Einen Angriff beginnen: Eintrag, Abklingzeit, Fx an die Clients (Bild am Zombie / Banditen). Treffer-Uhr aus B.CLIPS (B.ClipMs,
-- B.ClipHitMs; shared/BanditsNPCBearFightRules.lua).
local function start(rec, a, f, bd, ms)
    local key = "zbite"
    if f.kind == "b" then key = "smack" end
    local dur = B.ClipMs(key, 0) or 1600
    local hit = B.ClipHitMs(key) or math.floor(dur * 0.3)
    B._fa[#B._fa + 1] = { id = rec.id, a = a, o = f.o, kind = f.kind, oid = f.oid, t0 = ms, hitAt = ms + hit, clipEnd = ms + dur,
                          endAt = ms + dur + 1000 }
    local cd = cfg("zBiteCdMs", 1600)
    if f.kind == "b" then cd = cfg("bSmackCdMs", 2200) end
    if B._fcd[f.oid] == nil then
        if B._fcdN >= 128 then cdClean(ms) end
        B._fcdN = B._fcdN + 1
    end
    B._fcd[f.oid] = ms + cd
    local bx, by = a:getX(), a:getY()
    local fx = { id = rec.id, oid = f.oid, zx = f.o:getX(), zy = f.o:getY(), bx = bx, by = by }
    if f.kind == "z" then
        fx.low = bd ~= "big"
        B.Fx("zbite", fx, bx, by)
    else
        B.Fx("smack", fx, bx, by)
    end
end

-- Neue Angriffe auf einen Baeren aus seiner Gegnerliste (Deckel je Baer, gesamt, Abklingzeit, ein Angriff je Gegner).
local function startOn(rec, a, foes, ms, players)
    local bd, sz = B.BodyNow(rec)
    local maxOn = cfg("foeMaxCub", 2)
    if bd == "big" then maxOn = cfg("foeMaxBig", 4) end
    local on = attackersOn(rec.id, ms)
    local bx, by, bz = a:getX(), a:getY(), math.floor(a:getZ())
    for j = 1, #foes do
        if on >= maxOn or #B._fa >= cfg("foePendMax", 64) then return end
        local f = foes[j]
        local o = f.o
        local cd = num(B._fcd[f.oid])
        if o ~= nil and (cd == nil or cd - ms <= 0) and not clipRunning(o, ms) and o:isAlive() then
            local ox, oy = o:getX(), o:getY()
            if math.floor(o:getZ()) == bz and B.DistXY(ox, oy, bx, by) <= B.FoeReach(f.kind, bd, sz) then
                local go
                if f.kind == "z" then go = not o:isProne() else go = not playerNear(players, ox, oy) end
                if go then
                    start(rec, a, f, bd, ms)
                    on = on + 1
                end
            end
        end
    end
end

-- Je Kampf-Takt: laufende Angriffe zu Ende rechnen (Treffer genau einmal nach der Uhr), dann neue beginnen. Der Treffer bleibt aus, wenn
-- der Gegner zwischen Start und Treffer wegzog, liegt oder eine Wand dazwischen ist (still). B.BearHurt kann den Baeren zu Boden schicken
-- oder schliessen (Tod) -- seine weiteren Eintraege fallen dann ueber die Pruefung heraus. ZombRandFloat(a, b): Vanilla
-- shared/TimedActions/ISApplyBandage.lua:112 (wie Staging server/BanditsNPCBearWorld.lua:176-177).
function B.FoeAttackTick(ms)
    ms = num(ms) or getTimestampMs()
    if B.Opt("BearZombiesAttack") ~= true then
        if #B._fa > 0 then B._fa = {} end
        return
    end
    local reg = B.Reg and B.Reg() or nil
    if not reg then return end
    local old = B._fa
    local keep = {}
    B._fa = keep
    for i = 1, #old do
        local e = old[i]
        local rec = reg.cubs[e.id]
        local s = B._s[e.id]
        local drop = rec == nil or rec.st ~= "tame" or rec.ride ~= nil or rec.down ~= nil or s == nil or s.obj ~= e.a
            or not e.o:isAlive()
        if not drop and not e.done and ms >= e.hitAt then
            e.done = true
            if lands(e, rec) then
                B.BearHurt(rec, e.a, B.FoePts(e.kind, ZombRandFloat(0, 1)), e.kind, e)
                -- am Boden / tot: dieser Eintrag geht mit (die anderen fielen schon ueber B.FoeDrop bzw. fallen unten heraus)
                drop = reg.cubs[e.id] ~= rec or rec.down ~= nil
            end
        end
        if not drop and ms >= e.endAt then drop = true end
        if not drop then keep[#keep + 1] = e end
    end
    local live = B._fightLive
    if type(live) ~= "table" or (B._foeN or 0) <= 0 then return end
    local players = nil
    for k = 1, #live do
        local rec, a = live[k].rec, live[k].a
        local s = B._s[rec.id]
        local foes = B._foes[rec.id]
        if reg.cubs[rec.id] == rec and rec.st == "tame" and rec.down == nil and rec.ride == nil and s ~= nil and s.obj == a
            and type(foes) == "table" and #foes > 0 then
            if players == nil then players = B.Players() end
            startOn(rec, a, foes, ms, players)
        end
    end
end
