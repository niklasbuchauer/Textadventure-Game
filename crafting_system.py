"""
Crafting System
===============
Station-based crafting with discoverable recipes.
Recipes are learned from NPCs, books, or discovered at altars.
Crafting requires being at the correct station type.
"""

# Progression integration
try:
	from progression_system import award_xp, XP_AWARDS
	PROGRESSION_AVAILABLE = True
except ImportError:
	PROGRESSION_AVAILABLE = False

# =====================================================================
# STATION TYPES
# =====================================================================
# "forge"          — Village Blacksmith
# "altar_crystal"  — Crystal Caverns (Forge of Light)
# "altar_shadow"   — Shadow Depths (Shadowforge)
# "altar_iron"     — Iron Halls (Dwarven Anvil / altar)
# "altar_catacomb" — Sunken Catacombs (altar)
# "any"            — Any crafting station (forge or any altar)
# =====================================================================

STATION_NAMES = {
	"forge": "Blacksmith's Forge",
	"altar_crystal": "Forge of Light",
	"altar_shadow": "The Shadowforge",
	"altar_iron": "Dwarven Eternal Anvil",
	"altar_catacomb": "Catacomb Soul Altar",
	"campfire": "Campfire",
}

# =====================================================================
# RECIPE DATABASE
# =====================================================================
# Each recipe:
#   id:          unique string identifier
#   name:        display name
#   ingredients: {item_name: count_needed}
#   result:      (item_name, count_produced)
#   station:     station type required (or "any")
#   description: flavor text
#   auto_discover: True if discovered when visiting the altar (not NPC-taught)
# =====================================================================

