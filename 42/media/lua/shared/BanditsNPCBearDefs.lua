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
-- Erwachsenen, NCBearTest media/scripts/nc_bear_tier.txt; Textur wie NCBearTest shared/NCBearDefs.lua:40-41), minSize 0,72 (= B.CFG.swapSize) / maxSize 1,35, Schatten/Leiche wie der Erwachsene.
-- NIE die alte Art "bear". F2 (PLAN_F2.md 4.1): die Rasse des grossen Koerpers bekommt die Stimmen des Erwachsenen (pain, death, huff,
-- huffsoft, growl1-3) -- Schmerz, Tod, Schnauben, Knurren im Kampf (Kampf-Code server/BanditsNPCBearFight.lua, Bild client/BanditsNPCBearFx.lua).
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 1, 4.1; Kevin 12.11.2026 "ja fuer spieler als knopf"): drei weitere Arten fuer dieselben
-- zwei Koerper (unten): "ncbeargrowngen" (Generator-Baer braun), "ncbeargrowngenfoto" (Generator-Baer Fototon), "ncbearcubgen2"
-- (Generator-Junges v2). Artnamen ENDGUELTIG. Welche Art welcher Koerper und welches Aussehen ist, sagt nur B.LOOKS (shared/BanditsNPCBear.lua).
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
    -- Nachbesserung F1 B2: nie in Vanillas Tier-Anhaenger (jeder Spieler koennte ihn sonst ohne Besitzfrage einladen; im Anhaenger ist
    -- der Koerper nicht in der Welt -> "missing" -> C1 setzt einen neuen, der alte waere beim Ausladen ein zweiter Baer). Platz im
    -- Anhaenger = trailerBaseSize x Groesse (NUR JAR dec/IsoAnimal.java:2794-2796); Vanilla graut die Zeile dann "zu gross" aus
    -- (V:client/Vehicles/ISUI/ISVehicleMenu.lua:796-800, Anhaenger hoechstens 500: V:scripts/generated/vehicles/
    -- vehicle_trailer_livestock.txt:51). Der Baer faehrt wie die Crew im Auto mit (B1c, Kevin ENTSCHEIDUNGEN.md:244).
    trailerBaseSize = 100000,
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
    -- Rasse: Kopie der Junges-Rasse (Symbole, Stimmen fallover/petting; F2: + Erwachsenen-Stimmen, unten), Textur des grossen
    -- Baeren (media/textures/Body/NCBear.png); texture UND textureMale (textureBaby allein wirkt ohne nextStage nicht)
    local b = copyOf(breeds[BREED])
    b.name = BREED
    b.texture = "NCBear"
    b.textureMale = "NCBear"
    b.textureBaby = "NCBear"
    b.sounds = copyOf(breeds[BREED].sounds)
    -- F2 (PLAN_F2.md 4.1, FG L4): Stimmen des grossen Koerpers, Werte wie der gespielte Erwachsene (NCBearTest shared/NCBearDefs.lua:48-57).
    -- Namen sind Ton-Skripte (media/scripts/nc_bear_sounds.txt, Dateinamen bleiben), kein Befehl. Gespielt ueber animal:playBreedSound(Schluessel)
    -- (Vanilla shared/TimedActions/Animals/ISKillAnimalInInventory.lua:19 "pain", :41 "death"; OBERFLAECHE und Knoten-XML).
    b.sounds.pain = { name = "NCBear_Pain", slot = "voice", priority = 50 }
    b.sounds.death = { name = "NCBear_Pain", slot = "voice", priority = 100 }
    b.sounds.huff = { name = "NCBear_Huff", slot = "voice", priority = 10 }
    b.sounds.huffsoft = { name = "NCBear_HuffSoft", slot = "voice", priority = 5 }
    b.sounds.growl1 = { name = "NCBear_Growl1", slot = "voice", priority = 20 }
    b.sounds.growl2 = { name = "NCBear_Growl2", slot = "voice", priority = 20 }
    b.sounds.growl3 = { name = "NCBear_Growl3", slot = "voice", priority = 20 }
    d.breeds = { [BREED] = b }
    local st = {}
    st[BIG] = { ageToGrow = 36500 }        -- Eintrag gleich dem Artnamen, kein nextStage (wie das Junge, PLAN_B1D.md 0.3)
    d.stages = st
    d.genes = copyOf(genes)
    d.minSize = 0.72                       -- = B.CFG.swapSize (shared/BanditsNPCBear.lua); ein frischer Koerper steht so gleich bei 0,72
    d.maxSize = 1.35                       -- Kevin: Erwachsen 1,35 (baer/begleiter/ENTSCHEIDUNGEN.md:10)
    d.animalSize = 0.3                     -- wie die fruehere Test-Art "bear" (0,3)
    d.collisionSize = 0.30                 -- wirkt x Groesse: 0,22 beim Tausch, 0,41 bei 1,35 (Frage F10, im Spiel ansehen)
    d.shadoww = 0.9                        -- wie die fruehere Test-Art "bear"
    d.shadowfm = 1.8
    d.shadowbm = 1.8
    d.corpseSize = 3.0
    d.minWeight = 60                       -- Vorschlag (kein Hochheben, kein Anhaenger)
    d.maxWeight = 200
    d.minBlood = 800
    d.maxBlood = 2000
    d.trailerBaseSize = 100000             -- Nachbesserung F1 B2: nie in den Tier-Anhaenger (siehe Junges oben)
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

