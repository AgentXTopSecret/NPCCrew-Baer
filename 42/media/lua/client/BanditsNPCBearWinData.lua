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
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 8.1; Kevin 12.11.2026: "ja fuer spieler als knopf"): Knopf "Look: <Name>" (d.look,
-- Zelle 3 der vierten Reihe). Name = Text des Eintrags B.LookFor(Koerper, Sicht lk) aus der Tabelle des Kerns B.LOOKS (keine eigene
-- Liste hier); Angebot = Eintraege des Koerpers ohne hide, deren Art definiert ist (B.LookHas). Grau mit Grund (Vorpruefung aus der
-- Sicht: mitfahrend, ausser Reichweite, am Boden, im Fahrzeug, Kampf, beschaeftigt, Zombies nah, Wachs-Tausch wartet lkg, gemeinsame Uhr
-- mit Unstuck, nur ein Aussehen); die Uhr steht wie bei Unstuck als "Look  m:ss" am Knopf. Der Klick oeffnet im Fenster ein kleines
-- Menue (d.look.picks); entscheiden tut der Schreiber (B.HandleLook). Fehlt B.LOOKS (Kern ohne Aussehen), gibt es keinen Knopf.
-- Sandbox-Kuerzung (Kevin 12.11.2026, PLAN_AUSSEHEN.md 9.3): Abstand fuer Folgen, Frei-Radius, Ausweichen / Kampf-Bonus auf Stufe 10,
-- Verband-Stunden und die Unstuck-Abklingzeit sind feste Werte des Kerns (B.CFG followMaxDist, roamRadius, dodgeMax, fightBonusMax,
-- bandageHours, callCoolMin) -- gelesen ueber cfgNum; ueber optNum nur noch die zwoelf Optionen (hier BearFleeHits, BearDamagePercent).
-- F3 (Lauf baer-f3, PLAN_F3.md 10; Kevin 13.11.2026, f3/KEVIN_ANTWORTEN.md): Fenster Variante B. Die "Coming later"-Zeile ist weg -- dafuer
-- vier Balken-Zeilen Hunger / Thirst / Tiredness (fuellen sich mit dem Druck) und Trust (fuellt sich mit dem Guten) aus den Sicht-Feldern
-- hun / thr / tir / tru (0..100; fehlt eins: "--" ohne Balken, nie geraten). Prozent in der Zeile, das WORT der Stufe im Tooltip (Antwort
-- 6g), dazu was senkt, was droht und was gerade wirkt; KEINE Uhrzeiten (6c). Zustand "Sleeping" (Sicht slp) nach Boden / Kampf / Rueckzug,
-- Fusszeile "Any order wakes it up" (6e: kein Schlaf-Knopf). SICHTBARE Gruende (Antworten 3 und 4): kaempft der grosse Baer nicht, weil er
-- zu muede ist (ab 90 %) oder sich weigert (sehr wenig Vertrauen), steht das in der Fusszeile in Warnfarbe und in den Tooltips von
-- Muedigkeit / Vertrauen / Melee damage -- Grund aus dem Sicht-Feld nof ("tired" / "trust") des Schreibers; fehlt es (Kern ohne das Feld),
-- aus tir / tru und den Schwellen des Kerns (B.CFG tirVery / trRefuse). Die spaeteren Knoepfe Fish (F5), Inventory (F4) und der Schalter
-- Nose alerts (F5) stehen schon an ihrem Platz, grau mit "Comes with a later version." -- kein Klick, keine Bitte, nichts wandert spaeter.
-- Alle Zahlen der Texte (Schwellen, Bonus, Untergrenze des Lebens) liest das Fenster aus B.CFG (cfgNum mit Rueckfall), keine eigene Wahrheit.
-- F4 (Lauf baer-f4, PLAN_F4.md 8.1; Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md): die Zeile "Can carry up to 62" wird "Load 18.5 / 62 kg"
-- (Sicht ivW / ivC des Schreibers, nur fuer den Besitzer; ueber der Grenze ivX: Wert in Warnfarbe; alte Sicht ohne ivW: "--"). Tooltip: was er
-- jetzt traegt, wie viel er je Groesse tragen kann (B.CFG.carryAt x Sandbox BearCarryPercent), Packtaschen an / aus (Sicht bag, +bagAdd ab
-- halbstark), Zahl der Dinge (ivK von invMaxItems = 1000) und ggf. "zu schwer". Die Felder heissen weiter d.carry / s.tCarry (das Fenster legt die
-- Zeile unveraendert). Der Knopf "Inventory" ist scharf: ansehen geht immer -- auch von weitem (Kevin Antwort 2); grau nur, wenn das
-- Inventar-Fenster fehlt (U.InvOpen, client/ISUI/BanditsNPCBearInvWindow.lua). Geben / Nehmen prueft erst das Inventar-Fenster.
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

