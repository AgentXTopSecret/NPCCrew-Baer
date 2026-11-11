--
-- NPC Crew -- Baer, Tierart des Jungen "ncbearcub" (B1a, PLAN_ZAEHMEN.md 6.5).
--
-- Java liest AnimalDefinitions.animals erst in IsoWorld.init (AnimalDefinitions.loadAnimalDefinitions), nach allen Lua-Dateien.
-- Deshalb steht die Definition auf Dateiebene; spaetere Aenderungen (auch aus Sandbox-Werten) sieht die Engine nicht mehr.
-- Form: NCBearTest shared/NCBearDefs.lua:62-127 (der Erwachsene "bear", gespielt). Diese Datei aendert nichts Fremdes,
-- sie legt nur neue Schluessel an (Naht 6).
--
-- Der Artname ist ENDGUELTIG: ein gespeichertes Tier einer unbekannten Art bricht das Laden des Spielstands.
--
-- Bauart der Scheu (Plan 0.1): NICHT wild. Ein wildes Tier flieht unter 3 Kacheln immer, Fuettern aus der Hand waere damit
-- nicht zuverlaessig. "Scheu" ist ein Zustand im Register; das Weglaufen macht der Takt des Schreibers.
-- Eine Stufe gleich dem Artnamen, ohne nextStage (dann kein Stufenwechsel, isBaby() ist falsch). Das Wachsen (B1d) macht NICHT die
-- Engine, sondern das Register (rec.g, server/BanditsNPCBearGrow.lua); die Engine bekommt nur die Groesse (B.ApplySize).
-- B1d (PLAN_B1D.md 0.3, Weg B, Frage F1): minSize 0,35 / maxSize 1,35 und ageToGrow 36500. Grund (NUR JAR, forschung_b1d.md 0.2,
-- 1.2-1.3): die Engine klemmt die Groesse beim Laden, bei der Mehrspieler-Erstuebertragung, je Alterstag (growUp) und in einer Tierzone
-- auf [minSize, maxSize] -- bei min = max fiele jede gesetzte Groesse dort auf 0,35 zurueck. Neue Koerper starten weiter bei minSize 0,35
-- (initSize endet mit setSize(0.1F), dec/AnimalData.java:1353-1358); das Engine-Wachsen je Alterstag ist (max - min) / ageToGrow x Leben
-- = praktisch 0. Lehnt Kevin F1 ab, werden nur maxSize und ageToGrow zurueckgedreht (das Nachsetzen je Hirn-Takt deckt beides).
-- B1e (PLAN_B1E.md 2.1, 2.2, 0.13): zweite Art "ncbeargrown" = der GROSSE Koerper desselben Eintrags (ab Halbstark, waechst bis 1,35).
-- Kopie der Junges-Definition (Felder per pairs, eigene stages/breeds/genes), mit dem heutigen grossen Modell (model-Skript des
-- Erwachsenen, NCBearTest media/scripts/nc_bear_tier.txt; Textur wie NCBearTest shared/NCBearDefs.lua:40-41), minSize 0,72 (= B.CFG.swapSize) / maxSize 1,35, Schatten/Leiche wie der Erwachsene. KEINE
-- Erwachsenen-Stimmen und NIE die alte Art "bear" (NCBearTest shared/NCBearFight.lua:1787 kennt nur "bear"; Kampf ist B5a).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}

AnimalDefinitions = AnimalDefinitions or {}                     -- Vanilla shared/Definitions/animal/DeerDefinitions.lua:1
AnimalDefinitions.animals = AnimalDefinitions.animals or {}     -- DeerDefinitions.lua:56

local CUB = "ncbearcub"
local BREED = "brown"

-- Gene wie beim Erwachsenen (NCBearDefs.lua:16-26), ohne maxSize-Gen: dann sind die Grenzen genau minSize / maxSize der Definition
-- (NUR JAR dec/AnimalData.java:1717-1751).
-- meatRatio ist Pflicht fuer den Tod (Vanilla ButcheringUtil).
local genes = {
    meatRatio = "meatRatio",
    maxWeight = "maxWeight",
    resistance = "resistance",
    strength = "strength",
    hungerResistance = "hungerResistance",
    thirstResistance = "thirstResistance",
    stress = "stress",
}

