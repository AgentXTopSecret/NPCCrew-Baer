--
-- NPC Crew -- Baer, Kampf-Ereignisse auf der Baeren-Seite (F2 = B5a, PLAN_F2.md 0.1, 3.2, 4.4, 4.6; Nachtrag 11.1 "Show damage").
--
-- Der Schreiber (Einzelspieler: dasselbe Programm; Mehrspieler: der Server) entscheidet alles, was zaehlt, und schickt je Ereignis EIN
-- Kampf-Ereignis { k = Art, ... } (B.Fx, shared/BanditsNPCBear.lua; im Mehrspieler Befehl "Fx", client/BanditsNPCBearClient.lua). B.OnFx
-- (shared/BanditsNPCBearFoe.lua, KERN) macht die Zombie-Seite und ruft danach U.FightFx -- diese Datei zeigt NUR: Clip am Baeren
-- (U.PoseAct, client/BanditsNPCBearPose.lua), Stimme, Blut, "DODGE" / "down" ueber dem Baeren und die Schadenszahl ueber dem getroffenen
-- Zombie/Banditen. Sie entscheidet nichts, setzt nie einen Wert und schickt nichts zurueck (kein Client -> Server-Befehl).
--   act    U.PoseAct(id, act)                               growl  playBreedSound("growl" .. n)      (nur grosser Koerper)
--   huff   playBreedSound("huffsoft" / "huff") (nur gross) hurt   dodge -> "DODGE"; sonst Blut + Schmerzlaut (gross, je Baer <= 1 je 800 ms)
--   down   "down" ueber dem Baeren                           dead   playBreedSound("death") (gross)
--   hit    Schadenszahl ueber dem Zombie/Banditen -- nur fuer den EIGENEN Baeren (Besitz ueber die Sicht, nie aus dem Ereignis allein,
--          U.WinMine), nur mit Schalter "Show damage" an (client/BanditsNPCBearTags.lua, je Spieler, Vorgabe an)
-- Fehlt die lebende Kopie des Baeren (zu weit, nicht geladen): Baeren-Seite still (PLAN_F2.md 4.4).
--
-- Schadenszahl (11.1): EINHEIT wie Kevins Mod CombatText (nur gelesen, nichts kopiert): sie zeigt das Leben eines Zombies x 100
-- (CombatText 42/media/lua/client/CombatText/CombatText.lua:20 getHealth() * 100, ISHealthBarManager.lua:162-167); dmg im Ereignis ist
-- Zombie-Leben (B.FightDamage, shared/BanditsNPCBearFightRules.lua) -> hier x 100, mit "-" davor wie CombatText (dort Vorgabe
-- DamageNumberAsAbsolute = false). Doppelte Zahlen: CombatText verfolgt nur Zombies, die ein SPIELER mit einer Waffe trifft
-- (Events.OnWeaponHitCharacter, CombatText.lua:31-35, :162) oder die brennen (:71); dann zeigt es jede Lebens-Aenderung dieses Zombies
-- (ISHealthBarManager.lua:653-674) -- also auch unseren Treffer, aber nur an einem Zombie, den der Spieler kurz vorher selbst geschlagen hat.
-- Darum Vorgabe AN; die seltene Doppelzahl steht als Frage im Bericht. Ohne CombatText geht alles gleich.
--
-- Zeichnen: je Bild NUR aus der fertigen Liste (keine Suche, kein getText): U.FloatDraw(el, now) wird vom Anzeige-Element gerufen
-- (client/ISUI/BanditsNPCBearHud.lua prerender). Deckel: 16 Zeilen ueber Baeren, 24 Schadenszahlen (die aelteste faellt heraus).
-- K1 (Lauf baer-k1, PLAN_K1.md 3): "DODGE" / "down" ueber dem Baeren heben sich mit derselben Pose wie das Schild (U.PoseLift(id, now),
-- client/BanditsNPCBearPose.lua; die Kennung steht dafuer im Eintrag) -- kein Engine-Aufruf.
-- Engine-Aufrufe (Fundstelle):
--   animal:playBreedSound(Text): V:shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19 ("pain"), :41 ("death"); die Stimmen der
--     Rasse des grossen Koerpers (pain, death, huff, huffsoft, growl1-3) traegt shared/BanditsNPCBearDefs.lua (KERN)
--   addBloodSplat(Kachel, Zahl): V:client/DebugUIs/Scenarios/Trailer2Scenario.lua:148; animal:getSquare(): V:client/ISUI/Animal/
--     ISAnimalContextMenu.lua:90; animal:getX()/getY()/getZ(): V:client/TimedActions/ISContextualActions.lua:100
--   animal:isExistInTheWorld(): V:client/ISUI/Animal/ISAnimalUI.lua:15; getTimestampMs(): V:client/Foraging/ISBaseIcon.lua:485
--   isoToScreenX/Y(0, x, y, z): V:client/Fishing/TensionUI.lua:11-12; el:drawTextCentre(Text, x, y, r, g, b, a, Schrift):
--     V:client/ISUI/ISUIElement.lua:1280 (UIFont.Medium V:client/ISUI/ISFitnessUI.lua:204, UIFont.Large V:client/Chat/ISAlert.lua:35)
--   getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45; player:getZ(): V:client/Fishing/TensionUI.lua:11
-- Laeuft im Einzelspieler und auf jedem MP-Client (der dedizierte Server laedt client/ nicht). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local PAIN_MS = 800             -- Schmerzlaut je Baer hoechstens so oft (PLAN_F2.md 4.4)
local PAIN_KEEP = 32            -- Deckel der Drossel-Tabelle (sonst geleert)
local TAG_MS = 1200             -- "DODGE" / "down" steht so lange (PLAN_F2.md 3.2)
local TAG_RISE = 12             -- ... und steigt so viele Pixel
local TAG_UP = 40               -- Abstand ueber dem Anker des Namensschilds (Pixel, damit er ueber dem Schild steht)
local TAG_MAX = 16              -- Deckel Zeilen ueber Baeren
local DMG_MS = 1500             -- Schadenszahl steht so lange (11.1 "steigt ~1,5 s und blendet aus")
local DMG_RISE = 30             -- ... und steigt so viele Pixel
local DMG_MAX = 24              -- Deckel Schadenszahlen (11.1)
local DMG_LIFT = 0.8            -- Kopfhoehe eines Zombies ueber seinen Fuessen (Ebenen); der Baer traegt sein Schild bei tagZ x Groesse
local FADE_AT = 0.5             -- ab diesem Anteil der Zeit blendet eine Zeile aus
local BLOOD_N = 3               -- Blutflecken je Treffer am Baeren (PLAN_F2.md 4.4)