local CMDS = { "follow", "stay", "sit", "roam", "come", "unstuck", "fish", "inv" }     -- F3: + fish (grau bis F5), inv (F4 scharf)
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
    -- F3 (PLAN_F3.md 10.1): schlaeft (Chip in der EINEN Schlaf-Farbe, client/ISUI/BanditsNPCBearWinParts.lua)
    sleep = { "UI_BN_Bear_Win_St_Sleep", "stSleep" },
}
local STATE_ORDER = { "missing", "ride", "away", "down", "fight", "retreat", "rest", "sleep", "hide", "come", "follow", "stay", "sit",
    "roam" }
-- F3 (PLAN_F3.md 10.3; Kevin Antwort 6g): Woerter der Stufen fuer den Tooltip, je Wert ausgeschrieben (Stufe 1 = gut).
local WORD_KEY = {
    hun = { "UI_BN_Bear_Win_Word_Hun1", "UI_BN_Bear_Win_Word_Hun2", "UI_BN_Bear_Win_Word_Hun3", "UI_BN_Bear_Win_Word_Hun4" },
    thr = { "UI_BN_Bear_Win_Word_Thr1", "UI_BN_Bear_Win_Word_Thr2", "UI_BN_Bear_Win_Word_Thr3", "UI_BN_Bear_Win_Word_Thr4" },
    tir = { "UI_BN_Bear_Win_Word_Tir1", "UI_BN_Bear_Win_Word_Tir2", "UI_BN_Bear_Win_Word_Tir3", "UI_BN_Bear_Win_Word_Tir4" },
    tru = { "UI_BN_Bear_Win_TrustWord1", "UI_BN_Bear_Win_TrustWord2", "UI_BN_Bear_Win_TrustWord3", "UI_BN_Bear_Win_TrustWord4",
        "UI_BN_Bear_Win_TrustWord5" },
}
local WORD_ORDER = { "hun", "thr", "tir", "tru" }
-- Verlauf der letzten Tage (Sicht trW: Text aus Ziffern, aeltester Tag zuerst): Ziffer -> Schluessel
local DAY_KEY = { ["0"] = "UI_BN_Bear_Win_TrustDay0", ["1"] = "UI_BN_Bear_Win_TrustDay1", ["2"] = "UI_BN_Bear_Win_TrustDay2" }
local NEED_EFFECT = { "UI_BN_Bear_Win_NeedEffect2", "UI_BN_Bear_Win_NeedEffect3", "UI_BN_Bear_Win_NeedEffect4" }
-- F2 (11.4): Tooltip-Satz je Wachstums-Stufe am Alters-Deckel (ausgeschrieben; ausgewachsen gibt es keinen Deckel unter 10)
local STAGE_IDX = { cub = 1, half = 2, strong = 3, adult = 4 }
local CAP_TIP = { "UI_BN_Bear_Win_SkAgeTip_Cub", "UI_BN_Bear_Win_SkAgeTip_Half", "UI_BN_Bear_Win_SkAgeTip_Strong" }
local DIR_KEY = { N = "UI_BN_Bear_Dir_N", NE = "UI_BN_Bear_Dir_NE", E = "UI_BN_Bear_Dir_E", SE = "UI_BN_Bear_Dir_SE",
    S = "UI_BN_Bear_Dir_S", SW = "UI_BN_Bear_Dir_SW", W = "UI_BN_Bear_Dir_W", NW = "UI_BN_Bear_Dir_NW" }
local BTN_KEY = { follow = "UI_BN_Bear_Win_Follow", stay = "UI_BN_Bear_Win_Stay", sit = "UI_BN_Bear_Win_Sit",
    roam = "UI_BN_Bear_Win_Roam", come = "UI_BN_Bear_Win_Come", unstuck = "UI_BN_Bear_Win_Unstuck",
    fish = "UI_BN_Bear_Win_Fish", inv = "UI_BN_Bear_Win_Inv" }                         -- F3: Fish Platzhalter bis F5; F4: Inventory scharf

local ST = nil      -- feste Texte dieser Sitzung (einmal ueber U.T geholt)

-- Fester Wert des Kerns (B.CFG) als Zahl, sonst def. Steht vor statics, weil die F3-Texte Zahlen des Kerns nennen.
local function cfgNum(name, def)
    local c = B.CFG
    local v = c and tonumber(c[name])
    if v == nil then return def end
    return v
end

-- F3: Anteil (0..1) des Kerns als ganze Prozent fuer einen Text (0,2 -> 20). Ein Wert ueber 1 gilt schon als Prozent.
local function cfgPct(name, def)
    local v = cfgNum(name, def)
    if v <= 1 then v = v * 100 end
    return math.floor(v + 0.5)
