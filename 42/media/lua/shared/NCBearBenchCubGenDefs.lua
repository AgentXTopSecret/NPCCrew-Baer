--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Lauf baer-gen-junges-v2, 12.11.2026.
-- Kevin 12.11.2026: "starte noch einen workflow fuer den anderen baby baeren mach da auch das gesicht besser und vorallem die beine";
-- das Generator-Junge kommt nur als Vergleich per Testbefehl NCBear_CubGen() zurueck (client/NCBearBenchCubGen.lua).
--
-- Zwei Vergleichs-Arten, beide mit derselben Definition wie das echte Junge (shared/BanditsNPCBearDefs.lua), Form GENAU wie
-- shared/NCBearBenchVergleichDefs.lua (ncbearcubalt, gespielt): flache Kopie, eigene Stufe, eigene Rasse, Groesse 0,35 .. 1,35.
--   "ncbearcubgen"  das neue Generator-Junge (Foto C, kurze Beine, Baerenfuesse, groesseres Gesicht): eigenes Modell/Textur
--                   NCBearBenchCubGen (scripts/NCBearBenchCubGen.txt, textures/Body/NCBearBenchCubGen.png)
--   "ncbearcubstd"  das Standard-Junge der Test-Mod als Massstab daneben: Modell und Textur bleiben die des echten Jungen
--                   (NCBearCub_Body / NCBearCub). Eigene Art statt eines echten "ncbearcub", damit (1) beide genau gleich behandelt
--                   werden (nur Engine, kein Baeren-Kern) und Gang/Tempo fair vergleichbar sind, (2) der Kern es nie als Waise sieht
--                   und (3) die Testhilfe nie dein eigenes gezaehmtes Junges anfasst.
-- Unser Junge-Code fasst beide nie an (B.BodyKind -> B.TYPE_BODY kennt nur ncbearcub / ncbeargrown, shared/BanditsNPCBear.lua:41).
-- Gruppe "ncbear" (aus der Kopie): NPC Crews Naht NOT_TENDED["ncbear"] (shared/BanditsNPCBearCrew.lua) -- kein Vieh fuer die Crew.
--
-- SPIELSTAND: ein gespeichertes Tier einer Art, die es spaeter nicht mehr gibt, bricht das Laden (shared/BanditsNPCBearDefs.lua Kopf).
-- Vor dem Entfernen dieser Testhilfe NCBear_CubGenClean() ausfuehren und speichern (oder einen Wegwerf-Spielstand benutzen).
-- Java liest AnimalDefinitions erst in IsoWorld.init, nach allen Lua-Dateien; diese Datei setzt nur auf Dateiebene.
-- Kein Translate-Ordner: der Tiername zeigt im Debug-Menue den Schluessel IGUI_AnimalType_ncbearcubgen (wie ncbeargen).
-- Statisch geprueft, nicht gespielt.
--
require "BanditsNPCBearDefs"

local SRC = "ncbearcub"
local BREED = "brown"

-- name = Artname; model/tex = eigenes Modell und eigene Textur (nil = die des echten Jungen behalten)
local ARTEN = {
    { name = "ncbearcubgen", model = "NCBearBenchCubGen_Body", tex = "NCBearBenchCubGen" },   -- scripts/NCBearBenchCubGen.txt
    { name = "ncbearcubstd", model = nil, tex = nil },                                        -- NCBearCub_Body / NCBearCub
}

local src = AnimalDefinitions and AnimalDefinitions.animals and AnimalDefinitions.animals[SRC]
if not src then
    print("[NCBear] *** cubgen: animal definition 'ncbearcub' is missing (shared/BanditsNPCBearDefs.lua), comparison cubs not defined")
else
    for _, art in ipairs(ARTEN) do
        local d = {}
        for k, v in pairs(src) do d[k] = v end
        if art.model then d.bodyModel = art.model end
        d.minSize = 0.35
        d.maxSize = 1.35   -- wie NCBearBenchVergleichDefs.lua: bei min = max setzt die Engine jede gesetzte Groesse beim Laden/naechsten
                           -- Tag zurueck (_arbeit/baer_zaehmen/forschung_b1d.md 0.2); ageToGrow bleibt riesig
        local stages = {}
        stages[art.name] = { ageToGrow = 36500 }      -- Eintrag gleich dem Artnamen (wie BanditsNPCBearDefs.lua:78)
        d.stages = stages
        local b = {}
        local sb = src.breeds and src.breeds[BREED]
        if sb then for k, v in pairs(sb) do b[k] = v end end
        b.name = BREED
        if art.tex then
            b.texture = art.tex
            b.textureMale = art.tex
            b.textureBaby = art.tex
        end
        d.breeds = { [BREED] = b }
        AnimalDefinitions.animals[art.name] = d
        -- Fenster "Tier-Info": ohne Eintrag wirft ISAnimalUI.lua:31 (wie NCBearBenchVergleichDefs.lua)
        if AnimalAvatarDefinition and AnimalAvatarDefinition[SRC] then
            AnimalAvatarDefinition[art.name] = AnimalAvatarDefinition[SRC]
        end
        -- Teile beim Zerlegen: Schluessel Tiername .. Rasse (ButcheringUtil.lua:18), wie NCBearBenchVergleichDefs.lua
        if AnimalPartsDefinitions and AnimalPartsDefinitions.animals and AnimalPartsDefinitions.animals[SRC .. BREED] then
            AnimalPartsDefinitions.animals[art.name .. BREED] = AnimalPartsDefinitions.animals[SRC .. BREED]
        end
    end
end