-- ---------------------------------------------------------------------------
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 1, 4.1). Je Art eine Kopie der Quell-Art (copyOf: Groessen-Grenzen -- gross 0,72..1,35 =
-- B.CFG.swapSize, Junges 0,35..1,35 --, Gruppe ncbear, Schatten, Gewicht, feedByHandAnim, trailerBaseSize, wild false ...) mit EIGENEN
-- Tabellen stages / breeds / genes. Die Rasse ist eine Kopie der Quell-Rasse (Symbole; gross: mit den F2-Stimmen) mit eigener Ton-Tabelle,
-- nur die drei Textur-Felder neu. Jede Zeile mit bodyModel und Textur ist ein Literal (das Uebernahme-Skript prueft die Literale: model-Skript
-- in scripts/nc_bear_look.txt, Textur-Datei in media/textures/Body). Zwei Arten auf EINEM Modell mit verschiedener Textur: Vanilla
-- shared/Definitions/animal/RabbitDefinitions.lua:158/:212 (rabdoe / rabbuck, beide Rab_Body). Hinter denselben Riegeln wie oben.
-- ---------------------------------------------------------------------------
local GEN = "ncbeargrowngen"              -- Generator-Baer braun (grosser Koerper)
local GENFOTO = "ncbeargrowngenfoto"      -- Generator-Baer Fototon (grosser Koerper, gleiches Modell)
local CUBGEN = "ncbearcubgen2"            -- Generator-Junges v2 (Junges-Koerper)

-- Kopie der Quell-Rasse mit eigener Ton-Tabelle (die Textur setzt der Aufrufer als Literal).
local function breedOf(src)
    local sb = type(src) == "table" and type(src.breeds) == "table" and src.breeds[BREED] or nil
    local b = copyOf(sb)
    b.name = BREED
    b.sounds = copyOf(type(sb) == "table" and sb.sounds or nil)
    return b
end

local bigDef = AnimalDefinitions.animals[BIG]
if bigDef then
    local d = copyOf(bigDef)
    d.bodyModel = "NCBearGen_Body"          -- Generator-Baer (model-Skript in module Base, media/scripts/nc_bear_look.txt)
    local b = breedOf(bigDef)
    b.texture = "NCBearGen"
    b.textureMale = "NCBearGen"
    b.textureBaby = "NCBearGen"
    d.breeds = { [BREED] = b }
    local st = {}
    st[GEN] = { ageToGrow = 36500 }        -- Eintrag gleich dem Artnamen, kein nextStage (wie oben)
    d.stages = st
    d.genes = copyOf(genes)
    AnimalDefinitions.animals[GEN] = d

    local f = copyOf(bigDef)
    f.bodyModel = "NCBearGen_Body"          -- dasselbe Modell, andere Textur (Fototon)
    local fb = breedOf(bigDef)
    fb.texture = "NCBearGenFoto"
    fb.textureMale = "NCBearGenFoto"
    fb.textureBaby = "NCBearGenFoto"
    f.breeds = { [BREED] = fb }
    local fst = {}
    fst[GENFOTO] = { ageToGrow = 36500 }
    f.stages = fst
    f.genes = copyOf(genes)
    AnimalDefinitions.animals[GENFOTO] = f
end

if cubDef then
    local d = copyOf(cubDef)
    d.bodyModel = "NCBearCubGen_Body"       -- Generator-Junges v2 (model-Skript in module Base, media/scripts/nc_bear_look.txt)
    local b = breedOf(cubDef)
    b.texture = "NCBearCubGen"
    b.textureMale = "NCBearCubGen"
    b.textureBaby = "NCBearCubGen"
    d.breeds = { [BREED] = b }
    local st = {}
    st[CUBGEN] = { ageToGrow = 36500 }
    d.stages = st
    d.genes = copyOf(genes)
    AnimalDefinitions.animals[CUBGEN] = d
end

-- Fenster "Animal info": Werte wie die Quell-Art (eigene Tabelle); ohne Eintrag wirft Vanilla client/ISUI/Animal/ISAnimalUI.lua:31.
if AnimalAvatarDefinition then
    if AnimalAvatarDefinition[BIG] then
        AnimalAvatarDefinition[GEN] = copyOf(AnimalAvatarDefinition[BIG])
        AnimalAvatarDefinition[GENFOTO] = copyOf(AnimalAvatarDefinition[BIG])
    end
    if AnimalAvatarDefinition[CUB] then
        AnimalAvatarDefinition[CUBGEN] = copyOf(AnimalAvatarDefinition[CUB])
    end
end

-- Teile beim Zerlegen wie die Quell-Art, Schluessel Art .. Rasse (Vanilla ButcheringUtil.lua:18).
if AnimalPartsDefinitions and AnimalPartsDefinitions.animals then
    AnimalPartsDefinitions.animals[GEN .. BREED] = AnimalPartsDefinitions.animals[BIG .. BREED]
    AnimalPartsDefinitions.animals[GENFOTO .. BREED] = AnimalPartsDefinitions.animals[BIG .. BREED]
    AnimalPartsDefinitions.animals[CUBGEN .. BREED] = AnimalPartsDefinitions.animals[CUB .. BREED]
end
