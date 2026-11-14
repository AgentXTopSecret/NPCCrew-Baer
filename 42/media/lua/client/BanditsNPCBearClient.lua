--
-- NPC Crew -- Baer, Client-Seite der Befehle und Meldungen (B1a, PLAN_ZAEHMEN.md 5.6, 6.2.4, 6.2.6; B1b, PLAN_B1B.md 5.4:
-- Namen fuer das Schild, neue Texte; B1c, PLAN_B1C.md 6.4/6.7: neue Texte, Ankunftszeit der Sicht U.viewAt; B1d, PLAN_B1D.md
-- 6.5/6.7: Meldungen "stage" (Stufe erreicht) und "skill" (Faehigkeit gestiegen), U.StageName, Texte fuer Schild und Optionen;
-- B1e, PLAN_B1E.md 6.4/6.5/6.8: Texte je Koerper -- U.TB, Big-Fassungen in U.NoteText und U.CubName, Texte der Markierungs-Groesse;
-- F1, PLAN_F1.md 4a/7.6: Texte des Baeren-Fensters und der neuen Befehle, U.WhyText mit Koerper bd; F1B, PLAN_F1B.md 3.2: Texte der
-- zwei Tasten (Optionen-Seite), der Fusszeile und des Wachstums-Schalters, zwei neue Werte, "Tag_AgeDone" entfaellt; F2 = B5a,
-- PLAN_F2.md 2.7, 4.1, 4.4, Nachtrag 11: Texte des Kampfs, Am Boden, Verband, Show damage, Melee damage, Kills, Alters-Deckel; der neue
-- Befehl "Fx" Schreiber -> Client wird an B.OnFx weitergereicht -- shared/BanditsNPCBearFoe.lua, KERN); Aussehen (Lauf baer-aussehen,
-- PLAN_AUSSEHEN.md 10): 27 Texte des Aussehen-Knopfs (Namen, Knopf, Tooltips, Meldung, Ablehnungen des Schreibers mit Big-Fassung);
-- F3 (Lauf baer-f3, PLAN_F3.md 11; Kevin 13.11.2026): 91 Texte fuer Beduerfnisse, Vertrauen, Schlafen, Traenken und das Fenster
-- Variante B (2 geaendert, 2 entfernt), dazu U.SleepColor -- die EINE Schlaf-Farbe fuer z Z z, Chip und Schild-Zeile.
-- F4 (Lauf baer-f4, PLAN_F4.md 13; Kevin 13.11.2026 abends): Texte fuer Traglast, Inventar-Fenster, Packtaschen, Ablehnungen und Meldungen des
-- Kerns (f4/schnittstelle.md K6 / K7; "Can carry" faellt weg); neuer Befehl "Inv" Schreiber -> Client (eine Seite der Inventar-Liste, weiter an
-- B.OnInv, client/BanditsNPCBearInvClient.lua) und Meldungs-Typ "item" (v = voller Typ, w / x = Anzahl; Name ueber U.ItemName).
-- K1 (Lauf baer-k1, PLAN_K1.md 2, 4, 5, 8; Kevin 13./14.11.2026): 38 neue und 22 geaenderte Texte (Vertrauen -100..+100, Zahnrad-Menue, roter
-- Schaden, Tagesbedarf, Einfrieren, Zahlenfeld, Meldungen des Kerns zu Vertrauen / Look-Sperre / Buendeln / Selbst-Trinken) -- U.EN wortgleich EN.
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

-- F3 (PLAN_F3.md 8, 10.1; Kevin 13.11.2026 "Hellblau, ueber dem Kopf"): die EINE Schlaf-Farbe -- z Z z (client/ISUI/BanditsNPCBearZz.lua),
-- Chip "Sleeping" (client/ISUI/BanditsNPCBearWinParts.lua) und Schild-Zeile "sleeping" (client/ISUI/BanditsNPCBearHud.lua). Der Wert
-- gehoert dem Kern (B.CFG.sleepCol = { r, g, b }, auch als Felder r / g / b); fehlt er oder ist er Unsinn: derselbe Wert als Rueckfall.
-- Reines Tabellen-Lesen, gibt r, g, b.
local SLEEP_COL = { 0.70, 0.85, 1.00 }
function U.SleepColor()
    local c = B.CFG and B.CFG.sleepCol
    if type(c) == "table" then
        local r, g, b = tonumber(c[1] or c.r), tonumber(c[2] or c.g), tonumber(c[3] or c.b)
        if r and g and b and r == r and g == g and b == b then return r, g, b end
    end
    return SLEEP_COL[1], SLEEP_COL[2], SLEEP_COL[3]