end

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
    s.tHealth, s.tStamina, s.tCarry = U.T("UI_BN_Bear_Win_Health"), U.T("UI_BN_Bear_Win_Stamina"), U.T("UI_BN_Bear_Win_Load")   -- F4: Load
    s.tipHealth = TIP_HEAD .. s.tHealth .. TIP_BODY .. U.T("UI_BN_Bear_Win_HealthTip")
    s.tipStamina = TIP_HEAD .. s.tStamina .. TIP_BODY .. U.T("UI_BN_Bear_Win_StaminaTip")
    -- F4 (PLAN_F4.md 8.1): Teile des Load-Tooltips; die Zahlen (Traglast je Groesse x Sandbox-Prozent) setzt loadTip je Modell ein
    s.packsOn = U.T("UI_BN_Bear_Win_LoadPacks", math.floor(cfgNum("bagAdd", 150) + 0.5))       -- Rueckfall 150 (Kevin 13.11., Nachbesserung P11)
    s.packsOff = U.T("UI_BN_Bear_Win_LoadNoPacks")
    s.packsTip = U.T("UI_BN_Bear_Win_LoadPacksTip", math.floor(cfgNum("bagAdd", 150) + 0.5))
    s.loadOver, s.tipInv = U.T("UI_BN_Bear_Win_LoadOver"), U.T("UI_BN_Bear_Win_InvTip")
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
    -- F3 (PLAN_F3.md 10): Karte "Needs", Woerter der Stufen, Tooltip-Texte mit den Zahlen des Kerns (B.CFG; Rueckfall = Kevins Antworten
    -- vom 13.11.: Leben bis 1 %, zu muede ab 90 %, schlaeft bei 100 % ein, Vertrauen +-20 %, Weigerung unter 15 %), Schlaf, Platzhalter
    s.tNeeds = U.T("UI_BN_Bear_Win_Needs")
    s.tHunger, s.tThirst, s.tTired, s.tTrust = U.T("UI_BN_Bear_Win_Hunger"), U.T("UI_BN_Bear_Win_Thirst"), U.T("UI_BN_Bear_Win_Tired"),
        U.T("UI_BN_Bear_Win_Trust")
    s.word = {}
    for i = 1, #WORD_ORDER do
        local k = WORD_ORDER[i]
        s.word[k] = {}
        for j = 1, #WORD_KEY[k] do s.word[k][j] = U.T(WORD_KEY[k][j]) end
    end
    s.trDay = {}
    for digit, key in pairs(DAY_KEY) do s.trDay[digit] = U.T(key) end
    s.needEffect = {}
    for i = 1, #NEED_EFFECT do s.needEffect[i] = U.T(NEED_EFFECT[i]) end
    local floorPct = cfgPct("needHpFloor", 0.01)
    s.bodyHunger = U.T("UI_BN_Bear_Win_HungerTip", floorPct)
    s.bodyThirst = U.T("UI_BN_Bear_Win_ThirstTip", floorPct)
    s.sleepHeal = U.T("UI_BN_Bear_Win_SleepHeal")
    s.bodyTired = U.T("UI_BN_Bear_Win_TiredTip", math.floor(cfgNum("tirVery", 90) + 0.5), math.floor(cfgNum("tirCollapse", 100) + 0.5))
        .. TIP_LINE .. s.sleepHeal
    local bonus = cfgPct("trBonus", 0.2)
    s.bodyTrust = U.T("UI_BN_Bear_Win_TrustTip", bonus, cfgPct("trMalus", bonus / 100), math.floor(cfgNum("trRefuse", 15) + 0.5))
        .. TIP_LINE .. U.T("UI_BN_Bear_Win_TrustHeart")
    s.hintSleep, s.hintTired, s.hintNoTrust = U.T("UI_BN_Bear_Win_HintSleep"), U.T("UI_BN_Bear_Win_HintTired"),
        U.T("UI_BN_Bear_Win_HintNoTrust")
    s.nose, s.whyLater = U.T("UI_BN_Bear_Win_Nose"), U.T("UI_BN_Bear_Why_Later")
    s.needsOff = U.T("UI_BN_Bear_Win_NeedsOff")
    s.off = U.T("UI_BN_Bear_MO_Off")                            -- Nachbesserung P3: Wert der drei Zeilen bei Sandbox-Regler 0
    s.widePctNeed = U.T("UI_BN_Bear_Win_Pct", 100)
    -- Breiteste Texte fuer das Legen des Fensters (Breite waechst nur, wenn ein Text nicht passt, PLAN_F1.md 1.1)
    s.wideVal = U.T("UI_BN_Bear_Win_Count", 888, 888)
    s.wideCarry = U.T("UI_BN_Bear_Win_LoadVal", "888.8", 888)             -- F4: "Load 888.8 / 888 kg"
    s.wideLv = U.T("UI_BN_Bear_Win_Lv", 10)
    s.widePct = U.T("UI_BN_Bear_Win_Pct", 100)
    s.wideUnstuck = U.T("UI_BN_Bear_Win_UnstuckWait", "9:59")
    s.wideDist = U.T("UI_BN_Bear_Win_LastSeen", 888, U.T("UI_BN_Bear_Dir_NW"))
    s.wideDist2 = U.T("UI_BN_Bear_Win_Dist", 888, U.T("UI_BN_Bear_Dir_NW"))
    s.wideMelee = U.T("UI_BN_Bear_Win_MeleeVal", 888)                     -- F2 (11.2)
    s.wideKills = U.T("UI_BN_Bear_Win_KillsVal", 8888, 888)               -- F2 (11.5)
    -- Aussehen (PLAN_AUSSEHEN.md 8.1): Namen aller Aussehen beider Koerper (Schluessel aus B.LOOKS des Kerns, einmal je Sitzung) und die
    -- Knopf-Texte mit jedem Namen und mit der Uhr -- das Fenster misst daran die Knopfbreite (nichts springt beim Wechsel)
    s.lookName = {}
    s.lookLabels = {}
    local looks = B.LOOKS
    if type(looks) == "table" then
        for _, list in pairs(looks) do
            if type(list) == "table" then
                for i = 1, #list do
                    local key = type(list[i]) == "table" and list[i].txt
                    if type(key) == "string" and s.lookName[key] == nil then
                        s.lookName[key] = U.T(key)
                        s.lookLabels[#s.lookLabels + 1] = U.T("UI_BN_Bear_Win_Look", s.lookName[key])
                    end
                end
            end
        end
    end
    s.wideLook = U.T("UI_BN_Bear_Win_LookWait", "9:59")
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

-- Sandbox-Zahl ueber den Kern (B.Opt klemmt und faellt selbst auf die Vorgabe zurueck); fehlt der Kern: def. Nur fuer die zwoelf
-- Optionen aus B.OPTS (Sandbox-Kuerzung): alles andere ist ein fester Wert des Kerns -> cfgNum.
local function optNum(name, def)
    local v = nil
    if B.Opt then v = tonumber(B.Opt(name)) end
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
        tip = tip .. TIP_LINE .. U.T("UI_BN_Bear_Menu_BandageTip", item:getDisplayName(), math.floor(cfgNum("bandageHours", 8) + 0.5))
    end
    local e = cmdBtn(s.bandage, false, why, tip)
    e.kind = "mend"
    return e
end

-- Wirkung einer Faehigkeit mit der Zahl von jetzt (PLAN_F1.md 1.5 Tabelle; Zahlen aus der Sicht bzw. Kevins Formeln ENT:221-230).
local function skillEffect(key, v, L)
    if key == "agi" then
        return U.T("UI_BN_Bear_Win_SkTip_Agi", pctOf(v.dodge), math.floor(cfgNum("dodgeMax", 40) + 0.5))
    elseif key == "vit" then
        return U.T("UI_BN_Bear_Win_SkTip_Vit", math.floor(cfgNum("vitPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "con" then
        return U.T("UI_BN_Bear_Win_SkTip_Con", math.floor(cfgNum("conPerLv", 0.05) * L * 100 + 0.5))
    elseif key == "fgt" then
        return U.T("UI_BN_Bear_Win_SkTip_Fgt", pctOf(v.fgtB), math.floor(cfgNum("fightBonusMax", 70) + 0.5))
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

-- F4 (PLAN_F4.md 8.1): Zeile "Load 18.5 / 62 kg" aus der Sicht des Schreibers (ivW Last, ivC Kapazitaet -- nur fuer den Besitzer).
-- Ueber der Grenze (ivX) steht der Wert in Warnfarbe (e.col, client/ISUI/BanditsNPCBearWinParts.lua drawVal); fehlt ein Wert (alte Sicht):
-- "--". Nie nachgerechnet. kg mit einer Nachkommastelle (U.Kg, client/BanditsNPCBearInvClient.lua; Rueckfall string.format wie dort).
local function loadRow(v, s)
    local e = { label = s.tCarry, val = s.none }
    if isNum(v.ivW) and isNum(v.ivC) then
        local kg = U.Kg and U.Kg(v.ivW) or string.format("%.1f", v.ivW)
        e.val = U.T("UI_BN_Bear_Win_LoadVal", kg, math.floor(v.ivC + 0.5))
        if v.ivX == true then e.col = "warn" end
    end
    return e
end

-- F4: Tooltip der Load-Zeile -- Erklaerung mit der Traglast je Groesse (B.CFG.carryAt des Kerns, 10 / 40 / 100, mal Sandbox
-- BearCarryPercent), Packtaschen an / aus (Sicht bag), Zahl der Dinge (ivK von B.CFG.invMaxItems), "zu schwer" (ivX), Sandbox-Prozent.
local function loadTip(v, s)
    local pct = optNum("BearCarryPercent", 100)
    local at = B.CFG and B.CFG.carryAt
    local a, b, c = 10, 40, 100
    if type(at) == "table" then a, b, c = tonumber(at[1]) or a, tonumber(at[2]) or b, tonumber(at[3]) or c end
    local k = pct / 100
    -- U.TB: Junges "your cub", grosser Koerper "your bear" (Nachbesserung F4, Befund P10)
    local t = TIP_HEAD .. s.tCarry .. TIP_BODY .. U.TB("UI_BN_Bear_Win_LoadTip", v.bd, math.floor(a * k + 0.5), math.floor(b * k + 0.5),
        math.floor(c * k + 0.5))
    if v.bag == true then
        t = t .. TIP_LINE .. s.packsOn
    else
        t = t .. TIP_LINE .. s.packsOff .. TIP_LINE .. s.packsTip
    end
    if isNum(v.ivK) then
        t = t .. TIP_LINE .. U.T("UI_BN_Bear_Inv_Things", math.floor(v.ivK), math.floor(cfgNum("invMaxItems", 1000)))
    end
    if v.ivX == true then t = t .. TIP_LINE .. s.loadOver end
    if math.floor(pct + 0.5) ~= 100 then t = t .. TIP_LINE .. U.T("UI_BN_Bear_Win_LoadPct", math.floor(pct + 0.5)) end
    return t
end

-- F3 (PLAN_F3.md 10.3): Stufe eines Werts (0..100) fuer das Wort im Tooltip -- 1 = gut. Hunger und Durst teilen ihre Schwellen
-- (needPeckish 25 / needHungry 50 / needStarve 80), Muedigkeit tirTired 40 / tirHeavy 70 / tirVery 90 (ab da zu muede zum Kaempfen,
-- Kevin Antwort 3), Vertrauen feste Fuenftel (PLAN_F3.md 4.2). Die Regel gehoert dem Kern: B.NeedWord(kind, v) -> 1..4 bzw.
-- B.TrustWord(v) -> 1..5 (shared/BanditsNPCBearNeedRules.lua, f3/schnittstelle.md K5); fehlen sie, dieselbe Regel hier mit den Zahlen
-- aus B.CFG (Rueckfall wie genannt).
local function needLevel(kind, v)
    local f = B.NeedWord
    if kind == "tru" then f = B.TrustWord end
    if f then
        local L = nil
        if kind == "tru" then L = tonumber(f(v)) else L = tonumber(f(kind, v)) end
        if L ~= nil and L >= 1 then return math.floor(L) end
    end
    if kind == "tru" then
        if v >= 80 then return 5 elseif v >= 60 then return 4 elseif v >= 40 then return 3 elseif v >= 20 then return 2 end
        return 1
    end
    local a, b, c = cfgNum("needPeckish", 25), cfgNum("needHungry", 50), cfgNum("needStarve", 80)
    if kind == "tir" then a, b, c = cfgNum("tirTired", 40), cfgNum("tirHeavy", 70), cfgNum("tirVery", 90) end
    if v >= c then return 4 elseif v >= b then return 3 elseif v >= a then return 2 end
    return 1
end

-- F3 (PLAN_F3.md 10.1): Beduerfnis-Zeile. Wert 0..100 aus der Sicht; fehlt er: "--" ohne Balken (nie geraten, wie valueRow). Hunger /
-- Durst / Muedigkeit fuellen sich mit dem Druck (Verlauf "need"), Vertrauen mit dem Guten ("trust"). e.pct = ganze Prozent, e.word = Wort.
-- Nachbesserung P3: off = der Sandbox-Regler BearNeedsPercent steht auf 0 (B.NeedsOn() == false) -- dann steht "Off" statt "0%" da und
-- kein Balken (ein leerer Balken mit 0 % saehe aus wie "alles bestens"); den Satz dazu traegt der Tooltip (s.needsOff).
local function needRow(label, pct, kind, ramp, s, off)
    local e = { label = label, val = s.none }
    if off then
        e.val = s.off
        return e
    end
    if isNum(pct) then
        local frac = clamp(pct / 100, 0, 1)
        e.frac = frac
        e.pct = math.floor(frac * 100 + 0.5)
        e.val = U.T("UI_BN_Bear_Win_Pct", e.pct)
        e.word = s.word[kind][needLevel(kind, e.pct)] or ""
        if U.WinRamp then e.r, e.g, e.b = U.WinRamp(ramp, frac) end
    end
    return e
end

-- F3: Tooltip eines Beduerfnis-Balkens -- Kopf, "Now: <Wort> (n%)", Erklaerung (body), dazu bis zu zwei Zeilen (was gerade wirkt).
local function needTip(title, e, body, extra1, extra2)
    local t = TIP_HEAD .. title .. TIP_BODY
    if e.pct ~= nil then t = t .. U.T("UI_BN_Bear_Win_NeedNow", e.word, e.pct) .. TIP_LINE end
    t = t .. body
    if extra1 then t = t .. TIP_LINE .. extra1 end
    if extra2 then t = t .. TIP_LINE .. extra2 end
    return t                                                    -- extra1 / extra2 duerfen einzeln fehlen
end

-- F3 (PLAN_F3.md 3.1): was Hunger bzw. Durst GERADE bewirkt (Satz fuer den Tooltip) oder nil -- ab needHungry langsamer / schwaecher,
-- ab needStarve kein Wachsen / Heilen, bei 100 kostet es Leben.
local function needEffect(e, s)
    local p = e.pct
    if p == nil then return nil end
    if p >= 100 then return s.needEffect[3] end
    if p >= cfgNum("needStarve", 80) then return s.needEffect[2] end
    if p >= cfgNum("needHungry", 50) then return s.needEffect[1] end
    return nil
end

-- F3 (Kevin 13.11.2026, Antworten 3 und 4): kaempft der Baer gerade NICHT, und warum? "trust" (weigert sich, sehr wenig Vertrauen) vor
-- "tired" (zu muede). Wahrheit ist das Sicht-Feld nof des Schreibers ("tired" / "trust"): ein Kern mit F3 (erkennbar an seiner Regel
-- B.NoFight, shared/BanditsNPCBearNeedRules.lua) meldet es selbst -- fehlt nof dann, kaempft er (kein Nachrechnen aus gerundeten
-- Sicht-Zahlen, keine zweite Wahrheit). Nur ohne einen solchen Kern aus tru / tir und den Schwellen (Rueckfall 15 / 90). Nur der grosse
-- Koerper kaempft ueberhaupt.
local function noFight(v)
    if v.bd ~= "big" or v.st ~= "tame" then return nil end
    local f = v.nof
    if f == "tired" or f == "trust" then return f end
    if f ~= nil or B.NoFight ~= nil then return nil end
    if isNum(v.tru) and v.tru < cfgNum("trRefuse", 15) then return "trust" end
    if isNum(v.tir) and v.tir >= cfgNum("tirVery", 90) then return "tired" end
    return nil
end

-- F3 (PLAN_F3.md 4.1): Verlauf der letzten (bis zu drei) Tage als Tooltip-Zeile aus dem Sicht-Feld trW (Text aus Ziffern, aeltester Tag
-- zuerst: 0 gut versorgt, 1 hungrig oder durstig, 2 ausgehungert oder ausgetrocknet). Kein Text oder nur Unbekanntes: nil.
local function trustDays(w, s)
    if type(w) ~= "string" or w == "" then return nil end
    local parts = {}
    local n = string.len(w)
    if n > 3 then n = 3 end
    for i = 1, n do
        local word = s.trDay[string.sub(w, i, i)]
        if word then parts[#parts + 1] = word end
    end
    if #parts == 0 then return nil end
    return U.T("UI_BN_Bear_Win_TrustDays", table.concat(parts, ", "))
end

-- Zustand nach Vorrang (PLAN_F1.md 1.4): vermisst > faehrt mit > ausser Reichweite > versteckt > kommt > Modus.
local function stateOf(v, mode)
    if v.st == "missing" then return "missing" end
    if v.ride == true then return "ride" end
    if v.ld ~= true then return "away" end
    if v.dn == true then return "down" end                      -- F2 (PLAN_F2.md 3.2): am Boden > kaempft > zurueck / verschnauft
    if v.fst == "fight" then return "fight" end
    if v.fst == "retreat" or v.fst == "rest" then return v.fst end
    if v.slp == true then return "sleep" end                    -- F3 (PLAN_F3.md 9, 10.1): schlaeft (Boden und Kampf gehen vor)
    if v.hide == true then return "hide" end
    if v.cm == true then return "come" end
    return mode
end

-- Aussehen (PLAN_AUSSEHEN.md 8.1): Name eines Eintrags aus B.LOOKS (Text einmal je Sitzung, statics; ein unbekannter Schluessel wird
-- nachgeholt). Nur Tabellen-Lesen und U.T.
local function lookNameOf(s, e)
    local key = type(e) == "table" and e.txt or nil
    if type(key) ~= "string" then return "?" end
    local name = s.lookName[key]
    if name == nil then
        name = U.T(key)
        s.lookName[key] = name
    end
    return name
end

-- Erster Grund aus einer Liste (nil-Luecken erlaubt, n = Laenge).
local function firstIn(list, n)
    for i = 1, n do
        if list[i] then return list[i] end
    end
    return nil
end

-- Aussehen (PLAN_AUSSEHEN.md 8.1): Knopf "Look: <Name>" (Uhr: "Look  m:ss"). Vorpruefung aus der Sicht in der Reihenfolge des Plans
-- (mitfahrend, ausser Reichweite, am Boden, im Fahrzeug, Kampf, beschaeftigt, Zombies nah, Wachs-Tausch wartet, gemeinsame Uhr mit
-- Unstuck, nur ein Aussehen); entscheiden tut der Schreiber. e.picks = Angebot fuer das Menue des Fensters { k, name, cur } in der
-- Reihenfolge von B.LOOKS. nil, wenn der Kern kein Aussehen kennt (B.LOOKS / B.LookFor / B.LookHas fehlen) -- dann kein Knopf.
local function lookBtn(v, bd, s, w, waitMs, cool)
    if type(B.LOOKS) ~= "table" or not B.LookFor or not B.LookHas then return nil end
    local body = (bd == "big") and "big" or "cub"
    local cur = B.LookFor(body, v.lk or "std")
    local curName = lookNameOf(s, cur)
    local picks = {}
    local others = 0
    local list = B.LOOKS[body]
    if type(list) == "table" then
        for i = 1, #list do
            local e = list[i]
            if type(e) == "table" and type(e.k) == "string" and e.hide ~= true and B.LookHas(e.art) then
                picks[#picks + 1] = { k = e.k, name = lookNameOf(s, e), cur = (e.k == cur.k) }
                if e.k ~= cur.k then others = others + 1 end
            end
        end
    end
    local label = U.T("UI_BN_Bear_Win_Look", curName)
    local shared = U.T("UI_BN_Bear_Win_LookShared", cool)
    local whyWait, whyOne = nil, nil
    if waitMs > 0 then
        label = U.T("UI_BN_Bear_Win_LookWait", clock(waitMs))
        whyWait = U.T("UI_BN_Bear_Win_LookWaitClock", clock(waitMs)) .. TIP_LINE .. shared
    end
    -- Nachbesserung Aussehen A1 (PRUEF_A.md): grau "nur ein Aussehen" erst, wenn es AUSSER dem jetzigen kein Angebot gibt. Traegt der
    -- Baer ein spaeter mit hide gestrichenes Aussehen (es steht dann nicht im Angebot), bleiben die anderen waehlbar -- der Schreiber
    -- prueft nur das ZIEL (server/BanditsNPCBearLook.lua). Dieselbe Zaehlung oeffnet das Menue (client/ISUI/BanditsNPCBearWindow.lua).
    if others < 1 then whyOne = U.TB("UI_BN_Bear_Win_LookOne", bd) end
    local whyFight = v.fst ~= nil and U.TB("UI_BN_Bear_Why_LookFight", bd)
    local whyBusy = v.busy == true and U.TB("UI_BN_Bear_Why_LookBusy", bd)
    local whyDanger = v.hide == true and U.TB("UI_BN_Bear_Why_LookDanger", bd)
    local whyGrow = v.lkg == true and U.TB("UI_BN_Bear_Why_LookGrow", bd)
    local why = firstIn({ w.ride, w.away, w.down, w.car, whyFight, whyBusy, whyDanger, whyGrow, whyWait, whyOne }, 10)
    local e = cmdBtn(label, false, why, U.TB("UI_BN_Bear_Win_LookTip", bd) .. TIP_LINE .. shared)
    e.picks = picks
    e.others = others
    e.cur = cur.k
    return e
end

-- ---------------------------------------------------------------------------
-- U.WinModel(v, player, nowMs): das fertige Modell eines Baeren (v = Eintrag aus U.WinBears). Neue Tabelle je Aufruf (1 x je Sekunde).
-- ---------------------------------------------------------------------------
function U.WinModel(v, player, nowMs)
    local s = statics()
    local d = { id = v.id, tCond = s.tCond, tNeeds = s.tNeeds, tSkills = s.tSkills, tOrders = s.tOrders, rename = s.rename, wide = s }
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
    -- F3 (Kevin Antworten 3 und 4): kaempft er gerade nicht ("tired" / "trust")? Steht in Fusszeile und Tooltips.
    local nof = noFight(v)
    d.noFight = nof
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
    elseif st == "sleep" then
        d.footer = s.hintSleep                                  -- F3 (Kevin 6e): kein Schlaf-Knopf, jeder Befehl weckt
    elseif nof == "trust" then
        d.footer, d.footerCol = s.hintNoTrust, "warn"           -- F3 (Kevin Antwort 4): weigert sich zu kaempfen -- steht sichtbar da
    elseif nof == "tired" then
        d.footer, d.footerCol = s.hintTired, "warn"             -- F3 (Kevin Antwort 3): zu muede zum Kaempfen -- er sagt es
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
    d.carry = loadRow(v, s)                                     -- F4 (PLAN_F4.md 8.1): "Load 18.5 / 62 kg"
    -- F2: Leben mit Verband (Zeichen am Wert + Tooltip) und Flucht-Schwelle (nur der grosse Koerper kaempft); Melee damage, Kills
    local hpTip = s.tipHealth
    if isNum(v.bnd) and v.bnd > 0 then
        d.hp.bnd = true
        hpTip = hpTip .. TIP_LINE .. U.T("UI_BN_Bear_Win_Bandaged", hoursOf(v.bnd))
    end
    if bd == "big" then hpTip = hpTip .. TIP_LINE .. fleeLine(v, s) end
    hpTip = hpTip .. TIP_LINE .. s.sleepHeal                    -- F3 (Kevin 11.11.2026: im Schlaf viel schneller heilen)
    d.melee = meleeRow(v, s)
    d.kills = killsRow(v, s)
    -- F3 (PLAN_F3.md 10.1, 10.3): vier Balken der Karte "Needs" -- Prozent in der Zeile, Wort und Folgen im Tooltip
    local whyNoFight = nil
    if nof == "trust" then whyNoFight = s.hintNoTrust elseif nof == "tired" then whyNoFight = s.hintTired end
    if whyNoFight then d.melee.tip = d.melee.tip .. TIP_LINE .. whyNoFight end
    local needsOff = B.NeedsOn ~= nil and B.NeedsOn() == false
    d.hun = needRow(s.tHunger, v.hun, "hun", "need", s, needsOff)
    d.thr = needRow(s.tThirst, v.thr, "thr", "need", s, needsOff)
    d.tir = needRow(s.tTired, v.tir, "tir", "need", s, needsOff)
    d.tru = needRow(s.tTrust, v.tru, "tru", "trust", s)           -- das Vertrauen laeuft auch bei Regler 0 weiter
    -- Sicht mdmgK (nur wenn < 1): Schaden-Faktor durch Hunger / Durst, in mdmg schon eingerechnet -- der Tooltip nennt ihn
    if isNum(v.mdmgK) and v.mdmgK > 0 and v.mdmgK < 1 then
        d.melee.tip = d.melee.tip .. TIP_LINE .. U.T("UI_BN_Bear_Win_MeleeWeak", math.floor(v.mdmgK * 100 + 0.5))
    end
    -- Sicht meal / bowl: so viele Prozent senkt EINE Mahlzeit / ein halber Liter bei dieser Groesse (wahlfrei); Sandbox-Regler auf 0
    -- (B.NeedsOn() == false): die drei Beduerfnisse stehen still -- der Tooltip sagt es
    local mealLine, bowlLine, offLine = nil, nil, nil
    if isNum(v.meal) and v.meal > 0 then mealLine = U.T("UI_BN_Bear_Win_MealLine", fmt100(v.meal)) end
    if isNum(v.bowl) and v.bowl > 0 then bowlLine = U.T("UI_BN_Bear_Win_BowlLine", fmt100(v.bowl)) end
    if needsOff then offLine = s.needsOff end
    d.tips = { hp = hpTip, sta = s.tipStamina, carry = loadTip(v, s), melee = d.melee.tip, kills = d.kills.tip,
        hun = needTip(s.tHunger, d.hun, s.bodyHunger, firstOf(offLine, mealLine), needEffect(d.hun, s)),
        thr = needTip(s.tThirst, d.thr, s.bodyThirst, firstOf(offLine, bowlLine), needEffect(d.thr, s)),
        tir = needTip(s.tTired, d.tir, s.bodyTired, offLine, nof == "tired" and s.hintTired or nil),
        tru = needTip(s.tTrust, d.tru, s.bodyTrust, trustDays(v.trW, s), nof == "trust" and s.hintNoTrust or nil) }
    d.skills = skillsOf(v, s)
    -- Befehle (PLAN_F1.md 1.6): Vorpruefung aus der Sicht, entscheiden tut der Schreiber
    local ride = (v.ride == true)
    local gone = (v.st == "missing") or (v.ld ~= true)
    local inCar = player:getVehicle() ~= nil            -- V:client/ISUI/Hutch/ISHutchMenu.lua:8
    local far = (not gone) and d.distN ~= nil and d.distN > cfgNum("followMaxDist", 40)
    local cm = tame and v.cm == true
    local whyRide = ride and U.TB("UI_BN_Bear_Why_Riding", bd)
    local whyAway = gone and U.TB("UI_BN_Bear_Why_OutOfReach", bd)
    local whyCar = inCar and s.whyCar
    local whyFar = far and s.whyFar
    local whyDown = tame and v.dn == true and U.TB("UI_BN_Bear_Why_Down", bd)    -- F2: am Boden nimmt der Schreiber keinen Befehl an
    local act = nil
    if tame then act = mode end
    local radius = math.floor(cfgNum("roamRadius", 12) + 0.5)
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
    local cool = math.floor(cfgNum("callCoolMin", 5) + 0.5)
    -- Aussehen (PLAN_AUSSEHEN.md 8.1): Knopf in Zelle 3 der vierten Reihe (nil = Kern ohne Aussehen, kein Knopf); die Uhr ist dieselbe wie
    -- bei Unstuck -- deshalb nennt auch der Unstuck-Tooltip die gemeinsame Wartezeit (nur, wenn es den Knopf gibt)
    d.look = lookBtn(v, bd, s, { ride = whyRide, away = whyAway, down = whyDown, car = whyCar }, waitMs, cool)
    local uTip = U.TB("UI_BN_Bear_Menu_CallTip", bd, cool)
    if d.look then uTip = uTip .. TIP_LINE .. U.T("UI_BN_Bear_Win_UnstuckShared", cool) end
    b.unstuck = cmdBtn(uLabel, false, firstOf(whyRide, whyCar, whyWait), uTip)
    -- F3 (PLAN_F3.md 10.2): Fish (F5) steht schon an seinem Platz -- grau mit Grund, kein Klick, keine Bitte
    b.fish = cmdBtn(s.btn.fish, false, s.whyLater, nil)
    -- F4 (PLAN_F4.md 7, 8.1; Kevin Antwort 2): Inventory scharf -- ansehen geht immer; grau nur ohne das Inventar-Fenster (Datei fehlt)
    b.inv = cmdBtn(s.btn.inv, false, (not U.InvOpen) and s.whyLater or nil, s.tipInv)
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
        dmg = dmgOn, dmgLabel = s.showDmg, dmgTip = TIP_HEAD .. s.showDmg .. TIP_BODY .. s.tipShowDmg,
        -- F3 (PLAN_F3.md 10.2): Schalter "Nose alerts" (F5) als grauer Platzhalter
        nose = false, noseOff = true, noseLabel = s.nose, noseTip = TIP_HEAD .. s.nose .. TIP_BODY .. s.whyLater }
    return d
end
