"""
Overworld Encounter System
==========================
Random and visible enemy encounters in the overworld (non-dungeon).
Enemies scale to player level and are region-appropriate.

Two encounter types:
  1. Random encounters — chance-based on room entry (wilderness only)
  2. Visible encounters — persistent enemies that show in room description
"""

import random

# =====================================================================
# OVERWORLD ENEMY DATABASE
# =====================================================================
# Enemies organized by region/biome. Stats are base values, scaled by
# player level when spawned.

OVERWORLD_ENEMIES = {
	# ── Forest Region ──
	"wild_wolf": {
		"name": "Wild Wolf",
		"description": "A snarling grey wolf with hungry yellow eyes.",
		"hp": 22, "attack": 6, "defense": 2,
		"xp_reward": 12, "gold_reward": (2, 6),
		"loot": [("wolf_pelt", 0.40), ("raw_meat", 0.30), ("wolf_fang", 0.15)],
		"abilities": ["bite", "howl"],
		"regions": ["forest"],
	},
	"forest_spider": {
		"name": "Forest Spider",
		"description": "A large spider with bristly legs and dripping fangs.",
		"hp": 16, "attack": 7, "defense": 1,
		"xp_reward": 10, "gold_reward": (1, 4),
		"loot": [("spider_silk", 0.35), ("venom_sac", 0.15)],
		"abilities": ["bite", "web"],
		"regions": ["forest"],
	},
	"wild_boar": {
		"name": "Wild Boar",
		"description": "A stocky boar with sharp tusks and a foul temper.",
		"hp": 28, "attack": 5, "defense": 3,
		"xp_reward": 14, "gold_reward": (3, 7),
		"loot": [("raw_meat", 0.50), ("boar_tusk", 0.20), ("leather_scrap", 0.25)],
		"abilities": ["charge", "gore"],
		"regions": ["forest", "farmland"],
	},
	"forest_bandit": {
		"name": "Forest Bandit",
		"description": "A ragged outlaw hiding among the trees, blade drawn.",
		"hp": 25, "attack": 8, "defense": 2,
		"xp_reward": 18, "gold_reward": (8, 20),
		"loot": [("health_potion", 0.20), ("iron_dagger", 0.10), ("lockpick", 0.15)],
		"abilities": ["slash", "dodge"],
		"regions": ["forest", "road"],
	},

	# ── Mountain Region ──
	"mountain_goat": {
		"name": "Aggressive Mountain Goat",
		"description": "A wild mountain goat that charges at intruders.",
		"hp": 20, "attack": 5, "defense": 4,
		"xp_reward": 10, "gold_reward": (1, 5),
		"loot": [("raw_meat", 0.40), ("leather_scrap", 0.30)],
		"abilities": ["charge", "headbutt"],
		"regions": ["mountain"],
	},
	"rock_elemental": {
		"name": "Rock Elemental",
		"description": "A hulking mass of stone and gravel, eyes glowing with dull orange light.",
		"hp": 40, "attack": 7, "defense": 6,
		"xp_reward": 25, "gold_reward": (5, 15),
		"loot": [("stone_chunk", 0.50), ("raw_diamond", 0.05), ("cave_crystal", 0.15)],
		"abilities": ["slam", "stone_shield"],
		"regions": ["mountain"],
	},
	"highland_brigand": {
		"name": "Highland Brigand",
		"description": "A hardened mountain bandit wrapped in furs and leather.",
		"hp": 30, "attack": 9, "defense": 3,
		"xp_reward": 22, "gold_reward": (10, 25),
		"loot": [("health_potion", 0.25), ("iron_sword", 0.08), ("gold_ring", 0.10)],
		"abilities": ["slash", "intimidate"],
		"regions": ["mountain", "road"],
	},

	# ── Swamp Region ──
	"swamp_snake": {
		"name": "Swamp Viper",
		"description": "A venomous snake slithering through the murky water.",
		"hp": 14, "attack": 8, "defense": 1,
		"xp_reward": 11, "gold_reward": (1, 4),
		"loot": [("venom_sac", 0.35), ("snake_scale", 0.20)],
		"abilities": ["bite", "poison_strike"],
		"regions": ["swamp"],
	},
	"bog_shambler": {
		"name": "Bog Shambler",
		"description": "A rotting, moss-covered figure that lurches from the murk.",
		"hp": 35, "attack": 6, "defense": 4,
		"xp_reward": 20, "gold_reward": (3, 8),
		"loot": [("swamp_moss", 0.40), ("bone_fragment", 0.25), ("health_potion", 0.10)],
		"abilities": ["slam", "poison_touch"],
		"regions": ["swamp"],
	},
	"marsh_hag": {
		"name": "Marsh Hag",
		"description": "A hunched crone surrounded by sickly green mist and muttering curses.",
		"hp": 24, "attack": 10, "defense": 2,
		"xp_reward": 28, "gold_reward": (6, 18),
		"loot": [("health_potion", 0.30), ("shadow_essence", 0.15), ("enchanted_charm", 0.08)],
		"abilities": ["curse", "drain_life"],
		"regions": ["swamp"],
	},

	# ── Graveyard/Undead Region ──
	"skeleton_warrior": {
		"name": "Skeleton Warrior",
		"description": "A rattling skeleton with rusted armor and a chipped sword.",
		"hp": 20, "attack": 7, "defense": 3,
		"xp_reward": 15, "gold_reward": (4, 10),
		"loot": [("bone_fragment", 0.40), ("iron_sword", 0.05), ("old_shield", 0.10)],
		"abilities": ["slash", "bone_throw"],
		"regions": ["graveyard"],
	},
	"restless_spirit": {
		"name": "Restless Spirit",
		"description": "A translucent figure wailing in sorrow, cold mist trailing behind.",
		"hp": 18, "attack": 9, "defense": 1,
		"xp_reward": 16, "gold_reward": (2, 8),
		"loot": [("ectoplasm", 0.35), ("shadow_essence", 0.20)],
		"abilities": ["chill_touch", "wail"],
		"regions": ["graveyard"],
	},

	# ── Farmland/Road (easier) ──
	"rabid_dog": {
		"name": "Rabid Dog",
		"description": "A feral dog foaming at the mouth, growling viciously.",
		"hp": 15, "attack": 5, "defense": 1,
		"xp_reward": 8, "gold_reward": (1, 3),
		"loot": [("raw_meat", 0.30), ("leather_scrap", 0.20)],
		"abilities": ["bite"],
		"regions": ["farmland", "road"],
	},
	"highway_thief": {
		"name": "Highway Thief",
		"description": "A cloaked figure blocking the road with a dagger drawn.",
		"hp": 22, "attack": 7, "defense": 2,
		"xp_reward": 14, "gold_reward": (12, 30),
		"loot": [("lockpick", 0.25), ("health_potion", 0.15), ("gold_ring", 0.08)],
		"abilities": ["slash", "dodge"],
		"regions": ["road"],
	},

	# ── Desert Region ──
	"desert_scorpion": {
		"name": "Giant Desert Scorpion",
		"description": "A massive scorpion with pincers clicking and tail poised to strike.",
		"hp": 26, "attack": 8, "defense": 4,
		"xp_reward": 16, "gold_reward": (3, 8),
		"loot": [("scorpion_tail", 0.45), ("venom_sac", 0.25)],
		"abilities": ["sting", "pincer_grab"],
		"regions": ["desert"],
	},
	"sand_viper": {
		"name": "Sand Viper",
		"description": "A venomous snake perfectly camouflaged in the sand.",
		"hp": 16, "attack": 9, "defense": 1,
		"xp_reward": 12, "gold_reward": (1, 4),
		"loot": [("venom_sac", 0.40), ("snake_scale", 0.25)],
		"abilities": ["bite", "poison_strike"],
		"regions": ["desert"],
	},
	"desert_raider": {
		"name": "Desert Raider",
		"description": "A sun-darkened bandit wrapped in desert robes, scimitar gleaming.",
		"hp": 28, "attack": 9, "defense": 3,
		"xp_reward": 20, "gold_reward": (15, 35),
		"loot": [("health_potion", 0.20), ("gold_ring", 0.12), ("scimitar", 0.08)],
		"abilities": ["slash", "sand_throw"],
		"regions": ["desert"],
	},
	"sand_elemental": {
		"name": "Sand Elemental",
		"description": "A swirling mass of sand and wind in vaguely humanoid form.",
		"hp": 38, "attack": 7, "defense": 5,
		"xp_reward": 24, "gold_reward": (5, 12),
		"loot": [("sandstone_chunk", 0.50), ("desert_rose", 0.15)],
		"abilities": ["sandstorm", "blind"],
		"regions": ["desert"],
	},

	# ── Tundra/Frozen Region ──
	"frost_wolf": {
		"name": "Frost Wolf",
		"description": "A white-furred wolf with ice crystals in its breath.",
		"hp": 28, "attack": 7, "defense": 3,
		"xp_reward": 15, "gold_reward": (3, 8),
		"loot": [("wolf_pelt", 0.45), ("ice_crystal", 0.20), ("raw_meat", 0.30)],
		"abilities": ["bite", "frost_howl"],
		"regions": ["tundra"],
	},
	"ice_wraith": {
		"name": "Ice Wraith",
		"description": "A spectral figure of frozen mist and bitter cold.",
		"hp": 22, "attack": 10, "defense": 2,
		"xp_reward": 18, "gold_reward": (4, 10),
		"loot": [("ectoplasm", 0.35), ("ice_crystal", 0.30), ("shadow_essence", 0.15)],
		"abilities": ["chill_touch", "frost_breath"],
		"regions": ["tundra"],
	},
	"polar_bear": {
		"name": "Polar Bear",
		"description": "A massive white bear, territorial and deadly.",
		"hp": 45, "attack": 8, "defense": 5,
		"xp_reward": 22, "gold_reward": (5, 12),
		"loot": [("raw_meat", 0.50), ("thick_fur", 0.35), ("bear_claw", 0.20)],
		"abilities": ["maul", "roar"],
		"regions": ["tundra"],
	},
	"frost_giant_scout": {
		"name": "Frost Giant Scout",
		"description": "A towering blue-skinned humanoid with a massive ice club.",
		"hp": 55, "attack": 11, "defense": 6,
		"xp_reward": 35, "gold_reward": (10, 25),
		"loot": [("ice_crystal", 0.40), ("giant_tooth", 0.15), ("health_potion", 0.20)],
		"abilities": ["slam", "frost_strike"],
		"regions": ["tundra"],
	},

	# ── Coastal Region ──
	"giant_crab": {
		"name": "Giant Crab",
		"description": "An oversized crab with snapping pincers and a hard shell.",
		"hp": 30, "attack": 6, "defense": 6,
		"xp_reward": 14, "gold_reward": (2, 6),
		"loot": [("raw_meat", 0.40), ("crab_shell", 0.30)],
		"abilities": ["pincer_grab", "shell_defense"],
		"regions": ["coast"],
	},
	"sea_serpent": {
		"name": "Sea Serpent",
		"description": "A serpentine creature rising from the waves with gleaming scales.",
		"hp": 35, "attack": 9, "defense": 3,
		"xp_reward": 20, "gold_reward": (5, 15),
		"loot": [("snake_scale", 0.45), ("pearl", 0.10), ("raw_meat", 0.25)],
		"abilities": ["bite", "constrict"],
		"regions": ["coast"],
	},
	"pirate_raider": {
		"name": "Pirate Raider",
		"description": "A grizzled seafarer with a cutlass and murderous intent.",
		"hp": 26, "attack": 8, "defense": 2,
		"xp_reward": 18, "gold_reward": (20, 45),
		"loot": [("health_potion", 0.20), ("gold_coin", 0.50), ("cutlass", 0.08)],
		"abilities": ["slash", "pistol_shot"],
		"regions": ["coast"],
	},
	"drowned_sailor": {
		"name": "Drowned Sailor",
		"description": "A waterlogged corpse shambling from the surf, seaweed draped over its frame.",
		"hp": 24, "attack": 7, "defense": 3,
		"xp_reward": 15, "gold_reward": (3, 10),
		"loot": [("bone_fragment", 0.35), ("seaweed", 0.40), ("gold_coin", 0.20)],
		"abilities": ["slam", "curse"],
		"regions": ["coast"],
	},

	# ══════════════════════════════════════════════════════════════
	# ISLAND ENEMIES — stronger than mainland, better loot
	# ══════════════════════════════════════════════════════════════

	# ── Sunstone Atoll (Tier 1 Island, lvl 8+) ──
	"coconut_crab": {
		"name": "Giant Coconut Crab",
		"description": "A massive red-shelled crab the size of a dog, its claws can crush coconuts — and bones.",
		"hp": 45, "attack": 12, "defense": 8,
		"xp_reward": 30, "gold_reward": (8, 20),
		"loot": [("crab_shell", 0.50), ("raw_meat", 0.40), ("pearl", 0.15)],
		"abilities": ["pincer_grab", "shell_defense"],
		"regions": ["sunstone"],
	},
	"jungle_viper": {
		"name": "Sunstone Jungle Viper",
		"description": "A brilliant emerald serpent with golden patterns, coiled among the fronds. Its venom burns like sunfire.",
		"hp": 35, "attack": 14, "defense": 4,
		"xp_reward": 28, "gold_reward": (6, 15),
		"loot": [("venom_sac", 0.40), ("snake_scale", 0.50), ("sunstone_fang", 0.12)],
		"abilities": ["bite", "venom_strike"],
		"regions": ["sunstone"],
	},
	"sun_cultist": {
		"name": "Sun Cultist",
		"description": "A robed figure with sun-symbol face paint, wielding a curved golden blade. They guard the temple ruins with zealous fury.",
		"hp": 50, "attack": 13, "defense": 6,
		"xp_reward": 35, "gold_reward": (15, 35),
		"loot": [("gold_coin", 0.60), ("sun_talisman", 0.18), ("health_potion", 0.25), ("golden_blade", 0.06)],
		"abilities": ["slash", "solar_flare"],
		"regions": ["sunstone"],
	},
	"reef_shark": {
		"name": "Reef Shark",
		"description": "A sleek grey predator that patrols the shallow lagoon, drawn by the scent of blood.",
		"hp": 55, "attack": 15, "defense": 5,
		"xp_reward": 32, "gold_reward": (5, 12),
		"loot": [("raw_meat", 0.50), ("shark_tooth", 0.35), ("shark_fin", 0.20)],
		"abilities": ["bite", "thrash"],
		"regions": ["sunstone"],
	},
	"tropical_slime": {
		"name": "Tropical Slime",
		"description": "A pulsating mass of bioluminescent goo, tinted orange and gold. It dissolves organic matter on contact.",
		"hp": 40, "attack": 10, "defense": 10,
		"xp_reward": 25, "gold_reward": (4, 10),
		"loot": [("slime_core", 0.45), ("bioluminescent_gel", 0.30), ("health_potion", 0.15)],
		"abilities": ["slam", "dissolve"],
		"regions": ["sunstone"],
	},
	"temple_guardian": {
		"name": "Temple Guardian",
		"description": "An animated stone statue wreathed in golden light, still fulfilling its ancient duty to protect the Sun Temple.",
		"hp": 70, "attack": 16, "defense": 12,
		"xp_reward": 45, "gold_reward": (20, 45),
		"loot": [("stone_chunk", 0.40), ("sun_talisman", 0.25), ("guardian_core", 0.10), ("enchanted_cloak_fragment", 0.05)],
		"abilities": ["slam", "stone_shield", "solar_flare"],
		"regions": ["sunstone"],
	},

	# ── Emerald Isle (Tier 2 Island, lvl 12+) ──
	"jungle_panther": {
		"name": "Emerald Panther",
		"description": "A huge panther with shimmering green-black fur that blends perfectly into the dense foliage.",
		"hp": 60, "attack": 18, "defense": 7,
		"xp_reward": 40, "gold_reward": (10, 25),
		"loot": [("panther_pelt", 0.45), ("raw_meat", 0.40), ("panther_fang", 0.20)],
		"abilities": ["bite", "pounce", "dodge"],
		"regions": ["emerald"],
	},
	"spore_shambler": {
		"name": "Spore Shambler",
		"description": "A shambling mass of fungi and rotting wood, releasing clouds of hallucinogenic spores with every step.",
		"hp": 55, "attack": 14, "defense": 12,
		"xp_reward": 35, "gold_reward": (5, 12),
		"loot": [("glowing_mushroom", 0.50), ("spore_sac", 0.35), ("fungal_essence", 0.15)],
		"abilities": ["slam", "spore_cloud", "regenerate"],
		"regions": ["emerald"],
	},
	"druid_wraith": {
		"name": "Druid Wraith",
		"description": "The spectral remnant of an ancient druid, still bound to the island by unfinished rituals. Vines and leaves orbit its translucent form.",
		"hp": 50, "attack": 16, "defense": 8,
		"xp_reward": 42, "gold_reward": (12, 30),
		"loot": [("spirit_essence", 0.35), ("druid_staff_shard", 0.12), ("health_potion", 0.30), ("nature_rune", 0.20)],
		"abilities": ["curse", "entangle", "nature_blast"],
		"regions": ["emerald"],
	},
	"dire_gorilla": {
		"name": "Dire Gorilla",
		"description": "A silverback gorilla of enormous size, covered in moss and lichen. It beats its chest with earth-shaking force.",
		"hp": 80, "attack": 17, "defense": 10,
		"xp_reward": 48, "gold_reward": (8, 20),
		"loot": [("raw_meat", 0.50), ("gorilla_hide", 0.35), ("primal_tooth", 0.15)],
		"abilities": ["slam", "charge", "roar"],
		"regions": ["emerald"],
	},
	"poison_dart_frog": {
		"name": "Giant Poison Dart Frog",
		"description": "A brilliant blue and orange frog the size of a large dog. Its skin glistens with deadly toxin.",
		"hp": 35, "attack": 20, "defense": 4,
		"xp_reward": 38, "gold_reward": (6, 14),
		"loot": [("venom_sac", 0.55), ("bioluminescent_gel", 0.30), ("frog_skin", 0.40)],
		"abilities": ["venom_strike", "tongue_lash"],
		"regions": ["emerald"],
	},
	"treant_guardian": {
		"name": "Treant Guardian",
		"description": "A massive living tree that defends the ancient groves. Its bark-covered fists can crush stone, and roots erupt from the ground at its command.",
		"hp": 95, "attack": 19, "defense": 15,
		"xp_reward": 55, "gold_reward": (15, 40),
		"loot": [("ancient_bark", 0.40), ("living_wood", 0.25), ("treant_heart", 0.08), ("nature_rune", 0.20)],
		"abilities": ["slam", "root_snare", "bark_shield", "regenerate"],
		"regions": ["emerald"],
	},

	# ── Stormbreak Reef (Tier 3 Island, lvl 16+) ──
	"storm_elemental": {
		"name": "Storm Elemental",
		"description": "A swirling mass of wind and lightning given form. It crackles with static electricity, and bolts arc from its body to nearby metal.",
		"hp": 75, "attack": 22, "defense": 8,
		"xp_reward": 52, "gold_reward": (12, 30),
		"loot": [("storm_crystal", 0.45), ("lightning_shard", 0.30), ("storm_essence", 0.15)],
		"abilities": ["lightning_strike", "gust", "static_field"],
		"regions": ["stormbreak"],
	},
	"drowned_pirate": {
		"name": "Drowned Pirate Captain",
		"description": "The barnacle-encrusted corpse of a pirate captain, still clutching a rusted cutlass. Lightning plays across its waterlogged frame.",
		"hp": 70, "attack": 20, "defense": 10,
		"xp_reward": 48, "gold_reward": (25, 55),
		"loot": [("gold_coin", 0.60), ("pirate_cutlass", 0.12), ("compass_fragment", 0.20), ("health_potion", 0.25)],
		"abilities": ["slash", "curse", "pistol_shot"],
		"regions": ["stormbreak"],
	},
	"reef_lurker": {
		"name": "Reef Lurker",
		"description": "A camouflaged predator that blends perfectly with the coral formations. Razor-sharp coral growths cover its hide like natural armor.",
		"hp": 65, "attack": 18, "defense": 14,
		"xp_reward": 45, "gold_reward": (8, 20),
		"loot": [("coral_shard", 0.50), ("lurker_hide", 0.35), ("pearl", 0.18)],
		"abilities": ["bite", "ambush", "coral_armor"],
		"regions": ["stormbreak"],
	},
	"thunder_hawk": {
		"name": "Thunder Hawk",
		"description": "A massive raptor with feathers that crackle with stored lightning. It dives from storm clouds at blinding speed.",
		"hp": 55, "attack": 24, "defense": 6,
		"xp_reward": 50, "gold_reward": (10, 22),
		"loot": [("thunder_feather", 0.40), ("raw_meat", 0.45), ("lightning_shard", 0.15)],
		"abilities": ["dive", "lightning_strike", "screech"],
		"regions": ["stormbreak"],
	},
	"kraken_tentacle": {
		"name": "Kraken Tentacle",
		"description": "A massive tentacle extending from the deep waters, covered in suction cups lined with teeth. The rest of the creature lurks below.",
		"hp": 90, "attack": 21, "defense": 12,
		"xp_reward": 58, "gold_reward": (15, 35),
		"loot": [("kraken_sucker", 0.40), ("tentacle_meat", 0.50), ("kraken_ink", 0.25), ("black_pearl", 0.08)],
		"abilities": ["constrict", "slam", "drag_under"],
		"regions": ["stormbreak"],
	},
	"coral_golem": {
		"name": "Coral Golem",
		"description": "A hulking construct of living coral and barnacles, animated by the reef's residual magic. Seawater streams from its joints.",
		"hp": 100, "attack": 20, "defense": 18,
		"xp_reward": 60, "gold_reward": (18, 40),
		"loot": [("coral_shard", 0.50), ("golem_core", 0.12), ("black_pearl", 0.10), ("enchanted_cloak_fragment", 0.06)],
		"abilities": ["slam", "coral_armor", "tidal_wave"],
		"regions": ["stormbreak"],
	},

	# ── Cinderforge Isle (Tier 4 Island, lvl 20+) ──
	"magma_hound": {
		"name": "Magma Hound",
		"description": "A wolf-like creature with cracked obsidian skin revealing rivers of molten lava beneath. Its paw prints leave smoldering tracks.",
		"hp": 85, "attack": 25, "defense": 12,
		"xp_reward": 62, "gold_reward": (14, 32),
		"loot": [("obsidian_shard", 0.45), ("magma_core", 0.20), ("raw_meat", 0.30)],
		"abilities": ["bite", "fire_breath", "lava_trail"],
		"regions": ["cinderforge"],
	},
	"fire_elemental": {
		"name": "Greater Fire Elemental",
		"description": "A towering pillar of white-hot fire with a vaguely humanoid shape. The air around it shimmers with heat distortion.",
		"hp": 80, "attack": 28, "defense": 8,
		"xp_reward": 65, "gold_reward": (15, 35),
		"loot": [("fire_essence", 0.50), ("ember_crystal", 0.30), ("ash_dust", 0.40)],
		"abilities": ["fire_breath", "inferno_burst", "heat_wave"],
		"regions": ["cinderforge"],
	},
	"obsidian_sentinel": {
		"name": "Obsidian Sentinel",
		"description": "A walking mass of volcanic glass, its edges razor-sharp. Ancient dwarven runes glow red on its surface.",
		"hp": 110, "attack": 23, "defense": 20,
		"xp_reward": 70, "gold_reward": (20, 45),
		"loot": [("obsidian_shard", 0.55), ("sentinel_core", 0.10), ("dwarven_rune_stone", 0.15)],
		"abilities": ["slam", "obsidian_shatter", "stone_shield"],
		"regions": ["cinderforge"],
	},
	"salamander_warrior": {
		"name": "Salamander Warrior",
		"description": "A bipedal lizard-like creature wreathed in flame, wielding a spear of hardened magma. These ancient warriors guard the volcanic forges.",
		"hp": 95, "attack": 26, "defense": 14,
		"xp_reward": 68, "gold_reward": (18, 42),
		"loot": [("magma_spear_tip", 0.20), ("salamander_scale", 0.40), ("fire_essence", 0.30), ("health_potion", 0.20)],
		"abilities": ["thrust", "fire_breath", "flame_whirl"],
		"regions": ["cinderforge"],
	},
	"ash_wraith": {
		"name": "Ash Wraith",
		"description": "A spectral figure formed from volcanic ash and cinder, drifting through the smoke. Its touch leaves burns that won't heal naturally.",
		"hp": 70, "attack": 24, "defense": 10,
		"xp_reward": 58, "gold_reward": (12, 28),
		"loot": [("ash_dust", 0.50), ("wraith_ember", 0.25), ("spirit_essence", 0.15)],
		"abilities": ["curse", "ash_cloud", "burning_touch"],
		"regions": ["cinderforge"],
	},
	"forge_titan": {
		"name": "Forge Titan",
		"description": "An enormous construct of metal and magma, built by ancient dwarven smiths to guard their greatest forge. It swings a hammer that could flatten a house.",
		"hp": 130, "attack": 27, "defense": 22,
		"xp_reward": 78, "gold_reward": (25, 55),
		"loot": [("titan_hammer_shard", 0.08), ("dwarven_rune_stone", 0.20), ("magma_core", 0.30), ("enchanted_cloak_fragment", 0.08)],
		"abilities": ["slam", "hammer_strike", "molten_splash", "stone_shield"],
		"regions": ["cinderforge"],
	},

	# ── Dreadmist Isle (Tier 5 Island, lvl 25+) ──
	"mist_stalker": {
		"name": "Mist Stalker",
		"description": "A shadowy predator that exists only in the perpetual fog. Its form is barely visible — just a darker patch of mist with gleaming eyes.",
		"hp": 90, "attack": 28, "defense": 12,
		"xp_reward": 72, "gold_reward": (15, 35),
		"loot": [("shadow_essence", 0.40), ("mist_cloak_fragment", 0.15), ("stalker_fang", 0.30)],
		"abilities": ["ambush", "shadow_strike", "fade"],
		"regions": ["dreadmist"],
	},
	"banshee": {
		"name": "Dreadmist Banshee",
		"description": "A wailing spirit draped in tattered robes, its face a mask of eternal agony. Its scream can stop hearts.",
		"hp": 75, "attack": 30, "defense": 8,
		"xp_reward": 70, "gold_reward": (10, 25),
		"loot": [("spirit_essence", 0.45), ("banshee_tear", 0.20), ("cursed_necklace", 0.10)],
		"abilities": ["screech", "curse", "life_drain"],
		"regions": ["dreadmist"],
	},
	"plague_bearer": {
		"name": "Plague Bearer",
		"description": "A bloated undead creature oozing disease and corruption. Every step leaves a trail of sickness, and its breath is a cloud of pestilence.",
		"hp": 105, "attack": 24, "defense": 16,
		"xp_reward": 75, "gold_reward": (12, 30),
		"loot": [("plague_vial", 0.35), ("corrupted_flesh", 0.45), ("health_potion", 0.20)],
		"abilities": ["slam", "plague_cloud", "venom_strike"],
		"regions": ["dreadmist"],
	},
	"fog_horror": {
		"name": "Fog Horror",
		"description": "A massive amorphous entity that fills corridors with its bulk. Dozens of eyes blink within its foggy mass, and pseudopods lash out unpredictably.",
		"hp": 120, "attack": 26, "defense": 14,
		"xp_reward": 80, "gold_reward": (18, 40),
		"loot": [("horror_eye", 0.30), ("fog_essence", 0.40), ("eldritch_fragment", 0.12)],
		"abilities": ["constrict", "mind_blast", "fog_cloud"],
		"regions": ["dreadmist"],
	},
	"death_knight": {
		"name": "Death Knight",
		"description": "An armored warrior raised from death by dark magic. Black flames lick its blade, and its hollow eye sockets burn with unholy purpose.",
		"hp": 115, "attack": 30, "defense": 18,
		"xp_reward": 85, "gold_reward": (25, 55),
		"loot": [("death_knight_blade_shard", 0.08), ("shadow_essence", 0.35), ("dark_armor_piece", 0.12), ("health_potion", 0.25)],
		"abilities": ["slash", "death_strike", "unholy_shield", "curse"],
		"regions": ["dreadmist"],
	},
	"lich_acolyte": {
		"name": "Lich Acolyte",
		"description": "A skeletal mage draped in rotting robes, its phylactery swinging from a chain around its neck. Dark magic crackles between its bony fingers.",
		"hp": 100, "attack": 32, "defense": 12,
		"xp_reward": 88, "gold_reward": (22, 50),
		"loot": [("lich_phylactery_shard", 0.06), ("dark_rune", 0.25), ("necrotic_staff_fragment", 0.10), ("death_essence", 0.35)],
		"abilities": ["death_bolt", "curse", "life_drain", "summon_undead"],
		"regions": ["dreadmist"],
	},

	# ── Wyrmscale Isle (Tier 6 Island, lvl 30+) ──
	"young_dragon": {
		"name": "Young Dragon",
		"description": "A dragon the size of a horse, scales gleaming like jewels. Young but deadly, with a vicious temper and scorching breath.",
		"hp": 130, "attack": 34, "defense": 18,
		"xp_reward": 95, "gold_reward": (30, 65),
		"loot": [("dragon_scale", 0.40), ("dragon_fang", 0.25), ("dragon_blood_vial", 0.15)],
		"abilities": ["bite", "fire_breath", "tail_swipe", "roar"],
		"regions": ["wyrmscale"],
	},
	"drake_rider": {
		"name": "Drake Rider",
		"description": "A fierce warrior mounted on a smaller drake, wielding a lance of dragonbone. The pair fight as one devastating unit.",
		"hp": 120, "attack": 32, "defense": 16,
		"xp_reward": 90, "gold_reward": (25, 55),
		"loot": [("dragonbone_lance_tip", 0.10), ("drake_hide", 0.35), ("rider_signet", 0.15), ("health_potion", 0.25)],
		"abilities": ["charge", "thrust", "drake_fire"],
		"regions": ["wyrmscale"],
	},
	"wyvern": {
		"name": "Wyvern",
		"description": "A two-legged winged dragon-kin with a venomous tail barb. It strikes from above with devastating speed.",
		"hp": 110, "attack": 30, "defense": 14,
		"xp_reward": 85, "gold_reward": (20, 45),
		"loot": [("wyvern_scale", 0.40), ("wyvern_venom", 0.30), ("raw_meat", 0.40), ("wyvern_wing_membrane", 0.12)],
		"abilities": ["dive", "venom_strike", "tail_swipe"],
		"regions": ["wyrmscale"],
	},
	"dragonkin_shaman": {
		"name": "Dragonkin Shaman",
		"description": "A scaled humanoid with vestigial wings, channeling draconic magic through a staff topped with a dragon skull.",
		"hp": 100, "attack": 35, "defense": 12,
		"xp_reward": 92, "gold_reward": (22, 50),
		"loot": [("dragon_rune", 0.25), ("dragon_blood_vial", 0.20), ("shaman_staff_shard", 0.10)],
		"abilities": ["fire_breath", "dragon_curse", "heal", "summon_drake"],
		"regions": ["wyrmscale"],
	},
	"elder_drake": {
		"name": "Elder Drake",
		"description": "A massive drake covered in battle scars and ancient scales. Its breath can melt stone, and its roar shakes the island.",
		"hp": 150, "attack": 36, "defense": 22,
		"xp_reward": 105, "gold_reward": (35, 75),
		"loot": [("elder_drake_scale", 0.35), ("drake_heart", 0.08), ("dragon_blood_vial", 0.25), ("enchanted_cloak_fragment", 0.10)],
		"abilities": ["fire_breath", "slam", "tail_swipe", "roar", "stone_shield"],
		"regions": ["wyrmscale"],
	},
	"wyrm_cultist": {
		"name": "Wyrm Cultist",
		"description": "A fanatical worshipper of the ancient wyrms, covered in dragon-scale tattoos. They wield obsidian blades and dark draconic magic.",
		"hp": 95, "attack": 28, "defense": 14,
		"xp_reward": 82, "gold_reward": (20, 45),
		"loot": [("obsidian_blade", 0.12), ("dragon_scale", 0.30), ("health_potion", 0.25), ("gold_coin", 0.50)],
		"abilities": ["slash", "dragon_curse", "fire_breath"],
		"regions": ["wyrmscale"],
	},

	# ── Abyssal Depths (Tier 7 Island, lvl 35+) ──
	"abyssal_horror": {
		"name": "Abyssal Horror",
		"description": "A nightmarish deep-sea creature dragged from impossible depths. Too many limbs, too many eyes, and a maw that opens wider than physics should allow.",
		"hp": 150, "attack": 38, "defense": 18,
		"xp_reward": 110, "gold_reward": (30, 65),
		"loot": [("abyssal_chitin", 0.40), ("horror_eye", 0.30), ("void_essence", 0.20)],
		"abilities": ["constrict", "mind_blast", "devour", "deep_scream"],
		"regions": ["abyssal"],
	},
	"void_leviathan_spawn": {
		"name": "Void Leviathan Spawn",
		"description": "A juvenile of the world-ending leviathans that swim between realities. Even young, it distorts space around itself.",
		"hp": 170, "attack": 40, "defense": 20,
		"xp_reward": 120, "gold_reward": (35, 75),
		"loot": [("leviathan_scale", 0.30), ("void_essence", 0.35), ("reality_shard", 0.10)],
		"abilities": ["slam", "reality_warp", "deep_scream", "devour"],
		"regions": ["abyssal"],
	},
	"deep_one_warrior": {
		"name": "Deep One Warrior",
		"description": "A fish-like humanoid from the deepest trenches, wielding weapons of bone and coral. Its cold, intelligent eyes show no mercy.",
		"hp": 120, "attack": 34, "defense": 16,
		"xp_reward": 100, "gold_reward": (22, 50),
		"loot": [("deep_one_scale", 0.40), ("bone_trident_tip", 0.15), ("black_pearl", 0.20), ("health_potion", 0.20)],
		"abilities": ["thrust", "tidal_wave", "screech"],
		"regions": ["abyssal"],
	},
	"shadow_kraken": {
		"name": "Shadow Kraken",
		"description": "Not a true kraken but something worse — a creature of pure shadow given form in the lightless depths. Its tentacles phase through solid matter.",
		"hp": 160, "attack": 36, "defense": 15,
		"xp_reward": 115, "gold_reward": (28, 60),
		"loot": [("shadow_essence", 0.45), ("kraken_ink", 0.35), ("abyssal_chitin", 0.25), ("void_pearl", 0.08)],
		"abilities": ["constrict", "shadow_strike", "fade", "ink_cloud"],
		"regions": ["abyssal"],
	},
	"eldritch_sentinel": {
		"name": "Eldritch Sentinel",
		"description": "A towering construct of alien geometry, covered in eyes that see through dimensions. It guards the threshold between worlds.",
		"hp": 180, "attack": 42, "defense": 24,
		"xp_reward": 130, "gold_reward": (40, 85),
		"loot": [("eldritch_fragment", 0.25), ("sentinel_eye", 0.15), ("reality_shard", 0.12), ("void_pearl", 0.06)],
		"abilities": ["slam", "mind_blast", "reality_warp", "stone_shield", "curse"],
		"regions": ["abyssal"],
	},
	"mind_flayer": {
		"name": "Mind Flayer",
		"description": "A tentacle-faced horror from beyond reality, its psychic powers can shatter minds with a thought. It feeds on intelligence itself.",
		"hp": 140, "attack": 44, "defense": 14,
		"xp_reward": 125, "gold_reward": (35, 70),
		"loot": [("mind_crystal", 0.20), ("tentacle_meat", 0.40), ("psychic_shard", 0.15), ("enchanted_cloak_fragment", 0.12)],
		"abilities": ["mind_blast", "life_drain", "psychic_scream", "dominate"],
		"regions": ["abyssal"],
	},
}