RECIPE_DATABASE = {
	# ─── FORGE (Blacksmith) Recipes ─────────────────────────────────
	"steel_dagger": {
		"id": "steel_dagger",
		"name": "Steel Dagger",
		"ingredients": {"iron_ingot": 1, "stick": 1},
		"result": ("steel_dagger", 1),
		"station": "forge",
		"description": "A sharp, reliable dagger forged from iron and wood.",
	},
	"iron_sword": {
		"id": "iron_sword",
		"name": "Iron Sword",
		"ingredients": {"iron_ingot": 2, "stick": 1},
		"result": ("iron_sword", 1),
		"station": "forge",
		"description": "A sturdy iron sword. The blacksmith's bread and butter.",
	},
	"steel_longsword": {
		"id": "steel_longsword",
		"name": "Steel Longsword",
		"ingredients": {"iron_ingot": 3, "refined_iron": 1},
		"result": ("steel_longsword", 1),
		"station": "forge",
		"description": "A long, balanced blade of tempered steel.",
	},
	"leather_armor_piece": {
		"id": "leather_armor_piece",
		"name": "Leather Armor",
		"ingredients": {"wolf_pelt": 2, "rope_coil": 1},
		"result": ("leather_armor_piece", 1),
		"station": "forge",
		"description": "Light armor stitched from wolf pelts. Offers decent protection.",
	},
	"masterwork_shield": {
		"id": "masterwork_shield",
		"name": "Masterwork Shield",
		"ingredients": {"iron_ingot": 2, "broken_shield": 1, "refined_iron": 1},
		"result": ("masterwork_shield", 1),
		"station": "forge",
		"description": "A shield reforged from scrap into something magnificent.",
	},
	"refined_iron": {
		"id": "refined_iron",
		"name": "Refined Iron",
		"ingredients": {"iron_ingot": 2},
		"result": ("refined_iron", 1),
		"station": "forge",
		"description": "Purified iron, ready for advanced smithing.",
	},

	# ─── ANY STATION Recipes (potions, simpler crafts) ──────────────
	"healing_potion": {
		"id": "healing_potion",
		"name": "Healing Potion",
		"ingredients": {"strange_herb": 2, "mineral_water_flask": 1},
		"result": ("healing_potion", 1),
		"station": "any",
		"description": "A powerful restorative potion brewed from rare herbs.",
	},
	"antidote": {
		"id": "antidote",
		"name": "Antidote",
		"ingredients": {"strange_herb": 1, "shelf_mushroom": 2},
		"result": ("antidote", 1),
		"station": "any",
		"description": "A remedy that neutralizes most poisons.",
	},
	"poison_cure": {
		"id": "poison_cure",
		"name": "Swamp Poison Cure",
		"ingredients": {"glowing_moss": 2, "marsh_lily": 1},
		"result": ("poison_cure", 1),
		"station": "any",
		"description": "A potent cure brewed from swamp ingredients. The witch's specialty.",
	},
	"holy_water": {
		"id": "holy_water",
		"name": "Holy Water",
		"ingredients": {"prayer_candle": 1, "mineral_water_flask": 1},
		"result": ("holy_water", 1),
		"station": "any",
		"description": "Water blessed with divine energy. Heals and purifies.",
	},
	"quality_torch": {
		"id": "quality_torch",
		"name": "Quality Torch",
		"ingredients": {"torch": 1, "rope_coil": 1, "glowing_moss": 1},
		"result": ("quality_torch", 1),
		"station": "any",
		"description": "A well-made torch with a long-lasting, bright flame.",
	},

	# ─── CRYSTAL ALTAR Recipes ──────────────────────────────────────
	"crystal_shield": {
		"id": "crystal_shield",
		"name": "Crystal Shield",
		"ingredients": {"raw_diamond": 1, "heart_crystal_fragment": 1},
		"result": ("crystal_shield", 1),
		"station": "altar_crystal",
		"description": "A shield of living crystal that refracts attacks into harmless light.",
		"auto_discover": True,
	},
	"enchanted_ring": {
		"id": "enchanted_ring",
		"name": "Enchanted Ring",
		"ingredients": {"golden_ring": 1, "resonance_crystal": 1},
		"result": ("enchanted_ring", 1),
		"station": "altar_crystal",
		"description": "A ring humming with crystalline energy.",
		"auto_discover": True,
	},
	"prismatic_blade": {
		"id": "prismatic_blade",
		"name": "Prismatic Blade",
		"ingredients": {"spectrum_prism": 1, "steel_longsword": 1, "concentrated_light_essence": 1},
		"result": ("prismatic_blade", 1),
		"station": "altar_crystal",
		"description": "A sword that splits light into deadly rainbows with each swing.",
		"auto_discover": True,
	},

	# ─── SHADOW ALTAR Recipes ───────────────────────────────────────
	"shadow_blade": {
		"id": "shadow_blade",
		"name": "Shadow Blade",
		"ingredients": {"obsidian_blade_fragment": 2, "concentrated_void_essence": 1},
		"result": ("shadow_blade", 1),
		"station": "altar_shadow",
		"description": "A blade forged from void and obsidian. Cuts through shadow and steel alike.",
		"auto_discover": True,
	},
	"void_amulet": {
		"id": "void_amulet",
		"name": "Void Amulet",
		"ingredients": {"dread_idol": 1, "void_heart_fragment": 1},
		"result": ("void_amulet", 1),
		"station": "altar_shadow",
		"description": "An amulet pulsing with void energy. Protects against shadow attacks.",
		"auto_discover": True,
	},
	"sovereign_cloak": {
		"id": "sovereign_cloak",
		"name": "Sovereign's Cloak",
		"ingredients": {"sovereign_shadow_crown": 1, "enchanted_cloak_fragment": 1, "umbral_thread": 2},
		"result": ("sovereign_cloak", 1),
		"station": "altar_shadow",
		"description": "A cloak woven from the Shadow Sovereign's own essence. Grants partial invisibility.",
		"auto_discover": True,
	},

	# ─── IRON ALTAR Recipes ─────────────────────────────────────────
	"mithril_blade": {
		"id": "mithril_blade",
		"name": "Mithril Blade",
		"ingredients": {"raw_mithril": 1, "eternal_ember": 1},
		"result": ("mithril_blade", 1),
		"station": "altar_iron",
		"description": "The finest blade that can be forged. Light as a feather, strong as mountains.",
		"auto_discover": True,
	},
	"dwarven_masterwork": {
		"id": "dwarven_masterwork",
		"name": "Dwarven Masterwork Armor",
		"ingredients": {"tempered_steel_ingot": 2, "mithril_dust": 1, "forgemaster_hammer": 1},
		"result": ("dwarven_masterwork", 1),
		"station": "altar_iron",
		"description": "Armor forged using ancient dwarven techniques. Nearly indestructible.",
		"auto_discover": True,
	},

	# ─── CATACOMB ALTAR Recipes ─────────────────────────────────────
	"soul_blade": {
		"id": "soul_blade",
		"name": "Soul Blade",
		"ingredients": {"soul_gem": 1, "cracked_phylactery": 1, "iron_sword": 1},
		"result": ("soul_blade", 1),
		"station": "altar_catacomb",
		"description": "A blade infused with spectral energy. Glows with ghostly fire.",
		"auto_discover": True,
	},
	"lich_crown": {
		"id": "lich_crown",
		"name": "Lich Crown",
		"ingredients": {"lich_crown_fragment": 1, "enchanted_ring": 1, "blood_ruby": 1},
		"result": ("lich_crown", 1),
		"station": "altar_catacomb",
		"description": "A crown of dark power, restored from its shattered form.",
		"auto_discover": True,
	},

	# ═══════════════════════════════════════════════════════════════════
	# EXPANDED EQUIPMENT CRAFTING - Common & Uncommon at Forge
	# ═══════════════════════════════════════════════════════════════════

	# --- WEAPONS (Forge) ---
	"bronze_sword": {
		"id": "bronze_sword",
		"name": "Bronze Sword",
		"ingredients": {"copper_ore": 2, "tin_ore": 1, "stick": 1},
		"result": ("bronze_sword", 1),
		"station": "forge",
		"description": "A simple sword made from bronze alloy.",
	},
	"iron_axe": {
		"id": "iron_axe",
		"name": "Iron Axe",
		"ingredients": {"iron_ingot": 2, "stick": 1, "rope_coil": 1},
		"result": ("iron_axe", 1),
		"station": "forge",
		"description": "A heavy axe for chopping foes and firewood alike.",
	},
	"steel_mace": {
		"id": "steel_mace",
		"name": "Steel Mace",
		"ingredients": {"refined_iron": 2, "iron_ingot": 1},
		"result": ("steel_mace", 1),
		"station": "forge",
		"description": "A weighty mace that crushes armor.",
	},
	"hunters_bow": {
		"id": "hunters_bow",
		"name": "Hunter's Bow",
		"ingredients": {"stick": 3, "rope_coil": 2, "wolf_pelt": 1},
		"result": ("hunters_bow", 1),
		"station": "forge",
		"description": "A reliable bow for hunting and combat.",
	},
	"silver_rapier": {
		"id": "silver_rapier",
		"name": "Silver Rapier",
		"ingredients": {"silver_ingot": 2, "refined_iron": 1},
		"result": ("silver_rapier", 1),
		"station": "forge",
		"description": "An elegant thrusting blade of pure silver.",
	},

	# --- ARMOR (Forge) ---
	"padded_vest": {
		"id": "padded_vest",
		"name": "Padded Vest",
		"ingredients": {"cloth_scraps": 4, "rope_coil": 1},
		"result": ("padded_vest", 1),
		"station": "forge",
		"description": "A simple padded vest offering basic protection.",
	},
	"chainmail_shirt": {
		"id": "chainmail_shirt",
		"name": "Chainmail Shirt",
		"ingredients": {"iron_ingot": 4, "rope_coil": 2},
		"result": ("chainmail_shirt", 1),
		"station": "forge",
		"description": "Interlocking iron rings provide flexible protection.",
	},
	"iron_plate": {
		"id": "iron_plate",
		"name": "Iron Plate Armor",
		"ingredients": {"iron_ingot": 5, "refined_iron": 2, "leather_strip": 2},
		"result": ("iron_plate", 1),
		"station": "forge",
		"description": "Heavy plate armor forged from solid iron.",
	},

	# --- HELMS (Forge) ---
	"leather_cap": {
		"id": "leather_cap",
		"name": "Leather Cap",
		"ingredients": {"wolf_pelt": 1, "leather_strip": 2},
		"result": ("leather_cap", 1),
		"station": "forge",
		"description": "A simple leather cap for head protection.",
	},
	"iron_helm": {
		"id": "iron_helm",
		"name": "Iron Helm",
		"ingredients": {"iron_ingot": 2, "leather_strip": 1},
		"result": ("iron_helm", 1),
		"station": "forge",
		"description": "A solid iron helmet with nose guard.",
	},
	"steel_greathelm": {
		"id": "steel_greathelm",
		"name": "Steel Greathelm",
		"ingredients": {"refined_iron": 3, "iron_ingot": 2},
		"result": ("steel_greathelm", 1),
		"station": "forge",
		"description": "A fully enclosed helm of tempered steel.",
	},

	# --- BOOTS (Forge) ---
	"leather_boots": {
		"id": "leather_boots",
		"name": "Leather Boots",
		"ingredients": {"wolf_pelt": 2, "rope_coil": 1},
		"result": ("leather_boots", 1),
		"station": "forge",
		"description": "Sturdy boots for long journeys.",
	},
	"iron_sabatons": {
		"id": "iron_sabatons",
		"name": "Iron Sabatons",
		"ingredients": {"iron_ingot": 2, "leather_strip": 2},
		"result": ("iron_sabatons", 1),
		"station": "forge",
		"description": "Heavy iron boots that clank with each step.",
	},
	"steel_greaves": {
		"id": "steel_greaves",
		"name": "Steel Greaves",
		"ingredients": {"refined_iron": 2, "iron_ingot": 2, "leather_strip": 1},
		"result": ("steel_greaves", 1),
		"station": "forge",
		"description": "Steel leg armor extending from knee to ankle.",
	},

	# --- GLOVES (Forge) ---
	"cloth_gloves": {
		"id": "cloth_gloves",
		"name": "Cloth Gloves",
		"ingredients": {"cloth_scraps": 2},
		"result": ("cloth_gloves", 1),
		"station": "forge",
		"description": "Simple cloth hand wraps.",
	},
	"leather_gloves": {
		"id": "leather_gloves",
		"name": "Leather Gloves",
		"ingredients": {"wolf_pelt": 1, "leather_strip": 1},
		"result": ("leather_gloves", 1),
		"station": "forge",
		"description": "Sturdy leather gloves with good grip.",
	},
	"iron_gauntlets": {
		"id": "iron_gauntlets",
		"name": "Iron Gauntlets",
		"ingredients": {"iron_ingot": 2, "leather_strip": 1},
		"result": ("iron_gauntlets", 1),
		"station": "forge",
		"description": "Heavy iron gauntlets that double as weapons.",
	},

	# --- SHIELDS (Forge) ---
	"wooden_buckler": {
		"id": "wooden_buckler",
		"name": "Wooden Buckler",
		"ingredients": {"stick": 3, "rope_coil": 1},
		"result": ("wooden_buckler", 1),
		"station": "forge",
		"description": "A small wooden shield for parrying.",
	},
	"iron_kite_shield": {
		"id": "iron_kite_shield",
		"name": "Iron Kite Shield",
		"ingredients": {"iron_ingot": 3, "leather_strip": 2},
		"result": ("iron_kite_shield", 1),
		"station": "forge",
		"description": "A large kite-shaped shield for infantry.",
	},
	"steel_tower_shield": {
		"id": "steel_tower_shield",
		"name": "Steel Tower Shield",
		"ingredients": {"refined_iron": 3, "iron_ingot": 2, "leather_strip": 2},
		"result": ("steel_tower_shield", 1),
		"station": "forge",
		"description": "A massive tower shield providing full body coverage.",
	},

	# --- ACCESSORIES (Forge/Any) ---
	"copper_ring": {
		"id": "copper_ring",
		"name": "Copper Ring",
		"ingredients": {"copper_ore": 2},
		"result": ("copper_ring", 1),
		"station": "forge",
		"description": "A simple copper ring with minor enchantment.",
	},
	"silver_ring": {
		"id": "silver_ring",
		"name": "Silver Ring",
		"ingredients": {"silver_ingot": 1},
		"result": ("silver_ring", 1),
		"station": "forge",
		"description": "A silver ring that wards off curses.",
	},
	"bone_amulet": {
		"id": "bone_amulet",
		"name": "Bone Amulet",
		"ingredients": {"bone_fragments": 3, "rope_coil": 1},
		"result": ("bone_amulet", 1),
		"station": "any",
		"description": "A tribal amulet carved from bones.",
	},

	# ═══════════════════════════════════════════════════════════════════
	# CRYSTAL ALTAR RECIPES - Crystal-themed Epic/Legendary Equipment
	# ═══════════════════════════════════════════════════════════════════

	"crystal_blade": {
		"id": "crystal_blade",
		"name": "Crystal Blade",
		"ingredients": {"heart_crystal_fragment": 2, "resonance_crystal": 1, "steel_longsword": 1},
		"result": ("crystal_blade", 1),
		"station": "altar_crystal",
		"description": "A sword of pure crystallized light.",
		"auto_discover": True,
	},
	"radiant_helm": {
		"id": "radiant_helm",
		"name": "Radiant Helm",
		"ingredients": {"heart_crystal_fragment": 1, "steel_greathelm": 1, "concentrated_light_essence": 1},
		"result": ("radiant_helm", 1),
		"station": "altar_crystal",
		"description": "A helm that glows with inner light.",
		"auto_discover": True,
	},
	"prismatic_boots": {
		"id": "prismatic_boots",
		"name": "Prismatic Boots",
		"ingredients": {"spectrum_prism": 1, "steel_greaves": 1, "resonance_crystal": 1},
		"result": ("prismatic_boots", 1),
		"station": "altar_crystal",
		"description": "Boots that leave rainbow trails with each step.",
		"auto_discover": True,
	},
	"crystalweave_gloves": {
		"id": "crystalweave_gloves",
		"name": "Crystalweave Gloves",
		"ingredients": {"heart_crystal_fragment": 1, "leather_gloves": 1, "concentrated_light_essence": 1},
		"result": ("crystalweave_gloves", 1),
		"station": "altar_crystal",
		"description": "Gloves woven with crystal thread.",
		"auto_discover": True,
	},
	"lightweaver_robes": {
		"id": "lightweaver_robes",
		"name": "Lightweaver Robes",
		"ingredients": {"concentrated_light_essence": 2, "enchanted_cloak_fragment": 1, "resonance_crystal": 1},
		"result": ("lightweaver_robes", 1),
		"station": "altar_crystal",
		"description": "Robes that shimmer with captured sunlight.",
		"auto_discover": True,
	},

	# ═══════════════════════════════════════════════════════════════════
	# SHADOW ALTAR RECIPES - Shadow-themed Epic/Legendary Equipment
	# ═══════════════════════════════════════════════════════════════════

	"nightblade": {
		"id": "nightblade",
		"name": "Nightblade",
		"ingredients": {"obsidian_blade_fragment": 2, "steel_longsword": 1, "umbral_thread": 2},
		"result": ("nightblade", 1),
		"station": "altar_shadow",
		"description": "A blade that drinks in light.",
		"auto_discover": True,
	},
	"shadowstep_boots": {
		"id": "shadowstep_boots",
		"name": "Shadowstep Boots",
		"ingredients": {"umbral_thread": 3, "leather_boots": 1, "concentrated_void_essence": 1},
		"result": ("shadowstep_boots", 1),
		"station": "altar_shadow",
		"description": "Boots that muffle sound and shadow.",
		"auto_discover": True,
	},
	"hood_of_whispers": {
		"id": "hood_of_whispers",
		"name": "Hood of Whispers",
		"ingredients": {"umbral_thread": 2, "leather_cap": 1, "dread_idol": 1},
		"result": ("hood_of_whispers", 1),
		"station": "altar_shadow",
		"description": "A hood that lets you hear secrets on the wind.",
		"auto_discover": True,
	},
	"void_touched_gauntlets": {
		"id": "void_touched_gauntlets",
		"name": "Void-Touched Gauntlets",
		"ingredients": {"void_heart_fragment": 1, "iron_gauntlets": 1, "concentrated_void_essence": 1},
		"result": ("void_touched_gauntlets", 1),
		"station": "altar_shadow",
		"description": "Gauntlets that phase through armor.",
		"auto_discover": True,
	},
	"shadow_mail": {
		"id": "shadow_mail",
		"name": "Shadow Mail",
		"ingredients": {"umbral_thread": 4, "chainmail_shirt": 1, "void_heart_fragment": 1},
		"result": ("shadow_mail", 1),
		"station": "altar_shadow",
		"description": "Armor woven from solidified shadows.",
		"auto_discover": True,
	},

	# ═══════════════════════════════════════════════════════════════════
	# IRON ALTAR RECIPES - Dwarven Epic/Legendary Equipment
	# ═══════════════════════════════════════════════════════════════════

	"runeforged_blade": {
		"id": "runeforged_blade",
		"name": "Runeforged Blade",
		"ingredients": {"raw_mithril": 1, "tempered_steel_ingot": 2, "eternal_ember": 1},
		"result": ("runeforged_blade", 1),
		"station": "altar_iron",
		"description": "A blade inscribed with dwarven power runes.",
		"auto_discover": True,
	},
	"forgemaster_helm": {
		"id": "forgemaster_helm",
		"name": "Forgemaster Helm",
		"ingredients": {"tempered_steel_ingot": 2, "eternal_ember": 1, "steel_greathelm": 1},
		"result": ("forgemaster_helm", 1),
		"station": "altar_iron",
		"description": "A helm forged in the eternal flames.",
		"auto_discover": True,
	},
	"ironbound_boots": {
		"id": "ironbound_boots",
		"name": "Ironbound Boots",
		"ingredients": {"tempered_steel_ingot": 2, "mithril_dust": 1, "iron_sabatons": 1},
		"result": ("ironbound_boots", 1),
		"station": "altar_iron",
		"description": "Boots reinforced with ancient dwarven alloy.",
		"auto_discover": True,
	},
	"steamfist_gauntlets": {
		"id": "steamfist_gauntlets",
		"name": "Steamfist Gauntlets",
		"ingredients": {"eternal_ember": 1, "iron_gauntlets": 1, "clockwork_gear": 2},
		"result": ("steamfist_gauntlets", 1),
		"station": "altar_iron",
		"description": "Steam-powered gauntlets that enhance punch force.",
		"auto_discover": True,
	},
	"adamantine_shield": {
		"id": "adamantine_shield",
		"name": "Adamantine Shield",
		"ingredients": {"raw_mithril": 1, "tempered_steel_ingot": 2, "iron_kite_shield": 1},
		"result": ("adamantine_shield", 1),
		"station": "altar_iron",
		"description": "A shield of the hardest known metal.",
		"auto_discover": True,
	},
	"runeplate_armor": {
		"id": "runeplate_armor",
		"name": "Runeplate Armor",
		"ingredients": {"tempered_steel_ingot": 3, "mithril_dust": 2, "iron_plate": 1, "eternal_ember": 1},
		"result": ("runeplate_armor", 1),
		"station": "altar_iron",
		"description": "Masterwork dwarven plate etched with protective runes.",
		"auto_discover": True,
	},

	# ═══════════════════════════════════════════════════════════════════
	# CATACOMB ALTAR RECIPES - Undead-themed Epic/Legendary Equipment
	# ═══════════════════════════════════════════════════════════════════

	"bonereaper_scythe": {
		"id": "bonereaper_scythe",
		"name": "Bonereaper Scythe",
		"ingredients": {"bone_fragments": 5, "soul_gem": 2, "cracked_phylactery": 1},
		"result": ("bonereaper_scythe", 1),
		"station": "altar_catacomb",
		"description": "A scythe that harvests souls.",
		"auto_discover": True,
	},
	"grave_warden_helm": {
		"id": "grave_warden_helm",
		"name": "Grave Warden Helm",
		"ingredients": {"bone_fragments": 3, "soul_gem": 1, "iron_helm": 1},
		"result": ("grave_warden_helm", 1),
		"station": "altar_catacomb",
		"description": "A skull-like helm of bound spirits.",
		"auto_discover": True,
	},
	"soulbound_boots": {
		"id": "soulbound_boots",
		"name": "Soulbound Boots",
		"ingredients": {"soul_gem": 2, "leather_boots": 1, "umbral_thread": 1},
		"result": ("soulbound_boots", 1),
		"station": "altar_catacomb",
		"description": "Boots empowered by trapped souls.",
		"auto_discover": True,
	},
	"phylactery_gauntlets": {
		"id": "phylactery_gauntlets",
		"name": "Phylactery Gauntlets",
		"ingredients": {"cracked_phylactery": 2, "iron_gauntlets": 1, "blood_ruby": 1},
		"result": ("phylactery_gauntlets", 1),
		"station": "altar_catacomb",
		"description": "Gauntlets that drain life force from foes.",
		"auto_discover": True,
	},
	"deathshroud_armor": {
		"id": "deathshroud_armor",
		"name": "Deathshroud Armor",
		"ingredients": {"umbral_thread": 3, "soul_gem": 3, "chainmail_shirt": 1},
		"result": ("deathshroud_armor", 1),
		"station": "altar_catacomb",
		"description": "Armor wreathed in deathly energy.",
		"auto_discover": True,
	},
	"necromancer_ring": {
		"id": "necromancer_ring",
		"name": "Necromancer Ring",
		"ingredients": {"soul_gem": 1, "blood_ruby": 1, "silver_ring": 1},
		"result": ("necromancer_ring", 1),
		"station": "altar_catacomb",
		"description": "A ring that commands the restless dead.",
		"auto_discover": True,
	},

	# ═══════════════════════════════════════════════════════════════════
	# MYTHIC CRAFTING - Requires Multiple Boss Materials
	# ═══════════════════════════════════════════════════════════════════

	"titans_grasp": {
		"id": "titans_grasp",
		"name": "Titan's Grasp",
		"ingredients": {"titans_heart": 1, "forgemaster_heart": 1, "raw_mithril": 2, "eternal_ember": 2},
		"result": ("titans_grasp", 1),
		"station": "altar_iron",
		"description": "Gauntlets forged from two titans' essence. Grants immense strength.",
		"auto_discover": True,
	},
	"eclipse_blade": {
		"id": "eclipse_blade",
		"name": "Eclipse Blade",
		"ingredients": {"titans_heart": 1, "sovereign_shadow_crown": 1, "prismatic_blade": 1, "shadow_blade": 1},
		"result": ("eclipse_blade", 1),
		"station": "altar_shadow",
		"description": "A blade of light and shadow in perfect balance.",
		"auto_discover": True,
	},
	"crown_of_dominion": {
		"id": "crown_of_dominion",
		"name": "Crown of Dominion",
		"ingredients": {"lich_crown_fragment": 1, "sovereign_shadow_crown": 1, "frost_sovereign_crystal": 1, "blood_ruby": 3},
		"result": ("crown_of_dominion", 1),
		"station": "altar_catacomb",
		"description": "A crown that commands all who behold it.",
		"auto_discover": True,
	},
	"worldshaper_armor": {
		"id": "worldshaper_armor",
		"name": "Worldshaper Armor",
		"ingredients": {"forgemaster_heart": 1, "verdant_guardian_seed": 1, "dwarven_masterwork": 1, "raw_mithril": 3},
		"result": ("worldshaper_armor", 1),
		"station": "altar_iron",
		"description": "Armor infused with the power to reshape reality.",
		"auto_discover": True,
	},
	"boots_of_the_void": {
		"id": "boots_of_the_void",
		"name": "Boots of the Void",
		"ingredients": {"void_heart_fragment": 2, "sovereign_shadow_crown": 1, "shadowstep_boots": 1},
		"result": ("boots_of_the_void", 1),
		"station": "altar_shadow",
		"description": "Boots that step between dimensions.",
		"auto_discover": True,
	},
}

