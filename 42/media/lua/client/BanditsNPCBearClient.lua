--
-- NPC Crew -- Baer, Client-Seite der Befehle und Meldungen (B1a, PLAN_ZAEHMEN.md 5.6, 6.2.4, 6.2.6).
--
-- Laeuft im Einzelspieler und auf jedem MP-Client (der dedizierte Server laedt client/ nicht). Diese Datei entscheidet NICHTS:
-- sie nimmt die Sicht ("Sync") und die Meldungen ("Note") des Schreibers an, zeigt Meldungen ueber der Figur und bittet beim
-- Start um die Sicht ("Hello"). Was gilt, entscheidet immer der Schreiber (Einzelspieler: dasselbe Programm; Mehrspieler: Server).
--   Einzelspieler: der Kern ruft B.ShowNote und B.ApplySync direkt (sendServerCommand tut dort nichts), B.Ask ruft B.Handle direkt.
--   Mehrspieler:   beides kommt ueber OnServerCommand; B.Ask schickt sendClientCommand.
-- Eigene Helfer der Oberflaeche liegen nur unter B.UI (der Kern belegt B.UI nicht). Kein Engine-Aufruf ohne Vanilla-Fundstelle
-- (Kommentar daneben). Nichts hier laeuft je Bild: der Takt unten ist ein Wahrheitswert-Vergleich, solange nichts zu tun ist.
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- ---------------------------------------------------------------------------
-- Englische Ersatztexte (wortgleich mit Translate/EN/UI.json; attrappe/ober/texte_pruefen.py vergleicht beide). Gebraucht, wenn ein
-- Schluessel in der Sprache des Spielers fehlt: B.T(key, ersatz, ...) setzt dann hier ein.
-- ---------------------------------------------------------------------------
U.EN = {
    UI_BN_Bear_Why_Gone = "The cub is gone.",
    UI_BN_Bear_Why_Far = "You are too far away.",
    UI_BN_Bear_Why_FeedWait = "It is still full. Try again in about %1.",
    UI_BN_Bear_Why_PetWait = "It wants a break. Try again in about %1.",
    UI_BN_Bear_Why_Shy = "It is still too shy to be petted. Offer it food first.",
    UI_BN_Bear_Why_Other = "This cub already trusts someone else.",
    UI_BN_Bear_Why_NotOwner = "Only its owner can do that.",
    UI_BN_Bear_Why_HasBear = "You already have a bear.",
    UI_BN_Bear_Why_HasCub = "You are already taming another cub.",
    UI_BN_Bear_Why_Locked = "You are still mourning your bear. A new cub will trust you in about %1 day(s).",
    UI_BN_Bear_Why_NotFood = "A bear will not eat that.",
    UI_BN_Bear_Why_Rotten = "It turns away from spoiled food.",
    UI_BN_Bear_Why_NoItem = "You no longer have that food.",
    UI_BN_Bear_Why_Full = "There are too many wild cubs around right now.",
    UI_BN_Bear_Why_Off = "Bear cubs are switched off in the sandbox settings.",
    UI_BN_Bear_Why_MoreFood = "It still wants to be fed %1 more time(s) before it fully trusts you.",
    UI_BN_Bear_Note_Heard = "You hear a faint whimpering from the forest to the %1.",
    UI_BN_Bear_Note_Seen = "A bear cub! It looks lost and hungry.",
    UI_BN_Bear_Note_Gain = "+%1 trust",
    UI_BN_Bear_Note_GainMix = "+%1 trust - it likes the change!",
    UI_BN_Bear_Note_GainFav = "+%1 trust - it loves this!",
    UI_BN_Bear_Note_FirstFed = "It ate from your hand. It will stay around here now.",
    UI_BN_Bear_Note_Tamed = "The cub trusts you. It is yours now!",
    UI_BN_Bear_Note_Happy = "It enjoys that.",
    UI_BN_Bear_Note_Vanished = "The bear cub has wandered off.",
    UI_BN_Bear_Note_Dead = "The bear cub is dead.",
    UI_BN_Bear_Note_BearDead = "Your bear is dead. A new cub will trust you in %1 day(s) at the earliest.",
    UI_BN_Bear_Note_Missing = "You have lost track of your bear.",
    UI_BN_Bear_Note_Back = "Your bear is back.",
    UI_BN_Bear_Note_Abandoned = "The cub has stopped waiting for you.",
    UI_BN_Bear_Bait_Placed = "Bait laid out. Come back after a night or two - and keep your distance.",
    UI_BN_Bear_Bait_NotForest = "Bait only works in or right next to a forest.",
    UI_BN_Bear_Bait_Inside = "Bait has to lie outdoors on free ground.",
    UI_BN_Bear_Bait_HasOne = "You already have a bait spot.",
    UI_BN_Bear_Bait_TooClose = "Another bait spot is too close.",
    UI_BN_Bear_Bait_BadFood = "Only honey or fish lures a bear cub.",
    UI_BN_Bear_Bait_Near = "Something is circling the bait but will not come out while people are close.",
    UI_BN_Bear_Bait_Came = "A bear cub has found your bait!",
    UI_BN_Bear_Bait_Expired = "The bait is gone. No cub came.",
    UI_BN_Bear_Bait_Dropped = "Bait spot given up.",
    UI_BN_Bear_Bait_Off = "Bear bait is switched off in the sandbox settings.",
    UI_BN_Bear_Bait_Honey = "honey",
    UI_BN_Bear_Bait_Fish = "fish",
    UI_BN_Bear_Dir_N = "north",
    UI_BN_Bear_Dir_NE = "north-east",
    UI_BN_Bear_Dir_E = "east",
    UI_BN_Bear_Dir_SE = "south-east",
    UI_BN_Bear_Dir_S = "south",
    UI_BN_Bear_Dir_SW = "south-west",
    UI_BN_Bear_Dir_W = "west",
    UI_BN_Bear_Dir_NW = "north-west",
    UI_BN_Bear_Menu_Feed = "Feed",
    UI_BN_Bear_Menu_Pet = "Pet",
    UI_BN_Bear_Menu_NoFood = "You carry nothing a bear would eat: meat, fish, honey, berries, fruit, eggs, nuts or insects.",
    UI_BN_Bear_Menu_Bait = "Lay out bear bait",
    UI_BN_Bear_Menu_BaitTip = "The bait is used up. A cub may come after one to three nights.",
    UI_BN_Bear_Menu_BaitDrop = "Give up bait spot",
    UI_BN_Bear_Menu_BaitDropTip = "The bait will not come back.",
    UI_BN_Bear_Food_Fav = "%1 - loves it",
    UI_BN_Bear_Food_Ok = "%1",
    UI_BN_Bear_Food_Snack = "%1 - only a nibble",
    UI_BN_Bear_Time_Minutes = "%1 min",
    UI_BN_Bear_Time_Hours = "%1 h",
    UI_BN_Bear_Hud_Taming = "Taming %1%%",
    UI_BN_Bear_Hud_Shy = "shy",
    UI_BN_Bear_Hud_Feed = "Food: %1",
    UI_BN_Bear_Hud_Pet = "Petting: %1",
    UI_BN_Bear_Hud_Ready = "ready",
    UI_BN_Bear_Hud_Tamed = "Tamed!",
    UI_BN_Bear_Hud_Other = "trusts %1",
    UI_BN_Bear_Hud_Bait = "Bear bait (%1)",
    UI_BN_Bear_Hud_BaitNight = "night %1 of up to %2",
    UI_BN_Bear_Hud_BaitReady = "something was here",
    UI_BN_Bear_Tip_Mix = "Taking turns between feeding and petting earns more trust.",
}

