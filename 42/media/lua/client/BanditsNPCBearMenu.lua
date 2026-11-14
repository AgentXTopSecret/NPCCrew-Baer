--
-- NPC Crew -- Baer, Rechtsklick (B1a, PLAN_ZAEHMEN.md 5.2-5.4, 5.7, 6.8).
--
-- Tier-Menue: am Jungen (Art B.CUB) "Fuettern" (Untermenue mit dem Futter aus dem Inventar) und "Streicheln"; Vanillas "Kill"
-- wird am Jungen ausgeblendet (Menue-Hygiene, kein Schutz). Welt-Menue: "Baeren-Koeder auslegen" und "Koederplatz aufgeben".
-- B1b (PLAN_B1B.md 1.1, 3.1, 3.2): am eigenen gezaehmten Jungen der Umschalter "Follow me" / "Stay here" und "Name the cub"
-- (nur der Besitzer, nur mit Sicht-Eintrag); im Welt-Menue "Hold out food for the cub" (Futter nur in die Hand nehmen, ohne das
-- Tier anzuklicken), wenn ein passendes Junges in B.CFG.lureDist Kacheln steht.
-- B1c (PLAN_B1C.md 1.5): am eigenen gezaehmten Jungen zusaetzlich "Call to me" (holt es neben den Besitzer; Abklingzeit,
-- Fahrzeug und freie Kachel prueft der Schreiber, grau vorgeprueft aus der Sicht).
-- B1e (PLAN_B1E.md 1.4, 3.2 Nr. 12): alles gilt fuer BEIDE Koerper -- das Junge (Art B.CUB) und den grossen Koerper ab Halbstark
-- (Art B.BIG). Ob ein Tier unser Baer ist, fragt nur B.BodyKind (Kern, einziger Art-Vergleich); "bear" (Test-Baer) bekommt nichts.
-- Beim grossen Koerper (Sicht bd == "big") heissen "Name the bear", der Call-Tooltip und die Wartezeit "bear" statt "cub" (U.TB).
-- F1 (PLAN_F1.md 3.3, 4a): am eigenen gezaehmten Baeren zusaetzlich "Bear window" (oeffnet das Baeren-Fenster,
-- client/ISUI/BanditsNPCBearWindow.lua); Gruende der Vorpruefung und "Hold out food" je Koerper (U.WhyText / U.TB mit bd); der
-- Umschalter kennt vier Modi (bei follow "Stay here", sonst "Follow me"); "Futter hinhalten" lockt nur einen BLEIBENDEN Baeren (der
-- Schreiber lockt im Sitzen und beim freien Herumlaufen nicht, PLAN_F1.md 2.3/2.4).
-- F1B (PLAN_F1B.md 0 E9, 2.4; Kevin 12.11.2026: V gehoert wieder NPC Crew und Vanilla): Vanillas Tier-Radial (Taste "Animal Radial
-- Menu", Vorgabe V) geht an unseren Baeren wieder auf -- aber wie das Rechtsklick-Menue OHNE "Kill", an jedem Baeren unserer Art
-- (eigen und fremd). Dafuer eine Huelle um AnimalContextMenu.showRadialMenu (Vanilla-Lua, angelegt in OnGameBoot, genau einmal,
-- Existenz-Riegel): Original rufen, danach die Kill-Scheibe herausnehmen (Vergleich der Funktion, sprachunabhaengig). Neue
-- Vanilla-Beruehrung -> baer/NAEHTE.md. Der Rechtsklick "Bear window" bleibt; sein Tooltip nennt jetzt die Nah-Taste.
-- F2 = B5a (PLAN_F2.md 2.5, 3.2, 4.6; Kevin 11.11.2026: "wir koennen den baeren manuel heilen"): am eigenen gezaehmten Baeren "Bandage the
-- cub/bear" (Zeitaktion BanditsNPCBearMendAction mit dem besten sauberen Verband aus dem Inventar, U.BestBandage) und am Boden "Help up the
-- cub/bear" (BanditsNPCBearHelpAction). U.MendAsk / U.HelpAsk stellen die Aktion an -- auch fuer den Knopf im Baeren-Fenster. Grau mit Grund
-- nur aus der Sicht (kein Verband, nicht verletzt, schon verbunden, am Boden); ob es gilt, entscheidet der Schreiber in complete()
-- (B.MendComplete / B.HelpUpComplete, KERN) -- dort wird GENAU EIN Verband genommen, ein Abbruch verbraucht nichts. Folgen/Bleiben ist am
-- Boden grau (Why_Down).
-- Sandbox-Kuerzung (Lauf baer-aussehen, PLAN_AUSSEHEN.md 9.3; Kevin 12.11.2026): Call-Abklingzeit, Verband-Heilung und -Stunden sind feste
-- Werte des Kerns (B.CFG callCoolMin, bandageHeal, bandageHours) statt Sandbox-Optionen. Das Aussehen hat KEINEN Rechtsklick-Eintrag
-- (Kevin: "fuer spieler als knopf" -- nur das Baeren-Fenster, PLAN_AUSSEHEN.md 8.3).
-- F3 (Lauf baer-f3, PLAN_F3.md 5; Kevin 13.11.2026, f3/KEVIN_ANTWORTEN.md): am eigenen gezaehmten Baeren "Give water to the cub/bear"
-- mit einem Untermenue der Wasser-Behaelter aus dem Inventar -- Vanillas eigene Liste und Beschriftung (V:client/ISUI/Animal/
-- ISAnimalContextMenu.lua:464-489), Zeitaktion BanditsNPCBearDrinkAction; wie viel er trinkt und ob es gilt, entscheidet der Schreiber
-- (B.DrinkComplete: Wasser wird erst nach allen Pruefungen in EINEM Aufruf genommen). Grau mit Grund aus der Sicht (B.CheckDrink des
-- Kerns: faehrt mit, am Boden, nicht durstig) bzw. Vanillas Text "kein Wasser". "Feed" am gezaehmten Baeren senkt jetzt den Hunger (die
-- Abklingzeit faellt dort weg, "satt" lehnt ab -- B.CheckFeed des Kerns); der Tooltip nennt Hunger bzw. Vertrauen von jetzt.
-- Schlaeft der Baer (Sicht slp), schickt der Klick auf Fuettern / Traenken vorher die Bitte "Wake" { id } (sanft wecken, Kevin 6e); die
-- Zeitaktionen warten ueber U.WakeWait hoechstens 5 s darauf. Streicheln weckt nicht. Kein Schlaf- oder Weck-Punkt im Menue.
-- F4 (Lauf baer-f4, PLAN_F4.md 7; Kevin 13.11.2026 abends, f4/KEVIN_ANTWORTEN.md): am eigenen gezaehmten Baeren "Open its inventory"
-- (Inventar-Fenster, client/ISUI/BanditsNPCBearInvWindow.lua -- ansehen geht immer) und, solange er keine Packtaschen traegt und du welche
-- dabei hast (B.CFG.bagType "NPCCrew.BearPacks"), "Put packs on the cub/bear": hingehen + Zeitaktion BanditsNPCBearPutAction mit mode "bag"
-- (U.InvPacksOn, client/BanditsNPCBearInvClient.lua). Grau mit Grund (Junges zu klein, faehrt mit, nicht geladen); ob es gilt, entscheidet
-- der Schreiber in complete() (B.InvPutComplete).
--
-- Das Menue BIETET nur AN. Es stellt Zeitaktionen an (Fuettern, Streicheln, Koeder) bzw. schickt eine Bitte (Koederplatz
-- aufgeben); ob etwas gilt, entscheidet der Schreiber in complete() bzw. in B.Handle (Einzelspieler: dasselbe Programm,
-- Mehrspieler: der Server). Die grauen Punkte sind nur eine Vorpruefung mit denselben Regel-Funktionen des Kerns
-- (B.CheckFeed, B.CheckPet, B.CheckBait) auf der Sicht des Spielers; lehnt der Schreiber trotzdem ab, kommt seine Meldung.
-- Nichts hier nimmt oder gibt einen Gegenstand. Laeuft nur beim Rechtsklick, nie je Bild.
-- K1 (Lauf baer-k1, PLAN_K1.md 2.3, 8; Kevin 13./14.11.2026): Vertrauen -100..+100 -- die Zeile "Trust" im Streichel-Tooltip traegt das Vorzeichen
-- ("Trust +12%" / "Trust -20%"); jede Futterzeile im Fuettern-Menue sagt "Fills it for about x% of its daily need." (Kevin ~02:10 "soll da stehn
-- mit prozent"; Regel des Kerns B.FoodDayPct mit item:getHungerChange(), V:client/ISUI/Animal/ISAnimalContextMenu.lua:37).
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local DROP_RANGE = 3    -- Kacheln: so nah am eigenen Koederplatz gibt es "Koederplatz aufgeben" (Plan 6.8)
local WAKE_WAIT_MS = 5000   -- F3: so lange wartet Fuettern / Traenken hoechstens darauf, dass ein schlafender Baer aufsteht
-- F3: Phasen des Ruhe-Treibers, in denen er gerade aufsteht (client/BanditsNPCBearPose.lua)
local RISING = { standup = true, wakeup = true, wakealarm = true, wakecurl = true, curlout = true }

-- ---------------------------------------------------------------------------
-- Kleine Helfer
-- ---------------------------------------------------------------------------

-- Tooltip an einem Menuepunkt. Form: client/ISUI/Animal/ISAnimalContextMenu.lua:161-163 (addToolTip :161, setName :162),
-- client/ISUI/ISWorldObjectContextMenu.lua:271-273 (description).
local function setTip(option, name, text)
    local tip = ISWorldObjectContextMenu.addToolTip()
    if name then tip:setName(name) end
    if text then tip.description = text end
    option.toolTip = tip
    return tip
end

-- Grauer Punkt mit Grund: ISAnimalContextMenu.lua:160-163.
local function setGray(option, text)
    option.notAvailable = true
    setTip(option, nil, text)
end

-- Die Sicht des Spielers, wenn sie von diesem Spiel ist (sonst nil: dann wird nichts vorgeprueft, der Schreiber entscheidet).
local function viewMe()
    if not U.Fresh or not U.Fresh() then return nil end
    return B.View.me
end

-- Der n-te Menuepunkt mit diesem Namen. Vanilla legt je angeklicktem Tier einen Punkt mit animal:getFullName() an
-- (ISAnimalContextMenu.lua:140-141); zwei Junge heissen gleich. Der erste geht ueber Vanillas eigene Suche
-- (context:getOptionFromName, client/Tutorial/Tutorial1.lua:131), ab dem zweiten dieselbe Schleife mit Zaehler
-- (context.options ist eine Lua-Tabelle, client/ISUI/ISContextMenu.lua:889-895).
local function nthOption(context, name, n)
    if n <= 1 then return context:getOptionFromName(name) end
    local seen = 0
    for _, opt in ipairs(context.options) do
        if opt.name == name then
            seen = seen + 1
            if seen == n then return opt end
        end
    end
    return nil
end

-- ---------------------------------------------------------------------------
-- F2 (PLAN_F2.md 2.5 Nr. 1, 4.6): Verband. U.BestBandage(player) = der saubere Verband mit der hoechsten Staerke im Inventar (auch in
-- Taschen) und seine Staerke, sonst nil, 0. Sauber wie Vanilla: string.match(item:getType(), "Dirty") (V:shared/TimedActions/
-- ISApplyBandage.lua:113); Verband ueberhaupt: item:isCanBandage() (V:client/ISUI/ISInventoryPaneContextMenu.lua:169) und
-- item:getBandagePower() > 0 (V:client/XpSystem/ISUI/ISHealthPanel.lua:1154). Suche: inv:getAllEvalRecurse(fn), :size(), :get(i)
-- (V:client/ISUI/Animal/ISAnimalContextMenu.lua:33-53, Form S:shared/BanditsNPCBearFood.lua B.FoodList). Nur auf Klick bzw. im 1-s-Takt
-- des offenen Baeren-Fensters, nie je Bild.
-- ---------------------------------------------------------------------------
local function cleanBandage(item)
    if not item:isCanBandage() then return false end
    if item:getBandagePower() <= 0 then return false end
    return string.match(item:getType(), "Dirty") == nil
end

function U.BestBandage(player)
    if not player then return nil, 0 end
    local inv = player:getInventory()
    if not inv then return nil, 0 end
    local found = inv:getAllEvalRecurse(cleanBandage)
    if not found then return nil, 0 end
    local best, bestP = nil, 0
    for i = 0, found:size() - 1 do
        local item = found:get(i)
        local pw = item:getBandagePower()
        if pw > bestP then best, bestP = item, pw end
    end
    return best, bestP
end

-- Ist dieser Sicht-Eintrag mein gezaehmter Baer? (U.WinMine, client/BanditsNPCBearWinData.lua; fehlt die Datei: ueber den Spielerschluessel)
local function ownTame(playerObj, v)
    if type(v) ~= "table" or v.id == nil or v.st ~= "tame" then return false end
    if U.WinMine then return U.WinMine(v) == true end
    return v.owner ~= nil and v.owner == B.PlayerKey(playerObj)
end

-- Hinweis ueber der Figur. HaloTextHelper.addBadText(Spieler, Text): V:client/ISUI/ISWorldObjectContextMenu.lua:1038.
local function bad(playerObj, text)
    HaloTextHelper.addBadText(playerObj, text)
end

-- U.MendAsk(player, v) (PLAN_F2.md 2.5 Nr. 4): hingehen, den besten sauberen Verband bei Bedarf aus der Tasche holen, dann die Zeitaktion.
-- Reihenfolge wie Vanilla V:client/ISUI/ISWorldObjectContextMenu.lua:426-428 (walkAdj leert die Warteschlange, transferIfNeeded und die
-- Aktion kommen danach hinein). Nur am eigenen gezaehmten Baeren mit lebender Kopie (U.CubObj). Nimmt nichts: das tut der Schreiber in
-- complete(). Rueckgabe true, wenn angestellt.
function U.MendAsk(playerObj, v)
    if not playerObj or not ownTame(playerObj, v) then return false end
    local a = U.CubObj and U.CubObj(v.id) or nil
    if a == nil or v.ride == true then
        bad(playerObj, U.TB("UI_BN_Bear_Why_OutOfReach", v.bd))
        return false
    end
    local item = U.BestBandage(playerObj)
    if item == nil then
        bad(playerObj, U.T("UI_BN_Bear_Why_NoBandage"))
        return false
    end
    local sq = a:getSquare()                                        -- ISAnimalContextMenu.lua:90
    if not sq then return false end
    if luautils.walkAdj(playerObj, sq) then                         -- ISWorldObjectContextMenu.lua:426
        ISWorldObjectContextMenu.transferIfNeeded(playerObj, item)  -- :427
        ISTimedActionQueue.add(BanditsNPCBearMendAction:new(playerObj, a, item))     -- Form :428 / ISAnimalContextMenu.lua:94
    end
    return true
end

-- U.HelpAsk(player, v) (PLAN_F2.md 2.5 Nr. 5): hingehen, dann die Zeitaktion "Aufhelfen". Nur am eigenen gezaehmten Baeren.
function U.HelpAsk(playerObj, v)
    if not playerObj or not ownTame(playerObj, v) then return false end
    local a = U.CubObj and U.CubObj(v.id) or nil
    if a == nil or v.ride == true then
        bad(playerObj, U.TB("UI_BN_Bear_Why_OutOfReach", v.bd))
        return false
    end
    local sq = a:getSquare()
    if not sq then return false end
    if luautils.walkAdj(playerObj, sq) then                         -- ISAnimalContextMenu.lua:90 (Form wie onPet unten)
        ISTimedActionQueue.add(BanditsNPCBearHelpAction:new(playerObj, a))
    end
    return true
end

-- ---------------------------------------------------------------------------
-- F3 (PLAN_F3.md 5.3; Kevin 13.11.2026 Antwort 6e): Fuettern / Traenken wecken einen schlafenden Baeren sanft.
-- wakeAsk: schlaeft der EIGENE Baer laut Sicht, eine Bitte "Wake" { id } an den Schreiber (B.Ask: Einzelspieler B.Handle direkt,
-- Mehrspieler sendClientCommand; der Schreiber prueft Besitz und Typ selbst). Nur auf Klick.
-- U.WakeWait(action): fuer waitToStart der Fuetter- und der Traenk-Aktion (shared/TimedActions) -- true, solange gewartet werden soll:
-- der Baer schlief beim ersten Blick laut Sicht und schlaeft noch oder steht gerade auf (U.PosePhase), hoechstens WAKE_WAIT_MS seit dem
-- ersten Blick. Schlief er nie: sofort false. So startet die Aktion nie in das Aufsteh-Bild hinein und haengt nie.
-- getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485.
-- ---------------------------------------------------------------------------
local function wakeAsk(playerObj, animal)
    local v = nil
    if B.ViewOf and viewMe() then v = B.ViewOf(animal) end
    if type(v) ~= "table" or v.id == nil or v.slp ~= true or not ownTame(playerObj, v) then return end
    B.Ask(playerObj, "Wake", { id = v.id })
end

function U.WakeWait(action)
    local a = type(action) == "table" and action.animal or nil
    if a == nil or not B.ViewOf then return false end
    local v = B.ViewOf(a)
    if type(v) ~= "table" then return false end
    local now = getTimestampMs()
    if action.wakeAt == nil then
        if v.slp ~= true then return false end
        action.wakeAt = now
    end
    if now < action.wakeAt or now - action.wakeAt >= WAKE_WAIT_MS then return false end
    if v.slp == true then return true end
    local ph = nil
    if U.PosePhase then ph = U.PosePhase(v.id) end
    return ph ~= nil and RISING[ph] == true
end

-- ---------------------------------------------------------------------------
-- Klick-Handler: stellen nur Aktionen an
-- ---------------------------------------------------------------------------

-- Fuettern (Plan 5.3). Reihenfolge ist Absicht: ZUERST das Futter in die Hand, DANN hingehen -- mit Futter in der Hand haelt der
-- Takt des Schreibers das Junge fest. luautils.walkAdj leert ohne drittes Argument die Warteschlange
-- (shared/luautils.lua:119-122) und wuerde das Anlegen wieder streichen; deshalb erst selbst leeren, dann mit keepActions gehen.
local function onFeed(playerObj, animal, food)
    if not playerObj or not animal or not food then return end
    if not animal:isExistInTheWorld() then return end               -- ISAnimalContextMenu.lua:88
    local sq = animal:getSquare()                                   -- :90
    if not sq then return end
    wakeAsk(playerObj, animal)                                      -- F3: schlaeft er, vorher sanft wecken
    ISTimedActionQueue.clear(playerObj)                             -- client/ISUI/ISWorldObjectContextMenu.lua:1056
    -- equip holt das Stueck bei Bedarf selbst aus der Tasche (transferIfNeeded, ISWorldObjectContextMenu.lua:2606-2612)
    ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)    -- ISAnimalContextMenu.lua:93
    if luautils.walkAdj(playerObj, sq, true) then                   -- ISWorldObjectContextMenu.lua:2564 (keepActions)
        ISTimedActionQueue.add(BanditsNPCBearFeedAction:new(playerObj, animal, food))   -- ISAnimalContextMenu.lua:94
    end
end

-- F3 (PLAN_F3.md 5.2): Wasser geben -- hingehen, den Behaelter bei Bedarf aus der Tasche holen, dann die Zeitaktion. Reihenfolge wie
-- U.MendAsk oben (V:client/ISUI/ISWorldObjectContextMenu.lua:426-428: walkAdj leert die Warteschlange, transferIfNeeded und die Aktion
-- kommen danach hinein). Der Behaelter wird NICHT in die Hand gelegt (Vanilla ruestet ihn aus, ISAnimalContextMenu.lua:498 -- hier bleibt
-- die Waffe in der Hand; das Bild in der Hand setzt die Aktion selbst, setOverrideHandModels). Nimmt nichts: das tut der Schreiber in
-- complete() (B.DrinkComplete). Schlaeft der Baer, vorher die Bitte "Wake".
local function onWater(playerObj, animal, item)
    if not playerObj or not animal or not item then return end
    if not animal:isExistInTheWorld() then return end               -- ISAnimalContextMenu.lua:494
    local sq = animal:getSquare()                                   -- :496
    if not sq then return end
    wakeAsk(playerObj, animal)
    if luautils.walkAdj(playerObj, sq) then                         -- :496
        ISWorldObjectContextMenu.transferIfNeeded(playerObj, item)  -- ISWorldObjectContextMenu.lua:427
        ISTimedActionQueue.add(BanditsNPCBearDrinkAction:new(playerObj, animal, item))  -- Form ISAnimalContextMenu.lua:499
    end
end

-- Streicheln (Plan 5.4): hingehen, dann die Aktion.
local function onPet(playerObj, animal)
    if not playerObj or not animal then return end
    if not animal:isExistInTheWorld() then return end
    local sq = animal:getSquare()
    if not sq then return end
    if luautils.walkAdj(playerObj, sq) then                         -- ISAnimalContextMenu.lua:90
        ISTimedActionQueue.add(BanditsNPCBearPetAction:new(playerObj, animal))
    end
end

-- Koeder auslegen (Plan 5.2): hingehen, Stueck bei Bedarf aus der Tasche holen, dann die Aktion. Reihenfolge wie Vanillas
-- Fuettern (ISAnimalContextMenu.lua:90-94): walkAdj leert die Warteschlange, alles Weitere kommt danach hinein.
local function onBait(playerObj, food, sq)
    if not playerObj or not food or not sq then return end
    if luautils.walkAdj(playerObj, sq) then
        ISWorldObjectContextMenu.transferIfNeeded(playerObj, food)  -- ISAnimalContextMenu.lua:577
        ISTimedActionQueue.add(BanditsNPCBearBaitAction:new(playerObj, food, sq:getX(), sq:getY(), sq:getZ()))
    end
end

-- Koederplatz aufgeben: eine Bitte an den Schreiber, der den Besitz selbst prueft.
local function onBaitDrop(playerObj, baitId)
    if not playerObj or baitId == nil then return end
    B.Ask(playerObj, "BaitDrop", { id = baitId })
end

-- Folgen / Bleiben (B1b, Plan 1.1): nur eine Bitte. Ob sie gilt (Besitz, Fahrzeug, Abstand), entscheidet der Schreiber
-- (Einzelspieler: B.Handle direkt; Mehrspieler: sendClientCommand). Die Tabelle ist nie leer (Plan 5.5).
local function onMode(playerObj, id, mode)
    if not playerObj or id == nil then return end
    if mode ~= "follow" and mode ~= "stay" then return end
    B.Ask(playerObj, "Mode", { id = id, mode = mode })
end

-- Umbenennen (B1b, Plan 3.1): das Eingabefenster (client/ISUI/BanditsNPCBearNameBox.lua) schickt die Bitte "Rename".
local function onName(playerObj, v)
    if not playerObj or not v or not U.AskName then return end
    U.AskName(playerObj, v)
end

-- "Call to me" (B1c, PLAN_B1C.md 1.5): nur eine Bitte. Besitz, Zustand, Fahrzeug, Abklingzeit und freie Kachel prueft der Schreiber
-- (Einzelspieler: B.Handle direkt; Mehrspieler: sendClientCommand, Rolle user genuegt). Die Tabelle ist nie leer.
local function onCall(playerObj, id)
    if not playerObj or id == nil then return end
    B.Ask(playerObj, "Call", { id = id })
end

-- Futter hinhalten (B1b, Plan 3.2): das Stueck NUR in die Hand nehmen -- kein Hingehen, die Warteschlange bleibt. equip holt es
-- bei Bedarf selbst aus der Tasche (transferIfNeeded) und stellt ISEquipWeaponAction an (client/ISUI/ISWorldObjectContextMenu.lua:2594-2622);
-- derselbe Aufruf mit Futter: client/ISUI/Animal/ISAnimalContextMenu.lua:93. Danach greift die Regel des Schreibers "Futter in
-- der Hand und stillstehen -> das Junge kommt naeher". Kein Gegenstand wird erzeugt oder vernichtet.
local function onHold(playerObj, food)
    if not playerObj or not food then return end
    ISWorldObjectContextMenu.equip(playerObj, playerObj:getPrimaryHandItem(), food, true, false)
end

-- ---------------------------------------------------------------------------
-- Tier-Menue
-- ---------------------------------------------------------------------------

-- Tooltip der freien Punkte: Stand des Balkens und der Hinweis auf die Mischung. F3: am GEZAEHMTEN Baeren steht oben der Wert von jetzt
-- aus der Sicht (field "hun" -> "Hunger 35%", "tru" -> "Trust 62%"; Schluessel der Schild-Zahlen), wenn die Sicht ihn traegt.
local NOW_KEY = { hun = "UI_BN_Bear_Tag_Hunger", tru = "UI_BN_Bear_Tag_Trust" }
local function tipStatus(option, v, field)
    local name = nil
    if v and type(v.tame) == "number" and v.st ~= "tame" then
        name = U.T("UI_BN_Bear_Hud_Taming", math.floor(v.tame))
    elseif v and v.st == "tame" and field ~= nil and NOW_KEY[field] and type(v[field]) == "number" then
        local n = math.floor(v[field] + 0.5)
        if field == "tru" then
            -- K1: Vertrauen mit Vorzeichen (ganze Zahl, wie der Kopf-Balken)
            if n > 0 then n = "+" .. string.format("%d", n) elseif n < 0 then n = "-" .. string.format("%d", -n) else n = "0" end
        end
        name = U.T(NOW_KEY[field], n)
    end
    setTip(option, name, U.T("UI_BN_Bear_Tip_Mix"))
end

-- K1 (PLAN_K1.md 8): Text "x" fuer "Fills it for about x%". U.DayPctText(pct): ab 10 ganz, darunter eine Nachkommastelle, nie unter 0,1
-- (string.format wie U.Kg); nil = nichts. U.FoodDayText(v, hungerChange): so viel Prozent seines Tagesbedarfs macht EIN Stueck mit diesem
-- Hunger-Wert satt (Regel des Kerns B.FoodDayPct; ohne sie B.MealsOf x B.MealPct mit dem Sicht-Feld meal). Nur Rechnen; auch das Inventar-Fenster.
function U.DayPctText(pct)
    pct = tonumber(pct)
    if pct == nil or pct ~= pct or pct <= 0 then return nil end
    if pct >= 10 then return string.format("%d", math.floor(pct + 0.5)) end
    if pct < 0.1 then pct = 0.1 end
    return string.format("%.1f", math.floor(pct * 10 + 0.5) / 10)
end

function U.FoodDayText(v, hungerChange)
    local pct = nil
    if B.FoodDayPct then
        pct = tonumber(B.FoodDayPct(v, hungerChange))
    elseif B.MealsOf and B.MealPct then
        pct = (tonumber(B.MealsOf(hungerChange)) or 0) * (tonumber(B.MealPct(v)) or 0)
    end
    return U.DayPctText(pct)
end

-- Text einer Futterzeile (Fuettern und Futter hinhalten): Lieblingsfutter / normal / nur ein Happen, dazu die Anzahl.
local function foodLabel(row)
    local label
    if row.class == "fav" then
        label = U.T("UI_BN_Bear_Food_Fav", row.name)
    elseif row.class == "snack" then
        label = U.T("UI_BN_Bear_Food_Snack", row.name)
    else
        label = U.T("UI_BN_Bear_Food_Ok", row.name)
    end
    if type(row.count) == "number" and row.count > 1 then
        label = label .. " (" .. tostring(row.count) .. ")"
    end
    return label
end

local function addFeed(menu, playerObj, animal, v, me, key)
    local feedOpt = menu:addOption(U.T("UI_BN_Bear_Menu_Feed"), nil, nil)       -- ISAnimalContextMenu.lua:272 (Punkt mit Untermenue)
    if v and me then
        local ok, whyKey, whyVal = B.CheckFeed(v, key, me, B.Now())
        if not ok then
            setGray(feedOpt, U.WhyText(whyKey, whyVal, v.bd))
            return
        end
    end
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    if not rows or #rows == 0 then
        setGray(feedOpt, U.T("UI_BN_Bear_Menu_NoFood"))
        return
    end
    tipStatus(feedOpt, v, "hun")
    local sub = ISContextMenu:getNew(menu)                                      -- ISAnimalContextMenu.lua:273
    menu:addSubMenu(feedOpt, sub)                                               -- :274
    for _, row in ipairs(rows) do
        local opt = sub:addOption(foodLabel(row), playerObj, onFeed, animal, row.item)      -- ISAnimalContextMenu.lua:280
        -- K1 (PLAN_K1.md 8): "Fills it for about x% of its daily need." je Futter (nur mit Sicht -- fremde / ungezaehmte Baeren ohne Zeile)
        if v and v.st == "tame" then
            local txt = U.FoodDayText and U.FoodDayText(v, row.item:getHungerChange())     -- ISAnimalContextMenu.lua:37
            if txt then setTip(opt, nil, U.T("UI_BN_Bear_Food_DayPct", txt)) end
        end
    end
end

local function addPet(menu, playerObj, animal, v, me, key)
    local petOpt = menu:addOption(U.T("UI_BN_Bear_Menu_Pet"), playerObj, onPet, animal)     -- ISAnimalContextMenu.lua:287
    petOpt.iconTexture = getTexture("media/ui/AnimalActions_Pet.png")                       -- :288
    if v and me then
        local ok, whyKey, whyVal = B.CheckPet(v, key, me, B.Now())
        if not ok then
            setGray(petOpt, U.WhyText(whyKey, whyVal, v.bd))
            return
        end
    end
    tipStatus(petOpt, v, "tru")
end

-- F3 (PLAN_F3.md 5.2): "Give water to the cub/bear" am eigenen gezaehmten Baeren -- Untermenue der Wasser-Behaelter wie Vanilla:
-- playerObj:getInventory():getAllWaterFluidSources(true) V:client/ISUI/Animal/ISAnimalContextMenu.lua:466, :isEmpty() :472, :size() /
-- :get(i) :483-484, Beschriftung item:getName() .. " (" .. round(item:getFluidContainer():getAmount() * 1000, 2) .. " mL)" :485 (round:
-- Definition V:shared/env.lua:1), gleiche Beschriftung nur einmal :486-489; Punkt mit Untermenue :468 / :480-481, Bild :469, grau ohne Wasser
-- mit Vanillas Text :473-476. Grau mit Grund aus der Sicht ueber die Regel des Kerns B.CheckDrink(Eintrag, Spielerschluessel) -> ok,
-- Grund (faehrt mit, am Boden, nicht durstig); fehlt sie (Kern ohne F3), bleibt der Punkt frei und der Schreiber entscheidet.
-- Existenz-Riegel wie "Bandage": ohne die Zeitaktion kein Punkt. Der Tooltip nennt den Durst von jetzt.
local function addWater(menu, playerObj, animal, v, key)
    if BanditsNPCBearDrinkAction == nil then return end
    local opt = menu:addOption(U.TB("UI_BN_Bear_Menu_Water", v.bd), nil, nil)
    opt.iconTexture = getTexture("Item_WaterDrop.png")
    if B.CheckDrink then
        local ok, whyKey, whyVal = B.CheckDrink(v, key)
        if not ok then
            setGray(opt, U.WhyText(whyKey, whyVal, v.bd))
            return
        end
    end
    local items = playerObj:getInventory():getAllWaterFluidSources(true)
    if items:isEmpty() then
        opt.notAvailable = true
        local tip = ISWorldObjectContextMenu.addToolTip()
        tip:setName(getText("ContextMenu_NoWaterItemFound"))
        opt.toolTip = tip
        return
    end
    local name = nil
    if type(v.thr) == "number" then name = U.T("UI_BN_Bear_Tag_Thirst", math.floor(v.thr + 0.5)) end
    setTip(opt, name, U.T("UI_BN_Bear_Menu_WaterTip"))
    local sub = ISContextMenu:getNew(menu)
    menu:addSubMenu(opt, sub)
    local seen = {}
    for i = 0, items:size() - 1 do
        local item = items:get(i)
        local text = item:getName() .. " (" .. round(item:getFluidContainer():getAmount() * 1000, 2) .. " mL)"
        if not seen[text] then
            sub:addOption(text, playerObj, onWater, animal, item)               -- Form ISAnimalContextMenu.lua:487
            seen[text] = true
        end
    end
end

-- Zustand des Jungen laut Sicht (Regel des Kerns B.ModeOf, Plan 5.3: nil und alles andere heisst "stay"; F1: follow / stay / sit /
-- roam, PLAN_F1.md 7.2).
local function modeOf(v)
    local f = B.ModeOf
    if f then return f(v) end
    local m = v.mode
    if m == "follow" or m == "sit" or m == "roam" then return m end
    return "stay"
end

-- Umschalter (Plan 1.1): bei "stay" steht "Follow me", bei "follow" "Stay here" -- nie beide. Grau nur mit Grund: im Fahrzeug
-- kann das Junge nicht folgen (Vorpruefung; alles andere entscheidet der Schreiber). getVehicle() am Spieler:
-- client/ISUI/Hutch/ISHutchMenu.lua:8.
local function addMode(menu, playerObj, v)
    if modeOf(v) == "follow" then
        local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Stay"), playerObj, onMode, v.id, "stay")
        if v.dn == true then
            setGray(opt, U.TB("UI_BN_Bear_Why_Down", v.bd))         -- F2: am Boden nimmt der Schreiber keinen Befehl an
            return
        end
        setTip(opt, nil, U.T("UI_BN_Bear_Menu_StayTip"))
        return
    end
    local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Follow"), playerObj, onMode, v.id, "follow")
    if v.dn == true then
        setGray(opt, U.TB("UI_BN_Bear_Why_Down", v.bd))
        return
    end
    if playerObj:getVehicle() then
        setGray(opt, U.T("UI_BN_Bear_Why_InCar"))
        return
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_FollowTip"))
end

-- "Name the cub" (Plan 3.1): kein Graufall. B1e: beim grossen Koerper "Name the bear".
local function addName(menu, playerObj, v)
    menu:addOption(U.TB("UI_BN_Bear_Menu_Name", v.bd), playerObj, onName, v)
end

-- Rest der Call-Abklingzeit in ganzen Minuten (aufgerundet, mindestens 1), 0 = bereit. Die Sicht traegt den Rest in Sekunden
-- (callWait, nur fuer den Besitzer) zum Zeitpunkt ihres Baus; abgezogen wird die Zeit seit ihrer Ankunft (U.viewAt). Uhr
-- rueckwaerts: so, als waere die Sicht gerade angekommen. getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485.
local function callWaitMinutes(v)
    local left = tonumber(v.callWait)
    if left == nil or left <= 0 then return 0 end
    local ms = left * 1000
    local at = U.viewAt
    if type(at) == "number" then
        local now = getTimestampMs()
        if now >= at then ms = ms - (now - at) end
    end
    if ms <= 0 then return 0 end
    local m = math.ceil(ms / 60000)
    if m < 1 then m = 1 end
    return m
end

-- "Call to me" (B1c, Plan 1.5): nur am eigenen gezaehmten Jungen (der Aufrufer prueft Besitz und Zustand), nie an einem
-- mitfahrenden. Grau mit Grund nur aus der Sicht: im Fahrzeug, Abklingzeit laeuft. Der Tooltip nennt die Abklingzeit (seit der
-- Sandbox-Kuerzung der feste Wert B.CFG.callCoolMin; dieselbe Uhr gilt fuer den Aussehen-Knopf im Fenster).
-- getVehicle() am Spieler: client/ISUI/Hutch/ISHutchMenu.lua:8.
local function addCall(menu, playerObj, v)
    if v.ride == true then return end
    local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Call"), playerObj, onCall, v.id)
    if playerObj:getVehicle() then
        setGray(opt, U.T("UI_BN_Bear_Why_InCar"))
        return
    end
    local wait = callWaitMinutes(v)
    if wait > 0 then
        setGray(opt, U.TB("UI_BN_Bear_Why_CallWait", v.bd, wait))
        return
    end
    -- Sandbox-Kuerzung (PLAN_AUSSEHEN.md 9.3): die Abklingzeit ist ein fester Wert des Kerns (B.CFG.callCoolMin, Vorgabe 5)
    local mins = tonumber(B.CFG and B.CFG.callCoolMin)
    if mins == nil then mins = 5 end
    setTip(opt, nil, U.TB("UI_BN_Bear_Menu_CallTip", v.bd, math.floor(mins)))
end

-- F1 (PLAN_F1.md 3.3): "Bear window" -- oeffnet das Baeren-Fenster dieses Baeren (U.WinOpen, client/ISUI/BanditsNPCBearWindow.lua).
local function onWindow(playerObj, id)
    if not playerObj or id == nil or not U.WinOpen then return end
    U.WinOpen(playerObj, id)
end

local function addWindow(menu, playerObj, v)
    if not U.WinOpen then return end
    local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Window"), playerObj, onWindow, v.id)    -- Form wie :241 / ISAnimalContextMenu.lua:287
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_WindowTip"))
end

-- F4 (PLAN_F4.md 7): "Open its inventory" (U.InvOpen) und "Put packs on the cub/bear" (U.InvPacksOn mit Hingehen). Existenz-Riegel: ohne
-- Inventar-Fenster bzw. Put-Aktion kein Punkt. "Put packs on" nur mit Packtaschen im Inventar und ohne angelegte Taschen (Sicht bag).
local function onInvOpen(playerObj, id)
    if U.InvOpen then U.InvOpen(playerObj, id) end
end

local function onPacksOn(playerObj, v)
    if U.InvPacksOn then U.InvPacksOn(playerObj, v, true) end
end

local function addInv(menu, playerObj, v)
    if U.InvOpen then
        local opt = menu:addOption(U.T("UI_BN_Bear_Menu_Inv"), playerObj, onInvOpen, v.id)    -- Form wie addWindow / ISAnimalContextMenu.lua:287
        setTip(opt, nil, U.T("UI_BN_Bear_Win_InvTip"))
    end
    if not U.InvPacksOn or not U.InvPacksItem or BanditsNPCBearPutAction == nil then return end
    if v.bag == true or U.InvPacksItem(playerObj) == nil then return end
    local opt = menu:addOption(U.TB("UI_BN_Bear_Menu_PacksOn", v.bd), playerObj, onPacksOn, v)
    local why = U.InvPacksWhy(playerObj, v, true, true)
    if why then
        setGray(opt, why)
        return
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Inv_PutOnTip", math.floor(tonumber(B.CFG and B.CFG.bagAdd) or 150)))     -- Rueckfall 150 (P11)
end

-- F2 (PLAN_F2.md 2.5, 3.2, 4.6): Klick -> U.MendAsk / U.HelpAsk (hingehen, Zeitaktion). Der Sicht-Eintrag wird beim Klick frisch geholt.
local function onMend(playerObj, v)
    if U.MendAsk then U.MendAsk(playerObj, v) end
end

local function onHelp(playerObj, v)
    if U.HelpAsk then U.HelpAsk(playerObj, v) end
end

-- Stunden fuer einen Text: ganze Stunden, mindestens 1 (5,2 -> 5; 0,4 -> 1).
local function hoursOf(h)
    local n = math.floor(tonumber(h) or 0)
    if n < 1 then n = 1 end
    return n
end

-- Grund, warum "Bandage" gerade nicht geht (aus der Sicht), sonst nil -- dieselben Gruende wie der Knopf im Fenster (Vorpruefung; der
-- Schreiber prueft in complete() alles noch einmal, PLAN_F2.md 2.5 Nr. 3). item = bester sauberer Verband (oder nil).
function U.MendWhy(v, item)
    if type(v) ~= "table" then return nil end
    if v.ride == true then return U.TB("UI_BN_Bear_Why_Riding", v.bd) end
    if v.st ~= "tame" or v.ld ~= true then return U.TB("UI_BN_Bear_Why_OutOfReach", v.bd) end
    -- Nachbesserung F2 B7: "Verband heilt 0" -> grau mit Grund (der Schreiber lehnt ebenso ab, ohne Verbrauch). Sandbox-Kuerzung
    -- (PLAN_AUSSEHEN.md 9.3): fester Wert B.CFG.bandageHeal (6) -- mit der Vorgabe unerreichbar, bleibt fuer einen geaenderten Wert
    if (tonumber(B.CFG and B.CFG.bandageHeal) or 1) <= 0 then return U.T("UI_BN_Bear_Why_BandageOff") end
    if item == nil then return U.T("UI_BN_Bear_Why_NoBandage") end
    if type(v.bnd) == "number" and v.bnd > 0 then return U.TB("UI_BN_Bear_Why_Bandaged", v.bd, hoursOf(v.bnd)) end
    if type(v.hp) == "number" and v.hp >= 100 then return U.TB("UI_BN_Bear_Why_Healthy", v.bd) end
    return nil
end

-- "Bandage the cub/bear" (immer, auch am Boden -- der Verband wirkt dort, PLAN_F2.md 2.4) und am Boden zuerst "Help up the cub/bear".
-- Existenz-Riegel wie "Bear window" (U.WinOpen): ohne die Zeitaktion (shared/TimedActions/BanditsNPCBear{Help,Mend}Action.lua) kein Punkt.
local function addCare(menu, playerObj, v)
    if v.dn == true and BanditsNPCBearHelpAction ~= nil then
        local hopt = menu:addOption(U.TB("UI_BN_Bear_Menu_HelpUp", v.bd), playerObj, onHelp, v)
        setTip(hopt, nil, U.T("UI_BN_Bear_Win_HelpUpTip"))
    end
    if BanditsNPCBearMendAction == nil then return end
    local item = U.BestBandage(playerObj)
    local opt = menu:addOption(U.TB("UI_BN_Bear_Menu_Bandage", v.bd), playerObj, onMend, v)
    local why = U.MendWhy(v, item)
    if why then
        setGray(opt, why)
        return
    end
    local hours = tonumber(B.CFG and B.CFG.bandageHours)            -- Sandbox-Kuerzung: fester Wert des Kerns (Vorgabe 8)
    if hours == nil then hours = 8 end
    setTip(opt, item:getDisplayName(), U.T("UI_BN_Bear_Menu_BandageTip", item:getDisplayName(), math.floor(hours))   -- getDisplayName:
        .. " " .. U.T("UI_BN_Bear_Win_BandageTip"))                 -- S:shared/BanditsNPCBearFood.lua B.FoodList
end

-- Ein Junges: Vanillas Untermenue suchen (fehlt es, auf die oberste Ebene), "Kill" entfernen, eigene Punkte anhaengen.
local function cubMenu(context, playerObj, animal, name, nth)
    local menu = context
    local opt = nthOption(context, name, nth)
    if opt and opt.subOption then
        local sub = context:getSubMenu(opt.subOption)       -- client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:41
        if sub then
            menu = sub
            -- Vanilla bietet "Kill" fuer jedes nicht wilde Tier an (ISAnimalContextMenu.lua:307-324); am Jungen blenden wir es
            -- aus. removeOptionByName ist reines Lua (client/ISUI/ISContextMenu.lua:1016).
            sub:removeOptionByName(getText("ContextMenu_KillAnimal"))           -- Text: ISAnimalContextMenu.lua:310
        end
    end
    local me = viewMe()
    local v = nil
    if me then v = B.ViewOf(animal) end
    if not v then
        -- Der Client kennt dieses Junge (noch) nicht: Punkte bleiben frei, der Schreiber entscheidet; Sicht nachfragen.
        if U.AskHello then U.AskHello(playerObj) end
    end
    local key = B.PlayerKey(playerObj)
    addFeed(menu, playerObj, animal, v, me, key)
    addPet(menu, playerObj, animal, v, me, key)
    -- B1b: nur am eigenen gezaehmten Jungen und nur, wenn die Sicht es kennt (Fremde sehen die Punkte gar nicht, Plan 1.1, 1.6).
    if v and v.id ~= nil and v.st == "tame" and key ~= nil and v.owner == key then
        -- F3: "Give water" (PLAN_F3.md 5.2) gleich nach Fuettern / Streicheln
        addWater(menu, playerObj, animal, v, key)
        addMode(menu, playerObj, v)
        addName(menu, playerObj, v)
        -- B1c: "Call to me" (Plan 1.5)
        addCall(menu, playerObj, v)
        -- F1: "Bear window" (PLAN_F1.md 3.3)
        addWindow(menu, playerObj, v)
        -- F4: "Open its inventory", "Put packs on" (PLAN_F4.md 7)
        addInv(menu, playerObj, v)
        -- F2: "Help up" (am Boden) und "Bandage" (PLAN_F2.md 2.5, 3.2)
        addCare(menu, playerObj, v)
    end
end

-- ---------------------------------------------------------------------------
-- F1B (PLAN_F1B.md 2.4): Vanillas Tier-Radial an jedem Baeren unserer Art ohne "Kill" -- wie das Rechtsklick-Menue (cubMenu oben).
-- Das Radial ist eine Lua-Tabelle: menu.slices mit { text, texture, command = { fn, a1..a6 } }, menu:clear(), menu:addSlice(...)
-- (V:client/ISUI/ISRadialMenu.lua:37-53; Vanilla liest slices selbst V:client/ISUI/ISFirearmRadialMenu.lua:267-269). Ein removeSlice gibt
-- es nicht -- also neu aufbauen, nur wenn etwas wegfiel. Kill erkennt man an command[1] == AnimalContextMenu.onKillAnimal
-- (V:client/ISUI/Animal/ISAnimalContextMenu.lua:1175, Funktion :1079). Laeuft im selben Lua-Aufruf wie Vanillas Aufbau, also bevor ein
-- Bild gezeichnet wird; deckt Tastatur (V:client/ISUI/ISUIHandler.lua:56, :93) und Controller (V:client/ISUI/ISDPadWheels.lua:101),
-- weil beide ueber das Tabellenfeld rufen. Vorbild einer Huelle (gelernt, nicht kopiert): NC:client/BanditsNPCSleep.lua:380-406.
-- ---------------------------------------------------------------------------
local function noKill(menu)
    local kill = AnimalContextMenu.onKillAnimal
    if kill == nil then return end
    local keep = {}
    local dropped = false
    for i = 1, #menu.slices do
        local sl = menu.slices[i]
        local c = sl and sl.command
        if type(c) == "table" and c[1] == kill then
            dropped = true
        else
            keep[#keep + 1] = sl
        end
    end
    if not dropped then return end
    menu:clear()                                                                -- ISRadialMenu.lua:37-42
    for i = 1, #keep do
        local sl = keep[i]
        local c = sl.command or {}
        menu:addSlice(sl.text, sl.texture, c[1], c[2], c[3], c[4], c[5], c[6], c[7])   -- ISRadialMenu.lua:44-53 (Form :18-26)
    end
end

local function hookRadial()
    if U.radialHooked then return end
    if type(AnimalContextMenu) ~= "table" or type(AnimalContextMenu.showRadialMenu) ~= "function" then return end   -- Existenz-Riegel
    U.radialHooked = true
    local orig = AnimalContextMenu.showRadialMenu
    AnimalContextMenu.showRadialMenu = function(playerObj)
        local menu = nil
        if playerObj then menu = getPlayerRadialMenu(playerObj:getPlayerNum()) end   -- ISAnimalContextMenu.lua:1156-1157
        local wasOpen = menu ~= nil and menu:isReallyVisible()                       -- :1160 (dann schliesst orig nur)
        orig(playerObj)
        if wasOpen or menu == nil or not B.BodyKind or type(menu.slices) ~= "table" then return end
        local an = AnimalContextMenu.getAnimalToInteractWith(playerObj)               -- :1170
        if an and B.BodyKind(an) ~= nil then noKill(menu) end
    end
end

-- Vanillas eigenes Tier-Menue haengt am selben Ereignis (ISAnimalContextMenu.lua:1013-1017, :1235) und laedt vor uns: sein
-- Untermenue je Tier steht schon, wenn wir drankommen.
-- B1e: unser Baer ist jedes Tier, fuer das B.BodyKind (Kern, shared) "cub" oder "big" sagt -- der einzige Art-Vergleich (darin
-- animal:getAnimalType(), client/ISUI/Animal/ISAnimalUI.lua:65). Fehlt der Helfer (Kern ohne B1e), bleibt das Menue still.
local function onClickedAnimals(player, context, animals, test)
    if not B.CUB or not B.T or not B.View or not B.BodyKind then return end
    local cubs = nil
    for _, a in ipairs(animals) do                                              -- ISAnimalContextMenu.lua:1014
        if B.BodyKind(a) ~= nil then
            cubs = cubs or {}
            cubs[#cubs + 1] = a
        end
    end
    if not cubs then return end
    -- Probelauf fuer Controller: nur melden, dass es Eintraege gibt (client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81).
    if test then return ISWorldObjectContextMenu.setTest() end
    local playerObj = getSpecificPlayer(player)                                 -- ISAnimalContextMenu.lua:134
    if not playerObj then return end
    -- Je Name mitzaehlen: das zweite Junge gleichen Namens gehoert zum zweiten Vanilla-Punkt dieses Namens.
    local seen = {}
    for _, a in ipairs(cubs) do
        local name = a:getFullName()                                            -- ISAnimalContextMenu.lua:140
        seen[name] = (seen[name] or 0) + 1
        cubMenu(context, playerObj, a, name, seen[name])
    end
end

-- ---------------------------------------------------------------------------
-- Welt-Menue: Koeder
-- ---------------------------------------------------------------------------

-- Koeder-Futter im Inventar: die Zeilen der Futterliste des Kerns, die Koeder sein duerfen (Honig oder Fisch).
local function baitRows(playerObj)
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    local out = {}
    if not rows then return out end
    for _, row in ipairs(rows) do
        local ok, kind = B.IsBaitFood(row.item)
        if ok then
            row.kind = kind
            out[#out + 1] = row
        end
    end
    return out
end

local function addBaitDrop(context, playerObj, sq, view)
    local bait = view.bait
    if not bait or bait.id == nil then return false end
    if sq:getZ() ~= bait.z then return false end
    if math.abs(sq:getX() - bait.x) > DROP_RANGE or math.abs(sq:getY() - bait.y) > DROP_RANGE then return false end
    local opt = context:addOption(U.T("UI_BN_Bear_Menu_BaitDrop"), playerObj, onBaitDrop, bait.id)
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_BaitDropTip"))
    return true
end

local function addBait(context, playerObj, sq, me, rows, near)
    local opt = context:addOption(U.T("UI_BN_Bear_Menu_Bait"), nil, nil)
    if not near then
        setGray(opt, U.T("UI_BN_Bear_Bait_NotForest"))
        return
    end
    if not sq:isOutside() then                                  -- client/Foraging/ISZoneDisplay.lua:400
        setGray(opt, U.T("UI_BN_Bear_Bait_Inside"))
        return
    end
    if me then
        local ok, whyKey, whyVal = B.CheckBait(me)
        if not ok then
            setGray(opt, U.WhyText(whyKey, whyVal))
            return
        end
    end
    setTip(opt, nil, U.T("UI_BN_Bear_Menu_BaitTip"))
    local sub = ISContextMenu:getNew(context)                   -- client/ISUI/Animal/ISAnimalContextMenu.lua:48
    context:addSubMenu(opt, sub)                                -- :49
    for _, row in ipairs(rows) do
        local label = U.T("UI_BN_Bear_Food_Ok", row.name)
        if type(row.count) == "number" and row.count > 1 then
            label = label .. " (" .. tostring(row.count) .. ")"
        end
        local rowOpt = sub:addOption(label, playerObj, onBait, row.item, sq)
        setTip(rowOpt, nil, U.T("UI_BN_Bear_Menu_BaitTip"))
    end
end

-- ---------------------------------------------------------------------------
-- Welt-Menue: Futter hinhalten (B1b, Plan 3.2)
-- ---------------------------------------------------------------------------

-- Steht ein Junges mit Objekt in B.CFG.lureDist Kacheln um den Spieler, das auf sein Futter reagiert? Wie die Regel des
-- Schreibers (server keysOf): scheue (new/shy) jeder, angefuetterte nur der Gebundene, gezaehmte nur der Besitzer -- und nur,
-- solange es bleibt: ein folgendes Junges rechnet B.FollowDecide, dort spielt Futter keine Rolle (Nachbesserung B1b B6).
-- F1 (PLAN_F1.md 2.3, 2.4, 4a): gezaehmt nur im Modus "stay" (sitzend und frei herumlaufend lockt der Schreiber nicht). Gibt das
-- naechste passende Junge zurueck (fuer den Text je Koerper), sonst nil.
local function holdWanted(playerObj, key)
    if not U.CubsNear or key == nil then return nil end
    local near = U.CubsNear(playerObj, B.CFG.lureDist or 15)
    for i = 1, #near do
        local c = near[i].c
        local st = c.st
        if st == "new" or st == "shy" then return c end
        if st == "fed" and c.bond == key then return c end
        if st == "tame" and c.owner == key and modeOf(c) == "stay" then return c end
    end
    return nil
end

local function addHold(context, playerObj, c)
    local bd = c and c.bd
    local opt = context:addOption(U.TB("UI_BN_Bear_Menu_Hold", bd), nil, nil)
    local rows = B.FoodList(playerObj, B.CFG.menuFoods)
    if not rows or #rows == 0 then
        setGray(opt, U.T("UI_BN_Bear_Menu_NoFood"))
        return
    end
    setTip(opt, nil, U.TB("UI_BN_Bear_Menu_HoldTip", bd))
    local sub = ISContextMenu:getNew(context)                   -- client/ISUI/Animal/ISAnimalContextMenu.lua:48
    context:addSubMenu(opt, sub)                                -- :49
    for _, row in ipairs(rows) do
        sub:addOption(foodLabel(row), playerObj, onHold, row.item)
    end
end

local function onFillWorld(player, context, worldobjects, test)
    -- Dieselbe Tuer wie Vanillas Menues: client/ISUI/Hutch/ISHutchMenu.lua:4
    if test and ISWorldObjectContextMenu.Test then return true end
    if not B.CUB or not B.T or not B.View or not B.Opt then return end
    local playerObj = getSpecificPlayer(player)                 -- ISHutchMenu.lua:6
    if not playerObj or playerObj:getVehicle() then return end  -- ISHutchMenu.lua:8
    local sq = nil
    for _, o in ipairs(worldobjects) do                         -- ISHutchMenu.lua:11
        sq = o:getSquare()                                      -- client/ISUI/ISWorldObjectContextMenu.lua:2571
        if sq then break end
    end
    if not sq then return end

    -- Die alte Sicht eines anderen Spielstands wird nicht benutzt (U.Fresh); ohne Sicht kein Koeder-Punkt.
    local me = viewMe()
    if not me then return end
    local view = B.View

    -- Aufgeben geht immer am eigenen Platz, auch ohne Koeder in der Tasche.
    if view.bait and view.bait.id ~= nil then
        if test then
            if sq:getZ() == view.bait.z and math.abs(sq:getX() - view.bait.x) <= DROP_RANGE
                and math.abs(sq:getY() - view.bait.y) <= DROP_RANGE then
                return ISWorldObjectContextMenu.setTest()       -- client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua:81
            end
        else
            addBaitDrop(context, playerObj, sq, view)
        end
    end

    -- B1b: Futter hinhalten -- nur wenn ein passendes Junges nah ist (sonst kein Menue-Muell in der Stadt). Steht VOR dem Riegel
    -- des Koeder-Teils: auch mit ausgeschaltetem Koeder oder ausgeschalteten neuen Jungen bleibt das eigene Junge lockbar.
    local holdCub = holdWanted(playerObj, B.PlayerKey(playerObj))
    if holdCub then
        if test then return ISWorldObjectContextMenu.setTest() end
        addHold(context, playerObj, holdCub)
    end

    -- Auslegen: nur wenn Junge und Koeder eingeschaltet sind (sonst kein Menue-Muell).
    if me.on == false or B.Opt("BearBaitEnabled") == false then return end
    local rows = baitRows(playerObj)
    if #rows == 0 then return end
    local near = B.NearForest(sq:getX(), sq:getY(), sq:getZ(), B.CFG.baitEdge)
    if not near then
        -- Ausserhalb des Waldes nur dann ein (grauer) Punkt, wenn der Spieler Honig oder Fisch in der Hand haelt.
        local hand = playerObj:getPrimaryHandItem()             -- ISAnimalContextMenu.lua:93
        if not hand then return end
        local inHand = B.IsBaitFood(hand)
        if not inHand then return end
    end
    if test then return ISWorldObjectContextMenu.setTest() end
    addBait(context, playerObj, sq, me, rows, near)
end

Events.OnClickedAnimalForContext.Add(onClickedAnimals)          -- client/ISUI/Animal/ISAnimalContextMenu.lua:1235
Events.OnFillWorldObjectContextMenu.Add(onFillWorld)            -- client/ISUI/Hutch/ISHutchMenu.lua:115
Events.OnGameBoot.Add(hookRadial)                               -- F1B; V:client/Foraging/ISSearchManager.lua:1481
