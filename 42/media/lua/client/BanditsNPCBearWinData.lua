--
-- NPC Crew -- Baer, Inhalt des Baeren-Fensters (F1, PLAN_F1.md 1.4-1.6, 7.5): welche Baeren dem Spieler gehoeren (U.WinBears) und
-- das fertige Modell eines Baeren (U.WinModel) -- alle Texte, Zahlen, Knopf-Zustaende und Tooltips, die das Fenster zeichnet.
--
-- Rein bis auf U.T (Texte) und B.* (Kern): kein Zeichnen, keine Engine-Abfrage ausser player:getX/getY/getVehicle des uebergebenen
-- Spielers (V:client/Fishing/TensionUI.lua:11, V:client/ISUI/Hutch/ISHutchMenu.lua:8) und -- F2 -- dem besten Verband (U.BestBandage,
-- client/BanditsNPCBearMenu.lua) mit item:getDisplayName() (S:shared/BanditsNPCBearFood.lua B.FoodList). Gebaut wird das Modell nur bei neuer Sicht
-- und hoechstens 1 x je Sekunde (client/ISUI/BanditsNPCBearWindow.lua), nie je Bild. Die festen Texte (Knoepfe, Titel, Zustaende,
-- Hinweise) holt U.T nur einmal je Sitzung (Tabelle ST, gedeckelt durch die feste Zahl der Schluessel).
-- Daten: der Sicht-Eintrag des Kerns (S:server/BanditsNPCBearRegistry.lua viewEntry, S:server/BanditsNPCBearGrow.lua B.GrowView;
-- Felder PLAN_F1.md 5.3: mode pas u ld hide sit cm busy, x* carry dodge fgtB fish nose, dazu B1b-B1e: name owner st x y ride callWait
-- bd sz hp hpMax sta staMax day nst nxt). Fehlt ein Wert, steht "--" bzw. die Zeile faellt weg -- nie geraten (PLAN_F1.md 1.4, 1.5).
-- Was der Spieler sieht, ist nur eine Vorpruefung: entscheiden tut immer der Schreiber (B.Handle; Einzelspieler: dasselbe Programm,
-- Mehrspieler: der Server).
-- F1B (PLAN_F1B.md 3.4, 5.3): die Fusszeile nennt die Tasten, die gelten ("E near your bear", die Fern-Taste, falls gesetzt; Namen aus
-- U.WinKeyName, client/BanditsNPCBearKey.lua); der dritte Schalter "Growth line" (U.AgeOn, client/BanditsNPCBearTags.lua) traegt
-- ageShow = der Baer waechst noch (Sicht mit day UND nst) -- ausgewachsen verschwindet er aus dem Fenster.
-- F2 = B5a (PLAN_F2.md 3.2, 4.7, Nachtrag 11): Zustaende "am Boden" (dn) > "kaempft" (fst fight) > "zieht sich zurueck" / "verschnauft"
-- (fst retreat / rest) nach "ausser Reichweite"; Fusszeile am Boden (Win_HintDown mit dnH); Befehle grau am Boden (Why_Down, Unstuck geht);
-- Knopf "Bandage" bzw. am Boden "Help up" (d.care, kind "mend" / "help"; grau mit Grund wie das Menue: U.MendWhy, client/BanditsNPCBearMenu.lua;
-- bester Verband ueber U.BestBandage -- die einzige Inventar-Frage, im 1-s-Takt); Leben-Tooltip mit Verband (bnd) und Flucht-Schwelle
-- (11.7: Sicht fleeP, N Treffer vor dem Tod, "about %1 health"); Zeilen "Melee damage" (11.2, Sicht mdmg / mdmgB / mdmgM / mdmgS / mdmgF) und "Kills"
-- (11.5, kZ / kB); Schalter "Show damage" (11.1, U.DmgOn, je Spieler); Faehigkeit am Alters-Deckel (11.4: Sicht skCap vom Schreiber)
-- mit "max for its age" und Tooltip. Die "kommt spaeter"-Zeilen von Agilitaet / Leben / Kaempfen sind weg (sie wirken jetzt).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Rich-Text des Vanilla-Tooltips (ISToolTip -> ISRichTextPanel): Kopfzeile in der Titelfarbe, danach weiss, Zeilen ueber " <LINE> ".
-- Formen: " <LINE> <RGB:1,0,0> " V:client/ISUI/ISWorldObjectContextMenu.lua:376, " <LINE> " V:client/ISUI/ISGarmentUI.lua:136.
-- Nie "<" oder ">" in UI.json (Uebernahme-Regel): die Marken stehen nur hier.
local TIP_HEAD = " <RGB:1,0.7,0.3> "
local TIP_BODY = " <LINE> <RGB:1,1,1> "
local TIP_LINE = " <LINE> "

local CMDS = { "follow", "stay", "sit", "roam", "come", "unstuck" }
U.WIN_CMDS = CMDS