-- Rasse. texture UND textureMale (textureBaby allein wirkt ohne nextStage nicht), Datei media/textures/Body/NCBearCub.png.
-- Symbole des Rehs als Attrappe (DeerDefinitions.lua:44-54, wie NCBearDefs.lua:42-47). Keine Erwachsenen-Stimme am Jungen:
-- nur der Aufprall (DeerDefinitions.lua:185).
local breeds = {}
breeds[BREED] = {
    name = BREED,
    texture = "NCBearCub",
    textureMale = "NCBearCub",
    textureBaby = "NCBearCub",
    invIconMale = "Item_DeerMale_Dead",
    invIconFemale = "Item_DeerFemale_Dead",
    invIconMaleDead = "Item_DeerMale_Dead",
    invIconFemaleDead = "Item_DeerFemale_Dead",
    invIconMaleSkel = "Item_Skeleton_Deer_Stag",
    invIconFemaleSkel = "Item_Skeleton_Deer_Doe",
    sounds = {
        fallover = { name = "AnimalFoleyBuckBodyfall" },
        -- Fix 3 (Kevin 10.11.2026: "wieso macht streicheln keinen sound wie bei tiere streicheln"): Streichel-Ton der Hand wie beim
        -- Kalb (Form CowDefinitions.lua:340 "petting = { name = "PetAnimalCalf" }", Ton category Player,
        -- scripts/generated/sounds/player/sounds_player_farming.txt:57). Vanilla spielt ihn ueber das Anim-Ereignis PlayBreedSound
        -- im idlePetting-Knoten der Kuh (AnimSets/cow/idle/idlePetting.xml:13); das Animset buck hat keinen solchen Knoten, deshalb
        -- spielt ihn unsere Zeitaktion selbst (BanditsNPCBearPetAction.lua start).
        petting = { name = "PetAnimalCalf" },
    },
}

local stages = {}
-- B1d: ageToGrow 36500 (100 Jahre; ganze Zahl, NUR JAR dec/AnimalDefinitions.java:813-814) -> die Engine waechst selbst nicht
stages[CUB] = { ageToGrow = 36500 }       -- Eintrag gleich dem Artnamen; kein nextStage (Wachsen: Register, B1d)

AnimalDefinitions.animals[CUB] = {
    bodyModel = "NCBearCub_Body",         -- model-Skript in module Base (scripts/nc_bear_cub.txt)
    animset = "buck",                     -- Vanilla-Gruppe; das Junge traegt dieselben 15 Clip-Namen wie der Erwachsene
    group = "ncbear",                     -- neu und endgueltig; braucht IGUI_Animal_Group_ncbear
    male = true,
    stages = stages,
    breeds = breeds,
    genes = genes,
    minSize = 0.35,                       -- Kevin: Jungtier 0,35; das Netz ist bei 1,0 gebaut
    maxSize = 1.35,                       -- B1d (Weg B, F1): Kevin "mach den finalen baeren doch auf 1,35" (ENTSCHEIDUNGEN.md:10)
    animalSize = 0.1,                     -- nach dem Kitz (DeerDefinitions.lua:65-66); ungespielt
    collisionSize = 0.24,
    shadoww = 0.4,                        -- DeerDefinitions.lua:68 (Kitz: fm/bm 1, hier 0.8)
    shadowfm = 0.8,
    shadowbm = 0.8,
    minWeight = 8,
    maxWeight = 20,
    corpseSize = 1.0,
    minBlood = 200,
    maxBlood = 500,
    trailerBaseSize = 100,
    wild = false,                         -- Plan 0.1
    canBeDomesticated = false,
    alwaysFleeHumans = false,             -- Vorgabe waere true; die Scheu spielt unser Takt
    fleeZombies = false,                  -- Vorgabe waere true; NPC Crew setzt fuer nicht wilde Arten ohnehin false
    canBePicked = false,                  -- Vorgabe waere true: kein Aufheben
    canThump = false,                     -- Vorgabe waere true
    canBeAlerted = false,
    sitRandomly = false,
    needMom = false,                      -- Vanilla shared/Definitions/animal/ChickenDefinitions.lua:127
    -- canBePet, canBeFeedByHand, canBeAttached, hungerMultiplier, thirstMultiplier fehlen mit Absicht (Vorgabe false bzw. 0):
    -- kein Vanilla-Streicheln, kein Anleinen, kein Hunger. Fuettern und Streicheln sind eigene Zeitaktionen.
    feedByHandAnim = "AnimalLureLow",     -- Haltung der Figur beim Fuettern (DeerDefinitions.lua:92)
    dontAttackOtherMale = true,
    wanderMul = 600,
    idleTypeNbr = 0,
    spottingDist = 10,
}

-- Fenster "Animal info" und NPC Crews Portrait lesen AnimalAvatarDefinition[Art]; ohne Eintrag wirft Vanilla
-- client/ISUI/Animal/ISAnimalUI.lua:31. Felder vom Reh (Vanilla AnimalAvatarDefinition.lua:231-240), ohne hook.
if AnimalAvatarDefinition then
    local buck = AnimalAvatarDefinition["buck"]
    if buck then
        AnimalAvatarDefinition[CUB] = {
            zoom = buck.zoom,
            xoffset = buck.xoffset,
            yoffset = buck.yoffset,
            avatarWidth = buck.avatarWidth,
            avatarDir = buck.avatarDir,
            trailerDir = buck.trailerDir,
            trailerZoom = buck.trailerZoom,
            trailerXoffset = buck.trailerXoffset,
            trailerYoffset = buck.trailerYoffset,
        }
    end
end