end

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
    UI_BN_Bear_Note_Tamed = "The cub trusts you. It is yours now! Right-click it and choose Follow me.",
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
    UI_BN_Bear_Tip_Mix = "Petting, feeding it until it is full and watering it until it is full each bring +0.5 trust once a day.",
    -- B1b (PLAN_B1B.md 6.1 und 6.2): Folgen, Bleiben, Namensschild, Umbenennen, Futter hinhalten
    UI_BN_Bear_Why_NameBad = "That name does not work. Use 1 to %1 characters, without angle brackets or percent signs.",
    UI_BN_Bear_Why_InCar = "Not while you are in a vehicle.",
    UI_BN_Bear_Note_Follow = "Your cub follows you.",
    UI_BN_Bear_Note_Stay = "Your cub stays here.",
    UI_BN_Bear_Note_StayCar = "Your cub was too far away to get in. It waits here.",
    UI_BN_Bear_Note_StayFar = "Your cub could not keep up. It waits to the %1.",
    UI_BN_Bear_Note_StayBehind = "Your cub stayed behind to the %1.",
    UI_BN_Bear_Note_Renamed = "Your cub is now called %1.",
    UI_BN_Bear_Menu_Follow = "Follow me",
    UI_BN_Bear_Menu_Stay = "Stay here",
    UI_BN_Bear_Menu_FollowTip = "It runs after you and rides along in vehicles. If you get too far ahead, it waits.",
    UI_BN_Bear_Menu_StayTip = "It stays around this spot.",
    UI_BN_Bear_Menu_Name = "Name the cub",
    UI_BN_Bear_Name_Title = "Name for your cub:",
    UI_BN_Bear_Menu_Hold = "Hold out food for the cub",
    UI_BN_Bear_Menu_HoldTip = "Takes it in your hand. Stand still and the cub comes closer.",
    UI_BN_Bear_Tag_Name = "%1's cub",
    UI_BN_Bear_Tag_Follow = "following",
    UI_BN_Bear_Tag_Stay = "staying",
    UI_BN_Bear_Tag_Owner = "belongs to %1",
    -- B1c (PLAN_B1C.md 6.7): Mitfahren, Call to me, Markierung, Anzeige-Optionen (die MO_*-Texte liest Vanillas Optionen-Fenster
    -- selbst ueber getText; hier stehen sie nur, damit U.EN wortgleich mit EN/UI.json bleibt)
    UI_BN_Bear_Note_RideOn = "Your cub jumps in with you.",
    UI_BN_Bear_Note_RideOff = "Your cub hops out.",
    UI_BN_Bear_Note_Called = "Here is your cub again.",
    UI_BN_Bear_Why_CallWait = "You can call your cub again in about %1 min.",
    UI_BN_Bear_Why_Riding = "Your cub is riding with you.",
    UI_BN_Bear_Why_NoRoom = "There is no free spot next to you.",
    UI_BN_Bear_Menu_Call = "Call to me",
    UI_BN_Bear_Menu_CallTip = "Brings your cub right next to you if it is stuck. Works once every %1 minutes.",
    UI_BN_Bear_Marker_Cub = "Bear cub nearby",
    UI_BN_Bear_MO_Page = "NPC Crew: Bear",
    UI_BN_Bear_MO_Title = "Display above bears",
    UI_BN_Bear_MO_TagShow = "Show name tags above tamed bears",
    UI_BN_Bear_MO_TagShowTip = "Name and state - and the heart at full trust. The taming bar always shows.",
    UI_BN_Bear_MO_TagSize = "Size of the display above bears (%%)",
    UI_BN_Bear_MO_TagSizeTip = "100, 150 or 200.",
    -- B1d (PLAN_B1D.md 6.7): Werte-Zeilen des Schilds, Stufen, Faehigkeiten, zwei Meldungen des Kerns, Anzeige-Optionen
    UI_BN_Bear_Tag_Health = "Health %1/%2",
    UI_BN_Bear_Tag_Stamina = "Stamina %1/%2",
    UI_BN_Bear_Tag_Age = "Day %1 - %2 in %3 day(s)",
    UI_BN_Bear_Stage_Half = "half-grown",
    UI_BN_Bear_Stage_Strong = "strong",
    UI_BN_Bear_Stage_Adult = "full-grown",
    UI_BN_Bear_Skill_Agi = "agility",
    UI_BN_Bear_Skill_Vit = "toughness",
    UI_BN_Bear_Skill_Con = "endurance",
    UI_BN_Bear_Skill_Fgt = "fighting",
    UI_BN_Bear_Skill_Fsh = "fishing",
    UI_BN_Bear_Skill_Nos = "keen nose",
    UI_BN_Bear_Note_Grown = "Your bear is %1 now.",
    UI_BN_Bear_Note_SkillUp = "Your bear's %1 is now level %2.",
    UI_BN_Bear_MO_Health = "Health above tamed bears",
    UI_BN_Bear_MO_HealthTip = "Off, as a bar or as a number (now / most).",
    UI_BN_Bear_MO_Stamina = "Stamina above tamed bears",
    UI_BN_Bear_MO_StaminaTip = "Off, as a bar or as a number. Stamina drops while a bear runs and comes back while it rests.",
    UI_BN_Bear_MO_Age = "Age and growth above tamed bears",
    UI_BN_Bear_MO_AgeTip = "Growth day and when the next stage comes. Main switch: each bear also has its own switch in the bear window. Full-grown bears show no line.",
    UI_BN_Bear_MO_Off = "Off",
    UI_BN_Bear_MO_Bar = "Bar",
    UI_BN_Bear_MO_Number = "Number",
    -- B1e (PLAN_B1E.md 6.8): Big-Fassungen fuer den grossen Koerper (U.TB / U.NoteText waehlen sie bei bd == "big"; Platzhalter je
    -- Schluessel gleich dem Grundschluessel) und die Groesse der Markierung (Optionen-Seite, MarkerSize)
    UI_BN_Bear_Tag_NameBig = "%1's bear",
    UI_BN_Bear_Note_FollowBig = "Your bear follows you.",
    UI_BN_Bear_Note_StayBig = "Your bear stays here.",
    UI_BN_Bear_Note_StayCarBig = "Your bear was too far away to get in. It waits here.",
    UI_BN_Bear_Note_StayFarBig = "Your bear could not keep up. It waits to the %1.",
    UI_BN_Bear_Note_StayBehindBig = "Your bear stayed behind to the %1.",
    UI_BN_Bear_Note_RenamedBig = "Your bear is now called %1.",
    UI_BN_Bear_Note_RideOnBig = "Your bear climbs in with you.",
    UI_BN_Bear_Note_RideOffBig = "Your bear climbs out.",
    UI_BN_Bear_Note_CalledBig = "Here is your bear again.",
    UI_BN_Bear_Why_RidingBig = "Your bear is riding with you.",
    UI_BN_Bear_Why_CallWaitBig = "You can call your bear again in about %1 min.",
    UI_BN_Bear_Menu_NameBig = "Name the bear",
    UI_BN_Bear_Menu_CallTipBig = "Brings your bear right next to you if it is stuck. Works once every %1 minutes.",
    UI_BN_Bear_Name_TitleBig = "Name for your bear:",
    UI_BN_Bear_MO_MarkerSize = "Size of the cub marker at the top of the screen",
    UI_BN_Bear_MO_MarkerSizeTip = "Auto grows with the screen height (1080p = 100%%, 4K = 200%%).",
    UI_BN_Bear_MO_Auto = "Auto",
    UI_BN_Bear_MO_Pct100 = "100%%",
    UI_BN_Bear_MO_Pct125 = "125%%",
    UI_BN_Bear_MO_Pct150 = "150%%",
    UI_BN_Bear_MO_Pct200 = "200%%",
    UI_BN_Bear_MO_Pct250 = "250%%",
    UI_BN_Bear_MO_Pct300 = "300%%",
    -- F1 (PLAN_F1.md 7.6): Baeren-Fenster (Win_*), Rechtsklick "Bear window", Fenstergroesse (MO_WinSize*), Schild Sitz/Frei,
    -- die neuen Meldungen des KERNs mit Big-Fassung (U.NoteText waehlt sie bei bd == "big") und die B1e-Reste A1/B6
    -- (Why_GoneBig, Note_DeadBig, Menu_HoldBig, Menu_HoldTipBig). F1B: keine Zeile mehr in Vanillas Tastaturbelegung -- die zwei
    -- Schluessel UI_optionscreen_binding_* sind aus allen sieben UI.json entfernt.
    UI_BN_Bear_Win_BodyCub = "Bear cub",
    UI_BN_Bear_Win_BodyBear = "Bear",
    UI_BN_Bear_Win_Sub = "%1 - day %2",
    UI_BN_Bear_Win_Next = "%1 in %2 day(s)",
    UI_BN_Bear_Win_Grown = "full-grown",
    UI_BN_Bear_Win_St_Follow = "Following you",
    UI_BN_Bear_Win_St_Stay = "Staying",
    UI_BN_Bear_Win_St_Sit = "Sitting",
    UI_BN_Bear_Win_St_Roam = "Roaming",
    UI_BN_Bear_Win_St_Come = "Coming to you",
    UI_BN_Bear_Win_St_Hide = "Hiding",
    UI_BN_Bear_Win_St_Ride = "Riding with you",
    UI_BN_Bear_Win_St_Missing = "Missing",
    UI_BN_Bear_Win_St_Away = "Out of reach",
    UI_BN_Bear_Win_Here = "right next to you",
    UI_BN_Bear_Win_Dist = "%1 tiles to the %2",
    UI_BN_Bear_Win_LastSeen = "last seen %1 tiles to the %2",
    UI_BN_Bear_Win_Count = "%1 / %2",
    UI_BN_Bear_Win_Rename = "Rename",
    UI_BN_Bear_Win_Cond = "Condition",
    UI_BN_Bear_Win_Skills = "Skills",
    UI_BN_Bear_Win_Orders = "Orders",
    UI_BN_Bear_Win_Health = "Health",
    UI_BN_Bear_Win_Stamina = "Stamina",
    UI_BN_Bear_Win_None = "--",
    UI_BN_Bear_Win_Hunger = "Hunger",
    UI_BN_Bear_Win_Thirst = "Thirst",
    UI_BN_Bear_Win_Tired = "Tiredness",
    UI_BN_Bear_Win_Trust = "Trust",
    UI_BN_Bear_Win_HealthTip = "Grows every day as your bear grows, and with Toughness. Heals slowly on its own, faster with a bandage.",
    UI_BN_Bear_Win_StaminaTip = "Drops while your bear runs and fights, and comes back while it rests. Empty: it backs off to catch its breath. More with Endurance.",
    UI_BN_Bear_Win_Sk_Agi = "Agility",
    UI_BN_Bear_Win_Sk_Vit = "Toughness",
    UI_BN_Bear_Win_Sk_Con = "Endurance",
    UI_BN_Bear_Win_Sk_Fgt = "Fighting",
    UI_BN_Bear_Win_Sk_Fsh = "Fishing",
    UI_BN_Bear_Win_Sk_Nos = "Keen nose",
    UI_BN_Bear_Win_Lv = "Lv %1",
    UI_BN_Bear_Win_Pct = "%1%%",
    UI_BN_Bear_Win_Max = "max",
    UI_BN_Bear_Win_SkHead = "%1 - level %2",
    UI_BN_Bear_Win_SkProg = "%1 of %2 to level %3",
    UI_BN_Bear_Win_SkTop = "Level 10 - the highest level.",
    UI_BN_Bear_Win_SkTip_Agi = "A hit misses your bear completely: %1%% now, %2%% at level 10.",
    UI_BN_Bear_Win_SkFrom_Agi = "Grows with every hit your bear takes.",
    UI_BN_Bear_Win_SkTip_Vit = "Adds +%1%% health on top of the daily growth.",
    UI_BN_Bear_Win_SkFrom_Vit = "Grows with every hit your bear takes.",
    UI_BN_Bear_Win_SkTip_Con = "Bigger stamina bar (+%1%%) and faster rest.",
    UI_BN_Bear_Win_SkFrom_Con = "Grows when your bear runs and gets out of breath.",
    UI_BN_Bear_Win_SkTip_Fgt = "+%1%% damage now, +%2%% at level 10, on top of the daily growth.",
    UI_BN_Bear_Win_SkFrom_Fgt = "Grows with every hit your bear lands.",
    UI_BN_Bear_Win_SkTip_Fsh = "Catch chance %1%% (from half-grown; clumsy at first, much better later).",
    UI_BN_Bear_Win_SkFrom_Fsh = "Grows while your bear fishes.",
    UI_BN_Bear_Win_SkTip_Nos = "Smells zombies earlier and warns you with a growl: %1 tiles.",
    UI_BN_Bear_Win_SkFrom_Nos = "Grows when it sniffs out zombies.",
    UI_BN_Bear_Win_LaterFish = "Fishing comes later.",
    UI_BN_Bear_Win_LaterNose = "Comes later and can be switched off.",
    UI_BN_Bear_Win_Follow = "Follow",
    UI_BN_Bear_Win_Stay = "Stay",
    UI_BN_Bear_Win_Sit = "Sit",
    UI_BN_Bear_Win_Roam = "Roam free",
    UI_BN_Bear_Win_Come = "Come here",
    UI_BN_Bear_Win_Unstuck = "Unstuck",
    UI_BN_Bear_Win_UnstuckWait = "Unstuck  %1",
    UI_BN_Bear_Win_CallWaitClock = "You can call your cub again in %1.",          -- Nachbesserung F1 B6 (Tooltip mit m:ss)
    UI_BN_Bear_Win_CallWaitClockBig = "You can call your bear again in %1.",
    UI_BN_Bear_Win_Passive = "Passive",
    UI_BN_Bear_Win_Tag = "Name tag",
    UI_BN_Bear_Win_StayTip = "It stays right at this spot and waits.",
    UI_BN_Bear_Win_SitTip = "It sits down right here and stays sitting until you give another order.",
    UI_BN_Bear_Win_RoamTip = "It strolls around freely, but never further than %1 tiles from this spot.",
    UI_BN_Bear_Win_ComeTip = "It walks over to you and waits there. If it is stuck, use Unstuck.",
    UI_BN_Bear_Win_PassiveTip = "Your bear stays out of fights and comes back to you. A cub never fights anyway.",
    UI_BN_Bear_Win_TagTip = "Shows the name above this bear - and its heart at full trust. Only on your screen.",
    UI_BN_Bear_Win_TagOffAll = "All name tags are switched off in Options - Mods.",
    UI_BN_Bear_Win_RoamInfo = "Roams within %1 tiles",
    UI_BN_Bear_Win_Active = "This is its current order.",
    UI_BN_Bear_Win_Hint = "Drag to move.  %1 or Esc closes.",
    UI_BN_Bear_Win_HintEsc = "Drag to move.  Esc closes.",
    UI_BN_Bear_Win_HintMissing = "No body now. It can come back while you are near, or use Unstuck.",
    UI_BN_Bear_Win_HintRide = "It rides with you and gets out when you stop.",
    UI_BN_Bear_Win_HintAway = "Too far away for orders. Unstuck brings it to you.",
    UI_BN_Bear_Win_NoBear = "You do not have a bear yet.",
    UI_BN_Bear_Win_NoData = "The bear window is still loading. Try again in a moment.",
    UI_BN_Bear_Menu_Window = "Bear window",
    UI_BN_Bear_Menu_WindowTip = "Also opens with a key when you stand near your bear (E by default) - Options, Mods, NPC Crew: Bear.",
    UI_BN_Bear_MO_WinSize = "Size of the bear window",
    UI_BN_Bear_MO_WinSizeTip = "Auto grows with the screen height (1080p = 100%%, 4K = 200%%).",
    UI_BN_Bear_Tag_Sit = "sitting",
    UI_BN_Bear_Tag_Roam = "roaming",
    UI_BN_Bear_Note_Sit = "Your cub sits down.",
    UI_BN_Bear_Note_SitBig = "Your bear sits down.",
    UI_BN_Bear_Note_Roam = "Your cub roams around here (up to %1 tiles).",
    UI_BN_Bear_Note_RoamBig = "Your bear roams around here (up to %1 tiles).",
    UI_BN_Bear_Note_Coming = "Your cub is coming to you.",
    UI_BN_Bear_Note_ComingBig = "Your bear is coming to you.",
    UI_BN_Bear_Note_Came = "Your cub is with you and waits here.",
    UI_BN_Bear_Note_CameBig = "Your bear is with you and waits here.",
    UI_BN_Bear_Note_ComeFail = "Your cub could not get to you. It waits where it is.",
    UI_BN_Bear_Note_ComeFailBig = "Your bear could not get to you. It waits where it is.",
    UI_BN_Bear_Note_PassiveOn = "Your cub is passive now: it keeps out of fights and comes back to you.",
    UI_BN_Bear_Note_PassiveOnBig = "Your bear is passive now: it keeps out of fights and comes back to you.",
    UI_BN_Bear_Note_PassiveOff = "Your cub is no longer passive.",
    UI_BN_Bear_Note_PassiveOffBig = "Your bear is no longer passive.",
    UI_BN_Bear_Why_OutOfReach = "Your cub is out of reach. Use Unstuck.",
    UI_BN_Bear_Why_OutOfReachBig = "Your bear is out of reach. Use Unstuck.",
    UI_BN_Bear_Why_GoneBig = "The bear is gone.",
    UI_BN_Bear_Note_DeadBig = "Your bear is dead.",
    UI_BN_Bear_Menu_HoldBig = "Hold out food for the bear",
    UI_BN_Bear_Menu_HoldTipBig = "Takes it in your hand. Stand still and the bear comes closer.",
    -- F1B (PLAN_F1B.md 3.2): die zwei Tasten auf der Optionen-Seite (MO_Key*; die Namen holt client/BanditsNPCBearOptions.lua selbst
    -- ueber getText, hier stehen sie nur, damit U.EN wortgleich mit EN/UI.json bleibt), die Fusszeile des Fensters (Win_Hint*) und der
    -- Wachstums-Schalter (Win_Growth*)
    UI_BN_Bear_MO_Keys = "Bear window keys",
    UI_BN_Bear_MO_KeyNear = "Bear window: key near your bear",
    UI_BN_Bear_MO_KeyNearTip = "Opens and closes the bear window while you stand close to your own bear. It does nothing at a door, window, fence or car, while aiming or when no bear of yours is near, so E keeps working as usual. A single key only (no Shift, Ctrl or Alt). If the game says the key is already used, choose Keep Both.",
    UI_BN_Bear_MO_KeyFar = "Bear window: key from anywhere",
    UI_BN_Bear_MO_KeyFarTip = "Opens and closes the bear window wherever you are - handy for Unstuck when your bear is far away or missing. No key by default. A single key only (no Shift, Ctrl or Alt). If the game says the key is already used, choose Keep Both.",
    UI_BN_Bear_Win_HintNear = "Drag to move.  %1 near your bear or Esc closes.",
    UI_BN_Bear_Win_HintBoth = "Drag to move.  %1 near your bear, %2 anywhere or Esc closes.",
    UI_BN_Bear_Win_Growth = "Growth line",
    UI_BN_Bear_Win_GrowthTip = "Shows the day and growth line above this bear - only on your screen. When it is full-grown, the line and this switch go away.",
    UI_BN_Bear_Win_GrowthOffAll = "The age line is switched off for all bears in Options - Mods.",
    -- F2 (PLAN_F2.md 2.7, 3.2, Nachtrag 11): Meldungen Am Boden / Aufgeholfen / Allein aufgestanden / Fliehen (11.7: "a few hits
    -- from death") / Verbunden mit Big-Fassung, Ablehnungen, Schild, Option DODGE, Fenster (Zustaende, Hinweis, Knopf Verband /
    -- Aufhelfen, Leben-Tooltip, Show damage 11.1, Melee damage 11.2, Alters-Deckel 11.4, Kills 11.5), Rechtsklick. Geaendert (ehrlich):
    -- Note_PassiveOn(+Big), Win_PassiveTip, Win_StaminaTip, Win_HealthTip; entfernt: Win_LaterFight, Win_LaterGrow.
    UI_BN_Bear_Note_Down = "Your cub is down! Help it up.",
    UI_BN_Bear_Note_DownBig = "Your bear is down! Help it up.",
    UI_BN_Bear_Note_HelpedUp = "Your cub is back on its feet.",
    UI_BN_Bear_Note_HelpedUpBig = "Your bear is back on its feet.",
    UI_BN_Bear_Note_GotUp = "Your cub got back up on its own.",
    UI_BN_Bear_Note_GotUpBig = "Your bear got back up on its own.",
    UI_BN_Bear_Note_Flee = "Your cub is badly hurt - a few more hits would kill it. It comes back to you.",
    UI_BN_Bear_Note_FleeBig = "Your bear is badly hurt - a few more hits would kill it. It comes back to you.",
    UI_BN_Bear_Note_Bandaged = "Your cub is bandaged and heals faster for %1 hour(s).",
    UI_BN_Bear_Note_BandagedBig = "Your bear is bandaged and heals faster for %1 hour(s).",
    UI_BN_Bear_Why_NoBandage = "You have no clean bandage.",
    UI_BN_Bear_Why_BandageOff = "Bandages do not heal bears in this world.",
    UI_BN_Bear_Why_Dirty = "This bandage is dirty. Use a clean one.",
    UI_BN_Bear_Why_Healthy = "Your cub is not hurt.",
    UI_BN_Bear_Why_HealthyBig = "Your bear is not hurt.",
    UI_BN_Bear_Why_Bandaged = "Your cub is already bandaged (%1 hour(s) left).",
    UI_BN_Bear_Why_BandagedBig = "Your bear is already bandaged (%1 hour(s) left).",
    UI_BN_Bear_Why_Down = "Your cub is down. Help it up first.",
    UI_BN_Bear_Why_DownBig = "Your bear is down. Help it up first.",
    UI_BN_Bear_Why_NotDown = "Your cub is not down.",
    UI_BN_Bear_Why_NotDownBig = "Your bear is not down.",
    UI_BN_Bear_Tag_Fight = "fighting",
    UI_BN_Bear_Tag_Retreat = "backing off",
    UI_BN_Bear_Tag_Rest = "catching its breath",
    UI_BN_Bear_Tag_Down = "down",
    UI_BN_Bear_Tag_Dodge = "DODGE",
    UI_BN_Bear_MO_Dodge = "Show DODGE above bears",
    UI_BN_Bear_MO_DodgeTip = "Shows DODGE above your bear when an attack misses it - only on your screen.",
    UI_BN_Bear_Win_St_Fight = "Fighting",
    UI_BN_Bear_Win_St_Retreat = "Backing off",
    UI_BN_Bear_Win_St_Rest = "Catching its breath",
    UI_BN_Bear_Win_St_Down = "Down",
    UI_BN_Bear_Win_HintDown = "Your bear is down. Help it up, or it gets up on its own in %1 hour(s).",
    UI_BN_Bear_Win_Bandage = "Bandage",
    UI_BN_Bear_Win_HelpUp = "Help up",
    UI_BN_Bear_Win_BandageTip = "Uses one clean bandage from your inventory. Your bear heals faster for a while.",
    UI_BN_Bear_Win_HelpUpTip = "Takes a few seconds next to your bear. It gets up with almost half its health.",
    UI_BN_Bear_Win_Bandaged = "Bandaged: heals faster for %1 more hour(s).",
    UI_BN_Bear_Win_Fled = "With about %1 health left (%2 hits from death) it stops fighting and comes back to you.",
    UI_BN_Bear_Win_FledNever = "It never backs off on its own (sandbox setting).",
    UI_BN_Bear_Menu_Bandage = "Bandage the cub",
    UI_BN_Bear_Menu_BandageBig = "Bandage the bear",
    UI_BN_Bear_Menu_BandageTip = "%1 - heals faster for %2 hour(s).",
    UI_BN_Bear_Menu_HelpUp = "Help up the cub",
    UI_BN_Bear_Menu_HelpUpBig = "Help up the bear",
    UI_BN_Bear_Win_ShowDmg = "Show damage",
    UI_BN_Bear_Win_ShowDmgTip = "Shows the damage your bear deals above zombies and bandits - only on your screen, for all your bears.",
    UI_BN_Bear_Win_Melee = "Melee damage",
    UI_BN_Bear_Win_MeleeVal = "%1 per hit",
    UI_BN_Bear_Win_MeleeCub = "A cub does not fight. It hides behind you.",
    UI_BN_Bear_Win_MeleeTip = "Damage per hit right now, from its size and Fighting - the same numbers that float above zombies.",
    UI_BN_Bear_Win_MeleeSwipe = "Paw swipe: %1",
    UI_BN_Bear_Win_MeleeBite = "Bite: %1",
    UI_BN_Bear_Win_MeleeMaul = "Maul (enemy on the ground): %1",
    UI_BN_Bear_Win_MeleeSize = "From its size: %1%% of a full-grown bear",
    UI_BN_Bear_Win_MeleeFgt = "Fighting level %1: +%2%%",
    UI_BN_Bear_Win_MeleePct = "Sandbox: %1%% damage",
    UI_BN_Bear_Win_SkAgeMax = "max for its age",
    UI_BN_Bear_Win_SkAgeTip_Cub = "Level %1 is the most a cub can learn. More once it is half-grown (about day %2).",
    UI_BN_Bear_Win_SkAgeTip_Half = "Level %1 is the most a half-grown bear can learn. More once it is strong (about day %2).",
    UI_BN_Bear_Win_SkAgeTip_Strong = "Level %1 is the most a strong bear can learn. More once it is full-grown (about day %2).",
    UI_BN_Bear_Win_Kills = "Kills",
    UI_BN_Bear_Win_KillsVal = "zombies %1, bandits %2",
    UI_BN_Bear_Win_KillsTip = "Counts zombies and bandits that die right after your bear hit them, even if someone else landed the last blow.",
    -- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 8.1, 10): Namen der Aussehen (Schluessel stehen in B.LOOKS des Kerns), Knopf "Look"
    -- mit Uhr und Tooltips (die Uhr ist dieselbe wie bei Unstuck), Meldung des Schreibers und seine Ablehnungen (Big-Fassung = grosser
    -- Koerper, U.NoteText / U.TB)
    UI_BN_Bear_Look_Classic = "Classic",
    UI_BN_Bear_Look_Brown = "Brown",
    UI_BN_Bear_Look_Natural = "Natural",
    UI_BN_Bear_Win_Look = "Look: %1",
    UI_BN_Bear_Win_LookWait = "Look  %1",
    UI_BN_Bear_Win_LookTip = "Changes how your cub looks, right where it stands. Its health and stamina stay as they are.",
    UI_BN_Bear_Win_LookTipBig = "Changes how your bear looks, right where it stands. Its health and stamina stay as they are.",
    UI_BN_Bear_Win_LookShared = "Shares its wait time with Unstuck (%1 min).",
    UI_BN_Bear_Win_UnstuckShared = "Shares its wait time with Look (%1 min).",
    UI_BN_Bear_Win_LookWaitClock = "You can change its look again in %1.",
    UI_BN_Bear_Win_LookOne = "Your cub has only one look in this world.",
    UI_BN_Bear_Win_LookOneBig = "Your bear has only one look in this world.",
    UI_BN_Bear_Note_Look = "Your cub has a new look.",
    UI_BN_Bear_Note_LookBig = "Your bear has a new look.",
    UI_BN_Bear_Why_LookWait = "You can change your cub's look again in about %1 min.",
    UI_BN_Bear_Why_LookWaitBig = "You can change your bear's look again in about %1 min.",
    UI_BN_Bear_Why_LookDanger = "Not now: zombies or enemies are close to your cub.",
    UI_BN_Bear_Why_LookDangerBig = "Not now: zombies or enemies are close to your bear.",
    UI_BN_Bear_Why_LookBusy = "Not now: your cub is busy. Try again in a moment.",
    UI_BN_Bear_Why_LookBusyBig = "Not now: your bear is busy. Try again in a moment.",
    UI_BN_Bear_Why_LookFight = "Not now: your cub is fighting or catching its breath.",
    UI_BN_Bear_Why_LookFightBig = "Not now: your bear is fighting or catching its breath.",
    UI_BN_Bear_Why_LookGrow = "Your cub is about to grow. Try again in a moment.",
    UI_BN_Bear_Why_LookGrowBig = "Your bear is about to change its body. Try again in a moment.",
    UI_BN_Bear_Why_LookMissing = "This look is not available in this world.",
    UI_BN_Bear_Why_LookNoRoom = "There is no free spot right next to your cub.",
    UI_BN_Bear_Why_LookNoRoomBig = "There is no free spot right next to your bear.",
    -- F3 (Lauf baer-f3, PLAN_F3.md 11; Kevin 13.11.2026): Beduerfnisse, Vertrauen, Schlafen, Traenken, Fenster Variante B -- wortgleich
    -- mit Translate/EN/UI.json (Quelle _arbeit/baer_zaehmen/f3/werkzeug/texte_f3_daten.py). Entfernt: Win_Later, Win_LaterTip.
    UI_BN_Bear_Win_Needs = "Needs",
    UI_BN_Bear_Win_Fish = "Fish",
    UI_BN_Bear_Win_Inv = "Inventory",
    UI_BN_Bear_Win_Nose = "Nose alerts",
    UI_BN_Bear_Why_Later = "Comes with a later version.",
    UI_BN_Bear_Win_St_Sleep = "Sleeping",
    UI_BN_Bear_Win_HintSleep = "Your bear is asleep. Any order wakes it up.",
    UI_BN_Bear_Win_HintTired = "Your bear is too tired to fight. Let it sleep.",
    UI_BN_Bear_Win_HintNoTrust = "Your bear refuses to fight: it does not trust you enough. Feed, water and pet it.",
    UI_BN_Bear_Win_NeedNow = "Now: %1 (%2%%)",
    UI_BN_Bear_Win_HungerTip = "Rises while it is awake: from full to empty in 16 hours. A full bar is one day's food for its size - the bigger it gets, the more it needs. Nothing rises while it or you sleep. Hungry: slower, weaker, grows slower. Starving: no growth, no healing. At 100%% it loses health down to %1%%. It never dies of hunger.",
    UI_BN_Bear_Win_ThirstTip = "Rises like hunger: from full to empty in 16 hours awake. Right-click your bear: Give water - it drinks until it is full. Water it carries, it drinks by itself. Thirsty: slower, weaker, grows slower. Parched: no growth, no healing. At 100%% it loses health down to %1%%. It never dies of thirst.",
    UI_BN_Bear_Win_TiredTip = "Rises while your bear is awake - also while it follows you, and faster when it runs and fights. From %1%% it is too tired to fight and only backs off. At %2%% it falls asleep where it stands and sleeps until it is rested. Any order wakes it. When you sleep or fast-forward, it lies down next to you, whatever its order.",
    UI_BN_Bear_Win_SleepHeal = "Asleep it heals much faster - after a few hours of sleep it is almost full.",
    UI_BN_Bear_Win_TrustTip = "Starts at 0 and runs from -100%% to +100%%. Petting it, feeding it until it is full and watering it until it is full each bring +0.5 once a day. It drops by 5 when hunger or thirst reaches 90%%, by 10 when hunger or thirst brings it down to 1%% health (each at most once a day), and by 10 every time it goes down. At +100 its needs rise %1%% slower and a heart shows; at -100 they rise %2%% faster. Below %3%% it refuses to fight.",
    UI_BN_Bear_Win_TrustHeart = "At full trust a heart shows above its name tag.",
    UI_BN_Bear_Win_TrustDays = "Last days, oldest first: %1.",
    UI_BN_Bear_Win_TrustDay0 = "well cared for",
    UI_BN_Bear_Win_TrustDay1 = "hungry or thirsty",
    UI_BN_Bear_Win_TrustDay2 = "starving or parched",
    UI_BN_Bear_Win_NeedEffect2 = "Right now: it is slower and weaker and grows slower.",
    UI_BN_Bear_Win_NeedEffect3 = "Right now: it is much weaker, does not grow and does not heal on its own.",
    UI_BN_Bear_Win_NeedEffect4 = "Right now: it is losing health.",
    UI_BN_Bear_Win_Word_Hun1 = "Full",
    UI_BN_Bear_Win_Word_Hun2 = "Peckish",
    UI_BN_Bear_Win_Word_Hun3 = "Hungry",
    UI_BN_Bear_Win_Word_Hun4 = "Starving",
    UI_BN_Bear_Win_Word_Thr1 = "Quenched",
    UI_BN_Bear_Win_Word_Thr2 = "A little thirsty",
    UI_BN_Bear_Win_Word_Thr3 = "Thirsty",
    UI_BN_Bear_Win_Word_Thr4 = "Parched",
    UI_BN_Bear_Win_Word_Tir1 = "Rested",
    UI_BN_Bear_Win_Word_Tir2 = "Tired",
    UI_BN_Bear_Win_Word_Tir3 = "Very tired",
    UI_BN_Bear_Win_Word_Tir4 = "Exhausted",
    UI_BN_Bear_Win_TrustWord1 = "Distrustful",
    UI_BN_Bear_Win_TrustWord2 = "Wary",
    UI_BN_Bear_Win_TrustWord3 = "Neutral",
    UI_BN_Bear_Win_TrustWord4 = "Trusting",
    UI_BN_Bear_Win_TrustWord5 = "Devoted",
    UI_BN_Bear_Tag_Hunger = "Hunger %1%%",
    UI_BN_Bear_Tag_Thirst = "Thirst %1%%",
    UI_BN_Bear_Tag_Tired = "Tired %1%%",
    UI_BN_Bear_Tag_Trust = "Trust %1%%",
    UI_BN_Bear_Tag_Sleep = "sleeping",
    UI_BN_Bear_Tag_TiredBack = "too tired - backing off",
    UI_BN_Bear_Tag_TrustBack = "won't fight - backing off",
    UI_BN_Bear_MO_Hunger = "Hunger above tamed bears",
    UI_BN_Bear_MO_HungerTip = "Off, as a bar or as a number (percent). The bar fills as hunger grows. From 75%% it shows above your own bear anyway.",
    UI_BN_Bear_MO_Thirst = "Thirst above tamed bears",
    UI_BN_Bear_MO_ThirstTip = "Off, as a bar or as a number (percent). The bar fills as thirst grows. From 75%% it shows above your own bear anyway.",
    UI_BN_Bear_MO_Tired = "Tiredness above tamed bears",
    UI_BN_Bear_MO_TiredTip = "Off, as a bar or as a number (percent). The bar fills as tiredness grows. From 75%% it shows above your own bear anyway.",
    UI_BN_Bear_MO_Trust = "Trust above tamed bears",
    UI_BN_Bear_MO_TrustTip = "Off, as a bar or as a number (-100%% to +100%%): green when it trusts you, red when it does not. The heart at full trust belongs to the name tag, not to this setting.",
    UI_BN_Bear_MO_Sleep = "z Z z above sleeping bears",
    UI_BN_Bear_MO_SleepTip = "Small letters rise above a sleeping bear - only on your screen.",
    UI_BN_Bear_Menu_Water = "Give water to the cub",
    UI_BN_Bear_Menu_WaterBig = "Give water to the bear",
    UI_BN_Bear_Menu_WaterTip = "Drinks from the container until the thirst is gone or the water runs out.",
    UI_BN_Bear_Why_NotHungry = "Your cub is not hungry.",
    UI_BN_Bear_Why_NotHungryBig = "Your bear is not hungry.",
    UI_BN_Bear_Why_NotThirsty = "Your cub is not thirsty.",
    UI_BN_Bear_Why_NotThirstyBig = "Your bear is not thirsty.",
    UI_BN_Bear_Why_NoWater = "There is no water in that container.",
    UI_BN_Bear_Note_Fed = "Fed. Hunger %1%%.",
    UI_BN_Bear_Note_Drank = "Watered. Thirst %1%%.",
    UI_BN_Bear_Note_Hungry = "Your cub is hungry.",
    UI_BN_Bear_Note_HungryBig = "Your bear is hungry.",
    UI_BN_Bear_Note_Starving = "Your cub is starving! Feed it.",
    UI_BN_Bear_Note_StarvingBig = "Your bear is starving! Feed it.",
    UI_BN_Bear_Note_Thirsty = "Your cub is thirsty.",
    UI_BN_Bear_Note_ThirstyBig = "Your bear is thirsty.",
    UI_BN_Bear_Note_Parched = "Your cub is parched! Give it water.",
    UI_BN_Bear_Note_ParchedBig = "Your bear is parched! Give it water.",
    UI_BN_Bear_Note_Tired = "Your cub is worn out and needs sleep.",
    UI_BN_Bear_Note_TiredBig = "Your bear is too tired to fight. Let it sleep.",
    UI_BN_Bear_Note_NoTrust = "Your cub hardly trusts you. Feed, water and pet it.",
    UI_BN_Bear_Note_NoTrustBig = "Your bear refuses to fight: it does not trust you enough. Feed, water and pet it.",
    UI_BN_Bear_Note_TrustBack = "Your cub trusts you again.",
    UI_BN_Bear_Note_TrustBackBig = "Your bear trusts you enough to fight for you again.",
    UI_BN_Bear_Note_Collapse = "Your cub is exhausted and lies down to sleep.",
    UI_BN_Bear_Note_CollapseBig = "Your bear is exhausted and lies down to sleep.",
    UI_BN_Bear_Note_Rested = "Your cub wakes up, well rested.",
    UI_BN_Bear_Note_RestedBig = "Your bear wakes up, well rested.",
    UI_BN_Bear_Note_TrustTop = "Your cub trusts you completely.",
    UI_BN_Bear_Note_TrustTopBig = "Your bear trusts you completely.",
    UI_BN_Bear_Win_MealLine = "A jar of honey (20 hunger points) fills about %1%% of its daily need at its size.",
    UI_BN_Bear_Win_BowlLine = "Half a litre of water covers about %1%% of its daily need at its size.",
    UI_BN_Bear_Win_MeleeWeak = "%1 %2%%: %3%% of its normal damage.",
    UI_BN_Bear_Win_NeedsOff = "Hunger, thirst and tiredness are switched off in the sandbox settings.",
    -- F4 (Lauf baer-f4, PLAN_F4.md 13; Kevin 13.11.2026 abends): Traglast, Inventar-Fenster, Packtaschen, Gruende und Meldungen -- wortgleich
    -- mit Translate/EN/UI.json (Quelle _arbeit/baer_zaehmen/f4/werkzeug_ober/texte_f4_daten.py). Entfernt: Win_Carry, Win_CarryVal, Win_CarryTip.
    UI_BN_Bear_Win_Load = "Load",
    UI_BN_Bear_Win_LoadVal = "%1 / %2 kg",
    UI_BN_Bear_Win_LoadTip = "What your cub carries now, of how much it can carry. The more it grows, the more it carries: about %1 kg as a cub, %2 kg half-grown, %3 kg full-grown.",
    UI_BN_Bear_Win_LoadTipBig = "What your bear carries now, of how much it can carry. The more it grows, the more it carries: about %1 kg as a cub, %2 kg half-grown, %3 kg full-grown.",
    UI_BN_Bear_Win_LoadPacks = "Packs: on (+%1 kg)",
    UI_BN_Bear_Win_LoadNoPacks = "No packs",
    UI_BN_Bear_Win_LoadPacksTip = "Bear packs add %1 kg from half-grown. Sew them yourself (Tailoring 3) and put them on with a right-click on your bear.",
    UI_BN_Bear_Win_LoadOver = "Too heavy - it takes nothing new until it carries less.",
    UI_BN_Bear_Win_LoadPct = "Carrying capacity in the sandbox settings: %1%%.",
    UI_BN_Bear_Win_InvTip = "Look into its inventory - from anywhere. Put things in or take them out when you stand next to it.",
    UI_BN_Bear_Inv_Title = "Inventory: %1",
    UI_BN_Bear_Inv_Bear = "Your cub carries",
    UI_BN_Bear_Inv_BearBig = "Your bear carries",
    UI_BN_Bear_Inv_You = "You carry",
    UI_BN_Bear_Inv_Give = "Give",
    UI_BN_Bear_Inv_Take = "Take",
    UI_BN_Bear_Inv_All = "All",
    UI_BN_Bear_Inv_GiveTip = "Puts some into its inventory - you choose how many.",
    UI_BN_Bear_Inv_TakeTip = "Takes some out into your inventory - you choose how many.",
    UI_BN_Bear_Inv_Things = "%1 / %2 things",
    UI_BN_Bear_Inv_Kg = "%1 kg",
    UI_BN_Bear_Inv_Many = "%1 (%2)",
    UI_BN_Bear_Inv_PutOn = "Put on",
    UI_BN_Bear_Inv_TakeOff = "Take off",
    UI_BN_Bear_Inv_PutOnTip = "Takes a while. From half-grown your bear carries %1 kg more with them.",
    UI_BN_Bear_Inv_TakeOffTip = "The packs go into your inventory. Only works if everything still fits without them.",
    UI_BN_Bear_Inv_Empty = "Nothing in here yet.",
    UI_BN_Bear_Inv_YouEmpty = "Your inventory is empty.",
    UI_BN_Bear_Inv_Wait = "Waiting for your bear...",
    UI_BN_Bear_Inv_NoAnswer = "No answer - trying again in a moment.",
    UI_BN_Bear_Inv_Unknown = "Unknown item",
    UI_BN_Bear_Inv_Hint = "Give and Take ask how many; All moves the whole stack (up to 1000).",
    UI_BN_Bear_Inv_AllTake = "Take all %1.",
    UI_BN_Bear_Inv_AllTakeTip = "Takes the whole stack out in one go, as much as fits.",
    UI_BN_Bear_Inv_AllGive = "Give %1 of them.",
    UI_BN_Bear_Inv_AllGiveTip = "As many as fit. Favorites and things you hold or wear stay with you.",
    UI_BN_Bear_Inv_TipEach = "%1 kg each, %2 kg in all",
    UI_BN_Bear_Inv_TipCond = "Condition: %1%%",
    UI_BN_Bear_Inv_TipFresh = "Fresh",
    UI_BN_Bear_Inv_TipStale = "Stale",
    UI_BN_Bear_Inv_TipRotten = "Rotten",
    UI_BN_Bear_Inv_TipCooked = "Cooked",
    UI_BN_Bear_Inv_TipBurnt = "Burnt",
    UI_BN_Bear_Inv_TipFrozen = "Frozen",
    UI_BN_Bear_Inv_TipFluid = "Holds %1 l of %2",
    UI_BN_Bear_Inv_TipUses = "%1%% left",
    UI_BN_Bear_Inv_TipFav = "Favorite",
    UI_BN_Bear_Inv_TipFood = "Your cub eats this by itself when it gets hungry.",
    UI_BN_Bear_Inv_TipFoodBig = "Your bear eats this by itself when it gets hungry.",
    UI_BN_Bear_Inv_MineMore = "Only %1 kinds of your things are listed here.",
    UI_BN_Bear_Menu_Inv = "Open its inventory",
    UI_BN_Bear_Menu_PacksOn = "Put packs on the cub",
    UI_BN_Bear_Menu_PacksOnBig = "Put packs on the bear",
    UI_BN_Bear_Why_InvLossy = "Your cub cannot carry this without losing something about it.",
    UI_BN_Bear_Why_InvLossyBig = "Your bear cannot carry this without losing something about it.",
    UI_BN_Bear_Why_InvMain = "Only the first player can put things in or take them out.",
    UI_BN_Bear_Why_InvBagFirst = "Empty it first.",
    UI_BN_Bear_Why_InvFull = "Too heavy for your cub: %1 kg left.",
    UI_BN_Bear_Why_InvFullBig = "Too heavy for your bear: %1 kg left.",
    UI_BN_Bear_Why_InvCap = "Your cub already carries %1 things.",
    UI_BN_Bear_Why_InvCapBig = "Your bear already carries %1 things.",
    UI_BN_Bear_Why_InvWorn = "Take it off first.",
    UI_BN_Bear_Why_InvFar = "Walk to your cub to put things in or take them out.",
    UI_BN_Bear_Why_InvFarBig = "Walk to your bear to put things in or take them out.",
    UI_BN_Bear_Why_InvFight = "Not while your cub fights.",
    UI_BN_Bear_Why_InvFightBig = "Not while your bear fights.",
    UI_BN_Bear_Why_InvRoom = "Your inventory is full.",
    UI_BN_Bear_Why_InvCub = "A cub is too small for packs.",
    UI_BN_Bear_Why_InvPacks = "Take some things out first - without the packs it cannot carry it all.",
    UI_BN_Bear_Why_InvPacksBig = "Take some things out first - without the packs your bear cannot carry it all.",
    UI_BN_Bear_Why_InvHasPacks = "Your cub already wears packs.",
    UI_BN_Bear_Why_InvHasPacksBig = "Your bear already wears packs.",
    UI_BN_Bear_Why_InvGone = "That is no longer there.",
    UI_BN_Bear_Why_InvUnknown = "This item no longer exists in this world.",
    UI_BN_Bear_Why_InvData = "Your cub cannot keep track of that many different things. Take something out first.",
    UI_BN_Bear_Why_InvDataBig = "Your bear cannot keep track of that many different things. Take something out first.",
    UI_BN_Bear_Why_InvNoPacks = "You have no bear packs. Sew them first: Tailoring 3.",
    UI_BN_Bear_Note_InvPut = "Packed: %1 (%2).",
    UI_BN_Bear_Note_InvTook = "You took %1 (%2).",
    UI_BN_Bear_Note_InvTookSome = "You took %2 of %3 %1 - your inventory is full.",
    UI_BN_Bear_Note_InvAte = "Your cub ate %1 it was carrying.",
    UI_BN_Bear_Note_InvAteBig = "Your bear ate %1 it was carrying.",
    UI_BN_Bear_Note_InvDrop = "Your cub's things lie where it died.",
    UI_BN_Bear_Note_InvDropBig = "Your bear's things lie where it died.",
    UI_BN_Bear_Note_PacksOn = "Your cub wears its packs now.",
    UI_BN_Bear_Note_PacksOnBig = "Your bear wears its packs now.",
    UI_BN_Bear_Note_PacksOff = "You took the packs off your cub.",
    UI_BN_Bear_Note_PacksOffBig = "You took the packs off your bear.",
    -- K1 (Lauf baer-k1, PLAN_K1.md; Kevin 13./14.11.2026): Vertrauen -100..+100, Zahnrad, Schaden rot, Tagesbedarf, Zahlenfeld, Meldungen des
    -- Kerns -- wortgleich mit Translate/EN/UI.json (Quelle _arbeit/baer_zaehmen/k1/werkzeug_ober/texte_k1_daten.py).
    UI_BN_Bear_Win_TrustOpen = "Still possible today: %1.",
    UI_BN_Bear_Win_TrustDone = "Today's trust is earned - more tomorrow.",
    UI_BN_Bear_Win_TrustSrcPet = "petting",
    UI_BN_Bear_Win_TrustSrcFed = "feeding it until it is full",
    UI_BN_Bear_Win_TrustSrcDrank = "watering it until it is full",
    UI_BN_Bear_Note_TrustUpPet = "+0.5 trust: it enjoyed the petting.",
    UI_BN_Bear_Note_TrustUpFed = "+0.5 trust: you fed it until it was full.",
    UI_BN_Bear_Note_TrustUpDrank = "+0.5 trust: you gave it all the water it wanted.",
    UI_BN_Bear_Note_TrustHungry = "Your cub is starving and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustHungryBig = "Your bear is starving and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustThirsty = "Your cub is parched and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustThirstyBig = "Your bear is parched and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustDown = "Your cub went down and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustDownBig = "Your bear went down and trusts you less (-%1).",
    UI_BN_Bear_Note_TrustWeak = "Hunger and thirst wore your cub down to 1%% health (-%1 trust).",
    UI_BN_Bear_Note_TrustWeakBig = "Hunger and thirst wore your bear down to 1%% health (-%1 trust).",
    UI_BN_Bear_Num_Dec = ".",                          -- fix1 (R4): Dezimalzeichen der Sprache (shared/BanditsNPCBear.lua B.DecText)
    UI_BN_Bear_Why_LookCool = "Your cub only just grew or changed - try again in %1 s.",
    UI_BN_Bear_Why_LookCoolBig = "Your bear only just grew or changed - try again in %1 s.",
    UI_BN_Bear_Why_LookRetry = "Your cub could not change just now - try again in %1 s.",
    UI_BN_Bear_Why_LookRetryBig = "Your bear could not change just now - try again in %1 s.",
    UI_BN_Bear_Win_Gear = "Settings",
    UI_BN_Bear_Win_GearTip = "Show or hide what appears above this bear: name tag, health bar, damage numbers, growth line. Only on your screen.",
    UI_BN_Bear_Win_HpBar = "Health bar",
    UI_BN_Bear_Win_HpBarTip = "Shows the health bar above this bear, the way you chose it in the options. Only on your screen.",
    UI_BN_Bear_Win_HpBarOffAll = "Health above the bear is switched off for all bears in Options - Mods.",
    UI_BN_Bear_Win_DmgRedTip = "Red: hunger or thirst weakens it right now.",
    UI_BN_Bear_Win_MeleeNormal = "Normally %1 per hit, now %2.",
    UI_BN_Bear_Win_MeleeWas = "%1 (normally %2)",
    UI_BN_Bear_Win_NeedDay = "Daily need at its size: %1 hunger points (about %2 steaks) and %3 l of water.",
    UI_BN_Bear_Win_NeedsPaused = "Its needs are resting: %1.",
    UI_BN_Bear_Win_NeedsPausedSleep = "it is asleep",
    UI_BN_Bear_Win_NeedsPausedOwner = "you are asleep",
    UI_BN_Bear_Win_NeedsPausedFar = "you are too far away",
    UI_BN_Bear_Food_DayPct = "Fills it for about %1%% of its daily need.",
    UI_BN_Bear_Inv_HowMany = "How many do you give? (1 - %1)",
    UI_BN_Bear_Inv_HowManyTake = "How many do you take? (1 - %1)",
    UI_BN_Bear_Inv_CountBad = "Enter a whole number from 1 to %1.",
    UI_BN_Bear_Note_InvPutSome = "Packed %2 of %3 %1 - it can't carry more.",
    UI_BN_Bear_Note_InvDrank = "Your cub drank %1 l of the water it was carrying.",
    UI_BN_Bear_Note_InvDrankBig = "Your bear drank %1 l of the water it was carrying.",
}

