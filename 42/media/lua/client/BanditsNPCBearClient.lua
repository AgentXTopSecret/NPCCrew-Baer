--
-- NPC Crew -- Baer, Client-Seite der Befehle und Meldungen (B1a, PLAN_ZAEHMEN.md 5.6, 6.2.4, 6.2.6; B1b, PLAN_B1B.md 5.4:
-- Namen fuer das Schild, neue Texte; B1c, PLAN_B1C.md 6.4/6.7: neue Texte, Ankunftszeit der Sicht U.viewAt; B1d, PLAN_B1D.md
-- 6.5/6.7: Meldungen "stage" (Stufe erreicht) und "skill" (Faehigkeit gestiegen), U.StageName, Texte fuer Schild und Optionen;
-- B1e, PLAN_B1E.md 6.4/6.5/6.8: Texte je Koerper -- U.TB, Big-Fassungen in U.NoteText und U.CubName, Texte der Markierungs-Groesse;
-- F1, PLAN_F1.md 4a/7.6: Texte des Baeren-Fensters und der neuen Befehle, U.WhyText mit Koerper bd).
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
    UI_BN_Bear_Tip_Mix = "Taking turns between feeding and petting earns more trust.",
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
    UI_BN_Bear_MO_TagShowTip = "Name and state. The taming bar always shows.",
    UI_BN_Bear_MO_TagSize = "Size of the display above bears (%%)",
    UI_BN_Bear_MO_TagSizeTip = "100, 150 or 200.",
    -- B1d (PLAN_B1D.md 6.7): Werte-Zeilen des Schilds, Stufen, Faehigkeiten, zwei Meldungen des Kerns, Anzeige-Optionen
    UI_BN_Bear_Tag_Health = "Health %1/%2",
    UI_BN_Bear_Tag_Stamina = "Stamina %1/%2",
    UI_BN_Bear_Tag_Age = "Day %1 - %2 in %3 day(s)",
    UI_BN_Bear_Tag_AgeDone = "Day %1 - full-grown",
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
    UI_BN_Bear_MO_AgeTip = "Growth day and when the next stage comes.",
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
    -- (Why_GoneBig, Note_DeadBig, Menu_HoldBig, Menu_HoldTipBig). Die zwei Tasten-Schluessel UI_optionscreen_binding_* liest
    -- Vanillas Tastaturbelegung selbst (nur in UI.json).
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
    UI_BN_Bear_Win_Carry = "Can carry",
    UI_BN_Bear_Win_CarryVal = "up to %1",
    UI_BN_Bear_Win_None = "--",
    UI_BN_Bear_Win_Later = "Coming later:",
    UI_BN_Bear_Win_Hunger = "Hunger",
    UI_BN_Bear_Win_Thirst = "Thirst",
    UI_BN_Bear_Win_Tired = "Tiredness",
    UI_BN_Bear_Win_Trust = "Trust",
    UI_BN_Bear_Win_HealthTip = "Grows every day as your bear grows, and with Toughness. Heals slowly on its own.",
    UI_BN_Bear_Win_StaminaTip = "Drops while your bear runs and comes back while it rests. More with Endurance. It matters once bears fight (comes later).",
    UI_BN_Bear_Win_CarryTip = "How much your bear could carry. Its own inventory and bags come later.",
    UI_BN_Bear_Win_LaterTip = "Hunger, thirst, tiredness and trust come with a later version. Nothing is counted yet.",
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
    UI_BN_Bear_Win_LaterFight = "Works once bears fight - comes later.",
    UI_BN_Bear_Win_LaterFish = "Fishing comes later.",
    UI_BN_Bear_Win_LaterNose = "Comes later and can be switched off.",
    UI_BN_Bear_Win_LaterGrow = "Only grows once bears fight - comes later. The bonus already counts.",
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
    UI_BN_Bear_Win_PassiveTip = "Your bear stays out of fights and keeps to its order or comes back to you. No effect yet: fighting comes with a later version. A cub never fights anyway.",
    UI_BN_Bear_Win_TagTip = "Shows the name above this bear - only on your screen.",
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
    UI_BN_Bear_Menu_WindowTip = "Also opens with a key - Options, Key bindings, NPC Crew: Bear.",
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
    UI_BN_Bear_Note_PassiveOn = "Your cub is passive now. It keeps out of fights once bears can fight (comes later).",
    UI_BN_Bear_Note_PassiveOnBig = "Your bear is passive now. It keeps out of fights once bears can fight (comes later).",
    UI_BN_Bear_Note_PassiveOff = "Your cub is no longer passive.",
    UI_BN_Bear_Note_PassiveOffBig = "Your bear is no longer passive.",
    UI_BN_Bear_Why_OutOfReach = "Your cub is out of reach. Use Unstuck.",
    UI_BN_Bear_Why_OutOfReachBig = "Your bear is out of reach. Use Unstuck.",
    UI_BN_Bear_Why_GoneBig = "The bear is gone.",
    UI_BN_Bear_Note_DeadBig = "Your bear is dead.",
    UI_BN_Bear_Menu_HoldBig = "Hold out food for the bear",
    UI_BN_Bear_Menu_HoldTipBig = "Takes it in your hand. Stand still and the bear comes closer.",
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
    end
end

Events.OnServerCommand.Add(onServerCommand)         -- client/ServerCommands.lua:218
Events.OnGameStart.Add(onGameStart)                 -- client/Chat/ISChat.lua:1186
Events.OnTick.Add(helloTick)                        -- client/Chat/ISChat.lua:943
