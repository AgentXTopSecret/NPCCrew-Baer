--
-- NPC Crew -- Baer, Anzeige ueber der Welt (B1a, PLAN_ZAEHMEN.md 5.6, 6.8, 7): Zaehm-Balken ueber dem Jungen und das Schild
-- ueber dem eigenen Koederplatz. B1b (PLAN_B1B.md 2): Namensschild ueber jedem gezaehmten Jungen (Zeile 1 Name, Zeile 2 klein
-- der Zustand bzw. bei fremden Jungen der Besitzer); Balken und Schild haengen am selben Anker B.CFG.tagZ dicht ueber dem Kopf.
-- Dazu U.CubsNear (die Jungen mit Objekt in der Naehe, fuer "Futter hinhalten" im Welt-Menue).
-- B1c (PLAN_B1C.md 1.9, 6.4): Anzeige-Optionen je Spieler ueber U.Opt (client/BanditsNPCBearOptions.lua) -- "TagShow" aus blendet
-- die Namensschilder ALLER gezaehmten Baeren aus (der Zaehm-Balken bleibt immer), "TagSize" 100 / 150 / 200 waehlt die Schrift
-- Small / Medium / Large fuer Schild UND Balken (Balken und Abstaende wachsen mit dem Verhaeltnis der Schrifthoehen). Gelesen nur
-- beim Listenbau (hoechstens 1 x je Sekunde). Ein mitfahrendes Junges (Sicht "ride") hat keinen Koerper: kein Suchlauf seinetwegen.
-- U.CubObj / U.CubPos geben anderen Anzeigen (Markierung, Karte) die lebende Client-Kopie aus derselben Tabelle -- ohne eigenen Suchlauf.
--
-- Reine Anzeige: liest nur B.View (die Sicht, die der Schreiber diesem Spieler geschickt hat) und fragt nie den Server.
-- Einzelspieler und Mehrspieler laufen gleich; im Mehrspieler stammen alle Zahlen vom Server. Der dedizierte Server laedt client/ nicht.
--
-- Bauart (Vorbild: ein kleines Element, das weit daneben zeichnet; Vanilla ISButtonPrompt.lua:1244 haelt genauso ein 1 x 1-Element):
--   * EIN ISPanel, 1 x 1 Pixel in der Ecke oben links, angelegt bei OnGameStart. Es bleibt 1 x 1 (ein grosses Element frisst jeden
--     Weltklick) und wird NIE unsichtbar geschaltet (ein unsichtbares Element erreicht prerender nie wieder); Ein/Aus sitzt im
--     Zeichencode. Die drei Maus-Funktionen geben false zurueck.
--   * Die Liste der Balken wird hoechstens einmal je Sekunde neu gebaut (und sofort nach einer neuen Sicht): hoechstens
--     B.CFG.hudMax Junge in B.CFG.hudDist Kacheln, dazu fertige Texte. Die Objektliste der Zelle wird nur durchsucht, wenn ein
--     Junges aus der Sicht noch kein Objekt hat, und dann hoechstens einmal je Sekunde (nach fuenf vergeblichen Laeufen alle 5 s).
--   * Je Bild wird nur aus der fertigen Liste gezeichnet: je Balken zwei Umrechnungen, zwei Rechtecke, ein Rahmen, zwei Texte
--     (jeder mit Schatten); je Namensschild zwei Umrechnungen und zwei Texte (mit Schatten: vier drawTextCentre). Keine Suche,
--     kein getText, keine Tabelle je Bild. Kein Sichtfeld-Test: ein folgendes Junges laeuft HINTER dem Spieler (Plan 2.3).
--   * Bei mehr als einem lokalen Spieler (geteilter Bildschirm) wird nichts gezeichnet.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Die Klasse bleibt ein Local: sie muss nicht global sein (nur Zeitaktionen muessen das).
local Hud = ISPanel:derive("BanditsNPCBearHud")