# =====================================================================
# FISH COOKING RECIPES (loaded dynamically from fishing_system)
# =====================================================================
try:
	from fishing_system import FISH_COOKING_RECIPES
	RECIPE_DATABASE.update(FISH_COOKING_RECIPES)
except ImportError:
	pass

# Item worth for crafted items (that don't already exist in the item_worth table)
CRAFTED_ITEM_WORTH = {
	# Original forge items
	"steel_dagger": 35,
	"iron_sword": 30,
	"steel_longsword": 110,
	"leather_armor_piece": 25,
	"masterwork_shield": 125,
	"refined_iron": 40,
	"healing_potion": 85,
	"antidote": 45,
	"poison_cure": 50,
	"holy_water": 55,
	"quality_torch": 15,
	"crystal_shield": 220,
	"enchanted_ring": 120,
	"prismatic_blade": 350,
	"shadow_blade": 280,
	"void_amulet": 250,
	"sovereign_cloak": 400,
	"mithril_blade": 320,
	"dwarven_masterwork": 380,
	"soul_blade": 300,
	"lich_crown": 350,

	# New Forge Weapons
	"bronze_sword": 20,
	"iron_axe": 45,
	"steel_mace": 90,
	"hunters_bow": 55,
	"silver_rapier": 130,

	# New Forge Armor
	"padded_vest": 15,
	"chainmail_shirt": 85,
	"iron_plate": 150,

	# New Forge Helms
	"leather_cap": 18,
	"iron_helm": 50,
	"steel_greathelm": 120,

	# New Forge Boots
	"leather_boots": 22,
	"iron_sabatons": 55,
	"steel_greaves": 100,

	# New Forge Gloves
	"cloth_gloves": 8,
	"leather_gloves": 25,
	"iron_gauntlets": 60,

	# New Forge Shields
	"wooden_buckler": 12,
	"iron_kite_shield": 70,
	"steel_tower_shield": 140,

	# New Forge Accessories
	"copper_ring": 25,
	"silver_ring": 65,
	"bone_amulet": 35,

	# Crystal Altar Equipment
	"crystal_blade": 280,
	"radiant_helm": 240,
	"prismatic_boots": 220,
	"crystalweave_gloves": 180,
	"lightweaver_robes": 260,

	# Shadow Altar Equipment
	"nightblade": 260,
	"shadowstep_boots": 200,
	"hood_of_whispers": 190,
	"void_touched_gauntlets": 210,
	"shadow_mail": 240,

	# Iron Altar Equipment
	"runeforged_blade": 300,
	"forgemaster_helm": 270,
	"ironbound_boots": 230,
	"steamfist_gauntlets": 220,
	"adamantine_shield": 280,
	"runeplate_armor": 350,

	# Catacomb Altar Equipment
	"bonereaper_scythe": 290,
	"grave_warden_helm": 200,
	"soulbound_boots": 180,
	"phylactery_gauntlets": 210,
	"deathshroud_armor": 260,
	"necromancer_ring": 220,

	# Mythic Crafted Items
	"titans_grasp": 800,
	"eclipse_blade": 950,
	"crown_of_dominion": 900,
	"worldshaper_armor": 1000,
	"boots_of_the_void": 750,

	# Cooked food
	"cooked_fish": 10,
	"grilled_trout": 18,
	"grilled_perch": 15,
	"hearty_fish_stew": 40,
	"eel_skewer": 25,
	"fried_catfish": 22,
	"golden_sashimi": 80,
	"pike_feast": 60,
	"ethereal_broth": 55,
	"legendary_feast": 200,
	"rainbow_sushi": 180,
}