local KEY_HEAD = "UI_BN_Bear_"
local DIRS = { N = true, NE = true, E = true, SE = true, S = true, SW = true, W = true, NW = true }
-- B1d (PLAN_B1D.md 6.5): feste Listen fuer die Werte, die der Kern in einer Meldung schickt (v). Nur diese Werte werden zu einem
-- Schluessel; alles andere wird "?" -- nie ein roher Schluessel und nie ein Text, den der Schreiber zusammengesetzt hat. Die
-- Schluessel stehen hier ausgeschrieben (nicht zusammengesetzt), damit jeder im Code zu finden ist.
local STAGE_KEY = { half = "UI_BN_Bear_Stage_Half", strong = "UI_BN_Bear_Stage_Strong", adult = "UI_BN_Bear_Stage_Adult" }
local SKILL_KEY = { agi = "UI_BN_Bear_Skill_Agi", vit = "UI_BN_Bear_Skill_Vit", con = "UI_BN_Bear_Skill_Con",
    fgt = "UI_BN_Bear_Skill_Fgt", fsh = "UI_BN_Bear_Skill_Fsh", nos = "UI_BN_Bear_Skill_Nos" }

-- ---------------------------------------------------------------------------
-- Texte
-- ---------------------------------------------------------------------------

-- Text zu einem Schluessel mit bis zu drei Einsetzungen. Uebersetzen und Einsetzen macht B.T (Kern); von hier kommt nur der
-- englische Ersatztext aus U.EN.
function U.T(key, a1, a2, a3)
    return B.T(key, U.EN[key] or key, a1, a2, a3)