local LIST_MS = 1000        -- Liste hoechstens so oft neu
local SCAN_FAST_MS = 1000   -- Suchlauf, solange ein Junges ohne Objekt ist
local SCAN_SLOW_MS = 5000   -- ... nach SCAN_FAST_N vergeblichen Laeufen
local SCAN_FAST_N = 5
-- Nach SCAN_SLOW_N vergeblichen Laeufen nur noch je SCAN_IDLE_MS (das eigene Junge steht in der Sicht, ist aber weit weg und
-- nicht geladen). Kommt der Spieler in seine Naehe, schickt der Schreiber eine neue Sicht (Server pushNewSights) und es geht
-- wieder schnell (S.scanMiss = 0 bei jeder neuen Sicht). Nachbesserung B6.
local SCAN_SLOW_N = 17
local SCAN_IDLE_MS = 30000
local FLASH_MS = 5000       -- so lange steht "Gezaehmt!"
local BAR_W = 64
local BAR_H = 7
local BAIT_DIST = 25        -- Kacheln: so nah steht das Schild ueber dem eigenen Koederplatz
local BAIT_Z = 0.3
local TAG_Z = 0.18          -- Rueckfall fuer B.CFG.tagZ (Anker von Balken und Schild ueber dem Boden des Tiers, Plan 2.2)

local panel = nil
local fontH = nil           -- Hoehe UIFont.Small (Zeile 1, Balken-Texte)
local font2 = nil           -- Schrift der kleinen Zeile 2 des Namensschilds: UIFont.NewSmall, wenn sie niedriger ist, sonst Small
local fontH2 = nil

-- B1c: Groessenstufen der Anzeige (U.Opt "TagSize"). Je Stufe: f1/h1 = Schrift und Hoehe von Zeile 1 und den Balken-Texten, f2/h2 =
-- die kleinere Zeile 2 des Schilds, barW/barH/gap = Balkenmasse (Stufe 1 = genau der Stand B1b). Die Hoehe jeder Schrift wird nur
-- einmal geholt, wenn die Stufe zum ersten Mal gebraucht wird. Hoechstens drei Eintraege.
local tiers = {}
local SIZE_MID = 125        -- TagSize unter 125 -> Stufe 1 (Small), unter 175 -> Stufe 2 (Medium), sonst Stufe 3 (Large)
local SIZE_BIG = 175

-- Alles, was die Anzeige sich merkt. Nichts davon wird gespeichert oder gesendet; die Tabellen sind durch die Sicht gedeckelt
-- (hoechstens so viele Kennungen, wie B.View.cubs traegt; verschwundene Kennungen fallen bei jeder neuen Sicht heraus).
local S = {
    dirty = true,   -- neue Sicht: Liste sofort neu
    listAt = 0,     -- ms, letzte Liste
    scanAt = 0,     -- ms, fruehestens naechster Suchlauf
    scanMiss = 0,   -- vergebliche Suchlaeufe in Folge
    list = {},      -- fertige Eintraege fuer den Zeichner
    n = 0,
    bait = nil,     -- fertiger Eintrag fuer das Koeder-Schild
    objs = {},      -- id -> IsoAnimal (nur in dieser Sitzung, jedes Mal gegengeprueft)
    prev = {},      -- id -> letzter gesehener Zustand (fuer "gerade gezaehmt")
    flash = {},     -- id -> ms, bis wann "Gezaehmt!" steht
    tier = nil,     -- B1c: Groessenstufe der aktuellen Liste (tiers[1..3]); nil = noch keine Liste
}

local function reset()
    S.dirty = true
    S.listAt = 0
    S.scanAt = 0
    S.scanMiss = 0
    S.list = {}
    S.n = 0
    S.bait = nil
    S.objs = {}
    S.prev = {}
    S.flash = {}
    S.tier = nil
end