class CraftingSystem:
	"""Handles station-based crafting with discoverable recipes."""

	def __init__(self, engine):
		self.engine = engine

	def get_known_recipes(self):
		"""Get list of recipe IDs the player knows."""
		return self.engine.player.state.get("known_recipes", [])

	def learn_recipe(self, recipe_id):
		"""
		Teach the player a recipe. Returns a message string.
		"""
		if recipe_id not in RECIPE_DATABASE:
			return None

		known = self.engine.player.state.get("known_recipes", [])
		if recipe_id in known:
			return None  # Already known, no message

		known.append(recipe_id)
		self.engine.player.state["known_recipes"] = known

		recipe = RECIPE_DATABASE[recipe_id]
		return f"  📜 New recipe learned: {recipe['name']}!"

	def get_current_station_type(self):
		"""
		Determine what crafting station (if any) is in the current room.
		Returns station type string or None.
		"""
		room_id = self.engine.player.current_room

		# Check Room object's crafting_station property (world rooms)
		room_obj = self.engine.get_room_data(room_id)
		if room_obj and hasattr(room_obj, 'crafting_station') and room_obj.crafting_station:
			return room_obj.crafting_station

		# Check village blacksmith (fallback)
		if room_id == "village_blacksmith":
			return "forge"

		# Check dungeon altar rooms
		raw_room = self._get_raw_room(room_id)
		if raw_room and raw_room.get("crafting_altar"):
			# Determine altar type from dungeon context
			if self.engine.current_fixed_dungeon:
				dungeon_id = self.engine.current_fixed_dungeon.get("dungeon_id", "")
				if dungeon_id == "crystal_caverns":
					return "altar_crystal"
				elif dungeon_id == "shadow_depths":
					return "altar_shadow"
				elif dungeon_id == "iron_halls":
					return "altar_iron"
				elif dungeon_id == "sunken_catacombs":
					return "altar_catacomb"
			# Fallback: check room ID prefix
			if room_id.startswith("cc_"):
				return "altar_crystal"
			elif room_id.startswith("sd_"):
				return "altar_shadow"
			elif room_id.startswith("ih_"):
				return "altar_iron"
			elif room_id.startswith("sc_"):
				return "altar_catacomb"

		return None

	def get_available_recipes(self, station_type):
		"""
		Get recipes the player knows that can be crafted at this station.
		Returns list of (recipe_id, recipe_data, can_craft_bool) tuples.
		"""
		known = self.get_known_recipes()
		available = []

		for rid in known:
			recipe = RECIPE_DATABASE.get(rid)
			if not recipe:
				continue
			# Check station compatibility
			req_station = recipe["station"]
			if req_station == "any" or req_station == station_type:
				can_craft = self._has_ingredients(recipe)
				available.append((rid, recipe, can_craft))

		return available

	def _has_ingredients(self, recipe):
		"""Check if player has all ingredients for a recipe."""
		inv = self.engine.player.inventory
		for item, count in recipe["ingredients"].items():
			if inv.get(item, 0) < count:
				return False
		return True

	def craft_recipe(self, recipe_id):
		"""
		Attempt to craft a recipe. Consumes ingredients, produces result.
		Returns result message string.
		"""
		recipe = RECIPE_DATABASE.get(recipe_id)
		if not recipe:
			return "Unknown recipe."

		# Verify station
		station = self.get_current_station_type()
		req = recipe["station"]
		if req != "any" and req != station:
			station_name = STATION_NAMES.get(req, req)
			return f"This recipe requires: {station_name}"

		# Verify ingredients
		inv = self.engine.player.inventory
		missing = []
		for item, count in recipe["ingredients"].items():
			have = inv.get(item, 0)
			if have < count:
				nice = item.replace("_", " ")
				missing.append(f"  {nice}: need {count}, have {have}")

		if missing:
			result = f"Not enough materials for {recipe['name']}:\n"
			result += "\n".join(missing)
			return result

		# Consume ingredients
		for item, count in recipe["ingredients"].items():
			if inv[item] > count:
				inv[item] -= count
			else:
				inv.pop(item, None)

		# Produce result
		result_item, result_count = recipe["result"]
		inv[result_item] = inv.get(result_item, 0) + result_count
		self.engine._inventory_changed = True

		# Trigger ASCII animation overlay
		gui = getattr(self.engine, "gui", None)
		if gui is not None:
			station_type = recipe.get("station", "any")
			if station_type == "campfire" or ("campfire" in str(recipe.get("name","")).lower()):
				gui._crafting_overlay = CookingOverlay(recipe["name"], result_item, gui=gui)
			else:
				gui._crafting_overlay = CraftingOverlay(recipe["name"], result_item, station_type)

		# Register item worth if not already known
		if result_item not in self.engine.item_worth:
			self.engine.item_worth[result_item] = CRAFTED_ITEM_WORTH.get(result_item, 50)

		nice_name = result_item.replace("_", " ")
		result_text = "\n" + "═" * 50 + "\n"
		result_text += f"  ⚒️  CRAFTED: {recipe['name']}\n"
		result_text += "═" * 50 + "\n\n"
		result_text += f"  {recipe['description']}\n\n"
		result_text += f"  +{result_count} {nice_name} added to inventory.\n"
		result_text += "═" * 50 + "\n"

		# Award XP for crafting (tiered by station type)
		if PROGRESSION_AVAILABLE:
			try:
				station_type = recipe.get("station", "any")
				if station_type.startswith("altar_"):
					# Altar recipes are legendary
					xp_key = "craft_legendary"
				elif station_type == "forge":
					# Forge recipes are advanced
					xp_key = "craft_advanced"
				else:
					xp_key = "craft_basic"
				result_text += award_xp(self.engine.player, XP_AWARDS.get(xp_key, 10), "crafted item")
			except Exception:
				pass

		return result_text

	def use_station(self, choice=None):
		"""
		Main entry point when player uses 'craft' command at a station.
		If choice is None, shows the recipe menu.
		If choice is a number, attempts to craft that recipe.
		"""
		station = self.get_current_station_type()
		if not station:
			return "There is no crafting altar or station here.\nYou can craft at the Blacksmith's Forge or at dungeon altars."

		station_name = STATION_NAMES.get(station, "Crafting Station")

		# Track discovered dungeon altars
		if station.startswith("altar_"):
			found = set(self.engine.player.state.get("found_altars", []))
			found.add(station_name)
			self.engine.player.state["found_altars"] = list(found)

		# Crystal Caverns altar is placeholder content for now
		if station == "altar_crystal":
			result = "\n" + "═" * 50 + "\n"
			result += f"  ⚒️  {station_name}\n"
			result += "═" * 50 + "\n\n"
			result += "  The Forge of Light hums softly, but its power\n"
			result += "  is not yet fully understood.\n\n"
			result += "  Crafting here is coming soon.\n"
			result += "  Check back after the forge is awakened.\n"
			result += "═" * 50 + "\n"
			return result

		# Auto-discover altar recipes when first visiting
		self._auto_discover_recipes(station)

		# Get available recipes
		recipes = self.get_available_recipes(station)

		if not recipes:
			result = "\n" + "═" * 50 + "\n"
			result += f"  ⚒️  {station_name}\n"
			result += "═" * 50 + "\n\n"
			result += "  You don't know any recipes for this station yet.\n"
			result += "  Talk to NPCs to learn crafting recipes!\n\n"
			result += "  Hint: The blacksmith, hermit, priest, and\n"
			result += "  swamp witch all know useful recipes.\n"
			result += "═" * 50 + "\n"
			return result

		if choice is not None:
			# Craft specific recipe
			try:
				idx = int(choice) - 1
				if 0 <= idx < len(recipes):
					recipe_id = recipes[idx][0]
					return self.craft_recipe(recipe_id)
				else:
					return "Invalid recipe number."
			except ValueError:
				return "Please enter a recipe number."

		# Show recipe menu — store pending state
		result = "\n" + "═" * 50 + "\n"
		result += f"  ⚒️  {station_name}\n"
		result += "═" * 50 + "\n\n"
		result += "  Available recipes:\n\n"

		for i, (rid, recipe, can_craft) in enumerate(recipes, 1):
			status = "✅" if can_craft else "❌"
			result += f"  {i}. {status} {recipe['name']}\n"
			# Show ingredients
			for item, count in recipe["ingredients"].items():
				have = self.engine.player.inventory.get(item, 0)
				nice = item.replace("_", " ")
				indicator = "✓" if have >= count else "✗"
				result += f"       {indicator} {nice}: {have}/{count}\n"
			result += f"       → {recipe['description']}\n\n"

		result += "  Enter a number to craft, or anything else to cancel.\n"
		result += "═" * 50 + "\n"

		# Set pending crafting state
		self.engine.pending_crafting = {
			"station": station,
			"recipes": [(rid, r["name"]) for rid, r, _ in recipes],
		}

		return result

	def handle_crafting_choice(self, cmd):
		"""Handle player's response to crafting menu."""
		pending = self.engine.pending_crafting
		if not pending:
			return None

		self.engine.pending_crafting = None

		cmd = cmd.strip().lower()
		if cmd in ("cancel", "no", "back", "quit", "exit"):
			return "You step back from the crafting station."

		try:
			idx = int(cmd) - 1
			recipes = pending["recipes"]
			if 0 <= idx < len(recipes):
				recipe_id = recipes[idx][0]
				return self.craft_recipe(recipe_id)
			else:
				return "Invalid choice. Crafting cancelled."
		except ValueError:
			return "Crafting cancelled."

	def _auto_discover_recipes(self, station_type):
		"""Auto-discover recipes marked for this station type."""
		learned_any = False
		for rid, recipe in RECIPE_DATABASE.items():
			if recipe.get("auto_discover") and recipe["station"] == station_type:
				msg = self.learn_recipe(rid)
				if msg:
					learned_any = True
					# We'll show the discovery as part of the station display
		return learned_any

	def _get_raw_room(self, room_id):
		"""Get raw room data from dungeon."""
		if self.engine.current_dungeon_instance:
			try:
				from trap_system import TrapSystem
				raw = TrapSystem.find_raw_room(self.engine.current_dungeon_instance, room_id)
				if raw:
					return raw
			except Exception:
				pass
		if self.engine.current_fixed_dungeon:
			for _fnum, fdata in self.engine.current_fixed_dungeon.get("floors", {}).items():
				if room_id in fdata.get("rooms", {}):
					return fdata["rooms"][room_id]
		return None

	# ═══════════════════════════════════════════════════════════════
	# CRAFTING EXPERIMENTATION / DISCOVERY
	# ═══════════════════════════════════════════════════════════════

	def start_experiment(self):
		"""Begin an experimentation session at a crafting station.
		Player selects items from inventory to combine."""
		station = self.get_current_station_type()
		if not station:
			return "There is no crafting station here to experiment at."

		station_name = STATION_NAMES.get(station, "Crafting Station")
		inv = self.engine.player.inventory

		# Get items that could be ingredients
		available_items = []
		for item_id, count in sorted(inv.items()):
			if count > 0:
				available_items.append((item_id, count))

		if len(available_items) < 1:
			return "You don't have any items to experiment with."

		result = "\n" + "═" * 55 + "\n"
		result += f"  🧪 EXPERIMENTATION — {station_name}\n"
		result += "═" * 55 + "\n\n"
		result += "  Select items to combine (2-4 items).\n"
		result += "  Enter item numbers separated by spaces.\n"
		result += "  ⚠️ Failed experiments consume ingredients!\n\n"

		for i, (item_id, count) in enumerate(available_items, 1):
			nice = item_id.replace("_", " ")
			result += f"  {i:>3}. {nice} (x{count})\n"

		result += "\n  Example: '1 3' to combine items 1 and 3\n"
		result += "  Type 'cancel' to stop experimenting.\n"
		result += "═" * 55 + "\n"

		# Store pending experiment state
		self.engine.pending_experiment = {
			"station": station,
			"items": available_items,
		}

		return result

	def handle_experiment_choice(self, cmd):
		"""Handle the player's item selection for experimentation."""
		import random as _rng

		pending = self.engine.pending_experiment
		if not pending:
			return None

		self.engine.pending_experiment = None

		cmd = cmd.strip().lower()
		if cmd in ("cancel", "no", "back", "quit", "exit"):
			return "You step back from the station."

		# Parse item indices
		try:
			indices = [int(x) - 1 for x in cmd.split()]
		except ValueError:
			return "Invalid input. Enter numbers separated by spaces, or 'cancel'."

		available = pending["items"]
		station = pending["station"]

		if len(indices) < 2 or len(indices) > 4:
			return "Combine 2-4 items. Try again with 'experiment'."

		# Validate indices
		selected_items = {}
		for idx in indices:
			if idx < 0 or idx >= len(available):
				return f"Invalid item number: {idx + 1}. Try again."
			item_id, max_count = available[idx]
			selected_items[item_id] = selected_items.get(item_id, 0) + 1
			if selected_items[item_id] > max_count:
				nice = item_id.replace("_", " ")
				return f"You don't have enough {nice}."

		# Check if this combination matches any recipe at this station
		known = self.get_known_recipes()
		match_recipe = None
		for rid, recipe in RECIPE_DATABASE.items():
			if rid in known:
				continue  # Already known
			req_station = recipe["station"]
			if req_station != "any" and req_station != station:
				continue
			# Check ingredients match exactly
			if recipe["ingredients"] == selected_items:
				match_recipe = (rid, recipe)
				break

		if match_recipe:
			rid, recipe = match_recipe
			# SUCCESS! Learn and craft
			self.learn_recipe(rid)

			# Consume ingredients
			inv = self.engine.player.inventory
			for item_id, count in selected_items.items():
				inv[item_id] = inv.get(item_id, 0) - count
				if inv[item_id] <= 0:
					del inv[item_id]

			# Produce result
			result_item, result_count = recipe["result"]
			inv[result_item] = inv.get(result_item, 0) + result_count
			self.engine._inventory_changed = True

			if result_item not in self.engine.item_worth:
				self.engine.item_worth[result_item] = CRAFTED_ITEM_WORTH.get(result_item, 50)

			result = "\n" + "═" * 55 + "\n"
			result += "  🧪✨ DISCOVERY!\n"
			result += "═" * 55 + "\n\n"
			result += f"  You discovered how to make: {recipe['name']}!\n"
			result += f"  {recipe['description']}\n\n"
			nice = result_item.replace("_", " ")
			result += f"  +{result_count} {nice} added to inventory.\n"
			result += f"  📜 Recipe permanently learned!\n\n"

			# XP for discovery
			if PROGRESSION_AVAILABLE:
				try:
					xp_msg = award_xp(self.engine.player, XP_AWARDS.get("discover_recipe", 25), "recipe discovery")
					if xp_msg:
						result += xp_msg + "\n"
				except Exception:
					pass

			result += "═" * 55 + "\n"
			return result
		else:
			# FAILURE — consume ingredients with partial recovery chance
			inv = self.engine.player.inventory
			recovered = []
			for item_id, count in selected_items.items():
				inv[item_id] = inv.get(item_id, 0) - count
				if inv[item_id] <= 0:
					del inv[item_id]
				# 30% chance to recover each ingredient
				for _ in range(count):
					if _rng.random() < 0.30:
						inv[item_id] = inv.get(item_id, 0) + 1
						recovered.append(item_id)

			self.engine._inventory_changed = True

			result = "\n" + "═" * 55 + "\n"
			result += "  🧪💨 EXPERIMENT FAILED\n"
			result += "═" * 55 + "\n\n"
			result += "  The materials fizz and sputter... nothing useful forms.\n"

			items_text = ", ".join(item.replace("_", " ") for item in selected_items)
			result += f"  Lost: {items_text}\n"

			if recovered:
				rec_text = ", ".join(r.replace("_", " ") for r in recovered)
				result += f"  Salvaged: {rec_text}\n"

			# Hint system — check if any recipe partially matches
			hint = self._get_experiment_hint(selected_items, station)
			if hint:
				result += f"\n  💡 {hint}\n"

			result += "\n═" * 55 + "\n"
			return result

	def _get_experiment_hint(self, selected_items, station):
		"""Provide a hint if the selection is close to a real recipe."""
		known = self.get_known_recipes()
		best_match = 0
		best_recipe = None

		for rid, recipe in RECIPE_DATABASE.items():
			if rid in known:
				continue
			req_station = recipe["station"]
			if req_station != "any" and req_station != station:
				continue

			# Count matching ingredients
			match_count = 0
			for item in selected_items:
				if item in recipe["ingredients"]:
					match_count += 1

			total_needed = len(recipe["ingredients"])
			if match_count > best_match and match_count >= 1:
				best_match = match_count
				best_recipe = recipe

		if best_recipe and best_match >= 1:
			total = len(best_recipe["ingredients"])
			if best_match == total - 1:
				# Very close — give a strong hint
				missing = [item for item in best_recipe["ingredients"] if item not in selected_items]
				if missing:
					nice = missing[0].replace("_", " ")
					return f"You feel like you're close... maybe try adding {nice}?"
			elif best_match >= 1:
				return "Some of these materials resonated briefly. You might be on to something..."

		return None