-- Farben (r, g, b): DODGE hell, down rot, Schadenszahl Hauptziel Honig-Orange, Umwerfen Honig-Gelb, Nebenziel blasses Rot
local C_DODGE = { 0.95, 0.95, 0.85 }
local C_DOWN = { 0.95, 0.35, 0.30 }
local C_MAIN = { 1.00, 0.62, 0.18 }
local C_KNOCK = { 1.00, 0.80, 0.30 }
local C_SIDE = { 1.00, 0.45, 0.40 }

local painAt = {}               -- id -> ms des letzten Schmerzlauts
local painN = 0
local tags = {}                 -- Zeilen ueber Baeren { obj, lift, text, c, t0 }
local dmgs = {}                 -- Schadenszahlen { x, y, z, text, c, t0, big }

-- Sicht-Eintrag einer Kennung (oder nil). B.View gehoert dem Kern (nur lesen).
local function viewOf(id)
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" or id == nil then return nil end
    local v = cubs[id]
    if type(v) ~= "table" then return nil end
    return v
end

-- Grosser Koerper? Aus der Sicht; fehlt sie, aus dem Ereignis (big), sonst nein.
local function isBig(id, t)
    local v = viewOf(id)
    if v then return v.bd == "big" end
    return type(t) == "table" and t.big == true
end

local function obj(id)
    if not U.CubObj or id == nil then return nil end
    return U.CubObj(id)
end

-- Schrift der schwebenden Zeilen: eine Stufe ueber der des Namensschilds (Option TagSize 100 / 150 / 200, client/BanditsNPCBearOptions.lua).
local function floatFont()
    local size = 100
    if U.Opt then size = tonumber(U.Opt("TagSize", 100)) or 100 end
    if size < 125 then return UIFont.Medium end
    return UIFont.Large
end

-- Liste auf ihren Deckel kuerzen (die aeltesten fallen vorn heraus).
local function cap(list, max)
    while #list > max do table.remove(list, 1) end
end