-- Teile beim Zerlegen: Attrappe vom Kitz (Vanilla AnimalPartsDefinitions.lua:456-465), Schluessel Art .. Rasse
-- (Vanilla ButcheringUtil.lua:18). Stirbt ein Junges, entsteht eine Leiche; ohne Eintrag wuerfe das Zerlegen.
if AnimalPartsDefinitions and AnimalPartsDefinitions.animals then
    AnimalPartsDefinitions.animals[CUB .. BREED] = AnimalPartsDefinitions.animals["fawnwhitetailed"]
end

-- ---------------------------------------------------------------------------
-- B1e (PLAN_B1E.md 2.2): der grosse Koerper "ncbeargrown". Artname ENDGUELTIG (steht in Spielstaenden, siehe Kopf).
-- ---------------------------------------------------------------------------
local BIG = "ncbeargrown"

local function copyOf(t)
    local out = {}
    if type(t) == "table" then
        for k, v in pairs(t) do out[k] = v end
    end
    return out
end

local cubDef = AnimalDefinitions.animals[CUB]
if cubDef then
    local d = copyOf(cubDef)
    d.bodyModel = "NCBear_Body"            -- heutiges grosses Modell (model-Skript in module Base, media/scripts/nc_bear_tier.txt)
    -- Rasse: Kopie der Junges-Rasse (Symbole, Stimmen fallover/petting -- keine Erwachsenen-Stimmen bis B5a), Textur des grossen
    -- Baeren (media/textures/Body/NCBear.png); texture UND textureMale (textureBaby allein wirkt ohne nextStage nicht)
    local b = copyOf(breeds[BREED])
    b.name = BREED
    b.texture = "NCBear"
    b.textureMale = "NCBear"
    b.textureBaby = "NCBear"
    b.sounds = copyOf(breeds[BREED].sounds)
    d.breeds = { [BREED] = b }
    local st = {}
    st[BIG] = { ageToGrow = 36500 }        -- Eintrag gleich dem Artnamen, kein nextStage (wie das Junge, PLAN_B1D.md 0.3)
    d.stages = st
    d.genes = copyOf(genes)
    d.minSize = 0.72                       -- = B.CFG.swapSize (shared/BanditsNPCBear.lua); ein frischer Koerper steht so gleich bei 0,72
    d.maxSize = 1.35                       -- Kevin: Erwachsen 1,35 (baer/begleiter/ENTSCHEIDUNGEN.md:10)
    d.animalSize = 0.3                     -- wie "bear" (NCBearTest shared/NCBearDefs.lua:75)
    d.collisionSize = 0.30                 -- wirkt x Groesse: 0,22 beim Tausch, 0,41 bei 1,35 (Frage F10, im Spiel ansehen)
    d.shadoww = 0.9                        -- wie "bear" (NCBearDefs.lua:77-80)
    d.shadowfm = 1.8
    d.shadowbm = 1.8
    d.corpseSize = 3.0
    d.minWeight = 60                       -- Vorschlag (kein Hochheben, kein Anhaenger)
    d.maxWeight = 200
    d.minBlood = 800
    d.maxBlood = 2000
    d.trailerBaseSize = 300
    -- Nachbesserung B1e B4: Haltung der Figur beim Fuettern wie bei grossen Vanilla-Tieren (Kuh CowDefinitions.lua:245, Hirschkuh
    -- DeerDefinitions.lua:137; Knoten AnimSets/player/actions/AnimalLureHigh.xml) statt gebueckt wie beim Jungen (oben "AnimalLureLow").
    -- Die Fuetter-Aktion spielt a:getFeedByHandAnim() (shared/TimedActions/BanditsNPCBearFeedAction.lua). Im Spiel ansehen.
    d.feedByHandAnim = "AnimalLureHigh"
    AnimalDefinitions.animals[BIG] = d
end

-- Fenster "Animal info": Werte vom Reh wie beim Jungen (oben); ohne Eintrag wirft Vanilla client/ISUI/Animal/ISAnimalUI.lua:31.
if AnimalAvatarDefinition then
    local buck = AnimalAvatarDefinition["buck"]
    if buck then
        AnimalAvatarDefinition[BIG] = {
            zoom = buck.zoom,
            xoffset = buck.xoffset,
            yoffset = buck.yoffset,
            avatarWidth = buck.avatarWidth,
            avatarDir = buck.avatarDir,
            trailerDir = buck.trailerDir,
            trailerZoom = buck.trailerZoom,
            trailerXoffset = buck.trailerXoffset,
            trailerYoffset = buck.trailerYoffset,
        }
    end
end

-- Teile beim Zerlegen: Attrappe vom Rehbock wie der Erwachsene (NCBearTest shared/NCBearDefs.lua:125), Schluessel Art .. Rasse
-- (Vanilla ButcheringUtil.lua:18).
if AnimalPartsDefinitions and AnimalPartsDefinitions.animals then
    AnimalPartsDefinitions.animals[BIG .. BREED] = AnimalPartsDefinitions.animals["buckwhitetailed"]
end
