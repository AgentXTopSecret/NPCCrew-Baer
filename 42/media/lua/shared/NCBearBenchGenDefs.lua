--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Lauf baer-gen-gross, 11.11.2026.
-- Kevin 11.11. ~18:25 (Freigabe 3): "der Generator-Baer nur als Vergleich per Testbefehl NCBear_GenLive() (braun + Fototon); Kevin waehlt spaeter".
--
-- Zwei Vergleichs-Arten des neuen grossen Baeren E (Generator-Netz auf GENAU dem Skelett und den 15 Clips des 2c-Baeren):
--   "ncbeargen"      braun    (media/textures/Body/NCBearGen.png)
--   "ncbeargenfoto"  Fototon  (media/textures/Body/NCBearGenFoto.png)
-- Beide sind eine Kopie der Art "bear" (shared/NCBearDefs.lua, gespielt) -- gleiche Groesse 1,0, gleiche Werte, gleiches animset "buck",
-- gleiche Gruppe "bear" -- nur mit eigenem Modell (scripts/NCBearBenchGen.txt, NCBearGen_Body), eigener Stufe und eigener Rasse/Textur.
-- Form der Kopie: shared/NCBearBenchVergleichDefs.lua (ncbearcubalt, gespielt) und shared/BanditsNPCBearDefs.lua (ncbeargrown, copyOf).
--
-- Wer fasst diese Arten an? NIEMAND ausser der Testhilfe client/NCBearBenchGen.lua:
--   * NCBearFight registriert nur getAnimalType() == "bear" (shared/NCBearFight.lua:1787) -> nie Kampfbaer, keine Laerm-Riegel, nie sitzt er
--     von selbst; alle Testbefehle NCBear_Sit/Eat/AnimTest gehen ueber F.NearestBear = nur registrierte Baeren (client/NCBearBench.lua:58).
--   * Der Baeren-Code (Junges/grosser Koerper) fragt nur B.BodyKind -> B.TYPE_BODY (shared/BanditsNPCBear.lua:36, :500-505): nur ncbearcub
--     und ncbeargrown. NCBearSpawn/NCBearSize/NCBearAttackProbe kennen nur bear/bearstag (NCBearSpawn.lua:7, NCBearSize.lua:24,
--     NCBearAttackProbe.lua:34).
--   * Gruppe "bear" bleibt: dann greift die NPC-Crew-Naht NOT_TENDED["bear"] (shared/BanditsNPCBearCrew.lua:34) -- kein Vieh fuer die Crew.
--
-- SPIELSTAND: ein gespeichertes Tier einer Art, die es spaeter nicht mehr gibt, bricht das Laden (shared/BanditsNPCBearDefs.lua Kopf).
-- Vor dem Entfernen dieser Testhilfe also NCBear_GenClean() ausfuehren und speichern (oder einen Wegwerf-Spielstand benutzen).
--
-- Java liest AnimalDefinitions erst in IsoWorld.init, nach allen Lua-Dateien (shared/NCBearDefs.lua Kopf); diese Datei setzt nur auf Dateiebene.
-- Kein Translate-Ordner: der Tiername zeigt im Debug-Menue/Tier-Fenster den Schluessel IGUI_AnimalType_ncbeargen (sonst wuerde die
-- IG_UI.json der Test-Mod ueberschrieben).
--

-- Diese Datei laedt alphabetisch VOR NCBearDefs.lua ("NCBearB" < "NCBearD"): require laedt sie zuerst. Vanilla: shared/BodyDragging/
-- corpseStorageCheck.lua:5 (require "Util/LuaTableUtil", auch eine alphabetisch spaetere Datei); gespielt: NCBearBenchVergleichDefs.lua.
-- Die Engine fuehrt eine schon geladene Datei nicht zweimal aus (Jar LuaManager.RunLuaInternal Offset 11-30: loaded.contains -> Rueckgabe).
require "NCBearDefs"

local SRC = "bear"
local BREED = "brown"
local MODEL = "NCBearGen_Body"                 -- scripts/NCBearBenchGen.txt (module Base)
local ARTEN = {
    { name = "ncbeargen", tex = "NCBearGen" },          -- braun
    { name = "ncbeargenfoto", tex = "NCBearGenFoto" },  -- Fototon
}

local function copyOf(t)                       -- flache Kopie wie shared/BanditsNPCBearDefs.lua copyOf
    local out = {}
    if type(t) == "table" then
        for k, v in pairs(t) do out[k] = v end
    end
    return out
end

local src = AnimalDefinitions and AnimalDefinitions.animals and AnimalDefinitions.animals[SRC]
if not src then
    print("[NCBear] *** gen: animal definition 'bear' is missing (shared/NCBearDefs.lua), comparison bears ncbeargen/ncbeargenfoto not defined")
else
    local sb = src.breeds and src.breeds[BREED]
    for _, art in ipairs(ARTEN) do
        local d = copyOf(src)                  -- alle Felder von "bear" (minSize = maxSize = 1,0, group "bear", animset "buck", wild false ...)
        d.bodyModel = MODEL
        local st = {}
        st[art.name] = { ageToGrow = 60 }      -- Eintrag gleich dem Artnamen, wie NCBearDefs.lua stufen[name]
        d.stages = st
        d.genes = copyOf(src.genes)            -- eigene Tabelle je Art (wie ncbeargrown)
        local b = copyOf(sb)
        b.name = BREED
        b.texture = art.tex                    -- texture UND textureMale (IsoAnimal.initTexture, NCBearDefs.lua Kommentar zur Rasse)
        b.textureMale = art.tex
        if sb then b.sounds = copyOf(sb.sounds) end   -- Stimmen des 2c-Baeren (pain, death, huff ...), eigene Tabelle
        d.breeds = { [BREED] = b }
        AnimalDefinitions.animals[art.name] = d
        -- Fenster "Tier-Info": ohne Eintrag wirft ISAnimalUI.lua:31 (Vanilla :622 liest AnimalAvatarDefinition[getAnimalType()])
        if AnimalAvatarDefinition and AnimalAvatarDefinition[SRC] then
            AnimalAvatarDefinition[art.name] = AnimalAvatarDefinition[SRC]
        end
        -- Teile beim Zerlegen: Schluessel Tiername .. Rasse (ButcheringUtil.lua:18), wie "bearbrown" (NCBearDefs.lua)
        if AnimalPartsDefinitions and AnimalPartsDefinitions.animals and AnimalPartsDefinitions.animals[SRC .. BREED] then
            AnimalPartsDefinitions.animals[art.name .. BREED] = AnimalPartsDefinitions.animals[SRC .. BREED]
        end
    end
end