end

-- B1e (PLAN_B1E.md 0.10, 6.5): Text je Koerper. bd = Koerper aus der Sicht oder der Meldung ("cub" / "big" / nil). Beim grossen
-- Koerper die Big-Fassung, aber nur, wenn es sie gibt (U.EN kennt sie -- dieselbe Liste wie EN/UI.json); sonst der Grundtext.
-- Der Schluessel "<key>Big" wird hier zusammengesetzt: jede Big-Fassung steht ausgeschrieben in U.EN oben.
function U.TB(key, bd, a1, a2, a3)
    if bd == "big" and type(key) == "string" and U.EN[key .. "Big"] ~= nil then
        return U.T(key .. "Big", a1, a2, a3)
    end
    return U.T(key, a1, a2, a3)
end

-- Dauer als Text: unter einer Stunde Minuten, sonst Stunden (Rundung macht B.WaitParts).
function U.WaitText(hours)
    local n, unitKey = B.WaitParts(tonumber(hours) or 0)
    return U.T(unitKey, n)
end

-- Text einer Ablehnung der Regel-Funktionen (B.CheckFeed, B.CheckPet, B.CheckBait): whyVal ist bei Wartezeiten die Reststunden,
-- bei der Sperre die Resttage, sonst nil (Plan 6.2.2).
-- F1 (PLAN_F1.md 4a, B1e-Rest A1/B6): bd = Koerper aus der Sicht ("big" -> Big-Fassung ueber U.TB, z. B. "The bear is gone."); ohne
-- bd wie bisher.
function U.WhyText(whyKey, whyVal, bd)
    if type(whyKey) ~= "string" then return "" end
    if whyVal == nil then return U.TB(whyKey, bd) end
    if whyKey == "UI_BN_Bear_Why_FeedWait" or whyKey == "UI_BN_Bear_Why_PetWait" then
        return U.TB(whyKey, bd, U.WaitText(whyVal))
    end
    if type(whyVal) == "number" then
        if whyKey == "UI_BN_Bear_Why_Locked" then return U.TB(whyKey, bd, math.ceil(whyVal)) end
        -- F2: Reststunden eines Verbands ganz, mindestens 1 (0,4 h -> "1 hour(s) left", nie "0")
        if whyKey == "UI_BN_Bear_Why_Bandaged" then return U.TB(whyKey, bd, math.max(1, math.floor(whyVal))) end
        return U.TB(whyKey, bd, math.floor(whyVal))
    end
    return U.TB(whyKey, bd, tostring(whyVal))
