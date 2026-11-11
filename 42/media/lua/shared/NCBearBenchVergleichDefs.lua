--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, tools/baer_uebernahme.py BENCH_ANY).
-- Kevin 11.11.2026: "ich will das du die 2 baby varianten einbaust zum spawnen und beide grosse!"
-- Vergleichs-Art "ncbearcubalt" = das ALTE Junge (Entwurf baer_baby) mit derselben Definition wie das echte Junge
-- (shared/BanditsNPCBearDefs.lua), nur eigenes Modell/Textur und feste Groesse 0,35. Unser Junge-Code fasst sie nie an
-- (er prueft getAnimalType() == "ncbearcub"). Form der Definition: Vanilla shared/Definitions/animal/DeerDefinitions.lua.
--
require "BanditsNPCBearDefs"

local SRC = "ncbearcub"
local ALT = "ncbearcubalt"
local BREED = "brown"

local src = AnimalDefinitions and AnimalDefinitions.animals and AnimalDefinitions.animals[SRC]
if src then
    local d = {}
    for k, v in pairs(src) do d[k] = v end
    d.bodyModel = "NCBearBenchCubAlt_Body"     -- scripts/NCBearBenchVergleich.txt
    d.minSize = 0.35
    d.maxSize = 0.35
    local stages = {}
    stages[ALT] = { ageToGrow = 36500 }      -- Eintrag gleich dem Artnamen (wie BanditsNPCBearDefs.lua:73)
    d.stages = stages
    local b = {}
    local sb = src.breeds and src.breeds[BREED]
    if sb then for k, v in pairs(sb) do b[k] = v end end
    b.name = BREED
    b.texture = "NCBearBenchCubAlt"
    b.textureMale = "NCBearBenchCubAlt"
    b.textureBaby = "NCBearBenchCubAlt"
    d.breeds = { [BREED] = b }
    AnimalDefinitions.animals[ALT] = d
    if AnimalAvatarDefinition and AnimalAvatarDefinition[SRC] then
        AnimalAvatarDefinition[ALT] = AnimalAvatarDefinition[SRC]
    end
    if AnimalPartsDefinitions and AnimalPartsDefinitions.animals and AnimalPartsDefinitions.animals[SRC .. BREED] then
        AnimalPartsDefinitions.animals[ALT .. BREED] = AnimalPartsDefinitions.animals[SRC .. BREED]
    end
end