-- Stufe k (1..3) mit Schriften und Massen. Stufe 1 braucht fontH/font2/fontH2 (in prerender einmal geholt).
-- getFontHeight(UIFont.Medium): V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8; getFontHeight(UIFont.Large):
-- V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6.
local function tierOf(k)
    local t = tiers[k]
    if t then return t end
    local h1, f1, h2, f2 = fontH, UIFont.Small, fontH2, font2
    if k == 2 or k == 3 then
        local tm = getTextManager()
        local hMed = tm:getFontHeight(UIFont.Medium)
        if k == 2 then
            f1, h1 = UIFont.Medium, hMed
            f2, h2 = UIFont.Small, fontH
        else
            f1, h1 = UIFont.Large, tm:getFontHeight(UIFont.Large)
            f2, h2 = UIFont.Medium, hMed
        end
        if type(h1) ~= "number" or h1 <= 0 then h1 = fontH end
        if type(h2) ~= "number" or h2 <= 0 then h2 = fontH end
    end
    local ratio = 1
    if k ~= 1 and fontH and fontH > 0 then ratio = h1 / fontH end
    if ratio < 1 then ratio = 1 end
    t = {
        f1 = f1, h1 = h1, f2 = f2, h2 = h2,
        barW = math.floor(BAR_W * ratio + 0.5), barH = math.floor(BAR_H * ratio + 0.5),
        gap = math.floor(4 * ratio + 0.5), gap2 = math.floor(2 * ratio + 0.5),
    }
    tiers[k] = t
    return t
end

-- Gewaehlte Stufe aus der Anzeige-Option (fehlt client/BanditsNPCBearOptions.lua: Vorgabe 100 = Stufe 1).
local function tierWanted()
    local size = 100
    local opt = U.Opt
    if opt then size = tonumber(opt("TagSize", 100)) or 100 end
    if size < SIZE_MID then return 1 end
    if size < SIZE_BIG then return 2 end
    return 3
end

-- Namensschilder zeigen? (fehlt die Options-Datei: ja)
local function tagsWanted()
    local opt = U.Opt
    if not opt then return true end
    return opt("TagShow", true) ~= false
end

-- ---------------------------------------------------------------------------
-- Liste bauen (hoechstens einmal je Sekunde)
-- ---------------------------------------------------------------------------

-- Objekt noch da und lebendig? isExistInTheWorld: client/ISUI/Animal/ISAnimalUI.lua:15; isDead: client/ISUI/Hutch/ISHutchUI.lua:427.
local function alive(a)
    return a ~= nil and a:isExistInTheWorld() and not a:isDead()
end

-- Bekommt dieses Junge eine Anzeige? B1b: jedes Junge der Sicht, das ein Objekt haben kann -- ungezaehmte den Balken, gezaehmte
-- (eigene und fremde) das Namensschild. "missing" hat kein Objekt (Plan 2.1). B1c: ein mitfahrendes Junges ("ride") auch nicht.
local function wanted(c)
    if c.ride == true then return false end
    local st = c.st
    return st == "new" or st == "shy" or st == "fed" or st == "tame"
end