end

-- B1d (PLAN_B1D.md 6.5): Name einer Wachstums-Stufe ("half" / "strong" / "adult"), sonst "?". Gerufen fuer Meldungen und beim
-- Listenbau des Schilds (hoechstens 1 x je Sekunde), nie je Bild.
function U.StageName(key)
    if type(key) ~= "string" then return "?" end
    local k = STAGE_KEY[key]
    if k == nil then return "?" end
    return U.T(k)
end

-- Text einer Meldung des Schreibers: { k = Schluessel, t = "wait" / "days" / "dir" / "num" / "name" / "stage" / "skill" / nil,
-- v = Wert, w = zweiter Wert } (Plan 6.2.6; B1d PLAN_B1D.md 6.5: "stage" v = Stufe, "skill" v = Faehigkeit, w = neue Stufe 1..10).
-- Gibt nil, wenn die Meldung keine von uns ist.
-- B1e (PLAN_B1E.md 6.4): traegt die Meldung bd = "big" (der Kern haengt es an, wenn der Eintrag den grossen Koerper hat) und gibt es
-- die Big-Fassung des Schluessels, kommt diese ("Your bear follows you."); sonst der Grundtext wie bisher.
function U.NoteText(note)
    if type(note) ~= "table" then return nil end
    local key = note.k
    if type(key) ~= "string" or string.sub(key, 1, string.len(KEY_HEAD)) ~= KEY_HEAD then return nil end
    if note.bd == "big" and U.EN[key .. "Big"] ~= nil then key = key .. "Big" end
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
    elseif t == "stage" then
        return U.T(key, U.StageName(v))
    elseif t == "skill" then
        local sk = nil
        if type(v) == "string" then sk = SKILL_KEY[v] end
        local skName = "?"
        if sk ~= nil then skName = U.T(sk) end
        return U.T(key, skName, math.floor(tonumber(note.w) or 0))
    elseif t == "item" then
        -- F4 (f4/schnittstelle.md K7): v = voller Typ, nm = eigener Name (wahlfrei), w = Anzahl, x = gewollte Anzahl. Name des Typs ueber
        -- U.ItemName (client/BanditsNPCBearInvClient.lua; getItemNameFromFullType) -- nie ein Text, den der Schreiber zusammengesetzt hat.
        local name = note.nm
        if type(name) ~= "string" or name == "" then
            name = "?"
            if type(v) == "string" and U.ItemName then name = U.ItemName(v) end
        end
        return U.T(key, name, math.floor(tonumber(note.w) or 1), math.floor(tonumber(note.x) or 0))
    end
    return U.T(key)