local KEY_HEAD = "UI_BN_Bear_"
local DIRS = { N = true, NE = true, E = true, SE = true, S = true, SW = true, W = true, NW = true }

-- ---------------------------------------------------------------------------
-- Texte
-- ---------------------------------------------------------------------------

-- Text zu einem Schluessel mit bis zu drei Einsetzungen. Uebersetzen und Einsetzen macht B.T (Kern); von hier kommt nur der
-- englische Ersatztext aus U.EN.
function U.T(key, a1, a2, a3)
    return B.T(key, U.EN[key] or key, a1, a2, a3)
end

-- Dauer als Text: unter einer Stunde Minuten, sonst Stunden (Rundung macht B.WaitParts).
function U.WaitText(hours)
    local n, unitKey = B.WaitParts(tonumber(hours) or 0)
    return U.T(unitKey, n)
end

-- Text einer Ablehnung der Regel-Funktionen (B.CheckFeed, B.CheckPet, B.CheckBait): whyVal ist bei Wartezeiten die Reststunden,
-- bei der Sperre die Resttage, sonst nil (Plan 6.2.2).
function U.WhyText(whyKey, whyVal)
    if type(whyKey) ~= "string" then return "" end
    if whyVal == nil then return U.T(whyKey) end
    if whyKey == "UI_BN_Bear_Why_FeedWait" or whyKey == "UI_BN_Bear_Why_PetWait" then
        return U.T(whyKey, U.WaitText(whyVal))
    end
    if type(whyVal) == "number" then
        if whyKey == "UI_BN_Bear_Why_Locked" then return U.T(whyKey, math.ceil(whyVal)) end
        return U.T(whyKey, math.floor(whyVal))
    end
    return U.T(whyKey, tostring(whyVal))
end

-- Text einer Meldung des Schreibers: { k = Schluessel, t = "wait" / "days" / "dir" / "num" / "name" / nil, v = Wert } (Plan 6.2.6).
-- Gibt nil, wenn die Meldung keine von uns ist.
function U.NoteText(note)
    if type(note) ~= "table" then return nil end
    local key = note.k
    if type(key) ~= "string" or string.sub(key, 1, string.len(KEY_HEAD)) ~= KEY_HEAD then return nil end
    local t = note.t
    local v = note.v
    if t == "wait" then
        return U.T(key, U.WaitText(v))
    elseif t == "days" then
        return U.T(key, math.ceil(tonumber(v) or 0))
    elseif t == "dir" then
        if type(v) == "string" and DIRS[v] then
            return U.T(key, U.T(KEY_HEAD .. "Dir_" .. v))
        end
        return U.T(key, tostring(v))
    elseif t == "num" then
        return U.T(key, math.floor(tonumber(v) or 0))
    elseif t == "name" then
        return U.T(key, tostring(v))
    end
    return U.T(key)