-- Kennungen vergessen, die die Sicht nicht mehr traegt. Erst sammeln, dann loeschen (nie waehrend des Durchlaufs).
local function forget(t, cubs)
    local gone = nil
    for id, _ in pairs(t) do
        if cubs[id] == nil then
            gone = gone or {}
            gone[#gone + 1] = id
        end
    end
    if gone then
        for i = 1, #gone do t[gone[i]] = nil end
    end
end

-- Suchlauf: alle geladenen Jungen einmal ihrem Sicht-Eintrag zuordnen. Die Liste ist eine Kopie der Engine, deshalb selten.
-- getCell():getObjectListForLua(), size(), get(i): Vanilla FenrisScenario.lua:505-507; instanceof(o, "IsoAnimal"):
-- shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29; getAnimalType(): client/ISUI/Animal/ISAnimalUI.lua:65.
local function scan()
    local objects = getCell():getObjectListForLua()
    for i = 0, objects:size() - 1 do
        local o = objects:get(i)
        if instanceof(o, "IsoAnimal") and o:getAnimalType() == B.CUB then
            local v = B.ViewOf(o)
            if v and v.id ~= nil then S.objs[v.id] = o end
        end
    end
end

-- "bereit" oder die Restzeit als Text.
local function waitWord(c, kind, nowH)
    local left = B.WaitLeft(c, kind, nowH)
    if type(left) ~= "number" or left <= 0 then return U.T("UI_BN_Bear_Hud_Ready") end
    return U.WaitText(left)
end

-- Zustand eines gezaehmten Jungen. B.ModeOf ist die Regel des Kerns (shared, Plan 5.3: nil und alles andere = "stay"); fehlt
-- die Kern-Datei, gilt dieselbe Regel hier.
local function modeOf(c)
    local f = B.ModeOf
    if f then return f(c) end
    if c.mode == "follow" then return "follow" end
    return "stay"
end

-- Namensschild (Plan 2.1): Zeile 1 der Name (U.CubName), Zeile 2 beim eigenen Jungen der Zustand, beim fremden der Besitzer.
-- Gerade gezaehmt: Zeile 2 blinkt FLASH_MS lang gruen "Tamed!", danach der Zustand. Eigen ist ein Junges, wenn der Besitzer mein
-- Schluessel ist -- oder im Einzelspieler der feste Einzelspieler-Schluessel (dann gibt es keinen anderen Besitzer). Im
-- Mehrspieler zaehlt "__sp" nie als eigen und erscheint nie als Text (Nachbesserung B1b B8: Junge eines frueheren
-- Einzelspieler-Stands auf einem Server zeigen "belongs to ?").
local function describeTag(e, meKey)
    local c = e.c
    e.tag = true
    e.line1 = U.CubName(c, meKey)
    local own = (c.owner ~= nil) and (c.owner == meKey or (c.owner == B.SP_KEY and B.IsSP ~= nil and B.IsSP()))
    if own then
        e.r, e.g, e.b = 0.96, 0.96, 0.90
        if modeOf(c) == "follow" then
            e.line2 = U.T("UI_BN_Bear_Tag_Follow")
        else
            e.line2 = U.T("UI_BN_Bear_Tag_Stay")
        end
        e.till = S.flash[c.id] or 0
        e.flashLine = U.T("UI_BN_Bear_Hud_Tamed")
    else
        e.r, e.g, e.b = 0.80, 0.88, 1.00
        local who = c.owner
        if who == nil or who == B.SP_KEY then who = "?" end
        e.line2 = U.T("UI_BN_Bear_Tag_Owner", tostring(who))
        e.till = 0
    end
end

-- Die fertigen Texte eines Eintrags (einmal je Liste, nie je Bild).
local function describe(e, meKey, nowH)
    local c = e.c
    if c.st == "tame" then
        describeTag(e, meKey)
        return
    end
    local pct = math.floor(tonumber(c.tame) or 0)
    if pct < 0 then pct = 0 end
    if pct > 100 then pct = 100 end
    local barW = BAR_W
    if S.tier then barW = S.tier.barW end
    e.fill = math.floor(barW * pct / 100)
    local unfed = (c.st == "new" or c.st == "shy")
    e.unfed = unfed
    local line1 = U.T("UI_BN_Bear_Hud_Taming", pct)
    if unfed then line1 = line1 .. " - " .. U.T("UI_BN_Bear_Hud_Shy") end
    e.line1 = line1
    if c.bond ~= nil and c.bond ~= meKey then
        -- an jemand anderen gebunden
        e.line2 = U.T("UI_BN_Bear_Hud_Other", tostring(c.bond))
    elseif unfed then
        -- noch nie gefuettert: Streicheln geht noch nicht, also nur die Futter-Zeile
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH))
    else
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH)) .. "   "
            .. U.T("UI_BN_Bear_Hud_Pet", waitWord(c, "pet", nowH))
    end
end

local function byDist(a, b)
    return a.d2 < b.d2
end