# =====================================================================
# ROOM → REGION MAPPING
# =====================================================================
# Maps room IDs to encounter regions. Rooms not listed use their
# location_type to infer region.

ROOM_REGION_MAP = {
	# Forest
	"clearing": "forest",
	"forest_path": "forest",
	"mossy_hollow": "forest",
	"deep_forest": "forest",
	"woodland_shrine": "forest",
	"ancient_grove": "forest",
	"forest_grove": "forest",
	"dungeon_forest_entrance": "forest",
	"forest_stream": "forest",
	"overgrown_ruins": "forest",
	"hollow_tree": "forest",
	"hunters_blind": "forest",
	"thornwood_copse": "forest",
	"sunlit_glade": "forest",
	"mushroom_grove": "forest",
	"spider_hollow": "forest",
	"old_logging_camp": "forest",
	"druid_stones": "forest",

	# Mountain
	"highland_trail": "mountain",
	"mountain_foothills": "mountain",
	"mountain_path": "mountain",
	"mountain_peak": "mountain",
	"dungeon_mountain_entrance": "mountain",
	"cliffside_ledge": "mountain",
	"eagles_nest": "mountain",
	"windswept_ridge": "mountain",
	"hidden_cave": "mountain",
	"rocky_overlook": "mountain",
	"collapsed_mine": "mountain",
	"goat_trail": "mountain",
	"stone_giant_bones": "mountain",
	"avalanche_debris": "mountain",

	# Swamp
	"swamp_trail": "swamp",
	"foggy_marsh": "swamp",
	"swamp_edge": "swamp",
	"murky_depths": "swamp",
	"sunken_temple": "swamp",
	"will_o_wisp_bog": "swamp",
	"crocodile_pool": "swamp",
	"rotting_pier": "swamp",
	"lizardfolk_territory": "swamp",
	"black_water_lake": "swamp",
	"mangrove_maze": "swamp",

	# Graveyard
	"graveyard_gates": "graveyard",
	"graveyard": "graveyard",
	"open_crypt": "graveyard",
	"haunted_mausoleum": "graveyard",
	"forgotten_graves": "graveyard",
	"bone_pit": "graveyard",

	# Road/transition
	"village_road": "road",
	"village_outskirts": "road",
	"crossroads": "road",
	"watchtower_hill": "road",
	"old_bridge": "road",
	"milestone": "road",
	"roadside_shrine": "road",
	"traders_rest": "road",
	"bandit_ambush_site": "road",

	# Farmland
	"farmland": "farmland",
	"windmill_hill": "farmland",
	"apple_orchard": "farmland",
	"wheat_fields": "farmland",
	"scarecrow_field": "farmland",
	"old_barn": "farmland",
	"beekeepers_meadow": "farmland",

	# Desert
	"desert_dunes": "desert",
	"scorched_wastes": "desert",
	"rocky_badlands": "desert",
	"ancient_temple_ruins": "desert",
	"dried_riverbed": "desert",
	"sandstone_arch": "desert",
	"vulture_roost": "desert",
	"mirage_flats": "desert",
	"buried_statue": "desert",
	"scorpion_nest": "desert",
	"salt_flats": "desert",
	"cactus_grove": "desert",
	"nomad_campsite": "desert",
	"sunken_pyramid": "desert",
	"bone_yard": "desert",

	# Tundra
	"frozen_plains": "tundra",
	"ice_caves": "tundra",
	"frozen_lake": "tundra",
	"mammoth_graveyard": "tundra",
	"aurora_overlook": "tundra",
	"blizzard_pass": "tundra",
	"frost_giant_ruins": "tundra",
	"ice_fishing_hole": "tundra",
	"permafrost_dig": "tundra",
	"snow_drift_valley": "tundra",
	"frozen_waterfall": "tundra",
	"wolf_den": "tundra",
	"yeti_territory": "tundra",
	"ice_shrine": "tundra",
	"abandoned_sled": "tundra",

	# Coast
	"sandy_beach": "coast",
	"rocky_shore": "coast",
	"tidal_pools": "coast",
	"shipwreck_cove": "coast",
	"lighthouse_cliff": "coast",
	"smugglers_cave": "coast",
	"kelp_forest_shallows": "coast",
	"nesting_cliffs": "coast",
	"pirates_landing": "coast",
	"coral_reef_overlook": "coast",
	"beachcombers_stretch": "coast",
	"sea_cave": "coast",
	"jetty_ruins": "coast",
	"fishing_shoals": "coast",
	"merfolk_shrine": "coast",

	# Castle (low danger, patrolled)
	"castle_walls": "castle",
	"castle_gardens": "castle",
	"training_grounds": "castle",
	"royal_stables": "castle",

	# ── Island Regions ──
	# Sunstone Atoll
	"sunstone_beach_south": "sunstone",
	"sunstone_palm_beach": "sunstone",
	"sunstone_palm_grove": "sunstone",
	"sunstone_palm_heights": "sunstone",
	"sunstone_palm_cove": "sunstone",
	"sunstone_tidal_flats": "sunstone",
	"sunstone_coral_shallows": "sunstone",
	"sunstone_coral_arch": "sunstone",
	"sunstone_coral_garden": "sunstone",
	"sunstone_coral_deep": "sunstone",
	"sunstone_coral_grotto": "sunstone",
	"sunstone_lagoon_edge": "sunstone",
	"sunstone_lagoon_center": "sunstone",
	"sunstone_lagoon_falls": "sunstone",
	"sunstone_lagoon_cave": "sunstone",
	"sunstone_jungle_edge": "sunstone",
	"sunstone_jungle_path": "sunstone",
	"sunstone_jungle_heart": "sunstone",
	"sunstone_jungle_canopy": "sunstone",
	"sunstone_jungle_clearing": "sunstone",
	"sunstone_jungle_spring": "sunstone",
	"sunstone_jungle_ruins": "sunstone",
	"sunstone_jungle_overlook": "sunstone",
	"sunstone_temple_approach": "sunstone",
	"sunstone_temple_gate": "sunstone",
	"sunstone_temple_courtyard": "sunstone",
	"sunstone_temple_inner": "sunstone",
	"sunstone_temple_altar": "sunstone",
	"sunstone_temple_deep_crypt": "sunstone",
	"sunstone_hidden_cove": "sunstone",
	"sunstone_pirate_cache": "sunstone",
	"sunstone_smuggler_tunnel": "sunstone",
	"sunstone_volcanic_vent": "sunstone",
	"sunstone_obsidian_pool": "sunstone",
	"sunstone_lava_tube": "sunstone",
	"sunstone_tide_pools": "sunstone",
	"sunstone_craft_hut": "sunstone",
	"sunstone_lookout_tower": "sunstone",
	"sunstone_fishing_spot": "sunstone",
	"sunstone_shell_beach": "sunstone",
}