-- Faehigkeiten in der Reihenfolge von B.SKILLS (S:shared/BanditsNPCBearStats.lua:110). Jeder Schluessel ausgeschrieben.
-- later = ehrlicher Satz, wo die Faehigkeit noch nicht (ganz) wirkt (PLAN_F1.md 1.5). F2: Agilitaet, Leben und Kaempfen wirken jetzt
-- (Ausweichen, eingesteckte und ausgeteilte Treffer) -- ihre Saetze Win_LaterFight / Win_LaterGrow sind weg (PLAN_F2.md 2.7).
local SKILL_ROWS = {
    { key = "agi", name = "UI_BN_Bear_Win_Sk_Agi", tip = "UI_BN_Bear_Win_SkTip_Agi", from = "UI_BN_Bear_Win_SkFrom_Agi" },
    { key = "vit", name = "UI_BN_Bear_Win_Sk_Vit", tip = "UI_BN_Bear_Win_SkTip_Vit", from = "UI_BN_Bear_Win_SkFrom_Vit" },
    { key = "con", name = "UI_BN_Bear_Win_Sk_Con", tip = "UI_BN_Bear_Win_SkTip_Con", from = "UI_BN_Bear_Win_SkFrom_Con" },
    { key = "fgt", name = "UI_BN_Bear_Win_Sk_Fgt", tip = "UI_BN_Bear_Win_SkTip_Fgt", from = "UI_BN_Bear_Win_SkFrom_Fgt" },
    { key = "fsh", name = "UI_BN_Bear_Win_Sk_Fsh", tip = "UI_BN_Bear_Win_SkTip_Fsh", from = "UI_BN_Bear_Win_SkFrom_Fsh",
        later = "UI_BN_Bear_Win_LaterFish" },
    { key = "nos", name = "UI_BN_Bear_Win_Sk_Nos", tip = "UI_BN_Bear_Win_SkTip_Nos", from = "UI_BN_Bear_Win_SkFrom_Nos",
        later = "UI_BN_Bear_Win_LaterNose" },
}
local SKILL_FIELD = { agi = "xAgi", vit = "xVit", con = "xCon", fgt = "xFgt", fsh = "xFsh", nos = "xNos" }

-- Zustand -> Text und Farbe (PLAN_F1.md 1.4, Farben 1.3)
local STATE = {
    missing = { "UI_BN_Bear_Win_St_Missing", "stMissing" }, ride = { "UI_BN_Bear_Win_St_Ride", "stRide" },
    away = { "UI_BN_Bear_Win_St_Away", "stAway" }, hide = { "UI_BN_Bear_Win_St_Hide", "stHide" },
    come = { "UI_BN_Bear_Win_St_Come", "stCome" }, follow = { "UI_BN_Bear_Win_St_Follow", "stFollow" },
    stay = { "UI_BN_Bear_Win_St_Stay", "stStay" }, sit = { "UI_BN_Bear_Win_St_Sit", "stSit" },
    roam = { "UI_BN_Bear_Win_St_Roam", "stRoam" },
    -- F2 (PLAN_F2.md 3.2)
    down = { "UI_BN_Bear_Win_St_Down", "stDown" }, fight = { "UI_BN_Bear_Win_St_Fight", "stFight" },
    retreat = { "UI_BN_Bear_Win_St_Retreat", "stBack" }, rest = { "UI_BN_Bear_Win_St_Rest", "stBack" },
}
local STATE_ORDER = { "missing", "ride", "away", "down", "fight", "retreat", "rest", "hide", "come", "follow", "stay", "sit", "roam" }
-- F2 (11.4): Tooltip-Satz je Wachstums-Stufe am Alters-Deckel (ausgeschrieben; ausgewachsen gibt es keinen Deckel unter 10)
local STAGE_IDX = { cub = 1, half = 2, strong = 3, adult = 4 }
local CAP_TIP = { "UI_BN_Bear_Win_SkAgeTip_Cub", "UI_BN_Bear_Win_SkAgeTip_Half", "UI_BN_Bear_Win_SkAgeTip_Strong" }
local DIR_KEY = { N = "UI_BN_Bear_Dir_N", NE = "UI_BN_Bear_Dir_NE", E = "UI_BN_Bear_Dir_E", SE = "UI_BN_Bear_Dir_SE",
    S = "UI_BN_Bear_Dir_S", SW = "UI_BN_Bear_Dir_SW", W = "UI_BN_Bear_Dir_W", NW = "UI_BN_Bear_Dir_NW" }
local BTN_KEY = { follow = "UI_BN_Bear_Win_Follow", stay = "UI_BN_Bear_Win_Stay", sit = "UI_BN_Bear_Win_Sit",
    roam = "UI_BN_Bear_Win_Roam", come = "UI_BN_Bear_Win_Come", unstuck = "UI_BN_Bear_Win_Unstuck" }

local ST = nil      -- feste Texte dieser Sitzung (einmal ueber U.T geholt)

