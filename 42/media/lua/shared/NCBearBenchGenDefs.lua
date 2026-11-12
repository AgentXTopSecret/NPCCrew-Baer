--
-- NUR TESTHILFE (NCBearBench*: wird nie nach NPC Crew kopiert, baer/tools/baer_uebernahme.py BENCH_ANY). Lauf baer-gen-gross, 11.11.2026.
-- Kevin 11.11. ~18:25 (Freigabe 3): "der Generator-Baer nur als Vergleich per Testbefehl NCBear_GenLive() (braun + Fototon); Kevin waehlt spaeter".
-- F2 (Lauf baer-f2, PLAN_F2.md 1.1): Quelle ist jetzt die Test-Art "ncbear" (shared/NCBearBenchDefs.lua; die alte shared/NCBearDefs.lua ist ein
-- Stummel) -- gleiche Felder wie die alte Art "bear", nur Gruppe "ncbear" statt "bear". Artnamen ncbeargen / ncbeargenfoto bleiben (Spielstaende).
--
-- Zwei Vergleichs-Arten des neuen grossen Baeren E (Generator-Netz auf GENAU dem Skelett und den 15 Clips des 2c-Baeren):
--   "ncbeargen"      braun    (media/textures/Body/NCBearGen.png)
--   "ncbeargenfoto"  Fototon  (media/textures/Body/NCBearGenFoto.png)
-- Beide sind eine Kopie der Test-Art "ncbear" (shared/NCBearBenchDefs.lua) -- gleiche Groesse 1,0, gleiche Werte, gleiches animset "buck",
-- gleiche Gruppe "ncbear" -- nur mit eigenem Modell (scripts/NCBearBenchGen.txt, NCBearGen_Body), eigener Stufe und eigener Rasse/Textur.
-- Form der Kopie: shared/NCBearBenchVergleichDefs.lua (ncbearcubalt, gespielt) und shared/BanditsNPCBearDefs.lua (ncbeargrown, copyOf).
--
-- Wer fasst diese Arten an? NIEMAND ausser der Testhilfe client/NCBearBenchGen.lua:
--   * Der Baeren-Code (Junges/grosser Koerper) fragt nur B.BodyKind -> B.TYPE_BODY (shared/BanditsNPCBear.lua): seit dem Lauf
--     baer-aussehen die 5 Arten aus B.LOOKS (ncbearcub, ncbearcubgen2, ncbeargrown, ncbeargrowngen, ncbeargrowngenfoto), nie eine
--     Werkbank-Art wie diese. Der Kampf (F2) kennt nur den eigenen gezaehmten Baeren. Die Bench-Befehle fuer die Test-Arten (client/NCBearBench.lua,
--     NCBearBenchAdult.lua, NCBearBenchAttackProbe.lua) kennen nur ncbear / bear / bearstag.
--   * Gruppe "ncbear": NPC Crews Naht NOT_TENDED["ncbear"] (shared/BanditsNPCBearCrew.lua) -- kein Vieh fuer die Crew.
--
-- SPIELSTAND: ein gespeichertes Tier einer Art, die es spaeter nicht mehr gibt, bricht das Laden (shared/BanditsNPCBearDefs.lua Kopf).
-- Vor dem Entfernen dieser Testhilfe also NCBear_GenClean() ausfuehren und speichern (oder einen Wegwerf-Spielstand benutzen).
--
-- Java liest AnimalDefinitions erst in IsoWorld.init, nach allen Lua-Dateien; diese Datei setzt nur auf Dateiebene.
-- Kein Translate-Ordner: der Tiername zeigt im Debug-Menue/Tier-Fenster den Schluessel IGUI_AnimalType_ncbeargen (sonst wuerde die
-- IG_UI.json der Test-Mod ueberschrieben).
--

-- "NCBearBenchD" < "NCBearBenchG": die Quelle laedt ohnehin vorher; require schadet nicht (Vanilla: shared/BodyDragging/
-- corpseStorageCheck.lua:5 require "Util/LuaTableUtil"). Die Engine fuehrt eine schon geladene Datei nicht zweimal aus
-- (Jar LuaManager.RunLuaInternal Offset 11-30: loaded.contains -> Rueckgabe; gespielt mit NCBearBenchVergleichDefs.lua).
require "NCBearBenchDefs"

local SRC = "ncbear"
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
    print("[NCBear] *** gen: animal definition 'ncbear' is missing (shared/NCBearBenchDefs.lua), comparison bears ncbeargen/ncbeargenfoto not defined")
else
    local sb = src.breeds and src.breeds[BREED]
    for _, art in ipairs(ARTEN) do
        local d = copyOf(src)                  -- alle Felder von "ncbear" (minSize = maxSize = 1,0, group "ncbear", animset "buck", wild false ...)
        d.bodyModel = MODEL
        local st = {}
        st[art.name] = { ageToGrow = 60 }      -- Eintrag gleich dem Artnamen, wie NCBearBenchDefs.lua stufen[name]
        d.stages = st
        d.genes = copyOf(src.genes)            -- eigene Tabelle je Art (wie ncbeargrown)
        local b = copyOf(sb)
        b.name = BREED
        b.texture = art.tex                    -- texture UND textureMale (IsoAnimal.initTexture, alte NCBearDefs.lua Kommentar zur Rasse)
        b.textureMale = art.tex
        if sb then b.sounds = copyOf(sb.sounds) end   -- Stimmen des 2c-Baeren (pain, death, huff ...), eigene Tabelle
        d.breeds = { [BREED] = b }
        AnimalDefinitions.animals[art.name] = d
        -- Fenster "Tier-Info": ohne Eintrag wirft ISAnimalUI.lua:31 (Vanilla :622 liest AnimalAvatarDefinition[getAnimalType()])
        if AnimalAvatarDefinition and AnimalAvatarDefinition[SRC] then
            AnimalAvatarDefinition[art.name] = AnimalAvatarDefinition[SRC]
        end
        -- Teile beim Zerlegen: Schluessel Tiername .. Rasse (ButcheringUtil.lua:18), wie "ncbearbrown" (NCBearBenchDefs.lua)
        if AnimalPartsDefinitions and AnimalPartsDefinitions.animals and AnimalPartsDefinitions.animals[SRC .. BREED] then
            AnimalPartsDefinitions.animals[art.name .. BREED] = AnimalPartsDefinitions.animals[SRC .. BREED]
        end
    end
end