end

-- ---------------------------------------------------------------------------
-- Namen fuer das Schild (B1b, PLAN_B1B.md 2.1, 5.4). Der Name lebt nur im Register (Plan 0.3); fehlt er, setzt der Client den
-- Vorgabe-Namen "<Spieler>'s cub" selbst zusammen -- der Schreiber kennt den Vornamen der Figur nicht und braucht ihn nicht.
-- Gerufen nur beim Listenbau des Schilds (hoechstens 1 x je Sekunde), nie je Bild.
-- ---------------------------------------------------------------------------

-- Vorname der eigenen Figur. getSpecificPlayer(0): client/Farming/CFarmingSystem.lua:45;
-- getDescriptor():getForename() an der Spielfigur: client/XpSystem/ISUI/ISCharacterScreen.lua:84.
function U.LocalName()
    local p = getSpecificPlayer(0)
    if not p then return "?" end
    local desc = p:getDescriptor()
    local name = desc and desc:getForename()
    if type(name) ~= "string" or name == "" then return "?" end
    return name
end

-- Zeile 1 des Schilds: der Name aus dem Register, sonst der Vorgabe-Name. Besitzer im Einzelspieler ist der feste Schluessel
-- B.SP_KEY ("__sp") -- der erscheint nie als Text, an seiner Stelle steht der Vorname der Figur. Im Mehrspieler ist der Besitzer
-- der Kontoname (so steht er in der Sicht). Der zweite Parameter (meKey, Schnittstelle 5.4) aendert daran nichts: auch das eigene
-- Junge heisst im Mehrspieler nach dem Kontonamen; ohne Besitzer steht "?". "__sp" im Mehrspieler (Junges eines frueheren
-- Einzelspieler-Stands) -> "?", nie der eigene Vorname (Nachbesserung B1b B8).
-- B1e (PLAN_B1E.md 6.5): beim grossen Koerper (Sicht bd == "big") heisst der Vorgabe-Name "<Spieler>'s bear" (Tag_NameBig).
function U.CubName(c, _meKey)
    if type(c) ~= "table" then return "" end
    local name = c.name
    if type(name) == "string" and name ~= "" then return name end
    local owner = c.owner
    local who
    if owner == nil then
        who = "?"
    elseif owner == B.SP_KEY then
        if B.IsSP ~= nil and B.IsSP() then who = U.LocalName() else who = "?" end
    else
        who = tostring(owner)
    end
    return U.TB("UI_BN_Bear_Tag_Name", c.bd, who)
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