local function statics()
    if ST ~= nil then return ST end
    local s = {}
    s.bodyCub = U.T("UI_BN_Bear_Win_BodyCub")
    s.bodyBig = U.T("UI_BN_Bear_Win_BodyBear")
    s.grown = U.T("UI_BN_Bear_Win_Grown")
    s.here = U.T("UI_BN_Bear_Win_Here")
    s.none = U.T("UI_BN_Bear_Win_None")
    s.rename = U.T("UI_BN_Bear_Win_Rename")
    s.tCond, s.tSkills, s.tOrders = U.T("UI_BN_Bear_Win_Cond"), U.T("UI_BN_Bear_Win_Skills"), U.T("UI_BN_Bear_Win_Orders")
    s.tHealth, s.tStamina, s.tCarry = U.T("UI_BN_Bear_Win_Health"), U.T("UI_BN_Bear_Win_Stamina"), U.T("UI_BN_Bear_Win_Carry")
    s.tLater = U.T("UI_BN_Bear_Win_Later")
    s.needs = { U.T("UI_BN_Bear_Win_Hunger"), U.T("UI_BN_Bear_Win_Thirst"), U.T("UI_BN_Bear_Win_Tired"), U.T("UI_BN_Bear_Win_Trust") }
    s.tipHealth = TIP_HEAD .. s.tHealth .. TIP_BODY .. U.T("UI_BN_Bear_Win_HealthTip")
    s.tipStamina = TIP_HEAD .. s.tStamina .. TIP_BODY .. U.T("UI_BN_Bear_Win_StaminaTip")
    s.tipCarry = TIP_HEAD .. s.tCarry .. TIP_BODY .. U.T("UI_BN_Bear_Win_CarryTip")
    s.tipLater = TIP_HEAD .. s.tLater .. TIP_BODY .. U.T("UI_BN_Bear_Win_LaterTip")
    s.state = {}
    for i = 1, #STATE_ORDER do
        local k = STATE_ORDER[i]
        s.state[k] = U.T(STATE[k][1])
    end
    s.btn = {}
    for i = 1, #CMDS do s.btn[CMDS[i]] = U.T(BTN_KEY[CMDS[i]]) end
    s.passive, s.tag = U.T("UI_BN_Bear_Win_Passive"), U.T("UI_BN_Bear_Win_Tag")
    s.tipStay, s.tipSit = U.T("UI_BN_Bear_Win_StayTip"), U.T("UI_BN_Bear_Win_SitTip")
    s.tipFollow, s.tipCome = U.T("UI_BN_Bear_Menu_FollowTip"), U.T("UI_BN_Bear_Win_ComeTip")
    s.tipPassive, s.tipTag = U.T("UI_BN_Bear_Win_PassiveTip"), U.T("UI_BN_Bear_Win_TagTip")
    s.tagOffAll, s.active = U.T("UI_BN_Bear_Win_TagOffAll"), U.T("UI_BN_Bear_Win_Active")
    -- F1B: Wachstums-Schalter (Text, Tooltip, Hinweis auf den Hauptschalter TagAge in Optionen -> Mods)
    s.growth, s.tipGrowth = U.T("UI_BN_Bear_Win_Growth"), U.T("UI_BN_Bear_Win_GrowthTip")
    s.growthOffAll = U.T("UI_BN_Bear_Win_GrowthOffAll")
    s.whyCar, s.whyFar = U.T("UI_BN_Bear_Why_InCar"), U.T("UI_BN_Bear_Why_Far")
    s.hintMissing, s.hintRide, s.hintAway = U.T("UI_BN_Bear_Win_HintMissing"), U.T("UI_BN_Bear_Win_HintRide"),
        U.T("UI_BN_Bear_Win_HintAway")
    s.hintEsc = U.T("UI_BN_Bear_Win_HintEsc")
    s.skName, s.skFrom, s.skLater = {}, {}, {}
    for i = 1, #SKILL_ROWS do
        local r = SKILL_ROWS[i]
        s.skName[i] = U.T(r.name)
        s.skFrom[i] = U.T(r.from)
        if r.later then s.skLater[i] = U.T(r.later) end
    end
    s.skTop = U.T("UI_BN_Bear_Win_SkTop")
    s.max = U.T("UI_BN_Bear_Win_Max")
    -- F2: Verband / Aufhelfen, Show damage, Melee damage, Kills, Alters-Deckel, Flucht
    s.bandage, s.helpUp = U.T("UI_BN_Bear_Win_Bandage"), U.T("UI_BN_Bear_Win_HelpUp")
    s.tipBandage, s.tipHelpUp = U.T("UI_BN_Bear_Win_BandageTip"), U.T("UI_BN_Bear_Win_HelpUpTip")
    s.showDmg, s.tipShowDmg = U.T("UI_BN_Bear_Win_ShowDmg"), U.T("UI_BN_Bear_Win_ShowDmgTip")
    s.tMelee, s.meleeTip, s.meleeCub = U.T("UI_BN_Bear_Win_Melee"), U.T("UI_BN_Bear_Win_MeleeTip"), U.T("UI_BN_Bear_Win_MeleeCub")
    s.tKills, s.killsTip = U.T("UI_BN_Bear_Win_Kills"), U.T("UI_BN_Bear_Win_KillsTip")
    s.ageMax = U.T("UI_BN_Bear_Win_SkAgeMax")
    s.fledNever = U.T("UI_BN_Bear_Win_FledNever")
    -- Breiteste Texte fuer das Legen des Fensters (Breite waechst nur, wenn ein Text nicht passt, PLAN_F1.md 1.1)
    s.wideVal = U.T("UI_BN_Bear_Win_Count", 888, 888)
    s.wideCarry = U.T("UI_BN_Bear_Win_CarryVal", 888)
    s.wideLv = U.T("UI_BN_Bear_Win_Lv", 10)
    s.widePct = U.T("UI_BN_Bear_Win_Pct", 100)
    s.wideUnstuck = U.T("UI_BN_Bear_Win_UnstuckWait", "9:59")
    s.wideDist = U.T("UI_BN_Bear_Win_LastSeen", 888, U.T("UI_BN_Bear_Dir_NW"))
    s.wideDist2 = U.T("UI_BN_Bear_Win_Dist", 888, U.T("UI_BN_Bear_Dir_NW"))
    s.wideMelee = U.T("UI_BN_Bear_Win_MeleeVal", 888)                     -- F2 (11.2)
    s.wideKills = U.T("UI_BN_Bear_Win_KillsVal", 8888, 888)               -- F2 (11.5)
    ST = s
    return s
end
U.WinStatics = statics

local function isNum(v)
    return type(v) == "number" and v == v
end

local function clamp(v, lo, hi)
    if v < lo then return lo end
    if v > hi then return hi end
    return v
end

-- Sandbox-Zahl ueber den Kern (B.Opt klemmt und faellt selbst auf die Vorgabe zurueck); fehlt der Kern: def.
local function optNum(name, def)
    local v = nil
    if B.Opt then v = tonumber(B.Opt(name)) end
    if v == nil then return def end
    return v