# ──────────────────────────────────────────────────────────────────────────────
#  CRAFTING OVERLAY — auto-play sparkle animation (no interaction)
# ──────────────────────────────────────────────────────────────────────────────

class CraftingOverlay:
    """
    Purely visual overlay shown after a successful craft.
    Plays the appropriate station animation for ~2 seconds then auto-dismisses.
    """
    DURATION = 2.2

    def __init__(self, recipe_name: str, result_item: str, station_type: str = "any"):
        self.recipe_name = recipe_name
        self.result_item = result_item
        self.station_type = station_type
        self.done = False
        self._t = 0.0
        self._frame = 0
        self._frame_t = 0.0
        self._font = None

        _anim_map = {
            "forge":          "forging_hammer",
            "altar_crystal":  "ritual_circle",
            "altar_shadow":   "ritual_circle",
            "altar_iron":     "forging_hammer",
            "altar_catacomb": "ritual_circle",
        }
        self._anim_key = _anim_map.get(station_type, "forging_hammer")

    def handle_event(self, event):
        import pygame
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.done = True

    def update(self, dt):
        self._t += dt
        self._frame_t += dt
        if self._frame_t >= 0.18:
            self._frame_t = 0.0
            self._frame += 1
        if self._t >= self.DURATION:
            self.done = True

    def render(self, surface):
        try:
            import pygame
            from ascii_art import (ANIMATION_FRAMES, render_ascii_block,
                                   draw_dim_overlay, draw_panel, render_label, _ensure_fonts)
            _ensure_fonts()
        except ImportError:
            return
        if self._font is None:
			from font_support import load_font, wrap_font_with_symbol_fallback

			self._font = wrap_font_with_symbol_fallback(
				load_font({}, 14, mono=True)
			)
        sw, sh = surface.get_size()
        pw, ph = 440, 320
        px = (sw - pw) // 2
        py = (sh - ph) // 2
        draw_dim_overlay(surface, 140)
        draw_panel(surface, (px, py, pw, ph), title="CRAFTING")
        frames = ANIMATION_FRAMES.get(self._anim_key, [[]])
        frame = frames[self._frame % max(len(frames), 1)]
        render_ascii_block(surface, frame, px + pw // 2 - 80, py + 60, color=(180, 200, 255))
        nice = self.result_item.replace("_", " ").title()
        render_label(surface, f"Crafted: {nice}", px + pw // 2, py + ph - 80,
                     color=(255, 220, 80))
        render_label(surface, "[SPACE] to skip", px + pw // 2, py + ph - 50,
                     color=(100, 100, 130), small=True)


# ──────────────────────────────────────────────────────────────────────────────
#  COOKING OVERLAY — campfire timing bar minigame
# ──────────────────────────────────────────────────────────────────────────────

class CookingOverlay:
    """
    Campfire cooking overlay — hold SPACE to push heat right, release to drift left.
    Build cook progress while inside moving cooking zones before timer runs out.
    """
    DURATION       = 15.0
    HEAT_RATE      = 0.18
    ZONE_WIDTH     = 0.22
    PERFECT_WIDTH  = 0.08

    def __init__(self, recipe_name: str, result_item: str, gui=None):
        self.recipe_name = recipe_name
        self.result_item = result_item
        self._gui        = gui
        self.done        = False
        self._t          = 0.0
        self._heat       = 0.0
        self._fired      = False
        self._fire_result = ""
        self._result_t   = 0.0
        self._frame      = 0
        self._frame_t    = 0.0
        self._font       = None
        self._space_held = False
        self._progress   = 0.0  # 0.0..1.0
        self._required_progress = 1.0
        self._perfect_gain = 0.24
        self._near_gain    = 0.04
        self._outside_loss = 0.78

        # Moving zone state (random target + random motion speed)
        self._rng = __import__("random")
        self._zone_center = self._rng.uniform(0.44, 0.60)
        self._zone_target = self._zone_center
        self._zone_shift_timer = 0.0
        self._zone_shift_every = 1.0
        self._zone_move_speed = 0.5
        self._zone_shift_min = 0.35
        self._zone_shift_max = 1.10
        self._zone_speed_min = 0.55
        self._zone_speed_max = 1.40

        # Runtime zone bounds (near + perfect)
        self._zone_start = 0.40
        self._zone_end = 0.68
        self._perfect_start = 0.48
        self._perfect_end = 0.60
        self._result_logged = False

        # Difficulty scaling (cooking has no ingredient tiers, use tier 1)
        try:
            from ascii_art import get_diff_params
            dp = get_diff_params(1)
        except Exception:
            dp = {"heat_rate_mult":1.0,"zone_mult":1.0,"result_secs":0.0,"timer_mult":1.0}

        self._heat_rate = self.HEAT_RATE * dp.get("heat_rate_mult", 1.0)
        self._duration = max(8.0, self.DURATION * dp.get("timer_mult", 1.0))
        self._zone_width = max(0.14, self.ZONE_WIDTH * dp["zone_mult"])
        self._perfect_width = max(0.06, self.PERFECT_WIDTH * dp["zone_mult"])
        self._result_secs = 3.0 + max(0.0, dp["result_secs"])

        self._roll_zone_motion()
        self._zone_shift_timer = self._zone_shift_every
        self._update_zones()

    def handle_event(self, event):
        import pygame
        if self.done or self._fired:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._space_held = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self._space_held = False

    def _resolve_result(self):
        self._fired = True
        if self._progress >= self._required_progress:
            self._fire_result = "perfect"
        elif self._progress >= 0.55:
            self._fire_result = "normal"
        else:
            self._fire_result = "normal"

        if self._gui is not None and not self._result_logged:
            progress_pct = int(100 * min(1.0, self._progress / max(self._required_progress, 0.001)))
            if self._fire_result == "perfect":
                self._gui.append(
                    f"  ✨ Cooking minigame success: {self.recipe_name}. Perfect cook at {progress_pct}% progress."
                )
            else:
                self._gui.append(
                    f"  ❌ Cooking minigame failed: {self.recipe_name}. Only {progress_pct}% progress; no perfect cook bonus."
                )
            self._result_logged = True

    def _update_zones(self):
        half_near = self._zone_width * 0.5
        min_center = 0.10 + half_near
        max_center = 0.90 - half_near
        self._zone_center = max(min_center, min(max_center, self._zone_center))

        self._zone_start = self._zone_center - half_near
        self._zone_end = self._zone_center + half_near

        half_perf = min(self._perfect_width * 0.5, half_near - 0.015)
        self._perfect_start = self._zone_center - half_perf
        self._perfect_end = self._zone_center + half_perf

    def _pick_new_zone_target(self):
        half_near = self._zone_width * 0.5
        min_center = 0.10 + half_near
        max_center = 0.90 - half_near
        prev = self._zone_target
        for _ in range(6):
            candidate = self._rng.uniform(min_center, max_center)
            if abs(candidate - prev) >= 0.06:
                self._zone_target = candidate
                return
        self._zone_target = self._rng.uniform(min_center, max_center)

    def _roll_zone_motion(self):
        self._zone_shift_every = self._rng.uniform(self._zone_shift_min, self._zone_shift_max)
        self._zone_move_speed = self._rng.uniform(self._zone_speed_min, self._zone_speed_max)

    def update(self, dt):
        if self.done:
            return
        self._t += dt
        self._frame_t += dt
        if self._frame_t >= 0.22:
            self._frame_t = 0.0
            self._frame  += 1

        if not self._fired:
            # Move near/perfect zones with random pace and target.
            self._zone_shift_timer -= dt
            if self._zone_shift_timer <= 0:
                self._roll_zone_motion()
                self._zone_shift_timer = self._zone_shift_every
                self._pick_new_zone_target()

            delta = self._zone_target - self._zone_center
            step = min(1.0, self._zone_move_speed * dt)
            self._zone_center += delta * step
            self._update_zones()

            # Hold/release control like alchemy: hold raises heat, release lowers it.
            if self._space_held:
                self._heat = min(1.0, self._heat + self._heat_rate * 1.95 * dt)
            else:
                self._heat = max(0.0, self._heat - self._heat_rate * 1.45 * dt)

            # Perfect zone gives strong progress, near zone gives much less.
            if self._perfect_start <= self._heat <= self._perfect_end:
                self._progress = min(self._required_progress, self._progress + self._perfect_gain * dt)
            elif self._zone_start <= self._heat <= self._zone_end:
                self._progress = min(self._required_progress, self._progress + self._near_gain * dt)
            else:
                self._progress = max(0.0, self._progress - self._outside_loss * dt)

            # Early completion if player fully stabilizes cooking.
            if self._progress >= self._required_progress:
                self._resolve_result()

            # Timeout fallback.
            if self._t >= self._duration and not self._fired:
                self._resolve_result()
        else:
            self._result_t += dt
            if self._result_t >= self._result_secs:
                self.done = True

    def render(self, surface):
        try:
            import pygame
            from ascii_art import (ANIMATION_FRAMES, render_ascii_block,
                                   draw_dim_overlay, draw_panel, render_label, _ensure_fonts)
            _ensure_fonts()
        except ImportError:
            return
        if self._font is None:
			from font_support import load_font, wrap_font_with_symbol_fallback

			self._font = wrap_font_with_symbol_fallback(
				load_font({}, 14, mono=True)
			)
        sw, sh = surface.get_size()
        pw, ph = 460, 340
        px = (sw - pw) // 2
        py = (sh - ph) // 2
        draw_dim_overlay(surface, 150)
        draw_panel(surface, (px, py, pw, ph), title="COOKING")
        # Countdown timer bar (time remaining until bar auto-fires)
        if not self._fired:
            try:
                from ascii_art import draw_timer_bar
                draw_timer_bar(surface, px, py, pw,
                               max(0.0, self._duration - self._t), self._duration)
            except Exception:
                pass
        # Animation
        frames = ANIMATION_FRAMES.get("campfire_cook", [[]])
        frame  = frames[self._frame % max(len(frames), 1)]
        render_ascii_block(surface, frame, px + pw // 2 - 70, py + 55,
                           color=(255, 160, 60))
        # Timing bar
        bar_x = px + 60
        bar_y = py + 186
        bar_w = pw - 120
        bar_h = 28
        pygame.draw.rect(surface, (40, 20, 10),  (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        zx = bar_x + int(self._zone_start * bar_w)
        zw = int((self._zone_end - self._zone_start) * bar_w)
        pygame.draw.rect(surface, (62, 122, 70), (zx, bar_y, zw, bar_h), border_radius=4)

        # Perfect sub-zone (brighter center)
        px2 = bar_x + int(self._perfect_start * bar_w)
        pw2 = int((self._perfect_end - self._perfect_start) * bar_w)
        pygame.draw.rect(surface, (110, 210, 120), (px2, bar_y + 3, pw2, bar_h - 6), border_radius=4)

        ind_x = bar_x + int(self._heat * bar_w) - 3
        pygame.draw.rect(surface, (255, 255, 200), (ind_x, bar_y - 4, 6, bar_h + 8), border_radius=3)
        pygame.draw.rect(surface, (100, 60, 20), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)

        # Progress bar (percentage)
        prog_x = bar_x
        prog_y = bar_y + 40
        prog_w = bar_w
        prog_h = 14
        pygame.draw.rect(surface, (28, 40, 24), (prog_x, prog_y, prog_w, prog_h), border_radius=3)
        fill_w = int(prog_w * min(1.0, self._progress / max(self._required_progress, 0.001)))
        if fill_w > 0:
            pygame.draw.rect(surface, (80, 200, 110), (prog_x, prog_y, fill_w, prog_h), border_radius=3)
        pygame.draw.rect(surface, (80, 110, 70), (prog_x, prog_y, prog_w, prog_h), 1, border_radius=3)

        text_y = py + ph - 74
        render_label(surface, f'Cooking: {self.recipe_name}',
                     px + pw // 2, text_y, color=(220, 180, 80))
        if not self._fired:
            progress_pct = int(100 * min(1.0, self._progress / max(self._required_progress, 0.001)))
            render_label(surface, f"Cook Progress: {progress_pct}%",
                         px + pw // 2, text_y + 18, color=(120, 230, 140), small=True)
            render_label(surface, "Perfect zone moves. Hold [SPACE] -> | release <-",
                         px + pw // 2, text_y + 34, color=(200, 200, 100), small=True)
        else:
            quality_col = (100, 255, 100) if self._fire_result == "perfect" else (200, 200, 200)
            quality_lbl = "Perfectly cooked!" if self._fire_result == "perfect" else "Cooked."
            render_label(surface, quality_lbl, px + pw // 2, text_y + 28, color=quality_col)
