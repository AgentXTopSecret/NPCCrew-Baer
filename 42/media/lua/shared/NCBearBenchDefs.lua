--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Lauf baer-f2, PLAN_F2.md 1.1, 1.4.
-- Frueher shared/NCBearDefs.lua (heute ein Stummel). Die Stimmen der Rasse des GROSSEN Koerpers stehen seit F2 in
-- shared/BanditsNPCBearDefs.lua (KERN, Art "ncbeargrown"); hier stehen nur die Test-Arten:
--   "ncbear"    NEUE Test-Art (Kollisionsprobe 12.11.: 0 Treffer in NPC Crew, Vanilla, Bandits): der alte Erwachsene zum Ansehen der
--               Clips und Groessen (NCBear_SpawnLive(), NCBear_AnimTest(...)). Gruppe "ncbear" (= B.GROUP, Vanilla-Praxis Art = Gruppe:
--               V:shared/Definitions/animal/CowDefinitions.lua:235), Stufe "ncbear", Rasse "brown". Sie KAEMPFT NICHT (Frage F-G5):
--               gekaempft wird mit dem eigenen gezaehmten Baeren (NCBear_CubGrow, NCBear_FightZed).
--   "bear", "bearstag"  ALT-Arten, FELDGLEICH wie die alte shared/NCBearDefs.lua (nur verschoben): ein gespeichertes Tier einer
--               unbekannten Art bricht das Laden (shared/BanditsNPCBearDefs.lua Kopf) -- so laden Kevins alte Spielstaende ohne roten
--               Fehler; der alte Baer steht dann nur (kein Kampf-Code kennt "bear"). Wegraeumen: NCBear_OldClean() (client/NCBearBenchAdult.lua).
-- NPC Crew (nur Test-Mod, Riegel): die ALT-Gruppe "bear" ist kein Vieh -- der Kern traegt sie seit F2 nicht mehr ein
-- (shared/BanditsNPCBearCrew.lua), darum hier in OnGameBoot selbst (Form shared/BanditsNPCBearCrew.lua install).
-- Java liest AnimalDefinitions erst in IsoWorld.init (AnimalDefinitions.loadAnimalDefinitions), nach allen Lua-Dateien: nur Dateiebene.
-- Jedes Feld ist ein Schluessel, den AnimalDefinitions.loadAnimalDefinitions liest (alte Datei, gespielt); Werte nach
-- V:shared/Definitions/animal/DeerDefinitions.lua (buck), wo nichts anderes steht. Statisch geprueft, nicht gespielt.
--

AnimalDefinitions = AnimalDefinitions or {}                     -- V:shared/Definitions/animal/DeerDefinitions.lua:1
AnimalDefinitions.animals = AnimalDefinitions.animals or {}     -- DeerDefinitions.lua:56

-- Gene wie die alte Datei: nur vorhandene (DeerDefinitions.lua:20-31), kein maxSize-Gen; meatRatio ist Pflicht fuer den Tod.
local function gene()
    return {
        meatRatio = "meatRatio",
        maxWeight = "maxWeight",
        resistance = "resistance",
        strength = "strength",
        hungerResistance = "hungerResistance",
        thirstResistance = "thirstResistance",
        stress = "stress",
    }
end

-- Rasse wie die alte Datei (Textur NCBear, Symbole des Rehs, Stimmen aus scripts/nc_bear_sounds.txt; Form CowDefinitions.lua:315-330).
local function rassen()
    return {
        brown = {
            name = "brown",
            texture = "NCBear",
            textureMale = "NCBear",
            invIconMale = "Item_DeerMale_Dead",
            invIconFemale = "Item_DeerFemale_Dead",
            invIconMaleDead = "Item_DeerMale_Dead",
            invIconFemaleDead = "Item_DeerFemale_Dead",
            invIconMaleSkel = "Item_Skeleton_Deer_Stag",
            invIconFemaleSkel = "Item_Skeleton_Deer_Doe",
            sounds = {
                fallover = { name = "AnimalFoleyBuckBodyfall" },
                pain = { name = "NCBear_Pain", slot = "voice", priority = 50 },
                death = { name = "NCBear_Pain", slot = "voice", priority = 100 },
                huff = { name = "NCBear_Huff", slot = "voice", priority = 10 },
                huffsoft = { name = "NCBear_HuffSoft", slot = "voice", priority = 5 },
                growl1 = { name = "NCBear_Growl1", slot = "voice", priority = 20 },
                growl2 = { name = "NCBear_Growl2", slot = "voice", priority = 20 },
                growl3 = { name = "NCBear_Growl3", slot = "voice", priority = 20 },
            },
        },
    }