# Settlement/building rooms that NEVER have encounters
SAFE_ROOMS = {
	# Starting village
	"village_square", "village_tavern", "village_shop", "village_blacksmith",
	"village_east_end", "chapel", "hermit_cabin",
	# Other villages
	"fishing_village", "mining_village", "swamp_village",
	# Oasis
	"oasis_village", "oasis_well", "oasis_market",
	# Port Haven
	"port_haven_docks", "port_haven_market", "port_haven_north", "harbor_inn",
	"harbor_warehouse", "sailors_guild",
	# Tundra settlements
	"tundra_outpost", "warm_springs_inn", "fur_traders_post",
	# Castle
	"castle_gates", "castle_courtyard", "castle_throne_room", "castle_barracks",
	"castle_armory", "castle_library", "castle_kitchen", "castle_dungeon_entrance",
	# Other safe locations
	"witch_hut", "dungeon_ruins_entrance",
	# Grand Harbor
	"grand_harbor_road", "grand_harbor_gate", "grand_harbor_square",
	"harbor_master_office", "harbor_tavern", "harbor_inn_room",
	"harbor_shop", "harbor_south_pier", "harbor_watchtower",
	"harbor_north_dock", "harbor_east_dock", "harbor_west_dock",
	"harbor_warehouse",
	# Island settlements
	"sunstone_docks", "sunstone_dock_market", "sunstone_dock_storage",
	"sunstone_village_west", "sunstone_village_center", "sunstone_village_east",
	"sunstone_village_elder", "sunstone_village_healer", "sunstone_village_smith",
	"sunstone_village_inn", "sunstone_village_shrine", "sunstone_village_well",
	"sunstone_village_lookout", "sunstone_village_market", "sunstone_village_garden",
	# Emerald Isle settlements
	"emerald_docks", "emerald_dock_cargo", "emerald_dock_lookout",
	"emerald_village_path", "emerald_village_gate", "emerald_village_center",
	"emerald_village_elder", "emerald_village_healer", "emerald_village_market",
	"emerald_village_inn", "emerald_village_shrine", "emerald_village_garden",
	"emerald_village_workshop", "emerald_village_lookout", "emerald_village_bridge",
	"emerald_village_spring", "emerald_village_hollow", "emerald_village_grove",
	# Stormbreak Reef settlements
	"stormbreak_docks", "stormbreak_dock_cargo", "stormbreak_dock_lighthouse",
	"stormbreak_town_gate", "stormbreak_town_center", "stormbreak_town_elder",
	"stormbreak_town_healer", "stormbreak_town_market", "stormbreak_town_inn",
	"stormbreak_town_smithy", "stormbreak_town_shrine", "stormbreak_town_tavern",
	"stormbreak_town_sailmaker", "stormbreak_town_lookout", "stormbreak_town_well",
	"stormbreak_town_hall", "stormbreak_town_barracks", "stormbreak_town_stable",
	# Cinderforge Isle settlements
	"cinder_docks", "cinder_dock_cargo", "cinder_dock_beacon",
	"cinder_village_gate", "cinder_village_center", "cinder_village_elder",
	"cinder_village_healer", "cinder_village_market", "cinder_village_inn",
	"cinder_village_smithy", "cinder_village_shrine", "cinder_village_tavern",
	"cinder_village_workshop", "cinder_village_lookout", "cinder_village_well",
	# Dreadmist Isle settlements
	"dreadmist_docks", "dreadmist_dock_cargo", "dreadmist_dock_lantern",
	"dreadmist_village_gate", "dreadmist_village_center", "dreadmist_village_elder",
	"dreadmist_village_healer", "dreadmist_village_market", "dreadmist_village_inn",
	"dreadmist_village_shrine", "dreadmist_village_tavern", "dreadmist_village_smith",
	"dreadmist_village_crypt_keeper", "dreadmist_village_lookout", "dreadmist_village_well",
	# Wyrmscale Isle settlements
	"wyrm_docks", "wyrm_dock_cargo", "wyrm_dock_watchtower",
	"wyrm_village_gate", "wyrm_village_center", "wyrm_village_elder",
	"wyrm_village_healer", "wyrm_village_market", "wyrm_village_inn",
	"wyrm_village_smithy", "wyrm_village_shrine", "wyrm_village_tavern",
	"wyrm_village_armory", "wyrm_village_lookout", "wyrm_village_well",
	# Abyssal Depths settlements
	"abyssal_docks", "abyssal_dock_cargo", "abyssal_dock_beacon",
	"abyssal_outpost_gate", "abyssal_outpost_center", "abyssal_outpost_commander",
	"abyssal_outpost_healer", "abyssal_outpost_market", "abyssal_outpost_barracks",
	"abyssal_outpost_shrine", "abyssal_outpost_tavern", "abyssal_outpost_armory",
	"abyssal_outpost_lookout", "abyssal_outpost_well",
}

