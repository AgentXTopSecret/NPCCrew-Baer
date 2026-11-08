-- NC Bear Test: der Braunbaer als lebendes Tier. Kein Teil von NPC Crew, nicht fuer den Workshop.
-- Zwei Arten:
--   "bear"      eigenes Skelett, eigene Clips (Passgang, Galopp, Sturz zur Seite). Das ist der eigentliche Baer.
--   "bearstag"  Rueckfall: dasselbe Netz auf den Knochen des Rehs, bewegt sich mit den Rehclips.
-- Beide friedlich: wild = false, fleeZombies = false, animset "buck" (die Gruppe buck hat keinen Angriffszustand).
-- Beide erscheinen nie von selbst: keine Wandergruppe, kein Hof, keine Geschichte, keine Zucht (tier_spez.md 1.4).
-- Java liest diese Tabelle erst in IsoWorld.init (AnimalDefinitions.loadAnimalDefinitions), also nach allen Lua-Dateien.
-- Jedes Feld unten ist ein Schluessel, den AnimalDefinitions.loadAnimalDefinitions liest (Jar 42.21); die Werte nach
-- DeerDefinitions.lua:135-176 (buck), wo nichts anderes steht.

AnimalDefinitions = AnimalDefinitions or {}           -- DeerDefinitions.lua:1
AnimalDefinitions.animals = AnimalDefinitions.animals or {}   -- DeerDefinitions.lua:56

-- Gene: nur vorhandene (DeerDefinitions.lua:20-31). maxSize absichtlich nicht: dann ist die Groesse genau minSize = maxSize.
-- meatRatio ist Pflicht fuer den Tod (ButcheringUtil.lua:40).
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

-- Rasse: texture und textureMale beide (IsoAnimal.initTexture), Datei media/textures/Body/NCBear.png.
-- Symbole des Rehs als Attrappe (DeerDefinitions.lua:44-54). Der Aufprall hat den Ton des Rehs (DeerDefinitions.lua:185).
-- Seit dem Kampf (08.11., kampf_lua.md) eigene Stimmen aus nc_bear_sounds.txt, Form wie CowDefinitions.lua:315-330:
-- "pain" spielt die Engine selbst bei Treffern (AnimSets/buck/hitreaction/hitreaction1.xml PlayBreedSound pain),
-- "death" beim Sturz (falldown.xml PlayDeathSound, Jar IsoAnimal liest den Schluessel "death"); "huff" und "growl1..3"
-- ruft NCBearFight.lua mit animal:playBreedSound(name) (ISHutchGrabAnimal.lua:31). Schluessel klein (AnimalBreed.loadSounds).
-- "huffsoft" (08.11., anim_spez.md 5): derselbe Huff mit kuerzerer Reichweite (distanceMax 20) fuer das Schnauben im Alltag;
-- volume 0.6 ist seit der Gegenpruefung raus, NCBear_Huff.wav auf -1 dBFS angehoben (anim_review_gegen.md 1).
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
				huffsoft = { name = "NCBear_HuffSoft", slot = "voice", priority = 5 },   -- Alltags-Schnauben (anim_spez.md 5)
				growl1 = { name = "NCBear_Growl1", slot = "voice", priority = 20 },
				growl2 = { name = "NCBear_Growl2", slot = "voice", priority = 20 },
				growl3 = { name = "NCBear_Growl3", slot = "voice", priority = 20 },
			},
		},
	}
end

local function baer(name, modell)
	local stufen = {}
	stufen[name] = { ageToGrow = 60 }     -- Eintrag gleich dem Tiernamen, ageToGrow >= 1 (AnimalData.initSize)
	return {
		bodyModel = modell,               -- model-Skript in module Base (nc_bear_tier.txt)
		animset = "buck",                 -- eigener Name geht nicht: ActionGroup liest nur den Spielordner (tier_spez.md 3.1)
		group = "bear",                   -- Pflicht fuer das Debug-Menue (DebugContextMenu.lua:253)
		male = true,
		stages = stufen,
		breeds = rassen(),
		genes = gene(),
		minSize = 1.0,                    -- Massstab steckt im Netz (0,544 Einheiten je Meter)
		maxSize = 1.0,
		animalSize = 0.3,                 -- wie das Reh (DeerDefinitions.lua:154)
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
		wild = false,                     -- zahm: flieht nicht vor dem Spieler (BaseAnimalBehavior.spotted)
		canBeDomesticated = false,
		fleeZombies = false,              -- keine Flucht vor Zombies (BaseAnimalBehavior.spotted)
		alwaysFleeHumans = false,
		canThump = false,                 -- Vorgabe waere true
		canBePicked = false,              -- Vorgabe waere true
		canBeAlerted = false,
		sitRandomly = false,
		dontAttackOtherMale = true,
		wanderMul = 600,                  -- laeuft alle 600..3000 Ticks ein Stueck (wanderIdle)
		idleTypeNbr = 0,                  -- nur DeerStag_Idle01
		spottingDist = 10,
	}
end

AnimalDefinitions.animals["bear"] = baer("bear", "NCBear_Body")
AnimalDefinitions.animals["bearstag"] = baer("bearstag", "NCBearStag_Body")

-- Fenster "Tier-Info": ohne Eintrag ist ISAnimalUI.lua:622 nil und :31 (avatarDefinition.zoom) wirft. Felder vom Reh, ohne hook
-- (dann kein Schlachthaken, Zerlegen am Boden; ButcheringUtil.lua:36).
local b = AnimalAvatarDefinition["buck"]     -- AnimalAvatarDefinition.lua:231-240
if b then
	for _, name in ipairs({ "bear", "bearstag" }) do
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

-- Teile beim Zerlegen: Attrappe vom Reh (AnimalPartsDefinitions.lua:445-454), Schluessel Tiername .. Rasse (ButcheringUtil.lua:18)
if AnimalPartsDefinitions and AnimalPartsDefinitions.animals then
	AnimalPartsDefinitions.animals["bearbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
	AnimalPartsDefinitions.animals["bearstagbrown"] = AnimalPartsDefinitions.animals["buckwhitetailed"]
end