end

-- Eine Test-Art. name = Artname (= Stufe), modell = model-Skript in module Base, gruppe = Gruppe.
local function baer(name, modell, gruppe)
    local stufen = {}
    stufen[name] = { ageToGrow = 60 }     -- Eintrag gleich dem Tiernamen, ageToGrow >= 1 (alte Datei)
    return {
        bodyModel = modell,               -- scripts/nc_bear_tier.txt (NCBear_Body) bzw. scripts/NCBearBenchStag.txt (NCBearStag_Body)
        animset = "buck",
        group = gruppe,                   -- Pflicht fuer das Debug-Menue (V:client/DebugUIs/DebugContextMenu.lua:253)
        male = true,
        stages = stufen,
        breeds = rassen(),
        genes = gene(),
        minSize = 1.0,
        maxSize = 1.0,
        animalSize = 0.3,
        collisionSize = 0.42,
        shadoww = 0.9,
        shadowfm = 1.8,
        shadowbm = 1.8,
        corpseSize = 3.0,
        minWeight = 200,
        maxWeight = 400,
        minBlood = 1500,
        maxBlood = 4000,
        trailerBaseSize = 600,
        wild = false,
        canBeDomesticated = false,
        fleeZombies = false,
        alwaysFleeHumans = false,
        canThump = false,
        canBePicked = false,
        canBeAlerted = false,
        sitRandomly = false,
        dontAttackOtherMale = true,
        wanderMul = 600,
        idleTypeNbr = 0,
        spottingDist = 10,
    }
end

AnimalDefinitions.animals["ncbear"] = baer("ncbear", "NCBear_Body", "ncbear")
-- ALT-Arten: Felder genau wie die alte shared/NCBearDefs.lua (Gruppe "bear")
AnimalDefinitions.animals["bear"] = baer("bear", "NCBear_Body", "bear")
AnimalDefinitions.animals["bearstag"] = baer("bearstag", "NCBearStag_Body", "bear")

-- Fenster "Tier-Info": ohne Eintrag wirft V:client/ISUI/Animal/ISAnimalUI.lua (avatarDefinition.zoom). Felder vom Reh
-- (V:shared/Definitions/animal/AnimalAvatarDefinition.lua "buck"), ohne hook (wie die alte Datei).
local b = AnimalAvatarDefinition and AnimalAvatarDefinition["buck"]
if b then
    for _, name in ipairs({ "ncbear", "bear", "bearstag" }) do
        AnimalAvatarDefinition[name] = {
            zoom = b.zoom,
            xoffset = b.xoffset,
            yoffset = b.yoffset,
            avatarWidth = b.avatarWidth,
            avatarDir = b.avatarDir,
            trailerDir = b.trailerDir,
            trailerZoom = b.trailerZoom,
            trailerXoffset = b.trailerXoffset,
            trailerYoffset = b.trailerYoffset,
        }
    end
end

-- Teile beim Zerlegen: Attrappe vom Reh, Schluessel Tiername .. Rasse (V:shared/Definitions/animal/ButcheringUtil.lua:18, alte Datei)
if AnimalPartsDefinitions and AnimalPartsDefinitions.animals then
    AnimalPartsDefinitions.animals["ncbearbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
    AnimalPartsDefinitions.animals["bearbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
    AnimalPartsDefinitions.animals["bearstagbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
end

-- NPC Crew (nur in der Test-Mod, Riegel): die ALT-Gruppe "bear" ist kein Vieh. Die neue Gruppe "ncbear" traegt der Kern ein
-- (shared/BanditsNPCBearCrew.lua). Events.OnGameBoot.Add: V:client/Foraging/ISSearchManager.lua:1481. Ohne NPC Crew: nichts.
local benchCrewDone = false
local function benchCrew()
    if benchCrewDone then return end
    benchCrewDone = true
    local crew = BanditsNPC and BanditsNPC.Livestock
    if crew == nil or type(crew.NOT_TENDED) ~= "table" then return end
    crew.NOT_TENDED["bear"] = true
end
Events.OnGameBoot.Add(benchCrew)