-- ---------------------------------------------------------------------------
-- U.HudFloat(id, what): "dodge" / "down" ueber dem Baeren (PLAN_F2.md 3.2, 4.6). "dodge" nur mit Option TagDodge (Vorgabe an).
-- ---------------------------------------------------------------------------
function U.HudFloat(id, what)
    local text, c
    if what == "dodge" then
        if U.Opt and U.Opt("TagDodge", true) == false then return false end
        text, c = U.T("UI_BN_Bear_Tag_Dodge"), C_DODGE
    elseif what == "down" then
        text, c = U.T("UI_BN_Bear_Tag_Down"), C_DOWN
    else
        return false
    end
    local a = obj(id)
    if a == nil then return false end
    local lift = 0.18
    if U.TagLift then lift = U.TagLift(viewOf(id)) end
    tags[#tags + 1] = { obj = a, id = id, lift = lift, text = text, c = c, t0 = getTimestampMs(), font = floatFont() }   -- K1: id fuer U.PoseLift
    cap(tags, TAG_MAX)
    return true
end

-- Zahl -> Text in der Einheit von CombatText (Zombie-Leben x 100, siehe Kopf): ab 10 ganze Zahl, darunter eine Nachkommastelle; "-" davor.
-- string.format("%d"): S:shared/BanditsNPCBear.lua argText; "%.1f": V:client/ISUI/ISDebugAvatarUI.lua:224.
-- fix1 (R4): die Nachkommastelle mit dem Dezimalzeichen der Sprache (B.DecText, wie jede Zahl in den Texten -- "-8,5" im Deutschen).
local function dmgText(dmg)
    local v = (tonumber(dmg) or 0) * 100
    if v ~= v or v <= 0 then return nil end
    if v >= 10 then return "-" .. string.format("%d", math.floor(v + 0.5)) end
    local txt = "-" .. string.format("%.1f", v)
    if B.DecText then txt = B.DecText(txt) end
    return txt
end
U.DmgText = dmgText

-- ---------------------------------------------------------------------------
-- U.DmgFloat(oid, zx, zy, zz, dmg, knock, main) (Nachtrag 11.1): Schadenszahl ueber dem getroffenen Zombie/Banditen. Lage aus dem Ereignis
-- (zx, zy); Ebene zz = die des Baeren (der Schreiber trifft nur auf gleicher Ebene, PLAN_F2.md 2.2.4). Prueft NICHT, wem der Baer gehoert --
-- das tut U.FightFx vorher.
-- ---------------------------------------------------------------------------
function U.DmgFloat(oid, zx, zy, zz, dmg, knock, main)
    local x, y, z = tonumber(zx), tonumber(zy), tonumber(zz)
    if x == nil or y == nil or z == nil then return false end
    local text = dmgText(dmg)
    if text == nil then return false end
    local c = C_SIDE
    if knock ~= nil and knock ~= false then
        c = C_KNOCK
    elseif main == true then
        c = C_MAIN
    end
    dmgs[#dmgs + 1] = { x = x, y = y, z = math.floor(z) + DMG_LIFT, text = text, c = c, t0 = getTimestampMs(), font = floatFont() }
    cap(dmgs, DMG_MAX)
    return true
end

-- Ebene fuer eine Schadenszahl: die der lebenden Baeren-Kopie, sonst die des Spielers.
local function levelFor(id)
    local a = obj(id)
    if a ~= nil then return a:getZ() end
    local p = getSpecificPlayer(0)
    if p then return p:getZ() end
    return nil
end

-- Gehoert der Baer dieses Ereignisses mir? NUR ueber die Sicht (U.WinMine, client/BanditsNPCBearWinData.lua), gezaehmt.
local function mine(id)
    local v = viewOf(id)
    if v == nil or v.st ~= "tame" then return false end
    return U.WinMine ~= nil and U.WinMine(v) == true
end

local function dmgOn()
    if U.DmgOn then return U.DmgOn() ~= false end
    return true
end

-- Schmerzlaut gedrosselt (je Baer hoechstens je PAIN_MS); Tabelle <= PAIN_KEEP (dann geleert).
local function pain(id, a, now)
    local last = painAt[id]
    if last ~= nil and now - last >= 0 and now - last < PAIN_MS then return end
    if last == nil then
        painN = painN + 1
        if painN > PAIN_KEEP then
            painAt = {}
            painN = 1
        end
    end
    painAt[id] = now
    a:playBreedSound("pain")                                     -- ISKillAnimalInInventory.lua:19
end

-- ---------------------------------------------------------------------------
-- U.FightFx(kind, t): Baeren-Seite eines Kampf-Ereignisses (PLAN_F2.md 4.4, Spalte OBER). Gerufen von B.OnFx (KERN) auf SP und MP-Client.
-- ---------------------------------------------------------------------------
function U.FightFx(kind, t)
    if type(t) ~= "table" or type(kind) ~= "string" then return end
    local id = t.id
    if kind == "act" then
        if U.PoseAct and type(t.act) == "string" then U.PoseAct(id, t.act) end
        return
    end
    if kind == "hit" then
        if dmgOn() and mine(id) then
            -- Ebene: zz traegt der Schreiber mit (die des Baeren, server/BanditsNPCBearFight.lua); fehlt sie, die der Kopie / des Spielers
            U.DmgFloat(t.oid, t.zx, t.zy, tonumber(t.zz) or levelFor(id), t.dmg, t.knock, t.main == true)
        end
        return
    end
    if kind == "down" then
        U.HudFloat(id, "down")
        return
    end
    if kind == "hurt" and t.dodge == true then
        if mine(id) then U.HudFloat(id, "dodge") end       -- Nachbesserung F2 B8: nur ueber dem EIGENEN Baeren (Option TagDodge)
        return
    end
    local a = obj(id)
    if a == nil then return end                                   -- keine lebende Kopie: Baeren-Seite still
    local big = isBig(id, t)
    if kind == "hurt" then
        local sq = a:getSquare()                                  -- ISAnimalContextMenu.lua:90
        if sq then addBloodSplat(sq, BLOOD_N) end                 -- Trailer2Scenario.lua:148
        if big then pain(id, a, getTimestampMs()) end
    elseif kind == "growl" then
        if big then
            local n = math.floor(tonumber(t.n) or 1)
            if n < 1 then n = 1 end
            if n > 3 then n = 3 end
            a:playBreedSound("growl" .. string.format("%d", n))   -- ISKillAnimalInInventory.lua:19 (Rasse: growl1-3)
        end
    elseif kind == "huff" then
        if big then
            if t.soft == true then a:playBreedSound("huffsoft") else a:playBreedSound("huff") end
        end
    elseif kind == "dead" then
        if big then a:playBreedSound("death") end                  -- ISKillAnimalInInventory.lua:41
    end
end

-- ---------------------------------------------------------------------------
-- Zeichnen je Bild (aus client/ISUI/BanditsNPCBearHud.lua prerender, das Element liegt bei 0,0: Bildschirm-Koordinaten). Nur Rechnen und
-- je Zeile zwei drawTextCentre (Schatten + Farbe); abgelaufene Zeilen fallen heraus (in-place, keine neue Tabelle).
-- ---------------------------------------------------------------------------
local function alpha(frac)
    if frac <= FADE_AT then return 1 end
    local a = 1 - (frac - FADE_AT) / (1 - FADE_AT)
    if a < 0 then return 0 end
    return a
end

local function drawLine(el, s, sx, sy, c, a, font)
    el:drawTextCentre(s, sx + 1, sy + 1, 0, 0, 0, 0.7 * a, font)        -- ISUIElement.lua:1280
    el:drawTextCentre(s, sx, sy, c[1], c[2], c[3], a, font)
end

function U.FloatDraw(el, now)
    if #tags == 0 and #dmgs == 0 then return end
    local keep = 0
    for i = 1, #tags do
        local e = tags[i]
        local dt = now - e.t0
        local a = e.obj
        if dt >= 0 and dt < TAG_MS and a:isExistInTheWorld() then          -- ISAnimalUI.lua:15
            keep = keep + 1
            tags[keep] = e
            local frac = dt / TAG_MS
            -- K1 (PLAN_K1.md 3): derselbe Pose-Faktor wie das Schild (U.PoseLift, client/BanditsNPCBearPose.lua), sonst 1
            local pk = 1
            if U.PoseLift then pk = tonumber(U.PoseLift(e.id, now)) or 1 end
            local x, y, z = a:getX(), a:getY(), a:getZ() + e.lift * pk      -- ISContextualActions.lua:100
            local sx = math.floor(isoToScreenX(0, x, y, z))                 -- TensionUI.lua:11
            local sy = math.floor(isoToScreenY(0, x, y, z)) - TAG_UP - math.floor(TAG_RISE * frac)
            drawLine(el, e.text, sx, sy, e.c, alpha(frac), e.font)
        end
    end
    for i = #tags, keep + 1, -1 do tags[i] = nil end
    keep = 0
    for i = 1, #dmgs do
        local e = dmgs[i]
        local dt = now - e.t0
        if dt >= 0 and dt < DMG_MS then
            keep = keep + 1
            dmgs[keep] = e
            local frac = dt / DMG_MS
            local sx = math.floor(isoToScreenX(0, e.x, e.y, e.z))
            local sy = math.floor(isoToScreenY(0, e.x, e.y, e.z)) - math.floor(DMG_RISE * frac)
            drawLine(el, e.text, sx, sy, e.c, alpha(frac), e.font)
        end
    end
    for i = #dmgs, keep + 1, -1 do dmgs[i] = nil end
end

-- Zum Pruefen: Zahl der schwebenden Zeilen ueber Baeren und der Schadenszahlen.
function U.FloatCount()
    return #tags, #dmgs
end

-- Je Spielstart leer (Objekte eines alten Spielstands nie anfassen). Events.OnGameStart: V:client/Chat/ISChat.lua:1186.
local function onGameStart()
    painAt, painN = {}, 0
    tags, dmgs = {}, {}
end

Events.OnGameStart.Add(onGameStart)