-- B1c (PLAN_B1C.md 6.4): U.viewAt = Echtzeit (ms), zu der die letzte Sicht ankam. Die Sicht traegt Restzeiten in Sekunden
-- (callWait); das Menue rechnet damit die Restzeit zum Zeitpunkt des Klicks. getTimestampMs: V:client/Foraging/ISBaseIcon.lua:485.
function U.NoteSync()
    U.syncN = (U.syncN or 0) + 1
    U.viewAt = getTimestampMs()
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
    elseif command == "Inv" then
        -- F4 (f4/schnittstelle.md K4): eine Seite der Inventar-Liste NUR an den Besitzer; B.OnInv sammelt die Seiten (nur Anzeige)
        if B.OnInv then B.OnInv(args) end
    elseif command == "Fx" then
        -- F2 (PLAN_F2.md 4.4): ein Kampf-Ereignis { k = Art, ... } vom Server. B.OnFx (KERN) macht die Zombie-Seite (nur beim Zombie-Rechner)
        -- und ruft danach U.FightFx (client/BanditsNPCBearFx.lua). Nur Anzeige: dieser Client entscheidet und meldet nichts zurueck.
        if B.OnFx and type(args.k) == "string" then B.OnFx(args.k, args) end
    end
end

Events.OnServerCommand.Add(onServerCommand)         -- client/ServerCommands.lua:218
Events.OnGameStart.Add(onGameStart)                 -- client/Chat/ISChat.lua:1186
Events.OnTick.Add(helloTick)                        -- client/Chat/ISChat.lua:943