# =====================================================================
# ENCOUNTER CONFIGURATION
# =====================================================================

# Base chance of random encounter in wilderness rooms (0.0 - 1.0)
OVERWORLD_SPAWN_CHANCE = 0.13

# Rooms recently visited have lower encounter chance (cooldown tracking)
ENCOUNTER_COOLDOWN = 4  # Must visit N other rooms before re-roll

# Chance multiplier by region danger level
REGION_DANGER = {
	"forest": 1.0,
	"mountain": 1.2,
	"swamp": 1.3,
	"graveyard": 1.5,
	"road": 0.6,
	"farmland": 0.4,
	"desert": 1.1,
	"tundra": 1.4,
	"coast": 0.8,
	"castle": 0.2,  # Heavily patrolled, very safe
	# Island regions — progressively more dangerous
	"sunstone": 1.6,
	"emerald": 1.8,
	"stormbreak": 2.0,
	"cinderforge": 2.2,
	"dreadmist": 2.5,
	"wyrmscale": 2.8,
	"abyssal": 3.2,
}

# Level scaling: stat multiplier per player level above 1
OVERWORLD_LEVEL_SCALE = 0.08  # +8% stats per player level

# =====================================================================
# VISIBLE ENCOUNTER SYSTEM
# =====================================================================
# Some rooms have persistent visible enemies that appear in descriptions
# and must be engaged before looting/progressing freely.