-- Koeder-Schild: nur der eigene Platz (mehr traegt die Sicht nicht), nur in BAIT_DIST Kacheln.
local function baitEntry(view, px, py)
    local bait = view.bait
    if type(bait) ~= "table" or type(bait.x) ~= "number" or type(bait.y) ~= "number" then return nil end
    local dx = bait.x + 0.5 - px
    local dy = bait.y + 0.5 - py
    if dx * dx + dy * dy > BAIT_DIST * BAIT_DIST then return nil end
    local kindKey = "UI_BN_Bear_Bait_Fish"
    if bait.kind == "honey" then kindKey = "UI_BN_Bear_Bait_Honey" end
    local e = { x = bait.x + 0.5, y = bait.y + 0.5, z = (tonumber(bait.z) or 0) + BAIT_Z }
    e.line1 = U.T("UI_BN_Bear_Hud_Bait", U.T(kindKey))
    if bait.ready == true then
        e.line2 = U.T("UI_BN_Bear_Hud_BaitReady")
    else
        e.line2 = U.T("UI_BN_Bear_Hud_BaitNight", tonumber(bait.nights) or 0, tonumber(bait.max) or 0)
    end
    return e
end

local function rebuild(now)
    local wasDirty = S.dirty
    S.dirty = false
    S.listAt = now
    S.n = 0
    S.bait = nil
    -- Nur eine Sicht von DIESEM Spiel zeigen (B.UI.Fresh, client/BanditsNPCBearClient.lua).
    if not U.Fresh or not U.Fresh() then return end
    local view = B.View
    local cubs = view.cubs
    if type(cubs) ~= "table" then return end

    if wasDirty then
        forget(S.objs, cubs)
        forget(S.prev, cubs)
        forget(S.flash, cubs)
        S.scanMiss = 0
    end

    -- 1. Zustandswechsel merken; fehlt einem gewuenschten Jungen das Objekt?
    local need = false
    local any = false
    for id, c in pairs(cubs) do
        any = true
        local was = S.prev[id]
        if c.st == "tame" and (was == "fed" or was == "shy" or was == "new") then
            S.flash[id] = now + FLASH_MS
        end
        S.prev[id] = c.st
        if wanted(c) and not alive(S.objs[id]) then
            S.objs[id] = nil
            need = true
        end
    end
    -- Die Sicht kennt weder ein Junges noch einen Koederplatz: nichts zu tun, kein Engine-Aufruf.
    if not any and view.bait == nil then return end

    local player = getSpecificPlayer(0)                 -- client/Farming/CFarmingSystem.lua:45
    if not player then return end
    local px = player:getX()                            -- client/Fishing/TensionUI.lua:11
    local py = player:getY()

    -- 2. Suchlauf, nur bei Bedarf und gedrosselt (now < scanAt - SCAN_IDLE_MS: die Uhr lief rueckwaerts).
    if need and (now >= S.scanAt or now < S.scanAt - SCAN_IDLE_MS) then
        scan()
        local still = false
        for id, c in pairs(cubs) do
            if wanted(c) and S.objs[id] == nil then still = true end
        end
        if still then
            S.scanMiss = S.scanMiss + 1
            local wait = SCAN_IDLE_MS
            if S.scanMiss <= SCAN_FAST_N then
                wait = SCAN_FAST_MS
            elseif S.scanMiss <= SCAN_SLOW_N then
                wait = SCAN_SLOW_MS
            end
            S.scanAt = now + wait
        else
            S.scanMiss = 0
            S.scanAt = now + SCAN_FAST_MS
        end
    end

    -- 3. Eintraege: die naechsten hudMax in hudDist Kacheln. B1c: Anzeige-Optionen einmal je Liste lesen (U.Opt, je Wert
    -- hoechstens 1 x je Sekunde); "Namensschilder aus" laesst gezaehmte Junge weg (sie zaehlen dann auch nicht gegen hudMax).
    S.tier = tierOf(tierWanted())
    local showTags = tagsWanted()
    local cfg = B.CFG
    local reach = cfg.hudDist or 20
    local max = cfg.hudMax or 6
    local found = {}
    for id, c in pairs(cubs) do
        local a = S.objs[id]
        if a ~= nil and wanted(c) and (showTags or c.st ~= "tame") and alive(a) then
            local dx = a:getX() - px                    -- client/TimedActions/ISContextualActions.lua:100
            local dy = a:getY() - py
            local d2 = dx * dx + dy * dy
            if d2 <= reach * reach then
                found[#found + 1] = { a = a, c = c, d2 = d2 }
            end
        end
    end
    if #found > 1 then table.sort(found, byDist) end
    local n = #found
    if n > max then n = max end
    if n > 0 then
        local meKey = view.me and view.me.key
        local nowH = B.Now()
        for i = 1, n do
            describe(found[i], meKey, nowH)
        end
    end
    S.list = found
    S.n = n

    -- 4. Koeder-Schild
    S.bait = baitEntry(view, px, py)
end

-- ---------------------------------------------------------------------------
-- Zeichnen (je Bild, nur aus der fertigen Liste)
-- ---------------------------------------------------------------------------

-- Text mit Schatten, sonst ist heller Text auf Sand oder Beton unlesbar. drawTextCentre(text, x, y, r, g, b, a, Schrift):
-- client/ISUI/ISUIElement.lua:1280 (UIFont.Small); mit UIFont.NewSmall: client/Foraging/ISSearchManager.lua:148.
local function text(self, str, x, y, r, g, b, a, font)
    self:drawTextCentre(str, x + 1, y + 1, 0, 0, 0, 0.7, font)
    self:drawTextCentre(str, x, y, r, g, b, a, font)
end

-- Namensschild: der Block waechst vom Anker nach OBEN -- Zeile 2 (klein, blasser) sitzt mit ihrer Unterkante am Anker, Zeile 1
-- 1 px darueber (Plan 2.2). Gerade gezaehmt: Zeile 2 blinkt gruen "Tamed!" (450 von 700 ms an), danach der Zustand.
-- B1c: Schriften und Hoehen aus der Groessenstufe t (Stufe 1 = Small / NewSmall wie B1b). drawTextCentre mit UIFont.Medium:
-- V:client/ISUI/ISFitnessUI.lua:204; mit UIFont.Large: V:client/Chat/ISAlert.lua:35.
local function drawTag(self, e, sx, sy, now, t)
    local y2 = sy - t.h2
    text(self, e.line1, sx, y2 - 1 - t.h1, e.r, e.g, e.b, 0.95, t.f1)
    if now < e.till then
        if (now % 700) < 450 then
            text(self, e.flashLine, sx, y2, 0.55, 1.0, 0.55, 1.0, t.f2)
        end
    else
        text(self, e.line2, sx, y2, 0.78, 0.78, 0.74, 0.80, t.f2)
    end
end

-- Zaehm-Balken wie B1a (Zeile 2 unten am Anker, darueber der Balken, darueber Zeile 1); nur der Anker ist neu.
-- B1c: Balkenbreite, -hoehe und Abstaende aus der Groessenstufe t (Stufe 1: 64 x 7, 4 und 2 px wie B1b).
local function drawBar(self, e, sx, sy, t)
    local fh = t.h1
    local bw, bh = t.barW, t.barH
    local bx = sx - bw / 2
    local by = sy - fh - bh - t.gap
    text(self, e.line1, sx, by - fh - t.gap2, 0.96, 0.96, 0.90, 0.95, t.f1)
    self:drawRect(bx - 1, by - 1, bw + 2, bh + 2, 0.65, 0, 0, 0)
    if e.fill > 0 then
        if e.unfed then
            self:drawRect(bx, by, e.fill, bh, 0.95, 0.95, 0.70, 0.25)
        else
            self:drawRect(bx, by, e.fill, bh, 0.95, 0.45, 0.85, 0.35)
        end
    end
    self:drawRectBorder(bx - 1, by - 1, bw + 2, bh + 2, 0.9, 0.85, 0.85, 0.80)
    text(self, e.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80, t.f1)
end

-- Das Element liegt bei 0,0 und wird nie verschoben: seine Koordinaten sind Bildschirm-Koordinaten.
-- isoToScreenX/Y(Spielernummer, x, y, z): client/Fishing/TensionUI.lua:11-12 (erstes Argument eine Zahl).
-- drawRect / drawRectBorder (x, y, w, h, a, r, g, b): client/ISUI/ISUIElement.lua:1191 / :1219.
-- Anker fuer Balken UND Schild: a:getZ() + B.CFG.tagZ (Plan 2.2; je Bild gelesen, damit ein geaenderter Stellwert sofort wirkt).
local function draw(self, now)
    local cfg = B.CFG
    local lift = tonumber(cfg.tagZ) or TAG_Z
    local small = UIFont.Small
    local t = S.tier or tierOf(1)
    for i = 1, S.n do
        local e = S.list[i]
        local a = e.a
        if a:isExistInTheWorld() then
            local x = a:getX()
            local y = a:getY()
            local z = a:getZ() + lift
            local sx = math.floor(isoToScreenX(0, x, y, z))
            local sy = math.floor(isoToScreenY(0, x, y, z))
            if e.tag then
                drawTag(self, e, sx, sy, now, t)
            else
                drawBar(self, e, sx, sy, t)
            end
        end
    end
    local bait = S.bait
    if bait then
        local fh = fontH
        local sx = math.floor(isoToScreenX(0, bait.x, bait.y, bait.z))
        local sy = math.floor(isoToScreenY(0, bait.x, bait.y, bait.z))
        text(self, bait.line1, sx, sy - fh * 2 - 2, 0.98, 0.85, 0.45, 0.95, small)
        text(self, bait.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80, small)
    end
end

-- Ein Panel sagt zu jedem Klick ja, wenn man es laesst: ausdruecklich nein.
function Hud:onMouseDown() return false end
function Hud:onMouseUp() return false end
function Hud:onRightMouseDown() return false end

function Hud:prerender()
    ISPanel.prerender(self)
    if not B.View or not B.CFG or not B.T then return end
    -- Geteilter Bildschirm: lieber nichts als auf der falschen Haelfte. getNumActivePlayers: client/Fishing/FishingHandler.lua:6.
    if getNumActivePlayers() > 1 then return end
    local now = getTimestampMs()                        -- client/Foraging/ISBaseIcon.lua:485
    if S.dirty or now - S.listAt >= LIST_MS or now < S.listAt then
        if not fontH then
            -- Schrifthoehen einmal holen. getFontHeight(UIFont.Small): client/ISUI/Animal/ISAnimalUI.lua:4;
            -- getFontHeight(UIFont.NewSmall): client/Entity/ISUI/Controls/ISWidgetTitleHeader.lua:4. Statisch entschieden
            -- (Nachbesserung B1b A3): in JEDER Vanilla-Sprache laden "font NewSmall" und "font Small" dieselbe Datei
            -- (media/fonts/EN/fonts.txt:75-79 und :93-97, ebenso CN, CH, JP, KO, PL, RU, TH) -- Zeile 2 ist also gleich gross, nur
            -- blasser. Der Vergleich bleibt (schadet nicht, greift, falls ein Schriftsatz NewSmall einmal kleiner macht); kleiner
            -- zeichnen ginge nur mit drawTextZoomed, das Vanilla nirgends aufruft (braucht Kevins Wort).
            local tm = getTextManager()
            fontH = tm:getFontHeight(UIFont.Small)
            local hNew = tm:getFontHeight(UIFont.NewSmall)
            if type(hNew) == "number" and hNew > 0 and hNew < fontH then
                font2 = UIFont.NewSmall
                fontH2 = hNew
            else
                font2 = UIFont.Small
                fontH2 = fontH
            end
        end
        rebuild(now)
    end
    if S.n > 0 or S.bait then
        draw(self, now)
    end
end

-- ---------------------------------------------------------------------------
-- Junge mit Objekt in der Naehe (B1b, Plan 3.2 / 5.4): fuer "Futter hinhalten" im Welt-Menue. Quelle sind die Objekte, die der
-- Balken ohnehin kennt (S.objs) -- kein Suchlauf, kein Server-Weg. Liste { id, c, a, d }, naechste zuerst. Laeuft nur auf
-- Rechtsklick. getX/getY am Tier: client/TimedActions/ISContextualActions.lua:100; isExistInTheWorld/isDead siehe alive().
-- ---------------------------------------------------------------------------
local function byD(a, b)
    return a.d < b.d
end

function U.CubsNear(playerObj, radius)
    local out = {}
    if not playerObj or not U.Fresh or not U.Fresh() then return out end
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return out end
    local r = tonumber(radius) or 0
    if r <= 0 then return out end
    local px = playerObj:getX()                         -- client/Fishing/TensionUI.lua:11
    local py = playerObj:getY()
    for id, c in pairs(cubs) do
        local a = S.objs[id]
        if a ~= nil and alive(a) then
            local dx = a:getX() - px
            local dy = a:getY() - py
            local d = math.sqrt(dx * dx + dy * dy)
            if d <= r then
                out[#out + 1] = { id = id, c = c, a = a, d = d }
            end
        end
    end
    if #out > 1 then table.sort(out, byD) end
    return out
end

-- ---------------------------------------------------------------------------
-- B1c (PLAN_B1C.md 6.4): die lebende Client-Kopie eines Jungen fuer Markierung und Karte -- aus derselben Tabelle wie der
-- Balken (S.objs), ohne eigenen Suchlauf. Nur auf Abruf (Markierung je 400 ms, Karte je 500 ms), nie je Bild.
-- U.CubObj(id): das Objekt, wenn es lebt UND sein Sicht-Eintrag noch diese Kennung ist (B.ViewOf: Spiegel bzw. OnlineID), sonst
-- nil -- schuetzt davor, einer anderen Figur zu folgen, falls die Engine ein Objekt weiterreicht.
-- U.CubPos(id): x, y, z dieser Kopie oder nil. getX/getY/getZ am Tier: client/TimedActions/ISContextualActions.lua:100.
-- ---------------------------------------------------------------------------
function U.CubObj(id)
    if id == nil then return nil end
    local a = S.objs[id]
    if a == nil or not alive(a) then return nil end
    local v = B.ViewOf and B.ViewOf(a)
    if not v or v.id ~= id then return nil end
    return a
end

function U.CubPos(id)
    local a = U.CubObj(id)
    if a == nil then return nil end
    return a:getX(), a:getY(), a:getZ()
end

-- ---------------------------------------------------------------------------
-- Naht zum Kern (Plan 6.2.4): B.ApplySync ruft das nach jeder neuen Sicht.
-- ---------------------------------------------------------------------------
function B.OnView()
    S.dirty = true
    if U.NoteSync then U.NoteSync() end
end

-- Je Spielstart ein frisches Element. Ein altes (Hauptmenue und neu laden) wird vorher abgemeldet und vergessen:
-- removeFromUIManager ist Vanillas eigenes Lua (client/ISUI/ISUIElement.lua:1373) und tut nichts, wenn es schon weg ist.
local function onGameStart()
    if panel then panel:removeFromUIManager() end
    reset()
    panel = Hud:new(0, 0, 1, 1)
    panel:initialise()                                  -- client/ISUI/Animal/ISAnimalContextMenu.lua:746
    panel:noBackground()                                -- client/ISUI/ISPanel.lua:9
    panel:addToUIManager()                              -- client/ISUI/Animal/ISAnimalContextMenu.lua:747
end

Events.OnGameStart.Add(onGameStart)                     -- client/Chat/ISChat.lua:1186
