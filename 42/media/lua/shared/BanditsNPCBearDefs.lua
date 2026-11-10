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
-- Kein Wachsen in B1a: eine Stufe gleich dem Artnamen, ohne nextStage (dann kein Stufenwechsel, isBaby() ist falsch).
-- Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}

AnimalDefinitions = AnimalDefinitions or {}                     -- Vanilla shared/Definitions/animal/DeerDefinitions.lua:1
AnimalDefinitions.animals = AnimalDefinitions.animals or {}     -- DeerDefinitions.lua:56

local CUB = "ncbearcub"
local BREED = "brown"

-- Gene wie beim Erwachsenen (NCBearDefs.lua:16-26), ohne maxSize: dann ist die Groesse genau minSize = maxSize.
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
    },
}

local stages = {}
stages[CUB] = { ageToGrow = 60 }          -- Eintrag gleich dem Artnamen, ageToGrow >= 1; kein nextStage (Wachsen ist B1b)

AnimalDefinitions.animals[CUB] = {
    bodyModel = "NCBearCub_Body",         -- model-Skript in module Base (scripts/nc_bear_cub.txt)
    animset = "buck",                     -- Vanilla-Gruppe; das Junge traegt dieselben 15 Clip-Namen wie der Erwachsene
    group = "ncbear",                     -- neu und endgueltig; braucht IGUI_Animal_Group_ncbear
    male = true,
    stages = stages,
    breeds = breeds,
    genes = genes,
    minSize = 0.35,                       -- Kevin: Jungtier 0,35; das Netz ist bei 1,0 gebaut
    maxSize = 0.35,
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