# Probability that a wilderness room has a visible enemy on first visit
VISIBLE_ENEMY_CHANCE = 0.18


class OverworldEncounterManager:
	"""Manages random and visible overworld encounters."""

	def __init__(self, engine):
		self.engine = engine
		# Tracks recent rooms for cooldown
		self.recent_rooms = []
		# Persistent visible enemies: {room_id: enemy_data_dict}
		self.visible_enemies = {}
		# Rooms that have already been rolled for visible enemies
		self.rooms_rolled = set()

	def _get_game_feel_intensity(self):
		"""Resolve current gameplay intensity for encounter messaging cadence."""
		if hasattr(self.engine, "get_game_feel_intensity"):
			return self.engine.get_game_feel_intensity()
		level = "normal"
		try:
			cfg = getattr(getattr(self.engine, "gui", None), "config", None)
			if isinstance(cfg, dict):
				gameplay = cfg.get("gameplay", {})
				if isinstance(gameplay, dict):
					level = gameplay.get("game_feel_intensity", "normal")
		except Exception:
			level = "normal"
		level = str(level or "normal").strip().lower()
		if level not in ("low", "normal", "high"):
			return "normal"
		return level

	def _format_visible_enemy_text(self, enemy_name):
		"""Format room warning text for visible enemies based on feel intensity."""
		feel = self._get_game_feel_intensity()
		if feel == "low":
			return f"\n  ⚠️ {enemy_name} nearby. (Type 'fight')"
		if feel == "high":
			flair = random.choice([
				"The air tightens as it stalks your position.",
				"Its movement syncs with your heartbeat.",
				"You sense violence coiled, ready to spring.",
			])
			return f"\n  ⚠️ A {enemy_name} prowls here! (Type 'fight' to engage)\n  {flair}"
		return f"\n  ⚠️ A {enemy_name} lurks here! (Type 'fight' to engage)"

	# ─── Region Detection ───

	def get_region(self, room_id):
		"""Determine the encounter region for a room."""
		if room_id in ROOM_REGION_MAP:
			return ROOM_REGION_MAP[room_id]
		# Infer from room name
		rid = room_id.lower()
		if "forest" in rid or "grove" in rid or "wood" in rid:
			return "forest"
		if "mountain" in rid or "highland" in rid or "peak" in rid or "foothill" in rid or "cliff" in rid:
			return "mountain"
		if "swamp" in rid or "marsh" in rid or "bog" in rid:
			return "swamp"
		if "grave" in rid or "crypt" in rid or "tomb" in rid:
			return "graveyard"
		if "farm" in rid or "field" in rid or "orchard" in rid or "barn" in rid:
			return "farmland"
		if "road" in rid or "trail" in rid or "path" in rid or "crossroad" in rid:
			return "road"
		if "desert" in rid or "sand" in rid or "dune" in rid or "oasis" in rid or "pyramid" in rid:
			return "desert"
		if "tundra" in rid or "frozen" in rid or "ice" in rid or "snow" in rid or "frost" in rid:
			return "tundra"
		if "coast" in rid or "beach" in rid or "shore" in rid or "harbor" in rid or "port" in rid or "pier" in rid or "lighthouse" in rid:
			return "coast"
		if "castle" in rid or "royal" in rid or "throne" in rid:
			return "castle"
		# Island regions (prefix-based)
		if rid.startswith("sunstone_"):
			return "sunstone"
		if rid.startswith("emerald_"):
			return "emerald"
		if rid.startswith("stormbreak_"):
			return "stormbreak"
		if rid.startswith("cinder_") or rid.startswith("cinderforge_"):
			return "cinderforge"
		if rid.startswith("dreadmist_"):
			return "dreadmist"
		if rid.startswith("wyrm_") or rid.startswith("wyrmscale_"):
			return "wyrmscale"
		if rid.startswith("abyssal_"):
			return "abyssal"
		if "harbor" in rid or "dock" in rid:
			return "coast"
		return "forest"  # default

	def is_safe_room(self, room_id):
		"""Check if a room is a safe zone (no encounters)."""
		if room_id in SAFE_ROOMS:
			return True
		# Check location_type
		room = self.engine.rooms.get(room_id)
		if room:
			lt = getattr(room, "location_type", "wilderness")
			if lt in ("settlement", "building"):
				return True
		# Dungeon rooms handled separately
		if room_id.startswith("dungeon_") and "_floor" in room_id:
			return True
		if hasattr(self.engine, 'fixed_dungeon_room_ids') and room_id in self.engine.fixed_dungeon_room_ids:
			return True
		return False

	# ─── Enemy Selection ───

	def get_enemies_for_region(self, region):
		"""Get list of enemy IDs suitable for a region."""
		primary = []
		secondary = []
		for eid, edata in OVERWORLD_ENEMIES.items():
			regions = list(edata.get("regions", []))
			if not regions or region not in regions:
				continue
			# First listed region is treated as the biome identity region.
			if regions[0] == region:
				primary.append(eid)
			else:
				secondary.append(eid)

		# Prefer primary-region enemies heavily for stronger biome identity.
		if primary:
			return primary + secondary[: max(1, len(primary) // 3)]
		return secondary

	def scale_enemy(self, enemy_id, player_level=1):
		"""Create a scaled enemy data dict for combat."""
		template = OVERWORLD_ENEMIES.get(enemy_id)
		if not template:
			return None

		data = dict(template)
		data["id"] = enemy_id

		# Scale stats based on player level
		scale = 1 + (player_level - 1) * OVERWORLD_LEVEL_SCALE
		data["hp"] = max(10, int(data["hp"] * scale))
		data["attack"] = max(3, int(data["attack"] * scale))
		data["defense"] = max(1, int(data["defense"] * scale))
		data["xp_reward"] = max(5, int(data["xp_reward"] * scale))

		# Scale gold reward
		gmin, gmax = data["gold_reward"]
		data["gold_reward"] = (max(1, int(gmin * scale)), max(2, int(gmax * scale)))

		return data

	# ─── Random Encounter Check ───

	def check_random_encounter(self, room_id):
		"""Check if a random encounter should trigger on entering a room.
		Returns (should_fight: bool, enemy_data: dict or None).
		"""
		if self.is_safe_room(room_id):
			return False, None

		# Cooldown check — skip if recently visited
		if room_id in self.recent_rooms:
			return False, None

		# Track room in recent list
		self.recent_rooms.append(room_id)
		if len(self.recent_rooms) > ENCOUNTER_COOLDOWN:
			self.recent_rooms.pop(0)

		# Don't trigger if there's a visible enemy here (fight that instead)
		if room_id in self.visible_enemies:
			return False, None

		# Get region and check eligible enemies
		region = self.get_region(room_id)
		eligible = self.get_enemies_for_region(region)
		if not eligible:
			return False, None

		# Roll for encounter
		danger = REGION_DANGER.get(region, 1.0)
		chance = OVERWORLD_SPAWN_CHANCE * danger
		if random.random() >= chance:
			return False, None

		# Spawn an enemy
		enemy_id = random.choice(eligible)
		player_level = 1
		if hasattr(self.engine, 'player') and self.engine.player:
			player_level = self.engine.player.stats.get("level", 1)

		enemy_data = self.scale_enemy(enemy_id, player_level)
		return True, enemy_data

	# ─── Visible Encounter System ───

	def roll_visible_enemy(self, room_id):
		"""Roll once for a visible enemy in a room (only on first visit).
		Returns enemy description text to add to room, or empty string.
		"""
		if self.is_safe_room(room_id):
			return ""
		if room_id in self.rooms_rolled:
			return ""

		self.rooms_rolled.add(room_id)

		region = self.get_region(room_id)
		feel = self._get_game_feel_intensity()

		# Roll chance (scaled by regional danger, capped for sanity)
		danger = REGION_DANGER.get(region, 1.0)
		visible_chance = min(0.45, VISIBLE_ENEMY_CHANCE * (0.75 + 0.25 * danger))
		if feel == "low":
			visible_chance *= 0.85
		elif feel == "high":
			visible_chance = min(0.55, visible_chance * 1.20)
		if random.random() >= visible_chance:
			return ""

		eligible = self.get_enemies_for_region(region)
		if not eligible:
			return ""

		enemy_id = random.choice(eligible)
		player_level = 1
		if hasattr(self.engine, 'player') and self.engine.player:
			player_level = self.engine.player.stats.get("level", 1)

		enemy_data = self.scale_enemy(enemy_id, player_level)
		if not enemy_data:
			return ""

		# Store visible enemy
		self.visible_enemies[room_id] = {
			"enemy_id": enemy_id,
			"enemy_data": enemy_data,
		}

		return self._format_visible_enemy_text(enemy_data["name"])

	def get_visible_enemy_text(self, room_id):
		"""Get text about any visible enemy in a room."""
		if room_id not in self.visible_enemies:
			return ""
		enemy = self.visible_enemies[room_id]
		return self._format_visible_enemy_text(enemy["enemy_data"]["name"])

	def engage_visible_enemy(self, room_id):
		"""Start combat with a visible enemy. Returns enemy_data or None."""
		if room_id not in self.visible_enemies:
			return None
		enemy_info = self.visible_enemies.pop(room_id)
		return enemy_info["enemy_data"]

	# ─── Persistence ───

	def to_dict(self):
		"""Serialize for saving."""
		return {
			"recent_rooms": list(self.recent_rooms),
			"visible_enemies": {
				room_id: {
					"enemy_id": info["enemy_id"],
					"enemy_data": {
						k: v for k, v in info["enemy_data"].items()
						if k != "regions"  # don't save region tags
					},
				}
				for room_id, info in self.visible_enemies.items()
			},
			"rooms_rolled": list(self.rooms_rolled),
		}

	def load_from_dict(self, data):
		"""Restore from saved data."""
		if not isinstance(data, dict):
			return
		self.recent_rooms = list(data.get("recent_rooms", []))
		self.rooms_rolled = set(data.get("rooms_rolled", []))
		self.visible_enemies = {}
		for room_id, info in data.get("visible_enemies", {}).items():
			self.visible_enemies[room_id] = {
				"enemy_id": info.get("enemy_id", "unknown"),
				"enemy_data": info.get("enemy_data", {}),
			}