end

local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- Modus nach der Regel des Kerns (B.ModeOf, F1: follow / stay / sit / roam; nil und Unsinn = stay). Fehlt der Kern: dieselbe Regel.
local function modeOf(v)
    if B.ModeOf then return B.ModeOf(v) end
    local m = v.mode
    if m == "follow" or m == "sit" or m == "roam" then return m end
    return "stay"
end

-- Prozent als ganze Zahl oder "?" (fehlt der Wert in der Sicht, wird nichts geraten).
local function pctOf(v)
    if not isNum(v) then return "?" end
    return math.floor(v + 0.5)
end

-- Eigener Spieler-Schluessel: aus der Sicht (B.View.me.key, S:server/BanditsNPCBearRegistry.lua B.SlotsOf), sonst ueber den Kern.
local function myKey()
    local me = B.View and B.View.me
    if type(me) == "table" and me.key ~= nil then return me.key end
    local p = getSpecificPlayer(0)                      -- V:client/Farming/CFarmingSystem.lua:45
    if p and B.PlayerKey then return B.PlayerKey(p) end
    return nil
end

local function byId(a, b)
    if type(a.id) == type(b.id) then return a.id < b.id end
    return tostring(a.id) < tostring(b.id)
end

-- ---------------------------------------------------------------------------
-- U.WinBears(): eigene Eintraege der Sicht (gezaehmt oder vermisst), nach Kennung sortiert. Eigen = Besitzer ist mein Schluessel --
-- im Einzelspieler auch der feste Einzelspieler-Schluessel (wie S:client/ISUI/BanditsNPCBearHud.lua describeTag). Die Frische der
-- Sicht (U.Fresh) prueft der Aufrufer.
-- ---------------------------------------------------------------------------
function U.WinBears()
    local out = {}
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return out end
    local key = myKey()
    local sp = B.IsSP ~= nil and B.IsSP()
    for _, c in pairs(cubs) do
        if type(c) == "table" and c.id ~= nil and (c.st == "tame" or c.st == "missing") and c.owner ~= nil
            and (c.owner == key or (sp and c.owner == B.SP_KEY)) then
            out[#out + 1] = c
        end
    end
    if #out > 1 then table.sort(out, byId) end
    return out
end

-- U.WinMine(v): gehoert dieser Sicht-Eintrag mir (jeder Zustand, auch das Junge im Zaehmen)? Fuer die Taste (Nachbesserung F1 A2,
-- client/BanditsNPCBearKey.lua): an einem FREMDEN Baeren bleibt Vanillas Tier-Radial.
function U.WinMine(v)
    if type(v) ~= "table" or v.owner == nil then return false end
    if v.owner == myKey() then return true end
    return B.IsSP ~= nil and B.IsSP() and v.owner == B.SP_KEY
end

-- Rest der Call-Abklingzeit in ms (0 = bereit). Die Sicht traegt den Rest in Sekunden (callWait, nur fuer den Besitzer) zum
-- Zeitpunkt ihres Baus; abgezogen wird die Zeit seit ihrer Ankunft (U.viewAt) -- wie S:client/BanditsNPCBearMenu.lua callWaitMinutes.
local function callWaitMs(v, nowMs)
    local left = tonumber(v.callWait)
    if left == nil or left <= 0 then return 0 end
    local ms = left * 1000
    local at = U.viewAt
    if type(at) == "number" and type(nowMs) == "number" and nowMs >= at then ms = ms - (nowMs - at) end
    if ms <= 0 then return 0 end
    return ms
end

-- "m:ss" aus ms (aufgerundet auf ganze Sekunden). string.format("%d"): S:shared/BanditsNPCBear.lua argText.
local function clock(ms)
    local s = math.ceil(ms / 1000)
    local m = math.floor(s / 60)
    s = s - m * 60
    local ss = string.format("%d", s)
    if s < 10 then ss = "0" .. ss end
    return string.format("%d", m) .. ":" .. ss
end

-- Knopf-Eintrag (PLAN_F1.md 1.6): grau mit Grund (why) vor aktiv; Tooltip = Kopf (Knopftext) + Grund bzw. Erklaerung (+ "aktueller
-- Befehl").
local function cmdBtn(label, active, why, tip)
    local e = { label = label, state = "normal" }
    if why then
        e.state = "off"
        e.tip = TIP_HEAD .. label .. TIP_BODY .. why
        return e
    end
    if active then e.state = "active" end
    local t = TIP_HEAD .. label .. TIP_BODY .. (tip or "")
    if active then t = t .. TIP_LINE .. statics().active end
    e.tip = t
    return e
end

local function firstOf(a, b, c, d, e)
    if a then return a end
    if b then return b end
    if c then return c end
    if d then return d end
    if e then return e end
    return nil
end

-- F2: ganze Stunden fuer einen Text, mindestens 1 (5,2 -> 5; 0,4 -> 1) -- wie die Vorpruefung im Menue (client/BanditsNPCBearMenu.lua).
local function hoursOf(h)
    local n = math.floor(tonumber(h) or 0)
    if n < 1 then n = 1 end
    return n
end

-- F2 (11.1 / 11.2): Schaden in der Einheit von CombatText = Zombie-Leben x 100 (client/BanditsNPCBearFx.lua Kopf). Die Sicht traegt
-- Zombie-Leben wie das Ereignis "hit" (schnittstelle_aenderungen.md "F2 OBERFLAECHE"); ein Wert ueber 20 ist schon x 100 (ein Treffer ist
-- hoechstens 1,8 x 1,7 x 3 = 9,2 Zombie-Leben) und bleibt. nil, wenn nichts da ist.
local function units100(x)
    if not isNum(x) or x <= 0 then return nil end
    if x > 20 then return x end
    return x * 100
end

-- Zahl fuer die Anzeige: ab 10 ganz, darunter eine Nachkommastelle (wie die schwebenden Zahlen). string.format: S:shared/BanditsNPCBear.lua, V:client/ISUI/ISDebugAvatarUI.lua:224.
local function fmt100(v)
    if v >= 10 then return string.format("%d", math.floor(v + 0.5)) end
    return string.format("%.1f", v)
end

-- F2 (11.4): Alters-Deckel der Faehigkeiten fuer diesen Eintrag. Der Schreiber rechnet ihn (B.SkillCapLv, S:shared/BanditsNPCBearFightRules.lua
-- -- dieselbe Zahl, ueber die B.SkillAdd keine Erfahrung gutschreibt) und schickt ihn als Sicht-Feld skCap, nur wenn er unter 10 liegt
-- (Sandbox BearSkillAgeCap aus oder ausgewachsen: fehlt). Rueckgabe: Deckel und Index der Wachstums-Stufe aus der Sicht stg (fuer den
-- Tooltip-Satz) -- oder 10, nil. Das Fenster rechnet nichts nach: keine zweite Wahrheit.
local function ageCap(v)
    local cap = tonumber(v.skCap)
    if cap == nil or cap >= 10 then return 10, nil end
    return cap, STAGE_IDX[v.stg]
end

-- F2 (11.7): Flucht-Schwelle. Die Sicht traegt sie fertig in Lebenspunkten (fleeP, B.FleeHp des Kerns mit den Gegnern von gerade,
-- S:server/BanditsNPCBearFight.lua B.FightView; fehlt = er flieht nie); N = Sandbox BearFleeHits.
local function fleeLine(v, s)
    local n = math.floor(optNum("BearFleeHits", 3) + 0.5)
    if n <= 0 or not isNum(v.fleeP) or v.fleeP <= 0 then return s.fledNever end
    return U.T("UI_BN_Bear_Win_Fled", math.floor(v.fleeP + 0.5), n)
end

-- F2 (11.2): Zeile "Melee damage": Hieb je Treffer als Hauptzahl, im Tooltip jeder freigeschaltete Angriff, Anteil aus der Groesse,
-- Kaempfen-Bonus, Sandbox-Prozent. Junges: "--" mit "A cub does not fight." Die Zahlen rechnet der Kern (B.MeleeDamage, dieselbe Rechnung
-- wie der Kampf); fehlen sie, "--".
local function meleeRow(v, s)
    local head = TIP_HEAD .. s.tMelee .. TIP_BODY
    local e = { label = s.tMelee, val = s.none, tip = head .. s.meleeTip }
    if v.bd ~= "big" then
        e.tip = head .. s.meleeCub
        return e
    end
    local main = units100(v.mdmg)
    if main == nil then return e end
    e.val = U.T("UI_BN_Bear_Win_MeleeVal", fmt100(main))
    local t = e.tip .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeSwipe", fmt100(main))
    local bite = units100(v.mdmgB)
    if bite then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeBite", fmt100(bite)) end
    local maul = units100(v.mdmgM)
    if maul then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeMaul", fmt100(maul)) end
    if isNum(v.mdmgS) then
        local pct = v.mdmgS
        if pct <= 1.5 then pct = pct * 100 end                  -- Anteil 0..1 -> Prozent eines ausgewachsenen Baeren
        t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeSize", math.floor(pct + 0.5))
    end
    if isNum(v.mdmgF) then
        local lv = "?"
        if B.SkillProgress then
            local L = B.SkillProgress(v, "fgt")                 -- Mehrfachrueckgabe: erst ins Local (CLAUDE.md Abschnitt 5)
            lv = math.floor(tonumber(L) or 0)
        end
        t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeFgt", lv, math.floor(v.mdmgF + 0.5))
    end
    local dp = math.floor(optNum("BearDamagePercent", 100) + 0.5)
    if dp ~= 100 then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleePct", dp) end
    e.tip = t
    return e
end

-- F2 (11.5): Zeile "Kills" -- Zombies und Banditen, die DIESER Baer selbst erledigt hat (der Schreiber zaehlt). Junges ohne Zaehler: "--".
local function killsRow(v, s)
    local e = { label = s.tKills, val = s.none, tip = TIP_HEAD .. s.tKills .. TIP_BODY .. s.killsTip }
    local z, b = tonumber(v.kZ) or 0, tonumber(v.kB) or 0
    if v.bd == "big" or z > 0 or b > 0 then e.val = U.T("UI_BN_Bear_Win_KillsVal", math.floor(z), math.floor(b)) end
    return e
end

-- F2 (PLAN_F2.md 3.2): Knopf in der Pflege-Zelle -- "Help up" am Boden, sonst "Bandage". Grau mit Grund (dieselben Gruende wie das
-- Menue, U.MendWhy). Klick: das Fenster ruft U.HelpAsk / U.MendAsk (hingehen, Zeitaktion; entscheiden tut der Schreiber in complete()).
local function careBtn(v, player, s, whyRide, whyAway)
    if v.dn == true then
        local e = cmdBtn(s.helpUp, false, firstOf(whyRide, whyAway), s.tipHelpUp)
        e.kind = "help"
        return e
    end
    local item = nil
    if U.BestBandage then item = U.BestBandage(player) end
    local why = firstOf(whyRide, whyAway)
    if not why and U.MendWhy then why = U.MendWhy(v, item) end
    if not why and not item then why = U.T("UI_BN_Bear_Why_NoBandage") end
    local tip = s.tipBandage
    if item and not why then
        tip = tip .. TIP_LINE .. U.T("UI_BN_Bear_Menu_BandageTip", item:getDisplayName(), math.floor(optNum("BearBandageHours", 8) + 0.5))
    end
    local e = cmdBtn(s.bandage, false, why, tip)
    e.kind = "mend"
    return e
end

-- Wirkung einer Faehigkeit mit der Zahl von jetzt (PLAN_F1.md 1.5 Tabelle; Zahlen aus der Sicht bzw. Kevins Formeln ENT:221-230).
local function skillEffect(key, v, L)
    if key == "agi" then
        return U.T("UI_BN_Bear_Win_SkTip_Agi", pctOf(v.dodge), math.floor(optNum("BearDodgeMax", 40) + 0.5))
    elseif key == "vit" then
        return U.T("UI_BN_Bear_Win_SkTip_Vit", math.floor(cfgNum("vitPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "con" then
        return U.T("UI_BN_Bear_Win_SkTip_Con", math.floor(cfgNum("conPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "fgt" then
        return U.T("UI_BN_Bear_Win_SkTip_Fgt", pctOf(v.fgtB), math.floor(optNum("BearFightBonusMax", 70) + 0.5))
    elseif key == "fsh" then
        return U.T("UI_BN_Bear_Win_SkTip_Fsh", pctOf(v.fish))
    end
    local nose = "?"
    if isNum(v.nose) then nose = math.floor(v.nose * 10 + 0.5) / 10 end
    return U.T("UI_BN_Bear_Win_SkTip_Nos", nose)
end

-- Faehigkeiten (PLAN_F1.md 1.5): Stufe, Fortschritt, Texte, Tooltip. known = die Sicht ist eine F1-Sicht: B.GrowView schickt ab F1 fuer
-- tame und missing IMMER carry / dodge / fgtB / fish / nose, die Erfahrung x* aber nur, wenn sie > 0 ist (fehlt = 0,
-- S:server/BanditsNPCBearGrow.lua B.GrowView). Traegt die Sicht nichts davon, ist es eine alte Sicht -> "--" statt einer geratenen 0.
local function skillsOf(v, s)
    local known = isNum(v.dodge) or isNum(v.carry)
    for i = 1, #SKILL_ROWS do
        if isNum(v[SKILL_FIELD[SKILL_ROWS[i].key]]) then known = true end
    end
    if not B.SkillProgress then known = false end
    local cap, capK = ageCap(v)
    local out = {}
    for i = 1, #SKILL_ROWS do
        local r = SKILL_ROWS[i]
        local e = { key = r.key, name = s.skName[i], known = known, lv = 0, frac = 0, pct = 0 }
        local head, prog
        if known then
            local L, xpIn, need = B.SkillProgress(v, r.key)
            L = tonumber(L) or 0
            xpIn = tonumber(xpIn) or 0
            need = tonumber(need) or 0
            e.lv = L
            e.lvTxt = U.T("UI_BN_Bear_Win_Lv", L)
            if L >= 10 or need <= 0 then
                e.frac, e.pct, e.pctTxt = 1, 100, s.max
                prog = s.skTop
            else
                e.frac = clamp(xpIn / need, 0, 1)
                e.pct = math.floor(e.frac * 100)
                e.pctTxt = U.T("UI_BN_Bear_Win_Pct", e.pct)
                prog = U.T("UI_BN_Bear_Win_SkProg", math.floor(xpIn), math.floor(need + 0.5), L + 1)
            end
            head = U.T("UI_BN_Bear_Win_SkHead", e.name, L)
        else
            e.lvTxt = s.none
            e.pctTxt = ""
            head = e.name
        end
        local t = TIP_HEAD .. head .. TIP_BODY .. skillEffect(r.key, v, e.lv) .. TIP_LINE .. s.skFrom[i]
        if s.skLater[i] then t = t .. TIP_LINE .. s.skLater[i] end
        -- F2 (11.4): am Alters-Deckel ausgegraut + "max for its age"; der Tooltip nennt Stufe und ungefaehren Tag, ab dem es weitergeht
        if known and cap < 10 and e.lv >= cap then
            e.capped = true
            e.pctTxt = s.ageMax
            local nextDay = "?"
            if isNum(v.day) and isNum(v.nxt) then nextDay = math.floor(v.day + v.nxt) end
            local tk = capK and CAP_TIP[capK]
            if tk then t = t .. TIP_LINE .. U.T(tk, math.floor(cap), nextDay) end
        elseif prog then
            t = t .. TIP_LINE .. prog
        end
        e.tip = t
        out[i] = e
    end
    return out
end

-- Wert-Zeile Leben / Ausdauer (PLAN_F1.md 1.5): "jetzt / hoechst" und Balken aus Prozent (0..100) und Hoechstwert; fehlt einer:
-- "--" ohne Balken (frac nil), nie 0.
local function valueRow(label, pct, most, kind, s)
    local e = { label = label, val = s.none }
    if isNum(pct) and isNum(most) then
        local frac = clamp(pct / 100, 0, 1)
        local mx = math.floor(most + 0.5)
        if mx < 0 then mx = 0 end
        e.now = math.floor(frac * mx + 0.5)
        e.max = mx
        e.frac = frac
        e.val = U.T("UI_BN_Bear_Win_Count", e.now, mx)
        if U.WinRamp then e.r, e.g, e.b = U.WinRamp(kind, frac) end
    end
    return e
end

-- Zustand nach Vorrang (PLAN_F1.md 1.4): vermisst > faehrt mit > ausser Reichweite > versteckt > kommt > Modus.
local function stateOf(v, mode)
    if v.st == "missing" then return "missing" end
    if v.ride == true then return "ride" end
    if v.ld ~= true then return "away" end
    if v.dn == true then return "down" end                      -- F2 (PLAN_F2.md 3.2): am Boden > kaempft > zurueck / verschnauft
    if v.fst == "fight" then return "fight" end
    if v.fst == "retreat" or v.fst == "rest" then return v.fst end
    if v.hide == true then return "hide" end
    if v.cm == true then return "come" end
    return mode
end

-- ---------------------------------------------------------------------------
-- U.WinModel(v, player, nowMs): das fertige Modell eines Baeren (v = Eintrag aus U.WinBears). Neue Tabelle je Aufruf (1 x je Sekunde).
-- ---------------------------------------------------------------------------
function U.WinModel(v, player, nowMs)
    local s = statics()
    local d = { id = v.id, tCond = s.tCond, tSkills = s.tSkills, tOrders = s.tOrders, tLater = s.tLater, needs = s.needs,
        rename = s.rename, wide = s }
    local bd = v.bd
    d.name = U.CubName(v)
    -- Kopf: Koerper und Tag, naechste Stufe (Zahlen aus B.GrowView; fehlen sie, faellt die Zeile weg)
    local body = s.bodyCub
    if bd == "big" then body = s.bodyBig end
    if isNum(v.day) then
        d.sub = U.T("UI_BN_Bear_Win_Sub", body, math.floor(v.day))
    else
        d.sub = body
    end
    if v.nst ~= nil and isNum(v.nxt) then
        local left = math.floor(v.nxt)
        if left < 1 then left = 1 end
        d.next = U.T("UI_BN_Bear_Win_Next", U.StageName(v.nst), left)
    elseif isNum(v.day) then
        d.next = s.grown
    end
    -- Zustand, Chip-Farbe, Fusszeile
    local tame = (v.st == "tame")
    local mode = modeOf(v)
    local st = stateOf(v, mode)
    d.state = st
    d.chipText = s.state[st] or ""
    if U.WinColor then
        d.cr, d.cg, d.cb = U.WinColor(STATE[st][2])
    else
        d.cr, d.cg, d.cb = 1, 1, 1
    end
    if st == "missing" then
        d.footer = s.hintMissing
    elseif st == "ride" then
        d.footer = s.hintRide
    elseif st == "away" then
        d.footer = s.hintAway
    elseif st == "down" then
        -- F2: wie lange er noch liegt, wenn ihm keiner aufhilft (Sicht dnH, Stunden; aufgerundet, mindestens 1)
        local h = math.ceil(tonumber(v.dnH) or 1)
        if h < 1 then h = 1 end
        d.footer = U.T("UI_BN_Bear_Win_HintDown", h)
    else
        -- F1B (PLAN_F1B.md 3.4): welche Tasten gelten. Liegen beide auf derselben Taste, gilt sie als Fern-Taste (oeffnet ueberall).
        local nn, fn = nil, nil
        if U.WinKeyName then nn, fn = U.WinKeyName() end
        if nn and fn and nn == fn then nn = nil end
        if nn and fn then
            d.footer = U.T("UI_BN_Bear_Win_HintBoth", nn, fn)
        elseif nn then
            d.footer = U.T("UI_BN_Bear_Win_HintNear", nn)
        elseif fn then
            d.footer = U.T("UI_BN_Bear_Win_Hint", fn)
        else
            d.footer = s.hintEsc
        end
    end
    -- Abstand: lebende Kopie (U.CubPos, S:client/ISUI/BanditsNPCBearHud.lua), sonst die letzte Stelle der Sicht (ganze Kacheln)
    local px, py = player:getX(), player:getY()         -- V:client/Fishing/TensionUI.lua:11
    local bx, by = nil, nil
    if isNum(v.x) and isNum(v.y) then bx, by = v.x + 0.5, v.y + 0.5 end
    if U.CubPos and v.ride ~= true then
        local lx, ly = U.CubPos(v.id)
        if lx ~= nil then bx, by = lx, ly end
    end
    if bx ~= nil then
        local dist = B.DistXY(px, py, bx, by)
        d.distN = dist
        local dirTxt = U.T(DIR_KEY[B.DirOf(bx - px, by - py)] or "UI_BN_Bear_Dir_N")
        local n = math.floor(dist + 0.5)
        if st == "missing" or st == "away" then
            if n < 1 then n = 1 end
            d.dist = U.T("UI_BN_Bear_Win_LastSeen", n, dirTxt)
        elseif dist < 2 then
            d.dist = s.here
        else
            d.dist = U.T("UI_BN_Bear_Win_Dist", n, dirTxt)
        end
    end
    -- Werte
    d.hp = valueRow(s.tHealth, v.hp, v.hpMax, "hp", s)
    d.sta = valueRow(s.tStamina, v.sta, v.staMax, "sta", s)
    d.carry = { label = s.tCarry, val = s.none }
    if isNum(v.carry) then d.carry.val = U.T("UI_BN_Bear_Win_CarryVal", math.floor(v.carry + 0.5)) end
    -- F2: Leben mit Verband (Zeichen am Wert + Tooltip) und Flucht-Schwelle (nur der grosse Koerper kaempft); Melee damage, Kills
    local hpTip = s.tipHealth
    if isNum(v.bnd) and v.bnd > 0 then
        d.hp.bnd = true
        hpTip = hpTip .. TIP_LINE .. U.T("UI_BN_Bear_Win_Bandaged", hoursOf(v.bnd))
    end
    if bd == "big" then hpTip = hpTip .. TIP_LINE .. fleeLine(v, s) end
    d.melee = meleeRow(v, s)
    d.kills = killsRow(v, s)
    d.tips = { hp = hpTip, sta = s.tipStamina, carry = s.tipCarry, later = s.tipLater, melee = d.melee.tip, kills = d.kills.tip }
    d.skills = skillsOf(v, s)
    -- Befehle (PLAN_F1.md 1.6): Vorpruefung aus der Sicht, entscheiden tut der Schreiber
    local ride = (v.ride == true)
    local gone = (v.st == "missing") or (v.ld ~= true)
    local inCar = player:getVehicle() ~= nil            -- V:client/ISUI/Hutch/ISHutchMenu.lua:8
    local far = (not gone) and d.distN ~= nil and d.distN > optNum("BearFollowMaxDistance", 40)
    local cm = tame and v.cm == true
    local whyRide = ride and U.TB("UI_BN_Bear_Why_Riding", bd)
    local whyAway = gone and U.TB("UI_BN_Bear_Why_OutOfReach", bd)
    local whyCar = inCar and s.whyCar
    local whyFar = far and s.whyFar
    local whyDown = tame and v.dn == true and U.TB("UI_BN_Bear_Why_Down", bd)    -- F2: am Boden nimmt der Schreiber keinen Befehl an
    local act = nil
    if tame then act = mode end
    local radius = math.floor(optNum("BearRoamRadius", 12) + 0.5)
    local b = {}
    b.follow = cmdBtn(s.btn.follow, act == "follow" and not cm, firstOf(whyRide, whyAway, whyDown, whyCar, whyFar), s.tipFollow)
    b.stay = cmdBtn(s.btn.stay, act == "stay", firstOf(whyRide, whyAway, whyDown), s.tipStay)
    b.sit = cmdBtn(s.btn.sit, act == "sit", firstOf(whyRide, whyAway, whyDown), s.tipSit)
    b.roam = cmdBtn(s.btn.roam, act == "roam", firstOf(whyRide, whyAway, whyDown), U.T("UI_BN_Bear_Win_RoamTip", radius))
    b.come = cmdBtn(s.btn.come, cm, firstOf(whyRide, whyAway, whyDown, whyCar, whyFar), s.tipCome)
    -- Unstuck = "Call to me" (B1c): geht auch fuer vermisste und nicht geladene; grau beim Mitfahren, im Fahrzeug, in der Abklingzeit
    local waitMs = callWaitMs(v, nowMs)
    local whyWait = nil
    if waitMs > 0 then
        -- Nachbesserung F1 B6: dieselbe m:ss-Uhr wie auf dem Knopf (nicht "about 4 min" neben "3:12"); das Menue behaelt Why_CallWait
        whyWait = U.TB("UI_BN_Bear_Win_CallWaitClock", bd, clock(waitMs))
    end
    local uLabel = s.btn.unstuck
    if waitMs > 0 then uLabel = U.T("UI_BN_Bear_Win_UnstuckWait", clock(waitMs)) end
    local cool = math.floor(optNum("BearCallCooldownMinutes", 5) + 0.5)
    b.unstuck = cmdBtn(uLabel, false, firstOf(whyRide, whyCar, whyWait), U.TB("UI_BN_Bear_Menu_CallTip", bd, cool))
    d.buttons = b
    d.care = careBtn(v, player, s, whyRide, whyAway)                -- F2: "Bandage" / am Boden "Help up"
    d.ordersInfo = ""
    if act == "roam" then d.ordersInfo = U.T("UI_BN_Bear_Win_RoamInfo", radius) end
    -- Schalter: Passiv (Register, Sicht pas) und Namensschild (je Spieler, client/BanditsNPCBearTags.lua)
    local tagOn = true
    if U.TagOn then tagOn = U.TagOn(v) ~= false end
    local tagTip = TIP_HEAD .. s.tag .. TIP_BODY .. s.tipTag
    if U.Opt and U.Opt("TagShow", true) == false then tagTip = tagTip .. TIP_LINE .. s.tagOffAll end
    -- F1B (PLAN_F1B.md 5.3): Wachstums-Schalter -- an/aus je Baer (U.AgeOn, je Spieler), sichtbar nur, solange er waechst (nst fehlt,
    -- wenn er ausgewachsen ist: S:server/BanditsNPCBearGrow.lua:758, :786-787). TagAge aus (Hauptschalter): Hinweis im Tooltip.
    local ageOn = true
    if U.AgeOn then ageOn = U.AgeOn(v) ~= false end
    local ageTip = TIP_HEAD .. s.growth .. TIP_BODY .. s.tipGrowth
    if U.Opt and U.Opt("TagAge", true) == false then ageTip = ageTip .. TIP_LINE .. s.growthOffAll end
    -- F2 (11.1): Schalter "Show damage" -- je Spieler fuer ALLE seine Baeren (U.DmgOn, client/BanditsNPCBearTags.lua), Vorgabe an
    local dmgOn = true
    if U.DmgOn then dmgOn = U.DmgOn() ~= false end
    d.toggles = { pas = (v.pas == true), tag = tagOn, pasLabel = s.passive, tagLabel = s.tag,
        pasTip = TIP_HEAD .. s.passive .. TIP_BODY .. s.tipPassive, tagTip = tagTip,
        age = ageOn, ageShow = isNum(v.day) and v.nst ~= nil, ageLabel = s.growth, ageTip = ageTip,
        dmg = dmgOn, dmgLabel = s.showDmg, dmgTip = TIP_HEAD .. s.showDmg .. TIP_BODY .. s.tipShowDmg }
    return d
end