end

-- ---------------------------------------------------------------------------
-- Meldung zeigen (Plan 6.2.4). Der Kern ruft das im Einzelspieler direkt, im Mehrspieler kommt es ueber "Note".
-- ---------------------------------------------------------------------------
function B.ShowNote(player, note)
    if not player then return end
    local text = U.NoteText(note)
    if not text or text == "" then return end
    local tone = note.tone
    if tone == "good" then
        HaloTextHelper.addGoodText(player, text)    -- client/ServerCommands.lua:183
    elseif tone == "bad" then
        HaloTextHelper.addBadText(player, text)     -- client/ISUI/ISWorldObjectContextMenu.lua:1038
    else
        HaloTextHelper.addText(player, text)        -- client/Foraging/forageClient.lua:73
    end
end

-- ---------------------------------------------------------------------------
-- Sicht: ist sie von DIESEM Spiel?
--
-- B.View gehoert dem Kern (nur lesen). Nach "Hauptmenue und anderen Spielstand laden" kann eine alte Sicht stehen geblieben
-- sein; Menue und Balken benutzen sie deshalb erst, wenn seit dem Spielstart eine Sicht angekommen ist. Gezaehlt wird in
-- B.OnView (client/ISUI/BanditsNPCBearHud.lua), das der Kern nach jeder Sicht ruft.
-- ---------------------------------------------------------------------------
U.syncN = U.syncN or 0
local hello = { on = false, wait = false, base = 0, n = 0, nextAt = 0 }

function U.NoteSync()
    U.syncN = (U.syncN or 0) + 1
end

function U.Fresh()
    local view = B.View
    if not view or view.ready ~= true or not hello.on then return false end
    -- Ohne B.OnView (Balken-Datei fehlt) kann nicht gezaehlt werden: dann gilt, was der Kern "ready" nennt.
    if not B.OnView then return true end
    return (U.syncN or 0) > hello.base
end

-- ---------------------------------------------------------------------------
-- "Hello": um die Sicht bitten. Einmal beim Start, dann alle 10 s, bis sie da ist (nach 12 Versuchen nur noch jede Minute:
-- nichts haengt, nichts flutet). Ausserdem, wenn der Spieler ein Junges anklickt, das seine Sicht nicht kennt (hoechstens alle 5 s).
-- ---------------------------------------------------------------------------
local HELLO_MS = 10000
local HELLO_SLOW_MS = 60000
local HELLO_FAST_N = 12
local HELLO_CLICK_MS = 5000

local function sendHello(player, now)
    U.helloAt = now
    -- Nie eine LEERE Tabelle: die Engine schickt sie als nil (Vanilla client/ServerCommands.lua:210-213 "Can be nil if sending
    -- an empty table"; Jar GameClient.sendClientCommand, dec/SinglePlayerServer.java:179-190). Nachbesserung B1.
    if B.Ask then B.Ask(player, "Hello", { v = 1 }) end
end

function U.AskHello(player)
    if not player then return end
    local now = getTimestampMs()                    -- server/Foraging/forageServer.lua:456
    local last = U.helloAt
    if last and now >= last and now - last < HELLO_CLICK_MS then return end
    sendHello(player, now)
end

local function helloTick()
    if not hello.wait then return end
    local now = getTimestampMs()
    if now < hello.nextAt and hello.nextAt - now <= HELLO_SLOW_MS then return end
    if U.Fresh() then
        hello.wait = false
        return
    end
    local player = getSpecificPlayer(0)             -- client/ISUI/Animal/ISAnimalContextMenu.lua:134 (Zahl)
    if not player then
        hello.nextAt = now + 1000
        return
    end
    hello.n = hello.n + 1
    hello.nextAt = now + ((hello.n <= HELLO_FAST_N) and HELLO_MS or HELLO_SLOW_MS)
    sendHello(player, now)
end

local function onGameStart()
    hello.base = U.syncN or 0
    hello.n = 0
    hello.nextAt = 0
    hello.wait = true
    hello.on = true
end

-- ---------------------------------------------------------------------------
-- Schreiber -> Client (nur Mehrspieler). args kann nil sein, wenn eine leere Tabelle geschickt wurde
-- (client/ServerCommands.lua:210-213).
-- ---------------------------------------------------------------------------
local function onServerCommand(module, command, args)
    if not B.CMD or module ~= B.CMD then return end
    if type(args) ~= "table" then return end
    if command == "Sync" then
        if B.ApplySync then B.ApplySync(args) end
    elseif command == "Note" then
        B.ShowNote(getPlayer(), args)               -- getPlayer(): client/ServerCommands.lua:204
    end
end

Events.OnServerCommand.Add(onServerCommand)         -- client/ServerCommands.lua:218
Events.OnGameStart.Add(onGameStart)                 -- client/Chat/ISChat.lua:1186
Events.OnTick.Add(helloTick)                        -- client/Chat/ISChat.lua:943
